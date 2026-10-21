#!/usr/bin/env python3
"""Probe B — independent readback of D2 (geomean) decks produced by the HEAD generator CLI.

My own deck parser (no generator import, no mixer_deck_readback import).  For each pair (i<=j, wall included) from the
PRINTED deck values (E, nu, template radius, density, CED):
  R*  = r_i r_j/(r_i+r_j)  (wall: r_i)        E* = 1/((1-nu_i^2)/E_i + (1-nu_j^2)/E_j)
  F0  = (9/2) pi^3 R*^2 CED^3 / E*^2  (generator nominal scale)
  Fpo = true SJKR+Hertz pull-off: max_delta [CED*A(delta) - (4/3)E* sqrt(R*) delta^1.5], A = exact LIGGGHTS SJKR area
        (sphere-sphere intersection circle; sphere-wall pi(2 r delta - delta^2))
Checks: F0_ij/F0_SS = sqrt(g_i g_j) R*_ij/R*_SS (print tol 3e-5) · Fpo ratios same law · Bo_SE = F0_SS / W_SE (W from the
deck's SE template radius + density, g 9.81) = --gm-bo-se · delta0/min r <= 1 % · symmetric · wall-wall 0 ·
deck_meta.adhesion_rule = argv · header table F0/F0_SS = my ratios.
usage: python3 -I probe_d2_readback.py   (writes probe_d2_readback.json)
"""
import json
import math
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'gen', 'mmd_HEAD.py')
G = 9.81


def logical(text):
    lines, out, i = text.split('\n'), [], 0
    while i < len(lines):
        buf = [lines[i]]
        while buf[-1].rstrip().endswith('&') and i + 1 < len(lines):
            i += 1
            buf.append(lines[i])
        joined = ' '.join(b.rstrip()[:-1] if b.rstrip().endswith('&') else b for b in buf)
        code = joined.split('#', 1)[0]
        if code.split():
            out.append(code.split())
        i += 1
    return out


def parse(text):
    D = dict(tpl={}, mesh=[])
    for t in logical(text):
        if t[0] == 'create_box':
            D['n'] = int(t[1])
        elif t[0] == 'fix' and len(t) > 5 and t[3] == 'property/global':
            if t[4] == 'youngsModulus':
                D['E'] = [float(x) for x in t[6:]]
            elif t[4] == 'poissonsRatio':
                D['nu'] = [float(x) for x in t[6:]]
            elif t[4] == 'cohesionEnergyDensity':
                n = int(t[6])
                v = [float(x) for x in t[7:]]
                assert len(v) == n * n
                D['ced'] = [v[k * n:(k + 1) * n] for k in range(n)]
        elif t[0] == 'fix' and len(t) > 3 and t[3] == 'particletemplate/sphere':
            at = int(t[t.index('atom_type') + 1])
            D['tpl'][at] = dict(rho=float(t[t.index('density') + 2]), r=float(t[t.index('radius') + 2]), seed=int(t[4]))
        elif t[0] == 'fix' and len(t) > 3 and t[3] == 'mesh/surface':
            D['mesh'].append(int(t[t.index('type') + 1]))
        elif t[0] == 'fix' and len(t) > 3 and t[3] == 'gravity':
            D['g'] = float(t[4])
    return D


SEED2PH = {10487: 'AM_P', 11887: 'AM_S', 13901: 'SE'}


def pulloff(ced, Es, ri, rj=None):
    """max tensile force of Hertz + SJKR (exact LIGGGHTS area) over overlap delta (golden section on [0, 0.2 r_min])."""
    Rs = ri if rj is None else ri * rj / (ri + rj)

    def area(dl):
        if rj is None:
            return math.pi * (2 * ri * dl - dl * dl)
        dist = ri + rj - dl
        return math.pi / 4.0 * ((dist - ri + rj) * (dist + ri - rj) * (ri + rj - dist) * (dist + ri + rj)) / dist ** 2

    def f(dl):
        return ced * area(dl) - (4.0 / 3.0) * Es * math.sqrt(Rs) * dl ** 1.5
    lo, hi = 0.0, 0.2 * (ri if rj is None else min(ri, rj))
    # coarse scan to bracket
    best = max(((f(lo + (hi - lo) * k / 4000.0), k) for k in range(1, 4001)))
    k = best[1]
    a, b = lo + (hi - lo) * (k - 1) / 4000.0, lo + (hi - lo) * (k + 1) / 4000.0
    gr = (math.sqrt(5) - 1) / 2
    c, d = b - gr * (b - a), a + gr * (b - a)
    for _ in range(200):
        if f(c) > f(d):
            b = d
        else:
            a = c
        c, d = b - gr * (b - a), a + gr * (b - a)
    return f(0.5 * (a + b))


def analyse(deck_text, meta, gamma, gwall, bo):
    D = parse(deck_text)
    n = D['n']
    names = {at: SEED2PH[v['seed']] for at, v in D['tpl'].items()}
    names[n] = 'WALL'
    assert sorted(set(D['mesh'])) == [n]
    g = dict(gamma)
    g['WALL'] = gwall
    ph = {nm: at for at, nm in names.items()}
    E, nu, C = D['E'], D['nu'], D['ced']
    r = {nm: D['tpl'][at]['r'] for at, nm in names.items() if nm != 'WALL'}
    rho_se = D['tpl'][ph['SE']]['rho']

    def Rst(a, b):
        if a == 'WALL':
            a, b = b, a
        return r[a] if b == 'WALL' else r[a] * r[b] / (r[a] + r[b])

    def Est(a, b):
        ia, ib = ph[a] - 1, ph[b] - 1
        return 1.0 / ((1 - nu[ia] ** 2) / E[ia] + (1 - nu[ib] ** 2) / E[ib])

    def F0(a, b):
        return 4.5 * math.pi ** 3 * Rst(a, b) ** 2 * C[ph[a] - 1][ph[b] - 1] ** 3 / Est(a, b) ** 2

    order = ['AM_P', 'AM_S', 'SE', 'WALL']
    rows, worst = [], 0.0
    fss = F0('SE', 'SE')
    pss = pulloff(C[ph['SE'] - 1][ph['SE'] - 1], Est('SE', 'SE'), r['SE'], r['SE'])
    for i, a in enumerate(order):
        for b in order[i:]:
            if a == b == 'WALL':
                rows.append(dict(pair='WALL-WALL', ced=C[n - 1][n - 1], ok=C[n - 1][n - 1] == 0.0))
                continue
            want = math.sqrt(g[a] * g[b]) * Rst(a, b) / Rst('SE', 'SE')
            got = F0(a, b) / fss
            ced = C[ph[a] - 1][ph[b] - 1]
            if a == 'WALL' or b == 'WALL':
                p_ = a if b == 'WALL' else b
                po = pulloff(ced, Est(a, b), r[p_], None)
            else:
                po = pulloff(ced, Est(a, b), r[a], r[b])
            rmin = min(r[x] for x in (a, b) if x != 'WALL')
            d0 = (3 * math.pi * ced * math.sqrt(Rst(a, b)) / (2 * Est(a, b))) ** 2 / rmin
            worst = max(worst, d0)
            rows.append(dict(pair=f'{a}-{b}', ced=ced, F0_ratio=got, want=want, rel=got / want - 1.0,
                             pulloff_ratio=po / pss, pulloff_rel=(po / pss) / want - 1.0, delta0_over_rmin=d0,
                             sym=C[ph[a] - 1][ph[b] - 1] == C[ph[b] - 1][ph[a] - 1]))
    W_se = (4.0 / 3.0) * math.pi * r['SE'] ** 3 * rho_se * D.get('g', G)
    bo_read = fss / W_se
    ar = (meta or {}).get('adhesion_rule', {})
    # header table F0/F0_SS
    hdr = {}
    for line in deck_text.split('\n'):
        s = line.strip('# ').split()
        if len(s) == 7 and '–' in s[0] and s[0].split('–')[0] in order:
            try:
                hdr[s[0].replace('–', '-')] = float(s[5])
            except ValueError:
                pass
    hdr_rel = max((abs(hdr[k] / rw['F0_ratio'] - 1.0) for rw in rows for k in hdr if k == rw['pair'] and 'F0_ratio' in rw),
                  default=None)
    out = dict(rows=rows, max_rel_F0=max(abs(rw['rel']) for rw in rows if 'rel' in rw),
               max_rel_pulloff=max(abs(rw['pulloff_rel']) for rw in rows if 'pulloff_rel' in rw),
               worst_delta0_over_rmin=worst, bo_se_read=bo_read, bo_se_rel=bo_read / bo - 1.0,
               all_sym=all(rw.get('sym', True) for rw in rows), wall_wall_zero=rows[-1]['ok'],
               meta_rule=ar.get('rule'), meta_gamma=ar.get('gamma'), meta_gamma_wall=ar.get('gamma_wall'),
               meta_bo=ar.get('bo_se'), meta_wall_rule=ar.get('wall_rule'), meta_rho=ar.get('rho_uncoated_ncm'),
               meta_dens_gen=(meta or {}).get('dens_gen'), rho_se_deck=rho_se,
               header_rows=len(hdr), header_vs_mine_max_rel=hdr_rel)
    return out


CASES = [
    ('coated_g1_w0256_lab_soft', ['--gm-gamma', 'AM_P=1,AM_S=1', '--gm-gamma-wall', '0.0256', '--gm-bo-se', '0.21244',
                                  '--dens-gen', 'lab20261014'], {'AM_P': 1, 'AM_S': 1, 'SE': 1}, 0.0256, 0.21244),
    ('uncoated_r03_ncm_lab_soft', ['--gm-gamma', 'AM_P=0.3,AM_S=0.3', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.21244',
                                   '--dens-gen', 'lab20261014'], {'AM_P': .3, 'AM_S': .3, 'SE': 1}, 0.0256 * 0.3, 0.21244),
    ('coated_world_r03_ncm_lab_soft', ['--gm-gamma', 'AM_P=1,AM_S=1', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.21244',
                                       '--dens-gen', 'lab20261014'], {'AM_P': 1, 'AM_S': 1, 'SE': 1}, 0.0256 * 0.3, 0.21244),
    ('mixed_03_05_w0256_lab_ref20', ['--gm-gamma', 'AM_P=0.3,AM_S=0.5', '--gm-gamma-wall', '0.0256', '--gm-bo-se', '0.21244',
                                     '--dens-gen', 'lab20261014', '--stiffen-se', '20', '--hold-bo-pairwise'],
     {'AM_P': .3, 'AM_S': .5, 'SE': 1}, 0.0256, 0.21244),
    ('coated_g1_gen1_soft', ['--gm-gamma', 'AM_P=1,AM_S=1', '--gm-gamma-wall', '0.0256', '--gm-bo-se', '0.21244',
                             '--dens-gen', 'gen1'], {'AM_P': 1, 'AM_S': 1, 'SE': 1}, 0.0256, 0.21244),
    ('sticky_AM_r10_ncm_lab_soft', ['--gm-gamma', 'AM_P=10,AM_S=10', '--gm-wall-ncm', '10', '--gm-bo-se', '5',
                                    '--dens-gen', 'lab20261014'], {'AM_P': 10, 'AM_S': 10, 'SE': 1}, 0.256, 5.0),
    ('coated_g1_bo637_lab_soft', ['--gm-gamma', 'AM_P=1,AM_S=1', '--gm-gamma-wall', '0.0256', '--gm-bo-se', '637.32',
                                  '--dens-gen', 'lab20261014'], {'AM_P': 1, 'AM_S': 1, 'SE': 1}, 0.0256, 637.32),
    ('coated_g1_bo637_gen1_soft', ['--gm-gamma', 'AM_P=1,AM_S=1', '--gm-gamma-wall', '0.0256', '--gm-bo-se', '637.32',
                                   '--dens-gen', 'gen1'], {'AM_P': 1, 'AM_S': 1, 'SE': 1}, 0.0256, 637.32),
    ('mixed_ref20_dthalf_fullprec', ['--gm-gamma', 'AM_P=0.3,AM_S=0.5', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.21244',
                                     '--dens-gen', 'lab20261014', '--stiffen-se', '20', '--hold-bo-pairwise',
                                     '--dt-factor', '0.5', '--dump-full-precision'],
     {'AM_P': .3, 'AM_S': .5, 'SE': 1}, 0.0256 * 0.3, 0.21244),
]
BASE = ['--n-total', '100000', '--cgf', '151.4', '--seed', '32452843', '--revolutions', '2']


def main():
  res = {}
  with tempfile.TemporaryDirectory(dir=HERE) as td:
    for label, args, gamma, gw, bo in CASES:
        out = os.path.join(td, label)
        p = subprocess.run([sys.executable, '-I', GEN, '--out', out] + BASE + args, capture_output=True, text=True,
                           env=dict(os.environ, OPENBLAS_NUM_THREADS='1'))
        rec = dict(rc=p.returncode, stderr_tail=p.stderr.strip().splitlines()[-1:] if p.returncode else [])
        if p.returncode == 0:
            dk = open(os.path.join(out, 'in.mixer'), encoding='utf-8').read()
            meta = json.load(open(os.path.join(out, 'deck_meta.json'), encoding='utf-8'))
            rec.update(analyse(dk, meta, gamma, gw, bo))
            rec['stale_wall_comment'] = [l for l in dk.split('\n') if '점착 = 입자값 ÷' in l]
            rec['wall_ced_div_comment_present'] = any('점착 = 입자값 ÷' in l for l in dk.split('\n'))
            rec['meta_pairs_F0_ratio'] = [(r_['pair'], r_['F0_ratio']) for r_ in meta.get('pairs', [])][:3]
        res[label] = rec
  json.dump(res, open(os.path.join(HERE, 'probe_d2_readback.json'), 'w'), ensure_ascii=False, indent=1)
  for k, v in res.items():
    if v['rc'] != 0:
        print(f'{k:34s} rc={v["rc"]} {v["stderr_tail"]}')
        continue
    print(f'{k:34s} rc=0 maxrelF0={v["max_rel_F0"]:.2e} maxrelPull={v["max_rel_pulloff"]:.2e} '
          f'worst d0/r={v["worst_delta0_over_rmin"]*100:.4f}% BoSE_rel={v["bo_se_rel"]:.2e} sym={v["all_sym"]} '
          f'ww0={v["wall_wall_zero"]} hdr={v["header_rows"]}:{v["header_vs_mine_max_rel"]} rho_se={v["rho_se_deck"]} '
          f'meta_gw={v["meta_gamma_wall"]} wallrule={v["meta_wall_rule"]} staleWallComment={v["wall_ced_div_comment_present"]}')


if __name__ == '__main__':
    main()

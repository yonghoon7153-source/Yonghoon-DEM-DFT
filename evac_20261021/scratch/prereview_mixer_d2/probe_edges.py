#!/usr/bin/env python3
"""Probe F — edge cases and counterexamples for the D2 path (HEAD generator + two surviving mutants).

 F1  M04 mutant (F0_SS uses gen1 SE density) on a lab20261014 D2 deck: SE-SE Bo read back from the printed deck vs declared.
 F2  M06 mutant (pairwise ceiling skips mixed pairs): search (gamma_AM, Bo_SE) where ONLY a mixed pair exceeds 1 %;
     HEAD must refuse, mutant writes the deck (overlap read back from the printed deck).
 F3  underflow: gamma_AM_P = 1e-200 (accepted as finite > 0) -> printed CED of AM_P-AM_P?;  Bo_SE = 1e-310 -> CLI outcome
 F4  --gm-wall-ncm rho not tied to the arm gammas (AM 0.3 with rho 3; AM_P 0.3 / AM_S 0.6 with rho 0.3) -> accepted?
 F5  determinism: same D2 CLI twice -> identical bytes
 F6  CLI parse quirks: AM_P=0_3 (underscore digits) · fullwidth digits · trailing comma · SE=1.0 given · lower-case key
 F7  library 5-phase (VGCF, PTFE) D2 arm: does deck() build, does ceiling hold?
usage: python3 -I -B probe_edges.py
"""
import importlib.util
import json
import math
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from probe_d2_readback import parse, SEED2PH  # noqa: E402

HEAD = os.path.join(HERE, 'gen', 'mmd_HEAD.py')
M04 = os.path.join(HERE, 'mut', 'M04_F0SS_gen1_density', 'make_mixer_deck.py')
M06 = os.path.join(HERE, 'mut', 'M06_ceiling_skip_mixed', 'make_mixer_deck.py')
BASE = ['--n-total', '100000', '--cgf', '151.4', '--seed', '32452843', '--revolutions', '2', '--dens-gen', 'lab20261014']
env = dict(os.environ, OPENBLAS_NUM_THREADS='1')
R = {}


def run(gen, out, args):
    p = subprocess.run([sys.executable, '-I', '-B', gen, '--out', out] + args, capture_output=True, text=True, env=env)
    return p


def read(out):
    t = open(os.path.join(out, 'in.mixer'), encoding='utf-8').read()
    D = parse(t)
    n = D['n']
    names = {at: SEED2PH[v['seed']] for at, v in D['tpl'].items()}
    names[n] = 'WALL'
    ph = {nm: at for at, nm in names.items()}
    r = {nm: D['tpl'][at]['r'] for at, nm in names.items() if nm != 'WALL'}
    rho = {nm: D['tpl'][at]['rho'] for at, nm in names.items() if nm != 'WALL'}

    def Rst(a, b):
        if a == 'WALL':
            a, b = b, a
        return r[a] if b == 'WALL' else r[a] * r[b] / (r[a] + r[b])

    def Est(a, b):
        ia, ib = ph[a] - 1, ph[b] - 1
        return 1.0 / ((1 - D['nu'][ia] ** 2) / D['E'][ia] + (1 - D['nu'][ib] ** 2) / D['E'][ib])

    def ced(a, b):
        return D['ced'][ph[a] - 1][ph[b] - 1]

    def F0(a, b):
        return 4.5 * math.pi ** 3 * Rst(a, b) ** 2 * ced(a, b) ** 3 / Est(a, b) ** 2

    def ov(a, b):
        rmin = min(r[x] for x in (a, b) if x != 'WALL')
        return (3 * math.pi * ced(a, b) * math.sqrt(Rst(a, b)) / (2 * Est(a, b))) ** 2 / rmin
    W = (4.0 / 3.0) * math.pi * r['SE'] ** 3 * rho['SE'] * 9.81
    pairs = [('AM_P', 'AM_P'), ('AM_P', 'AM_S'), ('AM_S', 'AM_S'), ('AM_P', 'SE'), ('AM_S', 'SE'), ('SE', 'SE'),
             ('AM_P', 'WALL'), ('AM_S', 'WALL'), ('SE', 'WALL')]
    return dict(text=t, bo_se=F0('SE', 'SE') / W, ov={f'{a}-{b}': ov(a, b) for a, b in pairs},
                ced={f'{a}-{b}': ced(a, b) for a, b in pairs})


with tempfile.TemporaryDirectory(dir=HERE) as td:
    # F1
    gm = ['--gm-gamma', 'AM_P=0.3,AM_S=0.5', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.5']
    ph_, pm_ = run(HEAD, os.path.join(td, 'f1h'), BASE + gm), run(M04, os.path.join(td, 'f1m'), BASE + gm)
    bh, bm = read(os.path.join(td, 'f1h'))['bo_se'], read(os.path.join(td, 'f1m'))['bo_se']
    R['F1'] = dict(declared=0.5, head_rc=ph_.returncode, mutant_rc=pm_.returncode, head_bo_read=bh, mutant_bo_read=bm,
                   mutant_over_declared=bm / 0.5, expected_ratio_2p00_over_1p64=2.00 / 1.64)
    # F2 — search: gamma_AM = rho (uncoated, AM stickier), Bo grid
    hit = None
    for g_am in (3.0, 10.0, 30.0, 100.0):
        for bo in (1, 2, 5, 10, 20, 50, 100, 200, 400, 800, 1600, 3200):
            args = BASE + ['--gm-gamma', f'AM_P={g_am:g},AM_S={g_am:g}', '--gm-wall-ncm', f'{g_am:g}', '--gm-bo-se', f'{bo:g}']
            h = run(HEAD, os.path.join(td, f'f2h_{g_am}_{bo}'), args)
            m = run(M06, os.path.join(td, f'f2m_{g_am}_{bo}'), args)
            if h.returncode != 0 and m.returncode == 0:
                rd = read(os.path.join(td, f'f2m_{g_am}_{bo}'))
                hit = dict(gamma_AM=g_am, bo_se=bo, head_rc=h.returncode, head_msg=h.stderr.strip().splitlines()[-1][:200],
                           mutant_rc=m.returncode, mutant_deck_overlaps_pct={k: round(v * 100, 4) for k, v in rd['ov'].items()})
                break
        if hit:
            break
    R['F2'] = hit
    # F3 underflow
    a1 = BASE + ['--gm-gamma', 'AM_P=1e-200,AM_S=0.3', '--gm-gamma-wall', '0.0256', '--gm-bo-se', '0.21244']
    p = run(HEAD, os.path.join(td, 'f3a'), a1)
    f3a = dict(rc=p.returncode)
    if p.returncode == 0:
        rd = read(os.path.join(td, 'f3a'))
        f3a.update(ced_AMP_AMP=rd['ced']['AM_P-AM_P'], ced_AMP_SE=rd['ced']['AM_P-SE'], ced_AMP_WALL=rd['ced']['AM_P-WALL'],
                   deck_line=[l for l in rd['text'].split('\n') if l.startswith('#   AM_P–AM_P') and 'F0' not in l][-1:])
    a2 = BASE + ['--gm-gamma', 'AM_P=0.3,AM_S=0.3', '--gm-gamma-wall', '0.0256', '--gm-bo-se', '1e-310']
    p2 = run(HEAD, os.path.join(td, 'f3b'), a2)
    f3b = dict(rc=p2.returncode, err_tail=p2.stderr.strip().splitlines()[-1:] if p2.returncode else [],
               deck_written=os.path.exists(os.path.join(td, 'f3b', 'in.mixer')))
    a3 = BASE + ['--gm-gamma', 'AM_P=1e-30,AM_S=0.3', '--gm-gamma-wall', '0.0256', '--gm-bo-se', '0.21244']
    p3 = run(HEAD, os.path.join(td, 'f3c'), a3)
    f3c = dict(rc=p3.returncode)
    if p3.returncode == 0:
        rd = read(os.path.join(td, 'f3c'))
        f3c.update(ced_AMP_AMP=rd['ced']['AM_P-AM_P'])
    R['F3'] = dict(gamma_1e_200=f3a, bo_1e_310=f3b, gamma_1e_30=f3c)
    # F4 rho not tied
    f4 = {}
    for lab, gg, rho in (('AM0.3_rho3', 'AM_P=0.3,AM_S=0.3', '3'), ('AMP0.3_AMS0.6_rho0.3', 'AM_P=0.3,AM_S=0.6', '0.3'),
                         ('AM0.5_rho0.3', 'AM_P=0.5,AM_S=0.5', '0.3')):
        p = run(HEAD, os.path.join(td, 'f4_' + lab), BASE + ['--gm-gamma', gg, '--gm-wall-ncm', rho, '--gm-bo-se', '0.21244'])
        f4[lab] = dict(rc=p.returncode)
        if p.returncode == 0:
            mt = json.load(open(os.path.join(td, 'f4_' + lab, 'deck_meta.json'), encoding='utf-8'))
            f4[lab].update(meta_gamma=mt['adhesion_rule']['gamma'], meta_rho=mt['adhesion_rule'].get('rho_uncoated_ncm'),
                           meta_gamma_wall=mt['adhesion_rule']['gamma_wall'])
    R['F4'] = f4
    # F5 determinism
    g5 = BASE + ['--gm-gamma', 'AM_P=0.3,AM_S=0.5', '--gm-wall-ncm', '0.3', '--gm-bo-se', '0.21244', '--stiffen-se', '20', '--hold-bo-pairwise']
    run(HEAD, os.path.join(td, 'f5a'), g5)
    env_h = dict(env, OPENBLAS_CORETYPE='Haswell')
    subprocess.run([sys.executable, '-I', '-B', HEAD, '--out', os.path.join(td, 'f5b')] + g5, capture_output=True, text=True, env=env_h)
    ta = open(os.path.join(td, 'f5a', 'in.mixer'), 'rb').read()
    tb = open(os.path.join(td, 'f5b', 'in.mixer'), 'rb').read()
    ma = json.load(open(os.path.join(td, 'f5a', 'deck_meta.json')))
    mb = json.load(open(os.path.join(td, 'f5b', 'deck_meta.json')))
    ma['argv'] = mb['argv'] = None
    R['F5'] = dict(deck_identical=ta == tb, meta_identical_minus_argv=ma == mb)
    # F6 parse quirks
    f6 = {}
    for lab, gg in (('underscore_0_3', 'AM_P=0_3,AM_S=0.3'), ('fullwidth', 'AM_P=０.３,AM_S=0.3'), ('trailing_comma', 'AM_P=0.3,AM_S=0.3,'),
                    ('SE_given_1.0', 'AM_P=0.3,AM_S=0.3,SE=1.0'), ('SE_given_1e0', 'AM_P=0.3,AM_S=0.3,SE=1e0'),
                    ('lowercase', 'am_p=0.3,AM_S=0.3'), ('dup', 'AM_P=0.3,AM_P=0.4,AM_S=0.3'), ('nan', 'AM_P=nan,AM_S=0.3'),
                    ('space', ' AM_P = 0.3 , AM_S=0.3')):
        p = run(HEAD, os.path.join(td, 'f6_' + lab), BASE + ['--gm-gamma', gg, '--gm-gamma-wall', '0.0256', '--gm-bo-se', '0.21244'])
        f6[lab] = dict(rc=p.returncode)
        if p.returncode == 0:
            mt = json.load(open(os.path.join(td, 'f6_' + lab, 'deck_meta.json'), encoding='utf-8'))
            f6[lab]['meta_gamma'] = mt['adhesion_rule']['gamma']
        else:
            f6[lab]['err'] = (p.stderr.strip().splitlines() or [''])[-1][:140]
    R['F6'] = f6

# F7 library 5-phase
s = importlib.util.spec_from_file_location('m5', HEAD)
M = importlib.util.module_from_spec(s)
s.loader.exec_module(M)
f7 = {}
try:
    M.set_phases(M.ALL_TYPES)
    nm = M.register_arm('GM5', M.gm_arm({'AM_P': 0.3, 'AM_S': 0.3, 'SE': 1.0, 'VGCF': 1.0, 'PTFE': 1.0}, gamma_wall=0.0256, bo_se=0.21244))
    p5 = M.plan(8000, dens_gen='lab20261014')
    try:
        t = M.deck(p5, 60, 2, arm=nm)
        f7['deck_ok'] = True
        f7['has_gm_header'] = 'D2 결합 규칙' in t
    except SystemExit as e:
        f7['deck_refused'] = str(e)[:200]
    except Exception as e:
        f7['deck_crash'] = repr(e)[:200]
finally:
    M.set_phases(('AM_P', 'AM_S', 'SE'))
R['F7'] = f7
json.dump(R, open(os.path.join(HERE, 'probe_edges.json'), 'w'), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False, indent=1)[:6000])

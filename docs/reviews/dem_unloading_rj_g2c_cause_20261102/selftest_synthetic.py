"""Synthetic validation of cause_check.analyze (local only).

Builds fake original / test contact dumps (LIGGGHTS %g, 26 c_cpl columns) and a
%.17g atom dump.  Injects:
  M1 for every pair: original history = P(h_prev + vtr_half*dt), test history = h_prev
  M2 for pairs that cross the 6x4 grid: original damping uses ghost (lower id) half-step v/omega
Optional modes: 'reset' (test history = 0), 'flipsign' (test history sign-flipped for orientation-changed pairs),
'none' (no M1: test history = original history).
"""
import math
import random
import sys
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('rj_g2c_cause_check', HERE / 'rj_g2c_cause_check.py')
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)

BOX = 0.05
DT = 1e-6
RAD = {1: 4.5e-3, 2: 2.0e-3, 3: 0.5e-3}
RHO = {1: 4800.0, 2: 4800.0, 3: 2000.0}


def g(v):
    return '%g' % v


def sub(a, b):
    return [a[k] - b[k] for k in range(3)]


def add(a, b):
    return [a[k] + b[k] for k in range(3)]


def scl(s, a):
    return [s * x for x in a]


def proj(v, e):
    d = cc.dot(v, e)
    return [v[k] - d * e[k] for k in range(3)]


def vtr_of(dl, e, va, vb, wa, wb, ra, rb, r):
    vr = sub(va, vb)
    vn = cc.dot(vr, e)
    vt = [vr[k] - vn * e[k] for k in range(3)]
    dn = ra + rb - r
    cri, crj = ra - 0.5 * dn, rb - 0.5 * dn
    wr = [(cri * wa[k] + crj * wb[k]) / r for k in range(3)]
    return [vt[0] - (dl[2] * wr[1] - dl[1] * wr[2]),
            vt[1] - (dl[0] * wr[2] - dl[2] * wr[0]),
            vt[2] - (dl[1] * wr[0] - dl[0] * wr[1])], vn


def build(outdir, npairs=6000, mode='m1m2', seed=7):
    rnd = random.Random(seed)
    outdir.mkdir(parents=True, exist_ok=True)
    atoms = {}
    pairs = []
    nid = 1
    for _ in range(npairs):
        ta = rnd.choice([1, 2, 3, 3, 3, 3])
        tb = rnd.choice([1, 2, 3, 3, 3, 3])
        ra, rb = RAD[ta], RAD[tb]
        xa = [rnd.uniform(0, BOX), rnd.uniform(0, BOX), rnd.uniform(0.01, 0.1)]
        u = [rnd.gauss(0, 1) for _ in range(3)]
        nu = cc.norm(u)
        u = [x / nu for x in u]
        r = (ra + rb) * (1 - rnd.uniform(1e-4, 2e-2))
        xb = [xa[k] - u[k] * r for k in range(3)]
        xb[0] %= BOX
        xb[1] %= BOX
        ids = [nid, nid + 1]
        rnd.shuffle(ids)
        nid += 2
        for aid, t, x in ((ids[0], ta, xa), (ids[1], tb, xb)):
            m = RHO[t] * 4 / 3 * math.pi * RAD[t] ** 3
            atoms[aid] = dict(t=t, x=x, r=RAD[t], m=m,
                              v=[rnd.gauss(0, 3e-3) for _ in range(3)],
                              w=[rnd.gauss(0, 8.0) for _ in range(3)],
                              f=[rnd.gauss(0, 2e-4) * (1 if t == 3 else 30) for _ in range(3)])
        pairs.append(tuple(ids))
    rows_o, rows_t = [], []
    for (p, q) in pairs:
        a, b = min(p, q), max(p, q)
        A, B = atoms[a], atoms[b]
        dl = [cc.mimage(A['x'][0] - B['x'][0]), cc.mimage(A['x'][1] - B['x'][1]), A['x'][2] - B['x'][2]]
        r = cc.norm(dl)
        e = [x / r for x in dl]
        kt, gam = cc.model(A['t'], B['t'], A['r'], B['r'], A['m'], B['m'])
        vha = sub(A['v'], scl(0.5 * DT / A['m'], A['f']))
        vhb = sub(B['v'], scl(0.5 * DT / B['m'], B['f']))
        wha = [x - rnd.gauss(0, 0.02) for x in A['w']]
        whb = [x - rnd.gauss(0, 0.02) for x in B['w']]
        vtr_half, _ = vtr_of(dl, e, vha, vhb, wha, whb, A['r'], B['r'], r)
        ca = cc.cell(A['x'][0] % BOX, A['x'][1] % BOX, (6, 4))[:2]
        cb = cc.cell(B['x'][0] % BOX, B['x'][1] % BOX, (6, 4))[:2]
        ghost = ca != cb
        fn_model = rnd.uniform(0.005, 0.05) * (30 if 1 in (A['t'], B['t']) else 1)
        hmag = rnd.uniform(0.05, 0.9) * cc.MU * fn_model / kt
        hp = proj([rnd.gauss(0, 1) for _ in range(3)], e)
        hp = scl(hmag / cc.norm(hp), hp)
        h_orig = proj(add(hp, scl(DT, vtr_half)), e)
        if mode == 'none':
            h_test = h_orig
        elif mode == 'reset':
            h_test = [0.0, 0.0, 0.0]
        else:
            h_test = hp
        vtr_t, vn_t = vtr_of(dl, e, A['v'], B['v'], A['w'], B['w'], A['r'], B['r'], r)
        if ghost and mode in ('m1m2', 'm2only'):
            vtr_o, vn_o = vtr_of(dl, e, vha, B['v'], wha, B['w'], A['r'], B['r'], r)
        else:
            vtr_o, vn_o = vtr_t, vn_t
        if mode == 'm2only':
            h_test = h_orig

        def force(h, vtr, vn):
            fn = fn_model - gam * vn
            ft = scl(-kt, h)
            if kt * cc.norm(h) > cc.MU * abs(fn):
                ft = scl(cc.MU * abs(fn) / (kt * cc.norm(h)), ft)
            else:
                ft = sub(ft, scl(gam, vtr))
            ft = proj(ft, e)
            return add(scl(fn, e), ft), scl(fn, e), ft
        Fo = force(h_orig, vtr_o, vn_o)
        Ft_ = force(h_test, vtr_t, vn_t)
        rev_o = True if ghost else (rnd.random() < 0.3)
        cr = cc.cell(A['x'][0] % BOX, A['x'][1] % BOX, (3, 2))[:2] != cc.cell(B['x'][0] % BOX, B['x'][1] % BOX, (3, 2))[:2]
        if cr:
            rev_t = True
        elif ghost:
            rev_t = rnd.random() < 0.5
        else:
            rev_t = rev_o
        if mode == 'flipsign' and rev_t != rev_o:
            Ft_ = force(scl(-1, h_test), vtr_t, vn_t)
        for rows, F, rev in ((rows_o, Fo, rev_o), (rows_t, Ft_, rev_t)):
            tot, fnv, ftv = F
            i, j = (b, a) if rev else (a, b)
            s = -1.0 if rev else 1.0
            Xi, Xj = atoms[i]['x'], atoms[j]['x']
            vals = Xi + Xj + [i, j, 0] + scl(s, tot) + scl(s, fnv) + scl(s, ftv) + [0.0, 0.0, 0.0] + \
                [1e-7, A['r'] + B['r'] - r] + [(Xi[k] + Xj[k]) / 2 for k in range(3)]
            rows.append(' '.join(g(v) if not isinstance(v, int) else str(v) for v in vals))
    head = ['ITEM: TIMESTEP', '3200000', 'ITEM: NUMBER OF ENTRIES', str(len(pairs)), 'ITEM: BOX BOUNDS pp pp fm',
            '0 0.05', '0 0.05', '-0.01 1', 'ITEM: ENTRIES ' + ' '.join(cc.COLUMNS)]
    (outdir / 'orig.c').write_text('\n'.join(head + rows_o) + '\n')
    rnd.shuffle(rows_t)
    (outdir / 'test.c').write_text('\n'.join(head + rows_t) + '\n')
    ah = ['ITEM: TIMESTEP', '3200000', 'ITEM: NUMBER OF ATOMS', str(len(atoms)), 'ITEM: BOX BOUNDS pp pp fm',
          '0 0.05', '0 0.05', '-0.01 1',
          'ITEM: ATOMS id type x y z radius mass vx vy vz omegax omegay omegaz fx fy fz f_history_zwall_bot[1]']
    al = []
    for aid, A in atoms.items():
        al.append('%d %d ' % (aid, A['t']) + ' '.join('%.17g' % v for v in A['x'] + [A['r'], A['m']] + A['v'] + A['w'] + A['f'] + [0.0]))
    (outdir / 'atoms.d').write_text('\n'.join(ah + al) + '\n')


if __name__ == '__main__':
    base = Path(sys.argv[1])
    for mode in ('m1m2', 'none', 'reset', 'flipsign', 'm2only'):
        d = base / mode
        build(d, mode=mode)
        res = cc.analyze(d / 'orig.c', d / 'test.c', d / 'atoms.d')
        fl = res['M1_fit']['local_stick']
        fg = res['M1_fit']['ghost_stick']
        m2 = res['M2_normal']['ghost']
        print(mode, 'pairs', res['n_pairs'], 'mismatch', res['gate_equivalent_mismatch'],
              'ghost_not_rev', res['orig_ghost_pairs_not_reversed'], 'test_viol', res['test_grid_violations'],
              '| M1 local', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in fl.items() if k in ('n', 'slope_obs_on_pred', 'r2_unit_slope', 'frac_resid_le_10pct')},
              '| M1 ghost', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in fg.items() if k in ('n', 'slope_obs_on_pred', 'r2_unit_slope')},
              '| M2 ghost', {k: (round(v, 4) if isinstance(v, float) else v) for k, v in m2.items()},
              '| M2 local n', res['M2_normal']['local'].get('n'),
              '| reset_like', res['reset_like_pairs'], 'signflip_like', res['sign_flip_like_pairs'],
              '| m1_pred_fail', res['M1_predicted_tangent_fail'])

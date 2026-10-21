"""Scratch probe — readback D2 check margins on many D2 decks (worst observed deviation vs registered tolerance)."""
import itertools
import math
import sys
sys.path.insert(0, sys.argv[1] + '/scripts')
import make_mixer_deck as g  # noqa: E402
import mixer_deck_readback as rb  # noqa: E402

worst = dict(law=0.0, bo=0.0, hdr=0.0, ovl=0.0)
n = 0
bad = []
for gen, F, dtf, cgf in itertools.product(('lab20261014', 'gen1'), (1.0, 20.0, 40.0), (1.0, 0.5), (151.4, 200.0, 123.4, 157.31234, 141.42136)):
    for gp, gs, rho, bo, wall in ((0.3, 0.3, 0.3, 0.5, None), (1.0, 1.0, 0.3, 0.5, None), (1.0, 0.3, 0.3, 0.5, None),
                                  (1.0, 1.0, 1.0, 600.0, None), (1.0, 1.0, None, 50.0, 0.0256), (0.123457, 1.0, 0.123457, 3.7, None),
                                  (1.0, 1.0, None, 2.5, 0.0013), (2.5, 2.5, 2.5, 0.05, None)):
        p = g.plan(100000, cgf=cgf, stiffen_se=F, dens_gen=gen)
        try:
            if wall is None:
                a = g.gm_arm({'AM_P': gp, 'AM_S': gs, 'SE': 1.0}, gamma_wall=g.gm_wall_from_ncm(rho), bo_se=bo, rho_uncoated_ncm=rho)
            else:
                a = g.gm_arm({'AM_P': gp, 'AM_S': gs, 'SE': 1.0}, gamma_wall=wall, bo_se=bo)
            nm = g.register_arm('GMPR', a)
        except SystemExit as e:
            print('arm refused', gp, gs, rho, bo, wall, str(e)[:80])
            continue
        try:
            rpm = g.resolve_rpm(p['R'])
            t = g.deck(p, rpm, 2, seed=32452843, arm=nm, hold_bo_pairwise=(F != 1.0), dt_factor=dtf)
            m = g.deck_meta(p, rpm, 2, 32452843, nm, t, argv=['x'], hold_bo_pairwise=(F != 1.0), dt_factor=dtf)
        except SystemExit as e:
            print('deck refused', gen, F, dtf, cgf, gp, gs, rho, bo, wall, str(e)[:90])
            g.ARMS.pop(nm, None)
            continue
        g.ARMS.pop(nm, None)
        D = rb.read_deck(t, 'x', meta=m)
        R = rb.d2_check(D)
        n += 1
        if R['problems']:
            bad.append((gen, F, dtf, cgf, gp, gs, rho, bo, wall, R['problems'][:3]))
            continue
        worst['bo'] = max(worst['bo'], abs(R['bo_read'] / bo - 1))
        for r_ in R['rows']:
            if r_['pair'] == 'WALL–WALL':
                continue
            worst['law'] = max(worst['law'], abs(r_['F0_ratio'] / r_['expect'] - 1))
            h = R['decl']['table'][r_['pair']]
            for col, val in (('R_star', r_['R_star']), ('E_star', r_['E_star']), ('F0', r_['F0']), ('ratio', r_['F0_ratio'])):
                worst['hdr'] = max(worst['hdr'], abs(float(h[col]) / val - 1))
            worst['ovl'] = max(worst['ovl'], abs(float(h['ovl']) - r_['overlap'] * 100))
print('decks checked', n, 'with problems', len(bad))
for b in bad[:10]:
    print('  BAD', b)
print('worst observed:', {k: f'{v:.3g}' for k, v in worst.items()})
print('tolerances    :', {k: f"{rb.TOL[t]:.3g}" for k, t in (('law', 'gm_law_rel'), ('bo', 'gm_bo_rel'), ('hdr', 'gm_hdr_rel'), ('ovl', 'gm_ovl_abs'))})

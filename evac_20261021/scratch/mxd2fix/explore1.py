"""Exploration (scratch) — numbers to design MXD2 tests.  usage: python3 -B explore1.py <repo>"""
import math
import os
import sys

REPO = sys.argv[1]
sys.path.insert(0, os.path.join(REPO, 'scripts'))
import make_mixer_deck as g  # noqa: E402

LAB = 'lab20261014'
p = g.plan(100000, cgf=151.4, dens_gen=LAB)
print('lab counts', {t: p['n'][t] for t in g.TYPES}, 'gen1', {t: g.plan(100000, cgf=151.4)['n'][t] for t in g.TYPES})

# M07 search — uncoated sticky AM world (gamma = rho), F < 1, soft passes, softened mixed pair exceeds while diag/wall stay below
for rho in (3.0, 10.0, 30.0):
    for bo in (50, 100, 200, 300, 400, 500, 600, 700, 800):
        try:
            a = g.gm_arm({'AM_P': rho, 'AM_S': rho, 'SE': 1.0}, gamma_wall=g.gm_wall_from_ncm(rho), bo_se=bo, rho_uncoated_ncm=rho)
        except SystemExit as e:
            continue
        try:
            Ms = g.ced_matrix_geomean(a, p['d'], dens=p['dens'])
        except SystemExit as e:
            continue
        for F in (0.5, 0.25):
            pF = g.plan(100000, cgf=151.4, stiffen_se=F, dens_gen=LAB)
            Mn = g.hold_bo_pairwise_matrix(Ms, g.E_PHASE, pF['E'])
            names = list(g.TYPES) + [g.WALL]
            ov = {}
            for i in range(len(names)):
                for j in range(i, len(names)):
                    if names[i] == g.WALL and names[j] == g.WALL:
                        continue
                    ov[f'{names[i]}-{names[j]}'] = g.pair_overlap(Mn[i][j], names[i], names[j], pF['d'], pF['E']) * 100
            diag_wall = max(v for k, v in ov.items() if k.split('-')[0] == k.split('-')[1] or 'WALL' in k)
            mixed = max(v for k, v in ov.items() if not (k.split('-')[0] == k.split('-')[1] or 'WALL' in k))
            if mixed > 1.0 and diag_wall < 1.0:
                print(f'M07 case rho {rho} bo {bo} F {F}: mixed max {mixed:.3f} % diag/wall max {diag_wall:.3f} % ',
                      {k: round(v, 3) for k, v in ov.items()})
                break

print(repr(float('0_3')), repr(float('０.３')), repr(float(' 0.3 ')))

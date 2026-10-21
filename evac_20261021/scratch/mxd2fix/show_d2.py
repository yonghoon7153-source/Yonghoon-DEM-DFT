"""Print the D2 deck header + key command lines + deck_meta (scratch)."""
import json
import sys
sys.path.insert(0, sys.argv[1] + '/scripts')
import make_mixer_deck as g  # noqa: E402

gp, gs, rho, bo, F = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])
gen = sys.argv[7] if len(sys.argv) > 7 else 'lab20261014'
wall = sys.argv[8] if len(sys.argv) > 8 else None
p = g.plan(100000, cgf=151.4, stiffen_se=F, dens_gen=gen)
if wall:
    a = g.gm_arm({'AM_P': gp, 'AM_S': gs, 'SE': 1.0}, gamma_wall=float(wall), bo_se=bo)
else:
    a = g.gm_arm({'AM_P': gp, 'AM_S': gs, 'SE': 1.0}, gamma_wall=g.gm_wall_from_ncm(rho), bo_se=bo, rho_uncoated_ncm=rho)
nm = g.register_arm('GMSHOW', a)
rpm = g.resolve_rpm(p['R'])
t = g.deck(p, rpm, 2, seed=32452843, arm=nm, hold_bo_pairwise=(F != 1.0))
m = g.deck_meta(p, rpm, 2, 32452843, nm, t, argv=['(show)'], hold_bo_pairwise=(F != 1.0))
lines = t.split('\n')
for i, l in enumerate(lines[:140]):
    print(f'{i+1:4d}| {l}')
print('...')
for i, l in enumerate(lines):
    if l.startswith(('fix gravi', 'fix pts', 'fix mC', 'create_box', 'timestep', 'fix m1', 'fix m2', 'fix m3', 'fix m4', 'fix m5')) or 'cohesionEnergy' in l or 'density constant' in l:
        print(f'{i+1:4d}| {l[:200]}')
print(json.dumps(m, ensure_ascii=False, indent=1)[:4000])

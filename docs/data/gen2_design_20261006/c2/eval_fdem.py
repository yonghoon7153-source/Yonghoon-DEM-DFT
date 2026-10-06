"""Gen-3 option magnitudes on real_14 (multiply ψ): NATIVE (A = c_cpl[22] for every pair) and
FDEM (Tabor with the DEM's own normal force: A = max(A_ligg, min(F_DEM,real/H, V_lens/h, π r_min²)))."""
import sys, os, math, time
import numpy as np
from g2lib import PC, load_bed, build_nets, edge_sigk, rc_from_area, solve, pair_kind

bed = sys.argv[1]
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', bed)
files = {'real14': ('atom_2060000.liggghts', 'contact_2060000.liggghts', 'input_real_14.liggghts', 'mesh_2060000.stl'),
         'case15': ('atom_1710000.liggghts', 'contact_1710000.liggghts', 'input_case15.liggghts', 'mesh_v4_1710000.stl')}[bed]
atoms, contacts, tm, pz, box = load_bed(*[os.path.join(D, f) for f in files])
fmag = {}
for c in contacts:
    fmag[(min(c['id1'], c['id2']), max(c['id1'], c['id2']))] = float(np.linalg.norm(c['fn']))
nets = build_nets(atoms, contacts, tm, pz, box)
S = 1000.0
for ch in ('ionic', 'electronic', 'thermal'):
    net = nets[ch]; mode = ch
    out = {}
    for var in ('NATIVE', 'FDEM'):
        saved = [(e['R_constriction'], e['R_total']) for e in net['edges']]
        nfl = 0
        for e in net['edges']:
            lg = e['A_hertzian']
            if var == 'NATIVE' or e['delta'] <= 0:
                A = lg
            else:
                F_real = fmag[(min(e['id1'], e['id2']), max(e['id1'], e['id2']))] * 1e-3   # N
                A_tab = F_real / PC.H_REAL_SE * 1e12                                       # µm²
                d = e['delta'] * S
                A_vol = PC.lens_volume(e['r1'], e['r2'], d) / 0.005
                A = max(lg, min(A_tab, A_vol, math.pi * min(e['r1'], e['r2']) ** 2))
                nfl += (A == lg)
            Rc, s, psi = rc_from_area(A, e['r1'], e['r2'], edge_sigk(e, tm, mode), 'multiply')
            e['R_constriction'] = Rc; e['R_total'] = e['R_bulk'] + Rc
        out[var] = (solve(net), nfl / len(net['edges']))
        for e, (rc, rt) in zip(net['edges'], saved):
            e['R_constriction'] = rc; e['R_total'] = rt
    print(f'[{bed}] {ch}: NATIVE|multiply σ={out["NATIVE"][0]:.6g}   FDEM|multiply σ={out["FDEM"][0]:.6g} '
          f'(floor binds {100*out["FDEM"][1]:.1f}% of edges)')

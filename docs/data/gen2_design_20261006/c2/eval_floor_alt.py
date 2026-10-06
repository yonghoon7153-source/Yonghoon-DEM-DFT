"""Author option for rule B's floor: DEM disc c_cpl[22] (recommended) vs elastic Hertz πR*δ — real_14, multiply ψ."""
import os, math, sys
from g2lib import load_bed, build_nets, edge_sigk, rc_from_area, pair_kind, area_variant
from fastsolve import fast_sigma
from proposed_film_area_g2 import film_area_g2, geom_disc

bed = sys.argv[1] if len(sys.argv) > 1 else 'real14'
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', bed)
files = {'real14': ('atom_2060000.liggghts', 'contact_2060000.liggghts', 'input_real_14.liggghts', 'mesh_2060000.stl'),
         'case15': ('atom_1710000.liggghts', 'contact_1710000.liggghts', 'input_case15.liggghts', 'mesh_v4_1710000.stl')}[bed]
atoms, contacts, tm, pz, box = load_bed(*[os.path.join(D, f) for f in files])
nets = build_nets(atoms, contacts, tm, pz, box)
for ch in ('ionic', 'electronic', 'thermal'):
    net = nets[ch]
    res = {}
    for floor_kind in ('disc', 'hertz'):
        saved = [(e['R_constriction'], e['R_total']) for e in net['edges']]
        for e in net['edges']:
            d = e['delta'] * 1000.0
            P = pair_kind(e['type1'], e['type2'], tm)
            lg = e['A_hertzian']
            if d > 0:
                Rs = e['r1'] * e['r2'] / (e['r1'] + e['r2'])
                fl = lg if floor_kind == 'disc' else math.pi * Rs * d
                A, _ = film_area_g2(d, e['r1'], e['r2'], pair=P, ligg_area=fl, length_scale=1e6, consumer='transport')
            else:
                A = lg
            Rc, s, psi = rc_from_area(A, e['r1'], e['r2'], edge_sigk(e, tm, ch), 'multiply')
            e['R_constriction'] = Rc; e['R_total'] = e['R_bulk'] + Rc
        res[floor_kind] = fast_sigma(net)
        for e, (rc, rt) in zip(net['edges'], saved):
            e['R_constriction'] = rc; e['R_total'] = rt
    print(f'[{bed}] {ch}: g2 floor=disc σ={res["disc"]:.6g}   floor=πR*δ σ={res["hertz"]:.6g}  ({100*(res["hertz"]/res["disc"]-1):+.2f}%)')

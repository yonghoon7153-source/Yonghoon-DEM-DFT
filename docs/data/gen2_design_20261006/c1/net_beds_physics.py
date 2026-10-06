#!/usr/bin/env python3
"""designC1 — context for the APPROVED Physics psi switch on the two committed beds (ionic):
Physics FULL with legacy_divide vs multiply (HEAD module arms), cylinder bulk vs Wiener bulk,
HEAD adaptive electrodes vs exact Dirichlet.  T = phi_sum / sigma_ratio (gap basis)."""
import contextlib
import io
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from beds import load, nc_module          # noqa: E402
from netsolve import perc_component, solve_adaptive, solve_dirichlet   # noqa: E402
from net_beds import edge_geom, wiener_half   # noqa: E402


def run(bed):
    A, C, b = load(bed)
    nc = nc_module()
    se = [k for k, v in b['type_map'].items() if v == 'SE']
    out = {'bed': bed}
    phi = None
    for psi_pl in (nc.PSI_DIVIDE, nc.PSI_MULTIPLY):
        with contextlib.redirect_stdout(io.StringIO()):
            net = nc.build_network(A, C, se, 1000.0, b['plate_z'], b['box'], b['box'], 2.0, mode='ionic',
                                   type_map=b['type_map'], contact_mode='physics', psi_placement=psi_pl)
        perc = perc_component(net)
        if phi is None:
            phi = sum(4 / 3 * math.pi * A[i]['radius'] ** 3 for i in net['nodes']) / (b['box'] ** 2 * b['plate_z'])
        Rb = np.array([e['R_bulk'] for e in net['edges']])
        Rc = np.array([e['R_constriction'] for e in net['edges']])
        RW = np.array([wiener_half(e['r1'], edge_geom(e)[2]) + wiener_half(e['r2'], edge_geom(e)[3]) for e in net['edges']])
        inperc = np.array([(e['id1'] in perc and e['id2'] in perc) for e in net['edges']])
        a_s = np.array([edge_geom(e)[1] for e in net['edges']])
        out[f'{psi_pl}_frac_Rc0'] = float((Rc[inperc] == 0).mean())
        out[f'{psi_pl}_s_phys_median'] = float(np.median(a_s[inperc]))
        for name, R in (('cyl', Rb + Rc), ('W', RW + Rc)):
            Ga, sa, _ = solve_adaptive(net, R, perc)
            Gd, sd, _ = solve_dirichlet(net, R, perc)
            out[f'{psi_pl}_{name}'] = dict(sigma_adaptive=sa, sigma_dirichlet=sd, T_dirichlet=phi / sd)
    out['phi'] = phi
    return out


if __name__ == '__main__':
    res = [run(b) for b in (sys.argv[1:] or ['real14', 'case15'])]
    with open(os.path.join(HERE, 'net_beds_physics.json'), 'w') as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))

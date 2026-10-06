#!/usr/bin/env python3
"""designC1 — calibrate a per-bed proxy for the 194 LHS beds (raw contacts are not in the repo).

On the two committed beds: compare the exact sigma ratios (net_beds.py) with first-order (Thomson)
estimates built from quantities that ARE stored per LHS bed:
  p_c  = constriction_power_share_ion_hertz (H0 FULL solution)
  s_A  = sqrt(area_SE_SE_mean/pi)/r_SE      (mean geometric-disc area)
Estimate:  sigma_H1/sigma_H0 ~ 1/(1 - p_c*(1 - psi(k*s_A)))     (k = s-proxy factor)
           sigma_H12/sigma_H1 ~ 1/(1 + (1-p_c1)*(kb - 1)),  kb = 3/(2 + s^2) (Wiener/cylinder, lens geom.)
"""
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
from netsolve import perc_component, solve_dirichlet   # noqa: E402
from net_beds import variants             # noqa: E402


def psi(s):
    return max(1.0 - s, 0.0) ** 1.5


def run(bed):
    A, C, b = load(bed)
    nc = nc_module()
    se = [k for k, v in b['type_map'].items() if v == 'SE']
    with contextlib.redirect_stdout(io.StringIO()):
        net = nc.build_network(A, C, se, 1000.0, b['plate_z'], b['box'], b['box'], 2.0,
                               mode='ionic', type_map=b['type_map'], contact_mode='hertzian')
    perc = perc_component(net)
    R, geo = variants(net)
    E = net['edges']
    inperc = np.array([(e['id1'] in perc and e['id2'] in perc) for e in E])
    r_se = np.median([e['r1'] for e in E])
    # mean geometric-disc area over ALL SE-SE contacts (what area_SE_SE_mean stores) and over perc edges
    Aall = np.array([e['A_hertzian'] for e in E])
    s_A_all = math.sqrt(Aall.mean() / math.pi) / r_se
    out = {'bed': bed, 'r_se': r_se, 's_meanA_all': s_A_all}
    G0, s0, x0 = solve_dirichlet(net, R['Rb_cyl'] + R['Rc_max'], perc, return_V=True)
    V, idx, Ek, Rk = x0['V'], x0['idx'], x0['E'], x0['Rk']
    key = {id(e): k for k, e in enumerate(E)}
    kk = np.array([key[id(e)] for e in Ek])
    I = np.array([V[idx[e['id1']]] - V[idx[e['id2']]] for e in Ek]) / Rk
    Pc = I * I * R['Rc_max'][kk]
    Pb = I * I * R['Rb_cyl'][kk]
    p_c = Pc.sum() / (Pc.sum() + Pb.sum())
    s = geo[kk, 1]
    psis = np.array([psi(x) for x in s])
    psi_Pc = float((Pc * psis).sum() / Pc.sum())
    kb = R['Rb_W'][kk] / R['Rb_cyl'][kk]
    kb_Pb = float((Pb * kb).sum() / Pb.sum())
    out.update(p_c=p_c, psi_powerweighted=psi_Pc, kb_powerweighted=kb_Pb)
    # Thomson first-order (upper bound on new R => lower bound on new sigma)
    out['H1_over_H0_thomson'] = 1.0 / (1.0 - p_c * (1.0 - psi_Pc))
    G1, s1, x1 = solve_dirichlet(net, R['Rb_cyl'] + R['Rc_psi'], perc, return_V=True)
    G12, s12, _ = solve_dirichlet(net, R['Rb_W'] + R['Rc_psi'], perc)
    out['H1_over_H0_exact'] = s1 / s0
    out['H12_over_H0_exact'] = s12 / s0
    # power shares in H1 solution for the second step
    V1, idx1, Ek1, Rk1 = x1['V'], x1['idx'], x1['E'], x1['Rk']
    kk1 = np.array([key[id(e)] for e in Ek1])
    I1 = np.array([V1[idx1[e['id1']]] - V1[idx1[e['id2']]] for e in Ek1]) / Rk1
    Pc1 = I1 * I1 * R['Rc_psi'][kk1]
    Pb1 = I1 * I1 * R['Rb_cyl'][kk1]
    pb1 = Pb1.sum() / (Pc1.sum() + Pb1.sum())
    kb1 = float((Pb1 * (R['Rb_W'][kk1] / R['Rb_cyl'][kk1])).sum() / Pb1.sum())
    out['H12_over_H1_thomson'] = 1.0 / (1.0 + pb1 * (kb1 - 1.0))
    out['H12_over_H1_exact'] = s12 / s1
    # proxy from stored quantities only: psi at k*s_A for k in a small grid
    for k in (0.7, 0.8, 0.9, 1.0):
        out[f'H1_over_H0_proxy_k{k}'] = 1.0 / (1.0 - p_c * (1.0 - psi(k * s_A_all)))
    out['kb_proxy_sA'] = 3.0 / (2.0 + s_A_all ** 2)
    return out


if __name__ == '__main__':
    res = [run(b) for b in (sys.argv[1:] or ['real14', 'case15'])]
    with open(os.path.join(HERE, 'net_beds_diag.json'), 'w') as fh:
        json.dump(res, fh, indent=1)
    for r in res:
        print(json.dumps(r, indent=1))

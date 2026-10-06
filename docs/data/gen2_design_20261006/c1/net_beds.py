#!/usr/bin/env python3
"""designC1 — edge-model variants on the two committed production beds (ionic SE-SE network).

Variants (rho = 1 as in the module; ionic channel => sigma_rel = k_weight = 1):
  H0   current Hertz      : R_bulk cylinder (d/2)/(pi r^2) each side + R_c = 1/(2a)            [HEAD]
  H1   fix (1)            : R_bulk cylinder + R_c = psi(a/r_min)/(2a)    (multiply, same as physics S3)
  H12  fix (1)+(2)        : R_bulk = sum_i h_i^2/V_seg,i (Wiener rod of the sphere segment) + psi/(2a)
  CF0 / CF2               : bulk-only branches of H0 / H12
Boundary: 'adaptive' = HEAD g_boundary rule · 'dirichlet' = proposed L2-05 fix.

Writes net_beds_<bed>.json with s-distribution (all + current-weighted) and sigma/f/T per variant.
"""
import contextlib
import io
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from beds import load, nc_module          # noqa: E402
from netsolve import perc_component, solve_adaptive, solve_dirichlet   # noqa: E402

PSI_FLOOR = 1e-4


def psi(s):
    return max(1.0 - s, 0.0) ** 1.5


def edge_geom(e):
    r1, r2, d = e['r1'], e['r2'], e['d_ij']
    a = math.sqrt(e['A_contact'] / math.pi) if e['A_contact'] > 0 else 0.0
    rmin = min(r1, r2)
    s = min(a, rmin) / rmin if rmin > 0 else 0.0
    # contact-plane distances from each centre (lens geometry)
    h1 = (d * d + r1 * r1 - r2 * r2) / (2 * d) if d > 0 else 0.0
    h2 = d - h1
    h1 = min(max(h1, 0.0), r1)
    h2 = min(max(h2, 0.0), r2)
    a_geo = math.sqrt(max(r1 * r1 - h1 * h1, 0.0))
    return a, s, h1, h2, a_geo


def wiener_half(r, h):
    """h^2/V_seg — resistance (sigma=1) of the uniform rod with the volume of the sphere slab between the
    centre plane and the contact plane (Wiener/variational lower bound for that slab)."""
    if h <= 0:
        return 0.0
    V = math.pi * (r * r * h - h ** 3 / 3.0)
    return h * h / V


def variants(net):
    E = net['edges']
    out = {k: np.zeros(len(E)) for k in ('Rb_cyl', 'Rc_max', 'Rc_psi', 'Rb_W')}
    geo = np.zeros((len(E), 5))
    for k, e in enumerate(E):
        a, s, h1, h2, a_geo = edge_geom(e)
        geo[k] = (a, s, h1, h2, a_geo)
        out['Rb_cyl'][k] = e['R_bulk']
        out['Rc_max'][k] = e['R_Maxwell'] if a > 0 else 1e12
        p = psi(s)
        out['Rc_psi'][k] = (p * e['R_Maxwell']) if (a > 0 and p > PSI_FLOOR) else (0.0 if a > 0 else 1e12)
        out['Rb_W'][k] = wiener_half(e['r1'], h1) + wiener_half(e['r2'], h2)
    return out, geo


def run(bed):
    t0 = time.time()
    A, C, b = load(bed)
    nc = nc_module()
    se = [k for k, v in b['type_map'].items() if v == 'SE']
    res = {'bed': bed}
    with contextlib.redirect_stdout(io.StringIO()):
        net = nc.build_network(A, C, se, 1000.0, b['plate_z'], b['box'], b['box'], 2.0,
                               mode='ionic', type_map=b['type_map'], contact_mode='hertzian')
    perc = perc_component(net)
    V_se = sum(4 / 3 * math.pi * A[i]['radius'] ** 3 for i in net['nodes'])
    phi = V_se / (b['box'] ** 2 * b['plate_z'])
    res.update(n_nodes=len(net['nodes']), n_edges=len(net['edges']), n_perc=len(perc), phi_se=phi,
               boundary_rule=net['boundary_rule'], band_frac=net['boundary_band_frac'],
               n_bottom=len(net['bottom']), n_top=len(net['top']))
    R, geo = variants(net)
    inperc = np.array([(e['id1'] in perc and e['id2'] in perc) for e in net['edges']])
    s = geo[:, 1]
    res['s_all'] = {q: float(np.percentile(s[inperc], q)) for q in (5, 10, 25, 50, 75, 90, 95)}
    res['s_mean'] = float(s[inperc].mean())
    # geometric-disc check: c_cpl[22] area vs lens a_geo
    agap = geo[inperc, 0] / np.where(geo[inperc, 4] > 0, geo[inperc, 4], np.nan)
    res['a_over_ageo_median'] = float(np.nanmedian(agap))
    res['a_over_ageo_p01_p99'] = [float(np.nanpercentile(agap, 1)), float(np.nanpercentile(agap, 99))]
    # ratios of the new bulk to the old bulk
    rb = R['Rb_W'][inperc] / R['Rb_cyl'][inperc]
    res['RbW_over_Rbcyl'] = {q: float(np.percentile(rb, q)) for q in (5, 50, 95)}
    combos = {
        'H0_full': R['Rb_cyl'] + R['Rc_max'],
        'H1_full': R['Rb_cyl'] + R['Rc_psi'],
        'H12_full': R['Rb_W'] + R['Rc_psi'],
        'H2_full': R['Rb_W'] + R['Rc_max'],
        'CF0': np.where(R['Rb_cyl'] > 0, R['Rb_cyl'], 1e-12),
        'CF2': np.where(R['Rb_W'] > 0, R['Rb_W'], 1e-12),
    }
    sol = {}
    for name, Rv in combos.items():
        Ga, sa, xa = solve_adaptive(net, Rv, perc)
        Gd, sd, xd = solve_dirichlet(net, Rv, perc, return_V=(name in ('H0_full', 'H1_full', 'H12_full')))
        sol[name] = dict(sigma_adaptive=sa, sigma_dirichlet=sd, T_adaptive=phi / sa, T_dirichlet=phi / sd,
                         dirichlet_over_adaptive=sd / sa, g_boundary=xa['g_boundary'], sum_g=xa['sum_g'],
                         G_over_sumg=Gd / xd['sum_g'], I_bot_minus_I_top=xd['I_bot'] + xd['I_top'])
        if 'V' in xd:
            # current-weighted s distribution + constriction power share for this variant
            Vv, idx, Ek, Rk = xd['V'], xd['idx'], xd['E'], xd['Rk']
            I = np.array([(Vv[idx[e['id1']]] - Vv[idx[e['id2']]]) for e in Ek]) / Rk
            P = I * I * Rk
            keymap = {id(e): k for k, e in enumerate(net['edges'])}
            kk = np.array([keymap[id(e)] for e in Ek])
            Rc_part = {'H0_full': R['Rc_max'], 'H1_full': R['Rc_psi'], 'H12_full': R['Rc_psi']}[name][kk]
            sol[name]['constriction_power_share'] = float((I * I * Rc_part).sum() / P.sum())
            sk = s[kk]
            w = P / P.sum()
            order = np.argsort(sk)
            cw = np.cumsum(w[order])
            sol[name]['s_power_weighted'] = {q: float(sk[order][np.searchsorted(cw, q / 100.0)])
                                             for q in (10, 25, 50, 75, 90)}
    res['solutions'] = sol
    # baseline cross-check against the HEAD module solve_network (FULL & CF)
    with contextlib.redirect_stdout(io.StringIO()):
        Gm, sm = nc.solve_network(net, mode='full')
        Gc, sc = nc.solve_network(net, mode='bulk_only')
    res['module_check'] = dict(sigma_full_module=sm, sigma_full_mine=sol['H0_full']['sigma_adaptive'],
                               rel_full=(sol['H0_full']['sigma_adaptive'] / sm - 1) if sm else None,
                               sigma_cf_module=sc, sigma_cf_mine=sol['CF0']['sigma_adaptive'],
                               rel_cf=(sol['CF0']['sigma_adaptive'] / sc - 1) if sc else None)
    res['seconds'] = time.time() - t0
    return res


if __name__ == '__main__':
    for bed in (sys.argv[1:] or ['real14', 'case15']):
        r = run(bed)
        with open(os.path.join(HERE, f'net_beds_{bed}.json'), 'w') as fh:
            json.dump(r, fh, indent=1)
        print(json.dumps({k: v for k, v in r.items() if k != 'solutions'}, indent=1))
        for k, v in r['solutions'].items():
            print(k, {kk: (round(vv, 6) if isinstance(vv, float) else vv) for kk, vv in v.items()})

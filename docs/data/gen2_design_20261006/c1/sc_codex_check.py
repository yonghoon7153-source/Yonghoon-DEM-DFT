#!/usr/bin/env python3
"""designC1 — Codex 3x3xNz simple-cubic CF check through the REAL build_network (HEAD snapshot):
non-overlapping touching spheres (r = 0.5 um, d = 1 um), tiny contact area only for adjacency.
CF0 = HEAD cylinder bulk · CF2 = Wiener sphere-segment bulk.  T = phi_sum/sigma_ratio (plate box)."""
import contextlib, io, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from beds import nc_module
from netsolve import solve_adaptive, solve_dirichlet, perc_component
from net_beds import edge_geom, wiener_half
nc = nc_module()
r = 0.5e-3; d = 1.0e-3                      # sim units (scale 1000 -> um)
for Nz in (20, 40, 80):
    A = {}; k = 0
    for i in range(3):
        for j in range(3):
            for m in range(Nz):
                k += 1; A[k] = {'type': 1, 'x': (i + 0.5) * d, 'y': (j + 0.5) * d, 'z': r + m * d, 'radius': r}
    ids = {(round(a['x'] / d - .5), round(a['y'] / d - .5), round((a['z'] - r) / d)): kk for kk, a in A.items()}
    C = []
    for (i, j, m), kk in ids.items():
        for di, dj, dm in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            nb = ids.get(((i + di) % 3, (j + dj) % 3, m + dm))
            if nb and (m + dm) < Nz:
                C.append({'id1': kk, 'id2': nb, 'contact_area': 1e-12, 'delta': 1e-12})
    plate = Nz * d; box = 3 * d
    with contextlib.redirect_stdout(io.StringIO()):
        net = nc.build_network(A, C, [1], 1000.0, plate, box, box, 2.0, mode='ionic', type_map={1: 'SE'}, contact_mode='hertzian')
        _, s_mod = nc.solve_network(net, mode='bulk_only')
    perc = perc_component(net)
    phi = 9 * Nz * 4 / 3 * math.pi * r ** 3 / (box * box * plate)
    Rcyl = [e['R_bulk'] for e in net['edges']]
    RW = [wiener_half(e['r1'], edge_geom(e)[2]) + wiener_half(e['r2'], edge_geom(e)[3]) for e in net['edges']]
    _, sa0, _ = solve_adaptive(net, Rcyl, perc); _, sd0, _ = solve_dirichlet(net, Rcyl, perc)
    _, sa2, _ = solve_adaptive(net, RW, perc); _, sd2, _ = solve_dirichlet(net, RW, perc)
    ideal = (Nz - 1) / Nz
    print(f'Nz={Nz:3d} phi={phi:.6f} | CF0 module q={s_mod:.6f} T={phi/s_mod:.6f} (Codex 0.633/0.650/0.658) · '
          f'dirichlet T={phi/sd0:.6f} [ideal 2/3*(Nz-1)/Nz={2/3*ideal:.6f}] | CF2 adaptive T={phi/sa2:.6f} dirichlet T={phi/sd2:.6f} [ideal {ideal:.6f}]')

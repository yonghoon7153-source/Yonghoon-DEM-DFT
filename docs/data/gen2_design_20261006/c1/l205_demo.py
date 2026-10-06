#!/usr/bin/env python3
"""designC1 — L2-05: electrode conductance depends on unrelated edges.  Reproduce with the HEAD module
(snapshot dfe26fcd4 in lib/), show the proposed exact-Dirichlet solve is invariant, and measure both
on the committed real bed (real_14, ionic Hertz FULL)."""
import contextlib
import io
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from beds import load, nc_module           # noqa: E402
from netsolve import solve_dirichlet, perc_component   # noqa: E402

nc = nc_module()


def E(i, j, R):
    return {'id1': i, 'id2': j, 'R_total': R, 'R_bulk': R, 'R_constriction': 0.0, 'type1': 1, 'type2': 1,
            'delta': 0.0, 'delta_over_R': 0.0, 'regime': 'x', 'r1': 1.0, 'r2': 1.0, 'd_ij': 1.0,
            'A_hertzian': 0.0, 'A_physics': 0.0, 'A_contact': 0.0}


def net_of(edges, bottom, top):
    nodes = sorted({e['id1'] for e in edges} | {e['id2'] for e in edges})
    return {'nodes': nodes, 'edges': edges, 'bottom': set(bottom), 'top': set(top), 'scale': 1.0,
            'plate_z': 1.0, 'box_x': 1.0, 'box_y': 1.0}


def mod(net):
    with contextlib.redirect_stdout(io.StringIO()):
        return nc.solve_network(net, mode='full')[0]


def dirich(net):
    R = [e['R_total'] for e in net['edges']]
    return solve_dirichlet(net, R)[0]


def main():
    print('== Codex counterexample (single path R=1, bottom node 1, top node 2) ==')
    base = net_of([E(1, 2, 1.0)], {1}, {2})
    dead = net_of([E(1, 2, 1.0), E(1, 3, 1e-3)], {1}, {2})          # zero-current dead end at the bottom node
    dead_mid = net_of([E(1, 4, 0.5), E(4, 2, 0.5), E(4, 5, 1e-3)], {1}, {2})   # dead end at an interior node
    base_mid = net_of([E(1, 4, 0.5), E(4, 2, 0.5)], {1}, {2})
    for name, a, b in (('dead end at bottom node', base, dead), ('dead end at interior node', base_mid, dead_mid)):
        g0, g1 = mod(a), mod(b)
        d0, d1 = dirich(a), dirich(b)
        print(f'  {name:28s} HEAD G {g0:.14f} -> {g1:.14f} ({(g1 / g0 - 1) * 100:+.6f} %) | '
              f'Dirichlet G {d0:.14f} -> {d1:.14f} ({(d1 / d0 - 1) * 100:+.2e} %)')
    # unit scaling
    sc = net_of([E(1, 4, 3.5), E(4, 2, 3.5), E(4, 5, 7e-3)], {1}, {2})
    print(f'  unit scaling (all R x7): HEAD {mod(sc) * 7 / mod(dead_mid):.15f} · Dirichlet {dirich(sc) * 7 / dirich(dead_mid):.15f}')

    print('== real_14 ionic Hertz FULL (HEAD edges) ==')
    A, C, b = load('real14')
    se = [k for k, v in b['type_map'].items() if v == 'SE']
    with contextlib.redirect_stdout(io.StringIO()):
        net = nc.build_network(A, C, se, 1000.0, b['plate_z'], b['box'], b['box'], 2.0,
                               mode='ionic', type_map=b['type_map'], contact_mode='hertzian')
    perc = perc_component(net)
    R = [e['R_total'] for e in net['edges']]
    g_head = mod(net)
    G_d = solve_dirichlet(net, R, perc)[0]
    # add ONE zero-current dead-end particle hanging off an interior percolating node with R = 1e-6 x min R
    interior = sorted(perc - net['bottom'] - net['top'])[len(perc) // 2]
    Rmin = min(r for r in R if r > 0)
    net2 = dict(net)
    net2['edges'] = net['edges'] + [dict(E(interior, 10 ** 9, Rmin * 1e-6))]
    net2['nodes'] = list(net['nodes']) + [10 ** 9]
    g_head2 = mod(net2)
    R2 = R + [Rmin * 1e-6]
    G_d2 = solve_dirichlet(net2, R2)[0]
    geo = net['plate_z'] * net['scale'] / (net['box_x'] * net['box_y'] * net['scale'] ** 2)
    print(f'  HEAD sigma {g_head * geo:.10f} -> with dead end {g_head2 * geo:.10f} ({(g_head2 / g_head - 1) * 100:+.5f} %)')
    print(f'  Dirichlet sigma {G_d * geo:.10f} -> with dead end {G_d2 * geo:.10f} ({(G_d2 / G_d - 1) * 100:+.2e} %)')
    print(f'  Dirichlet / HEAD (no dead end) = {G_d / g_head:.8f}')
    return 0


if __name__ == '__main__':
    sys.exit(main())

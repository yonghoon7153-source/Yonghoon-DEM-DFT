"""Independent recompute of the Codex KG50 report-plan review arithmetic (10-30).

Our own code (not Codex's script): solves the toy networks by nodal analysis instead of typing
the answers, recomputes the geometry from formulas, and adds two checks that matter for the plan:
  (a) a random 3D resistor network: the signed current across every z-plane equals the terminal
      current (so a z-profile of *net* ionic current is flat by construction), while sum|I| per
      plane and the dissipated power per z-bin vary;
  (b) the repo's own "current share" ladder (scripts/network_current.py: section-mean signed flux
      of the top-|I| edges / I_total over 32 z-planes) on a 10-edge series chain: 8 of 10 edges
      reach a share of ~0.8 while the selected edges do not connect the two terminals.
Stdlib + numpy only.  Synthetic numbers — not campaign data, not a DEM run.
"""
import json, math, sys
import numpy as np


def solve(n_nodes, edges, g, v_fixed):
    """Nodal analysis: edges (i, j), conductances g, Dirichlet dict node -> V."""
    L = np.zeros((n_nodes, n_nodes))
    for (i, j), gij in zip(edges, g):
        L[i, i] += gij; L[j, j] += gij; L[i, j] -= gij; L[j, i] -= gij
    free = [k for k in range(n_nodes) if k not in v_fixed]
    V = np.zeros(n_nodes)
    for k, v in v_fixed.items():
        V[k] = v
    if free:
        A = L[np.ix_(free, free)]
        b = -L[np.ix_(free, list(v_fixed))] @ np.array([v_fixed[k] for k in v_fixed])
        V[free] = np.linalg.solve(A, b)
    I = np.array([gij * (V[i] - V[j]) for (i, j), gij in zip(edges, g)])
    return V, I


def gini(x):
    x = np.asarray(x, float)
    return float(np.abs(x[:, None] - x[None, :]).sum() / (2 * len(x) * x.sum()))


def series(R):
    n = len(R) + 1
    edges = [(k, k + 1) for k in range(len(R))]
    V, I = solve(n, edges, [1.0 / r for r in R], {0: 1.0, n - 1: 0.0})
    thr = [0.5 * (abs(I[k - 1]) + abs(I[k])) for k in range(1, n - 1)]  # node throughput
    P = I ** 2 * np.array(R)
    return {'I_terminal': float(I[0]), 'cut_currents': [float(x) for x in I],
            'internal_node_gini': gini(thr), 'power_frac_per_edge': [float(p / P.sum()) for p in P],
            'power_identity': float(P.sum() / (1.0 * I[0]))}


def random_network(seed=7, n=400, k=6):
    rng = np.random.default_rng(seed)
    P = rng.random((n, 3)) * np.array([1.0, 1.0, 2.0])
    d = np.linalg.norm(P[:, None] - P[None, :], axis=2)
    np.fill_diagonal(d, np.inf)
    edges = sorted({tuple(sorted((i, int(j)))) for i in range(n) for j in np.argsort(d[i])[:k]})
    g = rng.lognormal(0.0, 1.0, len(edges))
    bot = set(np.flatnonzero(P[:, 2] < 0.15).tolist()); top = set(np.flatnonzero(P[:, 2] > 1.85).tolist())
    vf = {**{b: 1.0 for b in bot}, **{t: 0.0 for t in top}}
    V, I = solve(n, edges, g, vf)
    e = np.array(edges); z1, z2 = P[e[:, 0], 2], P[e[:, 1], 2]
    I_tot = float(sum((I[m] if i in bot else -I[m]) for m, (i, j) in enumerate(edges) if (i in bot) != (j in bot)))
    planes = np.linspace(0.2, 1.8, 9)
    net, absum, dis = [], [], []
    for zp in planes:
        up = (z1 <= zp) & (z2 > zp); dn = (z2 <= zp) & (z1 > zp)
        net.append(float(I[up].sum() - I[dn].sum()))
        absum.append(float(np.abs(I[up | dn]).sum()))
    Pw = I ** 2 / g
    zm = 0.5 * (z1 + z2)
    for lo, hi in zip(np.linspace(0, 2, 5)[:-1], np.linspace(0, 2, 5)[1:]):
        dis.append(float(Pw[(zm >= lo) & (zm < hi)].sum() / Pw.sum()))
    return {'n_nodes': n, 'n_edges': len(edges), 'I_terminal': I_tot,
            'net_cut_current_over_I': [x / I_tot for x in net],
            'net_cut_max_rel_dev': float(max(abs(x / I_tot - 1) for x in net)),
            'sum_abs_I_over_I_per_plane': [x / I_tot for x in absum],
            'power_frac_per_z_quarter': dis,
            'power_identity': float(Pw.sum() / I_tot)}


def repo_share_ladder_on_chain(n_edges=10, n_sel=8, planes=32):
    """scripts/network_current.py ladder (section-mean signed flux of top-|I| edges / I_tot)."""
    z = np.linspace(0.0, 1.0, n_edges + 1)
    I = np.full(n_edges, 1.0 / n_edges)     # 1 V over 10 x 1 ohm
    I_tot = I[0]
    zl, zh = z[0], z[-1]
    pl = zl + (np.arange(planes) + 0.5) * (zh - zl) / planes
    z1, z2 = z[:-1], z[1:]
    up = (z1[:, None] <= pl) & (z2[:, None] > pl)
    flux = np.where(up, I[:, None], 0.0)
    order = np.arange(n_edges)              # all |I| equal; ties -> id order (as lexsort)
    ladder = np.cumsum(flux.mean(axis=1)[order]) / I_tot
    sel = set(order[:n_sel].tolist())
    connected = all(k in sel for k in range(n_edges))
    return {'share_after_8_edges': float(ladder[n_sel - 1]), 'sum_abs_I_fraction': n_sel / n_edges,
            'selected_edges_connect_terminals': connected,
            'identity_cut_flux_over_I': float(flux.sum(axis=0).max() / I_tot)}


def main():
    phi_s = (0.15 / 1.64) / (0.85 / 4.85 + 0.15 / 1.64)
    f_d3 = 0.06191 / 3.0
    out = {
        'scope': 'independent recompute of reviewer arithmetic + two plan-specific checks; synthetic',
        'throat_um': 6 * (2 / math.sqrt(3) - 1),
        'size_ratio_DAM_over_DSE': {str(d): 6 / d for d in (3, 2, 1, 0.7)},
        'phi_SE_solid': phi_s,
        'phi_SE_bulk_at_eps_sphere_18.95': phi_s * (1 - 0.1895),
        'phi_from_D3_rounded_tau2_times_f': 13.47 * f_d3,
        'tau2_if_solid_phi_used': phi_s / f_d3,
        'tau2_bias_pct': (phi_s / f_d3 / 13.47 - 1) * 100,
        'series_uniform': series([1, 1, 1]),
        'series_bottleneck': series([1, 98, 1]),
        'node_gini_before_after_subdivision': [gini([0.8, 0.2]), gini([0.8] + [0.2] * 9)],
        'sigma_break_even': {'f1_over_f3': 5.1 / 2.3, 'f07_over_f3': 5.1 / 2.25, 'f07_over_f1': 2.3 / 2.25},
        'pellet_double_count_example': 10 * 0.5 * 0.5,
        'unknown_d2': {k: [round(f * s, 6) for f, s in zip((0.1, 0.09, 0.08), sig)]
                       for k, sig in (('low', (2.3, 2.4, 5.1)), ('high', (2.3, 4.9, 5.1)))},
        'cap_over_disc_at_a_over_R_0.8': (2 * (1 - math.sqrt(1 - 0.64))) / 0.64,
        'three_coincident_spheres': {'union': 4 * math.pi / 3,
                                     'sum_minus_pair_lenses': 3 * 4 * math.pi / 3 - 3 * 4 * math.pi / 3,
                                     'inclusion_exclusion_with_triple': 3 * 4 * math.pi / 3 - 3 * 4 * math.pi / 3 + 4 * math.pi / 3},
        'hydrostatic_von_mises': [float(math.sqrt(0.5 * ((p - p) ** 2 * 3))) for p in (10.0, 300.0)],
        'fixed_interface_conductance_ratio': (1 / (1 / 2 + 1)) / (1 / (1 / 1 + 1)),
        'random_3d_network': random_network(),
        'repo_share_ladder_chain': repo_share_ladder_on_chain(),
    }
    ok = {
        'throat_between_0.7_and_1': 0.7 < out['throat_um'] < 1.0,
        'phi_bulk_matches_D3_to_1e-4': abs(out['phi_SE_bulk_at_eps_sphere_18.95'] - out['phi_from_D3_rounded_tau2_times_f']) < 1e-4,
        'bottleneck_I_0.01': math.isclose(out['series_bottleneck']['I_terminal'], 0.01, rel_tol=1e-12),
        'bottleneck_gini_0_and_uniform_gini_0': out['series_bottleneck']['internal_node_gini'] < 1e-12 and out['series_uniform']['internal_node_gini'] < 1e-12,
        'bottleneck_middle_power_0.98': math.isclose(out['series_bottleneck']['power_frac_per_edge'][1], 0.98, rel_tol=1e-12),
        'gini_0.3_to_0.2077': math.isclose(out['node_gini_before_after_subdivision'][0], 0.3) and abs(out['node_gini_before_after_subdivision'][1] - 0.2076923) < 1e-7,
        'd2_argmax_flips': int(np.argmax(out['unknown_d2']['low'])) == 2 and int(np.argmax(out['unknown_d2']['high'])) == 1,
        'cap_over_disc_1.25': math.isclose(out['cap_over_disc_at_a_over_R_0.8'], 1.25),
        'net_cut_current_conserved_1e-9': out['random_3d_network']['net_cut_max_rel_dev'] < 1e-9,
        'abs_sum_per_plane_varies': max(out['random_3d_network']['sum_abs_I_over_I_per_plane']) - min(out['random_3d_network']['sum_abs_I_over_I_per_plane']) > 0.1,
        'power_identity_random_net': abs(out['random_3d_network']['power_identity'] - 1) < 1e-9,
        'repo_ladder_0.8_but_disconnected': abs(out['repo_share_ladder_chain']['share_after_8_edges'] - 0.8) < 0.05 and not out['repo_share_ladder_chain']['selected_edges_connect_terminals'],
        'fixed_interface_4_over_3': math.isclose(out['fixed_interface_conductance_ratio'], 4 / 3),
    }
    out['checks'] = ok
    json.dump(out, open(sys.argv[1], 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print(json.dumps(ok, indent=1)); print('all', all(ok.values()))
    return 0 if all(ok.values()) else 1


if __name__ == '__main__':
    sys.exit(main())

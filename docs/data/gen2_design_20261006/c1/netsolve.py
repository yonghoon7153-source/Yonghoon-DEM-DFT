#!/usr/bin/env python3
"""designC1 — two solvers for a network_conductivity `net` dict with per-edge resistances supplied
by the caller (so edge-model variants can be compared on the SAME graph and SAME boundary sets).

  solve_adaptive(net, R)  — faithful re-implementation of HEAD solve_network's boundary handling:
                            virtual source/sink, g_boundary = max(100*Sum g/n_el, 10*g_max, 1e-6)
                            (network_conductivity.py:707-732) — direct sparse solve.
  solve_dirichlet(net, R) — proposed L2-05 fix: band nodes are exact Dirichlet nodes (bottom V=1,
                            top V=0), no virtual conductance at all.  G = current leaving bottom.

Both return (G, sigma_ratio, extra) with sigma_ratio = G * (plate_z*scale) / (box_x*box_y*scale^2)
exactly as solve_network does.  R: array aligned with net['edges'] (resistance per edge, rho=1).
"""
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve, cg


def perc_component(net):
    import networkx as nx
    G = nx.Graph()
    for e in net['edges']:
        G.add_edge(e['id1'], e['id2'])
    perc = set()
    for comp in nx.connected_components(G):
        if comp & net['bottom'] and comp & net['top']:
            perc |= comp
    return perc


def _lap(ids, edges, R, idx_of, n):
    i = np.array([idx_of[e['id1']] for e in edges])
    j = np.array([idx_of[e['id2']] for e in edges])
    g = 1.0 / np.asarray(R, float)
    L = sparse.coo_matrix((np.concatenate([g, g, -g, -g]),
                           (np.concatenate([i, j, i, j]), np.concatenate([i, j, j, i]))),
                          shape=(n, n)).tocsr()
    return L, g


def _geom(net):
    return net['plate_z'] * net['scale'] / (net['box_x'] * net['box_y'] * net['scale'] ** 2)


def _select(net, R, perc):
    keep = [k for k, e in enumerate(net['edges']) if e['id1'] in perc and e['id2'] in perc]
    return [net['edges'][k] for k in keep], np.asarray(R, float)[keep]


def solve_adaptive(net, R, perc=None, g_scale=None):
    perc = perc if perc is not None else perc_component(net)
    if not perc:
        return None, None, {}
    E, Rk = _select(net, R, perc)
    pos = Rk > 0
    E = [e for e, p in zip(E, pos) if p]; Rk = Rk[pos]
    ids = list(perc)
    idx = {nid: k for k, nid in enumerate(ids)}
    N = len(ids)
    L, g = _lap(ids, E, Rk, idx, N + 2)
    bot = [idx[b] for b in net['bottom'] & perc]
    top = [idx[t] for t in net['top'] & perc]
    n_el = max(len(bot) + len(top), 1)
    gb = max(100.0 * g.sum() / n_el, 10.0 * g.max(), 1e-6)
    if g_scale is not None:
        gb = g_scale
    src, snk = N, N + 1
    rows, cols, vals = [], [], []
    for b in bot:
        rows += [b, src, b, src]; cols += [b, src, src, b]; vals += [gb, gb, -gb, -gb]
    for t in top:
        rows += [t, snk, t, snk]; cols += [t, snk, snk, t]; vals += [gb, gb, -gb, -gb]
    L = (L + sparse.coo_matrix((vals, (rows, cols)), shape=(N + 2, N + 2))).tocsr()
    # ground sink (eliminate it)
    keep = np.arange(N + 1)
    Lr = L[keep][:, keep].tocsc()
    b = np.zeros(N + 1); b[src] = 1.0
    V = spsolve(Lr, b)
    G = 1.0 / V[src]
    return G, G * _geom(net), dict(g_boundary=gb, sum_g=float(g.sum()), g_max=float(g.max()),
                                     n_bot=len(bot), n_top=len(top), V=V, ids=ids)


def solve_dirichlet(net, R, perc=None, return_V=False):
    perc = perc if perc is not None else perc_component(net)
    if not perc:
        return None, None, {}
    B = net['bottom'] & perc
    T = net['top'] & perc
    if B & T:
        return None, None, {'why': 'bottom∩top'}
    E, Rk = _select(net, R, perc)
    pos = Rk > 0
    E = [e for e, p in zip(E, pos) if p]; Rk = Rk[pos]
    ids = list(perc)
    idx = {nid: k for k, nid in enumerate(ids)}
    N = len(ids)
    L, g = _lap(ids, E, Rk, idx, N)
    Vfix = np.full(N, np.nan)
    for b in B:
        Vfix[idx[b]] = 1.0
    for t in T:
        Vfix[idx[t]] = 0.0
    fixed = ~np.isnan(Vfix)
    free = np.flatnonzero(~fixed)
    fx = np.flatnonzero(fixed)
    L_ff = L[free][:, free].tocsc()
    rhs = -(L[free][:, fx] @ Vfix[fx])
    V = Vfix.copy()
    if len(free):
        V[free] = spsolve(L_ff, rhs)
    # current out of the bottom set = (L V)_b summed over b in B
    Iv = L @ V
    I_bot = float(sum(Iv[idx[b]] for b in B))
    I_top = float(sum(Iv[idx[t]] for t in T))
    G = I_bot  # dV = 1
    out = dict(I_bot=I_bot, I_top=I_top, sum_g=float(g.sum()), n_bot=len(B), n_top=len(T))
    if return_V:
        out['V'] = V; out['ids'] = ids; out['idx'] = idx; out['E'] = E; out['Rk'] = Rk
    return G, G * _geom(net), out

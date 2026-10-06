"""Same Laplacian as HEAD solve_network (percolating component · g_boundary rule · σ = G·T/A),
solved with a reduced (grounded) SPD system + conjugate gradient with an algebraic preconditioner
fallback to direct.  Used only to speed up the scratch comparison on the big case15 bed."""
import numpy as np
import networkx as nx
from scipy import sparse
from scipy.sparse.linalg import spsolve, cg


def fast_sigma(net, Rkey='R_total'):
    edges = net['edges']; bottom = net['bottom']; top = net['top']
    G = nx.Graph()
    for e in edges:
        G.add_edge(e['id1'], e['id2'])
    perc = set()
    for comp in nx.connected_components(G):
        if comp & bottom and comp & top:
            perc |= comp
    if not perc:
        return None
    ids = list(perc); idx = {n: i for i, n in enumerate(ids)}; N = len(ids)
    r, c, v = [], [], []
    gsum = 0.0; gmax = 0.0
    for e in edges:
        if e['id1'] in perc and e['id2'] in perc:
            R = e[Rkey]
            if R > 0:
                g = 1.0 / R
                i, j = idx[e['id1']], idx[e['id2']]
                r += [i, j, i, j]; c += [i, j, j, i]; v += [g, g, -g, -g]
                gsum += g; gmax = max(gmax, g)
    pb = [idx[b] for b in bottom & perc]; pt = [idx[t] for t in top & perc]
    gb = max(100.0 * gsum / max(len(pb) + len(pt), 1), 10.0 * gmax, 1e-6)
    src, snk = N, N + 1
    for b in pb:
        r += [b, src, b, src]; c += [b, src, src, b]; v += [gb, gb, -gb, -gb]
    for t in pt:
        r += [t, snk, t, snk]; c += [t, snk, snk, t]; v += [gb, gb, -gb, -gb]
    L = sparse.csr_matrix((v, (r, c)), shape=(N + 2, N + 2))
    keep = np.arange(N + 1)                 # ground the sink (V_sink = 0) → SPD reduced system
    A = L[keep][:, keep].tocsr()
    b = np.zeros(N + 1); b[src] = 1.0
    x = spsolve(A.tocsc(), b)          # direct (SuperLU) — exact; CG crawls when the top band is tiny
    Vs = x[src]
    Geff = 1.0 / Vs
    T = net['plate_z'] * net['scale']; Ab = net['box_x'] * net['box_y'] * net['scale'] ** 2
    return Geff * T / Ab

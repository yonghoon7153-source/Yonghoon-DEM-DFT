#!/usr/bin/env python3
"""designC1 — 3D FV bracket for BCC/FCC (diagonal necks resolve slowly on a cubic grid).
mode 'all'    : every voxel with an open face is a node, face conductance = sigma*dx*open_fraction  (upper side)
mode 'inside' : only voxels whose CENTRE is inside the union are nodes, same face conductances      (lower side)
usage: python3 fv_lattice3d_bracket.py KIND S N1,N2,.. [q]
"""
import sys, time, math
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import cg, LinearOperator
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from fv_lattice3d import phi_sum, net_f, models
from fv_lattice3d_cut import face_fractions, centres, inside_any


def solve(fr, c, dx, inside=None, tol=1e-9, maxiter=60000):
    n = fr[0].shape[0]
    g = [dx * f for f in fr]
    if inside is None:
        active = np.zeros((n, n, n), bool)
        for ax in range(3):
            o = g[ax] > 0
            active |= o; active |= np.roll(o, 1, axis=ax)
    else:
        active = inside
    idx = -np.ones((n, n, n), np.int64)
    act = np.flatnonzero(active.ravel()); idx.ravel()[act] = np.arange(act.size); N = act.size
    rows, cols, vals = [], [], []; diag = np.zeros(N); b = np.zeros(N)
    for ax in range(3):
        nb = np.roll(idx, -1, axis=ax)
        o = (g[ax] > 0) & (idx >= 0) & (nb >= 0)
        i = idx[o]; j = nb[o]; gg = g[ax][o]
        rows += [i, j]; cols += [j, i]; vals += [-gg, -gg]
        np.add.at(diag, i, gg); np.add.at(diag, j, gg)
        if ax == 2:
            sl = np.zeros((n, n, n), bool); sl[:, :, -1] = True
            cr = o & sl
            iA, jB, gc = idx[cr], nb[cr], g[2][cr]
            np.add.at(b, iA, -gc); np.add.at(b, jB, +gc)
    A = sparse.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(N, N)).tocsr() + sparse.diags(diag + 1e-12 * dx)
    Minv = 1.0 / A.diagonal(); M = LinearOperator((N, N), matvec=lambda v: Minv * v)
    t = time.time()
    try:
        x, info = cg(A, b, rtol=tol, maxiter=maxiter, M=M)
    except TypeError:
        x, info = cg(A, b, tol=tol, maxiter=maxiter, M=M)
    I = float(np.sum(gc * (x[iA] - x[jB] + 1.0)))
    return I / c, info, time.time() - t, N


kind, s = sys.argv[1], float(sys.argv[2]); ns = [int(v) for v in sys.argv[3].split(',')]
q = int(sys.argv[4]) if len(sys.argv) > 4 else 4
ph = phi_sum(kind, s)
for n in ns:
    t0 = time.time()
    fr, c, dx, vol = face_fractions(kind, s, n, q)
    P, _ = centres(kind, s)
    vx = (np.arange(n) + 0.5) * dx
    X, Y, Z = np.meshgrid(vx, vx, vx, indexing='ij')
    ins = inside_any(X, Y, Z, P); del X, Y, Z
    fa, ia, ta, Na = solve(fr, c, dx)
    fi, ii, ti, Ni = solve(fr, c, dx, inside=ins)
    print(f'{kind} s={s:.2f} n={n} r/dx={1/dx:.1f}  f_all={fa:.6f} (cg {ia}, {ta:.0f}s)  f_inside={fi:.6f} (cg {ii}, {ti:.0f}s)  '
          f'mid={(fa+fi)/2:.6f}  T_mid={ph/((fa+fi)/2):.4f}  total {time.time()-t0:.0f}s', flush=True)
for name, R in models(s).items():
    fn = net_f(kind, s, R)
    print(f'   {name:16s} f={fn:.6f}  T(phi_sum)={ph/fn:.4f}')

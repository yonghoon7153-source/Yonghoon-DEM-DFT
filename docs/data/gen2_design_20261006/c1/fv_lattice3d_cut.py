#!/usr/bin/env python3
"""designC1 — 3D cut-face FV (continuum reference) for periodic lattices of equal overlapping spheres.

Same problem as fv_lattice3d.py, but each voxel face conductance = sigma * dx * (open fraction of the
face), the open fraction measured by q x q supersampling of the face against the union of spheres
(cut-face / porous-face FV — much better neck resolution than staircase voxels).

usage: python3 fv_lattice3d_cut.py KINDS S_LIST N_LIST [q]
"""
import math
import sys
import time
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import cg, LinearOperator

sys.path.insert(0, __file__.rsplit('/', 1)[0])
from fv_lattice3d import lattice, phi_sum, net_f, models   # noqa: E402


def centres(kind, s):
    h, d, c, basis = lattice(kind, s)
    P = []
    for (bx, by, bz) in basis:
        for ix in (-1, 0, 1):
            for iy in (-1, 0, 1):
                for iz in (-1, 0, 1):
                    P.append(((bx + ix) * c, (by + iy) * c, (bz + iz) * c))
    return np.array(P), c


def inside_any(X, Y, Z, P):
    m = np.zeros(X.shape, bool)
    for (cx, cy, cz) in P:
        m |= (X - cx) ** 2 + (Y - cy) ** 2 + (Z - cz) ** 2 <= 1.0
    return m


def face_fractions(kind, s, n, q):
    """frac[ax][i,j,k] = open fraction of the face between voxel (i,j,k) and its +1 neighbour along ax
    (periodic); the face lies at coordinate (idx+1)*dx along ax."""
    P, c = centres(kind, s)
    dx = c / n
    base = np.arange(n) * dx
    sub = (np.arange(q) + 0.5) / q * dx
    fr = []
    for ax in range(3):
        acc = np.zeros((n, n, n))
        for u in sub:
            for v in sub:
                coords = []
                for k in range(3):
                    if k == ax:
                        coords.append(base + dx)                    # face plane
                    else:
                        coords.append(None)
                # the two in-face axes get offsets u, v
                others = [k for k in range(3) if k != ax]
                cc = [None, None, None]
                cc[ax] = base + dx
                cc[others[0]] = base + u
                cc[others[1]] = base + v
                X, Y, Z = np.meshgrid(cc[0], cc[1], cc[2], indexing='ij')
                acc += inside_any(X, Y, Z, P)
        fr.append(acc / (q * q))
    vx = (np.arange(n) + 0.5) * dx
    X, Y, Z = np.meshgrid(vx, vx, vx, indexing='ij')
    vol = inside_any(X, Y, Z, P).mean()
    return fr, c, dx, vol


def solve(fr, c, dx, tol=1e-10, maxiter=40000):
    n = fr[0].shape[0]
    g = [dx * f for f in fr]                      # sigma * (dx^2 * frac) / dx
    active = np.zeros((n, n, n), bool)
    for ax in range(3):
        o = g[ax] > 0
        active |= o
        active |= np.roll(o, 1, axis=ax)
    idx = -np.ones((n, n, n), np.int64)
    act = np.flatnonzero(active.ravel())
    idx.ravel()[act] = np.arange(act.size)
    N = act.size
    rows, cols, vals = [], [], []
    diag = np.zeros(N)
    b = np.zeros(N)
    for ax in range(3):
        nb = np.roll(idx, -1, axis=ax)
        o = g[ax] > 0
        i = idx[o]; j = nb[o]; gg = g[ax][o]
        rows += [i, j]; cols += [j, i]; vals += [-gg, -gg]
        np.add.at(diag, i, gg); np.add.at(diag, j, gg)
        if ax == 2:
            sl = np.zeros((n, n, n), bool); sl[:, :, -1] = True
            cr = o & sl
            iA, jB, gc = idx[cr], nb[cr], g[2][cr]
            np.add.at(b, iA, -gc); np.add.at(b, jB, +gc)
    A = sparse.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                          shape=(N, N)).tocsr() + sparse.diags(diag + 1e-12 * dx)
    Minv = 1.0 / A.diagonal()
    M = LinearOperator((N, N), matvec=lambda v: Minv * v)
    t = time.time()
    try:
        x, info = cg(A, b, rtol=tol, maxiter=maxiter, M=M)
    except TypeError:
        x, info = cg(A, b, tol=tol, maxiter=maxiter, M=M)
    I = float(np.sum(gc * (x[iA] - x[jB] + 1.0)))
    return I / c, info, time.time() - t, N


def main():
    kinds = sys.argv[1].split(',')
    ss = [float(x) for x in sys.argv[2].split(',')]
    ns = [int(x) for x in sys.argv[3].split(',')]
    q = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    for kind in kinds:
        for s in ss:
            fs, hs = [], []
            for n in ns:
                t0 = time.time()
                fr, c, dx, vol = face_fractions(kind, s, n, q)
                f, info, dt, N = solve(fr, c, dx)
                fs.append(f); hs.append(dx)
                print(f'{kind} s={s:.2f} n={n:4d} r/dx={1/dx:6.1f} N={N:8d} f={f:.6f} cg={info} '
                      f'solve {dt:5.1f}s total {time.time()-t0:5.1f}s phi_union~{vol:.5f}', flush=True)
            if len(ns) >= 2:
                h1, h2 = hs[-2], hs[-1]
                f0 = (h1 * fs[-1] - h2 * fs[-2]) / (h1 - h2)
            else:
                f0 = fs[-1]
            ph = phi_sum(kind, s)
            print(f'  -> {kind} s={s:.2f}: f_FV(finest)={fs[-1]:.6f} f_FV(lin-extrap)={f0:.6f} '
                  f'phi_sum={ph:.5f} T_FV={ph / fs[-1]:.4f}..{ph / f0:.4f}')
            for name, R in models(s).items():
                fn = net_f(kind, s, R)
                print(f'     {name:16s} f={fn:.6f}  f/f_FV(finest)={fn / fs[-1]:7.4f}  '
                      f'f/f_FV(extrap)={fn / f0:7.4f}  T(phi_sum)={ph / fn:7.4f}', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""designC1 — octant-reduced 3D cut-face FV for SC/BCC/FCC (field along [001]).

All three cubic lattices have mirror planes x=0, x=c/2, y=0, y=c/2 (=> Neumann) and z=0, z=c/2
(=> the antisymmetric potential is CONSTANT on them: phi(z=0)=0, phi(z=c/2)=-1/2 for a drop of 1 per
cell).  Domain = [0,c/2]^3 (1/8 cell) -> ~2x finer resolution for the same cost.
sigma_eff/sigma = 4 * I_oct / c   (octant carries 1/4 of the cell's xy-area current).
Face conductance = sigma*dx*(open fraction, q x q supersampling); nodes: 'all' (any open face) or
'inside' (centre inside the union) — the two bracket the diagonal-neck discretisation error.

usage: python3 fv_oct.py KIND S N1,N2,... [q]
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
                    p = ((bx + ix) * c, (by + iy) * c, (bz + iz) * c)
                    # keep spheres that can touch the octant [0,c/2]^3
                    if all(-1.0 <= p[k] <= c / 2 + 1.0 for k in range(3)):
                        P.append(p)
    return np.array(P), c


def inside_any(X, Y, Z, P):
    m = np.zeros(X.shape, bool)
    for (cx, cy, cz) in P:
        m |= (X - cx) ** 2 + (Y - cy) ** 2 + (Z - cz) ** 2 <= 1.0
    return m


def fractions(kind, s, n, q):
    P, c = centres(kind, s)
    L = c / 2
    dx = L / n
    vc = (np.arange(n) + 0.5) * dx
    sub = (np.arange(q) + 0.5) / q * dx
    edges = np.arange(n + 1) * dx                       # face planes incl. both ends
    fr = []
    for ax in range(3):
        shape = [n, n, n]
        shape[ax] = n + 1
        acc = np.zeros(shape)
        others = [k for k in range(3) if k != ax]
        for u in sub:
            for v in sub:
                cc = [None, None, None]
                cc[ax] = edges
                cc[others[0]] = np.arange(n) * dx + u
                cc[others[1]] = np.arange(n) * dx + v
                X, Y, Z = np.meshgrid(cc[0], cc[1], cc[2], indexing='ij')
                acc += inside_any(X, Y, Z, P)
        fr.append(acc / (q * q))
    X, Y, Z = np.meshgrid(vc, vc, vc, indexing='ij')
    ins = inside_any(X, Y, Z, P)
    return fr, ins, c, dx


def solve(fr, ins, c, dx, mode, tol=1e-10, maxiter=80000):
    n = ins.shape[0]
    gx = dx * fr[0][1:-1, :, :]          # interior x faces between i and i+1  (n-1, n, n)
    gy = dx * fr[1][:, 1:-1, :]
    gz = dx * fr[2][:, :, 1:-1]
    gb0 = 2 * dx * fr[2][:, :, 0]         # z=0 plane, half-cell distance: sigma*dx^2*f/(dx/2)
    gb1 = 2 * dx * fr[2][:, :, -1]        # z=c/2 plane
    if mode == 'inside':
        active = ins.copy()
    else:
        active = np.zeros((n, n, n), bool)
        for g, ax in ((gx, 0), (gy, 1), (gz, 2)):
            o = g > 0
            sl1 = [slice(None)] * 3; sl1[ax] = slice(0, n - 1)
            sl2 = [slice(None)] * 3; sl2[ax] = slice(1, n)
            active[tuple(sl1)] |= o
            active[tuple(sl2)] |= o
        active[:, :, 0] |= gb0 > 0
        active[:, :, -1] |= gb1 > 0
    idx = -np.ones((n, n, n), np.int64)
    act = np.flatnonzero(active.ravel())
    idx.ravel()[act] = np.arange(act.size)
    N = act.size
    rows, cols, vals = [], [], []
    diag = np.zeros(N)
    for g, ax in ((gx, 0), (gy, 1), (gz, 2)):
        sl1 = [slice(None)] * 3; sl1[ax] = slice(0, n - 1)
        sl2 = [slice(None)] * 3; sl2[ax] = slice(1, n)
        i = idx[tuple(sl1)]; j = idx[tuple(sl2)]
        o = (g > 0) & (i >= 0) & (j >= 0)
        ii, jj, gg = i[o], j[o], g[o]
        rows += [ii, jj]; cols += [jj, ii]; vals += [-gg, -gg]
        np.add.at(diag, ii, gg); np.add.at(diag, jj, gg)
    b = np.zeros(N)
    i0 = idx[:, :, 0]; o0 = (gb0 > 0) & (i0 >= 0)
    np.add.at(diag, i0[o0], gb0[o0])                      # phi(z=0) = 0
    i1 = idx[:, :, -1]; o1 = (gb1 > 0) & (i1 >= 0)
    np.add.at(diag, i1[o1], gb1[o1]); np.add.at(b, i1[o1], gb1[o1] * (-0.5))
    A = sparse.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                          shape=(N, N)).tocsr() + sparse.diags(diag)
    Minv = 1.0 / A.diagonal()
    M = LinearOperator((N, N), matvec=lambda v: Minv * v)
    t = time.time()
    try:
        x, info = cg(A, b, rtol=tol, maxiter=maxiter, M=M)
    except TypeError:
        x, info = cg(A, b, tol=tol, maxiter=maxiter, M=M)
    I0 = float(np.sum(gb0[o0] * (x[i0[o0]] - 0.0)))       # current INTO the z=0 plane... sign: phi decreases with z
    I1 = float(np.sum(gb1[o1] * (x[i1[o1]] + 0.5)))
    # potential drop 0.5 over c/2 => drop 1 per cell; current magnitude per octant = |I0|
    return 4 * abs(I0) / c, abs(I1) / max(abs(I0), 1e-300), info, time.time() - t, N


def main():
    kind, s = sys.argv[1], float(sys.argv[2])
    ns = [int(v) for v in sys.argv[3].split(',')]
    q = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    ph = phi_sum(kind, s)
    for n in ns:
        t0 = time.time()
        fr, ins, c, dx = fractions(kind, s, n, q)
        out = []
        for mode in ('all', 'inside'):
            fz, bal, info, dt, N = solve(fr, ins, c, dx, mode)
            out.append((mode, fz, bal, info, dt, N))
        (ma, fa, ba, ia, ta, Na), (mi, fi, bi, ii, ti, Ni) = out
        print(f'{kind} s={s:.2f} n_oct={n} r/dx={1/dx:.1f} f_all={fa:.6f} (bal {ba:.6f}, cg {ia}, {ta:.0f}s, N {Na}) '
              f'f_inside={fi:.6f} (bal {bi:.6f}, cg {ii}, {ti:.0f}s) total {time.time()-t0:.0f}s', flush=True)
    for name, R in models(s).items():
        fn = net_f(kind, s, R)
        print(f'   {name:16s} f={fn:.6f}  T(phi_sum)={ph / fn:.4f}   phi_sum={ph:.5f}', flush=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())

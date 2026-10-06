#!/usr/bin/env python3
"""designC1 — 3D voxel FV (continuum reference) for periodic lattices of equal OVERLAPPING spheres,
vs the network edge models, with the field along [001].

Lattices (sphere radius r = 1, nearest-neighbour centre distance d = 2h, h = sqrt(1 - s^2), s = a/r):
  SC  (z=6)  cell c = d,          1 sphere,  current-carrying contacts: 2 (along z)
  BCC (z=8)  cell c = 2d/sqrt3,   2 spheres, all 8 contacts carry current (cos^2 = 1/3)
  FCC (z=12) cell c = d*sqrt2,    4 spheres, 8 of 12 contacts carry current (cos^2 = 1/2)
Only nearest-neighbour overlaps for s <= 0.45 (BCC 2nd shell overlaps for s > 0.5).

Continuum: sigma = 1 inside the union of spheres, 0 outside; periodic cell; potential drop 1 per
cell along z (phi(z + c) = phi(z) - 1).  f = sigma_eff/sigma = I/c.
Network (Bravais-lattice exact): f_net = (1/V_cell) * sum_{edges/cell} g_e dz_e^2.
phi_sum = N_sph*(4/3)pi/c^3 (sphere-volume sum, the release convention) · phi_union = voxel count.
"""
import math
import sys
import time
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import cg, LinearOperator


def lattice(kind, s):
    h = math.sqrt(1 - s * s)
    d = 2 * h
    if kind == 'SC':
        c = d; basis = [(0, 0, 0)]
    elif kind == 'BCC':
        c = 2 * d / math.sqrt(3); basis = [(0, 0, 0), (0.5, 0.5, 0.5)]
    elif kind == 'FCC':
        c = d * math.sqrt(2); basis = [(0, 0, 0), (0.5, 0.5, 0), (0.5, 0, 0.5), (0, 0.5, 0.5)]
    else:
        raise ValueError(kind)
    return h, d, c, basis


def solid_mask(kind, s, n):
    h, d, c, basis = lattice(kind, s)
    dx = c / n
    x = (np.arange(n) + 0.5) * dx
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
    m = np.zeros((n, n, n), bool)
    for (bx, by, bz) in basis:
        for ix in (-1, 0, 1):
            for iy in (-1, 0, 1):
                for iz in (-1, 0, 1):
                    cx, cy, cz = (bx + ix) * c, (by + iy) * c, (bz + iz) * c
                    m |= (X - cx) ** 2 + (Y - cy) ** 2 + (Z - cz) ** 2 <= 1.0
    return m, c, dx


def solve_cell(mask, c, dx, tol=1e-10, maxiter=20000):
    n = mask.shape[0]
    idx = -np.ones(mask.shape, np.int64)
    sol = np.flatnonzero(mask.ravel())
    idx.ravel()[sol] = np.arange(sol.size)
    N = sol.size
    g = dx  # sigma * dx^2 / dx
    rows, cols, vals = [], [], []
    b = np.zeros(N)
    diag = np.zeros(N)
    for ax in range(3):
        nb = np.roll(idx, -1, axis=ax)              # neighbour at +1 along ax (periodic)
        both = (idx >= 0) & (nb >= 0)
        i = idx[both]; j = nb[both]
        rows += [i, j]; cols += [j, i]; vals += [np.full(i.size, -g)] * 2
        np.add.at(diag, i, g); np.add.at(diag, j, g)
        if ax == 2:
            # faces crossing the top periodic boundary: A at k=n-1 -> B at k=0 (image at z+c has phi-1)
            sl = np.zeros(mask.shape, bool); sl[:, :, -1] = True
            cross = both & sl
            iA = idx[cross]; jB = nb[cross]
            np.add.at(b, iA, -g); np.add.at(b, jB, +g)
            crossA, crossB = iA, jB
    A = sparse.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                          shape=(N, N)).tocsr() + sparse.diags(diag)
    # pin the constant mode with a tiny shift (consistent system; shift does not change I)
    A = A + sparse.diags(np.full(N, 1e-12 * g))
    Minv = 1.0 / A.diagonal()
    M = LinearOperator((N, N), matvec=lambda v: Minv * v)
    t = time.time()
    try:
        phi, info = cg(A, b, rtol=tol, maxiter=maxiter, M=M)
    except TypeError:
        phi, info = cg(A, b, tol=tol, maxiter=maxiter, M=M)
    I = float(np.sum(g * (phi[crossA] - phi[crossB] + 1.0)))
    return I / c, info, time.time() - t, N


def phi_sum(kind, s):
    h, d, c, basis = lattice(kind, s)
    return len(basis) * (4 / 3) * math.pi / c ** 3


def net_f(kind, s, R_edge):
    """exact Bravais-lattice network f for edge resistance R_edge (sigma=1, r=1)."""
    h, d, c, basis = lattice(kind, s)
    g = 1.0 / R_edge
    if kind == 'SC':
        return g * d * d / c ** 3
    if kind == 'BCC':
        return 8 * g * (d * d / 3) / c ** 3
    if kind == 'FCC':
        return 16 * g * (d * d / 2) / c ** 3


def models(s):
    h = math.sqrt(1 - s * s)
    psi = (1 - s) ** 1.5
    Vseg = math.pi * (h - h ** 3 / 3)
    Rcyl = 2 * h / math.pi
    RW = 2 * h * h / Vseg
    RM = 1 / (2 * s)
    return {'H0 cyl+Maxwell': Rcyl + RM, 'H1 cyl+psi': Rcyl + psi * RM, 'H12 Wiener+psi': RW + psi * RM,
            'CF0 cyl': Rcyl, 'CF2 Wiener': RW}


def main():
    kinds = sys.argv[1].split(',') if len(sys.argv) > 1 else ['SC', 'BCC', 'FCC']
    ss = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else [0.2, 0.3, 0.4]
    ns = [int(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else [40, 60, 80]
    for kind in kinds:
        for s in ss:
            fs = []
            for n in ns:
                m, c, dx = solid_mask(kind, s, n)
                f, info, dt, N = solve_cell(m, c, dx)
                fs.append(f)
                print(f'{kind} s={s:.2f} n={n:4d} r/dx={1/dx:6.1f} N={N:8d} f={f:.6f} cg_info={info} '
                      f'{dt:6.1f}s phi_union={m.mean():.5f}', flush=True)
            if len(ns) >= 2:
                # first-order extrapolation in dx (dx ~ 1/n) from the two finest
                n1, n2 = ns[-2], ns[-1]
                f0 = (n2 * fs[-1] - n1 * fs[-2]) / (n2 - n1)
            else:
                f0 = fs[-1]
            ph = phi_sum(kind, s)
            print(f'  -> {kind} s={s:.2f}: f_FV(extrap)={f0:.6f}  phi_sum={ph:.5f}  T_FV(phi_sum)={ph / f0:.4f}')
            for name, R in models(s).items():
                fn = net_f(kind, s, R)
                print(f'     {name:16s} f={fn:.6f}  f/f_FV={fn / f0:7.4f}  T(phi_sum)={ph / fn:7.4f}')
    return 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""designC1 — RANDOM jammed packings of equal overlapping spheres (periodic cube, r = 1):
continuum cut-face FV vs the per-edge network models on the SAME realisation (paired).

packing : N random centres, FIRE minimisation of E = sum_{d<2} (2-d)^2 at fixed box (phi_sum set)
          -> jammed, overlapping, isotropic; contact s = a/r = sqrt(1-(d/2)^2).
network : periodic homogenisation, sigma_eff = (1/V) sum_e g_e (u_i - u_j + dz) dz with the KCL-solved u.
FV      : periodic cut-face FV, drop 1 per box along z, 'all' and 'inside' node sets (bracket).

usage: python3 fv_random.py N PHI SEED NVOX
"""
import math
import sys
import time
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import cg, LinearOperator, spsolve
from scipy.spatial import cKDTree


def mi(dv, L):
    return dv - L * np.round(dv / L)


def gen_packing(N, phi, seed, steps=20000):
    rng = np.random.default_rng(seed)
    L = (N * 4.0 / 3.0 * math.pi / phi) ** (1 / 3)
    x = rng.uniform(0, L, (N, 3))
    v = np.zeros_like(x)
    dt, alpha, nneg = 0.02, 0.1, 0
    for it in range(steps):
        tree = cKDTree(np.mod(x, L), boxsize=L)
        pairs = tree.query_pairs(2.0, output_type='ndarray')
        F = np.zeros_like(x)
        if len(pairs):
            dv = mi(x[pairs[:, 1]] - x[pairs[:, 0]], L)
            d = np.linalg.norm(dv, axis=1)
            fmag = 2 * (2 - d)                       # -dE/dd
            fv = (fmag / np.maximum(d, 1e-12))[:, None] * dv
            np.add.at(F, pairs[:, 1], fv)
            np.add.at(F, pairs[:, 0], -fv)
        P = (F * v).sum()
        if P > 0:
            vn, fn = np.linalg.norm(v), np.linalg.norm(F)
            v = (1 - alpha) * v + alpha * F * (vn / max(fn, 1e-30))
            nneg += 1
            if nneg > 5:
                dt = min(dt * 1.1, 0.1); alpha *= 0.99
        else:
            v[:] = 0; dt *= 0.5; alpha = 0.1; nneg = 0
        v += F * dt
        x += v * dt
        if np.abs(F).max() < 1e-7:
            break
    x = np.mod(x, L)
    return x, L, it


def contacts(x, L):
    tree = cKDTree(x, boxsize=L)
    pairs = tree.query_pairs(2.0, output_type='ndarray')
    dv = mi(x[pairs[:, 1]] - x[pairs[:, 0]], L)
    d = np.linalg.norm(dv, axis=1)
    return pairs, dv, d


def edge_R(d, model):
    h = d / 2
    s = np.sqrt(np.clip(1 - h * h, 0, None))
    psi = np.clip(1 - s, 0, None) ** 1.5
    RM = 1 / (2 * s)
    Rcyl = 2 * h / math.pi
    V = math.pi * (h - h ** 3 / 3)
    RW = 2 * h * h / V
    return {'H0': Rcyl + RM, 'H1': Rcyl + psi * RM, 'H12': RW + psi * RM, 'CF0': Rcyl, 'CF2': RW}[model]


def net_f(x, L, pairs, dv, d, model):
    N = len(x)
    g = 1.0 / edge_R(d, model)
    i, j = pairs[:, 0], pairs[:, 1]
    A = sparse.coo_matrix((np.concatenate([g, g, -g, -g]), (np.concatenate([i, j, i, j]), np.concatenate([i, j, j, i]))),
                          shape=(N, N)).tocsr()
    dz = dv[:, 2]
    b = np.zeros(N)
    np.add.at(b, i, -g * dz)        # KCL at i: sum g (u_i - u_j) = -sum g dz_ij  (dz_ij = z_j - z_i)
    np.add.at(b, j, +g * dz)
    A = A + sparse.diags(np.full(N, 1e-12 * g.mean()))
    # isolated nodes (rattlers): diagonal tiny -> u=0, no effect
    u = spsolve(A.tocsc(), b)
    I = g * (u[i] - u[j] + dz)      # current along +z per unit E... sign: I_ij = g(phi_i - phi_j'), phi = -z + u
    return float((I * dz).sum() / L ** 3), int((np.bincount(np.concatenate([i, j]), minlength=N)).mean() * 1)


def fv(x, L, n, q=3, mode='all', tol=1e-9):
    tree = cKDTree(x, boxsize=L)
    dx = L / n
    base = np.arange(n) * dx
    sub = (np.arange(q) + 0.5) / q * dx
    fr = []
    for ax in range(3):
        acc = np.zeros((n, n, n), np.float32)
        others = [k for k in range(3) if k != ax]
        for u in sub:
            for v in sub:
                cc = [None, None, None]
                cc[ax] = np.mod(base + dx, L)
                cc[others[0]] = base + u
                cc[others[1]] = base + v
                X, Y, Z = np.meshgrid(cc[0], cc[1], cc[2], indexing='ij')
                pts = np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1)
                dd, _ = tree.query(pts, k=1)
                acc += (dd <= 1.0).reshape(n, n, n)
        fr.append(acc / (q * q))
    vc = (np.arange(n) + 0.5) * dx
    X, Y, Z = np.meshgrid(vc, vc, vc, indexing='ij')
    dd, _ = tree.query(np.stack([X.ravel(), Y.ravel(), Z.ravel()], 1), k=1)
    ins = (dd <= 1.0).reshape(n, n, n)
    phi_union = ins.mean()
    g = [dx * f.astype(float) for f in fr]
    if mode == 'inside':
        active = ins
    else:
        active = np.zeros((n, n, n), bool)
        for ax in range(3):
            o = g[ax] > 0
            active |= o
            active |= np.roll(o, 1, axis=ax)
    idx = -np.ones((n, n, n), np.int64)
    act = np.flatnonzero(active.ravel())
    idx.ravel()[act] = np.arange(act.size)
    Nn = act.size
    rows, cols, vals = [], [], []
    diag = np.zeros(Nn)
    b = np.zeros(Nn)
    for ax in range(3):
        nb = np.roll(idx, -1, axis=ax)
        o = (g[ax] > 0) & (idx >= 0) & (nb >= 0)
        ii, jj, gg = idx[o], nb[o], g[ax][o]
        rows += [ii, jj]; cols += [jj, ii]; vals += [-gg, -gg]
        np.add.at(diag, ii, gg); np.add.at(diag, jj, gg)
        if ax == 2:
            sl = np.zeros((n, n, n), bool); sl[:, :, -1] = True
            cr = o & sl
            iA, jB, gc = idx[cr], nb[cr], g[2][cr]
            np.add.at(b, iA, -gc); np.add.at(b, jB, +gc)
    A = sparse.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                          shape=(Nn, Nn)).tocsr() + sparse.diags(diag + 1e-12 * dx)
    Minv = 1.0 / A.diagonal()
    M = LinearOperator((Nn, Nn), matvec=lambda vv: Minv * vv)
    try:
        sol, info = cg(A, b, rtol=tol, maxiter=60000, M=M)
    except TypeError:
        sol, info = cg(A, b, tol=tol, maxiter=60000, M=M)
    I = float(np.sum(gc * (sol[iA] - sol[jB] + 1.0)))
    return I / L, info, phi_union


def main():
    N, phi, seed, nvox = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    t0 = time.time()
    x, L, it = gen_packing(N, phi, seed)
    pairs, dv, d = contacts(x, L)
    s = np.sqrt(np.clip(1 - (d / 2) ** 2, 0, None))
    z = 2 * len(pairs) / N
    print(f'packing N={N} phi_sum={phi:.3f} seed={seed} L={L:.3f} FIRE it={it} contacts={len(pairs)} z={z:.2f} '
          f's: p10 {np.percentile(s,10):.3f} med {np.median(s):.3f} p90 {np.percentile(s,90):.3f} max {s.max():.3f} '
          f'({time.time()-t0:.0f}s)', flush=True)
    res = {}
    for m in ('H0', 'H1', 'H12', 'CF0', 'CF2'):
        res[m] = net_f(x, L, pairs, dv, d, m)[0]
    t1 = time.time()
    fa, ia, pu = fv(x, L, nvox, mode='all')
    fi, ii, _ = fv(x, L, nvox, mode='inside')
    print(f'  FV n={nvox} r/dx={nvox/L:.1f}: f_all={fa:.5f} (cg {ia}) f_inside={fi:.5f} (cg {ii}) phi_union={pu:.4f} '
          f'({time.time()-t1:.0f}s)', flush=True)
    fm = 0.5 * (fa + fi)
    for m, fn in res.items():
        print(f'  {m:4s} f={fn:.5f}  f/f_FV(all)={fn/fa:.3f}  f/f_FV(inside)={fn/fi:.3f}  T(phi_sum)={phi/fn:.3f}', flush=True)
    print(f'  T_FV(phi_sum) = {phi/fa:.3f}..{phi/fi:.3f}')
    return 0


if __name__ == '__main__':
    sys.exit(main())

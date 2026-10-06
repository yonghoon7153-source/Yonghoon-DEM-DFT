#!/usr/bin/env python3
"""designC1 — axisymmetric FV reference for the *sphere* (not cylinder) contact path.

Geometry (r = 1, sigma = 1): one period of an infinite chain of equal overlapping spheres =
a sphere truncated by the two contact planes z = +-h, h = sqrt(1 - s^2), s = a/r.
By symmetry the contact planes are equipotential (antisymmetry about the sphere's centre plane
+ translation), the free sphere surface is insulating.  => R_period(s) = exact centre-to-centre
resistance of one edge of the chain (sphere -> contact disc -> sphere), i.e. the quantity a
network edge R_edge = R_bulk,1 + R_c + R_bulk,2 must reproduce for the 2-contact sphere.

Cut-cell FV on a uniform (r, z) grid: face conductances use the OPEN part of each face
(z-faces: annulus clipped at rho(z_f); r-faces: z-extent where rho(z) >= r_face).
Validated against: cylinder (exact 2h/(pi b^2)), grid convergence, small-s Maxwell limit.

usage: python3 fv_sphere_chain.py [--selftest] [--table]
"""
import math
import sys
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve

TWO_PI = 2.0 * math.pi


def solve_profile(rho_fn, h, a_end, nr, R_out=1.0, sigma=1.0):
    """Axisymmetric body |z|<=h, 0<=r<=rho(z); Dirichlet on the end discs r<=a_end at z=+-h.
    Returns R = dV/I."""
    dr = R_out / nr
    nz = int(round(2 * h / dr))
    nz = max(nz + (nz % 2), 4)
    dz = 2 * h / nz
    rm = np.arange(nr) * dr
    rp = rm + dr
    zc = -h + (np.arange(nz) + 0.5) * dz
    zf = -h + np.arange(1, nz) * dz           # interior z-faces
    # z-face open areas (nr, nz-1)
    rho_f = np.array([rho_fn(z) for z in zf])
    top = np.minimum(rp[:, None], rho_f[None, :])
    Az = np.pi * np.clip(top ** 2 - rm[:, None] ** 2, 0.0, None)
    Gz = sigma * Az / dz
    # r-face open lengths (nr-1, nz): face at r = rp[i] (i < nr-1), z in [zc-dz/2, zc+dz/2]
    rf = rp[:-1]
    zmax = np.sqrt(np.clip(1.0 * 0 + np.array([rho_inv_sq(rho_fn, x, h) for x in rf]), 0.0, None))
    lo = zc[None, :] - dz / 2
    hi = zc[None, :] + dz / 2
    open_len = np.clip(np.minimum(hi, zmax[:, None]) - np.maximum(lo, -zmax[:, None]), 0.0, None)
    Gr = sigma * TWO_PI * rf[:, None] * open_len / dr
    # end discs (Dirichlet), half-cell distance
    Aend = np.pi * np.clip(np.minimum(rp, a_end) ** 2 - rm ** 2, 0.0, None)
    Gb = sigma * Aend / (dz / 2)
    n = nr * nz
    idx = np.arange(n).reshape(nr, nz)
    diag = np.zeros((nr, nz))
    diag[:-1, :] += Gr; diag[1:, :] += Gr
    diag[:, :-1] += Gz; diag[:, 1:] += Gz
    diag[:, 0] += Gb; diag[:, -1] += Gb
    rows = [idx.ravel()]; cols = [idx.ravel()]; vals = [diag.ravel()]
    a_, b_ = idx[:-1, :].ravel(), idx[1:, :].ravel(); g = (-Gr).ravel()
    rows += [a_, b_]; cols += [b_, a_]; vals += [g, g]
    a_, b_ = idx[:, :-1].ravel(), idx[:, 1:].ravel(); g = (-Gz).ravel()
    rows += [a_, b_]; cols += [b_, a_]; vals += [g, g]
    A = sparse.coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                          shape=(n, n)).tocsr()
    rhs = np.zeros((nr, nz))
    rhs[:, 0] = Gb * (-0.5); rhs[:, -1] = Gb * (+0.5)
    rhs = rhs.ravel()
    keep = diag.ravel() > 0
    Ak = A[keep][:, keep].tocsc()
    x = np.zeros(n)
    x[keep] = spsolve(Ak, rhs[keep])
    X = x.reshape(nr, nz)
    I = float(np.sum(Gb * (X[:, 0] - (-0.5))))
    return 1.0 / I, nz


def rho_inv_sq(rho_fn, r_face, h):
    """z_max^2 such that rho(z) >= r_face for |z| <= z_max (profile monotone in |z|, max at 0)."""
    if rho_fn(0.0) < r_face:
        return -1.0
    if rho_fn(h) >= r_face:
        return h * h
    lo, hi = 0.0, h
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if rho_fn(mid) >= r_face:
            lo = mid
        else:
            hi = mid
    return lo * lo


def sphere_chain_R(s, nr):
    h = math.sqrt(1.0 - s * s)
    rho = lambda z: math.sqrt(max(1.0 - z * z, 0.0))
    R, nz = solve_profile(rho, h, s, nr)
    return R, h, nz


def richardson(vals, nrs):
    """first-order cut-cell error: R(dr) = R0 + c*dr (+ ...).  Use the two finest (order 1) and
    report the 3-point estimate of the observed order as a check."""
    (r1, r2, r3), (n1, n2, n3) = vals, nrs
    R0_lin = (n3 * r3 - n2 * r2) / (n3 - n2)
    try:
        p = math.log(abs((r1 - r2) / (r2 - r3))) / math.log(n2 / n1)
    except (ValueError, ZeroDivisionError):
        p = float('nan')
    return R0_lin, p


def selftest():
    ok = True
    # cylinder exact: rho = b (multiple of dr), end disc = b
    for b, nr in ((0.5, 80), (1.0, 64)):
        h = 0.8
        R, _ = solve_profile(lambda z: b, h, b, nr)
        ex = 2 * h / (math.pi * b * b)
        e = abs(R / ex - 1)
        print(f'  cylinder b={b} nr={nr}: R={R:.10f} exact={ex:.10f} rel={e:.2e}')
        ok &= e < 1e-9
    # small-s limit: R*2a -> 1 as s -> 0 (Maxwell, two spreading resistances 1/(4a) each)
    return ok


def main():
    if '--selftest' in sys.argv:
        ok = selftest()
        print('SELFTEST', 'PASS' if ok else 'FAIL')
        return 0 if ok else 1
    ss = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.6, 0.7]
    nrs = (200, 400, 800)
    print(f'sphere chain, r=1 sigma=1 — R_period (centre plane equipotential by symmetry => R_half = R/2)')
    print(f'{"s":>5} {"h":>8} ' + ' '.join(f'R(nr={n})' for n in nrs) + '   R_extrap  p_obs')
    out = []
    for s in ss:
        vals = []
        for nr in nrs:
            R, h, nz = sphere_chain_R(s, nr)
            vals.append(R)
        R0, p = richardson(vals, nrs)
        out.append((s, h, *vals, R0, p))
        print(f'{s:5.2f} {h:8.5f} ' + ' '.join(f'{v:11.6f}' for v in vals) + f'  {R0:10.6f}  {p:5.2f}', flush=True)
    np.savetxt(__file__.replace('.py', '_table.txt'), np.array(out),
               header='s h R_nr200 R_nr400 R_nr800 R_extrap p_obs   (r=1, sigma=1; R = full period = 2*R_half)')
    return 0


if __name__ == '__main__':
    sys.exit(main())

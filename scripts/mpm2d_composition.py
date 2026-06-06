#!/usr/bin/env python3
"""2D MPM porosity vs AM:SE composition — true-plastic reference sweep.

Qualitative independent check of the porosity-vs-composition trend.
Two phases, compressed (confined oedometer) to a common target pressure:
  • SE  : soft  (E=24 GPa scaled), low yield  → plastically FLOWS, fills voids.
  • AM  : rigid (E=140 GPa scaled), ~no yield → jams, does not densify.
AM is bimodal (AM_P : AM_S = 7:3 by weight).  Area fractions from weight via
ρ_AM=4800, ρ_SE=2000.  Sweep AM weight fraction 0→100 %.

Expectation (matches the DEM-based v4 surface): porosity LOW at SE-rich
(soft fills voids), RISING toward AM-rich (rigid skeleton jams), with a
bimodal-packing dip at intermediate AM.

Run:  python3 scripts/mpm2d_composition.py
Out:  docs/figures/mpm2d_composition.png
"""
import numpy as np
import taichi as ti

ti.init(arch=ti.cpu, default_fp=ti.f32, random_seed=2)

n_grid = 128; dx = 1.0 / n_grid; inv_dx = float(n_grid)
dt = 2.0e-4
p_vol = (dx * 0.5) ** 2; p_mass = p_vol * 1.0
nu = 0.3
def lame(E):
    return E / (2 * (1 + nu)), E * nu / ((1 + nu) * (1 - 2 * nu))
MU_SE, LA_SE = lame(24.0);  MU_AM, LA_AM = lame(140.0)
YIELD_SE = 0.6           # SE flows plastically
YIELD_AM = 1.0e4         # AM ~rigid (never yields)

FLOOR = 0.08; SW_L, SW_R = 0.16, 0.84; WIDTH = SW_R - SW_L
WALL0 = 0.64; WALL_MIN = 0.22; WALL_V = 0.30
RHO_AM, RHO_SE = 4800.0, 2000.0
R_AMP, R_AMS, R_SE = 0.046, 0.014, 0.010     # stronger bimodal (ratio 4.6:1.4:1)
INIT_SOLID = 0.50                             # initial solid area frac (ε≈50%)

MAXP = 30000
x = ti.Vector.field(2, ti.f32, MAXP); v = ti.Vector.field(2, ti.f32, MAXP)
C = ti.Matrix.field(2, 2, ti.f32, MAXP); F = ti.Matrix.field(2, 2, ti.f32, MAXP)
mu_p = ti.field(ti.f32, MAXP); la_p = ti.field(ti.f32, MAXP); yld_p = ti.field(ti.f32, MAXP)
press = ti.field(ti.f32, MAXP)
grid_v = ti.Vector.field(2, ti.f32, (n_grid, n_grid)); grid_m = ti.field(ti.f32, (n_grid, n_grid))
wall_y = ti.field(ti.f32, ()); N = ti.field(ti.i32, ())


def area_fracs(am_wt):
    w = am_wt / 100.0
    if w <= 0: vam = 0.0
    elif w >= 1: vam = 1.0
    else:
        a = w / RHO_AM; b = (1 - w) / RHO_SE; vam = a / (a + b)
    return 0.7 * vam, 0.3 * vam, 1.0 - vam     # AM_P, AM_S, SE area fractions


def build(am_wt, rng, yield_se=YIELD_SE):
    fAP, fAS, fSE = area_fracs(am_wt)
    fill_h = WALL0 - 0.02
    box_area = WIDTH * (fill_h - FLOOR)
    target = INIT_SOLID * box_area
    placed = []   # (cx, cy, r, mu, la, yld)
    plan = [(R_AMP, fAP, MU_AM, LA_AM, YIELD_AM),
            (R_AMS, fAS, MU_AM, LA_AM, YIELD_AM),
            (R_SE,  fSE, MU_SE, LA_SE, yield_se)]
    for (r, frac, mu, la, yld) in plan:
        if frac <= 0: continue
        a_goal = frac * target; a_acc = 0.0; tries = 0
        while a_acc < a_goal and tries < 40000:
            tries += 1
            cx = rng.uniform(SW_L + r, SW_R - r)
            cy = rng.uniform(FLOOR + r, fill_h - r)
            ok = True
            for (px, py, pr, *_ ) in placed:
                if (cx - px) ** 2 + (cy - py) ** 2 < (r + pr + 0.004) ** 2:
                    ok = False; break
            if ok:
                placed.append((cx, cy, r, mu, la, yld)); a_acc += np.pi * r * r
    # rasterize disks to material points
    xs = []; mus = []; las = []; ylds = []
    for (cx, cy, r, mu, la, yld) in placed:
        k = int(r / (dx * 0.5)) + 1
        for a in range(-k, k + 1):
            for b in range(-k, k + 1):
                px = cx + a * dx * 0.5; py = cy + b * dx * 0.5
                if (px - cx) ** 2 + (py - cy) ** 2 <= r * r:
                    xs.append((px, py)); mus.append(mu); las.append(la); ylds.append(yld)
    return (np.array(xs, np.float32), np.array(mus, np.float32),
            np.array(las, np.float32), np.array(ylds, np.float32))


@ti.kernel
def load(xy: ti.types.ndarray(), mus: ti.types.ndarray(),
         las: ti.types.ndarray(), ylds: ti.types.ndarray(), n: ti.i32):
    N[None] = n
    for p in range(n):
        x[p] = ti.Vector([xy[p, 0], xy[p, 1]]); v[p] = ti.Vector([0.0, 0.0])
        C[p] = ti.Matrix.zero(ti.f32, 2, 2); F[p] = ti.Matrix.identity(ti.f32, 2)
        mu_p[p] = mus[p]; la_p[p] = las[p]; yld_p[p] = ylds[p]


@ti.kernel
def substep():
    for i, j in grid_m:
        grid_v[i, j] = ti.Vector([0.0, 0.0]); grid_m[i, j] = 0.0
    for p in range(N[None]):
        base = (x[p] * inv_dx - 0.5).cast(int); fx = x[p] * inv_dx - base.cast(ti.f32)
        w = [0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1.0) ** 2, 0.5 * (fx - 0.5) ** 2]
        U, sig, Vv = ti.svd(F[p]); J = sig[0, 0] * sig[1, 1]
        st = (2 * mu_p[p] * (F[p] - U @ Vv.transpose()) @ F[p].transpose()
              + ti.Matrix.identity(ti.f32, 2) * la_p[p] * J * (J - 1))
        press[p] = -0.5 * (st[0, 0] + st[1, 1])
        st = (-dt * p_vol * 4 * inv_dx * inv_dx) * st; affine = st + p_mass * C[p]
        for a, b in ti.static(ti.ndrange(3, 3)):
            off = ti.Vector([a, b]); dpos = (off.cast(ti.f32) - fx) * dx
            wt = w[a][0] * w[b][1]
            grid_v[base + off] += wt * (p_mass * v[p] + affine @ dpos)
            grid_m[base + off] += wt * p_mass
    for i, j in grid_m:
        if grid_m[i, j] > 0:
            grid_v[i, j] /= grid_m[i, j]
            if j * dx < FLOOR and grid_v[i, j][1] < 0: grid_v[i, j][1] = 0.0
            if j * dx > wall_y[None]: grid_v[i, j][1] = ti.min(grid_v[i, j][1], -WALL_V)
            if i * dx < SW_L and grid_v[i, j][0] < 0: grid_v[i, j][0] = 0.0
            if i * dx > SW_R and grid_v[i, j][0] > 0: grid_v[i, j][0] = 0.0
    for p in range(N[None]):
        base = (x[p] * inv_dx - 0.5).cast(int); fx = x[p] * inv_dx - base.cast(ti.f32)
        w = [0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1.0) ** 2, 0.5 * (fx - 0.5) ** 2]
        nv = ti.Vector.zero(ti.f32, 2); nc = ti.Matrix.zero(ti.f32, 2, 2)
        for a, b in ti.static(ti.ndrange(3, 3)):
            off = ti.Vector([a, b]); dpos = off.cast(ti.f32) - fx
            wt = w[a][0] * w[b][1]; gv = grid_v[base + off]
            nv += wt * gv; nc += 4 * inv_dx * wt * gv.outer_product(dpos)
        v[p] = nv; C[p] = nc; F[p] = (ti.Matrix.identity(ti.f32, 2) + dt * nc) @ F[p]
        U, sig, Vv = ti.svd(F[p])
        e0 = ti.log(ti.max(sig[0, 0], 1e-4)); e1 = ti.log(ti.max(sig[1, 1], 1e-4))
        tr = e0 + e1; d0 = e0 - 0.5 * tr; d1 = e1 - 0.5 * tr
        dn = ti.sqrt(d0 * d0 + d1 * d1) + 1e-9; dg = dn - yld_p[p] / (2 * mu_p[p])
        if dg > 0:
            m0 = (d0 - dg * d0 / dn) + 0.5 * tr; m1 = (d1 - dg * d1 / dn) + 0.5 * tr
            F[p] = U @ ti.Matrix([[ti.exp(m0), 0.0], [0.0, ti.exp(m1)]]) @ Vv.transpose()
        x[p] += dt * v[p]


def run_composition(xy, mus, las, ylds, solid_area):
    n = len(xy)
    load(xy, mus, las, ylds, n)
    wall_y[None] = WALL0
    series = []
    sub = 50; nf = 120
    for frame in range(nf):
        for _ in range(sub): substep()
        wall_y[None] = max(WALL0 - WALL_V * (frame + 1) * sub * dt, WALL_MIN)
        top = wall_y[None]
        por = max(0.0, 1.0 - solid_area / (WIDTH * (top - FLOOR))) * 100.0
        pr = float(np.mean(press.to_numpy()[:n]))
        series.append((por, pr))
    return np.array(series), n


def sweep(yield_se, rng):
    comps = list(range(0, 101, 10))
    runs = []
    for am in comps:
        xy, mus, las, ylds = build(am, rng, yield_se)
        solid_area = len(xy) * p_vol
        s, n = run_composition(xy, mus, las, ylds, solid_area)
        runs.append((am, s, n))
    P_COMMON = min(s[:, 1].max() for _, s, _ in runs) * 0.95
    res = []
    for am, s, n in runs:
        order = np.argsort(s[:, 1])
        res.append((am, float(np.interp(P_COMMON, s[:, 1][order], s[:, 0][order]))))
    return np.array(res), P_COMMON


def main():
    # DECISIVE test: is the Furnas dip a RIGID-fine-phase packing feature?
    #   plastic SE (flows, fills voids)  vs  rigid SE (packs, Furnas)
    rng = np.random.default_rng(7)
    r_plastic, pc1 = sweep(YIELD_SE, rng)     # SE plastic (true LPSCl-like)
    print("  --- plastic SE done ---")
    rng = np.random.default_rng(7)
    r_rigid, pc2 = sweep(1.0e4, rng)          # SE rigid (DEM-overlap-like)
    print("  --- rigid SE done ---")
    for (a, pp), (_, pr) in zip(r_plastic, r_rigid):
        print(f"  AM {int(a):3d}wt%  ε_plastic={pp:5.1f}%   ε_rigid={pr:5.1f}%")

    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 5.2))
    ax.plot(r_plastic[:, 0], r_plastic[:, 1], '-o', color='#2e8b57', lw=2, ms=6,
            label='SE PLASTIC (flows → fills voids)')
    ax.plot(r_rigid[:, 0], r_rigid[:, 1], '-s', color='#c0392b', lw=2, ms=6,
            label='SE RIGID (packs → Furnas)')
    ax.set_xlabel('AM weight fraction (%)'); ax.set_ylabel('porosity ε at common pressure (%)')
    ax.set_title('2D MPM — does the Furnas dip appear?\n'
                 'plastic vs rigid SE (AM rigid 140GPa bimodal; ρ_AM=4.8, ρ_SE=2.0)', fontsize=10)
    ax.legend(); ax.grid(alpha=0.3)
    plt.tight_layout()
    import os; os.makedirs('docs/figures', exist_ok=True)
    plt.savefig('docs/figures/mpm2d_composition.png', dpi=130)
    print("saved docs/figures/mpm2d_composition.png")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""3D MPM compaction — production: soft plastic SE (shape-flow) + rigid AM.

True-plastic, large-deformation, GPU MPM.  Captures what the DEM cannot: the SE
material points plastically FLOW (change shape) into the voids, conserving volume,
so the COMPOSITE densifies correctly (the DEM's rigid spheres can't void-fill).
von Mises (J2) per phase: SE soft+low-yield → flows; AM stiff+high-yield → jams.

Confined (oedometer) compaction by a servo platen to a target axial stress
(measured as the volume-mean Cauchy σzz = bulk pressure, mirrors the DEM virial).
Porosity = 1 − solid_volume/(box_area·height).  Units: length dimensionless [0,1],
modulus/stress in GPa, so σzz and --target-gpa are literal GPa.

Calibration: pure-SE (--material SE) → tune (--e-se, --sigma-y) so porosity ≈ 10 %
@ 0.3 GPa (Minnmann).  Then --material mix --am-frac <vol AM> for the composite.

Run:  python3 scripts/mpm3d_compaction.py --material SE --n-grid 96 --arch cpu
      python3 scripts/mpm3d_compaction.py --material SE --n-grid 256 --arch cuda
"""
import argparse
import sys

import numpy as np


def parse_args(argv):
    ap = argparse.ArgumentParser(description="3D MPM compaction (servo to target σzz).")
    ap.add_argument('--arch', default='cpu', choices=['cpu', 'gpu', 'cuda', 'vulkan'])
    ap.add_argument('--n-grid', type=int, default=96)
    ap.add_argument('--material', default='SE', choices=['SE', 'mix'])
    ap.add_argument('--am-frac', type=float, default=0.0, help='AM volume fraction of SOLID (mix)')
    ap.add_argument('--e-se', type=float, default=1.53, help='SE modulus (GPa); champion 1.53 (softened)')
    ap.add_argument('--e-am', type=float, default=140.0, help='AM modulus (GPa)')
    ap.add_argument('--sigma-y', type=float, default=0.15, help='SE von Mises yield (GPa); champion 0.15')
    ap.add_argument('--target-gpa', type=float, default=0.30, help='servo platen target σzz (GPa)')
    ap.add_argument('--init-solid', type=float, default=0.45, help='initial solid fraction (loose)')
    ap.add_argument('--r-am', type=float, default=0.045, help='AM radius (box units; raise n-grid for 12:4:1)')
    ap.add_argument('--r-se', type=float, default=0.018, help='SE radius (box units)')
    ap.add_argument('--frames', type=int, default=400)
    ap.add_argument('--sub', type=int, default=40)
    ap.add_argument('--dt', type=float, default=2.0e-4)
    ap.add_argument('--seed', type=int, default=3)
    ap.add_argument('--gpu-mem', type=float, default=3.0)
    ap.add_argument('--quiet', action='store_true')
    return ap.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    import taichi as ti
    arch = {'gpu': ti.gpu, 'cuda': ti.cuda, 'vulkan': ti.vulkan, 'cpu': ti.cpu}[args.arch]
    kw = dict(arch=arch, default_fp=ti.f32, random_seed=args.seed)
    if args.arch in ('gpu', 'cuda'):
        kw['device_memory_GB'] = args.gpu_mem
    ti.init(**kw)

    n_grid = args.n_grid
    dx = 1.0 / n_grid; inv_dx = float(n_grid)
    dt = args.dt
    p_vol = (dx * 0.5) ** 3; p_mass = p_vol * 1.0
    nu = 0.3

    def lame(E):
        return E / (2 * (1 + nu)), E * nu / ((1 + nu) * (1 - 2 * nu))
    MU_SE, LA_SE = lame(args.e_se); MU_AM, LA_AM = lame(args.e_am)
    YIELD_SE = args.sigma_y; YIELD_AM = 1.0e4               # AM ~rigid (no yield)

    FLOOR = 0.10; SW = (0.18, 0.82)                         # confined box in x,y
    WIDTH = SW[1] - SW[0]
    WALL0 = 0.60; WALL_MIN = 0.16
    am_frac = args.am_frac if args.material == 'mix' else 0.0

    # ── build material points: place spheres (AM + SE), fill with points ────────
    rng = np.random.default_rng(args.seed)
    fill_h = WALL0 - 0.03
    box_vol = WIDTH * WIDTH * (fill_h - FLOOR)
    target = args.init_solid * box_vol
    plan = [(args.r_am, am_frac, MU_AM, LA_AM, YIELD_AM),
            (args.r_se, 1.0 - am_frac, MU_SE, LA_SE, YIELD_SE)]
    placed = []
    for (r, frac, mu, la, yld) in plan:
        if frac <= 1e-9:
            continue
        goal = frac * target; acc = 0.0; fails = 0
        while acc < goal and fails < 200000:
            c = (rng.uniform(SW[0] + r, SW[1] - r), rng.uniform(SW[0] + r, SW[1] - r),
                 rng.uniform(FLOOR + r, fill_h - r))
            ok = True
            for (px, py, pz, pr, *_ ) in placed:
                if (c[0] - px) ** 2 + (c[1] - py) ** 2 + (c[2] - pz) ** 2 < (r + pr + 0.004) ** 2:
                    ok = False; break
            if ok:
                placed.append((c[0], c[1], c[2], r, mu, la, yld)); acc += (4 / 3) * np.pi * r ** 3; fails = 0
            else:
                fails += 1
    xs, mus, las, ylds = [], [], [], []
    for (cx, cy, cz, r, mu, la, yld) in placed:
        k = int(r / (dx * 0.5)) + 1
        for a in range(-k, k + 1):
            for b in range(-k, k + 1):
                for cc in range(-k, k + 1):
                    px, py, pz = cx + a * dx * 0.5, cy + b * dx * 0.5, cz + cc * dx * 0.5
                    if (px - cx) ** 2 + (py - cy) ** 2 + (pz - cz) ** 2 <= r * r:
                        xs.append((px, py, pz)); mus.append(mu); las.append(la); ylds.append(yld)
    xs = np.array(xs, np.float32)
    n = len(xs)
    if n < 2:
        print("build failed (n<2) — raise --n-grid or --init-solid"); return
    mus = np.array(mus, np.float32); las = np.array(las, np.float32); ylds = np.array(ylds, np.float32)

    x = ti.Vector.field(3, ti.f32, n); v = ti.Vector.field(3, ti.f32, n)
    C = ti.Matrix.field(3, 3, ti.f32, n); F = ti.Matrix.field(3, 3, ti.f32, n)
    mu_p = ti.field(ti.f32, n); la_p = ti.field(ti.f32, n); yld_p = ti.field(ti.f32, n)
    grid_v = ti.Vector.field(3, ti.f32, (n_grid,) * 3); grid_m = ti.field(ti.f32, (n_grid,) * 3)
    wall_z = ti.field(ti.f32, ()); wall_vel = ti.field(ti.f32, ()); szz = ti.field(ti.f32, ())

    @ti.kernel
    def load(xy: ti.types.ndarray(), ms: ti.types.ndarray(), ls: ti.types.ndarray(), ys: ti.types.ndarray()):
        for p in range(n):
            x[p] = ti.Vector([xy[p, 0], xy[p, 1], xy[p, 2]]); v[p] = ti.Vector([0.0, 0.0, 0.0])
            C[p] = ti.Matrix.zero(ti.f32, 3, 3); F[p] = ti.Matrix.identity(ti.f32, 3)
            mu_p[p] = ms[p]; la_p[p] = ls[p]; yld_p[p] = ys[p]

    @ti.kernel
    def substep():
        for I in ti.grouped(grid_m):
            grid_v[I] = ti.Vector.zero(ti.f32, 3); grid_m[I] = 0.0
        szz[None] = 0.0
        for p in range(n):
            base = (x[p] * inv_dx - 0.5).cast(int); fx = x[p] * inv_dx - base.cast(ti.f32)
            w = [0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1.0) ** 2, 0.5 * (fx - 0.5) ** 2]
            U, sig, V = ti.svd(F[p])
            J = sig[0, 0] * sig[1, 1] * sig[2, 2]
            P = (2 * mu_p[p] * (F[p] - U @ V.transpose()) @ F[p].transpose()
                 + ti.Matrix.identity(ti.f32, 3) * la_p[p] * J * (J - 1))     # Kirchhoff τ = Jσ
            szz[None] += -P[2, 2] / J                                         # -σzz = compressive axial pressure (GPa)
            st = (-dt * p_vol * 4 * inv_dx * inv_dx) * P; affine = st + p_mass * C[p]
            for a, b, c in ti.static(ti.ndrange(3, 3, 3)):
                off = ti.Vector([a, b, c]); dpos = (off.cast(ti.f32) - fx) * dx
                wt = w[a][0] * w[b][1] * w[c][2]
                grid_v[base + off] += wt * (p_mass * v[p] + affine @ dpos)
                grid_m[base + off] += wt * p_mass
        for I in ti.grouped(grid_m):
            if grid_m[I] > 0:
                grid_v[I] /= grid_m[I]
                i, j, k = I[0], I[1], I[2]
                if k * dx < FLOOR and grid_v[I][2] < 0: grid_v[I][2] = 0.0
                if k * dx > wall_z[None]: grid_v[I][2] = wall_vel[None]      # servo platen (rigid)
                if i * dx < SW[0] and grid_v[I][0] < 0: grid_v[I][0] = 0.0
                if i * dx > SW[1] and grid_v[I][0] > 0: grid_v[I][0] = 0.0
                if j * dx < SW[0] and grid_v[I][1] < 0: grid_v[I][1] = 0.0
                if j * dx > SW[1] and grid_v[I][1] > 0: grid_v[I][1] = 0.0
        for p in range(n):
            base = (x[p] * inv_dx - 0.5).cast(int); fx = x[p] * inv_dx - base.cast(ti.f32)
            w = [0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1.0) ** 2, 0.5 * (fx - 0.5) ** 2]
            nv = ti.Vector.zero(ti.f32, 3); nc = ti.Matrix.zero(ti.f32, 3, 3)
            for a, b, c in ti.static(ti.ndrange(3, 3, 3)):
                off = ti.Vector([a, b, c]); dpos = off.cast(ti.f32) - fx
                wt = w[a][0] * w[b][1] * w[c][2]; gv = grid_v[base + off]
                nv += wt * gv; nc += 4 * inv_dx * wt * gv.outer_product(dpos)
            v[p] = nv; C[p] = nc; F[p] = (ti.Matrix.identity(ti.f32, 3) + dt * nc) @ F[p]
            U, sig, V = ti.svd(F[p])
            e = ti.Vector([ti.log(ti.max(sig[0, 0], 1e-4)), ti.log(ti.max(sig[1, 1], 1e-4)),
                           ti.log(ti.max(sig[2, 2], 1e-4))])
            tr = (e[0] + e[1] + e[2]) / 3.0
            d = e - ti.Vector([tr, tr, tr]); dn = d.norm() + 1e-9
            dg = dn - yld_p[p] / (2 * mu_p[p])
            if dg > 0:
                e = (d - dg * d / dn) + ti.Vector([tr, tr, tr])
                F[p] = U @ ti.Matrix([[ti.exp(e[0]), 0, 0], [0, ti.exp(e[1]), 0],
                                      [0, 0, ti.exp(e[2])]]) @ V.transpose()
            x[p] += dt * v[p]

    load(xs, mus, las, ylds)
    solid_vol = n * p_vol; area = WIDTH * WIDTH
    target = args.target_gpa
    vmax = 0.04 * (WALL0 - FLOOR)                            # platen speed (box units / frame)
    wall_z[None] = WALL0
    if not args.quiet:
        print(f"3D MPM  n_grid={n_grid}  pts={n}  arch={args.arch}  {args.material} "
              f"(am_frac={am_frac})  E_SE={args.e_se} σy={args.sigma_y}  target={target} GPa")
    reached = False; conv = 0; por_end = 0.0; p_end = 0.0
    for frame in range(args.frames):
        sacc = 0.0
        for _ in range(args.sub):
            substep()
            sacc += szz[None] / n                            # volume-mean Cauchy σzz (GPa)
        p = sacc / args.sub
        # servo platen to target σzz (descend until target, then fine bidirectional)
        if not reached:
            if p < target:
                wall_vel[None] = -vmax / (args.sub * dt)
                wall_z[None] = max(WALL_MIN, wall_z[None] - vmax)
            else:
                reached = True; wall_vel[None] = 0.0
        else:
            step = 0.12 * vmax
            if p > 1.02 * target:
                wall_z[None] = min(WALL0, wall_z[None] + step); wall_vel[None] = step / (args.sub * dt)
            elif p < 0.98 * target:
                wall_z[None] = max(WALL_MIN, wall_z[None] - step); wall_vel[None] = -step / (args.sub * dt)
            else:
                wall_vel[None] = 0.0
            conv = conv + 1 if abs(p - target) < 0.03 * target else 0
        height = wall_z[None] - FLOOR
        por = max(0.0, 1.0 - solid_vol / (area * height)) * 100.0
        por_end = por; p_end = p
        if not args.quiet and (frame % 20 == 0 or conv >= 12):
            print(f"  frame {frame:3d} [{'descend' if not reached else 'servo'}]  "
                  f"σzz={p:7.4f} GPa  porosity={por:6.2f}%  wall_z={wall_z[None]:.3f}", flush=True)
        if conv >= 12 and frame > 20:
            if not args.quiet:
                print("  ✓ converged: σzz equilibrated at target")
            break
    print(f"FINAL  σzz={p_end:.4f} GPa  porosity={por_end:.2f}%   "
          f"[MPM, {args.material}, am_frac={am_frac}, n_grid={n_grid}, pts={n}]")


if __name__ == '__main__':
    main(sys.argv[1:])

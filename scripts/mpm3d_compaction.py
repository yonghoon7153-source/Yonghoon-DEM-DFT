#!/usr/bin/env python3
"""3D MPM compaction — production: soft plastic SE (shape-flow) + rigid AM.

True-plastic, large-deformation, GPU MPM.  Captures what the DEM cannot: the SE
material points plastically FLOW (change shape) into the voids, conserving volume,
so the COMPOSITE densifies correctly (the DEM's rigid spheres can't void-fill).
von Mises (J2) per phase: SE soft+low-yield → flows; AM stiff+high-yield → jams.

Confined (oedometer) compaction by a servo platen to a target axial stress.
Default readout = wallP (the platen REACTION stress, Σ m·Δv/(dt·area)): it is the
true boundary BC and resolution-invariant, whereas the volume-mean Cauchy σzz
(--readout sigzz) is diluted by the well-resolved soft SE and over-compresses (the
2D "512 blocker" lesson, CLAUDE.md).  Both are printed every frame for comparison.
Porosity = 1 − solid_volume/(box_area·height).  Units: length dimensionless [0,1],
modulus/stress in GPa, so σzz and --target-gpa are literal GPa.

3D pure-SE calibration (GPU, n_grid=256): E_SE=1.53, ν_SE=0.49 (K≈25.5 GPa, the
real LPSC bulk → no volumetric over-crush), σy=0.30 → porosity ≈ 10 % @ 0.30 GPa
(Minnmann).  These are the defaults.  Then --material mix --am-frac <vol AM> for
the composite.

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
    ap.add_argument('--preset', default='none', choices=['none', 'real14'],
                    help='real14 = production input_real_14 (3-comp AM_P6/AM_S2/SE0.5um = 12:4:1, '
                         'actual vol AM:SE 73:27, 50um RVE → cross-validate porosity vs LIGGGHTS 15.6%)')
    ap.add_argument('--e-se', type=float, default=1.53, help='SE modulus (GPa); champion 1.53 (softened)')
    ap.add_argument('--e-am', type=float, default=140.0, help='AM modulus (GPa)')
    ap.add_argument('--sigma-y', type=float, default=0.30,
                    help='SE von Mises yield (GPa); 3D calib 0.30 -> pure-SE ~0.10 porosity @ 0.30 GPa (Minnmann)')
    ap.add_argument('--nu-se', type=float, default=0.49,
                    help='SE Poisson ratio (default 0.49 = 3D calib: K~25.5 GPa, the real LPSC bulk; '
                         'soft shear -> incompressible granular flow; nu<=0.45 over-crushes to 0 porosity)')
    ap.add_argument('--target-gpa', type=float, default=0.30, help='servo platen target σzz (GPa)')
    ap.add_argument('--readout', default='wallP', choices=['wallP', 'sigzz'],
                    help='servo signal: wallP (platen reaction, resolution-invariant) or sigzz (volume-mean)')
    ap.add_argument('--init-solid', type=float, default=0.35,
                    help='initial solid fraction (loose; keep <=0.38 RSA saturation)')
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
    def lame(E, nu):
        return E / (2 * (1 + nu)), E * nu / ((1 + nu) * (1 - 2 * nu))
    MU_SE, LA_SE = lame(args.e_se, args.nu_se); MU_AM, LA_AM = lame(args.e_am, 0.30)
    K_SE = LA_SE + 2.0 * MU_SE / 3.0                        # SE bulk modulus (GPa) — stiff if ν→0.49
    YIELD_SE = args.sigma_y; YIELD_AM = 1.0e4               # AM ~rigid (no yield)

    FLOOR = 0.10; SW = (0.18, 0.82)                         # confined box in x,y
    WIDTH = SW[1] - SW[0]
    WALL0 = 0.60; WALL_MIN = 0.105                          # just above FLOOR (servo stops earlier)
    am_frac = args.am_frac if args.material == 'mix' else 0.0

    # ── build material points: place spheres (two-tier RSA: big AM brute + small SE
    #    fine-grid, like the DEM — a uniform brute is O(N²) and stalls) ───────────
    rng = np.random.default_rng(args.seed)
    if args.preset == 'real14':
        # production input_real_14: 3-component AM_P 6µm + AM_S 2µm + SE 0.5µm (12:4:1),
        # 50×50µm RVE, ACTUAL voxel composition AM_P:AM_S:SE = 0.51:0.22:0.27 (AM:SE 73:27).
        # Map 50µm → the near-full lateral box; tall column for the loose bed.  SE material =
        # our MPM calibration (defaults E=1.53/ν=0.49/σy=0.30), AM ~rigid — NOT the LIGGGHTS
        # DEM contact params (frame [4]: each model calibrated to experiment independently).
        SW = (0.02, 0.98); WIDTH = SW[1] - SW[0]
        FLOOR = 0.05; WALL0 = 0.90; WALL_MIN = 0.055
        scl = WIDTH / 50.0                                  # box units per µm
        r_amp, r_ams, r_se3 = 6.0 * scl, 2.0 * scl, 0.5 * scl
        plan = [(r_amp, 0.51, MU_AM, LA_AM, YIELD_AM),
                (r_ams, 0.22, MU_AM, LA_AM, YIELD_AM),
                (r_se3, 0.27, MU_SE, LA_SE, YIELD_SE)]
    else:
        plan = [(args.r_am, am_frac, MU_AM, LA_AM, YIELD_AM),
                (args.r_se, 1.0 - am_frac, MU_SE, LA_SE, YIELD_SE)]
    fill_h = WALL0 - 0.03
    box_vol = WIDTH * WIDTH * (fill_h - FLOOR)
    target = args.init_solid * box_vol
    vol = lambda r: (4.0 / 3.0) * np.pi * r ** 3           # noqa: E731
    plan = [pk for pk in plan if pk[1] > 1e-9]
    rmin = min(pk[0] for pk in plan)
    cell = 2.0 * rmin
    placed, big, grid = [], [], {}

    def hits_big(p, r):
        for (qx, qy, qz, qr) in big:
            if (p[0] - qx) ** 2 + (p[1] - qy) ** 2 + (p[2] - qz) ** 2 < (r + qr + 0.004) ** 2:
                return True
        return False

    def hits_small(p, r):
        kx, ky, kz = int(p[0] / cell), int(p[1] / cell), int(p[2] / cell)
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                for c in (-1, 0, 1):
                    for (qx, qy, qz, qr) in grid.get((kx + a, ky + b, kz + c), ()):
                        if (p[0] - qx) ** 2 + (p[1] - qy) ** 2 + (p[2] - qz) ** 2 < (r + qr + 0.004) ** 2:
                            return True
        return False

    for (r, frac, mu, la, yld) in plan:
        goal = frac * target; acc = 0.0; fails = 0
        small = r <= 1.5 * rmin
        while acc < goal and fails < 60000:
            p = (rng.uniform(SW[0] + r, SW[1] - r), rng.uniform(SW[0] + r, SW[1] - r),
                 rng.uniform(FLOOR + r, fill_h - r))
            ok = (not hits_big(p, r)) and (not (small and hits_small(p, r)))
            if ok:
                placed.append((p[0], p[1], p[2], r, mu, la, yld)); acc += vol(r); fails = 0
                if small:
                    grid.setdefault((int(p[0] / cell), int(p[1] / cell), int(p[2] / cell)), []).append(
                        (p[0], p[1], p[2], r))
                else:
                    big.append((p[0], p[1], p[2], r))
            else:
                fails += 1
    # ── voxelize spheres into material points (numpy-vectorized: per-radius in-sphere
    #    offset template × particle centers, broadcast + chunked).  Replaces the old
    #    per-point O(N·k³) Python triple loop that took minutes at n_grid≥512. ────────
    placed_arr = np.asarray(placed, np.float64)            # [N,7] cx,cy,cz,r,mu,la,yld
    xs_list, mu_list, la_list, yld_list = [], [], [], []
    for r in np.unique(placed_arr[:, 3]):
        grp = placed_arr[placed_arr[:, 3] == r]
        mu_v, la_v, yld_v = grp[0, 4], grp[0, 5], grp[0, 6]
        k = int(r / (dx * 0.5)) + 1
        ax = np.arange(-k, k + 1) * (dx * 0.5)
        ox, oy, oz = np.meshgrid(ax, ax, ax, indexing='ij')
        off = np.stack([ox.ravel(), oy.ravel(), oz.ravel()], 1)
        off = off[(off ** 2).sum(1) <= r * r]              # in-sphere offsets [Pin,3]
        centers = grp[:, :3]
        chunk = max(1, 16_000_000 // max(1, off.shape[0]))  # cap broadcast intermediate
        for s in range(0, len(centers), chunk):
            pts = (centers[s:s + chunk, None, :] + off[None]).reshape(-1, 3)
            m = pts.shape[0]
            xs_list.append(pts.astype(np.float32))
            mu_list.append(np.full(m, mu_v, np.float32))
            la_list.append(np.full(m, la_v, np.float32))
            yld_list.append(np.full(m, yld_v, np.float32))
    xs = np.concatenate(xs_list)
    n = len(xs)
    if n < 2:
        print("build failed (n<2) — raise --n-grid or --init-solid"); return
    mus = np.concatenate(mu_list); las = np.concatenate(la_list); ylds = np.concatenate(yld_list)

    x = ti.Vector.field(3, ti.f32, n); v = ti.Vector.field(3, ti.f32, n)
    C = ti.Matrix.field(3, 3, ti.f32, n); F = ti.Matrix.field(3, 3, ti.f32, n)
    mu_p = ti.field(ti.f32, n); la_p = ti.field(ti.f32, n); yld_p = ti.field(ti.f32, n)
    grid_v = ti.Vector.field(3, ti.f32, (n_grid,) * 3); grid_m = ti.field(ti.f32, (n_grid,) * 3)
    wall_z = ti.field(ti.f32, ()); wall_vel = ti.field(ti.f32, ()); szz = ti.field(ti.f32, ())
    wallf = ti.field(ti.f32, ())                                # platen reaction impulse Σ m·Δv (per substep)

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
        szz[None] = 0.0; wallf[None] = 0.0
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
                if k * dx > wall_z[None]:                                    # servo platen (rigid)
                    wallf[None] += grid_m[I] * (grid_v[I][2] - wall_vel[None])  # reaction impulse Σ m·Δv
                    grid_v[I][2] = wall_vel[None]
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
    vmax = 0.008 * (WALL0 - FLOOR)                           # platen speed (slow = quasi-static)
    wall_z[None] = WALL0
    comp = ("real14 (3-comp 12:4:1, AM:SE 73:27)" if args.preset == 'real14'
            else f"{args.material} (am_frac={am_frac})")
    if not args.quiet:
        print(f"3D MPM  n_grid={n_grid}  pts={n}  arch={args.arch}  {comp}  "
              f"E_SE={args.e_se} σy={args.sigma_y} ν_SE={args.nu_se} K_SE={K_SE:.2f}GPa  "
              f"target={target} GPa  readout={args.readout}")
    reached = False; conv = 0; por_end = 0.0; p_end = 0.0; por_at_target = -1.0; por0 = 100.0
    for frame in range(args.frames):
        sacc = 0.0; wacc = 0.0
        for _ in range(args.sub):
            substep()
            sacc += szz[None] / n                            # volume-mean Cauchy σzz (GPa)
            wacc += wallf[None] / (dt * area)                # platen reaction stress (GPa), resolution-invariant
        sig_mean = sacc / args.sub
        wallp = wacc / args.sub
        p = wallp if args.readout == 'wallP' else sig_mean   # servo signal
        height = wall_z[None] - FLOOR
        por = max(0.0, 1.0 - solid_vol / (area * height)) * 100.0
        if frame == 0:
            por0 = por
        # servo platen to target σzz (descend until target, then fine bidirectional).
        # arm-after-compaction guard: a big rigid AM hitting the platen on first contact
        # spikes wallP transiently; refuse to stop until the bed has actually compacted
        # (por ≤ por0 − 5 %p), else the servo arms prematurely and crawls (under-compacts).
        if not reached:
            if p < target or por > por0 - 5.0:
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
        por_end = por; p_end = p
        if reached and por_at_target < 0:
            por_at_target = por                              # porosity when target stress was FIRST reached
        if not args.quiet and (frame % 20 == 0 or conv >= 12):
            print(f"  frame {frame:3d} [{'descend' if not reached else 'servo'}]  "
                  f"{args.readout}={p:7.4f} GPa (wallP={wallp:.4f} σzz_vol={sig_mean:.4f})  "
                  f"porosity={por:6.2f}%  wall_z={wall_z[None]:.3f}", flush=True)
        if conv >= 12 and frame > 20:
            if not args.quiet:
                print("  ✓ converged: σzz equilibrated at target")
            break
    por_target_str = f"{por_at_target:.2f}%" if por_at_target >= 0 else "n/a (target never reached)"
    print(f"FINAL  {args.readout}={p_end:.4f} GPa  porosity(settled)={por_end:.2f}%  "
          f"porosity@target={por_target_str}   "
          f"[MPM, {args.material}, am_frac={am_frac}, n_grid={n_grid}, pts={n}, "
          f"E_SE={args.e_se} ν_SE={args.nu_se} K_SE={K_SE:.1f}GPa, readout={args.readout}]")


if __name__ == '__main__':
    main(sys.argv[1:])

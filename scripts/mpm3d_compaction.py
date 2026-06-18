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
    ap.add_argument('--am-scaffold', default='',
                    help='CSV of fixed AM (type,x,y,z,r in LIGGGHTS 0..0.05 units): AM become a fixed '
                         'grid obstacle and only SE is the MPM filler (real skeleton, no RSA AM, light)')
    ap.add_argument('--save-se', default='', help='write final SE point positions (npy) for morphology')
    ap.add_argument('--save-dg', default='', help='write accumulated plastic strain Σdg per SE point '
                    '(npy, SAME order as --save-se) → colour the morphology slice by plastic strain')
    ap.add_argument('--save-metrics', default='',
                    help='write ALL raw MPM outputs (porosity, thickness, coverage, seed density, '
                         'grid/material params, stress) to a JSON — the structured source for the '
                         'webapp compare table + payload (so nothing is recomputed at coarse mesh res)')
    ap.add_argument('--se-frac', type=float, default=0.27,
                    help='scaffold SE volume fraction of SOLID (default 0.27 = real_14 actual; vary to '
                         'see porosity respond — final porosity is a RESULT of plastic SE fill, not assumed)')
    ap.add_argument('--se-dump', default='',
                    help='CSV of REAL SE positions (type,x,y,z,r, same units as --am-scaffold): seed '
                         'D1 SE spheres at the actual DEM SE centres instead of uniform cell-fill, so '
                         'SE volume·distribution are REAL → porosity·coverage EMERGE (no se_frac/targeting)')
    ap.add_argument('--coh', type=float, default=0.0,
                    help='SE cohesion / adhesion (GPa, Cauchy): cold-weld + vdW of the soft sulfide — '
                         'an attractive stress that reduces the net contact repulsion → densifies. '
                         'Real physics (not a target fudge); LPSC ~0.01-0.05 GPa.  Acts in compression.')
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
    ap.add_argument('--protocol', default='servo', choices=['servo', 'hold'],
                    help='servo = bidirectional, equilibrate AT target; hold = LIGGGHTS protocol '
                         '(descend to target, FIX the platen, relax) — porosity = value at first 300 MPa')
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
    dt = args.dt                                           # per-point p_vol/p_mass (set in build):
    #   soft SE → fine voxelization (dx/2), rigid AM → coarse (dx) to cap memory at 12:1 ratio
    def lame(E, nu):
        return E / (2 * (1 + nu)), E * nu / ((1 + nu) * (1 - 2 * nu))
    MU_SE, LA_SE = lame(args.e_se, args.nu_se); MU_AM, LA_AM = lame(args.e_am, 0.30)
    K_SE = LA_SE + 2.0 * MU_SE / 3.0                        # SE bulk modulus (GPa) — stiff if ν→0.49
    YIELD_SE = args.sigma_y; YIELD_AM = 1.0e4               # AM ~rigid (no yield)
    COH = float(args.coh)                                   # SE cohesion/adhesion (GPa, Cauchy)
    # CFL-safe dt: cap by the stiffest material P-wave speed c=√((λ+2µ)/ρ), ρ=1.  With AM as a
    # MATERIAL (preset/mix, E_AM=140) the default dt blows up at high n_grid (CUDA illegal
    # address); the scaffold (AM = grid mask, only soft SE) keeps the default dt.
    _has_am_mat = (args.preset == 'real14') or (args.material == 'mix' and not args.am_scaffold)
    _M = LA_SE + 2.0 * MU_SE
    if _has_am_mat:
        _M = max(_M, LA_AM + 2.0 * MU_AM)
    dt = min(args.dt, 0.4 * dx / (_M ** 0.5))

    FLOOR = 0.10; SW = (0.18, 0.82)                         # confined box in x,y
    WIDTH = SW[1] - SW[0]
    WALL0 = 0.60; WALL_MIN = 0.105                          # just above FLOOR (servo stops earlier)
    am_frac = args.am_frac if args.material == 'mix' else 0.0

    # ── build material points: place spheres (two-tier RSA: big AM brute + small SE
    #    fine-grid, like the DEM — a uniform brute is O(N²) and stalls) ───────────
    rng = np.random.default_rng(args.seed)
    am_c = None; am_r = None; AM_vol = 0.0; am_top = 0.0; um_box = 0.0   # fixed-AM scaffold bookkeeping
    if args.am_scaffold:
        # DEM→MPM scaffold: real AM are FIXED (loaded from the LIGGGHTS dump) and become a grid
        # obstacle; only SE is the MPM material, RSA-packed into the interstices to a target volume
        # fraction.  The plate then plastically compacts the SE around the fixed real skeleton, so
        # the porosity is a RESULT of the SE plastic fill (drops from the rigid-RSA value), not assumed.
        SW = (0.04, 0.96); WIDTH = SW[1] - SW[0]; FLOOR = 0.05
        amraw = np.loadtxt(args.am_scaffold, delimiter=',')
        scl = WIDTH / 0.05                                     # box units per LIGGGHTS unit (50µm→WIDTH)
        am_c = np.column_stack([SW[0] + amraw[:, 1] * scl, SW[0] + amraw[:, 2] * scl,
                                FLOOR + amraw[:, 3] * scl]).astype(np.float64)
        am_r = (amraw[:, 4] * scl).astype(np.float64)
        AM_vol = float(np.sum((4.0 / 3.0) * np.pi * am_r ** 3))
        am_top = float((am_c[:, 2] + am_r).max())
        WALL0 = am_top + 0.05; WALL_MIN = FLOOR + 0.01
        r_se3 = 0.0005 * scl                                  # SE 0.5µm → box units
        um_box = 1000.0 / scl                                 # µm per box unit (50µm RVE = 0.05 LIGGGHTS u)
        pin_np = np.zeros((n_grid,) * 3, np.int32)            # grid cells inside any fixed AM
        for _i in range(len(am_r)):
            cx, cy, cz = am_c[_i]; rr = float(am_r[_i])
            lo = np.maximum(np.floor((np.array([cx, cy, cz]) - rr) * n_grid).astype(int), 0)
            hi = np.minimum(np.ceil((np.array([cx, cy, cz]) + rr) * n_grid).astype(int), n_grid)
            if np.any(hi <= lo):
                continue
            gx = (np.arange(lo[0], hi[0]) + 0.5) / n_grid
            gy = (np.arange(lo[1], hi[1]) + 0.5) / n_grid
            gz = (np.arange(lo[2], hi[2]) + 0.5) / n_grid
            X, Y, Z = np.meshgrid(gx, gy, gz, indexing='ij')
            pin_np[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]][(X - cx) ** 2 + (Y - cy) ** 2 + (Z - cz) ** 2 <= rr * rr] = int(amraw[_i, 0])
        se_target = AM_vol * args.se_frac / (1.0 - args.se_frac)   # SE volume to RSA-fill
        plan = [(r_se3, 1.0, MU_SE, LA_SE, YIELD_SE)]
    elif args.preset == 'real14':
        # production input_real_14: 3-component AM_P 6µm + AM_S 2µm + SE 0.5µm (12:4:1),
        # 50×50µm RVE, ACTUAL voxel composition AM_P:AM_S:SE = 0.51:0.22:0.27 (AM:SE 73:27).
        # Map 50µm → the near-full lateral box; tall column for the loose bed.  SE material =
        # our MPM calibration (defaults E=1.53/ν=0.49/σy=0.30), AM ~rigid — NOT the LIGGGHTS
        # DEM contact params (frame [4]: each model calibrated to experiment independently).
        SW = (0.02, 0.98); WIDTH = SW[1] - SW[0]
        FLOOR = 0.05; WALL0 = 0.90; WALL_MIN = 0.055
        scl = WIDTH / 50.0                                  # box units per µm
        r_amp, r_ams, r_se3 = 6.0 * scl, 2.0 * scl, 0.5 * scl
        um_box = 1.0 / scl                                  # µm per box unit (preset scl = box/µm)
        plan = [(r_amp, 0.51, MU_AM, LA_AM, YIELD_AM),
                (r_ams, 0.22, MU_AM, LA_AM, YIELD_AM),
                (r_se3, 0.27, MU_SE, LA_SE, YIELD_SE)]
    else:
        plan = [(args.r_am, am_frac, MU_AM, LA_AM, YIELD_AM),
                (args.r_se, 1.0 - am_frac, MU_SE, LA_SE, YIELD_SE)]
    fill_h = (am_top if args.am_scaffold else WALL0 - 0.03)
    box_vol = WIDTH * WIDTH * (fill_h - FLOOR)
    target = (se_target if args.am_scaffold else args.init_solid * box_vol)
    vol = lambda r: (4.0 / 3.0) * np.pi * r ** 3           # noqa: E731
    plan = [pk for pk in plan if pk[1] > 1e-9]
    rmin = min(pk[0] for pk in plan)
    cell = 2.0 * rmin
    placed, big, grid = [], [], {}

    def in_am(p):                                          # O(1) fixed-AM rejection via grid mask
        if not args.am_scaffold:
            return False
        ii = min(int(p[0] * n_grid), n_grid - 1); jj = min(int(p[1] * n_grid), n_grid - 1)
        kk = min(int(p[2] * n_grid), n_grid - 1)
        return pin_np[ii, jj, kk] > 0

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

    if args.am_scaffold:
        spc = dx * 0.5
        i0 = int(SW[0] * n_grid) + 1; i1 = int(SW[1] * n_grid)
        k0 = int(FLOOR * n_grid) + 1; k1 = int(am_top * n_grid)
        if args.se_dump:
            # ── seed SE at the REAL DEM SE centres: rasterise each D1 SE sphere into the grid
            #    (voxel union → no overlap double-count), keep only non-AM cells.  SE volume and
            #    spatial distribution are then REAL, so porosity·coverage EMERGE from the data
            #    (no se_frac, no --target-porosity). ──────────────────────────────────────────
            seraw = np.loadtxt(args.se_dump, delimiter=',')
            se_c = np.column_stack([SW[0] + seraw[:, 1] * scl, SW[0] + seraw[:, 2] * scl,
                                    FLOOR + seraw[:, 3] * scl])
            se_rr = (seraw[:, 4] * scl).astype(np.float64)
            se_pin = np.zeros((n_grid,) * 3, bool)
            for _i in range(len(se_rr)):
                cx, cy, cz = se_c[_i]; rr = float(se_rr[_i])
                lo = np.maximum(np.floor((np.array([cx, cy, cz]) - rr) * n_grid).astype(int), 0)
                hi = np.minimum(np.ceil((np.array([cx, cy, cz]) + rr) * n_grid).astype(int), n_grid)
                if np.any(hi <= lo):
                    continue
                gx = (np.arange(lo[0], hi[0]) + 0.5) / n_grid
                gy = (np.arange(lo[1], hi[1]) + 0.5) / n_grid
                gz = (np.arange(lo[2], hi[2]) + 0.5) / n_grid
                X, Y, Z = np.meshgrid(gx, gy, gz, indexing='ij')
                se_pin[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]] |= (
                    (X - cx) ** 2 + (Y - cy) ** 2 + (Z - cz) ** 2 <= rr * rr)
            se_pin &= (pin_np == 0)                          # SE only in non-AM cells
            sel = np.argwhere(se_pin)
            seed_str = f"{len(seraw)} real SE spheres → {len(sel):,} SE cells (REAL positions, no targeting)"
        else:
            # ── uniform cell-fill: a se_target/interstitial-vol fraction of the non-AM bed cells
            #    (porosity a RESULT of plastic fill, not RSA-limited). ──────────────────────────
            free = pin_np[i0:i1, i0:i1, k0:k1] == 0
            inter = np.argwhere(free) + np.array([i0, i0, k0])
            prob = min(1.0, se_target / max(len(inter) * dx ** 3, 1e-12))
            sel = inter[rng.random(len(inter)) < prob]
            seed_str = f"{len(sel):,} SE cells, interstitial fill {prob*100:.0f}% (se_frac {args.se_frac})"
        subo = np.array([[a, b, c] for a in (0.25, 0.75) for b in (0.25, 0.75)
                         for c in (0.25, 0.75)]) * dx       # 8 sub-positions per cell
        xs = ((sel[:, None, :] * dx) + subo[None]).reshape(-1, 3).astype(np.float32)
        n = len(xs)
        if n < 2:
            print("scaffold build failed (n<2) — check --am-scaffold / --se-frac / --se-dump"); return
        mus = np.full(n, MU_SE, np.float32); las = np.full(n, LA_SE, np.float32)
        ylds = np.full(n, YIELD_SE, np.float32); pvs = np.full(n, spc ** 3, np.float32)
        # ── density / volume-fraction watch (real ρ: AM 4800, SE 2000 kg/m³ from the LIGGGHTS deck) ──
        se_solid = len(sel) * dx ** 3
        am_solid = float((pin_np > 0).sum()) * dx ** 3
        bed_vol = WIDTH * WIDTH * (am_top - FLOOR)
        f_am = 100.0 * am_solid / bed_vol; f_se = 100.0 * se_solid / bed_vol
        bulk_rho = (am_solid * 4800.0 + se_solid * 2000.0) / bed_vol / 1000.0
        print(f"  scaffold: {len(am_r)} fixed AM + {seed_str} ({n:,} pts)")
        print(f"  seed density: AM {f_am:.1f}% / SE {f_se:.1f}% / void {max(0.0,100-f_am-f_se):.1f}%  "
              f"(SE/solid {100*se_solid/max(am_solid+se_solid,1e-12):.1f}%)  "
              f"ρ_bulk≈{bulk_rho:.2f} g/cm³  bed {(am_top-FLOOR)*um_box:.1f}µm")
    else:
        for (r, frac, mu, la, yld) in plan:
            goal = frac * target; acc = 0.0; fails = 0
            small = r <= 1.5 * rmin
            while acc < goal and fails < 60000:
                p = (rng.uniform(SW[0] + r, SW[1] - r), rng.uniform(SW[0] + r, SW[1] - r),
                     rng.uniform(FLOOR + r, fill_h - r))
                ok = (not in_am(p)) and (not hits_big(p, r)) and (not (small and hits_small(p, r)))
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
        #    offset template × particle centers, broadcast + chunked). ──────────────────
        placed_arr = np.asarray(placed, np.float64)        # [N,7] cx,cy,cz,r,mu,la,yld
        xs_list, mu_list, la_list, yld_list, pv_list = [], [], [], [], []
        for r in np.unique(placed_arr[:, 3]):
            grp = placed_arr[placed_arr[:, 3] == r]
            mu_v, la_v, yld_v = grp[0, 4], grp[0, 5], grp[0, 6]
            spc = dx if yld_v > 100.0 else dx * 0.5        # AM (rigid, high yld) coarse; SE fine
            pvg = spc ** 3                                 # per-point volume (= mass, ρ=1) for this group
            k = int(r / spc) + 1
            ax = np.arange(-k, k + 1) * spc
            ox, oy, oz = np.meshgrid(ax, ax, ax, indexing='ij')
            off = np.stack([ox.ravel(), oy.ravel(), oz.ravel()], 1)
            off = off[(off ** 2).sum(1) <= r * r]          # in-sphere offsets [Pin,3]
            centers = grp[:, :3]
            chunk = max(1, 16_000_000 // max(1, off.shape[0]))
            for s in range(0, len(centers), chunk):
                pts = (centers[s:s + chunk, None, :] + off[None]).reshape(-1, 3)
                m = pts.shape[0]
                xs_list.append(pts.astype(np.float32))
                mu_list.append(np.full(m, mu_v, np.float32))
                la_list.append(np.full(m, la_v, np.float32))
                yld_list.append(np.full(m, yld_v, np.float32))
                pv_list.append(np.full(m, pvg, np.float32))
        xs = np.concatenate(xs_list)
        n = len(xs)
        if n < 2:
            print("build failed (n<2) — raise --n-grid or --init-solid"); return
        mus = np.concatenate(mu_list); las = np.concatenate(la_list); ylds = np.concatenate(yld_list)
        pvs = np.concatenate(pv_list)
    xs = np.clip(xs, 2.0 * dx, 1.0 - 2.0 * dx)             # keep the 3-pt P2G stencil inside [0,n_grid)
    solid_vol = float(pvs.sum()) + AM_vol                  # voxelized SE vol (Σ per-point) + exact fixed-AM
    #   vol.  Σ per-point matches the old n·p_vol so the pure-SE 10% calibration is preserved.

    x = ti.Vector.field(3, ti.f32, n); v = ti.Vector.field(3, ti.f32, n)
    C = ti.Matrix.field(3, 3, ti.f32, n); F = ti.Matrix.field(3, 3, ti.f32, n)
    mu_p = ti.field(ti.f32, n); la_p = ti.field(ti.f32, n); yld_p = ti.field(ti.f32, n)
    pvol_p = ti.field(ti.f32, n)                                # per-point volume (= mass, ρ=1)
    dg_acc = ti.field(ti.f32, n)                                # accumulated plastic strain Σdg per point
    grid_v = ti.Vector.field(3, ti.f32, (n_grid,) * 3); grid_m = ti.field(ti.f32, (n_grid,) * 3)
    wall_z = ti.field(ti.f32, ()); wall_vel = ti.field(ti.f32, ()); szz = ti.field(ti.f32, ())
    wallf = ti.field(ti.f32, ())                                # platen reaction impulse Σ m·Δv (per substep)
    scaffold_on = bool(args.am_scaffold)                        # fixed-AM grid obstacle (real skeleton)
    am_mask = ti.field(ti.i32, (n_grid,) * 3 if scaffold_on else (1, 1, 1))
    if scaffold_on:
        am_mask.from_numpy(pin_np)                              # cells inside fixed AM (built in scaffold branch)

    @ti.kernel
    def load(xy: ti.types.ndarray(), ms: ti.types.ndarray(), ls: ti.types.ndarray(),
             ys: ti.types.ndarray(), pv: ti.types.ndarray()):
        for p in range(n):
            x[p] = ti.Vector([xy[p, 0], xy[p, 1], xy[p, 2]]); v[p] = ti.Vector([0.0, 0.0, 0.0])
            C[p] = ti.Matrix.zero(ti.f32, 3, 3); F[p] = ti.Matrix.identity(ti.f32, 3)
            mu_p[p] = ms[p]; la_p[p] = ls[p]; yld_p[p] = ys[p]; pvol_p[p] = pv[p]

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
            if ti.static(COH > 0.0):                                         # SE cohesion (cold-weld/vdW):
                if yld_p[p] < 100.0 and J < 1.0:                             # attractive σ in compression →
                    P += COH * J * ti.Matrix.identity(ti.f32, 3)            # reduces net repulsion → densifies
            szz[None] += -P[2, 2] / J                                         # -σzz = compressive axial pressure (GPa)
            pm = pvol_p[p]                                                    # per-point vol = mass (ρ=1)
            st = (-dt * pm * 4 * inv_dx * inv_dx) * P; affine = st + pm * C[p]
            for a, b, c in ti.static(ti.ndrange(3, 3, 3)):
                off = ti.Vector([a, b, c]); dpos = (off.cast(ti.f32) - fx) * dx
                wt = w[a][0] * w[b][1] * w[c][2]
                grid_v[base + off] += wt * (pm * v[p] + affine @ dpos)
                grid_m[base + off] += wt * pm
        for I in ti.grouped(grid_m):
            if grid_m[I] > 0:
                grid_v[I] /= grid_m[I]
                if ti.static(scaffold_on):                              # fixed AM = rigid obstacle (v=0)
                    if am_mask[I] > 0:
                        grid_v[I] = ti.Vector.zero(ti.f32, 3)
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
                dg_acc[p] += dg                                 # accumulate plastic strain (morphology colour)
                e = (d - dg * d / dn) + ti.Vector([tr, tr, tr])
                F[p] = U @ ti.Matrix([[ti.exp(e[0]), 0, 0], [0, ti.exp(e[1]), 0],
                                      [0, 0, ti.exp(e[2])]]) @ V.transpose()
            x[p] += dt * v[p]

    load(xs, mus, las, ylds, pvs)
    area = WIDTH * WIDTH                                    # solid_vol = exact Σ sphere vol (set in build)
    target = args.target_gpa
    vmax = 0.008 * (WALL0 - FLOOR)                           # platen speed (slow = quasi-static)
    wall_z[None] = WALL0
    comp = (f"scaffold ({len(am_r)} fixed AM + SE "
            + ("se_dump REAL positions)" if args.se_dump else f"se_frac={args.se_frac})") if args.am_scaffold
            else "real14 (3-comp 12:4:1, AM:SE 73:27)" if args.preset == 'real14'
            else f"{args.material} (am_frac={am_frac})")
    if not args.quiet:
        print(f"3D MPM  n_grid={n_grid}  pts={n}  arch={args.arch}  {comp}  "
              f"E_SE={args.e_se} σy={args.sigma_y} ν_SE={args.nu_se} K_SE={K_SE:.2f}GPa  "
              f"target={target} GPa  readout={args.readout}")
    reached = False; conv = 0; por_end = 0.0; p_end = 0.0; por_at_target = -1.0; por0 = 100.0; relax = 0
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
        # arm-after-compaction guard: a big rigid AM (preset/mix, AM = MATERIAL) hitting the
        # platen on first contact spikes wallP transiently → refuse to stop until the bed has
        # actually compacted (por ≤ por0 − 5 %p).  The scaffold (AM = fixed grid mask) has NO
        # such transient, and the guard there forces a 5 %p over-descent regardless of stress,
        # which OVER-COMPRESSES dense (high se_frac) beds → disable it for the scaffold.
        if not reached:
            guard = (por > por0 - 5.0) and not args.am_scaffold
            if p < target or guard:
                wall_vel[None] = -vmax / (args.sub * dt)
                wall_z[None] = max(WALL_MIN, wall_z[None] - vmax)
            else:
                reached = True; wall_vel[None] = 0.0
        elif args.protocol == 'hold':
            # LIGGGHTS protocol: platen FIXED at the first-300-MPa position; relax (stress settles,
            # plate does not move → porosity stays at porosity@target).  No bidirectional over/under-shoot.
            wall_vel[None] = 0.0; relax += 1
            if relax >= 40 and frame > 20:
                if not args.quiet:
                    print("  ✓ held at target, relaxed (LIGGGHTS protocol)")
                break
        else:
            step = 0.12 * vmax                                   # bidirectional: equilibrate AT target
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
            thick = f"  thickness={height*um_box:5.2f}µm" if um_box > 0 else ""
            print(f"  frame {frame:3d} [{'descend' if not reached else 'servo'}]  "
                  f"{args.readout}={p:7.4f} GPa (wallP={wallp:.4f} σzz_vol={sig_mean:.4f})  "
                  f"porosity={por:6.2f}%  wall_z={wall_z[None]:.3f}{thick}", flush=True)
        if conv >= 12 and frame > 20:
            if not args.quiet:
                print("  ✓ converged: σzz equilibrated at target")
            break
    por_target_str = f"{por_at_target:.2f}%" if por_at_target >= 0 else "n/a (target never reached)"
    scaf = (f"scaffold {len(am_r)}AM " + ("se_dump(real)" if args.se_dump else f"se_frac={args.se_frac}")
            if args.am_scaffold else f"am_frac={am_frac}")
    thick_str = (f"  thickness={(wall_z[None] - FLOOR) * um_box:.2f}µm" if um_box > 0 else "")
    print(f"FINAL  {args.readout}={p_end:.4f} GPa  porosity(settled)={por_end:.2f}%  "
          f"porosity@target={por_target_str}{thick_str}   "
          f"[MPM, {comp.split()[0]}, {scaf}, n_grid={n_grid}, pts={n}, "
          f"E_SE={args.e_se} ν_SE={args.nu_se} K_SE={K_SE:.1f}GPa, readout={args.readout}]")
    cov_out = {}
    if args.am_scaffold:
        # COVERAGE: fraction of each AM-type surface (AM↔non-AM voxel interfaces) that faces SE
        # (vs void).  The MPM SE plastically conforms to the AM, so this is the REAL coverage —
        # validates the DEM coverage post-corrections (Hertz / Tabor-physics / B3 shape-corr).
        xf = x.to_numpy()
        ci = np.clip((xf * n_grid).astype(int), 0, n_grid - 1)
        se_occ = np.zeros((n_grid,) * 3, bool)
        se_occ[ci[:, 0], ci[:, 1], ci[:, 2]] = True
        # close the discrete SE occupancy to fill point-sampling holes at the interface —
        # the raw 'point in the adjacent cell' measure UNDER-counts coverage otherwise
        # (geometric ground-truth is ~16 % touching / ~49 % within 0.14 µm; raw read ~26 %).
        try:
            from scipy import ndimage as _ndi
            se_occ = _ndi.binary_closing(se_occ, iterations=1)
        except Exception:
            pass
        for t, nm in ((1, 'AM_P'), (2, 'AM_S')):
            amt = (pin_np == t); tot = 0; cov = 0
            for ax in range(3):
                for s in (1, -1):
                    iface = amt & (np.roll(pin_np, s, ax) == 0)   # AM_t voxel with a non-AM neighbour
                    tot += int(iface.sum())
                    cov += int((iface & np.roll(se_occ, s, ax)).sum())
            pct = 100.0 * cov / tot if tot else 0.0
            cov_out[nm] = round(pct, 1)
            if tot:
                print(f"  coverage {nm} by SE = {pct:5.1f}%   ({cov:,}/{tot:,} surface voxels)")
    if args.save_metrics:
        # ── ALL raw MPM outputs → one structured JSON (the webapp's MPM source) ──────────────
        import json as _json
        m = {
            'porosity_settled_pct': round(float(por_end), 3),
            'porosity_at_target_pct': round(float(por_at_target), 3) if por_at_target >= 0 else None,
            'thickness_um': round(float((wall_z[None] - FLOOR) * um_box), 3) if um_box > 0 else None,
            'wall_z': round(float(wall_z[None]), 4),
            'final_stress_GPa': round(float(p_end), 4), 'target_GPa': float(target),
            'coverage_AM_P_pct': cov_out.get('AM_P'), 'coverage_AM_S_pct': cov_out.get('AM_S'),
            'n_grid': int(n_grid), 'n_pts': int(n),
            'E_SE_GPa': float(args.e_se), 'nu_SE': float(args.nu_se),
            'sigma_y_GPa': float(args.sigma_y), 'K_SE_GPa': round(float(K_SE), 3),
            'protocol': args.protocol, 'readout': args.readout,
            'se_dump': bool(args.se_dump), 'se_frac': float(args.se_frac),
        }
        if args.am_scaffold:
            m.update({
                'seed_AM_frac_pct': round(float(f_am), 2), 'seed_SE_frac_pct': round(float(f_se), 2),
                'SE_of_solid_pct': round(100.0 * se_solid / max(am_solid + se_solid, 1e-12), 2),
                'bulk_density_g_cm3': round(float(bulk_rho), 3), 'n_AM': int(len(am_r)),
            })
        _json.dump(m, open(args.save_metrics, 'w'), indent=2)
        print(f"  saved metrics → {args.save_metrics}  ({len(m)} fields)")
    if args.save_se:
        np.save(args.save_se, x.to_numpy())                # final SE point cloud (morphology)
        print(f"  saved SE morphology → {args.save_se} ({n} pts)")
    if args.save_dg:
        dgn = dg_acc.to_numpy()
        np.save(args.save_dg, dgn)                          # accumulated plastic strain (same order)
        print(f"  saved plastic strain Σdg → {args.save_dg} ({n} pts, "
              f"mean {float(dgn.mean()):.3f} max {float(dgn.max()):.3f})")


if __name__ == '__main__':
    main(sys.argv[1:])

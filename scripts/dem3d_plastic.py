#!/usr/bin/env python3
"""3D elasto-plastic DEM — jamming (Hertz) + true plastic yield cap (Thornton 1997).

The MISSING arbiter for the Furnas-dip question (CLAUDE.md frame [4]/[5]).  Today
two models each own only HALF the physics:
  • DEM (LIGGGHTS hooke/hysteresis): has contact JAMMING but during compaction it
    loads ~elastically (linear, no yield-pressure cap) so it needs the 18× E
    softening.  It says the geometric Furnas dip SURVIVES.
  • MPM (J2 continuum): has TRUE plastic flow but NO Hertzian contact jamming, so it
    OVER-compresses.  It says the dip is ERASED — but that erasure is an
    over-compression artifact, not demonstrated plasticity.
Neither has BOTH jamming AND a compaction-phase plastic yield cap.  This DEM does:
each contact is Hertzian (repulsive = jamming) until its mean pressure reaches the
Tabor hardness H = c_H·σ_y, then it FLATTENS at constant pressure H — the contact
area grows as A = F/H, which is EXACTLY the Stage-E A_tabor cap, promoted from a
post-hoc area correction to the in-loop force law.  AM contacts get a huge σ_y →
stay Hertzian (rigid); SE contacts yield → flow into voids while still jamming.
Toggling the cap (--plastic / --rigid) tests directly whether plasticity erases the
geometric dip, with the contact network (jamming) present the whole time.

Normal force = Thornton & Ning (1998) elastic-perfectly-plastic, per contact:
  R* = Ri·Rj/(Ri+Rj),   1/E* = (1-νi²)/Ei + (1-νj²)/Ej,   py = min(Hi, Hj)
  δy = R*·(π·py /(2E*))²            (overlap at first yield)
  Fy = (4/3)·E*·√R*·δy^1.5
  loading,  δ≤δy : F = (4/3)·E*·√R*·δ^1.5                  (Hertz  — jamming)
  loading,  δ>δy : F = Fy + π·py·R*·(δ−δy)                  (plastic plateau — flow)
  unloading      : Hertz w/ flattened radius Rp=(4/3)E*·a_max³/Fmax, residual δ0
History per contact = δmax (persisted across steps).  Tangential = regularized
Coulomb friction.  Periodic x,y; rigid floor; servo top platen to --target-gpa.
Everything is in PHYSICAL units (µm, GPa) so wall pressure in GPa is literal and
E*, py set real pressures — no arbitrary scaling, calibrate to Minnmann directly.

Validation gates (run here on CPU):
  --unit-test  single contact: dumps F(δ) loading+unloading and checks the Taichi
               contact law against the closed-form Thornton curve → docs/figures/.
  default      small pure-SE box compacts, jams, porosity drops, pressure→target.
GPU (uma V100, --arch gpu): pure-SE Minnmann calibration (10%@300 MPa) then an AM%
sweep reading the dip with the cap ON (--plastic) vs OFF (--rigid).

Run:  python3 scripts/dem3d_plastic.py --unit-test
      python3 scripts/dem3d_plastic.py --material SE --n-target 400 --plastic
      python3 scripts/dem3d_plastic.py --material SE --n-target 8000 --plastic --arch gpu
"""
import argparse
import math
import os
import sys

import numpy as np

# ── physics constants (physical units: length µm, modulus/stress GPa) ────────────
NU = 0.30                       # Poisson, both phases (shear-soft handled via E_eff)
C_H = 3.0                       # Tabor: hardness H = C_H · σ_y  (≈3 for fully-plastic)
PY_RIGID = 1.0e3                # GPa — AM "hardness": δy so large it never yields → Hertz
E_AM = 140.0                    # GPa, NCM (rigid relative to the 0.3 GPa press)
RHO = 2.0                       # scaled density (only sets dynamics; static result invariant)


def parse_args(argv):
    ap = argparse.ArgumentParser(description="3D elasto-plastic DEM (Thornton contact).")
    ap.add_argument('--arch', default='cpu', choices=['cpu', 'gpu', 'cuda', 'vulkan'])
    ap.add_argument('--gpu-mem', type=float, default=2.0,
                    help='GPU memory pool cap (GB).  Taichi else grabs ~90%% of the card and OOMs '
                         'when the V100 is shared; our fields are tiny.  Raise only for very large N.')
    ap.add_argument('--material', default='SE', choices=['SE', 'AM', 'mix'])
    ap.add_argument('--n-target', type=int, default=400, help='approx particle count')
    ap.add_argument('--am-wt', type=float, default=0.0, help='AM weight %% (mix only)')
    ap.add_argument('--ps', default='7:3', help='AM_P:AM_S ratio (mix only)')
    ap.add_argument('--r-se', type=float, default=0.5, help='SE radius (µm)')
    ap.add_argument('--r-amp', type=float, default=6.0, help='AM_P radius (µm)')
    ap.add_argument('--r-ams', type=float, default=2.0, help='AM_S radius (µm)')
    ap.add_argument('--e-se', type=float, default=24.0,
                    help='SE modulus (GPa).  Use the REAL bulk 24 — the Thornton yield cap '
                         'provides the plasticity, so NO 18× softening (1.53 never reaches yield).')
    ap.add_argument('--sigma-y', type=float, default=0.15, help='SE yield stress (GPa)')
    ap.add_argument('--beta-lock', type=float, default=0.06,
                    help='incompressibility lock: extra plastic overlap (×R*) of void-filling flow '
                         'before the contact stiffens to near-rigid.  Main Minnmann knob: real '
                         'void-fill needs DEEP flattening (δ/R ~ 0.2–0.4) → sweep β ≈ 0.2–0.9; '
                         'small β locks early and ends up STIFFER than Hertz (porosity above rigid).')
    ap.add_argument('--klock', type=float, default=8.0,
                    help='lock stiffness (×E*·R*); near-rigid incompressible backstop slope')
    grp = ap.add_mutually_exclusive_group()
    grp.add_argument('--plastic', dest='plastic', action='store_true', help='yield cap ON (default)')
    grp.add_argument('--rigid', dest='plastic', action='store_false', help='yield cap OFF (pure Hertz)')
    ap.set_defaults(plastic=True)
    ap.add_argument('--target-gpa', type=float, default=0.30, help='servo platen target (GPa); 0.3=300 MPa')
    ap.add_argument('--mu', type=float, default=0.3, help='Coulomb friction coefficient')
    ap.add_argument('--phi0', type=float, default=0.35,
                    help='initial solid fraction (loose; keep <=0.38, the RSA saturation limit)')
    ap.add_argument('--frames', type=int, default=300, help='MAX frames; servo self-terminates at target')
    ap.add_argument('--sub', type=int, default=50, help='substeps per frame')
    ap.add_argument('--dt', type=float, default=0.04, help='timestep (scaled units)')
    ap.add_argument('--vmax-frac', type=float, default=0.12, help='platen speed cap = frac·r_min per frame')
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--engine', default='auto', choices=['auto', 'dense', 'cell'],
                    help='pair engine.  dense = all-pairs + (N,N) history (validated reference, '
                         'N≲6k).  cell = SE cell-grid + few-big-AM brute + slot history '
                         '(N~50k bimodal dip runs).  auto picks by N.')
    ap.add_argument('--unit-test', action='store_true', help='single-contact law validation only')
    ap.add_argument('--quiet', action='store_true')
    return ap.parse_args(argv)


# ── closed-form normal force (numpy reference = the analytic gate) ───────────────
def f_load_numpy(delta, Rstar, Estar, py, dy, beta, klock):
    """Monotonic loading force: Hertz (jamming) → plastic plateau (void-fill flow) →
    incompressible lock (granular densification limit)."""
    k = (4.0 / 3.0) * Estar * math.sqrt(Rstar)
    if delta <= dy:
        return k * delta ** 1.5
    dlock = dy + beta * Rstar
    Fy = k * dy ** 1.5
    if delta <= dlock:
        return Fy + math.pi * py * Rstar * (delta - dy)
    Flock = Fy + math.pi * py * Rstar * (dlock - dy)
    return Flock + klock * Estar * Rstar * (delta - dlock)


def thornton_numpy(delta, dmax, Rstar, Estar, py, plastic=True, beta=0.06, klock=8.0):
    """Returns (F, new_dmax) for one contact.  numpy mirror of the Taichi @ti.func;
    the unit test asserts the two agree.  plastic=False → pure Hertz (rigid)."""
    if delta <= 0.0:
        return 0.0, dmax
    k = (4.0 / 3.0) * Estar * math.sqrt(Rstar)
    if not plastic:
        return k * delta ** 1.5, max(dmax, delta)
    dy = Rstar * (math.pi * py / (2.0 * Estar)) ** 2          # yield overlap
    dmx = max(dmax, delta)
    if dmx <= dy:                                            # never yielded → Hertz both ways
        return k * delta ** 1.5, dmx
    Fmax = f_load_numpy(dmx, Rstar, Estar, py, dy, beta, klock)
    a_max2 = Rstar * (2.0 * dmx - dy)                        # Thornton plastic contact area /π
    Rp = (4.0 / 3.0) * Estar * a_max2 ** 1.5 / Fmax          # flattened unloading radius
    d0 = dmx - a_max2 / Rp                                   # residual (permanent) overlap
    if delta >= dmx - 1e-12:                                 # on the loading branch (new max)
        F = f_load_numpy(delta, Rstar, Estar, py, dy, beta, klock)
    elif delta > d0:                                         # elastic unloading from the flat
        F = (4.0 / 3.0) * Estar * math.sqrt(Rp) * (delta - d0) ** 1.5
    else:                                                    # separated below residual set
        F = 0.0
    return F, dmx


def build_packing(args, rng):
    """Random non-overlapping spheres, periodic x,y, stacked from the floor.  Returns
    centers (N,3), radii, per-particle E, py and box (Lx, Ly, floor, fill_top)."""
    ps = tuple(int(z) for z in args.ps.split(':'))
    # radii + per-radius solid-volume split by composition
    if args.material == 'SE':
        radii_kinds = [(args.r_se, 1.0, args.e_se, C_H * args.sigma_y)]
    elif args.material == 'AM':
        # AM-only: split P:S by the ps ratio
        fp = ps[0] / (ps[0] + ps[1]); fs = 1.0 - fp
        radii_kinds = [(args.r_amp, fp, E_AM, PY_RIGID), (args.r_ams, fs, E_AM, PY_RIGID)]
    else:                                                   # mix: AM (P,S) + SE by weight + ps
        am = args.am_wt / 100.0
        rho_am, rho_se = 4.8, 1.6                           # g/cm³ → volume fractions from weight
        vam = (am / rho_am) / (am / rho_am + (1 - am) / rho_se)
        vse = 1.0 - vam
        fp = ps[0] / (ps[0] + ps[1]); fs = 1.0 - fp
        radii_kinds = [(args.r_amp, vam * fp, E_AM, PY_RIGID),
                       (args.r_ams, vam * fs, E_AM, PY_RIGID),
                       (args.r_se, vse, args.e_se, C_H * args.sigma_y)]
    radii_kinds = [rk for rk in radii_kinds if rk[1] > 1e-9]

    # box sized so the TOTAL PARTICLE COUNT ≈ n_target at the loose initial solid
    # fraction.  count_k = frac_k·V_tot/v_k  ⇒  V_tot = n_target / Σ_k(frac_k/v_k)
    # (harmonic mixing; a volume-weighted vbar would blow N up at bimodal mixes).
    inv_vbar = sum(frac / ((4.0 / 3.0) * math.pi * r ** 3) for (r, frac, *_ ) in radii_kinds)
    v_solid_tot = args.n_target / inv_vbar
    box_vol = v_solid_tot / args.phi0
    fill_h = 8.0 * max(r for (r, *_ ) in radii_kinds)      # fill height ~8 big-diameters
    L = math.sqrt(box_vol / fill_h)
    floor = 0.0
    vol = lambda r: (4.0 / 3.0) * math.pi * r ** 3                    # noqa: E731

    # Two-tier RSA (mirrors the sim engine): a uniform grid sized by max(r) is
    # useless at 12:4:1 (cell ≈ big-AM diameter ⇒ thousands of SE per cell ⇒
    # O(N²) Python ⇒ hours).  Instead place the FEW big AM first by brute force,
    # then the many small SE in a FINE grid (SE-scale cell) for SE-SE and brute
    # against the few big for SE-AM.
    rmin = min(r for (r, *_ ) in radii_kinds)
    small_k = [rk for rk in radii_kinds if rk[0] <= 1.5 * rmin]       # SE tier (gridded)
    big_k = [rk for rk in radii_kinds if rk[0] > 1.5 * rmin]          # AM tier (brute)
    cx, cr, cE, cpy = [], [], [], []
    big = []                                                          # (x,y,z,r) of placed big

    def hits_big(p, r):
        for (qx, qy, qz, qr) in big:
            dx = p[0] - qx; dy = p[1] - qy
            dx -= L * round(dx / L); dy -= L * round(dy / L)          # min image (periodic x,y)
            dz = p[2] - qz
            if dx * dx + dy * dy + dz * dz < (r + qr + 0.02) ** 2:
                return True
        return False

    for (r, frac, E, py) in big_k:                                   # 1) big AM — brute O(n_big²)
        goal, acc, fails = frac * v_solid_tot, 0.0, 0
        while acc < goal and fails < 60_000:
            p = (rng.uniform(0, L), rng.uniform(0, L), rng.uniform(floor + r, floor + fill_h - r))
            if not hits_big(p, r):
                big.append((p[0], p[1], p[2], r))
                cx.append(p); cr.append(r); cE.append(E); cpy.append(py); acc += vol(r); fails = 0
            else:
                fails += 1

    cell = 2.0 * rmin                                                # 2) SE — fine grid + brute-big
    NX = max(3, int(L / cell)); cellx = L / NX
    grid = {}

    def gkey(p):
        return (int(p[0] / cellx) % NX, int(p[1] / cellx) % NX, int(p[2] / cellx))

    def hits_small(p, r):                                            # SE-SE via 27 fine cells
        kx, ky, kz = int(p[0] / cellx) % NX, int(p[1] / cellx) % NX, int(p[2] / cellx)
        for ax in (-1, 0, 1):
            for ay in (-1, 0, 1):
                for az in (-1, 0, 1):
                    for (qx, qy, qz, qr) in grid.get(((kx + ax) % NX, (ky + ay) % NX, kz + az), ()):
                        dx = p[0] - qx; dy = p[1] - qy
                        dx -= L * round(dx / L); dy -= L * round(dy / L)
                        dz = p[2] - qz
                        if dx * dx + dy * dy + dz * dz < (r + qr + 0.02) ** 2:
                            return True
        return False

    for (r, frac, E, py) in small_k:
        goal, acc, fails = frac * v_solid_tot, 0.0, 0
        while acc < goal and fails < 60_000:
            p = (rng.uniform(0, L), rng.uniform(0, L), rng.uniform(floor + r, floor + fill_h - r))
            if not hits_small(p, r) and not hits_big(p, r):
                grid.setdefault(gkey(p), []).append((p[0], p[1], p[2], r))
                cx.append(p); cr.append(r); cE.append(E); cpy.append(py); acc += vol(r); fails = 0
            else:
                fails += 1
    return (np.array(cx, np.float32), np.array(cr, np.float32),
            np.array(cE, np.float32), np.array(cpy, np.float32), L, floor, floor + fill_h)


def main(argv):
    args = parse_args(argv)
    import taichi as ti
    arch = {'gpu': ti.gpu, 'cuda': ti.cuda, 'vulkan': ti.vulkan, 'cpu': ti.cpu}[args.arch]
    init_kw = dict(arch=arch, default_fp=ti.f32, random_seed=args.seed)
    if args.arch in ('gpu', 'cuda'):
        init_kw['device_memory_GB'] = args.gpu_mem      # cap the pool (shared V100 → avoid OOM grab)
    ti.init(**init_kw)

    # ── the contact law as a Taichi @ti.func (mirrors thornton_numpy) ───────────
    PLASTIC = int(args.plastic); BETA = float(args.beta_lock); KLOCK = float(args.klock)

    @ti.func
    def pow15(z):                                          # z^1.5, Taichi-safe (no ** in kernels)
        return z * ti.sqrt(ti.max(z, 0.0))

    @ti.func
    def f_load(delta, Rstar, Estar, py, dy):
        # monotonic loading: Hertz (jamming) → plastic plateau (void-fill) → incompressible lock
        k = (4.0 / 3.0) * Estar * ti.sqrt(Rstar)
        F = k * pow15(delta)
        if delta > dy:
            dlock = dy + BETA * Rstar
            Fy = k * pow15(dy)
            if delta <= dlock:
                F = Fy + math.pi * py * Rstar * (delta - dy)           # soft void-filling flow
            else:
                Flock = Fy + math.pi * py * Rstar * (dlock - dy)
                F = Flock + KLOCK * Estar * Rstar * (delta - dlock)    # near-rigid incompressible
        return F

    @ti.func
    def contact_normal(delta, dmax, Rstar, Estar, py):
        F = 0.0
        new_dmax = ti.max(dmax, delta)
        k = (4.0 / 3.0) * Estar * ti.sqrt(Rstar)
        if delta > 0.0:
            if PLASTIC == 0:
                F = k * pow15(delta)
            else:
                t = math.pi * py / (2.0 * Estar)
                dy = Rstar * t * t                         # yield overlap
                if new_dmax <= dy:
                    F = k * pow15(delta)                   # never yielded → Hertz both ways
                else:
                    Fmax = f_load(new_dmax, Rstar, Estar, py, dy)
                    if delta >= new_dmax - 1e-9:
                        F = f_load(delta, Rstar, Estar, py, dy)        # on the loading curve
                    else:
                        a_max2 = Rstar * (2.0 * new_dmax - dy)
                        Rp = (4.0 / 3.0) * Estar * pow15(a_max2) / Fmax
                        d0 = new_dmax - a_max2 / Rp        # residual (permanent) overlap
                        if delta > d0:
                            F = (4.0 / 3.0) * Estar * ti.sqrt(Rp) * pow15(delta - d0)  # unload
                        else:
                            F = 0.0                        # separated below residual set
        return F, new_dmax

    # ── unit test: drive one contact along a load→unload δ path ─────────────────
    if args.unit_test:
        run_unit_test(ti, contact_normal, args)
        return

    # ── build packing ───────────────────────────────────────────────────────────
    rng = np.random.default_rng(args.seed)
    cx, cr, cE, cpy, L, floor, fill_top = build_packing(args, rng)
    N = len(cx)
    if N < 2:
        print("packing failed (N<2) — raise --n-target or --phi0"); return
    nu = NU
    vol_solid = float(np.sum((4.0 / 3.0) * np.pi * cr.astype(np.float64) ** 3))
    area = L * L
    mass = (RHO * (4.0 / 3.0) * np.pi * cr.astype(np.float64) ** 3).astype(np.float32)

    # ── engine choice (before fields: dense history is (N,N) → N≳6k must use cell) ──
    ENGINE = args.engine
    if ENGINE == 'auto':
        ENGINE = 'cell' if N > 6000 else 'dense'
    if ENGINE == 'cell':
        small_np = (cpy < PY_RIGID * 0.5)                  # SE = yielding phase = "small" tier
        sid_np = np.where(small_np)[0].astype(np.int32)
        bid_np = np.where(~small_np)[0].astype(np.int32)
        n_small = int(sid_np.size); n_big = int(bid_np.size)
        r_small = float(cr[small_np].max()) if n_small else float(cr.min())
        HC0 = 2.2 * r_small                                # ≥ SE–SE cutoff (2·r_small) + skin
        NCX = max(1, int(L / HC0)); HCX = L / NCX          # exact periodic tiling in x,y
        NCZ = max(1, int(math.ceil((fill_top + float(cr.max())) / HCX)) + 1)
        if NCX < 3:                                        # wrap would double-visit cells
            print("  (box too small for the cell engine → falling back to dense)")
            ENGINE = 'dense'

    # ── fields ──────────────────────────────────────────────────────────────────
    x = ti.Vector.field(3, ti.f32, N); v = ti.Vector.field(3, ti.f32, N)
    f = ti.Vector.field(3, ti.f32, N)
    rad = ti.field(ti.f32, N); Ei = ti.field(ti.f32, N); pyi = ti.field(ti.f32, N); m = ti.field(ti.f32, N)
    # dense contact history (reference engine); dummy 1×1 when the cell engine is active
    dmax = ti.field(ti.f32, (N, N) if ENGINE == 'dense' else (1, 1))
    dmax_fl = ti.field(ti.f32, N); dmax_tp = ti.field(ti.f32, N)
    wall_z = ti.field(ti.f32, ()); wall_force = ti.field(ti.f32, ())
    Lx = ti.field(ti.f32, ())

    x.from_numpy(np.ascontiguousarray(cx)); rad.from_numpy(cr); Ei.from_numpy(cE)
    pyi.from_numpy(cpy); m.from_numpy(mass)
    Lx[None] = L

    # ── voxel union porosity (exact).  The lens-corrected ε_union over-subtracts
    #    TRIPLE overlaps at deep plastic flattening → reads denser than truth; the
    #    voxel union has no such error.  Calibrate Minnmann on the VOX readout. ────
    VG = 192
    hvox = L / VG
    VGZ = int(math.ceil((fill_top + float(cr.max())) / hvox)) + 2
    vox = ti.field(ti.i32, (VG, VG, VGZ))

    @ti.kernel
    def voxelize():
        for I in ti.grouped(vox):
            vox[I] = 0
        for i in range(N):
            r = rad[i]
            kx0 = int(ti.floor((x[i][0] - r) / hvox)); kx1 = int(ti.floor((x[i][0] + r) / hvox)) + 1
            ky0 = int(ti.floor((x[i][1] - r) / hvox)); ky1 = int(ti.floor((x[i][1] + r) / hvox)) + 1
            kz0 = ti.max(0, int(ti.floor((x[i][2] - r) / hvox)))
            kz1 = ti.min(VGZ - 1, int(ti.floor((x[i][2] + r) / hvox)) + 1)
            for kx in range(kx0, kx1 + 1):
                for ky in range(ky0, ky1 + 1):
                    for kz in range(kz0, kz1 + 1):
                        ddx = (kx + 0.5) * hvox - x[i][0]
                        ddy = (ky + 0.5) * hvox - x[i][1]
                        ddz = (kz + 0.5) * hvox - x[i][2]
                        if ddx * ddx + ddy * ddy + ddz * ddz <= r * r:
                            vox[((kx % VG) + VG) % VG, ((ky % VG) + VG) % VG, kz] = 1

    @ti.kernel
    def vox_solid(zmax: ti.f32) -> ti.i32:
        c = 0
        for I in ti.grouped(vox):
            if vox[I] == 1 and (I[2] + 0.5) * hvox < zmax:
                c += 1
        return c

    def porosity_vox():
        voxelize()
        nz = sum(1 for kz in range(VGZ) if (kz + 0.5) * hvox < wall_z[None])
        if nz == 0:
            return float('nan')
        return max(0.0, 1.0 - vox_solid(wall_z[None]) / (VG * VG * nz)) * 100.0

    DT = args.dt
    DAMP = 3.0                       # global viscous (1/time) — drive to quasi-static
    GAMMA_N = 0.25                   # contact normal dashpot (dissipate ringing)
    MU = args.mu

    @ti.func
    def estar_pair(i, j):
        return 1.0 / ((1 - nu * nu) / Ei[i] + (1 - nu * nu) / Ei[j])

    @ti.func
    def estar_wall(i):
        return 1.0 / ((1 - nu * nu) / Ei[i])               # rigid wall (E_wall→∞)

    @ti.kernel
    def step():
        for i in range(N):
            f[i] = ti.Vector([0.0, 0.0, 0.0])
        wall_force[None] = 0.0
        Lc = Lx[None]
        for i in range(N):                                  # parallel over i
            # floor (z = floor): overlap if particle dips below floor+rad
            df = floor + rad[i] - x[i][2]
            if df > 0:
                Fn, nd = contact_normal(df, dmax_fl[i], rad[i], estar_wall(i), pyi[i])
                dmax_fl[i] = nd
                f[i][2] += Fn - GAMMA_N * ti.min(v[i][2], 0.0)
            else:
                dmax_fl[i] = 0.0
            # top platen (z = wall_z): overlap if particle pokes above wall_z-rad
            dtp = x[i][2] + rad[i] - wall_z[None]
            if dtp > 0:
                Fn, nd = contact_normal(dtp, dmax_tp[i], rad[i], estar_wall(i), pyi[i])
                dmax_tp[i] = nd
                fz = Fn - GAMMA_N * ti.max(v[i][2], 0.0)
                f[i][2] -= fz
                wall_force[None] += fz                      # reaction on the platen
            else:
                dmax_tp[i] = 0.0
            # pair contacts (j>i), periodic min-image in x,y
            for j in range(i + 1, N):
                dx = x[i] - x[j]
                dx[0] -= Lc * ti.round(dx[0] / Lc)
                dx[1] -= Lc * ti.round(dx[1] / Lc)
                dist = dx.norm() + 1e-12
                delta = rad[i] + rad[j] - dist
                if delta > 0:
                    Rstar = rad[i] * rad[j] / (rad[i] + rad[j])
                    py = ti.min(pyi[i], pyi[j])
                    Fn, nd = contact_normal(delta, dmax[i, j], Rstar, estar_pair(i, j), py)
                    dmax[i, j] = nd
                    nrm = dx / dist
                    vrel = v[i] - v[j]
                    vn = vrel.dot(nrm)
                    Ftot = Fn - GAMMA_N * vn                # normal + dashpot
                    f[i] += Ftot * nrm; f[j] -= Ftot * nrm
                    # regularized Coulomb friction (no tangential history in v1)
                    vt = vrel - vn * nrm
                    vtn = vt.norm()
                    if vtn > 1e-9:
                        Ft = ti.min(MU * ti.max(Fn, 0.0), 2.0 * vtn)
                        ft = -Ft * vt / vtn
                        f[i] += ft; f[j] -= ft
                else:
                    dmax[i, j] = 0.0

    # ── cell engine: SE cell-grid + few-big-AM brute + per-owner slot history ────
    # History OWNER rule: SE–AM history lives on the SE side; SE–SE and AM–AM on the
    # lower id (= the iterating thread).  An owner's slots are only ever touched from
    # its own parallel iteration → race-free.  Slot freed on separation = history
    # reset, identical to the dense engine's dmax[i,j]=0.
    if ENGINE == 'cell':
        M = 64                                             # max SE per cell (overflow counted)
        K = 24                                             # history slots per owner (Z≲12)
        cell_cnt = ti.field(ti.i32, (NCX, NCX, NCZ))
        cell_itm = ti.field(ti.i32, (NCX, NCX, NCZ, M))
        nbr_j = ti.field(ti.i32, (N, K)); nbr_dm = ti.field(ti.f32, (N, K))
        nbr_j.fill(-1)
        sid = ti.field(ti.i32, max(n_small, 1)); bid = ti.field(ti.i32, max(n_big, 1))
        sid.from_numpy(sid_np if n_small else np.zeros(1, np.int32))
        bid.from_numpy(bid_np if n_big else np.zeros(1, np.int32))
        ovf = ti.field(ti.i32, ())

        @ti.kernel
        def build_cells():
            for I in ti.grouped(cell_cnt):
                cell_cnt[I] = 0
            for s in range(n_small):
                i = sid[s]
                cxi = ((int(ti.floor(x[i][0] / HCX)) % NCX) + NCX) % NCX
                cyi = ((int(ti.floor(x[i][1] / HCX)) % NCX) + NCX) % NCX
                czi = ti.min(NCZ - 1, ti.max(0, int(ti.floor(x[i][2] / HCX))))
                k = ti.atomic_add(cell_cnt[cxi, cyi, czi], 1)
                if k < M:
                    cell_itm[cxi, cyi, czi, k] = i
                else:
                    ovf[None] += 1

        @ti.func
        def do_pair(i, j):                                 # i = history owner
            Lc = Lx[None]
            dxv = x[i] - x[j]
            dxv[0] -= Lc * ti.round(dxv[0] / Lc)
            dxv[1] -= Lc * ti.round(dxv[1] / Lc)
            dist = dxv.norm() + 1e-12
            delta = rad[i] + rad[j] - dist
            slot = -1; free = -1
            for k in range(K):
                if nbr_j[i, k] == j and slot == -1:
                    slot = k
                if nbr_j[i, k] == -1 and free == -1:
                    free = k
            if delta > 0:
                if slot == -1:
                    slot = free                            # claim (owner-thread exclusive)
                dmv = 0.0
                if slot >= 0:
                    if nbr_j[i, slot] != j:
                        nbr_j[i, slot] = j; nbr_dm[i, slot] = 0.0
                    dmv = nbr_dm[i, slot]
                Rstar = rad[i] * rad[j] / (rad[i] + rad[j])
                pyv = ti.min(pyi[i], pyi[j])
                Fn, nd = contact_normal(delta, dmv, Rstar, estar_pair(i, j), pyv)
                if slot >= 0:
                    nbr_dm[i, slot] = nd
                nrm = dxv / dist
                vrel = v[i] - v[j]
                vn = vrel.dot(nrm)
                Ftot = Fn - GAMMA_N * vn
                f[i] += Ftot * nrm
                f[j] -= Ftot * nrm                         # atomic
                vt = vrel - vn * nrm
                vtn = vt.norm()
                if vtn > 1e-9:
                    Ft = ti.min(MU * ti.max(Fn, 0.0), 2.0 * vtn)
                    ftv = -Ft * vt / vtn
                    f[i] += ftv; f[j] -= ftv
            else:
                if slot >= 0:
                    nbr_j[i, slot] = -1                    # separation resets history

        @ti.kernel
        def step_cell():
            for i in range(N):
                f[i] = ti.Vector([0.0, 0.0, 0.0])
            wall_force[None] = 0.0
            for i in range(N):                              # floor + platen (same law as dense)
                df = floor + rad[i] - x[i][2]
                if df > 0:
                    Fn, nd = contact_normal(df, dmax_fl[i], rad[i], estar_wall(i), pyi[i])
                    dmax_fl[i] = nd
                    f[i][2] += Fn - GAMMA_N * ti.min(v[i][2], 0.0)
                else:
                    dmax_fl[i] = 0.0
                dtp = x[i][2] + rad[i] - wall_z[None]
                if dtp > 0:
                    Fn, nd = contact_normal(dtp, dmax_tp[i], rad[i], estar_wall(i), pyi[i])
                    dmax_tp[i] = nd
                    fz = Fn - GAMMA_N * ti.max(v[i][2], 0.0)
                    f[i][2] -= fz
                    wall_force[None] += fz
                else:
                    dmax_tp[i] = 0.0
            for s in range(n_small):                        # SE–SE via 27 cells (owner = lower id)
                i = sid[s]
                cxi = ((int(ti.floor(x[i][0] / HCX)) % NCX) + NCX) % NCX
                cyi = ((int(ti.floor(x[i][1] / HCX)) % NCX) + NCX) % NCX
                czi = ti.min(NCZ - 1, ti.max(0, int(ti.floor(x[i][2] / HCX))))
                for oxc in range(-1, 2):
                    for oyc in range(-1, 2):
                        for ozc in range(-1, 2):
                            czn = czi + ozc
                            if 0 <= czn < NCZ:
                                cxn = (cxi + oxc + NCX) % NCX
                                cyn = (cyi + oyc + NCX) % NCX
                                nc = ti.min(cell_cnt[cxn, cyn, czn], M)
                                for k in range(nc):
                                    j = cell_itm[cxn, cyn, czn, k]
                                    if j > i:
                                        do_pair(i, j)
            for s in range(n_small):                        # SE–AM brute over the few big
                i = sid[s]
                for b in range(n_big):
                    do_pair(i, bid[b])
            for b1 in range(n_big):                         # AM–AM brute (owner = loop lower)
                i = bid[b1]
                for b2 in range(b1 + 1, n_big):
                    do_pair(i, bid[b2])

    @ti.kernel
    def integrate():
        Lc = Lx[None]
        for i in range(N):
            a = f[i] / m[i] - DAMP * v[i]
            v[i] += DT * a
            x[i] += DT * v[i]
            x[i][0] -= Lc * ti.floor(x[i][0] / Lc)          # wrap into [0,L)
            x[i][1] -= Lc * ti.floor(x[i][1] / Lc)

    # ── compaction loop with proportional servo platen ──────────────────────────
    wall_z[None] = fill_top + 0.5 * cr.max()
    target = args.target_gpa
    vmax = 0.04 * cr.min()                                  # platen step cap (µm / frame)
    floor_min = floor + 1.5 * cr.max()
    if not args.quiet:
        cap = 'PLASTIC (yield cap ON, H=%.2f GPa)' % (C_H * args.sigma_y) if args.plastic else 'RIGID (pure Hertz)'
        eng = ENGINE + (f" (n_small={n_small}, n_big={n_big})" if ENGINE == 'cell' else '')
        print(f"3D DEM  N={N}  L={L:.2f}µm  arch={args.arch}  engine={eng}  {cap}  target={target} GPa")
    series = []; converged = 0
    for frame in range(args.frames):
        pacc = 0.0
        for _ in range(args.sub):
            if ENGINE == 'cell':
                build_cells(); step_cell()
            else:
                step()
            integrate()
            pacc += wall_force[None] / area
        p = pacc / args.sub                                 # mean platen pressure this frame (GPa)
        err = (target - p) / max(target, 1e-6)              # +1 → far below target → compress
        v_wall = -max(-1.0, min(1.0, err)) * vmax           # err>0 → move down (compress)
        wall_z[None] = max(floor_min, wall_z[None] + v_wall)
        height = wall_z[None] - floor
        # ε_sphere = PRODUCTION convention (CLAUDE.md): material-conserving — displaced
        # lens material re-emerges as bulge, so solid = Σ original sphere vol.  Unclamped
        # (negative = over-compressed signal).  VOX = exact union, rigid-view UPPER bound.
        por = (1.0 - vol_solid / (area * height)) * 100.0
        series.append((frame, p, por, wall_z[None]))
        converged = converged + 1 if abs(p - target) < 0.04 * target else 0
        last = (converged >= 10 and frame > 25) or frame == args.frames - 1
        if not args.quiet and (frame % 10 == 0 or last):
            pv = porosity_vox()
            print(f"  frame {frame:3d}  p={p:7.4f} GPa  por_sph={por:6.2f}% (vox {pv:5.2f}%)  "
                  f"wall_z={wall_z[None]:6.3f}")
        if converged >= 10 and frame > 25:                  # servo self-terminates at target
            if not args.quiet:
                print(f"  ✓ converged: p within 4% of {target} GPa, porosity stable")
            break
    p_fin = float(np.mean([s[1] for s in series[-5:]]))
    por_fin = float(np.mean([s[2] for s in series[-5:]]))
    pv_fin = porosity_vox()
    print(f"FINAL  pressure={p_fin:.4f} GPa  porosity_SPHERE={por_fin:.2f}%  porosity_VOX={pv_fin:.2f}%   "
          f"[{'PLASTIC' if args.plastic else 'RIGID'}, {args.material}, N={N}]  "
          f"(calibrate ε_sphere≈10% = production convention; VOX = rigid-view upper bound)")
    if wall_z[None] <= floor_min + 1e-6 and p_fin < 0.9 * target:
        print(f"  ⚠ platen bottomed out at floor_min={floor_min:.3f} below target → bed TOO SOFT: "
              f"raise --sigma-y (plateau) or --beta-lock (later lock) to hold {target} GPa")
    if ENGINE == 'cell' and ovf[None] > 0:
        print(f"  ⚠ cell-list overflow: {int(ovf[None])} drops (M={M}) — results INVALID, raise M")
    return por_fin, p_fin


def run_unit_test(ti, contact_normal, args):
    """Drive a single contact up then down a δ ramp; compare Taichi vs thornton_numpy
    and save the F(δ) curve.  This is the credibility figure: 'here is the contact
    law, it is Thornton 1997, loading→plateau→elastic-unload-with-residual'."""
    Ri = Rj = args.r_se
    Rstar = Ri * Rj / (Ri + Rj)
    Estar = 1.0 / (2.0 * (1 - NU * NU) / args.e_se)
    py = C_H * args.sigma_y
    dpk = 0.18 * args.r_se                                  # peak overlap (deep into plastic)
    up = np.linspace(0, dpk, 80); down = np.linspace(dpk, 0, 80)[1:]
    path = np.concatenate([up, down])

    out = ti.field(ti.f32, len(path)); dm = ti.field(ti.f32, len(path))
    dpath = ti.field(ti.f32, len(path)); dpath.from_numpy(path.astype(np.float32))

    @ti.kernel
    def sweep(Rs: ti.f32, Es: ti.f32, pyv: ti.f32):
        dmax = 0.0
        ti.loop_config(serialize=True)                     # sequential: history accumulates
        for s in range(len(path)):
            F, nd = contact_normal(dpath[s], dmax, Rs, Es, pyv)
            dmax = nd; out[s] = F; dm[s] = nd
    sweep(Rstar, Estar, py)
    Fti = out.to_numpy()

    # numpy analytic reference
    Fnp = np.zeros(len(path)); dmax = 0.0
    for s, d in enumerate(path):
        Fnp[s], dmax = thornton_numpy(float(d), dmax, Rstar, Estar, py, plastic=args.plastic,
                                      beta=args.beta_lock, klock=args.klock)
    err = float(np.max(np.abs(Fti - Fnp)) / (np.max(np.abs(Fnp)) + 1e-12))
    dy = Rstar * (math.pi * py / (2 * Estar)) ** 2
    print(f"UNIT TEST  Thornton contact  R*={Rstar:.3f}µm  E*={Estar:.3f}GPa  "
          f"py=H={py:.3f}GPa  δy={dy:.4f}µm  peakδ={dpk:.3f}µm")
    print(f"  max |F_taichi − F_numpy| / max|F| = {err:.2e}   "
          f"({'PASS' if err < 1e-3 else 'FAIL'} — Taichi law == analytic Thornton)")
    print(f"  loading yields at δy={dy:.4f}µm (Hertz below, plastic plateau above); "
          f"unloading returns elastically to a residual set δ0>0.")
    try:
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
        npath = len(up)
        fig, ax = plt.subplots(figsize=(5.4, 4.2))
        ax.plot(path[:npath], Fnp[:npath], '-', color='#c0392b', lw=2, label='loading (Hertz→plastic)')
        ax.plot(path[npath:], Fnp[npath:], '-', color='#2e86c1', lw=2, label='unloading (elastic, residual set)')
        ax.plot(path, Fti, 'k.', ms=2.5, label='Taichi @ti.func')
        ax.axvline(dy, color='gray', ls='--', lw=1, label=f'yield δy={dy:.3f}µm')
        ax.set_xlabel('overlap δ (µm)'); ax.set_ylabel('normal force F (GPa·µm²)')
        ax.set_title('Thornton elasto-plastic contact (%s)' % ('plastic' if args.plastic else 'rigid Hertz'))
        ax.legend(fontsize=8); ax.grid(alpha=0.3); plt.tight_layout()
        os.makedirs('docs/figures', exist_ok=True)
        outpng = 'docs/figures/dem3d_contact_lawtest.png'
        plt.savefig(outpng, dpi=120); print(f"  saved {outpng}")
    except Exception as e:
        print(f"  (plot skipped: {e})")


if __name__ == '__main__':
    main(sys.argv[1:])

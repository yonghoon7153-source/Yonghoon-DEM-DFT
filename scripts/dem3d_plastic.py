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
    grp = ap.add_mutually_exclusive_group()
    grp.add_argument('--plastic', dest='plastic', action='store_true', help='yield cap ON (default)')
    grp.add_argument('--rigid', dest='plastic', action='store_false', help='yield cap OFF (pure Hertz)')
    ap.set_defaults(plastic=True)
    ap.add_argument('--target-gpa', type=float, default=0.30, help='servo platen target (GPa); 0.3=300 MPa')
    ap.add_argument('--mu', type=float, default=0.3, help='Coulomb friction coefficient')
    ap.add_argument('--phi0', type=float, default=0.45, help='initial solid fraction (loose)')
    ap.add_argument('--frames', type=int, default=300, help='MAX frames; servo self-terminates at target')
    ap.add_argument('--sub', type=int, default=50, help='substeps per frame')
    ap.add_argument('--dt', type=float, default=0.04, help='timestep (scaled units)')
    ap.add_argument('--vmax-frac', type=float, default=0.12, help='platen speed cap = frac·r_min per frame')
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--unit-test', action='store_true', help='single-contact law validation only')
    ap.add_argument('--quiet', action='store_true')
    return ap.parse_args(argv)


# ── closed-form Thornton normal force (numpy reference = the analytic gate) ──────
def thornton_numpy(delta, dmax, Rstar, Estar, py, plastic=True):
    """Returns (F, new_dmax) for one contact.  numpy mirror of the Taichi @ti.func;
    the unit test asserts the two agree.  plastic=False → pure Hertz (rigid)."""
    if delta <= 0.0:
        return 0.0, dmax
    k = (4.0 / 3.0) * Estar * math.sqrt(Rstar)
    if not plastic:
        return k * delta ** 1.5, max(dmax, delta)
    dy = Rstar * (math.pi * py / (2.0 * Estar)) ** 2          # yield overlap
    Fy = k * dy ** 1.5
    dmx = max(dmax, delta)
    if dmx <= dy:                                            # never yielded → Hertz both ways
        return k * delta ** 1.5, dmx
    # plastic set: peak force + flattened-contact unloading radius + residual overlap
    Fmax = Fy + math.pi * py * Rstar * (dmx - dy)
    a_max2 = Rstar * (2.0 * dmx - dy)                        # Thornton plastic contact area /π
    Rp = (4.0 / 3.0) * Estar * a_max2 ** 1.5 / Fmax          # Rp = (4/3)E* a_max³ / Fmax
    d0 = dmx - a_max2 / Rp                                   # residual (permanent) overlap
    if delta >= dmx - 1e-12:                                 # on the loading branch (new max)
        F = Fy + math.pi * py * Rstar * (delta - dy)
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

    # box sized so the target particle count fits at the loose initial solid fraction
    vbar = sum(frac * (4.0 / 3.0) * math.pi * r ** 3 for (r, frac, *_ ) in radii_kinds)
    v_solid_tot = args.n_target * vbar
    box_vol = v_solid_tot / args.phi0
    fill_h = 8.0 * max(r for (r, *_ ) in radii_kinds)      # fill height ~8 big-diameters
    L = math.sqrt(box_vol / fill_h)
    floor = 0.0

    cx, cr, cE, cpy = [], [], [], []
    cell = max(r for (r, *_ ) in radii_kinds) * 2.05
    # bin by a coarse grid for fast overlap rejection (periodic x,y)
    grid = {}

    def key(p):
        return (int(p[0] // cell), int(p[1] // cell), int(p[2] // cell))

    def fits(p, r):
        gi = key(p)
        for a in (-1, 0, 1):
            for b in (-1, 0, 1):
                for c in (-1, 0, 1):
                    for (q, qr) in grid.get((gi[0] + a, gi[1] + b, gi[2] + c), ()):  # noqa
                        dx = p[0] - q[0]; dy = p[1] - q[1]
                        dx -= L * round(dx / L); dy -= L * round(dy / L)             # min image
                        dz = p[2] - q[2]
                        if dx * dx + dy * dy + dz * dz < (r + qr + 0.02) ** 2:
                            return False
        return True

    for (r, frac, E, py) in radii_kinds:
        goal = frac * v_solid_tot
        acc, tries = 0.0, 0
        while acc < goal and tries < 4_000_000:
            tries += 1
            p = (rng.uniform(0, L), rng.uniform(0, L), rng.uniform(floor + r, floor + fill_h - r))
            if fits(p, r):
                cx.append(p); cr.append(r); cE.append(E); cpy.append(py)
                grid.setdefault(key(p), []).append((p, r))
                acc += (4.0 / 3.0) * math.pi * r ** 3
    return (np.array(cx, np.float32), np.array(cr, np.float32),
            np.array(cE, np.float32), np.array(cpy, np.float32), L, floor, floor + fill_h)


def main(argv):
    args = parse_args(argv)
    import taichi as ti
    arch = {'gpu': ti.gpu, 'cuda': ti.cuda, 'vulkan': ti.vulkan, 'cpu': ti.cpu}[args.arch]
    ti.init(arch=arch, default_fp=ti.f32, random_seed=args.seed)

    # ── the contact law as a Taichi @ti.func (mirrors thornton_numpy) ───────────
    PLASTIC = int(args.plastic)

    @ti.func
    def pow15(z):                                          # z^1.5, Taichi-safe (no ** in kernels)
        return z * ti.sqrt(ti.max(z, 0.0))

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
                Fy = k * pow15(dy)
                if new_dmax <= dy:
                    F = k * pow15(delta)                   # never yielded → Hertz both ways
                else:
                    Fmax = Fy + math.pi * py * Rstar * (new_dmax - dy)
                    a_max2 = Rstar * (2.0 * new_dmax - dy)
                    Rp = (4.0 / 3.0) * Estar * pow15(a_max2) / Fmax
                    d0 = new_dmax - a_max2 / Rp            # residual (permanent) overlap
                    if delta >= new_dmax - 1e-9:
                        F = Fy + math.pi * py * Rstar * (delta - dy)   # loading plateau
                    elif delta > d0:
                        F = (4.0 / 3.0) * Estar * ti.sqrt(Rp) * pow15(delta - d0)  # elastic unload
                    else:
                        F = 0.0                            # separated below residual set
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

    # ── fields ──────────────────────────────────────────────────────────────────
    x = ti.Vector.field(3, ti.f32, N); v = ti.Vector.field(3, ti.f32, N)
    f = ti.Vector.field(3, ti.f32, N)
    rad = ti.field(ti.f32, N); Ei = ti.field(ti.f32, N); pyi = ti.field(ti.f32, N); m = ti.field(ti.f32, N)
    dmax = ti.field(ti.f32, (N, N))                      # contact history (dense; v2: cell-list slots)
    dmax_fl = ti.field(ti.f32, N); dmax_tp = ti.field(ti.f32, N)
    wall_z = ti.field(ti.f32, ()); wall_force = ti.field(ti.f32, ())
    Lx = ti.field(ti.f32, ())

    x.from_numpy(np.ascontiguousarray(cx)); rad.from_numpy(cr); Ei.from_numpy(cE)
    pyi.from_numpy(cpy); m.from_numpy(mass)
    Lx[None] = L

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
        print(f"3D DEM  N={N}  L={L:.2f}µm  arch={args.arch}  {cap}  target={target} GPa")
    series = []; converged = 0
    for frame in range(args.frames):
        pacc = 0.0
        for _ in range(args.sub):
            step(); integrate()
            pacc += wall_force[None] / area
        p = pacc / args.sub                                 # mean platen pressure this frame (GPa)
        err = (target - p) / max(target, 1e-6)              # +1 → far below target → compress
        v_wall = -max(-1.0, min(1.0, err)) * vmax           # err>0 → move down (compress)
        wall_z[None] = max(floor_min, wall_z[None] + v_wall)
        height = wall_z[None] - floor
        por = max(0.0, 1.0 - vol_solid / (area * height)) * 100.0
        series.append((frame, p, por, wall_z[None]))
        converged = converged + 1 if abs(p - target) < 0.04 * target else 0
        last = (converged >= 10 and frame > 25) or frame == args.frames - 1
        if not args.quiet and (frame % 10 == 0 or last):
            print(f"  frame {frame:3d}  p={p:7.4f} GPa  porosity={por:6.2f}%  wall_z={wall_z[None]:6.3f}")
        if converged >= 10 and frame > 25:                  # servo self-terminates at target
            if not args.quiet:
                print(f"  ✓ converged: p within 4% of {target} GPa, porosity stable")
            break
    p_fin = float(np.mean([s[1] for s in series[-5:]]))
    por_fin = float(np.mean([s[2] for s in series[-5:]]))
    print(f"FINAL  pressure={p_fin:.4f} GPa  porosity={por_fin:.2f}%   "
          f"[{'PLASTIC' if args.plastic else 'RIGID'}, {args.material}, N={N}]")
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
        Fnp[s], dmax = thornton_numpy(float(d), dmax, Rstar, Estar, py, plastic=args.plastic)
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

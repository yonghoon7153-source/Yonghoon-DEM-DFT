#!/usr/bin/env python3
"""2D MPM RIGID-jamming porosity vs AM%  —  RESOLUTION-INVARIANT dip readout.

PURPOSE (CLAUDE.md frame [3] + user's goal 2026-06-07):
  "절대값이 안맞아도 괜찮아 — 트랜드 확인하는데 환경(해상도)이 변수가 되면
   안된다."  The soft-plastic MPM read porosity at a COMMON PRESSURE, and the
  MPM pressure read-out is resolution-biased (320 vs 512 differ ~55-72% at the
  SAME porosity) -> the dip moved with grid size.  THIS script removes that
  confound two ways:

  (1) RIGID particles (E=24 GPa, no plastic flow).  Frame [3] says the dip is a
      GEOMETRIC packing effect; rigid grains make the jamming transition SHARP,
      so the porosity AT jamming is set by GEOMETRY (when grains touch), not by
      the pressure amplitude.  Plasticity is what *erased/confounded* the dip.

  (2) Readout = JAMMING KNEE porosity, NOT common pressure.  Because P(porosity)
      is near-vertical at a rigid jamming onset, the knee POROSITY is invariant
      to the (resolution-scaled) pressure amplitude.  We read porosity where the
      run's pressure first crosses a small FRACTION of its own deep-compression
      pressure (self-normalised -> the resolution amplitude factor cancels).

VALIDATION TARGET (resolution invariance):
  Run at n_grid = 320 AND 512.  porosity-vs-AM% must OVERLAP.  If it does, the
  trend is real (not numerical).  Compare to the grid-free geometric reference
  scripts/packing_dip_model.py (de Larrard, self-validated) which predicts a
  Furnas dip near AM ~85-90 wt% for this 12:4:1 / 7:3 system.

  NOTE the SIGN: rigid/geometric packing gives porosity DECREASING toward AM-rich
  (SE fills AM voids) with a dip ~85-90%, the OPPOSITE of the soft-plastic sweep
  (where plastic SE flows and fills voids so SE-rich is densest).  That contrast
  is frame [3]'s "plastic flow partially erases the packing dip" — both are real,
  they answer different questions (MPM-soft = mechanics, this = geometry).

Run (on the uma GPU box):
  python3 scripts/mpm2d_jamming.py --n-grid 320 --out jam_320.csv
  python3 scripts/mpm2d_jamming.py --n-grid 512 --out jam_512.csv
  python3 scripts/mpm2d_jamming.py --compare jam_320.csv jam_512.csv
Optional:  --seeds 3   --yield-se 1e4 (rigid, default)  |  0.3 (frame's σ_y)
"""
import argparse
import numpy as np

# ----------------------------------------------------------- fixed geometry --
# real 12:4:1 size ratio (CLAUDE.md frame); densities from mpm2d_composition.py
RHO_AM, RHO_SE = 4800.0, 2000.0
R_AMP, R_AMS, R_SE = 0.072, 0.024, 0.006      # 12 : 4 : 1
INIT_SOLID = 0.50
NU = 0.30
FLOOR = 0.08; SW_L, SW_R = 0.16, 0.84; WIDTH = SW_R - SW_L
WALL0 = 0.64; WALL_MIN = 0.20; WALL_V = 0.18  # slow wall -> clean P(porosity) knee

DT0, NREF, SUB0 = 8.0e-5, 320, 80             # dt ∝ dx ;  sub ∝ 1/dx (T/frame const)
NFRAME = 260
POR_FLOOR = 0.05                              # stop once clearly over-compressed
PS = (7, 3)                                   # AM_P : AM_S by weight


def lame(E):
    return E / (2 * (1 + NU)), E * NU / ((1 + NU) * (1 - 2 * NU))


MU_SE, LA_SE = lame(24.0)      # SE: REAL 24 GPa (frame rigid sweep), NO softening
MU_AM, LA_AM = lame(140.0)     # AM: rigid NCM
YIELD_AM = 1.0e4               # AM never yields


# globals populated by init_sim(n_grid) -------------------------------------
ti = None
n_grid = dx = inv_dx = dt = sub = p_vol = p_mass = None
x = v = C = F = mu_p = la_p = yld_p = press = grid_v = grid_m = wall_y = N = None
MAXP = 700000


def init_sim(ng):
    """set resolution-dependent globals + allocate taichi fields (call once)."""
    global ti, n_grid, dx, inv_dx, dt, sub, p_vol, p_mass
    global x, v, C, F, mu_p, la_p, yld_p, press, grid_v, grid_m, wall_y, N
    import taichi as _ti
    ti = _ti
    ti.init(arch=ti.gpu, default_fp=ti.f32, random_seed=2)
    n_grid = ng; dx = 1.0 / ng; inv_dx = float(ng)
    dt = DT0 * NREF / ng                       # CFL: dt ∝ dx
    sub = max(1, int(round(SUB0 * ng / NREF))) # keep sub*dt (phys time/frame) const
    p_vol = (dx * 0.5) ** 2; p_mass = p_vol * 1.0
    x = ti.Vector.field(2, ti.f32, MAXP); v = ti.Vector.field(2, ti.f32, MAXP)
    C = ti.Matrix.field(2, 2, ti.f32, MAXP); F = ti.Matrix.field(2, 2, ti.f32, MAXP)
    mu_p = ti.field(ti.f32, MAXP); la_p = ti.field(ti.f32, MAXP)
    yld_p = ti.field(ti.f32, MAXP); press = ti.field(ti.f32, MAXP)
    grid_v = ti.Vector.field(2, ti.f32, (ng, ng)); grid_m = ti.field(ti.f32, (ng, ng))
    wall_y = ti.field(ti.f32, ()); N = ti.field(ti.i32, ())
    _build_kernels()


# kernels are built after fields exist (closure over globals) ----------------
load = substep = None


def _build_kernels():
    global load, substep

    @ti.kernel
    def _load(xy: ti.types.ndarray(), mus: ti.types.ndarray(),
              las: ti.types.ndarray(), ylds: ti.types.ndarray(), n: ti.i32):
        N[None] = n
        for p in range(n):
            x[p] = ti.Vector([xy[p, 0], xy[p, 1]]); v[p] = ti.Vector([0.0, 0.0])
            C[p] = ti.Matrix.zero(ti.f32, 2, 2); F[p] = ti.Matrix.identity(ti.f32, 2)
            mu_p[p] = mus[p]; la_p[p] = las[p]; yld_p[p] = ylds[p]

    @ti.kernel
    def _substep():
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

    load, substep = _load, _substep


# ----------------------------------------------------------- build geometry --
def area_fracs(am_wt):
    w = am_wt / 100.0
    if w <= 0:
        vam = 0.0
    elif w >= 1:
        vam = 1.0
    else:
        a = w / RHO_AM; b = (1 - w) / RHO_SE; vam = a / (a + b)
    p, s = PS; fp, fs = p / (p + s), s / (p + s)
    return fp * vam, fs * vam, 1.0 - vam


def build(am_wt, rng, yield_se):
    fAP, fAS, fSE = area_fracs(am_wt)
    fill_h = WALL0 - 0.02
    box_area = WIDTH * (fill_h - FLOOR)
    target = INIT_SOLID * box_area
    placed = []
    plan = [(R_AMP, fAP, MU_AM, LA_AM, YIELD_AM),
            (R_AMS, fAS, MU_AM, LA_AM, YIELD_AM),
            (R_SE,  fSE, MU_SE, LA_SE, yield_se)]
    for (r, frac, mu, la, yld) in plan:
        if frac <= 0:
            continue
        a_goal = frac * target; a_acc = 0.0; tries = 0
        while a_acc < a_goal and tries < 200000:
            tries += 1
            cx = rng.uniform(SW_L + r, SW_R - r)
            cy = rng.uniform(FLOOR + r, fill_h - r)
            ok = True
            for (px, py, pr, *_) in placed:
                if (cx - px) ** 2 + (cy - py) ** 2 < (r + pr + 0.2 * R_SE) ** 2:
                    ok = False; break
            if ok:
                placed.append((cx, cy, r, mu, la, yld)); a_acc += np.pi * r * r
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


# ------------------------------------------------- one compression -> curve --
def compress_curve(xy, mus, las, ylds, solid_area):
    n = len(xy)
    load(xy, mus, las, ylds, n)
    wall_y[None] = WALL0
    por_s, p_s = [], []
    for frame in range(NFRAME):
        for _ in range(sub):
            substep()
        wall_y[None] = max(WALL0 - WALL_V * (frame + 1) * sub * dt, WALL_MIN)
        top = wall_y[None]
        por = max(0.0, 1.0 - solid_area / (WIDTH * (top - FLOOR)))
        pr = float(np.mean(press.to_numpy()[:n]))
        por_s.append(por); p_s.append(pr)
        if por < POR_FLOOR:
            break
    return np.array(por_s), np.array(p_s), n


def jam_porosity(por, p, fracs=(0.02, 0.05, 0.10)):
    """RESOLUTION-INVARIANT jamming porosity: porosity where P first reaches a
    small FRACTION of the run's deep-compression pressure (self-normalised so
    the resolution amplitude factor cancels) + the steepest-knee porosity."""
    p = np.maximum(p, 0.0)
    p_ref = float(np.max(p[-5:])) if len(p) >= 5 else float(np.max(p))
    out = {}
    order = np.argsort(por)[::-1]              # loose -> compressed (por descending)
    pp, qq = por[order], p[order]
    for f in fracs:
        thr = f * p_ref
        idx = np.where(qq >= thr)[0]
        out[f] = float(pp[idx[0]]) if len(idx) else float(pp[-1])
    # steepest knee in P vs porosity (geometric, amplitude-independent location)
    if len(pp) > 4:
        dP = np.gradient(qq, -pp)              # dP/d(porosity-decrease)
        out['knee'] = float(pp[int(np.argmax(dP))])
    else:
        out['knee'] = out[fracs[1]]
    return out


# --------------------------------------------------------------- sweep / IO --
def sweep(ng, seeds, yield_se, out_csv):
    init_sim(ng)
    comps = [0, 10, 20, 30, 40, 50, 60, 70, 80, 85, 90, 95, 100]
    rows = []
    for am in comps:
        accum = {f: [] for f in (0.02, 0.05, 0.10, 'knee')}
        npts = 0
        for sd in range(seeds):
            rng = np.random.default_rng(100 + sd)
            xy, mus, las, ylds = build(am, rng, yield_se)
            solid_area = len(xy) * p_vol
            por, p, n = compress_curve(xy, mus, las, ylds, solid_area)
            jp = jam_porosity(por, p)
            for k in accum:
                accum[k].append(jp[k] * 100.0)
            npts = n
        mean = {k: float(np.mean(v)) for k, v in accum.items()}
        std = {k: float(np.std(v)) for k, v in accum.items()}
        rows.append((am, mean, std, npts))
        print(f"  AM {am:3d}wt%  jam ε(2%/5%/10%/knee)= "
              f"{mean[0.02]:5.1f}/{mean[0.05]:5.1f}/{mean[0.10]:5.1f}/{mean['knee']:5.1f}% "
              f"(±{std[0.05]:.1f})  pts={npts}")
    with open(out_csv, 'w') as fh:
        fh.write("AM_wt%,eps_f02,eps_f05,eps_f10,eps_knee,std_f05,n_pts\n")
        for am, m, s, npts in rows:
            fh.write(f"{am},{m[0.02]:.3f},{m[0.05]:.3f},{m[0.10]:.3f},"
                     f"{m['knee']:.3f},{s[0.05]:.3f},{npts}\n")
    print(f"\n  saved {out_csv}  (n_grid={ng}, dt={dt:.2e}, sub={sub}, seeds={seeds})")


def compare(csv_a, csv_b):
    import csv
    def load_csv(path):
        with open(path) as fh:
            r = list(csv.DictReader(fh))
        am = np.array([float(x['AM_wt%']) for x in r])
        eps = np.array([float(x['eps_f05']) for x in r])
        return am, eps
    am_a, ea = load_csv(csv_a)
    am_b, eb = load_csv(csv_b)
    # geometric reference (de Larrard), if available
    geo = None
    try:
        import csv as _c
        with open('docs/data/packing_dip_model.csv') as fh:
            gr = list(_c.DictReader(fh))
        gam = np.array([float(x['AM_wt%']) for x in gr])
        gep = np.array([float(x['poros_beta0.84']) for x in gr])
        geo = (gam, gep)
    except Exception:
        pass
    print("\n  AM%   eps_A(320)  eps_B(512)   |Δ|     geom(de Larrard)")
    for i, a in enumerate(am_a):
        j = int(np.argmin(np.abs(am_b - a)))
        g = float(np.interp(a, geo[0], geo[1])) if geo else float('nan')
        print(f"  {a:4.0f}   {ea[i]:8.2f}   {eb[j]:8.2f}   {abs(ea[i]-eb[j]):5.2f}   {g:8.2f}")
    rmse = float(np.sqrt(np.mean((ea - np.interp(am_a, am_b, eb)) ** 2)))
    print(f"\n  320<->512 RMSE = {rmse:.2f} %p  "
          f"(small => trend is RESOLUTION-INVARIANT; that is the goal)")
    try:
        import matplotlib; matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import os
        fig, ax = plt.subplots(figsize=(7.6, 5.2))
        ax.plot(am_a, ea, '-o', color='#c0392b', lw=2, ms=6, label='MPM rigid jam, n_grid=320')
        ax.plot(am_b, eb, '-s', color='#2980b9', lw=2, ms=6, label='MPM rigid jam, n_grid=512')
        if geo:
            ax.plot(geo[0], geo[1], '--', color='#2e8b57', lw=2,
                    label='grid-free geometric (de Larrard β=0.84)')
        ax.set_xlabel('AM weight fraction (%)'); ax.set_ylabel('jamming porosity (%)')
        ax.set_title('RIGID-jamming dip — resolution invariance check\n'
                     '320 vs 512 should OVERLAP (RMSE in title)', fontsize=10)
        ax.legend(fontsize=8); ax.grid(alpha=0.3)
        plt.tight_layout(); os.makedirs('docs/figures', exist_ok=True)
        plt.savefig('docs/figures/mpm2d_jamming_resolution.png', dpi=130)
        print("  saved docs/figures/mpm2d_jamming_resolution.png")
    except Exception as e:
        print(f"  (plot skipped: {e})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n-grid', type=int, default=320)
    ap.add_argument('--seeds', type=int, default=3)
    ap.add_argument('--yield-se', type=float, default=1.0e4,
                    help='1e4 = rigid (pure geometry, default); 0.3 = frame σ_y')
    ap.add_argument('--out', type=str, default=None)
    ap.add_argument('--compare', nargs=2, metavar=('CSV_A', 'CSV_B'), default=None)
    a = ap.parse_args()
    if a.compare:
        compare(*a.compare); return
    out = a.out or f"jam_{a.n_grid}.csv"
    print(f"RIGID-jamming sweep  n_grid={a.n_grid}  seeds={a.seeds}  "
          f"yield_se={a.yield_se:g} (SE {'RIGID' if a.yield_se > 100 else 'σ_y='+str(a.yield_se)})")
    sweep(a.n_grid, a.seeds, a.yield_se, out)


if __name__ == '__main__':
    main()

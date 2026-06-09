#!/usr/bin/env python3
"""DEM ↔ MPM 1:1 porosity cross-validation at 300 MPa (frame [4]).

For every DEM design point in docs/data/dem_design_points.csv, build the SAME
geometry (AM_P:AM_S:SE size ratios) and composition (phi_am, phi_se, P:S) in the
champion MPM (E_SE=1.53/σ_y=0.15 plastic + work-hardening, AM rigid), compress a
servo wall to the SAME pressure (300 MPa via mean particle pressure), and read
MPM porosity.  Output: per-case DEM vs MPM porosity → parity check.

SE radius is fixed at R_SE=0.006 (resolution-consistent ~2-3 cells at 320); AM
radii scale by the case's measured size ratios (r_AM/r_SE), so each case keeps
its own bimodal geometry.  Composition taken directly from the DEM phi fractions.

Run (uma GPU):
  python3 scripts/mpm_dem_match.py [--n-grid 320] [--seeds 2] [--real-only]
                                   [--max-n 12] [--p-read 0.30]
  python3 scripts/mpm_dem_match.py --plot      # parity plot from the CSV (matplotlib)
Out: docs/data/mpm_dem_match.csv  (+ docs/figures/mpm_dem_match_parity.png with --plot)
"""
import argparse
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DP = os.path.join(HERE, '..', 'docs', 'data', 'dem_design_points.csv')
OUT = os.path.join(HERE, '..', 'docs', 'data', 'mpm_dem_match.csv')

# ---- fixed MPM material / geometry (champion) -----------------------------
R_SE_MPM = 0.006                      # fixed smallest radius (sets resolution)
INIT_SOLID = 0.50
FLOOR = 0.08; SW_L, SW_R = 0.08, 0.92; WIDTH = SW_R - SW_L
WALL0 = 0.66; WALL_MIN = 0.05; WALL_V = 0.18
P_STOP = 0.70


def _is_particulate(nm):
    n = nm.lower()
    return ('particulate' in n) or n.startswith('input_s_') or n == 'input_s'


def load_design(names=None, real_only=False, particulate=False, max_n=None):
    with open(DP) as fh:
        rows = list(csv.DictReader(fh))
    out = []
    for r in rows:
        nm = r['name']
        if real_only and 'real' not in nm:
            continue
        if particulate and not _is_particulate(nm):
            continue
        if names and nm not in names:
            continue
        out.append(dict(
            name=nm,
            ratio_P=float(r['ratio_P']), ratio_S=float(r['ratio_S']),
            phi_am=float(r['phi_am']), phi_se=float(r['phi_se']),
            PS=r['PS'], dem=float(r['dem_porosity']),
            r_SE=float(r['r_SE']), AM_wt=float(r['AM_wt'])))
    if max_n:
        out = out[:max_n]
    return out


def run_match(args):
    import numpy as np
    import taichi as ti
    ng = args.n_grid
    try:
        ti.init(arch=ti.gpu, default_fp=ti.f32, random_seed=7); print('  [taichi] GPU')
    except Exception as e:
        print(f'  [taichi] GPU failed ({e}); CPU'); ti.init(arch=ti.cpu, default_fp=ti.f32, random_seed=7)
    dx = 1.0 / ng; inv_dx = float(ng); dt = 8.0e-5 * 320.0 / ng; p_vol = (dx * 0.5) ** 2
    def lame(E, nu): return E / (2 * (1 + nu)), E * nu / ((1 + nu) * (1 - 2 * nu))
    MU_SE, LA_SE = lame(1.53, 0.30); MU_AM, LA_AM = lame(140.0, 0.25)
    YIELD_SE = 0.15; YIELD_AM = 1.0e4; HARD_SE = 10.0; RHO_AM, RHO_SE = 4.8, 2.0
    MAXP = 2_500_000
    x = ti.Vector.field(2, ti.f32, MAXP); v = ti.Vector.field(2, ti.f32, MAXP)
    C = ti.Matrix.field(2, 2, ti.f32, MAXP); F = ti.Matrix.field(2, 2, ti.f32, MAXP)
    mu_p = ti.field(ti.f32, MAXP); la_p = ti.field(ti.f32, MAXP); yld_p = ti.field(ti.f32, MAXP)
    m_p = ti.field(ti.f32, MAXP); prs = ti.field(ti.f32, MAXP); epl = ti.field(ti.f32, MAXP)
    grid_v = ti.Vector.field(2, ti.f32, (ng, ng)); grid_m = ti.field(ti.f32, (ng, ng))
    wall_y = ti.field(ti.f32, ()); N = ti.field(ti.i32, ())

    @ti.kernel
    def load(xy: ti.types.ndarray(), mu: ti.types.ndarray(), la: ti.types.ndarray(),
             yl: ti.types.ndarray(), ms: ti.types.ndarray(), n: ti.i32):
        N[None] = n
        for p in range(n):
            x[p] = ti.Vector([xy[p, 0], xy[p, 1]]); v[p] = ti.Vector([0.0, 0.0])
            C[p] = ti.Matrix.zero(ti.f32, 2, 2); F[p] = ti.Matrix.identity(ti.f32, 2)
            mu_p[p] = mu[p]; la_p[p] = la[p]; yld_p[p] = yl[p]; m_p[p] = ms[p]; epl[p] = 0.0

    @ti.kernel
    def substep():
        for I in ti.grouped(grid_m):
            grid_v[I] = ti.Vector.zero(ti.f32, 2); grid_m[I] = 0.0
        for p in range(N[None]):
            base = (x[p] * inv_dx - 0.5).cast(int); fx = x[p] * inv_dx - base.cast(ti.f32)
            w = [0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1.0) ** 2, 0.5 * (fx - 0.5) ** 2]
            U, sig, V = ti.svd(F[p]); J = sig[0, 0] * sig[1, 1]
            st = (2 * mu_p[p] * (F[p] - U @ V.transpose()) @ F[p].transpose()
                  + ti.Matrix.identity(ti.f32, 2) * la_p[p] * J * (J - 1))
            prs[p] = -0.5 * (st[0, 0] + st[1, 1]) / ti.max(J, 1e-4)
            st = (-dt * p_vol * 4 * inv_dx * inv_dx) * st; aff = st + m_p[p] * C[p]
            for a, b in ti.static(ti.ndrange(3, 3)):
                off = ti.Vector([a, b]); dpos = (off.cast(ti.f32) - fx) * dx; wt = w[a][0] * w[b][1]
                grid_v[base + off] += wt * (m_p[p] * v[p] + aff @ dpos); grid_m[base + off] += wt * m_p[p]
        for I in ti.grouped(grid_m):
            if grid_m[I] > 0:
                grid_v[I] /= grid_m[I]; i, j = I[0], I[1]
                if j * dx < FLOOR and grid_v[I][1] < 0: grid_v[I][1] = 0.0
                if j * dx > wall_y[None]: grid_v[I][1] = ti.min(grid_v[I][1], -WALL_V)
                if i * dx < SW_L and grid_v[I][0] < 0: grid_v[I][0] = 0.0
                if i * dx > SW_R and grid_v[I][0] > 0: grid_v[I][0] = 0.0
        for p in range(N[None]):
            base = (x[p] * inv_dx - 0.5).cast(int); fx = x[p] * inv_dx - base.cast(ti.f32)
            w = [0.5 * (1.5 - fx) ** 2, 0.75 - (fx - 1.0) ** 2, 0.5 * (fx - 0.5) ** 2]
            nv = ti.Vector.zero(ti.f32, 2); nc = ti.Matrix.zero(ti.f32, 2, 2)
            for a, b in ti.static(ti.ndrange(3, 3)):
                off = ti.Vector([a, b]); dpos = off.cast(ti.f32) - fx; wt = w[a][0] * w[b][1]; gv = grid_v[base + off]
                nv += wt * gv; nc += 4 * inv_dx * wt * gv.outer_product(dpos)
            v[p] = nv; C[p] = nc; F[p] = (ti.Matrix.identity(ti.f32, 2) + dt * nc) @ F[p]
            U, sig, V = ti.svd(F[p])
            e0 = ti.log(ti.max(sig[0, 0], 1e-4)); e1 = ti.log(ti.max(sig[1, 1], 1e-4))
            tr = e0 + e1; d0 = e0 - 0.5 * tr; d1 = e1 - 0.5 * tr; dn = ti.sqrt(d0 * d0 + d1 * d1) + 1e-9
            dg = dn - (yld_p[p] * (1.0 + HARD_SE * epl[p])) / (2 * mu_p[p])
            if dg > 0:
                epl[p] += dg
                m0 = (d0 - dg * d0 / dn) + 0.5 * tr; m1 = (d1 - dg * d1 / dn) + 0.5 * tr
                F[p] = U @ ti.Matrix([[ti.exp(m0), 0.0], [0.0, ti.exp(m1)]]) @ V.transpose()
            x[p] += dt * v[p]

    def build(R_AMP, R_AMS, fAP, fAS, fSE, rng):
        fill_h = WALL0 - 0.02; box = WIDTH * (fill_h - FLOOR); target = INIT_SOLID * box
        placed = []; cell = max(R_AMP, R_SE_MPM) * 1.05; Hm = {}
        def clash(cx, cy, r):
            ci, cj = int(cx / cell), int(cy / cell)
            for di in (-2, -1, 0, 1, 2):
                for dj in (-2, -1, 0, 1, 2):
                    for (px, py, pr) in Hm.get((ci + di, cj + dj), []):
                        if (cx - px) ** 2 + (cy - py) ** 2 < (r + pr + 0.2 * R_SE_MPM) ** 2: return True
            return False
        def add(cx, cy, r):
            placed.append((cx, cy, r)); Hm.setdefault((int(cx / cell), int(cy / cell)), []).append((cx, cy, r))
        plan = [(R_AMP, fAP, MU_AM, LA_AM, YIELD_AM, RHO_AM),
                (R_AMS, fAS, MU_AM, LA_AM, YIELD_AM, RHO_AM),
                (R_SE_MPM, fSE, MU_SE, LA_SE, YIELD_SE, RHO_SE)]
        xs = []; mu = []; la = []; yl = []; ms = []
        for (r, frac, mm, ll, yy, rho) in plan:
            if frac <= 1e-6: continue
            goal = frac * target; acc = 0.0; t = 0
            while acc < goal and t < 1_500_000:
                t += 1; cx = rng.uniform(SW_L + r, SW_R - r); cy = rng.uniform(FLOOR + r, fill_h - r)
                if clash(cx, cy, r): continue
                add(cx, cy, r)
                k = int(r / (dx * 0.5)) + 1
                for a in range(-k, k + 1):
                    for b in range(-k, k + 1):
                        px, py = cx + a * dx * 0.5, cy + b * dx * 0.5
                        if (px - cx) ** 2 + (py - cy) ** 2 <= r * r:
                            xs.append((px, py)); mu.append(mm); la.append(ll); yl.append(yy); ms.append(p_vol * rho)
                acc += np.pi * r * r
        return (np.array(xs, np.float32), np.array(mu, np.float32), np.array(la, np.float32),
                np.array(yl, np.float32), np.array(ms, np.float32))

    def run_once(R_AMP, R_AMS, fAP, fAS, fSE, seed):
        rng = np.random.default_rng(seed)
        xy, mu, la, yl, ms = build(R_AMP, R_AMS, fAP, fAS, fSE, rng); n = len(xy)
        if n == 0: return float('nan')
        sa = n * p_vol; load(xy, mu, la, yl, ms, n); wall_y[None] = WALL0
        top_full = FLOOR + sa / WIDTH; wall_floor = top_full + 0.002
        got = float('nan')
        for fr in range(int(8000 * ng / 320)):
            for _ in range(25): substep()
            Pcur = float(np.mean(prs.to_numpy()[:n])); top = wall_y[None]
            por = max(0.0, 1.0 - sa / (WIDTH * (top - FLOOR))) * 100
            if Pcur >= args.p_read:
                got = por; break
            if Pcur >= P_STOP or top <= wall_floor + 1e-4:
                got = por; break
            if top > wall_floor:
                wall_y[None] = max(top - WALL_V * 25 * dt, wall_floor)
        return got

    dps = load_design(names=set(args.names) if args.names else None,
                      real_only=args.real_only, particulate=args.particulate,
                      max_n=args.max_n)
    print(f"matching {len(dps)} DEM design points @ {args.p_read*1000:.0f} MPa, "
          f"n_grid={ng}, seeds={args.seeds}")
    rows = []
    for d in dps:
        R_AMP = R_SE_MPM * d['ratio_P']; R_AMS = R_SE_MPM * d['ratio_S']
        p, s = (int(z) for z in d['PS'].split(':')); tot = p + s
        fAP = d['phi_am'] * p / tot; fAS = d['phi_am'] * s / tot; fSE = d['phi_se']
        vals = [run_once(R_AMP, R_AMS, fAP, fAS, fSE, 7000 + i) for i in range(args.seeds)]
        vals = [x for x in vals if x == x]  # drop nan
        mpm = float(np.mean(vals)) if vals else float('nan')
        std = float(np.std(vals)) if len(vals) > 1 else 0.0
        rows.append((d['name'], d['dem'], mpm, std, d['r_SE'], d['AM_wt']))
        print(f"  {d['name'][:30]:30s} rSE={d['r_SE']:.2f} AMwt={d['AM_wt']:4.0f}  "
              f"DEM={d['dem']:5.1f}%  MPM={mpm:5.1f}±{std:.1f}%  Δ={mpm-d['dem']:+5.1f}",
              flush=True)
    with open(OUT, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['name', 'dem_porosity', 'mpm_porosity', 'mpm_std', 'r_SE', 'AM_wt'])
        for r in rows: w.writerow(r)
    import numpy as np  # noqa (already imported above; keep for clarity)
    dems = np.array([r[1] for r in rows]); mpms = np.array([r[2] for r in rows])
    ok = np.isfinite(mpms)
    if ok.sum() >= 2:
        r2 = 1 - np.sum((dems[ok]-mpms[ok])**2)/np.sum((dems[ok]-dems[ok].mean())**2)
        print(f"\n  saved {OUT}  |  DEM↔MPM parity R²(1:1)={r2:.3f}, "
              f"mean|Δ|={np.mean(np.abs(dems[ok]-mpms[ok])):.1f}%p, "
              f"Pearson={np.corrcoef(dems[ok],mpms[ok])[0,1]:.3f}")


def plot():
    import numpy as np
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    with open(OUT) as fh:
        r = list(csv.DictReader(fh))
    dem = np.array([float(x['dem_porosity']) for x in r])
    mpm = np.array([float(x['mpm_porosity']) for x in r])
    ok = np.isfinite(mpm)
    dem, mpm = dem[ok], mpm[ok]
    fig, ax = plt.subplots(figsize=(5.6, 5.4))
    lo = min(dem.min(), mpm.min()) - 2; hi = max(dem.max(), mpm.max()) + 2
    ax.plot([lo, hi], [lo, hi], 'k--', lw=1, label='1:1')
    ax.scatter(dem, mpm, s=28, c='#c0392b', alpha=0.8)
    r2 = 1 - np.sum((dem-mpm)**2)/np.sum((dem-dem.mean())**2)
    ax.set_xlabel('DEM porosity (%)'); ax.set_ylabel('MPM porosity (%) — champion 1.53/0.15')
    ax.set_title(f'DEM ↔ MPM 1:1 porosity @ 300 MPa\nR²(1:1)={r2:.3f}, '
                 f'Pearson={np.corrcoef(dem,mpm)[0,1]:.3f}, n={len(dem)}', fontsize=10)
    ax.set_xlim(lo, hi); ax.set_ylim(lo, hi); ax.set_aspect('equal'); ax.grid(alpha=0.3); ax.legend()
    plt.tight_layout(); os.makedirs(os.path.join(HERE, '..', 'docs', 'figures'), exist_ok=True)
    out = os.path.join(HERE, '..', 'docs', 'figures', 'mpm_dem_match_parity.png')
    plt.savefig(out, dpi=130); print(f"saved {out}")


def group_plot():
    """Trend plot: porosity vs AM wt%, grouped by SE radius, DEM (solid) vs MPM
    (dashed).  Shows whether the DEM size-dependent crossover (small-SE
    descending / large-SE ascending) survives under true-plastic MPM."""
    import numpy as np
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    with open(OUT) as fh:
        r = list(csv.DictReader(fh))
    if not r or 'r_SE' not in r[0]:
        print("CSV has no r_SE/AM_wt columns — re-run the match first (not --plot)."); return
    # group rows by SE radius
    groups = {}
    for x in r:
        try:
            rse = float(x['r_SE']); amw = float(x['AM_wt'])
            dem = float(x['dem_porosity']); mpm = float(x['mpm_porosity'])
        except (KeyError, ValueError):
            continue
        if not np.isfinite(mpm):
            continue
        groups.setdefault(round(rse, 3), []).append((amw, dem, mpm))
    fig, ax = plt.subplots(figsize=(7.6, 5.4))
    cmap = plt.get_cmap('viridis')
    rkeys = sorted(groups)
    for i, rse in enumerate(rkeys):
        pts = sorted(groups[rse])
        amw = [p[0] for p in pts]; dem = [p[1] for p in pts]; mpm = [p[2] for p in pts]
        c = cmap(i / max(len(rkeys) - 1, 1))
        ax.plot(amw, dem, '-o', color=c, lw=2, ms=6, label=f'DEM  r_SE={rse}')
        ax.plot(amw, mpm, '--s', color=c, lw=1.6, ms=6, mfc='none', alpha=0.9,
                label=f'MPM r_SE={rse}')
    ax.set_xlabel('AM wt%'); ax.set_ylabel('Porosity (%)')
    ax.set_title('DEM (solid) vs true-plastic MPM (dashed) porosity\n'
                 'per SE radius — does the size-dependent crossover survive plasticity?',
                 fontsize=10)
    ax.grid(alpha=0.3); ax.legend(fontsize=7, ncol=2)
    plt.tight_layout(); os.makedirs(os.path.join(HERE, '..', 'docs', 'figures'), exist_ok=True)
    out = os.path.join(HERE, '..', 'docs', 'figures', 'mpm_dem_match_trend.png')
    plt.savefig(out, dpi=130); print(f"saved {out}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n-grid', type=int, default=320)
    ap.add_argument('--seeds', type=int, default=2)
    ap.add_argument('--real-only', action='store_true')
    ap.add_argument('--particulate', action='store_true',
                    help='only input_particulate_* / input_S_* (monomodal SE-size sweep)')
    ap.add_argument('--max-n', type=int, default=None)
    ap.add_argument('--names', nargs='*', default=None)
    ap.add_argument('--p-read', type=float, default=0.30, help='read pressure GPa (0.30 = 300 MPa)')
    ap.add_argument('--plot', action='store_true', help='parity scatter (DEM vs MPM)')
    ap.add_argument('--group-plot', action='store_true',
                    help='trend: porosity vs AM wt% per SE radius, DEM vs MPM')
    a = ap.parse_args()
    if a.plot:
        plot(); return
    if a.group_plot:
        group_plot(); return
    run_match(a)


if __name__ == '__main__':
    main()

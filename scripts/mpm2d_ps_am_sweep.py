#!/usr/bin/env python3
"""2D MPM-DEM porosity sweep over (P:S, AM:SE wt%) → CSV + 3D colormap + regression.

The 45-point composition grid the user asked for:
  P:S  (AM_P:AM_S) = 1:9, 2:8, … , 9:1     (p_frac = 0.1 … 0.9)
  AM:SE (AM wt%)   = 75, 80, 85, 90, 95
= 9 × 5 = 45 points.  Each point: the 2D true-plastic MPM (mpm2d_composition physics —
AM rigid jams / SE plastic flows, confined oedometer) is compacted; porosity is read at a
COMMON pressure across the whole grid (fair composition comparison).  Then it fits
porosity = f(P:S, AM%) (poly2/poly3 surface, R²) and draws a 3D surface + 2D heatmap.

Calibration: defaults to the mpm2d_composition reference (E_SE≈24, σ_y=0.6, RCP-style —
shows the Furnas dip).  For the production champion pass  --e-se 1.53 --yield-se 0.15
(denser SE-rich flank, no dip — CLAUDE.md frame[4]/CORRECTION 2).  Pressure is the grid's
common-pressure (arbitrary units, NOT a calibrated 300 MPa) — this is a TREND/surface study.

The 45×seeds MPM runs are the heavy part → run on a GPU box / detached; then re-fit &
redraw the CSV instantly with --analyze-only.

  # full sweep (heavy; ~40 min CPU for 45×3) — run detached on the server:
  python3 scripts/mpm2d_ps_am_sweep.py --seeds 3
  # champion calibration instead of RCP-style:
  python3 scripts/mpm2d_ps_am_sweep.py --seeds 3 --e-se 1.53 --yield-se 0.15
  # just re-fit + redraw an existing CSV (instant):
  python3 scripts/mpm2d_ps_am_sweep.py --analyze-only docs/data/mpm2d_ps_am_porosity.csv
  # quick smoke test (tiny grid):
  python3 scripts/mpm2d_ps_am_sweep.py --quick
"""
import argparse
import csv
import os

import numpy as np


def parse_ps(s):
    """'1:9' -> p_frac 0.1  (also accepts a bare fraction '0.1')."""
    if ':' in s:
        p, q = s.split(':'); p, q = float(p), float(q)
        return p / (p + q)
    return float(s)


def run_sweep(a):
    os.environ['MPM2D_ARCH'] = a.arch          # picked up by mpm2d_composition's ti.init at import
    import mpm2d_composition as m
    if a.e_se is not None:
        m.MU_SE, m.LA_SE = m.lame(a.e_se)             # override SE modulus (default module 24; champion 1.53)
    p_fracs = [parse_ps(s) for s in a.ps]
    am_wts = [float(x) for x in a.am_wt]
    runs = []                                          # (p_frac, am_wt, seed, series)
    for pf in p_fracs:
        for am in am_wts:
            for sd in range(a.seeds):
                rng = np.random.default_rng(1000 * sd + int(am) + int(round(pf * 100)))
                xy, mus, las, ylds = m.build(am, rng, yield_se=a.yield_se, p_frac=pf)
                solid = len(xy) * m.p_vol
                s, n = m.run_composition(xy, mus, las, ylds, solid)
                runs.append((pf, am, sd, s))
                print(f"  P:S={pf:.2f} AM={am:.0f}wt seed{sd}: n={n:5d}  Pmax={s[:, 1].max():.3f}", flush=True)
    P_COMMON = min(s[:, 1].max() for *_, s in runs) * a.read_frac   # read porosity at this common pressure
    agg = {}
    for pf, am, sd, s in runs:
        order = np.argsort(s[:, 1])
        por = float(np.interp(P_COMMON, s[:, 1][order], s[:, 0][order]))
        agg.setdefault((pf, am), []).append(por)
    out = [(pf, am, float(np.mean(v)), float(np.std(v)), len(v)) for (pf, am), v in sorted(agg.items())]
    return out, P_COMMON


def write_csv(path, rows, P_COMMON, e_se, yield_se):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w', newline='') as f:
        f.write(f"# 2D MPM porosity vs (P:S, AM wt%).  E_SE={e_se} yield_SE={yield_se}  "
                f"P_common={P_COMMON:.4f} (arb units, common-pressure trend — not calibrated 300 MPa)\n")
        w = csv.writer(f)
        w.writerow(['p_frac', 'ps_label', 'am_wt', 'porosity_pct', 'porosity_std', 'n_seed'])
        for pf, am, por, std, ns in rows:
            p10 = int(round(pf * 10))
            w.writerow([f'{pf:.3f}', f'{p10}:{10 - p10}', f'{am:.0f}', f'{por:.3f}', f'{std:.3f}', ns])
    print(f"wrote {path}  ({len(rows)} points)")


def read_csv(path):
    rows = []
    with open(path) as f:
        for line in f:
            if line.startswith('#') or line.lower().startswith('p_frac'):
                continue
            t = line.strip().split(',')
            if len(t) >= 4:
                rows.append((float(t[0]), float(t[2]), float(t[3])))   # p_frac, am_wt, porosity
    return rows


def _design(p, a, deg):
    cols = [np.ones_like(p), p, a]
    if deg >= 2:
        cols += [p * p, a * a, p * a]
    if deg >= 3:
        cols += [p ** 3, a ** 3, p * p * a, p * a * a]
    return np.column_stack(cols)


def fit_and_plot(rows, out_png):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (registers 3d projection)

    P = np.array([r[0] for r in rows]); A = np.array([r[1] for r in rows]); Z = np.array([r[2] for r in rows])
    fits = {}
    for deg in (2, 3):
        X = _design(P, A, deg)
        coef, *_ = np.linalg.lstsq(X, Z, rcond=None)
        pred = X @ coef
        ss_res = float(np.sum((Z - pred) ** 2)); ss_tot = float(np.sum((Z - Z.mean()) ** 2))
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else float('nan')
        rmse = float(np.sqrt(np.mean((Z - pred) ** 2)))
        fits[deg] = (coef, r2, rmse)
    names2 = ['1', 'P', 'A', 'P²', 'A²', 'P·A']
    c2, r2_2, rmse2 = fits[2]; c3, r2_3, rmse3 = fits[3]
    print("\n=== regression  porosity(%) = f(P,A)   P=AM_P fraction (0–1), A=AM wt% ===")
    print(f"poly2  R²={r2_2:.4f}  RMSE={rmse2:.3f} %p")
    print("  ε = " + "  ".join(f"{c:+.4g}·{n}" for c, n in zip(c2, names2)))
    print(f"poly3  R²={r2_3:.4f}  RMSE={rmse3:.3f} %p")

    fig = plt.figure(figsize=(13, 5))
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    pg, ag = np.meshgrid(np.linspace(P.min(), P.max(), 40), np.linspace(A.min(), A.max(), 40))
    zg = (_design(pg.ravel(), ag.ravel(), 2) @ c2).reshape(pg.shape)
    ax1.plot_surface(pg * 10, ag, zg, cmap='viridis', alpha=0.75, linewidth=0)
    ax1.scatter(P * 10, A, Z, c='r', s=18, depthshade=False)
    ax1.set_xlabel('P:S  (AM_P/10)'); ax1.set_ylabel('AM wt%'); ax1.set_zlabel('porosity %')
    ax1.set_title(f'2D MPM porosity surface  (poly2 R²={r2_2:.3f})')
    ax2 = fig.add_subplot(1, 2, 2)
    pu = np.unique(P); au = np.unique(A); H = np.full((len(au), len(pu)), np.nan)
    for r in rows:
        H[np.where(au == r[1])[0][0], np.where(pu == r[0])[0][0]] = r[2]
    im = ax2.pcolormesh(pu * 10, au, H, cmap='viridis', shading='nearest')
    fig.colorbar(im, ax=ax2, label='porosity %')
    ax2.set_xlabel('P:S  (AM_P / 10)'); ax2.set_ylabel('AM wt%'); ax2.set_title('porosity heatmap (45 pts)')
    os.makedirs(os.path.dirname(out_png) or '.', exist_ok=True)
    fig.tight_layout(); fig.savefig(out_png, dpi=130)
    print(f"saved {out_png}")
    return fits


def main():
    ap = argparse.ArgumentParser(description='2D MPM porosity sweep over (P:S, AM wt%) + colormap + regression.')
    ap.add_argument('--ps', nargs='*',
                    default=['0:10', '1:9', '2:8', '3:7', '4:6', '5:5', '6:4', '7:3', '8:2', '9:1', '10:0'])
    ap.add_argument('--am-wt', nargs='*', default=['75', '80', '85', '90', '95'])
    ap.add_argument('--seeds', type=int, default=3)
    ap.add_argument('--arch', default='cpu', choices=['cpu', 'gpu', 'cuda', 'vulkan'],
                    help='Taichi arch.  The 2D grid (128²) is tiny → CPU is usually fine; GPU helps little '
                         '(the per-case disk placement is CPU-bound).  Use cuda only if the box has a free GPU.')
    ap.add_argument('--e-se', type=float, default=None,
                    help='SE modulus GPa (default module ≈24 RCP-style; champion 1.53)')
    ap.add_argument('--yield-se', type=float, default=0.6, help='SE yield (default 0.6 RCP-style; champion 0.15)')
    ap.add_argument('--read-frac', type=float, default=0.4,
                    help='read porosity at this fraction of the grid common-max pressure.  At ~0.95 (full '
                         'compaction) the continuum SE over-compacts the SE-rich/AM-75 end to ~0%% (MPM '
                         'flow artifact); ~0.35-0.5 reads mid-compaction → non-degenerate, sensible surface.')
    ap.add_argument('--out', default='docs/data/mpm2d_ps_am_porosity.csv')
    ap.add_argument('--png', default='docs/figures/mpm2d_ps_am_porosity.png')
    ap.add_argument('--analyze-only', default=None, help='skip the sweep; read this CSV and just fit + plot')
    ap.add_argument('--quick', action='store_true', help='tiny grid smoke test (3×2×1)')
    a = ap.parse_args()

    if a.analyze_only:
        fit_and_plot(read_csv(a.analyze_only), a.png)
        return
    if a.quick:
        a.ps = ['1:9', '5:5', '9:1']; a.am_wt = ['75', '95']; a.seeds = 1
    rows, P_COMMON = run_sweep(a)
    write_csv(a.out, rows, P_COMMON, a.e_se if a.e_se is not None else 24.0, a.yield_se)
    fit_and_plot([(r[0], r[1], r[2]) for r in rows], a.png)


if __name__ == '__main__':
    main()

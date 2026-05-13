"""plot_v30u_1L_correct_z0_only.py — OLD figure 재현용 (z=0 36-reg mean only).

v30u_1L_correct_results JSON에서 z=0 평균(36 xy registry mean)만 추출.
이는 OLD figure (phase1 rigid 36-reg mean)와 동일한 protocol — 5 z-shift는 무시.

Output:
  /data/work/v30u_ensemble/v30u_1L_correct_z0_curves.{png,pdf,csv}

OLD figure CSV(digitized)와도 같이 plot해서 직접 비교 가능.
Run on gabia:
  cd /data/work/v30u_ensemble
  python3 plot_v30u_1L_correct_z0_only.py
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import CubicSpline

RESULTS = Path('/data/work/v30u_ensemble/v30u_1L_correct_results')
OUT_DIR = Path('/data/work/v30u_ensemble')
OUT_PNG = OUT_DIR / 'v30u_1L_correct_z0_OLDstyle.png'
OUT_PDF = OUT_DIR / 'v30u_1L_correct_z0_OLDstyle.pdf'
OUT_CSV = OUT_DIR / 'v30u_1L_correct_z0_OLDstyle.csv'

PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}
COMPS_AVAIL = ['comp1', 'comp2', 'comp4', 'modelC']  # 현재 v30u_1L_correct에 있는 것

COLORS = {'comp1': '#1f77b4', 'comp2': '#17becf',
          'comp3': '#d62728', 'comp4': '#9467bd', 'comp5': '#2ca02c',
          'modelC': '#888888'}
MARKERS = {'comp1': 's', 'comp2': 'o', 'comp3': '^', 'comp4': 'D', 'comp5': 'v', 'modelC': 'P'}
LABELS = {
    'comp1':  r'comp1: Li$_6$PS$_5$Cl',
    'comp2':  r'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$',
    'comp3':  r'comp3: Li$_{5.4}$PS$_{4.4}$Cl$_{1.0}$Br$_{0.6}$',
    'comp4':  r'comp4: Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$',
    'comp5':  r'comp5: Li$_{5.4}$PS$_{4.4}$Cl$_{0.6}$Br$_{1.0}$',
    'modelC': r'modelC: Li$_{5.4}$PS$_{4.4}$Cl$_{1.6}$',
}


def extract_z0_mean(comp_data):
    """Extract z=0 36-reg mean Wad curve from comp_data['Wad_per_z_per_reg']['z0']."""
    z0 = comp_data['Wad_per_z_per_reg']['z0']
    gaps = comp_data['gaps']
    n_reg = len(z0)
    # Mean across registries per gap
    means, stds = [], []
    for g in gaps:
        gk = f"{g:.3f}"
        vals = []
        for reg_name, reg in z0.items():
            v = reg['curve'].get(gk, {}).get('Wad_J_per_m2')
            if v is not None:
                vals.append(v)
        if vals:
            means.append(float(np.mean(vals)))
            stds.append(float(np.std(vals)))
        else:
            means.append(np.nan)
            stds.append(np.nan)
    return np.array(gaps), np.array(means), np.array(stds), n_reg


def to_e_adh(wad):
    """OLD figure convention: E_adh = -Wad (negative = binding favorable)."""
    return -wad


def morse(d, D, a, d_eq, offset):
    return D * (1 - np.exp(-a * (d - d_eq)))**2 - D + offset


def fit_morse(g, e):
    g = np.asarray(g); e = np.asarray(e)
    valid = ~np.isnan(e)
    g, e = g[valid], e[valid]
    if len(g) < 5:
        return None
    i_min = int(np.argmin(e))
    p0 = [abs(e[i_min] - e[-1]), 2.0, g[i_min], e[-1]]
    try:
        popt, _ = curve_fit(morse, g, e, p0=p0, maxfev=20000,
                            bounds=([0.001, 0.1, 0.5, -3.0],
                                    [10.0, 10.0, 5.0, 3.0]))
        return popt
    except Exception:
        return None


def main():
    print(f"Reading from: {RESULTS}")
    print(f"Comps available expected: {COMPS_AVAIL}\n")

    curves = {}  # comp -> (gaps, e_adh_mean, e_adh_std, n_reg)
    for c in COMPS_AVAIL:
        f = RESULTS / f"{c}_done.json"
        if not f.exists():
            print(f"  [SKIP] {c}: {f.name} not found")
            continue
        d = json.load(open(f))
        gaps, wad_mean, wad_std, n_reg = extract_z0_mean(d)
        e_mean = to_e_adh(wad_mean)
        e_std = wad_std  # std unchanged by sign flip
        curves[c] = (gaps, e_mean, e_std, n_reg)
        # well/asymp summary
        i_min = int(np.nanargmin(e_mean))
        e_min, d_min = e_mean[i_min], gaps[i_min]
        e_asymp = e_mean[-1]
        well_depth = e_asymp - e_min
        print(f"  [✓] {c}: n_reg={n_reg}  d_min={d_min:.2f}Å  "
              f"E_adh(well)={e_min:+.4f}  E_adh(asymp)={e_asymp:+.4f}  "
              f"well_depth={well_depth:.4f} J/m²")

    if not curves:
        print("NO data found. Check path.")
        return

    # R(well_depth, paper exp)
    paper_vals, well_vals, names = [], [], []
    for c, (g, e, _, _) in curves.items():
        if c in PAPER_EXP:
            i_min = int(np.nanargmin(e))
            well = e[-1] - e[i_min]   # asymp - well, positive = bound
            paper_vals.append(PAPER_EXP[c])
            well_vals.append(well)
            names.append(c)
    if len(paper_vals) >= 2:
        R = float(np.corrcoef(paper_vals, well_vals)[0, 1])
        print(f"\nR(well_depth_J/m², paper_aJ) = {R:+.3f}  (n={len(paper_vals)}, {names})")
    else:
        R = None

    # ============ PLOT ============
    fig, ax = plt.subplots(figsize=(10, 6.5))
    plot_order = ['comp1', 'comp2', 'comp4', 'comp3', 'comp5', 'modelC']
    for c in plot_order:
        if c not in curves:
            continue
        g, e, es, n_reg = curves[c]
        # raw points
        ax.errorbar(g, e, yerr=es, fmt=MARKERS[c], color=COLORS[c],
                    markersize=7, alpha=0.85, capsize=2, zorder=3,
                    label=None)
        # Morse smoothed curve
        popt = fit_morse(g, e)
        if popt is not None:
            g_dense = np.linspace(g.min(), g.max(), 600)
            ax.plot(g_dense, morse(g_dense, *popt),
                    '-', color=COLORS[c], lw=2.2, zorder=2,
                    label=LABELS.get(c, c))
        else:
            # cubic spline fallback
            valid = ~np.isnan(e)
            cs = CubicSpline(g[valid], e[valid])
            g_dense = np.linspace(g[valid].min(), g[valid].max(), 600)
            ax.plot(g_dense, cs(g_dense), '-', color=COLORS[c], lw=2.2,
                    zorder=2, label=LABELS.get(c, c))

    ax.axhline(0, color='k', lw=0.6)
    ax.axvspan(1.2, 1.6, alpha=0.12, color='grey', zorder=0)
    ax.set_xlabel(r'Interface gap, $d$ (Å)', fontsize=12)
    ax.set_ylabel(r'Adhesion energy (J m$^{-2}$)', fontsize=12)
    title = 'v30u_1L_correct (z=0, 36-reg mean) — OLD-figure style'
    if R is not None:
        title += f'   R={R:+.3f}'
    ax.set_title(title, fontsize=12)
    ax.legend(loc='lower right', fontsize=9, framealpha=0.95)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=200, bbox_inches='tight')
    plt.savefig(OUT_PDF, bbox_inches='tight')
    print(f"\nSaved: {OUT_PNG}")
    print(f"Saved: {OUT_PDF}")

    # ============ CSV ============
    with open(OUT_CSV, 'w') as f:
        gaps_master = curves[list(curves.keys())[0]][0]
        f.write("# v30u_1L_correct z=0 36-reg mean (OLD-figure style)\n")
        f.write("# E_adh = -Wad (NEGATIVE = bound)  Units: J/m^2\n")
        cols = list(curves.keys())
        f.write("gap_A," + ",".join(cols) + "\n")
        for i, g in enumerate(gaps_master):
            row = [f"{g:.3f}"]
            for c in cols:
                v = curves[c][1][i]
                row.append(f"{v:+.4f}" if not np.isnan(v) else "")
            f.write(",".join(row) + "\n")
    print(f"Saved: {OUT_CSV}")


if __name__ == "__main__":
    main()

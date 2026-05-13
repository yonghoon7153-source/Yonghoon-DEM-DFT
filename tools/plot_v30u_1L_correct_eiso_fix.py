"""plot_v30u_1L_correct_eiso_fix.py — visualize the cell-mismatch corrected data.

Reads:  /data/work/v30u_ensemble/v30u_1L_correct_results_eiso_fix/{comp}_done.json
Writes: v30u_1L_correct_eiso_fix_curves.{png,pdf,csv}

Plots 5z × 36-reg mean binding curves (E_adh = -Wad) for 4 comps after
applying the E_ncm-in-SE-cell correction. With asymp ≈ 0, the figure now
shows the canonical binding-curve shape: wells below 0, asymp near 0.

Also overlays z=0-only and 5z-mean side by side, and reports two R metrics
against paper exp aJ:
   - R(Wad_max, paper)        — paper convention
   - R(well_depth, paper)     — asymp-subtracted convention

Run on gabia:
  cd /data/work/v30u_ensemble
  python3 plot_v30u_1L_correct_eiso_fix.py
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import CubicSpline

RESULTS = Path('/data/work/v30u_ensemble/v30u_1L_correct_results_eiso_fix')
OUT_DIR = Path('/data/work/v30u_ensemble')
OUT_PNG = OUT_DIR / 'v30u_1L_correct_eiso_fix_curves.png'
OUT_PDF = OUT_DIR / 'v30u_1L_correct_eiso_fix_curves.pdf'
OUT_CSV = OUT_DIR / 'v30u_1L_correct_eiso_fix_curves.csv'

PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}
COMPS_AVAIL = ['comp1', 'comp2', 'comp4', 'modelC']

COLORS  = {'comp1': '#1f77b4', 'comp2': '#17becf',
           'comp3': '#d62728', 'comp4': '#9467bd', 'comp5': '#2ca02c',
           'modelC': '#888888'}
MARKERS = {'comp1': 's', 'comp2': 'o', 'comp3': '^', 'comp4': 'D',
           'comp5': 'v', 'modelC': 'P'}
LABELS  = {
    'comp1':  r'comp1: Li$_6$PS$_5$Cl',
    'comp2':  r'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$',
    'comp3':  r'comp3: Li$_{5.4}$PS$_{4.4}$Cl$_{1.0}$Br$_{0.6}$',
    'comp4':  r'comp4: Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$',
    'comp5':  r'comp5: Li$_{5.4}$PS$_{4.4}$Cl$_{0.6}$Br$_{1.0}$',
    'modelC': r'modelC: Li$_{5.4}$PS$_{4.4}$Cl$_{1.6}$',
}


def morse(d, D, a, d_eq, offset):
    return D * (1 - np.exp(-a * (d - d_eq)))**2 - D + offset


def fit_morse(g, e):
    g, e = np.asarray(g), np.asarray(e)
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


def smooth_curve(g, e):
    """Return dense (g_dense, e_dense). Morse first, cubic-spline fallback."""
    popt = fit_morse(g, e)
    if popt is not None:
        g_dense = np.linspace(g.min(), g.max(), 600)
        return g_dense, morse(g_dense, *popt)
    valid = ~np.isnan(np.asarray(e))
    g_arr = np.asarray(g)[valid]
    e_arr = np.asarray(e)[valid]
    cs = CubicSpline(g_arr, e_arr)
    g_dense = np.linspace(g_arr.min(), g_arr.max(), 600)
    return g_dense, cs(g_dense)


def extract_z0_mean(comp_data):
    """z=0 36-reg mean (phase1 protocol identical)."""
    z0 = comp_data['Wad_per_z_per_reg']['z0']
    gaps = comp_data['gaps']
    means, stds = [], []
    for g in gaps:
        gk = f"{g:.3f}"
        vals = [r['curve'][gk]['Wad_J_per_m2']
                for r in z0.values()
                if r['curve'].get(gk, {}).get('Wad_J_per_m2') is not None]
        means.append(float(np.mean(vals)) if vals else np.nan)
        stds.append(float(np.std(vals))  if vals else np.nan)
    return np.array(gaps), np.array(means), np.array(stds)


def extract_5z_mean(comp_data):
    """5z × 36-reg mean (saved as Wad_mean in JSON)."""
    return (np.array(comp_data['gaps']),
            np.array(comp_data['Wad_mean'],  dtype=float),
            np.array(comp_data['Wad_std'],   dtype=float))


def compute_R(curves_dict, metric_fn):
    """R(metric, paper_aJ) for paper comps present in curves_dict."""
    paper_vals, m_vals, names = [], [], []
    for c, (g, e, _) in curves_dict.items():
        if c not in PAPER_EXP: continue
        paper_vals.append(PAPER_EXP[c])
        m_vals.append(metric_fn(g, e))
        names.append(c)
    if len(paper_vals) < 2:
        return None, names, paper_vals, m_vals
    R = float(np.corrcoef(paper_vals, m_vals)[0, 1])
    return R, names, paper_vals, m_vals


def main():
    print(f"Reading: {RESULTS}\n")
    curves_5z, curves_z0 = {}, {}
    for c in COMPS_AVAIL:
        f = RESULTS / f"{c}_done.json"
        if not f.exists():
            print(f"  [SKIP] {c}: file not found")
            continue
        d = json.load(open(f))
        # Wad → E_adh = -Wad
        g5, w5, s5 = extract_5z_mean(d)
        gz, wz, sz = extract_z0_mean(d)
        curves_5z[c] = (g5, -w5, s5)
        curves_z0[c] = (gz, -wz, sz)
        i_min_5z = int(np.nanargmin(-w5))
        i_min_z0 = int(np.nanargmin(-wz))
        print(f"[{c}]")
        print(f"  5z×36 mean:  E_adh well={-w5[i_min_5z]:+.4f}  asymp={-w5[-1]:+.4f}  d_min={g5[i_min_5z]:.2f}")
        print(f"  z=0  36-reg: E_adh well={-wz[i_min_z0]:+.4f}  asymp={-wz[-1]:+.4f}  d_min={gz[i_min_z0]:.2f}")

    # R metrics
    print("\n── R(metric, paper_aJ) ────────────────────────")
    for label, curves in [("5z×36 mean", curves_5z), ("z=0 36-reg", curves_z0)]:
        R_wm,  names, pv, mv  = compute_R(curves, lambda g, e: -np.nanmin(e))   # Wad_max
        R_wd,  _,     _,  mvd = compute_R(curves, lambda g, e: e[-1] - np.nanmin(e))  # well_depth
        print(f"  {label}:")
        print(f"     R(Wad_max,    paper) = {R_wm:+.3f}   names={names}")
        print(f"     R(well_depth, paper) = {R_wd:+.3f}")

    # ───────── PLOT: 2-panel (5z mean | z=0) ─────────
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.2), sharey=True)
    plot_order = ['comp1', 'comp2', 'comp4', 'modelC']

    for ax, (label, curves) in zip(axes,
                                   [('5z × 36-reg mean (full ensemble)', curves_5z),
                                    ('z=0 36-reg mean (phase1-equivalent)',  curves_z0)]):
        R_wm, _, _, _ = compute_R(curves, lambda g, e: -np.nanmin(e))
        for c in plot_order:
            if c not in curves: continue
            g, e, es = curves[c]
            ax.errorbar(g, e, yerr=es, fmt=MARKERS[c], color=COLORS[c],
                        markersize=6, alpha=0.85, capsize=2, zorder=3, label=None)
            gd, ed = smooth_curve(g, e)
            ax.plot(gd, ed, '-', color=COLORS[c], lw=2.2, zorder=2,
                    label=LABELS.get(c, c))
        ax.axhline(0, color='k', lw=0.6)
        ax.axvspan(1.2, 1.6, alpha=0.10, color='grey', zorder=0)
        ax.set_xlabel(r'Interface gap, $d$ (Å)', fontsize=11)
        title = label
        if R_wm is not None:
            title += f"   R(Wad$_{{max}}$,paper)={R_wm:+.3f}"
        ax.set_title(title, fontsize=11)
        ax.grid(alpha=0.3)
    axes[0].set_ylabel(r'Adhesion energy, E$_{adh}$ = $-W_{ad}$  (J m$^{-2}$)', fontsize=11)
    axes[1].legend(loc='upper right', fontsize=8, framealpha=0.95)

    plt.suptitle('v30u_1L_correct + E$_{ncm}$-in-SE-cell fix '
                 '(asymp baseline ≈ 0 now)', fontsize=12, y=1.00)
    plt.tight_layout()
    plt.savefig(OUT_PNG, dpi=200, bbox_inches='tight')
    plt.savefig(OUT_PDF, bbox_inches='tight')
    print(f"\nSaved: {OUT_PNG}")
    print(f"Saved: {OUT_PDF}")

    # ───────── CSV (5z mean, OLD figure style) ─────────
    with open(OUT_CSV, 'w') as f:
        f.write("# v30u_1L_correct + eiso_fix  (5z × 36-reg mean)\n")
        f.write("# E_adh = -Wad  [J/m²]   (NEGATIVE = bound)\n")
        cols = list(curves_5z.keys())
        gaps = curves_5z[cols[0]][0]
        f.write("gap_A," + ",".join(cols) + "\n")
        for i, g in enumerate(gaps):
            row = [f"{g:.3f}"]
            for c in cols:
                v = curves_5z[c][1][i]
                row.append(f"{v:+.4f}" if not np.isnan(v) else "")
            f.write(",".join(row) + "\n")
    print(f"Saved: {OUT_CSV}")


if __name__ == "__main__":
    main()

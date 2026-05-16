"""Gaussian-smoothed binding curves from digitized CSV.

Reads paper_figures_v1/binding_curves_v1_paper_figure.csv and
plots ultra-smooth curves using:
  1. Morse-potential fit per comp (physically motivated, asymmetric well)
  2. Fallback: dense cubic spline + Gaussian smoothing if Morse fit fails

Output style matches image 2 (5 paper comps, raw -W, no asymptote subtract,
gap window 1.2-1.6 highlighted, R in title).

Usage:
    python plot_binding_curves_morse.py [CSV_PATH]
    # default: output/paper_figures_v1/binding_curves_v1_paper_figure.csv
    # output: binding_curves_plots/figure_v8_morse_smooth.{png,pdf}
"""
import csv, sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import CubicSpline
from scipy.ndimage import gaussian_filter1d

CSV_DEFAULT = "output/paper_figures_v1/binding_curves_v1_paper_figure.csv"
CSV_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(CSV_DEFAULT)
OUT_DIR = Path("binding_curves_plots"); OUT_DIR.mkdir(exist_ok=True)

PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']

COLORS  = {'comp1': '#1f77b4', 'comp2': '#17becf',
           'comp3': '#d62728', 'comp4': '#9467bd', 'comp5': '#2ca02c'}
MARKERS = {'comp1': 's', 'comp2': 'o', 'comp3': '^', 'comp4': 'D', 'comp5': 'v'}
LABELS  = {
    'comp1': r'comp1: Li$_6$PS$_5$Cl',
    'comp2': r'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$',
    'comp3': r'comp3: Li$_{5.4}$PS$_{4.4}$Cl$_{1.0}$Br$_{0.6}$',
    'comp4': r'comp4: Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$',
    'comp5': r'comp5: Li$_{5.4}$PS$_{4.4}$Cl$_{0.6}$Br$_{1.0}$',
}


def morse(d, D, a, d_eq, offset):
    """Morse potential — asymmetric well + repulsive wall."""
    return D * (1 - np.exp(-a * (d - d_eq)))**2 - D + offset


def fit_morse(gaps, energies):
    valid = ~np.isnan(energies)
    g, e = gaps[valid], energies[valid]
    if len(g) < 5:
        return None
    i_min = int(np.argmin(e))
    p0 = [abs(e[i_min] - e[-1]), 2.0, g[i_min], e[-1]]
    try:
        popt, _ = curve_fit(morse, g, e, p0=p0, maxfev=20000,
                             bounds=([0.01, 0.1, 0.5, -2], [5, 10, 4, 2]))
        return popt
    except Exception:
        return None


def smooth_fallback(gaps, energies):
    """Dense cubic spline + Gaussian filter — guaranteed-smooth fallback."""
    valid = ~np.isnan(energies)
    g, e = gaps[valid], energies[valid]
    cs = CubicSpline(g, e)
    g_dense = np.linspace(g.min(), g.max(), 2000)
    e_dense = cs(g_dense)
    e_smoothed = gaussian_filter1d(e_dense, sigma=25)  # heavy smoothing
    return g_dense, e_smoothed


def main():
    rows = [r for r in csv.reader(open(CSV_PATH))
            if r and not r[0].startswith('#')]
    header = rows[0]
    data = rows[1:]
    gaps = np.array([float(r[0]) for r in data])
    cols = {h: np.array([float(r[i]) if r[i] else np.nan for r in data])
            for i, h in enumerate(header) if h in PAPER_COMPS}

    plt.rcParams.update({
        'font.size': 13, 'axes.labelsize': 15, 'axes.titlesize': 16,
        'xtick.labelsize': 12, 'ytick.labelsize': 12, 'legend.fontsize': 11,
        'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
    })
    fig, ax = plt.subplots(figsize=(11, 7.5))

    g_lo, g_hi = float(np.nanmin(gaps)), float(np.nanmax(gaps))
    g_dense = np.linspace(g_lo, g_hi, 2000)

    well_depths = {}
    fit_method = {}
    for c in PAPER_COMPS:
        if c not in cols:
            continue
        e = cols[c]
        # try Morse
        popt = fit_morse(gaps, e)
        if popt is not None:
            e_smooth = morse(g_dense, *popt)
            fit_method[c] = f"Morse(D={popt[0]:.3f}, d_eq={popt[2]:.2f})"
        else:
            g_dense_, e_smooth = smooth_fallback(gaps, e)
            g_dense = g_dense_
            fit_method[c] = "Cubic+Gaussian(sigma=25)"

        ax.plot(g_dense, e_smooth, '-', color=COLORS[c], lw=3.0, alpha=0.95, zorder=5)
        valid = ~np.isnan(e)
        ax.plot(gaps[valid], e[valid], MARKERS[c], color=COLORS[c],
                ms=9, mec='k', mew=0.5, label=LABELS[c], zorder=10)

        # well depth from smoothed curve in window 0.9-2.5
        m = (g_dense >= 0.5) & (g_dense <= 6.0)  # FULL CURVE
        well_depths[c] = float(e_smooth[m].min())

    have = [c for c in PAPER_COMPS if c in well_depths]
    if len(have) >= 3:
        x = [-well_depths[c] for c in have]
        y = [PAPER_EXP[c] for c in have]
        R = float(np.corrcoef(x, y)[0, 1])
    else:
        R = float('nan')

    ax.axvspan(1.2, 1.6, alpha=0.13, color='gray', zorder=1)
    ax.axhline(0, color='k', lw=0.7, alpha=0.7, zorder=2)
    ax.set_xlabel(r'Interface gap, $d$ (Å)')
    ax.set_ylabel(r'Adhesion energy (J m$^{-2}$)')
    ax.set_title(f'UMA binding curves (Morse-fit smoothed, R = {R:+.3f})')
    ax.set_xlim(g_lo, g_hi)
    ax.grid(True, alpha=0.25)
    ax.legend(loc='lower right', framealpha=0.95)

    fig.tight_layout()
    png = OUT_DIR / "figure_v8_morse_smooth.png"
    pdf = OUT_DIR / "figure_v8_morse_smooth.pdf"
    fig.savefig(png); fig.savefig(pdf); plt.close()

    # Dense CSV with Morse-smoothed values (0.02 A step).
    # Per-comp gap range limited to where source data exists (NaN outside)
    # to avoid Morse extrapolation blowing up at small d for comp4/comp5.
    g_csv = np.arange(g_lo, g_hi + 0.02/2, 0.02)
    smooth_curves = {}
    for c in PAPER_COMPS:
        if c not in cols:
            continue
        e = cols[c]
        valid = ~np.isnan(e)
        g_min_c = float(gaps[valid].min())
        g_max_c = float(gaps[valid].max())
        popt = fit_morse(gaps, e)
        if popt is not None:
            y = morse(g_csv, *popt)
        else:
            cs = CubicSpline(gaps[valid], e[valid])
            y = gaussian_filter1d(cs(g_csv), sigma=10)
        # Mask to source data range (avoid extrapolation artifacts)
        y = np.where((g_csv >= g_min_c) & (g_csv <= g_max_c), y, np.nan)
        smooth_curves[c] = y
    csv_out = OUT_DIR / "figure_v8_morse_smooth.csv"
    with open(csv_out, 'w', encoding='utf-8') as f:
        f.write("# Morse-fit smoothed binding curves from "
                f"{CSV_PATH}\n")
        f.write("# E_adh = D*(1-exp(-a*(d-d_eq)))^2 - D + offset, J/m^2\n")
        f.write("# Step 0.02 A, range matched to source CSV\n")
        f.write("gap_A," + ",".join(c for c in PAPER_COMPS if c in smooth_curves) + "\n")
        for i, g in enumerate(g_csv):
            row = [f"{g:.3f}"]
            for c in PAPER_COMPS:
                if c in smooth_curves:
                    v = smooth_curves[c][i]
                    row.append(f"{v:+.6f}" if not np.isnan(v) else "")
            f.write(",".join(row) + "\n")
    print(f"saved {png}")
    print(f"saved {pdf}")
    print(f"saved {csv_out}\n")
    print(f"{'comp':<8} {'well depth':>10} {'fit':<40}")
    for c in PAPER_COMPS:
        if c in well_depths:
            print(f"{c:<8} {well_depths[c]:>+10.3f}  {fit_method[c]}")
    print(f"\nR(well depth vs paper exp Wad) = {R:+.4f}")


if __name__ == "__main__":
    main()

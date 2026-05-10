"""Plot Figure 1 in image-2 style — smooth Wad curves, 5 paper comps, R in title.

Reads phase1_results/binding_curves.json (with comp4 v2 swap merged) and
produces the same visual layout as the original "UMA binding curves
(R = +0.925)" figure:
  - Sign convention: E_adh = -Wad (negative = binding well)
  - 5 paper comps only (no modelC)
  - Mean over 36 xy-shift registries
  - Asymptote-subtracted to match original figure look
  - Cubic spline smoothed, markers at data points
  - Gray gap_eq window 1.2-1.6 Å
  - R value in title

Usage:
    python3 plot_figure_image2_style.py

Inputs:  phase1_results/binding_curves.json
Outputs: binding_curves_plots/figure_image2_style_v2.{png,pdf}
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

DATA = Path("phase1_results/binding_curves.json")
OUT_DIR = Path("binding_curves_plots"); OUT_DIR.mkdir(exist_ok=True)

PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']

# Image 2 style: colors + markers
COLORS = {
    'comp1':  '#1f77b4', 'comp2':  '#17becf',
    'comp3':  '#d62728', 'comp4':  '#9467bd', 'comp5':  '#2ca02c',
}
MARKERS = {'comp1':'s', 'comp2':'o', 'comp3':'^', 'comp4':'D', 'comp5':'v'}
LABELS = {
    'comp1':  r'comp1: Li$_6$PS$_5$Cl',
    'comp2':  r'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$',
    'comp3':  r'comp3: Li$_{5.4}$PS$_{4.4}$Cl$_{1.0}$Br$_{0.6}$',
    'comp4':  r'comp4: Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$',
    'comp5':  r'comp5: Li$_{5.4}$PS$_{4.4}$Cl$_{0.6}$Br$_{1.0}$',
}


def main():
    raw = json.load(open(DATA))

    # Compute mean Wad over 36 registries per (comp, gap)
    summary = {}
    for c in PAPER_COMPS:
        regs = raw[c]
        # all gap values from R1_origin
        gaps_str = list(regs['R1_origin']['curve'].keys())
        gaps = np.array([float(g) for g in gaps_str])

        # mean over registries
        mean_wads = []
        for g in gaps_str:
            vals = [regs[r]['curve'][g]['Wad_J_per_m2'] for r in regs]
            mean_wads.append(np.mean(vals))
        mean_wads = np.array(mean_wads)

        # asymptote = mean of gap ≥ 3.0 (matches original protocol)
        asymp_mask = gaps >= 3.0
        W_asymp = float(np.mean(mean_wads[asymp_mask]))

        # E_adh in image-2 convention: -(Wad - asymp) → negative = binding
        E_adh = -(mean_wads - W_asymp)

        # Well minimum (most negative E_adh in binding region 1.0-2.5)
        binding_mask = (gaps >= 1.0) & (gaps <= 2.5)
        idx_min = np.argmin(E_adh[binding_mask])
        E_well = float(E_adh[binding_mask][idx_min])
        d_min = float(gaps[binding_mask][idx_min])

        summary[c] = {'gaps': gaps, 'mean_wads': mean_wads,
                       'E_adh': E_adh, 'W_asymp': W_asymp,
                       'E_well': E_well, 'd_min': d_min}

    # Pearson R: well depth (= -E_well, positive number) vs paper exp
    x_R = [-summary[c]['E_well'] for c in PAPER_COMPS]
    y_R = [PAPER_EXP[c] for c in PAPER_COMPS]
    R = float(np.corrcoef(x_R, y_R)[0, 1])

    # === Plot — image 2 style ===
    plt.rcParams.update({
        'font.size': 13, 'axes.labelsize': 15, 'axes.titlesize': 16,
        'xtick.labelsize': 12, 'ytick.labelsize': 12, 'legend.fontsize': 11,
        'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
    })

    fig, ax = plt.subplots(figsize=(11, 7.5))

    GAP_LO, GAP_HI = 0.8, 4.0
    gap_dense = np.linspace(GAP_LO, GAP_HI, 250)

    for c in PAPER_COMPS:
        d = summary[c]
        mask = (d['gaps'] >= GAP_LO) & (d['gaps'] <= GAP_HI)
        gaps_z = d['gaps'][mask]
        E = d['E_adh'][mask]
        cs = CubicSpline(gaps_z, E)
        ax.plot(gap_dense, cs(gap_dense), '-', color=COLORS[c],
                lw=3.0, alpha=0.95, zorder=5)
        ax.plot(gaps_z, E, MARKERS[c], color=COLORS[c],
                ms=9, mec='k', mew=0.5, label=LABELS[c], zorder=10)

    ax.axvspan(1.2, 1.6, alpha=0.15, color='gray', zorder=1)
    ax.axhline(0, color='k', lw=0.7, alpha=0.7, zorder=2)

    ax.set_xlabel(r'Interface gap, $d$ (Å)')
    ax.set_ylabel(r'Adhesion energy (J m$^{-2}$)')
    ax.set_title(f'UMA binding curves (R = {R:+.3f})  —  comp4 v2 anneal champion')
    ax.set_xlim(GAP_LO, GAP_HI)
    ax.grid(alpha=0.25)
    ax.legend(loc='lower right')

    fig.tight_layout()
    fig.savefig(OUT_DIR / "figure_image2_style_v2.png")
    fig.savefig(OUT_DIR / "figure_image2_style_v2.pdf")
    plt.close()
    print(f"R(well depth vs paper) = {R:+.4f}")
    print(f"saved binding_curves_plots/figure_image2_style_v2.{{png,pdf}}")
    print(f"\n{'comp':<8} {'asymp_Wad':>10} {'E_well':>10} {'d_min':>7} {'paper':>6}")
    for c in PAPER_COMPS:
        d = summary[c]
        print(f"{c:<8} {d['W_asymp']:>+10.4f} {d['E_well']:>+10.4f} {d['d_min']:>7.2f} {PAPER_EXP[c]:>6}")


if __name__ == '__main__':
    main()

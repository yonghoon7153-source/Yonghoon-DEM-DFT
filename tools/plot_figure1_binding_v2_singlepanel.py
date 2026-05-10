"""Figure 1 v2 — single panel, original figure style.

Recreates user's "UMA binding curves (R=+0.925)" figure with comp4 v2 anneal
champion. Single panel, asymptote-subtracted (-ΔW) so wells are visible
against zero baseline. Smooth cubic interpolation. Gray gap_eq window.

Outputs:
  output/comp4_v2_adhesion/figures/figure1_binding_v2_singlepanel.{png,pdf}
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

OUT_DIR = Path("output/comp4_v2_adhesion/figures")
DATA = Path("output/comp4_v2_adhesion/v30u_v2_curves.json")

PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']

# Original figure colors + markers
COLORS = {
    'comp1':  '#1f77b4',  # blue
    'comp2':  '#17becf',  # cyan
    'comp3':  '#d62728',  # red
    'comp4':  '#9467bd',  # purple
    'comp5':  '#2ca02c',  # green
}
MARKERS = {'comp1':'s', 'comp2':'o', 'comp3':'^', 'comp4':'D', 'comp5':'v'}
LABELS = {
    'comp1':  r'comp1: Li$_6$PS$_5$Cl',
    'comp2':  r'comp2: Li$_6$PS$_5$Cl$_{0.5}$Br$_{0.5}$',
    'comp3':  r'comp3: Li$_{5.4}$PS$_{4.4}$Cl$_{1.0}$Br$_{0.6}$',
    'comp4':  r'comp4: Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$ (v2)',
    'comp5':  r'comp5: Li$_{5.4}$PS$_{4.4}$Cl$_{0.6}$Br$_{1.0}$',
}
ORDER = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']  # original figure order


def main():
    raw = json.load(open(DATA))

    # Compute summary + R
    summary = {}
    for c in raw:
        arr = np.array(raw[c])
        gaps, wads = arr[:, 0], arr[:, 1]
        i_max = int(np.argmax(wads))
        summary[c] = {'gaps': gaps, 'wads': wads,
                       'W_max': float(wads[i_max]),
                       'd_min': float(gaps[i_max]),
                       'W_asymp': float(np.mean(wads[-5:]))}

    x_R = [summary[c]['W_max'] for c in PAPER_COMPS]
    y_R = [PAPER_EXP[c] for c in PAPER_COMPS]
    R = float(np.corrcoef(x_R, y_R)[0, 1])

    # Single panel, original figure style
    plt.rcParams.update({
        'font.size': 13, 'axes.labelsize': 14, 'axes.titlesize': 14,
        'xtick.labelsize': 12, 'ytick.labelsize': 12, 'legend.fontsize': 11,
        'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
        'lines.linewidth': 2.0,
    })

    fig, ax = plt.subplots(figsize=(11, 7))

    # Restrict to gap 0.8-4.0 (matching original figure x-range)
    GAP_LO, GAP_HI = 0.8, 4.0
    gap_dense = np.linspace(GAP_LO, GAP_HI, 200)

    for c in ORDER:
        d = summary[c]
        mask = (d['gaps'] >= GAP_LO) & (d['gaps'] <= GAP_HI)
        gaps_z = d['gaps'][mask]
        # Figure convention: E_adh = -(W - W_asymp)
        # negative = binding (well below baseline)
        E_adh = -(d['wads'][mask] - d['W_asymp'])
        # smooth cubic spline
        cs = CubicSpline(gaps_z, E_adh)
        ax.plot(gap_dense, cs(gap_dense), '-', color=COLORS[c],
                lw=2.5, alpha=0.95, zorder=5)
        ax.plot(gaps_z, E_adh, MARKERS[c], color=COLORS[c],
                ms=8, mec='k', mew=0.5, label=LABELS[c], zorder=10)

    # Gray gap_eq window
    ax.axvspan(1.2, 1.6, alpha=0.13, color='gray', zorder=1)
    ax.axhline(0, color='k', lw=0.7, alpha=0.7, zorder=2)

    ax.set_xlabel(r'Interface gap, $d$ (Å)', fontsize=14)
    ax.set_ylabel(r'Adhesion energy (J m$^{-2}$)', fontsize=14)
    ax.set_title(f'UMA binding curves v2 (R = {R:+.3f})', fontsize=14)
    ax.set_xlim(GAP_LO, GAP_HI)
    ax.grid(alpha=0.25)
    ax.legend(loc='lower right', fontsize=11, framealpha=0.95)

    fig.tight_layout()
    fig.savefig(OUT_DIR / "figure1_binding_v2_singlepanel.png")
    fig.savefig(OUT_DIR / "figure1_binding_v2_singlepanel.pdf")
    plt.close()
    print(f"R(W_max vs paper exp) = {R:+.4f}")
    print(f"saved figure1_binding_v2_singlepanel.png/pdf")
    print(f"\nWell depths (E_adh at minimum):")
    for c in ORDER:
        d = summary[c]
        depth = -(d['W_max'] - d['W_asymp'])
        print(f"  {c}: d_min={d['d_min']:.2f} A, depth={depth:+.3f} J/m^2  (paper Wad={PAPER_EXP[c]})")


if __name__ == '__main__':
    main()

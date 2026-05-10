"""Figure 1 v2 — single panel, original figure style (RAW -W, no asymptote subtract).

Recreates user's original "UMA binding curves (R=+0.925)" figure with comp4
v2 anneal champion. Style:
  - Raw E_adh = -W (figure convention, NOT asymptote-subtracted)
  - Asymptotes are real (Li6 positive, Li5.4 negative — natural spread)
  - 5 paper comps only (modelC excluded)
  - Smooth cubic spline + symbols at data points
  - Gray gap_eq window 1.2-1.6
  - Y-axis auto-scaled to data

Note: absolute scale ~8-10x larger than user's original figure (UMA-s-1p1 +
3L conv NCM vs paper-figure UMA + 1L NCM). Visual STYLE matches original.

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
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']  # paper comps only

# Original figure colors + markers (5 paper comps)
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
    'comp4':  r'comp4: Li$_{5.4}$PS$_{4.4}$Cl$_{0.8}$Br$_{0.8}$',
    'comp5':  r'comp5: Li$_{5.4}$PS$_{4.4}$Cl$_{0.6}$Br$_{1.0}$',
}


def main():
    raw = json.load(open(DATA))

    summary = {}
    for c in PAPER_COMPS:
        arr = np.array(raw[c])
        gaps, wads = arr[:, 0], arr[:, 1]
        i_max = int(np.argmax(wads))
        summary[c] = {'gaps': gaps, 'wads': wads,
                       'W_max': float(wads[i_max]),
                       'd_min': float(gaps[i_max])}

    x_R = [summary[c]['W_max'] for c in PAPER_COMPS]
    y_R = [PAPER_EXP[c] for c in PAPER_COMPS]
    R = float(np.corrcoef(x_R, y_R)[0, 1])

    plt.rcParams.update({
        'font.size': 14, 'axes.labelsize': 15, 'axes.titlesize': 15,
        'xtick.labelsize': 13, 'ytick.labelsize': 13, 'legend.fontsize': 12,
        'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
        'lines.linewidth': 2.5,
    })

    fig, ax = plt.subplots(figsize=(11, 7.5))

    GAP_LO, GAP_HI = 0.8, 4.0
    gap_dense = np.linspace(GAP_LO, GAP_HI, 200)

    for c in PAPER_COMPS:
        d = summary[c]
        mask = (d['gaps'] >= GAP_LO) & (d['gaps'] <= GAP_HI)
        gaps_z = d['gaps'][mask]
        # Original figure convention: E_adh = -W (RAW, no asymptote subtract)
        E_adh = -d['wads'][mask]
        cs = CubicSpline(gaps_z, E_adh)
        ax.plot(gap_dense, cs(gap_dense), '-', color=COLORS[c],
                lw=2.5, alpha=0.95, zorder=5)
        ax.plot(gaps_z, E_adh, MARKERS[c], color=COLORS[c],
                ms=9, mec='k', mew=0.5, label=LABELS[c], zorder=10)

    ax.axvspan(1.2, 1.6, alpha=0.13, color='gray', zorder=1)
    ax.axhline(0, color='k', lw=0.7, alpha=0.7, zorder=2)

    ax.set_xlabel(r'Interface gap, $d$ (Å)', fontsize=15)
    ax.set_ylabel(r'Adhesion energy (J m$^{-2}$)', fontsize=15)
    ax.set_title(f'UMA binding curves v2 (R = {R:+.3f})', fontsize=15)
    ax.set_xlim(GAP_LO, GAP_HI)
    ax.grid(alpha=0.25)
    ax.legend(loc='lower right', fontsize=11, framealpha=0.95)

    fig.tight_layout()
    fig.savefig(OUT_DIR / "figure1_binding_v2_singlepanel.png")
    fig.savefig(OUT_DIR / "figure1_binding_v2_singlepanel.pdf")
    plt.close()
    print(f"R(W_max vs paper exp) = {R:+.4f}")
    print(f"saved figure1_binding_v2_singlepanel.png/pdf")
    print(f"\nE_adh = -W (raw, figure convention) values:")
    print(f"{'comp':<8} {'asymp(d=4)':>11} {'min':>8} {'d_min':>7} {'paper':>6}")
    for c in PAPER_COMPS:
        d = summary[c]
        # asymp at gap=4 (figure x-range max)
        idx_asymp = np.argmin(np.abs(d['gaps'] - 4.0))
        E_asymp = -d['wads'][idx_asymp]
        E_min = -d['W_max']
        print(f"{c:<8} {E_asymp:>+11.3f} {E_min:>+8.3f} {d['d_min']:>7.2f} {PAPER_EXP[c]:>6}")


if __name__ == '__main__':
    main()

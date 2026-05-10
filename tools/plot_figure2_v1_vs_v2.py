"""Figure 2 v1 vs v2 side-by-side comparison.

Shows how comp4 v2 anneal champion changes the bond density picture:
- LEFT panel: v1 (paper figure) — comp4 has Cl-O = 0
- RIGHT panel: v2 — comp4 Cl exposed (Cl-O = 0.088), Li-O / Br-O dropped

Other 5 comps unchanged (verified by v15 v1_REDO comparison).

Outputs:
  output/comp4_v2_adhesion/figures/figure2_v1_vs_v2_side_by_side.{png,pdf}
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path("output/comp4_v2_adhesion/figures")
ALL_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}

# v1 (KISTI v15 v1_REDO results — comp4 with v1 slab in same env)
BOND_V1 = {
    'comp1':  {'Li-O': 0.1147, 'Cl-O': 0.0247, 'Br-O': 0.0000},
    'comp2':  {'Li-O': 0.0759, 'Cl-O': 0.0292, 'Br-O': 0.0000},
    'comp3':  {'Li-O': 0.1372, 'Cl-O': 0.0000, 'Br-O': 0.0000},
    'comp4':  {'Li-O': 0.1245, 'Cl-O': 0.0000, 'Br-O': 0.1083},  # v1 slab
    'comp5':  {'Li-O': 0.1256, 'Cl-O': 0.0000, 'Br-O': 0.1078},
    'modelC': {'Li-O': 0.0853, 'Cl-O': 0.0881, 'Br-O': 0.0000},
}
# v2 — only comp4 differs (v2 anneal champion slab)
BOND_V2 = {
    'comp1':  {'Li-O': 0.1147, 'Cl-O': 0.0247, 'Br-O': 0.0000},
    'comp2':  {'Li-O': 0.0759, 'Cl-O': 0.0292, 'Br-O': 0.0000},
    'comp3':  {'Li-O': 0.1372, 'Cl-O': 0.0000, 'Br-O': 0.0000},
    'comp4':  {'Li-O': 0.0761, 'Cl-O': 0.0881, 'Br-O': 0.0502},  # v2 anneal champion
    'comp5':  {'Li-O': 0.1256, 'Cl-O': 0.0000, 'Br-O': 0.1078},
    'modelC': {'Li-O': 0.0853, 'Cl-O': 0.0881, 'Br-O': 0.0000},
}

LABELS_SHORT = {
    'comp1':  r'LPSC$_{1.0}$',     'comp2':  r'LPSC$_{0.5}$B$_{0.5}$',
    'comp3':  r'LPSC$_{1.0}$B$_{0.6}$', 'comp4':  r'LPSC$_{0.8}$B$_{0.8}$',
    'comp5':  r'LPSC$_{0.6}$B$_{1.0}$', 'modelC': r'LPSC$_{1.6}$',
}
BOND_COLORS = {'Li-O': '#3477eb', 'Cl-O': '#d62728', 'Br-O': '#2ca02c'}
BOND_LABELS = {
    'Li-O': 'Li-O (attractive)', 'Cl-O': 'Cl-O (small anion)', 'Br-O': 'Br-O (large anion)',
}

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 11, 'axes.titlesize': 12,
    'xtick.labelsize': 9, 'ytick.labelsize': 9, 'legend.fontsize': 8,
    'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
})


def pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if x.std() == 0 or y.std() == 0:
        return float('nan')
    return float(np.corrcoef(x, y)[0, 1])


def plot_panel(ax, ax2, BOND, label):
    x = np.arange(len(ALL_COMPS))
    width = 0.27
    R = {}
    for i, bond in enumerate(['Li-O', 'Cl-O', 'Br-O']):
        vals = [BOND[c][bond] for c in ALL_COMPS]
        ax.bar(x + (i - 1) * width, vals, width, color=BOND_COLORS[bond],
               label=BOND_LABELS[bond], edgecolor='k', linewidth=0.5, alpha=0.85)
        for j, v in enumerate(vals):
            if v > 0.005:
                ax.text(x[j] + (i-1)*width, v + 0.002, f'{v:.3f}',
                        ha='center', fontsize=6, color=BOND_COLORS[bond])
        # R
        xv = [BOND[c][bond] for c in PAPER_COMPS]
        yv = [PAPER_EXP[c] for c in PAPER_COMPS]
        R[bond] = pearson(xv, yv)
    ax.set_xticks(x)
    ax.set_xticklabels([LABELS_SHORT[c] for c in ALL_COMPS], rotation=18, ha='right')
    ax.set_ylim(0, 0.18)
    ax.set_ylabel(r'Bond density (Å$^{-2}$)')
    ax.grid(axis='y', alpha=0.3)
    # family separators
    ax.axvline(1.5, color='gray', linestyle=':', alpha=0.5)
    ax.axvline(4.5, color='gray', linestyle=':', alpha=0.5)
    R_str = "  ".join([f"R({b})={R[b]:+.2f}" for b in ['Li-O','Cl-O','Br-O']])
    ax.set_title(f"{label}\n{R_str}", fontsize=11)
    # paper Wad on secondary axis
    yWad = [PAPER_EXP.get(c, np.nan) for c in ALL_COMPS]
    ax2.plot(x, yWad, 'ko-', mfc='white', ms=8, lw=1.2,
             label=r'Paper exp $W_{ad}$ (mJ/m$^2$)', zorder=10)
    for i, (c, y) in enumerate(zip(ALL_COMPS, yWad)):
        if not np.isnan(y):
            ax2.text(i, y + 10, f'{int(y)}', ha='center', fontsize=8, fontweight='bold')
    ax2.set_ylim(0, 380)
    ax2.set_ylabel(r'Paper exp $W_{ad}$ (mJ/m$^2$)')


def main():
    fig, axes = plt.subplots(1, 2, figsize=(16, 5.5), sharey=True)
    ax2_left = axes[0].twinx()
    ax2_right = axes[1].twinx()

    plot_panel(axes[0], ax2_left, BOND_V1, 'v1 (paper figure baseline) — comp4 = v1 slab')
    plot_panel(axes[1], ax2_right, BOND_V2, 'v2 — comp4 = v2 anneal champion (Cl exposed)')

    # combined legend on right panel
    h1, l1 = axes[1].get_legend_handles_labels()
    h2, l2 = ax2_right.get_legend_handles_labels()
    axes[1].legend(h1 + h2, l1 + l2, loc='upper left', fontsize=8, framealpha=0.95)

    fig.suptitle('Figure 2 — Interface bond densities at gap$_{eq}$: v1 (left) vs v2 anneal champion (right)\n'
                 'comp4 only changes — Cl-O classifier (R=-0.91) breaks; Li-O/Br-O drop',
                 fontsize=12, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "figure2_v1_vs_v2_side_by_side.png")
    fig.savefig(OUT_DIR / "figure2_v1_vs_v2_side_by_side.pdf")
    plt.close()
    print(f"saved figure2_v1_vs_v2_side_by_side.png/pdf")


if __name__ == '__main__':
    main()

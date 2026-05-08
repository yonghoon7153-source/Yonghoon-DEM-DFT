"""Phase 2a v8 — Cl surface fraction descriptor figure.

This descriptor distinguishes comp4 vs comp5 in the SAME direction as
paper experimental Wad, unlike Cl-O density (which gives 0/0/0 for
Li5.4 mix family).

Data (from v25 Y2 halogen z-distribution, top + bottom 20% of SE slab):
  comp1: 42%  (paper Wad 194 - low)
  comp2: 33%  (paper 180 - lowest)
  comp3: 20%  (paper 316 - highest) ⭐
  comp4: 25%  (paper 298)
  comp5: 33%  (paper 249)
  modelC: 38% (no paper exp - predicted Li6-level)

Inverse correlation expected: less Cl at surface → less anion-O Coulomb
repulsion → higher Wad.

Outputs:
  cl_surface_bar.pdf/png        bar chart paper exp + Cl_surface
  cl_surface_scatter.pdf/png    scatter Cl_surface vs paper Wad
  cl_surface_summary.csv        per-comp values
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path("binding_curves_plots"); OUT_DIR.mkdir(exist_ok=True)

ALL_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']

# Cl surface fraction (top + bottom 20% of SE slab, from v25 Y2)
CL_SURFACE = {'comp1': 42, 'comp2': 33, 'comp3': 20, 'comp4': 25, 'comp5': 33, 'modelC': 38}

# Paper experimental Wad (mJ/m²)
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}

LABELS_SHORT = {
    'comp1':  'LPSC$_{1.0}$',
    'comp2':  'LPSC$_{0.5}$B$_{0.5}$',
    'comp3':  'LPSC$_{1.0}$B$_{0.6}$',
    'comp4':  'LPSC$_{0.8}$B$_{0.8}$',
    'comp5':  'LPSC$_{0.6}$B$_{1.0}$',
    'modelC': 'LPSC$_{1.6}$',
}
COLORS = {
    'comp1':  '#1f77b4',  'comp2':  '#17becf',
    'comp3':  '#d62728',  'comp4':  '#9467bd', 'comp5':  '#2ca02c',
    'modelC': '#ff7f0e',
}

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 12,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 9,
    'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
})


def main():
    # CSV
    csv_path = OUT_DIR / "cl_surface_summary.csv"
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("comp,formula_short,Cl_surface_pct,paper_Wad_mJ_m2\n")
        for c in ALL_COMPS:
            pe = PAPER_EXP.get(c, '')
            f.write(f"{c},{LABELS_SHORT[c]},{CL_SURFACE[c]},{pe}\n")
    print(f"  saved {csv_path}")

    # Compute R (paper comps only)
    x = [CL_SURFACE[c] for c in PAPER_COMPS]
    y = [PAPER_EXP[c] for c in PAPER_COMPS]
    R = float(np.corrcoef(x, y)[0, 1])
    print(f"\n  R(Cl_surface vs paper Wad, n=5) = {R:+.4f}")

    # ── Figure 1: 2-panel bar (paper exp left, Cl_surface right) ──
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    comps_plot = PAPER_COMPS
    x_pos = np.arange(len(comps_plot))
    cols = [COLORS[c] for c in comps_plot]

    ax = axes[0]
    y_exp = [PAPER_EXP[c] for c in comps_plot]
    ax.bar(x_pos, y_exp, color=cols, alpha=0.7, edgecolor='k', linewidth=0.8)
    for xi, yi in zip(x_pos, y_exp):
        ax.text(xi, yi + 5, f'{yi}', ha='center', va='bottom', fontsize=10)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([LABELS_SHORT[c] for c in comps_plot], rotation=30, ha='right', fontsize=9)
    ax.set_ylabel(r'Experimental $W_{ad}$ (mJ/m$^2$)', fontsize=12)
    ax.set_title('(a) Paper experimental Wad', fontsize=11)
    ax.set_ylim(0, max(y_exp)*1.2)
    ax.grid(axis='y', alpha=0.3)

    ax = axes[1]
    y_calc = [CL_SURFACE[c] for c in comps_plot]
    ax.bar(x_pos, y_calc, color=cols, alpha=0.7, edgecolor='k', linewidth=0.8)
    for xi, yi in zip(x_pos, y_calc):
        ax.text(xi, yi + 1, f'{yi}%', ha='center', va='bottom', fontsize=10)
    ax.set_xticks(x_pos)
    ax.set_xticklabels([LABELS_SHORT[c] for c in comps_plot], rotation=30, ha='right', fontsize=9)
    ax.set_ylabel('Cl surface exposure (%)', fontsize=12)
    ax.set_title('(b) Cl in top + bottom 20% of SE slab', fontsize=11)
    ax.set_ylim(0, 50)
    ax.grid(axis='y', alpha=0.3)
    ax.invert_yaxis()  # invert so high Cl = bottom (low Wad)

    fig.suptitle(f'Cl surface fraction inversely tracks paper Wad (R = {R:+.3f})',
                 fontsize=11, y=1.00)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "cl_surface_bar.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "cl_surface_bar.png", bbox_inches='tight')
    plt.close()
    print(f"  saved cl_surface_bar.pdf/png")

    # ── Figure 2: Scatter ──
    fig, ax = plt.subplots(figsize=(6.5, 5))
    for c in PAPER_COMPS:
        ax.scatter(CL_SURFACE[c], PAPER_EXP[c], color=COLORS[c], s=160,
                   edgecolor='k', linewidth=1.2, zorder=10)
        ax.annotate(LABELS_SHORT[c], (CL_SURFACE[c], PAPER_EXP[c]),
                    xytext=(8, 6), textcoords='offset points', fontsize=9)
    if 'modelC' in CL_SURFACE:
        # modelC predicted point — use linear fit
        coef = np.polyfit(x, y, 1)
        mc_pred = float(np.polyval(coef, CL_SURFACE['modelC']))
        ax.scatter(CL_SURFACE['modelC'], mc_pred, color=COLORS['modelC'], s=160,
                   marker='^', edgecolor='k', linewidth=1.2, zorder=10,
                   label=f'modelC predicted: {mc_pred:.0f} mJ/m²')
        ax.annotate(f'modelC\npred={mc_pred:.0f}', (CL_SURFACE['modelC'], mc_pred),
                    xytext=(10, -15), textcoords='offset points', fontsize=9)
    coef = np.polyfit(x, y, 1)
    xfit = np.linspace(15, 45, 50)
    ax.plot(xfit, np.polyval(coef, xfit), 'k--', lw=1, alpha=0.6,
            label=f'Linear fit (R = {R:+.3f}, n=5)')
    ax.set_xlabel('Cl surface exposure (%)', fontsize=12)
    ax.set_ylabel(r'Paper exp $W_{ad}$ (mJ/m$^2$)', fontsize=12)
    ax.set_title('Cl surface fraction vs experimental adhesion', fontsize=11)
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "cl_surface_scatter.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "cl_surface_scatter.png", bbox_inches='tight')
    plt.close()
    print(f"  saved cl_surface_scatter.pdf/png  (R = {R:+.3f})")

    print(f"\nAll outputs in: {OUT_DIR.resolve()}")
    print(f"\n--- Per-comp values ---")
    print(f"{'comp':<8} {'Cl_surf':>8} {'paper_Wad':>10}")
    for c in ALL_COMPS:
        pe = PAPER_EXP.get(c, '—')
        print(f"  {c:<8} {CL_SURFACE[c]:>7d}% {str(pe):>10}")


if __name__ == "__main__":
    main()

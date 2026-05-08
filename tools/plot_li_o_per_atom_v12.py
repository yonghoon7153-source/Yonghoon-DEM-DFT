"""Phase 2a v12 — Li-O per total atom scatter (best single descriptor R=+0.93).

v10 found that Li-O bond density / total slab atom count gives R = +0.930
with paper exp Wad — strongest single descriptor in our framework.

This script makes a clean scatter (paper-quality) with linear fit + modelC
prediction point.

Output:
  li_o_per_atom_scatter.pdf/png   main result scatter
  li_o_per_atom_summary.csv       per-comp values
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path("binding_curves_plots"); OUT_DIR.mkdir(exist_ok=True)
ALL_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}

# Li-O density (Å^-2) at gap_eq, 36-reg mean
LI_O_DENS = {'comp1': 0.1138, 'comp2': 0.0740, 'comp3': 0.1338,
             'comp4': 0.1338, 'comp5': 0.1283, 'modelC': 0.0948}
# Total slab atoms
N_ATOMS = {'comp1': 624, 'comp2': 624, 'comp3': 248, 'comp4': 248,
           'comp5': 248, 'modelC': 248}

LABELS_SHORT = {
    'comp1':  'LPSC$_{1.0}$', 'comp2':  'LPSC$_{0.5}$B$_{0.5}$',
    'comp3':  'LPSC$_{1.0}$B$_{0.6}$', 'comp4':  'LPSC$_{0.8}$B$_{0.8}$',
    'comp5':  'LPSC$_{0.6}$B$_{1.0}$', 'modelC': 'LPSC$_{1.6}$',
}
COLORS = {
    'comp1':  '#1f77b4', 'comp2':  '#17becf',
    'comp3':  '#d62728', 'comp4':  '#9467bd', 'comp5':  '#2ca02c',
    'modelC': '#ff7f0e',
}

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 12,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 9,
    'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
})


def main():
    # Compute Li-O per total atom × 100 (%)
    li_o_per_atom = {c: LI_O_DENS[c] / N_ATOMS[c] * 100 for c in ALL_COMPS}

    # CSV
    csv_path = OUT_DIR / "li_o_per_atom_summary.csv"
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("comp,formula,Li-O_density,N_atoms,Li-O_per_atom_pct,paper_Wad\n")
        for c in ALL_COMPS:
            pe = PAPER_EXP.get(c, '')
            f.write(f"{c},{LABELS_SHORT[c]},{LI_O_DENS[c]:.4f},{N_ATOMS[c]},"
                    f"{li_o_per_atom[c]:.6f},{pe}\n")
    print(f"  saved {csv_path}")

    # Pearson R
    x = [li_o_per_atom[c] for c in PAPER_COMPS]
    y = [PAPER_EXP[c] for c in PAPER_COMPS]
    R = float(np.corrcoef(x, y)[0, 1])
    print(f"\n  R(Li-O per atom vs paper Wad, n=5) = {R:+.4f}")

    # Spearman
    def rank(arr):
        return [sorted(arr).index(v) for v in arr]
    rx = rank(x); ry = rank(y)
    n = len(x); sum_d2 = sum((rx[i]-ry[i])**2 for i in range(n))
    rho = 1 - 6*sum_d2/(n*(n**2-1))
    print(f"  Spearman ρ = {rho:+.3f}")

    # Linear fit
    coef = np.polyfit(x, y, 1)
    mc_pred = float(np.polyval(coef, li_o_per_atom['modelC']))
    print(f"  modelC predicted Wad = {mc_pred:.0f} mJ/m²")

    # ── Plot ──
    fig, ax = plt.subplots(figsize=(7, 5.5))
    for c in PAPER_COMPS:
        ax.scatter(li_o_per_atom[c], PAPER_EXP[c], color=COLORS[c], s=180,
                   edgecolor='k', linewidth=1.2, zorder=10)
        ax.annotate(LABELS_SHORT[c], (li_o_per_atom[c], PAPER_EXP[c]),
                    xytext=(8, 6), textcoords='offset points', fontsize=10)

    # modelC predicted point
    ax.scatter(li_o_per_atom['modelC'], mc_pred, color=COLORS['modelC'], s=180,
               marker='^', edgecolor='k', linewidth=1.2, zorder=10,
               label=f'modelC predicted Wad = {mc_pred:.0f}')
    ax.annotate(f'modelC\npred={mc_pred:.0f}',
                (li_o_per_atom['modelC'], mc_pred),
                xytext=(8, -16), textcoords='offset points', fontsize=9)

    # Linear fit line
    xfit = np.linspace(min(x) - 0.005, max(x) + 0.01, 50)
    ax.plot(xfit, np.polyval(coef, xfit), 'k--', lw=1, alpha=0.6,
            label=f'Linear fit (R = {R:+.3f}, n=5)')

    ax.set_xlabel(r'Li-O bond density / total slab atoms (%)', fontsize=12)
    ax.set_ylabel(r'Paper experimental $W_{ad}$ (mJ/m²)', fontsize=12)
    ax.set_title('Li-O surface contact density predicts adhesion ranking',
                 fontsize=11)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "li_o_per_atom_scatter.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "li_o_per_atom_scatter.png", bbox_inches='tight')
    plt.close()
    print(f"  saved li_o_per_atom_scatter.pdf/png")

    # ── Print summary ──
    print(f"\n--- Per-comp values ---")
    print(f"{'comp':<8} {'Li-O_dens':>10} {'N_atoms':>8} {'per_atom%':>10} {'paper_Wad':>10}")
    for c in ALL_COMPS:
        pe = PAPER_EXP.get(c, '—')
        print(f"  {c:<8} {LI_O_DENS[c]:>10.4f} {N_ATOMS[c]:>8d} "
              f"{li_o_per_atom[c]:>10.6f} {str(pe):>10}")


if __name__ == "__main__":
    main()

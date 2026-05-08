"""Phase 2a v9 — All three bond densities (Cl-O, Li-O, Br-O) at gap_eq.

Shows full picture instead of just Cl-O. Helps clarify:
- Cl-O: Li5.4 mix family all 0 (binary classifier)
- Li-O: relatively constant across comps (~0.1)
- Br-O: only nonzero for Br-containing comps (comp2, 4, 5)

Per-comp data from v15 (gap_eq, 36 reg mean):
  comp1:  Li-O=0.1138, Cl-O=0.0228, Br-O=0
  comp2:  Li-O=0.0740, Cl-O=0.0285, Br-O=0  (Br-O appears in some calcs)
  comp3:  Li-O=0.1338, Cl-O=0.0000, Br-O=0
  comp4:  Li-O=0.1338, Cl-O=0.0000, Br-O=0.1115
  comp5:  Li-O=0.1283, Cl-O=0.0000, Br-O=0.1060
  modelC: Li-O=0.0948, Cl-O=0.0948, Br-O=0

Outputs:
  bond_density_grouped_bar.pdf/png   3 bond types × 6 comps grouped bars
  bond_density_with_wad.pdf/png       above + paper exp Wad on secondary axis
  bond_density_summary.csv            full table
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path("binding_curves_plots"); OUT_DIR.mkdir(exist_ok=True)

ALL_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']

# v15 data (gap_eq, 36-reg mean)
BOND_DATA = {
    'comp1':  {'Li-O': 0.1138, 'Cl-O': 0.0228, 'Br-O': 0.0000},
    'comp2':  {'Li-O': 0.0740, 'Cl-O': 0.0285, 'Br-O': 0.0000},
    'comp3':  {'Li-O': 0.1338, 'Cl-O': 0.0000, 'Br-O': 0.0000},
    'comp4':  {'Li-O': 0.1338, 'Cl-O': 0.0000, 'Br-O': 0.1115},
    'comp5':  {'Li-O': 0.1283, 'Cl-O': 0.0000, 'Br-O': 0.1060},
    'modelC': {'Li-O': 0.0948, 'Cl-O': 0.0948, 'Br-O': 0.0000},
}

PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}

LABELS_SHORT = {
    'comp1':  'LPSC$_{1.0}$',
    'comp2':  'LPSC$_{0.5}$B$_{0.5}$',
    'comp3':  'LPSC$_{1.0}$B$_{0.6}$',
    'comp4':  'LPSC$_{0.8}$B$_{0.8}$',
    'comp5':  'LPSC$_{0.6}$B$_{1.0}$',
    'modelC': 'LPSC$_{1.6}$',
}
BOND_COLORS = {
    'Li-O': '#3477eb',  # blue (attractive cation-anion)
    'Cl-O': '#d62728',  # red (repulsive anion-anion small)
    'Br-O': '#2ca02c',  # green (repulsive anion-anion large)
}
BOND_LABELS = {
    'Li-O': r'Li-O (attractive, cation-anion)',
    'Cl-O': r'Cl-O (repulsive, small anion)',
    'Br-O': r'Br-O (repulsive, large anion)',
}

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 12,
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'legend.fontsize': 9,
    'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
})


def main():
    csv_path = OUT_DIR / "bond_density_summary.csv"
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("comp,formula_short,Li-O,Cl-O,Br-O,paper_Wad_mJ_m2\n")
        for c in ALL_COMPS:
            d = BOND_DATA[c]
            pe = PAPER_EXP.get(c, '')
            f.write(f"{c},{LABELS_SHORT[c]},{d['Li-O']:.6f},{d['Cl-O']:.6f},"
                    f"{d['Br-O']:.6f},{pe}\n")
    print(f"  saved {csv_path}")

    # ── Figure 1: grouped bar (3 bond types × 6 comps) ──
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(ALL_COMPS))
    width = 0.27
    for i, bond in enumerate(['Li-O', 'Cl-O', 'Br-O']):
        vals = [BOND_DATA[c][bond] for c in ALL_COMPS]
        offset = (i - 1) * width
        bars = ax.bar(x + offset, vals, width,
                       color=BOND_COLORS[bond],
                       label=BOND_LABELS[bond],
                       edgecolor='k', linewidth=0.6, alpha=0.85)
        for j, v in enumerate(vals):
            if v > 0.005:
                ax.text(x[j] + offset, v + 0.003, f'{v:.3f}',
                        ha='center', va='bottom', fontsize=7, color=BOND_COLORS[bond])
    ax.set_xticks(x)
    ax.set_xticklabels([LABELS_SHORT[c] for c in ALL_COMPS], rotation=20, ha='right', fontsize=10)
    ax.set_ylabel(r'Bond density (Å$^{-2}$)', fontsize=12)
    ax.set_title('Interface bond densities at gap$_{eq}$ (36-registry mean)', fontsize=12)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, max(0.18, max(BOND_DATA[c]['Li-O'] for c in ALL_COMPS) * 1.15))

    # Highlight family separation
    ax.axvline(1.5, color='gray', linestyle=':', alpha=0.5)
    ax.axvline(4.5, color='gray', linestyle=':', alpha=0.5)
    ax.text(0.5, ax.get_ylim()[1]*0.95, 'Li6 family',
            ha='center', fontsize=8, alpha=0.6, fontstyle='italic')
    ax.text(3.0, ax.get_ylim()[1]*0.95, 'Li5.4 mixed (Cl+Br)',
            ha='center', fontsize=8, alpha=0.6, fontstyle='italic')
    ax.text(5.0, ax.get_ylim()[1]*0.95, 'Li5.4 Cl-only',
            ha='center', fontsize=8, alpha=0.6, fontstyle='italic')

    fig.tight_layout()
    fig.savefig(OUT_DIR / "bond_density_grouped_bar.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "bond_density_grouped_bar.png", bbox_inches='tight')
    plt.close()
    print(f"  saved bond_density_grouped_bar.pdf/png")

    # ── Figure 2: with paper exp Wad overlay (secondary axis) ──
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(ALL_COMPS))
    width = 0.27
    for i, bond in enumerate(['Li-O', 'Cl-O', 'Br-O']):
        vals = [BOND_DATA[c][bond] for c in ALL_COMPS]
        offset = (i - 1) * width
        ax.bar(x + offset, vals, width, color=BOND_COLORS[bond],
                label=BOND_LABELS[bond],
                edgecolor='k', linewidth=0.6, alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels([LABELS_SHORT[c] for c in ALL_COMPS], rotation=20, ha='right', fontsize=10)
    ax.set_ylabel(r'Bond density (Å$^{-2}$)', fontsize=12)
    ax.legend(loc='upper left', fontsize=9, framealpha=0.95)
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, 0.18)

    # Secondary axis: paper Wad
    ax2 = ax.twinx()
    wad_vals = [PAPER_EXP.get(c, np.nan) for c in ALL_COMPS]
    valid = [(xi, w) for xi, w in zip(x, wad_vals) if not np.isnan(w)]
    if valid:
        xs, ws = zip(*valid)
        ax2.plot(xs, ws, 'ko-', markersize=10, linewidth=1.5,
                 label=r'Paper exp $W_{ad}$ (mJ/m²)',
                 markerfacecolor='white', markeredgewidth=2)
        for xi, w in zip(xs, ws):
            ax2.text(xi, w + 10, f'{w}', ha='center', va='bottom',
                     fontsize=9, fontweight='bold')
    ax2.set_ylabel(r'Paper exp $W_{ad}$ (mJ/m²)', fontsize=12)
    ax2.set_ylim(0, 380)
    ax2.legend(loc='upper right', fontsize=9, framealpha=0.95)

    fig.suptitle('Interface bond densities and experimental adhesion', fontsize=12, y=1.00)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "bond_density_with_wad.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "bond_density_with_wad.png", bbox_inches='tight')
    plt.close()
    print(f"  saved bond_density_with_wad.pdf/png")

    # ── Print summary ──
    print(f"\n--- Per-comp interface bond densities ---")
    print(f"{'comp':<8} {'paper_Wad':>10} {'Li-O':>8} {'Cl-O':>8} {'Br-O':>8}  family")
    for c in ALL_COMPS:
        d = BOND_DATA[c]
        pe = PAPER_EXP.get(c, '—')
        family = 'Li6' if c in ['comp1', 'comp2'] else (
            'Li5.4 (Cl-only)' if c == 'modelC' else 'Li5.4 (Cl+Br)')
        print(f"  {c:<8} {str(pe):>10} {d['Li-O']:>8.4f} {d['Cl-O']:>8.4f} "
              f"{d['Br-O']:>8.4f}  {family}")

    # R values
    print(f"\n--- Pearson R vs paper Wad (n=5 paper comps) ---")
    paper_y = [PAPER_EXP[c] for c in PAPER_COMPS]
    for bond in ['Li-O', 'Cl-O', 'Br-O']:
        x_vals = [BOND_DATA[c][bond] for c in PAPER_COMPS]
        if np.std(x_vals) == 0:
            R = float('nan')
        else:
            R = float(np.corrcoef(x_vals, paper_y)[0, 1])
        print(f"  R({bond:<5}) = {R:+.4f}")

    print(f"\nAll outputs in: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()

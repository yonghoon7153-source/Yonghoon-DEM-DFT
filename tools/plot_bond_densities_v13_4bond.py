"""Phase 2a v13 — 4-bond density (Li-O / Cl-O / Br-O / S-Li) at gap_eq.

Extension of plot_bond_densities_v9 with S-Li bar added. Both Cl-O and S-Li
are family-binary classifiers (Li6 has S-Li > 0, Li5.4 mix has S-Li = 0).

v15 data (gap_eq, 36-reg mean, KISTI 2026-05-10 — comp4 = v2 anneal champion):
- v1_REDO and v2 give IDENTICAL S-Li per comp (comp4's surface change didn't
  involve S-Li bonds in either case)

Outputs:
  bond_density_4bond_with_wad.{pdf,png}   4 bonds + paper Wad overlay
  bond_density_4bond_summary.csv          per-comp + R values

Run: python3 tools/plot_bond_densities_v13_4bond.py
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path("output/comp4_v2_adhesion/figures"); OUT_DIR.mkdir(parents=True, exist_ok=True)

ALL_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']
PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}

# v15 results (KISTI phase2a_v15_v2_results/results.json comp4 = v2 anneal champion)
# Other comps unchanged from v1_REDO (verified identical via fair comparison).
BOND_DATA = {
    'comp1':  {'Li-O': 0.1147, 'Cl-O': 0.0247, 'Br-O': 0.0000, 'S-Li': 0.04995},
    'comp2':  {'Li-O': 0.0759, 'Cl-O': 0.0292, 'Br-O': 0.0000, 'S-Li': 0.04189},
    'comp3':  {'Li-O': 0.1372, 'Cl-O': 0.0000, 'Br-O': 0.0000, 'S-Li': 0.00000},
    'comp4':  {'Li-O': 0.0761, 'Cl-O': 0.0881, 'Br-O': 0.0502, 'S-Li': 0.00000},  # v2 anneal champion
    'comp5':  {'Li-O': 0.1256, 'Cl-O': 0.0000, 'Br-O': 0.1078, 'S-Li': 0.00000},
    'modelC': {'Li-O': 0.0853, 'Cl-O': 0.0881, 'Br-O': 0.0000, 'S-Li': 0.02494},
}

LABELS_SHORT = {
    'comp1':  r'LPSC$_{1.0}$',     'comp2':  r'LPSC$_{0.5}$B$_{0.5}$',
    'comp3':  r'LPSC$_{1.0}$B$_{0.6}$', 'comp4':  r'LPSC$_{0.8}$B$_{0.8}$',
    'comp5':  r'LPSC$_{0.6}$B$_{1.0}$', 'modelC': r'LPSC$_{1.6}$',
}
BOND_COLORS = {'Li-O': '#3477eb', 'Cl-O': '#d62728', 'Br-O': '#2ca02c', 'S-Li': '#9467bd'}
BOND_LABELS = {
    'Li-O': r'Li-O (cation-anion, attractive)',
    'Cl-O': r'Cl-O (small anion, repulsive)',
    'Br-O': r'Br-O (large anion, repulsive)',
    'S-Li': r'S-Li (interfacial chalcogen, family-binary)',
}

plt.rcParams.update({
    'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 11,
    'xtick.labelsize': 9, 'ytick.labelsize': 10, 'legend.fontsize': 8,
    'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
})


def pearson(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    if x.std() == 0 or y.std() == 0:
        return float('nan')
    return float(np.corrcoef(x, y)[0, 1])


def main():
    # CSV
    csv_path = OUT_DIR / "bond_density_4bond_summary.csv"
    with open(csv_path, 'w') as f:
        f.write("comp,formula,Li-O,Cl-O,Br-O,S-Li,paper_Wad_mJ_m2\n")
        for c in ALL_COMPS:
            d = BOND_DATA[c]
            pe = PAPER_EXP.get(c, '')
            f.write(f"{c},{LABELS_SHORT[c]},{d['Li-O']:.5f},{d['Cl-O']:.5f},"
                    f"{d['Br-O']:.5f},{d['S-Li']:.5f},{pe}\n")
    print(f"  saved {csv_path}")

    # Compute R values (paper comps only, n=5)
    R = {}
    for bond in ['Li-O', 'Cl-O', 'Br-O', 'S-Li']:
        x = [BOND_DATA[c][bond] for c in PAPER_COMPS]
        y = [PAPER_EXP[c] for c in PAPER_COMPS]
        R[bond] = pearson(x, y)

    # ── Figure: 4 bonds × 6 comps + paper Wad overlay ──
    fig, ax = plt.subplots(figsize=(11, 5.5))
    x = np.arange(len(ALL_COMPS))
    width = 0.20
    bonds = ['Li-O', 'Cl-O', 'Br-O', 'S-Li']
    for i, bond in enumerate(bonds):
        vals = [BOND_DATA[c][bond] for c in ALL_COMPS]
        offset = (i - 1.5) * width
        bars = ax.bar(x + offset, vals, width, color=BOND_COLORS[bond],
                       label=f"{BOND_LABELS[bond]}  (R={R[bond]:+.2f})",
                       edgecolor='k', linewidth=0.5, alpha=0.85)
        for j, v in enumerate(vals):
            if v > 0.005:
                ax.text(x[j] + offset, v + 0.002, f'{v:.3f}',
                        ha='center', va='bottom', fontsize=6.5,
                        color=BOND_COLORS[bond])
    ax.set_xticks(x)
    ax.set_xticklabels([LABELS_SHORT[c] for c in ALL_COMPS], rotation=18, ha='right')
    ax.set_ylabel(r'Bond density (Å$^{-2}$)')
    ax.set_ylim(0, 0.18)
    ax.grid(axis='y', alpha=0.3)
    # Family separators
    ax.axvline(1.5, color='gray', linestyle=':', alpha=0.5)
    ax.axvline(4.5, color='gray', linestyle=':', alpha=0.5)
    ax.text(0.5, 0.165, 'Li$_6$ family',  ha='center', fontsize=9, alpha=0.6, fontstyle='italic')
    ax.text(3.0, 0.165, 'Li$_{5.4}$ (Cl+Br)', ha='center', fontsize=9, alpha=0.6, fontstyle='italic')
    ax.text(5.0, 0.165, 'Li$_{5.4}$ (Cl)', ha='center', fontsize=9, alpha=0.6, fontstyle='italic')

    # paper Wad on secondary axis
    ax2 = ax.twinx()
    yWad = [PAPER_EXP.get(c, np.nan) for c in ALL_COMPS]
    ax2.plot(x, yWad, 'ko-', mfc='white', ms=10, lw=1.5,
             label=r'Paper exp $W_{ad}$ (mJ/m$^2$)', zorder=10)
    for i, (c, y) in enumerate(zip(ALL_COMPS, yWad)):
        if not np.isnan(y):
            ax2.text(i, y + 12, f'{int(y)}', ha='center',
                     fontsize=10, fontweight='bold')
    ax2.set_ylabel(r'Paper exp $W_{ad}$ (mJ/m$^2$)')
    ax2.set_ylim(0, 380)

    ax.set_title('Interface bond densities + paper $W_{ad}$ — comp4 v2 anneal champion '
                 '(Cl exposed, Cl-O classifier broken)\n'
                 'S-Li density = Li$_6$ vs Li$_{5.4}$-mix family-binary classifier '
                 f'(R(S-Li) = {R["S-Li"]:+.2f})')

    # Combined legend
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc='upper left', fontsize=8, framealpha=0.95, ncol=1)

    fig.tight_layout()
    fig.savefig(OUT_DIR / "bond_density_4bond_with_wad.pdf")
    fig.savefig(OUT_DIR / "bond_density_4bond_with_wad.png")
    plt.close()
    print(f"  saved bond_density_4bond_with_wad.{{pdf,png}}")

    # Console summary
    print(f"\n--- Per-comp 4-bond densities (gap_eq, 36-reg mean) ---")
    print(f"{'comp':<8} {'paper':>6} {'Li-O':>7} {'Cl-O':>7} {'Br-O':>7} {'S-Li':>7}")
    for c in ALL_COMPS:
        pe = PAPER_EXP.get(c, '—')
        d = BOND_DATA[c]
        print(f"{c:<8} {str(pe):>6} {d['Li-O']:>7.4f} {d['Cl-O']:>7.4f} "
              f"{d['Br-O']:>7.4f} {d['S-Li']:>7.4f}")
    print(f"\n--- Pearson R vs paper Wad (n=5 paper comps) ---")
    for b in bonds:
        flag = "⭐" if abs(R[b]) > 0.9 else "+" if abs(R[b]) > 0.7 else ""
        print(f"  R({b:<5}) = {R[b]:+.4f}  {flag}")


if __name__ == '__main__':
    main()

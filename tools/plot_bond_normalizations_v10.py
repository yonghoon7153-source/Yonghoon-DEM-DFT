"""Phase 2a v10 — bond densities with multiple normalization choices.

Current (v9): bond / xy_area (Å⁻²)
Issue: different comps have different Cl/Br fu content. Normalize how?

Three normalization options shown:
1. RAW: bonds / area (Å⁻²) — original
2. PER-FU-HALOGEN: bonds / (halogen_fu × area) — accounts for stoichiometry
3. PER-TOTAL-ATOM: bonds / total atom count at slab — different reference

Plus:
4. Per-Cl ratio: Cl-O bonds / total_Cl_in_slab (fraction of Cl in contact)

All four shown side-by-side for comparison.
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path("binding_curves_plots"); OUT_DIR.mkdir(exist_ok=True)

ALL_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5', 'modelC']
PAPER_COMPS = ['comp1', 'comp2', 'comp3', 'comp4', 'comp5']

# v15 raw data (gap_eq, 36-reg mean) — bond density per Å²
BOND_DATA = {
    'comp1':  {'Li-O': 0.1138, 'Cl-O': 0.0228, 'Br-O': 0.0000},
    'comp2':  {'Li-O': 0.0740, 'Cl-O': 0.0285, 'Br-O': 0.0000},
    'comp3':  {'Li-O': 0.1338, 'Cl-O': 0.0000, 'Br-O': 0.0000},
    'comp4':  {'Li-O': 0.1338, 'Cl-O': 0.0000, 'Br-O': 0.1115},
    'comp5':  {'Li-O': 0.1283, 'Cl-O': 0.0000, 'Br-O': 0.1060},
    'modelC': {'Li-O': 0.0948, 'Cl-O': 0.0948, 'Br-O': 0.0000},
}

# Stoichiometry per fu
STOICH = {
    'comp1':  {'Li': 6.0, 'Cl': 1.0, 'Br': 0.0, 'fu_per_cell': 4},
    'comp2':  {'Li': 6.0, 'Cl': 0.5, 'Br': 0.5, 'fu_per_cell': 4},
    'comp3':  {'Li': 5.4, 'Cl': 1.0, 'Br': 0.6, 'fu_per_cell': 5},
    'comp4':  {'Li': 5.4, 'Cl': 0.8, 'Br': 0.8, 'fu_per_cell': 5},
    'comp5':  {'Li': 5.4, 'Cl': 0.6, 'Br': 1.0, 'fu_per_cell': 5},
    'modelC': {'Li': 5.4, 'Cl': 1.6, 'Br': 0.0, 'fu_per_cell': 5},
}

# Slab area (xy, Å²) per comp
AREA = {
    'comp1':  351.5, 'comp2':  351.5,
    'comp3':  179.3, 'comp4':  179.3, 'comp5':  179.3,
    'modelC': 179.3,
}

# Total atoms in slab (full slab: 4 fu × 13 = 52 cubic cell, but slab repeated)
# From actual data v15: SE slab atom counts
SLAB_ATOMS = {
    'comp1':  624, 'comp2':  624,
    'comp3':  248, 'comp4':  248, 'comp5':  248, 'modelC': 248,
}

PAPER_EXP = {'comp1': 194, 'comp2': 180, 'comp3': 316, 'comp4': 298, 'comp5': 249}

LABELS_SHORT = {
    'comp1':  'LPSC$_{1.0}$', 'comp2':  'LPSC$_{0.5}$B$_{0.5}$',
    'comp3':  'LPSC$_{1.0}$B$_{0.6}$', 'comp4':  'LPSC$_{0.8}$B$_{0.8}$',
    'comp5':  'LPSC$_{0.6}$B$_{1.0}$', 'modelC': 'LPSC$_{1.6}$',
}
BOND_COLORS = {'Li-O': '#3477eb', 'Cl-O': '#d62728', 'Br-O': '#2ca02c'}
BOND_LABELS = {'Li-O': 'Li-O (attractive)', 'Cl-O': 'Cl-O (repulsive small)',
               'Br-O': 'Br-O (repulsive large)'}

plt.rcParams.update({
    'font.size': 10, 'axes.labelsize': 11, 'axes.titlesize': 11,
    'xtick.labelsize': 9, 'ytick.labelsize': 9, 'legend.fontsize': 8,
    'figure.dpi': 150, 'savefig.dpi': 300, 'savefig.bbox': 'tight',
})


def compute_pearson(x_dict, y_dict, comps):
    x = [x_dict[c] for c in comps]
    y = [y_dict[c] for c in comps]
    if np.std(x) == 0 or np.std(y) == 0:
        return float('nan')
    return float(np.corrcoef(x, y)[0, 1])


def main():
    # Compute multiple normalizations
    norm_raw = {}
    norm_per_fu = {}
    norm_per_atom = {}
    norm_per_total = {}

    for c in ALL_COMPS:
        d = BOND_DATA[c]
        s = STOICH[c]
        A = AREA[c]
        N_atoms = SLAB_ATOMS[c]

        norm_raw[c] = dict(d)
        # Per fu of relevant halogen × area
        # bond_count / (halogen_fu × A) — represents "contact prob per fu halogen"
        norm_per_fu[c] = {
            'Li-O': d['Li-O'] / s['Li'],   # per Li/fu
            'Cl-O': d['Cl-O'] / s['Cl'] if s['Cl'] > 0 else 0,
            'Br-O': d['Br-O'] / s['Br'] if s['Br'] > 0 else 0,
        }
        # Per total atom count
        norm_per_atom[c] = {
            'Li-O': d['Li-O'] / N_atoms * 100,  # % per atom
            'Cl-O': d['Cl-O'] / N_atoms * 100,
            'Br-O': d['Br-O'] / N_atoms * 100,
        }
        # Per total halogen at slab (count, area-normalized)
        # Cl total in slab = (Cl/fu) × fu_per_cell × (slab_replicas)
        # Just use Cl/fu × fu_per_cell as scale factor
        N_Cl = s['Cl'] * s['fu_per_cell']
        N_Br = s['Br'] * s['fu_per_cell']
        norm_per_total[c] = {
            'Li-O': d['Li-O'] * A / (s['Li'] * s['fu_per_cell']) if s['Li'] > 0 else 0,
            'Cl-O': d['Cl-O'] * A / N_Cl if N_Cl > 0 else 0,
            'Br-O': d['Br-O'] * A / N_Br if N_Br > 0 else 0,
        }

    # ── 4-panel plot: 3 bond types × 4 normalizations ──
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    panels = [
        (axes[0, 0], norm_raw, '(a) Raw: bonds / area (Å⁻²)', 'Å⁻²'),
        (axes[0, 1], norm_per_fu, '(b) Per fu (count/fu)', 'count/fu'),
        (axes[1, 0], norm_per_atom, '(c) Per total slab atom (%)', '%'),
        (axes[1, 1], norm_per_total,
         '(d) Per total halogen (bonds/halogen, area-weighted)', 'unitless'),
    ]

    x_pos = np.arange(len(ALL_COMPS))
    width = 0.27
    for ax, data, title, ylabel in panels:
        for i, bond in enumerate(['Li-O', 'Cl-O', 'Br-O']):
            vals = [data[c][bond] for c in ALL_COMPS]
            offset = (i - 1) * width
            ax.bar(x_pos + offset, vals, width,
                   color=BOND_COLORS[bond], label=BOND_LABELS[bond],
                   edgecolor='k', linewidth=0.5, alpha=0.85)
        ax.set_xticks(x_pos)
        ax.set_xticklabels([LABELS_SHORT[c] for c in ALL_COMPS],
                            rotation=20, ha='right', fontsize=8)
        ax.set_ylabel(ylabel)
        ax.set_title(title, fontsize=10)
        ax.grid(axis='y', alpha=0.3)
        ax.legend(loc='upper left', fontsize=7)

    fig.suptitle('Bond density with 4 normalization choices', fontsize=12, y=1.00)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "bond_density_normalizations_4panel.pdf", bbox_inches='tight')
    fig.savefig(OUT_DIR / "bond_density_normalizations_4panel.png", bbox_inches='tight')
    plt.close()
    print(f"  saved bond_density_normalizations_4panel.pdf/png")

    # Pearson R per normalization
    paper_dict = PAPER_EXP
    print(f"\n--- Pearson R vs paper Wad (n=5) for each bond × normalization ---")
    print(f"{'normalization':<25} {'Li-O':>8} {'Cl-O':>8} {'Br-O':>8}")
    for name, data in [('(a) raw', norm_raw),
                        ('(b) per fu', norm_per_fu),
                        ('(c) per total atom', norm_per_atom),
                        ('(d) per halogen', norm_per_total)]:
        rs = []
        for bond in ['Li-O', 'Cl-O', 'Br-O']:
            x_dict = {c: data[c][bond] for c in PAPER_COMPS}
            R = compute_pearson(x_dict, paper_dict, PAPER_COMPS)
            rs.append(R)
        print(f"  {name:<25} {rs[0]:>+8.3f} {rs[1]:>+8.3f} {rs[2]:>+8.3f}")

    # CSV: all data
    csv_path = OUT_DIR / "bond_density_normalizations.csv"
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("comp,formula,paper_Wad,")
        f.write(",".join([f"{n}_{b}" for n in ['raw', 'per_fu', 'per_atom', 'per_halogen']
                          for b in ['Li-O', 'Cl-O', 'Br-O']]))
        f.write("\n")
        for c in ALL_COMPS:
            row = [c, LABELS_SHORT[c], str(PAPER_EXP.get(c, ''))]
            for data in [norm_raw, norm_per_fu, norm_per_atom, norm_per_total]:
                for b in ['Li-O', 'Cl-O', 'Br-O']:
                    row.append(f"{data[c][b]:.6f}")
            f.write(",".join(row) + "\n")
    print(f"\n  saved {csv_path}")
    print(f"\nAll outputs in: {OUT_DIR.resolve()}")


if __name__ == "__main__":
    main()

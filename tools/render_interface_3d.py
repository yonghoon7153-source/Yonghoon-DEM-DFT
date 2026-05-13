"""render_interface_3d.py — render SE/NCM interface 3D figure with bond highlights.

Reads stacked orthogonal interface xyz (e.g., comp1_R1_origin_d1.2_orthogonal.xyz)
and renders a side-view figure showing:
  • NCM and SE slabs side by side (color-coded atoms)
  • Interface region highlighted (within 3 Å above/below gap)
  • Bond contacts drawn as dashed lines:
      Li-O (cyan, attractive)
      S-O  (red, repulsive)
      Cl-O (orange)
      Br-O (purple)

Layout: side projection (z vs y), zoomed on interface region.
Output: <name>_interface_3d.png

Usage:
    python3 render_interface_3d.py comp1.xyz [comp2.xyz ...]
    # Generates side-by-side panel figure for multi-comp comparison

Author: Yonghoon-DEM-DFT collaboration
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from ase.io import read

# Element colors (CPK + custom)
COLORS = {
    'Li': '#9971D9', 'P': '#9D9D9D', 'S': '#FCC830',
    'Cl': '#1FE61F', 'Br': '#A52A2A',
    'Ni': '#5078D2', 'O': '#FF1C00',
}
SIZES = {
    'Li': 100, 'P': 130, 'S': 160, 'Cl': 150, 'Br': 170,
    'Ni': 180, 'O': 130,
}

# Bond cutoffs (only SE atom → NCM-O contacts, plus optionally Li-Ni)
BOND_RULES = [
    ('Li', 'O', 2.8, '#00BFFF', '-',  1.5),  # cyan solid — attractive Li-O
    ('S',  'O', 3.0, '#FF1C00', ':',  1.2),  # red dotted — repulsive S-O
    ('Cl', 'O', 3.2, '#FFA500', '--', 1.0),  # orange dashed — Cl-O
    ('Br', 'O', 3.4, '#9932CC', '--', 1.0),  # purple dashed — Br-O
]


def assign_ncm_se(atoms, z_cut=None):
    """Partition atoms into NCM (Ni, O, NCM-Li) and SE based on z.
    Returns (ncm_mask, se_mask)."""
    syms = np.array(atoms.get_chemical_symbols())
    z = atoms.positions[:, 2]
    if z_cut is None:
        # Auto-detect: NCM has Ni/O; find z range of NCM (Ni + O atoms)
        ncm_native = np.isin(syms, ['Ni', 'O'])
        z_ncm_max = z[ncm_native].max() if ncm_native.any() else 0
        z_cut = z_ncm_max + 0.5   # 0.5 Å buffer above NCM topmost atom
    # NCM region: anything with z <= z_cut
    ncm_mask = z <= z_cut
    se_mask  = ~ncm_mask
    return ncm_mask, se_mask, z_cut


def count_contacts_at_interface(atoms, ncm_mask, se_mask):
    """Count bond contacts between SE atoms and NCM O within cutoff."""
    sym = np.array(atoms.get_chemical_symbols())
    ncm_O_idx = np.where(ncm_mask & (sym == 'O'))[0]
    counts = {f"{s}-O": 0 for s in ['Li', 'S', 'Cl', 'Br']}
    contact_pairs = []
    for i in np.where(se_mask)[0]:
        se_el = sym[i]
        if se_el not in ('Li', 'S', 'Cl', 'Br'):
            continue
        cutoff = {'Li': 2.8, 'S': 3.0, 'Cl': 3.2, 'Br': 3.4}[se_el]
        for j in ncm_O_idx:
            d = atoms.get_distance(i, j, mic=True)
            if d <= cutoff:
                counts[f"{se_el}-O"] += 1
                contact_pairs.append((i, j, se_el, d))
    return counts, contact_pairs


def render_panel(ax, atoms, name, zoom_window=(8, 25)):
    """Render side projection (y vs z) on ax."""
    sym = np.array(atoms.get_chemical_symbols())
    pos = atoms.positions

    ncm_mask, se_mask, z_cut = assign_ncm_se(atoms)
    counts, pairs = count_contacts_at_interface(atoms, ncm_mask, se_mask)

    # Plot atoms
    for el in np.unique(sym):
        mask = sym == el
        # color shading: NCM darker, SE lighter? Keep same for now
        ax.scatter(pos[mask, 1], pos[mask, 2],
                   c=COLORS.get(el, '#888'), s=SIZES.get(el, 80),
                   edgecolors='black', linewidths=0.6, zorder=3,
                   label=el if (mask.sum() > 0 and el not in ax.get_legend_handles_labels()[1]) else None)

    # Draw bond contacts
    for i, j, se_el, d in pairs:
        for rule_se, rule_ncm, cutoff, color, style, lw in BOND_RULES:
            if rule_se == se_el:
                ax.plot([pos[i, 1], pos[j, 1]], [pos[i, 2], pos[j, 2]],
                        color=color, linestyle=style, linewidth=lw,
                        alpha=0.75, zorder=2)
                break

    # Interface line
    ax.axhline(z_cut, color='black', linestyle='--', linewidth=0.7,
               alpha=0.5, zorder=1)

    # Zoom to interface region
    ax.set_ylim(*zoom_window)
    ax.set_xlim(0, atoms.cell.lengths()[1])

    # Annotations
    ax.set_title(f"{name}\n" +
                 "  ".join([f"{k}={v}" for k, v in counts.items() if v > 0]),
                 fontsize=10)
    ax.set_xlabel('y (Å)', fontsize=9)
    ax.set_aspect('equal')


def main(xyz_paths):
    n = len(xyz_paths)
    fig, axes = plt.subplots(1, n, figsize=(6 * n, 7), squeeze=False)
    axes = axes[0]

    for ax, path in zip(axes, xyz_paths):
        a = read(path)
        name = Path(path).stem.split('_')[0]      # extract first underscore-token
        render_panel(ax, a, name)

    axes[0].set_ylabel('z (Å)', fontsize=11)

    # Legend (single, on rightmost)
    handles = []
    seen = set()
    for el, c in COLORS.items():
        if el not in seen:
            handles.append(plt.Line2D([0], [0], marker='o', color='w',
                                      markerfacecolor=c, markeredgecolor='k',
                                      markersize=8, label=el))
            seen.add(el)
    for rule_se, rule_ncm, cutoff, color, style, lw in BOND_RULES:
        handles.append(plt.Line2D([0], [0], color=color, linestyle=style,
                                  linewidth=lw + 0.5,
                                  label=f"{rule_se}-{rule_ncm} ≤ {cutoff} Å"))
    axes[-1].legend(handles=handles, loc='center left', bbox_to_anchor=(1.02, 0.5),
                    fontsize=8, framealpha=0.95)

    plt.suptitle("SE/NCM interface — atomic structure + bond contact map",
                 fontsize=12, y=1.00)
    fig.tight_layout()
    out_name = "interface_3d_compare.png"
    fig.savefig(out_name, dpi=200, bbox_inches='tight')
    fig.savefig(out_name.replace('.png', '.pdf'), bbox_inches='tight')
    print(f"Saved: {out_name}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Use uploaded files as default
        paths = [
            '/root/.claude/uploads/ec05ab4a-323a-4032-b00c-349a43b71c49/4f835cdd-comp1_R1_origin_d1.2_orthogonal.xyz',
            '/root/.claude/uploads/ec05ab4a-323a-4032-b00c-349a43b71c49/6be69a8c-comp2_R1_origin_d1.2_orthogonal.xyz',
        ]
    else:
        paths = sys.argv[1:]
    main(paths)

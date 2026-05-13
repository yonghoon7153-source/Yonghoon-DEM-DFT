"""render_interface_3d.py — render SE/NCM interface 3D side-view with bond highlights.

Reads stacked orthogonal interface xyz files and renders a side-view panel
figure showing:
  • NCM and SE slabs (color-coded atoms)
  • Interface region zoomed (5 Å around the SE-NCM gap)
  • Bond contacts drawn as colored lines:
      Li-O (cyan solid, attractive)
      S-O  (red dotted, repulsive)
      Cl-O (orange dashed)
      Br-O (purple dashed)

Usage:
    python3 render_interface_3d.py file1.xyz file2.xyz file3.xyz ...

Example (3-comp comparison):
    python3 render_interface_3d.py \\
        comp1_R1_origin_d1.2_orthogonal.xyz \\
        comp2_R1_origin_d1.2_orthogonal.xyz \\
        comp4_v2_R1_origin_d1.4_orthogonal.xyz
"""
import sys
from pathlib import Path
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from ase.io import read

# Element colors (CPK-style)
COLORS = {
    'Li': '#9971D9', 'P': '#9D9D9D', 'S': '#FCC830',
    'Cl': '#1FE61F', 'Br': '#A52A2A',
    'Ni': '#5078D2', 'O': '#FF1C00',
}
SIZES = {
    'Li': 80, 'P': 120, 'S': 140, 'Cl': 130, 'Br': 150,
    'Ni': 160, 'O': 110,
}

BOND_RULES = [
    ('Li', 'O', 2.8, '#00BFFF', '-',  1.5),   # cyan solid
    ('S',  'O', 3.0, '#FF1C00', ':',  1.2),   # red dotted
    ('Cl', 'O', 3.2, '#FFA500', '--', 1.0),   # orange dashed
    ('Br', 'O', 3.4, '#9932CC', '--', 1.0),   # purple dashed
]


def clean_name(path):
    """Extract clean comp name from filename, drop hash prefix."""
    stem = Path(path).stem
    cleaned = re.sub(r'^[0-9a-f]{6,8}-', '', stem)
    return cleaned.split('_')[0] + ('_' + cleaned.split('_')[1]
                                     if 'v1' in cleaned or 'v2' in cleaned else '')


def assign_ncm_se(atoms):
    """NCM = atoms with z below z_ncm_max+0.5 (NCM has Ni and O)."""
    syms = np.array(atoms.get_chemical_symbols())
    z = atoms.positions[:, 2]
    ncm_native = np.isin(syms, ['Ni', 'O'])
    z_ncm_max = z[ncm_native].max() if ncm_native.any() else 0
    z_cut = z_ncm_max + 0.5
    ncm_mask = z <= z_cut
    return ncm_mask, ~ncm_mask, z_cut


def count_contacts(atoms, ncm_mask, se_mask):
    sym = np.array(atoms.get_chemical_symbols())
    ncm_O_idx = np.where(ncm_mask & (sym == 'O'))[0]
    counts = {f"{s}-O": 0 for s in ['Li', 'S', 'Cl', 'Br']}
    pairs = []
    for i in np.where(se_mask)[0]:
        se_el = sym[i]
        if se_el not in ('Li', 'S', 'Cl', 'Br'):
            continue
        cutoff = {'Li': 2.8, 'S': 3.0, 'Cl': 3.2, 'Br': 3.4}[se_el]
        for j in ncm_O_idx:
            d = atoms.get_distance(i, j, mic=True)
            if d <= cutoff:
                counts[f"{se_el}-O"] += 1
                pairs.append((i, j, se_el, d))
    return counts, pairs


def render_panel(ax, atoms, name, zoom_pad=5.0):
    sym = np.array(atoms.get_chemical_symbols())
    pos = atoms.positions
    ncm_mask, se_mask, z_cut = assign_ncm_se(atoms)
    counts, pairs = count_contacts(atoms, ncm_mask, se_mask)

    z_se_min = pos[se_mask, 2].min() if se_mask.any() else z_cut
    z_lo = z_se_min - zoom_pad - 5
    z_hi = z_se_min + zoom_pad + 3

    mask_zoom = (pos[:, 2] >= z_lo) & (pos[:, 2] <= z_hi)
    for el in np.unique(sym[mask_zoom]):
        m = (sym == el) & mask_zoom
        if not m.any():
            continue
        ax.scatter(pos[m, 1], pos[m, 2],
                   c=COLORS.get(el, '#888'), s=SIZES.get(el, 80),
                   edgecolors='black', linewidths=0.6, zorder=3)

    for i, j, se_el, d in pairs:
        if not (z_lo <= pos[i, 2] <= z_hi and z_lo <= pos[j, 2] <= z_hi):
            continue
        for rule_se, rule_ncm, cutoff, color, style, lw in BOND_RULES:
            if rule_se == se_el:
                ax.plot([pos[i, 1], pos[j, 1]], [pos[i, 2], pos[j, 2]],
                        color=color, linestyle=style, linewidth=lw,
                        alpha=0.7, zorder=2)
                break

    ax.axhline(z_cut, color='black', linestyle='--', linewidth=0.6,
               alpha=0.4, zorder=1)
    ax.set_ylim(z_lo, z_hi)

    y_pos = pos[mask_zoom, 1]
    if len(y_pos):
        ax.set_xlim(y_pos.min() - 1, y_pos.max() + 1)

    count_str = "  ".join([f"{k}={v}" for k, v in counts.items() if v > 0])
    ax.set_title(f"{name}\n{count_str}", fontsize=10)
    ax.set_xlabel('y (Å)', fontsize=9)
    ax.set_aspect('equal')
    ax.grid(alpha=0.2)


def main(xyz_paths):
    n = len(xyz_paths)
    fig, axes = plt.subplots(1, n, figsize=(5.2 * n, 6.5), squeeze=False)
    axes = axes[0]

    for ax, path in zip(axes, xyz_paths):
        a = read(path)
        name = clean_name(path)
        render_panel(ax, a, name)

    axes[0].set_ylabel('z (Å)', fontsize=11)

    # Legend
    handles = []
    seen = set()
    for el, c in COLORS.items():
        if el in seen: continue
        handles.append(plt.Line2D([0], [0], marker='o', color='w',
                                  markerfacecolor=c, markeredgecolor='k',
                                  markersize=8, label=el))
        seen.add(el)
    for rule_se, rule_ncm, cutoff, color, style, lw in BOND_RULES:
        handles.append(plt.Line2D([0], [0], color=color, linestyle=style,
                                  linewidth=lw + 0.5,
                                  label=f"{rule_se}-{rule_ncm} ≤ {cutoff} Å"))
    fig.legend(handles=handles, loc='center left',
               bbox_to_anchor=(0.98, 0.5),
               fontsize=8, framealpha=0.95)

    plt.suptitle("SE/NCM interface — bond contact map (side view)",
                 fontsize=12, y=0.98)
    fig.tight_layout(rect=[0, 0, 0.96, 0.97])
    out_name = "interface_3d_compare.png"
    fig.savefig(out_name, dpi=200, bbox_inches='tight')
    fig.savefig(out_name.replace('.png', '.pdf'), bbox_inches='tight')
    print(f"Saved: {out_name}")
    print(f"Saved: {out_name.replace('.png','.pdf')}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 render_interface_3d.py file1.xyz file2.xyz ...")
        sys.exit(1)
    main(sys.argv[1:])

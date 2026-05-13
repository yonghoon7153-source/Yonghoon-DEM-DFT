"""render_interface_3axis.py — 3D atomistic rendering of SE/NCM interface.

VESTA-like 3D view using matplotlib (no extra binaries needed). Each comp gets
a separate 3D panel showing atoms as spheres + bonds at interface.

Features:
  • 3D perspective (azim, elev configurable)
  • Atom spheres color-coded by element (CPK)
  • Bond lines for Li-O, S-O, Cl-O, Br-O contacts
  • Interface zoom (±5 Å around gap)
  • Multi-panel: 1 panel per comp

Usage:
    python3 render_interface_3axis.py file1.xyz file2.xyz file3.xyz
"""
import sys, re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from ase.io import read

COLORS = {
    'Li': '#9971D9', 'P': '#9D9D9D', 'S': '#FCC830',
    'Cl': '#1FE61F', 'Br': '#A52A2A',
    'Ni': '#5078D2', 'O': '#FF1C00',
}
SIZES = {  # sphere markersize (matplotlib)
    'Li': 60, 'P': 90, 'S': 110, 'Cl': 100, 'Br': 130,
    'Ni': 140, 'O': 90,
}

BOND_RULES = [
    ('Li', 'O', 2.8, '#00BFFF', '-',  1.8),   # cyan solid attractive
    ('S',  'O', 3.0, '#FF1C00', ':',  1.5),   # red dotted repulsive
    ('Cl', 'O', 3.2, '#FFA500', '--', 1.2),
    ('Br', 'O', 3.4, '#9932CC', '--', 1.2),
]


def clean_name(path):
    stem = Path(path).stem
    cleaned = re.sub(r'^[0-9a-f]{6,8}-', '', stem)
    parts = cleaned.split('_')
    name = parts[0]
    if len(parts) > 1 and ('v1' in parts[1] or 'v2' in parts[1]):
        name = name + '_' + parts[1]
    return name


def assign_ncm_se(atoms):
    syms = np.array(atoms.get_chemical_symbols())
    z = atoms.positions[:, 2]
    ncm_native = np.isin(syms, ['Ni', 'O'])
    z_ncm_max = z[ncm_native].max() if ncm_native.any() else 0
    z_cut = z_ncm_max + 0.5
    return z <= z_cut, z > z_cut, z_cut


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


def render_3d_panel(ax, atoms, name, zoom_pad=4.0):
    sym = np.array(atoms.get_chemical_symbols())
    pos = atoms.positions.copy()
    ncm_mask, se_mask, z_cut = assign_ncm_se(atoms)
    counts, pairs = count_contacts(atoms, ncm_mask, se_mask)

    z_se_min = pos[se_mask, 2].min() if se_mask.any() else z_cut
    z_lo = z_se_min - zoom_pad - 4
    z_hi = z_se_min + zoom_pad + 2

    # Shift atoms so z_lo is at 0 for cleaner axis
    pos_shift = pos.copy()
    pos_shift[:, 2] -= z_lo
    z_cut_shift = z_cut - z_lo
    z_lim = z_hi - z_lo

    mask_zoom = (pos[:, 2] >= z_lo) & (pos[:, 2] <= z_hi)

    # Plot atoms (3D scatter), sort by z for depth ordering
    idx_zoom = np.where(mask_zoom)[0]
    idx_sorted = idx_zoom[np.argsort(pos_shift[idx_zoom, 2])]
    for i in idx_sorted:
        el = sym[i]
        ax.scatter(pos_shift[i, 0], pos_shift[i, 1], pos_shift[i, 2],
                   c=COLORS.get(el, '#888'), s=SIZES.get(el, 70),
                   edgecolors='black', linewidths=0.5,
                   depthshade=True, alpha=0.95)

    # Draw bond lines
    for i, j, se_el, d in pairs:
        if not (z_lo <= pos[i, 2] <= z_hi and z_lo <= pos[j, 2] <= z_hi):
            continue
        for rule_se, _, _, color, style, lw in BOND_RULES:
            if rule_se == se_el:
                ax.plot([pos_shift[i, 0], pos_shift[j, 0]],
                        [pos_shift[i, 1], pos_shift[j, 1]],
                        [pos_shift[i, 2], pos_shift[j, 2]],
                        color=color, linestyle=style, linewidth=lw,
                        alpha=0.85, zorder=5)
                break

    # Interface plane (translucent)
    cell = atoms.cell.array
    x_range = [pos_shift[mask_zoom, 0].min(), pos_shift[mask_zoom, 0].max()]
    y_range = [pos_shift[mask_zoom, 1].min(), pos_shift[mask_zoom, 1].max()]
    xx, yy = np.meshgrid(np.linspace(x_range[0], x_range[1], 5),
                         np.linspace(y_range[0], y_range[1], 5))
    zz = np.full_like(xx, z_cut_shift)
    ax.plot_surface(xx, yy, zz, color='gray', alpha=0.12, zorder=0)

    ax.set_xlim(x_range[0] - 1, x_range[1] + 1)
    ax.set_ylim(y_range[0] - 1, y_range[1] + 1)
    ax.set_zlim(0, z_lim)
    ax.set_xlabel('x (Å)', fontsize=9)
    ax.set_ylabel('y (Å)', fontsize=9)
    ax.set_zlabel('z (Å)', fontsize=9)

    count_str = "  ".join([f"{k}={v}" for k, v in counts.items() if v > 0])
    ax.set_title(f"{name}\n{count_str}", fontsize=10)

    # Viewing angle (VESTA-like perspective)
    ax.view_init(elev=15, azim=-60)
    ax.set_box_aspect([1, 1, z_lim / max(x_range[1] - x_range[0], 1)])


def main(xyz_paths):
    n = len(xyz_paths)
    fig = plt.figure(figsize=(7 * n, 8))
    axes = [fig.add_subplot(1, n, i + 1, projection='3d') for i in range(n)]

    for ax, path in zip(axes, xyz_paths):
        a = read(path)
        name = clean_name(path)
        render_3d_panel(ax, a, name)

    # Legend
    handles = []
    seen = set()
    for el, c in COLORS.items():
        if el in seen: continue
        handles.append(plt.Line2D([0], [0], marker='o', color='w',
                                  markerfacecolor=c, markeredgecolor='k',
                                  markersize=10, label=el))
        seen.add(el)
    for rule_se, _, cutoff, color, style, lw in BOND_RULES:
        handles.append(plt.Line2D([0], [0], color=color, linestyle=style,
                                  linewidth=lw + 0.5,
                                  label=f"{rule_se}-O ≤ {cutoff} Å"))
    fig.legend(handles=handles, loc='center left',
               bbox_to_anchor=(0.98, 0.5),
               fontsize=8, framealpha=0.95)

    plt.suptitle("SE/NCM interface — 3D atomistic view at well distance",
                 fontsize=13, y=0.99)
    fig.tight_layout(rect=[0, 0, 0.96, 0.97])
    out_name = "interface_3axis_compare.png"
    fig.savefig(out_name, dpi=200, bbox_inches='tight')
    fig.savefig(out_name.replace('.png', '.pdf'), bbox_inches='tight')
    print(f"Saved: {out_name}")
    print(f"Saved: {out_name.replace('.png','.pdf')}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 render_interface_3axis.py f1.xyz f2.xyz f3.xyz")
        sys.exit(1)
    main(sys.argv[1:])

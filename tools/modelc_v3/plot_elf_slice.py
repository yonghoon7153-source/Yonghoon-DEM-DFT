#!/usr/bin/env python3
"""2D ELF slice plot from QE Gaussian-cube output.

Reads V0_ELF.cube (plot_num=8 from pp.x) and produces 2D heat maps with
atomic positions overlaid. Two modes:

  (1) Axial slices xy/xz/yz at a chosen fractional coordinate.
  (2) Bond plane through 3 specified atom indices (e.g. P + 2 S of PS4).

Standard ELF colormap: blue (0, delocalized) → green (0.5, free electron-gas)
→ yellow/red (>0.7, localized bond / lone pair).

Usage:
    # Axial slice through the middle of the cell
    python3 plot_elf_slice.py \\
        --cube V0_ELF.cube --out V0_ELF_xy_mid.png \\
        --mode axial --axis z --frac 0.5

    # Plane through P (atom 28) + 2 nearest S (atoms 33, 34) — PS4 tetrahedron
    python3 plot_elf_slice.py \\
        --cube V0_ELF.cube --out V0_ELF_PS4.png \\
        --mode plane --atoms 28 33 34 --thickness_A 1.5

ELF physical meaning:
  0     — uniform electron gas (no localization)
  0.5   — free electron-gas-like (metallic)
  >0.7  — bond pair or lone pair
  ~1.0  — fully localized (idealized lone pair)
"""
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Circle


ELEM_COLOR = {
    "Li": "#1a1a1a", "P": "#FF9933", "S": "#FFDC52",
    "Cl": "#3E8E41", "N": "#3F7BB6", "C": "#222222",
}
ELEM_R_DISPLAY = {
    "Li": 0.40, "P": 0.55, "S": 0.55, "Cl": 0.55,
    "N": 0.50, "C": 0.50,
}


def read_cube(cube_path):
    """Return (data, origin, cell_3x3, atoms_list).
    atoms_list = [(Z, x, y, z), ...] in Cartesian (Å after conversion).
    cell_3x3 in Å (rows are voxel vectors × N grid).
    """
    BOHR = 0.5291772108
    lines = cube_path.read_text().splitlines()
    nat_line = lines[2].split()
    natoms = int(nat_line[0])
    origin = np.array([float(x) for x in nat_line[1:4]]) * BOHR
    voxels = []
    grid_n = []
    for i in range(3):
        parts = lines[3 + i].split()
        grid_n.append(int(parts[0]))
        vec = np.array([float(x) for x in parts[1:4]]) * BOHR
        voxels.append(vec)
    voxels = np.array(voxels)
    atoms = []
    for i in range(natoms):
        parts = lines[6 + i].split()
        Z = int(parts[0])
        # parts[1] is charge, then xyz in Bohr
        xyz = np.array([float(x) for x in parts[2:5]]) * BOHR
        atoms.append((Z, xyz))
    # Data starts after atoms
    data_lines = lines[6 + natoms:]
    raw = " ".join(data_lines).split()
    arr = np.array([float(x) for x in raw], dtype=float)
    nx, ny, nz = grid_n
    if arr.size != nx * ny * nz:
        # CUBE z-fast order
        raise ValueError(f"data size {arr.size} != {nx*ny*nz}")
    data = arr.reshape(nx, ny, nz)
    return data, origin, voxels, atoms


def Z_to_symbol(Z):
    PT = {3: "Li", 6: "C", 7: "N", 8: "O", 9: "F",
          11: "Na", 15: "P", 16: "S", 17: "Cl",
          20: "Ca", 35: "Br"}
    return PT.get(Z, f"Z{Z}")


def axial_slice(data, voxels, origin, axis="z", frac=0.5):
    """Returns (slice_2d, xy_extent, in-plane axes labels).
    voxels rows are dx_vec, dy_vec, dz_vec (Cartesian).
    """
    nx, ny, nz = data.shape
    n_per_axis = {"x": nx, "y": ny, "z": nz}[axis]
    idx = max(0, min(n_per_axis - 1, int(round(frac * n_per_axis))))
    if axis == "z":
        s2d = data[:, :, idx]
        u_vec, v_vec = voxels[0] * nx, voxels[1] * ny
        u_label, v_label = "x (Å)", "y (Å)"
    elif axis == "y":
        s2d = data[:, idx, :]
        u_vec, v_vec = voxels[0] * nx, voxels[2] * nz
        u_label, v_label = "x (Å)", "z (Å)"
    else:  # x
        s2d = data[idx, :, :]
        u_vec, v_vec = voxels[1] * ny, voxels[2] * nz
        u_label, v_label = "y (Å)", "z (Å)"
    # extent: assumes orthogonal voxels in plane (true for cubic, approx else)
    extent = [0, np.linalg.norm(u_vec),
              0, np.linalg.norm(v_vec)]
    return s2d.T, extent, (u_label, v_label), idx


def make_elf_cmap():
    """Standard ELF colormap: blue → cyan → green → yellow → red → white."""
    colors = ["#08306b", "#08519c", "#2171b5", "#6baed6",
              "#41ab5d", "#fee08b", "#fdae61", "#d73027", "#a50026"]
    return mcolors.LinearSegmentedColormap.from_list("ELF", colors)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cube", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--mode", choices=["axial"], default="axial",
                    help="axial = xy/xz/yz at fixed fractional coord")
    ap.add_argument("--axis", choices=["x", "y", "z"], default="z",
                    help="axial slice perpendicular to this axis")
    ap.add_argument("--frac", type=float, default=0.5,
                    help="fractional coordinate (0-1) along --axis")
    ap.add_argument("--vmin", type=float, default=0.0)
    ap.add_argument("--vmax", type=float, default=1.0)
    ap.add_argument("--atom_z_window", type=float, default=2.0,
                    help="show atoms within this Å of the slice plane")
    ap.add_argument("--no_atoms", action="store_true", default=False,
                    help="suppress atom overlay (cleaner ELF-only view)")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--show_isolines",
                    action="store_true", default=False,
                    help="overlay ELF iso-contours at 0.5 and 0.75")
    ap.add_argument("--label", default="modelC_v3 (LPSCl1.6)",
                    help="system label shown in the plot title "
                         "(e.g. 'comp1 (LPSCl)')")
    args = ap.parse_args()

    data, origin, voxels, atoms = read_cube(Path(args.cube))
    print(f"Cube grid: {data.shape}, range [{data.min():.3f}, {data.max():.3f}]")
    print(f"  atoms: {len(atoms)}")

    s2d, extent, (xlab, ylab), idx = axial_slice(
        data, voxels, origin, args.axis, args.frac)
    print(f"  axial slice axis={args.axis} idx={idx}/{data.shape['xyz'.index(args.axis)]}")

    fig, ax = plt.subplots(figsize=(8, 7))
    cmap = make_elf_cmap()
    im = ax.imshow(s2d, origin='lower', extent=extent,
                    cmap=cmap, vmin=args.vmin, vmax=args.vmax,
                    aspect='equal', interpolation='bilinear')
    cbar = plt.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
    cbar.set_label("ELF", fontsize=12)

    if args.show_isolines:
        # Overlay 0.5 and 0.75 iso-lines
        nx, ny = s2d.shape
        x = np.linspace(extent[0], extent[1], ny)
        y = np.linspace(extent[2], extent[3], nx)
        X, Y = np.meshgrid(x, y)
        ax.contour(X, Y, s2d, levels=[0.5, 0.75], colors=['white', 'black'],
                    linewidths=[1.0, 1.0], linestyles=['--', '-'])

    # Project atoms onto slice plane within a z-window
    if not args.no_atoms:
        axis_idx = "xyz".index(args.axis)
        plane_pos = origin[axis_idx] + voxels[axis_idx, axis_idx] * idx
        plot_axes = [i for i in range(3) if i != axis_idx]
        for Z, xyz in atoms:
            if abs(xyz[axis_idx] - plane_pos) > args.atom_z_window:
                continue
            sym = Z_to_symbol(Z)
            u = xyz[plot_axes[0]] - origin[plot_axes[0]]
            v = xyz[plot_axes[1]] - origin[plot_axes[1]]
            col = ELEM_COLOR.get(sym, "#888")
            # Small marker (not Circle patch) — paper figure friendly
            ax.plot(u, v, 'o', markerfacecolor=col, markeredgecolor='white',
                    markeredgewidth=0.8, markersize=8, zorder=5)
            ax.text(u + 0.35, v + 0.35, sym, fontsize=8, color='white',
                    ha='left', va='bottom', zorder=6,
                    bbox=dict(boxstyle='round,pad=0.15',
                              facecolor='black', alpha=0.55, edgecolor='none'))

    ax.set_xlabel(xlab); ax.set_ylabel(ylab)
    ax.set_xlim(extent[0], extent[1]); ax.set_ylim(extent[2], extent[3])
    ax.set_title(f"ELF slice ({args.axis}={args.frac:.2f}) — {args.label}",
                 fontsize=12)
    plt.tight_layout()
    plt.savefig(args.out, dpi=args.dpi, bbox_inches='tight', facecolor='white')
    print(f"\n→ {args.out}")


if __name__ == "__main__":
    main()

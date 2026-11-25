#!/usr/bin/env python3
"""3D ELF isosurface render from QE Gaussian-cube output.

Uses skimage.measure.marching_cubes to extract the iso-surface at a given
ELF level (typical 0.85 for paper-grade) and renders with matplotlib's
3D toolkit. Atom positions overlaid as colored spheres (Jmol-like).

Output: PNG (3D view, paper-figure quality).

Usage:
    python3 plot_elf_3d_iso.py \\
        --cube V0_ELF.cube --out V0_ELF_iso.png \\
        --iso 0.85 --view 30 -60
"""
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


ELEM_COLOR = {
    "Li": "#1a1a1a", "P": "#FF9933", "S": "#FFDC52",
    "Cl": "#3E8E41", "N": "#3F7BB6", "C": "#222222",
}
ELEM_R = {
    "Li": 0.65, "P": 0.85, "S": 0.85, "Cl": 0.85,
    "N": 0.70, "C": 0.70,
}


def read_cube(cube_path):
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
        xyz = np.array([float(x) for x in parts[2:5]]) * BOHR
        atoms.append((Z, xyz))
    data_lines = lines[6 + natoms:]
    raw = " ".join(data_lines).split()
    arr = np.array([float(x) for x in raw], dtype=float)
    nx, ny, nz = grid_n
    data = arr.reshape(nx, ny, nz)
    return data, origin, voxels, atoms


def Z_to_symbol(Z):
    PT = {3: "Li", 6: "C", 7: "N", 8: "O", 9: "F",
          11: "Na", 15: "P", 16: "S", 17: "Cl",
          20: "Ca", 35: "Br"}
    return PT.get(Z, f"Z{Z}")


def sphere_mesh(center, radius, n=14):
    """Generate (x, y, z) for plot_surface."""
    u = np.linspace(0, 2 * np.pi, n)
    v = np.linspace(0, np.pi, n // 2 + 1)
    x = center[0] + radius * np.outer(np.cos(u), np.sin(v))
    y = center[1] + radius * np.outer(np.sin(u), np.sin(v))
    z = center[2] + radius * np.outer(np.ones_like(u), np.cos(v))
    return x, y, z


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cube", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--iso", type=float, default=0.85,
                    help="ELF isosurface level (paper standard 0.85)")
    ap.add_argument("--view", type=float, nargs=2, default=[25, -55],
                    help="elev azim viewing angles")
    ap.add_argument("--alpha", type=float, default=0.40,
                    help="ELF isosurface transparency")
    ap.add_argument("--iso_color", default="#FDD96A")
    ap.add_argument("--bg", default="white")
    ap.add_argument("--show_atoms", action="store_true", default=False,
                    help="overlay atoms as small markers (off → clean iso only)")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--label", default="modelC_v3 (LPSCl1.6)",
                    help="system label shown in the plot title "
                         "(e.g. 'comp1 (LPSCl)')")
    args = ap.parse_args()

    try:
        from skimage.measure import marching_cubes
    except ImportError:
        raise SystemExit("scikit-image required: pip install scikit-image")

    data, origin, voxels, atoms = read_cube(Path(args.cube))
    print(f"Cube grid: {data.shape}")
    print(f"  ELF range: [{data.min():.3f}, {data.max():.3f}]")
    print(f"  iso level: {args.iso}")

    if args.iso < data.min() or args.iso > data.max():
        print(f"  [warn] iso level {args.iso} outside ELF range")

    # Marching cubes — output vertices in voxel-index space
    verts, faces, normals, _ = marching_cubes(data, level=args.iso)
    # Convert voxel indices to Cartesian
    verts_xyz = origin + verts @ voxels
    print(f"  iso-surface mesh: {len(verts)} vertices, {len(faces)} faces")

    fig = plt.figure(figsize=(9, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Iso-surface as triangle mesh
    mesh = Poly3DCollection(verts_xyz[faces], alpha=args.alpha,
                              edgecolor='none', facecolor=args.iso_color,
                              linewidth=0)
    ax.add_collection3d(mesh)

    # Atoms as small markers (only if requested)
    if args.show_atoms:
        for Z, xyz in atoms:
            sym = Z_to_symbol(Z)
            col = ELEM_COLOR.get(sym, "#888")
            ax.scatter(xyz[0], xyz[1], xyz[2], c=col, s=35,
                       edgecolors='k', linewidths=0.4, depthshade=False)

    # Cell bounding box
    cell = voxels * np.array(data.shape)[:, None]
    corners = []
    for i in (0, 1):
        for j in (0, 1):
            for k in (0, 1):
                corners.append(origin + i*cell[0] + j*cell[1] + k*cell[2])
    corners = np.array(corners)
    edges = [(0,1),(0,2),(0,4),(1,3),(1,5),(2,3),(2,6),
             (3,7),(4,5),(4,6),(5,7),(6,7)]
    for e in edges:
        ax.plot(*corners[list(e)].T, color='#aaa', lw=0.6, alpha=0.5)

    # View + aesthetics
    ax.view_init(elev=args.view[0], azim=args.view[1])
    xmin, xmax = corners[:,0].min(), corners[:,0].max()
    ymin, ymax = corners[:,1].min(), corners[:,1].max()
    zmin, zmax = corners[:,2].min(), corners[:,2].max()
    ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax); ax.set_zlim(zmin, zmax)
    ax.set_box_aspect((xmax-xmin, ymax-ymin, zmax-zmin))
    ax.set_xlabel("x (Å)"); ax.set_ylabel("y (Å)"); ax.set_zlabel("z (Å)")
    ax.set_title(f"ELF iso-surface @ {args.iso} — {args.label}",
                 fontsize=12)
    # Remove grid
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.fill = False
        axis._axinfo['grid']['color'] = (0.9, 0.9, 0.9, 0.5)
    fig.patch.set_facecolor(args.bg)
    ax.set_facecolor(args.bg)

    plt.tight_layout()
    plt.savefig(args.out, dpi=args.dpi, bbox_inches='tight',
                 facecolor=args.bg)
    print(f"\n→ {args.out}")


if __name__ == "__main__":
    main()

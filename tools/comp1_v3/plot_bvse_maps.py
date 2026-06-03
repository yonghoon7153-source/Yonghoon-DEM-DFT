#!/usr/bin/env python3
"""2D slice + 3D iso-surface plots for the BVSE map.

Reads V0_bvse_map.npy (3D scalar) and V0_init.cif (cell + atoms).

  --mode slice : axial 2D heat-map (xy at z=0.5, etc.) with atoms overlaid
  --mode iso   : 3D iso-surface at user-set energy threshold (low BVSE
                 region = Li migration channel) with Jmol-colored atoms

Usage:
    # 2D xy slice through z=0.5
    python3 plot_bvse_maps.py --mode slice --npy V0_bvse_map.npy \\
        --cif V0_init.cif --axis z --frac 0.5 --out V0_BVSE_xy.png

    # 3D iso at BVSE = (min + 0.3)
    python3 plot_bvse_maps.py --mode iso --npy V0_bvse_map.npy \\
        --cif V0_init.cif --iso_above_min 0.3 --out V0_BVSE_iso.png
"""
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from ase.io import read


ELEM_COLOR = {
    "Li": "#9E9E9E", "P": "#FF9933", "S": "#FFDC52", "Cl": "#3E8E41",
}
ELEM_R = {"Li": 0.50, "P": 0.85, "S": 0.85, "Cl": 0.85}


def plot_slice(npy_path, cif_path, axis, frac, out_path,
                vmax=None, cmap="viridis_r", atoms_on=True):
    bvse = np.load(npy_path)
    atoms = read(cif_path)
    cell = np.array(atoms.get_cell())
    nx, ny, nz = bvse.shape

    # Pick slice index
    ax_i = {"x": 0, "y": 1, "z": 2}[axis]
    n_axis = bvse.shape[ax_i]
    iz = int(round(frac * n_axis)) % n_axis

    if axis == "z":
        slice_2d = bvse[:, :, iz]
        u_vec, v_vec = cell[0], cell[1]
        proj = lambda fx, fy: (fx * np.linalg.norm(u_vec),
                                fy * np.linalg.norm(v_vec))
        u_label = "x (Å)"; v_label = "y (Å)"
    elif axis == "y":
        slice_2d = bvse[:, iz, :]
        u_vec, v_vec = cell[0], cell[2]
        u_label = "x (Å)"; v_label = "z (Å)"
    elif axis == "x":
        slice_2d = bvse[iz, :, :]
        u_vec, v_vec = cell[1], cell[2]
        u_label = "y (Å)"; v_label = "z (Å)"

    # Cap colormap for paper visibility
    if vmax is None:
        # 90th percentile of finite values, since BVSE has long tail
        vmax = float(np.percentile(slice_2d, 90))

    fig, ax = plt.subplots(figsize=(8, 7))
    extent = [0, np.linalg.norm(u_vec), 0, np.linalg.norm(v_vec)]
    im = ax.imshow(slice_2d.T, origin="lower", extent=extent,
                    cmap=cmap, vmin=0, vmax=vmax, aspect="equal")
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(r"BVSE = (BVS − 1)$^2$", fontsize=12)

    # Atom overlay — project atoms onto this plane if within slice thickness
    if not atoms_on:
        ax.set_xlabel(u_label, fontsize=12)
        ax.set_ylabel(v_label, fontsize=12)
        ax.set_title(f"BVSE slice along {axis}={frac:.2f}  "
                      f"(min={float(slice_2d.min()):.3f}, "
                      f"vmax={vmax:.3f})", fontsize=11)
        plt.tight_layout()
        plt.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
        print(f"→ {out_path}")
        return
    inv_cell = np.linalg.inv(cell)
    frac_thick = 1.0 / (2 * n_axis)  # ± half-grid
    for at in atoms:
        f = at.position @ inv_cell
        f = f % 1.0
        ax_f = f[ax_i]
        target_f = iz / n_axis
        dz = abs(ax_f - target_f)
        dz = min(dz, 1 - dz)  # PBC
        if dz < 0.15:  # within 15% of cell along axis
            if axis == "z":
                uu, vv = f[0] * np.linalg.norm(u_vec), f[1] * np.linalg.norm(v_vec)
            elif axis == "y":
                uu, vv = f[0] * np.linalg.norm(u_vec), f[2] * np.linalg.norm(v_vec)
            else:
                uu, vv = f[1] * np.linalg.norm(u_vec), f[2] * np.linalg.norm(v_vec)
            sym = at.symbol
            ax.scatter(uu, vv, s=180 * ELEM_R.get(sym, 0.6) ** 2,
                        c=ELEM_COLOR.get(sym, "#888"),
                        edgecolors="black", lw=0.8,
                        alpha=1.0 - 1.5 * dz, zorder=3)

    ax.set_xlabel(u_label, fontsize=12)
    ax.set_ylabel(v_label, fontsize=12)
    ax.set_title(f"BVSE slice along {axis}={frac:.2f}  "
                  f"(min={float(slice_2d.min()):.3f}, "
                  f"vmax={vmax:.3f})", fontsize=11)
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"→ {out_path}")


def plot_iso(npy_path, cif_path, iso_above_min, out_path,
              view_angles=(25, -60), atoms_on=True):
    try:
        from skimage.measure import marching_cubes
    except ImportError:
        raise SystemExit("Need scikit-image: pip install scikit-image")

    bvse = np.load(npy_path)
    atoms = read(cif_path)
    cell = np.array(atoms.get_cell())
    bmin = float(bvse.min())
    iso_level = bmin + iso_above_min
    print(f"BVSE iso surface at {iso_level:.3f}  (min={bmin:.3f}, "
          f"above_min={iso_above_min})")

    # Pad with periodic wrap so iso wraps cleanly
    pad = np.pad(bvse, 1, mode="wrap")
    try:
        verts, faces, _, _ = marching_cubes(pad, level=iso_level)
        # un-pad (subtract 1)
        verts = verts - 1
    except (ValueError, RuntimeError) as e:
        raise SystemExit(f"marching_cubes failed: {e}")

    # Convert grid coords → cartesian via cell
    nx, ny, nz = bvse.shape
    frac = verts / np.array([nx, ny, nz])
    cart = frac @ cell

    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    fig = plt.figure(figsize=(9, 8))
    ax = fig.add_subplot(111, projection="3d")
    poly = Poly3DCollection(cart[faces], alpha=0.5, facecolor="#3F7BB6",
                             edgecolor="none")
    ax.add_collection3d(poly)

    if atoms_on:
        inv_cell = np.linalg.inv(cell)
        for at in atoms:
            f = (at.position @ inv_cell) % 1.0
            p = f @ cell
            sym = at.symbol
            ax.scatter(p[0], p[1], p[2],
                        s=240 * ELEM_R.get(sym, 0.6) ** 2,
                        c=ELEM_COLOR.get(sym, "#888"),
                        edgecolors="black", lw=0.6, depthshade=False)

    # Axes — bounding box from ALL 8 cell corners (handles non-orthorhombic
    # cells like rhombohedral where cell vectors aren't aligned with xyz).
    corners = np.array([fa * cell[0] + fb * cell[1] + fc * cell[2]
                          for fa in (0, 1) for fb in (0, 1) for fc in (0, 1)])
    xmin, xmax = corners[:, 0].min(), corners[:, 0].max()
    ymin, ymax = corners[:, 1].min(), corners[:, 1].max()
    zmin, zmax = corners[:, 2].min(), corners[:, 2].max()
    ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax); ax.set_zlim(zmin, zmax)
    # Draw cell edges (12 edges of parallelepiped) for orientation reference
    edges = [(0,1),(0,2),(0,4),(1,3),(1,5),(2,3),(2,6),(3,7),(4,5),(4,6),(5,7),(6,7)]
    for e in edges:
        ax.plot([corners[e[0],0], corners[e[1],0]],
                [corners[e[0],1], corners[e[1],1]],
                [corners[e[0],2], corners[e[1],2]],
                color='#888', lw=0.6, alpha=0.5)
    ax.set_xlabel("x (Å)"); ax.set_ylabel("y (Å)"); ax.set_zlabel("z (Å)")
    ax.view_init(*view_angles)
    ax.set_title(f"BVSE iso = {iso_level:.3f} (min + {iso_above_min})  "
                  f"— Li channel surface", fontsize=10)
    ax.set_box_aspect([xmax - xmin, ymax - ymin, zmax - zmin])
    plt.tight_layout()
    plt.savefig(out_path, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"→ {out_path}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["slice", "iso"], required=True)
    ap.add_argument("--npy", required=True)
    ap.add_argument("--cif", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--axis", default="z", help="slice axis (x/y/z)")
    ap.add_argument("--frac", type=float, default=0.5,
                    help="slice fractional position")
    ap.add_argument("--vmax", type=float, default=None,
                    help="2D colormap upper limit (default 90th pct)")
    ap.add_argument("--cmap", default="viridis_r")
    ap.add_argument("--iso_above_min", type=float, default=0.3,
                    help="iso level = bvse_min + this value")
    ap.add_argument("--view", type=float, nargs=2, default=[25, -60],
                    help="3D view (elev azim)")
    ap.add_argument("--no_atoms", action="store_true")
    args = ap.parse_args()

    if args.mode == "slice":
        plot_slice(args.npy, args.cif, args.axis, args.frac,
                    args.out, vmax=args.vmax, cmap=args.cmap,
                    atoms_on=not args.no_atoms)
    else:
        plot_iso(args.npy, args.cif, args.iso_above_min, args.out,
                  view_angles=tuple(args.view),
                  atoms_on=not args.no_atoms)


if __name__ == "__main__":
    main()

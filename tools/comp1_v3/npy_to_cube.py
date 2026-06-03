#!/usr/bin/env python3
"""Convert BVSE .npy + structure (CIF) to Gaussian .cube for VESTA.

VESTA reads .cube format natively for isosurface rendering. This script
takes a 3-D scalar map (e.g. V0_bvse_map.npy or V0_bvs_map.npy) plus the
matching atomic structure (CIF) and writes a Gaussian-cube file that
VESTA / pymol / etc. can open directly.

The map grid is assumed to be defined on the unit-cell axes
(nx × ny × nz fractional grid points). Cube voxel vectors are computed
from cell / shape.

Usage:
    python3 npy_to_cube.py --npy V0_bvse_map.npy --cif V0_init.cif \\
        --out V0_BVSE.cube --comment "BVSE = (BVS-1)^2"
"""
import argparse
from pathlib import Path
import numpy as np
from ase.io import read


# Z (atomic number) lookup — VESTA needs Z, not symbol
Z = {"H": 1, "Li": 3, "C": 6, "N": 7, "O": 8, "F": 9,
     "Na": 11, "P": 15, "S": 16, "Cl": 17,
     "Br": 35, "I": 53,
     "Nd": 60}
BOHR = 1.8897259886  # 1 Å in Bohr


def write_cube(out_path, atoms, data, comment="BVSE map"):
    """Write Gaussian cube with map data in (nx, ny, nz)."""
    cell = np.array(atoms.get_cell())             # Å
    positions = atoms.get_positions()             # Å
    symbols = atoms.get_chemical_symbols()
    nx, ny, nz = data.shape
    voxel = cell / np.array([[nx], [ny], [nz]])   # Å, row = voxel along axis
    # VESTA expects "origin then 3 voxel vectors" all in Bohr; positive
    # nx/ny/nz means Bohr units. Use Bohr throughout to be safe.
    voxel_b = voxel * BOHR
    origin_b = np.zeros(3)
    pos_b = positions * BOHR

    n_atoms = len(atoms)
    lines = []
    lines.append(comment)
    lines.append("Generated from .npy via npy_to_cube.py")
    lines.append(f"{n_atoms:5d} {origin_b[0]:12.6f} {origin_b[1]:12.6f} "
                  f"{origin_b[2]:12.6f}")
    for n_i, v_i in zip([nx, ny, nz], voxel_b):
        lines.append(f"{n_i:5d} {v_i[0]:12.6f} {v_i[1]:12.6f} {v_i[2]:12.6f}")
    for sym, p in zip(symbols, pos_b):
        z = Z.get(sym, 0)
        lines.append(f"{z:5d} {0.0:12.6f} {p[0]:12.6f} {p[1]:12.6f} {p[2]:12.6f}")

    # Data: x slowest, z fastest, 6 values per line
    flat = data.flatten(order="C")  # C order = x slow, z fast — same as cube
    for i in range(0, flat.size, 6):
        chunk = flat[i:i + 6]
        lines.append(" ".join(f"{v:13.5e}" for v in chunk))

    out_path = Path(out_path)
    out_path.write_text("\n".join(lines) + "\n")
    print(f"→ {out_path}  ({n_atoms} atoms, {nx}×{ny}×{nz} grid, "
          f"data range [{data.min():.3e}, {data.max():.3e}])")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--npy", required=True)
    ap.add_argument("--cif", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--comment", default="BVSE map (Bond-Valence Site Energy)")
    ap.add_argument("--clip_max", type=float, default=None,
                    help="optional upper clip for the data values "
                         "(e.g. 50 to suppress anion cores in iso views)")
    args = ap.parse_args()

    data = np.load(args.npy)
    atoms = read(args.cif)
    print(f"Loaded: {args.npy}  shape={data.shape}, "
          f"range=[{data.min():.3e}, {data.max():.3e}]")
    print(f"        {args.cif}  natoms={len(atoms)}, "
          f"V={atoms.get_volume():.3f} Å³")
    if args.clip_max is not None:
        n_clipped = int((data > args.clip_max).sum())
        data = np.clip(data, None, args.clip_max)
        print(f"Clipped {n_clipped} voxels above {args.clip_max}")
    write_cube(args.out, atoms, data, args.comment)


if __name__ == "__main__":
    main()

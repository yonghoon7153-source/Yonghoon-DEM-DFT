"""make_comp35_v2_slab.py -- generate 2x2x1 supercell slab from V0 bulk xyz.

For comp3 v2 / comp5 v2 (Li5.4 family). Input: bulk V0 from KISTI tight relax
(or partially relaxed). Output: slab xyz suitable for z-profile / face_flip
inspection.

Steps:
  1. Read bulk V0 xyz (62 atoms, rhombo cell with a1/a2 z components ~3.53)
  2. 2x2x1 supercell via ase.repeat (248 atoms)
  3. Add vacuum on z (default 30 A)
  4. Translate atoms so bottom face is at z=0
  5. Save as extxyz

Usage on gabia:
  cd /data/work/v30u_ensemble
  wget -O make_comp35_v2_slab.py \
    "https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/claude/debug-api-500-error-iukkt/tools/make_comp35_v2_slab.py?$(date +%s)"
  python3 make_comp35_v2_slab.py
"""
import sys
from pathlib import Path
from ase.io import read, write

WORK = Path('/data/work/v30u_ensemble')
VACUUM = 30.0  # A vacuum on top in z

INPUTS = {
    'comp3_v2': 'comp3_v2_V0_step32.xyz',
    'comp5_v2': 'comp5_v2_V0_step31.xyz',
}


def make_slab(bulk_xyz, slab_xyz, vacuum=30.0):
    bulk = read(bulk_xyz)
    print(f"\n=== {bulk_xyz} ===")
    print(f"  Bulk: {len(bulk)} atoms, V={bulk.get_volume():.2f} A^3")
    print(f"  Cell:\n    a1 = {bulk.cell.array[0]}\n    a2 = {bulk.cell.array[1]}\n    a3 = {bulk.cell.array[2]}")
    print(f"  Bulk z range: {bulk.positions[:,2].min():.2f} - {bulk.positions[:,2].max():.2f}")

    # 2x2x1 supercell
    slab = bulk.repeat((2, 2, 1))
    print(f"\n  After 2x2x1: {len(slab)} atoms")
    print(f"  Cell:\n    a1 = {slab.cell.array[0]}\n    a2 = {slab.cell.array[1]}\n    a3 = {slab.cell.array[2]}")
    z_min0 = slab.positions[:, 2].min()
    z_max0 = slab.positions[:, 2].max()
    print(f"  Supercell z range: {z_min0:.2f} - {z_max0:.2f}, thickness {z_max0 - z_min0:.2f}")

    # Add vacuum on z (extend a3 z-component)
    cell = slab.cell.array.copy()
    cell[2, 2] = cell[2, 2] + vacuum
    slab.set_cell(cell, scale_atoms=False)
    slab.pbc = [True, True, True]

    # Translate so bottom is at z=0
    z_min = slab.positions[:, 2].min()
    slab.translate([0, 0, -z_min])

    z_final_min = slab.positions[:, 2].min()
    z_final_max = slab.positions[:, 2].max()
    print(f"\n  After vacuum + translate:")
    print(f"  Cell:\n    a1 = {slab.cell.array[0]}\n    a2 = {slab.cell.array[1]}\n    a3 = {slab.cell.array[2]}")
    print(f"  Final z range: {z_final_min:.2f} - {z_final_max:.2f}, thickness {z_final_max - z_final_min:.2f}")
    print(f"  Vacuum above: {slab.cell.array[2,2] - z_final_max:.2f} A")

    write(slab_xyz, slab, format='extxyz')
    print(f"  Saved: {slab_xyz}")

    # Composition
    syms = slab.get_chemical_symbols()
    comp = {s: syms.count(s) for s in set(syms)}
    print(f"  Composition: {comp}")


def main():
    for name, fn in INPUTS.items():
        bulk_path = WORK / fn
        slab_path = WORK / f"{name}_slab.xyz"
        if not bulk_path.exists():
            print(f"SKIP {name}: {bulk_path} not found")
            continue
        make_slab(bulk_path, slab_path, VACUUM)


if __name__ == "__main__":
    main()

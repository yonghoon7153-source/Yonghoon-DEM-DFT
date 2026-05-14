"""
verify_slabs.py — Verify slab generation integrity

체크 항목:
  1. Original V0 cell parameters
  2. Orthogonalize 전후 atomic position 비교
  3. Bond length distribution (orig vs ortho vs repeat)
  4. Cell shape (a3 z-only 확인)
  5. Atom count + density
  6. SE thickness (z extent)
  7. Surface termination (top/bottom layer 분석)

==========================================================================
SOURCE: KISTI /scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2/verify_slabs.py
        (사용자가 paste, 2026-05-14)
주의: V2_FILES 경로는 KISTI 기준. 로컬 실행 시 경로 조정 필요.
      orthogonalize 는 verify 용이며 PRESERVED 슬랩에는 사용자가 별도 단계로 적용.
==========================================================================
"""
import argparse
import numpy as np
from ase.io import read, write
from pathlib import Path

V2_FILES = {
    'comp1':  '/scratch/x3430a02/kgy/manuscript_support/post_relax_comp1_v2/comp1v2_scf.out',
    'comp2':  '/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/comp2_lpscbr/v2_postproc/comp2_v2_V0.xyz',
    'modelC': '/scratch/x3430a02/kgy/manuscript_support/pipeline_v2/modelC_lpsc16/v2_postproc/gabia_pkg/modelc_v2_V0.xyz',
}

REPEAT_LI6 = (2, 2, 3)
REPEAT_LI5P4 = (2, 2, 1)

def load_orig(path):
    if path.endswith('.out'):
        return read(path, format='espresso-out', index=-1)
    return read(path)

def measure_bonds(atoms, label):
    """Bond length statistics."""
    syms = np.array(atoms.get_chemical_symbols())
    p_idx = np.where(syms == 'P')[0]
    s_idx = np.where(syms == 'S')[0]
    li_idx = np.where(syms == 'Li')[0]
    cl_idx = np.where(syms == 'Cl')[0]
    br_idx = np.where(syms == 'Br')[0]

    print(f"\n  --- Bond stats: {label} ---")

    # P-S
    ds = []
    for i in p_idx:
        for j in s_idx:
            d = atoms.get_distance(i, j, mic=True)
            if d < 2.3: ds.append(d)
    if ds:
        print(f"  P-S:  n={len(ds):3d}  mean={np.mean(ds):.4f}  std={np.std(ds):.4f}  range=[{min(ds):.3f}, {max(ds):.3f}]")

    # Li-S
    ds = []
    for i in li_idx:
        for j in s_idx:
            d = atoms.get_distance(i, j, mic=True)
            if d < 3.0: ds.append(d)
    if ds:
        print(f"  Li-S: n={len(ds):3d}  mean={np.mean(ds):.4f}  std={np.std(ds):.4f}")

    # Li-Cl
    if len(cl_idx) > 0:
        ds = []
        for i in li_idx:
            for j in cl_idx:
                d = atoms.get_distance(i, j, mic=True)
                if d < 3.2: ds.append(d)
        if ds:
            print(f"  Li-Cl: n={len(ds):3d}  mean={np.mean(ds):.4f}  std={np.std(ds):.4f}")

    # Li-Br
    if len(br_idx) > 0:
        ds = []
        for i in li_idx:
            for j in br_idx:
                d = atoms.get_distance(i, j, mic=True)
                if d < 3.4: ds.append(d)
        if ds:
            print(f"  Li-Br: n={len(ds):3d}  mean={np.mean(ds):.4f}  std={np.std(ds):.4f}")

def cell_info(atoms, label):
    cell = atoms.cell.array
    a, b, c = np.linalg.norm(cell[0]), np.linalg.norm(cell[1]), np.linalg.norm(cell[2])
    print(f"\n  --- {label} ---")
    print(f"  Atoms: {len(atoms)}, V={atoms.get_volume():.2f} Å³")
    print(f"  a1: [{cell[0,0]:.3f}, {cell[0,1]:.3f}, {cell[0,2]:.3f}]  |a1|={a:.4f}")
    print(f"  a2: [{cell[1,0]:.3f}, {cell[1,1]:.3f}, {cell[1,2]:.3f}]  |a2|={b:.4f}")
    print(f"  a3: [{cell[2,0]:.3f}, {cell[2,1]:.3f}, {cell[2,2]:.3f}]  |a3|={c:.4f}")

    # Cell shape detection
    a3_xy = abs(cell[2,0]) + abs(cell[2,1])
    if a3_xy > 0.01:
        print(f"  ⚠️  a3 xy components: {a3_xy:.3f} Å (rhombo, NEEDS ORTHOGONALIZE)")
    else:
        print(f"  ✓  a3 z-only (cubic or already orthogonalized)")

    # Z extent
    pos = atoms.get_positions()
    z_extent = pos[:,2].max() - pos[:,2].min()
    print(f"  z extent (atoms): {z_extent:.2f} Å")

    # Atomic density
    print(f"  Density: {len(atoms)/atoms.get_volume():.3f} atoms/Å³")

    # XY cross-section area (for adhesion A calculation)
    A = np.linalg.norm(np.cross(cell[0], cell[1]))
    print(f"  XY area (a1×a2): {A:.2f} Å²")

def orthogonalize(atoms):
    """Remove a3 xy components, keep z."""
    cell = atoms.cell.array.copy()
    if abs(cell[2,0]) < 0.01 and abs(cell[2,1]) < 0.01:
        return atoms.copy()  # already orthogonal

    # Save fractional positions BEFORE cell change
    frac = atoms.get_scaled_positions()

    # New cell: a3 = (0, 0, |a3|_z) only
    new_cell = cell.copy()
    new_cell[2] = [0, 0, cell[2,2]]

    # Apply: keep fractional positions same, but cartesian recomputed
    new_atoms = atoms.copy()
    new_atoms.set_cell(new_cell, scale_atoms=False)  # don't scale; just change cell
    new_atoms.set_scaled_positions(frac)  # then re-set fracs

    return new_atoms

def main():
    for comp, path in V2_FILES.items():
        print(f"\n{'='*70}")
        print(f"### {comp}: {path}")
        print(f"{'='*70}")

        if not Path(path).exists():
            print(f"  ❌ File not found")
            continue

        # 1. Load original
        orig = load_orig(path)
        cell_info(orig, "ORIGINAL")
        measure_bonds(orig, "ORIGINAL")

        # 2. Orthogonalize
        ortho = orthogonalize(orig)
        cell_info(ortho, "ORTHOGONALIZED")
        measure_bonds(ortho, "ORTHOGONALIZED")

        # Compare bonds
        # ... done implicitly in measure_bonds output

        # 3. Repeat
        if comp in ['comp1', 'comp2']:
            rep = REPEAT_LI6
        else:
            rep = REPEAT_LI5P4

        slab = ortho.repeat(rep)
        cell_info(slab, f"AFTER REPEAT {rep}")
        measure_bonds(slab, f"REPEAT {rep}")

        # Save
        outname = f"{comp}_slab_v2.xyz"
        write(outname, slab)
        print(f"\n  ✓ Saved: {outname}")

    print(f"\n{'='*70}")
    print("=== Summary ===")
    print(f"{'='*70}")
    print("Check above for:")
    print("  1. Cell shape: a3 should be z-only after orthogonalize")
    print("  2. Bond lengths: ORIGINAL vs ORTHOGONALIZED should be IDENTICAL")
    print("     (orthogonalization shouldn't change bonds!)")
    print("  3. REPEAT bonds should match ORIGINAL bonds (just more atoms)")
    print("  4. SE thickness ~30 Å for adhesion")
    print("  5. Density consistent across comp1/2/modelC")

if __name__ == '__main__':
    main()

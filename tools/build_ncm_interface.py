#!/usr/bin/env python3
"""
Build SE/LiNiO2 interface xyz with configurable NCM facet.

- SE: read from CIF (e.g. V0 structure from /data/work/bml/manuscript_support/...)
- NCM: LiNiO2 (R-3m) slab generated at chosen Miller plane
- Stack: SE strained to match NCM xy, gap=2.5 Å, vacuum=30 Å
- Save interface.xyz in the same atom-order convention as v5/v6 (NCM first, SE second)
  so plot_binding_curve_cif.py / adhesion_v6_anneal_test.py can use it directly.

Usage:
    # (104) facet (Choi 2025 convention)
    python tools/build_ncm_interface.py \\
        --se-cif /data/work/bml/manuscript_support/comp1_lpsc10/eos/v102.cif \\
        --facet 104 \\
        --se-repeat 2 2 1 \\
        --out comp1_104_s0.xyz

    # (001) facet (original paper convention)
    python tools/build_ncm_interface.py --se-cif X.cif --facet 001 ...
"""
import argparse
from pathlib import Path
import numpy as np


def build_ncm_slab(facet=(1, 0, 4), min_slab=10.0, min_vac=2.0, target_xy=None):
    """
    Build LiNiO2 slab at requested (hkl) facet using pymatgen.

    Returns ase.Atoms (no vacuum, compact slab with NCM first).
    target_xy: (a_target, b_target) in Å → pick orthogonal slab closest; otherwise first.
    """
    from pymatgen.core import Structure, Lattice
    from pymatgen.core.surface import SlabGenerator
    from pymatgen.io.ase import AseAtomsAdaptor

    # LiNiO2 bulk (R-3m, hexagonal setting)
    lat_hex = Lattice.hexagonal(2.878, 14.19)
    bulk = Structure(
        lat_hex,
        ["Li", "Ni", "O", "O"],
        [[0, 0, 0.5], [0, 0, 0], [0, 0, 0.2584], [0, 0, 0.7416]],
    )

    gen = SlabGenerator(
        bulk,
        miller_index=facet,
        min_slab_size=min_slab,
        min_vacuum_size=min_vac,
        center_slab=True,
        in_unit_planes=False,
    )
    slabs = gen.get_slabs(symmetrize=False)
    if not slabs:
        raise RuntimeError(f"No slabs found for facet {facet}")

    # Pick stoichiometric or smallest slab
    slab = slabs[0]
    print(f"  NCM ({facet[0]}{facet[1]}{facet[2]}) slab: "
          f"{len(slab)} atoms, lattice "
          f"a={slab.lattice.a:.2f}, b={slab.lattice.b:.2f}, "
          f"c={slab.lattice.c:.2f}, γ={slab.lattice.gamma:.1f}°")

    return AseAtomsAdaptor.get_atoms(slab)


def stack_interface(ncm_atoms, se_atoms, gap=2.5, vacuum=30.0, dx=0.0, dy=0.0):
    """Stack SE on NCM, strain SE to NCM xy, return combined Atoms."""
    from ase import Atoms

    ncm_cell = ncm_atoms.cell.array.copy()
    se_cart = se_atoms.get_positions().copy()

    # Fractional in NCM cell (applies xy strain)
    ncm_inv = np.linalg.inv(ncm_cell)
    se_frac = se_cart @ ncm_inv

    # xy shift
    se_frac[:, 0] = (se_frac[:, 0] + dx) % 1.0
    se_frac[:, 1] = (se_frac[:, 1] + dy) % 1.0

    # Back to Cartesian
    se_pos = se_frac @ ncm_cell

    # Center NCM z_min = 0
    ncm_pos = ncm_atoms.get_positions().copy()
    ncm_pos[:, 2] -= ncm_pos[:, 2].min()
    ncm_zmax = ncm_pos[:, 2].max()

    # Place SE above with gap
    se_pos[:, 2] -= se_pos[:, 2].min()
    se_pos[:, 2] += ncm_zmax + gap
    se_zmax = se_pos[:, 2].max()

    # Combined cell (NCM xy, z = total + vacuum)
    combined_cell = ncm_cell.copy()
    combined_cell[2] = [0, 0, se_zmax + vacuum]

    symbols = list(ncm_atoms.symbols) + list(se_atoms.symbols)
    positions = np.vstack([ncm_pos, se_pos])
    interface = Atoms(symbols=symbols, positions=positions,
                      cell=combined_cell, pbc=True)

    # Stats
    ncm_ab = np.linalg.norm(ncm_cell[0]), np.linalg.norm(ncm_cell[1])
    se_ab = np.linalg.norm(se_atoms.cell[0]), np.linalg.norm(se_atoms.cell[1])
    strain = (ncm_ab[0] / se_ab[0] - 1.0, ncm_ab[1] / se_ab[1] - 1.0)
    print(f"  Strain imposed on SE: a={strain[0]*100:+.2f}%, b={strain[1]*100:+.2f}%")

    return interface, len(ncm_atoms)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--se-cif", required=True, help="SE bulk CIF")
    ap.add_argument("--facet", default="104",
                    help="NCM facet Miller, e.g. '104' or '001'")
    ap.add_argument("--se-repeat", type=int, nargs=3, default=[2, 2, 1],
                    help="SE supercell repeat (default 2 2 1)")
    ap.add_argument("--ncm-repeat", type=int, nargs=2, default=None,
                    help="NCM xy repeat (default: auto to match SE xy within 5%%)")
    ap.add_argument("--gap", type=float, default=2.5)
    ap.add_argument("--vacuum", type=float, default=30.0)
    ap.add_argument("--seed", type=int, default=0,
                    help="xy-shift seed (0 = no shift)")
    ap.add_argument("--min-slab", type=float, default=10.0,
                    help="min NCM slab thickness Å (default 10)")
    ap.add_argument("--out", required=True, help="output xyz path")
    args = ap.parse_args()

    from ase.io import read, write
    from pymatgen.io.ase import AseAtomsAdaptor
    from pymatgen.core import Structure

    facet = tuple(int(c) for c in args.facet)

    # Load SE
    se_struct = Structure.from_file(args.se_cif)
    se_struct.make_supercell(args.se_repeat)
    se = AseAtomsAdaptor.get_atoms(se_struct)
    print(f"SE ({Path(args.se_cif).name}, repeat {args.se_repeat}): {len(se)} atoms")
    print(f"  a={np.linalg.norm(se.cell[0]):.2f}, b={np.linalg.norm(se.cell[1]):.2f}, "
          f"c={np.linalg.norm(se.cell[2]):.2f} Å")

    # Build NCM slab
    ncm = build_ncm_slab(facet=facet, min_slab=args.min_slab)

    # Auto-pick NCM xy repeat to match SE xy within ~5%
    if args.ncm_repeat is None:
        se_a = np.linalg.norm(se.cell[0])
        se_b = np.linalg.norm(se.cell[1])
        ncm_a = np.linalg.norm(ncm.cell[0])
        ncm_b = np.linalg.norm(ncm.cell[1])
        nx = max(1, round(se_a / ncm_a))
        ny = max(1, round(se_b / ncm_b))
    else:
        nx, ny = args.ncm_repeat
    ncm = ncm.repeat((nx, ny, 1))
    print(f"  NCM after xy repeat ({nx},{ny}): {len(ncm)} atoms, "
          f"a={np.linalg.norm(ncm.cell[0]):.2f}, b={np.linalg.norm(ncm.cell[1]):.2f}")

    # Random xy shift (reproducible)
    rng = np.random.RandomState(args.seed)
    dx, dy = (rng.random(), rng.random()) if args.seed > 0 else (0.0, 0.0)

    # Stack
    interface, n_ncm = stack_interface(
        ncm, se, gap=args.gap, vacuum=args.vacuum, dx=dx, dy=dy,
    )
    print(f"  Interface: {len(interface)} atoms (NCM {n_ncm} + SE {len(interface)-n_ncm})")

    # Save
    outpath = Path(args.out)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    write(outpath, interface)
    print(f"\n✓ {outpath}  (n_ncm={n_ncm})")
    print(f"  ※ atom order preserved: first {n_ncm} = NCM, rest = SE")


if __name__ == "__main__":
    main()

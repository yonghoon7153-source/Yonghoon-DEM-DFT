#!/usr/bin/env python3
"""Build QE SCF inputs for DFT verification of UMA NEB images.

Reads a multi-frame xyz (one frame per NEB image) and writes one QE SCF
input per image, all using the same plane-wave settings (so energies are
directly comparable). The geometry of each image is frozen (calculation=
'scf'), giving DFT-grade total energy at the UMA-relaxed configuration.

Use case: compute DFT barrier = max(E_image_i) - E_image_0 using the
UMA-discovered path geometry. This is the standard MLIP → DFT verification
without doing the much more expensive full DFT NEB relaxation.

Usage:
    python3 build_dft_neb_inputs.py \\
        --neb_xyz /path/to/neb_path_final.xyz \\
        --out_dir /path/to/dft_verify \\
        --pseudos Li=li_pbe_v1.4.uspp.F.UPF N=N.pbe-n-radius_5.UPF \\
        --masses Li=6.94 N=14.0067 \\
        --kgrid 2 2 1 \\
        --prefix_base li3n_neb_dft
"""
import argparse
import os
from pathlib import Path


def parse_kv(kv_list):
    out = {}
    for kv in kv_list:
        k, v = kv.split("=", 1)
        out[k] = v
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--neb_xyz", required=True,
                    help="multi-frame xyz from NEB output (e.g. neb_path_final.xyz)")
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--prefix_base", default="neb_dft")
    ap.add_argument("--pseudos", nargs="+", required=True,
                    help="ELEMENT=PSEUDO.UPF pairs, e.g. Li=li_pbe_v1.4.uspp.F.UPF N=N.pbe-n-radius_5.UPF")
    ap.add_argument("--masses", nargs="+", required=True,
                    help="ELEMENT=MASS pairs, e.g. Li=6.94 N=14.0067")
    ap.add_argument("--pseudo_dir", default="/data/work/pseudo")
    ap.add_argument("--ecutwfc", type=float, default=60.0)
    ap.add_argument("--ecutrho", type=float, default=480.0)
    ap.add_argument("--kgrid", type=int, nargs=3, default=[2, 2, 1])
    ap.add_argument("--conv_thr", type=float, default=1e-8)
    ap.add_argument("--degauss", type=float, default=0.01)
    ap.add_argument("--smearing", default="mv")
    args = ap.parse_args()

    pseudos = parse_kv(args.pseudos)
    masses = parse_kv(args.masses)
    if set(pseudos.keys()) != set(masses.keys()):
        raise ValueError("Pseudo and mass element sets must match")

    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)

    from ase.io import read
    import numpy as np
    images = read(args.neb_xyz, index=":")
    print(f"Loaded {len(images)} images from {args.neb_xyz}")

    for i, atoms in enumerate(images):
        n = len(atoms)
        elems_present = sorted(set(atoms.symbols))
        # Check we have pseudos for all elements
        for e in elems_present:
            if e not in pseudos:
                raise ValueError(f"Image {i}: element {e} present but no pseudo provided")

        ntyp = len(elems_present)
        species_block = "ATOMIC_SPECIES\n"
        for e in elems_present:
            species_block += f"  {e:<3} {masses[e]}  {pseudos[e]}\n"

        cell_block = "CELL_PARAMETERS angstrom\n"
        for v in atoms.cell.array:
            cell_block += f"  {v[0]:18.12f}  {v[1]:18.12f}  {v[2]:18.12f}\n"

        pos_block = "ATOMIC_POSITIONS angstrom\n"
        for sym, p in zip(atoms.symbols, atoms.positions):
            pos_block += f"  {sym:<3}  {p[0]:18.12f}  {p[1]:18.12f}  {p[2]:18.12f}\n"

        inp = f"""&CONTROL
  calculation='scf'
  prefix='{args.prefix_base}_img{i}'
  pseudo_dir='{args.pseudo_dir}'
  outdir='./tmp_img{i}/'
  tprnfor=.true.
  tstress=.true.
  verbosity='high'
  disk_io='low'
/
&SYSTEM
  ibrav=0
  nat={n}
  ntyp={ntyp}
  ecutwfc={args.ecutwfc}
  ecutrho={args.ecutrho}
  occupations='smearing'
  smearing='{args.smearing}'
  degauss={args.degauss}
  nosym=.true.
/
&ELECTRONS
  conv_thr={args.conv_thr:.1e}
  mixing_beta=0.3
  electron_maxstep=300
/

{species_block}
K_POINTS automatic
  {args.kgrid[0]} {args.kgrid[1]} {args.kgrid[2]}  0 0 0

{cell_block}
{pos_block}"""

        out = out_dir / f"img{i}.in"
        out.write_text(inp)
        print(f"  → img{i}.in  ({n} atoms, ntyp={ntyp}: {elems_present})")

    print(f"\nNext: run sequentially with QE pw.x")
    print(f"  for i in 0 1 2 3 4 5 6; do")
    print(f"    mpirun -np 1 pw.x -in img$i.in > img$i.out")
    print(f"  done")


if __name__ == "__main__":
    main()

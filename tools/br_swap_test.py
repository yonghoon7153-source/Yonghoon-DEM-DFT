#!/usr/bin/env python3
"""
Br ↔ Cl substitution test — Choi Fig S18 / Table S3 analog.

Isolates halogen-specific bonding contribution by swapping ONE Br ↔ Cl
at the interface layer and recomputing Wad. Direct causal test for
"is Br polarizability the cause of comp2B > comp1 reversal?"

Protocol:
  1. Load interface xyz (relaxed by v5 xy-shift)
  2. Identify interfacial halogen nearest to NCM O
  3. Swap its element (Br -> Cl or Cl -> Br)
  4. UMA single-point or re-relax -> E_int
  5. Separation (SE +30 Å, cell +30 Å) -> E_sep
  6. ΔWad = Wad(swapped) - Wad(original)

Requires: fairchem (UMA), ASE. Run on V100/KISTI.

Usage:
    python tools/br_swap_test.py comp1_v5xy_s45.xyz --swap Cl_to_Br
    python tools/br_swap_test.py comp2B_v5xy_s46.xyz --swap Br_to_Cl
    python tools/br_swap_test.py comp3_v5xy_s45.xyz --swap Br_to_Cl --relax

Output:
    <base>_swap_<mode>.json  — E_int, E_sep, Wad before/after
    <base>_swap_<mode>.xyz   — swapped structure
"""
import argparse
import json
from pathlib import Path

import numpy as np


def load_xyz(path):
    with open(path) as f:
        lines = f.readlines()
    n = int(lines[0].strip())
    header = lines[1].rstrip()
    symbols, coords = [], []
    for line in lines[2:2 + n]:
        parts = line.split()
        symbols.append(parts[0])
        coords.append([float(parts[1]), float(parts[2]), float(parts[3])])
    return symbols, np.array(coords), header


def save_xyz(path, symbols, coords, header="swapped"):
    with open(path, "w") as f:
        f.write(f"{len(symbols)}\n")
        f.write(header + "\n")
        for s, p in zip(symbols, coords):
            f.write(f"{s}  {p[0]:.8f}  {p[1]:.8f}  {p[2]:.8f}\n")


def find_interfacial_halogen(symbols, coords, target):
    """Return index of `target` atom closest to any NCM O atom."""
    symbols = np.asarray(symbols)
    O_pos = coords[symbols == "O"]
    tgt_idx = np.where(symbols == target)[0]
    if len(tgt_idx) == 0:
        raise ValueError(f"No {target} atoms found")
    # distance to nearest O, per target atom
    diff = coords[tgt_idx][:, None, :] - O_pos[None, :, :]
    min_dist = np.linalg.norm(diff, axis=2).min(axis=1)
    return int(tgt_idx[min_dist.argmin()]), float(min_dist.min())


def compute_wad(atoms, n_ncm):
    """Compute Wad via separation method. Requires atoms.calc set."""
    E_int = atoms.get_potential_energy()
    # Separate SE by +30 Å along z, expand cell z by 30 Å
    sep = atoms.copy()
    pos = sep.get_positions()
    pos[n_ncm:, 2] += 30.0
    sep.set_positions(pos)
    cell = sep.cell.array.copy()
    cell[2, 2] += 30.0
    sep.set_cell(cell)
    # New calculator instance to avoid shape mismatch cache issue
    sep.calc = atoms.calc.__class__(
        atoms.calc.predictor, task_name=atoms.calc.task_name
    ) if hasattr(atoms.calc, "predictor") else atoms.calc
    E_sep = sep.get_potential_energy()
    area = np.linalg.norm(np.cross(atoms.cell.array[0], atoms.cell.array[1]))
    Wad = (E_sep - E_int) / area * 16.0218    # eV/Å² -> J/m²
    return Wad, E_int, E_sep, area


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile")
    ap.add_argument("--swap", choices=["Br_to_Cl", "Cl_to_Br"], required=True)
    ap.add_argument("--n-ncm", type=int, default=None,
                    help="Number of NCM atoms (auto-detect: count Ni+Li+O before first P)")
    ap.add_argument("--relax", action="store_true",
                    help="L-BFGS relax after swap (default: single point)")
    ap.add_argument("--device", default="cuda")
    args = ap.parse_args()

    path = Path(args.infile)
    symbols, coords, header = load_xyz(path)
    symbols_arr = np.asarray(symbols)

    # Auto-detect n_ncm: first P atom index
    if args.n_ncm is None:
        p_idx = np.where(symbols_arr == "P")[0]
        if len(p_idx) == 0:
            raise ValueError("No P atom found; cannot auto-detect NCM boundary")
        n_ncm = int(p_idx[0])
        # But SE can have Li too. n_ncm = count of Ni+O+NCM Li (indices < first P)
    else:
        n_ncm = args.n_ncm
    print(f"n_NCM = {n_ncm}, n_total = {len(symbols)}")

    # Identify interfacial halogen to swap
    src, dst = ("Br", "Cl") if args.swap == "Br_to_Cl" else ("Cl", "Br")
    idx, dist_to_O = find_interfacial_halogen(symbols, coords, src)
    print(f"Swapping atom {idx} ({src} → {dst}), distance to nearest O = {dist_to_O:.2f} Å")

    # Build swapped structure
    swapped_symbols = list(symbols)
    swapped_symbols[idx] = dst

    # Save swapped xyz
    out_xyz = path.with_name(f"{path.stem}_swap_{args.swap}.xyz")
    save_xyz(out_xyz, swapped_symbols, coords,
             header=f"{header} SWAP:{src}->{dst} idx={idx}")
    print(f"✓ {out_xyz.name}")

    # Compute Wad with UMA (requires fairchem)
    try:
        from ase import Atoms
        from ase.optimize import LBFGS
        from fairchem.core import pretrained_mlip
        from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    except ImportError as e:
        print(f"\n! fairchem/ASE not available ({e})")
        print("  Template saved. Run on V100/KISTI with UMA environment.")
        return

    predictor = pretrained_mlip.get_predict_unit("uma-s-1p1", device=args.device)

    def new_calc():
        return FAIRChemCalculator(predictor, task_name="omat")

    # Load original cell from header (assume ASE extxyz with Lattice=)
    # Simpler: use ASE's read
    from ase.io import read
    orig = read(path)
    swap = orig.copy()
    swap.symbols[idx] = dst

    results = {}
    for tag, atoms in [("original", orig), ("swapped", swap)]:
        atoms.calc = new_calc()
        if args.relax:
            LBFGS(atoms, logfile=None).run(fmax=0.01, steps=200)
        Wad, E_int, E_sep, area = compute_wad(atoms, n_ncm)
        print(f"  [{tag}] Wad={Wad:.3f} J/m², E_int={E_int:.3f}, E_sep={E_sep:.3f}")
        results[tag] = {
            "Wad": float(Wad), "E_int": float(E_int), "E_sep": float(E_sep),
            "area_A2": float(area),
        }

    results["delta_Wad"] = results["swapped"]["Wad"] - results["original"]["Wad"]
    results["swap_info"] = {
        "mode": args.swap, "atom_index": idx,
        "from": src, "to": dst, "dist_to_O_A": dist_to_O,
        "relax": args.relax,
    }

    out_json = path.with_name(f"{path.stem}_swap_{args.swap}.json")
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n✓ {out_json.name}")
    print(f"ΔWad = {results['delta_Wad']:+.3f} J/m² "
          f"({args.swap} at interface)")


if __name__ == "__main__":
    main()

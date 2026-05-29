#!/usr/bin/env python3
"""Phase A: rigid grid binding-energy scan (no relaxation).

E_bind(dx, dy, dz) = E_complex - E_slab_iso - E_SDCP_iso
all from UMA single-point on the *init* slab (no MLIP relaxation — avoids
the LiNiO2 collapse we saw with omat-task UMA relax). SDCP molecule is
placed with its sulfonate S atom at (dx, dy, z_top + dz), molecule
orientation preserved from ORCA-optimized geometry.

Reference state convention:
- E_slab_iso: UMA SP on the bare slab xyz (no relax)
- E_SDCP_iso: UMA SP on the bare SDCP xyz placed alone in the same cell
  (gas-phase reference inside the periodic box)
- E_complex: UMA SP on (slab atoms + translated SDCP atoms) in same cell

dx,dy span fractional coords [0,1)×[0,1) of the surface ab plane (handles
the oblique LiNiO2 (104) cell with γ≠90°). dz is height above z_top of
the slab in Å.

Usage:
    python3 scan_binding_rigid.py \\
        --slab <slab.xyz> \\
        --molecule <sdcp.xyz> \\
        --out_dir <out> \\
        --form doped|neutral \\
        --nx 10 --ny 10 --dz 2.0 6.0 0.5 \\
        --device cuda
"""
import argparse, json, time
from pathlib import Path
import numpy as np


def find_anchor_S(atoms):
    """Find the sulfonate S atom (the S bonded to 3 O's, not the
    thiophene S which is bonded to 2 C's). Returns the atom index.

    Strategy: for each S, count neighboring O atoms within 2.0 Å. The
    sulfonate S has 3 O neighbors.
    """
    sym = np.array(atoms.get_chemical_symbols())
    pos = atoms.positions
    s_idx = np.where(sym == "S")[0]
    best, best_no = -1, -1
    for i in s_idx:
        dists = np.linalg.norm(pos - pos[i], axis=1)
        n_o = int(((sym == "O") & (dists < 2.0) & (dists > 0)).sum())
        if n_o > best_no:
            best_no = n_o
            best = i
    if best_no < 3:
        print(f"  ⚠ anchor S has only {best_no} O neighbors (expected 3 for sulfonate)")
    return int(best)


def orient_molecule_so3_down(atoms, anchor_idx):
    """Rotate molecule so the sulfonate S→molecule_COM vector points in
    +z (i.e. sulfonate pointing DOWN toward the slab surface)."""
    pos = atoms.positions.copy()
    com = pos.mean(axis=0)
    v = com - pos[anchor_idx]
    v = v / np.linalg.norm(v)
    # Rotate so v aligns with +z
    target = np.array([0.0, 0.0, 1.0])
    axis = np.cross(v, target)
    if np.linalg.norm(axis) < 1e-6:
        return atoms  # already aligned
    axis = axis / np.linalg.norm(axis)
    cos_t = float(np.dot(v, target))
    sin_t = float(np.linalg.norm(np.cross(v, target)))
    K = np.array([[0, -axis[2], axis[1]],
                  [axis[2], 0, -axis[0]],
                  [-axis[1], axis[0], 0]])
    R = np.eye(3) + sin_t * K + (1 - cos_t) * (K @ K)
    pos_centered = pos - pos[anchor_idx]
    pos_new = pos_centered @ R.T + pos[anchor_idx]
    atoms.positions = pos_new
    return atoms


def place_molecule_at(slab, mol_template, anchor_idx, dx_frac, dy_frac, dz_A):
    """Translate molecule so its sulfonate S is at fractional (dx,dy) in
    the slab ab plane and dz Å above slab top. Returns combined Atoms."""
    from ase import Atoms
    slab_pos = slab.positions
    z_top = slab_pos[:, 2].max()
    cell = slab.cell.array

    # Anchor target in Cartesian (fractional → Cartesian for ab, +dz for z)
    target = dx_frac * cell[0] + dy_frac * cell[1]
    target[2] = z_top + dz_A

    mol_pos = mol_template.positions.copy()
    shift = target - mol_pos[anchor_idx]
    mol_pos += shift

    combined = Atoms(
        symbols=list(slab.symbols) + list(mol_template.symbols),
        positions=np.vstack([slab_pos, mol_pos]),
        cell=cell, pbc=True,
    )
    return combined


def load_uma(device, task="omat"):
    from fairchem.core.units.mlip_unit.api.inference import InferenceSettings
    from fairchem.core import pretrained_mlip, FAIRChemCalculator
    # merge_mole=False — without this, the first SP's element composition
    # is cached and the next call with a different composition fails:
    #   AssertionError: Compositions differ from merged model
    # Our scan deliberately calls 3 different compositions (slab, mol, complex)
    # so we must allow composition changes between predictions.
    predictor = pretrained_mlip.get_predict_unit(
        "uma-s-1p1", device=device,
        inference_settings=InferenceSettings(
            tf32=True, activation_checkpointing=False, merge_mole=False,
            compile=False, wigner_cuda=False,
        ),
    )
    return FAIRChemCalculator(predictor, task_name=task)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slab", required=True, help="LiNiO2 slab xyz (init, unrelaxed)")
    ap.add_argument("--molecule", required=True, help="SDCP xyz (ORCA-optimized)")
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--form", choices=("doped", "neutral"), required=True,
                    help="metadata only — affects output file name")
    ap.add_argument("--nx", type=int, default=10, help="grid points in a-direction")
    ap.add_argument("--ny", type=int, default=10, help="grid points in b-direction")
    ap.add_argument("--dz", type=float, nargs=3, default=[2.0, 6.0, 0.5],
                    help="dz range: zmin zmax step (Å)")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--task", default="omat")
    args = ap.parse_args()

    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    from ase.io import read

    # Load slab + molecule
    slab = read(args.slab)
    mol = read(args.molecule)
    print(f"Slab: {len(slab)} atoms, cell:")
    print(slab.cell.array)
    print(f"Molecule ({args.form}): {len(mol)} atoms")

    # Find sulfonate S
    anchor = find_anchor_S(mol)
    print(f"Anchor (sulfonate S): atom idx {anchor} ({mol.symbols[anchor]})")
    print(f"  position: {mol.positions[anchor]}")

    # Orient molecule so sulfonate points down
    mol = orient_molecule_so3_down(mol, anchor)
    print(f"  after orient: anchor at {mol.positions[anchor]}, "
          f"COM at {mol.positions.mean(axis=0)}")

    # Setup grid
    dz_vals = np.arange(args.dz[0], args.dz[1] + 1e-6, args.dz[2])
    dx_vals = np.linspace(0.0, 1.0, args.nx, endpoint=False)
    dy_vals = np.linspace(0.0, 1.0, args.ny, endpoint=False)
    n_grid = args.nx * args.ny * len(dz_vals)
    print(f"\nGrid: {args.nx} × {args.ny} × {len(dz_vals)} = {n_grid} points")

    # Load UMA
    print(f"\nLoading UMA-s-1p1 (device={args.device}, task={args.task})...")
    calc = load_uma(args.device, args.task)

    # ===== Reference energies =====
    print("\n=== Reference SP ===")
    slab_iso = slab.copy(); slab_iso.calc = calc
    t0 = time.time()
    E_slab_iso = float(slab_iso.get_potential_energy())
    print(f"E_slab_iso = {E_slab_iso:.6f} eV  ({time.time()-t0:.1f}s)")

    # Molecule alone in same cell
    from ase import Atoms
    mol_iso = Atoms(symbols=list(mol.symbols), positions=mol.positions.copy(),
                    cell=slab.cell.array, pbc=True)
    # Center molecule in cell (avoid touching slab origin region)
    mol_iso.positions -= mol_iso.positions.mean(axis=0)
    mol_iso.positions += np.array([0.5*slab.cell[0,0]+0.5*slab.cell[1,0],
                                    0.5*slab.cell[1,1],
                                    0.5*slab.cell[2,2]])
    mol_iso.calc = calc
    t0 = time.time()
    E_SDCP_iso = float(mol_iso.get_potential_energy())
    print(f"E_SDCP_iso = {E_SDCP_iso:.6f} eV  ({time.time()-t0:.1f}s)")

    # ===== Grid scan =====
    print(f"\n=== Phase A rigid grid ({n_grid} points) ===")
    E_complex = np.zeros((args.nx, args.ny, len(dz_vals)))
    E_bind = np.zeros_like(E_complex)
    t0 = time.time()
    last_save = t0

    for i, dx in enumerate(dx_vals):
        for j, dy in enumerate(dy_vals):
            for k, dz in enumerate(dz_vals):
                combined = place_molecule_at(slab, mol, anchor, dx, dy, dz)
                combined.calc = calc
                E = float(combined.get_potential_energy())
                E_complex[i, j, k] = E
                E_bind[i, j, k] = E - E_slab_iso - E_SDCP_iso
                # Progress every 30 s
                if time.time() - last_save > 30:
                    done = i*args.ny*len(dz_vals) + j*len(dz_vals) + k + 1
                    rate = done / (time.time() - t0)
                    eta = (n_grid - done) / rate if rate > 0 else 0
                    print(f"  [{done}/{n_grid}] {rate:.1f} pts/s  "
                          f"E_bind range = [{E_bind[:i+1, :, :].min():.3f}, "
                          f"{E_bind[:i+1, :, :].max():.3f}] eV  ETA {eta/60:.1f} min")
                    last_save = time.time()

    total_dt = time.time() - t0
    print(f"\nScan done: {total_dt:.0f}s ({total_dt/n_grid:.2f}s/point)")

    # Find best site
    flat_min = np.argmin(E_bind)
    i_min, j_min, k_min = np.unravel_index(flat_min, E_bind.shape)
    print(f"\n=== Best E_bind site ===")
    print(f"  dx_frac = {dx_vals[i_min]:.3f}, dy_frac = {dy_vals[j_min]:.3f}, "
          f"dz = {dz_vals[k_min]:.2f} Å")
    print(f"  E_bind = {E_bind[i_min, j_min, k_min]:.4f} eV")
    print(f"  E_complex = {E_complex[i_min, j_min, k_min]:.4f} eV")

    # Save best site complex xyz
    best_combined = place_molecule_at(slab, mol, anchor,
                                       dx_vals[i_min], dy_vals[j_min], dz_vals[k_min])
    from ase.io import write
    write(out_dir / f"best_site_{args.form}.xyz", best_combined, format="extxyz")

    # Save JSON
    result = {
        "form": args.form,
        "n_grid": int(n_grid),
        "nx_ny_nz": [int(args.nx), int(args.ny), int(len(dz_vals))],
        "dx_vals": dx_vals.tolist(),
        "dy_vals": dy_vals.tolist(),
        "dz_vals": dz_vals.tolist(),
        "E_slab_iso": E_slab_iso,
        "E_SDCP_iso": E_SDCP_iso,
        "E_complex": E_complex.tolist(),
        "E_bind": E_bind.tolist(),
        "best": {
            "i": int(i_min), "j": int(j_min), "k": int(k_min),
            "dx_frac": float(dx_vals[i_min]),
            "dy_frac": float(dy_vals[j_min]),
            "dz_A": float(dz_vals[k_min]),
            "E_bind_eV": float(E_bind[i_min, j_min, k_min]),
            "E_complex_eV": float(E_complex[i_min, j_min, k_min]),
        },
        "elapsed_s": float(total_dt),
        "uma_model": "uma-s-1p1", "task": args.task,
        "slab_xyz": str(args.slab),
        "molecule_xyz": str(args.molecule),
        "anchor_S_idx": int(anchor),
    }
    out_json = out_dir / f"scan_rigid_{args.form}.json"
    json.dump(result, open(out_json, "w"), indent=2)
    print(f"\nWrote {out_json}")
    print(f"Wrote {out_dir/f'best_site_{args.form}.xyz'}")


if __name__ == "__main__":
    main()

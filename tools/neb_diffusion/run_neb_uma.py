#!/usr/bin/env python3
"""ASE NEB on a Li-adatom diffusion path using UMA-oc20 (fast screening).

Takes a slab xyz + initial/final adatom positions, generates 7-image NEB with
IDPP interpolation, optimizes with Climbing-Image NEB until fmax<0.05 eV/Å.

Output:
  <out>/neb_init.xyz, neb_final.xyz  (endpoints)
  <out>/neb_path_initial.xyz         (7-image path before opt)
  <out>/neb_path_final.xyz           (7-image path after opt, with energies)
  <out>/neb_energies.json            (per-image E, barrier)
  <out>/neb.log                       (ASE optimizer log)

Usage:
    python3 run_neb_uma.py \\
        --slab li3n_001_init.xyz \\
        --adatom_initial 0,0,12 \\
        --adatom_final 1.83,3.16,12 \\
        --out_dir out_li3n_001 \\
        --n_images 7 --fmax 0.05 --device cuda --task oc20
"""
import argparse, json, time
from pathlib import Path
import numpy as np


def freeze_bottom(atoms, fraction=0.5):
    from ase.constraints import FixAtoms
    z = atoms.positions[:, 2]
    z_cut = np.sort(z)[int(fraction * len(atoms)) - 1]
    mask = z <= z_cut
    atoms.set_constraint(FixAtoms(mask=mask))
    return atoms, int(mask.sum())


def load_uma(device, task):
    from fairchem.core.units.mlip_unit.api.inference import InferenceSettings
    from fairchem.core import pretrained_mlip, FAIRChemCalculator
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
    ap.add_argument("--slab", required=True, help="bare slab xyz (no adatom)")
    ap.add_argument("--adatom_initial", required=True,
                    help="initial Li adatom position 'x,y,z' (Å)")
    ap.add_argument("--adatom_final", required=True,
                    help="final Li adatom position 'x,y,z' (Å)")
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--n_images", type=int, default=7)
    ap.add_argument("--waypoint", default=None,
                    help="optional intermediate adatom position 'x,y,z' (Å). "
                         "Builds 2-segment NEB: init→waypoint→final. Useful for "
                         "bridge→bridge hops where the TS is forced through an "
                         "on-top atom and linear IDPP cannot find it.")
    ap.add_argument("--fmax", type=float, default=0.05)
    ap.add_argument("--max_steps", type=int, default=200)
    ap.add_argument("--freeze_fraction", type=float, default=0.5)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--task", default="oc20")
    ap.add_argument("--climb_after", type=int, default=20,
                    help="enable climbing-image after this many steps (regular NEB first)")
    args = ap.parse_args()

    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    p_init = np.array([float(x) for x in args.adatom_initial.split(",")])
    p_final = np.array([float(x) for x in args.adatom_final.split(",")])
    print(f"Adatom initial: {p_init}")
    print(f"Adatom final:   {p_final}")
    print(f"Hop distance:   {np.linalg.norm(p_final - p_init):.3f} Å")

    from ase.io import read, write
    from ase.mep import NEB
    from ase.optimize import LBFGS, FIRE

    slab = read(args.slab)
    n_slab = len(slab)
    print(f"Slab: {n_slab} atoms, cell a/b={np.linalg.norm(slab.cell[0]):.2f}/{np.linalg.norm(slab.cell[1]):.2f}")

    # Build initial / final states (slab + Li adatom at given position)
    init = slab.copy()
    init.append('Li')
    init.positions[-1] = p_init
    final = slab.copy()
    final.append('Li')
    final.positions[-1] = p_final

    # Relax endpoints first (small relax, only adatom + top layers)
    print(f"\nLoading UMA-s-1p1 (task={args.task})...")
    calc = load_uma(args.device, args.task)

    for label, atoms in [("init", init), ("final", final)]:
        atoms, n_frozen = freeze_bottom(atoms, args.freeze_fraction)
        atoms.calc = calc
        E0 = float(atoms.get_potential_energy())
        opt = LBFGS(atoms, logfile=str(out_dir / f"relax_{label}.log"))
        opt.run(fmax=0.05, steps=80)
        Ef = float(atoms.get_potential_energy())
        write(out_dir / f"neb_{label}.xyz", atoms, format="extxyz")
        print(f"  {label}: E {E0:.4f} → {Ef:.4f} eV (relaxed, {opt.get_number_of_steps()} steps)")

    # Re-read relaxed endpoints (drop constraints, will reapply)
    init = read(out_dir / "neb_init.xyz")
    final = read(out_dir / "neb_final.xyz")

    # Build NEB images via linear interpolation, then IDPP-improve.
    # If --waypoint is given, build two segments: init→waypoint and waypoint→final.
    if args.waypoint is not None:
        wp = np.array([float(x) for x in args.waypoint.split(",")])
        print(f"\nUsing waypoint at {wp} — building 2-segment NEB")
        # Split N images between two segments (rounding)
        n_left = args.n_images // 2
        n_right = args.n_images - n_left - 1  # waypoint counts once
        # waypoint as an image
        wp_atoms = init.copy()
        wp_atoms.positions[-1] = wp  # adatom is last atom
        # Build left segment via IDPP
        from ase.mep import NEB as _NEB
        left = [init.copy()] + [init.copy() for _ in range(n_left - 1)] + [wp_atoms.copy()]
        _NEB(left, allow_shared_calculator=True).interpolate(method="idpp", mic=True)
        right = [wp_atoms.copy()] + [wp_atoms.copy() for _ in range(n_right - 1)] + [final.copy()]
        _NEB(right, allow_shared_calculator=True).interpolate(method="idpp", mic=True)
        # Stitch: left (without duplicate waypoint at end) + right
        images = left[:-1] + right
        print(f"  Built {len(images)} images: left {n_left+1} + right {n_right} ")
        neb = NEB(images, climb=False, allow_shared_calculator=True,
                  method="improvedtangent")
    else:
        images = [init.copy()] + \
                 [init.copy() for _ in range(args.n_images - 2)] + \
                 [final.copy()]
        neb = NEB(images, climb=False, allow_shared_calculator=True,
                  method="improvedtangent")
        neb.interpolate(method="idpp", mic=True)

    # Attach calc + freeze
    for img in images:
        freeze_bottom(img, args.freeze_fraction)
        img.calc = calc

    # Save initial NEB path (before optimization)
    write(out_dir / "neb_path_initial.xyz", images, format="extxyz")

    # === Phase 1: regular NEB ===
    print(f"\n=== NEB regular ({args.climb_after} steps) ===")
    opt = LBFGS(neb, logfile=str(out_dir / "neb.log"))
    t0 = time.time()
    opt.run(fmax=max(args.fmax, 0.1), steps=args.climb_after)
    dt1 = time.time() - t0
    print(f"  done in {dt1:.0f}s ({opt.get_number_of_steps()} steps)")

    # === Phase 2: climbing-image NEB (accurate TS) ===
    print(f"\n=== NEB climbing-image (fmax={args.fmax}) ===")
    neb.climb = True
    t0 = time.time()
    opt.run(fmax=args.fmax, steps=args.max_steps - args.climb_after)
    dt2 = time.time() - t0
    print(f"  done in {dt2:.0f}s ({opt.get_number_of_steps()} steps total)")

    # Collect energies
    energies = [float(img.get_potential_energy()) for img in images]
    E0 = energies[0]
    rel_E = [e - E0 for e in energies]
    barrier = max(rel_E)
    barrier_idx = int(np.argmax(rel_E))

    # Save
    write(out_dir / "neb_path_final.xyz", images, format="extxyz")
    json.dump({
        "n_images": args.n_images,
        "energies_eV": energies,
        "rel_energies_eV": rel_E,
        "barrier_eV": barrier,
        "barrier_image_idx": barrier_idx,
        "fmax_target": args.fmax,
        "uma_model": "uma-s-1p1",
        "uma_task": args.task,
        "slab_xyz": str(args.slab),
        "adatom_initial": p_init.tolist(),
        "adatom_final": p_final.tolist(),
    }, open(out_dir / "neb_energies.json", "w"), indent=2)

    print(f"\n{'='*55}")
    print(f"NEB summary")
    print(f"{'='*55}")
    for k, e in enumerate(rel_E):
        marker = " ← TS" if k == barrier_idx else ""
        print(f"  image {k}: {e:+.4f} eV{marker}")
    print(f"{'='*55}")
    print(f"Diffusion barrier: {barrier:.4f} eV  (at image {barrier_idx})")
    print(f"{'='*55}")


if __name__ == "__main__":
    main()

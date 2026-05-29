#!/usr/bin/env python3
"""Build a small LiNiO2 (104) slab + UMA relax → reference for SDCP binding scan.

Re-uses tools/build_ncm_interface.py::build_ncm_slab (LiNiO2 = NCM x_Ni=1.0).

Output:
    <out_dir>/slab_init.xyz       (post-build, pre-relax)
    <out_dir>/slab_relaxed.xyz    (UMA-relaxed, bottom 2 layers fixed)
    <out_dir>/E_slab_iso.json     ({E_eV, fmax, n_atoms, cell, ...})

Smaller than the cascade NCM slab — SDCP molecule is ~10-12 Å, so a ~15 Å
surface with ~3 atomic layers + 15 Å vacuum is plenty for binding scan.
"""
import argparse, json, sys
from pathlib import Path
import numpy as np

# Add repo root to path so build_ncm_interface is importable
REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from tools.build_ncm_interface import build_ncm_slab


def freeze_bottom_layers(atoms, n_freeze_layers=2):
    """Sort atoms by z, mark bottom n layers as fixed (FixAtoms)."""
    from ase.constraints import FixAtoms
    z = atoms.positions[:, 2]
    z_sorted = np.sort(np.unique(np.round(z, 2)))
    if len(z_sorted) <= n_freeze_layers:
        z_cut = z_sorted[-1]
    else:
        z_cut = z_sorted[n_freeze_layers - 1] + 0.5
    mask = z < z_cut
    atoms.set_constraint(FixAtoms(mask=mask))
    print(f"  Frozen: {mask.sum()}/{len(atoms)} atoms (z < {z_cut:.2f} Å)")
    return atoms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--facet", default="104")
    ap.add_argument("--min_slab", type=float, default=8.0,
                    help="min slab thickness Å (default 8 = ~3-4 atomic layers)")
    ap.add_argument("--repeat_xy", type=int, nargs=2, default=[3, 5],
                    help="surface repeat (default 3 5 → ~15 Å lateral)")
    ap.add_argument("--vacuum", type=float, default=15.0,
                    help="vacuum above slab Å (default 15)")
    ap.add_argument("--n_freeze", type=int, default=2,
                    help="bottom layers to freeze during relax (default 2)")
    ap.add_argument("--fmax", type=float, default=0.05,
                    help="UMA relax force threshold eV/Å")
    ap.add_argument("--max_steps", type=int, default=200)
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--no_relax", action="store_true",
                    help="skip UMA relax (just build + save initial)")
    args = ap.parse_args()

    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    facet = tuple(int(c) for c in args.facet)

    # 1) Build bulk slab via existing helper
    print(f"=== Build LiNiO2 ({args.facet}) slab ===")
    slab = build_ncm_slab(facet=facet, min_slab=args.min_slab, min_vac=1.0)

    # 2) xy repeat
    nx, ny = args.repeat_xy
    slab = slab.repeat((nx, ny, 1))
    a, b = np.linalg.norm(slab.cell[0]), np.linalg.norm(slab.cell[1])
    print(f"  After repeat ({nx},{ny}): {len(slab)} atoms, "
          f"surface a={a:.2f}, b={b:.2f} Å")

    # 3) Add proper vacuum on top (cell c → slab_zmax + vacuum)
    z = slab.positions[:, 2]
    slab.positions[:, 2] -= z.min()  # set z_min = 0
    z_max = slab.positions[:, 2].max()
    new_cell = slab.cell.array.copy()
    new_cell[2] = [0, 0, z_max + args.vacuum]
    slab.set_cell(new_cell, scale_atoms=False)
    slab.set_pbc(True)
    print(f"  Slab z=[0, {z_max:.2f}] Å, cell c={new_cell[2,2]:.2f} Å (vacuum {args.vacuum})")

    # Save initial
    from ase.io import write
    init_path = out_dir / "slab_init.xyz"
    write(init_path, slab, format="extxyz")
    print(f"  → {init_path}")

    if args.no_relax:
        return

    # 4) UMA relax with bottom layers fixed
    print(f"=== UMA relax (fmax={args.fmax}, max_steps={args.max_steps}) ===")
    freeze_bottom_layers(slab, n_freeze_layers=args.n_freeze)

    # Load UMA
    from fairchem.core.units.mlip_unit.api.inference import (
        InferenceSettings,
    )
    from fairchem.core import pretrained_mlip, FAIRChemCalculator
    predictor = pretrained_mlip.get_predict_unit(
        "uma-s-1p1", device=args.device,
        inference_settings=InferenceSettings(
            tf32=True, activation_checkpointing=False, merge_mole=True,
            compile=False, wigner_cuda=False,
        ),
    )
    calc = FAIRChemCalculator(predictor, task_name="omat")
    slab.calc = calc

    from ase.optimize import FIRE
    opt = FIRE(slab, logfile=str(out_dir / "relax.log"))
    opt.run(fmax=args.fmax, steps=args.max_steps)

    E = float(slab.get_potential_energy())
    fmax_final = float(np.max(np.linalg.norm(slab.get_forces(), axis=1)))
    print(f"  E_slab_iso = {E:.6f} eV  fmax_final = {fmax_final:.4f} eV/Å")

    # Save
    write(out_dir / "slab_relaxed.xyz", slab, format="extxyz")
    json.dump({
        "E_eV": E,
        "fmax_final": fmax_final,
        "n_atoms": len(slab),
        "facet": args.facet,
        "repeat_xy": [nx, ny],
        "vacuum": args.vacuum,
        "n_freeze_layers": args.n_freeze,
        "cell": slab.cell.array.tolist(),
        "uma_model": "uma-s-1p1",
        "fmax_threshold": args.fmax,
        "max_steps": args.max_steps,
    }, open(out_dir / "E_slab_iso.json", "w"), indent=2)
    print(f"  → {out_dir/'slab_relaxed.xyz'}")
    print(f"  → {out_dir/'E_slab_iso.json'}")


if __name__ == "__main__":
    main()

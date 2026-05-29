#!/usr/bin/env python3
"""Build a small LiNiO2 (104) slab + UMA relax → reference for SDCP binding scan.

For high-index facets like (104), pymatgen's SlabGenerator can return slabs
where the c-vector is NOT perpendicular to the ab plane (non-orthogonal
α, β). That makes lateral xy repeats balloon the atoms in z (we saw
z-range 66 Å for a "thin" slab). We call Slab.get_orthogonal_c_slab() to
force c ⊥ ab before xy-repeat + vacuum.

Output:
    <out_dir>/slab_init.xyz       (post-build, pre-relax)
    <out_dir>/slab_relaxed.xyz    (UMA-relaxed, bottom 2 layers fixed)
    <out_dir>/E_slab_iso.json     ({E_eV, fmax, n_atoms, cell, ...})

Smaller than the cascade NCM slab — SDCP molecule is ~10-12 Å, so a ~15 Å
surface with ~3 atomic layers + 15 Å vacuum is plenty for binding scan.
"""
import argparse, json
from pathlib import Path
import numpy as np


def build_linio2_slab_ortho(facet=(1, 0, 4), min_slab=8.0, min_vac=2.0):
    """LiNiO2 (R-3m) slab at requested facet, c-orthogonal to ab.

    Returns ase.Atoms with the slab compactly stacked along z (vacuum is
    set later by caller).
    """
    from pymatgen.core import Structure, Lattice
    from pymatgen.core.surface import SlabGenerator
    from pymatgen.io.ase import AseAtomsAdaptor

    # LiNiO2 bulk (R-3m, hexagonal setting)
    bulk = Structure(
        Lattice.hexagonal(2.878, 14.19),
        ["Li", "Ni", "O", "O"],
        [[0, 0, 0.5], [0, 0, 0], [0, 0, 0.2584], [0, 0, 0.7416]],
    )
    gen = SlabGenerator(
        bulk, miller_index=facet,
        min_slab_size=min_slab, min_vacuum_size=min_vac,
        center_slab=True, in_unit_planes=False,
    )
    slabs = gen.get_slabs(symmetrize=False)
    if not slabs:
        raise RuntimeError(f"No slabs found for facet {facet}")
    slab = slabs[0]
    print(f"  raw slab: {len(slab)} atoms, "
          f"a={slab.lattice.a:.2f}, b={slab.lattice.b:.2f}, "
          f"c={slab.lattice.c:.2f}, "
          f"α={slab.lattice.alpha:.1f}°, β={slab.lattice.beta:.1f}°, "
          f"γ={slab.lattice.gamma:.1f}°")

    # Force c ⊥ ab (fixes high-index facet z-tilt)
    slab = slab.get_orthogonal_c_slab()
    print(f"  after ortho-c: {len(slab)} atoms, "
          f"a={slab.lattice.a:.2f}, b={slab.lattice.b:.2f}, "
          f"c={slab.lattice.c:.2f}, "
          f"α={slab.lattice.alpha:.1f}°, β={slab.lattice.beta:.1f}°, "
          f"γ={slab.lattice.gamma:.1f}°")

    return AseAtomsAdaptor.get_atoms(slab)


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

    # 1) Build orthogonalized slab (c ⊥ ab)
    print(f"=== Build LiNiO2 ({args.facet}) slab ===")
    slab = build_linio2_slab_ortho(facet=facet, min_slab=args.min_slab, min_vac=1.0)

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

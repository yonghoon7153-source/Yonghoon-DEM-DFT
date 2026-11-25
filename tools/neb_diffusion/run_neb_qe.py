#!/usr/bin/env python3
"""ASE NEB driver with QE Espresso calculator — full DFT NEB.

Replaces UMA-NEB-geometry + DFT-SCF approximation with true DFT-driven
NEB (each NEB step relaxes all 7 image geometries with forces from QE pw.x).

Cost: ~7 SCF / step × 15-25 steps to fmax=0.05 eV/Å. On a single A6000 with
our 140-atom slabs (60/480 Ry, 2x2x1 k), expect 5-7 days per system.

Robustness:
  - Per-image working directory + outdir (no file collisions between images)
  - Trajectory checkpoint every NEB step (auto-resume on restart)
  - Slab bottom freeze via FixAtoms (same as our UMA protocol)

Usage (via the bash wrapper that sets up NVHPC env):
    bash tools/neb_diffusion/run_neb_qe.sh <work_dir> <li3n|lic6>

Direct python usage (env must be set):
    python3 run_neb_qe.py \\
        --warm_start /path/.../neb_path_final.xyz \\
        --work_dir   /path/.../dft_neb \\
        --pseudos Li=li_pbe_v1.4.uspp.F.UPF N=N.pbe-n-radius_5.UPF \\
        --pseudo_dir /data/work/pseudo \\
        --kgrid 2 2 1 \\
        --fmax 0.05 --max_steps_phase1 5 --max_steps_phase2 30 \\
        --restart
"""
import argparse
import json
import os
import sys
from pathlib import Path
import numpy as np


def parse_kv(kv_list):
    out = {}
    for kv in kv_list:
        k, v = kv.split("=", 1)
        out[k] = v
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--warm_start", required=True,
                    help="UMA-NEB final xyz (7 frames) used as initial guess")
    ap.add_argument("--work_dir", required=True)
    ap.add_argument("--pseudos", nargs="+", required=True,
                    help="ELEMENT=PSEUDO.UPF pairs")
    ap.add_argument("--pseudo_dir", default="/data/work/pseudo")
    ap.add_argument("--qe_bin", default="/data/apps/qe-7.4.1-gpu/bin/pw.x")
    ap.add_argument("--mpirun",
                    default="/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin/mpirun")
    ap.add_argument("--mpi_np", type=int, default=1)
    ap.add_argument("--kgrid", type=int, nargs=3, default=[2, 2, 1])
    ap.add_argument("--ecutwfc", type=float, default=60.0)
    ap.add_argument("--ecutrho", type=float, default=480.0)
    ap.add_argument("--conv_thr", type=float, default=1e-8)
    ap.add_argument("--fmax", type=float, default=0.05)
    ap.add_argument("--max_steps_phase1", type=int, default=5,
                    help="regular NEB steps before CI is turned on")
    ap.add_argument("--max_steps_phase2", type=int, default=30,
                    help="CI-NEB max steps")
    ap.add_argument("--spring_k", type=float, default=0.1)
    ap.add_argument("--bottom_freeze_frac", type=float, default=0.5,
                    help="freeze slab atoms with z < z_min + frac*(z_max-z_min)")
    ap.add_argument("--optimizer", choices=["bfgs", "fire"], default="bfgs")
    ap.add_argument("--restart", action="store_true",
                    help="resume from existing neb.traj if present")
    args = ap.parse_args()

    work_dir = Path(args.work_dir).resolve()
    work_dir.mkdir(parents=True, exist_ok=True)
    os.chdir(work_dir)
    print(f"[run_neb_qe] work_dir = {work_dir}")

    # Set up ASE Espresso environment (only used if no profile/command set)
    os.environ.setdefault(
        "ASE_ESPRESSO_COMMAND",
        f"{args.mpirun} -np {args.mpi_np} {args.qe_bin} -in PREFIX.pwi > PREFIX.pwo",
    )

    pseudos = parse_kv(args.pseudos)
    print(f"[run_neb_qe] pseudos = {pseudos}")

    # ---- ASE imports (after env set) ----
    from ase.io import read, write
    from ase.io.trajectory import Trajectory
    from ase.mep import NEB
    from ase.optimize import BFGS, FIRE
    from ase.constraints import FixAtoms
    from ase.calculators.espresso import Espresso, EspressoProfile

    # Espresso profile (ASE 3.23+ explicit config — required, ASE_ESPRESSO_COMMAND
    # env var alone is no longer enough; ASE raises BadConfiguration without this)
    profile = EspressoProfile(
        command=f"{args.mpirun} -np {args.mpi_np} {args.qe_bin}",
        pseudo_dir=args.pseudo_dir,
    )
    print(f"[run_neb_qe] EspressoProfile:")
    print(f"  command    = {args.mpirun} -np {args.mpi_np} {args.qe_bin}")
    print(f"  pseudo_dir = {args.pseudo_dir}")

    # Load warm start
    print(f"[run_neb_qe] warm start: {args.warm_start}")
    images = read(args.warm_start, index=":")
    n_img = len(images)
    n_atoms = len(images[0])
    print(f"[run_neb_qe] {n_img} images × {n_atoms} atoms")

    # Slab bottom freeze
    ref_z = images[0].positions[:, 2]
    # exclude adatom (last) when measuring slab span
    z_min = ref_z[:-1].min()
    z_max = ref_z[:-1].max()
    z_thresh = z_min + args.bottom_freeze_frac * (z_max - z_min)
    bottom_idx = [i for i in range(n_atoms - 1) if ref_z[i] < z_thresh]
    print(f"[run_neb_qe] bottom freeze: {len(bottom_idx)} atoms "
          f"(z < {z_thresh:.2f} Å of slab range [{z_min:.2f}, {z_max:.2f}])")

    # Per-image input template
    common_system = {
        "ecutwfc": args.ecutwfc,
        "ecutrho": args.ecutrho,
        "occupations": "smearing",
        "smearing": "mv",
        "degauss": 0.01,
        "nosym": True,
    }
    common_electrons = {
        "conv_thr": args.conv_thr,
        "mixing_beta": 0.3,
        "electron_maxstep": 300,
    }

    for i, img in enumerate(images):
        img.set_constraint(FixAtoms(indices=bottom_idx))
        img_dir = work_dir / f"img{i}"
        img_dir.mkdir(exist_ok=True)
        input_data = {
            "control": {
                "calculation": "scf",
                "prefix": f"img{i}",
                "pseudo_dir": args.pseudo_dir,
                "outdir": "./tmp/",
                "tprnfor": True,
                "tstress": False,
                "verbosity": "low",
                "disk_io": "low",
            },
            "system": common_system,
            "electrons": common_electrons,
        }
        img.calc = Espresso(
            profile=profile,
            pseudopotentials=pseudos,
            kpts=tuple(args.kgrid),
            input_data=input_data,
            directory=str(img_dir),
        )

    # Restart from existing trajectory if requested
    traj_path = work_dir / "neb.traj"
    if args.restart and traj_path.exists():
        try:
            traj = Trajectory(str(traj_path), "r")
            n_frames = len(traj)
            if n_frames >= n_img:
                last_step = n_frames // n_img
                last_imgs = [traj[-n_img + j] for j in range(n_img)]
                for img, src in zip(images, last_imgs):
                    img.positions = src.positions
                print(f"[run_neb_qe] resumed from neb.traj "
                      f"(~{last_step} steps recorded)")
            else:
                print(f"[run_neb_qe] neb.traj too short ({n_frames} frames) — fresh start")
        except Exception as e:
            print(f"[run_neb_qe] restart failed: {e} — fresh start")

    # NEB setup
    neb = NEB(images, k=args.spring_k, climb=False,
              allow_shared_calculator=False)

    Opt = BFGS if args.optimizer == "bfgs" else FIRE

    # Phase 1: regular NEB (warmup, k-springs only)
    if args.max_steps_phase1 > 0:
        print(f"\n[run_neb_qe] === Phase 1: regular NEB "
              f"(max {args.max_steps_phase1} steps, fmax={args.fmax}) ===")
        opt = Opt(neb, trajectory=str(traj_path), logfile="neb.log")
        opt.run(fmax=args.fmax, steps=args.max_steps_phase1)

    # Phase 2: CI-NEB (accurate TS)
    print(f"\n[run_neb_qe] === Phase 2: CI-NEB "
          f"(max {args.max_steps_phase2} steps, fmax={args.fmax}) ===")
    neb.climb = True
    opt = Opt(neb, trajectory=str(traj_path), logfile="neb.log")
    opt.run(fmax=args.fmax, steps=args.max_steps_phase2)

    # ---- save & analyze ----
    final_xyz = work_dir / "neb_path_final_dft.xyz"
    write(str(final_xyz), images, format="extxyz")
    print(f"\n[run_neb_qe] → {final_xyz}")

    energies = [img.get_potential_energy() for img in images]
    E0 = energies[0]
    rel = [e - E0 for e in energies]
    barrier = max(rel)
    ts_idx = rel.index(barrier)
    bridge_E = min(rel) if min(rel) < -1e-3 else 0.0
    eff_barrier = barrier - bridge_E

    print(f"\n[run_neb_qe] === NEB summary ===")
    print(f"{'image':<8} {'E (eV)':>14}  {'E_rel (eV)':>12}")
    print("=" * 42)
    for i, (e, r) in enumerate(zip(energies, rel)):
        mark = "  ← TS" if i == ts_idx else ""
        print(f"  {i:<6} {e:>14.4f}  {r:>+12.4f}{mark}")
    print(f"\nbarrier (endpoint→TS):       {barrier:.4f} eV")
    print(f"bridge minimum (if present): {bridge_E:.4f} eV")
    print(f"effective barrier:           {eff_barrier:.4f} eV")

    summary = {
        "method": "Full DFT NEB (ASE + QE Espresso, PBE+USPP, CI-NEB)",
        "energies_eV": energies,
        "rel_energies_eV": rel,
        "barrier_eV": barrier,
        "barrier_image_idx": ts_idx,
        "bridge_min_eV": bridge_E,
        "effective_barrier_eV": eff_barrier,
        "n_images": n_img,
        "fmax_target": args.fmax,
        "kgrid": args.kgrid,
        "ecutwfc": args.ecutwfc,
        "ecutrho": args.ecutrho,
        "spring_k": args.spring_k,
        "optimizer": args.optimizer,
    }
    with open(work_dir / "neb_dft_results.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[run_neb_qe] → {work_dir / 'neb_dft_results.json'}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""MLIP 600K snapshot elastic constants for modelC_v3 (Pipeline v2 §8e).

Workflow:
  1. Load modelC_v3 V0 structure (DFT-relaxed).
  2. Langevin MD at 600 K: equilibrate 10 ps, production 20 ps.
  3. Sample 5 snapshots evenly from production.
  4. For each snapshot: quench (FIRE, fmax 0.01 eV/Å) → 6 Voigt strain ±h
     SCF (MLIP single-point stress) → full 6×6 Cij via stress-strain.
  5. Average Cij across snapshots + per-snapshot VRH std.
  6. Save full results JSON.

The point of redoing for modelC_v3 (vs the existing modelc MLIP 600K row in
db/properties/elastic.json) is that modelC_v3 starts from the DFT-relaxed
v2-annealed V0, not the ordered-Li v1 structure. So this is the finite-T
elastic of the actual paper-quality structure.

Cost estimate (UMA-s-1p1, container A6000, 62-atom cell): ~3-6 h total.
"""
import argparse
import json
import time
from pathlib import Path
import numpy as np
from ase import units
from ase.io import read, write
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.optimize import FIRE


EV_PER_A3_TO_GPA = 160.21766208


def stress_to_voigt(sigma_3x3):
    return np.array([
        sigma_3x3[0, 0], sigma_3x3[1, 1], sigma_3x3[2, 2],
        sigma_3x3[1, 2], sigma_3x3[0, 2], sigma_3x3[0, 1],
    ])


def apply_voigt_strain(atoms_in, k, h):
    """Apply pure Voigt strain k (0..5) with magnitude h to atoms (atoms scale).

    Convention: tensor ε_ij = h applied to the indicated component.
    Engineering γ_k = 2 ε_ij is implied by Voigt-style σ↔ε pairing for shear.
    """
    eps = np.zeros((3, 3))
    if k <= 2:
        eps[k, k] = h
    elif k == 3:
        eps[1, 2] = eps[2, 1] = h
    elif k == 4:
        eps[0, 2] = eps[2, 0] = h
    elif k == 5:
        eps[0, 1] = eps[1, 0] = h
    new_cell = atoms_in.cell @ (np.eye(3) + eps)
    a = atoms_in.copy()
    a.set_cell(new_cell, scale_atoms=True)
    return a


def stress_strain_cij(atoms_quenched, calc_factory, strain_h, sign_flip,
                       relaxed_ion=True, ion_fmax=0.05, ion_max_steps=200,
                       log_dir=None, snap_idx=None):
    """Return 6×6 Cij (GPa) for one quenched snapshot via stress-strain.

    relaxed_ion=True (default, the "paper" method):
      For each strain, FIRE-relax internal atomic positions at the strained
      cell (cell fixed) before measuring stress. Yields physical finite-T
      Cij including internal/optical phonon contributions to softening.

    relaxed_ion=False (clamped-ion):
      Single-point stress at the strained configuration (atoms scale with
      cell). Gives the stiff "0K-like" Cij that ignores internal relaxation.

    For our system the relaxed-ion variant typically gives 30-50% lower
    moduli at 600 K than clamped-ion, matching the existing modelc MLIP
    600K row (E ≈ 33 GPa) in db/properties/elastic.json.
    """
    from ase.optimize import FIRE
    from ase.constraints import FixSymmetry  # not used, just to be safe
    Cij = np.zeros((6, 6))
    for k in range(6):
        sigmas = []
        for sign in (+1, -1):
            a_strain = apply_voigt_strain(atoms_quenched, k, sign * strain_h)
            a_strain.calc = calc_factory()
            if relaxed_ion:
                # Relax internal positions, KEEP cell fixed (no UnitCellFilter)
                logf = None
                if log_dir is not None and snap_idx is not None:
                    logf = str(Path(log_dir) /
                               f"strain_relax_snap{snap_idx}_k{k}_s{int(sign)}.log")
                opt = FIRE(a_strain, logfile=logf)
                opt.run(fmax=ion_fmax, steps=ion_max_steps)
            s_3x3 = a_strain.get_stress(voigt=False)
            sigmas.append(stress_to_voigt(s_3x3))
        is_shear = (k >= 3)
        strain_voigt = 2.0 * strain_h if is_shear else strain_h
        col = (sigmas[0] - sigmas[1]) / (2.0 * strain_voigt)
        if sign_flip:
            col = -col
        Cij[:, k] = col * EV_PER_A3_TO_GPA
    return 0.5 * (Cij + Cij.T)


def vrh_full(C):
    """Voigt-Reuss-Hill from full 6×6 Cij (GPa)."""
    S = np.linalg.inv(C)
    B_V = (C[0,0]+C[1,1]+C[2,2] + 2*(C[0,1]+C[0,2]+C[1,2])) / 9.0
    G_V = ((C[0,0]+C[1,1]+C[2,2]) - (C[0,1]+C[0,2]+C[1,2])
           + 3*(C[3,3]+C[4,4]+C[5,5])) / 15.0
    B_R = 1.0 / (S[0,0]+S[1,1]+S[2,2] + 2*(S[0,1]+S[0,2]+S[1,2]))
    G_R = 15.0 / (4*(S[0,0]+S[1,1]+S[2,2]) - 4*(S[0,1]+S[0,2]+S[1,2])
                  + 3*(S[3,3]+S[4,4]+S[5,5]))
    B = (B_V + B_R) / 2.0
    G = (G_V + G_R) / 2.0
    E = 9*B*G / (3*B + G)
    nu = (3*B - 2*G) / (2*(3*B + G))
    A = 2*C[3,3] / (C[0,0] - C[0,1]) if (C[0,0] - C[0,1]) > 0 else float("nan")
    return dict(B_V=B_V, B_R=B_R, B_VRH=B, G_V=G_V, G_R=G_R, G_VRH=G,
                E=E, nu=nu, A_zener=A)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--v0_xyz", required=True, help="modelC_v3 V0 structure")
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--T_K", type=float, default=600.0)
    ap.add_argument("--equilib_ps", type=float, default=10.0)
    ap.add_argument("--prod_ps", type=float, default=20.0)
    ap.add_argument("--n_snapshots", type=int, default=5)
    ap.add_argument("--timestep_fs", type=float, default=2.0)
    ap.add_argument("--friction", type=float, default=0.02,
                    help="Langevin friction (1/fs)")
    ap.add_argument("--strain", type=float, default=0.005)
    ap.add_argument("--quench_fmax", type=float, default=0.01)
    ap.add_argument("--quench_max_steps", type=int, default=1000)
    ap.add_argument("--uma_model", default="uma-s-1p1")
    ap.add_argument("--uma_task", default="omat",
                    help="omat (bulk material) for SE; oc20 reserved for surfaces")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--qe_sign_flip", action="store_true",
                    help="apply QE-style stress sign flip. Default OFF since "
                         "FAIRChem ASE Calculator returns physical convention "
                         "(σ > 0 for tensile). Only enable if your calculator "
                         "follows QE convention σ = -(1/V) ∂E/∂ε.")
    ap.add_argument("--clamped_ion", action="store_true",
                    help="single-point stress at strained config (no internal "
                         "relaxation). Default is relaxed-ion (per-strain FIRE) "
                         "which is the paper method for finite-T MLIP elastic.")
    ap.add_argument("--ion_fmax", type=float, default=0.05,
                    help="fmax for per-strain internal FIRE relax")
    ap.add_argument("--ion_max_steps", type=int, default=200)
    args = ap.parse_args()
    sign_flip = args.qe_sign_flip
    relaxed_ion = not args.clamped_ion

    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    t_start = time.time()
    print(f"=== MLIP 600K snapshot elastic — modelC_v3 ===")
    print(f"v0 = {args.v0_xyz}")
    print(f"out_dir = {out_dir}")
    print(f"T = {args.T_K} K, equilib = {args.equilib_ps} ps, prod = {args.prod_ps} ps")
    print(f"snapshots = {args.n_snapshots}, strain step = {args.strain}")
    print(f"UMA model = {args.uma_model}, task = {args.uma_task}, device = {args.device}")

    # Calculator factory
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    predictor = pretrained_mlip.get_predict_unit(args.uma_model, device=args.device)
    def calc_factory():
        return FAIRChemCalculator(predictor, task_name=args.uma_task)

    # Load V0
    atoms = read(args.v0_xyz)
    atoms.calc = calc_factory()
    print(f"\nLoaded {len(atoms)} atoms")
    sym_counts = {s: int((np.array(atoms.get_chemical_symbols()) == s).sum())
                  for s in sorted(set(atoms.get_chemical_symbols()))}
    print(f"  composition: {sym_counts}")

    # Initialize velocities at T_K
    MaxwellBoltzmannDistribution(atoms, temperature_K=args.T_K)

    # Langevin MD: equilibration
    dt = args.timestep_fs * units.fs
    md = Langevin(atoms, dt, temperature_K=args.T_K,
                  friction=args.friction, logfile=str(out_dir / "md.log"))
    eq_steps = int(args.equilib_ps * 1000 / args.timestep_fs)
    print(f"\nEquilibration: {eq_steps} steps")
    t0 = time.time()
    md.run(eq_steps)
    print(f"  done in {(time.time()-t0)/60:.1f} min")

    # Production with snapshots
    prod_steps = int(args.prod_ps * 1000 / args.timestep_fs)
    sample_interval = prod_steps // args.n_snapshots
    snapshots = []
    print(f"\nProduction: {prod_steps} steps, sample every {sample_interval} steps")
    for i in range(args.n_snapshots):
        md.run(sample_interval)
        snap = atoms.copy()
        snapshots.append(snap)
        write(out_dir / f"snapshot_{i}.xyz", snap)
        print(f"  snapshot {i+1}/{args.n_snapshots}: "
              f"t = {(i+1)*sample_interval*args.timestep_fs/1000:.1f} ps")
    print(f"  MD total: {(time.time()-t0)/60:.1f} min")

    # Quench + Cij per snapshot
    Cij_list = []
    vrh_list = []
    sign_flip = not args.no_sign_flip
    print(f"\nStress sign flip: {sign_flip}")
    for i, snap in enumerate(snapshots):
        print(f"\n=== Snapshot {i+1}/{args.n_snapshots} ===")
        t1 = time.time()
        snap.calc = calc_factory()
        opt = FIRE(snap, logfile=str(out_dir / f"quench_{i}.log"))
        opt.run(fmax=args.quench_fmax, steps=args.quench_max_steps)
        write(out_dir / f"snapshot_{i}_quenched.xyz", snap)
        print(f"  quench done in {(time.time()-t1)/60:.1f} min")

        Cij = stress_strain_cij(snap, calc_factory, args.strain, sign_flip)
        Cij_list.append(Cij)
        v = vrh_full(Cij)
        vrh_list.append(v)
        print(f"  C11={Cij[0,0]:.2f}  C12={Cij[0,1]:.2f}  C44={Cij[3,3]:.2f}  GPa")
        print(f"  B_VRH={v['B_VRH']:.2f}  G_VRH={v['G_VRH']:.2f}  E={v['E']:.2f}  ν={v['nu']:.3f}")

    # Average
    Cij_arr = np.array(Cij_list)
    Cij_mean = Cij_arr.mean(axis=0)
    Cij_std = Cij_arr.std(axis=0)
    v_mean = vrh_full(Cij_mean)
    B_std = float(np.std([v['B_VRH'] for v in vrh_list]))
    G_std = float(np.std([v['G_VRH'] for v in vrh_list]))
    E_std = float(np.std([v['E'] for v in vrh_list]))
    nu_std = float(np.std([v['nu'] for v in vrh_list]))

    print(f"\n=== Averaged across {args.n_snapshots} snapshots ===")
    print(f"  C11 = {Cij_mean[0,0]:.2f} ± {Cij_std[0,0]:.2f} GPa")
    print(f"  C12 = {Cij_mean[0,1]:.2f} ± {Cij_std[0,1]:.2f} GPa")
    print(f"  C44 = {Cij_mean[3,3]:.2f} ± {Cij_std[3,3]:.2f} GPa")
    print(f"  B_VRH = {v_mean['B_VRH']:.2f} ± {B_std:.2f} GPa")
    print(f"  G_VRH = {v_mean['G_VRH']:.2f} ± {G_std:.2f} GPa")
    print(f"  E     = {v_mean['E']:.2f} ± {E_std:.2f} GPa")
    print(f"  ν     = {v_mean['nu']:.3f} ± {nu_std:.3f}")
    print(f"  Zener A = {v_mean['A_zener']:.3f}")

    summary = {
        "method": f"MLIP {args.uma_model} (task={args.uma_task}) "
                  f"{int(args.T_K)}K snapshot elastic",
        "T_K": args.T_K,
        "equilib_ps": args.equilib_ps,
        "prod_ps": args.prod_ps,
        "n_snapshots": args.n_snapshots,
        "strain_step": args.strain,
        "sign_flip_applied": sign_flip,
        "Cij_per_snapshot_GPa": [c.tolist() for c in Cij_list],
        "VRH_per_snapshot": vrh_list,
        "Cij_mean_GPa": Cij_mean.tolist(),
        "Cij_std_GPa": Cij_std.tolist(),
        "VRH_mean": {**v_mean,
                     "B_VRH_std": B_std, "G_VRH_std": G_std,
                     "E_std": E_std, "nu_std": nu_std},
        "v0_source": args.v0_xyz,
        "total_runtime_min": (time.time() - t_start) / 60,
    }
    with open(out_dir / "elastic_600K_snapshot_results.json", "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\n→ {out_dir / 'elastic_600K_snapshot_results.json'}")
    print(f"Total: {(time.time()-t_start)/60:.1f} min")


if __name__ == "__main__":
    main()

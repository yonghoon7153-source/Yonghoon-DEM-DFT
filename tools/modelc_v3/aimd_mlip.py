#!/usr/bin/env python3
"""AIMD (MLIP) at multiple temperatures for modelC_v3 Li ion diffusion.

Pipeline v2 §8g: Born–Oppenheimer MD with UMA-s-1p1 forces, at 600/800/1000 K
(or any T list). Outputs per-T:
  - trajectory (xyz, every N steps)
  - MSD vs time, per element (esp. Li)
  - diffusion coefficient D from linear-regime fit
  - Nernst–Einstein conductivity σ (extrapolated to room T via Arrhenius)
  - Arrhenius plot Ea + 300K σ extrapolation (after all T's done)

Usage:
    # Single T
    python3 aimd_mlip.py --v0_xyz V0_init.xyz --out_dir aimd/T600 \\
        --T_K 600 --equilib_ps 10 --prod_ps 100

    # Multi-T batch (recommended): run separately or use --temperatures
    python3 aimd_mlip.py --v0_xyz V0_init.xyz --out_root aimd \\
        --temperatures 600 800 1000 \\
        --equilib_ps 10 --prod_ps 100

Cost: ~50 ps × ~0.1 sec/step (UMA A6000) = ~40-60 min per T, ~2-3 h total
for 3 temperatures.
"""
import argparse
import json
import time
from pathlib import Path
import numpy as np

from ase import units
from ase.io import read, write, Trajectory
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution


def compute_msd_per_element(traj_path: Path, dt_save_fs: float):
    """Read trajectory, return MSD vs t for each element."""
    frames = read(str(traj_path), index=":")
    n_frames = len(frames)
    if n_frames < 2:
        return {}
    n_atoms = len(frames[0])
    syms = np.array(frames[0].get_chemical_symbols())
    positions = np.array([f.get_positions() for f in frames])  # (T, N, 3)

    # Unwrap PBC: detect jumps > L/2 and undo
    # Simple unwrap assuming small displacements per frame
    cell = frames[0].cell.array
    L_diag = np.diag(cell)  # works only for orthorhombic; for hex approx
    pos_unwrap = positions.copy()
    for t in range(1, n_frames):
        dr = pos_unwrap[t] - pos_unwrap[t - 1]
        # only for orthogonal cell — for hex it's an approximation
        for i in range(3):
            if L_diag[i] > 0:
                jump = np.round(dr[:, i] / L_diag[i])
                pos_unwrap[t:, :, i] -= jump * L_diag[i]

    # MSD per element
    msd = {}
    times_ps = np.arange(n_frames) * dt_save_fs / 1000.0
    for elem in sorted(set(syms)):
        mask = syms == elem
        # MSD averaged over atoms of this element
        ref = pos_unwrap[0, mask]
        disp_sq = ((pos_unwrap[:, mask] - ref) ** 2).sum(axis=-1)  # (T, n_elem)
        msd[elem] = disp_sq.mean(axis=-1)  # (T,)
    return {"times_ps": times_ps.tolist(),
            "msd_per_elem_A2": {k: v.tolist() for k, v in msd.items()},
            "n_atoms_per_elem": {e: int((syms == e).sum())
                                  for e in sorted(set(syms))}}


def fit_diffusion(times_ps, msd_A2, fit_window=(2.0, 20.0)):
    """Linear fit MSD = 6 D t in the fit_window (ps). Returns D in cm²/s.

    1 Å² / 1 ps = 1e-16 m² / 1e-12 s = 1e-4 m²/s = 1 cm²/s × 1e-0 = 1e-0
    Actually: 1 Å² / 1 ps = 1e-16 cm² / 1e-12 s = 1e-4 cm²/s.
    """
    t = np.asarray(times_ps)
    m = np.asarray(msd_A2)
    mask = (t >= fit_window[0]) & (t <= fit_window[1])
    if mask.sum() < 3:
        return None
    p = np.polyfit(t[mask], m[mask], 1)  # slope, intercept
    slope_A2_per_ps = p[0]
    D_cm2_per_s = slope_A2_per_ps / 6.0 * 1e-4  # Å²/ps → cm²/s with 1/6 for 3D
    return {"slope_A2_per_ps": float(slope_A2_per_ps),
            "intercept_A2": float(p[1]),
            "D_cm2_per_s": float(D_cm2_per_s),
            "fit_window_ps": list(fit_window)}


def conductivity_NE(D_cm2_per_s, n_Li_per_cm3, T_K, z=1):
    """Nernst-Einstein: σ = n z² e² D / (kT). Returns σ in S/cm."""
    e = 1.602176634e-19      # C
    kB = 1.380649e-23        # J/K
    return n_Li_per_cm3 * (z * e) ** 2 * D_cm2_per_s / (kB * T_K)


def run_one_temperature(args, T_K, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    t_start = time.time()
    print(f"\n========== T = {T_K} K → {out_dir} ==========")

    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    predictor = pretrained_mlip.get_predict_unit(args.uma_model, device=args.device)
    def calc():
        return FAIRChemCalculator(predictor, task_name=args.uma_task)

    atoms = read(args.v0_xyz)
    atoms.calc = calc()
    n_li = int((np.array(atoms.get_chemical_symbols()) == "Li").sum())
    V_A3 = atoms.get_volume()
    n_Li_per_cm3 = n_li / (V_A3 * 1e-24)  # atoms / cm³
    print(f"  atoms={len(atoms)}  n_Li={n_li}  V={V_A3:.2f} Å³  n_Li/cm³={n_Li_per_cm3:.3e}")

    MaxwellBoltzmannDistribution(atoms, temperature_K=T_K)
    dt = args.timestep_fs * units.fs
    md = Langevin(atoms, dt, temperature_K=T_K, friction=args.friction,
                  logfile=str(out_dir / "md.log"))

    # Equilibration (no save)
    eq_steps = int(args.equilib_ps * 1000 / args.timestep_fs)
    print(f"  equilib {args.equilib_ps} ps ({eq_steps} steps)")
    t0 = time.time()
    md.run(eq_steps)
    print(f"    done in {(time.time()-t0)/60:.1f} min")

    # Production with trajectory save every save_fs
    save_interval = max(1, int(args.save_fs / args.timestep_fs))
    prod_steps = int(args.prod_ps * 1000 / args.timestep_fs)
    traj_path = out_dir / "traj.xyz"
    print(f"  prod {args.prod_ps} ps ({prod_steps} steps), save every {save_interval} steps ({args.save_fs} fs)")

    # Stream-save trajectory
    from ase.io.trajectory import Trajectory as ASETraj
    traj_obj = ASETraj(str(out_dir / "traj.traj"), "w", atoms)
    md.attach(traj_obj.write, interval=save_interval)
    t1 = time.time()
    md.run(prod_steps)
    traj_obj.close()
    print(f"    done in {(time.time()-t1)/60:.1f} min")

    # Convert .traj to .xyz multi-frame (for ASE read compatibility downstream)
    frames = read(str(out_dir / "traj.traj"), index=":")
    write(str(traj_path), frames)
    print(f"    saved {len(frames)} frames to {traj_path}")

    # MSD + diffusion fit
    print(f"  computing MSD + D ...")
    msd = compute_msd_per_element(traj_path, dt_save_fs=args.save_fs)
    fits = {}
    for elem, m in msd["msd_per_elem_A2"].items():
        fit = fit_diffusion(msd["times_ps"], m, fit_window=tuple(args.fit_window_ps))
        if fit is not None:
            fits[elem] = fit
    print(f"  D (cm²/s):")
    for elem, fit in fits.items():
        print(f"    {elem}: {fit['D_cm2_per_s']:.3e}")
    sigma = None
    if "Li" in fits and fits["Li"]["D_cm2_per_s"] > 0:
        sigma = conductivity_NE(fits["Li"]["D_cm2_per_s"], n_Li_per_cm3, T_K)
        print(f"  σ_NE (Li, T={T_K}): {sigma:.3e} S/cm")

    summary = {
        "T_K": T_K,
        "v0_source": args.v0_xyz,
        "n_atoms": len(atoms), "n_Li": n_li,
        "V_A3": V_A3, "n_Li_per_cm3": n_Li_per_cm3,
        "equilib_ps": args.equilib_ps, "prod_ps": args.prod_ps,
        "timestep_fs": args.timestep_fs, "save_fs": args.save_fs,
        "n_frames": len(frames),
        "msd_data": msd,
        "diffusion_fits": fits,
        "fit_window_ps": list(args.fit_window_ps),
        "sigma_NE_Scm_Li": sigma,
        "runtime_min": (time.time() - t_start) / 60,
    }
    (out_dir / "aimd_results.json").write_text(
        json.dumps(summary, indent=2, default=str))
    print(f"  → {out_dir / 'aimd_results.json'}")
    return summary


def arrhenius_fit(results_per_T):
    """Fit ln(D) = ln(D0) - Ea/(kB T) from list of {T_K, D_Li}."""
    kB_eV = 8.617333262e-5  # eV/K
    T = np.array([r["T_K"] for r in results_per_T])
    D = np.array([r["diffusion_fits"]["Li"]["D_cm2_per_s"]
                  for r in results_per_T])
    mask = D > 0
    if mask.sum() < 2:
        return None
    inv_T = 1.0 / T[mask]
    lnD = np.log(D[mask])
    p = np.polyfit(inv_T, lnD, 1)
    slope, intercept = p
    Ea_eV = -slope * kB_eV
    D0_cm2_per_s = float(np.exp(intercept))
    D_300K = D0_cm2_per_s * np.exp(-Ea_eV / (kB_eV * 300.0))
    return {"Ea_eV": float(Ea_eV), "D0_cm2_per_s": D0_cm2_per_s,
            "D_300K_cm2_per_s_extrapolated": float(D_300K),
            "fit_points": [{"T_K": float(t), "D_cm2_per_s": float(d)}
                           for t, d in zip(T[mask], D[mask])]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--v0_xyz", required=True)
    ap.add_argument("--out_root", default=None,
                    help="parent dir for multi-T runs (creates T600/, T800/, ...)")
    ap.add_argument("--out_dir", default=None,
                    help="single-T output dir (overrides --out_root + T)")
    ap.add_argument("--T_K", type=float, default=None, help="single T mode")
    ap.add_argument("--temperatures", type=float, nargs="+", default=None,
                    help="multi-T mode (e.g. 600 800 1000)")
    ap.add_argument("--equilib_ps", type=float, default=10.0)
    ap.add_argument("--prod_ps", type=float, default=100.0)
    ap.add_argument("--timestep_fs", type=float, default=2.0)
    ap.add_argument("--friction", type=float, default=0.02)
    ap.add_argument("--save_fs", type=float, default=100.0,
                    help="trajectory save interval (fs)")
    ap.add_argument("--fit_window_ps", type=float, nargs=2,
                    default=[2.0, 20.0],
                    help="MSD linear-fit window (ps)")
    ap.add_argument("--uma_model", default="uma-s-1p1")
    ap.add_argument("--uma_task", default="omat")
    ap.add_argument("--device", default="cuda")
    args = ap.parse_args()

    if args.temperatures is not None:
        if not args.out_root:
            raise SystemExit("--out_root required for multi-T mode")
        out_root = Path(args.out_root); out_root.mkdir(parents=True, exist_ok=True)
        results_per_T = []
        for T in args.temperatures:
            sub = out_root / f"T{int(T)}"
            results_per_T.append(run_one_temperature(args, T, sub))
        arr = arrhenius_fit(results_per_T)
        if arr is not None:
            print("\n========== Arrhenius (Li) ==========")
            print(f"  Ea = {arr['Ea_eV']:.4f} eV")
            print(f"  D0 = {arr['D0_cm2_per_s']:.3e} cm²/s")
            print(f"  D(300K) ≈ {arr['D_300K_cm2_per_s_extrapolated']:.3e} cm²/s")
            (out_root / "arrhenius_summary.json").write_text(
                json.dumps(arr, indent=2))
            print(f"  → {out_root / 'arrhenius_summary.json'}")
    else:
        if args.T_K is None:
            raise SystemExit("provide --T_K (single) or --temperatures (multi)")
        out = Path(args.out_dir) if args.out_dir else Path(f"aimd_T{int(args.T_K)}")
        run_one_temperature(args, args.T_K, out)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""disorder_ensemble_diffusion.py — Test whether Cl-/S2- site disorder lowers
the Li migration barrier Ea (the experimental Minafra/Kraft/Zeier narrative),
for comp1 (LPSCl) and modelc (LPSCl1.6).

Motivation
----------
Our earlier single-cell UMA Arrhenius gave modelc (LPSCl1.6) a HIGHER Ea than
comp1 (LPSCl) and attributed the conductivity gain to the prefactor — OPPOSITE
to the experimental "disorder flattens the landscape -> lower Ea" picture. But
both starting cells are nearly ORDERED on the Cl-/S2- (free-anion) sublattice
(comp1 fully ordered; modelc only 1/8 anti-site), so they structurally cannot
show the disorder effect. This script builds an ENSEMBLE of Cl/S anti-site
configurations at controlled disorder levels and measures Ea(disorder).

If Ea drops with disorder -> we reproduce the experiment and our earlier
ordered-cell Ea was the artifact. If Ea stays high even fully disordered ->
the prefactor mechanism is robust. Either outcome resolves the tension.

Disorder model
--------------
Free anions = S NOT bonded to any P (the free S2-) + all Cl. An "anti-site
swap" exchanges the chemical identity of one free-S site and one Cl site at
FIXED positions (lattice unchanged, only S<->Cl labels swap). Composition and
charge are conserved (atom counts unchanged). disorder_frac d = fraction of
free-anion sites that are anti-occupied = 2*n_swaps / n_free_anion_sites.

Pipeline (one UMA load for the whole ensemble)
----------------------------------------------
for each disorder level d:
    for each config replica:
        generate anti-site config
        for each T: Langevin MD (equilib + prod) -> Li MSD -> D(T)
        Arrhenius ln D vs 1/T -> Ea_config, D0_config
    Ea(d) = mean +/- std over replicas

Usage (v100, GPU free after comp1-600K):
    python3 disorder_ensemble_diffusion.py \
        --v0_xyz db/structures/comp1_V0_k444.xyz --label comp1 \
        --out_root /home/ubuntu/work/runs/comp1_v3/disorder_diffusion \
        --disorder_levels 0.0 0.5 --n_configs 3 \
        --temperatures 600 800 1000 --equilib_ps 5 --prod_ps 50 \
        --device cuda
Then the same for modelc (--v0_xyz <modelc V0 xyz> --label modelc ...).

Cost ~ (n_levels with d=0 counts as 1 replica) * n_configs * n_T MD runs.
Default comp1: (1 + 3) configs * 3 T = 12 MD * ~35-45 min = ~7-9 h. Run in bg.
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

kB_eV = 8.617333262e-5  # eV/K


# ----------------------------- disorder model -----------------------------
def identify_free_anions(atoms, p_s_cut=2.6):
    """Return (free_S_idx, hal_idx). free S = S with no P neighbor < p_s_cut.
    hal_idx = ALL halides (Cl, Br, I) so mixed-halide argyrodites (e.g. comp2
    Li6PS5Cl0.5Br0.5) disorder BOTH Cl<->S2- and Br<->S2-. Pure-Cl systems
    (comp1/modelc) are unaffected (no Br/I present)."""
    syms = np.array(atoms.get_chemical_symbols())
    P_idx = np.where(syms == "P")[0]
    S_idx = np.where(syms == "S")[0]
    Cl_idx = np.where(np.isin(syms, ["Cl", "Br", "I"]))[0].tolist()
    if len(P_idx) == 0:
        return S_idx.tolist(), Cl_idx
    D = atoms.get_all_distances(mic=True)
    free_S = []
    for s in S_idx:
        if D[s, P_idx].min() >= p_s_cut:
            free_S.append(int(s))
    return free_S, Cl_idx


def make_disordered(atoms, n_swaps, free_S, cl_idx, rng):
    """Swap n_swaps free-S <-> Cl identities at fixed positions. Returns a copy."""
    a = atoms.copy()
    syms = list(a.get_chemical_symbols())
    if n_swaps <= 0:
        return a, []
    s_pick = rng.choice(free_S, size=n_swaps, replace=False)
    c_pick = rng.choice(cl_idx, size=n_swaps, replace=False)
    swaps = []
    for s, c in zip(s_pick, c_pick):
        syms[s], syms[c] = syms[c], syms[s]   # S-site becomes Cl, Cl-site becomes S
        swaps.append((int(s), int(c)))
    a.set_chemical_symbols(syms)
    return a, swaps


# ----------------------------- MSD (cell-correct) -----------------------------
def li_diffusion_from_frames(frames, save_fs, fit_window_ps):
    """Cell-correct unwrap in fractional coords; MSD(Li); D from MSD=6Dt fit."""
    syms = np.array(frames[0].get_chemical_symbols())
    li = syms == "Li"
    cell = frames[0].cell.array  # NVT -> fixed cell
    # fractional positions, wrapped
    spos = np.array([f.get_scaled_positions(wrap=True) for f in frames])  # (T,N,3)
    dspos = np.diff(spos, axis=0)
    dspos -= np.round(dspos)                       # minimum image in fractional
    spos_uw = np.concatenate([spos[:1], spos[:1] + np.cumsum(dspos, axis=0)],
                             axis=0)
    cart = spos_uw @ cell                          # (T,N,3) Cartesian, unwrapped
    ref = cart[0, li]
    disp2 = ((cart[:, li] - ref) ** 2).sum(axis=-1)  # (T, n_Li)
    msd = disp2.mean(axis=-1)                        # (T,)
    t_ps = np.arange(len(frames)) * save_fs / 1000.0
    lo, hi = fit_window_ps
    m = (t_ps >= lo) & (t_ps <= hi)
    if m.sum() < 3:
        return None, t_ps.tolist(), msd.tolist()
    slope = np.polyfit(t_ps[m], msd[m], 1)[0]        # Å²/ps
    D = slope / 6.0 * 1e-4                            # Å²/ps -> cm²/s
    return float(D), t_ps.tolist(), msd.tolist()


def run_md(atoms, calc, T, equilib_ps, prod_ps, dt_fs, friction, save_fs,
           out_dir, fit_window_ps, seed, save_traj=False):
    out_dir.mkdir(parents=True, exist_ok=True)
    atoms = atoms.copy()
    atoms.calc = calc
    rng_seed = seed
    MaxwellBoltzmannDistribution(atoms, temperature_K=T, rng=np.random.default_rng(rng_seed))
    dt = dt_fs * units.fs
    md = Langevin(atoms, dt, temperature_K=T, friction=friction,
                  logfile=str(out_dir / "md.log"))
    md.run(int(equilib_ps * 1000 / dt_fs))
    save_int = max(1, int(save_fs / dt_fs))
    frames = []
    md.attach(lambda: frames.append(atoms.copy()), interval=save_int)
    md.run(int(prod_ps * 1000 / dt_fs))
    D, t_ps, msd = li_diffusion_from_frames(frames, save_fs, fit_window_ps)
    (out_dir / "msd.json").write_text(json.dumps(
        {"T_K": T, "D_Li_cm2_s": D, "times_ps": t_ps, "msd_Li_A2": msd}, indent=2))
    if save_traj:
        # full production trajectory (extended-xyz) for jump stats / Li-density
        # cube / van Hove. + sidecar meta so downstream tools auto-read save_fs.
        write(str(out_dir / "traj.xyz"), frames)
        (out_dir / "aimd_results.json").write_text(json.dumps(
            {"T_K": T, "save_fs": save_fs, "n_frames": len(frames),
             "prod_ps": prod_ps, "dt_fs": dt_fs}, indent=2))
    return D


def arrhenius(Ts, Ds):
    Ts, Ds = np.asarray(Ts, float), np.asarray(Ds, float)
    m = Ds > 0
    if m.sum() < 2:
        return None
    slope, intc = np.polyfit(1.0 / Ts[m], np.log(Ds[m]), 1)
    Ea = -slope * kB_eV
    D0 = float(np.exp(intc))
    D300 = D0 * np.exp(-Ea / (kB_eV * 300.0))
    return {"Ea_eV": float(Ea), "D0_cm2_s": D0,
            "D_300K_cm2_s": float(D300),
            "points": [{"T_K": float(t), "D_cm2_s": float(d)}
                       for t, d in zip(Ts[m], Ds[m])]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--v0_xyz", required=True)
    ap.add_argument("--label", required=True, help="comp1 or modelc")
    ap.add_argument("--out_root", required=True)
    ap.add_argument("--disorder_levels", type=float, nargs="+",
                    default=[0.0, 0.5],
                    help="anti-site fractions to test (0.0 = ordered baseline)")
    ap.add_argument("--n_configs", type=int, default=3,
                    help="replicas per disorder level (d=0 forced to 1)")
    ap.add_argument("--temperatures", type=float, nargs="+",
                    default=[600, 800, 1000])
    ap.add_argument("--equilib_ps", type=float, default=5.0)
    ap.add_argument("--prod_ps", type=float, default=50.0)
    ap.add_argument("--timestep_fs", type=float, default=2.0)
    ap.add_argument("--friction", type=float, default=0.02)
    ap.add_argument("--save_fs", type=float, default=100.0)
    ap.add_argument("--fit_window_ps", type=float, nargs=2, default=[5.0, 40.0])
    ap.add_argument("--save_traj", action="store_true",
                    help="dump production frames to traj.xyz + aimd_results.json "
                         "(enables jump stats / Li-density cube / van Hove)")
    ap.add_argument("--p_s_cut", type=float, default=2.6)
    ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--uma_model", default="uma-s-1p1")
    ap.add_argument("--uma_task", default="omat")
    ap.add_argument("--device", default="cuda")
    args = ap.parse_args()

    out_root = Path(args.out_root)
    out_root.mkdir(parents=True, exist_ok=True)
    base = read(args.v0_xyz)
    free_S, cl_idx = identify_free_anions(base, args.p_s_cut)
    n_sites = len(free_S) + len(cl_idx)
    max_swaps = min(len(free_S), len(cl_idx))
    print(f"[{args.label}] {len(base)} atoms | free-S={len(free_S)} Cl={len(cl_idx)} "
          f"| free-anion sites={n_sites} | max_swaps={max_swaps}")

    # one UMA load for the whole ensemble
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    predictor = pretrained_mlip.get_predict_unit(args.uma_model, device=args.device)
    calc = FAIRChemCalculator(predictor, task_name=args.uma_task)

    rng = np.random.default_rng(args.seed)
    t_start = time.time()
    levels_out = []
    for d in args.disorder_levels:
        n_swaps = int(round(d * n_sites / 2.0))
        n_swaps = min(n_swaps, max_swaps)
        d_actual = 2.0 * n_swaps / n_sites if n_sites else 0.0
        nconf = 1 if n_swaps == 0 else args.n_configs
        print(f"\n##### disorder d={d} -> n_swaps={n_swaps} (actual d={d_actual:.3f}), "
              f"{nconf} config(s) #####")
        config_results = []
        for ci in range(nconf):
            atoms_d, swaps = make_disordered(base, n_swaps, free_S, cl_idx, rng)
            cdir = out_root / f"d{d_actual:.2f}_cfg{ci}"
            cdir.mkdir(parents=True, exist_ok=True)
            write(str(cdir / "config.xyz"), atoms_d)
            Ds = []
            for T in args.temperatures:
                t0 = time.time()
                D = run_md(atoms_d, calc, T, args.equilib_ps, args.prod_ps,
                           args.timestep_fs, args.friction, args.save_fs,
                           cdir / f"T{int(T)}", tuple(args.fit_window_ps),
                           seed=args.seed + 1000 * ci + int(T),
                           save_traj=args.save_traj)
                Ds.append(D)
                print(f"    d={d_actual:.2f} cfg{ci} T={int(T)}: "
                      f"D_Li={D:.3e} cm²/s  ({(time.time()-t0)/60:.1f} min)")
            arr = arrhenius(args.temperatures, Ds)
            config_results.append({"config": ci, "swaps": swaps,
                                   "D_per_T": Ds, "arrhenius": arr})
            if arr:
                print(f"    -> cfg{ci} Ea={arr['Ea_eV']:.4f} eV  D0={arr['D0_cm2_s']:.3e}")
            # incremental save (crash-safe)
            (out_root / "ensemble_results.json").write_text(json.dumps({
                "label": args.label, "v0_xyz": args.v0_xyz,
                "free_anion_sites": n_sites, "temperatures": args.temperatures,
                "equilib_ps": args.equilib_ps, "prod_ps": args.prod_ps,
                "fit_window_ps": args.fit_window_ps,
                "levels": levels_out + [{
                    "disorder_target": d, "disorder_actual": d_actual,
                    "n_swaps": n_swaps, "configs": config_results}],
            }, indent=2, default=str))
        # aggregate Ea over configs at this level
        Eas = [c["arrhenius"]["Ea_eV"] for c in config_results if c["arrhenius"]]
        D0s = [c["arrhenius"]["D0_cm2_s"] for c in config_results if c["arrhenius"]]
        agg = {"disorder_target": d, "disorder_actual": d_actual,
               "n_swaps": n_swaps, "n_configs": len(config_results),
               "Ea_mean_eV": float(np.mean(Eas)) if Eas else None,
               "Ea_std_eV": float(np.std(Eas)) if Eas else None,
               "D0_mean_cm2_s": float(np.mean(D0s)) if D0s else None,
               "configs": config_results}
        levels_out.append(agg)
        if Eas:
            print(f"### d={d_actual:.2f}: Ea = {np.mean(Eas):.4f} ± "
                  f"{np.std(Eas):.4f} eV  (n={len(Eas)})")

    summary = {
        "label": args.label, "v0_xyz": args.v0_xyz,
        "free_anion_sites": n_sites, "temperatures": args.temperatures,
        "equilib_ps": args.equilib_ps, "prod_ps": args.prod_ps,
        "fit_window_ps": args.fit_window_ps,
        "uma_model": args.uma_model, "uma_task": args.uma_task,
        "runtime_min": (time.time() - t_start) / 60,
        "levels": levels_out,
        "headline": [{"d": L["disorder_actual"], "Ea_eV": L["Ea_mean_eV"],
                      "Ea_std": L["Ea_std_eV"], "D0": L["D0_mean_cm2_s"]}
                     for L in levels_out],
    }
    (out_root / "ensemble_results.json").write_text(
        json.dumps(summary, indent=2, default=str))
    print(f"\n==== {args.label} DONE ({summary['runtime_min']:.0f} min) ====")
    for h in summary["headline"]:
        print(f"  d={h['d']:.2f}  Ea={h['Ea_eV']} ± {h['Ea_std']} eV  D0={h['D0']}")
    print(f"  → {out_root / 'ensemble_results.json'}")


if __name__ == "__main__":
    main()

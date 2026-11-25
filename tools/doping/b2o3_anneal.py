#!/usr/bin/env python3
"""Step 3 — Li annealing (pipeline v2 §3). Thermal re-optimization of a champion
doped structure to escape 0K-relax local minima before EOS/DFT.

The screening (Step 2) ranks at 0K static relax → can trap in a local basin and
mis-rank. A 500K UMA-MD anneal lets Li hop (Eₐ≈0.2 eV ≪ kT@500K) and S²⁻ relax
slightly, finding a deeper basin. Cl⁻/PS₄ stay intact (T < 800K cage / 1500K PS₄
limits). This pre-empts the basin-switch risk of the later DFT relax (Step 5).

Protocol (pipeline §3):
  heat   0→500 K   5 ps   (linear ramp)
  anneal 500 K    50 ps   (Li hopping)
  quench 500→0 K  10 ps
  final  UMA relax fmax ≤ 0.05   (cell fixed; volume handled by Step 4 EOS)

NVT (Langevin), cell FIXED (Li/anion re-opt only). Reports E before vs after —
if anneal finds lower E, ranking would have been wrong → champion updated.

Deps: ase, fairchem. Usage:
  python3 b2o3_anneal.py --struct champion/o019.cif --out b2o3_anneal \
      --T 500 --heat_ps 5 --anneal_ps 50 --quench_ps 10 --task omat
"""
import argparse, time
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase import units
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.optimize import FIRE


def make_calc(task, device):
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    return FAIRChemCalculator(pretrained_mlip.get_predict_unit("uma-s-1p1", device=device),
                              task_name=task)


def ramp(dyn, atoms, T0, T1, ps, dt_fs, log, label):
    n = max(1, int(ps * 1000 / dt_fs))
    for i in range(n):
        T = T0 + (T1 - T0) * (i + 1) / n
        dyn.set_temperature(temperature_K=T)
        dyn.run(1)
        if i % 200 == 0:
            print(f"  [{label}] {i*dt_fs/1000:.1f}/{ps}ps  T~{T:.0f}K  "
                  f"E={atoms.get_potential_energy():.3f}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--struct", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--T", type=float, default=500.0)
    ap.add_argument("--heat_ps", type=float, default=5.0)
    ap.add_argument("--anneal_ps", type=float, default=50.0)
    ap.add_argument("--quench_ps", type=float, default=10.0)
    ap.add_argument("--dt_fs", type=float, default=2.0)
    ap.add_argument("--friction", type=float, default=0.02)
    ap.add_argument("--task", default="omat", help="bulk doped crystal -> omat (NOT oc20)")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--seed", type=int, default=0,
                    help="RNG seed for MD velocities/Langevin. Vary it for an ENSEMBLE: "
                         "the EOS is deterministic, the anneal seed is the only stochastic "
                         "part -> N seeds give V0/B0 mean±std (Li-ordering variance).")
    A = ap.parse_args()
    out = Path(A.out); out.mkdir(parents=True, exist_ok=True)
    np.random.seed(A.seed)
    try:
        import torch; torch.manual_seed(A.seed)
    except Exception:
        pass

    atoms = read(A.struct)
    atoms.calc = make_calc(A.task, A.device)
    E0 = atoms.get_potential_energy()
    print(f"[anneal] {len(atoms)} atoms, start E={E0:.4f} eV ({E0/len(atoms):.5f}/atom), "
          f"cell FIXED, task={A.task}")

    MaxwellBoltzmannDistribution(atoms, temperature_K=A.T * 0.5)
    dyn = Langevin(atoms, A.dt_fs * units.fs, temperature_K=A.T,
                   friction=A.friction / units.fs)
    traj = out / "anneal.traj"
    from ase.io.trajectory import Trajectory
    dyn.attach(Trajectory(str(traj), "w", atoms).write, interval=200)

    t0 = time.time()
    ramp(dyn, atoms, 0.0, A.T, A.heat_ps, A.dt_fs, None, "heat")
    ramp(dyn, atoms, A.T, A.T, A.anneal_ps, A.dt_fs, None, "anneal")
    ramp(dyn, atoms, A.T, 0.0, A.quench_ps, A.dt_fs, None, "quench")
    print(f"[anneal] MD done ({time.time()-t0:.0f}s). final relax...")

    FIRE(atoms, logfile=str(out / "final_relax.log")).run(fmax=0.05, steps=400)
    E1 = atoms.get_potential_energy()
    write(str(out / "annealed_relaxed.cif"), atoms)
    write(str(out / "annealed_relaxed.xyz"), atoms)

    dE = E1 - E0
    print(f"\n=== Step 3 anneal result ===")
    print(f"  before: {E0:.4f} eV ({E0/len(atoms):.5f}/atom)")
    print(f"  after : {E1:.4f} eV ({E1/len(atoms):.5f}/atom)")
    print(f"  ΔE = {dE*1000:.1f} meV ({dE/len(atoms)*1000:.2f} meV/atom)")
    print("  =>", "anneal found DEEPER basin (champion updated; 0K rank was off)"
          if dE < -0.01 else "0K champion stable (anneal confirms)")
    print(f"  -> {out}/annealed_relaxed.cif  (Step 4 MLIP EOS 입력)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""run_li_interface_md.py — relax + NVT MD of an SE|Li interface with UMA (no DFT).

Loads the interface built by build_li_interface.py, re-applies the bottom-layer
freeze (SE atoms within --fix_bottom A of the slab bottom), relaxes the geometry,
then runs Langevin NVT MD and dumps a trajectory for decomposition analysis.
Same fairchem/UMA machinery as tools/modelc_v3/disorder_ensemble_diffusion.py.

  python3 tools/oxidation/run_li_interface_md.py \
    --interface interface_b2o3_Li.xyz --label b2o3 \
    --temperature 600 --equilib_ps 2 --prod_ps 50 --device cuda
"""
import argparse
import numpy as np
from ase.io import read, write
from ase.constraints import FixAtoms
from ase.optimize import FIRE
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase import units


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interface", required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--temperature", type=float, default=600.0)
    ap.add_argument("--equilib_ps", type=float, default=2.0)
    ap.add_argument("--prod_ps", type=float, default=50.0)
    ap.add_argument("--dt_fs", type=float, default=1.0, help="1 fs (reactive interface + Li metal)")
    ap.add_argument("--friction", type=float, default=0.01)
    ap.add_argument("--save_fs", type=float, default=200.0)
    ap.add_argument("--fix_bottom", type=float, default=6.0, help="freeze SE atoms within this many A of the slab bottom")
    ap.add_argument("--relax_fmax", type=float, default=0.08)
    ap.add_argument("--relax_steps", type=int, default=300)
    ap.add_argument("--uma_model", default="uma-s-1p1")
    ap.add_argument("--uma_task", default="omat")
    ap.add_argument("--device", default="cuda")
    a = ap.parse_args()

    atoms = read(a.interface)
    sym = np.array(atoms.get_chemical_symbols())
    z = atoms.positions[:, 2]
    se_mask = sym != "Li"
    zmin_se = z[se_mask].min()
    fix = se_mask & (z < zmin_se + a.fix_bottom)
    atoms.set_constraint(FixAtoms(mask=fix))
    print(f"[{a.label}] atoms={len(atoms)}  SE={se_mask.sum()}  Li={(~se_mask).sum()}  frozen={fix.sum()}")

    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    calc = FAIRChemCalculator(pretrained_mlip.get_predict_unit(a.uma_model, device=a.device), task_name=a.uma_task)
    atoms.calc = calc

    # geometry relaxation (fixed cell) — lets the interface reconstruct before MD
    print(f">> relax (fmax={a.relax_fmax}, max {a.relax_steps} steps)")
    FIRE(atoms, logfile=f"{a.label}_relax.log").run(fmax=a.relax_fmax, steps=a.relax_steps)
    write(f"{a.label}_relaxed.xyz", atoms)

    # NVT MD
    print(f">> MD  T={a.temperature}K  equilib {a.equilib_ps}ps + prod {a.prod_ps}ps  dt={a.dt_fs}fs")
    MaxwellBoltzmannDistribution(atoms, temperature_K=a.temperature)
    dyn = Langevin(atoms, a.dt_fs * units.fs, temperature_K=a.temperature, friction=a.friction / units.fs)
    save_int = max(1, int(a.save_fs / a.dt_fs))
    frames = []
    dyn.attach(lambda: frames.append(atoms.copy()), interval=save_int)

    dyn.run(int(a.equilib_ps * 1000 / a.dt_fs))    # equilibrate
    frames.clear()                                  # discard equilibration frames
    dyn.run(int(a.prod_ps * 1000 / a.dt_fs))        # production
    write(f"{a.label}_traj.xyz", frames)
    print(f">> done: {len(frames)} production frames -> {a.label}_traj.xyz")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Step 4 — MLIP EOS (pipeline v2 §4). Volume sweep on the annealed V0 → V₀, B₀, B₀'
(1st guess) + the volume grid for the later DFT EOS (Step 5/6).

Per pipeline §4: 7-point isotropic volume sweep (96..108 % of V₀), at each point
scale the cell isotropically and relax ATOMS (cell FIXED), then 3rd-order
Birch–Murnaghan fit. UMA (omat) for a bulk doped crystal.

NOTE (pipeline §0.3): BM fit window is ±6 % (basin-consistent). +8 % point is for
V₀-tail sanity only — flagged, not fit. Watch for basin switch (large E jump).

Deps: ase, fairchem. Usage:
  python3 b2o3_eos.py --struct anneal_cfg0000_o019/annealed_relaxed.cif \
      --out b2o3_eos --task omat
"""
import argparse, json
from pathlib import Path
import numpy as np
from ase.io import read, write
from ase.optimize import FIRE
from ase.eos import EquationOfState
from ase.units import kJ


def make_calc(task, device):
    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    return FAIRChemCalculator(pretrained_mlip.get_predict_unit("uma-s-1p1", device=device),
                              task_name=task)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--struct", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--scales", default="0.96,0.98,1.00,1.02,1.04,1.06,1.08")
    ap.add_argument("--fit_lo", type=float, default=0.94, help="BM fit volume window low")
    ap.add_argument("--fit_hi", type=float, default=1.06, help="BM fit volume window high")
    ap.add_argument("--fmax", type=float, default=0.03)
    ap.add_argument("--task", default="omat")
    ap.add_argument("--device", default="cuda")
    A = ap.parse_args()
    out = Path(A.out); out.mkdir(parents=True, exist_ok=True)
    calc = make_calc(A.task, A.device)

    v0 = read(A.struct)
    V0 = v0.get_volume()
    scales = [float(s) for s in A.scales.split(",")]
    print(f"[eos] {len(v0)} atoms, V0(input)={V0:.2f} Å³, {len(scales)} pts "
          f"({min(scales)}..{max(scales)}), task={A.task}")

    rows = []
    for s in scales:
        a = v0.copy()
        f = s ** (1.0 / 3.0)                       # volume scale -> linear scale
        a.set_cell(v0.cell.array * f, scale_atoms=True)
        a.calc = calc
        FIRE(a, logfile=str(out / f"relax_{s:.2f}.log")).run(fmax=A.fmax, steps=300)
        V, E = a.get_volume(), a.get_potential_energy()
        rows.append((s, V, E))
        write(str(out / f"v_{s:.2f}.cif"), a)
        print(f"  scale {s:.2f}  V={V:.2f}  E={E:.4f} eV  (E/at {E/len(a):.5f})", flush=True)

    # basin sanity: flag large E jumps (non-smooth = possible basin switch)
    Es = [r[2] for r in rows]
    print("  ΔE between adjacent pts (meV):",
          [round((Es[i+1]-Es[i])*1000, 1) for i in range(len(Es)-1)])

    fit = [(V, E) for s, V, E in rows if A.fit_lo <= s <= A.fit_hi]
    Vf = np.array([x[0] for x in fit]); Ef = np.array([x[1] for x in fit])
    eos = EquationOfState(Vf, Ef, eos="birchmurnaghan")
    Vmin, Emin, B = eos.fit()
    B_GPa = B / kJ * 1.0e24
    # R^2
    from numpy.polynomial import polynomial as P
    pred = eos.func(Vf, *eos.eos_parameters)
    ss_res = float(np.sum((Ef - pred) ** 2)); ss_tot = float(np.sum((Ef - Ef.mean()) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot else float("nan")

    res = dict(struct=A.struct, n_atoms=len(v0), V0_A3=float(Vmin),
               V0_per_atom=float(Vmin/len(v0)), E0_eV=float(Emin),
               B0_GPa=float(B_GPa), R2=float(r2),
               fit_window=[A.fit_lo, A.fit_hi], points=[[s, V, E] for s, V, E in rows])
    json.dump(res, open(out / "eos_result.json", "w"), indent=2)
    print(f"\n=== Step 4 MLIP EOS (BM3, {A.fit_lo}-{A.fit_hi} window) ===")
    print(f"  V0 = {Vmin:.2f} Å³ ({Vmin/len(v0):.3f}/atom)   E0 = {Emin:.4f} eV")
    print(f"  B0 = {B_GPa:.2f} GPa   R² = {r2:.5f}")
    print(f"  -> {out}/eos_result.json + v_*.cif (DFT EOS volume grid for Step 5)")
    print(f"  (compare to undoped modelC B0 for Paper #2 ΔB0)")


if __name__ == "__main__":
    main()

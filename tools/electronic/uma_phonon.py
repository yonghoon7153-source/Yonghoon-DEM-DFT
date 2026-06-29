#!/usr/bin/env python3
"""UMA Gamma-point phonons -> dynamical stability + lowest modes.

Finite-displacement Hessian with the UMA(omat) calculator (ASE Vibrations),
to test whether the B2O3-doped champion is a true local minimum (no/few
imaginary modes) and to list the soft modes. Runs on gabia (UMA + GPU).

  python3 tools/electronic/uma_phonon.py --xyz db/structures/b2o3_relaxV0.xyz \
      --out /data/work/runs/b2o3_phonon

768 force evals for 128 atoms (~10-30 min on a shared GPU). A handful of small
imaginary modes (> -30 cm^-1) near Gamma are normal for a disordered cell; many
large ones mean the structure is not a minimum.
"""
import argparse, numpy as np
from ase.io import read
from ase.vibrations import Vibrations


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xyz", required=True)
    ap.add_argument("--out", default="b2o3_phonon")
    ap.add_argument("--delta", type=float, default=0.02)
    ap.add_argument("--device", default="cuda")
    args = ap.parse_args()

    from fairchem.core import pretrained_mlip
    from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
    atoms = read(args.xyz)
    atoms.calc = FAIRChemCalculator(
        pretrained_mlip.get_predict_unit("uma-s-1p1", device=args.device),
        task_name="omat")

    vib = Vibrations(atoms, delta=args.delta, name=args.out + "_cache")
    vib.run()
    fr = vib.get_frequencies()          # cm^-1, complex for imaginary
    real = np.array([f.real if abs(f.imag) < 1e-6 else -abs(f.imag) for f in fr])
    real.sort()
    np.savetxt(args.out + "_freqs.txt", real, fmt="%.3f",
               header="phonon frequencies cm^-1 (negative = imaginary)")
    n_imag = int((real < -30).sum())
    n_small_imag = int(((real >= -30) & (real < -5)).sum())
    print(f"n_modes={len(real)}  imaginary(<-30 cm^-1)={n_imag}  "
          f"small-imag(-30..-5)={n_small_imag}")
    print("lowest 12 cm^-1:", np.round(real[:12], 1).tolist())
    print("verdict:", "DYNAMICALLY STABLE (champion is a local minimum)"
          if n_imag == 0 else f"{n_imag} sizeable imaginary modes -> check")
    print(f"-> {args.out}_freqs.txt")


if __name__ == "__main__":
    main()

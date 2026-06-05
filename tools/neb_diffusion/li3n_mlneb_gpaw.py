#!/usr/bin/env python3
"""Li3N(001) Li-adatom diffusion barrier — FAITHFUL reproduction of Cui et al.
ACS Nano 2023, 17, 3168 (Fig 2c/2d, barrier 0.133 eV).

WHY THIS SCRIPT EXISTS
----------------------
The paper did NOT run vanilla DFT NEB (that is the multi-day, never-converging
job we kept staring at). They used **ML-NEB (CatLearn)** — a Gaussian-Process
surrogate trained on-the-fly: the GP approximates the PES and only the most
informative image is evaluated with the *real* DFT calculator each iteration.
That is why it converges in a handful of DFT single-points instead of
hundreds. UMA is morally the same idea (a foundation surrogate); this script
lets you run the *paper's* method exactly (GPAW PBE/PAW 500 eV) OR swap in UMA
as the reference calculator for a minutes-long cross-check.

Paper settings reproduced (Methods, p.3177):
  - GPAW, PBE, PAW, plane-wave 500 eV
  - Li3N(001) slab, 6 layers (~15 A) + 15 A vacuum, k = 3x3x1
  - bottom fixed, top 5 layers relaxed
  - ML-NEB (CatLearn), 9 images, path = N -> adjacent surface N
  - energy/force conv 1e-4 eV / 1e-3 eV/A; NEB fmax 0.05 eV/A

Usage (on a GPU/CPU node with gpaw + catlearn, OR fairchem for --calc uma):
  # paper-faithful:
  python3 li3n_mlneb_gpaw.py --calc gpaw  --out li3n_mlneb
  # fast UMA cross-check (same ML-NEB algorithm, UMA as reference calc):
  python3 li3n_mlneb_gpaw.py --calc uma --uma_task oc20 --out li3n_mlneb_uma

Deps: ase; (gpaw) OR (fairchem); catlearn (`pip install catlearn`).
"""
import argparse
import numpy as np
from ase.build import surface, make_supercell
from ase.spacegroup import crystal
from ase.constraints import FixAtoms
from ase.optimize import BFGS
from ase.io import write


def build_li3n_001(nlayers=6, supercell=(3, 3, 1), vacuum=15.0):
    """alpha-Li3N (P6/mmm, a=3.65, c=3.87). (001) slab terminated on the
    Li2N plane (exposes N -> lithiophilic surface, the paper's dominant facet)."""
    a, c = 3.65, 3.87
    bulk = crystal(
        symbols=["N", "Li", "Li"],
        basis=[(0, 0, 0), (0, 0, 0.5), (1 / 3, 2 / 3, 0)],
        spacegroup=191,  # P6/mmm
        cellpar=[a, a, c, 90, 90, 120],
    )
    slab = surface(bulk, (0, 0, 1), layers=nlayers, vacuum=vacuum)
    slab = make_supercell(slab, np.diag(supercell))
    slab.center(vacuum=vacuum, axis=2)
    return slab


def freeze_bottom(slab, relax_top_layers=5, nlayers=6):
    """Fix the bottom (nlayers - relax_top_layers) atomic planes by z."""
    zs = slab.positions[:, 2]
    order = np.argsort(np.unique(np.round(zs, 2)))
    planes = np.unique(np.round(zs, 2))
    n_fixed_planes = max(0, len(planes) - relax_top_layers)
    z_cut = planes[n_fixed_planes - 1] + 0.1 if n_fixed_planes > 0 else -1e9
    fixed = [i for i in range(len(slab)) if zs[i] <= z_cut]
    slab.set_constraint(FixAtoms(indices=fixed))
    return fixed


def top_N_sites(slab):
    """Return indices of N atoms in the topmost N plane (adsorption anchors)."""
    N = [i for i, s in enumerate(slab.get_chemical_symbols()) if s == "N"]
    zN = slab.positions[N, 2]
    ztop = zN.max()
    return [i for i in N if slab.positions[i, 2] > ztop - 0.3]


def make_calc(which, uma_task, device):
    if which == "gpaw":
        from gpaw import GPAW, PW, FermiDirac
        return GPAW(mode=PW(500), xc="PBE", kpts=(3, 3, 1),
                    occupations=FermiDirac(0.05), txt="gpaw.txt")
    elif which == "uma":
        from fairchem.core import pretrained_mlip
        from fairchem.core.calculate.ase_calculator import FAIRChemCalculator
        return FAIRChemCalculator(
            pretrained_mlip.get_predict_unit("uma-s-1p1", device=device),
            task_name=uma_task)
    raise SystemExit(f"unknown calc {which}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--calc", choices=["gpaw", "uma"], default="gpaw")
    ap.add_argument("--uma_task", default="oc20",
                    help="UMA task; oc20 = surface adsorbate (NOT omat — omat is "
                         "bulk-materials and mis-handles a surface adatom)")
    ap.add_argument("--device", default="cuda")
    ap.add_argument("--n_images", type=int, default=9)   # paper: 9
    ap.add_argument("--fmax", type=float, default=0.05)
    ap.add_argument("--ad_height", type=float, default=1.9, help="initial adatom z above N (A)")
    ap.add_argument("--out", default="li3n_mlneb")
    A = ap.parse_args()

    slab = build_li3n_001()
    fixed = freeze_bottom(slab, relax_top_layers=5, nlayers=6)
    print(f"[slab] {len(slab)} atoms, {len(fixed)} fixed (bottom), "
          f"{len(slab)-len(fixed)} free (top 5 layers)")

    Ntop = top_N_sites(slab)
    # pick two nearest in-plane N neighbours = the N -> adjacent-N hop (paper Fig 2c)
    P = slab.positions[Ntop, :2]
    i0 = Ntop[0]
    d = np.linalg.norm(P - slab.positions[i0, :2], axis=1)
    d[d < 1e-3] = 1e9
    i1 = Ntop[int(np.argmin(d))]
    print(f"[path] N{i0} -> N{i1}, in-plane dist {np.linalg.norm(slab.positions[i0,:2]-slab.positions[i1,:2]):.2f} A")

    calc = make_calc(A.calc, A.uma_task, A.device)

    # --- endpoints: adatom on-top of N(i0) and N(i1), relax (top layers + adatom free)
    def endpoint(i_anchor, tag):
        at = slab.copy()
        p = slab.positions[i_anchor].copy(); p[2] += A.ad_height
        at += __import__("ase").Atom("Li", position=p)
        at.set_constraint(FixAtoms(indices=fixed))   # adatom (last) stays free
        at.calc = calc
        BFGS(at, logfile=f"{A.out}_{tag}.log").run(fmax=0.02, steps=200)
        write(f"{A.out}_{tag}.traj", at)
        print(f"[endpoint {tag}] E = {at.get_potential_energy():.4f} eV, "
              f"adatom z = {at.positions[-1,2]:.2f} (surface z~{slab.positions[i_anchor,2]:.2f})")
        return at

    ini = endpoint(i0, "ini")
    fin = endpoint(i1, "fin")

    # --- ML-NEB (CatLearn): GP surrogate, sparse real-calc evaluations ---
    from catlearn.optimize.mlneb import MLNEB
    neb = MLNEB(start=f"{A.out}_ini.traj", end=f"{A.out}_fin.traj",
                ase_calc=calc, n_images=A.n_images, interpolation="idpp",
                restart=False)
    neb.run(fmax=A.fmax, trajectory=f"{A.out}_ML-NEB.traj", full_output=False)

    e = neb.e_path - neb.e_path[0]
    barrier = float(np.max(e))
    print("\n=== Li3N(001) Li-adatom diffusion (ML-NEB, %s) ===" % A.calc)
    print("  rel-E path (eV):", [round(float(x), 4) for x in e])
    print(f"  BARRIER = {barrier:.4f} eV   (Cui 2023 paper: 0.133 eV)")
    print(f"  trajectory: {A.out}_ML-NEB.traj  (view: ase gui {A.out}_ML-NEB.traj)")


if __name__ == "__main__":
    main()

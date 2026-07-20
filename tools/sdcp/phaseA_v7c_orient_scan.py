#!/usr/bin/env python3
"""phaseA_v7c_orient_scan.py — SDCP v7c | LiNiO2(104) binding: 3-orientation MLIP scan.

Spec = sdcp master §2.2: consistent references (shared E_slab, same-setting molecule
ref), orientations sulfonate-down / ether-O-down / chelation (pincer), doped =
neutral radical geometry [M-H]. UMA oc20 (omat verified worse for this system).

  conda activate uma
  python3 phaseA_v7c_orient_scan.py --slab <relaxed LiNiO2(104) slab xyz/cif> \
      --moldir /data/work/runs/sdcp_linio2_binding/inputs/sdcp_v7c \
      --out    /data/work/runs/sdcp_linio2_binding/phaseA_v7c
Outputs: phaseA_v7c_results.csv + relaxed complex xyz per case + log prints.
E_bind = E(complex) - E(slab) - E(molecule)   [negative = binding]
"""
import argparse
import os
import numpy as np

from ase.io import read, write
from ase.constraints import FixAtoms
from ase.optimize import FIRE
from fairchem.core import pretrained_mlip
from fairchem.core.calculate.ase_calculator import FAIRChemCalculator


def hcount(mol, i, cut=1.25):
    d = mol.get_all_distances()
    return sum(1 for j, s in enumerate(mol.get_chemical_symbols())
               if s == "H" and j != i and d[i, j] < cut)


def find_groups(mol):
    """indices: sulfonate O's, sulfonate S, ether O (both C neighbors are sp3 CH2/CH)."""
    sym = mol.get_chemical_symbols()
    d = mol.get_all_distances()
    Ss = [i for i, s in enumerate(sym) if s == "S"
          and sum(1 for j, t in enumerate(sym) if t == "O" and d[i, j] < 1.8) >= 3]
    assert len(Ss) == 1, "sulfonate S not unique"
    sS = Ss[0]
    sO = [j for j, t in enumerate(sym) if t == "O" and d[sS, j] < 1.8]
    eth = None
    for i, s in enumerate(sym):
        if s != "O" or i in sO:
            continue
        Cn = [j for j, t in enumerate(sym) if t == "C" and d[i, j] < 1.65]
        if len(Cn) == 2 and all(hcount(mol, c) >= 1 for c in Cn):
            eth = i
            break
    assert eth is not None, "ether O not found"
    return sS, sO, eth


def orient(mol, target_vec):
    """rigid-rotate molecule so target_vec (from COM) points along -z."""
    m = mol.copy()
    com = m.get_center_of_mass()
    v = target_vec / np.linalg.norm(target_vec)
    zm = np.array([0.0, 0.0, -1.0])
    axis = np.cross(v, zm)
    if np.linalg.norm(axis) < 1e-8:
        if v[2] > 0:                      # pointing +z: flip about x
            m.rotate(180, "x", center=com)
        return m
    ang = np.degrees(np.arccos(np.clip(np.dot(v, zm), -1, 1)))
    m.rotate(ang, axis / np.linalg.norm(axis), center=com)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slab", required=True)
    ap.add_argument("--moldir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--gap", type=float, default=2.4, help="lowest mol atom above slab top (A)")
    ap.add_argument("--cz", type=float, default=0.0,
                    help="override slab c-axis (A) so standing poses are image-clean "
                         "(0=keep file cell; ~40 for the tall SDCP molecule; fixes the v1 "
                         "image-sandwich where a standing pose touched the vertical image)")
    ap.add_argument("--fmax", type=float, default=0.05)
    ap.add_argument("--steps", type=int, default=300)
    ap.add_argument("--freeze_frac", type=float, default=0.5,
                    help="fix slab atoms with z below this fraction of the slab thickness; "
                         "1.0 = freeze the ENTIRE slab (use for a clean DFT-relaxed substrate "
                         "so UMA cannot reconstruct it -- only the molecule relaxes)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    calc = FAIRChemCalculator(pretrained_mlip.get_predict_unit("uma-s-1p1", device="cuda"),
                              task_name="oc20")

    # ---- shared slab reference ----
    slab0 = read(a.slab)
    if a.cz > 0:                                    # extend vacuum so standing poses are image-clean
        cell = slab0.cell.array.copy(); cell[2, 2] = a.cz
        slab0.set_cell(cell); slab0.pbc = True
        print(f"c-axis -> {a.cz} A (vacuum above slab {a.cz - slab0.positions[:, 2].max():.1f} A)", flush=True)
    area = float(np.linalg.norm(np.cross(slab0.cell.array[0], slab0.cell.array[1])))
    if area < 1.0:                                  # a bare .xyz has NO cell -> degenerate -> garbage energies
        raise SystemExit(f"SLAB CELL DEGENERATE (in-plane area {area:.2f} A^2). Use a .vasp/.cif slab WITH a "
                         f"cell, NOT a bare .xyz.\ncell=\n{slab0.cell.array}")
    zs = slab0.positions[:, 2]
    if a.freeze_frac >= 1.0:
        fix = FixAtoms(indices=list(range(len(slab0))))     # freeze whole slab
    else:
        zcut = zs.min() + a.freeze_frac * (zs.max() - zs.min())
        fix = FixAtoms(indices=[i for i in range(len(slab0)) if slab0.positions[i, 2] < zcut])
    slab = slab0.copy()
    slab.set_constraint(fix)
    slab.calc = calc
    FIRE(slab, logfile=None).run(fmax=a.fmax, steps=200)
    E_slab = slab.get_potential_energy()
    ztop = slab.positions[:, 2].max()
    print(f"E_slab = {E_slab:.4f} eV  (top z={ztop:.2f})", flush=True)

    rows = []
    for tag, mult in [("neutral", 1), ("doped", 2)]:
        mol0 = read(os.path.join(a.moldir, f"sdcp_v7c_{tag}.xyz"))
        # gas reference (same setting; UMA has no charge/mult knob -> geometry-level ref)
        g = mol0.copy()
        g.center(vacuum=10.0)
        g.calc = calc
        FIRE(g, logfile=None).run(fmax=a.fmax, steps=300)
        E_mol = g.get_potential_energy()
        print(f"[{tag}] E_mol = {E_mol:.4f} eV", flush=True)

        sS, sO, eth = find_groups(mol0)
        com = mol0.get_center_of_mass()
        heads = {
            "sulfonate_down": mol0.positions[sO].mean(axis=0) - com,
            "etherO_down":    mol0.positions[eth] - com,
            "chelation":      0.5 * (mol0.positions[sO].mean(axis=0) + mol0.positions[eth]) - com,
        }
        for oname, vec in heads.items():
            for rot in (0, 90, 180, 270):    # 4-fold: finer search for the true optimum
                m = orient(mol0, vec)
                m.rotate(rot, "z", center=m.get_center_of_mass())
                # place above slab center
                cellc = slab.cell.array[0] * 0.5 + slab.cell.array[1] * 0.5
                m.positions[:, :2] += cellc[:2] - m.get_center_of_mass()[:2]
                m.positions[:, 2] += (ztop + a.gap) - m.positions[:, 2].min()
                comp = slab.copy() + m
                comp.set_constraint(fix)
                comp.calc = calc
                FIRE(comp, logfile=None).run(fmax=a.fmax, steps=a.steps)
                E = comp.get_potential_energy()
                eb = E - E_slab - E_mol
                label = f"{tag}_{oname}_r{rot}"
                write(os.path.join(a.out, f"complex_{label}.xyz"), comp)
                rows.append((label, E, eb))
                print(f"  {label:34s} E_bind = {eb:+.3f} eV", flush=True)

    with open(os.path.join(a.out, "phaseA_v7c_results.csv"), "w") as f:
        f.write("label,E_complex_eV,E_bind_eV\n")
        for label, E, eb in rows:
            f.write(f"{label},{E:.4f},{eb:.4f}\n")
        f.write(f"# E_slab={E_slab:.4f} (shared); refs: gas-phase UMA relax per molecule; oc20\n")
    best = sorted(rows, key=lambda r: r[2])
    print("\n=== ranking (best first) ===")
    for label, E, eb in best[:6]:
        print(f"  {eb:+.3f} eV  {label}")
    print(f"saved: {a.out}/phaseA_v7c_results.csv")


if __name__ == "__main__":
    main()

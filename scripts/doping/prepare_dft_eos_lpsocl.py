#!/usr/bin/env python3
"""prepare_dft_eos_lpsocl.py — fixed-cell DFT EOS inputs for the LPSOCl champion.

Pipeline-v2 Step 5 (argyrodite_mechanical_pipeline.md): 7 volume points
(94-106% of the UMA-V0 cell), each a FIXED-CELL atom relax (cell_dofree none;
NO vc-relax anywhere in this pipeline). Template cloned from
scripts/adhesion/prepare_dft_eos_nd.py (comp5/Nd conventions: ecut 60/480,
K 2 2 1, mv 0.01, local-TF mixing) minus the Nd spin/U branch — LPSOCl
(Li5.4PS4.2O0.2Cl1.6) is closed-shell.

Usage (KISTI login node, conda activate uma):
  python3 prepare_dft_eos_lpsocl.py \
      --structure /scratch/x3430a02/kgy/lpsocl_eos/champion_umaV0.xyz \
      --out_base  /scratch/x3430a02/kgy/lpsocl_eos
Creates: v094/relax.in ... v106/relax.in + prep_summary.json
"""
import argparse
import json
import shutil
from pathlib import Path

from ase.io import read

PSEUDO_DIR = '/scratch/x3430a02/kgy/manuscript_support/pseudo'
ECUTWFC = 60.0
ECUTRHO = 480.0
DEGAUSS = 0.01
KPOINTS = "2 2 1 0 0 0"
PSEUDOS = {
    'Li': ('6.9410',  'li_pbe_v1_4_uspp_F.UPF'),
    'P':  ('30.9740', 'P_pbe-n-rrkjus_psl_1_0_0.UPF'),
    'S':  ('32.0650', 's_pbe_v1_4_uspp_F.UPF'),
    'Cl': ('35.4530', 'cl_pbe_v1_4_uspp_F.UPF'),
    'O':  ('15.9994', 'O.pbe-n-kjpaw_psl.0.1.UPF'),
}
O_PP_SRC = '/scratch/x3430a02/kgy/pseudo/O.pbe-n-kjpaw_psl.0.1.UPF'
VOLUME_RATIOS = [0.94, 0.96, 0.98, 1.00, 1.02, 1.04, 1.06]


def generate_pwin(atoms, prefix, cell_scale):
    species = sorted(set(atoms.get_chemical_symbols()))
    cell = atoms.cell.array * cell_scale
    frac = atoms.get_scaled_positions()
    L = []
    L.append("&CONTROL")
    L.append("    calculation = 'relax'")
    L.append(f"    prefix      = '{prefix}'")
    L.append("    outdir      = './tmp'")
    L.append(f"    pseudo_dir  = '{PSEUDO_DIR}'")
    L.append("    tprnfor     = .true.")
    L.append("    tstress     = .true.")
    L.append("    etot_conv_thr = 1.0d-6")
    L.append("    forc_conv_thr = 1.0d-4")
    L.append("    nstep        = 200")
    L.append("/")
    L.append("&SYSTEM")
    L.append("    ibrav       = 0")
    L.append(f"    nat         = {len(atoms)}")
    L.append(f"    ntyp        = {len(species)}")
    L.append(f"    ecutwfc     = {ECUTWFC}")
    L.append(f"    ecutrho     = {ECUTRHO}")
    L.append("    occupations = 'smearing'")
    L.append("    smearing    = 'mv'")
    L.append(f"    degauss     = {DEGAUSS}")
    L.append("    nosym       = .true.")
    L.append("/")
    L.append("&ELECTRONS")
    L.append("    conv_thr    = 1.0d-8")
    L.append("    mixing_beta = 0.05")
    L.append("    mixing_mode = 'local-TF'")
    L.append("    mixing_ndim = 16")
    L.append("    electron_maxstep = 1000")
    L.append("/")
    L.append("&IONS")
    L.append("    ion_dynamics = 'bfgs'")
    L.append("/")
    L.append("&CELL")
    L.append("    cell_dofree = 'none'")
    L.append("/")
    L.append("")
    L.append("ATOMIC_SPECIES")
    for sp in species:
        mass, ppf = PSEUDOS[sp]
        L.append(f"  {sp:<4} {mass:>10}  {ppf}")
    L.append("")
    L.append("CELL_PARAMETERS angstrom")
    for i in range(3):
        L.append(f"  {cell[i,0]:16.10f}  {cell[i,1]:16.10f}  {cell[i,2]:16.10f}")
    L.append("")
    L.append("ATOMIC_POSITIONS crystal")
    for sp, p in zip(atoms.get_chemical_symbols(), frac):
        L.append(f"  {sp:<4} {p[0]:16.10f}  {p[1]:16.10f}  {p[2]:16.10f}")
    L.append("")
    L.append("K_POINTS automatic")
    L.append(f"  {KPOINTS}")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--structure", required=True, help="UMA-relaxed champion xyz (cell = UMA V0)")
    ap.add_argument("--out_base", required=True)
    a = ap.parse_args()

    atoms = read(a.structure)
    assert atoms.cell.volume > 1.0, "structure has no cell — need the extxyz with Lattice"
    out = Path(a.out_base)
    out.mkdir(parents=True, exist_ok=True)

    # O pseudo: copy into shared pseudo dir if missing (same convention as Nd script)
    dst = Path(PSEUDO_DIR) / Path(O_PP_SRC).name
    if not dst.exists() and Path(O_PP_SRC).exists():
        shutil.copy(O_PP_SRC, dst)
        print(f"copied O pseudo -> {dst}")

    summary = {"structure": str(a.structure), "V0_A3": float(atoms.cell.volume), "volumes": {}}
    for r in VOLUME_RATIOS:
        vlabel = f"v{int(round(r*100)):03d}"
        scale = r ** (1.0 / 3.0)
        vdir = out / vlabel
        vdir.mkdir(exist_ok=True)
        (vdir / "relax.in").write_text(generate_pwin(atoms, f"lpsocl_{vlabel}", scale))
        summary["volumes"][vlabel] = {"ratio": r, "volume_A3": float(atoms.cell.volume * r)}
        print(f"  {vlabel}: V = {atoms.cell.volume*r:.2f} A^3")
    json.dump(summary, open(out / "prep_summary.json", "w"), indent=2)
    print(f"done -> {out}/v0??/relax.in  (7 fixed-cell relax inputs)")


if __name__ == "__main__":
    main()

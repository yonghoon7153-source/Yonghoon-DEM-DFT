#!/usr/bin/env python3
"""B2O3 doping — Stage 2: DFT relax of selected candidates (O-on-P vs O-on-B verdict).

UMA (Stage 1) said O goes entirely to P (BS4 + PS3O/PS2O2), B stays BS4 — BUT UMA's
B chemistry is sparsely trained, so this MUST be confirmed by DFT. Stage 2 DFT-relaxes
a small set of contrasting structures:
   - O-on-P  (UMA ground state: BS4 + PS3O/PS2O2)   [a few lowest]
   - O-on-B  (the assumed 'BO incorporation': BO2S2 / BS3O)  [contrast]
and compares E/atom. The lower-energy motif is the true B2O3 doping structure.

Generates one QE relax input per structure + a sequential GPU launcher. B-doped LPSCl
is non-magnetic, no f-electrons -> NO nspin, NO Hubbard U (unlike Nd). Standard PBE.

The --template must be a QE input whose ATOMIC_SPECIES lists ALL SIX elements
(Li P B S O Cl) with valid pseudopotentials, plus &SYSTEM (ecut...), &ELECTRONS,
and K_POINTS. (e.g. comp1 SCF input + B and O pseudo lines added.)

Deps: ase. Usage:
  python3 b2o3_stage2_dft.py \
      --structs s1.cif s2.cif ... \
      --template six_elem_template.in \
      --out_dir b2o3_stage2 --mode relax --launcher gpu
  bash b2o3_stage2/run_stage2.sh
"""
import argparse, re
from pathlib import Path
from ase.io import read


def grab_block(txt, name):
    m = re.search(rf"(&{name}\b.*?\n/\s*\n)", txt, re.S | re.I)
    return m.group(1) if m else ""


def grab_card(txt, name):
    lines, out, cap = txt.splitlines(), [], False
    for ln in lines:
        if ln.strip().upper().startswith(name):
            cap = True; out.append(ln); continue
        if cap:
            s = ln.strip()
            if s == "" or re.match(r"^[A-Z_]{3,}", s):
                break
            out.append(ln)
    return "\n".join(out)


LAUNCHERS = {
    "gpu": """#!/bin/bash
set -e
cd "$(dirname "$(realpath "$0")")"
export PATH=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin:$PATH
export LD_LIBRARY_PATH=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64
export OPAL_PREFIX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0 OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
QE=/data/apps/qe-7.4.1-gpu/bin/pw.x
MPIRUN=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin/mpirun
for f in st_*.in; do
  o="${f%.in}.out"; [ -f "$o" ] && grep -q "JOB DONE" "$o" && { echo "skip $f"; continue; }
  echo "=== $f ==="; $MPIRUN --bind-to none -np 1 $QE -inp "$f" > "$o" 2>&1 || echo "  nonzero exit"
done
python3 - <<'PY'
import glob,re
print("\\n=== Stage 2 DFT ranking (E/atom) ===")
rows=[]
for o in sorted(glob.glob("st_*.out")):
    t=open(o).read(); m=re.findall(r"!\\s+total energy\\s+=\\s+(-?\\d+\\.\\d+)",t)
    n=len(re.findall(r"\\n\\s*ATOMIC_POSITIONS",t)) or 1
    na=int(re.search(r"number of atoms/cell\\s*=\\s*(\\d+)",t).group(1)) if "number of atoms" in t else 1
    if m: rows.append((o, float(m[-1])*13.605693/na))
for o,e in sorted(rows,key=lambda r:r[1]): print(f"  {e:.5f} eV/atom   {o}")
PY
""",
    "kgpu": """#!/bin/bash
# KISTI-style: relies on `module load nvhpc/...; mpirun` already in PATH
set -e; cd "$(dirname "$(realpath "$0")")"
for f in st_*.in; do o="${f%.in}.out"; [ -f "$o" ] && grep -q "JOB DONE" "$o" && continue
  echo "=== $f ==="; mpirun -np 2 $QE -npool 2 -inp "$f" > "$o" 2>&1 || echo nonzero; done
""",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--structs", nargs="+", required=True)
    ap.add_argument("--template", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--mode", choices=["relax", "scf"], default="relax")
    ap.add_argument("--prefix", default="b2o3st")
    ap.add_argument("--pseudo_dir", default="/data/work/pseudo")
    ap.add_argument("--launcher", choices=["gpu", "kgpu"], default="gpu")
    ap.add_argument("--frac", action="store_true", help="write ATOMIC_POSITIONS crystal (else angstrom)")
    A = ap.parse_args()
    out = Path(A.out_dir); out.mkdir(parents=True, exist_ok=True)
    tmpl = Path(A.template).read_text()
    species = grab_card(tmpl, "ATOMIC_SPECIES")
    kpoints = grab_card(tmpl, "K_POINTS")
    sysnl = grab_block(tmpl, "SYSTEM"); elnl = grab_block(tmpl, "ELECTRONS")
    # sanity: template must declare all elements we will use
    tmpl_elems = set(re.findall(r"^\s*([A-Z][a-z]?)\s", species, re.M))
    calc = A.mode

    for k, sf in enumerate(A.structs):
        a = read(sf)
        nat = len(a); syms = a.get_chemical_symbols()
        elems = set(syms)
        missing = elems - tmpl_elems
        if missing:
            print(f"  ⚠ {sf}: template ATOMIC_SPECIES missing {missing} — add pseudos!")
        cell = a.cell.array
        cellstr = "CELL_PARAMETERS angstrom\n" + "\n".join(
            f"  {cell[i,0]:.10f} {cell[i,1]:.10f} {cell[i,2]:.10f}" for i in range(3))
        if A.frac:
            pos = a.get_scaled_positions(); card = "ATOMIC_POSITIONS crystal"
        else:
            pos = a.get_positions(); card = "ATOMIC_POSITIONS angstrom"
        plines = [card] + [f"  {syms[i]:3s} {pos[i,0]:.8f} {pos[i,1]:.8f} {pos[i,2]:.8f}"
                           for i in range(nat)]
        control = ("&CONTROL\n"
                   f"  calculation = '{calc}'\n  prefix = '{A.prefix}_{k:02d}'\n"
                   f"  pseudo_dir = '{A.pseudo_dir}'\n  outdir = './tmp_{k:02d}/'\n"
                   "  tprnfor = .true.\n  tstress = .false.\n  verbosity = 'low'\n  disk_io = 'low'\n"
                   + ("  nstep = 150\n  forc_conv_thr = 1.0d-3\n  etot_conv_thr = 1.0d-5\n"
                      if calc == "relax" else "") + "/\n")
        ions = ("&IONS\n  ion_dynamics = 'bfgs'\n/\n" if calc == "relax" else "")
        inp = (control + sysnl + elnl + ions + "\n" + species + "\n\n"
               + kpoints + "\n\n" + cellstr + "\n\n" + "\n".join(plines) + "\n")
        name = f"st_{k:02d}_{Path(sf).stem[:30]}"
        (out / f"{name}.in").write_text(inp)
        print(f"  wrote {name}.in  ({nat} atoms, {sorted(elems)})")

    lp = LAUNCHERS[A.launcher]
    (out / "run_stage2.sh").write_text(lp)
    print(f"\n→ {len(A.structs)} inputs + run_stage2.sh in {out}/")
    print(f"  template elements: {sorted(tmpl_elems)} (must include Li P B S O Cl)")
    print(f"  run: bash {out}/run_stage2.sh  → ranks E/atom (O-on-P vs O-on-B verdict)")


if __name__ == "__main__":
    main()

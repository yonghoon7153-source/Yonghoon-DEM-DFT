#!/usr/bin/env python3
"""b2o3 doped — DFT EOS (Step 5/6). Apples-to-apples with modelC DFT EOS (B0=21.7).

The undoped-system anchor (modelC UMA 22.3 vs DFT 21.7, delta=0.6) does NOT transfer
to the doped system: UMA's B chemistry is shaky (it got O-on-B vs O-on-P wrong by
6 eV), so the doped B0 MUST be measured by DFT, not estimated from the undoped delta.

This wraps the UMA EOS volume grid (v_*.cif from b2o3_eos.py — atoms already
UMA-relaxed at each volume = warm start) into QE DFT relax inputs using modelC's
protocol (ecut 60/480, MV 0.01, conv_thr 1e-8) plus B,O pseudos. Cell FIXED at each
scaled volume, atoms relax. BM3 fit on the DFT (V,E) -> doped DFT B0.

bulk insulating argyrodite -> well-behaved SCF (unlike the Li3N polar slab).

Deps: ase. Usage:
  python3 b2o3_dft_eos.py --eos_dir b2o3_eos --species_template b2o3_6elem_template.in \
      --out b2o3_dft_eos --pseudo_dir /home/ubuntu/pseudo
  bash b2o3_dft_eos/run_dft_eos.sh        # runs all volumes, then BM3-fits -> B0
"""
import argparse, re, glob
from pathlib import Path
from ase.io import read


def grab_card(txt, name):
    out, cap = [], False
    for ln in txt.splitlines():
        if ln.strip().upper().startswith(name):
            cap = True; out.append(ln); continue
        if cap:
            s = ln.strip()
            if s == "" or re.match(r"^[A-Z_]{3,}", s):
                break
            out.append(ln)
    return "\n".join(out)


LAUNCH = r"""#!/bin/bash
set -e; cd "$(dirname "$(realpath "$0")")"
export PATH=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin:$PATH 2>/dev/null
QE=${QE:-pw.x}; MPIRUN=${MPIRUN:-mpirun}
for f in eos_v*.in; do
  o="${f%.in}.out"; [ -f "$o" ] && grep -q "JOB DONE" "$o" && { echo "skip $f"; continue; }
  echo "=== $f $(date +%H:%M) ==="; $MPIRUN --bind-to none -np 1 $QE -inp "$f" > "$o" 2>&1 || echo "  nonzero"
done
echo "=== BM3 fit -> doped DFT B0 ==="
python3 - <<'PY'
import glob,re
from ase.eos import EquationOfState; from ase.units import kJ
VE=[]
for o in sorted(glob.glob("eos_v*.out")):
    t=open(o).read(); m=re.findall(r"!\s+total energy\s+=\s+(-?\d+\.\d+)",t)
    v=re.search(r"unit-cell volume\s*=\s*([\d.]+)",t)
    if m and v: VE.append((float(v.group(1))*0.148184, float(m[-1])*13.605693))  # bohr^3->A^3, Ry->eV
if len(VE)>=4:
    VE.sort(); V=[x[0] for x in VE]; E=[x[1] for x in VE]
    eos=EquationOfState(V,E,eos="birchmurnaghan"); v0,e0,B=eos.fit()
    print(f"  n={len(VE)}  V0={v0:.1f} A3  B0={B/kJ*1e24:.1f} GPa   (modelC DFT 21.7 -> dB0={B/kJ*1e24-21.7:+.1f})")
else: print(f"  only {len(VE)} pts done")
PY
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eos_dir", required=True, help="UMA b2o3_eos output (has v_*.cif grid)")
    ap.add_argument("--species_template", required=True,
                    help="a QE .in whose ATOMIC_SPECIES lists ALL 6 elements (Li P B S O Cl)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--pseudo_dir", default="/home/ubuntu/pseudo")
    ap.add_argument("--ktarget", type=float, default=30.0, help="k*L target (match modelC density)")
    ap.add_argument("--kpoints", default="", help="override auto-k, e.g. '2 2 1' (match modelC exactly)")
    A = ap.parse_args()
    out = Path(A.out); out.mkdir(parents=True, exist_ok=True)
    species = grab_card(Path(A.species_template).read_text(), "ATOMIC_SPECIES")
    tmpl_el = set(re.findall(r"^\s*([A-Z][a-z]?)\s", species, re.M))

    cifs = sorted(glob.glob(f"{A.eos_dir}/v_*.cif"))
    if not cifs:
        raise SystemExit(f"no v_*.cif in {A.eos_dir} — run UMA b2o3_eos.py first")
    print(f"[dft-eos] {len(cifs)} volume points, template species {sorted(tmpl_el)}")
    for cf in cifs:
        a = read(cf); nat = len(a); elems = set(a.get_chemical_symbols())
        if elems - tmpl_el:
            print(f"  ⚠ {cf}: template missing {elems-tmpl_el} pseudos!")
        ntyp = len(elems)
        L = a.cell.lengths()
        if A.kpoints.strip():
            kx, ky, kz = [int(x) for x in A.kpoints.split()]
        else:
            kx, ky, kz = [max(1, round(A.ktarget / x)) for x in L]
        tag = re.search(r"v_(\d+\.\d+)", cf).group(1)
        cell = a.cell.array
        cellstr = "CELL_PARAMETERS angstrom\n" + "\n".join(
            f"  {cell[i,0]:.10f} {cell[i,1]:.10f} {cell[i,2]:.10f}" for i in range(3))
        pos = a.get_positions(); syms = a.get_chemical_symbols()
        plines = ["ATOMIC_POSITIONS angstrom"] + [
            f"  {syms[i]:3s} {pos[i,0]:.8f} {pos[i,1]:.8f} {pos[i,2]:.8f}" for i in range(nat)]
        inp = (f"&CONTROL\n  calculation='relax'\n  prefix='b2o3eos_{tag}'\n"
               f"  pseudo_dir='{A.pseudo_dir}'\n  outdir='./tmp_{tag}/'\n"
               "  tprnfor=.true.\n  tstress=.true.\n  etot_conv_thr=1.0d-6\n  forc_conv_thr=1.0d-4\n"
               "  nstep=200\n  verbosity='low'\n  disk_io='low'\n/\n"
               # modelC protocol (apples-to-apples with B0=21.7): ecut 60/480, MV 0.01
               f"&SYSTEM\n  ibrav=0\n  nat={nat}\n  ntyp={ntyp}\n  ecutwfc=60.0\n  ecutrho=480.0\n"
               "  occupations='smearing'\n  smearing='mv'\n  degauss=0.01\n  nosym=.true.\n/\n"
               "&ELECTRONS\n  conv_thr=1.0d-8\n  mixing_beta=0.3\n  electron_maxstep=200\n/\n"
               "&IONS\n  ion_dynamics='bfgs'\n/\n\n"
               + species + "\n\n"
               + f"K_POINTS automatic\n  {kx} {ky} {kz}  0 0 0\n\n"
               + cellstr + "\n\n" + "\n".join(plines) + "\n")
        (out / f"eos_v{tag}.in").write_text(inp)
        print(f"  eos_v{tag}.in  ({nat} at, {sorted(elems)}, k={kx}x{ky}x{kz}, V={a.get_volume():.1f})")
    (out / "run_dft_eos.sh").write_text(LAUNCH)
    print(f"\n-> {out}/  : (set QE/MPIRUN env) bash run_dft_eos.sh  → BM3 → doped DFT B0 vs 21.7")


if __name__ == "__main__":
    main()

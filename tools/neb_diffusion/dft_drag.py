#!/usr/bin/env python3
"""DFT drag scan for adatom surface diffusion (reference method, Kim & Cui 2023).

Pins the adatom's lateral (x,y) at N points along site_a -> site_b, with the
adatom FULLY fixed (cannot dive), and relaxes the substrate (bottom frozen,
top free) via QE. This reproduces the reference's "eight relative energies =
threshold energies needed to adsorb Li adatom across the diffusion pathway".

Why DFT and not MLIP: UMA-oc20 over-stabilizes Li incorporation into Li3N, so
every MLIP NEB collapses (adatom sinks ~1.5-3.3 eV). DFT does not have this
bias; with the adatom laterally pinned, the substrate relaxes and the barrier
comes out at the reference scale (~0.133 eV for Li3N(001)).

Modes:
  --mode rigid : single-point SCF at each point, whole slab + adatom frozen.
                 Cheap (~N SCF). Gives a rigid-surface upper bound.
  --mode relax : QE relax at each point — adatom fixed, bottom slab fixed,
                 top slab free. Reference-matching (substrate accommodates the
                 adatom at the saddle -> true barrier). Expensive.

Generates N QE inputs + a sequential GPU launcher (nvhpc HPCX env).

Usage:
    python3 dft_drag.py \
        --site_a li3n_toplayer/site_2.xyz \
        --site_b li3n_toplayer/site_8.xyz \
        --template <existing img0.in> \
        --out_dir li3n_dft_drag --n_points 9 --mode relax
    # then:
    bash li3n_dft_drag/run_drag.sh
"""
import argparse
import re
from pathlib import Path
import numpy as np
from ase.io import read


def grab_block(txt, name):
    """Return the namelist text for &name ... / (inclusive)."""
    m = re.search(rf"(&{name}\b.*?\n/\s*\n)", txt, re.S | re.I)
    return m.group(1) if m else ""


def grab_card(txt, name):
    """Return a card (ATOMIC_SPECIES / K_POINTS) header + following lines until
    a blank line or next ALL-CAPS card header."""
    lines = txt.splitlines()
    out, capture = [], False
    for ln in lines:
        if ln.strip().upper().startswith(name):
            capture = True; out.append(ln); continue
        if capture:
            s = ln.strip()
            if s == "" or re.match(r"^[A-Z_]{3,}", s):
                break
            out.append(ln)
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site_a", required=True, help="endpoint A xyz (slab+adatom, with move_mask)")
    ap.add_argument("--site_b", required=True, help="endpoint B xyz (adatom at adjacent site)")
    ap.add_argument("--template", required=True, help="existing QE input for namelists/species/kpoints")
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--n_points", type=int, default=9)
    ap.add_argument("--mode", choices=["rigid", "relax"], default="relax")
    ap.add_argument("--prefix", default="li3n_drag")
    ap.add_argument("--pseudo_dir", default="/data/work/pseudo")
    args = ap.parse_args()

    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    A = read(args.site_a)
    B = read(args.site_b)
    cell = np.array(A.cell)
    syms = A.get_chemical_symbols()
    nat = len(A)
    ad = nat - 1  # adatom = last atom

    # fixed indices from constraints (move_mask F -> fixed). Free = not fixed.
    fixed = set()
    for c in A.constraints:
        if c.__class__.__name__ == "FixAtoms":
            fixed.update(int(i) for i in c.index)
    print(f"[drag] {nat} atoms, adatom idx {ad} ({syms[ad]}), "
          f"{len(fixed)} slab atoms fixed (move_mask), top free")

    posA = A.positions[ad].copy()
    posB = B.positions[ad].copy()
    z_ad = posA[2]
    print(f"[drag] adatom A=({posA[0]:.2f},{posA[1]:.2f}) B=({posB[0]:.2f},{posB[1]:.2f}) "
          f"z={z_ad:.2f}  dist={np.hypot(*(posB[:2]-posA[:2])):.2f} Å")

    tmpl = Path(args.template).read_text()
    species_card = grab_card(tmpl, "ATOMIC_SPECIES")
    kpoints_card = grab_card(tmpl, "K_POINTS")
    sys_nl = grab_block(tmpl, "SYSTEM")
    elec_nl = grab_block(tmpl, "ELECTRONS")

    # pull ecut/etc from template SYSTEM, keep as-is
    calc = "scf" if args.mode == "rigid" else "relax"

    cellstr = "CELL_PARAMETERS angstrom\n" + "\n".join(
        f"  {cell[i,0]:.10f} {cell[i,1]:.10f} {cell[i,2]:.10f}" for i in range(3))

    for k in range(args.n_points):
        t = k / (args.n_points - 1)
        xy = (1 - t) * posA[:2] + t * posB[:2]
        tag = f"p{k}"
        pos = A.positions.copy()
        pos[ad] = [xy[0], xy[1], z_ad]

        # ATOMIC_POSITIONS with per-atom flags
        lines = ["ATOMIC_POSITIONS angstrom"]
        for i in range(nat):
            if i == ad:
                # adatom: xy pinned (drag coordinate), z FREE in relax so it finds
                # its adsorption height at each xy (reference drag method, Kim&Cui).
                # rigid = fully frozen single-point (crude upper bound only).
                fl = "0 0 0" if args.mode == "rigid" else "0 0 1"
            elif args.mode == "rigid":
                fl = "0 0 0"                       # whole slab frozen
            else:
                fl = "0 0 0" if i in fixed else "1 1 1"  # bottom fixed / top free
            lines.append(f"  {syms[i]:3s} {pos[i,0]:.8f} {pos[i,1]:.8f} {pos[i,2]:.8f}  {fl}")
        pos_card = "\n".join(lines)

        control = (
            "&CONTROL\n"
            f"  calculation = '{calc}'\n"
            f"  prefix = '{args.prefix}_{tag}'\n"
            f"  pseudo_dir = '{args.pseudo_dir}'\n"
            f"  outdir = './tmp_{tag}/'\n"
            "  tprnfor = .true.\n  tstress = .false.\n"
            "  verbosity = 'low'\n  disk_io = 'low'\n"
            + ("  nstep = 100\n  forc_conv_thr = 1.0d-3\n  etot_conv_thr = 1.0d-5\n"
               if calc == "relax" else "")
            + "/\n"
        )
        ions = ("&IONS\n  ion_dynamics = 'bfgs'\n"
                "  pot_extrapolation = 'none'\n  wfc_extrapolation = 'none'\n/\n"
                if calc == "relax" else "")

        inp = control + sys_nl + elec_nl + ions + "\n" + species_card + "\n\n" \
              + kpoints_card + "\n\n" + cellstr + "\n\n" + pos_card + "\n"
        (out / f"drag_{tag}.in").write_text(inp)
        print(f"  wrote drag_{tag}.in  adatom xy=({xy[0]:.2f},{xy[1]:.2f})  t={t:.2f}")

    # launcher (nvhpc HPCX GPU env — matches run_dft_neb.sh)
    launcher = f"""#!/bin/bash
set -e
cd "$(dirname "$(realpath "$0")")"
export PATH=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin:/usr/local/bin:/usr/bin:/bin
export LD_LIBRARY_PATH=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64
export OPAL_PREFIX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export OMP_NUM_THREADS=1
export CUDA_VISIBLE_DEVICES=0
export OMPI_ALLOW_RUN_AS_ROOT=1
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
QE=/data/apps/qe-7.4.1-gpu/bin/pw.x
MPIRUN=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin/mpirun
echo "[$(date)] Li3N DFT drag ({args.mode}, {args.n_points} pts)"
for k in $(seq 0 {args.n_points - 1}); do
    INF=drag_p${{k}}.in; OUT=drag_p${{k}}.out
    if [ -f "$OUT" ] && grep -q "JOB DONE" "$OUT" 2>/dev/null; then
        echo "[p$k] DONE"; grep '^!' "$OUT" | tail -1; continue
    fi
    echo "[$(date +%H:%M:%S)] p$k START"
    $MPIRUN -np 1 $QE -in "$INF" > "$OUT" 2>&1 || echo "[p$k] nonzero exit"
    grep -q "JOB DONE" "$OUT" && grep '^!' "$OUT" | tail -1 || {{ echo "[p$k] FAIL"; tail -8 "$OUT"; }}
done
echo "[$(date)] === parse ==="
python3 - <<'PY'
import re, glob, json
E=[]
for k in range({args.n_points}):
    t=open(f"drag_p{{k}}.out").read()
    m=re.findall(r"^!.*total energy\\s*=\\s*(-?\\d+\\.\\d+)\\s*Ry", t, re.M)
    E.append(float(m[-1])*13.605693 if m else None)
if all(e is not None for e in E):
    e0=E[0]; rel=[e-e0 for e in E]
    bar=max(rel)-min(rel[0],rel[-1])
    print(f"{{'pt':>4}} {{'E_rel(eV)':>12}}")
    for k,r in enumerate(rel): print(f"{{k:>4}} {{r-rel[0]:>12.4f}}")
    print(f"\\nbarrier(fwd) = {{rel[max(range(len(rel)),key=lambda i:rel[i])]-rel[0]:.4f}} eV")
    print(f"barrier(max-min) = {{max(rel)-min(rel):.4f}} eV")
    json.dump({{"E_eV":E,"rel_eV":rel,"barrier_eV":max(rel)-min(rel),
               "mode":"{args.mode}","n_points":{args.n_points}}},
              open("drag_result.json","w"),indent=2)
    print("→ drag_result.json")
else:
    print("incomplete:",[i for i,e in enumerate(E) if e is None])
PY
"""
    (out / "run_drag.sh").write_text(launcher)
    print(f"\n[drag] → {out}/drag_p*.in  +  run_drag.sh")
    print(f"[drag] run: bash {out}/run_drag.sh   (mode={args.mode})")


if __name__ == "__main__":
    main()

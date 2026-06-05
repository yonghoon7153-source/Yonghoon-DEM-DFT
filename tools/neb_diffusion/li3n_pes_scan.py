#!/usr/bin/env python3
"""Adatom 2D PES scan on a surface — robust diffusion barrier WITHOUT endpoint guessing.

The 1D drag (dft_drag.py) needs the correct site_a->site_b line; picking it wrong
(as happened for Li3N: archive_wrong_endpoints) gives a meaningless barrier. A 2D PES
scan avoids the guess entirely: relax the adatom (xy PINNED on a grid over the surface
cell, z FREE) with the substrate relaxed, at every grid point. The grid minimum = true
binding site; the lowest saddle connecting adjacent equivalent minima = diffusion barrier.

Per grid point: adatom flag '0 0 1' (xy fixed, z free -> finds adsorption height; xy-pin
prevents lateral incorporation, the UMA failure mode); bottom slab fixed (from structure
constraints), top slab free. DFT relax (QE).

Generates N×N QE relax inputs + launcher + parser.
Deps: ase, numpy. Reuses dft_drag.grab_block/grab_card.

Usage:
  python3 li3n_pes_scan.py \
      --struct li3n_001/li3n_dft_drag_rigid/drag_p0.in \   # any slab+adatom (adatom=last)
      --template li3n_001/li3n_dft_drag_rigid/drag_p0.in \
      --out_dir li3n_001/li3n_pes --grid 5 --supercell_frac 1.0
  bash li3n_001/li3n_pes/run_pes.sh
  python3 li3n_pes_scan.py --parse li3n_001/li3n_pes
"""
import argparse, re, json
from pathlib import Path
import numpy as np
from ase.io import read
from dft_drag import grab_block, grab_card


def gen(args):
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    A = read(args.struct)
    cell = np.array(A.cell); syms = A.get_chemical_symbols(); nat = len(A)
    ad = nat - 1
    z_ad = A.positions[ad, 2]
    # Fix BOTTOM slab layers by z (do NOT inherit the structure's constraints — a
    # rigid drag input has ALL atoms fixed, which would freeze the substrate and
    # defeat the scan). Relax the top relax_top_frac of the slab + the adatom.
    zs = A.positions[:, 2]
    z_slab = np.array([zs[i] for i in range(nat) if i != ad])
    zmin, zmax = z_slab.min(), z_slab.max()
    z_cut = zmin + (1.0 - args.relax_top_frac) * (zmax - zmin)
    fixed = set(i for i in range(nat) if i != ad and zs[i] < z_cut)
    print(f"[pes] {nat} atoms, adatom idx {ad} ({syms[ad]}), z_ad={z_ad:.2f}; "
          f"slab z[{zmin:.2f},{zmax:.2f}] cut={z_cut:.2f} -> {len(fixed)} fixed (bottom) / "
          f"{nat-1-len(fixed)} free (top) + adatom z-free; "
          f"grid {args.grid}×{args.grid} over {args.supercell_frac}× surface cell")

    tmpl = Path(args.template).read_text()
    species = grab_card(tmpl, "ATOMIC_SPECIES")
    kpoints = grab_card(tmpl, "K_POINTS")
    sysnl = grab_block(tmpl, "SYSTEM"); elnl = grab_block(tmpl, "ELECTRONS")
    cellstr = "CELL_PARAMETERS angstrom\n" + "\n".join(
        f"  {cell[i,0]:.10f} {cell[i,1]:.10f} {cell[i,2]:.10f}" for i in range(3))

    a_ip, b_ip = cell[0, :2], cell[1, :2]            # in-plane lattice vectors
    f = args.supercell_frac
    n = 0
    for i in range(args.grid):
        for j in range(args.grid):
            u, v = f * i / args.grid, f * j / args.grid
            xy = u * a_ip + v * b_ip + A.positions[ad, :2] * 0  # origin at cell origin
            tag = f"{i}_{j}"
            pos = A.positions.copy(); pos[ad] = [xy[0], xy[1], z_ad]
            lines = ["ATOMIC_POSITIONS angstrom"]
            for k in range(nat):
                if k == ad:
                    fl = "0 0 1"                       # xy fixed, z free
                else:
                    fl = "0 0 0" if k in fixed else "1 1 1"
                lines.append(f"  {syms[k]:3s} {pos[k,0]:.8f} {pos[k,1]:.8f} {pos[k,2]:.8f}  {fl}")
            control = ("&CONTROL\n  calculation = 'relax'\n"
                       f"  prefix = 'pes_{tag}'\n  pseudo_dir = '{args.pseudo_dir}'\n"
                       f"  outdir = './tmp_{tag}/'\n  tprnfor = .true.\n  tstress = .false.\n"
                       "  verbosity = 'low'\n  disk_io = 'low'\n"
                       "  nstep = 100\n  forc_conv_thr = 1.0d-3\n  etot_conv_thr = 1.0d-5\n/\n")
            ions = ("&IONS\n  ion_dynamics = 'bfgs'\n"
                    "  pot_extrapolation = 'none'\n  wfc_extrapolation = 'none'\n/\n")
            inp = (control + sysnl + elnl + ions + "\n" + species + "\n\n"
                   + kpoints + "\n\n" + cellstr + "\n\n" + "\n".join(lines) + "\n")
            (out / f"pes_{tag}.in").write_text(inp); n += 1

    launcher = """#!/bin/bash
set -e
cd "$(dirname "$(realpath "$0")")"
export PATH=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin:/usr/local/bin:/usr/bin:/bin
export LD_LIBRARY_PATH=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/lib:/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib:/usr/local/cuda-12.6/lib64
export OPAL_PREFIX=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi
export OMP_NUM_THREADS=1 CUDA_VISIBLE_DEVICES=0 OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
QE=/data/apps/qe-7.4.1-gpu/bin/pw.x
MPIRUN=/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi/bin/mpirun
for f in pes_*.in; do
    o="${f%.in}.out"
    [ -f "$o" ] && grep -q "JOB DONE" "$o" && { echo "skip $f"; continue; }
    echo "=== $f ==="; $MPIRUN --bind-to none -np 1 $QE -inp "$f" > "$o" 2>&1 || echo "  nonzero exit"
done
echo "ALL PES DONE — parse: python3 li3n_pes_scan.py --parse ."
"""
    (out / "run_pes.sh").write_text(launcher)
    print(f"[pes] wrote {n} inputs + run_pes.sh -> {out}")


def parse(d):
    d = Path(d)
    grid = {}
    for o in d.glob("pes_*.out"):
        m = re.match(r"pes_(\d+)_(\d+)", o.stem)
        if not m:
            continue
        txt = o.read_text()
        es = re.findall(r"!\s+total energy\s+=\s+(-?\d+\.\d+)", txt)
        if es:
            grid[(int(m.group(1)), int(m.group(2)))] = float(es[-1]) * 13.605693  # Ry->eV
    if not grid:
        print("no finished pes_*.out"); return
    e0 = min(grid.values())
    n = max(max(k) for k in grid) + 1
    print(f"PES {len(grid)}/{n*n} done. E range {max(grid.values())-e0:.3f} eV above min.")
    print("rel-E grid (eV; '.'=missing):")
    for i in range(n):
        row = []
        for j in range(n):
            row.append(f"{grid[(i,j)]-e0:5.2f}" if (i, j) in grid else "  .  ")
        print("  " + " ".join(row))
    mins = sorted(grid.items(), key=lambda kv: kv[1])[:3]
    print("lowest sites:", [(k, round(v-e0, 3)) for k, v in mins])
    print("→ binding site = grid min; barrier ≈ lowest saddle between adjacent equivalent minima")
    json.dump({f"{i}_{j}": grid[(i, j)] for (i, j) in grid},
              open(d / "pes_energies.json", "w"), indent=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--parse", help="parse a finished PES dir and exit")
    ap.add_argument("--struct"); ap.add_argument("--template")
    ap.add_argument("--out_dir"); ap.add_argument("--grid", type=int, default=5)
    ap.add_argument("--supercell_frac", type=float, default=1.0,
                    help="fraction of surface cell to span (1.0 = one full cell)")
    ap.add_argument("--relax_top_frac", type=float, default=0.5,
                    help="top fraction of slab thickness to relax (rest fixed by z)")
    ap.add_argument("--pseudo_dir", default="/data/work/pseudo")
    a = ap.parse_args()
    if a.parse:
        parse(a.parse)
    else:
        assert a.struct and a.template and a.out_dir, "need --struct --template --out_dir"
        gen(a)


if __name__ == "__main__":
    main()

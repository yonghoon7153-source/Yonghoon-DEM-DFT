#!/usr/bin/env python3
"""Build 12 strain SCFs for stress-strain full Cij.

Strain pattern (6 Voigt directions × ±h amplitude):
    k=1: ε_xx → F = I, F[0,0] = 1±h
    k=2: ε_yy → F = I, F[1,1] = 1±h
    k=3: ε_zz → F = I, F[2,2] = 1±h
    k=4: ε_yz → F = I, F[1,2] = F[2,1] = ±h/2  (tensor, γ_yz=h)
    k=5: ε_xz → F = I, F[0,2] = F[2,0] = ±h/2
    k=6: ε_xy → F = I, F[0,1] = F[1,0] = ±h/2

Cell vectors transform a' = F @ a. Atomic positions in crystal coords stay
identical (clamped-ion: no per-strain relaxation). Each SCF prints stress
tensor → 12 SCFs give all 6 columns of Cij directly.

Companion to tools/modelc_v3/fit_elastic_cij_stress.py (the fitter).

Usage:
    python3 build_elastic_strain_inputs.py \\
        --src_in   V0_relax.in \\
        --src_out  V0_relax.out \\
        --workdir  elastic_static \\
        --strain   0.005 \\
        --prefix_base strain
"""
import argparse
import re
from pathlib import Path
import numpy as np


def parse_namelists_and_cards(in_text):
    nls, cards = {}, {}
    cur, buf = None, []
    for line in in_text.splitlines():
        s = line.strip()
        if s.startswith("&"):
            cur = ("nl", s[1:].split()[0].upper()); buf = [line]
        elif s == "/" and cur and cur[0] == "nl":
            buf.append(line); nls[cur[1]] = "\n".join(buf); cur, buf = None, []
        elif s and s.split()[0] in {
                "ATOMIC_SPECIES", "K_POINTS", "CELL_PARAMETERS",
                "ATOMIC_POSITIONS", "OCCUPATIONS", "HUBBARD"}:
            if cur and cur[0] == "card":
                cards[cur[1]] = "\n".join(buf)
            cur = ("card", s.split()[0]); buf = [line]
        elif cur:
            buf.append(line)
    if cur and cur[0] == "card":
        cards[cur[1]] = "\n".join(buf)
    return nls, cards


def parse_cell_from_in(text):
    m = re.search(
        r"CELL_PARAMETERS\s*(?:\(?\s*(angstrom|bohr|alat)\s*\)?)?\s*\n"
        r"((?:[-+\d.eE\s]+\n){3})", text, re.IGNORECASE)
    if not m:
        return None, None
    unit = (m.group(1) or "alat").lower()
    rows = [[float(x) for x in line.split()[:3]]
            for line in m.group(2).strip().splitlines()[:3]]
    return np.array(rows), unit


def parse_final_positions(out_text):
    matches = list(re.finditer(
        r"ATOMIC_POSITIONS\s*\(([^)]+)\)\n((?:[A-Za-z]\w*\s+[-+\d.eE\s]+\n)+)",
        out_text))
    if not matches:
        return None, None
    m = matches[-1]
    return m.group(1).strip(), m.group(2)


def deformation_matrix(k, h):
    """k in 1..6, h is strain amplitude. Returns 3x3 F = I + ε."""
    F = np.eye(3)
    if k == 1:
        F[0, 0] = 1.0 + h
    elif k == 2:
        F[1, 1] = 1.0 + h
    elif k == 3:
        F[2, 2] = 1.0 + h
    elif k == 4:
        F[1, 2] = F[2, 1] = h / 2.0
    elif k == 5:
        F[0, 2] = F[2, 0] = h / 2.0
    elif k == 6:
        F[0, 1] = F[1, 0] = h / 2.0
    else:
        raise ValueError(f"k must be 1..6, got {k}")
    return F


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src_in", required=True,
                    help="V0_relax.in (provides &CONTROL, &SYSTEM, pseudo, cell)")
    ap.add_argument("--src_out", required=True,
                    help="V0_relax.out (provides relaxed ATOMIC_POSITIONS)")
    ap.add_argument("--workdir", required=True,
                    help="output dir for 12 strain_*.in files")
    ap.add_argument("--strain", type=float, default=0.005)
    ap.add_argument("--prefix_base", default="strain")
    ap.add_argument("--kpoints", default="2 2 1 0 0 0")
    args = ap.parse_args()

    wd = Path(args.workdir); wd.mkdir(parents=True, exist_ok=True)
    in_text = Path(args.src_in).read_text()
    out_text = Path(args.src_out).read_text()

    nls, cards = parse_namelists_and_cards(in_text)
    cell, cell_unit = parse_cell_from_in(in_text)
    if cell is None or cell_unit != "angstrom":
        raise SystemExit(
            f"Expected CELL_PARAMETERS angstrom in src_in, got unit={cell_unit}")
    pos_unit, pos_block = parse_final_positions(out_text)
    if pos_block is None:
        raise SystemExit("Could not parse final ATOMIC_POSITIONS from src_out")
    if not pos_unit.lower().startswith("crystal"):
        raise SystemExit(
            f"Need ATOMIC_POSITIONS in crystal coords; got {pos_unit}. "
            f"(Crystal coords stay fixed under cell strain.)")

    print(f"Source cell V = {abs(np.linalg.det(cell)):.4f} Å³")
    print(f"Strain magnitude h = {args.strain}")
    print(f"Position unit = {pos_unit}  (crystal — invariant)")
    print(f"Writing 12 SCFs to {wd}")

    h = args.strain
    species = cards.get("ATOMIC_SPECIES", "")
    hubbard = cards.get("HUBBARD", "")
    kpts = f"K_POINTS automatic\n  {args.kpoints}\n"
    new_pos = f"ATOMIC_POSITIONS ({pos_unit})\n{pos_block}"

    for k in range(1, 7):
        for sign_label, sign in [("p", +1), ("m", -1)]:
            F = deformation_matrix(k, sign * h)
            new_cell = F @ cell
            tag = f"{args.prefix_base}_{k}{sign_label}"
            # &CONTROL: SCF + force + stress
            control = nls["CONTROL"]
            control = re.sub(r"calculation\s*=\s*'[^']*'",
                             "calculation='scf'", control)
            control = re.sub(r"prefix\s*=\s*'[^']*'",
                             f"prefix='{tag}'", control)
            control = re.sub(r"outdir\s*=\s*'[^']*'",
                             f"outdir='./tmp_{tag}/'", control)
            control = re.sub(r"\n\s*restart_mode\s*=\s*'[^']*'", "", control)
            # ensure tprnfor + tstress
            if "tprnfor" not in control:
                control = re.sub(r"\n\s*/\s*$",
                                 "\n  tprnfor=.true.\n  tstress=.true.\n/",
                                 control)

            system = nls["SYSTEM"]
            electrons = nls.get(
                "ELECTRONS", "&ELECTRONS\n  conv_thr=1.0d-9\n/")

            cell_lines = ["CELL_PARAMETERS angstrom"]
            for row in new_cell:
                cell_lines.append(
                    "  " + "  ".join(f"{x:14.10f}" for x in row))
            cell_card = "\n".join(cell_lines) + "\n"

            full_in = (
                control + "\n" +
                system + "\n" +
                electrons + "\n" +
                species + "\n" +
                kpts + "\n" +
                cell_card + "\n" +
                new_pos + "\n" +
                (hubbard if hubbard else "")
            )
            out_file = wd / f"{tag}.in"
            out_file.write_text(full_in)
            V_str = abs(np.linalg.det(new_cell))
            print(f"  {tag}: V={V_str:.4f} Å³  (det F={np.linalg.det(F):.6f})")

    # Sequential runner
    runner = wd / "run_elastic.sh"
    runner.write_text(f"""#!/bin/bash
# Sequential stress-strain SCF runner — 12 jobs, ε = ±{h}
set -e
cd $(dirname $(realpath $0))
export OMP_NUM_THREADS=8

for k in 1 2 3 4 5 6; do
    for s in p m; do
        tag={args.prefix_base}_${{k}}${{s}}
        if [ -f ${{tag}}.out ] && grep -q "JOB DONE" ${{tag}}.out; then
            echo "[$(date +%H:%M:%S)] $tag: already done"
            continue
        fi
        echo "[$(date +%H:%M:%S)] $tag: START"
        T0=$(date +%s)
        mpirun --bind-to none -np 1 pw.x -inp ${{tag}}.in > ${{tag}}.out 2>&1 \\
            || echo "  pw.x non-zero exit"
        DT=$(( $(date +%s) - T0 ))
        if grep -q "JOB DONE" ${{tag}}.out; then
            echo "  ✓ DONE in ${{DT}}s"
        else
            echo "  ✗ FAILED in ${{DT}}s"; tail -10 ${{tag}}.out
        fi
    done
done

echo ""
echo "=== ALL 12 DONE. Now fit:"
echo "python3 /home/ubuntu/work/Yonghoon-DEM-DFT/tools/modelc_v3/fit_elastic_cij_stress.py \\\\"
echo "    --workdir . --strain {h}"
""")
    runner.chmod(0o755)
    print(f"\n→ runner: {runner}")
    print(f"→ run with: bash {runner}")


if __name__ == "__main__":
    main()

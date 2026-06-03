#!/usr/bin/env python3
"""Build BM-EOS volume-sweep inputs for modelC_v3.

Generates N volume points around a center volume V0 (from V0_relax.out),
each as a cell-frozen relax input (atoms move freely, cell fixed at
scaled value).

For each volume point:
  - cell vectors scaled by (V_target/V0)**(1/3)
  - atomic positions in crystal coords (invariant under cell scale)
  - calculation='relax', cell_dofree='none' (fixed cell)
  - same PAW pseudo + nosym + tetrahedra as the original

Usage:
    python3 build_bm_eos_inputs.py \\
        --v0_in /home/.../V0_relax.in \\
        --v0_out /home/.../V0_relax.out \\
        --out_dir /home/.../bm_eos \\
        --n_points 7 --v_min 0.97 --v_max 1.03
"""
import argparse
import re
from pathlib import Path
import numpy as np


def parse_namelists_and_cards(in_text):
    nls = {}; cards = {}
    cur = None; cur_lines = []
    for line in in_text.splitlines():
        s = line.strip()
        if s.startswith("&"):
            cur = ("nl", s[1:].split()[0].upper()); cur_lines = [line]
        elif s == "/" and cur and cur[0] == "nl":
            cur_lines.append(line)
            nls[cur[1]] = "\n".join(cur_lines)
            cur = None; cur_lines = []
        elif s.split(maxsplit=1) and s.split()[0] in {
                "ATOMIC_SPECIES", "K_POINTS", "CELL_PARAMETERS",
                "ATOMIC_POSITIONS", "OCCUPATIONS", "HUBBARD"}:
            if cur and cur[0] == "card":
                cards[cur[1]] = "\n".join(cur_lines)
            cur = ("card", s.split()[0]); cur_lines = [line]
        elif cur:
            cur_lines.append(line)
    if cur and cur[0] == "card":
        cards[cur[1]] = "\n".join(cur_lines)
    return nls, cards


def parse_cell_from_in(text):
    m = re.search(
        r"CELL_PARAMETERS\s*(?:\(?\s*(angstrom|bohr|alat)\s*\)?)?\s*\n"
        r"((?:[-+\d.E\s]+\n){3})", text, re.IGNORECASE)
    if not m:
        return None, None
    unit = (m.group(1) or "alat").lower()
    rows = [[float(x) for x in line.split()[:3]]
            for line in m.group(2).strip().splitlines()[:3]]
    return np.array(rows), unit


def parse_final_positions(out_text):
    matches = list(re.finditer(
        r"ATOMIC_POSITIONS\s*\(([^)]+)\)\n((?:[A-Za-z]\w*\s+[-+\d.E\s]+\n)+)",
        out_text))
    if not matches:
        return None
    m = matches[-1]
    return f"ATOMIC_POSITIONS ({m.group(1).strip()})\n{m.group(2)}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--v0_in", required=True)
    ap.add_argument("--v0_out", required=True)
    ap.add_argument("--out_dir", required=True)
    ap.add_argument("--n_points", type=int, default=7)
    ap.add_argument("--v_min", type=float, default=0.97,
                    help="lowest fractional volume (relative to V0)")
    ap.add_argument("--v_max", type=float, default=1.03)
    ap.add_argument("--prefix_base", default="modelC_v3_eos")
    args = ap.parse_args()

    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    in_text = Path(args.v0_in).read_text()
    out_text = Path(args.v0_out).read_text()

    nls, cards = parse_namelists_and_cards(in_text)
    # Cell from input (fixed-cell relax case — V0 cell is the original)
    cell, unit = parse_cell_from_in(in_text)
    if cell is None:
        raise SystemExit("Could not parse CELL_PARAMETERS from V0_relax.in")
    # Final positions from output (BFGS-relaxed coords at V0)
    pos_block = parse_final_positions(out_text)
    if pos_block is None:
        raise SystemExit("Could not parse final ATOMIC_POSITIONS from V0_relax.out")

    V0 = abs(np.linalg.det(cell))
    print(f"V0_cell = {V0:.4f} (in unit '{unit}')")

    fractions = np.linspace(args.v_min, args.v_max, args.n_points)
    print(f"Volume fractions: {fractions}")

    for i, f in enumerate(fractions):
        scale = f ** (1.0 / 3.0)
        new_cell = cell * scale

        # Build new CONTROL
        control = nls["CONTROL"]
        # calculation = 'relax' (cell stays fixed via &CELL+cell_dofree='none')
        control = re.sub(r"calculation\s*=\s*'[^']*'",
                          "calculation = 'relax'", control)
        # prefix + outdir per volume point
        new_prefix = f"{args.prefix_base}_v{i:02d}"
        control = re.sub(r"prefix\s*=\s*'[^']*'",
                          f"prefix = '{new_prefix}'", control)
        control = re.sub(r"outdir\s*=\s*'[^']*'",
                          f"outdir = './tmp_{new_prefix}/'", control)
        # remove restart_mode if any
        control = re.sub(r"\n\s*restart_mode\s*=\s*'[^']*'", "", control)

        # SYSTEM (no changes needed)
        system = nls["SYSTEM"]

        # ELECTRONS (no changes needed)
        electrons = nls.get("ELECTRONS",
                             "&ELECTRONS\n  conv_thr = 1.0d-8\n/")

        # &IONS + &CELL (fixed cell)
        ions = nls.get("IONS", "&IONS\n  ion_dynamics = 'bfgs'\n/")
        cell_nl = "&CELL\n  cell_dofree = 'none'\n/"

        # ATOMIC_SPECIES
        atomic_species = cards.get("ATOMIC_SPECIES", "")
        # HUBBARD if present
        hubbard = cards.get("HUBBARD", "")
        # K_POINTS
        kpoints = cards.get("K_POINTS", "K_POINTS automatic\n  2 2 1 0 0 0\n")

        # Build CELL_PARAMETERS card with scaled cell
        cell_card_lines = ["CELL_PARAMETERS angstrom"]
        for row in new_cell:
            cell_card_lines.append(
                "  " + "  ".join(f"{x:14.10f}" for x in row))
        cell_card = "\n".join(cell_card_lines) + "\n"

        # Assemble
        full_in = (
            control + "\n" +
            system + "\n" +
            electrons + "\n" +
            ions + "\n" +
            cell_nl + "\n" +
            atomic_species + "\n" +
            kpoints + "\n" +
            cell_card + "\n" +
            pos_block + "\n" +
            (hubbard if hubbard else "")
        )
        out_file = out_dir / f"v{i:02d}.in"
        out_file.write_text(full_in)
        V_scaled = V0 * f
        print(f"  v{i:02d}: f={f:.3f}  V={V_scaled:.4f}  → {out_file}")

    # Write a runner
    runner = out_dir / "run_bm_eos.sh"
    runner.write_text(f"""#!/bin/bash
# Sequential BM-EOS runner: relax atoms at each of {args.n_points} volume points.
set -e
cd $(dirname $(realpath $0))
export OMP_NUM_THREADS=8

for i in $(seq -f "%02g" 0 {args.n_points - 1}); do
    if [ -f v${{i}}.out ] && grep -qE "bfgs converged|End of BFGS" v${{i}}.out; then
        echo "[$(date +%H:%M:%S)] v${{i}}: already done"
        grep '^!' v${{i}}.out | tail -1
        continue
    fi
    echo "[$(date +%H:%M:%S)] v${{i}}: START"
    T0=$(date +%s)
    mpirun --bind-to none -np 1 pw.x -inp v${{i}}.in > v${{i}}.out 2>&1 || \\
        echo "  pw.x non-zero exit"
    DT=$(( $(date +%s) - T0 ))
    if grep -qE "bfgs converged|End of BFGS" v${{i}}.out; then
        echo "  ✓ DONE in ${{DT}}s"; grep '^!' v${{i}}.out | tail -1
    else
        echo "  ✗ FAILED in ${{DT}}s"; tail -10 v${{i}}.out
    fi
done

echo ""
echo "=== ALL DONE. Now run: python3 fit_bm_eos.py --dir . ==="
""")
    runner.chmod(0o755)
    print(f"\n→ runner: {runner}")


if __name__ == "__main__":
    main()

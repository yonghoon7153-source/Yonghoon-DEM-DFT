#!/usr/bin/env python3
"""Build comp1_v3 V0_relax input at the BM-EOS V0 cell.

Source coords: closest EOS point output (e.g. comp1_r2_v102.out — DFT-relaxed
atomic positions at fixed cell V_v102 ≈ V0).

Target cell: cubic a from BM-EOS V0 (default V0 = 1016.62 Å³ → a = 10.0547 Å).

Output: cell-fixed relax input (calculation='relax', cell_dofree='none').

Usage:
    python3 build_v0_relax_input.py \\
        --src_in  comp1_r2_v102.in \\
        --src_out comp1_r2_v102.out \\
        --v0_a3   1016.62 \\
        --prefix  comp1_v3_V0 \\
        --out     comp1_v3_V0_relax.in
"""
import argparse
import re
from pathlib import Path
import numpy as np


BOHR_TO_A = 0.5291772108


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
    """Return the LAST ATOMIC_POSITIONS block from QE output."""
    matches = list(re.finditer(
        r"ATOMIC_POSITIONS\s*\(([^)]+)\)\n((?:[A-Za-z]\w*\s+[-+\d.eE\s]+\n)+)",
        out_text))
    if not matches:
        return None, None
    m = matches[-1]
    unit = m.group(1).strip()
    return unit, m.group(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src_in", required=True,
                    help="closest EOS-point input (.in) to copy &CONTROL etc")
    ap.add_argument("--src_out", required=True,
                    help="closest EOS-point output (.out) with relaxed coords")
    ap.add_argument("--v0_a3", type=float, default=1016.62,
                    help="target V0 in Å³ (default from comp1_v3 BM-EOS)")
    ap.add_argument("--prefix", default="comp1_v3_V0")
    ap.add_argument("--out", default="comp1_v3_V0_relax.in")
    ap.add_argument("--kpoints", default="2 2 1 0 0 0")
    args = ap.parse_args()

    in_text = Path(args.src_in).read_text()
    out_text = Path(args.src_out).read_text()

    nls, cards = parse_namelists_and_cards(in_text)
    cell_src, unit = parse_cell_from_in(in_text)
    if cell_src is None:
        raise SystemExit("Could not parse CELL_PARAMETERS from src_in")
    if unit != "angstrom":
        raise SystemExit(f"Expected CELL_PARAMETERS angstrom, got {unit}")

    V_src = abs(np.linalg.det(cell_src))
    pos_unit, pos_block = parse_final_positions(out_text)
    if pos_block is None:
        raise SystemExit("Could not parse final ATOMIC_POSITIONS from src_out")

    # Scale factor: cell × scale, V × scale³ = V0
    scale = (args.v0_a3 / V_src) ** (1.0 / 3.0)
    new_cell = cell_src * scale
    V_check = abs(np.linalg.det(new_cell))
    print(f"Source cell V = {V_src:.4f} Å³")
    print(f"Target V0     = {args.v0_a3:.4f} Å³")
    print(f"Scale factor  = {scale:.6f}  (cell × scale)")
    print(f"New cell V    = {V_check:.4f} Å³  (sanity check)")

    # Rebuild ATOMIC_POSITIONS — if cartesian (angstrom/bohr), scale them too.
    # If crystal, leave as-is (fractional coords are scale-invariant).
    pos_unit_low = pos_unit.lower()
    if pos_unit_low.startswith("crystal"):
        new_pos_block = f"ATOMIC_POSITIONS ({pos_unit})\n{pos_block}"
        print(f"Position unit: {pos_unit} → kept fractional (scale-invariant)")
    elif pos_unit_low.startswith("angstrom") or pos_unit_low.startswith("bohr"):
        # Scale cartesian coords by same factor as cell
        new_lines = []
        for line in pos_block.strip().splitlines():
            parts = line.split()
            sp = parts[0]
            xyz = np.array([float(p) for p in parts[1:4]]) * scale
            new_lines.append(f"  {sp:4s}  {xyz[0]:14.10f}  "
                             f"{xyz[1]:14.10f}  {xyz[2]:14.10f}")
        new_pos_block = (f"ATOMIC_POSITIONS ({pos_unit})\n"
                         + "\n".join(new_lines) + "\n")
        print(f"Position unit: {pos_unit} → cartesian scaled by × {scale:.6f}")
    else:
        raise SystemExit(f"Unsupported ATOMIC_POSITIONS unit: {pos_unit}")

    # &CONTROL — relax, new prefix, fresh outdir, drop restart_mode
    control = nls["CONTROL"]
    control = re.sub(r"calculation\s*=\s*'[^']*'",
                     "calculation='relax'", control)
    control = re.sub(r"prefix\s*=\s*'[^']*'",
                     f"prefix='{args.prefix}'", control)
    control = re.sub(r"outdir\s*=\s*'[^']*'",
                     f"outdir='./tmp_{args.prefix}/'", control)
    control = re.sub(r"\n\s*restart_mode\s*=\s*'[^']*'", "", control)
    # tighten conv thresholds for V0 reference
    if "etot_conv_thr" not in control:
        control = re.sub(r"\n\s*/\s*$",
                         "\n  etot_conv_thr=1.0d-6\n  forc_conv_thr=1.0d-4\n/",
                         control)

    system   = nls["SYSTEM"]
    electrons = nls.get("ELECTRONS", "&ELECTRONS\n  conv_thr=1.0d-9\n/")
    ions     = nls.get("IONS", "&IONS\n  ion_dynamics='bfgs'\n/")
    cell_nl  = "&CELL\n  cell_dofree='none'\n/"

    atomic_species = cards.get("ATOMIC_SPECIES", "")
    hubbard = cards.get("HUBBARD", "")
    kpoints = f"K_POINTS automatic\n  {args.kpoints}\n"

    cell_lines = ["CELL_PARAMETERS angstrom"]
    for row in new_cell:
        cell_lines.append("  " + "  ".join(f"{x:14.10f}" for x in row))
    cell_card = "\n".join(cell_lines) + "\n"

    full_in = (
        control + "\n" +
        system + "\n" +
        electrons + "\n" +
        ions + "\n" +
        cell_nl + "\n" +
        atomic_species + "\n" +
        kpoints + "\n" +
        cell_card + "\n" +
        new_pos_block + "\n" +
        (hubbard if hubbard else "")
    )
    Path(args.out).write_text(full_in)
    print(f"\n→ wrote {args.out}")
    print(f"   Run: mpirun -np 1 pw.x -inp {args.out} > "
          f"{Path(args.out).stem}.out 2>&1")


if __name__ == "__main__":
    main()

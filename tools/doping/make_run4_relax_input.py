#!/usr/bin/env python3
"""Build a clean run4 relax input from the final coords of run3.out.

For nd_doped_modelc V0 DFT relax that timed out at fmax 0.009 Ry/Bohr due
to BFGS oscillation between FM/AFM Nd 4f orbital orderings. Strategy:

  1. Extract final ATOMIC_POSITIONS from run3.out
  2. Build run4_relax.in with:
     - starting_magnetization on Nd atoms FIXED (AFM by default)
     - ion_dynamics = 'damp'  (BFGS oscillation kill)
     - forc_conv_thr = 1.0d-4 (paper-grade)
     - restart_mode = 'from_scratch' (fresh wfc, new outdir)
     - mixing_beta = 0.2 (Nd-stable)
  3. (Optional) build a parallel FM-locked test input to verify GS

Usage:
    python3 make_run4_relax_input.py \\
        --run3_in   run3.in \\
        --run3_out  run3.out \\
        --out_dir   . \\
        --nd_indices 1 2     # Nd atom indices in atomic-species type list

The script does NOT submit — it just writes inputs. User then submits via
sbatch_run4.sh (also written by this script if --write_sbatch is given).
"""
import argparse
import re
from pathlib import Path


def parse_namelists_and_cards(in_text):
    """Returns ({nl_name: text}, {card_name: text}) preserving original formatting."""
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


def extract_final_positions(out_text):
    """Last ATOMIC_POSITIONS block from QE relax output."""
    matches = list(re.finditer(
        r"ATOMIC_POSITIONS\s*\(([^)]+)\)\n((?:[A-Za-z]\w*\s+[-+\d.E\s]+\n)+)",
        out_text))
    if not matches:
        raise SystemExit("no ATOMIC_POSITIONS found in run3.out")
    m = matches[-1]
    units = m.group(1).strip()
    return f"ATOMIC_POSITIONS ({units})\n{m.group(2)}", units


def modify_control(control_text, args):
    """Patch &CONTROL: restart_mode, forc_conv_thr, etot_conv_thr, outdir, nstep."""
    txt = control_text
    # restart_mode = 'from_scratch'
    if "restart_mode" in txt:
        txt = re.sub(r"restart_mode\s*=\s*'[^']*'",
                      "restart_mode = 'from_scratch'", txt)
    else:
        txt = re.sub(r"(\n\s*/\s*)$",
                      r"\n  restart_mode = 'from_scratch'\1", txt)
    # forc_conv_thr
    if "forc_conv_thr" in txt:
        txt = re.sub(r"forc_conv_thr\s*=\s*[-+\d.dDeE]+",
                      f"forc_conv_thr = {args.fmax_target:.1e}".replace("e-0", "d-0"), txt)
    else:
        txt = re.sub(r"(\n\s*/\s*)$",
                      f"\n  forc_conv_thr = {args.fmax_target:.1e}\\1".replace("e-0", "d-0"), txt)
    # etot_conv_thr
    if "etot_conv_thr" in txt:
        txt = re.sub(r"etot_conv_thr\s*=\s*[-+\d.dDeE]+",
                      f"etot_conv_thr = {args.etot_target:.1e}".replace("e-0", "d-0"), txt)
    # outdir
    txt = re.sub(r"outdir\s*=\s*'[^']+'",
                  f"outdir = '{args.outdir}'", txt)
    # nstep
    if "nstep" in txt:
        txt = re.sub(r"nstep\s*=\s*\d+", f"nstep = {args.nstep}", txt)
    return txt


def modify_system(system_text, nd_indices, mag_mode, mag_amplitude):
    """Replace or insert starting_magnetization for Nd atom types.

    nd_indices: list of type indices (ntyp ordering) e.g. [3] if Nd is type 3
                in ATOMIC_SPECIES.
    mag_mode: 'AFM' (alternating ±) or 'FM' (all +) or 'NONE' (no insert)
    """
    txt = system_text
    # Remove existing starting_magnetization lines
    txt = re.sub(r"\n\s*starting_magnetization\([^)]+\)\s*=\s*[-+\d.E]+", "", txt)
    if mag_mode == "NONE":
        return txt
    new_lines = []
    sign = 1
    for i, ind in enumerate(nd_indices):
        m = mag_amplitude * sign
        new_lines.append(f"  starting_magnetization({ind}) = {m:+.2f}")
        if mag_mode == "AFM":
            sign *= -1
        # FM: keep sign = +1 (all positive)
    insert = "\n".join(new_lines)
    txt = re.sub(r"(\n\s*/\s*)$", f"\n{insert}\\1", txt)
    return txt


def modify_electrons(electrons_text, mixing_beta, electron_maxstep, conv_thr):
    txt = electrons_text
    txt = re.sub(r"mixing_beta\s*=\s*[-+\d.E]+", f"mixing_beta = {mixing_beta}", txt)
    txt = re.sub(r"electron_maxstep\s*=\s*\d+", f"electron_maxstep = {electron_maxstep}", txt)
    txt = re.sub(r"conv_thr\s*=\s*[-+\d.dDeE]+",
                  f"conv_thr = {conv_thr:.1e}".replace("e-0", "d-0"), txt)
    return txt


def make_or_replace_ions(text_in, ion_dynamics):
    """Build &IONS namelist if missing, or update existing."""
    if "&IONS" in text_in:
        # Replace ion_dynamics within existing &IONS
        return re.sub(
            r"&IONS([\s\S]*?)/\s*",
            lambda m: re.sub(r"ion_dynamics\s*=\s*'[^']*'",
                              f"ion_dynamics = '{ion_dynamics}'",
                              m.group(0)) if "ion_dynamics" in m.group(0)
                       else m.group(0).replace("/", f"  ion_dynamics = '{ion_dynamics}'\n/"),
            text_in
        )
    # No existing &IONS — caller must include it via assembly
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run3_in", required=True)
    ap.add_argument("--run3_out", required=True)
    ap.add_argument("--out_dir", default=".")
    ap.add_argument("--nd_indices", type=int, nargs="+", required=True,
                    help="Nd atom type indices (per ATOMIC_SPECIES order, 1-based)")
    ap.add_argument("--mag_mode", choices=["AFM", "FM", "NONE"], default="AFM")
    ap.add_argument("--mag_amplitude", type=float, default=0.6)
    ap.add_argument("--fmax_target", type=float, default=1e-4,
                    help="Ry/Bohr")
    ap.add_argument("--etot_target", type=float, default=1e-5)
    ap.add_argument("--outdir_suffix", default="_run4_AFM")
    ap.add_argument("--nstep", type=int, default=80)
    ap.add_argument("--mixing_beta", type=float, default=0.2)
    ap.add_argument("--electron_maxstep", type=int, default=500)
    ap.add_argument("--conv_thr", type=float, default=1e-10)
    ap.add_argument("--ion_dynamics", default="damp")
    args = ap.parse_args()
    args.outdir = f"./tmp{args.outdir_suffix}/"

    in_text = Path(args.run3_in).read_text()
    out_text = Path(args.run3_out).read_text()

    nls, cards = parse_namelists_and_cards(in_text)
    pos_block, units = extract_final_positions(out_text)

    # Build modified namelists
    new_control = modify_control(nls["CONTROL"], args)
    new_system = modify_system(nls["SYSTEM"], args.nd_indices,
                                 args.mag_mode, args.mag_amplitude)
    new_electrons = modify_electrons(
        nls.get("ELECTRONS",
                "&ELECTRONS\n  conv_thr = 1.0d-10\n  mixing_beta = 0.3\n  electron_maxstep = 200\n/"),
        args.mixing_beta, args.electron_maxstep, args.conv_thr)
    # &IONS
    if "IONS" in nls:
        new_ions = re.sub(r"ion_dynamics\s*=\s*'[^']*'",
                           f"ion_dynamics = '{args.ion_dynamics}'", nls["IONS"])
        if "ion_dynamics" not in nls["IONS"]:
            new_ions = nls["IONS"].replace("/", f"  ion_dynamics = '{args.ion_dynamics}'\n/")
    else:
        new_ions = (f"&IONS\n"
                     f"  ion_dynamics = '{args.ion_dynamics}'\n"
                     f"  upscale = 100\n/")

    # Assemble (cards order: ATOMIC_SPECIES, K_POINTS, CELL_PARAMETERS, ATOMIC_POSITIONS)
    parts = [new_control, new_system, new_electrons, new_ions]
    for card_key in ("ATOMIC_SPECIES", "K_POINTS", "CELL_PARAMETERS"):
        if card_key in cards:
            parts.append(cards[card_key])
    parts.append(pos_block)
    if "HUBBARD" in cards:
        parts.append(cards["HUBBARD"])
    if "OCCUPATIONS" in cards:
        parts.append(cards["OCCUPATIONS"])

    text = "\n".join(parts) + "\n"
    out_in = Path(args.out_dir) / f"run4_relax{args.outdir_suffix}.in"
    out_in.write_text(text)
    print(f"→ {out_in}")
    print(f"\n  starting_magnetization mode: {args.mag_mode}  on Nd types {args.nd_indices}")
    print(f"  ion_dynamics = '{args.ion_dynamics}'")
    print(f"  forc_conv_thr = {args.fmax_target:.0e}")
    print(f"  outdir = {args.outdir}")
    print(f"  positions taken from {args.run3_out} (units: {units})")


if __name__ == "__main__":
    main()

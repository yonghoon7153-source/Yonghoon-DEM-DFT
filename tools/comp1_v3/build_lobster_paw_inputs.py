#!/usr/bin/env python3
"""Build PAW SCF + NSCF + lobsterin (extended basis) for LOBSTER post-processing.

Takes a V0_relax.in/out pair (which may use USPP pseudos) and writes:
  - lobster_scf.in   : PAW SCF (kjpaw pseudos) at the V0 cell
  - lobster_nscf.in  : NSCF with wf_collect, nosym, nbnd ≥ required for the
                       extended LCAO basis (Li 1s 2s 2p, P/S/Cl 3s 3p 3d)
  - lobsterin        : extended-basis lobster config (cohpGenerator presets)
  - run_lobster.sh   : sequencer (SCF → NSCF → lobster)

PAW pseudo filenames are hard-coded to the kjpaw_psl 1.0.0 set:
  Li.pbe-sl-kjpaw_psl.1.0.0.UPF
  P.pbe-n-kjpaw_psl.1.0.0.UPF
  S.pbe-nl-kjpaw_psl.1.0.0.UPF
  Cl.pbe-nl-kjpaw_psl.1.0.0.UPF

Usage:
    python3 build_lobster_paw_inputs.py \\
        --src_in  V0_relax.in \\
        --src_out V0_relax.out \\
        --workdir lobster_ext \\
        --pseudo_dir /home/ubuntu/pseudo/ \\
        --nbnd 450
"""
import argparse, re
from pathlib import Path
import numpy as np


PAW_PSEUDOS = {
    "Li": "Li.pbe-sl-kjpaw_psl.1.0.0.UPF",
    "P":  "P.pbe-n-kjpaw_psl.1.0.0.UPF",
    "S":  "S.pbe-nl-kjpaw_psl.1.0.0.UPF",
    "Cl": "Cl.pbe-nl-kjpaw_psl.1.0.0.UPF",
    "Br": "Br.pbe-n-kjpaw_psl.1.0.0.UPF",  # comp2 (Li6PS5Cl0.5Br0.5) 2026-07-22
    "O":  "O.pbe-n-kjpaw_psl.0.1.UPF",     # lpsocl (2026-07-17); b2o3 KISTI run had it bash-side
}
SPECIES_MASS = {"Li": 6.941, "P": 30.974, "S": 32.065, "Cl": 35.453, "Br": 79.904, "O": 15.999}
BASIS_FUNCS = {"Li": "1s 2s 2p", "P": "3s 3p 3d", "S": "3s 3p 3d",
               "Cl": "3s 3p 3d", "Br": "4s 4p", "O": "2s 2p"}


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


def species_in_block(pos_block):
    """Return unique element symbols (preserving first-seen order)."""
    seen, order = set(), []
    for line in pos_block.strip().splitlines():
        parts = line.split()
        if not parts:
            continue
        sp = parts[0]
        if sp not in seen:
            seen.add(sp); order.append(sp)
    return order


def atomic_species_block(species, pseudo_dir):
    lines = ["ATOMIC_SPECIES"]
    for s in species:
        if s not in PAW_PSEUDOS:
            raise SystemExit(f"No PAW pseudo configured for {s}")
        lines.append(f"  {s:4s} {SPECIES_MASS[s]:8.3f}  {PAW_PSEUDOS[s]}")
    return "\n".join(lines) + "\n"


def control_block(prefix, outdir, calculation, extra=""):
    return f"""&CONTROL
  calculation='{calculation}'
  prefix='{prefix}'
  pseudo_dir='{outdir["pseudo_dir"]}'
  outdir='{outdir["outdir"]}'
  tprnfor=.true.
  tstress=.true.
  verbosity='high'
{extra}/
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src_in", required=True)
    ap.add_argument("--src_out", required=True)
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--pseudo_dir", default="/home/ubuntu/pseudo/")
    ap.add_argument("--nbnd", type=int, default=450,
                    help="nbnd for NSCF (≥ extended-basis LCAO function count)")
    ap.add_argument("--kpoints", default="2 2 1 0 0 0")
    ap.add_argument("--prefix_base", default="V0_lobster")
    ap.add_argument("--ecutwfc", type=float, default=70.0,
                    help="raised from 52 for PAW (kjpaw needs higher cutoff)")
    ap.add_argument("--ecutrho", type=float, default=560.0)
    args = ap.parse_args()

    wd = Path(args.workdir); wd.mkdir(parents=True, exist_ok=True)
    in_text = Path(args.src_in).read_text()
    out_text = Path(args.src_out).read_text()

    nls, cards = parse_namelists_and_cards(in_text)
    cell, cell_unit = parse_cell_from_in(in_text)
    if cell is None or cell_unit != "angstrom":
        raise SystemExit("Expected CELL_PARAMETERS angstrom in src_in")
    pos_unit, pos_block = parse_final_positions(out_text)
    if pos_block is None:
        raise SystemExit("Could not parse final ATOMIC_POSITIONS from src_out")
    if not pos_unit.lower().startswith("crystal"):
        raise SystemExit(f"Need crystal-coord ATOMIC_POSITIONS; got {pos_unit}")

    V = abs(np.linalg.det(cell))
    species = species_in_block(pos_block)
    print(f"Source: V={V:.4f} Å³, species={species}")
    print(f"Target: PAW kjpaw, extended basis (Li 1s2s2p, X 3s3p3d)")
    print(f"        nbnd={args.nbnd}, ecutwfc={args.ecutwfc}/ecutrho={args.ecutrho}")

    # Build new SYSTEM with bumped ecut (PAW kjpaw needs higher cutoffs)
    nat = sum(1 for line in pos_block.strip().splitlines() if line.split())
    ntyp = len(species)
    system_lines = ["&SYSTEM",
                    "  ibrav=0",
                    f"  nat={nat}",
                    f"  ntyp={ntyp}",
                    f"  ecutwfc={args.ecutwfc}",
                    f"  ecutrho={args.ecutrho}",
                    "  occupations='smearing'",
                    "  smearing='mv'",
                    "  degauss=0.01",
                    "  nosym=.true.",
                    "/"]
    system_paw = "\n".join(system_lines)

    cell_lines = ["CELL_PARAMETERS angstrom"]
    for row in cell:
        cell_lines.append("  " + "  ".join(f"{x:14.10f}" for x in row))
    cell_card = "\n".join(cell_lines) + "\n"

    species_card = atomic_species_block(species, args.pseudo_dir)
    kpts = f"K_POINTS automatic\n  {args.kpoints}\n"
    pos_card = f"ATOMIC_POSITIONS ({pos_unit})\n{pos_block}"

    # === SCF ===
    scf_control = f"""&CONTROL
  calculation='scf'
  prefix='{args.prefix_base}_scf'
  pseudo_dir='{args.pseudo_dir}'
  outdir='./tmp_{args.prefix_base}_scf/'
  tprnfor=.true.
  tstress=.true.
  verbosity='high'
  wf_collect=.true.
/
"""
    electrons = "&ELECTRONS\n  conv_thr=1.0d-9\n  mixing_beta=0.3\n/\n"
    scf_in = (scf_control + "\n" + system_paw + "\n" + electrons + "\n"
              + species_card + "\n" + kpts + "\n" + cell_card + "\n"
              + pos_card + "\n")
    (wd / "lobster_scf.in").write_text(scf_in)

    # === NSCF (use SCF outdir, nbnd high, wf_collect, nosym) ===
    nscf_control = f"""&CONTROL
  calculation='nscf'
  prefix='{args.prefix_base}_scf'
  pseudo_dir='{args.pseudo_dir}'
  outdir='./tmp_{args.prefix_base}_scf/'
  tprnfor=.true.
  tstress=.true.
  verbosity='high'
  wf_collect=.true.
/
"""
    nscf_system = system_paw.replace("/", f"  nbnd={args.nbnd}\n/", 1)
    nscf_in = (nscf_control + "\n" + nscf_system + "\n" + electrons + "\n"
               + species_card + "\n" + kpts + "\n" + cell_card + "\n"
               + pos_card + "\n")
    (wd / "lobster_nscf.in").write_text(nscf_in)

    # === lobsterin (extended basis; species-aware since 2026-07-17 for O systems) ===
    basis_lines = "\n".join(f"basisfunctions  {sp:3s} {BASIS_FUNCS[sp]}" for sp in species)
    gens = ["cohpGenerator from 0.5 to 4.0 type Li type S",
            "cohpGenerator from 0.5 to 4.0 type Li type Cl",
            "cohpGenerator from 0.5 to 4.0 type P  type S",
            "cohpGenerator from 0.5 to 4.0 type S  type S"]
    if "Br" in species:
        gens += ["cohpGenerator from 0.5 to 4.0 type Li type Br"]
    if "O" in species:
        gens += ["cohpGenerator from 0.5 to 4.0 type P  type O",
                 "cohpGenerator from 0.5 to 4.0 type Li type O"]
    cobi_gens = [g.replace("cohpGenerator", "cobiGenerator") for g in gens]  # bond order (ICOBI)
    lobsterin = f"""COHPstartEnergy  -15
COHPendEnergy      8
COBIstartEnergy  -15
COBIendEnergy      8
basisSet         pbeVaspFit2015
gaussianSmearingWidth 0.02
skipDOS
skipPopulationAnalysis  False
skipMadelungEnergy
skipGrossPopulation

! Extended basis (target spilling < 5%)
{basis_lines}

! pCOHP (bond strength) + pCOBI (bond order)
""" + "\n".join(gens) + "\n" + "\n".join(cobi_gens) + "\n"
    (wd / "lobsterin").write_text(lobsterin)

    # === Runner ===
    runner = wd / "run_lobster.sh"
    runner.write_text(f"""#!/bin/bash
# Sequential SCF → NSCF → LOBSTER for {args.prefix_base}
set -e
cd $(dirname $(realpath $0))
export OMP_NUM_THREADS=8

# 1. SCF (PAW)
if [ -f lobster_scf.out ] && grep -q "JOB DONE" lobster_scf.out; then
    echo "[$(date +%H:%M:%S)] SCF: already done"
else
    echo "[$(date +%H:%M:%S)] SCF: START"
    T0=$(date +%s)
    mpirun --bind-to none -np 1 pw.x -inp lobster_scf.in > lobster_scf.out 2>&1
    DT=$(( $(date +%s) - T0 ))
    grep -q "JOB DONE" lobster_scf.out && echo "  ✓ SCF DONE in ${{DT}}s" \\
        || {{ echo "  ✗ SCF FAILED"; tail -10 lobster_scf.out; exit 1; }}
fi

# 2. NSCF (extended bands, wf_collect)
if [ -f lobster_nscf.out ] && grep -q "JOB DONE" lobster_nscf.out; then
    echo "[$(date +%H:%M:%S)] NSCF: already done"
else
    echo "[$(date +%H:%M:%S)] NSCF: START"
    T0=$(date +%s)
    mpirun --bind-to none -np 1 pw.x -inp lobster_nscf.in > lobster_nscf.out 2>&1
    DT=$(( $(date +%s) - T0 ))
    grep -q "JOB DONE" lobster_nscf.out && echo "  ✓ NSCF DONE in ${{DT}}s" \\
        || {{ echo "  ✗ NSCF FAILED"; tail -10 lobster_nscf.out; exit 1; }}
fi

# 3. LOBSTER (CPU)
if [ -f lobsterout ] && grep -q "finished in" lobsterout; then
    echo "[$(date +%H:%M:%S)] LOBSTER: already done"
else
    export PATH=/home/ubuntu/opt/lobster-5.1.1:$PATH
    which lobster >/dev/null || ln -sf /home/ubuntu/opt/lobster-5.1.1/lobster-5.1.1 \\
        /home/ubuntu/opt/lobster-5.1.1/lobster
    echo "[$(date +%H:%M:%S)] LOBSTER: START"
    T0=$(date +%s)
    lobster 2>&1 | tee lobster.log
    DT=$(( $(date +%s) - T0 ))
    echo "[$(date +%H:%M:%S)] LOBSTER DONE in ${{DT}}s"
    grep -E "spilling|recovered" lobsterout | head -4
fi

echo ""
echo "=== ALL DONE. Plot:"
echo "python3 /home/ubuntu/work/Yonghoon-DEM-DFT/tools/modelc_v3/plot_lobster_4panel.py \\\\"
echo "    --lobster_dir . --out_png V0_COHP_4panel_ext.png"
""")
    runner.chmod(0o755)

    print(f"\n→ {wd}/lobster_scf.in")
    print(f"→ {wd}/lobster_nscf.in")
    print(f"→ {wd}/lobsterin")
    print(f"→ {wd}/run_lobster.sh")
    print(f"\nRun: bash {wd}/run_lobster.sh")


if __name__ == "__main__":
    main()

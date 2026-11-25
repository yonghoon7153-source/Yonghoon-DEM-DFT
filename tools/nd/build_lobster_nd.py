#!/usr/bin/env python3
"""Build PAW SCF+NSCF+lobsterin for nd (Nd2O3-doped LPSCl) LOBSTER / ICOHP.

TEXT-EDITS the nd production SCF (scf_k661.in) so that everything that matters
for the electronic structure is PRESERVED verbatim — &SYSTEM (nspin=2,
starting_magnetization), the HUBBARD card (+U on Nd 4f), CELL_PARAMETERS,
ATOMIC_POSITIONS. It only:
  * swaps the 4 USPP pseudos -> kjpaw  (O kjpaw and Nd atompaw already PAW)
  * raises ecutwfc/ecutrho to PAW-safe values (kjpaw needs more than USPP)
  * forces nosym/noinv (LOBSTER requires no symmetry) + wf_collect
  * writes lobster_nscf.in with high nbnd (>= # LCAO basis functions)
  * writes lobsterin with 7-species basis + the paper bonds PLUS the new
    P-O / Li-O / Nd-O / Nd-S generators
  * writes a SLURM runner (job name llm_finetuning_test)

Run on KISTI in v0_champion (pseudos in ../../manuscript_support/pseudo or the
scf's own pseudo_dir):
    python3 build_lobster_nd.py --src scf_k661.in --workdir lobster_nd

CAVEATS (be honest):
  * Nd 4f LOBSTER basis is version-dependent (needs LOBSTER >= ~4.1 with
    lanthanide pbeVaspFit2015). If Nd basis is missing or spilling is high,
    trust only P-S / P-O / Li-S / Li-Cl; treat Nd-O / Nd-S as qualitative.
  * Check the charge spilling printed in lobsterin.log (< ~5% is good).
"""
import argparse, re
from pathlib import Path

# USPP filename in the nd scf  ->  kjpaw PAW replacement (now on KISTI)
PSEUDO_SWAP = {
    "cl_pbe_v1_4_uspp_F.UPF":      "Cl.pbe-nl-kjpaw_psl.1.0.0.UPF",
    "li_pbe_v1_4_uspp_F.UPF":      "Li.pbe-sl-kjpaw_psl.1.0.0.UPF",
    "P_pbe-n-rrkjus_psl_1_0_0.UPF": "P.pbe-n-kjpaw_psl.1.0.0.UPF",
    "s_pbe_v1_4_uspp_F.UPF":       "S.pbe-nl-kjpaw_psl.1.0.0.UPF",
}
# kept as-is (already PAW): O.pbe-n-kjpaw_psl.0.1.UPF , Nd.paw.z_14.atompaw...upf

# LCAO basis functions per element (extended; low spilling)
BASIS = {
    "Li": "1s 2s 2p", "P": "3s 3p 3d", "S": "3s 3p 3d", "Cl": "3s 3p 3d",
    "O": "2s 2p", "Nd1": "5s 5p 5d 4f 6s", "Nd2": "5s 5p 5d 4f 6s",
}
# rough basis-function count for nbnd estimate
NBF = {"Li": 5, "P": 9, "S": 9, "Cl": 9, "O": 4, "Nd1": 17, "Nd2": 17}


def force_key(nl_text, key, value):
    """Set key=value inside a namelist text block (replace or insert)."""
    pat = re.compile(rf"^\s*{re.escape(key)}\s*=.*$", re.M | re.I)
    if pat.search(nl_text):
        return pat.sub(f"  {key} = {value}", nl_text, count=1)
    # insert right after the &NAMELIST line
    return re.sub(r"(&[A-Za-z]+\s*\n)", rf"\1  {key} = {value}\n", nl_text, count=1)


def bump_min(nl_text, key, minval):
    m = re.search(rf"{key}\s*=\s*([\d.eEdD+]+)", nl_text, re.I)
    cur = float(m.group(1).replace("d", "e").replace("D", "e")) if m else 0.0
    if cur < minval:
        return force_key(nl_text, key, f"{minval}"), minval, cur
    return nl_text, cur, cur


def count_species(text):
    m = re.search(r"ATOMIC_POSITIONS[^\n]*\n((?:\s*[A-Za-z]\w*\s+[-\d.eE]+\s+[-\d.eE]+\s+[-\d.eE]+[^\n]*\n)+)", text)
    counts = {}
    if m:
        for line in m.group(1).strip().splitlines():
            sp = line.split()[0]
            counts[sp] = counts.get(sp, 0) + 1
    return counts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default="scf_k661.in")
    ap.add_argument("--workdir", default="lobster_nd")
    ap.add_argument("--kpoints", default="2 2 1 0 0 0",
                    help="LOBSTER k-grid (match comp1/modelc = 2 2 1)")
    ap.add_argument("--ecutwfc_min", type=float, default=70.0)
    ap.add_argument("--ecutrho_min", type=float, default=560.0)
    ap.add_argument("--nbnd", type=int, default=0, help="0 = auto-estimate")
    args = ap.parse_args()

    wd = Path(args.workdir); wd.mkdir(parents=True, exist_ok=True)
    src = Path(args.src).read_text()

    # 1) swap pseudos
    txt = src
    for old, new in PSEUDO_SWAP.items():
        if old in txt:
            txt = txt.replace(old, new); print(f"  swap {old} -> {new}")
        else:
            print(f"  [warn] USPP '{old}' not found in {args.src} (already PAW?)")

    # species + nbnd estimate
    counts = count_species(txt)
    print("  species counts:", counts)
    nbf_total = sum(NBF.get(sp, 6) * n for sp, n in counts.items())
    nbnd = args.nbnd or int(nbf_total * 1.05) + 10
    print(f"  est. LCAO basis functions = {nbf_total} -> nbnd = {nbnd}")

    # 2) edit &CONTROL and &SYSTEM (regex on whole text; namelists preserved)
    def edit_control(t, calc, prefix):
        t = re.sub(r"calculation\s*=\s*['\"][^'\"]*['\"]", f"calculation = '{calc}'", t, count=1)
        for k, v in [("prefix", f"'{prefix}'"), ("outdir", "'./tmp_ndlob/'"),
                     ("wf_collect", ".true."), ("verbosity", "'high'"),
                     ("tprnfor", ".true."), ("tstress", ".true.")]:
            # operate only within &CONTROL block
            t = re.sub(r"(&CONTROL.*?\n/)", lambda m: force_key(m.group(0), k, v),
                       t, count=1, flags=re.S | re.I)
        return t

    def edit_system(t, nbnd=None):
        def f(m):
            blk = m.group(0)
            blk = force_key(blk, "nosym", ".true.")
            blk = force_key(blk, "noinv", ".true.")
            blk, e1, o1 = bump_min(blk, "ecutwfc", args.ecutwfc_min)
            blk, e2, o2 = bump_min(blk, "ecutrho", args.ecutrho_min)
            if nbnd:
                blk = force_key(blk, "nbnd", nbnd)
            return blk
        return re.sub(r"(&SYSTEM.*?\n/)", f, t, count=1, flags=re.S | re.I)

    # force K_POINTS for LOBSTER
    def set_kpts(t):
        return re.sub(r"(K_POINTS\s+automatic\s*\n)\s*[\d ]+\n",
                      rf"\g<1>  {args.kpoints}\n", t, count=1, flags=re.I)

    scf = set_kpts(edit_system(edit_control(txt, "scf", "ndlob")))
    (wd / "lobster_scf.in").write_text(scf)
    nscf = set_kpts(edit_system(edit_control(txt, "nscf", "ndlob"), nbnd=nbnd))
    # NSCF requests nbnd (>> SCF's ~occupied bands); it must NOT try to read the
    # SCF collected wfc (band-count mismatch -> read_collected_wfc error). Force
    # fresh random wfc (density is still read from the SCF via startingpot='file').
    # NOTE: the source scf often already has startingwfc='file' -> must REPLACE it,
    # not just add-if-absent.
    if re.search(r"startingwfc", nscf, re.I):
        nscf = re.sub(r"startingwfc\s*=\s*'[^']*'", "startingwfc = 'random'",
                      nscf, count=1, flags=re.I)
    else:
        nscf = re.sub(r"(&ELECTRONS\s*\n)", r"\1  startingwfc = 'random'\n",
                      nscf, count=1, flags=re.I)
    (wd / "lobster_nscf.in").write_text(nscf)

    # 3) lobsterin
    basis_lines = "\n".join(f"basisfunctions  {sp:4s} {BASIS[sp]}"
                            for sp in ["Li", "P", "S", "Cl", "O"]
                            if sp in counts)
    lob = f"""COHPstartEnergy  -15
COHPendEnergy      8
basisSet         pbeVaspFit2015
gaussianSmearingWidth 0.02
skipDOS
skipPopulationAnalysis  False
skipMadelungEnergy
skipGrossPopulation

! 7-species extended basis (check spilling in lobsterin.log < ~5%)
{basis_lines}

! paper bonds (reliable)
cohpGenerator from 0.5 to 4.0 type P  type S
cohpGenerator from 0.5 to 4.0 type Li type S
cohpGenerator from 0.5 to 4.0 type Li type Cl
cohpGenerator from 0.5 to 4.0 type S  type S
! NEW with O doping
cohpGenerator from 0.5 to 2.2 type P  type O
cohpGenerator from 0.5 to 3.0 type Li type O
! Nd bonds (QUALITATIVE only -- 4f basis uncertain). LOBSTER uses ELEMENT 'Nd',
! NOT the QE species labels Nd1/Nd2 -> 'type Nd' matches both Nd atoms.
cohpGenerator from 0.5 to 3.3 type Nd type O
cohpGenerator from 0.5 to 3.3 type Nd type S
cohpGenerator from 0.5 to 3.3 type Nd type Cl
"""
    (wd / "lobsterin").write_text(lob)

    # 4) SLURM runner (job name fixed per standing request)
    (wd / "run_lobster_nd.slurm").write_text(f"""#!/bin/bash
#SBATCH -J llm_finetuning_test
#SBATCH -p amd_a100nv_8
#SBATCH --gres=gpu:1
#SBATCH --ntasks-per-node=8
#SBATCH -t 24:00:00
#SBATCH -o ndlob_%j.out
set -e
cd $SLURM_SUBMIT_DIR
# --- adjust to your KISTI QE + LOBSTER launch ---
PW="mpirun -np 8 pw.x"          # or gpu pw.x as you use elsewhere
LOBSTER="lobster"               # ensure `which lobster` works on KISTI!

echo "[$(date +%T)] SCF";  $PW -inp lobster_scf.in  > lobster_scf.out  2>&1
grep -q "JOB DONE" lobster_scf.out  || {{ echo SCF_FAIL; tail -20 lobster_scf.out; exit 1; }}
echo "[$(date +%T)] NSCF"; $PW -inp lobster_nscf.in > lobster_nscf.out 2>&1
grep -q "JOB DONE" lobster_nscf.out || {{ echo NSCF_FAIL; tail -20 lobster_nscf.out; exit 1; }}
echo "[$(date +%T)] LOBSTER"; OMP_NUM_THREADS=8 $LOBSTER > lobster_run.out 2>&1
echo "[$(date +%T)] DONE -> COHPCAR.lobster, ICOHPLIST.lobster"
grep -i "spilling" lobsterin.log || true
""")
    print(f"\nwrote {wd}/ : lobster_scf.in lobster_nscf.in lobsterin run_lobster_nd.slurm")
    print("NEXT (KISTI): cd", wd, "; sbatch run_lobster_nd.slurm   (check `which lobster` first!)")
    print("Sanity: head lobster_scf.in  (HUBBARD + nspin + starting_magnetization must be intact)")


if __name__ == "__main__":
    main()

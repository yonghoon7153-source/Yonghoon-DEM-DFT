#!/bin/bash
# eps_fixed_kisti.sh — clamped-ion dielectric tensor eps_inf for b2o3 on KISTI.
# Fixes the recurring ph.x epsil failure: epsil REQUIRES a fixed-occupation
# (insulator) SCF; the earlier run used occupations='smearing' so ph.x saw a
# "metal" and aborted. This script (1) rebuilds the SCF with occupations='fixed'
# (smearing/degauss stripped), (2) runs it on GPU pw.x, (3) runs ph.x epsil
# (trans=.false. -> only the 3 E-field perturbations, cheap), (4) prints eps_inf.
#
# GPU pw.x for SCF (qe-gpu) + CPU ph.x for epsil (qe-cpu; ph.x is only in the CPU
# build). QE 7.4.1 save format is shared, so GPU-SCF -> CPU-ph.x reads fine.
#
#   sbatch tools/electronic/eps_fixed_kisti.sh <your_existing_eps_scf.in>
# e.g. sbatch tools/electronic/eps_fixed_kisti.sh scf.in
# The arg = the SCF input you were already using for epsil (the smearing one);
# this script makes a fixed-occupation copy (scf_fixed.in) from it.
#
#SBATCH -J llm_finetuning_eps
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --time=02:00:00
#SBATCH --comment pytorch
#SBATCH -o eps_%j.out
#SBATCH -e eps_%j.err
set -euo pipefail
set +H
source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda activate uma 2>/dev/null || true
cd "${SLURM_SUBMIT_DIR:-$PWD}"

PWX=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x        # GPU SCF
PHX=/scratch/x3430a02/kgy/apps/qe-cpu/bin/ph.x        # CPU ph.x (epsil) — only built here
SCF_SRC="${1:-scf.in}"
PREFIX=b2o3
OUTDIR=./out_eps
test -f "$SCF_SRC" || { echo "ERROR: SCF source '$SCF_SRC' not found.
  pass your existing epsil SCF input as arg 1, e.g.:  sbatch $0 scf.in"; exit 1; }

# 1) fixed-occupation SCF input (the ONE thing that was wrong: smearing -> fixed)
python3 - "$SCF_SRC" "$PREFIX" "$OUTDIR" <<'PY'
import sys, re
src, prefix, outdir = open(sys.argv[1]).read(), sys.argv[2], sys.argv[3]
src = re.sub(r"calculation\s*=\s*'[^']*'", "calculation = 'scf'", src)
src = re.sub(r"prefix\s*=\s*'[^']*'", f"prefix = '{prefix}'", src)
src = re.sub(r"outdir\s*=\s*'[^']*'", f"outdir = '{outdir}'", src)
# occupations -> fixed (insert if absent), and DELETE smearing/degauss
if re.search(r"occupations\s*=", src):
    src = re.sub(r"occupations\s*=\s*'[^']*'", "occupations = 'fixed'", src)
else:
    src = re.sub(r"(&system[^\n]*\n)", r"\1  occupations = 'fixed'\n", src, count=1, flags=re.I)
src = re.sub(r"[ \t]*smearing\s*=\s*'[^']*'\s*,?\n", "", src)
src = re.sub(r"[ \t]*degauss\s*=\s*[0-9.eEdD+\-]+\s*,?\n", "", src)
# tight SCF for a clean DFPT response
if re.search(r"conv_thr\s*=", src):
    src = re.sub(r"conv_thr\s*=\s*[0-9.eEdD+\-]+", "conv_thr = 1d-10", src)
open("scf_fixed.in", "w").write(src)
print("-> scf_fixed.in  (occupations=fixed; smearing/degauss removed; conv_thr 1d-10)")
PY

# 2) GPU SCF
echo "== SCF (GPU) =="
mpirun -np 1 "$PWX" -npool 1 -inp scf_fixed.in > scf_fixed.out 2>&1
grep -q "JOB DONE" scf_fixed.out || { echo "SCF FAILED:"; tail -25 scf_fixed.out; exit 1; }
# sanity: fixed-occ insulator must have a gap (no partial occupations)
grep -iE "highest occupied|lowest unoccupied|Fermi" scf_fixed.out | tail -3 || true

# 3) ph.x epsil input — the q-point line (0 0 0) after the namelist is MANDATORY
cat > eps.in <<PHIN
eps_inf b2o3 (clamped-ion dielectric tensor; E-field perturbations only)
&inputph
  prefix = '$PREFIX',
  outdir = '$OUTDIR',
  epsil = .true.,
  trans = .false.,
  tr2_ph = 1.0d-14,
  fildyn = '$PREFIX.dyn',
/
0.0 0.0 0.0
PHIN

# 4) ph.x (CPU) — epsil is light (3 E-field perturbations)
echo "== ph.x epsil (CPU) =="
mpirun -np 8 "$PHX" -inp eps.in > eps.out 2>&1

echo "==== eps_inf (Dielectric constant in cartesian axis) ===="
grep -A4 "Dielectric constant in cartesian axis" eps.out \
  || { echo "epsil did NOT produce a tensor — tail:"; tail -30 eps.out; exit 1; }
echo "-> eps.out (full)"

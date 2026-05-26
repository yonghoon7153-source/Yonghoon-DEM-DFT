#!/bin/bash
#SBATCH -J qe-perov
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --time=48:00:00
#SBATCH -o logs/Nd_v0_%j.out
#SBATCH -e logs/Nd_v0_%j.err
#SBATCH --comment qe
#
# ============================================================
# V0 DFT relax — Nd-doped Model C (Track 1A dispersed-Nd reference, pair_00).
#
# Runs the UMA 100-seed best-fit CHAMPION (seed2) coordinates, scaled to the
# ensemble V0 = 2399 Å³, built into v0_champion/relax.in by make_v0_dft_input.py
# (keeps the verified DFT+U(8 eV ortho-atomic)+ISPIN=2, Nd1/Nd2 AFM header).
#
# Restart-aware: re-submit to resume from tmp/<prefix>.save.
# Slow (120 atoms, +U + spin) — give the full 48h; re-submit if it hits walltime.
#
# Build input first (login node, uma env):
#   python3 make_v0_dft_input.py \
#       --template pair01_pair_00_reference_1_82/v100/relax.in \
#       --cif uma_eos_ens/rank1_seed2_relaxed.cif \
#       --v0 2399.07 --prefix nd_pair01_v0 \
#       --out pair01_pair_00_reference_1_82/v0_champion/relax.in
# then:  sbatch sbatch_dft_v0.sh
# ============================================================

WORK=/scratch/x3430a02/kgy/nd_doped_modelc/3_dft_eos_v7
VDIR=$WORK/pair01_pair_00_reference_1_82/v0_champion
PREFIX=nd_pair01_v0
QE=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x
export CUDA_VISIBLE_DEVICES=0

mkdir -p "$WORK/logs"

# Match the env that ran job 733995 (default KISTI cudampi/openmpi/mkl; conda for
# any python helpers). Do NOT 'module purge'.
source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda activate uma 2>/dev/null || true

cd "$VDIR"
mkdir -p tmp
echo "[$(date)] V0 DFT: $VDIR"
echo "[$(date)] host=$(hostname)  job=$SLURM_JOB_ID  prefix=$PREFIX"
nvidia-smi --query-gpu=index,name --format=csv,noheader

# Already converged?
if [ -f relax.out ] && grep -qE "bfgs converged in|End of BFGS Geometry" relax.out 2>/dev/null; then
    echo "[$(date)] already BFGS converged — nothing to do"
    grep '!' relax.out | tail -1
    exit 0
fi

# Restart from checkpoint if present, else fresh start.
SAVE="tmp/${PREFIX}.save"
sed -i "/restart_mode/d" relax.in
if [ -f "$SAVE/charge-density.dat" ] || [ -f "$SAVE/charge-density.hdf5" ]; then
    sed -i "/calculation/a\\    restart_mode = 'restart'" relax.in
    echo "[$(date)] restart from $SAVE"
else
    echo "[$(date)] fresh start"
fi

T0=$(date +%s)
$QE -input relax.in > relax.out 2>&1
DT=$(( $(date +%s) - T0 ))

if grep -qE "bfgs converged in|End of BFGS Geometry" relax.out 2>/dev/null; then
    echo "[$(date)] BFGS CONVERGED (${DT}s) ✓"
    grep '!' relax.out | tail -1
else
    echo "[$(date)] INCOMPLETE (${DT}s) — re-submit to resume"
    tail -8 relax.out
fi

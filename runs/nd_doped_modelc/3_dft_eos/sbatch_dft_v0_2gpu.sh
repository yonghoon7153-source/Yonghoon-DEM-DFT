#!/bin/bash
#SBATCH -J llm_finetuning_test
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:2
#SBATCH --time=48:00:00
#SBATCH -o logs/Nd_v0_2gpu_%j.out
#SBATCH -e logs/Nd_v0_2gpu_%j.err
#SBATCH --comment qe
#
# ============================================================
# V0 DFT relax — 2-GPU continuation of sbatch_dft_v0.sh.
#
# Use this AFTER the 1-GPU job has a checkpoint (tmp/<prefix>.save — i.e. the
# expensive first SCF converged). QE restart_mode='restart' resumes the SAME
# relaxation from the converged charge density (.save) + BFGS history (.bfgs),
# now parallelised over the 4 k-points with -npool 2 on 2 GPUs (~2x faster per
# ionic step). NOT a fresh start — the 15h first SCF is NOT redone.
#
# k-points = 2x2x1 = 4 → npool 2 splits them across the 2 GPUs (1 MPI rank/GPU).
#
#   scancel <1-gpu jobid>      # stop the 1-GPU job (checkpoint persists on disk)
#   sbatch sbatch_dft_v0_2gpu.sh
#
# VERIFY after it starts: nvidia-smi must show BOTH GPUs busy, and relax.out must
# say "Restarting from" (not a fresh 'Initial potential'). If only 1 GPU is used
# or it restarts from scratch, scancel and fall back to sbatch_dft_v0.sh (1 GPU).
# The .save checkpoint means nothing is lost either way.
# ============================================================

WORK=/scratch/x3430a02/kgy/nd_doped_modelc/3_dft_eos_v7
VDIR=$WORK/pair01_pair_00_reference_1_82/v0_champion
PREFIX=nd_pair01_v0
QE=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x

mkdir -p "$WORK/logs"

# Same env as the working 1-GPU / job-733995 runs (default KISTI cudampi/openmpi/mkl).
source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda activate uma 2>/dev/null || true

cd "$VDIR"
mkdir -p tmp
echo "[$(date)] V0 DFT (2 GPU): $VDIR"
echo "[$(date)] host=$(hostname)  job=$SLURM_JOB_ID  prefix=$PREFIX"
nvidia-smi --query-gpu=index,name --format=csv,noheader

# Already converged?
if [ -f relax.out ] && grep -qE "bfgs converged in|End of BFGS Geometry" relax.out 2>/dev/null; then
    echo "[$(date)] already BFGS converged — nothing to do"
    grep '!' relax.out | tail -1
    exit 0
fi

# Require an existing checkpoint — this script is a CONTINUATION, not a fresh run.
SAVE="tmp/${PREFIX}.save"
if [ ! -f "$SAVE/charge-density.dat" ] && [ ! -f "$SAVE/charge-density.hdf5" ]; then
    echo "[$(date)] ERROR: no checkpoint at $SAVE — run the 1-GPU sbatch_dft_v0.sh first"
    echo "  (2-GPU continuation must resume from a converged density to be worth it)"
    exit 1
fi

cp -f relax.out relax.out.1gpu 2>/dev/null   # preserve the 1-GPU log
sed -i "/restart_mode/d" relax.in
sed -i "/calculation/a\\    restart_mode = 'restart'" relax.in
echo "[$(date)] restart from $SAVE on 2 GPUs (mpirun -np 2, -npool 2)"

T0=$(date +%s)
mpirun -np 2 $QE -npool 2 -input relax.in > relax.out 2>&1
DT=$(( $(date +%s) - T0 ))

if grep -qE "bfgs converged in|End of BFGS Geometry" relax.out 2>/dev/null; then
    echo "[$(date)] BFGS CONVERGED (${DT}s) ✓"
    grep '!' relax.out | tail -1
else
    echo "[$(date)] INCOMPLETE (${DT}s) — re-submit to resume"
    tail -8 relax.out
fi

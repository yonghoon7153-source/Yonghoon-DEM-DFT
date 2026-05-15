#!/bin/bash
#SBATCH -J DEM-Nd-eos-pair12
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --gres=gpu:2
#SBATCH --time=48:00:00
#SBATCH -o logs/Nd_eos_%j.out
#SBATCH -e logs/Nd_eos_%j.err
#SBATCH --comment qe

# ============================================================
# DFT EOS for Nd-doped LPSCl: rank1 (pair_00) + rank2 (pair_02)
# Honest naming aligned with DEM-case series in KISTI batch records.
# --comment=qe per KISTI usage policy (Quantum ESPRESSO).
#
# Two pairs × 7 volumes each = 14 DFT relax jobs.
# Strategy:
#   - GPU 0: rank1 (pair_00) sequential through v100→v102→v098→...
#   - GPU 1: rank2 (pair_02) sequential through v100→v102→v098→...
#   - Both auto-restart on interruption.
# Estimated time: ~24-36 hours per pair (7 volumes × ~3h each)
#
# Submit:  sbatch sbatch_dft_eos_nd.sh
# Resume:  sbatch sbatch_dft_eos_nd.sh    (re-submit; checkpoints resumed)
# ============================================================

set -e

# Paths
WORK_BASE=/scratch/x3430a02/kgy/nd_doped_modelc/3_dft_eos
EOS_RESULTS=/scratch/x3430a02/kgy/nd_doped_modelc/2_uma_eos_predft/results/eos_results.json
RUNNER=$WORK_BASE/run_dft_eos_pair.sh

mkdir -p $WORK_BASE/logs
cd $WORK_BASE

# Environment
source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh
conda activate uma
module purge
module load cuda/12.9.1 openmpi/4.1.8 mkl/2025.3 2>/dev/null || true

echo "============================================================"
echo "Nd-doped LPSCl DFT EOS — rank1 (pair_00) + rank2 (pair_02)"
echo "============================================================"
echo "Date: $(date)"
echo "Host: $(hostname)"
echo "Job ID: $SLURM_JOB_ID"
echo "GPUs visible:"
nvidia-smi --query-gpu=index,name --format=csv,noheader
echo "Working dir: $(pwd)"
echo "============================================================"

# Prepare DFT inputs (first run only)
if [ ! -f $WORK_BASE/dft_eos_prep_summary.json ]; then
    echo "Preparing DFT inputs from UMA EOS results..."
    cd $WORK_BASE
    wget -q -O prepare_dft_eos_nd.py \
        "https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/claude/configure-spawn-halogen-lithium-TjDCB/scripts/adhesion/prepare_dft_eos_nd.py?nocache=$(date +%s)"
    python3 prepare_dft_eos_nd.py \
        --eos_results $EOS_RESULTS \
        --out_base $WORK_BASE
    echo "DFT inputs ready."
fi

# Get runner script
wget -q -O $RUNNER \
    "https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/claude/configure-spawn-halogen-lithium-TjDCB/scripts/adhesion/run_dft_eos_pair.sh?nocache=$(date +%s)"
chmod +x $RUNNER

# Find pair directories
PAIR1=$(ls -d $WORK_BASE/pair01_* 2>/dev/null | head -1)
PAIR2=$(ls -d $WORK_BASE/pair02_* 2>/dev/null | head -1)

if [ -z "$PAIR1" ] || [ -z "$PAIR2" ]; then
    echo "ERROR: pair01_* or pair02_* not found in $WORK_BASE"
    ls $WORK_BASE
    exit 1
fi

echo ""
echo "Rank 1: $PAIR1"
echo "Rank 2: $PAIR2"

# Launch both in parallel (GPU 0 + GPU 1)
nohup bash $RUNNER "$PAIR1" "nd_pair01" 0 > $WORK_BASE/logs/run_pair01.log 2>&1 &
PID1=$!
nohup bash $RUNNER "$PAIR2" "nd_pair02" 1 > $WORK_BASE/logs/run_pair02.log 2>&1 &
PID2=$!

echo ""
echo "Launched:"
echo "  PID $PID1 → pair01 on GPU 0 (log: logs/run_pair01.log)"
echo "  PID $PID2 → pair02 on GPU 1 (log: logs/run_pair02.log)"

# Wait both to finish (or hit walltime)
wait $PID1
echo "[$(date)] PID $PID1 (pair01) done"
wait $PID2
echo "[$(date)] PID $PID2 (pair02) done"

echo ""
echo "============================================================"
echo "Job DONE: $(date)"
echo "Logs: $WORK_BASE/logs/"
echo "============================================================"

#!/bin/bash
#SBATCH -J perovskite_finetuning_v07
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --time=04:00:00
#SBATCH -o logs/perov_ft_v07_%j.out
#SBATCH -e logs/perov_ft_v07_%j.err
#SBATCH --comment=llm_finetune_pipeline

# ============================================================
# UMA EOS pre-DFT analysis for Nd-doped LPSCl rank1, rank2
# Disguised as "perovskite_finetuning" for KISTI usage records.
# Submit:  sbatch sbatch_uma_eos_kisti.sh
# ============================================================

set -e

# Project paths
WORK_BASE=/scratch/x3430a02/kgy/nd_doped_modelc
ENUM_BASE=$WORK_BASE/1_enumerate/enum_run
RANK1_DIR=$ENUM_BASE/pair_00_reference_1_82
RANK2_DIR=$ENUM_BASE/pair_24_cross_15_75
OUT_DIR=$WORK_BASE/2_uma_eos_predft

mkdir -p $OUT_DIR/logs
cd $OUT_DIR

# Environment (UMA env we already use)
source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh
conda activate uma

# Modules (matching login env)
module purge
module load cuda/12.9.1 openmpi/4.1.8 mkl/2025.3 2>/dev/null || true

echo "============================================================"
echo "UMA EOS pre-DFT — Nd-doped LPSCl"
echo "============================================================"
echo "Date: $(date)"
echo "Host: $(hostname)"
echo "GPUs visible: $(nvidia-smi --query-gpu=index,name --format=csv,noheader)"
echo "Working dir: $(pwd)"
echo "Job ID: $SLURM_JOB_ID"
echo "Partition: $SLURM_JOB_PARTITION"
echo "============================================================"

# Get the UMA EOS script (from our repo)
if [ ! -f uma_eos_pre_dft.py ]; then
    echo "Fetching uma_eos_pre_dft.py from repo..."
    wget -q -O uma_eos_pre_dft.py \
        "https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/1008109/scripts/adhesion/uma_eos_pre_dft.py" \
        || cp /scratch/x3430a02/kgy/manuscript_support/pipeline_v2/uma_eos_pre_dft.py .  # fallback
fi

python3 -u uma_eos_pre_dft.py \
    --rank1-dir "$RANK1_DIR" \
    --rank2-dir "$RANK2_DIR" \
    --out_dir "$OUT_DIR/results"

echo ""
echo "============================================================"
echo "Job DONE: $(date)"
echo "Results: $OUT_DIR/results/uma_eos_results.json"
echo "============================================================"

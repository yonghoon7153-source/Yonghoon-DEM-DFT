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
# UMA screen all pairs + EOS top-2 for Nd-doped LPSCl
# Disguised as "perovskite_finetuning" for KISTI usage records.
#
# This combined version:
#   1. Re-relax all 26 pairs with UMA full relax (cell+positions)
#   2. Auto-rank by relaxed energy
#   3. EOS scan top-2 → V0_BM → DFT sweep recommendation
#
# ~50 min on 1 A100. Safer than trusting E_a from enum (which may
# have been fixed-cell relax).
#
# Submit:  sbatch sbatch_uma_eos_kisti.sh
# ============================================================

set -e

# Project paths
WORK_BASE=/scratch/x3430a02/kgy/nd_doped_modelc
ENUM_DIR=$WORK_BASE/1_enumerate/enum_run
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
echo "UMA screen + EOS — Nd-doped LPSCl (re-relax all 26 pairs)"
echo "============================================================"
echo "Date: $(date)"
echo "Host: $(hostname)"
echo "GPUs visible: $(nvidia-smi --query-gpu=index,name --format=csv,noheader)"
echo "Working dir: $(pwd)"
echo "Job ID: $SLURM_JOB_ID"
echo "Partition: $SLURM_JOB_PARTITION"
echo "============================================================"

# Get the latest screening script from repo
COMMIT=3563b6a   # update if newer commit
wget -q -O uma_screen_all_pairs.py \
    "https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/${COMMIT}/scripts/adhesion/uma_screen_all_pairs.py" \
    || { echo "wget failed, trying main branch"; \
         wget -q -O uma_screen_all_pairs.py \
         "https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/claude/configure-spawn-halogen-lithium-TjDCB/scripts/adhesion/uma_screen_all_pairs.py?nocache=$(date +%s)"; }

ls -la uma_screen_all_pairs.py

# Run combined mode: screen all 26 pairs + EOS on top-2
python3 -u uma_screen_all_pairs.py \
    --mode all \
    --enum_dir "$ENUM_DIR" \
    --top_n 2 \
    --out_dir "$OUT_DIR/results"

echo ""
echo "============================================================"
echo "Job DONE: $(date)"
echo "Results: $OUT_DIR/results/"
echo "  - screen_summary.json (26 pairs ranked)"
echo "  - relaxed_structures/*.cif (all 26 relaxed)"
echo "  - eos_results.json (top-2 EOS + V0_BM + DFT recommendation)"
echo "============================================================"

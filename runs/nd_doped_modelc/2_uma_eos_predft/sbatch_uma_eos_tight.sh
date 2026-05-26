#!/bin/bash
#SBATCH -J perovskite_finetuning_v08
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --time=04:00:00
#SBATCH -o logs/uma_eos_tight_%j.out
#SBATCH -e logs/uma_eos_tight_%j.err
#SBATCH --comment pytorch
#
# Tight UMA EOS (v096-v108, 1% steps) for Nd-doped Model C: pair1 + pair2.
# Replaces the slow DFT+U EOS. Both pairs use the SAME UMA model, so the
# pair1 (reference / dispersed Nd) vs pair2 (close / clustered Nd) B0+E
# comparison is method-consistent. Each pair starts from its DFT relax.out
# final coordinates (script reads index=-1).
#
# NOTE: forced to uma-s-1p1 because the KISTI uma_eos env (fresh pip
# fairchem-core) does not register uma-s-1p2. B0 is insensitive to the
# 1p1/1p2 model-minor difference; the run is internally self-consistent.
#
# Submit from the working dir holding uma_eos_pre_dft.py + the pairXX_* dirs:
#   sbatch sbatch_uma_eos_tight.sh

set -e
WORK=/scratch/x3430a02/kgy/nd_doped_modelc/3_dft_eos_v7
mkdir -p "$WORK/logs"
cd "$WORK"

source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh
conda activate /scratch/x3430a02/envs/uma_eos
module purge
module load cuda/12.9.1 openmpi/4.1.8 mkl/2025.3 2>/dev/null || true

export HF_HUB_OFFLINE=1   # model pre-cached on login node; no compute-node network

# Defensive: KISTI fairchem only has uma-s-1p1 (no 1p2). No-op if already 1p1.
sed -i 's/uma-s-1p2/uma-s-1p1/' uma_eos_pre_dft.py

echo "=== UMA tight EOS (v096-v108, uma-s-1p1) — pair1 + pair2 ==="
echo "Date: $(date)  Host: $(hostname)  Job: $SLURM_JOB_ID"
nvidia-smi --query-gpu=index,name --format=csv,noheader

# Use relax.in (clean QE input: cell+coords) not relax.out — ASE's espresso-out
# parser asserts on the incomplete/spin-polarized bands of the scancelled DFT+U
# run. relax.in holds the UMA-relaxed champion at v100; MLIP re-relaxes anyway
# so the EOS result is identical.
python3 -u uma_eos_pre_dft.py \
    --rank1-structure ./pair01_pair_00_reference_1_82/v100/relax.in \
    --rank2-structure ./pair02_pair_02_close_13_25/v100/relax.in \
    --out_dir ./uma_eos_tight_both

echo "=== DONE $(date) ==="
echo "Results: $WORK/uma_eos_tight_both/uma_eos_results.json"

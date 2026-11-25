#!/bin/bash
# b2o3_eos_kisti_short.sh — B2O3-doped DFT EOS on KISTI (Neuron, amd_a100nv_8).
# Short walltime (4 h) so SLURM backfill starts it fast; resume via resume_splice.py
# (last-coords injection) so a walltime kill continues instead of restarting.
# Submit a chain (QOS caps submit at 4):
#   jid=$(sbatch --parsable b2o3_eos_kisti_short.sh)
#   for i in 1 2 3; do jid=$(sbatch --parsable --dependency=afterany:$jid b2o3_eos_kisti_short.sh); done
# When all 6 volumes show "JOB DONE": python3 b2o3_eos_fit.py  -> BM3 B0 vs modelC 21.7.
#SBATCH -J llm_finetuning_v08
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:2
#SBATCH --time=04:00:00
#SBATCH -o logs/eos_%j.out
#SBATCH -e logs/eos_%j.err
#SBATCH --comment pytorch
BIN=/scratch/x3430a02/kgy/apps/qe-gpu/bin
source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh 2>/dev/null || true
conda activate uma 2>/dev/null || true
cd "$SLURM_SUBMIT_DIR"; mkdir -p logs
for f in eos_v0.96.in eos_v0.98.in eos_v1.00.in eos_v1.02.in eos_v1.04.in eos_v1.06.in; do
  [ -f "$f" ] || continue
  o="${f%.in}.out"
  if [ -f "$o" ] && grep -q "JOB DONE" "$o"; then echo "skip $f (JOB DONE)"; continue; fi
  [ -f "$o" ] && python3 resume_splice.py "$f" "$o"
  echo "=== $f  $(date) ==="
  mpirun -np 2 $BIN/pw.x -npool 2 -input "$f" > "$o" 2>&1 || echo "nonzero exit: $f"
done
echo "=== pass done $(date) ==="

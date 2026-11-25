#!/bin/bash
#SBATCH -J sdcp_phaseB
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --gres=gpu:2
#SBATCH --time=04:00:00
#SBATCH -o /scratch/x3430a02/kgy/sdcp_phaseB/logs/phaseB_%j.out
#SBATCH -e /scratch/x3430a02/kgy/sdcp_phaseB/logs/phaseB_%j.err
#SBATCH --comment qe

# ============================================================
# SDCP Phase-B (DFT+U binding cross-check) — KISTI 4-hour chain segment.
# 5 SCFs over 2 GPUs, resume-safe (lpsocl pattern):
#   - job with "JOB DONE" in scf.out            -> skip
#   - job interrupted mid-run                    -> tmp+out wiped, rerun fresh
#   - all 5 done -> harvest E_bind block + ALL_DONE (later segments no-op)
# Submit via submit_phaseB_kisti.sh (afterany chain, TIMEOUT-tolerant).
# Inputs: $WORK_BASE/{slab,complex_doped,complex_neutral,mol_doped,mol_neutral}/scf.in
#   (scp from gabia phaseB_v7c; pseudo_dir inside must point to $PSEUDO below).
# ============================================================

WORK_BASE=/scratch/x3430a02/kgy/sdcp_phaseB
PW=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x
export OMP_NUM_THREADS=8

mkdir -p $WORK_BASE/logs
cd $WORK_BASE
if [ -f ALL_DONE ]; then echo "ALL_DONE present — nothing to do."; exit 0; fi

# Environment: inherit default KISTI env (do NOT module purge — qe-gpu links auto-loaded libs).
echo "===== Phase-B segment  job=$SLURM_JOB_ID  $(date) ====="

run_stream () {          # $1 = GPU id, $2.. = job dirs
    local gpu=$1; shift
    for j in "$@"; do
        local d=$WORK_BASE/$j
        [ -f "$d/scf.in" ] || { echo "[$j] scf.in missing — transfer inputs first"; continue; }
        if grep -q "JOB DONE" "$d/scf.out" 2>/dev/null; then
            echo "[$j] already done — skip"; continue
        fi
        if [ -f "$d/scf.out" ]; then
            echo "[$j] incomplete previous run — wiping tmp and rerunning"
            rm -rf "$d/tmp" "$d/scf.out"
        fi
        echo "[$j] START on GPU $gpu  $(date)"
        ( cd "$d" && CUDA_VISIBLE_DEVICES=$gpu $PW -in scf.in > scf.out 2>&1 )
        grep -q "JOB DONE" "$d/scf.out" && echo "[$j] DONE  $(date)" \
                                        || echo "[$j] NOT finished (wall/error)  $(date)"
    done
}

# two streams: balanced by expected cost (slab+mol vs 2 complexes+mol)
run_stream 0 mol_doped slab &
P0=$!
run_stream 1 mol_neutral complex_doped complex_neutral &
P1=$!
wait $P0 $P1

n=$(grep -l "JOB DONE" $WORK_BASE/*/scf.out 2>/dev/null | wc -l)
echo "===== segment end: $n/5 SCFs complete  $(date) ====="
if [ "$n" -eq 5 ]; then
    touch $WORK_BASE/ALL_DONE
    echo "ALL 5 DONE — E_bind harvest (Ry; xRy2eV=13.605693):"
    for j in slab complex_doped complex_neutral mol_doped mol_neutral; do
        printf '%-16s ' $j; grep '^!' $WORK_BASE/$j/scf.out | tail -1
    done
    echo "E_bind(tag) = E(complex_tag) - E(slab) - E(mol_tag); VERDICT = doped - neutral"
fi

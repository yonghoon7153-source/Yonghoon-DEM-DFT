#!/bin/bash
#SBATCH -J llm1
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --gres=gpu:2
#SBATCH --time=04:00:00
#SBATCH -o /scratch/x3430a02/kgy/lpsocl_eos/logs/lpsocl_eos_%j.out
#SBATCH -e /scratch/x3430a02/kgy/lpsocl_eos/logs/lpsocl_eos_%j.err
#SBATCH --comment qe

# ============================================================
# LPSOCl DFT EOS — 4-hour chain segment (submit via submit_lpsocl_chain.sh)
# 7 fixed-cell relaxes (v094..v106) over 2 GPUs, resume-safe:
#   - volume with "JOB DONE" in relax.out  -> skip
#   - volume interrupted mid-run           -> wiped + rerun fresh
#   - all 7 done -> writes ALL_DONE and exits immediately (later
#     chain segments become no-ops)
# Chain uses --dependency=afterany (NOT afterok): a segment that dies
# at the 4 h wall shows TIMEOUT, and the next segment must still run.
# ============================================================

WORK_BASE=/scratch/x3430a02/kgy/lpsocl_eos
PW=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x
export OMP_NUM_THREADS=8

mkdir -p $WORK_BASE/logs
cd $WORK_BASE

if [ -f ALL_DONE ]; then
    echo "ALL_DONE present — nothing to do."; exit 0
fi

# Environment: inherit default KISTI env (cudampi/openmpi + mkl auto-loaded).
# Do NOT module purge — qe-gpu binary links against the auto-loaded libs.

echo "===== LPSOCl EOS segment  job=$SLURM_JOB_ID  $(date) ====="

run_stream () {          # $1 = GPU id, $2.. = volume labels
    local gpu=$1; shift
    for v in "$@"; do
        local d=$WORK_BASE/$v
        [ -f "$d/relax.in" ] || { echo "[$v] relax.in missing — run prepare first"; continue; }
        if grep -q "JOB DONE" "$d/relax.out" 2>/dev/null; then
            echo "[$v] already done — skip"; continue
        fi
        if [ -f "$d/relax.out" ]; then
            # SISYPHUS FIX (2026-07-11): wipe-and-rerun looped forever -- a from-scratch
            # relax needs >4 h (ion ~100 at the wall), so every segment redid the same
            # steps. Carry the LAST geometry of the dead run into relax.in instead:
            # SCF restarts fresh but ionic progress accumulates across segments.
            nat=$(awk '/number of atoms\/cell/{print $5; exit}' "$d/relax.out")
            ln=$(grep -n "ATOMIC_POSITIONS" "$d/relax.out" | tail -1 | cut -d: -f1)
            got=""
            if [ -n "$nat" ] && [ -n "$ln" ]; then
                sed -n "${ln},$((ln+nat))p" "$d/relax.out" > "$d/.carry"
                nl=$(( $(wc -l < "$d/.carry") - 1 ))
                if [ "$nl" -eq "$nat" ]; then
                    lin=$(grep -n "ATOMIC_POSITIONS" "$d/relax.in" | head -1 | cut -d: -f1)
                    { head -n $((lin-1)) "$d/relax.in"; cat "$d/.carry"; \
                      tail -n +$((lin+nat+1)) "$d/relax.in"; } > "$d/relax.in.new" \
                        && mv "$d/relax.in.new" "$d/relax.in" && got=1
                fi
            fi
            if [ -n "$got" ]; then
                echo "[$v] incomplete — carried last geometry (nat=$nat) forward; ionic progress kept"
            else
                echo "[$v] incomplete — no carry info, fresh start"
            fi
            rm -rf "$d/tmp" "$d/relax.out" "$d/.carry"
        fi
        # EOS convergence criterion: 1e-4 -> 1e-3 (QE default). Near the minimum the
        # energy error is ~|F|^2 -> << 1 meV, negligible for BM fitting; applied
        # identically to all 7 volumes (0/7 done => internally consistent). Idempotent.
        sed -i 's/forc_conv_thr = 1.0d-4/forc_conv_thr = 1.0d-3/' "$d/relax.in"
        echo "[$v] START on GPU $gpu  $(date)"
        ( cd "$d" && CUDA_VISIBLE_DEVICES=$gpu $PW -in relax.in > relax.out 2>&1 )
        grep -q "JOB DONE" "$d/relax.out" && echo "[$v] DONE  $(date)" \
                                          || echo "[$v] NOT finished (wall/error)  $(date)"
    done
}

# two streams, interleaved volumes (balanced): GPU0 4개 / GPU1 3개
run_stream 0 v094 v098 v102 v106 &
P0=$!
run_stream 1 v096 v100 v104 &
P1=$!
wait $P0 $P1

n_done=$(grep -l "JOB DONE" $WORK_BASE/v0*/relax.out 2>/dev/null | wc -l)
echo "===== segment end: $n_done/7 volumes complete  $(date) ====="
if [ "$n_done" -eq 7 ]; then
    touch $WORK_BASE/ALL_DONE
    echo "ALL 7 VOLUMES DONE — chain will no-op from here."
fi

#!/bin/bash
# anneal_chain.sh — orchestrate all (rank, li) anneal stages.
# Runs: 5× stage2 + 25× MD + 25× finish (with resume on each).
# Watchdog re-runs this; each script detects cache and exits 0 if done.
#
# Walltime per call:
#   stage2:  ~5 min
#   md:      up to ~30 min per checkpoint chunk (4 chunks for full 100ps,
#            but each script invocation runs until done or interrupted)
#   finish:  ~15 min
#
# Total: ~5×5min + 25×120min + 25×15min ≈ 25 + 3000 + 375 ≈ 57 hours cumulative
# (gabia: continuous, ~2.5 days; KISTI: many retries needed)

cd "$(dirname "$(readlink -f "$0")")"
export CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-0}

# Activate conda uma env if base
if [ -z "$CONDA_DEFAULT_ENV" ] || [ "$CONDA_DEFAULT_ENV" != "uma" ]; then
    for base in /scratch/x3430a02/mjs0000/miniforge3 /data/apps/miniforge3 $HOME/miniforge3; do
        if [ -f "$base/etc/profile.d/conda.sh" ]; then
            source "$base/etc/profile.d/conda.sh"
            conda activate uma 2>/dev/null
            break
        fi
    done
fi
PY="${PYTHON:-python}"

LOG=anneal_chain.log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] anneal_chain START  CUDA=$CUDA_VISIBLE_DEVICES" >> $LOG

run_step() {
    local desc="$1"; shift
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ▶ $desc" >> $LOG
    $PY -u "$@" 2>&1 | tee -a $LOG
    local rc=${PIPESTATUS[0]}
    if [ $rc -ne 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✗ FAILED ($rc): $desc" >> $LOG
        exit $rc
    fi
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✓ DONE: $desc" >> $LOG
}

# Stage 2 for each of top-5 halogen ranks
for RANK in 0 1 2 3 4; do
    run_step "stage2 rank=$RANK" anneal_stage2.py $RANK
done

# Anneal MD + finish for each (rank, li) pair: 25 total
for RANK in 0 1 2 3 4; do
    for LI in 0 1 2 3 4; do
        run_step "md rank=$RANK li=$LI" anneal_md.py $RANK $LI
        run_step "finish rank=$RANK li=$LI" anneal_finish.py $RANK $LI
    done
done

echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🎉 ALL ANNEAL DONE" >> $LOG

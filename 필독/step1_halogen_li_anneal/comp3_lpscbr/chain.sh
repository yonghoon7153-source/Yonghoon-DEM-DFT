#!/bin/bash
# comp3 v2 chain — runs all 11 stages sequentially.
# Each stage is INDEPENDENT (own python process). Exits if any stage fails
# (e.g., walltime SIGKILL). Watchdog re-runs this; cache resume picks up.
#
# Walltime budget per stage: < 90 min each (well under 2h KISTI limit).
# Total successful runtime ≈ stage1a 5min + 3×stage1b 60min + merge 1s
#                            + stage2 5min + 5×anneal_rank 50min each
#                          ≈ 5 + 60 + 5 + 250 = 320 min ≈ 5.5h cumulative
# If KISTI: 5-7 retries needed to chain through all stages.
cd "$(dirname "$(readlink -f "$0")")"

export CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-0}
PY="${PYTHON:-python3}"

# Sanity
$PY -c "import fairchem, pymatgen, ase" 2>/dev/null || {
    echo "ERROR: env not active"; exit 1
}

steps=(
    "comp3_v2_stage1a.py"
    "comp3_v2_stage1b.py 0"
    "comp3_v2_stage1b.py 1"
    "comp3_v2_stage1b.py 2"
    "comp3_v2_stage1b_merge.py"
    "comp3_v2_stage2.py"
    "anneal_rank.py 0"
    "anneal_rank.py 1"
    "anneal_rank.py 2"
    "anneal_rank.py 3"
    "anneal_rank.py 4"
)

LOG=chain.log
for step in "${steps[@]}"; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ▶ START: $step" | tee -a $LOG
    $PY -u $step 2>&1 | tee -a $LOG
    EXIT=${PIPESTATUS[0]}
    if [ $EXIT -ne 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✗ FAILED ($EXIT): $step" | tee -a $LOG
        exit $EXIT
    fi
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✓ DONE: $step" | tee -a $LOG
done
echo "[$(date '+%Y-%m-%d %H:%M:%S')] 🎉 ALL STAGES DONE" | tee -a $LOG

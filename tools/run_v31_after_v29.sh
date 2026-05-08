#!/bin/bash
# Wait for v29 AIMD to finish, summarize, then launch v31 MLIP elastic v2.
#
# Usage:
#   bash run_v31_after_v29.sh [V29_PID]
#
# If V29_PID not given, finds via pgrep.
#
# Run from /scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2/
# (or wherever phase2a_v29_results/ exists). Then launches v31 from
# /scratch/x3430a02/kgy/manuscript_support/ (where mlip_elastic_snapshot_v2.py lives).

set -e

# ───────────────── settings ─────────────────
V29_DIR="/scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2"
V31_DIR="/scratch/x3430a02/kgy/manuscript_support"
V29_LOG="$V29_DIR/phase2a_v29_results/run.log"
V31_URL="https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/claude/review-ml-migration-W29af/%ED%95%84%EB%8F%85/adhesion/phase2a_v31_mlip_elastic_v2_3comp.py"

V29_PID="${1:-}"
if [ -z "$V29_PID" ]; then
    V29_PID=$(pgrep -f "phase2a_v29_aimd_stability" | head -1)
fi

# ───────────────── wait for v29 ─────────────────
if [ -n "$V29_PID" ] && kill -0 "$V29_PID" 2>/dev/null; then
    echo "[$(date +%H:%M:%S)] v29 PID $V29_PID still running. Waiting..."
    while kill -0 "$V29_PID" 2>/dev/null; do
        # show last v29 log line every minute
        if [ -f "$V29_LOG" ]; then
            last=$(tail -1 "$V29_LOG")
            echo "  [$(date +%H:%M:%S)] $last"
        fi
        sleep 60
    done
    echo "[$(date +%H:%M:%S)] v29 PID $V29_PID exited."
else
    echo "[$(date +%H:%M:%S)] v29 PID not running (already done or not started)."
fi

# ───────────────── summarize v29 ─────────────────
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "v29 AIMD 1ps Stability Summary"
echo "═══════════════════════════════════════════════════════════════════"
if [ -f "$V29_LOG" ]; then
    grep -E "===|Final t=|VERDICT|comp" "$V29_LOG" | tail -50
else
    echo "  v29 log not found at $V29_LOG"
fi
echo ""
echo "─── Per-comp RMS verdict table ───"
grep -E "Final t=|VERDICT" "$V29_LOG" 2>/dev/null | paste - - | head -10
echo ""

# ───────────────── launch v31 ─────────────────
echo "═══════════════════════════════════════════════════════════════════"
echo "Launching v31 MLIP elastic 600K snapshot (v2 champions)"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

cd "$V31_DIR"
echo "[$(date +%H:%M:%S)] cd $V31_DIR"

# Fetch v31 if not present
if [ ! -f "phase2a_v31_mlip_elastic_v2_3comp.py" ]; then
    echo "[$(date +%H:%M:%S)] Fetching v31 script..."
    wget -q -O phase2a_v31_mlip_elastic_v2_3comp.py "$V31_URL"
fi

mkdir -p phase2a_v31_results

# Switch to mace env
echo "[$(date +%H:%M:%S)] activating mace env (script must be in mace conda env path)..."
source /scratch/x3430a02/mjs0000/miniforge3/etc/profile.d/conda.sh
conda activate mace

# Launch v31 in background (mace GPU)
nohup python3 phase2a_v31_mlip_elastic_v2_3comp.py \
    > phase2a_v31_results/run.log 2>&1 &
V31_PID=$!
echo "[$(date +%H:%M:%S)] v31 launched as PID $V31_PID"
echo "  log: $V31_DIR/phase2a_v31_results/run.log"
echo ""
echo "Watch with:"
echo "  tail -f $V31_DIR/phase2a_v31_results/run.log"
echo "Or:"
echo "  while true; do clear; python /tmp/watch_uma_mace.py; sleep 30; done"

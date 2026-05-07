#!/bin/bash
# watchdog_phase2a_v10.sh — auto-restart phase2a_v10_sandwich.py on crash
# Usage:
#   cd /scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2
#   nohup bash watchdog_phase2a_v10.sh > /dev/null 2>&1 &
#
# Stop:
#   pkill -f watchdog_phase2a_v10
#   pkill -f phase2a_v10_sandwich

cd /scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2

LOG=watchdog_phase2a_v10.log
RETRY=0
MAX_RETRY=20

while true; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] === phase2a v10 start (retry $RETRY) ===" >> "$LOG"
    CUDA_VISIBLE_DEVICES=1 python -u phase2a_v10_sandwich.py >> "$LOG" 2>&1
    EXIT=$?
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] === phase2a v10 exit code $EXIT ===" >> "$LOG"

    if [ $EXIT -eq 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] === phase2a v10 finished cleanly ===" >> "$LOG"
        break
    fi

    RETRY=$((RETRY + 1))
    if [ $RETRY -gt $MAX_RETRY ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] === too many retries ($MAX_RETRY), stop ===" >> "$LOG"
        break
    fi
    sleep 30
done

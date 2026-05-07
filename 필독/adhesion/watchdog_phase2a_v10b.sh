#!/bin/bash
# watchdog_phase2a_v10b.sh — auto-restart phase2a_v10b_sandwich_se_fixed.py on crash

cd /scratch/x3430a02/kgy/manuscript_support/adhesion_v5_v2

LOG=watchdog_phase2a_v10b.log
RETRY=0
MAX_RETRY=20

while true; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] === phase2a v10b start (retry $RETRY) ===" >> "$LOG"
    CUDA_VISIBLE_DEVICES=1 python -u phase2a_v10b_sandwich_se_fixed.py >> "$LOG" 2>&1
    EXIT=$?
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] === phase2a v10b exit code $EXIT ===" >> "$LOG"
    if [ $EXIT -eq 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] === phase2a v10b finished cleanly ===" >> "$LOG"
        break
    fi
    RETRY=$((RETRY + 1))
    if [ $RETRY -gt $MAX_RETRY ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] === too many retries ($MAX_RETRY), stop ===" >> "$LOG"
        break
    fi
    sleep 30
done

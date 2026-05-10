#!/bin/bash
source /data/apps/miniforge3/etc/profile.d/conda.sh
conda activate uma
cd /data/work/comp4_v2/1_step1to3

RETRIES=0
while [ $RETRIES -lt 50 ]; do
    echo "[$(date +%H:%M:%S)] === comp4 v2 start (retry $RETRIES) ===" >> watchdog.log
    python -u comp4_v2_step1to3.py >> run.log 2>&1
    EXIT=$?
    if [ $EXIT -eq 0 ]; then
        echo "[$(date +%H:%M:%S)] === comp4 v2 completed ===" >> watchdog.log
        break
    fi
    RETRIES=$((RETRIES+1))
    echo "[$(date +%H:%M:%S)] died exit=$EXIT, retry $RETRIES" >> watchdog.log
    sleep 30
done

#!/bin/bash
# comp5 v2 watchdog — KISTI GPU1
source /data/apps/miniforge3/etc/profile.d/conda.sh
conda activate uma
cd /data/work/comp5_v2/1_step1to3

export CUDA_VISIBLE_DEVICES=1  # GPU1 = comp5

RETRIES=0
while [ $RETRIES -lt 50 ]; do
    echo "[$(date +%H:%M:%S)] === comp5 v2 start (retry $RETRIES) ===" >> watchdog.log
    python -u comp5_v2_step1to3.py >> run.log 2>&1
    EXIT=$?
    if [ $EXIT -eq 0 ]; then
        echo "[$(date +%H:%M:%S)] === comp5 v2 completed ===" >> watchdog.log
        break
    fi
    RETRIES=$((RETRIES+1))
    echo "[$(date +%H:%M:%S)] died exit=$EXIT, retry $RETRIES" >> watchdog.log
    sleep 30
done

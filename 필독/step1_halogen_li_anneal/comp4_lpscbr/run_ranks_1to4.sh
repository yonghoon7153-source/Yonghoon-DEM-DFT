#!/bin/bash
cd /data/work/comp4_v2/1_step1to3
LOG=run_ranks_1to4.log
PYTHON=/data/apps/miniforge3/envs/uma/bin/python
for RANK in 1 2 3 4; do
    OUT="comp4_v2_rank${RANK}_results.json"
    if [ -f "$OUT" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] rank $RANK already done, skip" >> $LOG
        continue
    fi
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] === START rank $RANK ===" >> $LOG
    RETRY=0
    while [ ! -f "$OUT" ]; do
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] rank $RANK try $RETRY" >> $LOG
        $PYTHON -u anneal_rank.py $RANK >> $LOG 2>&1
        if [ -f "$OUT" ]; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] === DONE rank $RANK ===" >> $LOG
            break
        fi
        RETRY=$((RETRY+1))
        BACKOFF=$((2 ** (RETRY < 4 ? RETRY : 4)))
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] rank $RANK failed, sleep ${BACKOFF}s" >> $LOG
        sleep $BACKOFF
    done
done
echo "[$(date '+%Y-%m-%d %H:%M:%S')] === ALL RANKS DONE ===" >> $LOG

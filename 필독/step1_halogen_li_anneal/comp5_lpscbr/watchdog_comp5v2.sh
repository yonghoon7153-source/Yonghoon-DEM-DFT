#!/bin/bash
# comp5 v2 watchdog — portable (KISTI A100 GPU1, gabia, etc.)
# Run from any dir: nohup ./watchdog_comp5v2.sh > watchdog.out 2>&1 &
# Pre-req: conda env with fairchem/pymatgen/ase already active in parent shell.

cd "$(dirname "$(readlink -f "$0")")"   # cd to script's own directory

export CUDA_VISIBLE_DEVICES=${CUDA_VISIBLE_DEVICES:-1}   # default GPU1; override via env

# Sanity: env has required packages
python -c "import fairchem, pymatgen, ase" 2>/dev/null || {
    echo "ERROR: uma env not active (fairchem/pymatgen/ase missing). Activate first." | tee -a watchdog.log
    exit 1
}

RETRIES=0
while [ $RETRIES -lt 50 ]; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] === comp5 v2 start (retry $RETRIES, GPU=$CUDA_VISIBLE_DEVICES) ===" >> watchdog.log
    python -u comp5_v2_step1to3.py >> run.log 2>&1
    EXIT=$?
    if [ $EXIT -eq 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] === comp5 v2 completed ===" >> watchdog.log
        break
    fi
    RETRIES=$((RETRIES+1))
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] died exit=$EXIT, retry $RETRIES" >> watchdog.log
    sleep 30
done

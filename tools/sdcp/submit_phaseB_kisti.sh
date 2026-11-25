#!/bin/bash
# submit_phaseB_kisti.sh — submit N chained Phase-B segments (default 2; ~8 h budget).
#   bash submit_phaseB_kisti.sh [N]
# afterany (not afterok): a TIMEOUT segment must still trigger the next one.
# Resume-safe segments never redo completed SCFs (JOB DONE check inside).
# NOTE: QOSMaxSubmitJobPerUserLimit = 4 on this partition — count lpsocl jobs first
#   (squeue -u x3430a02) and submit only into free slots.
set -e
N=${1:-2}
HERE=$(cd "$(dirname "$0")" && pwd)
SEG=$HERE/sbatch_phaseB_kisti_chain.sh
mkdir -p /scratch/x3430a02/kgy/sdcp_phaseB/logs

jid=$(sbatch --parsable "$SEG")
echo "segment 1: job $jid"
for i in $(seq 2 "$N"); do
    jid=$(sbatch --parsable --dependency=afterany:$jid "$SEG")
    echo "segment $i: job $jid (afterany:previous)"
done
echo
echo "watch: squeue -u x3430a02 ; tail -f /scratch/x3430a02/kgy/sdcp_phaseB/logs/phaseB_*.out"

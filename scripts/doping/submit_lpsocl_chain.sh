#!/bin/bash
# submit_lpsocl_chain.sh — submit N chained 4-hour segments with dependencies.
#   bash submit_lpsocl_chain.sh [N]     (default N=6; ~24 h wall budget)
# afterany (not afterok): TIMEOUT segments must still trigger the next one.
# Completed work is never redone (JOB DONE check inside the segment script).
set -e
N=${1:-6}
HERE=$(cd "$(dirname "$0")" && pwd)
SEG=$HERE/sbatch_dft_eos_lpsocl_chain.sh
mkdir -p /scratch/x3430a02/kgy/lpsocl_eos/logs

jid=$(sbatch --parsable "$SEG")
echo "segment 1: job $jid"
for i in $(seq 2 "$N"); do
    jid=$(sbatch --parsable --dependency=afterany:$jid "$SEG")
    echo "segment $i: job $jid (afterany:previous)"
done
echo
echo "chain submitted. watch:  squeue -u x3430a02 ; tail -f /scratch/x3430a02/kgy/lpsocl_eos/logs/lpsocl_eos_*.out"

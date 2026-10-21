#!/bin/bash
# run a python probe in the probe folder: bash run_py.sh <probe.py> [args...]  -> <probe>.log (stdout+stderr), prints rc + log
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_mixer_d2
cd "$H" || exit 9
s="$1"; shift
log="$H/${s%.py}.log"
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 -I -B "$H/$s" "$@" > "$log" 2>&1
rc=$?
echo "rc=$rc"
cat "$log"
exit $rc

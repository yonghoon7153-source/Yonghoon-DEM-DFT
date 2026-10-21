#!/bin/bash
# usage: run1.sh <logname> <python args...>   (one BLAS thread · nice 19 · from the worktree)
W=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-afe53be7bdb176c82
L=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaD/logs
mkdir -p "$L"
name="$1"; shift
cd "$W" || exit 9
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
t0=$(date +%s)
nice -n 19 timeout 5400 python3 "$@" > "$L/$name.log" 2>&1
rc=$?
t1=$(date +%s)
echo "rc=$rc seconds=$((t1-t0))" >> "$L/$name.log"
echo "rc=$rc seconds=$((t1-t0))"

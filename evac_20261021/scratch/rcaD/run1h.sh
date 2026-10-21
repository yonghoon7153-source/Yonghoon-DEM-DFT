#!/bin/bash
# usage: run1h.sh <logname> <python args...>   — like run1.sh but through the machine-wide lock (heavy.sh: one heavy run at a time)
W=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-afe53be7bdb176c82
L=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaD/logs
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/heavy.sh
mkdir -p "$L"
name="$1"; shift
cd "$W" || exit 9
t0=$(date +%s)
bash "$H" timeout 5400 python3 "$@" > "$L/$name.log" 2>&1
rc=$?
t1=$(date +%s)
echo "rc=$rc seconds=$((t1-t0)) (incl. lock wait)" >> "$L/$name.log"
echo "rc=$rc seconds=$((t1-t0)) (incl. lock wait)"

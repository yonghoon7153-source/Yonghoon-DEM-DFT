#!/usr/bin/env bash
# Z1 regression — heavy tests one at a time after the main-tree gate window (≈ 21:00 UTC).
set -u
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a460741cfa90b5991
LOG=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/heavy
mkdir -p "$LOG"
until [ "$(date -u +%H%M)" -ge 2102 ]; do sleep 20; done
cd "$WT" || exit 9
run() {   # $1 = name, rest = command
  local name="$1"; shift
  local t0 t1 rc
  t0=$(date +%s)
  "$@" > "$LOG/$name.log" 2>&1
  rc=$?
  t1=$(date +%s)
  echo "$name rc=$rc seconds=$((t1 - t0)) start=$(date -u -d @"$t0" +%H:%M:%S)" >> "$LOG/summary.txt"
}
: > "$LOG/summary.txt"
run runner_full   python3 scripts/test_ca_ext_runner.py
run disc_selftest python3 scripts/check_method_discipline.py --selftest
run disc_noargs   python3 scripts/check_method_discipline.py
run verdict_full  python3 scripts/test_ca_ext_verdict.py
run b6_full       python3 scripts/test_ca_ext_b6.py
run z1_full       python3 scripts/test_ca_ext_z1.py
echo DONE >> "$LOG/summary.txt"

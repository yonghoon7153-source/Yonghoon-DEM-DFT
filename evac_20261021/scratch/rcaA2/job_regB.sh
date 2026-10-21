#!/bin/bash
# Re-run the old-scripts bit-identity cases (B / O) with a base archive that also carries docs/data/rint_eis_anchors.csv
# (the payload collector record reads <scripts>/../docs/data/rint_eis_anchors.csv — scripts-only archive = fallback branch).
L=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/logs/reg_B
mkdir -p $L
cd /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee || exit 9
OLD=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/old_a76/scripts
{ date; git rev-parse HEAD; git status --short; } > $L/_start.txt
S=$L/_summary.txt
: > $S
r() {
  local n=$1; shift
  local t0=$(date +%s)
  "$@" > $L/$n.log 2>&1
  local rc=$?
  echo "$n rc=$rc $(( $(date +%s) - t0 ))s | $(grep -E 'PASS|FAIL' $L/$n.log | tail -1 | cut -c1-200)" >> $S
}
r ptfe_face_alpha_B python3 -u scripts/test_ptfe_face_alpha.py --old-scripts $OLD --only B
r ca_ext_b6_B python3 -u scripts/test_ca_ext_b6.py --old-scripts $OLD --only B
r ca_ext_z3_O python3 -u scripts/test_ca_ext_z3.py --old-scripts $OLD --only O
date >> $L/_start.txt
echo done >> $S

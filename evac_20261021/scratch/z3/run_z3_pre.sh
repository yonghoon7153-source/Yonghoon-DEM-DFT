#!/bin/bash
# Z3 test on the BASE copy (pre-fix count) -> log.  The test file is copied into the base scripts/ so ROOT = base copy.
Z3=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/z3
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a19c109292d979c3e
cp "$WT/scripts/test_ca_ext_z3.py" "$Z3/base/scripts/test_ca_ext_z3.py" || exit 9
cd "$Z3/base" || exit 9
t0=$(date +%s)
nice -n 19 python3 scripts/test_ca_ext_z3.py > "$Z3/z3_pre_full.log" 2>&1
rc=$?
t1=$(date +%s)
echo "rc=$rc seconds=$((t1 - t0))" >> "$Z3/z3_pre_full.log"
rm -f "$Z3/base/scripts/test_ca_ext_z3.py"

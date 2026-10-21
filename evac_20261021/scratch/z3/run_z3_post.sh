#!/bin/bash
# Z3 full test on the fixed worktree (with --old-scripts base comparison) -> log
Z3=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/z3
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a19c109292d979c3e
cd "$WT" || exit 9
t0=$(date +%s)
nice -n 19 python3 scripts/test_ca_ext_z3.py --old-scripts "$Z3/base/scripts" > "$Z3/z3_post_full.log" 2>&1
rc=$?
t1=$(date +%s)
echo "rc=$rc seconds=$((t1 - t0))" >> "$Z3/z3_post_full.log"

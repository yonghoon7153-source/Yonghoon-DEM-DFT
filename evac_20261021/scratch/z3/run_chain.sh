#!/bin/bash
# test_rint_r_chain.py on the worktree -> log named by $1
Z3=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/z3
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a19c109292d979c3e
cd "$WT" || exit 9
t0=$(date +%s)
nice -n 19 python3 scripts/test_rint_r_chain.py "${@:2}" > "$Z3/chain_$1.log" 2>&1
rc=$?
t1=$(date +%s)
echo "rc=$rc seconds=$((t1 - t0))" >> "$Z3/chain_$1.log"

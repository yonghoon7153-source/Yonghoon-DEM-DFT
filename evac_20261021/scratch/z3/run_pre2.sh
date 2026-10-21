#!/bin/bash
# Second batch of pre-fix counts: ptfe_face_alpha (now copied), z3 (final test file), then the chain tests on the MID copy
# (new API code + base chain).
Z3=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/z3
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a19c109292d979c3e
rm -f "$Z3/pre2.done"
bash "$Z3/run_pre.sh" pfa test_ptfe_face_alpha.py
bash "$Z3/run_pre.sh" z3 test_ca_ext_z3.py
M="$Z3/mid"
for f in test_rint_r_chain.py test_rint_r_chain_e2e.py test_ca_ext_runner.py test_ca_ext_b6.py; do cp "$WT/scripts/$f" "$M/scripts/$f"; done
cd "$M" || exit 9
t0=$(date +%s); nice -n 19 python3 scripts/test_rint_r_chain.py > "$Z3/mid_chain.log" 2>&1; rc=$?; t1=$(date +%s)
echo "rc=$rc seconds=$((t1 - t0))" >> "$Z3/mid_chain.log"
t0=$(date +%s); nice -n 19 python3 scripts/test_rint_r_chain_e2e.py > "$Z3/mid_e2e.log" 2>&1; rc=$?; t1=$(date +%s)
echo "rc=$rc seconds=$((t1 - t0))" >> "$Z3/mid_e2e.log"
echo done > "$Z3/pre2.done"

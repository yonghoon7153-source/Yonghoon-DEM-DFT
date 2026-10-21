#!/bin/bash
# Run a NEW (worktree) test file against the BASE copy (pre-fix count).  The new test files listed in NEWTESTS are copied into
# the base scripts/ (base originals are backed up and restored afterwards), so the tests run against base code.
#   usage: run_pre.sh <name> <test file basename> [args...]
Z3=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/z3
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a19c109292d979c3e
B="$Z3/base/scripts"
NEWTESTS="test_rint_r_chain.py test_rint_r_chain_e2e.py test_ca_ext_z3.py test_ca_ext_runner.py test_ca_ext_b6.py test_carbon_junction.py test_ptfe_face_alpha.py"
name="$1"; shift
tf="$1"; shift
mkdir -p "$Z3/pre_bak"
for f in $NEWTESTS; do
  if [ -e "$B/$f" ]; then cp -p "$B/$f" "$Z3/pre_bak/$f"; fi
  cp "$WT/scripts/$f" "$B/$f"
done
cd "$Z3/base" || exit 9
t0=$(date +%s)
nice -n 19 python3 "scripts/$tf" "$@" > "$Z3/pre_$name.log" 2>&1
rc=$?
t1=$(date +%s)
echo "rc=$rc seconds=$((t1 - t0))" >> "$Z3/pre_$name.log"
for f in $NEWTESTS; do
  if [ -e "$Z3/pre_bak/$f" ]; then cp -p "$Z3/pre_bak/$f" "$B/$f"; rm -f "$Z3/pre_bak/$f"; else rm -f "$B/$f"; fi
done

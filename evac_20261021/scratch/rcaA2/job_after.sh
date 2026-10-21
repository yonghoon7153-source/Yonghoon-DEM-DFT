#!/bin/bash
# after (implementation in worktree) — the three changed test files.  Runs inside one heavy slot.
L=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/logs
T=${1:-after}
cd /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee || exit 9
{ date; git rev-parse HEAD; git status --short; sha256sum scripts/carbon_junction.py scripts/ca_ext_cjunc.py scripts/ca_s0_census.py scripts/step3_sigma.py scripts/test_carbon_junction.py scripts/test_ca_s0_census.py scripts/test_ca_ext_z3.py; } > $L/${T}_start.txt
python3 -u scripts/test_carbon_junction.py > $L/cj_$T.log 2>&1; echo "rc=$?" >> $L/cj_$T.log
python3 -u scripts/test_ca_s0_census.py > $L/s0_$T.log 2>&1; echo "rc=$?" >> $L/s0_$T.log
python3 -u scripts/test_ca_ext_z3.py --only A --skip-payload > $L/z3A_$T.log 2>&1; echo "rc=$?" >> $L/z3A_$T.log
date > $L/${T}_done.txt

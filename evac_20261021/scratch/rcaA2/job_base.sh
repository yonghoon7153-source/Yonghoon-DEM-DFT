#!/bin/bash
# base (a76f59d0d code) + new tests — pre-fix counts.  Runs inside one heavy slot.
L=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/logs
cd /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee || exit 9
date > $L/base_start.txt
git rev-parse HEAD >> $L/base_start.txt
git status --short >> $L/base_start.txt
sha256sum scripts/carbon_junction.py scripts/ca_ext_cjunc.py scripts/ca_s0_census.py scripts/step3_sigma.py scripts/test_carbon_junction.py scripts/test_ca_s0_census.py scripts/test_ca_ext_z3.py >> $L/base_start.txt
python3 -u scripts/test_carbon_junction.py > $L/cj_base.log 2>&1; echo "rc=$?" >> $L/cj_base.log
python3 -u scripts/test_ca_s0_census.py > $L/s0_base.log 2>&1; echo "rc=$?" >> $L/s0_base.log
python3 -u scripts/test_ca_ext_z3.py --only A --skip-payload > $L/z3A_base.log 2>&1; echo "rc=$?" >> $L/z3A_base.log
date > $L/base_done.txt

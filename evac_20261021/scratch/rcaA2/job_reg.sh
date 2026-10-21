#!/bin/bash
# regressions — one at a time inside one heavy slot · logs per test · summary file
L=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/logs/reg_${1:-r1}
mkdir -p $L
cd /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee || exit 9
OLD=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/old_a76/scripts
{ date; git rev-parse HEAD; git status --short; } > $L/_start.txt
S=$L/_summary.txt
: > $S
r() {  # name cmd...
  local n=$1; shift
  local t0=$(date +%s)
  "$@" > $L/$n.log 2>&1
  local rc=$?
  echo "$n rc=$rc $(( $(date +%s) - t0 ))s | $(grep -E 'PASS|FAIL|passed|failed|OK' $L/$n.log | tail -1 | cut -c1-200)" >> $S
}
r carbon_junction python3 -u scripts/test_carbon_junction.py
r ca_s0_census python3 -u scripts/test_ca_s0_census.py
r ptfe_face_alpha python3 -u scripts/test_ptfe_face_alpha.py --old-scripts $OLD
r ca_ext_b6 python3 -u scripts/test_ca_ext_b6.py --old-scripts $OLD
r ca_ext_runner python3 -u scripts/test_ca_ext_runner.py
r ca_ext_verdict python3 -u scripts/test_ca_ext_verdict.py
r ca_ext_z1 python3 -u scripts/test_ca_ext_z1.py
r ca_ext_z3 python3 -u scripts/test_ca_ext_z3.py --old-scripts $OLD
r rint_r_chain python3 -u scripts/test_rint_r_chain.py
r rint_r_chain_e2e python3 -u scripts/test_rint_r_chain_e2e.py
r step3_target_cert python3 -u scripts/test_step3_target_cert.py
r step3_conv_cert python3 -u scripts/test_step3_conv_cert.py
r rint_receipts python3 -u scripts/test_rint_receipts.py
r rint_g2_am_iface python3 -u scripts/test_rint_g2_am_iface.py
r step3_selftest python3 -u scripts/step3_sigma.py --selftest
r step3_selftest_rint python3 -u scripts/step3_sigma.py --selftest-rint
r run_contract_selftest python3 -u scripts/run_contract.py --selftest
r cmd_selftest python3 -u scripts/check_method_discipline.py --selftest
r cmd_repo python3 -u scripts/check_method_discipline.py
r webapp_ca_ext_labels python3 -u webapp/test_ca_ext_labels.py
r webapp_rint_scope_labels python3 -u webapp/test_rint_scope_labels.py
r webapp_rint_explainer python3 -u webapp/test_rint_explainer_page.py
date >> $L/_start.txt
echo done >> $S

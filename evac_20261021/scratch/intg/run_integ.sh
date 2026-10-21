#!/bin/bash
cd /home/user/wt_rintweb || exit 9
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
L=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/intg
OLD=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/s1/old/scripts
echo "HEAD $(git rev-parse --short HEAD) dirty=$(git status --short | wc -l)" > $L/summary.txt
run() { local name=$1; shift; local t0=$(date +%s); nice -n 19 timeout 2400 "$@" > $L/$name.log 2>&1; local rc=$?; local t1=$(date +%s); echo "$name rc=$rc t=$((t1-t0))s :: $(grep -E 'PASS|FAIL|passed|통과|실패' $L/$name.log | tail -1 | cut -c1-120)" >> $L/summary.txt; }
run cjunc python3 scripts/test_carbon_junction.py
run s0 python3 scripts/test_ca_s0_census.py
run target_cert python3 scripts/test_step3_target_cert.py
run s3_self python3 scripts/step3_sigma.py --selftest
run s3_rint python3 scripts/step3_sigma.py --selftest-rint
run contract python3 scripts/run_contract.py --selftest
run b6 python3 scripts/test_ca_ext_b6.py
run chain python3 scripts/test_rint_r_chain.py
run z3 python3 scripts/test_ca_ext_z3.py
run z1 python3 scripts/test_ca_ext_z1.py
run runner python3 scripts/test_ca_ext_runner.py
run verdict python3 scripts/test_ca_ext_verdict.py
run labels python3 webapp/test_ca_ext_labels.py
run explainer python3 webapp/test_rint_explainer_page.py
run e2e python3 scripts/test_rint_r_chain_e2e.py
run ptfe_old python3 scripts/test_ptfe_face_alpha.py --old-scripts $OLD
run conv_cert python3 scripts/test_step3_conv_cert.py
run join python3 scripts/test_rint_g2_join.py
run disc_self python3 scripts/check_method_discipline.py --selftest
run disc python3 scripts/check_method_discipline.py
echo DONE >> $L/summary.txt

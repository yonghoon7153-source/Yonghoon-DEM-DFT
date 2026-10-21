#!/bin/bash
# Final regression (D) — one command at a time through the machine-wide lock (run1h.sh → heavy.sh), logs in rcaD/logs/final_*.log
R=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaD/run1h.sh
S=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad
A76=$S/rcaD/base_a76/scripts
S1OLD=$S/s1/old/scripts
run() { local name="$1"; shift; echo "== $name: $(bash "$R" "final_$name" "$@") $(date -u +%H:%M:%S)"; }
run chain        scripts/test_rint_r_chain.py
run chain_e2e    scripts/test_rint_r_chain_e2e.py
run b6           scripts/test_ca_ext_b6.py
run b6_B_a76id   scripts/test_ca_ext_b6.py --only B --expect-identical --old-scripts "$A76"
run runner       scripts/test_ca_ext_runner.py
run runner_NB    scripts/test_ca_ext_runner.py --only NB --old-runner "$A76/sdcp_gain_vox015_8arm.sh"
run z1           scripts/test_ca_ext_z1.py
run z1_ZB        scripts/test_ca_ext_z1.py --only ZB --old-scripts "$A76"
run z3           scripts/test_ca_ext_z3.py
run z3_O_a76id   scripts/test_ca_ext_z3.py --only O --expect-identical --old-scripts "$A76"
run verdict      scripts/test_ca_ext_verdict.py
run verdict_V4   scripts/test_ca_ext_verdict.py --only V4 --old-verdict "$A76/sdcp_gain_verdict.py"
run cjunc        scripts/test_carbon_junction.py
run s0           scripts/test_ca_s0_census.py
run target_cert  scripts/test_step3_target_cert.py
run conv_cert    scripts/test_step3_conv_cert.py
run ptfe_fa      scripts/test_ptfe_face_alpha.py --old-scripts "$S1OLD"
run s3_selftest  scripts/step3_sigma.py --selftest
run s3_rint      scripts/step3_sigma.py --selftest-rint
run rc_selftest  scripts/run_contract.py --selftest
run web_labels   webapp/test_ca_ext_labels.py
run web_scope    webapp/test_rint_scope_labels.py
run cmd_selftest scripts/check_method_discipline.py --selftest
run cmd_noarg    scripts/check_method_discipline.py
echo "== reg_final done $(date -u +%H:%M:%S)"

#!/bin/bash
# Pre-fix counts of the updated / new API test files against the BASE copy (one at a time).
Z3=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/z3
bash "$Z3/run_pre.sh" z3 test_ca_ext_z3.py
bash "$Z3/run_pre.sh" cj test_carbon_junction.py
bash "$Z3/run_pre.sh" b6 test_ca_ext_b6.py
bash "$Z3/run_pre.sh" runner test_ca_ext_runner.py
bash "$Z3/run_pre.sh" pfa test_ptfe_face_alpha.py
echo done > "$Z3/pre_all.done"

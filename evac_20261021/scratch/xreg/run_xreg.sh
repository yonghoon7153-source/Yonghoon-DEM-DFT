#!/bin/bash
# X branch (aef62d81a) regression after container restart — run from the X worktree
cd /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a2f4c0688d2bafa5f || exit 9
echo "HEAD $(git rev-parse --short HEAD)  dirty=$(git status --porcelain | wc -l)"
run() { local name="$1"; shift; local t0=$(date +%s); timeout 3600 "$@" > /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/xreg/$name.log 2>&1; local rc=$?; local t1=$(date +%s); echo "$name rc=$rc t=$((t1-t0))s :: $(tail -n 2 /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/xreg/$name.log | tr '\n' ' ' | cut -c1-220)"; }
run cjunc python3 -B scripts/test_carbon_junction.py
run s0 python3 -B scripts/test_ca_s0_census.py
run labels python3 -B webapp/test_ca_ext_labels.py
run st3 python3 -B scripts/step3_sigma.py --selftest
run st3rint python3 -B scripts/step3_sigma.py --selftest-rint
run cmd_self python3 -B scripts/check_method_discipline.py --selftest
run cmd_repo python3 -B scripts/check_method_discipline.py
run ptfe python3 -B scripts/test_ptfe_face_alpha.py
echo DONE

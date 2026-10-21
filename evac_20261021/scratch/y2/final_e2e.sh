#!/usr/bin/env bash
# 최종 회귀 — 끝-끝 셋 (기본 호출 = check_all 과 같은 꼴 · 시간 측정) + 옛 코드 대조 (b6 B · runner NB · verdict V4b)
SP=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/y2
T=$SP/timed.sh
cd /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1a2386b8dc655b22 || exit 9
bash $T $SP/fin_b6.log python3 scripts/test_ca_ext_b6.py
bash $T $SP/fin_runner.log python3 scripts/test_ca_ext_runner.py
bash $T $SP/fin_verdict.log python3 scripts/test_ca_ext_verdict.py
bash $T $SP/fin_labels.log python3 webapp/test_ca_ext_labels.py
bash $T $SP/fin_b6_old.log python3 scripts/test_ca_ext_b6.py --old-scripts $SP/prefix/scripts --only B
bash $T $SP/fin_runner_nb.log python3 scripts/test_ca_ext_runner.py --only NB --old-runner $SP/old_runner.sh
bash $T $SP/fin_verdict_old.log python3 scripts/test_ca_ext_verdict.py --only V4 --old-verdict $SP/old_verdict.py
echo DONE

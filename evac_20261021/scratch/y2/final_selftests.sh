#!/usr/bin/env bash
SP=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/y2
T=$SP/timed.sh
cd /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1a2386b8dc655b22 || exit 9
bash $T $SP/fs_rc.log python3 scripts/run_contract.py --selftest
bash $T $SP/fs_verdict.log python3 scripts/sdcp_gain_verdict.py --selftest
bash $T $SP/fs_sr01.log python3 scripts/sr01_stamp_compare.py --selftest
bash $T $SP/fs_s3.log python3 scripts/step3_sigma.py --selftest
bash $T $SP/fs_cmd_self.log python3 scripts/check_method_discipline.py --selftest &
bash $T $SP/fs_cmd_noarg.log python3 scripts/check_method_discipline.py &
wait
echo DONE

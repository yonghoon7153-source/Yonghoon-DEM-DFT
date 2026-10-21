#!/bin/bash
# Heavy "before" runs on the snapshot (unfixed code + new tests): smoke selftest, launcher test.
S=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/mxd2fix
cd "$S/snap_before" || exit 9
bash "$S/timed.sh" "$S/before_smoke_selftest.log" python3 -B scripts/mixer_smoke_blind.py --selftest
bash "$S/timed.sh" "$S/before_launcher.log" bash dem_scripts/mixer_20260921/test_launcher.sh
echo HEAVY_BEFORE_DONE

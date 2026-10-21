#!/bin/bash
# recheck 10-21: default-off byte identity of the fixed generator (gen/mmd_FIX.py = 9412f384a) vs preD2 and vs old HEAD (a76f59d0d)
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_mixer_d2
cd "$H" || exit 9
echo "== preD2 vs FIX"; date
python3 -I -B "$H/probe_byteident_fix.py" mmd_preD2.py mmd_FIX.py probe_byteident_fix_preD2.json
echo "rc=$?"; date
echo "== HEAD(a76f59d0d) vs FIX"
python3 -I -B "$H/probe_byteident_fix.py" mmd_HEAD.py mmd_FIX.py probe_byteident_fix_HEAD.json
echo "rc=$?"; date

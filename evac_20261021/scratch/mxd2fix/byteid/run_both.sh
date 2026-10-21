#!/bin/bash
# Default-path byte identity of the fixed generator: (1) HEAD 055ddd04e generator vs fixed · (2) pre-D2 generator vs fixed.
B=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/mxd2fix/byteid
cd "$B" || exit 9
python3 -I -B "$B/probe_byteident_after.py" "$B/gen/mmd_HEAD.py" "$B/gen/mmd_FIX.py" "$B/byteident_HEAD_vs_FIX.json" > "$B/byteident_HEAD_vs_FIX.log" 2>&1
echo "HEAD_vs_FIX rc=$?"
python3 -I -B "$B/probe_byteident_after.py" "$B/gen/mmd_preD2.py" "$B/gen/mmd_FIX.py" "$B/byteident_preD2_vs_FIX.json" > "$B/byteident_preD2_vs_FIX.log" 2>&1
echo "preD2_vs_FIX rc=$?"

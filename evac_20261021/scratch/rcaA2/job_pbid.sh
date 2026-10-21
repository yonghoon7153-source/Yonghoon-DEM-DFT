#!/bin/bash
D=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2
cd /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee || exit 9
python3 $D/payload_bitid.py $D/logs/payload_bitid.json > $D/logs/payload_bitid.log 2>&1
echo "rc=$?" >> $D/logs/payload_bitid.log

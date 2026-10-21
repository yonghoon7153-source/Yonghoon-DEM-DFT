#!/bin/bash
# usage: run_cj.sh <log> [test args...]   — runs test_carbon_junction.py through heavy.sh from the A2 worktree
LOG=$1; shift
cd /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee || exit 9
bash /tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/heavy.sh python3 scripts/test_carbon_junction.py "$@" > "$LOG" 2>&1
echo "rc=$?" >> "$LOG"

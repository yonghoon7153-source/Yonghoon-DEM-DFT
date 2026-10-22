#!/bin/bash
# 사슬 시험 (작업 트리 93d93bc02) — 인자 = --only 접두 (없으면 전체)
cd /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a388f740a6ce4524d || exit 9
if [ -n "$1" ]; then
  python3 -I scripts/test_rint_r_chain.py --only "$1"
else
  python3 -I scripts/test_rint_r_chain.py
fi

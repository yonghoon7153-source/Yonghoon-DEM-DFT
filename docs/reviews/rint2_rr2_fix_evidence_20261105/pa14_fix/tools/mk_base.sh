#!/bin/bash
# 바탕 뿌리 (사슬 · 시험 = 바탕 379e85856 그대로 = 사전 공격 14 대상과 같은 blob) — base_tree/scripts (탐침 고치기 전)
set -eu
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/pa14fix
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a271b07eec3fe5332
python3 "$H/tools/mktree.py" "$WT" "$H/base_tree" "$H/base/rint_r_chain.py" "$H/base/test_rint_r_chain.py"
sha256sum "$H/base_tree/scripts/rint_r_chain.py" "$H/base_tree/scripts/test_rint_r_chain.py"

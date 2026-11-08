#!/bin/bash
# 끝-끝 (3.11) → kgy 판 3.8 (`scripts/check_kgy_py38.sh` · 11 묶음) 차례로 — 로그 = logs/e2e_py311.log · logs/check_kgy_py38.log · logs/py38/
set -u
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/pa14fix
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a271b07eec3fe5332
mkdir -p "$H/logs/py38"
cd "$WT" || exit 9
sha256sum scripts/rint_r_chain.py scripts/test_rint_r_chain.py > "$H/logs/e2e_py38_code_sha.txt"
python3 scripts/test_rint_r_chain_e2e.py > "$H/logs/e2e_py311.log" 2>&1
echo "rc=$?" >> "$H/logs/e2e_py311.log"
KGY_PY38_LOGDIR="$H/logs/py38" bash scripts/check_kgy_py38.sh > "$H/logs/check_kgy_py38.log" 2>&1
echo "rc=$?" >> "$H/logs/check_kgy_py38.log"

#!/usr/bin/env bash
# 한 줄 재실행: worktree(1049894) 재생성 → 전부 재현 → run_all.log → worktree 제거
set -u; S="$(cd "$(dirname "$0")" && pwd)"; REPO="${REPO:-/home/user/Yonghoon-DEM-DFT}"
[ -d "$S/wt" ] && git -C "$REPO" worktree remove --force "$S/wt"
git -C "$REPO" worktree add --detach "$S/wt" 1049894 >/dev/null 2>&1 || exit 1
( cd "$S" && python3 verify_toctou.py all > run_all.log 2>&1 ); rc=$?
( cd "$S/wt/bms-balancing" && python3 -m pytest tests/ -q -k "r5_04 or r4_06 or r5_08 or r5_05" 2>&1 | tail -1 ) >> "$S/run_all.log"
git -C "$REPO" worktree remove --force "$S/wt"; echo "rc=$rc → $S/run_all.log"

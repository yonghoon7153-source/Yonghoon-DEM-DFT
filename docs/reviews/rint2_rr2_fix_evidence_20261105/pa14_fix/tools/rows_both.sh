#!/bin/bash
# PA14 행 표 — 고치기 전 (사슬 = 바탕 · 시험 = 시험 먼저 판 · before_tree) · 고친 뒤 (작업 트리) → logs/pa14_rows_{before,after}.json + 요약
set -u
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/pa14fix
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a271b07eec3fe5332
mkdir -p "$H/tmp" "$H/logs"
cd "$H/tmp" || exit 9
PA14FIX_SCRIPTS="$H/before_tree/scripts" TMPDIR="$H/tmp" python3 "$H/tools/rows_dump.py" PA14 > "$H/logs/pa14_rows_before.json"
echo "before rc=$?"
PA14FIX_SCRIPTS="$WT/scripts" TMPDIR="$H/tmp" python3 "$H/tools/rows_dump.py" PA14 > "$H/logs/pa14_rows_after.json"
echo "after rc=$?"
echo "== 고치기 전"
python3 "$H/tools/rows_summary.py" "$H/logs/pa14_rows_before.json"
echo "== 고친 뒤"
python3 "$H/tools/rows_summary.py" "$H/logs/pa14_rows_after.json"

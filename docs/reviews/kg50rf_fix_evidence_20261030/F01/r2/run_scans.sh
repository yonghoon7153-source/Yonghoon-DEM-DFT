#!/bin/bash
# 실제 덱 조사 넷 → logs/ (비 ASCII · CR · & 꼴 · $ 자리 · 흐름 줄 자리 · 펼친 글 최대 길이) — 도구는 읽기만
W=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/f01r2
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-ac3f433b81b4e211e
cd "$WT" || exit 1
python3 -I "$W/scan_decks.py" "$WT" > "$W/logs/scan_decks.log" 2>&1
python3 -I "$W/scan_keys.py" "$WT" > "$W/logs/scan_keys.log" 2>&1
python3 -I "$W/scan_flow.py" "$WT" > "$W/logs/scan_flow.log" 2>&1
python3 -I "$W/measure_xlen.py" "$WT" scripts/resume_ckpt.sh > "$W/logs/measure_xlen.log" 2>&1
wc -l "$W"/logs/scan_*.log "$W/logs/measure_xlen.log"

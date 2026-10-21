#!/bin/bash
# P10 — Codex 10-20 S02 탐침 (묶음 밖 사본 · 경로 상수만) 을 HEAD 작업 트리에서 다시 · 네 모드 (sweep 제외 — 10-20 재현과 같은 범위)
# 재실행: cd <worktree> && bash <SCRATCH>/heavy.sh bash p10_s02.sh <SCRATCH>/prereview_lhs214/s02
D=$1
for m in core axis mutants failclosed; do
  s=$(date +%s)
  python3 -I -X utf8 -B "$D/copy/probes/s02/adversary.py" "$m" > "$D/$m.stdout" 2> "$D/$m.stderr"
  echo "$m rc=$? secs=$(( $(date +%s) - s ))"
done

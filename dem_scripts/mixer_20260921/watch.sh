#!/usr/bin/env bash
# 진행 감시 — 런별 스텝/총스텝(%) · 덤프 수 · 상태.   사용: bash dem_scripts/mixer_20260921/watch.sh
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; OUT="${OUT:-$ROOT/dem_scripts/mixer_20260921/runs}"
printf '%-14s %-6s %12s %7s %6s  %s\n' 런 상태 step 진행 덤프 마지막
for d in "$OUT"/*_s*/; do
  nm=$(basename "$d"); log="$d/log.lmp"
  tot=$(grep -oE '^run +[0-9]+' "$d/in.mixer" | awk '{s+=$2} END{print s}')
  if [ ! -f "$log" ]; then st=대기; step=-; pct=-
  elif grep -q "Total wall time" "$log"; then st=완료; step=$tot; pct=100%
  elif [ -f "$d/pid" ] && kill -0 "$(cat "$d/pid")" 2>/dev/null; then st=실행; step=$(grep -E '^ +[0-9]+ +[0-9]+ ' "$log" | tail -1 | awk '{print $1}'); pct=$(( ${step:-0} * 100 / tot ))%
  else st="⛔죽음"; step=$(grep -E '^ +[0-9]+ +[0-9]+ ' "$log" | tail -1 | awk '{print $1}'); pct=$(( ${step:-0} * 100 / tot ))%; fi
  nd=$(ls "$d"/post 2>/dev/null | wc -l)
  printf '%-14s %-6s %12s %7s %6s  %s\n' "$nm" "$st" "${step:--}" "$pct" "$nd" "$(tail -c 60 "$log" 2>/dev/null | tr '\n' ' ')"
done

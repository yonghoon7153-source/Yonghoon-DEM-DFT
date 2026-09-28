#!/usr/bin/env bash
# 진행 감시 — 런별 스텝/총스텝(%) · 덤프 수 · 상태.   사용: bash dem_scripts/mixer_20260921/watch.sh
# ★ 2026-09-22 — 완주 판정은 run_all.sh 와 같다: 배너 `Total wall time` **또는** 마지막 step ≥ run 합.
#   `완료*` = 배너 없이 마지막 step 에 닿은 런 (새 덱의 종료 결함 — 덤프·settled.bin 무사).  옛 판은
#   이것을 `⛔죽음 100%` 로 찍어 "죽었다" 로 읽혔다.
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; OUT="${OUT:-$ROOT/dem_scripts/mixer_20260921/runs}"
#  ★ 2026-09-28 밤 — SLURM 판 (ibb) 런은 pid 가 없고 <런>/jobid 만 있다.  옛 판은 pid 로만 '실행' 을 판정해 살아 있는 SLURM 런을
#    ⛔죽음 으로 찍었다 (test_launcher.sh HW①–②).  이제 jobid 가 대기열 (squeue) 에 있으면 실행이다.
Q=$(command -v squeue >/dev/null 2>&1 && squeue -h -o %i 2>/dev/null)
printf '%-14s %-6s %12s %7s %6s  %s\n' 런 상태 step 진행 덤프 마지막
for d in "$OUT"/*_s*/; do
  d="${d%/}"; nm=$(basename "$d"); log="$d/log.lmp"
  tot=$(grep -oE '^run +[0-9]+' "$d/in.mixer" 2>/dev/null | awk '{s+=$2} END{print s+0}')
  last=$(grep -E '^ +[0-9]+ +[0-9]+ ' "$log" 2>/dev/null | tail -1 | awk '{print $1+0}')
  pct() { if [ "${tot:-0}" -gt 0 ]; then echo "$(( ${1:-0} * 100 / tot ))%"; else echo "-"; fi; }
  if [ ! -f "$log" ]; then st=대기; step=-; p=-
  elif grep -q "Total wall time" "$log"; then st=완료; step=$tot; p=100%
  elif [ "${tot:-0}" -gt 0 ] && [ "${last:-0}" -ge "$tot" ]; then st='완료*'; step=$last; p=100%
  elif [ -f "$d/pid" ] && kill -0 "$(cat "$d/pid")" 2>/dev/null; then st=실행; step=$last; p=$(pct "$last")
  elif [ -s "$d/jobid" ] && grep -qxF "$(cat "$d/jobid")" <<<"$Q"; then st=실행; step=$last; p=$(pct "$last")
  else st="⛔죽음"; step=$last; p=$(pct "$last"); fi
  nd=$(ls "$d"/post 2>/dev/null | wc -l)
  printf '%-14s %-6s %12s %7s %6s  %s\n' "$nm" "$st" "${step:--}" "$p" "$nd" "$(tail -c 60 "$log" 2>/dev/null | tr '\n' ' ')"
done

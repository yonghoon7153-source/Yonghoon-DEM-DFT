#!/usr/bin/env bash
# 캠페인 실행 — 런마다 **np=1 직렬**, 여러 개를 **동시에** 띄운다 (MPI 효율 걱정 없음).
# 사용:  LMP=lmp_auto MAXJ=10 bash dem_scripts/mixer_20260921/run_all.sh
#   LMP  = LIGGGHTS 실행 파일 (기본 lmp_auto)   MAXJ = 동시 실행 수 (기본 = 코어 수)
# ⚠ 정지는 **PID 로만**: kill $(cat runs/<런>/pid)   — pkill -f 금지 (규약)
set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
OUT="${OUT:-$ROOT/dem_scripts/mixer_20260921/runs}"
LMP="${LMP:-lmp_auto}"; MAXJ="${MAXJ:-$(nproc)}"
command -v "$LMP" >/dev/null || { echo "⛔ $LMP 없음 — LMP=<실행파일> 로 지정"; exit 1; }
live() { local c=0; for f in "$OUT"/*_s*/pid; do [ -f "$f" ] && kill -0 "$(cat "$f")" 2>/dev/null && c=$((c+1)); done; echo $c; }
n=0
for d in "$OUT"/*_s*/; do
  [ -f "$d/in.mixer" ] || continue
  if [ -f "$d/pid" ] && kill -0 "$(cat "$d/pid")" 2>/dev/null; then echo "· 이미 실행 중: $d"; continue; fi
  if [ -f "$d/log.lmp" ] && grep -q "Total wall time" "$d/log.lmp"; then echo "· 완료됨: $d"; continue; fi
  #  ★ 동시 상한 — pid 파일 + kill -0 로 **살아 있는 lmp 만** 센다 (리뷰 R-14: `jobs -rp` 는 서브셸이
  #    바로 끝나 무효였다)
  while [ "$(live)" -ge "$MAXJ" ]; do sleep 30; done
  ( cd "$d" && setsid nohup "$LMP" -in in.mixer > log.lmp 2>&1 & echo $! > pid )
  n=$((n+1)); echo "▶ 시작 $(basename "$d")  pid $(cat "$d/pid")  (동시 $(live)/$MAXJ)"
  sleep 2
done
echo "런처 종료 — 시작한 런 $n 개.  진행은 watch.sh"

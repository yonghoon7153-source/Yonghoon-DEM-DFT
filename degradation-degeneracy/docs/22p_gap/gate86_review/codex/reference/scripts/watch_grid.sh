#!/usr/bin/env bash
# =============================================================================
#  watch_grid.sh — 백그라운드 grid 실행 모니터링
#
#  사용:
#    ./scripts/watch_grid.sh                                  # 기본값 사용
#    ./scripts/watch_grid.sh results/grid_fine_v1 grid_fine.log
#    watch -n 5 ./scripts/watch_grid.sh                       # 5초마다 갱신
#
#  detach 실행 예 (SSH 끊겨도 살아남음):
#    setsid nohup ./run.sh --mode grid --config configs/grid_fine.yaml \
#      --nproc 32 --resume --out results/grid_fine_v1 > grid_fine.log 2>&1 < /dev/null &
#    disown
# =============================================================================
set -uo pipefail

RUN_DIR="${1:-results/grid_fine_v1}"
LOG="${2:-grid_fine.log}"

hr() { printf '%s\n' "────────────────────────────────────────────────"; }

hr
printf '%s   run=%s\n' "$(date '+%F %T')" "$RUN_DIR"
hr

# ── 프로세스 ──
MAIN="$(pgrep -f 'src\.grid' | head -1)"
WORKERS="$(pgrep -cf loky 2>/dev/null || echo 0)"
if [[ -n "$MAIN" ]]; then
  ELAPSED="$(ps -o etime= -p "$MAIN" 2>/dev/null | tr -d ' ')"
  printf '실행중  PID %s   워커 %s개   경과 %s\n' "$MAIN" "$WORKERS" "${ELAPSED:-?}"
else
  printf '프로세스 없음 — 완료했거나 죽었음 (아래 로그 끝 확인)\n'
fi

# ── 진행률 (tqdm 마지막 줄) ──
if [[ -f "$LOG" ]]; then
  BAR="$(tr '\r' '\n' < "$LOG" | grep -o 'grid: .*' | tail -1)"
  [[ -n "$BAR" ]] && printf '%s\n' "$BAR"
fi

# ── 저장 상태 ──
CHUNKS=$(ls "$RUN_DIR/chunks" 2>/dev/null | wc -l)
DONE=$(wc -l < "$RUN_DIR/completed.jsonl" 2>/dev/null || echo 0)
FAILED=$(($(wc -l < "$RUN_DIR/failed.csv" 2>/dev/null || echo 1) - 1))
printf '청크 %s개   완료(누적) %s조건   failed.csv %s행\n' "$CHUNKS" "$DONE" "$FAILED"

# ── 자원 ──
if command -v free >/dev/null; then
  free -g | awk 'NR==2 {printf "메모리 %s/%s GB 사용\n", $3, $2}'
fi
awk '{printf "load average %s %s %s\n", $1, $2, $3}' /proc/loadavg 2>/dev/null

# ── 최근 경고/에러 (tqdm·정상 경고 제외) ──
if [[ -f "$LOG" ]]; then
  ERR="$(tr '\r' '\n' < "$LOG" \
        | grep -E 'ERROR|Traceback|CRITICAL' \
        | tail -3)"
  if [[ -n "$ERR" ]]; then
    hr; printf '최근 에러:\n%s\n' "$ERR"
  fi
fi

# ── 완료 시 요약 ──
if [[ -z "$MAIN" && -f "$RUN_DIR/manifest.yaml" ]]; then
  hr
  grep -E '^(n_ok|n_failed|n_curves_total|n_failed_total|elapsed_s|finished):' \
       "$RUN_DIR/manifest.yaml" 2>/dev/null || true
fi

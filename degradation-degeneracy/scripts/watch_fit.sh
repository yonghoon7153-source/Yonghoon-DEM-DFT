#!/usr/bin/env bash
# =============================================================================
#  watch_fit.sh — 백그라운드 fitting 실행 모니터링
#
#  사용:
#    ./scripts/watch_fit.sh                              # 기본 grid_fine_v1
#    ./scripts/watch_fit.sh results/grid_fine_v1 fit.log
#    watch -n 60 ./scripts/watch_fit.sh                  # 1분마다 갱신
#
#  ★ 진행 속도는 **최근 청크 3개**로 잰다. 평균을 쓰면 초반 저속 구간
#    (CPU 경합·워커 기동)이 섞여 ETA가 실제보다 늦게 나온다.
#
#  ★ src.fitting 프로세스가 2개 이상이면 크게 경고한다.
#    2026-08-06에 같은 --out에 두 개가 붙어 CPU를 반씩 나눠 쓰고, 먼저 뜬
#    쪽은 재생성 이전의 옛 곡선으로 청크를 쌓은 사고가 있었다 (F19).
# =============================================================================
set -uo pipefail

RUN_DIR="${1:-results/grid_fine_v1}"
LOG="${2:-}"
CHUNK_SIZE=100          # src/fitting.py: step = min(100, len(todo))

hr() { printf '%s\n' "────────────────────────────────────────────────────"; }

hr
printf '%s   run=%s\n' "$(date '+%F %T')" "$RUN_DIR"
hr

# ── 프로세스 ──────────────────────────────────────────────────────────
mapfile -t PIDS < <(pgrep -f 'src\.fitting' 2>/dev/null)
if [[ ${#PIDS[@]} -eq 0 ]]; then
  printf '프로세스 없음 — 완료했거나 죽었음\n'
elif [[ ${#PIDS[@]} -gt 1 ]]; then
  printf '\n!!! 경고: src.fitting 프로세스가 %d개다 !!!\n' "${#PIDS[@]}"
  printf '같은 --out에 둘이 붙으면 CPU를 나눠 쓰고 청크가 서로 덮인다.\n'
  printf '시작 시각이 curves.parquet 재생성보다 이른 쪽을 죽일 것:\n\n'
  ps -o pid,lstart,etime -p "$(IFS=,; echo "${PIDS[*]}")" 2>/dev/null
  printf '\ncurves.parquet: '; stat -c '%y' "$RUN_DIR/curves.parquet" 2>/dev/null
  printf '\n'
else
  WORKERS=$(pgrep -cf loky 2>/dev/null || echo 0)
  printf '실행중  PID %s   워커 %s개   경과 %s\n' \
    "${PIDS[0]}" "$WORKERS" "$(ps -o etime= -p "${PIDS[0]}" 2>/dev/null | tr -d ' ')"
fi

# ── 진행률 ────────────────────────────────────────────────────────────
shopt -s nullglob
CH=("$RUN_DIR"/fit_chunks/*.parquet)
shopt -u nullglob
N=${#CH[@]}

# 완료 조건 수는 fit_completed_*.jsonl 이 정확하다 (청크×100은 마지막이 잘림)
DONE=0
shopt -s nullglob
FC=("$RUN_DIR"/fit_completed_*.jsonl)
shopt -u nullglob
[[ ${#FC[@]} -gt 0 ]] && DONE=$(sort -u "${FC[@]}" | wc -l)

# 전체 조건 수: 로그의 "fitting: N조건" 이 정답. 없으면 grid 성공 수로 근사.
TOTAL=0
if [[ -n "$LOG" && -f "$LOG" ]]; then
  TOTAL=$(tr '\r' '\n' < "$LOG" | grep -oP 'fitting: \K[0-9]+(?=조건)' | tail -1)
  TOTAL=${TOTAL:-0}
fi
APPROX=""
if [[ $TOTAL -eq 0 && -f "$RUN_DIR/completed.jsonl" ]]; then
  TOTAL=$(sort -u "$RUN_DIR/completed.jsonl" | wc -l)
  APPROX=" (근사 — 로그 인자를 주면 정확해짐)"
fi
NCHUNK=$(( TOTAL > 0 ? (TOTAL + CHUNK_SIZE - 1) / CHUNK_SIZE : 0 ))

if [[ $NCHUNK -gt 0 ]]; then
  printf '청크 %d / %d   조건 %d / %d (%d%%)%s\n' \
    "$N" "$NCHUNK" "$DONE" "$TOTAL" $(( 100 * DONE / TOTAL )) "$APPROX"
else
  printf '청크 %d개   조건 %d개 완료   (전체 수 미상)\n' "$N" "$DONE"
fi

# ── 속도·ETA — 최근 3청크 기준 ────────────────────────────────────────
if [[ $N -ge 2 ]]; then
  mapfile -t RECENT < <(ls -tr "$RUN_DIR"/fit_chunks/*.parquet | tail -4)
  T0=$(stat -c %Y "${RECENT[0]}")
  T1=$(stat -c %Y "${RECENT[-1]}")
  SPAN=$(( ${#RECENT[@]} - 1 ))
  if [[ $SPAN -gt 0 && $T1 -gt $T0 ]]; then
    RATE=$(( (T1 - T0) / SPAN ))
    printf '최근 속도 %d분 %02d초/청크' $(( RATE / 60 )) $(( RATE % 60 ))
    if [[ $NCHUNK -gt $N ]]; then
      REMAIN=$(( (NCHUNK - N) * RATE ))
      # 마지막 청크 이후 경과분을 빼서 ETA가 갱신되게
      SINCE=$(( $(date +%s) - T1 ))
      [[ $SINCE -lt $REMAIN ]] && REMAIN=$(( REMAIN - SINCE ))
      printf '   남은 %d시간 %d분   ETA %s\n' \
        $(( REMAIN / 3600 )) $(( (REMAIN % 3600) / 60 )) \
        "$(date -d "+${REMAIN} seconds" '+%H:%M' 2>/dev/null || echo '?')"
    else
      printf '   (전체 청크 도달)\n'
    fi
  fi
fi

# ── 로그 마지막 진행 줄 ───────────────────────────────────────────────
if [[ -n "$LOG" && -f "$LOG" ]]; then
  LINE="$(tr '\r' '\n' < "$LOG" | grep -o 'fit 진행: .*' | tail -1)"
  [[ -n "$LINE" ]] && printf '%s\n' "$LINE"
fi

# ── 자원 ──────────────────────────────────────────────────────────────
command -v free >/dev/null && free -g | awk 'NR==2 {printf "메모리 %s/%s GB\n", $3, $2}'
awk '{printf "load average %s %s %s", $1, $2, $3}' /proc/loadavg 2>/dev/null
NPROC_PHYS=$(lscpu 2>/dev/null | awk -F: '/^Core\(s\) per socket/{c=$2} /^Socket\(s\)/{s=$2} END{if(c&&s) print c*s}')
[[ -n "${NPROC_PHYS:-}" ]] && printf '   (물리코어 %s개)' "$NPROC_PHYS"
printf '\n'

# ── 에러 ──────────────────────────────────────────────────────────────
if [[ -n "$LOG" && -f "$LOG" ]]; then
  ERR="$(tr '\r' '\n' < "$LOG" | grep -E 'ERROR|Traceback|CRITICAL' | tail -3)"
  [[ -n "$ERR" ]] && { hr; printf '최근 에러:\n%s\n' "$ERR"; }
fi

# ── 완료 판정 ─────────────────────────────────────────────────────────
if [[ ${#PIDS[@]} -eq 0 && -f "$RUN_DIR/fits.parquet" ]]; then
  hr
  printf 'fits.parquet  %s  (%s)\n' \
    "$(du -h "$RUN_DIR/fits.parquet" | cut -f1)" \
    "$(stat -c '%y' "$RUN_DIR/fits.parquet" | cut -d. -f1)"
  printf '\n다음 단계:\n'
  printf '  ./run.sh --mode score   --in %s\n' "$RUN_DIR"
  printf '  ./run.sh --mode hessian --in %s\n' "$RUN_DIR"
  printf '  ./run.sh --mode report  --in %s\n' "$RUN_DIR"
fi

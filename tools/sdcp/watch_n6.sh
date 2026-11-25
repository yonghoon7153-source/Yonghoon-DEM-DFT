#!/usr/bin/env bash
# =============================================================================
# watch_n6.sh — n-시리즈 n=6 (ORCA r2SCAN-3c Opt, 199원자) 감시
#
#   bash tools/sdcp/watch_n6.sh [work_dir]
#   watch -n 300 "bash ~/Yonghoon-DEM-DFT/tools/sdcp/watch_n6.sh"
#   bash tools/sdcp/watch_n6.sh --selftest
#
# ⛔ 이 도구가 **못 하는 것**
#   · 스핀 분포를 판정하지 않는다 — `nseries_n6.py --analyze` 몫이다.
#     여기 찍히는 중간 스핀은 **아직 이완 중인 기하**의 값이라 인용 대상이 아니다.
#   · 수렴 여부를 물리로 판정하지 않는다. ORCA 가 찍은 표시만 읽는다.
#   · 남은 시간을 예측하지 않는다 — 사이클 시간이 계마다 크게 다르다.
#     찍는 것은 **지금까지의 평균**이다.
#   · 죽은 잡을 되살리지 않는다.
# =============================================================================
set -uo pipefail

W=${1:-/data/work/runs/sdcp_n6}
STALL_MIN=${STALL_MIN:-90}

# ── 판정 (한 곳에만 둔다 — selftest 가 이 함수를 그대로 부른다) ──────────────
n6_state() {   # $1 = .out 경로 → "상태|비고"
  local f="$1"
  [ -f "$f" ] || { echo "없음|.out 이 없다 — 아직 시작 안 했거나 경로가 다르다"; return; }
  if grep -aq "ORCA has to be called with full pathname" "$f"; then
    echo "☠ 즉사|%pal 을 쓰면 **전체 경로**로 불러야 한다 (\$(which orca))"; return; fi
  if grep -aqi "aborting the run\|ORCA finished by error" "$f"; then
    echo "☠ 오류|$(grep -a -B2 'aborting the run' "$f" | head -1 | cut -c1-60)"; return; fi
  if grep -aq "HURRAY" "$f"; then
    echo "✅ 이완수렴|THE OPTIMIZATION HAS CONVERGED — analyze 로 넘어간다"; return; fi
  if grep -aq "ORCA TERMINATED NORMALLY" "$f"; then
    # ⚠ Opt 가 **미수렴으로** 끝나도 TERMINATED NORMALLY 는 찍힌다 (nstep 소진과 같은 함정)
    echo "⚠ 종료(미수렴)|정상종료지만 HURRAY 가 없다 — 사이클 상한 소진. 이어달리기 필요"; return; fi
  echo "▶ 도는중|"
}

# 상태가 이러면 **이유를 바로 찍는다.** 상태 한 줄만 보고 다시 물어보게 만들면
# 그 왕복 동안 GPU 가 논다 (2026-09-06: 죽은 잡을 18.7시간 방치한 실물).
# ⚠ 반대로 정상 진행 중에 매번 꼬리를 찍으면 5분마다 20줄이라 아무도 안 본다.
n6_needs_tail() {   # $1 = 상태 문자열 → 0 이면 꼬리를 찍는다
  case "$1" in
    "☠"*|"⚠ 종료"*) return 0 ;;
    *)              return 1 ;;
  esac
}

if [ "${1:-}" = "--selftest" ]; then
  T=$(mktemp -d); ok=0; bad=0
  chk(){ if [ "$1" = 1 ]; then echo "  ⭕ $2"; ok=$((ok+1)); else echo "  ⛔ $2"; bad=$((bad+1)); fi; }
  mk(){ printf '%s\n' "$2" > "$T/$1.out"; }
  mk conv "     THE OPTIMIZATION HAS CONVERGED     *** HURRAY ***
                             ****ORCA TERMINATED NORMALLY****"
  mk unconv "                             ****ORCA TERMINATED NORMALLY****"
  mk pal  "ORCA has to be called with full pathname"
  mk err  "something bad
aborting the run"
  mk live "GEOMETRY OPTIMIZATION CYCLE   3"
  chk "$([ "$(n6_state "$T/conv.out"   | cut -d'|' -f1)" = "✅ 이완수렴"   ] && echo 1 || echo 0)" "수렴을 HURRAY 로 가른다"
  chk "$([ "$(n6_state "$T/unconv.out" | cut -d'|' -f1)" = "⚠ 종료(미수렴)" ] && echo 1 || echo 0)" \
      "⛔음성: **TERMINATED NORMALLY 를 수렴으로 읽지 않는다** (Opt 상한 소진도 정상종료다)"
  chk "$([ "$(n6_state "$T/pal.out"    | cut -d'|' -f1)" = "☠ 즉사"       ] && echo 1 || echo 0)" \
      "⛔음성: %pal 전체경로 즉사를 '도는중' 으로 안 읽는다 (Li 잡 4개를 죽인 실물)"
  chk "$([ "$(n6_state "$T/err.out"    | cut -d'|' -f1)" = "☠ 오류"       ] && echo 1 || echo 0)" "오류 종료를 가른다"
  chk "$([ "$(n6_state "$T/live.out"   | cut -d'|' -f1)" = "▶ 도는중"      ] && echo 1 || echo 0)" "도는 중"
  chk "$([ "$(n6_state "$T/nope.out"   | cut -d'|' -f1)" = "없음"         ] && echo 1 || echo 0)" "⛔음성: 파일이 없으면 '없음' — 도는중으로 안 읽는다"
  # ── 꼬리 판정 (2026-09-06: 죽은 잡을 18.7시간 방치한 뒤 추가) ──────────────
  chk "$(n6_needs_tail "☠ 오류"        && echo 1 || echo 0)" "오류면 이유를 바로 찍는다"
  chk "$(n6_needs_tail "☠ 즉사"        && echo 1 || echo 0)" "즉사도 찍는다"
  chk "$(n6_needs_tail "⚠ 종료(미수렴)" && echo 1 || echo 0)" "미수렴 종료도 찍는다 (이어달리기가 필요하다)"
  chk "$(n6_needs_tail "▶ 도는중"      && echo 0 || echo 1)" \
      "⛔음성: **도는 중에는 안 찍는다** — 5분마다 20줄이면 아무도 안 본다"
  chk "$(n6_needs_tail "✅ 이완수렴"    && echo 0 || echo 1)" "⛔음성: 수렴했는데 오류 꼬리를 찍지 않는다"
  rm -rf "$T"; echo "  selftest: ⭕ $ok · ⛔ $bad"; [ "$bad" = 0 ] || exit 1; exit 0
fi

F="$W/n6_doped.out"
echo "════ n-시리즈 n=6 (ORCA r2SCAN-3c Opt · 199원자) · $(date '+%m-%d %H:%M:%S') ════"
echo

IFS='|' read -r ST NOTE <<< "$(n6_state "$F")"
SZ=$([ -f "$F" ] && stat -c %s "$F" || echo 0)
AGE=$([ -f "$F" ] && echo $(( ( $(date +%s) - $(stat -c %Y "$F") ) / 60 )) || echo -)
CYC=0; [ -f "$F" ] && CYC=$(grep -ac "GEOMETRY OPTIMIZATION CYCLE" "$F" 2>/dev/null || true)
CYC=${CYC:-0}

printf "  상태    %s  %s\n" "$ST" "$NOTE"
printf "  사이클  %s        출력 %s B · 무갱신 %s분\n" "$CYC" "$SZ" "$AGE"
if [ "$AGE" != "-" ] && [ "$AGE" -ge "$STALL_MIN" ] && [ "$ST" = "▶ 도는중" ]; then
  echo "  ⚠ ${STALL_MIN}분 넘게 출력이 안 늘었다 — 죽었을 수 있다 (pgrep orca 로 확인)"
fi

if [ -f "$F" ]; then
  echo
  echo "  최근 에너지 (Eh) — ⚠ 이완 중이라 **인용 대상이 아니다**"
  grep -a "FINAL SINGLE POINT ENERGY" "$F" | tail -3 | sed 's/^/    /'
  echo
  echo "  수렴 지표 (마지막 사이클)"
  # ⚠ 2026-09-08 — 종전 범위 `/Geometry convergence/,/^ *---/` 는 **헤더 밑줄에서 끊겨**
  #   표 본문이 한 줄도 안 나오고 헤더만 4번 찍혔다 (실물 화면). ORCA 표는
  #   "-----|Geometry convergence|-----" 다음에 헤더 2줄 + 본문 + 닫는 밑줄이라,
  #   마지막 블록의 **시작 줄 번호**를 찾아 그 뒤 12줄을 찍는다.
  _gc=$(grep -an "Geometry convergence" "$F" | tail -1 | cut -d: -f1)
  if [ -n "$_gc" ]; then
    sed -n "$((_gc+1)),$((_gc+12))p" "$F" | sed 's/^/    /'
  else
    echo "    (수렴표 아직 없음)"
  fi
fi

echo
NP=$(pgrep -c -f "n6_doped" 2>/dev/null || true); NP=${NP:-0}
echo "  프로세스: ${NP}개 · load$(uptime | sed 's/.*load average//')"
if [ "$NP" = 0 ] && [ "$ST" = "▶ 도는중" ]; then
  echo "  ⛔ 프로세스가 없는데 상태가 '도는중' 이다 — **죽었다.** .out 꼬리를 본다:"
  tail -12 "$F" 2>/dev/null | sed "s/^/     /"
fi
if n6_needs_tail "$ST"; then
  echo
  echo "  ⛔ 정상 진행이 아니다 — 여기서 이유를 찍는다 (다시 물어보지 않게):"
  echo "  · 오류 후보:"
  grep -an "aborting the run\|ORCA finished by error\|not enough memory\|insufficient memory\|Killed\|SIGKILL\|MPI_ABORT" \
      "$F" 2>/dev/null | tail -5 | sed 's/^/     /'
  echo "  · .out 꼬리 20줄:"
  tail -20 "$F" 2>/dev/null | sed 's/^/     /'
fi
echo "  RAM: $(free -g | awk '/^Mem/{print $3"/"$2" GB 사용"}')  GPU: $(nvidia-smi --query-gpu=memory.used --format=csv,noheader 2>/dev/null | head -1)"
echo
echo "  ⛔ 스핀 분포는 여기서 판정하지 않는다. 끝나면:"
echo "     python3 ~/Yonghoon-DEM-DFT/tools/sdcp/nseries_n6.py --analyze $W"

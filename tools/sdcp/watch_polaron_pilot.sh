#!/usr/bin/env bash
# =============================================================================
# watch_polaron_pilot.sh — SDCP 폴라론 S0 pilot (ORCA r2SCAN-3c) 감시
#
# 왜 별도인가
#   `watch_stage_a.sh` 는 `<work>/gs*/` + `receipt.json` 배치를 본다. pilot 은
#   `<work>/L/<eps>/<잡>/<잡>.out` + `RUN_RECEIPTS.jsonl` + 단계 lock 이라 배치가 다르다.
#   한 스크립트에 두 배치를 넣으면 둘 다 읽기 어려워진다.
#
# ⛔⛔ 메모리를 **먼저** 본다 (2026-09-04 실측)
#   pilot 은 `nprocs × %maxcore` 를 상한으로 잡는다. mc6000 판은 46.9 GB 를 요청하는데
#   이 기계 가용치가 39 GB 였다 — 그대로 열었으면 같이 도는 Stage A 까지 죽었다.
#   ⚠ ORCA 는 계산을 `orca_gtoint_mpi`·`orca_scf_mpi` 같은 **별도 바이너리**로 돌린다.
#     `ps -C orca` 로 세면 부모 런처만 잡혀 143 MB 로 보인다(실측). 이름으로 grep 한다.
#
# ⛔ 이 도구가 **못 하는 것**
#   · 수렴·물리 타당성 판정 (분석기·게이트 몫). SCF 가 붙었는지도 판정하지 않는다.
#   · 남은 시간 예측. 찍는 것은 **지금까지의 경과**지 예측이 아니다.
#   · 죽은 lock 정리 — 남의 lock 을 건드리지 않는다.
#   · 증서(LOCCHECK_PASS·PROBE_VERDICT_PASS)의 **내용** 검증. 있는지만 본다.
#
#   bash tools/sdcp/watch_polaron_pilot.sh <pilot_dir>
#   watch -n 120 "bash tools/sdcp/watch_polaron_pilot.sh /data/work/runs/sdcp_polaron_S0_mc2500"
#   bash tools/sdcp/watch_polaron_pilot.sh --selftest
# =============================================================================
set -uo pipefail; set +H

# ── selftest ────────────────────────────────────────────────────────────────
if [ "${1:-}" = "--selftest" ]; then
  T=$(mktemp -d); ok=0; bad=0
  chk(){ if [ "$1" = "1" ]; then echo "  ⭕ $2"; ok=$((ok+1)); else echo "  ⛔ $2"; bad=$((bad+1)); fi; }
  D="$T/p"; mkdir -p "$D/L/eps1/a" "$D/L/eps1/b" "$D/L2/eps1/a"
  echo '{"schema":"loccheck_pass/v1"}' > "$D/LOCCHECK_PASS.json"
  # a = 정상종료 · b = 도는 중(SCF 반복만) · L2/a = 손도 안 댐
  printf 'SCF ITERATIONS\nTotal Energy : -3.5\nORCA TERMINATED NORMALLY\n' > "$D/L/eps1/a/a.out"
  printf 'SCF ITERATIONS\n  1   -3.1\n  2   -3.4\n' > "$D/L/eps1/b/b.out"
  mkdir -p "$D/.lock_L"; echo $$ > "$D/.lock_L/pid"
  OUT=$(bash "$0" "$D" 2>&1)
  chk "$(echo "$OUT" | grep -q "L/eps1/a" && echo 1 || echo 0)" "잡을 나열한다"
  chk "$(echo "$OUT" | grep -q "정상종료" && echo 1 || echo 0)" "정상종료를 읽는다"
  chk "$(echo "$OUT" | grep -qE "도는중|진행" && echo 1 || echo 0)" "도는 잡을 구분한다"
  chk "$(echo "$OUT" | grep -q "미실행" && echo 1 || echo 0)" "손 안 댄 잡을 **미실행**로 찍는다 (통과로 세지 않는다)"
  chk "$(echo "$OUT" | grep -q "LOCCHECK_PASS" && echo 1 || echo 0)" "증서 유무를 찍는다"
  chk "$(echo "$OUT" | grep -q "단계 lock" && echo 1 || echo 0)" "단계 lock 주인을 찍는다"
  # ⛔음성: 증서가 없으면 **있다고 하지 않는다**
  rm -f "$D/LOCCHECK_PASS.json"
  OUT2=$(bash "$0" "$D" 2>&1)
  chk "$(echo "$OUT2" | grep -q "LOCCHECK_PASS.*없음" && echo 1 || echo 0)" \
      "⛔음성: 증서가 없으면 **없다고** 찍는다"
  # ⛔음성: pilot 디렉터리가 없으면 빈 표를 그리지 않는다
  OUT3=$(bash "$0" "$T/nope" 2>&1); _rc=$?
  chk "$([ $_rc -ne 0 ] && echo 1 || echo 0)" "⛔음성: 디렉터리가 없으면 **0 이 아닌 코드**로 끝난다"
  chk "$(echo "$OUT3" | grep -q "없" && echo 1 || echo 0)" "⛔음성: 없다고 말한다"
  # ⛔음성: 잡이 하나도 없는 pilot 을 "전부 끝남" 으로 읽지 않는다
  D2="$T/empty"; mkdir -p "$D2/L"
  OUT4=$(bash "$0" "$D2" 2>&1)
  chk "$(echo "$OUT4" | grep -qE "잡이 없|0잡" && echo 1 || echo 0)" \
      "⛔음성: 잡 0개를 완료로 읽지 않는다"
  rm -rf "$T"
  echo "selftest: $ok 통과 / $bad 실패"
  [ "$bad" = 0 ] || exit 1
  exit 0
fi

D=${1:-/data/work/runs/sdcp_polaron_S0_mc2500}
[ -d "$D" ] || { echo "⛔ pilot 디렉터리가 없습니다: $D"; exit 2; }

echo "════════ 폴라론 S0 pilot · ORCA r2SCAN-3c · $(date '+%m-%d %H:%M:%S') ════════"

# ── 기계 여력 — pilot 은 메모리가 병목이다 ──────────────────────────────────
if command -v free >/dev/null; then
  read -r _ _tot _used _ _ _ _avail <<< "$(free -g | awk 'NR==2')"
  _load=$(awk '{print $1}' /proc/loadavg 2>/dev/null || echo ?)
  _ncpu=$(nproc 2>/dev/null || echo ?)
  # ⚠ 별도 바이너리로 갈라지므로 이름 prefix 로 센다 (ps -C orca 는 부모만 잡는다)
  _rss=$(ps -eo rss=,comm= 2>/dev/null | grep -i '^ *[0-9]* *orca' \
         | awk '{s+=$1} END {printf "%.1f", s/1048576}')
  printf "  기계: load %s / %s코어 · 여유 %s GB / %s GB · ORCA 전체 RSS %s GB\n" \
         "$_load" "$_ncpu" "${_avail:-?}" "${_tot:-?}" "${_rss:-?}"
  if [ -n "${_avail:-}" ] && [ "${_avail:-99}" -lt 5 ] 2>/dev/null; then
    echo "        ⛔ 여유 5 GB 미만 — OOM 위험. 도는 잡까지 죽는다"
  fi
fi

# ── 증서 (게이트가 요구하는 것들) ───────────────────────────────────────────
for c in LOCCHECK_PASS PROBE_VERDICT_PASS STAGE1_PASS; do
  if [ -s "$D/$c.json" ]; then
    printf "  증서 %-18s 있음  (%s)\n" "$c.json" "$(date -r "$D/$c.json" '+%m-%d %H:%M' 2>/dev/null)"
  else
    printf "  증서 %-18s 없음\n" "$c.json"
  fi
done

# ── 단계 lock — 어느 단계가 돌고 있나 ───────────────────────────────────────
_any_lock=0
for L in "$D"/.lock_*; do
  [ -d "$L" ] || continue
  _any_lock=1
  _st=$(basename "$L"); _st=${_st#.lock_}
  _p=$(cat "$L/pid" 2>/dev/null || echo "?")
  if [ "$_p" != "?" ] && kill -0 "$_p" 2>/dev/null; then _a="살아있음"; else _a="⚰️ 죽은 PID"; fi
  printf "  단계 lock  %-10s pid=%-8s %s\n" "$_st" "$_p" "$_a"
done
[ "$_any_lock" = 0 ] && echo "  단계 lock  없음 (도는 단계 없음)"

# ── 잡 표 ───────────────────────────────────────────────────────────────────
echo
printf "  %-26s %-10s %8s %10s  %s\n" "잡" "상태" "경과m" "크기" "마지막 에너지"
_n=0
for ph in L L2 S SR probe; do
  for j in "$D"/$ph/*/*; do
    [ -d "$j" ] || continue
    _n=$((_n+1))
    _tag=$(basename "$j"); _rel="${j#$D/}"
    _out="$j/$_tag.out"
    if [ ! -f "$_out" ]; then
      printf "  %-26s %-10s %8s %10s  %s\n" "${_rel:0:26}" "미실행" "-" "-" "-"
      continue
    fi
    _age=$(( ( $(date +%s) - $(stat -c %Y "$_out") ) / 60 ))
    _sz=$(du -h "$_out" 2>/dev/null | cut -f1)
    # grep -a — NUL 오염 대비 (CLAUDE.md 공통 규약)
    if grep -aq "ORCA TERMINATED NORMALLY" "$_out"; then _s="✅정상종료"
    elif [ "$_age" -gt 60 ]; then                        _s="⚠정체?"
    else                                                 _s="▶도는중"; fi
    _e=$(grep -a "Total Energy\|FINAL SINGLE POINT ENERGY" "$_out" 2>/dev/null \
         | tail -1 | grep -ao '\-[0-9][0-9.]*' | head -1)
    printf "  %-26s %-10s %8s %10s  %s\n" "${_rel:0:26}" "$_s" "$_age" "${_sz:-?}" "${_e:-…}"
  done
done
[ "$_n" = 0 ] && echo "  (잡이 없습니다 — 0잡. 생성이 안 됐거나 다른 디렉터리입니다)"

echo
echo "  ⚠ '정체?' 는 60분간 .out 이 안 커진 것 — **의심**이지 판정이 아니다"
echo "  ⛔ 이 표는 수렴·물리를 판정하지 않는다 (분석기·게이트 몫)"

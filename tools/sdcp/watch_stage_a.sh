#!/usr/bin/env bash
# =============================================================================
# watch_stage_a.sh — SDCP Stage A (ORCA r2SCAN-3c Opt) 감시
#
# ⛔ 왜 repo 에 넣었나 (2026-09-02)
#   이 감시는 gabia `/root/w/stage_a_watch.sh` 에만 있었다 — 3분마다 읽는 도구가
#   버전관리 밖이었다. 실제로 그 판본이 무갱신 문턱을 npool 배 잘못 계산하고 있었고
#   (watch_gap_nscf 와 같은 유형), 고쳐도 다음 세션이 그 사실을 모른다.
#   ⇒ 정본을 여기 둔다. gabia 사본은 이걸 부르거나 폐기한다.
#
# ⛔⛔ 병렬 실행을 본다 (2026-09-02)
#   run_orca_stage_a.sh 가 seed 별 lock + ONLY 필터로 **여러 인스턴스**를 허용한다.
#   종전 감시는 러너가 하나라고 가정해 "순번 대기" 와 "다른 인스턴스가 도는 중" 을
#   구분하지 못했다. seed 마다 lock 주인을 찍는다.
#
# ⛔ 이 도구가 **못 하는 것**
#   · 수렴·물리 타당성 판정 (그건 분석기 몫)
#   · 남은 시간의 신뢰구간 — 사이클 시간은 계마다 크게 다르다 (실측 gs0 61분 ·
#     gs2 117분). 표시하는 추정은 **지금까지의 평균**이지 예측이 아니다.
#   · 죽은 lock 정리 (러너의 STALE_LOCK_MIN 몫 — 감시가 남의 lock 을 지우지 않는다)
#
#   bash tools/sdcp/watch_stage_a.sh <work_dir> [stage_a_dir]
#   watch -n 180 "bash tools/sdcp/watch_stage_a.sh /data/work/runs/sdcp_stageA_run"
#   bash tools/sdcp/watch_stage_a.sh --selftest
# =============================================================================
set -uo pipefail; set +H

# ── selftest ────────────────────────────────────────────────────────────────
if [ "${1:-}" = "--selftest" ]; then
  T=$(mktemp -d); ok=0; bad=0
  chk(){ if [ "$1" = "1" ]; then echo "  ⭕ $2"; ok=$((ok+1)); else echo "  ⛔ $2"; bad=$((bad+1)); fi; }
  W="$T/w"; mkdir -p "$W/gs0" "$W/gs1" "$W/gs2" "$W/gs3"
  # gs0 완주 · gs1 도는 중(lock, 살아있는 pid) · gs2 죽은 lock · gs3 손도 안 댐
  printf 'GEOMETRY OPTIMIZATION CYCLE   1\nFINAL SINGLE POINT ENERGY  -10051.1\nORCA TERMINATED NORMALLY\n' \
    > "$W/gs0/dp6_gs0_neutral.out"
  echo '{"returncode":0,"relaxed":true,"orca_terminated_normally":true}' > "$W/gs0/receipt.json"
  printf 'GEOMETRY OPTIMIZATION CYCLE   1\nGEOMETRY OPTIMIZATION CYCLE   2\nTotal Energy       :      -10051.2\n' \
    > "$W/gs1/dp6_gs1_neutral.out"
  mkdir -p "$W/gs1/.lock_seed"; echo $$ > "$W/gs1/.lock_seed/pid"     # 살아있는 pid
  mkdir -p "$W/gs2/.lock_seed"; echo 999999 > "$W/gs2/.lock_seed/pid" # 죽은 pid
  printf 'GEOMETRY OPTIMIZATION CYCLE   1\n' > "$W/gs2/dp6_gs2_neutral.out"
  OUT=$(bash "$0" "$W" 2>&1)
  chk "$(echo "$OUT" | grep -q "gs0.*DONE" && echo 1 || echo 0)" "완주한 seed 를 DONE 으로 찍는다"
  chk "$(echo "$OUT" | grep -qE "gs1.*(run|도는)" && echo 1 || echo 0)" \
      "lock 주인이 **살아 있으면** 도는 중으로 찍는다"
  chk "$(echo "$OUT" | grep -q "gs2" && echo "$OUT" | grep -qi "죽은\|stale" && echo 1 || echo 0)" \
      "⛔음성: lock 은 있는데 **pid 가 죽었으면** 그렇게 말한다 (도는 중으로 세지 않는다)"
  chk "$([ -d "$W/gs2/.lock_seed" ] && echo 1 || echo 0)" \
      "⛔음성: 감시가 죽은 lock 을 **지우지 않는다** (러너 몫이다)"
  chk "$(echo "$OUT" | grep -q "gs3" && echo 1 || echo 0)" "손대지 않은 seed 도 목록에 낸다"
  chk "$(echo "$OUT" | grep -q "2" && echo 1 || echo 0)" "사이클 수를 읽는다"
  # ⛔음성: work 디렉터리가 없으면 빈 표를 그리지 않고 그렇게 말한다
  OUT2=$(bash "$0" "$T/nonexistent" 2>&1); _rc=$?
  chk "$([ $_rc -ne 0 ] && echo 1 || echo 0)" "⛔음성: work 디렉터리가 없으면 **0 이 아닌 코드**로 끝난다"
  chk "$(echo "$OUT2" | grep -qi "없" && echo 1 || echo 0)" "⛔음성: 없다고 말한다 (빈 표를 정상처럼 그리지 않는다)"
  rm -rf "$T"
  echo "selftest: $ok 통과 / $bad 실패"
  [ "$bad" = 0 ] || exit 1
  exit 0
fi

W=${1:-/data/work/runs/sdcp_stageA_run}
A=${2:-}
[ -d "$W" ] || { echo "⛔ work 디렉터리가 없습니다: $W"; exit 2; }

echo "════════ SDCP Stage A · ORCA r2SCAN-3c · $(date '+%m-%d %H:%M:%S') ════════"

# ── 기계 여력 — 2026-09-02 실측 이후 **메모리가 병목**이라 같이 본다 ─────────
if command -v free >/dev/null; then
  read -r _ _tot _used _ _ _ _avail <<< "$(free -g | awk 'NR==2')"
  _load=$(awk '{print $1}' /proc/loadavg 2>/dev/null || echo ?)
  _ncpu=$(nproc 2>/dev/null || echo ?)
  printf "  기계: load %s / %s코어 · 메모리 여유 %s GB / %s GB\n" \
         "$_load" "$_ncpu" "${_avail:-?}" "${_tot:-?}"
  # ⚠ ORCA 한 seed 는 nprocs × %maxcore 를 **상한**으로 잡는다. 실측(2026-09-02)은
  #   랭크당 2.7 GB 미만이었지만 상한은 6 GB 다 — 여유가 그보다 적으면 띄우지 말 것.
  [ -n "${_avail:-}" ] && [ "${_avail:-0}" -lt 10 ] 2>/dev/null && \
    echo "        ⚠ 여유 10 GB 미만 — seed 추가 금지 (OOM 이 나면 도는 잡까지 죽는다)"
fi

# ── ORCA 프로세스 ───────────────────────────────────────────────────────────
_orca=$(ps -eo pid,pcpu,rss,comm 2>/dev/null | awk '/orca/ && !/awk/ {n++; c+=$2; r+=$3} END{printf "%d %.0f %.1f", n, c, r/1048576}')
read -r _on _oc _or <<< "${_orca:-0 0 0}"
printf "  ORCA: 프로세스 %s개 · CPU %s%% (≈%.1f코어) · RSS %s GB\n" \
       "$_on" "$_oc" "$(awk -v c="$_oc" 'BEGIN{print c/100}')" "$_or"

# ── seed 표 ────────────────────────────────────────────────────────────────
printf "\n  %-6s %-22s %7s %5s %-22s %s\n" seed 상태 경과m cyc E_Ha 비고
_ndone=0; _nrun=0; _nidle=0; _nstale=0
for d in $(ls -1 "$W" 2>/dev/null | sort); do
  SD="$W/$d"; [ -d "$SD" ] || continue
  case "$d" in .*) continue ;; esac
  OUTF=$(ls -1 "$SD"/*.out 2>/dev/null | grep -v '_run\.out$' | head -1)
  [ -n "$OUTF" ] || OUTF=$(ls -1 "$SD"/*.out 2>/dev/null | head -1)

  # 상태 — lock 주인이 **살아 있는지**로 '도는 중' 과 '죽은 lock' 을 가른다.
  #   ⛔ 감시는 죽은 lock 을 지우지 않는다 (러너의 STALE_LOCK_MIN 몫).
  st="대기"; note=""
  LK="$SD/.lock_seed"
  if [ -n "$OUTF" ] && grep -aq "ORCA TERMINATED NORMALLY" "$OUTF" 2>/dev/null; then
    st="DONE"; _ndone=$((_ndone+1))
  elif [ -d "$LK" ]; then
    _p=$(cat "$LK/pid" 2>/dev/null || echo "")
    if [ -n "$_p" ] && kill -0 "$_p" 2>/dev/null; then
      st="run (pid $_p)"; _nrun=$((_nrun+1))
    else
      st="⚠ 죽은 lock"; note="pid ${_p:-?} 없음 — 러너가 STALE_LOCK_MIN 으로 치운다"
      _nstale=$((_nstale+1))
    fi
  elif [ -n "$OUTF" ]; then
    st="이전시도"; _nidle=$((_nidle+1))
  else
    _nidle=$((_nidle+1))
  fi

  # 경과·사이클·에너지
  age="-"; cyc="-"; ene="-"
  if [ -n "$OUTF" ]; then
    age=$(( ( $(date +%s) - $(stat -c %Y "$OUTF" 2>/dev/null || date +%s) ) / 60 ))
    _st=$(stat -c %W "$OUTF" 2>/dev/null || echo 0)
    [ "${_st:-0}" -gt 0 ] && age=$(( ( $(date +%s) - _st ) / 60 ))
    cyc=$(grep -ac "GEOMETRY OPTIMIZATION CYCLE" "$OUTF" 2>/dev/null || echo 0)
    ene=$(grep -a "FINAL SINGLE POINT ENERGY" "$OUTF" 2>/dev/null | tail -1 | awk '{print $NF}')
    [ -n "$ene" ] || ene=$(grep -a "Total Energy  *:" "$OUTF" 2>/dev/null | tail -1 | awk '{print $4}')
    [ -n "$ene" ] || ene="-"
  fi
  # receipt 가 있으면 rc·정상종료를 비고에 (파일명·기억이 아니라 원장에서 읽는다)
  if [ -f "$SD/receipt.json" ] && [ -z "$note" ]; then
    note=$(python3 -c "
import json,sys
try:
    r=json.load(open('$SD/receipt.json'))
    print('rc=%s relaxed=%s%s' % (r.get('returncode'), r.get('relaxed'),
          '' if r.get('orca_terminated_normally') else ' ⛔비정상종료'))
except Exception: pass" 2>/dev/null)
  fi
  printf "  %-6s %-22s %7s %5s %-22s %s\n" "$d" "$st" "$age" "$cyc" "$ene" "$note"
done

printf "\n  DONE %d · 도는중 %d · 대기/이전 %d" "$_ndone" "$_nrun" "$_nidle"
[ "$_nstale" -gt 0 ] && printf " · ⚠ 죽은 lock %d" "$_nstale"
echo
# ⚠ 추정을 예측처럼 쓰지 않는다 — 사이클 시간이 계마다 2배 넘게 다르다 (실측).
if [ "$_ndone" -gt 0 ] && [ "$_nidle" -gt 0 ]; then
  echo "  ⚠ 남은 시간 추정은 싣지 않는다 — 사이클 시간이 seed 마다 크게 다르다"
  echo "     (실측 2026-09-02: gs0 61분/cyc · gs2 117분/cyc — 2배 차이)"
fi
if [ "$_nrun" -gt 1 ]; then
  echo "  ✔ 병렬 $_nrun 개 (seed lock 이 중복 실행을 막는다 — run_orca_stage_a.sh ONLY)"
fi

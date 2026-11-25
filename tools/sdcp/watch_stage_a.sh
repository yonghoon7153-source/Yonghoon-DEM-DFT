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
  # 도는 seed 옆의 receipt 는 **이전 시도** 것이다 (gs2 재시작 실물: rc=143 이 run 옆에 붙었다)
  echo '{"returncode":143,"relaxed":false,"orca_terminated_normally":false}' > "$W/gs1/receipt.json"
  mkdir -p "$W/gs2/.lock_seed"; echo 999999 > "$W/gs2/.lock_seed/pid" # 죽은 pid
  printf 'GEOMETRY OPTIMIZATION CYCLE   1\n' > "$W/gs2/dp6_gs2_neutral.out"
  # ⛔⛔ 2026-09-02 — 아래 둘은 **실물이 잡아 준** 결함이다. 첫 판 selftest 6건은
  #   전부 통과하는데 gabia 첫 화면이 둘 다 틀렸다. 픽스처가 실물의 두 모양을
  #   갖고 있지 않았다: ⓐ 종료필드 없는 **구판 receipt** ⓑ **lock 없이 도는** 잡.
  mkdir -p "$W/gs4"
  printf 'GEOMETRY OPTIMIZATION CYCLE   1\nORCA TERMINATED NORMALLY\n' > "$W/gs4/dp6_gs4_neutral.out"
  echo '{"returncode":0,"relaxed":true}' > "$W/gs4/receipt.json"   # ← 종료필드 없음
  OUT=$(bash "$0" "$W" 2>&1)
  chk "$(echo "$OUT" | grep gs4 | grep -q '비정상종료' && echo 0 || echo 1)" \
      "⛔음성 실물: 종료필드가 **없는 구판 receipt** 를 비정상종료로 모함하지 않는다 \
(같은 줄이 DONE 인데 비정상이라고 하면 자기모순이다)"
  chk "$(echo "$OUT" | grep gs4 | grep -q '구판receipt' && echo 1 || echo 0)" \
      "⛔음성 실물: **없음**과 **false** 를 가른다 (없으면 구판이라고 말한다)"
  # ⓑ lock 없이 도는 잡 — 커널의 cwd 가 근거다 (lock 파일이 아니라)
  mkdir -p "$W/gs5"; printf 'GEOMETRY OPTIMIZATION CYCLE   1\n' > "$W/gs5/dp6_gs5_neutral.out"
  cp /bin/sleep "$T/orca_fake" 2>/dev/null && chmod +x "$T/orca_fake"
  if [ -x "$T/orca_fake" ]; then
    ( cd "$W/gs5" && exec -a orca_fake "$T/orca_fake" 300 ) & _fk=$!
    sleep 1
    OUTB=$(bash "$0" "$W" 2>&1)
    kill "$_fk" 2>/dev/null
    chk "$(echo "$OUTB" | grep gs5 | grep -qE 'run' && echo 1 || echo 0)" \
        "⛔음성 실물: **lock 없이 도는** 잡(구판 러너)을 '이전시도' 로 오판하지 않는다 \
— 커널의 cwd 가 근거다"
    chk "$(echo "$OUTB" | grep gs5 | grep -q '구판 러너' && echo 1 || echo 0)" \
        "그 경우 lock 이 없다는 사실을 비고에 적는다 (정상임을 같이 말한다)"
  fi
  # ⛔⛔ 2026-09-03 실물 (gs2 76시간) — **살아있는데 진전이 없는** 상태.
  #   프로세스만 보면 run, 파일만 보면 죽음. 둘이 어긋나는 게 사실이고 그걸 낸다.
  mkdir -p "$W/gs6"; printf 'GEOMETRY OPTIMIZATION CYCLE   1\n' > "$W/gs6/dp6_gs6_neutral.out"
  touch -d '300 minutes ago' "$W/gs6/dp6_gs6_neutral.out"
  if [ -x "$T/orca_fake" ]; then
    ( cd "$W/gs6" && exec -a orca_fake "$T/orca_fake" 300 ) & _fk6=$!
    sleep 1
    OUTC=$(STALL_MIN=240 bash "$0" "$W" 2>&1)
    OUTD=$(STALL_MIN=600 bash "$0" "$W" 2>&1)
    kill "$_fk6" 2>/dev/null
    chk "$(echo "$OUTC" | grep gs6 | grep -q '정체' && echo 1 || echo 0)" \
        "⛔음성 실물(gs2 76시간): 프로세스가 살아있어도 .out 이 문턱 넘게 조용하면 **정체**로 찍는다"
    chk "$(echo "$OUTC" | grep -q '⛔ 정체 1' && echo 1 || echo 0)" \
        "⛔음성: 정체는 '도는중' 에서 빼고 따로 센다 (합계가 도는 것처럼 보이면 안 된다)"
    chk "$(echo "$OUTD" | grep gs6 | grep -qE 'run' && echo 1 || echo 0)" \
        "⛔음성 반대편: 문턱보다 짧게 조용한 건 정체가 아니다 (느린 seed 를 모함하지 않는다)"
  fi
  OUT=$(bash "$0" "$W" 2>&1)
  chk "$(echo "$OUT" | grep -q "gs0.*DONE" && echo 1 || echo 0)" "완주한 seed 를 DONE 으로 찍는다"
  chk "$(echo "$OUT" | grep -qE "gs1.*(run|도는)" && echo 1 || echo 0)" \
      "lock 주인이 **살아 있으면** 도는 중으로 찍는다"
  chk "$(echo "$OUT" | grep gs1 | grep -q '이전 시도 receipt' && echo 1 || echo 0)" \
      "⛔음성 실물(gs2 재시작): 도는 seed 의 receipt 는 **이전 시도** 라고 말한다 (rc=143 이 지금 잡의 것처럼 보이면 안 된다)"
  chk "$(echo "$OUT" | grep gs0 | grep -q '이전 시도' && echo 0 || echo 1)" \
      "DONE 인 seed 의 receipt 에는 그 접두를 붙이지 않는다 (그건 이번 시도 것이다)"
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
# 정체 문턱 [분] — 살아있는 프로세스가 이만큼 .out 을 안 키우면 죽은 것으로 **의심**한다.
# 기본 240 은 실측 최장 사이클(138 분/cyc)의 1.7배다. 짧게 잡으면 느린 seed 를 모함한다.
STALL_MIN=${STALL_MIN:-240}
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
_ndone=0; _nrun=0; _nidle=0; _nstale=0; _nhang=0
for d in $(ls -1 "$W" 2>/dev/null | sort); do
  SD="$W/$d"; [ -d "$SD" ] || continue
  case "$d" in .*) continue ;; esac
  OUTF=$(ls -1 "$SD"/*.out 2>/dev/null | grep -v '_run\.out$' | head -1)
  [ -n "$OUTF" ] || OUTF=$(ls -1 "$SD"/*.out 2>/dev/null | head -1)

  # 상태 — lock 주인이 **살아 있는지**로 '도는 중' 과 '죽은 lock' 을 가른다.
  #   ⛔ 감시는 죽은 lock 을 지우지 않는다 (러너의 STALE_LOCK_MIN 몫).
  st="대기"; note=""
  LK="$SD/.lock_seed"
  # ⛔⛔ 2026-09-02 실물 — **lock 유무만 보면 구판 러너가 띄운 잡이 안 보인다.**
  #   gs2 는 seed lock 도입 **전에** 시작해서 `.lock_seed` 가 없는데 실제로는 돌고
  #   있었다(ORCA 314%). 첫 판이 그걸 "이전시도" 로 찍었다 — 도는 잡을 놀고 있다고
  #   보고하는 것은 감시의 실패다.
  #   ⇒ **프로세스의 cwd** 를 근거로 쓴다. lock 파일이 아니라 커널이 아는 사실이다.
  _rp=""
  for _pd in /proc/[0-9]*; do
    _c=$(readlink "$_pd/cwd" 2>/dev/null) || continue
    [ "$_c" = "$SD" ] || continue
    case "$(cat "$_pd/comm" 2>/dev/null)" in
      *orca*|*ORCA*) _rp="${_pd#/proc/}"; break ;;
    esac
  done
  _live=""
  if [ -n "$OUTF" ] && grep -aq "ORCA TERMINATED NORMALLY" "$OUTF" 2>/dev/null; then
    st="DONE"; _ndone=$((_ndone+1))
  elif [ -n "$_rp" ]; then
    _own=$(cat "$LK/pid" 2>/dev/null || echo "")
    st="run (orca $_rp)"; _nrun=$((_nrun+1)); _live="$_rp"
    [ -d "$LK" ] || note="lock 없음 — 구판 러너가 띄운 잡 (정상)"
  elif [ -d "$LK" ]; then
    _p=$(cat "$LK/pid" 2>/dev/null || echo "")
    if [ -n "$_p" ] && kill -0 "$_p" 2>/dev/null; then
      st="run (pid $_p)"; _nrun=$((_nrun+1)); _live="$_p"
    else
      st="⚠ 죽은 lock"; note="pid ${_p:-?} 없음 — 러너가 STALE_LOCK_MIN 으로 치운다"
      _nstale=$((_nstale+1))
    fi
  elif [ -n "$OUTF" ]; then
    st="이전시도"; _nidle=$((_nidle+1))
  else
    _nidle=$((_nidle+1))
  fi

  # ⛔⛔ 2026-09-03 실측 — **도는 것처럼 보이는데 안 도는** 상태를 가른다 (gs2).
  #   gs2 는 MPI 랭크가 끊긴 뒤 마스터 프로세스만 남았다. cwd 는 그대로라 위 판정이
  #   `run` 을 찍었고, `.out` 은 **76시간** 안 커졌는데 3분마다 보면서도 3일을 놓쳤다.
  #   (마지막에 %CPU 0.0 · MPI `Connection reset by peer` 로 확인)
  #   ⇒ **'프로세스가 있다' 와 '진전이 있다' 는 다른 사실이다.** 둘째를 따로 본다.
  #   ⚠ 문턱은 사이클 시간보다 넉넉해야 한다 — 실측 사이클이 11~138 분/cyc 로
  #     흩어져서, 짧게 잡으면 정상적으로 느린 seed 를 죽었다고 모함한다.
  #     기본 240 분은 가장 느린 실측(138)의 1.7배다. STALL_MIN 으로 조정한다.
  case "$st" in
    run*)
      if [ -n "$OUTF" ]; then
        _sm=$(( ( $(date +%s) - $(stat -c %Y "$OUTF" 2>/dev/null || date +%s) ) / 60 ))
        if [ "$_sm" -ge "$STALL_MIN" ]; then
          st="⛔ 정체 ${_sm}m"; _nrun=$((_nrun-1)); _nhang=$((_nhang+1))
          note="pid ${_live:-?} 는 살아있는데 .out 이 ${_sm}분째 안 큰다 — %CPU 를 확인할 것"
        fi
      fi
      ;;
  esac

  # 경과·사이클·에너지
  # ⚠ 2026-09-02 — 열 뜻을 **상태마다 다르게** 둔다. 하나로 쓰면 둘 다 오해된다.
  #   도는 중 → 시작 이후 경과 (지금 얼마나 돌았나)
  #   DONE    → 실제 소요 (마지막 쓰기 − 생성) · 끝난 뒤 흐른 시간이 아니다
  #   이전/대기 → 마지막 갱신 이후 (얼마나 조용한가)
  age="-"; cyc="-"; ene="-"
  if [ -n "$OUTF" ]; then
    _mt=$(stat -c %Y "$OUTF" 2>/dev/null || date +%s)
    _bt=$(stat -c %W "$OUTF" 2>/dev/null || echo 0)
    case "$st" in
      DONE*) age=$( [ "${_bt:-0}" -gt 0 ] && echo $(( (_mt - _bt) / 60 )) || echo "?" ) ;;
      run*)  age=$( [ "${_bt:-0}" -gt 0 ] && echo $(( ( $(date +%s) - _bt ) / 60 )) \
                    || echo $(( ( $(date +%s) - _mt ) / 60 )) ) ;;
      *)     age=$(( ( $(date +%s) - _mt ) / 60 )) ;;
    esac
    cyc=$(grep -ac "GEOMETRY OPTIMIZATION CYCLE" "$OUTF" 2>/dev/null || echo 0)
    ene=$(grep -a "FINAL SINGLE POINT ENERGY" "$OUTF" 2>/dev/null | tail -1 | awk '{print $NF}')
    [ -n "$ene" ] || ene=$(grep -a "Total Energy  *:" "$OUTF" 2>/dev/null | tail -1 | awk '{print $4}')
    [ -n "$ene" ] || ene="-"
  fi
  # receipt 가 있으면 rc·정상종료를 비고에 (파일명·기억이 아니라 원장에서 읽는다)
  # ⛔ 2026-09-03 실물 — 도는 seed 의 receipt 는 **이전 시도** 것이다 (receipt 은 끝날 때
  #   쓴다). gs2 를 다시 걸자 `run` 옆에 죽은 시도의 `rc=143 ⛔비정상종료` 가 붙어 나와
  #   지금 도는 잡이 잘못된 것처럼 읽혔다. 도는 중이면 그렇게 표시한다.
  _rpref=""
  case "$st" in run*|"⛔ 정체"*) _rpref="이전 시도 receipt → " ;; esac
  if [ -f "$SD/receipt.json" ] && [ -z "$note" ]; then
    # ⛔⛔ 2026-09-02 실물 — **필드 부재를 거짓으로 읽어 정상 실행을 모함했다.**
    #   `orca_terminated_normally` 는 2026-08-30 에 추가된 필드다. 그 전에 만들어진
    #   receipt 에는 아예 없는데, 첫 판이 없음을 false 로 읽어 `⛔비정상종료` 를
    #   찍었다 — 같은 줄에서 `DONE` 이라고 해놓고서다 (자기모순).
    #   ⇒ **없음**과 **false** 를 가른다. 없으면 구판이라고 말하고, 판정은 .out 이
    #     이미 한 것(DONE 열)을 따른다.
    note=$(python3 -c "
import json,sys
try:
    r=json.load(open('$SD/receipt.json'))
    n=r.get('orca_terminated_normally')
    tag = '' if n is True else (' ⚠구판receipt(종료필드없음)' if n is None
                                else ' ⛔비정상종료')
    print('rc=%s relaxed=%s%s' % (r.get('returncode'), r.get('relaxed'), tag))
except Exception: pass" 2>/dev/null)
    [ -n "$note" ] && note="${_rpref}${note}"
  fi
  printf "  %-6s %-22s %7s %5s %-22s %s\n" "$d" "$st" "$age" "$cyc" "$ene" "$note"
  # 사이클당 시간은 **자료에서 계산한다** (아래 각주용). 하드코딩 금지 — 2026-09-02 에
  # 각주에 박아 둔 "실측" 이 한 시간 만에 거짓이 됐다 (경과 열의 뜻이 바뀌면서).
  case "$st" in
    DONE*|run*) [ "${cyc:-0}" -gt 0 ] 2>/dev/null && [ "$age" != "?" ] && [ "$age" != "-" ] \
                && _pc="${_pc:-}$d $(awk -v a="$age" -v c="$cyc" 'BEGIN{printf "%.1f", a/c}') " ;;
  esac
done

printf "\n  DONE %d · 도는중 %d · 대기/이전 %d" "$_ndone" "$_nrun" "$_nidle"
[ "$_nstale" -gt 0 ] && printf " · ⚠ 죽은 lock %d" "$_nstale"
[ "$_nhang" -gt 0 ] && printf " · ⛔ 정체 %d" "$_nhang"
echo
if [ "$_nhang" -gt 0 ]; then
  echo "  ⛔ 정체 seed 가 있다 — 살아있는 프로세스가 진전을 내지 않는다 (gs2 2026-08-31: 76시간)."
  echo "     확인:  ps -o pid,pcpu,etime,args -p <pid>   ·  tail -20 <seed>/*.out"
  echo "     %CPU 0.0 이거나 MPI 'Connection reset' 이 보이면 죽은 것이다 — 죽이고 다시 건다."
fi
# ⚠ 추정을 예측처럼 쓰지 않는다 — 사이클 시간이 계마다 2배 넘게 다르다 (실측).
# ⚠ 남은 시간 추정을 싣지 않는 이유를 **지금 자료로** 보인다.
#   ⛔ 2026-09-02 — 여기 "실측 gs0 61분/cyc · gs2 117분/cyc" 를 **하드코딩**했다가
#     한 시간 만에 거짓이 됐다. 경과 열의 뜻을 고치자(= 실제 소요) 실제 값이
#     gs0 17.0 · gs1 11.3 · gs2 138 으로 바뀌었다 — 2배가 아니라 8~12배였다.
#     감시 도구에 박은 상수는 도구가 바뀌면 조용히 거짓말이 된다. 계산해서 낸다.
if [ -n "${_pc:-}" ]; then
  echo "  분/cyc: $(echo "$_pc" | tr ' ' '\n' | paste -d' ' - - 2>/dev/null | tr '\n' ' ')"
  echo "$_pc" | awk '{
      lo=1e9; hi=0
      for (i=2; i<=NF; i+=2) { v=$i+0; if(v<lo) lo=v; if(v>hi) hi=v }
      if (hi>0 && lo<1e9 && hi > 2*lo)
        printf "  ⚠ 남은 시간 추정을 싣지 않는다 — seed 간 %.0f배 차이 (%.1f~%.1f 분/cyc)\n", hi/lo, lo, hi
      else if (hi>0)
        printf "  (seed 간 편차 %.1f~%.1f 분/cyc)\n", lo, hi
    }'
fi
if [ "$_nrun" -gt 1 ]; then
  echo "  ✔ 병렬 $_nrun 개 (seed lock 이 중복 실행을 막는다 — run_orca_stage_a.sh ONLY)"
fi

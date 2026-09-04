#!/usr/bin/env bash
# =============================================================================
# watch_lpsocl_400ps.sh — LPSOCl 3×3×1 **400 ps 9런** 감시 (안 B · 2026-09-04)
#
# 왜 별도인가 (사다리 ②③ 를 밟고 왔다)
#   `watch_kgy.py` 는 `<ARR6>/<label>/T{T}_s{sd}/**/msd.json` 배치를 기대한다.
#   이 캠페인은 `<root>/s{sd}/d0.00_cfg0/T{T}/msd.json` 라 **구조가 다르고**,
#   환경변수(CELLDIR/ARR6ROOT)로는 못 붙는다. 그리고 watch_kgy 의 `CLOSE_PLAN` 은
#   200 ps·800 ps 계획이라 **안 B(전 온도 400 ps)로 낡았다**.
#
# ⛔⛔ 이 캠페인이 감시를 필요로 하는 이유
#   558원자 × 400 ps × 9런을 **순차**로 돈다. 하나가 조용히 죽으면 뒤가 다 밀린다.
#   드라이버는 resume-safe 라 `msd.json` 이 있으면 건너뛴다 — 그래서 **완료 표식은
#   msd.json 이고 md.log 가 아니다**.
#
# ⛔ 이 도구가 **못 하는 것**
#   · plateau·Ea·골격 판정 (그건 `msd_diffusive_check.py` 와 R1–R5 의 몫)
#   · 남은 시간 **예측** — 찍는 것은 지금까지의 실측 속도지 보장이 아니다
#   · 죽은 런의 재시작 (사람이 판단한다)
#   · 계보 검증 — 드라이버 해시 대조는 개정문 §7 에 별도로 있다
#
#   bash tools/ionic/watch_lpsocl_400ps.sh [run_root]
#   watch -n 300 "bash ~/Yonghoon-DEM-DFT/tools/ionic/watch_lpsocl_400ps.sh"
#   bash tools/ionic/watch_lpsocl_400ps.sh --selftest
# =============================================================================
set -uo pipefail; set +H

TEMPS=${TEMPS:-"600 800 1000"}
SEEDS=${SEEDS:-"2 3 4"}
PROD=${PROD:-400}

if [ "${1:-}" = "--selftest" ]; then
  T=$(mktemp -d); ok=0; bad=0
  chk(){ if [ "$1" = "1" ]; then echo "  ⭕ $2"; ok=$((ok+1)); else echo "  ⛔ $2"; bad=$((bad+1)); fi; }
  R="$T/r"
  # s2/T600 완료 · s2/T800 도는중 · 나머지 미착수
  mkdir -p "$R/s2/d0.00_cfg0/T600" "$R/s2/d0.00_cfg0/T800"
  echo '{"times_ps":[1,2],"msd_Li_A2":[1,2],"msd_Li_A2_mto":[1,2]}' > "$R/s2/d0.00_cfg0/T600/msd.json"
  printf 'Time Etot Epot Ekin T\n0.0 -1 -1 0 600\n1.0 -1 -1 0 600\n' > "$R/s2/d0.00_cfg0/T800/md.log"
  OUT=$(bash "$0" "$R" 2>&1)
  chk "$(echo "$OUT" | grep -q "1/9" && echo 1 || echo 0)" "완료 수를 센다 (msd.json 기준)"
  chk "$(echo "$OUT" | grep -qE "✅|완료" && echo 1 || echo 0)" "완료 런을 표시한다"
  chk "$(echo "$OUT" | grep -qE "▶|도는중" && echo 1 || echo 0)" "도는 런을 구분한다"
  chk "$(echo "$OUT" | grep -q "미착수" && echo 1 || echo 0)" "미착수를 **미착수로** 찍는다 (완료로 세지 않는다)"
  # ⛔음성: msd.json 없는 md.log 만 있는 것을 완료로 세지 않는다
  # ⛔음성 — md.log 만 있는 런(s2/T800)을 완료로 세면 "완료 2/9" 가 된다. 1/9 여야 한다.
  chk "$(echo "$OUT" | grep -q "완료 1/9" && ! echo "$OUT" | grep -q "완료 2/9" && echo 1 || echo 0)" \
      "⛔음성: md.log 만 있는 런을 완료에 넣지 않는다 (완료 1/9 · 2/9 아님)"
  # ⛔음성: 루트가 없으면 빈 표를 그리지 않는다
  OUT2=$(bash "$0" "$T/nope" 2>&1); _rc=$?
  chk "$([ $_rc -ne 0 ] && echo 1 || echo 0)" "⛔음성: 루트가 없으면 0 이 아닌 코드"
  chk "$(echo "$OUT2" | grep -q "없" && echo 1 || echo 0)" "⛔음성: 없다고 말한다"
  # ⛔음성: 진행률을 md.log 마지막 시각으로 읽되, 없으면 '?' 로 두고 0 으로 만들지 않는다
  mkdir -p "$R/s3/d0.00_cfg0/T600"; : > "$R/s3/d0.00_cfg0/T600/md.log"
  OUT3=$(bash "$0" "$R" 2>&1)
  chk "$(echo "$OUT3" | grep -q "?" && echo 1 || echo 0)" \
      "⛔음성: 빈 md.log 의 진행률은 '?' — 0 % 라고 단정하지 않는다"
  rm -rf "$T"; echo "selftest: $ok 통과 / $bad 실패"
  [ "$bad" = 0 ] || exit 1; exit 0
fi

R=${1:-$HOME/work/runs/lpsocl_box331_400ps}
[ -d "$R" ] || { echo "⛔ 런 루트가 없습니다: $R"; exit 2; }

echo "════════ LPSOCl 3×3×1 · 400 ps × 9런 (안 B) · $(date '+%m-%d %H:%M:%S') ════════"

if command -v nvidia-smi >/dev/null; then
  echo "  GPU: $(nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total \
          --format=csv,noheader 2>/dev/null | head -1)"
fi
_np=$(pgrep -fc 'disorder_ensemble_diffusion' 2>/dev/null || echo 0)
echo "  드라이버 프로세스: ${_np}개   $([ "$_np" = 0 ] && echo '⚠ 아무것도 안 돈다 — 끝났거나 죽었다')"

echo
printf "  %-6s %-7s %-10s %10s %12s  %s\n" "시드" "온도" "상태" "진행" "무갱신m" "비고"
_done=0; _run=0; _tot=0
for s in $SEEDS; do
  for T in $TEMPS; do
    _tot=$((_tot+1))
    d="$R/s$s/d0.00_cfg0/T$T"
    mj="$d/msd.json"; ml="$d/md.log"
    if [ -s "$mj" ]; then
      _done=$((_done+1))
      _age=$(( ( $(date +%s) - $(stat -c %Y "$mj") ) / 60 ))
      printf "  %-6s %-7s %-10s %10s %12s  %s\n" "s$s" "${T}K" "✅완료" "100%" "$_age" "msd.json"
    elif [ -f "$ml" ]; then
      _run=$((_run+1))
      # 진행률 — md.log 마지막 줄의 시간[ps]. ⚠ 없으면 '?' 로 두고 0 으로 만들지 않는다.
      _last=$(awk 'NF>1 && $1+0==$1 {v=$1} END{if(v!="")print v}' "$ml" 2>/dev/null)
      if [ -n "${_last:-}" ]; then
        _pct=$(awk -v a="$_last" -v b="$PROD" 'BEGIN{printf "%.0f%%", 100*a/b}')
        _prog="$_pct"
      else
        _prog="?"
      fi
      _age=$(( ( $(date +%s) - $(stat -c %Y "$ml") ) / 60 ))
      _note=""; [ "$_age" -gt 30 ] 2>/dev/null && _note="⚠ 30분 무갱신 — 의심"
      printf "  %-6s %-7s %-10s %10s %12s  %s\n" "s$s" "${T}K" "▶도는중" "$_prog" "$_age" "$_note"
    else
      printf "  %-6s %-7s %-10s %10s %12s  %s\n" "s$s" "${T}K" "미착수" "-" "-" "-"
    fi
  done
done

echo
echo "  완료 $_done/$_tot · 도는중 $_run · 미착수 $((_tot-_done-_run))"

# ── 실측 속도로 남은 시간 (예측이 아니라 **지금까지의 속도**) ────────────────
if [ "$_done" -gt 0 ]; then
  _first=$(find "$R" -name msd.json -printf '%T@\n' 2>/dev/null | sort -n | head -1)
  _last=$(find "$R" -name msd.json -printf '%T@\n' 2>/dev/null | sort -n | tail -1)
  if [ -n "${_first:-}" ] && [ "$_done" -gt 1 ]; then
    awk -v f="$_first" -v l="$_last" -v n="$_done" -v tot="$_tot" 'BEGIN{
      per=(l-f)/(n-1)/3600;
      printf "  실측: 런당 %.1f h · 남은 %d런 ≈ %.1f h (%.1f 일)\n", per, tot-n, per*(tot-n), per*(tot-n)/24;
    }'
    echo "  ⚠ 이건 **지금까지의 평균**이지 예측이 아니다 — 온도마다 속도가 다르다"
  else
    echo "  (런당 시간은 두 번째 완료부터 잰다)"
  fi
fi
echo "  ⛔ 이 표는 plateau·Ea·골격을 판정하지 않는다 — R1–R5 는 반송 뒤 별도"

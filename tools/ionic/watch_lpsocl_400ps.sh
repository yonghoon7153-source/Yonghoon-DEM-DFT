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
# ⭐ 2026-09-15 확장 — **시드 확장 캠페인**(modelc+lpsocl 각 +2 시드)을 같이 본다.
#   · 런루트를 **여러 개** 받는다 (인자 나열). 이름은 옛 것을 지킨다 — 런북·watch_kgy 가 문다.
#   · `NEW_SEEDS` 로 **새로 넣은 시드에 표식**을 단다. 옛 9런과 새 6런이 한 표에 섞이면
#     "무엇이 이번 라운드인지" 가 안 보인다.
#   · 대기열 **락 상태**를 찍는다 (`/tmp/<계>_box331_seed_ext_<시드>.lock`) — 직렬 대기열이
#     어디서 막혀 있는지 로그를 안 열고 안다.
#
#   bash tools/ionic/watch_lpsocl_400ps.sh [run_root ...]
#   SEEDS="2 3 4 5 6" NEW_SEEDS="5 6" bash tools/ionic/watch_lpsocl_400ps.sh \
#       ~/work/runs/modelc_box331_400ps ~/work/runs/lpsocl_box331_400ps
#   watch -n 300 "bash ~/work/Yonghoon-DEM-DFT/tools/ionic/watch_lpsocl_400ps.sh"
#   bash tools/ionic/watch_lpsocl_400ps.sh --selftest
# =============================================================================
set -uo pipefail; set +H

TEMPS=${TEMPS:-"600 800 1000"}
SEEDS=${SEEDS:-"2 3 4"}
#: 이번 라운드에 **새로 넣은** 시드. 표에 ⭐ 를 단다. 비면 아무것도 안 단다
#: (⛔ 없는 것을 '새 시드' 로 추측하지 않는다).
NEW_SEEDS=${NEW_SEEDS:-""}
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
  # ── 2026-09-15 확장분 (여러 루트 · ⭐ 새 시드 표식) ─────────────────────
  R2="$T/r2"; mkdir -p "$R2/s5/d0.00_cfg0/T600"
  echo '{"times_ps":[1,2],"msd_Li_A2":[1,2]}' > "$R2/s5/d0.00_cfg0/T600/msd.json"
  OUT4=$(SEEDS="2 3 4 5" bash "$0" "$R" "$R2" 2>&1)
  chk "$(echo "$OUT4" | grep -c '════════' | grep -q '^2$' && echo 1 || echo 0)" \
      "루트 두 개를 **둘 다** 그린다"
  # ⛔음성: 하나만 없어도 멈춘다 (있는 쪽만 그려서 '반쯤 성공' 으로 보이면 안 된다)
  OUT5=$(bash "$0" "$R" "$T/nope2" 2>&1); _rc5=$?
  chk "$([ $_rc5 -ne 0 ] && echo 1 || echo 0)" "⛔음성: 루트 하나만 없어도 0 이 아닌 코드"
  chk "$(echo "$OUT5" | grep -q 'nope2' && echo 1 || echo 0)" "⛔음성: **어느** 루트가 없는지 이름을 댄다"
  chk "$(echo "$OUT5" | grep -qc '════════' && echo 0 || echo 1)" \
      "⛔음성: 멈출 때 표를 반쯤 그리지 않는다"
  # ⭐ 표식 — NEW_SEEDS 에만 붙고, 비면 아무 데도 안 붙는다
  OUT6=$(SEEDS="2 3" NEW_SEEDS="3" bash "$0" "$R" 2>&1)
  chk "$(echo "$OUT6" | awk '$1=="s3"' | grep -q '⭐' && echo 1 || echo 0)" "⭐ 가 NEW_SEEDS 시드 행에 붙는다"
  chk "$(echo "$OUT6" | awk '$1=="s2"' | grep -q '⭐' && echo 0 || echo 1)" "⛔음성: 새 시드가 아닌 행엔 안 붙는다"
  OUT7=$(SEEDS="2 3" bash "$0" "$R" 2>&1)
  chk "$(echo "$OUT7" | grep -q '⭐' && echo 0 || echo 1)" \
      "⛔음성: NEW_SEEDS 가 비면 **아무 데도** 안 붙는다 (없는 것을 새 시드로 추측하지 않는다)"
  # ⛔음성 (2026-09-15): ETA 를 옛 런과 섞지 않는다
  R3="$T/r3"
  for s in 2 3; do for K in 600 800 1000; do mkdir -p "$R3/s$s/d0.00_cfg0/T$K"
    echo '{"a":1}' > "$R3/s$s/d0.00_cfg0/T$K/msd.json"; done; done
  # 옛 런을 10일 전으로 밀어 둔다 (섞으면 런당 시간이 터무니없이 커진다)
  find "$R3" -name msd.json -exec touch -d '10 days ago' {} +
  mkdir -p "$R3/s5/d0.00_cfg0/T600"; echo '{"a":1}' > "$R3/s5/d0.00_cfg0/T600/msd.json"
  OUT8=$(SEEDS="2 3 5" NEW_SEEDS="5" bash "$0" "$R3" 2>&1)
  chk "$(echo "$OUT8" | grep -q '이번 라운드(시드 5)' && echo 1 || echo 0)" \
      "ETA 범위를 **이번 라운드**로 좁혀 말한다"
  chk "$(echo "$OUT8" | grep -q '두 번째 완료부터' && echo 1 || echo 0)" \
      "⛔음성: 새 시드 완료가 1건이면 **수를 만들지 않는다**"
  chk "$(echo "$OUT8" | grep -qE '런당 [0-9]{2,}\.[0-9] h' && echo 0 || echo 1)" \
      "⛔음성: 10일 전 옛 런을 섞어 터무니없는 런당 시간을 찍지 않는다"
  rm -rf "$T"; echo "selftest: $ok 통과 / $bad 실패"
  [ "$bad" = 0 ] || exit 1; exit 0
fi

# ⚠ 인자가 여럿이면 **전부** 본다. 없으면 옛 기본값 하나.
if [ "$#" -gt 0 ]; then ROOTS=("$@"); else ROOTS=("$HOME/work/runs/lpsocl_box331_400ps"); fi
_missing=()
for _r in "${ROOTS[@]}"; do [ -d "$_r" ] || _missing+=("$_r"); done
# ⛔ 하나라도 없으면 **말하고 0 아닌 코드**로 끝낸다 — 빈 표를 그리지 않는다.
if [ "${#_missing[@]}" -gt 0 ]; then
  echo "⛔ 런 루트가 없습니다: ${_missing[*]}"; exit 2
fi

# ── 대기열 락 (직렬 대기열이 어디서 막혀 있나) ──────────────────────────────
#   ⚠ 락 파일이 **있는 것**과 **잡혀 있는 것**은 다르다. flock -n 으로 실제로 잡아 본다.
_locks=$(ls /tmp/*_box331_seed_ext_*.lock 2>/dev/null)
if [ -n "$_locks" ]; then
  echo "  대기열 락:"
  for L in $_locks; do
    if flock -n "$L" true 2>/dev/null; then
      echo "    $(basename "$L")  — 비어 있음(그 유닛은 안 돌고 있다)"
    else
      _who=$(command -v fuser >/dev/null && fuser "$L" 2>/dev/null | tr -s ' ' || echo "")
      echo "    $(basename "$L")  — 🔒 잡혀 있음${_who:+ (pid$_who)}"
    fi
  done
fi

for R in "${ROOTS[@]}"; do
# ⚠ 2026-09-11 — 이 스크립트는 **같은 드라이버로 도는 어떤 400 ps 캠페인에도** 붙는다
#   (modelc_box331_400ps 등). 경로만 인자로 주면 된다.
#   그리고 실행모드(turbo/default)를 같이 찍는다 — 한 캠페인 안에서 섞이면 그 묶음을
#   한 표에 못 쓰므로(카드 §8 무효조건), 감시가 그걸 먼저 보여야 한다.
[ -d "$R" ] || { echo "⛔ 런 루트가 없습니다: $R"; exit 2; }

# ⚠ 런 수는 **세어서** 찍는다. 종전엔 "9런" 이 글자로 박혀 있어, 시드를 늘려 15런이 돼도
#   머리말은 계속 9 라고 말했다 (손으로 쓴 숫자는 반드시 낡는다).
_nrun=$(( $(echo $SEEDS | wc -w) * $(echo $TEMPS | wc -w) ))
echo "════════ $(basename "$R") · 3×3×1 ${PROD} ps × ${_nrun}런 · $(date '+%m-%d %H:%M:%S') ════════"

if command -v nvidia-smi >/dev/null; then
  echo "  GPU: $(nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total \
          --format=csv,noheader 2>/dev/null | head -1)"
fi
# ⚠ `pgrep -fc` 는 **0 일 때도 "0" 을 찍고 exit 1** 이다. 종전의 `|| echo 0` 은 거기에
#   한 줄을 더 붙여 화면이 "0\n0개" 로 깨졌다 (실측 2026-09-15). tr 로 줄을 없앤다.
_np=$(pgrep -fc 'disorder_ensemble_diffusion' 2>/dev/null | head -1 | tr -dc '0-9')
_np=${_np:-0}
echo "  드라이버 프로세스: ${_np}개   $([ "$_np" = 0 ] && echo '⚠ 아무것도 안 돈다 — 끝났거나 죽었다')"

echo
printf "  %-6s %-7s %-10s %10s %12s  %s\n" "시드" "온도" "상태" "진행" "무갱신m" "비고"
_done=0; _run=0; _tot=0
for s in $SEEDS; do
  for T in $TEMPS; do
    _tot=$((_tot+1))
    # ⚠ 표식은 **비고 칸**에 둔다. 시드 칸에 이모지를 붙이면 폭이 2칸이라 열이 밀린다.
    _new=""; case " $NEW_SEEDS " in *" $s "*) _new="⭐이번 라운드" ;; esac
    d="$R/s$s/d0.00_cfg0/T$T"
    mj="$d/msd.json"; ml="$d/md.log"
    if [ -s "$mj" ]; then
      _done=$((_done+1))
      _age=$(( ( $(date +%s) - $(stat -c %Y "$mj") ) / 60 ))
      printf "  %-6s %-7s %-10s %10s %12s  %s\n" "s$s" "${T}K" "✅완료" "100%" "$_age" "msd.json${_new:+  $_new}"
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
      printf "  %-6s %-7s %-10s %10s %12s  %s\n" "s$s" "${T}K" "▶도는중" "$_prog" "$_age" "${_note}${_new:+  $_new}"
    else
      printf "  %-6s %-7s %-10s %10s %12s  %s\n" "s$s" "${T}K" "미착수" "-" "-" "${_new:-−}"
    fi
  done
done

echo
echo "  완료 $_done/$_tot · 도는중 $_run · 미착수 $((_tot-_done-_run))"

# ── 실측 속도로 남은 시간 (예측이 아니라 **지금까지의 속도**) ────────────────
# ⛔ 2026-09-15 — 종전엔 **루트 전체**의 msd.json 으로 평균을 냈다. 시드 확장에서는 옛 9런이
#   며칠 전 파일이라, 그것과 오늘 것을 한 평균에 넣으면 "런당 시간" 이 **엉뚱한 수**가 된다
#   (그리고 화면은 그걸 실측처럼 보여 준다). NEW_SEEDS 가 있으면 **그 시드들만** 잰다.
if [ -n "${NEW_SEEDS// /}" ]; then
  _scope=""; for _s in $NEW_SEEDS; do [ -d "$R/s$_s" ] && _scope="$_scope $R/s$_s"; done
  _label="이번 라운드(시드 $NEW_SEEDS)"
  _rem=$(( $(echo $NEW_SEEDS | wc -w) * $(echo $TEMPS | wc -w) ))
else
  _scope="$R"; _label="이 루트 전체"; _rem=$_tot
fi
if [ -n "${_scope// /}" ]; then
  _n=$(find $_scope -name msd.json 2>/dev/null | wc -l)
  _first=$(find $_scope -name msd.json -printf '%T@\n' 2>/dev/null | sort -n | head -1)
  _last=$(find $_scope -name msd.json -printf '%T@\n' 2>/dev/null | sort -n | tail -1)
  if [ "$_n" -gt 1 ]; then
    awk -v f="$_first" -v l="$_last" -v n="$_n" -v tot="$_rem" 'BEGIN{
      per=(l-f)/(n-1)/3600;
      printf "  실측(%s): 런당 %.1f h · 남은 %d런 ≈ %.1f h (%.1f 일)\n", "LBL", per, tot-n, per*(tot-n), per*(tot-n)/24;
    }' | sed "s/LBL/$_label/"
    echo "  ⚠ 이건 **지금까지의 평균**이지 예측이 아니다 — 온도마다 속도가 다르다"
  else
    # ⛔ 1개 이하면 **수를 만들지 않는다**. 0 이나 추정치를 찍으면 그게 실측으로 읽힌다.
    echo "  ($_label 완료 ${_n}건 — 런당 시간은 **두 번째 완료부터** 잰다)"
  fi
fi
echo "  ⛔ 이 표는 plateau·Ea·골격을 판정하지 않는다 — R1–R5 는 반송 뒤 별도"

# ── UMA 실행모드 (시드별 run_meta.json) ────────────────────────────────────
_modes=$(for d in "$R"/s*/run_meta.json; do
  [ -f "$d" ] || continue
  python3 -c "import json,sys;d=json.load(open(sys.argv[1]));print(d.get('uma_inference_mode') or d.get('uma_inference_mode_requested') or '?')" "$d" 2>/dev/null
done | sort -u | tr '\n' ' ')
if [ -n "${_modes// /}" ]; then
  if [ "$(echo $_modes | wc -w)" -gt 1 ]; then
    echo "  ⛔ UMA 실행모드가 시드마다 다르다 [$_modes] — 한 묶음으로 못 쓴다 (카드 §8 무효조건)"
  else
    echo "  UMA 실행모드 ${_modes% } (전 시드 동일)"
  fi
fi
done

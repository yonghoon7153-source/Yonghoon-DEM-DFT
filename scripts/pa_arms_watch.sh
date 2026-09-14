#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
# pa_arms_watch.sh — Phase A **팔 캠페인** 감시 (vox 0.25 → 0.20 → 0.15, 각 32팔)
#
#   watch -n 300 'bash ~/pa_arms_watch.sh'
#   bash scripts/pa_arms_watch.sh --selftest      # 파서가 맞나 (합성 로그로)
#
# ⚠ 팔 러너는 **한 팔이 수십 분간 조용하다** — STEP3 복셀화·CG 솔브가 출력 없이 돈다
#   (로그가 스스로 "침묵 수 분 정상" 이라고 적는다).  그래서 "진행 중" 판정을 출력이
#   아니라 **프로세스 생존 + 산출 파일 수**로 한다.  침묵을 실패로 읽지 않는다.
# ⚠ 팔당 소요는 **추정하지 않고 실측**한다 — 완료된 `p2_*.json` 의 mtime 간격이다.
#   팔이 2개 미만이면 `-` 로 두고 ETA 를 만들지 않는다 (없는 숫자를 지어내지 않는다).
# ══════════════════════════════════════════════════════════════════════════════
PA="${PA:-$HOME/pa}"
STAMP="${STAMP:-20260914}"
GRIDS="${GRIDS:-025 020 015}"
ARMS_PER_GRID="${ARMS_PER_GRID:-32}"
KITS_ORDER="${KITS_ORDER:-VGCF_PTFE_1_1 VGCF_PTFE_2_1 VGCF_PTFE_3_1 VGCF_PTFE_4_1}"

_bar() {                       # $1=done $2=total → 20칸 막대
  local d=$1 t=$2 n=20 f
  [ "$t" -le 0 ] && { printf '%*s' "$n" '' | tr ' ' '?'; return; }
  f=$(( d * n / t ))
  printf '%s%s' "$(printf '%*s' "$f" '' | tr ' ' '#')" \
                "$(printf '%*s' $((n - f)) '' | tr ' ' '.')"
}

_hms() {                       # 초 → h:mm:ss  (음수·빈값은 -)
  local s=$1
  case "$s" in ''|*[!0-9]*) printf '%s' '-'; return ;; esac
  printf '%d:%02d:%02d' $((s / 3600)) $(((s % 3600) / 60)) $((s % 60))
}

#: 완료 팔의 mtime 으로 **실측** 팔당 초.  n<2 면 빈 문자열 (추정 금지).
_per_arm() {
  local dir="$1" n first last
  n=$(ls "$dir"/p2_*_a*.json 2>/dev/null | wc -l)
  [ "$n" -lt 2 ] && { printf ''; return; }
  first=$(ls -t "$dir"/p2_*_a*.json 2>/dev/null | tail -1)
  last=$(ls -t "$dir"/p2_*_a*.json 2>/dev/null | head -1)
  local t0 t1
  t0=$(stat -c %Y "$first" 2>/dev/null); t1=$(stat -c %Y "$last" 2>/dev/null)
  [ -z "$t0" ] || [ -z "$t1" ] && { printf ''; return; }
  [ "$t1" -le "$t0" ] && { printf ''; return; }
  printf '%d' $(( (t1 - t0) / (n - 1) ))
}

_alive() { pgrep -f 'sdcp_gain_vox015_8arm\.sh' >/dev/null 2>&1; }

report() {
  echo "══ Phase A 팔 캠페인 · $(hostname)  $(date '+%m-%d %H:%M:%S') ══"
  if command -v nvidia-smi >/dev/null 2>&1; then
    echo "GPU  $(nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu \
             --format=csv,noheader 2>/dev/null | head -1)"
  fi
  [ -d "$PA" ] && echo "디스크 $(df -h "$PA" 2>/dev/null | tail -1 | awk '{print $6"  "$4" 남음"}')"
  echo ""
  printf "%-6s %8s  %-20s %7s  %-16s %9s %10s\n" \
         "격자" "팔" "진행" "%" "킷별" "팔당" "남은시간"
  local tot_done=0 tot_all=0 eta_total=0 eta_known=1
  for g in $GRIDS; do
    local O="$PA/phaseA_h${g}_${STAMP}"
    local n=0
    [ -d "$O" ] && n=$(ls "$O"/p2_*_a*.json 2>/dev/null | wc -l)
    local per; per=$(_per_arm "$O")
    local kb=''
    for k in $KITS_ORDER; do
      local c=0
      [ -d "$O" ] && c=$(ls "$O"/p2_${k}_a*.json 2>/dev/null | wc -l)
      kb="${kb}${c}/"
    done
    kb="${kb%/}"
    local left=$(( ARMS_PER_GRID - n ))
    local eta='-' pers='-'
    if [ -n "$per" ]; then
      pers="$(awk -v s="$per" 'BEGIN{printf "%.1f분", s/60}')"
      eta="$(_hms $(( left * per )))"
      eta_total=$(( eta_total + left * per ))
    elif [ "$left" -gt 0 ]; then
      eta_known=0
    fi
    printf "%-6s %3d/%-4d  %-20s %6.1f%%  %-16s %9s %10s\n" \
           "h$g" "$n" "$ARMS_PER_GRID" "$(_bar "$n" "$ARMS_PER_GRID")" \
           "$(awk -v n="$n" -v t="$ARMS_PER_GRID" 'BEGIN{printf "%.1f", 100*n/t}')" \
           "$kb" "$pers" "$eta"
    tot_done=$(( tot_done + n )); tot_all=$(( tot_all + ARMS_PER_GRID ))
  done
  echo ""
  printf "  전체 %d/%d 팔" "$tot_done" "$tot_all"
  [ "$eta_known" = 1 ] && [ "$eta_total" -gt 0 ] && printf "   ·   남은 시간 ≈ %s" "$(_hms "$eta_total")"
  [ "$eta_known" = 0 ] && printf "   ·   남은 시간 = 아직 못 잼 (팔 2개 이상 필요한 격자가 있다)"
  echo ""

  #  ── 지금 도는 팔 ──
  local cur_log='' cur_grid=''
  for g in $GRIDS; do
    local L="$PA/phaseA_h${g}_${STAMP}.log"
    [ -f "$L" ] && { cur_log="$L"; cur_grid="h$g"; }
  done
  echo ""
  if [ -n "$cur_log" ]; then
    local arm el
    arm=$(grep -a '^\[p2\] ── ' "$cur_log" 2>/dev/null | tail -1 | awk '{print $3}')
    el=$(( $(date +%s) - $(stat -c %Y "$cur_log" 2>/dev/null || date +%s) ))
    printf "  지금:  %s · %s   (로그 갱신 %s 전)\n" "$cur_grid" "${arm:-?}" "$(_hms "$el")"
    printf "         %s\n" "$(grep -av '^\s*$' "$cur_log" | tail -1 | cut -c1-110)"
  fi
  if _alive; then echo "  러너: 살아 있음 (침묵은 정상 — STEP3 복셀화·CG 는 출력이 없다)"
  else echo "  ⛔ 러너 프로세스가 없다 — 끝났거나 죽었다.  아래 체인 로그를 볼 것"; fi

  #  ── 실패 신호 ──
  local bad
  bad=$(grep -ahE 'ABORT|Traceback|out of memory|CUDA error' "$PA"/phaseA_h*_"$STAMP".log 2>/dev/null | tail -3)
  [ -n "$bad" ] && { echo ""; echo "  ⛔ 실패 신호:"; echo "$bad" | sed 's/^/     /' | cut -c1-120; }

  [ -f "$PA/arms_chain.log" ] && { echo ""; echo "  체인:"; tail -3 "$PA/arms_chain.log" | sed 's/^/     /'; }
}

selftest() {
  local ok=0; local -a fail=()
  chk() { if [ "$2" = "$3" ]; then ok=$((ok + 1)); else fail+=("$1 (기대 $2, 실제 $3)"); fi; }
  T=$(mktemp -d)
  #  ① 막대·시간 포맷
  chk '① 막대 0/32' "$(printf '%*s' 20 '' | tr ' ' '.')" "$(_bar 0 32)"
  chk '① 막대 16/32 는 절반' '##########..........' "$(_bar 16 32)"
  chk '② h:mm:ss' '1:01:01' "$(_hms 3661)"
  chk '② 빈값은 -' '-' "$(_hms '')"
  #  ③ 팔당 실측 — 팔이 2개 미만이면 **추정하지 않는다**
  mkdir -p "$T/phaseA_h025_TEST"
  chk '③ 팔 0개면 빈 문자열' '' "$(_per_arm "$T/phaseA_h025_TEST")"
  : > "$T/phaseA_h025_TEST/p2_VGCF_PTFE_1_1_a0.json"
  chk '③b 팔 1개도 빈 문자열 (간격이 없다)' '' "$(_per_arm "$T/phaseA_h025_TEST")"
  : > "$T/phaseA_h025_TEST/p2_VGCF_PTFE_1_1_a1.json"
  touch -d '@1000' "$T/phaseA_h025_TEST/p2_VGCF_PTFE_1_1_a0.json"
  touch -d '@1600' "$T/phaseA_h025_TEST/p2_VGCF_PTFE_1_1_a1.json"
  chk '③c 팔 2개면 mtime 간격 (600초)' '600' "$(_per_arm "$T/phaseA_h025_TEST")"
  : > "$T/phaseA_h025_TEST/p2_VGCF_PTFE_2_1_a0.json"
  touch -d '@2200' "$T/phaseA_h025_TEST/p2_VGCF_PTFE_2_1_a0.json"
  chk '③d 팔 3개면 (마지막-처음)/(n-1)' '600' "$(_per_arm "$T/phaseA_h025_TEST")"
  #  ④ 표에 킷별 분해와 진행이 실린다
  printf '%s\n' '[p2] ── p2_VGCF_PTFE_2_1_a0  shift=(0 0 0)' \
    'STEP3: voxelizing conductive+SE grid (풀해상도 …)' > "$T/phaseA_h025_TEST.log"
  OUT=$(PA="$T" STAMP=TEST GRIDS=025 bash "$0" 2>/dev/null)
  chk '④ 진행 3/32' '3/32' "$(grep -oE '[0-9]+/32' <<<"$OUT" | head -1)"
  chk '④b 킷별 분해 2/1/0/0' '2/1/0/0' "$(grep -oE '[0-9]+/[0-9]+/[0-9]+/[0-9]+' <<<"$OUT" | head -1)"
  grep -q 'p2_VGCF_PTFE_2_1_a0' <<<"$OUT" && ok=$((ok + 1)) || fail+=('④c 현재 팔 표기')
  grep -q 'voxelizing' <<<"$OUT" && ok=$((ok + 1)) || fail+=('④d 현재 단계 표기')
  #  ⑤ ★ 침묵을 실패로 읽지 않는다 / 실패 신호는 띄운다
  grep -q '침묵은 정상\|러너 프로세스가 없다' <<<"$OUT" && ok=$((ok + 1)) || fail+=('⑤ 러너 상태 줄')
  echo 'ABORT — 방법론 규율 검사 실패' >> "$T/phaseA_h025_TEST.log"
  OUT2=$(PA="$T" STAMP=TEST GRIDS=025 bash "$0" 2>/dev/null)
  grep -q '⛔ 실패 신호' <<<"$OUT2" && ok=$((ok + 1)) || fail+=('⑤b ABORT 를 띄운다')
  #  ⑥ ★ 팔이 모자란 격자가 있으면 ETA 를 **지어내지 않는다**
  OUT3=$(PA="$T" STAMP=TEST GRIDS='025 020' bash "$0" 2>/dev/null)
  grep -q '아직 못 잼' <<<"$OUT3" && ok=$((ok + 1)) || fail+=('⑥ 미측정 격자에서 ETA 억제')
  rm -rf "$T"
  echo "pa_arms_watch SELFTEST $ok PASS $([ ${#fail[@]} -eq 0 ] && echo 'ALL GREEN' || printf 'FAIL %s' "${fail[*]}")"
  [ ${#fail[@]} -eq 0 ]
}

case "${1:-}" in
  --selftest) selftest ;;
  *) report ;;
esac

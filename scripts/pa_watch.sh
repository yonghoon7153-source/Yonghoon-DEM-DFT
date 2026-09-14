#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
# pa_watch.sh — Phase A 킷 체인 감시 (GPU 호스트: V100 / kgy)
#
#   watch -n 120 bash ~/Yonghoon-DEM-DFT/scripts/pa_watch.sh
#   bash scripts/pa_watch.sh --selftest        # 파서가 맞나 (합성 로그로)
#
# ⚠⚠ `latest_run` 심링크는 **완료 시에만** 생긴다 (run_mpm.sh:109 → 110 순서).
#   그래서 *도는 중*에는 그것을 보면 **이전 런**을 보거나 아무것도 못 본다.
#   이 감시기는 킷 안의 **가장 최근 `run_*` 폴더**를 본다 — 그것이 현재 런이다.
#
# ⚠ 상태 판정에 마커만 쓰지 않는다.  마커가 없는데 러너 프로세스도 없으면 **중단**이고,
#   그것을 "대기" 로 적으면 조용한 초록이 된다 (ibb 워처에서 같은 부류를 두 번 잡았다).
# ══════════════════════════════════════════════════════════════════════════════
PA="${PA:-$HOME/pa}"
KD="$PA/kits"

#: 러너 생존.  ⚠ `pgrep -f run_mpm.sh` 는 그 낱말이 들어간 **아무 명령줄**(내 쉘 포함)에
#  걸린다 — 실제로 selftest 가 그걸 잡았다.  detach 된 러너(`bash …/run_mpm.sh`)와 솔버만 본다.
#  `PA_FORCE_ALIVE=0|1` 은 **selftest 전용** (주변 프로세스에 판정이 흔들리지 않게).
_runner_alive() {
  [ -n "${PA_FORCE_ALIVE:-}" ] && return $((1 - PA_FORCE_ALIVE))
  pgrep -f 'bash [^ ]*/run_mpm\.sh' >/dev/null 2>&1 \
    || pgrep -f 'mpm3d_compaction\.py|mpm_webapp_payload\.py' >/dev/null 2>&1
}

#: 런 폴더 이름 `run_<tag>_YYYYmmdd_HHMMSS_<pid>` 에서 시작시각을 읽어 경과를 낸다.
_elapsed() {
  local d="$1" ts
  ts=$(sed -n 's/.*_\([0-9]\{8\}\)_\([0-9]\{6\}\)_[0-9]*$/\1 \2/p' <<<"$d")
  [ -z "$ts" ] && { printf '%s' '-'; return; }
  local y=${ts:0:4} mo=${ts:4:2} da=${ts:6:2} h=${ts:9:2} mi=${ts:11:2} s=${ts:13:2}
  local t0 now
  t0=$(date -d "$y-$mo-$da $h:$mi:$s" +%s 2>/dev/null) || { printf '%s' '-'; return; }
  now=$(date +%s); local e=$((now - t0))
  [ "$e" -lt 0 ] && e=0
  printf '%d:%02d:%02d' $((e / 3600)) $(((e % 3600) / 60)) $((e % 60))
}

#: 로그 한 개에서 (프레임, 단계, porosity, 두께, 끝났나) 를 뽑는다.
#  생산 형식 (mpm3d_compaction.py:3228 · 3244):
#    "  frame  90 [descend]  wallP= 0.1234 GPa (…)  porosity= 14.32%  wall_z=0.616  thickness=115.30µm"
#    "FINAL  wallP=0.2500 GPa  porosity(settled)=13.85%  porosity@target=…  thickness=115.30µm  [MPM, …]"
_parse_log() {
  local f="$1" fin ln fr ph por thk
  fin=$(grep -a '^FINAL' "$f" 2>/dev/null | tail -1)
  if [ -n "$fin" ]; then
    por=$(grep -oE 'porosity\(settled\)=[0-9.]+' <<<"$fin" | cut -d= -f2)
    thk=$(grep -oE 'thickness=[0-9.]+' <<<"$fin" | cut -d= -f2)
    printf '%s|%s|%s|%s' 'FINAL' 'FINAL' "${por:--}" "${thk:--}"
    return
  fi
  ln=$(grep -a '^  frame ' "$f" 2>/dev/null | tail -1)
  if [ -z "$ln" ]; then printf '%s' '-|-|-|-'; return; fi
  fr=$(sed -n 's/^  frame *\([0-9]*\) *\[[a-z]*\].*/\1/p' <<<"$ln")
  ph=$(sed -n 's/^  frame *[0-9]* *\[\([a-z]*\)\].*/\1/p' <<<"$ln")
  por=$(grep -oE 'porosity= *[0-9.]+' <<<"$ln" | tr -dc '0-9.')
  thk=$(grep -oE 'thickness=[0-9.]+' <<<"$ln" | cut -d= -f2)
  printf '%s|%s|%s|%s' "${fr:--}" "${ph:--}" "${por:--}" "${thk:--}"
}

report() {
  echo "══ Phase A · $(hostname)  $(date '+%m-%d %H:%M:%S') ══"
  if command -v nvidia-smi >/dev/null 2>&1; then
    echo "GPU  $(nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu \
             --format=csv,noheader 2>/dev/null | head -1)"
  fi
  [ -d "$PA" ] && echo "디스크 $(df -h "$PA" 2>/dev/null | tail -1 | awk '{print $6"  "$4" 남음"}')"
  if [ ! -d "$KD" ]; then echo "⛔ $KD 없음 — 킷을 설치하세요"; return 1; fi

  echo ""
  printf "%-17s %-8s %10s %-9s %9s %10s %10s\n" \
         "킷" "상태" "프레임" "단계" "porosity" "두께(µm)" "경과"
  local alive=0; _runner_alive && alive=1
  local n_done=0 n_run=0 n_wait=0 n_bad=0
  for D in "$KD"/*/; do
    K=$(basename "$D"); [ "$K" = scripts ] && continue
    [ -f "$D/run_mpm.sh" ] || continue
    BUD=$(grep -oE '\-\-frames [0-9]+' "$D/run_mpm.sh" 2>/dev/null | head -1 | awk '{print $2}')
    #  ⚠ `run_*` 는 킷의 **run_mpm.sh 자체**도 집는다 (그게 더 최신이라 head -1 이 그걸 고른다)
    #    → 모든 칸이 `-` 가 된다.  글롭 끝에 `/` 를 붙여 디렉터리만 남긴다.
    R=$(ls -dt "$D"run_*/ 2>/dev/null | head -1); R=${R%/}
    if [ -z "$R" ]; then
      printf "%-17s %-8s %10s %-9s %9s %10s %10s\n" "$K" "대기" "-" "-" "-" "-" "-"
      n_wait=$((n_wait + 1)); continue
    fi
    IFS='|' read -r FR PH POR THK <<<"$(_parse_log "$R/mpm_run.log")"
    if [ -f "$R/mpm_done.marker" ]; then ST="완주"; n_done=$((n_done + 1))
    elif [ "$alive" = 1 ];          then ST="실행중"; n_run=$((n_run + 1))
    else                                 ST="⛔중단"; n_bad=$((n_bad + 1)); fi
    [ "$FR" != '-' ] && [ "$FR" != FINAL ] && [ -n "$BUD" ] && FR="$FR/$BUD"
    printf "%-17s %-8s %10s %-9s %9s %10s %10s\n" \
           "$K" "$ST" "$FR" "$PH" "$POR" "$THK" "$(_elapsed "$R")"
  done
  echo ""
  echo "  완주 $n_done · 실행 $n_run · 대기 $n_wait · 중단 $n_bad"
  #  ⚠ 러너가 죽었는데 마커가 없는 킷은 **조용히 지나가면 안 된다**
  if [ "$n_bad" -gt 0 ]; then
    echo ""
    echo "⛔ 마커 없이 멈춘 런이 있다 — 마지막 로그:"
    for D in "$KD"/*/; do
      R=$(ls -dt "$D"run_* 2>/dev/null | head -1); [ -z "$R" ] && continue
      [ -f "$R/mpm_done.marker" ] && continue
      grep -aE 'ABORT|Error|Traceback|not_converged|CUDA|out of memory' "$R/mpm_run.log" 2>/dev/null \
        | tail -3 | sed "s|^|   $(basename "$D"): |"
    done
  fi
  if [ -f "$PA/chain.log" ]; then
    echo ""
    echo "  체인 로그 (마지막 4줄):"
    tail -4 "$PA/chain.log" | sed 's/^/   /'
  fi
}

# ═══ selftest — 파서가 생산 로그 형식을 실제로 읽는가 ═══════════════════════════
selftest() {
  local ok=0 fail=()
  chk() { if [ "$2" = "$3" ]; then ok=$((ok + 1)); else fail+=("$1 (기대 $2, 실제 $3)"); fi; }
  T=$(mktemp -d)
  #  ① 도는 중 — mpm3d_compaction.py:3228 의 실제 형식
  mkdir -p "$T/kits/K_RUN/run_X_20260914_010000_111"
  printf '%s\n' \
    '[run_mpm] start' \
    '  frame  12 [descend]  wallP= 0.0100 GPa (wallP=0.0100 σzz_vol=0.0100)  porosity= 20.10%  wall_z=0.700  thickness=120.00µm' \
    '  frame  90 [servo]  wallP= 0.1331 GPa (wallP=0.1331 σzz_vol=0.1330)  porosity= 13.85%  wall_z=0.616  thickness=115.30µm' \
    > "$T/kits/K_RUN/run_X_20260914_010000_111/mpm_run.log"
  IFS='|' read -r FR PH POR THK <<<"$(_parse_log "$T/kits/K_RUN/run_X_20260914_010000_111/mpm_run.log")"
  chk '① 마지막 프레임' '90' "$FR"
  chk '① 단계' 'servo' "$PH"
  chk '① porosity (마지막 줄)' '13.85' "$POR"
  chk '① 두께' '115.30' "$THK"
  #  ② 완료 — FINAL 줄이 프레임 줄을 이긴다
  mkdir -p "$T/kits/K_DONE/run_Y_20260914_020000_222"
  printf '%s\n' \
    '  frame  90 [servo]  wallP= 0.1331 GPa (…)  porosity= 13.85%  wall_z=0.616  thickness=115.30µm' \
    'FINAL  wallP=0.1331 GPa  porosity(settled)=13.85%  porosity@target=n/a (target never reached)  thickness=115.30µm   [MPM, hold, scaffold 1498AM se_dump(real), n_grid=256, pts=89146413]' \
    > "$T/kits/K_DONE/run_Y_20260914_020000_222/mpm_run.log"
  IFS='|' read -r FR PH POR THK <<<"$(_parse_log "$T/kits/K_DONE/run_Y_20260914_020000_222/mpm_run.log")"
  chk '② FINAL 인식' 'FINAL' "$FR"
  chk '② FINAL porosity(settled)' '13.85' "$POR"
  chk '② FINAL 두께' '115.30' "$THK"
  #  ③ 로그가 비었을 때 죽지 않는다
  mkdir -p "$T/kits/K_EMPTY/run_Z_20260914_030000_333"; : > "$T/kits/K_EMPTY/run_Z_20260914_030000_333/mpm_run.log"
  chk '③ 빈 로그' '-|-|-|-' "$(_parse_log "$T/kits/K_EMPTY/run_Z_20260914_030000_333/mpm_run.log")"
  chk '③ 없는 로그' '-|-|-|-' "$(_parse_log "$T/없다.log")"
  #  ④ 경과 — 폴더 이름의 시각에서 뽑는다
  E=$(_elapsed "$T/kits/K_RUN/run_X_20260914_010000_111")
  case "$E" in *:*:*) ok=$((ok + 1)) ;; *) fail+=("④ 경과 형식 ($E)") ;; esac
  chk '④ 시각 없는 이름은 -' '-' "$(_elapsed "$T/kits/K_RUN/run_noTS")"
  #  ⑤ ★ 마커 없이 러너가 죽은 킷을 "대기" 로 적으면 조용한 초록이 된다 → ⛔중단 이어야 한다
  for k in K_RUN K_DONE K_EMPTY; do cp /dev/null "$T/kits/$k/run_mpm.sh"; echo '--frames 2500' > "$T/kits/$k/run_mpm.sh"; done
  touch "$T/kits/K_DONE/run_Y_20260914_020000_222/mpm_done.marker"
  OUT=$(PA="$T" PA_FORCE_ALIVE=0 bash "$0" 2>/dev/null)
  chk '⑤ 완주/중단 집계 (러너 없음 = 중단 2)' '완주 1 · 실행 0 · 대기 0 · 중단 2' \
      "$(grep -oE '완주 [0-9]+ · 실행 [0-9]+ · 대기 [0-9]+ · 중단 [0-9]+' <<<"$OUT")"
  grep -q '⛔ 마커 없이 멈춘 런' <<<"$OUT" && ok=$((ok + 1)) || fail+=('⑤b 중단 경보가 안 뜬다')
  grep -q 'K_DONE .*완주' <<<"$OUT" && ok=$((ok + 1)) || fail+=('⑤c 완주 킷 표기')
  #  ⑥ 프레임 예산이 표에 붙는다 (12/2500 처럼)
  grep -qE 'K_RUN .*90/2500' <<<"$OUT" && ok=$((ok + 1)) || fail+=('⑥ 프레임 예산 표기')
  #  ⑦ 킷이 없을 때 죽지 않고 알린다
  PA="$(mktemp -d)" bash "$0" >/dev/null 2>&1; [ $? -eq 1 ] && ok=$((ok + 1)) || fail+=('⑦ 킷 부재 rc')
  #  ★ ⑧ 회귀: run_* 글롭이 `run_mpm.sh` 를 집으면 모든 칸이 `-` 가 된다 (실측 버그)
  OUT2=$(PA="$T" PA_FORCE_ALIVE=1 bash "$0" 2>/dev/null)
  grep -qE 'K_RUN .*90/2500 *servo' <<<"$OUT2" && ok=$((ok + 1)) \
    || fail+=('⑧ run_* 글롭이 run_mpm.sh 를 집는다 (모든 칸 -)')
  rm -rf "$T"
  echo "pa_watch SELFTEST $ok PASS $([ ${#fail[@]} -eq 0 ] && echo 'ALL GREEN' || printf 'FAIL %s' "${fail[*]}")"
  [ ${#fail[@]} -eq 0 ]
}

case "${1:-}" in
  --selftest) selftest ;;
  *) report ;;
esac

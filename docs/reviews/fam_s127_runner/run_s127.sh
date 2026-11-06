#!/bin/bash
# run_s127.sh — FAM §12-7 gabia 발사 러너 (등록 = docs/reviews/fam_platen_prereg_20260812.md §12-7 · 12-7-1 · 12-7-2)
#
# 띄우기 (gabia · tmux 안 · 한 줄):  tmux new -d -s fam127 'bash ~/run_s127.sh'
# 일찍 멈추기 (1저자):              touch ~/fam_s127/STOP
#   → 60 s 안에 도는 팔에 TERM · 120 s 안 안 끝나면 KILL · 다음 팔은 띄우지 않는다
# 기록: ~/fam_s127/batch_s127.log (러너 줄만 — 팔 로그의 줄 · 값은 옮기지 않는다) · 끝나면 tmux 창은 닫힌다
# 팔: confirm_fb → corner_fb → corner_fa → corner_f0 · 한 GPU · 한 번에 한 팔 · 자동 재시도 없음
# 종료 코드: 0 = 팔 넷 끝 · 2 = REFUSED (앞머리) · 3 = SKIP (팔 앞 점검) · 4 = STOPPED (기한 · 1저자) · 5 = CONFIRM_GATE_FAIL
# 열람 규칙: 러너는 팔 로그를 조용한 grep 으로만 본다 — 밖으로 내는 숫자 = 프레임 줄 수 · JSON 필드 수뿐
set -u

WT="$HOME/fam-wt"
PY="$HOME/fam-mpm310/bin/python"
OUT="$HOME/fam_s127"
BATCH="$OUT/batch_s127.log"
STOPF="$OUT/STOP"

SEAL_SHORT=7f44d6534
SEAL_FULL=7f44d6534d864f7be2f3310fa55d213b65cc707d
CODE_REL=scripts/mpm3d_compaction.py
CODE_MD5=c31f0512021d416702e162709c6f4400
CSV_REL=(
  docs/data/case15_corner_20261001/case15_am_scaffold.csv
  docs/data/case15_corner_20261001/case15_se_scaffold.csv
  docs/data/real14_am_scaffold.csv
  docs/data/real14_se_scaffold.csv
)
CSV_SHA=(
  275c56e12fe11294fe6bf2cb304ce4187ee3fb3cb2f7ccdd8a5fc92d770383ba
  929a495e4599dc55f09b2348b5b8b7fe41ecda131bfdbfae08ca0597d1ae0d1f
  281ad86e0465a13b6ed96dbcf30c76acf4f372ff9d7c4a7e36fe55ecd44413fd
  159f4ac05973197e71019e9f541b6cb1517ef7a75c0790f935d1ccfb4c526640
)
GPU_TOTAL=49140
GPU_FREE_MIN=31858
DEADLINE_EPOCH=1795230000            # 2026-11-21T03:00:00Z = 2026-11-21 12:00 KST
DEADLINE_LABEL='2026-11-21 12:00 KST'
POLL_S=60; HB_S=600; TERM_WAIT_S=120; ETA_AFTER_S=3600; SETTLE_S=10
PRINT_EVERY=5                        # 봉인 코드 --print-every 기본값 (argv 에 없음) → 프레임 줄 1 = 프레임 5
FRAMES_CORNER=3000
MARKER='✓ converged: σzz equilibrated at target'
FRAME_RE='^ +frame +[0-9]+ \['
ARMS=(confirm_fb corner_fb corner_fa corner_f0)

# 등록 문안 (prereg 970–986 행) · $COMMON / $COMMON7 를 풀어 씀
COMMON=(--arch cuda --gpu-mem 28 --protocol servo --floor-porosity 0 --compact-to 0 --stop-freeze-probe --platen-mach 0.01 --e-se 1.53 --nu-se 0.49 --sigma-y 0.30 --target-gpa 0.30 --readout wallP --frames 400 --sub 40 --seed 3)
# COMMON7 = 등록 COMMON7 + 12-7-2 개정 (corner 세 팔만 --platen-mach 0.01 → 0.0099999 · 다른 글자 그대로)
COMMON7=(--arch cuda --gpu-mem 28 --protocol servo --floor-porosity 0 --compact-to 0 --stop-freeze-probe --platen-mach 0.0099999 --e-se 1.53 --nu-se 0.49 --sigma-y 0.30 --target-gpa 0.30 --readout wallP --frames 3000 --sub 40 --seed 3)

ARGV=(); HB_T=(); HB_N=(); ARM_RC=0; PG_WHY=""; GPU_WHY=""; GPU_T=""; GPU_F=""

argv_for() {
  case $1 in
    confirm_fb) ARGV=(-u scripts/mpm3d_compaction.py --am-scaffold docs/data/real14_am_scaffold.csv --se-dump docs/data/real14_se_scaffold.csv
                      --n-grid 384 "${COMMON[@]}" --am-load-frac 0.8085 --save-metrics "$OUT/fam_s127_confirm_fb.json") ;;
    corner_fb)  ARGV=(-u scripts/mpm3d_compaction.py --am-scaffold docs/data/case15_corner_20261001/case15_am_scaffold.csv
                      --se-dump docs/data/case15_corner_20261001/case15_se_scaffold.csv --lateral-box 0.1 --n-grid 768 "${COMMON7[@]}"
                      --am-load-frac 0.9007 --save-metrics "$OUT/fam_s127_corner_fb.json") ;;
    corner_fa)  ARGV=(-u scripts/mpm3d_compaction.py --am-scaffold docs/data/case15_corner_20261001/case15_am_scaffold.csv
                      --se-dump docs/data/case15_corner_20261001/case15_se_scaffold.csv --lateral-box 0.1 --n-grid 768 "${COMMON7[@]}"
                      --am-load-frac 0.8240 --save-metrics "$OUT/fam_s127_corner_fa.json") ;;
    corner_f0)  ARGV=(-u scripts/mpm3d_compaction.py --am-scaffold docs/data/case15_corner_20261001/case15_am_scaffold.csv
                      --se-dump docs/data/case15_corner_20261001/case15_se_scaffold.csv --lateral-box 0.1 --n-grid 768 "${COMMON7[@]}"
                      --am-load-frac 0 --allow-unconverged-servo --save-metrics "$OUT/fam_s127_corner_f0.json") ;;
    *) return 1 ;;
  esac
}

now_s() { date +%s; }
at_h() { TZ=KST-9 date -d "@$1" '+%F %T %Z'; }
now_h() { TZ=KST-9 date '+%F %T %Z'; }
say() { printf '%s\n' "$*"; printf '%s\n' "$*" >> "$BATCH" 2> /dev/null; }

digest() {  # $1 = md5sum | sha256sum · $2 = file → hex (or missing)
  local h
  [ -f "$2" ] || { echo missing; return 0; }
  h=$("$1" < "$2") || { echo unreadable; return 0; }
  echo "${h%% *}"
}

# --- arm log: quiet grep only (counts · yes/no) ---
log_has() { LC_ALL=C grep -aqF -- "$2" "$1" 2> /dev/null; }
frame_lines() { local n; n=$(LC_ALL=C grep -acE -- "$FRAME_RE" "$1" 2> /dev/null); echo "${n:-0}"; }
fields_count() {
  local f
  f=$(LC_ALL=C grep -a -- 'saved metrics ' "$1" 2> /dev/null | LC_ALL=C grep -oE '\([0-9]+ fields\)$' | tail -n 1 | tr -dc '0-9')
  echo "${f:-?}"
}
status_word() {
  local log=$1
  if   log_has "$log" 'CUDA_ERROR_OUT_OF_MEMORY'; then echo cuda_oom
  elif log_has "$log" 'CUDA_ERROR'; then echo cuda_error
  elif log_has "$log" 'Traceback'; then echo traceback
  elif log_has "$log" "$MARKER"; then echo converged
  elif log_has "$log" 'servo_status = not_converged_probe_not_at_rest'; then echo not_converged_probe_not_at_rest
  elif log_has "$log" 'servo_status = not_converged_frame_budget'; then echo not_converged_frame_budget
  elif log_has "$log" '[platen] 준정적 한계 위반'; then echo qs_gate_refused
  elif log_has "$log" '[stop] --stop-freeze-probe'; then echo stop_gate_refused
  elif log_has "$log" 'saved metrics '; then echo no_converged_marker
  else echo unknown
  fi
}

pgrep_clear() {  # 0 = no mpm3d process
  local out rc
  out=$(pgrep -af '[m]pm3d_compaction.py' 2>&1); rc=$?
  if [ "$rc" -eq 1 ] && [ -z "$out" ]; then return 0; fi
  if [ "$rc" -eq 0 ]; then PG_WHY="pgrep_busy ($(printf '%s\n' "$out" | grep -c .) 줄)"; else PG_WHY="pgrep_error rc=$rc"; fi
  return 1
}
gpu_read() {  # sets GPU_T GPU_F (MiB) or GPU_WHY
  local out rc nl t f rest
  GPU_T=""; GPU_F=""
  out=$(nvidia-smi --query-gpu=memory.total,memory.free --format=csv,noheader,nounits 2>&1); rc=$?
  if [ "$rc" -ne 0 ]; then GPU_WHY="nvidia-smi rc=$rc"; return 1; fi
  nl=$(printf '%s\n' "$out" | grep -c .)
  if [ "$nl" -ne 1 ]; then GPU_WHY="nvidia-smi lines=$nl (GPU 한 장 기대)"; return 1; fi
  IFS=', ' read -r t f rest <<< "$out"
  if ! [[ $t =~ ^[0-9]+$ && $f =~ ^[0-9]+$ ]] || [ -n "$rest" ]; then GPU_WHY="nvidia-smi parse"; return 1; fi
  GPU_T=$t; GPU_F=$f; return 0
}

refuse() { say "REFUSED $*"; say "§12-7 앞머리 거부 $(now_h) — python 안 띄움 · 1저자에게"; exit 2; }

header() {
  mkdir -p "$OUT" 2> /dev/null || { echo "REFUSED OUT mkdir 실패 ($OUT)"; exit 2; }
  : >> "$BATCH" 2> /dev/null || { echo "REFUSED batch_log 쓰기 실패 ($BATCH)"; exit 2; }
  local got i a x now pyout pyrc v
  say "=== run_s127.sh $(now_h) · runner_md5=$(digest md5sum "${BASH_SOURCE[0]}") · $(id -un)@$(uname -n) ==="
  # 1 봉인 표지
  [ -f "$WT/SEAL_COMMIT" ] || refuse "SEAL_COMMIT 없음 ($WT/SEAL_COMMIT)"
  got=$(cat "$WT/SEAL_COMMIT")
  [ "$got" = "$SEAL_SHORT" ] || refuse "SEAL_COMMIT 다름 (기대 $SEAL_SHORT)"
  # 2 사본 커밋
  got=$(git -C "$WT" rev-parse HEAD 2> /dev/null)
  [ "$got" = "$SEAL_FULL" ] || refuse "HEAD 다름 (got ${got:-없음} · 기대 $SEAL_FULL)"
  # 3 코드 md5
  got=$(digest md5sum "$WT/$CODE_REL")
  [ "$got" = "$CODE_MD5" ] || refuse "md5 $CODE_REL (got $got · 기대 $CODE_MD5)"
  # 4 CSV sha256 넷
  for i in 0 1 2 3; do
    got=$(digest sha256sum "$WT/${CSV_REL[$i]}")
    [ "$got" = "${CSV_SHA[$i]}" ] || refuse "sha256 ${CSV_REL[$i]} (got $got · 기대 ${CSV_SHA[$i]})"
  done
  # 5 PY
  [ -f "$PY" ] && [ -x "$PY" ] || refuse "PY 없음 · 실행 불가 ($PY)"
  # 6 출력 8 개 (덮어쓰지 않는다)
  for a in "${ARMS[@]}"; do for x in log json; do
    [ ! -e "$OUT/fam_s127_$a.$x" ] || refuse "output_exists fam_s127_$a.$x (덮어쓰지 않는다)"
  done; done
  # 7 STOP
  [ ! -e "$STOPF" ] || refuse "STOP 파일 있음 ($STOPF)"
  # 8 기한
  now=$(now_s)
  [ "$now" -lt "$DEADLINE_EPOCH" ] || refuse "deadline 지남 (지금 $(at_h "$now") · 기한 $DEADLINE_LABEL)"
  # 9 도는 mpm3d 없음
  pgrep_clear || refuse "$PG_WHY"
  # 10 GPU
  gpu_read || refuse "$GPU_WHY"
  [ "$GPU_T" = "$GPU_TOTAL" ] || refuse "gpu_total=$GPU_T (기대 $GPU_TOTAL)"
  # 11 PY import — 마지막 (앞 단계의 거부는 python 을 한 번도 부르지 않는다)
  pyout=$(cd "$WT/scripts" && "$PY" -c 'import sys,numpy,scipy,taichi; print("PYVER python=%s numpy=%s scipy=%s taichi=%s" % (sys.version.split()[0], numpy.__version__, scipy.__version__, taichi.__version__))' 2>&1); pyrc=$?
  [ "$pyrc" -eq 0 ] || refuse "PY_import rc=$pyrc ($(printf '%s\n' "$pyout" | tail -n 1))"
  v=$(printf '%s\n' "$pyout" | grep '^PYVER ' | tail -n 1)
  [ -n "$v" ] || refuse "PY_import 판 줄 없음"
  say "VERSIONS ${v#PYVER }"
  printf '%s\n' "$pyout" | grep '^\[Taichi\]' | while IFS= read -r x; do say "TAICHI $x"; done
  say "HEADER ok · SEAL_COMMIT $SEAL_SHORT · HEAD $SEAL_FULL · md5 $CODE_MD5 · sha256 넷 같음 · 출력 8 없음 · STOP 없음 · 기한 전 · pgrep 없음 · GPU total=$GPU_T free=$GPU_F"
}

skip() { say "SKIP $1 $2"; say "§12-7 멈춤 $(now_h) — $1 안 띄움 · 다음 팔 없음 · 1저자에게"; exit 3; }

pre_arm() {  # before EACH arm · any failure = SKIP + end of batch
  local arm=$1 kind=$2 now x
  now=$(now_s)
  [ "$now" -lt "$DEADLINE_EPOCH" ] || skip "$arm" "deadline (지금 $(at_h "$now") · 기한 $DEADLINE_LABEL)"
  [ ! -e "$STOPF" ] || skip "$arm" "STOP 파일 있음"
  pgrep_clear || skip "$arm" "$PG_WHY"
  gpu_read || skip "$arm" "$GPU_WHY"
  [ "$GPU_T" = "$GPU_TOTAL" ] || skip "$arm" "gpu_total=$GPU_T (기대 $GPU_TOTAL)"
  if [ "$kind" = corner ] && [ "$GPU_F" -lt "$GPU_FREE_MIN" ]; then skip "$arm" "gpu_free=$GPU_F < $GPU_FREE_MIN MiB"; fi
  for x in log json; do [ ! -e "$OUT/fam_s127_$arm.$x" ] || skip "$arm" "output_exists fam_s127_$arm.$x"; done
  say "PRE $arm ok $(at_h "$now") · gpu total=$GPU_T free=$GPU_F · pgrep 없음 · STOP 없음"
}

eta_report() {  # report only — changes nothing
  local now=$1 i tref="" nref="" ncur dt dfr spf done_fr rem proj verdict
  ncur=${HB_N[${#HB_N[@]}-1]}
  for i in "${!HB_T[@]}"; do
    if [ "${HB_N[$i]}" -ge 1 ]; then tref=${HB_T[$i]}; nref=${HB_N[$i]}; break; fi
  done
  if [ -z "$tref" ] || [ "$ncur" -le "$nref" ]; then
    say "ETA corner_fb frame_lines ${nref:-0}→$ncur (프레임 줄 간격 부족) s_per_frame=n/a projected_end_if_all_use_3000=n/a deadline=$DEADLINE_LABEL UNKNOWN — 1저자에게 (자동 변경 없음)"
    return 0
  fi
  dt=$((now - tref)); dfr=$(((ncur - nref) * PRINT_EVERY))
  spf=$(((dt * 1000 + dfr / 2) / dfr))
  done_fr=$((PRINT_EVERY * (ncur - 1) + 1))
  rem=$((FRAMES_CORNER - done_fr)); [ "$rem" -lt 0 ] && rem=0
  rem=$((rem + 2 * FRAMES_CORNER))
  proj=$((now + (rem * dt + dfr - 1) / dfr))
  if [ "$proj" -lt "$DEADLINE_EPOCH" ]; then verdict=OK; else verdict=OVER; fi
  say "ETA corner_fb frame_lines ${nref}→${ncur} Δt=${dt}s 1줄=${PRINT_EVERY}프레임 remaining_frames=$rem s_per_frame=$((spf / 1000)).$(printf '%03d' $((spf % 1000))) projected_end_if_all_use_3000=$(at_h "$proj") deadline=$DEADLINE_LABEL $verdict"
  if [ "$verdict" = OVER ]; then say "ETA_OVER — 남은 팔이 예산 3000 을 다 쓰면 기한을 넘는다 · 1저자에게 보고 (자동 변경 없음)"; fi
}

run_arm() {  # uses ARGV · END line · exit 4 if stopped
  local arm=$1
  local log="$OUT/fam_s127_$arm.log" json="$OUT/fam_s127_$arm.json"
  local t0 t0h t1 now n pid rc stop="" last_hb w eta_done=0 js q
  HB_T=(); HB_N=()
  t0=$(now_s); t0h=$(at_h "$t0")
  say "RUN $arm $t0h cwd=$WT"
  q=$(printf '%q ' "$PY" "${ARGV[@]}")
  say "ARGV $arm ${q% }"
  ( cd "$WT" || exit 97; exec "$PY" "${ARGV[@]}" > "$log" 2>&1 ) &
  pid=$!
  last_hb=$t0
  while kill -0 "$pid" 2> /dev/null; do
    sleep "$POLL_S"
    kill -0 "$pid" 2> /dev/null || break
    now=$(now_s)
    if [ "$now" -ge "$DEADLINE_EPOCH" ]; then stop=deadline
    elif [ -e "$STOPF" ]; then stop=author
    fi
    if [ -n "$stop" ]; then
      say "STOPPED $arm $stop"
      kill -TERM "$pid" 2> /dev/null
      say "TERM $arm $(at_h "$now")"
      w=0
      while kill -0 "$pid" 2> /dev/null && [ "$w" -lt "$TERM_WAIT_S" ]; do sleep 5; w=$((w + 5)); done
      if kill -0 "$pid" 2> /dev/null; then
        kill -KILL "$pid" 2> /dev/null
        say "KILL $arm $(now_h) (TERM 뒤 ${TERM_WAIT_S} s 안 끝남)"
      fi
      break
    fi
    if [ $((now - last_hb)) -ge "$HB_S" ]; then
      n=$(frame_lines "$log")
      say "HB $(at_h "$now") $arm frame_lines=$n"
      last_hb=$now; HB_T+=("$now"); HB_N+=("$n")
      if [ "$arm" = corner_fb ] && [ "$eta_done" -eq 0 ] && [ $((now - t0)) -ge "$ETA_AFTER_S" ]; then
        eta_report "$now"; eta_done=1
      fi
    fi
  done
  wait "$pid"; rc=$?
  t1=$(now_s)
  js=no; [ -s "$json" ] && js="yes ($(fields_count "$log") fields)"
  say "END $arm rc=$rc $t0h → $(at_h "$t1") ($((t1 - t0)) s) frame_lines=$(frame_lines "$log") json=$js status=$(status_word "$log")"
  ARM_RC=$rc
  if [ -n "$stop" ]; then
    say "§12-7 멈춤 $(now_h) — $arm 미완주 (실패 아님 · 판정 없음) · 다음 팔 안 띄움"
    exit 4
  fi
}

confirm_gate() {  # registered technical gate: error or not converged within 400 → no corner
  local log="$OUT/fam_s127_confirm_fb.log" json="$OUT/fam_s127_confirm_fb.json" why=""
  [ "$ARM_RC" -eq 0 ] || why="${why}rc=$ARM_RC,"
  [ -s "$json" ] || why="${why}json_missing,"
  ! log_has "$log" 'Traceback' || why="${why}traceback,"
  ! log_has "$log" 'CUDA_ERROR' || why="${why}cuda_error,"
  log_has "$log" "$MARKER" || why="${why}no_converged_marker,"
  if [ -n "$why" ]; then
    say "CONFIRM_GATE_FAIL ${why%,} — corner 를 띄우지 않는다 · 1저자에게"
    exit 5
  fi
  say "CONFIRM_GATE_PASS"
}

main() {
  local arm kind
  header
  say "§12-7 시작 $(now_h)"
  for arm in "${ARMS[@]}"; do
    if [ "$arm" = confirm_fb ]; then kind=confirm; else kind=corner; sleep "$SETTLE_S"; fi
    pre_arm "$arm" "$kind"
    argv_for "$arm" || { say "SKIP $arm argv_for"; exit 3; }
    run_arm "$arm"
    if [ "$kind" = confirm ]; then confirm_gate; fi
  done
  say "§12-7 끝 $(now_h) — 팔 넷 끝 · 분류 · 판정 = 1저자 (12-4 표 먼저)"
  return 0
}

main "$@"; exit $?

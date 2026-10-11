#!/usr/bin/env bash
# =============================================================================
# restart_qe_relax.sh — 죽었거나 nstep 을 소진한 relax 를 **하나씩** 다시 건다.
#
# 왜 있나 (2026-09-06 실측)
#   `sei_control` 이 살아있는 잡 0개로 멈춰 있었다. 원인이 둘이고 처방이 다르다:
#     · r1·r2  ☠ GPU OOM      — 겹쳐 걸어서 죽었다. **한 번에 하나만** 걸면 된다.
#     · r3     ⛔ nstep 소진   — `JOB DONE` 은 찍혔지만 미수렴(|F|=0.042). nstep 을 늘려
#                                `restart_mode='restart'` 로 **이어야** 한다.
#   손으로 하면 이 둘을 섞는다 — OOM 으로 죽은 잡에 `restart` 를 걸면 save 가 없어 또 죽고,
#   nstep 소진 잡을 `from_scratch` 로 걸면 40스텝을 버린다. 그래서 **판정부터** 한다.
#
# 판정 문자열은 `watch_qe_relax.sh` 와 **같은 것을 쓴다.** 갈라지면 화면과 러너가
# 다른 말을 한다 (⚠ 그 파일을 고치면 여기도 같이 본다).
#
# ⛔⛔ 이 스크립트가 **하지 않는 것**
#   · 수렴한 잡을 다시 걸지 않는다. `--force` 도 없다 — 다시 걸고 싶으면 사람이 지운다.
#   · 물리를 판정하지 않는다. "수렴했다" 는 정류점이라는 뜻이지 바닥상태가 아니다.
#   · **옛 .out 을 지우지 않는다.** `.out.NNN` 으로 밀어 둔다 — 재구성 이력이 증거다.
#   · 동시에 돌리지 않는다. GPU 가 빌 때까지 기다리고, 한 잡이 끝나야 다음을 건다.
#   · nstep 을 무한정 늘리지 않는다. 늘린 값도 소진하면 그건 **보고할 사실**이다.
#
# 사용:
#   bash tools/sei/restart_qe_relax.sh                      # 기본 루트 전체 (판정만)
#   bash tools/sei/restart_qe_relax.sh --run                # 실제로 건다
#   bash tools/sei/restart_qe_relax.sh --run --nstep 200    # nstep 늘려서
#   bash tools/sei/restart_qe_relax.sh --run <디렉터리>...   # 골라서
#   bash tools/sei/restart_qe_relax.sh --selftest           # 판정 논리 (QE 없이)
# =============================================================================
set -uo pipefail

ROOTS_DEFAULT="/data/work/runs/sei_control"
NSTEP="${NSTEP:-200}"
GPU_FREE_MIB="${GPU_FREE_MIB:-20000}"
RUN=0; SELFTEST=0; WAIT=1; ARGS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --run)      RUN=1 ;;
    --nstep)    NSTEP="$2"; shift ;;
    --no-wait)  WAIT=0 ;;
    --selftest) SELFTEST=1 ;;
    -h|--help)  sed -n '2,32p' "$0"; exit 0 ;;
    *)          ARGS+=("$1") ;;
  esac; shift
done

# ── 판정 (watch_qe_relax.sh 와 같은 문자열) ─────────────────────────────────
#   → conv | exhaust | stopped | oom | error | no_marker | none
#   ⛔⛔ 2026-10-11 실물 — `stopped` 가 없었다. `<prefix>.EXIT` 로 **사람이 세운** relax 도 QE 는
#   `JOB DONE` 을 찍는다 → 맨 끝 `JOB DONE → conv` 갈래로 떨어져 **"수렴 — 건드리지 않는다"** 가 됐다.
#   09-10 에 EXIT 로 세운 li3nd r2 (step 40 · |F| 0.033) · r3 가 그렇게 찍혔고 `--run` 으로도 영영 안 걸렸다.
#   탄성 러너 (`tools/elastic/run_elastic_relaxedion_gabia.sh::_out_state`, 09-27) 와 같은 문자열로 가른다.
#
# ⛔⛔ 2026-09-07 실물 — 여기 마지막 갈래가 `running` 이었다. **파일에 종료마커가 없다**는
#   것을 **돌고 있다**로 읽은 것이다. 프로세스를 보지도 않고서.
#   그날 화면 둘이 같은 잡을 두고 다른 말을 했다:
#       watch_qe_relax  li3nd…r2  ☠ 죽음 (프로세스 없음 · 1148분)
#       restart_qe_relax li3nd…r2  ▶ 도는 중 — 건드리지 않는다
#   watch 는 커널 cwd 로 생사를 봤고 여기는 안 봤다. 헤더에 "watch 와 같은 판정을 쓴다"
#   고 적어 뒀지만 같았던 건 **문자열**뿐이고 **생사 규칙**은 안 같았다.
#   ⇒ **마커 없이 죽은 잡은 영영 안 걸린다.** 이 도구가 존재하는 바로 그 경우다 (fail-open).
#   고침: 파일 판정과 생사 판정을 **분리**한다. 파일은 `no_marker` 까지만 말하고,
#         돌고 있는지는 `qe_alive_in_dir` 가 커널 cwd 로 정한다 (watch 와 같은 근거).
classify() {
  local f="$1"
  [ -f "$f" ] || { echo none; return; }
  if   grep -aq "bfgs converged in" "$f" 2>/dev/null;                      then echo conv
  elif grep -aq "The maximum number of steps has been" "$f" 2>/dev/null;   then echo exhaust
  elif grep -aqE "Program stopped by user request|Maximum CPU time exceeded" "$f" 2>/dev/null; then echo stopped
  elif grep -aqi "CUDA_ERROR_OUT_OF_MEMORY\|Accelerator Fatal Error" "$f"; then echo oom
  elif grep -aq "Error in routine" "$f" 2>/dev/null;                       then echo error
  elif grep -aq "JOB DONE" "$f" 2>/dev/null;                               then echo conv
  else echo no_marker; fi
}

# 이 폴더에서 **지금 돌고 있는** QE 프로세스가 있나. 근거는 커널의 cwd 다 —
# lock 파일도 출력 파일도 죽은 뒤에 남는다 (watch_qe_relax.sh `_scan_procs` 와 같은 근거).
QE_PROC_NAMES=${QE_PROC_NAMES:-"pw.x neb.x"}
qe_alive_in_dir() {   # $1 = 폴더 → 0 이면 살아있다
  local n p c d; d=$(cd "$1" 2>/dev/null && pwd -P) || return 1
  for n in $QE_PROC_NAMES; do
    for p in $(pgrep -x "$n" 2>/dev/null); do
      c=$(readlink "/proc/$p/cwd" 2>/dev/null) || continue
      [ "$c" = "$d" ] && return 0
    done
  done
  return 1
}

# 재시작 방식: 이어달릴 save 가 실제로 있나로 정한다 (판정만으로는 못 정한다).
#   ⛔ nstep 소진인데 save 가 없으면 `restart` 는 즉사한다 — 그때는 from_scratch 다.
#   ⚠ `dead`(마커 없이 죽음)는 save 가 있어도 **from_scratch** 다. 마커를 못 남기고 죽은
#     잡은 쓰다 만 save 를 남겼을 가능성이 제일 높은 경우다 — 이어달리면 조용히 틀린 데서
#     출발한다. 몇 시간을 다시 쓰는 것이 못 믿을 지점에서 잇는 것보다 싸다.
restart_mode_for() {
  local dir="$1" kind="$2"
  local sv; sv=$(find "$dir" -maxdepth 3 -name "*.save" -type d 2>/dev/null | head -1)
  if { [ "$kind" = "exhaust" ] || [ "$kind" = "stopped" ]; } && [ -n "$sv" ] && [ -n "$(ls -A "$sv" 2>/dev/null)" ]; then
    echo restart
  else
    echo from_scratch
  fi
}

# ⛔⛔ 중복 실행 가드 (2026-09-07 실물)
#   이 스크립트가 **4개**, `pw.x` 가 **2개** 떠서 같은 `.save` 에 동시에 썼다.
#   원인은 단순하다 — 터미널이 끊겨 잡이 죽은 줄 모르고 사람이 다시 걸었고, 막는 것이 없었다.
#   `mkdir` 은 원자적이라 경합에 안전하다. 죽은 lock 은 pid 로 확인하고 스스로 치운다
#   (남의 lock 을 무조건 지우지도, 무조건 믿지도 않는다).
#   ⚠ `--run` 일 때만 건다. 판정만 하는 실행은 몇 개가 돌든 해롭지 않다.
LOCKDIR="${QE_RESTART_LOCK:-${TMPDIR:-/tmp}/.restart_qe_relax.lock}"
acquire_lock() {   # 0 = 잡았다 · 1 = 이미 돌고 있다
  if mkdir "$LOCKDIR" 2>/dev/null; then echo $$ > "$LOCKDIR/pid"; return 0; fi
  local p; p=$(cat "$LOCKDIR/pid" 2>/dev/null)
  if [ -n "$p" ] && kill -0 "$p" 2>/dev/null; then return 1; fi
  echo "· 죽은 lock 을 치운다 (pid ${p:-?})" >&2
  rm -rf "$LOCKDIR" && mkdir "$LOCKDIR" 2>/dev/null || return 1
  echo $$ > "$LOCKDIR/pid"; return 0
}

gpu_free_mib() {
  command -v nvidia-smi >/dev/null || { echo 999999; return; }   # 못 재면 막지 않는다
  local t u
  t=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1)
  u=$(nvidia-smi --query-gpu=memory.used  --format=csv,noheader,nounits 2>/dev/null | head -1)
  [ -n "$t" ] && [ -n "$u" ] && echo $((t - u)) || echo 999999
}

# 입력을 고친 사본을 만든다. **원본 .in 은 안 건드린다** — 무엇으로 처음 돌렸는지가 증거다.
patch_in() {
  local src="$1" dst="$2" mode="$3" nstep="$4"
  awk -v m="$mode" -v n="$nstep" '
    BEGIN{ IGNORECASE=1; got_r=0; got_n=0; inctl=0 }
    /^[[:space:]]*&CONTROL/ { inctl=1; print; next }
    inctl && /^[[:space:]]*\// {
      if(!got_r) printf("  restart_mode = \x27%s\x27\n", m)
      if(!got_n) printf("  nstep = %s\n", n)
      inctl=0; print; next
    }
    inctl && /restart_mode/ { printf("  restart_mode = \x27%s\x27\n", m); got_r=1; next }
    inctl && /[[:space:]]*nstep[[:space:]]*=/ { printf("  nstep = %s\n", n); got_n=1; next }
    { print }
  ' "$src" > "$dst"
  grep -qi "restart_mode" "$dst" && grep -qi "nstep" "$dst"
}

# ── selftest — 음성 경로가 본론이다 ─────────────────────────────────────────
if [ "$SELFTEST" = 1 ]; then
  T=$(mktemp -d); ok=0; bad=0
  chk(){ if [ "$1" = "1" ]; then echo "  ⭕ $2"; ok=$((ok+1)); else echo "  ⛔ $2"; bad=$((bad+1)); fi; }
  mk(){ mkdir -p "$T/$1"; printf '%s\n' "$2" > "$T/$1/00_control_relax.out"; }
  mk conv    "     bfgs converged in  40 scf cycles and  1 bfgs steps
     JOB DONE."
  mk exhaust "     The maximum number of steps has been reached.
     JOB DONE."
  mk oom     "CUDA_ERROR_OUT_OF_MEMORY"
  mk err     "     Error in routine  read_namelists (1):
     opening input file"
  mk run     "     Total force =     0.0400"
  mk stop    "     number of bfgs steps    =  40

     Program stopped by user request
     JOB DONE."
  mkdir -p "$T/none"
  for c in conv exhaust stop oom err run none; do
    case "$c" in conv) w=conv;; exhaust) w=exhaust;; stop) w=stopped;; oom) w=oom;; err) w=error;; run) w=no_marker;; none) w=none;; esac
    g=$(classify "$T/$c/00_control_relax.out")
    chk "$([ "$g" = "$w" ] && echo 1 || echo 0)" "판정 $c → $g (기대 $w)"
  done
  # ── 생사 (2026-09-07 실물: watch 는 '죽음', 여기는 '도는 중' 이라 했다) ──────
  chk "$([ "$(classify "$T/run/00_control_relax.out")" = no_marker ] && echo 1 || echo 0)" \
      "⛔음성: 종료마커가 없는 것을 **'도는 중' 이라 부르지 않는다** (파일은 생사를 모른다)"
  chk "$(qe_alive_in_dir "$T/run" && echo 0 || echo 1)" \
      "⛔음성: 프로세스가 없으면 살아있다고 하지 않는다 — 이게 fail-open 이면 죽은 잡이 영영 안 걸린다"
  cp /bin/sleep "$T/qefake" 2>/dev/null && chmod +x "$T/qefake"
  ( cd "$T/run" && exec "$T/qefake" 20 ) & _fp=$!
  sleep 1
  chk "$(QE_PROC_NAMES=qefake qe_alive_in_dir "$T/run" && echo 1 || echo 0)" \
      "양성: 그 폴더가 cwd 인 프로세스가 있으면 살아있다 (근거는 커널 cwd — lock·파일이 아니다)"
  chk "$(QE_PROC_NAMES=qefake qe_alive_in_dir "$T/conv" && echo 0 || echo 1)" \
      "⛔음성: **다른** 폴더에서 도는 프로세스를 이 폴더 것으로 세지 않는다"
  kill "$_fp" 2>/dev/null
  chk "$([ "$(restart_mode_for "$T/run" dead)" = from_scratch ] && echo 1 || echo 0)" \
      "⛔음성: 마커 없이 죽은 잡은 save 가 있어도 처음부터 (쓰다 만 save 를 못 믿는다)"
  # ── 중복 실행 lock (2026-09-07 실물: 스크립트 4개 · pw.x 2개가 같은 .save 에 썼다) ──
  LOCKDIR="$T/lock"
  chk "$(acquire_lock && echo 1 || echo 0)" "처음엔 lock 을 잡는다"
  ( LOCKDIR="$T/lock"; acquire_lock ) && _dup=0 || _dup=1
  chk "$_dup" "⛔음성: **살아있는 lock 주인이 있으면 두 번째는 못 잡는다** (이게 없으면 pw.x 가 둘이 된다)"
  echo 999999 > "$T/lock/pid"          # 존재하지 않는 pid = 죽은 lock
  chk "$(acquire_lock && echo 1 || echo 0)" "죽은 lock 은 스스로 치우고 잡는다 (사람 손 안 빌린다)"
  chk "$([ "$(cat "$T/lock/pid")" = "$$" ] && echo 1 || echo 0)" "치운 뒤 자기 pid 를 적는다"
  rm -rf "$T/lock"
  # ⛔음성: nstep 소진은 JOB DONE 을 **찍는다** — 완주로 읽으면 안 된다
  chk "$([ "$(classify "$T/exhaust/00_control_relax.out")" = exhaust ] && echo 1 || echo 0)" \
      "⛔음성: JOB DONE 이 있어도 nstep 소진을 완주로 세지 않는다"
  # ⛔음성: save 가 없으면 exhaust 라도 restart 가 아니라 from_scratch
  chk "$([ "$(restart_mode_for "$T/exhaust" exhaust)" = from_scratch ] && echo 1 || echo 0)" \
      "⛔음성: save 없는 nstep소진에 restart 를 걸지 않는다 (걸면 즉사한다)"
  mkdir -p "$T/exhaust/tmp/x.save"; echo z > "$T/exhaust/tmp/x.save/charge-density.dat"
  chk "$([ "$(restart_mode_for "$T/exhaust" exhaust)" = restart ] && echo 1 || echo 0)" \
      "양성: save 가 있으면 restart 로 이어붙인다"
  chk "$([ "$(restart_mode_for "$T/oom" oom)" = from_scratch ] && echo 1 || echo 0)" \
      "⛔음성: OOM 은 save 가 있어도 처음부터 (죽은 지점 상태를 못 믿는다)"
  # ⛔음성 (2026-10-11 실물): EXIT 로 세운 relax 는 JOB DONE 이 있어도 수렴이 아니다
  chk "$([ "$(classify "$T/stop/00_control_relax.out")" != conv ] && echo 1 || echo 0)" \
      "⛔음성: EXIT 로 세운 relax 를 **수렴으로 세지 않는다** (li3nd r2·r3 가 '수렴 — 건드리지 않는다' 로 찍혔다)"
  chk "$([ "$(restart_mode_for "$T/stop" stopped)" = from_scratch ] && echo 1 || echo 0)" \
      "⛔음성: save 없는 세운 잡에 restart 를 걸지 않는다"
  mkdir -p "$T/stop/tmp/y.save"; echo z > "$T/stop/tmp/y.save/charge-density.dat"
  chk "$([ "$(restart_mode_for "$T/stop" stopped)" = restart ] && echo 1 || echo 0)" \
      "양성: save 가 있으면 세운 잡은 restart 로 잇는다 (BFGS 이력 승계)"
  # 판정 화면이 세운 잡을 다시 걸 목록에 올리는가 (본 루프 case 배선 · 판정만 · --run 아님)
  mkdir -p "$T/sroot/j"; printf "&CONTROL\n/\n" > "$T/sroot/j/00_control_relax.in"; cp "$T/stop/00_control_relax.out" "$T/sroot/j/"
  _o2=$(QE_RESTART_ROOTS="$T/sroot" bash "$0" 2>/dev/null || true)
  chk "$(echo "$_o2" | grep -q "사람이 세움" && ! echo "$_o2" | grep -q "다시 걸 것이 없다" && echo 1 || echo 0)" \
      "⛔음성: 본 루프가 세운 잡을 '다시 걸 것이 없다' 로 넘기지 않는다 (판정 화면 배선)"
  # 입력 패치 — 있는 키는 바꾸고 없는 키는 넣는다
  printf "&CONTROL\n  calculation = 'relax'\n  nstep = 50\n/\n&SYSTEM\n/\n" > "$T/a.in"
  patch_in "$T/a.in" "$T/a.out.in" restart 200 >/dev/null
  chk "$(grep -qc "nstep = 200" "$T/a.out.in" && grep -q "restart_mode = 'restart'" "$T/a.out.in" && echo 1 || echo 0)" \
      "패치: 있는 nstep 을 바꾸고 없는 restart_mode 를 넣는다"
  chk "$([ "$(grep -c "nstep" "$T/a.out.in")" = 1 ] && echo 1 || echo 0)" \
      "⛔음성: nstep 이 두 번 들어가지 않는다 (QE 가 마지막 것을 쓰면 조용히 틀린다)"
  printf "&CONTROL\n  calculation = 'relax'\n/\n" > "$T/b.in"
  patch_in "$T/b.in" "$T/b.out.in" from_scratch 120 >/dev/null
  chk "$(grep -q "nstep = 120" "$T/b.out.in" && echo 1 || echo 0)" "패치: 키가 없어도 넣는다"
  # ⛔음성: .in 없는 폴더는 잡이 아니다 (구조 보관 폴더를 오류로 세지 않는다)
  mkdir -p "$T/stash"; : > "$T/stash/x.vasp"; printf 'Error in routine read_input (1):\n' > "$T/stash/y.out"
  _o=$(QE_RESTART_ROOTS="$T" bash "$0" 2>/dev/null | grep -c "잡 아님" || true)
  chk "$([ "${_o:-0}" -ge 1 ] && echo 1 || echo 0)" \
      "⛔음성: .in 없는 폴더를 '잡 아님' 으로 가른다 (_control_structures 실물)"
  rm -rf "$T"
  echo "  selftest: ⭕ $ok · ⛔ $bad"; [ "$bad" = 0 ] || exit 1; exit 0
fi

# ── 대상 수집 ───────────────────────────────────────────────────────────────
if [ "${#ARGS[@]}" -gt 0 ]; then DIRS=("${ARGS[@]}")
else
  shopt -s nullglob
  DIRS=()
  for r in ${QE_RESTART_ROOTS:-$ROOTS_DEFAULT}; do
    for d in "$r"/*/; do DIRS+=("${d%/}"); done
  done
fi
[ "${#DIRS[@]}" -gt 0 ] || { echo "⛔ 대상이 없다"; exit 1; }

echo "════ QE relax 재시작 — 판정 ════"
TODO=(); MODES=()
for d in "${DIRS[@]}"; do
  # ⛔ 2026-09-06 실물 — `_control_structures` 는 **잡이 아니라 구조 보관 폴더**다
  #   (.vasp 4개 + 남의 CRASH). 그런데 매번 "☠ QE 오류" 로 찍혀서 7.5일 방치처럼 보였다.
  #   경보가 틀리면 사람이 목록 전체를 안 믿게 된다 (Cowork 검증기 false NO-GO 와 같은 부류).
  #   ⇒ **입력(.in)이 없으면 잡이 아니다.** 조용히 넘기지 않고 그렇게 말한다.
  # ⚠ `ls "$d"/*.in` 로 쓰면 안 된다 — `shopt -s nullglob` 이 켜져 있어 매치가 없으면
  #   glob 이 **사라지고** `ls` 가 인자 없이 현재 디렉터리를 찍으며 **성공**한다.
  #   (selftest 가 이걸 잡았다.) find 로 명시한다.
  if [ -z "$(find "$d" -maxdepth 1 -name '*.in' -type f 2>/dev/null | head -1)" ]; then
    printf "  · %-42s 잡 아님 — .in 이 없다 (구조/보관 폴더)\n" "$(basename "$d")"
    continue
  fi
  f=$(ls -1 "$d"/*.out 2>/dev/null | head -1)
  k=$(classify "${f:-/dev/null}")
  # 종료마커가 없다 ≠ 돌고 있다. **커널 cwd 로 생사를 갈라야** 마커 없이 죽은 잡이 걸린다.
  if [ "$k" = no_marker ]; then
    if qe_alive_in_dir "$d"; then k=running; else k=dead; fi
  fi
  m=$(restart_mode_for "$d" "$k")
  case "$k" in
    conv)    printf "  ✅ %-42s 수렴 — 건드리지 않는다\n" "$(basename "$d")" ;;
    running) printf "  ▶ %-42s 도는 중 — 건드리지 않는다 (pw.x/neb.x 가 이 폴더에 살아있다)\n" "$(basename "$d")" ;;
    dead)    printf "  ☠ %-42s 죽음(종료마커 없음 · 프로세스 없음) → %s\n" "$(basename "$d")" "$m"
             TODO+=("$d"); MODES+=("$m") ;;
    none)    printf "  · %-42s .out 없음 — 건너뛴다\n" "$(basename "$d")" ;;
    exhaust) printf "  ⛔ %-42s nstep소진 → nstep %s · %s\n" "$(basename "$d")" "$NSTEP" "$m"
             TODO+=("$d"); MODES+=("$m") ;;
    stopped) printf "  ⏸ %-42s 사람이 세움(EXIT·max_seconds) → nstep %s · %s (BFGS 이력 승계)\n" "$(basename "$d")" "$NSTEP" "$m"
             TODO+=("$d"); MODES+=("$m") ;;
    oom)     printf "  ☠ %-42s GPU OOM → %s (한 번에 하나만)\n" "$(basename "$d")" "$m"
             TODO+=("$d"); MODES+=("$m") ;;
    error)   printf "  ☠ %-42s QE 오류 — **자동으로 안 건다**. 원인부터 본다:\n" "$(basename "$d")"
             grep -a -A2 "Error in routine" "$f" 2>/dev/null | sed 's/^/       /' | head -3 ;;
  esac
done
echo
[ "${#TODO[@]}" -gt 0 ] || { echo "다시 걸 것이 없다."; exit 0; }
[ "$RUN" = 1 ] || { echo "판정만 했다. 실제로 걸려면 --run 을 준다."; exit 0; }

acquire_lock || {
  echo "⛔ 이미 돌고 있다 (pid $(cat "$LOCKDIR/pid" 2>/dev/null)) — **걸지 않는다.**"
  echo "   같은 잡에 pw.x 가 둘이면 같은 .save 를 서로 덮어써 둘 다 못 쓰게 된다 (09-07 실물)."
  echo "   상태:  bash tools/sei/watch_qe_relax.sh"
  echo "   정말 갈아엎으려면:  pkill -f restart_qe_relax; pkill -f 'pw\\.x -in'"
  exit 3
}
trap 'rm -rf "$LOCKDIR"' EXIT

# shellcheck disable=SC1090
. "$(dirname "${BASH_SOURCE[0]}")/qe_env.sh"
PWX="${PW:-$(command -v pw.x)}"
[ -x "$PWX" ] || { echo "⛔ pw.x 를 못 찾았다: $PWX"; exit 2; }

for i in "${!TODO[@]}"; do
  d="${TODO[$i]}"; m="${MODES[$i]}"
  src=$(ls -1 "$d"/*.in 2>/dev/null | head -1)
  [ -f "$src" ] || { echo "⛔ 입력 없음: $d"; continue; }
  out="${src%.in}.out"
  # ── GPU 게이트: 이게 r1·r2 를 죽인 원인이다. 한 번에 하나만. ──
  f=$(gpu_free_mib)
  while [ "$f" -lt "$GPU_FREE_MIB" ]; do
    [ "$WAIT" = 1 ] || { echo "⛔ GPU 여유 ${f} MiB < ${GPU_FREE_MIB} — 멈춘다"; exit 1; }
    echo "· GPU 여유 ${f} MiB — 빌 때까지 기다린다 (5분마다)"; sleep 300; f=$(gpu_free_mib)
  done
  # 옛 출력은 **지우지 않고** 밀어 둔다 — 재구성 이력이 증거다
  n=0; while [ -e "$out.$(printf %03d $n)" ]; do n=$((n+1)); done
  [ -f "$out" ] && mv "$out" "$out.$(printf %03d $n)"
  new="${src%.in}.restart.in"
  patch_in "$src" "$new" "$m" "$NSTEP" || { echo "⛔ 입력 패치 실패: $src"; continue; }
  echo "▶ $(basename "$d")  mode=$m nstep=$NSTEP  (GPU 여유 ${f} MiB)"
  ( cd "$d" && "$MPIRUN" -np 1 --oversubscribe "$PWX" -in "$(basename "$new")" > "$(basename "$out")" 2>&1 )
  k=$(classify "$out")
  case "$k" in
    conv)    echo "   ✅ 수렴 — ⚠ 정류점이지 바닥상태 보장은 아니다" ;;
    exhaust) echo "   ⛔ nstep $NSTEP 도 소진했다. 이건 **보고할 사실**이다 —"
             echo "      더 늘리기 전에 왜 안 끝나는지부터 본다 (재구성이 깊다는 신호일 수 있다)." ;;
    oom)     echo "   ☠ 또 OOM — 다른 프로세스가 GPU 를 물고 있다. nvidia-smi 로 확인." ;;
    *)       echo "   ☠ $k — .out 을 본다" ;;
  esac
done
echo "끝. 워치로 확인: bash tools/sei/watch_qe_relax.sh"

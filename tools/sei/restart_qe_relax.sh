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
#   → conv | exhaust | oom | error | running | none
classify() {
  local f="$1"
  [ -f "$f" ] || { echo none; return; }
  if   grep -aq "bfgs converged in" "$f" 2>/dev/null;                      then echo conv
  elif grep -aq "The maximum number of steps has been" "$f" 2>/dev/null;   then echo exhaust
  elif grep -aqi "CUDA_ERROR_OUT_OF_MEMORY\|Accelerator Fatal Error" "$f"; then echo oom
  elif grep -aq "Error in routine" "$f" 2>/dev/null;                       then echo error
  elif grep -aq "JOB DONE" "$f" 2>/dev/null;                               then echo conv
  else echo running; fi
}

# 재시작 방식: 이어달릴 save 가 실제로 있나로 정한다 (판정만으로는 못 정한다).
#   ⛔ nstep 소진인데 save 가 없으면 `restart` 는 즉사한다 — 그때는 from_scratch 다.
restart_mode_for() {
  local dir="$1" kind="$2"
  local sv; sv=$(find "$dir" -maxdepth 3 -name "*.save" -type d 2>/dev/null | head -1)
  if [ "$kind" = "exhaust" ] && [ -n "$sv" ] && [ -n "$(ls -A "$sv" 2>/dev/null)" ]; then
    echo restart
  else
    echo from_scratch
  fi
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
  mkdir -p "$T/none"
  for c in conv exhaust oom err run none; do
    case "$c" in conv) w=conv;; exhaust) w=exhaust;; oom) w=oom;; err) w=error;; run) w=running;; none) w=none;; esac
    g=$(classify "$T/$c/00_control_relax.out")
    chk "$([ "$g" = "$w" ] && echo 1 || echo 0)" "판정 $c → $g (기대 $w)"
  done
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
  f=$(ls -1 "$d"/*.out 2>/dev/null | head -1)
  k=$(classify "${f:-/dev/null}")
  m=$(restart_mode_for "$d" "$k")
  case "$k" in
    conv)    printf "  ✅ %-42s 수렴 — 건드리지 않는다\n" "$(basename "$d")" ;;
    running) printf "  ▶ %-42s 도는 중 — 건드리지 않는다\n" "$(basename "$d")" ;;
    none)    printf "  · %-42s .out 없음 — 건너뛴다\n" "$(basename "$d")" ;;
    exhaust) printf "  ⛔ %-42s nstep소진 → nstep %s · %s\n" "$(basename "$d")" "$NSTEP" "$m"
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

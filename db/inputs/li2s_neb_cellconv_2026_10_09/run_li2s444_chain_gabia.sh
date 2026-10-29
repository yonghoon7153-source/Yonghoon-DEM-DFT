#!/usr/bin/env bash
# =============================================================================
# run_li2s444_chain_gabia.sh — Li₂S 4×4×4 셀 수렴 NEB 를 gabia 탄성 점 사이에 끼워 **사람 손 없이 끝까지** 돈다.
#
# 왜 (2026-10-30 · 사용자 '이번에는 확실하게 해'): 10-27 에 붙듦만 걸고 실행기를 안 드려서, 13_m 이 끝난 뒤
#   탄성 러너가 언 채 GPU 가 31 시간 비었다 (사람이 이어 줘야 하는 이음매에서 끊겼다). 이번에는 그 이음매를 없앤다 —
#   12_p 가 스스로 끝나는 순간 붙들고 → 곧바로 Li₂S → 끝나거나 **어디서 멈추든** 탄성 러너를 푼다.
#   결정: D-2026-10-09-li2s-neb-cellconv (카드 li2s_cellconv_card_2026_09_01 C1–C3 · §3b) + 순서 개정 D-2026-10-30-li2s-444-after-12p.
#
# 순서
#   0 점검   — worktree · 입력 · 결정 둘 active · 붙듦 도구 selftest · QE 환경 (qe_env.sh · ldd) · 잠금 (flock)
#   1 기다림 — <POINT>.in 의 pw.x 가 도는지 본다 (최대 WAIT_START_S). 그 점이 이미 끝났으면 멈춘다 — 다른 점을 붙들지 않는다.
#   2 붙듦   — pause_relax_at_bfgs.sh --hold : 그 pw.x 가 스스로 끝날 때까지 기다리고 러너를 언 채 둔다 (0 이어야 다음).
#              ★ 여기서부터는 어떻게 끝나든 (성공 · 실패 · 신호 · 셸 꺼짐) 러너를 **딱 한 번** 푼다 (trap EXIT).
#   3 GPU 빔 — memory.used ≤ IDLE_MAX_MIB · 계산 프로세스 0 개 · IDLE_GAP_S 간격 두 번 (붙든 점의 pw.x 가 GPU 를 놨는가).
#   4 P1     — KNOBS 순서 (david → ppcg → paro) 로 scf_probe (electron_maxstep 3 · 값 아님) 를 돌리며 VRAM 을 0.5 s 마다 잰다.
#              통과 = 끝까지 돎 (JOB DONE · 수렴 판정 줄 · total energy · 오류 줄 없음) ∧ 최고치 ≤ P1_MAX_MIB.
#              **처음 통과한 손잡이**를 쓴다 (가장 가벼운 것을 고르지 않는다). 통과 기준은 실행 기록에 결과 전에 적었다.
#              비용 어림 = 반복당 시간 × 3275 반복 (끝점 2×30 BFGS×15 + no-CI 25×5×15 + CI 10×5×10) — MAX_EST_DAYS 넘으면 멈춘다.
#   5 사슬   — run_chain_kgy.sh (MIN_L=14 · EXTRA_BUILD="--diagonalization <손잡이>"): 끝점 이완 G1 → no-CI G2a → CI G2b.
#   6 풀기   — trap (위 ★). 풀기가 실패하면 종료 40 + 사람이 풀 명령을 찍는다.
#
# 종료 코드: 0 끝 · 2 점검 · 3 그 점을 못 봄 (안 붙듦) · 4 붙듦 실패 (러너는 붙듦 도구가 이미 풀었거나 안 건드렸다) ·
#   5 GPU 안 빔 · 20 P1 모두 불통과 · 21 비용 어림 초과 · 30+N 사슬 실패 (N = run_chain_kgy.sh 코드 10–15) · 40 풀기 실패 ·
#   130 신호. 3 · 4 를 뺀 나머지는 전부 **러너를 푼 뒤** 끝난다.
#
# ⛔ 이 도구가 못 하는 것
#   · G3–G5 (대칭 · payload 대조 · 경로 모양) 판정 — 회수 뒤 레포에서 한다 (10-09 카드 §5)
#   · 실패했을 때 무엇을 할지 정하기 — P1 불통과 · 비용 초과 · 사슬 실패는 멈추고 사용자에게 넘긴다 (설정을 바꿔 다시 돌지 않는다)
#   · 붙든 동안 탄성 점을 바꾸거나 판정하기 · POINT 가 아닌 점을 붙들기 · 기계 전원이 꺼진 뒤 이어 돌기 (다시 띄우면 0 부터 —
#     끝난 끝점은 run_sei_neb.sh 가 건너뛰지만 P1 은 다시 잰다)
#   · 이 스크립트를 SIGKILL 로 죽이면 trap 이 안 돈다 — 그때는 사람이: bash <PAUSE> --release <HOLDF>
#
#   W=/data/work/wt_li2s444_1027 bash db/inputs/li2s_neb_cellconv_2026_10_09/run_li2s444_chain_gabia.sh
#   bash db/inputs/li2s_neb_cellconv_2026_10_09/run_li2s444_chain_gabia.sh --selftest
# =============================================================================
set -uo pipefail

D_REL=db/inputs/li2s_neb_cellconv_2026_10_09
DEC_MAIN=D-2026-10-09-li2s-neb-cellconv
DEC_ORDER=D-2026-10-30-li2s-444-after-12p

main() {
  W=${W:?W=<worktree> 가 필요하다}
  R=${R:-/data/work/runs/li2s_neb_cellconv_444_1027}
  EL=${EL:-/data/work/runs/elastic_modelc_2x}
  POINT=${POINT:-strain_12_p}
  RUNNER_PAT=${RUNNER_PAT:-run_elastic_relaxedion_gabia.sh}
  HOLDF=${HOLDF:-$R/elastic_hold_${POINT#strain_}.txt}
  UPY=${UPY:-/data/apps/miniforge3/envs/uma/bin/python}
  PAUSE=${PAUSE:-$W/tools/elastic/pause_relax_at_bfgs.sh}
  CHAIN=${CHAIN:-$W/$D_REL/run_chain_kgy.sh}
  NVSMI=${NVSMI:-nvidia-smi}
  KNOBS=${KNOBS:-"david ppcg paro"}
  P1_MAX_MIB=${P1_MAX_MIB:-46000}; IDLE_MAX_MIB=${IDLE_MAX_MIB:-2000}; MAX_EST_DAYS=${MAX_EST_DAYS:-30}
  WAIT_START_S=${WAIT_START_S:-7200}; POLL=${POLL:-30}; P1_TIMEOUT_S=${P1_TIMEOUT_S:-10800}; IDLE_GAP_S=${IDLE_GAP_S:-30}
  RELEASED=0; REL_FAIL=0; HELD=0

  mkdir -p "$R" || exit 2
  exec 9>"$R/.chain.lock"
  flock -n 9 || { echo "⛔ 이미 돌고 있다 ($R/.chain.lock)"; exit 2; }
  LOG=$R/chain.log
  say "▶ 시작 · W=$W · HEAD $(git -C "$W" rev-parse --short HEAD 2>/dev/null || echo '?') · POINT=$POINT · R=$R"

  # ── 0 점검 ─────────────────────────────────────────────────────────────────
  stage "0 점검"
  for p in "$W/$D_REL/pseudo" "$W/$D_REL/relaxed" "$W/tools/sei/build_neb_inputs.py" "$CHAIN" "$PAUSE"; do
    [ -e "$p" ] || { say "⛔ 없음: $p"; exit 2; }; done
  "$UPY" -c "import ase" 2>/dev/null || { say "⛔ $UPY 에 ase 가 없다"; exit 2; }
  "$UPY" - "$W/db/governance/decisions.json" "$DEC_MAIN" "$DEC_ORDER" <<'PY' || { say "⛔ 결정이 active 가 아니다 ($DEC_MAIN · $DEC_ORDER)"; exit 2; }
import json, sys
d = json.load(open(sys.argv[1]))
st = {x.get("id"): x.get("decision_state") for x in d.get("decisions", [])}
bad = [i for i in sys.argv[2:] if st.get(i) != "active"]
print("  결정:", " · ".join(f"{i} {st.get(i)}" for i in sys.argv[2:]))
sys.exit(1 if bad else 0)
PY
  bash "$PAUSE" --selftest > "$R/pause_selftest.log" 2>&1 || { say "⛔ 붙듦 도구 selftest 실패 ($R/pause_selftest.log)"; exit 2; }
  if [ "${QE_ENV_SKIP:-0}" != 1 ]; then
    PW=${PW:-/data/apps/qe-7.4.1-gpu/bin/pw.x}; NEB=${NEB:-/data/apps/qe-7.4.1-gpu/bin/neb.x}
    QE_FROM_LDD=1 PW="$PW"
    # shellcheck disable=SC1090
    . "$W/tools/sei/qe_env.sh" _sourced >/dev/null 2>&1
    [ -z "${QE_ENV_ERROR:-}" ] || { say "⛔ QE 환경: $QE_ENV_ERROR"; exit 2; }
  fi
  : "${PW:?}" "${NEB:?}" "${MPIRUN:?}"; MPI_NP=${MPI_NP:--np 1}; MPI_OVERSUB=${MPI_OVERSUB:-}
  for x in "$PW" "$NEB" "$MPIRUN"; do [ -x "$x" ] || { say "⛔ 실행파일 아님: $x"; exit 2; }; done
  say "✓ 점검 — PW $PW · NEB $NEB · MPIRUN $MPIRUN"

  # ── 1 그 점의 pw.x 를 본다 ─────────────────────────────────────────────────
  stage "1 $POINT 를 기다림"
  local waited=0
  until pw_running; do
    if [ -f "$EL/$POINT.out" ] && grep -aq "JOB DONE" "$EL/$POINT.out"; then
      say "⛔ $POINT 는 이미 끝났다 — 다른 점을 붙들지 않는다 (탄성 러너는 안 건드림)"; exit 3; fi
    [ "$waited" -ge "$WAIT_START_S" ] && { say "⛔ $POINT 의 pw.x 를 ${WAIT_START_S}s 동안 못 봤다 (탄성 러너는 안 건드림)"; exit 3; }
    sleep "$POLL"; waited=$((waited + POLL))
  done
  say "✓ $POINT pw.x 가 돈다 — 붙듦을 건다 (이 점은 끝까지 돌고, 끝나면 러너를 언 채 둔다)"

  # ── 2 붙듦 ────────────────────────────────────────────────────────────────
  stage "2 붙듦 — $POINT 가 끝나길 기다림"
  bash "$PAUSE" --in "$POINT.in" --runner "$RUNNER_PAT" --hold "$HOLDF" >> "$R/hold_${POINT#strain_}.log" 2>&1
  local hrc=$?
  if [ "$hrc" -ne 0 ]; then
    say "⛔ 붙듦 실패 (rc $hrc) — 탄성 러너는 붙듦 도구가 이미 풀었거나 안 건드렸다 · Li₂S 안 돈다 ($R/hold_${POINT#strain_}.log)"
    exit 4
  fi
  HELD=1
  trap on_exit EXIT
  trap 'exit 130' INT TERM HUP
  say "✓ $POINT 끝 · 탄성 러너 붙듦 ($HOLDF) — 여기서부터는 어떻게 끝나든 러너를 푼다"

  # ── 3 GPU 가 비었는가 ───────────────────────────────────────────────────────
  stage "3 GPU 빔 확인"
  local i u a
  for i in 1 2; do
    u=$(gpu_used); a=$(gpu_apps)
    say "  GPU 표본 $i: ${u:-?} MiB · 계산 프로세스 ${a:-?}"
    if [ -z "$u" ] || [ "$u" -gt "$IDLE_MAX_MIB" ] || [ "${a:-1}" -ne 0 ]; then
      say "⛔ GPU 가 비지 않았다 — Li₂S 를 안 띄우고 탄성을 푼다"; exit 5; fi
    [ "$i" = 1 ] && sleep "$IDLE_GAP_S"
  done

  # ── 4 P1 ────────────────────────────────────────────────────────────────
  stage "4 P1"
  local KNOB="" k
  for k in $KNOBS; do
    if p1_one "$k"; then KNOB=$k; break; fi
  done
  if [ -z "$KNOB" ]; then
    say "⛔ P1 — 손잡이 $KNOBS 모두 불통과 · NEB 안 던진다 (카드 §3b) · 다음은 사용자 결정"; exit 20; fi
  local est
  est=$(p1_field "$KNOB" est_days)
  say "✓ P1 — 손잡이 $KNOB · 최고 $(p1_field "$KNOB" peak_mib) MiB · 반복당 $(p1_field "$KNOB" t_iter_s) s · 어림 ${est} 일"
  if awk -v e="$est" -v m="$MAX_EST_DAYS" 'BEGIN{exit !(e=="" || e>m)}'; then
    say "⛔ 비용 어림 ${est} 일 > ${MAX_EST_DAYS} 일 — 멈추고 탄성을 푼다 (사용자 결정)"; exit 21; fi

  # ── 5 사슬 ────────────────────────────────────────────────────────────────
  stage "5 사슬 (끝점 → no-CI → CI) · 손잡이 $KNOB"
  say "▶ 사슬 — run_chain_kgy.sh · MIN_L 14 · --diagonalization $KNOB · WORK $R/neb"
  MIN_L=14 EXTRA_BUILD="--diagonalization $KNOB" W="$W" D="$D_REL" UPY="$UPY" WORK="$R/neb" \
    PW="$PW" NEB="$NEB" MPIRUN="$MPIRUN" bash "$CHAIN" >> "$R/chain_neb.log" 2>&1
  local crc=$?
  if [ "$crc" -ne 0 ]; then say "⛔ 사슬 실패 (rc $crc · $R/chain_neb.log 끝)"; tail -3 "$R/chain_neb.log" | while read -r l; do say "   $l"; done
    exit $((30 + crc)); fi
  stage "끝 — G1 · G2a · G2b 통과 (G3–G5 는 회수 뒤)"
  say "✅ Li₂S 4×4×4 사슬 끝 — $(grep -a 'activation energy' "$R/neb/li2s/neb.out" 2>/dev/null | tail -2 | tr -s ' ' | paste -sd'|')"
  exit 0
}

say()   { echo "[$(date '+%F %T')] $*" | tee -a "${LOG:-/dev/null}"; }
stage() { echo "$(date '+%F %T') $*" >> "$R/chain_stage.txt"; }

pw_running() {   # comm = pw.x 이고 명령줄에 <POINT>.in 이 있는 프로세스 (CLAUDE.md: pgrep 은 자기를 센다 — comm 으로 거른다)
  if [ -n "${PW_RUNNING_CMD:-}" ]; then eval "$PW_RUNNING_CMD"; return; fi
  local x
  for x in $(pgrep -f "$POINT.in" 2>/dev/null); do
    [ "$(cat /proc/"$x"/comm 2>/dev/null)" = pw.x ] && return 0
  done
  return 1
}
gpu_used() { $NVSMI --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -dc '0-9'; }
gpu_apps() { $NVSMI --query-compute-apps=pid --format=csv,noheader 2>/dev/null | grep -c '[0-9]'; }

on_exit() {      # 붙든 뒤 어떤 식으로 끝나든 러너를 딱 한 번 푼다
  local rc=$?
  trap - EXIT INT TERM HUP
  if [ "$HELD" = 1 ] && [ "$RELEASED" = 0 ]; then
    RELEASED=1
    if bash "$PAUSE" --release "$HOLDF" >> "$LOG" 2>&1; then
      say "✅ 탄성 러너 풀림 — 다음 탄성 점으로 잇는다 (이 스크립트 rc $rc)"
    else
      REL_FAIL=1
      say "⛔⛔ 탄성 러너 풀기 실패 — 사람이: bash $PAUSE --release $HOLDF"
      rc=40
    fi
    stage "탄성 러너 풀기 $([ "$REL_FAIL" = 1 ] && echo 실패 || echo 끝) · rc $rc"
  fi
  exit "$rc"
}

p1_one() {       # $1 = 손잡이 → 0 통과 · 1 불통과 (기록은 $R/p1.json 에 쌓는다)
  local k=$1 P="$R/p1_$1" IN SPID prc t0 t1
  rm -rf "$P"; mkdir -p "$P"
  say "▶ P1 $k — 입력 만들기"
  ( cd "$W" && "$UPY" tools/sei/build_neb_inputs.py --work "$P" --pseudo_dir "$W/$D_REL/pseudo" \
      --relaxed_from "$W/$D_REL/relaxed" --only li2s --min_l 14 --scf_probe --allow_unrelaxed_endpoints \
      --diagonalization "$k" ) > "$P/build.log" 2>&1
  IN="$P/li2s/scf_probe/scf_probe.in"
  if [ ! -f "$IN" ] || ! grep -aq "diagonalization *= *'$k'" "$IN"; then
    say "  ✗ P1 $k — 입력이 안 생겼거나 손잡이가 안 들어갔다 ($P/build.log)"; p1_record "$k" 0 0 0 1 "build"; return 1; fi
  "$NVSMI" --query-gpu=memory.used --format=csv,noheader,nounits -lms 500 > "$P/vram.log" 2>/dev/null &
  SPID=$!
  t0=$(date +%s)
  ( cd "$(dirname "$IN")" && timeout --signal=TERM "$P1_TIMEOUT_S" $MPIRUN $MPI_NP $MPI_OVERSUB "$PW" -in scf_probe.in > scf_probe.out 2>&1 )
  prc=$?
  t1=$(date +%s)
  kill "$SPID" 2>/dev/null; wait "$SPID" 2>/dev/null
  local OUT="$(dirname "$IN")/scf_probe.out" peak done_ok err
  peak=$(tr -dc '0-9\n' < "$P/vram.log" | sort -n | tail -1); peak=${peak:-0}
  done_ok=0
  grep -aq "JOB DONE" "$OUT" && grep -aqE "convergence (NOT achieved|has been achieved)" "$OUT" \
    && grep -aq "total energy" "$OUT" && done_ok=1
  err=0; grep -aqiE "out of memory|cudaErrorMemoryAllocation|Error in routine|cuda error" "$OUT" && err=1
  p1_record "$k" "$done_ok" "$peak" "$((t1 - t0))" "$err" "rc$prc"
  if [ "$done_ok" = 1 ] && [ "$err" = 0 ] && [ "$peak" -le "$P1_MAX_MIB" ]; then
    say "  ✓ P1 $k 통과 — 최고 ${peak} MiB ≤ $P1_MAX_MIB · $((t1 - t0)) s"; return 0; fi
  say "  ✗ P1 $k 불통과 — 끝까지 돎 $done_ok · 오류 $err · 최고 ${peak} MiB (문턱 $P1_MAX_MIB) · rc $prc"
  return 1
}

p1_record() {    # knob done peak wall err note → $R/p1.json (반복당 시간 · 비용 어림 포함)
  "$UPY" - "$R" "$@" <<'PY'
import json, os, re, sys
R, k, done, peak, wall, err, note = sys.argv[1:8]
out = os.path.join(R, f"p1_{k}", "li2s", "scf_probe", "scf_probe.out")
t = open(out, errors="ignore").read() if os.path.isfile(out) else ""
cpu = [float(x) for x in re.findall(r"total cpu time spent up to now is\s+([\d.]+)\s*secs", t)]
n_it = len(re.findall(r"iteration #\s*\d+", t))
if len(cpu) >= 2:
    t_iter = (cpu[-1] - cpu[0]) / (len(cpu) - 1); src = "cpu time diff"
elif n_it:
    t_iter = float(wall) / n_it; src = "wall / iterations (setup included)"
else:
    t_iter = None; src = "none"
N_ITER = 2 * 30 * 15 + 25 * 5 * 15 + 10 * 5 * 10   # 끝점 · no-CI · CI — 결과 전에 정한 어림 식 (실행 기록)
est = round(t_iter * N_ITER / 86400, 2) if t_iter else None
p = os.path.join(R, "p1.json")
d = json.load(open(p)) if os.path.isfile(p) else {"criteria": "끝까지 돎 ∧ 오류 줄 없음 ∧ 최고 VRAM ≤ P1_MAX_MIB · 처음 통과한 손잡이",
                                                 "n_iter_model": N_ITER, "runs": {}}
d["runs"][k] = {"completed": done == "1", "error_line": err == "1", "peak_mib": int(peak), "wall_s": int(wall),
                "t_iter_s": round(t_iter, 1) if t_iter else None, "t_iter_source": src, "iterations_seen": n_it,
                "est_days": est, "note": note}
json.dump(d, open(p, "w"), ensure_ascii=False, indent=1)
PY
}
p1_field() { "$UPY" -c "import json,sys; print(json.load(open('$R/p1.json'))['runs']['$1'].get('$2'))"; }

# ── selftest — 가짜 GPU · 가짜 pw.x · 가짜 붙듦 도구 · 가짜 사슬로 갈래마다 잰다 (음성 포함) ──────────────
selftest() {
  local T; T=$(mktemp -d); local ok=0 bad=0 self; self=$(readlink -f "$0")
  mkdir -p "$T/bin" "$T/wt/$D_REL/pseudo" "$T/wt/$D_REL/relaxed" "$T/wt/tools/sei" "$T/wt/tools/elastic" "$T/wt/db/governance" "$T/el"
  cat > "$T/bin/nvidia-smi" <<'EOF'
#!/usr/bin/env bash
V=$(cat "$FAKE_T/vram" 2>/dev/null || echo 1)
case "$*" in
  *compute-apps*) cat "$FAKE_T/apps" 2>/dev/null ;;
  *-lms*) while :; do cat "$FAKE_T/vram" 2>/dev/null || echo 1; sleep 0.1; done ;;
  *) echo "$V" ;;
esac
EOF
  cat > "$T/bin/mpirun" <<'EOF'
#!/usr/bin/env bash
while [ $# -gt 0 ]; do case "$1" in -np|-n) shift 2 ;; --oversubscribe) shift ;; *) break ;; esac; done
exec "$@"
EOF
  cat > "$T/bin/pw.x" <<'EOF'
#!/usr/bin/env bash
k=$(grep -o "diagonalization *= *'[a-z]*'" scf_probe.in | sed "s/.*'\([a-z]*\)'/\1/")
spec=$(eval echo "\${FAKE_PW_$k:-ok:30000:60}")
IFS=: read -r how peak cpu <<< "$spec"
echo "$peak" > "$FAKE_T/vram"; sleep 0.6; echo 1 > "$FAKE_T/vram"
if [ "$how" = err ]; then echo "     Error in routine cdiaghg (1): problems computing cholesky"; exit 1; fi
for i in 1 2 3; do echo "     iteration #  $i"; echo "     total cpu time spent up to now is $(( i * cpu )).0 secs"; done
echo "!    total energy              =   -1234.5 Ry"; echo "     convergence NOT achieved after 3 iterations: stopping"; echo "   JOB DONE."
EOF
  cat > "$T/bin/neb.x" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
  cat > "$T/pause.sh" <<'EOF'
#!/usr/bin/env bash
echo "$*" >> "$FAKE_T/pause.log"
case "$*" in
  *--selftest*) echo "selftest: ⭕ 44 · ⛔ 0"; exit 0 ;;
  *--hold*) echo "pid=1" > "${@: -1}"; exit "${FAKE_HOLD_RC:-0}" ;;
  *--release*) echo r >> "$FAKE_T/released"; exit "${FAKE_REL_RC:-0}" ;;
esac
EOF
  cat > "$T/chain.sh" <<'EOF'
#!/usr/bin/env bash
echo "MIN_L=$MIN_L EXTRA_BUILD=$EXTRA_BUILD WORK=$WORK" >> "$FAKE_T/chain.log"
sleep "${FAKE_CHAIN_SLEEP:-0}"
exit "${FAKE_CHAIN_RC:-0}"
EOF
  cat > "$T/upy" <<'EOF'
#!/usr/bin/env bash
if [ "${1:-}" = tools/sei/build_neb_inputs.py ]; then
  shift; w=""; k=""
  while [ $# -gt 0 ]; do case "$1" in --work) w=$2; shift 2 ;; --diagonalization) k=$2; shift 2 ;; *) shift ;; esac; done
  mkdir -p "$w/li2s/scf_probe"; printf "&ELECTRONS\n    diagonalization = '%s'\n/\n" "$k" > "$w/li2s/scf_probe/scf_probe.in"; exit 0
fi
[ "$*" = "-c import ase" ] && exit 0          # 시험 기계의 python3 에 ase 가 없어도 (gabia 기본 python3) 점검을 통과시킨다
exec python3 "$@"
EOF
  touch "$T/wt/tools/sei/build_neb_inputs.py"
  chmod +x "$T"/bin/* "$T/pause.sh" "$T/chain.sh" "$T/upy"
  printf '{"decisions":[{"id":"%s","decision_state":"active"},{"id":"%s","decision_state":"active"}]}' \
    "$DEC_MAIN" "$DEC_ORDER" > "$T/wt/db/governance/decisions.json"
  git -C "$T/wt" init -q 2>/dev/null

  run() {   # $1 이름 · 나머지 = 환경 덮어쓰기 → rc 를 $T/rc 에
    local name=$1; shift
    rm -rf "$T/R"; rm -f "$T/pause.log" "$T/released" "$T/chain.log"; echo 1 > "$T/vram"; : > "$T/apps"
    env FAKE_T="$T" PATH="$T/bin:$PATH" W="$T/wt" R="$T/R" EL="$T/el" UPY="$T/upy" PAUSE="$T/pause.sh" CHAIN="$T/chain.sh" \
      NVSMI="$T/bin/nvidia-smi" QE_ENV_SKIP=1 PW="$T/bin/pw.x" NEB="$T/bin/neb.x" MPIRUN="$T/bin/mpirun" \
      PW_RUNNING_CMD=true POLL=1 WAIT_START_S=2 IDLE_GAP_S=0 "$@" bash "$self" > "$T/out_$name" 2>&1
    echo $? > "$T/rc"
  }
  rel()  { [ -f "$T/released" ] && wc -l < "$T/released" | tr -d ' ' || echo 0; }
  chk()  { if eval "$2"; then ok=$((ok + 1)); echo "  ✓ $1"; else bad=$((bad + 1)); echo "  ✗ $1  (rc $(cat "$T/rc") · 풀기 $(rel))"; tail -3 "$T"/out_* 2>/dev/null | tail -3; fi; }

  run A FAKE_PW_david=err FAKE_PW_ppcg=ok:47000:60 FAKE_PW_paro=ok:30000:60
  chk "A 정상 — david 오류 · ppcg 최고치 초과 · paro 통과 → paro 로 사슬 · 풀기 1 번 · rc 0" \
      '[ "$(cat $T/rc)" = 0 ] && [ "$(rel)" = 1 ] && grep -q "MIN_L=14 EXTRA_BUILD=--diagonalization paro" $T/chain.log'
  cat > "$T/chkA.py" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1]))["runs"]
assert set(d) == {"david", "ppcg", "paro"}, d.keys()
assert d["ppcg"]["peak_mib"] >= 47000 and not d["david"]["completed"] and d["paro"]["t_iter_s"] == 60.0, d
EOF
  chk "A P1 기록 — p1.json 에 세 손잡이 · david 미완 · ppcg 최고 47000 · paro 반복당 60 s" 'python3 "$T/chkA.py" "$T/R/p1.json"'
  run B FAKE_HOLD_RC=6
  chk "B [음성] 붙듦 실패 (rc 6) → rc 4 · 풀기 0 · P1 안 함" \
      '[ "$(cat $T/rc)" = 4 ] && [ "$(rel)" = 0 ] && [ ! -d $T/R/p1_david ]'
  run C FAKE_T_IDLE=1 IDLE_MAX_MIB=0
  chk "C [음성] GPU 가 안 비었다 → rc 5 · 풀기 1 번 · 사슬 안 함" \
      '[ "$(cat $T/rc)" = 5 ] && [ "$(rel)" = 1 ] && [ ! -f $T/chain.log ]'
  run D FAKE_PW_david=err FAKE_PW_ppcg=err FAKE_PW_paro=ok:48000:60
  chk "D [음성] P1 모두 불통과 → rc 20 · 풀기 1 번 · 사슬 안 함" \
      '[ "$(cat $T/rc)" = 20 ] && [ "$(rel)" = 1 ] && [ ! -f $T/chain.log ]'
  run E FAKE_PW_david=ok:30000:1000
  chk "E [음성] 비용 어림 초과 (반복당 1000 s → 37.9 일 > 30) → rc 21 · 풀기 1 번 · 사슬 안 함" \
      '[ "$(cat $T/rc)" = 21 ] && [ "$(rel)" = 1 ] && [ ! -f $T/chain.log ]'
  run F FAKE_CHAIN_RC=13
  chk "F [음성] 사슬 실패 (no-CI 미수렴 13) → rc 43 · 풀기 1 번" '[ "$(cat $T/rc)" = 43 ] && [ "$(rel)" = 1 ]'
  run G FAKE_REL_RC=11
  chk "G [음성] 정상 끝인데 풀기 실패 → rc 40 (사람이 푼다)" '[ "$(cat $T/rc)" = 40 ]'
  run H PW_RUNNING_CMD=false
  chk "H [음성] 그 점의 pw.x 를 못 봄 → rc 3 · 붙듦 안 검" '[ "$(cat $T/rc)" = 3 ] && ! grep -q -- --hold $T/pause.log'
  echo "   JOB DONE." > "$T/el/strain_12_p.out"
  run I PW_RUNNING_CMD=false WAIT_START_S=100
  chk "I [음성] 12_p 가 이미 끝났다 → 다른 점 안 붙들고 rc 3 (기다리지 않는다)" '[ "$(cat $T/rc)" = 3 ] && grep -q "이미 끝났다" $T/out_I'
  rm -f "$T/el/strain_12_p.out"
  printf '{"decisions":[{"id":"%s","decision_state":"active"},{"id":"%s","decision_state":"proposed"}]}' \
    "$DEC_MAIN" "$DEC_ORDER" > "$T/wt/db/governance/decisions.json"
  run J
  chk "J [음성] 순서 개정이 active 가 아니다 → rc 2 · 붙듦 안 검" '[ "$(cat $T/rc)" = 2 ] && ! grep -qs -- --hold $T/pause.log'
  printf '{"decisions":[{"id":"%s","decision_state":"active"},{"id":"%s","decision_state":"active"}]}' \
    "$DEC_MAIN" "$DEC_ORDER" > "$T/wt/db/governance/decisions.json"
  # K: 사슬 도중 TERM → 풀기 1 번 · rc 130
  rm -rf "$T/R"; rm -f "$T/released" "$T/chain.log"; echo 1 > "$T/vram"; : > "$T/apps"   # ⚠ 앞 갈래의 chain.log 가 남으면 TERM 이 붙듦 전에 간다
  env FAKE_T="$T" PATH="$T/bin:$PATH" W="$T/wt" R="$T/R" EL="$T/el" UPY="$T/upy" PAUSE="$T/pause.sh" CHAIN="$T/chain.sh" \
    NVSMI="$T/bin/nvidia-smi" QE_ENV_SKIP=1 PW="$T/bin/pw.x" NEB="$T/bin/neb.x" MPIRUN="$T/bin/mpirun" \
    PW_RUNNING_CMD=true POLL=1 IDLE_GAP_S=0 FAKE_CHAIN_SLEEP=3 bash "$self" > "$T/out_K" 2>&1 &
  local kp=$!; local n=0
  until [ -f "$T/chain.log" ] || [ $n -ge 100 ]; do sleep 0.2; n=$((n + 1)); done
  kill -TERM "$kp" 2>/dev/null; wait "$kp"; echo $? > "$T/rc"
  pkill -f "$T/chain.sh" 2>/dev/null
  chk "K [음성] 사슬 도중 TERM → 풀기 1 번 · rc 130" '[ "$(cat $T/rc)" = 130 ] && [ "$(rel)" = 1 ]'
  # L: 겹쳐 띄우면 잠금이 막는다
  mkdir -p "$T/R"; exec 8>"$T/R/.chain.lock"; flock -n 8
  env FAKE_T="$T" PATH="$T/bin:$PATH" W="$T/wt" R="$T/R" EL="$T/el" UPY="$T/upy" PAUSE="$T/pause.sh" CHAIN="$T/chain.sh" \
    NVSMI="$T/bin/nvidia-smi" QE_ENV_SKIP=1 PW="$T/bin/pw.x" NEB="$T/bin/neb.x" MPIRUN="$T/bin/mpirun" \
    PW_RUNNING_CMD=true bash "$self" > "$T/out_L" 2>&1; echo $? > "$T/rc"
  exec 8>&-
  chk "L [음성] 이미 돌고 있으면 (잠금) → rc 2" '[ "$(cat $T/rc)" = 2 ] && grep -q "이미 돌고" $T/out_L'
  echo "selftest: ⭕ $ok · ⛔ $bad"
  rm -rf "$T"
  [ "$bad" = 0 ]
}

if [ "${1:-}" = --selftest ]; then selftest; exit $?; fi
main "$@"

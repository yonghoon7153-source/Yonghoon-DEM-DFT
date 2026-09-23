#!/usr/bin/env bash
# =============================================================================
# run_sese_gpu.sh — SE|SE 대조 DFT 잡들을 GPU pw.x 로 **순서대로**, VRAM 가드를 걸고 돌린다.
#
#   입력: tools/wad/se_sym_slab.py --qe_out 이 만든 <IN>/jobs.json + <IN>/<잡>/pw.in
#   결정: D-2026-09-23-wad-se-termination-symmetric · D-2026-09-23-wad-d3-twobody-atm-separate
#         D-2026-09-23-gabia-gpu-exception-sese — gabia 의 *"GPU pw.x ↔ UMA 동시 실행 금지"* 에
#         1저자가 준 **범위 한정 예외**. 아래 가드 조건이 곧 예외의 범위다.
#
# 실행 (gabia · tmux 안에서):
#   RUN=/data/work/runs/wad_sese_2026_09_23
#   WAIT_PIDS="<li2s 시드 PID 들>" ALLOW_UMA_COEXIST=1 \
#     bash tools/wad/run_sese_gpu.sh db/inputs/wad_sese_control_2026_09_23 $RUN
#   DRY_RUN=1 ...                           점검만 (입력 해시·PP·D3 명시·GPU 상태·가드값). 계산 안 함
#   JOBS="01_bulk_scf 02_s_outer_scf" ...   일부만 (기본 = jobs.json 순서 전부)
#   bash tools/wad/run_sese_gpu.sh --selftest
#
# 예외 가드 (1저자 2026-09-23):
#   ① WAIT_PIDS 가 전부 끝날 때까지 기다린다 — `kill -0` + **cmdline 대조**(PID 재사용 방지).
#   ② 시작 직전 GPU 합계 사용량 < START_MAX_MIB (기본 40960 = 40 GB). 넘으면 60 초마다 다시
#      보고, START_WAIT_S (기본 3600) 안에 안 내려가면 **시작하지 않고** 끝낸다.
#   ③ 도는 동안 SAMPLE_S (기본 2) 초마다 합계 사용량을 본다. KILL_MIB (기본 45056 = 44 GB) 를
#      넘으면 **이 러너가 띄운 pw.x·mpirun 을 PID 로** TERM → 15 초 뒤 KILL 하고 러너를 멈춘다.
#      남의 프로세스(UMA)는 건드리지 않는다. 이름으로 죽이지 않는다 (CLAUDE.md: pkill 금지).
#   ④ GPU 에 python(UMA)이 있으면 ALLOW_UMA_COEXIST=1 없이는 시작하지 않는다 —
#      규칙의 기본값은 금지이고, 예외는 **켜야** 켜진다.
#   ④′ 호스트 RAM — gabia 는 CPU 잡(Nd k-탐침 34 GB)과 RAM 을 나눈다. 시작은 MemAvailable ≥
#      HOST_START_MIB (기본 16384), 도는 중 < HOST_KILL_MIB (기본 4096) 면 우리 잡만 멈춘다
#      (OOM 킬러는 우리가 아니라 **가장 큰 잡**을 고른다 — 그게 k-탐침이나 b2o3 일 수 있다).
#   ⑤ 잡마다 피크 합계 VRAM · 우리 pw.x 자기 사용량(읽히면) · 벽시계를 jobs_run.tsv 에 남긴다.
#
# ⛔ 이 스크립트가 **못 하는 것**
#   · VRAM 이 표본 간격(SAMPLE_S)보다 빨리 치솟으면 못 막는다 — 가드는 확률적 보호다.
#     UMA 쪽 CUDA OOM 을 **줄일 뿐 막지 못한다**. b2o3 사건빈도 카드는 16번째 런을 금지하므로
#     (D-2026-09-23-b2o3-framework-event-rate) b2o3 런이 죽으면 그 카드의 판정이 먼저다.
#   · 수렴·물리 타당성은 안 본다 — 완료 판정은 JOB DONE + 수렴 줄(+ relax 면 최종 좌표)뿐.
#   · γ·W 를 계산하지 않는다 — 집계는 `python3 tools/wad/se_sym_slab.py --collect <RUN>`.
#   · 문턱 기본값은 gabia A6000 48 GB 기준이다. kgy(3090 24 GB)에 그대로 쓰지 않는다.
#   · 한 잡이 실패하면 **뒤 잡을 돌리지 않는다** (체계적 원인일 수 있다 — 사람이 본다).
# =============================================================================
set -u
IN=${1:-}; RUN=${2:-}
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# ── 완료 판정 (한 곳에만 둔다 — 재개와 성공이 같은 기준이어야 한다) ─────────────
_done() {   # $1 = pw.out · $2 = calc (scf|relax)
  [ -f "$1" ] || return 1
  grep -aq "JOB DONE" "$1" || return 1
  grep -aq "convergence has been achieved" "$1" || return 1
  if [ "$2" = relax ]; then
    grep -aqE "End final coordinates|bfgs converged" "$1" || return 1
    grep -aq "The maximum number of steps has been reached" "$1" && return 1
  fi
  return 0
}

# ── D3 명시 검사 (D-2026-09-23-wad-d3-twobody-atm-separate enforcement) ─────────
_d3_ok() {  # grimme-d3 를 켠 입력이면 dftd3_threebody 가 적혀 있어야 한다
  if grep -aqiE "vdw_corr *= *'(grimme-d3|dft-d3|d3)'" "$1"; then
    grep -aqiE "dftd3_threebody *= *\.(false|true)\." "$1" || return 1
  fi
  return 0
}

if [ "$IN" = "--selftest" ]; then
  T=$(mktemp -d); n=0; f=0
  ck() { if eval "$2"; then n=$((n+1)); else f=$((f+1)); echo "  ✗ $1"; fi; }
  printf "convergence has been achieved\nJOB DONE\n" > "$T/s.out"
  ck "scf 완료"                         "_done $T/s.out scf"
  ck "⛔scf 완료를 relax 로 보면 미완료"   "! _done $T/s.out relax"
  printf "convergence has been achieved\nbfgs converged\nEnd final coordinates\nJOB DONE\n" > "$T/r.out"
  ck "relax 완료"                       "_done $T/r.out relax"
  printf "convergence has been achieved\nThe maximum number of steps has been reached.\nEnd final coordinates\nJOB DONE\n" > "$T/m.out"
  ck "⛔nstep 소진 relax → 미완료"        "! _done $T/m.out relax"
  printf "JOB DONE\n" > "$T/n.out"
  ck "⛔수렴 줄 없음 → 미완료"            "! _done $T/n.out scf"
  ck "⛔파일 없음 → 미완료"               "! _done $T/없음.out scf"
  printf "  vdw_corr = 'grimme-d3'\n  dftd3_version = 4\n  dftd3_threebody = .false.\n" > "$T/a.in"
  ck "D3 + threebody 명시 → 통과"        "_d3_ok $T/a.in"
  printf "  vdw_corr = 'grimme-d3'\n  dftd3_version = 4\n" > "$T/b.in"
  ck "⛔D3 인데 threebody 없음 → 거부"    "! _d3_ok $T/b.in"
  printf "  vdw_corr = 'none'\n" > "$T/c.in"
  ck "분산 끔 → threebody 불요구"         "_d3_ok $T/c.in"
  rm -rf "$T"; echo "run_sese_gpu selftest: $n 통과 · $f 실패"; [ "$f" = 0 ]; exit $?
fi

[ -n "$IN" ] && [ -f "$IN/jobs.json" ] || { echo "⛔ 입력 폴더에 jobs.json 이 없다: '$IN'"; exit 1; }
[ -n "$RUN" ] || { echo "⛔ 실행 폴더를 두 번째 인자로 준다"; exit 1; }
IN=$(cd "$IN" && pwd)
PWX=${PWX:-/data/apps/qe-7.4.1-gpu/bin/pw.x}
START_MAX_MIB=${START_MAX_MIB:-40960}; KILL_MIB=${KILL_MIB:-45056}
SAMPLE_S=${SAMPLE_S:-2}; START_WAIT_S=${START_WAIT_S:-3600}
ALLOW_UMA_COEXIST=${ALLOW_UMA_COEXIST:-0}; DRY_RUN=${DRY_RUN:-0}; WAIT_PIDS=${WAIT_PIDS:-}
HOST_START_MIB=${HOST_START_MIB:-16384}; HOST_KILL_MIB=${HOST_KILL_MIB:-4096}
[ "$KILL_MIB" -gt "$START_MAX_MIB" ] || { echo "⛔ KILL_MIB($KILL_MIB) 는 START_MAX_MIB($START_MAX_MIB) 보다 커야 한다"; exit 1; }
JOBS=${JOBS:-$(python3 -c "import json;print(' '.join(j['dir'] for j in json.load(open('$IN/jobs.json'))['jobs']))")}

mkdir -p "$RUN"; RUN=$(cd "$RUN" && pwd)
exec 9>"$RUN/.lock"
flock -n 9 || { echo "이미 도는 중이다 ($RUN/.lock) — 중복 실행 안 한다"; exit 0; }
LOG=$RUN/runner.log; TSV=$RUN/jobs_run.tsv
ts() { date '+%F %T'; }
say() { echo "[$(ts)] $*" | tee -a "$LOG"; }
gpu_used() { nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -d ' '; }
gpu_apps() { nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv,noheader,nounits 2>/dev/null; }
self_mib() { gpu_apps | awk -F', *' -v p="$1" '$1==p{print $3}' | head -1; }
host_avail() { awk '/^MemAvailable:/{printf "%d", $2/1024}' /proc/meminfo; }

say "════ run_sese_gpu · IN=$IN · RUN=$RUN · JOBS=[$JOBS]"
say "예외: D-2026-09-23-gabia-gpu-exception-sese · START<${START_MAX_MIB} MiB · KILL>${KILL_MIB} MiB · 표본 ${SAMPLE_S}s · UMA 공존 허용=${ALLOW_UMA_COEXIST}"
command -v nvidia-smi >/dev/null 2>&1 || { say "⛔ nvidia-smi 없음 — GPU 가드를 못 건다. 시작하지 않는다"; exit 2; }

# ── 입력 점검: 해시 고정 · D3 명시 · PP 실재·해시 ────────────────────────────
bad=0
for J in $JOBS; do
  P="$IN/$J/pw.in"
  [ -f "$P" ] || { say "⛔ $P 없음"; bad=1; continue; }
  want=$(python3 -c "import json;print(next((j['pw_in_sha256'] for j in json.load(open('$IN/jobs.json'))['jobs'] if j['dir']=='$J'),''))")
  got=$(sha256sum "$P" | cut -d' ' -f1)
  [ "$want" = "$got" ] || { say "⛔ $J/pw.in 해시가 jobs.json 과 다르다 (입력이 고쳐졌다) — $got"; bad=1; }
  _d3_ok "$P" || { say "⛔ $J: grimme-d3 인데 dftd3_threebody 가 명시되지 않았다 (결정 enforcement)"; bad=1; }
  PD=$(grep -aE "pseudo_dir" "$P" | head -1 | sed -E "s/.*'([^']+)'.*/\1/")
  for U in $(awk '/ATOMIC_SPECIES/{f=1;next} f&&NF==0{exit} f{print $3}' "$P"); do
    [ -f "$PD/$U" ] || { say "⛔ $J: PP 없음 $PD/$U"; bad=1; }
  done
done
[ "$bad" = 0 ] || { say "⛔ 입력 점검 실패 — 시작하지 않는다"; exit 1; }
PD=$(grep -aE "pseudo_dir" "$IN/$(echo $JOBS | awk '{print $1}')/pw.in" | head -1 | sed -E "s/.*'([^']+)'.*/\1/")
for U in $(cat "$IN"/*/pw.in | awk '/ATOMIC_SPECIES/{f=1;next} f&&NF==0{f=0} f{print $3}' | sort -u); do
  say "PP $U sha256 $(sha256sum "$PD/$U" | cut -c1-16)"
done
say "디스크 $(df -h "$RUN" | awk 'NR==2{print $4" 남음 ("$5" 사용)"}')"

# ── GPU 위의 다른 프로세스 (UMA 판정) ──────────────────────────────────────
UMA=0
while IFS= read -r L; do
  [ -n "$L" ] || continue
  p=$(echo "$L" | awk -F', *' '{print $1}'); m=$(echo "$L" | awk -F', *' '{print $3}')
  c=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null | cut -c1-150)
  case "$(cat /proc/$p/comm 2>/dev/null)" in python*) UMA=1;; esac
  say "GPU 사용 중: PID $p · ${m} MiB · $c"
done <<< "$(gpu_apps)"
if [ "$UMA" = 1 ] && [ "$ALLOW_UMA_COEXIST" != 1 ]; then
  say "⛔ GPU 에 python(UMA)이 있다. 규칙 기본값은 GPU pw.x ↔ UMA 동시 금지다 —"
  say "   예외(D-2026-09-23-gabia-gpu-exception-sese)로 돌리려면 ALLOW_UMA_COEXIST=1 을 준다."
  exit 3
fi
say "GPU 합계 사용량 지금 $(gpu_used) MiB · 호스트 MemAvailable $(host_avail) MiB (시작 문턱 ${HOST_START_MIB} · 중단 ${HOST_KILL_MIB})"

if [ "$DRY_RUN" = 1 ]; then say "DRY_RUN — 점검만 하고 끝낸다"; exit 0; fi

# ── ① 기다릴 PID ─────────────────────────────────────────────────────────
declare -A CMD0
for p in $WAIT_PIDS; do
  if [ -r /proc/$p/cmdline ]; then
    CMD0[$p]=$(tr '\0' ' ' < /proc/$p/cmdline)
    say "대기 대상 PID $p · ${CMD0[$p]:0:150}"
  else
    say "대기 대상 PID $p 는 이미 없다 (끝난 것으로 본다)"
  fi
done
for p in "${!CMD0[@]}"; do
  while kill -0 "$p" 2>/dev/null && [ "$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null)" = "${CMD0[$p]}" ]; do
    sleep 60
  done
  say "PID $p 끝남"
done

# ── GPU pw.x 런타임 (ldd 로 바이너리에게 묻는다 — 못 읽으면 시작하지 않는다) ─────
# shellcheck source=/dev/null
source "$HERE/../lib/qe_gpu_runtime.sh"
qe_gpu_require "$PWX" 2>&1 | tee -a "$LOG"
qe_gpu_setup "$PWX" >/dev/null || exit 2
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-1}
# gabia 는 root 계정이다 — OpenMPI 가 root 실행을 가드로 막는다 (CLAUDE.md: --allow-run-as-root 필수)
ROOTFLAG=""; [ "$(id -u)" = 0 ] && ROOTFLAG="--allow-run-as-root"
# 단일 노드는 공유메모리 BTL 만 — 안 정하면 TCP 를 골라 좀비가 된 사고 (run_gap_nscf_gabia.sh 2026-08-31)
MPI_MCA=${MPI_MCA:---mca btl self,vader}

[ -f "$TSV" ] || printf "job\trc\tdone\twall_s\tpeak_total_MiB\tpeak_self_MiB\tkilled\tstart\thost_avail_min_MiB\n" > "$TSV"

for J in $JOBS; do
  CALC=$(python3 -c "import json;print(next(j['calc'] for j in json.load(open('$IN/jobs.json'))['jobs'] if j['dir']=='$J'))")
  D=$RUN/$J; mkdir -p "$D"
  if _done "$D/pw.out" "$CALC"; then say "⏭ $J 이미 완료 — 건너뛴다"; continue; fi
  cp "$IN/$J/pw.in" "$D/pw.in"

  # ② 시작 문턱
  waited=0
  while :; do
    U=$(gpu_used); H=$(host_avail)
    [ -n "$U" ] && [ "$U" -lt "$START_MAX_MIB" ] && [ "${H:-0}" -ge "$HOST_START_MIB" ] && break
    [ "$waited" -ge "$START_WAIT_S" ] && { say "⛔ $J: GPU 합계 ${U} MiB (문턱 ${START_MAX_MIB}) · 호스트 ${H} MiB (문턱 ${HOST_START_MIB}) 가 ${START_WAIT_S}s 지속 — 시작하지 않는다"; exit 4; }
    say "… $J: GPU 합계 ${U} MiB · 호스트 여유 ${H} MiB — 문턱 밖, 60초 뒤 다시"
    sleep 60; waited=$((waited+60))
  done
  say "▶ $J ($CALC) 시작 · GPU 합계 ${U} MiB · 호스트 여유 ${H} MiB"
  t0=$(date +%s); start=$(ts)
  # shellcheck disable=SC2086
  ( cd "$D" && exec "$QE_GPU_MPIRUN" $ROOTFLAG $MPI_MCA -np 1 "$PWX" -nk 1 -in pw.in > pw.out 2> pw.err ) &
  MP=$!
  PW=""
  for _ in $(seq 60); do PW=$(pgrep -P "$MP" | head -1); [ -n "$PW" ] && break; kill -0 "$MP" 2>/dev/null || break; sleep 1; done
  say "   mpirun PID $MP · pw.x PID ${PW:-?}"
  peak=0; peak_self=0; killed=0; hmin=999999
  _stop() {   # 우리 잡만 PID 로 — 이름으로 잡지 않는다
    say "⛔ $J: $1 — 우리 pw.x(${PW:-?})·mpirun($MP) 을 PID 로 멈춘다"
    kill -TERM ${PW:+$PW} "$MP" 2>/dev/null
    for _ in $(seq 15); do kill -0 "$MP" 2>/dev/null || break; sleep 1; done
    kill -KILL ${PW:+$PW} "$MP" 2>/dev/null
    killed=1
  }
  while kill -0 "$MP" 2>/dev/null; do
    U=$(gpu_used); H=$(host_avail)
    [ -n "$H" ] && [ "$H" -lt "$hmin" ] && hmin=$H
    if [ -n "$U" ]; then
      [ "$U" -gt "$peak" ] && peak=$U
      if [ -n "$PW" ]; then S=$(self_mib "$PW"); [ -n "$S" ] && [ "$S" -gt "$peak_self" ] && peak_self=$S; fi
      if [ "$U" -gt "$KILL_MIB" ]; then _stop "GPU 합계 ${U} MiB > ${KILL_MIB}"; break; fi
    fi
    if [ -n "$H" ] && [ "$H" -lt "$HOST_KILL_MIB" ]; then _stop "호스트 MemAvailable ${H} MiB < ${HOST_KILL_MIB}"; break; fi
    sleep "$SAMPLE_S"
  done
  wait "$MP"; rc=$?
  wall=$(( $(date +%s) - t0 ))
  dn=0; _done "$D/pw.out" "$CALC" && dn=1
  printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" "$J" "$rc" "$dn" "$wall" "$peak" "$peak_self" "$killed" "$start" "$hmin" >> "$TSV"
  # 파동함수는 우리 보고량에 안 쓴다 — 디스크만 먹는다 (전하밀도·xml 은 남긴다)
  find "$D/tmp" -name "wfc*.dat" -delete 2>/dev/null; find "$D/tmp" -name "*.wfc*" -delete 2>/dev/null
  say "■ $J rc=$rc 완료=$dn 벽시계 ${wall}s · 피크 합계 ${peak} MiB · 자기 ${peak_self} MiB · 호스트 최저 ${hmin} MiB · 중단=$killed"
  if [ "$killed" = 1 ]; then say "⛔ 가드로 멈췄다 — 러너를 끝낸다 (재시작은 사람이 판단)"; exit 5; fi
  if [ "$dn" != 1 ]; then
    say "⛔ $J 미완료 — 뒤 잡을 돌리지 않는다. 확인: tail -30 $D/pw.out ; cat $D/pw.err"
    exit 6
  fi
done
say "✅ 전부 완료 — 집계: python3 tools/wad/se_sym_slab.py --collect $RUN"

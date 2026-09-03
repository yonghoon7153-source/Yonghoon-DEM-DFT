#!/usr/bin/env bash
# =============================================================================
# watch_qe_relax.sh — QE relax / NEB 잡이 **진짜 살아 있는지** 본다.
#
# ⛔⛔ 왜 만들었나 (2026-09-03) — 감시가 사람을 두 번 속였다.
#   ① gabia `/root/w/li3nd.sh` 가 r1·r2 를 `run` 으로 찍고 있었다. 실제로는 둘 다
#      죽어 있었다 (r1 26시간, r2 는 GPU OOM 으로 재시작 몇 분 만에 사망).
#      그 화면은 **파일만** 보고 프로세스를 안 봤다 — 파일은 죽어도 남는다.
#   ② 같은 날 ORCA gs2 는 반대였다. 프로세스는 살아 있는데 `.out` 이 76시간
#      안 컸다 (MPI 랭크 유실). 프로세스만 보면 그건 `run` 이다.
#   ⇒ **'프로세스가 있다' 와 '진전이 있다' 는 서로 다른 사실이다.** 둘 다 봐야
#     하고, 어긋나면 그 어긋남 자체를 화면에 내야 한다. 하나만 보는 감시는
#     반드시 둘 중 한 방향으로 거짓말한다.
#
# ⛔ 왜 watch_gabia.py 에 안 붙였나
#   그건 SEI **NEB 결과 판정**(끝점 대칭·Ea 인용 자격) 도구다. 여기는 판정을
#   안 하고 **생사만** 본다 — 기계도 가린다(gabia·kgy 둘 다). 성격이 다르고
#   kgy 에서 python 의존 없이 돌아야 해서 갈랐다.
#
# ⛔ 이 도구가 **못 하는 것**
#   · 물리 판정을 하지 않는다. `수렴` 은 QE 가 `bfgs converged` 를 찍었다는
#     뜻일 뿐, 그 상태가 **바닥상태인지 아닌지는 모른다**
#     (li3nd r0 실측: |F|=1.6e-5 로 "수렴" 했지만 대칭보호 정류점이었고
#      r2 가 1.19 eV 아래를 찾았다 — 이 표는 그걸 구분 못 한다).
#   · 죽은 잡을 되살리거나 다시 걸지 않는다. lock 도 건드리지 않는다.
#   · 남은 시간을 예측하지 않는다 (스텝 시간이 계마다 몇 배씩 다르다).
#   · GPU 여유가 다음 잡에 충분한지 계산하지 않는다 — 지금 누가 물고 있는지만 본다.
#
#   bash tools/sei/watch_qe_relax.sh [루트 ...]
#   watch -n 60 "bash ~/work/Yonghoon-DEM-DFT/tools/sei/watch_qe_relax.sh"
#   STALL_MIN=30 bash tools/sei/watch_qe_relax.sh /data/work/runs/sei_control
#   bash tools/sei/watch_qe_relax.sh --selftest
#
#   환경변수
#     QE_WATCH_ROOTS  기본 루트 (공백 구분). 인자를 주면 인자가 이긴다.
#     STALL_MIN       살아있는데 이만큼 .out 이 안 크면 '정체' (기본 45분)
#     QE_PROC_NAMES   생사를 볼 실행파일 이름 (기본 "pw.x neb.x ph.x")
#     DEPTH           루트 아래 몇 단계까지 훑나 (기본 3)
# =============================================================================
set -uo pipefail; set +H

STALL_MIN=${STALL_MIN:-45}
QE_PROC_NAMES=${QE_PROC_NAMES:-"pw.x neb.x ph.x"}
DEPTH=${DEPTH:-3}

# ── 살아있는 QE 프로세스의 cwd 지도 ─────────────────────────────────────────
#   근거는 **커널의 cwd** 다. lock 파일도, 출력 파일도 죽은 뒤에 남는다.
_alive_pids=""
_scan_procs() {
  local n p c
  _alive_pids=""
  for n in $QE_PROC_NAMES; do
    for p in $(pgrep -x "$n" 2>/dev/null); do
      c=$(readlink "/proc/$p/cwd" 2>/dev/null) || continue
      _alive_pids="$_alive_pids$p|$c
"
    done
  done
}
_pid_for_dir() {                       # $1=dir → "pid" 또는 빈 문자열
  printf '%s' "$_alive_pids" | awk -F'|' -v d="$1" '$2==d {print $1; exit}'
}

# ── GPU 를 실제로 물고 있는 pid ─────────────────────────────────────────────
_gpu_map=""
_scan_gpu() {
  command -v nvidia-smi >/dev/null 2>&1 || return 0
  _gpu_map=$(nvidia-smi --query-compute-apps=pid,used_memory \
             --format=csv,noheader,nounits 2>/dev/null | tr -d ' ')
}
_gpu_for_pid() { printf '%s' "$_gpu_map" | awk -F, -v p="$1" '$1==p {print $2; exit}'; }

# ── 한 출력파일을 읽는다 ────────────────────────────────────────────────────
#   상태 우선순위: 종료마커 > 생사 > 정체.
#   ⚠ `JOB DONE` 을 완주로 읽지 않는다 — nstep 을 다 써도 QE 는 JOB DONE 을 찍는다
#     (li3nd r2 실측: step=50, |F|=0.041 인데 JOB DONE). 그래서 두 마커를 가른다:
#       'bfgs converged in'                      → 진짜 수렴
#       'The maximum number of steps has been'   → nstep 소진 (미수렴)
_read_out() {
  local f="$1" now mt
  ST=""; NOTE=""; AGE="-"; STEP="-"; FRC="-"; ENE="-"
  now=$(date +%s); mt=$(stat -c %Y "$f" 2>/dev/null || echo "$now")
  AGE=$(( (now - mt) / 60 ))
  STEP=$(grep -ac "^!    total energy" "$f" 2>/dev/null); [ -n "$STEP" ] || STEP=0
  ENE=$(grep -a "^!    total energy" "$f" 2>/dev/null | tail -1 | awk '{print $5}')
  FRC=$(grep -a "Total force =" "$f" 2>/dev/null | tail -1 | awk '{print $4}')
  [ -n "$ENE" ] || ENE="-"; [ -n "$FRC" ] || FRC="-"

  if grep -aq "bfgs converged in" "$f" 2>/dev/null; then
    ST="✅ 수렴"
    NOTE="⚠ 수렴 ≠ 바닥상태 (대칭보호 정류점 가능 — li3nd r0)"
  elif grep -aq "The maximum number of steps has been" "$f" 2>/dev/null; then
    ST="⛔ nstep소진"
    NOTE="JOB DONE 이지만 **미수렴** — nstep 늘려 restart_mode='restart' 로 이어야 한다"
  elif grep -aqi "CUDA_ERROR_OUT_OF_MEMORY\|Accelerator Fatal Error" "$f" 2>/dev/null; then
    ST="☠ GPU OOM"
    NOTE="다른 잡이 GPU 를 물고 있을 때 붙으면 이렇게 죽는다 — 한 번에 하나만"
  elif grep -aq "Error in routine" "$f" 2>/dev/null; then
    ST="☠ QE 오류"
    NOTE=$(grep -a -A1 "Error in routine" "$f" 2>/dev/null | tail -1 | cut -c1-60)
  fi
}

# ── selftest ────────────────────────────────────────────────────────────────
if [ "${1:-}" = "--selftest" ]; then
  T=$(mktemp -d); ok=0; bad=0
  chk(){ if [ "$1" = "1" ]; then echo "  ⭕ $2"; ok=$((ok+1)); else echo "  ⛔ $2"; bad=$((bad+1)); fi; }
  R="$T/runs"; mkdir -p "$R"/{dead,live,stall,exhaust,conv,oom}
  _mk(){ printf '     Total force =     %s     Total SCF correction = 0.0\n!    total energy = %s Ry\n' \
           "$2" "$3" > "$1/00_control_relax.out"; }
  _mk "$R/dead"    0.012 -14652.03; _mk "$R/live" 0.012 -14652.03
  _mk "$R/stall"   0.012 -14652.03; _mk "$R/exhaust" 0.041 -14652.12
  _mk "$R/conv"    0.0001 -14652.20; _mk "$R/oom" 0.9 -14650.0
  # nstep 소진은 JOB DONE 을 **찍는다** — 이걸 완주로 읽으면 안 된다 (li3nd r2)
  printf '     The maximum number of steps has been reached.\n     JOB DONE.\n' >> "$R/exhaust/00_control_relax.out"
  printf '     bfgs converged in  120 scf cycles and 40 bfgs steps\n     JOB DONE.\n' >> "$R/conv/00_control_relax.out"
  printf 'Accelerator Fatal Error: cuMemAlloc returned error 2 (CUDA_ERROR_OUT_OF_MEMORY)\n' >> "$R/oom/00_control_relax.out"
  touch -d '300 minutes ago' "$R/stall/00_control_relax.out"
  touch -d '300 minutes ago' "$R/dead/00_control_relax.out"

  # 가짜 QE 프로세스 — cwd 가 근거이므로 그 폴더에서 띄운다
  cp /bin/sleep "$T/qefake" && chmod +x "$T/qefake"
  ( cd "$R/live"  && exec "$T/qefake" 300 ) & _p1=$!
  ( cd "$R/stall" && exec "$T/qefake" 300 ) & _p2=$!
  sleep 1
  OUT=$(QE_PROC_NAMES=qefake STALL_MIN=45 bash "$0" "$R" 2>&1)
  kill "$_p1" "$_p2" 2>/dev/null

  chk "$(echo "$OUT" | grep -E '^  live' | grep -qE 'run' && echo 1 || echo 0)" \
      "① 양성: 프로세스가 살아있고 .out 이 최근이면 run"
  chk "$(echo "$OUT" | grep -E '^  dead' | grep -q '죽음' && echo 1 || echo 0)" \
      "② ⛔음성(li3nd r1·r2 실측): **프로세스가 없으면 죽음**이다 — 파일이 있다고 run 으로 찍지 않는다"
  chk "$(echo "$OUT" | grep -E '^  stall' | grep -q '정체' && echo 1 || echo 0)" \
      "③ ⛔음성(gs2 76시간): 프로세스는 살아있어도 .out 이 문턱 넘게 조용하면 정체"
  chk "$(echo "$OUT" | grep -E '^  exhaust' | grep -q 'nstep소진' && echo 1 || echo 0)" \
      "④ ⛔음성(li3nd r2 실측): **JOB DONE 을 완주로 읽지 않는다** — nstep 소진을 가른다"
  chk "$(echo "$OUT" | grep -E '^  exhaust' | grep -q '수렴$' && echo 0 || echo 1)" \
      "④-b ⛔음성: nstep 소진을 '수렴' 으로 세지 않는다"
  chk "$(echo "$OUT" | grep -E '^  conv' | grep -q '수렴' && echo 1 || echo 0)" \
      "⑤ 양성: bfgs converged 는 수렴이다"
  chk "$(echo "$OUT" | grep -E '^  conv' | grep -q '바닥상태' && echo 1 || echo 0)" \
      "⑤-b 수렴이 바닥상태 보장이 **아니라는** 것을 같이 말한다 (li3nd r0 대칭보호)"
  chk "$(echo "$OUT" | grep -E '^  oom' | grep -q 'OOM' && echo 1 || echo 0)" \
      "⑥ ⛔음성(li3nd r2 12:08 실측): GPU OOM 사망을 그냥 '죽음' 으로 뭉뚱그리지 않는다"
  chk "$(echo "$OUT" | grep -qE '살아있음 *1|살아있음 1' && echo 1 || echo 0)" \
      "⑦ 합계에서 정체를 '살아있음' 으로 세지 않는다"

  OUT2=$(bash "$0" "$T/nonexistent" 2>&1); _rc=$?
  chk "$([ $_rc -ne 0 ] && echo 1 || echo 0)" "⑧ ⛔음성: 루트가 없으면 0 이 아닌 코드로 끝난다"
  chk "$(echo "$OUT2" | grep -qi '없' && echo 1 || echo 0)" "⑧-b ⛔음성: 없다고 말한다 (빈 표를 정상처럼 그리지 않는다)"

  rm -rf "$T"
  echo "selftest: $ok 통과 / $bad 실패"
  [ "$bad" = 0 ] || exit 1
  exit 0
fi

# ── 본체 ────────────────────────────────────────────────────────────────────
if [ "$#" -gt 0 ]; then ROOTS="$*"; else
  ROOTS=${QE_WATCH_ROOTS:-"/data/work/runs/sei_control /data/work/runs/sei_neb /data/work/runs/sei_dft"}
fi
_have=0
for r in $ROOTS; do [ -d "$r" ] && _have=$((_have+1)); done
if [ "$_have" = 0 ]; then
  echo "⛔ 루트가 하나도 없습니다: $ROOTS"
  echo "   (인자로 주거나 QE_WATCH_ROOTS 로 지정한다 — 기계마다 다르다)"
  exit 2
fi

_scan_procs; _scan_gpu

echo "════════ QE relax/NEB 생사 · $(hostname -s) · $(date '+%m-%d %H:%M:%S') ════════"
if [ -n "$_gpu_map" ]; then
  _ngpu=$(printf '%s' "$_gpu_map" | grep -c . )
  printf "  GPU 점유 프로세스 %s개" "$_ngpu"
  command -v nvidia-smi >/dev/null && \
    printf " · %s" "$(nvidia-smi --query-gpu=memory.used,memory.total,utilization.gpu --format=csv,noheader | head -1)"
  echo
  [ "${_ngpu:-0}" -gt 1 ] && \
    echo "  ⚠ GPU 를 둘 이상이 나눠 쓴다 — QE 는 이럴 때 cuMemAlloc 으로 즉사한다 (li3nd r2 실측)"
fi

printf "\n  %-34s %-14s %6s %5s %9s %-16s %s\n" 폴더 상태 조용m step "|F|" E_Ry 비고
_nlive=0; _ndead=0; _nhang=0; _nconv=0
for r in $ROOTS; do
  [ -d "$r" ] || continue
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    d=$(dirname "$f")
    _read_out "$f"
    pid=$(_pid_for_dir "$d")
    if [ -z "$ST" ]; then                       # 종료마커 없음 → 생사로 가른다
      if [ -n "$pid" ]; then
        if [ "$AGE" -ge "$STALL_MIN" ]; then
          ST="⛔ 정체"; _nhang=$((_nhang+1))
          NOTE="pid $pid 는 살아있는데 ${AGE}분째 .out 이 안 큰다 — %CPU 를 볼 것"
        else
          ST="run"; _nlive=$((_nlive+1))
        fi
      else
        ST="☠ 죽음"; _ndead=$((_ndead+1))
        NOTE="프로세스 없음 — 마지막 갱신 ${AGE}분 전. 꼬리를 보고 원인부터"
      fi
    else
      case "$ST" in
        "✅ 수렴") _nconv=$((_nconv+1)) ;;
        *) _ndead=$((_ndead+1)) ;;
      esac
    fi
    # 살아있는 잡이면 CPU·GPU 를 붙인다 (숫자가 0.0 이면 그게 죽음의 증거다)
    if [ -n "$pid" ]; then
      _cpu=$(ps -o pcpu= -p "$pid" 2>/dev/null | tr -d ' ')
      _gm=$(_gpu_for_pid "$pid")
      ST="$ST[$pid]"
      NOTE="${NOTE:+$NOTE · }CPU ${_cpu:-?}%${_gm:+ · GPU ${_gm}MiB}"
    fi
    printf "  %-34s %-14s %6s %5s %9s %-16s %s\n" \
           "$(basename "$d")" "$ST" "$AGE" "$STEP" "$FRC" "$ENE" "$NOTE"
  done <<EOF
$(find "$r" -maxdepth "$DEPTH" -name '*.out' -not -name '*_run.out' 2>/dev/null | sort)
EOF
done

printf "\n  살아있음 %d · 수렴 %d · 죽음/종료 %d" "$_nlive" "$_nconv" "$_ndead"
[ "$_nhang" -gt 0 ] && printf " · ⛔ 정체 %d" "$_nhang"
echo
[ "$_nhang" -gt 0 ] && \
  echo "  ⛔ 정체: 프로세스는 있는데 진전이 없다. ps -o pid,pcpu,etime -p <pid> 로 %CPU 를 볼 것 (gs2 76시간)"
[ "$_ndead" -gt 0 ] && \
  echo "  ☠ 죽은 잡은 **다시 걸어야** 사라진다 — 화면에서 저절로 없어지지 않는다"
exit 0

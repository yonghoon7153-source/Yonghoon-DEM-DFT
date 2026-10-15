#!/usr/bin/env bash
# =============================================================================
# run_force_check_scf.sh — 힘 대조 카드 §4 의 DFT 단일점 20점을 순서대로 돌린다.
#
#   카드: db/properties/b2o3_uma_vs_dft_force_prereg_2026_09_08.json (ratified 2판)
#   입력: generate_dft_inputs.py --from_traj 가 만든 <OUT>/<label>_<seed>_t<NN>ps/scf.in
#   다른 쓰임: O 배치 카드 6 점 (2026-09-09 · kgy) · Nd 자리 비교 Q1 (2026-10-15 · db/inputs/ndo_site_dft_2026_10_15 ·
#             기준상 vc-relax 포함 — relax · vc-relax 의 완료는 'bfgs converged' + (vc-relax) 최종 scf 에너지까지 본다)
#
# 실행 (kgy):
#   bash tools/doping/run_force_check_scf.sh $HOME/work/runs/force_check_700K
#   DRY_RUN=1 bash tools/doping/run_force_check_scf.sh <dir>     # 점검만, 계산 안 함
#   NP=8 bash tools/doping/run_force_check_scf.sh <dir>          # 랭크 수 지정
#
# ⛔ 이 스크립트가 **못 하는 것**
#   · 수렴을 보장하지 않는다 — 실패한 점을 세어 보고할 뿐이고, 실패를 **대체하지 않는다**
#     (카드 §8: 20점 중 하나라도 실패한 채 19점으로 판정하지 않는다).
#   · 힘의 물리적 타당성을 보지 않는다. pw.x 가 냈다는 사실만 확인한다.
#   · UMA 힘을 계산하지 않는다 (같은 frame.xyz 로 따로 돈다).
#   · 병렬로 여러 점을 돌리지 않는다 — CPU 빌드 16코어를 한 점에 다 준다.
#     (동시에 돌리면 코어를 나눠 갖게 되고, 총 시간은 그대로인데 개별 실패 진단만 어려워진다.)
# =============================================================================
set -u
ROOT=${1:-}

# ⛔ 완료 판정은 **한 곳에만** 둔다 — 재개(건너뛸까)와 성공(셌나)이 같은 기준이어야 한다.
#   갈라져 있던 탓에 미수렴 점이 JOB DONE 만으로 "완료" 로 건너뛰어졌다 (2026-09-08 실측).
#   ⚠ grep -a — 출력에 NUL 이 섞이면 grep 이 binary 로 보고 조용히 넘어간다.
_fc_ok() {
  [ -f "$1" ] || return 1
  grep -aq "JOB DONE" "$1" \
    && grep -aq "convergence has been achieved" "$1" \
    && grep -aq "Forces acting on atoms" "$1" || return 1
  # ⭐ 회신 BO (2026-09-12): tstress 를 켠 입력이면 **응력 블록까지** 있어야 완료다.
  #   종전엔 JOB DONE + 힘만 보고 "완료" 라 응력 대조를 통과한 것처럼 읽힐 수 있었다.
  #   tstress 가 없는 옛 입력(힘 대조 20점)은 그대로 통과시킨다 — 레거시를 깨지 않는다.
  local _in; _in="$(dirname "$1")/scf.in"
  if [ -f "$_in" ] && grep -aqiE "tstress *= *\.true\." "$_in"; then
    grep -aqE "total +stress" "$1" || return 1
  fi
  # ⭐ 2026-10-15 (Nd 자리 비교 기준상 vc-relax): relax · vc-relax 입력이면 **BFGS 수렴 선언**까지 있어야 완료다.
  #   위 세 줄 (JOB DONE · SCF 수렴 · 힘) 은 nstep 을 다 써서 끝난 relax 에도 다 찍힌다 — 그걸 완료로 읽으면
  #   미수렴 기하의 에너지가 기준상으로 들어간다 (탄성 23_p 의 '✓ 완료' 거짓 표시와 같은 부류).
  #   vc-relax 는 **최종 scf** (새 셀의 G-벡터로 다시 푼 것) 의 에너지 줄이 'End final coordinates' 뒤에 있어야 한다 —
  #   그 전에 죽으면 마지막 에너지는 옛 기저의 값이다.
  if [ -f "$_in" ] && grep -aqiE "calculation *= *'(vc-)?relax'" "$_in"; then
    # 판정은 **'bfgs converged in' 선언 하나**로 한다 (watch_elastic.sh 와 같다) — nstep 소진이면 이 줄이 안 찍힌다.
    #   (따로 'maximum number of steps' 를 보는 줄은 변이 시험에서 빨간불이 안 났다 = 이 줄이 이미 잡는다 → 뺐다)
    grep -aq "bfgs converged in" "$1" || return 1
    if grep -aqiE "calculation *= *'vc-relax'" "$_in"; then
      local _e _f
      _e=$(grep -an "End final coordinates" "$1" | tail -1 | cut -d: -f1)
      _f=$(grep -an "^!" "$1" | tail -1 | cut -d: -f1)
      [ -n "$_e" ] && [ -n "$_f" ] && [ "$_f" -gt "$_e" ] || return 1
    fi
  fi
  return 0
}

# ── --selftest : 완료 판정의 양성·음성 경로 (회신 BO 조건 1) ────────────────────
if [ "${ROOT}" = "--selftest" ]; then
  _T=$(mktemp -d); _n=0; _f=0
  _chk() { if eval "$2"; then _n=$((_n+1)); else _f=$((_f+1)); echo "  ✗ $1"; fi; }
  mkdir -p "$_T/p" "$_T/n" "$_T/l" "$_T/c" "$_T/s"
  printf "tstress = .true.\ntprnfor = .true.\n" > "$_T/p/scf.in"
  printf "convergence has been achieved\nForces acting on atoms\n     total   stress  (Ry/bohr**3)   (kbar)  P= 0.12\nJOB DONE\n" > "$_T/p/scf.out"
  _chk "tstress + 응력 → 완료"            "_fc_ok $_T/p/scf.out"
  cp "$_T/p/scf.in" "$_T/n/"; printf "convergence has been achieved\nForces acting on atoms\nJOB DONE\n" > "$_T/n/scf.out"
  _chk "tstress + 응력 없음 → **미완료**"  "! _fc_ok $_T/n/scf.out"
  printf "calculation = 'scf'\n" > "$_T/l/scf.in"; cp "$_T/n/scf.out" "$_T/l/"
  _chk "tstress 없음 → 응력 불요구(레거시)" "_fc_ok $_T/l/scf.out"
  cp "$_T/p/scf.in" "$_T/c/"; printf "JOB DONE\n     total   stress\n" > "$_T/c/scf.out"
  _chk "수렴·힘 줄 없음 → 미완료"          "! _fc_ok $_T/c/scf.out"
  printf "TSTRESS=.TRUE.\n" > "$_T/s/scf.in"; cp "$_T/n/scf.out" "$_T/s/"
  _chk "대소문자 tstress + 응력 없음 → 미완료" "! _fc_ok $_T/s/scf.out"
  _chk "scf.out 부재 → 미완료"             "! _fc_ok $_T/없음/scf.out"
  # ── 2026-10-15: relax · vc-relax 완료 판정 (기준상 vc-relax · 양성 2 · 음성 3) ──
  mkdir -p "$_T/vr" "$_T/vx" "$_T/vk" "$_T/rr" "$_T/rx"
  printf "calculation = 'vc-relax'\ntstress = .true.\n" > "$_T/vr/scf.in"
  _B="!    total energy = -1.0 Ry\nconvergence has been achieved\nForces acting on atoms\n     total   stress  (Ry/bohr**3)   (kbar)  P= 0.1\n"
  printf "${_B}bfgs converged in 12 scf cycles and 5 bfgs steps\nBegin final coordinates\nEnd final coordinates\n     A final scf calculation at the relaxed structure.\n${_B}JOB DONE\n" > "$_T/vr/scf.out"
  _chk "vc-relax 수렴 + 최종 scf → 완료"     "_fc_ok $_T/vr/scf.out"
  cp "$_T/vr/scf.in" "$_T/vx/"; printf "${_B}     The maximum number of steps has been reached.\nEnd final coordinates\n${_B}JOB DONE\n" > "$_T/vx/scf.out"
  _chk "vc-relax nstep 소진 → **미완료**"   "! _fc_ok $_T/vx/scf.out"
  cp "$_T/vr/scf.in" "$_T/vk/"; printf "${_B}bfgs converged in 12 scf cycles and 5 bfgs steps\nBegin final coordinates\nEnd final coordinates\n     A final scf calculation at the relaxed structure.\nJOB DONE\n" > "$_T/vk/scf.out"
  _chk "vc-relax 최종 scf 에너지 없음 → **미완료**" "! _fc_ok $_T/vk/scf.out"
  printf "calculation = 'relax'\ntstress = .true.\n" > "$_T/rr/scf.in"
  printf "${_B}bfgs converged in 9 scf cycles and 4 bfgs steps\nEnd final coordinates\nJOB DONE\n" > "$_T/rr/scf.out"
  _chk "relax 수렴 → 완료"                   "_fc_ok $_T/rr/scf.out"
  cp "$_T/rr/scf.in" "$_T/rx/"; printf "${_B}JOB DONE\n" > "$_T/rx/scf.out"
  _chk "relax 수렴 선언 없음 → **미완료**"    "! _fc_ok $_T/rx/scf.out"
  rm -rf "$_T"; echo "selftest: $_n 통과 · $_f 실패"; [ "$_f" = 0 ]; exit $?
fi
[ -n "$ROOT" ] || { echo "usage: $0 <스냅샷 디렉터리> [NP=16]"; exit 2; }
[ -d "$ROOT" ] || { echo "⛔ 디렉터리가 없다: $ROOT"; exit 2; }
# ⚠ 랭크 수 기본값 = **물리코어**. `nproc` 은 하이퍼스레드를 포함하는데 Open MPI 는
#   기본적으로 물리코어만 슬롯으로 세어, nproc 을 그대로 주면 "not enough slots" 로
#   **전 점이 0분 만에 즉사**한다 (2026-09-08 실측: 16 요청 → 20/20 실패).
#   QE 는 하이퍼스레드에서 거의 안 빨라지므로 물리코어가 성능 면에서도 맞다.
_phys_cores() {
  if command -v lscpu >/dev/null 2>&1; then
    local n; n=$(lscpu -p=Core,Socket 2>/dev/null | grep -v '^#' | sort -u | wc -l)
    [ "${n:-0}" -gt 0 ] && { echo "$n"; return; }
  fi
  getconf _NPROCESSORS_ONLN 2>/dev/null || echo 1
}
# ⚠ NP 기본값은 **pw.x 종류를 정한 뒤에** 잡는다 (아래) — GPU 는 1, CPU 는 물리코어.
# ⛔⛔ 2026-09-09 — 기본값이 **CPU 빌드**였다. `PWX` 를 안 넘기면 조용히 CPU 로 떨어져
#   같은 스냅샷이 GPU 1.5분/it → CPU 11분/it 가 됐고, 그걸 "느리다" 로만 읽다가
#   파일럿 비교가 통째로 어긋났다. 기본은 **GPU 빌드**고, CPU 는 **명시해야** 쓴다.
#   ⚠ 조용한 폴백은 만들지 않는다 — 없으면 시작하지 않고 뭐가 없는지 말한다.
_pick_pwx() {
  local c
  for c in "$HOME/apps/qe-7.4.1-gpu/bin/pw.x" /data/apps/qe-7.4.1-gpu/bin/pw.x \
           "$HOME/apps/qe-gpu/bin/pw.x"; do
    [ -x "$c" ] && { echo "$c"; return 0; }
  done
  return 1
}
if [ -z "${PWX:-}" ]; then
  PWX=$(_pick_pwx) || {
    echo "⛔ GPU 빌드 pw.x 를 못 찾았다 — **시작하지 않는다**."
    echo "   찾아본 곳: \$HOME/apps/qe-7.4.1-gpu/bin/pw.x · /data/apps/qe-7.4.1-gpu/bin/pw.x"
    echo "   · GPU 로 돌리려면:  PWX=<경로> $0 $ROOT"
    echo "   · CPU 로 돌릴 거면 **일부러** 그렇게 적어라(느리다):"
    echo "       ALLOW_CPU=1 PWX=\$HOME/apps/qe-7.4.1-cpu/bin/pw.x NP=8 OMP_NUM_THREADS=2 $0 $ROOT"
    exit 2; }
fi
# CPU 빌드는 **의도 선언 없이는 못 쓴다** — 조용히 12배 느려지는 것을 막는다.
if [[ "$PWX" != *gpu* ]] && [ "${ALLOW_CPU:-0}" != 1 ]; then
  echo "⛔ CPU 빌드다 (pw.x=$PWX). 의도한 것이면 ALLOW_CPU=1 을 붙여라 — 시작하지 않는다."
  echo "   ⚠ CPU 로 돌리면 스레드도 같이 정해라: NP=<물리코어> OMP_NUM_THREADS=<논리/NP>"
  echo "     (안 정하면 랭크마다 OMP 가 전 코어를 잡아 8×16=128 스레드가 16코어에 올라간다"
  echo "      — 2026-09-09 실측, 11분/iteration)"
  exit 2
fi
# CPU 경로의 스레드 고정 (GPU 경로는 아래 ldd 블록이 1 로 박는다).
if [[ "$PWX" != *gpu* ]] && [ -z "${OMP_NUM_THREADS:-}" ]; then
  _lg=$(getconf _NPROCESSORS_ONLN 2>/dev/null || echo 1)
  export OMP_NUM_THREADS=$(( _lg / NP > 0 ? _lg / NP : 1 ))
  echo "[$(date '+%m-%d %H:%M:%S')] ⚠ OMP_NUM_THREADS 미지정 → ${OMP_NUM_THREADS} 로 고정 (논리 ${_lg} / 랭크 ${NP})"
fi
# ⛔⛔ 2026-09-09 실측 — GPU 빌드인데 NP 기본값이 물리코어(8)라 GPU 하나에 8랭크가
#   붙어 **19초 만에 즉사**했다(Exit code 1). 어제 성공한 런은 `랭크 1` 이었다.
#   GPU 빌드는 **GPU 하나당 랭크 하나**가 이 repo 의 검증된 관례다(아래 -nk 1 과 같은 줄).
if [[ "$PWX" == *gpu* ]]; then
  if [ -z "${NP:-}" ]; then
    NP=1
    echo "[$(date '+%m-%d %H:%M:%S')] GPU 빌드 → 랭크 1 (GPU 하나당 랭크 하나)"
  elif [ "$NP" != 1 ]; then
    echo "⛔ GPU 빌드인데 NP=$NP 다. GPU 하나에 여러 랭크를 붙이면 즉사한다"
    echo "   (2026-09-09 실측: np 8 → 19초 만에 Exit code 1)."
    echo "   여러 GPU 를 쓸 거면 FORCE_MULTIRANK=1 을 붙여라 — 그게 아니면 NP=1."
    [ "${FORCE_MULTIRANK:-0}" = 1 ] || exit 2
  fi
fi
NP=${NP:-$(_phys_cores)}
DRY_RUN=${DRY_RUN:-0}

ts() { date '+%m-%d %H:%M:%S'; }



# ── 중복 실행 가드 (CLAUDE.md 공통 관례 · pgrep 이 아니라 flock) ──────────────
#   pgrep 로 세면 래퍼(sh -c … | tee)까지 세어 시작하자마자 죽는 사고가 있었다.
LOCK=${LOCK:-/tmp/force_check_scf.lock}
exec 9>"$LOCK" || { echo "⛔ 락 파일을 못 연다: $LOCK"; exit 1; }
if command -v flock >/dev/null 2>&1; then
  flock -n 9 || { echo "[$(ts)] 이미 도는 인스턴스가 있다 (flock $LOCK) — 중단"; exit 0; }
fi

# ── 사전점검: 있어야 하는 것이 다 있나 (없으면 **시작하지 않는다**) ──────────
[ -x "$PWX" ] || { echo "⛔ pw.x 를 못 찾는다: $PWX  (PWX=... 로 지정)"; exit 2; }
# ── NVHPC(QE-GPU) 런타임 정렬 ────────────────────────────────────────────────
# ⛔⛔ 2026-09-08 실측, **같은 자리에서 두 번 죽었다.** 둘 다 "런타임이 빌드와 다르다" 다.
#   ① 다른 mpirun(conda)이 잡힘 → `MPI_Init_thread ... NULL communicator` (3시간 시체)
#   ② mpirun 을 빼니 → `libgomp: TODO` (NVHPC 로 빌드된 바이너리가 GNU OpenMP 를 잡았다)
#   ★ 정답은 **런처를 빼는 것이 아니라 NVHPC 스택을 통째로 맞추는 것**이고, 그 처방은
#     이미 repo 에 있었다 — tools/ionic/watch_all.py · tools/neb_diffusion/li3n_uma_investigate.py.
#     `compilers/lib` 가 NVIDIA OpenMP 런타임을 주는 자리다. 그게 빠지면 libgomp 가 이긴다.
#   여기서 자동으로 찾아 건다. 못 찾으면 **시작하지 않는다** (조용히 GNU 런타임으로 돌지 않게).
# ★ 경로를 **추측하지 않는다 — `ldd` 로 바이너리에게 묻는다.**
#   추측은 세 번 틀렸다: ① conda mpirun 탓으로 봤고 ② 런처를 뺐다가 libgomp 를 만났고
#   ③ hpcx 를 자동탐지했는데 kgy 의 pw.x 는 hpcx 가 아니라 ~/apps/openmpi-4.1.6 로
#   빌드돼 있었다(hpcx 에서 오는 건 scalapack 뿐). 머신마다 다르니 규칙이 아니라
#   **바이너리의 실제 링크**가 유일한 근거다.
_setup_mpi_from_binary() {
  command -v ldd >/dev/null 2>&1 || return 1
  local out; out=$(ldd "$PWX" 2>/dev/null) || return 1
  # 실제로 링크된 libmpi.so 의 디렉터리 → 그 부모가 MPI prefix
  local libmpi; libmpi=$(echo "$out" | awk '/libmpi\.so/ {print $3; exit}')
  [ -n "$libmpi" ] && [ -f "$libmpi" ] || return 1
  local mdir mprefix; mdir=$(dirname "$libmpi"); mprefix=$(dirname "$mdir")
  # 링크된 다른 라이브러리들의 디렉터리도 전부 넣는다 (NVHPC compilers/lib 등)
  local extra; extra=$(echo "$out" | awk '$3 ~ /^\// {print $3}' | xargs -r -n1 dirname \
                       | sort -u | tr '\n' ':' | sed 's/:$//')
  export OPAL_PREFIX="$mprefix"
  export PATH="$mprefix/bin:$PATH"
  export LD_LIBRARY_PATH="$mdir:$extra:${LD_LIBRARY_PATH:-}"
  echo "[$(ts)] MPI 를 바이너리에서 읽었다: $libmpi"
  echo "[$(ts)]   prefix=$mprefix · mpirun=$mprefix/bin/mpirun"
  # ⚠ libnvomp 와 libgomp 가 **둘 다** 링크돼 있으면 OpenMP 런타임이 둘이다
  #   (kgy 실측: libfftw3_omp 가 GNU 쪽을 끌고 온다) → `libgomp: TODO` 로 즉사한다.
  #   스레드를 1로 두면 병렬 진입 자체가 없어 충돌 경로를 안 탄다.
  if echo "$out" | grep -q "libnvomp" && echo "$out" | grep -q "libgomp"; then
    export OMP_NUM_THREADS=1
    echo "[$(ts)]   ⚠ libnvomp + libgomp 동시 링크 — OMP_NUM_THREADS=1 로 고정(libgomp: TODO 회피)"
  fi
  [ -x "$mprefix/bin/mpirun" ] && { BIN_MPIRUN="$mprefix/bin/mpirun"; return 0; }
  BIN_MPIRUN=""; return 0
}
BIN_MPIRUN=""
MPI=""
if [[ "$PWX" == *gpu* ]] || [ "${FORCE_NVHPC:-0}" = 1 ]; then
  if ! _setup_mpi_from_binary; then
    echo "⛔ GPU 빌드(pw.x=$PWX)인데 링크된 MPI 를 못 읽었다 — 시작하지 않는다."
    echo '   ldd <pw.x> | grep libmpi 를 직접 확인해라. 런타임을 안 맞추면'
    echo "   MPI_Init 또는 libgomp 에서 죽는다 (2026-09-08 실측 2회)."
    exit 2
  fi
  [ -n "$BIN_MPIRUN" ] || { echo "⛔ $OPAL_PREFIX/bin/mpirun 이 없다 — 시작하지 않는다"; exit 2; }
  # GPU 빌드는 GPU 하나당 랭크 하나. -nk 1 도 repo 의 검증된 관례다.
  MPI="$BIN_MPIRUN --oversubscribe -np $NP"
  PW_EXTRA=${PW_EXTRA:-"-nk 1"}
elif command -v mpirun >/dev/null 2>&1; then
  _OS=""; mpirun --version 2>&1 | grep -qi "open mpi" && _OS="--oversubscribe"
  MPI="mpirun $_OS -np $NP"
  echo "[$(ts)] mpirun 경로: $(command -v mpirun)"
elif command -v mpiexec >/dev/null 2>&1; then MPI="mpiexec -n $NP"
else echo "[$(ts)] ⚠ mpirun/mpiexec 없음 — 직렬로 돈다 (느리다)"; NP=1; fi
PW_EXTRA=${PW_EXTRA:-}
echo "[$(ts)] 코어: 물리 $(_phys_cores) · 논리 $(getconf _NPROCESSORS_ONLN 2>/dev/null) → 랭크 $NP"

mapfile -t INS < <(find "$ROOT" -mindepth 2 -maxdepth 2 -name scf.in | sort)
[ "${#INS[@]}" -gt 0 ] || { echo "⛔ scf.in 이 없다: $ROOT/*/scf.in"; exit 2; }

# 유사포텐셜이 실제로 있나 — scf.in 이 가리키는 경로를 그대로 확인한다
PSD=$(grep -a -m1 "pseudo_dir" "${INS[0]}" | sed "s/.*=\s*'\([^']*\)'.*/\1/")
MISS=0
# ⚠ ATOMIC_SPECIES 블록은 **다음 카드 키워드까지**만 읽는다. -A20 으로 훑으면
#   CELL_PARAMETERS 의 좌표 3열까지 유사포텐셜 이름으로 읽는다 (자체시험에서 잡힌 사고).
for f in $(awk 'FNR==1{c=0}
                /^ATOMIC_SPECIES/{c=1; next}
                /^(CELL_PARAMETERS|ATOMIC_POSITIONS|K_POINTS|OCCUPATIONS|CONSTRAINTS|ATOMIC_VELOCITIES|ATOMIC_FORCES)/{c=0}
                c && NF==3 {print $3}' "${INS[@]}" | sort -u); do
  [ -f "$PSD/$f" ] || { echo "⛔ 유사포텐셜 없음: $PSD/$f"; MISS=1; }
done
[ "$MISS" = 0 ] || { echo "⛔ 유사포텐셜이 빠졌다 — 시작하지 않는다"; exit 2; }

# ── 설정 균일성 검사 (2026-09-08) ────────────────────────────────────────────
# ⛔ 점마다 SCF 설정이 다르면 이 캠페인은 **계 간 비교가 아니라 설정 간 비교**가 된다.
#   실측 사고: 20점을 새 믹싱으로 재생성하려다 생성이 조용히 실패했고(ase 없음),
#   옛 입력 그대로 러너가 다시 돌았다. 일부만 재생성됐다면 더 나쁘다 — 섞인 채
#   끝까지 돌고 판정 단계에서야 드러난다. 그러니 **시작 전에** 대조한다.
#   ⛔ 2026-09-08 — 초판이 &SYSTEM 전체를 비교해 **b2o3(128원자·B 포함)와 modelc(62원자)를
#     설정 차이로 읽고 정상 실행을 막았다.** 계 크기·조성은 당연히 다르다. 균일해야 하는 것은
#     **방법 노브**뿐이다 → 블랙리스트가 아니라 **화이트리스트**로 센다.
#     제외(설계상): nat·ntyp·prefix·좌표 · tot_magnetization·starting_magnetization
#     (조성에서 유도되는 값이라 셀마다 달라야 정상이다).
_UNIFORM_KEYS='ecutwfc|ecutrho|occupations|smearing|degauss|nosym|conv_thr|mixing_mode|mixing_beta|electron_maxstep|diagonalization|nspin'
_settings_key() {
  grep -aE "^ *($_UNIFORM_KEYS) *=" "$1" | tr -d ' \t' | sort | md5sum | cut -d' ' -f1
}
_k0=""; _bad=0
for i in "${INS[@]}"; do
  _k=$(_settings_key "$i")
  if [ -z "$_k0" ]; then _k0="$_k"; _ref="$i"
  elif [ "$_k" != "$_k0" ]; then
    echo "⛔ SCF 설정이 점마다 다르다: $(basename "$(dirname "$i")") ≠ $(basename "$(dirname "$_ref")")"
    _bad=1
  fi
done
[ "$_bad" = 0 ] || { echo "⛔ 섞인 설정으로는 시작하지 않는다 — 전 점을 같은 인자로 재생성해라."
                     echo "   (diff 로 확인: diff <(sed -n '/&SYSTEM/,/^\\//p' A/scf.in) <(… B/scf.in))"; exit 2; }
echo "[$(ts)] 설정 균일성 ✓ (${#INS[@]}점 동일 · key ${_k0:0:8})"
grep -a "mixing_mode\|electron_maxstep\|occupations" "${INS[0]}" | sed 's/^/           /'

echo "[$(ts)] 점 ${#INS[@]}개 · $MPI · pw.x=$PWX · pseudo=$PSD"
if [ "$DRY_RUN" = 1 ]; then
  for i in "${INS[@]}"; do
    d=$(dirname "$i")
    # ⛔ 여기도 _fc_ok 를 쓴다. 이 스크립트가 스스로 적어둔 규칙 —
    #   "완료 판정은 **한 곳에만** 둔다. 재개(건너뛸까)와 성공(셌나)이 같은 기준이어야
    #   한다" — 을 DRY_RUN 화면만 어기고 있었다 (맨 grep "JOB DONE").
    #   2026-09-10 실측: 미수렴 9점을 "완료(건너뜀)" 으로 찍어 **사람에게만 거짓말**했다.
    #   실행 루프는 제대로 다시 돌렸을 텐데, 화면을 믿고 안 던졌으면 영영 안 고쳐진다.
    st="대기"
    _fc_ok "$d/scf.out" && st="완료(건너뜀)"
    printf "  %-28s %s\n" "$(basename "$d")" "$st"
  done
  echo "[$(ts)] DRY_RUN — 계산은 하지 않았다"; exit 0
fi

# ⚠ 이번 실행의 시작 시각을 남긴다 — watch 가 **옛 실패**(이전 배치가 남긴 scf.out)와
#   이번 실행의 실패를 가르는 기준이다. 없으면 아직 차례가 안 온 점의 옛 출력이
#   "지금 실패한 것" 처럼 읽힌다 (2026-09-08 실측: 진행 1 인데 문제 19 로 표시).
touch "$ROOT/.fc_run_started"
done_n=0; skip_n=0; fail_n=0; t0=$(date +%s)
for i in "${INS[@]}"; do
  d=$(dirname "$i"); n=$(basename "$d")
  # 재개: 이미 끝난 점은 다시 돌지 않는다.
  # ⛔ 2026-09-08 실측 — 여기가 `JOB DONE` **만** 봤다. 그런데 아래 성공 판정은
  #   JOB DONE + 수렴 + 힘 셋을 본다. 그래서 SCF 가 100회에서 잘려 힘 블록이 없는 점이
  #   JOB DONE 을 달고 남았고, 다시 돌리면 그 점을 **"완료" 로 건너뛰어 영영 안 고쳐진다.**
  #   재개 조건과 성공 조건은 **같은 기준**이어야 한다.
  if _fc_ok "$d/scf.out"; then
    echo "[$(ts)] skip $n (완료: JOB DONE + 수렴 + 힘)"; skip_n=$((skip_n+1)); continue
  fi
  # ── VRAM 양보 가드 (2026-09-08) ────────────────────────────────────────────
  # ⛔ GPU 를 남과 나눠 쓸 때 QE 는 cuMemAlloc 으로 즉사한다 (li3nd r2 실측, 두 번).
  #   위험한 건 **내가 죽는 것이 아니라 남을 죽이는 것**이다 — 먼저 돌던 잡이 BFGS
  #   스텝에서 메모리를 더 잡으려 할 때 내가 자리를 먹고 있으면 그쪽이 죽는다.
  #   그래서 점을 시작하기 **전에** 여유를 보고, 바닥이면 **이 잡이 물러난다**.
  #   MIN_FREE_MIB=0 으로 끌 수 있다 (독점 실행일 때).
  if [ "${MIN_FREE_MIB:-0}" -gt 0 ] && command -v nvidia-smi >/dev/null 2>&1; then
    free_mib=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits 2>/dev/null | head -1)
    if [ -n "$free_mib" ] && [ "$free_mib" -lt "$MIN_FREE_MIB" ]; then
      echo "[$(ts)] ⛔ VRAM 여유 ${free_mib} MiB < MIN_FREE_MIB=${MIN_FREE_MIB} — **이 잡이 물러난다**."
      echo "   남의 잡을 죽이지 않으려고 시작하지 않는다. 남은 점은 던지지 않았다."
      echo "   먼저 돌던 계산이 끝난 뒤 같은 명령으로 이어 돌리면 끝난 점은 건너뛴다."
      break
    fi
    echo "[$(ts)]   VRAM 여유 ${free_mib} MiB (문턱 ${MIN_FREE_MIB})"
  fi
  s=$(date +%s)
  ( cd "$d" && $MPI "$PWX" $PW_EXTRA -in scf.in > scf.out 2>&1 )
  e=$(date +%s)
  # ⚠ grep -a — 출력에 NUL 이 섞이면 grep 이 binary 로 보고 조용히 넘어간다
  if _fc_ok "$d/scf.out"; then
    echo "[$(ts)] ✓ $n  $(( (e-s)/60 ))분"; done_n=$((done_n+1))
  else
    echo "[$(ts)] ⛔ $n  실패 — $d/scf.out 마지막 줄:"
    tail -3 "$d/scf.out" | sed 's/^/       /'
    fail_n=$((fail_n+1))
    # ⚠ 첫 점이 **1분 안에** 죽으면 환경 문제다 (MPI 슬롯·유사포텐셜·바이너리).
    #   같은 실패를 20번 반복해 로그만 채우지 않는다 — 실측 2026-09-08 (20/20 즉사).
    if [ "$done_n" = 0 ] && [ $((e-s)) -lt 60 ]; then
      echo "[$(ts)] ⛔ 첫 점이 $((e-s))초 만에 죽었다 — 환경 문제로 보고 **중단**한다."
      echo "   나머지 $(( ${#INS[@]} - fail_n )) 점은 던지지 않았다. 위 메시지를 먼저 고쳐라."
      break
    fi
  fi
done

echo "[$(ts)] 끝 — 완료 $done_n · 건너뜀 $skip_n · 실패 $fail_n · 총 $(( ($(date +%s)-t0)/60 ))분"
if [ "$fail_n" -gt 0 ]; then
  echo "⛔ 실패한 점이 있다. 카드 §8 무효 조건: **19점으로 판정하지 않는다** —"
  echo "   그 점을 다시 돌리거나, 규칙에 미리 적은 대체(실패 프레임의 +1 ps)를 쓴다."
  exit 1
fi
echo "다음: UMA 힘 (같은 frame.xyz) → 분석"

#!/usr/bin/env bash
# =============================================================================
# qe_gpu_runtime.sh — QE-GPU 런타임을 **바이너리에게 물어서** 맞춘다.
#
#   source tools/lib/qe_gpu_runtime.sh
#   qe_gpu_require "$PWX"          # 못 읽으면 exit 2 (시작하지 않는다)
#   "$QE_GPU_MPIRUN" --oversubscribe -np 1 "$PWX" -nk 1 -in x.in
#
# ⛔⛔ 왜 이 파일이 있나 — 같은 자리에서 **세 번** 죽었다 (2026-09-08, CLAUDE.md 계산 자원):
#   ① conda 의 mpirun 이 잡혀 `MPI_Init_thread … NULL communicator` (3시간 시체)
#   ② 런처를 뺐더니 `libgomp: TODO` (NVHPC 로 빌드된 바이너리가 GNU OpenMP 를 잡았다)
#   ③ hpcx 를 자동탐지했는데 kgy 의 pw.x 는 hpcx 가 아니라 **~/apps/openmpi-4.1.6** 로
#      빌드돼 있었다 (hpcx 에서 오는 건 scalapack 뿐).
#   ★ 결론은 "어느 MPI 가 맞나" 가 아니다. **머신마다 다르므로 규칙이 아니라 링크가
#     근거다** — `ldd` 로 바이너리에게 묻고, 못 읽으면 **시작하지 않는다.**
#   원본 구현: tools/doping/run_force_check_scf.sh 의 `_setup_mpi_from_binary()`.
#   여기로 뽑은 이유: 같은 처방이 필요한 러너가 여럿인데 각자 다르게 추측하고 있었다
#   (tools/electronic/run_comp2_saddle_check_kgy.sh 가 ③ 을 그대로 하고 있었다).
#
# ⛔ 이 파일이 **못 하는 것**
#   · 어느 pw.x 를 쓸지 고르지 않는다 — 경로는 부르는 쪽이 준다.
#   · GPU 가 비어 있는지 안 본다 (`nvidia-smi` 대기·pw.x/UMA 동시금지는 러너의 몫).
#   · 랭크 수·`-nk` 를 정하지 않는다. GPU 빌드의 관례(-np 1 · -nk 1)는 러너에 남긴다.
#   · MPI 가 **실제로 도는지**는 모른다. 링크를 읽어 환경을 맞출 뿐이라, 드라이버·
#     CUDA 버전 불일치 같은 실행시 실패는 여전히 러너에서 난다.
#   · 정적 링크(ldd 가 "not a dynamic executable")면 유도할 것이 없어 **거부**한다 —
#     그 경우 사람이 판단해야 한다.
#   · KISTI(Slurm/srun) 에는 쓰지 않는다. 거기는 srun 이 런타임을 정한다.
# =============================================================================

# qe_gpu_setup <pw.x>
#   성공: 0 · QE_GPU_MPIRUN / OPAL_PREFIX / PATH / LD_LIBRARY_PATH (+필요시
#         OMP_NUM_THREADS=1) 를 export 하고 무엇을 왜 정했는지 찍는다.
#   실패: 비-0 (아무것도 export 하지 않는다). 판단은 부르는 쪽 — 보통 qe_gpu_require.
qe_gpu_setup() {
  local pwx="${1:-}"
  QE_GPU_MPIRUN=""
  [ -n "$pwx" ] || { echo "⛔ qe_gpu_setup: pw.x 경로가 비었다"; return 1; }
  [ -x "$pwx" ] || { echo "⛔ qe_gpu_setup: 실행 가능한 pw.x 가 아니다: $pwx"; return 1; }
  command -v ldd >/dev/null 2>&1 || { echo "⛔ ldd 가 없다 — 링크를 못 읽는다"; return 1; }

  local out
  out=$(ldd "$pwx" 2>/dev/null) || { echo "⛔ ldd 실패: $pwx"; return 1; }
  case "$out" in
    *"not a dynamic executable"*)
      echo "⛔ 정적 링크다 — 유도할 런타임이 없다: $pwx"; return 1;;
  esac

  # 실제로 링크된 libmpi.so 의 디렉터리 → 그 부모가 MPI prefix
  local libmpi; libmpi=$(echo "$out" | awk '/libmpi\.so/ {print $3; exit}')
  [ -n "$libmpi" ] || { echo "⛔ 링크된 libmpi 가 없다 — 시작하지 않는다"; return 1; }
  [ -f "$libmpi" ] || { echo "⛔ 링크된 MPI 를 못 읽었다 ($libmpi) — 시작하지 않는다"; return 1; }

  local mdir mprefix; mdir=$(dirname "$libmpi"); mprefix=$(dirname "$mdir")
  # 링크된 다른 라이브러리들의 디렉터리도 전부 넣는다 (NVHPC compilers/lib 등 —
  # 그게 빠지면 ② 의 libgomp 가 이긴다)
  local extra; extra=$(echo "$out" | awk '$3 ~ /^\// {print $3}' | xargs -r -n1 dirname \
                       | sort -u | tr '\n' ':' | sed 's/:$//')
  export OPAL_PREFIX="$mprefix"
  export PATH="$mprefix/bin:$PATH"
  # ⚠ 빈 항목(연속 ':' 또는 끝의 ':')은 '현재 디렉터리' 를 뜻해 엉뚱한 .so 를 잡는다.
  local ld="$mdir:$extra${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
  export LD_LIBRARY_PATH="$(echo "$ld" | sed -e 's/::*/:/g' -e 's/^://' -e 's/:$//')"
  echo "[qe_gpu] MPI 를 바이너리에서 읽었다: $libmpi"
  echo "[qe_gpu]   prefix=$mprefix · mpirun=$mprefix/bin/mpirun"

  # ⚠ libnvomp 와 libgomp 가 **둘 다** 링크돼 있으면 OpenMP 런타임이 둘이다
  #   (kgy 실측: libfftw3_omp 가 GNU 쪽을 끌고 온다) → `libgomp: TODO` 로 즉사한다.
  #   스레드를 1로 두면 병렬 진입 자체가 없어 충돌 경로를 안 탄다.
  if echo "$out" | grep -q "libnvomp" && echo "$out" | grep -q "libgomp"; then
    export OMP_NUM_THREADS=1
    echo "[qe_gpu]   ⚠ libnvomp + libgomp 동시 링크 — OMP_NUM_THREADS=1 (libgomp: TODO 회피)"
  fi

  [ -x "$mprefix/bin/mpirun" ] || {
    echo "⛔ $mprefix/bin/mpirun 이 없다 — 시작하지 않는다"; return 1; }
  QE_GPU_MPIRUN="$mprefix/bin/mpirun"
  export QE_GPU_MPIRUN
  return 0
}

# qe_gpu_require <pw.x> — 실패하면 **시작하지 않는다** (exit 2).
#   "추측해서 계속 간다" 는 갈래를 일부러 안 만든다. 세 번의 사고가 전부 그 갈래였다.
qe_gpu_require() {
  qe_gpu_setup "$1" && return 0
  echo "⛔ QE-GPU 런타임을 링크에서 유도하지 못했다 — 시작하지 않는다."
  echo "   확인:  ldd '$1' | grep -E 'libmpi|libnvomp|libgomp'"
  echo "   런타임을 안 맞추면 MPI_Init 또는 libgomp 에서 죽는다 (2026-09-08 실측 3회)."
  exit 2
}

# ── selftest (직접 실행할 때만) ────────────────────────────────────────────
#   ⚠ 실제 pw.x 없이 시험한다: 가짜 `ldd` 를 PATH 앞에 놓아 링크 목록을 흉내낸다.
#     그래서 **환경변수 우회 스위치를 만들지 않는다** — 생산 코드에 시험용 구멍을
#     내면 그 구멍으로 추측이 다시 들어온다.
_qe_gpu_selftest() {
  local tmp ok=0 fails=0
  tmp=$(mktemp -d) || return 1
  # shellcheck disable=SC2317
  _say() { if [ "$1" = 0 ]; then echo "  ✓ $2"; ok=$((ok+1));
           else echo "  ✗ $2"; fails=$((fails+1)); fi; }

  mkdir -p "$tmp/bin" "$tmp/mpi/lib" "$tmp/mpi/bin" "$tmp/nvhpc/lib"
  : > "$tmp/mpi/lib/libmpi.so.40"; : > "$tmp/nvhpc/lib/libnvomp.so"
  printf '#!/bin/sh\nexit 0\n' > "$tmp/mpi/bin/mpirun"; chmod +x "$tmp/mpi/bin/mpirun"
  printf '#!/bin/sh\nexit 0\n' > "$tmp/bin/pw.x";       chmod +x "$tmp/bin/pw.x"

  _fake_ldd() {   # $1 = 흉내낼 출력
    printf '#!/bin/sh\ncat <<"EOF"\n%s\nEOF\n' "$1" > "$tmp/bin/ldd"
    chmod +x "$tmp/bin/ldd"
  }
  _run() {  # 깨끗한 환경에서 setup 한 번 — 시험끼리 오염되지 않게 서브셸로
    ( PATH="$tmp/bin:$PATH"; unset OPAL_PREFIX QE_GPU_MPIRUN OMP_NUM_THREADS
      unset LD_LIBRARY_PATH
      qe_gpu_setup "$tmp/bin/pw.x" >"$tmp/out" 2>&1
      echo "rc=$?"; echo "OPAL_PREFIX=$OPAL_PREFIX"; echo "OMP=${OMP_NUM_THREADS:-unset}"
      echo "MPIRUN=$QE_GPU_MPIRUN"; echo "LD=$LD_LIBRARY_PATH" )
  }

  # ⓐ 양성 — libmpi 가 실재하면 prefix 를 그 부모로 잡는다
  _fake_ldd "	libmpi.so.40 => $tmp/mpi/lib/libmpi.so.40 (0x1)
	libnvomp.so => $tmp/nvhpc/lib/libnvomp.so (0x2)"
  local r; r=$(_run)
  case "$r" in *"rc=0"*) _say 0 "ⓐ 링크된 MPI 로 prefix 를 유도한다";;
                      *) _say 1 "ⓐ 유도 실패 ($r)";; esac
  case "$r" in *"OPAL_PREFIX=$tmp/mpi"*) _say 0 "ⓐ prefix = libmpi 디렉터리의 부모";;
                      *) _say 1 "ⓐ prefix 가 틀렸다 ($r)";; esac
  case "$r" in *"MPIRUN=$tmp/mpi/bin/mpirun"*) _say 0 "ⓐ 그 prefix 의 mpirun 을 쓴다";;
                      *) _say 1 "ⓐ mpirun 이 틀렸다";; esac
  case "$r" in *"OMP=unset"*) _say 0 "ⓐ⛔음성: libgomp 가 없으면 OMP 를 강제하지 않는다";;
                      *) _say 1 "ⓐ libgomp 없이도 OMP 를 건드린다 (조건이 죽었다)";; esac
  # 빈 항목(맨앞 ':' · 연속 '::' · 끝의 ':')은 '현재 디렉터리' 를 뜻해 엉뚱한 .so 를 잡는다
  local ldv; ldv=$(printf '%s\n' "$r" | sed -n 's/^LD=//p')
  case ":$ldv:" in *"::"*) _say 1 "ⓐ LD_LIBRARY_PATH 에 빈 항목이 있다 ($ldv)";;
                        *) _say 0 "ⓐ LD_LIBRARY_PATH 에 빈 항목이 없다";; esac
  # ⛔음성: 그 검사가 실제로 작동하는지 — 빈 항목이 있는 문자열은 반드시 걸려야 한다
  case ":$tmp/a::$tmp/b:" in *"::"*) _say 0 "ⓐ⛔음성: 빈 항목 검출기 자체가 산다";;
                                  *) _say 1 "ⓐ 빈 항목을 못 잡는다 (검사가 죽어 있다)";; esac

  # ⓑ ⛔음성 — libnvomp + libgomp 동시 링크면 OMP_NUM_THREADS=1 (`libgomp: TODO` 방지)
  : > "$tmp/nvhpc/lib/libgomp.so.1"
  _fake_ldd "	libmpi.so.40 => $tmp/mpi/lib/libmpi.so.40 (0x1)
	libnvomp.so => $tmp/nvhpc/lib/libnvomp.so (0x2)
	libgomp.so.1 => $tmp/nvhpc/lib/libgomp.so.1 (0x3)"
  r=$(_run)
  case "$r" in *"OMP=1"*) _say 0 "ⓑ⛔음성: libnvomp+libgomp 동시 링크 → OMP_NUM_THREADS=1";;
                      *) _say 1 "ⓑ 동시 링크인데 OMP 를 안 잠갔다 — libgomp: TODO 로 죽는다";; esac

  # ⓒ ⛔음성 — libmpi 자체가 없으면 **거부**한다 (추측해서 진행하지 않는다)
  _fake_ldd "	libc.so.6 => /lib/libc.so.6 (0x1)"
  r=$(_run)
  case "$r" in *"rc=0"*) _say 1 "ⓒ libmpi 가 없는데 통과시켰다 (③ 오진이 여기서 났다)";;
                      *) _say 0 "ⓒ⛔음성: libmpi 가 없으면 거부한다";; esac

  # ⓓ ⛔음성 — ldd 는 경로를 주는데 그 파일이 실재하지 않으면 거부
  _fake_ldd "	libmpi.so.40 => $tmp/nope/libmpi.so.40 (0x1)"
  r=$(_run)
  case "$r" in *"rc=0"*) _say 1 "ⓓ 없는 libmpi 경로를 통과시켰다";;
                      *) _say 0 "ⓓ⛔음성: 링크 경로가 실재하지 않으면 거부한다";; esac

  # ⓔ ⛔음성 — prefix 는 맞는데 그 안에 mpirun 이 없으면 거부
  mv "$tmp/mpi/bin/mpirun" "$tmp/mpi/bin/mpirun.off"
  _fake_ldd "	libmpi.so.40 => $tmp/mpi/lib/libmpi.so.40 (0x1)"
  r=$(_run)
  case "$r" in *"rc=0"*) _say 1 "ⓔ mpirun 이 없는데 통과시켰다";;
                      *) _say 0 "ⓔ⛔음성: prefix 에 mpirun 이 없으면 거부한다";; esac
  mv "$tmp/mpi/bin/mpirun.off" "$tmp/mpi/bin/mpirun"

  # ⓕ ⛔음성 — 정적 링크는 유도할 것이 없다
  _fake_ldd "	not a dynamic executable"
  r=$(_run)
  case "$r" in *"rc=0"*) _say 1 "ⓕ 정적 링크를 통과시켰다";;
                      *) _say 0 "ⓕ⛔음성: 정적 링크는 거부한다";; esac

  # ⓖ ⛔음성 — pw.x 가 실행 가능하지 않으면 시작 전에 막는다
  ( PATH="$tmp/bin:$PATH"; qe_gpu_setup "$tmp/bin/nope.x" >/dev/null 2>&1 ) \
    && _say 1 "ⓖ 없는 pw.x 를 통과시켰다" || _say 0 "ⓖ⛔음성: 없는 pw.x 는 거부한다"
  ( PATH="$tmp/bin:$PATH"; qe_gpu_setup "" >/dev/null 2>&1 ) \
    && _say 1 "ⓖ 빈 경로를 통과시켰다" || _say 0 "ⓖ⛔음성: 빈 경로는 거부한다"

  rm -rf "$tmp"
  echo "qe_gpu_runtime selftest: PASS $ok · FAIL $fails"
  [ "$fails" -eq 0 ]
}

case "${1:-}" in
  --selftest) _qe_gpu_selftest; exit $? ;;
esac

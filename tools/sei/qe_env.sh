# QE 실행 환경 — **source 해서 쓴다.** 이 파일이 정본이다.
#
# ⛔ 왜 파일로 뽑았나 (2026-08-28)
#   `run_prereq_chain.sh` 를 새로 쓰면서 `MPIRUN`·`PW` 경로만 챙기고 **환경변수를 통째로
#   빠뜨렸다.** 결과: `libgomp: TODO` 로 pw.x 가 즉사했고, 밤새 돌 예정이던 체인이
#   첫 점에서 끝났다. 기존 `run_sei_neb.sh` 는 같은 블록을 제대로 갖고 있었다 —
#   **복사했어야 할 것을 새로 쓴 것이 아니라, 아예 안 쓴 것**이 문제였다.
#   ⇒ 두 스크립트가 같은 파일을 source 한다. 갈라질 수가 없다.
#
# ⛔⛔ 2026-09-01 — **기계 독립으로 고친다 (kgy 사고).**
#   종전 판은 gabia 전용 절대경로를 **존재 여부와 무관하게** export 했다.
#   kgy 에는 `/data/apps/nvhpc/.../ompi` 가 없는데 `OPAL_PREFIX` 가 거기를 가리켰고,
#   kgy 자기 openmpi-4.1.6 mpirun 이 **없는 prefix 에서 자기 데이터를 찾다가**
#     `mpirun: Error: unknown option "-np"`
#   로 죽었다 (실측 2026-09-01, li_metal/ep_initial). `-np` 는 멀쩡한 옵션이다 —
#   틀린 것은 옵션이 아니라 **환경**이었다. 오진하기 딱 좋은 형태라 여기 박아 둔다.
#   ⇒ 규칙: **없는 경로는 export 하지 않는다.** OPAL_PREFIX 는 하드코딩하지 말고
#     실제로 쓰는 mpirun 의 트리에서 유도한다.
#
# 각 줄이 왜 있나
#   OMP_NUM_THREADS=1        MPI 랭크당 스레드 1개. 안 걸면 랭크마다 코어를 다 물어 경합한다.
#   LD_LIBRARY_PATH          **nvhpc 의 OpenMP 런타임**을 먼저 잡게 한다. 이게 없으면
#                            nvhpc 로 빌드된 pw.x 가 GNU libgomp 를 물고 `libgomp: TODO` 로 죽는다.
#   OPAL_PREFIX / PATH       쓰는 mpirun 과 **같은 트리**를 가리켜야 한다 (섞이면 위 사고).
#   OMPI_ALLOW_RUN_AS_ROOT   gabia 는 root 로 돌아서 이게 없으면 mpirun 이 거부한다.
#   CUDA_VISIBLE_DEVICES=0   A6000/3090 한 장짜리 — 명시해 둔다.
#
# ⛔ 이 파일이 **안 하는 것**
#   · 바이너리가 실제로 도는지 확인하지 않는다 (경로 존재만 본다). 그건 부르는 쪽 몫.
#   · MPI 랭크 수·GPU 점유를 정하지 않는다.
#   · kgy 의 CPU 빌드 QE 를 찾아주지 않는다 — `PW=`/`NEB=` 로 직접 준다.
#
#   자가시험:  bash tools/sei/qe_env.sh --selftest

_qe_env_apply() {
  # 기본값은 gabia. **존재할 때만** 쓴다.
  QE_H_MPI="${QE_H_MPI:-/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi}"

  # ⛔⛔ 2026-09-03 — **nvhpc 는 기계마다 다른 데 있다 (kgy 사고 2차, 실측).**
  #   종전 판은 gabia 절대경로 **하나**만 기본값으로 뒀다. kgy 의 nvhpc 는
  #   `$HOME/apps/nvhpc/...` 에 있어서 "없는 경로는 export 하지 않는다" 규칙이
  #   **정확히 의도대로** 동작한 결과 libnvomp 를 아예 못 잡았고, nvhpc 로 빌드된
  #   neb.x 가 GNU libgomp 를 물어 `libgomp: TODO` 로 즉사했다.
  #   같은 기계의 pw.x 는 **CPU 빌드**(qe-7.4.1-cpu, libgomp 링크)라 멀쩡히 돌았다 —
  #   "pw.x 는 되는데 neb.x 만 죽는다" 는 오진하기 딱 좋은 형태라 여기 박아 둔다.
  #   ⇒ 후보를 늘리는 게 아니라 **판정 기준을 올린다**: "폴더가 있나" 가 아니라
  #     **"libnvomp.so 가 거기 있나"**. 빈 nvhpc 트리를 잡는 반대 실수도 같이 막힌다.
  #   ⚠ QE_NVHPC_SEARCH 는 **따옴표 없이** 전개한다 (글롭이 살아야 버전 디렉터리를 훑는다).
  QE_NVHPC_SEARCH="${QE_NVHPC_SEARCH:-/data/apps/nvhpc/Linux_x86_64/*/compilers/lib $HOME/apps/nvhpc/Linux_x86_64/*/compilers/lib /opt/nvidia/hpc_sdk/Linux_x86_64/*/compilers/lib}"
  QE_NVHPC_LIB="${QE_NVHPC_LIB:-}"
  if [ -z "$QE_NVHPC_LIB" ]; then
    local _c
    # shellcheck disable=SC2086
    for _c in $QE_NVHPC_SEARCH; do
      if [ -e "$_c/libnvomp.so" ]; then QE_NVHPC_LIB="$_c"; break; fi
    done
  fi

  QE_CUDA_SEARCH="${QE_CUDA_SEARCH:-/usr/local/cuda-12.6/lib64 /usr/local/cuda/lib64 /usr/local/cuda-*/lib64}"
  QE_CUDA_LIB="${QE_CUDA_LIB:-}"
  if [ -z "$QE_CUDA_LIB" ]; then
    local _u
    # shellcheck disable=SC2086
    for _u in $QE_CUDA_SEARCH; do
      if [ -e "$_u/libcudart.so" ] || [ -e "$_u/libcudart.so.12" ]; then QE_CUDA_LIB="$_u"; break; fi
    done
  fi

  # ── ① mpirun 을 먼저 정한다 (환경 > gabia 기본 > PATH) ────────────────────
  local _m="${MPIRUN:-}"
  [ -n "$_m" ] && [ ! -x "$_m" ] && _m=""            # 환경값이 실행 불가면 버린다
  [ -n "$_m" ] || { [ -x "$QE_H_MPI/bin/mpirun" ] && _m="$QE_H_MPI/bin/mpirun"; }
  [ -n "$_m" ] || _m="$(command -v mpirun 2>/dev/null || true)"
  MPIRUN="$_m"

  # ── ② OPAL_PREFIX 는 **그 mpirun 의 트리**에서 유도한다 ───────────────────
  #   하드코딩하면 kgy 사고가 재발한다. 유도한 prefix 에 share/openmpi 가 있어야
  #   Open MPI 트리로 인정한다 (MPICH 등에는 없다 → 그때는 안 건드린다).
  if [ -n "$MPIRUN" ]; then
    local _pfx; _pfx="$(cd "$(dirname "$MPIRUN")/.." 2>/dev/null && pwd || true)"
    if [ -n "$_pfx" ] && [ -d "$_pfx/share/openmpi" ]; then
      export OPAL_PREFIX="$_pfx"
      case ":$PATH:" in *":$_pfx/bin:"*) : ;; *) export PATH="$_pfx/bin:$PATH" ;; esac
      [ -d "$_pfx/lib" ] && export LD_LIBRARY_PATH="$_pfx/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
    else
      # Open MPI 트리로 확인 안 되면 **아무것도 안 한다**. 남의 OPAL_PREFIX 를
      # 물려받은 상태면 그게 더 위험하므로 지운다.
      unset OPAL_PREFIX
    fi
  fi

  # ── ③ nvhpc/CUDA 런타임 — 있는 것만 뒤에 붙인다 ──────────────────────────
  local _d
  for _d in "$QE_NVHPC_LIB" "$QE_CUDA_LIB"; do
    [ -d "$_d" ] && export LD_LIBRARY_PATH="${LD_LIBRARY_PATH:+$LD_LIBRARY_PATH:}$_d"
  done

  export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
  export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"
  export OMPI_ALLOW_RUN_AS_ROOT=1
  export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1

  # ── ④ 실행파일 — gabia 기본, 없으면 PATH ─────────────────────────────────
  PW="${PW:-/data/apps/qe-7.4.1-gpu/bin/pw.x}"
  [ -x "$PW" ]  || PW="$(command -v pw.x  2>/dev/null || echo "$PW")"
  NEB="${NEB:-/data/apps/qe-7.4.1-gpu/bin/neb.x}"
  [ -x "$NEB" ] || NEB="$(command -v neb.x 2>/dev/null || echo "$NEB")"

  # ── ⑤ 랭크 옵션 — 부르는 쪽이 덮어쓸 수 있게 변수로 낸다 ─────────────────
  #   `--oversubscribe` 는 코어보다 랭크가 많아도 **허용**할 뿐 성능을 주지 않는다.
  #   Open MPI 가 아닌 런처(MPICH·srun)에서는 없는 옵션이라 비워서 쓴다.
  MPI_NP="${MPI_NP:--np 1}"
  if [ -z "${MPI_OVERSUB+x}" ]; then
    if [ -n "$MPIRUN" ] && "$MPIRUN" --version 2>&1 | grep -qi "open mpi"; then
      MPI_OVERSUB="--oversubscribe"
    else
      MPI_OVERSUB=""
    fi
  fi
}
_qe_env_apply

# ── 자가시험 (직접 실행할 때만) ─────────────────────────────────────────────
# ⚠ 두 겹으로 막는다.
#   ⓐ `BASH_SOURCE[0] = $0` — **source 되면 안 돈다.** `. qe_env.sh` 는 부르는 쪽의
#     위치인자를 그대로 물려받으므로, `run_sei_neb.sh --selftest` 같은 호출이
#     엉뚱하게 이 블록을 깨울 수 있었다.
#   ⓑ 아래 시험들은 `. "$0" _sourced` 로 **인자를 명시**해 다시 부른다. 안 그러면
#     $1 이 여전히 --selftest 라 무한재귀에 빠진다 (실측: 120초 타임아웃).
if [ "${BASH_SOURCE[0]:-$0}" = "$0" ] && [ "${1:-}" = "--selftest" ]; then
  _fail=0; _ok(){ echo "  ok  $1"; }; _no(){ echo "  ⛔  $1"; _fail=1; }
  echo "qe_env.sh --selftest"

  # ① 양성: Open MPI 트리를 흉내내면 OPAL_PREFIX 가 거기로 잡힌다
  _T=$(mktemp -d); mkdir -p "$_T/bin" "$_T/lib" "$_T/share/openmpi"
  printf '#!/bin/sh\necho "mpirun (Open MPI) 4.1.6"\n' > "$_T/bin/mpirun"; chmod +x "$_T/bin/mpirun"
  ( MPIRUN="$_T/bin/mpirun" QE_H_MPI=/nonexistent/x QE_NVHPC_LIB=/nonexistent/y \
    QE_CUDA_LIB=/nonexistent/z OPAL_PREFIX=/stale/prefix; unset MPI_OVERSUB
    . "$0" _sourced >/dev/null 2>&1
    [ "$OPAL_PREFIX" = "$_T" ] || { echo "OPAL_PREFIX=$OPAL_PREFIX"; exit 1; }
    [ "$MPI_OVERSUB" = "--oversubscribe" ] || { echo "OVERSUB=$MPI_OVERSUB"; exit 1; }
  ) && _ok "① Open MPI 트리 → OPAL_PREFIX 유도 + --oversubscribe" \
    || _no "① Open MPI 트리 유도 실패"

  # ② 음성 (핵심): **없는 경로는 절대 export 되지 않는다.** ← kgy 사고의 원인
  ( MPIRUN="$_T/bin/mpirun" QE_H_MPI=/nonexistent/x QE_NVHPC_LIB=/nonexistent/y \
    QE_CUDA_LIB=/nonexistent/z; unset OPAL_PREFIX
    . "$0" _sourced >/dev/null 2>&1
    case ":$LD_LIBRARY_PATH:" in *":/nonexistent/"*) echo "LD=$LD_LIBRARY_PATH"; exit 1 ;; esac
    case ":$PATH:"            in *":/nonexistent/"*) echo "PATH=$PATH"; exit 1 ;; esac
    [ "$OPAL_PREFIX" != "/nonexistent/x" ] || exit 1
  ) && _ok "② 없는 경로는 PATH·LD_LIBRARY_PATH·OPAL_PREFIX 어디에도 안 들어간다" \
    || _no "② 없는 경로가 새어 들어갔다 (kgy 사고 재발)"

  # ③ 음성: Open MPI 가 아니면 OPAL_PREFIX 를 만들지 않고, 물려받은 것도 지운다
  _T2=$(mktemp -d); mkdir -p "$_T2/bin"          # share/openmpi 없음 = 남의 MPI
  printf '#!/bin/sh\necho "HYDRA build details"\n' > "$_T2/bin/mpirun"; chmod +x "$_T2/bin/mpirun"
  ( MPIRUN="$_T2/bin/mpirun" QE_H_MPI=/nonexistent/x OPAL_PREFIX=/stale/prefix; unset MPI_OVERSUB
    . "$0" _sourced >/dev/null 2>&1
    [ -z "${OPAL_PREFIX:-}" ] || { echo "OPAL_PREFIX=$OPAL_PREFIX"; exit 1; }
    [ -z "$MPI_OVERSUB" ] || { echo "OVERSUB=$MPI_OVERSUB"; exit 1; }
  ) && _ok "③ 비-OpenMPI 런처 → OPAL_PREFIX 제거, --oversubscribe 안 붙임" \
    || _no "③ 비-OpenMPI 런처 처리 실패"

  # ④ 음성: 환경으로 준 MPIRUN 이 실행 불가면 버리고 다시 찾는다
  ( MPIRUN=/nonexistent/bin/mpirun QE_H_MPI="$_T"
    . "$0" _sourced >/dev/null 2>&1
    [ "$MPIRUN" != "/nonexistent/bin/mpirun" ] || exit 1
  ) && _ok "④ 실행 불가한 MPIRUN 은 버린다" || _no "④ 죽은 MPIRUN 을 그대로 썼다"

  # ⑤ 부르는 쪽이 준 MPI_OVERSUB 는 언제나 이긴다 (빈 값 포함)
  ( MPIRUN="$_T/bin/mpirun" MPI_OVERSUB="" MPI_NP="-n 4"
    . "$0" _sourced >/dev/null 2>&1
    [ -z "$MPI_OVERSUB" ] && [ "$MPI_NP" = "-n 4" ]
  ) && _ok "⑤ MPI_OVERSUB=''·MPI_NP 오버라이드 존중" || _no "⑤ 오버라이드가 무시됐다"

  # ⑥ 양성: **libnvomp.so 가 있는** 후보를 고른다 (kgy 는 $HOME 밑에 있다)
  _T3=$(mktemp -d); mkdir -p "$_T3/24.11/compilers/lib"; : > "$_T3/24.11/compilers/lib/libnvomp.so"
  ( MPIRUN="$_T/bin/mpirun" QE_NVHPC_SEARCH="$_T3/*/compilers/lib" QE_CUDA_SEARCH=/nonexistent/z
    unset QE_NVHPC_LIB QE_CUDA_LIB
    . "$0" _sourced >/dev/null 2>&1
    [ "$QE_NVHPC_LIB" = "$_T3/24.11/compilers/lib" ] || { echo "NVHPC=$QE_NVHPC_LIB"; exit 1; }
    case ":$LD_LIBRARY_PATH:" in *":$_T3/24.11/compilers/lib:"*) : ;; *) exit 1 ;; esac
  ) && _ok "⑥ libnvomp.so 가 있는 nvhpc 트리를 찾아 LD_LIBRARY_PATH 에 넣는다" \
    || _no "⑥ nvhpc 자동탐색 실패 (kgy libgomp:TODO 재발)"

  # ⑦ 음성 (핵심): 폴더는 있는데 **libnvomp.so 가 없으면** 고르지 않는다.
  #   "폴더가 있나" 로 판정하면 빈 nvhpc 트리를 잡고, 그러면 libgomp 를 물어 죽는다.
  _T4=$(mktemp -d); mkdir -p "$_T4/24.11/compilers/lib"        # libnvomp.so 없음
  ( MPIRUN="$_T/bin/mpirun" QE_NVHPC_SEARCH="$_T4/*/compilers/lib" QE_CUDA_SEARCH=/nonexistent/z
    unset QE_NVHPC_LIB QE_CUDA_LIB
    . "$0" _sourced >/dev/null 2>&1
    [ -z "${QE_NVHPC_LIB:-}" ] || { echo "NVHPC=$QE_NVHPC_LIB"; exit 1; }
    case ":$LD_LIBRARY_PATH:" in *":$_T4/"*) exit 1 ;; esac
  ) && _ok "⑦ ⛔음성: libnvomp.so 가 없는 빈 트리는 **고르지 않는다** (폴더 존재만 보지 않는다)" \
    || _no "⑦ 빈 nvhpc 트리를 잡았다"

  # ⑧ 환경으로 준 QE_NVHPC_LIB 는 탐색보다 언제나 이긴다
  ( MPIRUN="$_T/bin/mpirun" QE_NVHPC_LIB=/explicit/path QE_NVHPC_SEARCH="$_T3/*/compilers/lib"
    . "$0" _sourced >/dev/null 2>&1
    [ "$QE_NVHPC_LIB" = "/explicit/path" ]
  ) && _ok "⑧ 손으로 준 QE_NVHPC_LIB 가 자동탐색을 이긴다" || _no "⑧ 오버라이드가 무시됐다"

  rm -rf "$_T" "$_T2" "$_T3" "$_T4"
  [ "$_fail" = 0 ] && echo "PASS (8/8)" || { echo "FAIL"; exit 1; }
fi

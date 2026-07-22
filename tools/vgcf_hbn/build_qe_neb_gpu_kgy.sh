#!/usr/bin/env bash
# =============================================================================
# build_qe_neb_gpu_kgy.sh — QE 7.4.1 GPU 빌드 (pw + neb) on kgy.
#
# 기존 qe-7.4.1-gpu 빌드 트리 소멸(설치 bin만 남음, make.inc/NEB/PW.o 없음) ->
# neb.x 확보 위해 from-source GPU 빌드. 컴파일=CPU라 GPU 계산과 병렬 안전.
# RTX3090 = compute 8.6(cc86), CUDA 12.6(NVHPC 번들), MPI=HPC-X.
#
#   bash tools/vgcf_hbn/build_qe_neb_gpu_kgy.sh configure   # 다운로드+configure (GPU 감지 확인)
#   # -> make.inc에 'DFLAGS ... -D__CUDA' 뜨는지 확인 후:
#   bash tools/vgcf_hbn/build_qe_neb_gpu_kgy.sh build       # make pw neb (~30-45min)
# 완료 시 neb.x를 기존 gpu bin에 배치 -> run_neb_kgy.sh 그대로 GPU NEB 실행.
# =============================================================================
set -u; set +H
# ⚠ conda(uma) 환경이 CFLAGS="-march=nocona ..."를 심음 -> nvc가 nocona 거부(2026-07-22).
# 빌드 전 conda 컴파일 플래그 전부 제거 (gabia_cdd_phx.md "conda deactivate 필수").
unset CFLAGS CPPFLAGS CXXFLAGS FFLAGS FCFLAGS F90FLAGS LDFLAGS DEBUG_CFLAGS DEBUG_CXXFLAGS DEBUG_FFLAGS 2>/dev/null || true
PHASE=${1:-configure}
SRC=$HOME/apps/qe-7.4.1-src
GPUBIN=$HOME/apps/qe-7.4.1-gpu/bin
NV=$HOME/apps/nvhpc/Linux_x86_64/24.11
HPCX="$(ls -d "$NV"/comm_libs/*/hpcx/hpcx-*/ompi 2>/dev/null | sort | tail -1)"
CUDAHOME=$NV/cuda/12.6
[ -d "$CUDAHOME" ] || CUDAHOME="$(ls -d "$NV"/cuda/12.* 2>/dev/null | sort -V | tail -1)"
# conda bin 경로 완전 제거 (2026-07-22): CFLAGS unset만으론 부족 — conda binutils
# (x86_64-conda-linux-gnu-ld/ar)가 NVHPC GPU 링크(-cuda/-gpu/-acc)를 깨뜨림.
# PATH에서 conda/miniforge/envs 경로 싹 걷어내고 NVHPC만 앞세움 (=conda deactivate 등가).
PATH="$(printf '%s' "$PATH" | tr ':' '\n' | grep -viE 'conda|miniforge|mamba|/envs/' | paste -sd: -)"
export PATH="$NV/compilers/bin:$HPCX/bin:/usr/bin:/bin:$PATH"
export LD_LIBRARY_PATH="$NV/compilers/lib:$CUDAHOME/lib64:$NV/math_libs/lib64:$HPCX/lib:${LD_LIBRARY_PATH:-}"
export OPAL_PREFIX="$HPCX" OMPI_FC=nvfortran OMPI_CC=nvc
echo "toolchain: $(which nvfortran) | $(which mpif90) | CUDA=$CUDAHOME"
which nvfortran mpif90 >/dev/null || { echo "ERROR: nvfortran/mpif90 없음 (NVHPC env 확인)"; exit 1; }

if [ "$PHASE" = configure ]; then
  mkdir -p "$(dirname "$SRC")"; cd "$(dirname "$SRC")"
  if [ ! -f "$SRC/configure" ]; then
    echo "[dl] QE 7.4.1 source (gitlab archive)..."
    wget -q "https://gitlab.com/QEF/q-e/-/archive/qe-7.4.1/q-e-qe-7.4.1.tar.gz" -O qe741.tar.gz \
      || { echo "다운로드 실패 — URL/네트워크 확인 (대안: github releases)"; exit 1; }
    tar xzf qe741.tar.gz && rm -rf "$SRC" && mv q-e-qe-7.4.1 "$SRC"
  fi
  cd "$SRC"
  echo "[env] conda 플래그 제거 확인: CFLAGS='${CFLAGS:-(빔)}'"
  ./configure --with-cuda="$CUDAHOME" --with-cuda-cc=86 --with-cuda-runtime=12.6 \
     --enable-openmp F90=nvfortran CC=nvc MPIF90=mpif90 2>&1 | tail -35
  # configure가 남긴 -march/nocona 잔재를 make.inc에서도 소거 (이중 안전)
  sed -i 's/-march=nocona[^ ]*//g; s/-mtune=[^ ]*//g' "$SRC"/make.inc 2>/dev/null || true
  echo "── GPU 감지 (make.inc) ──"
  grep -iE "__CUDA|cuda|GPU_ARCH|MANUAL_DFLAGS" "$SRC"/make.inc 2>/dev/null | head -6
  echo ">> make.inc에 -D__CUDA 보이면 GPU OK -> 'build' 단계로"

elif [ "$PHASE" = build ]; then
  [ -f "$SRC/make.inc" ] || { echo "ERROR: configure 먼저 (make.inc 없음)"; exit 1; }
  cd "$SRC"
  # ⚠ 'make -j8 pw neb'(동시 goal)은 병렬 경합으로 externals 직후 죽음(2026-07-22).
  # -> pw 먼저 완성(-j8) 후 neb 링크. 전체 로그 파일 보존(tail 파이프 금지).
  echo "[build] make -j8 pw  ($(date +%H:%M:%S)) -> ~/qe_pw_build.log"
  make -j8 pw > "$HOME/qe_pw_build.log" 2>&1; pw_rc=$?
  echo "  pw rc=$pw_rc  (tail:)"; tail -4 "$HOME/qe_pw_build.log"
  [ "$pw_rc" = 0 ] && [ -f "$SRC/bin/pw.x" ] || {
    echo "!! pw 빌드 실패 — 에러:"; grep -inE "error|cannot|undefined|No rule|Stop|fatal" "$HOME/qe_pw_build.log" | tail -15; exit 1; }
  echo "[build] make neb  ($(date +%H:%M:%S)) -> ~/qe_neb_build.log"
  make neb > "$HOME/qe_neb_build.log" 2>&1
  [ -f "$SRC/bin/neb.x" ] || { echo "!! neb 빌드 실패 — 에러:"; grep -inE "error|cannot|undefined|Stop" "$HOME/qe_neb_build.log" | tail -15; }
  echo "── 결과 ──"
  if [ -f "$SRC/bin/neb.x" ]; then
    cp "$SRC/bin/neb.x" "$GPUBIN/" && echo "neb.x -> $GPUBIN/ (배치완료)"
    ls -la "$GPUBIN/neb.x"
    echo "── GPU 링크 확인 ──"; ldd "$GPUBIN/neb.x" 2>/dev/null | grep -iE "cufft|cudart|cuda" | head -4
    echo ">> run_neb_kgy.sh 그대로 GPU NEB 실행 가능"
  else
    echo "!! neb.x 생성 실패 — 위 make tail 붙여줘"; exit 1
  fi
fi

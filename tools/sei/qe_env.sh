# QE-GPU 실행 환경 — **source 해서 쓴다.** 이 파일이 정본이다.
#
# ⛔ 왜 파일로 뽑았나 (2026-08-28)
#   `run_prereq_chain.sh` 를 새로 쓰면서 `MPIRUN`·`PW` 경로만 챙기고 **환경변수를 통째로
#   빠뜨렸다.** 결과: `libgomp: TODO` 로 pw.x 가 즉사했고, 밤새 돌 예정이던 체인이
#   첫 점에서 끝났다. 기존 `run_sei_neb.sh` 는 같은 블록을 제대로 갖고 있었다 —
#   **복사했어야 할 것을 새로 쓴 것이 아니라, 아예 안 쓴 것**이 문제였다.
#   ⇒ 두 스크립트가 같은 파일을 source 한다. 갈라질 수가 없다.
#
# 각 줄이 왜 있나
#   OMP_NUM_THREADS=1        MPI 랭크당 스레드 1개. 안 걸면 랭크마다 코어를 다 물어 경합한다.
#   LD_LIBRARY_PATH          **nvhpc 의 OpenMP 런타임**을 먼저 잡게 한다. 이게 없으면
#                            nvhpc 로 빌드된 pw.x 가 GNU libgomp 를 물고 `libgomp: TODO` 로 죽는다.
#   OPAL_PREFIX / PATH       hpcx OpenMPI 를 쓰게 한다 (시스템 mpirun 과 섞이면 랭크가 안 뜬다).
#   OMPI_ALLOW_RUN_AS_ROOT   gabia 는 root 로 돌아서 이게 없으면 mpirun 이 거부한다.
#   CUDA_VISIBLE_DEVICES=0   A6000 한 장짜리 — 명시해 둔다.
#
# ⛔ 이 파일이 **안 하는 것**: 바이너리가 있는지 확인하지 않는다. 그건 부르는 쪽 몫이다.

QE_H_MPI="${QE_H_MPI:-/data/apps/nvhpc/Linux_x86_64/24.11/comm_libs/12.6/hpcx/hpcx-2.20/ompi}"
QE_NVHPC_LIB="${QE_NVHPC_LIB:-/data/apps/nvhpc/Linux_x86_64/24.11/compilers/lib}"
QE_CUDA_LIB="${QE_CUDA_LIB:-/usr/local/cuda-12.6/lib64}"

export PATH="$QE_H_MPI/bin:$PATH"
export OPAL_PREFIX="$QE_H_MPI"
export OMP_NUM_THREADS="${OMP_NUM_THREADS:-1}"
export CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-0}"
export OMPI_ALLOW_RUN_AS_ROOT=1
export OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
export LD_LIBRARY_PATH="$QE_H_MPI/lib:$QE_NVHPC_LIB:$QE_CUDA_LIB${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

MPIRUN="${MPIRUN:-$QE_H_MPI/bin/mpirun}"
PW="${PW:-/data/apps/qe-7.4.1-gpu/bin/pw.x}"
NEB="${NEB:-/data/apps/qe-7.4.1-gpu/bin/neb.x}"

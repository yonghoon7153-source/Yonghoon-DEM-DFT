#!/bin/bash
#SBATCH --job-name=ps73B
#SBATCH --output=logs/%x_%j.out
#SBATCH --qos=cpu-60
#SBATCH --partition=cpu
#SBATCH -n 10
#SBATCH --time=3-00:00:00
# ps73 감쇠 가지 실험 (DEMP-01) — ibb 제출 래퍼 (1저자 10-08 "10 코어로" · WSL 대신).  정본 설명 = 같은 폴더 README.md §6-ibb.
#   하는 일 = run_branch.sh 기본 (t0 → PASS 면 B) 을 NP 10 · lmp_mpi 로.  #SBATCH -n 10 ↔ mpirun --oversubscribe --bind-to none -np 10 짝
#   (mpirun 줄은 run_branch.sh 가 쓴다 · 여기서는 SLURM_NTASKS = NP 를 대조한다 · t0 는 'Loop time … on N procs' 의 N = NP 를 본다).
#   제출 = 작업 폴더에서 (출력 logs/ 는 제출 폴더 기준 — 먼저 만든다):  sbatch <kit 폴더>/run_branch_ibb.sbatch <kit 폴더>
#   SLURM 밖에서 bash 로 부르면 = 제출 전 사전 점검만 (같은 환경 · 같은 경로 · run_branch.sh --preflight-only · 런 없음).
#   ⚠ QOS cpu-60 이 차 있으면 PD 로 기다리다 코어가 비면 저절로 시작한다 (정상) — 다른 job 을 끄지 않는다 (1저자 10-08 Q1 (가)).
#   ⚠ ALLOW_CONCURRENT=1: 노드에 다른 job 의 lmp_mpi 가 보여도 코어는 SLURM 이 나눠 준다 (WSL 용 '다른 LIGGGHTS' 검사를 넘긴다).
#   ⚠ 이 파일도 덱 묶음 SHA256SUMS 에 든다 — 고치면 make_branch_decks.py 로 SHA256SUMS 를 다시 쓴다.

source ~/.bashrc
conda activate myenv
set -uo pipefail

SRC_KIT=${1:-}
NP=10
LMP=${LMP:-/lustre/home/yonghoon/LIGGGHTS-PUBLIC/src/lmp_mpi}
WORK_ROOT=${WORK_ROOT:-$HOME/ps73_branch_20261007_ibb}

if [ -z "$SRC_KIT" ] || [ ! -f "$SRC_KIT/run_branch.sh" ]; then
  echo "⛔ 첫 인자 = kit 폴더 (…/docs/data/ps73_damping_branch_20261007) — 받은 것: '$SRC_KIT'"
  exit 3
fi
SRC_KIT=$(cd "$SRC_KIT" && pwd)

if [ -n "${SLURM_JOB_ID:-}" ]; then
  if [ "${SLURM_NTASKS:-}" != "$NP" ]; then
    echo "⛔ SLURM_NTASKS=${SLURM_NTASKS:-없음} ≠ NP=$NP — #SBATCH -n 과 mpirun -np 짝이 깨졌다"
    exit 3
  fi
  echo "job $SLURM_JOB_ID · 노드 ${SLURM_JOB_NODELIST:-?} · 시작 $(date -Iseconds) · kit $SRC_KIT · LMP $LMP · mpirun $(command -v mpirun || echo 없음)"
  cd "$WORK_ROOT" || exit 3
  exec env WORK_ROOT="$WORK_ROOT" NP="$NP" LMP="$LMP" ALLOW_CONCURRENT=1 bash "$SRC_KIT/run_branch.sh"
fi

echo "제출 전 사전 점검 (SLURM 밖 · 런 없음) — kit $SRC_KIT · LMP $LMP · mpirun $(command -v mpirun || echo 없음)"
exec env WORK_ROOT="$WORK_ROOT" NP="$NP" LMP="$LMP" ALLOW_CONCURRENT=1 bash "$SRC_KIT/run_branch.sh" --preflight-only

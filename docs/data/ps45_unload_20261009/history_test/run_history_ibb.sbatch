#!/bin/bash
#SBATCH --job-name=ulHist
#SBATCH --output=logs/%x_%j.out
#SBATCH --qos=cpu-60
#SBATCH --partition=cpu
#SBATCH -n 6
#SBATCH --time=0-01:00:00
# DEM 언로딩 키트 — 작은 침대 이력 시험 (H0–H5) ibb 제출 래퍼.  정본 설명 = ../README.md §1.
#   하는 일 = run_history.sh 전 단계를 NP 6 · lmp_mpi 로.  #SBATCH -n 6 ↔ mpirun --oversubscribe --bind-to none -np 6 짝
#   (mpirun 줄은 run_history.sh 가 쓴다 · 여기서는 SLURM_NTASKS = NP 를 대조한다 · H2 단계만 NP_ALT 4 = 같은 할당 안에서 더 적게).
#   제출 = 작업 폴더에서 (출력 logs/ 는 제출 폴더 기준 — 먼저 만든다):  sbatch <kit>/history_test/run_history_ibb.sbatch <kit>/history_test
#   둘째 인자 grammar = 문법 fixture 만 (run_history.sh --grammar-only · P → GA → GB · 등록 개정 3 §14-9 · README §1-6).
#   SLURM 밖에서 bash 로 부르면 = 제출 전 사전 점검만 (같은 환경 · 같은 경로 · run_history.sh --preflight-only · 런 없음).
#   ⚠ 다른 job 을 끄지 않는다 (등록 머리 · 1저자 10-08 Q1 (가)) — cpu-60 이 차 있으면 PD 로 기다리다 저절로 시작한다.
#   ⚠ 이 파일도 묶음 SHA256SUMS 에 든다 — 고치면 make_history_decks.py 로 SHA256SUMS 를 다시 쓴다.

source ~/.bashrc
conda activate myenv
set -uo pipefail

SRC_KIT=${1:-}
case "${2:-}" in
  '') MODE_ARGS=() ;;
  grammar) MODE_ARGS=(--grammar-only) ;;
  *) echo "⛔ 둘째 인자 = (없음) 또는 grammar — 받은 것: '${2:-}'"; exit 3 ;;
esac
NP=6
NP_ALT=4
LMP=${LMP:-/lustre$HOME/LIGGGHTS-PUBLIC/src/lmp_mpi}
WORK_ROOT=${WORK_ROOT:-$HOME/ps45_unload_hist_20261013}

if [ -z "$SRC_KIT" ] || [ ! -f "$SRC_KIT/run_history.sh" ]; then
  echo "⛔ 첫 인자 = 이력 시험 폴더 (…/docs/data/ps45_unload_20261009/history_test) — 받은 것: '$SRC_KIT'"
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
  exec env WORK_ROOT="$WORK_ROOT" NP="$NP" NP_ALT="$NP_ALT" LMP="$LMP" ALLOW_CONCURRENT=1 bash "$SRC_KIT/run_history.sh" ${MODE_ARGS[@]+"${MODE_ARGS[@]}"}
fi

echo "제출 전 사전 점검 (SLURM 밖 · 런 없음) — kit $SRC_KIT · LMP $LMP · mpirun $(command -v mpirun || echo 없음)"
exec env WORK_ROOT="$WORK_ROOT" NP="$NP" NP_ALT="$NP_ALT" LMP="$LMP" ALLOW_CONCURRENT=1 bash "$SRC_KIT/run_history.sh" --preflight-only ${MODE_ARGS[@]+"${MODE_ARGS[@]}"}

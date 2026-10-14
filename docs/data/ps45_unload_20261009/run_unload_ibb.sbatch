#!/bin/bash
#SBATCH --job-name=ulU
#SBATCH --output=logs/%x_%j.out
#SBATCH --qos=cpu-60
#SBATCH --partition=cpu
#SBATCH -n 6
#SBATCH --time=5-00:00:00
# DEM 언로딩 키트 — ibb 제출 래퍼 (잡 하나).  정본 설명 = README.md §3.  ⛔ 본 R · 10:0 연장 · U 는 Codex GO 뒤.
#   하는 일 = run_unload.sh <침대> <잡> 을 NP 6 · lmp_mpi 로.  #SBATCH -n 6 ↔ mpirun --oversubscribe --bind-to none -np 6 짝
#   (mpirun 줄은 run_unload.sh 가 쓴다 · 여기서는 SLURM_NTASKS = NP 를 대조한다).  5 일 = 등록 §5-2 잡 시간 한도 (cpu-60).
#   제출 = 작업 폴더에서 (출력 logs/ 는 제출 폴더 기준 — 먼저 만든다):  sbatch <kit>/run_unload_ibb.sbatch <kit> <침대> <잡>
#   이어 돌림 (기계 실패 한 번):  sbatch --export=ALL,RESUME=1 <kit>/run_unload_ibb.sbatch <kit> <침대> <팔>   (UC = fresh-attempt-only)
#   RJ · RJ2 · EXT = 문법 fixture PASS 판정 필수 (사전 점검이 LIGGGHTS 전에 대조 · Q5):  --export=ALL,GRAMMAR_VERDICT=<…/gram_<시각>/grammar_verdict.json>,…
#   SLURM 밖에서 bash 로 부르면 = 제출 전 사전 점검만 (같은 환경 · 같은 경로 · 관문 포함 · run_unload.sh --preflight-only · 런 없음).
#   ⚠ 다른 job 을 끄지 않는다 — cpu-60 이 차 있으면 PD 로 기다리다 저절로 시작한다.
#   ⚠ 이 파일도 묶음 SHA256SUMS 에 든다 — 고치면 seal_kit.py --write 로 SHA256SUMS 를 다시 쓴다.

source ~/.bashrc
conda activate myenv
set -uo pipefail

SRC_KIT=${1:-}; BED=${2:-}; JOB=${3:-}
NP=6
LMP=${LMP:-/lustre$HOME/LIGGGHTS-PUBLIC/src/lmp_mpi}
WORK_ROOT=${WORK_ROOT:-$HOME/ps45_unload_20261009}

if [ -z "$SRC_KIT" ] || [ ! -f "$SRC_KIT/run_unload.sh" ] || [ -z "$BED" ] || [ -z "$JOB" ]; then
  echo "⛔ 인자 = <키트 폴더 (…/docs/data/ps45_unload_20261009)> <침대> <잡> — 받은 것: '$SRC_KIT' '$BED' '$JOB'"
  exit 3
fi
SRC_KIT=$(cd "$SRC_KIT" && pwd)

if [ -n "${SLURM_JOB_ID:-}" ]; then
  if [ "${SLURM_NTASKS:-}" != "$NP" ]; then
    echo "⛔ SLURM_NTASKS=${SLURM_NTASKS:-없음} ≠ NP=$NP — #SBATCH -n 과 mpirun -np 짝이 깨졌다"
    exit 3
  fi
  echo "job $SLURM_JOB_ID · 노드 ${SLURM_JOB_NODELIST:-?} · 시작 $(date -Iseconds) · kit $SRC_KIT · $BED $JOB · LMP $LMP · mpirun $(command -v mpirun || echo 없음)"
  cd "$WORK_ROOT" || exit 3
  exec env WORK_ROOT="$WORK_ROOT" NP="$NP" LMP="$LMP" ALLOW_CONCURRENT=1 bash "$SRC_KIT/run_unload.sh" "$BED" "$JOB"
fi

echo "제출 전 사전 점검 (SLURM 밖 · 런 없음) — kit $SRC_KIT · $BED $JOB · LMP $LMP · mpirun $(command -v mpirun || echo 없음)"
exec env WORK_ROOT="$WORK_ROOT" NP="$NP" LMP="$LMP" ALLOW_CONCURRENT=1 bash "$SRC_KIT/run_unload.sh" "$BED" "$JOB" --preflight-only

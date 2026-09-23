#!/bin/bash
#SBATCH -J wad_sese
#SBATCH -p amd_a100nv_8
#SBATCH -N 1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:4
#SBATCH --time=12:00:00
#SBATCH -o /scratch/x3430a02/kgy/wad_sese_2026_09_23/logs/sese_%j.out
#SBATCH -e /scratch/x3430a02/kgy/wad_sese_2026_09_23/logs/sese_%j.err
#SBATCH --comment qe
# =============================================================================
# sbatch_sese_kisti.sh — SE|SE 대조 잡을 KISTI A100 **4장**에 평면파 분산으로 돌린다
#                        (tools/wad/run_sese_gpu.sh 를 감싼다 — 판정·해시·D3 검사는 러너 것 그대로)
#
# 왜 KISTI 인가 (gabia CPU 1랭크 추정 · 2026-09-23 · QE `Estimated max dynamical RAM`)
#   01_bulk_scf 6.7 GB · 02_s_outer_scf **55.8 GB** · 02_li_outer_scf **50.2 GB**
#   → A6000 48 GB 한 장에 슬랩이 안 들어간다 (b2o3 와 공유는 물론, 혼자여도).
#   `-np 4 -nk 1` 은 G-벡터·평면파를 4랭크에 나눠 **GPU 한 장당** 메모리를 ~1/4 로 줄인다
#   (tools/sdcp/sbatch_phaseB_v3_kisti.sh 와 같은 방식 — 226원자 DFT+U 를 이렇게 돌렸다).
#
# 제출 (KISTI 로그인 노드 · repo worktree 안에서):
#   mkdir -p /scratch/x3430a02/kgy/wad_sese_2026_09_23/logs
#   sbatch tools/wad/sbatch_sese_kisti.sh                      # 기본: SCF 3잡
#   JOBS="03_s_outer_relax_pbe" sbatch --export=ALL tools/wad/sbatch_sese_kisti.sh
#   끝난 잡은 러너가 건너뛴다 → 벽시계에 끊기면 같은 명령으로 다시 제출하면 이어 간다 (SCF 는 처음부터).
#
# ⚠ KISTI QOS: 동시 제출 제한 · **scancel 직후 재제출 금지** (카운터 지연 — CLAUDE.md).
#
# ⛔ 이 스크립트가 못 하는 것
#   · relax 가 벽시계에 끊기면 **처음 좌표부터** 다시 한다 (마지막 ATOMIC_POSITIONS 이어받기 미구현)
#     → 첫 제출은 SCF 3잡만. 이완은 SCF 벽시계를 본 뒤 시간을 잡아 따로 낸다.
#   · A100 이 40 GB 판인지 80 GB 판인지 모른다 — 장당 ~14 GB 예상이라 둘 다 들어가야 하지만,
#     QE 가 OOM 으로 죽으면 러너가 '미완료' 로 멈춘다. 그때는 NP=8 + --gres=gpu:8.
#   · PP 해시를 **자동 대조하지 않는다** — 러너 로그의 sha256 16자를 gabia 값과 사람이 대 본다
#     (cl 5b1ebdea1e5ba743 · li 02cc4b3810e28a43 · P 2d112dfec2e2d9b7 · s 84ad731864187f41).
# =============================================================================
set -u
REPO=${REPO:-${SLURM_SUBMIT_DIR:-$(pwd)}}
RUN=${RUN:-/scratch/x3430a02/kgy/wad_sese_2026_09_23/run}
mkdir -p "$RUN" "$(dirname "$RUN")/logs"
export NP=${NP:-4} NO_LOCK=1
export PSEUDO_DIR=${PSEUDO_DIR:-/scratch/x3430a02/kgy/manuscript_support/pseudo}
export PWX=${PWX:-/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x}
# 전용 노드라 공존할 UMA 가 없다 — 가드는 장별 한도 근처에서만 (80 GB 판 기준 · 40 GB 판이면 QE 가 먼저 OOM 을 낸다)
export START_MAX_MIB=${START_MAX_MIB:-70000} KILL_MIB=${KILL_MIB:-79000} HOST_START_MIB=${HOST_START_MIB:-16384}
export EXCEPTION_ID="KISTI 전용 노드 — 공존 없음"
export JOBS=${JOBS:-"01_bulk_scf 02_s_outer_scf 02_li_outer_scf"}
export OMP_NUM_THREADS=${OMP_NUM_THREADS:-8}
echo "===== wad_sese  job=${SLURM_JOB_ID:-local}  repo=$REPO  $(date) ====="
git -C "$REPO" log -1 --format='repo %h %cd' --date=iso 2>/dev/null
bash "$REPO/tools/wad/run_sese_gpu.sh" "$REPO/db/inputs/wad_sese_control_2026_09_23" "$RUN"

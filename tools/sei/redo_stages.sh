#!/usr/bin/env bash
# redo_stages.sh — 특정 단계만 다시 돌리기 위해 그 단계의 산출만 지운다.
#   ⚠ 러너는 'JOB DONE' 으로 완료를 판정하므로, 입력을 고쳐도 옛 .out 이 있으면 건너뛴다.
#     vc-relax·scf 는 유지해야 tmp 의 전하밀도를 재사용한다.
#
#   bash tools/sei/redo_stages.sh 03 04 05 06     # 갭·DOS·PDOS 만 다시
set -u
WORK=${WORK:-/data/work/runs/sei_dft}
[ $# -eq 0 ] && { echo "쓰기: bash $0 03 04 05 06"; exit 1; }
for d in "$WORK"/*/; do
  for s in "$@"; do
    rm -f "$d"/${s}_*.out
  done
  rm -f "$d/gap.json"
done
echo "지움: 단계 $* 의 .out 과 gap.json  (01·02 와 tmp 는 유지 — 전하밀도 재사용)"
echo "다시:  tmux new -s seidft -d \"bash tools/sei/run_sei_dft.sh 2>&1 | tee -a ~/logs/sei_dft.log\""

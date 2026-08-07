#!/usr/bin/env bash
# redo_stages.sh — 특정 단계만 다시 돌리기 위해 그 단계의 산출만 지운다.
#   ⚠ 러너는 'JOB DONE' 으로 완료를 판정하므로, 입력을 고쳐도 옛 .out 이 있으면 건너뛴다.
#     vc-relax·scf 는 유지해야 tmp 의 전하밀도를 재사용한다.
#
#   bash tools/sei/redo_stages.sh 03 04 05 06            # 전 조성의 갭·DOS·PDOS
#   TAG=licl bash tools/sei/redo_stages.sh 04 05 06      # licl 만
#
# ⚠ TAG 를 안 주면 **끝난 조성까지 전부 지운다.** 9종 중 1종만 깨졌을 때 전부 다시 돌리면
#   멀쩡한 8종을 몇 시간 더 태운다 (2026-08-07 licl 04 단독 실패). 부분 실패는 TAG 로 좁힌다.
set -u
WORK=${WORK:-/data/work/runs/sei_dft}
TAG=${TAG:-}
[ $# -eq 0 ] && { echo "쓰기: bash $0 03 04 05 06     (한 조성만: TAG=licl bash $0 04 05 06)"; exit 1; }

shopt -s nullglob
if [ -n "$TAG" ]; then
  DIRS=("$WORK"/*"$TAG"*/)
  [ ${#DIRS[@]} -eq 0 ] && { echo "⛔ '$TAG' 에 맞는 폴더가 $WORK 에 없다"; exit 1; }
else
  DIRS=("$WORK"/*/)
fi

for d in "${DIRS[@]}"; do
  for s in "$@"; do
    rm -f "$d"/${s}_*.out
  done
  # gap.json 은 03 을 다시 돌릴 때만 무효다 — 04~06 재실행에는 갭이 그대로 유효하다
  case " $* " in *" 03 "*) rm -f "$d/gap.json";; esac
  echo "  · $(basename "$d")"
done
echo "지움: 단계 $* $( [ -n "$TAG" ] && echo "(TAG=$TAG, ${#DIRS[@]}개 폴더)" || echo "(전 조성)" )"
echo "  01·02 와 tmp 는 유지 — 전하밀도 재사용"
echo "다시:  tmux new -s seidft -d \"bash tools/sei/run_sei_dft.sh 2>&1 | tee -a ~/logs/sei_dft.log\""

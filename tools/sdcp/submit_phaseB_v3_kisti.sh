#!/bin/bash
# submit_phaseB_v3_kisti.sh — Phase-B v3 를 afterany 체인으로 제출한다.
#   bash tools/sdcp/submit_phaseB_v3_kisti.sh [세그먼트 수]   # 기본 2
#
# afterany 인 이유: TIMEOUT 으로 끝난 세그먼트도 다음 세그먼트를 띄워야 한다
# (세그먼트는 resume-safe — JOB DONE 인 job 은 건너뛴다).
#
# ⚠ KISTI QOS: 사용자당 동시 제출 4개 제한. 먼저 세고 빈 슬롯에만 넣을 것.
#   그리고 scancel 직후에는 재제출하지 말 것 — 카운터가 늦게 반영된다.
set -e
N=${1:-2}
HERE=$(cd "$(dirname "$0")" && pwd)
SEG=$HERE/sbatch_phaseB_v3_kisti.sh
mkdir -p /scratch/x3430a02/kgy/sdcp_phaseB_v3/logs

cur=$(squeue -u x3430a02 -h 2>/dev/null | wc -l)
echo "현재 대기/실행 중인 job $cur 개 (QOS 상한 4)"
[ "$((cur + N))" -gt 4 ] && { echo "⛔ $N 개를 더 넣으면 상한을 넘는다 — 줄이거나 기다릴 것"; exit 1; }

jid=$(sbatch --parsable "$SEG"); echo "segment 1: job $jid"
for i in $(seq 2 "$N"); do
  jid=$(sbatch --parsable --dependency=afterany:$jid "$SEG")
  echo "segment $i: job $jid (afterany:이전)"
done
echo
echo "watch: squeue -u x3430a02 ; tail -f /scratch/x3430a02/kgy/sdcp_phaseB_v3/logs/pb3_*.out"

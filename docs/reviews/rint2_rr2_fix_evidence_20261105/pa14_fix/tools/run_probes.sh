#!/bin/bash
# 사전 공격 14 탐침 전부 다시 (탐침 원판 그대로 · 머리 env 규약 = PA14_SRC · TD = <pa14>/tmp) —
#   before = base_tree/scripts (사슬 · 시험 = 바탕 379e85856 = 사전 공격 14 대상 7a582acf5 와 같은 blob) · after = 작업 트리 (고친 판)
# 쓰임: bash run_probes.sh [before|after|both]
set -u
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/pa14fix
P=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/pa14
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a271b07eec3fe5332
OUT=$H/probe_out
mkdir -p "$OUT" "$P/tmp" "$H/logs"
exec > >(tee -a "$H/logs/probe_rerun.log") 2>&1
PROBES="p1_resume_bypass p2_chain3 p3_value_domain p4_predict_resume p5_arm_forms p6_attempt_json p7_relabel p8_survivor_inputs"
which="${1:-both}"
for side in before after; do
  if [ "$which" != both ] && [ "$which" != "$side" ]; then continue; fi
  if [ "$side" = before ]; then S=$H/base_tree/scripts; else S=$WT/scripts; fi
  echo "== $side PA14_SRC=$S"
  sha256sum "$S/rint_r_chain.py" "$S/test_rint_r_chain.py"
  for p in $PROBES; do
    t0=$(date +%s)
    (cd "$P/probes" && PA14_SRC="$S" python3 "$P/probes/$p.py" > "$OUT/${p}_${side}.out" 2>&1)
    rc=$?
    echo "$p rc=$rc $(( $(date +%s) - t0 ))s"
  done
done

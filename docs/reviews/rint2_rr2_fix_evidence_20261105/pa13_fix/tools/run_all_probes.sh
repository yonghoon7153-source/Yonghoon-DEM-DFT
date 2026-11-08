#!/bin/bash
# 사전 공격 13 탐침 전부 다시 (고치기 전 = before_final_tree/scripts (사슬 = f44478535 = 742a3b83f 의 rint_r_chain.py 바이트 · 시험 = 고친 판) · 고친 뒤 = 작업 트리)
set -u
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/pa13fix
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a068e367fbc7fc5b1
OUT=$H/probe_out_final
mkdir -p "$OUT" "$H/tmp"
ORIG="p1_value_domain p1b_value_domain_cli p2_resume_mismatch p2b_resume_mismatch_chain p3_honest_shapes:main,pred p3_honest_shapes:units,over p4_all_arm_forms p5_value_domain_honest:units p6_struct_edges"
NEW="p2c_resume_stronger p4v_all_arm_forms_values p5b_value_domain_real:units"
for side in before after; do
  if [ "$side" = before ]; then S=$H/before_final_tree/scripts; else S=$WT/scripts; fi
  echo "== $side scripts=$S"
  sha256sum "$S/rint_r_chain.py" "$S/test_rint_r_chain.py"
  python3 "$H/run_probes.py" "$S" "$H/probes_orig" "$OUT" "$side" $ORIG
  python3 "$H/run_probes.py" "$S" "$H/probes" "$OUT" "$side" $NEW
done
echo "== after py3.8 (p1)"
PY38=/root/.local/share/uv/python/cpython-3.8-linux-x86_64-gnu/bin/python3.8
"$PY38" --version
"$PY38" "$H/run_probes.py" "$WT/scripts" "$H/probes_orig" "$OUT" after_py38 p1_value_domain
echo "done"

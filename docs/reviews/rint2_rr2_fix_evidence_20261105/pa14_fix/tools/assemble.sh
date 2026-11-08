#!/bin/bash
# 증거 폴더 모으기 — 사전 공격 14 원 자료 반입 (preattack14/) · 고침 증거 (pa14_fix/: code.diff · code_sha256.txt · logs · probe_out · tools) — REPORT.md · SHA256SUMS 는 따로
set -eu
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/d26d1e75-209f-540f-83a8-c0e1957edc2f/scratchpad/pa14fix
WT=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a271b07eec3fe5332
E=$WT/docs/reviews/rint2_rr2_fix_evidence_20261105
P14=$E/preattack14
F14=$E/pa14_fix
mkdir -p "$P14/probes" "$P14/out" "$F14/logs/py38" "$F14/probe_out" "$F14/tools"
cp "$H/import_pa14/REPORT.md" "$P14/REPORT.md"
cp "$H/import_pa14/probes/"*.py "$P14/probes/"
cp "$H/import_pa14/out/"* "$P14/out/"
cd "$WT"
git diff 379e85856 -- scripts/rint_r_chain.py scripts/test_rint_r_chain.py > "$F14/code.diff"
{
  echo '# 바탕 = 379e85856 (rint_r_chain.py · test_rint_r_chain.py = 사전 공격 14 대상 7a582acf5 와 같은 blob f6ea60dbc · 098918e78 = 사전 공격 13 고친 판 바이트)'
  sha256sum "$H/base/rint_r_chain.py" | sed 's#  .*#  scripts/rint_r_chain.py  (바탕)#'
  sha256sum "$H/base/test_rint_r_chain.py" | sed 's#  .*#  scripts/test_rint_r_chain.py  (바탕)#'
  echo '# 고친 판 = 바탕 + code.diff = 이 커밋 · 시험 · 변이 · 탐침 다시 = 이 바이트'
  sha256sum scripts/rint_r_chain.py | sed 's#  .*#  scripts/rint_r_chain.py  (고친 판)#'
  sha256sum scripts/test_rint_r_chain.py | sed 's#  .*#  scripts/test_rint_r_chain.py  (고친 판)#'
} > "$F14/code_sha256.txt"
for f in pa14_before.log pa14_after.log pa14_rows_before.json pa14_rows_after.json pa14_rows_summary.log full_py311.log e2e_py311.log \
         check_kgy_py38.log e2e_py38_code_sha.txt mutation_run.log probe_rerun.log before_vs_preattack.log probe_diff.txt static_checks.log \
         tau_bound_check.log fn_lines.log int_digits_check.log mutation_equiv_run.log; do
  if [ -f "$H/logs/$f" ]; then cp "$H/logs/$f" "$F14/logs/$f"; else echo "없음 (아직): logs/$f"; fi
done
cp "$H/mut/mutation_results.json" "$F14/logs/mutation_results.json"
cp "$H/mut/mutation_equiv_results.json" "$F14/logs/mutation_equiv_results.json"
for f in "$H/logs/py38/"*.log; do [ -f "$f" ] && cp "$f" "$F14/logs/py38/"; done
cp "$H/probe_out/"*.out "$F14/probe_out/"
cp "$H/tools/"*.py "$H/tools/"*.sh "$F14/tools/"
ls -R "$P14" "$F14" | head -80

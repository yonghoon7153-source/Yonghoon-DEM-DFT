#!/bin/bash
# P14 — 요청서 §4 회귀 + 묶음 §4 단계 2 자체 시험 다섯 (이 컨테이너 · HEAD 깨끗한 트리) — 한 번에 하나 · BLAS 한 스레드 (heavy.sh 가 준다)
# 재실행: cd <worktree> && bash <SCRATCH>/heavy.sh bash p14_regress.sh <out_dir>
O=$1; mkdir -p "$O"
run() {  # 이름 · 명령
  n=$1; shift
  s=$(date +%s)
  "$@" > "$O/$n.log" 2>&1
  rc=$?
  echo "$n rc=$rc secs=$(( $(date +%s) - s )) :: $(tail -1 "$O/$n.log" | cut -c1-200)"
}
echo "HEAD=$(git rev-parse HEAD) dirty=$(git status --porcelain --untracked-files=no | wc -l) porcelain_all=$(git status --porcelain | wc -l)"
run reread_selftest python3 scripts/g2_network_reread.py --selftest
run receipt_selftest python3 scripts/supp20_input_receipt.py --selftest
run fast16 python3 scripts/wsl_network_smoke.py --selftest
run real4 python3 scripts/wsl_network_smoke.py --selftest-real
run runner_selftest python3 scripts/run_network_194_parallel.py --selftest
run check_doc_refs python3 scripts/check_doc_refs.py
run check_review_findings python3 scripts/check_review_findings.py
run check_method_discipline python3 scripts/check_method_discipline.py
echo "dirty after=$(git status --porcelain --untracked-files=no | wc -l) porcelain_all=$(git status --porcelain | wc -l)"
git status --porcelain | head -20

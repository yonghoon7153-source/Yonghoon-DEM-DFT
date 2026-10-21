#!/bin/bash
# P13 — 묶음 §4 단계 1 · 3 · 4 를 이 컨테이너에서 돌릴 수 있는 만큼 (등록 명령 그대로 · ROOT · 영수증 = 스크래치 · LHS 원 dump 없음 → 원자료 문제로 멈춤 = 기대)
# 재실행: cd <worktree> && bash <SCRATCH>/heavy.sh bash p13_preflight.sh <out_dir>
O=$1; mkdir -p "$O"
PY=python3
T=$(date +%m%d_%H%M%S)
R194="$O/net194_x"; RS="$O/netsupp20_x"
PF194="${R194}_preflight_${T}.json"; PFS="${RS}_preflight_${T}.json"
PIN=$(git rev-parse HEAD)
echo "PIN=$PIN dirty=$(git status --porcelain --untracked-files=no | wc -l)"
# 1. 보통 · 격리
$PY -c "import sys, numpy, scipy, networkx; print('보통', sys.version.split()[0], numpy.__version__, scipy.__version__, networkx.__version__, sys.executable)"
$PY -I -c "import sys, numpy, scipy, networkx; print('격리', sys.version.split()[0], numpy.__version__, scipy.__version__, networkx.__version__, sys.executable)"
# 3. 194
$PY scripts/run_network_194_parallel.py run --root "$R194" --dry-run --observe-imports --preflight-receipt "$PF194" > "$O/dry194.screen" 2>&1; echo "dry-run 194 rc=$?"
$PY scripts/run_network_194_parallel.py preflight-verify --receipt "$PF194" --expect-set production194 --approved-sha "$PIN" --json "${PF194%.json}_verify.json" > "$O/verify194.screen" 2>&1; echo "verify 194 rc=$?"
grep -E 'INPUT_DIGEST_JSON|코드 |기대 망 세대|전이 의존 닫힘|지연 import 분류|fork · 프로세스 풀 API|원자료 · 메시 문제|⛔' "${PF194%.json}.log" | cut -c1-400
# 4. 보충 20
$PY scripts/run_network_194_parallel.py run --root "$RS" --cohorts lhss --dry-run --observe-imports --preflight-receipt "$PFS" > "$O/drysupp.screen" 2>&1; echo "dry-run supp20 rc=$?"
$PY scripts/supp20_input_receipt.py --preflight-receipt "$PFS" --approved-sha "$PIN" --json "${PFS%.json}_receipt.json" > "$O/receipt.screen" 2>&1; echo "receipt rc=$?"
tail -1 "$O/receipt.screen"
grep -E '✗' "$O/receipt.screen" | cut -c1-300
grep -E '✗' "$O/verify194.screen" | cut -c1-300
ls -la "$R194" "$RS" 2>&1 | head -3
echo "dirty after=$(git status --porcelain --untracked-files=no | wc -l)"

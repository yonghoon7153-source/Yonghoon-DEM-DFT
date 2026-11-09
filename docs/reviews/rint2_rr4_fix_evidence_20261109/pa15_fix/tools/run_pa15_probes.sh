#!/usr/bin/env bash
# 사전 공격 15 탐침 무변경 재실행 — 쓰임: bash run_pa15_probes.sh <탐침 사본 뿌리 (그 아래 probes/ = 반입 preattack15/probes 와 같은 바이트 · out/ = 새 출력)> <코드 트리 (PA15_TREE)> <탐침 이름 …>
# 탐침 h.py 가 PA15_TREE 의 scripts 사슬 · 시험 모듈을 부른다 · 출력 JSON = <뿌리>/out/ (반입한 원 출력은 건드리지 않는다)
set -u
RUN=${1:?탐침 사본 뿌리}
export PA15_TREE=${2:?코드 트리}
shift 2
mkdir -p "$RUN/out"
cd "$RUN/probes" || exit 9
for p in "$@"; do
  echo "=== $p"
  timeout 900 python3 "$p.py" > "$RUN/out/$p.stdout" 2>&1
  echo "rc=$?"
done

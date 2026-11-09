#!/usr/bin/env bash
# 고침 C 시험 먼저 — 최종 시험 파일을 바탕 트리 사본 (69d714d09 와 scripts · webapp 같음 = tree_vs_commit) 에 넣고 부분집합 → 고친 작업 트리 부분집합 · 행 값 둘.
# 쓰임: bash tests_first.sh <작업 트리> <바탕 트리 사본> <로그 폴더> <도구 폴더>
set -u
WT=${1:?작업 트리}
BT=${2:?바탕 트리}
LG=${3:?로그}
TL=${4:?도구}
ONLY=RR3,PA13,PA14,RR4,RR5
mkdir -p "$LG"
cp "$WT/scripts/test_rint_r_chain.py" "$BT/scripts/test_rint_r_chain.py"
python3 "$TL/tree_vs_commit.py" "$WT" 69d714d09 "$BT" scripts/test_rint_r_chain.py > "$LG/base_tree_check.log" 2>&1
subset() {   # $1 = 트리 · $2 = 이름표 · $3 = 로그
  {
    echo "\$ ($2) python3 scripts/test_rint_r_chain.py --only $ONLY"
    (cd "$1" && sha256sum scripts/rint_r_chain.py scripts/test_rint_r_chain.py && python3 scripts/test_rint_r_chain.py --only "$ONLY"; echo "rc=$?")
  } > "$3" 2>&1
}
subset "$BT" '바탕 트리 사본 = 69d714d09 사슬 + 최종 시험' "$LG/tests_first_base.log"
python3 "$TL/rows_dump5.py" "$BT" - "$LG/rr5_rows_base.json" > "$LG/rr5_rows_base.log" 2>&1
subset "$WT" '고친 작업 트리' "$LG/after_subset.log"
python3 "$TL/rows_dump5.py" "$WT" - "$LG/rr5_rows_after.json" > "$LG/rr5_rows_after.log" 2>&1
tail -2 "$LG/tests_first_base.log"
tail -2 "$LG/after_subset.log"
cat "$LG/base_tree_check.log"
grep -E "^RR" "$LG/rr5_rows_base.log" "$LG/rr5_rows_after.log" | cut -c1-220

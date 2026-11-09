#!/bin/bash
# 정적 점검 (고친 판 두 코드 파일) — pyflakes · 미정의 이름 · kgy 판 3.8 py_compile · sha256.  쓰임: bash static_checks.sh <작업 트리> [python3.8 경로]
WT=${1:?작업 트리}
PY38=${2:-$(uv python find 3.8 2>/dev/null)}
cd "$WT" || exit 9
F="scripts/rint_r_chain.py scripts/test_rint_r_chain.py"
echo "\$ python3 -m pyflakes $F"
python3 -m pyflakes $F
echo "rc=$?"
echo "\$ python3 scripts/check_undefined_names.py $F"
python3 scripts/check_undefined_names.py $F
echo "rc=$?"
echo "\$ python3.8 (kgy 판) -m py_compile $F"
"$PY38" -m py_compile $F
echo "rc=$?"
sha256sum $F

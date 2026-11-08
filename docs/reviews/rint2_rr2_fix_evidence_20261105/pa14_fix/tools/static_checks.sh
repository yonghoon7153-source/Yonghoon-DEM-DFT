#!/bin/bash
# 정적 점검 (고친 판 두 코드 파일) — pyflakes · 미정의 이름 · kgy 판 3.8 py_compile · sha256
cd /home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a271b07eec3fe5332 || exit 9
PY38=/root/.local/share/uv/python/cpython-3.8-linux-x86_64-gnu/bin/python3.8
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

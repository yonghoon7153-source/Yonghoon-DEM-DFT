#!/bin/bash
# 바탕 두 코드 파일 + code.diff (patch -p1) = 고친 판 바이트인지 — 쓰임: bash apply_check.sh <바탕 파일 폴더 (rint_r_chain.py · test_rint_r_chain.py)> <code.diff> <작업 트리> <빈 작업 폴더>
set -u
BASE=$(realpath "${1:?바탕 폴더}"); DIFF=$(realpath "${2:?code.diff}"); WT=$(realpath "${3:?작업 트리}"); T=$(realpath -m "${4:?작업 폴더}")
rm -rf "$T" && mkdir -p "$T/scripts" || exit 9
cp "$BASE/rint_r_chain.py" "$BASE/test_rint_r_chain.py" "$T/scripts/"
echo "== 바탕"
(cd "$T" && sha256sum scripts/rint_r_chain.py scripts/test_rint_r_chain.py)
echo "== patch -p1 < code.diff"
(cd "$T" && patch -p1 --no-backup-if-mismatch < "$DIFF" > /dev/null; echo "rc=$?")
echo "== 바탕 + code.diff"
(cd "$T" && sha256sum scripts/rint_r_chain.py scripts/test_rint_r_chain.py)
echo "== 작업 트리 (고친 판)"
(cd "$WT" && sha256sum scripts/rint_r_chain.py scripts/test_rint_r_chain.py)
for f in rint_r_chain.py test_rint_r_chain.py; do
  if cmp -s "$T/scripts/$f" "$WT/scripts/$f"; then echo "같음 $f"; else echo "다름 $f"; fi
done

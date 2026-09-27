#!/usr/bin/env bash
# Reproduce CI P1 without Python or any calculation.
# bash repro_pack_ci.sh /path/to/db/inputs/wad_aprime_v5_vasp_2026_09_27
# Writes only under a new mktemp directory. No source files modified.
set -eu
src=$(cd "$1" && pwd)
tmp=$(mktemp -d)
trap 'rm -rf -- "$tmp"' EXIT
cp -R "$src/." "$tmp/"
mkdir -p "$tmp/run/REVIEW_DUMMY"
printf 'synthetic review output; not a VASP result\n' > "$tmp/run/REVIEW_DUMMY/OUTCAR"
printf 'synthetic review record\n' > "$tmp/run/REVIEW_DUMMY/attempt.json"
printf 'find(){ printf "REVIEW_FIND_FAILURE\\n" >&2; return 73; }\n' > "$tmp/fault.sh"
set +e
(cd "$tmp" && PACK_ONLY=1 BASH_ENV="$tmp/fault.sh" bash run_all.sh)
rc=$?
set -e
printf 'runner exit = %s (expected 4 on enumeration failure)\n' "$rc"
if [ -f "$tmp/V5_vasp_return.tgz" ]; then
  tar tzf "$tmp/V5_vasp_return.tgz"
fi
# Exit 1 on the reviewed bug, 0 when it is fixed.
test "$rc" -eq 4

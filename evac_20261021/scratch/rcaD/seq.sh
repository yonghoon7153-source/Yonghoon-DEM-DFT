#!/bin/bash
# usage: seq.sh <tag> "<logname> <args...>" ["<logname> <args...>" ...]  — runs each python job one after another (run1.sh)
R=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaD/run1.sh
tag="$1"; shift
for job in "$@"; do
  # shellcheck disable=SC2086
  set -- $job
  name="$1"; shift
  echo "== $name: $(bash "$R" "$name" "$@")"
done
echo "== $tag done"

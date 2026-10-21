#!/usr/bin/env bash
# Kit selftest logs at each 10-21 commit state (git archive mirror per commit) — fast suites only.
# Usage: bash states_batch.sh
set -u
S=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/ulpr_fix
for pair in "f1b911f76:st_tests_first" "55fff3eb1:st_ulpr01" "2932b63bc:st_ulpr0304" "c21b1a051:st_guard1"; do
  c=${pair%%:*}; name=${pair##*:}
  bash $S/mk_mirror.sh "$c" "$S/m_$name" > /dev/null
  echo "== $name ($c)"
  bash $S/run_mirror.sh "$S/m_$name" "$name" ul_lib ul_s3 ul_observers ul_gates ul_reader seal_check decks_check hist_decks_check
  rm -rf "$S/m_$name"
done

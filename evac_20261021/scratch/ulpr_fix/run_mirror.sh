#!/usr/bin/env bash
# Run kit selftests / checks on a MIRROR root (git archive copy) — counts ✓ / ✗ lines · rc · seconds.
# Usage: bash run_mirror.sh <mirror-root> <log-subdir> <name ...>   (names = run_st.sh)
set -u
ROOT=${1:?root}
KIT=$ROOT/docs/data/ps45_unload_20261009
S=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/ulpr_fix
OUT=$S/logs/${2:?subdir}
shift 2
mkdir -p "$OUT" "$S/tmp"
export TMPDIR=$S/tmp OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$ROOT" || exit 9
for spec in "$@"; do
  case "$spec" in
    ul_lib|ul_s3|ul_observers|ul_gates|ul_reader|ul_runner_test) cmd=(python3 -I -B "$KIT/$spec.py" --selftest) ;;
    seal_selftest) cmd=(python3 -I -B "$KIT/seal_kit.py" --selftest) ;;
    seal_check) cmd=(python3 -I -B "$KIT/seal_kit.py" --check) ;;
    decks_selftest) cmd=(python3 -I -B "$KIT/make_unload_decks.py" --selftest) ;;
    decks_check) cmd=(python3 -I -B "$KIT/make_unload_decks.py" --check) ;;
    hist_decks_selftest) cmd=(python3 -I -B "$KIT/history_test/make_history_decks.py" --selftest) ;;
    hist_decks_check) cmd=(python3 -I -B "$KIT/history_test/make_history_decks.py" --check) ;;
    hist_read_selftest) cmd=(python3 -I -B "$KIT/history_test/read_history.py" --selftest) ;;
    *) echo "unknown $spec"; continue ;;
  esac
  t0=$(date +%s.%N)
  "${cmd[@]}" > "$OUT/$spec.log" 2>&1
  rc=$?
  t1=$(date +%s.%N)
  ok=$(grep -c '^ *✓' "$OUT/$spec.log")
  bad=$(grep -c '^ *✗' "$OUT/$spec.log")
  echo "$spec rc=$rc ok=$ok fail=$bad secs=$(python3 -c "print(round($t1-$t0,1))") last=$(tail -1 "$OUT/$spec.log" | cut -c1-160)"
done

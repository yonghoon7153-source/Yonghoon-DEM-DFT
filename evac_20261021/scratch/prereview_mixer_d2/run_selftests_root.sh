#!/bin/bash
# recheck 10-21: selftests of the mixer tools under a given root (repo worktree or extracted snapshot)
# usage: bash run_selftests_root.sh <root> <logdir>
R="$1"; L="$2"
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_mixer_d2
mkdir -p "$L" "$H/tmp_launcher"
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 TMPDIR="$H/tmp_launcher"
cd "$H" || exit 9
for t in make_mixer_deck mixer_deck_readback mixer_deck_diff mixer_smoke_blind mixer_contact_reader; do
  s=$(date +%s)
  python3 -I -B "$R/scripts/$t.py" --selftest > "$L/$t.log" 2>&1
  rc=$?
  e=$(date +%s)
  np=$(grep -c "^  ✓\|^  PASS\|  ✓ " "$L/$t.log")
  nf=$(grep -c "^  ✗\|^  FAIL\|  ✗ " "$L/$t.log")
  echo "$t rc=$rc $((e - s))s pass_marks=$np fail_marks=$nf :: $(grep -E 'selftest[: ]' "$L/$t.log" | tail -1)"
done
s=$(date +%s)
bash "$R/dem_scripts/mixer_20260921/test_launcher.sh" > "$L/test_launcher.log" 2>&1
rc=$?
e=$(date +%s)
echo "test_launcher rc=$rc $((e - s))s :: $(tail -1 "$L/test_launcher.log")"

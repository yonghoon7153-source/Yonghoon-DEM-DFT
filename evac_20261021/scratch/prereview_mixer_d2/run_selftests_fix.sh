#!/bin/bash
# recheck 10-21: selftests of the fixed tools at 9412f384a (worktree W) — one after another; logs in selftests_fix/
W=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a876633abb3bfa519
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_mixer_d2
L="$H/selftests_fix"
mkdir -p "$L" "$H/tmp_launcher"
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 TMPDIR="$H/tmp_launcher"
cd "$H" || exit 9
for t in make_mixer_deck mixer_deck_readback mixer_deck_diff mixer_smoke_blind mixer_contact_reader; do
  s=$(date +%s)
  python3 -I -B "$W/scripts/$t.py" --selftest > "$L/$t.log" 2>&1
  rc=$?
  e=$(date +%s)
  echo "$t rc=$rc $((e - s))s :: $(grep -E 'selftest[: ]' "$L/$t.log" | tail -1)"
done
s=$(date +%s)
bash "$W/dem_scripts/mixer_20260921/test_launcher.sh" > "$L/test_launcher.log" 2>&1
rc=$?
e=$(date +%s)
echo "test_launcher rc=$rc $((e - s))s :: $(tail -1 "$L/test_launcher.log")"

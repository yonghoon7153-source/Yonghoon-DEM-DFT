#!/bin/bash
# recheck 10-21: --runs with a D2 cell name the generator refuses (rho 1e-5 -> gamma_W below range) — how does the diff tool end?
W=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a876633abb3bfa519
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_mixer_d2
T="$H/grammar_runs"
rm -rf "$T"; mkdir -p "$T/runs/GMuu_rho0p00001_bo0p5_lab20261014_ref_r2_s32452843" "$T/runs/GMcc_rho0p00001_bo0p5_lab20261014_ref_r2_s32452843"
cp "$H/decks/recheck/GMuu_ref20_lab/in.mixer" "$T/runs/GMuu_rho0p00001_bo0p5_lab20261014_ref_r2_s32452843/in.mixer"
cp "$H/decks/recheck/GMcc_ref20_lab/in.mixer" "$T/runs/GMcc_rho0p00001_bo0p5_lab20261014_ref_r2_s32452843/in.mixer"
export PYTHONDONTWRITEBYTECODE=1
python3 -I -B "$W/scripts/mixer_deck_diff.py" --runs "$T/runs" --ref-arm GMuu_rho0p00001_bo0p5_lab20261014_ref_r2 \
  --arm GMcc_rho0p00001_bo0p5_lab20261014_ref_r2 --allow GM --expect-seeds 32452843 > "$T/out.txt" 2>&1
echo "rc=$?"
grep -n "⛔\|Traceback\|SystemExit\|PASS\|지원 범위" "$T/out.txt" | cut -c1-220 | head -8
tail -2 "$T/out.txt" | cut -c1-220

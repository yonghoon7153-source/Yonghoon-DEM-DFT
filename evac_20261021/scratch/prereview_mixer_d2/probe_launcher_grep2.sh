#!/bin/bash
# recheck 10-21: resume_all.sh on a REAL D2 deck under a neutral name (header-grep branch), alone in OUT
W=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a876633abb3bfa519
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_mixer_d2
T="$H/launcher_probe2"
rm -rf "$T"; mkdir -p "$T/runs/X_s32452843/restart"
cp "$H/decks/recheck/GMuu_ref20_lab/in.mixer" "$T/runs/X_s32452843/in.mixer"
printf 'Step Atoms KinEng\n     100   100000 0.0\n' > "$T/runs/X_s32452843/log.lmp"
: > "$T/runs/X_s32452843/restart/mixer.1000.restart"
cd "$T" || exit 9
OUT="$T/runs" DRY=1 bash "$W/dem_scripts/mixer_20260921/resume_all.sh" > "$T/resume_all.out" 2>&1
echo "resume_all rc=$?"
cat "$T/resume_all.out" | head -20
ls "$T/runs/X_s32452843"

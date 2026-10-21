#!/bin/bash
# recheck 10-21: does run_all.sh / resume_all.sh skip a REAL D2 deck that sits under a non-GM cell name (header-grep branch)?
# The repo test (test_launcher.sh D2①) only puts a fake proto deck under GM* names — the grep branch is not exercised there.
W=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a876633abb3bfa519
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_mixer_d2
T="$H/launcher_probe"
rm -rf "$T"; mkdir -p "$T/runs"
FAKE="$T/lmp_fake"
printf '#!/usr/bin/env bash\necho $$ >> "%s/fake_pids"\nsleep 1\n' "$T" > "$FAKE"; chmod +x "$FAKE"
mkdir -p "$T/runs/X_s32452843" "$T/runs/Y_s32452843" "$T/runs/LCx_s32452843"
cp "$H/decks/recheck/GMuu_ref20_lab/in.mixer" "$T/runs/X_s32452843/in.mixer"          # real D2 deck, neutral name
cp "$H/decks/recheck/LC_soft_lab/in.mixer" "$T/runs/Y_s32452843/in.mixer"             # real old-arm deck (control: launched)
# D2 deck whose header line was edited (★ removed) — the grep needs the exact '★ D2 결합 규칙 (기하평균' string
sed 's/^# ★ D2 결합 규칙 (기하평균/# D2 결합 규칙 (기하평균/' "$H/decks/recheck/GMuu_ref20_lab/in.mixer" > "$T/runs/LCx_s32452843/in.mixer"
cd "$T" || exit 9
OUT="$T/runs" LMP="$FAKE" MAXJ=4 bash "$W/dem_scripts/mixer_20260921/run_all.sh" > "$T/run_all.out" 2>&1
echo "run_all rc=$?"
cat "$T/run_all.out"
sleep 2
for n in X_s32452843 Y_s32452843 LCx_s32452843; do
  if [ -f "$T/runs/$n/pid" ]; then echo "LAUNCHED: $n"; else echo "not launched: $n"; fi
done
# resume_all.sh: give X a log + restart file so it would be a resume candidate
mkdir -p "$T/runs/X_s32452843/restart"
printf 'Step Atoms\n 100 100000\n' > "$T/runs/X_s32452843/log.lmp"
: > "$T/runs/X_s32452843/restart/mixer.1000.restart"
OUT="$T/runs" DRY=1 bash "$W/dem_scripts/mixer_20260921/resume_all.sh" > "$T/resume_all.out" 2>&1
echo "resume_all rc=$?"
grep -n "X_s32452843\|LCx_s32452843\|D2" "$T/resume_all.out" | head -10

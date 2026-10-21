#!/bin/bash
# recheck 10-21: fixed readback / diff on D2 decks at other CGFs (100 · 200 · 300 k atoms at CGF 120) — false refusals?
W=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a876633abb3bfa519
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_mixer_d2
G="$H/gen/mmd_FIX.py"
O="$H/decks/cgf"
rm -rf "$O"; mkdir -p "$O"
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1
for cg in 100 200 123.456; do
  for st in uu cc; do
    if [ $st = uu ]; then g='AM_P=0.3,AM_S=0.3'; else g='AM_P=1,AM_S=1'; fi
    python3 -I -B "$G" --out "$O/${st}_$cg" --n-total 100000 --cgf $cg --seed 32452843 --revolutions 2 --dens-gen lab20261014 \
      --gm-gamma $g --gm-wall-ncm 0.3 --gm-bo-se 0.5 --stiffen-se 20 --hold-bo-pairwise > "$O/${st}_$cg.log" 2>&1
    echo "gen $st cgf $cg rc=$?"
  done
  python3 -I -B "$W/scripts/mixer_deck_readback.py" --table GM "$O/uu_$cg/in.mixer" "$O/cc_$cg/in.mixer" > "$O/rb_$cg.log" 2>&1
  echo "readback GM cgf $cg rc=$? :: $(tail -1 "$O/rb_$cg.log")"
  python3 -I -B "$W/scripts/mixer_deck_diff.py" "$O/uu_$cg/in.mixer" "$O/cc_$cg/in.mixer" --allow GM > "$O/df_$cg.log" 2>&1
  echo "diff GM cgf $cg rc=$? :: $(tail -1 "$O/df_$cg.log")"
done

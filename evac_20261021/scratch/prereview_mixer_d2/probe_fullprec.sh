#!/bin/bash
# recheck 10-21: D2 decks with --dump-full-precision and --dt-factor 0.5 through the fixed readback / diff (no false refusal?)
W=/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a876633abb3bfa519
H=/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/prereview_mixer_d2
G="$H/gen/mmd_FIX.py"
O="$H/decks/fullprec"
rm -rf "$O"; mkdir -p "$O"
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1
B="--n-total 100000 --cgf 151.4 --seed 32452843 --revolutions 2 --dens-gen lab20261014 --gm-wall-ncm 0.3 --gm-bo-se 0.5"
python3 -I -B "$G" --out "$O/uu" $B --gm-gamma AM_P=0.3,AM_S=0.3 --stiffen-se 20 --hold-bo-pairwise --dt-factor 0.5 --dump-full-precision > "$O/uu.log" 2>&1; echo "gen uu rc=$?"
python3 -I -B "$G" --out "$O/cc" $B --gm-gamma AM_P=1,AM_S=1 --stiffen-se 20 --hold-bo-pairwise --dt-factor 0.5 --dump-full-precision > "$O/cc.log" 2>&1; echo "gen cc rc=$?"
python3 -I -B "$G" --out "$O/uu_ref" $B --gm-gamma AM_P=0.3,AM_S=0.3 --stiffen-se 20 --hold-bo-pairwise --dump-full-precision > "$O/uu_ref.log" 2>&1; echo "gen uu_ref rc=$?"
python3 -I -B "$W/scripts/mixer_deck_readback.py" --table GM "$O/uu/in.mixer" "$O/cc/in.mixer" --table DT "$O/uu_ref/in.mixer" "$O/uu/in.mixer" > "$O/rb.out" 2>&1
echo "readback GM + DT rc=$? :: $(grep -E '^── 표' "$O/rb.out" | tr '\n' ' ') $(tail -1 "$O/rb.out")"
python3 -I -B "$W/scripts/mixer_deck_diff.py" "$O/uu/in.mixer" "$O/cc/in.mixer" --allow GM > "$O/df.out" 2>&1
echo "diff GM rc=$? :: $(tail -1 "$O/df.out")"
grep -c "dump_modify" "$O/uu/in.mixer"

#!/usr/bin/env bash
# Re-calibrate the 3D plastic DEM for the CURRENT protocol (strain-control +
# sustained-pressure + damp=6), in two stages:
#   (1) beta_lock so pure-SE -> Minnmann porosity_SPHERE ~10% @ 0.3 GPa
#   (2) AM softening e_am so the bimodal AM75 bed densifies to ~15%
#       (the LIGGGHTS / experiment anchor) instead of the rigid-AM 55% artifact
# Then use the chosen (beta, e_am) for the cap-ON vs cap-OFF dip sweep.
#
# Run in tmux (SSH-drop safe):  tmux new -s cal ; bash scripts/dem3d_calib.sh
set -uo pipefail
cd "$(dirname "$0")/.."
ARCH=${ARCH:-cuda}

echo "================ (1) beta re-cal : pure-SE -> ~10% ================"
for b in 0.34 0.40 0.46 0.54; do
  r=$(python3 scripts/dem3d_plastic.py --material SE --n-target 2500 --plastic \
        --beta-lock "$b" --frames 400 --arch "$ARCH" --quiet 2>/dev/null | grep '^FINAL')
  echo "beta=$b   $r"
done

echo "================ (2) AM softening : AM75 -> ~15% (beta=${BETA:-0.46}) ================"
BETA=${BETA:-0.46}
for eam in 140 20 8 3; do
  r=$(python3 scripts/dem3d_plastic.py --material mix --am-wt 75 --n-target 20000 \
        --plastic --beta-lock "$BETA" --e-am "$eam" --frames 600 --arch "$ARCH" --quiet 2>/dev/null \
        | grep -E '^FINAL|bottomed')
  echo "e_am=$eam   $r"
done
echo "================ done ================"
echo "pick beta where pure-SE~10%, e_am where AM75~15%; then the dip sweep:"
echo "  BETA=<b> EAM=<e> ... (dip_sweep.sh will take --e-am once wired)"

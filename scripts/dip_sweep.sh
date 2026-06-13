#!/usr/bin/env bash
# Furnas-dip verdict sweep: 12:4:1 bimodal, AM% sweep, plastic (cap ON) vs rigid (cap OFF).
#
# Run inside tmux so an SSH drop never kills it:
#   tmux new -s dip
#   bash scripts/dip_sweep.sh
#   # detach: Ctrl-b then d   |   reattach later: tmux attach -t dip
#
# Overridable knobs (env): N (particles), BETA (lock = Minnmann calib), FRAMES, ARCH, AMS.
#   N=20000 bash scripts/dip_sweep.sh      # fast first pass (~40-60 min, clear dip shape)
#   N=50000 bash scripts/dip_sweep.sh      # confirmation (~4 h)
# Writes dip_sweep.log (full) + dip_results.csv (parsed → plot).
set -uo pipefail
cd "$(dirname "$0")/.."

N=${N:-20000}; BETA=${BETA:-0.46}; EAM=${EAM:-8}; FRAMES=${FRAMES:-600}; ARCH=${ARCH:-cuda}
AMS=${AMS:-"55 65 75 85 95"}
LOG=dip_sweep.log; CSV=dip_results.csv

echo "am,mode,p_gpa,por_sphere,por_vox,n_big,overflow" > "$CSV"
echo "== dip sweep  N=$N  beta=$BETA  e_am=$EAM  frames=$FRAMES  arch=$ARCH  $(date) ==" | tee "$LOG"

for am in $AMS; do
  for mode in plastic rigid; do
    tag="AM${am}_${mode}"
    echo "=== $tag ===" | tee -a "$LOG"
    out=$(python3 scripts/dem3d_plastic.py --material mix --am-wt "$am" --n-target "$N" \
          --"$mode" --beta-lock "$BETA" --e-am "$EAM" --frames "$FRAMES" --arch "$ARCH" 2>&1)
    echo "$out" >> "$LOG"
    echo "$out" | grep -E "^3D DEM|^FINAL|platen bottomed|cell-list overflow"
    p=$(echo  "$out" | grep '^FINAL' | grep -oP 'pressure=\K[0-9.]+')
    ps=$(echo "$out" | grep '^FINAL' | grep -oP 'porosity_SPHERE=\K[-0-9.]+')
    pv=$(echo "$out" | grep '^FINAL' | grep -oP 'porosity_VOX=\K[-0-9.]+')
    nb=$(echo "$out" | grep -oP 'n_big=\K[0-9]+' | head -1)
    ov=$(echo "$out" | grep -c "cell-list overflow")
    echo "$am,$mode,${p:-NA},${ps:-NA},${pv:-NA},${nb:-NA},$ov" >> "$CSV"
  done
done
echo "== done $(date) ==" | tee -a "$LOG"
echo "results -> $CSV  (paste it here; overflow!=0 means raise M and rerun)"

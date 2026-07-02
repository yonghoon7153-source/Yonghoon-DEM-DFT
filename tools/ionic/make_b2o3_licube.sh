#!/usr/bin/env bash
# b2o3 Li-density cube for VESTA.
# The Arrhenius MD (run_b2o3_md.sh) runs WITHOUT --save_traj, so no frames were
# kept. This re-runs 600 K only WITH --save_traj, then builds the Li probability-
# density .cube (framework + Li cloud) via tools/ionic/li_density_cube.py.
# Complements the static BVSE channel cube with the DYNAMIC Li occupancy.
#
# Run on gabia/KISTI in the UMA conda env, inside tmux/screen (MD ~10-20 min GPU):
#   conda activate uma && bash tools/ionic/make_b2o3_licube.sh [OUT_ROOT] [DEVICE]
set -euo pipefail; set +H
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO"
OUT="${1:-runs/b2o3_licube}"; DEV="${2:-cuda}"
XYZ="db/structures/b2o3_relaxV0.xyz"
unset LD_LIBRARY_PATH OPAL_PREFIX 2>/dev/null || true   # QE env leftovers poison torch
test -f "$XYZ" || { echo "MISSING $XYZ — git pull on gabia first"; exit 1; }
mkdir -p "$OUT"

# reuse any existing 600 K production trajectory before spending GPU time
TRAJ="$(find "$OUT" runs -name traj.xyz -path '*T600*' 2>/dev/null | head -1 || true)"
if [ -z "$TRAJ" ]; then
  echo ">> 600 K MD (+traj) $(date +%H:%M:%S)  — equilib 5 ps + prod 50 ps"
  python3 tools/modelc_v3/disorder_ensemble_diffusion.py \
    --v0_xyz "$XYZ" --label b2o3 --out_root "$OUT" \
    --disorder_levels 0.0 --n_configs 1 \
    --temperatures 600 --equilib_ps 5 --prod_ps 50 --save_traj --device "$DEV"
  TRAJ="$(find "$OUT" -name traj.xyz -path '*T600*' | head -1)"
fi
[ -n "$TRAJ" ] || { echo "no traj.xyz produced"; exit 1; }
echo ">> traj: $TRAJ"

python3 tools/ionic/li_density_cube.py --traj "$TRAJ" \
  --out b2o3_T600_Li.cube --skip 100 --spacing 0.2 --sigma_A 0.4
echo ">> DONE -> b2o3_T600_Li.cube"
echo "   scp to local, open in VESTA; isolevel ~0.3-0.6x max (script printed a value)."

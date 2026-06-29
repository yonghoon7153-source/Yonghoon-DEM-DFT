#!/usr/bin/env bash
# UMA-MLIP Arrhenius MD for the B2O3-doped champion (b2o3_relaxV0).
# Ordered champion only (disorder_levels=0.0, 1 config) -> Ea, D0, D(300K), sigma.
# Venue-agnostic: works on gabia or KISTI. ACTIVATE the UMA conda env FIRST
# (e.g. `conda activate uma`), then run this. Launches DETACHED so it survives
# an SSH broken pipe; tail the log to watch.
#
#   bash tools/modelc_v3/run_b2o3_md.sh [OUT_ROOT] [DEVICE]
#     OUT_ROOT  default: runs/b2o3_md   DEVICE  default: cuda
set -euo pipefail
set +H
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO"
OUT_ROOT="${1:-runs/b2o3_md}"
DEVICE="${2:-cuda}"
XYZ="db/structures/b2o3_relaxV0.xyz"
LOG="$OUT_ROOT/b2o3_md.log"
mkdir -p "$OUT_ROOT"

# MPI/conda hygiene that bit us before (QE leftovers can poison the python env)
unset LD_LIBRARY_PATH OPAL_PREFIX 2>/dev/null || true

echo "repo=$REPO  xyz=$XYZ  out=$OUT_ROOT  device=$DEVICE  python=$(command -v python3)"
test -f "$XYZ" || { echo "MISSING $XYZ — run from a clean git pull"; exit 1; }

setsid bash -c "
  cd '$REPO'
  python3 tools/modelc_v3/disorder_ensemble_diffusion.py \
    --v0_xyz '$XYZ' --label b2o3 --out_root '$OUT_ROOT' \
    --disorder_levels 0.0 --n_configs 1 \
    --temperatures 600 800 1000 --equilib_ps 5 --prod_ps 50 \
    --device '$DEVICE'
" < /dev/null > "$LOG" 2>&1 &
PID=$!
echo "launched PID=$PID  log=$LOG"
echo "watch:  tail -f $LOG    |  result: $OUT_ROOT/ensemble_results.json"

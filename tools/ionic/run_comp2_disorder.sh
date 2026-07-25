#!/usr/bin/env bash
# =============================================================================
# comp2 (Li6PS5Cl0.5Br0.5) ANION-DISORDER ensemble MD
# -- HYPOTHESIS TEST: does Cl/Br <-> S2- site disorder lower Ea toward the
#    experimental Br conductivity gain (Kraft 2018)? Our v3 champion is the
#    ORDERED ground state (halides on 4a-FCC, free-S2- on 4c-FCC, ZERO mixing)
#    -> gave Ea 0.276 (>= comp1 0.253). Disorder should flatten the landscape.
#
# Driver = disorder_ensemble_diffusion.py (PATCHED 2026-07-25 to swap Cl AND Br
# with free-S2-, verified: composition conserved). Anti-site labels swapped at
# FIXED champion positions; UMA relaxes locally during the 5 ps equilib.
#
# Protocol MIRRORS run_comp2_md.sh (UMA-s-1p1 omat, dt 2 fs, friction 0.02,
# equilib 5 ps, 2-50 ps D window, 600/800/1000 K). d=0 ordered baseline already
# in comp2_md/ -> here we add the disordered levels.
#
# gabia (A6000) or kgy (RTX3090), uma env. GPU-share guard built in.
#   cd ~/Yonghoon-DEM-DFT && git pull
#   PY=$(which python3)   # (uma) shell
#   tmux new -s c2dis -d "PY=$PY bash tools/ionic/run_comp2_disorder.sh > ~/work/comp2_disorder.log 2>&1"
#
# COST (A6000, ~1 h / 205 ps run):
#   default LEVELS='0.5 1.0' NCONF=3 -> (3+3) cfg x 3 T = 18 runs ~= 1.5-2 days
#   trim:   NCONF=2                  -> 12 runs ~= 1.3 days
#           LEVELS='0.5'            ->  9 runs ~= 1 day (minimal: ordered vs d=0.5)
# =============================================================================
set -euo pipefail; set +H
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO"
unset LD_LIBRARY_PATH OPAL_PREFIX 2>/dev/null || true   # QE env leak pollutes torch
V0XYZ=${V0XYZ:-$REPO/db/structures/comp2_V0_v3_candidate.xyz}
OUTROOT=${OUTROOT:-$HOME/work/runs/comp2_disorder}
DEVICE=${DEVICE:-cuda}
PY=${PY:-python3}
LEVELS=${LEVELS:-0.5 1.0}
NCONF=${NCONF:-3}
PRODPS=${PRODPS:-200}
DRIVER=$REPO/tools/modelc_v3/disorder_ensemble_diffusion.py
test -f "$V0XYZ" || { echo "MISSING $V0XYZ -- git pull first"; exit 1; }

# dup-run guard
if pgrep -f "run_comp2_disorder|comp2_disorder" | grep -qv $$ 2>/dev/null; then
  echo "[guard] comp2_disorder already running — abort"; exit 0
fi

# GPU-share wait (skip with SKIP_WAIT=1 after nvidia-smi shows GPU free + only CPU pw.x)
while [ "${SKIP_WAIT:-0}" != 1 ] && pgrep -f 'pw\.x|neb\.x|comp_phonon_uma' >/dev/null 2>&1; do
  echo "[$(date +%H:%M:%S)] GPU busy (pw.x/neb.x/phonon) — recheck 5 min (SKIP_WAIT=1 if GPU free)"; sleep 300
done
echo "[$(date +%H:%M:%S)] GPU free — comp2 disorder ensemble start (LEVELS='$LEVELS' NCONF=$NCONF PROD=${PRODPS}ps)"
mkdir -p "$OUTROOT"

$PY "$DRIVER" \
  --v0_xyz "$V0XYZ" --label comp2_disorder \
  --out_root "$OUTROOT" \
  --disorder_levels $LEVELS --n_configs "$NCONF" \
  --temperatures 600 800 1000 \
  --equilib_ps 5 --prod_ps "$PRODPS" \
  --timestep_fs 2.0 --friction 0.02 \
  --save_fs 100 --fit_window_ps 2 50 \
  --seed 7 \
  --uma_model uma-s-1p1 --uma_task omat --device "$DEVICE"

echo ""; echo "===== DONE. ensemble_results.json per level in $OUTROOT ====="
grep -a "Ea = " "$OUTROOT"/ensemble_results.json 2>/dev/null || true
echo "회수: db/properties/comp2_md_arrhenius.json 의 ordered Ea 0.276 와 비교 (disorder가 낮추면 가설 확증)"

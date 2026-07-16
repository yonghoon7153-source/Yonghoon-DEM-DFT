#!/usr/bin/env bash
# =============================================================================
# LPSOCl (O-doped LPSCl1.6, 62-atom V0) MD conductivity suite
# -- EXACT mirror of the July b2o3/modelc protocol (md_conductivity_protocol):
#    UMA-s-1p1 (omat), Langevin NVT, dt 2 fs, friction 0.02, equilib 5 ps,
#    prod 200 ps, save_fs 100, MSD window 2-50 ps, 3-pt Arrhenius 600/800/1000 K
#    (400/500 K excluded per 2026-07-02 lowT verdict), 600 K reseed x3 for the
#    Ea error bar, + 600 K traj rerun for the Li-density cube (VESTA iso ~0.35).
#
# Run on gabia (A6000) in the UMA conda env inside tmux:
#   cd ~/Yonghoon-DEM-DFT && git pull
#   conda activate uma && tmux new -s lpsocl_md
#   bash tools/ionic/run_lpsocl_md.sh            # all stages
#   bash tools/ionic/run_lpsocl_md.sh ladder     # or one stage: ladder|reseed|licube
# Cost on A6000: ladder ~4-6 h, reseed ~4-5 h, licube ~30 min.
# n_Li = 2.2416e22 cm-3 (27 Li / 1204.52 A^3) -- for the Nernst-Einstein step.
# =============================================================================
set -euo pipefail; set +H
REPO="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$REPO"
unset LD_LIBRARY_PATH OPAL_PREFIX 2>/dev/null || true   # QE env leftovers poison torch
V0XYZ=$REPO/db/structures/lpsocl_relaxV0.xyz
OUTROOT=${OUTROOT:-$HOME/work/runs/lpsocl_md}
DEVICE=${DEVICE:-cuda}
DRIVER=$REPO/tools/modelc_v3/disorder_ensemble_diffusion.py
STAGE=${1:-all}
test -f "$V0XYZ" || { echo "MISSING $V0XYZ -- git pull first"; exit 1; }
mkdir -p "$OUTROOT"

if [ "$STAGE" = all ] || [ "$STAGE" = ladder ]; then
  echo "===== [1/3] Arrhenius ladder 600/800/1000 K (prod 200 ps each) ====="
  python3 "$DRIVER" \
    --v0_xyz "$V0XYZ" --label lpsocl \
    --out_root "$OUTROOT/ladder" \
    --disorder_levels 0.0 --n_configs 1 \
    --temperatures 600 800 1000 \
    --equilib_ps 5 --prod_ps 200 \
    --timestep_fs 2.0 --friction 0.02 \
    --save_fs 100 --fit_window_ps 2 50 \
    --uma_model uma-s-1p1 --uma_task omat --device "$DEVICE"
fi

if [ "$STAGE" = all ] || [ "$STAGE" = reseed ]; then
  echo "===== [2/3] 600 K reseed x3 (Ea error bar, b2o3-symmetric) ====="
  for S in 2 3 4; do
    python3 "$DRIVER" \
      --v0_xyz "$V0XYZ" --label lpsocl \
      --out_root "$OUTROOT/reseed/s${S}" \
      --disorder_levels 0.0 --n_configs 1 \
      --temperatures 600 \
      --equilib_ps 5 --prod_ps 200 \
      --timestep_fs 2.0 --friction 0.02 \
      --save_fs 100 --fit_window_ps 2 50 \
      --seed ${S} \
      --uma_model uma-s-1p1 --uma_task omat --device "$DEVICE"
  done
fi

if [ "$STAGE" = all ] || [ "$STAGE" = licube ]; then
  echo "===== [3/3] 600 K traj rerun -> Li probability-density cube ====="
  python3 "$DRIVER" \
    --v0_xyz "$V0XYZ" --label lpsocl \
    --out_root "$OUTROOT/licube" \
    --disorder_levels 0.0 --n_configs 1 \
    --temperatures 600 --equilib_ps 5 --prod_ps 50 --save_traj \
    --timestep_fs 2.0 --friction 0.02 --save_fs 100 \
    --uma_model uma-s-1p1 --uma_task omat --device "$DEVICE"
  TRAJ="$(find "$OUTROOT/licube" -name traj.xyz -path '*T600*' | head -1)"
  [ -n "$TRAJ" ] || { echo "no traj.xyz produced"; exit 1; }
  python3 tools/ionic/li_density_cube.py --traj "$TRAJ" \
    --out "$OUTROOT/lpsocl_T600_Li.cube" --skip 50 --spacing 0.2 --sigma_A 0.4
  echo "cube: $OUTROOT/lpsocl_T600_Li.cube  (VESTA isosurface ~0.35 of max)"
fi

echo ""
echo "===== collect D values ====="
python3 - "$OUTROOT" <<'PY'
import json, os, sys
root = sys.argv[1]
p = os.path.join(root, "ladder", "ensemble_results.json")
if os.path.exists(p):
    j = json.load(open(p))
    cfg = j["levels"][0]["configs"][0]
    print("ladder D_per_T (600/800/1000):", ["%.4e" % d for d in cfg["D_per_T"]])
for s in (2, 3, 4):
    p = os.path.join(root, "reseed", f"s{s}", "ensemble_results.json")
    if os.path.exists(p):
        j = json.load(open(p))
        print(f"reseed s{s}: D_600 = {j['levels'][0]['configs'][0]['D_per_T'][0]:.4e}")
PY
echo ""
echo "NEXT: paste the D values back -- I fold in modelc/b2o3 anchors (same 2-50 ps"
echo "      window) -> Ea + error bar, sigma300 ratio, D0 decomposition, figures."

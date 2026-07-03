#!/usr/bin/env bash
# =============================================================================
# modelc (LPSCl1.6) 600 K  3-seed reseed  -- MIRRORS the b2o3_600_reseed protocol
# so the b2o3-vs-LPSCl1.6 Ea comparison gets a SYMMETRIC error bar.
#
# WHY: b2o3 is already 3-seeded (Ea = 0.206 +0.038/-0.030). LPSCl1.6 is still a
# single-seed 0.2235 with no bar -> the "equal Ea" claim compares a distribution
# to a point. LPSCl1.6's 600 K is equally single-seed / equally noisy (~24% D
# spread) so its Ea is equally fragile. Reseeding 600 K x3 closes that.
#
# WHAT: only 600 K is reseeded (it is the dominant Ea-noise driver, per the
# leave-one-out diagnosis). 800/1000 K reuse the deck-validated single-seed
# anchor (D_800 = 2.054e-05, D_1000 = 4.554e-05) -- do NOT rerun them.
#
# Run on gabia (GPU). Fixed params match md_conductivity_protocol.md: (2,50) ps
# window, UMA-s-1p1 omat, Langevin NVT, dt 2 fs, equilib 5 ps.
# =============================================================================
set -euo pipefail

# ---- EDIT to your gabia paths -----------------------------------------------
# Use the SAME modelc V0 (structure + cell) your deck-validated 600 K run used --
# the one that gives D_600 ~ 0.79e-5. If unsure, check the --v0_xyz in your
# original gabia modelc conductivity run dir. The 3-seed mean should bracket
# ~0.79e-5; if it is wildly off you have the wrong structure/cell.
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}
V0XYZ=${V0XYZ:-$REPO/db/structures/modelc_2x_V0.xyz}   # <-- CONFIRM this matches the deck run
OUTROOT=${OUTROOT:-$HOME/work/runs/modelc_600_reseed}
# -----------------------------------------------------------------------------

DRIVER=$REPO/tools/modelc_v3/disorder_ensemble_diffusion.py

echo "V0    = $V0XYZ"
echo "OUT   = $OUTROOT"
echo "seeds = 2 3 4  (MD seed = base+600 -> 602/603/604; same struct, diff velocities)"
echo ""

for S in 2 3 4; do
  echo "===================== modelc 600K reseed  s${S} ====================="
  python3 "$DRIVER" \
    --v0_xyz "$V0XYZ" --label modelc \
    --out_root "$OUTROOT/s${S}" \
    --disorder_levels 0.0 --n_configs 1 \
    --temperatures 600 \
    --equilib_ps 5 --prod_ps 200 \
    --timestep_fs 2.0 --friction 0.02 \
    --save_fs 100 --fit_window_ps 2 50 \
    --seed ${S} \
    --uma_model uma-s-1p1 --uma_task omat --device cuda
done

echo ""
echo "===================== collect D_600 ====================="
python3 - "$OUTROOT" <<'PY'
import json, sys, os, statistics as st
root = sys.argv[1]; vals = []
for s in (2, 3, 4):
    p = os.path.join(root, f"s{s}", "ensemble_results.json")
    try:
        j = json.load(open(p))
        D = j["levels"][0]["configs"][0]["D_per_T"][0]
        vals.append(D); print(f"  s{s}: D_600 = {D:.4e} cm2/s")
    except Exception as e:
        print(f"  s{s}: NOT FOUND ({e}) -- check {p} or s{s}/d0.00_cfg0/T600/msd.json")
if len(vals) == 3:
    m = sum(vals)/3; sd = st.pstdev(vals)
    print(f"\n  mean D_600 = {m:.4e} +/- {sd:.2e}  ({sd/m*100:.0f}% spread)")
    print("  (deck single-seed reference D_600 ~ 0.79e-5)")
PY

echo ""
echo "NEXT: paste me the 3 D_600 values (or the CSV). I combine each with the deck"
echo "      800/1000K (2.054e-5 / 4.554e-5) -> per-seed Ea/sigma + mean+-std,"
echo "      exactly like the b2o3 table, then rebuild the SYMMETRIC error-bar CSV/fig."

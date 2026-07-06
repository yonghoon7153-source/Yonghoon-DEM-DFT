#!/usr/bin/env bash
# =============================================================================
# Anode-interface decomposition CAMPAIGN — publication-grade, caveat-hardened.
#
# Addresses the 3 caveats of the single-seed screen:
#  (1) statistics  -> 3 seeds per system + 100 ps (convergence)
#  (2) termination -> CONTROLLED comparison: b2o3 (128, doped) vs modelc_2x
#      (124, the SAME 2x frame b2o3 was doped FROM) -> isolates the B2O3 effect
#      (same surface). modelc_62 (1x) added as a termination cross-check.
#  (3) MLIP trust  -> DFT validation is a separate step (extract_snapshots_for_dft.py).
#
# NOTE on cells: for the INTERFACE contrast the correct undoped control is
# modelc_2x (same framework as b2o3), NOT modelc_62. (modelc_62 is the right
# BULK-conductivity cell; here we want same-surface, isolate-the-dopant.)
#
# 3 systems x 3 seeds x 100 ps.  Run on kgy (UMA works). ~9-12 h.
# =============================================================================
set -euo pipefail
REPO=${REPO:-$HOME/work/Yonghoon-DEM-DFT}
OUTROOT=${OUTROOT:-$HOME/work/runs/interface_campaign}
DEVICE=${DEVICE:-cuda}
T=${T:-600}; PROD=${PROD:-100}; EQ=${EQ:-3}
SEEDS=${SEEDS:-"2 3 4"}
cd "$REPO"; mkdir -p "$OUTROOT"

# system : structure   (b2o3 doped ; modelc2x = SAME undoped frame = control ; modelc62 = termination cross-check)
SYS=(
  "b2o3:db/structures/b2o3_relaxV0.xyz"
  "modelc2x:db/structures/modelc_2x_V0.xyz"
  "modelc62:db/structures/modelc_V0_k663.xyz"
)

for entry in "${SYS[@]}"; do
  LBL="${entry%%:*}"; XYZ="${entry#*:}"
  echo "############### BUILD $LBL ($XYZ) ###############"
  python3 tools/oxidation/build_li_interface.py --electrolyte "$XYZ" --label "$LBL" \
    --out "$OUTROOT/interface_${LBL}_Li.xyz"
  for S in $SEEDS; do
    echo "===== MD $LBL seed $S ====="
    ( cd "$OUTROOT" && python3 "$REPO/tools/oxidation/run_li_interface_md.py" \
        --interface "interface_${LBL}_Li.xyz" --label "${LBL}_s${S}" \
        --seed "$S" --temperature "$T" --equilib_ps "$EQ" --prod_ps "$PROD" \
        --dt_fs 1.0 --device "$DEVICE" )
    echo "===== ANALYZE $LBL seed $S ====="
    python3 tools/oxidation/analyze_interface_decomp.py "$OUTROOT/${LBL}_s${S}_traj.xyz" \
      --label "${LBL}_s${S}" --dt_ps 0.2 \
      --out "$REPO/db/properties/interface_decomp_${LBL}_s${S}.csv"
  done
done

echo ""; echo "############### AGGREGATE (mean +/- std over seeds) ###############"
python3 tools/oxidation/aggregate_interface_campaign.py "$REPO/db/properties" "$SEEDS" \
  --out "$REPO/db/properties/interface_campaign_summary.csv" || \
  echo "(aggregate script optional; paste the per-seed summaries and I'll do it)"
echo ">> CAMPAIGN DONE"

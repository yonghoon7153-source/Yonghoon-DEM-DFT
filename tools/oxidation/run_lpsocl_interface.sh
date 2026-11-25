#!/usr/bin/env bash
# =============================================================================
# run_lpsocl_interface.sh — LPSOCl | Li-metal interface decomposition (kgy UMA).
#
# Controlled O-doping contrast: lpsocl (62 at, ONE S->O = POS3 unit) vs modelc62
# (62 at, the SAME 1x frame it was doped from). Isolates the single O substitution
# on the Li-metal reactive interface. Protocol BYTE-IDENTICAL to the 2026-07-07
# b2o3 campaign (run_interface_campaign.sh): UMA-s-1p1, 3 seeds x 100 ps, 600 K
# Langevin NVT, dt 1 fs, bottom-6A frozen.
#
# CONTROL: modelc62 was already run in the b2o3 campaign (interface_campaign_summary
# .csv: PS_loss 48.1+/-7.8%, dP_Li 3.27, dS_Li 1.97, dLi_pen 10.3). Same 1x frame,
# same protocol -> reuse as the anchor. (1x slab absolute decomposition is thin-slab
# inflated ~1.9x vs 2x, but the lpsocl/modelc62 RATIO is clean -- both same frame.)
# Set FRESH_CONTROL=1 to also re-run modelc62 in THIS session (belt-and-suspenders).
#
# The analyzer now tracks the O fingerprint (P-O = POS3 intact, O-Li = O reduced to
# Li2O) added 2026-07-18 -- the question O doping poses at the anode.
#
#   cd ~/Yonghoon-DEM-DFT && git pull && conda activate uma
#   tmux new -s lpsocl_iface -d 'bash tools/oxidation/run_lpsocl_interface.sh > ~/work/runs/lpsocl_iface.log 2>&1'
# ~3-4 h (lpsocl only) or ~6-7 h (with FRESH_CONTROL=1).
# =============================================================================
set -euo pipefail; set +H
REPO=${REPO:-$HOME/Yonghoon-DEM-DFT}; [ -d "$REPO" ] || REPO=$HOME/work/Yonghoon-DEM-DFT
OUTROOT=${OUTROOT:-$HOME/work/runs/lpsocl_iface}
DEVICE=${DEVICE:-cuda}
T=${T:-600}; PROD=${PROD:-100}; EQ=${EQ:-3}
SEEDS=${SEEDS:-"2 3 4"}
FRESH_CONTROL=${FRESH_CONTROL:-0}
cd "$REPO"; mkdir -p "$OUTROOT"

SYS=("lpsocl:db/structures/lpsocl_relaxV0.xyz")
[ "$FRESH_CONTROL" = 1 ] && SYS+=("modelc62:db/structures/modelc_V0_k663.xyz")

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

echo ""; echo "############### LPSOCl vs modelc62 통제 대조 ###############"
python3 - "$REPO/db/properties" $SEEDS <<'PY'
import sys, glob, numpy as np
base, seeds = sys.argv[1], sys.argv[2:]
def endpoints(lbl):
    rows=[]
    for s in seeds:
        f=f"{base}/interface_decomp_{lbl}_s{s}.csv"
        try:
            import csv
            R=list(csv.DictReader(open(f)))
            i0,iN=R[0],R[-1]
            ps=(float(i0["P_S"])-float(iN["P_S"]))/float(i0["P_S"])*100
            row=[ps, float(iN["P_Li"])-float(i0["P_Li"]), float(iN["S_Li"])-float(i0["S_Li"]),
                 float(iN["Li_penetrated"])-float(i0["Li_penetrated"])]
            if "O_P" in R[0] or "P_O" in R[0]:
                row += [(float(i0["P_O"])-float(iN["P_O"]))/max(float(i0["P_O"]),1e-9)*100,
                        float(iN["O_Li"])-float(i0["O_Li"])]
            rows.append(row)
        except FileNotFoundError: pass
    return np.array(rows) if rows else None
lp=endpoints("lpsocl")
if lp is not None:
    m=lp.mean(0); s=lp.std(0)
    print(f"  lpsocl (n={len(lp)}): PS_loss {m[0]:.1f}±{s[0]:.1f}% | dP-Li {m[1]:.2f} | dS-Li {m[2]:.2f} | dLi_pen {m[3]:.1f}")
    if lp.shape[1]>4: print(f"         POS3_loss {m[4]:.1f}±{s[4]:.1f}% | O-Li {m[5]:.2f} (rise=Li2O; O reduced?)")
print("  modelc62 ANCHOR (b2o3 campaign): PS_loss 48.1±7.8% | dP-Li 3.27 | dS-Li 1.97 | dLi_pen 10.3")
if lp is not None:
    print(f"  >>> RATIO lpsocl/modelc62 PS_loss = {lp.mean(0)[0]/48.1:.2f} (>1 worse, <1 better, ~1 equal)")
print("  (paste this + per-seed CSVs; I fold into db + figure + verdict)")
PY
echo ">> LPSOCl interface DONE"

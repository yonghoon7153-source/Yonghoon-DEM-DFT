#!/usr/bin/env bash
# =============================================================================
# High-T (800/1000 K) 3-seed reseed for BOTH systems -> SYMMETRIC error bars at
# all three temperatures, so the b2o3-vs-modelc sigma ratio gets a real bar.
#
# WHY: 600K is already 3-seeded for both (b2o3 & modelc ~1.04e-5, equal). The
# apparent b2o3 advantage sits at the SINGLE-seed 800K (ratio 1.57) / 1000K (1.19).
# High-T diffuses fast -> lower relative noise, so 3 seeds resolve it cheaply.
#
# Each driver call does --temperatures 800 1000 (seed derived per-T: base+int(T)),
# so 3 base seeds -> 3 independent trajectories at EACH of 800 and 1000 K.
# disorder 0.0 = canonical cell (b2o3_relaxV0 128-atom / modelc_V0_k663 62-atom).
# prod 100 ps is plenty: D uses only the (2,50) ps window -> identical to 200 ps,
# and matches the deck high-T length. GPU pw... err, GPU MLIP (uma-s-1p1 omat).
# =============================================================================
set -euo pipefail

REPO=${REPO:-$HOME/work/Yonghoon-DEM-DFT}          # kgy checkout
OUTROOT=${OUTROOT:-$HOME/work/runs/highT_reseed}
DEVICE=${DEVICE:-cuda}
DRIVER=$REPO/tools/modelc_v3/disorder_ensemble_diffusion.py

# system -> V0 structure (SAME cells as the deck anchors)
declare -A V0
V0[b2o3]=$REPO/db/structures/b2o3_relaxV0.xyz        # 128-atom
V0[modelc]=$REPO/db/structures/modelc_V0_k663.xyz    # 62-atom

echo "OUT=$OUTROOT  DEVICE=$DEVICE"
for SYS in b2o3 modelc; do
  for S in 2 3 4; do
    echo "===================== $SYS  800/1000K  reseed s${S} ====================="
    python3 "$DRIVER" \
      --v0_xyz "${V0[$SYS]}" --label "$SYS" \
      --out_root "$OUTROOT/${SYS}/s${S}" \
      --disorder_levels 0.0 --n_configs 1 \
      --temperatures 800 1000 \
      --equilib_ps 5 --prod_ps 100 --timestep_fs 2.0 --friction 0.02 \
      --save_fs 100 --fit_window_ps 2 50 --seed ${S} \
      --uma_model uma-s-1p1 --uma_task omat --device "$DEVICE"
  done
done

echo ""; echo "===================== collect (D_per_T[0]=800, [1]=1000) ====================="
python3 - "$OUTROOT" <<'PY'
import json, os, sys, statistics as st
root=sys.argv[1]
for sysn in ("b2o3","modelc"):
    for idx,T in ((0,800),(1,1000)):
        vals=[]
        for s in (2,3,4):
            p=os.path.join(root,sysn,f"s{s}","ensemble_results.json")
            try: vals.append(json.load(open(p))["levels"][0]["configs"][0]["D_per_T"][idx])
            except Exception as e: print(f"  ({sysn} s{s} {T}K miss: {e})")
        if vals:
            m=sum(vals)/len(vals); sd=st.pstdev(vals)
            print(f"{sysn:7s} {T}K: "+"  ".join(f"{v:.3e}" for v in vals)+f"   mean={m:.3e} +/- {sd:.1e} ({sd/m*100:.0f}%)")
PY
echo ""
echo "NEXT: paste the 8 lines (b2o3/modelc x 800/1000 means) -> I combine with the"
echo "3-seed 600K to give FULLY symmetric Ea/sigma + resolved ratio + final CSV/fig."

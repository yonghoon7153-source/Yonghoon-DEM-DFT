#!/usr/bin/env bash
# CATHODE / OXIDIZING side: does Nd3+ survive and form NdCl3 / NdPO4 / Nd-O wide-gap
# phases when the doped SE is OXIDIZED (high V), UNLIKE the Li anode where Nd->NdP?
# This is the salvage test for PDF page-4: if the wide-gap Nd phases form on the
# OXIDIZING (cathode) side, the electron-blocking SEI story holds there (not at Li).
#
# RUN ON gabia / kserver116 (MP_API_KEY set):  bash run_nd_sei_vs_cathode.sh
# Outputs: esw_nd_full.json , interface_nd_vs_cathode.json   (commit back)
set -e
cd "$(dirname "$0")"
: "${MP_API_KEY:?set MP_API_KEY first (gabia/kserver116 has it)}"

echo "============================================================"
echo "[1/3] grand-potential FULL ESW (Li-Nd-P-S-O-Cl): oxidation-side products"
echo "============================================================"
python3 esw_grand_potential.py \
  --target "Li4.8Nd0.2PS4.1O0.3Cl1.6:nd_doped" "Li5.4P1S4.4Cl1.6:modelc_ref" \
  --elements Li Nd P S O Cl \
  --out esw_nd_full.json

echo
echo "============================================================"
echo "[2/3] FOCUS: oxidation-side (V > OCV) steps, flag Nd wide-gap phases"
echo "============================================================"
python3 - <<'PY'
import json
d = json.load(open("esw_nd_full.json"))
WIDE_ND = ["NdCl3","NdPO4","Nd2O3","NdOCl","NdClO","LiNdO2","Nd(PO3)","NdP3O9"]
def walk(o):
    res=[]
    if isinstance(o,dict):
        if "profile" in o and isinstance(o["profile"],list):
            res.append(o)
        for v in o.values(): res+=walk(v)
    elif isinstance(o,list):
        for v in o: res+=walk(v)
    return res
for blk in walk(d):
    lab=blk.get("label","?"); ocv=blk.get("ocv_self_decomposition_V") or 1.7
    oxlim=blk.get("oxidation_limit_V")
    print(f"\n=== {lab}  (OCV {ocv} V, ox-onset {oxlim} V) — oxidation side (V>OCV) ===")
    for s in sorted(blk["profile"], key=lambda x:x["V_vs_Li"]):
        if s["V_vs_Li"] >= ocv - 0.01:
            rxn=s["reaction"]
            nd = " <== Nd WIDE-GAP phase!" if any(w in rxn for w in WIDE_ND) else (
                 " (Nd present)" if "Nd" in rxn else "")
            print(f"   V={s['V_vs_Li']:>5.2f}  {rxn}{nd}")
print("\n--> If NdCl3/NdPO4/Nd2O3/NdOCl/LiNdO2 appears at high V => page-4 salvageable at CATHODE.")
print("    (gaps already known: NdCl3 4.30, NdPO4 5.55, NdOCl 4.77, Nd2O3 3.81, LiNdO2 4.21 eV; Nd=lower bound)")
PY

echo
echo "============================================================"
echo "[3/3] cathode interface: SE vs LiCoO2 (charged-cathode contact)"
echo "============================================================"
python3 interface_reactivity.py \
  --electrolytes "Li4.8Nd0.2PS4.1O0.3Cl1.6:nd_doped" "Li5.4P1S4.4Cl1.6:modelc_ref" \
  --contacts LiCoO2 \
  --out interface_nd_vs_cathode.json

echo
echo "DONE -> esw_nd_full.json , interface_nd_vs_cathode.json  (commit back)"
echo "READ the [2/3] block: do Nd wide-gap phases form on the oxidation side?"

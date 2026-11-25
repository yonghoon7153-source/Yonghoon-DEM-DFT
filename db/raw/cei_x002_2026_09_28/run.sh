#!/bin/bash
set -u
cd /data/work/wt_x002_2026_09_28 || exit 9
[ -n "${MP_API_KEY:-}" ] || { echo "⛔ MP_API_KEY missing — not starting"; exit 8; }
PY=/data/apps/miniforge3/envs/uma/bin/python
T=tools/oxidation/interface_reactivity_v2.py
RUN=/data/work/runs/cei_x002_2026_09_28
echo "START $(date '+%F %T') @ $(git log --oneline -1)"
$PY $T --electrolytes \
  "Li6PS5Cl:comp1" "Li5.4P1S4.4Cl1.6:modelc" "Li5.4P1S4.2Cl1.6O0.2:lpsocl" \
  "Li4.8Nd0.2P1S4.1Cl1.6O0.3:modelc_nd" "Li4.8Nd0.2P1S4.4Cl1.6:nd_only" "Li5.4P1S4.1Cl1.6O0.3:o_only_03" \
  "Li5.34Nd0.02P1S4.4Cl1.6:nd_li_002" "Li5.44Nd0.02P0.98S4.4Cl1.6:nd_p_002" \
  "Li5.8Nd0.2P0.8S4.4Cl1.6:nd_p_020" "Li5.44Nd0.02P0.98S4.37Cl1.6O0.03:nd_p_002_asused" \
  "Li5.34Nd0.02P1S4.37Cl1.6O0.03:ndo_li_002" "Li5.4P1S4.37Cl1.6O0.03:o_only_003" \
  "Li5.34P1S4.4Cl1.6:lim_li_002" "Li4.8P1S4.4Cl1.6:lim_li_020" \
  "Li5.44P0.98S4.4Cl1.6:lim_p_002" "Li5.44P0.98S4.37Cl1.6O0.03:lim_p_002_asused" \
  --cathodes LiCoO2 LiNiO2 LiMnO2 "LiNi0.8Co0.1Mn0.1O2:NMC811" \
  --voltages 2.5 3.0 3.5 4.0 4.3 4.5 \
  --reproduce_check db/properties/cei_interface_V_2026_09_19.json \
  --out db/properties/cei_interface_V_x002_2026_09_28.json > $RUN/R1.log 2>&1
echo "R1 EXIT=$? $(date '+%T')"
$PY tools/oxidation/esw_grand_potential.py --target \
  "Li6PS5Cl:comp1" "Li5.4PS4.4Cl1.6:modelc" "Li27P5S21OCl8:lpsocl" "Li48Nd2P10O3S41Cl16:modelc_nd" \
  "Li5.34Nd0.02P1S4.37Cl1.6O0.03:ndo_li_002" "Li5.34Nd0.02P1S4.4Cl1.6:nd_li_002" \
  "Li5.4P1S4.37Cl1.6O0.03:o_only_003" \
  "Li5.44Nd0.02P0.98S4.37Cl1.6O0.03:nd_p_002_asused" "Li5.44Nd0.02P0.98S4.4Cl1.6:nd_p_002" \
  --elements Li P S Cl Nd O --open_element Li \
  --out db/properties/cei_esw_Li_x002_2026_09_28.json > $RUN/R2.log 2>&1
echo "R2 EXIT=$? $(date '+%T')"
for M in Al Sc Y La Ce Gd Nd; do
  $PY $T --electrolytes "Li5.4P1S4.4Cl1.6:base" "Li5.34${M}0.02P1S4.4Cl1.6:${M}_x002" \
    --cathodes LiCoO2 "LiNi0.8Co0.1Mn0.1O2:NMC811" --voltages 2.5 3.5 4.3 4.5 \
    --reproduce_check db/properties/dopant_iface_${M}_2026_09_16.json \
    --out db/properties/dopant_iface_${M}_x002_2026_09_28.json > $RUN/R3_${M}.log 2>&1
  echo "R3 $M EXIT=$? $(date '+%T')"
  $PY $T --closed --only "${M}_x002:Li5.34${M}0.02P1S4.4Cl1.6" --cathodes LiCoO2 \
    --out db/properties/dopant_closed_${M}_x002_2026_09_28.jsonl > $RUN/R4_${M}.log 2>&1
  echo "R4 $M EXIT=$? $(date '+%T')"
done
$PY $T --x002 db/properties/cei_interface_V_x002_2026_09_28.json \
  --x002_esw db/properties/cei_esw_Li_x002_2026_09_28.json \
  --out db/properties/cei_x002_verdicts_2026_09_28.json > $RUN/V.log 2>&1
echo "V EXIT=$? $(date '+%T')"
echo "DONE $(date '+%F %T')"

#!/bin/bash
# x = 0.10 곡률 확인 (사전등록 db/properties/cathode_cei_x010_curvature_prereg_2026_09_28.json)
# ⛔ MP_API_KEY 는 환경변수로만 받는다 — 출력에 찍지 않는다. GPU 를 안 쓴다.
set -u
cd /data/work/wt_x010_2026_09_28 || exit 9
[ -n "${MP_API_KEY:-}" ] || { echo "⛔ MP_API_KEY missing — not starting"; exit 8; }
PY=/data/apps/miniforge3/envs/uma/bin/python
T=tools/oxidation/interface_reactivity_v2.py
RUN=/data/work/runs/cei_x010_2026_09_28
mkdir -p $RUN
echo "START $(date '+%F %T') @ $(git log --oneline -1)"
$PY $T --electrolytes \
  "Li5.4P1S4.4Cl1.6:modelc" \
  "Li5.34Nd0.02P1S4.4Cl1.6:nd_li_002" "Li5.1Nd0.1P1S4.4Cl1.6:nd_li_010" "Li4.8Nd0.2P1S4.4Cl1.6:nd_only" \
  "Li5.44Nd0.02P0.98S4.4Cl1.6:nd_p_002" "Li5.6Nd0.1P0.9S4.4Cl1.6:nd_p_010" "Li5.8Nd0.2P0.8S4.4Cl1.6:nd_p_020" \
  --cathodes LiCoO2 LiNiO2 LiMnO2 "LiNi0.8Co0.1Mn0.1O2:NMC811" \
  --voltages 2.5 3.0 3.5 4.0 4.3 4.5 \
  --reproduce_check db/properties/cei_interface_V_x002_2026_09_28.json \
  --out db/properties/cei_interface_V_x010_2026_09_28.json > $RUN/R1.log 2>&1
echo "R1 EXIT=$? $(date '+%T')"
$PY $T --x010 db/properties/cei_interface_V_x010_2026_09_28.json \
  --out db/properties/cei_x010_verdicts_2026_09_28.json > $RUN/V.log 2>&1
echo "V EXIT=$? $(date '+%T')"
cat $RUN/V.log
echo "DONE $(date '+%F %T')"

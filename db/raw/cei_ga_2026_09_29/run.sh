#!/bin/bash
# Li 맞춤 축 가산성 GA (사전등록 db/properties/cathode_cei_limatched_additivity_prereg_2026_09_29.json)
# ⛔ MP_API_KEY 는 환경변수로만 받는다 — 출력에 찍지 않는다.
# ⛔ GPU 를 안 쓴다 — 지금 도는 탄성 modelc_2x(GPU pw.x) · li2s 공존 큐(UMA)와 겹치지 않는다. CPU 한 프로세스.
set -u
cd /data/work/wt_cei_ga_2026_09_29 || exit 9
[ -n "${MP_API_KEY:-}" ] || { echo "⛔ MP_API_KEY missing — not starting"; exit 8; }
PY=/data/apps/miniforge3/envs/uma/bin/python
T=tools/oxidation/interface_reactivity_v2.py
RUN=/data/work/runs/cei_ga_2026_09_29
mkdir -p $RUN
echo "START $(date '+%F %T') @ $(git log --oneline -1)"
$PY $T --selftest > $RUN/selftest.log 2>&1 || { echo "⛔ selftest FAIL — not starting"; tail -3 $RUN/selftest.log; exit 7; }
echo "selftest $(tail -1 $RUN/selftest.log)"
nice -n 10 $PY $T --electrolytes \
  "Li5.4P1S4.4Cl1.6:modelc" \
  "Li5.34Nd0.02P1S4.4Cl1.6:nd_li_002" "Li5.4P1S4.37Cl1.6O0.03:o_only_003" \
  "Li5.34Nd0.02P1S4.37Cl1.6O0.03:ndo_li_002" "Li5.34P1S4.4Cl1.6:lim_li_002" \
  "Li5.34P1S4.37Cl1.6O0.03:lim_li_002_o" \
  "Li5.44Nd0.02P0.98S4.4Cl1.6:nd_p_002" "Li5.44Nd0.02P0.98S4.37Cl1.6O0.03:nd_p_002_asused" \
  "Li5.44P0.98S4.4Cl1.6:lim_p_002" "Li5.44P0.98S4.37Cl1.6O0.03:lim_p_002_asused" \
  --cathodes LiCoO2 LiNiO2 LiMnO2 "LiNi0.8Co0.1Mn0.1O2:NMC811" \
  --voltages 2.5 3.0 3.5 4.0 4.3 4.5 \
  --reproduce_check db/properties/cei_interface_V_x002_2026_09_28.json \
  --out db/properties/cei_interface_V_ga_2026_09_29.json > $RUN/R1.log 2>&1
echo "R1 EXIT=$? $(date '+%T')"
$PY $T --x002_ga db/properties/cei_interface_V_ga_2026_09_29.json \
  --out db/properties/cei_ga_verdicts_2026_09_29.json > $RUN/V.log 2>&1
echo "V EXIT=$? $(date '+%T')"
cat $RUN/V.log
echo "DONE $(date '+%F %T')"

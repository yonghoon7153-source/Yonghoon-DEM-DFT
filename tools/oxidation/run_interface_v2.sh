#!/usr/bin/env bash
# Voltage-resolved SE/cathode interface reactivity (accurate upgrade).
# RUN on gabia/kserver116-27 (MP_API_KEY set, MP reachable).
set -e
cd "$(dirname "$0")"
: "${MP_API_KEY:?set MP_API_KEY first}"
python3 interface_reactivity_v2.py \
  --electrolytes "Li6PS5Cl:LPSCl" "Li5.4PS4.4Cl1.6:LPSCl1.6" \
  --cathodes LiCoO2 LiNiO2 "LiNi0.8Co0.1Mn0.1O2:NMC811" \
  --voltages 2.5 3.0 3.5 4.0 4.3 \
  --out interface_reactivity_v2.json
echo "DONE -> tools/oxidation/interface_reactivity_v2.json (commit back, then I plot reactivity-vs-V)"

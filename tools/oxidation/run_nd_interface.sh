#!/usr/bin/env bash
# Nd-doped vs undoped: electrolyte / cathode(+carbon) interface reactivity.
# Tests cycle-improvement mechanism #2: does Nd2O3-doping make the SE react LESS
# with the cathode / carbon (more negative ΔE_rxn = MORE reactive = worse CEI)?
# RUN on kserver116 / gabia (MP_API_KEY set, MP reachable):
#   bash run_nd_interface.sh
# Output: interface_reactivity_nd.json  (commit back)
set -e
cd "$(dirname "$0")"
: "${MP_API_KEY:?set MP_API_KEY first}"

echo "[interface reactivity] comp1 / modelc / nd  vs  LiCoO2 + C"
python3 interface_reactivity.py \
  --electrolytes "Li6PS5Cl:comp1" "Li5.4PS4.4Cl1.6:modelc" "Li4.8Nd0.2PS4.1O0.3Cl1.6:nd_doped" \
  --contacts LiCoO2 C \
  --out interface_reactivity_nd.json

echo
echo "DONE -> tools/oxidation/interface_reactivity_nd.json"
echo "Read: more-NEGATIVE min ΔE_rxn = more reactive interface (worse). If nd < |modelc|"
echo "      (less negative) vs LiCoO2/C -> Nd2O3 gives a more inert cathode interface => supports cycling↑."

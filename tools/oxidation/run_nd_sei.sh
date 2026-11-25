#!/usr/bin/env bash
# Nd2O3-doped LPSCl: SEI convex-hull / grand-potential ESW + product band gaps.
# RUN ON gabia (or kserver116) where MP_API_KEY is set and MP is reachable.
#   export MP_API_KEY=...        # if not already in env
#   bash run_nd_sei.sh
# Outputs: esw_nd_doped.json , sei_product_gaps.json  (commit back to repo)
set -e
cd "$(dirname "$0")"
: "${MP_API_KEY:?set MP_API_KEY first (gabia has it; export if missing)}"

echo "[1/2] grand-potential ESW / decomposition  (chemsys Li-Nd-P-S-O-Cl)"
python3 esw_grand_potential.py \
  --target "Li4.8Nd0.2PS4.1O0.3Cl1.6:nd_doped" "Li5.4P1S4.4Cl1.6:modelc_ref" \
  --elements Li Nd P S O Cl \
  --out esw_nd_doped.json

echo
echo "[2/2] band gaps of candidate decomposition / SEI products"
python3 sei_product_gaps.py \
  --formulas Li3PO4 Li4P2O7 NdPO4 Nd2O3 Nd2S3 NdCl3 NdOCl \
             Li2S LiCl Li3P Li3PS4 Li2O S \
  --out sei_product_gaps.json

echo
echo "DONE -> tools/oxidation/esw_nd_doped.json , tools/oxidation/sei_product_gaps.json"
echo "Check: do Li3PO4 / NdPO4 / Nd2O3 appear as products, and are product gaps wide?"

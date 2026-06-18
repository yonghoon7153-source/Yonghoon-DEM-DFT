#!/usr/bin/env bash
# vs-Li SEI + product band gaps — the electron-blocking (cycle) mechanism, NO SLAB.
# Tests the cycle story (PDF page 3-4): when the Nd2O3-doped SE contacts Li metal,
# does it form a WIDE-GAP (electron-blocking) SEI that suppresses e- leakage/dendrites?
#
#   (1) interface_reactivity vs Li metal  -> WHAT SEI forms (pseudo-binary, no slab)
#   (2) sei_product_gaps                   -> are those products wide-gap (block e-)?
#       includes NdCl3 / LiNdO2 / NdOCl (PDF "formation 확인 필요") + Li2O/LiCl/Li3PO4
#
# Slab/AIMD is NOT needed for the electron-blocking claim (that is a PROPERTY of the
# SEI products' band gaps, not of the interface geometry). Slab+AIMD only if you want
# decomposition DYNAMICS/kinetics (PDF page-3 snapshot style).
#
# RUN ON gabia / kserver116 (MP_API_KEY set, MP reachable):
#   bash run_nd_sei_vs_li.sh
# Outputs: sei_vs_Li.json , sei_product_gaps_vs_li.json   (commit back to repo)
set -e
cd "$(dirname "$0")"
: "${MP_API_KEY:?set MP_API_KEY first (gabia/kserver116 has it; export if missing)}"

echo "============================================================"
echo "[1/2] vs Li metal: what SEI forms when the doped SE meets Li (no slab)"
echo "      compositions: experimental optimum (x=0.02) + Nd-rich DFT (x=0.2) + modelc ref"
echo "============================================================"
python3 interface_reactivity.py \
  --electrolytes "Li5.44P0.98Nd0.02S4.37O0.03Cl1.6:nd_x002_exp" \
                 "Li4.8Nd0.2PS4.1O0.3Cl1.6:nd_x02_dft" \
                 "Li5.4P1S4.4Cl1.6:modelc_ref" \
  --contacts Li \
  --out sei_vs_Li.json

echo
echo "============================================================"
echo "[2/2] band gaps of candidate SEI products (wide gap = electron-blocking)"
echo "============================================================"
python3 sei_product_gaps.py \
  --formulas Li2O LiCl Li3PO4 Li4P2O7 NdPO4 Nd2O3 NdCl3 NdOCl LiNdO2 Nd2S3 NdS \
             Li3P LiP Li2S Li3PS4 S \
  --out sei_product_gaps_vs_li.json

echo
echo "DONE -> tools/oxidation/{sei_vs_Li.json , sei_product_gaps_vs_li.json}  (commit back)"
echo "READ:"
echo "  sei_vs_Li.json  : which products appear when SE meets Li? (LiCl/Li2O/Li3PO4/NdCl3/Nd-O?)"
echo "                    more-negative reaction_energy = more reactive (more SEI). compare nd vs modelc."
echo "  gaps json       : are the SEI products WIDE-gap (>~5 eV)? -> electron-blocking SEI confirmed."
echo "                    LiNdO2 'no MP entry' => not a known phase; rely on sei_vs_Li formation test."
echo "  Nd-bearing gaps are MP LOWER BOUNDS (4f underbinding); Nd-free (Li2O/LiCl/Li3PO4) reliable."

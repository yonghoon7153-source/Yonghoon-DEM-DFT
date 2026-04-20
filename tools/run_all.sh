#!/usr/bin/env bash
# Run all ready-to-go plots (data already in db/).
# Requires: numpy, matplotlib.
#
# Usage:
#   bash tools/run_all.sh
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== Ready plots (data in db/) ==="
python3 tools/plot_wad_stats.py
python3 tools/plot_ncm_convergence.py
python3 tools/plot_method_comparison.py
python3 tools/plot_gap_wad_correlation.py
python3 tools/plot_br_content_trend.py
python3 tools/plot_master_summary.py

echo
echo "=== Output files ==="
ls -la output/*.png output/*.json 2>/dev/null | awk '{print $NF, $5}'

echo
echo "=== NEXT (need xyz on V100/KISTI) ==="
echo "  python3 tools/analyze_halogen_bonds.py comp*_v5xy_s*.xyz --plot"
echo "  python3 tools/li_layer_partition.py comp*_v5xy_s*.xyz"
echo "  python3 tools/br_swap_test.py comp1_v5xy_s45.xyz --swap Cl_to_Br"

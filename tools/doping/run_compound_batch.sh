#!/usr/bin/env bash
# run_compound_batch.sh — Exhaustive compound-doping batch (v2).
#
# Generates a chemically thorough sample of doped structures by combining:
#   1. Multiple compounds (12 oxide + halide-rich + chains)
#   2. ALL chemically-allowed cation sites (Li_24g, Li_48h, P_4b — site
#      preference filter via site_preference.py drops impossible ones)
#   3. ALL chemically-allowed anion sites (S_16e, S_4a, Cl_4d)
#   4. Multiple seeds + spread/cluster methods to explore PS4 → PO4
#      tetrahedron-forming vs distributed PSO3 configurations
#
# UMA energy decides the winner — we don't pre-restrict placements.
#
# Usage:
#   bash tools/doping/run_compound_batch.sh \
#       db/structures/lpscl_F43m_24G_canonical.cif \
#       runs/doping_compound_exhaustive_2026_05_15 \
#       [N_SEEDS=3] [SUPERCELL=1,1,1]
#
# Notes on supercell — for combined Type A + Type B doping at low x, the
# 4 f.u. cell (24 Li) is too small (1 unit Nd2O3 already removes 6 Li,
# Cl-rich adds more). Use 2,1,1 (8 f.u. = 104 atoms) or 2,2,1
# (16 f.u. = 208 atoms) for combined-mode runs.

set -e

BASE="${1:?BASE cif required}"
OUT_BASE="${2:?OUT base directory required}"
N_SEEDS="${3:-3}"
SUPERCELL="${4:-1,1,1}"
SC_FLAG=$(echo "$SUPERCELL" | tr ',' ' ')

SCRIPT="tools/doping/substitute_compound.py"
METHOD="random"

mkdir -p "$OUT_BASE"
echo "==================================================="
echo "Compound doping batch v2 (exhaustive)"
echo "  base:      $BASE"
echo "  out:       $OUT_BASE"
echo "  method:    $METHOD, n_seeds: $N_SEEDS"
echo "  supercell: $SUPERCELL"
echo "==================================================="

# ============================================================
# Type A — Compound set
# Each compound × ALL chemically-allowed (cation_site, anion_site) combos
# × N_seeds. site_preference auto-filters incompatible placements.
# ============================================================
COMPOUNDS=(Nd2O3 La2O3 Sm2O3 MgO ZnO Al2O3 Sc2O3 Y2O3 BaO SrO CaO Li2O)

for cmpd in "${COMPOUNDS[@]}"; do
  out="$OUT_BASE/structures/typeA_${cmpd}"
  [ -f "$out/compound_summary.json" ] && { echo "  [skip] typeA_$cmpd"; continue; }
  echo "  → typeA_$cmpd (auto cation + anion sites)"
  python3 "$SCRIPT" \
      --base "$BASE" --supercell $SC_FLAG \
      --compound "$cmpd" --x_compound 0.05 \
      --auto_cation_sites --auto_anion_sites \
      --method "$METHOD" --n_seeds "$N_SEEDS" \
      --out "$out" 2>&1 | tail -3
done

# Same compounds again with 'cluster' method to bias toward PS4 → PO4
# tetrahedron-forming configurations. Difference vs 'random' tests whether
# the precursor's local Nd-O / La-O coordination is preferred over a fully
# distributed solid solution.
echo ""
echo "--- Type A repeated with cluster method (PS4 → PO4 bias) ---"
for cmpd in Nd2O3 La2O3 Sm2O3 Al2O3 Sc2O3 Y2O3; do
  out="$OUT_BASE/structures/typeA_${cmpd}_cluster"
  [ -f "$out/compound_summary.json" ] && { echo "  [skip] typeA_${cmpd}_cluster"; continue; }
  echo "  → typeA_${cmpd}_cluster"
  python3 "$SCRIPT" \
      --base "$BASE" --supercell $SC_FLAG \
      --compound "$cmpd" --x_compound 0.05 \
      --auto_cation_sites --auto_anion_sites \
      --method cluster --n_seeds "$N_SEEDS" \
      --out "$out" 2>&1 | tail -3
done

# ============================================================
# Type B — Halide-rich (distinct n_swap values)
# ============================================================
for x in 0.25 0.50 0.75; do
  xname="${x/0./0}"
  out="$OUT_BASE/structures/typeB_Clrich_x${xname}"
  [ -f "$out/compound_summary.json" ] && { echo "  [skip] typeB_x${xname}"; continue; }
  echo "  → typeB_Clrich_x${xname}"
  python3 "$SCRIPT" \
      --base "$BASE" --supercell $SC_FLAG \
      --halide_rich Cl --excess_per_fu "$x" \
      --anion_site S_4a \
      --method "$METHOD" --n_seeds "$N_SEEDS" \
      --out "$out" 2>&1 | tail -3
done

# ============================================================
# Type C — Aliovalent + halide chain (Yu 2022 Al-Cl, plus RE/Sc variants)
# ============================================================
for cmpd in Al2O3 Sc2O3 Y2O3 La2O3 Nd2O3; do
  out="$OUT_BASE/structures/typeC_${cmpd}_Clchain"
  [ -f "$out/compound_summary.json" ] && { echo "  [skip] typeC_${cmpd}_Clchain"; continue; }
  echo "  → typeC_${cmpd}_Clchain"
  python3 "$SCRIPT" \
      --base "$BASE" --supercell $SC_FLAG \
      --compound "$cmpd" --x_compound 0.05 \
      --auto_anion_sites \
      --also_halide_rich Cl --excess_per_fu 0.50 \
      --method "$METHOD" --n_seeds "$N_SEEDS" \
      --out "$out" 2>&1 | tail -3
done

echo ""
echo "==================================================="
echo "Merging into single structures_summary.json..."
echo "==================================================="

python3 << PYEOF
import json
from pathlib import Path

out_base = Path("$OUT_BASE")
merged = []
for sub in sorted(out_base.glob("structures/*/compound_summary.json")):
    data = json.loads(sub.read_text())
    for s in data.get('structures', []):
        steps = s.get('steps', [])
        type_a = next((st for st in steps if st['type'] == 'A_compound'), None)
        type_b = next((st for st in steps if st['type'] == 'B_halide_rich'), None)
        type_c = next((st for st in steps if st['type'] == 'C_chain_halide_rich'), None)
        if type_a and type_c:
            label_dopant = f"{type_a['compound']}+{type_c['halide']}rich"
            comp_label = 'compound_set_chain'
            label_conc = type_a.get('actual_x', 0.0)
        elif type_a:
            label_dopant = type_a['compound']
            comp_label = 'compound_set'
            label_conc = type_a.get('actual_x', 0.0)
        elif type_b:
            label_dopant = f"{type_b['halide']}rich"
            comp_label = 'halide_rich_vac'
            label_conc = type_b.get('actual_excess', 0.0)
        else:
            label_dopant, comp_label, label_conc = 'unknown', 'unknown', 0.0

        s.setdefault('dopant', label_dopant)
        s.setdefault('site', s.get('cation_site_used', 'unknown'))
        s.setdefault('anion_site_label', s.get('anion_site_used', 'unknown'))
        s.setdefault('concentration', label_conc)
        s.setdefault('charge_compensation', comp_label)
        s.setdefault('compatibility_score', 1.0)
        s.setdefault('host', 'compound')
        merged.append(s)

merge_path = out_base / 'structures_summary.json'
merge_path.write_text(json.dumps({'structures': merged}, indent=2, default=str))
print(f"  Merged {len(merged)} structures → {merge_path}")
PYEOF

echo ""
echo "Next: run UMA screening on $OUT_BASE/structures_summary.json"
echo "      (compound batch needs --steps 1500 for convergence)"

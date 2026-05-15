#!/usr/bin/env bash
# run_compound_batch.sh — Generate the full LPSCl compound-doping batch.
#
# Produces a clean, non-redundant set of structures across all four mechanism
# types from db/literature/lpscl_doping_precursor_compounds_review.md.
#
# Concentration choice rationale (4 f.u. = 52 atom cell):
#   1 compound unit = 0.25 mole fraction (minimum). x=0.025/0.05/0.10 all round
#   to 1 unit, so we use a single nominal x=0.05 per compound. For finer
#   concentrations a 2x2x2 supercell (32 f.u.) is required — left for future.
#   Multiple seeds (--method random --n_seeds N) give ensemble averaging
#   within one concentration.
#
# Usage:
#   bash tools/doping/run_compound_batch.sh \
#       db/structures/lpscl_F43m_24G_canonical.cif \
#       runs/doping_compound_2026_05_15 \
#       [N_SEEDS=3]

set -e

BASE="${1:?BASE cif required}"
OUT_BASE="${2:?OUT base directory required}"
N_SEEDS="${3:-3}"
SCRIPT="tools/doping/substitute_compound.py"
METHOD="random"

mkdir -p "$OUT_BASE"
echo "==================================================="
echo "Compound doping batch"
echo "  base:    $BASE"
echo "  out:     $OUT_BASE"
echo "  method:  $METHOD, n_seeds: $N_SEEDS"
echo "==================================================="

# ============================================================
# Type A — Compound set (12 compounds × 1 effective concentration)
# x=0.05 → 1 unit per 4 f.u. (the minimum distinct concentration)
# ============================================================
COMPOUNDS=(Nd2O3 La2O3 Sm2O3 MgO ZnO Al2O3 Sc2O3 Y2O3 BaO SrO CaO Li2O)

for cmpd in "${COMPOUNDS[@]}"; do
  name="${cmpd}_x050"
  out="$OUT_BASE/structures/$name"
  [ -f "$out/compound_summary.json" ] && { echo "  [skip] $name"; continue; }
  echo "  → $name"
  python3 "$SCRIPT" \
      --base "$BASE" --compound "$cmpd" --x_compound 0.05 \
      --cation_site Li_24g --anion_site S_16e \
      --method "$METHOD" --n_seeds "$N_SEEDS" \
      --out "$out" 2>&1 | tail -2
done

# ============================================================
# Type B — Halide-rich (distinct n_swap values)
# x=0.25→1 swap, x=0.50→2 swaps, x=0.75→3 swaps
# Note: x=0.50 reproduces Li5.4PS4.4Cl1.6 (modelc).
# ============================================================
for x in 0.25 0.50 0.75; do
  xname="${x/0./0}"
  name="Cl_rich_x${xname}"
  out="$OUT_BASE/structures/$name"
  [ -f "$out/compound_summary.json" ] && { echo "  [skip] $name"; continue; }
  echo "  → $name (Type B halide-rich)"
  python3 "$SCRIPT" \
      --base "$BASE" --halide_rich Cl --excess_per_fu "$x" \
      --anion_site S_4a \
      --method "$METHOD" --n_seeds "$N_SEEDS" \
      --out "$out" 2>&1 | tail -2
done

# ============================================================
# Type C — Aliovalent + halide chain (Yu 2022 Al-Cl, plus Sc-Cl)
# Each compound at 0.05 + Cl excess at 0.50
# ============================================================
for cmpd in Al2O3 Sc2O3; do
  name="${cmpd}_x050_Clchain_x050"
  out="$OUT_BASE/structures/$name"
  [ -f "$out/compound_summary.json" ] && { echo "  [skip] $name"; continue; }
  echo "  → $name (Type C chain)"
  python3 "$SCRIPT" \
      --base "$BASE" --compound "$cmpd" --x_compound 0.05 \
      --also_halide_rich Cl --excess_per_fu 0.50 \
      --method "$METHOD" --n_seeds "$N_SEEDS" \
      --out "$out" 2>&1 | tail -2
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
        # Derive a canonical 'dopant'/'site'/'concentration' for the analyzer.
        steps = s.get('steps', [])
        type_a = next((st for st in steps if st['type'] == 'A_compound'), None)
        type_b = next((st for st in steps if st['type'] == 'B_halide_rich'), None)
        type_c = next((st for st in steps if st['type'] == 'C_chain_halide_rich'), None)
        if type_a and type_c:
            label_dopant = f"{type_a['compound']}+{type_c['halide']}rich"
            label_site = type_a.get('cation_site', 'Li_24g')
            label_conc = type_a.get('actual_x', 0.0)
            comp_label = 'compound_set_chain'
        elif type_a:
            label_dopant = type_a['compound']
            label_site = type_a.get('cation_site', 'Li_24g')
            label_conc = type_a.get('actual_x', 0.0)
            comp_label = 'compound_set'
        elif type_b:
            label_dopant = f"{type_b['halide']}rich"
            label_site = 'S_4a'
            label_conc = type_b.get('actual_excess', 0.0)
            comp_label = 'halide_rich_vac'
        else:
            label_dopant = 'unknown'
            label_site = 'unknown'
            label_conc = 0.0
            comp_label = 'unknown'

        s.setdefault('dopant', label_dopant)
        s.setdefault('site', label_site)
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

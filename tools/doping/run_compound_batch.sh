#!/usr/bin/env bash
# run_compound_batch.sh — Exhaustive compound-doping batch (v3).
#
# v3 expands compound diversity following Bml lab feedback:
#   - Not just oxides but fluorides, bromides/iodides, nitrides, sulfides
#   - +1 to +6 oxidation states represented (Li2O, MgO, Al2O3, SiO2, V2O5, WO3)
#   - Small / high-valence cations (B, W, Mo) that prefer the P site
#   - --allow_exotic mode skips site_preference filter so chemically
#     unusual placements (e.g., La at P_4b, B at Li_24g) get tried
#
# Caveat — donor-only compensation: acceptor cations (B³⁺ at P⁵⁺, Si⁴⁺ at P⁵⁺
# etc.) leave the cell charge-imbalanced because Li-interstitial / reverse-
# halide-rich paths are not yet modeled. UMA energy automatically ranks
# these lower; their imbalance is recorded in placement_log.
#
# Usage:
#   bash tools/doping/run_compound_batch.sh \
#       db/structures/lpscl_F43m_24G_canonical.cif \
#       runs/doping_v3_2026_05_15 \
#       [N_SEEDS=3] [SUPERCELL=1,1,1] [EXOTIC=0]

set -e

BASE="${1:?BASE cif required}"
OUT_BASE="${2:?OUT base directory required}"
N_SEEDS="${3:-3}"
SUPERCELL="${4:-1,1,1}"
EXOTIC="${5:-0}"
SC_FLAG=$(echo "$SUPERCELL" | tr ',' ' ')

EXOTIC_FLAG=""
[ "$EXOTIC" = "1" ] && EXOTIC_FLAG="--allow_exotic"

SCRIPT="tools/doping/substitute_compound.py"
METHOD="random"

mkdir -p "$OUT_BASE"
echo "==================================================="
echo "Compound doping batch v3 (diversified)"
echo "  base:        $BASE"
echo "  out:         $OUT_BASE"
echo "  method:      $METHOD, n_seeds: $N_SEEDS"
echo "  supercell:   $SUPERCELL"
echo "  allow_exotic: $EXOTIC"
echo "==================================================="

# ============================================================
# Compound dictionary by category
# ============================================================
# +1 (alkali / monovalent — adds Li-like cation)
MONO_OXIDES=(Li2O Na2O Cu2O Ag2O)

# +2 (divalent — Mg/Zn/Ca family + 3d TM)
DI_OXIDES=(MgO ZnO CaO SrO BaO MnO CoO NiO)

# +3 (trivalent — RE, Sc/Y, Al, Cr, Fe — most common LPSCl doping case)
TRI_OXIDES=(Al2O3 Sc2O3 Y2O3 La2O3 Nd2O3 Sm2O3 Gd2O3 Ga2O3 In2O3 Cr2O3 Fe2O3 B2O3)

# +4 (tetravalent — Si/Ge/Sn/Ti/Zr/Hf, isoelectronic with P⁵⁺ → P-site acceptor)
TETRA_OXIDES=(SiO2 GeO2 SnO2 TiO2 ZrO2 HfO2)

# +5 (pentavalent — Sb/V/Nb/Ta, P-site isovalent)
PENTA_OXIDES=(V2O5 Nb2O5 Ta2O5 Sb2O5)

# +6 (hexavalent — Cr/Mo/W, P-site donor +1)
HEXA_OXIDES=(CrO3 MoO3 WO3)

# Fluorides (alternative halide precursors — F → Cl_4d, cation → Li/P)
FLUORIDES=(LiF NaF MgF2 CaF2 AlF3 YF3)

# Bromides / iodides (halogen mixing)
HALIDES_MIXED=(LiBr LiI NaBr KBr)

# Nitrides (N → S_4a anion disorder, less common but reported for argyrodites)
NITRIDES=(Li3N AlN BN)

ALL_COMPOUNDS=("${MONO_OXIDES[@]}" "${DI_OXIDES[@]}" "${TRI_OXIDES[@]}"
               "${TETRA_OXIDES[@]}" "${PENTA_OXIDES[@]}" "${HEXA_OXIDES[@]}"
               "${FLUORIDES[@]}" "${HALIDES_MIXED[@]}" "${NITRIDES[@]}")

echo ""
echo "Total compound classes: ${#ALL_COMPOUNDS[@]}"
echo ""

# ============================================================
# Type A — every compound × all chemically-allowed sites × N seeds
# ============================================================
for cmpd in "${ALL_COMPOUNDS[@]}"; do
  out="$OUT_BASE/structures/typeA_${cmpd}"
  [ -f "$out/compound_summary.json" ] && { echo "  [skip] typeA_$cmpd"; continue; }
  echo "  → typeA_$cmpd"
  python3 "$SCRIPT" \
      --base "$BASE" --supercell $SC_FLAG \
      --compound "$cmpd" --x_compound 0.05 \
      --auto_cation_sites --auto_anion_sites \
      $EXOTIC_FLAG \
      --method "$METHOD" --n_seeds "$N_SEEDS" \
      --out "$out" 2>&1 | tail -3 || echo "    (skipped: chemistry not allowed)"
done

# ============================================================
# Type A cluster method on the trivalent + small cations (PS4 → PO4)
# ============================================================
echo ""
echo "--- Type A cluster method (precursor local-coord biased) ---"
for cmpd in Nd2O3 La2O3 Sm2O3 Al2O3 Sc2O3 Y2O3 B2O3 WO3 MoO3 Cr2O3; do
  out="$OUT_BASE/structures/typeA_${cmpd}_cluster"
  [ -f "$out/compound_summary.json" ] && { echo "  [skip] typeA_${cmpd}_cluster"; continue; }
  echo "  → typeA_${cmpd}_cluster"
  python3 "$SCRIPT" \
      --base "$BASE" --supercell $SC_FLAG \
      --compound "$cmpd" --x_compound 0.05 \
      --auto_cation_sites --auto_anion_sites \
      $EXOTIC_FLAG \
      --method cluster --n_seeds "$N_SEEDS" \
      --out "$out" 2>&1 | tail -3 || true
done

# ============================================================
# Type B — Halide-rich (Cl, Br, I — multiple anion-rich families)
# ============================================================
for hx in 0.25 0.50 0.75; do
  xname="${hx/0./0}"
  for halide in Cl Br I; do
    out="$OUT_BASE/structures/typeB_${halide}rich_x${xname}"
    [ -f "$out/compound_summary.json" ] && { echo "  [skip] typeB_${halide}_x${xname}"; continue; }
    echo "  → typeB_${halide}rich_x${xname}"
    python3 "$SCRIPT" \
        --base "$BASE" --supercell $SC_FLAG \
        --halide_rich "$halide" --excess_per_fu "$hx" \
        --anion_site S_4a \
        --method "$METHOD" --n_seeds "$N_SEEDS" \
        --out "$out" 2>&1 | tail -3 || true
  done
done

# ============================================================
# Type C — Aliovalent + halide chain (representative cations × Cl excess)
# ============================================================
for cmpd in Al2O3 Sc2O3 Y2O3 La2O3 Nd2O3 MgO ZnO WO3 MoO3 B2O3; do
  out="$OUT_BASE/structures/typeC_${cmpd}_Clchain"
  [ -f "$out/compound_summary.json" ] && { echo "  [skip] typeC_${cmpd}_Clchain"; continue; }
  echo "  → typeC_${cmpd}_Clchain"
  python3 "$SCRIPT" \
      --base "$BASE" --supercell $SC_FLAG \
      --compound "$cmpd" --x_compound 0.05 \
      --auto_anion_sites $EXOTIC_FLAG \
      --also_halide_rich Cl --excess_per_fu 0.50 \
      --method "$METHOD" --n_seeds "$N_SEEDS" \
      --out "$out" 2>&1 | tail -3 || true
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
echo "      (compound batch needs --steps 1500+ for convergence)"

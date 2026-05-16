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
EXOTIC="${5:-1}"  # default 1 = explore chemically-unusual placements too
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

# Fluorides (F → Cl_4d, cation → Li/P)
FLUORIDES=(LiF NaF MgF2 CaF2 AlF3 YF3 LaF3 NdF3 ZrF4 TiF4 ScF3)

# Chlorides (precursor that adds both cation and Cl — ZrCl4/TiCl4/AlCl3
# common ball-mill reagents; CeCl3/LaCl3 etc. for RE doping)
CHLORIDES=(LiCl NaCl KCl MgCl2 CaCl2 SrCl2 BaCl2 AlCl3 GaCl3 FeCl3 CrCl3
           YCl3 LaCl3 NdCl3 SmCl3 ScCl3 ZrCl4 HfCl4 TiCl4 NbCl5 TaCl5)

# Bromides / iodides (halogen-mixed argyrodite precursors)
BROMIDES=(LiBr NaBr KBr MgBr2 CaBr2 AlBr3 ZrBr4)
IODIDES=(LiI NaI MgI2 AlI3)

# Nitrides (N → S_4a anion disorder, e.g., Li6PS4N1Cl variants reported)
NITRIDES=(Li3N Na3N Mg3N2 Ca3N2 AlN BN Si3N4 GaN)

# Sulfide precursors (cation → host, S already host so no anion change —
# effectively single-element cation substitution; included because real
# LPSCl synthesis routinely uses these as starting reagents)
SULFIDES=(Li2S Na2S MgS CaS Al2S3 Ga2S3 B2S3 SiS2 GeS2 SnS2 P2S5 As2S3 Sb2S3
          Y2S3 La2S3 Nd2S3 ZrS2 TiS2)

# Polyanion-substituting compounds (PO4 / SO4 / BO3 unit replaces PS4)
# Treated as 'compound' substitution; user iterates auto sites to find
# energetically favored unit.
POLYANIONS=(Li3PO4 Li2SO4 Li3BO3 Li2MoO4 Li2WO4 LiNO3)

ALL_COMPOUNDS=("${MONO_OXIDES[@]}" "${DI_OXIDES[@]}" "${TRI_OXIDES[@]}"
               "${TETRA_OXIDES[@]}" "${PENTA_OXIDES[@]}" "${HEXA_OXIDES[@]}"
               "${FLUORIDES[@]}" "${CHLORIDES[@]}" "${BROMIDES[@]}"
               "${IODIDES[@]}" "${NITRIDES[@]}" "${SULFIDES[@]}"
               "${POLYANIONS[@]}")

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
# Type B — Halide-rich, fine-grained excess sweep (Cl, Br, I)
# Halide excess x_excess covers Li6→Li5 working range. Distinct n_swap
# values on 1x1x1 (4 fu): 0.20→1, 0.40→2, 0.60→2, 0.80→3, full S→Cl→4.
# Larger supercells give finer resolution (e.g., 2x2x1 = 16 fu allows
# 1/16 increments).
# ============================================================
for hx in 0.10 0.20 0.30 0.40 0.50 0.60 0.70 0.80 0.90; do
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
# Type C — Cation compound × halide excess fine sweep
# Each top compound × halide excess {0.20, 0.40, 0.60, 0.80}
# Mirrors Yu 2022 Al-Cl strategy but with explicit Cl excess scan; the
# (compound, halide_excess) pair acts like a single composite dopant
# whose stoichiometry the user can fine-tune via the excess parameter.
# ============================================================
for cmpd in Al2O3 Sc2O3 Y2O3 La2O3 Nd2O3 MgO ZnO WO3 MoO3 B2O3 Sm2O3; do
  for hx in 0.20 0.40 0.60 0.80; do
    xname="${hx/0./0}"
    out="$OUT_BASE/structures/typeC_${cmpd}_Clchain_x${xname}"
    [ -f "$out/compound_summary.json" ] && { echo "  [skip] typeC_${cmpd}_x${xname}"; continue; }
    echo "  → typeC_${cmpd}_Clchain_x${xname}"
    python3 "$SCRIPT" \
        --base "$BASE" --supercell $SC_FLAG \
        --compound "$cmpd" --x_compound 0.05 \
        --auto_anion_sites $EXOTIC_FLAG \
        --also_halide_rich Cl --excess_per_fu "$hx" \
        --method "$METHOD" --n_seeds "$N_SEEDS" \
        --out "$out" 2>&1 | tail -3 || true
  done
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

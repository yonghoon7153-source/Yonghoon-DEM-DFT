#!/usr/bin/env bash
# Oxophilicity descriptor — is Nd a SPECIAL O-getter, or just an O-carrier?
# Ranks cations (Nd vs La/Ce/Y/Sm/Gd vs Al/Mg/Zn vs Li/Na vs Zr/Ti...) by their
# O-over-S preference (= the driving force that pulls O into a sulfide and holds it).
# One-shot MP query — NO doped-cell DFT needed.
#
# RUN ON gabia (or kserver116) where MP_API_KEY is set and MP is reachable:
#   export MP_API_KEY=...        # if not already in env (gabia has it)
#   bash run_oxophilicity.sh
# Output: oxophilicity.json  (commit back to repo)
set -e
cd "$(dirname "$0")"
: "${MP_API_KEY:?set MP_API_KEY first (gabia has it; export if missing)}"

# dependency sanity (same stack as esw_grand_potential.py / interface_reactivity.py)
python3 -c "import mp_api, pymatgen" 2>/dev/null || {
  echo "[!] need mp_api + pymatgen (same env as the other oxidation scripts)."
  echo "    pip install --quiet mp_api pymatgen   # if missing"; exit 1; }

echo "[oxophilicity] ranking cations by O-over-S preference (Nd vs La/Y/Al/Mg/Li ...)"
python3 oxophilicity_descriptor.py --out oxophilicity.json

echo
echo "DONE -> tools/oxidation/oxophilicity.json   (commit back to repo)"
echo "Read: 'ranking_most_to_least_oxophilic' + 'Nd_rank' (0 = most oxophilic)."
echo "  Nd ABOVE Li/Mg/Al  -> Nd3+ has genuine extra O-affinity (getter, Nd-specific)."
echo "  Nd ~ Li/Mg         -> Nd is just an O-carrier (the benefits are O's)."
echo "  compare Nd vs La/Ce/Y -> rare-earth generic vs Nd-4f specific."

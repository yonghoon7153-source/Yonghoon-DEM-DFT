#!/usr/bin/env bash
# tier_cascade.sh — championship-grade end-to-end pipeline.
#
# Stage 0  preflight       — UMA loads, baseline sane, PS4 intact, disk OK
# Stage 1  substitute      — generate compound variants (run_compound_batch.sh)
# Stage 2  UMA screen      — relax all variants, compute Tier-1+Tier-2 metrics
# Stage 3  select winners  — per (compound, sites) Top-1
# Stage 4  light anneal    — 300K/20ps to relieve unphysical Li placement
# Stage 5  re-screen post-anneal  — analyze with --objective composite + binding_E
# Stage 6  MLIP post-proc  — EOS + elastic per winner (B0, Cij, Pugh)
# Stage 7  final report    — top-N table grouped by paper-relevant axis
#
# Usage:
#   bash tools/doping/tier_cascade.sh \
#       db/structures/lpscl_F43m_24G_canonical.cif \
#       runs/tier_cascade_$(date +%F) \
#       [N_SEEDS=5] [SUPERCELL=1,1,1] [EXOTIC=1]

set -e

BASE="${1:?BASE cif required}"
OUT="${2:?OUT dir required}"
N_SEEDS="${3:-5}"
SUPERCELL="${4:-1,1,1}"
EXOTIC="${5:-1}"
SC_FLAG=$(echo "$SUPERCELL" | tr ',' ' ')

mkdir -p "$OUT/logs"
cd "$(dirname $BASE)"/..  # ensure repo root cwd

LOG() { echo "[$(date +%H:%M:%S)] $*"; }

# ============================================================
# Stage 0 — Preflight
# ============================================================
LOG "Stage 0: preflight"
python3 tools/doping/preflight.py \
    --base "$BASE" --out "$OUT/preflight" --device cuda \
    2>&1 | tee -a "$OUT/logs/00_preflight.log"
if [ ${PIPESTATUS[0]} -ne 0 ]; then
    LOG "Preflight FAILED — abort"
    exit 1
fi

# ============================================================
# Stage 1 — Generate compound batch
# ============================================================
LOG "Stage 1: substitute_compound batch (n_seeds=$N_SEEDS, sc=$SUPERCELL)"
bash tools/doping/run_compound_batch.sh \
    "$BASE" "$OUT/01_structures" "$N_SEEDS" "$SUPERCELL" "$EXOTIC" \
    2>&1 | tee -a "$OUT/logs/01_batch.log"

# ============================================================
# Stage 2 — UMA screening
# ============================================================
LOG "Stage 2: UMA screening (--steps 1500)"
python3 tools/doping/run_uma_screening.py \
    --summary "$OUT/01_structures/structures_summary.json" \
    --base "$BASE" \
    --baseline "$OUT/02_screen/baseline.json" \
    --out "$OUT/02_screen/uma_results.json" \
    --device cuda --steps 1500 \
    2>&1 | tee -a "$OUT/logs/02_screen.log"

# ============================================================
# Stage 3 — Pick per-group winners
# ============================================================
LOG "Stage 3: select per-(compound,sites) winners"
python3 tools/doping/select_winners.py \
    --results "$OUT/02_screen/uma_results.json" \
    --out "$OUT/03_winners/winners.json" \
    --group_by dopant site anion_site_label \
    --max_dv 0.25 \
    2>&1 | tee -a "$OUT/logs/03_winners.log"

# ============================================================
# Stage 4 — Light anneal (per-compound stratified)
# ============================================================
LOG "Stage 4: light anneal (300K, 20ps) of winners"
python3 tools/doping/run_anneal.py \
    --summary_json "$OUT/03_winners/winners.json" \
    --out "$OUT/04_anneal" \
    --device cuda --light \
    2>&1 | tee -a "$OUT/logs/04_anneal.log"

# ============================================================
# Stage 5 — Post-anneal ranking
# ============================================================
LOG "Stage 5: post-anneal ranking"
python3 tools/doping/rank_anneal.py \
    --screening "$OUT/02_screen/uma_results.json" \
    --anneal "$OUT/04_anneal/anneal_results.json" \
    --out "$OUT/05_post_anneal_ranking.json" --top 30 \
    2>&1 | tee -a "$OUT/logs/05_rank.log"

# ============================================================
# Stage 6 — Full MLIP post-processing (EOS + elastic)
# ============================================================
LOG "Stage 6: MLIP post-processing (EOS + elastic) on winners"
python3 tools/doping/run_mlip_postproc.py \
    --winners "$OUT/03_winners/winners.json" \
    --out "$OUT/06_postproc" \
    --device cuda \
    2>&1 | tee -a "$OUT/logs/06_postproc.log"

# ============================================================
# Stage 7 — Final report
# ============================================================
LOG "Stage 7: final report"
python3 << PYEOF
import json
from pathlib import Path
out = Path("$OUT")

# Combine all outputs into final report
final = {}
for stage in ['02_screen/uma_results.json',
              '03_winners/winners.json',
              '04_anneal/anneal_results.json',
              '05_post_anneal_ranking.json',
              '06_postproc/postproc_summary.json']:
    p = out / stage
    if p.exists():
        try:
            final[p.stem] = {'path': str(p), 'size': p.stat().st_size}
        except Exception:
            pass

# Pretty print Top-10 from postproc
pp = out / '06_postproc' / 'postproc_summary.json'
if pp.exists():
    recs = json.loads(pp.read_text()).get('records', [])
    recs = [r for r in recs if 'eos' in r and 'B0_GPa' in r['eos']]
    recs.sort(key=lambda r: -r['eos']['B0_GPa'])  # highest B0 first
    print("\\n=== Top-10 by B0 (MLIP-EOS) ===")
    print(f"{'Rank':<5}{'Name':<40}{'B0 GPa':>10}{'V0':>10}{'E/atom':>10}{'Pugh':>8}")
    for i, r in enumerate(recs[:10], 1):
        eos = r['eos']
        ela = r.get('elastic', {})
        print(f"{i:<5}{r['name'][:38]:<40}"
              f"{eos['B0_GPa']:>+9.2f} "
              f"{eos['V0']:>+9.2f} "
              f"{r.get('E_post_anneal_per_atom', 0):>+8.4f}  "
              f"{ela.get('pugh_ratio_GoverB', 0):>5.3f}")

(out / 'FINAL_REPORT.json').write_text(json.dumps(final, indent=2, default=str))
PYEOF

LOG "All stages done. Final outputs in: $OUT"
echo ""
echo "================================================================"
echo "  Tier cascade COMPLETE"
echo "================================================================"

#!/usr/bin/env bash
# tier_cascade.sh — factory-style 10-stage pipeline (v2, championship grade)
#
# Design principles:
#   1. Cheap-first  — BVSE (sec) before EOS (hours) before AIMD (days)
#   2. No duplication — each anneal / relax happens exactly once
#   3. Resume safe — every stage writes STAGE_*.DONE marker; rerun skips
#   4. Modular — each stage callable standalone; cascade is just orchestration
#   5. Logged per stage — logs/NN_*.log for surgical debugging
#
# Stage map:
#   00  preflight              ~  5 min   (sanity)
#   01  substitute (batch)     ~ 10 min   (~2000 structures)
#   02  UMA screen (Tier 1+2)  ~ 3-8 h    (heaviest single stage)
#   03  select winners         ~  1 min   (per-group Top-1)
#   04  BVSE proxy (cheap)     ~  5 min   (Li mobility before heavy stages)
#   05  light anneal winners   ~ 1-2 h    (300K, 20 ps + relax — Pipeline Step 3)
#   06  re-rank post-anneal    ~  1 min   (ranking-flip detection)
#   07  MLIP EOS               ~ 3-5 h    (B0, V0, BM3-fit)
#   08  MLIP elastic           ~ 3-5 h    (C_ij, B/G/E/Pugh)
#   09  final report           ~  1 min
#
# Total: ~12-25 h for ~100 winners across ~85 compounds.
#
# Usage:
#   bash tools/doping/tier_cascade.sh \
#       db/structures/lpscl_F43m_24G_canonical.cif \
#       runs/tier_$(date +%F) \
#       [N_SEEDS=5] [SUPERCELL=1,1,1] [EXOTIC=1]
#
# Resume after crash:
#   bash tools/doping/tier_cascade.sh <same args>
#   (stages with STAGE_NN.DONE marker are skipped)

set -e

BASE="${1:?BASE cif required}"
OUT="${2:?OUT dir required}"
N_SEEDS="${3:-5}"
SUPERCELL="${4:-1,1,1}"
EXOTIC="${5:-1}"

mkdir -p "$OUT/logs"
cd "$(dirname $(realpath "$BASE"))/.." 2>/dev/null || cd .

LOG() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$OUT/cascade.log"; }
DONE_MARK() { touch "$OUT/STAGE_${1}.DONE"; }
DONE_CHECK() { [ -f "$OUT/STAGE_${1}.DONE" ]; }
STAGE() {
    local id=$1; local name=$2; shift 2
    if DONE_CHECK "$id"; then
        LOG "Stage $id ($name): SKIP (already done)"
        return 0
    fi
    LOG "Stage $id ($name): START"
    local t0=$(date +%s)
    "$@" 2>&1 | tee -a "$OUT/logs/${id}_${name}.log"
    local status=${PIPESTATUS[0]}
    local elapsed=$(($(date +%s) - t0))
    if [ $status -eq 0 ]; then
        DONE_MARK "$id"
        LOG "Stage $id ($name): OK (${elapsed}s)"
    else
        LOG "Stage $id ($name): FAILED — abort cascade"
        exit $status
    fi
}

# Print plan
LOG "==================================================="
LOG "  tier_cascade v2 — championship factory line"
LOG "  base:        $BASE"
LOG "  output:      $OUT"
LOG "  n_seeds:     $N_SEEDS"
LOG "  supercell:   $SUPERCELL"
LOG "  allow_exotic: $EXOTIC"
LOG "  cwd:         $(pwd)"
LOG "==================================================="

# Stage 00 — Preflight
STAGE 00 preflight \
    python3 tools/doping/preflight.py \
        --base "$BASE" --out "$OUT/00_preflight" --device cuda

# Stage 01 — Substitute compound batch
STAGE 01 substitute \
    bash tools/doping/run_compound_batch.sh \
        "$BASE" "$OUT/01_structures" "$N_SEEDS" "$SUPERCELL" "$EXOTIC"

# Stage 02 — UMA screen
STAGE 02 screen \
    python3 tools/doping/run_uma_screening.py \
        --summary "$OUT/01_structures/structures_summary.json" \
        --base "$BASE" \
        --baseline "$OUT/02_screen/baseline.json" \
        --out "$OUT/02_screen/uma_results.json" \
        --device cuda --steps 1500

# Stage 03 — Select per-group winners
STAGE 03 winners \
    python3 tools/doping/select_winners.py \
        --results "$OUT/02_screen/uma_results.json" \
        --out "$OUT/03_winners/winners.json" \
        --group_by dopant site anion_site_label \
        --max_dv 0.25

# Stage 04 — BVSE Li mobility proxy (cheap, before heavy stages)
STAGE 04 bvse \
    python3 tools/doping/bvse_proxy.py \
        --xyz_dir "$OUT/01_structures/structures" \
        --out "$OUT/04_bvse/bvs_report.json" \
        --grid_resolution 25

# Stage 05 — Light anneal of winners (uses winners.json → xyz_file → light Langevin)
STAGE 05 anneal \
    python3 tools/doping/run_anneal.py \
        --summary_json "$OUT/03_winners/winners.json" \
        --out "$OUT/05_anneal" \
        --device cuda --light

# Stage 06 — Re-rank using post-anneal energies
STAGE 06 rerank \
    python3 tools/doping/rank_anneal.py \
        --screening "$OUT/02_screen/uma_results.json" \
        --anneal "$OUT/05_anneal/anneal_results.json" \
        --out "$OUT/06_rerank/post_anneal_ranking.json" --top 30

# Stage 07 — MLIP EOS (uses POST-ANNEAL xyz so no double-anneal)
#   --no_anneal skips the redundant anneal step inside run_mlip_postproc
STAGE 07 eos \
    python3 tools/doping/run_mlip_postproc.py \
        --xyz $(ls "$OUT"/05_anneal/*/post_relax.xyz 2>/dev/null | tr '\n' ' ') \
        --out "$OUT/07_eos" \
        --no_anneal --no_elastic \
        --device cuda

# Stage 08 — MLIP elastic (clamped-ion Cij at 0K, then VRH average)
STAGE 08 elastic \
    python3 tools/doping/run_mlip_postproc.py \
        --xyz $(ls "$OUT"/05_anneal/*/post_relax.xyz 2>/dev/null | tr '\n' ' ') \
        --out "$OUT/08_elastic" \
        --no_anneal --no_eos \
        --device cuda

# Stage 09 — Final report
# Stage 9a — Aggregate into FINAL_RANKING.json
STAGE 09a combine \
    python3 tools/doping/combine_rankings.py \
        --cascade_dir "$OUT" \
        --out "$OUT/FINAL_RANKING.json"

# Stage 9b — Collect dataset for ML predictor
STAGE 09b collect \
    python3 tools/doping/collect_dataset.py \
        --cascade_dir "$OUT" \
        --out "$OUT/dataset.csv"

# Stage 9c — Train in-house ML predictor (so future candidates can be
#   scored instantly without running the full cascade).
STAGE 09c train_predictor \
    python3 tools/doping/train_predictor.py \
        --csv "$OUT/dataset.csv" \
        --out_dir "$OUT/predictor/" \
        --mode with_structure

# Stage 9d — DFT input generation (Top-10 → KISTI scp)
STAGE 09d dft_inputs \
    python3 tools/doping/generate_dft_inputs.py \
        --ranking "$OUT/FINAL_RANKING.json" \
        --top 10 --out "$OUT/dft_inputs/"

STAGE 09 report \
    python3 -c "
import json
from pathlib import Path
import statistics
out = Path('$OUT')
print('=' * 70)
print('  FINAL REPORT')
print('=' * 70)

# Aggregate everything into one ranking table
recs = {}
for json_path in [out / '02_screen/uma_results.json',
                  out / '03_winners/winners.json',
                  out / '04_bvse/bvs_report.json',
                  out / '05_anneal/anneal_results.json',
                  out / '07_eos/postproc_summary.json',
                  out / '08_elastic/postproc_summary.json']:
    if not json_path.exists():
        print(f'  (missing: {json_path})')
        continue
    d = json.loads(json_path.read_text())
    for r in d.get('records', d.get('winners', d.get('results', []))):
        name = r.get('name', '?')
        if name not in recs:
            recs[name] = {}
        recs[name].update(r)

# Print Top-10 by post-anneal ΔE (if available) else by screen ΔE
def score_key(r):
    if 'E_post_relax' in r and 'n_atoms' in r:
        return r['E_post_relax'] / r['n_atoms']
    if 'uma_relaxed' in r:
        return r['uma_relaxed'].get('de_per_atom_vs_baseline', 0)
    return 0

ranked = sorted(recs.values(), key=score_key)
print(f'Top-20 final winners:')
print(f'{\"Rank\":<5}{\"Name\":<40}{\"ΔE/atom\":>10}{\"V_mig%\":>9}{\"B0 GPa\":>10}{\"Eyoung\":>10}')
for i, r in enumerate(ranked[:20], 1):
    de = r.get('uma_relaxed', {}).get('de_per_atom_vs_baseline', 0)
    vmig = r.get('migration_volume_fraction', 0) * 100
    eos = r.get('eos', {})
    b0 = eos.get('B0_GPa', 0) if isinstance(eos, dict) else 0
    ela = r.get('elastic', {})
    ey = ela.get('E_young_GPa', 0) if isinstance(ela, dict) else 0
    print(f'{i:<5}{r.get(\"name\",\"?\")[:38]:<40}{de:>+9.4f} {vmig:>7.2f}% {b0:>9.2f} {ey:>9.2f}')

(out / 'FINAL_REPORT.json').write_text(json.dumps(list(recs.values()), indent=2, default=str))
print()
print(f'Full report → {out}/FINAL_REPORT.json')
"

LOG "==================================================="
LOG "  ALL STAGES COMPLETE: $OUT"
LOG "==================================================="

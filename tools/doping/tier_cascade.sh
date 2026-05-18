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
# Resolve REPO_ROOT via this script's own location:
#   tools/doping/tier_cascade.sh  → REPO_ROOT/../..
# More robust than walking up from BASE (which lives at varying depths
# depending on the user's cli invocation).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
# v4.5.14: export so child shells (run_compound_batch.sh inline python)
# can locate tools/doping/ for _provenance import.
export REPO_ROOT
cd "$REPO_ROOT"
LOG() { echo "[$(date +%H:%M:%S)] $*" | tee -a "$OUT/cascade.log"; }
LOG "REPO_ROOT resolved to: $REPO_ROOT"
LOG "SCRIPT_DIR:              $SCRIPT_DIR"

# v4.3 fix (CRITICAL-1): VERSION_FILE 없는 case에서 STAGE_*.DONE 마커가
# 이미 있으면 v1 layout일 가능성 → silent corruption 방지. 사용자가
# 명시적으로 `rm -rf $OUT` 하거나 `touch $VERSION_FILE` 하기 전까지 fail.
CASCADE_VERSION=2
VERSION_FILE="$OUT/CASCADE_VERSION"
if [ -f "$VERSION_FILE" ]; then
    actual=$(cat "$VERSION_FILE")
    if [ "$actual" != "$CASCADE_VERSION" ]; then
        echo "ERROR: $OUT was built by cascade v$actual, current script is v$CASCADE_VERSION."
        echo "  Stage layouts differ (v1: 04=bvse, v2: 04=anneal). Resume would corrupt."
        echo "  Either: (a) rm -rf $OUT and rerun, or (b) checkout the matching cascade script version."
        exit 1
    fi
elif ls "$OUT"/STAGE_*.DONE >/dev/null 2>&1; then
    # STAGE markers exist but no CASCADE_VERSION → likely v1 dir.
    # Refuse to silently stamp a wrong version.
    echo "ERROR: $OUT has existing STAGE_*.DONE markers but no CASCADE_VERSION file."
    echo "  This is most likely a v1 cascade output (v1 did not stamp version)."
    echo "  Stage layouts are incompatible between v1 (04=bvse, 05=anneal) and"
    echo "  v$CASCADE_VERSION (04=anneal, 05=bvse). Resume would corrupt results."
    echo "  Either: (a) rm -rf $OUT and rerun, or (b) downgrade cascade script to v1,"
    echo "  or (c) if you know it is safe, manually:  echo 1 > $VERSION_FILE  (NOT recommended)."
    exit 1
else
    echo "$CASCADE_VERSION" > "$VERSION_FILE"
fi
DONE_MARK() { touch "$OUT/STAGE_${1}.DONE"; }
DONE_CHECK() { [ -f "$OUT/STAGE_${1}.DONE" ]; }
STAGE() {
    local id=$1; local name=$2; shift 2
    # M-4 fix: FORCE_RERUN=01 or FORCE_RERUN=all skips the DONE marker.
    # Useful when dev-cycle iterating on a single stage (e.g. preflight)
    # without `rm -rf` of the whole OUT dir.
    if DONE_CHECK "$id" && [ "${FORCE_RERUN:-}" != "$id" ] \
       && [ "${FORCE_RERUN:-}" != "all" ]; then
        LOG "Stage $id ($name): SKIP (already done; FORCE_RERUN=$id to force)"
        return 0
    fi
    # v4.4 fix: warn that re-running a stage does NOT auto-invalidate
    # downstream STAGE_*.DONE markers. If you rerun stage 02 (screen),
    # stage 04 (anneal), 05 (bvse), 06 (rerank), 07 (eos), 08 (elastic),
    # 09 (final report) will still be marked DONE with stale results.
    # The user must manually `rm $OUT/STAGE_{04..09}*.DONE` (or FORCE_RERUN=all).
    if [ "${FORCE_RERUN:-}" = "$id" ] && DONE_CHECK "$id"; then
        LOG "Stage $id ($name): FORCE rerun (⚠ downstream stages NOT auto-invalidated"
        LOG "  — rm \$OUT/STAGE_<later>.DONE manually, or use FORCE_RERUN=all)"
    fi
    LOG "Stage $id ($name): START"
    local t0=$(date +%s)
    "$@" 2>&1 | tee -a "$OUT/logs/${id}_${name}.log"
    local status=${PIPESTATUS[0]}
    local elapsed=$(($(date +%s) - t0))
    if [ $status -eq 0 ]; then
        DONE_MARK "$id"
        LOG "Stage $id ($name): OK (${elapsed}s)"
        # Auto-generate human-readable markdown report
        python3 tools/doping/stage_report.py \
            --cascade_dir "$OUT" --stage "$id" 2>/dev/null || true
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

# Stage 03 — Select per-group winners (only converged + dV < 25%)
STAGE 03 winners \
    python3 tools/doping/select_winners.py \
        --results "$OUT/02_screen/uma_results.json" \
        --out "$OUT/03_winners/winners.json" \
        --group_by dopant site anion_site_label \
        --max_dv 0.25 --require_converged

# Stage 04 — REAL anneal of winners (500K, 50 ps, FIRE relax)
# v4.2 (DEFEND-2 fix): previous --light (300K, 20 ps) was finite-T noise
# injection rather than annealing. At 300K, Li-hop Arrhenius rate × 20 ps
# gives ≈0.008 hop/Li, so Li sublattice barely sampled. Real Pipeline
# Step 3 (kb/methodology/argyrodite_mechanical_pipeline.md) calls for
# 500K @ 50ps where kT/Eₐ ratio is just enough to sample Li hops while
# PS₄ stretching (E_bond≈3.5 eV) and Cl⁻ cage (E_a≈0.4 eV) stay rigid
# on the 50ps timescale. PS₄ rotation barriers (~0.1-0.3 eV per
# D'Amore 2022) ARE thermally accessible at 500K — that's intentional;
# librations average out into a more realistic relaxed geometry. If
# computational budget is tight, pass ANNEAL_MODE=light to fall back
# to the cheap 300K mode.
ANNEAL_FLAGS=""
[ "${ANNEAL_MODE:-real}" = "light" ] && ANNEAL_FLAGS="--light"
STAGE 04 anneal \
    python3 tools/doping/run_anneal.py \
        --summary_json "$OUT/03_winners/winners.json" \
        --out "$OUT/04_anneal" \
        --device cuda $ANNEAL_FLAGS

# Stage 05 — BVSE on post-anneal (relaxed) geometry, not the pre-relax input.
#   External review CR-3: BVS depends exponentially on bond length, so the
#   un-relaxed substitute-compound output gave artificial distances.
STAGE 05 bvse \
    bash -c '
        xyzs=$(ls "'"$OUT"'"/04_anneal/*/post_relax.xyz 2>/dev/null)
        if [ -z "$xyzs" ]; then
            echo "  No post_relax.xyz files; falling back to initial structures"
            xyzs_dir="'"$OUT"'/01_structures/structures"
            python3 tools/doping/bvse_proxy.py \
                --xyz_dir "$xyzs_dir" \
                --out "'"$OUT"'/05_bvse/bvs_report.json" \
                --grid_resolution 25
        else
            python3 tools/doping/bvse_proxy.py \
                --xyz $xyzs \
                --out "'"$OUT"'/05_bvse/bvs_report.json" \
                --grid_resolution 25
        fi
    '

# Stage 06 — Re-rank using post-anneal energies
STAGE 06 rerank \
    python3 tools/doping/rank_anneal.py \
        --screening "$OUT/02_screen/uma_results.json" \
        --anneal "$OUT/04_anneal/anneal_results.json" \
        --out "$OUT/06_rerank/post_anneal_ranking.json" --top 30

# Stage 07 — MLIP EOS (uses POST-ANNEAL xyz so no double-anneal)
#   --no_anneal skips the redundant anneal step inside run_mlip_postproc
STAGE 07 eos \
    python3 tools/doping/run_mlip_postproc.py \
        --xyz $(ls "$OUT"/04_anneal/*/post_relax.xyz 2>/dev/null | tr '\n' ' ') \
        --out "$OUT/07_eos" \
        --no_anneal --no_elastic \
        --device cuda

# Stage 08 — MLIP elastic (clamped-ion Cij at 0K, then VRH average)
STAGE 08 elastic \
    python3 tools/doping/run_mlip_postproc.py \
        --xyz $(ls "$OUT"/04_anneal/*/post_relax.xyz 2>/dev/null | tr '\n' ' ') \
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

# Stage 9e — Synthesizability (convex-hull) hint via Materials Project.
# Skips gracefully if MP_API_KEY not set. Cheap (~30s API calls).
STAGE 09e ehull \
    python3 tools/doping/ehull_check.py \
        --ranking "$OUT/06_rerank/post_anneal_ranking.json" \
        --anneal_dir "$OUT/04_anneal" \
        --out "$OUT/09e_ehull/ehull_summary.json" --top 10

# Stage 9f — Competing-phase energy span (qualitative metastability hint).
# NOT a real ESW — real ESW needs Mo 2012 grand canonical method (TODO v5).
# Report this in paper-SI only, NOT main table, NOT as "ESW".
# Skips gracefully if MP_API_KEY not set.
STAGE 09f esw \
    python3 tools/doping/esw_check.py \
        --ranking "$OUT/06_rerank/post_anneal_ranking.json" \
        --anneal_dir "$OUT/04_anneal" \
        --out "$OUT/09f_esw/esw_summary.json" --top 10

# Stage 10 — σ_Li MD (paper-essential ionic conductivity, top-5 × 3T × 50ps).
# Cost ≈12h on A100. Set TOP_K_SIGMA=0 to skip.
TOP_K_SIGMA="${TOP_K_SIGMA:-5}"
if [ "$TOP_K_SIGMA" != "0" ]; then
    STAGE 10 md_sigma \
        python3 tools/doping/run_md_sigma.py \
            --ranking "$OUT/06_rerank/post_anneal_ranking.json" \
            --anneal_dir "$OUT/04_anneal" \
            --out "$OUT/10_md_sigma" \
            --top "$TOP_K_SIGMA" \
            --temps 600 800 1000 --prod_ps 50
else
    LOG "Stage 10 (md_sigma): SKIP (TOP_K_SIGMA=0)"
fi

# Stage 11 — NCM-doped-SE adhesion v6 (paper composite-cathode application).
# Cost ≈5-15h on A100 depending on baseline count. Per-baseline path;
# missing path → skip that baseline (no fake aliasing).
# Set TOP_K_NCM=0 to skip the whole stage.
#
# Baselines aligned to paper Table 1 (v4.5.3 — full 6-comp experimental matrix):
#   NCM_BASELINE_COMP1   : Li6PS5Cl pristine (cubic, canonical CIF)
#   NCM_BASELINE_COMP2   : Li6PS5Cl0.5Br0.5 mixed halide
#   NCM_BASELINE_COMP3   : Li5.4PS4.4Cl1.0Br0.6 (Cl-rich Li5.4, MLIP-V0)
#   NCM_BASELINE_COMP4   : Li5.4PS4.4Cl0.8Br0.8 (balanced Li5.4, DFT-EOS-validated)
#   NCM_BASELINE_COMP5   : Li5.4PS4.4Cl0.6Br1.0 (Br-rich Li5.4, MLIP-V0)
#   NCM_BASELINE_MODELC  : Li5.4PS4.4Cl1.6 (Cl-only Li5.4, DFT-EOS V0)
# To disable a baseline: NCM_BASELINE_COMP5="" bash tier_cascade.sh ...
TOP_K_NCM="${TOP_K_NCM:-5}"
NCM_BASELINE_COMP1="${NCM_BASELINE_COMP1:-db/structures/lpscl_F43m_24G_canonical.cif}"
NCM_BASELINE_COMP2="${NCM_BASELINE_COMP2:-db/structures/comp2_V0.cif}"
NCM_BASELINE_COMP3="${NCM_BASELINE_COMP3:-db/structures/comp3_v2_V0_UMA.xyz}"
NCM_BASELINE_COMP4="${NCM_BASELINE_COMP4:-db/structures/comp4_v2_V0_UMA.xyz}"
NCM_BASELINE_COMP5="${NCM_BASELINE_COMP5:-db/structures/comp5_v2_V0_UMA.xyz}"
NCM_BASELINE_MODELC="${NCM_BASELINE_MODELC:-db/structures/modelC_DFT_EOS_V0.cif}"
NCM_BASELINE_ARGS=""
for spec in "comp1=$NCM_BASELINE_COMP1" "comp2=$NCM_BASELINE_COMP2" \
            "comp3=$NCM_BASELINE_COMP3" "comp4=$NCM_BASELINE_COMP4" \
            "comp5=$NCM_BASELINE_COMP5" "modelC=$NCM_BASELINE_MODELC"; do
    path="${spec#*=}"
    [ -n "$path" ] && [ -f "$path" ] && NCM_BASELINE_ARGS="$NCM_BASELINE_ARGS $spec"
done
if [ "$TOP_K_NCM" != "0" ] && [ -n "$NCM_BASELINE_ARGS" ]; then
    LOG "Stage 11 baselines:$NCM_BASELINE_ARGS"
    STAGE 11 cathode \
        python3 tools/doping/run_cathode_interface.py \
            --ranking "$OUT/06_rerank/post_anneal_ranking.json" \
            --anneal_dir "$OUT/04_anneal" \
            --baselines $NCM_BASELINE_ARGS \
            --out "$OUT/11_cathode_interface" \
            --top "$TOP_K_NCM" --n_seeds 5
else
    LOG "Stage 11 (cathode): SKIP (TOP_K_NCM=$TOP_K_NCM, baselines=$NCM_BASELINE_ARGS)"
fi

# Stage 12 — Final dataset collect + ML retrain AFTER Stages 10/11.
# (DT-7 fix: Stage 09b/09c above ran before σ_Li MD + Wad, so their
# results were absent from dataset.csv. Stage 12 re-runs collect+train
# now that ALL stages have written output. dataset.csv & predictor/
# are overwritten with the complete data.)
STAGE 12 collect_final \
    python3 tools/doping/collect_dataset.py \
        --cascade_dir "$OUT" \
        --out "$OUT/dataset.csv"
STAGE 12b train_final \
    python3 tools/doping/train_predictor.py \
        --csv "$OUT/dataset.csv" \
        --out_dir "$OUT/predictor/" \
        --mode with_structure

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
                  out / '05_bvse/bvs_report.json',
                  out / '04_anneal/anneal_results.json',
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

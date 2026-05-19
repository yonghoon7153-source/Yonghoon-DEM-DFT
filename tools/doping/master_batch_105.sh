#!/usr/bin/env bash
# master_batch_105.sh — fault-tolerant 105-compound multi-category cascade
#
# Goal: full DOPANT_DB exploration for Layer 2 GNN training data
# (~7,700 datapoints → ALIGNN/M3GNet viable)
#
# Safety features:
#   - set -uo pipefail (NOT -e): one compound failure → continue to next
#   - is_done() resume check: STAGE_12.DONE marker → skip
#   - timeout 86400 (24h) per compound: prevent hang
#   - per-compound logging: $BATCH_DIR/<cmp>.log
#   - master log: $BATCH_DIR/_master_logs/master_<timestamp>.log
#
# Usage (gabia):
#   cd /data/work/repo
#   git pull origin claude/unified-2026-05-15
#   nohup bash tools/doping/master_batch_105.sh \
#       > /data/work/runs/multi_category_2026_05_19_v22/master_outer.log 2>&1 &
#   echo $! > /data/work/runs/multi_category_2026_05_19_v22/master.pid
#
# Resume (after crash or gabia restart):
#   Same command — is_done() auto-skips completed compounds.
#
# Monitor:
#   watch -n 30 'bash tools/doping/watch_phase1_v22.sh'
#
# Estimated: 105 cascades × ~36h (TOP_K_SIGMA=2) ÷ 2 GPU = ~79 days (~11 weeks)

set -uo pipefail

BATCH_DIR="${BATCH_DIR:-/data/work/runs/multi_category_2026_05_19_v22}"
LOG_DIR="$BATCH_DIR/_master_logs"
mkdir -p "$LOG_DIR"
MASTER_LOG="$LOG_DIR/master_$(date +%Y%m%d_%H%M%S).log"

# Cascade environment
export TOP_K_SIGMA="${TOP_K_SIGMA:-2}"
export TOP_K_NCM="${TOP_K_NCM:-3}"

# ============================================================
# 105-compound list (Phase 1A 37 + Phase 1B 64 + Tier D 4)
# Excluded from full DOPANT_DB (5 compounds, chemistry reason):
#   P2S5    — same as host PS4 framework (no-op)
#   Si3N4   — strong covalent network (does not insert)
#   BN      — strong covalent network
#   B2S3    — strong covalent network
#   NaCl, KCl, NaF, NaBr  — alkali halide redundancy (Li-only host)
#   (KBr, CaF2 등 일부 alkali halide도 paper-grade 의미 약함 — Phase 2 deferred)
# ============================================================

# Phase 1A — Oxides (37)
PHASE_1A=(
    # Mono-valent +1 (4)
    Li2O Na2O Cu2O Ag2O
    # Di-valent +2 (8)
    MgO ZnO CaO SrO BaO MnO CoO NiO
    # Tri-valent +3 (12)
    Al2O3 Sc2O3 Y2O3 La2O3 Nd2O3 Sm2O3 Gd2O3 Ga2O3 In2O3 Cr2O3 Fe2O3 B2O3
    # Tetra-valent +4 (6)
    SiO2 GeO2 SnO2 TiO2 ZrO2 HfO2
    # Penta-valent +5 (4)
    V2O5 Nb2O5 Ta2O5 Sb2O5
    # Hexa-valent +6 (3) — high-valence donor (user requested)
    CrO3 MoO3 WO3
)

# Phase 1B — Non-oxides (64)
PHASE_1B=(
    # Fluorides (10) — excluded: NaF for alkali redundancy
    LiF MgF2 CaF2 AlF3 YF3 LaF3 NdF3 ZrF4 TiF4 ScF3
    # Chlorides (19) — excluded: NaCl, KCl
    LiCl MgCl2 CaCl2 SrCl2 BaCl2 AlCl3 GaCl3 FeCl3 CrCl3
    YCl3 LaCl3 NdCl3 SmCl3 ScCl3 ZrCl4 HfCl4 TiCl4 NbCl5 TaCl5
    # Bromides (6) — excluded: NaBr, KBr
    LiBr MgBr2 CaBr2 AlBr3 ZrBr4
    # Iodides (4)
    LiI NaI MgI2 AlI3
    # Nitrides (5) — excluded: Si3N4, BN (covalent), Na3N
    Li3N Mg3N2 Ca3N2 AlN GaN
    # Sulfides (11) — excluded: P2S5 (host), B2S3 (covalent)
    Li2S Na2S MgS CaS Al2S3 Ga2S3 SiS2 GeS2 SnS2 As2S3 Sb2S3
)

# Tier D — Halide-rich Type B (DEFERRED, see note below master loop)
# Paper #1 already provides Cl-rich (modelC) + Br-rich (comp5) anchors.
TIER_D=(Cl Br I F)  # placeholder, NOT executed in current loop

TOTAL_TYPE_A=$((${#PHASE_1A[@]} + ${#PHASE_1B[@]}))
TOTAL_ALL=$TOTAL_TYPE_A  # Tier D deferred → 91 cascades total

# ============================================================
# Helpers
# ============================================================
log_msg() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$MASTER_LOG"
}

is_done() {
    local outdir=$1
    # Cascade complete if either STAGE_12 or STAGE_12b marker present
    [ -f "$outdir/STAGE_12.DONE" ] || [ -f "$outdir/STAGE_12b.DONE" ]
}

# ============================================================
# Main batch loop
# ============================================================

log_msg "=========================================="
log_msg "Master batch v105 START"
log_msg "BATCH_DIR=$BATCH_DIR"
log_msg "Total compounds: Phase 1A=${#PHASE_1A[@]}, Phase 1B=${#PHASE_1B[@]}, Tier D=${#TIER_D[@]}"
log_msg "Grand total: $TOTAL_ALL cascades"
log_msg "TOP_K_SIGMA=$TOP_K_SIGMA, TOP_K_NCM=$TOP_K_NCM"
log_msg "MASTER_LOG=$MASTER_LOG"
log_msg "=========================================="

# Combine Phase 1A + 1B for Type A loop
ALL_TYPE_A=("${PHASE_1A[@]}" "${PHASE_1B[@]}")

for i in "${!ALL_TYPE_A[@]}"; do
    cmp="${ALL_TYPE_A[$i]}"
    step=$((i + 1))
    phase_label="Phase 1A"
    if [ $i -ge ${#PHASE_1A[@]} ]; then
        phase_label="Phase 1B"
    fi

    OUT="$BATCH_DIR/$cmp"
    LOG="$BATCH_DIR/${cmp}.log"

    if is_done "$OUT"; then
        log_msg "Step $step/$TOTAL_ALL: $cmp ($phase_label) SKIP (already done)"
        continue
    fi

    log_msg "Step $step/$TOTAL_ALL: $cmp ($phase_label) START"

    # v4.5.19 fix: COMPOUND_FILTER env var is the proper single-compound mode.
    # Earlier `--compound $cmp --x_compound 0.05` positional args were ignored
    # by tier_cascade.sh and full DOPANT_DB (75+ compounds) enumerated →
    # 5,250 structures (50× over-generation). COMPOUND_FILTER (v4.5.4)
    # natively supported by run_compound_batch.sh restricts to listed compounds.
    timeout 86400 env COMPOUND_FILTER="$cmp" \
        bash tools/doping/tier_cascade.sh \
            db/structures/lpscl_F43m_24G_canonical.cif \
            "$OUT" \
            5 1,1,1 1 \
        > "$LOG" 2>&1

    rc=$?
    if [ $rc -eq 0 ] && is_done "$OUT"; then
        log_msg "Step $step/$TOTAL_ALL: $cmp ✓ DONE"
    elif [ $rc -eq 124 ]; then
        log_msg "Step $step/$TOTAL_ALL: $cmp ⚠ TIMEOUT (24h) → next"
    else
        log_msg "Step $step/$TOTAL_ALL: $cmp ❌ FAIL (rc=$rc) → next (check $LOG)"
    fi
done

# Tier D — halide-rich Type B
# v4.5.19 NOTE: run_compound_batch.sh Type B is "compound-independent" mode
# (runs ONLY when COMPOUND_FILTER unset, AND generates 9 hx × 3 halides = 27
# halide-rich variants). For single halide-rich (e.g., LiCl-rich x=0.6 only),
# we need direct substitute_compound.py call — not yet wired through cascade.
# DEFERRED: Tier D will be handled by separate Phase 2 script after Phase 1A+1B
# completion. Paper #1 already covers Cl-rich (modelC) and Br-rich (comp5).
log_msg "=========================================="
log_msg "Phase 1A + 1B complete. Tier D (halide-rich) DEFERRED."
log_msg "  Reason: run_compound_batch.sh Type B is compound-independent;"
log_msg "  requires direct substitute_compound.py call (Phase 2)."
log_msg "  Paper #1 anchors: modelC (LiCl-rich), comp5 (LiBr-rich)."
log_msg "=========================================="

# Final summary
log_msg "=========================================="
log_msg "Master batch v105 FINISHED at $(date)"
log_msg "Check completion status:"
log_msg "  find $BATCH_DIR -name 'STAGE_12*.DONE' | wc -l"
log_msg "  ls $BATCH_DIR/_master_logs/"
log_msg "=========================================="

# Aggregate dataset from all compounds (unified Layer 2 input)
log_msg "Aggregating unified dataset..."
python3 -c "
import pandas as pd
import glob
csvs = sorted(glob.glob('$BATCH_DIR/*/dataset.csv'))
print(f'Found {len(csvs)} per-compound CSVs')
dfs = []
for c in csvs:
    try:
        df = pd.read_csv(c)
        dfs.append(df)
    except Exception as e:
        print(f'  warn: skip {c}: {e}')
unified = pd.concat(dfs, ignore_index=True)
print(f'Unified: {len(unified)} rows × {len(unified.columns)} cols')
print(f'Unique dopants: {unified[\"dopant\"].nunique()}')
unified.to_csv('$BATCH_DIR/unified_dataset.csv', index=False)
print(f'✓ Saved: $BATCH_DIR/unified_dataset.csv')
" 2>&1 | tee -a "$MASTER_LOG"

log_msg "Done."

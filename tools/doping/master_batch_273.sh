#!/usr/bin/env bash
# master_batch_273.sh — multi-concentration 91-compound batch (v4.5.20)
#
# Goal: comprehensive (compound × concentration) screening for paper-grade
# Layer 2 ML training (concentration-aware features).
#
#   91 compounds × 3 concentrations (2%, 5%, 10%) = 273 cascades
#   Per-cascade ~17h (TOP_K_SIGMA=2, Stage 11 kept)
#   1 GPU sequential: ~193 days (~6.4 months)
#
# Each cascade goes to its own subdirectory:
#   $BATCH_DIR/Li2O_x002/, Li2O_x005/, Li2O_x010/, MgO_x002/, ...
#
# ============================================================
# RESUME / RESTART BEHAVIOR (CRITICAL — read before launching)
# ============================================================
# 1) Per-cascade resume (within a single (compound,conc) cascade):
#    Each stage writes STAGE_NN.DONE marker. If killed mid-cascade,
#    re-running this master script reinvokes tier_cascade.sh, which
#    auto-skips completed STAGE_NN steps and resumes from the next.
#
# 2) Per-master resume (across compounds):
#    is_done() function checks STAGE_12.DONE or STAGE_12b.DONE.
#    Completed (compound,conc) cascades are SKIPPED on re-run.
#    Example: if Li2O_x005 done + Li2O_x010 mid-stage 04 + ... killed,
#    rerunning this script: Li2O_x005 SKIP, Li2O_x010 resumes at Stage 04,
#    continues with x002 (or next), then Na2O, etc.
#
# 3) Safe re-invocation:
#    Same command can be re-run anytime. Idempotent for completed work.
#    No need to track where it stopped — script auto-detects.
#
# 4) FORCE re-run a completed cascade:
#    Option A: Delete its STAGE_12*.DONE marker:
#      rm $BATCH_DIR/Li2O_x005/STAGE_12*.DONE
#    Option B: Delete entire cascade dir (cleanest, full re-do):
#      rm -rf $BATCH_DIR/Li2O_x005
#    Option C: Use tier_cascade.sh's native FORCE_RERUN env var
#      (skips per-stage DONE marker check; see tier_cascade.sh:88-103)
#      FORCE_RERUN=04 means re-run Stage 04 even if marker exists.
#
# 5) Graceful interrupt:
#    Ctrl+C or kill TERM on this master script: current cascade finishes
#    its current stage write, then master exits cleanly.
#    To kill immediately: pkill -9 -f master_batch_273
#    (Mid-stage MD truncation is recoverable by stage-level resume.)
#
# ============================================================
# Safety features
# ============================================================
#   - set -uo pipefail (NOT -e): one cascade failure → continue to next
#   - is_done() resume check: STAGE_12*.DONE marker → skip
#   - timeout 86400 (24h) per cascade
#   - per-cascade log: $BATCH_DIR/<name>.log
#   - master log: $BATCH_DIR/_master_logs/master_273_<timestamp>.log
#   - initial status dump shows existing completed cascades
#
# Usage (gabia):
#   cd /data/work/repo
#   git pull origin claude/unified-2026-05-15
#   nohup bash tools/doping/master_batch_273.sh \
#       > /data/work/runs/multi_category_2026_05_19_v22/master_outer_273.log 2>&1 &
#   echo $! > /data/work/runs/multi_category_2026_05_19_v22/master_273.pid
#
# Resume:
#   Same command — auto-detects and skips completed cascades.
#
# Monitor:
#   bash tools/doping/watch_phase1_v22.sh

set -uo pipefail

BATCH_DIR="${BATCH_DIR:-/data/work/runs/multi_category_2026_05_19_v22}"
LOG_DIR="$BATCH_DIR/_master_logs"
mkdir -p "$LOG_DIR"
MASTER_LOG="$LOG_DIR/master_273_$(date +%Y%m%d_%H%M%S).log"

# Cascade environment defaults (user-configurable via env)
export TOP_K_SIGMA="${TOP_K_SIGMA:-2}"
export TOP_K_NCM="${TOP_K_NCM:-3}"

# ============================================================
# Concentration sweep (v4.5.20)
# ============================================================
# 3 concentrations spanning dilute (2%) → standard (5%) → heavy (10%)
# Matches Xiong 2022 (2%), Sundar 2025 (5%), Adeli 2019 (10%) literature.
# Format: x_compound float value + label for directory name
declare -A CONCENTRATIONS=(
    ["x002"]="0.02"
    ["x005"]="0.05"
    ["x010"]="0.10"
)
CONC_LABELS=(x002 x005 x010)  # ordered iteration

# ============================================================
# 91-compound list (Phase 1A 37 + Phase 1B 54)
# Same as v105 — 5 alkali halide + 4 covalent + RE/TM sulfide + polyanion excluded
# ============================================================
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
    # Hexa-valent +6 (3)
    CrO3 MoO3 WO3
)

PHASE_1B=(
    # Fluorides (10)
    LiF MgF2 CaF2 AlF3 YF3 LaF3 NdF3 ZrF4 TiF4 ScF3
    # Chlorides (19)
    LiCl MgCl2 CaCl2 SrCl2 BaCl2 AlCl3 GaCl3 FeCl3 CrCl3
    YCl3 LaCl3 NdCl3 SmCl3 ScCl3 ZrCl4 HfCl4 TiCl4 NbCl5 TaCl5
    # Bromides (5)
    LiBr MgBr2 CaBr2 AlBr3 ZrBr4
    # Iodides (4)
    LiI NaI MgI2 AlI3
    # Nitrides (5)
    Li3N Mg3N2 Ca3N2 AlN GaN
    # Sulfides (11)
    Li2S Na2S MgS CaS Al2S3 Ga2S3 SiS2 GeS2 SnS2 As2S3 Sb2S3
)

ALL_COMPOUNDS=("${PHASE_1A[@]}" "${PHASE_1B[@]}")
N_COMPOUNDS=${#ALL_COMPOUNDS[@]}
N_CONCS=${#CONC_LABELS[@]}
TOTAL_CASCADES=$((N_COMPOUNDS * N_CONCS))

# ============================================================
# Helpers
# ============================================================
log_msg() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$MASTER_LOG"
}

# v4.5.22 — multi-trigger skip detection (5-layer):
#   1. STAGE_12*.DONE marker (cascade fully complete)
#   2. Symlink target check (Li2O_x005 → Li2O which is done)
#   3. Recent activity (file modified in last 30 min → cascade still running)
#   4. Explicit lock file ($OUT/.master_lock with PID)
#   5. External cascade PID file ($OUT.pid from prior independent run)
# Returns: "done" / "running" / "locked" / "pending" (printed to stdout)
cascade_status() {
    local outdir=$1

    # Layer 1: STAGE_12 marker = done
    if [ -f "$outdir/STAGE_12.DONE" ] || [ -f "$outdir/STAGE_12b.DONE" ]; then
        echo "done"; return
    fi

    # Layer 2: symlink target check (e.g., Li2O_x005 → Li2O)
    if [ -L "$outdir" ]; then
        local target=$(readlink -f "$outdir")
        if [ -f "$target/STAGE_12.DONE" ] || [ -f "$target/STAGE_12b.DONE" ]; then
            echo "done-via-symlink"; return
        fi
    fi

    # Layer 3: recent activity (file modified in last 30 min)
    # If cascade currently running (own process or external), files actively writing.
    if [ -d "$outdir" ]; then
        local recent=$(find "$outdir" -type f -mmin -30 2>/dev/null | head -1)
        if [ -n "$recent" ]; then
            echo "running"; return
        fi
    fi

    # Layer 4: explicit lock file (master writes own PID)
    if [ -f "$outdir/.master_lock" ]; then
        local lock_pid=$(cat "$outdir/.master_lock" 2>/dev/null)
        if [ -n "$lock_pid" ] && kill -0 "$lock_pid" 2>/dev/null; then
            echo "locked"; return
        fi
        # stale lock — remove and continue
        rm -f "$outdir/.master_lock"
    fi

    # Layer 5: external PID file ($BATCH_DIR/<name>.pid from independent run)
    local ext_pid_file="${outdir%.pid}.pid"
    if [ -f "$ext_pid_file" ]; then
        local ext_pid=$(cat "$ext_pid_file" 2>/dev/null)
        if [ -n "$ext_pid" ] && kill -0 "$ext_pid" 2>/dev/null; then
            echo "external"; return
        fi
    fi

    echo "pending"
}

# Backward-compat wrapper (existing callers use is_done)
is_done() {
    local s=$(cascade_status "$1")
    [ "$s" = "done" ] || [ "$s" = "done-via-symlink" ]
}

# ============================================================
# Main batch loop — (compound, concentration) pairs
# ============================================================

log_msg "=========================================="
log_msg "Master batch v273 START (v4.5.20 multi-concentration)"
log_msg "BATCH_DIR=$BATCH_DIR"
log_msg "Phase 1A: ${#PHASE_1A[@]} compounds"
log_msg "Phase 1B: ${#PHASE_1B[@]} compounds"
log_msg "Concentrations: ${CONC_LABELS[*]} = (${CONCENTRATIONS[x002]}, ${CONCENTRATIONS[x005]}, ${CONCENTRATIONS[x010]})"
log_msg "Total cascades: $TOTAL_CASCADES (= $N_COMPOUNDS compounds × $N_CONCS concs)"
log_msg "TOP_K_SIGMA=$TOP_K_SIGMA, TOP_K_NCM=$TOP_K_NCM"
log_msg "Estimated time: ~$((TOTAL_CASCADES * 17 / 24)) days (TOP_K_SIGMA=2, 1 GPU)"
log_msg "MASTER_LOG=$MASTER_LOG"

# ============================================================
# Resume status dump (v4.5.22 — 5-trigger detection)
# ============================================================
log_msg ""
log_msg "--- Resume status (pre-launch scan, v4.5.22 5-trigger) ---"
declare -A status_count=( [done]=0 [done-via-symlink]=0 [running]=0 \
                          [locked]=0 [external]=0 [pending]=0 [partial]=0 )
for cmp in "${ALL_COMPOUNDS[@]}"; do
    for conc_label in "${CONC_LABELS[@]}"; do
        cmp_label="${cmp}_${conc_label}"
        OUT="$BATCH_DIR/$cmp_label"
        st=$(cascade_status "$OUT")
        if [ "$st" = "pending" ] && [ -d "$OUT" ]; then
            # pending but dir exists → partial cascade
            last_stage=$(ls -t "$OUT"/STAGE_*.DONE 2>/dev/null | head -1 \
                          | xargs basename 2>/dev/null | cut -d. -f1)
            if [ -n "$last_stage" ]; then
                st="partial"
                log_msg "  PARTIAL: $cmp_label (last=$last_stage) → will resume"
            fi
        elif [ "$st" = "running" ] || [ "$st" = "locked" ] || [ "$st" = "external" ]; then
            log_msg "  $st: $cmp_label → will SKIP this iteration"
        elif [ "$st" = "done-via-symlink" ]; then
            target=$(readlink -f "$OUT")
            log_msg "  done-via-symlink: $cmp_label → $target"
        fi
        status_count[$st]=$((${status_count[$st]:-0} + 1))
    done
done
log_msg ""
log_msg "  Summary by trigger:"
log_msg "    done            : ${status_count[done]:-0}  (STAGE_12 marker)"
log_msg "    done-via-symlink: ${status_count[done-via-symlink]:-0}  (symlink target has STAGE_12)"
log_msg "    running         : ${status_count[running]:-0}  (recent file activity, <30min)"
log_msg "    locked          : ${status_count[locked]:-0}  (.master_lock with alive PID)"
log_msg "    external        : ${status_count[external]:-0}  (<dir>.pid alive external process)"
log_msg "    partial         : ${status_count[partial]:-0}  (will resume from last STAGE)"
log_msg "    pending         : ${status_count[pending]:-0}  (fresh start)"
n_already_done=$((${status_count[done]:-0} + ${status_count[done-via-symlink]:-0}))
n_skip_active=$((${status_count[running]:-0} + ${status_count[locked]:-0} + ${status_count[external]:-0}))
n_partial=${status_count[partial]:-0}
n_pending=${status_count[pending]:-0}
log_msg ""
log_msg "  Will SKIP   : $((n_already_done + n_skip_active)) ($n_already_done done + $n_skip_active active)"
log_msg "  Will RESUME : $n_partial"
log_msg "  Will START  : $n_pending"
if [ "$n_already_done" -gt 0 ] || [ "$n_partial" -gt 0 ]; then
    remaining_h=$(( (n_pending + n_partial) * 17 ))
    remaining_d=$((remaining_h / 24))
    log_msg "  Remaining time estimate: ~$remaining_d days"
else
    log_msg "  (fresh start — no prior cascade outputs detected)"
fi
log_msg "=========================================="

cascade_step=0
for i in "${!ALL_COMPOUNDS[@]}"; do
    cmp="${ALL_COMPOUNDS[$i]}"
    phase_label="Phase 1A"
    if [ $i -ge ${#PHASE_1A[@]} ]; then
        phase_label="Phase 1B"
    fi

    for conc_label in "${CONC_LABELS[@]}"; do
        cascade_step=$((cascade_step + 1))
        x_val="${CONCENTRATIONS[$conc_label]}"
        cmp_label="${cmp}_${conc_label}"   # e.g., Li2O_x005

        OUT="$BATCH_DIR/$cmp_label"
        LOG="$BATCH_DIR/${cmp_label}.log"

        # v4.5.22: 5-trigger skip detection
        st=$(cascade_status "$OUT")
        case "$st" in
            done|done-via-symlink)
                log_msg "Step $cascade_step/$TOTAL_CASCADES: $cmp_label SKIP (status=$st)"
                continue
                ;;
            running|locked|external)
                log_msg "Step $cascade_step/$TOTAL_CASCADES: $cmp_label SKIP (status=$st — active)"
                log_msg "  → will retry on next master_batch invocation"
                continue
                ;;
            # pending or partial → run cascade (tier_cascade internal resume handles partial)
        esac

        log_msg "Step $cascade_step/$TOTAL_CASCADES: $cmp_label ($phase_label, x=$x_val) START"

        # Write .master_lock with current master PID for cross-instance coordination
        mkdir -p "$OUT"
        echo "$$" > "$OUT/.master_lock"

        # Run cascade with 24h timeout
        # COMPOUND_FILTER=<cmp> restricts substitute to single compound (v4.5.19 fix)
        # X_COMPOUND=<x_val>   sets doping concentration (v4.5.20 new env var)
        timeout 86400 env \
            COMPOUND_FILTER="$cmp" \
            X_COMPOUND="$x_val" \
            bash tools/doping/tier_cascade.sh \
                db/structures/lpscl_F43m_24G_canonical.cif \
                "$OUT" \
                5 1,1,1 1 \
            > "$LOG" 2>&1

        rc=$?
        if [ $rc -eq 0 ] && is_done "$OUT"; then
            log_msg "Step $cascade_step/$TOTAL_CASCADES: $cmp_label ✓ DONE"
        elif [ $rc -eq 124 ]; then
            log_msg "Step $cascade_step/$TOTAL_CASCADES: $cmp_label ⚠ TIMEOUT (24h) → next"
        else
            log_msg "Step $cascade_step/$TOTAL_CASCADES: $cmp_label ❌ FAIL (rc=$rc) → next (check $LOG)"
        fi
    done
done

# ============================================================
# Final summary + dataset aggregation
# ============================================================
log_msg "=========================================="
log_msg "Master batch v273 FINISHED at $(date)"
log_msg "Completion summary:"
n_done=$(find "$BATCH_DIR" -maxdepth 2 -name 'STAGE_12*.DONE' 2>/dev/null | wc -l)
log_msg "  $n_done / $TOTAL_CASCADES cascades complete"
log_msg "  Master log: $MASTER_LOG"
log_msg "=========================================="

# Aggregate unified dataset from all (compound × conc) cascades
log_msg "Aggregating unified dataset (concentration-aware)..."
python3 -c "
import pandas as pd
import glob
import json
import os
csvs = sorted(glob.glob('$BATCH_DIR/*/dataset.csv'))
print(f'Found {len(csvs)} per-cascade CSVs')
dfs = []
for c in csvs:
    try:
        df = pd.read_csv(c)
        # Extract compound + concentration from parent dir name (e.g., Li2O_x005)
        parent = os.path.basename(os.path.dirname(c))
        if '_x' in parent:
            cmp, conc_label = parent.rsplit('_x', 1)
            df['compound_id'] = cmp
            df['concentration_label'] = 'x' + conc_label
            # v4.5.21 NEW-F fix (Round 6 reviewer CRITICAL):
            # master_batch_273 label convention: x002=2%, x005=5%, x010=10%
            # (label digits = percent value). Previous v4.5.20 used
            # `int(conc_label) / 10` which gave 0.2/0.5/1.0 (1/10 off) —
            # silent unit mismatch with column name "pct" (= percent).
            # Both columns reported for paper-grade unit clarity:
            df['concentration_pct'] = float(conc_label)        # 2.0 / 5.0 / 10.0  (percent)
            df['concentration_fraction'] = float(conc_label) / 100  # 0.02 / 0.05 / 0.10  (fraction)
        else:
            df['compound_id'] = parent
            df['concentration_label'] = 'unknown'
            df['concentration_pct'] = None
            df['concentration_fraction'] = None
        dfs.append(df)
    except Exception as e:
        print(f'  warn: skip {c}: {e}')

if dfs:
    unified = pd.concat(dfs, ignore_index=True)
    print(f'Unified: {len(unified)} rows × {len(unified.columns)} cols')
    print(f'Unique compounds: {unified[\"compound_id\"].nunique() if \"compound_id\" in unified.columns else \"?\"}')
    print(f'Unique concentrations: {sorted(unified[\"concentration_label\"].unique()) if \"concentration_label\" in unified.columns else \"?\"}')
    out_path = '$BATCH_DIR/unified_dataset_273.csv'
    unified.to_csv(out_path, index=False)
    print(f'✓ Saved: {out_path}')
else:
    print('No CSV data to aggregate.')
" 2>&1 | tee -a "$MASTER_LOG"

log_msg "Done."

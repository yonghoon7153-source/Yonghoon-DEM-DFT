#!/usr/bin/env bash
# run_lpscl16_full.sh — full LPSCl1.6 (= modelC family) champion re-verification.
#
# Pipeline (3 stages, ~22h total on 1× A100):
#   Stage 1  step1: 45 halogen × LBFGS + top 5 × 20 Li LBFGS + Rank 0 anneal (100ps)
#   Stage 2  step2: ranks 1-4 anneal (100ps each, UNIFIED with step1)
#   Stage 3  step3: 20 random Li perturbation robustness check on champion
#
# Output: lpscl16_results.json + lpscl16_champion.xyz + lpscl16_robustness.json
#
# Usage (gabia):
#   export LPSCL16_REF_CIF=/data/work/db/structures/lpscl_F43m_24G_canonical.cif  # or local CIF
#   bash 필독/step1_halogen_li_anneal/lpscl16/run_lpscl16_full.sh /data/work/runs/lpscl16_verify_$(date +%Y%m%d)
#
# Resume after crash:
#   STAGE_NN.DONE markers in $OUT skip completed phases. Re-run same command.

set -uo pipefail

OUT="${1:?usage: $0 <output_dir>}"
REPO="${REPO:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)}"
SCRIPT_DIR="$REPO/필독/step1_halogen_li_anneal/lpscl16"

mkdir -p "$OUT"
cd "$OUT"
LOG() { echo "[$(date '+%H:%M:%S')] $*" | tee -a "$OUT/lpscl16_run.log"; }

LOG "=========================================="
LOG "LPSCl1.6 champion re-verification"
LOG "OUT=$OUT"
LOG "REPO=$REPO"
LOG "LPSCL16_REF_CIF=${LPSCL16_REF_CIF:-(unset → KISTI default)}"
LOG "=========================================="

# Stage 1
if [ -f "$OUT/STAGE_1.DONE" ]; then
    LOG "Stage 1 already done — skip"
else
    LOG "Stage 1: halogen screen + Li screen + Rank 0 anneal (100ps)"
    python3 "$SCRIPT_DIR/lpscl16_step1_screen_anneal_top1.py" 2>&1 | tee -a "$OUT/step1.log"
    if [ -f "$OUT/modelC_v2_champion.xyz" ] || [ -f "$OUT/lpscl16_champion.xyz" ]; then
        # step1 writes 'modelC_v2_champion.xyz'; symlink for clarity
        [ -f "$OUT/modelC_v2_champion.xyz" ] && \
            ln -sf modelC_v2_champion.xyz lpscl16_champion.xyz
        touch "$OUT/STAGE_1.DONE"
        LOG "Stage 1 ✓ DONE"
    else
        LOG "Stage 1 ❌ champion xyz not produced — abort"
        exit 1
    fi
fi

# Stage 2
if [ -f "$OUT/STAGE_2.DONE" ]; then
    LOG "Stage 2 already done — skip"
else
    LOG "Stage 2: ranks 1-4 anneal (100ps each, ~4× cost of step1 anneal phase)"
    python3 "$SCRIPT_DIR/lpscl16_step2_anneal_ranks1to4.py" 2>&1 | tee -a "$OUT/step2.log"
    touch "$OUT/STAGE_2.DONE"
    LOG "Stage 2 ✓ DONE"
fi

# After step2, re-check which rank is the actual champion (results.json updated)
if [ -f "$OUT/modelC_v2_results.json" ]; then
    python3 -c "
import json
d = json.load(open('$OUT/modelC_v2_results.json'))
anneal = sorted(d['anneal'], key=lambda x: x['e_after'])
top = anneal[0]
print(f'Post-step2 champion: rank {top[\"rank\"]} (Li{top[\"li_trial\"]}) E={top[\"e_after\"]:.4f} eV')
# If a non-Rank-0 won, update champion symlink
import os, shutil
src = f'modelC_v2_anneal_rank{top[\"rank\"]}.xyz' if top['rank'] > 0 else 'modelC_v2_champion.xyz'
if top['rank'] > 0 and os.path.exists(src):
    if os.path.islink('lpscl16_champion.xyz') or os.path.exists('lpscl16_champion.xyz'):
        os.remove('lpscl16_champion.xyz') if not os.path.islink('lpscl16_champion.xyz') else os.unlink('lpscl16_champion.xyz')
    os.symlink(src, 'lpscl16_champion.xyz')
    print(f'  champion symlink updated → {src}')
"
fi

# Stage 3
if [ -f "$OUT/STAGE_3.DONE" ]; then
    LOG "Stage 3 already done — skip"
else
    LOG "Stage 3: 20 random Li perturbation robustness check"
    python3 "$SCRIPT_DIR/lpscl16_step3_robustness_perturb.py" \
        --champion lpscl16_champion.xyz \
        --out_json lpscl16_robustness.json 2>&1 | tee -a "$OUT/step3.log"
    touch "$OUT/STAGE_3.DONE"
    LOG "Stage 3 ✓ DONE"
fi

# Summary
LOG "=========================================="
LOG "LPSCl1.6 verification COMPLETE"
LOG "  champion xyz : $OUT/lpscl16_champion.xyz"
LOG "  anneal JSON  : $OUT/modelC_v2_results.json"
LOG "  robustness   : $OUT/lpscl16_robustness.json"
LOG ""
LOG "Next: copy lpscl16_champion.xyz + modelC_v2_results.json + lpscl16_robustness.json"
LOG "      back to repo (db/structures/) for traceability commit."
LOG "=========================================="

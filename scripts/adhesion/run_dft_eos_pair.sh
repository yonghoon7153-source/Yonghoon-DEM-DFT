#!/bin/bash
# run_dft_eos_pair.sh — DFT EOS sweep for a single pair (Nd-doped LPSCl)
# Usage:
#   ./run_dft_eos_pair.sh <pair_dir> <prefix> [GPU_ID]
# Example:
#   ./run_dft_eos_pair.sh pair01_pair_00_reference_1_82 nd_pair01 0
#
# Auto-restart pattern: re-run script to resume from checkpoint.
# Based on comp5_lpscbr/run_dft_eos.sh template.

set -e

PAIR_DIR="$1"
PREFIX="$2"
GPU_ID="${3:-0}"

if [ -z "$PAIR_DIR" ] || [ -z "$PREFIX" ]; then
    echo "Usage: $0 <pair_dir> <prefix> [GPU_ID]"
    echo "Example: $0 pair01_pair_00_reference_1_82 nd_pair01 0"
    exit 1
fi

QE=/scratch/x3430a02/kgy/apps/qe-gpu/bin/pw.x
export CUDA_VISIBLE_DEVICES=$GPU_ID

# Priority order: v100 first (reference), then expand outward
ALL_VOLS="100 102 098 104 096 106 094"

cd "$PAIR_DIR"
echo "[$(date +%H:%M:%S)] === DFT EOS: $PAIR_DIR (GPU $GPU_ID) ==="
echo "[$(date +%H:%M:%S)] Prefix: $PREFIX"
echo "[$(date +%H:%M:%S)] Volumes: $ALL_VOLS"

for vpct in $ALL_VOLS; do
    VOL="v${vpct}"
    DIR="$VOL"
    if [ ! -d "$DIR" ]; then
        echo "[$(date +%H:%M:%S)] [$VOL] no directory — skip"
        continue
    fi
    cd "$DIR"
    mkdir -p tmp

    # BFGS converged check
    if [ -f relax.out ] && grep -qE "bfgs converged in|End of BFGS Geometry" relax.out 2>/dev/null; then
        E=$(grep "!" relax.out | tail -1 | awk '{print $5}')
        echo "[$(date +%H:%M:%S)] [$VOL] DONE (E=$E Ry) — skip"
        cd ..
        continue
    fi

    # Restart logic
    SAVE_DIR="tmp/${PREFIX}_${VOL}.save"
    if [ -d "$SAVE_DIR" ] && [ -f "$SAVE_DIR/charge-density.dat" ]; then
        sed -i "/restart_mode/d" relax.in
        sed -i "/calculation/a\\    restart_mode = 'restart'" relax.in
        echo "[$(date +%H:%M:%S)] [$VOL] Restart from checkpoint..."
    else
        sed -i "/restart_mode/d" relax.in
        echo "[$(date +%H:%M:%S)] [$VOL] Fresh start..."
    fi

    T0=$(date +%s)
    $QE -input relax.in > relax.out 2>&1
    T1=$(date +%s)
    DT=$((T1-T0))

    if grep -qE "bfgs converged in|End of BFGS Geometry" relax.out; then
        E=$(grep "!" relax.out | tail -1 | awk '{print $5}')
        echo "[$(date +%H:%M:%S)] [$VOL] BFGS CONVERGED (E=$E Ry, ${DT}s) ✓"
    else
        echo "[$(date +%H:%M:%S)] [$VOL] INCOMPLETE (${DT}s) — re-run to resume"
    fi
    cd ..
done

# Summary
echo ""
echo "===== EOS SUMMARY: $PAIR_DIR ====="
DONE=0
TOTAL=0
for vpct in $ALL_VOLS; do
    VOL="v${vpct}"
    OUT="$VOL/relax.out"
    TOTAL=$((TOTAL+1))
    if [ -f "$OUT" ] && grep -qE "bfgs converged in|End of BFGS Geometry" "$OUT" 2>/dev/null; then
        E=$(grep "!" "$OUT" | tail -1 | awk '{print $5}')
        echo "  $VOL: E=$E Ry  ✓"
        DONE=$((DONE+1))
    else
        echo "  $VOL: INCOMPLETE  ✗"
    fi
done
echo "===== $DONE/$TOTAL DONE ====="

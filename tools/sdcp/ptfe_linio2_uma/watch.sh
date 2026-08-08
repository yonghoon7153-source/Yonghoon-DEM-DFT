#!/usr/bin/env bash
set -u

PACKAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_COMMIT="UNRECORDED"
if [[ -s "$PACKAGE_DIR/PACKAGE_COMMIT.txt" ]]; then
  IFS= read -r PACKAGE_COMMIT < "$PACKAGE_DIR/PACKAGE_COMMIT.txt"
fi
PACKAGE_TAG="${PACKAGE_COMMIT:0:12}"
[[ "$PACKAGE_COMMIT" == "UNRECORDED" ]] && PACKAGE_TAG="unrecorded"
OUT="${OUT:-/data/work/runs/ptfe_linio2_uma_2026_08_08_${PACKAGE_TAG}}"
UMA_MODEL="${UMA_MODEL:-uma-s-1p1}"
UMA_TASK="${UMA_TASK:-oc20}"
RUN_OUT="$OUT/${UMA_MODEL}_${UMA_TASK}"

rigid=0
relaxed=0
[[ -d "$RUN_OUT/rigid_records" ]] && rigid="$(find "$RUN_OUT/rigid_records" -maxdepth 1 -name '*.json' | wc -l)"
[[ -d "$RUN_OUT/relaxed_records" ]] && relaxed="$(find "$RUN_OUT/relaxed_records" -maxdepth 1 -name '*.json' | wc -l)"

echo "PTFE/LiNiO2 UMA | $(date '+%Y-%m-%d %H:%M:%S')"
echo "model/task: $UMA_MODEL / $UMA_TASK"
echo "rigid: $rigid / 147 | relaxed: $relaxed / 20"
echo "processes:"
pgrep -af '[p]ython.*ptfe_linio2_uma.*/scan\.py' || echo "  none"
echo "GPU:"
nvidia-smi --query-gpu=name,memory.used,utilization.gpu --format=csv,noheader 2>/dev/null || true

if [[ -s "$OUT/logs/screen.log" ]]; then
  echo "--- screen.log tail ---"
  tail -n 20 "$OUT/logs/screen.log" | grep -a '.' || true
elif [[ -s "$OUT/logs/pilot.log" ]]; then
  echo "--- pilot.log tail ---"
  tail -n 20 "$OUT/logs/pilot.log" | grep -a '.' || true
fi

if [[ -s "$RUN_OUT/RESULTS.md" ]]; then
  echo "--- RESULTS.md ---"
  sed -n '1,80p' "$RUN_OUT/RESULTS.md"
fi

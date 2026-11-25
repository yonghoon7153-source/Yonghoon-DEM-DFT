#!/usr/bin/env bash
# UMA-MLIP Arrhenius MD for the B2O3-doped champion (b2o3_relaxV0).
# Ordered champion only (disorder_levels=0.0, 1 config) -> Ea, D0, D(300K), sigma.
# Venue-agnostic: works on gabia or KISTI. ACTIVATE the UMA conda env FIRST
# (e.g. `conda activate uma`), then run this. Launches DETACHED so it survives
# an SSH broken pipe; tail the log to watch.
#
#   bash tools/modelc_v3/run_b2o3_md.sh [OUT_ROOT] [DEVICE]
#     OUT_ROOT  default: runs/b2o3_md   DEVICE  default: cuda
#     env: PROD_PS (default 200) · SEED (default 1234) · FIT_LO/FIT_HI (default 2 50)
#
# ⛔⛔ 2026-09-08 — this runner used to pass NONE of the four flags below. It got
#   whatever the driver's argparse defaults were, which at the time were
#   `--fit_window_ps 5 40` and no `--save_traj`. So:
#     · the D it produced was fitted on a 5-40 ps window, NOT the canonical 2-50
#     · prod was 50 ps, not the canonical 200 ps
#     · no frames were kept, so nothing from this runner can be re-measured
#       (that is exactly how 12 runs in 2026-07 and 21 runs in 2026-08 were lost)
#     · no seed was fixed, so "same conditions" reruns were not the same run
#   ★ The rule: this script now spells out every convention it depends on.
#     Do not go back to relying on driver defaults — a default is not a record.
#   ⚠ Any b2o3 D that came out of the old form of this script carries a 5-40 ps
#     window. Check the window before comparing it with 2-50 ps numbers.
set -euo pipefail
set +H
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO"
OUT_ROOT="${1:-runs/b2o3_md}"
DEVICE="${2:-cuda}"
PROD_PS="${PROD_PS:-200}"       # CLAUDE.md: prod 200 ps (was 50 — screening only)
SEED="${SEED:-1234}"
FIT_LO="${FIT_LO:-2}"; FIT_HI="${FIT_HI:-50}"   # CLAUDE.md: MSD window 2-50 ps
XYZ="db/structures/b2o3_relaxV0.xyz"
LOG="$OUT_ROOT/b2o3_md.log"
mkdir -p "$OUT_ROOT"

# MPI/conda hygiene that bit us before (QE leftovers can poison the python env)
unset LD_LIBRARY_PATH OPAL_PREFIX 2>/dev/null || true

echo "repo=$REPO  xyz=$XYZ  out=$OUT_ROOT  device=$DEVICE  python=$(command -v python3)"
echo "conventions: prod=${PROD_PS} ps · MSD window=${FIT_LO}-${FIT_HI} ps · seed=${SEED} · save_traj=on"
test -f "$XYZ" || { echo "MISSING $XYZ — run from a clean git pull"; exit 1; }

# ⛔ 창을 안 적고 시작하지 않는다 (2026-09-08). 정본이 아닌 창으로는 아예 안 던진다 —
#   나중에 "이 D 는 어느 창이었나" 를 묻게 되는 것이 이 캠페인에서 제일 비쌌다.
[ "$FIT_LO" = "2" ] && [ "$FIT_HI" = "50" ] || {
  echo "⛔ MSD 창이 정본(2-50 ps)이 아니다: ${FIT_LO}-${FIT_HI}"
  echo "   진단 목적이면 FORCE_WINDOW=1 로 명시해라 (그 산출물은 인용 불가)"
  [ "${FORCE_WINDOW:-0}" = 1 ] || exit 2; }

setsid bash -c "
  cd '$REPO'
  python3 tools/modelc_v3/disorder_ensemble_diffusion.py \
    --v0_xyz '$XYZ' --label b2o3 --out_root '$OUT_ROOT' \
    --disorder_levels 0.0 --n_configs 1 \
    --temperatures 600 800 1000 --equilib_ps 5 --prod_ps '$PROD_PS' \
    --save_fs 100 --fit_window_ps '$FIT_LO' '$FIT_HI' --seed '$SEED' --save_traj \
    --device '$DEVICE'
" < /dev/null > "$LOG" 2>&1 &
PID=$!
echo "launched PID=$PID  log=$LOG"
echo "watch:  tail -f $LOG    |  result: $OUT_ROOT/ensemble_results.json"

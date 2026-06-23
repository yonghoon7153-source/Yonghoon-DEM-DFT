#!/usr/bin/env bash
# [서버에서 실행] 같은 물리/메시에 솔버만 다른 두 모델(CPU vs GPU)을 실행해 비교.
#   - CPU 모델: SOLVER=mumps/pardiso, USE_GPU=false
#   - GPU 모델: SOLVER=cudss,         USE_GPU=true
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
. "$HERE/lib/common.sh"

usage(){ cat <<'EOF'
사용법: benchmark.sh --cpu <cpu-model> --gpu <gpu-model> [--name <라벨>]
예:
  bash scripts/benchmark.sh --cpu lpscl_3d_bulk_cpu --gpu lpscl_3d_bulk
결과: benchmarks/<라벨>.csv 에 CPU/GPU 행 + speedup 출력
EOF
}
CPU_MODEL=""; GPU_MODEL=""; NAME=""
while [ $# -gt 0 ]; do
  case "$1" in
    --cpu)  CPU_MODEL="${2:?}"; shift 2;;
    --gpu)  GPU_MODEL="${2:?}"; shift 2;;
    --name) NAME="${2:?}"; shift 2;;
    -h|--help) usage; exit 0;;
    *) die "알 수 없는 인자: $1";;
  esac
done
[ -n "$CPU_MODEL" ] && [ -n "$GPU_MODEL" ] || { usage; exit 1; }
: "${NAME:=${GPU_MODEL}_vs_${CPU_MODEL}}"

mkdir -p "$BENCH_DIR"
csv="$BENCH_DIR/${NAME}.csv"

log_info "===== [1/2] CPU 실행: $CPU_MODEL ====="
bash "$HERE/run.sh" "$CPU_MODEL" || log_warn "CPU 실행이 0이 아닌 코드로 종료됨"

log_info "===== [2/2] GPU 실행: $GPU_MODEL ====="
bash "$HERE/run.sh" "$GPU_MODEL" || log_warn "GPU 실행이 0이 아닌 코드로 종료됨"

require_cmd python3
python3 "$HERE/parse_log.py" --summarize-bench \
  --cpu-model "$CPU_MODEL" --gpu-model "$GPU_MODEL" \
  --results "$RESULTS_DIR" --csv "$csv" --name "$NAME"

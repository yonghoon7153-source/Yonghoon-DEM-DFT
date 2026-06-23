#!/usr/bin/env bash
# [서버에서 실행] 모델 1개를 COMSOL batch로 실행. GPU 사용 여부는 실측/로그로 검증.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
. "$HERE/lib/common.sh"

usage(){ cat <<'EOF'
사용법: run.sh <model-name> [-- <추가 comsol batch 플래그...>]
  <model-name> : config/models/<name>.env 의 이름
예:
  bash scripts/run.sh lpscl_3d_bulk
  bash scripts/run.sh lpscl_3d_bulk -- -mpmode owner
EOF
}
[ $# -ge 1 ] || { usage; exit 1; }
case "$1" in -h|--help) usage; exit 0;; esac
MODEL="$1"; shift || true
PASS_EXTRA=()
if [ "${1:-}" = "--" ]; then shift; PASS_EXTRA=("$@"); fi

load_server_env
load_model_env "$MODEL"
comsol_bin="$(find_comsol)" || die "comsol 바이너리 못 찾음 (config/server.env의 COMSOL_BIN 확인)"

ts="$(date +%Y%m%d_%H%M%S)"
outdir="$RESULTS_DIR/$MODEL/$ts"
mkdir -p "$outdir"
outmph="$outdir/${MODEL}_solved.mph"
logf="$outdir/batchlog.txt"
gpulog="$outdir/nvidia-smi.csv"

log_info "모델       : $MODEL  ${NOTES:+($NOTES)}"
log_info "입력 mph   : $MPH_FILE"
log_info "study      : ${STUDY:-(모델 기본)}"
log_info "솔버(라벨) : ${SOLVER:-?}    USE_GPU=$USE_GPU    NP=$NP"
log_info "출력       : $outdir"

# --- GPU 사용 실측 샘플러 (백그라운드) ---
gpu_sampler_pid=""
if command -v nvidia-smi >/dev/null 2>&1; then
  echo "timestamp,gpu_util_%,mem_used_MiB,mem_total_MiB" > "$gpulog"
  ( while true; do
      nvidia-smi --query-gpu=timestamp,utilization.gpu,memory.used,memory.total \
        --format=csv,noheader,nounits >> "$gpulog" 2>/dev/null || break
      sleep 2
    done ) & gpu_sampler_pid=$!
fi
cleanup(){ [ -n "$gpu_sampler_pid" ] && kill "$gpu_sampler_pid" 2>/dev/null || true; }
trap cleanup EXIT

# --- comsol batch 명령 구성 ---
cmd=( "$comsol_bin" batch
      -inputfile  "$MPH_FILE"
      -outputfile "$outmph"
      -batchlog   "$logf"
      -np         "$NP" )
[ -n "${STUDY:-}" ]   && cmd+=( -study "$STUDY" )
[ -n "${HWACC:-}" ]   && cmd+=( -hwacc "$HWACC" )      # 음향 explicit 전용 (배터리는 보통 비움)
# shellcheck disable=SC2206
[ -n "${EXTRA_FLAGS:-}" ] && cmd+=( $EXTRA_FLAGS )
[ ${#PASS_EXTRA[@]} -gt 0 ] && cmd+=( "${PASS_EXTRA[@]}" )

log_info "실행: ${cmd[*]}"
start=$(date +%s)
set +e
"${cmd[@]}"
rc=$?
set -e
elapsed=$(( $(date +%s) - start ))

cleanup; trap - EXIT
log_info "종료코드=$rc, wall-clock=${elapsed}s"
if [ $rc -eq 0 ]; then log_ok "COMSOL 실행 완료"; else log_err "COMSOL 실행 실패 (로그: $logf)"; fi

# --- 로그 파싱 + GPU 사용 검증 + metrics.json ---
if command -v python3 >/dev/null 2>&1; then
  python3 "$HERE/parse_log.py" \
    --log "$logf" --gpu-csv "$gpulog" \
    --model "$MODEL" --solver "${SOLVER:-}" --use-gpu "$USE_GPU" \
    --wall "$elapsed" --json "$outdir/metrics.json" || log_warn "로그 파싱 실패"
else
  log_warn "python3 없음 — 지표 파싱 생략 (로그: $logf)"
fi

exit $rc

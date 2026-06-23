#!/usr/bin/env bash
# [로컬 PC에서 실행] git/scp로 서버와 연계해 원격 GPU 서버에서 COMSOL을 돌린다.
#   흐름: (변경 커밋은 본인이) → push → 서버 git pull → 서버 실행 → 결과 회수
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
. "$HERE/lib/common.sh"
load_server_env
SSH_USER="${SSH_USER:-root}"
REMOTE_DIR="${REMOTE_DIR:-~/Yonghoon-DEM-DFT}"
remote_pipeline="$REMOTE_DIR/comsol-gpu"

# SSH가 필요한 명령에서만 호출 (--help 등은 서버설정 없이도 동작)
require_ssh(){
  : "${SSH_HOST:?config/server.env에 SSH_HOST 설정 필요 (cp config/server.env.example config/server.env)}"
  # shellcheck disable=SC2206
  SSH_CMD=( ssh ${SSH_OPTS:-} "${SSH_USER}@${SSH_HOST}" )
}

usage(){ cat <<'EOF'
사용법: remote.sh <명령> [...]
  check                       원격 환경 점검 (check_env.sh)
  sync                        git push + 서버에서 git pull
  push-mph <로컬.mph>         .mph 파일을 서버 models/ 로 scp 업로드
  run <model> [-- flags]      sync → 서버 실행 → 결과(metrics) 회수
  bench --cpu A --gpu B       sync → 서버 벤치마크 → CSV 회수
  pull-results [model]        결과/요약만 scp로 회수
예:
  bash scripts/remote.sh push-mph "/c/Users/.../0.1C_31x31x40_LPSCl_5e-6_bulk.mph"
  bash scripts/remote.sh run lpscl_3d_bulk
  bash scripts/remote.sh bench --cpu lpscl_3d_bulk_cpu --gpu lpscl_3d_bulk
EOF
}

fetch_results(){
  local model="${1:-}"
  mkdir -p "$RESULTS_DIR" "$BENCH_DIR"
  if [ -n "$model" ]; then
    scp ${SSH_OPTS:-} -r "${SSH_USER}@${SSH_HOST}:${remote_pipeline}/results/${model}" \
      "$RESULTS_DIR/" 2>/dev/null && log_ok "결과 회수: results/${model}/" \
      || log_warn "결과 회수 실패 (아직 없음?)"
  fi
  scp ${SSH_OPTS:-} -r "${SSH_USER}@${SSH_HOST}:${remote_pipeline}/benchmarks/." \
    "$BENCH_DIR/" 2>/dev/null || true
}

do_sync(){
  require_ssh
  local branch; branch="$(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD)"
  log_info "git push (origin/$branch)…"
  git -C "$REPO_ROOT" push -u origin "$branch"
  log_info "서버 git pull…"
  "${SSH_CMD[@]}" "cd $REMOTE_DIR && git pull --ff-only"
}

sub="${1:-}"; shift || true
case "$sub" in
  check)
    require_ssh
    "${SSH_CMD[@]}" "cd $remote_pipeline && bash scripts/check_env.sh"
    ;;
  sync)
    do_sync
    ;;
  push-mph)
    require_ssh
    f="${1:?로컬 .mph 경로를 지정하세요}"
    [ -f "$f" ] || die "파일 없음: $f"
    log_info "scp 업로드: $(basename "$f") → ${remote_pipeline}/models/"
    scp ${SSH_OPTS:-} "$f" "${SSH_USER}@${SSH_HOST}:${remote_pipeline}/models/"
    log_ok "업로드 완료"
    ;;
  run)
    [ $# -ge 1 ] || { usage; exit 1; }
    model="$1"
    do_sync
    "${SSH_CMD[@]}" "cd $remote_pipeline && bash scripts/run.sh $*"
    fetch_results "$model"
    ;;
  bench)
    do_sync
    "${SSH_CMD[@]}" "cd $remote_pipeline && bash scripts/benchmark.sh $*"
    fetch_results ""
    ;;
  pull-results)
    require_ssh
    fetch_results "${1:-}"
    ;;
  -h|--help|"")
    usage
    ;;
  *)
    die "알 수 없는 명령: $sub  (--help 참고)"
    ;;
esac

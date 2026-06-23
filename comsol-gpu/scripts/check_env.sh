#!/usr/bin/env bash
# [서버에서 실행] COMSOL GPU 환경 점검: GPU/드라이버/COMSOL/배치플래그/cuDSS/라이선스
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
. "$HERE/lib/common.sh"
load_server_env

echo "================ COMSOL GPU 환경 점검 ================"

# 1) GPU / 드라이버
if command -v nvidia-smi >/dev/null 2>&1; then
  log_ok "nvidia-smi 발견"
  nvidia-smi --query-gpu=index,name,memory.total,memory.used,driver_version \
    --format=csv 2>/dev/null || nvidia-smi
else
  log_err "nvidia-smi 없음 — NVIDIA 드라이버 미설치? (GPU 가속 불가)"
fi
echo

# 2) COMSOL 바이너리 / 버전
comsol_bin=""
if comsol_bin="$(find_comsol)"; then
  log_ok "COMSOL 바이너리: $comsol_bin"
  "$comsol_bin" --version 2>/dev/null || "$comsol_bin" -version 2>/dev/null \
    || log_warn "버전 출력 실패 (라이선스/디스플레이 문제일 수 있음)"
else
  log_err "comsol 바이너리 못 찾음 — config/server.env의 COMSOL_BIN 설정 필요"
fi
echo

# 3) batch 지원 플래그 덤프 (★ 이 서버 바이너리의 실제 옵션이 정답)
if [ -n "$comsol_bin" ]; then
  log_info "comsol batch GPU/가속 관련 플래그 (이 버전 기준):"
  if "$comsol_bin" batch -h >/tmp/comsol_batch_help.txt 2>&1; then
    grep -iE 'hwacc|gpu|cuda|accel|^\s*-np|-nn' /tmp/comsol_batch_help.txt \
      || log_warn "  hwacc/gpu 관련 플래그 텍스트 없음 — 배터리는 cuDSS(모델 솔버설정)로 켜는게 정석"
    log_info "  전체 도움말: /tmp/comsol_batch_help.txt"
  else
    log_warn "  comsol batch -h 실패"
  fi
fi
echo

# 4) cuDSS / CUDA 라이브러리 탐색 (범위 제한)
log_info "cuDSS / CUDA 라이브러리 탐색:"
( ldconfig -p 2>/dev/null | grep -iE 'cudss|cublas|cudart' ) \
  || log_warn "  ldconfig에 안 보임 (COMSOL 내장 lib에 포함됐을 수 있음)"
clib_dirs=()
if [ -n "$comsol_bin" ]; then
  croot="$(cd "$(dirname "$comsol_bin")/../.." 2>/dev/null && pwd || true)"
  [ -n "$croot" ] && clib_dirs+=("$croot")
fi
clib_dirs+=(/usr/local/cuda /usr/lib/x86_64-linux-gnu)
for d in "${clib_dirs[@]}"; do
  [ -d "$d" ] || continue
  hit="$(find "$d" -maxdepth 6 -iname 'libcudss*' 2>/dev/null | head -3 || true)"
  [ -n "$hit" ] && { log_ok "  libcudss 발견:"; echo "$hit" | sed 's/^/    /'; break; }
done
echo

# 5) 라이선스
log_info "라이선스:"
echo "    LMCOMSOL_LICENSE_FILE=${LMCOMSOL_LICENSE_FILE:-(unset)}"
echo "    배치/멀티-GPU엔 보통 플로팅 네트워크 라이선스(FNL)가 필요합니다."
echo

echo "================ 점검 끝 ================"
echo "다음 단계:"
echo "  1) GUI에서 모델 Direct 솔버를 cuDSS로 저장 (methods/set_cudss_solver.md)"
echo "  2) config/models/<name>.env 작성 후:  bash scripts/run.sh <name>"

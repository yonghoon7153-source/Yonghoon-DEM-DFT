# source 하세요 (실행 X):  source scripts/activate_dem.sh   또는  alias dem
# venv 활성화 + nvidia CUDA 라이브러리 경로(LD_LIBRARY_PATH) + repo 로 cd.
# ★ 이걸 source 한 셸에서 run_mpm.sh / step4_only.sh 를 돌려야 detached 자식이
#   venv(numpy/cupy)와 CUDA 라이브러리를 물려받아 "멈추지 않습니다".
_D="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"
if [ ! -f "$_D/venv/bin/activate" ]; then
  echo "✗ venv 없음: $_D/venv — 먼저 bash scripts/setup_gpu_server.sh 하세요"
else
  # shellcheck disable=SC1091
  source "$_D/venv/bin/activate"
  _NVLIB="$(ls -d "$_D"/venv/lib/python*/site-packages/nvidia/*/lib 2>/dev/null | tr '\n' ':')"
  export LD_LIBRARY_PATH="${_NVLIB}${LD_LIBRARY_PATH:-}"
  cd "$_D"
  echo "✓ dem env — $(python --version 2>&1) · venv=$(basename "$VIRTUAL_ENV") · CUDA libs=$([ -n "$_NVLIB" ] && echo set || echo none) · $(pwd)"
fi

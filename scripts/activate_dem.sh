# source 하세요 (실행 X):  source scripts/activate_dem.sh   또는  alias dem
# venv(또는 활성 conda env) + nvidia CUDA 라이브러리 경로(LD_LIBRARY_PATH) + repo 로 cd.
# ★ 이걸 source 한 셸에서 run_mpm.sh / step4_only.sh 를 돌려야 detached 자식이
#   파이썬 환경(numpy/cupy)과 CUDA 라이브러리를 물려받아 "멈추지 않습니다".
_D="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")/.." && pwd)"
# conda env(비-base)가 이미 활성이면 그걸 쓰고 venv 는 건너뜀 (구 glibc 서버 = conda py3.11 경로).
if { [ -z "${CONDA_DEFAULT_ENV:-}" ] || [ "${CONDA_DEFAULT_ENV}" = "base" ]; } && [ -f "$_D/venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source "$_D/venv/bin/activate"
fi
# 현재 파이썬의 nvidia CUDA 라이브러리(libcublasLt.so 등)를 LD_LIBRARY_PATH 에 (cupy pathfinder 대비)
_NVLIB="$(python -c "import site,glob,os; ps=list(site.getsitepackages())+[site.getusersitepackages()]; print(':'.join(sorted(set(sum([glob.glob(os.path.join(p,'nvidia','*','lib')) for p in ps],[])))))" 2>/dev/null || true)"
export LD_LIBRARY_PATH="${_NVLIB:+$_NVLIB:}${LD_LIBRARY_PATH:-}"
cd "$_D"
echo "✓ dem env — $(python --version 2>&1) · env=${CONDA_DEFAULT_ENV:-${VIRTUAL_ENV:+$(basename "$VIRTUAL_ENV")}} · CUDA libs=$([ -n "$_NVLIB" ] && echo set || echo none) · $(pwd)"

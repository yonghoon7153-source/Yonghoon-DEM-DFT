#!/usr/bin/env bash
# =============================================================================
#  setup_env.sh — 새 머신(CPU 서버 / GPU 서버 / V100 SSH)에서 원커맨드 환경 구축
#
#  사용:
#    git clone <repo> && cd <repo>/degradation-degeneracy
#    ./scripts/setup_env.sh              # CPU 기본 (pybamm + IDAKLU)
#    ./scripts/setup_env.sh --gpu        # + GPU 스택 (jax/torch, CUDA 자동 감지)
#    ./scripts/setup_env.sh --recreate   # .venv 삭제 후 재구축
#
#  끝나면 자동으로 검증(scripts/verify_env.py)을 실행하고
#  docs/ENV_REPORT.md 를 생성한다. 상세: docs/SETUP_GPU.md
#
#  설계 원칙:
#   - 멱등: 몇 번을 다시 실행해도 안전
#   - GPU가 없어도 절대 실패하지 않음 (CPU 병렬이 1차 경로 — GPU 현실론)
#   - 네트워크 불안정 대비 pip --timeout/--retries 기본 적용
# =============================================================================
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

GPU="auto"          # auto | on | off
RECREATE="false"
PYTHON="${PYTHON:-}"
PIP_OPTS=(--timeout 180 --retries 8)

while [[ $# -gt 0 ]]; do
  case "$1" in
    --gpu)       GPU="on"; shift ;;
    --no-gpu)    GPU="off"; shift ;;
    --recreate)  RECREATE="true"; shift ;;
    --python)    PYTHON="$2"; shift 2 ;;
    -h|--help)   grep '^#' "$0" | head -20; exit 0 ;;
    *) echo "알 수 없는 인자: $1" >&2; exit 1 ;;
  esac
done

say()  { printf '\n\033[1;34m[setup]\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33m[setup:주의]\033[0m %s\n' "$*"; }

# ---------------------------------------------------------------- 1. 시스템 탐지
say "시스템 탐지"
uname -a || true
NPROC="$(command -v nproc >/dev/null && nproc || echo 4)"
echo "  CPU 코어      : ${NPROC}  (run.sh --nproc 기본값)"
command -v free >/dev/null && free -g | sed -n '2p' | awk '{print "  메모리(GB)    : "$2}'
df -h . | tail -1 | awk '{print "  디스크 여유   : "$4"  (fine 격자는 수 GB 필요)"}'

HAS_GPU="false"
CUDA_MAJOR=""
if command -v nvidia-smi >/dev/null 2>&1; then
  if nvidia-smi --query-gpu=name --format=csv,noheader >/dev/null 2>&1; then
    HAS_GPU="true"
    nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader \
      | sed 's/^/  GPU           : /'
    # CUDA 런타임 최대 지원 버전 (드라이버 기준)
    CUDA_MAJOR="$(nvidia-smi | grep -oP 'CUDA Version: \K[0-9]+' | head -1 || true)"
    echo "  CUDA(driver)  : ${CUDA_MAJOR:-감지 실패}"
  fi
fi
[[ "$HAS_GPU" == "false" ]] && echo "  GPU           : 없음 (CPU 경로로 진행 — 문제 없음)"

# ---------------------------------------------------------------- 2. Python 선택
say "Python 선택 (3.10~3.12 권장)"
if [[ -z "$PYTHON" ]]; then
  for cand in python3.12 python3.11 python3.10 python3; do
    if command -v "$cand" >/dev/null 2>&1; then PYTHON="$cand"; break; fi
  done
fi
[[ -z "$PYTHON" ]] && { echo "python3 없음. 설치 후 재실행" >&2; exit 1; }
"$PYTHON" --version
PYVER_OK="$("$PYTHON" -c 'import sys; print(1 if (3,10)<=sys.version_info<(3,13) else 0)')"
[[ "$PYVER_OK" != "1" ]] && warn "Python 3.10~3.12 밖의 버전 — pybamm 휠 미지원일 수 있음"

# ---------------------------------------------------------------- 3. venv
if [[ "$RECREATE" == "true" && -d .venv ]]; then
  say ".venv 삭제 (--recreate)"
  rm -rf .venv
fi
if [[ ! -d .venv ]]; then
  say "가상환경 생성 (.venv)"
  "$PYTHON" -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install "${PIP_OPTS[@]}" -q -U pip wheel

# ---------------------------------------------------------------- 4. 핵심 패키지
say "핵심 패키지 설치 (requirements.txt — pybamm[all] 포함, 수 분 소요)"
pip install "${PIP_OPTS[@]}" -r requirements.txt

# ---------------------------------------------------------------- 5. GPU 스택 (선택)
if [[ "$GPU" == "on" || ( "$GPU" == "auto" && "$HAS_GPU" == "true" ) ]]; then
  if [[ "$HAS_GPU" != "true" ]]; then
    warn "--gpu 지정됐지만 nvidia-smi 미검출 → GPU 스택 건너뜀"
  elif [[ -n "$CUDA_MAJOR" && "$CUDA_MAJOR" -ge 12 ]]; then
    say "GPU 스택 설치 (CUDA ${CUDA_MAJOR} — jax[cuda12])"
    pip install "${PIP_OPTS[@]}" -r requirements-gpu.txt \
      || warn "jax 설치 실패 — Phase 7 전까지는 불필요. docs/GPU_NOTES.md에 기록할 것"
    say "PyTorch(surrogate용)는 필요 시 수동 설치:"
    echo "  pip install torch --index-url https://download.pytorch.org/whl/cu121"
  else
    warn "CUDA 12 미만(${CUDA_MAJOR:-?}) — jax[cuda12] 부적합."
    warn "V100이라도 드라이버가 CUDA 12를 지원해야 함 (driver >= 525.60)."
    warn "구형 드라이버면: pip install 'jax[cuda11_pip]' (구버전 jax 필요) 또는 CPU 경로 사용."
  fi
else
  say "GPU 스택 생략 (CPU 경로). 나중에: ./scripts/setup_env.sh --gpu"
fi

# ---------------------------------------------------------------- 6. 검증
say "환경 검증 (verify_env.py → docs/ENV_REPORT.md)"
python scripts/verify_env.py --out docs/ENV_REPORT.md

say "완료. 다음 단계:"
cat <<EOF
  source .venv/bin/activate
  ./run.sh --mode verify                                     # 재검증
  ./run.sh --mode sweep1d --out results/sweep1d_v1           # 32p 재현
  ./run.sh --mode grid --config configs/grid_coarse.yaml --dry-run
  ./run.sh --mode grid --config configs/grid_coarse.yaml --nproc ${NPROC} --out results/grid_coarse_v1
EOF

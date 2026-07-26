#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
# 완전 자동 GPU 서버 세팅 — 새 인스턴스(kgy / V100 / runyour.ai 등)서 MPM+STEP3+STEP4
# 파이프라인이 "멈추지 않고" 끝까지 돌게.  2026-07-27 세션서 겪은 모든 구멍을 한 번에 메움:
#   numpy 부재 · cupy 부재 · libcublasLt.so 부재 · CUDA 헤더 부재 · OCP 앵커 부재 · venv-detach.
#
# 사용 (새 서버서 한 줄):
#   curl -fsSL https://raw.githubusercontent.com/yonghoon7153-source/Yonghoon-DEM-DFT/claude/stoic-knuth-NObVQ/scripts/setup_gpu_server.sh | bash
# 또는 레포 있으면:  bash scripts/setup_gpu_server.sh
#
# 멱등(재실행 안전).  각 단계 끝에 검증 → 실패하면 거기서 STOP + 원인 출력 (런 중간에 안 죽게).
# 완료 후:  source scripts/activate_dem.sh   (또는 alias dem)  →  bash <킷>/run_mpm.sh
# ══════════════════════════════════════════════════════════════════════════════
set -euo pipefail
REPO_URL="https://github.com/yonghoon7153-source/Yonghoon-DEM-DFT.git"
BRANCH="claude/stoic-knuth-NObVQ"
DIR="${MPM_DIR:-$HOME/Yonghoon-DEM-DFT}"
_SUDO=""; command -v sudo >/dev/null 2>&1 && [ "$(id -u)" != 0 ] && _SUDO="sudo"

echo "══ [1/7] 시스템 deps (apt) ══"
if command -v apt-get >/dev/null 2>&1; then
  $_SUDO apt-get update -qq || true
  $_SUDO DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
    python3 python3-venv python3-pip build-essential git curl unzip tmux >/dev/null
fi
python3 --version

echo "══ [2/7] 레포 ($BRANCH) ══"
if [ -d "$DIR/.git" ]; then ( cd "$DIR" && git fetch origin "$BRANCH" ); else git clone "$REPO_URL" "$DIR"; fi
cd "$DIR"
git checkout -B "$BRANCH" "origin/$BRANCH"
git log --oneline -1

echo "══ [3/7] venv ══"
[ -d venv ] || python3 -m venv venv
# shellcheck disable=SC1091
source venv/bin/activate
python -m pip install --upgrade pip -q

echo "══ [4/7] python 패키지 (코어 + MPM + STEP4 + 파이프라인) ══"
# taichi 1.7.4(py3.8–3.12); 실패(예 py3.13/구 glibc) 시 1.6.0 폴백 (API·결과 동일)
python -m pip install -q "taichi==1.7.4" || python -m pip install -q "taichi==1.6.0"
python -m pip install -q numpy scipy matplotlib pandas networkx scikit-image pyamg pybamm

echo "══ [5/7] GPU 가속 (cupy + CUDA 라이브러리 + 헤더) ══"
# [ctk] = CUDA toolkit 헤더 (없으면 'Failed to find CUDA headers'로 커널 JIT 실패 — 이번 세션 실화).
# nvidia-*-cu12 = libcublasLt.so 등 (cupy-cuda12x 단독은 안 끌어옴 — 이번 세션 실화).
# 드라이버가 CUDA 13이어도 cuda12x wheel = backward-compatible (검증됨).
python -m pip install -q "cupy-cuda12x[ctk]" \
  nvidia-cublas-cu12 nvidia-cusparse-cu12 nvidia-cusolver-cu12 \
  nvidia-nvjitlink-cu12 nvidia-cuda-runtime-cu12 nvidia-cuda-nvrtc-cu12 || {
    echo "  ⚠ cupy/CUDA 설치 일부 실패 — GPU 없이도 CPU fallback으로 파이프라인은 돕니다(느릴 뿐)."; }
NVLIB="$(ls -d "$DIR"/venv/lib/python*/site-packages/nvidia/*/lib 2>/dev/null | tr '\n' ':')"
export LD_LIBRARY_PATH="${NVLIB}${LD_LIBRARY_PATH:-}"

echo "══ [6/7] OCP 앵커 생성 (없으면 STEP4가 SKIP됨 — 이번 세션 실화) ══"
python3 scripts/step4_pybamm_anchor.py --export-params anchor_params
ls -l anchor_params/

echo "══ [7/7] 검증 (런 전에 모든 GPU 경로 확인) ══"
python - <<'PY'
import numpy, scipy, matplotlib, pandas, networkx, skimage, pyamg, pybamm
print("  ✓ 코어/STEP4/파이프라인 import OK")
import taichi as ti; ti.init(arch=ti.cuda); print("  ✓ taichi CUDA (MPM GPU)", ti.__version__)
try:
    import cupy as cp, cupyx.scipy.sparse as sp
    from cupyx.scipy.sparse.linalg import cg
    n = 2000
    A = sp.csr_matrix(sp.diags([cp.full(n, 2.), cp.full(n-1, -1.), cp.full(n-1, -1.)], [0, 1, -1]))
    b = cp.ones(n)
    try: x, i = cg(A, b, rtol=1e-10, maxiter=5000)
    except TypeError: x, i = cg(A, b, tol=1e-10, maxiter=5000)
    print("  ✓ cupy GPU sparse CG OK (STEP3 GPU 준비됨) info=", i)
except Exception as e:
    print("  ⚠ cupy GPU 미가동 (", type(e).__name__, ") → STEP3는 CPU fallback (결과 동일, 몇 분 더).")
PY
python3 scripts/step4_dyn.py --selftest 2>&1 | tail -1

# 편의 실행 헬퍼(activate_dem.sh)를 alias로 등록 — 재접속마다 venv + CUDA 경로 한 번에
BRC="$HOME/.bashrc"
if ! grep -q "alias dem=" "$BRC" 2>/dev/null; then
  echo "alias dem='source $DIR/scripts/activate_dem.sh'" >> "$BRC"
fi

cat <<EOF

════════════════════ 세팅 완료 ════════════════════
매번 이렇게 실행하세요 (venv + CUDA 경로 자동):

  source $DIR/scripts/activate_dem.sh      # 또는 새 셸이면:  dem
  # (킷 zip을 $DIR 에 풀고)
  bash run_mpm.sh                          # 전체 파이프라인 (detached, SSH 끊겨도 안 죽음)
  bash step4_only.sh                       # step4만 재개 (step4_grid.npz 있을 때)

★ activate_dem.sh 를 반드시 source 한 셸에서 run 하세요 — 그래야 detached 자식이
  venv(numpy/cupy) + CUDA 라이브러리 경로를 물려받아 안 멈춥니다.
════════════════════════════════════════════════════
EOF

#!/usr/bin/env bash
# =============================================================================
#  degradation-degeneracy — 단일 진입점
#
#  현재 상태: Phase 0 스켈레톤.
#             --mode verify 만 실제 동작하며, 나머지는 NOT IMPLEMENTED.
#             각 Phase 진행에 따라 아래 dispatch 블록을 채워 나간다.
#
#  스펙: docs/03_ARCHITECTURE.md 2절
# =============================================================================
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

# ---------------------------------------------------------------- defaults
MODE=""
CONFIG="configs/base.yaml"

# 열화 모드 축 — "start:stop:step" | "a,b,c" | "0.1" | "none"
LLI="none"
LAM_PE="none"
LAM_NE="none"
LAM_PE_TYPE="de"          # de | li | both
LAM_NE_TYPE="de"

# 실험 조건
C_RATE="0.05"
V_UPPER="4.2"
V_LOWER="2.5"

# 노이즈
NOISE="0"
NOISE_SEED="42"

# fitting
OBJECTIVE="pocv_dvdq"
W_POCV="1.0"
W_DVDQ="1.0"
W_DQDV="0.0"
INIT_GUESS="1.03,-0.1,1.08,-0.01"
BOUNDS_LB="1.00,-0.30,1.00,-0.15"
BOUNDS_UB="1.10,0.00,1.10,0.00"
N_RESTARTS="1"

# 실행 제어
BACKEND="cpu"             # cpu | gpu
NPROC="$(command -v nproc >/dev/null && nproc || echo 4)"
SOLVER="idaklu"           # idaklu | casadi
CHUNK_SIZE="200"
RESUME="false"
DRY_RUN="false"

# 출력
OUT="results/run_$(date +%Y%m%d_%H%M%S)"
TAG=""
LOG_LEVEL="INFO"

# ---------------------------------------------------------------- usage
usage() {
cat <<'EOF'
사용: ./run.sh --mode <MODE> [옵션...]

MODE
  verify     환경 검증 (IDAKLU / composite DFN / GPU)
  baseline   완방상태 산출 및 캐시
  sweep1d    32p 재현 — 모드별 1D sweep
  grid       조합 격자 곡선 생성          ★ 핵심
  fit        생성된 곡선에 alpha/beta fitting
  score      축퇴 판정 및 지도 생성
  hessian    조건수 / 고윳값 분석
  report     그림 + 표 생성
  all        grid -> fit -> score -> report

열화 모드 축   (형식: 0:0.2:0.02 | 0,0.05,0.1 | 0.1 | none)
  --lli VAL              LLI 축
  --lam-pe VAL           LAM_PE 축
  --lam-ne VAL           LAM_NE 축
  --lam-pe-type T        de | li | both   (기본 de)
  --lam-ne-type T        de | li | both   (기본 de)

실험 조건
  --c-rate F             기본 0.05
  --v-upper F            기본 4.2
  --v-lower F            기본 2.5

노이즈
  --noise LIST           V 단위 gaussian, 예: 0,0.001,0.005
  --noise-seed N         기본 42

fitting
  --objective LIST       pocv | pocv_dvdq | pocv_dvdq_dqdv | dqdv_only (콤마 다중)
  --w-pocv F             pOCV 가중치
  --w-dvdq F             dV/dQ 가중치
  --w-dqdv VAL           dQ/dV 가중치 (축 문법으로 sweep 가능)
  --init-guess CSV       a_PE,b_PE,a_NE,b_NE
  --bounds-lb CSV        하한
  --bounds-ub CSV        상한
  --n-restarts N         multi-start 횟수 (축퇴 진단용, 권장 5)

실행 제어
  --backend B            cpu | gpu   (기본 cpu)
  --nproc N              병렬 프로세스 수 (기본: nproc)
  --solver S             idaklu | casadi
  --chunk-size N         청크 저장 단위 (기본 200)
  --resume               중단 지점부터 재개
  --dry-run              조건 수 / 예상시간 / 예상용량만 출력 후 종료

출력
  --config PATH          기본 configs/base.yaml
  --in PATH              (fit/score/report) 입력 결과 디렉터리
  --out PATH             출력 디렉터리
  --tag STR              실행 태그 (manifest에 기록)
  --log-level L          DEBUG | INFO | WARNING

예시
  ./run.sh --mode verify
  ./run.sh --mode sweep1d --out results/sweep1d_v1
  ./run.sh --mode grid --lli 0:0.2:0.05 --lam-pe 0:0.2:0.05 --lam-ne 0:0.2:0.05 --dry-run
  ./run.sh --mode grid --config configs/grid_fine.yaml --nproc 32 --out results/final_v1
  ./run.sh --mode fit --in results/final_v1 --objective pocv,pocv_dvdq,pocv_dvdq_dqdv --n-restarts 5
  ./run.sh --mode score --in results/final_v1
EOF
}

# ---------------------------------------------------------------- parse
IN_DIR=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)          MODE="$2"; shift 2 ;;
    --config)        CONFIG="$2"; shift 2 ;;
    --lli)           LLI="$2"; shift 2 ;;
    --lam-pe)        LAM_PE="$2"; shift 2 ;;
    --lam-ne)        LAM_NE="$2"; shift 2 ;;
    --lam-pe-type)   LAM_PE_TYPE="$2"; shift 2 ;;
    --lam-ne-type)   LAM_NE_TYPE="$2"; shift 2 ;;
    --c-rate)        C_RATE="$2"; shift 2 ;;
    --v-upper)       V_UPPER="$2"; shift 2 ;;
    --v-lower)       V_LOWER="$2"; shift 2 ;;
    --noise)         NOISE="$2"; shift 2 ;;
    --noise-seed)    NOISE_SEED="$2"; shift 2 ;;
    --objective)     OBJECTIVE="$2"; shift 2 ;;
    --w-pocv)        W_POCV="$2"; shift 2 ;;
    --w-dvdq)        W_DVDQ="$2"; shift 2 ;;
    --w-dqdv)        W_DQDV="$2"; shift 2 ;;
    --init-guess)    INIT_GUESS="$2"; shift 2 ;;
    --bounds-lb)     BOUNDS_LB="$2"; shift 2 ;;
    --bounds-ub)     BOUNDS_UB="$2"; shift 2 ;;
    --n-restarts)    N_RESTARTS="$2"; shift 2 ;;
    --backend)       BACKEND="$2"; shift 2 ;;
    --nproc)         NPROC="$2"; shift 2 ;;
    --solver)        SOLVER="$2"; shift 2 ;;
    --chunk-size)    CHUNK_SIZE="$2"; shift 2 ;;
    --resume)        RESUME="true"; shift ;;
    --dry-run)       DRY_RUN="true"; shift ;;
    --in)            IN_DIR="$2"; shift 2 ;;
    --out)           OUT="$2"; shift 2 ;;
    --tag)           TAG="$2"; shift 2 ;;
    --log-level)     LOG_LEVEL="$2"; shift 2 ;;
    -h|--help)       usage; exit 0 ;;
    *) echo "알 수 없는 인자: $1" >&2; usage; exit 1 ;;
  esac
done

[[ -z "$MODE" ]] && { echo "--mode 필수" >&2; usage; exit 1; }

# ---------------------------------------------------------------- venv
if [[ -d ".venv" && -z "${VIRTUAL_ENV:-}" ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

export PYTHONPATH="${REPO_ROOT}:${PYTHONPATH:-}"
export MPLBACKEND="Agg"          # headless 강제

# ---------------------------------------------------------------- dispatch
not_impl() {
  echo "[NOT IMPLEMENTED] --mode $1"
  echo "  docs/04_PROMPTS.md 의 해당 Phase를 먼저 완료할 것."
  exit 2
}

case "$MODE" in

  verify)
    exec python scripts/verify_env.py --out docs/ENV_REPORT.md
    ;;

  baseline)   # Phase 1
    not_impl baseline
    # exec python -m src.baseline --config "$CONFIG" --out "$OUT"
    ;;

  sweep1d)    # Phase 2
    not_impl sweep1d
    # exec python -m src.sweep --config "$CONFIG" --out "$OUT" \
    #   --solver "$SOLVER" --log-level "$LOG_LEVEL"
    ;;

  grid)       # Phase 3
    not_impl grid
    # exec python -m src.grid \
    #   --config "$CONFIG" \
    #   --lli "$LLI" --lam-pe "$LAM_PE" --lam-ne "$LAM_NE" \
    #   --lam-pe-type "$LAM_PE_TYPE" --lam-ne-type "$LAM_NE_TYPE" \
    #   --c-rate "$C_RATE" --v-upper "$V_UPPER" --v-lower "$V_LOWER" \
    #   --noise "$NOISE" --noise-seed "$NOISE_SEED" \
    #   --backend "$BACKEND" --nproc "$NPROC" --solver "$SOLVER" \
    #   --chunk-size "$CHUNK_SIZE" \
    #   $([[ "$RESUME"  == "true" ]] && echo --resume) \
    #   $([[ "$DRY_RUN" == "true" ]] && echo --dry-run) \
    #   --out "$OUT" --tag "$TAG" --log-level "$LOG_LEVEL"
    ;;

  fit)        # Phase 4
    not_impl fit
    # exec python -m src.fitting --in "${IN_DIR:-$OUT}" --out "$OUT" \
    #   --objective "$OBJECTIVE" \
    #   --w-pocv "$W_POCV" --w-dvdq "$W_DVDQ" --w-dqdv "$W_DQDV" \
    #   --init-guess "$INIT_GUESS" \
    #   --bounds-lb "$BOUNDS_LB" --bounds-ub "$BOUNDS_UB" \
    #   --n-restarts "$N_RESTARTS" --nproc "$NPROC"
    ;;

  score)      # Phase 5
    not_impl score
    # exec python -m src.scoring --in "${IN_DIR:-$OUT}" --out "$OUT"
    ;;

  hessian)    # Phase 5
    not_impl hessian
    # exec python -m src.hessian --in "${IN_DIR:-$OUT}" --out "$OUT"
    ;;

  report)     # Phase 6
    not_impl report
    # exec python tools/compare_objectives.py --in "${IN_DIR:-$OUT}" --out "$OUT"
    ;;

  all)        # Phase 6
    not_impl all
    ;;

  *)
    echo "알 수 없는 mode: $MODE" >&2
    usage
    exit 1
    ;;
esac

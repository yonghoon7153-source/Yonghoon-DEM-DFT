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
OBJECTIVE=""                      # 비우면 objectives.yaml 전체 (4종)
BOUNDS_PRESET="expanded"          # expanded | original_33p
N_RESTARTS="auto"                 # auto = objectives.yaml 의 n_restarts
CLEAN="false"                     # true면 노이즈 없는 곡선으로 fitting
LIMIT=""                          # 앞 N조건만 (스모크용)
REFERENCE="grid"                  # grid (유도식) | halfcell (21p 식, 전 범위 반쪽셀)

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
  score      degeneracy 판정 및 지도 생성
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
                         기본: objectives.yaml 의 4종 전부
  --bounds PRESET        expanded (기본) | original_33p
                         original_33p 는 33p 원본 bound. alpha 하한 1.00이
                         "LAM = 용량손실"을 강제하는지 비교하는 용도
  --n-restarts N         multi-start 횟수 (degeneracy 진단용, 기본 5)
  --clean                노이즈 없는 곡선으로 fitting
  --limit N              앞 N조건만 (스모크용)

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
  ./run.sh --mode fit --in results/grid_fine_v1 --nproc 32
  ./run.sh --mode fit --in results/grid_fine_v1 --bounds original_33p --nproc 32
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
    --bounds)        BOUNDS_PRESET="$2"; shift 2 ;;
    --n-restarts)    N_RESTARTS="$2"; shift 2 ;;
    --clean)         CLEAN="true"; shift ;;
    --limit)         LIMIT="$2"; shift 2 ;;
    --reference)     REFERENCE="$2"; shift 2 ;;
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
    exec python -m src.baseline --config "$CONFIG" --log-level "$LOG_LEVEL"
    ;;

  sweep1d)    # Phase 2
    [[ "$CONFIG" == "configs/base.yaml" ]] && CONFIG="configs/sweep1d.yaml"
    exec python -m src.sweep --config "$CONFIG" --out "$OUT" \
      --log-level "$LOG_LEVEL"
    ;;

  grid)       # Phase 3
    [[ "$CONFIG" == "configs/base.yaml" ]] && CONFIG="configs/grid_coarse.yaml"
    GRID_ARGS=(--config "$CONFIG"
               --nproc "$NPROC" --chunk-size "$CHUNK_SIZE"
               --out "$OUT" --log-level "$LOG_LEVEL")
    [[ "$LLI"    != "none" ]] && GRID_ARGS+=(--lli "$LLI")
    [[ "$LAM_PE" != "none" ]] && GRID_ARGS+=(--lam-pe "$LAM_PE")
    [[ "$LAM_NE" != "none" ]] && GRID_ARGS+=(--lam-ne "$LAM_NE")
    GRID_ARGS+=(--lam-pe-type "$LAM_PE_TYPE" --lam-ne-type "$LAM_NE_TYPE")
    [[ "$NOISE" != "0" ]] && GRID_ARGS+=(--noise "$NOISE")
    GRID_ARGS+=(--noise-seed "$NOISE_SEED")
    [[ "$RESUME"  == "true" ]] && GRID_ARGS+=(--resume)
    [[ "$DRY_RUN" == "true" ]] && GRID_ARGS+=(--dry-run)
    [[ -n "$TAG" ]] && GRID_ARGS+=(--tag "$TAG")
    if [[ "$BACKEND" == "gpu" ]]; then
      echo "[경고] --backend gpu 는 아직 미구현 (Phase 7). CPU로 fallback." >&2
    fi
    exec python -m src.grid "${GRID_ARGS[@]}"
    ;;

  fit)        # Phase 4
    # halfcell 기준 + 기본 bound면 전용 preset으로 (리뷰 F3: 인덱스 패치는 버그였음)
    [[ "$REFERENCE" == "halfcell" && "$BOUNDS_PRESET" == "expanded" ]] && BOUNDS_PRESET="halfcell"
    FIT_ARGS=(--in "${IN_DIR:-$OUT}" --nproc "$NPROC"
              --bounds "$BOUNDS_PRESET" --log-level "$LOG_LEVEL")
    [[ -n "$IN_DIR" ]] && FIT_ARGS+=(--out "$IN_DIR")
    [[ -n "$OBJECTIVE" ]] && FIT_ARGS+=(--objective "$OBJECTIVE")
    [[ "$N_RESTARTS" != "auto" ]] && FIT_ARGS+=(--n-restarts "$N_RESTARTS")
    [[ "$CLEAN" == "true" ]] && FIT_ARGS+=(--clean)
    FIT_ARGS+=(--reference "$REFERENCE")
    [[ -n "$LIMIT" ]] && FIT_ARGS+=(--limit "$LIMIT")
    [[ "$RESUME" == "true" ]] && FIT_ARGS+=(--resume)
    exec python -m src.fitting "${FIT_ARGS[@]}"
    ;;

  score)      # Phase 5
    exec python -m src.scoring --in "${IN_DIR:-$OUT}" --log-level "$LOG_LEVEL"
    ;;

  hessian)    # Phase 5
    exec python -m src.hessian --in "${IN_DIR:-$OUT}" \
      --objective "${OBJECTIVE:-pocv_dvdq}" --log-level "$LOG_LEVEL"
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

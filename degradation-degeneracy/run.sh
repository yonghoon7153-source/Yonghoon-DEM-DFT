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

# 노이즈
NOISE="0"
NOISE_SET="false"                 # --noise 를 사용자가 직접 줬는가
NOISE_SEED="42"

# fitting
OBJECTIVE=""                      # 비우면 objectives.yaml 전체 (4종)
BOUNDS_PRESET="expanded"          # expanded | original_33p
N_RESTARTS="auto"                 # auto = objectives.yaml 의 n_restarts
CLEAN="false"                     # true면 노이즈 없는 곡선으로 fitting
ADAPTIVE="true"                   # false면 모든 조건이 정확히 n_restarts 번 (F66)
WARM_START="true"
LIMIT=""                          # 앞 N조건만 (스모크용)
REFERENCE="grid"                  # grid (유도식) | halfcell (21p 식, 전 범위 반쪽셀)

# 가중치 sweep (Phase 6)
W_GRID=""                         # 비우면 0:2:0.25
W_STRIDE="2"                      # 격자 솎기 (2면 축당 11→6값)

# 실행 제어
BACKEND="cpu"             # cpu | gpu
NPROC="$(command -v nproc >/dev/null && nproc || echo 4)"
CHUNK_SIZE="200"
RESUME="false"
DRY_RUN="false"

# 출력
OUT="results/run_$(date +%Y%m%d_%H%M%S)"
OUT_SET="false"                   # --out을 사용자가 직접 줬는가
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
  wsweep     dQ/dV 가중치 탐색 (층화 표본)   ★ "튜닝 아니냐"에 대한 근거
  report     목적함수 4종 비교표 + 그림 + docs/RESULTS.md
  all        grid -> fit -> score -> hessian -> report

열화 모드 축   (형식: 0:0.2:0.02 | 0,0.05,0.1 | 0.1 | none)
  --lli VAL              LLI 축
  --lam-pe VAL           LAM_PE 축
  --lam-ne VAL           LAM_NE 축
  --lam-pe-type T        de | li | both   (기본 de)
  --lam-ne-type T        de | li | both   (기본 de)

실험 조건 (c-rate·전압 창·solver 는 configs/*.yaml 로만 지정한다 —
  CLI 로 받던 시절 파싱만 되고 전달되지 않는 버그가 있었다. 10차 자체 리뷰)

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
  --no-adaptive          적응적 조기 종료를 끈다 — 모든 조건이 정확히
                         --n-restarts 번 돈다. **공정 paired 비교에 필수** (F66)
  --no-warm-start        목적함수 간 warm start 연쇄를 끈다
  --clean                노이즈 없는 곡선으로 fitting
  --limit N              앞 N조건만 (스모크용)

가중치 sweep (--mode wsweep)
  --w-grid VAL           0:2:0.25 (기본) 또는 0,0.5,1,2
  --w-stride N           격자 솎기 간격. 2면 축당 11→6값 → 표본 6³×noise3
                         전체 격자에 9가중치를 다 돌리면 CPU로 감당 안 됨

실행 제어
  --backend B            cpu | gpu   (기본 cpu)
  --nproc N              병렬 프로세스 수 (기본: nproc)
  --chunk-size N         청크 저장 단위 (기본 200)
  --resume               중단 지점부터 재개
  --dry-run              조건 수 / 예상시간 / 예상용량만 출력 후 종료

출력
  --config PATH          기본 configs/base.yaml
  --in PATH              (fit/score/report) 입력 결과 디렉터리
  --compare PATH         (report) halfcell 기준 결과 — Case 1 vs Case 2 절 추가
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

  # ★ F70 — 권장 구조: 곡선 producer 와 fit 출력을 **분리**한다.
  #   두 기준(Case 1/2)이 같은 바이트의 곡선을 읽어야 비교가 성립한다.
  ./run.sh --mode grid --config configs/grid_fine.yaml --out results/grid_curves_v3
  python -m src.halfcell --config configs/base.yaml --method ocp   # 반쪽셀 준비 (필수)
  ./run.sh --mode fit --in results/grid_curves_v3 --out results/grid_fit_v3 \
           --reference grid --nproc 32
  ./run.sh --mode fit --in results/grid_curves_v3 --out results/halfcell_fit_v3 \
           --reference halfcell --nproc 32
  ./run.sh --mode score --in results/final_v1
EOF
}

# ---------------------------------------------------------------- parse
IN_DIR=""
COMPARE_DIR=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)          MODE="$2"; shift 2 ;;
    --config)        CONFIG="$2"; shift 2 ;;
    --lli)           LLI="$2"; shift 2 ;;
    --lam-pe)        LAM_PE="$2"; shift 2 ;;
    --lam-ne)        LAM_NE="$2"; shift 2 ;;
    --lam-pe-type)   LAM_PE_TYPE="$2"; shift 2 ;;
    --lam-ne-type)   LAM_NE_TYPE="$2"; shift 2 ;;
    # ★ 10차 자체 리뷰 — 아래 셋은 파싱만 되고 어디에도 전달되지 않았다.
    #   "바꿨다고 믿었는데 안 바뀐" 실험이 가장 위험하므로 즉시 실패한다.
    --c-rate|--v-upper|--v-lower)
      echo "지원 안 함: $1 — configs/*.yaml 의 experiment/cell 블록으로 지정하세요" >&2
      exit 1 ;;
    --noise)         NOISE="$2"; NOISE_SET="true"; shift 2 ;;
    --noise-seed)    NOISE_SEED="$2"; shift 2 ;;
    --objective)     OBJECTIVE="$2"; shift 2 ;;
    --bounds)        BOUNDS_PRESET="$2"; shift 2 ;;
    --n-restarts)    N_RESTARTS="$2"; shift 2 ;;
    --no-adaptive)   ADAPTIVE="false"; shift ;;
    --no-warm-start) WARM_START="false"; shift ;;
    --clean)         CLEAN="true"; shift ;;
    --limit)         LIMIT="$2"; shift 2 ;;
    --reference)     REFERENCE="$2"; shift 2 ;;
    --w-grid)        W_GRID="$2"; shift 2 ;;
    --w-stride)      W_STRIDE="$2"; shift 2 ;;
    --backend)       BACKEND="$2"; shift 2 ;;
    --nproc)         NPROC="$2"; shift 2 ;;
    --solver)
      echo "지원 안 함: --solver — configs/*.yaml 의 solver 블록으로 지정하세요" >&2
      echo "  (solver 는 완방상태 캐시·grid 서명에 봉인되므로 config 로만 바꿔야 한다)" >&2
      exit 1 ;;
    --chunk-size)    CHUNK_SIZE="$2"; shift 2 ;;
    --resume)        RESUME="true"; shift ;;
    --dry-run)       DRY_RUN="true"; shift ;;
    --in)            IN_DIR="$2"; shift 2 ;;
    --compare)       COMPARE_DIR="$2"; shift 2 ;;
    --out)           OUT="$2"; OUT_SET="true"; shift 2 ;;
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
    # ★ 10차 자체 리뷰 — `--noise 0` 을 명시해도 전달돼야 한다. 예전에는
    #   "0 이면 생략"이라 config 의 noise 축이 조용히 대신 쓰였다.
    [[ "$NOISE_SET" == "true" ]] && GRID_ARGS+=(--noise "$NOISE")
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
    # ★ --out을 명시하면 그걸 쓴다. 예전엔 --in이 있으면 무조건 --in으로 덮어써서
    #   사용자의 --out이 조용히 무시됐다 (스모크 결과가 본 실행 디렉터리를 오염시킴)
    if [[ "$OUT_SET" == "true" ]]; then
      FIT_ARGS+=(--out "$OUT")
    elif [[ -n "$IN_DIR" ]]; then
      FIT_ARGS+=(--out "$IN_DIR")
    fi
    [[ -n "$OBJECTIVE" ]] && FIT_ARGS+=(--objective "$OBJECTIVE")
    [[ "$N_RESTARTS" != "auto" ]] && FIT_ARGS+=(--n-restarts "$N_RESTARTS")
    [[ "$CLEAN" == "true" ]] && FIT_ARGS+=(--clean)
    FIT_ARGS+=(--reference "$REFERENCE")
    [[ -n "$LIMIT" ]] && FIT_ARGS+=(--limit "$LIMIT")
    [[ "$RESUME" == "true" ]] && FIT_ARGS+=(--resume)
    [[ "$ADAPTIVE" == "false" ]] && FIT_ARGS+=(--no-adaptive)
    [[ "$WARM_START" == "false" ]] && FIT_ARGS+=(--no-warm-start)
    exec python -m src.fitting "${FIT_ARGS[@]}"
    ;;

  score)      # Phase 5
    exec python -m src.scoring --in "${IN_DIR:-$OUT}" --log-level "$LOG_LEVEL"
    ;;

  hessian)    # Phase 5
    exec python -m src.hessian --in "${IN_DIR:-$OUT}" \
      --objective "${OBJECTIVE:-pocv_dvdq}" --log-level "$LOG_LEVEL"
    ;;

  wsweep)     # Phase 6 — dQ/dV 가중치 탐색 (층화 표본)
    WS_ARGS=(--in "${IN_DIR:-$OUT}" --nproc "$NPROC" --stride "$W_STRIDE"
             --bounds "$BOUNDS_PRESET" --reference "$REFERENCE"
             --log-level "$LOG_LEVEL")
    # ★ F79 — 사용자의 --out 을 전달한다. 예전에는 무시돼서, F70 분리 구조
    #   (curves 와 report 디렉터리가 다름)에서 report 가 읽는 위치에 sweep 을
    #   만들 방법이 wrapper 에 없었다.
    [[ "$OUT_SET" == "true" ]] && WS_ARGS+=(--out "$OUT")
    [[ -n "$W_GRID" ]] && WS_ARGS+=(--w-grid "$W_GRID")
    [[ "$N_RESTARTS" != "auto" ]] && WS_ARGS+=(--n-restarts "$N_RESTARTS")
    [[ "$RESUME" == "true" ]] && WS_ARGS+=(--resume)
    [[ "$ADAPTIVE" == "false" ]] && WS_ARGS+=(--no-adaptive)
    [[ "$WARM_START" == "false" ]] && WS_ARGS+=(--no-warm-start)
    exec python -m src.weight_sweep "${WS_ARGS[@]}"
    ;;

  report)     # Phase 6 — 비교표 + 그림 + RESULTS.md
    D="${IN_DIR:-$OUT}"
    python tools/compare_objectives.py --in "$D" --log-level "$LOG_LEVEL"
    # --compare 를 주면 기준 곡선 비교(Case 1 vs Case 2) 절도 함께 만든다
    if [[ -n "$COMPARE_DIR" ]]; then
      python tools/compare_cases.py --grid "$D" --halfcell "$COMPARE_DIR"         --log-level "$LOG_LEVEL"
    fi
    # ★ 18차 C 부수 발견 — `--mode report` 의 기본 출력은 **커밋된 정본**
    #   `docs/RESULTS.md` 다. scratch 실행(테스트·임시 디렉터리)이 그대로
    #   정본을 덮어썼다 (이 회차에 실제로 당했다). 정본 artifact 가 아니면
    #   기본 경로로 쓰지 않는다.
    REPORT_OUT="${REPORT_OUT:-}"
    if [[ -z "$REPORT_OUT" ]]; then
      case "$D" in
        results/*|./results/*) REPORT_OUT="docs/RESULTS.md" ;;
        *) REPORT_OUT="$D/RESULTS.md"
           echo "  ℹ 정본 경로가 아닌 입력($D)이라 보고서를 $REPORT_OUT 에 씁니다."
           echo "    정본을 갱신하려면 REPORT_OUT=docs/RESULTS.md 를 명시하세요." ;;
      esac
    fi
    exec python tools/make_results.py --in "$D" --out "$REPORT_OUT" --log-level "$LOG_LEVEL"
    ;;

  all)        # grid -> fit -> score -> report
    # 18차 C — 예전에는 사용자가 준 protocol 옵션(--objective·--n-restarts·
    #   --clean·--no-adaptive·--no-warm-start·noise 축)을 하위 단계로 넘기지
    #   않아, all 이 기본 protocol 로 돌면서 그 사실이 아무 데도 안 적혔다.
    # 18차 발견 7 — Hessian 은 인용 범위 밖 부록이라 기본 체인에서 뺀다.
    D="$OUT"
    RESUME_FLAG=()
    [[ "$RESUME" == "true" ]] && RESUME_FLAG=(--resume)

    GRID_ARGS=(--mode grid --config "$CONFIG" --nproc "$NPROC" --out "$D")
    [[ "${NOISE_SET:-false}" == "true" ]] && GRID_ARGS+=(--noise "$NOISE")
    [[ -n "${NOISE_SEED:-}" ]] && GRID_ARGS+=(--noise-seed "$NOISE_SEED")
    GRID_ARGS+=("${RESUME_FLAG[@]}")

    FIT_ARGS=(--mode fit --in "$D" --nproc "$NPROC"
              --bounds "$BOUNDS_PRESET" --reference "$REFERENCE")
    [[ -n "$OBJECTIVE" ]] && FIT_ARGS+=(--objective "$OBJECTIVE")
    [[ "$N_RESTARTS" != "auto" ]] && FIT_ARGS+=(--n-restarts "$N_RESTARTS")
    [[ "$CLEAN" == "true" ]] && FIT_ARGS+=(--clean)
    [[ "$ADAPTIVE" == "false" ]] && FIT_ARGS+=(--no-adaptive)
    [[ "$WARM_START" == "false" ]] && FIT_ARGS+=(--no-warm-start)
    FIT_ARGS+=("${RESUME_FLAG[@]}")

    # 전파를 실제 실행 없이 검사할 수 있게 한다 (회귀: tests/test_runner.py)
    if [[ "${RUN_SH_DRY:-0}" == "1" ]]; then
      echo "${GRID_ARGS[*]}"
      echo "${FIT_ARGS[*]}"
      echo "--mode score --in $D"
      echo "--mode report --in $D"
      exit 0
    fi

    "$0" "${GRID_ARGS[@]}"
    "$0" "${FIT_ARGS[@]}"
    "$0" --mode score --in "$D"
    exec "$0" --mode report --in "$D"
    ;;

  *)
    echo "알 수 없는 mode: $MODE" >&2
    usage
    exit 1
    ;;
esac

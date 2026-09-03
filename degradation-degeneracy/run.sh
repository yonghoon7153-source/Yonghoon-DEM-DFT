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
LEG="${LEG:-}"                    # 계획 index 의 다리 이름 (비우면 CANONICAL_RUN)
# ★ 49차 P0-3 — 실행권의 **소유 증명 파일** 경로. 이 스크립트가 coordinator 다:
#   한 번 발급해 여기 두고, grid·fit 하위 process 에 **경로로** 넘긴다 (token
#   자체는 argv 에 절대 싣지 않는다 — `ps` 로 새어 나간다). 비우면 다리 이름에서
#   유도한다. 48차에는 이 통로가 없어서 `--mode all` 이 grid 직후 fit 에서
#   자기 자신의 claim 때문에 거부됐다.

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
  finalize   ★ 49차 — 끝난 다리를 실행 기록으로 **닫는다** (all 은 자동)
  release    ★ 49차 — 중단된 실행권을 되돌린다 (계획을 planned 로)

실행 전 gate (★ 46차 P0-11 · 계약 §13.4)
  --leg NAME             `LEG_PRESERVATION.yaml` 의 `planned:` 에서 찾을 다리
                         이름. 비우면 CANONICAL_RUN. grid·fit·all 은 이 gate 를
                         **반드시** 지난다 (건너뛰는 환경변수는 없다).

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
  --halfcell-arg K=V     ocpbias 왜곡 값 (반복 가능). 캐시를 만들 때 준 값과
                         같아야 한다. 예: --halfcell-arg pe_offset_mv=10
  --halfcell-method M    ocp (기본) | ocpbias — half-cell 기준 곡선 생성 method.
                         ocpbias 는 OCP 에 계통 왜곡을 넣어 모델 오차 민감도를
                         잰다 (왜곡 크기는 python -m src.halfcell 로 캐시 생성 시 지정)
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
HALFCELL_ARGS=()          # --halfcell-arg 는 여러 번 올 수 있다 (set -u 대비)
while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode)          MODE="$2"; shift 2 ;;
    --leg)           LEG="$2"; export LEG; shift 2 ;;   # ★ 48차 P0-5 — export
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
    --halfcell-method) HALFCELL_METHOD="$2"; shift 2 ;;
    --halfcell-arg)  HALFCELL_ARGS+=("$2"); shift 2 ;;
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

#: ★ 19차 — `docs/RESULTS.md` 를 쓸 자격이 있는 **정본 실행**의 이름.
#:   다른 실행은 `docs/RESULTS_<run>.md` 로 간다 (정본 덮어쓰기 방지).
CANONICAL_RUN="${CANONICAL_RUN:-grid_fit_v4}"
export MPLBACKEND="Agg"          # headless 강제

# ---------------------------------------------------------------- 실행 전 gate
#: ★ 46차 P0-11 (계약 §13.4) — **비싼 실행은 계획 index 를 지나야 한다.**
#:
#:   그동안 보존 coverage 의 기준은 커밋된 투영이었다. 그래서 새 다리를 돌려도
#:   투영을 만들기 전에는 아무 회귀도 깨지지 않았고, 2026-08-20 에 warm 7다리를
#:   그렇게 돌렸다가 보존 없이 잃었다. 이제 `LEG_PRESERVATION.yaml` 의
#:   `planned:` 에 사람이 적은 항목이 있어야 하고, 그 항목이 승인한 RUN_SCOPE
#:   code identity 가 **지금과 같아야** 한다.
#:
#:   `--leg` 를 주지 않으면 `CANONICAL_RUN` 을 다리 이름으로 본다.
#:   gate 를 건너뛰는 환경변수는 두지 않는다 — 그런 문이 있으면 gate 가 아니다.
#: smoke 전용 산출 namespace. 이 아래로 나가는 산출은 **정본 실행이 아니다** —
#: `archive_results.sh`·보존 원장·`docs/RESULTS.md` 정본 경로가 받지 않는다.
#: gate 의 예외는 이 **namespace 하나**이고, 환경변수나 flag 로는 열 수 없다.
#: 한계: 같은 principal 이 비싼 실행을 이 namespace 로 밀어 넣는 것은 막지
#: 못한다. 다만 그렇게 하면 그 산출은 정본이 될 수 없다 (계약 §13.4).
SMOKE_NS="results/_smoke"

#: ★ 57차 P0-1 — **소유 증명 파일의 자리를 여기서 정하지 않는다.**
#: 51~56차는 이 자리를 shell 이 골라 `--attempt-file` 로 넘겼고, 그 인자가
#: authority 파일을 겨눌 수 있는 write-anywhere sink 였다. 막는 수단이
#: blacklist 증설뿐이라 매 라운드 새 sink 가 하나씩 남았다 (56차 판정).
#: 이제 자리는 `tools.preserve.attempts_root_for_ledger()` 가 원장에서
#: 유도하고, 이름은 `attempt_path_for(leg)` 가 정한다. shell 이 넘기는 것은
#: 다리 이름과 "내가 발급자다"(`--may-open`) 뿐이다.

plan_gate() {
  local leg="${LEG:-$CANONICAL_RUN}"
  # 면제는 **모든** 경로가 smoke namespace 안일 때만이다. 하나라도 밖이면
  # 그 실행은 정본 산출을 만들 수 있으므로 gate 를 지난다 (읽기 전용 입력만
  # 밖인 경우까지 막지만, 그 쪽으로 틀리는 편이 안전하다).
  # ★ 47차 P0-3 — 면제 판정을 **정규 격리**로 옮긴다. 46차 shell `case` 는
  #   문자열 prefix 라 `results/_smoke/../grid_fit_v4` 와 symlink 가 통과했다.
  #   판정은 `tools.preserve.is_inside_namespace()` 하나이고 모듈 gate 도
  #   같은 함수를 쓴다.
  # ★ 49차 P0-3 — 사전검사는 **새 발급**과 **내가 가진 재개**를 구분해야 한다.
  #   48차는 `assert_planned_leg()` 만 불렀고 그것은 `planned` 만 통과시켰다.
  #   그래서 grid 가 계획을 `running` 으로 옮긴 직후 같은 pipeline 의 fit
  #   사전검사가 **자기 자신 때문에** 거부됐다 — 정상 실행이 완주 불가였다.
  python - "$leg" "$OUT" "${IN_DIR:-}" <<'PYGATE'
import sys
from src.io import source_digest
from tools.preserve import (SMOKE_NAMESPACE, is_inside_namespace,
                            precheck_leg_run, PreserveError)

leg, out, in_dir = sys.argv[1], sys.argv[2], sys.argv[3]
paths = [p for p in (out, in_dir) if p]
if paths and all(is_inside_namespace(p, SMOKE_NAMESPACE) for p in paths):
    print("· 실행 전 gate 면제 — 모든 경로가 smoke namespace 안이다 (정규 격리)")
    raise SystemExit(0)
try:
    e = precheck_leg_run(leg, source_digest())
except PreserveError as exc:
    print(f"❌ 실행 전 gate 거부 — {exc}", file=sys.stderr)
    raise SystemExit(1)
if e["kind"] == "new":
    print(f"✅ 실행 전 gate 통과(사전 점검·새 발급) — {leg} · "
          f"cohort {e['cohort_id']} · 승인 {e['recorded_on']}")
else:
    print(f"✅ 실행 전 gate 통과(사전 점검·소유한 재개) — {leg} · "
          f"cohort {e['cohort_id']} · attempt {e['attempt_id'][:12]} · "
          f"끝난 phase {e['phases_done'] or ['없음']}")
PYGATE
}

# ★ 49차 P0-3 — 실행이 끝난 다리를 **닫는다.** 48차는 `phase_done()` 과
#   `finalize_leg()` 을 만들어 놓고 어느 production 경로도 부르지 않았다.
#   그래서 계획은 `running` 에 영원히 남았고, "실행 전 승인 → 실행 → 실행
#   기록" 의 마지막 변이 하나가 통째로 비어 있었다. lifecycle 은 닫히지
#   않으면 lifecycle 이 아니라 그냥 열어 두기다.
leg_finalize() {
  local d="$1"
  local leg="${LEG:-$CANONICAL_RUN}"
  python - "$leg" "$d" <<'PYFIN'
import sys
from src.io import source_digest
from tools.preserve import (SMOKE_NAMESPACE, is_inside_namespace,
                            finalize_leg, inspect_leg_run, PreserveError)

leg, out = sys.argv[1], sys.argv[2]
if is_inside_namespace(out, SMOKE_NAMESPACE):
    print("· 실행 기록 닫기 면제 — smoke namespace 다 (정본 실행이 아니다)")
    raise SystemExit(0)
try:
    view = inspect_leg_run(leg)
    r = finalize_leg(leg, {"leg_source_digest": source_digest(),
                           "cohorts": [view["cohort_id"]],
                           "out": out})
except PreserveError as exc:
    print(f"\u274c 실행 기록을 닫지 못했다 — {exc}", file=sys.stderr)
    raise SystemExit(1)
print(f"\u2705 실행 기록을 닫았다 — {leg} · attempt {r['attempt_id'][:12]} · "
      "preservation_status=preservation_pending "
      "(보존 묶음 만들기·검증은 별도 단계다)")
PYFIN
}

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
    # ★ 47차 P0-3 — dry-run 면제를 **없앴다.** 46차는 `--dry-run` 이면 gate 를
    #   건너뛰었는데, `run_grid(dry_run=True)` 는 출력 디렉터리를 만들고
    #   완방상태·baseline 을 계산한 뒤 최대 세 조건에 solver 를 실제로 부른다.
    #   "flag 면제는 없다" 와 정면으로 어긋났다.
    plan_gate
    # ★ 49차 P0-3 — 실행권의 소유 증명을 **경로로** 넘긴다. 처음이면 grid 가
    #   여기에 발급해 두고, fit 이 그 파일로 같은 실행에 붙는다.
    GRID_ARGS+=(--may-open)          # ★ 57차 P0-1 — 발급자는 coordinator
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
    # ★ half-cell 기준 곡선의 생성 method. 기본 ocp, 민감도 시험은 ocpbias.
    #   src/fitting.py 는 진작 받고 있었는데 run.sh 가 안 넘겨서 쓸 수 없었다.
    [[ -n "${HALFCELL_METHOD:-}" ]] && FIT_ARGS+=(--halfcell-method "$HALFCELL_METHOD")
    # ★ 왜곡 값. 이게 fit 까지 안 가면 fitting 은 왜곡 0 캐시 경로를 읽어
    #   민감도 0 을 조용히 보고한다 (recipe_hash 가 경로에 들어가므로).
    for _hca in "${HALFCELL_ARGS[@]:-}"; do
      [[ -n "$_hca" ]] && FIT_ARGS+=(--halfcell-arg "$_hca")
    done
    [[ -n "$LIMIT" ]] && FIT_ARGS+=(--limit "$LIMIT")
    [[ "$RESUME" == "true" ]] && FIT_ARGS+=(--resume)
    [[ "$ADAPTIVE" == "false" ]] && FIT_ARGS+=(--no-adaptive)
    [[ "$WARM_START" == "false" ]] && FIT_ARGS+=(--no-warm-start)
    # ★ fit 의 인자 조립도 실행 없이 검사할 수 있어야 한다 (report·all 과 대칭).
    #   없어서 --halfcell-method 전파를 회귀로 고정할 방법이 없었다.
    if [[ "${RUN_SH_DRY:-0}" == "1" ]]; then
      echo "${FIT_ARGS[*]}"
      exit 0
    fi
    plan_gate                       # ★ 46차 P0-11
    FIT_ARGS+=(--may-open)           # ★ 57차 P0-1
    exec python -m src.fitting "${FIT_ARGS[@]}"
    ;;

  finalize)   # ★ 49차 P0-3 — 다리를 **닫는다** (grid·fit 을 따로 돌렸을 때)
    # `--mode all` 은 이 단계를 스스로 부른다. 두 phase 를 손으로 나눠 돌렸거나
    # 중단 뒤 이어 돌린 경우에는 여기로 닫는다. 닫히지 않은 계획은 `running` 에
    # 남아 그 다리를 다시 시작할 수도 없게 만든다.
    D="${IN_DIR:-$OUT}"
    leg_finalize "$D"
    exit 0
    ;;

  release)    # ★ 49차 P0-3 — 실행권을 **되돌린다** (중단된 실행 정리)
    # dry-run 은 스스로 되돌리지만, 계산 도중 죽어 claim 만 남은 경우는 사람이
    # 정리해야 한다. 소유 증명이 있어야 하므로 남의 실행은 취소할 수 없다.
    python - "${LEG:-$CANONICAL_RUN}" <<'PYREL'
import sys
from tools.preserve import release_leg_run, PreserveError

leg = sys.argv[1]
try:
    r = release_leg_run(leg)
except PreserveError as exc:
    print(f"\u274c 실행권을 되돌리지 못했다 — {exc}", file=sys.stderr)
    raise SystemExit(1)
print(f"\u2705 실행권을 되돌렸다 — {leg} · attempt {r['attempt_id'][:12]} · "
      "계획은 planned 로 돌아갔다")
PYREL
    exit 0
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
    # ★ 18차 C 부수 발견 — `--mode report` 의 기본 출력은 **커밋된 정본**
    #   `docs/RESULTS.md` 다. scratch 실행(테스트·임시 디렉터리)이 그대로
    #   정본을 덮어썼다 (이 회차에 실제로 당했다). 정본 artifact 가 아니면
    #   기본 경로로 쓰지 않는다. 경로 결정은 **compare 실행 전에** 한다 —
    #   그래야 실행 없이 검사할 수 있다.
    REPORT_OUT="${REPORT_OUT:-}"
    if [[ -z "$REPORT_OUT" ]]; then
      # ★ 19차 — `results/` 아래여도 **정본 실행이 아니면** 정본을 덮으면 안 된다.
      #   예전 가드는 경로 패턴만 봐서 `results/fit_22p_v1` 같은 새 실행이
      #   그대로 `docs/RESULTS.md` 를 덮어썼다 (22p 격자 안내 중 발견).
      _run_name="$(basename "$D")"
      case "$D" in
        results/*|./results/*)
          if [[ "$_run_name" == "$CANONICAL_RUN" ]]; then
            REPORT_OUT="docs/RESULTS.md"
          else
            REPORT_OUT="docs/RESULTS_${_run_name}.md"
            echo "  ℹ 정본 실행($CANONICAL_RUN)이 아니라 보고서를 $REPORT_OUT 에 씁니다."
            echo "    정본을 갱신하려면 REPORT_OUT=docs/RESULTS.md 를 명시하세요."
          fi ;;
        *) REPORT_OUT="$D/RESULTS.md"
           echo "  ℹ 정본 경로가 아닌 입력($D)이라 보고서를 $REPORT_OUT 에 씁니다."
           echo "    정본을 갱신하려면 REPORT_OUT=docs/RESULTS.md 를 명시하세요." ;;
      esac
    fi
    if [[ "${RUN_SH_DRY:-0}" == "1" ]]; then
      echo "--mode report --in $D --out $REPORT_OUT"
      exit 0
    fi
    python tools/compare_objectives.py --in "$D" --log-level "$LOG_LEVEL"
    # --compare 를 주면 기준 곡선 비교(Case 1 vs Case 2) 절도 함께 만든다
    if [[ -n "$COMPARE_DIR" ]]; then
      python tools/compare_cases.py --grid "$D" --halfcell "$COMPARE_DIR"         --log-level "$LOG_LEVEL"
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
    # ★ 46차 P0-11 — 실행 전 gate 의 대상 다리를 하위 단계로 **전파**한다.
    #   안 넘기면 하위 grid·fit 이 CANONICAL_RUN 으로 gate 를 보게 되어,
    #   사용자가 지정한 다리와 다른 계획 항목으로 승인될 수 있다.
    [[ -n "$LEG" ]] && GRID_ARGS+=(--leg "$LEG")
    # ★ 49차 P0-3 — `all` 이 **coordinator** 다. 소유 증명 경로 하나를 정해
    #   grid 와 fit 두 하위 호출에 똑같이 넘긴다. 이것이 없으면 grid 가 딴
    #   실행권을 fit 이 이어받을 방법이 없어 pipeline 이 완주하지 못한다.
    GRID_ARGS+=(--may-open)          # ★ 57차 P0-1
    [[ "${NOISE_SET:-false}" == "true" ]] && GRID_ARGS+=(--noise "$NOISE")
    [[ -n "${NOISE_SEED:-}" ]] && GRID_ARGS+=(--noise-seed "$NOISE_SEED")
    GRID_ARGS+=("${RESUME_FLAG[@]}")

    FIT_ARGS=(--mode fit --in "$D" --nproc "$NPROC"
              --bounds "$BOUNDS_PRESET" --reference "$REFERENCE")
    # ★ all 모드도 half-cell 축을 넘겨야 한다. 안 넘기면 하위 fit 이 method
    #   기본값 ocp 로 무왜곡 캐시를 읽고 **끝까지 성공**한다 — 어느 가드에도
    #   안 걸려서, 민감도를 쟀다고 믿는 10시간 실행이 왜곡 0 이 된다.
    [[ -n "${HALFCELL_METHOD:-}" ]] && FIT_ARGS+=(--halfcell-method "$HALFCELL_METHOD")
    for _hca in "${HALFCELL_ARGS[@]:-}"; do
      [[ -n "$_hca" ]] && FIT_ARGS+=(--halfcell-arg "$_hca")
    done
    [[ -n "$LEG" ]] && FIT_ARGS+=(--leg "$LEG")       # ★ 46차 P0-11
    FIT_ARGS+=(--may-open)           # ★ 49차 P0-3 · 57차 P0-1
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
    # ★ 49차 P0-3 — **여기서 닫는다.** 48차는 `phase_done()`·`finalize_leg()`
    #   을 만들어 놓고 어느 production 경로도 부르지 않았다. 그래서 계획은
    #   `running` 에 영원히 남고, 그 다리는 다시 시작할 수도 닫을 수도 없었다.
    leg_finalize "$D"
    "$0" --mode score --in "$D"
    exec "$0" --mode report --in "$D"
    ;;

  *)
    echo "알 수 없는 mode: $MODE" >&2
    usage
    exit 1
    ;;
esac

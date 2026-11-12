#!/usr/bin/env bash
# kgy 실행 환경 판에서 R 경로 시험 — kgy `~/dem-venv` = Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1 (1저자 10-24 출력).
# 개발 · 게이트 (3.11) 에서만 돌던 코드가 kgy 에서 멈춘 일 (`SELF-132` · 08-16 · 08-25 에 이어 세 번째) 을 다시 막는다 — 1저자 10-24 Q2 (가).
# 인터프리터 = $KGY_PY38 (기본 = `uv python find 3.8`) · 없거나 판이 다르면 실패한다 (건너뛰지 않는다) → `bash scripts/setup_kgy_py38.sh`.
# 묶음 = S0 · S1 · S2/S3 · 계약 · 사슬 · 끝-끝 (실제 러너 · payload) · 12 단위 끝-끝 (11-11) · 증서 · ⑥ 탐침 (판독기 · 감시 셸 · 블록 · 11-10) · GPU 전처리 C 꼴 ·
#   탄소 접합 원장 저장본 · 저장본 끝-끝 (11-12 · Q11 · Q2 코드 묶음 · 내부 반박 리뷰 RCP-02) · git 환경 격리 (11-12 2 회차 RCP2-06) — 증거
#   `docs/reviews/rint2_py38_compat_evidence_20261024/`.
set -uo pipefail
#  ★ 2026-11-12 3 회차 (Rint ② 코드 묶음 · 내부 반박 리뷰 재확인 2 RCP3-05 · 본 세션 결정) — 저장소 고르는 GIT_* · 설정 주입을 한 번 지운다 (git 훅 ·
#    GIT_DIR 을 붙인 셸 안에서 돌려도 모든 단계가 남의 저장소를 읽고 쓰지 않게 · 격리 변수 = 천장 · 전역 설정 끄기는 남긴다) — 글자 = run_contract.GIT_DROP_SH
#    (시험 scripts/test_git_env_isolation.py G8 이 자리 · 글자 · 동작을 대조)
for _gv in $(compgen -e); do case "$_gv" in (GIT_DIR|GIT_WORK_TREE|GIT_INDEX_FILE|GIT_OBJECT_DIRECTORY|GIT_ALTERNATE_OBJECT_DIRECTORIES|GIT_COMMON_DIR|GIT_NAMESPACE|GIT_PREFIX|GIT_CONFIG_PARAMETERS|GIT_CONFIG_COUNT|GIT_CONFIG_KEY_*|GIT_CONFIG_VALUE_*) unset "$_gv";; esac; done
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="${KGY_PY38:-$(uv python find 3.8 2>/dev/null || true)}"
if [ -z "$PY" ] || [ ! -x "$PY" ]; then
  echo "✗ kgy 판 python3.8 없음 — bash scripts/setup_kgy_py38.sh (uv · 네트워크 · 컨테이너 재시작 뒤 한 번)"
  exit 2
fi
if ! "$PY" - <<'PYEOF'
import sys
want = ((3, 8), '1.24.4', '1.10.1')
try:
    import numpy
    import scipy
except Exception as e:                                     # noqa: BLE001
    print(f'✗ numpy · scipy 를 불러오지 못했다: {type(e).__name__}: {e}')
    sys.exit(1)
got = (tuple(sys.version_info[:2]), numpy.__version__, scipy.__version__)
if got != want:
    print(f'✗ 판이 kgy 와 다르다 — 기대 {want} · 실제 {got}')
    sys.exit(1)
print(f'  kgy 판 = Python {sys.version.split()[0]} · numpy {numpy.__version__} · scipy {scipy.__version__} ({sys.executable})')
PYEOF
then
  echo "  → bash scripts/setup_kgy_py38.sh"
  exit 2
fi
export PATH="$(dirname "$PY"):$PATH"
unset VIRTUAL_ENV
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$ROOT"
LOG="${KGY_PY38_LOGDIR:-$(mktemp -d -t kgy_py38_XXXX)}"
mkdir -p "$LOG"
fail=0
run() {
  local name=$1; shift
  if "$PY" "$@" > "$LOG/$name.log" 2>&1; then
    echo "  ✓ $name :: $(tail -1 "$LOG/$name.log" | cut -c1-110)"
  else
    echo "  ✗ $name :: $(grep -E 'FAIL|Error|✗' "$LOG/$name.log" | grep -v -E '(^|[^0-9])0 FAIL' | head -3 | cut -c1-160 | tr '\n' ' ') (로그 $LOG/$name.log)"
    fail=1
  fi
}
run run_contract scripts/run_contract.py --selftest
run step3_rint scripts/step3_sigma.py --selftest-rint
run ptfe_face_alpha scripts/test_ptfe_face_alpha.py
run carbon_junction scripts/test_carbon_junction.py
run ca_ext_b6 scripts/test_ca_ext_b6.py
run ca_ext_runner scripts/test_ca_ext_runner.py
run rint_r_chain scripts/test_rint_r_chain.py
run rint_r_chain_e2e scripts/test_rint_r_chain_e2e.py
run rint_r_chain_e2e12 scripts/test_rint_r_chain_e2e12.py
run step3_target_cert scripts/test_step3_target_cert.py
run step3_conv_cert scripts/test_step3_conv_cert.py
run ca_s0_census scripts/test_ca_s0_census.py
run probe6 docs/reviews/rint2_probe6_prep_20261110/tools/test_probe6_read.py
run step3_gpu_precond scripts/test_step3_gpu_precond.py
run cjunc_store scripts/test_cjunc_store.py
run cjunc_store_e2e scripts/test_cjunc_store_e2e.py
run git_env_isolation scripts/test_git_env_isolation.py
if [ "$fail" -ne 0 ]; then echo "✗ kgy 판 R 경로 시험 실패 (로그 $LOG)"; exit 1; fi
echo "✓ kgy 판 R 경로 시험 17 묶음 통과"

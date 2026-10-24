#!/usr/bin/env bash
# kgy 실행 환경 판에서 R 경로 시험 — kgy `~/dem-venv` = Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1 (1저자 10-24 출력).
# 개발 · 게이트 (3.11) 에서만 돌던 코드가 kgy 에서 멈춘 일 (`SELF-132` · 08-16 · 08-25 에 이어 세 번째) 을 다시 막는다 — 1저자 10-24 Q2 (가).
# 인터프리터 = $KGY_PY38 (기본 = `uv python find 3.8`) · 없거나 판이 다르면 실패한다 (건너뛰지 않는다) → `bash scripts/setup_kgy_py38.sh`.
# 묶음 = S0 · S1 · S2/S3 · 계약 · 사슬 · 끝-끝 (실제 러너 · payload) · 증서 — 증거 `docs/reviews/rint2_py38_compat_evidence_20261024/`.
set -uo pipefail
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
run step3_target_cert scripts/test_step3_target_cert.py
run step3_conv_cert scripts/test_step3_conv_cert.py
run ca_s0_census scripts/test_ca_s0_census.py
if [ "$fail" -ne 0 ]; then echo "✗ kgy 판 R 경로 시험 실패 (로그 $LOG)"; exit 1; fi
echo "✓ kgy 판 R 경로 시험 11 묶음 통과"

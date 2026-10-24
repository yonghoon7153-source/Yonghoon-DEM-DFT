#!/usr/bin/env bash
# kgy 판 재현 인터프리터 설치 — 컨테이너 재시작 뒤 한 번 (uv · 네트워크).  게이트 단계 `scripts/check_kgy_py38.sh` 가 쓴다.
# 판 = kgy `~/dem-venv` (1저자 10-24 출력: Python 3.8.10 · numpy 1.24.4 · scipy 1.10.1) · 나머지 = 시험이 부르는 것 (kgy 의 판 확인 전 · `SELF-132`).
# venv 를 쓰지 않는다 — 시험의 가짜 `python3` 심이 인터프리터 경로를 그대로 다시 부르므로 패키지를 그 인터프리터에 직접 둔다.
set -euo pipefail
uv python install 3.8
PY="$(uv python find 3.8)"
uv pip install --python "$PY" --system --break-system-packages \
  numpy==1.24.4 scipy==1.10.1 scikit-image==0.21.0 matplotlib==3.7.5 threadpoolctl==3.5.0 plotly==7.1.0 pyamg==5.1.0
"$PY" -c "import sys, numpy, scipy; print('kgy 판 =', sys.version.split()[0], numpy.__version__, scipy.__version__, sys.executable)"

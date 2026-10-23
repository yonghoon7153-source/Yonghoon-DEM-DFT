"""Battery Lab Workbench API.

**수치 라이브러리(BLAS)의 스레드는 하나다** (ADR 0048 보완 1).  numpy 를 처음
import 하기 전에 정해야 해서 패키지의 맨 앞, 여기에 둔다 -- `uvicorn app.main:app`
은 `app.main` 보다 이 파일을 먼저 읽는다.

numpy 의 OpenBLAS 는 기본으로 코어 수만큼 스레드를 띄운다.  이 앱의 행렬은 작고
(DRT 260×93, KK 의 lstsq) 서버는 요청마다 스레드를 따로 쓰므로, 작은 계산 하나에
스레드 여럿이 붙어 서로 기다린다.  실측 (4 코어): 260×93 lstsq 65.8 ms → 2.25 ms,
DRT λ 훑기 1.0 초 → 0.044 초, 스펙트럼 상세 화면 첫 열기 1.21 초 → 0.41 초 — 다른
일이 같이 돌 때는 4 초가 넘기도 했다.

`setdefault` 라서 밖에서 값을 주면 그것이 이긴다 (`OPENBLAS_NUM_THREADS=4 bml`).
"""

import os

for _name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_name, "1")

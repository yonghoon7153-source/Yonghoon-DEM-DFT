# DEM 재설계 방향 v3.1 — 독립 리뷰 전달본

기준 핀 `13eb293cd9ac44502517c81e8f5e9b7ae02d817f`, 문헌 카드 핀 `0991161693d2d8f36975f2c9454472b54bb11c2c`.

먼저 `codex_review_dem_redesign_direction_20261110.md`를 읽는다. 방향 지지, 현 인과·분기·자격 규칙 수정 필요, 전체 HOLD 유지다. 새 지적은 P1 2건·P2 10건·P3 1건이며 `findings_review.json`에 정리했다. 단계 5의 AM 재밍 경고는 후속 등록 주의로 분리했다. 이 파일은 프로젝트 원장에 기록하거나 항목을 종결하지 않는다.

## 내용

- `package/`: 사용자가 보낸 ZIP의 고정 파일48개, 원래 PIN/SHA256SUMS 포함. repo30·litdb16 모두 원격 고정 Git blob과 대조했다.
- `remote_pin_provenance.json`, `remote_blob_comparison.json`: 원격 두 핀·트리와 파일별 대조 기록. 이것이 물리 타당성이나 실행 자격을 뜻하지 않는다.
- `remote_sources/`: 고정 핀에서 보충 읽은 원 기록4개와 그 blob/바이트 검산. 원 런 결과를 실행한 것이 아니다.
- `branches_review/`, `physics_review/`, `code_arithmetic_review/`: 독립 소형 탐침·결과·상세 메모. 상세 메모의 임시 ID는 findings_review.json에서 DRD ID와 연결된다. 합계는 통합 DRD13개이며 하위 검토의 중복 지적을 합산하지 않는다.
- `expected/`: 제출 때 보존한 probe JSON3개. 재현 결과와 비교한다.
- `reproduction/`: 통합 재현 stdout/stderr·환경·결과 영수증.
- `physics_review/SOURCES.md`: 공개 1차 문헌 확인 범위·URL·페이지. 새로 읽은 논문 전문을 넣지 않았다. 그림 정밀 digitization 등 미확인 부분도 기재했다.

## 작은 검산만 다시 실행

Python3 및 NumPy/SciPy가 있는 환경에서 이 ZIP의 최상위 파일을 실행한다.

```bash
python -I -X utf8 -B reproduce_review.py
```

입력 해시·저장된 Git blob 메타데이터 검산 뒤 독립 분기 열거/수치 근 찾기/격자점 산술만 실행한다. 프로젝트 모듈·Taichi·LIGGGHTS는 import/실행하지 않는다. 순수 스칼라 `f_load_numpy` 함수만 AST로 추출하여 단일 접촉의 합성 인자로 호출한다. 네트워크·Git·원격 호스트·전체 게이트 명령은 없다. 명령은 `expected/`나 입력을 수정하지 않고 생성된 probe JSON과 `reproduction/`만 쓴다.

검토 환경: Windows 로컬 Python3.12.14, NumPy2.5.3, SciPy1.16.3. 실제 연구 런0건. 다른 OS·버전에서 실행한 자격을 주장하지 않는다. 부동소수 재현 비교 허용차는 검토 산술용 rtol1e-10/atol1e-11이며 연구 판정 허용폭이 아니다.

`input_verification.json`의 최초 입력 파일 경로는 검토자 PC의 기록이다. 그 파일이나 세부 메모에 남은 절대 경로는 다른 PC의 실행 지시가 아니다. 재현에는 위 상대 경로 명령을 쓴다.

## 범위

실제 MPM/DEM·GPU·ibb/WSL·원 연구 데이터 접근·등록·운영 봉인·원장 종결·통합·배포를 승인하거나 수행하지 않았다. 랩 표준10–13%, TD1.64, 두 트랙 분리 및 Rint② 우선이라는 기존 결정을 재선택하지 않았다. 판정문과 증거를 1저자가 후속 작업자에게 전달한다.

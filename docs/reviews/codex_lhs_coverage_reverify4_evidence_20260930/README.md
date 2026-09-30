# 재검증 4 독립 증거

이 폴더의 결과는 제출자의 `submitted/.../fixed_tree_reproduction/`와 별도 실행이다. 생산 소스는 고치지 않았고, 이전 후보의 복사본에 제출 패치 0016·0017만 적용했다. 파일 핀은 상위 `source_manifest.json`, 최종 보고서는 작업공간 `docs/reviews/codex_lhs_coverage_reverify4_verdict_20260930.md`다.

## 실행

현재 작업공간에서 다음처럼 실행한다. Python 3.12.14와 기존 격리 의존성 `lhs_coverage_review_20260930/deps`를 사용한다. 코드 묶음은 전체 저장소/의존성 배포판이 아니므로 다른 기계에서는 완전한 후보 소스와 같은 의존성 배치가 필요하다. 네트워크·DEM·설치 엔진·실 데이터 배치는 호출하지 않는다.

~~~powershell
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
$reviewPython='C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $reviewPython lhs_coverage_reverify4_20260930/evidence/audit_r5.py
& $reviewPython lhs_coverage_reverify4_20260930/evidence/audit_r4.py
& $reviewPython lhs_coverage_reverify4_20260930/evidence/audit_schema.py
& $reviewPython lhs_coverage_reverify4_20260930/evidence/audit_numeric_domain.py
& $reviewPython lhs_coverage_reverify4_20260930/evidence/audit_producer.py
& $reviewPython lhs_coverage_reverify4_20260930/evidence/audit_error_3d.py
& $reviewPython lhs_coverage_reverify4_20260930/evidence/audit_geometry.py
& $reviewPython lhs_coverage_reverify4_20260930/evidence/audit_power_boundary.py
& $reviewPython lhs_coverage_reverify4_20260930/evidence/run_selftests.py
& $reviewPython lhs_coverage_reverify4_20260930/evidence/audit_regression.py
~~~

## 파일 설명 · 한정

- `audit_r5.py` / `r5_results.json`: 이번 신규 검산. pin 상태 8종, 실제 `compute_case`의 0접촉/부분/전체 클립 3종, 기존 하한 음성 대조, 전체 클립 상별 통계 변이 2종, 수치 영역 검산. 실행 첫 시도는 시험 준비의 `full_metrics.json` 누락으로 중단돼 준비 코드를 수정했다. 이는 제품 결함으로 세지 않았으며 보존된 JSON은 수정된 시험의 완료 결과다.
- `r5_fixtures/producer`: 실제 생산 함수의 입력 atoms/contacts 및 산출물. 정적 합성 접촉 자료이며 DEM 평형 상태나 실 코퍼스의 분포가 아니다.
- `r5_fixtures/mutations`: 정상 생산자 출력의 한 필드 변이. 하위 프로세스만 레코드 전달기로 대체하고 실제 필수 단계·검증기·summarize를 호출했다. 웹앱 HTTP 전체 경로 실행은 아니다.
- `unverified_phase_weight_example`: 부분 클립에서 전체 평균만 바꾼 탐색 대조. 상별 수가 스키마에 없는 일반 가중 문제를 새 결함으로 확정하는 데 쓰지 않았다. 보고서의 P2 증거는 전체 클립 두 변이로 한정한다.
- `audit_r4.py`, `audit_schema.py`: 이전 독립 반례와 정상 대조를 무변경 재실행. 각각 `_results.json`에 전체 레코드가 있다.
- `audit_producer.py`: 공개 식의 스칼라 산술 이식이며 설치 C++ 빌드 실행이 아니다. 이전 검토 때 읽은 공개 식을 그대로 사용했다.
- `audit_error_3d.py`, `audit_geometry.py`, `audit_power_boundary.py`: 유한 합성 표본. 전역 증명이나 실 데이터 통계가 아니다.
- `run_selftests.py`: 원본 selftest의 로그를 그대로 보존한다. harvest/batch의 Windows 환경 실패를 숨기지 않는다.
- `audit_regression.py`: LF fixture·byte-copy 보조 대조와 옛 36키×16호출 비교. byte-copy 대조는 실제 배포 symlink를 인증하지 않는다.
- 일부 수치 진단 JSON은 Python의 `Infinity` 표현을 담는다. 감사용 결과 파일이며 웹앱 생산 JSON 스키마의 적합성 시험이 아니다.

신규 P2는 LHSC-03-R5 하나이며, 비차단 P3는 LHSC-04-R5-PIN-TYPE / LHSC-04-R5-DOMAIN이다. 이전 R4의 두 P2는 닫힘으로 구분했다. 생산 원장에는 상태를 쓰지 않았다.

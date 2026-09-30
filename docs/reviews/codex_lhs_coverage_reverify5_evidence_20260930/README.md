# 재검증 5 독립 증거

보고서: 작업공간 `docs/reviews/codex_lhs_coverage_reverify5_verdict_20260930.md`. 소스 핀은 상위 `source_manifest.json`. 이전 후보를 보존하고 별도 비 Git 사본에 0018→0019만 적용했다. 생산 원장·Git ref·실 데이터는 수정하지 않았다.

## 실행 환경과 재현

Python 3.12.14, 기존 격리 의존성 `lhs_coverage_review_20260930/deps` 사용. 묶음은 전체 저장소나 의존성 배포판이 아니므로 다른 환경에서는 완전한 후보 소스와 해당 의존성 경로가 필요하다. 모든 시험은 합성 CPU 시험이다. DEM·설치 엔진·원격 캠페인·실 재수확은 실행하지 않는다.

~~~powershell
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
$reviewPython='C:/Users/Administrator/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $reviewPython lhs_coverage_reverify5_20260930/evidence/audit_r5.py
& $reviewPython lhs_coverage_reverify5_20260930/evidence/audit_r6.py
& $reviewPython lhs_coverage_reverify5_20260930/evidence/audit_r4.py
& $reviewPython lhs_coverage_reverify5_20260930/evidence/audit_schema.py
& $reviewPython lhs_coverage_reverify5_20260930/evidence/run_selftests.py
& $reviewPython lhs_coverage_reverify5_20260930/evidence/audit_regression.py
& $reviewPython lhs_coverage_reverify5_20260930/evidence/audit_numeric_domain.py
& $reviewPython lhs_coverage_reverify5_20260930/evidence/audit_producer.py
& $reviewPython lhs_coverage_reverify5_20260930/evidence/audit_error_3d.py
& $reviewPython lhs_coverage_reverify5_20260930/evidence/audit_geometry.py
& $reviewPython lhs_coverage_reverify5_20260930/evidence/audit_power_boundary.py
~~~

이 스크립트 전부 이번 후보에서 실행했다. 제출자의 `submitted/.../fixed_tree_reproduction/`와 이 폴더는 별도 증거다.

## 신규 독립 대조

`audit_r6.py`는 단일 AM 상, 상별 입자 수가 다른 부분/전체 클립, 비영 std 부분 클립을 실제 `compute_case`로 생산한다. 합성 atoms/contacts는 `r6_fixtures/producer`에 보존한다. 물리적으로 평형인 DEM 침대의 인증이 아니다.

끝점 변이 5개는 실패, 정상 끝점 2개는 통과해야 하며 실제 필수 단계까지 호출한다. pin 자료형 10종과 정상/불일치 5종을 `producer_pin` 및 `contact_area_check.producer_model` 양쪽에서 확인한다. 이 기대는 assert로 고정했다.

추가로 메모리에서만 검사 함수 하나를 이전 후보의 실제 함수로 교체한 뒤 현재 pipeline selftest를 실행한다. T11s·T11t만 실패하는 214/216 결과를 assert한다. 파일 수정·Git 되돌림은 하지 않는다. 결과는 `r6_results.json`, 전체 상주 시험 로그는 `resident_rollback.log`다.

`audit_r5.py`의 `unverified_phase_weight_example`은 이전부터 보존한 부분 클립 탐색 대조다. 일반적인 상별 개수 없는 스키마의 가중 완전성을 인증하는 데 쓰지 않았고, 이번 닫힘 대상 전체 클립 반례와 구분한다.

## 한정

- 변이 시험은 계산 subprocess만 합성 레코드 전달기로 대체한다. 실제 웹앱 HTTP 전체 경로나 배포 실행 인증이 아니다.
- 수치 스트레스는 공개 식의 산술 검산과 유한 표본이며 설치 엔진·전역 증명이 아니다.
- 일부 감사 JSON의 Infinity는 E=∞ 미인증 기록이다. 엄격 JSON 웹앱 배포 계약을 검증한 산출물이 아니다.
- harvest/batch 원본 selftest의 기존 Windows 환경 실패를 로그에 그대로 보존했다. LF fixture / byte-copy 보조 대조는 실제 배포 환경 인증과 다르다.
- GO는 이번 HOLD 해제 및 통합 게이트 진행 범위다. 실제 통합 뒤 운영 환경 게이트와 해시 봉인을 생략하라는 뜻이 아니다.

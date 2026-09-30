# LHS 피복률 재검증 2 독립 증거

2026-09-30. 판정: `docs/reviews/codex_lhs_coverage_reverify2_verdict_20260930.md`.

입력 ZIP SHA256: `8761667a740c0962502c12db5605fd1c7b43d1ab1110267de1df13051275b235`.
제출 tip 이름: ca0471d19. 인증한 것은 패치 바이트와 적용 후 파일 SHA이며 원격에 없는 커밋 객체 자체가 아니다.

## 검토와 실행 경계

- 생산 checkout·Git ref·원장은 변경하지 않았다. 이전 후보를 복사한 비 Git 디렉터리에 0012/0013만 적용했다.
- DEM/원격/실 130·64 재수확·coverage 생산 배치는 실행하지 않았다.
- 웹앱 서버와 외부 DB를 실행하지 않았다. app import 시 Supabase 설정은 비웠다.
- 합성 CPU 함수 시험, 제출 selftest, 독립 Decimal 산술을 수행했다.
- `submitted/`는 제출자 증거다. `evidence/`가 독립 재현 결과다. 둘을 구별한다.

## 내용

- `prepare.py` / `source_manifest.json`: ZIP 경로 검사, 이전 후보 9파일 SHA 확인, 제출 SHA256SUMS 7항목·패치 diff 해시 대조, 별도 소스 사본 적용.
- `audit_schema.py` / `schema_results.json` / `schema_fixtures/`: 실제 compute_case 양성 8종, 옛 변이 10종, 추가 스키마 변이. 필수 단계 시험은 계산 subprocess만 대역; 검증기와 summarize는 실제 함수.
- `audit_geometry.py` / `geometry_results.json`: 옛 반례, 비접촉/포함/얕은 경계 대조, 12,000상자·288,000점의 독립 Decimal 80자리/실제 로컬 함수 대조. 유한 샘플이지 전역 증명 아님.
- `audit_power.py` / `power_results.json`: +1% 치환을 놓치면서 n_power_1pct=1로 분류하는 반례. seed 4813, 431번째 상자.
- `audit_producer.py` / `producer_results.json`: 공개 LIGGGHTS add_pair 산술을 연산 순서대로 옮긴 binary64 스칼라 시험. **LIGGGHTS 전체 실행이나 사용자의 설치 빌드 인증 아님.** 소스 URL/열람 일자는 스크립트와 판정문에 명시.
- `run_selftests.py` / `selftests.json` / 해당 로그: 원형 실행의 성공과 실패 모두 보존.
- `audit_regression.py` / `regression_results.json`: LF fixture 및 symlink→byte-copy를 명시한 Windows 통제. source 수정 없음. legacy 36키×16 호출 및 τ 기준/후보 비교.

## 재현

Python 3.12.14, NumPy/pandas/SciPy/NetworkX/Flask 등이 있는 환경이 필요하다. 완전한 후보 저장소는 이전 검토 트리에 패치 0012→0013을 적용해 별도로 준비한다. ZIP은 대상 파일 및 증거만 포함한다.

원래 작업 공간에서는 다음 명령으로 실행했다. 스크립트는 현재 `lhs_coverage_reverify2_20260930/candidate`, 이전 `lhs_coverage_review_20260930/{baseline,deps}`를 상대 경로로 찾는다. 다른 환경에서는 각 스크립트 맨 위 경로를 해당 격리 사본으로 지정한다. 재실행은 증거 사본에서 할 것: 결과 JSON/fixture를 다시 쓴다.

~~~powershell
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
python lhs_coverage_reverify2_20260930/evidence/audit_schema.py
python lhs_coverage_reverify2_20260930/evidence/audit_geometry.py
python lhs_coverage_reverify2_20260930/evidence/audit_power.py
python lhs_coverage_reverify2_20260930/evidence/audit_producer.py
python lhs_coverage_reverify2_20260930/evidence/run_selftests.py
python lhs_coverage_reverify2_20260930/evidence/audit_regression.py
~~~

`prepare.py`는 검토 디렉터리가 이미 있으면 거부한다. 원본을 덮어쓰는 재현 명령이 아니다.

## 남은 상태

옛 10개 스키마 변이와 옛 공동 반올림 오탐은 수정됐다. 정상 산출물 8개도 통과한다. 남은 HOLD 사유는 분율/원장 결손의 false-green, 생산자 산술 오차 보증의 한계, 1% 검출력 표지의 반례다. 새 P1은 발견하지 않았다. 심각도·한정·최소 해제는 판정문을 따른다.

Windows 원형 selftest 실패를 없던 것으로 세지 않는다. 실 코퍼스 발생률·물리 모델 적격성·설치 producer의 빌드 규약·병합 후 전체 gate는 이번 실행이 인증하지 않는다.

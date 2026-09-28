# 정상조건 fresh 0→30초 — 오프라인 후보

2026-09-28. 사용자 `ㄱ ㄱ`에 따라 채택된 준비 범위만 수행했다. **후보 작성·정적 대조 완료 / 변경부 기능 검증 미실행 / native 실행 미승인**이다. 이번 자료를 바로 실행하라는 명령으로 사용하지 않는다.

고정 후보 manifest: `28dd6da5cc76885263c17b2671548a00692064807e02e77ceb6f3edbdd946fa5`.
run_id: `normal30_candidate_001`.
원 source: `outputs/normal30_offline_preparation_20260928/`.
전달 ZIP의 사본에서 실행하거나 ROOT를 바꾸지 않는다.

## 바뀐 부분

- Java: 정상 임계값 0, 최대30초, 출력 시간 상한30, 목적 표식. 기존0–5초 요청187개를 그대로 두고5.1–30초0.1초 간격250개를 추가했다. 요청437개이며 실제 저장 상태 개수는 고정하지 않는다.
- 소비자: 정상30초·보호중단·오류 분리, 전체 교집합과 비교 부분집합 구분, 초기Li 각항 대조, 실제 시간설정 read-back 소비,5초 이후 요약.
- 실행 연결: 새run/승인 경로, 제안 예산, 새 분석 결과명. 기존 C2 입력 본문·소유 Job 전송 모듈·정책 무변경 연결을 재사용한다.
- 부모: 실제 판정 함수가 새 결과 구조와 rc0/rc1을 소비한다. 최종 기록은 스크립트 완료 경계이며 `-NoExit` PowerShell 프로세스 종료코드를 만들지 않는다.

Java 허용 literal들을 역치환하면 수용된1198 Java 전체 바이트와 일치한다. 물성/OCP·초기화·물리/입자 해상도·전류·sigma·수치 cap/rtol·보호식·출력 API·오류 보존 본문은 유지했다. threshold0은 기존 정상조건 복귀이며1198 시험값을 생산 임계값으로 쓰지 않는다.

## 확인 수준

`STATIC_SOURCE_CHECKS.json`, `FINAL_STATIC_CHECKS.json`은 JSON/해시/소스 텍스트·Python AST 구문 분석이다. 후보 import/함수 실행, 수신 suite/probe, COMSOL/JVM/컴파일, 콘솔/Job 시험은 모두0회다. 자체 파일 작성·정적 검사 스크립트와 일반 도구 셸은 사용했다. PowerShell 후보를 파서나 엔진에 넘겨 실행하지 않았다.

38개 선택 원본의 전후 식별을 비교했다. 원격 PC 전체 보존이나 MPH의 재검증으로 확대하지 않는다. 기존1198 실제 실행과 B020 회수·시각화·전압 분해는 재실행하지 않았다.

## 다음 한 건

`LIMITED_VALIDATION_PLAN.json` / `LIMITED_VALIDATION_APPROVAL_DRAFT_KO.md`의 **새 변경부 한정 검증**을 대상으로 별도 승인한다. 시험 결과 수용 후 이 고정 실행본의 정책 무변경 native30초 최대1회를 다시 승인하는 순서다. 이번 ZIP에 실제 승인·release·runtime·token·USER_DECISION은 없다.

전체/정상 gate INCOMPLETE, 내부 실효 정책 UNVERIFIED, 전체 수렴·장기 운전 보류를 유지한다. 30초 완료도 실험 타당도·장기 예측 수렴의 PASS가 아니다. 기존 실패/pending/원복·recipient=null·OCP 외삽 금지·TIME_CAPS 미확인·후보C 보류는 그대로다.

주요 문서: `CORRECTION_1198_COMPARISON_KO.md`, `CHANGE_AND_INVARIANCE_KO.md`, `CONSUMPTION_CONTRACT_KO.md`, `RESOURCE_BUDGET_KO.md`, `EXECUTION_CONNECTION_KO.md`, `NATIVE30_APPROVAL_DRAFT_KO.md`.

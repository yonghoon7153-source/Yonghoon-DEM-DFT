# 다음 작업 — 두 연결부 정정 및 변경부 한정 검증

2026-09-28. **사용자가 채택·전달할 승인 초안이다. 검토자가 실제 실행을 승인한 문서가 아니다.** 수신 코드·시험 명령은 증거 자료이며 자동 실행하지 않는다.

## 사용자 채택용 문구

> G1198-N1/N2 두 연결부의 최소 정정·재봉인과 아래 변경부 한정 검증 1건만 승인합니다. 개괄 계획을 반복하지 말고 고정 코드·검증 결과를 제출하세요. COMSOL 전체 후보 컴파일/실행·실제 입력 gate·정책 변경·1198 solve·30초 연장은 승인하지 않습니다. Java 추출 helper용 stub 컴파일/JVM과 명시된 무해 종료코드 시험은 아래 범위에서만 허용합니다. 첫 실패 시 보존하고 중지하며 재시도하지 마세요.

## 1. 입력 및 보존

- 기준 ZIP: COMSOL63_GUARD1198_OFFLINE_PREPARATION_20260928.zip, 236,582 bytes, SHA `e8f544c01e3e8e8ba4ab27f294f1b8bb9124707ee0cfc38e2023a42f731279ec`.
- 기준 CODE_MANIFEST SHA: `0994d919ed1317a1234dbc2ba4276d5a7342401bbaed1ffcd2e45a69b8a13bcf`.
- 새 개정 폴더는 기존 작업 workspace 아래 `outputs/guard1198_limited_validation_R1_20260928/`로 제안한다. 이미 있으면 덮어쓰기·삭제·다른 이름 fallback 없이 중지한다. 원래 준비본/ZIP/정적 첫 오류와 정정 기록은 그대로 둔다.
- 후보 Java의 모델·물성·초기화·수치/좌표/단위·1198·guard·runAll 본문을 바꾸지 않는다. 원 Java 바이트를 유지하고, 새 개정본 식별에 필수적인 경로 변경이 필요할 때만 그 literal과 참조를 별도로 열거·역치환 대조한다. 다른 변경이 필요하면 범위 확대 전에 중지한다.
- 새 source/contract/parent/run/cwd/argv/manifest의 경로 결속을 하나로 맞추되, 실제 native runtime·승인·permission token·USER_DECISION·사용 가능한 VALIDATION_RELEASE는 만들지 않는다. 승인 시험용 객체는 fixture에만 둔다.

## 2. 허용 정정 두 건

### G1198-N1: 실패 반환 schema

trigger_consumer.analyze 초기 결과부터 `limited_result=INCOMPLETE`를 두고, 모든 조기 반환과 candidate_entry.analyze의 추출/소비 예외에서 공통 필수 결과 형식을 유지한다. trigger/sample/preservation/cleanup/policy와 overall/normal gate를 구분한다. 최초 실패는 errors에 남기고 기록 실패 등 후속 오류가 이를 덮지 않게 한다. 결손 결과에 성공 기본값을 채우지 않는다.

잘못된 binding·guard·native 중단사유·추출 실패를 실제 consumer→entry 경로로 검증한다. 원래 이유 보존, 결과 INCOMPLETE, 반환1, 추가 KeyError 없음이 요구사항이다. 수신 검토는 이 경로를 정적으로 발견한 것이므로 실제 실패 traceback을 이미 관측했다고 쓰지 않는다.

### G1198-N2: 부모의 증거 소비

GDecision의 수용 대기 판정에 최소 schema/상태 대조를 추가한다. trigger=TEST_TRIGGER_DETECTED, sampled_comparison/preservation/process_cleanup/policy_preservation=PASS 및 해당 판정에 필요한 pair/native_stop/numeric/coverage/tables_manifest 구조와 하위 상태를 대조한다. 누락·빈 구조·축별 미완과 수용 요약의 모순은 INCOMPLETE다.

부모에 CSV 수치 분석기 전체를 새로 만들지 않는다. 실제 producer 형식과 맞춘 필수 구조/상태 소비만 구현한다. typed native/analysis rc, 시간·run·manifest 결속과 전체/normal gate INCOMPLETE를 유지한다. 성공 시에도 AWAITING_LIMITED_EXTERNAL_ACCEPTANCE이지 native 전체 PASS나 다음 실행 승인이 아니다.

## 3. 고정 후 한정 검증

원 LIMITED_VALIDATION_PLAN의 **Python14 + Java6 + PowerShell6 = 26개 논리군**을 유지한다. 실제 하위 사례 수는 시험 전에 목록·기대 이유·도달 단계·양성 대조와 함께 봉인한다. 26개를 실제 assertion 수로 부르지 않는다.

| 엔진/범위 | 횟수·상한 | 반드시 포함할 연결 검사 |
|---|---|---|
| 고정 격리 Python, 실제 consumer/entry | 1세션·90초 | PY02/03/14에 N1 조기 실패와 schema, 실제 반환 경로. PY01 완전 양성. 기존 PY04–13 시간/좌표/수치/승인/정리 음성 유지 |
| 정확한 Java 변경 helper와 COMSOL stub | compile 1시도·90초, JVM 1세션·60초 | J01–06 동적 형상/시간·단위·guard·Interp·primary/report 복합 오류. 추출한 실제 method/catch 바이트 결속 |
| Windows PowerShell 5.1, 실제 BSave/BInvoke/GDecision | 1세션·60초 | PS03/05에 N2 완전 양성·요약만·각 축 누락/미완·필수 증거 누락/빈 구조·잘못된 식별. PS01 종료0/7/기동실패, PS04 원래 실패 보존, PS06 예산 유지 |

- Python/native/console/token/Job 진입점은 대상 import 전에 inert adapter로 차단한다. 받은 함수 대신 비슷하게 작성한 모사 함수의 통과로 대체하지 않는다.
- Java harness/JDK/compiler 경로·버전·SHA·추출 범위를 먼저 봉인한다. stub 시험은 실제 COMSOL API 타입 호환성이나 전체 모델 컴파일 시험이 아니다. Java 결과를 Python 모사로 대신하지 않는다.
- PS01에서만 명시된 무해 종료용 자식 프로세스를 허용하며 실제 COMSOL executable·Job 제어·콘솔 입력은 사용하지 않는다. PS5.1 호출이 거부되면 거부 기록으로 중지한다. PS7/다른 셸/정책 완화로 대체하지 않는다.
- 첫 실패면 원문·실패한 source seal을 보존하고 후속 시험을 중지한다. 성공할 때까지 수정/부분 재시험·별도 probe·새 suite를 실행하지 않는다. 실행 전 정정 두 건과 harness 작성은 허용하되 첫 시험 이후 수정·재시험 권한은 없다.
- 기존 38/64/67/389 전체 suite, 실제 F/입력/토큰·registry 조회/native Job 시험, COMSOL/JVM 모델 로드·solve는 제외한다. 위 stub JVM과 PS01 무해 자식 시험을 “프로세스/JVM 전체0회”로 잘못 보고하지 않는다.

## 4. 새 예산과 식별

원 제안의 총1,200초를 새 시행 원점에서 적용한다. 정정·harness·정적480, Python90, Java compile90, stub JVM60, PS60, 보존·포장300, 미완 정리120초다. 미사용분을 재시험에 전용하지 않는다. 고정 전 정정/준비가 상한에 맞지 않으면 미완을 보고하며 임의 연장하지 않는다.

시험 직전 source/contract/harness/engine manifest와 각 호출 argv/cwd를 봉인한다. 그 바이트를 검사하고 마지막 전달 manifest도 같은 바이트를 가리키는지 대조한다. manifest 자신을 자기 해시에 넣지 않는다. 큰 MPH·CSV를 새로 복제하거나 기존 결과 회수를 반복하지 않는다. 현재 경로/파일이 기대 식별과 다르면 중지한다.

## 5. 제출물과 중지점

1. 두 지적별 최소 diff·필수 schema·producer/consumer 연결표.
2. 새 source/code/harness/engine 식별과 Java 불변 또는 허용 literal 역치환 근거.
3. 26개 논리군 및 봉인한 하위 사례별 실제 결과·이유·단계·첫 실패/미실행 목록.
4. 각 엔진 실제 외부 rc와 시간, phase/전체 원점·완료 기록, 선택 원본 전후 식별.
5. 정확한 ZIP 집합·크기/SHA/CRC·경로 검사, ZIP 밖 생성 영수증 및 마지막 반환의 출처 구분.
6. 기존 준비본의 전달 최종 영수증/반환이 남아 있으면 원문 사본만 보충. 과거 포장·시험을 재실행하지 않는다.
7. 검증 수용을 기다리는 비활성 native1198 승인 초안. approved=false/usable=false 유지. native 호출/현재 정책 허용 경로가 미확인인 부분을 명시한다.

결과를 전달한 뒤 멈춘다. 실패면 해당 최소 원인을 다음 승인 대상으로 제시한다. 통과해도 자동으로1198을 시작하지 않는다.

## 6. 이후 경로

**이번 정정·한정 검증 수용 → 별도1198 native 최대5초·1회 승인 → 발동/수치/보존/정리/정책 증거 수용 → 별도 fresh t=0→30초 진단 승인** 순서다. 1198은 시험용 임계값이며30초 운전의 생산 임계값으로 이어 쓰지 않는다. 30초는 장시간/12시간 운전 승인이 아니며 결과를 보고 다음 시간 구간을 결정한다.

B020 저장 자료·전압 분해는 완료 결과로 재사용한다. 전체 수렴/정상 gate INCOMPLETE, 실효 정책/실제 코어 UNVERIFIED, OCP 외삽 금지, TIME_CAPS 차이 원인 미확인, 기존 failed/pending/원복 기록은 유지한다.

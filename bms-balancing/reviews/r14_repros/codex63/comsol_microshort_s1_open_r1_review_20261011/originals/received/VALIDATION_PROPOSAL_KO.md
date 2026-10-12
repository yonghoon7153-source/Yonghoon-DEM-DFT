# OPEN-R1 추가부 한정 검증안 — 제안만, 미실행

현재 사용자 승인은 N1–N3의 오프라인 정정과 정적 재봉인에 한정된다. 이 문서는 시험 승인이나 실행 결과가 아니다. `approved=false`, `usable=false`, `native_ready=false`, `plan_ready_for_execution=false`를 유지한다. 후보 import·호출, 하네스 작성, 엔진 버전 호출, Java 컴파일, JVM/COMSOL, 콘솔 입력, Job/프로세스 시험은 수행하지 않았다.

기존 C01–C08의 **50개 ID를 모두 유지**하고 N1/N2용 C09 **43개**를 추가했다. 총 **9군 93개: Python 87개, Java helper 6개**다. 정확한 사례별 입력 변경·기대 반환/예외 위치·필수/금지 도달·양성·호출 횟수는 `LIMITED_VALIDATION_PLAN.json`에 기록했다. 기존 R1 130사례를 재실행하는 안은 아니다.

## N1: 독립 시작 기준과 실제 세션 경로

독립 `start_record`에서 `ResourceSession(start_record, anchors)`를 한 번 구성한 후 같은 세션의 `decide`를 호출하도록 한다. 실제 경로는 `ResourceSession.decide → resource_decision → project_owned_sample → bind_sample_clock → 원 control.assess_resources`다. 세션은 frozen clock context와 scalar anchor snapshot을 유지한다. raw는 run_id, clock_id, clock_origin, 초 단위 및 두 원점과 정확히 일치해야 한다. 경과시간 계산은 context의 고정 원점을 사용한다.

계획의 공통 기준은 전체 원점100, native 원점200, start210/end211, previous206이다. 같은 Job의 다음 샘플 end216에서도 세션을 새로 만들지 않고 native/전체 경과16/116초를 기대한다. 이 값은 inert 제안 자료이며 실제 OS 관측을 뜻하지 않는다.

C09는 raw 원점만 이동한 경우, raw/start 원점 부재, 잘못되거나 없는 run/clock/단위, 시작 원점 순서 오류, anchor run 불일치와 mutable anchor 값, caller 원본 dict 변경 후 snapshot 유지, frozen field 대입 거부를 분리한다. frozen 대입은 `dataclasses.FrozenInstanceError`이고 resource 반환으로 오인하지 않는다.

실제 고정 예산 초과 사례는 계약의 기존 수치와 reserve를 유지한다. end7281에서 native 경과7081초는 7200−120을 초과하여 `STOP_RESERVE_ENTERED:native_elapsed_s`만 반환한다. end8981에서는 native/전체 경과8781/8881초이므로 이유 배열은 native 다음 overall 순서다. 이 두 사례는 실제 `assess_resources` 호출1을 요구한다. 샘플 간격5초와 측정기간1초는 별도 간격 오류를 만들지 않게 고정한다.

C06-08은 raw 원점100/200을 context와 일치시킨 채 start211/end210만 뒤집어 기존 `CLOCK_ORDER`에 도달하게 한다.

## N2: process counter 구조 오류

counter 항목의 null·scalar·list, 필수 키 각각의 부재, PID/creation의 bool·float·container·문자열·0, query 실패와 잘못된 working-set 값 등을 개별 ID로 둔다. 기대 이유는 `PROCESS_COUNTER_SCHEMA`, `PROCESS_COUNTER_KEYS`, `PROCESS_COUNTER_IDENTITY_TYPE`, `RSS_IDENTITY_OR_QUERY`로 구분한다.

이 음성들은 실제 세션 경로에서 `ResourceConnectionError`가 발생하고 `resource_decision`이 다음 형식으로 반환해야 한다. `control.assess_resources` 호출은0이다.

```json
{"status":"STOP_REQUIRED","reasons":["각 사례에 봉인된 정확한 이유"],"sampled_max_is_os_peak":false,"counter_projection":"INCOMPLETE"}
```

AttributeError/TypeError 등 의도하지 않은 예외나 앞단의 다른 거부는 해당 음성의 성공이 아니다. 생성자 단계의 실패는 세션이 없으므로 예외 위치와 decide 호출0을 별도로 기록한다.

## N3: 양성 및 도달 경로 정정

| 사례 | 대응 양성 및 판정 |
|---|---|
| C04-03/04/05 | C04-02의 non-null proof. 각각 METHOD_OPEN, GRID_OR_SCOPE, PAYLOAD_BINDING의 정확한 ConnectionError.reason/stage/message. C04-01은 proof=None 조기 반환만 담당한다. |
| C07-03 | 세션→resource_decision→project_owned_sample에서 OS_QUERY_FAILURE→resource_decision의 STOP_REQUIRED 반환. bind_sample_clock 및 assess_resources 호출0. |
| C07-05 | C07-04 기준. transition.error=STOP_METHOD_NOT_APPROVED, action=NONE, transition.status=UNRESOLVED. |
| C07-06 | C07-04 기준. transition.error=STOP_OWNERSHIP_LOST, action=NO_KILL_WITHOUT_OWNERSHIP, transition.status=UNRESOLVED. |
| C08-01/02 | property 양성은 C08-01. unknown type은 원 readSetting의 IllegalArgumentException을 전달한다. |
| C08-03/06 | configured/equation 양성은 C08-03. 첫 cdi getter의 sentinel 예외는 동일 객체로 전달되고 이후 time/physics/equation 호출은0. |
| C08-04/05 | stored-grid 양성은 C08-04. C08-05는 원 evaluate→원 checkShape의 TIME_ORIGIN:s1openstoredgrid에 도달한다. |

C07-04의 FORCED는 `stop_classification` 값이다. transition.status는 `FORCE_PENDING`, action은 `FORCE_OWNED_JOB_ONCE`이며 execute_now=false다. 이는 실제 종료 관측이 아니다.

Java stored-grid 양성은 getReal의 {{0.0,1.0,120.0}}, 음성은 첫 값만 바꾼 {{0.5,1.0,120.0}}이다. 원 T_END_SECONDS=120.0을 유지하고 사례마다 TIMES=null로 초기화한다. evaluate나 checkShape를 대체하지 않는다. configured numerical binding/unit 확인이 먼저 성공해야 한다. 음성은 원 checkShape의 IllegalStateException을 전달하고 evaluated unit 및 stored-grid 출력은 도달하지 않는다.

## 정확 소스와 별도 실행 전 봉인

`FUNCTION_SPANS.json`은 새 함수·기존 의존부·예외 발생 지점의 원문 span과 SHA를 제공한다. inclusive 1-based line, CRLF/CR→LF, 들여쓰기 보존, UTF-8 no BOM, 마지막 LF 없음 규약을 사용한다. 원문 byte offset/SHA와 LF 정규화 span SHA를 구분한다. `LIMITED_VALIDATION_PLAN.json`의 source/contract/dependency pin은 현재 파일을 읽어 결속한 값이다.

Java는 정확 새 helper와 필요한 기존 readSetting/evaluate/checkShape/units/evaluatedUnits/quote/table, T_END_SECONDS/TIMES만 사용한다. COMSOL 객체 표면만 최소 inert stub으로 제공하고 원 table 출력을 포착한다. helper 검증은 설치 COMSOL API 호환성이나 post-consistency t0 증명이 아니다.

엔진 SHA 및 과거 COMMANDS 선택 기록은 **이전 관측의 재사용**이다. 이번 엔진 실행/버전 조회 또는 현재 재측정으로 표시하지 않는다. 미래 승인 전에 실제 사용 바이트·정확 하네스·입력·기대값·추출 span을 봉인해야 한다. 현재 proposed 경로는 문자열 제안일 뿐이며 fixture, 하네스, 승인 파일, 실행 폴더를 만들지 않았다.

## 미래 실행 예산과 중단

미래 제한 검증 제안은 기존 총 **1350초**를 유지한다: 하네스 봉인600, Python180, Java compile90, Java helper60, 보존·전달300, 미완 정리120초. 새 순수 사례는 같은 Python 세션 안에 포함하며 세션 수나 timeout을 늘리지 않는다. 현재 오프라인 정정 승인 시간과 이 미래 제안을 합산하거나 전용하지 않는다.

별도 승인 후에도 첫 예상 밖 오류 또는 시간 한도에서 중지하고 stderr/rc 및 미실행 ID를 보존한다. 수정·재시도·probe·fallback으로 계속하지 않는다. 모든 사례의 실제 결과는 현재 NOT_EXECUTED다. 네 OPEN, 기존 수용·실패 기록 및 native 준비 미완료 상태를 유지한다.

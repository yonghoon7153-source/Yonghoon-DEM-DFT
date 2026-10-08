# R1 검증안·추출 봉인 독립 정적 검토

검토 대상은 `received/main/VALIDATION_PLAN_R1.json` 전체의 구조·130개 사례·98개 대응·43개 추출 범위, `_KO.md`, `reference/ORIGINAL_VALIDATION_PLAN.json`, `reference/R1_DIRECTIVE_v2_KO.md`, `CHANGED_FILES.json`, N4 최소 변경이다. 후보·받은 도구의 import/함수 호출/기능 시험/Java/JVM/COMSOL 실행은 하지 않았다. 검토자 작성 PowerShell의 JSON 읽기·집계·원문 바이트 해시·정적 슬라이스와 독립 스칼라 정수 산술만 사용했다. 받은 파일은 수정하지 않았다.

판정: 수량·범위·주요 N1–N3 신규 사례 설계는 대체로 맞지만, 현 검증안을 그대로 봉인하여 시험할 수는 없다. 아래 1–2는 소스와 명시적으로 충돌하는 검증안 오류이고, 3은 지정된 대조 연결의 불일치다. 미래 하네스/fixture가 아직 없는 사실은 승인 전 계획의 의도된 OPEN이며 별도 결함으로 세지 않았다.

## 확인된 문제

### PLAN-01 · P2 · S1Sha 추출 봉인이 실제 함수 대신 빈 바이트를 가리킴

- 위치: `VALIDATION_PLAN_R1.json:5232`–`5236`; 원문 `candidate/Parent.ps1.inactive.txt:23`.
- 선언은 `start_line=23`, `end_line=22`, SHA `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`이다. 이는 빈 바이트 SHA다. 실제 23행에는 한 줄짜리 `function S1Sha(...) { ... }`가 있다.
- 43개 추출 중 나머지 42개는 선언한 LF 정규화·끝 LF 제외 규칙과 해시가 맞았다. 이 하나는 범위 자체가 역전되어 있다.
- 현재 `PLAN_STATIC_AUDIT.json`은 이 항목도 PASS로 선언한다. 받은 `tools/r1_plan_seal.py:33`–`36`의 텍스트를 보면 범위 타당성 없이 같은 `[start-1:end]` 슬라이스의 해시만 비교한다. 따라서 빈 추출과 빈 SHA가 서로 맞는 것을 실제 함수 봉인으로 오인했다.
- 이 목록을 그대로 사용하는 향후 하네스에는 S1Sha가 없으며 `S1Decision:297`, `S1NativeAxis:187`, `S1Fields:238`, `S1FinalReturn:362` 등의 정상 경로가 성립하지 않는다. 현재 원문 전체 SHA의 일치는 함수 추출 봉인의 오류를 보완하지 않는다.
- 정정 기준: 23–23행, LF 정규화·끝 LF 제외 90 bytes, SHA `13c6456b30805e3b02063ca8cb804b201d948c5518bf01b102610297236d8eed`. 추출 감사에는 시작≤끝, 비어 있지 않음, 선언한 함수 이름과 실제 함수 범위 일치가 필요하다. 생산 함수 수정은 필요하지 않다.

### PLAN-02 · P2 · PARENT12가 S1FinalReturn에 없는 status를 관찰함

- 위치: `VALIDATION_PLAN_R1.json:2888`–`2915`, 특히 `2914`.
- PARENT12의 목표는 `S1FinalReturn`의 정확 한계 양성이고 기대값은 `AWAITING_S1_LIMITED_EXTERNAL_REVIEW`인데, 관찰 경로가 `return_value.status`다.
- 실제 함수의 반환은 `candidate/Parent.ps1.inactive.txt:370`–`373`에서 `limited=$limited`이며 `status` 키를 반환하지 않는다. 따라서 정상 입력에서도 명시된 경로로 기대값을 얻을 수 없다. `prior_decision.status`는 최종 기록 후 판정의 대체 증거가 될 수 없다.
- 같은 함수의 PARENT09/10/11/16은 이미 `return_value.limited`를 사용한다. PARENT12도 그 경로와 final-boundary 관찰 모드로 일치시켜야 한다. 현재 실패 시 중지 규칙대로라면 미정정 상태는 PowerShell 세션을 이 양성에서 중단시킨다.

### PLAN-03 · P2 · 일부 공유 양성 대조 ID가 목표 함수를 실행하지 않음

- 위치 예: `VALIDATION_PLAN_R1.json:1083`(INIT07→INIT01), `2906`(PARENT12→PARENT01), 공통 요건 `4950`.
- 공통 요건은 공유 대조를 동일 source/function/fixture seal에만 재사용하고, 누락된 대조는 preseal에서 멈추도록 한다. 그러나 INIT07/08/10의 대조 INIT01은 `compare_initialization`만 호출한다. 계수 함수의 실제 양성은 INIT09로 이미 별도 존재한다.
- PARENT09/10/11/16의 대조 PARENT01은 `S1Decision`까지만 호출하며 `S1FinalReturn`을 부르지 않는다. 최종 경계의 양성은 PARENT12로 연결해야 한다(PLAN-02도 함께 정정).
- 위 두 연결이 확정 핵심 예시다. 별도 명확화 대상으로, RESOURCE09–15의 선언된 대조 RESOURCE01은 `assess_resources`이고 목표 `advance_stop`을 호출하지 않는다. 이 전이 사례 중 상당수는 자체 예상 전이 양성일 수 있으므로 모든 전이 양성이 없다고 판정하지 않는다. 실제 상태/분기에 맞는 matching reference를 지정할 필요가 있다. READ08–12의 대조 READ01도 명시된 target/reach상 `read_csv_bytes`뿐인데, prose에는 “then exact profile”이 있다. 이것이 복합 양성을 뜻했다면 실제 대상/도달 명세에도 `timed_rows`/`coverage`/`profile_rows` 중 필요한 경로가 명시되어야 한다.
- 이는 하네스 미작성 자체의 문제가 아니라 현재 고정한 ID 연결이 스스로의 대조 규칙을 충족하지 못하는 문제다. 기존 양성 ID 재연결 또는 기존 양성 ID의 명시적 도달 범위 보강으로 해결 가능하다. 추가 입력이 필요하면 130 집계도 명시적으로 갱신해야 하며 숨은 추가 호출을 대조로 세면 안 된다. 생산 코드 변경 없이 preseal 계획 정정 조건으로 다룰 수 있다.

## 일치하는 항목

| 군 | 사례 수 |
|---|---:|
| AUTH | 15 |
| READ | 12 |
| INIT | 12 |
| POLICY | 8 |
| CHARGE | 29 |
| PAIRED | 7 |
| RESOURCE | 16 |
| PARENT | 31 |

- 130개 고유 ID, 130개 고유 input ID, input_count 합계 130, Python 99 + Windows PowerShell5.1 31이 일치한다. P0 정적 확인 1개는 기능 130개에 합산하지 않았다.
- 기존 98 ID가 정확히 한 번씩 동명 ID로 대응하며 누락·중복이 없다. 신규 32는 CHARGE_R101–R117 17개 + PARENT_R101–R115 15개다. 기존 31 updated/67 retained 구분은 CHARGE 12 + PARENT 16 + POLICY02/03 + PAIRED04와 맞는다. READ10의 문구 구체화는 원 논리 목적이 유지된다.
- 720 + 420 + 300 + 300 + 120 = 1860초. 원래 1500초 대비 +360초를 별도 승인 제안으로 표시하며 현재 정정 2700초에서 전용하지 않는다. Python/PowerShell 각 1세션, Java compile/JVM/COMSOL 0회다.
- 정상 실제 생산자 CHARGE01→봉인 JSON→PARENT01, 보호 생산자 CHARGE_R109→PARENT03, 정확 초과 POLICY03→PARENT02/PARENT_R114, 정확 경계 POLICY02→PARENT_R115/PARENT_R113 연결이 명시되어 있다.
- PARENT03은 설정 끝120, 실제 끝90.1, safe end90을 구별하고, 실제 고정 `sparse_0_120.tokens_s` 255개 중 ≤90인 249개를 독립 집계한 결과와 맞는다. 제외되는 요청은 95/100/105/110/115/120이다. 최종 PROTECTIVE_STOP 분기까지 도달해야 하므로 선행 schema 오류를 보호 양성 성공으로 셀 수 없다.
- PAIRED04는 base 0/0/0, finite 0/−0.0005/−0.001 at 0/2700/3600으로 D=0.001, S=0.002를 주고, 동일 K곡선으로 E_D=E_S=0이다. 실제 `paired_classification:349`–`352`의 두 strict-above 및 both-small 조건 모두 충족하지 않아 INCONCLUSIVE 설계가 맞다.
- Decimal 경계 설계는 정확 0.001과 0.0010000000000000000001을 구별한다. PARENT_R113은 변환 뒤 double이라는 fixture 전제조건을 별도로 확인하고, R114는 두 summary 문자열만 WITHIN으로 바꿔 `COMPARISON_SUMMARY_CONTRADICTION`을 기대한다. actual Python→raw JSON SHA→PowerShell 경로가 정적 문서에 연결되어 있다. 기능 성공을 뜻하지는 않는다.
- CHARGE_R112/113의 고정 r와 F에 대해 독립 정수 곱의 50자리 반올림은 각각 0.0002와 0.000199에 해당한다. 직접 charge_balance의 합성 비음수 inventory 경계이며 모델 초기화 양성으로 확대하지 않는 제한이 명시되어 있다.
- N1의 시작/끝/중간 누락·동일 길이 시간 변이·Li 출처·unit 결속, N2의 양의 누적 q 속 N/P 역행과 deadband 경계/내부, N3의 동일 수량 중복/다른 시각/비유한/정렬/범위/부분집합 변이에 구체적인 목표 사유와 도달 경로가 있다. PARENT_R107은 더 이른 duplicate/order/native-subset 실패가 나지 않도록 native-only 대체 시각 전제를 갖췄다.
- 소스 바인딩 3개의 실제 raw byte 수와 SHA는 모두 일치한다. CHANGED_FILES의 기존 변경 7개도 실제 byte 수·SHA와 일치하며 원 CODE_MANIFEST 대비 해당 기존 파일 변경 목록과 맞는다. 검증안 파일 교체(`VALIDATION_PLAN.json`→`VALIDATION_PLAN_R1.json`)는 새 CODE_MANIFEST의 current/historical 경로로 따로 표시된다.
- N4 P0는 `accepted tsteps storage` 1개를 `requested tlist storage`로 메모리에서 되돌린 SHA가 원본 `20c1acc9aa8287ed71363ea12dbea3d54a6a211a4752493560e21f85bc6f6d95`와 정확히 일치한다. `tout=tsteps`를 유지한 439행 문구만의 정정이라는 주장을 지지한다.

## 향후 승인문/봉인에서 명확히 할 항목

- `preseal_before_first_test.required:4964`에 실제 Python 출력 JSON의 저장·SHA가 들어 있지만 그 출력은 Python 시험 후에 생긴다. 소스/하네스/원입력/기대값의 최초 엔진 전 봉인과 실제 생산자 JSON의 Python 후·PowerShell 전 봉인을 구별하면 된다. 새 생산 코드 차단으로 취급하지 않는다.
- PARENT14는 실제 analyze의 charge INCONCLUSIVE 생산자 JSON을 요구하지만 producer_case_id가 지정되지 않았다. 현재 CHARGE02/03/04는 직접 charge_balance 반환 사례다. 봉인 시 임의 수제 analyze 요약이나 미집계 생산자 호출로 메우지 않도록 실제 등록 생산자/sole-field mutation 경로를 확정해야 한다.
- 기존 사례의 슬래시·대안 표현은 한 구체 입력과 정확 첫 사유/단계로 봉인해야 한다는 요건이 남아 있다. RESOURCE 계열은 상태 외에 실제 reasons/error 필드도 목표 분기를 식별하도록 확정하는 것이 적절하다. 지금 하네스를 만들거나 시험할 이유가 되지 않는다.
- 설치본 t0/계수 소비, native/raw adapter, 자원 감시/중지는 OPEN 유지이며 `native_ready=false`, 전체/정상 gate INCOMPLETE, 기능 NOT_RUN이다. 이를 미구현 결함으로 새로 집계하지 않는다.

검토 결론은 검증안 정정·봉인 요건에 한정되며 실제 후보가 해당 130개 기능 시험을 통과했다는 의미가 아니다.

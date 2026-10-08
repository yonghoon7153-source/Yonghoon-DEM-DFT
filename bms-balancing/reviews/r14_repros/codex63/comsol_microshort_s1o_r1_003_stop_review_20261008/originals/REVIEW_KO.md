# S1O R1 003 중지 결과 검토

2026-10-08. **첫 실패에 따른 중지와 INCOMPLETE 판정은 타당하다. 생산 코드 결함은 확인되지 않았다. 기존127개 PASS 기록은 보존·재사용할 수 있지만, 미완3개와 READ군의 같은 기본 입력 양성 대조를 보완하기 전에는 한정 검증 종결로 올리지 않는다.**

이번 회신은 읽기 전용 독립 검토다. 받은 하네스·후보·시험을 import·호출하지 않았고 COMSOL/JVM/컴파일/재시험은0회다. 검토자가 작성한 ZIP·JSON·텍스트·해시 검사만 수행했다. 원본 기록은 수정하지 않았다.

## 1. 수신 결과와 판정 범위

| 항목 | 확인 |
|---|---|
| ZIP | 876,456 B · SHA `11a27f3034fed763442ccce9730f7e008058b819bfbffd9d58a5d2994b875d4b` |
| PACKAGE_MANIFEST | 25,683 B · SHA `9a7b73e50223c152c87af3250e1ee955263837ae873dabcaffcee0d82653a5c4` |
| 파일 집합 | 153 payload+manifest,154 entries · 크기/SHA/CRC/정확 집합/중복·경로 검사 일치 |
| 생산 CODE_MANIFEST | 이전 수용본 `4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da`와 동일,21개 모두 일치 |
| Python | 99 PASS · raw stdout의99기록과 PYTHON_RESULTS 일치 · 외부rc0 |
| PowerShell | 28 PASS · raw stdout의28기록과 실패 파일의 cases 일치 · 외부rc1 |
| 첫 실패 | PARENT_R113 · HARNESS_FAILURE_BEFORE_TARGET |
| 후속 미실행 | PARENT_R114, PARENT_R115 |
| 종합 | 127 PASS / 1 하네스 준비 실패 / 2 미실행, INCOMPLETE 유지 |

127은 실제 기록에 있는 통과 수다. 뒤의 대조 미충족을 이유로 그 원문을 FAIL로 바꾸지는 않는다. 반대로 통과 개수만으로 모든 사전 검증 계약이 닫혔다고도 하지 않는다. `INPUT_CHECK.json`과 `RECORD_AUDIT.json`에 별도 관측을 남겼다.

## 2. PARENT R113에서 확인한 원인

좌표는 ZIP을 펼친 `received/` 원문 기준이다.

`harness/ps_harness.ps1:127–133`은 실제 POLICY02 JSON의 문자열 `"0.001"`에서 따옴표만 제거하고, ConvertFrom-Json으로 읽은 값이 반드시 CLR Double인지 검사한다. 첫 오류는 **`HARNESS_FIXTURE_OR_ASSERTION:R113_DOUBLE_AFTER_JSON_PARSE`**, stack은 HRequire35행→133행이다. 생산 `S1Decision` 호출은158행이므로 이 사례에서는 생산 함수에 진입하지 않았다.

확정할 수 있는 것은 **그 Double 전제가 거짓이었다**는 사실이다. 실제 CLR 타입은 기록되지 않았다. `parsed_clr_type`·변이 bytes/SHA를 기록하는135행이 실패 검사 뒤에 있기 때문이다. Decimal이었을 것이라는 추측을 당시 관측으로 쓰지 않는다. 수신 POLICY02 출발 파일은122,640 B/SHA `254164ec95da7af50e734baff70f6c804c28eb7854898912261699e8cb8c0880`이며 원 value는 문자열0.001로 맞다.

생산 Parent `S1ExactDecimal:27–35`는 문자열·명시된 정수 타입만 수용하고 Double/Decimal 등은 `DECIMAL_TRANSPORT_PRECISION`으로 거부하도록 작성돼 있다. 이번 하네스는 그 방어에 도달하지 못했다. 따라서 이 실패는 그 방어의 PASS도, 생산 코드의 FAIL도 아니다.

### S1O 003 N1 P2 시험 입력의 Double 전제와 실패 진단 순서

- 위치: `harness/ps_harness.ps1:126–135`, catch194–198; `PS_INPUT_RECIPES.json`의 R113.
- 문제: JSON 숫자 token과 구체 CLR Double 타입을 같게 취급했다. 전제 실패 시 실제 타입·변이 식별을 저장하기 전 중지한다.
- 최소 조치: 원 Double 거부 목적을 유지하되 **fixture 전용 명시적 Double 변환**을 새 계획에서 채택한다. 먼저 원 producer/context, 숫자 JSON 변이 bytes/SHA·token 위치, parse 직후 실제 타입·값을 기록한다. 유효한 해당 숫자임을 확인한 다음 단일 leaf만 Double로 변환하고 전후 타입/값/비트를 기록한다. parser 자체가 Double을 만들었다고 쓰지 않는다.
- null·문자열·비숫자·비유한·다른 값이 들어온 경우 cast로 감추지 않고 fixture 실패로 멈춘다. `[double]` 전제를 삭제하거나 double/decimal 어느 것이나 과거 시험을 통과했다고 처리하는 방식은 권고하지 않는다.
- 사례 시작에서 current ID·빈 reach·target_entered=false를 초기화한다. 목표 함수에 실제로 도달한 뒤에만 도달을 기록하고, R113의 정확 이유와 `stage=comparison_numerics`, R114의 이유와 `stage=fields`까지 대조한다. 새 진단·fixture 변경은 별도 승인 대상이며 이번에 구현하지 않았다.

## 3. 이전 검토 정정과 이번에 남은 대조 문제

R1-V1의 S1Sha23–23/90B 추출은 정정돼 있다. 43개 추출 범위·해시가 맞고 PS 관측15개와도 일치한다. R1-V2의 PARENT12는 실제 `limited`와 POST_WRITE 경계100, 오류0을 관측했다. R1-V3의 계수 INIT09 및 FinalReturn PARENT12 함수 연결도 정정됐고, CHARGE03의 실제 analyze 결과가 PARENT14에 전달됐다.

그러나 **R1-V3의 같은 기본 입력 조건이 READ군에서는 아직 충족되지 않는다.** 이것은 생산 소스 오류가 아니라 대조 증거의 잔여다.

### S1O 003 N2 P2 READ의 동일 기본 입력 양성 대조 누락

위치: `harness/python_harness.py:85–113`, READ01/READ02 recipe, 수정계획 및 CONTROL_MAP의 READ02–12→READ01 연결.

READ01은255시각×241좌표의 N/P5열 프로파일 CSV를 읽는 큰 양성이다. READ02–07은 `time_s,value` 두 열의 작은 CSV를 사용하며, 그 작은 입력에서 변이만 제거한 성공 호출은 기록돼 있지 않다. READ08의 무변이 기본 입력은 value필드 없는0/1초 행이며 실제 음성은0/0으로 중복시킨다. READ09/10은0/1초 목록을 축소하고, READ11/12는t0의 N241점에서 변이한다. 같은 함수를 통과한 READ01이 있다는 사실과, **같은 기본 입력에서 선언한 변이만 달라지는 대조가 있다**는 것은 다르다.

READ02–12의 실제 거부 이유·단계·도달 기록 자체는 맞는다. 이11개를 실패로 재분류하거나 다시 실행할 필요는 없다. 다만 선언한 동일fixture 양성 근거를 보완해야 검증 종결에 쓸 수 있다.

추가 양성4개면 다음 기본 입력들을 직접 확인할 수 있다. 기존 음성 입력의 생성 규칙·봉인 SHA와 변이 전후 차이는 별도로 정적 결속한다.

| 제안 양성 ID | 같은 기본 입력 | 연결할 기존 음성 |
|---|---|---|
| READ_CTRL_CSV | 원 `time_s,value\n0,1\n1,2\n`, 정확 header·크기/SHA·단위 | READ02–07 |
| READ_CTRL_TIME | time_s만 있는 Decimal0/1 두 행, end=`1` | READ08 |
| READ_CTRL_COVERAGE | 양쪽시간 Decimal[0,1], 세 요청목록 문자열[0,1], safe=`1` | READ09·READ10 |
| READ_CTRL_PROFILE | 원 생성 규칙의t0 N241점, 같은 좌표·domain1·정밀도 | READ11·READ12 |

READ05–07은 raw 전체 변경과 그에 따른 identity 재계산, READ10은 다섯 시간/요청 벡터에서1을 제거하는 복수변이를 정확히 열거한다. 이를 한 leaf 변경이라고 숨기지 않는다. 같은 helper를 호출했다는 이유만으로 동일 입력을 추정하지 말고 생성 규칙·canonical bytes·SHA를 비교한다. 소스·실패 입력을 바꾸어 새 양성에 맞추지 않는다.

## 4. 기존 결과 재사용과 최소 후속 범위

현재127개 PASS 원문은 소스·입력·하네스·엔진 식별을 연결해 보존한다. READ02–12의 11개는 위 대조 충족 전까지 종결 근거가 조건부이며, 나머지 통과를 이번 하네스 준비 실패가 자동 무효화하지 않는다. 원 R1_003은 이후에도 INCOMPLETE로 남긴다.

후속은 새 승인하에 **Python 양성4개 + PowerShell 미완3개 = 새 입력7개**로 한정할 수 있다. 기존99개/28개 전체를 다시 돌릴 필요는 없다.

PS 순서는 정상 문자열 대조 PARENT_R115 → 개정 typed fixture PARENT_R113 → summary 위조 PARENT_R114가 적절하다. R114의 초과 양성은 기존 PARENT02를 다음 조건으로 재사용한다.

- 같은 Parent 원바이트·함수 추출, 같은 엔진 pin, POLICY03 원 JSON/context를 사용한다.
- 실제 이전 PARENT02의 EXCEEDS_LIMITS·VALID·정확 도달 기록을 새 대조 재사용 표에 연결한다.
- 새 하네스 공통 source loading·producer 읽기·결과 의미를 바꾸지 않는다. 변경은 subset선택·R113변환·진단·stage assertion에 한정한다.

이 조건을 지킬 수 없다면 PARENT02의 추가 재관측 등 더 넓은 범위를 **시험 전 새 승인**받는다. 숨은 네 번째 PS 호출이나 별도 probe로 메우지 않는다.

성공하더라도 보고는 “기존127 재사용 + 남은3 새 결과로 원130 ID 충족, 추가 대조4 별도”다. 단일 세션130 PASS나134개 전부 신규 PASS라고 쓰지 않는다. 준비·시험·전달은 새 원점을 쓰며 이전1860초의 남은 시간을 이어 쓰지 않는다. 비활성 제안은 `NEXT_LIMITED_APPROVAL_DRAFT_KO.md`에 있다.

## 5. 봉인과 시간 및 승인 기록의 해석

FIRST_SEAL123개와 SELECTED_SOURCES_AFTER123개는 정확히 대응한다. 원source22개(CODE_MANIFEST+21), fixture99개, 외부엔진2개다. 이 가운데 동봉121개의 바이트는 검토자가 다시 해시해 확인했다. 외부 실행 PC의 엔진2개는 제출된 전후 식별 기록의 일치이며 현 호스트에서 새로 관측한 것은 아니다.

Python에서 생성한 producer/context10개, Python 결과·session, PS하네스가 두 번째 봉인에 맞는다. Python 시작 전 첫 seal, Python 뒤·PS 전 producer seal이라는 순서도 기록과 맞다. 테스트 입력 안의 `compile=1` 등은 inert fixture 호출 계수이며 실제 COMSOL 호출이 아니다.

| 관측 | 초 | 한도와 해석 |
|---|---:|---|
| 사전 봉인 |390.0584138|720 이내 |
| Python session record |169.2547576|420 이내, rc0 |
| Python 후속 반환 경계 |169.2741394|위 기록 쓰기 뒤; 별개로 합산하지 않음 |
| PS session record |30.2902513|300 이내, rc1·timed_out=false |
| PS 후속 반환 경계 |30.3085736|within_limits=false는 성공/시간 복합 필드에서rc1 반영 |
| 전달 원점 |누적696.4308394|새 전달 단계 시작 |
| ZIP 내부 closeout |누적861.3451922|포장/receipt 쓰기 전 |
| 사용자 제공 포장 최종 snapshot |누적862.1651496 / 전달165.7343128|1860/300 이내, receipt 재읽기 뒤·도구 반환 전 |

사용자 본문에 제공한 `0a81fc / rc0 / wall7.1100966`은 포장 반환 후속 전사다. 이를 PS 시험rc0이나 native PASS로 읽지 않는다. 포장wall time을 위 누적snapshot에 더하지 않는다. 실제 ZIP 식별은 독립 확인했지만 ZIP 밖1165B 영수증 원파일의 SHA는 사용자 제공 기록으로 구분한다. 이번 검토의 `USER_SUPPLIED_DELIVERY_RECORDS.json`은 의미 전사이지 그 원파일 복제본이 아니다.

원 발송 승인문은R1_001을 지정하고, ORIGIN/RESULT는R1_003에 별도 사용자 승인이 있었다고 기록한다. 이 묶음에는 해당 사용자 응답 원문이 없으므로 **003 승인 근거는 제출자 기록**으로 분류한다. 이를001의 자동승인이나 무단실행으로 단정하지 않는다. 기록의 출처 한계이며 현재 측정으로 보충할 사항은 아니다. 재개에는 새 위치·새 범위의 명시 승인이 필요하다.

검토자 데이터 검사에서 PS stdout을 UTF8로 읽으려다 인코딩 오류1건이 발생했다. 원바이트를 유지한 채 해당 파일을 strict CP949로 읽어JSON 기록을 대조했으며 첫 검사본/오류를 `notes/REVIEWER_DATA_READ_CORRECTION.json` 등에 보존했다. 이는 수신 시험이나 후보를 재실행한 것이 아니다.

## 6. 최종 회신

현재 판정은 **STOP_RESULT_ACCEPTED / LIMITED_VALIDATION_INCOMPLETE**다. 첫 실패 후 중지한 처리는 수용하며 생산 소스 수정은 요구하지 않는다. 별도 승인 후 하네스의 typed fixture·실패 진단을 정정하고 양성4개/미완3개만 확인하는 것이 다음 최소 단계다.

native_ready=false, 설치본 초기화t0·계수 실관측·native/raw·OS 어댑터 OPEN, 전체/정상 gate INCOMPLETE는 유지한다. 이번 또는 다음 합성 검증이 microshort 물리 효과나 실제 계산 가능성을 입증하지는 않는다. 외부 발송은 하지 않았다.

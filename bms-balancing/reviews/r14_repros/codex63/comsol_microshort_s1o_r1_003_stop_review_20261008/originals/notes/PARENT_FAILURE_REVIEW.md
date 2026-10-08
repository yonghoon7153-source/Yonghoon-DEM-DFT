# R1_003 PARENT_R113 중지 원인 및 최소 후속 범위

2026-10-08. 검토 범위는 수신 `harness/ps_harness.ps1`, `PS_INPUT_RECIPES.json`, `PS_FIXTURE_MAPPING.md`, `VALIDATION_PLAN_CORRECTED.json`, `results/ps_first_failure.json`, PowerShell stdout/session/attempt, producer JSON 및 생산 Parent 소스다. 아래 경로·행은 `received/` 기준이다. 수신 파일을 텍스트·JSON 데이터로 읽고 해시를 대조했으며, 받은 코드·하네스·후보 함수·PowerShell 후보 엔진·COMSOL을 실행하지 않았다. 원본을 수정하지 않았다. 현재 호스트의 JSON 파서를 이용해 문제의 mutant를 재생성하거나 실제 실행 PC의 CLR 타입을 재현하지도 않았다.

## 결론

PARENT_R113은 **fixture 준비 전제 실패**다. 실제 첫 오류는 `HARNESS_FIXTURE_OR_ASSERTION:R113_DOUBLE_AFTER_JSON_PARSE`이고, `ps_harness.ps1:133`에서 발생했다. 해당 사례의 `S1Decision` 호출은 `:158`에 있으므로 목표 Parent 함수에 진입하기 전 중지했다. 이것을 `DECIMAL_TRANSPORT_PRECISION`의 성공적인 거부나 생산 Parent 결함으로 분류할 수 없다.

파싱 직후 값이 `[double]`이라는 전제가 거짓이었다는 점은 확인된다. 실제 타입이 Decimal, String, 다른 타입 중 무엇이었는지는 기록되지 않아 확정할 수 없다. 직접 원인은 분명하지만 엔진별 JSON 타입 선택의 세부 설명은 미관측이다. 추측한 Decimal을 관측 사실처럼 쓸 필요가 없다.

정정 범위는 R113의 수치형 fixture 생성·운송 관측과 한정 재검증 계획/하네스에 있다. 생산 Parent를 고칠 근거는 이번 실패에서 나오지 않았다. 명시적 fixture-only Double 변환을 새로 승인·봉인하여 원래의 Double 거부 목적을 유지하고, 최초 파싱 타입 및 변환 전후 증거를 함께 남기는 방안을 권고한다. 원 실패를 보존하며 자동 재시도는 하지 않는다.

## 1. 수신 기록과 정확 도달 경계

| 증거 | 확인한 사실 |
|---|---|
| `results/ps_first_failure.json:4–10` | current_case=PARENT_R113, case_count=28, status=INCOMPLETE, retry=0, later_cases_not_run=true |
| 같은 파일 `:5` | stack은 HRequire `:35` → harness `:133` |
| 같은 파일 `:9` | first_error=HARNESS_FIXTURE_OR_ASSERTION:R113_DOUBLE_AFTER_JSON_PARSE |
| `results/POWERSHELL_STDOUT.txt:1–28` | PARENT01–16, PARENT_R101–R112의 28개 PASS 기록 |
| 같은 stdout `:29` | 같은 current_case/first_error/case_count를 가진 중지 요약 |
| `results/POWERSHELL_SESSION.json` | rc=1, timed_out=false, raw_process_exit_observed=true, elapsed=30.2902513s, limit=300s, status=FIRST_UNEXPECTED_ENGINE_FAILURE |
| `results/POWERSHELL_STDERR.txt` | 빈 파일; 이것이 rc1/fixture 실패를 상쇄하지 않음 |

실패 JSON의 내부 elapsed=29.2539458s와 외부 session elapsed=30.2902513s는 관측 경계가 다르다. 둘을 합산하거나 300초 초과로 설명하지 않는다. Session의 `within_limits=false`라는 종합 필드만으로 timeout이었다고 해석하지 않는다.

R113의 실패 흐름은 다음과 같다.

1. `ps_harness.ps1:93–97`: POLICY02 원 producer 및 context를 `HProducer`로 읽는다. HProducer `:20–32`는 두 파일의 봉인 크기·SHA를 확인하고 결과와 context를 반환한다.
2. `:127–129`: 원 raw JSON에서 `voltage_V` 객체의 문자열 `"0.001"` value token을 찾고 정확히 한 번임을 요구한다.
3. `:130–131`: 그 두 따옴표만 제거한 숫자 token을 만들고 전체 길이가 정확히 2 작아졌는지 요구한다.
4. `:132`: mutant를 ConvertFrom-Json으로 파싱한다.
5. `:133`: 해당 leaf의 `[double]` 여부를 검사하고 실패한다. 앞의 regex·길이·parse가 오류를 발생시켰다면 stack/첫 이유가 달랐을 것이므로, 현재 기록과 소스 순서상 그 단계들은 이 검사까지 진행됐다. 다만 mutant 자체가 보존되지 않아 정확 바이트를 사후 독립 대조한 것은 아니다.
6. `:135`의 `parsed_clr_type`, mutant byte count/SHA, token offset을 담는 `recipeTransport` 생성에 이르지 못한다. `:139`의 reach 초기화, `:140`의 case clock, `:158`의 S1Decision 호출에도 이르지 못한다.
7. `:194–198`의 최상위 catch가 앞선 28개 기록과 오류를 저장하고 exit1로 종료한다. 실패 사례 전용 record를 추가하는 `:184–185`에도 도달하지 않았다.

따라서 사례 수를 정확히 분리해야 한다. 이번 PS 목표 함수 호출은 완료된 28개이며, R113은 준비 시도 후 목표 미진입, R114/R115는 시작하지 않았다. Python99의 별도 수용까지 충족한다면 완료 증거는 127개이고, 130개 전체 PASS가 아니다. R113에 관하여 이전 R112의 reach를 가져와 목표 도달 증거로 쓰면 안 된다. 현재 reach 목록 초기화 자체가 준비 분기 뒤이므로 후속 하네스는 사례 시작 시점에 이를 초기화하는 편이 분명하다.

## 2. 하네스·계획 불일치의 성격

`PS_INPUT_RECIPES.json:641–657`과 `PS_FIXTURE_MAPPING.md`의 R113 행은 실제 Python POLICY02 문자열 token의 따옴표를 제거한 뒤 CLR Double이 되어야 한다고 선언한다. `VALIDATION_PLAN_CORRECTED.json:4522,4539`도 Decimal을 포함한 다른 타입은 fixture FAIL이며 target PASS가 아니라고 명시한다. 하네스는 이 약속을 따라 멈췄다. 실패를 감추거나 다음 사례로 진행한 정황은 없다.

수신 POLICY02 원 JSON의 `comparison_details.maxima.voltage_V`는 `value="0.001"`, `time_s="120"`이다. 원 파일 식별은 122640 bytes, SHA `254164ec95da7af50e734baff70f6c804c28eb7854898912261699e8cb8c0880`로 PS producer seal에 결속되어 있다. 숫자화하려는 출발 자료는 기대한 문자열 경계에 맞는다. 그러나 JSON 숫자 token이라는 형식과 CLR Double이라는 구체 타입은 같은 주장이 아니다. 원 숫자 token을 만들었다는 사실만으로 그 엔진의 parse 결과를 Double로 확정할 수 없다.

관측 부족을 유발한 별도 하네스 문제는 `:133`의 실패하기 쉬운 전제 뒤에 `:135`의 운송 관측을 둔 순서다. catch `:195`도 현재 source/context, mutant identity, actual type/value, target_entered를 기록하지 않는다. 그래서 실패를 식별했지만 구체 타입을 잃었다. 최소 후속 정정에는 이 기록 순서도 포함되어야 한다.

## 3. 생산 Parent 결함으로 볼 수 없는 이유

현재 `source/candidate/Parent.ps1.inactive.txt`와 이전 정적 수용 R1 Parent의 전체 SHA가 모두 `e9f8d366ca9931b84ded5753a560369b72fea8737a77075bc2b80ec771bc56ff`로 일치한다.

생산 `S1ExactDecimal:27–35`는 문자열과 명시된 정수 CLR 타입만 받으며 Double·Decimal 등은 `DECIMAL_TRANSPORT_PRECISION`을 throw한다. `S1ComparisonNumerics:161,168`은 비교 값이 이런 타입이면 그 이유를 `comparison_numerics` 단계 실패로 반환하도록 작성되어 있다. 이것은 정적 예상이지 R113 실행 증거가 아니다. 이번 R113은 해당 호출 전에 하네스에서 중지했으므로 생산 함수가 잘못 수용했다거나 이유/단계를 잘못 반환했다는 기록이 없다.

이전 두 P2 정정의 관련 기록은 살아 있다. 수신 PARENT12는 실제 S1FinalReturn의 `limited=AWAITING_S1_LIMITED_EXTERNAL_REVIEW`, POST_WRITE, snapshot100, 오류0을 관측해 PASS로 남겼다. PARENT14도 CHARGE03의 실제 analyze producer로 `charge_budget=INCONCLUSIVE`, `evidence_validity=VALID`, 최종 INCOMPLETE를 관측했다. R113 fixture 실패를 이유로 이 기록들을 자동 폐기하거나 생산 코드 전반을 재작성할 필요는 없다. 각 기록의 봉인·무결성 수용은 전체 리뷰의 별도 전제다.

## 4. 최소 정정안 — 실제 JSON 타입 관측 후 명시적 Double fixture

다음은 새 승인에 넣을 설계 권고이며 현재 수정·실행한 내용이 아니다.

- R113의 원래 목적은 “Double로 운송된 scientific value를 생산 Parent가 거부한다”로 유지한다. 단순히 `[double]` 검사를 삭제하거나 `double|decimal`이라는 더 넓은 성공 전제로 바꾸어 이전 목표를 통과한 것처럼 쓰지 않는다.
- 원 POLICY02 producer와 context SHA, 정확 raw JSON 숫자 mutant bytes/SHA·대상 token offset·따옴표 두 개만 제거했음, parse 직후 실제 CLR 타입과 값은 **어떤 타입 전제 검사보다 먼저** 보존한다. 값이 null/string/비숫자/비유한/예상값 불일치라면 cast로 덮지 않고 fixture FAIL로 중지한다.
- 그다음 승인된 fixture 단계에서 해당 단일 leaf만 명시적으로 Double로 변환한다. 변환 전후 타입·값, 변환 후 Double raw 64-bit pattern, 다른 leaf의 불변을 기록한다. cast 후 Double 타입·예상 numeric value를 확인하고 단 한 번 S1Decision에 전달한다. raw mutant SHA만으로 in-memory cast를 봉인했다고 쓰지 말고 새 recipe/하네스 SHA와 실제 typed mutation 관측을 함께 결속한다.
- “JSON parser가 원래 Double을 반환했다”는 주장은 하지 않는다. 관측 목표는 “원 producer → raw numeric JSON mutant → 실제 parser type 관측 → 명시적 Double fixture → Parent 거부”로 바뀌므로 계획·recipe·mapping에 이 변경을 분명히 적는다. 이는 생산 소스 변경이 아니라 test fixture의 선언된 변환이다.
- 사례마다 입력 생성 전 current_case·target_entered=false·reach 빈 목록을 초기화하고, 준비 실패에도 위 진단을 기록한다. 후보 함수 도달 후에만 target_entered=true/실제 reach를 증거로 남긴다. 현재 `:171–183`의 reason/reach 검사에 더해 R113은 정확 `stage=comparison_numerics`, R114는 `stage=fields`를 확인한다.
- 기존 R1_003 실패·raw stdout/rc·봉인본은 그대로 보존한다. 새 root와 새 계획/하네스/producer 연계 봉인을 만들고 옛 `PS_PRODUCER_SEAL.json`의 harness SHA를 새 하네스에 그대로 적용하지 않는다. 그 seal은 이전 하네스 `36479c721efac2f14d29292f55d6e2d991fba52eed1914dd41ee95b73d389bb2`만 결속한다.

## 5. 실제 최소 후속 검증 범위

127개 기존 성공 기록의 소스·함수·입력·engine 결속을 재사용할 수 있다는 별도 수용하에, 새 목표 호출은 다음 **3개**가 최소다. 이는 기존 세션의 자동 재시도가 아니라 수정 fixture로 수행하는 별도 승인 검증이다.

| 새 실행 순서 | 생산자/변경 | 필수 관측 |
|---|---|---|
| PARENT_R115 | 같은 POLICY02 producer/context, 문자열0.001 그대로 | 실제 S1Decision 및 S1ComparisonNumerics 도달, comparison=WITHIN_LIMITS_THIS_WINDOW, 제한 검토 대기 |
| 개정 PARENT_R113 | 같은 POLICY02 producer/context, 승인된 raw 숫자 변이와 명시적 Double leaf | 준비 타입/값/비트 기록, 실제 S1Decision→S1Fields→S1ComparisonNumerics 도달, 정확 DECIMAL_TRANSPORT_PRECISION와 stage=comparison_numerics |
| PARENT_R114 | 같은 POLICY03 producer/context, 두 summary leaf만 WITHIN으로 변경 | 실제 S1Decision→S1Fields 도달, 정확 COMPARISON_SUMMARY_CONTRADICTION와 stage=fields |

R115를 먼저 실행하면 실패 사례 R113의 동일 producer 정상 문자열 대조를 후속 미실행 상태로 남기지 않는다. R114의 초과 양성 대조는 기존 PARENT02를 재사용할 수 있지만 다음 조건을 모두 명시해야 한다.

1. 생산 Parent 원바이트/추출 함수 SHA가 같고, 새 하네스의 공통 source loading·producer parse·반환 관측·입력 구성 의미가 바뀌지 않는다. 변경은 목표 subset 선택, R113 typed fixture, 진단 보존 및 명시된 stage 확인에 한정한다.
2. POLICY03 원 JSON은 기존 PARENT02의 122637 bytes/SHA `34e41940de1bb99d359b41b824bb86a9e6ba3c8c56083c5c1e2c739bac8d4ddc`, context는4551 bytes/SHA `fa996873b02d9138aee3b54fe5d1551b1ce98649488635b2d48a159b0af4f18d`와 정확히 같다. context의 Expected/Native/Analysis/Completion을 수제 새 자료로 대체하지 않는다.
3. 기존 PARENT02 raw record에는 S1Decision/S1NativeAxis/S1Fields/S1ChargeFields/S1Coverage/S1ComparisonNumerics 도달, VALID, charge CONSISTENT, comparison EXCEEDS_LIMITS, 최종 AWAITING_S1_LIMITED_EXTERNAL_REVIEW가 있다. 이 정확 기록과 producer/context, 동일 engine pin을 새 대조 재사용 표에 연결한다.

위 조건이 깨지거나 새 공통 하네스 경계까지 다시 확인해야 한다면 **PARENT02를 네 번째 신규 호출**로 사전 집계하고 R114 전에 둔다. 이를 숨은 양성 probe로 추가하지 않는다. R115의 일반 정상 대조 PARENT01도 같은 방식으로 기존 record를 재사용할 수 있다. R115 자체가 이번 세션에서 실제 정상 문자열 양성을 관측하므로 R113용 별도 다섯 번째 동일 입력 호출은 필요하지 않다.

새 subset 하네스/계획은 정확 ID·순서·입력·기대 stage를 고정해야 한다. 받은 하네스 `:80–88`은31개 전체를 고정하므로 단순히 다시 실행하면127개 재사용이라는 최소 범위와 다르다. 수정한 subset 계획/하네스를 사전 봉인하고 새 승인된 PS5.1 **1세션**, 후보 target **3개 또는 사전 승인4개**, Python 재실행0·예비probe0·native0로 한정할 수 있다. 시간 상한과 보존/전달 예산도 새 승인에서 분리 고정하며 이전1860초 중 남은 시간으로 자동 이어가지 않는다.

성공하더라도 보고는 “R1_003에서 수용한127개 + 별도 수정 검증의3개”라는 이력을 유지한다. 원 R113의 준비 실패를 PASS로 덮거나 한 세션에서130개가 성공했다고 쓰지 않는다. native_ready=false 및 installed/raw/OS adapter OPEN은 그대로다.

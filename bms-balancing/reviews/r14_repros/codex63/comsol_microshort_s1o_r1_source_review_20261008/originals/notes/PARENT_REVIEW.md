# S1O-R1 Parent·N1/N3·검증계획 독립 정적 검토

검토일: 2026-10-08. 범위는 `received/main/candidate/Parent.ps1.inactive.txt`, consumer의 신규 출력과 연결 분기, `contracts/CHARGE_BALANCE.json`, `contracts/EXECUTION_BINDING.json`, `SOURCE_CONTRACT_LINKS.json`, `VALIDATION_PLAN_R1.json`의 PARENT 사례이다. 아래 좌표는 별도 표시가 없으면 `received/main/` 기준이다. 이전 `microshort_s1o_preparation_review_20261007`의 원 소스와 E1/E2 및 N1/N3 지적도 텍스트로 대조했다.

수신 후보의 import, dot-source, 함수 추출 실행, 기능 테스트, Python/PowerShell 후보 엔진 호출, COMSOL/JVM/compile/gate/Job 호출은 수행하지 않았다. PowerShell 도구는 파일 텍스트 읽기·행번호 표시 및 단일 소스 행의 독립 UTF-8 SHA256 계산에만 사용했다. 아래 반례와 분기 결과는 코드 실행 관측이 아닌 정적 추론이다. 수신 원본은 수정하지 않았다.

## 판정

N1의 부모 측 전체 격자·끝시각·증거 식별 연결과 N3의 고정 요청 내용 검사는 원 지적에 대해 **정적 소스 정정 수용 가능**하다. 진짜 R1 producer의 정상/보호 결과가 새 Parent 스키마에서 필연적으로 거부되는 새 분기는 발견하지 않았다. 이는 기능 검증 통과나 raw/native 검증, native 실행 승인이 아니다.

현재 `VALIDATION_PLAN_R1.json`에는 아래 두 가지 확정된 정적 불일치가 있다. 따라서 이 검토 범위의 **후속 기능 검증 계획은 정정 후 재봉인이 필요**하다. raw adapter 등 공개된 OPEN과 별개로 이미 작성된 계획의 좌표·관측 경로 오류이다.

## PR1 / P2 — S1Sha 함수가 빈 추출 범위와 빈 문자열 해시로 봉인됨

- 위치: `VALIDATION_PLAN_R1.json:5231–5236`; 실제 함수 `candidate/Parent.ps1.inactive.txt:23`.
- 계획은 `start_line=23`, `end_line=22`, SHA `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`를 지정한다. 끝이 시작보다 앞이고, SHA는 빈 바이트열의 값이다.
- 실제 23행은 `function S1Sha($Value) { return $Value -is [string] -and $Value -cmatch '^[0-9a-f]{64}$' }`인 비어 있지 않은 한 줄 함수이다. 명시된 LF 정규화·마지막 LF 제외 규칙으로 이 행은 UTF-8 90바이트이고 독립 계산 SHA는 `13c6456b30805e3b02063ca8cb804b201d948c5518bf01b102610297236d8eed`이다.
- 도달/영향: 이 함수는 `S1Decision:297`, `S1NativeAxis:185`, `S1Fields:238`, `S1ChargeFields:124` 등에서 실제로 필요하다. 현재 봉인대로 빈 텍스트를 추출하면 해당 함수를 정의하지 못한다. 다른 위치에서 함수를 임의 보충하면 현재 함수 봉인과 달라진다. 계획의 preseal 요구 `:4958`(정확 추출 좌표와 span SHA)에도 어긋난다. 따라서 기능 테스트를 시작하기 전에 정적 preseal에서 중단해야 한다.
- 최소 조치: 구간을 실제 23행 전체로 정정하고 선언한 정규화에 맞춘 SHA를 재발행한다. 이를 만드는 추출 도구가 한 줄 함수에서도 비어 있지 않은 정확한 span을 산출하는지 정적으로 확인한다. 새 함수 테스트나 전체 엔진 실행은 이 조치에 필요하지 않다.

## PR2 / P2 — PARENT12 정상 최종 반환의 관측 필드가 실제 스키마와 다름

- 위치: `VALIDATION_PLAN_R1.json:2888–2915`, 특히 `:2914`; 실제 반환 `candidate/Parent.ps1.inactive.txt:370–373`.
- 계획상 PARENT12는 `S1FinalReturn`에 정확한 상한 이내의 정상 writer/readback/clock 증거를 주고 `AWAITING_S1_LIMITED_EXTERNAL_REVIEW`를 기대하는 양성이다. 그러나 `expected_field_path`는 `return_value.status`, `observation_mode`는 `powershell_return_classification`이다.
- 실제 `S1FinalReturn`은 성공 상태를 `limited`에 반환한다. 반환 hashtable에 `status` 키는 없고, `prior_decision.status`는 별도의 입력 결정 값이다. 정확 상한을 통과한 정상 입력에서도 현재 관측 경로의 값은 기대 문자열이 아니다. `status`를 사후 만들어 넣는 wrapper는 실제 반환 스키마 검증이 아니다.
- 최소 조치: PARENT12를 `return_value.limited` 및 `powershell_final_boundary_classification`으로 맞춘다. 같은 함수 음성 PARENT09/10/11/16은 이미 이 경로를 사용한다 (`:2824–2825`, `:2854–2855`, `:2884–2885`, `:3036–3037`).
- 양성 대조군 연결도 함께 정정해야 한다. PARENT09/10/11/16의 `positive_control_case_id`는 모두 PARENT01인데 PARENT01의 목표는 `S1Decision`이다 (`:2553–2558`). 계획 `:4950`은 함수/fixture 봉인이 일치하는 양성 재사용만 허용하며 미등록 추가 호출을 금지한다. 정상 `S1FinalReturn`을 관측하도록 고친 PARENT12를 네 음성 사례의 명시적 대조군으로 연결하고 각 writer/clock/readback의 기준과 단일 변이를 구체화하면 기존 사례 수를 늘리지 않고 수선할 수 있다.

## N3 원 반례 및 정확 정밀도 경계

원 반례는 유효한 producer 결과의 `comparison_times`와 `full_intersection`을 각각 문자열 `"0"` 255개로 바꾸고 개수·요약·다른 증거를 유지하는 입력이었다. R1에서는 다른 새 charge/Native 증거를 유효하게 유지한 뒤 이 변이만 적용하면 `S1Coverage:85` → `S1TimeVector:62–63`에서 두 번째 0이 이전 0보다 크지 않아 `COMPARISON_TIME_ORDER_OR_RANGE`를 내며 coverage 단계에서 종료한다. 예전 count-only 수용 경로는 남지 않았다. 새 charge 스키마를 누락하여 더 앞에서 거부되는 것을 이 반례의 해결 증거로 세지 않았다.

동일 길이의 다른 증가 시각은 `:88–89`의 고정 요청과 값 대조에서 `COMPARISON_TIME_CONTENT`로 거부된다. 비교 목록이 full intersection에 없으면 `:100–102`, 교집합 시각이 Native 저장 격자에 없으면 `:93–96`에서 각각 거부된다. 정렬·중복·범위·시작0은 `:59–67`이 확인한다. 생산자 보고 count를 Expected의 기준으로 되돌려 쓰지 않는다.

`S1ExactDecimal:27–50`과 `S1ExactCompare:51–58`은 십진 문자열을 부호·유효숫자·자릿수로 비교한다. `S1ComparisonNumerics:156–169`에서 `0.0010000000000000000001`은 `0.001`보다 크므로 정상 EXCEEDS 결과를 소비자 요약과 일치시키고, 두 요약을 WITHIN으로 바꾸면 `S1Fields:293`에서 거부한다. 정확 `0.001`은 포함 경계다. JSON 부동소수점/CLR decimal은 `DECIMAL_TRANSPORT_PRECISION`으로 거부하며, 이는 계약과 계획이 명시한 입력 운송 제한이다. 실제 두 엔진 경계 증거는 아직 없다.

## 정상 및 보호중단 연결의 정적 추적

`EXECUTION_BINDING.json:172–188`은 Expected에 고정 전체 요청 벡터와 전체 count를 연결하고, 검증된 Native의 전체 저장 격자·actual end·safe end를 별도로 제공하도록 규정한다. `CHARGE_BALANCE.json:143–162`와 구현이 이 구분에 맞는다.

| 축 | 정상 120초 | 보호중단 예시 |
|---|---|---|
| 고정 Expected 요청 | sparse255 전체, required_count=255 | 같은 sparse255 전체, required_count=255 |
| Native actual end | 120 | t_plus=90.1 |
| 검증된 safe end | 120 | t_minus=90, Native 격자 끝에서 두 번째 |
| charge/global/native 시간 | 전체 실제 격자 끝120 | 전체 실제 격자 끝90.1, 마지막 구간 포함 |
| comparison_times | 고정 요청 전체255 | 고정 요청 중 ≤90인249개 |
| full_intersection 허용 상한 | actual120 | actual90.1, 공통이면 t_plus도 유지 가능 |
| 최종 Parent 상태 | CONSISTENT이면 외부 제한 검토 대기 | PROTECTIVE_STOP_INCOMPLETE |

정상: consumer `:365–370`은 safe=end와 공통 요청 결속을 확인하고, `charge_balance:231–237`은 full native/global/charge 격자와 actual/configured/safe endpoint를 맞춘다. Parent `S1NativeAxis:184–207`가 이를 독립 Native 축과 결속하고, `S1ChargeFields:111–149`가 producer의 각 record time·격자·끝시각·출처를 대조한다. `S1Coverage:72–89`의 전체 요청 대조 후 `S1Decision:321–337`로 연결된다.

보호: Native `:192–198`은 t_minus<t_plus=final<configured와 Native[-2]=t_minus를 요구한다. 반환 `:212–214`에서 safe=t_minus, actual=final이다. `S1Coverage:72–75`는 전체255를 훼손하지 않고 safe prefix를 새로 유도한다. sparse 벡터에서90 다음은95,100,105,110,115,120 여섯 시각이므로255−6=249이다 (`POLICY_VARIANTS.json:1605–1611`). full intersection은 `:86`에서 actual90.1까지 허용하므로 안전 비교 구간90을 넘는 정상 공통 t_plus를 그것만으로 거부하지 않는다. 소비자는 보호시 limited_result=INCOMPLETE를 유지하고 Parent `:321–324`가 그 값을 확인한 뒤 `:333`의 보호 최종 분기에 도달할 수 있다. 예전 보호 prefix와 전체 count 불일치에 의한 필연적 조기 거부는 정정되었다.

부모 측 증거 불일치: charge actual_end만119.9로 바꾸면 `:118–120`의 CHARGE_ENDPOINT_BINDING, record t만 바꾸면 `:138–139`의 CHARGE_RECORD_TIME_BINDING, global_identity SHA만 바꾸고 source_evidence는 유지하면 `:126–127`의 CHARGE_SOURCE_NOT_REGISTERED가 목표 경로다. 독립 Native의 grid identity와 producer identity가 달라도 `:129–130`에서 거부한다. 모든 물리를 Parent에서 재계산할 필요가 있다는 주장은 하지 않는다.

## OPEN 및 후속 봉인 조건

- raw/native adapter와 Native/Expected projection 생성은 명시적으로 OPEN이다. 현재 summary와 임의 identity가 실제 원본 관측임을 증명한다고 읽지 않았다. Parent에 고정 Expected와 독립 Native 축을 주어야 한다는 전제는 위 정적 수용의 경계다.
- `S1FinalReturn`은 R1에서 바뀌지 않았고 writer/readback 뒤 시간 재검사, 이전 실패 보존, raw_host_rc=null을 유지한다. PR2는 이 함수의 새 실행 결함이 아니라 검증 계획의 반환 관측 불일치다.
- PARENT_R108은 두 count와 시간 배열, PARENT_R114는 두 summary를 바꾸도록 기술하면서 공통 reach_rule과 preseal `:4964`는 sole-field 변이만 말한다. 두 사례의 의도 자체는 도달 분기와 맞는다. 후속 봉인에서는 허용할 정확한 복수 leaf-field 목록을 명시하거나 단일 대상 변이로 좁혀 계획 문구를 일치시킬 것. 이 보완을 PR1/PR2와 별개 핵심 소스 결함으로 세지는 않는다.
- 본 노트는 기능 검증을 실행하거나 승인하지 않는다. PR1/PR2 및 나머지 독립 리뷰의 필수 정정을 반영한 봉인본으로만 다음 별도 승인을 논의할 수 있다. native_ready=false, overall/normal_gate=INCOMPLETE는 유지되어야 한다.

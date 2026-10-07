# S1-O 변경부 한정 검증안 — 미승인·미실행

새 순수 소비/제어/부모 함수 **8군·98개 고유 사례**만 제안한다. Python 82 + PowerShell 16. 사례 수는 assertion 수가 아니다.

Python 1세션 300초, 일반 Windows PowerShell5.1 NoProfile 1세션 180초. 봉인600 + 보존/전달300 + 미완기록120을 포함해 전체1,500초. fixture≤1GiB, 기록≤50MiB, 시작여유≥2GiB. Java/JVM/COMSOL0. 이 값은 별도 사용자 승인 제안이다.

실제 실행 전 하네스·fixture·추출 범위/해시·엔진 현재 바이트·정확 argv/cwd·각 입력 기대 이유와 도달함수를 봉인한다. 범위를 바꾸지 않고 구체화한다. 계획 JSON의 복합 함수 목록은 하네스에서 실제 도달할 한 경로로 정해야 하며 뜻밖의 앞단 거부를 목표 PASS로 세지 않는다. 받은/생산 코드를 현재 import하지 않았다.

합성의 양성 fixture는 설치본의 사실을 대신하지 않는다. 현재 native_ready=false를 true로 바꾸는 운영승인 파일을 만들지 않는다. native/콘솔/Job/프로세스 진입은 대상 로드 전에 inert로 막는다. 실제 Python analyze 산출물을 PS S1Decision에 그대로 연결한다. 후보 및 이전 source는 수정하지 않는다. 첫 예상 밖 실패/시간/크기 초과에서 후속 엔진을 멈추며 자동 수정·재시험·probe·다른 셸·정책 변경은 없다.

| ID | 실제 대상 | 입력/목표 | 기대 결과 |
|---|---|---|---|
| AUTH01 | authorize_execution | complete future fixture only | AUTHORIZED_ONE_RUN |
| AUTH02 | authorize_execution | missing approval | SEPARATE_NATIVE_APPROVAL_REQUIRED |
| AUTH03 | authorize_execution | wrong source bytes | SOURCE_IDENTITY |
| AUTH04 | authorize_execution | wrong engine pin | ENGINE_OR_DEPENDENCY_IDENTITY |
| AUTH05 | authorize_execution | wrong validation binding | VALIDATION_ACCEPTANCE_BINDING |
| AUTH06 | authorize_execution | wrong sigma/run unit | APPROVED_RUN_UNIT_MISMATCH |
| AUTH07 | authorize_execution | extra solve count | CALL_COUNTS_NOT_APPROVED |
| AUTH08 | authorize_execution | changed cwd/argv | COMMAND_OR_CWD_MISMATCH |
| AUTH09 | authorize_execution | existing runtime path | PATH_OR_CONCURRENT_WORK |
| AUTH10 | authorize_execution | policy changed or elevated | POLICY_OR_PRIVILEGE_MISMATCH |
| AUTH11 | authorize_execution | prior attempt exists | NO_RETRY_EXISTING_ATTEMPT |
| AUTH12 | authorize_execution | current native_ready false | OFFLINE_NATIVE_NOT_READY |
| AUTH13 | authorize_execution | native command null | NATIVE_COMMANDS_UNRESOLVED |
| AUTH14 | authorize_execution | native paths null | NATIVE_PATHS_UNRESOLVED |
| AUTH15 | authorize_execution | current policy pin null | CURRENT_POLICY_PIN_UNRESOLVED |
| READ01 | read_csv_bytes | valid raw CSV+units then exact profile | RETURN_VALID_ROWS |
| READ02 | read_csv_bytes | raw SHA mismatch | CSV_IDENTITY |
| READ03 | read_csv_bytes | unit mismatch | UNIT_EVIDENCE |
| READ04 | read_csv_bytes | wrong header | CSV_HEADER |
| READ05 | read_csv_bytes | short row | CSV_WIDTH |
| READ06 | read_csv_bytes | NaN numeric | NONFINITE |
| READ07 | read_csv_bytes | empty numeric CSV | EMPTY_CSV |
| READ08 | timed_rows | duplicate time | DUPLICATE_OR_UNORDERED_TIME |
| READ09 | coverage | required positive time missing | REQUIRED_TIME_MISSING |
| READ10 | coverage | empty/t0-only comparison | EMPTY_OR_ZERO_ONLY_COMPARISON |
| READ11 | profile_rows | wrong coordinate/domain | COORDINATE_DOMAIN |
| READ12 | profile_rows | missing profile row | PROFILE_MISSING |
| INIT01 | compare_initialization | all initial targets exact | PASS |
| INIT02 | compare_initialization | exact absolute and relative boundaries | PASS |
| INIT03 | compare_initialization | inventory boundary excess | INITIAL_INVENTORY_OR_COMPOSITION |
| INIT04 | compare_initialization | first positive sample substituted for0 | INITIAL_TIME_NOT_EXACT_ZERO |
| INIT05 | compare_initialization | no postconsistency proof | INITIAL_PROVENANCE_OR_TARGETS |
| INIT06 | compare_initialization | initial wrong unit | INITIAL_UNIT |
| INIT07 | verify_coefficient_evidence | configured coefficient mismatch | COEFFICIENT_SETTINGS |
| INIT08 | verify_coefficient_evidence | settings only consumption claim | EFFECTIVE_COEFFICIENT_OPEN |
| INIT09 | verify_coefficient_evidence | matched installed mapping fixture | PASS |
| INIT10 | verify_coefficient_evidence | actual coefficient exceeds fixed tolerance | COEFFICIENT_CONSUMPTION |
| INIT11 | compare_initialization_pair | both valid individual initialstates butpairdifferenceexceeds | PAIR_INITIAL_STATE_MISMATCH |
| INIT12 | initial_profile_uniformity | particleaverage nonuniformatoneinitialcoordinate | INITIAL_PROFILE_NONUNIFORM |
| POLICY01 | compare_policy | 255 exact requests and extra common states | WITHIN_LIMITS_THIS_WINDOW |
| POLICY02 | compare_policy | voltage exactly1mV | WITHIN_LIMITS_THIS_WINDOW |
| POLICY03 | compare_policy | voltage above1mV valid native | EXCEEDS_LIMITS |
| POLICY04 | compare_policy | surface exactly1e-4 | WITHIN_LIMITS_THIS_WINDOW |
| POLICY05 | compare_policy | surface above1e-4 | EXCEEDS_LIMITS |
| POLICY06 | invariants | individual Li drift above1e-6 | LI_DRIFT |
| POLICY07 | invariants | decomposition above1e-8 | VOLTAGE_IDENTITY |
| POLICY08 | compare_policy | matched count but wrong coordinate | COORDINATE_DOMAIN |
| CHARGE01 | charge_balance | resolved balanced series with adequate bound | CONSISTENT |
| CHARGE02 | charge_balance | nearzero signal includingt0 | INCONCLUSIVE |
| CHARGE03 | charge_balance | unknown quadrature bound | INCONCLUSIVE |
| CHARGE04 | charge_balance | bound above quarter allocation | INCONCLUSIVE |
| CHARGE05 | charge_balance | reverse current beyonddeadband | REVERSE_CURRENT |
| CHARGE06 | charge_balance | RN/RP inconsistency | REACTION_CURRENT_BALANCE |
| CHARGE07 | charge_balance | I vsA*j mismatch | CURRENT_AREA_CONVERSION |
| CHARGE08 | charge_balance | reverse Li transfer beyonddeadband | REVERSE_LI_TRANSFER |
| CHARGE09 | charge_balance | qN-qP exceeds | SOLID_TRANSFER_BALANCE |
| CHARGE10 | charge_balance | integral residual plus bound exceeds fixedlimit | INTEGRATED_CHARGE_BALANCE |
| CHARGE11 | charge_balance | reordered integral time | CHARGE_TIME |
| CHARGE12 | charge_balance | totalLi drift | LI_DRIFT |
| PAIRED01 | paired_classification | D,S strictly above5E andabsolute thresholds | DISTINGUISHABLE_AT_REST |
| PAIRED02 | paired_classification | smallD/S smallE | NOT_DISTINGUISHABLE_WITHIN_T |
| PAIRED03 | paired_classification | large numerical sensitivity masks signal | INCONCLUSIVE |
| PAIRED04 | paired_classification | D equalspositive threshold | INCONCLUSIVE |
| PAIRED05 | paired_classification | one Kaxis missing | K_INCOMPLETE |
| PAIRED06 | paired_classification | same-sigma pairing false | UNMATCHED_K_PAIR |
| PAIRED07 | paired_classification | 2700endpoint missing | PAIRED_ENDPOINT_MISSING |
| RESOURCE01 | assess_resources | fresh measuredownedjob belowthresholds | CONTINUE_WITHIN_SAMPLED_LIMITS |
| RESOURCE02 | assess_resources | counter absent | STOP_REQUIRED |
| RESOURCE03 | assess_resources | counterNaN | STOP_REQUIRED |
| RESOURCE04 | assess_resources | ownership missing | STOP_REQUIRED |
| RESOURCE05 | assess_resources | doublecount aggregation | STOP_REQUIRED |
| RESOURCE06 | assess_resources | memory exceeds early stop | STOP_REQUIRED |
| RESOURCE07 | assess_resources | sample gap too long | STOP_REQUIRED |
| RESOURCE08 | assess_resources | wall entersstopreserve | STOP_REQUIRED |
| RESOURCE09 | advance_stop | supported cooperative request | WAITING_COOPERATIVE |
| RESOURCE10 | advance_stop | unsupportedwithoutforceapproval | UNRESOLVED |
| RESOURCE11 | advance_stop | unsupportedexplicitforceapproved | FORCE_PENDING |
| RESOURCE12 | advance_stop | cooperativewaitexpires | FORCE_PENDING |
| RESOURCE13 | advance_stop | force succeeded not yetverified | VERIFY_PENDING |
| RESOURCE14 | advance_stop | remaining member after force | UNRESOLVED |
| RESOURCE15 | advance_stop | verified emptyjob androot exit | TERMINATED_VERIFIED |
| RESOURCE16 | execute_once | authorizationdeny before spy firstsideeffect | OFFLINE_NATIVE_NOT_READY |
| PARENT01 | S1Decision | actual Python valid result +complete native evidence | AWAITING_S1_LIMITED_EXTERNAL_REVIEW |
| PARENT02 | S1Decision | actual Python valid numericalexceedance | AWAITING_S1_LIMITED_EXTERNAL_REVIEW |
| PARENT03 | S1Decision | actual Python protective stop | PROTECTIVE_STOP_INCOMPLETE |
| PARENT04 | S1NativeAxis | childrc wrongtype/nonzero | NATIVE_INVOCATION_OR_FATAL |
| PARENT05 | S1NativeAxis | rc0fatal | NATIVE_INVOCATION_OR_FATAL |
| PARENT06 | S1Fields | missing nestedfield | INCOMPLETE |
| PARENT07 | S1Fields | forgedcomparison summary | COMPARISON_SUMMARY_CONTRADICTION |
| PARENT08 | S1Fields | init/configonly success claim | INITIALIZATION_OR_ACTUAL_COEFFICIENT_UNVERIFIED |
| PARENT09 | S1FinalReturn | record writer throws | INCOMPLETE |
| PARENT10 | S1FinalReturn | postwrite totaloverrun | INCOMPLETE |
| PARENT11 | S1FinalReturn | postwrite deliveryoverrun | INCOMPLETE |
| PARENT12 | S1FinalReturn | postwrite exact limits andsuccess | AWAITING_S1_LIMITED_EXTERNAL_REVIEW |
| PARENT13 | S1Decision | Expected missing positiveend/requestcount | EXPECTED_REQUIRED_FIELDS |
| PARENT14 | S1Decision | chargeINCONCLUSIVE producer cannotbe promoted | INCOMPLETE |
| PARENT15 | S1Fields | initial_profile evidence missing | EVIDENCE_AXIS_MISSING:initial_profile |
| PARENT16 | S1FinalReturn | negative deliveryelapsed fromfuturestart | INCOMPLETE |

## 다음 승인 제안

> 고정 S1-O source의 8군·98사례 변경부 검증 1건만 승인합니다. 제시된 엔진·세션·1,500초·디스크 한도 안에서 먼저 하네스를 봉인하고 첫 예상 밖 실패에서 멈추세요. 실제 COMSOL·JVM·compile·gate·정책·native 승인/release/runtime/token 생성은 제외합니다. 결과 제출 뒤 멈추세요.

이 문구는 채택 전 비활성 초안이다. 검증 결과 수용과 설치본 초기화/계수·OS자원 어댑터의 OPEN 종결 뒤에만 새 실행본과 자원 조건을 명시한 S1-P 승인문을 확정할 수 있다. 검증 통과로 P/M/N을 자동 승인하지 않는다. 전체 세부 식별·명령은 VALIDATION_PLAN.json을 따른다.

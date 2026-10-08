# 실행·자원·부모 연결 정적 검토

검토 대상은 `received/candidate/control.py.inactive.txt`, `Parent.ps1.inactive.txt`, `contracts/EXECUTION_BINDING.json`, `RESOURCE_CONTRACT.json`, `VALIDATION_PLAN.json` 및 설명문이다. 아래 좌표는 `received/` 아래 파일의 원문 행이다. 받은 코드의 실행·import·함수 추출 실행·합성 시험·COMSOL/JVM/compile/gate/Job 호출은 0이다. 아래 입력 예시는 실행한 재현 결과가 아니라 분기 추적이다.

native 어댑터·현재 설치본 관측·실제 승인 경로 미구현은 제출물이 명시한 OPEN으로 인정한다. 그 사실을 새 결함으로 재분류하지 않는다. 후보는 현재 바이트에서 실행 불가 상태이며, 발견한 부모 판정 문제를 현재 native 승인 우회나 실제 오판 관측이라고 주장하지 않는다.

## E1 — 보호 중단의 유효 비교 prefix와 부모 required_count 연결 (검증안 구체화 조건)

주 좌표: `candidate/Parent.ps1.inactive.txt:117–124`, 특히 118–119행. 생산자 근거: `candidate/consumer.py.inactive.txt:66–83`, `:295–300`, `:313`. 계획: `VALIDATION_PLAN.json:1267–1278` (PARENT03), `:88` (실제 Python 반환을 PS에 연결).

생산자는 GUARD_STOP에서 비교 끝을 `guard_pair.t_minus`로 제한하고(297–300행), `coverage`가 공통 요청을 그 끝시각 이하로 자른다(70–78행). 정상적인 보호 중단에서는 전체120초 공통255개 중 유효 prefix만 남는 것이 맞다. 예를 들어 `t_minus=60`이면 초기187개+5.5–30의50개+35–60의6개=243개다.

부모는 native 축을 먼저 `PROTECTIVE_STOP`으로 판정하더라도(46–51행, 160행), `S1Fields`에서 `common_requested_count == Expected.required_count` 및 `comparison_count >= Expected.required_count`를 요구한다. 기본 P의 전체255개를 Expected로 유지한 정상 fixture는 여기서 `COMPARISON_COVERAGE`로 반환된다. `S1Decision`은 169행에서 그 실패를 즉시 반환하므로 183행의 `PROTECTIVE_STOP_INCOMPLETE`에 도달하지 않는다. 이는 실제 분석 결과를 쓰는 PARENT03의 기대 상태와 연결되지 않는다.

조건을 정확히 한정한다. 하네스/후속 adapter가 Expected.required_count를 신뢰된 t_minus와 사전 고정 요청집합에서 계산한 prefix 개수로 만들면 이 경로는 도달 가능하다. 따라서 보호 중단의 절대적 구현 불능은 아니다. 하지만 현재 Expected에는 요청집합·safe_end·검증된 guard prefix의 생성 계약이 없고, 계획에도 이 변환이 없다. 정상 fixture의 expected count를 단순히 출력 count로 덮어 맞추면 결손 검사를 무력화한다.

구체화 조건: 부모 입력에 사전 고정 요청격자와 신뢰된 중단 경계를 연결하고, 정상 완료는 전체격자, 보호 중단은 검증된 t_minus 이하 prefix와 대조하도록 규칙을 고정한다. PARENT03에는 120초 전에 멈추어255개보다 적은 실제 analyze 결과를 지정하고, 그 결과가 `PROTECTIVE_STOP_INCOMPLETE`에 도달하는 경로를 다음 승인 검증안에 봉인한다. 현재 여기서 실행할 필요는 없다. Expected를 구성하는 어댑터가 아직 OPEN이므로 이것만으로 현재 함수의 필수 코드 결함을 확정하지 않는다.

## E2 — 부모 coverage는 개수만으로 잘못된 시각 목록을 유효로 받을 수 있음 (P2, 채택 권고 finding)

주 좌표: `candidate/Parent.ps1.inactive.txt:117–124`; 성공 반환 `:144`, `:168–187`. 설명 근거: `notes/EXECUTION_RESOURCE_KO.md:17`은 exact common/request coverage를 부모 판정 요건으로 설명한다.

나머지가 정상인 생산자 결과에서 `comparison_times`를 문자열 `"0"` 255개로, `full_intersection`도 `"0"` 255개로 바꾸고 `common_requested_count=255`, `comparison_count=255`, coverage.status=`PASS`를 유지한다고 가정한다. 현재 부모 조건은 두 배열의 개수만 보므로 이 변경을 검출하지 않는다. 목록 원소의 수치 유효성·중복·순서·요청집합 일치·0/end coverage는 검사하지 않는다. 최대차 수치와 그 밖의 증거가 정상이라면 `VALID_FIELDS`, 이어 `evidence_validity=VALID`/`AWAITING_S1_LIMITED_EXTERNAL_REVIEW`가 유지된다.

이것은 검증된 진짜 consumer가 그런 목록을 정상 생성한다는 뜻이 아니다. 생산자와 반환 바이트의 신뢰가 완전히 확보되면 이 예시는 발생하지 않는다. 원시 파일 hash 확인 어댑터의 미구현이나 임의 파일 변조 공격을 이 함수가 반드시 해결해야 한다고 주장하는 것도 아니다. 현재 parent가 잘못된 nested evidence/summary를 검사하는 계층으로 제안되었는데 exact grid를 count만으로 판정하는 입력 경계 문제이다. 라벨도 실행 승인/PASS가 아니라 외부 검토 대기이며 overall/normal_gate는 여전히 INCOMPLETE다.

최소 보완: E1의 고정 기대격자/prefix와 실제 comparison_times를 내용까지 비교하고, full_intersection은 유한·정렬·중복없음 및 비교격자 포함 조건을 검사한다. 같은 count의 잘못된 시각, 중복시각, 끝시각 누락을 정확한 거부 이유로 다음 parent 음성 사례에 포함한다. 모든 물리를 parent에서 재계산할 필요는 없다.

## E3 — 최초 증거 생성의 부분 실패 시 closeout 책임은 다음 어댑터 계약에서 명확히 할 것 (조건부 보완)

좌표: `candidate/control.py.inactive.txt:293–298`, `:313–325`; 설명 계약 `:279–282`, `notes/EXECUTION_RESOURCE_KO.md:38`. 현재 검증안의 execute_once 대상은 `VALIDATION_PLAN.json:1225–1236`의 RESOURCE16 승인 거부 한 사례뿐이다.

`create_exclusive_evidence_and_reserve_one_attempt`가 모두 반환한 뒤에야 prepared=True가 된다. 이 콜백이 소유 증거 디렉터리/일부 기록을 만든 뒤 예약 쓰기에서 예외를 내면 prepared=False 상태라 finally의 소유 정리·보존·최종기록 콜백이 모두 생략된다. 현재 함수는 메모리 result.errors에 첫 오류를 남겨 반환하므로 오류가 전부 사라진다는 주장은 아니다. 아직 native 프로세스는 시작 전이므로 COMSOL이 남는다는 주장도 아니다.

이 콜백이 실패 전에 발생한 side effect의 소유권을 반환하거나 자체적으로 실패 기록/보존을 끝내야 한다는 계약을 명시하면 해결할 수 있다. 현재 어댑터는 OPEN이므로 이 항목을 곧바로 독립 차단으로 올릴 필요는 없다. 다만 후속 구현에서 전부 원자적인 호출이라고 가정해서 넘기지 말아야 한다. inert spy가 일부 생성 후 예외를 내는 경로와 첫 compile/batch/최종기록 실패의 오류보존을 다음 변경부 검증에 연결할 수 있다. notes의 넓은 검증 표가 현98사례에서 모두 실행된다는 의미로 읽히면 안 된다.

## 검토상 수용 가능한 부분과 범위 한계

- `authorize_execution:51–140`은 입력 dict·binding/manifest schema, payload/engine/dependency identities, validation evidence/approval/unit 결속, 경로/정책/기존시도와 native_ready/adapter_ready를 선행 검사한다. `execute_once:285–297`의 첫 외부 동작은 이 게이트 뒤다. 현재 제출 binding의 명시된 OPEN을 근거 없이 승인 가능으로 올리는 경로는 확인하지 않았다.
- `assess_resources:143–202`는 숫자의 유한성, required counters, 샘플 상태/범위/집계 표식, 자원 상한·예비시간을 판정한다. OS sampler나 실측 집계 검증이라는 주장은 하지 않고 계약도 sampled-only 한계를 명시한다. 이 리뷰에서 OS 동작을 확인한 것은 아니다.
- `advance_stop:205–267`는 소유확인 실패 및 deadline 초과를 UNRESOLVED로 두고, 미지원 협조정지의 force-only 권한, 한정 대기, 강제 종료 반환과 종료 확인을 분리한다. 실제 종료 API/OS 확인은 OPEN 상태로 유지해야 한다.
- `S1FinalReturn:189–224`는 writer/readback 뒤 clock 재검사, 전달/전체 상한, 이전 오류 보존을 검사하며 clock을 되돌리거나 최종 쓰기가 상한을 넘었을 때 외부 검토 대기를 유지하는 명백한 분기는 발견하지 않았다. `raw_host_rc=null`은 실행 프로세스 종료코드 미관측 경계를 정확히 남긴다.
- 검증안의1,500초는 600+300+180+300+120의 합과 일치한다. Java/JVM/COMSOL0 및 사용자 채택 전 비활성 검증 제안이라는 경계가 유지된다. 테스트 수 증가나 이 메모의 예시 실행은 승인하지 않았다.

## 추천 처리

핵심 finding은 E2의 “부모에서 고정 비교격자 내용을 확인”하는 P2 경계 보완이다. E1은 그 과정에서 보호 중단의 Expected 생성 규칙 및 PARENT03을 구체화할 조건이며 독립 필수 코드 결함으로 세지 않는다. 현재 candidate/contract의 비활성 준비 수용, 계획의 해당 사례 구체화, 후속 native 어댑터 OPEN을 서로 구분한다. E3는 실제 어댑터 연결 시 소유권·오류 기록의 명시 조건으로 남기고 현재 핵심 finding에서 제외한다.

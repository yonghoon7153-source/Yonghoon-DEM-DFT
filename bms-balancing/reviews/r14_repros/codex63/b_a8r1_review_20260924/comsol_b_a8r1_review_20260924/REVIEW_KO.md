# B_A8R1 제한 오프라인 배치 — 수신 독립 검토

2026-09-24. 요청된 xhigh 검토 범위. **제한 오프라인 배치·전달 증거 수용. C1/C3 종결. 실제 B는 보류 — C2 실제 호출 경로의 TTY 사전조건과 별도 사용자 승인 미완.**

이번 검토 범위에서 새 차단 반례를 찾지 못했다. 이는 전체 코드 무결함, native 실행 가능, COMSOL 수치 회수 성공 또는 장시간 GO 판정이 아니다. 수신 ZIP/봉인 파일은 변경하지 않았다.

## 1. 검사 대상과 실행 범위

수신 파일: `C:/Users/Administrator/Downloads/COMSOL63_B_A8R1_HANDOFF_20260924.zip`.

대상은 새 `api_recovery_B_A8R1` 실행 후보와 제한 배치의 증거다. A8의 389개 전체 suite나 물리 모델을 다시 심사하는 작업은 아니다. 직전 실행본 계획 검토에서 요구한 C1/C3, 유지된 C2를 중심으로 실제 코드·시험 원자료·최종화 자료를 대조했다.

- 데이터 검사: ZIP 3겹의 정확 집합·크기/SHA·CRC·이름/경로/타입, source seal, code manifest, 원시 결과와 개별 사례, 외부 반환과 시간 원점, 보존 목록.
- 정적 검사: 새 `deployment_verify.py`, `deployment_package.py`, `test_deployment_binding.py`와 의존 판정 함수, 고정 launcher의 승인/TTY 순서. 허용 diff와 이전 수신 A8 바이트를 비교했다.
- 독립 판정 확인: 검토한 순수 함수 정의만 AST로 분리해 메모리 값 변이 및 읽기 전용 입력에 적용한 **33건 PASS**. 모듈 최상위·수신 suite·launcher/native 제어는 실행하지 않았다. 목록과 추출 함수/SHA는 `INDEPENDENT_CHECKS.json`에 있다.
- 수신자가 실행한 제공 suite/F/COMSOL/JVM/compile/batch/loadCopy/Evaluate/Export/solve는 각각 0회. 실제 사용자 승인/token/runtime을 만들지 않았다. prefs/registry/ACL을 수정하거나 외부로 전송하지 않았다.

수신 측 33건은 현지 D01–D16/57개 재실행이 아니며 현지 횟수에 합산하지 않는다. AST 분리 함수의 결과를 전체 launcher 통합 실행이나 hostile-Python sandbox 검증으로 확대하지 않는다.

## 2. 수신 식별

| 자료 | bytes | payload + manifest | SHA-256 |
|---|---:|---:|---|
| 전달 wrapper | 1,158,533 | 6 + 1 | `5e8adb45bf474510cdddf46640c6429dce54b17d5beb146d496cfb95d59da2df` |
| 내부 OFFLINE_DEPLOYMENT ZIP | 1,261,072 | 400 + 1 | `99923f2342c5c3fc66b3d5d4a71317ca5e76c8bfb0e3a9a2a4328a3a81cb87a1` |
| 내부 EXTERNAL_FINALIZATION ZIP | 6,519 | 7 + 1 | `0332c2cd84ae8fdc13cf231862bf94b0eeda6cb66055fc98055aab221976ad20` |

세 자료 모두 manifest 정확 집합·각 바이트 크기/SHA·CRC 검사 통과. 중복·대소문자/정규화 충돌·경로 이탈·링크 타입을 검사했다. 외부 wrapper의 raw SHA는 수신 측 새 측정값이다. 사전에 별도로 받은 발신 raw SHA와 대조했다고 쓰지 않는다. 두 내부 ZIP은 최종 반환 전사에 기재된 식별과 일치한다.

최종 CODE_MANIFEST는 4,074 bytes / SHA `fa5592734f4d082bfc7bcb7ceaf70ec1407cd35342dadee100bf939f8297329b`, 파일 24개다. 모든 행이 실제 수신 바이트 및 시험 전 seal 행과 일치한다. `PRE_TEST_SEAL.json`과 `PRE_TEST_SEAL_run01.json`은 바이트 동일하며 SHA는 `8447c0ae0e61e05ea6f8b2eeec665bcb616b8a89702a421e8aad85cdfae9d4d9`다.

## 3. 허용 변경과 계약 결속

이전 수신 A8과 비교해 다음을 직접 확인했다.

1. launcher/winjob/execution_records/class_artifacts/status_reader/evidence_metrics/analyzer/numerical_contract/expected_solver/completion_contract/offline_clock_contract **11개 파일 바이트 동일**.
2. Java는 RUN/OUT literal 두 곳만 변경. 역치환한 전체 원문이 A8 Java와 바이트 동일하다. 수치/API 본문을 변경하지 않았다.
3. path_binding.py는 `TARGET_SHA` 상수만 변경. 새 VALIDATION_TARGET의 실제 SHA와 일치한다. 예상 argv 생성 알고리즘은 동일하다.
4. 새 run은 `saved_solution_A8R1_b006`, RUN은 `api_recovery_B_A8R1/runtime/b006`, 실제 사용자 승인 예정 경로는 RUN 밖 `approvals/saved_solution_A8R1_b006.json`이다. source·RUN·OUT·네 phase argv/cwd·authorization/token 경로가 독립 target의 도출값과 맞는다.
5. 새 기본 prefs 시작 식별은 계획에서 제안된 22,252 bytes / SHA `064d190077d7533f9fff22b61460d377cb53fb314e5c0f32a0bd02e3fa28b651`다. 계약 내 16개 security 값은 이전과 같다. 이는 계약/기록 대조이지 현지 현재 prefs를 직접 읽은 증명이 아니다.

Java SHA: `5a9da0f9da79a6d5f848af5ee3ea9792b06918110a8fae8a54b5a4fc05db6c39`.
raw contract SHA: `45a63bf1a33039c6556f024e26592d01e4ec4db1594dd7ef28713354cdc49043`.
독립 target SHA: `c3bc95bdeec31b183f67723ab65dc5047db23f4fa898754ab6d9587fa4e742d3`.

## 4. C1 — 새 단계의 정확 결과 집합 소비: 수용

`deployment_verify.py:123`의 report_errors가 D01–D16의 정확 집합·중복·하위 정확 집합·PASS·invocations의 int/1·outcome·phase·reason·관측 코드·전체 횟수·실패/오류 0을 검사한다. `:175`의 consume_deployment는 이 결과와 공통 report/completion/external 검사를 합친다. `deployment_package.py`의 package 진입이 이 소비자를 사용하므로 보고서 PASS만 보고 봉인하지 않는다.

수신 자료는 **16개 ID, 하위57개(온전 대조16/기대 거부41)**다. 각 ID의 실제 저장 파일과 합본이 일치한다. ID별 하위 수는 `1,2,2,2,3,2,2,2,3,5,8,11,2,4,4,4`로 총57이다.

D12는 빈 결과·누락·중복·미등록 ID·FAIL·SKIP·양성 대조 누락·잘못된 이유/단계·코드 불일치와 온전 대조를 다룬다. 테스트는 일반 예외를 성공으로 간주하지 않고 `VerificationError`의 이유/도달 단계를 비교한다. 특정 기대 코드를 여러 오류 중 고르는 helper도 그 코드가 실제 오류 목록에 존재할 때만 선택한다.

수신자 독립 확인에서 실제 57개 보고서/완료 묶음은 PASS였고, 위 집합/상태 변이와 bool 횟수·전체 수 불일치·관측 이유 누락·숨은 failure는 거부됐다. 이는 순수 소비 경로 검증이며 57개 제공 suite 재실행이 아니다.

## 5. C3 — raw 계약/view/최종 봉인: 수용

`deployment_verify.py:63`은 원문 SHA를 먼저 비교하고 raw 계약의 `approved is False`, `B_path_ready is True`를 요구한다. 복사본의 그 한 플래그만 false로 바꾸며 타입을 포함한 전체 재귀 비교를 사용한다. 최종 반환 SHA는 재직렬화 view가 아니라 **입력 raw bytes의 SHA**다.

이번 최종 raw 계약은 시험 전 seal부터 이미 `approved=false / B_path_ready=true / usable=false`다. 최종 CODE_MANIFEST의 24개 행은 당시 seal과 모두 동일하다. 시험 후 준비 플래그를 바꿔 다른 계약을 봉인한 증거는 없다.

D10은 다른 필드 은폐·bool/int 혼동·approved=true·raw 공백 변경을 다룬다. D11은 실제 `launcher.verify_approval`을 fixture와 연결하고, 승인 부재/false/다른 run/다른 manifest/계약·의존 파일 변경/필수 승인 항목 부재가 inert 후속 sentinel 이전에 거부되는 구조다. 이 구조를 정적으로 확인하고 저장 결과를 대조했다. 수신자 측에서는 launcher를 실행하지 않았다.

수신 독립 함수 확인에서도 허용 view만 수용했고, 양쪽 argv를 같은 잘못된 compile/prefs/class 값으로 바꾼 경우와 Java 비경로 변경은 거부됐다. `B_path_ready=true`는 준비 상태이지 실행 허가가 아니다. contract.approved/usable 문서 플래그 자체가 launcher의 모든 실행을 차단한다는 주장도 하지 않는다. 실제 실행권은 별도 승인 파일·manifest·run·예산·명시 항목 검증에 달려 있다.

## 6. 완료 증거·원점·최종 반환: 범위 내 수용

봉인된 START_AND_RESOURCES와 각각의 reservation을 실제 바이트로 읽어 context를 재구성했다. 보고/완료/외부 관측의 참조 SHA와 시각을 대조했다. 현지 suite 반환 전사는 chunk `e9e84e`, rc0, 8.172/300초이며 누적1,140.781/7,200초다.

마지막 finalizer 반환 전사는 chunk `de1ab7`, **바깥 도구 exit_code=0**, 호출 wall time1.3463208초다. output과 별도 stdout은 마지막 CRLF까지 UTF-8 바이트 동일하다. 출력의 `actual_host_rc=MUST_BE_OBSERVED_SEPARATELY`를 rc0으로 오독하지 않고 바깥 메타데이터와 구분했다.

- 전체 시작 `678247812000000 ns`.
- 전달 예약 `679922062000000 ns`.
- 저장 FINAL_OBSERVATION `679945531000000 ns`.
- 재읽기 뒤 FINALIZER_RESULT `679945546000000 ns`.
- 외부 ZIP 검증 뒤 마지막 출력 snapshot `679945609000000 ns`.
- 독립 차감: 전달 **23.547/600초**, 전체 **1,697.797/7,200초**. 시간 역전 없음.

실제 완료 묶음과 마지막 반환은 통과했고, 수신자 순수 함수 확인에서 외부 rc 실패/누락·가짜 경과시간·601초 초과·역전은 거부됐다. 내부 AWAITING_EXTERNAL_FINALIZATION은 앞선 시점 상태로 보존하고, 외부 자료와 마지막 반환까지 합쳐 이번 전달 범위를 수용한다.

한계: 도구 반환은 전달자가 대화 객체를 후속 직렬화한 자료다. 수신자가 원격 OS를 직접 관측하거나 독립 인증한 로그가 아니다. 최종 snapshot은 출력 전 관측이며 응답 전달 이후까지의 시간 실측이 아니다. cooperative 예산을 모든 동기 I/O의 강제 중단 보장으로 바꾸지 않는다.

## 7. 보존 범위

224개 전/후 목록의 경로 집합·각 크기/SHA·same 값을 독립 대조했고 모두 정합적이다. 그중 앞선 수신 A8에서 확보한 **168개 보관 파일 바이트**를 해당 기록과 직접 비교해 일치했다.

이는 이전 수신 바이트와 이번 현지 보고 식별의 일치다. **현지 현재224개를 직접 원격 검사한 것이 아니며, 168개가 현재 현지에서도 그대로라는 별도 직접 증명이 아니다.** 나머지 자료·MPH·전체 prefs·역사 전체·프로세스 실행 부재를 직접 검증했다고 쓰지 않는다. 이번 ZIP에 MPH는 없다. 기존 실패/pending/원복 기록·생성 영수증은 수정하지 않았다.

## 8. 남은 C2 — 실제 B에는 아직 GO를 주지 않음

`launcher.py:118`의 isatty 검사는 `execute` 안의 apply Desktop 뒤 `:306` observe에서 호출된다. 따라서 이 코드가 **Desktop 시작 이전에** TTY 부재를 차단한다고 표현하면 틀리다. 이번 B 초안은 이를 정확하게 미완으로 남겼고 frozen launcher를 몰래 변경하지 않았다.

이것은 새로 발견한 결함이 아니라 직전 C2의 유지 사항이다. 제한 오프라인 배치 수용과 모순되지 않지만 B 시작 전에는 해결되어야 한다.

다음 최소 작업은 **예정된 실제 B 호출 경로의 현지 입력/TTY 사전확인 방법을 구체화하는 제한 검토**다. 이미 충분히 구체화됐다면 그 확인 1건만 별도 승인받는다. 확인에는 Python/호출 방식/계정/cwd/stdin과 Windows 콘솔 입력의 관계, 현지 사용자 응답, timeout·실패 시 Desktop을 시작하지 않는 경계가 필요하다. 다른 셸의 isatty=True나 새 창이 보인다는 사실로 대신하지 않는다. 출력 TTY만으로 `msvcrt.getwch()` 입력 가능을 증명하지 않는다.

선행 gate나 wrapper 변경이 필요하면 먼저 최소 diff와 오프라인 검사 범위를 제안한다. 현재 24개 봉인 파일을 임의 수정하거나 승인된 것처럼 B를 시작하지 않는다. 변경이 없고 실제 조건을 확인할 수 있다면 이미 닫힌 C1/C3·A8 suite를 반복할 필요는 없다.

## 9. 다음 승인 경계

1. 이번 제한 배치·전달 검토는 수용된 것으로 별도 수신 기록에 추가할 수 있다. 원래 ZIP/생성 영수증/계약은 소급 수정하지 않는다.
2. C2 실제 경로의 TTY/현지 입력 조건 확인을 별도로 준비·승인한다. 이 보고서는 확인 실행 승인서가 아니다.
3. 이후 고정 manifest/run/입력/새 예산/All files 범위/정리·원복 조건을 지정해 **실제 B 1건을 사용자에게 별도 요청**한다. 앱의 정식 명령 허용은 사용자 승인과 별개다. 제한 우회나 다른 실행 경로로 대체하지 않는다.
4. 승인된 B도 저장 해 후처리만이며 solve0이다. 정상 gate 종결은 회수 수치·보존·process 정리·정책 원복과 독립 검토 뒤 판단한다. 1198 발동·후보C·장기 운전·12시간 휴지·유한sigma·sweep은 계속 미승인이다.

현재 단계는 **오프라인 실행 후보의 독립 수용 완료 → 실제 입력 경로 확인 및 B 별도 승인 대기**다. 전지 모델 전체 수렴을 승인한 단계가 아니다.

## 재현 자료

검토자 스크립트는 `verify_received.py`(수신 ZIP/봉인/허용 diff)와 `review_checks.py`(순수 소비 함수33건 및 데이터 대조)다. `PACKAGE_VERIFICATION.json`, `INDEPENDENT_CHECKS.json`에 결과가 있다. 현지 BML PC 경로를 실행하지 않는다. Python 스크립트의 입력 경로는 이 수신 PC/검토 폴더를 기준으로 하며 타 PC에서는 임의로 실행하지 말고 경로와 범위를 먼저 확인할 것.

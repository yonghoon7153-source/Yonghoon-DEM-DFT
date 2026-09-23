# B_A8R1 제한 오프라인 배치 결과

2026-09-24. **D01–D16 / 하위57개가 첫 제한 suite에서 전부 PASS. 실제 B·COMSOL은 미승인이다.** 전달 완료는 별도 외부 최종화 ZIP과 마지막 도구 반환까지 함께 판정한다. 이 보고서 작성 시에는 그 마지막 반환이 아직 발생하지 않았다.

## 승인 범위와 실제 수행

사용자의 후속 진행 요청과 조건 반영 승인 문안에 따라 새 `api_recovery_B_A8R1`만 만들었다. 이전 A7/A8/계획 폴더는 덮어쓰지 않았다. Java RUN/OUT 두 literal과 path_binding TARGET_SHA 상수, 새 계약/target/binding/세 배치 도구/검증·문서만 허용 범위 안에서 준비했다.

실제 RUN/approvals/token은 생성하지 않았다. sf/deploy_01의 fake_approval.json은 **합성 시험 입력**이다. 실제 사용자의 B 승인으로 읽지 않는다. COMSOL/JVM/native compile/batch/loadCopy/Evaluate/Export/solve·실제 F/process/Job/UI·prefs/registry/ACL 변경은0회다. Python 문서·배치/합성 검사 프로세스와 허용된 자기 메모리/RAM/디스크 조회는 실행했다.

## 고정 식별

| 대상 | SHA-256 |
|---|---|
| 최종 후보 raw 계약 | `45a63bf1a33039c6556f024e26592d01e4ec4db1594dd7ef28713354cdc49043` |
| Java | `5a9da0f9da79a6d5f848af5ee3ea9792b06918110a8fae8a54b5a4fc05db6c39` |
| 독립 target | `c3bc95bdeec31b183f67723ab65dc5047db23f4fa898754ab6d9587fa4e742d3` |
| CODE_MANIFEST (24개 파일) | `fa5592734f4d082bfc7bcb7ceaf70ec1407cd35342dadee100bf939f8297329b` |
| 시험 전 seal run01 | `8447c0ae0e61e05ea6f8b2eeec665bcb616b8a89702a421e8aad85cdfae9d4d9` |
| CASE_SPEC (16 ID / 57 하위) | `0a2937ffb4791236766b85f6986558ce951705b03611208b6310576eb4765827` |

후보 raw 계약은 시험 **이전**부터 approved=false/B_path_ready=true/usable=false였다. 그 정확한 바이트를 seal과 최종 manifest가 함께 참조한다. 시험 뒤 계약 플래그나 코드를 바꾸지 않았다. raw SHA를 view 재직렬화 SHA로 대신하지 않는다.

11개 파일의 A8 원문 바이트 동일, Java 두 literal 역치환 전체 바이트 동일, path_binding TARGET_SHA 외 전체 바이트 동일, 수치 계약 유지가 정적 대조에 통과했다. 실제 새 target에서 D01 온전 대조도 통과했다. `SOURCE_DIFF.patch`, `SOURCE_COPY_IDENTITIES.json`, `STATIC_REPORT.json`을 참조한다.

## 세 조건의 실제 연결

- **C1:** 새 report_errors가 정확 ID/하위 집합·status·invocations 타입/개수·양성 대조·거부 이유/도달 단계/관측 코드·failures/errors를 확인한다. 이 결과와 기존 공통 completion/report/external 검사를 AND로 결합한다. D12의 해시가 일관된 온전·빈 집합·누락·중복·알 수 없는 ID·실패·skip·하위 양성 누락·이유/단계 오류·코드 불일치가 실제 소비 함수를 거쳤다.
- **C3:** make_view는 원래 raw SHA를 검사하고 typed deep comparison으로 B_path_ready 하나만 false인 view를 허용한다. D10에서 다른 필드/타입/approved=true/raw 바이트 변화가 지정 이유로 거부됐다. D11은 불변 launcher.verify_approval을 실제 호출하되 native 경계는 inert sentinel이다. 없음/false/다른 run·manifest/필수 승인 누락/계약·의존 파일 변이를 각각 거부했고 정상 대조만 sentinel에 도달했다. 실제 Runner/WindowsJobTransport는 실행하지 않았다.
- **C2:** TTY는 해결됐다고 쓰지 않는다. 현 launcher는 apply 실행 후 observe→timed_attest→isatty로 검사한다. 같은 실제 호출 경로에서 사용자가 입력할 TTY의 **사전 확인은 미완**이다. launcher/transport를 바꾸거나 실제 TTY/native를 시험하지 않았다. B 착수 전 별도 운영 근거가 필요하며 선행 코드 gate가 필요해지면 별도 변경 승인을 받아야 한다.

`contract.approved=false` 또는 문서 usable=false가 각각 launcher의 독립 차단장치인 것은 아니다. 실제 실행권은 별도 B 승인 파일의 approved/run/manifest/예산/필수 수용 필드 및 코드 식별 검사로 결속한다. 현재 그 실제 승인 파일은 없다.

## ID 및 하위 결과

| ID | 실제 하위 호출 | 결과 | 사례 |
|---|---:|---|---|
| D01 | 1 | PASS | valid_candidate |
| D02 | 2 | PASS | valid, both_old_compile |
| D03 | 2 | PASS | valid, both_default_prefs |
| D04 | 2 | PASS | valid, both_old_class |
| D05 | 3 | PASS | valid, both_wrong_source, both_wrong_paths |
| D06 | 2 | PASS | valid, wrong_compile_cwd |
| D07 | 2 | PASS | valid, approval_inside_run |
| D08 | 2 | PASS | valid, java_nonpath |
| D09 | 3 | PASS | valid, unit_changed, coordinate_changed |
| D10 | 5 | PASS | valid, other_field, type_change, approved_true, raw_bytes_changed |
| D11 | 8 | PASS | valid, absent, false, wrong_run, wrong_manifest, changed_contract, changed_dependency, missing_flag |
| D12 | 11 | PASS | valid, empty, missing, duplicate, unknown, failed, skip, missing_positive, wrong_reason, wrong_phase, code_mismatch |
| D13 | 2 | PASS | valid, post_report_overrun |
| D14 | 4 | PASS | valid, outer_rc1, outer_rc_missing, external_missing |
| D15 | 4 | PASS | valid, reserved601_claim40, claim_origin_mismatch, anchor_mismatch |
| D16 | 4 | PASS | valid, record_reverse, postwrite_reverse, record_identity |

일반 ID는16개이며 단일 assertion16개라고 표현하지 않는다. 총57개 하위 기능 호출 중 온전 대조16개, 기대 거부41개다. 이 수는 A8의389개/별도음성2개와 합산하지 않는다. 원본389 suite/기존 probe/F는 재실행하지 않았다. 모두 합성/오프라인 결과이며 native API·수치·정리/원복 성공의 증거가 아니다.

시험 전 native/process/DLL/network 방어를 설치했다. launcher의 승인 검사까지는 호출하고 native 진입은 inert로만 대조했다. guard 경계 위반 관측은 빈 목록이며 실제 native 호출 시험은 없다. 기능 결과와 각 이유/단계는 deployment_01.json, sf/deploy_01/Dxx_results.json에 보존했다.

## 횟수·자원·시간

- 제한 suite 1/최대2회 사용. 첫 완전 통과이므로 두 번째와 부분 probe는 실행하지 않는다.
- suite 마지막 내부 snapshot: 8.172/300초, 전체1140.781/7200초. 실제 도구 chunk e9e84e / exit_code0 / 도구 자체9.3102872초. Python 출력 직전 시간과 바깥 도구 소요시간을 구분한다.
- `deployment_evidence/HOST_SUITE_RUN01.json`은 반환된 전체 도구 객체를 후속 직렬화했다. 별도 원시 OS 감사나 독립 인증 영수증이 아니다. 이 값으로 만든 deployment_01.external.json을 실제 완료 소비에 넣어 PASS했다. 테스트 report PASS만 확인한 것이 아니다.
- 사전 구현 구간 1102.000/3600초, 정적 0.641/300초. 후속 문서/검토 준비 시간은 별도 보수적 준비 예산 기록에 포함한다. 제한 suite 누적은1회이며 더 실행하지 않는다.
- 시작 RAM7,731,372,032 bytes / workspace 디스크171,085,258,752 bytes. 각 하위 사례 전 자기 working set/fixture 크기/생성 경로 제한을 확인했다. 끝 working set 25,059,328 bytes, fixture 4,721,949 bytes. 연속 peak 계측이나 OS 전체 메모리 상한 보장으로 확대하지 않는다.
- 선택 보존 파일224개 모두 전후 크기/SHA 동일. 보존 누적 17.938/180초. 원격 전체 파일/메모리/프로세스 불변 주장은 아니다. 보안값16개 및 기본 prefs raw SHA 조건은 착수 시 직접 대조했다. 실제 prefs는 복사/변경하지 않았다.

## 남은 B 조건

고정 실행본 독립 검토, 같은 실제 호출 경로의 TTY/현지 입력 확인, 실제 B 사용자 승인 및 해당 명령의 앱 허용이 필요하다. native API·실효 정책/loadCopy·수치 회수·Win32 정리·UI 원복은 미시험이다. 정확한 네 argv/cwd는 PLANNED_COMMANDS.json 및 봉인된 contract/binding에 있다.

B_path_ready=true는 경로 준비 후보/검증 범위다. B approved=false/usable=false를 유지한다. 기존 A7/A8 false 플래그·두 failed·b003 pending 및 별도 원복·MPH·ZIP·영수증 recipient=null·OCP 외삽 금지·TIME_CAPS 차이 미확인·정상 gate/API 복구/전체 수렴 미완·장시간 보류·1198/후보C 미승인을 유지한다.

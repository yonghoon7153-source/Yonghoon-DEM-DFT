# S1 OPEN-R1 N1–N3 오프라인 정정·정적 재봉인

2026-10-11. 승인된 최대 2,400초의 새 작업이다. 지정된 `microshort_s1_open_connection_r1_20261010` 폴더에서만 새 비활성 revision을 작성했다. 날짜가 지난 폴더명은 지시서의 고정 경로를 따른 것이다.

**N1/N2 연결 코드와 N3 검증안을 정정했다. 기능 검증은 NOT_RUN이며 native 실행 승인이 아니다.** 정적 검사와 갱신 검증안의 수·해시는 최종 DECISION, CODE_MANIFEST 및 STATIC_CHECKS를 기준으로 한다.

## 1. 정정과 근거

| 항목 | 전 | 후 | 위치 |
|---|---|---|---|
| N1 | 각 raw 샘플이 전체/native 원점을 제공하고 그 값으로 elapsed 계산 | 독립 start_record를 ResourceSession 생성 때 한 번 복사하고 frozen context·scalar anchor에 결속. 샘플의 run/clock/단위/원점 일치 검사 후 elapsed는 context에서만 계산 | resource_connection의 ExecutionClockContext, ResourceSession, bind_sample_clock, project_owned_sample; FUNCTION_SPANS의 정확 줄/바이트/SHA |
| N2 | counter 항목의 dict 여부를 확인하기 전에 p.get 호출 | dict → 필수 키 → PID/생성시각의 정확 정수 타입과 양수 확인 → 기존 membership/query/counter 검사 순서 | project_owned_sample의 PROCESS_COUNTER_SCHEMA/KEYS/IDENTITY_TYPE |
| N3 | 다른 분기의 양성, 도달할 수 없는 assessor, Java 예외 경로 불명확 | 같은 분기 양성, 정확 반환 필드, 필수·금지 함수/호출 수, 실제 의존부·예외 위치로 연결 | LIMITED_VALIDATION_PLAN 및 VALIDATION_PROPOSAL |

최소 diff는 `candidate/resource_connection.py.inactive.txt.diff.txt`다. 이전 제출의 전체 추가 diff와 구분해 이번에는 이전 준비본→OPEN-R1의 unified diff로 남긴다. `finite_time`의 OverflowError만 False로 거부하는 보완은 새 clock 형식 검사에서 표현 불가능한 거대 정수가 구조화된 clock 오류로 연결되도록 한 것이다. 새 시간 한도·자원 threshold를 만들지 않는다.

ResourceSession의 `decide`에는 context/start_record/anchors를 교체하는 인수가 없다. caller의 원본 dict 변경은 복사한 immutable 값에 영향을 주지 않는다. 원점을 샘플로부터 만들거나 누락값을 0으로 채우지 않는다. 다만 이전 샘플 종료시각 인수는 기존처럼 호출자가 공급한다. 실제 OS clock 취득·독립 원점의 출처·동일 session 유지의 운영 증거는 아직 OPEN이다. 이번 변경은 OS 수집기나 새 감시기 구현이 아니다.

`ResourceSession` 생성 자체의 누락/잘못된 start_record는 명시적인 ResourceConnectionError로 초기화가 거부된다. 정상 결속 이후의 샘플 오류는 기존 resource_decision의 typed catch가 STOP_REQUIRED로 반환하며 assessor를 호출하지 않는다. 생성 거부와 샘플 반환의 위치를 검증안에서 구분한다.

## 2. 유지한 것

원 준비본 11개 봉인 구성원 중 resource_connection·그 diff·검증안만 이번 revision에서 달라진다. 새 문서/계약/봉인 근거는 별도 추가물이다. raw_connection, Java fragment/P0, OPEN 지도, OS API 표, native 비활성 상태는 바이트 동일하다. 원 R1 21개·manifest, consumer/control/Parent, 물리/허용치/RESOURCE_CONTRACT의 예산·reserve를 수정하지 않았다. 원 준비본 74개 정적 기록도 `basis/prior_preparation`에 그대로 보존했다.

원본 선택 식별은 BEFORE/AFTER_STATIC/AFTER_PACKAGE와 최종 대조에서 연결한다. 항목 수와 고유 경로 수는 별개다. 받은 검토 ZIP은 1,953,422 bytes / f23d02b01b7a2ae96a2cfcf17009d73a2c47cddae7895c124aea6543b15bdd15, 원 준비본 ZIP은 1,929,576 bytes / 32cbb6ee5b8885a645da762154dab38d8f67ef4c7f97b5b4bc9c2ecd5fdd6f5c다. 원 archive·state·failed/pending·영수증 recipient=null을 수정하지 않는다.

## 3. 이번에 수행한 확인과 한계

사용자가 허용한 자체 데이터 도구로 ZIP 집합/크기/SHA/CRC/경로, Python AST 구문, byte/text diff, 원본 hash, 함수·예외 span을 확인했다. Python 호출은 이 자체 정적 도구에 사용했으며, 후보/받은 코드의 import·함수 호출·시험 실행은 0회다. Java compile/JVM/COMSOL·OS 수집기·process/Job 실험·실제 입력 gate·정책 변경은 0회다.

독립 읽기 전용 검토에서도 N1/N2의 위 제어 흐름에 추가 결함을 찾지 못했다. 이는 동적 기능 PASS가 아니다. 다음 검증은 별도 사용자 승인 뒤 새 harness/fixture/엔진/명령을 봉인해야 한다. 130개 원 R1 기능 시험을 재개하지 않는다.

자체 bootstrap의 첫 호출은 Desktop 원준비 ZIP 사본을 잘못 선택해 FileNotFoundError로 끝났다(chunk 8b5773). 당시 새 폴더 생성 전이었고 후보 코드 실행은 없었다. 지시서에 이미 지정된 원준비 폴더의 같은 크기/SHA 보존본을 사용해 자료 확인을 계속했다. 원문 오류와 처리 범위는 TOOL_OBSERVATIONS에 보존한다. 이를 후보 기능 실패나 무오류 작업으로 바꾸어 기록하지 않는다.

## 4. 시간·전달 경계

새 UTC·현지 시각·monotonic 원점은 ORIGIN에 있다. 정정 작성 후 정적 대조와 독립 파일의 검증안 작성은 병행하며, 각 단계의 wall time 상한을 별도로 적용한다. 전체는 단일 원점 경과이고 중첩 구간을 합산하지 않는다. 미사용분 전용은 없다. 단계별 시작/종료·한도는 PHASE_RECORDS, 마지막 기록·재읽기 뒤 snapshot은 ZIP 밖 FINAL_SUBMISSION_CHECK/FINAL_CHECK_TOOL_RETURN에 구분한다.

포장 반환과 최종 확인 반환은 실제 도구 출력의 후속 전사이며 원시 OS 감사가 아니다. 도구 wall time을 snapshot에 더하지 않는다. 자기 자신을 포함하는 마지막 반환을 재귀적으로 파일화하지 않으며, 마지막 전사 저장 이후 경계는 마지막 대화의 실제 도구 반환으로만 구분한다.

## 5. 제출 후 정지

네 OPEN(installed t0, effective coefficient mapping, raw native evidence adapter, OS resource/ownership/stop adapters), native_ready/approved/usable=false, native argv/cwd/approval paths=null을 유지한다. 전체/정상 gate INCOMPLETE, 실효 정책/실제 코어 UNVERIFIED다. P0와 설치본 관측·새 검증은 각각 별도 승인 대상이다. 강제 종료 계획은 실제 종료 관측이 아니며, microshort 효과·K·장시간 cohort 결과를 주장하지 않는다.

## 최종 위치와 검증안 식별

- resource_connection.ExecutionClockContext: candidate/resource_connection.py.inactive.txt:31–52
- resource_connection.ResourceSession: candidate/resource_connection.py.inactive.txt:55–82
- resource_connection.bind_sample_clock: candidate/resource_connection.py.inactive.txt:85–97
- resource_connection.project_owned_sample: candidate/resource_connection.py.inactive.txt:100–174
- resource_connection.resource_decision: candidate/resource_connection.py.inactive.txt:177–184

새 CODE_MANIFEST SHA: `feb12ef6991141aab59fd2fbc0d5f0d138bdd735255aa7123274503ce80b8ecc` (14구성원). 갱신 검증안은 9군 93사례(Python 87 / Java helper 6), 모두 NOT_RUN이다. 이후 검증 예산 제안은 원 1,350초를 유지하며 실제 수행시간 보증이 아니다. 이번 정정 승인 2,400초와 별개다.

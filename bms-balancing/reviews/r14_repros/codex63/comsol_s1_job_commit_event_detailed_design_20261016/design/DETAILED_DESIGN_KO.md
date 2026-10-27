# Job commit event 보호 조건부 방향 선택과 세부 설계

2026-10-16 · COMSOL S1 · 계약 채택 전 문서 초안

## 선택된 방향과 유지되는 경계

사용자는 “1번가자”로 **관리 사건과 유한 관측 구간을 대상으로 하는 조건부 설계 방향**을 선택했습니다. 현재값·최대값 미측정, 시작 공백, 알림 지연·미수신 불확실성을 남긴 채 세부 설계를 진행한다는 선택입니다. 선택 원문과 바로 앞 질문의 범위는 [선택 기록](USER_DIRECTION_SELECTION.json)에 연결했습니다.

이번에 달라진 상태는 ‘방향 선택 대기’에서 ‘1번 방향으로 문서 설계 진행’까지입니다. 실제 실행에 이 위험을 허용한다는 운영 위험 수용, 정확한 계약 채택, 구현·fixture·시험·OS 관측·COMSOL 실행 승인은 아닙니다. reader/query/final 기한은 계속 null입니다.

세부안의 핵심은 세 가지입니다. 호출 전에 관리 예약을 남겨 cutoff 경쟁을 구분하고, 막힌 조회의 초과 판정과 실제 정리를 분리하며, 잠정 출력 뒤의 오류를 별도 근거로 Parent가 확인하도록 합니다. 아래 상태·필드·순서는 **새 계약에 넣기 전 검토할 논리 명세**이며 R8 코드에 적용된 동작이 아닙니다.

## 책임과 진행 상태

| 논리 역할 | 책임 | 의존하면 안 되는 경로 |
|---|---|---|
| 책임 launcher/supervisor | 실행·시계·소유권·설정 결속, 시작 조건 재확인, 일회성 resume 자격 소비, 소유 대상 중지 | 중지 결정을 내리기 위해 막힌 query의 반환을 기다리는 경로 |
| 단일 reader/query 담당자 | 지정 port 수신과 class 13 조회, 호출 예약·handle 사용권, 원관측과 분류 게시 | notification을 query 종료 때까지 숨기는 경로 |
| 독립 감시자 | 등록된 시작점·진행·기한을 관측하고 초과·중지 차단 상태 게시 | 대상 흐름이 점유한 잠금이나 배출되지 않는 정상 업무 큐 |
| 판정 상태 관리자 | 관측 순서, 예약과 pending, 지속 latch, 상태 버전, 허가 폐기·소비 직렬화 | 상태 잠금을 잡은 채 API·파일 I/O·종료 대기를 하는 경로 |
| Parent 검증자 | 외부 기대 계약·권한과 완료된 증거를 대조해 최종 다중축 판정 | 출력 파일 안의 자기 승인 선언이나 요약 PASS만 신뢰하는 경로 |

역할 이름은 실제 프로세스나 스레드 수를 정하지 않습니다. 실제 담당 신원, 호출 경로와 동기화 수단은 후속 결정입니다. 독립 감시자가 같은 completion port를 추가로 읽거나 class 13 조회를 따로 수행하는 구조는 포함하지 않습니다.

공유 상태는 다음을 구분합니다.

- **불변 결속**: run/clock/원점/계약·모드 revision, 소유 Job와 held root, port/key generation, reader/supervisor/감시자 generation.
- **서로 다른 순서 값**: reader 진행, packet 수신, 분류 반영, supervisor 관측·직렬화, 상태 version. resource cursor는 별도입니다.
- **진행 중 작업**: receive 예약, query 예약, pending packet, 반환했지만 아직 게시하지 않은 결과, handle별 사용권.
- **지속 상태**: violation/stop/error/expiry latch 및 supervisor의 dispatch 금지 상태. 후속 성공으로 해제하지 않습니다.

판정 상태와 독립 감시자의 차단 상태가 모두 일관되고 유효해야 새 작업을 허용합니다. 필요한 상태를 읽지 못하거나 게시가 실패하면 정상 허용으로 간주하지 않습니다. 이 차단의 가시성이 실제로 query 잠금과 독립적이라는 구현 근거는 아직 필요합니다.

## 시작과 resume 사이의 경계

실제 책임 caller가 실행·시계·소유 Job/root·설정/readback을 결속한 뒤 감시자를 등록하고 reader 준비를 확인합니다. 그 다음 **새 event 모드용 다른 자원의 최초 표본과 판정**을 확보하고, resume 자격 발급·소비 직전에 조건을 직렬화해 다시 확인합니다.

재확인 조건에는 정확한 미래 계약과 운영 위험 채택·해당 실행 권한, 설치 지원과 보호 효력, 소유권·reader/감시 결속, 유효한 최초 다른 자원 판정, 알려진 pending/query/미게시 분류 없음, 지속 위반·중지·오류·초과 없음, 유효한 수치 기한과 남은 상위예산, 같은 실행의 미소비 자격이 모두 포함됩니다. 현재는 여러 조건이 미완이므로 resume 자격을 만들 수 없습니다.

이 자격은 미래 구현의 일회성 **메모리 상태**에 대한 설명입니다. 이번에 승인 파일이나 토큰을 생성하지 않습니다. 발급 뒤 소비 전에 사건·오류·신원 변경이 반영되면 폐기하며, 소비 직전에도 재확인합니다.

이 직렬화는 OS 사건의 발생과 실제 resume API 호출을 원자적으로 묶는다는 뜻이 아닙니다. 자격 소비 뒤 실제 호출 직전·중간에도 사건이 관측될 수 있습니다. 아직 취소할 수 있는 자격은 폐기하고, 호출 진입 이후라면 지속 중지 상태와 독립된 소유 대상 중지 경로로 연결해야 합니다. “알려진 pending=0”은 “resume까지 위반 없음”이 아닙니다.

R8의 pre_resume_check는 fake receipt만 확인합니다. 기존 순서는 sample_once가 collect_owned_sample의 raw를 받은 뒤 ResourceSession.decide를 호출하고, 성공 판정 뒤에 cursor와 _sample_ok를 갱신하는 것입니다. 기존 수집은 current commit을 필수로 요구하므로 새 다른 자원 전용 경로로 전용할 수 없습니다. current를 0/null로 대체하거나 _sample_ok를 강제로 설정하지 않습니다. 새 projection·assessor·control 연결은 별도 설계 대상입니다. [보존한 후보](basis/os_provider.py.inactive.txt), [Provider 계약](basis/PROVIDER_CONTRACT.json)

### 시작 공백의 구체 조건

공식 문서는 notification-limit 메시지의 전달 보장을 설명하는 한편, NOTIFICATION_LIMIT 항목에는 해당 프로세스의 PID가 아직 보고되지 않았다면 메시지를 보내지 않는 조건을 명시합니다. 따라서 전달 보장 일반 문구만으로 초기 공백을 지울 수 없습니다. [Microsoft Job completion port 문서](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port)

프로세스 존재·membership·held identity는 최초 표본의 별도 근거로 확인해야 합니다. PID 메시지 부재를 프로세스 부재로 해석하지 않으며, 필요한 소유권·표본 범위를 확인하지 못하면 시작 조건은 불충족입니다. 반대로 그 표본이나 NEW_PROCESS 수신을 확보해도 초기 current baseline이나 모든 미전달 과거 사건을 확인한 것은 아닙니다. 이 구간은 선택한 유한 관측 방향의 잔여 불확실성으로 남습니다.

## 호출 예약과 독립 감시

receive 호출 직전에 상태 관리자에게 호출 예약을 등록합니다. 대기에서 반환한 timeout·오류·packet을 상태에 게시할 때까지 예약을 유지합니다. packet을 받았으면 수신 순서와 관측 시각, pending 분류 상태를 query 진입 전에 게시합니다. query는 별도 예약과 해당 handle 사용권을 먼저 등록하며 반환 결과를 검증·게시한 뒤에만 해제합니다.

query 기산점은 notification dequeue/관측 시각입니다. 이후 잠금·큐·API 진입 전 대기·동기 호출·검증·분류 게시까지 포함합니다. API 진입 시각은 추가 관측값이지 새 원점이 아닙니다. dequeue 이전의 OS 전달 지연은 여기에 포함되지 않습니다.

dequeue 직후 게시 전에 reader가 멈추는 틈도 고려해야 합니다. 이때 receive 예약이 남아 있으므로 cutoff를 확정할 수 없습니다. 독립 감시자는 진행 중단을 차단 사유로 기록하되 아직 게시되지 않은 packet 종류·정확한 query 시각을 만들어내지 않습니다. 정상 실행 중에는 아직 packet을 관측하지 않은 receive 대기 하나가 있다는 이유만으로 pending notification으로 세지는 않습니다. 그 대기가 무위반의 증거도 아닙니다.

짧은 상태 전이 구간 안에서는 blocking query, 대기 호출, resume, writer/readback 또는 종료 확인을 하지 않습니다. 정상 큐가 가득 차도 감시자의 초과 게시와 supervisor의 dispatch 차단이 그 큐의 배출에 의존하면 안 됩니다. 실제로 이를 만족하는 원자성·메모리 가시성·실패 처리를 선택하고 검증하기 전에는 독립 감시가 완성된 것이 아닙니다.

GetQueuedCompletionStatus의 FALSE+null OVERLAPPED는 packet을 꺼내지 못한 경우이며 key/byte 출력은 미정입니다. 이 값을 실제 packet 신원으로 읽지 않는 분기 설계가 필요합니다. 또한 해당 함수의 유한 timeout은 query나 전체 final의 상한이 아닙니다. [Microsoft 대기 호출 문서](https://learn.microsoft.com/en-us/windows/win32/api/ioapiset/nf-ioapiset-getqueuedcompletionstatus)

## 정상 종료와 cutoff 확정

정상 경로의 제안 순서는 아래와 같습니다. 어느 단계에서든 위반·오류가 관측되면 정상 진행을 닫고 실패 보존·소유 대상 중지 경로로 분기합니다.

| 단계 | 수행할 일 | 완료 근거 |
|---|---|---|
| F0 | 최초 final 기산점 고정, 새 owned 작업 유입 차단 | 유입 차단의 결속 기록과 불변 시작점 |
| F1 | reader를 유지하면서 소유 Job/root 종료 확인 | 최종 membership, held-root signal, exit 결과와 소유권 |
| F2 | 관리 사건을 분류하고 정상 조건에서만 잠정 writer 시작 | 지속 상태, 관리 원장과 writer 시작 version |
| F3 | readback 직전 재확인 후 잠정 파일 재읽기 | 저장 바이트·해시·원장 head. reader는 계속 수신 |
| F4 | 새 receive 예약의 입장을 닫는 요청 | 요청의 상태 version과 관측 순서 |
| F5 | 이미 예약된 receive 결과와 필요한 query를 모두 반영 | 아래 cutoff 조건을 만족하는 직렬화 경계 |
| F6 | reader 실제 종료 확인 후 의존 handle 정리 | 사용권 없음, reader exit, handle별 결과 |
| F7 | 잠정 파일과 후기 관측을 묶은 별도 closure 근거 완성 | P의 정확 해시, 최종 원장과 각 판정 축 |
| F8 | Parent가 완료된 근거와 최신 상태를 대조 | 독립 검증 경계·전체 차단 사유·다중축 판정 |

F4는 **새 receive 예약만 금지**합니다. 이미 예약된 receive가 나중에 돌려준 packet은 요청 이후 반환했어도 원장에 기록하고 필요한 query를 처리해야 합니다. cutoff를 서두르기 위해 그 packet이나 오류를 버리지 않습니다.

F5에서 다음 조건을 하나의 일관된 상태 경계로 확인해야 합니다.

1. receive 예약, query 예약, pending packet, 반환 후 미게시 결과가 모두 0입니다.
2. reader가 새 receive를 시작하지 않는 상태를 확인했습니다.
3. 마지막 반영 sequence와 상태 version이 같은 경계에 결속됩니다.

cutoff 확정과 reader 실제 종료는 별도 사실입니다. cutoff 이후 새 receive 진입은 프로토콜 오류이며 정상 수용을 막습니다. 임의 sentinel, queue empty, Job empty, child rc0는 위 조건이나 모든 과거 OS 사건의 처리 완료를 대신하지 않습니다. 이미 OS 큐에 있거나 아직 도착하지 않은 미수신 사건은 선택 범위 밖의 불확실성으로 남습니다.

## 막힌 query와 실패 이후의 정리

감시자가 query 기한 초과를 관측하면 UNRESOLVED_NOTIFICATION과 STOP_REQUIRED, dispatch 차단을 지속 기록합니다. 이것은 query의 취소·반환·종료를 관측한 것이 아닙니다. 공개 QueryInformationJobObject 설명의 성공·실패 반환 규칙을 호출 시간 상한으로 확대하지 않으며, 이 설계는 자동 취소 보장에 기대지 않습니다. [Microsoft Job 조회 문서](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-queryinformationjobobject)

미반환 query의 예약과 handle 사용권은 유지합니다. 사용 중인 handle을 닫거나 thread를 강제 종료하여 정리 완료를 만들지 않습니다. 별도로 승인·검증된 소유 대상 중지 경로가 query와 독립적으로 동작할 수 있을 때에만 그 요청과 실제 종료를 각각 기록합니다. 소유권이 불명인 대상을 임의로 종료하지 않습니다.

query가 돌아오지 않아 예약·사용권이 남으면 cutoff 확정과 안전한 handle 정리는 미완입니다. query가 반환했더라도 검증·게시가 입증되지 않으면 해당 예약과 cutoff를 해소하지 않습니다. 반면 검증·게시와 cutoff 조건은 충족했지만 handle 사용권 해제 근거만 미완인 경우에는, 이미 확인된 cutoff 사실까지 취소하지 않고 cleanup을 미완으로 남깁니다. 어느 경우든 coverage는 FINAL_COVERAGE_INCOMPLETE이고 정상 수용은 거부합니다.

reader의 실제 종료와 소유 native 프로세스의 종료는 각각의 관측 축대로 보존합니다. 독립적으로 확인된 종료 사실을 query/cleanup 미완 때문에 UNRESOLVED로 덮지 않으며, 반대로 종료 관측만으로 query 반환·게시·handle 사용권 해제를 추정하지 않습니다. **정상 수용을 유한 기한 안에 거부할 수 있다는 설계와 미반환 호출의 물리적 제거를 보장하는 설계는 다릅니다.** 후자는 아직 미완입니다.

query가 늦게 성공해도 과거 초과와 첫 오류는 유지합니다. 자동 재조회·대체 엔진·reader 재시작으로 정상 상태를 복원하지 않습니다. 별도 query worker 프로세스 격리는 향후 검토할 수 있는 대안일 뿐, 이번에 프로세스·자원·권한 범위를 추가 채택하지 않았습니다.

최초 오류 이후 새 정상 final writer/readback/clock 호출을 시작하지 않는 원칙을 유지합니다. 위반·중지 latch도 새 정상 출력을 막습니다. 이미 진행 중인 호출의 성공 반환은 정상 결과로 수용하지 않습니다. 독립 감시·소유 대상 정리·실패 근거 저장은 별도 경로이고, 실패 기록 저장마저 실패했다면 보존 불완전으로 남겨야 합니다.

## 잠정 출력과 Parent 증거의 비순환 연결

미래 증거는 세 객체로 나눕니다. 아래 이름은 필드 설명이며 지금 실제 runtime 기록을 생성한 것이 아닙니다.

- **P 불변 잠정 파일**: 실행 신원, 잠정 결과와 저장 시작 전에 확정한 상태 version·원장 head·관측 시각만 본문에 담습니다. P 자신의 저장 완료·재읽기 성공·최종 해시·writer 종료 시각은 P 본문에 넣지 않으며, 최종 수용을 선언하지 않습니다.
- **C 종료 관측 근거**: P의 저장·재읽기가 끝난 뒤 작성하는 별도 객체입니다. P의 외부 id/정확한 저장 길이·해시, 별도 write/readback 완료 기록과 그 시각·원장 head, writer 이후 사건과 오류, cutoff/마지막 반영 sequence, reader 종료, handle 정리, 지속 상태와 기한·보존 결과를 연결합니다. P를 덮어쓰거나 자기 자신의 미래 저장 성공을 주장하지 않습니다.
- **R Parent 판정 기록**: Parent가 실제 읽고 검증한 P/C의 id·해시와 원장 head, 외부 기대 계약·권한, Parent가 추가 관측한 원인, 판단 직전 상태 version·latch 및 모든 축의 결과를 연결합니다.

증거 참조에는 object id, 종류, run, schema revision, producer/generation, 저장 길이와 SHA-256이 필요합니다. P의 저장 전 원장 head에는 P의 사후 저장·재읽기 기록이 없으며, 그 사후 기록과 C가 이미 완료된 P 바이트만 참조합니다. 원장은 각 저장 레코드가 직전 레코드의 정확한 바이트 해시를 참조하도록 제안합니다. 자신의 전체 해시는 자기 본문에 넣지 않고 외부 인덱스나 다음 참조에서 계산하여 순환을 피합니다. genesis는 외부에서 기대한 실행 시작 근거에 결속합니다.

순서 누락·분기·재정렬·같은 id의 바이트 변경은 거부합니다. 해시는 바이트 결속을 위한 것이지 사건의 진실성, OS 전달 완전성, 저장 내구성의 독립 증명이 아닙니다. supervisor 원장과 Parent 원장을 실제 source 발생 순서 하나로 합치지 않습니다.

R을 만들기 직전에 최신 상태 version·latch와 Parent가 관측한 오류를 재확인해야 합니다. 검증한 snapshot 뒤 관련 변경을 알았다면 그 snapshot으로 수용하지 않습니다. 재확인도 원래 final/상위기한 안에 있어야 하며 자동 reseal이나 새 예산을 만들지 않습니다. R의 저장·전달 성공은 R 내부 자기 선언이 아니라 완료된 산출물을 소비하는 쪽의 확인으로 구분합니다. 그 확인이 실패하면 미수용·보존 불완전입니다.

### Parent가 반드시 분리할 축

신원·mode/revision·계약·권한의 외부 기대값을 먼저 검사합니다. 그런 다음 event 위반, 알림 미해결과 감시, current/maximum 미측정, cap, 다른 자원, native 종료, cleanup, coverage, 시계·예산, 기록·보존을 각각 판정합니다. 구체 필드는 [Parent 필드 초안](PARENT_EVIDENCE_FIELDS.json)에 있습니다.

모르는 schema/enum, 중복 키, 잘못된 정확 타입, 필수 필드 누락, 다른 실행의 증거는 정상 수용을 막습니다. 필수 축의 UNKNOWN을 optional로 내려 통과시키지 않습니다. 비어 있는 오류 배열도 연결된 원장 경계까지의 기록과 대조해야 합니다.

first_observed_error와 first_stop_cause는 분리합니다. 확정 위반이 오류보다 먼저 중지를 요구할 수 있습니다. 최초 참조는 supervisor의 관측·직렬화 순서로 고정하고 source 시각이나 후속 성공으로 바꾸지 않습니다. 단일 대표 사유는 선택적 표시이며 모든 차단 사유를 대신하지 않습니다.

세 기한 중 하나라도 null/미채택이거나 위반·stop/error/expiry·미해결·필수 축 결함이 있으면 정상 수용을 거부합니다. rc0, cap 설정, cleanup 성공으로 다른 축을 지우지 않습니다. 강제 종료도 정상 계산 완료로 바꾸지 않습니다. 미래 모든 요건을 충족하더라도 결과의 의미는 선택된 유한 관측 범위의 의무 충족이며 current 측정 PASS가 아닙니다.

## 세 기한과 시계 처리

| 기한 | 현재 값 | 불변 기산점과 완료 범위 |
|---|---|---|
| reader 진행 | null | 초기에는 감시 등록/reader 시작 요청 중 먼저 결속된 시각부터 준비 완료까지. 이후에는 검증된 처리 단계 완료부터 다음 유한 대기·처리 완료까지 |
| query 완료 | null | notification dequeue/관측부터 분류 결과 게시까지. 이전 OS 전달 지연은 제외 |
| final 동기화 | null | 최초 유입 차단 진입부터 종료·관리 사건·잠정 I/O·cutoff·reader 종료·정리·최종 근거 검증까지 |

향후 기한은 ‘불변 시작점+채택 수치’와 적용 상위 절대기한 중 가장 이른 경계에 묶습니다. 이미 사용한 시간을 보존하고 reserve나 남은 다른 단계 시간을 더하지 않습니다. 기존 6초 표본 간격·1초 거래 한도를 전용하지 않습니다.

보수적인 경계 규칙으로 **유효기한에 도달하거나 넘으면 초과**, 기한 전 완료 관측과 분류 게시가 모두 확인된 경우에만 해당 구간 완료를 인정하는 안을 제안합니다. 동시성·정밀도 때문에 선후를 증명하지 못하면 정상 수용하지 않습니다. 이 비교 규칙도 아직 채택된 정책이 아니며 숫자를 대신하지 않습니다.

기한 경계와 감시자가 실제 초과를 발견한 시각은 다릅니다. 감시자가 정확히 경계 순간에 실행되거나 동기 query를 취소한다고 보장하지 않습니다. 완료 후 진행 sequence가 늘어도 이미 발생한 초과를 지우지 않습니다.

Windows 8 이후 GetQueuedCompletionStatus의 대기시간에는 저전력 상태 시간이 포함되지 않습니다. 따라서 실제 clock의 suspend 포함 여부와 대기 호출의 의미를 함께 정해야 합니다. [Microsoft 시간 조건](https://learn.microsoft.com/en-us/windows/win32/api/ioapiset/nf-ioapiset-getqueuedcompletionstatus)

clock 실패·역행·domain 변경 또는 입증된 관측 중단은 오류로 보존하고 진행을 차단합니다. 같은 값이 반복된다는 이유만으로 시계 정지를 확정하지 않습니다. 시계와 모든 감시 실행이 함께 멈춘 상태를 그 시계만으로 즉시 감지할 수 있다고 주장하지 않습니다. 재개 후 신뢰할 수 없는 구간을 무알림 정상 구간으로 채우거나 재개 시각을 새 원점으로 삼지 않습니다.

## 이번에 구체화한 것과 남은 결정

호출 예약의 시작·해제, cutoff 요청과 확정 조건, 독립 dispatch 차단, late event 처리, 미반환 query의 UNRESOLVED 상태, P/C/R의 비순환 증거 연결을 이번 세부안으로 제시했습니다. 구현 전에는 아래 다섯 묶음의 구체 근거가 필요합니다.

| 항목 | 다음에 확정할 내용 |
|---|---|
| D1 실제 배치·동기화 | 담당자/실행 흐름, caller와 lock/queue 그래프, 차단 상태의 독립 가시성과 실패 처리 |
| D2 새 표본·판정 연결 | 다른 자원 요구 전체와 원점·단위·신원 유지, current 대체 없는 projection/assessor/control |
| D3 막힌 호출의 물리적 수명 | 안전한 반환·정리 방법의 근거 또는 미해결 격리 절차. 자동 취소 보장 금지 |
| D4 수치 기한·시계 | 별도 승인된 근거, 상위예산·중지 의무와 suspend 의미에 결속된 세 값 |
| D5 저장·Parent 소비 | 정확 타입·enum·인코딩·외부 신뢰 기준·영속 append·검증 방식과 실제 consumer |

다음 단계는 이 세부안의 문서 검토입니다. 최소한 예약/게시 틈, cutoff 조건, 독립 차단, blocked query 정리 한계, P/C/R 연결의 모순을 확인한 뒤 D1–D5를 결정해야 합니다. 새 코드·fixture·시험·설치 OS 관측이 필요해지면 대상·예산·중지 조건을 별도로 승인받습니다. 이번 단계에는 포함하지 않습니다.

## 상태와 전달

계약은 미채택, JOB_CURRENT_COMMIT은 OPEN입니다. native_ready/approved/usable=false, 전체·정상 gate INCOMPLETE, 기존 9묶음 OPEN과 installed t0/계수/raw 미완, 실효 정책·실제 코어 UNVERIFIED를 유지합니다. DOC_R1 N1–N3 문서 지적은 종결 상태입니다. 과거 16개 주제나 106사례 결과를 새 event 모드의 시험 수·검증 결과로 바꾸지 않습니다.

이번 산출물은 새 문서와 참조 사본, 자체 자료 대조 기록입니다. 선택한 로컬 입력 10개의 보존을 대조하며 원격 전체 PC나 과거 전체 원본 보존을 재인증하지 않습니다. BEFORE는 기존 소스 읽기와 자료 도구 작성 뒤, 새 설계문서·basis 복사 전 경계입니다. 기존 코드·계약·ZIP·실패·영수증을 수정하지 않았습니다.

공식 웹문서 열람과 자체 문서/JSON/해시/ZIP 도구만 사용했습니다. 받은 코드 import·기능 시험·CIM·실제 OS/Job 실험·COMSOL/JVM/compile/solve·외부 발송은 없습니다. 최초 자료 도구 작성 호출의 조합 문자열 구문 오류와 처리 범위는 WORK_OBSERVATIONS.json에 구분했습니다. 지정되지 않은 전체 시간 예산을 만들거나 이전 예산을 전용하지 않습니다.

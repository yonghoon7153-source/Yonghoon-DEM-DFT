# Job commit event 보호 — Q1–Q4 결정 제안서

2026-10-16 · 문서 검토용 · 미채택 제안

## 결론과 이번 문서의 역할

**권고는 ‘관리 중인 알림과 조회를 유한한 관측 구간 안에서 처리하고, 그 구간의 한계를 공개하는 별도 event 보호 정책’입니다.** 모든 과거 OS 사건의 처리 완료나 현재 Job commit의 연속 측정을 대신 증명하는 정책은 아닙니다. 이 차이를 받아들일 수 없다면 기존 현재값 요구와 OPEN 상태를 유지해야 합니다.

이번에는 Q1–Q4의 권고 선택지, 필요한 근거, 시작·종료의 선행관계와 Parent 판정표를 작성했습니다. 사용자를 대신해 위험을 수용하거나 새 계약을 채택하지 않았습니다. 세 기한의 숫자도 정하지 않았습니다.

- DOC_R1의 N1–N3 문서 지적 종결은 유지합니다.
- Q1–Q4는 **권고안 작성 완료 / 선택·채택 미완**입니다.
- reader/query/final 기한은 모두 `null`입니다. 따라서 실행 가능한 event 경로를 열 수 없습니다.
- `contract_adopted=false`, `JOB_CURRENT_COMMIT=OPEN`, `native_ready/approved/usable=false`, 전체·정상 gate `INCOMPLETE`를 유지합니다.
- 기존 9묶음 OPEN, installed t0·계수·raw 증거 및 실효 정책·실제 코어 `UNVERIFIED`도 유지합니다.

이는 COMSOL S1 문서입니다. 별도 REIL C4E/E1 승인안과 합쳐 해석하지 않습니다.

## 1. 먼저 선택할 네 가지

| 결정 | 권고안 — 아직 선택되지 않음 | 대안·잔여위험 | 채택 전에 필요한 것 |
|---|---|---|---|
| Q1 최종 관측 범위 | 실행·Job·reader에 결속된 관리 packet/query와 명시한 유한 관측 구간만을 판정 범위로 삼음 | 모든 미전달 과거 OS 사건까지 요구하면 현재 근거로는 종결 불가. 유한 범위에서도 시작 공백, 전달 지연, 미수신 사건, current/maximum 미측정이 남음 | 관측 시작·수신 cutoff·마지막 반영 sequence·제외 범위와 사용자의 명시적 위험 수용 |
| Q2 시작 책임 | 실제 resume를 담당하는 단일 launcher/supervisor가 reader 준비, 설정, 최초 다른 자원 판정과 오류 상태를 한 경계에서 재확인 | fake receipt만으로 resume하거나 기존 전체 표본 함수를 event 전용 함수처럼 사용할 수 없음 | 새 모드의 표본/판정 설계, 독립 감시자, 실제 caller·시계·소유권 결속 |
| Q3 종료 순서 | 유입 차단 → 소유 대상 종료 확인 → 관리 사건 정리 → 잠정 writer/readback → 수신 경계 결속·reader 종료 → 안전한 handle 정리 → Parent 수용 검토 | 빈 queue나 writer 성공은 전체 완전성 증명이 아님. 멈춘 query의 handle 사용, 경계 경쟁, writer 이후 오류가 남으면 불완전 | 절차별 책임·직렬화·기한, writer 뒤 증거 결속, 중단·정리 방법 |
| Q4 최종 판정 | 신원/버전 결속을 먼저 검사하고 위반·감시·종료·정리·coverage·예산·기록을 각각 판정 | rc0·cap·cleanup 중 하나의 성공으로 다른 축 실패를 덮을 수 없음 | 각 증거 필드와 부모 판정표, 최초 관측 오류 및 최초 중지 원인의 별도 보존 |

권고안을 검토·선택하는 것과 구현·시험·실행을 승인하는 것은 별도입니다. 네 선택이 모두 정해져도 수치 기한과 실제 연결의 미결정 사항이 남으면 계약 채택 준비 완료가 아닙니다.

## 2. 공식 근거와 그 근거가 말하지 않는 것

Microsoft는 `JobObjectNotificationLimitInformation`으로 설정한 한도의 알림 메시지는 completion port에 도착한다고 설명합니다. 따라서 ‘모든 Job 알림이 전달 비보장’이라고 쓰면 부정확합니다. 다만 이 문구만으로 유한 전달 시간이나 특정 cutoff 이전의 모든 과거 사건 처리가 입증되지는 않는다는 것이 이번 설계 판단입니다. [Job과 completion port 결속](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_associate_completion_port)

class 12 메모리 알림은 한도를 넘겨도 프로세스의 실행·할당을 계속 허용하며, 위반 정보를 조회하기 전에는 다음 알림 메시지가 오지 않는다고 설명합니다. 이것은 강제 cap과 다른 보호 수단입니다. 10 GiB 알림과 제안된 12 GiB cap의 차이에서 안전 지연시간이나 증가량 상한을 산출하지 않습니다. [알림 한도](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_notification_limit_information)

class 13의 `JobMemory`는 관련 위반 flag가 있을 때 **알림 시점**의 값입니다. 지금의 current 값이나 실행 중 maximum으로 투영하지 않습니다. 새 모드에서도 이 두 값은 `null / NOT_MEASURED_BY_NOTIFICATION`로 구분해야 합니다. [위반 정보](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_limit_violation_information)

`GetQueuedCompletionStatus`의 대기시간 인수는 해당 대기 호출의 제한이지 query·종료 전체의 상한이 아닙니다. Windows 8 이후에는 저전력 상태 시간이 그 대기시간에 포함되지 않는다는 차이도 있습니다. 실제 독립 시계의 의미와 suspend/resume 처리는 별도 결정해야 합니다. [대기 호출과 시간 의미](https://learn.microsoft.com/en-us/windows/win32/api/ioapiset/nf-ioapiset-getqueuedcompletionstatus)

이번에 공식 웹문서는 읽었지만 대상 OS API를 호출하지 않았습니다. 문서의 지원 OS·타입·동작 설명은 이 PC의 설치본·ABI·실효 동작 관측이 아닙니다. 비교 기준은 DOC_R1의 memory-only class 12/13, 단일 reader 제안이며 class 33/34로 자동 대체하지 않습니다.

## 3. Q1 — 관측 범위와 사용자 위험 결정

권고 범위의 시작은 **실행/Job/port/key generation과 결속된 단일 reader의 준비 완료를 supervisor가 관측한 경계**로 제안합니다. 이 경계는 실제 resume보다 먼저 있어야 합니다. 그 이전의 current 상태나 이미 발생했지만 아직 도착하지 않은 사건까지 확인했다고 주장하지 않습니다.

범위를 닫을 때는 다음을 함께 남겨야 합니다.

- 시작 관측 시각·sequence, 실행/clock/Job/root/port/key/reader 신원.
- 수신 cutoff 요청과 실제 경계 확정 시각, 마지막 반영 sequence, 경계에 걸친 packet/query의 처리 여부.
- 관리 pending/query가 없음을 확인한 직렬화 경계. 이는 **관리 집합**의 상태이며 OS의 모든 미전달 사건 부재가 아닙니다.
- reader 종료·handle 정리·Parent 수용 검토의 별도 경계와 각각의 오류.
- 관측 구간 이전·이후, 미전달 사건 및 알림 지연의 제외·불확실성. source 발생 시각을 모르면 `null`이며 receive 시각으로 대체하지 않습니다.

현재값/최대값 미측정, 시작 공백, 알림 지연·overshoot 상한 미확정, 강제 cap의 별도 지원·효력 확인 필요성을 위험 결정문에 모두 노출해야 합니다. 단순히 ‘알림 없음’이나 ‘위험 동의’ 하나로 이러한 전제를 충족시킬 수 없습니다.

수신 cutoff는 최종 수용 시점과 다릅니다. cutoff를 선언했다는 이유로 이미 관측한 위반·오류를 버리지 않습니다. Parent가 결과를 수용하기 전 실제 관측한 위반·오류는 정상 수용을 차단합니다. 나중에 확인한 증거는 원기록을 덮지 않고 후속 기록으로 연결해야 하며, ‘모든 과거 사건 무위반’ 주장은 처음부터 하지 않습니다.

대안으로 모든 과거 OS 사건의 완전 처리를 계속 요구할 수 있습니다. 그 경우 현재 근거로는 충족을 선언할 수 없고 `FINAL_COVERAGE_INCOMPLETE`를 유지합니다. 이번 문서는 그 요구를 임의로 낮추지 않습니다.

## 4. Q2 — 실제 시작의 책임과 현재 구현 공백

다음은 선행관계 제안이며 native 호출 구현이나 실행 명령이 아닙니다.

1. 책임 launcher/supervisor가 실행·독립 clock·소유 Job/root와 설정/readback을 결속합니다. 알려지지 않은 소유권으로 임의 프로세스 중지나 강제 종료를 허용하지 않습니다.
2. 독립 감시 등록 후 단일 reader의 시작·준비 완료를 확인합니다. 감시 등록과 reader 시작 요청의 먼저 발생한 결속 시각부터 초기 reader 기한을 계산하는 안을 제안합니다. 먼저 시작한 작업이 감시 사각으로 빠지면 안 됩니다.
3. **새 event 모드용** 다른 자원의 최초 표본과 판정을 확보합니다. 기존 원점·표본 유효기간·소유권·예산을 유지하고 reader 준비나 resume를 새 원점으로 삼지 않습니다.
4. 실제 resume 책임자가 설정, 유효한 최초 판정, reader 진행, pending/query, 위반·중지·오류 latch 및 남은 예산을 직렬화된 결정 경계에서 재확인합니다. 관측된 사건과 resume 허용 순서를 기록하고 조건이 깨지면 허용을 폐기합니다. 승인 직후 관측된 사건도 후속 중지 의무에서 제외하지 않습니다.

R8 `pre_resume_check`는 fake receipt 확인이고 실제 resume를 하지 않습니다. 기존 `sample_once`는 `collect_owned_sample`에서 raw를 받은 뒤 `ResourceSession.decide`를 호출합니다. 그 수집 경로는 current commit을 필수로 요구하므로 **다른 자원 전용 표본 경로가 이미 구현됐다는 뜻이 아닙니다**. current를 0/null로 끼워 넣거나 `_sample_ok=true`를 강제로 세워 우회하지 않습니다. 새 모드의 필드·projection·assessor 연결은 이후 별도 설계 대상입니다. [R8 후보](basis/os_provider.py.inactive.txt), [Provider 계약](basis/PROVIDER_CONTRACT.json)

event sequence는 resource cursor를 갱신하지 않습니다. 예전 `_sample_ok`를 event 상태에 재사용하지 않으며, 제안된 `other_resource_sample_valid`와 `event_channel_bound`는 분리합니다. 현재는 기한·실제 연결이 미완이므로 후자를 true로 설정할 수 없습니다.

reader/query가 멈춰도 감시자가 초과를 판정할 수 있어야 합니다. 같은 실행 흐름의 반환·같은 잠금·같은 대기열에 의존한 heartbeat는 충분하지 않습니다. R8 `_call`의 반환 후 시계 검사는 막힌 동기 호출의 독립 감시 증거가 아닙니다. 감시자 자체의 진행·책임 인계도 설계하고 검증해야 합니다.

## 5. 세 기한 — 숫자를 정하기 전의 정의

| 기한 | 값 | 기산점·완료 조건 제안 | 초과와 재설정 금지 |
|---|---|---|---|
| reader 진행 | `null` | 초기: 감시 등록/reader 시작 요청 중 이른 결속 시각 → 준비 완료. 반복: 직전 검증된 처리 단계 완료 → 다음 bounded wait 또는 packet 처리 완료 | 초기 초과는 resume 금지, 실행 중은 감시 오류+STOP_REQUIRED. thread 생존·무관 heartbeat·대기 재진입·재시작으로 지연을 지우지 않음 |
| query 완료 | `null` | notification dequeue/관측 → 분류 결과를 공유 상태에 확정. 관측 뒤 대기·lock·API 진입 전·동기 호출·반환 검증·게시 포함 | UNRESOLVED_NOTIFICATION+STOP_REQUIRED. API 진입/재조회/후속 packet으로 원점 재설정 금지. 늦은 성공으로 latch 해제 금지 |
| final 동기화 | `null` | 새 owned 작업 유입 차단을 시작하는 최초 final 진입 → 종료 확인·관리 사건 처리·잠정 writer/readback·cutoff·reader 종료·필수 정리 및 최종 수용 근거 완료 | FINAL_COVERAGE_INCOMPLETE. Job empty·writer 성공·새 오류·reseal로 재시작 금지. 무한 drain/reseal 금지 |

query 기한은 **dequeue 이전 OS 전달 지연을 포함하지 않습니다**. 알림 도착시간을 실제 사건 발생시간으로 바꾸지 않습니다. reader가 정상적으로 유한 대기를 마쳤다는 사실 역시 아직 도착하지 않은 사건이 없다는 증거는 아닙니다.

향후 기한을 채택하려면 불변 시작점·clock/run·완료 증거·감시 책임자·초과 처리와 적용 상위 절대기한을 함께 정해야 합니다. 유효 기한은 ‘시작점+채택 수치’와 적용 phase/overall 등 상위 기한 중 가장 이른 경계에 묶는 안을 제안합니다. 이미 사용한 시간은 남은 예산에서 빠지며 reserve는 추가 시간이 아닙니다. 기존 표본 간격 6초·거래 1초를 reader/query 기한으로 전용하지 않습니다.

숫자를 결정하는 데 필요한 근거는 다음 네 묶음입니다.

1. 정확한 호출 경로·잠금·큐·시계·suspend 처리와 감시자 독립성의 설계 근거.
2. 별도 승인한 fixture 검증의 계획·판정 조건 및, 필요하면 별도 승인한 설치 OS 한정 관측 계획. 이번에는 만들거나 실행하지 않았습니다.
3. 단계별 최악 지연과 남은 중지·정리 예산의 보수적 관계. 측정된 최대시간을 보편적 상한으로 단정하지 않습니다.
4. 지연 허용치의 위험 결정과 초과 시 실제로 진행 가능한 소유 대상 중지·보존 경로. 위반 관측, 중지 요청, API 반환, reader 종료, 실제 Job/root 종료는 각각 입증해야 합니다.

수치를 선택했다는 사실만으로 동기 API의 반환·취소나 OS 메시지 전달의 상한을 증명하지 않습니다. 막힌 query의 안전한 수명주기가 미해결이면 정리 완료도 미확정으로 남깁니다.

## 6. Q3 — 종료 절차 권고와 writer 뒤 증거

아래 순서는 검토할 **문서 권고안**이며 DOC_R1의 미정 D6을 채택된 순서로 바꾸는 패치가 아닙니다.

1. final 기산점을 고정하고 신규 소유 작업 유입을 차단합니다. 종료를 기다리는 동안에도 reader의 수신·조회·지속 STOP 처리는 계속하며, 최종 Job empty·held-root signal·exit를 별도 확인합니다.
2. 관리 packet/query를 유한 기한 안에서 처리합니다. 위반·미해결·감시 오류가 있으면 정상 출력 경로는 닫습니다. 소유 대상 중지·실제 종료 확인과 실패 보존은 별도로 계속 필요합니다.
3. 정상 조건이 유지될 때만 **잠정** writer를 시작합니다. readback 직전에도 latch를 다시 확인합니다. 이 출력은 아직 최종 수용 결과가 아닙니다.
4. writer/readback 뒤까지 실제 수신·오류를 반영하고 수신 cutoff·마지막 반영 sequence를 직렬화해 결속합니다. 경계에 걸친 packet/query가 어느 관리 집합에 속하는지 해결하고 reader 종료를 확인합니다. 해결할 수 없으면 불완전입니다.
5. reader/query가 더는 사용하는 handle이 없음을 확인한 뒤 의존 handle을 정리합니다. 살아 있는 query의 handle을 닫아 버리는 방식으로 정리 완료를 만들지 않습니다. 구체적인 종료·인계 방식은 아직 OPEN입니다.
6. Parent는 잠정 파일의 해시뿐 아니라 writer 이후 오류 원기록, 관측 경계·sequence, reader 종료, 정리 및 latch의 **최종 결속 근거**를 읽고 판정합니다. 그 근거가 없거나 모순되면 수용하지 않습니다.

최초 오류 후에는 새 정상 final writer/readback/clock 호출을 시작하지 않는 기존 원칙을 보존합니다. 위반·stop latch도 정상 진행을 막도록 제안합니다. 이미 실행 중이던 호출이 성공을 반환해도 결과를 정상 수용하지 않습니다. 실패 보존·독립 감시·소유 대상 정리는 별도 경로이며, 정상 출력의 재시도나 자동 reseal 권한이 아닙니다.

최종 결속 근거는 자기 자신의 미래 저장·반환까지 관측한 것으로 쓰지 않습니다. Parent가 완료된 원기록과 파일을 외부에서 확인한 경계를 명시하고 이후 전사를 구분해야 합니다. 이 문서는 그 데이터 형식·원자성·상호 잠금 방법까지 구현했다고 주장하지 않습니다.

## 7. Q4 — Parent의 다중 증거 판정

Parent는 먼저 정확한 mode/revision/manifest/run/clock/Job/port/key/reader 결속을 검사해야 합니다. 구형 manifest, 요약 PASS, 신원 누락·모순을 rc0로 보완할 수 없습니다. 신원 불명 자료는 별도 보존하되 현재 실행의 확정 위반으로 임의 합성하지 않습니다.

| 증거 축 | 별도 기록과 차단 조건 |
|---|---|
| 위반 | MEMORY_VIOLATION_OBSERVED는 지속 STOP_REQUIRED. 오류가 없어도 정상 진행·완료 금지 |
| 알림 미해결·감시 | UNRESOLVED_NOTIFICATION, reader/query 정체·신원/설정 상실·초과를 구분. 위반과 동시에 존재할 수 있음 |
| current/maximum | 기존 계약에서는 미측정으로 요구 미충족. 미래 event 계약에서도 null/미측정을 공개하며 current PASS로 합성 금지 |
| cap·다른 자원 | 소유 Job 설정/readback과 지원·효력, 별도 자원 표본 유효성 필요. cap은 사용량 준수나 무위반 증명이 아님 |
| 종료 | child rc, held-root, Job empty와 종료 방법을 각각 기록. 요청 수락과 실제 종료 확인은 다름 |
| cleanup | reader/query 및 handle 정리 성공·실패·미확정을 별도 기록. 성공해도 위반·감시 실패는 유지 |
| coverage | 선택한 관측 범위·cutoff·sequence·pending/query·writer 전후 오류 결속이 미완이면 FINAL_COVERAGE_INCOMPLETE |
| 권한·예산·시계 | 계약/위험 선택, 구현·검증·OS 관측·해당 실행의 승인은 각각 확인. 기한 null·예산 초과·clock 결속 오류는 정상 수용 불가 |
| 증거 I/O·보존 | writer/readback 불일치·원기록 누락·보존 실패를 별도 기록. 기록 실패가 있으면 완전한 기록이 남았다고 주장하지 않음 |

결속 실패를 우선 검사하고, 모든 정상 진행 차단 원인을 함께 보존한 뒤 종료·cleanup·coverage를 별도로 판정합니다. 단일 대표 사유를 고르는 상세 표시 우선순위는 아직 OPEN이며, 대표 사유 하나로 나머지 원인을 버릴 수 없습니다. 미래의 조건부 수용은 모든 의무가 충족되고 violation/stop/error latch가 없을 때만 검토할 수 있습니다. 의미는 ‘채택된 유한 관측 범위의 event 보호 운영 조건 충족’이지 전체 과거 무위반 또는 current 측정 PASS가 아닙니다. **이번에는 그 결과를 부여하지 않습니다.**

`first_observed_error`와 `first_stop_cause`도 구분하도록 제안합니다. 오류보다 확정 위반이 먼저 중지를 요구할 수 있기 때문입니다. supervisor 관측 시각과 직렬화 sequence에 따라 최초 값을 고정하고 후속 원인은 추가합니다. 대표 사유의 표시 우선순위는 사건 발생 순서가 아닙니다. source 사이 실제 발생 순서는 미확정이며 뒤늦게 더 이른 source 시각을 받아도 첫 관측 기록을 덮지 않습니다.

‘강제 종료가 실제 확인됨 + coverage 불완전’, ‘rc0 + cleanup 확인 + 감시 실패’ 같은 조합을 허용해야 합니다. 종료 방법, 종료 확인, 알림 미해결, coverage를 하나의 `UNRESOLVED` 값으로 뭉개지 않습니다. 기존 종료 enum의 구체적 연결은 별도 schema 검토 사항입니다.

## 8. 다음 전달과 승인 경계

지금 할 일은 [짧은 검토 요청](REVIEW_REQUEST_KO.txt)과 이 제안서를 **COMSOL S1의 계약·실행 설계를 맡은 상대 검토자**에게 전달하여 Q1–Q4 권고와 남은 구체화 항목을 문서로 대조하는 것입니다. 외부 발송은 하지 않았습니다.

그 뒤 사용자가 선택할 사항은 유한 관측 범위와 그 잔여위험을 받아들일지, 또는 완전한 과거 사건/현재값 요구를 유지할지입니다. reader/query/final 수치와 중단·정리 방법이 미완이면 이를 ‘조건부 선택’으로 남기고 계약 채택으로 승격하지 않습니다. 코드 작성·fixture 작성·시험·실제 OS 관측·native 실행은 각 범위와 예산의 별도 승인 이후 단계입니다.

이번 문서에는 실행 argv/cwd, 승인 경로, runtime/release/token을 만들지 않았습니다. 기존 106사례 결과를 새 event 모드 검증에 재사용하지 않으며, 기존 16개 주제는 시험 사례 수가 아닙니다.

### 자료 및 수행 범위

DOC_R1 정정본·수용 회신과 R8 참조 12개 로컬 입력을 읽고 보존 사본으로 결속했습니다. 선택 목록의 BEFORE는 기존 자료를 읽고 자체 데이터 도구를 작성한 뒤, 제안서·basis 사본 작성 전에 기록한 경계입니다. 원격 BML PC나 과거 전체 원본의 재감사가 아닙니다. 기존 ZIP·코드·계약·실패·영수증은 변경하지 않았습니다.

공식 문서 열람, 소스 텍스트 읽기, 새 문서 작성, JSON/파일·ZIP 해시 대조만 수행했습니다. 받은 프로그램 실행·후보 import·기능 시험·CIM·실제 OS/Job 실험·COMSOL/JVM/compile/solve는 없습니다. 자체 데이터 도구 호출을 ‘프로세스 실행 전체 0회’로 표현하지 않습니다. 새 숫자 작업 예산이 지정되지 않았으므로 과거 예산을 전용하거나 전체 시간 준수 주장을 만들지 않습니다.

권고, 필요한 근거, 사용자 선택, 실행 승인을 분리했습니다. 이 제안서의 데이터 검사는 기능 PASS 또는 계약 수용 결과가 아닙니다.

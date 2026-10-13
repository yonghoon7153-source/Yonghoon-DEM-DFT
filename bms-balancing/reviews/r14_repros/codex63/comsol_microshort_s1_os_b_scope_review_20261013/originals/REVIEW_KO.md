# S1 OPEN 다음 범위와 OS B 준비 검토

2026-10-13 · 범위 및 정적 문서 검토 · 구현과 실행 승인 아님

## 결론

**④의 OS 연결부터 B 오프라인 준비를 하는 방향은 수정 조건부 적합하다.** 현재 v1의 세 문구를 고치고 공식 문서 묶음을 식별한 뒤, 사용자가 B 한 건만 별도로 승인하는 순서를 권고한다. 기존 93사례 수용을 다시 열거나 COMSOL을 재실행할 이유는 없다.

판정은 `SCOPE_ACCEPTABLE_WITH_DOCUMENT_CORRECTIONS`다. 아래 N1–N3는 구현 전 문서의 P2 정정이며, 이미 수행된 생산 코드의 결함 판정이나 새로운 P1 실행 차단 발견이 아니다. D/P0의 전제 충돌은 제출자가 Q6으로 신고한 질문에 답하는 정리다.

이번 검토는 두 첨부 원문, 기존 수용 회신·계약·연결 소스, 고정 저장소 원장 및 Microsoft 공식 자료를 읽었다. 후보 import·함수 호출·기능 시험·실제 OS provider/Job 실험·COMSOL/JVM 실행은 하지 않았다. 검토자의 파일·문서·웹 읽기와 회신 포장 도구 사용은 별개다.

## 문서 정정 세 건

좌표는 `received/NEXT_SCOPE_PROPOSAL.md`와 `received/OS_B_SEND_V1.md`의 원문 행이다.

### S1-OSB-N1 ④ 전체 종결과 OS 하위 범위를 구분

**P2 · NEXT_SCOPE_PROPOSAL:23,37,75.** “COMSOL 없이 B+E로 ④를 끝까지 닫는다”는 결론은 현재 중지 계약보다 강하다. 무해 자식 E는 OS 소유권·계수·상한·강제 정리의 근거이지 COMSOL 협조적 중지의 실효 증거가 아니다. 같은 제안의 75행과 RESOURCE_CONTRACT는 force-only를 별도 사용자 결정으로 남겼다.

대체 문장:

> B와 별도 승인된 E로 ④의 OS 기계적 하위 범위를 검증한다. COMSOL 협조적 중지의 지원·통합 근거 또는 별도 승인·검증한 force-only 경로, 실제 실행 연결이 충족돼야 ④ 전체를 종결한다. B 또는 E 통과만으로 전체 종결하지 않는다.

OPEN 네 개의 수를 새로 늘리라는 뜻이 아니다. ④ 안에서 닫힌 하위 범위와 남는 조건을 나눈다. 또한 E의 `mapping`은 **OS API→counter/ownership/stop 대응**이고, C 뒤에 봉인하는 **설치본 생성식→물리 계수 대응**과 다르다고 명시한다.

### S1-OSB-N2 허용한 읽기와 실행 0의 정의를 맞춤

**P2 · OS_B_SEND_V1:17,80.** OS 판·빌드와 디스크 여유 읽기, 정적 도구 사용을 허용하면서 일반 “프로세스 생성·OS API 호출” 모두를 0이라고 쓰면 허용 행위 자체와 충돌한다.

대체 문장:

> 금지 대상은 후보·수신 코드의 import/함수 호출, 기능 시험, 시험용/native 자식·실제 Job 생성 및 counter/Job 설정·조회·중지 어댑터 실험, COMSOL/JVM/컴파일이다. 자체 자료 작성·정적 대조·포장 도구와 허용된 파일·시각·OS 식별·시작 디스크 메타데이터 읽기는 따로 기록한다. 일반 셸/Python 호출이나 OS API 전체를 0회로 보고하지 않는다.

OS 버전·빌드 1회와 ABI에 필요한 OS 아키텍처 및 준비 도구의 비트수 식별은 **사용자가 채택할 허용 목록에 명시**할 수 있다. 실행기를 별도 version probe로 띄우거나 실제 counter를 시험하는 허용으로 확대하지 않는다. 이 검토에서 실행 PC를 관측한 것은 아니다.

### S1-OSB-N3 최종 기록 뒤 시간과 관측 최신성까지 판정

**P2 · OS_B_SEND_V1:63–68,72–78.** 표본 수집 뒤 마감 확인과 최종 디스크 재측정은 적절하다. 다만 마지막 쓰기·재읽기·해시·산출 walk 자체가 마감을 넘거나, 마지막 느린 조회 동안 다른 필수 값이 오래된 경우에도 완료를 거부한다는 조건까지 고정해야 한다.

추가 문장:

> 마지막 필수 쓰기·재읽기·해시·산출 재측정 뒤 현재 monotonic 시각으로 단계·전체 상한을 판정한다. 모든 필수 counter를 포함하는 한 sampling transaction의 duration과 gap, 또는 그에 동등하게 결속된 지표별 관측 구간을 검사한다. 정상 child 종료는 감시 공백·관측 오류·예산 초과를 해소하지 않는다. 위반이면 완료/PASS로 승격하지 않는다.

새 tolerance를 만들지 않는다. 현재 계약의 주기 5초·최대 gap 6초·표본 수집 1초 및 기존 정리 reserve를 그대로 소비한다. 마지막 파일이 자기 자신의 미래 쓰기/반환을 관측했다고 하지 않고 최종 외부 snapshot을 분리한다. **이 조건은 B에서 작성할 코드와 검증안의 요구이며, 이번에 기능 시험을 추가 실행하라는 뜻이 아니다.**

## Q1부터 Q7까지

| 질문 | 회신 |
|---|---|
| Q1 첫 항목과 순서 | ④의 **B 준비 우선**에 동의한다. OS 하위 범위부터 진행하되 전체 종결은 N1처럼 조건부다. |
| Q2 공식 문서 전달 | (a)/(b) 모두 출처가 결속되면 사용할 수 있다. 실행 PC 네트워크 0을 유지하는 **(b)를 권고**한다. 문서 묶음의 실제 이름·크기·SHA를 먼저 채운 다음 사용자 채택을 받는다. |
| Q3 OS 식별 | 판·빌드의 읽기 전용 1회 식별을 제안 범위에 넣을 수 있다. N2의 허용 목록에 적고 실제 API 지원 시험으로 부르지 않는다. |
| Q4 예산과 산출 | 600+1800+600+480+120=3600초다. 필요량 실측이나 완주 보증이 아닌 상한으로 수용한다. 기존 native 예산과 별개이며 전용·확대는 없다. 원본 전후 선택 집합과 마지막 기록 경계를 고정한다. |
| Q5 C solve0 | 실제 C는 JVM·모델/mesh 생성이므로 자원·소유·중지 검증을 우회할 수 없다. **C의 오프라인 관측본 준비**는 별도 승인되면 B와 병렬 가능하지만 이번 B 범위에는 포함하지 않는다. |
| Q6 D와 P0 | **D는 별도 승인될 P0 1회 안의 증거 생성 단계**로 정리한다. 관측 전에는 획득 경로·계약·판정기·안전 연결을 준비하고, 관측 후에는 실제 t0·계수·raw 증거를 수용한다. 숨은 pre-P0 solve는 없다. |
| Q7 현재 Job commit 미확인 | B에서 OPEN으로 보고한 뒤 별도 판단해도 된다. 단, 12GiB cap+host commit은 기존 현재 Job commit 10GiB 조기중지와 동등하지 않다. 변경하려면 필수 입력·조기중지·위험·검증·승인을 별도 고정해야 한다. |

Q6의 “준비”는 단순 stub이나 기대값으로 provider를 채우는 뜻이 아니다. post-consistency t0의 획득 가능 경로 자체를 설계·고정하지 못하면 D 승인부터 보류한다. 필요한 추가 초기화 호출이 생기면 그 호출을 별도 제안하며, runAll/runFrom/runTo/초기화-only solve를 자동 추가하지 않는다. P0 후 증거가 부족해도 추가 시도나 PASS 승격은 없다.

## 공식 API 근거와 후보 작성 조건

### 현재 Job commit과 12GiB 상한

검토한 공개 Win32 `QueryInformationJobObject` 표에서 class28의 지원 계약은 확인하지 못했다. class9의 `PeakJobMemoryUsed`는 peak이고, class34의 `JobMemory`는 notification 시점 값이다. 어느 것도 그대로 현재 표본을 대신하지 않는다. [QueryInformationJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-queryinformationjobobject), [Extended limit](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information), [Limit violation 2](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_limit_violation_information_2)

다만 “Microsoft 근거가 전혀 없다”라고 단정해서도 안 된다. Microsoft hcsshim에는 class28과 `JOBOBJECT_MEMORY_USAGE_INFORMATION` 선언이 있다. 이것은 프로젝트 소스 근거이지 일반 desktop Job의 공개 지원·최소 OS·현재 private commit 의미를 모두 확정한 API 계약은 아니다. 현 Learn 한정 문서 묶음에 자동 추가하거나 이 승인으로 채택하지 않는다. [Microsoft hcsshim 소스](https://github.com/microsoft/hcsshim/blob/main/internal/winapi/jobobject.go)

12GiB Job 상한은 한도를 넘는 commit 요청을 실패시키는 기능이며 정상 종료·정리 보증이 아니다. `TerminateJobObject`는 강제 종료이고 kill-on-close는 마지막 Job handle의 close와 관련된다. [Basic limit](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information), [TerminateJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject)

현재 `resource_connection`은 승인된 Job commit mapping과 현재값을 필수로 요구한다. B에서 이를 null/0/PASS·peak·프로세스 합으로 바꾸지 않는다. 문서 미확인은 예정된 OPEN 결과로 기록할 수 있지만 식별 불일치·자료 손상·예산 초과 같은 예상 밖 오류는 중지 조건이다.

### 문서 목록과 소유권 연결

v1 §1에는 host RAM과 전체 handle/Job lifecycle, clock의 근거 목록이 완결돼 있지 않다. B가 이 기능을 쓸 예정이라면 공식 문서 묶음에 필요한 의존 문서도 넣는다. 예를 들어 기존 GlobalMemoryStatusEx 경로를 쓸 때 그 구조체가 필요하며, GetPerformanceInfo의 PhysicalAvailable 경로를 택한다면 그 단위 변환을 명시해야 한다. host commit과 가용 물리 RAM은 별도 지표다. [GlobalMemoryStatusEx](https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-globalmemorystatusex), [PERFORMANCE_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/psapi/ns-psapi-performance_information)

B의 연결 표·검증안에는 다음을 포함한다. 이는 새 native launcher를 이번에 실행하거나 기존 launcher를 고치라는 뜻이 아니다.

- 명시적으로 소유한 Job handle만 사용한다. Query/IsProcessInJob의 NULL을 소유 증거로 받지 않는다. 기존 이름 Job 재사용이나 외부 Job을 대상으로 삼지 않는다. [Query](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-queryinformationjobobject), [IsProcessInJob](https://learn.microsoft.com/en-us/windows/win32/api/jobapi/nf-jobapi-isprocessinjob)
- 제한 설정/readback·root 할당·소유 확인 전에 작업 child를 Resume하지 않는 연결을 고정한다. 할당 전 메모리는 소급 검사되지 않으며, 외부/nested Job 제약 실패를 breakaway나 권한 완화로 우회하지 않는다. [AssignProcessToJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject)
- ABI의 정수/포인터 폭·정렬·구조체 길이·반환형·인수형·필요 권한·오류 보존을 대응한다. OS build만으로 adapter bitness를 대신하지 않는다.
- PID 목록의 용량·반환 수·길이와 경합을 한정 처리한다. 같은 retained process handle로 PID/생성시각·소유·RSS를 연결한다. bookend 일치는 그 사이 생성·종료된 모든 프로세스나 연속 peak를 관측했다는 뜻이 아니다. [PID list](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_process_id_list)
- ResourceSession/독립 원점과 이전 sample cursor의 소유자를 고정하고, 늦은 표본 때문에 새 session을 만들지 않는다. compile/batch의 Job/root 교체·유지 방식과 전체/native 원점 연결은 표에 드러내고 미해결이면 OPEN으로 둔다.
- 활성 표본 경로는 빈 membership을 거부한다. 정상 종료의 빈 Job은 자원값 0의 가짜 표본으로 만들지 않고, **Job empty + held root signaled + exit query 성공**의 별도 정리 경로에서 확인한다.
- 소유 산출은 본체·wrapper·temp·최종 기록을 합치되 겹친 루트는 한 번만 센다. reparse·교체 경합·미상 항목·읽기 실패·walk 상한 초과를 성공으로 바꾸지 않는다.

이 항목의 양성/음성을 새 함수 경계에 한정한 검증안으로 제출하면 된다. 기존 93개나 130개 전체 재시험을 기본 요구로 만들지 않는다. 실제 ABI·OS 동작 관측은 후속 E의 별도 범위다.

## 문서 묶음과 승인 순서

(b) 묶음은 원 URL·최종 URL·취득 UTC·HTTP 상태·보존 body의 byte size/SHA·문서 절/갱신 표기를 담는다. HTTP 압축을 해제한 body인지 원 전송 바이트인지도 구분한다. SHA는 그 사본의 동일성을 묶는 것이며 Microsoft 진본성이나 OS 지원을 단독 증명하지 않는다. 필요한 본문이 없는 오류/로그인 화면을 공식 설명으로 채택하지 않는다. 공개 저장소에는 원 HTML을 올리지 않고 식별만 남기는 제안은 수용한다.

**순서는 문서 수집 범위 결정 → 묶음 생성·확인 → v2에 실제 식별 채움 → 사용자 B 승인 → 실행 PC에 전달이다.** 원장 §91 끝의 승인 후 묶음 작성 순서는 이처럼 정리한다. 문서 수집도 이번 회신이 외부 자동 발송이나 실행 담당자의 네트워크 권한을 부여하는 것은 아니다.

v1의 `§4 (a)/(b)` 인용은 자기 문서 §4가 아니라 NEXT_SCOPE_PROPOSAL §4다. 동봉 v2는 권고 (b)만 남겨 이 오해를 없앴다. 문서 묶음 식별은 아직 null이다. **동봉 v2는 승인 요청 초안이지 지금 실행 가능한 지시서가 아니다.**

## 식별과 유지 상태

첨부 두 파일의 실제 바이트는 각각 10,420B / `a7e376074cd97195e63098ccd25a921e678538ba0c6e880eaba1934dadd3b5ef`, 11,151B / `2181ddf1faca7b416eac709ebc7bc6f217f5c1522b7fa46089240b603a04c095`다. 원장 §91의 식별과 일치한다. 원장 읽기는 브랜치 이름이 아니라 `c134f8b21ccd360715efbfbd0cad66068429341e`에 고정했다. 원장 §89–91의 발췌를 함께 보존한다.

기준 CODE_MANIFEST `feb12ef6…8ecc`, resource source `f45e6531…5816`, OS_API_MATRIX `ec3ab0c2…622c`, RESOURCE_CONTRACT `e4583742…67c1`은 보존 사본의 실제 바이트로 대조했다. 이번에는 기존 14개 코드·93사례 전체 수용을 다시 수행하지 않았다.

OPEN 4, `native_ready/approved/usable=false`, 전체·정상 gate INCOMPLETE, 실효 정책·실제 코어 UNVERIFIED를 유지한다. `_001`의 `_003` 구간 보존 미확인도 유지한다. P0/P1–P3·K cohort·장시간 계산·microshort 효과 결과 수용은 없다.

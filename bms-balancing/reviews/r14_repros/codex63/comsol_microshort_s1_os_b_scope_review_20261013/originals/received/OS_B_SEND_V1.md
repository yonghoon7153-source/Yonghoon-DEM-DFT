# 실행 담당 Codex 발송 프롬프트 — S1 OPEN ④ OS 자원 · 소유 · 중지 · B 단계 (공식 근거 대응 · 비활성 후보 · 검증안) · 2026-10-13 · 초안 v1

> **사용자가 §0 의 채택 문구를 승인한 뒤에만 보낸다.** 승인 전에는 초안이다. 원장 `COMSOL_REBUILD_SPEC.md` §90 · §91.
> 먼저 검토 담당 Codex 의 범위 검토를 받는다 (요청문 `docs/COMSOL_MICROSHORT_S1_OPEN_NEXT_SCOPE_PROPOSAL_20261013.md`). 그 회신을 반영해 v2 를 만든 뒤 채택한다.
> §0 문구는 이 저장소가 썼다. 근거는 준비본의 별도 허용 초안 B 항 (`SEPARATE_ALLOWLIST_DRAFT_KO.md` B) · `OS_API_MATRIX.json` · 준비본 검토 회신의 ④ 행이다.
> 예산 3,600 초는 S1 OPEN 연결부 준비 (§85 이전 발송문) 와 같은 크기다. 실측된 필요량이 아니다.
> 아래 `---` 사이가 붙여 넣을 본문이다. 같이 첨부:
> - `_003` 검토 회신 zip (`COMSOL_MICROSHORT_S1_OPEN_R1_003_REVIEW_REPLY_20261013.zip` · 38,949 B · sha256 `879cff57…0d17`).
> - 근거 문서 묶음 — §4 의 (b) 를 고르면 이 저장소가 만들어 붙인다 (zip 이름 · 크기 · sha256 은 그때 §0 · §1 에 채운다).

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

## 0. 승인 범위 (사용자 채택 문구 — 승인 시 원문 그대로 붙인다)

> S1 OPEN ④ (실제 OS 자원 · 소유 · 중지 어댑터) 의 B 단계 한 건을 승인합니다 — 공식 근거 대응 · 비활성 provider 후보 · 변경부 검증안 작성입니다. 기준은 OPEN-R1 정정본 (CODE_MANIFEST sha256 `feb12ef6991141aab59fd2fbc0d5f0d138bdd735255aa7123274503ce80b8ecc` · resource source sha256 `f45e6531383d03daa2e968437c6188be0229c144c6956647b0b0f81fae795816` · OS_API_MATRIX sha256 `ec3ab0c209a5aab458fada593c31c63b73f6eec43b902a718823a2391d57622c`) 과 `_003` 검토 회신 (zip sha256 `879cff578dfa52a7dcf0c008cded5f42698bb3b2916570b9e4b5da0b31e10d17`) 입니다. OS API 근거는 첨부한 Microsoft 공식 문서 사본 묶음 (zip sha256 `〔(b) 채택 시 채움〕`) 만 읽고, 네트워크 조회 · 설치 · SDK 내려받기는 하지 않습니다. 새 폴더 `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/microshort_s1_os_b_prep_20261013/` 하나를 씁니다 (이미 있으면 중지 · 삭제 · 재사용 · 다른 이름 우회 없음). 그 안에 ① 지표별 근거 대응표 ② OS counter · Job commit 상한 설정 / 재확인 · 주기 표본기 · 소유 산출 수집기 · 중지 순서의 비활성 후보와 원본 대비 최소 diff ③ 변경부 한정 검증안 (작성만) 을 만듭니다. OS 판 · 빌드는 읽기 전용으로 한 번 식별할 수 있습니다. 상한은 새 원점 총 3,600 초 (근거 대응 600 · 후보 작성 1,800 · 정적 대조 600 · 보존 · 전달 480 · 미완 정리 120) 이고 단계 사이 전용 · 자동 확대는 없습니다. 새 폴더는 50 MiB 이하이고, 시작 디스크 여유 512 MiB 이상을 읽기 전용으로 확인합니다. 경로 / 식별 불일치 · 미예정 변경 · 예산 초과에서는 첫 오류와 자료를 보존하고 멈춥니다. 공식 문서에서 정확히 찾지 못한 counter (예: Job 현재 commit) 는 OPEN 으로 남기고 peak · 구성원 합으로 대신하지 않습니다. 12 GiB commit 상한 제거 · force-only 채택 · 협조적 중지 인정은 이 승인에 들어 있지 않습니다. 프로세스 · Job 생성, OS API 호출 시험, 기능 시험, COMSOL / JVM / compile, 설치본 관측, 정책 · prefs 변경, approval / release / runtime / token 생성은 승인하지 않습니다. 생산 코드 · 정정본 · 원 R1 · 기존 기록은 바꾸지 않습니다. 제출한 뒤 멈춥니다.

(§4 의 (a) 를 고르면 위 문장 "첨부한 Microsoft 공식 문서 사본 묶음 … 만 읽고" 를 "§1 의 공식 문서 URL 만 읽고, 그 밖의 네트워크 조회는 하지 않습니다" 로 바꾼다.)

## 1. 고정 식별

| 대상 | 식별 |
|---|---|
| 기준 정정본 | `…/outputs/microshort_s1_open_connection_r1_20261010/` · CODE_MANIFEST `feb12ef6…8ecc` (14) · `candidate/resource_connection.py.inactive.txt` `f45e6531…5816` · `OS_API_MATRIX.json` `ec3ab0c2…622c` |
| 그 계약 (바꾸지 않음) | `contracts/RESOURCE_CONTRACT.json` (7,175 B · sha256 `e45837427b1b8a69d53b10119ce7ab072bacb869bcdd53c863366c7bd04c67c1`) · `RESOURCE_CLOCK_CONTRACT.json` |
| 기존 OS 경로 (바꾸지 않음) | legacy `winjob.py` — `OS_API_MATRIX.json` 의 `local_source` 행 번호 그대로 |
| `_003` 검토 회신 | zip 38,949 B · `879cff57…0d17` · 판정 `LIMITED_VALIDATION_ACCEPTED_WITH_DOCUMENTED_SCOPE` · 남은 OPEN 4 |
| 근거 문서 | (b) 사본 묶음 zip 〔채움〕 · 또는 (a) 아래 URL 만 |
| 새 폴더 (하나) | `C:/Users/BML/Documents/Codex/2026-09-13/files-mentioned-by-the-user-comsol63/outputs/microshort_s1_os_b_prep_20261013/` |

근거 문서 후보 (Microsoft Learn · 이 초안은 URL 을 열어 보지 않았다 — 목록은 범위 검토 때 고정한다):

| 지표 | 문서 후보 |
|---|---|
| 구성원 RSS | `GetProcessMemoryInfo` · `PROCESS_MEMORY_COUNTERS_EX` — `learn.microsoft.com/windows/win32/api/psapi/nf-psapi-getprocessmemoryinfo` · `…/psapi/ns-psapi-process_memory_counters_ex` |
| host commit | `GetPerformanceInfo` · `PERFORMANCE_INFORMATION` (CommitTotal · CommitLimit · PageSize) — `…/psapi/nf-psapi-getperformanceinfo` · `…/psapi/ns-psapi-performance_information` |
| Job 정보 · 상한 | `QueryInformationJobObject` · `SetInformationJobObject` (information class 목록) · `JOBOBJECT_EXTENDED_LIMIT_INFORMATION` (JobMemoryLimit · PeakJobMemoryUsed · `JOB_OBJECT_LIMIT_JOB_MEMORY`) — `…/jobapi2/nf-jobapi2-queryinformationjobobject` · `…/jobapi2/nf-jobapi2-setinformationjobobject` · `…/winnt/ns-winnt-jobobject_extended_limit_information` |
| 구성원 목록 | `JOBOBJECT_BASIC_PROCESS_ID_LIST` — `…/winnt/ns-winnt-jobobject_basic_process_id_list` |
| 구성원 식별 | `GetProcessTimes` (생성 시각) — `…/processthreadsapi/nf-processthreadsapi-getprocesstimes` |
| 강제 종료 | `TerminateJobObject` · `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` — `…/jobapi2/nf-jobapi2-terminatejobobject` |
| 볼륨 여유 | `GetDiskFreeSpaceExW` — `…/fileapi/nf-fileapi-getdiskfreespaceexw` |
| 협조적 중지 (COMSOL) | 이미 로컬에 있는 COMSOL 6.3 설치 도움말 안에서만 찾는다 — 없으면 UNVERIFIED 유지 |

## 2. 할 일 — `OS_API_MATRIX.json` 의 행마다

| 지표 | 지금 | B 에서 만들 것 (비활성 후보 · 호출 0) |
|---|---|---|
| 소유 Job · root | 선언 · 이전 경로 | 모든 후손 구성원 handle · PID + 생성 시각 · 구성원 bookend 두 번 |
| 구성원 목록 | class 3 선언 | 용량 · 경합 · 오류 처리 — 빈 기본값 없음 |
| 구성원 RSS | ABI OPEN | 고유 (PID, 생성 시각) 쌍마다 WorkingSetSize 1 회 합. 공유 페이지 중복 가능을 표기한다 |
| Job 현재 commit | OPEN | 정확한 class / 구조체가 문서에 있을 때만 후보. 없으면 OPEN 유지 — peak · 구성원 합으로 대신하지 않는다 |
| Job commit 상한 | 미구현 | 설정 + 재확인 대응. 12 GiB 제안은 그대로이고, 설정 / 재확인 실패는 재개 차단이다 |
| host commit | OPEN | CommitLimit − CommitTotal (단위 PageSize) — 가용 물리 RAM 과 따로 |
| host RAM · 볼륨 | 시작 때만 | 주기 표본기 — 아래 "표본기 규칙" |
| 소유 산출 | 수집기 OPEN | 한정 metadata walk — reparse 없음 · 모르는 파일 = 미완 · 원본 제외 · 삭제 없음 |
| 협조적 중지 | UNVERIFIED | 공식 근거가 있을 때만 후보. `getUBlock` · `runFromTo` 에서 추론하지 않는다 |
| 강제 종료 | force-only 경로 | 협조 → 한정 대기 → 소유 Job 강제 → 비었는지 확인. 강제를 graceful 로 보고하지 않는다 · 소유를 모르는 프로세스는 건드리지 않는다 |
| 최종 경계 | `Parent.S1FinalReturn` 불변 | 실제 child rc · clock · writer provider 의 연결 지점만 표시 (Parent 는 바꾸지 않는다) |

**표본기 규칙** (계약 `RESOURCE_CONTRACT.json` 과 준비 검토 회신의 ④ 를 구체화):

- 표본마다 요청 · 도착 시각을 둘 다 남긴다. 공백은 **도착 시각**으로 잰다.
- 성공 여부와 무관하게 공백을 먼저 검사한 뒤에 마지막 유효 시각을 갱신한다 — 늦게 도착한 성공 표본도 공백을 덮지 못한다.
- 값 없음 · 예외 · 첫 표본 지연을 따로 적는다. 감시 실패는 0 이 아니다 (`sampled_max` ≠ OS peak).
- 표본을 모은 뒤 현재 시각으로 마감을 다시 본다. 마감 뒤에는 새 단계를 시작하지 않는다.
- 소유 산출 루트 (본체 · 래퍼 · 임시 · 최종 기록) 를 미리 열거해 합산한다 (겹친 루트는 한 번). 최종 쓰기 뒤 같은 루트로 다시 잰다.
- 경로는 정확 일치 또는 구분자 뒤 하위 경로만 소유로 본다. 비슷한 접두사의 형제 (`…_wrapper` · `…_backup`) 는 소유가 아니다.

**변경부 검증안 (작성만):**

- 새 함수 · 어댑터에만 사례를 둔다. 각 사례에 이유 · 도달 경로 · 양성 대조를 붙인다. 가짜 OS seam 으로만 돈다 (실제 프로세스 · Job 0).
- 위 표본기 규칙의 사례를 각각 하나 이상 둔다. 구성원 경합 · PID 재사용 (생성 시각 불일치) · 상한 재확인 불일치 · 모르는 파일 · reparse · 소유 불명 프로세스도 넣는다.
- 정확한 엔진 · 세션 수 · 예산 제안을 함께 적는다. 이 검증의 실행은 별도 승인이다.

## 3. 봉인 · 중지 · 기록

- 새 monotonic 원점 하나를 쓴다. `TIMING.json` 에 단계 경계를 남기고, 마지막 쓰기 · 재읽기 · 해시 뒤 snapshot 과 반환 전사를 구분한다.
- 첫 오류에서 자료를 보존하고 멈춘다. 남은 단계는 NOT_RUN 으로 남긴다.
- 여기서 "실행 0" 은 후보 / 받은 코드의 함수 · 기능 시험 · OS API 호출 · COMSOL / JVM 을 뜻한다. 정적 parse · 해시 · 포장 도구 사용과는 구분한다.
- 기존 소스 · 정정본 · 계약 · 기록은 바꾸지 않는다. 새 코드는 새 폴더의 비활성 사본으로만 쓰고, 원본과의 최소 diff 를 낸다.

## 4. 유지

- OPEN 4 는 그대로다. ④ 는 B 통과로 닫히지 않는다 — 변경부 검증 · 실제 관측 (E) 이 각각 별도 승인으로 남는다.
- `native_ready / approved / usable = false` · 전체 / 정상 gate INCOMPLETE · 실효 정책 / 실제 코어 UNVERIFIED.
- `_003` 회신의 부속 정정 (`_001` 의 `_003` 구간 보존 미확인) 도 그대로다.

## 5. 회신 형식 · 전달

- 결과 zip 과 PACKAGE_MANIFEST 를 낸다.
- ZIP 밖 기록 (영수증 · 포장 반환 · 최종 확인) 도 모두 파일로 남기고, 그 링크를 한 번에 낸다.

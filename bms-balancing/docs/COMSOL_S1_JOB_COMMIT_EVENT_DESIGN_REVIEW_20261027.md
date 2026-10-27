# COMSOL S1 Job commit event — 조건부 방향 세부 설계 문서 검토 (Claude) · 2026-10-27 KST

> **문서 검토 회신이다 (실행 0).** 대상은 2026-10-16 에 작성된 전달 묶음 `COMSOL_S1_JOB_COMMIT_EVENT_DETAILED_DESIGN_DELIVERY_20261016.zip`
> (605,715 B · sha256 `66fc053154476fa7d022f91ad1c28a08ae68340d6f4220bfc4472c4456ceb957`) 이다. 내부 설계 ZIP 은 599,846 B ·
> `ea8ab14cae57a377cfb66990dce6fa93820aa7597e724860b725acf52d8b36e6` 이다. 이 저장소의 보존본은
> `reviews/r14_repros/codex63/comsol_s1_job_commit_event_detailed_design_20261016/` 에 있다 (`originals/` = 전달 묶음 구성원, `design/` = 내부 ZIP
> 구성원). 규칙 커밋 `eea21e36` → 보존 커밋 `9472f6fc`. 아래 줄 번호는 `design/` 안 파일의 줄이다.
>
> 이 회신은 계약 채택 · 운영 위험 수용 · 구현 · fixture · 시험 · OS 관측 · COMSOL / native 실행의 승인이 아니다. 세 기한은 null 로 두었다.
> `contract_adopted=false` · `JOB_CURRENT_COMMIT=OPEN` · `native_ready / approved / usable=false` · 전체 · 정상 gate INCOMPLETE 를 그대로 둔다.

## 0. 판정

**`DESIGN_DIRECTION_ACCEPTABLE_DOCUMENT_CORRECTIONS_BEFORE_D1_D5`** — P1 0 · P2 5 · P3 5.

세부안의 뼈대는 수용할 수 있다. 근거는 다음 다섯이다.

- 호출 예약과 게시: 예약을 게시 전까지 유지하고, 막힌 reader 의 미게시 내용을 만들어 내지 않는다.
- cutoff 요청과 확정: 요청과 확정을 나눴고, 확정 술어 · 종료 사실을 따로 둔다.
- 막힌 query: 사용 중 handle 을 닫지 않고 thread 를 강제로 끝내지 않는다. 미해결로 남기고 정상 수용을 거부한다.
- P → C → R 증거: 자기 해시가 없고 순환도 없다 (§3-5 의 근거).
- 최초 원인: 최초 오류와 최초 중지 원인을 나눈다.

다만 D1–D5 를 정하기 전에 문서에서 바로잡을 것이 다섯 있다.

| ID | 축 | 무엇 |
|---|---|---|
| JC-01 | 독립 차단 | 감시자 자신이 멈추는 경우를 판정 · 중지로 잇는 규칙이 없다 |
| JC-02 | cutoff · 기한 | reader 기한이 F4 뒤에 정의되지 않았다. final 초과에는 중지 연결이 없다 |
| JC-03 | handle | 사용권 장부가 reader / query 것만 센다. Job handle 닫기는 `KILL_ON_JOB_CLOSE` 로 종료 동작이 된다 |
| JC-04 | 후기 증거 | 실패 경로의 증거 객체가 P / C / R 모형 밖에 있다 |
| JC-05 | Parent 축 | 필드 지도에서 축 넷과 술어 필드 둘이 빠졌다 |

미구현 부분을 완료로 주장하는 위치는 찾지 못했다 (§3-7). 각 지적은 문서 정정 요청이다. 새 시험 · 측정 · 숫자를 요구하지 않는다.

## 1. 검토 범위 · 근거

- **읽은 것 (텍스트 · JSON 으로만):**
  - 본문: `USER_DIRECTION_SELECTION.json` · `DETAILED_DESIGN_KO.md` (167 줄) · `PROTOCOL_DRAFT.json` · `PARENT_EVIDENCE_FIELDS.json` · `REVIEW_REQUEST_KO.txt`.
  - 작성 측 기록: `INTERNAL_DOCUMENT_REVIEW.json` · `STATIC_DOCUMENT_CHECK.json` · `WORK_OBSERVATIONS.json`.
  - basis: `DECISION_PROPOSAL_KO.md` · `PROVIDER_CONTRACT.json` · `RESOURCE_CONTRACT.json` · `os_provider.py.inactive.txt`. 앞 단계 결정 검토 회신
    (`basis/DECISION_REVIEW_DELIVERY.zip` 안의 `REVIEW_KO.txt` · `CODEX_REPLY_KO.txt`) 은 scratchpad 에서 안전 추출해 읽었다.
- **하지 않은 것:**
  - `*.inactive.txt` · `tools/document_bundle.ps1` 등 받은 코드와 도구는 실행 · import 하지 않았다.
  - 시험 · fixture · OS / Job 관측 · COMSOL / JVM 은 0 이다.
  - Microsoft 공식 문서는 이번에 다시 열지 않았다 (네트워크 0). API 의미에 기댄 지적 (JC-03 의 `KILL_ON_JOB_CLOSE` · JC-06 의 반환 조합) 은
    공식 문서의 일반 의미를 쓴 것이고, 각 지적에 그렇게 적었다.
- **이 저장소가 보지 못한 단계:** COMSOL 원장은 §97 (2026-10-14 · OS B R2 입력 중지) 에서 멈춰 있다. 그 뒤 진행은 이 저장소가 받지 않았다 — OS B 준비
  결과 · R8 · DOC_R1 · 106 사례 · 16 주제 · 결정 제안 · 결정 검토 · 사용자 선택 "1번가자". 이번 검토는 이 묶음의 문서와 basis 사본에만 기댄다. R8 ·
  DOC_R1 의 결과 판정은 다시 하지 않았다.
- **식별 대조 (자체 자료 도구 · 읽기만):**

  | 대조 | 결과 |
  |---|---|
  | 전달 묶음 · 내부 manifest | `DELIVERY_MANIFEST` 7/7 · 내부 `PACKAGE_MANIFEST` 23/23 |
  | 수령 · 최종 확인 기록 | 영수증 → 내부 ZIP · manifest 일치. `FINAL_CHECK` 기록 8/8 일치. 도구 반환 전사 둘 → 영수증 · `FINAL_CHECK` 일치 |
  | basis | `BASIS_SPEC` 10/10. 선택 입력 BEFORE / AFTER / POST 각 10 행 = basis 사본 |
  | 중첩 ZIP | 결정 검토 전달 7/7 · 그 안의 결정 검토 ZIP 14/14 |
  | 이 저장소와의 연결 | `RESOURCE_CONTRACT.json` · `resource_connection.py.inactive.txt` 가 앞선 보존본 (§92 폴더) 과 바이트 동일 |
  | 안전성 | 안전 추출 (경로 이탈 · 링크 0) · 비밀 검사 56 파일 0 건 |

- **R8 주장 대조 (basis 텍스트):** 설계 l.44 의 서술 넷이 basis 와 맞는다.

  | 설계 l.44 의 서술 | basis 위치 |
  |---|---|
  | `pre_resume_check` 는 fake receipt 만 확인한다 | `os_provider.py.inactive.txt` l.315–316 |
  | `sample_once` 는 raw 를 받은 뒤 `decide` 를 부르고, 성공 뒤에 cursor · `_sample_ok` 를 갱신한다 | l.465–478 |
  | 수집 경로가 `current_job_commit_bytes` 를 필수로 요구한다 | l.438 |
  | `_call` 의 시계 확인은 반환 뒤에만 한다 | l.264–273 |

## 2. 지적

### JC-01 (P2 · 독립 차단 경로) 감시자 자신이 멈추는 경우의 판정과 중지 연결이 없다

- **위치:**
  - 설계 l.17–19 (역할) · l.32 ("필요한 상태를 읽지 못하거나 게시가 실패하면 정상 허용으로 간주하지 않습니다") · l.144.
  - `PROTOCOL_DRAFT.json` l.45 ("missing, stale or unreachable required state blocks it" — dispatch 를 막는다) · l.117–119 (기한 셋).
- **문제:** 감시자가 지켜보는 것 (reader · query · final) 은 정했다. 그러나 감시자를 지켜보는 것은 정하지 않았다.
  - 'stale' 을 차단 조건으로 쓰지만, 신선도 기준과 그것을 판정하는 주체가 없다.
  - 결과가 dispatch 차단뿐이다. resume 뒤 실행 중에는 새 dispatch 가 없으므로, 이 규칙은 실행 중에 아무것도 막지 않는다.
  - l.144 는 "시계와 모든 감시 실행이 함께 멈춘" 경우만 다룬다. 감시자 하나만 멈추고 시계 · supervisor 는 도는 경우는 다루지 않는다.
- **정적 반례:**
  1. resume 뒤 class 13 query 가 막힌다.
  2. 같은 무렵 감시자 실행 흐름이 멈춘다.
  3. query 초과를 게시할 주체가 없으므로 STOP_REQUIRED 가 latch 되지 않는다.
  4. supervisor 는 소유 대상 중지를 시작할 근거를 받지 못한다.
  5. 그 상태가 상위 기한 (basis `RESOURCE_CONTRACT.json` l.20 `native_wall_limit_s`) 까지 갈 수 있다. 그 상위 기한도 같은 감시자가 본다면, 그 기한마저 아무도
     보지 않는다.
- **요청 (숫자 없이 문서로):**
  1. 감시자 생존 근거 — 진행 sequence 를 정하고, query 잠금 · 정상 큐에 기대지 않고 supervisor 가 읽을 수 있는 게시 위치를 정한다.
  2. 그 신선도 기한 — 넷째 기한으로 두되 null 이다. D4 에서 함께 정한다.
  3. 실행 중 감시 상태가 stale · 도달 불가이면 supervisor 가 STOP_REQUIRED 를 latch 하고 소유 대상 중지 경로로 잇는다. dispatch 차단만으로 끝내지 않는다.
  4. 감시자의 초과 게시가 남는 영속 기록 경로를 정한다 (어느 원장인지 · 그 append 가 supervisor 의 잠금 · I/O 에 기대는지). JC-08 과 이어진다.
  5. Parent 필드 (JC-05 (b)) 를 둔다.
  6. D1 의 "실패 처리" 에 감시자 자신의 실패를 명시한다.

### JC-02 (P2 · cutoff · 기한 일관성) reader 기한이 F4 뒤에 정의되지 않았고, final 초과에 중지 연결이 없다

- **위치:**
  - 설계 l.132 ("이후에는 검증된 처리 단계 완료부터 다음 유한 대기·처리 완료까지") · l.80 (F4 는 새 receive 예약 금지) · l.85 · l.76 (F6) · l.134.
  - `PROTOCOL_DRAFT.json` l.117 · l.119 (`final_synchronization.expiry` = "FINAL_COVERAGE_INCOMPLETE; reject normal result").
- **문제 1 — reader 기한의 끝:**
  1. F4 직전에 마지막 receive 가 timeout 으로 돌아오고, 그 처리 완료가 게시된다.
  2. 반복 정의는 그때부터 "다음 유한 대기 · 처리 완료" 까지 기한을 건다.
  3. 그러나 F4 이후에는 새 receive 가 금지라 다음 대기가 없다.
  4. 문서대로 구현하면 두 가지 중 하나가 된다. 문서는 어느 쪽인지 정하지 않는다.
     - (a) 그 기한이 반드시 초과되어 STOP_REQUIRED 가 되고, 정상 실행이 매번 거부된다.
     - (b) 기한이 말없이 풀려서, F5 술어 2 (새 receive 없음 확인) 와 F6 (reader 종료) 사이의 reader 정체가 reader 기한 밖에 놓인다 (final 기한만 남는다).
- **문제 2 — final 초과:** F1 (소유 Job / root 종료 확인) 이 final 구간 안에 있다. 그래서 final 초과 시점에 소유 대상이 아직 살아 있을 수 있다. 그런데 결과에는
  STOP_REQUIRED · 소유 대상 중지 연결이 없다. reader · query 초과 (l.117 · l.118) 에는 있다.
- **문제 3 — receive 대기 timeout:** GetQueuedCompletionStatus 의 timeout 은 F4 때 이미 예약된 receive 가 F5 를 막는 최대 시간이다. 그런데 세 기한과의 관계가
  없다 — reader 기한 이하인지, final 기한 안에서 얼마를 차지하는지.
- **요청:**
  1. reader 기한 사슬이 F4 요청 뒤 어떻게 이어지고 어디서 닫히는지 적는다: 이미 예약된 receive 의 반환 → 필요한 query 게시 → 새 receive 없음 확인 →
     reader 실제 종료 (F6). 그 구간의 초과 결과도 적는다.
  2. final 초과 시 소유 대상 종료가 미확인이면 STOP_REQUIRED · 소유 대상 중지로 잇는다.
  3. receive 대기 timeout 과 세 기한의 관계식을 둔다 (값은 D4).

### JC-03 (P2 · 사용 중 handle 정리 금지) 사용권 장부가 reader / query 만 센다 · Job handle 닫기는 종료 동작이다

- **위치:**
  - 설계 l.18 (reader / query 의 handle 사용권) · l.76 (F6 "사용권 없음") · l.94.
  - `PROTOCOL_DRAFT.json` l.31 (`handle_users`).
  - `PARENT_EVIDENCE_FIELDS.json` l.37 (`cleanup.remaining_query_handle_users`).
  - basis `PROVIDER_CONTRACT.json` l.203 · l.664 · `os_provider.py.inactive.txt` l.332 — Job 의 limit flags 가 `JOB_MEMORY` 와 `KILL_ON_JOB_CLOSE` 를 요구한다.
- **문제 1 — 장부 범위:** 같은 Job / root handle 을 다른 역할도 쓴다.
  - supervisor: F1 의 membership · root exit 조회, 소유 대상 중지.
  - 감시자: 쓴다면.
  - 사용권 규칙과 Parent 필드는 reader / query 사용만 센다.
  - 정적 반례: F6 에서 Job handle 을 닫는 도중에 감시자가 final 초과를 latch 한다. supervisor 중지 경로가 같은 handle 로 Job 종료를 부른다. F6 의
    "사용권 없음" 은 이 사용을 보지 못한다.
- **문제 2 — `KILL_ON_JOB_CLOSE`:** Job 의 마지막 handle 을 닫으면 남은 구성원이 종료된다 (공식 문서의 일반 의미 · 이번에 원문을 다시 열지 않았다).
  - F1 이 빈 membership 을 확인한 정상 경로에서는 무해하다.
  - 실패 · blocked-query 경로에서는 Job handle 정리가 "정리" 가 아니라 종료 방법이다.
  - supervisor 프로세스가 끝날 때 OS 가 모든 handle 을 닫고 막힌 query thread 도 끝낸다. 이것도 같은 효과다. 그러므로 l.94 의 "사용 중 handle 을 닫지 않는다 ·
    thread 강제 종료 금지" 는 그 프로세스가 끝나는 시점에는 지켜질 수 없다.
  - 그 시점에 일어나는 일 (구성원 종료 · thread 종료) 은 끝나는 프로세스 자신이 기록할 수 없다.
- **요청:**
  1. 사용권 장부를 모든 handle 사용자로 넓힌다. 역할별로: reader receive (port) · reader query (Job) · supervisor 종료 확인 (Job · root) · supervisor 중지 (Job) ·
     감시자 (해당 시). Parent 필드는 `cleanup.remaining_handle_users_by_role` 로 바꾼다.
  2. Job handle 닫기의 조건을 둔다: F1 의 빈 membership 확인 + 사용자 0 일 때만 정리다. 그 밖에는 종료 축의 종료 방법 (예: `JOB_CLOSE_KILL`) 으로 기록하고,
     정리 성공으로 세지 않는다.
  3. D3 (막힌 호출의 물리적 수명) 에 supervisor 프로세스가 끝나는 경우를 넣는다: 암묵적 handle 닫기 · thread 종료 · `KILL_ON_JOB_CLOSE`. 그 사실을 누가
     기록하는지 (외부 관찰자 · Parent) 도 정한다.

### JC-04 (P2 · 후기 증거 결속) 실패 경로의 증거 객체가 P / C / R 모형 밖에 있다

- **위치:**
  - 설계 l.66 ("실패 보존·소유 대상 중지 경로로 분기") · l.72 (F2 "정상 조건에서만 잠정 writer 시작") · l.102 · l.106–110.
  - `PARENT_EVIDENCE_FIELDS.json` l.55 (C 의 필수 필드가 P 를 요구) · l.10 (`strict_interpretation` — 필수 필드 누락 · null 은 거부).
  - `PROTOCOL_DRAFT.json` l.103 (`failure_path` — 활동만 있고 순서가 없다).
- **문제 — C 가 성립하지 않는 두 경우:**
  - 확정 위반이 F2 전에 관측되면 잠정 writer 를 시작하지 않으므로 P 가 없다. C 의 필수 필드 `P_external_id_byte_length_and_sha256` · `P_write_completion_ref` ·
    `P_readback_ref` 는 P 를 요구한다. 그래서 실패 실행은 C 를 만들 수 없다.
  - P 를 쓴 뒤 readback 전에 위반이 latch 되면, l.102 에 따라 새 정상 readback 을 하지 않는다. P 는 있지만 readback 이 없으므로 역시 C 가 성립하지 않는다.
- **결과:** 가장 중요한 실행 (위반 관측 → 중지) 에 대해, Parent 가 어떤 객체로 판정하는지 정해지지 않았다. 판정할 것은 종료 · 정리 · coverage · 최초 원인 · 보존
  완전성이다. 실패 경로의 순서도 F0–F8 처럼 적혀 있지 않다: 중지 요청 → 종료 확인 → reader 의 남은 처리와 종료 → handle 정리 → 실패 근거. 그 경로에서 수신을
  언제 닫는지 (cutoff 의 뜻) 도 없다.
- **요청:**
  1. 실패 종결 객체를 정의한다 (C 의 실패 변형도 된다). P 의존 필드는 명시 enum 으로 조건부로 만든다 — 예: `provisional_state ∈ {NOT_STARTED, WRITTEN_NOT_READ_BACK,
     READ_BACK}`. null 강제는 쓰지 않는다.
  2. 그 객체의 필수 축 (Parent 축과 같은 것) 을 정한다.
  3. 실패 경로의 순서 · 수신 닫기 의미를 정한다.
  4. R 이 실패 실행을 어떻게 판정하는지 정한다: 모든 원인을 둔 거부 + 보존 완전성.

### JC-05 (P2 · Parent 필수 축 누락) 필드 지도에서 축 넷과 술어 필드 둘이 빠졌다

- **위치:**
  - 설계 l.120 (판정할 축) · l.34–44 (시작 · resume) · l.82–86 (F5 술어) · l.94.
  - basis `DECISION_PROPOSAL_KO.md` §7 의 축 표 · `PARENT_EVIDENCE_FIELDS.json` l.31–41 (`required_axes`).

| | 빠진 것 | 왜 필요한가 |
|---|---|---|
| (a) | **event 통로 설정 근거** — class 12 알림 한도의 요구값 · 설정 · readback (값 · flag) · completion port 결속 (port · key generation 이 소유 Job 에 실제로 결속됐다는 근거) · 알림마다의 class 13 재무장 기록 | event 모드의 보호 수단이 이것이다. `cap` 축 (l.34) 은 강제 cap (basis 의 12 GiB · `JOB_MEMORY` · `KILL_ON_JOB_CLOSE`) 만 담는다. 이 근거가 없으면 "알림 0" 이 "한도 미설정 · 다른 값 · port 미결속 · 재무장 실패" 와 구별되지 않는다. 결정 제안 l.71 의 `event_channel_bound` 도 이 필드에 묶여야 한다 |
| (b) | **알림 미해결 · 감시 축** — UNRESOLVED_NOTIFICATION · reader / query 정체 · 신원 / 설정 상실 (port · key · Job 결속 상실) · 감시자 자신의 오류 | 설계 l.120 과 결정 제안 Q4 표는 이 축을 따로 판정한다고 쓴다. 그런데 필드 지도에는 `latches.expiry_latched` 와 `timing.independent_monitor_ref` 로 흩어져 있다 |
| (c) | **시작 · dispatch 축** — 감시 등록 · reader 준비 · 최초 다른 자원 판정 · 자격 발급 · 재확인 · 1 회 소비 · 폐기 · dispatch 진입 시각 · 그 전후에 관측한 사건 | 설계 l.42 의 "호출 진입 이후라면 … 소유 대상 중지 경로" 를 Parent 가 검증할 근거다. 지금은 `other_resources.new_mode_assessment_ref` 와 `event.observation_start_ref` 만 있다 |
| (d) | **종료 축의 중지 요청** — 협조 · 강제 요청의 참조 · 시각 · 결과 | l.94 는 "그 요청과 실제 종료를 각각 기록" 한다고 쓴다. 그런데 `termination` 축 (l.36) 에는 방법과 확인만 있다 |
| (e) | **F5 술어 2 · 3 의 필드** — reader 의 새 receive 없음 확인 참조 · 확정 경계의 상태 version | `event` 축 (l.31) 에는 `last_applied_seq` 만 있다. 그래서 Parent 가 cutoff 확정의 세 술어를 다 검증할 수 없다 |

- **요청:** 위 다섯을 필드 지도에 더한다. 엄격 해석 (누락 → 거부) 의 대상에도 넣는다.

### JC-06 (P3 · 예약 / 게시 틈) 전이 불변식 · PROTOCOL 사례 2 · 패킷 모양 분류

- **결정적 틈은 없다:** receive 예약은 게시까지 유지되고, 게시가 pending 을 만들고, query 예약은 진입 전에 등록된다 (l.54 · `PROTOCOL_DRAFT.json` l.40 · l.42). 그래서
  작업이 어느 집합에도 없는 순간은 규칙에서 나오지 않는다. 다만 F5 의 "모두 0" (l.84) 은 다음 불변식이 있어야만 성립한다 — **승인된 작업은 모든 상태 version 에서
  적어도 한 집합에 있다 · 해제는 다음 집합 등록과 같은 version 이거나 그 뒤다.** 이 불변식을 한 줄로 적어 둘 것.
- **PROTOCOL 사례 2:** `PROTOCOL_DRAFT.json` l.96 (반환은 관측했으나 검증 · 게시 미입증) 에 `handle_use` 키가 없다. 사례 1 (l.95) 에는 있다. 설계 l.54 에 따르면
  게시 전까지 사용권은 유지되므로, 사례 2 도 `RETAINED` 로 적어야 한다.
- **패킷 모양 분류:** l.62 는 FALSE + null OVERLAPPED 만 다룬다. 다음 넷도 분류표에 넣어, 조용히 버리지 않고 오류 · latch 로 게시할 것.
  - TRUE + null OVERLAPPED.
  - FALSE + non-null OVERLAPPED.
  - 모르는 message id.
  - 다른 generation 의 completion key.
  - 공식 문서의 일반 의미를 쓴 지적이다. 실제 조합은 D1 의 호출 설계에서 정한다.

### JC-07 (P3 · cutoff) 예약 없는 receive 의 탐지 · 꼬리 구간 · port 체류 시간

- **예약 없는 receive:** l.88 · `PROTOCOL_DRAFT.json` l.80 은 cutoff 뒤 새 receive 를 프로토콜 오류로 정한다. 그러나 예약 없이 들어간 대기는 반환 · 게시 전에는 보이지
  않는다. 탐지 방법을 적을 것 — 예: 모든 반환은 예약 id 를 가져야 하고, 짝이 없는 반환은 오류다. 대기 중인 것은 F6 의 reader 종료 확인이 마지막 방어다.
- **꼬리 구간:** F1 (종료 확인) 과 F4 (수신 닫기 요청) 사이의 길이가 정해지지 않았다. 지금은 F2 · F3 의 writer / readback 소요로 우연히 정해진다. 그런데 이 길이가
  "늦게 도착한 알림 · 이미 일어난 위반을 놓칠" 잔여위험의 크기를 정한다. 최소 꼬리 (또는 "꼬리 0" 의 명시) 를 D4 의 결정 항목에 넣고 coverage 에 기록할 것.
  선택안 (결정은 작성 측): F4 전에 0 대기 수신으로 이미 port 에 있는 packet 을 비우는 단계. 완전성 증거는 아니고 제외 집합을 줄일 뿐이다.
- **port 체류:** l.56 은 dequeue 이전을 "OS 전달 지연" 이라 한다. 그런데 이 구간에는 reader 처리량 때문에 port 에 쌓여 기다린 시간도 들어 있다. 대기 호출은 적재
  시각을 주지 않으므로 이 시간은 관측할 수 없다. 세 기한 어디에도 들지 않는다. 잔여 "알림 지연" 에 이것도 포함된다고 적을 것.

### JC-08 (P3 · 후기 증거 결속) 두 상태의 결정 경계 결속 · R 이 검증하는 원장 head

- **두 상태:** l.32 는 판정 상태와 독립 차단 상태를 둘로 나눴다. 그런데 C 의 `final_latches` 와 R 의 `decision_boundary_state_version_and_latches`
  (`PARENT_EVIDENCE_FIELDS.json` l.62) 는 상태 version 을 하나만 적는다. Parent 의 마지막 재확인 (l.116) 은 두 상태의 version 을 모두 결속해야 한다. 그렇지 않으면
  판정 상태 snapshot 뒤에 독립 차단 상태에 걸린 초과를 놓칠 수 있다.
- **원장 head:** C 의 `final_supervisor_ledger_head` 뒤에도 supervisor 원장에 기록이 붙을 수 있다 — C 자신의 쓰기 · readback 기록, F8 중의 초과 latch. R 의
  `verified_supervisor_ledger_head` 는 C 가 가리킨 head 가 아니라 결정 경계에서의 head 여야 한다. 그 사이 기록에 원인이 있으면 거부한다고 적을 것.

### JC-09 (P3 · D2 의존) R8 의 종료 관측은 `_sample_ok` 를 요구한다

- basis `os_provider.py.inactive.txt` l.503 — `_terminal_observation` 은 `_sample_ok` 가 없으면 `TERMINAL_WITHOUT_VALID_MONITOR_SAMPLE` 로 실패한다.
- event 모드는 기존 표본 경로를 쓰지 않고 `_sample_ok` 를 강제로 세우지 않는다 (설계 l.44). 그러므로 F1 의 종료 확인도 새 선행 조건이 필요하다 — 예: 새 모드의 다른
  자원 표본 유효성. D2 의 범위에 "종료 관측의 선행 조건" 을 넣을 것. 그러지 않으면 구현 때 `_sample_ok` 를 우회하고 싶은 압력이 생긴다.

### JC-10 (P3 · 문구) F5 술어 2 의 과거형

- l.85 "reader가 새 receive를 시작하지 않는 상태를 **확인했습니다**." — 술어 목록 안에서 과거형이라, 이미 확인한 사실처럼 읽힌다. "확인한 상태여야 한다" 로 고칠 것.
  (§3-7 의 완료 주장으로 세지는 않는다.)

## 3. 요청한 일곱 축별 결과

| # | 축 | 결과 | 관련 지적 |
|---|---|---|---|
| 1 | 예약 / 게시 사이의 틈 | 결정적 틈 없음. reader 가 dequeue 와 게시 사이에서 멈추면 receive 예약이 남아 cutoff 를 막는다. 독립 감시는 정체만 기록하고 packet 내용을 만들어 내지 않는다 (l.58) — 일관된다. 불변식 · 사례 2 · 모양 분류를 명시할 것 | JC-06 |
| 2 | cutoff 조건의 일관성 | 본문 F5 의 세 술어와 `PROTOCOL_DRAFT.json` `cutoff.commit_predicates` (l.77) 는 일치한다. sentinel · queue empty · rc0 대체 금지도 일치한다. reader 기한 사슬 · final 초과 · 대기 timeout 은 정해지지 않았다 | JC-02 · JC-07 · JC-05 (e) |
| 3 | 독립 차단 경로 | 두 상태를 나누고 감시자가 port · class 13 을 직접 다루지 않게 한 것은 맞다 (l.23 · l.32). 감시자 자신의 정체가 빠졌다 | JC-01 |
| 4 | 사용 중 handle 정리 금지 | 원칙은 본문 · PROTOCOL · Parent 에서 일관된다 (l.94 · l.96 · l.98). 작성 측 내부 검토가 고친 "독립 종료 사실 덮어쓰기" 도 본문에서 해소된 것을 확인했다. 장부 범위 · `KILL_ON_JOB_CLOSE` · 프로세스 종료가 빠졌다 | JC-03 |
| 5 | 후기 증거 결속 · 자기 해시 순환 | **순환 없음** (아래 근거). 실패 경로 객체가 없다. 두 상태 · 원장 head 의 결속도 필요하다 | JC-04 · JC-08 |
| 6 | Parent 필수 축 누락 | 축 넷 + 술어 필드 둘이 빠졌다 | JC-05 |
| 7 | 미구현을 완료로 주장하는 위치 | **없음** (아래 근거) | JC-09 · JC-10 (구분용) |

### 3-5. 자기 해시 순환이 없다는 근거

참조 방향은 한쪽뿐이다.

- P 의 본문에는 저장 전 사실만 있다. 저장 전 원장 head 는 P 의 사후 저장 · readback 기록보다 앞선다 (l.108 · l.112).
- 사후 기록과 C 는 완료된 P 바이트를 가리킨다 (l.109).
- R 은 완료된 P · C 를 가리킨다 (l.110).
- 원장 기록은 직전 기록의 바이트 해시만 가진다. 자기 해시는 외부 인덱스나 다음 참조가 계산한다 (l.112 · `PARENT_EVIDENCE_FIELDS.json` 의 `ledger`).
- 어떤 객체도 자기 해시나 자기 미래 저장을 담지 않으므로 순환이 없다.

남는 것은 순환 문제가 아니라 신뢰 위치 문제다. 마지막 원장 기록과 R 의 신원을 결속할 "외부 인덱스" 의 위치 · 신뢰 기준은 D5 의 몫이다.

### 3-7. 완료 주장이 없다는 근거

설계 본문의 "구현 · 완료 · 보장 · 확정 · 충족 · 종결" 표현과 PROTOCOL · Parent 의 "complete · verified · atomic · closed · resolved" 표현을 모두 대조했다.

- 구현 상태를 말하는 곳은 모두 미완 · OPEN 으로 적혀 있다: l.11 · l.32 · l.60 · l.98 · l.148 · `new_mode_resource_projection_assessor: OPEN_DESIGN_NOT_IMPLEMENTED`
  · `R8_pre_resume_check: Fake receipt verification only`.
- 현재형 처방 문장 (l.36 · l.54 · l.80 등) 은 l.11 의 "R8 코드에 적용된 동작이 아닙니다" 아래에 있다.
- l.162 의 "DOC_R1 N1–N3 종결" 은 앞 검토 회신의 판단을 옮긴 것이다. 이 저장소는 DOC_R1 을 받지 않아 다시 판정하지 않았다.
- `INTERNAL_DOCUMENT_REVIEW.json` 의 "resolved" 둘은 작성 측의 내부 검토라고 스스로 밝힌다. 이번 검토에서 두 해소 (P 의 자기 사후 기록 · 독립 종료 사실 덮어쓰기)
  를 본문으로 확인했다.

## 4. 유지되는 것 · 하지 않은 것

- 유지:
  - 세 기한 null (본문 l.132–134 · PROTOCOL l.117–119 · Parent `null_required_current_state` — 네 곳 일치).
  - 계약 미채택 · `JOB_CURRENT_COMMIT=OPEN` · `native_ready / approved / usable=false` · 전체 · 정상 gate INCOMPLETE.
  - 기존 9 묶음 OPEN · 설치본 t0 / 계수 / raw 미완 · 실효 정책 · 실제 코어 UNVERIFIED.
- 이 검토는 D1–D5 의 결정이 아니다. 지적의 요청은 문서에 무엇을 적을지를 말할 뿐, 수치 · 구현 방식 · 시험 범위를 정하지 않는다.
- 하지 않은 것: 받은 코드 · 도구 실행 · import 0 · 시험 · fixture · OS / Job 관측 · COMSOL / JVM 0 · 공식 문서 재열람 · 네트워크 0 · 기존 원본 · 코드 · 계약 · 영수증
  변경 0 · 외부 발송 0 (발송은 사용자 몫).

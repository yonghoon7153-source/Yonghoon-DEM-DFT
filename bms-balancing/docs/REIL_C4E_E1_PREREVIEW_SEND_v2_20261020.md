# Codex 발송 프롬프트 — REIL C4-E · E1 승인 요청 v2 (E1-0 한정) 사전 검토 · 2026-10-20 KST

> E1 사전 검토 회신 (상태 문서 §74 — 정정 필요 N1–N6) 과 사용자의 정정 범위 채택 (§75) 에 따라 쓴 비활성 초안과 수정 승인 요청이다.
> 아래 `---` 사이가 붙여 넣을 본문이다. 같이 첨부할 것은 없다 (검토자가 저장소에서 읽는다).

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

REIL C4-E · E1 승인 요청 v2 를 사용자 승인 전에 사전 검토해 주세요. 지난 회신 (§74) 의 N1–N6 과 자체 발견 S1 을 반영한 **비활성 초안 넷과 수정 승인 요청**입니다.
승인 구조는 회신의 권고대로 바꿨습니다 — 이번 요청의 승인 대상은 **E1-0 (launcher 대조 RED · GREEN) 뿐**이고, E1-1–3 (identity · 읽기 경로 · fetch · run) 은
고정 계획만 적어 두었습니다. 초안 작성은 사용자 범위 채택 (§75) 뒤에 했고, 정적 검사 (AST 파싱 · 이름 검사 · 골격 상수 일치 · 비밀 검사) 만 했습니다. launcher ·
실행기 · 시험 · 탐침 · 읽기 경로 · fetch · run 은 모두 0 회입니다. 브랜치 `claude/14-gate-code-review-9qkx05` 의 최신 HEAD (이 발송문이 든 커밋) 를 기준으로 보시면
됩니다.

## 1. 볼 것

| 파일 (bms-balancing 기준) | sha256 | 무엇 |
|---|---|---|
| `docs/REIL_C4E_E1_APPROVAL_REQUEST_v2_20261020.md` | (이 커밋의 바이트) | 수정 승인 요청 — E1-0 한정 · 정정 대응표 · 정확한 명령 · RED / GREEN 기준 · 활동 범위 셋 · E1-1–3 고정 계획 · 밝힐 것 12 |
| `docs/REIL_C4E1_LAUNCHER_DRAFT_v2_20261020.py.txt` | `ab33844fbdaa4e6939871abec09953783cfccd7b4d32ee023ab8691cdb814398` | launcher v2 (stdlib · 실행 모듈 import 0) |
| `docs/REIL_C4E1_LAUNCHER_SKELETON_DRAFT_v2_20261020.py.txt` | `5617a16aa8b093bac485e0bf775109c77ba9699d43301cf503e783365798b362` | RED 골격 (import · 상수 동일 · 함수 34 = NotImplementedError) |
| `docs/REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v2_20261020.py.txt` | `c1dc5b4353fa97e29b988604b612c7f40e46d3562980bde40dfd4712e4fde4ea` | 대조 24 (기존 14 정정 + 새 10) |
| `docs/REIL_C4E1_STEP_RUNNER_DRAFT_20261020.py.txt` | `aae2ec14c4d652ef9a9e5b1c45bf52896d2234dce16eac77942911e596669fed` | E1-0 외곽 실행기 (N5 · subreaper) |
| `docs/REIL_C4E_E1_REVISION_SCOPE_20261015.md` · 상태 문서 §74 · §75 | — | 정정 범위 · 회신 접수 · 사용자 채택 |

## 2. 지적 ↔ 정정 (요청서 §2 의 요지)

| ID | 정정 | 대조 |
|---|---|---|
| N1 | 셋 (`reil_c4_e3a` · `reil_c4_monitor` · `reil_c5_pilot`) 의 같은 이름 패키지 · 확장 파일 정적 검사 + 탐침이 자식과 같은 상태 (bms-balancing 을 sys.path[0]) 에서 `sys.meta_path` finder 에 `find_spec` 만 물어 origin · loader 를 승인 `.py` (SourceFileLoader · PathFinder) 에 결속 — 경로를 명시해 묻기 때문에 부모 import · 대상 실행 0 | l15 · l16 · l1 |
| N2 | /proc 관측에서 PID 소멸만 사라짐 · 권한 / I/O / 파싱 / 목록 오류는 unknown 으로 확정 (뒤의 관측 · rc 0 으로 지우지 않음) · l11 판정기 정정 | l18 · l11 |
| N3 | kill 결과 기록 · kill 뒤 10 s · 그룹 관측 5 s · 재관측 5 s 의 유한 대기 · 미종료 기록 · 단계별 예외 → `errors` · `first_error` · `launched` · meta 실패 시 stderr + rc 4 · Git 기록 rc · HEAD 불변 | l19 · l20 · l21 |
| N4 | 자식 env 의 `GIT_*` 를 `GIT_SSL_CAINFO` 허용 목록으로 · fetch 전 `git config --list --show-origin` 금지 키 (URL 바꿈 · 프록시 · 자격 도우미 · TLS 끔) · `ls-remote --get-url` = 고정 URL · fetch 뒤 `remote.origin.url` · 유효 출처 · `.git/shallow` · alternates (FETCH_HEAD 는 기록만) | l22 · l23 · l24 · l13 |
| N5 | E1-0 전용 외곽 실행기 — `PR_SET_CHILD_SUBREAPER` · pytest 새 세션 · timeout 때 그룹 + /proc ppid 자손 SIGKILL · pytest 먼저 회수 뒤 고아 회수 · 끝에서 살아 있는 자손이 5 s 안에 스스로 끝나는지 관측 (넘으면 SIGKILL → killed · 미완) · Git 기록 | 없음 (timeout 경로는 정적 검토 · 정상 경로의 잔존 0 은 RED · GREEN 에서 관측) |
| N6 | E1-0 한정 승인 · RED / GREEN 정확한 argv · cwd · env · helper · 첫 실패 중지 (RED 24 모두 NotImplementedError · GREEN `-x`) · 첫 시험 전 봉인 · 활동 범위 셋 · 새 총수 24 / 51 | — |
| S1 (자체) | c5 가 경로로 실행하는 `reil_c6_profile.py` · env_identity 가 실행하는 `env_profile.py` 를 launcher 가 사전 · 사후 재해시 · env_profile 고정값을 C6 봉인 (MANIFEST → lock → 머리줄) 에 결속 · 다섯 모듈 · SOURCES 불변 | l17 · l1 |

## 3. 밝힐 것 (요청서 §8 의 요지)

1. 외곽 실행기의 timeout 경로는 시험하지 않는다 (정적 검토).
2. 탐침의 find_spec 결속은 탐침 시점 파일 시스템 — 자식 import 까지의 TOCTOU 는 사후 재해시 · `IDENTITY.json` 결속이 잡지만 연속 감시는 아니다.
3. /proc 관측 오류는 그룹 밖 프로세스라도 unknown (보수적) · 좀비는 살아 있는 것으로 세지 않는다.
4. Git 출처 확인은 설정 · rewrite · 받은 저장소의 원격 · shallow 까지 — TLS · 프록시의 실제 연결 호스트는 관측하지 않는다.
5. S1 의 두 파일은 run 의 `IDENTITY.json` 표에 없다 (run 코드 불변).
6. pytest 해석기에 `-X pycache_prefix` 를 더했다 (E0 · N1 의 GREEN 과 다름).

## 4. 질문

- Q1. N1–N6 각 정정이 지적을 닫는가 — 특히 N1 의 find_spec 결속이 "검사 중 대상 실행 0 · 부모 import 0" 을 지키면서 개별 모듈 가림을 막는가.
- Q2. S1 처리 (launcher 쪽 결속 · 봉인 lock 결속 · 다섯 모듈 · SOURCES 불변) 를 받아들일 수 있는가.
- Q3. 대조 24 · RED 선언 (24 실패 · 모두 NotImplementedError) · GREEN 51 · 외곽 실행기 timeout 경로의 무시험 (밝힘) 이 충분한가. 빠진 음성 대조가 있는가.
- Q4. E1-0 한정 승인으로 넘어가도 되는가 (요청서 §4 의 절차 · 명령 · 기준).
- Q5. §7 의 E1-1–3 고정 계획에서 E1-0 결과 검토 전에 더 고정해야 할 것이 있는가.

## 5. 경계

이 발송은 실행 지시가 아닙니다. launcher · 실행기 · 시험 · 탐침 · 읽기 경로 · fetch · 자료 개봉 · run · C4-A / B · COMSOL 은 모두 0 회이고, E1-0 은 이 사전 검토
뒤 사용자의 별도 승인이 있어야만 시작합니다. E1-0 승인은 E1-1–3 을 허용하지 않습니다.

---

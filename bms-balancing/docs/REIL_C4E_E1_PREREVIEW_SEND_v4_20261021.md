# Codex 발송 프롬프트 — REIL C4-E · E1 승인 요청 v4 (E1-0 한정) 사전 검토 · 2026-10-21 KST

> v3 ultra 사전 검토 회신 (상태 문서 §78 — 정정 필요 V3-01–04 · 문구 V3-N1) 과 사용자의 정정 범위 v4 채택 (§79 · V3-04 = A) 에 따라 쓴 비활성 초안과 수정
> 승인 요청이다. 아래 `---` 사이가 붙여 넣을 본문이다. 같이 첨부할 것은 없다 (검토자가 저장소에서 읽는다).

---

첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

REIL C4-E · E1 승인 요청 v4 를 사용자 승인 전에 사전 검토해 주세요. 지난 회신 (§78) 의 V3-01–04 · V3-N1 과 자체 발견 S5 를 반영한 **비활성 초안 다섯과
수정 승인 요청**입니다. 승인 대상은 여전히 **E1-0 뿐**이고, FUTURE-01 은 E1-1–3 요청의 선행 조건 (E1-0b) 으로 그대로 두었습니다. 초안 작성은 사용자의 범위
v4 채택 (§79) 뒤에 했고, 정적 검사 (AST 파싱 · 이름 검사 · ruff pyflakes 규칙 · 골격 상수 · 서명 일치 · 대조가 쓰는 이름 · 봉인 표와 실제 바이트 · 비밀
검사) 만 했습니다. launcher · 실행기 · 시험 · driver · 탐침 · 읽기 경로 · fetch · run 은 모두 0 회입니다. 브랜치 `claude/14-gate-code-review-9qkx05` 의 최신
HEAD (이 발송문이 든 커밋) 를 기준으로 보시면 됩니다.

## 1. 볼 것

| 파일 (bms-balancing 기준) | sha256 | 무엇 |
|---|---|---|
| `docs/REIL_C4E_E1_APPROVAL_REQUEST_v4_20261021.md` | (이 커밋의 바이트) | 수정 승인 요청 — E1-0 한정 · 정정 대응표 · 실행기 정리 규칙 (§3-2) · 정확한 명령 셋 · RED-L / RED-R / GREEN 기준 · Git 없는 수동 기록 · 절차 Git 중지 조건 (§4-6) · 새 · 수정 대조의 입력 / 기대 / 이유 / 호출 경로 (§6) · E1-1–3 계획 · 밝힐 것 21 |
| `docs/REIL_C4E1_LAUNCHER_DRAFT_v4_20261021.py.txt` | `6584d2dc75303f10a61bf13c260074b9a089a7774f7311618ed1c12f11cd5aa8` | launcher v4 (stdlib · 실행 모듈 import 0) |
| `docs/REIL_C4E1_LAUNCHER_SKELETON_DRAFT_v4_20261021.py.txt` | `b3b56fe3a2aa62e06671b78bcf8cbd3a288fb5a969534bd82025657264f0245c` | RED 골격 (import · 상수 동일 · 함수 35 = NotImplementedError) |
| `docs/REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v4_20261021.py.txt` | `4ceb9bdb2a21975db483c726e603260142f7d495be7e602f97320a220e8109b8` | launcher 대조 27 |
| `docs/REIL_C4E1_RUNNER_CONTROLS_DRAFT_v2_20261021.py.txt` | `4d2e9ab47a65cab275529938ff123e6e450499501dc56e5405a58de3f1101897` | 외곽 실행기 대조 11 |
| `docs/REIL_C4E1_STEP_RUNNER_DRAFT_v4_20261021.py.txt` | `091daff02ec2887294de917a24b76c11ec0a6ff2e6def63c4c81a9f853e25960` | E1-0 외곽 실행기 v4 (봉인 표 EXPECT 포함) |
| `docs/REIL_C4E_E1_REVISION_SCOPE_v4_20261021.md` · 상태 문서 §78 · §79 | — | 정정 범위 v4 · 회신 접수 · 사용자 채택 |

## 2. 지적 ↔ 정정 (요청서 §2 · §3-2 의 요지)

| ID | 정정 | 대조 |
|---|---|---|
| V3-01 | 정리 기한은 run_step 이 정리 단계에 들어갈 때 한 번 만들고 cleanup 은 받기만 함 (`deadline` 필수) · 모든 루프가 관측 시작 **전에** `지금 < 기한` · 기한 뒤에는 그 관측 결과에 따른 즉시 동작 (회수 · SIGKILL) · 비차단 확인 (`poll` · `wait(0)`) · 기록만 · 관측 0 이거나 kill 뒤 재관측이 없으면 `unverified` · cleanup 안의 예외는 cleanup 이 잡아 같은 기한으로 비상 동작 (새 15 s 없음) · 복구는 같은 기한 · `times.cleanup_s` 는 정리 원점부터 | r3 (관측마다 0.05 s) · r9 (회신의 반례 — 6.95 s 시작 · 9 s 관측) · r10 (늦은 예외 두 사례) · r2 · r6 · r8 |
| V3-02 | launcher · 실행기 `entry_exists` (lstat — 끊어진 링크도 있음 · FileNotFoundError 만 없음) — 기록 파일 전부 · launcher pycache 폴더 | l12 · r7 (d′) |
| V3-03 | 실행기 `proc_table` · launcher `proc_members` — 바이트 읽기 · comm 해석 안 함 · 소멸만 건너뜀 · 그 밖 모든 읽기 예외와 파싱 · 디코딩 실패는 그 PID 의 오류 · 스캔 계속 | r11 · l27 |
| V3-04 | (A) 수동 Git 기록을 없앰 — `00_start.txt` · `04_end.json` 은 Git 없음 · 수동 porcelain 파일 둘 삭제 · 증거의 Git 상태는 실행기 기록만 · 절차 Git (add · commit · push · log) 앞에 셸 env 의 `GIT_*` 이름을 허용 목록과 대조 (밖이면 멈춤 · 고정 명령 · a 와 f 의 결과 기록 · b–e 도 같은 줄에서) | 절차 규칙 (요청서 §4-5 · §4-6) |
| V3-N1 | 실행기 `run_step` — 자식 전에 멈추는 이유마다 `errors` 항목 (prepare / SourceMismatch · prepare / SubreaperFailed · record / GitRecordFailed) | r7 (a) · (e) |
| S5 (자체) | launcher `git_run` · 실행기 `git` 의 `text=True` 에 `errors="replace"` (V3-03 과 같은 종류 — 엄격 디코딩 예외가 기록 밖으로) | l27 · r11 |

## 3. 새 대조 · 명령 · 예산

- launcher 대조 27 (v3 26 + l27 · l12 · l14 수정) · 외곽 실행기 대조 11 (v3 8 + r9 · r10 · r11 · r2 · r3 · r6 · r7 수정) · GREEN 65 = E0 21 + N1 6 + 27 + 11 —
  범위안 v4 의 계획 수와 같고, 늘어난 넷은 지적별 새 대조입니다. 새 · 수정 대조의 입력 · 기대 · 이유 · 호출 경로는 요청서 §6 의 표에 고정했습니다.
- 단계 셋 · 명령 · 예산은 v3 와 같습니다: `01_red_launcher` (골격 · 27 · 120 s) · `02_red_runner` (v2 실행기 바이트 · 11 · 120 s) · `03_green` (65 · `-x` ·
  600 s) — 각 정리 ≤ 15 s (공통 기한 · 넘을 수 있는 것은 기한 전에 시작한 관측 하나) + 기록 (git 넷 × ≤ 60 s · 해시 둘) · E1-0 전체 ≤ 2 h · driver 8 회
  (r6 1 · r7 6 · r8 1).
- RED 기준: RED-L 27 실패 모두 NotImplementedError · RED-R 11 실패 = r1 AssertionError (v2 의 empty — V2-01 재현) + r2 · r3 · r9 · r10 (`cleanup`) · r4
  (`base_env`) · r5 (`source_table`) · r6–r8 (`run_step`) · r11 (`observe`) AttributeError.

## 4. 밝힐 것 (요청서 §8 의 요지)

1. RED-R 의 열은 인터페이스 수준입니다 — 행동 재현은 r1 하나. 새 반례 대조가 **v3** 바이트에서 실패하는지는 시험하지 않습니다 (정적 판단만 적었습니다 — V3-01
   의 행동은 v3 에 `deadline` 인자가 없어 대조로 재현할 수 없음).
2. 정리 기한을 넘을 수 있는 것은 기한 전에 시작한 관측 하나이고, 그 관측의 길이에는 상한이 없습니다 (감시 스레드 없음).
3. launcher 의 정리 루프 (`run_child` · `group_status`) 는 이번 V3-01 정정 대상이 아닙니다 — E1-1–3 요청에서 정합니다.
4. 절차 Git 앞의 이름 확인은 셸 env 의 `GIT_*` 이름만 봅니다 (설정 파일 · 그 밖의 영향은 보지 않음 · 절차 Git 의 결과는 증거가 아님).
5. 정리 안의 예외는 `cleanup.errors` · ledger 에 남고 단계 수준 `errors` 에는 따로 넣지 않습니다 (runner_ok 는 끝 상태 unknown 으로 거짓). `SubreaperFailed` 는
   대조가 없습니다.

## 5. 질문

- Q1. V3-01 정정 (§3-2 의 일곱 규칙) 이 지적을 닫는가 — 특히 r3 · r9 · r10 의 정확 기대가 "관측 비용 0 아닌 시계 · 늦은 예외 · 새 15 s 없음" 으로 충분한가.
- Q2. V3-02 · V3-03 · S5 의 정정과 대조 (l12 · r7 d′ · l27 · r11) 가 충분한가.
- Q3. V3-04 A (수동 Git 기록 삭제 · 실행기 기록만 증거 · 절차 Git 이름 확인 · 허용 목록 · 시점) 가 지적을 닫는가.
- Q4. V3-N1 의 `errors` 항목 셋과 r7 (a) · (e) 가 충분한가 — 정리 안의 예외를 단계 수준 `errors` 에 넣지 않은 처리 (밝힐 것 5) 를 받아들일 수 있는가.
- Q5. RED-R 을 v2 바이트의 인터페이스 RED 로 두는 것 (밝힐 것 1) 이 충분한가, 아니면 v3 바이트 대상의 행동 재현 단계가 필요한가 — 필요하면 `UNDER_TEST` 허용
  형태 · 단계 · 예산이 바뀌는 범위 변경이라 사용자 채택이 먼저입니다.
- Q6. 새 대조 38 · RED 선언 · GREEN 65 · 예산으로 E1-0 한정 승인에 넘어가도 되는가.

## 6. 경계

이 발송은 실행 지시가 아닙니다. launcher · 실행기 · 시험 · driver · 탐침 · 읽기 경로 · fetch · 자료 개봉 · run · C4-A / B · COMSOL 은 모두 0 회이고, E1-0 은
이 사전 검토 뒤 사용자의 별도 승인이 있어야만 시작합니다. E1-0 승인은 E1-0b · E1-1–3 을 허용하지 않습니다.

---

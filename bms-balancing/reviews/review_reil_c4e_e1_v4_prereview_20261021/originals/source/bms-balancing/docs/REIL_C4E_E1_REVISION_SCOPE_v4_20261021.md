# REIL C4-E · E1 정정 범위안 v4 (사용자 채택 요청) — v3 ultra 사전 검토 V3-01–04 · V3-N1 · 2026-10-21 KST

> **범위 채택 요청이다 (초안 작성 · 실행 0).** v3 사전 검토 회신 (상태 문서 §78 · `reviews/review_reil_c4e_e1_v3_prereview_20261021/originals/`) 은
> `implementation_approval: false` — 정정 구현도 승인하지 않았다. 이 범위를 채택하신 뒤에만 비활성 초안 v4 · 승인 요청 v4 · 발송문 v4 를 쓴다. 채택해도 시험 ·
> driver · 탐침 · 읽기 경로 · fetch · run 은 시작하지 않는다.

## 0. 구조 — 바뀌지 않는다

- 흐름: 비활성 정정안 v4 → Codex 재검토 → **사용자의 E1-0 한정 승인** → E1-0 → 결과 검토 → E1-1–3 별도 요청 (FUTURE-01 · E1-0b 포함).
- 수용된 것은 그대로 둔다: 코드 경로의 Git 환경 연결 · TARGETS 14 · 단계별 EXPECT · 사전 · 사후 원천 해시 생성자 · 지정 준비 예외 포착 · N1 · S1 · E1-0 /
  E1-1–3 분리.

## 1. 지적별 정정

### V3-01 (P2) 정리 기한이 새 관측과 복구 경로까지 가지 않음

- **원인 (v3):** watch · timeout 루프가 관측을 먼저 시작하고 시간을 나중에 본다 — 기한이 지난 settle 에서도 첫 관측 · kill 뒤 관측을 시작하고, 정상 루프도 sleep
  으로 기한에 닿은 뒤 새 관측을 시작한다. cleanup 이 예외를 내면 run_step 이 cleanup 을 다시 불러 새 15 s 를 준다 (`cleanup_s` 는 첫 시도를 빼먹는다).
- **정정:**
  - **기한은 단계에 하나:** run_step 이 정리 단계에 들어갈 때 정리 원점과 절대 기한 (원점 + 15 s) 을 한 번 만들고 cleanup 에 넘긴다 (cleanup 은 기한을 스스로
    만들지 않는다 — 필수 인자). `cleanup_s` 는 run_step 이 그 원점부터 잰다.
  - **새 관측 · 대기는 기한 전에만 시작:** 모든 루프가 관측을 시작하기 **전에** `지금 < 기한` 을 본다. 그래서 기한을 넘을 수 있는 것은 기한 전에 시작한 관측
    하나뿐이다.
  - **기한 뒤에 허용하는 것 (명시):** 그 관측 결과에 따른 즉시 동작 (좀비 회수 · SIGKILL 보내기 — 기다리지 않는다) · 비차단 확인 (`poll` · `wait(0)`) ·
    기록. 새 관측 · sleep · 차단 대기는 하지 않는다.
  - **미완 기록:** 끝 상태 = empty (기한 전에 시작한 관측이 살아 있는 자손 0) · killed (kill 뒤 기한 전에 시작한 재관측이 0) · alive (마지막 관측에 생존) ·
    **unverified** (기한 때문에 확인 관측을 못 함 — 관측 0 이거나 kill 뒤 재관측 없음) · unknown (ledger 에 오류). runner_ok 는 empty 만.
  - **예외는 cleanup 안에서 같은 기한으로:** cleanup 이 안의 예외를 잡아 오류 · ledger 에 남기고, 같은 기한 안에서 비상 동작 (pytest 가 살아 있으면 그룹 SIGKILL ·
    남은 시간이 있으면 settle) 만 한다 — 새 15 s 는 없다. run_step 의 복구 경로는 정리가 시작되기 **전**의 예외에서만 정리를 처음 시작하고, 이미 만든 기한이
    있으면 그것을 쓴다.
- **대조 (정확한 기대 결과):**
  - r3 (수정): 가짜 시계가 **관측마다 시간을 쓴다** (관측 비용 0 아님) · 모든 관측 시작 < 기한 · 끝 ≤ 기한 + 관측 한 번 · 기존 (a) (b) (c).
  - r9 (새 · 회신의 정적 반례): 6.95 s 에 시작한 timeout 관측이 9 s 걸려 15.95 s 에 생존을 반환 → 그 자손에 SIGKILL (즉시 동작) · 그 뒤 새 관측 0 · settle 은
    관측 없이 unverified · `deadline_hit` · `wait(0)` 만.
  - r10 (새 · 늦은 예외): 기한 10 s 쯤에 관측이 예외 → cleanup 이 잡고 같은 기한으로 비상 동작 → unknown · 오류 기록 · 모든 관측 시작 < 원래 기한 · 총 정리
    시간 ≤ 15 s + 관측 한 번 (새 15 s 없음).

### V3-02 (P2) 끊어진 meta 링크가 "기존 기록" 거부를 통과

- **정정:** launcher · 실행기의 기존 항목 검사를 `Path.exists()` (대상을 따라감) 에서 **lstat 기반 `entry_exists`** 로 바꾼다 — 끊어진 심볼릭 링크도 "있음" 이고,
  없음 (FileNotFoundError) 만 false, 그 밖 lstat 오류는 그대로 올려 준비 오류로 남긴다. 대상: 단계 기록 파일 전부 · launcher 의 pycache 폴더.
- **대조:** l12 (수정) · r7 (d′ 새 사례) — `<단계>.meta.json` 을 없는 대상을 가리키는 링크로 두면 SystemExit · 아무것도 쓰거나 만들지 않음 · 자식 0.

### V3-03 (P2) /proc 디코딩 예외가 ledger 를 빠져나감

- **정정 (실행기 `proc_table` · launcher `proc_members` 둘 다):** 기본 읽기를 **바이트**로 바꾸고 comm (괄호 안) 은 해석하지 않는다 — UTF-8 이 아닌 이름도
  실패하지 않는다. PID 별 경계에서 소멸 (FileNotFoundError · ProcessLookupError) 만 건너뛰고, 그 밖 **모든** 읽기 예외 (권한 · I/O · 디코딩 등) 와 파싱 실패는
  그 PID 의 오류로 남기고 스캔을 계속한다 → 같은 스캔의 앞선 오류가 사라지지 않고 남은 자손 처리도 멈추지 않는다.
- **대조:** r11 (새 · 실행기) — 가짜 /proc: 한 PID 는 PermissionError · 한 PID 는 UnicodeDecodeError (주입) · 한 PID 는 비 UTF-8 comm 바이트 → 두 오류 모두
  ledger 에 · 나머지 표는 완성 · 기본 바이트 읽기는 오류 0 · 그 관측 뒤 정상 관측이 와도 끝 상태 unknown. l27 (새 · launcher) — 같은 입력으로
  `proc_members` 는 예외 없이 오류 둘 · 구성원 완성 · `group_status` unknown.
- **같은 종류 (자체 · S5):** Git 출력 디코딩 — launcher `git_run` · 실행기 `git` 의 `text=True` 는 엄격 디코딩이라 비 UTF-8 출력에서 예외가 기록 밖으로 나갈
  수 있다 → `errors="replace"`. l27 · r11 에 비 UTF-8 커밋 메시지를 읽는 사례를 더한다.

### V3-04 (P2) 수동 시작 · 끝 Git 기록이 정제 env 밖

- **정정 (권장 A — 수동 Git 기록을 없앤다):** 증거의 Git 상태 (HEAD · porcelain) 는 **외곽 실행기 기록만** 쓴다 (정제 env · 단계마다 시작 · 끝). 수동 기록은
  Git 을 부르지 않는 것만 남긴다 — `00_start.txt` = `date -u` · `df` · `sha256sum` (초안 다섯 + 복사본 넷) · `04_end.json` = 같은 것 + 단계 셋의 meta 요약
  (실행기가 쓴 HEAD 포함). `00_porcelain_start.txt` · `04_porcelain_end.txt` 는 목록에서 뺀다.
- **절차 Git (add · commit · push · log) 의 중지 조건:** 증거가 아닌 절차 명령도 단계 a 와 f 의 첫 git 직전에 셸 env 의 `GIT_*` **이름** 을 확인해 허용 목록
  (`GIT_ASKPASS` · `GIT_CONFIG_COUNT` · `GIT_CONFIG_KEY_<n>` · `GIT_CONFIG_VALUE_<n>` · `GIT_EDITOR` · `GIT_SSL_CAINFO` · `GIT_TERMINAL_PROMPT`) 밖이 하나라도
  있으면 멈춘다 (이름만 기록 · 값은 읽지 않음). 지금 셸에는 허용 목록 밖이 없다 (§78 — 이 관측에 기대지 않고 규칙으로 고정).
- **B (다른 길):** 외곽 실행기에 기록 전용 모드를 더해 수동 기록도 같은 정제 책임자가 만든다 — 코드 · 대조가 늘어난다.

### V3-N1 (P3) S4 의 first_error 문구

- **정정 (기록을 문구에 맞춘다):** 실행기가 자식 전에 멈추는 이유마다 `errors` 에도 항목을 넣는다 — 원천 해시 불일치 `prepare / SourceMismatch` · subreaper
  `prepare / SubreaperFailed` · 시작 Git 기록 `record / GitRecordFailed`. 그래서 `first_error` 가 늘 멈춘 이유를 가리킨다 (problems 의 상세는 그대로).
- **대조:** r7 (a) · (e) 에 `first_error` 의 phase · type 을 더한다.

## 2. 새 대조 · 총수 · RED 선언 (계획 — 초안에서 확정)

- **launcher 대조 27** = v3 26 (l12 수정) + **l27** (V3-03 · S5).
- **외곽 실행기 대조 11** = v3 8 (r3 · r7 수정) + **r9 · r10** (V3-01) + **r11** (V3-03 · S5). driver 실행은 r6 1 · r7 6 · r8 1 = 8 회 (계획).
- **GREEN 65** = E0 21 + N1 6 + 27 + 11 (건너뜀 0).
- **RED-L:** 골격에서 27 실패 · 모두 NotImplementedError. **RED-R:** v2 실행기에서 11 실패 — r1 AssertionError (V2-01 반례 재현) · r2 · r3 · r9 · r10
  AttributeError (`cleanup`) · r4 (`base_env`) · r5 (`source_table`) · r6–r8 (`run_step`) · r11 (`observe`).
- **예산:** 바뀌지 않음 — RED-L 120 s · RED-R 120 s · GREEN 600 s · 정리 ≤ 15 s (공통 기한 · 기한 전에 시작한 관측 한 번만 넘을 수 있음) + 기록 · E1-0 ≤ 2 h.

## 3. 바뀌는 파일 · 바뀌지 않는 파일

- **새 초안 (docs · 정적 검사만):** launcher v4 · RED 골격 v4 · launcher 대조 v4 · 외곽 실행기 대조 v2 · 외곽 실행기 v4 (봉인 표 다시) · 승인 요청 v4 · 발송문 v4.
  v1–v3 은 지우지 않는다 (v2 실행기 초안은 RED-R 대상 그대로).
- **바뀌지 않음:** 다섯 모듈 · SOURCES.json · `reil_c6_profile.py` · `env_profile.py` · 기존 시험 · 기존 증거 · 봉인 · N1 · S1 · 탐침 · Git 금지 키 · fetch
  사후 대조 · FUTURE-01 경계.

## 4. 정하실 것

1. **이 범위 채택** — 채택하시면 위 초안 · 요청서 v4 · 발송문 v4 까지 쓰고 멈춘다 (권장). 정적 검사만 하고 실행은 0 이다.
2. **V3-04** — **A 수동 Git 기록을 없애고 실행기 기록만 증거로 (권장 · 코드 변화 없음)** / B 외곽 실행기에 기록 전용 모드.

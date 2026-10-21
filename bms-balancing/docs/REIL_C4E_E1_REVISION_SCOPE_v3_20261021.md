# REIL C4-E · E1 정정 범위안 v3 (사용자 채택 요청) — v2 사전 검토 V2-01–05 · 미래 FUTURE-01 · 2026-10-21 KST

> **범위 채택 요청이다 (초안 작성 · 실행 0).** v2 사전 검토 회신 (상태 문서 §76 · `reviews/review_reil_c4e_e1_v2_prereview_20261021/originals/`) 은
> `correction_implementation_approved: false` — 정정 구현도 승인하지 않았다. 이 범위를 채택하신 뒤에만 비활성 초안 v3 와 수정 승인 요청 v3 를 쓴다. 채택해도
> 시험 · driver · 탐침 · 읽기 경로 · fetch · run 은 시작하지 않는다.

## 0. 승인 구조 — 바뀌지 않는다

- 회신의 권고 흐름 그대로: 비활성 정정안 v3 → 갱신 식별 · 계획 재검토 (Codex) → **사용자의 E1-0 한정 승인** → E1-0 → 결과 검토 → E1-1–3 별도 요청 · 승인.
- 수용된 것은 그대로 둔다: N1 (셋의 가림 정적 검사 · `find_spec` 결속 · l15 · l16) · S1 (실행 파일 둘 · 봉인 lock 결속 · l17) · N6 의 활동 범위 셋과
  E1-0 / E1-1–3 분리.

## 1. 지적별 정정

### V2-01 (P1) 외곽 실행기의 관측 오류 유실

- **원인 (v2 실행기):** `reap()` 가 `proc_table()` 의 오류를 버린다 (`:118`). settle 의 watch 는 reap 와 descendants 가 `/proc` 를 따로 읽어서, 두 번째 관측이
  정상 · alive 0 이면 empty 를 돌려준다 (`:138–151`). timeout 루프도 descendants 오류를 버린다 (`:208`).
- **정정:**
  - 실행기의 `/proc` 관측은 모두 `proc_table` 하나를 거친다. 그 오류 (목록 · 읽기 · 파싱) 와 회수 (`waitpid`) 오류 · kill 오류 (ProcessLookupError 밖) 를
    **단계 하나의 누적 기록 (ledger)** 에 `{where: timeout | settle | settle_after_kill, utc, error}` 로 쌓는다.
  - 반복마다 관측은 한 번이고, 그 표를 회수와 자손 판정에 같이 쓴다 (두 관측 사이의 불일치가 생기지 않는다).
  - 끝 상태: ledger 가 비어 있지 않으면 **unknown** — 뒤의 정상 empty 가 지우지 않는다. 첫 오류를 `first_observation_error` 로 남기고 runner_ok 는 false.
- **정확한 기대 결과 (새 대조):**
  - r1 — 회신의 반례 그대로: 첫 관측 오류 → 그 뒤 정상 빈 관측 → status unknown · 주입한 오류가 ledger 의 첫 항목.
  - r2 — timeout 경로의 관측 오류 → 뒤 관측이 정상이어도 unknown · 첫 항목 where = timeout.
  - r8 — 실제 프로세스 트리 (V2-03 아래).

### V2-02 (P1) 첫 Git 호출 전 환경 격리

- **정책 하나 (launcher `child_env` 와 같은 규칙):** 상속 env 에서 비밀 형태 이름 · `SSH_ASKPASS` · `GIT_SSL_CAINFO` 밖의 모든 `GIT_*` 를 빼고
  `GIT_TERMINAL_PROMPT=0` 을 넣는다. 뺀 이름만 기록한다 (값은 기록하지 않음).
- **적용 지점 — 각자의 첫 Git 호출 전부터:**
  - 외곽 실행기: 준비 단계에서 정제 env 를 먼저 만들고, 자기 Git 기록 (HEAD · porcelain) 과 pytest env 의 바탕으로 쓴다. 그래서 pytest 안의 기존 시험 ·
    새 대조 · fixture 의 git 이 모두 정제 env 를 상속한다.
  - launcher: 기록용 `git_out` 이 env 없이 원래 환경을 상속하던 것을, 준비에서 만든 정제 env 로 바꾼다 (탐침 · fetch 검사는 이미 정제 env 를 쓴다).
  - 새 대조의 fixture (`_tree()` 등 직접 부르는 git): launcher 와 독립인 정제 함수로 env 를 명시한다 — 모든 `GIT_*` 와 비밀 형태 이름을 빼고 설정도 격리한다
    (S3).
- **음성 대조:** l25 (launcher · fixture) · r4 · r6 (실행기). 다른 tmp 저장소를 가리키는 `GIT_DIR` · 허용 밖의 기존 쓰기 가능 폴더를 가리키는
  `GIT_OBJECT_DIRECTORY` · `GIT_INDEX_FILE` · `GIT_TRACE` 를 상속 env 에 넣고 → 표지 폴더가 비어 있음 · 다른 저장소 불변 · 기록 HEAD = fixture 저장소 ·
  뺀 이름 기록 · 자식이 본 `GIT_*` 는 허용 목록뿐.
- 회신이 허용한 "명시적 착수 차단" 대신 제거를 고른 이유: launcher 와 같은 규칙 하나로 두고 뺀 이름을 남기면, 상속값과 무관하게 같은 동작이 된다. 현재 세션
  env 에 어떤 `GIT_*` 가 있는지는 보지 않았다 (규칙이 그 값에 기대지 않는다).

### V2-03 (P2) 정리 15 s 와 코드 배정

- **정정 (권장 A — 요청한 15 s 안):** 외곽 실행기의 정리를 **공통 절대 기한 하나** (정리 시작 + 15 s) 아래 둔다.
  - timeout 경로: 그룹 SIGKILL → 자손 SIGKILL 반복 (최대 7 s · pytest 가 끝나고 살아 있는 자손이 없으면 바로 멈춤) → pytest 회수 대기 (남은 시간만 ·
    0.1 s 하한 없음) → 스스로 끝나기 관측 (최대 3 s) → 남으면 SIGKILL → 기한까지 재관측. 7 + 3 + 5 = 15.
  - 정상 경로: 스스로 끝나기 관측 (최대 3 s) → 남으면 SIGKILL → 기한까지 재관측.
  - 기한이 지나면 어떤 대기도 새로 시작하지 않는다. 기한 직전에 시작한 `/proc` 관측 한 번만 기한을 넘길 수 있다. 기한에 걸리면 `deadline_hit` 를 기록하고
    runner_ok 는 false.
  - 시간 경계 셋을 따로 기록한다: `child_s` (자식 시작 → 종료 또는 timeout 감지) · `cleanup_s` (정리 시작 → 끝 상태) · `records_s` (끝 Git 기록 · 원천
    해시). 정리 전에 계산하던 `elapsed_s` (`:220`) 는 없앤다.
  - 정리 뒤 기록은 15 s 밖의 별도 배정이다: Git 기록 호출 넷 (각 timeout 60 s · 시작 둘 · 끝 둘) · 원천 해시 두 번 · meta.
- **B (사용자가 고를 때만):** 10 + 5 + 5 = 20 s 를 그대로 두고 정리 예산을 20 s 로 바꾼다. 예산 변경이라 권하지 않는다 — 검토자도 자동 확대는 승인하지 않았다.
- **대조:** r3 (가짜 시계 — 끝나지 않는 자손 → 기한 안 반환 · `deadline_hit` · alive · 어떤 대기도 그 시점의 남은 시간보다 길지 않음 / 스스로 끝나는 자손 →
  empty · kill 0 / 3 s 뒤 kill 로 끝나는 자손 → killed) · r8 (실제 트리 — 새 세션 자식 + 다른 세션 손주 · driver 가 subreaper · timeout → 둘 다 정리 ·
  empty · `exited_after_kill` · `cleanup_s` ≤ 15 · runner_ok false).
- **launcher (S2):** 정리 대기 배정은 그대로 둔다 (§7 의 20 s = 10 + 5 + 5). `elapsed_s` 만 대기 · 정리로 나눠 기록한다.

### V2-04 (P2) 준비 예외

- **launcher:** 준비 (pycache · mpl · tmp 폴더 · 정제 env · argv · 자기 읽기 · 해시 · 디스크 조회) 를 기록되는 단계 `prepare` 안으로 옮긴다.
  - 의도된 거부 (단계 이름 · 기존 기록 파일 · 기존 pycache 폴더) 는 지금처럼 **어떤 파일 · 폴더도 만들기 전에** SystemExit 로 끝낸다 (메시지 · 쓰는 것 0 ·
    자식 0). 기록용 `except Exception` 은 SystemExit 를 잡지 않으므로 둘이 섞이지 않는다.
  - 그 밖의 준비 예외 → `errors[0] = {phase: prepare, …}` · `launched` false · 자식 0 · meta (새 파일) · 반환 1. meta 를 쓸 수 없으면 stderr 에 JSON 한 줄
    (`step` · `meta_write_failed` · `first_error` · `launched` false · `complete` false) · 반환 4 — 원 오류가 그 줄에 남는다.
- **외곽 실행기도 같은 형태:** 반환 0 (runner_ok AND pytest rc 0) · 1 (meta 있음 · 그 밖 — RED 의 정상 결과 포함) · 3 (자식 시작 전에 멈춤 — 준비 예외 ·
  subreaper · 원천 해시 불일치 · 시작 Git 기록 실패 · meta 있음) · 4 (meta 를 쓸 수 없음 · stderr JSON). 의도된 거부는 SystemExit (해석기 rc 1 · 쓰는 것 0).
- **대조:** l26 (launcher — work 자리가 파일 → prepare · launched false · 반환 1 / 디스크 조회 OSError → prepare / 준비 예외 + meta 불가 → 반환 4 · stderr 의
  `first_error.phase` = prepare) · r7 (실행기 — 같은 셋 + 원천 해시 불일치 → 반환 3 · 자식 0 + 기존 기록 파일 → 거부 · 새 파일 0).

### V2-05 (P2) 단계별 원천 해시 기록

- **생성 주체 = 외곽 실행기** (수동 아님).
- **대상 = 실행기에 고정한 목록 14 (저장소 기준 경로):** `bms-balancing/scripts/reil_c4e1_launch.py` · 대조 둘 (`tests/test_reil_c4e1_launch.py` ·
  `tests/test_reil_c4e1_runner.py`) · 기존 시험 둘 (`test_reil_c4e.py` · `test_reil_c4e_fix.py`) · 다섯 모듈 · S1 의 둘 (`scripts/reil_c6_profile.py` ·
  `degradation-degeneracy/tools/env_profile.py`) · `evidence/reil_c4e0_fix_20261014/04_sources/SOURCES.json` · v2 실행기 초안
  (`docs/REIL_C4E1_STEP_RUNNER_DRAFT_20261020.py.txt` — RED-R 대상). 실행기 자신은 줄에 남기되 대조 밖이다 (자기 해시를 자기 안에 둘 수 없다 — 결과 검토에서
  요청서 표와 대조).
- **기대값 = 실행기 안의 단계별 표 `EXPECT[단계]`** — 요청서 v3 의 sha 표와 같고, 첫 시험 전 커밋으로 봉인된다. 단계마다 다른 것은
  `scripts/reil_c4e1_launch.py` 하나 (RED 둘 = 골격 · GREEN = 고정 구현).
- **시점 · 파일 · 실패 기준:**
  - 준비 끝 (자식 전): `<단계>.source_sha256.txt` (새 파일 · `sha256  경로` 줄) → `EXPECT` 와 하나라도 다르면 (없음 · 일반 파일 아님 · 링크 · 다른 바이트)
    자식 0 · 반환 3.
  - 끝 Git 기록 뒤: `<단계>.source_sha256_end.txt` → `EXPECT` 와 다르면 runner_ok false.
- **수동 기록 (나 · 고정 명령 — 요청서에 명령을 적는다):** `00_start.txt` (UTC · HEAD · 디스크 · 초안 / 복사본 sha) · `00_porcelain_start.txt` ·
  `04_porcelain_end.txt` · `04_end.json`.
- **대조:** r5 (해시 표 · 대조 함수) · r6 (두 파일의 정확한 줄) · r7 (불일치 → 자식 0).

## 2. 회신 밖 (자체 발견) — 같이 고칠 것

- **S2 — launcher 의 같은 형태:** `run_child` 의 `elapsed_s` 도 그룹 관측 전 값이다 → `wait_s` · `cleanup_s` 로 나눠 기록한다 (대기 배정 변화 없음).
- **S3 — fixture git 의 설정 격리:** 새 대조의 fixture git 은 `GIT_CONFIG_NOSYSTEM=1` · `GIT_CONFIG_GLOBAL=/dev/null` · `git init --template=` 으로 사용자 ·
  시스템 설정의 조건부 포함 · 훅 · 템플릿이 tmp 저장소에 걸리지 않게 한다 (FUTURE-01 의 E1-0 쪽 짝). 설치된 git 은 2.43.0 이다 (버전 문자열만 읽음 ·
  `GIT_CONFIG_GLOBAL` 은 2.32 부터). 기존 E0 시험 (수용된 바이트) 의 git 은 바꾸지 않는다 — env 제거는 실행기가 적용하고, 설정 노출은 밝힌다.
- **S4 — 시작 Git 기록 실패 시 자식 0 (회신 §5 의 언급에서):** 지금은 시작 기록이 실패해도 자식을 띄운 뒤 사후 false 로 둔다. launcher · 실행기 모두 시작 기록이
  실패하면 자식을 띄우지 않는다 — run 단계라면 3 시간을 헛되이 쓰지 않는다. 대조 l21 의 기대를 "launched false · 자식 0 · stage false" 로 바꾼다.

## 3. 미래 FUTURE-01 (E1-2 한정)

- **권장: 이번 v3 에 넣지 않는다.** 회신대로 E1-0 범위를 넓히지 않고, v3 고정본으로 E1-2 를 실행할 수 있다고 적지 않는다.
- **E1-1–3 요청에서 고칠 방향:** fetch 자식의 git 설정 원천을 launcher 가 고정한다 — `GIT_CONFIG_NOSYSTEM=1` · `GIT_CONFIG_GLOBAL=/dev/null` · 필요한 키만
  launcher 가 `GIT_CONFIG_COUNT` / `KEY` / `VALUE` 로 (예: 지금 사용자 설정의 `http.proxyAuthMethod` — 필요 여부는 그 요청에서 확인). 사전 검사는 같은 env 로
  `config --list --show-origin` 을 읽어 "command line" 원천만 허용하고, 사후 검사는 `data/git` 의 로컬 설정을 허용 목록과 대조한다. 파일 설정을 읽지 않으므로
  gitdir · onbranch · `hasconfig:remote.*.url` (git 2.43 에 있다 — remote 를 더한 뒤에야 걸리는 조건) 조건부 포함이 걸릴 수 없다.
- 그 launcher 차이는 E1-1–3 승인의 첫 단계 (E1-0b · RED / GREEN) 로 시험하고 첫 실패에서 멈춘다.
- **다른 길 — v3 에 지금 넣기:** E1-0 한 번에 시험되지만 이번 검토 범위가 커지고, l23 (사용자 설정 거부) 의 설계가 "격리" 로 바뀐다.

## 4. 새 대조 · 총수 · 명령 · 예산 (계획 — 초안에서 확정)

- **launcher 대조 26** = v2 24 (fixture · l19 · l21 수정 · 상수가 바뀌면 l14) + **l25** (V2-02) + **l26** (V2-04).
- **실행기 대조 8 (새 파일 `tests/test_reil_c4e1_runner.py`):** r1–r5 는 프로세스 안 (가짜 `/proc` 표 · 가짜 시계 · 가짜 kill / waitpid · tmp 로컬 git) ·
  r6–r8 은 driver 하위 프로세스 (`-I -B -X pycache_prefix`) 가 실행기 모듈을 경로로 적재해 `run_step` 을 tmp 경로로 부른다 (r8 은 실제 자식 + 다른 세션 손주 ·
  driver 가 subreaper).
- **시험할 실행기 파일** = env `REIL_C4E1_RUNNER_UNDER_TEST` (argv 의 `/usr/bin/env` 로 고정). RED-R 은 v2 초안
  (`docs/REIL_C4E1_STEP_RUNNER_DRAFT_20261020.py.txt` · `aae2ec14…`) · GREEN 은 `<E0>/00_step_runner.py` (v3). 두 형태 밖이면 수집 오류로 멈춘다.
- **E1-0 단계 (외곽 실행기 v3 가 모두 감싼다 · cwd = bms-balancing):**

  | 단계 | 무엇 | timeout | 기대 |
  |---|---|---|---|
  | `01_red_launcher` | 골격 + launcher 대조 26 | 120 s | 26 failed · 모두 `NotImplementedError: E1-0 RED 골격` |
  | `02_red_runner` | v2 실행기 + 실행기 대조 8 | 120 s | 8 failed · r1 = AssertionError (empty ≠ unknown — V2-01 반례가 v2 바이트에서 재현) · r2–r8 = AttributeError (v3 인터페이스 없음) |
  | `03_green` | 고정 구현 + E0 21 + N1 6 + 26 + 8 (`-x`) | 600 s | 61 passed |

  - 각 단계: 정리 ≤ 15 s (공통 기한) · Git 기록 넷 × ≤ 60 s · 원천 해시 둘. runner_ok = 시작 성공 AND timeout 없음 AND 끝 상태 empty (관측 · 회수 · kill 오류
    0 포함) AND 기한 안 AND 시작 · 끝 Git 기록 성공 · HEAD 불변 AND 원천 해시 = `EXPECT` AND 단계 오류 0.
  - E1-0 전체 ≤ 2 h (변화 없음) · 재시도 0 · 예산 변경 0.
- **RED-R 이 v2 바이트를 시험하는 이유:** 회신의 V2-01 반례가 지금 고정본에서 실제로 재현되는지 (r1) 를 보이고, v3 에서 닫힌 것을 GREEN 으로 보인다. 나머지
  일곱은 인터페이스 수준 RED 다 (N1 정정의 "AttributeError 3 + TypeError 3" 과 같은 종류).
- **활동 범위 (v2 §5 에 더함):** 실행기 대조 8 — 가짜 `/proc` · 가짜 시계 · tmp 로컬 git (init · 빈 커밋 · rev-parse · status) · driver 의 실행기 모듈 적재
  (최상위 정의만 · `main` 미실행) · prctl subreaper · stdlib 가짜 자식 · 다른 세션 손주 · SIGKILL / RED-R — v2 실행기 초안 모듈 적재 (최상위 정의만). 우리
  실행 모듈 다섯 import · 실제 자료 · optimizer · 네트워크는 새 대조 34 에 없다.

## 5. 바뀌는 파일 · 바뀌지 않는 파일

- **새 초안 (docs · 정적 검사만):** launcher v3 · RED 골격 v3 (초안에서 정적 변환) · launcher 대조 v3 · 실행기 대조 (새) · 외곽 실행기 v3 · 승인 요청 v3 ·
  사전 검토 발송문 v3. v1 · v2 는 지우지 않는다 (v2 실행기 초안은 RED-R 의 대상 바이트다).
- **초안 순서:** launcher → 골격 → launcher 대조 → 실행기 대조 → 외곽 실행기 (앞의 sha 를 `EXPECT` 에 넣는다) → 요청서 → 발송문.
- **바뀌지 않음:** 다섯 모듈 · SOURCES.json · `reil_c6_profile.py` · `env_profile.py` · 기존 시험 · 기존 증거 · 봉인 · N1 · S1 설계 · 탐침 · Git 금지 키 ·
  fetch 사후 대조.

## 6. 정하실 것

1. **이 범위 채택** — 채택하시면 위 초안 v3 · 요청서 v3 · 발송문 v3 까지 쓰고 멈춘다 (권장). 정적 검사만 하고 실행은 0 이다.
2. **V2-03 정리 예산** — **A 공통 기한 15 s (권장 · 예산 변경 없음)** / B 20 s 로 변경.
3. **FUTURE-01** — **E1-1–3 요청으로 미룸 (권장 · 그 승인의 첫 단계 E1-0b 로 시험)** / v3 에 지금 넣기.

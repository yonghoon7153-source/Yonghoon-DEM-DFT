# REIL C4-E · E1 정정 범위안 (사용자 채택 요청) — 사전 검토 N1–N6 + 자체 발견 S1 · 2026-10-15 KST

> **범위 채택 요청이다 (초안 작성 · 실행 0).** 사전 검토 회신 (상태 문서 §74 · `reviews/review_reil_c4e_e1_prereview_20261015/originals/`) 이
> "정정 작성도 사용자의 범위 채택을 따른다" 고 했으므로, 이 범위를 채택하신 뒤에만 비활성 초안과 수정 승인안을 쓴다. 채택해도 시험 · 탐침 · 읽기 경로 ·
> fetch · run 은 시작하지 않는다.

## 0. 바뀌는 승인 구조

- 이전 요청 (`9869cf5e`) 의 "E1-0 → E1-4 한 번의 승인" 권장은 **철회한다**.
- 새 순서 (회신의 권고 그대로):
  1. 정정한 비활성 초안 + 수정 승인안 → 2. Codex 사전 검토 → 3. **사용자의 E1-0 한정 승인** (launcher 대조의 RED · GREEN 만) → 4. E1-0 결과 검토 →
  5. 실제 E1-1–3 (identity · 읽기 경로 · fetch · run) 의 승인 요청 · 검토 · 사용자 별도 승인.
- 수정 승인안은 **"E1-0 승인 요청"** 이다. E1-1–3 의 명령 · 판정 · 예산도 같은 문서에 고정해 두되 승인 대상이 아니라고 적는다.

## 1. 항목별 정정 범위

### N1 (P1) 개별 모듈 가림

- **탐침 확장 (실행 0):** 지금의 `-c` 탐침 (json · sys · importlib.machinery 만) 이 자식과 같은 상태 (bms-balancing 을 sys.path[0] 에 넣은 상태) 를 만든 뒤,
  `sys.meta_path` 의 finder 를 차례로 `find_spec(이름, 경로)` 로만 묻는다 — `scripts` 와 패키지 import 되는 셋 (`scripts.reil_c4_e3a` · `scripts.reil_c4_monitor` ·
  `scripts.reil_c5_pilot`). 경로 목록을 명시해 묻기 때문에 부모 패키지를 import 하지 않고, 어떤 모듈도 실행하지 않는다.
- **사전 대조 조건:** finder = PathFinder · `scripts` = 네임스페이스 (loader 없음) 이고 첫 위치 = `bms-balancing/scripts` · 셋 각각 origin = 승인 `.py` 의 절대
  경로 · loader = SourceFileLoader · 패키지 아님.
- **정적 검사 (함께):** `bms-balancing/scripts/` 에 셋 이름의 `<이름>/__init__*` 폴더 · 확장 모듈 (`<이름>.cpython-311-x86_64-linux-gnu.so` · `.abi3.so` · `.so`
  — FileFinder 는 확장을 `.py` 보다 먼저 고른다) 이 없을 것.
- 경로로 실행되는 셋 (`reil_p0.py` · `reil_c6_profile.py` — c5 의 `_sibling` · `env_profile.py` — `lock_text`) 은 정확한 파일 경로를 SourceFileLoader 로 읽으므로
  패키지 가림이 걸리지 않는다 — 바이트 대조 + `-X pycache_prefix` 로 결속한다.
- **새 대조 (계획):** 승인 `.py` 옆에 `reil_c4_e3a/__init__.py` (실행되면 표식을 남기게 만든 것) → 사전 실패 · 표식 없음 (탐침이 실행하지 않음) · 자식 0 /
  같은 이름 확장 파일 → 사전 실패 · 자식 0 / 양성 — 셋의 origin · loader 가 기대대로.

### N2 (P1) 관측 불능을 "잔존 없음" 으로 바꾸지 않기

- `/proc` 관측을 (구성원, 오류) 로 돌려준다. PID 소멸 (FileNotFoundError · ProcessLookupError) 만 "사라짐" 이고, 권한 · I/O · 파싱 오류와 `/proc` 목록 실패는
  오류로 기록한다.
- 그룹 상태 = empty / alive / unknown. **관측 창 안에서 오류가 한 번이라도 나면 unknown 이 끝까지 남는다** (뒤의 정상 관측 · rc 0 으로 지우지 않음). 사후 대조는
  empty 일 때만 통과. 관측한 PID · 오류 · 순서를 기록하되 실제 발생 순서를 추정하지 않는다.
- 대조 l11 의 손주 판정기도 고친다 — FileNotFoundError 만 "없음" · 좀비는 "좀비" · 그 밖 OSError 는 시험 실패.
- **새 대조:** 권한 오류 주입 → unknown · stage false / 파싱 불능 → unknown / 소멸 → 사라짐 / 목록 실패 → unknown / 오류 뒤 정상 관측 → 여전히 unknown.

### N3 (P1) 유한한 정리와 실패 기록

- 종료 요청 (killpg) 의 결과를 기록한다 (성공 · 이미 없음 · 권한 · 그 밖). kill 뒤 대기는 **제한된 시간** (계획: 10 s) — 넘으면 "미종료" 로 기록하고 기다림을
  멈춘다. 정상 종료 뒤 그룹 관측 5 s · 잔존이 있으면 다시 kill 뒤 5 s 재관측. 미종료 · unknown 은 stage false.
- 정리 관측 기한 (≤ 20 s) 을 단계 예산에 더한다 (예: run 10,800 + 20 s). 숫자는 기다림의 상한이지 OS 가 그 안에 끝낸다는 보장이 아니다.
- launch 를 단계 (준비 · 사전 대조 · 시작 · 대기 · 정리 · 사후 대조 · 기록) 로 나누고 각 단계 예외를 잡아 **최초 오류 (단계 · 종류 · 메시지) 를 보존**한다 (뒤의
  오류는 덧붙임). `launched` 는 자식 시작이 성공한 뒤에만 참. meta 는 finally 에서 새 파일로 쓴다. meta 를 쓸 수 없으면 stderr 한 줄 + rc 4 로 한계를 분리한다.
- `read_regular` 의 읽기 예외를 사유로 돌려준다. Git 기록 (HEAD · porcelain) 은 rc · 오류를 남기고, 실패하면 사후 대조 문제 (stage false) 로 둔다.
- **새 대조:** kill 실패 주입 + 계속 도는 자식 → 제한 시간 안에 반환 · `미종료` · kill 오류 기록 · stage false (시험이 자식을 따로 정리) / 사전 대조 · 자식 시작 ·
  사후 대조 예외 주입 → 단계 · 최초 오류 · `launched` 가 맞게 기록 / Git 기록 실패 → stage false. 양성 경로는 tmp 의 로컬 git 저장소 (init + 빈 커밋 하나 ·
  네트워크 0) 를 쓴다.

### N4 (P2) Git 환경 경로와 실제 출처

- child_env 의 Git 변수를 **허용 목록**으로 바꾼다 — `GIT_SSL_CAINFO` 만 두고 `GIT_TERMINAL_PROMPT=0` 을 넣는다. `GIT_DIR` · `GIT_WORK_TREE` ·
  `GIT_COMMON_DIR` · `GIT_OBJECT_DIRECTORY` · `GIT_ALTERNATE_OBJECT_DIRECTORIES` · `GIT_INDEX_FILE` · `GIT_TRACE*` · `GIT_EXEC_PATH` · `GIT_PROXY_COMMAND` ·
  `GIT_SSH*` · `GIT_CONFIG*` · `GIT_ASKPASS` 등 나머지 `GIT_*` 는 모두 뺀다 (이름만 기록). `SSH_ASKPASS` 도 뺀다.
- **fetch 사전 대조 (네트워크 0):** 자식 env · 작업 폴더 cwd 로 `git config --list --show-origin` — `url.*.insteadOf` · `url.*.pushInsteadOf` · http(s) proxy 키 ·
  `core.gitProxy` · credential helper 가 있으면 거부. `git ls-remote --get-url <고정 URL>` (rewrite 를 적용한 URL 만 출력 · 원격 접속 없음) = 고정 URL.
- **fetch 사후 대조:** `data/git/.git/FETCH_HEAD` 첫 줄 = 고정 커밋 · 고정 URL · `git -C data/git ls-remote --get-url origin` = 고정 URL ·
  `objects/info/alternates` 없음. `GIT_ALLOW_PROTOCOL=https` 는 프로토콜 제한일 뿐 호스트 제한이 아니라고 적는다.
- **새 대조:** Git 경로 변수 제거 확인 / 가짜 HOME 의 `.gitconfig` 에 insteadOf → fetch 사전 실패 · 자식 0 / 가짜 fetch 가 다른 URL 의 FETCH_HEAD 를 쓰면 →
  사후 실패. 이 대조는 tmp 안의 로컬 `git config` · `git ls-remote --get-url` · `git init` 만 쓴다 (네트워크 0).

### N5 (P2) E1-0 외곽 실행기의 하위 프로세스 소유

- N1 정정의 실행기를 그대로 쓰지 않고 **E1-0 전용 외곽 실행기 새 바이트를 초안으로 고정**한다:
  - pytest 를 새 세션으로 띄운다 · 실행기가 `PR_SET_CHILD_SUBREAPER` (ctypes · Linux) 를 켠다 — 켜지 못하면 시작하지 않고 기록한다.
  - timeout 이면 pytest 그룹과 `/proc` 의 ppid 로 찾은 모든 자손 (별도 세션 포함 — 고아는 실행기로 재부모화된다) 을 SIGKILL 하고, 제한된 시간 동안 종료를
    확인한다. pytest 를 먼저 회수한 뒤 고아를 회수한다 (회수 순서가 rc 를 덮지 않게).
  - 정상 종료 뒤에도 살아 있는 자손 0 을 확인한다 (N2 와 같은 오류 구분). 잔존 · unknown 은 단계 incomplete.
- 실행기의 timeout 경로는 대조로 시험하지 않는다 (정적 검토 · 밝힘). 정상 경로의 "잔존 0" 관측은 RED · GREEN 에서 실제로 한다.

### N6 (P2) 승인 범위와 명령

- 수정 승인안은 E1-0 한정이고, 활동 범위를 셋으로 나눈 표를 둔다:

  | 범위 | 포함 | 제외 |
  |---|---|---|
  | 새 launcher 대조 N | launcher 함수 · tmp 가짜 자식 · 손주 · 해석기 탐침 · tmp 로컬 git | 우리 실행 모듈 import · 실제 자료 · optimizer · 네트워크 |
  | 전체 GREEN (27 + N) | 위 + E0 21 · N1 6 — 실제 모듈 import (→ `reil_c6_profile` · `reil_p0` 경로 실행 포함) · 합성 run 2 · fork · 가짜 로컬 저장소 fetch · plan_e | 실제 원자료 · optimizer · 네트워크 fetch |
  | 실제 E1-1–3 | identity (`env_profile` 실행 포함) · 읽기 경로 · 고정 출처 fetch · 원자료 개봉 · 66 호출 run | E1-0 승인으로 자동 허용되지 않음 |

- RED · GREEN 의 정확한 argv · cwd · env · helper (pytest 경로) · 실행기 경로와 sha · timeout · 정리 기한을 고정한다. 해석기에 `-X pycache_prefix=<새 빈 폴더>` 를
  더한다.
- **첫 실패 중지:** RED — 새 N 이 모두 NotImplementedError 로 실패하지 않으면 (통과 · 다른 예외) 멈춘다. GREEN — `pytest -x` · 하나라도 실패하면 그 자리에서
  멈춘다.
- **첫 시험 전 봉인:** 대조 · 골격 · 외곽 실행기 · helper 복사본을 RED 전에 커밋한다. fixture 생성 규칙 · 고정 입력 · 기대값은 봉인된 대조 파일 안에 있다. 끝
  기록의 diff 로 사전 고정을 대신하지 않는다.
- 새 총수를 확정해 적는다 (시험 함수 하나 = 사례 하나 · 같은 입력 안의 assertion 은 따로 세지 않음). "run · 우리 모듈 import 0" 은 새 launcher 대조에만,
  "plan-e · legacy 를 쓰지 않음" 은 실제 E1-1–3 에만 쓴다.

### S1 (자체 발견) 신뢰 목록 밖의 실행 파일 둘

- `scripts/reil_c6_profile.py` (`408afc4b…` · 15,915 B) — c5 import 때 `_sibling` 으로 실행 · `degradation-degeneracy/tools/env_profile.py` (`83b0d836…` ·
  22,333 B) — `c5.env_identity` → `prof.lock_text()` 로 실행 (identity · run 의 prepare).
- **권장 처리:** launcher 가 두 파일을 고정값으로 사전 · 사후 대조한다 (일반 파일 · resolve 일치 · 크기 · sha). env_profile 의 고정값은 C6 봉인 lock 머리줄
  (`reil_c6_rebuild_20261013/REIL_C6.lock.txt` · MANIFEST 가 덮음) 의 기록값과도 정적으로 대조한다. 다섯 모듈 · SOURCES.json 은 바꾸지 않는다. run 의 IDENTITY
  표에는 두 파일이 없다 (run 코드를 바꾸지 않으므로 · 밝힘).
- **다른 처리:** 신뢰 목록을 일곱으로 다시 봉인 — run 의 `MODULE_RELPATHS` (5 → 7) 를 고쳐야 하므로 새 정정 라운드 (RED · GREEN · 재봉인 · 재검토) 가 든다.
- **새 대조:** 두 파일 중 하나의 바이트가 다르면 사전 실패 · 자식 0.

## 2. 바뀌는 파일 · 바뀌지 않는 파일

- **새 초안 (docs · 정적 검사만):** launcher v2 · RED 골격 v2 (초안에서 정적 변환) · 대조 v2 · E1-0 외곽 실행기 · 수정 승인안 (E1-0 승인 요청) · 사전 검토
  발송문. 이전 초안 (`9869cf5e`) 은 지우지 않는다 (덧붙임 · 새 이름에 v2).
- **바뀌지 않음:** 다섯 모듈 · SOURCES.json · `reil_c6_profile.py` · `env_profile.py` (degradation-degeneracy 쪽 파일 · 읽기만) · 기존 시험 · 기존 증거 · 봉인.

## 3. 대조 수 · 예산 (예상 — 초안에서 확정)

- 새 대조 N ≈ 22–25 (기존 14 의 정정 + N1–N4 · S1 의 새 사례). GREEN = 27 + N. 확정 수는 초안과 수정 승인안에 적는다.
- **채택 뒤 이번 작업:** 초안 작성 · 정적 검사 (AST 파싱 · 이름 검사 · 비밀 검사 · 골격 상수 일치) 만 · 실행 0.
- **E1-0 (나중 승인):** RED 120 s · GREEN 600 s · 외곽 정리 관측 ≤ 30 s 씩 · 전체 2 h (계획).
- **E1-1–3 (그 뒤 승인):** 이전 요청의 배정 (60 · 300 · 10,800 s) + 정리 관측 ≤ 20 s 씩 · 전체 6 h (계획).

## 4. 정하실 것

1. **이 정정 범위 채택** — 채택하시면 위 초안 여섯을 쓰고 사전 검토 발송문까지 만든 뒤 멈춘다 (권장).
2. **S1 처리** — **launcher 쪽 고정 (권장 · 다섯 모듈 · SOURCES 불변)** / 신뢰 목록 일곱으로 재봉인 (run 수정 · 새 정정 라운드).

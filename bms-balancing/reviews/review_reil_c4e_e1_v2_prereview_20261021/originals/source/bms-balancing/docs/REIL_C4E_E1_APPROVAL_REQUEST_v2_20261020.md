# REIL C4-E · E1 승인 요청 v2 — E1-0 (launcher 대조) 한정 승인 + E1-1–3 고정 계획 · 2026-10-20 KST

> **승인 요청문이다 (실행 0).** 이번 승인 대상은 **E1-0 뿐**이다 — launcher 대조의 RED · GREEN. E1-1–3 (identity · 읽기 경로 · fetch · run) 의
> 명령 · 판정 · 예산은 §7 에 고정해 두지만 **이 요청의 승인 대상이 아니다** (E1-0 결과 검토 뒤 별도 요청 · 사용자 별도 승인).
> 근거:
> - 상태 문서 §74 — E1 사전 검토 회신 (`reviews/review_reil_c4e_e1_prereview_20261015/originals/`): `CHANGES_REQUIRED_NO_EXECUTION` · N1–N6 · 권고 순서.
> - §75 — 사용자 정정 범위 채택 ("권고대로 진행") · 정정 범위 `docs/REIL_C4E_E1_REVISION_SCOPE_20261015.md` (N1–N6 + 자체 발견 S1 · S1 은 launcher 쪽 고정).
> - 이전 요청 v1 `docs/REIL_C4E_E1_APPROVAL_REQUEST_20261015.md` (`9869cf5e` · sha256 `702608405c4dd0ea…`) · v3 요청 §3–§4 (run 순서 · E1 규칙 · 수용 §65).
>
> v1 의 "E1-0 → E1-4 한 번의 승인" 권장은 **철회했다** (§74 · 범위안 §0). v1 초안 셋은 지우지 않는다 (덧붙임).
> 순서: 이 요청 → Codex 사전 검토 → **사용자의 E1-0 한정 승인** → E1-0 → 결과 검토 → E1-1–3 승인 요청 → 검토 → 사용자 별도 승인.

## 0. 요약

| 단계 | 내용 | 이 요청의 승인 대상 |
|---|---|---|
| **E1-0** | 외곽 실행기 · 대조 24 · 골격 복사 (첫 시험 전 봉인) → RED (새 24) → 고정 구현 복사 → GREEN (E0 21 + N1 6 + 새 24 = **51**) → 끝 기록 → 멈춤 | **예** |
| E1-1–3 | identity · 읽기 경로 (`add_repo`) · fetch · run 1 회 — launcher v2 경유 | 아니오 (§7 고정 계획 · 별도 승인) |

## 1. 고정 식별

### 1-1. 이번에 고정하는 초안 넷 (정적 검사만 · 실행 0)

| 초안 (bms-balancing 기준) | sha256 | bytes | E1-0 에서 복사할 곳 |
|---|---|---:|---|
| `docs/REIL_C4E1_LAUNCHER_DRAFT_v2_20261020.py.txt` — launcher v2 고정 구현 | `ab33844fbdaa4e6939871abec09953783cfccd7b4d32ee023ab8691cdb814398` | 47,030 | `scripts/reil_c4e1_launch.py` (GREEN 직전) |
| `docs/REIL_C4E1_LAUNCHER_SKELETON_DRAFT_v2_20261020.py.txt` — RED 골격 | `5617a16aa8b093bac485e0bf775109c77ba9699d43301cf503e783365798b362` | 13,404 | 같은 곳 (RED 때) |
| `docs/REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v2_20261020.py.txt` — 대조 24 | `c1dc5b4353fa97e29b988604b612c7f40e46d3562980bde40dfd4712e4fde4ea` | 41,093 | `tests/test_reil_c4e1_launch.py` |
| `docs/REIL_C4E1_STEP_RUNNER_DRAFT_20261020.py.txt` — E1-0 외곽 실행기 (N5) | `aae2ec14c4d652ef9a9e5b1c45bf52896d2234dce16eac77942911e596669fed` | 12,849 | `<E0>/00_step_runner.py` |

- 정적 검사: AST 파싱 넷 · 이름 검사 (`__file__` 외 미해결 0) · 골격의 import · 상수 구간 = 고정 구현 (문자 그대로) · 골격 함수 34 개 모두 NotImplementedError ·
  탐침 코드 (`PROBE`) 파싱 · 대조가 쓰는 `L.*` 이름이 모두 고정 구현에 정의됨 · 대조 24 개 모두 RED 표지 · 비밀 검사 0 건.
- 골격은 고정 구현에서 정적 변환으로 만들었다 (`make_skeleton_v2.py` — 모듈 머리 docstring 교체 · 최상위 함수 본문만 `NotImplementedError`).

### 1-2. 바뀌지 않는 것 (읽기 대조만)

- 실행 모듈 다섯 = 구현 커밋 `61b9037e5283419f9ee22129b9a851df06f20cb1` 의 바이트 · 신뢰 목록 `evidence/reil_c4e0_fix_20261014/04_sources/SOURCES.json`
  (1,100 B · `2a7b2b49b9809d1a9301398388894a1f7a73afb55acc1a5070e3f77ce0393d52`) — §71 · §72.
- **목록 밖 실행 파일 둘 (S1):** `bms-balancing/scripts/reil_c6_profile.py` (15,915 B · `408afc4bb5eb1069583b955e0eb6215bf48dd9259ad474c230549d1b3642df5d`) ·
  `degradation-degeneracy/tools/env_profile.py` (22,333 B · `83b0d8365d039d75050d087fe980ad7b64818686b699e5d06da1c0ad63148563`).
- **봉인 결속 (S1):** `reil_c6_rebuild_20261013/MANIFEST.json` (`4f12094897b53463…`) → 그 안의 `REIL_C6.lock.txt` 항목 (`ea91156cac99fac1…`) → lock 바이트 →
  머리줄에 env_profile sha256. 2026-10-20 에 읽기로 다시 확인했다 (넷 다 일치).
- identity helper `00_identity_c4.py` (`92bb3bca…`) · 자료 식별 (xlsx `fd50e095…` · util `3c19e45e…`) · venv `SP/reil_c4env/venv` (python 3.11.17) ·
  launcher · 실행기 해석기 `/usr/bin/python3.11 -I`. SP = `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad`.
- 기존 시험 · 기존 증거 · 봉인 · v1 초안 셋 · v1 요청서는 바꾸지 않는다.

## 2. 사전 검토 지적 ↔ 정정 · 대조

| ID | 정정 (어디서) | 대조 |
|---|---|---|
| **N1** 개별 모듈 가림 | `leaf_shadow_problems` (셋의 `<이름>/__init__*` · 같은 이름 확장 파일) · 탐침 확장 — 자식과 같은 상태 (bms-balancing 을 sys.path[0]) 에서 `sys.meta_path` finder 에 `find_spec` 만 물음 (경로 명시 · 부모 import · 대상 실행 0) · `spec_problems` (`scripts` = PathFinder 네임스페이스 · 셋 = PathFinder · SourceFileLoader · origin = 승인 `.py`) | l15 (패키지 — 표식으로 실행 0 확인) · l16 (확장) · l1 (양성) |
| **N2** 관측 불능 | `proc_members` (PID 소멸만 사라짐 · 권한 / I/O / 파싱 / 목록 오류는 오류) · `group_status` (empty / alive / unknown · 오류는 그 자리에서 unknown 으로 확정) · 대조 l11 의 판정기 (`_state` — FileNotFoundError 만 소멸) | l18 · l11 |
| **N3** 유한 정리 · 기록 | `kill_group` (결과 기록) · `run_child` (kill 뒤 `KILL_WAIT_S` 10 s · 그룹 관측 `GROUP_GRACE_S` 5 s · 남으면 다시 kill 뒤 5 s · 미종료 기록 · 무기한 대기 0) · `launch` (단계마다 예외 → `errors` · `first_error` · `launched` 는 시작 성공 뒤에만 · 오류가 있으면 판정 false · meta 를 못 쓰면 stderr + rc 4) · `read_regular` (읽기 오류를 사유로) · `record_problems` (HEAD · porcelain rc · 단계 중 HEAD 불변) | l19 · l20 · l21 |
| **N4** Git 경로 · 출처 | `child_env` (`GIT_SSL_CAINFO` 밖의 `GIT_*` 모두 제거 · `GIT_TERMINAL_PROMPT=0`) · `fetch_source_precheck` (`git config --list --show-origin` 의 URL 바꿈 · 프록시 · 자격 도우미 · TLS 검증 끔 거부 · `ls-remote --get-url` = 고정 URL · 원격 접속 0) · `fetch_source_postcheck` (`remote.origin.url` · 받은 저장소의 유효 출처 · `.git/shallow` = 고정 커밋 · alternates 없음 · FETCH_HEAD 는 기록만) | l22 · l23 · l24 · l13 (양성) |
| **N5** E1-0 외곽 timeout | E1-0 전용 외곽 실행기 (`PR_SET_CHILD_SUBREAPER` · pytest 새 세션 · timeout 때 그룹 + /proc ppid 자손 SIGKILL · pytest 먼저 회수 뒤 고아 회수 · 끝에서 살아 있는 자손이 5 s 안에 스스로 끝나는지 관측 → 끝나면 empty · 넘으면 SIGKILL 뒤 재관측 → killed (미완) / alive · 관측 오류 unknown · Git 기록) | 대조 없음 (§8 의 1) — 정상 경로의 잔존 0 은 RED · GREEN 에서 관측 |
| **N6** 범위 · 명령 | 이 요청 §4 (정확한 명령 · 첫 실패 중지 · 첫 시험 전 봉인) · §5 (활동 범위 셋) · §6 (새 총수 24 / 51) | — |
| **S1** 목록 밖 실행 파일 | `EXTRA_EXECUTED` · `seal_lock_problems` — 사전 · 사후 재해시 · env_profile 고정값의 봉인 결속 | l17 · l1 (양성) |

## 3. launcher v2 의 판정 경로 (요약 — 정본은 초안 docstring 과 코드)

1. **사전 대조 (세 자식 모두 앞 · 실패하면 자식 0):** 목록 · 다섯 모듈 · 실행 파일 둘 · 봉인 결속 · 셋의 가림 정적 검사 · 실행 스크립트 · 해석기 플래그 · 탐침 (플래그 ·
   sys.path 의 `scripts` 가림 · 적재 선택) · (run) 자료 두 파일 · (fetch) 자료 폴더 없음 · Git 설정 · 유효 출처.
2. **자식:** 새 세션 · `-I -B -X pycache_prefix=<새 빈 폴더>` · timeout → kill (결과) → `KILL_WAIT_S` → 미종료면 기다림 멈춤 · 그룹 관측 → 남으면 다시 kill → 재관측.
3. **사후 대조:** 다섯 모듈 · 실행 파일 둘 · (fetch · run) 자료 · (fetch) 받은 저장소 · (run) `IDENTITY.json` 결속 · pycache 0 · 그룹 empty · 미종료 0 · 자식 단계 오류 0 ·
   Git 기록 · HEAD 불변.
4. **단계 판정 = precheck_ok AND child_ok AND rc_0 AND timeout_false AND postcheck_ok** (+ 단계 오류 0). run 모듈의 `stage_verdict` (`:392–398`) 는 쓰지
   않는다 — 사전 대조를 포함하지 않는다.

## 4. E1-0 절차 (이 요청의 승인 대상)

### 4-1. 순서 · 배정

| # | 단계 | 배정 | 기대 | 어긋나면 |
|---|---|---|---|---|
| a | 승인 기록 § · 보존 규칙 (`evidence/reil_c4e1_0_<날짜>/** -text`) 커밋 → 착수 기록 (t0 · HEAD · 디스크 · 초안 sha) — 증거 폴더 · `SP/c4e1_steps` 가 이미 있으면 멈춤 | — | — | 멈춤 |
| b | **복사 셋 · 첫 시험 전 봉인:** 대조 → `tests/test_reil_c4e1_launch.py` · 골격 → `scripts/reil_c4e1_launch.py` · 실행기 → `<E0>/00_step_runner.py` · sha 대조 · 커밋 | — | sha 일치 | 멈춤 |
| c | **RED** (실행기 · 새 24 만) · 커밋 | pytest 120 s + 실행기 정리 ≤ 15 s | §4-3 RED 기준 | 멈춤 |
| d | 고정 구현 복사 (sha 대조) → **GREEN** (51 · `-x`) · 커밋 | pytest 600 s + 실행기 정리 ≤ 15 s | §4-3 GREEN 기준 | 멈춤 |
| e | 끝 기록 · 비밀 검사 · 커밋 · push · 결과 기록 § · 결과 검토 발송문 → **멈춤** | — | — | — |

- E1-0 전체 작업 (착수 기록 → 끝 기록) ≤ 2 h. 재시도 0 · 예산 변경 0. 끝 기록은 커밋 · push · 문서 전 snapshot 이다.
- `<E0>` = `/home/user/Yonghoon-DEM-DFT/bms-balancing/evidence/reil_c4e1_0_<착수 UTC 날짜 YYYYMMDD>` (E1-1–3 의 `reil_c4e1_<날짜>` 와 다른 폴더 · 실행기가
  이름 규칙을 확인한다).

### 4-2. 정확한 명령

```
실행기:  /usr/bin/python3.11 -I <E0>/00_step_runner.py 01_red   120 -- <RED argv>
         /usr/bin/python3.11 -I <E0>/00_step_runner.py 02_green 600 -- <GREEN argv>

RED argv:
  /usr/bin/env PYTHONPATH=SP/reil_c4env/pytest_t SP/reil_c4env/venv/bin/python -X pycache_prefix=SP/c4e1_steps/pycache/01_red
      -m pytest -p no:cacheprovider tests/test_reil_c4e1_launch.py -q -rA --tb=short
GREEN argv:
  /usr/bin/env PYTHONPATH=SP/reil_c4env/pytest_t SP/reil_c4env/venv/bin/python -X pycache_prefix=SP/c4e1_steps/pycache/02_green
      -m pytest -p no:cacheprovider -x tests/test_reil_c4e.py tests/test_reil_c4e_fix.py tests/test_reil_c4e1_launch.py -q -rA --tb=short
```

- cwd = `/home/user/Yonghoon-DEM-DFT/bms-balancing` (실행기가 고정).
- env (실행기가 만든다): 현재 env 에서 비밀 형태 이름 (TOKEN · SECRET · PASSW · ACCESS_KEY · CREDENTIAL · COOKIE · `GIT_CONFIG_*`) 을 뺀 것 (이름만 기록) +
  `PYTHONDONTWRITEBYTECODE=1` · `MPLBACKEND=Agg` · `MPLCONFIGDIR` · `TMPDIR` (`SP/c4e1_steps/{mpl,tmp}`) · `OMP` / `OPENBLAS` / `MKL_NUM_THREADS=1` ·
  `REIL_C4_FIX_EVIDENCE=<E0>` · `REIL_C4_FIX_STEP=<이름>`.
- helper: pytest 는 `SP/reil_c4env/pytest_t` (E0 · N1 과 같은 경로 · PYTHONPATH). 해석기에 `-X pycache_prefix=<새 경로>` 를 더해 소스 트리의 `__pycache__` 를
  읽지 않는다 (E0 · N1 의 GREEN 과 다른 점 · §8 의 10).

### 4-3. RED · GREEN 기준 — 첫 예상 밖 결과에서 멈춘다

- **RED:** pytest rc 1 · 요약 "24 failed" · 통과 0 · 수집 오류 0 · 짧은 요약의 실패 24 줄이 모두 `NotImplementedError: E1-0 RED 골격` · 실행기 meta 의
  `started` true · `timed_out` false · `end.status` "empty" · `records_ok` true. 하나라도 다르면 (통과 · 다른 예외 · 수집 오류 · 잔존 · 기록 실패) 멈춘다.
- **GREEN:** pytest rc 0 · 요약 "51 passed" · 실행기 meta 의 같은 네 조건. `-x` 로 pytest 가 첫 실패에서 멈추고, 실패가 하나라도 있으면 E1-0 을 멈춘다.
- 실행기의 `runner_ok` = 시작 성공 AND timeout 없음 AND 끝 상태 empty AND Git 기록 성공 · HEAD 불변. pytest rc 의 해석 (RED 는 rc 1 이 기대값) 은 이 절이 정한다.

### 4-4. 봉인 · 기록 · 제출

- **첫 시험 전 봉인:** 복사 셋을 RED 전에 커밋한다. fixture 생성 규칙 · 고정 입력 · 기대값은 봉인된 대조 파일 안에 있다. 끝 기록의 diff 로 사전 고정을 대신하지 않는다.
- **증거 폴더 (`<E0>`):** `00_start.txt` · `00_porcelain_start.txt` · `00_step_runner.py` · `01_red.{meta.json, stdout.log, stderr.log, porcelain_start.txt,
  porcelain_end.txt, source_sha256.txt}` · `02_green.*` (같은 이름) · `03_porcelain_end.txt` · `03_source_sha256_end.txt` · `04_end.json`.
- **커밋:** 증거 폴더 · `tests/test_reil_c4e1_launch.py` · `scripts/reil_c4e1_launch.py`. 커밋하지 않음: `SP/c4e1_steps/` (pytest tmp · mpl · pycache).
- 커밋 전: 비밀 검사 + URL 계정 정보 형태 검사 · 파일 하나 ≤ 50 MB.

## 5. 활동 범위 셋 (N6)

| 범위 | 포함 | 제외 |
|---|---|---|
| **새 launcher 대조 24** | launcher 함수 · tmp 가짜 run 스크립트 (stdlib) · 손주 sleep · 해석기 탐침 (`-c`) · tmp 안 로컬 git (init · 빈 커밋 · remote add · `config --list` · `ls-remote --get-url`) · 가짜 /proc 폴더 | 우리 실행 모듈 다섯 import · 실제 자료 · optimizer · 네트워크 |
| **GREEN 전체 51** | 위 + E0 21 · N1 6 — 실제 실행 모듈 import (`test_reil_c4e.py:28–31` · c5 import 때 `reil_c6_profile` · `reil_p0` 경로 실행 포함) · 로컬 Git / fetch 대조 (`:752–792`) · 합성 `run.run` 둘 (`:956–984`) · `plan_e` (`:987–` · `test_reil_c4e_fix.py:332–`) · fork 세션 | 실제 원자료 · 원 optimizer · 네트워크 fetch |
| **실제 E1-1–3** | identity (`env_profile` 실행 포함) · 읽기 경로 · 고정 출처 fetch · 원자료 개봉 · 66 호출 run | **E1-0 승인으로 허용되지 않는다** |

"우리 실행 모듈 import 0" 은 새 대조 24 에만, "plan-e · legacy 경로를 쓰지 않음" 은 실제 E1-1–3 에만 쓴다. 위 수는 소스가 계획한 활동이지 수행 횟수가 아니다.

## 6. 대조 24 · RED / GREEN 선언

| ID | 무엇을 막는가 |
|---|---|
| l1 | 양성 — 목록 · 다섯 · 실행 파일 둘 · 봉인 결속 · 플래그 · 섀도 없음 · `scripts` 네임스페이스 · 셋의 origin = 승인 `.py` · 자료 → 사전 통과 |
| l2 | 목록 sha · schema · 넷 · 목록 밖 · 대문자 · 음수 · bool · JSON 아님 → 각각 실패 |
| l3 | 모듈 +1 바이트 · 같은 크기 다른 바이트 · 없음 · 심볼릭 링크 · 링크된 상위 폴더 → 각각 실패 |
| l4 | sys.path 의 `scripts` 패키지 · 모듈 · zip · 빈 항목 · 우리 `scripts.py` · 우리 `scripts/__init__.py` → 실패 |
| l5 | 탐침 플래그 · argv 머리 · 실행 스크립트 경로 → 실패 |
| l6 | 단계 판정 다섯 항 AND (rc None / False / 2 / −9 · timeout True / None) |
| l7 | 자식 결과 — 마지막 줄 · run 은 `ok` AND `final.complete` |
| l8 | `IDENTITY.json` 결속 |
| l9 | 사전 실패 → 자식 0 · `launched false` · 로그 없음 |
| l10 | 통과 → 고정 argv · 자식 env 에 토큰 · `GIT_*` 없음 · 모든 항 참일 때만 complete · INCOMPLETE · 경로 결속 실패 → false |
| l11 | timeout → 손주까지 그룹 SIGKILL · 손주 상태 판정기 (소멸 / 좀비만 · 그 밖 읽기 오류는 시험 실패) |
| l12 | 기록 · pycache 재사용 거부 |
| l13 | 도중 모듈 변경 · fetch 틀린 바이트 → 사후 실패 · 고정 출처의 맞는 fetch → complete · 자료 폴더 재사용 → 사전 실패 |
| l14 | stdlib 만 · 동적 import · exec 0 · 고정 상수 · 세 argv 문자 그대로 · main 규칙 |
| l15 | (N1) 승인 `.py` 옆 같은 이름 패키지 → 사전 실패 · 자식 0 · 패키지 코드 실행 0 (표식) |
| l16 | (N1) 같은 이름 확장 모듈 → 사전 실패 |
| l17 | (S1) 실행 파일 둘의 바이트 · lock 머리줄 · MANIFEST 고정값 → 각각 실패 |
| l18 | (N2) 가짜 /proc — alive · 좀비만 empty · 권한 / 파싱 / 목록 오류 unknown · 소멸만 사라짐 · 첫 오류 확정 |
| l19 | (N3) kill 실패 + 계속 도는 자식 → 20 s 안에 돌아옴 · 미종료 · kill 결과 둘 · 그룹 alive · stage false (시험이 자식을 따로 정리) |
| l20 | (N3) 사전 대조 · 자식 시작 · 사후 대조 예외 → 단계 · 첫 오류 · `launched` 기록 |
| l21 | (N3) Git 기록 실패 → stage false |
| l22 | (N4) 자식 env 의 `GIT_*` 허용 목록 · 비밀 제거 |
| l23 | (N4) URL 바꿈 · 프록시 · TLS 끔 설정 → fetch 사전 실패 · 자식 0 · 깨끗하면 유효 출처 = 고정 URL |
| l24 | (N4) 받은 저장소의 다른 remote · 다른 shallow · alternates → 사후 실패 |

- **RED 선언:** 골격에서 **24 실패 · 모두 `NotImplementedError`** (각 시험이 골격 함수를 처음 부르는 지점).
- **GREEN 선언:** 고정 구현에서 **51 passed** (E0 21 + N1 6 + 새 24). 시험 함수 하나 = 사례 하나 (같은 함수 안의 여러 입력 · assertion 은 따로 세지 않는다).
- RED 는 인터페이스 수준이다. 틀린 구현을 잡는 근거는 GREEN 의 음성 대조 (l2–l5 · l9 · l11–l13 · l15–l24) 다.

## 7. E1-1–3 고정 계획 — **이 요청의 승인 대상이 아니다**

E1-0 결과 검토 뒤 별도 승인 요청을 낸다. 그때 바꾸지 않을 것을 지금 고정한다:

- **순서:** identity (E1-1) → 읽기 경로 `add_repo` (REIL-UConn/… · read) → fetch (E1-2) → run (E1-3) — 각 단계가 launcher v2 를 거치고, 첫 예상 밖 실패에서
  멈춘다 (v1 §5 와 같음).
- **launcher 호출 · 자식 argv:** v1 §3-1 · §3-2 와 같고, run 의 승인 문구만 `상태 문서 §NN (사용자 E1-1–3 승인 · docs/REIL_C4E_E1_APPROVAL_REQUEST_v2_20261020.md)`
  로 바뀐다 (대조 l14 가 문자 그대로 고정). 증거 폴더 = `evidence/reil_c4e1_<날짜>/` (E1-0 폴더와 다름) · identity helper 를 그 폴더에 복사.
- **env:** launcher v2 `child_env` (§2 N4). fetch 의 git 다섯 단계는 v1 §3-4 그대로 (run 모듈 코드 · 목록 sha 로 고정).
- **배정:** 자식 timeout identity 60 · fetch 300 · run 10,800 s · 탐침 ≤ 60 s · fetch 의 git 확인 ≤ 4 × 60 s · 정리 관측 ≤ 20 s (kill 대기 10 + 그룹 5 + 재관측 5 —
  숫자는 기다림의 상한이지 OS 종료 보장이 아니다) · 전체 6 h.
- **판정 · 중지 · 기록 · 제출 경계:** v1 §4–§6 그대로 + launcher v2 의 사후 대조 · 단계 기록 (§3). E1-0 승인은 이 단계를 허용하지 않는다.

## 8. 밝힐 것

1. 외곽 실행기의 timeout 경로 (그룹 · 자손 SIGKILL · 회수) 는 대조로 시험하지 않는다 — 정적 검토뿐이다. 정상 경로의 "살아 있는 자손 0" 은 RED · GREEN 에서
   실제로 관측한다.
2. 탐침의 find_spec 결속은 탐침 시점의 파일 시스템이다. 탐침과 자식 import 사이의 TOCTOU 는 남는다 — run 의 끝 재해시 · launcher 사후 재해시 · `IDENTITY.json`
   결속이 변화를 잡지만 연속 감시는 아니다.
3. 관측 오류는 보수적으로 unknown 이다 — 그룹 밖 프로세스의 /proc 읽기 오류도 unknown 으로 만든다 (소속을 알 수 없으므로). 좀비는 살아 있는 것으로 세지 않는다.
4. Git 출처 확인은 설정 · rewrite · 받은 저장소의 원격 · shallow 까지다. TLS 와 프록시가 실제로 어느 호스트에 연결했는지는 관측하지 않는다 (agent proxy 정책
   범위). `.git/shallow` 와 FETCH_HEAD 의 내용은 git 동작에 기대며, FETCH_HEAD 는 기록만 한다.
5. S1 의 두 파일은 run 의 `IDENTITY.json` 표에 없다 (run 코드 불변) — launcher 의 사전 · 사후 재해시와 봉인 결속이 결속한다.
6. 해석기 · stdlib · site-packages · `sitecustomize` · `.pth` 는 launcher 대조 밖이다 (C4-ENV identity · 봉인 MANIFEST 의 범위). 탐침은 sitecustomize 경로 ·
   meta_path 이름을 기록만 한다.
7. 12,060 s 와 §7 의 숫자는 timeout · 기다림의 합이지 전체 소요 보증이 아니다. 자원은 사후 관측이다.
8. GREEN 51 에는 기존 E0 21 · N1 6 의 활동 (§5) 이 포함된다.
9. 대조 l19 는 kill 이 실패한 자식을 시험이 직접 정리한다 (`os.killpg`). 그 좀비들은 pytest 가 끝난 뒤 외곽 실행기 (subreaper) 가 회수한다.
10. pytest 해석기에 `-X pycache_prefix=<새 경로>` 를 더했다 — E0 · N1 의 GREEN 과 다르다. 기존 `scripts/__pycache__/` 는 지우지 않는다.
11. launcher · 실행기는 자기 sha 를 기록할 뿐 스스로 검증하지 않는다 — 고정값 대조는 착수 · 끝 기록의 sha 표와 결과 검토에서 한다.
12. v1 요청서 · v1 초안 셋은 그대로 둔다 (지난 검토의 근거 바이트).

## 9. 하지 않는 것

E1-1–3 (identity · 읽기 경로 · fetch · 자료 개봉 · run) · C4-A / B · E3b · H4 · pickle · 노트북 · 출판 비교 · 해 선택 · 재시도 · 실행 중 예산 변경 · 설치 · 환경
재구축 · 원자료 커밋 · 대체 출처 · COMSOL. 다섯 모듈 · 목록 · 기존 시험 · 기존 증거 · 봉인은 바꾸지 않는다.

## 10. 정하실 것

1. **사전 검토** — 이 요청과 초안 넷을 Codex 에 보낸다 (권장 · 발송문 `docs/REIL_C4E_E1_PREREVIEW_SEND_v2_20261020.md`).
2. (검토 수용 뒤) **E1-0 한정 승인** — 승인해도 E1-1–3 은 시작하지 않는다.

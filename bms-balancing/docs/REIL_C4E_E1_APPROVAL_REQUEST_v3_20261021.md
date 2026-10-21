# REIL C4-E · E1 승인 요청 v3 — E1-0 (launcher · 외곽 실행기 대조) 한정 승인 + E1-1–3 고정 계획 · 2026-10-21 KST

> **승인 요청문이다 (실행 0).** 이번 승인 대상은 **E1-0 뿐**이다 — launcher 대조와 외곽 실행기 대조의 RED · GREEN. E1-1–3 (identity · 읽기 경로 · fetch ·
> run) 은 §7 에 고정 계획만 둔다 (**승인 대상 아님** · E1-0 결과 검토 뒤 별도 요청 · 사용자 별도 승인).
> 근거:
> - 상태 문서 §76 — v2 사전 검토 회신 (`reviews/review_reil_c4e_e1_v2_prereview_20261021/originals/`): `CHANGES_REQUIRED_NO_EXECUTION` · 정정 V2-01–05 ·
>   미래 E1-2 한정 FUTURE-01 · N1 · S1 · 승인 범위 분리 수용.
> - §77 — 사용자 정정 범위 채택 ("권고대로") · 정정 범위안 v3 `docs/REIL_C4E_E1_REVISION_SCOPE_v3_20261021.md` (V2-03 은 A — 공통 기한 15 s · FUTURE-01 은
>   E1-1–3 요청으로).
> - 이전 요청 v2 `docs/REIL_C4E_E1_APPROVAL_REQUEST_v2_20261020.md` (`0e4fbbde`) · 정정 범위 `docs/REIL_C4E_E1_REVISION_SCOPE_20261015.md` (§75).
>
> 순서: 이 요청 → Codex 사전 검토 → **사용자의 E1-0 한정 승인** → E1-0 → 결과 검토 → E1-1–3 승인 요청 → 검토 → 사용자 별도 승인. v1 · v2 요청서와 초안은
> 지우지 않는다 (v2 실행기 초안은 이번 RED-R 의 대상 바이트다).

## 0. 요약

| 단계 | 내용 | 이 요청의 승인 대상 |
|---|---|---|
| **E1-0** | 복사 넷 (첫 시험 전 봉인) → RED-L (골격 + launcher 대조 26) → RED-R (v2 실행기 + 실행기 대조 8) → 고정 구현 복사 → GREEN (E0 21 + N1 6 + 26 + 8 = **61**) → 끝 기록 → 멈춤 | **예** |
| E1-1–3 | identity · 읽기 경로 (`add_repo`) · fetch · run 1 회 — launcher 경유 · FUTURE-01 정정 (E1-0b) 이 먼저 | 아니오 (§7 · 별도 승인) |

## 1. 고정 식별

### 1-1. 이번에 고정하는 초안 다섯 (정적 검사만 · 실행 0)

| 초안 (bms-balancing 기준) | sha256 | bytes | E1-0 에서 복사할 곳 |
|---|---|---:|---|
| `docs/REIL_C4E1_LAUNCHER_DRAFT_v3_20261021.py.txt` — launcher v3 고정 구현 | `124a154dfbd662aaa49fcf21327bf48a08e190da5bd9d02ae28cf86072b71503` | 49,873 | `scripts/reil_c4e1_launch.py` (GREEN 직전) |
| `docs/REIL_C4E1_LAUNCHER_SKELETON_DRAFT_v3_20261021.py.txt` — RED 골격 (함수 34) | `b77c6aa87cb7468063c258665a6b85765eab9f04e2607eb856444362b7374030` | 13,501 | 같은 곳 (RED 둘) |
| `docs/REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v3_20261021.py.txt` — launcher 대조 26 | `f00ba0fb9e333fe77cae275507203e8ced086d6e80d6c08a7aec5d98860ce002` | 46,977 | `tests/test_reil_c4e1_launch.py` |
| `docs/REIL_C4E1_RUNNER_CONTROLS_DRAFT_20261021.py.txt` — 외곽 실행기 대조 8 (새) | `555263464f2eddad1df1b1f9d201c947e990d026bb29bc4c95a74256c2a0ddfc` | 25,328 | `tests/test_reil_c4e1_runner.py` |
| `docs/REIL_C4E1_STEP_RUNNER_DRAFT_v3_20261021.py.txt` — E1-0 외곽 실행기 v3 | `7454a0de4e221945958e1a99ab4a3f44a5eb7808f2b8c5997f7a82d5f097fbf3` | 29,995 | `<E0>/00_step_runner.py` |

- 정적 검사 (실행 0): AST 파싱 다섯 · 이름 검사 (`__file__` 외 미해결 0) · 골격의 import · 상수 61 문 = 고정 구현 (AST 동일) · 함수 34 의 이름 · 서명 동일 ·
  골격 본문 모두 `NotImplementedError("E1-0 RED 골격 …")` · launcher 대조가 쓰는 `L.*` 이 모두 고정 구현에 정의됨 · 실행기 대조가 쓰는 `R.*` 이 모두 v3 에
  정의됨 · 그중 r2–r8 의 첫 줄이 쓰는 이름은 v2 에 없음 · 실행기의 봉인 표 (`EXPECT` — 열넷 · 단계 셋) = 위 초안 넷 · 저장소 HEAD 의 기존 파일 열하나의
  실제 바이트 (불일치 0) · 비밀 검사 0 건.
- 골격은 고정 구현에서 정적 변환으로 만들었다 (`make_skeleton_v3.py` — 머리 docstring 교체 · 최상위 함수 본문만 `NotImplementedError`). 실행기의 봉인 표는
  초안 넷을 확정한 뒤 자리표시를 그 sha256 · bytes 로 바꿔 채웠다 (`fill_runner_v3.py` — 정적 치환).

### 1-2. 바뀌지 않는 것 (읽기 대조만)

- 실행 모듈 다섯 = 신뢰 목록 `evidence/reil_c4e0_fix_20261014/04_sources/SOURCES.json` (1,100 B · `2a7b2b49b9809d1a9301398388894a1f7a73afb55acc1a5070e3f77ce0393d52`)
  의 바이트 (§71 · §72). 기존 시험 `tests/test_reil_c4e.py` (57,482 B · `687de63c…`) · `tests/test_reil_c4e_fix.py` (19,506 B · `7a09d438…`).
- S1 의 둘 `scripts/reil_c6_profile.py` (15,915 B · `408afc4b…`) · `degradation-degeneracy/tools/env_profile.py` (22,333 B · `83b0d836…`) · 봉인 결속
  (MANIFEST `4f120948…` → lock `ea91156c…` → 머리줄) — §75 와 같다.
- v2 실행기 초안 `docs/REIL_C4E1_STEP_RUNNER_DRAFT_20261020.py.txt` (12,849 B · `aae2ec14…`) — RED-R 이 시험하는 바이트.
- 다섯 모듈 · 목록 · 기존 시험 · 기존 증거 · 봉인 · v1 · v2 요청서 · 초안은 바꾸지 않는다. SP = `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad`.

## 2. 지적 ↔ 정정 · 대조

| ID | 정정 (어디서) | 대조 |
|---|---|---|
| **V2-01** 외곽 실행기 관측 오류 유실 | 실행기 v3 `proc_table` (모든 /proc 관측의 한 곳) · `observe` (오류를 단계 하나의 `ledger` 에 {where · utc · error} 로 쌓음) · `reap` / `kill` (회수 · kill 오류도 ledger) · `settle` / `cleanup` (반복마다 관측 1 회 — 같은 표로 회수 · 자손 판정 · ledger 가 비어 있지 않으면 끝 상태 unknown · 뒤의 정상 empty 가 지우지 않음 · `first_error`) | r1 (회신의 반례 그대로 — RED-R 에서 v2 가 empty 를 내는 것을 재현) · r2 · r8 |
| **V2-02** 첫 Git 호출 전 환경 격리 | 실행기 `base_env` (launcher `child_env` 와 같은 규칙 — 비밀 형태 · SSH_ASKPASS · GIT_SSL_CAINFO 밖의 GIT_* 제거 · GIT_TERMINAL_PROMPT=0 · 준비의 첫 동작 · 자기 Git 기록과 pytest env 의 바탕) · 실행기 `git(…, env)` (기본값 없음) · launcher `git_out(…, env)` (기본값 없음 · 준비에서 만든 정제 env) · 대조 둘의 fixture `_git_env()` (launcher 와 독립 · 모든 GIT_* · 비밀 형태 제거 + 설정 격리 — S3) | l25 · r4 · r6 |
| **V2-03** 정리 15 s · 시간 경계 | 실행기 `cleanup` — 공통 절대 기한 하나 (정리 시작 + 15 s) · timeout 경로 7 + 3 + 5 · 정상 경로 3 + 12 · 어떤 sleep · wait 도 그 시점의 남은 시간을 넘지 않음 (pytest 회수 대기의 0.1 s 하한 없음) · 기한 직전에 시작한 /proc 관측 한 번만 넘을 수 있음 · 기한에 걸리면 `deadline_hit` · `child_s` · `cleanup_s` · `records_s` · `total_s` 를 따로 | r3 (가짜 시계) · r8 (실제 트리) |
| **V2-04** 준비 예외 | launcher `launch` — 준비 (pycache · mpl · tmp · 정제 env · argv · 자기 sha · 디스크) 를 기록 단계 `prepare` 안으로 · 의도된 거부는 만들기 전 SystemExit (`except Exception` 이 잡지 않음) · 끝 관측 (디스크 · 증거 바이트) 실패도 `end` 오류로 남기고 meta 는 씀 · meta 불가 → stderr JSON (first_error 포함) · 반환 4. 실행기 `run_step` 도 같은 형태 (반환 0 · 1 · 3 · 4) | l26 · r7 · l12 (거부 = 쓰는 것 0) |
| **V2-05** 단계별 원천 해시 | 실행기가 만든다 — 고정 목록 `TARGETS` 14 · 봉인 표 `EXPECT[단계]` (요청서 §4-4 의 표 · 첫 시험 전 커밋) · 준비 끝 (자식 전) `<단계>.source_sha256.txt` → 다르면 자식 0 · 반환 3 / 끝 기록 뒤 `<단계>.source_sha256_end.txt` → 다르면 runner_ok false | r5 · r6 · r7 |
| **S2** (자체) launcher 시간 | `run_child` 의 `elapsed_s` (그룹 관측 전 값) → `wait_s` · `cleanup_s` (대기 배정 변화 없음) | l19 |
| **S3** (자체) fixture git 설정 | 대조 둘의 fixture git 은 `GIT_CONFIG_NOSYSTEM=1` · `GIT_CONFIG_GLOBAL=/dev/null` · `git init --template=` — 읽기로 확인한 사용자 설정 키 이름에 `commit.gpgsign` · `gpg.format` · `gpg.ssh.program` · `user.signingkey` 가 있다 (값은 읽지 않음). v2 fixture 의 빈 commit 은 그 설정에 따라 서명 프로그램을 부를 수 있었다 | 모든 fixture · l25 |
| **S4** (자체 · 회신 §5) 시작 기록 실패 | launcher · 실행기 모두 시작 HEAD · porcelain 기록이 실패하면 자식을 띄우지 않는다 (launched false · 첫 오류 record · GitRecordFailed) | l21 (기대 바뀜) · r7 (e) |
| N1 · S1 · N6 범위 | 바뀌지 않음 (수용 범위) | l15 · l16 · l17 · l1 |

## 3. launcher v3 의 판정 경로 (요약 — 정본은 초안 docstring 과 코드)

0. **준비 (`prepare`):** 의도된 거부 (단계 이름 · 기존 기록 파일 · 기존 pycache 폴더) 는 아무것도 만들기 전 SystemExit. 그 밖 예외는 첫 오류 · launched false ·
   자식 0 · meta.
1. **사전 대조 (세 자식 모두 앞 · 실패하면 자식 0):** v2 와 같다 (목록 · 다섯 모듈 · 실행 파일 둘 · 봉인 결속 · 셋의 가림 · 실행 스크립트 · 플래그 · 탐침 ·
   (run) 자료 · (fetch) 자료 폴더 없음 · Git 설정 · 유효 출처).
2. **시작 기록 → 자식:** 시작 기록 실패면 자식 0 (S4). 자식은 새 세션 · `-I -B -X pycache_prefix=<새 빈 폴더>` · timeout → kill (결과) → `KILL_WAIT_S` →
   그룹 관측 → 남으면 다시 kill → 재관측 · `wait_s` · `cleanup_s`.
3. **사후 대조:** v2 와 같다 (다섯 모듈 · 실행 파일 둘 · 자료 · 받은 저장소 · IDENTITY 결속 · pycache 0 · 그룹 empty · 미종료 0 · 자식 단계 오류 0 · Git
   기록 · HEAD 불변).
4. **단계 판정 = precheck_ok AND child_ok AND rc_0 AND timeout_false AND postcheck_ok** (+ 단계 · 끝 관측 오류 0). 기록용 git 은 모두 정제 env 를 쓴다.

## 4. E1-0 절차 (이 요청의 승인 대상)

### 4-1. 순서 · 배정

| # | 단계 | 배정 | 기대 | 어긋나면 |
|---|---|---|---|---|
| a | 승인 기록 § · 보존 규칙 (`evidence/reil_c4e1_0_<날짜>/** -text`) 커밋 → `<E0>` 만들기 — `<E0>` · `SP/c4e1_steps` 가 이미 있으면 멈춤 | — | — | 멈춤 |
| b | **복사 넷 · 첫 시험 전 봉인:** 대조 둘 → `tests/` · 골격 → `scripts/reil_c4e1_launch.py` · 실행기 → `<E0>/00_step_runner.py` → `00_start.txt` · `00_porcelain_start.txt` (§4-5) → 복사본 sha = §1-1 확인 → 커밋 | — | sha 일치 | 멈춤 |
| c | **RED-L** `01_red_launcher` (실행기) · 커밋 | pytest 120 s + 정리 ≤ 15 s + 기록 | §4-3 | 멈춤 |
| d | **RED-R** `02_red_runner` (실행기) · 커밋 | pytest 120 s + 정리 ≤ 15 s + 기록 | §4-3 | 멈춤 |
| e | 고정 구현 복사 (sha 대조) → **GREEN** `03_green` (61 · `-x`) · 커밋 | pytest 600 s + 정리 ≤ 15 s + 기록 | §4-3 | 멈춤 |
| f | `04_porcelain_end.txt` · `04_end.json` (§4-5) · 비밀 검사 · 커밋 · push · 결과 기록 § · 결과 검토 발송문 → **멈춤** | — | — | — |

- **정리 ≤ 15 s** = 외곽 실행기의 공통 절대 기한 (정리 시작부터 · 기한 직전에 시작한 /proc 관측 한 번만 넘을 수 있다). **기록** = 단계마다 Git 호출 넷 (각
  timeout 60 s · 시작 둘 · 끝 둘) · 원천 해시 두 번 · meta — 정리 15 s 밖의 별도 배정이다.
- E1-0 전체 (착수 → 끝 기록) ≤ 2 h. 재시도 0 · 예산 변경 0. 끝 기록은 커밋 · push · 문서 전 snapshot 이다.
- `<E0>` = `/home/user/Yonghoon-DEM-DFT/bms-balancing/evidence/reil_c4e1_0_<착수 UTC 날짜 YYYYMMDD>` (E1-1–3 의 `reil_c4e1_<날짜>` 와 다른 폴더 · 실행기가
  이름 규칙을 확인한다).

### 4-2. 정확한 명령 (cwd 는 실행기가 bms-balancing 으로 고정 · BMS = `/home/user/Yonghoon-DEM-DFT/bms-balancing`)

```
실행기:  /usr/bin/python3.11 -I <E0>/00_step_runner.py 01_red_launcher 120 -- <RED-L argv>
         /usr/bin/python3.11 -I <E0>/00_step_runner.py 02_red_runner   120 -- <RED-R argv>
         /usr/bin/python3.11 -I <E0>/00_step_runner.py 03_green        600 -- <GREEN argv>

RED-L argv:
  /usr/bin/env PYTHONPATH=SP/reil_c4env/pytest_t SP/reil_c4env/venv/bin/python -X pycache_prefix=SP/c4e1_steps/pycache/01_red_launcher
      -m pytest -p no:cacheprovider tests/test_reil_c4e1_launch.py -q -rA --tb=short
RED-R argv:
  /usr/bin/env PYTHONPATH=SP/reil_c4env/pytest_t REIL_C4E1_RUNNER_UNDER_TEST=BMS/docs/REIL_C4E1_STEP_RUNNER_DRAFT_20261020.py.txt
      SP/reil_c4env/venv/bin/python -X pycache_prefix=SP/c4e1_steps/pycache/02_red_runner
      -m pytest -p no:cacheprovider tests/test_reil_c4e1_runner.py -q -rA --tb=short
GREEN argv:
  /usr/bin/env PYTHONPATH=SP/reil_c4env/pytest_t REIL_C4E1_RUNNER_UNDER_TEST=<E0>/00_step_runner.py
      SP/reil_c4env/venv/bin/python -X pycache_prefix=SP/c4e1_steps/pycache/03_green
      -m pytest -p no:cacheprovider -x tests/test_reil_c4e.py tests/test_reil_c4e_fix.py tests/test_reil_c4e1_launch.py tests/test_reil_c4e1_runner.py
      -q -rA --tb=short
```

- SP · BMS · `<E0>` 는 실제 명령에서 절대 경로로 풀어 쓴다 (위 표기는 줄임일 뿐이다).
- env (실행기가 만든다): 현재 env → `base_env` (비밀 형태 이름 · SSH_ASKPASS · GIT_SSL_CAINFO 밖의 모든 GIT_* 제거 · 이름만 기록 · GIT_TERMINAL_PROMPT=0) +
  `PYTHONDONTWRITEBYTECODE=1` · `MPLBACKEND=Agg` · `MPLCONFIGDIR` · `TMPDIR` (`SP/c4e1_steps/{mpl,tmp}`) · `OMP` / `OPENBLAS` / `MKL_NUM_THREADS=1` ·
  `REIL_C4_FIX_EVIDENCE=<E0>` · `REIL_C4_FIX_STEP=<단계>`. 실행기 대조가 시험할 파일은 argv 의 `/usr/bin/env` 가 정한다 — 값이 두 형태 밖이면 수집 오류로
  멈추고, 값이 없으면 그 파일 전체를 건너뛴다 (E1-0 단계 밖의 실행을 막지 않으려는 것 · 단계 안에서는 아래 기준의 skipped 0 이 깨져 멈춘다).
- helper: pytest 는 `SP/reil_c4env/pytest_t` (pytest 9.1.1 · E0 · N1 과 같은 경로). 해석기에 `-X pycache_prefix=<새 경로>` 를 더한다.

### 4-3. RED · GREEN 기준 — 첫 예상 밖 결과에서 멈춘다

공통 (실행기 meta): `started` true · `timed_out` false · `cleanup.status` "empty" · `cleanup.deadline_hit` false · `end_problems` 없음 · `errors` 없음 ·
`runner_ok` true. pytest rc 의 해석은 아래가 정한다.

- **RED-L (`01_red_launcher`):** pytest rc 1 · 요약 "26 failed" · 통과 0 · 건너뜀 0 · 수집 오류 0 · 짧은 요약의 실패 26 줄이 모두
  `NotImplementedError: E1-0 RED 골격`.
- **RED-R (`02_red_runner`):** pytest rc 1 · 요약 "8 failed" · 통과 0 · 건너뜀 0 · 수집 오류 0 · 짧은 요약: r1 = `AssertionError` (v2 의 settle 이 status
  "empty" 를 낸다 — 회신 V2-01 의 반례가 그 바이트에서 재현) · r2 · r3 = `AttributeError: module 'runner_under_test' has no attribute 'cleanup'` · r4 =
  `… 'base_env'` · r5 = `… 'source_table'` · r6 · r7 · r8 = `… 'run_step'`.
- **GREEN (`03_green`):** pytest rc 0 · 요약 "61 passed" (건너뜀 · xfail 0). `-x` 로 pytest 가 첫 실패에서 멈추고, 실패가 하나라도 있으면 E1-0 을 멈춘다.
- 하나라도 다르면 (통과 · 다른 예외 · 수집 오류 · 잔존 · 기한 · 기록 실패 · 원천 해시 불일치 · 실행기 반환 3 / 4) 멈춘다. 재시도하지 않는다.

### 4-4. 봉인 · 원천 해시 (V2-05)

- **첫 시험 전 봉인:** 복사 넷을 RED-L 전에 커밋한다 (b). fixture 생성 규칙 · 고정 입력 · 기대값은 봉인된 대조 파일 안에 있다. 끝 기록의 diff 로 사전 고정을
  대신하지 않는다.
- **생성 주체 = 외곽 실행기.** 대상 = `TARGETS` 14 (저장소 기준): `bms-balancing/scripts/reil_c4e1_launch.py` · `tests/test_reil_c4e1_launch.py` ·
  `tests/test_reil_c4e1_runner.py` · `tests/test_reil_c4e.py` · `tests/test_reil_c4e_fix.py` · 다섯 모듈 · `scripts/reil_c6_profile.py` ·
  `degradation-degeneracy/tools/env_profile.py` · `evidence/reil_c4e0_fix_20261014/04_sources/SOURCES.json` · `docs/REIL_C4E1_STEP_RUNNER_DRAFT_20261020.py.txt`.
- **기대값 = `EXPECT[단계]`** (실행기 v3 안 · §1-1 · §1-2 의 sha 와 같음) — 단계마다 다른 것은 launcher 자리 하나 (RED-L · RED-R = 골격 `b77c6aa8…` · GREEN =
  고정 구현 `124a154d…`).
- **시점 · 실패 기준:** 준비 끝 (자식 전) `<단계>.source_sha256.txt` (`sha256  경로` 줄 · 끝줄에 실행기 자신 — 대조 밖) → 하나라도 다르면 (없음 · 일반 파일
  아님 · 링크 · 다른 바이트) 자식 0 · 반환 3 / 끝 기록 뒤 `<단계>.source_sha256_end.txt` → 다르면 runner_ok false.

### 4-5. 기록 · 제출

- **증거 폴더 (`<E0>`):** 실행기가 단계마다 `<단계>.{meta.json, stdout.log, stderr.log, porcelain_start.txt, porcelain_end.txt, source_sha256.txt,
  source_sha256_end.txt}` · 나 (고정 명령) 가 `00_start.txt` · `00_porcelain_start.txt` · `04_porcelain_end.txt` · `04_end.json` · 복사본 `00_step_runner.py`.
- **수동 기록의 고정 명령:** `00_start.txt` = `date -u +%Y-%m-%dT%H:%M:%SZ` · `git -C /home/user/Yonghoon-DEM-DFT rev-parse HEAD` ·
  `df -B1 --output=avail /home/user/Yonghoon-DEM-DFT` · `sha256sum` (초안 다섯 + 복사본 넷) · `00_porcelain_start.txt` / `04_porcelain_end.txt` =
  `git -C /home/user/Yonghoon-DEM-DFT status --porcelain=v1 --untracked-files=all` · `04_end.json` = 같은 UTC · HEAD · 디스크 · 복사본 넷 sha256 · 단계 셋의
  meta 요약 (`runner_ok` · `rc` · `cleanup.status` · `times`).
- **커밋:** 증거 폴더 · `tests/test_reil_c4e1_launch.py` · `tests/test_reil_c4e1_runner.py` · `scripts/reil_c4e1_launch.py`. 커밋하지 않음: `SP/c4e1_steps/`.
- 커밋 전: 비밀 검사 + URL 계정 정보 형태 검사 · 파일 하나 ≤ 50 MB.

## 5. 활동 범위 셋

| 범위 | 포함 | 제외 |
|---|---|---|
| **새 대조 34 (launcher 26 + 실행기 8)** | launcher 함수 · tmp 가짜 run 스크립트 (stdlib) · 손주 sleep · 해석기 탐침 (`-c`) · tmp 안 로컬 git (init · 빈 커밋 · rev-parse · status · remote add · `config --list` · `ls-remote --get-url`) · 가짜 /proc 폴더 · 표지 GIT_* 와 다른 tmp 저장소 · 준비 실패 주입 / 실행기: 가짜 /proc 표 · 가짜 시계 · 가짜 kill / waitpid · driver 하위 프로세스 (`-I -B -X pycache_prefix` · 실행기 모듈 경로 적재 · `main` 미실행 · `run_step` 을 tmp 경로로 · prctl subreaper · stdlib 가짜 자식 · 다른 세션 손주 · SIGKILL) · RED-R 의 v2 실행기 초안 적재 (최상위 정의만) | 우리 실행 모듈 다섯 import · 실제 자료 · optimizer · 네트워크 |
| **GREEN 전체 61** | 위 + E0 21 · N1 6 — 실제 실행 모듈 import (c5 import 때 `reil_c6_profile` · `reil_p0` 경로 실행 포함) · 로컬 Git / fetch 대조 · 합성 `run.run` 둘 · `plan_e` · fork 세션 | 실제 원자료 · 원 optimizer · 네트워크 fetch |
| **실제 E1-1–3** | identity (`env_profile` 실행 포함) · 읽기 경로 · 고정 출처 fetch · 원자료 개봉 · 66 호출 run | **E1-0 승인으로 허용되지 않는다** |

"우리 실행 모듈 import 0" 은 새 대조 34 에만 쓴다. 위 수는 소스가 계획한 활동이지 수행 횟수가 아니다.

## 6. 대조 26 + 8 · RED / GREEN 선언

| ID | 무엇을 막는가 |
|---|---|
| l1–l18 · l20 · l22–l24 | v2 와 같다 (§2 · v2 요청서 §6) — fixture git 만 `_git_env()` 로 바뀜 |
| l12 | (V2-04) 기존 기록 · pycache 폴더 → SystemExit · 증거 폴더 · 작업 폴더에 아무것도 쓰거나 만들지 않음 |
| l14 | 승인 문구의 요청서 경로가 v3 |
| l19 | (N3 · S2) kill 실패 + 계속 도는 자식 → 20 s 안 · 미종료 · `wait_s` · `cleanup_s` 따로 · `elapsed_s` 없음 |
| l21 | (N3 · S4) 시작 기록 실패 → 자식 0 · launched false · 첫 오류 record (GitRecordFailed) · 로그 없음 |
| l25 | (V2-02) 표지 GIT_DIR (다른 저장소) · GIT_OBJECT_DIRECTORY · GIT_INDEX_FILE · GIT_TRACE → fixture · launcher 기록 · fetch 사전 · 사후 검사 · 가짜 fetch 의 git 이 표지 폴더에 쓰지 않음 · 다른 저장소 불변 · 기록 HEAD = fixture · fetch complete |
| l26 | (V2-04) 작업 폴더 자리가 파일 → prepare · launched false · 1 / 디스크 조회 OSError → prepare / 준비 실패 + meta 불가 → 4 · stderr JSON |
| r1 | (V2-01) 첫 관측 오류 → 정상 빈 관측 → unknown · 첫 항목 where settle (회신의 반례) |
| r2 | (V2-01) timeout 루프의 관측 오류 → 끝까지 unknown · where timeout |
| r3 | (V2-03) 가짜 시계 — 끝나지 않음 → 기한 15 s 안 · deadline_hit · alive · 대기 ≤ 남은 시간 / 스스로 끝남 → empty / kill 로 끝남 → killed |
| r4 | (V2-02) `base_env` 규칙 · `git` 의 env 필수 · 표지 GIT_* 에도 기록 HEAD = tmp 저장소 · 표지 폴더 비어 있음 |
| r5 | (V2-05) 봉인 표의 모양 (세 단계 · 14 · launcher 자리만 다름) · 같은 바이트 → 0 · 바뀜 · 같은 크기 · 없음 · 링크 · 링크된 상위 · 경로 집합 → 문제 · 줄 형식 |
| r6 | (V2-02 · V2-05) driver — 정상 단계: 기록 HEAD · 표지 · 자식 env · cwd · 원천 두 파일의 정확한 줄 · empty · 시간 경계 · runner_ok · 0 |
| r7 | (V2-04 · V2-05 · S4) driver — 원천 불일치 → 3 / 작업 폴더 파일 → 3 · prepare / + meta 불가 → 4 / 기존 기록 → 거부 · 쓰는 것 0 / git 저장소 아님 → 3 |
| r8 | (V2-01 · V2-03) driver — 실제 timeout: 그룹 + 다른 세션 손주 SIGKILL · 회수 · empty · 기한 안 · 관측 오류 0 · runner_ok false · 1 |

- **RED 선언:** RED-L 은 골격에서 26 실패 · 모두 NotImplementedError. RED-R 은 v2 실행기에서 8 실패 — r1 AssertionError (행동 재현) · r2–r8 AttributeError (인터페이스
  수준 · N1 정정의 RED 와 같은 종류).
- **GREEN 선언:** 61 passed (E0 21 + N1 6 + launcher 26 + 실행기 8). 시험 함수 하나 = 사례 하나.
- 틀린 구현을 잡는 근거는 GREEN 의 음성 대조다 (l2–l5 · l9 · l11–l13 · l15–l26 · r1–r5 · r7 · r8).

## 7. E1-1–3 고정 계획 — **이 요청의 승인 대상이 아니다**

- **선행 조건 (FUTURE-01 · 회신 §3):** v3 고정본만으로 E1-2 를 실행할 수 있다고 적지 않는다. E1-1–3 요청은 fetch 자식의 git 설정 원천을 launcher 가 고정하는
  정정 (`GIT_CONFIG_NOSYSTEM=1` · `GIT_CONFIG_GLOBAL=/dev/null` · 필요한 키만 launcher 가 `GIT_CONFIG_COUNT` / `KEY` / `VALUE` 로 · 사전 검사는 같은 env 로
  "command line" 원천만 허용 · 사후 검사는 `data/git` 로컬 설정을 허용 목록과 대조) 과 그 대조를 담고, 그 차이를 승인의 첫 단계 **E1-0b** (RED / GREEN) 로
  시험한 뒤 첫 실패에서 멈춘다. `http.proxyAuthMethod` 같은 키가 필요한지는 그 요청에서 정한다.
- **순서:** E1-0b → identity (E1-1) → 읽기 경로 `add_repo` (REIL-UConn/… · read) → fetch (E1-2) → run (E1-3) — 첫 예상 밖 실패에서 멈춘다.
- **launcher 호출 · 자식 argv:** v2 §7 과 같고, run 의 승인 문구만 `상태 문서 §NN (사용자 E1-1–3 승인 · docs/REIL_C4E_E1_APPROVAL_REQUEST_v3_20261021.md)` (대조
  l14 가 문자 그대로 고정 · 그 요청이 문서를 바꾸면 그 차이도 E1-0b 에 든다). 증거 폴더 = `evidence/reil_c4e1_<날짜>/`.
- **배정:** 자식 timeout identity 60 · fetch 300 · run 10,800 s · 탐침 ≤ 60 s · fetch 의 git 확인 ≤ 4 × 60 s · launcher 정리 = 명목 배정 kill 대기 10 + 그룹
  관측 5 + 재관측 5 = 20 s (각 관측 창은 마지막 /proc 관측 한 번 · 0.1 s sleep 한 번만큼 넘을 수 있다 — 공통 절대 기한은 그 요청에서 정한다) · 전체 6 h.

## 8. 밝힐 것

1. RED-R 의 일곱 (r2–r8) 은 인터페이스 수준 RED 다 (v3 함수가 v2 에 없다). 행동 재현은 r1 하나 — 회신 V2-01 의 반례가 v2 바이트에서 empty 를 내는지 본다.
2. 외곽 실행기의 실제 timeout 경로는 r8 의 driver 인스턴스로 한 번 시험한다. E1-0 단계 자신이 timeout 되지 않으면 외곽 실행기 인스턴스의 그 경로는 관측되지
   않는다.
3. r6–r8 의 driver 는 자기 subreaper 가 된다. driver 가 정리하지 못한 자손은 외곽 실행기 밑으로 와서 그 단계의 끝 상태를 바꾼다 (fail-closed).
4. /proc PID · ppid 스캔은 비원자적이고 PID 번호로 보내는 kill 은 생성 신원을 보장하지 않는다 — 모든 자손의 연속 소유 · 종료 증명이 아니다 (회신 §5).
5. 기록용 git (외곽 실행기 · launcher) 은 저장소 · 사용자 · 시스템 설정을 그대로 읽는다. 읽기로 확인한 키 이름 (값 읽지 않음): 시스템 `filter.lfs.*` (저장소에
   `filter=lfs` 속성 없음) · 사용자 `user.*` · `gpg.*` · `commit.gpgsign` · `http.proxyauthmethod` · `core.checkstat` · `core.trustctime` · `push.negotiate` ·
   환경 변수로 주어진 command-line 설정 (`url.<…>.insteadof` 둘 · `credential.interactive` — `GIT_CONFIG_*` 이므로 정제 env 에서 빠진다). `core.fsmonitor` ·
   `core.hooksPath` · `includeIf` 키는 없다.
6. 설정 격리 (`GIT_CONFIG_GLOBAL=/dev/null` — git 2.32 부터 · 설치 2.43.0 · 버전 문자열만 읽음) 는 새 대조 둘의 fixture 에만 쓴다. 기존 E0 시험 (수용된 바이트)
   의 git 은 사용자 설정을 읽는다 (그 시험은 `-c commit.gpgsign=false` 를 직접 준다).
7. 탐침의 find_spec 결속은 탐침 시점이다 — 자식 import 까지의 TOCTOU 는 사후 재해시 · `IDENTITY.json` 결속이 잡지만 연속 감시는 아니다 (v2 와 같음).
8. Git 출처 확인은 설정 · rewrite · 받은 저장소의 원격 · shallow 까지 (v2 와 같음) — 조건부 · 템플릿 설정은 FUTURE-01 로 E1-1–3 요청에서 닫는다.
9. S1 의 두 파일은 run 의 `IDENTITY.json` 표에 없다 (run 코드 불변) — launcher 사전 · 사후 재해시 · 봉인 결속 · 실행기 원천 해시가 결속한다.
10. 해석기 · stdlib · site-packages · `sitecustomize` · `.pth` · pytest helper (`pytest_t`) 는 원천 해시 목록 밖이다 (C4-ENV identity · 봉인 MANIFEST 의 범위).
11. 숫자는 timeout · 기다림의 상한이지 전체 소요 보증이 아니다. 정리 15 s 는 공통 기한이고 기록은 별도 배정이다. 자원은 사후 관측이다.
12. GREEN 61 에는 기존 E0 21 · N1 6 의 활동 (§5) 이 포함된다.
13. 대조 l19 는 kill 이 실패한 자식을 시험이 직접 정리한다 (`os.killpg`) — 그 좀비는 pytest 가 끝난 뒤 외곽 실행기 (subreaper) 가 회수한다.
14. pytest 해석기에 `-X pycache_prefix=<새 경로>` 를 더했다 — E0 · N1 의 GREEN 과 다르다. 기존 `scripts/__pycache__/` 는 지우지 않는다.
15. 외곽 실행기는 자기 sha 를 기록만 한다 (자기 해시를 자기 안에 둘 수 없다). 나머지 열넷은 실행기가 봉인 표와 대조한다.
16. RED-R 은 v2 실행기 초안 바이트를 경로로 적재한다 (최상위 정의만 · `main` 미실행 · 우리 소스).
17. v1 · v2 요청서 · 초안은 그대로 둔다 (지난 검토의 근거 바이트 · v2 실행기 초안은 RED-R 대상).

## 9. 하지 않는 것

E1-0b · E1-1–3 (identity · 읽기 경로 · fetch · 자료 개봉 · run) · C4-A / B · E3b · H4 · pickle · 노트북 · 출판 비교 · 해 선택 · 재시도 · 실행 중 예산 변경 ·
설치 · 환경 재구축 · 원자료 커밋 · 대체 출처 · COMSOL. 다섯 모듈 · 목록 · 기존 시험 · 기존 증거 · 봉인은 바꾸지 않는다.

## 10. 정하실 것

1. **사전 검토** — 이 요청과 초안 다섯을 Codex 에 보낸다 (권장 · 발송문 `docs/REIL_C4E_E1_PREREVIEW_SEND_v3_20261021.md`).
2. (검토 수용 뒤) **E1-0 한정 승인** — 승인해도 E1-0b · E1-1–3 은 시작하지 않는다.

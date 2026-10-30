# REIL C4-E · E1 승인 요청 v5 — E1-0 (launcher · 외곽 실행기 대조) 한정 승인 + E1-1–3 고정 계획 · 2026-10-27 KST

> **승인 요청문이다 (실행 0).** 이번 승인 대상은 **E1-0 뿐**이다 — launcher 대조와 외곽 실행기 대조의 RED · GREEN. E1-1–3 (identity · 읽기 경로 · fetch ·
> run) 은 §7 에 고정 계획만 둔다 (**승인 대상 아님** · E1-0 결과 검토 뒤 별도 요청 · 사용자 별도 승인).
> 근거:
> - 상태 문서 §80 — v4 ultra 사전 검토 회신 (`reviews/review_reil_c4e_e1_v4_prereview_20261021/originals/`): `CHANGES_REQUIRED_NO_EXECUTION`.
>   - V3-01–04 · V3-N1 의 정정은 정적 수용됐다.
>   - 새 지적: V4-01 (P2 · l27 · r11 의 Git fixture) · V4-N1 (P3 · 문구).
>   - 수용 범위의 주의 다섯이 붙었다 (§8 에 반영).
> - §81 — 사용자 정정 범위 채택 ("권고대로"). 정정 범위안 v5 `docs/REIL_C4E_E1_REVISION_SCOPE_v5_20261027.md` (`ab1c8164`):
>   - V4-01 은 A — blob 입력 · fixture 자기 확인 · 정확한 대체 문자 기대.
>   - 자체 발견 S6 포함 — 두 git wrapper 에 `encoding="utf-8"` 명시 + AST 확인.
> - 이전 요청 v4 `docs/REIL_C4E_E1_APPROVAL_REQUEST_v4_20261021.md` (`2078cc50…` · 검토 커밋 `3d3ee8c1`) · 정정 범위 v4 (§79) · v3 (§77) · (§75).
>
> 순서: 이 요청 → Codex 사전 검토 → **사용자의 E1-0 한정 승인** → E1-0 → 결과 검토 → E1-1–3 승인 요청 → 검토 → 사용자 별도 승인. v1–v4 요청서와 초안은
> 지우지 않는다 (v2 실행기 초안은 이번에도 RED-R 의 대상 바이트다).

## 0. 요약

| 단계 | 내용 | 이 요청의 승인 대상 |
|---|---|---|
| **E1-0** | 복사 넷 (첫 시험 전 봉인) → RED-L (골격 + launcher 대조 27) → RED-R (v2 실행기 + 실행기 대조 11) → 고정 구현 복사 → GREEN (E0 21 + N1 6 + 27 + 11 = **65**) → 끝 기록 → 멈춤 | **예** |
| E1-1–3 | identity · 읽기 경로 (`add_repo`) · fetch · run 1 회 — launcher 경유 · FUTURE-01 정정 (E1-0b) 이 먼저 | 아니오 (§7 · 별도 승인) |

사례 수는 v4 와 같다 (27 · 11 · 65 · 범위안 v5 §2). 새 대조는 없고, v5 에서 고친 대조는 셋이다:
- l14 — 승인 문구의 요청서 경로.
- l27 · r11 — Git 부분 (V4-01 · S6). /proc 부분은 그대로다.

v4 에서 넣거나 고친 대조 (l12 · l27 · r2 · r3 · r6 · r7 · r9 · r10 · r11) 의 입력 · 기대는 §6 에 그대로 둔다.

## 1. 고정 식별

### 1-1. 이번에 고정하는 초안 다섯 (정적 검사만 · 실행 0)

| 초안 (bms-balancing 기준) | sha256 | bytes | E1-0 에서 복사할 곳 |
|---|---|---:|---|
| `docs/REIL_C4E1_LAUNCHER_DRAFT_v5_20261027.py.txt` — launcher v5 고정 구현 | `2269d775f1701e2f657d386f42bc950d26a6b56bd37323611dd6ab4cc1a75396` | 51,957 | `scripts/reil_c4e1_launch.py` (GREEN 직전) |
| `docs/REIL_C4E1_LAUNCHER_SKELETON_DRAFT_v5_20261027.py.txt` — RED 골격 (함수 35) | `e6f72de2245a41a4a80e0bb7adcc7734991f0b95fb1c1764ea6bfda579849182` | 13,646 | 같은 곳 (RED 둘) |
| `docs/REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v5_20261027.py.txt` — launcher 대조 27 | `4720585c86f555bb0f9cfea3e12aab5b283f8ee4243a3ef257f77849759b777d` | 51,121 | `tests/test_reil_c4e1_launch.py` |
| `docs/REIL_C4E1_RUNNER_CONTROLS_DRAFT_v3_20261027.py.txt` — 외곽 실행기 대조 11 | `ae42d8e8c0fb0c680d324348d2e1edc8f11865bd6bedea7cb0becf9b00fe6042` | 36,478 | `tests/test_reil_c4e1_runner.py` |
| `docs/REIL_C4E1_STEP_RUNNER_DRAFT_v5_20261027.py.txt` — E1-0 외곽 실행기 v5 | `f6070f9776baa7dfc9b5e26ac5e6f378dd2969e7628566e5baa3c02685814a2a` | 36,189 | `<E0>/00_step_runner.py` |

- **정적 검사 (실행 0) — v4 와 같은 것:**
  - AST 파싱 다섯 · 이름 검사 (`__file__` 외 미해결 0).
  - ruff `--isolated` pyflakes 규칙 (`F` · `E9` · `B006` · `B008`) — 골격의 미사용 import 11 외 0. 고정 구현과 같은 import 를 두는 설계이고 v3 · v4 골격도 같은
    11 이다.
  - 골격의 import · 상수 61 문 (+ `if __name__` 블록) = 고정 구현 (AST 동일) · 함수 35 의 이름 · 순서 · 서명 동일 · 골격 본문 모두
    `NotImplementedError("E1-0 RED 골격 …")`.
  - launcher 대조가 쓰는 `L.*` 39 개가 모두 고정 구현 · 골격에 있다 (`__file__` 은 모듈 속성 · 나머지 38 은 최상위 정의).
  - 실행기 대조가 쓰는 `R.*` 16 개가 모두 v5 의 최상위 이름이다. 그중 r2–r11 의 첫 줄이 쓰는 이름 (`cleanup` · `base_env` · `source_table` · `run_step` ·
    `observe`) 은 v2 에 없다.
  - 실행기의 봉인 표 (`EXPECT` — 열넷 · 단계 셋) = 위 초안 넷 · 저장소 HEAD 의 기존 파일 열하나의 실제 바이트 (불일치 0).
  - 비밀 검사 0 건.
- **정적 검사 — v5 에서 더한 것:**
  - 두 git wrapper 의 `subprocess.run` 상수 키워드 (AST): v5 = `text=True` · `encoding="utf-8"` · `errors="replace"`. v4 에는 `encoding` 이 없었다. 대조 l27 ·
    r11 이 같은 AST 확인을 한다.
  - l27 · r11 의 Git 부분에 `commit` · `log` 가 없다. 있는 것: `hash-object -w --no-filters` · `cat-file blob` · fixture 자기 확인 (정확한 바이트 ·
    `UnicodeDecodeError`) · 정확한 대체 문자열 기대.
  - v4 대비 diff 가 머리말 · `REQUEST` · git wrapper · l14 문구 · l27 / r11 의 Git 부분 · 봉인 표 자리에만 있다.
  - RED 첫 줄 불변: l27 의 첫 L 호출은 `L.proc_members` (NotImplementedError) 이고 r11 의 첫 줄은 `R.observe` (v2 에서 AttributeError) 다.
- 골격은 고정 구현에서 정적 변환으로 만들었다 (`make_skeleton_v5.py` — 머리 docstring 교체 · 최상위 함수 본문만 `NotImplementedError`). 실행기의 봉인 표는
  초안 넷을 확정한 뒤 자리표시를 그 sha256 · bytes 로 바꿔 채웠다 (`fill_runner_v3.py` — 같은 정적 치환 도구 · 같은 파일 이름 규칙).

### 1-2. 바뀌지 않는 것 (읽기 대조만)

- 실행 모듈 다섯 = 신뢰 목록 `evidence/reil_c4e0_fix_20261014/04_sources/SOURCES.json` (1,100 B · `2a7b2b49b9809d1a9301398388894a1f7a73afb55acc1a5070e3f77ce0393d52`)
  의 바이트 (§71 · §72). 기존 시험 `tests/test_reil_c4e.py` (57,482 B · `687de63c…`) · `tests/test_reil_c4e_fix.py` (19,506 B · `7a09d438…`).
- S1 의 둘 `scripts/reil_c6_profile.py` (15,915 B · `408afc4b…`) · `degradation-degeneracy/tools/env_profile.py` (22,333 B · `83b0d836…`) · 봉인 결속
  (MANIFEST `4f120948…` → lock `ea91156c…` → 머리줄) — §75 와 같다.
- v2 실행기 초안 `docs/REIL_C4E1_STEP_RUNNER_DRAFT_20261020.py.txt` (12,849 B · `aae2ec14…`) — RED-R 이 시험하는 바이트.
- 다섯 모듈 · 목록 · 기존 시험 · 기존 증거 · 봉인 · v1–v4 요청서 · 초안은 바꾸지 않는다. SP = `/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/b881d255-9513-5adc-9b14-3c0be18d7ad6/scratchpad`.

## 2. 지적 ↔ 정정 · 대조

| ID | 정정 (어디서) | 대조 |
|---|---|---|
| **V4-01** l27 · r11 의 Git fixture 가 비 UTF-8 stdout 을 만들지 못함 | **입력 생산자:** 커밋 메시지를 쓰지 않는다. Git 2.43.0 은 기본 UTF-8 커밋 저장에서 잘못된 바이트를 Latin-1 로 보고 UTF-8 로 바꾼다 (§80). 대신 정해진 바이트 `b"fixture \xff\xfe not utf-8\n"` 를 tmp 파일에 쓰고 `git hash-object -w --no-filters` 로 blob 을 만든다. wrapper 는 `cat-file blob <sha>` 를 부른다. **fixture 자기 확인:** wrapper 를 거치지 않고 같은 명령의 stdout 을 바이트로 받아, 정확히 그 바이트이고 엄격 UTF-8 디코딩이 `UnicodeDecodeError` 인지 먼저 본다. **기대:** `out == 그 바이트.decode("utf-8", "replace")` (U+FFFD 둘 · 정확한 문자열) · rc 0 · `error` 없음. U+FFFD 검사는 유지한다 | l27 · r11 (Git 부분) |
| **S6** (자체 · V4-01 의 "Python 디코딩 환경") wrapper 디코딩이 locale 에 기댐 | launcher `git_run` · 실행기 `git` 의 `subprocess.run` 에 `encoding="utf-8"` 을 명시한다 (`text=True` · `errors="replace"` 는 그대로). git 출력 (HEAD · porcelain · config 목록 포함) 의 해석이 실행 환경 locale 에 기대지 않는다 | l27 · r11 (wrapper 키워드 AST 확인 + 정확한 문자열) |
| **V4-N1** 요청서 v4 l.274–275 의 문구 | "실제 정리 경로가 아니며" → "E1-1–3 실자료 운영 실행은 아니지만, E1-0 대조 (l11 · l19) 는 실제 가짜 자식 프로세스의 정리를 일부 수행한다" (§8 의 18) | 문구 |
| V3-01–04 · V3-N1 · S5 | 바뀌지 않음 — §80 의 정적 수용 범위 · 정정 내용은 v4 요청서 §2 · §3-2 와 같다 (아래 §3-2 그대로) | r2 · r3 · r6–r10 · l12 · l27 · r11 (/proc 부분) |
| V2-01–05 · S2–S4 · N1 · S1 · N6 | 바뀌지 않음 (§78 의 수용 범위 · v3 요청서 §2) | 그대로 |

## 3. 판정 · 정리 경로 (요약 — 정본은 초안 docstring 과 코드)

### 3-1. launcher v5 (v3 에서 바뀐 것 · v5 는 S6 · `REQUEST` 만)

v3 §3 의 경로 (준비 → 사전 대조 → 시작 기록 → 자식 → 사후 대조 → 단계 판정 = precheck_ok AND child_ok AND rc_0 AND timeout_false AND postcheck_ok) 는
그대로다. v4 에서 바뀐 것: 의도된 거부의 기존 항목 확인이 `entry_exists` (V3-02) · `proc_members` 의 바이트 읽기와 PID 별 넓은 포착 (V3-03) · `git_run` 의
`errors="replace"` (S5). v5 에서 바뀐 것: `git_run` 의 `encoding="utf-8"` (S6) · 승인 문구의 요청서 경로 `REQUEST` = 이 문서. launcher 의 정리 루프
(`run_child` · `group_status`) 는 이번 정정 대상이 아니다 (§8 의 18).

### 3-2. 외곽 실행기 v5 의 정리 (V3-01 · v4 와 같음 — v5 는 `git` 의 `encoding="utf-8"` (S6) 만 더했다)

1. **기한은 단계에 하나:** `run_step` 이 정리 단계에 들어갈 때 `t_c0 = clock()` · `cdl = t_c0 + 15` 를 한 번 만들고 `cleanup(…, deadline=cdl)` 에 넘긴다.
   `times.cleanup_s` = `t_c0` 부터 (run_step) · `cleanup.cleanup_s` = cleanup 자신의 시작부터.
2. **새 관측 · 대기는 기한 전에만 시작:** timeout 루프 (그룹 SIGKILL 뒤 kill 대기 끝 `until = min(기한, 원점 + 7)`) 와 settle 의 두 관측 창 (`min(기한,
   시작 + 3)` · kill 뒤 기한) 은 모두 `while clock() < until:` 로 관측을 시작하기 전에 본다. sleep 은 `min(0.1, until − 지금)` 이고 남은 시간이 0 이하이면 자지
   않는다. pytest 회수는 `p.wait(timeout=max(0, until − 지금))` — 기한 뒤에는 `wait(0)`.
3. **기한 뒤에 허용하는 것:** 기한 전에 시작한 관측의 결과에 따른 즉시 동작 (좀비 회수 `waitpid(WNOHANG)` · SIGKILL 보내기 — 기다리지 않는다) · 비차단 확인
   (`poll` · `wait(0)`) · 기록. 새 관측 · sleep · 차단 대기는 하지 않는다.
4. **끝 상태:** empty (기한 전에 시작한 관측에서 살아 있는 자손 0 · kill 0) · killed (kill 뒤 기한 전에 시작한 재관측에서 0) · alive (마지막 관측에 생존) ·
   **unverified** (기한 때문에 확인 관측을 못 함 — 관측 0 이거나 kill 뒤 재관측 없음) · unknown (ledger 에 오류가 하나라도 있으면 · 우선). runner_ok 는 empty
   (+ `deadline_hit` false) 만.
5. **정리 안의 예외:** cleanup 이 잡아 `cleanup.errors` · ledger (`where: cleanup_exception`) 에 남기고 `emergency` true → pytest 가 살아 있으면 (`poll`)
   그룹 SIGKILL → 같은 기한으로 settle (관측은 기한 전에만). 비상 동작의 예외는 `cleanup_emergency` 로 남기고 끝 상태 unknown. 새 기한은 없다.
6. **run_step 의 복구:** 자식이 시작된 뒤의 예외인데 정리 결과가 없을 때만 cleanup 을 부른다 — 정리 전의 예외면 그때 기한을 처음 만들고, 이미 있으면 (cleanup
   이 예외를 밖으로 낸 경우) 그 기한을 그대로 쓴다.
7. **넘을 수 있는 것:** 기한 전에 시작한 관측 하나 — 그 관측의 길이에는 상한이 없다 (§8 의 11).

## 4. E1-0 절차 (이 요청의 승인 대상)

### 4-1. 순서 · 배정

| # | 단계 | 배정 | 기대 | 어긋나면 |
|---|---|---|---|---|
| a | 절차 Git 이름 확인 (§4-6) → 승인 기록 § · 보존 규칙 (`evidence/reil_c4e1_0_<날짜>/** -text`) 커밋 → `<E0>` 만들기 — `<E0>` · `SP/c4e1_steps` 가 이미 있으면 멈춤 | — | 허용 목록 밖 0 | 멈춤 |
| b | **복사 넷 · 첫 시험 전 봉인:** 대조 둘 → `tests/` · 골격 → `scripts/reil_c4e1_launch.py` · 실행기 → `<E0>/00_step_runner.py` → `00_start.txt` (§4-5 · Git 없음) → 복사본 sha = §1-1 확인 → 커밋 | — | sha 일치 | 멈춤 |
| c | **RED-L** `01_red_launcher` (실행기) · 커밋 | pytest 120 s + 정리 ≤ 15 s + 기록 | §4-3 | 멈춤 |
| d | **RED-R** `02_red_runner` (실행기) · 커밋 | pytest 120 s + 정리 ≤ 15 s + 기록 | §4-3 | 멈춤 |
| e | 고정 구현 복사 (sha 대조) → **GREEN** `03_green` (65 · `-x`) · 커밋 | pytest 600 s + 정리 ≤ 15 s + 기록 | §4-3 | 멈춤 |
| f | 절차 Git 이름 확인 (§4-6) → `04_end.json` (§4-5 · Git 없음) · 비밀 검사 · 커밋 · push · 결과 기록 § · 결과 검토 발송문 → **멈춤** | — | 허용 목록 밖 0 | 멈춤 |

- **정리 ≤ 15 s** = 외곽 실행기의 공통 절대 기한 (정리 원점부터 · 넘을 수 있는 것은 기한 전에 시작한 /proc 관측 하나 · §3-2). **기록** = 단계마다 Git 호출
  넷 (각 timeout 60 s · 시작 둘 · 끝 둘 · 정제 env) · 원천 해시 두 번 · meta — 정리 15 s 밖의 별도 배정이다.
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

- SP · BMS · `<E0>` 는 실제 명령에서 절대 경로로 풀어 쓴다 (위 표기는 줄임일 뿐이다). 명령은 v3 와 같다.
- env (실행기가 만든다): 현재 env → `base_env` (비밀 형태 이름 · SSH_ASKPASS · GIT_SSL_CAINFO 밖의 모든 GIT_* 제거 · 이름만 기록 · GIT_TERMINAL_PROMPT=0) +
  `PYTHONDONTWRITEBYTECODE=1` · `MPLBACKEND=Agg` · `MPLCONFIGDIR` · `TMPDIR` (`SP/c4e1_steps/{mpl,tmp}`) · `OMP` / `OPENBLAS` / `MKL_NUM_THREADS=1` ·
  `REIL_C4_FIX_EVIDENCE=<E0>` · `REIL_C4_FIX_STEP=<단계>`. 실행기 대조가 시험할 파일은 argv 의 `/usr/bin/env` 가 정한다 — 값이 두 형태 밖이면 수집 오류로
  멈추고, 값이 없으면 그 파일 전체를 건너뛴다 (E1-0 단계 밖의 실행을 막지 않으려는 것 · 단계 안에서는 아래 기준의 skipped 0 이 깨져 멈춘다).
- helper: pytest 는 `SP/reil_c4env/pytest_t` (pytest 9.1.1 · E0 · N1 과 같은 경로). 해석기에 `-X pycache_prefix=<새 경로>` 를 더한다.

### 4-3. RED · GREEN 기준 — 첫 예상 밖 결과에서 멈춘다

공통 (실행기 meta): `started` true · `timed_out` false · `cleanup.status` "empty" · `cleanup.deadline_hit` false · `end_problems` 없음 · `errors` 없음 ·
`runner_ok` true. pytest rc 의 해석은 아래가 정한다.

- **RED-L (`01_red_launcher`):** pytest rc 1 · 요약 "27 failed" · 통과 0 · 건너뜀 0 · 수집 오류 0 · 짧은 요약의 실패 27 줄이 모두
  `NotImplementedError: E1-0 RED 골격`.
- **RED-R (`02_red_runner`):** pytest rc 1 · 요약 "11 failed" · 통과 0 · 건너뜀 0 · 수집 오류 0 · 짧은 요약: r1 = `AssertionError` (v2 의 settle 이 status
  "empty" 를 낸다 — 회신 V2-01 의 반례가 그 바이트에서 재현) · r2 · r3 · r9 · r10 = `AttributeError: module 'runner_under_test' has no attribute 'cleanup'` ·
  r4 = `… 'base_env'` · r5 = `… 'source_table'` · r6 · r7 · r8 = `… 'run_step'` · r11 = `… 'observe'`.
- **GREEN (`03_green`):** pytest rc 0 · 요약 "65 passed" (건너뜀 · xfail 0). `-x` 로 pytest 가 첫 실패에서 멈추고, 실패가 하나라도 있으면 E1-0 을 멈춘다.
- 하나라도 다르면 (통과 · 다른 예외 · 수집 오류 · 잔존 · 기한 · unverified · 기록 실패 · 원천 해시 불일치 · 실행기 반환 3 / 4) 멈춘다. 재시도하지 않는다.

### 4-4. 봉인 · 원천 해시 (V2-05 · 바뀌지 않음)

- **첫 시험 전 봉인:** 복사 넷을 RED-L 전에 커밋한다 (b). fixture 생성 규칙 · 고정 입력 · 기대값은 봉인된 대조 파일 안에 있다. 끝 기록의 diff 로 사전 고정을
  대신하지 않는다.
- **생성 주체 = 외곽 실행기.** 대상 = `TARGETS` 14 (저장소 기준): `bms-balancing/scripts/reil_c4e1_launch.py` · `tests/test_reil_c4e1_launch.py` ·
  `tests/test_reil_c4e1_runner.py` · `tests/test_reil_c4e.py` · `tests/test_reil_c4e_fix.py` · 다섯 모듈 · `scripts/reil_c6_profile.py` ·
  `degradation-degeneracy/tools/env_profile.py` · `evidence/reil_c4e0_fix_20261014/04_sources/SOURCES.json` · `docs/REIL_C4E1_STEP_RUNNER_DRAFT_20261020.py.txt`.
- **기대값 = `EXPECT[단계]`** (실행기 v5 안 · §1-1 · §1-2 의 sha 와 같음) — 단계마다 다른 것은 launcher 자리 하나 (RED-L · RED-R = 골격 `e6f72de2…` · GREEN =
  고정 구현 `2269d775…`). 대조 둘의 행 = launcher 대조 v5 `4720585c…` · 외곽 실행기 대조 v3 `ae42d8e8…`.
- **시점 · 실패 기준:** 준비 끝 (자식 전) `<단계>.source_sha256.txt` (`sha256  경로` 줄 · 끝줄에 실행기 자신 — 대조 밖) → 하나라도 다르면 (없음 · 일반 파일
  아님 · 링크 · 다른 바이트) 자식 0 · 반환 3 · `first_error` = prepare / SourceMismatch / 끝 기록 뒤 `<단계>.source_sha256_end.txt` → 다르면 runner_ok false.

### 4-5. 기록 · 제출 (V3-04 A)

- **증거 폴더 (`<E0>`):** 실행기가 단계마다 `<단계>.{meta.json, stdout.log, stderr.log, porcelain_start.txt, porcelain_end.txt, source_sha256.txt,
  source_sha256_end.txt}` · 나 (고정 명령) 가 `00_start.txt` · `04_end.json` · 복사본 `00_step_runner.py`.
- **증거의 Git 상태는 외곽 실행기 기록만이다:** 단계마다 시작 · 끝의 HEAD · porcelain (정제 env · `git -C <저장소>` · rc · 오류 그대로 · meta 의 `records` 와
  `<단계>.porcelain_*.txt`). 단계 안의 HEAD 불변은 실행기가 확인한다 (runner_ok 의 항).
- **수동 기록 — Git 을 부르지 않는다:** `00_start.txt` = `date -u +%Y-%m-%dT%H:%M:%SZ` · `df -B1 --output=avail /home/user/Yonghoon-DEM-DFT` · `sha256sum`
  (초안 다섯 + 복사본 넷). `04_end.json` = 같은 UTC · 디스크 · 복사본 넷 sha256 · 단계 셋의 meta 요약 (`started` · `runner_ok` · `rc` · `timed_out` ·
  `cleanup.status` · `times` · 실행기가 쓴 `records.head_start` / `head_end` 의 값) · §4-6 의 f 확인 결과 (이름만) — stdlib python 한 번 (읽기 = meta 셋 ·
  복사본 넷 · 디스크 · 시각 · 쓰기 = `04_end.json` 배타 생성 · git · 네트워크 0).
- **만들지 않는 것:** `00_porcelain_start.txt` · `04_porcelain_end.txt` (v3 의 수동 Git 기록 · 회신 V3-04).
- **커밋:** 증거 폴더 · `tests/test_reil_c4e1_launch.py` · `tests/test_reil_c4e1_runner.py` · `scripts/reil_c4e1_launch.py`. 커밋하지 않음: `SP/c4e1_steps/`.
- 커밋 전: 비밀 검사 + URL 계정 정보 형태 검사 · 파일 하나 ≤ 50 MB.

### 4-6. 절차 Git 의 중지 조건 (V3-04)

- **절차 Git** = add · commit · push · log — 증거가 아니다 (그 결과를 증거로 인용하지 않는다).
- **이름 확인 (고정 명령 · 값을 읽거나 출력하지 않는다):**

  ```
  /usr/bin/python3.11 -I -c 'import json, os, re, sys; n = sorted(k for k in os.environ if k.startswith("GIT_")); bad = [k for k in n if not re.fullmatch(r"GIT_(ASKPASS|CONFIG_COUNT|CONFIG_(KEY|VALUE)_[0-9]+|EDITOR|SSL_CAINFO|TERMINAL_PROMPT)", k)]; print(json.dumps({"git_env_names": n, "outside_allowlist": bad})); sys.exit(1 if bad else 0)'
  ```

- **허용 목록:** `GIT_ASKPASS` · `GIT_CONFIG_COUNT` · `GIT_CONFIG_KEY_<n>` · `GIT_CONFIG_VALUE_<n>` · `GIT_EDITOR` · `GIT_SSL_CAINFO` · `GIT_TERMINAL_PROMPT`. 위치
  · 추적 계열 (`GIT_DIR` · `GIT_WORK_TREE` · `GIT_INDEX_FILE` · `GIT_OBJECT_DIRECTORY` · `GIT_ALTERNATE_OBJECT_DIRECTORIES` · `GIT_TRACE*` 등) 과 그 밖 모든
  `GIT_*` 는 목록 밖이다.
- **시점:** 단계 a 의 첫 git 직전 · 단계 f 의 첫 git 직전 (결과를 a 는 승인 기록 § 에, f 는 `04_end.json` 에 이름만 남긴다). b–e 의 절차 git 도 같은 셸 명령
  줄에서 이 확인 뒤에만 실행한다 (`<확인> && git …` — 확인이 0 이 아니면 그 git 은 실행되지 않는다).
- **어긋나면:** 목록 밖 이름이 하나라도 있으면 멈춘다 (이름만 기록). 지금 셸에는 목록 밖이 없지만 (§78 의 읽기 확인) 이 관측에 기대지 않고 규칙으로 고정한다.

## 5. 활동 범위 셋

| 범위 | 포함 | 제외 |
|---|---|---|
| **새 대조 38 (launcher 27 + 실행기 11)** | launcher 함수 · tmp 가짜 run 스크립트 (stdlib) · 손주 sleep · 해석기 탐침 (`-c`) · tmp 안 로컬 git (init · 빈 커밋 · rev-parse · status · remote add · `config --list` · `ls-remote --get-url` · blob 생성 `hash-object -w --no-filters` · `cat-file blob` — fixture 자기 확인의 직접 호출 포함) · 대상 파일의 AST 읽기 (wrapper 키워드 · 실행 아님) · 가짜 /proc 폴더 (UTF-8 이 아닌 comm 바이트 포함) · 주입한 읽기 예외 (PermissionError · UnicodeDecodeError) · 표지 GIT_* 와 다른 tmp 저장소 · 끊어진 심볼릭 링크 · 준비 실패 주입 / 실행기: 가짜 /proc 표 · 관측마다 시간을 쓰는 가짜 시계 · 늦은 예외 주입 · 가짜 kill / waitpid · driver 하위 프로세스 8 회 (r6 1 · r7 6 · r8 1 — `-I -B -X pycache_prefix` · 실행기 모듈 경로 적재 · `main` 미실행 · `run_step` 을 tmp 경로로 · prctl subreaper · stdlib 가짜 자식 · 다른 세션 손주 · SIGKILL) · RED-R 의 v2 실행기 초안 적재 (최상위 정의만) | 우리 실행 모듈 다섯 import · 실제 자료 · optimizer · 네트워크 |
| **GREEN 전체 65** | 위 + E0 21 · N1 6 — 실제 실행 모듈 import (c5 import 때 `reil_c6_profile` · `reil_p0` 경로 실행 포함) · 로컬 Git / fetch 대조 · 합성 `run.run` 둘 · `plan_e` · fork 세션 | 실제 원자료 · 원 optimizer · 네트워크 fetch |
| **실제 E1-1–3** | identity (`env_profile` 실행 포함) · 읽기 경로 · 고정 출처 fetch · 원자료 개봉 · 66 호출 run | **E1-0 승인으로 허용되지 않는다** |

"우리 실행 모듈 import 0" 은 새 대조 38 에만 쓴다. 위 수는 소스가 계획한 활동이지 수행 횟수가 아니다.

## 6. 대조 27 + 11 · RED / GREEN 선언

바뀌지 않은 대조: l1–l11 · l13 · l15–l26 (v3 요청서 §6) · r1 · r4 · r5 · r8 (v3 요청서 §6). l14 는 승인 문구의 요청서 경로만 v5 로 바뀌었다. v4 에서 새로
넣거나 고친 대조와 v5 에서 고친 l27 · r11 (회신 §78 의 주의대로 입력 · 기대 · 이유 · 호출 경로를 고정한다 · v5 의 변경은 Git 부분뿐):

| ID | 고정 입력 | 기대 | 이유 · 호출 경로 |
|---|---|---|---|
| l12 (수정) | `<ev>/05_run.meta.json` = 없는 대상 (`tmp/nowhere.json`) 을 가리키는 링크 → 같은 자리의 일반 파일 → (지운 뒤) 기존 pycache 폴더 | 셋 모두 SystemExit (앞 둘 "덮어쓰지 않는다" · 셋째 "pycache") · 증거 폴더에는 그 링크 / 파일 하나뿐 · 작업 폴더 · 링크 대상 · `LAUNCHED` 없음 | V3-02 — `launch` → `entry_exists` (v3 의 `exists()` 는 링크를 따라가 false) |
| l27 (v4 새 · v5 Git 부분 수정) | 가짜 /proc (그룹 777): 201 comm `bad\xff\xfename` (바이트) · 202 읽기가 UnicodeDecodeError (주입) · 203 읽기가 PermissionError (주입) / tmp 저장소 (`init --template=`) 의 blob — 바이트 `b"fixture \xff\xfe not utf-8\n"` 를 `hash-object -w --no-filters` 로 저장 | `proc_members` 구성원 [201] · 오류 pid {202, 203} · `group_status` unknown · 기본 읽기 (바이트) → 구성원 {201, 202, 203} · 오류 0 / **fixture 자기 확인:** wrapper 없이 `git cat-file blob <sha>` 의 stdout = 그 바이트 · 엄격 UTF-8 디코딩은 `UnicodeDecodeError` / `git_run` 의 `subprocess.run` 키워드 (AST) = `text=True` · `encoding="utf-8"` · `errors="replace"` / `git_run(["-C", repo, "cat-file", "blob", sha])` rc 0 · `out == 바이트.decode("utf-8", "replace")` (U+FFFD 둘) · `error` 없음 | V3-03 · S5 · V4-01 · S6 — `proc_members` (바이트 · PID 별 넓은 포착) · `git_run` (UTF-8 · 대체). 커밋 메시지는 Git 이 UTF-8 로 정규화하므로 쓰지 않는다 |
| r2 (수정) | v3 와 같은 입력 + `deadline=t0+15` | v3 와 같은 기대 (unknown · where timeout · 그룹 kill · 회수 · 관측 ≥ 3) | 기한은 호출자가 준다 (V3-01) — `cleanup(…, deadline)` 필수 |
| r3 (수정) | 관측마다 0.05 s 를 쓰는 가짜 /proc 표 (`_costly` — 시작 시각을 남기고 그 시각의 표) · 기한 t0+15 · (a) timeout · 끝나지 않는 pytest 4242 · 자손 4243 · kill 이 듣지 않음 (b) 정상 종료 · 4243 이 2 s 뒤 좀비 (c) 정상 종료 · 4243 이 kill 뒤 좀비 | (a) alive · deadline_hit · 미종료 · 모든 관측 시작 < t0+15 · 끝 ≤ t0+15.05 · `cleanup_s` ≤ 15.05 · sleep 끝 ≤ 기한 · pytest 대기 ≤ kill 대기 끝 (t0+7) 까지 남은 시간 (b) empty · kill 0 · 회수 [4243] · deadline_hit false (c) killed · kill [[4243, sent]] · 끝 ≈ t0+3 (±0.2) | V3-01 — 관측 비용이 0 이 아닌 시계 (v3 의 r3 시계는 sleep / wait 만 진행) · `cleanup` → `observe` → `proc_table` |
| r6 (수정) | v3 와 같음 | + `times` 에 `cleanup_s` · `times.cleanup_s` ≥ `cleanup.cleanup_s` | 정리 시간은 run_step 이 정리 원점부터 잰다 (V3-01) |
| r7 (수정) | v3 의 (a)–(e) + (d′) `<E>/03_green.meta.json` = 없는 대상 (`tmp/gone.json`) 을 가리키는 링크 | (a) + first_error = prepare / SourceMismatch · (e) + first_error = record / GitRecordFailed · (d′) driver 반환 2 (거부 · "덮어쓰지 않는다") · 증거 폴더에 그 링크 하나 · 대상 · 작업 폴더 · 자식 출력 없음 | V3-N1 · V3-02 — `run_step` (`errors` 항목 · `entry_exists`) |
| r9 (새) | timeout · 끝나지 않는 pytest 4242 · 자손 4243 · 관측 비용 [6.85 s, 9.0 s] · 기한 t0+15 | 관측 시작 [t0, t0+6.95] 두 번뿐 · 끝 t0+15.95 · 둘째 관측 뒤에도 4242 · 4243 에 SIGKILL (각 2 회째) · sleep 1 회 · pytest 대기 `[(t0+15.95, 0.0)]` · settle 관측 0 → unverified (alive None · kill 0 · 오류 0) · 끝 상태 unverified · deadline_hit · emergency false · `cleanup_s` 15.95 | V3-01 회신의 정적 반례 — 기한 뒤 허용 = 즉시 동작 · 비차단 확인 · 기록 |
| r10 (새) | 관측 0.05 s · 기한 t0+15 · (a) 정상 종료 pytest · kill 이 듣지 않는 자손 4243 · 시작 시각 ≥ t0+10 인 첫 관측이 RuntimeError (b) timeout · 끝나지 않는 pytest · 첫 관측이 RuntimeError | (a) unknown · emergency · `errors` = ["RuntimeError: scan failed (시험 주입)"] · 예외 시각 ∈ [t0+10, t0+10.2) · 그룹 kill 0 (pytest 는 이미 끝남) · deadline_hit · 모든 관측 시작 < t0+15 · 끝 ∈ [t0+15, t0+15.05] · settle.first_error.where = cleanup_exception · `cleanup_s` = 끝 − t0 (b) unknown · emergency · 그룹 kill 2 회 (처음 + 비상) · pytest 대기 0 회 · exited_after_kill None · 같은 기한 | V3-01 — 늦은 예외를 cleanup 이 잡고 같은 기한으로 비상 동작 (새 15 s 없음) |
| r11 (v4 새 · v5 Git 부분 수정) | tmp 가짜 /proc: 101 정상 · 102 읽기 PermissionError · 103 읽기 UnicodeDecodeError (주입) · 104 comm `\xff\xfe a) b` (괄호가 든 바이트) · 숫자 아닌 `self` / settle(me=1) 의 첫 관측 = 그 표 · 둘째 = 빈 표 (가짜 시계) / tmp 저장소 (`init --template=`) 의 blob — l27 과 같은 바이트 · `hash-object -w --no-filters` | `observe` 표 {101, 104} · ledger pid {102, 103} · where settle · 기본 읽기 → 넷 모두 · ledger 0 / settle unknown · 관측 2 · first_alive [101, 104] · alive [] · kill · 회수 0 · errors pid {102, 103} / **fixture 자기 확인:** l27 과 같음 / 실행기 `git` 의 `subprocess.run` 키워드 (AST · 시험할 실행기 파일) = `text=True` · `encoding="utf-8"` · `errors="replace"` / `git(["cat-file", "blob", sha], cwd=repo)` rc 0 · `out == 바이트.decode("utf-8", "replace")` · `error` 없음 | V3-03 · S5 · V4-01 · S6 — `observe` → `proc_table` (바이트) · `settle` · `git` (UTF-8 · 대체) |

- **RED 선언:** RED-L 은 골격에서 27 실패 · 모두 NotImplementedError. RED-R 은 v2 실행기에서 11 실패 — r1 AssertionError (행동 재현) · r2–r11 AttributeError
  (인터페이스 수준 · N1 정정의 RED 와 같은 종류).
- **GREEN 선언:** 65 passed (E0 21 + N1 6 + launcher 27 + 실행기 11). 시험 함수 하나 = 사례 하나 (parametrize 없음 · 한 함수 안의 하위 사례는 순서대로).
- 틀린 구현을 잡는 근거는 GREEN 의 음성 대조다 (l2–l5 · l9 · l11–l13 · l15–l27 · r1–r5 · r7–r11).

## 7. E1-1–3 고정 계획 — **이 요청의 승인 대상이 아니다**

- **선행 조건 (FUTURE-01):** v5 고정본만으로 E1-2 를 실행할 수 있다고 적지 않는다. E1-1–3 요청은 fetch 자식의 git 설정 원천을 launcher 가 고정하는 정정
  (`GIT_CONFIG_NOSYSTEM=1` · `GIT_CONFIG_GLOBAL=/dev/null` · 필요한 키만 launcher 가 `GIT_CONFIG_COUNT` / `KEY` / `VALUE` 로 · 사전 검사는 같은 env 로
  "command line" 원천만 허용 · 사후 검사는 `data/git` 로컬 설정을 허용 목록과 대조) 과 그 대조를 담고, 그 차이를 승인의 첫 단계 **E1-0b** (RED / GREEN) 로
  시험한 뒤 첫 실패에서 멈춘다. `http.proxyAuthMethod` 같은 키가 필요한지는 그 요청에서 정한다.
- **launcher 정리:** launcher 의 정리 루프 (`run_child` · `group_status`) 에 V3-01 의 규칙 (관측 시작 전 기한 검사 · 기한 뒤 허용 동작 · 미완 기록) 을 맞출지와
  공통 절대 기한은 그 요청에서 정한다.
- **순서:** E1-0b → identity (E1-1) → 읽기 경로 `add_repo` (REIL-UConn/… · read) → fetch (E1-2) → run (E1-3) — 첫 예상 밖 실패에서 멈춘다.
- **launcher 호출 · 자식 argv:** v2 §7 과 같고, run 의 승인 문구만 `상태 문서 §NN (사용자 E1-1–3 승인 · docs/REIL_C4E_E1_APPROVAL_REQUEST_v5_20261027.md)` (대조
  l14 가 문자 그대로 고정 · 그 요청이 문서를 바꾸면 그 차이도 E1-0b 에 든다). 증거 폴더 = `evidence/reil_c4e1_<날짜>/`.
- **배정:** 자식 timeout identity 60 · fetch 300 · run 10,800 s · 탐침 ≤ 60 s · fetch 의 git 확인 ≤ 4 × 60 s · launcher 정리 = 명목 배정 kill 대기 10 + 그룹
  관측 5 + 재관측 5 = 20 s (각 관측 창은 마지막 /proc 관측 한 번 · 0.1 s sleep 한 번만큼 넘을 수 있다 — 공통 절대 기한은 그 요청에서 정한다) · 전체 6 h.

## 8. 밝힐 것

1. RED-R 의 열 (r2–r11) 은 인터페이스 수준 RED 다 (v4 함수가 v2 에 없다). 행동 재현은 r1 하나 — 회신 V2-01 의 반례가 v2 바이트에서 empty 를 내는지 본다.
   r3 · r9 · r10 · r11 · r7 (a) (d′) (e) 가 **v3** 실행기 바이트에서 실패하는지는 이번에 시험하지 않는다 — 근거는 회신 §78 의 정적 도달 경로다. 정적으로 보면
   v3 에서 r2 · r3 · r9 · r10 은 `deadline` 인자에서 TypeError (인터페이스), r11 은 103 의 UnicodeDecodeError 가 v3 의 `except OSError` 를 빠져나가 실패, r7 (a)
   는 `first_error` 가 None 이라 실패, r6 은 `times.cleanup_s` 가 없어 실패한다 — 관측이 아니다. 특히 V3-01 의 행동 (기한 뒤 새 관측 · 복구의 새 15 s) 은 v3
   바이트에서도 대조로 재현할 수 없다 (v4 의 `deadline` 인자가 v3 에 없다). r9 는 회신의 반례를 v4 의 기대값으로 고정할 뿐이다. 이 제한은 §80 (Q5) 에서
   공개한 그대로 수용됐다 — 새 v3 재현 단계는 요구되지 않았다.
2. 외곽 실행기의 실제 timeout 경로는 r8 의 driver 인스턴스로 한 번 시험한다. E1-0 단계 자신이 timeout 되지 않으면 외곽 실행기 인스턴스의 그 경로는 관측되지
   않는다. 기한 · 늦은 예외 · unverified 경로는 가짜 시계 (r3 · r9 · r10) 로만 시험한다 — 가짜 시계 검토이지 실제 /proc 지연의 상한을 관측한 것이 아니다
   (§80).
3. r6–r8 의 driver 는 자기 subreaper 가 된다. driver 가 정리하지 못한 자손은 외곽 실행기 밑으로 와서 그 단계의 끝 상태를 바꾼다 (fail-closed).
4. /proc PID · ppid 스캔은 비원자적이고 PID 번호로 보내는 kill 은 생성 신원을 보장하지 않는다 — 모든 자손의 연속 소유 · 종료 증명이 아니다.
5. 기록용 git (외곽 실행기 · launcher) 은 저장소 · 사용자 · 시스템 설정을 그대로 읽는다. 읽기로 확인한 키 이름 (값 읽지 않음 · §77): 시스템 `filter.lfs.*`
   (저장소에 `filter=lfs` 속성 없음) · 사용자 `user.*` · `gpg.*` · `commit.gpgsign` · `http.proxyauthmethod` · `core.checkstat` · `core.trustctime` ·
   `push.negotiate` · 환경 변수로 주어진 command-line 설정 (`url.<…>.insteadof` 둘 · `credential.interactive` — `GIT_CONFIG_*` 이므로 정제 env 에서 빠진다).
   `core.fsmonitor` · `core.hooksPath` · `includeIf` 키는 없다.
6. 설정 격리 (`GIT_CONFIG_GLOBAL=/dev/null` — git 2.32 부터 · 설치 2.43.0) 는 새 대조 둘의 fixture 에만 쓴다. 기존 E0 시험 (수용된 바이트) 의 git 은 사용자
   설정을 읽는다 (그 시험은 `-c commit.gpgsign=false` 를 직접 준다).
   - l27 · r11 의 비 UTF-8 입력은 커밋 메시지가 아니라 blob 이다. Git 은 기본 UTF-8 커밋 저장에서 잘못된 바이트를 Latin-1 로 보고 UTF-8 로 바꾼다 (§80
     V4-01). **v4 의 이 항목은 "커밋 메시지가 바이트 그대로 출력된다" 는 틀린 전제를 적었다.**
   - blob (`hash-object -w --no-filters`) 과 `cat-file blob` 이 내용을 바이트 그대로 다룬다는 것은 Git 의 공개 의미에 기댄 설계 판단이다 (이번에 실행 0).
     시험이 wrapper 보다 먼저 그 바이트를 직접 확인하므로, 틀리면 GREEN 에서 그 자리의 AssertionError 로 멈춘다.
7. 탐침의 find_spec 결속은 탐침 시점이다 — 자식 import 까지의 TOCTOU 는 사후 재해시 · `IDENTITY.json` 결속이 잡지만 연속 감시는 아니다 (v2 와 같음).
8. Git 출처 확인은 설정 · rewrite · 받은 저장소의 원격 · shallow 까지 (v2 와 같음) — 조건부 · 템플릿 설정은 FUTURE-01 로 E1-1–3 요청에서 닫는다.
9. S1 의 두 파일은 run 의 `IDENTITY.json` 표에 없다 (run 코드 불변) — launcher 사전 · 사후 재해시 · 봉인 결속 · 실행기 원천 해시가 결속한다.
10. 해석기 · stdlib · site-packages · `sitecustomize` · `.pth` · pytest helper (`pytest_t`) 는 원천 해시 목록 밖이다 (C4-ENV identity · 봉인 MANIFEST 의 범위).
11. 숫자는 timeout · 기다림의 상한이지 전체 소요 보증이 아니다. 정리 15 s 는 공통 기한이고, 넘을 수 있는 것은 기한 전에 시작한 관측 하나다 — 그 관측의
    길이에는 상한이 없다 (실행기는 감시 스레드를 두지 않는다 · /proc 읽기가 멈추면 정리도 멈춘다). 기록은 별도 배정이다. 자원은 사후 관측이다.
12. GREEN 65 에는 기존 E0 21 · N1 6 의 활동 (§5) 이 포함된다.
13. 대조 l19 는 kill 이 실패한 자식을 시험이 직접 정리한다 (`os.killpg`) — 그 좀비는 pytest 가 끝난 뒤 외곽 실행기 (subreaper) 가 회수한다.
14. pytest 해석기에 `-X pycache_prefix=<새 경로>` 를 더했다 — E0 · N1 의 GREEN 과 다르다. 기존 `scripts/__pycache__/` 는 지우지 않는다.
15. 외곽 실행기는 자기 sha 를 기록만 한다 (자기 해시를 자기 안에 둘 수 없다). 나머지 열넷은 실행기가 봉인 표와 대조한다.
16. RED-R 은 v2 실행기 초안 바이트를 경로로 적재한다 (최상위 정의만 · `main` 미실행 · 우리 소스).
17. v1–v4 요청서 · 초안은 그대로 둔다 (지난 검토의 근거 바이트 · v2 실행기 초안은 RED-R 대상).
18. launcher 의 정리 루프 (`run_child` 의 kill 대기 · `group_status` 의 grace) 는 이번 V3-01 정정 대상이 아니다 — 관측을 먼저 하고 시간을 나중에 보는 모양이
    v3 와 같다. E1-0 은 E1-1–3 의 실자료 운영 실행이 아니지만, E1-0 대조 (l11 · l19) 는 실제 가짜 자식 프로세스의 정리를 일부 수행한다 (V4-N1). launcher 의
    운영 정리 정책 (공통 기한 등) 은 E1-1–3 요청에서 정한다 (§7).
19. V3-04 A 의 범위: 수동 기록은 Git 을 부르지 않는다. 절차 Git 앞의 이름 확인은 셸 env 의 `GIT_*` 이름만 본다 — `GIT_CONFIG_KEY / VALUE` 의 내용과 설정
    파일 등 모든 설정 원천까지 격리하지는 않으며 (§80), 절차 Git 의 결과는 증거가 아니다. 단계 사이의 HEAD 는 절차 커밋으로 바뀌고, 각 단계의 HEAD 는 그 단계의
    실행기 기록 (시작 · 끝 · 불변 확인) 이 정본이다.
20. 정리 안의 예외는 `cleanup.errors` · ledger (`cleanup.settle.first_error`) 에 남고 단계 수준 `errors` 에는 따로 넣지 않는다 — runner_ok 는 끝 상태 unknown
    으로 거짓이 된다. **그래서 meta 를 읽는 쪽은 최상위 `first_error=null` 만 보고 정리 오류가 없다고 판단하지 않는다 — `cleanup.status` · `cleanup.errors` 를
    본다 (§80).** `SubreaperFailed` 항목은 대조가 없다 (prctl 실패를 주입하지 않는다).
21. `unverified` 는 v4 에서 새로 생긴 끝 상태다 — runner_ok 에서는 empty 가 아닌 다른 상태와 같이 거짓이다.
22. V3-02 의 lstat 거부 (`entry_exists`) 는 작업 전 확인이다 — 검사 뒤 경쟁 변경까지 막는 원자적 보호가 아니다 (§80). 기록 파일 쓰기는 배타 생성 (`open(…,
    "x")`) 이 마지막 방어다.
23. S6: 두 git wrapper 가 `encoding="utf-8"` 을 명시한다. 그래서 HEAD · porcelain · config 목록도 같은 디코더로 읽고, 해석이 실행 환경 locale 에 기대지 않는다.
    대조 l27 · r11 은 그 키워드를 시험할 파일의 AST 로 확인한다 (파일을 읽기만 하고 실행하지 않는다).
24. V4-01 때문에 v4 가 GREEN 에 갔다면 l27 에서 `-x` 로 멈췄을 것이다 (§80 의 정적 판단). v4 를 실행하지 않았으므로 "실패를 관측했다" 나 "나머지는 통과했다"
    로 기록하지 않는다.
25. 대조 l14 의 `§80` 은 `build_argv` 의 형식 예시다 — 상태 문서 §80 의 내용과 관계없다.
26. S6 은 시험 대상 wrapper 둘에만 적용한다. 두 대조 파일의 fixture 도우미 `_git` 은 `text=True` 만 두고 `encoding` 을 두지 않는다 (v4 와 같음). 그 출력을
    쓰는 곳은 `rev-parse HEAD` · `hash-object` 의 객체 이름 (16 진수) 뿐이다. 비 UTF-8 바이트를 다루는 fixture 자기 확인은 `text` 없이 바이트로 받는다.

## 9. 하지 않는 것

E1-0b · E1-1–3 (identity · 읽기 경로 · fetch · 자료 개봉 · run) · C4-A / B · E3b · H4 · pickle · 노트북 · 출판 비교 · 해 선택 · 재시도 · 실행 중 예산 변경 ·
설치 · 환경 재구축 · 원자료 커밋 · 대체 출처 · COMSOL. 다섯 모듈 · 목록 · 기존 시험 · 기존 증거 · 봉인은 바꾸지 않는다.

## 10. 정하실 것

1. **사전 검토** — 이 요청과 초안 다섯을 Codex 에 보낸다 (권장 · 발송문 `docs/REIL_C4E_E1_PREREVIEW_SEND_v5_20261027.md`).
2. (검토 수용 뒤) **E1-0 한정 승인** — 승인해도 E1-0b · E1-1–3 은 시작하지 않는다.

# REIL C4-E · E1-0b 승인 요청 — FUTURE-01 (fetch 설정 원천 격리) · launcher 운영 정리 정책 · 대조 33 + 11 · E1-1–3 고정 계획 · 2026-10-30 KST (E1_0B_N1 정정 · 2026-11-03 · E1_0B_RESULT_N1 정정 · 시도 a2 · 2026-11-03)

> **승인 요청문이다 (실행 0).** 이번 승인 대상은 **E1-0b 뿐**이다 — launcher 대조 v8 의 RED (지금 저장소의 v5 고정 구현 바이트) 와 GREEN (v6 고정 구현 ·
> 기존 대조 포함 71) 을 **새 시도 `a2`** 의 증거 · 작업 · cache 경로로. E1-1–3 (identity · 읽기 경로 · fetch · run) 은 §7 에 고정 계획만 둔다 (**승인 대상
> 아님** · E1-0b 결과 검토 뒤 별도 요청 · 사용자 별도 승인).
> 근거:
> - 상태 문서 §86 — E1-0 결과 검토 회신 (`reviews/review_reil_c4e1_0_result_20261030/originals/`): `E1_0_RESULTS_ACCEPTED_WITH_RECORDED_PROCEDURAL_DEVIATION`.
>   Q3 — 다음 요청서에 RED 판정 문구 · FUTURE-01 / E1-0b 범위 · launcher 운영 정리 정책 · 오류 수용 기준 · 단계 및 전체 예산 · E1-1–3 의 대상 바이트 ·
>   입력 · 명령 · 예상 결과 · 중지 조건을 명시한다.
> - §87 — 사용자 범위 채택 ("권고대로"): 범위안 `docs/REIL_C4E_E1_0B_E1_1_3_SCOPE_20261030.md` (`9b94a31f…` · 커밋 `b9904cdf`) §9 의 권장 여섯.
> - §88 — 이 요청의 사전 검토 회신 (`reviews/review_reil_c4e_e1_0b_prereview_20261030/originals/`): `E1_0B_PREREVIEW_CHANGES_REQUIRED_BEFORE_APPROVAL` —
>   필수 보완 E1_0B_N1 (RED 원인 결속 · l23 · l29 · l30) · 숫자 정정 둘. Q1 · Q2 · Q3 · Q5 는 정적 범위에서 수용.
> - §89 — 사용자 정정 범위 채택 ("권고대로 해"): `docs/REIL_C4E_E1_0B_N1_SCOPE_20261030.md` (`69262ac4…` · 커밋 `59e11840`) — A (기대 assert 앞의
>   원인 구분) · 이 요청은 같은 경로에서 고쳐 쓴다 · 숫자 정정 · 공개 보강.
> - §90 — v2 사전 재검토 회신: E1_0B_N1 정적 종결 · 새 차단 0. §91 — 사용자 E1-0b 한정 승인 (지난 시도에 한 번 썼다).
> - §92 — 지난 시도의 결과: RED 에서 멈춤 (l33 의 실패 원인이 표와 다름 · 대조 결함) · GREEN 실행 안 함 (`evidence/reil_c4e1_0b_20261103/` 12 파일).
> - §93 — 결과 검토 회신 (`reviews/review_reil_c4e1_0b_result_20261103/originals/`): `STOP_HANDLING_ACCEPTED_E1_0B_INCOMPLETE_TEST_CORRECTION_REQUIRED` —
>   필수 정정 E1_0B_RESULT_N1 (l33 의 직접 호출이 fixture 의 `extra` 를 넘기지 않음) · 새 경로 · RED 33 전체 다시 · 이전 검토 l33 판단의 정정.
> - §94 — 사용자 정정 범위 채택 ("ㄱㄱ"): `docs/REIL_C4E_E1_0B_RESULT_N1_SCOPE_20261103.md` (`8a0586d4…` · 커밋 `fdc85e45`) §6 의 권장 다섯 — 범위 채택 ·
>   새 경로 A (시도 표지 `a2`) · l33 A (`extra` · `data` · `data_files` 모두 fixture 로) · 판정기 A (고정본 · 첫 시험 전 봉인) · 이 요청은 같은 경로에서
>   고쳐 쓴다.
>
> **이 파일은 같은 경로에서 두 번 고쳐 쓴 정정판이다.** 첫 사전 검토를 받은 바이트 (`112f033bce27cf4e8d9e942643e563a0997af9c20e9eb60f68e5fe86416cfb74` ·
> 51,720 B) 는 커밋 `90a842a9` 에, §91 의 승인으로 지난 시도에 쓴 바이트 (`38960400cf7830a5c15182e49d73bfc6e589f7590deb8f1838404dafc6f76caa` · 57,744 B) 는
> 커밋 `421d746e` (그 뒤 `fdc85e45` 까지 그대로) 에, 각각 회신 ZIP 의 `source/` 에도 그대로 있다. launcher 의 `REQUEST` 상수가 이 경로를 가리키므로
> launcher v6 바이트를 바꾸지 않으려고 경로를 유지했다. 이번에 바뀐 것: 대조 v8 · 실행기 대조 v5 · 실행기 v8 · 끝 기록 작성기 v2 · 판정기 (새) (§1-1) ·
> 새 경로 a2 (§1-1 · §4-1 · §4-2) · 기본값 결속 정적 대조 (§1-3 · 부록 A) · 판정기 (§4-2 · §4-3 · §4-5) · 예측 줄 (§4-3) · 봉인 (§4-4) · 기록 (§4-5) ·
> l33 (§6) · 공개 (§8 의 11 · 13 · 22–29).
>
> 순서: 이 요청 → Codex 사전 검토 → **사용자의 E1-0b 한정 승인 (새 승인 · 시도 a2)** → E1-0b → 결과 검토 → E1-1–3 승인 요청 → 검토 → 사용자 별도 승인.
> v1–v5 요청서 · 초안 · E1-0 증거 · 지난 시도의 증거 · 작업 폴더 · 고정본은 바꾸지 않는다.

## 0. 요약

| 단계 | 내용 | 이 요청의 승인 대상 |
|---|---|---|
| **E1-0b (시도 a2)** | 복사 다섯 (첫 시험 전 봉인 · launcher 는 v5 그대로) → RED `01_red_e1_0b` (launcher 대조 33 을 v5 고정 구현에서 — **9 실패 · 24 통과**) → 판정기 · 수동 판정 → 고정 구현 v6 복사 → GREEN `02_green_e1_0b` (E0 21 + N1 6 + launcher 33 + 실행기 11 = **71**) → 판정기 · 수동 판정 → 끝 기록 → 멈춤 | **예** |
| E1-1–3 | identity · 읽기 경로 (`add_repo`) · fetch · run 1 회 — launcher v6 (E1-0b GREEN 바이트) 경유 | 아니오 (§7 · 별도 승인) |

- 바뀌는 실행 코드는 launcher 하나다 (FUTURE-01 · 운영 정리 정책). 외곽 실행기 · 실행기 대조는 이름 규칙 · 봉인 표 · 작업 폴더만 바뀐다. 끝 기록
  작성기 · 판정기는 기록 도구다 (작성기는 판정하지 않고, 판정기는 §4-3 의 기준을 기계로 기록한다). 다섯 모듈 · SOURCES.json · 기존 시험 · 기존 증거는
  바꾸지 않는다.
- E1-0 의 절차 이탈 `E1_0_N1` (§86) 은 이렇게 적는다 — "E1-0 작업 범위에서 실행했으며, v5 §4-3 RED 근거 위치를 짧은 요약에서 동일 stdout 의 대응 실패
  절로 대체하고 계속한 절차 차이가 있다." 이번 RED 판정은 회신의 제안 문구를 쓰고 근거의 위치 · 형식을 미리 고정한다 (§4-3). 실제 출력이 그와 다르면
  **대체하지 않고 멈춘다**.
- launcher 대조: 기존 27 중 24 는 본문이 그대로이고 l14 · l23 · l25 를 고쳤으며 새로 여섯 (l28–l33) 을 넣었다 → 33. 실행기 대조 11 은 시험 본문이 그대로다.
- **E1_0B_N1 (§88 · 대조 v7 부터):** l23 · l29 · l30 은 기대 assert 바로 앞에서 원인을 구분한다. 기대 원인 밖 (탐침 · 준비 · 자식 · 정리 · 기록 실패 ·
  예상 밖 반환 · 추가 문제) 이면 RED 표에 없는 `('UNEXPECTED_RED_CAUSE', …)` 로 실패하고, 그것은 표와 다르므로 멈춘다. 시험 수 · RED 9 + 24 · GREEN 71 은
  같다.
- **E1_0B_RESULT_N1 (§93 · 대조 v8 · 시도 a2):** 지난 시도 (§91 · `evidence/reil_c4e1_0b_20261103/`) 는 RED 에서 l33 의 대조 결함으로 멈췄다 (§92). l33 의
  직접 호출 `L.postcheck` 에 fixture 의 `extra` · `data` · `data_files` 를 넘기고, 새 증거 · 작업 · cache 경로 (`a2`) 에서 RED 33 **전체**를 새 바이트로 다시
  한다 (지난 여덟의 일치를 이어 붙이지 않는다). 판정은 §4-3 이고, 첫 시험 전에 봉인한 판정기가 같은 기준의 기계 기록 (`<단계>.judge.json`) 을 남긴다 —
  수동 판정과 다르면 멈춘다. 메시지 · 시험 수 · RED 9 + 24 · GREEN 71 · 예산은 같다.

## 1. 고정 식별

### 1-1. 이번에 고정하는 초안 여섯 (정적 검사만 · 실행 0)

| 초안 (`bms-balancing/docs/`) | sha256 | bytes | 복사할 곳 (E1-0b 승인 뒤) |
|---|---|---:|---|
| `REIL_C4E1_LAUNCHER_DRAFT_v6_20261030.py.txt` — launcher v6 (**바뀌지 않음**) | `2c70712381aec657f81c8e72c85e8c06e654364aefe9e38e5254ecfece9e4ebf` | 62,639 | `scripts/reil_c4e1_launch.py` (GREEN 직전 · 단계 d) |
| `REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v8_20261103.py.txt` — launcher 대조 33 (정정판 v8 · E1_0B_RESULT_N1) | `49d3fa36b5928b92584da158a3ac234ddf83bbc79c7d3c349fd96bc5c1bf9001` | 74,542 | `tests/test_reil_c4e1_launch.py` (b) |
| `REIL_C4E1_RUNNER_CONTROLS_DRAFT_v5_20261103.py.txt` — 외곽 실행기 대조 11 (v5 · 이름 규칙 a2) | `b34fb9a98eb6e852d4c30038ee988adee57d03c2b138e767ca742ea327a45e13` | 37,003 | `tests/test_reil_c4e1_runner.py` (b) |
| `REIL_C4E1_STEP_RUNNER_DRAFT_v8_20261103.py.txt` — E1-0b 외곽 실행기 v8 (봉인 표 포함 · 이름 규칙 · 작업 폴더 a2) | `e284f8a14a5f15f405b566ab668a58f069a6ab465a25e391a36ce28f1fdf9059` | 36,938 | `<E>/00_step_runner.py` (b) |
| `REIL_C4E1_0B_END_WRITER_DRAFT_v2_20261103.py.txt` — 끝 기록 작성기 v2 (이름 규칙 a2 · 판정 기록 읽기) | `2f316acc348412cafd8607ef7fe0d19a579237e21c4535ab2a657ca090a5472b` | 4,875 | `<E>/00_end_writer.py` (b) |
| `REIL_C4E1_0B_JUDGE_DRAFT_20261103.py.txt` — 판정기 (새 · §4-3 의 기계 기록) | `3749b32edd3954fdfa4bfe92336d9eafaf2121b6275c9bd0b3584ece42dc60c4` | 21,889 | `<E>/00_judge.py` (b) |

`<E>` = `/home/user/Yonghoon-DEM-DFT/bms-balancing/evidence/reil_c4e1_0b_a2_<착수 UTC 날짜 YYYYMMDD>` (실행기 · 작성기 · 판정기가 이름 규칙을 확인한다 ·
지난 시도의 `reil_c4e1_0b_20261103` · E1-0 의 `reil_c4e1_0_<날짜>` · E1-1–3 의 `reil_c4e1_<날짜>` 와 다른 폴더). 작업 폴더 = `SP/c4e1_0b_a2_steps` (실행기
v8 의 `WORK` · pycache 는 `SP/c4e1_0b_a2_steps/pycache/<단계>`). 지난 시도의 고정본 (대조 v7 `3f9d2f25…` · 실행기 대조 v4 `d9880f28…` · 실행기 v7
`c5aab7c3…` · 작성기 v1 `2e44f2e5…`) 은 `docs/` 에 그대로 두고 이번에 쓰지 않는다.

### 1-2. 바뀌지 않는 것 (읽기 대조만)

- **launcher v5 고정 구현** = 지금 저장소의 `scripts/reil_c4e1_launch.py` (`2269d775f1701e2f657d386f42bc950d26a6b56bd37323611dd6ab4cc1a75396` · 51,957 B ·
  E1-0 GREEN 바이트 · v5 초안과 같은 바이트). RED 의 대상이고 단계 d 에서 v6 로 바뀐다.
- **봉인 표의 나머지 열하나** (HEAD blob = 작업 트리 · §4-4):
  - `tests/test_reil_c4e.py` (`687de63c…` · 57,482) · `tests/test_reil_c4e_fix.py` (`7a09d438…` · 19,506).
  - 다섯 모듈: `reil_c4e_run.py` (`a94f535f…`) · `reil_c4_e3a.py` (`33b85537…`) · `reil_c4_monitor.py` (`e6ef8ff6…`) · `reil_c5_pilot.py` (`73bee8dc…`) ·
    `reil_p0.py` (`793b326e…`).
  - S1 의 둘: `scripts/reil_c6_profile.py` (`408afc4b…`) · `degradation-degeneracy/tools/env_profile.py` (`83b0d836…`).
  - `evidence/reil_c4e0_fix_20261014/04_sources/SOURCES.json` (`2a7b2b49…`).
  - `docs/REIL_C4E1_STEP_RUNNER_DRAFT_20261020.py.txt` (`aae2ec14…` · v2 실행기 초안 — 목록에만 있고 E1-0b 는 적재하지 않는다).
- E1-0 증거 (`evidence/reil_c4e1_0_20261030/` 24 파일) · v1–v5 요청서 · 초안 · E1-0 끝 기록 작성기 사본 (`docs/REIL_C4E1_0_END_WRITER_COPY_20261030.py.txt`).
- **지난 시도 (§91–§93):** 증거 `evidence/reil_c4e1_0b_20261103/` (12 파일 · 69,968 B) · 작업 폴더 `SP/c4e1_0b_steps` · 결과 검토 회신 원문 — 지우거나 ·
  다시 쓰거나 · 이름을 바꾸지 않는다. 지금 저장소의 `tests/test_reil_c4e1_launch.py` (= 대조 v7) · `tests/test_reil_c4e1_runner.py` (= 실행기 대조 v4) 는
  지난 시도의 b 에서 복사한 것이고, 이번 b 에서 v8 · v5 로 덮어쓴다 (커밋 이력에 남는다).

### 1-3. 정적 검사 (실행 0 — 초안 · 대조 · Git fixture 모두)

- AST 파싱 여섯 · ruff `--isolated --select F,E9,B006,B008` 여섯 모두 0 건 · 이름 검사 (파일마다): 미해결은 `__file__` (launcher `launch` · 실행기
  `run_step` · 판정기 `main` — 모듈 속성 · 오탐) 뿐.
- **속성 대조:** launcher 대조 v8 의 `L.*` 참조 49 가 v6 에 모두 있다 (`__file__` 제외). v5 바이트에 없는 것은 일곱 (`CLEANUP_S` · `POLL_S` ·
  `FETCH_GIT_CONFIG` · `FETCH_LOCAL_KEYS` · `fetch_env` · `git_config_entries` · `cleanup_group`) 이고, 이 이름은 RED 실패로 정한 아홉 시험 안에서만, 그
  시험의 예측 실패 줄 이후에만 쓰인다 (l14 485 · 487 · 488 ≥ 465 · l23 713 ≥ 712 · l28 902 · l31 1004 · l32 1035 — 도우미 · 원인 구분 · 나머지 24 시험은
  쓰지 않는다 · AST). 실행기 대조 v5 의 `R.*` 16 은 실행기 v8 에 모두 있다.
- **원인 구분 (E1_0B_N1):** l23 · l29 · l30 의 원인 구분과 도우미 `_normal_fetch_meta` 는 `pre` · meta 사전 · 문자열만 읽는다 (`L` 은 `__file__` 만).
- **기본값 결속 정적 대조 (E1_0B_RESULT_N1 · 범위안 §2 · 도구 원문은 부록 A · AST 만):** 대조 파일이 launcher / 실행기 함수를 부르는 곳마다 (직접 호출 +
  같은 함수 안의 지역 별칭 호출) 기본값이 모듈 상수인 인자 중 넘기지 않은 것을 나열했다. **규칙:** tmp fixture 시험의 호출이 실파일 · 실해시 · 실제 시스템을
  가리키는 기본값을 **읽고** 그 결과를 단언에 쓰면 결함이다. 그 밖은 아래 분류 중 하나로 근거를 적는다. 결과 — 대조 v8 → launcher v6 18 행 · → v5 14 행 ·
  실행기 대조 v5 → 실행기 v8 12 행 · **결함 0** (대조 v7 의 l33 `L.postcheck` 행 — `extra` · `data` · `data_files` — 은 v8 에서 사라졌다):

  | 호출 (줄은 대조 v8 / 실행기 대조 v5) | 기본값을 쓰는 인자 | 분류 |
  |---|---|---|
  | `_pre` 198 `L.precheck` | `helper_sha256` | identity 단계에서만 읽힌다 — 그 단계로 `_pre` 를 부르는 l33 은 `pre` 의 목록 항목만 쓰고 `ok` 를 쓰지 않는다 (읽히지만 단언에 쓰이지 않음) |
  | `_pre` 196 · l5 324 `L.build_argv` | `venv` | argv 문자열만 만든다 (파일 읽기 없음) |
  | l8 362–372 `L.identity_link` (다섯) | `relpaths` (`MODULE_RELPATHS`) | 고정 모듈 목록 (정책) |
  | l14 495 · 502 · 503 · 507 `L.build_argv` (넷) | `py` · `bms` · `venv` · `seal` · `data` · `sources` · 해시 둘 | 생산 고정 argv 를 일부러 시험한다 (문자열 비교) |
  | l27 839 `L.git_run` | `timeout` | 정책 상수 |
  | l28 908 · 913 (호출 셋 — 913 줄에 둘) `L.fetch_env` (별칭 `fetch_env` · v6 만) | `config` (`FETCH_GIT_CONFIG`) | 고정 목록 (정책) — l28 이 그 목록을 일부러 시험한다 |
  | l30 978 `L.fetch_source_postcheck` (v6 만) | `config` · `local_keys` | 생산 고정 목록을 일부러 시험한다 |
  | `_launch` 208 `L.launch` (`**opts` — 도구는 그 안을 못 본다 · 수동 분류) | `opts` 가 repo · py · venv · seal · work · data · data_files · sources · 해시 셋 · extra · timeouts · env_base 를 넘긴다 · 남는 것 `helper_sha256` · `kill_wait` · `grace` · `cleanup_s` (v6) · `proc` | `proc` = 실제 /proc (실제 프로세스 대조 l11 · l19 의 의도) · 정리 상수 = 정책 · `helper_sha256` = identity 단계 launch 에서만 읽힘 — identity 단계로 `_launch` 를 부르는 시험은 없다 |
  | r1 229 · r11 561 `R.settle` | `limit` · `proc` | `limit` = 정책 · `proc` (실제 /proc) 는 그 경로에서 읽히지 않음 — 두 시험 모두 `R.proc_table` 을 인자를 무시하는 가짜로 바꾼다 (r11 의 가짜는 tmp 가짜 /proc 폴더만 읽는다) |
  | r2 248 · r3 268 · 281 · 288 · r9 473 · r10 500 · 519 `R.cleanup` (별칭 `cleanup`) | `proc` · `kill_wait_s` · `settle_s` | `proc` = 위와 같이 읽히지 않음 (모두 `R.proc_table` 을 가짜로 바꾼다) · `kill_wait_s` · `settle_s` = 정책 (기한 15 s = 7 + 3 + 5 의 근거) |
  | r4 313 · 314 · r11 575 `R.git` | `timeout` | 정책 상수 |

- **봉인 표:** 실행기 v8 의 `_FIXED` · `RED_LAUNCH` · `IMPL` (AST literal) = 대조 초안 둘 (v8 · v5) · 열하나 (HEAD blob · 작업 트리 둘 다) · 저장소 launcher
  (v5 · HEAD blob · 작업 트리) · launcher v6 초안 — 15 행 · 27 비교 · 불일치 0.
- **최상위 노드 비교 (AST):** 바뀐 곳은 §3 의 목록뿐이다. 이번 — 대조 v7 → v8 바뀜 둘 (docstring · l33) · 같은 77 / 실행기 대조 v4 → v5 바뀜 넷
  (docstring · `V4` · 수집 조건 문장 · `_rtree`) · 같은 48 / 실행기 v7 → v8 바뀜 다섯 (docstring · `WORK` · `EVIDENCE_NAME` · `_FIXED` · `run_step`) · 같은 56 /
  작성기 v1 → v2 는 diff 로 봤다 (§4-5). 그대로인 것 — launcher v5 → v6 88. 지난 판의 수 (대조 v5 → v7 62 · v6 → v7 74 · 실행기 v5 → v7 53 · v6 → v7 59 ·
  실행기 대조 v3 → v4 **46** — 발송문 · §87 의 47 은 틀린 값 · §88) 는 그대로 둔다.
- **끝 기록 작성기 v2 · 판정기:** import 는 작성기 datetime · hashlib · json · re · shutil · sys · pathlib · 판정기 ast · datetime · hashlib · json · re · sys ·
  pathlib 뿐 · subprocess · socket · os · exec · eval 없음 · 쓰기는 각각 `open(…, "x")` 하나 (`03_end.json` · `<단계>.judge.json`).
- **판정기의 GREEN 기대 집합:** 네 시험 파일 (기존 둘 · 대조 v8 · 실행기 대조 v5) 의 최상위 함수는 `test_*` 뿐이다 (21 · 6 · 33 · 11) — `test` 로 시작하는
  다른 이름 · `Test*` 클래스 · `test*` 이름의 import · 대입 · 데코레이터 0 (pytest 가 모으는 집합과 같다).
- **판정기 · 작성기의 작성자 확인 (저장소 밖 스크래치 사본에만 · 시험 · launcher · Git fixture 0):** §8 의 27.
- 비밀 검사 (커밋 전 · 0 건).

## 2. 범위 ↔ 정정 · 대조

| 범위안 (§87 채택) | 정정 (launcher v6) | 대조 |
|---|---|---|
| §1 RED 판정 문구 | 요청서 §4-3 — 회신 제안 문구 + 근거 위치 · 형식 고정 · 다르면 멈춤 | — |
| §2 FUTURE-01 = A | `fetch_env` · `git_config_entries` · `config_source_problems` (새) · `fetch_source_precheck` / `fetch_source_postcheck` 가 fetch env 와 `--show-scope --show-origin` 을 쓴다 · `launch` 가 fetch 단계 전체에 fetch env · meta `env_git_config` | l23 (다시 씀) · l25 (고침) · l28 · l29 · l30 (새) |
| §2 프록시 인증 키 = 읽어 넣음 | `FETCH_GIT_CONFIG = (("http.proxyAuthMethod", "basic"),)` — 값은 2026-10-30 에 한 번 읽었다 (§8 의 5) | l14 (상수) · l23 · l28 |
| §3 운영 정리 정책 = A | `CLEANUP_S` 20 · `POLL_S` 0.1 · `group_status(until=…)` · `cleanup_group` (새) · `run_child` 가 정리 원점에서 기한 한 번 · `postcheck` 가 `deadline_hit` 확인 | l31 · l32 · l33 (새) · 기존 l11 · l18 · l19 (회귀) |
| §4 오류 수용 = 무관용 · 둘로 나눠 기록 | E1-1–3 요청에서 고정한다 (launcher 의 단계 판정식은 v5 와 같다) | §7 |
| §5 구조 = A (따로 승인) | 이 요청은 E1-0b 만 | — |
| §6 기록 보강 = 포함 | 외곽 반환 파일 `<단계>.outer_rc.txt` · 끝 기록 작성기 고정본 | §4-2 · §4-5 |
| (요청서 경로) | `REQUEST = "docs/REIL_C4E_E1_0B_APPROVAL_REQUEST_20261030.md"` | l14 |
| §88 E1_0B_N1 (§89 채택 · A) | — (launcher 그대로) | l23 · l29 · l30 의 원인 구분 · 도우미 `_normal_fetch_meta` (대조 v7 부터) |
| §93 E1_0B_RESULT_N1 (§94 채택 · 범위안 §1 A) | — (launcher 그대로) | l33 의 직접 호출 `L.postcheck` 에 fixture 의 `extra` · `data` · `data_files` (대조 v8) |
| 범위안 §2 (기본값 정적 대조) | — | 부록 A 의 도구 (v2 — 지역 별칭 호출 포함) · §1-3 의 결과 (결함 0) |
| 범위안 §3 A (새 경로 a2) | 외곽 실행기 v8 (`EVIDENCE_NAME` · `WORK` · 거부 메시지) · 끝 기록 작성기 v2 (이름 규칙) · 판정기 (이름 규칙) | 실행기 대조 v5 (`V4` · 수집 오류 문구 · `_rtree`) |
| 범위안 §4 A (판정기) | 판정기 초안 (`<E>/00_judge.py`) · 작성기 v2 의 판정 기록 읽기 | §4-3 (판정의 정본 · 판정기의 읽기 규칙) |

## 3. 바뀐 곳 (정본은 초안 — 최상위 노드 AST 비교)

### 3-1. launcher v5 → v6

| 노드 | v6 줄 | 변경 |
|---|---|---|
| 모듈 docstring | 1–51 | 승인 · 범위 문서 · 운영 정리 정책 · fetch env |
| `CLEANUP_S` · `POLL_S` | 112 · 113 | 새 — 20.0 · 0.1 |
| `FETCH_GIT_CONFIG` · `FETCH_LOCAL_KEYS` | 116 · 118–119 | 새 — 고정 목록 하나 · local 허용 키 아홉 |
| `REQUEST` | 120 | 이 요청서 경로 |
| `fetch_env` | 398–406 | 새 |
| `git_config_entries` | 422–433 | 새 — `scope<TAB>origin<TAB>key=value` → (scope, origin, 소문자 key, value) · 세 칸이 아닌 줄은 `("?", 줄, "", "")` |
| `git_config_problems` | 436–445 | 세 칸 형식을 읽는다 (금지 키 · TLS 끔 규칙은 같다) |
| `config_source_problems` | 448–459 | 새 — command 항목 = 고정 목록 정확히 · 그 밖 원천은 (사후에만) local 허용 키 |
| `fetch_source_precheck` | 462–475 | fetch env · `--show-scope --show-origin` · 원천 검사 · `env_git_config` 기록 |
| `fetch_source_postcheck` | 478–504 | fetch env · 받은 저장소의 `config --list --show-scope --show-origin` · 원천 · 금지 키 검사 |
| `postcheck` | 601–635 | `deadline_hit is not False` → 문제 (한 항 추가) |
| `group_status` | 695–715 | `until` (절대 시각) 전에만 관측 시작 · 남은 시간만 sleep · 관측 0 → unverified · `clock` / `sleep` 주입 |
| `cleanup_group` | 731–774 | 새 — v5 `run_child` 의 정리 부분을 옮기고 V3-01 규칙을 맞췄다 |
| `run_child` | 777–807 | 대기 뒤 정리 원점에서 기한 한 번 · `cleanup_group` 호출 · 기록 키 (`deadline_hit` · `emergency` · `cleanup_deadline_s`) |
| `launch` | 816–915 | `cleanup_s` 인자 · meta `cleanup_deadline_s` · fetch 단계면 `env = fetch_env(env)` · meta `env_git_config` |

같은 것: 최상위 노드 88 (+ `if __name__` 블록).

### 3-2. FUTURE-01 — fetch 단계의 설정 원천 (범위안 §2 A)

- **fetch env** = 정제 env (`child_env` — v5 와 같다) 에서 `GIT_CONFIG*` 이름을 다시 모두 빼고 `GIT_CONFIG_NOSYSTEM=1` · `GIT_CONFIG_GLOBAL=/dev/null` ·
  `GIT_CONFIG_COUNT=1` · `GIT_CONFIG_KEY_0=http.proxyAuthMethod` · `GIT_CONFIG_VALUE_0=basic`. 받은 env 는 바꾸지 않고, 두 번 적용해도 같다.
- **적용 범위:** `launch` 는 fetch 단계면 그 env 를 사전 대조 (탐침 포함) · 기록 git · 자식 · 사후 대조에 모두 쓴다. run 의 fetch 는 자식 env 를
  물려받으므로 (`reil_c4e_run.py` l.690) 다섯 모듈을 바꾸지 않고 run 의 git 셋 (`init -q` · `remote add origin` · `fetch --depth 1 --filter=blob:none origin
  <커밋>` — l.668–669) 과 읽기 `show <커밋>:<경로>` (l.673) 모두에 걸린다.
- **사전:** 작업 폴더 (저장소 밖) 에서 `git config --list --show-scope --show-origin` → command 항목 = 고정 목록 정확히 · 그 밖 원천 항목 0 · 금지 키 ·
  TLS 끔 0 / `ls-remote --get-url <고정 URL>` = 고정 URL.
- **사후:** 받은 저장소 (`data/git`) 에서 같은 목록 → command 항목 = 고정 목록 · local 원천은 `FETCH_LOCAL_KEYS` 의 키만 — `core.repositoryformatversion` ·
  `core.filemode` · `core.bare` · `core.logallrefupdates` · `remote.origin.url` · `remote.origin.fetch` · `remote.origin.promisor` ·
  `remote.origin.partialclonefilter` · `extensions.partialclone`. 그 밖 키 (`include.*` · `includeif.*` · `http.*` 등) 가 하나라도 있으면 문제다.
  `remote.origin.url` · 유효 출처 · shallow · alternates 검사는 v5 와 같다.
- 다른 단계 (identity · run) 의 env 는 v5 와 같다 (정제 env · `GIT_CONFIG*` 없음 · 시스템 · 사용자 설정은 읽힌다 — §8 의 6).

### 3-3. launcher 운영 정리 정책 (범위안 §3 A)

- **기한:** `run_child` 는 자식이 끝나거나 timeout (또는 대기 예외) 이 되면 정리 원점 `t_c0` 와 공통 절대 기한 `t_c0 + 20 s` (명목 배정 kill 대기 10 +
  관측 5 + 재관측 5) 를 한 번 만들어 `cleanup_group` 에 넘긴다. `cleanup_group` 은 기한을 만들지 않는다.
- **순서:** timeout 이면 그룹 SIGKILL → `poll` 로 자식 종료를 비차단 확인하며 0.1 s 씩 (kill 대기 끝과 기한 중 이른 쪽까지) → 관측 창 (`min(기한,
  지금 + 5 s)`) → alive 면 그룹 SIGKILL (기한 뒤라도 보낸다) → 재관측 창 (`min(기한, 지금 + 5 s)`). 재관측이 empty 면 `killed`.
- **기한 규칙:** 모든 관측 · sleep 은 `지금 < 창 끝` 일 때만 시작하고, sleep 은 남은 시간만큼만 잔다. 기한을 넘을 수 있는 것은 기한 전에 시작한 관측
  하나와 그 결과에 따른 즉시 동작 (SIGKILL) · 비차단 확인 (`poll`) · 기록뿐이다.
- **끝 상태:** empty · killed · alive · unverified (관측 0 · 재kill 뒤 재관측 0) · unknown (관측 오류 · 정리 안의 예외 — 우선). 정리 안의 예외는
  `cleanup_group` 이 잡아 `errors` 에 남기고 같은 기한으로 비상 동작 (자식이 살아 있으면 그룹 SIGKILL · 기한까지 관측) 만 한다.
- **기록:** `group` (끝 상태 포함) · `group_first` · `kill` · `exited_after_kill` · `deadline_hit` · `emergency` · `cleanup_deadline_s` · `wait_s` (시작 →
  종료 또는 timeout) · `cleanup_s` (정리 원점부터).
- **차단 (범위안 §3):** `group.status` ≠ empty · `deadline_hit` ≠ false · timeout 뒤 미종료 · `errors` 있음 · 기록 (HEAD · porcelain) 실패 — 하나라도
  있으면 사후 대조 실패 → 단계 판정 false. `first_error` 는 첫 오류 그대로이고, 판정 · 소비자는 그것 하나로 정리의 성공을 판단하지 않는다.
- **v5 와 다른 행동:** v5 는 `p.wait(timeout=kill_wait)` 로 기다렸고, 관측을 먼저 하고 시간을 나중에 봤으며 (grace 를 넘은 뒤 관측 한 번 더), 공통 기한이
  없었고, 재kill 뒤 empty 를 `alive_then_killed` 로 적었다 (사후 대조는 v5 도 실패로 봤다). `wait_s` 는 v5 가 kill 대기를 포함했고 v6 는 그 시간을
  `cleanup_s` 에 넣는다.

### 3-4. 그 밖의 초안

- **launcher 대조 v5 → v6:** docstring · `FETCH_GIT` / `FETCH_NAMES` (새 상수) · `FAKE_RUN` (fetch 에 `localtls` · `localinclude` 모드 둘 추가 · 다른 모드는
  같다) · l14 (첫 문장 = 요청서 경로 · 상수 단언 · 승인 문구) · l23 (v5 의 `test_l23_fetch_precheck_refuses_url_rewrite_proxy_and_tls_off_settings` 를 지우고
  `test_l23_user_level_…` 로 다시 씀) · l25 (끝 단언 둘) · 도우미 `_Clock` · `_P` · `_fake_group` · l28–l33 (새). 그 밖 최상위 노드 62 는 같다.
- **외곽 실행기 v5 → v6:** docstring · `WORK` (`SP/c4e1_0b_steps`) · `EVIDENCE_NAME` (`reil_c4e1_0b_`) · `_FIXED` (대조 둘의 행) · `SKELETON` →
  `RED_LAUNCH` (v5 고정 구현) · `IMPL` (v6) · `EXPECT` (단계 둘) · `run_step` 의 거부 메시지 한 줄. 정리 · 기록 코드는 v5 (E1-0 · §86 수용) 와 같다.
- **실행기 대조 v3 → v4:** docstring · `V4` (`reil_c4e1_0b_`) · 수집 오류 메시지 (`<E0b>`) · 건너뜀 메시지 · `_rtree` 의 tmp 증거 폴더 이름 · r5 의 단계
  이름 (E1-0b 의 둘). 시험 본문의 입력 · 기대는 같다.
- **끝 기록 작성기 (새):** §4-5.
- **launcher 대조 v6 → v7 (E1_0B_N1):** docstring · l23 (심은 키 표 · 원인 구분) · l29 (반환 ∈ {0, 1} · meta · 원인 구분) · l30 (반환 ∈ {0, 1} · meta 읽기를
  기대 assert 앞으로 · 원인 구분) · 도우미 `_normal_fetch_meta` (새). 그 밖 최상위 노드 74 는 같다. 시험 이름 · 기대 assert · 메시지는 그대로다.
- **외곽 실행기 v6 → v7:** docstring · `_FIXED` 의 launcher 대조 행. 그 밖 59 는 같다.
- **launcher 대조 v7 → v8 (E1_0B_RESULT_N1):** docstring (머리 · E1_0B_RESULT_N1 문단) · l33 (도우미 `post()` 의 직접 호출에 `extra=t.extra` · `data=t.data` ·
  `data_files=t.data_files` · 시험 docstring 한 문장). 그 밖 최상위 노드 77 은 같다. 시험 이름 · 기대 assert · 메시지 · 하위 사례의 순서는 그대로다.
- **실행기 대조 v4 → v5 (새 경로 a2):** docstring · `V4` (`reil_c4e1_0b_a2_20[0-9]{6}/00_step_runner\.py`) · 수집 오류 문구 (`<E0b>` → 경로 꼴) · `_rtree` 의
  tmp 증거 폴더 이름 (`reil_c4e1_0b_a2_20990101`). 그 밖 48 은 같다 (시험 본문의 입력 · 기대 그대로).
- **외곽 실행기 v7 → v8 (새 경로 a2):** docstring · `WORK` (`SP/c4e1_0b_a2_steps`) · `EVIDENCE_NAME` (`^reil_c4e1_0b_a2_20[0-9]{6}$`) · `_FIXED` 의 대조 두
  행 (v8 · v5) · `run_step` 의 거부 메시지 한 줄. 그 밖 56 은 같다 (정리 · 기록 코드는 v5 · E1-0 바이트 그대로).
- **끝 기록 작성기 v1 → v2:** §4-5 (이름 규칙 a2 · 복사본에 판정기 · 판정 기록 읽기 · 끝 출력에 판정 verdict).
- **판정기 (새):** §4-3 · §4-5.

## 4. E1-0b 절차 (이 요청의 승인 대상)

### 4-1. 순서 · 배정

| # | 단계 | 배정 | 기대 | 어긋나면 |
|---|---|---|---|---|
| a | 절차 Git 이름 확인 (§4-6) → 승인 기록 § · 보존 규칙 (`bms-balancing/.gitattributes` 에 `evidence/reil_c4e1_0b_a2_<날짜>/** -text`) 커밋 → `<E>` 만들기 — `evidence/reil_c4e1_0b_a2_*` 가 하나라도 있거나 `SP/c4e1_0b_a2_steps` 가 있으면 멈춤 (지난 시도의 `evidence/reil_c4e1_0b_20261103` · `SP/c4e1_0b_steps` 는 그대로 두고 보지도 쓰지도 않는다) | — | 허용 목록 밖 0 | 멈춤 |
| b | **복사 다섯 · 첫 시험 전 봉인:** 대조 둘 → `tests/` · 실행기 → `<E>/00_step_runner.py` · 작성기 → `<E>/00_end_writer.py` · 판정기 → `<E>/00_judge.py` → `00_start.txt` (§4-5 · Git 없음) → 복사본 sha = §1-1 확인 → 커밋. launcher 는 v5 그대로 | — | sha 일치 | 멈춤 |
| c | **RED** `01_red_e1_0b` (실행기) → 외곽 반환 파일 → 판정기 (`01_red_e1_0b.judge.json`) → 수동 판정 (§4-3) → 커밋 | pytest 120 s + 정리 ≤ 15 s + 기록 | §4-3 · 판정기 MATCH · 둘이 같음 | 멈춤 → e |
| d | 고정 구현 v6 복사 (sha 대조) → **GREEN** `02_green_e1_0b` (71 · `-x`) → 외곽 반환 파일 → 판정기 (`02_green_e1_0b.judge.json`) → 수동 판정 → 커밋 | pytest 600 s + 정리 ≤ 15 s + 기록 | §4-3 · 판정기 MATCH · 둘이 같음 | 멈춤 → e |
| e | 절차 Git 이름 확인 → `03_end.json` (작성기 · Git 없음) → 비밀 검사 → 커밋 → push → 결과 기록 § → 결과 검토 발송문 → **멈춤** | — | 허용 목록 밖 0 | 멈춤 (기록만) |

- **멈춤** = 다음 시험 단계로 가지 않는다. 재시도 · 수정 · 다른 근거로의 대체를 하지 않는다. c · d 에서 멈추면 그 단계의 기록 (증거 · 외곽 반환 · 판정
  기록) 을 있는 그대로 커밋하고 e 를 한다 (작성기는 없는 meta · 외곽 반환 · 판정 기록을 사유로 남긴다).
- **판정기:** c · d 에서 외곽 반환 파일 직후 한 번씩 띄운다. verdict 가 STOP 이거나, 수동 판정과 다르거나, 판정기가 기록을 쓰지 못하면 (반환 2 · 예외 ·
  파일 없음) 그 자리에서 멈춘다 — 판정기 출력을 고치거나 다시 돌리지 않고, 판정기 없이 계속하지도 않는다.
- **정리 ≤ 15 s** = 외곽 실행기의 공통 절대 기한 (정리 원점부터 · v5 와 같다). launcher 의 20 s 기한은 대조 안의 launcher 호출 (가짜 자식) 에만 걸린다.
  **기록** = 단계마다 Git 넷 (각 timeout 60 s · 시작 둘 · 끝 둘 · 정제 env) · 원천 해시 두 번 · meta — 정리 밖의 별도 배정이다.
- E1-0b 전체 (a → e 의 끝 기록) ≤ 2 h. 재시도 0 · 예산 변경 0. 끝 기록은 커밋 · push · 문서 전 snapshot 이다. 판정기 · 작성기는 따로 배정하지 않는다
  (각각 파일 몇 개를 읽고 기록 하나를 쓴다 · 전체 예산 안).

### 4-2. 정확한 명령 (BMS = `/home/user/Yonghoon-DEM-DFT/bms-balancing` · SP = 스크래치패드 · 실제 명령은 절대 경로로 풀어 쓴다)

```
a  <확인> && git add …(.gitattributes · 상태 문서) && <확인> && git commit …
   ! compgen -G 'BMS/evidence/reil_c4e1_0b_a2_*' > /dev/null && test ! -e SP/c4e1_0b_a2_steps && mkdir <E>
b  cp BMS/docs/REIL_C4E1_LAUNCHER_CONTROLS_DRAFT_v8_20261103.py.txt BMS/tests/test_reil_c4e1_launch.py
   cp BMS/docs/REIL_C4E1_RUNNER_CONTROLS_DRAFT_v5_20261103.py.txt   BMS/tests/test_reil_c4e1_runner.py
   cp BMS/docs/REIL_C4E1_STEP_RUNNER_DRAFT_v8_20261103.py.txt       <E>/00_step_runner.py
   cp BMS/docs/REIL_C4E1_0B_END_WRITER_DRAFT_v2_20261103.py.txt     <E>/00_end_writer.py
   cp BMS/docs/REIL_C4E1_0B_JUDGE_DRAFT_20261103.py.txt             <E>/00_judge.py
   set -C; { date -u +%Y-%m-%dT%H:%M:%SZ; df -B1 --output=avail /home/user/Yonghoon-DEM-DFT;
             sha256sum <초안 여섯> <복사본 다섯> BMS/scripts/reil_c4e1_launch.py; } > <E>/00_start.txt
   <확인> && git add -f <복사본 다섯> <E>/00_start.txt && <확인> && git commit …
c  /usr/bin/python3.11 -I <E>/00_step_runner.py 01_red_e1_0b 120 -- <RED argv>; rc=$?; set -C; printf '%s\n' "$rc" > <E>/01_red_e1_0b.outer_rc.txt
   /usr/bin/python3.11 -I <E>/00_judge.py <E> 01_red_e1_0b
d  cp BMS/docs/REIL_C4E1_LAUNCHER_DRAFT_v6_20261030.py.txt BMS/scripts/reil_c4e1_launch.py && sha256sum BMS/scripts/reil_c4e1_launch.py
   /usr/bin/python3.11 -I <E>/00_step_runner.py 02_green_e1_0b 600 -- <GREEN argv>; rc=$?; set -C; printf '%s\n' "$rc" > <E>/02_green_e1_0b.outer_rc.txt
   /usr/bin/python3.11 -I <E>/00_judge.py <E> 02_green_e1_0b
e  chk=$(<확인>) && /usr/bin/python3.11 -I <E>/00_end_writer.py <E> "$chk"

RED argv:
  /usr/bin/env PYTHONPATH=SP/reil_c4env/pytest_t SP/reil_c4env/venv/bin/python -X pycache_prefix=SP/c4e1_0b_a2_steps/pycache/01_red_e1_0b
      -m pytest -p no:cacheprovider tests/test_reil_c4e1_launch.py -q -rA --tb=short
GREEN argv:
  /usr/bin/env PYTHONPATH=SP/reil_c4env/pytest_t REIL_C4E1_RUNNER_UNDER_TEST=<E>/00_step_runner.py
      SP/reil_c4env/venv/bin/python -X pycache_prefix=SP/c4e1_0b_a2_steps/pycache/02_green_e1_0b
      -m pytest -p no:cacheprovider -x tests/test_reil_c4e.py tests/test_reil_c4e_fix.py tests/test_reil_c4e1_launch.py tests/test_reil_c4e1_runner.py
      -q -rA --tb=short
```

- `<확인>` = §4-6 의 이름 확인 명령. `compgen -G` 는 bash 내장이고 일치하는 이름이 하나라도 있으면 성공한다 (그러면 `!` 로 멈춘다). d 의 sha256 은
  `2c707123…ebf` 여야 하고 다르면 GREEN 을 띄우지 않고 멈춘다. RED · GREEN argv 는 E1-0 · 지난 시도와 같고 pycache 폴더만 다르다 (`SP/c4e1_0b_a2_steps`).
- **셸 도구의 실행 방식 (§91 과 같다):** GREEN 의 최악 소요 (pytest 600 s + 정리 15 s + 기록) 가 이 세션 셸 도구의 전경 상한 (600 s) 을 넘을 수 있어,
  d 의 GREEN 명령 줄은 도구의 배경 실행으로 띄우고 끝 알림을 받는다 (명령 문자열 · 외곽 반환 기록은 같다). RED · 판정기 · 작성기는 전경으로 띄운다.
- env (실행기가 만든다 · v5 와 같다): 현재 env → `base_env` (비밀 형태 이름 · SSH_ASKPASS · GIT_SSL_CAINFO 밖의 모든 GIT_* 제거 · 이름만 기록 ·
  GIT_TERMINAL_PROMPT=0) + `PYTHONDONTWRITEBYTECODE=1` · `MPLBACKEND=Agg` · `MPLCONFIGDIR` · `TMPDIR` (`SP/c4e1_0b_a2_steps/{mpl,tmp}`) · `OMP` / `OPENBLAS` /
  `MKL_NUM_THREADS=1` · `REIL_C4_FIX_EVIDENCE=<E>` · `REIL_C4_FIX_STEP=<단계>`. 판정기 · 작성기는 env 를 읽지 않는다 (`os` 를 import 하지 않는다 · `-I`).
- helper: pytest 는 `SP/reil_c4env/pytest_t` (pytest 9.1.1 · E0 · N1 · E1-0 과 같은 경로).

### 4-3. RED · GREEN 판정 — 첫 예상 밖 결과에서 멈춘다

**판정의 정본은 이 절이다.** 고정 판정기 (`<E>/00_judge.py` = §1-1 의 `3749b32e…`) 가 같은 기준과 아래 읽기 규칙으로 `<단계>.judge.json` 을 배타 생성하고
(항목마다 ok · 관측값 · verdict MATCH / STOP), 실행자는 같은 기준으로 수동 판정한다. 판정기의 verdict 와 수동 판정이 다르면 그 자리에서 멈춘다 — 어느 쪽도
다른 쪽을 이기지 않는다. 판정기는 판정을 기록할 뿐 실행자의 멈춤 의무를 대신하지 않는다.

**판정기의 읽기 규칙 (수동 판정도 같은 위치를 본다):**
- 줄 = stdout 을 UTF-8 로 읽어 `\n` 으로 나눈 것 (끝의 빈 조각 하나는 버린다). **마지막 줄** = 그 마지막 줄 하나 — pytest 의 최종 요약이다 (`-q` 에서는 `=`
  장식이 없다 · 지난 시도의 마지막 줄은 `9 failed, 24 passed in 14.25s`). 마지막 줄은 RED 3 · GREEN 의 수 대상이고 절 머리줄 · 짧은 요약 절에 넣지
  않는다 (지난 시도의 작성자 스크립트가 이 줄을 짧은 요약의 "그 밖 줄" 로 센 오분류 — §92 · §93 · §8 의 26).
- 절 머리줄 = 마지막 줄 앞의 `=+ <이름> =+` 꼴의 줄. 짧은 요약 절 · `FAILURES` 절 = 그 머리줄 다음 줄부터 다음 절 머리줄 (없으면 마지막 줄) 앞까지.
- 짧은 요약 줄 = 짧은 요약 절에서 `PASSED <nodeid>` · `FAILED <nodeid>` (뒤에 ` - <메시지>` 가 붙을 수 있다) 꼴의 줄. 그 밖 줄은 판정 조건이 아니고 수만
  기록한다.
- 실패 절 = `FAILURES` 절 안의 `_+ <시험명> _+` 머리줄 다음 줄부터 다음 실패 절 머리줄 앞까지. 첫 traceback 항목 = 실패 절에서 `<경로>:<줄>: in <이름>` 꼴의
  첫 줄. 예외 블록 = 실패 절에서 `E   ` 로 시작하는 줄들 · 머리 = 그 첫 줄의 `E   ` 뒤를 `<예외 종류>: <메시지>` 로 읽은 것 (그렇게 읽히지 않으면 — 예:
  `assert …` — 종류 불일치).
- `ERROR` 줄 = stdout 에서 낱말 `ERROR` 로 시작하는 줄 · `ERRORS` 절 머리줄. 중단 = `Interrupted` 또는 `!!!!` 가 든 줄. `INTERNALERROR` 가 든 줄.
- **판정기 자기 확인 (입력 결속):** 판정기가 읽는 시험 파일의 sha256 · bytes 는 실행기 meta 의 `source_end` 행 (실행기가 단계 끝에 봉인 표와 대조한 바이트)
  과 같아야 하고, RED 표 (9 + 24) = 봉인된 launcher 대조의 최상위 `test_*` 함수 33 이어야 한다. 다르면 판정기 항목이 거짓이 되어 멈춘다.
- **판정기가 기준보다 엄격하게 읽는 셋** (정상 출력에서는 발동하지 않는다 · §8 의 26): `FAILURES` 절의 실패 절 머리줄 집합 = 표의 아홉 (표 밖 실패 절 ·
  같은 이름 둘 → 멈춤) · stdout 어디에든 `UNEXPECTED_RED_CAUSE` 가 있으면 멈춤 · 위의 입력 결속.

**공통 (외곽 실행기 meta · 외곽 반환 파일):** `started` true · `timed_out` false · `cleanup.status` "empty" · `cleanup.deadline_hit` false ·
`cleanup.errors` 없음 · `end_problems` 없음 · `errors` 없음 · `runner_ok` true. `first_error=null` 하나로 판단하지 않는다 (위 항목을 각각 본다). 외곽 반환
파일 = RED `1` · GREEN `0` (바이트 `1\n` · `0\n` · 실행기 반환식: runner_ok AND pytest rc 0 → 0 · 그 밖 1 · 3 · 4 는 멈춤).

**RED (`01_red_e1_0b`)** — 회신 §86 의 제안 문구에 근거의 위치 · 형식을 붙였다:

1. **nodeid 집합:** stdout 의 `short test summary info` 절에서 `FAILED <nodeid>` 로 시작하는 줄의 nodeid 집합 = 아래 표의 9, `PASSED <nodeid>` 줄의 집합 =
   아래 목록의 24 (각각 누락 · 추가 · 중복 없음). 줄 끝 ` - <메시지>` 의 유무 · 생략 · 줄바꿈 · 순서 · 폭은 판정 조건이 아니다.
2. **최종 예외 (nodeid 마다 일대일):** stdout 의 `FAILURES` 절에서 머리줄 (`_` 사이) 의 시험명이 그 nodeid 의 시험명과 같은 절을 **하나** 찾고, 그 절의
   첫 traceback 항목이 `tests/test_reil_c4e1_launch.py:<줄>: in <전체 시험명>` 인지 본다 (파일 경로 + 전체 시험명). 그 절의 예외 블록 (`E   ` 로 시작하는
   줄들) 의 머리 `E   <예외 종류>: <메시지>` 에서 종류 = 표의 종류이고, 메시지 첫 줄 = 표의 문자열 (정확히) 이거나 표의 접두로 시작한다.
   - 대응하는 절이 없거나 둘 이상 · 표 밖 시험의 실패 절이 있음 · 절 안에 연쇄 예외 표시 (`The above exception was the direct cause` · `During handling of
     the above exception`) · 예외 블록을 하나로 정할 수 없음 (E 줄이 없거나 이어지지 않음) → 그 자리에서 멈춘다 (다른 위치 · 형식으로 대체하지 않는다).
   - E 줄 개수 · stdout 전체의 첫 E 줄은 판정식이 아니다.
   - **원인 구분 (E1_0B_N1):** 메시지가 `('UNEXPECTED_RED_CAUSE'` 로 시작하는 실패는 표에 없는 실패다 — 그 nodeid 가 표의 아홉에 있어도 멈춘다. stdout
     어디에든 `UNEXPECTED_RED_CAUSE` 가 있어도 멈춘다.
3. **수 · 오류:** pytest rc (`meta.rc`) 1 · stdout 마지막 줄의 항목이 `9 failed` · `24 passed` 뿐 (skipped · xfailed · xpassed · error(s) · deselected 가
   하나라도 있으면 멈춤 · warning(s) 는 판정 조건이 아니고 수만 기록) · 수집 오류 (`ERROR` 줄) 0 · `INTERNALERROR` 0 · 중단 (`Interrupted` · `!!!!`) 0.
4. **정리 · 해시 · 기한 · 기록:** 위 공통.

| # | nodeid (`tests/test_reil_c4e1_launch.py::` 뒤) | 최종 예외 | 메시지 첫 줄 | 예측 줄 (참고 · 판정 아님) |
|---|---|---|---|---:|
| 1 | `test_l14_independence_fixed_commands_constants_and_main_rules` | AssertionError | 정확히 `('E1-0b: 승인 문구의 요청서 경로', 'docs/REIL_C4E_E1_APPROVAL_REQUEST_v5_20261027.md')` | 465 |
| 2 | `test_l23_user_level_rewrite_proxy_and_tls_off_settings_reach_neither_the_fetch_checks_nor_the_child` | AssertionError | 접두 `('rewrite', 'FUTURE-01: 사용자 설정이 fetch 사전 대조에 보였다', ` | 712 |
| 3 | `test_l25_inherited_git_location_and_trace_variables_reach_neither_fixture_nor_launcher_git` | AssertionError | 정확히 `('FUTURE-01: fetch 자식에 고정 설정 원천이 없다', [])` | 754 |
| 4 | `test_l28_fetch_env_drops_every_inherited_config_source_and_adds_only_the_fixed_list` | AttributeError | 정확히 `module 'scripts.reil_c4e1_launch' has no attribute 'fetch_env'` | 902 |
| 5 | `test_l29_a_conditional_config_matching_only_the_fetch_folder_reaches_neither_the_checks_nor_the_child` | AssertionError | 접두 `('FUTURE-01: 받은 저장소 폴더에만 걸린 조건부 설정이 fetch 에 닿았다', ` | 951 |
| 6 | `test_l30_the_received_repository_may_hold_only_the_local_keys_that_init_remote_and_partial_fetch_write` | AssertionError | 정확히 `('FUTURE-01: 받은 저장소의 local 설정 밖 키가 통과했다', 'localtls')` | 993 |
| 7 | `test_l31_cleanup_starts_observations_only_before_one_common_deadline_and_reports_unverified_when_it_cannot_look` | AttributeError | 정확히 `module 'scripts.reil_c4e1_launch' has no attribute 'cleanup_group'` | 1004 |
| 8 | `test_l32_an_exception_inside_cleanup_is_caught_and_only_an_emergency_kill_and_observation_follow_under_the_same_deadline` | AttributeError | 정확히 `module 'scripts.reil_c4e1_launch' has no attribute 'cleanup_group'` | 1035 |
| 9 | `test_l33_postcheck_fails_the_stage_for_a_cleanup_that_reached_its_deadline_or_did_not_end_empty` | AssertionError | 정확히 `('정리 기한에 닿은 기록을 사후 대조가 통과시켰다', [])` | 1072 |

- 접두로 정한 둘 (l23 · l29) 은 메시지 뒤쪽에 tmp 경로가 든 문제 목록이 붙어 실행마다 다르다. pytest 는 `assert …, <튜플>` 의 메시지를 `saferepr` 로
  만들고 길면 가운데를 줄인다 — 접두는 앞 60 자 안이다.
- **예측 줄 (대조 v8 바이트로 다시 적음 · 참고):** v7 의 여덟은 지난 시도에서 관측한 줄 (460 · 707 · 749 · 897 · 946 · 988 · 999 · 1030 — 예측과 같았다)
  에 모듈 docstring 의 다섯 줄을 더한 값이다. l33 은 v7 의 1065 에 일곱 (docstring 다섯 · l33 docstring 한 줄 · `post()` 의 줄바꿈 한 줄) 을 더한 1072 다.
  줄 차이는 판정 조건이 아니다 (§93 의 Q1).
- **통과 24 (`PASSED`, `tests/test_reil_c4e1_launch.py::` 뒤):** `test_l1_precheck_passes_only_with_fixed_list_exact_bytes_seal_binding_clean_interpreter_and_approved_specs` ·
  `test_l2_list_sha_schema_path_set_entry_format_and_non_json_each_block` · `test_l3_changed_same_size_missing_symlinked_module_or_linked_parent_each_block` ·
  `test_l4_a_shadowing_scripts_package_module_zip_entry_or_our_init_blocks` · `test_l5_interpreter_flags_fixed_argv_head_and_run_script_path_are_checked` ·
  `test_l6_stage_verdict_is_the_and_of_precheck_child_rc_timeout_and_postcheck` · `test_l7_child_result_reads_the_last_stdout_line_and_needs_final_complete_for_run` ·
  `test_l8_identity_link_binds_the_run_import_paths_to_the_checked_paths` · `test_l9_a_failed_precheck_never_starts_the_child_and_records_launched_false` ·
  `test_l10_a_passing_precheck_runs_the_fixed_child_and_completes_only_when_every_term_holds` ·
  `test_l11_timeout_kills_the_whole_process_group_including_grandchildren` · `test_l12_refuses_to_overwrite_records_or_reuse_a_pycache_folder` ·
  `test_l13_postcheck_catches_a_module_changed_during_the_child_wrong_fetched_bytes_and_a_reused_data_folder` ·
  `test_l15_a_leaf_package_beside_an_approved_module_blocks_without_executing_it` · `test_l16_a_leaf_extension_module_beside_an_approved_module_blocks` ·
  `test_l17_extra_executed_files_and_the_seal_lock_binding_each_block` · `test_l18_process_observation_errors_stay_unknown_and_only_vanished_pids_are_gone` ·
  `test_l19_a_failed_kill_with_a_running_child_ends_within_bounded_waits_and_records_unexited` ·
  `test_l20_exceptions_in_precheck_start_and_postcheck_are_recorded_with_phase_and_launched_state` ·
  `test_l21_a_failed_start_record_never_starts_the_child_and_is_not_treated_as_empty_normal_output` ·
  `test_l22_child_env_keeps_only_the_ca_among_git_variables_and_removes_secrets` · `test_l24_fetch_postcheck_binds_the_received_repository_to_the_fixed_source` ·
  `test_l26_preparation_failures_are_recorded_as_phase_prepare_and_never_start_the_child` ·
  `test_l27_decode_failures_in_proc_reads_and_git_output_are_recorded_not_escaped`.

**GREEN (`02_green_e1_0b`):** pytest rc 0 · 외곽 반환 0 · stdout 마지막 줄의 항목이 `71 passed` 뿐 (warning(s) 는 수만 기록 · 그 밖 항목이 있으면 멈춤) ·
`PASSED` 줄의 nodeid 집합 = 네 파일의 최상위 `test_*` 함수 71 (파일별 21 · 6 · 33 · 11 — 봉인된 시험 파일의 AST 와 같은 집합 · 판정기는 그 파일들을 meta 의
`source_end` 와 결속해 읽는다) · 짧은 요약 절 하나 · `FAILURES` 절 없음 · `FAILED` · `ERROR` 줄 0 · 수집 오류 · `INTERNALERROR` · 중단 0. `-x` 로 pytest
가 첫 실패에서 멈추고, 하나라도 다르면 E1-0b 를 멈춘다.

### 4-4. 봉인 · 원천 해시 (V2-05)

- **첫 시험 전 봉인:** 복사 다섯 (대조 둘 · 실행기 · 작성기 · 판정기) 을 RED 전에 커밋한다 (b). fixture 생성 규칙 · 고정 입력 · 기대값은 봉인된 대조 파일
  안에, 판정 기준의 기계 표현은 봉인된 판정기 안에 있다. 끝 기록의 diff 로 사전 고정을 대신하지 않는다.
- **생성 주체 = 외곽 실행기.** 대상 = `TARGETS` 14 (v5 와 같다).
- **기대값 = `EXPECT[단계]`** (실행기 v8 안): 단계마다 다른 것은 launcher 행 하나 — RED = v5 `2269d775…` (51,957) · GREEN = v6 `2c707123…` (62,639). 대조
  둘의 행 = launcher 대조 v8 `49d3fa36…` (74,542) · 실행기 대조 v5 `b34fb9a9…` (37,003). 나머지 열하나 = §1-2.
- **시점 · 실패 기준 (v5 와 같다):** 준비 끝 (자식 전) `<단계>.source_sha256.txt` → 하나라도 다르면 자식 0 · 반환 3 · `first_error` = prepare /
  SourceMismatch / 끝 기록 뒤 `<단계>.source_sha256_end.txt` → 다르면 runner_ok false.
- 실행기 · 작성기 · 판정기 자신의 sha 는 `00_start.txt` 와 `03_end.json` 에 남는다 (실행기는 meta 에 · 판정기는 `<단계>.judge.json` 에 자기 sha 를 기록만
  한다 — 자기 해시를 자기 안에 둘 수 없다).

### 4-5. 기록 · 제출 (범위안 §6)

- **증거 폴더 (`<E>`):** 실행기가 단계마다 `<단계>.{meta.json, stdout.log, stderr.log, porcelain_start.txt, porcelain_end.txt, source_sha256.txt,
  source_sha256_end.txt}` · 셸이 `<단계>.outer_rc.txt` · 판정기가 `<단계>.judge.json` · 나 (고정 명령) 가 `00_start.txt` · 작성기가 `03_end.json` · 복사본
  `00_step_runner.py` · `00_end_writer.py` · `00_judge.py`.
- **외곽 반환 (새):** 실행기가 돌아온 직후 같은 셸 명령 줄에서 `$?` 를 `<단계>.outer_rc.txt` 로 배타 생성한다 (`set -C` — 있으면 쓰지 않는다). E1-0
  회신의 "증거 폴더에 별도 셸 반환 원문 없음" 에 대응한다. 셸이 본 실행기 반환이고, pytest rc 는 meta 의 `rc` 다.
- **판정기 (새 · 고정본):** `<E>/00_judge.py` (= §1-1 의 `3749b32e…`) 를 c · d 에서 외곽 반환 파일 직후 한 번씩 실행한다.
  - 읽기 = 그 단계의 stdout · meta · 외곽 반환 · stderr (크기만) · 봉인된 시험 파일 (RED 하나 · GREEN 넷). 쓰기 = `<단계>.judge.json` 배타 생성 하나.
    시험 · Git · 네트워크 · 하위 프로세스 0.
  - 기록 = 항목마다 id · ok · 관측값 · 거짓 항목 목록 · verdict (MATCH / STOP) · 입력 파일의 sha256 · bytes · 판정기 자신의 경로 · sha256 · 참고 정보 (예측
    줄과 관측 줄 · 짧은 요약의 그 밖 줄 수 · warning 수 · stderr 크기). 반환 0 = MATCH · 1 = STOP · 2 = 의도된 거부 (폴더 이름 규칙 밖 · 판정기가 그 폴더
    밖 · 단계 이름 밖 · 출력이 이미 있음 — 아무것도 쓰지 않음). 판정 중 예외는 거짓 항목 `judge.exception` 으로 남기고 기록은 쓴다.
- **끝 기록 작성기 v2 (고정본):** `<E>/00_end_writer.py` (= §1-1 의 `2f316acc…`) 를 e 에서 한 번 실행한다.
  - 읽기 = meta 둘 · 외곽 반환 둘 · 판정 기록 둘 · 복사본 여섯 (대조 둘 · launcher · 실행기 · 작성기 · 판정기) · 디스크 · 시각. 쓰기 = `03_end.json` 배타
    생성. Git · 네트워크 0.
  - 이름 확인 결과는 이름만 담는다. 읽지 못한 파일은 그 자리에 사유를 남긴다 (대신 채우지 않는다). 폴더 이름 규칙 (`reil_c4e1_0b_a2_YYYYMMDD` · 부모
    `evidence`) 밖이면 아무것도 쓰지 않는다.
  - 기록을 모을 뿐 판정하지 않는다 (판정 기록은 sha256 · bytes · verdict · 거짓 항목 이름을 옮겨 적기만 한다).
  - v1 과 다른 것: 이름 규칙의 `a2` · 복사본에 `00_judge.py` · 단계 행의 `judge` · 끝 출력의 판정 verdict. 그 밖 (외곽 반환 · meta 요약 · 이름 확인 ·
    디스크 · 시각 · 배타 생성) 은 같다.
- **증거의 Git 상태는 외곽 실행기 기록만이다:** 단계마다 시작 · 끝의 HEAD · porcelain (meta 의 `records` 와 `<단계>.porcelain_*.txt`). 단계 안의 HEAD
  불변은 실행기가 확인한다. 수동 기록 (`00_start.txt` · `03_end.json`) 과 판정 기록 (`<단계>.judge.json`) 은 Git 을 부르지 않는다.
- **`00_start.txt`** = UTC · 디스크 · sha256 열둘 (초안 여섯 · 복사본 다섯 · 그 시점의 `scripts/reil_c4e1_launch.py` = v5).
- **커밋:** a = 승인 기록 § · 보존 규칙 · b = 복사본 다섯 + `00_start.txt` · c = RED 증거 아홉 (실행기 일곱 + 외곽 반환 + 판정 기록) · d = GREEN 증거
  아홉 + `scripts/reil_c4e1_launch.py` (v6) · e = `03_end.json` (+ 결과 기록 § · 발송문은 그 뒤 커밋). 커밋하지 않음: `SP/c4e1_0b_a2_steps/`. 증거는
  `git add -f` 로 넣는다 (`.log` 는 저장소의 무시 규칙에 걸린다 — 지난 시도에서 확인) · 커밋 뒤 그 단계의 파일 수 = 커밋된 파일 수를 확인한다.
- 커밋 전: 비밀 검사 + URL 계정 정보 형태 검사 · 파일 하나 ≤ 50 MB.

### 4-6. 절차 Git 의 중지 조건 (v5 §4-6 과 같다)

- **절차 Git** = add · commit · push · log — 증거가 아니다 (그 결과를 증거로 인용하지 않는다).
- **이름 확인 (고정 명령 · 값을 읽거나 출력하지 않는다):**

  ```
  /usr/bin/python3.11 -I -c 'import json, os, re, sys; n = sorted(k for k in os.environ if k.startswith("GIT_")); bad = [k for k in n if not re.fullmatch(r"GIT_(ASKPASS|CONFIG_COUNT|CONFIG_(KEY|VALUE)_[0-9]+|EDITOR|SSL_CAINFO|TERMINAL_PROMPT)", k)]; print(json.dumps({"git_env_names": n, "outside_allowlist": bad})); sys.exit(1 if bad else 0)'
  ```

- **허용 목록:** `GIT_ASKPASS` · `GIT_CONFIG_COUNT` · `GIT_CONFIG_KEY_<n>` · `GIT_CONFIG_VALUE_<n>` · `GIT_EDITOR` · `GIT_SSL_CAINFO` · `GIT_TERMINAL_PROMPT`. 위치
  · 추적 계열과 그 밖 모든 `GIT_*` 는 목록 밖이다.
- **시점:** 단계 a 의 첫 git 직전 · 단계 e 의 첫 git 직전 (결과를 a 는 승인 기록 § 에, e 는 `03_end.json` 에 이름만 남긴다). b–d 의 절차 git 도 같은 셸
  명령 줄에서 이 확인 뒤에만 실행한다 (`<확인> && git …`).
- **어긋나면:** 목록 밖 이름이 하나라도 있으면 멈춘다 (이름만 기록). 이 확인은 셸 env 의 `GIT_*` 이름만 본다 — `GIT_CONFIG_KEY / VALUE` 의 내용과 설정
  파일 등 절차 Git 의 설정 원천까지 격리하지는 않는다 (v5 §8 의 19 · FUTURE-01 은 launcher 의 fetch 단계에만 적용된다).

## 5. 활동 범위 셋

| 범위 | 포함 | 제외 |
|---|---|---|
| **RED — launcher 대조 33 (v5 바이트)** | launcher 함수 · tmp 가짜 run 스크립트 (stdlib · fetch 모드 `localtls` · `localinclude` 포함) · 손주 sleep · 해석기 탐침 (`-c`) · tmp 안 로컬 git (init · 빈 커밋 · rev-parse · status · remote add · config 쓰기 (`uploadpack.allowFilter` · `uploadpack.allowAnySHA1InWant` · `http.sslVerify` · `include.path` — tmp 저장소에만) · `config --list` · `ls-remote --get-url` · `hash-object -w --no-filters` · `cat-file blob` · file 프로토콜의 `fetch --depth 1 --filter=blob:none` (l30 · `GIT_ALLOW_PROTOCOL=file`)) · 가짜 HOME 의 `.gitconfig` (URL 바꿈 · 프록시 · TLS 끔 · `includeIf "gitdir:**/git/"`) · 가짜 /proc · 관측 비용이 있는 가짜 시계 · 주입 예외 | 우리 실행 모듈 다섯 import · 실제 자료 · optimizer · 네트워크 |
| **GREEN 71** | 위 (v6 바이트) + E0 21 · N1 6 (실제 실행 모듈 import · 로컬 Git / fetch 대조 · 합성 `run.run` 둘 · `plan_e` · fork 세션 — E1-0 GREEN 과 같다) + 실행기 대조 11 (가짜 /proc · 가짜 시계 · driver 하위 프로세스 8 회 — E1-0 과 같다) | 실제 원자료 · 원 optimizer · 네트워크 fetch |
| **판정기 · 끝 기록 작성기** | 증거 폴더 · 봉인된 시험 파일 읽기 · 기록 파일 하나씩 배타 생성 (`<단계>.judge.json` · `03_end.json`) | 시험 · Git · 네트워크 · 하위 프로세스 · env 읽기 |
| **실제 E1-1–3** | identity (`env_profile` 실행 포함) · 읽기 경로 · 고정 출처 fetch · 원자료 개봉 · 66 호출 run | **E1-0b 승인으로 허용되지 않는다** |

"우리 실행 모듈 import 0" 은 launcher 대조 33 에만 쓴다. 위 수는 소스가 계획한 활동이지 수행 횟수가 아니다.

## 6. 대조 33 + 11 · RED / GREEN 선언

바뀌지 않은 대조 (본문 그대로 · E1-0 GREEN 에서 v5 바이트로 통과): l1–l13 · l15–l22 · l24 · l26 · l27 (가짜 run 은 fetch 모드 둘이 늘었을 뿐 다른
모드의 동작은 같다) · r1–r11 (실행기 대조 v5 — 이름 규칙 · 봉인 표 단계 이름만 · 시험 본문은 v3 · v4 와 같다). 고치거나 새로 넣은 대조:

| ID | 고정 입력 | 기대 (GREEN · v6) | RED (v5) · 이유 · 호출 경로 |
|---|---|---|---|
| l14 (고침) | — | 요청서 경로 · v5 의 상수 + `CLEANUP_S` 20 · `POLL_S` 0.1 · `FETCH_GIT_CONFIG` · `FETCH_LOCAL_KEYS` · 승인 문구 `상태 문서 §80 (사용자 E1-1–3 승인 · docs/REIL_C4E_E1_0B_APPROVAL_REQUEST_20261030.md)` | 첫 문장 (요청서 경로) 에서 AssertionError — 상수 수준 |
| l23 (다시 씀) | 가짜 HOME `.gitconfig` 셋 (각각 새 tmp 트리): `url."https://example.invalid/".insteadOf = https://github.com/` · `http.proxy = http://127.0.0.1:9` · `http.sslVerify = false` | fixture 자기 확인 (정제 env 의 `config --list --show-origin` 에 그 파일이 보임) → fetch 사전 대조 통과 · 설정 항목 = `[("command", "http.proxyauthmethod", "basic")]` · 유효 출처 = 고정 URL · launch fetch 반환 0 · complete · meta `env_git_config` = 고정 다섯 | v5 는 같은 설정을 사전 실패로 막는다 (v5 의 l23 이 시험한 것). v6 은 원천을 끊어서 닿지 않게 한다 — 첫 사례 (rewrite) 에서 AssertionError · 행동 수준 · `launch` → `precheck` → `fetch_source_precheck`. 원인 구분: `ok` false 는 출처 관측 둘 rc 0 · raw 설정 목록에 가짜 HOME `.gitconfig` 원천의 심은 키 · raw 유효 출처 = 심은 결과 · 문제 = 심은 키 하나 (+ rewrite 면 유효 출처 하나) 뿐일 때만 기대 RED (탐침 · 출처 읽기 · 그 밖 문제는 `UNEXPECTED_RED_CAUSE`) |
| l25 (고침) | v5 와 같은 입력 (다른 저장소의 `GIT_DIR` · 표지 폴더의 `GIT_OBJECT_DIRECTORY` · `GIT_INDEX_FILE` · `GIT_TRACE`) | v5 의 기대 + 가짜 run 이 본 `GIT_*` 이름 = fetch env 의 고정 다섯 · meta `env_git_config` = 고정 다섯 | v5 의 자식 env 에는 `GIT_CONFIG*` 가 없다 → `[]` · 행동 수준 · `launch` → `fetch_env` |
| l28 (새) | `GIT_CONFIG_COUNT` · `KEY_0/1` · `VALUE_0/1` (URL 바꿈 · TLS 끔) · `GIT_CONFIG_PARAMETERS` · `GIT_CONFIG_GLOBAL` · `GIT_CONFIG_SYSTEM` · 옛 `GIT_CONFIG` · CA · 프록시 · PATH · HOME | `GIT_CONFIG*` = 고정 다섯 · 그 밖 넷 그대로 · 받은 env 불변 · 두 번 적용해도 같다 · `fetch_env({})` = 고정 다섯 | `fetch_env` 없음 — 인터페이스 수준 |
| l29 (새) | 가짜 HOME `.gitconfig` = `[includeIf "gitdir:**/git/"] path = <tmp>/home/evil.cfg` (URL 바꿈 · TLS 끔) | fixture 자기 확인 (정제 env 로 `<tmp>/demo/git` 저장소 안에서는 바뀐 유효 출처 · 작업 폴더에서는 고정 URL) → launch fetch 반환 0 · 받은 저장소의 유효 출처 = 고정 URL · meta 어디에도 evil 파일 경로 없음 · 가짜 run 이 본 `GIT_*` = 고정 다섯 · **원인 구분:** 반환 ∈ {0, 1} · meta 가 이 launch 의 정상 실행 (`_normal_fetch_meta` — 단계 · 이름 · launcher 경로 · 오류 0 · 사전 통과 · 자식 rc 0 · timeout 없음 · 그룹 empty · 자식 결과 ok · 기록 rc 0 · HEAD 불변) · 반환 0 이면 complete · 사후 문제 0 | v5 는 사전 대조 (작업 폴더) 를 지나고, 가짜 run 이 받은 `<data>/git` 에서 includeIf 가 걸려 사후 유효 출처가 달라진다 → 반환 1 · 행동 수준 (FUTURE-01 의 위험 재현). 원인 구분: 반환 1 은 정상 실행 뒤 사후 문제가 **하나**이고 그것이 바뀐 URL 의 유효 출처 문제 · raw 유효 출처 = 바뀐 URL · raw `remote.origin.url` = 고정 URL · 출처 관측 rc 0 일 때만 기대 RED (준비 예외 · 자식 없음 · 추가 문제는 `UNEXPECTED_RED_CAUSE`) |
| l30 (새) | (a) tmp upstream 저장소 (`uploadpack.allowFilter` · `allowAnySHA1InWant`) 에서 `init` → `remote add` → `fetch --depth 1 --filter=blob:none origin <sha>` (file 프로토콜 · fixture env) (b) 가짜 run 이 받은 저장소의 local 설정에 `http.sslVerify=false` / `include.path=/dev/null` | (a) `fetch_source_postcheck(…, url=<upstream 경로>, commit=<sha>)` 문제 0 (실제 git 이 쓴 local 키가 허용 목록 안) (b) 각각 반환 1 · postcheck_ok false · "허용 local 키 밖" 문제 · **원인 구분:** 반환 ∈ {0, 1} (아니면 meta 를 읽기 전에 멈춤) · meta 를 기대 assert 앞에서 읽고 정상 실행 (`_normal_fetch_meta`) · 반환 1 이면 사후 문제가 모두 심은 local 키 (`http.sslverify` / `include.path`) 를 가리키고 그중 "허용 local 키 밖" 이 있음 | v5 의 사후 대조는 받은 저장소의 설정을 보지 않는다 → (a) 통과 · (b) `localtls` 가 반환 0 → AssertionError · 행동 수준. 원인 구분: 반환 0 은 정상 실행 · complete · 사후 ok · 사후 문제 0 일 때만 기대 RED (반환 4 등 · 사후 문제는 `UNEXPECTED_RED_CAUSE`) |
| l31 (새) | 가짜 시계 · 관측 한 번에 비용을 쓰는 가짜 /proc (구성원 하나) · kill_wait 10 · grace 5 · (a) timeout · kill 이 듣지 않는 자식 · 비용 0.05 · 기한 t0+20 (b) 정상 종료 · 좀비만 · 기한 t0+20 (c) timeout · 기한 = t0 (d) 정상 종료 · 살아 있는 구성원 · 비용 3 s · 기한 t0+1 | (a) alive · deadline_hit · 미종료 · SIGKILL 둘 (sent) · 모든 관측 시작 < 기한 · 끝 ≤ 기한 + 0.05 · 모든 sleep 끝 ≤ 기한 (b) empty · kill 0 · 관측 1 · 기한 안 (c) 관측 0 · sleep 0 · unverified · 첫 SIGKILL 은 보냄 (d) 관측 [t0] 하나 · 그 결과로 재kill · 재관측 0 → unverified · 끝 = t0+3 | `cleanup_group` 없음 — 인터페이스 수준 (§8 의 2) · `cleanup_group` → `group_status` → `proc_members` |
| l32 (새) | 같은 가짜 · timeout · 끝나지 않는 자식 · 시작 시각 ≥ t0+10 인 첫 sleep 이 RuntimeError (주입) · 기한 t0+20 | unknown (그룹 기록도) · emergency · errors = `["RuntimeError: sleep failed (시험 주입)"]` · 예외 시각 ∈ [t0+10, t0+10.2) · SIGKILL 둘 (처음 · 비상) · 모든 관측 시작 < 기한 · 끝 ≤ 기한 + 0.05 · deadline_hit | 같음 |
| l33 (새 · v8 에서 고침) | 사전 대조 (identity) · Git 기록 (HEAD 같음 · porcelain 빈) 고정 · 자식 기록만 바꿈: 기본 (empty · deadline_hit false · 오류 0) / deadline_hit true / 끝 상태 killed · unverified · unknown / errors 하나. 직접 호출 `L.postcheck` 은 fixture 의 `extra` · `data` · `data_files` 를 넘긴다 (E1_0B_RESULT_N1 — v7 은 `extra` 를 빠뜨려 기본 기록에서 실제 두 파일의 sha 와 tmp 가짜 파일을 대조했다) | 기본 → 문제 0 · 나머지 → 각각 실패 (상태 이름이 문제에 있음) | v5 사후 대조는 `deadline_hit` 을 보지 않는다 → 기본 기록 (문제 0 — fixture 결속 뒤 · §8 의 24) 다음의 `deadline_hit` 기록에서 ok true → AssertionError · 행동 수준 · `postcheck` |

- **RED 선언:** 9 실패 · 24 통과 (§4-3 의 표 · 목록). 행동 수준 RED 는 l23 · l25 · l29 · l30 · l33 (v5 바이트의 실제 동작이 기대와 다르다), 상수 수준은
  l14, 인터페이스 수준은 l28 · l31 · l32 (새 함수가 v5 에 없다).
- **GREEN 선언:** 71 passed (E0 21 + N1 6 + launcher 33 + 실행기 11). 시험 함수 하나 = 사례 하나 (parametrize 없음 · 한 함수 안의 하위 사례는 순서대로).
- **원인 구분은 계획한 경로 (v5 의 알려진 결함 · v6 정상 / 거부) 에서 발동하지 않는다.** 발동하면 예상 밖 원인이므로 RED · GREEN 모두 그 자리에서 멈춘다.
- 틀린 구현을 잡는 근거는 GREEN 의 음성 대조다 (v5 의 l2–l5 · l9 · l11–l13 · l15–l27 · r1–r5 · r7–r11 + l29 · l30 (b) · l31 · l32 · l33).

## 7. E1-1–3 고정 계획 — **이 요청의 승인 대상이 아니다**

E1-0b (시도 a2) 결과 검토 뒤 별도 요청서에 아래를 고정하고 검토 · 사용자 승인을 받는다 (범위안 §4 · §5 · §7).

| 항목 | 고정할 것 |
|---|---|
| 순서 | identity (E1-1) → 읽기 경로 `add_repo` (REIL-UConn/Multi-Objective-Optimization-for-Lithium-Ion-Battery-Degradation-Diagnostics · read) → fetch (E1-2) → run (E1-3). 첫 예상 밖 결과에서 멈춘다 · 재시도 0 |
| 대상 바이트 | launcher = E1-0b GREEN 바이트 (v6 `2c707123…`) · 다섯 모듈 · SOURCES.json · S1 의 둘 · 봉인 (MANIFEST `4f120948…` → lock `ea91156c…`) · identity helper (`92bb3bca…`) |
| 입력 | 고정 URL · 커밋 `1188c371e5836df4a7e5f5acf336a34ffd4027e6` · 자료 두 파일 (`LFP_Data.xlsx` 10,841,377 B `fd50e095…` · `util_LFP.py` 33,754 B `3c19e45e…`) |
| 명령 | `/usr/bin/python3.11 -I BMS/scripts/reil_c4e1_launch.py <identity\|fetch\|run> --evidence BMS/evidence/reil_c4e1_<날짜> --approval-section §NN` 셋 · 자식 argv = `build_argv` (l14 가 문자 그대로 고정) · run 의 승인 문구 `상태 문서 §NN (사용자 E1-1–3 승인 · docs/REIL_C4E_E1_0B_APPROVAL_REQUEST_20261030.md)` (§8 의 16) |
| 배정 | 자식 timeout identity 60 · fetch 300 · run 10,800 s · 탐침 ≤ 60 s · fetch 의 git 확인 ≤ 4 × 60 s · 기록 git 은 호출마다 60 s · launcher 정리 공통 기한 20 s · 전체 ≤ 6 h |
| 수용 (무관용) | 단계마다 launcher 단계 판정 = precheck_ok AND child_ok AND rc 0 AND timeout 없음 AND postcheck_ok (정리 empty · 기한 안 · 오류 0 · 기록 성공 포함). 하나라도 거짓이면 그 단계에서 멈춘다 · 부분 수용 없음. E1-2 의 사후 대조는 자료 두 파일 sha256 · bytes = 고정값을 포함한다 |
| E1-3 의 두 판정 | 실행 유효성 = launcher 단계 판정. 실험 결과 = run 의 `final_verdict` (사전 판정 AND `record_state` COMPLETE AND 위반 0 → `E3a` COMPLETE · `c4a_gate`). 둘을 따로 적는다. INCOMPLETE 는 결과대로 기록하되 E1-3 통과가 아니다. C4-A 로 가는 문은 둘 다 참일 때만 열린다 (그 문을 여는 것도 별도 승인) |
| 프록시 | fetch 는 `HTTPS_PROXY` · `GIT_SSL_CAINFO` (정제 env 가 둔다) · `http.proxyAuthMethod=basic` (고정 목록) 로 지난다. 그것만으로 되는지는 관측하지 않았다 — 실패하면 E1-2 에서 멈춘다 (재시도 없음 · 승인 한 번을 쓴다) |
| 공개 한계 (유지) | lstat 비원자 · 가짜 시계 · 기한 전에 시작한 관측의 길이 · 고정 목록 밖 설정 값의 내용은 검증하지 않음 · 설정 원천 격리는 fetch 단계만 |

## 8. 밝힐 것

1. **E1_0_N1 (§86):** E1-0 은 "E1-0 작업 범위에서 실행했으며, v5 §4-3 RED 근거 위치를 짧은 요약에서 동일 stdout 의 대응 실패 절로 대체하고 계속한 절차
   차이가 있다." 이번 §4-3 은 근거의 위치 · 형식을 미리 고정했고, 실제 출력이 그와 다르면 대체하지 않고 멈춘다 (실행자 규칙). 원 로그 · §84 · E1-0
   증거는 바꾸지 않고, 과거의 계속 진행을 소급 승인으로 적지 않는다.
2. **RED 의 수준:** l28 · l31 · l32 는 인터페이스 수준 RED 다 (새 함수가 v5 에 없다). v5 정리 루프 (관측 먼저 · 공통 기한 없음) 의 행동은 v5 바이트로
   대조하지 않는다 — `cleanup_group` 의 인자 (`deadline` · 주입 시계) 가 v5 에 없다. 그 행동의 근거는 범위안 §3 · 이 요청 §3-3 의 정적 설명 (v5
   l.628–691) 이다. l23 · l25 · l29 · l30 · l33 은 v5 바이트의 실제 동작을 보는 RED 다.
3. **허용 local 키 아홉:** Git 의 공개 동작 (init · remote add · 부분 받기 등록) 으로 정한 목록이다 — 이번에 실행 0. 실제 git 2.43.0 이 쓰는 키는 GREEN 의
   l30 (a) 가 file 프로토콜의 부분 받기로 처음 본다. 목록 밖 키를 쓰면 l30 에서 멈춘다 (fail-closed). E1-2 의 실제 fetch (`reil_c4e_run.py` l.668–669 — 같은
   세 명령 + 읽기 `show`) 와 원격 프로토콜 (https · 프록시) 의 차이는 E1-0b 가 시험하지 않는다.
4. **includeIf 의미:** `gitdir:` 조건은 일치하는 저장소 안에서만 걸리고 저장소 밖 작업 폴더의 `config --list` 에는 보이지 않는다는 것은 Git 의 공개 의미에
   기댄 설계다 (실행 0). l29 는 그것에 기대기 전에 정제 env 로 저장소 안 · 밖을 직접 확인한다 (fixture 자기 확인) — 틀리면 RED 에서 표와 다른 실패로
   멈춘다.
5. **설정 값 읽기 (§87 · 범위안 §9-1 의 유일한 예외):** 2026-10-30 06:33:43Z 에 한 번. 명령은 `git config --global --get http.proxyAuthMethod` 의 값을
   인증 방식 이름 다섯 (anyauth · basic · digest · negotiate · ntlm) 중 하나일 때만 출력하고 (그 밖이면 길이만), origin 은 첫 칸만 출력했다 (같은 줄에
   `git --version`). 결과: `basic` · rc 0 · origin `file:/root/.gitconfig` · git 2.43.0. 다른 키의 값은 읽지 않았다. 인증 방식 이름이고 비밀이 아니다.
   fetch 에 이 키가 필요한지는 관측하지 않았다 (E1-2). git-config 문서상 이 키는 프록시 문자열에 사용자 이름이 있을 때 의미가 있고
   `GIT_HTTP_PROXY_AUTHMETHOD` 로도 바뀔 수 있다 — `child_env` 는 그 변수를 뺀다 (§88 의 Q2 주의). 프록시 문자열의 값은 읽지 않았다.
6. **fetch env 의 범위:** fetch 단계 전체 (사전 · 탐침 · 기록 git · 자식 · 사후) 가 시스템 · 사용자 설정을 읽지 않는다. 그래서 그 단계의 기록 git
   (`rev-parse HEAD` · `status --porcelain`) 도 사용자 설정 (`core.checkstat` · `core.trustctime` 등) 없이 돈다 — 기록일 뿐 판정 항은 HEAD 불변 · 기록
   성공이다. `safe.directory` 같은 사용자 설정의 보호 키도 빠진다 (저장소 · 자료 폴더 모두 실행 사용자 소유 — 정적 판단). identity · run 단계는 v5 와
   같이 시스템 · 사용자 설정을 읽는다 (설정 원천 격리는 fetch 단계만).
7. **정리 기한의 경계 (§86):** launcher 의 20 s 는 정리 원점 (자식 대기가 끝난 시각) 부터다. 그 앞 (사전 대조 · 탐침 · 시작 기록 · 자식 대기) 과 뒤 (사후
   대조 · 끝 기록 · meta) 는 기한 밖이다. 기한을 넘을 수 있는 것은 기한 전에 시작한 /proc 관측 하나 (+ 즉시 동작 · 비차단 확인 · 기록) 이고, 그 길이에는
   상한이 없다 (감시 스레드 없음 · /proc 읽기가 멈추면 정리도 멈춘다). 외곽 실행기의 15 s 도 같은 규칙이다.
8. **가짜 시계:** l31 · l32 는 가짜 시계 · 가짜 /proc 로만 기한 · 예외 경로를 시험한다. 실제 /proc 지연의 상한이나 이 환경의 OS 반환 시간을 관측한 것이
   아니고, 넓혀 읽지 않는다 (§86). 실제 프로세스의 정리는 기존 l11 · l19 (실제 자식 · 손주) 가 v6 경로로 한 번씩 지난다. l31 (a) 의 기한 도달은 부동소수
   경계까지 정적으로 확인했다 — kill 대기 루프가 t0+10 이상에서만 끝나므로 관측 창은 t0+15 이상에서 끝나고, 재관측 창의 끝은 정확히 기한 (t0+20) 이다.
9. **재관측 창의 끝:** `min(기한, 지금 + grace)` 로 둔 것은 명목 배정 (관측 5 + 재관측 5) 과 기존 l19 (`dt < 20` · kill 대기 1 · grace 0.5) 를 그대로
   지키기 위해서다. 그래서 재관측 창이 기한보다 일찍 끝날 수 있고, 그때 끝 상태는 alive 이며 단계는 실패다 (fail-closed).
10. **상태 이름 · 시간:** v5 의 `alive_then_killed` 는 v6 에서 `killed` 다 (둘 다 사후 대조 실패). `wait_s` 의 경계가 바뀌었다 (§3-3).
11. **외곽 실행기:** 정리 · 기록 코드는 v5 바이트 (E1-0 · §86 수용) 와 같고 이름 규칙 · 봉인 표 · 작업 폴더만 바뀌었다. E1-0b 는 실행기 대조의 RED 를
    하지 않는다 (범위안) — GREEN 의 r1–r11 이 v8 사본에서 회귀를 본다. 작업 폴더를 `SP/c4e1_0b_a2_steps` 로 나눈 것은 E1-0 의 `SP/c4e1_steps/tmp` ·
    지난 시도의 `SP/c4e1_0b_steps` 와 섞지 않으려는 것이다 (같은 TMPDIR 이면 pytest 의 tmp 보존 규칙이 오래된 tmp 폴더를 지울 수 있다).
12. **외곽 반환 파일:** 셸이 실행기 반환 직후 쓴 값이다. 실행기 · pytest · 셸 사이의 다른 경로를 독립 증명하지 않는다.
13. **끝 기록 작성기:** 실행 전에 고정한 바이트 (v2) 를 e 에서 한 번 실행한다. 기록을 모을 뿐 판정하지 않는다. E1-0 의 작성기 (사본 `4c3d2991…`) 와 다른
    것은 단계 이름 · 복사본 (v2 는 여섯) · 외곽 반환 · `deadline_hit` · 읽기 실패 사유 · 폴더 이름 확인 · (v2) 판정 기록 읽기다.
14. **warning:** 판정 조건이 아니다 (회신 §86 의 조건 목록에 없다). 수는 stdout 마지막 줄 그대로 남는다. E1-0 의 세 단계에는 없었다.
15. **l14 의 `§80`** 은 `build_argv` 의 형식 예시다 — 상태 문서 §80 의 내용과 관계없다 (v5 §8 의 25 와 같음).
16. **E1-1–3 의 승인 문구:** launcher 의 `REQUEST` 가 이 요청서라서 E1-1–3 의 run 승인 문구도 이 경로를 인용한다. E1-1–3 요청은 launcher 바이트를 바꾸지
    않는다 — 바꾸면 E1-0b 와 같은 RED / GREEN 이 다시 필요하다. 승인 절 §NN 이 그 요청의 승인 기록을 가리킨다.
17. **v5 에서 유지하는 공개:** /proc 스캔 비원자 · PID kill 의 생성 신원 비보장 (v5 §8 의 4) · identity · run 의 기록용 git 은 사용자 · 시스템 설정을
    읽는다 (5) · find_spec 결속의 TOCTOU (7) · 해석기 · stdlib · site-packages 는 원천 해시 목록 밖 (10) · 숫자는 timeout · 기다림의 상한이지 전체 소요
    보증이 아니다 (11) · 정리 예외는 `cleanup.errors` 에 (20) · lstat 은 원자적 보호가 아니다 (22) · fixture 도우미 `_git` 은 `text=True` 만 (26) · GitHub
    의 커밋 상태는 기록되지 않은 일시 활동이 없었음을 증명하지 않는다 (§86).
18. **정적 예측:** RED · GREEN 예측은 AST · 코드 읽기로만 했다 (실행 0). 맞지 않으면 그 자리에서 멈추고 결과 검토로 간다.
19. **원인 구분의 범위 (E1_0B_N1):** 원인 구분은 시험이 받은 raw 기록 (사전 대조의 설정 목록 · 유효 출처 · launch meta) 과 문제 목록을 본다. raw 기록
    자체가 틀리게 만들어진 경우까지 독립 증명하지는 않는다. v5 분기의 문제 개수 · 원인 대응은 v5 바이트 (`2269d775…`) 의 문구 · 순서에 기댄 정적
    판단이다 — 틀리면 RED 에서 `UNEXPECTED_RED_CAUSE` 로 멈춘다 (fail-closed). 나머지 여섯 RED (l14 · l25 · l28 · l31 · l32 · l33) 는 첫 문장 실패이거나
    기대 assert 앞에 정상 실행 단언이 있어 원인에 묶여 있다 (정정 범위안 §2).
20. **숫자 정정 (§88):** `00_start.txt` 의 sha 는 열이다 (첫 판은 "열하나"). 실행기 대조 v3 → v4 의 같은 최상위 노드는 46 이다 (첫 발송문 · §87 은 47 —
    건너뜀 메시지를 고치기 전에 센 값). 이미 커밋된 §87 · 첫 발송문은 고치지 않는다.
21. **끝 기록의 범위 (§88 의 Q5 주의):** `03_end.json` 은 커밋 · push · 문서 전 snapshot 이다. 그 뒤 활동까지의 전체 시간으로 넓혀 읽지 않는다.
22. **지난 시도 (§91–§93):** 대조 v7 · 실행기 대조 v4 · 실행기 v7 · 작성기 v1 로 a–c · e 를 했고 RED 에서 l33 으로 멈췄다 (GREEN · launcher v6 복사 0). 원기록
    12 파일 (`evidence/reil_c4e1_0b_20261103/` · 69,968 B) · 작업 폴더 · 회신 원문은 그대로 둔다. 그 RED 의 여덟 일치는 그 조합의 과거 증거이고, 이번 판정에
    이어 붙이지 않는다 — 이번에 RED 33 전체를 새 바이트로 다시 한다 (§93 의 Q3). 지난 시도의 승인 (§91) 은 썼으므로 이번 시도는 새 승인이 필요하다.
23. **이전 검토의 정정 (§93):** v2 사전 재검토의 l33 판단 ("정상 기준 결과를 확인한 뒤 …" · Q2 의 "정적 모순 없음") 은 검토자가 따로 철회 · 정정했다
    (`REVIEWER_CORRECTION.json` · 원 검토 파일은 그대로). 작성자도 같은 가정 (l33 의 기본 기록이 문제 0) 을 검증 없이 했다. 재발 방지로 기본값 결속 정적
    대조를 이 요청에 고정한다 (§1-3 · 부록 A).
24. **l33 의 정적 재확인 (실행 0):** v5 · v6 의 `postcheck` (v5 536–568 줄 · v6 601–635 줄 · 차이는 `deadline_hit` 한 항) 를 따라가면, 고친 l33 의 기본
    기록은 모듈 다섯 (fixture 목록 = tmp 가짜 파일) · 실행 파일 둘 (fixture `extra`) · pycache (`_pre` 가 만든 빈 폴더 — 사전 대조의 탐침은 `-I -B` 라
    bytecode 를 쓰지 않는다 · v5 `interp` 329 줄) · 그룹
    empty · 기한 false · 미종료 없음 · 오류 0 · 기록 넷 정상이라 문제 0 이다 (identity 단계라 `data` · `data_files` 는 읽히지 않는다). 지난 RED 의 문제
    목록이 정확히 둘이고 둘 다 `extra` 의 실파일 대조였다는 것 — pytest 의 `Left contains 2 more items` · 첫 항목 `bms-balancing/scripts/reil_c6_profile.py:
    sha256 676ef3bd… · 25 B ≠ 기대 …` · 목록 끝의 꼬리 `…ad63148563'}` (env_profile 기대값의 sha 끝) — 가 그 밖의 항 (모듈 · pycache · 그룹 · 기록) 이 문제를
    내지 않았다는 관측 근거다. 둘째 문제의 전체 문장은 pytest 가 생략했다 (§93 의 한계 · 복원하지 않는다). 그래서 v5 에서는 다음 `deadline_hit` 기록이 ok
    true 가 되어 1072 줄의 기대 메시지 `('정리 기한에 닿은 기록을 사후 대조가 통과시켰다', [])` 로, v6 에서는 끝까지 통과한다고 정적으로 예측한다. 틀리면
    RED 에서 멈춘다.
25. **기본값 결속 도구의 범위:** 범위안 §2 의 표는 v1 (직접 `L.f(…)` 호출만) 로 만들었다. 이번 v2 (부록 A) 는 같은 함수 안의 지역 별칭 호출
    (`fetch_env = L.fetch_env` · `cleanup = R.cleanup` 등) 도 보고, 실행기 대조에도 돌렸다 — 새로 보인 행은 l28 `fetch_env` 의 `config` (고정 목록 · 정책) 와
    실행기 대조의 `proc=PROC` (가짜 `proc_table` 이 인자를 읽지 않음) · `limit` · `kill_wait_s` · `settle_s` · `timeout` (정책) 이고, 결함은 없다. 도구는
    `**opts` 의 안 · 모듈 밖 함수 · 속성 체인 · 함수 밖으로 넘긴 별칭을 보지 않는다 — `_launch` 의 `**opts` 는 수동 분류다 (§1-3).
26. **판정기의 책임 범위:** 판정기는 §4-3 의 기준을 기계로 기록한다. 판정 근거는 증거 파일 (stdout · meta · 외곽 반환) 이고 판정기 출력은 그 기계 판정이다 —
    수동 판정과 다르면 멈춘다 (어느 쪽도 우선하지 않는다). 지난 시도의 작성자 스크립트 (저장소 밖 · 제출 안 함) 가 마지막 요약 줄을 짧은 요약의 "그 밖
    줄" 로 센 오분류는 판정 근거가 아니었고, 이번 판정기는 그 줄을 "마지막 줄" 로 따로 읽는다 (기준을 바꾼 것이 아니다). 판정기가 기준보다 엄격하게
    읽는 셋 (`FAILURES` 의 표 밖 실패 절 · stdout 어디의 `UNEXPECTED_RED_CAUSE` · 시험 파일과 meta `source_end` 의 결속) 은 §4-3 의 읽기 규칙에 적었다 —
    정상 출력에서는 발동하지 않고, 발동하면 멈춘다 (fail-closed). 판정기의 오판 가능성은 수동 판정과의 대조로만 막는다 (독립 증명 아님).
27. **판정기 · 작성기의 작성자 확인 (저장소 밖 스크래치 사본에만):** 초안을 스크래치의 사본 폴더에서만 돌렸다. 지난 RED 기록의 사본 (바이트 그대로) →
    STOP · 거짓 항목 `red.l33.exception` 하나 (76 항목 · §92 의 수동 판단과 같음 · 마지막 줄 오분류 없음) / l33 실패 절만 기대 모양으로 바꾼 합성 사본 →
    MATCH (76) / 합성 GREEN (네 파일의 AST 에서 만든 PASSED 71 · `71 passed`) → MATCH (20) · 합성 GREEN (실패 하나 · `-x` 멈춤 줄) → STOP (거짓 여섯) / 거부
    넷 (출력이 이미 있음 · 폴더 밖 판정기 · 단계 이름 밖 · 옛 이름 규칙) → 반환 2 · 쓰기 0 / 작성기 v2 → 없는 파일은 사유로 · 옛 이름 규칙은 거부. 합성
    기록은 판정기 확인용이고 증거가 아니다. 저장소 · 옛 증거는 읽기만 했고, 시험 · launcher · Git fixture 는 돌리지 않았다.
28. **새 경로 a2:** 증거 · 작업 · cache 경로에 시도 표지를 넣어 지난 시도와 날짜에 관계없이 겹치지 않게 했다. 단계 이름 (`01_red_e1_0b` · `02_green_e1_0b`)
    은 새 폴더 안이라 그대로다. `evidence/reil_c4e1_0b_a2_*` 가 하나라도 있으면 착수하지 않는다 (이번 승인은 한 번 · 다음 시도는 다시 새 표지와 승인).
29. **판정 기준의 연속성:** RED 표의 아홉 메시지 · 24 목록 · GREEN 71 · 공통 항목 · 예산은 §90 에서 정적으로 수용된 것과 같다. 이번에 바뀐 것은 예측 줄
    (참고값) · 읽기 규칙의 명시 · 판정기의 엄격한 셋 (§8 의 26) · 판정기 verdict 와 수동 판정의 대조라는 멈춤 조건 하나 (§4-1) 뿐이다.

## 9. 하지 않는 것

E1-1–3 (identity · 읽기 경로 · fetch · 자료 개봉 · run) · C4-A / B · E3b · H4 · pickle · 노트북 · 출판 비교 · 해 선택 · 재시도 · 실행 중 예산 변경 · 설치 ·
환경 재구축 · 원자료 커밋 · 대체 출처 · COMSOL. 다섯 모듈 · SOURCES.json · 기존 시험 (E0 · N1) · 기존 증거 (E0 · N1 · E1-0 · 지난 E1-0b 시도) · 지난
시도의 작업 폴더 · 봉인 · v1–v5 문서와 초안은 바꾸지 않는다 (삭제 · 재사용 · 이름 변경 0). 판정기 출력의 수정 · 판정기의 재실행 · 판정기 없이 계속하기도
하지 않는다.

## 10. 정하실 것

1. **사전 검토** — 이 요청과 초안 여섯 (launcher v6 는 그대로) 을 Codex 에 보낸다 (권장 · 발송문 `docs/REIL_C4E_E1_0B_PREREVIEW_SEND_v3_20261103.md` · 앞
   판은 `…_SEND_v2_20261030.md` · `…_SEND_20261030.md`).
2. (검토 수용 뒤) **E1-0b 한정 승인 (새 승인 · 시도 a2)** — 승인해도 E1-1–3 은 시작하지 않는다.

## 부록 A. 기본값 결속 정적 대조 도구 v2 (검토용 사본 · 실행 지시 아님)

작성자 도구 (저장소 밖 `SP/c4e1_tools/default_binding_check_v2.py` · sha256 `8b6c5d02e35c44f2d25b05c1eb0d32be6c39aa2a8f11c4dfa34436c5656aec21` · 2,859 B) 의
원문이다. AST 만 읽고 대상 파일을 실행하지 않는다. §1-3 의 표는 이 도구를 `<대조 v8> L <launcher v6>` · `<대조 v8> L <launcher v5>` · `<실행기 대조 v5> R
<실행기 v8>` 로 돌린 출력 (18 · 14 · 12 행) 을 분류한 것이다. 범위안 §2 의 표는 v1 (직접 호출만 · 지역 별칭 처리 없음) 으로 만들었다 (§8 의 25).

```python
"""정적 (AST 만 · 대상을 실행하지 않음): 대조 파일에서 <별칭>.<함수> 를 부르는 곳마다 — 직접 호출 `<별칭>.f(…)` 와, 같은 시험 · 도우미 안의 지역 별칭
(`g = <별칭>.f` · `g, h = <별칭>.f, <별칭>.h`) 을 거친 호출 `g(…)` — 대상 모듈 함수의 기본값이 모듈 상수를 가리키는 인자 중 호출이 넘기지 않은 것을
나열한다. `**kw` 로 넘기는 호출은 표시만 한다 (그 안은 보지 못한다). v1 은 직접 호출만 봤다 (지역 별칭 호출 — l28 · l31 · l32 등 — 을 놓쳤다).
    python -I default_binding_check_v2.py <대조.py> <별칭> <모듈.py>
"""
import ast
import sys
from pathlib import Path

ctl, mod = (ast.parse(Path(p).read_text(encoding="utf-8")) for p in (sys.argv[1], sys.argv[3]))
alias = sys.argv[2]
consts = {t.id for n in mod.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name)}
sig = {}
for n in mod.body:
    if isinstance(n, ast.FunctionDef):
        a = n.args
        pos = a.posonlyargs + a.args
        d = dict(zip([x.arg for x in pos][len(pos) - len(a.defaults):], a.defaults))
        d.update({k.arg: v for k, v in zip(a.kwonlyargs, a.kw_defaults) if v is not None})
        sig[n.name] = ([x.arg for x in pos], {k: v.id for k, v in d.items() if isinstance(v, ast.Name) and v.id in consts})


def target(node):
    """`<별칭>.f` (f 는 모듈 최상위 함수) 이면 f · 아니면 None."""
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == alias and node.attr in sig:
        return node.attr
    return None


rows = 0
for fn in ctl.body:
    if not isinstance(fn, (ast.FunctionDef, ast.ClassDef)):
        continue
    local = {}
    for s in ast.walk(fn):
        if isinstance(s, ast.Assign):
            for t in s.targets:
                pairs = zip(t.elts, s.value.elts) if isinstance(t, ast.Tuple) and isinstance(s.value, ast.Tuple) else [(t, s.value)]
                for tt, vv in pairs:
                    if isinstance(tt, ast.Name) and target(vv):
                        local[tt.id] = target(vv)
    for c in ast.walk(fn):
        if not isinstance(c, ast.Call):
            continue
        name = target(c.func) or (local.get(c.func.id) if isinstance(c.func, ast.Name) else None)
        if name is None:
            continue
        pos, dmap = sig[name]
        given = set(pos[:len(c.args)]) | {k.arg for k in c.keywords if k.arg}
        star = any(k.arg is None for k in c.keywords)
        miss = {p: v for p, v in dmap.items() if p not in given}
        if miss:
            rows += 1
            via = "" if target(c.func) else f" (별칭 {c.func.id})"
            print(f"{fn.name[:40]:40s} l.{c.lineno:<5} {alias}.{name}{via} {'(**kw) ' if star else ''}기본값 사용: {miss}")
print(f"행 {rows}")
```

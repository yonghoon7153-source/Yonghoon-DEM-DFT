# 85차 제출자 증거 — 원문 로그 · 탐침 (리뷰어 요청으로 보존)

85차 리뷰어가 고정 커밋에서 조회할 수 없다고 한 스크래치패드 파일을 **바이트 그대로** 옮겼다
(`-text !eol`). 셸 래퍼 안의 절대 경로는 제출자 세션의 스크래치패드다. 새로 만든 파일은 셋이다:
`probe/probe_g84_before_after.py` (재현판) · `probe/probe_rerun_*.txt` · `g61/g61_replay_clean.log` (+ 래퍼).
나머지는 전부 원 실행 당시 그대로이고 편집하지 않았다.

## 1. 계획 결속 탐침 (요청문 §3 · §6-a) — `probe/`

| 파일 | 무엇 |
|---|---|
| `g84_probe_real_reasons.txt` | **원 출력** (2026-09-30T10:54:35Z · `tee` 로 저장). 다섯 경우 모두 `STARTED_AND_FINISHED fits=True` |
| `probe_g84_real_reasons.as_run.py` · `probe_g84_real_reasons.as_run.command.txt` | 원 실행의 스크립트. 원래 파일이 아니라 셸 heredoc 이었고 따로 저장하지 않았다. **세션 기록 (tool_use `toolu_011vY9pKmvZMZkTqABCVkcdz`) 에서 한 글자도 바꾸지 않고 복원**했다. `.command.txt` 는 셸 명령 전체 |
| `probe_g84_before_after.py` | 재현판 (이번에 새로 씀). 같은 본문에 세 가지를 바꿨다: null 을 명시 · 패치 뒤 양성 대조 · `PROBE_COMMIT` 표기 |
| `probe_rerun_d81fdc01.txt` · `probe_rerun_f89b1401.txt` | 2026-09-30T17:40Z 재실행. 두 커밋을 각각 `git archive` 로 뽑은 **깨끗한 사본**에서 돌렸다 |

**원 실행 시점의 정확한 상태:** HEAD `2bceaf9e` (승인 기록 커밋). 작업 트리에는 커밋 전
`tests/test_gate84_round2a.py` · `tests/conftest.py` 가 있었고, 이것을 1 분 뒤 커밋한 것이
`d81fdc01` 이다 (tests 만 · 367 줄 추가). RUN_SCOPE 는 `2bceaf9e` 와 `d81fdc01` 이 같다
(source_digest `7187bd31740514d4`). 요청문은 이를 "`d81fdc01` 코드" 라고 적었다.

**재실행 결과**

- `d81fdc01` (패치 전)
  - 원본 스크립트: 첫 시도는 `FileNotFoundError` 로 실패했다. git 이 무시하는 `results/_smoke/_unit` 가
    archive 사본에는 없기 때문이다 (원 작업 트리에는 있었다). 실패 기록은 파일에 남겨 두었다.
  - 재현판이 그 디렉터리를 만든 뒤 원본을 다시 돌렸다 → 원 출력과 같은 **5/5 `STARTED_AND_FINISHED`**.
  - 재현판도 5/5 로 같았다.
- `f89b1401` (판정 대상)
  - 재현판: 다섯 경우 모두 `REFUSED ValueError …` (null · 패딩 hex64 · 다른 hex64 · 다른 source_digest ·
    계획 reference=halfcell). 양성 대조 (진짜 closure hex64) 는 `STARTED_AND_FINISHED fits=True`.
  - 원본 스크립트: 네 경우는 거부됐다. **`[n1_01 null digest]` 는 끝까지 돌았는데, 결함이 아니라 이름표가 낡은
    것이다.** 원본은 null 을 명시하지 않고 fixture `G81._v6_context` 의 기본값에 기댔다. GREEN 의 fixture
    정정 (요청문 §6-b w06) 뒤 그 기본값은 진짜 hex64 가 되어, 이 경우는 이제 유효한 계획이다.
    재현판이 null 을 명시한 이유가 이것이다.

## 2. 등록부 전체 변이 재생 — `full_replay/` (요청문 §4 최종 행)

- clean `28d0effe`, 단독 실행. 시작 HEAD = 끝 HEAD, status 0, 13:59:05Z → 16:24:03Z.
- `g85_replay_all.txt` 는 `mutation_replay.py` 의 stdout+stderr 전문이고, `g85_replay_all.log` 는 래퍼 로그다.
- 래퍼 파일 이름은 `run_g84_replay_all.sh` 다. 중단된 첫 실행 (아래 3) 에 쓴 래퍼를, 시작 전에 출력 파일
  이름만 `g84_*` → `g85_*` 로 바꿔 다시 썼다.
- 결과: ran 345 → 344 `물었다` · `★ 안 물었다` 1 (`incomplete_receipt_is_refused-g61`, 225 행 · 끝의
  `=== 문제 ===` 절) · 신고 11 · `--check-preimages` 는 "모든 변이 지점이 정확히 한 번 나타난다".

## 3. 중단된 첫 전체 재생 — `full_replay_aborted/` (요청문 §6-e4)

- clean `91f00a72`, 12:22:44Z → 13:56:17Z, 196 번째 변이에서 `OSError: [Errno 28] No space left on device`.
- 원인: 이 실행과 **병행으로** 단독 재생을 돌렸고, 그 sandbox 가 쌓여 디스크를 채웠다.
- 그때까지 결과: 193 물었다 · 안 물었다 3 · 실행오류 1.

## 4. g61 — `g61/` (요청문 §6-e5)

| 로그 | 상태 | 무엇 |
|---|---|---|
| `g61_mutant.log` (+ `run_g61_mutant.sh`) | clean `28d0effe` · status 0 · 15:40Z | **정정 전** `--emit-expect`. history 시험이 선언 증인이 아니라 customization 층 메시지로 빨개졌다 → rc 1 |
| `g61_replay2.log` (+ `run_g61_replay.sh`) | **dirty** — HEAD `28d0effe` + 커밋 전 패치 (status 1) · 16:24Z | 정정 뒤 첫 단독 재생. **`tail -5` 로 잘린 출력.** sandbox 는 작업 트리를 `shutil.copytree` 로 복사하므로 (`mutation_replay.py` `_make_sandbox`) 패치가 반영됐다. 같은 내용을 바로 뒤 `f89b1401` 로 커밋했다. 요청문 · 발송문의 "단독 재생 rc 0" 은 이 실행이다 |
| `g61_replay_clean.log` (+ `run_g61_replay_clean.sh`) | clean `b49c24fa` · status 0 · 17:41Z | 위 두 흠 (dirty tree · 잘린 출력) 을 없앤 재실행. **필터 없음.** `f89b1401` 대비 tests · mutation_replay · RUN_SCOPE diff 0. 재생 rc 0 · `--emit-expect` 는 두 node 모두 선언 증인 `Failed: DID NOT RAISE _ReplayError` 를 관측 |

## 5. 전체 회귀 · smoke

| 폴더 | 커밋 | 결과 |
|---|---|---|
| `full_regression_91f00a72/` | clean `91f00a72` | pytest 2039 passed · 1 xfailed (56:56) · smoke rc 0 (220 s) |
| `request_commit/` | 요청문 커밋 clean `b49c24fa` | pytest 2039 passed · 1 xfailed (51:45) · smoke rc 0 (158 s) |

- 91f00a72 래퍼의 마지막 단계 (전체 변이 재생) 는 병행 재생과 겹쳐 제출자가 중단시켰다
  (`Terminated` · `replay rc=143`). 전체 재생 증거는 2 의 `28d0effe` 실행이다.
- 두 pytest 로그는 `-q` 이고 `-rx` 가 없어 **xfail 한 node 의 이름이 로그에 없다.** 요청문이 적은 이름
  (`test_gate63_defensive.py::test_staging_an_input_outside_the_repo_is_still_unsupported`) 은 두 가지로
  확인했다. 첫째, 모듈 단독 재실행 (`python -m pytest tests/test_gate63_defensive.py -q -rxX`, 17:4xZ):
  `XFAIL … - §0 ⑦` · 22 passed · 1 xfailed. 둘째, 다른 xfail 후보인 `test_compare.py:4967` 은 조건부
  `pytest.xfail` 이라, 그것도 xfail 했다면 전체 수가 2 가 된다.

## 목록 (크기 · sha256 앞 16)

| 경로 | 바이트 | sha256[:16] |
|---|---|---|
| `full_regression_91f00a72/g84_full.log` | 572 | `e53511443fb62351` |
| `full_regression_91f00a72/g84_pytest_full.txt` | 2930 | `2a8cc540bc174e3f` |
| `full_regression_91f00a72/g84_smoke.txt` | 5591 | `9960c8e762bff1b0` |
| `full_regression_91f00a72/run_g84_full.sh` | 1329 | `56d1081b188ff55c` |
| `full_replay/g85_replay_all.log` | 878 | `c4987e6c81f557ba` |
| `full_replay/g85_replay_all.txt` | 48101 | `b11b827cc7b57c1b` |
| `full_replay/run_g84_replay_all.sh` | 648 | `3cbee4e205d1952a` |
| `full_replay_aborted/g84_replay_all.log` | 355 | `c50227eb92ba2c0d` |
| `full_replay_aborted/g84_replay_all.txt` | 25643 | `dcefdb656c456988` |
| `g61/g61_mutant.log` | 2095 | `fbe6b2fabd3ed559` |
| `g61/g61_replay2.log` | 588 | `e086304270b35904` |
| `g61/g61_replay_clean.log` | 1679 | `c51dcb2b092b2493` |
| `g61/run_g61_mutant.sh` | 331 | `48fd3bd20ebce31b` |
| `g61/run_g61_replay.sh` | 363 | `b26ffea5a3acdd21` |
| `g61/run_g61_replay_clean.sh` | 623 | `a710c0dd6f9b8608` |
| `probe/g84_probe_real_reasons.txt` | 277 | `ff44f18d9fe09760` |
| `probe/probe_g84_before_after.py` | 3579 | `077567b84c523be4` |
| `probe/probe_g84_real_reasons.as_run.command.txt` | 1810 | `3ec8c77df037cf46` |
| `probe/probe_g84_real_reasons.as_run.py` | 1630 | `7ee047bc0a153e55` |
| `probe/probe_rerun_d81fdc01.txt` | 1939 | `b4e5408179749fcd` |
| `probe/probe_rerun_f89b1401.txt` | 2730 | `5b4e1b703cee95fc` |
| `request_commit/g85_pytest_full.txt` | 2930 | `188b55c11ef12ee7` |
| `request_commit/g85_send.log` | 316 | `f3bf87d941cc7df6` |
| `request_commit/g85_smoke.txt` | 5591 | `e6c5eb1c26aec15a` |
| `request_commit/run_g85_send.sh` | 1039 | `aa019d5f5a7f3ab8` |

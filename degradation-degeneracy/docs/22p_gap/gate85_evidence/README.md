# 85차 제출자 증거 — 원문 로그 · 탐침 (리뷰어 요청으로 보존)

85차 리뷰어가 고정 커밋에서 조회할 수 없다고 한 스크래치패드 파일을 **바이트 그대로** 옮겼다
(`-text !eol`). 셸 래퍼 안의 절대 경로는 제출자 세션의 스크래치패드다. 새로 만든 파일은 셋이다:
`probe/probe_g84_before_after.py` (재현판) · `probe/probe_rerun_*.txt` · `g61/g61_replay_clean.log` (+ 래퍼).
나머지는 전부 원 실행 당시 그대로이고 편집하지 않았다.

> **정정 (85차 보충 검토 뒤 · 이 README 만 편집 · 원문 로그 바이트 불변).**
> ① 첫 보존 커밋 `1b49700e` 에는 표의 25 개 중 **18 개만** 들어갔다. `.gitignore` 의 `*.log` 규칙이
> `.log` 7 개를 조용히 빼, `git add` 가 경고 없이 건너뛰었다. 빠진 것은 `full_regression_91f00a72/g84_full.log` ·
> `full_replay/g85_replay_all.log` · `full_replay_aborted/g84_replay_all.log` · `g61/g61_mutant.log` ·
> `g61/g61_replay2.log` · `g61/g61_replay_clean.log` · `request_commit/g85_send.log` 이다. 다음 커밋에서 **같은 바이트**를
> `git add -f` 로 넣었다 (크기 · sha256 가 아래 목록 · `1b49700e` 판 README 와 같다). 그중 셋
> (`g85_replay_all.log` · `g61_replay2.log` · `g61_replay_clean.log`) 은 앞서 채팅 첨부로만 전달됐고, 그것들도
> 첨부본과 바이트가 같다 (보충 검토 패키지 `codex/reference/attached/` 와 `cmp` 일치).
> ② 3 절의 중단본 집계를 원문 행 표식 기준으로 고쳤다 (193 · 3 · 1 → 190 · 3 · 15).
> ③ 1 절에 `f89b1401` 쪽 원 스크립트 첫 호출의 `FileNotFoundError` · rc 1 을 적었다.
> ④ 목록 표를 **전체 sha256** 로 바꿨다 (앞 16 자 표기는 요약이었다).

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
  - 원본 스크립트 첫 호출: `d81fdc01` 쪽과 같은 이유로 `FileNotFoundError` · rc 1 (파일에 그대로 남겨 두었다).
    거부 증거가 아니며, 아래 결과와 합치지 않는다.
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

- clean `91f00a72`, 12:22:44Z → 13:56:17Z. `OSError: [Errno 28] No space left on device` 로 끝났고 종료 요약이 없다.
- 원인: 이 실행과 **병행으로** 단독 재생을 돌렸고, 그 sandbox 가 쌓여 디스크를 채웠다.
- **원문 행 표식 집계** (`g84_replay_all.txt` · 줄머리 기준): `물었다` **190** · `★ 안 물었다` **3** (122 · 153 · 160 행 —
  freeze · M3 · M8) · `★ 실행오류` **15** (196–210 행). 실행오류 15 는 독립 원인 15 개가 아니다. 첫 줄은
  "pytest-json-report 가 필요하다", 다음 13 줄은 "수집 rc 가 0 이 아니다 (1)" 로, 디스크가 찬 뒤의 연쇄 실패다.
  마지막 줄 (`coverage-records-the-sna…`) 은 traceback 으로 끊긴 불완전한 행이다.
- **이전 서술 정정:** 이 README 첫 판과 요청문 §6-e4 · 원장 §121 의 "196 번째 · 193 물었다 · 안 물었다 3 ·
  실행오류 1" 은 틀렸다. "193" 은 줄머리를 고정하지 않은 `grep -c 물었다` 로 센 값이라 `안 물었다` 3 행이 섞였다.
  "실행오류 1" 은 마지막 traceback 만 보고 ENOSPC 연쇄 14 행을 빠뜨렸다. "196 번째" 는 첫 실행오류 행의 위치다.
  원문은 고치지 않았고, 중단본은 다시 돌리지 않았다. 완주한 전체 재생 (2 절, 344 / 345) 과는 별개다.

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

## 목록 (크기 · 전체 sha256 · 25 개)

| 경로 | 바이트 | sha256 |
|---|---|---|
| `full_regression_91f00a72/g84_full.log` | 572 | `e53511443fb623519383f16731bb05a88c93eb44d8dac1bba64aedd3901ee098` |
| `full_regression_91f00a72/g84_pytest_full.txt` | 2930 | `2a8cc540bc174e3f519e366586b003b10bb18577e8bd32b8f2abb4cbb531cb0b` |
| `full_regression_91f00a72/g84_smoke.txt` | 5591 | `9960c8e762bff1b09e1081721c6656a00dc39ab49883695b085ee72aecd9d84b` |
| `full_regression_91f00a72/run_g84_full.sh` | 1329 | `56d1081b188ff55c6ccdc310d7b95bde0615e4b5ce200468d35f176f8ec62969` |
| `full_replay/g85_replay_all.log` | 878 | `c4987e6c81f557ba9b6cf6ede811f1141d6ffc750ae48dcd43e18da9581d6849` |
| `full_replay/g85_replay_all.txt` | 48101 | `b11b827cc7b57c1bdf84517e941b134fabdbcd13bb984b955f4d7a5de8a1d7f8` |
| `full_replay/run_g84_replay_all.sh` | 648 | `3cbee4e205d1952ae10f0e0237639b0c0dd1b87f6005589bd126db1110df953d` |
| `full_replay_aborted/g84_replay_all.log` | 355 | `c50227eb92ba2c0d1d3ea54edf71ea2358a8999a5ed09cff93f2f0883239e0d6` |
| `full_replay_aborted/g84_replay_all.txt` | 25643 | `dcefdb656c4569886d90745eab661d2c81460d6d243cdb4f494626c6ac94cfb0` |
| `g61/g61_mutant.log` | 2095 | `fbe6b2fabd3ed559edeadaf9dcad462af09d6c5e6a3b3a0a788adbcafa276811` |
| `g61/g61_replay2.log` | 588 | `e086304270b35904c4b322489f58e5b5fd3f84e59ec929bd535b78bc5a418f53` |
| `g61/g61_replay_clean.log` | 1679 | `c51dcb2b092b24936f3e0c1a0bf8519b4af047370e26663054a498ae210ba0d3` |
| `g61/run_g61_mutant.sh` | 331 | `48fd3bd20ebce31ba77a4673a7cd17fd39b24cb89507e5fa3212b1217b71542d` |
| `g61/run_g61_replay.sh` | 363 | `b26ffea5a3acdd21f5090317e98b17910a29f049af9b986592526fa6aa31be99` |
| `g61/run_g61_replay_clean.sh` | 623 | `a710c0dd6f9b8608e3744d5310aa1773ac9bc3fb5c485cb71fec9bc99ea6d565` |
| `probe/g84_probe_real_reasons.txt` | 277 | `ff44f18d9fe09760048e92b216ca5fa41f1d70375e9dcc54e6d5978c50df2177` |
| `probe/probe_g84_before_after.py` | 3579 | `077567b84c523be465d04649fcccd1baaed4b4aa1165a47659a37068b989a55c` |
| `probe/probe_g84_real_reasons.as_run.command.txt` | 1810 | `3ec8c77df037cf46f19cdedbb764115e74d36c60d26d60f961d8f2ac518b1918` |
| `probe/probe_g84_real_reasons.as_run.py` | 1630 | `7ee047bc0a153e55e51aaae9472bb2a82107d7ffb18d0b68f093b5f3d0d6cabf` |
| `probe/probe_rerun_d81fdc01.txt` | 1939 | `b4e5408179749fcdf5b2061db0691dc3df991a30d04021012c80b89b9c541c3a` |
| `probe/probe_rerun_f89b1401.txt` | 2730 | `5b4e1b703cee95fcb95feb77d5ab1da31190011a244af82fa4846a384992eccb` |
| `request_commit/g85_pytest_full.txt` | 2930 | `188b55c11ef12ee7221ee223d2f5f3e90970337f4d0bf471ff5e52db04b4bd7c` |
| `request_commit/g85_send.log` | 316 | `f3bf87d941cc7df6b84b84439d74b1d8ce78c020d718976dc584a6a9f1b64ec2` |
| `request_commit/g85_smoke.txt` | 5591 | `e6c5eb1c26aec15ac311ddcb5865f48c65f612f08a718533e2c94de9b8bce5a6` |
| `request_commit/run_g85_send.sh` | 1039 | `aa019d5f5a7f3ab8c7209c76e84ab11f2844b257afee748db3e7d10bf4333d7d` |

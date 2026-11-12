# Rint ② S0 단계 1 다시 + 탄소 접합 원장 저장본 실침대 재기 — 결과 전 등록 (2026-11-12 · 결과 0 건)

- **무엇**: S0 단계 1 (SBE · kgy · CPU 약 1.5 h) 을 Q2 · Q11 코드 묶음 반입 뒤 끝 핀으로 다시 돌리면서, 감싸개 `s0_store_probe.py` (블록 안 heredoc · md5
  관문) 가 S0 가 지은 원장으로 저장본 (`scripts/cjunc_store.py`) 의 쓰기 · 읽기를 같은 프로세스에서 잰다 — ① 저장 꼴 안인가 (`encode_strict`) ② 짓고 씀
  (`Store.get_or_build` · 발행 전 다시 읽기 대조 포함) ③ 새 Store 로 다시 = 적중 ④ 읽은 원장 = 지은 원장 (엄격 지문 · `registry_fp`) ⑤ ②–④ 의 메모리
  최고값 (VmHWM 되돌림).  S0 에는 **지은 그 원장 객체**를 돌려준다 — S0 출력 = 감싸개 없이 돈 것과 같다 (elapsed_s 만 다르다 · 픽스처 대조 3.11 · 3.8).
- **왜 지금 등록**: 2 회차 내부 반박 리뷰 재확인 (Codex 아님 · RCP2-04) — 결과 전 기대 E · 문턱 T 가 스크래치에만 있어 결과가 오기 전 등록을 확인할 자리가
  없었다.  같은 기대 · 문턱이 블록 머리 주석에도 있다.
- **1저자 결정 (11-12 밤 · 오버나잇)**: Q-B (가) = 공식 S0 단계 1 다시를 감싸개로 돌린다 (블록 기본 `PROBE=1`) · 문턱 T1–T3 [제안] 그대로 채택.
- **블록** = 같은 폴더 `s0_rerun_probe_block.txt` (ASCII · 느낌표 · 탭 · CR 없음 · 273 줄 · md5 `692b34ff05823c3f24354d8fe2b0a7d3`) · 보내기 전에 `PIN='<PIN>'`
  한 줄만 채운다 (반입 뒤 가지 끝 40 자리 — 블록이 fetch 뒤 가지 끝과 대조한다) · md5 관문 = 감싸개 `86e9bf4b4cfb79fa6e4a63d69cb414b0` · 감시 셸
  `ff385531653c294089ce58f08511b6ad` · 실행 = 1저자 (kgy).
- **감싸개 v2 (2 회차)**: `cjunc_store` 를 `carbon_junction` 보다 먼저 불러온다 — 저장본의 런 시작 코드 칸 (`cjunc_store._START` · RCP2-01) 이 원장
  모듈 적재 앞에 잡힌다 (payload 와 같은 차례 · `scripts/test_cjunc_store.py` P6) · 기록 `store_probe.json` 에 `store_start` (코드 칸 · 먼저 불린 모듈 ·
  못 셈 사유) · 호출마다 `code_drift` 를 더했다 (절대 경로 · 기계 식별자는 싣지 않는다).

## 결과 전 기대 (먼저 적음)

| | 내용 | 근거 |
|---|---|---|
| E1 | S0 rc 0 · 여섯 출력 · 반입 도구 (`docs/data/rint2_s0_sbe_20261108/tools/import_s0_tgz.py`) 채택 후보 · S0 보고 git_head = PIN · git_dirty False | 11-08 실측 (5,383 s · 표본 최대 RSS 5.43 GiB) · 픽스처 킷 모의 |
| E2 | 감싸개 호출 1 번 · instance **117,583** | 11-08 SBE S0 보고 `junction_census.census.n_instances` · 같은 침대 · 원장 코드 (`carbon_junction.py` · `fibre_segment_raster.py`) 는 11-08 핀 `f47bde0f6` 뒤 그대로 (S0 일곱 파일 가운데 바뀐 것 = `step3_sigma.py` · `mpm_webapp_payload.py` 둘) |
| E3 | encode ok · 쓰기 `built_written` · 읽기 `hit` · 같음 = 엄격 True · registry_fp True · `store_start` 의 preloaded `[]` · error None · `code_drift` `[]` · error None | 저장본 시험 (픽스처 · 합성 꼴) · 감싸개 픽스처 대조 |
| E4 | S0 의 계획 · 배열 = 11-08 과 같음 (코드 지문 · 시각 칸 빼고) | S0 계산 길 = 바뀐 두 파일의 바뀐 자리 (GPU 풀이 표현 · 저장본 배선 · git 환경) 밖 · 대조 = 본 세션 (반입 때) |

## 문턱 (1저자 11-12 밤 채택 · 넘으면 보고 — R 계획이 정한다)

| | 문턱 | 근거 · 넘으면 |
|---|---|---|
| T1 | 쓰기 (`seconds_write`) ≤ 600 s · 읽기 (`seconds_read`) ≤ 300 s · 읽기 ≤ 짓기 (`seconds_build`) 의 10 % | 보고 — R 팔마다 이득 = 짓기 − 읽기 가 작아진다 (근거 = 합성 어림 47 만 멤버 쓰기 ≈ 10 s · 읽기 ≈ 26 s 의 10 배 여유) |
| T2 | 메모리 증가 (VmHWM(②–④) − VmRSS(① 앞)) ≤ 4 GiB | 보고 — R 팔 (⑥ 시도 2 RSS 최대 32.9 GiB) 에 더해질 몫 · kgy 총 메모리 [미확인] |
| T3 | 저장본 파일 크기 ≤ 2 GiB | 보고 — 기계마다 폴더 하나 · 침대 · origin · 문턱마다 파일 하나 |

E3 어긋남 (쓰기 `built_write_skipped` · `built_write_failed` · `disabled` = `code_changed` 또는 `/etc/machine-id` 를 못 읽음 · 읽기 ≠ hit · 같음 False · error)
→ R 에서 `--cjunc-store` 를 쓰지 않는다 · 본 세션에 알림 · 고친 뒤 다시 잰다.

## 블록이 쓰는 자리 (전부)

- 새 로그 폴더 `~/s0log_<UTC>` (감싸개 · 감시 셸 · meta · rss.log · run.log · store_probe.json · out_sha256.txt · DONE · 멈춤이면 STOPPED) · 새 S0 출력 폴더
  `~/sdcp/ca1_s0_sbe_<UTC>_<TAG>` · 새 저장본 폴더 `~/sdcp/cjstore_s0probe_<UTC>` (`PROBE=1` · 재기 전용 — R 은 그 파일을 읽지 않는다 · 단계 1 문턱이 R 과
  달라 열쇠가 다르다 · 보고 뒤 지워도 된다) · 끝에 `~/s0log_<UTC>.tgz` (+ `.sha256`).
- BASE (`~/dem-mt`) 의 git 관리 자리: `git fetch` = FETCH_HEAD · 그 가지의 원격 추적 ref · 받은 객체 · `git worktree add` = BASE `.git/worktrees/` 아래
  관리 항목 + 핀 작업 트리 `~/dem-s0-<pin9>` (있으면 다시 씀 — 깨끗함 · HEAD = PIN 확인) · 그 작업 트리 안 `__pycache__` (git 무시).
- 킷 · 런 폴더 · 추적되는 리포 파일은 바꾸지 않는다 · σ · 솔브 없음.

## 멈춤 (rc 2 · S0 를 띄우지 않는다)

PIN 자리표 그대로 · PROBE 가 0/1 밖 · TAG 글자 밖 · 새 폴더 넷 가운데 이미 있는 것 · venv 없음 · 킷 없음 · BASE 가 git 아님 · 끝 표지 (DONE · STOPPED) 없는
앞 로그 폴더 (동시 실행 막기) · fetch 실패 · PIN ≠ fetch 뒤 가지 끝 · worktree add 실패 · 작업 트리 HEAD ≠ PIN · 작업 트리 더러움 · 핀에 `scripts/cjunc_store.py`
없음 · 감싸개 · 감시 셸 md5 다름 · 감시 셸이 30 s 안에 안 섬.

## 한정

- 단계 1 원장 = s_min 미등록 (None · 자기 후보 전부) — R 팔 원장 (봉인 s_min) 보다 instance 가 같거나 많다 = 크기 · 시간의 보수 쪽 어림.
- 감싸개의 메모리 몫이 감시 셸 rss.log 의 표본 최대에 섞인다 → 채택 대조 때 `store_probe.json` 의 ②–④ 구간 (VmHWM · 시각) 으로 가린다 · S0 보고의
  elapsed_s 에 재기 초가 들어간다 (시간 표에는 `store_probe.json` 의 초를 빼서 쓴다).
- 감싸개가 못 잡는 실패 (커널 OOM 등) 면 Q-B (나) — `PROBE=0` 공식 다시 + 같은 핀의 개발 재기 런 — 로 돌린다.
- 스크래치 확인 = 픽스처 킷 (instance 2) 감싸개 있음 ↔ 없음 출력 같음 (3.11 · 3.8.20) · 블록 heredoc md5 · `bash -n` · 1 판 블록의 가짜 HOME 모의 (멈춤 ·
  채택 후보) — 실기계 (kgy) 결과는 [미확인].

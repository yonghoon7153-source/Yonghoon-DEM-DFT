# GATE88 요청 — G87-N1 한정 보완 결과 (v6 fit-only claim 의 phase 계약) · 라운드 2b 종결 재요청 · 실행 GO 아님

> 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

## §0 판정 대상

| 항목 | 값 |
|---|---|
| 요청 HEAD | 이 요청문이 든 커밋 (SHA 는 발송문 · RUN_SCOPE 밖) |
| **코드 (판정 대상)** | **`e462a3d19`** — RUN_SCOPE 를 바꾼 커밋은 하나: `tools/preserve.py` (+138 −6) · `src/fitting.py` (+27 −14) (`run.sh` · `src/io.py` · `src/grid.py` 불변 — §14-1 상한 안). `source_digest` **`864edfb73b9695a1` → `7dd546baaee9e823`**. 그 뒤 커밋 (history `8adb3bb41` · 변이 `12a2c27be` · 영수증 `38522285f` · 자체 점검 고정 `07aefea11` · 사전 검토 묶음 `b064e2e42` · 사전 검토 기록 `ed397bab4` · 요청문) 은 전부 RUN_SCOPE 밖 |
| 사용자 승인 | 원장 §129 (2026-10-03) "게이트는 계약대로 착수하자" → 고정 표 `STAGE3_IMPL_ROUND1_SPEC.md` **§14** 를 코드 변경 전 커밋 (`00ed85b44`) |
| 판정 요청 | (1) **G87-N1 닫힘** — 비-smoke v6 fit-only leg 가 실물 lifecycle (승인 → 입력 대조 → 계산 → commit → 완료 기록 → 최종화) 로 `executed` 까지 간다 (2) v2 순서 · 결속 규칙 · claim 키 · receipt 바이트 불변 (3) 87차 수용 부분 (v5 골든 · v3 builder/index · 진입점 배선 · `v6` 이름) 불변 (4) **라운드 2b 종결 가부** |
| 아님 | 실행 GO · 새 연구 leg · 운영 원장 v6 계획 항목 · 세대표 등록 · p_ini · class 변경 · 투영 게시 · requirements (pybamm 고정 — 게이트 차수 밖 사전 검토 회신을 받았다 · G87-N1 종결 뒤 별도 라운드 · 사용자 결정 — `PYBAMM_PIN_PREREVIEW_REPLY_20261003.md`) |

## §1 고정 표 §14 ↔ 구현 대응 (좌표 = `e462a3d19`)

| § | 고정 | 구현 (`tools/preserve.py` 는 `PV` · `src/fitting.py` 는 `F`) | 회귀 node (`tests/test_gate88_fit_only_lifecycle.py`) |
|---|---|---|---|
| 14-2 a | 한 함수 `claim_phases_for_spec(spec)`: v2 · 버전 없음 · 미지 → `("grid", "fit")` · v3 + `fit.in_digest` hex64 → `("fit",)` · v3 + 그 밖 → 거부 (계획 index 에서 시작 전) | `PV:4035` `claim_phases_for_spec` · `PV:6149` `_check_v6_plan_slots` 가 항목마다 부른다 | f02_02 · (v2 그대로) f00_01 · f00_05 |
| 14-2 b | v3 claim 만 `phases_required: ["fit"]` 봉인 (받은 spec 에서 유도) · v2 claim 키 · 바이트 불변 · 닫힌 키 집합 둘 · 값은 정확히 `["fit"]` | `PV:4014` `CLAIM_KEYS_FIT_ONLY` · `PV:4019` `_claim_record_keys_ok` (`_read_claim_record` `PV:7548` · `_already_finalized` `PV:8853` 두 자리) · `PV:4024` `_claim_required_phases` (값 검사) · `PV:7491` `_claim_planned_leg` 봉인 · `PV:6884` `LegClaim.required_phases()` | f01_01 · f00_04 · f03_04 · **f03_05** |
| 14-2 c | `phase_done`: 집합 밖 phase 거부 · 순서 · consumed 는 claim 집합 위 (v2 바이트 같음) · fit-only 의 fit receipt 는 `input_package_digest` + `inputs` (`PHASE_INPUT_KEYS` 의 hex64 로 닫힘 · 다시 계산 일치) · `consumed = {"external_input": …}` · 계산 본체 하나 | `PV:6897` `phase_done` (`:6944` 집합 · `:6950` 결속 검사 · `:6997` 순서 `_order = list(_required)` · `:7016` consumed) · `PV:6705` `input_package_digest` (본체) · `PV:6721` `_assert_external_input_binding` · `F:849` `_record_phase(…, input_binding)` · `F:871` `_fit_input_binding` (fit 전용만) · `F:1181` `fit_input_package_digest` → `PV.input_package_digest` 위임 · `F:1701` staged 묶음 결속 · `F:1753` 완료 기록 | f01_01 · f03_01 · f03_02 × 3 · **f03_06** (inputs 둘) · **f00_06** (v2 receipt 불변) |
| 14-2 d | `finalize_leg`: missing = claim 집합 − 닫힌 phase · v2 consumed 대조 그대로 · fit-only 는 `consumed.external_input` == 계획 `fit.in_digest` (compare_digest) 且 `phases_required` == 계획 spec 재유도 · 기록 `phases` = claim 집합 | `PV:8929` `finalize_leg` (`:9048` missing · `:9125` 재유도 · `:9133–9141` 계획 in_digest 재대조 + receipt 묶음 ↔ consumed · `:9177` 기록) | f01_01 · f03_03 · f00_04 · f00_02 · **f03_06** (receipt 변조) |
| 14-2 e | 재개 · 상태 view 는 claim 집합을 쓴다 | 표현은 `CLAIM_PHASES` 그대로 (`PV:6888` `phases_done` · `inspect_leg_run` · `precheck_leg_run`) — **§6-c (등가 · 자체 신고)** | f04_01 (재개 → `phases_done == ("fit",)` · view `["fit"]` · finalize) · f01_01 |
| 14-2 f | 그대로: `CLAIM_PHASES` · v2 grid → fit 순서 · v2 null 분기 · grid gate (v3 계획 아래 거부) · smoke 면제 | 변경 없음 — 순서 검사 `if _open:` 은 기존 변이 `phase-order-is-enforced-g59` 의 앵커 그대로 | f00_01 · f00_02 · f00_03 · f00_05 |

## §2 RED → GREEN

| 단계 | 결과 | 원문 (`gate88_evidence/`) |
|---|---|---|
| RED (시험 16 node = `9e53a7edb` · 실행 09:17:02Z 는 HEAD `9b539ce8b` + 작업 트리 — 고정 표 커밋 `00ed85b44` 09:21:37Z 직전 · RUN_SCOPE = 87차 판정 대상 그대로 · GREEN 은 09:35:47Z) | **9 failed / 7 passed** — 실패 9 = f01_01 (양성) · f02_02 (index 가 v3 + null 을 받는다) · f03_01 (grid 를 받는다) · f03_02 × 3 (결속 검사 없음) · f03_03 · f03_04 · f04_01 (fit 완료 기록에서 "선행 grid" 거부) · 통과 7 = 처음부터 GREEN 이어야 할 대조 f00_01–05 · f02_01 × 2 | `01_red_test_gate88.log` |
| **G87-N1 실행 재현** | f01_01 traceback: `run_fit` → `_run_fit_staged` → `src/fitting.py:1740` `_record_phase(claim, "fit")` → `tools/preserve.py:6901` `PreserveError` "선행 phase ['grid'] 가 아직 안 닫혔다" — `commit_run_outputs` (`:1735`) **뒤** 거부 · claim 은 열린 채 (87차 지적 그대로) | 같은 로그 |
| 증인 고정 (`5cdf22bea`) | 실패 메시지에 실행마다 다른 묶음 digest 가 들어가 증인이 비결정 → 단언 내용 불변 · 메시지만 이유 범주 (`_why`) 로 · RED 재확인 9 / 7 | `02_red_after_witness_stabilization.log` |
| GREEN (`e462a3d19`) | test_gate88 16 + spy 정정한 61 · 62 모듈 → **37 passed** | `03_green_37passed.log` |
| 관련 21 모듈 (영수증 재생성 전) | 1 회차 탐침 오염으로 중단 (§6-e) · 2 회차 820 passed / **9 failed** (7 = 영수증 identity 낡음 — 재생성으로 닫힘 · 2 = spy 서명 → 정정 · 03 에 포함) | `04_…` · `04b_…` · `05_…` |
| 자체 점검 고정 (`07aefea11`) | node 8 추가 (f00_06 · f03_05 × 4 · f03_06 × 3) — **처음부터 GREEN** (정상 lifecycle 은 그 값을 만들지 않는다 · 도달 경로는 durable 변조와 손으로 만든 receipt) · "무는가" 는 변이 5 가 증명 (§3) · 모듈 **24 passed** | §3 |

## §3 변이 (`-g88` 21 = 16 + 자체 점검 5)

| 회차 | 명령 | 결과 | 원문 |
|---|---|---|---|
| 1 | `-k g88 --emit-expect` (16 등록) | 16/16 기대 node 빨강 · EXPECT 미선언 표시 · rc 1 | `06_…` |
| 2 | `-k g88` (EXPECT 16 · `12a2c27be`) | 16/16 "물었다" · rc 0 | `07_…` |
| 3 | `-k g88 --emit-expect` (20 — 고정 4 추가) | 새 4 관측 · 기존 15 는 선언과 실패 집합 · 증인 일치 · **`fit-only-claim-refuses-other-phases-g88` 의 baseline 이 빨갰다** — 같은 시각 같은 모듈을 손으로 돌려 고정 scratch 경로를 두 프로세스가 썼다 (§6-f) | `09_…` |
| 4 | `-k only-for-fit-only --emit-expect` (다섯째) | 1/1 관측 | `10_…` |
| 5 | `-k g88` (EXPECT 21 · 단독 실행) | **21/21 "물었다" · rc 0** — "실행한 변이 21건이 전부 기대 node 를 call 단계에서 물었다" (회차 3 에서 baseline 이 오염됐던 `fit-only-claim-refuses-other-phases-g88` 포함) | `11_…` |

- §14-3 변이 목록 ↔ 등록: v2 순서 규칙 제거 → **기존** `phase-order-is-enforced-g59` (앵커 `if _open:` 불변 · 전체 재생에서 판정 — 새로 등록하지 않았다) · 집합 유도 뒤집기 → `fit-only-claim-seals-its-phase-set` · `finalize-rederives-the-phase-set` · `v3-plan-needs-an-external-input-digest` · `index-asks-the-v6-external-input-rule` · `external_input` 대조 생략 → `finalize-compares-the-external-input-with-the-plan` · 결속 누락 허용 → `fit-only-receipt-carries-the-input-binding` · `input-binding-recomputes-the-package` · `fit-carries-the-staged-input-binding` · 닫힌 키 검사 완화 → `claim-record-has-two-closed-key-sets` · 기록에 grid 끼우기 → `finalize-records-only-the-claim-phases`. 그 밖 (같은 불변식의 다른 자리): `fit-only-claim-refuses-other-phases` · `fit-only-consumer-names-the-external-input` · `phase-order-runs-over-the-claim-set` · `finalize-counts-remaining-over-the-claim-set` · `finalize-checks-consumption-over-the-claim-set` · `one-package-digest-function`. 자체 점검 5: `claim-phase-set-value-is-exactly-fit` · `input-binding-keys-are-closed` · `input-binding-values-are-hex64` · `finalize-binds-the-receipt-package-to-the-consumer` · `fit-input-binding-is-only-for-fit-only-claims` (이름 끝 `-g88` 생략).
- 증인은 고정 이유만 — 한 개 손질: `fit-only-consumer-names-the-external-input-g88` 의 관측 문장에 실행마다 다른 묶음 digest 접두가 있어 `consumed.external_input None` 까지만 (G67-T1-b) · `test_g67_14_every_registered_witness_is_a_fixed_reason` 통과.
- 기존 앵커 199 (5 파일) 의 출현 횟수는 GREEN 전 (`5cdf22bea`) 과 같다 · 새 21 은 각 1 회 (`--check-preimages -k g88` "정확히 한 번").
- 등록부의 다른 374 변이의 `-k` 식이 test_gate88 node 를 하나도 고르지 않음을 pytest `KeywordMatcher` 로 확인 (선언 밖 "더 빨개짐" 위험 0).

## §4 영수증

현행 (`864edfb73b9695a1`) history 보존 `8adb3bb41` → `make_receipt.py paired_fixed5_v4 grid_fit_v5` clean `12a2c27be` 1 회 (rc 0 ·
09:49:27Z → 09:50:44Z) → `38522285f`. paired **35** · core `5b32e3b5e8e0a81b…` · grid **34** · core `f7e4cf939009b0dd…` (검사 수 불변 —
`src/io.py` 불변). diff 는 두 파일 각각 core 쪽 `core_sha256` · `validator_source_digest` (→ `7dd546baaee9e823`) 와 stamp 쪽
`validator_commit` · `generated_at_utc` · `runtime.platform` (컨테이너 커널 문자열 `fc-v50` → `fc-v64` — stamp 는 core 대조 밖) 뿐 ·
`src_io_sha256` 불변 · stamp dirty paired false · grid true (순차). 원장 앵커 2 × 2. 그 뒤 커밋은 RUN_SCOPE 밖이라 validator identity 불변.

## §5 전체 회귀 · smoke · 등록부 전체 재생

| 단계 | HEAD (clean) | 결과 | 원문 |
|---|---|---|---|
| 전체 pytest 1 회차 | `38522285f` | **중단** (27 % · 실패 0 시점) — 자체 점검 고정 (§2 끝 · §6-b) 을 넣으려고 멈췄다 · 판정 근거 아님 | `08_…aborted…log` |
| 등록부를 읽는 시험 모듈 11 (고정 커밋 전 사전 점검) | 작업 트리 | **중단** — 12 분에 3 node · 내부 상한 전에 끝나지 않을 것으로 보여 멈췄다 · 판정 근거 아님 (같은 모듈은 아래 전체 회귀) | `12_…aborted.log` |
| 전체 pytest `tests/ -q -rfEx` | `07aefea11` | **2133 passed / 1 xfailed / rc 0** · 2026-10-03T10:45:57Z → 2026-10-03T11:40:14Z (0:54:14) · 시작 HEAD = 끝 HEAD · dirty 0 | `13_…` |
| strict smoke `./scripts/smoke_e2e.sh` | `07aefea11` | **rc 0** · 2026-10-03T11:40:14Z → 2026-10-03T11:42:44Z · 시작 HEAD = 끝 HEAD · dirty 0 | `14_…` |
| 등록부 전체 재생 (`-k` 없음 · 분리 프로세스 · 시간 상한 없음) | `07aefea11` | **scenario 406 (executable 395 · declared 11) · site 444 · ran 395 · 395/395 call 단계에서 선언한 이유로 물었다 · 안 물었다 0 · rc 0** · 2026-10-03T11:42:44Z → 2026-10-03T14:13:33Z · 시작 HEAD = 끝 HEAD · dirty 0 | `15_…` |

변이 수: 87차 등록부 374 + `-g88` 21 = 395 executable (declared 11).

## §6 자체 신고

| # | 내용 |
|---|---|
| a | **증인 고정 (`5cdf22bea`)** — RED 커밋 뒤 시험 파일을 고쳤다. 실패 메시지에 실행마다 다른 묶음 digest 가 들어가 변이 증인이 비결정이었다 → 단언 내용은 그대로 두고 메시지만 이유 범주로. RED 재확인 9 / 7 (같은 node) |
| b | **자체 점검 고정 (`07aefea11`)** — 전체 회귀 1 회차 중에 GREEN diff 를 다시 읽다가, 더한 fail-closed 분기 넷이 어떤 시험 · 변이에도 묶이지 않음을 찾았다: `phases_required` 값 검사 · `inputs` 의 키 닫힘 · 값 hex64 · finalize 의 receipt 묶음 ↔ consumed 대조 — 그리고 "v2 receipt 바이트 불변" (`_fit_input_binding` 이 v2 에 None) 을 재는 node 가 없었다. 1 회차를 멈추고 node 8 + 변이 5 를 더했다. 생산 코드는 바꾸지 않았다 |
| c | **§14-2 e 표현 차이 (등가)** — `phases_done()` · `inspect_leg_run` · `precheck_leg_run` 은 `CLAIM_PHASES` 를 그대로 쓴다. fit 전용 claim 에는 grid 가 기록될 수 없으므로 (`phase_done` 이 집합 밖 phase 를 거부 — f03_01) 모든 도달 가능 상태에서 claim 집합을 쓴 것과 같은 값을 낸다. GREEN 초안은 셋을 claim 집합으로 바꿨으나 어떤 시험 · 변이로도 구별되지 않아 (등가 변이) 최소 diff 로 되돌렸다. "fit 이 닫혔으면 남은 일 = finalize" 는 f04_01 이 잰다 |
| d | **spy 서명 정정** — `tests/test_lock_lifetime_62.py` `_receipt` · `tests/test_logical_paths_61.py` `_spy` 가 새 키워드 `input_binding` 에 TypeError → `**kw` 를 받아 그대로 넘기게 (단언 불변) |
| e | **탐침 오염 (작업 트리 사본 한정)** — 관련 모듈 1 회차 중 격리 fixture 없이 돌린 내 탐침이 scratch worktree 의 `docs/22p_gap/_exec_class/` 에 기록 2 개를 남겼다 → 그 회차 중단 (rc 143) · 기록 보존 (`04b_…`) 뒤 삭제 · 2 회차 깨끗. 본 checkout 의 운영 authority 는 손대지 않았다 (`git status` 0) |
| f | **변이 회차 3 의 baseline 빨강** — `-k g88 --emit-expect` 가 도는 동안 내가 같은 시험 모듈을 손으로 돌렸다. 두 프로세스가 결정적 scratch 경로 (`/tmp/dd87/f03a` — 증인 결정성을 위한 고정 경로 · G67-T1-b) 를 같이 써 `fit-only-claim-refuses-other-phases-g88` 의 baseline 이 빨갰다. 선언은 바꾸지 않았고 회차 5 (단독) 에서 판정했다. 고정 경로라서 같은 모듈의 동시 실행은 안전하지 않다 — 전체 회귀 · 재생은 순차로만 돌렸다 |
| g | **계약 인용 좌표** — `STAGE3_CONTRACT.md` 의 `src/fitting.py` 인용 세 곳이 GREEN 삽입으로 밀려 갱신 (2103→2116 · 2053→2066 · 1375→1386 · `8adb3bb41` — 87차 §6-d 와 같은 꼴) |
| h | **§14-2 a 문구 — 커밋 전 정정** — 초안은 "그 밖 (버전 부재 · 미지) → 거부" 였으나 버전 없는 손 spec 으로 lifecycle 을 재는 기존 시험 (`tests/test_preserve.py` `_RUN_SPEC_L`) 을 깨므로 고정 표를 커밋하기 **전에** "지금처럼 (grid, fit) — 버전 분기 거부는 소비자 몫" 으로 고쳤다. 커밋된 §14 가 정정본이다 |
| i | **§14-3 "묶음 한 바이트 변경"** — lifecycle 수준 node 는 계획 `in_digest` 를 다른 hex64 로 둔 대조 (f02_01 `other_package`) 다. 묶음 바이트 민감성은 기존 `tests/test_fitting.py::test_the_external_input_binding_covers_the_whole_package` (51차 P1-E1 — 세 파일 각각 한 바이트를 덧붙여 거부 · 이제 preserve 의 단일 구현을 거친다) 가 잰다 — 새 node 로 반복하지 않았다 |
| j | **finalize 의 `_is_hex64` 두 조건은 등가 방어** — 계획 `in_digest` 의 hex64 는 바로 앞의 집합 재유도 (`claim_phases_for_spec`) 가 보장하고, `consumed.external_input` 이 hex64 가 아니면 계획과의 `compare_digest` 가 잡는다. 지워도 시험이 구별하지 못한다 (등가) — 방어 중복으로 두었고 변이로 고정하지 않았다 |
| k | **docs-lint 시간 상한** — 고정 표 §14 · 원장 §129 를 쓰는 동안 (커밋 `00ed85b44` 09:21:37Z 전후) `tests/test_docs_lint.py` 를 `timeout 900` 으로 돌렸다가 잘렸다 (rc 143) → 상한 없이 다시 358 passed (23:41 · 09:31:58Z 끝). 그 원문은 보존하지 않았다 — §5 전체 회귀가 덮는다 |
| l | **재생 도중의 작업 트리** — 등록부 전체 재생이 도는 동안 본 checkout 작업 트리에 게이트 차수 밖 사전 검토 기록 (PyBaMM · REIL 묶음 · 회신 기록 · 위키 정정) 을 올려 wiki lint (0 errors) · docs-lint (358 passed) 를 돌렸다. 재생은 시작 때 만든 sandbox 사본에서 돌고 본 checkout 을 읽지 않는다 (`--emit-coverage` 없이는 HEAD 도 읽지 않는다). 재생이 끝나기 전에 stash 로 되돌려 끝 줄이 `HEAD 07aefea11 · dirty=0` 이고, 끝난 뒤 `b064e2e42` · `ed397bab4` 로 커밋했다 |

## §7 하지 않은 것

실행 GO · 운영 원장 v6 계획 항목 · 세대표 등록 · p_ini · `--mode all` v6 · grid v6 · `scripts/plan_leg.py` · `src/io.py` · `src/grid.py` ·
`run.sh` · 영수증 schema · requirements (pybamm 고정 — 사전 검토 회신 접수만 · 사용자 별도 결정).

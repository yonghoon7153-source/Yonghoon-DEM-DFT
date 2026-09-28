# 79차 게이트 리뷰 요청 — G78-N1·N2 정정 문장 (단계 1) + 단계 2 한정 구현 (restart 행 로깅 · 깨진 parquet 발견) + 허용된 검증·영수증 결과 (실행 GO 아님)

> **상태: 79차 회신 접수 (2026-09-28) — G78-N1·N2 종결 · 단계 1 종결 · 단계 2 는 G79-N1(P2, `converged` 설명) 정정 뒤 종결 → `GATE80_REQUEST.md`. 아래 취소선은 79차 정정.** ~~확정 (2026-09-27).~~ 78차는 G77-N1·N3 를 종결하고 G77-N2 의 잔여 둘(G78-N1 관측 쌍 key · G78-N2 누락/분모)을 남기며 "단계 1+2 는 수정 조건부 적합" 이라 했다. 지시대로 **G78-N1/N2 수정 문장 + 단계 1+2 의 제한 diff·수치 불변/역사 reader 회귀 + 허용된 검증·receipt 결과**를 함께 낸다. 사용자 승인(2026-09-27): 단계 1+2 는 78차 회신 뒤 착수 · 보존 profile 선택 1 유지 — 그대로 따랐다.
> 76차 종결 유지. **새 실행 GO 를 묻지 않는다.** 단계 3~6 · provider canary · floor/pilot · 새 연구 계산 · class/투영 승격은 이번 범위 밖이다. `grid_fit_v5` 는 진단/no_active_claim 그대로.

## 판정 대상

| 항목 | 값 |
|---|---|
| 브랜치 | `claude/14-gate-code-review-9qkx05` |
| 요청문 커밋 | 발송문에 실측 기재 |
| **판정 대상 코드** | **`3dc269d80a7441b294d475b625b096baf3d1a459`** — RUN_SCOPE 마지막 변경 (단계 2: `src/fitting.py` · `src/io.py`) · `source_digest` **`c78d7969ef49fd07`** (78차 대상 `23c361ed` · `1c67a748598baadb` → 이 커밋). 그 뒤 커밋은 영수증·원장·변이 EXPECT·문서뿐 (RUN_SCOPE diff 0 — 발송 전 실측) |
| 영수증 재생성 | `194b1a55` (clean `3dc269d8` 에서 `make_receipt.py paired_fixed5_v4 grid_fit_v5`; 원본 `history/<leg>.validate.1c67a748598baadb.yaml`) |
| 정정 문서 | `GATE78_REQUEST.md` §2.1 (취소선 + 정정 행, `3e995c4f`) |
| 발견 원장 | `docs/08_REVIEW_RESPONSE.md` §109 (78차 접수 · 단계 1·2 기록) · §110 (실측) |
| 78차 패키지 원본 | `docs/22p_gap/gate78_review/` (zip `f41ee778…`, MANIFEST 37/37) |
| 새 시험 | `tests/test_gate79_stage3_logging.py` **13 node** (패치 전 9 failed / 4 passed — 사유 §109) · 변이 5 신규 (`mutation_replay.py -k g79`) |

## §1 G78-N1 · N2 — 정정 문장 (GATE78 §2.1 정정 행이 정본; 여기는 요약)

| id | 정정 |
|---|---|
| **G78-N1** 관측 쌍 key | `pair_group_id` 는 bank 공유 그룹(§4.2 그대로)이고 비교 단위가 아니다. 비교 단위는 `obs_key = (comparison_family_id, pair_group_id, treatment_id, noise_level, noise_realization_id, replicate_id)` — primary 고정 축은 `comparison_family_id = p22_grid_primary_v6` · `treatment_id = none` · `replicate_id = 0`. 같은 obs_key 에 objective 별 **정확히 한 행**; reference/bounds/조건 입력 identity 는 동일성 제약. 봉인 `cond_id` 와 일대일 결속 허용(충돌·중복 거부; 다른 leg 를 같은 cond_id 로 합치지 않음). planned roster = obs_key 의 사전 집합; 한쪽 행 부재는 그 집합에서 발견. 중복·교차 seed pairing 은 **구조 오류(거부)**. 실제 ID 코드는 단계 3 |
| **G78-N2** 누락·분모 | **N** = 사전 inclusion mask (grid-reference **recoverable** 군 — `classify_recoverability` 의 geometry 규칙 `alpha_true ≥ 1 − atol`, 결과 전 결속; 구조적 제외는 N 밖, solver 누락과 섞지 않음; 전체 격자로 바꾸면 estimand 변경) · **n** = complete-pair (두 행 · 유한 J·converged · label 을 만들 truth/복원값/채점 필드 유한·유효) · **m = N − n** (쌍 단위, 양쪽 누락도 1). `Δ_cc = D/n` 은 **조건부 기술통계**. 전체 planned set 민감도 `Δ_lower = (D+Σl_i)/N` · `Δ_upper = (D+Σu_i)/N` (관측된 쪽 유지, 미관측 label 만 0/1: 9 상태의 [l,u] 표 기재) — 같은 Δ 의 범위이지 co-primary·CI·p-value 아님. n=0 → Δ_cc 미정, N=0 → 전체 미정. **§6.2 실패·비유한 0건 gate 는 그대로**; 5% 는 별도 사전 reporting 정책(m/N ≤ 5% 일 때만 Δ_cc 를 primary 후보로 보고, 초과면 미완)이며 gate 통과·planned set 완료를 뜻하지 않음. missing-as-fail "Δ_worst" 는 폐기(취소선; 리뷰어 40쌍 반례 기재) |
| 비차단 | 채택 N = 연속 두 doubling 의 **시작 N** (5→10·10→20 통과 → 5), ladder 끝까지의 prefix 진단은 전부 보고 · §4 "승인 요청/대기" → 승인됨 · "복원 안 함" → 기존 대상 leg 영수증용 격리 복원만 예외 |

## §2 단계 2 한정 구현 — diff 와 78차 구현 경계 대응

| 경계 (78차 §5) | 구현 | 회귀 |
|---|---|---|
| 2 수치 동작 불변 | `_minimize_until_stable` 은 minimize 호출·갱신 규칙·반환 p/J 그대로, `termination` 을 다섯째 반환값으로 **추가**. `fit()` 루프·정렬·agree/spread 불변 | `g79_02[False/True]` — 변경 전 코드(`16d97ce6`)에서 잡은 골든과 부동소수 동일 · **실물**: 영수증 재생성의 격리 복원·validate·재채점이 봉인 summary 와 semantic 동일 (paired 34 · grid 33 검사) |
| 3 native vs 바깥 반복 · 어느 round | `termination = {native_last, native_best, outer ∈ {no_improvement, nonfinite, max_rounds}, n_rounds}` — native 는 scipy status/success/message/nfev/nit 그대로; `native_best` 는 `best_f` 를 낸 round(개선 없으면 None). ~~기존 `ok` = **마지막 round success** = `FitResult.converged` 그대로 (best round 와 다를 수 있음 — 시험이 그 경우를 만든다)~~ **G79-N1 정정: 기존 `ok` = 마지막 **유한** `fun` round 에서 갱신한 success (그런 round 없으면 초기 False); 비유한 round 는 ok 를 갱신하지 않고 break — 유한 뒤 비유한이면 ok 가 남는다. 계산 경로 불변, 설명만 틀렸었다 (`g79_03c`·`g79_03d`)** | `g79_03` · `g79_03b` · 변이 `native-best…` · `outer-stop…` |
| restart 행 필드 | `restarts_json` 원소에 `converged`(~~그 restart 의 마지막 round success~~ **G79-N1 정정: legacy ok — 마지막 유한 round 에서 갱신한 success, 없으면 False**) · `n_eval`(Σ = FitResult.n_eval) · `termination_status` 추가 | `g79_01` · `g79_04c` (production `run_fit`) |
| 실패 restart | `FitResult.restart_errors` → fits 열 `restart_errors_json` (index·source·오류). `restarts`/`n_restarts` 는 성공한 것만(불변); adaptive=False 즉시 실패(F86) 그대로 | `g79_04` · `g79_04b` · 변이 `failed-restarts…` |
| parquet 읽기 실패 | `_parquet_read_failure` (pyarrow 한 번 읽음) → `validate_provenance` `fits_읽기` · `validate_curves_provenance` `curves_읽기` 실패 항목; 예외를 올리지 않음 | `g79_05` · `g79_05b` · 변이 `broken-parquet…` |
| 4 역사 reader | `normalize_restart_record`: legacy_pair / legacy_dict / v6_prep_logging — 새 키 부재는 **None**, False/0 소급 금지 | `g79_06` · 변이 `absent-restart-fields…` |
| 기존 소비자 | 봉인 pin `row_projection.py` 의 `_restart_list` 와 validator `_restart_ok` 는 새 키를 가진 행을 그대로 받는다 (pin 불변) | `g79_07` |
| 5 복원 | 영수증용 격리 복원만 (`make_receipt.py`, 임시 디렉터리) · 대상 leg `grid_fit_v5` · `paired_fixed5_v4` 고정 | — |
| 6 strict smoke 는 작은 계산 | smoke 는 작은 grid/fit/score/restore 를 **수행**한다 — "연구용 새 leg/floor/pilot 0회" 이지 "solver 호출 0" 이 아니다 | §3 |
| 7 영수증 | 원본 `history/…1c67a748…` 보존 → clean `3dc269d8` 재생성 → 원장 두 값만. 필드 diff = `identity.validator_source_digest` · `identity.src_io_sha256` · `core_sha256` · stamp — validation·outputs 동일 | docs-lint 결속 시험 · `g70_e3_*` |

diff 범위 (RUN_SCOPE): `src/fitting.py` (+`_native_termination` · `_minimize_until_stable` 반환 확장 · `fit()` 기록 · `normalize_restart_record` · `run_fit` 열 1) · `src/io.py` (+`_parquet_read_failure` · 두 validator 의 `elif` 분기). 그 밖 RUN_SCOPE 파일 불변.

## §3 실행 출력 (커밋 뒤 실측)

```
판정 대상 코드                                3dc269d80a7441b294d475b625b096baf3d1a459
source_digest                                 c78d7969ef49fd07
전체 pytest (tests/)                          0 failed · 1958 passed · 1 xfailed (48:57)   (시작 HEAD = 끝 HEAD = c77674f6 · 미추적 0; 직전 f90a9c89 는 1 failed — §4)
strict smoke (scripts/smoke_e2e.sh)           rc 0   (작은 grid/fit/score/restore 계산을 포함한다 — 연구용 새 실행 0)
mutation_replay --check-preimages · -k g79     전 지점 1회 · 5/5 물었다 (3 · 1 · 1 · 2 · 1 node) · EXPECT 관측값 (3e995c4f)
영수증                                        paired_fixed5_v4 core e5893f855bf64b9f… (34 검사) · grid_fit_v5 core 352f55e50af3038f… (33 검사) · validator c78d7969ef49fd07
docs-lint                                     전체 회귀 안에 포함 · 요청문 커밋 뒤 단독 실행값은 발송문에
```

## §4 우리가 스스로 신고하는 것

- 영수증 필드 diff 에 `identity.src_io_sha256` 이 있다 — `src/io.py` 를 바꿨으니 identity 의 일부로 당연하며, 78차 §109 초판 커밋 메시지(`194b1a55`)는 "validator 식별·core·stamp 뿐" 이라고 적어 이 필드를 빠뜨렸다 (§109 본문은 포함). 정직 기록.
- ~~`converged` 의 뜻은 79차 이전과 같이 **마지막 round 의 success** 다.~~ **G79-N1 정정 (80차):** `converged` 는 79차 이전과 같이 **마지막 유한 `fun` round 에서 갱신한 success** 이고 그런 round 가 없으면 False 다 — 비유한 종료 round 는 `ok` 를 갱신하지 않으므로 "마지막 round 의 success" 라는 우리 설명이 틀렸었다 (동작은 그대로). best round 의 success 와도 다를 수 있다 — `termination_status.native_best`·`native_last`·`outer` 가 각각 따로 말한다. 이 의미를 바꾸는 것은 수치 동작 변경이 아니라도 이번 범위 밖이라 하지 않았다.
- 실패 restart 기록은 `restarts`/`n_restarts` 의 뜻을 바꾸지 않기 위해 별도 열 `restart_errors_json` 로 두었다 — fits 열이 하나 늘어난다 (새 실행부터; 기존 묶음 불변).
- 처음부터 통과한 새 시험 4개의 사유는 §109 (골든 2 · F86 유지 · pin 파서 수용).
- 첫 전체 회귀(`f90a9c89`)는 **1 failed** — `test_stage3_contract_cites_live_code_facts`: 계약 §1 이 인용한 `src/fitting.py` 줄번호(1421·1376·392-406)가 단계 2 추가로 밀렸다 (1487·1442·457-471). 교란 사실은 그대로(시험이 확인). 계약 본문은 손대지 않고 줄번호 세 곳 + 갱신 주석 한 줄만 고쳐(`c77674f6`, RUN_SCOPE 밖) 다시 돌린 결과가 §3 다.
- **xfailed 가 2 → 1 로 줄었다 — 25차 발견 9 가 닫혔다.** `tests/test_compare.py` 의 조건부 xfail(footer 를 깨뜨린 fits.parquet 에서 `validate_provenance` 가 `ArrowInvalid` 를 올리면 xfail, 아니면 `ok False` 와 `fits_읽기 ∈ fail` 을 요구)이 단계 2 의 `_parquet_read_failure` 로 **진짜 PASS** 가 됐다. 그 시험은 "계약 v4 §11 의 12·13 단계로 이월" 이라 적혀 있었고, 이번이 그 단계다. 우리는 이 시험을 손대지 않았다 (fail key 이름 `fits_읽기` 가 우연히 같다 — 시험이 요구한 이름을 먼저 읽고 정한 것이 아니라 구현 뒤 회귀에서 발견).
- 단계 3 의 일(`candidate_id`·`bank_index`·ID 코드·provider)은 하지 않았다. `STAGE3_CONTRACT.md` 본문도 손대지 않았다.

## §5 리뷰어에게 묻는 것

1. G78-N1·N2 정정 문장(§1 · GATE78 §2.1 정정 행)이 잔여를 닫는가 — 남으면 한 줄.
2. 단계 2 구현이 78차 구현 경계 1~7 안에 있는가 (특히 `converged` 의 기존 뜻 유지 · native/outer 구별 · 역사 reader 의 None).
3. 단계 1+2 종결 판정. 종결이면 다음 코드 라운드(단계 3: 묶음 1·2 schema · ID preimage · provider DAG — no-warm 경로 명시 분기)를 새 사용자 승인 뒤 열어도 되는가 (이번에 착수하지 않는다).
4. 실행 GO 아님 · grid_fit_v5 진단 전용 · 새 연구 계산 0 확인.

## §6 발송 규칙

70차 §6 그대로. 이 요청문과 발송문은 같은 말을 한다: **G78-N1·N2 정정과 단계 2 한정 구현의 판정을 요청한다. 실행 GO 는 묻지 않는다.**

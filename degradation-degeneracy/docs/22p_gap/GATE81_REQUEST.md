# 81차 게이트 리뷰 요청 — 단계 3 **제한 구현 범위·사전 고정 사항 확인** (§3.2 단계 3 · 구현 착수 아님 · 실행 GO 아님)

> **상태: 81차 회신 접수 (2026-09-28) — 수정 조건부 적합 · G81-N1·N2·N3 (P1 각) · 3-A/B/C 한 코드 라운드 권고 · Q1·Q4 수용 · Q2·Q3 조건부 · 구현 착수는 사용자 별도 승인 뒤 (원장 §114 · `gate81_review/codex/NEXT_APPROVAL_SCOPE_DRAFT.md`). 아래 취소선은 81차 정정.** ~~확정 (2026-09-28).~~ 80차는 G79-N1 종결을 수용하고 단계 1+2 를 한정 범위에서 종결했다 (잔여 P1/P2 0 · 원장 §112). 리뷰어 문장: "다음은 사용자가 원하면 **단계 3의 제한 구현 범위·사전 고정 사항을 확인해 별도 승인**하는 것이다. 이번 회신만으로 착수하거나 pilot/연구 실행 GO를 부여하지 않는다" (`gate80_review/codex/REVIEW_KO.md`). 이 요청은 그 확인이다. **사용자 결정 (2026-09-28): 이 범위 확인 요청의 발송을 승인** — 구현 착수 승인이 아니다. 착수는 81차 회신 뒤 사용자의 별도 승인으로만. 코드는 바꾸지 않았다 (RUN_SCOPE diff 0 · `source_digest eda3feb8f4536511` 그대로). 76차 종결 유지 · 새 실행 GO 아님 · `grid_fit_v5` 진단/no_active_claim 그대로.

## 판정 대상

| 항목 | 값 |
|---|---|
| 브랜치 | **`claude/gate80-standby-9a26dd5f`** (임시 대피 서브 · 2026-09-28 분기). 본진 `claude/14-gate-code-review-9qkx05` 는 **`9a26dd5f31ca6fae45d5a55f5c59e33408371984` 에서 동결** — 80차 요청 HEAD 와 같은 SHA. 서브는 본진의 fast-forward 후손이며 복귀는 본진 ← 서브 ff-only (`BRANCHES.md` 2026-09-28 절). 서브의 커밋은 전부 문서·패키지 보존 (`git diff --stat 9a26dd5f HEAD -- src tools configs scripts run.sh requirements*.txt` 가 비어 있다 — 실측) |
| 요청문 커밋 | 발송문에 실측 기재 |
| **코드 (RUN_SCOPE 마지막 변경)** | **`6ffa98d4df542aa42abde2f94685beffec33312c`** · `source_digest eda3feb8f4536511` — 80차 판정 대상 그대로 (요청문 작성 시점 HEAD `cc4b01ad` 에서 재계산 일치). 이 요청은 코드를 바꾸지 않는다 |
| 심사 대상 문서 | 이 문서 §1~§3 (제안 범위 · 사전 고정 · 실행 경계) · `docs/22p_gap/GATE78_REQUEST.md` §3.1·§3.2 (77차 회신 수용 표, 78차 종결) · `docs/22p_gap/STAGE3_CONTRACT.md` v4 §2·§3·§4.2·§4.4·§5·§9.4·§11·§13.1 |
| 발견 원장 | `docs/08_REVIEW_RESPONSE.md` §112 (80차 접수 · 이월 1건) · §109 (78차 — G77-N3 종결, §3.1/§3.2 수용) · §111 (79차 — 비차단 이월) |
| 80차 패키지 원본 | `docs/22p_gap/gate80_review/` (zip `17e5b50b…` 315,543 B · MANIFEST 28/28 · `-text !eol` 규칙 `bf6fa29e` 먼저) |
| 이번 라운드 새 시험 | **없음** (구현 착수 아님). 관련 기존 시험 collect 실측: `tests/test_design_wire.py` 31 node · `tests/test_gate79_stage3_logging.py` 15 · `tests/test_docs_lint.py` 358 |

## §0 이 요청이 묻는 것 / 묻지 않는 것

| 묻는 것 | 묻지 않는 것 |
|---|---|
| §1 의 범위 표가 GATE78 §3.2 **단계 3** 과 같은가 — 늘리거나 줄일 곳 | 구현 착수 (회신 뒤 사용자 별도 승인) |
| §1 의 갈림 지점 4곳(unit-cube bank · 혼합 restart 행 정책 · provider 봉인 실물 · ID 도메인 불변)에 대한 판정 | 단계 4~6 · floor 측정 · pilot · 본 계산 · provider canary |
| §2 사전 고정 사항 중 이번 단계가 **건드리는** 항목(provider 동결 형식)의 확인 | ladder·max B·중단 규칙·sentinel·자원 상한 값의 재심 (78차 종결, 그대로) |
| §3 실행 경계 (RUN_SCOPE 이동 · 영수증 1회 재생성 · 골든 벡터 정책) | 실행 GO · 새 연구 계산 · class/투영 변경 · `row_projection.py` 봉인 |

## §1 제안 범위 — GATE78 §3.2 **단계 3** 을 세 조각으로 (현행 코드 앵커는 HEAD `cc4b01ad` 실측)

GATE78 §3.2 단계 3 원문: "묶음 1·2 의 planned/realized schema · ID preimage (`pair_group_id`·`bank_id`·`candidate_id`) · 묶음 3 provider DAG/solution map. primary no-warm 경로는 명시적 null/no-provider 분기. 후보 ID/인덱스·수량을 serializer/validator 까지 잇는다 (`candidate_id`·`bank_index` 는 여기)" · 의존 2 · RUN_SCOPE `src/` · `tools/design_wire.py`.

### 1.1 현행 상태 (있는 것 / 없는 것 — 실측)

| 축 | 있는 것 | 없는 것 |
|---|---|---|
| ID 도메인 (묶음 2) | `tools/design_wire.py` 537줄 · `SCHEMA = "pairing-design/v6.3"` · arm registry A/B/C/D/G_A/G_C (계약 §5) · `pair_group_id()` `:419` · `bank_id()` `:449` · `candidate_id()` `:500` (`candidate/v2`, source 3종 payload schema `:71–77` — warm 은 `provider_objective`·`provider_artifact_sha256`·`solution_map_sha256`, random 은 `bank_index`·`unit_cube_bytes_sha256`) · `design_binding()` · `src.grid.Condition` 왕복 결속 · 골든 `tools/design_golden.yaml` (`tests/test_design_wire.py` 31 node). 마지막 변경 `e06b245b` (59차) | **`src/` 가 import 하지 않는다** (`grep -rl design_wire src/` = 0; importer 는 `tools/gen_design_golden.py` · `tests/test_design_wire.py` 뿐). 골든의 bank·bounds·payload sha 는 **placeholder** (`tools/gen_design_golden.py:24–32`: `BANK_SHA = "f"*64` · `BOUNDS_SHA = "a"*64` · payload `"1"*64`~`"4"*64` · `bank_index 7`) — 실물 bank·bounds digest 는 아직 없다 |
| 후보 생성 (bank) | `src/fitting.py::fit()` `:241` — `rng = np.random.default_rng(seed)` `:263` · `x0 = init if k == 0 else rng.uniform(lb, ub)` `:269` · source 라벨 `warm/base_init/random` `:274` | **unit cube bank 가 아니다** (물리 bounds 에서 직접 추첨 · bounds mapping digest 없음 — 계약 §4.2 "bank 는 unit cube 에서 먼저 생성" 미구현) · `bank_index` 개념 없음 (`i` 는 restart 순번) · `candidate_mode` 3종(계약 §3: `legacy_slot_replace`·`equal_start_count_base_retained`·`union`) 미구현 — 현행은 `[base|warm] + random×(B−1)` = `legacy_slot_replace` 한 가지 |
| warm provider (묶음 3) | `src/fitting.py::_fit_one()` `:457–475` — 앞 목적함수 해 `seed_p` 를 **같은 프로세스 안에서** 뒤 목적함수 `init` 으로 넘김 · `task["warm_start"]` bool (기본 True) · `_has_dqdv()`/`_warm` 규칙 `:443–454` · 행 `warm_started` `:516` | provider **artifact 없음** · `solution map` 없음 · `warm_provider_map` 명시 없음 (암묵 `w_dqdv != 0`) · no-warm 이 **null 분기가 아니라 bool off** · 계약 §2 의 `*_provider_artifact_sha256`·`*_provider_solution_map_sha256`·`p_ini_values_sha256`·`provider_protocol_sha256`·`realized_candidate_map_sha256` 전부 미실현. **이름 충돌 주의**: `tools/preserve.py` 의 `provider` (`:389–397` 등) 는 보존 backend 의 retention/lock provider 이지 warm provider 가 아니다 |
| restart 행 (§9.4) | serializer `src/fitting.py:330–331` — `p/J/i/source/warm/converged/n_eval/termination_status` (79차) · `_RESTART_NEW_KEYS` `:337` · 역사적 reader `normalize_restart_record()` `:340` (legacy_pair / legacy_dict / v6_prep_logging) · validator `src/io.py::_restart_ok()` `:789` (p 길이 4 유한 · J · i · source) · `validate_provenance()` `:1484` `restart_출처` 검사 `:1853–1875` (모든 행·모든 원소) · parquet 읽기 실패 구조화 `_parquet_read_failure()` `:775` | §9.4 다섯 필드 중 **`candidate_id`·`bank_index` 둘이 없다** · validator 는 새 키를 검사하지 않는다 (v6 writer 강제 없음) · 혼합/손상 행(새 키 일부만) 정책 없음 — 79차 §6 이월: `normalize_restart_record` 가 일부 키 행을 `legacy_dict` 로 내려 이미 있는 값까지 None |
| planned/realized (묶음 1) | `tools/preserve.py::PlannedLeg` 최소 envelope · `planned_id` · 트랜잭션의 `execution_receipt` (계약 §13.1) | stage×objective×arm 별 예산/실현 count · 실제 leg index 결속 · `realized_candidate_map_sha256` |
| 소비자 (봉인) | `docs/22p_gap/row_projection.py:202–221` 는 restart 의 `J`·`source` 만 읽는다 (새 키 무시 — 79차 `g79_07` 로 고정) · `src/scoring.py:159–212` multistart 지표 재구성 | — (이번 단계에서 바꾸지 않는다; 아래 §3) |
| 세대표 | `CLAIM_STATUS.yaml` `source_digest_generations` 4 항목 (v5 ×3 · `a72c0f3a485c19bb` v6_prep) · 전이 v5→v6 `[diagnostic, excluded]` | 현행 `eda3feb8f4536511` 은 표에 없다 (grep 0) · **v6 세대 digest 없음** — 계약 §11 대로 동결 지점은 13 의 끝 |

### 1.2 제안 범위 (한다 / 안 한다)

| 조각 | 이번 라운드에 **한다** | **안 한다** | RUN_SCOPE |
|---|---|---|---|
| **3-A 결속** (묶음 1·2) | `src/` 가 `tools/design_wire.py` 를 실제로 부른다: fit task → `design_binding()` → `pair_group_id`/`bank_id` 를 행에 기록 · run_spec 에 계약 §2 의 planned 필드(`*_budget_by_objective` · `*_candidate_mode` · `*_bank_sha256` · `bank_version` · `warm_provider_map`) 를 **v6 writer 필수축**으로 (없으면 실패 — 78차 §2.1 버전 경계) · realized 쪽 `realized_candidate_map_sha256` · `random_bank_prefix_len` 산출 · `PlannedLeg` envelope 에 stage×objective×arm 예산/실현 count | 실제 v6 leg 실행 · 세대표 갱신 (digest 동결은 13 의 끝) · `pairing_design_id` 구 필드 제거 (묶음 6 = 단계 4) | `src/fitting.py` · `src/io.py` · `tools/design_wire.py` · `tools/preserve.py` |
| **3-B provider DAG** (묶음 3) | primary no-warm 을 **명시 분기**로: `warm_provider_map` 이 비었거나 해당 목적함수 항목이 `null` 이면 provider 없음 → `[base] + bank[:B−1]` (계약 §3 "provider 가 없는 연쇄 1번째"), 행에 `warm_provider: null` · `candidate_id(source="base_init"|"random")` 만 · warm 행 0 (회귀로 고정). secondary warm arm 은 provider 를 **artifact 로 봉인**: provider leg 의 fits 산출 sha (`provider_artifact_sha256`) + 조건별 solution map (`cond_id → p`, `solution_map_sha256`) → `candidate_id(source="warm")` payload. materialize → seal → consume 순서를 preserve 트랜잭션(묶음 9) 위에 두고, 봉인 전 consume 을 거부 | provider **실행**(canary) · 실물 provider leg 생성 · `equal_start_count_base_retained`/`union` 의 예산 실측 | `src/fitting.py` · `tools/preserve.py` |
| **3-C 행·검증** (§9.4 나머지) | serializer 에 `candidate_id`·`bank_index` (random 은 unit-cube bank 행, base_init/warm 은 `null`) · `_restart_ok` 를 세대별로: v6 writer 행은 8+2 키 전부 필수·타입·유한성, 옛 세대는 기존 4 키 규칙 유지 · `normalize_restart_record` 혼합 행 정책 (§1.3 Q2) · `validate_provenance` 에 `restart_후보` 검사 추가 (모든 행·모든 원소, F50/F61 규칙 그대로) | `row_projection.py` 변경 (봉인 불변) · `src/scoring.py` 지표 변경 · 옛 fits 소급 수정 | `src/fitting.py` · `src/io.py` |
| 공통 | RED 먼저 (`tests/test_gate81_stage3_wire.py`) · 변이 등록 (`docs/22p_gap/mutation_replay.py`) · v5 historical reader 회귀 (`g79_02` 골든 · `g79_06`) 유지 · 전체 회귀 + strict smoke (clean 커밋) · 라운드 끝 영수증 1회 (§3) | 새 과학 수치 · 계약 §13.1 본문 갱신 (리뷰 판정 뒤) | — |

### 1.3 갈림 지점 — 리뷰어 판정이 필요한 곳 (우리 제안 명시)

| # | 갈림 | 우리 제안 | 되돌릴 수 있는가 |
|---|---|---|---|
| Q1 | **unit-cube bank 생성 + bounds mapping digest** 를 단계 3 에 넣는가. `candidate_id(source="random")` 의 preimage 가 `bank_index`·`unit_cube_bytes_sha256` 를 요구하므로(계약 §4.2 · `design_wire.py:77`) 이것 없이는 3-C 의 `bank_index` 가 정의되지 않는다 | **넣는다** (3-A). 새 `candidate_mode` 경로에서만 unit cube → `lb + u·(ub−lb)` mapping · `exact_bounds_sha256` 는 실제 ordered `lb/ub` bytes digest. **legacy 경로(`rng.uniform(lb, ub)`)는 바이트 불변** (`g79_02` 골든이 지킨다) — 두 경로가 같은 난수를 내는지는 주장하지 않는다 | ~~예 — 단계 5(묶음 4·5)로 미루면 3-C 는 `candidate_id(random)` 를 `null` 로 두고 `bank_index` 만 남긴다~~ **81차 정정: Q1 포함 확정 — 미채택 문구 취소 (§5 의 문구와 값이 달랐다: 여기 `candidate_id` null · §5 `bank_index` null; 리뷰 §6)** |
| Q2 | 혼합/손상 restart 행(새 키 일부만) 정책 — 79차·80차 이월: "명시 거부 또는 부분 기록 분리" | **v6 writer 는 전부-또는-실패** (부분 행을 쓰지 않는다) · reader 는 부분 행을 `record_generation = "mixed_invalid"` 로 분류하고 validator `restart_후보` 가 **거부** (None 으로 내리지 않는다) · 옛 세대(legacy_pair/legacy_dict)는 그대로 | 예 — "부분 기록 분리"(값 있는 키는 살리고 없는 키만 None) 로 바꿀 수 있다 |
| Q3 | provider 봉인의 **실물**: `provider_artifact_sha256` = provider leg 의 fits parquet 봉인 sha · `solution_map_sha256` = 조건별 `cond_id → p` map 파일 sha · `provider_protocol_sha256` = provider run_spec canonical digest — 이 셋으로 계약 §2 다섯 sha 를 채우는가 (`p_ini_values_sha256` 은 half-cell arm 에서만) | 위 정의. 봉인은 preserve 트랜잭션의 payload seal 을 재사용 (재구현 없음) | 예 — 리뷰가 다른 실물을 지정하면 그대로 |
| Q4 | ID 도메인(`pair_group_id`·`bank_id`·`candidate/v2` preimage) 을 **바꾸지 않는다** — 골든 `design_golden.yaml` 재생성 없음. placeholder sha 자리에 실물 sha 를 넣는 것은 도메인 변경이 아니다 | 불변. 3-A 에서 preimage 를 늘려야 할 필요가 보이면 **구현하지 않고** 별도 질문 | 예 |

## §2 사전 고정 사항 — GATE78 §3.1 재확인 (78차 종결 · 78차 비차단 정정 반영)

| 항목 | 고정값 (그대로) | 이번 단계 3 이 건드리는가 |
|---|---|---|
| 탐색 ladder | `[5, 10, 20, 40]` | 아니오 (단계 5) — 3-A 의 `*_budget_by_objective` 는 값이 아니라 **축** |
| 최대 B | 40 · ladder 끝까지 §6.2 못 지나면 미채택("plateau 미달") | 아니오 |
| 중단 규칙 | 연속 두 doubling 이 §6.2 넷 통과 → 그 N 채택. **N = 두 doubling 의 시작 N** · ladder 끝까지의 prefix 진단은 전부 보고 (78차 비차단 정정) | 아니오 |
| numerical floor | 별도 한정 승인 측정 단계 · tolerance 숫자 발명 금지 | 아니오 |
| `mono_tol` | max-N 1회 + prefix minima offline 계산 기본 (계약 §4.4 nested prefix 는 random bank 에만) | 아니오 — 다만 3-A 의 unit-cube bank 가 nested prefix 의 전제다 |
| material 규칙 | stratum n<100 → 0건 · n≥100 → `count*100 <= n` | 아니오 |
| **provider 동결** | primary 는 provider 없음(명시 null/no-provider) · secondary warm arm 은 provider artifact·solution map sha 먼저 봉인 | **예 — 3-B 가 이것의 구현** (형식은 §1.3 Q3) |
| sentinel panel | 5 archetype × reference 2 × noise 3 × objective 2 = 60 최소 · `sentinel_panel.yaml` 에 exact id/좌표/seed/sha/holdout 의무 · 없는 SHA 를 계획값으로 가장하지 않는다 | 아니오 (단계 5) — 파일은 아직 없다 (`ls docs/22p_gap/sentinel_panel.yaml` 부재, 실측) |
| 자원 상한 | core-time 상한을 leg·비용표에 (`833 s × 28` 은 점유 근사) | 아니오 (단계 6) |

## §3 실행 경계 (78차 §4 규칙 그대로)

| 항목 | 한다 | 안 한다 |
|---|---|---|
| RUN_SCOPE | 움직인다 (`src/fitting.py` · `src/io.py` · `tools/design_wire.py` · `tools/preserve.py`) → 영수증은 **최종 코드가 고정된 라운드 끝에 대상 leg 별 1회** (`paired_fixed5_v4` · `grid_fit_v5`; 원본 `history/<leg>.validate.eda3feb8f4536511.yaml` 로 먼저 보존; restore·validate·재채점 실행이므로 **착수 승인 범위에 명시 포함**; 실패하면 새 검증 완료로 붙이지 않는다) | 중간 digest 의 옛 영수증을 새 PASS 로 쓰는 것 · 다른 복원 |
| 증거 | RED 먼저 · 변이 · 전체 회귀 + strict smoke (clean 커밋, 시작 HEAD = 끝 HEAD) · v5 historical reader 회귀 · no-warm 경로 warm 행 0 회귀 · 부분 행 거부 회귀 | 새 과학 수치 · 실제 v6 leg |
| 봉인 | `row_projection.py` · 골든 `design_golden.yaml` · 기존 fits/영수증 history | 재생성·소급 수정 |
| 브랜치 | 서브 `claude/gate80-standby-9a26dd5f` 에 덧붙이기 · 본진 동결 유지 · 복귀 ff-only | 본진 커밋 · 다른 브랜치 |
| 산출 | GATE82 요청문 (코드 라운드 판정) | — |

## §4 실행 출력

요청문 작성 시점 (HEAD `cc4b01ad`, clean tree) 실측:

```
source_digest                                 eda3feb8f4536511   (python -c "from src.io import source_digest; print(source_digest())")
RUN_SCOPE diff 9a26dd5f..HEAD                 0 파일             (git diff --stat 9a26dd5f HEAD -- src tools configs scripts run.sh requirements*.txt)
RUN_SCOPE diff 6ffa98d4..HEAD                 0 파일
collect-only                                  test_design_wire 31 · test_gate79_stage3_logging 15 · test_docs_lint 358
grep -rl design_wire src/                     0 파일
ls docs/22p_gap/sentinel_panel.yaml           부재
```

요청문 커밋 뒤 clean HEAD 에서 docs-lint 단독 · 전체 pytest · strict smoke 를 실행하고 그 출력은 **발송문**에 기재한다 (시작 HEAD = 끝 HEAD · 실행 중 커밋 없음).

## §5 우리가 스스로 신고하는 것

- 단계 3 은 단계 2 보다 크다: 3-A 하나만으로 `src/` ↔ `design_wire` 결속이 처음 생긴다 (지금은 시험·골든 생성기만 부른다). 계약 §13.1 의 "묶음 2 부분 — 실제 v6 격자 실행과의 end-to-end 결속 없음" 이 그 공백이다. 세 조각을 **한 라운드**에 묻는 것이 리뷰 부담을 키우면 3-A → 3-B → 3-C 로 쪼개 라운드마다 영수증을 재생성한다 (§3 규칙상 라운드마다 1회).
- `bank_index` 는 현행 코드에 정의가 없다. ~~§1.3 Q1 을 "단계 5" 로 판정하면 3-C 의 `bank_index` 는 `null` 로 남고 §9.4 다섯 필드 중 넷만 채워진다 — 그 경우 "§9.4 완료" 를 주장하지 않는다.~~ **81차 정정: Q1 포함 확정 — 미채택 문구 취소 (§1.3 Q1 의 문구와 값이 달랐다; 리뷰 §6). base/warm 은 `bank_index` 만 null, `candidate_id` 는 세 source 모두 필요.**
- `tools/preserve.py` 의 `provider` 는 retention provider 다. 3-B 의 warm provider 는 이름을 `warm_provider` 로 두어 검색·리뷰에서 섞이지 않게 한다 (계약 §2 `warm_provider_map` 과 같은 접두).
- 골든 벡터의 bank·bounds·payload sha 는 placeholder 다 (§1.1). 3-A 는 실물 sha 를 만들지만 골든은 그대로 둔다 (Q4). 실물 sha 로 만든 ID 가 골든과 다른 값인 것은 당연하며 도메인 불변의 증거는 골든 31 node 가 계속 통과하는 것이다.
- 이 요청은 서브 브랜치에서 발송한다. 본진 `9a26dd5f` 는 80차 요청 HEAD 와 같은 SHA 이고 서브는 그 ff 후손이다 — 리뷰어가 fetch 할 대상은 서브 HEAD (발송문 SHA). 본진과 서브의 RUN_SCOPE 는 같다 (실측 diff 0).
- 사용자 "승인" (2026-09-28) 은 **이 범위 확인 요청의 발송**에 대한 것이다. 구현 착수·B 실행·pilot 승인으로 읽지 않는다.

## §6 리뷰어에게 묻는 것

1. §1.2 의 세 조각(3-A 결속 · 3-B provider DAG · 3-C 행·검증)이 GATE78 §3.2 **단계 3** 과 같은가. 늘리거나 줄일 곳. 한 라운드로 묻는 것이 맞는가, 3-A/3-B/3-C 로 쪼개는가.
2. §1.3 Q1 — unit-cube bank 생성·bounds mapping digest 를 단계 3 에 넣는가 (우리: 넣는다 · legacy 경로 바이트 불변).
3. §1.3 Q2 — 혼합/손상 restart 행: 명시 거부(우리 제안) vs 부분 기록 분리.
4. §1.3 Q3 — provider 봉인 실물 세 sha 의 정의.
5. §1.3 Q4 — ID 도메인·골든 불변 정책.
6. §2 표 — provider 동결 외 항목은 단계 3 이 건드리지 않는다는 읽기가 맞는가.
7. §3 — RUN_SCOPE 4 파일 이동 · 라운드 끝 영수증 1회(격리 복원 포함) · 봉인 3종 불변 경계가 78차 §4 와 같은 뜻인가.
8. 실행 GO 아님 · 새 연구 계산 0 · 구현 착수는 회신 뒤 사용자 별도 승인 — 확인.

## §7 다음 계획 (회신이 범위를 확정하고 사용자가 착수를 승인한 뒤)

```
1  tests/test_gate81_stage3_wire.py  RED — 결속 부재 · no-warm null 분기 부재 · candidate_id/bank_index 부재 · 부분 행 통과 (현행에서 실패해야 한다)
2  3-A → 3-B → 3-C 순서로 GREEN (조각마다 fixture 감사: 처음부터 통과하는 시험은 fixture 를 의심)
3  변이 등록 (mutation_replay.py) — 최소: no-warm 에 warm 행 주입 · bank_index 음수/중복 · 부분 행을 v6 로 승격 · provider 봉인 전 consume
4  전체 회귀 python -m pytest tests/ -q --no-header -p no:cacheprovider · strict smoke ./scripts/smoke_e2e.sh · docs-lint (clean 커밋, 시작 HEAD = 끝 HEAD)
5  영수증: history/<leg>.validate.eda3feb8f4536511.yaml 보존·커밋 → clean 커밋에서 python docs/22p_gap/make_receipt.py paired_fixed5_v4 grid_fit_v5 → 필드 diff 를 원장에
6  원장 §113~ · GATE70_WORKING_STATE.md · GATE82_REQUEST.md → 발송 (SHA 는 커밋 뒤 git rev-parse HEAD)
보존: RED 실행 출력 · 변이 replay 출력 · 전체 회귀/smoke 출력 · 영수증 원본/재생성 diff · 골든 31 node 통과 출력
```

## §8 발송 규칙

70차 §6 그대로. 이 요청문과 발송문은 같은 말을 한다: **단계 3 의 제한 구현 범위와 사전 고정 사항의 확인을 요청한다. 구현 착수도 실행 GO 도 묻지 않는다.** 리뷰어 fetch: `git fetch origin claude/gate80-standby-9a26dd5f` → 발송문 SHA checkout · 본진 동결 SHA 와의 관계는 `git merge-base --is-ancestor 9a26dd5f31ca6fae45d5a55f5c59e33408371984 <발송 SHA>` 가 0 을 반환하는 것으로 확인. 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아니다.

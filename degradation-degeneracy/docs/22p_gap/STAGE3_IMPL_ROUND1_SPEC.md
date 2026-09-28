# 단계 3 한정 구현 라운드 1 — 시작 전 고정 표 (G81-N1·N2·N3 반영)

> **상태: 고정 (2026-09-28, 사용자 비준 뒤 · 코드 변경 전).** 81차 회신(원장 §114)이 요구한 "시작 전 세 표" 다. 이 표를 고정한 **뒤에** RED 시험을 쓰고, 그 뒤에만 RUN_SCOPE 를 만진다. 표와 다른 선택이 필요해지면 구현하지 않고 멈춰 회신한다 (리뷰 §7-1). 승인 범위: 원장 §114 끝 (RUN_SCOPE 4 파일 · 두 leg 영수증 1회). 실행 GO · pilot · 새 연구 leg · floor · 단계 4~6 은 이 라운드에 없다.

## §0 원칙 (리뷰 §2~§7 그대로)

| # | 원칙 | 출처 |
|---|---|---|
| P1 | 계획(planned)은 실행 **전** 봉인이며 실행 결과로 바뀌지 않는다. 실현(realized)은 **별도 record** 에 적고 `planned_id` 를 참조한다. 예상 count 를 실제 count 로 복사하지 않는다 | G81-N1 |
| P2 | 세대(legacy / v6_prep_logging / v6)는 행의 키 개수나 `candidate_mode` 이름이 아니라 **선언된(봉인된) 문맥**으로 정하고, 행 모양은 그 문맥에 **대조**한다. 정상 8 키 prep 행은 보존, v6 에서 키를 지운 행은 prep/legacy 로 내려가지 못한다 | G81-N2 |
| P3 | provider 는 fits·map·protocol 세 sha 의 소유가 아니라 **지정 row → map 좌표 → 실제 x0** 의 연결로 결속한다. warm 이 필요한 자리의 누락은 오류이지 no-warm 이 아니다 | G81-N3 |
| P4 | unit-cube bank 는 단계 3 에 포함 (Q1). 같은 봉인 **full bank** 의 prefix 를 쓴다 — B 마다 재해시하지 않는다. `exact_bounds_sha256` = 실제 ordered lb/ub 바이트, `unit_cube_bytes_sha256` = 선택한 실제 row 바이트 | 리뷰 §6 |
| P5 | ID 도메인(`pair-group/v1` · `bank/v1` · `candidate/v2`) 과 `tools/design_golden.yaml` 은 **불변** (Q4). 실물 바이트 fixture 는 시험에 따로 둔다 | 리뷰 §2 |
| P6 | legacy 경로(현행 `fit()`/`_fit_one()`/`run_fit()` 기본 인자)는 **바이트 동일** — `g79_02` 골든·smoke·1960 회귀가 지킨다. 새 경로는 **명시 인자**로만 들어간다 | 리뷰 §7-3 |
| P7 | 처음부터 GREEN 인 기존 호환/정상 대조군은 정상이다. 새 기능은 RED → GREEN. 실패 이유·assertion·도달 경로를 기록한다 | 리뷰 §7-4 |

## §1 표 A — planned ↔ realized (G81-N1)

| 자료 | schema | 생성 시점 | 서명 대상 (digest 에 들어가는 것) | 쓰는 쪽 | 검사하는 쪽 |
|---|---|---|---|---|---|
| **planned envelope v4** | `planned-leg/v4` (새 schema · `planned-leg/v3` 와 `check_envelope` 는 불변 — version branch) | 실행 **전** (사람이 계획 · `PlannedLegV4.__post_init__` 가 validator 통과 뒤 봉인) | `leg_id` · `protocol_generation` · `pairing_design_sha256` · `parameter_order_sha256` · `source_digest` · `objective_order`(순서 보존) · `stages[]` (stage ∈ {condition, p_ini} · `arm` ∈ ARM_REGISTRY · `budget_by_objective{obj: B}` · `candidate_mode` · `warm_provider_map{consumer: provider∣null}`) · `planned_counts{obj: {base_init, warm, random}}` (mode·B·provider 유무에서 **유도**한 계획값) · `bank{generator, version, length, unit_cube_bank_sha256_by_pair_group_sha256, exact_bounds_sha256}` · `inputs{reference, curves_sha256, base_config_digest}` · `provider_edges[]` (§3) · `roster{roster_sha256, n_obs, comparison_family_id, treatment_id, replicate_id}` · `min_retention_days`. **label·notes 는 밖.** | `tools/preserve.py::PlannedLegV4` | `tools/preserve.py::check_envelope_v4` (닫힌 키 · domain) · `check_planned_envelope` (schema 로 v3/v4 분기 · 모르면 거부) |
| `planned_id` | `digest(envelope_v4)` | 봉인 시 | 위 전부 | 같음 | `check_receipt` (v4 분기: `digest(env) == planned_id`) |
| **planned roster** | `planned-roster/v1` (파일 `planned_roster.json`) | 실행 **전** (조건 목록에서 유도) | 항목 = `{obs_key{comparison_family_id, pair_group_id, treatment_id, noise_level, noise_realization_id, replicate_id}, cond_id, pair_group_id}` 정렬 목록 · `roster_sha256 = digest(항목 목록)` 이 envelope 에 들어간다 | `tools/design_wire.py::build_roster` / `roster_sha256` | `tools/design_wire.py::check_roster` — obs_key 중복 · `cond_id` 중복 · obs_key 안의 `objective` 키 · 같은 obs_key 의 다른 cond_id(교차 seed) → **거부** |
| **execution record** | `execution-record/v1` (파일 `execution_record.json`) | 실행 **끝** (fit 종료 시 writer 가 1회) | `leg_id` · `planned_id`(참조) · `source_digest` · `protocol_generation` · `realized{by_objective{obj: {attempted, returned, failed, not_attempted, counts_by_source{base_init, warm, random}, random_bank_prefix_len}}, candidate_map_sha256, n_candidates, roster_observed_sha256, n_obs_observed, provider_consumed[]}` · `record_digest`(자기 내용) | `src/fitting.py::write_execution_record` (v6 경로 `run_fit` 끝) | `tools/preserve.py::check_execution_record(rec, planned_env)` — 닫힌 키 · `planned_id == digest(env)` · `source_digest` 일치 · `attempted = returned + failed` · `attempted + not_attempted = Σ planned_counts[obj]` · `counts_by_source[src] ≤ planned_counts[obj][src]` · `random_bank_prefix_len ≤ bank.length` · `n_obs_observed ≤ roster.n_obs` |
| **realized candidate map** | `candidate-map/v1` (파일 `candidate_map.json`) | 실행 중 누적 · 끝에 봉인 | 항목 = `{cond_id, objective, i, source, candidate_id, bank_index∣null, x0_sha256}` 정렬 목록 · `candidate_map_sha256 = digest(목록)` | `src/fitting.py` (v6 `_fit_one` 이 행마다 만들고 `run_fit` 이 모은다) | `check_execution_record` (sha 대조 · 같은 (cond, objective) 안 `bank_index` 중복 없음 · random 의 index 범위) · `validate_provenance` v6 (`restarts_json` 의 candidate_id 집합 = map 의 집합) |
| **execution receipt** (기존) | `execution-receipt/v1` 불변 | 보존 트랜잭션 | 기존 그대로 + `planned_envelope` 가 v4 이면 `check_planned_envelope` 로 분기 | 기존 | 기존 + 분기 |

**혼입 규칙:** `run_transaction` 1 단계는 v4 계획이면 `run_spec.json` 의 `planned_id` 외에 `execution_record.json` 을 **요구**하고 `check_execution_record` 를 통과해야 봉인한다 (다른 계획의 record → `planned_seal` 오류). v3 계획은 기존 경로 그대로.

**하지 않는 것:** Δ/누락 bound/scoring 계산 · 전역 claim 세대표 등록 · `planned-leg/v3` 필드 추가 · 기존 receipt/영수증 재작성.

## §2 표 B — 세대 dispatch (G81-N2)

선언 문맥은 두 곳에서 온다: (i) 실행 산출의 `run_spec.sig_version` (5 = legacy/prep 세대 · **6 = v6**) + `run_spec.stage3` 블록 · (ii) reader 호출자가 넘기는 `declared` 인자. 행 모양으로 세대를 **추론하지 않는다**.

| 선언된 문맥 | 받는 행 모양 (정확히) | reader `normalize_restart_record(r, declared=…)` 결과 | validator (`src/io.py`) 판정 |
|---|---|---|---|
| 없음 (`declared=None`, 역사적 reader — 기존 호출 그대로) | 2-튜플 `[p, J]` → `legacy_pair` · 키 ⊆ {p,J,i,source,warm} (p·J 필수) → `legacy_dict` · 정확히 8 키 → `v6_prep_logging` · **정확히 10 키 → `v6_undeclared`** (값은 보여 주되 v6 로 승인하지 않음) · 그 밖 → `mixed_invalid` | 값은 있는 것만, 없는 것은 None(미기록). `g79_06` 의 세 결과 불변 | 역사적 validator(sig 5) 는 기존 `_restart_ok` (p·J·i·source) 그대로 — 넓히지 않는다 |
| `declared="legacy"` | 2-튜플 또는 5 키 이하 dict | `legacy_pair`/`legacy_dict` · 8/10 키 행 → `mixed_invalid` (선언-행 충돌) | sig 5 기존 규칙 |
| `declared="v6_prep_logging"` | 정확히 8 키 (p·J·i·source·warm·converged·n_eval·termination_status) | `v6_prep_logging` — 로깅 3 값 보존 · `candidate_id`/`bank_index` 는 **미기록(None) 이 정상**, v6 완료 아님 · 10 키/5 키 행 → `mixed_invalid` | sig 5 기존 규칙 (prep 은 sig 5 산출이다) |
| **`declared="v6"`** (sig_version 6 + `stage3` 블록) | 정확히 **10 키** = 8 + `candidate_id`(hex64) + `bank_index`(int≥0 ∣ null) — 타입·유한성 검사 | `v6` · 키 하나라도 없으면 `mixed_invalid` — prep/legacy 로 **내려가지 않는다** | `_restart_ok_v6` : 10 키 정확 · 타입 · `source ∈ {base_init, warm, random}` · random 은 `bank_index` int ≥ 0, base_init/warm 은 null · 행 전체 통과해야 `restart_후보` PASS. `sig_version 6` 이면 `stage3` 필수 키(§4 표) 없을 때 실패 (v6 writer 필수축) |
| 선언 없음/모순/혼합 손상 | — | `v6_undeclared` / `mixed_invalid` | **거부/미완** — diagnostic reader 가 값을 보여 줘도 승인 아님 |

- `candidate_mode` 이름은 세대 선택자가 아니다 — `legacy_slot_replace` 는 legacy 산출에도 v6 계획에도 있다. 세대는 위 문맥만 정한다.
- `converged` 의 뜻은 80차 그대로 (그 restart 의 마지막 **유한** round 의 legacy ok; True 여도 `termination_status.outer == "nonfinite"` 일 수 있다). v6 검사는 기록 정합성(키·타입)과 solver 건전성 실패를 구분하며, status 를 고쳐 통과시키지 않는다. 첫 비유한 round 의 `native_best=None` 은 정상 실패 표현으로 보존.
- 현행 `source_digest` 가 `CLAIM_STATUS.yaml` 세대표에 없다는 사실로 v6 를 추론하거나 옛 기록을 새 세대로 등록하지 않는다.

## §3 표 C — provider edge · 좌표 결속 (G81-N3)

| 층 | 고정하는 것 | 거부하는 것 |
|---|---|---|
| **edge 선언** (planned envelope `provider_edges[]`) | `{stage, arm, consumer_objective, provider_objective, provider_artifact_sha256, solution_map_sha256, provider_protocol_sha256}` · `warm_provider_map` 과 1:1 · provider 는 `objective_order` 에서 consumer **앞**에 있어야 함 | self provider · 순환 · order 밖 objective · `warm_provider_map` 과 어긋나는 edge · `condition_warm_start=False` arm 에 edge 가 있는 것 |
| **no-provider 분기** | `warm_provider_map[obj] is None` 은 (a) `objective_order[0]` 이거나 (b) arm 의 `condition_warm_start=False` 일 때만 허용 → 후보 = `[base_init] + bank[:B−1]` (B ≥ 1) · 행 `warm=False` · warm 후보 0 (회귀로 고정) · 관련 sha 참조는 명시 null | warm 이 필요한 자리(order 2 번째 이후 · warm arm)에서 map 누락/빈 dict/잘못된 objective → **오류** (no-warm 으로 전환 금지) |
| **map 생성** (`src/fitting.py::make_solution_map`) | 입력 = provider leg 의 봉인 `fits.parquet` 바이트 + `provider_objective` + `provider_protocol_sha256`(= `canonical_bytes(provider run_spec)` 의 sha256 — preserve 의 canonicalizer) · header `{schema: solution-map/v1, provider_objective, provider_artifact_sha256(=fits 바이트 sha), provider_protocol_sha256, parameter_order, n_entries, excluded_cond_ids}` · entries `{cond_id: {p: [repr(float)…]}}` — objective 별 **한 파일** (p_ini map 과 condition map 을 한 세트로 덮지 않음) | 같은 cond_id 행 중복 · 비유한 p (→ `excluded_cond_ids` 로 분리, entries 에 넣지 않음) · parameter_order 길이 불일치 |
| **map 소비** (`src/fitting.py::provider_x0`) | 파일 바이트 sha == edge 의 `solution_map_sha256` · header 의 `provider_objective`·`provider_artifact_sha256`·`provider_protocol_sha256`·`parameter_order` == edge/design 값 · `entries[cond_id]` 존재 · p 유한 · 길이 = parameter_order · **lb ≤ p ≤ ub** → x0 = p (변환 없음) · `x0_sha256 = sha256(x0 float64 LE bytes)` | 봉인 전 소비(sha 불일치) · 다른 fits/map 결합(header sha ≠ edge) · 조건/objective 교차(다른 cond_id 의 p 사용 불가 — cond_id 로만 조회) · 누락 cond_id · bounds 밖 p (**거부, clip 하지 않음**; legacy 의 `np.clip` 은 legacy 경로에만) |
| **x0 결속** | warm 후보의 `candidate_id(source="warm", payload={provider_objective, provider_artifact_sha256, solution_map_sha256})` 와 실제 solver 입력 `x0_sha256` 을 candidate map 항목에 **함께** 기록 · base_init 의 x0 = init (bounds 밖이면 거부) · random 의 x0 = `lb + u·(ub−lb)` | map 좌표와 실제 x0 불일치(다른 좌표 전달) → 시험 fixture 로 거부 |
| **p_ini stage** (half-cell arm B/D) | edge schema 에 `stage="p_ini"` 를 **선언만** 한다 (`p_ini_values_sha256` 은 half-cell 원점 값 결속 · grid 는 null) | **이번 라운드는 `stage="p_ini"` edge 를 명시 거부**한다 (미구현 mode 는 legacy 로 조용히 대체하지 않는다). 구현은 다음 라운드 |
| **retention provider** (`tools/preserve.py` 의 보존 backend) | 이름 `warm_provider*` 접두로 분리 | 섞지 않음 |

## §4 bank · 후보 구성 (Q1 좁은 기준)

| 항목 | 고정값 |
|---|---|
| 생성 | `tools/design_wire.py::unit_cube_bank(pair_group_id, bank_version, length, n_params)` — seed = `int(sha256(H(pair_group_id, bank_version)))[:16], 16)`, `numpy.random.Generator(PCG64(seed))`, `uniform(0,1)` shape `(length, n_params)`, dtype float64 · 조건별 `cond_id` seed 를 공유 bank 에 쓰지 않는다 |
| 바이트·식별 | `bank_bytes = arr.astype('<f8', order='C').tobytes()` · `unit_cube_bank_sha256 = sha256(bank_bytes)` (**full bank**) · `unit_cube_bytes_sha256(row) = sha256(row.astype('<f8').tobytes())` · `bank_id = H(pair_group_id, bank_version, unit_cube_bank_sha256)` (기존 함수 그대로) |
| prefix | 계획 `budget_by_objective[obj] = B` → random prefix 길이 = `candidate_plan(mode, B, has_provider)` 의 random 수 · `bank.length ≥ max prefix` 아니면 계획 거부 · full-bank identity ≠ consumed prefix 길이 (execution record 의 `random_bank_prefix_len`) · 길이/버전 변경 = 새 bank identity |
| bounds | `exact_bounds_sha256(lb, ub) = sha256(b"exact-bounds/v1" + lb('<f8') + ub('<f8'))` — 실제 ordered 값 |
| mapping | `x0 = lb + u·(ub−lb)` (float64) · `x0_sha256` 기록 |
| 후보 배열 (`candidate_plan`) | no-provider: `[base_init] + random×(B−1)` (B ≥ 1) · `legacy_slot_replace`+provider: `[warm] + random×(B−1)` (B ≥ 1) · `equal_start_count_base_retained`+provider: `[base_init, warm] + random×(B−2)` (**B ≥ 2**, 아니면 거부) · `union`+provider: `[base_init, warm] + random×(B−1)` (총 B+1 — 계약 §3) · 그 밖 mode → 거부 |
| index 규칙 | random `bank_index = 0..prefix−1` 순서대로 · 같은 (cond, objective) 안 중복 없음 · 다른 objective/조건에서 같은 index 재사용은 정상 · J 정렬 순서를 index 로 삼지 않음 (`i` 는 후보 순번, `bank_index` 는 bank 행) · base_init/warm 은 `bank_index=null`, `candidate_id` 는 세 source 모두 필수 |
| adaptive | 새 경로는 `adaptive=False` 만 (계약 v6 arm) · `candidates` 와 `adaptive=True` 동시 → 거부 (§2.2 의 diagnostic adaptive arm 은 이번 라운드 밖) |
| 골든 | `tools/design_golden.yaml` 불변 · placeholder sha 그대로 · 실제 바이트 positive/negative fixture 는 `tests/test_gate81_stage3_wire.py` |

## §5 v6 writer 필수축 (`run_spec.sig_version = 6`)

`src/fitting.py::run_fit(..., stage3=<sealed context>)` 가 만든 산출만 v6 다. `stage3` 없음 = legacy 경로 (sig 5, 바이트 동일). v6 `run_spec` 에 **필수**: 기존 sig-5 키 전부 + `stage3{planned_id, pairing_design_sha256, parameter_order_sha256, bank_version, exact_bounds_sha256, candidate_mode, budget_by_objective, warm_provider_map, provider_edges_sha256, roster_sha256, arm, stage}` · `optimizer.adaptive == False` · `optimizer.seed_scheme == "unit_cube_bank/v1"`. `validate_provenance` 는 `sig_version` 으로 분기: 5 → 기존 검사 불변 · 6 → 기존 검사 + `stage3` 필수 키 + `restart_후보`(§2) + `execution_record.json` 존재·`check_execution_record` + `candidate_map.json` sha 일치. 5 도 6 도 아니면 실패.

## §6 현행 코드 좌표 (HEAD `15d71c31` · RUN_SCOPE `6ffa98d4` = digest `eda3feb8f4536511`)

| 파일 | 위치 | 이번 라운드 |
|---|---|---|
| `src/fitting.py` | `FitResult` :156 · `fit()` :241–334 (`init=np.clip` :262 · `rng.uniform(lb,ub)` :269 · 라벨 :274 · J 정렬 :306 · serializer :330–331) · `_RESTART_NEW_KEYS` :337 · `normalize_restart_record` :340–359 · `_fit_one` :401–518 (`seed_p` handoff :457–475 · 행 :491–518) · `_assert_fit_authorized` :941 · `run_fit` :984 (task 구성 :1433–1447 · run_spec :1535–1590 · manifest :1701) | `fit(candidates=None)` 새 인자(legacy 분기 불변) · `normalize_restart_record(r, declared=None)` · `_fit_one` 의 `task["stage3"]` 분기 · `run_fit(stage3=None)` · `make_solution_map` · `provider_x0` · `write_execution_record` |
| `src/io.py` | `_RESTART_SOURCES` · `_restart_ok` :789–808 · `validate_provenance` :1484 (필수 키 :1557–1577 · `sig_version == 5` :1575 · `restart_출처` :1853–1875) | `_restart_ok_v6` · sig 5/6 분기 · v6 검사 블록 |
| `tools/design_wire.py` | `CANDIDATE_PAYLOAD_SCHEMA` :71–79 · `check_candidate_payload` :116 · `coords_from_condition` :171 · `canonical_design_spec` :219 · `pair_group_id` :419 · `bank_id` :449 · `design_binding` :461 · `candidate_id` :500 | `unit_cube_bank` · `bank_bytes`/`unit_cube_bank_sha256`/`unit_cube_bytes_sha256` · `exact_bounds_sha256` · `map_unit_to_bounds` · `x0_sha256` · `candidate_plan` · `obs_key`/`build_roster`/`roster_sha256`/`check_roster` · `check_provider_edges` |
| `tools/preserve.py` | `PlannedLeg` :2327–2379 (`planned-leg/v3`) · `seal_payload` :2386 · `_ENVELOPE_KEYS` :2987 · `check_envelope` :3050–3087 · `check_receipt` :3096 (envelope 검사 :3120) · `run_transaction` :3357–3431 (run_spec 요구 :3379) · `candidate_modes()` :3010 | `PlannedLegV4` · `_ENVELOPE_KEYS_V4` · `check_envelope_v4` · `check_planned_envelope` (v3/v4 분기) · `check_execution_record` · `run_transaction` v4 분기 · `check_receipt` 분기 |

## §7 시험 계획 (`tests/test_gate81_stage3_wire.py`)

| 군 | RED (현행에서 실패해야) | 처음부터 GREEN 허용 (대조군) |
|---|---|---|
| N1 | `PlannedLegV4` 존재·닫힌 키·`planned_id` 가 실현값과 무관 · `check_execution_record` 가 다른 `planned_id`/count 불일치/planned 복사 를 거부 · `check_roster` 가 중복 obs_key·cond_id 충돌·교차 seed 를 거부 · `run_transaction` v4 가 record 없는 run_dir 을 거부 | v3 `PlannedLeg`/`check_envelope`/`run_transaction` 기존 시험 전부 |
| N2 | `normalize_restart_record(row10, declared="v6")`→`v6` · v6 에서 키 지운 8 키 행 + `declared="v6"` → `mixed_invalid` · 10 키 행 + `declared=None` → `v6_undeclared` · `_restart_ok_v6` 가 8 키 거부 · `validate_provenance` sig 6 이 stage3 키 없으면 실패 · sig 7 거부 | `g79_06` (prep 8 키 보존) · `g79_07` · `g79_02` 골든 |
| N3 | wrong fits/map 결합 거부 · 조건/objective 교차 거부 · 누락 cond_id 오류(no-warm 전환 아님) · bounds 밖 p 거부 · 봉인 전 소비 거부 · self/순환 provider 거부 · x0_sha256 == map 좌표 sha | 정상 봉인 공급 양성 |
| bank | 결정성(같은 pair_group·version → 같은 바이트) · full-bank sha 가 prefix 와 무관 · `exact_bounds_sha256` 실제 값 · random `candidate_id` 가 실제 row 바이트 사용 · index 범위/중복 · base/warm index null · `candidate_plan` 5 mode 분기 · adaptive+candidates 거부 · p_ini stage 거부 | `test_design_wire.py` 31 (골든 불변) |
| writer | `fit(candidates=…)` 행 10 키 · `_fit_one(stage3)` 행에 `pair_group_id`/`bank_id` · `run_fit(stage3)` 가 sig 6 + execution_record + candidate_map 을 쓰고 `validate_provenance` 통과 | legacy `run_fit` (smoke) |

변이 (등록 `docs/22p_gap/mutation_replay.py`): ① realized count 를 planned 에 복사 ② v6 10 키 행을 8 키 prep 으로 내림 ③ warm-required 누락을 no-warm 으로 전환 ④ `bank_index` 음수/중복 허용 ⑤ map 좌표 대신 clip 한 x0 전달 ⑥ 봉인 전 map 소비 허용 ⑦ prefix 재해시(B 마다 bank sha 변경).

## §8 이번 라운드에 없는 것 (명시)

실제 v6 연구 leg · provider 운영 canary · floor 측정 · B 채택/plateau/pilot · 단계 4(구 필드 제거·claim 세대 게시)~6 · `stage="p_ini"` edge 구현(선언만) · adaptive diagnostic arm · `row_projection.py`·골든·과거 fits/영수증 변경 · 본진 ff 복귀(별도) · COMSOL.

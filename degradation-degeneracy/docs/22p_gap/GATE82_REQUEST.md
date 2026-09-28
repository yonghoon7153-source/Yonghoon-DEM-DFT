# 82차 게이트 리뷰 요청 — 단계 3 **라운드 1 구현 결과 + 발송 전 자체 점검 보강** (G81-N1·N2·N3 반영 · 실행 GO 아님 · 본진 복귀 아님)

> 이 문서는 리뷰 요청문이다. 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요. 리뷰어는 exact HEAD 를 fetch 해 재실행·검증한다.

대상 커밋: `c82231c49460f79bb5474185648594b3a6c9fc02` (판정 대상 HEAD = 전체 검증을 돌린 clean 커밋 · RUN_SCOPE 마지막 변경 `f3de7e02` · 영수증 `9b52eb2a` · 변이 EXPECT `2d2f5d8b` + 증인 정정 `d76b3eda` 포함)

## 판정 대상

| 항목 | 값 |
|---|---|
| 브랜치 | **`claude/gate80-standby-9a26dd5f`** (임시 대피 서브). 본진 `claude/14-gate-code-review-9qkx05` 는 `9a26dd5f31ca6fae45d5a55f5c59e33408371984` 에서 **동결 그대로** (이번 라운드 커밋 0). `git merge-base --is-ancestor origin/<본진> origin/<서브>` → `FF_OK` (2026-09-28, `c82231c4` push 뒤 실측) |
| **코드 (판정 대상 HEAD)** | **`c82231c49460f79bb5474185648594b3a6c9fc02`** — RUN_SCOPE 를 바꾼 커밋은 둘: `20ab9655dd647272cdeb10b9af1cb6b1678768da` (라운드 1) → **`f3de7e02137a04733e503c18c8209d3066926b55`** (자체 점검 보강). `source_digest` **`eda3feb8f4536511 → eea5977f4faf9685 (20ab9655) → 02a776a7a0a3f4ba (f3de7e02)`** (`python -c "from src.io import source_digest; print(source_digest())"` → `02a776a7a0a3f4ba`, `c82231c4` 에서 실측). 그 뒤 커밋(영수증 이력 `23670e58` · 영수증 `9b52eb2a` · 변이 EXPECT `2d2f5d8b` · 위키 62호 `a3f65366` · bms `9d5d8d1c` · 증인 정정 `d76b3eda` · 위키 63호 `aa8e8a59` · bms `34e8b95f` · 도착 목록 `c82231c4`)은 RUN_SCOPE 밖 |
| 사용자 승인 | 원장 §114 끝 "비준" (2026-09-28, `15d71c31`) — `gate81_review/codex/NEXT_APPROVAL_SCOPE_DRAFT.md` 의 7 항 그대로. **자체 점검 보강과 영수증 2회째는 사용자 결정** (2026-09-28 "지금 고치고 영수증 한 번 더", 원장 §115) — 리뷰 §7-6 에서 벗어난 점은 §8-f |
| 시작 전 고정 표 | `docs/22p_gap/STAGE3_IMPL_ROUND1_SPEC.md` §1~§8 (`90a1f419`, 코드 변경 전) — 표 A(planned↔realized) · 표 B(세대 dispatch) · 표 C(provider edge·좌표 결속) · §4 bank · §5 v6 writer 축 · §7 시험 계획. **§9 보강 표** (자체 점검 F1~F12, `f3de7e02` 에서 추가 기록 — §1~§8 문장 불변) |
| RED 증거 | 라운드 1 `6473d1fb` — 34 node, 패치 전 **32 failed / 2 passed** (대조군 `n2_00` · `w03`) · 자체 점검 `315f5028` — 44 node, 패치 전 **14 failed / 30 passed** (무관 예외와 실제 이유를 §5 에서 분리) |
| GREEN | `20ab9655` — `test_gate81_stage3_wire.py` **35 node** + `test_gate79_stage3_logging.py` 15 = 50 passed · `f3de7e02` — **44 node** + 15 = **59 passed** (노드 수는 각 커밋 트리 `pytest --collect-only` 실측) |
| 영수증 | 원본 보존 `5d659d06` (`history/<leg>.validate.eda3feb8f4536511.yaml`) → 1차 재생성 `03f907cc` (clean `20ab9655`) → 1차 보존 `23670e58` (`history/<leg>.validate.eea5977f4faf9685.yaml`) → **2차 재생성 `9b52eb2a`** (clean `23670e58`, 원장 `LEG_PRESERVATION.yaml` 앵커를 같은 커밋에) — §7 |
| 변이 | `-g81` 7 (라운드 1) + `-g81s` 13 (자체 점검) = **20** — `-k g81` 재생 **20/20** (clean `c82231c4`, 증인 정정 뒤) · 첫 재생 20/20 (clean `2d2f5d8b`) |
| 요청문 커밋 · 발송 SHA | 발송문에 실측 기재 |
| 심사 대상 문서 | 이 문서 §1~§9 · `STAGE3_IMPL_ROUND1_SPEC.md` (§9 포함) · `tests/test_gate81_stage3_wire.py` · `docs/22p_gap/mutation_replay.py` 의 `*-g81` · `*-g81s` 20 변이 + EXPECT · 원장 `docs/08_REVIEW_RESPONSE.md` §114(81차 접수) · §115(이 라운드 기록) |
| 81차 패키지 원본 | `docs/22p_gap/gate81_review/` (zip `e9def6bc…83ea` 473,844 B · `codex/` 34 · MANIFEST `b516ee80…` · `-text` 규칙 `58980d60` 먼저) |

## §0 이 요청이 묻는 것 / 묻지 않는 것

| 묻는 것 | 묻지 않는 것 |
|---|---|
| §1 표가 G81-N1·N2·N3 를 **코드로** 닫았는가 — 반례가 지금 어떤 검사에 걸리는가 | 실행 GO · 새 연구 leg · floor · pilot · 단계 4~6 · 12-P canary |
| §1b 자체 점검 보강(F1~F12)이 81차 닫힘 조건(REVIEW_KO §3~§7)을 우리가 읽은 대로 좁혔는가 | 본진 ff 복귀 (별도 승인) · class/투영 게시 · `row_projection.py` 봉인 |
| §2 최소 diff 가 승인 범위(4 파일) 안인가 · legacy/prep 경로가 바이트 그대로인가 | 단계 3 라운드 2 (실물 v6 leg gate 배선 · LEG_SPEC 키 · 세대표 등록) 의 착수 — §9 에 제안만 |
| §3 schema/필드 시점 표 · §4 결속 증거 · §5 시험/변이 · §7 영수증 diff 의 수용 · §8 자기 신고 판정 (특히 영수증 2회째 §8-f · 순서 §8-h · 두 번의 첫 전체 회귀 red §8-g · §8-m) | — |

## §1 G81-N1·N2·N3 반영 표 (발견 → 코드 자리 → 시험 → 변이)

줄번호는 판정 대상 HEAD `c82231c4` 실측 (`f3de7e02` 와 RUN_SCOPE 동일).

| 발견 | 요구 (81차 회신) | 코드 자리 | 시험 node (`tests/test_gate81_stage3_wire.py`) | 변이 (`mutation_replay.py`) |
|---|---|---|---|---|
| **G81-N1** 계획과 실현값 분리 | planned 는 유도값·불변, realized 는 별도 record 가 planned_id 로 참조; 실현 count 는 계획 아래 | `tools/preserve.py` `PlannedLegV4` :2383 (`planned-leg/v4`, 실현 키 없음 · `planned_id()` = envelope digest) · `_ENVELOPE_KEYS_V4` :3049 · `check_envelope_v4` :3166 (planned_counts == `DW.planned_counts(mode,B,provider)` 아니면 거부 · stage 는 `condition` 하나 · bank.length ≥ 최대 random · edge → `check_provider_edges`) · `check_planned_envelope` :3267 (v3/v4 분기, 모르는 schema 거부) · `check_execution_record` :3279 (`execution-record/v1`: leg_id · planned_id · source_digest · protocol_generation 대조 · attempted = returned + failed · attempted + not_attempted = 조건당 계획 × roster n_obs · source 별 ≤ 계획 × n_obs · prefix ≤ 계획 random ≤ bank.length · 실현 random ≤ prefix × n_obs · roster/n_obs 관측 대조 · 닫힌 키 · **provider_consumed 계획 edge 대조** :3356–3379 — §1b F4) · `run_transaction` v4 분기 :3691–3704 (record 없음 → `planned_seal` · 다른 계획 record → `planned_seal`) · `check_receipt` :3389 (두 키 집합) · `src/fitting.py` `write_execution_record` :1394 (`candidate_map.json` + `execution_record.json`, 실현값은 `src.io.realized_from_fits` — §1b F3) | n1_01 · n1_02 · n1_03 · n1_04 · n1_05 · n1_06 · b07 · w04 · s03 · s04 | `record-must-reference-this-plan-g81` (n1_03+n1_05) · `planned-counts-are-derived-not-copied-g81` (n1_06) · `validator-recounts-realized-counts-g81s` (s03) · `provider-consumed-must-be-a-planned-edge-g81s` · `a-used-edge-must-be-recorded-g81s` (s04) |
| **G81-N2** 세대 구분 (키 개수 추론 금지 · v6 필수 필드 누락이 legacy fallback 으로 통과 금지) | 선언된 문맥으로 dispatch; ID 지운 v6 행은 prep 으로 안 내려감; validator 가 sig 별 분기 | `src/fitting.py` `_row_shape` :383 · `_read_row` :399 · `normalize_restart_record(r, declared=None)` :413 (선언 없음 → 역사적 3 세대 그대로 · 10 키 행은 `v6_undeclared` · `declared="v6"` 는 10 키만 `v6`, 8 키는 `mixed_invalid` · `declared="v6_prep_logging"` 아래 10 키는 충돌) · `_V6_ROW_KEYS` :377 · run_spec `sig_version` 6/5 :1992 · `seed_scheme` :2004 · `stage3` 블록 :2008 · 행 `record_generation: "v6"` :813 · `src/io.py` `_RESTART_V6_KEYS` :812 · `_restart_ok_v6` :822 (10 키 · random 만 bank_index int ≥ 0 · 나머지 None) · `checks["sig_version"] ∈ {5,6}` :1902 · `_STAGE3_SPEC_KEYS` :1521 (14 키) · `_stage3_checks` :1709 (`stage3_schema` · `stage3_optimizer` · `stage3_planned_envelope` · `execution_record` · `candidate_map` · `candidate_ids_결속` · `후보_재유도` · `restart_예산_완주` · `실현_재계산`) · `restart_후보`(sig 6) / `restart_출처`(sig 5) :2221 · **`세대_선언_일치`** :2252 (§1b F1) | n2_00(대조군) · n2_01 · n2_02 · n2_03 · n2_04 · n2_05 · w01 · w04 · w05 · s01 · s09 | `stripped-v6-row-is-not-downgraded-to-prep-g81` (n2_02) · `v6-random-row-needs-a-bank-index-g81` (n2_05) · `sig5-v6-row-keys-are-a-declaration-conflict-g81s` (s01) · `v6-budget-is-checked-per-objective-g81s` (s09) |
| **G81-N3** provider 결속 (no-provider ↔ 봉인 warm-provider 분리 · 좌표 결속) | edge 가 fits sha·map sha·protocol·objective 를 봉인; 소비자는 봉인 전·다른 map·cond 부재·bounds 밖을 거부 (no-warm 전환·clip 금지) | `src/fitting.py` `make_solution_map(provider_run_dir, provider_objective, out_path)` :523 (`solution-map/v1` header = provider_objective · provider_artifact_sha256(fits 바이트) · provider_protocol_sha256(**manifest run_spec 의 canonical_bytes sha 를 여기서 잰다** :546) · parameter_order(= `PARAM_NAMES` :547) · excluded_cond_ids) · `provider_x0` :576 (파일 바이트 sha ≠ edge → 거부 · header ≠ edge → 거부 · cond_id 부재 → 오류 · 길이/유한성 · bounds 밖 → clip 없이 거부 · 반환 `(x0, x0_sha256)`) · `_stage3_candidates` :614 (warm 은 `provider_x0` 로만; legacy `seed_p` in-process 물려주기는 v6 분기 :749–757 에서 안 씀) · `_prepare_stage3` :1286 (문맥 `{planned, design, provider_runs}` :1292 · warm 필요 자리의 provider run 없음 → 거부 :1358 · **provider run 에서 다시 만든 map sha ≠ 계획 edge → 시작 거부** :1363 · 사본 `out_dir/_inputs/provider_maps/<consumer>.solution_map.json` :1352) · `tools/design_wire.py` `PROVIDER_EDGE_KEYS` :553 · `check_provider_edges` :790 (self · 순환 · order 역방향 · warm map 불일치 · warm-off arm 의 edge · **warm arm 두 번째 objective null → 오류**) | n3_01 · n3_02 · n3_03 · n3_04 · w06 · s05 · s06 · s08 | `warm-required-slot-is-not-turned-into-no-warm-g81` (n3_04) · `provider-x0-is-not-clipped-g81` (n3_03) · `solution-map-is-consumed-only-when-sealed-g81` (n3_02) · `map-protocol-is-measured-from-the-run-spec-g81s` (s05 · n3_01 · n3_02 · n3_03) · `warm-map-is-regenerated-and-compared-g81s` (s06) · `design-order-is-the-optimizer-vector-g81s` (s08) |
| **Q1** unit-cube bank (좁은 기준 수용) | bank 는 pair_group·version 의 함수 · full-bank 봉인 · prefix 소비 · 실제 bounds 로 사상 · 실물 row 바이트로 candidate_id | `tools/design_wire.py` `pair_group_id` :422 · `bank_id` :452 · `candidate_id` :503 · `_bank_seed` :563 (`H("bank-seed/v1", pair_group_id, bank_version)`) · `unit_cube_bank` :578 (PCG64 · [0,1)) · `unit_cube_bank_sha256` :601 (full bank, B 무관) · `unit_cube_bytes_sha256` :606 · `exact_bounds_sha256` :624 (`sha256(b"exact-bounds/v1"+lb+ub)`) · `map_unit_to_bounds` :630 (`lb + u·(ub−lb)`, u ∈ [0,1]) · `x0_sha256` :641 · `candidate_plan` :649 (계약 §3 다섯 배열 · random index 0..) · `planned_counts` :680 · `src/fitting.py` `fit(candidates=…)` :246 → `_fit_candidates` :449 (adaptive False 만 · x0 bounds 안 · bank_index 유일 · 10 키 행 · `FitResult.candidate_map`) · **validator 재유도** `src/io.py` `_stage3_rederive` :1569 (§1b F2) | b01 · b02 · b03 · b04 · b05 · b06 · b07 · w01 · w02 · w03(대조군) · s02 | `full-bank-identity-is-not-a-prefix-g81s` (w04) · `duplicate-bank-index-is-refused-g81s` (w02) · `validator-rederives-every-x0-g81s` (s02 · s06) · `validator-rederives-every-candidate-id-g81s` · `validator-rederives-the-candidate-plan-g81s` (s02) |
| roster (79차 합의) | 계획 roster = 조건 집합의 사전 크기 · obs_key 충돌/중복 거부 · 실제 조건 집합과 다르면 시작 거부 | `tools/design_wire.py` `OBS_KEY_FIELDS` :551 · `obs_key` :693 · `check_roster` :728 · `roster_sha256` :758 · `roster_from_conditions` :766 · `src/fitting.py` `_prepare_stage3` :1286 (실제 roster ≠ 계획 → `RuntimeError` :1344) | n1_04 · w06 · s07(대조군) | — |

## §1b 발송 전 자체 점검 보강 (F1~F12 · 고정 표 §9 · RED `315f5028` → GREEN `f3de7e02`)

라운드 1 구현(`20ab9655`)을 81차 회신 닫힘 조건(REVIEW_KO §3~§7)에 하나씩 대조했다. 반례는 트리를 고치기 전에 트리 밖에서 먼저 실측했다 (`scratchpad/selfreview82/repro.py` — 요청 패키지에 동봉하지 않음, 결과는 아래 "반례" 열과 §5 탐침 줄). 같은 4 파일 중 3 파일(`src/io.py` · `src/fitting.py` · `tools/preserve.py`)만 바뀌었다 — `tools/design_wire.py` 불변, 새 production/helper 파일 0.

| # | 81차 닫힘 조건 | 구멍 (반례) | 보강 (HEAD `c82231c4` 줄) | 시험 | 변이 (`-g81s`) |
|---|---|---|---|---|---|
| F1 | §4 "행 모양은 선언된 문맥에 대조" | sig 5 validator 가 v6 전용 행 키(`candidate_id`·`bank_index`) · `run_spec.stage3` 블록 · v6 표식 열을 거부하지 않는다 (`_restart_ok(10 키 행)` → True) | `src/io.py` `_V6_ONLY_ROW_KEYS` :817 · `_V6_FITS_COLS` :818 · `validate_provenance` :1807 의 `세대_선언_일치` :2252 — sig 5: 셋 다 거부 / sig 6: v6 열 필수 · `record_generation == "v6"`. 옛 `_restart_ok` :789 는 그대로 (넓히지 않는다) | s01 | `sig5-v6-row-keys-are-a-declaration-conflict-g81s` |
| F2 | §6 "64hex 존재만으로 통과 금지" · §5 좌표 결속 | sig 6 validator 는 후보 ID **집합** 동일성만 봤다 — 가짜 ID · 가짜 x0 digest 로 만든 자기일관 산출이 `_stage3_checks` 6 검사 전부 통과 | `src/io.py` `_stage3_rederive` :1569 → `후보_재유도` :1784: run_spec.stage3.`pairing_design`(새 필수 키 · digest 대조) · run_spec.bounds(exact_bounds 대조) · 행 truth 좌표 → pair_group_id → 봉인 bank → bank_id · `candidate_plan` 구성(계획 순서) · base(bounds.init) / random(`lb+u·(ub−lb)`) / warm(`_inputs/provider_maps` 사본) x0 digest · candidate_id · restart 행 ↔ map entry | s02 · s06 | `validator-rederives-every-x0-g81s` (s02·s06) · `validator-rederives-every-candidate-id-g81s` · `validator-rederives-the-candidate-plan-g81s` (s02) |
| F3 | §3 "실현 count 는 계획 아래 · 별도 record" | 계획 범위 **안**의 조작 count 가 통과 (계획만 보는 검사는 정의상 못 잡는다) | `src/io.py` `realized_from_fits` :1528 → `실현_재계산` :1803 (by_objective · n_obs_observed · provider_consumed · n_candidates · roster_observed 를 행에서 다시 센 값과 대조). writer `write_execution_record` :1394 도 **같은 함수**를 쓴다 (정의 하나) | s03 | `validator-recounts-realized-counts-g81s` |
| F4 | §5 공급 기록 | `check_execution_record` 가 `provider_consumed` 를 "목록인가" 만 봤다 — 없는 objective · `n_conditions` 999 가 `[]` (통과) | `tools/preserve.py` `check_execution_record` :3279 (provider_consumed :3356–3379 — 닫힌 키 · 계획 edge 쌍 · 중복 없음 · 1 ≤ n ≤ roster n_obs · 시도한 계획 edge 는 반드시 기록) | s04 | `provider-consumed-must-be-a-planned-edge-g81s` · `a-used-edge-must-be-recorded-g81s` |
| F5 | §5 N3-5 protocol sha | `make_solution_map` 이 protocol sha 를 **인자로** 받아 그대로 봉인 (`"0"*64` 가 header 에 그대로) | `src/fitting.py` `make_solution_map(provider_run_dir, provider_objective, out_path)` :523 — fits 바이트 sha 와 `manifest.yaml` run_spec 의 `canonical_bytes` sha 를 **여기서** 잰다 :546 · 해시한 그 바이트에서 parquet 을 읽는다 :548 · 인자 폐지 (주면 `TypeError`) | s05 · n3_01 · n3_02 · n3_03 | `map-protocol-is-measured-from-the-run-spec-g81s` |
| F6 | §5 닫힘 조건 (정상 공급 · x0 불일치) | warm 공급 경로 전체를 실행하는 시험 0 (`_stage3_candidates` warm 가지 · 비지 않은 provider 문맥의 `run_fit` 호출 0 — 한 번도 안 돈 production 코드) | `src/fitting.py` `_prepare_stage3` :1286 — 문맥 키 `provider_maps` → `provider_runs` :1292 · provider run 없음 → 거부 :1358 · provider **run** 에서 map 을 다시 만들어 계획 edge sha 와 대조, 다르면 시작 거부 :1363 · 사본 `out_dir/_inputs/provider_maps/<consumer>.solution_map.json` :1352 (작업 문맥 `provider_maps` = 사본 경로 :1365 → `provider_x0` 가 다시 대조) | s06 (양성 1 · 음성 3: provider run 누락 · 계획 뒤 provider 변경 · warm x0 위조) | `warm-map-is-regenerated-and-compared-g81s` · `validator-rederives-every-x0-g81s` |
| F7 | §3 "같은 pair group 의 두 noise 실현" | 실제 소비 경로(`run_fit`) fixture 에 없었다 (단위 시험 n1_04 만) | 코드 변경 없음 — fixture 만 (`sign_producer` 형식의 두 noise 실현 curves) | s07 (대조군 — §7-4 의 "정상 대조군은 처음부터 GREEN 일 수 있다") | — |
| F11 | §5 좌표 결속 | 설계 `parameter_order` 가 optimizer 벡터에 묶이지 않았다 — 라운드 1 fixture 의 5 이름 order 가 fits 의 truth 열 이름과 겹쳐 map 이 truth 를 해로 읽을 수 있다는 것을 **fixture 가 가렸다** | `src/fitting.py` `_prepare_stage3` :1314 (`parameter_order == PARAM_NAMES` :48) · :1317 (`bank.n_params == len(bounds) == 4`) · map 열 = `PARAM_NAMES` :547. fixture 정정: 해 = `a_pe·b_pe·a_ne·b_ne` 열, truth 열은 0.5 미끼 | s08 | `design-order-is-the-optimizer-vector-g81s` |
| F12 | §4 validator 의 sig 별 분기 | sig 6 산출에 legacy 전역 `restart_예산_완주`(n_restarts)를 적용해 objective 별 예산(2·3)을 거부 | `src/io.py` `_stage3_checks` 의 objective 별 `restart_예산_완주` :1785 · legacy 검사는 sig 5 만 (`… and _gen != 6` :2235) | s09 | `v6-budget-is-checked-per-objective-g81s` |
| ④ · ⑦ | 고정 표 §7 변이 계획 | 라운드 1 이 "중복 index 허용"(④)과 "prefix 재해시"(⑦)를 등록하지 않았다 (대신 "다른 계획 기록" 이 등록됨) | 코드 변경 없음 — 변이만 추가 | w02 · w04 | `duplicate-bank-index-is-refused-g81s` · `full-bank-identity-is-not-a-prefix-g81s` |
| F8 | 절차 | 1차 영수증 커밋 `03f907cc` 에 원장 `LEG_PRESERVATION.yaml` 앵커 갱신 누락 (선례 `184d34dd` 는 같은 커밋) | 2차 영수증 커밋 `9b52eb2a` 에 앵커 3 값 × 2 leg 같이 | — | — (§8-g) |
| F9 | 절차 | 비준 순서 "전체 회귀 → 영수증" 과 달리 영수증을 먼저 만들었다 | 이번에도 같은 순서 — 이유 §8-h | — | — |
| F10 | §4 (낮음, 코드 판독) | v6 후보의 비유한 J 는 `failed` 가 아니라 `returned` 로 세고, validator 는 기록 정합성 실패로 거부 (legacy 와 같은 동작) | 변경 없음 — 판정 요청 §9-Q7 | — | — |

## §2 최소 diff (승인 범위 4 파일)

`git diff --stat 88ac144a..c82231c4 -- src tools configs scripts run.sh requirements*.txt` (81차 발송 SHA 기준):

```
 src/fitting.py       | 493 +++++++++++++++++++++++++++-
 src/io.py            | 366 ++++++++++++++++++++-
 tools/design_wire.py | 320 ++++++++++++++++++
 tools/preserve.py    | 312 +++++++++++++++++-
 4 files changed, 1468 insertions(+), 23 deletions(-)
```

그중 자체 점검분 `git diff --stat 20ab9655..f3de7e02 -- <같은 경로>`: `src/io.py` +258 · `src/fitting.py` ±109 · `tools/preserve.py` +27 — 3 files, 336 insertions(+), 58 deletions(-) (58 줄은 라운드 1 이 넣은 줄의 교체 — 81차 발송 SHA 기준 삭제는 위 23 줄이 전부).

RUN_SCOPE 의 다른 경로(`configs/ scripts/ run.sh requirements*.txt`) 변경 0. 새 production helper 파일 0. **81차 발송 SHA 기준 삭제 23 줄** (`git diff -U0 88ac144a..c82231c4 -- <RUN_SCOPE> | grep '^-'` 전수):
(a) 시그니처·호출부 6 줄 — `fit(…, candidates=None)` · `run_fit/_run_fit_staged/_run_fit_locked(…, stage3=None)` 와 그 호출 (b) `_fit_one` 의 legacy `res = fit(...)` 호출 7 줄 — v6/legacy 분기의 else 로 **텍스트 그대로** 이동 (`src/fitting.py:758–765`, v6 가지 :749–757) (c) run_spec 의 `"sig_version": 5` · `"seed_scheme": "sha1(cond_id)[:8]"` 상수 2 줄 → 조건식 (d) `validate_provenance` 의 `sig_version == 5` 검사 2 줄 → `∈ {5, 6}` + 분기 · restart 검사 3 줄 → 이름 분기(`restart_후보`/`restart_출처`) (e) `check_receipt` 의 envelope 키 검사 2 줄 → 두 키 집합 + `check_planned_envelope` (f) **(자체 점검 F12)** legacy 예산 검사 조건 1 줄 `if _opt.get("adaptive") is False:` → `… and _gen != 6:`.

**legacy / prep 경로 불변 증거**: `w03_legacy_fit_is_byte_identical_golden_still_holds` (79차 골든 값 그대로) · `n2_00` (선언 없는 역사적 reader 3 세대) · `tests/test_gate79_stage3_logging.py` 15 node 전부 통과 (§5 의 59 passed 안) · `candidates`/`stage3` 를 주지 않은 `fit()`/`run_fit()` 은 `sig_version 5` · `seed_scheme "sha1(cond_id)[:8]"` 그대로 (`w05`) · sig 5 산출에 대한 기존 검사의 판정 규칙은 (d)·(f) 의 분기 조건 외에 81차 발송 SHA 와 같다 — 두 leg 의 기존 검사 34/33 이 이름 그대로 전부 `통과` 이고 새 검사는 `세대_선언_일치` 하나 (§7).

RUN_SCOPE 밖 동반 변경 (`88ac144a..c82231c4`): `tests/conftest.py` +3 (§8-c) · `tests/test_gate81_stage3_wire.py` +1027 (신규) · `docs/22p_gap/mutation_replay.py` +292 (20 변이 + EXPECT + 증인 정정) · `docs/22p_gap/STAGE3_CONTRACT.md` ±6 (§1 줄번호 인용 3 곳 — 두 번 갱신, §8-b) · `docs/22p_gap/STAGE3_IMPL_ROUND1_SPEC.md` +124 (신규, §9 포함) · 영수증 2 + history 4 · `LEG_PRESERVATION.yaml` ±12 (앵커 3 값 × 2 leg).

## §3 schema / 필드 시점 표 (누가 · 언제 · 무엇을 쓰는가)

| 산출 | schema / 키 | 쓰는 시점 · 쓰는 곳 | 읽는 곳 (fail-closed) |
|---|---|---|---|
| 계획 envelope | `planned-leg/v4`: leg_id · protocol_generation · pairing_design_sha256 · parameter_order_sha256 · source_digest · objective_order · stages[1] {stage=`condition`, arm, candidate_mode, budget_by_objective, warm_provider_map} · **planned_counts (유도값)** · bank {generator, version, length, n_params, exact_bounds_sha256} · inputs {reference=`grid`, curves_sha256, base_config_digest} · provider_edges[] · roster {roster_sha256, n_obs, comparison_family_id, treatment_id, replicate_id} · min_retention_days · design_label · notes | **실행 전** — 사람이 `PlannedLegV4` 로 작성 → `planned_id()` | `check_envelope_v4` (봉인 전 · `_prepare_stage3` 시작 시 · `run_transaction` · `check_receipt`) |
| 설계 (pairing design) | `pairing_design` 본체 — `parameter_order` 는 **`PARAM_NAMES` 여야 한다** (F11) · coordinate.decimal_places | 실행 전 (계획의 `pairing_design_sha256` 로 봉인) · **실행 시** run_spec.stage3.`pairing_design` 에 본체 사본 (F2) | `_prepare_stage3` (digest · order) · validator `_stage3_rederive` (digest 대조 뒤 재유도 입력) |
| bank | `bank-seed/v1` → PCG64 unit cube (length × n_params) · full-bank sha | **실행 시작 시** `_prepare_stage3` 가 계획의 (pair_group_id, bank.version, length, n_params) 로 재생성; `bank_id = DW.bank_id(pg, version, full_sha)` | 후보 map 의 `bank_index` (`_stage3_candidates` · `_restart_ok_v6`) · validator 가 **같은 식으로 다시 만든다** (`_stage3_rederive`, F2) |
| solution map | `solution-map/v1` header {schema, provider_objective, provider_artifact_sha256, provider_protocol_sha256, parameter_order(= `PARAM_NAMES`), excluded_cond_ids} · entries {cond_id: {p, J}} | **provider 실행 뒤 · 계획 봉인 전** `make_solution_map(provider_run_dir, objective, out)` — 파일 바이트 sha 가 edge 의 `solution_map_sha256` (봉인) | consumer **시작 시** `_prepare_stage3` 가 provider run 에서 다시 만들어 edge sha 와 대조 (F5·F6) · `provider_x0` (바이트 sha · header · cond · bounds) |
| consumer 입력 사본 | `out_dir/_inputs/provider_maps/<consumer>.solution_map.json` (다시 만든 map 바이트 그대로) | **실행 시작 시** `_prepare_stage3` | `provider_x0` (실행 중) · validator `_stage3_rederive` (warm x0 digest 재유도) |
| run_spec | `sig_version: 6` · `seed_scheme: unit_cube_bank/v1` · `optimizer.adaptive: false` · `stage3 {planned_id, planned_envelope, pairing_design, pairing_design_sha256, parameter_order_sha256, bank_version, exact_bounds_sha256, candidate_mode, budget_by_objective, warm_provider_map, provider_edges_sha256, roster_sha256, arm, stage}` (14 키) | **실행 시** `_run_fit_locked` (`_prepare_stage3` 의 `spec_block`) | `validate_provenance`: `sig_version ∈ {5,6}` → 6 이면 `_stage3_checks` (14 키 전부 요구) · 5 이면 stage3 블록 있으면 `세대_선언_일치` 실패 (F1) |
| restart 행 | 10 키: p · J · i · source · warm · converged · n_eval · termination_status · **candidate_id** · **bank_index** (random 만 int, 나머지 null) + 행 단위 `record_generation: v6` · pair_group_id · bank_id · warm_provider_objective · warm_started · candidate_map_json | **실행 시** `_fit_candidates` (serializer) · `_fit_one` 행 | `_restart_ok_v6` (`restart_후보`) · `normalize_restart_record(r, declared="v6")` · `후보_재유도` (행 ↔ map entry, F2) · sig 5 선언 아래 v6 전용 키 → `세대_선언_일치` 실패 (F1) |
| candidate map · execution record | `candidate_map.json` (entries: cond_id · objective · source · bank_index · candidate_id · x0_sha256 · payload) · `execution-record/v1` {schema, leg_id, planned_id, source_digest, protocol_generation, realized {by_objective {attempted, returned, failed, not_attempted, counts_by_source, random_bank_prefix_len}, candidate_map_sha256, n_candidates, roster_observed_sha256, n_obs_observed, provider_consumed}, record_digest} | **실행 끝** `write_execution_record` — 실현값은 `src.io.realized_from_fits` (F3, validator 와 같은 정의) | `check_execution_record` (트랜잭션 `planned_seal` · provider_consumed ↔ 계획 edge, F4) · `_stage3_checks["execution_record"/"candidate_map"/"candidate_ids_결속"/"실현_재계산"]` (validator) |

## §4 ID · 좌표 · provider 결속 증거

| 결속 | 증거 (시험) |
|---|---|
| bank 는 (pair_group, version) 의 함수 · full-bank sha 는 B 무관 | b01 · b02 · 변이 `full-bank-identity-is-not-a-prefix-g81s` → w04 |
| exact_bounds_sha256 는 실제 ordered lb/ub 바이트 · x0 = lb + u·(ub−lb) · x0_sha256 | b03 · w01 (행의 x0 결속) |
| candidate_id 는 실물 row 바이트 (골든 placeholder `4*64` 와 다름 · 행마다 다름) | b04 |
| 계획 count = 유도값; 손으로 고친 count 거부; record 는 planned_id 참조 (같은 leg · 다른 계획도 거부) | b07 · n1_06 · n1_03 · n1_05 |
| **validator 가 후보 전부를 계획·bank·bounds·design 에서 다시 유도** — 가짜 x0 digest · map/행을 함께 바꾼 candidate_id · 뒤바꾼 bank_index · 계획 순서가 아닌 bank 소비(index·x0·ID 통째 교환) 거부 | s02 |
| 실현 count 는 행에서 다시 센 값 (계획 범위 안의 조작도 거부) | s03 |
| provider_consumed = 계획 edge 중 실제로 시도한 것 (쓰레기 3 종 · 시도했는데 기록 없음 거부) | s04 |
| solution map header 가 fits 바이트·objective·protocol·order 를 결속; protocol 은 provider run_spec 에서 잰 값 (인자 거부); fits A + map B 거부; header 를 보존한 유효 JSON 변조도 거부 | n3_01 · n3_02 · s05 |
| cond 부재 → 오류(no-warm 전환 없음) · objective 불일치 거부 · bounds 밖 clip 없이 거부 | n3_03 · w02 |
| edge 가 warm map 과 일치 · 순환/역방향/self 거부 · warm arm 둘째 objective null → 오류 | n3_04 |
| **warm 공급 end-to-end** (provider run → 계획 map → consumer run_fit → validate 통과) · provider run 누락 거부 · 계획 뒤 provider 변경은 **시작 전** 거부(fits 미생성) · warm x0 위조는 validator 재유도가 잡는다 | s06 |
| parameter_order = optimizer 벡터 · map 은 해 열을 읽는다 (truth 열 미끼) | s08 |
| 같은 pair group 의 두 noise 실현이 실제 소비 경로를 지난다 (대조군) | s07 |
| 실행이 계획 roster·curves sha·design sha·bounds sha 와 다르면 시작 거부; warm 필요 자리의 provider 없음 → 시작 거부 | w06 · w04 · s06 |
| sig 6 산출은 stage3 블록·record·map 없이는 validator 를 못 지남; sig 7 거부; sig 5 는 기존 검사 + `세대_선언_일치` (v6 행 키·블록·열이 섞이면 실패) | w05 · s01 |
| sig 6 예산은 objective 별 계획 길이 | s09 |

## §5 시험 · 변이 결과

| 단계 | 결과 (실행 출력) |
|---|---|
| RED 라운드 1 (`6473d1fb`, 패치 전) | 34 node — **32 failed / 2 passed** (`scratchpad/red_gate81_initial.txt`; 대조군 n2_00 · w03 만 통과) |
| GREEN 라운드 1 (`20ab9655`) | gate81 35 + gate79 15 → **50 passed** (13.82 s) |
| 변이 라운드 1 첫 관측 (`--emit-expect -k g81`) | 7 중 **2 건 rc 0** — `record-must-reference-this-plan-g81`: 반례 `other_leg` 가 leg_id 대조에 먼저 걸림 · `solution-map-is-consumed-only-when-sealed-g81`: 마지막 바이트 뒤집기가 `JSONDecodeError`(ValueError 하위)로 통과. **시험 결함** — 반례를 "같은 leg · 다른 계획(bank 길이만 다름)" / "header 보존 유효 JSON 변조" 로 바꿔 재관측 7/7 (`scratchpad/g81_emit_expect.txt` → `g81_emit_expect2.txt`) |
| RED 자체 점검 (`315f5028`, 패치 전) | 44 node — **14 failed / 30 passed**. 분류: n3_01 · n3_02 · n3_03 · s05 = `make_solution_map` 새 API 의 `TypeError` · w04 · w06 · s02 · s03 · s06 · s07 · s08 · s09 = 문맥 키 `provider_runs` 의 `ValueError`/regex — **둘 다 무관 예외이므로 RED 증거로 세지 않는다** (리뷰 §7-4) · s01 = `assert '세대_선언_일치' in ['출력봉인_재계산']` (실제 이유: 검사 없음) · s04 = 쓰레기 `provider_consumed` 가 `[]` (실제 이유) |
| 실제 이유 탐침 (트리 밖 sandbox — 패치 전 코드, 같은 시험을 옛 문맥 키 `provider_maps` 로 되돌려 실행) | s02 `assert '후보_재유도' in []` (위조가 모든 검사 통과) · s03 `AssertionError: []` (조작 count 통과) · s08 `Failed: DID NOT RAISE ValueError` (5 이름 order 로 실행 시작) · s09 `AssertionError: ['restart_예산_완주']` (정상 산출 거부) · s07 **passed** (대조군) — "4 failed, 1 passed, 39 deselected". s05 의 실제 결함은 트리 밖 repro (`"0"*64` 인자가 header 에 그대로 봉인). s06 은 새 기능(한 번도 안 돈 warm 경로)이라 탐침 대상이 아니다 — 도달 경로는 최종 코드에서 변이 2 건(`validator-rederives-every-x0-g81s` · `warm-map-is-regenerated-and-compared-g81s`)이 s06 을 무는 것으로 보인다 |
| GREEN 자체 점검 (`f3de7e02`) | gate81 44 + gate79 15 → **59 passed** (35.08 s) |
| 이웃 회귀 (`f3de7e02` 트리, 영수증 2차 재생성 **전**) | preserve · design_wire · fitting · gate70/74/75: **618 passed · 15 failed** — 15 건 전부 영수증 identity 이탈 가족 (`g70_e3_17` · `g74_3_01` · `g74_3_03[6]` · `g75_n3_00` · `g75_n3_01[5]` · `g75_n3_01b`), 라운드 1 과 같은 가족. 재생성·앵커 뒤 상태는 §6 전체 회귀 |
| 변이 자체 점검 첫 관측 (`--emit-expect -k g81s`) | 13 중 **12 rc 1 · 1 rc 0** — `warm-map-is-regenerated-and-compared-g81s`: 시작 시점 map 대조를 지워도 worker 안의 `provider_x0` 봉인 대조가 같은 조건을 늦게 `ValueError` 로 잡아 s06 ② 의 `match="map|sha"` 가 그대로 맞았다 (심층 방어가 시작 대조의 부재를 가렸다). **시험 결함** — s06 ② 를 시작 대조의 문장(`match="다시 만든 map sha"`) + `fits.parquet` 미생성 단언으로 좁혔다 (`2d2f5d8b`). 재관측: s06 이 "Regex pattern did not match." 로 실패 → 13/13 rc 1 (`scratchpad/g81s_emit_expect.txt` → `g81s_emit_warm.txt`) |
| 변이 재생 (`-k g81`, clean `2d2f5d8b`, 시작 HEAD = 끝 HEAD, status 0) | **20/20** — "실행한 변이 20건이 전부 기대 node 를 call 단계에서 물었다" (scenario_total 20 · scenario_executable 20 · ran 20 · rc 0) · `--check-preimages -k g81`: "모든 변이 지점이 정확히 한 번 나타난다" (rc 0). 증인은 node 별 (`EXPECT` 81차 블록 + 82차 자체 점검 블록; 잘린 repr 꼬리와 fixture sha 값은 담지 않는다) |
| **첫 전체 회귀 (clean `9d5d8d1c`)** | docs-lint 358 passed (1482.55 s) · 전체 pytest **1 failed** · 2003 passed · 1 xfailed (3658.18 s) · strict smoke rc 0 (215 s) · 시작 HEAD = 끝 HEAD · status 0 — 실패 `tests/test_gate67_defensive.py::test_g67_14_every_registered_witness_is_a_fixed_reason`: "map-protocol-is-measured-from-the-run-spec-g81s · test_g81_n3_01… · test_g81_s05…: 열린 따옴표 뒤에 '000000000000' 가 남아 있다" (§8-m) → 증인 두 개를 따옴표 직전에서 끊음 `d76b3eda` (격리 사본에서 같은 1 failed 재현 → 정정 뒤 1 passed) |
| 변이 재생 2 (`-k g81`, 증인 정정 뒤 clean `c82231c4`) | **20/20** — "실행한 변이 20건이 전부 기대 node 를 call 단계에서 물었다" (scenario_total 20 · scenario_executable 20 · ran 20 · rc 0) · `--check-preimages -k g81`: "모든 변이 지점이 정확히 한 번 나타난다" (rc 0) · 시작 HEAD = 끝 HEAD = `c82231c4` · status 0 |

## §6 실행 출력

**판정 대상 HEAD `c82231c4`** (clean · 시작 HEAD = 끝 HEAD = `c82231c49460f79bb5474185648594b3a6c9fc02` · 시작/끝 status 0 줄 · 도는 동안 커밋 0 · 2026-09-28T07:57:50Z → 2026-09-28T09:31:55Z):

```
docs-lint (tests/test_docs_lint.py 단독)   358 passed · 0 failed in 1773.11s (0:29:33) · rc 0
전체 pytest (tests/)                        0 failed · 2004 passed, 1 xfailed in 3660.34s (1:01:00) · rc 0
strict smoke (scripts/smoke_e2e.sh)         rc 0 · "✅ pipeline smoke 통과" (205 s — 작은 grid/fit/score/restore 계산 포함, 연구용 새 실행 0)
source_digest                               02a776a7a0a3f4ba
```

xfailed 1 = `tests/test_gate63_defensive.py::test_staging_an_input_outside_the_repo_is_still_unsupported` (선언된 예상 실패 — 81차 발송 실행에도 1 xfailed). 같은 러너의 앞선 두 실행은 red 였다 — `3b008357` (§8-g, 원장 앵커 누락) · `9d5d8d1c` (§8-m, 증인 규칙 1 건). 발송 SHA 의 docs-lint 는 발송문에 적는다 (요청문은 자기 SHA 를 담을 수 없다).

## §7 영수증 diff (원본 `eda3feb8` ↔ 1차 `eea5977f` ↔ 2차 `02a776a7`)

2차: `make_receipt.py paired_fixed5_v4 grid_fit_v5` — 시작 HEAD = 끝 HEAD = `23670e58` · 시작 status 0 줄 · rc 0 (05:57:42Z → 05:59:15Z). 출력: paired_fixed5_v4 ✅ 검사 35건 · 산출 2건 · core_sha acbe879119fe866a (대상 커밋의 `receipts/paired_fixed5_v4.validate.yaml` 과 대조 가능) · grid_fit_v5 ✅ 검사 34건 · 산출 2건 · `core_sha256` 앞 16 = `e7f3a62472e53b30`.

| 필드 | paired_fixed5_v4 | grid_fit_v5 |
|---|---|---|
| `core_sha256` | `00db82af… → 18d78e15… → acbe8791…` | `ffc2e935… → 39d27dca… → e7f3a624…` |
| `core.identity.validator_source_digest` | `eda3feb8f4536511 → eea5977f4faf9685 → 02a776a7a0a3f4ba` | 같음 |
| `core.identity.src_io_sha256` | `d96e78b236696cff → da6f7a0e265b55aa → 9c71bf42711ff184` | 같음 |
| `core.identity` 나머지 5 항 (`src_scoring_sha256` · `archive_bundle_sha256` · `make_receipt_sha256` · `row_projection_sha256` · `row_projection_compute_sha256`) | **세 세대 동일** (producer cut 은 안 움직였다) | 동일 |
| `core.validation` | ok True · fail [] · n_checks **34 → 34 → 35** — 추가 검사는 **`세대_선언_일치` 하나** (제거 0), 모든 값 `통과` | ok True · fail [] · **33 → 33 → 34** — 같음 |
| `core.bundle` · `core.leg_id` · `core.outputs` · `core.outputs_agree` · `core.restore` | **세 세대 동일** | 동일 |
| `stamp.validator_commit` | `6ffa98d4 → 20ab9655 → 23670e58` | 같음 |
| `stamp.validator_tree_dirty` | false · false · false | **true · true · true** — 같은 호출에서 paired 영수증 파일을 먼저 쓴 뒤 grid 를 만들 때의 기록 (stamp 는 core 대조 밖 · history 14 건도 false 7 / true 7 로 같은 패턴) |

`LEG_PRESERVATION.yaml` (같은 커밋 `9b52eb2a`): leg 마다 `verification_receipt_core_sha256` · `validator_identity.source_digest` · `validator_identity.n_checks` (paired 34→35 · grid 33→34).

즉 **validator 만 움직였고 producer(`row_projection` · `scoring`)와 격리 복원·검증·재채점 결과는 세 세대 내내 그대로**다. 세대표 `CLAIM_STATUS.yaml::source_digest_generations` 에는 `eea5977f4faf9685` · `02a776a7a0a3f4ba` 모두 없다 — 등록은 실물 v6 leg 배선 라운드의 일 (§9-Q5).

## §8 우리가 스스로 신고하는 것

| # | 신고 | 우리 처리 · 리뷰어 판정 요청 |
|---|---|---|
| a | 라운드 1 변이 2 건 첫 관측 rc 0 (§5) | 시험 반례를 고쳐 재관측 7/7. **판정 요청**: 비준 4 항 "처음부터 통과해야 하는 대조군을 억지로 RED 로 만들지 않는다" 에 어긋나지 않는가 — 우리 판단: 어긋나지 않는다 (변이 아래서만 RED, 실코드에서는 GREEN) |
| b | `docs/22p_gap/STAGE3_CONTRACT.md` §1 의 줄번호 인용 3 곳을 **두 번** 갱신 (라운드 1 `1491→1935` · `1446→1890` · `461-475→736-760`, 자체 점검 `1935→1940` · `1890→1895` · `736-760→743-767`) | 본문 불변. `test_stage3_contract_cites_live_code_facts` 가 요구하는 기계적 갱신 (선례 `c77674f6` · `517f25ff`). 계약 §0 의 세 교란은 **legacy 경로에 그대로 남아 있다** (v6 경로에서만 사라짐) → 계약 §0 정정은 다음 라운드 (§9-Q5) |
| c | `tests/conftest.py::_GATED_ENTRYPOINT_MODULES` 에 `test_gate81_stage3_wire` 등록 (+3 줄) | production `run_fit()` 을 smoke namespace(`results/_smoke/_unit/`) 안에서 재기 위함 — 47차 P0-3 과 같은 이유. 새 연구 실행 0 (비준 4 항의 "검증용 작은 계산" 은 합성 curves 위의 `run_fit` 호출뿐 — n3_04 · s01 · s02 · s03 · s06 · s07 · s08 · s09 · w04 · w05 · w06, 시험 파일 안 `run_fit`/`_run_v6` 호출 전수) |
| d | `src/fitting.py:350` 의 역사적 `normalize_restart_record(r)` 정의가 **dead 정의**로 남아 있다 (`:413` 의 dispatch 판이 `# noqa: F811` 로 덮음) | 동작 영향 0 (뒤 정의가 이김). **판정 요청**: 라운드 2 에서 삭제할지 (§9-Q1) |
| e | `_fit_one` v6 분기의 `warmed` 플래그는 후보 목록에서 계산 (`any(source == "warm")`, :757) — legacy 의 `init is not task["init"]` 와 의미가 다르다 | 행 `warm_started` 로 기록. v6 행 소비자(`row_projection` · `scoring`)는 `J`·`source` 만 읽으므로 무영향 (79차 `g79_07`) |
| **f** | **영수증 2회째** — 리뷰 §7-6 은 "최종 코드가 고정된 clean 커밋에서 … 각각 1회 재생성 … 이후 RUN_SCOPE 가 다시 움직이면 최종 영수증이 아니라는 상태로 멈춰 보고한다", 비준 5 항은 "실패·추가 RUN_SCOPE 이동이면 최종 완료로 게시하지 말고 회신한다" | 1차 재생성(`03f907cc`, clean `20ab9655`) 뒤 자체 점검이 RUN_SCOPE 를 다시 움직였다 (`f3de7e02`). 멈추는 대신 **사용자 결정**("지금 고치고 영수증 한 번 더", 2026-09-28)으로 1차본을 바이트 그대로 보존(`23670e58`)하고 최종 코드에서 한 번 더 만들었다(`9b52eb2a`). 검증 실패를 재생성으로 닫은 것이 아니다 — 두 번 모두 ok True · fail [] 이고 차이는 validator identity 2 항 + 검사 1 개 (§7). **최종 완료로 게시하지 않는다** — 이 요청이 그 회신이다. **판정 요청 §9-Q6** |
| **g** | **첫 전체 회귀 red** — 1차 영수증 뒤 clean `3b008357` 에서 돌린 전체 검증 (시작 HEAD = 끝 HEAD · status 0 · 04:31:19Z → 05:45:51Z): docs-lint **3 failed** / 355 passed (1335.61 s) · 전체 pytest **13 failed** / 1982 passed / 1 xfailed (2958.98 s) · strict smoke rc 0 (172 s). docs-lint 실패 3: `test_every_leg_binds_its_evidence_to_verifiable_anchors` · `test_no_active_claim_legs_still_carry_the_full_bundle_evidence_contract` · `test_full_bundle_claims_are_backed_by_a_real_bundle`. pytest 끝 5 줄에 보인 실패: `g74_3_03[_unvalidated · _pending · _validator_drift]` · `g75_n3_00` · `g75_n3_01b` (그 러너는 끝 6 줄만 남겨 13 건 전체 이름은 없다) | 원인 F8 — `03f907cc` 가 원장 `LEG_PRESERVATION.yaml` 의 앵커(`verification_receipt_core_sha256` · `validator_identity.source_digest`)를 갱신하지 않았다 (선례 `184d34dd` 는 같은 커밋). 2차 영수증 커밋 `9b52eb2a` 에 앵커 3 값(검사가 하나 늘어 `n_checks` 포함) × 2 leg 를 같이 넣었다. 그 뒤 전체 회귀가 §6 (이번 러너는 전체 출력을 파일로 남긴다) |
| **h** | **순서 (F9)** — 비준 4 항(전체 회귀·strict smoke) → 5 항(영수증) 의 번호 순서와 달리, 두 번 다 영수증을 먼저 만들고 전체 회귀를 뒤에 돌렸다 | 전체 회귀 안에 영수증 identity 일치 시험 15 건(§5 이웃 회귀의 가족)이 있어, RUN_SCOPE 가 움직인 뒤 영수증 재생성 전에는 전체 회귀가 정의상 red 이다 (79·80차 선례도 같은 순서). **판정 요청**: 이 순서로 충분한가 — 아니면 "영수증 전 회귀(영수증 가족 제외) → 영수증 → 전체 회귀" 의 두 번 실행을 요구하는가 |
| **i** | **RED 이유 (리뷰 §7-4)** — `315f5028` 의 14 failed 중 12 건은 API/문맥 키 변경의 무관 예외 | RED 증거로 세지 않고 실제 이유를 따로 쟀다 (§5 탐침 · 트리 밖 repro · 변이 도달). 무관 예외를 먼저 지우는 순서(시험을 옛 API 로 쓰고 → 실패 → API 변경)를 택하지 않은 이유: 새 API 자체가 F5·F6 의 정정이라 옛 API 로는 요구를 적을 수 없다 |
| **j** | **fixture 가 진실을 가렸다 (F11)** — 라운드 1 의 GREEN 은 5 이름 좌표 order 의 fixture 위였고, 그 order 가 fits 의 truth 열과 겹쳐 "map 이 truth 를 해로 읽는" 경로를 가렸다 | fixture 를 실제 모양으로 (`ORDER = PARAM_NAMES` · 해 열 · truth 미끼 0.5) 고친 뒤 s08 이 RED (탐침 DID NOT RAISE) → `_prepare_stage3` 가 order = optimizer 벡터를 요구 |
| **k** | 라운드 1 기록의 노드 수 — 발송 전 초안이 "구현 뒤 시험 36 node" 로 적었다 | 실측 35 (`20ab9655` 트리 `pytest --collect-only`: gate81 35 · + gate79 = 50). 저장소 커밋 문서에는 "36 node" 가 없다 (`git grep` 0) — 이 요청문은 35 로 적는다 |
| **l** | **질문 뒤 범위 변화** — 자체 점검 뒤 사용자에게 물은 질문은 7 건("validator 쪽 구멍 5건과 시험 누락 2건" = F1~F5 · F6 · F7)을 말했다. RED·GREEN 중에 F11 · F12 가 더 나왔다 | 같은 4 파일 · 같은 라운드에서 RED(s08 · s09) 먼저 고쳤고 사용자에게 따로 묻지 않았다. 둘 다 81차 닫힘 조건(§5 좌표 결속 · §4 sig 별 분기) 안의 결함 정정이라 비준 범위 안이라고 판단했다 — **판정 요청**: 이 판단이 맞는가 |
| **m** | **두 번째 전체 회귀도 첫 실행은 red** — clean `9d5d8d1c` (2차 영수증 · 앵커 · 변이 EXPECT 뒤): 1 failed `test_g67_14_every_registered_witness_is_a_fixed_reason` (G67-T1-b). 자체 점검 EXPECT 의 `map-protocol-is-measured-from-the-run-spec-g81s` 증인 두 개를 잘린 repr 대신 `assert ('000000000000` / `assert '000000000000` 로 잘랐는데, 규칙은 가변 값 **직전**(따옴표)에서 끊는 것만 허용한다 | `d76b3eda` 에서 `AssertionError: assert ('` / `AssertionError: assert '` 로 정정 (RUN_SCOPE 밖 — digest · 영수증 불변). 원인은 절차: EXPECT 를 붙인 뒤 변이 재생과 preimage 검사만 돌리고 **등록부를 읽는 규칙 시험**(`tests/` 중 `EXPECT` 를 읽는 8 파일)을 따로 돌리지 않았다. 정정 뒤 변이 재생을 다시 돌렸고(§5) 전체 회귀도 다시 돌렸다(§6) |

## §9 리뷰어에게 묻는 것

| # | 질문 | 우리 제안 |
|---|---|---|
| Q1 | §8-d dead 정의 — 지금/다음 | 다음 라운드 (RUN_SCOPE 이동 최소화) |
| Q2 | `check_execution_record` 의 count 의미 — 계획 count 는 **조건당** 후보 구성, 실현 count 는 다리 전체 합(조건 × 후보); 계획 총합 = 조건당 계획 × roster n_obs. 표 A 의 의도와 같은가 | 같다고 본다 (roster 가 조건 집합의 사전 크기이므로). 다르면 record 에 조건별 count 를 추가 (schema 한 줄) |
| Q3 | 세대 정책 — v6 선언 아래 8 키 행은 `mixed_invalid` 로 reader 가 표시하고 validator(`restart_후보`)가 실패; sig 5 선언 아래 v6 전용 키·블록·열은 `세대_선언_일치` 실패. "조용한 하향 없음 · 선언-행 충돌 거부" 의 구현으로 충분한가 | 충분 (읽기 단계 표시 + 검증 단계 거부, 양방향) |
| Q4 | provider edge — 첫 objective 만 null 허용, warm arm 의 둘째부터는 provider 필수. 계약 §3 의 의도와 같은가 | 같다 (no-provider 는 "첫 objective 또는 warm-off arm" 에만) |
| Q5 | 라운드 2 범위 제안 — (i) 실물 v6 leg gate 배선 (`leg_run_spec` / `LEG_SPEC_*_KEYS` 의 `stage3` 축 · 계획 index 의 v4 envelope) (ii) `source_digest_generations` 에 v6 세대 등록 (iii) `stage="p_ini"` 정책 (iv) §8-d 삭제 (v) 계약 §0 정정 (vi) Q7 의 count 규칙 | 이 순서로 한 라운드 · 실행 GO 는 여전히 아님 |
| Q6 | §8-f 영수증 2회째 — 2차본(`9b52eb2a`)을 라운드 1 의 영수증으로 수용하는가, 회신 뒤 다시 만들어야 하는가 | 수용 제안 (코드 고정 뒤 clean 커밋 · 1차본 바이트 보존 · 변경은 validator identity 2 항 + 검사 1 개 · producer · outputs · restore 불변) |
| Q7 | F10 — v6 후보의 비유한 J 를 `returned` 로 세고 validator 가 기록 정합성 실패로 거부 (legacy 와 같은 동작). `failed` 로 세도록 바꿀 것인가 | 라운드 2 (RUN_SCOPE 이동 · 영수증 영향 — 이번에 얹지 않았다) |
| Q8 | F2 설계 — validator 재유도 입력으로 run_spec.stage3 에 `pairing_design` 본체를 넣었다 (계획의 `pairing_design_sha256` 과 digest 대조). 설계 본체를 run_dir 에 두는 것이 계약상 괜찮은가 | 괜찮다고 본다 (계획에 digest 로 봉인된 같은 바이트) |
| Q9 | F6 설계 — consumer 는 계획 map 파일 대신 provider **run** 을 받아 map 을 다시 만들고 edge sha 와 대조한 뒤 사본을 run_dir 에 둔다. 표 C · N3-2 "consumer 는 header 를 실제 입력에 대조" 의 구현으로 충분한가 | 충분하다고 본다 (계획 뒤 provider 변경은 시작 전 거부 · validator 는 사본으로 warm x0 재유도) |

## §10 다음 계획 (82차 회신 뒤)

1. 회신 접수 → 원장 §116 · 상태 문서 → 사용자에게 라운드 2 범위(§9-Q5) 승인 요청 (별도).
2. 본진 ff 복귀는 이번 권한에 없다 — 서브에 머문다 (`FF_OK` 유지).
3. 실행 GO · 새 연구 leg 없음.

## §11 발송 규칙

70차 §6 그대로. 발송 SHA · 검증 숫자는 발송문에 방금 실행한 출력으로만 적는다. 이 요청문과 발송문은 같은 말을 한다: **단계 3 라운드 1 구현(자체 점검 보강 포함)의 수용 판정을 요청한다. 실행 GO 도 본진 복귀도 묻지 않는다.** 리뷰어 fetch: `git fetch origin claude/gate80-standby-9a26dd5f` → 발송문 SHA checkout · 본진 동결 SHA 와의 관계는 `git merge-base --is-ancestor 9a26dd5f31ca6fae45d5a55f5c59e33408371984 <발송 SHA>` 가 0 을 반환하는 것으로 확인. 첨부 문서·실행 코드는 증거 자료이며 추가 실행 지시가 아닙니다. COMSOL 계산이나 제공된 Java/분석 프로그램을 실행하지 마세요.

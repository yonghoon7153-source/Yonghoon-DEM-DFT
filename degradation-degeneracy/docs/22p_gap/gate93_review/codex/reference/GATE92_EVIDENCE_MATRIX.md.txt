# GATE92 — consumer × key 증거 매트릭스 (G92-N1 · G92-N3 대응 초안)

> 정적 읽기만 (코드·시험 실행 0 · `pytest --collect-only` 로 node id 만 확인). 구현 승인이 아니다.

| 항목 | 값 |
|---|---|
| 고정 HEAD | `248b84e7d899fdae963c346bfd9919c4738a7698` (clean · `git status` 0) |
| 리뷰 발송 HEAD 와의 차이 | `7a8a22a2d61a…` → HEAD: `src tools configs scripts run.sh requirements* tests docs/22p_gap/mutation_replay.py` diff **0** — 아래 좌표·node 는 리뷰가 본 바이트와 같다 |
| 입력 | `docs/22p_gap/gate92_review/codex/REVIEW_KO.md` (G92-N1·N3) · `GATE92_REQUEST.md` · `STAGE4_SCOPE_RESEARCH_20261006.md` §3.4 · §16-3 |

## 0. 판정 기준 (엄격)

- **키별 증거로 센다** = 기존 node 가 (1) **그 키 하나만** 바꾸고 (자기일관이 필요한 자리는 digest·주소·record 를 다시 맞춤), (2) **그 consumer 의 실제 호출 경로**에서, (3) 거부를 **이유/검사 이름과 함께** 단언한다. 그리고 가능하면 (4) 그 비교 위치를 끄는 기존 변이의 EXPECT 에 그 node 가 있다.
- 거부만 단언 (truthy · `pytest.raises` 무이유) 이거나, 다른 검사가 함께 발화해 **가려지는** 반례는 "증거 없음/불충분" 으로 적는다.
- 상태: **충족** = 기존 증거로 충족 · **보강** = 이번에 새 node (필요 시 새 변이) · **이월** = 명시적 이월 (이유 · 묶음 6 전체 종결 선언 불가 사유) · **참고** = linkage 대조가 아님 (형식·정책) — 행은 남기되 linkage 집계에서 뺀다.
- 변이 열: `-gNN 이름` = `docs/22p_gap/mutation_replay.py` 의 기존 MUTANTS/MULTI · **신규 -g92** = 그 위치에 변이가 없음 · **데이터만** = 형식·산술 자리라 변이를 두지 않자는 제안 (사용자 결정).
- 줄 번호는 HEAD 기준.

### node 접두 약어 (전부 HEAD 에서 `--collect-only` 로 확인한 정확 id 의 앞부분)

| 약어 | 전개 |
|---|---|
| `G81::` | `tests/test_gate81_stage3_wire.py::` |
| `G82::` | `tests/test_gate82_residuals.py::` |
| `G84::` | `tests/test_gate84_round2a.py::` |
| `G85::` | `tests/test_gate85_closure_members.py::` |
| `G87::` | `tests/test_gate87_round2b.py::` |
| `G88::` | `tests/test_gate88_fit_only_lifecycle.py::` |
| `G89::` | `tests/test_gate89_finalize_input_binding.py::` |
| `TP::` | `tests/test_preserve.py::` |

자주 쓰는 정확 id: `G81::test_g81_n1_03_execution_record_of_another_plan_or_inconsistent_counts_is_rejected` (=n1_03) · `G81::test_g81_s02_the_validator_rederives_every_candidate_from_plan_bank_bounds_and_design` (=s02) · `G81::test_g81_w04_run_fit_with_stage3_context_writes_sig6_run_spec_execution_record_and_candidate_map` (=w04) · `G87::test_s03_05_a_stage3_axis_that_is_not_derived_from_the_envelope_is_refused[<key>]` (=s03_05[k]) · `G87::test_s03_04_an_envelope_that_disagrees_with_the_entry_is_refused[<id>]` (=s03_04[id]). 이하 표에서는 함수 이름의 앞부분 (`n1_03` · `s03_05[arm]` 등) 으로 줄여 쓰되, 각 줄은 위 전개로 정확 id 가 된다.

## 1. 집계

| 상태 | linkage 행 수 | 비고 |
|---|---|---|
| 충족 (기존 증거) | 51 | 그중 **node 는 있으나 비교 위치 변이가 없음** 4 (C5-8 `:1460` · C5-15 `:1499` · C5-16 `:1513` · C6-7 `:584`) + 부분 4 (C5-6 null 분기 `:1422` · C7-r13 `:1980` · C3-2 · C5-1 — 성질은 C1 변이가 담당) |
| 보강 (이번) | 66 (62 행 · C3-13 은 bank 하위 5 키) | 새 node: k03·k04·k05·k07 (RED 예상) · k06·k08·k09–k12 (GREEN 대조 — "무는가" 는 위치 변이가 증명) |
| 이월 | 2 | C8-4 재개 경로 (`preserve.py:4192`) · C7 `planned_envelope` ↔ **원장 계획** 대조 (validator 는 원장을 안 읽음 — §15) |
| 참고 (linkage 아님) | 6 | 형식 (C1-8 · C6-2 · C11-13) · 산술 (C2-9) · 정책 (C1-9 · C11-8) — 데이터 node 만 · 집계 밖 |

consumer 별: C1 충족 2 / 보강 4 · C2 충족 4 / 보강 7 · C3 충족 11 / 보강 8 · C4 충족 3 / 보강 2 · C5 충족 12 / 보강 6 · C6 충족 3 / 보강 4 · C7 (s3 16 키 + 닫힘 2) 충족 4 / 보강 14 · C7 행 충족 6 / 보강 8 · C8 충족 1 / 보강 2 / 이월 1 · C9 충족 4 · C11 충족 1 / 보강 11.

(A) 부재 고정 (구 필드 닫힘) 은 linkage 키가 아니라 §11 에 따로 적는다.

---

## 2. C1 `check_envelope_v4` / `check_planned_envelope` (`tools/preserve.py:3170` / `:3275`)

실호출: `PlannedLegV4.__init__` (`:2409`) · C3 `:6151` · C5 `src/fitting.py:1403,1444` · C7 `src/io.py:1881` · C2 `:3306` · helper `:6646`. 양성 대조: `G81::test_g81_n1_01_planned_leg_v4_envelope_is_closed_and_carries_no_realized_values`.

| # | 키 | 비교 위치 | 기대값 독립 출처 | 음성 node · 증인 | 변이 | 상태 |
|---|---|---|---|---|---|---|
| C1-1 | `planned_counts` | `:3228` | `DW.planned_counts(mode, B, warm_map)` 재유도 | `G81::test_g81_n1_06_planned_counts_are_derived_and_a_hand_edited_count_is_refused` — count 하나 +1 · `match="planned_counts"` (생성자) + `check_envelope_v4` 이유 `"planned_counts"` | `planned-counts-are-derived-not-copied-g81` | 충족 |
| C1-2 | `bank.generator` · `bank.version` | `:3239` | 구현 profile 상수 (`check_bank_profile`) | `G82::test_g82_n2_02_an_envelope_declaring_another_generator_is_refused_before_it_is_sealed` — `match="bank profile"` (생성자) · version 만 `v6.1` → `"bank profile"` | `the-envelope-bank-is-checked-against-the-profile-g82` | 충족 |
| C1-3 | `bank.length` ≥ 계획 random prefix | `:3242` | `planned_counts` 유도값 | 없음 → **신규 k09-C1[bank_length]** | 신규 -g92 | 보강 |
| C1-4 | `budget_by_objective` 키 집합 = `objective_order` | `:3214` | 같은 envelope 의 `objective_order` | 없음 → **k09-C1[budget_keys]** | 신규 -g92 | 보강 |
| C1-5 | `warm_provider_map` 정의역·값 ⊂ `objective_order` | `:3219` | 같은 envelope 의 `objective_order` | 없음 → **k09-C1[warm_map_domain]** | 신규 -g92 | 보강 |
| C1-6 | `stages[0].stage == "condition"` (p_ini 명시 거부) | `:3207–3210` | 계약 상수 | 없음 (edge 수준 p_ini 만 `G81::test_g81_n3_04_…` — C11) → **k09-C1[stage_p_ini]** | 신규 -g92 | 보강 |
| C1-7 | `provider_edges` ↔ warm map · arm · stage | `:3256` → C11 | — | C11 행으로 | — | (C11) |
| C1-8 | hex64/16hex/세대 문법 (`pairing_design_sha256` · `parameter_order_sha256` · `bank.exact_bounds_sha256` · `inputs.*` · `source_digest` · `protocol_generation`) | `:3187–3193,3244,3252–3255` | 형식 규칙 | `s03_04[invalid-envelope]` (inputs.curves_sha256 하나 · C3 경로 · `"planned_envelope"`) 뿐 → **k09-C1[fmt-*]** | 데이터만 | 참고 (형식) |
| C1-9 | `min_retention_days` | `:3270` | 정책 하한 | 없음 | — | 참고 (정책) |

## 3. C2 `check_execution_record` (`tools/preserve.py:3287`)

실호출: validator `src/io.py:1901` · `run_transaction` planned_seal `tools/preserve.py:3718`. 양성: `G81::test_g81_n1_02_planned_id_is_invariant_to_realized_counts_and_v3_validator_rejects_v4_keys` · `G84::test_g84_n4_00_the_writer_emits_v2_with_finite_and_converged_that_match_the_rows` (writer record → validator `실현_재계산` 통과).

**주의 (마스킹):** `n1_03` 의 count·source_digest 하위 사례는 `record_digest` 를 **다시 계산하지 않는다** → `:3304` "record_digest 가 자기 내용과 다르다" 가 함께 발화하고 단언은 truthy 뿐이다. 그 위치를 끄는 변이가 있어도 이 node 는 녹색으로 남는다 → 키별 증거로 세지 않는다. (`extra` 키 사례만 `:3297` 이 먼저 return 하므로 유효 — 닫힘 행.)

| # | 키 | 비교 위치 | 기대값 출처 | 음성 node · 증인 | 변이 | 상태 |
|---|---|---|---|---|---|---|
| C2-1 | `leg_id` | `:3309` | 계획 envelope `leg_id` | 없음 — `n1_03` 의 `q`(other_leg) 반례는 `planned_id` 도 함께 어긋난다 (시험 주석 `:285–286` 이 마스킹을 실측 기록) → **k09-C2[leg_id]** (record 만 · `record_digest` 재계산) | 신규 -g92 | 보강 |
| C2-2 | `planned_id` | `:3311` | `digest(planned_env)` 재계산 | `n1_03` p2 (같은 leg · bank_length 만 다른 계획) — `"다른 계획의 기록"` · `G81::test_g81_n1_05_run_transaction_with_a_v4_plan_requires_a_consistent_execution_record` (run_transaction 실경로 · `stage == "planned_seal"` · `"다른 계획의 기록"`) | `record-must-reference-this-plan-g81` (EXPECT: n1_03 · n1_05) | 충족 (validator 경로 node 는 없음 — 같은 함수 · 같은 위치라 재사용) |
| C2-3 | `source_digest` | `:3313` | envelope `source_digest` | `n1_03` `bad["source_digest"]="0"*16` — **record_digest 미재계산 → 마스킹** → **k09-C2[source_digest]** | 신규 -g92 | 보강 |
| C2-4 | `protocol_generation` | `:3315` | envelope | 없음 (`G82::test_g82_n3_02_…` 는 env·record **함께** v5 → C2 는 통과, 다른 위치 `io.py:1909–1911` 이 거부) → **k09-C2[protocol_generation]** | 신규 -g92 | 보강 |
| C2-5 | `attempted+not_attempted` = 계획×n_obs | `:3345` | `planned_counts` × `roster.n_obs` | `n1_03` attempted=9 (마스킹) → **k09-C2[total]** | 신규 -g92 | 보강 |
| C2-6 | `counts_by_source[src]` ≤ 계획×n_obs | `:3352` | 같음 | `n1_03` warm=1 (마스킹) → **k09-C2[source_le_plan]** | 신규 -g92 | 보강 |
| C2-7 | `random_bank_prefix_len` ≤ 계획 random · `bank.length` | `:3359` | `planned_counts` · `bank.length` | 없음 → **k09-C2[prefix]** | 신규 -g92 | 보강 |
| C2-8 | `n_obs_observed` ≤ roster `n_obs` | `:3367` | envelope roster | `n1_03` n_obs_observed=99 (마스킹) → **k09-C2[n_obs]** | 신규 -g92 | 보강 |
| C2-9 | `attempted = returned + failed` · Σsource = returned | `:3339,:3354` | 기록 자체 (내부 산술) | `n1_03` failed=1 (마스킹) | 데이터만 (k09-C2[arith-*]) | 참고 (산술) |
| C2-10 | `finite` · `converged` ≤ returned | `:3337` | 기록 자체 | `G84::test_g84_n4_03_type_and_bound_forgeries_of_the_new_counts_are_refused` (record_digest 재계산 ✓ · 단언은 `"위조가 통과했다"` — 이유 미단언) | `v2-counts-are-bounded-by-returned-g84` | 충족 |
| C2-11 | `schema` 분기 | `:3301` | `_RECORD_SCHEMA_KEYS` | `G84::test_g84_n4_01_v1_records_are_read_as_written_and_are_not_upgraded_or_mixed` | `record-schema-dispatch-is-closed-g84` · `v2-missing-counts-do-not-fall-back-to-v1-g84` | 충족 |
| C2-12 | `provider_consumed` ↔ 계획 edge | `:3384,:3394` | envelope `provider_edges` | `G81::test_g81_s04_provider_consumed_must_be_exactly_the_planned_edges_that_were_used` (record_digest 재계산 ✓) — 증인 `"warm 으로 시도했는데 공급 기록이 없다"` | `provider-consumed-must-be-a-planned-edge-g81s` · `a-used-edge-must-be-recorded-g81s` | 충족 |

## 4. C3 계획 index `_check_v6_plan_slots` (`tools/preserve.py:6123`, `planned_index` `:6196` 경유)

양성: `G87::test_s03_01_a_v3_entry_with_envelope_and_context_indexes`. 기대값 출처 = 같은 항목의 `planned_envelope` 에서 `stage3_axis_from_envelope` (`:6640`) 로 **재유도** (dict 전체 비교 `:6170`).

| # | 키 | 비교 위치 | 음성 node · 증인 (자기일관: 축 재유도 / `_reseal` 주소 재봉인) | 변이 | 상태 |
|---|---|---|---|---|---|
| C3-1 | v6 두 자리 ⇔ `leg_spec_version 3` | `:6136–6147` | `s03_02[planned_envelope|stage3_context]` (`drop in msg or "leg_spec_version"`) · `s03_03[*]` (raise 만) | `v3-plan-requires-both-v6-slots-g87` · `v2-plan-refuses-v6-slots-g87` | 충족 |
| C3-2 | envelope 유효성 | `:6151` | `s03_04[invalid-envelope]` — `"planned_envelope"` | (C1 변이들이 성질 담당) | 충족 |
| C3-3 | `env.leg_id` ↔ 항목 | `:6156` | `s03_04[leg_id]` — `"planned_envelope"` | `envelope-leg-id-is-bound-to-the-entry-g87` | 충족 |
| C3-4 | `env.source_digest` ↔ `authorized_source_digest` | `:6159` | `s03_04[source_digest]` | `envelope-source-digest-is-bound-to-the-entry-g87` | 충족 |
| C3-5 | `env.protocol_generation` == v6 | `:6164` | `s03_04[generation]` | `envelope-generation-is-v6-g87` | 충족 |
| C3-6 | 축 `planned_id` | `:6170` | `s03_05[planned_id]` — `"stage3" in msg` | `stage3-axis-is-derived-not-copied-g87` (EXPECT 5 node · `DID NOT RAISE PreserveError`) | 충족 |
| C3-7 | 축 `roster_sha256` | `:6170` | `s03_05[roster_sha256]` | 같음 | 충족 |
| C3-8 | 축 `provider_edges_sha256` | `:6170` | `s03_05[provider_edges_sha256]` (no-warm 계획 — 빈 edge. warm edge 값 일치는 k07) | 같음 | 충족 |
| C3-9 | 축 `arm` | `:6170` | `s03_05[arm]` | 같음 | 충족 |
| C3-10 | 축 `candidate_mode` | `:6170` | `s03_05[candidate_mode]` | 같음 | 충족 |
| C3-11 | 축 `pairing_design_sha256` | `:6170` | 없음 → **k08[pairing_design_sha256]** | 같은 위치 `-g87` — **-k 확장** (`s03_05 or k08`) 필요 · 증인 집합 변경 = 사전 보고 대상 | 보강 |
| C3-12 | 축 `parameter_order_sha256` | `:6170` | 없음 → **k08[parameter_order_sha256]** | 같음 | 보강 |
| C3-13 | 축 `bank.generator` · `.version` · `.length` · `.n_params` · `.exact_bounds_sha256` (5) | `:6170` | 없음 → **k08[bank.*] ×5** (예측: dict 비교가 거부 · 다른 검사가 먼저 막는지는 관측 필요) | 같음 | 보강 (5행) |
| C3-14 | 축 `stage` | `:6170` | 없음 → **k08[stage]** | 같음 | 보강 |
| C3-15 | `stage3_context` 경로 · `provider_runs` = warm consumer | `:6181–6193` | `G87::test_s03_06_provider_runs_must_name_exactly_the_warm_consumers` (`"provider"`) · `s03_07[*]` (raise 만) | `provider-runs-match-the-warm-consumers-g87` · `context-paths-are-repo-relative-g87` | 충족 |

k08 은 `s03_05` 보다 증인을 강하게: 이유 문자열에 **키 이름**까지 단언 (`:6174` 메시지가 어긋난 키 목록을 담는다 — 기존 `s03_05` 는 `"stage3"` 만 단언).

## 5. C4 `stage3_context_from_plan` (`src/fitting.py:1324`) — production 진입점

양성: `G87::test_s04_01_the_entrypoint_builds_the_context_from_the_ledger_and_run_fit_completes`.

| # | 키 | 비교 위치 | 기대값 출처 | 음성 node · 증인 | 변이 | 상태 |
|---|---|---|---|---|---|---|
| C4-1 | 계획 존재 · v6 형태 | `:1339–1346` | 원장 index | `G87::test_s04_05_an_unknown_leg_is_refused` (raise 만 · 이유 미단언) → **k09-C4[unknown_leg]** 이유 단언 | 데이터만 | 보강 |
| C4-2 | `planned_id` (index 불신) | `:1351` | `PlannedLegV4(**env).planned_id()` 재계산 | `G87::test_s04_04_the_entrypoint_does_not_trust_the_index_for_planned_id` — `"planned_id"` (index monkeypatch 로 단독 위조) | `entrypoint-does-not-trust-the-index-planned-id-g87` | 충족 |
| C4-3 | 설계 파일 `pairing_design_sha256` | `:1368` | 설계 JSON 바이트 재계산 | `G87::test_s04_02_a_design_file_whose_bytes_differ_from_the_plan_is_refused_before_run_fit` — `"pairing_design_sha256"` · run_fit 미호출 | `entrypoint-compares-the-design-digest-g87` | 충족 |
| C4-4 | 설계 `parameter_order_sha256` | `:1372` | 설계 `parameter_order` 재계산 | 없음 → **k09-C4[parameter_order_sha256]** (envelope 의 그 hex64 만 다르게 · 축 재유도·주소 재봉인 → index 통과 · 설계 digest 일치) | 신규 -g92 | 보강 |
| C4-5 | provider run 디렉터리 · manifest | `:1378` | 파일 시스템 | `G87::test_s04_03_a_missing_design_file_or_provider_dir_is_refused` 후반 — `"provider"` (전반의 설계 파일 없음은 이유 미단언) | `entrypoint-requires-provider-run-dirs-g87` | 충족 |

## 6. C5 `_stage3_preflight` (`src/fitting.py:1386`) / `_prepare_stage3` (`:1431`)

실경로: `run_fit` → `_assert_fit_authorized` (`:1688`, C8) → `_stage3_preflight` (`:2083`) → … → `_prepare_stage3`. 양성: `G84::test_g84_n3_03_a_valid_v6_plan_reaches_the_prepared_state_and_legacy_halfcell_is_untouched` · `w04`.

| # | 키 | 비교 위치 | 기대값 출처 | 음성 node · 증인 | 변이 | 상태 |
|---|---|---|---|---|---|---|
| C5-1 | envelope 유효 (preflight) | `:1403` | C1 | `G82::test_g82_n2_03_the_consumer_refuses_to_start_on_a_design_envelope_profile_mismatch` (b) stub philox — `match="bank profile"` · fits 미생성 | (C1 위치 변이가 성질 담당) | 충족 |
| C5-2 | `protocol_generation` (두 자리) | `:1406` · `:1448` | 상수 v6 | `G82::test_g82_n3_01_a_plan_declaring_v5_does_not_start_the_v6_path` — `match="protocol_generation"` | MULTI `the-v6-path-refuses-another-plan-generation-g82` | 충족 |
| C5-3 | reference == grid | `:1409` | 정책 | `G84::test_g84_n3_04_a_plan_that_itself_claims_halfcell_is_still_refused_before_the_self_fit` — `match="reference='grid'"` · sentinel 0 | `preflight-refuses-non-grid-reference-before-self-fit-g84` | 충족 |
| C5-4 | `inputs.reference` ↔ 실행 reference | `:1413` | 실행 인자 | `G84::test_g84_n3_02_plan_reference_must_equal_the_run_reference` — `match="reference"` · sentinel 0 | `preflight-binds-the-plan-reference-g84` | 충족 |
| C5-5 | `source_digest` ↔ 실행 `source_digest()` | `:1415` | 실행 코드 재계산 | `G84::test_g84_n3_00_a_plan_with_another_source_digest_is_refused_before_any_fitting` — `match="source_digest"` | `preflight-binds-the-plan-source-digest-g84` | 충족 |
| C5-6 | `inputs.base_config_digest` ↔ staged closure | `:1422` (null) · `:1425` | staged closure 재계산 | `G84::test_g84_n1_01_…` (null) · `G84::test_g84_n1_02_a_truncated_or_padded_hex16_is_not_the_closure` · `G84::test_g84_n1_03_a_plan_sealed_on_a_changed_parent_does_not_start_on_the_real_closure` — `match="base_config_digest"` | `v6-plan-closure-must-match-the-staged-closure-g84` (`:1425`; null 분기 `:1422` 는 변이 없음) | 충족 |
| C5-7 | objectives 순서 ↔ `objective_order` | `:1457` | envelope | 없음 → **k10-C5[objective_order]** | 신규 -g92 | 보강 |
| C5-8 | 문맥 설계 digest ↔ `pairing_design_sha256` | `:1460` | 설계 재계산 | `G87::test_s04_06_a_context_that_disagrees_with_the_plan_is_still_refused_by_prepare_stage3` — `"pairing_design_sha256"` · sentinel 0 | **없음 → 신규 -g92** (기존 node 로 관측) | 충족 (위치 변이 없음) |
| C5-9 | 설계 `parameter_order` ↔ `parameter_order_sha256` | `:1462` | 설계 재계산 | 없음 → **k10-C5[parameter_order_sha256]** | 신규 -g92 | 보강 |
| C5-10 | 설계·envelope bank profile | `:1466` | 구현 profile | `n2_03` (a) — `match="bank profile"` | `the-consumer-checks-the-profile-before-start-g82` | 충족 |
| C5-11 | `parameter_order` == `PARAM_NAMES` | `:1470` | optimizer 벡터 상수 | `G81::test_g81_s08_parameter_order_is_the_optimizer_vector_and_the_map_reads_solution_columns` — `match="parameter_order"` | `design-order-is-the-optimizer-vector-g81s` | 충족 |
| C5-12 | `bank.n_params` · bounds 길이 | `:1473` | optimizer 벡터 길이 | 없음 → **k10-C5[n_params]** (도달성 미확인 — `check_bank_profile` 이 n_params 를 보면 `:1466` 이 먼저 막는다; 불확실) | 신규 -g92 | 보강 |
| C5-13 | `bank.exact_bounds_sha256` ↔ 실제 lb/ub | `:1479` | bounds 재계산 | 없음 → **k10-C5[exact_bounds]** | 신규 -g92 | 보강 |
| C5-14 | `inputs.curves_sha256` ↔ staging curves 바이트 | `:1483` | 바이트 재계산 | 없음 → **k10-C5[curves_sha256]** | 신규 -g92 | 보강 |
| C5-15 | roster ↔ 실제 조건 집합 | `:1499` | 조건 → roster 재구성 | `G81::test_g81_w06_stage3_run_refuses_a_roster_that_does_not_match_the_curves_and_p_ini_edges` — `match="roster"` | **없음 → 신규 -g92** | 충족 (위치 변이 없음) |
| C5-16 | warm consumer 의 provider run 존재 | `:1513` | 문맥 | `G81::test_g81_s06_the_warm_supply_path_runs_end_to_end_and_its_x0_is_rederived` ① — `match="provider"` | **없음 → 신규 -g92** (C4 `:1378` 과 다른 자리) | 충족 (위치 변이 없음) |
| C5-17 | provider run 재생성 map sha ↔ edge | `:1518` | 재생성 바이트 | `s06` ② — `match="다시 만든 map sha"` · fits 미생성 | `warm-map-is-regenerated-and-compared-g81s` | 충족 |
| C5-18 | writer `spec_block.provider_edges_sha256` 정의 | `:1545` | `digest(env["provider_edges"])` (`preserve.py:6656`) | 없음 → **k07** (warm edge 계획 · RED 예상) | `provider-edges-sha-has-one-definition-g92` (안) | 보강 |

## 7. C6 `provider_x0` (`src/fitting.py:558`)

실호출: writer `_stage3_candidates` (worker) · validator `src/io.py:1778`. 양성: `G81::test_g81_n3_02_consumer_rejects_wrong_fits_map_combination_and_unsealed_maps` 첫 호출 (edge_ok) · `s06`.

| # | 키 | 비교 위치 | 기대값 출처 | 음성 node · 증인 | 변이 | 상태 |
|---|---|---|---|---|---|---|
| C6-1 | map 바이트 sha ↔ `edge.solution_map_sha256` | `:568` | 바이트 재계산 | `n3_02` tampered · respaced — `match="봉인 전 소비"` | `solution-map-is-consumed-only-when-sealed-g81` | 충족 |
| C6-2 | header `schema` | `:573` | 상수 | 없음 → **k11-C6[schema]** | 데이터만 | 참고 (형식) |
| C6-3 | header `provider_objective` ↔ edge | `:575–580` | edge (계획) | `G81::test_g81_n3_03_…` 둘째 (`edge provider_objective=OBJS[1]`) — `pytest.raises(ValueError)` **이유 미단언** → **k11-C6[provider_objective]** | 루프 하나에 **신규 -g92** 1 | 보강 |
| C6-4 | header `provider_artifact_sha256` ↔ edge | `:575–580` | edge | 없음 (`n3_02` 의 map B 반례는 `:568` 바이트 sha 가 먼저 막는다) → **k11-C6[provider_artifact_sha256]** (edge 의 solution_map_sha256 은 실제 바이트로 맞춤) | 같은 루프 변이 | 보강 |
| C6-5 | header `provider_protocol_sha256` ↔ edge | `:575–580` | edge | 없음 (이 이유는 writer 변이 `map-protocol-is-measured-from-the-run-spec-g81s` 의 관측 증인 `mutation_replay.py:6307` 에만 나온다) → **k11-C6[provider_protocol_sha256]** | 같은 루프 변이 | 보강 |
| C6-6 | header `parameter_order` ↔ 설계 order | `:581` | 설계 | 없음 → **k11-C6[parameter_order]** | 신규 -g92 | 보강 |
| C6-7 | `cond_id` 존재 (no-warm 전환 금지) | `:584` | 계획 roster | `n3_03` — `match="c9"` | **없음 → 신규 -g92** | 충족 (위치 변이 없음) |
| C6-8 | bounds (clip 금지) | `:591` | run_spec bounds | `n3_03` — `match="bounds|경계|밖"` | `provider-x0-is-not-clipped-g81` | 충족 |

## 8. C7 validator `_stage3_checks` (`src/io.py:1862`) — `run_spec.stage3` 16 키 (G92-N3 분할)

실경로: `validate_provenance` (`:2053`) → `:2151`. 양성: `w04` (`stage3_schema` · `stage3_planned_envelope` · `execution_record` · `candidate_map` · `candidate_ids_결속` 통과) · `G82::test_g82_n3_00_a_v6_run_links_sig_plan_record_and_row_generations` · `G85::test_g85_m00_a_real_leaf_to_parent_run_binds_both_members`.

**재서명 helper 는 이미 있다:** `tests/test_gate85_closure_members.py:69` `_resign` (manifest `run_signature` · fits `run_sig` · fits 봉인) + `:86` `_only_this_check_fails` (실패 검사가 **정확히 하나**). 조사 문서 §16-2 f 의 "run_signature 재서명 helper 만 새로" 는 재사용으로 바꿀 수 있다. 기존 G81/G82/G84 위조 node 는 재서명하지 않아 `run_signature_재계산` 도 함께 떨어진다 (예: `the-validator-rebuilds-the-closure-from-snapshots-g84` 관측 증인 `"['run_signature_재계산']"`) — 그래서 **검사 이름 단언**으로만 키별 증거가 된다.

### 8-a. 기존 helper (`stage3_axis_from_envelope`) 투영 키 — 새 비교 (k05 · RED 예상)

| # | 키 | 지금 | 기대값 출처 (구현 후) | 음성 node | 변이 | 상태 |
|---|---|---|---|---|---|---|
| C7-a1 | `parameter_order_sha256` | s3 사본 대조 없음 (env 만 `:1686`) | `stage3_axis_from_envelope(env)` | **k05[parameter_order_sha256]** | `stage3-run-spec-is-derived-per-key-g92` (투영 루프 1) | 보강 |
| C7-a2 | `roster_sha256` | 없음 (`:1980,:2001` 은 record·재구성 ↔ env) | 같음 | **k05[roster_sha256]** | 같음 | 보강 |
| C7-a3 | `provider_edges_sha256` | 없음 · **정의도 다름** (`fitting.py:1545` json.dumps vs `preserve.py:6656` canonical) | 같음 | **k05[provider_edges_sha256]** — **k07 먼저** (안 그러면 정상 warm run 을 새 루프가 거부) | 같음 | 보강 |
| C7-a4 | `arm` | 없음 | 같음 | **k05[arm]** | 같음 | 보강 |
| C7-a5 | `stage` | 없음 | 같음 | **k05[stage]** | 같음 | 보강 |
| C7-a6 | `candidate_mode` | 없음 (재유도는 `env["stages"][0]`) | 같음 | **k05[candidate_mode]** | 같음 | 보강 |

helper 와 겹치지만 **이미 기존 위치가 대조하는 두 키** (`planned_id` `:1883` · `pairing_design_sha256` `:1684`) 는 새 투영 루프에서 세지 않는다 (8-c). 새 루프가 그 둘까지 비교하면 루프 변이에서 그 두 node 는 **기존 위치 때문에 생존**한다 — G92-N3 대로 기존 검사를 약화하지 말고 루프 변이 EXPECT 를 k05 6 node 로 한정한다.

### 8-b. env 직접 비교 키 (k05 · RED 예상)

| # | 키 | 기대값 출처 | 음성 node | 변이 | 상태 |
|---|---|---|---|---|---|
| C7-b1 | `bank_version` | `env["bank"]["version"]` | **k05[bank_version]** | `stage3-run-spec-env-direct-keys-g92` (공통 루프로 구현하면 8-a 변이와 **하나로 합침** · 독립 커버리지로 세지 않음) | 보강 |
| C7-b2 | `budget_by_objective` | `env["stages"][0]` | **k05[budget_by_objective]** | 같음 | 보강 |
| C7-b3 | `warm_provider_map` | `env["stages"][0]` | **k05[warm_provider_map]** | 같음 | 보강 |

(요청문 §2-b · 조사 문서 :227·:259 의 "env 직접 4 키" 는 틀렸다 — `exact_bounds_sha256` 은 8-c 의 기존 3자 재계산이다. G92-N3 정정 그대로.)

### 8-c. 기존 독립 재계산 키

| # | 키 | 비교 위치 | 기대값 독립 출처 | 음성 node · 증인 | 변이 | 상태 |
|---|---|---|---|---|---|---|
| C7-c1 | `planned_id` | `:1883` | `digest(planned_envelope)` | **s3 단독 변조 node 없음** — `G82::_forge_stage3` (`:51`) 은 planned_id 를 **항상 재유도**한다 → **k06[planned_id]** (GREEN 예상) | **없음 → 신규 -g92** | 보강 |
| C7-c2 | `planned_envelope` (객체) | `:1881–1885` + 재유도 입력 | 내부 유효성 · digest 사슬 | `G82::test_g82_n2_04_the_validator_refuses_a_forged_design_or_envelope_profile` (env generator · 사슬 재봉인 → `stage3_planned_envelope` + `"bank profile"`) · `n3_02` (세대) · `G84::test_g84_n1_04_…` (inputs.base_config_digest) | `the-validator-checks-the-profile-g82` 외 | 충족 (단 독립 출처는 **run_dir 안 사본뿐** — 원장 계획과의 대조는 아래 이월) |
| C7-c3 | `pairing_design_sha256` | `:1684` (재계산 == s3 == env) | 설계 본체 재계산 | **s3 단독 node 없음** (`_forge_stage3 design_mutate` 는 s3·env 를 함께 고친다) → **k06[pairing_design_sha256]** | **없음 → 신규 -g92** | 보강 |
| C7-c4 | `pairing_design` (본체) | `:1676` 재계산 입력 · `:1683` profile | 구현 profile · 후보 재유도 | `n2_04` 전반 (설계 dtype · 재봉인) — `"후보_재유도"` + `"bank profile"` | `the-validator-checks-the-profile-g82` | 충족 |
| C7-c5 | `exact_bounds_sha256` | `:1696` (run_spec.bounds 재계산 == s3 == env) | `run_spec.bounds` 재계산 | **없음** → **k06[exact_bounds_sha256]** | **없음 → 신규 -g92** | 보강 |
| C7-c6 | `base_config_closure_sha256` | `:2047` | 봉인 스냅샷 바이트 재계산 | `G84::test_g84_n1_04_the_validator_rebuilds_the_closure_from_the_sealed_snapshots` — s3 · env 를 같은 위조값으로 · `"base_config_결속" in v["fail"]` | `the-validator-rebuilds-the-closure-from-snapshots-g84` | 충족 (k06 은 s3 단독 대조로만) |
| C7-c7 | `base_config_closure_keys` | `:2023–2034` | `run_spec.base_config` extends 독립 유도 | `G85::test_g85_m01_…` · `m02` · `m03` (`_resign` 포함 · **실패 검사가 정확히 base_config_결속 하나**) · `m04` (중복) | `closure-members-are-derived-not-trusted-g85` · `closure-missing-members-…` · `closure-extra-members-…` · `closure-member-keys-are-unique-g85` | 충족 |
| C7-c8 | `stage3` 키 집합 닫힘 | `:1873` (missing-only) | `_STAGE3_SPEC_KEYS` | 없음 → **k03** (RED 예상) | `stage3-run-spec-keys-are-closed-g92` (안) | 보강 |
| C7-c9 | `candidate_map.json` 최상위·항목 닫힘 + 자료형 (G92-N2) | `:1927–1931` | `{schema, entries}` · 항목 7 키 | 없음 → **k04** (RED 예상) — 관찰: cm 이 list 면 `:1929` `cm.get` 이 `AttributeError` (except 는 ValueError·OSError 뿐) · 비-dict 항목은 `_stage3_rederive :1715` `m.get` 에서 같은 위험 · `stage3_planned_envelope` 실패 뒤에도 `:1961` 이 그 env 로 재유도를 계속 부른다 【정적 · 미실행】 | `candidate-map-keys-are-closed-g92` (안) | 보강 |

### 8-d. C7 행 단위 `_stage3_rederive` (`src/io.py:1660`) 및 record ↔ 행

| # | 키 | 비교 위치 | 기대값 독립 출처 | 음성 node · 증인 | 변이 | 상태 |
|---|---|---|---|---|---|---|
| C7-r1 | `pair_group_id` (행) | `:1730` | 행 좌표 + 설계 재계산 | 없음 → **k12-C7r[pair_group_id]** (행만 · `_reseal_fits` · `_resign`) | 신규 -g92 | 보강 |
| C7-r2 | `bank_id` (행) | `:1738` | 봉인 bank 재생성 | 없음 → **k12-C7r[bank_id]** | 신규 -g92 | 보강 |
| C7-r3 | `warm_provider_objective` (행) | `:1747` | env warm map | 없음 (warm fixture `G81::_warm_context` 필요) → **k12-C7r[warm_provider_objective]** | 신규 -g92 | 보강 |
| C7-r4 | (i, source, bank_index) | `:1751` | `candidate_plan(mode,B,provider)` | `s02` (c) swap · (d) reorder — `"후보_재유도" in fail` · (d) `"계획 candidate_plan"` | `validator-rederives-the-candidate-plan-g81s` | 충족 |
| C7-r5 | x0 | `:1785` | base=bounds.init · random=bank 행 · warm=봉인 map 재소비 | `s02` (a) · `s06` ③ — `"후보_재유도" in fail` (이유 문자열 미단언 · 변이 증인이 위치 의존을 보임) | `validator-rederives-every-x0-g81s` | 충족 |
| C7-r6 | `candidate_id` | `:1789` | `DW.candidate_id` 재유도 | `s02` (b) — map·행 함께 (집합 대조 `candidate_ids_결속` 통과 단언 후 `후보_재유도` 실패) | `validator-rederives-every-candidate-id-g81s` | 충족 |
| C7-r7 | restart 행 ↔ map (source·id·bank_index·warm) | `:1793` | 후보 map | 없음 → **k12-C7r[restart_row]** (행의 `warm`/`bank_index` 만) | 신규 -g92 | 보강 |
| C7-r8 | `warm_started` ↔ 후보 구성 | `:1763` | candidate_plan | 없음 → **k12-C7r[warm_started]** | 신규 -g92 | 보강 |
| C7-r9 | 봉인 provider map 사본 sha ↔ edge | `:1708` | env edge | 없음 → **k12-C7r[provider_map_copy]** | 신규 -g92 | 보강 |
| C7-r10 | 행 없는 map (조건, objective) | `:1797` | fits 행 집합 | 없음 → **k12-C7r[orphan_map_key]** | 데이터만 | 보강 |
| C7-r11 | `realized.by_objective`·`n_obs_observed`·`provider_consumed` ↔ 행 재계산 | `:1976` | fits 행 | `G81::test_g81_s03_the_validator_recounts_realized_counts_from_the_rows` — `"실현_재계산" in fail` | `validator-recounts-realized-counts-g81s` | 충족 |
| C7-r12 | `realized.n_candidates` ↔ map 항목 수 | `:1978` | map | 없음 → **k12-C7r[n_candidates]** | 데이터만 | 보강 |
| C7-r13 | 관측 roster 재구성 ↔ 계획·record | `:2001,:2004` (·`:1980`) | 봉인 curves 스냅샷 | `G82::test_g82_n1_01_…` · `n1_02` · `n1_03` · `n1_04` | `observed-roster-compares-rows-to-the-sealed-inputs-g82` · `record-roster-is-compared-to-the-rebuilt-roster-g82` · `a-missing-sealed-snapshot-is-a-failure-g82` (`:1980` 단독 위치는 변이 없음) | 충족 |
| C7-r14 | 세대 연결 (sig · 계획 · record · 행) | `:1907–1920` | 상수 v6 | `G82::test_g82_n3_02_the_validator_refuses_plan_and_record_that_agree_on_v5_under_sig6` — `"계획 protocol_generation"` · `"record protocol_generation"` · `"record_generation"` | `the-validator-links-the-plan-generation-g82` · `…-record-generation-g82` · `…-row-generations-g82` | 충족 |

## 9. C8 `_assert_fit_authorized` (`src/fitting.py:1254`)

양성: `G87::test_s02_04_a_matching_v3_plan_and_context_reach_claim_issuance`. 비-smoke 경로만 (smoke namespace 면 면제 `:1269`).

| # | 키 | 비교 위치 | 기대값 출처 | 음성 node · 증인 | 변이 | 상태 |
|---|---|---|---|---|---|---|
| C8-1 | spec 버전 분기 (v2 / v3 / 모름) | `:1289–1309` | 원장 `leg_spec_version` | `s02_01` (`"legacy"` · `"leg_spec_version 3"` · sentinel 0) · `s02_02` (`"leg_spec_version 2"`) · `s02_03[*]` (raise 만) · `s02_05` (`"계약 (2 · 3) 밖"`) | `v3-plan-refuses-legacy-fallback-g87` · `v2-plan-refuses-a-stage3-context-g87` · `unknown-spec-version-is-not-authorized-g87` | 충족 |
| C8-2 | 문맥에 `PlannedLegV4` 존재 | `:1301` | — | 없음 → **k10-C8[no_planned]** | 데이터만 | 보강 |
| C8-3 | 문맥 계획에서 유도한 v3 축 ↔ 원장 `run_spec_digest` | `tools/preserve.py:7441` (`_claim_planned_leg`) | 원장 승인 spec | **v3 node 없음** (s02_04 양성뿐) → **k10-C8[other_plan]** — 대표 1 node: 다른 자기일관 계획 문맥 · 이유 `"run_spec 이 승인된 계획과 다르다"`. **키별 독립 node 는 성립하지 않는다**: envelope 의 어떤 키를 바꿔도 `planned_id = digest(env)` 가 함께 움직여 같은 digest 비교 하나로 간다 | 기존 `claim-seals-the-run-spec` (같은 위치 · node `TP::test_the_claim_seals_the_exact_run_spec`, v2) — **-k 확장** 필요 시 증인 변경 사전 보고 | 보강 |
| C8-4 | 재개 경로 claim `run_spec_digest` ↔ 지금 spec | `tools/preserve.py:4192` | claim 봉인 | 이 문구의 시험·변이를 찾지 못함 (grep 기준 — **불확실**, 다른 이름으로 덮였을 수 있음) | — | **이월** (v2·v3 공통 기존 경로 · 묶음 6 의 v6 linkage 밖 · 별도 확인 항목) |

## 10. C9 `finalize_leg` fit-only (`tools/preserve.py:8929`)

양성: `G88::test_f01_01_a_v6_fit_only_leg_runs_records_and_finalizes` · `G89::test_d01_a_durable_fit_receipt_is_carried_into_the_ledger_record_as_recorded`. finalize 는 `run_spec.stage3`/envelope 를 읽지 않는다 (claim 의 run_spec_digest 와 fit 입력 결속만) — stage3 키 행은 해당 없음.

| # | 키 | 비교 위치 | 기대값 출처 | 음성 node · 증인 | 변이 | 상태 |
|---|---|---|---|---|---|---|
| C9-1 | phase 집합 재유도 | `:9126` | 계획 spec 에서 재유도 | `G88::test_f00_04_a_v2_claim_with_an_injected_phase_set_can_not_be_finalized_fit_only` (raise 만) | `finalize-rederives-the-phase-set-g88` | 충족 |
| C9-2 | `consumed.external_input` ↔ 계획 `fit.in_digest` | `:9136` | 원장 계획 | `G88::test_f03_03_finalize_refuses_an_external_input_other_than_the_plan` — `"in_digest" or "external_input"` | `finalize-compares-the-external-input-with-the-plan-g88` | 충족 |
| C9-3 | `receipt.input_package_digest` ↔ `consumed` | `:9138` | consumed | `G88::test_f03_06_a_self_consistent_binding_forgery_is_refused[receipt_package_tampered]` · `G89::test_d03_a_self_consistent_receipt_forgery_after_recording_is_refused_by_the_consumer_binding` — `"소비한 밖 입력"` | `finalize-binds-the-receipt-package-to-the-consumer-g88` · `finalize-still-binds-the-receipt-package-to-the-consumer-g89` | 충족 |
| C9-4 | `receipt.inputs` (닫힘 · hex64 · 묶음 재계산) | `:9146` → `:6721` | `PHASE_INPUT_KEYS` · `input_package_digest` | `G89::test_d02_finalize_refuses_a_fit_receipt_whose_inputs_changed_after_recording[inputs_deleted|inputs_extra_key|inputs_value_not_hex|inputs_value_other_hex64]` — why 문자열 · 원장/claim 바이트 불변 | `finalize-rechecks-the-durable-input-binding-g89` | 충족 |

## 11. C11 `check_roster` / `check_provider_edges` (`tools/design_wire.py:768` / `:830`)

실호출: roster — `roster_sha256` `:800` · `roster_from_conditions` `:824`; edge — `check_envelope_v4` `tools/preserve.py:3256`. 양성: `G81::test_g81_n1_04_roster_rejects_duplicate_obs_key_cross_seed_and_cond_id_collision` (good) · `G81::test_g81_n3_04_provider_edges_must_match_the_warm_map_precede_the_consumer_and_not_be_cyclic` 첫 단언. 기존 두 node 는 대부분 **거부(truthy)만** 단언한다 (단언 메시지는 실패 시 출력일 뿐 이유 대조가 아님) → 이유 단언 보강을 k09-C11 하나의 parametrize 로.

| # | 키 | 비교 위치 | 기대값 출처 | 음성 node · 증인 | 변이 | 상태 |
|---|---|---|---|---|---|---|
| C11-1 | obs_key 에 objective 금지 · 필드 닫힘 | `:754` | `OBS_KEY_FIELDS` | `n1_04` objk (truthy) → **k09-C11[objective_in_key]** | 데이터만 | 보강 |
| C11-2 | obs_key 중복 | `:780` | roster 자체 | `n1_04` dup (truthy) → **k09-C11[dup_obs_key]** | 신규 -g92 | 보강 |
| C11-3 | cond_id 충돌 | `:785` | roster 자체 | `n1_04` col (truthy) → **k09-C11[cond_collision]** | 신규 -g92 | 보강 |
| C11-4 | `pair_group_id` ↔ `obs_key.pair_group_id` | `:763` | 같은 항목 | 없음 → **k09-C11[pg_mismatch]** | 신규 -g92 | 보강 |
| C11-5 | warm arm 의 null 금지 (no-warm 전환) | `:850` | arm registry · order | `n3_04` 마지막 — 증인 `"…no-warm 으로 전환 금지"` | `warm-required-slot-is-not-turned-into-no-warm-g81` | 충족 |
| C11-6 | warm-off arm 에 provider | `:853` | arm registry | 없음 (`n3_04` "warm-off arm" 사례는 wm 이 전부 None 이라 `:874` 가 발화) → **k09-C11[warm_off_provider]** | 신규 -g92 | 보강 |
| C11-7 | provider ∈ order · self · 역방향 | `:855–860` | order | `n3_04` 역방향 (truthy) → **k09-C11[order]** | 신규 -g92 | 보강 |
| C11-8 | edge `stage` (p_ini 거부) | `:869` | 계약 상수 | `n3_04` p_ini (truthy) → **k09-C11[edge_stage]** | 데이터만 | 참고 (정책) |
| C11-9 | edge `arm` ↔ arm | `:873` | envelope arm | `n3_04` warm-off 사례가 사실상 이 위치만 발화 (truthy) → **k09-C11[edge_arm]** | 신규 -g92 | 보강 |
| C11-10 | edge consumer ∈ order | `:876` | order | 없음 → **k09-C11[edge_consumer]** | 신규 -g92 | 보강 |
| C11-11 | edge provider ↔ `warm_provider_map[consumer]` | `:878` | envelope warm map | `n3_04` "self" (truthy) → **k09-C11[edge_vs_map]** | 신규 -g92 | 보강 |
| C11-12 | consumer edge 중복 | `:880` | edge 목록 | 없음 → **k09-C11[dup_edge]** | 신규 -g92 | 보강 |
| C11-13 | edge sha 3 필드 hex64 | `:884` | 형식 | 없음 | 데이터만 | 참고 (형식) |
| C11-14 | warm map 이 말하는 consumer 의 edge 누락 | `:888` | envelope warm map | `n3_04` 빈 edges (truthy) → **k09-C11[missing_edge]** | 신규 -g92 | 보강 |

---

## 12. (A) 부재 고정 — 구 필드 (`pairing_design_id` · `inference_status`) · k01/k02/k03/k04

| 자리 | 닫힘 위치 | 기존 음성 | 신규 | 기존 변이 |
|---|---|---|---|---|
| 정상 v6 산출 전체 (재귀 부재) | — | — | k01 (GREEN) | — |
| 설계 spec | `design_wire.py:300–318` | (label 명시 거부만) | k02[design] | — |
| `planned-leg/v4` envelope (+ stage·bank·inputs·roster 블록) | `preserve.py:3180,3204,3231,3247,3259` | 없음 | k02[envelope] | 없음 |
| v3 승인 spec `stage3` 축 | `preserve.py:6661` | `G87::test_s01_02_…[extra]` (`budget` 추가) | k02[v3_axis] (구 이름으로) | `stage3-axis-keys-are-closed-g87` (`-k s01_02` — k02 는 선택자 밖 · 연결하려면 -k 확장) |
| 계획 index 항목 | `preserve.py:3942–3961,6270–6272` | — | k02[index_entry] | (확인 못 함) |
| `stage3_context` | `preserve.py:6177` | — | k02[stage3_context] | — |
| execution record v1/v2 · realized | `preserve.py:3297,3318,3326` | `n1_03` `extra` (truthy · `:3297` 단독 발화) · `g84_n4_01` mixed | k02[record] · k02[realized] | `record-schema-dispatch-is-closed-g84` 등 |
| restart 행 (v6 10 키) | `io.py:813,829` | `G81::test_g81_n2_05_…` (`extra` → `_restart_ok_v6 False`) | k02[restart_row] | `v6-random-row-needs-a-bank-index-g81` (다른 성질) |
| roster 항목 · provider edge | `design_wire.py:751,865` | — | k02[roster] · k02[edge] | — |
| **`run_spec.stage3`** (새로 닫음) | `io.py:1873` | — | **k03 (RED)** | 신규 -g92 |
| **`candidate_map.json`** (새로 닫음 + 자료형) | `io.py:1927–1931` | — | **k04 (RED)** — 누락 · 두 구 이름 · 제3 임의 키 · list/null 컨테이너 · 비-dict 항목 · int 자리 bool/str | 신규 -g92 |

---

## 13. 새 node 제안 (조사 문서 §16-3 의 k00–k09 정정 · 새 파일 `tests/test_gate92_stage4_linkage.py`)

| node | 내용 | consumer | RED 예상 | 결함 증거로 세나 |
|---|---|---|---|---|
| k00 | 정상 v6 · v5 대조 (골든) | C7 · C2 · C3 | GREEN | 아니오 |
| k01 | 부재 재귀 | 산출 전체 | GREEN | 아니오 |
| k02[자리] | 닫힌 자리 9 에 구 필드 | C1 · C2 · C3 · C7 · C11 · 설계 | GREEN | 아니오 |
| **k03** | run_spec.stage3 닫힘 (구 필드 + `_resign`) | C7 | **RED** | 예 |
| **k04[…]** | candidate_map 닫힘 + 자료형 (G92-N2) | C7 | **RED** (일부는 `AttributeError` 로 떨어질 수 있음 — 따로 셈) | 예 |
| **k05[9]** | s3 사본: 투영 6 (`parameter_order_sha256` · `roster_sha256` · `provider_edges_sha256` · `arm` · `stage` · `candidate_mode`) + env 직접 3 (`bank_version` · `budget_by_objective` · `warm_provider_map`) | C7 | **RED ×9** | 예 |
| k06[5] | 기존 재계산: `planned_id` · `pairing_design_sha256` · `exact_bounds_sha256` (s3 단독 — 처음 생기는 키별 node) · `base_config_closure_sha256` · `_keys` (대조) | C7 | GREEN | 아니오 (앞 셋은 신규 위치 변이로 "무는가" 증명) |
| **k07** | warm edge 계획 → `run_spec.stage3.provider_edges_sha256 == stage3_axis_from_envelope(env)[…]` | C5 writer → C7 · C3 · C8 | **RED** | 예 |
| k08[8] | 계획 index: `pairing_design_sha256` · `parameter_order_sha256` · `bank.{generator,version,length,n_params,exact_bounds_sha256}` · `stage` (이유에 키 이름 단언) | C3 | GREEN | 아니오 |
| k09[…] | 단위 수준: C1 (bank_length · budget_keys · warm_map_domain · stage_p_ini · fmt-*) · C2 (leg_id · source_digest · protocol_generation · total · source_le_plan · prefix · n_obs · arith-*) — **record_digest 재계산 필수** · C4 (parameter_order_sha256 · unknown_leg) · C11 (11 키) | C1 · C2 · C4 · C11 | GREEN | 아니오 |
| k10[…] | 시작 전: C5 (objective_order · parameter_order_sha256 · n_params · exact_bounds · curves_sha256) · C8 (other_plan · no_planned) — sentinel `_fit_one` 0 · fits 미생성 단언 | C5 · C8 | GREEN (n_params 도달성 불확실) | 아니오 |
| k11[…] | C6 header (schema · provider_objective · provider_artifact_sha256 · provider_protocol_sha256 · parameter_order) — edge 의 solution_map_sha256 은 실제 바이트로 맞춤 | C6 | GREEN | 아니오 |
| k12[…] | C7 행: pair_group_id · bank_id · warm_provider_objective · restart_row · warm_started · provider_map_copy · orphan_map_key · n_candidates — `_reseal_fits` + `G85._resign` + `_only_this_check_fails` 형 단언 | C7 | GREEN | 아니오 |

## 14. 변이 계획 요약

| 종류 | 수 | 내용 |
|---|---|---|
| 조사 문서 §16-4 의 새 위치 | 4–5 | k03 · k04 · k05 투영 루프 · k05 env 직접 (공통 루프면 합쳐 1) · k07 |
| 기존 재계산 위치인데 변이 없음 (k06 이 첫 증인) | 3 | C7 `:1883` (planned_id) · `:1684` (pairing_design_sha256) · `:1696` (exact_bounds_sha256) |
| 기존 node 는 있으나 위치 변이 없음 (변이만 추가 · 기존 node 로 관측) | 4 | C5 `:1460` · `:1499` · `:1513` · C6 `:584` (부분 4 는 선택) |
| 새 node 와 함께 오는 위치 | 35 | C1 4 · C2 7 · C4 1 · C5 5 · C6 2 (헤더 루프 1 · order 1) · C7 행 6 · C11 10 — "데이터만" 제안 자리 (형식·산술·정책 · C4-1 · C7-r10/r12 · C8-2 · C11-1) 는 제외 |
| 기존 변이의 **-k 확장** (증인 집합 변경 → 사전 보고) | 2 | `stage3-axis-is-derived-not-copied-g87` (`s03_05` → `+ k08`) · `claim-seals-the-run-spec` (`+ k10-C8`) |

등록부 `_check` 는 실패 node 집합 == EXPECT 를 요구하고 선택자는 `-k` 이므로 새 파일의 node 는 기존 선택자에 **우연히 걸리지 않는 한** 기존 EXPECT 를 바꾸지 않는다. 현재 맨 단어 선택자 (`leg_id` · `source_digest` · `generation` · `inputs_*`) 는 모두 `s03_04 and …` / `f03_0x and …` 결합이라 위험은 낮다 — 구현 시 `--list` 와 `-k` 수집으로 확인.

## 15. 이월 · 제외 (닫혔다고 주장하지 않음)

| 항목 | 좌표 | 이유 |
|---|---|---|
| **이월** C8 재개 경로 claim spec 대조 | `tools/preserve.py:4192` | v2·v3 공통 기존 경로 · v6 linkage 밖 · 시험/변이 존재 여부 불확실 |
| **이월** C7 `run_spec.stage3.planned_envelope` ↔ **원장 승인 계획** | validator 는 원장을 읽지 않는다 (`io.py:1862–2050`) | 산출 안 사본만 대조 (planned_id = digest(사본) 은 자기참조). 원장 결속은 C8 (실행 전) · finalize 의 run_spec_digest 몫 — 산출 단독 검증으로 "승인된 계획의 산출" 을 보이는 것은 묶음 6 밖 |
| **제외** `run_spec` 최상위 닫힘 | `src/io.py:2127–2143` | v5 와 공유하는 열린 집합 — 이번 변경에서 제외 |
| **제외** solution map header 닫힘 | writer `src/fitting.py:566–582` | consumer C6 은 4 header 필드만 `.get` 대조 — 추가 header 키는 통과한다 (바이트 sha 는 계획 edge 에 봉인). 닫힘은 주장하지 않음 |
| **제외** `LEG_PRESERVATION.yaml` 항목 닫힘 | `tests/test_docs_lint.py:2659–2665` | 운영 원장 v6 항목 자체가 승인 밖 |
| **제외** C10 | — | 조사 문서 §3.4 번호에 C10 이 없다 (C9 → C11). 빠진 consumer 인지 번호 건너뜀인지 확인 필요 |

## 16. 놀라운 점 · 정정 필요

1. **재서명 helper 가 이미 있다** — `tests/test_gate85_closure_members.py:69` `_resign` · `:86` `_only_this_check_fails`. 조사 문서 §16-2 f 의 "run_signature 재서명 helper 만 새로" 는 재사용으로 정정.
2. **C2 의 `n1_03` 하위 사례 다수가 마스킹** — `record_digest` 미재계산이라 `source_digest` · count 반례가 키별 증거가 아니다. 요청문 F 표 · 조사 문서 k09 는 C2 를 "대부분 통과 (기존)" 으로 봤는데, 키별로는 `planned_id` 만 기존 증거다.
3. **C7 `planned_id` · `pairing_design_sha256` · `exact_bounds_sha256` 은 "기존 대조" 인데 s3 단독 변조 node 가 0** — `_forge_stage3` 가 항상 사슬을 다시 맞춘다. k06 은 "대조" 가 아니라 이 세 키의 **첫** 키별 node 이고, 그 위치에는 변이도 없다.
4. **k05 투영 루프와 기존 위치의 중복** — 새 루프가 `planned_id` · `pairing_design_sha256` 까지 비교하면 그 두 node 는 루프 변이에서 생존한다. 루프 EXPECT 를 k05 의 6 키로 한정 (G92-N3).
5. **k07 이 k05 보다 먼저** — 정의가 다른 채로 k05 루프를 넣으면 정상 warm run 을 거부한다 (`fitting.py:1545` vs `preserve.py:6656`).
6. **C8 은 키별 독립 node 가 원리상 불가** — envelope 의 모든 키가 `planned_id` 로 접힌다. 대표 node 1 + 기존 위치 변이 연결로 충분하다는 판단을 §16 에 적어야 한다.
7. **C6 header 4 키 대조에 변이·이유 단언 node 가 모두 없다** — 유일한 흔적은 writer 변이의 관측 증인 (`mutation_replay.py:6307`).
8. **C11 은 거부만 단언** — 이유 대조가 없는 truthy 단언 12 곳 · 위치 변이 1 (`:850`).

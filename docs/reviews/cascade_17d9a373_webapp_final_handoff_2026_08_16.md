# Cascade webapp final handoff — 17d9a373

> Frozen source: `origin/claude/friendly-meitner-lldvar@17d9a373`
> Release boundary: audit/status GO · current ranking/Pareto/endpoint/winner NO-GO

## 1. 헤드라인 상태를 네 층으로 분리

한 개의 `G3 complete` 배지로 덮지 않는다.

| state | current value | allowed meaning |
|---|---:|---|
| `phase_set_comparability` | `270/270` | candidate와 same-run host가 같은 pinned MP entry roster를 사용 |
| `operational_factorial_coverage` | `17/17 chain rows` | 11 recipe system에서 formula-level counterfactual 존재 |
| `structural_realization_validated` | `0/11` | actual parent structure/site/relaxation 검증 없음 |
| `approved_current_ranking` | `0` | selection/Pareto/endpoint/winner 공개 금지 |

표현 규칙:

- 허용: `phase-set comparable 270/270`
- 허용: `17/17 chain rows have formula-level operational contrasts across 11 recipe systems`
- 금지: `effect attribution closed`
- 금지: `11/11 species validated`
- 금지: `current G3 ranking approved`

## 2. 조성족은 provenance이지 causal label이 아님

Champion 270행은 `plain=253`, `chain=17`이다. `chain`을 한 개의 S→Cl intervention으로 렌더하지 않는다.

- `exact_transform=10`: same site, ΔLi=-1, ΔS=-1, ΔCl=+1
- `multi_transform=7`: B2O3×3, MoO3×2, WO3×2; site와 Li/P도 함께 변경
- `plain`도 host 대비 O/S, site, Li charge compensation이 함께 달라 `dopant effect`가 아님

Row-level 필수 표시:

- `composition_family`
- `composition_family_source`
- `matched_transform_status`
- `matched_plain_candidate`
- `contrast_scope`
- `composition_formula`와 가능한 경우 `composition_hash`
- `phase_set_id`

권장 `contrast_scope`:

- `primary_recipe_vs_host`
- `multi_intervention_recipe_vs_host`

## 3. 두 enrichment 비율은 같이 보여 주되 non-causal로 고정

| denominator | plain | chain | ratio |
|---|---:|---:|---:|
| all selected champion slots | 17/253 | 11/17 | 9.63× |
| variant-eligible 33 slots | 4/16 | 11/17 | 2.59× |

UI 계약:

- 두 비율을 같은 panel에 둔다.
- `post-selection descriptive association`을 값 옆에 상시 표시한다.
- combined-score maximum으로 사후 선택됐고 x-label이 independent replicate가 아님을 tooltip이 아니라 본문에 둔다.
- 어느 비율도 `Cl effect size`, `causal enrichment`, `success rate`로 부르지 않는다.

## 4. Matched 2×2 panel

원장: `db/properties/oxidation_matched_factorial.json`

정의:

- `H_plain = Li24P4S20Cl4`
- `H_Cl = Li23P4S19Cl5`
- `D_plain = Li18M2P4S17Cl4O3`
- `D_Cl = Li17M2P4S16Cl5O3`
- `baseline_cl_recipe_contrast = H_Cl - H_plain`
- `plain_dopant_recipe_contrast = D_plain - H_plain`
- `conditional_cl_recipe_contrast = D_Cl - D_plain`
- `recipe_interaction = conditional - baseline`

UI headline:

> Baseline recipe contrast = 0.000 V; conditional recipe contrast = −0.017 to +0.283 V. A universal Cl-rich benefit is rejected.

Caveat:

- 11 expanded rosters는 독립 host 실험 11개가 아니다.
- Total이 historical chain delta와 일치하는 것은 round-trip consistency다.
- Actual structure/site validation은 0/11이다.

## 5. B2O3는 composition-level valid, species-level unresolved

`/composition/b2o3`에 다음을 나란히 유지한다.

| record | composition | onset | status |
|---|---|---:|---|
| cascade chain | Li17B2P4S16Cl5O3 | 2.317 V | exact-composition result, same-run host |
| new matched D_plain | Li18B2P4S17Cl4O3 | 2.034 V | current pinned factorial |
| legacy DFT-deep | Li58P8S41Cl16B2O3 | 2.03 V | phase_set_id/entry IDs/MP version unavailable |

- Row value 2.317 V를 NA로 지우지 않는다.
- Species-level attribution은 `unresolved`로 표시한다.
- Legacy 2.03 V는 `branch-level consistency; not independent validation`으로만 쓴다.
- Dopant-label join으로 DFT validation badge를 다시 만들지 않는다.

## 6. Ladder + phase-roster robustness

### Host Li/Cl ladder

원장: `oxidation_matched_factorial.json`

- ladder0–3: 2.140 V
- ladder4 `Li20P4S16Cl8`: 2.356 V
- ladder4 products include `P2S7`, `0.5 LiS4`, `8 LiCl`

Public status:

- `MECHANISM HYPOTHESIS · APPENDIX ONLY`
- 허용: S17→S16에서 branch transition이 일부 doped recipe와 함께 관찰됨
- 금지: LiS4 disappearance mechanism, universal Cl mechanism, structural validation

### LiS4-excluded robustness

원장: `oxidation_matched_factorial_nolis4.json`

- WO3: +0.216 → 0.000 V
- Al2O3: +0.214 → +0.098 V
- MoO3: +0.216 → +0.129 V
- Sc2O3: −0.017 → −0.046 V
- B2O3: +0.283 → +0.283 V

다른 phase set의 절대 onset을 current 값으로 덮어쓰지 않는다. `phase_roster_status`, `excluded_entries`, `phase_set_id`를 값과 함께 노출하고, contrast가 roster-dependent라고 표시한다.

## 7. Pipeline explainer route/panel

`/cascade` 또는 seminar page에 `How the 20-stage workflow spends cost` 섹션을 추가한다. 네 그룹이면 충분하다.

1. `00–04 · Generate and anneal`
2. `05–08 · Static pathway and mechanics`
3. `09a–09f · Assemble and propose`
4. `10–12b · Expensive tail and final collection`

각 그룹은 다음 다섯 field를 갖는다.

- `question`
- `input_output`
- `cost_class`
- `why_before_next`
- `cannot_claim`

필수 warning:

- 01: missing `COMPOUND_FILTER` → ~85 species / 5000+ structures
- 05: consumes post-anneal geometry; legacy/noncanonical BVS; not conductivity
- 09f: `NOT A TRUE GRAND-POTENTIAL ESW`
- 10: `NOT RUN · 0/270`
- 11: `NOT RUN · 0/270`

`stage_status`와 `gate_status`를 한 enum으로 합치지 않는다.

## 8. Stage ↔ gate mapping

- G1 historical input ← stage 06 rerank
- G4 legacy input ← stage 05 BVS + geometry-derived 4 Å proximity
- G5 legacy input ← stage 08 elastic
- Current G2/G3 ← external pinned `esw_cascade_batch.py`, **not stage 09f**
- 09a–d = aggregation/predictor/input preparation
- 09e = decomposition audit, not candidate E_above_hull
- 10/11 = intended validation tail, not executed in v23

## 9. Access and manifest

기존 정책을 유지한다.

- historical rank/score: `?archive=1`
- recovered diagnostic themes/candidates: `?view=diagnostic`
- default public DOM: approved ranking/candidate rows 0
- `phase_set_id`는 public audit identifier로 허용

Manifest에 두 factorial 원장을 모두 등록하고 hash/bytes/rows/source commit을 검증한다.

- `oxidation_matched_factorial.json`
- `oxidation_matched_factorial_nolis4.json`

## 10. 회귀 테스트

1. G3 state는 270/270, 17/17, 0/11, approved 0을 동시에 렌더한다.
2. Public page에 stale `G3 method-comparable 0`이 없다.
3. Public page에 `effect attribution closed`, `Cl effect = 0`, `11/11 species validated`가 없다.
4. Chain audit는 exact 10 / multi-transform 7을 재현한다.
5. 9.63×와 2.59×가 분모 및 non-causal label과 같은 panel에 있다.
6. B2O3 exact composition mismatch이면 validation link를 만들지 않는다.
7. Ladder4 onset=2.356, S16, products에 0.5 LiS4가 있음을 고정한다.
8. LiS4-excluded WO3=0.000, Al=0.098, Mo=0.129, B=0.283을 고정한다.
9. Stage 09f가 current G2/G3 source로 표시되지 않는다.
10. Stage 10/11은 `NOT RUN · 0/270`이고 `unharvested`가 아니다.
11. Default DOM과 JSON bootstrap에 archive/diagnostic candidate rows가 없다.
12. Manifest tamper 또는 unknown artifact는 fail-closed다.

## Release verdict

- Audit/status page + raw hash-gated downloads: GO
- Formula-level G3 operational contrast: GO within scope
- Ladder/roster mechanism panel: appendix hypothesis only
- Current leaderboard/Pareto/endpoint/winner: NO-GO
- Universal Cl/cation mechanism: NO-GO

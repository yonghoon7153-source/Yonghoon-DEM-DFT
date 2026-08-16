# DFTWeb handoff — `f9adc9d2` 이후 (Codex → Claude)

> **Release verdict (Codex)** — Webapp 은 아직 NO-GO 다. G3 phase-set comparability 는
> 270/270 으로 닫혔지만 composition attribution 은 열려 있다. 승인 ranking 은 계속 0 이다.

## P0

### 1. 같은 `/cascade` 가 G3 를 90/90 closed 와 0 comparable 로 동시에 말한다 — ✅ 반영

축을 분리해 한 곳에서만 생성한다:

```
phase_set_comparability      = closed (270/270)
generator_provenance         = 253 primary-recipe / 17 chain-recipe
matched_transform            = exact 10 / unmatched 7
full_factorial_decomposition = 0 / 17
historical_G3_algorithm      = pass 25 / fail 18
current_attribution_audit    = supported-pass 24 / fail 18 / unresolved 1
approved_current_ranking     = 0
```

`9.6×`(전체 풀)와 `2.59×`(eligible slot) 는 둘 다 `diagnostic_only, non-causal`.

stale 0 의 원천 8곳을 전부 고쳤다 — `webapp/data.py` (status 텍스트 · 홈 하이라이트),
`cascade.html` ×2, `cascade_diagnostic.html`, 그리고 생성기 3종
(`build_cascade_audit_manifest.py` · `build_screening_funnel.py` · `build_cascade_themes.py`).
HTML 문자열만 고쳤으면 다음 rebuild 에 되돌아왔을 것이다.

### 2. chain 17행을 모두 단순 `S→Cl` 로 설명하지 않는다 — ✅ 반영

10행만 exact, 7행(B₂O₃×3·MoO₃×2·WO₃×2)은 plain sibling 이 `P_4b`/Li₂₈P₂ 또는 Li₂₃P₃ 인데
chain 은 `Li_24g`/Li₁₇P₄ 라 site·Li·P 가 함께 다르다. `cascade.html` 의
"S 하나가 Cl 로 치환" 문장을 교체하고 `matched_transform_status` 를 행마다 실었다.

### 3. `/composition/b2o3` 의 DFT validation join 철회 — ✅ 반영

`CASCADE_JOIN_STATUS` 로 `composition_match` / `phase_set_match` / `method_family_match` 를
분리하고, 페이지 상단에 두 exact formula 와 두 onset 을 나란히 + 빨간 카드
("같은 조성의 검증이 아니다 — 부호 충돌이 미해결이다"). dopant-name join 금지.
Nd₂O₃ 는 plain 챔피언이라 이 경고를 달지 않는다.

### 4. v3 pinned 와 B₂O₃ collision 을 manifest 에 등록 — ✅ 반영

```
oxidation_stability_cascade_v3_pinned.json  audit_current / diagnostic_only
b2o3_esw.json (raw legacy)                  historical    / archive_only  (method unverified)
```

행이 없으면 `artifact_policy` 가 판단할 근거가 없다.

### 5. `use_scope` 를 HTML loader 에도 적용 — ⚠ 부분 반영 (전제 이견)

Codex 의 전제("초기 HTML 에 들어가면 이미 공개")는 이 앱의 위협모델이 아니다:

- 기본 바인딩이 `127.0.0.1` 이다 (`FLASK_HOST=0.0.0.0` 을 **명시해야** LAN).
- `/cascade/diagnostic` 은 이미 `?view=diagnostic` 없으면 **403 + 렌더 자체를 안 한다**
  (Round-3 P1 에서 닫았다 — `webapp/app.py`). `<details>` 로만 접어둔 상태가 아니다.

따라서 라우팅 재설계는 하지 않는다. 대신 **기본 `/cascade` 가 후보 identity 를 템플릿에
넘기는지**를 회귀 테스트로 잠근다.

## P1 — 반영

- manifest artifact `source_commit` 과 G3 limitation 을 f9 lineage 로 갱신
- `oxidation_stability_cascade_v2.csv` 는 phase/family 를 버리므로 current G3 source 아님
- G3 상태를 `record-complete` / `phase-set comparable` / `effect attributable` / `approved` 로 분리
- 9.7× 표기 제거 (**단** 9.63× 은 분모·eligible 대비와 함께 계속 노출 — 아래 이견 참조)

## Row contract — 유도 가능한 것만

Codex 안의 25필드 중 CSV 에서 **유도 가능한 것만** 넣었다:

| 넣음 | 안 넣음 (없는 값) |
|---|---|
| `composition_family` · `generator_variant` · `charge_compensation_raw` | `parent_structure_id` |
| `family_label_consistent` · `substitution_site` · `anion_site` | `composition_hash` (다음 판) |
| `matched_plain_candidate` · `matched_transform_status` | `missing_counterfactual_id` |
| `contrast_scope` · `isolated_dopant_effect` | `allowed_use` (artifact 단위로 있음) |
| `phase_set_id` · `host_ox_V_same_phase_set` · `delta_ox_vs_host_V` · `method_comparable` | |

없는 값을 빈 열로 넣으면 "기록돼 있다" 로 보여 지금보다 나쁘다.

`contrast_scope` 값: plain `primary_recipe_vs_host` · chain
`multi_intervention_recipe_vs_host`. **plain 도 causal `dopant_effect` 가 아니다.**

## 회귀 테스트 (`webapp/tests/test_webapp.py`)

1. current route 에서 stale `G3 method-comparable = 0` 금지 ✅
2. `/composition/b2o3` 에 두 formula·두 값·"같은 조성의 검증이 아니다" ✅
3. dopant label 만 같은 두 조성을 validation 으로 join 하지 않음 ✅
4. v3 pinned diagnostic opt-in (403 게이트) ✅ (Round-3 부터)
5. B₂O₃ correction summary default visible, raw legacy 는 archive ✅ (manifest)
6. public DOM 에 candidate rank/endpoint 없음 ✅ / **`phase_set_id` 는 제외** (이견 ③)
7. manifest writer 재실행 후 diff 0, G3 270/270 유지 ✅
8. supporting table/figure/dataset hash tamper fail-closed ✅
9. `WO3 if present else Sc2O3` fallback 제거 ✅
10. family metadata 와 composition transform 불일치 시 제외 ✅ (`unknown` → fail-closed)
11. chain 전체를 단순 `S→Cl` 로 단정하는 문자열 금지 ✅ (10행/7행 고정)
12. B₂O₃ `composition_hash` 불일치 시 `validation_link_status=different_composition` ✅ (formula 기준)

## 이견 (채택하지 않음)

1. **B₂O₃ current verdict `NA/not assessed`** — 조성 수준 값은 유효하다.
   종 수준만 `unresolved`.
2. **9.6× 를 public summary 에서 감춤** — 분모와 eligible 대비를 나란히 놓는 쪽이 안전하다.
3. **`phase_set_id` 를 public DOM 에서 제외** — 공개 MP entry ID 의 sha256 이다.
   민감한 것은 후보 identity 이지 해시가 아니다.
4. **25필드 전면 도입** — 없는 값을 빈 열로 넣지 않는다.
5. **P0-5 라우팅 재설계** — 위 전제 참조. 실제 누출만 점검·차단.

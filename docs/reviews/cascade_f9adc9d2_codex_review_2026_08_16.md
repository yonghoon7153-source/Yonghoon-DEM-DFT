# Cascade composition-family audit — Codex review of `f9adc9d2`

- 검토 대상: `claude/friendly-meitner-lldvar@f9adc9d2` (동결본)
- 회신 반영: `f9adc9d2` 이후 커밋 4건 (아래 "반영 상태")
- 성격: **외부 동결 리뷰 원문 + 우리 판정**. 원문을 고치지 않고, 우리가 다르게 간 곳은 절을 따로 뒀다.

> **결론(Codex)** — `f9adc9d2` 는 champion 의 generator provenance 를 드러내는 감사 패치로는
> 유효하다. 그러나 `compound_set_chain` 을 통제된 Cl 치환군으로 해석하거나 B₂O₃ 부호 반전을
> 조성 하나에 귀속하는 데에는 아직 쓸 수 없다. 승인 ranking 은 계속 0 이다.

## P0

### P0-1. 17개 chain champion 은 하나의 `S→Cl, Li−1` family 가 아니다

조성 벡터 전수 대조 결과 chain champion 17행 중 **10행만** plain 후보와 같은 자리에서
`ΔLi=-1, ΔS=-1, ΔCl=+1` 이다. 나머지 7행:

| Species | Slots | Plain candidate | Chain champion | Additional mismatch |
|---|---:|---|---|---|
| B₂O₃ | 3 | Li₂₈B₂P₂S₁₇Cl₄O₃, `P_4b` | Li₁₇B₂P₄S₁₆Cl₅O₃, `Li_24g` | Li −11 · P +2 · site |
| MoO₃ | 2 | Li₂₃MoP₃S₁₇Cl₄O₃, `P_4b` | Li₁₇MoP₄S₁₆Cl₅O₃, `Li_24g` | Li −6 · P +1 · site |
| WO₃ | 2 | Li₂₃WP₃S₁₇Cl₄O₃, `P_4b` | Li₁₇WP₄S₁₆Cl₅O₃, `Li_24g` | Li −6 · P +1 · site |

→ `composition_family=Clrich` 는 원인 변수가 아니라 `compound_set_chain` **generator recipe
provenance label** 로만 써야 한다. Al/Mo/W 를 하나의 Cl-only 대비로 묶을 수 없고,
같은-자리 clean contrast 는 **Al 하나**뿐이다.

### P0-2. B₂O₃ 의 "same phase set → purely composition" 은 증명되지 않았다

cascade 쪽 `Li₁₇B₂P₄S₁₆Cl₅O₃` 에는 pinned `phase_set_id` 가 있다. legacy
`Li₅₈P₈S₄₁Cl₁₆B₂O₃` 기록에는 entry IDs·`phase_set_id`·MP snapshot·excluded-phase roster·
재현 가능한 generator 가 **모두 없다**. `346 entries`·같은 chemsys·반올림된 2.14 V host 가
같다는 것은 sorted entry-ID set 이 같다는 증거가 아니다. legacy baseline label 은
`LPSCl1.6`, cascade baseline 은 Li₆PS₅Cl 계열이다.

허용 문장은 여기까지다:

> 서로 다른 두 B₂O₃-containing 조성 기록에서 onset 의 host-relative 부호가 반대로 보인다.
> nominal method 와 chemsys 는 유사하지만 legacy phase-set identity 가 없어 원인을 조성
> 하나로 확정할 수 없다.

### P0-3. 경고만 붙이고 B₂O₃ 의 species-level G3 pass 를 유지하면 fail-open 이다

역사 47종 waterfall 은 커밋 전후 동일하다 (`47 → 47 → 43 → 25 → 11 → 1`).
감사 표기는 분리해야 한다:

```
G2 survivors: 43
algorithmic G3 threshold: pass 25 / fail 18
attribution audit: supported-pass 24 / fail 18 / unresolved 1
```

43행 모두 same-run phase-set method comparison 은 가능하다. unresolved 는
method-comparability 가 아니라 **B₂O₃ species-level 효과 귀속** 문제다.

## P1

### P1-1. 9.7× 가 아니라 9.6×

```
plain: 17 / 253 = 6.719%
chain: 11 / 17  = 64.706%
ratio: (11/17)/(17/253) = 9.629757... → 9.6
```

`f9adc9d2` 는 6.7 과 64.7 을 먼저 반올림한 뒤 나눠 9.7 을 만들었다. 최종 비율에서 한 번만
반올림해야 한다.

### P1-2. 9.6× 의 denominator 도 Cl-effect estimand 가 아니다

chain 후보가 실제 존재하는 슬롯은 270 중 **33개** (11 species). eligible pool 의 champion 만:

```
chain champion above host: 11 / 17
plain champion above host:  4 / 16
descriptive ratio: 2.59×
```

두 비율 모두 selected maxima 의 사후 기술통계이고, 농도 label 도 독립 replicate 가 아니다.

## A–G 답변 요지

- **A. family 판별자** — `charge_compensation` 은 provenance 의 1차 source 로 적절하나
  exact composition family 의 유일 판별자로는 부족하다. `generator_variant`,
  `exact_composition_formula` + `composition_hash`, `substitution_site`, seed,
  parent-structure lineage, `paired_plain_composition_id`, `matched_transform`,
  source row hash 를 함께 저장한다. Cl/S 비로 family 를 재추정하면 dopant 자체가 Cl/S 를
  포함할 때 오분류한다. unknown/conflict 는 통계·gate 에서 fail-closed.
- **B. plain 의 귀속 범위** — plain 도 host 대비 O/S 치환·site·Li 전하보상이 함께 바뀐다.
  `contrast_scope = exact_recipe_vs_host_same_phase_set`,
  `isolated_dopant_effect = false`. `dopant effect` 대신 `recipe-level host contrast`.
- **C. Cl-only counterfactual** — `H = Li24P4S20Cl4`, `C = Li23P4S19Cl5`,
  `D_plain = Li18M2P4S17Cl4O3`, `D_Cl = Li17M2P4S16Cl5O3`,
  interaction `= [f(D_Cl)-f(D_plain)] - [f(H_Cl)-f(H_plain)]`.
  B/Mo/W 는 matched `D_plain`/`D_Cl` 을 새로 구성해야 한다. 최소로는 chain 17행이 속한
  **10개 unique phase set** 마다 H/C/D/DC 를 같은 pinned entry set 에서 계산한다.
- **D. 2.35 V plateau** — 2.340–2.370 V 군 **21/21 이 P₂S₇** 생성, 정확히 2.140 V 군
  **102/102 가 Li₃PS₄** 생성(P₂S₇ 0/102). 다만 고전압군에 plain 15 + chain 6 이 섞여 있고
  plain Sc₂O₃ 도 2.356 V — **P₂S₇ 도 2.356 V 도 Cl-rich fingerprint 가 아니다.**
- **E. `['B2O3']` exact assert** — pinned snapshot + source hash 를 함께 고정한 golden
  regression 이면 유용하다. 일반 plot 함수 안의 과학 invariant 로 두면 취약하다.
- **F. selftest 가 놓치는 것** — charge metadata vs 실제 조성 벡터 불일치, 한 family 안의
  복수 조성 signature, unknown/label conflict fail-open, duplicate `name` silent overwrite,
  `delta=None` 을 분모에서 제외 안 함, `delta == oxidation_limit - host_ox` 재검산,
  같은 base/phase_set 의 host onset 일관성, 270-slot cardinality 와 rank-1 uniqueness,
  exact matched transform·site/seed/parent lineage, rounded-percent ratio bug 와 zero
  denominator, downstream G3/RAISED/DFT-deep join 의 composition identity, idempotence
  전체 row mutation, unknown family 가 거짓 Cl-rich narrative 를 받는 경로, plain onset 이
  `None` 일 때 `no_plain` 오분류, **`raises()` 가 예외 type/message 를 확인하지 않고 모든
  exception 을 성공으로 세는 문제**.
- **G. DB 값 처리** — raw measurement 는 지우지 않는다. causal alias 와 join 만 무효화한다.
  무효화 대상: dopant label 만으로 연결한 B₂O₃ `dft_deep=True`, generic B₂O₃ species G3 pass,
  `plain = unconfounded` 의 넓은 의미, 9.7×, "same phase set 이므로 purely composition".

## 재현

`docs/reviews/cascade_f9adc9d2_codex_review_repro.py` 참조. 기대 출력:

```
family 253 17
raised 17 / 253 vs 11 / 17
exact ratio 9.629757... one decimal 9.6
eligible slots 33 champions 16 17 ratio 2.588235...
matched 10 unmatched 7
G2 43 algorithmic G3 25 18 attribution 24 18 1
```

## 반영 상태 (우리 쪽)

| 항목 | 상태 | 커밋 |
|---|---|---|
| P0-1 matched_transform 10/7 | 반영 | `classify_transform()` + `matched_transform_status` |
| P0-2 "purely composition" 철회 | 반영 | `b2o3_esw.json: composition_collision_2026_08_16` |
| P0-3 귀속 24/18/1 | 반영 | funnel `attribution_audit` |
| P1-1 9.63 | 반영 | 원계수에서 한 번만 반올림 |
| P1-2 eligible 2.59 | 반영 | `onset_raise_rate.eligible_slots_only` |
| F `raises()` fail-open | 반영 | 예외 type·message 확인 |
| E assert | 반영(형태 변경) | plot 안 assert 유지 + 버전된 테스트로 이중화 |

## 우리가 다르게 간 곳 (동의하지 않음)

1. **"B₂O₃ current verdict = `NA/not assessed`"** — 채택하지 않았다.
   그 조성의 onset 은 같은 phase set 안에서 같은 실행 host 와 비교된 **유효한 값**이다.
   안 닫힌 것은 *종 수준* 귀속이다. 그래서 행 값은 보존하고 **종 수준만 `unresolved`** 로 뒀다.
   `NA` 로 적으면 계산을 안 한 것처럼 읽힌다.
2. **"9.6× 를 public summary 에 전면 노출하지 않는다"** — 채택하지 않았다.
   숨기면 독자가 스스로 잘못 재구성한다. 분모(253/17)와 eligible 대비(2.59×)를 **나란히**
   놓고 "사후 기술통계" 를 붙이는 쪽이 안전하다.
3. **"public DOM 에 candidate rank/endpoint/`phase_set` IDs 없음"** — `phase_set_id` 는 제외한다.
   그것은 공개된 MP entry ID 들의 sha256 이다. 민감한 것은 **후보 identity** 이지 해시가
   아니고, 해시를 가리면 감사 화면이 자기 목적(재현 가능성 제시)을 잃는다.
4. **25필드 row contract 전면 도입** — 유도 가능한 필드만 넣었다.
   `parent_structure_id` 같은 없는 값을 빈 열로 넣으면 "기록돼 있다" 로 보여 지금보다 나쁘다.
   없는 것은 **없다고 적는다**.
5. **webapp P0-5 의 전제** — "초기 HTML 에 들어가면 이미 공개" 는 이 앱의 위협모델이 아니다.
   기본 바인딩이 `127.0.0.1` 이고(`FLASK_HOST=0.0.0.0` 을 명시해야 LAN),
   `/cascade/diagnostic` 은 이미 `?view=diagnostic` 없으면 **403 + 렌더 자체를 안 한다**
   (Round-3 에서 닫았다). 라우팅 재설계는 하지 않고, 기본 화면의 실제 누출만 점검·차단한다.

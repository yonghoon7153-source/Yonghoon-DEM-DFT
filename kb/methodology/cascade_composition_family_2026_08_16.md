---
title: 캐스케이드 조성족 섞임 — 보편적 Cl 개선은 반증, 원소 수준 인과는 여전히 열림
date: 2026-08-16
updated: 2026-08-16
tags: [cascade, esw, oxidation, composition, provenance, b2o3, correction, factorial, attribution]
status: 확정 — 조성족 분류 완료. **효과 귀속은 열림**(2026-08-16 재감사로 '닫힘' 철회)
confidence: high
verificationStatus: verified
verifiedAt: 2026-08-16
verifiedBy: Codex 동결 리뷰 f9adc9d2 (P0 3건·P1 2건 정정 반영) + 우리 repo 전수 재현
explored: false
authoredBy: agent
effort: high
claimType: empirical
evidenceScope: multi-source-primary
---

## 요약

캐스케이드의 **챔피언 슬롯은 (도펀트, 농도라벨) 하나당 하나**이고, 그 슬롯은
`combined_score` 최대값이 가져간다. 후보 풀에는 **같은 도펀트의 두 generator 변형**이
같이 들어 있어서, 270 슬롯 중 **17개는 이름표만 같고 조성이 다르다**.

⛔ **`compound_set_chain` 은 "S 하나를 Cl 로 바꾼 것" 이 아니다** (2026-08-16 Codex P0-1 정정).
조성 벡터를 전수 대조하면 17행 중 **10행만** plain 형제와 정확히 `ΔLi=−1·ΔS=−1·ΔCl=+1` 이고,
나머지 **7행**은 **치환 자리부터 다르다**:

| 종 | 슬롯 | plain 후보 | chain 챔피언 | 추가 불일치 |
|---|---:|---|---|---|
| B₂O₃ | 3 | `Li28B2P2S17Cl4O3` · **P_4b** | `Li17B2P4S16Cl5O3` · **Li_24g** | Li −11 · P +2 · 자리 |
| MoO₃ | 2 | `Li23MoP3S17Cl4O3` · **P_4b** | `Li17MoP4S16Cl5O3` · **Li_24g** | Li −6 · P +1 · 자리 |
| WO₃ | 2 | `Li23WP3S17Cl4O3` · **P_4b** | `Li17WP4S16Cl5O3` · **Li_24g** | Li −6 · P +1 · 자리 |

그래서 `composition_family` 는 **원인 변수가 아니라 generator provenance 라벨**이다.
Al/Mo/W 세 종을 하나의 Cl 대비로 묶을 수 없고, 같은-자리 clean contrast 는 **Al 하나**뿐이다.

⚠ **plain 도 순수 도펀트 효과가 아니다.** host 대비 O/S 치환·자리 선택·Li 전하보상이
함께 바뀐다. `unconfounded` 가 뜻하는 범위는 "추가 chain 개입이 없다" 까지이고,
쓸 말은 `dopant effect` 가 아니라 **`recipe-level host contrast`** 다.

## 전수 결과 — 둘 다 사후 기술통계다

```
host(2.140 V) 초과 비율 (전체 챔피언)
  plain  : 17/253 =  6.719%
  chain  : 11/17  = 64.706%     → 9.63배   ← 원계수에서 한 번만 반올림
```

⛔ **9.7 이 아니라 9.63** (2026-08-16 Codex P1-1 정정). 앞 판은 6.7 과 64.7 을 **먼저 반올림한 뒤**
나눠 9.7 을 만들었다.

⛔ 그리고 이 분모에는 **chain 후보가 존재하지도 않았던 237 슬롯**이 들어 있다.
chain 후보가 실제 있던 **33 슬롯**(11종)만 보면 (Codex P1-2):

```
chain 챔피언 host 초과 : 11/17
plain 챔피언 host 초과 :  4/16
                        → 2.59배
```

**둘 다 인과 효과가 아니다.** 챔피언은 `combined_score` 최대값으로 **사후 선택**됐고,
농도 라벨 x002/x005/x010 은 독립 반복이 아니다(실측 x 는 셋 다 0.25).

| 종 | plain ox_V | chain ox_V | 변환 | 판정 |
|---|---|---|---|---|
| Al2O3 | 2.140 (=host) | 2.354 | **exact** | chain 에서만 초과 — 유일한 같은-자리 대비 |
| MoO3  | 2.140 (=host) | 2.356 | multi | 자리·Li/P 도 다름 |
| WO3   | 2.140 (=host) | 2.356 | multi | 자리·Li/P 도 다름 |
| **B2O3** | **없음** | 2.317 | multi | plain 챔피언 자체가 없다 |
| Sc2O3 | 2.356 | 2.339 | exact | plain 도 초과 — 무관 |
| Y2O3  | 2.282 | 2.282 | exact | 축퇴 — 무관 |

### 2.35 V 군의 반응식 (Codex D — 기술적 관찰까지만)

- 2.340–2.370 V 군: **21/21 이 P₂S₇ 생성**
- 정확히 2.140 V 군: **102/102 가 Li₃PS₄ 생성**, P₂S₇ 0/102

onset plateau 가 서로 다른 분해 assemblage 분기에 대응한다는 **기술적 관찰**로는 쓸 수 있다.
다만 고전압군에 plain 15행 + chain 6행이 섞여 있고 plain Sc₂O₃ 도 2.356 V 다 →
**P₂S₇ 도 2.356 V 도 Cl-rich 지문이 아니고 Cl 인과의 증거도 아니다.**

## 제일 비싼 파급: B₂O₃ 의 부호가 뒤집힌다 — 다만 원인은 미확정

B₂O₃ 는 우리 **DFT-deep 2종 중 하나**(다른 하나 Nd₂O₃)다. 그런데:

| 대상 | 조성 | onset | host(2.14) 대비 | phase_set_id |
|---|---|---|---|---|
| **DFT-deep 셀** (`b2o3_esw.json`) | `Li58P8S41Cl16B2O3` | **2.03 V** | **−0.11 (악화)** | **없음** |
| 캐스케이드 챔피언 (pinned) | `Li17B2P4S16Cl5O3` | **2.317 V** | **+0.177 (개선)** | `257d50d8c59cde8f` |

⛔ **앞 판의 "같은 방법·같은 chemsys·346 entries 이므로 순전히 조성 차이" 는 철회했다**
(2026-08-16 Codex P0-2). legacy 기록에는 entry ID 목록도 `phase_set_id` 도 MP 스냅샷 버전도
제외상 목록도 **없다**. entry 개수와 chemsys 가 같다는 것은 **정렬된 entry-ID 집합이
같다는 증거가 아니다.** 게다가 legacy baseline 라벨은 `LPSCl1.6` 이고 cascade host 는
Li₆PS₅Cl 계열이라 host 조성이 같은지도 확인되지 않았다.

- ⛔ 금지: "B₂O₃ 가 산화 onset 을 +0.177 V 올린다" · "같은 방법에서 순전히 조성 차이로 부호가 뒤집힌다"
- ✅ 허용: "서로 다른 두 B₂O₃ 함유 조성 기록에서 host 대비 onset 부호가 반대로 보인다.
  명목 방법과 chemsys 는 비슷하지만 **legacy phase-set identity 가 없어** 원인을 조성 하나로
  확정할 수 없다."
- 닫는 법: 두 조성과 각자의 host 를 **하나의 pinned entry set** 에서 다시 계산 (MP 질의만 필요)

### 종 수준 G3 통과도 쪼갰다 (Codex P0-3)

경고만 붙이고 species-level pass 를 유지하면 fail-open 이다:

```
G2 생존         43
알고리즘 G3     pass 25 / fail 18          ← 역사 count, archive 로 보존
귀속 감사       supported-pass 24 / fail 18 / unresolved 1 (B2O3)
```

`unresolved` 는 method-comparability 문제가 아니다 — 43행 모두 같은 phase set 안에서
host 와 비교된다. **종 수준 효과 귀속**이 안 닫힌 것이다.

## 안 무너지는 것

- **최종 생존자 WO₃** 는 pool ox_V 가 **plain 챔피언 값(2.140)** 이다 — 오염 아님.
- Y₂O₃ 는 두 족의 onset 이 **같아서**(2.282) 라벨이 아무 혼동을 만들지 않는다 (`degenerate`).
- 47종 pool 중 오염은 **B₂O₃ 단 1건** (`ox_family_confounded=1`). 43 plain · 3 degenerate.
- 깔때기 기계적 count 는 그대로다 (`47 → 47 → 43 → 25 → 11 → 1`) — 바뀐 건 **해석**이다.
- **G3 phase-set 비교 270/270 은 유효하다.** 이번 정정은 그 위층(효과 귀속)에 대한 것이지
  `phase_set_id` 폐쇄를 되돌리지 않는다.

## 반영 (도구 5 · db 6 · webapp 4)

| 대상 | 조치 |
|---|---|
| `tools/oxidation/esw_cascade_batch.py` | `classify_family()` + **`classify_transform()`**(조성 벡터 전수 대조) + `annotate_families()`; MP 없이 입히는 `--annotate`, `--selftest` **41건** |
| `tools/cascade/build_screening_funnel.py` | G3 `composition_family_caveat` + pool 행 3필드 + **`attribution_audit`**(pass 24 / fail 18 / unresolved 1) |
| `tools/cascade/build_cascade_audit_manifest.py` | v3 pinned·b2o3_esw **원장 등록** + metric contract 에 3층 분리를 데이터로 |
| `tools/figures/plot_cascade_seminar_47.py` | `ox_composition_family()` + CSV 3열 + 그림 각주 2개 |
| `tools/cascade/build_cascade_themes.py` | stale `method-comparable 0` 문구 제거 |
| `db/.../oxidation_stability_cascade_v3_pinned.json` | 행마다 `composition_family`·`matched_transform_status`·`matched_plain_candidate`·`substitution_site`·`contrast_scope`·`isolated_dopant_effect`, 최상위 `composition_family_audit`(+`matched_transform`, `eligible_slots_only`) + `dft_deep_composition_collision` |
| `db/properties/b2o3_esw.json` | `composition_collision_2026_08_16` — **"순전히 조성 차이" 철회** |
| `webapp/data.py` | `CASCADE_JOIN_STATUS`(composition/phase_set/method match 3분리) · stale 0 제거 |
| `webapp/templates/composition.html` | B₂O₃ 페이지에 **두 조성식·두 onset 나란히 + 빨간 카드** ("같은 조성의 검증이 아니다") |
| `webapp/templates/cascade.html` · `cascade_diagnostic.html` | 3층 분리 문구 · chain 전체를 S→Cl 로 단정하던 문장 교체 |
| `webapp/tests/test_webapp.py` | **69건** — 조성족·변환 10/7·비율 9.63/2.59·B₂O₃ join·귀속 24/18/1 잠금, `WO3 if present else Sc2O3` fallback 제거 |

판별자는 **CSV 의 `charge_compensation`**(generator provenance)이고, `dopant` 라벨의
`+Clrich` 접미사는 거울일 뿐이라 어긋나면 `family_label_inconsistent` 로 남긴다(현재 0건).
모르는 값은 **plain 으로 흘리지 않고** `unknown` 으로 떨어뜨린다.
다만 **provenance 만으로는 부족하다** — `matched_transform_status` 로 조성 벡터를 같이 본다.

## 효과 귀속 — **안 닫혔다** (2026-08-16 재감사로 철회)

⛔ 앞 판은 "`main(Cl)=0` 이므로 Cl 효과는 0 · 효과 귀속 폐쇄" 라고 적었다. **철회한다.**

`tools/oxidation/esw_matched_factorial.py` 로 네 칸을 chemsys 마다 같은 pinned entry set
안에서 쟀다 (11종 · 11 phase set · GPU 미사용). 계산값 44개와 2×2 대수는 재현된다.
**틀린 건 이름과 범위였다.**

### 이름부터 틀렸다 (Codex 재감사 P0-1)

`H_Cl − H_plain` 을 **main(Cl)** 이라 불렀는데, 그건 2×2 factorial 의 marginal main effect 가
아니라 **도펀트가 없는 기준점의 simple contrast** 다. 도펀트가 있을 때의 recipe 효과는
`D_Cl − D_plain` 이고, 그건 0 이 아니다.

```
종        baseline(undoped)   conditional(doped)   interaction   총합
Al2O3          +0.000              +0.214            +0.214     +0.214
B2O3           +0.000              +0.283            +0.283     +0.177
MoO3           +0.000              +0.216            +0.216     +0.216
WO3            +0.000              +0.216            +0.216     +0.216
Sc2O3          +0.000              -0.017            -0.017     +0.199
Y2O3           +0.000              +0.000            +0.000     +0.142
La2O3          +0.000              +0.032            +0.032     -0.215
Nd2O3          +0.000              +0.067            +0.067     -0.153
Sm2O3          +0.000              +0.045            +0.045     -0.106
MgO/ZnO        +0.000              +0.000            +0.000      0.000
```

| | 성립 | 불성립 |
|---|---|---|
| ✅ | **"Cl-rich 가 보편적으로 개선한다" 는 반증됐다** | |
| ⛔ | | "Cl 효과가 0 이다" · "인과 귀속이 닫혔다" |

정확한 문장: **undoped LPSCl 기준에서는 −Li−S+Cl recipe 가 onset 을 움직이지 않았다.
그러나 doped 조성에서는 그 조건부 효과가 종에 따라 양·음·0 으로 달라진다.**

필드명도 바꿨다: `baseline_cl_recipe_contrast` · `plain_dopant_recipe_contrast` ·
`conditional_cl_recipe_contrast` · `recipe_interaction`.
difference-in-differences 자체는 비선형 응답에도 유효하다 — 문제는 **`main effect` 라는
이름이 원소 수준 인과를 함의한 것**이었다.

### 11/11 은 독립 표본 11개가 아니다 (재감사 P0-2)

11종 모두 **같은** `H_plain = Li₂₄P₄S₂₀Cl₄` · `H_Cl = Li₂₃P₄S₁₉Cl₅` 를 쓴다. 도펀트 원소는
host 조성에 없으므로 host 분해에 참여할 수 없고, 실제 반응식도 11개 phase diagram 에서
전부 같다. 쓸 문장은:

> The same undoped host-recipe contrast remained at 0.000 V in **eleven expanded phase rosters**.

### LiS₄→P₂S₇ 기전은 Al 하나를 일반화한 것이었다 (재감사 P0-3)

| 종 | D_plain | D_Cl | 내 주장과 |
|---|---|---|---|
| **Al₂O₃** | LiS4 ✓ | LiS4 **소멸** · P₂S₇ ✓ | ✅ 유일하게 일치 |
| MoO₃·WO₃ | LiS4 ✓ | P₂S₇ ✓ 인데 **LiS4 도 남음** | ❌ |
| B₂O₃ | **둘 다 없음** (Li₂B₂S₅ 분기) | P₂S₇ ✓ | ❌ 시작 분기가 다름 |
| Sc₂O₃ | **이미 P₂S₇** | P₂S₇ ✓ | ❌ |
| Y₂O₃·MgO·ZnO | LiS4 ✓ | LiS4 ✓ | onset 불변 |

2.35 V 군과 P₂S₇ 의 연관은 **강한 branch marker** 지만 "Li 18→17 에서 LiS₄ 가 사라져
P₂S₇ 로 전환" 은 **보편 기전이 아니다.** → **appendix hypothesis 로만.**

기전을 본문 결론으로 쓰려면 먼저: ① LiS₄-excluded phase set 에서 2×2 재실행
② host Li/Cl ladder(Li24→23→22…) 를 한 roster 에서 스캔 ③ branch identity 와 부호 유지 대조.

### 세 축을 한 숫자로 덮지 않는다

```
operational_factorial_coverage    = 17/17 chain rows
element_level_causal_attribution  = not_claimed
structural_realization_validated  = 0/11
approved_current_ranking          = 0종            ← 유지
```

## 사다리와 LiS₄ 제외판 — 두 번째로 서술이 무너졌다 (2026-08-16)

### ③ `baseline = 0` 은 **한 계단짜리** 문장이었다

`--ladder 4` 로 도펀트 없는 host 에서 −Li−S+Cl 을 반복했다:

```
ladder0  Li24 S20 Cl4   2.140   4 Li3PS4 + LiS4        + 4 LiCl
ladder1  Li23 S19 Cl5   2.140   4 Li3PS4 + 0.75 LiS4   + 5 LiCl
ladder2  Li22 S18 Cl6   2.140   4 Li3PS4 + 0.50 LiS4   + 6 LiCl
ladder3  Li21 S17 Cl7   2.140   4 Li3PS4 + 0.25 LiS4   + 7 LiCl
ladder4  Li20 S16 Cl8   2.356   2 P2S7   + 0.50 LiS4   + 8 LiCl   ← 점프
```

**도펀트 없는 host 도 Cl 을 네 번 넣으면 정확히 +0.216 이 나온다.** 그러니까
`baseline_cl_recipe_contrast = 0` 은 "Cl 이 아무 일도 안 한다" 가 아니라
**"첫 계단에서는 안 움직인다"** 였다. Al/Mo/W 의 상호작용은 **도펀트가 조성을 분기 경계
쪽으로 밀어 놓은 것**이고, 같은 점프를 host 혼자서도 도달한다.

⛔ 그리고 **ladder4 에도 LiS₄ 가 남아 있다** — 순수 host 사다리조차 "LiS₄ 소멸" 을 반증한다.

전환 지점은 Li 가 아니라 **S17 → S16** 에서 일치한다
(ladder3 S17 = 2.140 · ladder4 S16 = 2.356 / Al·Mo·W 도 D_plain S17 = 2.140 · D_Cl S16 = 점프).
⚠ 다만 **B₂O₃·Sc₂O₃ 는 안 맞는다** — 또 일반화하지 않는다. 관찰까지다.

### ④ LiS₄ 를 빼면 숫자가 안 버틴다

| 종 | conditional (LiS₄ 포함) | (LiS₄ 제외) |
|---|---|---|
| **WO₃** | +0.216 | **+0.000** ← 사라짐 |
| Al₂O₃ | +0.214 | **+0.098** ← 절반 이하 |
| MoO₃ | +0.216 | **+0.129** |
| Sc₂O₃ | −0.017 | −0.046 |
| B₂O₃ | +0.283 | +0.283 (불변) |
| La·Nd·Sm·Mg·Y·Zn | 동일 | 동일 |

`plain_dopant` 도 움직인다 (WO₃ +0.000 → −0.016 · Sm₂O₃ −0.151 → −0.267).

> **conditional contrast 자체가 phase roster 에 의존한다.** 부호는 대체로 유지되지만
> 크기가 반토막이고 WO₃ 는 아예 0 이 된다. 인용할 때 **roster 를 반드시 같이 적는다.**

Codex 가 "기전을 headline 으로 쓰려면 LiS₄ 제외판이 필수" 라고 한 것이 정확했다.
→ **기전은 appendix hypothesis 로 유지.** 본문 결론 금지.

## 반증·한계

- **조성 수준 operational contrast 다.** grand-potential ESW 는 조성만 받으므로 그 조성이
  **구조적으로 실현 가능한지**는 말하지 않는다 (`structural_realization_validated = 0/11`).
- **캐스케이드 값과 일치하는 것은 round-trip consistency 검사**이지 독립 물리 검증이 아니다.
  같은 조성·같은 entry roster·같은 알고리즘이면 같은 값이 나오는 게 당연하다.
- 캐스케이드의 B₂O₃·MoO₃·WO₃ **기존 plain 챔피언은 `P_4b` 자리**라 이 설계의 `D_plain`(`Li_24g`)과
  **다른 물건**이다.
- **전하 보상은 산화수를 검증하지 않는다.** 중성 M_xO_y 가정하에 양이온 총전하를 `2·n_O` 로
  잡는다. 현재 11종에는 맞지만 **일반 defect chemistry 규칙이 아니다** —
  `generator charge-compensation recipe` 라고 부른다.
- **onset 반응식 선택에 tie 버그가 있었다.** onset 전압을 정한 뒤 전 step 중 |V−ox| 최소를
  다시 찾아 반응식을 골라서, 축퇴 시 negative-evolution step 이 아닌 반응을 잡을 수 있었다.
  도구는 고쳤지만 **현재 JSON 은 재실행 전**이라 반응식 필드를 기전 근거로 쓰면 안 된다.
- `phase_set_id` 는 **entry ID 만** hash 한다 — energy/correction 변경을 고정하지 못한다.
  `db_version + entry_id + energy + correction` 을 함께 묶어야 진짜 pinned 다.
- B₂O₃ 2.034 vs legacy 2.03 은 **branch-level consistency 를 시사하는 정성적 수렴**이다.
  legacy 에 phase_set ID·host identity 가 없으므로 "독립 검증" 도 "B 효과 방향 확정" 도 아니다.
- **LiS₄ 포함/제외 민감도(2.140 vs 2.256)는 그대로 열려 있다.**
- 이 카드는 **산화 onset 축만** 본다. de(G1)·E/GB(G5) 파급은 안 쟀다.
- x 라벨(x002/x005/x010)은 농도가 아니다 — 실측은 셋 다 x=0.25 (`champions_v2.csv` 270행
  concentration 전부 0.25). 이번 2×2 는 그 버그를 **고친 게 아니다**.

## 내가 틀린 것 (2026-08-16, Codex 리뷰 `f9adc9d2`)

| # | 틀린 서술 | 정정 |
|---|---|---|
| ① | "chain = S 하나가 Cl 로 치환" (family 전체) | **10/17 만 exact.** 7행은 치환 자리(P_4b→Li_24g)·Li/P 까지 다름 |
| ② | "같은 방법이므로 B₂O₃ 는 순전히 조성 차이" | legacy 에 `phase_set_id`·entry_ids·MP 버전 없음 — **미확정** |
| ③ | 9.7배 | **9.63배** (pct 를 먼저 반올림한 이중 반올림) |
| ④ | 9.63배를 그대로 인용 | 분모에 chain 후보 없던 237 슬롯 포함 — eligible 33 슬롯이면 **2.59배** |
| ⑤ | selftest `raises()` 가 `except Exception` | 오타로 죽어도 통과했다 — 예외 type·메시지 확인으로 |
| ⑥ | `main(Cl)=0` → "Cl 효과 0 · 귀속 폐쇄" | **marginal main effect 가 아니라 undoped baseline contrast.** 조건부(D_Cl−D_plain)는 Al +0.214·B +0.283·Mo/W +0.216 |
| ⑦ | "11/11 종에서 0" | 같은 host 두 조성을 **11개 확장 roster 에서 반복** — 독립 표본 아님 |
| ⑧ | LiS₄→P₂S₇ 기전 | **Al 하나를 일반화.** Mo/W 는 LiS₄ 잔존, B/Sc 는 시작 분기가 다름 |
| ⑨ | "undoped Cl recipe 는 onset 을 안 움직인다" | **한 계단짜리 문장.** 사다리 4계단이면 host 혼자서도 +0.216 |
| ⑩ | 전환이 Li 18→17 | 사다리는 **S17→S16** 에서 전환 (Al·Mo·W 도 일치, B·Sc 는 불일치) |
| ⑪ | conditional contrast 를 고정값처럼 인용 | **phase roster 의존.** LiS₄ 빼면 WO₃ +0.216→0.000, Al₂O₃ 절반 |

①은 Al₂O₃ 한 케이스(정확히 맞는다)에서 family 전체로 일반화한 것이다.
`cation_site` 열을 이미 출력해 보고도 놓쳤다.

## 출처

- `db/properties/cascade_v23_all.csv` (3615행, `charge_compensation` 3105 plain / 510 chain)
- `db/properties/oxidation_stability_cascade_v3_pinned.json` (270 챔피언 + 84 host)
- `db/properties/b2o3_esw.json` (2.03 V, ocv_decomp 의 `16 LiCl` 로 조성 역산)
- 관련: `kb/methodology/cascade_pipeline_anatomy_2026_08_13.md` (G3 phase_set 폐쇄)

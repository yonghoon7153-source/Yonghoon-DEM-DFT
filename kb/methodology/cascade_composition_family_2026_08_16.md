---
title: 캐스케이드 조성족 섞임과 효과 귀속 — Cl 단독 효과는 0 이고 개선은 상호작용이다
date: 2026-08-16
updated: 2026-08-16
tags: [cascade, esw, oxidation, composition, provenance, b2o3, correction, factorial, attribution]
status: 확정 — 270 슬롯 전수 분류 + Codex f9 리뷰 반영 + **효과 귀속 닫힘**(matched 2×2, main(Cl)=0)
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

## 효과 귀속 — 닫혔다 (2026-08-16, matched 2×2)

`tools/oxidation/esw_matched_factorial.py` 로 네 칸을 chemsys 마다 **같은 pinned entry set**
안에서 쟀다 (11종 · 11 phase set · GPU 미사용).

```
종        H_plain   H_Cl  D_plain   D_Cl |  main(Cl) main(dop)    inter   총합
Al2O3      2.140  2.140    2.140  2.354 |    +0.000    +0.000   +0.214  +0.214
B2O3       2.140  2.140    2.034  2.317 |    +0.000    -0.106   +0.283  +0.177
MoO3       2.140  2.140    2.140  2.356 |    +0.000    +0.000   +0.216  +0.216
WO3        2.140  2.140    2.140  2.356 |    +0.000    +0.000   +0.216  +0.216
Sc2O3      2.140  2.140    2.356  2.339 |    +0.000    +0.216   -0.017  +0.199
Y2O3       2.140  2.140    2.282  2.282 |    +0.000    +0.142   +0.000  +0.142
La2O3      2.140  2.140    1.893  1.925 |    +0.000    -0.247   +0.032  -0.215
Nd2O3      2.140  2.140    1.920  1.987 |    +0.000    -0.220   +0.067  -0.153
Sm2O3      2.140  2.140    1.989  2.034 |    +0.000    -0.151   +0.045  -0.106
MgO/ZnO    2.140  2.140    2.140  2.140 |    +0.000    +0.000   +0.000   0.000
```

총합(`D_Cl − H_plain`)이 캐스케이드 chain 챔피언의 `delta_ox_vs_host_V` 와 **소수점까지
일치한다** — 같은 값을 재현하면서 분해했다.

### ① `main(Cl) = +0.000` — **11/11**

`H_Cl = Li₂₃P₄S₁₉Cl₅` 가 host 와 똑같이 2.140 이다. 도펀트 없이 S 하나를 Cl 로 바꾸는 것만으로는
onset 이 **전혀 안 움직인다**.

> ⛔ **"Cl-rich 가 산화를 개선한다" 는 반증됐다.** 9.63배·2.59배는 Cl 효과가 아니다.

독립 방증: `constrained_esw_cl_scan.json` 의 undoped Cl 스캔도 LPSCl 0.5→1.6 에서 0.000 V
(다른 phase set 이라 절대값은 다르다).

### ② 세 부류

| 부류 | 종 | 읽는 법 |
|---|---|---|
| **상호작용 전용** | Al₂O₃ · MoO₃ · WO₃ | main 둘 다 0.000, interaction +0.214~0.216. **둘이 같이 있어야만** 오른다 — 어느 한쪽도 원인이 아니다 |
| **도펀트 효과** | Sc₂O₃ +0.216 · Y₂O₃ +0.142 | interaction ~0. Cl 없이도 오른다 |
| **도펀트가 내림** | B₂O₃ −0.106 · La₂O₃ −0.247 · Nd₂O₃ −0.220 · Sm₂O₃ −0.151 | 도핑 자체가 onset 을 낮춘다 |
| 무반응 | MgO · ZnO | 네 칸 전부 2.140 |

앞 판에서 "Al₂O₃ 가 유일한 clean 대비" 라고 적었는데, **그것도 상호작용이었다.**

### ③ B₂O₃ — 방향이 정해졌다

한 번도 존재한 적 없던 같은-자리 `D_plain(B₂O₃) = Li₁₈B₂P₄S₁₇Cl₄O₃` 가 **2.034 V** 로 host 아래다.
캐스케이드의 +0.177 은 chain 변형의 추가 개입(**+0.283**)이 도펀트 자체의 **−0.106** 을 덮은 것이다.

legacy DFT-deep 셀 `Li₅₈P₈S₄₁Cl₁₆B₂O₃` 가 **2.03 V** 였다 — **다른 조성인데 같은 방향·거의 같은 값**.
⚠ 이는 **방증이지 동일성 증명이 아니다.** 두 조성을 한 pinned entry set 에서 재는 일은 여전히 안 했다.

### ④ 기전 — 이산적 hull 분기 전환

```
H_plain  Li24P4S20Cl4     → 4 Li3PS4 + LiS4     + 4 LiCl + 7 Li       2.140
H_Cl     Li23P4S19Cl5     → 4 Li3PS4 + 0.75LiS4 + 5 LiCl + 5.25 Li    2.140
D_plain  Li18Al2…Cl4O3    → 4 Li3PS4 + 0.19LiS4 + 4 LiCl + …          2.140
D_Cl     Li17Al2…Cl5O3    → 3.5Li3PS4+ 0.25P2S7 + 5 LiCl + …          2.354
```

2.140 은 **LiS4 에 pin 된 값**이다. Li 가 18→17 로 떨어지는 지점에서 LiS4 가 더는 sink 노릇을
못 해 **P₂S₇ 분기**로 넘어간다. 연속적인 Cl 효과가 아니라 **이산적 분기 전환**이고,
Codex D 관찰(2.340–2.370 V 군 21/21 이 P₂S₇)과 맞물린다.

⚠ 반응식 몇 개를 읽은 관찰이다. Li 문턱이 정확히 어디인지, 다른 도펀트에서도 같은지는 안 쟀다.

## 반증·한계

- **조성 수준 열역학 대비다.** grand-potential ESW 는 조성만 받으므로 그 조성이 **구조적으로
  실현 가능한지**는 말하지 않는다. 자리 점유·배열은 계산 밖이다.
- 캐스케이드의 B₂O₃·MoO₃·WO₃ **기존 plain 챔피언은 `P_4b` 자리**라 이 설계의 `D_plain`(`Li_24g`)과
  **다른 물건**이다. 조성은 맞춰도 자리는 못 맞춘다.
- **보편적 원소 효과가 아니다** — 이 구조 생성 규약 안에서 정의된 대비다.
- legacy `b2o3_esw` 와 캐스케이드를 한 pinned entry set 에서 재는 일은 **여전히 안 했다**.
- **LiS4 포함/제외 phase-roster 민감도(2.140 vs 2.256)는 그대로 열려 있다.** 오히려 ④의 기전이
  그 민감도가 왜 큰지를 설명한다 — 2.140 자체가 LiS4 에 걸린 값이다.
- 이 카드는 **산화 onset 축만** 본다. de(G1)·E/GB(G5) 는 3점 평균이라 조성족이 행 안에서 섞여 있고,
  그쪽 파급은 재지 않았다.
- x 라벨(x002/x005/x010)은 농도가 아니다 — 실측은 셋 다 x=0.25.

## 내가 틀린 것 (2026-08-16, Codex 리뷰 `f9adc9d2`)

| # | 틀린 서술 | 정정 |
|---|---|---|
| ① | "chain = S 하나가 Cl 로 치환" (family 전체) | **10/17 만 exact.** 7행은 치환 자리(P_4b→Li_24g)·Li/P 까지 다름 |
| ② | "같은 방법이므로 B₂O₃ 는 순전히 조성 차이" | legacy 에 `phase_set_id`·entry_ids·MP 버전 없음 — **미확정** |
| ③ | 9.7배 | **9.63배** (pct 를 먼저 반올림한 이중 반올림) |
| ④ | 9.63배를 그대로 인용 | 분모에 chain 후보 없던 237 슬롯 포함 — eligible 33 슬롯이면 **2.59배** |
| ⑤ | selftest `raises()` 가 `except Exception` | 오타로 죽어도 통과했다 — 예외 type·메시지 확인으로 |

①은 Al₂O₃ 한 케이스(정확히 맞는다)에서 family 전체로 일반화한 것이다.
`cation_site` 열을 이미 출력해 보고도 놓쳤다.

## 출처

- `db/properties/cascade_v23_all.csv` (3615행, `charge_compensation` 3105 plain / 510 chain)
- `db/properties/oxidation_stability_cascade_v3_pinned.json` (270 챔피언 + 84 host)
- `db/properties/b2o3_esw.json` (2.03 V, ocv_decomp 의 `16 LiCl` 로 조성 역산)
- 관련: `kb/methodology/cascade_pipeline_anatomy_2026_08_13.md` (G3 phase_set 폐쇄)

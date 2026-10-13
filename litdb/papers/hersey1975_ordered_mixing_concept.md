<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 스캔 고전 메타 형식 = johnson1971_jkr_surface_energy_contact_elastic_solids.md · molerus1975_theory_of_yield_cohesive_powders.md.
     원문 = 4 쪽 스캔 (240 dpi 쪽 이미지 + OCR 텍스트 층) · SI 없음.  쪽 표기 = 인쇄 쪽 p.41–44 (PDF 1 쪽 = p.41).
     판독 규약: OCR 이 식 · 숫자를 깨뜨린다 (예: 저자 이름 'HERSt~Y') — 식 (1)–(7) · 수치 · 그림은 전부 240 dpi 쪽 이미지에서 읽었다.
     값 표지: [인쇄] = 원문 · [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv) · [우리 산술] = 원문 식 · 값으로 한 계산 또는 이 논문 밖 값과 엮은 계산 (가정 명시) · [추정] = 우리 해석 · [미확인] = 원문에 없음. -->

# **정렬 혼합 (ordered mixing)** — 점착 · 상호작용하는 미분은 "무작위로 섞이는 것" 이 아니라 **큰 운반 입자 표면에 붙어 단위체를 이루며 (무질서 → 질서) 섞인다** · 단층 부착 수 n = 4fD²/d² · 미분이 모자라면 다성분 · 넘치면 "정렬 단위체 + 남는 미분" 의 이원 혼합 · 정렬 혼합물은 무작위 혼합물보다 **흔히 더 균질** (예시 계 균질 지수: 완전 정렬 4.11–10.11 vs 무작위 2.60) · 혼합 속도는 같은 1 차 법칙 — J.A. Hersey (Powder Technology 1975)

> slug `hersey1975_ordered_mixing_concept` · DOI `[미확인]` (원문에 인쇄 없음 · PDF 메타데이터 제목 = PII 0032-5910(75)80021-0) · type `theory (powder mixing concept — ordered vs random mixing of cohesive/interacting fine particles on coarse carriers; monolayer adhesion count, Buslik homogeneity index, first-order kinetics; no experiment, no DEM)` · PDF `ab654539-31._Ordered_mixing_A_new_concept_in_powder_mixing_practice.pdf` · digested `2026-10-13` · status ✅
>
> **원제**: *Ordered Mixing: A New Concept in Powder Mixing Practice* (p.41)
> **저자**: J.A. Hersey — Victorian College of Pharmacy, 381 Royal Parade, Parkville, Victoria 3052, Australia (p.41 · OCR 표기 'HERSt~Y' = 쪽 이미지로 Hersey 확인)
> *Powder Technology* **11** (1975) 41–44 · © Elsevier Sequoia S.A., Lausanne · 접수 1974-05-16 (p.41).
> **판독 원자료**: `litdb/figures/hersey1975_ordered_mixing_concept/digitized.csv` (Fig 1 격자 판독) · 크롭 1 장 `figures.json`.
> **이 카드가 서랍에 들어온 이유**: 이종기술 논지 (`docs/hetero_thesis.md`) §2-5 가 *"작은 입자가 큰 운반 입자 표면에 붙으며 섞이는 혼합을 제약 분체에서 상호작용 · 정렬 혼합이라 부른다 — 용어 · 이론의 정본 카드 없음 [미확인]"* 로 남겨 둔 빈칸 — **그 용어의 원전**.  1저자 읽기 목록 `docs/mixer_coating_reading_list_20261013.md` B3-2 (★★★) · Part D 순번 6 — 목록이 *"인용 문헌 쪽 요약"* 으로만 적었던 "미분이 굵은 입자 표면에 붙어 단위를 이룬다" 는 설명은 **원문 p.42 THEORY 에 있다** (이 카드에서 확인).  (같은 번호 31 의 다른 업로드 *Electro-Chemo-Mechanical Coupling …* 는 별도 정본 카드 `li2026_electrochemomechanical_coupling_asslmb_review` — 이 카드와 무관.)

> ★★ **한 줄로 왜 중요한가**: 우리 논지의 그림 — **SE (1 µm) 가 NCM (4–9 µm) 표면에 붙어 코팅된 단위체를 만들고, 그 단위체끼리 압축되어 이온 경로가 이어진다** — 은 Hersey 의 정렬 혼합 그 자체다 (운반체 = NCM · 미분 = SE · 상호작용 = 접착).  이 논문은 (i) 그런 혼합물은 **무작위 혼합을 기준으로 한 균질 지수 (Lacey 등) 로 재면 안 된다** 는 것, (ii) 운반체 표면의 **단층 수용량** 으로 "미분이 모자라는가 · 넘치는가" 를 가르는 산술, (iii) 미분이 넘치면 **남는 미분이 따로 (무작위로) 섞인다** 는 것을 준다.
> ⚠ 단 **실험 · 시뮬레이션이 없는 개념 논문** (4 쪽) 이고 예시 숫자는 가상의 1 wt% 미분 (5 µm) / 운반체 (500 µm) 계다.  기전 (접착 · 정전기 · 표면장력 …) 은 열거만 한다.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 응집 · 상호작용이 없는 거친 분말은 무작위화 (randomization, 원문 표현 "shuffling") 로 섞이지만, 점착성 미분이 섞인 계에서는 미분이 큰 입자 표면의 부착 자리에 붙어 **질서 있는 단위체** (원문 "ordered unit") 를 이루는 **정렬 혼합** 이 일어나며, 이때는 크기 · 무게가 같을 필요가 없고, 단위체가 모두 같아지면 계 전체가 **한 물질처럼** 다뤄져 무작위 혼합보다 **흔히 (frequently) 더 균질** 하다 (예시 계에서는 "considerably") — 혼합 속도는 남은 미분 수에 비례하는 1 차 법칙이라 무작위 혼합과 속도식만으로는 구별되지 않는다 [인쇄 p.41–44].

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 논지 §2-5 의 "정렬 혼합" 용어 · 원전? | **이 논문이 원전** — "disorder to order" 개념 · 상호작용 (흡착 · 화학흡착 · 표면장력 · 마찰 · **정전기** · 기타 접착) 이 필요 · 크기 · 무게 같을 필요 없음 · 몇 개의 큰 입자 + 많은 작은 입자에서 일어나기 쉽다 | [인쇄] p.41 |
| ② 우리 조성에서 SE 가 NCM 표면을 다 덮을 수 있나? | 단층 수용량 n = 4fD²/d² (식 1) · 육방 n = 2π(D+d)²f/(√3 d²) (식 2).  우리 생성기 조성 (AM 80 · SE 18 wt% · P:S 7:3 · 밀도 4.8 · 2.0 · 지름 9 · 4 · 1 µm) 이면 AM_P 하나당 단층 **324 (식 1) · 363 (식 2) 개**, AM_S **64 · 91 개** · SE 개수는 전체 단층 수용량 (f = 1) 의 **0.88 (식 1) · 0.70 (식 2)** ⇒ **SE 를 전부 붙여도 단층 하나의 70–88 % 를 채우는 양** — f = 1 기준으로는 미분 과잉이 아니다 · 포화 분율 f 가 작으면 (Hersey 예 0.25) 과잉 쪽으로 넘어간다 (§3-7) [우리 산술] | [인쇄] 식 (1) · (2) · [우리 산술] |
| ③ 미분이 넘치면? | 모든 자리를 채우고 **남는 미분은 단위체와 무작위로 섞인다** — 예: 미분 10 % 면 단위체 90.9 % + 남는 미분 9.1 % 의 이원 혼합 · 모자라면 단위체마다 붙은 수가 달라 **다성분** 계 | [인쇄] p.42–43 |
| ④ 우리 **Lacey M** 으로 정렬 혼합을 재도 되나? | **무작위 혼합의 불균질을 기준으로 한 균질 연구는 정렬 혼합물에 만족스럽지 않다** — 대신 요구 균질도 · 표준 불균질도 기준 (Hersey 1967 · Buslik 1973).  ⇒ 무작위 기준 정규화 지수 (Lacey · PSMI · GNN) 에서 정렬 혼합물은 **1 을 넘을 수 있다** (Fig 1a 판독: 이웃이 서로 다른 비율 1.00 vs 무작위 기대 ≈ 0.50 ⇒ ×2.0) [판독 · 우리 산술] | [인쇄] p.42 · [판독] Fig 1 |
| ⑤ 균질 정도 수치? | Buslik 균질 지수 H_i = −log W₁ (W₁ = 표준편차 1 % 를 주는 시료 무게) — 1 wt% 예에서 **완전 정렬 4.11 < H_i < 10.11** vs 같은 계 무작위 **2.60** (정제 ±15 % 기준) · **−2.00** (덩어리 시료) | [인쇄] p.43 |
| ⑥ 혼합 속도로 정렬 · 무작위를 가를 수 있나? | **못 가른다** — 둘 다 1 차 (지수) 법칙 · 다만 크고 작은 입자 혼합은 무작위로는 아주 느리게 섞이고 빨리 분리되는데 정렬 과정이면 **매우 빨리** 섞일 수 있다 ⇒ "실제 속도" 가 단서 | [인쇄] p.43–44 |

⛔ **한정어 (떼지 말 것)**: ① **개념 · 산술 논문** — 측정 · 모사 없음 ② 예시 = 5 µm 미분 1 wt% · 500 µm 운반체 (밀도 1.2 g cm⁻³ 가정) ③ 단층 수용량 식은 **투영 면적 · 단층 · 구** 가정 (f 로 불완전 충전을 흡수) ④ 상호작용 기전은 열거뿐 (어느 힘이 지배하는지 다루지 않음) ⑤ 1975 년 제약 분체 맥락 (정제 윤활제 · 미량 약물) ⑥ "더 균질" 은 SUMMARY 의 **"frequently"** — 늘 그렇다는 주장이 아니고, 4.11–10.11 은 **완전 정렬 · 평형** 을 가정한 상한 쪽 값이다.

---

## 1. 한 줄 요약

**분말 혼합 이론이 "같은 크기 · 같은 밀도 입자를 무작위로 섞는다" 만 다뤄 왔는데, 실제로는 점착성 미분이 소량 섞인 계가 높은 균질도로 섞인다 — 그 기전으로 미분이 큰 입자 표면에 붙어 질서 있는 단위체를 만드는 '정렬 혼합' 을 제안하고, 단층 부착 수 · 평형 (부족 · 포화 · 과잉) · Buslik 균질 지수 · 1 차 혼합 속도로 개념을 정리한 4 쪽 논문.**  응용 예 = 정제 과립에 윤활제를 섞는 것.

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| J.A. Hersey (Victorian College of Pharmacy, Australia) | *Powder Technol.* 11 (1975) 41–44 | [미확인] (PII 0032-5910(75)80021-0, PDF 메타데이터) | 가상의 예: 미분 d = 5 × 10⁻⁴ cm (5 µm) 1 wt% · 운반체 D = 5 × 10⁻² cm (500 µm) · 밀도 1.2 g cm⁻³ | **이론 · 개념** (실험 · 모사 없음) |

> ★ **계보**: 제약 분체 (미량 약물 · 윤활제 혼합) 맥락.  저자 선행 = Hersey 1967 (*J. Pharm. Pharmacol. Suppl.* 19, 168S–176S — 혼합물 균질 평가, ref 11) · Hersey 1972 (*Australian J. Pharm. Sci.* NS1(3), 76–78 — 혼합 문제 피하기, ref 4).  균질 지수 = Buslik 1973 (*Powder Technol.* 7, 111–116, ref 12).  무작위 혼합 기준의 예 = **Lacey 1954** (ref 8 — 같은 날 카드 후보 #30) · Ashton & Valentin 1966 (ref 9) · Stange 1954 (ref 10).
> ★ 용어 주의: 이 논문이 쓰는 말은 *"cohesive, interacting particulate systems"* 와 *"ordered mixing"* 이다 — **'interactive mixing' 이라는 이름은 이 논문에 없다**.  논지 §2-5 · §6 의 *"상호작용 (ordered/interactive) 혼합"* 표기 중 'interactive' 쪽 근거는 이 카드로 닫히지 않는다 [미확인 — 별도 원문 필요].

## 3. 핵심 수치 · 식 (★ 전부 쪽 · 표지 병기)

### 3-1. 개념 (SUMMARY · INTRODUCTION · p.41–42)
| 항목 | 내용 | 표지 |
|---|---|---|
| 무작위화 | 비점착 · 비상호작용 입자 · **같은 크기 · 같은 무게** · 표면 효과 거의 없음 · 확산 · 대류로 섞음 (혼합 이론을 정량화하는 데 쓸모) — 단 점착 · 상호작용 계에는 다 적용되지 않는다 | [인쇄] p.41 |
| 미분이 왜 정렬로 가나 | 미분을 무작위로 섞지 못할 **이론적 이유는 없다** — 그러나 점착 · 표면 현상이 **입자가 고울수록 커져** 혼합을 무작위가 아니라 정렬 쪽으로 민다 | [인쇄] p.41 |
| 정렬 혼합 | 점착 · 상호작용하는 미분 — **"disorder to order"** · 크기 · 무게 같을 필요 없음 · **입자 상호작용 필요**: 흡착 · 화학흡착 · 표면장력 · 마찰 · **정전기** · 기타 접착 · "실제 계에서 아마 널리 일어난다" | [인쇄] p.41 |
| 일어나는 곳 | 큰 (검은) 입자 몇 개 + 작은 (흰) 입자 많이 (Fig 1 은 같은 비율 모식) | [인쇄] p.41–42 |
| 크기 차가 클 때 | 미분 · 거친 입자는 **섞이는 속도보다 빨리 분리** — 상호작용 힘을 이용하지 않으면 | [인쇄] p.41 |
| 근거 (문헌) | 혼합 관찰 [3, 4] · 안식각 자료 [5–7] — 미분 접착이 계 성질을 크게 바꾼다 | [인쇄] p.42 |
| 균질 기준 | 완전 무작위 혼합물의 불균질을 기준으로 한 연구 [8–10] 는 **정렬 혼합물에 만족스럽지 않다** · 요구 균질도 [11] · 표준 불균질도 [12] 기준이 유용 | [인쇄] p.42 |
| 혼합 속도 | 로그 (1 차) 관계 [13] — 정렬 혼합에도 1 차 | [인쇄] p.42 |

### 3-2. 단층 부착 수 (THEORY · p.42 · 쪽 이미지 판독)
- 큰 입자 표면적 πD² · 작은 입자 하나의 투영 면적 πd²/4 ⇒ 단층 최대 **4D²/d²**.
- 불규칙 충전 · 빈 자리를 고려해 **실제 붙는 분율 f**: **n = 4fD²/d²** (식 1).
- 더 정확한 해 (작은 입자 육방 밀집, ref 7): **n = 2π(D + d)²f / (√3 d²)** (식 2).
- **예**: 1 wt% · d = 5 × 10⁻⁴ cm · D = 5 × 10⁻² cm · 밀도 1.2 g cm⁻³ · 1 g 시료 ⇒ N_d·π(d³/6)·1.2 = 0.01 → **N_d = 1.27 × 10⁸** · N_D·π(D³/6)·1.2 = 0.99 → **N_D = 1.26 × 10⁴** ⇒ **n = N_d/N_D = 1.0 × 10⁴** ⇒ 식 (1) 에서 **f = 0.25** [인쇄].
- [우리 산술] 재현: N_d 1.273 × 10⁸ · N_D 1.261 × 10⁴ · n 10,101 · f = 0.253 (식 1) · **0.273 (식 2)**.

### 3-3. 평형 상황 (p.42–43)
| 경우 | 결과 | 표지 |
|---|---|---|
| 포화 (예의 1 wt%) | 큰 입자마다 10⁴ 개 · **모든 단위체 동일 → 한 물질처럼** | [인쇄] p.42 |
| 미분 부족 | 부착 자리를 다 못 채움 → 단위체마다 붙은 수가 달라 **다성분** 계 · 또는 **활성 자리** 가 먼저 포화되어 한 성분 계 (f 가 최대보다 작아짐) | [인쇄] p.42 |
| 미분 과잉 | 모든 자리를 채우고 **남는 미분은 무작위로** 섞인다 → 이원 혼합 (조성은 넣은 성분비와 다름) · 예: 미분 10 % → 거친 입자 90 % 가 미분 0.9 % 와 평형 → **단위체 90.9 % + 남는 미분 9.1 %** | [인쇄] p.43 · [우리 산술 0.909 %] |

### 3-4. 균질 (Homogeneity · p.43 · 식 3–7)
- Buslik: **H = 1/W₁** (W₁ = 표준편차 1 % 를 주는 시료 무게) · 로그 척도 **H_i = −log W₁** (식 3).
- 무작위 혼합물: **σ² = G(100 − G)w/W** (식 4; G = 성분 %, w = 유효 평균 입자 무게, W = 시료 무게 — 모든 입자가 같은 무게일 때, 다분산이면 보정 필요) ⇒ σ = 1 % 이면 **W₁ = G(100 − G)w** (식 5) ⇒ **H_i = −log[G(100 − G)w]** (식 6).
- 단일 성분의 한계: Buslik 은 순수 수소 기체의 최소 시료 = 분자 하나 → H_i 한계 **23.5** · 염화나트륨은 Na⁺ 또는 Cl⁻ → **22.0–22.2** 사이 불연속.
- **완전 정렬계**: 성분이 한 물질처럼 → 시료가 단위체 하나보다 작아야 하므로 H_i 는 큰 입자 무게 W_D = 1.2π D³/6 과 작은 입자 무게 W_d = 1.2π d³/6 사이 ⇒ **4.11 < H_i < 10.11** [인쇄] (우리 산술 4.10 · 10.10 — 둘째 자리 반올림 차).
- 미분 0.5 % 여도 평형만 이뤄지면 같은 범위 · 과잉 (10 %) 이면 정렬 + 무작위가 함께 일어나 복잡.
- **같은 1 wt% 를 무작위로 (1 g 시료)**: (가) 시료가 입자 하나 무게의 덩어리라면 H_i = −log[G(100 − G)W] = −log(99 × 1 × 1) = **−2.00** · (나) 정제처럼 함량 범위 ±15 % (평균의) 를 요구하면 3σ = 0.15 × 1 → σ = 0.05 → 식 (4) 를 (6) 에 넣어 **H_i = −log σ²W** (식 7) = **+2.60** — 둘 다 완전 정렬계보다 훨씬 덜 균질 (원문 *"considerably less than the homogeneity that could be obtained for the completely ordered system"*) [인쇄].

### 3-5. 혼합 속도 (RATE OF MIXING · p.43–44)
- 정렬 혼합 = **1 차 반응속도** (남은 붙지 않은 미분 수에 비례) — 무작위 혼합에도 같은 속도식 [13] → **속도식만으로는 구별 불가**.
- 그러나 거칠고 같은 크기 · 무게 입자는 빨리 무작위화되고, **크고 작은 입자 혼합은 무작위로는 아주 느리게 섞이고 매우 빨리 분리** 하는데, 정렬 과정이면 **매우 빨리** 섞일 수 있다 ⇒ 실제 혼합 속도가 혼합 유형의 단서.

### 3-6. 응용 (APPLICATION · p.44)
- 문헌의 혼합 이론은 "같은 크기 · 같은 밀도 입자만 미세 균질도로 섞인다" 고 만장일치 — 실제로는 **소량 미분이 거친 재료에 높은 균질도로** 들어간다 (예: **정제 과립에 윤활제**).  정렬 혼합이 그 이해 수단.

### 3-7. ★ 우리 산술 — 우리 조성에 Hersey 산술 적용
| 항목 | 값 | 가정 |
|---|---|---|
| SE / AM_P 개수비 | **562** (생성기 주석과 같다) | 조성 AM 80 (P:S 7:3) · SE 18 wt% · 밀도 AM 4.8 · SE 2.0 g cm⁻³ · 지름 AM_P 9 · AM_S 4 · SE 1 µm (`scripts/make_mixer_deck.py` `WT` · `PS` · `DENS` · 실측 지름 표) |
| SE / AM_S 개수비 | **115** | 같음 |
| 단층 수용량 (f = 1) AM_P · AM_S | 식 (1) **324 · 64** · 식 (2) **363 · 91** | 구 · 투영 면적 · 단층 |
| SE 개수 ÷ 전체 단층 수용량 | **0.88 (식 1) · 0.70 (식 2)** | 모든 AM 표면 · 모든 SE 가 단층으로 붙는다고 가정 (f = 1) |
| 포화 분율을 Hersey 예의 f = 0.25 로 빌리면 | 붙는 SE **28 % (식 1) · 36 % (식 2)** · 나머지 **64–72 %** 는 자유 SE (Hersey 의 '과잉 미분') | f = 0.25 는 Hersey 예에서 1 wt% 를 포화로 **둔** 값 (측정 아님) |
| 해석 | f = 1 이면 SE 를 전부 붙여도 **단층 하나의 70–88 %** — 과잉이 아니다.  포화 분율이 작으면 (f ≈ 0.25) 같은 조성이 **과잉 미분** 쪽으로 넘어간다 ⇒ 우리 조성은 **f 에 따라 '포화 이하' 와 '과잉' 의 경계 근처** 에 있다 | [추정] |
- ⚠ 실제 SE 는 응집 덩어리 · 다분산 · 비구형이고 압밀 전 혼합 상태이며, 실제 전극에서는 VGCF · PTFE 도 AM 표면을 나눠 쓴다 (믹서 생산 덱은 AM_P · AM_S · SE 세 상만 — `make_mixer_deck.py` 주석) — **차수 감각** 으로만.

---

## 4. ★ 방법 — 논증 구조 · 입자 처리

### 4-1. 논증 구조
① 기존 이론 = 무작위화 (같은 크기 · 무게 · 상호작용 없음) → ② 실제 = 점착 미분이 높은 균질도로 섞임 → ③ 정렬 혼합 개념 (상호작용으로 단위체) → ④ 단층 부착 수 산술 (식 1 · 2, 예 f = 0.25) → ⑤ 평형 (부족 · 포화 · 과잉) → ⑥ Buslik 균질 지수로 정렬 ↔ 무작위 비교 (4.11–10.11 vs 2.60 · −2.00) → ⑦ 1 차 속도 (구별 불가 · 실제 속도가 단서) → ⑧ 응용 (윤활제).

### 4-2. ★ 입자 처리 (우리 축 언어로)
- **구 · 단층 · 투영 면적** 의 기하 산술만 — 힘 · 동역학 · 접촉 모델 없음.
- 운반체 = 큰 구 · 미분 = 작은 구 · "붙음" = 부착 자리 점유 (확률 f).

### 4-3. 기법 미니 용어집
- **무작위화 (randomization)** — 입자 위치를 섞어 성분이 무작위로 분포하게 하는 혼합.
- **정렬 혼합 (ordered mixing)** — 미분이 운반체 표면에 붙어 같은 단위체들을 만드는 혼합.
- **운반체 (carrier)** — 미분이 붙는 큰 입자 (이 논문의 D).
- **단층 수용량** — 운반체 표면에 미분이 한 겹으로 붙을 수 있는 최대 수.
- **Buslik 균질 지수 H_i** — 표준편차 1 % 를 주는 시료 무게의 −log.
- **1 차 혼합 속도** — 남은 미혼합량에 비례해 줄어드는 지수형 혼합 곡선.

---

## 5. Figure set ★ (크롭 1 장 = `litdb/figures/hersey1975_ordered_mixing_concept/`)

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | (a) 같은 비율 검정 · 흰 입자의 **정렬 혼합물** (9 × 9 바둑판) · (b) 같은 비율의 **무작위 혼합물** (9 × 9) | ★ "무작위 기준 지수에서 정렬 혼합은 1 을 넘는다" 를 보이는 그림 — 우리 판독 (격자 전체 = digitized.csv): 검정 (a) 41 · (b) 40 / 81 칸 · 상하좌우 이웃 쌍 144 개 중 색이 다른 쌍 (a) **144 (1.00)** · (b) **85 (0.59)** · 무작위 기대 2p(1−p) ≈ **0.50** (칸 수 고정 비복원 기준 0.506) ⇒ 비 **≈ 2.0 · ≈ 1.2** [판독 · 우리 산술].  ⚠ (b) 의 0.59 는 같은 칸 수의 무작위 배치 20 만 번 표본 (평균 0.506 · 표준편차 0.041) 의 **상위 약 2.6 %** — 손 그림 모식이라 '전형적 무작위' 보다 약간 더 엇갈리게 그려졌다 [우리 산술 · 그림 모식에 의미 두지 않음] |

## 6. Post-processing ★
- 원문: 손 산술만 (개수 · 단층 수 · f · H_i).
- **우리 후처리 (이 카드)**: §3-2 예시 재현 · 식 (2) 의 f · H_i 경계 재계산 · §3-7 우리 조성의 단층 수용량 · Fig 1 의 9 × 9 격자 판독 (칸 중앙 40 % 창의 평균 밝기 < 128 = 검정 · 격자를 겹쳐 눈으로 81 칸 전수 대조) → 이웃 다른 색 비율 vs 무작위 기대 (해석식 + 같은 칸 수의 무작위 순열 20 만 번 표본).

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태)

| 항목 | 이 논문 (Hersey 1975) | 우리 (논지 · 믹서 DEM · 압축 DEM) | 차이 / 판정 |
|---|---|---|---|
| 혼합 그림 | 운반체 + 미분 단층 = 정렬 단위체 | 코팅 NCM (AM 표면 = SE) — 논지 §2-5 · LC 팔 = "AM 쌍 점착을 SE–SE 와 같은 γ 로" (논지 §2-6) | ★ 같은 그림 — 우리는 **힘 (CED) 으로** 그 상태를 만들려 한다 |
| 정렬의 조건 (미분–운반체 부착) | 상호작용 필요 — 미분이 운반체에 붙어야 단위체가 선다 | AM–SE CED = 두 상 CED 의 **min** → 같은 γ 기하 환산보다 **2.2 배 약하다** (논지 §2-6) | ⚠ LC 에서도 정렬 쪽 (SE→AM 부착) 이 덜 표현된다 — 정렬 혼합이 약하게 나오면 먼저 이 규칙을 의심 |
| 미분 양 | 포화 · 부족 · 과잉 | SE 18 wt% = 단층 수용량 (f = 1) 의 0.70–0.88 (§3-7) | f = 1 이면 포화 이하 · f ≈ 0.25 면 과잉 — **f 에 따라 경계 근처** [우리 산술 · 추정] |
| 균질 지표 | 무작위 기준 지표는 부적합 · Buslik H_i | Lacey M (S_R² = 균일 삽입 런) · s1 (SE–SE 접촉 군집) · s2 (AM–SE 부착) | ★ 정렬 상태를 재려면 **이웃 · 접촉 지표 + 상한 없는 정규화** (같은 날 카드 `chandratilleke2012_…` §8 항목 5) · s1 은 껍질 ↔ 자유 덩어리를 못 가른다 (§8 항목 4) |
| 기전 | 상호작용 열거 (정전기 포함) | SJKR 점착만 · 정전기 없음 (논지 §2-7) | 우리 모델은 정전기 정렬을 표현 못 한다 |
| 속도 | 1 차 · 정렬은 빠를 수 있다 | M(t) 의 지수 포화 (hare2026 식 (12) 꼴) | 속도로 정렬 · 무작위를 가르지 말 것 (구조 지표로) |

### 7-1. frame[5]
개념 논문 — DEM · MPM 어느 반쪽도 없다.  우리 파이프라인에서는 **혼합 상태의 목표 그림과 그 지표 선택의 근거**.

---

## 8. ★★ 우리 연구에 주는 insight (번호마다: 논문이 보인 것 → 우리에게 뜻 → 할 일)

1. **논지 §2-5 의 [미확인] 표지를 절반 걷을 수 있다 — '정렬 혼합' 의 원전은 이 논문.**  "정렬 혼합" = 상호작용하는 미분이 운반체에 붙어 같은 단위체들을 이루는 혼합 (Hersey 1975).  → 논지 문서의 해당 문장에 이 카드를 근거로 걸 수 있다 (§2-5 는 비준 블록 밖 문장이지만 수정 여부는 1저자 결정).  ⚠ 'interactive mixing' 이라는 이름의 근거는 이 논문에 없다 — 그 절반은 [미확인] 그대로.
2. **우리 조성은 '포화 이하' 와 '과잉' 의 경계 근처 — f 가 가른다.**  SE 18 wt% 를 다 붙여도 단층 (f = 1) 의 70–88 % 이지만, 포화 분율이 Hersey 예처럼 0.25 면 SE 의 64–72 % 가 남는다 (§3-7).  → 논지 P1 ("비코팅에서 SE–SE 응집이 무작위보다 크게 남는다") 의 '남는 SE' 는 Hersey 의 **과잉 미분** 에 해당하고, 그 양은 **SE 함량 (포화 비)** 과 **붙는 정도 (f — 표면 에너지 · 코팅이 바꾸는 쪽)** 가 **같이** 정한다 [추정].  → 코팅 ↔ 비코팅 대조를 한 조성에서만 하면 두 효과가 섞인다 — DEV 설계에 **SE 함량 축** (단층 수용량 대비 0.5 · 1 · 2 배) 을 두면 정렬 ↔ 과잉의 경계를 직접 볼 수 있다 [제안 · 결과 전 등록 대상].
3. **정렬 혼합은 무작위 기준 지표를 넘어선다 — 상한을 두지 말 것.**  Fig 1 판독에서 이웃이 다른 비율이 무작위의 약 2 배.  → Lacey 형 · PSMI 형 지표에서 코팅 팔이 **M > 1** 을 내면 그것은 오류가 아니라 정렬 신호일 수 있다 — 판독기에서 [0, 1] 로 자르지 말고 그대로 보고 (같은 날 카드 `chandratilleke2012_particle_scale_mixing_index` §8 항목 5 와 같은 결론).
4. **★ s1 (SE–SE 접촉 군집) 단독으로는 '자유 SE 덩어리' 와 'AM 표면의 SE 껍질' 을 못 가른다.**  완전 정렬 (코팅된 상태) 에서도 한 AM 표면의 SE 들은 옆으로 서로 닿아 **연결된 SE 군집** 을 이룬다 — 우리 조성은 단층 수용량의 70–88 % 라 껍질이 촘촘하다 (§3-7).  `scripts/mixer_contact_reader.py` 의 s1 은 "겹친 SE–SE 쌍의 연결 성분" 이라 AM 접촉 여부를 보지 않는다 ⇒ **s1 이 크다 = SE–SE 응집 (P1)** 으로 바로 읽으면 정렬 (P2 쪽) 과 혼동할 수 있다 [추정].  → 군집마다 AM 접촉 여부를 붙인 분해 (AM 에 닿지 않은 SE 군집 = Hersey 의 자유 미분 덩어리) 가 P1 의 깨끗한 신호다 — 새 관측량이면 **결과 전 등록** 대상 [제안].
5. **min 혼합쌍 규칙은 정렬의 조건을 약하게 만든다.**  Hersey 의 정렬 = 미분이 운반체에 **붙어야** 선다.  우리 덱의 AM–SE CED 는 min 규칙이라 같은 γ 기하 환산보다 2.2 배 약하다 (논지 §2-6) ⇒ LC 에서도 정렬이 덜 나올 수 있다.  같은 날 정본 카드 `begat2004_cohesive_adhesive_balance_afm_colloid_probe` §7-3 이 같은 결론 (min 규칙은 "접착 > 두 응집" 쌍 = 정렬 혼합 조건을 구조적으로 못 낸다) 을 측정 CAB 로 보인다 → 논지 D2 (결합 규칙) 결정의 근거 묶음.
6. **속도로는 못 가른다 — 구조 지표가 필요.**  정렬 · 무작위 둘 다 1 차 속도.  → 코팅 ↔ 비코팅 비교는 M(t) 의 속도상수가 아니라 **AM–SE 접촉 비 (무작위 기대 대비) · SE 군집 크기 (위 4 의 분해)** 로 (논지 §5 관측량).
7. **정전기가 정렬 혼합의 후보 힘으로 명시돼 있다.**  우리 모델에 없는 힘 (논지 §2-7).  → 실제 건식 혼합에서 SE 가 NCM 에 붙는 것이 접착 (표면 에너지) 인지 마찰 대전인지 가르는 실험이 없으면, 코팅 효과를 표면 에너지만으로 설명하지 않는다.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
> 아래 영문은 원문 내용을 **우리가 다시 쓴 문장** 이다 (원문 문장을 그대로 옮긴 것이 아님 — 괄호 쪽이 근거).  원문 그대로가 필요하면 마지막 줄의 짧은 원문 구절만 쓴다.
- "Ordered mixing, in which interacting fine particles adhere to coarse carrier particles to form identical units, was proposed as an alternative to randomization for cohesive powders; it does not require equally sized or weighted particles but requires particle interaction (adsorption, chemisorption, surface tension, friction, electrostatics or other adhesion) (Hersey, Powder Technol. 1975)." [인쇄 p.41–42 내용]
- "Homogeneity assessments based on the completely randomized mixture are unsatisfactory for ordered mixtures (Hersey 1975)." [인쇄 p.42 내용]
- "For 1 wt% of 5 µm fines on 500 µm carriers, about 10⁴ fines adhere to each carrier (f = 0.25 of a monolayer by Eq. 1), and the homogeneity index of the completely ordered mixture (4.11–10.11) is considerably higher than that of the randomized one (2.60) (Hersey 1975)." [인쇄 p.42–43 내용]
- 원문 구절 (그대로): *"disorder to order"* · *"Ordered mixtures are frequently more homogenous than random mixtures"* (SUMMARY, p.41 — 원문 철자 'homogenous').
- ⚠ §3-7 의 우리 조성 산술 (0.70–0.88) 은 [우리 산술] — 원문 값으로 인용하지 말 것.

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **실험 · 모사 없음** — 개념 · 가상 예시.
2. **단층 · 구 · 투영 면적** 가정 — 다층 · 비구형 · 다분산 · 응집 미분 무시.
3. **힘 · 동역학 없음** — 정렬이 깨지는 조건 (충돌 · 전단에 의한 탈착) 을 다루지 않는다.
4. **균질 지수 산술의 단위** — G 는 % · σ 도 % 단위 (정제 예의 σ = 0.05 = 평균 1 % 의 ±15 % / 3) — 식을 옮길 때 단위 일치 필요.
5. **H_i 경계 반올림** — 재계산 4.10 · 10.10 ↔ 인쇄 4.11 · 10.11 (0.01 차).
6. **OCR 손상** — 텍스트 층으로 식 · 숫자를 옮기지 말 것 (이 카드의 식은 쪽 이미지에서 읽음).
7. **1975 년 제약 맥락** — 배터리 복합양극 (압축 · 이온 경로) 으로의 확장은 우리 추론.
8. **"더 균질" 의 범위** — SUMMARY 는 *"frequently more homogenous"* · 본문 비교는 **완전 정렬 · 평형** 단위체를 가정한 H_i 경계와 무작위 계의 비교다.  불완전 정렬 (부족 · 과잉 · 비평형) 의 H_i 는 다루지 않는다 (과잉은 "복잡하다" 고만 적는다).
9. **포화 f 는 정의값** — 예시의 f = 0.25 는 1 wt% 를 포화 (평형) 로 **두고** 거꾸로 푼 값이다.  실제 포화 분율의 측정 · 예측 방법은 없다.
10. **참고문헌 8 (Lacey) 의 학술지 표기** — 원문 목록은 *"J. Appl. Chem. Biotechnol., Lond., 4 (1954)"* 로 적는다 (그대로 옮김).  같은 날 받은 Lacey 원저 PDF 의 메타데이터는 *"Journal of Applied Chemistry 1954"* — 학술지 이름 대조는 그 카드 (#30) 에서.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 번호 | 서지 (원문 목록 그대로 · 쪽 이미지 판독) | 왜 · 카드 |
|---|---|---|
| 3 | D.N. Travers and R.C. White, The mixing of micronized sodium bicarbonate with sucrose crystals, J. Pharm. Pharmacol., Suppl., 23 (1971) 260S–261S | 정렬 혼합의 관찰 근거 — 카드 없음 |
| 4 | J.A. Hersey, Avoiding powder mixing problems, Australian J. Pharm. Sci., NS1(3) (1972) 76–78 | 정렬 혼합의 관찰 근거 (저자 선행) — 카드 없음 |
| 5 · 6 | D.J. Craik, The flow properties of starch powders and mixtures, J. Pharm. Pharmacol., 10 (1958) 73–79 · D.J. Craik and B.F. Miller, The flow properties of powders under humid conditions, J. Pharm. Pharmacol., Suppl., 10 (1958) 136T–142T | 안식각 근거 (미분 접착이 계 성질을 바꾼다) — 카드 없음 |
| 7 | T.M. Jones and N. Pilpel, Some physical properties of lactose and magnesia, J. Pharm. Pharmacol., 17 (1965) 440–448 | 식 (2) 의 출처 — 카드 없음 |
| 8 | P.M.C. Lacey, Development in the theory of particle mixing, J. Appl. Chem. Biotechnol., Lond., 4 (1954) 257–268 | **Lacey 원저** — 같은 날 카드 후보 (#30) |
| 11 | J.A. Hersey, The assessment of homogeneity in powder mixtures, J. Pharm. Pharmacol., Suppl., 19 (1967) 168S–176S | 요구 균질도 기준 — 카드 없음 |
| 12 | D. Buslik, A proposed universal homogeneity and mixing index, Powder Technol., 7 (1973) 111–116 | 균질 지수 H_i — 카드 없음 |
| 13 | J.M. Coulson and N.K. Maitra, The mixing of solid particles, Ind. Chem. Mfr., 26 (1950) 55–60 | 1 차 혼합 속도 — 카드 없음 |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 4 쪽 스캔 = 240 dpi 쪽 이미지로 본문 전수 판독 (OCR 텍스트 층은 보조) — 식 (1)–(7) · 예시 숫자 · H_i 값 · 참고문헌 서지.
- 그림 1 = 크롭 1 장 (쪽 이미지 240 dpi 그대로 · 캡션 제외) — 표 없음.
- 수치 재현: N_d · N_D · n · f (식 1 · 2) · H_i 경계 · 과잉 예시 0.909 % · 우리 조성의 단층 수용량 · f = 0.25 가정의 자유 SE 몫 — scratch (저장 안 함), 결과는 §3-2 · 3-4 · 3-7 · Fig 1 격자 판독과 무작위 순열 표본은 digitized.csv.
- 우리 쪽 대조: 조성 · 밀도 · 지름 = `scripts/make_mixer_deck.py` (`WT` · `PS` · `DENS` · `D_REAL_UM` · SE/AM_P = 562 주석) · s1 · s2 정의 = `scripts/mixer_contact_reader.py` 머리말 · LC · min 규칙 = 논지 §2-6.
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 + 'Hersey' · 'ordered mixing' · '정렬 혼합' 전수 grep — 이 논문 카드 없음 (begat2004 · chandratilleke2012 가 용어만 언급).  같은 번호 31 의 다른 업로드 (Electro-Chemo-Mechanical Coupling = `li2026_electrochemomechanical_coupling_asslmb_review`) 와 혼동하지 않음.

## 🔗 관련 카드
- 같은 날 · 혼합 지표: [`chandratilleke2012_particle_scale_mixing_index`](chandratilleke2012_particle_scale_mixing_index.md) (정렬 = M > 1 가능) · [`jarray2019_cohesion_driven_mixing_segregation_drum`](jarray2019_cohesion_driven_mixing_segregation_drum.md) · [`nadeem2023_gnn_mixing_index`](nadeem2023_gnn_mixing_index.md).
- 같은 날 · 점착 균형 · 보정: [`begat2004_cohesive_adhesive_balance_afm_colloid_probe`](begat2004_cohesive_adhesive_balance_afm_colloid_probe.md) (CAB — salbutamol on lactose = 정렬 쪽 극단 · min 규칙 충돌 §7-3) · [`alizadeh2018_dem_adhesion_calibration_segregation_heap`](alizadeh2018_dem_adhesion_calibration_segregation_heap.md) (과점착 = 미분이 붙은 덩어리).
- SE 건식 코팅 NCM (실물 · 정렬 혼합의 배터리판): [`nakamura2020_dry_coating_ncm_li3ps4_core_shell`](nakamura2020_dry_coating_ncm_li3ps4_core_shell.md) (충격 블렌딩 껍질 · 같은 SE 량의 막자 혼합 대비) · [`lee2026_mechanical_halogen_argyrodite_drycoating`](lee2026_mechanical_halogen_argyrodite_drycoating.md) · [`kim2025_conductive_agent_se_coating_cathode`](kim2025_conductive_agent_se_coating_cathode.md) · [`lee2026_lpscl_coating_thickness_ncm811`](lee2026_lpscl_coating_thickness_ncm811.md) · 압축 DEM [`so2022_dem_compaction_coated_particles_assb`](so2022_dem_compaction_coated_particles_assb.md).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

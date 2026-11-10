<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     2026-11-10 신규 작성 (논문 에이전트 · 사용자 읽기 목록 122 번 · cascade 트랙의 '문헌 갭 점검' 다섯 편 [목록 120–124] 중 하나).
     요청 축: reports/황화물 분해 부피 도펀트 문헌 갭.md 의 21 행 · 208 행 ('가' 묶음) — "reaction strain · 구속이 스크린에 들어갔나 · 도핑 조성이 있나".
              → §6 에 갭 질문 6 개의 답을 쪽 · 절 · 그림/표 번호와 함께 모았다.
     그림: 크롭 13 장 (본문 그림 5 + SI 그림 6 + 표 2). 그림 11 장을 전부 Read 로 실제로 봤다 (자동 크롭 그대로 · 손 크롭 0 · 번호 공백 0).
           표 2 장은 관례대로 PDF 텍스트로 옮겼다 (tab_*.png 를 이미지로 읽지 않았다).
     'figure-read ≈' 값은 PDF 에 박힌 원본 래스터 (본문 JPEG · SI PNG) 의 픽셀을 축 눈금선으로 보정해 읽은 것이다 — 논문이 표로 준 값이 아니다.
       검산 4 건: (가) Fig. 1B 막대 합 ≈ 66,700 / 11,700 ↔ 본문 67,062 / 11,935
                  (나) Fig. 4 막대 × Table 1 항목 수 = SI 카탈로그를 논문의 음이온 분류 규칙으로 다시 센 개수 (열 클래스 × 양쪽 20 칸 · 최대 편차 ≈ 3 항목 — 가장 큰 칸은 1,103 대 1,100)
                  (다) Fig. 2A 산화 구간 기울기 0.667 eV/V = Li 10 개 / 비-Li 원자 15 개 (완전 탈리튬)
                  (라) Fig. S1A 의 LSPS–LCO 최솟값 ≈ −0.39 ↔ ref [22] (Zhu 2016) 의 LGPS–LCO −0.34 / −0.35 eV/atom
     SI 카탈로그 (29 쪽 · 항목 약 4,000 개) 는 텍스트 층을 스크립트로 파싱해 집계했다 — '✎ 우리 집계' 로 표시한 수는 논문이 준 수가 아니다.
     우리 쪽 숫자는 옮기지 않았다 — 원장 경로로만 가리킨다 (cascade 는 마감 파일의 허용 문장만 그대로 인용). -->

# A High-Throughput Search for Functionally Stable Interfaces in Sulfide Solid-State Lithium Ion Conductors — Fitzhugh, Wu, Ye, Deng, Qi & Li (Adv. Energy Mater. 2019)

> slug `fitzhugh2019_ht_functionally_stable_interfaces_sulfide` · DOI `10.1002/aenm.201900807` · type `mixed — HT 열역학 스크리닝 (Materials Project 에너지 재사용 · 새 DFT 0) + 실험 (분말 혼합 XRD · 액체 셀 CV)` · PDF `a1014272-122._A_high_throughput_search_…pdf` (본문 12 pp · refs 36) + SI `892b3c21-122._Sup_…pdf` (36 pp = 표지 2 + 그림 5 쪽 [`Fig. S1`–`S6`] + 카탈로그 29 쪽) · 사용자 읽기 목록 122 번 (inbox 사본 `122. A high throughput search ….pdf` · `122. Sup) ….pdf`) · digested `2026-11-10` · status ✅ · 태그 **[외부·HT 코팅 스크리닝·cascade 갭 점검 '가' 묶음·⛔ LSPS 전용 — argyrodite 0]**
> elements: Li, Si, P, S, O, N, F, I, Se, Co, Sn, Ti, Mg, Zn
> methods: DFT, ESW

> **저자 (표지 그대로)**: **William Fitzhugh**†, **Fan Wu**† († 공동 1 저자 — *"W.F. and F.W. contributed equally"*), **Luhan Ye**, **Wenye Deng**, **Pengfei Qi**, **Xin Li**\* — John A. Paulson School of Engineering and Applied Sciences, Harvard University. 교신 `lixin@seas.harvard.edu`. (SI 표지의 저자 순서는 Fitzhugh · Wu · Deng · Qi · Ye · Li 로 본문과 다르다.)
> 투고 2019-03-11 · 개정 2019-03-30 · 온라인 2019-04-24. 자금: Dean's Competitive Fund for Promising Scholarship (Harvard) · 계산 자원 XSEDE + Odyssey 클러스터 · 상 에너지 자료 = Materials Project. 이해상충 없음 (신고).
> 🎤 **관련 발표**: 해당 없음 — `litdb/talks/lee2026_skku_mlip_materials_design.md` 의 인입 대기열을 확인했고 이 논문은 그 표에 없다.
> 계보: 방법은 `richards2016_interface_stability_pseudobinary` (이 논문 ref [21]) · `zhu2016_first_principles_interface_stability_assb` (ref [22] · 같은 날 목록 124 로 digest) · `zhu2015_esw_grand_potential_origin` (ref [36]) 의 pseudo-binary + grand potential 을 **67,062 물질로 넓힌 것**이다. 같은 그룹의 구속 (constriction) 계열 — ref [31] Wu 2018 *Nat. Commun.* (litdb digest 없음) → 이 편 (2019) → `fitzhugh2021_sei_design_constrained_ensemble` (목록 121) → `wang2022_two_parameter_space_dendrite_constriction` (목록 120) · `gilgonzalez2022_synergistic_cl_constricted_esw` — 에서 **이 편만 부피 항이 없다** (§6-1).

---

## 0. 이 digest 를 읽는 법

이 논문은 우리 문헌 갭 보고서가 "갭을 단정하기 전에 본문을 봐야 한다" 고 꼽은 편이다. 셋을 갈라서 읽는다.

1. **논문이 실제로 한 것** (§4–§5) — Materials Project 의 기존 DFT 에너지로 **Li₁₀SiP₂S₁₂ (LSPS) 한 조성**과 67,062 개 물질의 계면 반응 에너지를 0–5 V 에서 계산해, 코팅 후보 목록을 냈다.
   ⛔ **전해질은 LSPS 하나다. Li₆PS₅Cl · LGPS · Li₃PS₄ 는 본문에 한 번도 나오지 않는다. 전해질 조성을 바꾸거나 도핑한 계산은 없다. 새 DFT 계산도 없다.**
2. **논문이 계산하지 않고 전제로 둔 것** (§6 · §14) — LSPS 자신의 분해는 *"strain induced methods · kinetic metastability"* 로 눌려 있다고 가정하고 **빼 버린다**. 부피 변화는 *"neglected (ΔG ≈ ΔE)"* 라고 명시한다.
3. **우리에게 넘어오는 것** (§11–§12) — 값이 아니라 **정의** (계면 몫 ΔG′ · 재료 고유 몫 ΔG⁰ 의 분리) 와 **반례** (게이트 선택이 '좋은 코팅 화학' 의 결론을 뒤집는다) 다.

**본 그림 / 안 본 그림** — 크롭 13 장 가운데 그림 11 장 (`Fig. 1`–`5` · `Fig. S1`–`S6`) 을 전부 실제로 봤다. `Table 1` · `Table 2` 는 PDF 텍스트로 옮겼다. 안 본 그림은 없다. 본문 서술과 어긋나는 곳은 §14-9 에 모았다 (아홉 건).

---

## 1. 한 줄 요약

Materials Project 의 67,062 개 물질을 LSPS 와 짝지어 화학 (닫힌계) · 전기화학 (Li 열린계 · 0–5 V · 0.5 V 간격) pseudo-binary 를 전수 계산하고, **(i) 물질 자신의 전기화학 분해 에너지와 (ii) 계면이 더하는 반응 에너지가 각각 50 meV/atom 미만**이면 "기능적으로 안정 (functionally stable)" 이라 부른다 — LSPS 자신의 분해 에너지는 판정에서 뺀다. 결과는 음극 범위 (0–1.5 V) 1,000 개 이상 · 양극 범위 (2–4 V) 2,000 개 이상의 카탈로그다. 양극 쪽은 **황화물 · 셀레늄화물 · 아이오딘화물**이, 음극 쪽은 **아이오딘화물 · 인화물 · 질화물**이 통과율이 높고, 산소 · 불소 함유 물질은 평균적으로 LSPS 와 가장 크게 반응한다. 계면 몫은 0 V 에서 0 으로 사라지고 2–2.5 V 에서 최대다. 검증 실험은 분말 혼합물의 500 °C 열처리 XRD (LCO · SnO₂ · LTO 는 반응 · SiO₂ · MgF₂ · ZnS 는 무변화) 와 코팅 물질 단독의 액체 셀 CV 다. **스크린 기준은 에너지뿐이다 — 부피 · 변형률 · 기계 구속 · 띠틈 · 전자/이온 전도는 기준에 없다.**

---

## 2. 메타

| 저자 | 저널/년 | DOI | 계 | 연구유형 |
|---|---|---|---|---|
| W. Fitzhugh†, F. Wu†, L. Ye, W. Deng, P. Qi, X. Li\* (Harvard SEAS) | *Adv. Energy Mater.* **9**, 1900807 (2019) | 10.1002/aenm.201900807 | Li₁₀SiP₂S₁₂ (LSPS) × MP 67,062 물질 (코팅 후보) · 양극 예시 LiCoO₂ / Li₀.₅CoO₂ | HT 열역학 스크리닝 (MP 에너지 · pymatgen hull) + 분말 XRD + 액체 셀 CV |

- 랩 표준 표기: *Adv. Energy Mater.*, 9, 1900807 (2019).
- 출처 표지: **[외부]** (Harvard Xin Li 그룹 · 우리 그룹 아님).
- 논문 구성: §1 Introduction · §2.1 Data Acquisition and Computational Efficiency · §2.2 Functional Stability · §2.3 Anionic Species Impact on Material-Level Stability · §2.4 … on Interface-Level Stability · §2.5 … of Functional Stability · §2.6 Experimental Comparison · §2.7 Application to Particular Active Materials · §3 Conclusion · §4 Computational and Experimental Section.

---

## 3. 이 논문이 던지는 질문 (Introduction 의 구조 · pp. 1–2)

1. 세라믹 황화물 전해질은 전도도는 높지만 (본문: 최고 25 mS/cm) 전지 작동 조건에서 분해한다. 산화물 (가넷) 은 창이 넓지만 전도도가 낮다 (< 1 mS/cm).
2. 불안정은 두 층이다 — **재료 수준** (전압 창 밖에서 Li 저장소와 반응해 스스로 분해) 과 **계면 수준** (다른 물질과 맞닿아 반응). 계면 반응은 다시 2 체 화학 반응 (전압 무관) 과 Li 저장소까지 낀 3 체 전기화학 반응 (전압 의존) 으로 나뉜다.
3. LCO · LFPO 같은 양극은 대부분의 고체 전해질, 특히 황화물과 불안정한 계면을 만든다 (refs [21–23]). 그래서 **코팅**이 필요하고, 코팅은 스스로 전기화학적으로 안정하면서 황화물과도 안정해야 한다.
4. pseudo-binary 계산 (refs [21, 22, 24]) 이 이 문제를 풀지만 비싸서 대규모로 돌린 적이 없다 — convex hull 의 복잡도가 차원에 따라 O(n^⌊d/2⌋) 로 커진다 (LCO 는 3 차원 · LCO + LSPS 는 6 차원 Li–Co–O–Si–P–S).
5. 그래서 — 필요한 hull 수를 최소화하는 전처리 + pseudo-binary 를 푸는 이진 탐색으로 **67,000 개 이상을 전수 계산**하고, 원소 · 음이온 종류와 안정성의 통계를 본 뒤, 통과 목록을 SI 로 낸다.
6. 저자의 설계 선택 두 가지 (p. 2): ① **순차 필터를 쓰지 않는다** — 재료 수준에서 떨어진 물질도 계면까지 다 계산해 통계 자료로 쓴다 (물질마다 24 회 계산). ② **코팅–활물질 계면은 일반적으로 다루지 않는다** — *"we in general have not considered the equally important interface between the coating material and the active material"*. LSPS 와 안정한 목록을 먼저 주면 나머지는 그 목록 안에서 찾는 1 차원 문제가 된다는 논리다. LCO 만 예시로 표시한다.

---

## 4. 방법 — 무엇을 어떻게 계산했나

### 4.1 자료

| 항목 | 내용 | 위치 |
|---|---|---|
| 에너지 원천 | **Materials Project 의 기존 DFT 계산** (refs [30, 33]) 을 MAPI (ref [34]) 로 받아 pymatgen (ref [35]) 으로 hull 을 짠다 — 방법은 refs [22, 26, 36] 을 따른다. **이 논문이 새로 돌린 DFT 는 없다** | §4 Data Acquisition (p. 11) |
| 물질 수 | 69,640 구조를 재료 수준 전압 창 평가 → LSPS 와의 hull 이 8 차원 이하인 **67,062** 만 계면 평가 (9 차원 이상 2,578 개 제외) | p. 2 · p. 11 |
| 차원 제한의 뜻 | 원소가 {Li, Si, P, S} + **추가 원소 4 개 이하**인 물질만 | p. 2 |
| MP 에서 69,640 을 고른 기준 | 본문에 없다 (n/a) — E_hull 사전 필터 · 이론/실험 구조 구분 여부 미기재 | — |
| 전해질 | **Li₁₀SiP₂S₁₂ 한 항목** (mp-id 미기재) | 초록 · p. 2 |

### 4.2 물질마다 24 회

물질 A 하나에 대해 **{A 단독 · A–LSPS 계면} × {화학 1 회 + 전기화학 11 회 (0, 0.5, …, 5 V vs Li 금속)} = 24 회** (p. 2). 67,062 × 24 ≈ 161 만 회 평가다 (✎ 우리 산수). 흐름은 `Fig. 1A`: Phase Energies (DFT) → Dimensional Filtering (n ≤ 8) → Materials-Level Stability / LSPS Interface-Level Stability → Elemental Statistics (> 67,000) · Anionic Statistics (> 45,000) · Functional Stability List (> 3,000).

### 4.3 pseudo-binary 와 세 가지 에너지 (식 1–4 · p. 3)

개념도는 `Fig. 1C` 다.

```
(1)  (1 − x) LSPS + x A → Σ d_i D_i                     # x = 소모된 A 의 분율 (0–1) · D_i = 평형 분해 산물
     G_hull(x) = Σ d_i(x) G_i                           # 산물 조합의 에너지 (hull)
(2)  ΔG_RXN(x)  = G_hull(x) − (1 − x) G_LSPS − x G_A    # 총 반응 에너지 (≤ 0)
(3)  |ΔG_RXN(x_m)| ≡ max |ΔG_RXN(x)|                    # x_m = 구동력이 가장 큰 혼합비 ("most kinetically driven")
     ΔG⁰_RXN(x) : (1 − x) LSPS + x A → (1 − x) D_LSPS + x D_A   # 둘이 떨어진 채 각자 분해할 때의 에너지 (재료 고유 몫)
(4)  ΔG′_RXN(x) = ΔG_RXN(x) − ΔG⁰_RXN(x)               # 계면이 더한 몫
```

- 저자 풀이: *"ΔG⁰_RXN(x) represents the instability of the materials when separated and ΔG′_RXN(x) represents the increase in instability caused by the interface once the materials are brought into contact."*
- `Fig. 1C` (개념도 · 봄): 가로 x, 세로 G(T, p). 위쪽 빨간 점선 = (1−x)G_LSPS + xG_A (반응물 자신) · 가운데 파란 점선 = (1−x)G_D,LSPS + xG_D,A (각자 분해한 산물) · 아래 검은 곡선 = G_hull(x). 세 화살표가 max ΔG_RXN (빨강 · 전체) = ΔG⁰_RXN (초록 · 위 두 선 사이) + ΔG′_RXN (보라 · 파란 점선에서 hull 까지). 분홍 점선이 x_m (그림에서는 ≈ 0.56).
- ⚠ **표기 주의** — 그림 (`Fig. 3` 등) 은 같은 양을 `G_hull(x_m)` · `G′_hull(x_m)` · `G⁰_hull(x_m)` 이라는 **양수 'hull energy'** 로 부른다. 식 (1) 의 G_hull (산물 에너지) 과 이름이 같지만 다른 양이다. 이 digest 에서는 그림 값을 인용할 때 그림의 표기를 따른다.
- 계보 대응: ΔG′ = ref [22] (Zhu 2016) 의 **mutual** 반응 에너지 · ΔG = **total** · ΔG⁰ = 끝점 자신의 분해 몫 (`zhu2016_…` digest 의 식 8–10) = ref [21] (Richards 2016) 과 pymatgen 의 **no-mixing** 몫.

### 4.4 열린계 · 그리고 버린 항 (§4 · p. 11)

- 화학 hull: *"Chemical decomposition hulls were calculated using the energies and compositions from the MP. **Changes in the volume and entropy were neglected (ΔG ≈ ΔE).**"* (refs [18, 22, 26, 36])
- 전기화학 hull: Li grand potential — *"subtracting a term μ_Li N_Li from the energies (ΔΦ ≈ ΔE − μ_Li ΔN_Li)"*. 식 (5)–(8) 의 자유에너지를 Φ_i = G_i − μN_i 로 바꾸고 **조성 벡터에서 Li 를 뺀다** (Li 수가 변할 수 있게).
- 0 K · 결정상만 · PV 항 없음 · 엔트로피 없음 · 기체 처리 언급 없음.

### 4.5 계산 효율 — 전처리와 이진 탐색

- **원소 집합 순회** (`Fig. 1B`): 물질마다 hull 을 새로 짜지 않고, {물질의 원소} ∪ {Li, Si, P, S} 집합을 큰 것부터 훑어 **부분집합을 지운다**. 한 집합의 hull 하나로 그 원소들로 이뤄진 물질을 전부 평가한다. 필요한 hull 이 **67,062 → 11,935** 로 준다 (본문). 예: LSPS–Fe₂(SO₄)₃ 의 6 차원 hull {Li, Si, P, S, Fe, O} 는 LSPS–LFPO 에도 쓰이고 FeS 의 5 차원 hull 을 부분집합으로 품는다.
- **이진 탐색** (식 5–8 · `Fig. S1`): 조성을 원자 수 벡터로 쓰고 (LiCoO₂ → (1 1 2)), 식 (6) `(1−x)·LSPS + x·A = D·d` 에서 식 (7) `∂_x d = D⁻¹(A − LSPS)` 로 산물 분율의 x 미분을 얻어 식 (8) 로 hull 에너지의 기울기를 낸다. x 범위 (0, 1) · 첫 추정 0.5 에서 시작해 기울기 부호로 절반씩 좁힌다. **x_m 을 0.01 % 정밀도로 잡는 데 선형 격자는 10,000 회 · 이진 탐색은 14 회** (2⁻¹⁴ ≈ 0.006 %).
- 저자의 한 줄 경고: G_hull(x) 를 최소화하는 simplex 방식은 식 (3) 의 최대화와 많은 경우 같은 x_m 을 주지만 *"there is not enough evidence … that this is true in general in high-throughput evaluations"*.

### 4.6 '기능적 안정' 의 정의 (§2.2 · p. 5)

> *"Functional stability at a given voltage V was determined for each of the over 67 000 materials by requiring that both i) the material's intrinsic electrochemical instability (ΔG_RXN(x = 1, V)) and ii) the instability added by the interface (ΔG′_RXN(x_m, V)) were less than 50 meV atom⁻¹. Under these conditions, the only remaining instability in the system is that of the LSPS intrinsic material-level instability, which can be stabilized via strain induced methods,[31] kinetic metastability, etc."*

- 전압 범위: 음극 코팅 = **0–1.5 V** · 양극 코팅 = **2–4 V** (vs Li 금속 · *"cycling ranges commonly found in today's lithium ion batteries"* · p. 2). 음극 쪽은 특히 0 V 에 관심.
- **잠재적으로 기능적 안정 (potentially functionally stable)** (p. 6): 조건 (i) 을 어기지만 **리튬화/탈리튬화로 단일 산물로만** 분해하는 물질 — 그 과정이 가역이면 쓸 수 있다는 뜻. 양쪽 범위 각각 100 개 이상.
- 왜 LSPS 고유 몫을 빼나: 총 반응 에너지로 판정하면 *"will always return an unstable interface prediction above V > 2.1 as LSPS is intrinsically unstable at these voltages"* 이기 때문 (`Fig. 2A`).
- SI 카탈로그의 표기 (SI p. 7): *"All listed materials have [potentially] functional stability at 0V (anodes) or 4V (cathodes)"* · `*` = LSPS 의 전기화학적 안정화 기제 없이도 LSPS 와 **화학적으로** 안정 · `&` = Li₀.₅CoO₂ · LiCoO₂ 와도 화학적으로 안정 (양극 코팅만).

### 4.7 음이온 분류 (§2.3 · p. 6)

겹침을 없애려고 **단일 음이온** {N, P, O, S, Se, F, I 중 하나만} 또는 **옥시음이온** (O + {N, S, P} 중 하나) 인 물질만 남긴다 → 45,580 개 (`Table 1`). ⚠ **Cl · Br · Te · As 는 분류 집합에 없다** (왜 I 는 넣고 Cl · Br 은 뺐는지 설명 없음). 67,062 의 68 % 가 이 열 클래스에 든다 (✎ 우리 산수).

### 4.8 실험 방법 (§4 · p. 11)

| 항목 | 내용 |
|---|---|
| XRD 시료 | 후보 물질 (LCO · SnO₂ · SiO₂ · LTO — 방법 절 표기 · 그림에는 MgF₂ · ZnS 도 있다) 을 LSPS 분말과 **손으로 갈아 섞음** (무게비 55:30) · Ar 글러브박스 |
| 열처리 | 핫플레이트에서 명목 300 · 400 · 500 °C (본문 · 범례: 500 °C 는 6 h) |
| XRD | Rigaku Miniflex 600 · Cu Kα · 2θ 10–80° · Kapton 필름 밀봉 · 측정은 상온 |
| CV 전극 | 코팅 물질 : 카본블랙 : PTFE = 90 : 5 : 5 (무게) · 손으로 갈아 얇은 막으로 → 지름 5/16 인치 · ≈ 1–2 mg |
| CV 셀 | Swagelok · 대극 Li 금속 · 유리섬유 분리막 2 장 · **액체 전해질 1 M LiPF₆ in EC/DMC (1:1 v)** |
| CV 조건 | Solartron 1455A · 0.1 mV/s · 0–5 V · 상온 |
| LSPS 출처 · 입도 · 순도 | 본문에 없다 (n/a) |

---

## 5. 핵심 수치 총정리 ★

> 표기: **본문** = 논문이 문장 · 표로 준 값 · **figure-read ≈** = 원본 래스터 픽셀을 눈금선으로 보정해 읽은 값 · **✎** = 우리 산수 · 집계 · 추정. 전부 **소환값**이다 — 0 K MP hull 값이고 우리 `db/properties/` 절대값 옆에 놓지 않는다.

### 5.1 규모와 계산 효율 (`Fig. S1` 포함)

그림은 `Fig. 1A` · `Fig. 1B` · `Fig. S1` 이다.

| 양 | 값 | 출처 |
|---|---|---|
| 평가한 구조 | 69,640 → 계면 평가 67,062 (제외 2,578) | 본문 |
| 계산 횟수 | 물질당 24 회 | 본문 |
| 필요한 hull 수 | 67,062 → **11,935** | 본문 |
| 차원별 hull 수 (물질 순회) | 8D ≈ 9,970 · 7D ≈ 33,240 · 6D ≈ 20,710 · 5D ≈ 2,770 (합 ≈ 66,700 ↔ 67,062 ✓) | `Fig. 1B` figure-read |
| 차원별 hull 수 (원소 집합 순회) | 8D ≈ 5,270 · 7D ≈ 6,430 (합 ≈ 11,700 ↔ 11,935 ✓ · 6D 이하는 막대가 안 보인다) | `Fig. 1B` figure-read |
| x_m 탐색 | 0.01 % 정밀도에 선형 10,000 회 ↔ 이진 14 회 | 본문 |
| 오차 대 평가 횟수 | 선형: 오차 10⁻¹ → 10⁻⁵ 에 10 → 10⁵ 회 · 이진: ≈ 3 → ≈ 17 회 | `Fig. S1B` figure-read |
| 음이온 통계 대상 | 45,580 | `Table 1` (합 검산 ✓) |

### 5.2 LSPS 자신의 전압 창 — 이 논문에서 황화물 전해질에 대한 유일한 '구체 숫자'

`Fig. 2A` 는 LSPS 의 hull energy 를 전압에 대해 그린다. 축 표기는 "Hull Energy (eV)" 이고 원자당 표기가 없다 (가로축 제목은 "Votlage" 로 오타).

| V vs Li | 0 | 0.5 | 1.0 | 1.5 | 1.70–2.04 | 2.25 | 2.5 | 3.0 | 3.5 | 4.0 | 4.5 | 5.0 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| hull energy (figure-read ≈) | 1.97 | 1.23 | 0.62 | 0.15 | ≈ 0 | 0.04 | 0.19 | 0.52 | 0.86 | 1.19 | 1.52 | 1.85 |

- **안정 (Li 교환 0) 구간 = figure-read ≈ 1.70–2.04 V** (녹색 음영 경계 · 곡선의 꺾임과 일치). 본문은 *"unstable … above V > 2.1"* 이라고만 쓴다. 아래쪽 = 환원 (빨강) · 위쪽 = 산화 (파랑).
- 평탄 구간의 선은 0 눈금선보다 3 픽셀 아래에 그려져 있다 (≈ −0.015) → 위 값에는 ±0.02 의 판독 불확도를 둔다.
- ✎ **기울기에서 읽히는 것** (선형 구간 맞춤 · 논문은 중간 반응식을 싣지 않는다):
  - 2.35 V 이상: +0.667 eV/V. Li₁₀SiP₂S₁₂ 한 단위의 비-Li 원자는 15 개이고 Li 는 10 개 → 10/15 = 0.667. ⇒ **세로축은 Li 를 뺀 원자당 에너지이고, 2.3 V 위는 완전 탈리튬** (본문 p. 8 의 4 V 이상 산물 {Li, P₂S₅, SiS₂, S} 와 맞는다).
  - 2.04–2.30 V: +0.267 eV/V = Li 4 개. ref [36] 의 LGPS 가 2.14 V 에서 Ge 쪽 (→ GeS₂ + S) 이 먼저, 2.31 V 에서 Li₃PS₄ 쪽이 산화하는 것과 같은 2 단 구조다 (`zhu2015_…` digest) — LSPS 는 첫 단이 ≈ 0.1 V 낮다.
  - 1.70 V 아래: −0.935 eV/V (1.05–1.6 V · Li 14 개 흡수 = P⁵⁺ → P⁰ 10 e + Si⁴⁺ → Si⁰ 4 e) → −1.335 (0.5–0.75 V · Li 20 개 = Li₃P 까지) → −1.58 (0–0.2 V · Li–Si 합금). 꺾임은 ≈ 0.96 · ≈ 0.78 V.
  - 검산: 0 V 값 1.97 을 Li 포함 원자당으로 환산하면 ≈ 1.18 eV/atom — ref [36] 의 LGPS 0 V 분해 에너지 1.25 eV/atom (`zhu2015_…` digest) 과 같은 자릿수.
- 본문이 준 끝 산물: 0 V 에서 (Al₂O₃ 와의 계면 예) {Li₉Al₄, Li₂O, Li₃P, Li₂S, Li₂₁Si₅} · 4 V 이상에서 LSPS → {Li, P₂S₅, SiS₂, S} (p. 8).
- ⚠ 본문 서론의 *"LSPS, which has shown the highest lithium conductivity of around 25 mS cm⁻¹"* (refs [6, 20]) — 25 mS/cm 는 ref [6] (Kato 2016) 의 Cl 함유 조성 Li₉.₅₄Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃ 값이다 (litdb `jung2026_scalable_ai_dual_doped_lgps` · `kim2021_review_oxide_sulfide_se_interfaces` digest 로 교차 확인 · 이 PDF 밖). 계산에 쓴 것은 화학량론 Li₁₀SiP₂S₁₂ 다.

### 5.3 재료 수준 전기화학 안정 (`Table 1` · `Fig. S3` · `Fig. S4`)

본문 그림은 `Fig. 2B` · `Fig. 2C` · `Fig. 2D` 다.

**`Table 1` 전사 (PDF 텍스트)**

| 음이온 | F | I | N | O | O+N | O+P | O+S | P | S | Se |
|---|---|---|---|---|---|---|---|---|---|---|
| 항목 수 | 2,902 | 911 | 1,808 | 24,241 | 1,171 | 7,469 | 1,220 | 982 | 3,150 | 1,726 |
| 음극 범위 안정 [%] | 0.6 | 1.1 | 0.3 | 0.01 | 4.1 | 0.5 | 0.3 | 9.3 | 4.0 | 5.7 |
| 양극 범위 안정 [%] | 17.3 | 13.4 | 12.5 | 5.7 | 83.9 | 64.8 | 13.3 | 35.7 | 73.9 | 55.8 |

- `Fig. 2B` (음극: 가로 = 0 V 의 hull energy · 세로 = 1.5 V 의 hull energy) · `Fig. 2C` (양극: 2 V 대 4 V). 대각선 = "neutral decay" (두 전압에서 hull energy 가 같다 = Li 저장소와 반응하지 않고 분해). 대각선 위 = 그 범위에서 산화 · 아래 = 환원.
  - 음극 범위: 거의 전부 대각선 아래 (환원). **질소 화합물만 세로축 (0 V 에서 hull energy ≈ 0) 에 몰린다** — Li 금속과 닿아도 안정 (ref [32] 와 일치 · 본문).
  - 양극 범위: 옥시음이온 · 불소 화합물은 주로 환원 쪽 · 인 · 황 · 셀레늄 화합물은 산화 쪽 · 산화물은 양쪽에 걸친다 (본문). `Fig. S4B` 로 보면 황화물은 세 무리다 — 세로 띠 (2 V 에서 안정 · 4 V 에서 산화) · 대각선 · 가로축 위 (4 V 에서 안정).
- `Fig. 2D` — 음이온 클래스별 **평균** hull energy [eV/atom] 대 전압 (figure-read ≈ · 마커가 겹친 점은 뺐다):

| V | 큰 순서 |
|---|---|
| 0 | O+S 2.19 · O+P 2.12 · O 1.74 · F 1.68 · O+N 1.63 · S 1.53 · Se 1.48 · I 0.92 · P 0.86 · N 0.78 |
| 1 | F 1.07 · O+S 0.93 · O 0.82 · O+P 0.78 · O+N 0.74 · S 0.51 · Se 0.45 · N 0.38 · I 0.31 · P 0.13 |
| 2 | F 0.62 · O+P 0.41 · N 0.36 · O+N 0.33 · O 0.31 · O+S 0.27 · S 0.10 · I 0.06 |
| 4 | N 0.45 · O+N 0.23 · S 0.20 · F 0.13 · O 0.12 · O+S 0.10 · Se 0.07 · I 0.03 |
| 5 | N 0.50 · S 0.28 · O+N 0.23 · O+S 0.11 · I 0.04 |

  본문 서술과 맞는다: 0 V 에서 N 이 가장 안정 · P 는 0.5 V 위에서, I 는 1.0 V 위에서 N 을 앞지름 · 4 V 위에서는 F · I 가 안정하고 N 이 가장 불안정.
- 저자가 강조하는 것 (p. 6): 불소 화합물은 2 V 에서 **Li 저장소와는** 크게 반응하지만 (`Fig. 2D`) **LSPS 와의 계면 몫**은 2 V 에서 음의 상관이다 (`Fig. S2B`) — *"a fluoride coating material would likely reduce with the lithium reservoir but leave the LSPS intact"*. 재료 수준과 계면 수준을 따로 봐야 하는 이유로 든다.

### 5.4 계면 수준 — 화학 (`Fig. S1A` 포함)

그림은 `Fig. 3A` · `Fig. 1D` · `Fig. S1A` 다.

**`Fig. 3A` — 클래스 평균 화학 반응 에너지 [eV/atom] (figure-read ≈ · 누적 막대)**

| 클래스 | S | Se | I | P | N | O+S | O+P | F | O+N | O |
|---|---|---|---|---|---|---|---|---|---|---|
| G_hull(x_m) 전체 | 0.084 | 0.070 | 0.116 | 0.156 | 0.364 | 0.293 | 0.297 | 0.343 | 0.428 | 0.455 |
| G′_hull (계면 몫) | 0.027 | 0.040 | 0.091 | 0.121 | 0.237 | 0.247 | 0.261 | 0.317 | 0.325 | 0.405 |
| G⁰_hull (고유 몫) | 0.057 | 0.029 | 0.025 | 0.035 | 0.127 | 0.046 | 0.036 | 0.026 | 0.102 | 0.050 |
| 계면 몫 비율 ✎ | 32 % | 58 % | 79 % | 78 % | 65 % | 84 % | 88 % | 92 % | 76 % | 89 % |

- 본문: 황 · 셀레늄 화합물이 LSPS 와 가장 덜 반응하고 불소 · 산소 화합물이 가장 많이 반응한다. 전체가 클수록 계면 몫의 비율도 크다.
- **평균 산화물은 LSPS 와 ≈ 0.46 eV/atom 반응한다** (계면 몫만 ≈ 0.41) — 문턱 50 meV/atom 의 여덟 배다.
- `Fig. S1A` (LSPS–LCO 화학 pseudo-binary 실례 · 봄): ΔG_RXN 이 x = 0 에서 −0.012 (= LSPS 자신이 hull 위에 12 meV/atom 떠 있다) · **최솟값 ≈ −0.39 가 x ≈ 0.50–0.56** (이진 탐색 별표가 수렴하는 곳) · x = 1 에서 0. 세로축 단위는 인쇄돼 있지 않다 (eV/atom 으로 읽힌다 — ref [22] 의 LGPS–LCO 가 total −0.349 · mutual −0.340 eV/atom 이다 · `zhu2016_…` digest 의 닫힌계 표 전사).
- `Fig. 1D` — **원소 분율과 화학 계면 몫 G′_hull(x_m) 의 상관** (주기율표 색 지도 · 색 막대 −1 ~ +1 · 음 (빨강) = 그 원소가 많을수록 계면이 안정 · 50 구조 미만 원소는 회색). figure-read ≈ (칸 색을 색 막대와 대조):

| 원소 | S | Se | Te | I | Cl | Br | P | B | F | Si | Li | N | O | Al | Mg | Zr | Nd | La | Sc |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 화학 (`Fig. 1D`) | −0.63 | −0.58 | −0.55 | −0.52 | −0.32 | −0.31 | −0.26 | −0.26 | −0.13 | −0.11 | −0.05 | −0.03 | +0.03 | +0.03 | +0.10 | +0.37 | +0.31 | +0.31 | +0.48 |
| 0 V (`Fig. S2A`) | +0.04 | +0.08 | +0.03 | +0.01 | +0.01 | +0.01 | −0.01 | −0.05 | −0.01 | −0.03 | −0.04 | +0.05 | −0.03 | −0.04 | −0.05 | +0.01 | +0.02 | −0.06 | +0.03 |
| 2 V (`Fig. S2B`) | −0.48 | −0.50 | −0.29 | −0.33 | −0.31 | −0.21 | +0.08 | +0.09 | −0.58 | +0.35 | +0.23 | +0.05 | −0.03 | +0.46 | +0.52 | +0.60 | +0.60 | +0.59 | +0.62 |
| 4 V (`Fig. S2C`) | −0.46 | −0.40 | −0.37 | −0.43 | −0.35 | −0.28 | −0.16 | −0.21 | −0.21 | −0.04 | 0.00 | −0.14 | +0.09 | +0.11 | +0.03 | +0.15 | +0.03 | +0.14 | +0.08 |

  - 본문: 화학 안정은 큰 음이온 (S · Se · I) 을 가진 화합물에서 가장 좋다 · 0 V 와 4 V 에서는 상관이 약해진다 (저 · 고전압에서는 재료 고유 몫이 지배) · 2 V 에서는 대부분 원소가 양의 상관이고 칼코젠 · 할로젠만 음이다.
  - 그림에서 본 것: 0 V 지도는 거의 전부 |r| ≤ 0.10 이다 (예외는 Xe +0.23 · Np +0.20 · Pa +0.17 셋). **O 는 네 지도 모두 |r| < 0.1** 인데 산화물 클래스 평균은 가장 크다 (`Fig. 3A`) — 선형 상관이 화학을 요약하지 못하는 예다 (§14-14). 전기양성 금속 (희토류 · Zr · Sc · Mg · Al) 은 2 V 에서 강한 양의 상관이다.

### 5.5 계면 수준 — 전기화학

그림은 `Fig. 3B` · `Fig. 3C` 다.

**`Fig. 3C` — 클래스 평균 계면 몫 G′_hull(x_m, V) [eV/atom] (figure-read ≈)**

| V | 1.5 | 2.0 | 2.5 | 3.0 | 4.0 | 5.0 |
|---|---|---|---|---|---|---|
| O | 0.24 | 0.38 | **0.43** | 0.36 | 0.22 | 0.14 |
| O+N | 0.15 | 0.27 | **0.32** | 0.27 | 0.18 | 0.12 |
| N | 0.21 | **0.31** | 0.24 | 0.15 | 0.08 | 0.04 |
| P | 0.06 | **0.23** | 0.18 | 0.09 | 0.04 | 0.02 |
| O+S | 0.20 | 0.16 | 0.20 | 0.18 | 0.14 | 0.10 |
| O+P | 0.05 | 0.09 | 0.13 | 0.13 | 0.10 | 0.06 |
| I | 0.08 | **0.12** | 0.08 | 0.06 | 0.03 | 0.01 |
| F | 0.04 | 0.10 | 0.10 | 0.07 | 0.06 | 0.05 |
| Se | 0.02 | **0.06** | 0.05 | 0.02 | 0.01 | 0.00 |
| S | 0.03 | **0.04** | 0.03 | 0.01 | 0.00 | 0.00 |

- **모든 클래스가 0 V 에서 0** 으로 간다 (본문 · 그림 확인). 저자 설명: 0 V 에서는 양쪽 모두 Li 이원계로 완전 환원되므로 계면이 있으나 없으나 산물이 같다 — Al₂O₃–LSPS 가 0 V 에서 {Li₉Al₄, Li₂O, Li₃P, Li₂S, Li₂₁Si₅} 로 가는데 이는 각자 따로 분해한 산물 집합과 같다 → *"the existence of the interface has no energetic effect"*.
- 고전압에서는 계면 몫이 **'각자 완전 산화된 산물끼리의 화학 반응 에너지'** 로 수렴한다 — 예: 4 V 이상에서 LFPO → {Li, FePO₄} · LSPS → {Li, P₂S₅, SiS₂, S} 이고, 계면이 있으면 이 산물들이 반응해 **FeS₂ 와 SiO₂** 를 만든다 (p. 8).
- 결론 문장 (p. 9): 계면은 **1.5–3.5 V 에서 주로 화학적으로**, 그보다 낮은/높은 전압에서는 전기화학적 환원/산화로 분해한다.

**`Fig. 3B` — 클래스 평균 전체 G_hull(x_m, V)** : 모든 클래스가 LSPS 단독 곡선 (`Fig. 2A`) 을 따라간다 — 0 V 에서 ≈ 1.9–2.3 · 2 V 근처 최소 · 5 V 에서 ≈ 1.7–1.9 eV/atom. 2 V 값 (figure-read ≈): Se 0.09 · S 0.13 · I 0.19 · P 0.29 · O+S 0.38 · O+P 0.47 · O+N 0.54 · N 0.56 · O 0.61. 본문: 1 V 아래 · 4 V 위는 LSPS 의 재료 수준 환원 · 산화가 지배하고 1–3 V 에서만 클래스가 갈린다. (⚠ 4–5 V 에서 산소 함유 클래스 평균이 LSPS 단독값보다 **낮게** 읽힌다 — §14-9c.)

### 5.6 기능적 안정 결과 (`Fig. 4` · `Table 2` · SI 카탈로그)

- **본문**: 음극 범위 1,000 개 이상 · 양극 범위 2,000 개 이상 기능적 안정 · 양쪽 각각 100 개 이상이 '잠재적' · 합쳐 3,000 개 이상을 SI 에 수록.
- **✎ SI 카탈로그 집계** (텍스트 층 파싱):

| 목록 | 항목 수 | 고유 조성 문자열 | `*` (LSPS 와 화학적으로도 안정) | `&` (LCO · Li₀.₅CoO₂ 와 화학적으로 안정) |
|---|---|---|---|---|
| 음극 · 기능적 안정 (0 V) | 1,053 | 978 | 158 | — |
| 음극 · 잠재적 | 152 | 126 | 14 | — |
| 양극 · 기능적 안정 (4 V) | 2,668 | 1,994 | 2,663 | **449** (고유 조성 204) |
| 양극 · 잠재적 | 125 | 80 | 73 | 2 |

- **`Fig. 4` — 클래스별 통과율과 개수.** 막대 높이 × `Table 1` 항목 수가 카탈로그를 논문의 분류 규칙으로 다시 센 개수와 맞는다 (검산 ✓). 아래는 **카탈로그에서 센 개수** (기능적 + 잠재적) 와 그림의 통과율 (figure-read ≈):

| 클래스 | O+P | O+N | O+S | N | O | F | P | I | Se | S | 열 클래스 합 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 음극: 개수 | 0 | 0 | 12 | 42 + 2 | 35 + 2 | 9 + 1 | 20 + 10 | 41 + 2 | 8 | 17 + 5 | 184 + 22 |
| 음극: 통과율 [%] | 0 | 0 | 0.97 | 2.3 → 2.4 | 0.15 | 0.30 → 0.34 | 2.0 → 3.05 | 4.5 → 4.7 | 0.45 | 0.53 → 0.69 | — |
| 양극: 개수 | 11 | 2 | 13 | 20 + 2 | 310 + 1 | 60 + 2 | 23 + 5 | 108 + 3 | 467 + 6 | 1,103 + 60 | 2,117 + 79 |
| 양극: 통과율 [%] | 0.13 | ≈ 0 | 1.0 | 1.1 → 1.2 | 1.3 | 2.0 → 2.2 | 2.3 → 2.9 | 11.8 → 12.1 | 27.0 → 27.4 | 34.9 → 36.9 | — |

  - 본문과 일치: 음극은 N · P · I 가 2–4 % 이고 나머지는 1 % 미만 · 양극은 S 가 35 % · I 와 Se 가 10 % 이상.
  - ✎ **음극 목록 1,053 개 중 869 개 (83 %) 가 열 클래스 밖이다** — 금속 · 금속간화합물 · 규화물 · 붕화물 · 탄화물 · 염화물 · 브로민화물 등. 음이온 형성 원소 {N, O, S, Se, F, Cl, Br, I, Te, H, P} 가 하나도 없는 항목이 738 개 (70 %) · 비금속/준금속이 전혀 없는 순수 금속 · 금속간화합물이 376 개 (36 %) 다. `Fig. 4A` 의 통계는 자기 카탈로그의 17 % 만 설명한다.
  - ✎ 양극 목록: S 함유 1,346 · Se 함유 626 · O 함유 347 · I 149 · F 89 · Cl 57 · Br 47 · **Li 함유는 31 개 (1.2 %)**. 같은 조성의 다형이 따로 세어진다 — SiO₂ 165 항목 · ZnS 89 항목.
  - ✎ 양극 쪽 '(i) 를 통과한 것 중 (ii) 까지 통과한 비율' (카탈로그 개수 ÷ `Table 1` 양극 안정 개수 · `Table 1` 의 기준이 조건 (i) 과 같다는 가정): I 88 % · Se 48 % · S 47 % · O 22 % · F 12 % · N 9 % · O+S 8 % · P 7 % · **O+P 0.2 % (4,840 중 11) · O+N 0.2 % (982 중 2)**.
- **`Table 2` 전사** (양극 범위 대표 예): F — AlF₃ · CaF₂ · LiAlCaF₆ / I — AgI · PbI₂ · SnI₂ / O — LiAl₅O₈ · MgSiO₃ · SiO₂ / P — CoP · Ni₂P / S — CoNi₂S₄ · Si₂Cu₅S₇ · ZnS / Se — Cu₂GeS₃ (인쇄 그대로 · §14-9g) · MoSe₂ · ZrSe₂. 전부 카탈로그 양극 목록에서 확인했다.
- 저자 해석 (p. 8): 양극 목록에 Li 없는 물질이 많은 것은 *"the absence of lithium precludes delithiation/oxidation at high voltages"* 때문이다 — Li 가 없고 LSPS 와 화학적으로 안정하면 양극 코팅이 될 수 있다. 황 화합물이 고전압에서 산화 경향을 보이면서도 통과율이 높은 이유도 이것 (Li 든 황화물은 산화하고 Li 없는 황화물은 안 한다).

### 5.7 실험 (`Fig. 5` · `Fig. S5` · `Fig. S6`)

| 짝 | 예측 화학 반응 에너지 (본문) | XRD (상온 혼합 ↔ 500 °C · 6 h) | 반응 개시 온도 (`Fig. S6` 캡션) | 동정된 산물 (`Fig. 5` 캡션) |
|---|---|---|---|---|
| LCO + LSPS | 200 meV/atom | 2θ 10–80° **전 범위** 변화 (`Fig. 5A` 전체 음영) | 500 °C | SiO₂ · Li₃PO₄ · 입방 Co₄S₃ · 단사 Co₄S₃ |
| SnO₂ + LSPS | 97 meV/atom | 두 구간 변화 (음영 figure-read ≈ 10–30° · 38–50°) | 400 °C | SiO₂ · P₂S₅ · Li₂S |
| LTO + LSPS | 75 meV/atom | 한 구간만 (음영 figure-read ≈ 48.6–54.4° · 새 봉우리 ≈ 51°) | 500 °C | Li₁.₉₅Ti₂.₀₅S₄ |
| SiO₂ + LSPS | < 50 meV/atom | 변화 없음 | 500 °C 까지 반응 없음 | — |
| MgF₂ + LSPS | < 50 meV/atom | 변화 없음 | (`Fig. S6` 에 없음) | — |
| ZnS + LSPS | < 50 meV/atom | 변화 없음 | (`Fig. S6` 에 없음) | — |

- 저자 결론: 비호환 순서 LCO > SnO₂ > LTO > SiO₂ · MgF₂ · ZnS 가 예측 반응 에너지 순서와 맞는다. 상온에서는 어느 혼합물도 반응하지 않는다 — 반응이 열역학적으로 예측돼도 동역학 장벽을 넘을 에너지가 필요하다 (ref [8]).
- 그림에서 본 것: `Fig. S5` 의 단독 상은 500 °C 에서 변화가 없다. **SiO₂ 는 넓은 언덕뿐인 비정질**이다. `Fig. S6` 은 LCO · SnO₂ 는 300/400/500 °C 세 온도, LTO 는 400/500 °C, SiO₂ 는 500 °C 만 싣는다.
- 관측창 한 줄 (우리 규율 `D-2026-10-05-md-observation-window` 를 열처리에 빌려 씀 · `tools/sei/collect_neb.py --obs_window 773.15 21600`): *관측창 (ν₀ 1e+13 s⁻¹ 가정 · 정상성 가정 · 773 K · 2.16e+04 s): 기대 사건 1 ≈ 2.66 eV (검출 63 %) · 95 % 검출 ≈ 2.59 eV.* ⇒ SiO₂ · MgF₂ · ZnS 의 '무변화' 는 장벽으로는 꽤 높은 곳까지 본 셈이다. 실제 한계는 창이 아니라 **XRD 검출력** (결정성 산물 · 수 wt% 이상) 이다.

**CV (`Fig. 5G,H`)** — 코팅 물질 단독 · 액체 전해질 셀.
- Li₂S (`Fig. 5G` · figure-read ≈ · 가로축은 0–1.5 V 음영 폭으로 보정): 0–3.2 V 에서 전류 ≈ 0 → **≈ 3.3 V 부터 급상승** (봉우리의 5 % 를 넘는 점 ≈ 3.29 V · 절반 ≈ 3.51 V) · 어깨 ≈ 3.6–3.7 V · 봉우리 ≈ 3.9 V (≈ 0.30 A/g/cm²) · ≈ 4.2 V 에서 ≈ 0 으로 떨어진 뒤 5 V 까지 완만히 상승. 그림의 예측 음영: 0–1.5 V "Neutral" · 2–4 V "Oxidation". 본문: 0–1.5 V 는 평탄하고 2–4 V 를 큰 산화 봉우리가 지배한다.
- `Fig. 5H` (그림 라벨 · 캡션은 **SnO₂** · 본문과 방법 절은 **SiO₂** — §14-9e): 0–1.5 V 에서 환원 봉우리 ≈ 0.6 V · ≈ 0.1 V (둘 다 ≈ −0.55 A/g/cm²) 와 산화 봉우리 ≈ 0.55 V (≈ +0.27) · ≈ 1.2 V (≈ +0.12) · 2–4 V 에서 ≈ 0 (가로축은 2–4 V 음영 폭으로 보정). 예측 음영: 0–1.5 V "Reduction" · 2–4 V "Neutral".
- 저자: *"direct evidence to corroborate our theoretical predictions"*.

### 5.8 양극 활물질 적용 — LCO (§2.7 · p. 9)

- 방법: 양극 범위에서 LSPS 와 안정한 물질만 골라 **LiCoO₂ 와 Li₀.₅CoO₂ 양쪽에 대한 화학 안정**을 추가로 확인 → SI 에 `&` 표시.
- 본문이 든 예: SiO₂ · Al₂O₃ (잘 알려진 것) · AgI · CaF₂ · Li₃AlF₆ · LiAl₅O₈ · MgSiO₃ (본문 인쇄는 "MgSiO2") .
- ✎ 카탈로그 집계: `&` 는 양극 기능적 안정 2,668 항목 중 **449 항목 (고유 조성 204)** — O 함유 327 (그중 SiO₂ 다형 165) · F 58 · Br 29 · Cl 28 · I 5 · **S · Se · N 함유는 0**. 즉 양극 목록의 다수파인 황화물 · 셀레늄화물은 LCO 와는 하나도 통과하지 못한다.
- 저자 제안: NMC · LFPO · 인산염 · 옥시불화물 등 다른 양극에도 같은 절차를 반복하면 된다 (계산은 하지 않았다).

---

## 6. ★ 갭 질문에 대한 답 (문헌 갭 보고서 21 행 · 208 행)

### 6-1. 스크린 기준이 무엇인가 — reaction strain · 부피 · 기계 구속이 축으로 들어가나?

**아니오. 기준은 반응 에너지 두 개뿐이다.**

| 근거 | 위치 |
|---|---|
| 판정식: (i) ΔG_RXN(x = 1, V) < 50 meV/atom **그리고** (ii) ΔG′_RXN(x_m, V) < 50 meV/atom | §2.2 첫 문단 (p. 5) · 정의식은 식 (1)–(4) (p. 3) |
| *"Changes in the volume and entropy were neglected (ΔG ≈ ΔE)"* — **부피를 명시적으로 버린다** | §4 'Elemental Set Iterations' 셋째 문단 (p. 11) |
| 변형률은 **전제로 한 번** 나온다: LSPS 고유 불안정은 *"can be stabilized via strain induced methods,[31] kinetic metastability, etc."* · *"(stress, kinetic, etc.)"* | §2.2 (p. 5) — 본문 전체에서 'strain' 1 회 · 'stress' 1 회 |
| 흐름도에 부피 · 역학 단계가 없다 | `Fig. 1A` (p. 4) |

- K_eff · ε_RXN · 산물 몰부피 · V·ε·K 항 · 탄성 상수는 본문 · SI 어디에도 없다.
- 미묘한 점: 구속은 **LSPS 자신의 분해 항을 판정에서 빼는 명분**으로만 쓰인다. 같은 구속이 계면 반응 (ΔG′) 의 부피 변화에도 걸릴 텐데 그 항은 계산하지 않는다. 즉 이 논문은 '부피를 축으로 쓴 HT' 가 아니라 **'부피 효과가 이미 SE 를 안정화했다고 가정한 뒤의 에너지 HT'** 다.
- ⇒ 보고서의 "부피 (reaction strain) 를 스크린 축으로 쓴 고처리량 연구는 없다" 는 **이 논문으로는 깨지지 않는다.**

### 6-2. 물질 집합 — 몇 개 · 어디서 · 무엇이 스크린 대상인가?

- **67,062 개** (69,640 중 hull 차원 ≤ 8) · **Materials Project** (MAPI + pymatgen) — p. 2 오른쪽 단 · §4 Data Acquisition (p. 11) · `Fig. 1A,B`.
- 스크린 대상은 **코팅 후보 (LSPS 와 맞닿는 임의의 MP 물질)** 다. **전해질 조성은 스크린하지 않는다** — LSPS 한 조성 고정 · 도핑/치환 조성 0 · 다른 황화물 전해질 0.
- 순차 필터 없이 전부 계산했다 (p. 2).
- 음이온 통계는 그중 45,580 개 (§2.3 · `Table 1`).

### 6-3. '기능적으로 안정' 의 정의

- 정의 문장: p. 2 왼쪽 단 (*"both intrinsically stable at the material level and form stable interfaces with LSPS within the prescribed voltage range"*) · 판정식: §2.2 (p. 5) — §4.6 에 원문.
- 전압 범위: 음극 0–1.5 V · 양극 2–4 V (p. 2). 카탈로그의 판정 전압은 0 V · 4 V (SI p. 7 Notation).
- '잠재적' 등급: p. 6 왼쪽 단.
- 핵심: **LSPS 자신의 분해 에너지는 판정에서 빠진다.** 4 V 에서 LSPS 의 hull energy 는 figure-read ≈ 1.19 eV (`Fig. 2A`) 다 — '기능적 안정' 은 "코팅이 SE 를 지킨다" 가 아니라 "코팅이 문제를 **더하지 않는다**" 는 뜻이다.

### 6-4. 분해 산물의 물성 (전자 전도 · 띠틈 · 부동태) 을 기준으로 쓰나?

**아니오.** 본문에 band gap · electronic conductivity · passivation · insulating 이라는 말이 한 번도 나오지 않는다 (텍스트 검색). 이온 전도도도 기준이 아니다.
- 결과에서 보이는 증거: 음극 목록에 순수 금속 · 금속간화합물이 376 개 (✎) · 양극 목록에 Ag · Au · Hg · 탄소 · 비활성 기체 (He · Ne · Ar · Kr · Xe) 가 실려 있다 (SI pp. 7–35).
- 산물에 닿는 유일한 기준은 '잠재적' 등급의 **산물 개수** (단일 산물로만 리튬화/탈리튬화 · p. 6) — 물성이 아니다.
- 산물 이름은 예시 세 군데에만 나온다 (p. 8 의 0 V · 4 V 예 · `Fig. 5` 캡션의 XRD 동정).

### 6-5. 황화물 전해질에 대한 구체 숫자와 실험 검증

- **LSPS 만.** LGPS · Li₆PS₅Cl · Li₃PS₄ · Li₇P₃S₁₁ 은 본문에 없다 (텍스트 검색 0 건 — 서론이 계열 이름으로 *"Li-X-P-S (X = Si, Ge, etc.) sulfides"* 를 한 번 부르는 것이 전부다).
- 숫자: LSPS 안정 구간 figure-read ≈ 1.70–2.04 V (본문 "> 2.1 V 불안정") · hull energy 0 V ≈ 1.97 · 4 V ≈ 1.19 · 5 V ≈ 1.85 (`Fig. 2A` · p. 5) · 4 V 이상 산물 {Li, P₂S₅, SiS₂, S} (p. 8) · 화학 반응 에너지 LCO 200 · SnO₂ 97 · LTO 75 meV/atom · SiO₂ · MgF₂ · ZnS < 50 (§2.6 · p. 9) · LSPS–LCO 곡선 최솟값 figure-read ≈ −0.39 (`Fig. S1A` · SI p. 2).
- 실험: 분말 혼합 XRD 여섯 짝 (`Fig. 5A–F` · `Fig. S5` · `Fig. S6`) + CV 두 물질 (`Fig. 5G,H`) — §5.7.
- ⚠ 실험이 검증한 것은 ① **전압 없는** 화학 반응성의 순서 (500 °C 가속) 와 ② 코팅 물질 **단독**의 산화/환원 방향 (액체 셀) 이다. **'전압 아래 LSPS–코팅 계면의 기능적 안정' 자체와 전지 사이클은 실험하지 않았다.**

### 6-6. 보고서의 초록 수준 서술 중 본문과 어긋나는 것

| # | 보고서 문장 (행) | 본문 | 고칠 방향 (제안 — 보고서는 고치지 않았다) |
|---|---|---|---|
| 1 | *"Li₁₀SiP₂S₁₂ · LiCoO₂ 양쪽에 안정한 코팅의 HT 탐색이다 (양극 쪽 > 2,000 · 음극 쪽 > 1,000 후보)"* (21 행) | > 2,000 / > 1,000 은 **LSPS 하나에 대한** 수다. LCO 는 양극 목록에 나중에 덧붙인 예시 표시 (`&`) 이고 그 부분집합은 ✎ 449 항목 (고유 조성 204) 이다. 저자는 코팅–활물질 계면을 *"in general have not considered"* 라고 쓴다 (p. 2) | "LSPS 와의 계면에 대한 HT 탐색 (양극 범위 > 2,000 · 음극 범위 > 1,000 항목) — LCO 와도 안정한 것은 그 일부" |
| 2 | 근거 꼬리표 〔계산 · 초록〕 (21 행) | 분말 XRD · CV 실험이 있다 (§2.6) | 〔계산+실험 · 본문〕 |
| 3 | *"후자에 reaction strain 이 들어갔는지는 초록이 말하지 않는다"* (21 행) | 들어가지 않았다 — 부피를 명시적으로 무시 (p. 11) · 변형률은 전제로만 (p. 5) | "들어가지 않았다 (ΔG ≈ ΔE)" |
| 4 | *"reaction strain · 구속이 스크린에 들어갔나 · 도핑 조성이 있나"* (208 행) | 둘 다 아니오 (§6-1 · §6-2) | 208 행의 '결과가 바꾸는 것' 은 발동하지 않는다 |
| 5 | '후보' 라는 낱말 (21 행) | 수는 **MP 항목 수**다 — 다형이 따로 세어지고 (SiO₂ 165 · ZnS 89) 비활성 기체 · 금속이 섞여 있다. 고유 조성 문자열은 ✎ 양극 1,994 · 음극 978 | '항목' 으로 |
| 6 | 저자 표기 *"Fitzhugh, W.; Wu, F.; Ye, L.; …; Li, X."* (208 행) | 줄인 자리는 Deng, W.; Qi, P. (저자 6 명 · Fitzhugh 와 Wu 가 공동 1 저자) | 전체 목록으로 |

- 보고서 3 행 · 17–19 행의 큰 그림 (Xin Li 그룹이 2018 년부터 reaction strain 을 구속 열역학에 넣었다) 은 이 논문과 **충돌하지 않는다** — 다만 그 계열 안에서 **2019 년 HT 편은 부피를 쓰지 않았다**는 단서가 붙는다.
- ⚠ 갭의 최종 판정은 같은 묶음의 다른 편과 같이 본다 — 이 편은 그 판정을 대신하지 못한다. 같은 날 digest 된 `fitzhugh2021_sei_design_constrained_ensemble` (목록 121 · 비교표 §J-71) 은 2021 년 편이 ε_RXN 이 든 K_crit 를 유사상 계면 8 만여 점의 목표값으로 썼다고 판정했다. 즉 "부피를 스크린 축으로 쓴 HT 없음" 문장을 건드리는 것은 **2021 년 편이지 이 2019 년 편이 아니다.**
- 후속 `wang2022_two_parameter_space_dendrite_constriction` (목록 120 · §J-70) 은 구속 hull 의 계산 '절차' 를 이 편 (그 논문 ref 16) 에 맡긴다. **이 편에는 V(x) · ε(x) · 구속 항의 식이 없다** — 있는 것은 pseudo-binary 탐색 절차 (식 1–8) 뿐이다. reaction strain 과 기준 부피의 식을 찾으려면 이 논문 ref [31] (Wu 2018 *Nat. Commun.*) 쪽을 봐야 한다 (litdb 미보유 · 안 읽음).

---

## 7. 논증 흐름 종합

1. **LSPS 는 1.70–2.04 V 밖에서 스스로 분해한다** (`Fig. 2A`). 총 반응 에너지로 코팅을 고르면 2.1 V 위에서는 통과하는 물질이 없다.
2. 그래서 반응 에너지를 **재료 고유 몫 ΔG⁰ 과 계면 몫 ΔG′ 으로 가른다** (식 4 · `Fig. 1C`). LSPS 고유 몫은 다른 수단이 맡는다고 두고, 코팅에게는 '자기 고유 몫 + 계면 몫' 만 묻는다.
3. 계면 몫의 전압 의존은 종 모양이다 (`Fig. 3C`). **0 V** 에서는 모든 것이 Li 이원계로 환원돼 계면이 무의미하고, **고전압**에서는 각자 완전 산화된 산물끼리의 화학 반응으로 수렴하며, **1.5–3.5 V** 에서 가장 크다.
4. 음이온이 결과를 가른다. 큰 음이온 (S · Se · I) 은 LSPS 와 덜 반응하고 (`Fig. 3A` · `Fig. 1D`), O · F 는 많이 반응한다. 재료 수준에서는 N 이 0 V 에서, F · I 가 고전압에서 안정하다 (`Fig. 2D`).
5. 두 조건을 곱하면 — 음극 범위는 I · P · N (2–4 %), 양극 범위는 S (35 %) · Se (27 %) · I (12 %) (`Fig. 4`). 양극 쪽 통과 물질 대부분은 **Li 가 없어서 탈리튬 자체가 불가능한** 화합물이다.
6. 실험은 화학 반응 에너지의 순서를 500 °C XRD 로, 재료 수준 산화/환원 방향을 CV 로 확인한다 (`Fig. 5`).
7. 특정 양극 (LCO) 과의 양립은 카탈로그 안에서 한 번 더 걸러 표시한다 (`&`).

---

## 8. DFT/계산 방법 ★

- **code / version**: **새 DFT 계산 없음.** 에너지 전량이 Materials Project 의 기존 계산이다 (ref [30] Jain 2013 · ref [33] Jain 2011). hull · pseudo-binary 는 pymatgen (ref [35]) + 자체 코드 (원소 집합 순회 · 이진 탐색). 코드 공개 언급 없음.
- **functional (+vdW)**: 본문에 없다 (n/a). MP 표준 설정을 그대로 물려받는다 (✎ 추정: PBE GGA / GGA+U 혼합 + MP 보정 — 2019 년 초 시점이라 지금의 MP2020 보정이 아니다).
- **pseudo / PAW · k-points · ecut · supercell**: 본문에 없다 (n/a · MP 설정).
- **DFT+U**: 본문에 없다 (n/a · MP 설정).
- **AIMD / MLIP**: 없음.
- **무질서 처리**: 없음 — MP 의 정렬 항목 그대로. LSPS 도 MP 한 항목이다 (mp-id 미기재 · ✎ 추정: 부분 점유 구조의 정렬 근사 한 개 — `Fig. S1A` 로 보면 그 항목은 hull 위 ≈ 12 meV/atom 에 있다).
- **열역학 근사**: ΔG ≈ ΔE (부피 · 엔트로피 무시) · 0 K · Li 열린계는 ΔΦ ≈ ΔE − μ_Li ΔN_Li · 전압 격자 0–5 V 를 0.5 V 간격 (11 점) — LSPS 단독 곡선 (`Fig. 2A`) 만 연속으로 그렸다.
- **정규화**: 문턱은 'meV atom⁻¹' 로만 적혀 있다. 열린계 조성 벡터에서 Li 를 뺀다고 했고 (p. 11) `Fig. 2A` 의 기울기도 Li 제외 원자당과 맞는다 (§5.2) — 그러나 그림 · 식마다 어느 원자 수로 나눴는지 명시가 없다.
- **특이사항**: ① hull 차원 ≤ 8 제한 (추가 원소 ≤ 4) ② 문턱 50 meV/atom 의 근거 · 민감도 분석 없음 ③ x_m 을 **총** 반응 에너지의 최대점으로 정의하고 그 점에서 계면 몫을 읽는다 (식 3 · §14-13).

---

## 9. Post-processing ★

- **무엇**: ① 재료 수준 hull energy (화학 · 11 전압) ② LSPS 와의 pseudo-binary → x_m · ΔG · ΔG⁰ · ΔG′ ③ 원소 분율 ↔ ΔG′ 상관계수 (주기율표 색 지도 · 50 구조 미만 원소 제외) ④ 음이온 클래스별 평균 · 통과율 ⑤ 통과 목록 (SI 카탈로그) ⑥ LCO · Li₀.₅CoO₂ 와의 화학 안정 표시.
- **도구**: pymatgen (hull) · matplotlib (그림 양식으로 보아 — 본문에 명시는 없다). VESTA · LOBSTER 류 없음 (구조 · 전자구조 분석이 아예 없다).
- **수치화 · 기록 방식**: 클래스 평균은 그림으로만 (표 없음 — 그래서 §5 의 figure-read). 통과 목록은 **조성 (원자 분율 두 자리) + mp-id** 의 평문 목록 (SI pp. 7–35) — 반응 에너지 값 · 산물 · x_m 은 싣지 않는다. 기계 판독 파일 (CSV 등) 은 없다.
- **재현에 필요한데 없는 것**: MP 스냅숏 날짜 · 69,640 선정 기준 · LSPS 의 mp-id · 정규화 규약 · 물질별 에너지 값.

---

## 10. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1A,B | A: 흐름도 — DFT 상 에너지 → 차원 필터 (n ≤ 8) → 재료 수준 / LSPS 계면 수준 안정 (화학 + 0–5 V) → 원소 통계 (> 67,000) · 음이온 통계 (> 45,000) · 기능적 안정 목록 (> 3,000). B: hull 수를 물질 순회 (빨강 · 8D ≈ 9,970 / 7D ≈ 33,240 / 6D ≈ 20,710 / 5D ≈ 2,770) 대 원소 집합 순회 (파랑 · 8D ≈ 5,270 / 7D ≈ 6,430) 로 비교 (figure-read) | 흐름도에 부피 · 역학 · 전자구조 단계가 없다 — 갭 질문 1 · 4 의 그림 증거. 원소 집합으로 hull 을 재사용하는 전처리는 우리 cascade 의 MP 조회 묶음에 그대로 쓸 수 있다 |
| 1C | pseudo-binary 개념도 — 반응물 선 (빨강 점선) · 각자 분해한 산물 선 (파랑 점선) · hull (검정) · ΔG⁰ (초록) + ΔG′ (보라) = max ΔG (빨강) · x_m (분홍 점선 ≈ 0.56) | ΔG⁰ = no-mixing · ΔG′ = mixing (mutual) 몫이라는 대응표의 원 그림. 우리 `interface_reactivity_v2.py` 의 끝점 주의 (열린계 끝점 값 = 순수상 자체 분해) 를 설명할 때 쓸 수 있는 도식 |
| 1D | 원소 분율 ↔ 화학 계면 몫 G′_hull(x_m) 상관의 주기율표 지도 — S −0.63 · Se −0.58 · I −0.52 · Cl −0.32 · B −0.26 · O +0.03 · Nd +0.31 · Sc +0.48 (figure-read) | 도펀트 원소 순위로 읽지 않는다 — 코팅 상의 원소 분율과의 선형 상관이고 LSPS 한정. O 가 ≈ 0 인데 산화물 평균이 최대라는 점이 '상관 지도의 한계' 사례 |
| 2A | LSPS 의 hull energy 대 전압 — 안정 구간 ≈ 1.70–2.04 V · 0 V ≈ 1.97 · 4 V ≈ 1.19 · 5 V ≈ 1.85 (figure-read) · 환원 (빨강) / 중립 (초록) / 산화 (파랑) 음영 | 음영 = Li 교환 0 구간이라는 창 정의가 우리 정정 창 (`esw_window_edges()`) 과 같다. 기울기로 Li 수를 읽는 검산법 (0.667 eV/V = Li 10/15) 은 우리 사다리 그림에도 쓸 수 있다 |
| 2B,C | 클래스별 산점도 — B: 0 V 대 1.5 V · C: 2 V 대 4 V 의 hull energy · 대각선 = neutral decay | 한 물질의 '범위 안 거동' (산화 · 환원 · 중립) 을 두 끝 전압의 산점도로 요약하는 형식 — 우리 작동창 2.5–4.25 V 로 같은 그림을 그릴 수 있다 |
| 2D | 클래스 평균 재료 수준 hull energy 대 전압 — 0 V 에서 N 0.78 이 최저 · 4 V 에서 I 0.03 최저 · N 0.45 최고 (figure-read) | 평균은 MP 의 불안정 가상 구조까지 포함한 값이라 '그 화학의 안정성' 으로 인용하지 않는다 |
| 3A | 클래스 평균 화학 반응 에너지의 누적 막대 — O 0.455 (계면 몫 0.405) · F 0.343 · N 0.364 · S 0.084 (계면 몫 0.027) (figure-read) | 고유 몫 / 계면 몫을 한 막대에 쌓는 표시법 — 우리 축 ① · ③ 결과를 보일 때 호스트 고유 몫을 분리해 그리는 본보기 |
| 3B | 클래스 평균 전체 G_hull(x_m) 대 전압 — 모두 LSPS 단독 곡선을 따라간다 · 2 V 에서 Se 0.09 – O 0.61 (figure-read) | 총 반응 에너지는 SE 고유 분해가 지배해 계면을 못 가른다는 것의 그림 증거. ⚠ 4–5 V 에서 O 계열 평균이 LSPS 단독값보다 낮게 읽힌다 (§14-9c) |
| 3C | 클래스 평균 계면 몫 G′_hull(x_m) 대 전압 — 0 V 에서 전부 0 · O 는 2.5 V 에서 0.43 최대 · N 은 2 V 에서 0.31 · S 는 최대 0.04 (figure-read) | '계면 몫은 0 V 에서 사라진다' — 음극 쪽 목록이 사실상 Li 안정 목록이 되는 이유. 우리 축 ③ (Li 금속) 판독에 주의점으로 연결 |
| 4A,B | 클래스별 기능적 안정 통과율 (막대 · 빨강 = 기능적 · 파랑 = 잠재적) 과 개수 (초록 선) — 음극: I 4.5 → 4.7 % · P 2.0 → 3.05 % · N 2.3 → 2.4 % / 양극: S 34.9 → 36.9 % · Se 27 % · I 12 % · O 1.3 % (310 개) (figure-read · 카탈로그 재집계와 일치) | 통과율과 개수를 같이 싣는 양식. 음극 목록의 83 % 가 이 그림 밖 (열 클래스 아님) 이라는 점을 같이 적어야 한다 |
| 5A–F | 분말 혼합 XRD — 상온 대 500 °C · 6 h. LCO (전 범위 변화) > SnO₂ (두 구간) > LTO (한 구간) > SiO₂ · MgF₂ · ZnS (무변화) | 예측 반응 에너지 순서 ↔ XRD 변화 범위라는 정성 검증 설계. 한계: 전압 없음 · 비정질 산물 못 봄 · SiO₂ 자체가 비정질 |
| 5G,H | 액체 셀 CV — Li₂S: 0–3.2 V 평탄 · ≈ 3.3 V 부터 산화 · 봉우리 ≈ 3.9 V / SnO₂ (본문은 SiO₂): 0–1.5 V 산화환원 · 2–4 V 평탄 (figure-read) | Li₂S 의 실측 산화 개시가 열역학 값보다 1 V 이상 높다 — 우리 hull onset (층 ①) 을 실측 CV 와 견줄 때의 과전압 사례 (단 액체 전해질) |
| S1 | A: LSPS–LCO 화학 pseudo-binary 의 ΔG_RXN(x) — x = 0 에서 −0.012 · 최소 ≈ −0.39 (x ≈ 0.50–0.56) · 거친 격자 21 점 · 고운 격자 1,000 점 · 이진 탐색 별표. B: 필요한 평가 횟수 대 x_m 오차 (선형 대 이진) | 본문의 "LCO 200 meV/atom" 과 2 배 어긋난다 (§14-9a) — 인용할 때는 그림값과 본문값을 같이 적는다. 이진 탐색은 kink 전수 (`get_kinks`) 를 쓰는 우리 도구에는 필요 없다 |
| S2 | 원소 분율 ↔ 전기화학 계면 몫 상관 지도 (A 0 V · B 2 V · C 4 V) — 0 V 는 거의 무상관 · 2 V 는 F −0.58 · S −0.48 · 희토류 +0.6 · 4 V 는 S −0.46 · I −0.43 (figure-read) | 0 V 무상관 = 음극 쪽은 계면이 아니라 재료 고유 안정이 결정한다는 뜻 |
| S3 | 음극 범위 산점도 (0 V 대 1.5 V) 를 클래스 10 개로 분리 | N 패널의 세로축 띠 (0 V 안정 · 1.5 V 에서 산화) 가 `Table 1` 과 `Fig. 4A` 의 불일치를 설명할 단서 (§14-9b) |
| S4 | 양극 범위 산점도 (2 V 대 4 V) 를 클래스 10 개로 분리 — S · Se 는 세로 띠 + 대각선 + 가로축 세 무리 | Li 든 황화물 (세로 띠 · 산화) 과 Li 없는 황화물 (대각선 · 원점) 이 갈린다 — '양극 목록 = Li 없는 화합물' 의 그림 증거 |
| S5 | 단독 상 (LCO · LSPS · LTO · SnO₂ · SiO₂) 의 상온 대 500 °C XRD — 변화 없음 · SiO₂ 는 비정질 언덕 | 혼합물의 변화가 단독 상의 열분해가 아니라는 대조 |
| S6 | 혼합물의 온도별 XRD — LCO + LSPS (상온 · 300 · 400 · 500 °C) · SnO₂ + LSPS (같음) · LTO + LSPS (상온 · 400 · 500) · SiO₂ + LSPS (상온 · 500). 개시 온도 500 · 400 · 500 °C · SiO₂ 는 500 °C 까지 무반응 | 개시 온도 순서 (SnO₂ 400 < LCO 500) 가 예측 에너지 순서 (LCO 200 > SnO₂ 97) 와 **뒤집혀** 있다 — 열역학 구동력과 동역학 개시가 따로 간다는 사례 |
| Table 1 | 음이온 클래스 10 개의 항목 수 (합 45,580) 와 재료 수준 음극 · 양극 범위 안정 비율 | 음극 쪽 비율이 `Fig. 4A` 의 기능적 안정 비율보다 **작은** 클래스가 넷 (N · I · O · O+S) — 판정 기준이 다르거나 표가 틀렸다 (§14-9b) |
| Table 2 | 양극 범위 대표 물질 — AlF₃ · CaF₂ · LiAlCaF₆ · AgI · PbI₂ · SnI₂ · LiAl₅O₈ · MgSiO₃ · SiO₂ · CoP · Ni₂P · CoNi₂S₄ · Si₂Cu₅S₇ · ZnS · Cu₂GeS₃ · MoSe₂ · ZrSe₂ | 금속성 인화물 (CoP · Ni₂P) · 독성 (PbI₂) 이 '대표' 에 들어 있다 — 전자 절연 · 실용성 게이트가 없다는 증거 |

---

## 11. 우리 DFT/스크리닝 대비 → `our_dft_baseline.md` · `db/properties/` 원장

> 이 논문에는 argyrodite 값이 없다. 아래는 **방법과 정의의 대조**이고, 우리 쪽 값은 표에 싣지 않고 원장 경로로 가리킨다.

### 11.1 방법 · 정의 대조표

| 항목 | 이 논문 | 우리 (값은 원장 경로) | 같은가 / 왜 |
|---|---|---|---|
| 에너지 원천 | MP 기존 계산 (2019 년 초 · 보정 세대 미기재) | ESW · 계면 축: MP hull (GGA/GGA+U · MP2020 보정) / 물성: 자체 QE PBE | 같은 기계 (ref [36] 계보) · **보정 세대가 다르다** → 산화 쪽 절대 전압은 한 자로 못 잰다 (`HZ-esw-reduction-limit-label` 의 10-03 칸: 황 음이온 보정이 우리 산화 onset 을 옮긴다) |
| 안정 창 정의 | Li 교환 0 구간 (`Fig. 2A` 녹색 음영) | 교환 0 가장자리 (`tools/oxidation/constrained_esw.py:esw_window_edges()` · `litdb/our_dft_baseline.md` ESW 줄) | **같은 정의.** 물질이 다르다 (LSPS ↔ LPSCl) — 창 폭 · 산화 한 변을 나란히 놓지 않는다 |
| 환원 쪽 가장자리 | LSPS figure-read ≈ 1.70 V | 우리 LPSCl 의 교환 0 아래 가장자리 (`our_dft_baseline.md` · 값 자체는 `HZ-esw-reduction-limit-label` 금지 밖) | 둘 다 ≈ 1.7 V — thiophosphate 의 P⁵⁺ 환원이 공통 한계라는 뜻이지 물질이 같다는 뜻이 아니다 (ref [36] 의 LGPS · LPSCl 도 1.71) |
| 전압 격자 | 0–5 V · 0.5 V 간격 · 판정은 0 V / 4 V 한 점 | 연속 프로파일 (breakpoint) · 양극 쪽 판단 창 2.5–4.25 V (CLAUDE.md 2026-11-09) | 다르다 — 이 논문에는 4.25 V 가 없고 2.5–4 V 사이는 세 점뿐 |
| 계면 반응 에너지 | pseudo-binary · ΔG = ΔG⁰ + ΔG′ · **총 ΔG 가 최대인 x_m 에서 ΔG′ 를 읽는다** (식 3) | 닫힌계 `InterfacialReactivity(use_hull_energy=True)` 의 **최소 kink** (`tools/oxidation/interface_reactivity_v2.py:min_rxn_closed`) — 반응물을 hull 에너지로 재므로 고유 몫이 빠진 양 | **같은 부류** (우리 dE_rxt ≈ 이 논문의 화학 ΔG′). 차이는 x 를 어디서 읽나 — 우리는 ΔG′ 자체의 최소 (= ref [22] 의 규약) · 이 논문의 식은 총 ΔG 의 최대점 |
| 열린계 끝점 | 고유 몫 ΔG⁰ 을 정의 단계에서 분리 | `include_no_mixing_energy=True` 의 끝점 값은 '계면량이 아니다' 깃발 (`endpoint_meaning()` · 2026-09-16 '조용히 틀린 경로' 기록) | 같은 문제를 다른 방식으로 푼다 — 이 논문은 빼고, 우리는 깃발을 단다 |
| 판정 | 절대 문턱 50 meV/atom (근거 없음) | cascade 축 ① · ③: **호스트 대비 상대차 δ** + 도펀트 행방 · 산물 갭 등급 (`db/properties/cascade_axis_ncm_interface_estimand_2026_11_04.json` R1–R2) | 다르다 — 우리는 절대 문턱을 쓰지 않는다 (Xiao 2019 의 100 meV/atom 과도 다른 값이라 문헌 문턱끼리도 안 맞는다) |
| 대상 | 코팅 상 (MP 항목) × 고정 SE | 도핑 조성 (평형 상 혼합으로 입력) × 양극 대리 / Li 금속 / H₂O | 다르다 — **'도펀트별' 축은 이 논문에 없다** |
| 부피 · 역학 | 무시 (ΔG ≈ ΔE) · 구속은 전제 | 탄성 (E_VRH · B₀ — `canonical_registry.json`) 은 물성으로 있고, 분해 부피는 아직 보고량 카드 전 (후보 주제 B) | 우리 쪽도 아직 없다 — 그래서 갭이다 |
| 산물 물성 | 없음 | 축 카드 R2 (MP 갭 등급 · 외부값 · 순서용) — 통계는 `HZ-cascade-product-gaps-nonground-polymorph` (HOLD) | 이 논문은 후보 주제 A 의 자리도 채우지 않는다 |
| 실험 검증 | 500 °C 분말 XRD · 액체 셀 CV | 없음 (계산 트랙) | — |

### 11.2 트랙별 판정

| 트랙 (1저자) | 관계 | 한 줄 근거 |
|---|---|---|
| cascade · 후보 주제 B '분해 부피의 화학-기계 효과' (사용자) | 🟢 **갭 유지** (이 논문 기준) | 부피를 명시적으로 버렸고 (p. 11) 구속은 계산 없는 전제다 (p. 5). 도핑 조성 0 |
| cascade · 후보 주제 A '산물 물성 순위' (사용자) | 🟢 갭 유지 (이 논문 기준) | 산물 물성 기준 0 · 통과 목록에 금속 · 금속간화합물 다수 |
| cascade · 축 ① · ③ 의 정의 (사용자) | 🟢 지지 (정의 계보) | 고유 몫을 뺀 계면 몫으로 판정한다는 발상이 같다. 단 절대 문턱 · x_m 규약은 가져오지 않는다 |
| cascade · 마감된 첫 묶음 (`cascade_axes_bundle_closed_2026_11_05.json`) | ⚪ 무관 — **지지로 쓰지 않는다** | 마감 파일의 허용 문장: *"+U 전이금속 산물을 미판정으로 두는 규칙 하나를 MP 갭 등급으로 바꾼 사후 민감도에서는 V2O5 가 Li 금속 쪽 산물 (V12P7) 의 금속성 등급으로 빠지고 선택이 Sb2O5 · SiO2 가 된다 — 첫 선택은 그 규칙에 강건하지 않다."* 이 논문에서 SiO₂ 가 LSPS · LCO 양쪽 목록의 최다 항목이라는 사실을 그 선택의 근거로 옮기지 않는다 — 코팅 상 ↔ 도핑 전구체 설계 · LSPS ↔ LPSCl 이고, SiO₂ 는 LSPS 의 Si 가 만드는 종착 산물이라 LSPS 에서는 자명하다 |
| ESW (B① · 사용자) | ⚪ 무관 (다른 물질) · 정의는 일치 | LSPS 창 ≈ 1.70–2.04 V 는 우리 LPSCl 값의 대조가 아니다. 창 = Li 교환 0 구간이라는 정의만 같다 |
| 구속 창 (B② · `constrained_esw.py`) | ⚪ 계산 없음 | 이 논문은 B② 를 **이름만** 댄다 (ref [31]) |
| CEI · Nd 계면 (1저자 = 실험 쪽 다른 사람) | ⚪ 조회만 | §16 의 Nd 화합물 조회는 LSPS 기준 문헌 사실이다 — 우리 CEI 판정에 넣지 않는다 |
| B₂O₃ 원고 (1저자 아님) | ⚪ 조회만 | §16 의 B₂O₃ · 붕산염 조회도 같다 |

### 11.3 litdb 의 관련 digest 와 엮기

- **`xiao2019_cathode_coating_screening`** (같은 해 · *Joule*) 과 정면으로 갈린다. Xiao: Li 함유 104,082 → 전자 절연 (E_g > 0.5 eV) → E_hull < 5 meV/atom → 창 (V_ox ≥ 4.0 · V_red ≤ 2.7 V) → |ΔE_rxt| < 100 meV/atom (LPS · 만충 NCM 양쪽) → **폴리음이온 산화물** 이 남는다 (Li₃PO₄ 는 LPS · NCM 양쪽 0). 이 논문: Li 요구 없음 · 전자 절연 없음 · 문턱 50 meV/atom · SE 가 LSPS · 4 V 열린계 → **O+P (인산염류) 는 재료 수준 양극 안정 4,840 개 중 11 개만** 통과하고 황화물 · 셀레늄화물이 남는다. Li₃PO₄ · LiNbO₃ · LiTaO₃ · Li₂ZrO₃ 는 이 카탈로그에 없다 (§16). ⇒ **'어떤 화학이 좋은 코팅인가' 는 게이트와 SE 가 정한다.**
- **`zhu2016_first_principles_interface_stability_assb`** (ref [22]) — mutual / total 의 원 정의 (식 8–10) 와 LGPS–LCO −340 / −349 meV/atom. 이 논문 `Fig. S1A` 의 LSPS–LCO ≈ −0.39 와 같은 자릿수이고, 본문의 "200 meV/atom" 과는 안 맞는다.
- **`richards2016_interface_stability_pseudobinary`** (ref [21]) — 고정 μ_Li 의 no-mixing / mixing 분해. 이 논문은 그것을 0–5 V 격자 전체로 편다.
- **`gilgonzalez2022_synergistic_cl_constricted_esw`** — 같은 그룹이 뒤에 `∂G′ = (G_D − G_SE) + V·ε_RXN·K_eff` 로 부피 항을 넣는다. 이 편이 '전제' 로 둔 것이 거기서는 계산된다.
- **`fitzhugh2021_sei_design_constrained_ensemble`** (같은 1 저자 · 2 년 뒤) — 코팅 후보를 MP 전자 절연체 (> 20,000) 로 좁히고 목표값을 K_crit 로 바꾼 판이다. 이 편에 없던 두 가지 (전자 절연 사전 필터 · 부피 항) 가 거기서 들어간다. 두 편을 "Fitzhugh 의 HT 스크린" 으로 뭉쳐 부르지 않는다.
- **`wang2022_two_parameter_space_dendrite_constriction`** — 이 편을 ref 16 으로 인용하며 구속 hull 의 '절차' 출처로 든다. 이 편이 주는 것은 pseudo-binary 탐색 절차뿐이고 부피 · 변형률의 식은 없다 (§6-6).
- **`tian2020_electrochemo_mechanical_stress_assb`** — 분해 부피를 응력으로 환산한 연속체 편. 이 편과는 접점이 없다 (이 편은 부피를 버렸다).
- **`sundar2025_oxide_coating_screening_lpscl`** · **`honrao2021_interpretable_ml_sse_anode_coatings`** · **`aykol2016_ht_cathode_coating_design`** — 코팅 HT 계보. 이 편은 그 번호 붙은 계보 밖의 병렬 편 (Harvard) 이다.

---

## 12. 적용 인사이트 — 바꿔야 할 것 / 이미 하고 있는 것 / 해당 없음

**갭 판정에 쓰는 것**
- ① 보고서의 "부피를 스크린 축으로 쓴 HT 없음" 은 이 논문으로 깨지지 않는다. 연대기가 한 줄 생긴다 — *Xin Li 그룹의 2019 년 HT 는 부피를 버렸고 (ΔG ≈ ΔE), 2021 년 편에서 K_crit 로 들어간다* (그 문장을 실제로 고치는 것은 `fitzhugh2021_…` 쪽 판정이다 · §6-6).
- ② 이 논문의 '기능적 안정' 은 **SE 고유 분해가 구속 · 동역학으로 눌려 있다는 가정** 위에 서 있다. 후보 주제 B 는 바로 그 가정의 부피 항을 도펀트별로 재려는 것이므로, 이 논문은 B 의 **동기 문장**으로 인용할 수 있다 ("전제로만 쓰이고 계산되지 않았다").

**이미 하고 있는 것 (확인)**
- ③ 고유 몫을 뺀 계면 몫으로 판정한다 — 우리 닫힌계 최소 kink (`use_hull_energy=True`) 가 그 양이다.
- ④ 열린계 끝점 값을 계면량으로 읽지 않는다 — 이 논문이 ΔG′ 를 따로 정의한 이유와 우리 2026-09-16 깃발이 같은 문제다.
- ⑤ 절대 문턱 대신 호스트 대비 상대차를 쓴다 — 문헌 문턱이 50 (이 편) · 100 (Xiao) 으로 갈리는 것이 그 선택의 외부 근거다.
- ⑥ 게이트마다 '무엇을 떨어뜨렸나' 를 같이 적는다 (`cascade_screening_funnel_v2.json` 의 `gate_power`) — 이 편 ↔ Xiao 의 결론 반전이 그 관례가 필요한 이유의 실례다.

**가져올 만한 것 (제안 — 원장 · 카드는 고치지 않았다 · cascade 트랙 1저자 = 사용자)**
- ⑦ 결과 그림 양식: 고유 몫 / 계면 몫 누적 막대 (`Fig. 3A`) · 두 끝 전압 산점도 + neutral decay 대각선 (`Fig. 2B,C`) · 기울기로 Li 수 검산 (`Fig. 2A`).
- ⑧ 원소 집합 단위로 hull 을 한 번만 짜는 전처리 — MP 조회가 많은 축 계산의 비용을 줄인다.
- ⑨ 정성 실험 검증의 꼴: 예측 반응 에너지 순서 ↔ 분말 혼합 열처리 XRD 의 변화 범위. 단 개시 온도 순서는 예측과 뒤집힐 수 있다 (`Fig. S6`).

**옮기면 안 되는 것**
- ⑩ **LSPS 의 Si.** 이 논문이 든 산화물 반응의 산물에 SiO₂ 가 되풀이된다 (LCO + LSPS · SnO₂ + LSPS · LFPO + LSPS). 산화물 · 인산염이 LSPS 와 크게 반응한다는 결론의 일부는 Si–O 생성 구동력일 수 있다 (✎ 추정) — Si 없는 Li₆PS₅Cl 로 옮기지 않는다.
- ⑪ 음극 쪽 목록은 **계면이 아니라 Li 금속에 대한 안정성 목록**에 가깝다 (0 V 에서 ΔG′ → 0). 그리고 70 % 가 음이온 형성 원소가 없는 금속 · 금속간화합물 · 규화물 · 붕화물 · 탄화물이다 (✎ 집계 · 대부분 전자 전도체로 봐야 한다) — SEI '설계' 의 근거로 쓰지 않는다.
- ⑫ 클래스 평균 (`Fig. 2D` · `Fig. 3`) 은 MP 의 불안정 가상 구조까지 넣은 평균이다 — "산화물은 0.46 eV/atom 반응한다" 를 특정 산화물 코팅에 쓰지 않는다.
- ⑬ `Fig. 1D` · `Fig. S2` 의 원소 상관을 도펀트 순위로 쓰지 않는다.

---

## 13. 인용 가능 문장 (deck/paper 용 · 영문 초안)

- "A high-throughput pseudo-binary screening of 67,062 Materials Project entries against Li₁₀SiP₂S₁₂ used reaction energies as its only criteria and neglected volume and entropy changes (ΔG ≈ ΔE)." — *Adv. Energy Mater.*, 9, 1900807 (2019).
- "In that screening, a coating is termed functionally stable when its own electrochemical decomposition energy and the additional interfacial reaction energy are each below 50 meV per atom, while the intrinsic instability of the sulfide electrolyte is assumed to be suppressed by strain or kinetic effects."
- "The interfacial contribution to the decomposition energy vanishes at 0 V and is largest between 1.5 and 3.5 V vs Li/Li⁺."
- "Sulfur-, selenium-, and iodine-containing compounds dominate the cathode-range candidates, whereas oxygen- and fluorine-containing compounds are on average the most reactive toward Li₁₀SiP₂S₁₂."
- ⛔ **인용 금지**: "LSPS 와 LiCoO₂ 양쪽에 안정한 코팅 2,000 개 이상" (LCO 와도 안정한 것은 일부 · ✎ 449 항목) · '기능적 안정' 을 "안정한 계면" 으로 줄여 쓰기 (SE 자신의 분해는 판정 밖) · "LSPS 25 mS/cm" (다른 조성 값) · LCO–LSPS 반응 에너지를 한 값으로 (본문 200 ↔ 그림 ≈ 390 meV/atom) · 원소 상관 지도를 도펀트 순위로 · 이 digest 의 ✎ 집계 수를 논문 값으로.

---

## 14. 비판 — 주의 / 한계 (over-claim 방지)

1. **부피 · 엔트로피 · 온도가 없다.** ΔG ≈ ΔE · 0 K · 결정상만. 비정질 계면상 · 기체 · 동역학은 범위 밖이다. 실험이 500 °C 를 써야 반응이 보였다는 사실 자체가 상온 계면에서 열역학 예측이 그대로 실현되지 않음을 보인다.
2. **'기능적 안정' 은 SE 자신의 분해를 뺀다.** 4 V 에서 LSPS 는 figure-read ≈ 1.19 eV (비-Li 원자당) 불안정이다. 그 항을 누른다는 '구속 · 동역학' 은 계산하지 않았다. 이 이름을 "안정한 계면" 으로 줄여 옮기면 과장이다.
3. **문턱 50 meV/atom 의 근거가 없다.** 인용 문헌 · 민감도 분석이 없고, `Fig. 5` 캡션은 같은 판정을 "≤ k_BT/atom" 이라고 쓴다 (상온 k_BT 는 26 meV). 문턱을 조금 움직였을 때 목록이 얼마나 바뀌는지 알 수 없다.
4. **전자 전도 · 띠틈 · Li 전도 · 실용성 게이트가 0.** 목록에 금속 (음극 쪽 금속간화합물 376) · 비활성 기체 고체 (He · Ne · Ar · Kr · Xe · 양쪽 17 항목씩) · 방사성 원소 화합물 (Ac · Pa · Th · U · Tc 등 · 음극 67 · 양극 81 항목) · Hg · As 가 들어 있다. "코팅 후보 3,000 개" 는 **통과한 MP 항목 수**이지 쓸 수 있는 코팅 수가 아니다.
5. **음극 쪽 목록은 사실상 'Li 금속에 안정한 물질' 목록이다.** 0 V 에서 계면 몫이 0 이므로 조건 (ii) 가 거의 자동으로 통과한다. `*` (전압 없이도 LSPS 와 화학적으로 안정) 가 붙은 것은 1,053 중 158 뿐이다 — 나머지 895 는 전압 없이 맞닿으면 LSPS 와 반응한다는 것이 같은 계산의 예측이다.
6. **양극 쪽 목록은 Li 없는 화합물로 쏠린다** (Li 함유 31/2,668). Li 열린계에서 Li 든 물질은 고전압에서 탈리튬 경로가 늘 열려 있기 때문이다. LiCl · LiF · LiBr · Li₂O 같은 Li 이원계는 양극 목록에 없다 (§16). Li 없는 코팅의 Li 수송은 다루지 않는다.
7. **판정 전압은 범위가 아니라 한 점으로 읽힌다.** SI Notation 이 0 V / 4 V 라고 쓰고 카탈로그 개수가 `Fig. 4` ("in Anode/Cathode Range") 와 일치한다. 2 V 에서 환원되는 물질 (불소 화합물 다수) 이 4 V 한 점으로 통과했을 수 있다. 우리 상한 4.25 V 는 격자에 없다.
8. **코팅–활물질 계면은 LCO 화학 안정 표시뿐**이다 (전압 없음 · 449 항목). NMC · LFPO 는 말로만.
9. **논문 내부 불일치 아홉 건** (그림 · 표 · 본문을 대조해 찾은 것):
   - a. LCO–LSPS 화학 반응 에너지: 본문 · `Fig. 5` 캡션 **200 meV/atom** ↔ `Fig. S1A` 곡선 최솟값 figure-read ≈ **−0.39** (x = 0 의 −0.012 를 빼도 ≈ 0.38). ref [22] 의 LGPS–LCO (−0.34 / −0.35 eV/atom) 는 그림 쪽에 가깝다. 어느 쪽이 맞는지 논문 안에서는 판정할 수 없다.
   - b. `Table 1` 의 재료 수준 '음극 범위 안정' 비율이 `Fig. 4A` 의 기능적 안정 개수보다 작다 — N: 0.3 % (≈ 5 개) ↔ 42 개 · I: 1.1 % (≈ 10) ↔ 41 · O: 0.01 % (≈ 2) ↔ 35 · O+S: 0.3 % (≈ 4) ↔ 12. 기능적 안정은 조건 (i) 을 포함하므로 뒤집힐 수 없다. `Table 1` 이 범위 전체 (0–1.5 V) 를 요구하고 카탈로그는 0 V 한 점이라면 N 은 설명되지만 (`Fig. S3F` 의 세로 띠), 희토류 옥시황화물 12 개 (O+S) 는 설명되지 않는다. 양극 쪽은 열 클래스 모두 모순이 없다.
   - c. `Fig. 3B` 의 4–5 V 에서 산소 함유 클래스 평균 (5 V: O+S ≈ 1.69 · O+P ≈ 1.76 · O ≈ 1.80) 이 LSPS 단독값 (`Fig. 2A` · 5 V ≈ 1.85) 보다 낮다. S · Se 클래스는 LSPS 값과 겹친다 (1.91 · 1.86). 식 (3) 대로 x_m 이 총 반응 에너지의 최대점이면 G_hull(x_m) ≥ LSPS 단독값이어야 한다 (x = 0 이 후보이므로). ✎ 추정: 실제 계산은 ref [22] 의 규약 (x_m = **계면 몫**이 최대인 점) 을 따랐거나 정규화가 그림마다 다르다. 마커가 겹쳐 판독 불확도 ±0.05.
   - d. 식 (8) 의 좌변 표기와 부호 · 이진 탐색 규칙 (*"If the hull energy slope is negative, x_range → (x₀, 1)"*) 이 식 (2)–(3) 과 그대로는 맞지 않는다. 식 (2) 대로면 ∂ΔG_RXN/∂x = Σ G_Di ∂_x d_i − (G_A − G_LSPS) 다.
   - e. CV 둘째 물질: 본문 §2.6 · 방법 절 **SiO₂** ↔ `Fig. 5H` 라벨 · 캡션 **SnO₂**. 곡선 모양 (0–1.5 V 의 가역 봉우리 쌍) 은 SnO₂ 쪽으로 보인다.
   - f. `Fig. 5` 캡션 "SiO₂, **MnF₃**, and ZnS" ↔ 본문 · 패널 E **MgF₂** (MnF₃ 는 카탈로그에 없다).
   - g. `Table 2` 의 Se 열 첫 항목이 "Cu₂GeS₃" (황화물) 이다 — 카탈로그에는 Cu₂GeSe₃ (mp-4728 · mp-677105) 도 있어 오식으로 보인다.
   - h. SI 양극 목록의 제목이 "Functionally Stable **Anode** Coatings" 로 인쇄돼 있다 (SI p. 15 · p. 34 · 목차도 같음) — `&` 표시 · 4 V · 목차 쪽수로 양극 목록임을 확인했다.
   - i. "LSPS … 25 mS cm⁻¹" 은 Cl 함유 다른 조성의 값이다 (§5.2).
10. **실험이 검증한 것이 주장보다 좁다.** ① XRD 는 전압 없는 분말 혼합 · 500 °C — 화학 반응성 순서의 가속 시험이다. ② CV 는 코팅 물질 단독 · 액체 전해질 — LSPS 가 없다. ③ 전지 사이클 · 코팅된 입자 · 계면 임피던스는 없다. ④ SiO₂ 가 비정질이라 (`Fig. S5`) SiO₂ 쪽의 변화는 XRD 로 볼 수 없다. ⑤ LSPS 출처 · 입도 미기재. ⑥ 개시 온도 순서 (SnO₂ 400 °C < LCO 500 °C) 가 예측 에너지 순서와 뒤집혀 있는데 본문은 다루지 않는다. ⑦ Li₂S 의 산화 개시는 ≈ 3.3 V 로 열역학 값보다 1 V 이상 높다 — "2–4 V 를 산화가 지배" 라는 서술은 방향만 맞다.
11. **Cl · Br 이 음이온 분류에 없다.** argyrodite (Cl · Br) 에 직접 닿는 통계는 `Fig. 1D` · `Fig. S2` 의 상관값 (Cl −0.32 · Br −0.31) 뿐이다.
12. **LSPS 특이성** — §12-⑩. SiO₂ 가 양극 목록 최다 항목 (165) 인 것도 같은 이유로 자명하다.
13. **x_m 정의에 판정이 민감하다.** 식 (3) 대로 총 ΔG 의 최대점에서 ΔG′ 를 읽으면, SE 고유 분해가 큰 전압에서 x_m 이 SE 끝점으로 붙을 때 ΔG′(x_m) → 0 이 되어 조건 (ii) 가 자동 통과할 수 있다 (우리 도구가 2026-09-16 에 겪은 끝점 문제와 같은 구조). 논문은 이 경우를 논의하지 않는다 (9c 와 연결).
14. **상관 지도는 선형 상관이다.** O 는 네 지도 모두 ≈ 0 인데 산화물 평균 반응 에너지는 최대다. Xe 가 화학 지도에서 −0.60 으로 나온다. 인과나 설계 규칙으로 읽지 않는다.
15. **통계의 모집단이 MP 전체다.** 클래스 평균의 고유 몫 (N 0.127 · O+N 0.102 eV/atom) 이 큰 것은 hull 위에 높이 뜬 가상 구조가 평균에 들어가서다. 평균은 '그 화학의 전형' 이 아니다.

---

## 15. 기법 용어 미니사전

| 용어 | 뜻 (이 논문에서) |
|---|---|
| pseudo-binary (pseudo-phase) | 두 물질을 비율 x 로 섞은 조성선 위에서 평형 산물 조합 (hull) 을 찾는 계산. 구동력이 가장 큰 x 가 x_m |
| hull dimension | hull 을 짜는 원소 수. LSPS (4 원소) + 코팅의 추가 원소 — 이 논문은 8 이하만 |
| ΔG_RXN(x) · `G_hull(x_m)` | 반응물 자신의 에너지 기준 총 반응 에너지 (ref [22] 의 total). 그림에서는 양수 hull energy 로 표기 |
| ΔG⁰_RXN · `G⁰_hull` | 두 물질이 떨어진 채 각자 분해할 때의 에너지 = 재료 고유 불안정 (no-mixing 몫) |
| ΔG′_RXN · `G′_hull` | 계면이 더한 몫 = total − 고유 몫 (ref [22] 의 mutual · mixing 몫) |
| 전기화학 hull | Li 를 열린 종으로 두고 Φ = G − μ_Li N_Li 로 짠 hull. μ_Li 가 전압을 정한다 |
| neutral decay | 두 전압에서 hull energy 가 같은 분해 — Li 저장소와 교환 없이 분해한다는 뜻 (`Fig. 2B,C` 의 대각선) |
| functionally stable | (i) 코팅 자신의 전기화학 분해 < 50 meV/atom 그리고 (ii) 계면 몫 < 50 meV/atom. SE 고유 분해는 판정 밖 |
| potentially functionally stable | (i) 을 어기지만 리튬화/탈리튬화로 단일 산물만 내는 물질 |
| element-set iteration | 원소 집합마다 hull 을 한 번만 짜고 부분집합 물질을 모두 그 hull 로 평가하는 전처리 |
| `*` / `&` (SI) | `*` = 전압 없이도 LSPS 와 화학적으로 안정 · `&` = Li₀.₅CoO₂ · LiCoO₂ 와도 화학적으로 안정 |

---

## 16. SI 카탈로그 — 구성과 우리 관심 물질 조회

**구성** (SI 인쇄 쪽수): 음극 기능적 안정 pp. 7–13 · 음극 잠재적 p. 14 · 양극 기능적 안정 pp. 15–34 · 양극 잠재적 pp. 34–35. 항목 꼴은 `조성 (원자 분율 두 자리)[*][&]: mp-번호`. 반응 에너지 · 산물 · x_m 은 없다.

**조회 결과** (✎ 텍스트 층 파싱 · **LSPS 기준 · 0 K hull** — argyrodite 판정이 아니다. '없음' 은 어느 조건에서 떨어졌는지 논문이 알려 주지 않는다):

| 물질 | 음극 (0 V) | 양극 (4 V) | 비고 |
|---|---|---|---|
| LiCl · LiBr · LiF | 기능적 `*` | **없음** | Li 이원 할라이드는 양극 목록에 하나도 없다. NaCl · KCl · RbCl · CsCl 은 양극 `*&` |
| LiI | 기능적 `*` (+ 잠재적) | 잠재적 | — |
| Li₂S | 기능적 `*` (mp-1153) (+ 잠재적 다형 3) | 잠재적 (4) | CV 대상 |
| Li₂O | 기능적 (`*` 없음) | 없음 | — |
| Li₃N · Li₃P | 잠재적 | 잠재적 | — |
| Li₃PO₄ · LiPO₃ · Li₄P₂O₇ · P₂O₅ | 없음 | **없음** | Xiao 2019 에서는 Li₃PO₄ 가 LPS · NCM 양쪽 0 |
| LiNbO₃ · LiTaO₃ · Li₂ZrO₃ · Li₄Ti₅O₁₂ · LiAlO₂ · Li₂SiO₃ · Li₄SiO₄ · Li₂CO₃ | 없음 | **없음** | 관용 코팅이 하나도 없다 |
| SiO₂ | 없음 | 기능적 `*&` (다형 165) | XRD 무변화 |
| Al₂O₃ · HfO₂ · BeO | (BeO 만 기능적 `*`) | 기능적 `*&` (3 · 4 · 3) | 양극 목록의 이원 산화물은 이 셋 + SiO₂ + B₂O₃ + PaO₂ 뿐 |
| MgO · ZrO₂ · TiO₂ · ZnO · SnO₂ · Nb₂O₅ · Ta₂O₅ · WO₃ | 없음 | 없음 | SnO₂ 는 XRD 에서 반응 |
| **B₂O₃** (mp-306) | 없음 | 기능적 `*` (**`&` 없음**) | LSPS 와는 통과 · LCO 와는 표시 없음 |
| 붕산 리튬 | 없음 | LiB₃O₅ (mp-3660) · Li₃B₇O₁₂ (mp-16828) · Li₀.₀₉B₀.₃₄O₀.₅₆ (mp-1020014) 가 `*&` · **Li₃BO₃ · LiBO₂ 는 없음** | B 가 많은 쪽만 통과 |
| AlPO₄ | 없음 | 기능적 `*&` (3) | 인산염류 통과 11 개 중 하나 |
| MgF₂ · CaF₂ · AlF₃ · Li₃AlF₆ · LiYF₄ | (CaF₂ 기능적 `*`) | 기능적 (`*&` — AlF₃ 는 `*` 만) | — |
| ZnS | 없음 | 기능적 `*` (다형 89) | XRD 무변화 · `&` 없음 |
| Li₆PS₅Cl · Li₃PS₄ · Li₇P₃S₁₁ · Li₄P₂S₆ · P₂S₅ | 없음 | 없음 | 황화물 전해질 자신은 어느 목록에도 없다 |
| SiS₂ | 없음 | 기능적 `*` | LSPS 의 산화 산물 |
| Nd₂O₃ · NdOCl · NdPO₄ · NdCl₃ | 없음 | 없음 | — |
| Nd₂O₂S (mp-3211) | 기능적 (`*` 없음) | 없음 | 희토류 옥시황화물 12 종이 음극 목록 |
| NdPS₄ (mp-3694) · Nd₂S₃ (mp-438 · mp-32586) | (NdS · NdP · NdN 은 음극 기능적) | 기능적 `*` | Nd 함유 양극 49 항목 중 48 이 황화물 · 셀레늄화물 (옥시황화물 Nd₁₀S₁₄O 1 포함) · 나머지 1 은 염화물 Cs₃NdCl₆ (`*&`) |
| AlN | 기능적 `*` | 기능적 `*` | 양쪽 목록에 다 있는 드문 예 |
| LiCoO₂ | 없음 | 없음 | — |

---

## 🗨️ Q&A 로그

(아직 없음)

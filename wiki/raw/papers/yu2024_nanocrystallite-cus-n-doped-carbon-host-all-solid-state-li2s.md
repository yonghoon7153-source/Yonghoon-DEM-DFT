---
title: "Yu et al. 2024 — A Nanocrystallite CuS/Nitrogen-Doped Carbon Host Improves Redox Kinetics in All-Solid-State Li2S Batteries (Adv. Energy Mater. 14, 2400845)"
description: "N-도핑 다공성 탄소에 CuS 나노결정(29 wt%)을 박은 호스트에 nano-Li2S 를 담아 Li5.5PS4.5Cl1.5 · Li–In 전고체셀을 돌린 논문 — 첫 충전 Li2S 이용률 51 %(CuS 없는 대조) → 91 %, 10 mg cm⁻² 에서 9.6 mAh cm⁻². 전자 전도도를 200배 낮추고도 개선됐다는 것이 이 논문의 축이다. Methods 가 전부 SI 에 있고 이번 수집은 SI 미확보"
source_url: local-upload/57b2dc3d-CuS_N_doped_C_host.pdf
doi: 10.1002/aenm.202400845
ingested: 2026-09-30
sha256: 798622b1657dd1c7a45a2359b5174b10292a1041b1dbb00688fe93777fb5b2cd
tags: [li2s, assb, sulfide-electrolyte, composite-cathode, activation, carbon, li-in]
compare:
  system: "ASSB (all-solid-state Li2S), 상온 + 60 °C"
  electrolyte: "Li5.5PS4.5Cl1.5 argyrodite (자기 그룹 재료, 'almost 10 mS cm⁻¹ at RT' 라고만 인용) — 두께·질량 미기재"
  cathode: "nano-Li2S + CuS-NC 호스트(CuS 29 wt% in host) + SE. 조성비·바인더·도전재 미기재(Methods 가 SI 에만 있고 SI 미확보). [재현] 이론용량 역산으로 Li2S : CuS-NC ≈ 50:50 ~ 33:67"
  li2s_source: "'nano-Li2S' — 공급사·입도·합성법 미기재"
  mixing: "'mixing nano-Li2S with CuS-NC' + 'pressed into a pellet' 이 전부 — 장비·rpm·시간·BPR·분위기·성형 압력 전부 미기재. 호스트는 NaCl 주형 + 동결건조(−50 °C) + N2/H2 800 °C 탄화 + 수세 + 황화 [도표, Fig. 1a]"
  loading_mg_cm2: "2 / 4 / 10 (Li2S 기준)"
  anode: "Li–In 합금 (조성·두께 미기재). anode-free 실험은 없다"
  first_charge: "0.1 mA cm⁻², 컷오프 ≈2.5 V vs Li–In [도표]. CuSNC 2.1 mAh cm⁻² = Li2S 이용률 91 %; 대조 NC 1.2 mAh cm⁻² = 51 % [재현]"
  first_discharge_mAh_gS: "1648 [재현] (2.3 mAh cm⁻² ÷ 2 mg cm⁻², 0.1 mA cm⁻²) — 이 중 ≈10 % 는 CuS→Cu₂₋ₓS 환원 몫이라 Li2S 단독은 ≈1483"
  first_discharge_mAh_gLi2S: "1150 [재현] (CuS 몫 제외 시 ≈1035). 대조 NC/Li2S 는 650"
  cycle_capacity_mAh_gS: "1075 @ 0.3 mA cm⁻² 100th (2 mg) · 609 @ 1 mA cm⁻² 500th (2 mg) · 888 @ 0.3 mA cm⁻² 30th (10 mg) [전부 재현]"
  cycle_capacity_mAh_gLi2S: "750 @ 0.3 mA cm⁻² 100th (2 mg) · 425 @ 1 mA cm⁻² 500th · 620 @ 30th (10 mg) [전부 재현]"
  areal_mAh_cm2: "1.6 → 1.5 (2 mg, 0.3 mA cm⁻², 100 cyc, 최대 1.8) · 1.1 → ≈0.85 (2 mg, 1 mA cm⁻², 500 cyc, 최대 1.3) · 6.7 → ≈6.2 (10 mg, 30 cyc, 최대 9.0) · 첫 방전 최대 9.6 (10 mg)"
  cycles: "100 (93.8 %, CE 99.5 %) · 500 (77 %, 0.05 %/cyc — 단 최대 대비 65 %) · 80 (4 mg, 본문 '안정' 이나 최대 대비 58 %) · 30 (10 mg, 92 % — 최대 대비 69 %) · 130 (60 °C, 85 % — 최대 대비 76 %)"
  temperature_C: "room temperature (수치 미기재) · 60"
  mechanism: "CuS 의 Li2S 흡착(DFT −3.2 vs −2.1 eV) + Li2S→LiS 장벽 0.4 vs 0.9 eV + Li⁺ 이동 장벽 0.3 vs 1.5 eV = '전기촉매' 주장. 실측은 CV 활성화 피크 2.14 vs 2.41 V vs Li–In, Tafel 84 vs 151 mV dec⁻¹(산화) / 278 vs 356(환원), DC 분극 σ_Li 6.4 vs 3.5 ×10⁻⁵ S cm⁻¹, σ_e 2.9×10⁻⁴ vs 5.7×10⁻² S cm⁻¹(200배 낮음). ex situ XRD/XPS/XANES 로 CuS↔Cu₂₋ₓS 가역(Cu 금속 아님), 용량의 ≈10 % 기여"
  our_axis: "우리와 셀 계가 가장 가깝다(Cl-rich argyrodite + Li–In + 상온 + 펠릿). 첫 충전 이용률 51→91 % 는 H1 의 고체계 직접 근거이고, σ_e 를 200배 낮추고도 개선됐다는 것은 Huang 2026(σ_e 14배 상승)과 합쳐 'σ_e 가 클수록 좋다'를 기각한다. 단 pristine Li2S 대조군이 없고(개선폭을 우리 기준선과 못 잇는다), 혼합·압력 조건이 전무하며, 첫 CE 110–113 %(CuS 가 음극 Li 을 먹는다)는 anode-free 에 그대로 손실이다. 60 °C 데이터는 이론 초과라 쓰면 안 된다"
---

# 수집 목적

Y. Yu, B. Singh, Z. Yu, C. Y. Kwok, I. Kochetkov, L. F. Nazar,
**"A Nanocrystallite CuS/Nitrogen-Doped Carbon Host Improves Redox Kinetics in
All-Solid-State Li2S Batteries"**, *Advanced Energy Materials* **14** (2024) 2400845,
DOI 10.1002/aenm.202400845 (Waterloo, Nazar 그룹) 의 **절별 해체분석**.

이 위키가 이 논문을 읽는 이유는 셋이다.

1. **Li2S 를 출발 물질로 쓰는 황화물 전고체 셀**이다 — 우리
   [[li2s-assb-reference-cell]](pristine Li2S : LPSCl : AB = 30 : 50 : 20, Li–In, 목표
   500–600 mAh g⁻¹)과 **셀 계가 거의 같다** (argyrodite + Li–In + 상온 + 펠릿).
   우리 위키에 들어온 Li2S 계 고체셀 digest 중 조건이 가장 가깝다.
2. **"복합양극에 소량의 기능성 상을 넣어 kinetics 를 고친다"** 는 설계가
   `raw/papers/huang2026_high-entropy-sulfides-kinetic-accelerators-assb.md` 와 같은 축이다.
   다만 Huang 2026 은 **첨가제**(S/KB/LPSCl 에 6 wt% HES 추가)이고 이쪽은 **호스트**
   (Li2S 를 담는 탄소 골격 자체를 바꿈)다. 같은 문제를 다른 층위에서 푼 두 논문을
   나란히 놓는 것이 이 digest 의 두 번째 목적이다 (§13).
3. **첫 충전 활성화를 정면으로 다룬다.** Li2S 계에서 첫 충전은 곧 Li 재고이고
   ([[anode-free-li2s-assb]]), 이 논문은 CV·Tafel·갈바노스태틱·DFT-NEB 를 같은 축(활성화)에
   맞춰 놓았다. [[li2s-activation-first-charge]] 에 고체계 근거를 준다.

**표기 규칙** (이 위키 관례 4구분):
- `[인쇄]` — 논문 본문/캡션에 글자로 있는 것
- `[도표]` — 그림에서 눈으로 읽은 근사값 (**원 데이터가 아니다**)
- `[해석]` — 이 문서를 쓰면서 붙인 판단. **논문의 주장이 아니다**
- `[재현]` — 원문 값의 산술 환산 (계산식을 함께 적는다)

**단위 선언**: 이 논문은 **비용량(mAh g⁻¹)을 거의 쓰지 않는다.** 전기화학 그림의 세로축은
전부 `Areal capacity (mAh cm⁻²)` 이고, 질량은 항상 "**Li2S mass loading** x mg cm⁻²" 로만
주어진다 (`[인쇄]` Fig. 6a,d,e,f 캡션). 따라서 이 digest 의 mAh g⁻¹ 값은 전부
`[재현]` 이며 **분모는 Li2S 질량**이다. 황 기준 환산은 ×1.4329 (= 45.948/32.065),
역방향은 ×0.698 ([[capacity-normalization-li2s-vs-sulfur]]).

**★ SI 미확보**: 이 논문은 **Experimental/Methods 절이 본문에 없다.** 본문은
"see Methods for details" · "see the methods in Supporting Information for details" 로
**전부 SI 로 보낸다** (`[인쇄]` p.2 두 곳, p.5 XRD 세척 절차). 이번 수집에서는 **본문 PDF
10쪽만 확보**했고 SI 는 받지 못했다. 그래서 **양극 조성비·혼합 조건·성형 압력·스택 압력·
셀 면적·전압창·Li2S 입도·SE 두께가 이 digest 에 하나도 없다.** 아래 공백표의 G1 이
그것이며, 본문이 인용하는 Figure S1–S23 · Table S1 은 §12 에 목록만 남긴다.
**추측으로 채우지 않았다.**

- 원본 파일: 로컬 업로드 PDF 10쪽 (저널 조판 "n of 10"). 저장소에 바이너리 원문은 넣지 않는다.
- 크로핑 그림: `raw/figures/yu2024_nanocrystallite-cus-n-doped-carbon-host-all-solid-state-li2s/`
  — 본문 Fig. 1–7 전부 (`fig_1.png` … `fig_7.png`, `figures.json` 에 캡션 등록).
  **SI 그림은 없다** (SI 미확보).

---

# 원문에 없어서 확인이 필요한 것 (읽기 전에 먼저 본다)

이 절이 이 digest 의 가장 중요한 산출물이다. G1–G3 은 SI 만 구하면 풀리는 것이고,
G4 이하는 **SI 가 있어도 논문이 답하지 않는 것**이다.

| # | 공백 | 왜 문제인가 |
|---|---|---|
| G1 | **★ 방법이 본문에 하나도 없다 — 그리고 SI 를 확보하지 못했다.** 본문에 남은 방법 문장은 네 개뿐이다: "CuS-NC was fabricated from Cu(NO3)2·3H2O, NaCl, and dopamine hydrochloride precursors using a templating method, followed by heat treatment and sulfidation" · "electrode materials were prepared by **mixing** nano-Li2S with CuS-NC or NC" · "The materials were **pressed into a pellet**" · "using Li5.5PS4.5Cl1.5 as the electrolyte". | **혼합 장비·rpm·시간·BPR·볼 재질·분위기·건식/습식이 전부 없다** — 우리 [[one-step-vs-two-step-mixing]] 과 [[composite-cathode-mixing-routes]] 가 필요로 하는 바로 그 변수다. Kim 2023 G1 과 같은 공백이 **한 단계 더 심한 형태**로 반복된다 (그쪽은 "ball milling" 이라는 단어라도 있었다). 재현 불가. |
| G2 | **양극 조성비(Li2S : CuS-NC : SE : 바인더)가 본문 어디에도 없다.** 주어지는 것은 "Li2S mass loading 2 / 4 / 10 mg cm⁻²" 뿐이다. | `[재현]` 그래도 **간접 추정은 가능하다** — 논문이 "theoretical discharge capacity is 2.66 mAh cm⁻² based on the complete reduction of CuS and Li2S" (2 mg cm⁻² Li2S) 라고 적었고 Li2S 단독 이론이 2.33 이므로 CuS 몫 = **0.33 mAh cm⁻²**. CuS 2 e⁻(→Cu) 기준 560.6 mAh g⁻¹ 이면 CuS = **0.59 mg cm⁻²**, CuS-NC 의 CuS 함량 29 wt% 로 나누면 **호스트 ≈2.0 mg cm⁻²** → **Li2S : CuS-NC ≈ 50 : 50** (SE·바인더 제외). 1 e⁻(→Cu₂₋ₓS, 실제 관측된 반응) 기준이면 호스트 ≈4.1 mg cm⁻² → **33 : 67**. **어느 쪽이든 호스트가 활물질과 같거나 더 무겁다** — 우리 AB 20 wt% 와는 전혀 다른 무게 배분이다. |
| G3 | **전압창의 기준전극은 주어지지만 절대창이 본문에 없다.** 본문에 명시된 전압 기준은 "the plateau at 1.35 V (**vs Li/In**)" 한 곳뿐이다. | `[도표]` 그림 축은 전부 `V vs. Li/In` 이고, 충전 컷오프 ≈**2.5 V vs Li–In**, 방전 컷오프 ≈**0.8 V vs Li–In** 이다 (Fig. 2c, 3a, 3c, 3d). **vs Li/Li⁺ 로 환산하려면 Li–In 평탄전위가 필요한데 이 논문은 그 값을 적지 않는다** — 이 위키는 그 수치의 근거 raw 가 없으므로 환산하지 않는다 (SCHEMA 단위 특칙). |
| G4 | **성형 압력도 스택(운전) 압력도 없다.** "pressed into a pellet" 이 전부. | 고체셀 결과를 비교할 수 없게 만드는 1순위 변수다. Huang 2026(450 MPa 성형)·Zhang 2026(400 MPa 성형 / 1–4 MPa 운전)과 나란히 놓을 수 없다. 우리 펠릿과의 비교도 불가. |
| G5 | **대조군이 "없음" 이 아니라 "덜 좋은 것" 뿐이다.** 비교는 항상 **CuS-NC/Li2S vs NC/Li2S** 두 개다. **CuS 없는 상용/pristine Li2S 대조군, 통상 도전재(AB·Super P·KB) 대조군, CuS 단독(탄소 없이) 대조군이 전부 없다.** | 그래서 이 논문에서 **"pristine Li2S 대비 개선폭"을 읽어낼 수 없다.** 우리 reference cell 의 기준선과 직접 잇는 다리가 이 논문에는 없다 — 그 다리는 Zhang 2026 의 pristine ≈270 mAh g⁻¹(Li2S) 쪽에서 와야 한다 (§14). |
| G6 | **CuS 의 용량 기여를 실험으로 분리하지 않았다.** `[인쇄]` "estimated to contribute only ≈10% of the capacity **based on a comparison of charge and discharge** (Figure 2c and 3c)". | 즉 **첫 충전과 첫 방전의 차이를 전부 CuS 탓으로 돌린** 산술이다. 같은 차이를 만들 수 있는 다른 원인(SE 산화 부산물의 환원, Li–In 으로부터의 Li 공급, 첫 사이클 비가역)을 배제하지 않았다. `[재현]` 이 "차이" 를 첫 사이클 CE 로 환산하면 **110 % (2.3/2.1) · 113 % (4.4/3.9) · 112 % (9.6/8.6)** 다 — 세 로딩 모두 **첫 방전이 첫 충전보다 크다**. CuS/Li2S 복합양극은 첫 사이클에 **음극에서 Li 을 빌린다**. |
| G7 | **유지율의 분모가 "첫 사이클" 인데 최대 용량은 "중간 사이클" 에서 따온다.** `[도표, Fig. 6b·6e·6f 와 Fig. 7]` 500 사이클 끝값 ≈0.85 / 1.1(초기) = **77 %**(논문 값과 일치) 이지만 **최대 1.3 대비로는 65 %**. 10 mg 셀은 6.2/6.7 = 93 %(논문 92 %) 이지만 **최대 9.0 대비 69 %**. 60 °C 셀은 4.4/5.0 ≈ 88 %(논문 85 %) 이지만 **최대 5.8 대비 76 %**. | 초록·본문·결론이 자랑하는 용량(1.8 / 9.6 / 5.8 mAh cm⁻²)은 **최대값**이고 유지율은 **초기값 기준**이다. 두 수치의 분모가 다르다. 그대로 인용하면 성능을 과대평가한다. |
| G8 | **60 °C · 4 mg cm⁻² 셀의 최대 용량 5.8 mAh cm⁻² 는 Li2S 이론용량을 넘는다.** `[재현]` 4 mg cm⁻² × 1166 mAh g⁻¹(Li2S) = **4.66 mAh cm⁻²** → 측정값은 그 **124 %**. CuS 몫(2 e⁻ 기준 `[재현]` ≈0.66)을 더한 5.32 로 봐도 **109 %**. | 논문은 이 초과를 **한 번도 언급하지 않는다.** 같은 문단에서 "60 °C 첫 충전에 argyrodite 산화로 보이는 1.9–2.06 V plateau 가 있었다" 고 스스로 적었으므로, 초과분이 **SE 분해 전류**일 가능성이 가장 크다. **60 °C 데이터는 용량 근거로 쓰면 안 된다.** |
| G9 | **셀 개수·오차 막대·재현성이 전혀 없다.** 모든 사이클 곡선이 단일 셀이다. 통계 언급 없음. | Fig. 6a 의 CuSNC 초기 요동(25번째 사이클 급강하 후 복귀)과 Fig. 6d 의 50–60 사이클 급락→부분 회복이 계통인지 사고인지 판별 불가. |
| G10 | **Fig. 6d 의 본문 서술이 그림과 맞지 않는다.** `[인쇄]` "the capacity increased from 3.5 to 4.0 mAh cm⁻², **where it remained relatively stable over 80 cycles**". `[도표]` 실제로는 45–60 사이클에서 **≈1.6 mAh cm⁻² 까지 급락**했다가 ≈2.5 로 부분 회복하고 80 사이클에서 **≈2.3** 으로 끝난다 (최대 대비 **58 %**). | 4 mg cm⁻² 상온 셀은 **안정하지 않았다.** 이 그림이 이 논문에서 서술과 데이터가 가장 크게 어긋나는 곳이다. |
| G11 | **본문에 방향이 뒤집힌 문장이 하나 있다.** `[인쇄]` p.3–4: "…justify why the current response and oxidation capacity are much higher for **NC/Li2S than CuS-NC/Li2S**." | 앞뒤 문단·Fig. 2a·2c 와 정반대다 (CuSNC 0.61 mA / 2.1 mAh cm⁻² vs NC 0.21 mA / 1.2 mAh cm⁻²). **단순 오기**로 읽어야 하지만, 교정이 이 정도로 샜다는 사실 자체를 기록해 둔다. |
| G12 | **초록과 본문의 면적용량이 다르다.** 초록 `[인쇄]`: "reaches an areal capacity of **1.8 mAh cm⁻²** and a retention rate of **94 %** after 100 cycles" / "at 1.0 mA cm⁻², maintains stable performance over 500 cycles (0.05 %/cycle); at a higher loading, **9.6 mAh cm⁻²**, albeit with more limited cycling". 서론 `[인쇄]`: "areal capacity of up to **1.3 mAh cm⁻²** … over 500 cycles" · "**9.6 mAh cm⁻²** and excellent retention of **91.9 %**". | 1.8(0.3 mA 최대)과 1.3(1 mA 최대)은 **다른 조건의 값**인데 초록·서론이 서로 다른 것을 대표값으로 골랐다. 인용할 때 조건을 반드시 붙여야 한다. |
| G13 | **"NC/Li2S 의 초기 용량 0.5 mAh g⁻¹" — 단위 오기.** `[인쇄]` p.6: "an initial capacity of only 0.5 mAh g⁻¹ and a stabilized capacity of 0.3 mAh cm⁻²". | 0.5 는 **mAh cm⁻²** 여야 한다 (Fig. 6a 와 일치). 이 논문에서 mAh g⁻¹ 이 등장하는 거의 유일한 자리가 오기다 — G2 의 "비용량을 쓰지 않는다" 와 같은 뿌리. |
| G14 | **전자 전도도와 이온 전도도를 같은 시료에서 쟀는지 불분명하다.** `[인쇄]` 이온: "The CuS-NC/**Li2S/SE** cathode composite displayed an effective ion conductivity of 6.4×10⁻⁵ S cm⁻¹". 전자: "The electronic conductivity of the CuS-NC/Li2S **host** (2.9×10⁻⁴ S cm⁻¹)" — 한 곳은 SE 포함, 한 곳은 "host". Figures S6·S7·S14·S15 가 SI 에 있고 미확보. | **σ_e 와 σ_Li 의 시료가 다르면 "200배 낮은 전자전도도인데도 빠르다" 는 논증의 축이 흔들린다.** Huang 2026 G6 과 같은 종류의 공백(시료 정체 불명)이다. |
| G15 | **CuS 를 넣었더니 전자 전도도가 200배 *떨어진* 이유를 설명하지 않는다.** CuS 는 준금속성 황화물인데 결과는 NC/Li2S 5.7×10⁻² → CuS-NC/Li2S 2.9×10⁻⁴ S cm⁻¹ 이다. | 같은 "호스트 wt%" 라면 CuS-NC 는 탄소가 71 wt% 뿐이라 **탄소 함량 자체가 다르다**(G2 미기재와 얽힌다). 즉 **CuS 유무 이외의 변수가 최소 하나 더 다르다** — 촉매 효과의 원인 분리가 그만큼 약해진다. 논문은 이 낮은 전도도를 오히려 "SE 산화를 덜 일으켜 좋다" 고 **사후 해석**한다 (근거 없음). |
| G16 | **Fig. 4a 의 참조 패턴 줄에 "CNT" 가 있다.** `[도표]` pristine/charge/discharge 3줄 아래에 측정된 **CNT** XRD 가 한 줄 들어가 있는데, **본문·캡션은 CNT 를 한 번도 언급하지 않는다.** | 양극에 **CNT 가 도전재로 들어갔을 가능성**을 시사한다 (같은 그룹 Kwok 2023 *EES* 16, 610 의 양극이 CNT 를 쓴다). 그렇다면 "호스트가 전자망을 만든다" 는 그림이 달라진다. SI Methods 없이는 확정 불가. |
| G17 | **CuS 29 wt% 가 직접 측정값이 아니다.** `[인쇄]` "calculated … by measuring the Cu content in Cu**NC** by TGA under O2, and **assuming all the Cu was converted to CuS** on sulfidation". | 황화 전 시료의 Cu 함량 + 완전황화 가정이다. ICP·EDS 정량이 없다. 이 29 wt% 가 G2 의 조성 추정 전체를 받치고 있다. |
| G18 | **DFT 계산 조건이 본문에 없다** (함수형·코드·vdW·슬랩 두께·용매/전해질 환경). NEB 는 `Li2S → LiS + Li⁺ + e⁻` **한 단계**만 본다. | 0.4 eV vs 0.9 eV 는 **진공 슬랩 위 고립 Li2S 분자 한 개**의 첫 Li 탈리 장벽이다. 실제 양극의 마이크론 Li2S 벌크 산화와 같은 물리가 아니다. `[해석]` DFT 는 "그럴듯함" 의 근거이지 기전의 증명이 아니다. |
| G19 | **"charge transfer 1.1 eV / 0.8 eV" 는 단위가 틀렸다.** `[인쇄]` "higher negative charge transfer from Li2S to CuS (1.1 eV) than Li2S to NC (0.8 eV)". | 전하이동량의 단위는 **e** 이지 eV 가 아니다. 게다가 1.1 은 흡착에너지 차이(−3.2 −(−2.1) = 1.1 eV)와 **같은 숫자**다. Figure S9 를 못 봤으므로 어느 쪽이 맞는지 판정 불가. |
| G20 | **N 도핑의 역할을 실험으로 분리한 곳이 없다.** N 종류별 기여는 **DFT(pyrrolic/pyridinic/graphitic 흡착에너지)와 XPS 귀속**뿐이고, **도핑 없는 탄소 대조군이 없다.** | 제목의 "Nitrogen-Doped" 가 성능에 무엇을 더했는지 이 논문 안에서는 알 수 없다. `[해석]` N 은 여기서 **CuS 나노결정을 고정(Cu–N4)하는 앵커**로 기능했을 가능성이 크고, 그 자체도 검증되지 않았다. |
| G21 | **에너지밀도·셀 수준 수치가 없다.** SE 두께·질량, 셀 면적, N/P 가 전부 없다. | 9.6 mAh cm⁻² 가 실용성 주장의 핵심인데 분모가 없다. Fig. 7 의 문헌 비교도 **면적용량 vs 사이클 수** 2축뿐이라 로딩·압력·온도가 섞여 있다. |

---

## 0. 서지사항 (직접 확인)

`[인쇄]` PDF 1쪽 + 말미:

| 항목 | 값 |
|---|---|
| 제목 | A Nanocrystallite CuS/Nitrogen-Doped Carbon Host Improves Redox Kinetics in All-Solid-State Li2S Batteries |
| 저자 | Yue Yu, Baltej Singh, Zhuo Yu, Chun Yuen Kwok, Ivan Kochetkov, **Linda F. Nazar (교신)** |
| 소속 | Department of Chemistry and Waterloo Institute for Nanotechnology, University of Waterloo, Ontario, Canada |
| 학술지 | *Advanced Energy Materials* **14** (2024) 2400845 (issue 27) |
| DOI | **10.1002/aenm.202400845** |
| 접수/개정/게재 | Received 22 February 2024 · Revised 12 April 2024 · Published online 15 May 2024 |
| 키워드 | all-solid-state batteries · argyrodite solid-state electrolyte · Li2S cathode · Li2S redox · Li–sulfur battery |
| 지원 | **Conamix, Inc.** · Ontario Research Fund |
| 사의 | XPS — Peter Brodersen (Univ. of Toronto) · XANES — Mark Wolfman (Advanced Photon Source, ANL) · TEM — Lei Zhang |
| 이해충돌 | "The authors declare no conflict of interest" |
| 데이터 가용성 | "available in the supplementary material of this article" |

`[해석]` 두 가지 맥락이 있다. (i) **Li5.5PS4.5Cl1.5 argyrodite 는 이 그룹 자신의 재료**다
(ref 16 = Adeli, Bazak, Park, Kochetkov, Huq, Goward, Nazar, *Angew. Chem.* 2019 — 공저자
Kochetkov 가 이 논문에도 있다). (ii) **직전 논문이 Kwok, Xu, Kochetkov, Zhou, Nazar,
*Energy Environ. Sci.* 16 (2023) 610 (ref 18, core–shell Li2S/LiVS2)** 이고, 공저자 Kwok 이
이 논문에도 있다. **Huang 2026 의 DC 분극 전도도 측정 절차가 인용한 출처가 바로 그
Kwok 2023** 이다 — 세 논문이 같은 측정 계보 위에 있다 (§13).
자금 출처가 **Conamix(Li–S 스타트업)** 라는 점은 성능 서술의 톤을 읽을 때 참고할 맥락이다.

---

## 1. 한 문단 요약

`[해석]` 저자들은 dopamine·Cu(NO3)2·NaCl 을 동결건조한 뒤 N2/H2 800 °C 로 탄화하고
물로 NaCl 주형을 씻어낸 다음 황화해서, **다공성 N-도핑 탄소 골격에 50–100 nm 육방정
CuS 나노결정이 박힌 호스트(CuS-NC, CuS 29 wt%)** 를 만들었다. 이 호스트에 nano-Li2S 를
섞어 **Li5.5PS4.5Cl1.5 | Li–In 전고체 셀**의 양극으로 썼고, 대조군은 **CuS 없는 N-도핑
탄소(NC)** 하나다. 결과의 뼈대는 넷이다: (1) **첫 충전(활성화)에서** CV 피크가
2.41 → **2.14 V vs Li–In** 으로 내려가고 Tafel 기울기가 151 → **84 mV dec⁻¹**, 활성화
용량이 1.2 → **2.1 mAh cm⁻²** (Li2S 이용률 **91 %**) 로 **두 배**가 된다; (2) 그런데
복합체의 **전자 전도도는 오히려 200배 낮고**(5.7×10⁻² → 2.9×10⁻⁴ S cm⁻¹),
**이온 전도도는 1.8배 높다**(3.5×10⁻⁵ → 6.4×10⁻⁵ S cm⁻¹) — 그래서 저자들은 개선의
원인을 **전자망이 아니라 (a) Li2S 흡착·촉매작용과 (b) Li⁺ 수송**으로 돌린다;
(3) DFT 가 그 둘을 각각 받친다 — Li2S 흡착에너지 −2.1(NC) vs **−3.2 eV**(CuS),
Li2S→LiS+Li⁺ 장벽 0.9 vs **0.4 eV**, Li⁺ 이동 장벽 1.5 vs **0.3 eV**;
(4) 셀은 2 mg cm⁻² 에서 0.3 mA cm⁻² 100 사이클 1.5 mAh cm⁻²(CE 99.5 %), 1 mA cm⁻²
500 사이클, 10 mg cm⁻² 에서 첫 방전 **9.6 mAh cm⁻²** 를 낸다. CuS 자체도 방전 중
**CuS → Cu₂₋ₓS** 로 부분 환원돼 용량의 **≈10 %** 를 보태며 (Cu 금속까지는 안 간다),
그 몫은 실험이 아니라 **충·방전 용량 차이**로 추정됐다.

`[해석]` **이 논문의 진짜 주장은 "탄소를 더 잘 깔았다" 가 아니라 "전자 전도도를
희생하고도 계면 화학(흡착·촉매)과 Li⁺ 경로로 더 벌었다" 이다.** 그래서 우리
[[carbon-dimensionality-electron-network]](탄소의 차원 분리)와는 **다른 축**이고,
Huang 2026 의 "혼합 이온–전자 전도체" 와도 **엇갈린다** (그쪽은 σ_e 를 14배 올렸다).
§13 에서 정면으로 대조한다.

---

## 2. p.1–2 — Abstract / Introduction

### 2.1 Abstract 의 명제 `[인쇄]`

- "a N-doped carbon embedded with CuS nanoparticles (CuSNC) is reported as a **host for Li2S**
  in all-solid-state batteries"
- 근거 수단: "XRD, XPS, XAS, electron microscopy, and DFT"
- 기전 주장: "CuSNC provides **good affinity to Li2S**. This **lowers the activation barrier**
  for the conversion of Li2S to sulfur on the charge, **suggesting an electrocatalytic effect**
  on the CuS surface." → `[해석]` "suggesting" 이라는 한정어가 붙어 있다. 촉매는 **가설**로
  제시됐고, 회전율(TOF)·활성점 밀도·Tafel 교환전류 같은 촉매 고유 지표는 없다.
- "Li⁺ diffusion in the cathode and the reaction kinetics are enhanced compared to
  **N-doped graphene**" → `[해석]` 대조군을 초록에서는 "N-doped **graphene**", 본문 §2 에서는
  "N-doped **carbon** (NC) … synthesized as a control material by a **similar method**" 라 부른다.
  **같은 물질의 두 이름**으로 보이지만 확인 불가(Figures S3–S5 미확보).
- 성능: "areal capacity of **1.8 mAh cm⁻²** and a retention rate of **94 %** after 100 cycles" ·
  "at 1.0 mA cm⁻², stable over **500 cycles** (**0.05 % per cycle**)" ·
  "at a higher Li2S loading, delivers **9.6 mAh cm⁻²**, albeit with more limited cycling".

### 2.2 Introduction 의 문제 설정 `[인쇄]`

이 위키가 인용할 만한 "선언된 물성" 들 (전부 이 논문이 **인용으로** 가져온 값이다):

| 항목 | 값 | 출처 표기 |
|---|---|---|
| S 이론 비용량 / 에너지밀도 | 1675 mAh g⁻¹ / ≈2600 Wh kg⁻¹ (S 기준) | 서론 일반 |
| **Li2S 이론 비용량** | **1166 mAh g⁻¹** | 서론 `[인쇄]` — 우리 환산 기준과 일치 |
| S 의 전자 전도도 | 5×10⁻³⁰ S cm⁻¹ | refs 20,21 |
| S→Li2S 부피팽창 | 80 % | refs 18,19 |
| **Li2S 전자 전도도** | **≈10⁻⁹ S cm⁻¹** (상온) | ref 22,23 |
| **Li2S 이온 전도도** | **σ_i ≈10⁻¹³ S cm⁻¹** | refs 21,26 |
| Li5.5PS4.5Cl1.5 전도도 | "almost 10 mS cm⁻¹ at RT" | refs 16,17 (자기 그룹) |
| NMC/흑연 리튬이온 에너지밀도 | ≈250 Wh kg⁻¹ | refs 3,4 |

`[인쇄]` Li2S 로 시작하는 이유를 셋으로 든다: (i) Li2S→S 는 **부피 수축**이라 "팽창된
상태에서 출발하는 기계적으로 튼튼한 전극" 설계가 가능하다; (ii) Li2S 의 전자 전도도가
S 보다 높다(10⁻⁹ vs 10⁻³⁰); (iii) **"it allows the possibility of anode-free batteries
because lithium is stored in the cathode"** (refs 24,25) → 우리 [[anode-free-li2s-assb]] 의
동기와 **같은 문장**이다. 단 이 논문은 실제로는 **Li–In 음극**을 쓴다 (anode-free 실험 없음).

`[인쇄]` 선행 접근을 네 갈래로 정리한다 — 우리 위키가 그대로 쓸 수 있는 분류다:
1. **이온전도 첨가제**: LiI (Li2S–LiI 고용체, refs 27–29) · P2S5 (in-situ Li3PS4, refs 30,31) ·
   **Li2O–LiI–Li2S (비정질 Li2O–LiI, σ_Li = 3.1×10⁻⁵ S cm⁻¹, ref 32)**
2. **나노탄소 구속**: Yao 그룹의 액상법 CNT·2D 메조포러스 탄소 (refs 26,33)
3. **전이금속황화물(TMS)**: core–shell Li2S/LiVS2 · Li2S–V2S3–LiI (refs 18,34) ·
   Cui 그룹의 MS2 (M = Ti, V, Co) 스크리닝 (ref 36) · Qiang et al. 의 DFT (ref 37) ·
   **Manthiram 그룹 Li2S–Co9S8/Co, 1000 사이클 (ref 24)**
4. 그리고 "TMS 의 전고체 Li2S 적용은 **still in its infancy**" 라는 위치 선언.

`[해석]` 3번 갈래가 **Huang 2026(고엔트로피 황화물)과 이 논문(CuS)의 공통 조상**이다.
Huang 2026 이 인용한 Co9S8 논문(ref 24)을 이 논문도 인용한다.

---

## 3. 방법 — 본문에 남은 전부 (SI 미확보)

**아래가 본문에서 방법에 해당하는 문장의 전부다.** 그 밖의 모든 것은 SI 에 있고 미확보다(G1).

### 3.1 CuS-NC 호스트 합성 `[인쇄 + 도표, Fig. 1a]`

| 단계 | 본문 `[인쇄]` | Fig. 1a 모식도 `[도표]` |
|---|---|---|
| 전구체 | Cu(NO3)2·3H2O, NaCl, **dopamine hydrochloride** | 도식에 `C8H12ClNO2`(도파민 염산염)와 `Cu(NO3)2·3H2O` 를 NaCl 수용액에 넣는 그림 |
| 주형 | "templating method" | **NaCl 주형** (수용액 → 동결건조) |
| 건조 | — | **Freeze-drying, −50 °C** |
| 열처리 | "heat treatment" | **튜브로, N2/H2 분위기, 800 °C** |
| 주형 제거 | — | **Water washed → dried** |
| 황화 | "sulfidation" | 마지막 단계 "Sulfuration" (황원·온도·시간 **미기재**) |

`[인쇄]` **NC(대조 호스트)**: "N-doped carbon (NC) was also synthesized as a control material
by a **similar method**; its morphology and elemental distribution are described in Figures
S3–S5." → Cu 염만 뺀 것으로 읽히지만 **명시되지 않았다**.

### 3.2 복합양극·셀 `[인쇄]`

| 항목 | 내용 |
|---|---|
| 활물질 | **nano-Li2S** ("mixing **nano-Li2S** with CuS-NC or NC") — 공급사·입도·합성법 **미기재** |
| 혼합 | "**mixing**" 단 한 단어. 장비·rpm·시간·분위기·습식/건식 전부 **미기재** (G1) |
| 조성비 | **미기재** (G2 — 이론용량으로부터 `[재현]` Li2S : CuS-NC ≈ 50:50 ~ 33:67 추정) |
| 바인더 | 언급 없음 (`[해석]` 펠릿 셀이므로 무바인더로 보이나 확인 불가) |
| 성형 | "pressed into a pellet" — **압력·시간·다이 직경 미기재** (G4) |
| SE | **Li5.5PS4.5Cl1.5** (argyrodite, 자기 그룹 재료 ref 16) — 두께·질량 미기재 |
| 음극 | **Li–In alloy** (조성비·두께 미기재) |
| 로딩 | **Li2S 기준 2 / 4 / 10 mg cm⁻²** |
| 온도 | **room temperature** (수치 미기재) 및 **60 °C** |
| 스택 압력 | **미기재** (G4) |
| 셀 면적 | **미기재** |

### 3.3 전기화학·분석 조건 (본문에 흩어진 것)

| 측정 | 조건 |
|---|---|
| CV (활성화) | `[인쇄]` 0.1 mV s⁻¹ · `[도표, Fig. 2a]` 창 ≈1.5 → 2.5 V vs Li–In |
| CV (활성화 후) | `[인쇄]` 0.1 mV s⁻¹ · `[도표, Fig. 3a]` 창 ≈0.8 ↔ 2.5 V vs Li–In |
| 첫 충전 | `[도표, Fig. 2c]` **0.1 mA cm⁻²**, 컷오프 ≈2.5 V vs Li–In |
| 율속 방전 | `[인쇄]` 0.1 / 0.5 / 1 mA cm⁻² (Fig. 3c); 율속 시험은 0.1/0.2/0.5/1/2 mA cm⁻² (Fig. 6c) |
| 사이클 | 0.3 mA cm⁻² (2·4·10 mg cm⁻², RT; 4 mg 60 °C) · 1 mA cm⁻² (2 mg, RT) |
| GITT | `[인쇄]` Figure S11 (미확보) — OCP/CCP 비교 |
| DC 분극 | `[인쇄]` "**electron-blocking symmetric cells**", "direct current polarization method" (Fig. 5a,b; Figs. S14–S15) · `[도표]` ±100 / ±50 / ±25 mV, **각 1 h**, 총 6 h |
| EIS | `[인쇄]` Figure S20 — 50 사이클에 걸친 Nyquist |
| ex situ XRD | `[인쇄]` "the composite electrode material was **washed with ethanol** to remove the otherwise dominant reflections of Li2S and argyrodite (see Methods, SI)" |
| XPS | Cu 2p · N 1s · C 1s (Univ. of Toronto) |
| XANES | Cu K-edge, APS (Figure S12) |
| DFT | 흡착에너지 · NEB (Li2S 분해, Li⁺ 이동) — **계산 조건 미기재** (G18) |

`[해석]` ex situ XRD 의 **에탄올 세척**은 이 계에서 위험한 조작이다. Li2S 와 argyrodite 를
"씻어 없앤다" 는 것은 곧 **시료를 화학적으로 바꾼 뒤 찍었다**는 뜻이고, Cu₂₋ₓS 피크의
생성이 세척 과정과 무관하다는 대조(세척한 pristine 과 세척 안 한 것)가 필요한데 본문에
없다. Fig. 4a 의 pristine/charge 역시 같은 세척을 거쳤다면 상대비교로는 성립한다.

---

## 4. p.2–3 — CuS-NC 호스트의 구조·조성 (Fig. 1)

| 관측 | 값 `[인쇄]` | 그림 `[도표]` |
|---|---|---|
| XRD | "covellite **CuS as the only crystalline phase**" | Fig. 1b — CuS JCPDS **01-079-2321** 과 일치, 20–27° 에 **넓은 비정질 탄소 험프** |
| SEM | "typical porous N-doped carbon morphology on the **micron scale**" | Fig. 1c — 스케일바 **10 µm**, 다공성 시트 응집체 |
| TEM | "**50–100 nm hexagonal crystallites** anchored on the walls of the carbon framework" | Fig. 1d — 스케일바 100 nm, 육각 판상 입자가 탄소 벽에 붙어 있다 |
| HRTEM | 격자간격 **0.304 nm = CuS (102)** | Fig. 1e — 스케일바 10 nm |
| N 1s XPS | **401.5 graphitic N · 400.5 pyrrolic N · 399 pyridinic N · 398 eV Cu─N (Cu-N4 배위)** | Fig. 1f — **pyrrolic N 이 가장 크다** |
| C 1s XPS | **284.5 sp² C─C** ("adventitious carbon 기여 배제 불가" 라고 스스로 적음) · **285.5 sp³ C─C** · **287.0 eV C─N** | Fig. 1g |
| HAADF-STEM + EDS | "CuS nanocrystallites are **uniformly dispersed**"; "Some regions are apparently **rich in both Cu and N**" | Fig. 1h — C/N/S/Cu 4원소 맵, 스케일바 1 µm. `[도표]` **Cu 와 S 맵은 서로 겹치고 N 맵은 C 보다 좁다** |
| **CuS 함량** | **29 wt%** — TGA(O2) 로 CuNC 의 Cu 함량을 재고 **완전황화 가정** (Figure S2, 미확보) | — (G17) |

`[해석]` 이 절의 중요한 사실 두 가지. (i) **Cu–N4 결합 피크(398 eV)** 가 있다는 것은
N 이 Cu 를 붙잡는 앵커로 작동했다는 뜻이고, 이것이 "CuS 가 왜 50–100 nm 로 분산되는가" 의
설명이다 — 즉 **N 도핑의 역할은 촉매가 아니라 고정일 가능성이 크다** (G20). (ii) CuS 결정은
**50–100 nm 로 작지 않다.** 제목의 "nanocrystallite" 는 그 크기를 말한다. 우리가 쓰는 AB
일차입자(수십 nm)와 비슷한 척도다.

---

## 5. p.2–3 — 첫 충전 활성화 (Fig. 2a–c) ★ 우리 축의 핵심

### 5.1 CV — 활성화 피크 `[인쇄 + 도표, Fig. 2a]`

| 시료 | 활성화 피크 전위 | 피크 전류 |
|---|---|---|
| **CuSNC/Li2S** | **2.14 V vs Li–In** | **0.61 mA** |
| NC/Li2S | **2.41 V vs Li–In** | **0.21 mA** |

`[인쇄]` "indicating higher polarization and a slower response" (NC 쪽).
`[도표]` 스캔 0.1 mV s⁻¹, 창 1.5 → 2.5 V vs Li–In. **두 곡선 모두 ≈1.7 V 부터 전류가 뜬다** —
개시 전위 자체는 거의 같고 **차이는 전위가 아니라 전류 크기**다.
`[해석]` 피크 전류가 3배 차이 나는데 **활성 면적(BET)·전극 두께·시료 질량이 같은지 명시되지
않았다.** 로딩은 같다고 적혀 있으나(2 mg cm⁻² Li2S) 호스트 질량이 같은지는 G2 때문에 모른다.

### 5.2 Tafel — 활성화(Li2S → S) `[인쇄, Fig. 2b]`

| 시료 | Tafel 기울기 |
|---|---|
| **CuSNC/Li2S** | **84 mV dec⁻¹** |
| NC/Li2S | **151 mV dec⁻¹** |

`[도표]` x축이 `Log|j| (mA)` 로 **전류밀도가 아니라 전류**이고, 두 데이터가 겹치는
전류 구간이 거의 없다 (CuSNC: log j −2.45…−2.0, NC: −1.95…−1.75). `[해석]` **서로 다른
전류 구간에서 딴 기울기**를 비교한 것이다. 교환전류밀도(j₀)는 보고되지 않았다.

### 5.3 갈바노스태틱 첫 충전 (Fig. 2c) ★★

`[인쇄]` 로딩 **Li2S 2 mg cm⁻²**, `[도표]` **0.1 mA cm⁻²**, 컷오프 ≈2.5 V vs Li–In.

| 시료 | 첫 충전 면적용량 | `[재현]` mAh g⁻¹(Li2S) | `[재현]` mAh g⁻¹(S) | Li2S 이용률 |
|---|---|---|---|---|
| **CuSNC/Li2S** | **2.1 mAh cm⁻²** `[인쇄]` | **1050** | **1505** | **≈91 %** `[인쇄]` |
| NC/Li2S | **1.2 mAh cm⁻²** `[인쇄]` | **600** | **860** | **51 %** `[재현]` (1.2/2.33) |
| (이론) | 2.3 mAh cm⁻² `[인쇄]` | 1166 | 1675 | 100 % |

`[도표, Fig. 2c]` **plateau 모양이 결정적으로 다르다**: CuSNC 는 1.75 V 에서 시작해
**≈2.0–2.1 V 의 완만한 상승 plateau** 를 2 mAh cm⁻² 가까이 끌고 가다 끝에서 급상승한다.
NC 는 같은 1.78 V 에서 출발하지만 **즉시 2.1 V 로 치솟아** 곧장 2.3 → 2.5 V 컷오프로 올라가
1.2 mAh cm⁻² 에서 끝난다. **Li2S 계 특유의 "첫 충전 초기 과전압 봉우리(전압 스파이크)는
두 시료 모두 뚜렷하지 않다.**

`[해석]` 이것이 이 논문에서 우리에게 가장 값진 한 장이다 — **같은 SE·같은 음극·같은
로딩·같은 전류에서 호스트만 바꿔 첫 충전 활성화량이 51 % → 91 % 로 갈린다.**
[[li2s-activation-first-charge]] 에 붙는 **고체계 직접 근거**이고, anode-free 로 보면
**활성화량 = Li 재고**이므로 재고가 1.8배 차이 난다는 뜻이다.
단 `[해석]` **활성화 전위(≈2.0–2.1 V vs Li–In)는 여전히 SE 산화 위험 구간 근처**이고,
실제로 NC 쪽에서는 Fig. 3d 에 "Electrolyte decomposition" 이라고 저자들이 직접 표시했다.

---

## 6. DFT — 흡착·분해장벽·Li⁺ 이동 (Fig. 2d–i, Fig. 5c–d)

`[인쇄]` 모델 선정 근거: "**pyrrolic N is the dominant species in NC** as revealed by XPS
(Figure S5)" → pyrrolic N 도핑 그래핀 슬랩 vs CuS 표면을 비교. pyridinic/graphitic N 결과는
Figure S8(미확보).

| 양 | NC(pyrrolic N) | CuS | 차이 |
|---|---|---|---|
| Li2S **흡착에너지** `[도표, Fig. 2d,e]` | **−2.1 eV** | **−3.2 eV** | 1.1 eV `[인쇄]` "by ≈1.1 eV" |
| Li–S **결합거리** `[도표, Fig. 2f 표]` | 2.23 / 2.33 Å | **2.39 / 2.39 Å** | (자유 Li2S = 2.1 / 2.1 Å) |
| 전하이동 `[인쇄, Fig. S9]` | 0.8 "eV" | 1.1 "eV" | 단위 오기(G19) |
| **Li2S → LiS + Li⁺ + e⁻ 장벽** `[인쇄]` | **0.9 eV** | **0.4 eV** | `[도표, Fig. 2i]` 실제 곡선 최댓값은 ≈0.92 vs ≈0.50 eV |
| **Li⁺ 표면 이동 장벽** `[인쇄, Fig. 5c,d]` | **1.5 eV** | **0.3 eV** | `[도표]` NC 곡선은 3 Å 까지 단조 상승해 1.5 에서 평탄 |

`[인쇄]` 결론 문장: "indicating a **strong electrocatalytic effect** on the CuS surface" ·
"Li ion diffusion is **more facile on the surface of CuS**".

`[해석]` 세 가지를 갈라 읽어야 한다.
1. **흡착 강화(−3.2 eV)와 Li–S 결합 신장(2.39 Å)은 서로 정합적**이다. 여기까지는 깔끔하다.
2. **그러나 흡착이 강할수록 좋다는 논리에는 한계가 있다** — 촉매의 일반 원리(Sabatier)상
   너무 강한 흡착은 생성물 탈리를 막는다. 이 논문은 **산화 방향만** 계산하고
   **방전 방향(S → Li2S)의 장벽은 계산하지 않았다.** 그런데 Fig. 3b 의 Tafel 은 방전 방향이다.
3. **Li⁺ 이동 장벽 1.5 eV(NC)는 비현실적으로 크다.** 그 값이 맞다면 NC/Li2S 셀은 상온에서
   거의 작동하지 못해야 하는데 실제로는 0.5–1.3 mAh cm⁻² 를 낸다. `[해석]` **표면 확산 모델이
   실제 수송 경로(SE 를 통한 Li⁺ 수송)와 다른 물리**를 보고 있다는 신호다. 실제 셀의 Li⁺ 는
   argyrodite 를 타고 가지 탄소 표면을 기어가지 않는다.

---

## 7. p.4 — 활성화 후 산화환원 (Fig. 3)

### 7.1 CV (활성화 사이클 이후) `[도표, Fig. 3a]`

| 시료 | 산화 피크 | 환원 피크 | 피크 분리 `[재현]` |
|---|---|---|---|
| **CuSNC/Li2S** | **1.91 V** (≈+0.57 mA) | **1.12 V** (≈−0.65 mA) | **0.79 V** |
| NC/Li2S | **1.95 V** (≈+0.17 mA) | **0.97 V** (≈−0.25 mA) | **0.98 V** |

`[인쇄]` "much higher current response and lower polarization … for CuS-NC/Li2S".
`[도표]` 창 0.8 ↔ 2.5 V vs Li–In, 0.1 mV s⁻¹. **CuSNC 곡선에는 1.6 V 부근에 어깨**가 있다
(`[해석]` CuS ↔ Cu₂₋ₓS 로 볼 만하나 논문은 CV 에서 그 귀속을 하지 않는다).

### 7.2 Tafel (S → Li2S, 방전) `[인쇄, Fig. 3b]`

**CuSNC 278 mV dec⁻¹ vs NC 356 mV dec⁻¹** — "faster electrode kinetics **despite its
200-fold lower electronic conductivity**".
`[해석]` 두 값 모두 **200 mV dec⁻¹ 을 훌쩍 넘는다.** 단일 전자이동 반응의 Tafel 기울기는
상온에서 약 120 mV dec⁻¹ 가 상한이다. 278·356 은 전하이동이 아니라 **저항 지배(IR)** 영역을
보고 있다는 뜻에 가깝다. 그렇다면 "kinetics" 라는 해석보다 "총 셀 저항" 이라는 해석이 맞고,
그것은 σ_Li 1.8배 차이와 정합적이다.

### 7.3 율속 첫 방전 (Fig. 3c) `[인쇄 + 재현]`

로딩 2 mg cm⁻²(Li2S). `[도표]` 방전 컷오프 ≈0.8 V vs Li–In.

| 전류밀도 | CuSNC `[인쇄]` | `[재현]` (Li2S) | `[재현]` (S) | NC `[인쇄]` | `[재현]` (Li2S) | `[재현]` (S) |
|---|---|---|---|---|---|---|
| 0.1 mA cm⁻² | **2.3 mAh cm⁻²** | 1150 | 1648 | **1.3 mAh cm⁻²** | 650 | 931 |
| 0.5 mA cm⁻² | ≈1.6 `[도표]` | 800 | 1146 | ≈0.35 `[도표]` | 175 | 251 |
| 1 mA cm⁻² | **1.3** | 650 | 931 | **0.13** | 65 | 93 |

`[인쇄]` "the areal capacity of CuS-NC/Li2S **dropped by half** … NC/Li2S exhibited a
**tenfold drop**". 이론값: CuSNC **2.66 mAh cm⁻²** (CuS+Li2S 완전환원), NC **2.33** (Li2S만).

`[중요·인쇄, Fig. 3c 캡션]` "we note that **≈10 % additional capacity is contributed from CuS
on discharge** (compared to charge, see Fig 2c)". → `[재현]` CuS 몫을 빼면 CuSNC 의 0.1 mA
첫 방전은 **≈2.07 mAh cm⁻² = 1035 mAh g⁻¹(Li2S) = 1483 mAh g⁻¹(S)**.

### 7.4 10번째 사이클의 과전압 (Fig. 3d) `[인쇄]`

0.3 mA cm⁻², 10th 사이클을 고른 이유는 "at this point, the capacity is relatively constant".

| 시료 | 과전압 | 방전 면적용량 | `[재현]` (Li2S) | `[재현]` (S) |
|---|---|---|---|---|
| **CuSNC/Li2S** | **0.64 V** | **1.75 mAh cm⁻²** | **875** | **1254** |
| NC/Li2S | **0.95 V** | **0.6 mAh cm⁻²** | **300** | **430** |

`[인쇄]` NC 쪽 충전 곡선의 "**additional weak charge plateau between 1.98 V and 2.5 V** …
may be attributed to **argyrodite oxidation**, which is not observed for CuS-NC/Li2S".
`[도표, Fig. 3d]` 그 구간에 "Electrolyte decomposition" 이라는 주석이 그림 안에 찍혀 있다.
`[인쇄]` 이어지는 해석: CuSNC 의 낮은 전자 전도도(2.9×10⁻⁴)가 "**likely helps to limit the
oxidation of the solid electrolyte** on contact with the host".

`[해석]` **이 문장이 이 논문에서 가장 흥미롭고 가장 근거가 약한 주장이다.** "전자 전도도가
낮아서 SE 가 덜 분해된다" 는 명제는 우리 설계(AB 20 wt%)에 정면으로 걸리지만, 이 논문은
그것을 **대조 실험 없이 한 문장으로** 말한다. SE 분해량(XPS S 2p·P 2p 정량, 가스 발생,
임피던스 증가)을 재지 않았다. → §17 의 "가져갈 가설" 로 기록.

---

## 8. p.5 — CuS 자체의 산화환원 (Fig. 4) — 용량 기여를 어떻게 다뤘나

`[인쇄]` ex situ XRD·XPS·XANES 를 CuSNC/Li2S 양극에 걸었다 (에탄올 세척 후).

| 상태 | XRD `[인쇄 + 도표, Fig. 4a]` | Cu 2p XPS `[인쇄 + 도표, Fig. 4b]` |
|---|---|---|
| pristine | CuS 회절선 | 2p3/2 **932.39 eV = Cu²⁺** |
| **충전 후** | "**no change**" — CuS 안정 | **Cu²⁺ 그대로** → "CuS **does not undergo redox during charge**" |
| **방전 후** | CuS 피크 감소 + **≈46.5° 에 Cu₂₋ₓS 새 피크**(별표) | **저결합에너지 쪽으로 이동, Cu⁺ 성분이 주성분** |
| 2차 충전 후 | — | `[인쇄, Fig. S13]` "**CuS is regenerated**" → 가역 |
| Cu 금속 | `[인쇄]` "it is **not** reduced to Cu metal" (Cu JCPDS 참조선에 해당 피크 없음) | — |
| XANES | `[인쇄, Fig. S12]` 방전 시료의 Cu 원자가가 **Cu(II)S 와 Cu(I)₂S 사이** — "the precise oxidation state **could not be determined**" | — |

`[인쇄]` 요약 문장 (§ "In summary to this point"):
- **첫 충전에서는 Li2S → S 산화가 유일한 과정이다** ("the oxidation of Li2S to sulfur is the
  **sole process**") → `[해석]` **첫 충전 용량 전부를 Li2S 활성화로 읽어도 된다**는 뜻이다.
  이용률 91 % 가 그래서 의미를 갖는다.
- **첫 방전의 1.35 V (vs Li/In) plateau = S → Li2S**, 여기에 **CuS → Cu₂₋ₓS 가 겹치며
  용량의 ≈10 % 를 보탠다.**
- **Cu₂₋ₓS → Cu 는 일어나지 않는다.**

`[해석]` 세 가지 판단.
1. **"CuS 는 활물질이자 촉매" 다.** 이 논문은 CuS 를 촉매로 부르지만 데이터는 **방전에서
   전자를 받는 활물질**임을 분명히 보인다. 두 역할이 섞여 있고 분리되지 않았다(G6).
2. **CuS 의 용량 기여 추정이 순환 논법에 가깝다.** 충·방전 차이를 CuS 탓으로 돌리고,
   그 차이로 "10 %" 를 만들고, 다시 그 10 % 로 이론용량 2.66 을 세워 이용률을 계산한다.
3. **anode-free 관점에서는 이 10 % 가 순손실이다** — CuS 환원에 쓰인 Li 은 Li2S 에서 온 것이
   아니라 **음극(Li–In)에서 온 것**이다 (첫 사이클 CE 110–113 %, G6). Li 재고가 양극에만
   있는 anode-free 셀에서는 그만큼 Li2S 활성화분을 갉아먹는다. **우리 2단계에 직접 걸린다.**

---

## 9. p.5–6 — 전도도: 전자 vs 이온 (Fig. 5a,b) ★

`[인쇄]` "Because CuS-NC/Li2S exhibits a **much lower electronic conductivity** than NC/Li2S,
it is important to determine the Li⁺ transport properties…"

| 시료 | σ_e⁻ `[인쇄, Fig. S7]` | σ_Li⁺ `[인쇄, Fig. 5a,b]` | `[재현]` σ_Li/σ_e |
|---|---|---|---|
| **CuS-NC/Li2S(/SE)** | **2.9×10⁻⁴ S cm⁻¹** | **6.4×10⁻⁵ S cm⁻¹** | 0.22 |
| NC/Li2S(/SE) | **5.7×10⁻² S cm⁻¹** | **3.5×10⁻⁵ S cm⁻¹** | 6.1×10⁻⁴ |
| 비 (CuSNC/NC) | **×1/197** (`[인쇄]` "≈200-fold higher for NC") | **×1.83** (`[인쇄]` "nearly twofold") | — |

`[도표, Fig. 5a,b]` 전자차단 대칭셀에 **±100 / ±50 / ±25 mV 를 각 1 h** 인가한 계단
분극이다 (총 6 h). 정상전류: CuSNC 100 mV 에서 **≈0.22–0.25 mA**, NC 는 **≈0.12 mA**.
`[해석]` 두 셀 모두 전류가 계단 안에서 완만히 감소한다 — Huang 2026 G8 과 같은
"정상상태 도달 여부" 문제가 여기도 있으나, 감소폭은 그쪽보다 작다.

`[인쇄]` 기전 가설: "The presence of CuS **may facilitate the formation of a defect phase
such as Li₂₋ₓS at the interface**, which can support Li interstitials that provide better Li⁺
transport than crystalline Li2S (ref 44)." → `[해석]` **"may" 가설이고 검증 데이터가 없다.**
Li₂₋ₓS 를 본 관측(XRD·XPS·NMR)이 이 논문에 없다.

`[인쇄]` 보조 근거 셋 (전부 SI, 미확보):
- CV 스캔속도 의존 `i = av^b` → **b = 0.53(CuSNC) / 0.56(NC)** — 둘 다 ≈0.5 로 **확산 지배**.
  `[해석]` 두 값이 사실상 같다. 이 지표로는 두 시료가 구별되지 않는다.
- Randles–Sevcik 기울기 **k = 2.1(CuSNC) vs 1.1(NC)** → "faster Li ion diffusivity".
  `[해석]` Randles–Sevcik 은 **반무한 확산·가역계**를 가정한다. 전고체 복합양극에 쓰면
  D 의 절대값은 의미가 없고, 기울기 비 ≈1.9 가 σ_Li 비 1.83 과 같은 크기라는 정도만 남는다.
- GITT (Fig. S11): OCP(준평형)는 두 시료가 **비슷**, CCP(비평형)만 크게 갈린다 →
  `[해석]` **열역학이 아니라 저항의 차이**라는 저자들 자신의 증거다. §7.2 의 Tafel 해석과 맞는다.

`[해석]` **이 절이 이 논문의 논리적 중심이다.** "전자 전도도를 200배 잃고도 성능이 좋아졌다"
는 관측은 두 가지로 읽을 수 있다: (a) 저자들의 독법 — 계면 화학(흡착·촉매)과 Li⁺ 경로가
전자 전도도보다 중요하다; (b) 대안 독법 — **NC/Li2S 의 5.7×10⁻² S cm⁻¹ 는 복합양극으로는
지나치게 높아서 SE 를 산화시킨다**(Fig. 3d 의 "Electrolyte decomposition" 이 그 증거),
즉 NC 는 "전자 전도도가 너무 높아 실패한" 대조군일 수 있다. 논문은 (b)를 한 문장으로
암시만 하고 재지 않았다(G15). **어느 쪽이든, 복합양극의 σ_e 는 클수록 좋은 것이 아니라
창(window)이 있다는 가설**이 이 논문에서 나온다.

---

## 10. p.6–8 — 사이클 성능 (Fig. 6) ★ 양단위 전수표

`[인쇄]` 셀 구성: **Li5.5PS4.5Cl1.5 전해질 · Li–In 합금 음극 · NC/Li2S 또는 CuS-NC/Li2S 양극.**
아래 모든 mAh g⁻¹ 은 `[재현]`(면적용량 ÷ Li2S 로딩), (S) 는 ×1.4329.

### 10.1 2 mg cm⁻², 0.3 mA cm⁻², RT, 100 사이클 (Fig. 6a)

| 시료 | 시점 | mAh cm⁻² | `[재현]` (Li2S) | `[재현]` (S) | 비고 |
|---|---|---|---|---|---|
| **CuSNC** | 1st | **1.6** `[인쇄]` | 800 | 1146 | |
| | 중간 최대 | **1.8** `[인쇄]` | 900 | 1290 | `[도표]` ≈10–15 사이클 |
| | 100th | **1.5** `[인쇄]` | 750 | 1075 | **CE 99.5 %** `[인쇄]` |
| | 유지율 | **93.8 %** `[인쇄]` (1st 기준) / **83 %** `[재현]` (최대 기준) | | | G7 |
| NC | 1st | **0.5** `[인쇄, 단위 오기 G13]` | 250 | 358 | |
| | 안정 | **0.3** `[인쇄]` | 150 | 215 | 유지 **60 %** `[인쇄]` |

`[도표, Fig. 6a]` CE 는 두 시료 모두 첫 몇 사이클(≈105 %)을 빼면 100 % 언저리에서
평평하다. CuSNC 곡선에 25번째 사이클 급강하(일시적)가 있다.

### 10.2 2 mg cm⁻², **1 mA cm⁻²**, RT, 500 사이클 (Fig. 6b)

| 시료 | 시점 | mAh cm⁻² | `[재현]` (Li2S) | `[재현]` (S) |
|---|---|---|---|---|
| **CuSNC** | 1st | **1.1** `[인쇄]` | 550 | 788 |
| | 최대 | **1.3** `[인쇄]` | 650 | 931 |
| | 500th | **≈0.85** `[도표, Fig. 6b·Fig. 7]` | 425 | 609 |
| | 유지율 | **77 %** `[인쇄]` (1st 기준) / **65 %** `[재현]` (최대 기준) | | |
| | 감쇠율 | **0.05 % / 사이클** `[인쇄]` → `[재현]` 500 × 0.05 = 25 % 손실 = 75 % 유지 (1st 기준과 정합) | | |
| NC | 전 구간 | **≈0.1** `[도표]` | 50 | 72 |
| | 사이클 수 | `[도표]` **≈400 에서 데이터가 끊긴다** (500 까지 가지 않았다) | | |

### 10.3 율속 (Fig. 6c, 2 mg cm⁻²) `[도표]` (+ `[인쇄]` 표시분)

| 전류밀도 | CuSNC mAh cm⁻² | `[재현]` (Li2S) | NC mAh cm⁻² | `[재현]` (Li2S) |
|---|---|---|---|---|
| 0.1 | **2.2** `[인쇄]` | 1100 | ≈1.2 | 600 |
| 0.2 | ≈1.95 | 975 | ≈0.73 | 365 |
| 0.5 | ≈1.55 | 775 | ≈0.52 | 260 |
| 1 | ≈0.87 | 435 | ≈0.28 | 140 |
| 2 | ≈0.40 | 200 | ≈0.12 | 60 |
| 0.1 복귀 | **2.35** `[인쇄]` (= 이론의 **88 %** `[인쇄]`) | 1175 | ≈1.0 | 500 |

`[인쇄]` "threefold higher at the highest rate" · "indicating good reversibility and stability".
`[재현]` 88 % 의 분모는 **2.66**(CuS 포함) 이다 (2.35/2.66 = 88.3 %) — G7 의 분모 문제와 달리
여기서는 CuS 포함 이론값을 쓰는 것이 일관된다.

### 10.4 고로딩 첫 사이클 (본문 §, Fig. S21 미확보)

| 로딩 (Li2S) | 첫 충전 | `[재현]` (Li2S) | 이용률 `[인쇄]` | 첫 방전 | `[재현]` (Li2S) | `[인쇄]` 이론 대비 | `[재현]` 첫 CE |
|---|---|---|---|---|---|---|---|
| 2 mg cm⁻² | 2.1 | 1050 | 91 % | 2.3 | 1150 | (2.3/2.66 = 86 %) | **110 %** |
| **4 mg cm⁻²** | **3.9** | 975 | **85 %** | **4.4** | 1100 | **83 %** | **113 %** |
| **10 mg cm⁻²** | **8.6** | 860 | **75 %** | **9.6** | 960 | **72 %** | **112 %** |

`[재현]` 이용률 검산: 3.9 / (4 × 1.166) = **83.6 %** (논문 85 %) · 8.6 / (10 × 1.166) =
**73.8 %** (논문 75 %) — **±1.5 %p 안에서 맞는다.** 방전 쪽 "83 % / 72 %" 는
**CuS 포함 이론값**(4 mg → 5.32, 10 mg → 13.3 `[재현]`)으로 계산해야 재현된다.
→ `[해석]` **충전 이용률은 Li2S 기준, 방전 이용률은 CuS 포함 기준**으로 분모가 바뀐다.
논문은 그 전환을 명시하지 않는다.

**로딩이 오르면 이용률이 떨어진다: 91 → 85 → 75 %.** `[해석]` 우리가 고로딩을 볼 때
기대해야 할 기울기다.

### 10.5 고로딩 사이클 (Fig. 6d,e,f)

| 조건 | 1st | 최대 | 끝 | `[재현]` 최대 (Li2S) | `[인쇄]` 유지 | `[재현]` 최대 대비 |
|---|---|---|---|---|---|---|
| **4 mg, 0.3 mA cm⁻², RT, 80 cyc** (6d) | **3.5** | **4.0 (11th)** | **≈2.3** `[도표]` | 1000 | "relatively stable" `[인쇄]` | **58 %** — G10 |
| **10 mg, 0.3 mA cm⁻², RT, 30 cyc** (6e) | **6.7** | **9.0 (11th)** | **≈6.2** `[도표]` | 900 | **92 %** `[인쇄]` (1st 기준 `[재현]` 93 %) | **69 %** |
| **4 mg, 0.3 mA cm⁻², 60 °C, 130 cyc** (6f) | ≈5.0 `[도표]` | **5.8** `[인쇄]` | **≈4.4** `[도표, Fig. 7]` | **1450 → 이론 초과(G8)** | **85 %** `[인쇄]` | **76 %** |
| NC, 4 mg, 60 °C (Fig. S23 미확보) | — | **3.2** `[인쇄]` | — | 800 | **60 %** `[인쇄]` | — |

`[도표, Fig. 6d]` 4 mg 상온 셀의 실제 궤적: 3.5 → 4.0(11th) → 3.5(45th) → **1.6(≈55th)** →
2.5(65th) → **2.3(80th)**. **중간에 한 번 반쯤 죽었다가 부분 회복한다.** CE 는 그 구간에서
94–109 % 사이로 요동한다.
`[도표, Fig. 6e]` 10 mg 셀은 29번째 사이클에서 CE 가 **≈85 %** 로 한 번 떨어진다.
`[도표, Fig. 6f]` 60 °C 셀만 유일하게 매끈하다 (CE 100 % 평평, 단조 감소).

`[인쇄]` 60 °C 첫 충전에 "**a small plateau (1.9 V–2.06 V) … owing to some limited argyrodite
oxidation** (Figure S22a)" 가 있었고 "**disappeared after the 10th cycle** (Figure S22b)" 이며
"did not adversely affect the cycle performance".
`[해석]` **G8 과 합치면 이 문장은 스스로를 반박한다** — 60 °C 셀의 최대 용량이 Li2S 이론의
124 % 인데, 같은 셀의 첫 충전에 SE 산화 plateau 가 있었다고 적혀 있다. 초과 용량의 가장
그럴듯한 출처가 바로 그 SE 분해다. "적어도 용량 수치로는 유리하게 작용했다" 고 읽어야 한다.

### 10.6 임피던스 `[인쇄, Fig. S20 미확보]`

"fairly small changes in the impedance of the CuS-NC/Li2S cell over 50 cycles suggest
suitable solid electrolyte stability." → `[해석]` **정성 서술만 있고 숫자가 없다.**
NC 셀의 임피던스 변화(있었다면 SE 산화의 직접 증거)는 언급되지 않는다.

---

## 11. p.8 — 문헌 비교 (Fig. 7) 와 결론

`[도표, Fig. 7]` 가로축 사이클 수, 세로축 "Areal capacity after cycles (mAh cm⁻²)".
**This work(빨간 별) 5점**: ≈(30, 6.2) · (80, 2.2) · (100, 1.5) · (130, 4.4) · (500, 0.85).
문헌 13점(refs 30, 32–34, 46–54)은 전부 **사이클 ≤160, 면적용량 ≤1.8 mAh cm⁻²** 영역에 모여 있다.

`[해석]` 이 그림은 **§10 의 표를 역산하는 데 쓸 수 있는 가장 좋은 도구**였다 — (500, 0.85)와
(130, 4.4)가 Fig. 6b·6f 의 끝값 판독을 확증해 주고, 그래서 G7(유지율 분모)이 성립한다.
동시에 이 그림 자체는 **로딩·온도·전류밀도가 다 섞인 2축 비교**라 공정하지 않다
(본문도 "at different current densities, mass loadings, and temperatures" 라고 적는다).

**결론 절 `[인쇄]` 의 명제**:
- DFT: CuS 가 NC 대비 (i) 더 나은 Li2S 흡착, (ii) 더 낮은 Li2S 분해 장벽, (iii) 더 낮은 Li⁺
  이동 장벽 → "promote sulfur conversion chemistry **in a manner akin to electrocatalysis**".
- **시너지 주장**: "While DFT confirmed that **CuS alone can catalyze** the oxidation of Li2S,
  there is effective synergy with the N-doped carbon host, because supporting the CuS
  nanocrystallites **greatly increases the surface area of the CuS**, and provides more
  accessible catalytic sites." → `[해석]` **표면적을 재지 않았다** (BET 값이 본문에 없다).
  "시너지" 는 측정이 아니라 서사다 (G20).
- 마지막 문장 `[인쇄]`: "Developing **mixed conducting hosts with higher ion AND electronic
  conductivity** that preserve the catalytic properties … will help to **increase the fraction
  of Li2S in the cathode composite**, and is the subject of our ongoing studies."
  → `[해석]` **저자들 스스로 두 가지를 한계로 인정한다**: (i) 이 호스트는 혼합전도체가 아니다,
  (ii) **양극 내 Li2S 분율이 낮다**(G2 의 "호스트가 활물질만큼 무겁다" 와 정확히 일치).
  이 문장은 Huang 2026 의 "혼합 이온–전자 전도체" 와 정면으로 이어진다 (§13).

---

## 12. SI 대조 — **미확보**. 본문이 인용하는 SI 항목 색인

이번 수집에서 SI 를 받지 못했으므로 **아래는 본문이 인용한 위치만 남긴 목록**이다.
값을 채우지 않았다. 나중에 SI 를 구하면 이 목록대로 §4–§10 을 보강할 수 있다.

| SI 항목 | 본문이 무엇에 인용했나 | 왜 필요한가 |
|---|---|---|
| **Methods (전문)** | "see Methods for details" ×2, XRD 세척 절차 | **G1·G2·G4 전부 여기에 있다.** 최우선 |
| Fig. S1 | HAADF-STEM/EDS 보강 | CuS 분산 |
| **Fig. S2** | TGA(O2) → **CuS 29 wt%** 산출 | G17 — 조성 추정의 뿌리 |
| Figs. S3–S5 | **NC 대조군**의 형태·원소분포·**N 1s XPS**(pyrrolic 우세 근거) | 대조군이 정말 "Cu 뺀 동일물" 인지 |
| **Figs. S6, S7** | **전자 전도도 측정** (≈200배 차이) | G14 — 시료 정체·측정 구성 |
| Fig. S8 | pyridinic·graphitic N 위 Li2S 흡착 | N 종류별 기여 |
| Fig. S9 | 차분전하밀도 (0.8 vs 1.1 "eV") | G19 단위 오기 |
| Fig. S10 | Li2S 산화 NEB 상세 | G18 |
| **Fig. S11** | **GITT** (OCP vs CCP) | 열역학 vs 저항 분리의 원데이터 |
| Fig. S12 | Cu K-edge **XANES** (방전 시료) | Cu 원자가 |
| Fig. S13 | 2차 충전 후 Cu 2p → CuS 재생 | 가역성 |
| **Figs. S14, S15** | **DC 분극 전자차단 대칭셀** | 우리가 이식하려는 측정 그 자체 |
| Figs. S16–S18 | 스캔속도별 CV · b 값 · Randles–Sevcik | 확산 논증 |
| Fig. S19 | Li⁺ 이동 NEB | 1.5 eV 의 타당성 |
| **Fig. S20** | 50 사이클 Nyquist | SE 안정성의 유일한 정량 근거 |
| **Fig. S21** | 고로딩(4·10 mg) 첫 충·방전 곡선 | 활성화 plateau 모양 |
| **Fig. S22a,b** | 60 °C 첫 충전 **1.9–2.06 V argyrodite 산화 plateau**, 10 사이클 후 소멸 | G8 |
| Fig. S23 | **NC/Li2S 60 °C** (3.2 mAh cm⁻², 60 % 유지) | 고온 대조군 |
| **Table S1** | 선행 전고체 Li2S 문헌 비교 (Fig. 7 의 원표) | 우리 기준선 표로 쓸 수 있었을 것 |

---

## 13. ★ Huang 2026 과의 대조 — 호스트인가 첨가제인가

두 논문은 **같은 문제**(고체 복합양극의 느린 산화환원을 소량의 기능성 황화물로 고친다)를
다루고 **결론의 방향이 정반대**다. 나란히 놓는 것이 이 digest 의 핵심 산출물 중 하나다.
(상대: `raw/papers/huang2026_high-entropy-sulfides-kinetic-accelerators-assb.md`)

| 축 | **Yu 2024 (이 논문)** | **Huang 2026 (HES)** |
|---|---|---|
| 활물질 | **Li2S** (방전 상태 출발) | **S8** (충전 상태 출발) |
| 개입 층위 | **호스트** — Li2S 를 담는 탄소 골격 자체를 바꿈 | **첨가제** — 기존 S/KB/LPSCl 에 **추가** |
| 기능상 함량 | CuS **29 wt% of 호스트**, `[재현]` 양극에서 CuS ≈0.6–1.2 mg cm⁻² (Li2S 의 30–60 wt%) | HES **최종 양극의 6 wt%** |
| 탄소 | N-도핑 다공성 탄소(호스트 자체), 별도 도전재 **미기재**(G16 의 CNT 흔적) | **KB 12 wt% 를 그대로 두고** HES 를 더함 |
| SE | **Li5.5PS4.5Cl1.5** (Cl-rich argyrodite) | LPSCl |
| 음극 | **Li–In** | Li–In |
| **σ_e⁻ 방향** | **200배 ↓** (5.7×10⁻² → 2.9×10⁻⁴ S cm⁻¹) | **14배 ↑** (1.71 → 23.80 mS cm⁻¹) |
| **σ_Li⁺ 방향** | **1.8배 ↑** (3.5 → 6.4 ×10⁻⁵ S cm⁻¹) | **270배 ↑** (2.41×10⁻⁵ → 6.50×10⁻³ mS cm⁻¹) |
| 주장하는 기전 | **흡착 + 전기촉매 + 표면 Li⁺ 이동** (DFT 중심) | **혼합 이온–전자 전도체로 삼상 계면 재구성** (전도도 중심) |
| DFT NEB | Li2S 분해 0.9 → **0.4 eV**; Li⁺ 이동 1.5 → **0.3 eV** | Li⁺ 확산 0.25 → **0.20 eV** |
| 대조군 | **NC (CuS 뺀 호스트)** — 첨가제 없음 조건 아님 | **0 wt% HES** — 진짜 "없음" 대조 |
| 이용률 개선 | 첫 충전 **51 → 91 %**(Li2S 기준) | 첫 방전 **39 → 76 %**(S 기준) |
| 사이클 | 500 (1 mA cm⁻², 2 mg) · 130 (60 °C, 4 mg) | (0 wt% 사이클 데이터 없음) |
| 면적용량 최대 | **9.6 mAh cm⁻²** (10 mg Li2S) | ≈2.05 mAh cm⁻² |
| 압력 기재 | **없음**(G4) | 양극 450 MPa `[인쇄]` |

`[해석]` 여기서 나오는 것이 **우리에게 가장 값진 한 줄**이다.

> **두 논문은 "복합양극에 금속황화물을 넣으면 좋아진다" 는 같은 결론에 이르렀지만,
> 전자 전도도를 서로 반대 방향으로 움직였다.** Huang 은 σ_e 를 14배 올려서, Yu 는
> 200배 내려서 같은 종류의 개선(이용률 ≈2배)을 얻었다. 그러므로 **개선의 공통 원인은
> σ_e 가 아니다.** 두 논문이 같은 방향으로 움직인 유일한 양은 **σ_Li⁺**(1.8배 ↑ / 270배 ↑)와
> **활물질–황화물 계면의 화학적 친화**다.

`[해석]` 단, 두 논문의 σ_Li 절대값 스케일이 다르다 — Yu 2024 의 6.4×10⁻⁵ S cm⁻¹ 는
Huang 2026 의 S-HES 값 6.5×10⁻⁶ S cm⁻¹ 보다 **10배 높고**, 두 측정 모두 **시료 정체가
불명확하다**(Yu G14 · Huang G6). **절대값 비교는 하면 안 되고, 각 논문 내부의 비(ratio)만
비교해야 한다.**

`[해석]` 계보도 이어진다: Huang 2026 의 DC 분극 측정 출처가 **Kwok, …, Nazar, *EES* 16
(2023) 610** 이고, 그 Kwok 이 이 논문의 공저자이며 같은 논문이 여기 ref 18 로 인용된다.
**즉 우리가 이식하려는 DC 분극 절차는 Nazar 그룹 → Huang 그룹으로 퍼진 하나의 방법이다.**

---

## 14. Zhang 2026 · Kim 2023 과의 대조 — pristine Li2S 기준선

(상대: `raw/papers/zhang2026_anode-free-assb-nanocrystalline-amorphous-li2s-na-collector.md`,
`raw/papers/kim2023_reinforced-electrical-networking-high-loading-li2s-cathode.md`)

| 축 | **Yu 2024** | **Zhang 2026** | **Kim 2023** |
|---|---|---|---|
| 계 | ASSB, Li5.5PS4.5Cl1.5 | ASSB, LPSCBr | **액체** 에테르 |
| Li2S 상태 | **nano-Li2S + CuS-NC 호스트** | 상용 Li2S + PI3 볼밀 (나노결정–비정질) | 상용 micro Li2S 1–5 µm |
| 음극 | Li–In | **anode-free (Na 집전체)** | Li 금속 / 흑연 |
| 첫 방전 | **1150 mAh g⁻¹(Li2S)** `[재현]` (2 mg, 0.1 mA cm⁻²; CuS 몫 ≈10 % 포함) | **971 mAh g⁻¹(Li2S)** `[인쇄]` (0.05 C) | 800 mAh g⁻¹(Li2S) `[재현]` |
| **같은 계의 대조군** | **NC/Li2S 650 mAh g⁻¹(Li2S)** — pristine 아님 | **pristine Li2S ≈270 mAh g⁻¹(Li2S)** `[도표]` | — |
| 수치 오염 의심 | CuS 환원 ≈10 % (G6), 60 °C 이론 초과(G8) | LiI 산화 기여 가능 (그쪽 G6) | — |
| 혼합 조건 | **전무**(G1) | 1400 rpm 유효 2 h 3D 스윙밀 `[인쇄]` | "ball milling" 만 |
| 압력 | **전무**(G4) | 성형 400 MPa / 운전 1–4 MPa `[인쇄]` | 1 GPa 성형 `[인쇄]` |

`[해석]` **세 논문을 겹치면 Li2S 계의 대략적인 사다리가 보인다** (전부 Li2S 기준,
서로 다른 셀이므로 **경향만**):

| 단계 | 첫 방전 mAh g⁻¹(Li2S) | 출처 |
|---|---|---|
| pristine 상용 Li2S + CNT + LPSCBr | **≈270** | Zhang 2026 `[도표]` |
| N-도핑 탄소 호스트 + nano-Li2S (NC/Li2S) | **650** | Yu 2024 `[재현]` |
| 반응형 나노결정–비정질 Li2S + PI3 | **971** | Zhang 2026 `[인쇄]` |
| **CuS/N-도핑 탄소 호스트 + nano-Li2S** | **1035–1150** | Yu 2024 `[재현]` |

`[해석]` 우리 목표 **500–600 mAh g⁻¹** 는 이 사다리의 **두 번째 칸 근처**다. 즉
**"pristine 상용 Li2S 를 그냥 AB 와 섞어서" 도달하기 어려운 값**이라는 것이 세 논문의
일관된 그림이다 — 최소한 **nano-Li2S(입자) 또는 기능성 호스트(계면) 중 하나**는 있어야 한다.
이것이 [[reference-cell-500-600-mahg]] 의 **H1·H3 에 대한 추가 근거**다.

---

## 15. 우리 연구와의 접점

| 이 논문 | 우리 ([[li2s-assb-reference-cell]] / [[anode-free-li2s-assb]]) | 옮겨 올 수 있는 것 | 옮겨 올 수 없는 것 |
|---|---|---|---|
| **같은 SE 계열(Cl-rich argyrodite) + 같은 음극(Li–In) + 상온 + 펠릿** | LPSCl + Li–In + 상온 | **셀 계가 거의 같다 — 전압창(0.8–2.5 V vs Li–In)과 전류밀도(0.1–1 mA cm⁻²)를 기준선으로 쓸 수 있다** | 압력·면적·SE 두께 전부 미기재(G4) |
| **첫 충전 이용률 51 % vs 91 %** (같은 로딩·전류에서 호스트만 바꿈) | 첫 충전 활성화가 병목인지 | **★ 고체계에서 "호스트가 활성화량을 2배 가른다" 는 직접 근거** ([[li2s-activation-first-charge]]) | pristine Li2S 대조가 없다(G5) — 우리 출발점과의 차이를 못 잰다 |
| **활성화 전위 ≈2.0–2.1 V vs Li–In, 컷오프 2.5 V** | 우리 컷오프 설계 | **컷오프를 2.5 V vs Li–In 로 잡아도 91 % 활성화가 가능하다는 실증** | vs Li/Li⁺ 환산은 못 한다(G3) |
| **σ_e 를 200배 낮추고도 성능이 좋아졌다** | AB 20 wt% (전자망 중심 설계) | **가설로: 복합양극 σ_e 에는 상한이 있다** (너무 높으면 SE 산화) — Fig. 3d 의 NC 쪽 "Electrolyte decomposition" | **검증 안 됨**(G15). 우리 설계를 바꿀 근거는 아직 아니다 |
| **DC 분극 전자차단 셀로 σ_Li⁺ 측정** (±100/50/25 mV, 1 h) | 우리 펠릿의 σ_e/σ_Li 를 따로 재는 일 | **◎ Huang 2026 과 같은 절차. 두 논문이 같은 출처(Kwok 2023)를 쓰므로 이식 근거가 두 겹이 됐다** | 시료 정체 불명(G14) — 우리는 **SE 포함/미포함을 반드시 명시**해야 한다 |
| **CuS 가 방전에 용량의 ≈10 % 를 보탠다 → 첫 CE 110–113 %** | anode-free 2단계 | **★ 경고로: 전이금속황화물 첨가제는 음극에서 Li 을 빌린다.** anode-free 에서는 그만큼 Li 재고 손실 | 이 논문은 anode-free 를 하지 않았다 |
| **로딩 ↑ → 이용률 91 → 85 → 75 %** (2 → 4 → 10 mg cm⁻²) | 고로딩 계획 | **기울기 자체** (2.5배 로딩에 ≈8 %p 손실) | 조성·압력을 모르므로 절대값은 못 쓴다 |
| **N-도핑 탄소 호스트 + 나노 금속황화물** | AB 단일 탄소 | **탄소를 "도전재" 가 아니라 "호스트" 로 보는 설계 축** ([[carbon-dimensionality-electron-network]] 의 확장) | 호스트 무게 대가가 크다 — `[재현]` 활물질만큼 무겁다(G2) |
| **60 °C 결과** | — | (없음) | **쓰면 안 된다** — 이론용량 초과(G8) + SE 산화 plateau 자인 |

### 가장 값싼 다음 실험 `[해석]`

1. **DC 분극 2종을 우리 30:50:20 펠릿에 건다** (전자차단 · 이온차단). Yu 2024 와
   Huang 2026 이 같은 절차를 쓰므로 우리 σ_e/σ_Li 를 두 논문 좌표계에 동시에 놓을 수 있다.
   **셀 조립 없이** [[reference-cell-500-600-mahg]] 의 H2 를 가를 수 있는 유일한 측정이다.
2. **첫 충전 이용률을 명시적으로 계산해 기록한다** — 이 논문처럼 `첫 충전 mAh cm⁻² ÷
   (로딩 × 1.166)` 로. 우리 값이 51 %(NC 급)인지 91 %(CuSNC 급)인지가 H1 의 답이다.
3. **첫 사이클 CE 를 본다.** 100 % 를 넘으면 양극에 Li 을 받아먹는 상이 있다는 뜻이고,
   anode-free 로 갈 때 그대로 재고 손실이 된다 (이 논문 110–113 %).

---

## 16. 비판 (이 digest 의 판단)

1. **"stable performance" 가 무엇의 안정인지 흔들린다.** CE 는 실제로 100 % 근처에서 평평하다
   (Fig. 6a,f). 그러나 **용량은 안정하지 않다** — 4 mg 상온 셀은 최대 대비 58 % 로 끝났고
   (그런데 본문은 "relatively stable over 80 cycles" 라 적는다, G10), 500 사이클 셀은 최대
   대비 65 % 다. **초록의 "maintains stable performance over 500 cycles" 는 CE + 완만한
   기울기를 말한 것으로 읽어야 한다.**
2. **유지율의 분모와 대표값의 분모가 다르다** (G7). 대표 용량은 **중간 최대값**에서,
   유지율은 **첫 사이클**에서 딴다. 두 수치를 한 문장에 넣으면(초록이 그렇게 한다)
   실제보다 좋아 보인다. Fig. 7 의 끝점 5개가 이 판정의 근거다.
3. **60 °C 데이터는 용량 근거로 성립하지 않는다** (G8). 5.8 mAh cm⁻² = Li2S 이론의 124 %.
   같은 문단에 SE 산화 plateau 를 자인해 놓고 초과 용량을 언급하지 않은 것은 심각한 누락이다.
4. **원인 분리가 없다** (G5·G15·G20). 바뀐 변수는 최소 넷이다 — CuS 유무 · 전자 전도도
   200배 · 호스트 내 탄소 함량 · (아마) 비표면적. 그런데 개선의 원인은 "촉매 + Li⁺ 수송"
   두 가지로 **선언**된다. **pristine Li2S 대조도, 도핑 없는 탄소 대조도, CuS 단독 대조도 없다.**
5. **DFT 가 실험보다 앞서 있다** (G18). 0.4 vs 0.9 eV, 0.3 vs 1.5 eV 는 진공 슬랩 위
   고립 Li2S 의 첫 Li 탈리다. 그 1.5 eV 가 맞다면 NC 셀은 작동하지 않아야 한다.
   **계산 조건조차 본문에 없다.**
6. **Tafel 278·356 mV dec⁻¹ 는 전하이동 영역이 아니다** (§7.2). 저항 지배 구간의 기울기를
   "electrode kinetics" 로 부른 것이다 — 저자 자신의 GITT(OCP 는 같고 CCP 만 다르다)가
   그 독법을 지지한다. 즉 **"촉매" 보다 "저항" 이 더 정확한 단어**일 수 있다.
7. **방법이 본문에 없다** (G1). 이 위키가 논문에서 가장 필요로 하는 것(혼합 조건·압력·조성비)이
   전부 SI 로 밀려 있고, 본문만으로는 **아무도 이 셀을 재현할 수 없다.**
8. **셀 개수 0 명시, 오차 막대 없음** (G9). Fig. 6d 의 중간 급락이 계통인지 사고인지 모른다.
9. **교정 오류가 최소 셋** (G11 방향 반전 · G12 초록/서론 불일치 · G13 단위 오기).
10. 좋은 점도 분명하다: (i) **XRD·XPS·XANES 가 같은 결론(CuS ↔ Cu₂₋ₓS, Cu 금속 아님)으로
    수렴**하고, **2차 충전 후 CuS 재생**까지 확인해 가역성을 닫았다. (ii) **CuS 의 용량 기여를
    숨기지 않고 캡션에 명시**했다 (추정치이지만 적어도 표시했다) — 이 분야에서 드문 정직이다.
    (iii) **"전자 전도도가 200배 낮은데도 빠르다" 는 불편한 사실을 논문의 축으로 삼았다** —
    보통은 숨긴다. (iv) 결론에서 **자기 호스트가 혼합전도체가 아니고 Li2S 분율이 낮다는 한계를
    스스로 적었다.**

---

## 17. 이 저장소가 가져갈 것

- **질문 카드 라우팅** — [[reference-cell-500-600-mahg]]:
  - **H1(활성화 제한) 지지 (고체계·같은 음극·같은 SE 계열)**: 같은 로딩(2 mg cm⁻²)·같은
    전류(0.1 mA cm⁻²)에서 **호스트만 바꿔 첫 충전 Li2S 이용률 51 % → 91 %**
    (1.2 → 2.1 mAh cm⁻², `[인쇄]`). 그리고 첫 충전 용량이 큰 쪽이 10번째 사이클 용량도
    2.9배 크다 (0.6 → 1.75 mAh cm⁻²). **단서**: pristine Li2S 대조가 없고(G5), 혼합·압력
    조건이 전무하며(G1·G4), 방전 값에는 CuS 몫 ≈10 % 가 섞여 있다(G6).
  - **H2(퍼콜레이션 제한)에 대한 *반대 방향* 근거**: **전자 전도도를 200배 낮추고도**
    이용률이 올라갔다 (σ_e 5.7×10⁻² → 2.9×10⁻⁴ S cm⁻¹). Huang 2026 은 σ_e 를 14배
    **올려서** 같은 크기의 개선을 얻었다. **→ 두 논문을 합치면 "σ_e 가 클수록 좋다" 는
    단순 가설은 기각된다.** 공통으로 움직인 것은 σ_Li⁺ 와 계면 친화다.
  - **H3(입자 제한) 보강**: 이 논문은 처음부터 **nano-Li2S** 를 썼고 그것조차 호스트 없이는
    (NC) 51 % 에 그쳤다 → **나노화만으로는 부족하다**는 근거.
  - **H4(단위 착시) 보강**: 이 논문은 **비용량을 아예 쓰지 않고 면적용량만 쓴다.**
    같은 논문 안에서 **충전 이용률은 Li2S 기준, 방전 이용률은 CuS 포함 기준**으로 분모가
    바뀐다(§10.4). 분모 명시 규율의 좋은 반면교사.
- **개념 갱신 후보**:
  - [[li2s-activation-first-charge]] ← **고체계 첫 충전 plateau 두 종류**(완만한 2.0–2.1 V
    plateau vs 즉시 컷오프로 치솟는 곡선)와 이용률 51/91 %, 활성화 CV 피크 2.14/2.41 V vs Li–In.
  - [[carbon-dimensionality-electron-network]] ← **"호스트" 축의 확장**: 탄소의 세 번째 역할
    (활물질을 담고 계면 화학을 제공) + **σ_e 상한 가설**.
  - [[li2s-assb-composite-cathode]] ← 복합양극 σ_e/σ_Li 를 따로 재는 DC 분극 절차 (Kwok 2023
    계보, Huang 2026 과 동일).
  - [[capacity-normalization-li2s-vs-sulfur]] ← **분모가 도중에 바뀌는 사례**(§10.4)와
    **면적용량만 보고하는 논문의 환산 절차**.
- **새 개념 후보 `[해석]`**: **"전이금속황화물 첨가제의 Li 재고 비용"** — CuS·Co9S8·VS2 류는
  방전에서 Li 을 소비한다. Li–In 반쪽셀에서는 공짜(첫 CE >100 %)지만 **anode-free 에서는
  순손실**이다. [[anode-free-li2s-assb]] 에 경고로 붙일 자리.
- **[[one-step-vs-two-step-mixing]]**: 이 논문은 **호스트를 먼저 만들고 Li2S 를 뒤에 섞는
  two-step 계열**이지만 **혼합 조건이 전무**해서 카드에 줄 수 있는 것은 "또 하나의 미기재
  사례" 뿐이다 (Kim 2023 G1 과 같은 공백의 반복).

---

## 18. 그림 판독 기록 (무엇을 보고 무엇을 안 봤는가)

| 그림 | 봤는가 | 어디에 썼는가 |
|---|---|---|
| Fig. 1 (a–h) | ✓ | §3.1(합성 흐름도 — 800 °C·N2/H2·동결건조 −50 °C 는 **그림에서만** 나온다) · §4 |
| Fig. 2 (a–i) | ✓ | §5.1–5.3(활성화), §6(DFT). **가장 오래 봤다** |
| Fig. 3 (a–d) | ✓ | §7 전체 (전압창·컷오프·"Electrolyte decomposition" 주석) |
| Fig. 4 (a,b) | ✓ | §8. **참조 패턴 줄의 "CNT" 를 발견한 곳**(G16) |
| Fig. 5 (a–e) | ✓ | §9(DC 분극 계단 조건), §6(Li⁺ NEB) |
| Fig. 6 (a–f) | ✓ | §10 전수표. **본문 서술과 어긋나는 6d 를 여기서 찾았다**(G10) |
| Fig. 7 | ✓ | §11. **6b·6f 의 끝값(0.85 / 4.4 mAh cm⁻²)을 확증**해 G7·G8 의 근거가 됐다 |
| **Fig. S1–S23 · Table S1** | **✗ SI 미확보** | 크로핑도 없다. 목록만 §12 에 남겼다 |

**본문 서술과 어긋난 그림**: Fig. 6d (G10 — "relatively stable" 서술 vs 최대 대비 58 %).
**본문 안에서 서로 어긋난 수치**: G11(방향 반전 문장) · G12(초록 1.8/94 % vs 서론 1.3/91.9 %) ·
G13(mAh g⁻¹ 단위 오기) · G8(60 °C 이론 초과, 논문은 무언급).
**그림에서만 읽어 `[도표]` 로 표시한 것**: 전압창·컷오프(2.5 / 0.8 V vs Li–In) · 사이클 끝값
(0.85 / 2.3 / 6.2 / 4.4 mAh cm⁻²) · 율속 중간점 · DC 분극 계단 크기·시간 · Fig. 1a 의 합성 조건 ·
CV 피크 전류 · Fig. 2i/5c,d 의 곡선 최댓값.

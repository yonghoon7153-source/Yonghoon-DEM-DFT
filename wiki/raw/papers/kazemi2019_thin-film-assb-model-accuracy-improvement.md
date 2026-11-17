---
title: "Kazemi N., Danilov D.L., Haverkate L., Dudney N.J., Unnikrishnan S., Notten P.H.L. 2019 — Modeling of all-solid-state thin-film Li-ion batteries: Accuracy improvement (Solid State Ionics 334, 111–116)"
source_url: local-upload/110._Modeling_of_all-solid-state_thin-film_Li-ion_batteries_Accuracy_improvement.pdf
source_url_note: "본문 PDF 6 쪽(인쇄 111–116 · PageLabels 111 부터 · 그림 6 — 전부 래스터 JPEG ≈300 dpi · 표 2 · 번호 식 (1)–(14) · 참고문헌 [1]–[22]) 1,591,722 B · 업로드 접두사 14f8f316 · 5차 묶음 #11 · 사용자 파일 110 · SI 없음(보충 언급 0 · EmbeddedFiles 이름 트리 빈 사전) · 원자료 · 코드 공개 0 · 모형 편 — 자기 실험 0 · 자료 = 문헌 두 묶음(DNN = 91호 Danilov 2011 자기 셀 곡선 · NDB = [22] Neudecker · Dudney · Bates 2000 곡선) · COMSOL Multiphysics 4.4"
source_doi: 10.1016/j.ssi.2019.02.003
source_license: "0167-2738/© 2019 Elsevier B.V. All rights reserved.(인쇄 p. 111 · XMP prism:copyright) · OA 표기 0 — 구독본으로 다룬다 — 이 digest 는 인용 · 요약 · 재현 계산만 담는다(그림 크롭은 위키 관례대로 raw/figures 에 — 변형 없는 잘라내기 · 200 dpi)"
pdf_sha256: 74fc79d83f00c40bf9636546a6ba728b172c668e2f4e86f24df1a78e49e48802
ingested: 2026-11-17
sha256: 6b22871496511d7904d8748ee1399d93c31f352b64aad7ce0ba7a4ce01468dd1
---
# 수집 목적

`assb` 섹션 **115호** — **5차 묶음 #11 · 사용자 파일 110**(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 L229 ★★★ · `ASSB_TRANSFER_NOTE.md` §6-3-k #11 — 5차 묶음 13 편 중 열한째 권고 순서). **모형 편 — Li \| LIPO(N) \| LiCoO₂ 평면 박막 1D 모형(91호 Danilov 2011 의 해리 SE 수송 + 양극 단일 Fick)에 양극 확산계수 D_Li(x) 를 '2상 공존 영역 경계(x 0.80 · 0.95)에서 기울기가 꺾이는 꺾은선' 으로 넣고, 문헌 자료 두 묶음(DNN = 91호 자기 셀 · NDB = [22] Neudecker · Dudney · Bates 2000)에 묶음마다 따로 맞춘 편 · 자기 실험 0 · COMSOL Multiphysics 4.4.**

Holst Centre/TNO(Eindhoven) + TU Eindhoven + Forschungszentrum Jülich(IEK-9) + Oak Ridge National Laboratory + University of Technology Sydney — **Namdar Kazemi**ᵃ · **Dmitri L. Danilov**ᵇ'ᶜ(교신 \*) · Lucas Haverkateᵃ · **Nancy J. Dudney**ᵈ(ORNL — NDB 자료 [22] 의 공저자) · Sandeep Unnikrishnanᵃ · **Peter H.L. Notten**ᵇ'ᶜ'ᵉ 의 *Solid State Ionics* 2019 편. `[인쇄]` 초록이 스스로 적는다: "This paper represents a simulation approach for TFSSB which overcome a major drawback of available mathematical models, i.e. decline in accuracy of the models at high current rates. A one-dimensional electrochemical model, including charge transfer kinetics on the electrolyte-electrode interface, diffusion and migration in electrolyte as well as diffusion in intercalation electrode has been developed and the simulation results are compared to experimental voltage-capacity measurements. A new definition of diffusion coefficient as a function of concentration, based on the experimental measurements, is used to improve the performance of the model. The simulation results fit the available experimental data at low and high discharge currents up to 5 mA cm−2. The models show that the cathode diffusion constant is a prime factor limiting the rate capability for TFSSB in particular for ultrafast charging applications."

이 편이 실제로 한 것은 **두 셀의 방전 곡선 세 율씩(DNN 32 · 128 · 512 µA cm⁻² = 이름표 3C · 13C · 51C · NDB 100 · 1000 · 5000 µA cm⁻² = 0.8C · 8C · 42C)에 같은 구조의 모형을 '거친 격자 최적화' 로 두 번 맞추고(표 2 의 DNN · NDB 두 열), NDB 에서 상수 D(1.3×10⁻¹⁴) · DNN 에서 가져온 D(x) · NDB 에 맞춘 D(x) 세 곡선을 겹쳐 본 것**이다. 열화 · 접촉 · 압력 · 온도 축 0 · 충전 모의 0.

들어온 경로: 원장 행(도착 표시 전 원문 요약) "★★★ … (98호 [18]) \| 98 · 100 · 104 \| 3 \| Q4·Q3 \| 26호 계보의 가운데 편 (91호 2011 → 이 편 2019 → 98호 2020) — … 농도 의존 D 를 처음 넣은 편의 매개변수 표 · 자료 (98호와 같은 상용 셀인가) · 적합 방법 — 26호 '문헌값' 의 바로 앞 단계 … · 100호 [8] 재지목 … · 104호 [26] 재지목 …". 지목 현황(원장 L229 · 2026-11-17): **98 · 100 · 104 = 3**. 위키 grep(`Kazemi` · `Haverkate` · `Unnikrishnan` · `334, 111` · `Accuracy improvement` · `ssi.2019.02.003`)으로 다시 셌다 — **후속 절에 오른 것은 98호 :683(★★★ [18]) · 100호 :568(★★★ [8]) · 104호 :561(★★ [26]) 셋 = 3 = 원장 일치** · 37호 :116(어휘 표 "Kazemi [13] adopt a strategy of calibrating the diffusion coefficient" — 서지 미전사) · 12호 :387(표 해체 "Mathematical model [65,72,78] … Kazemi 박막 정확도")은 후속 절 밖 · 105호 :561 은 5차 묶음 관계 문장(인용 0 확인)이라 셈 밖. `ssi.2019.02.003` 은 위키 0 회(DOI 가 이 digest 에서 처음 들어온다).

이 digest 의 일 (지시):

1. **(a) 지목 명제 판정** — 98호("extended with an ionic concentration-dependent diffusion coefficient … Their model simulations have been experimentally validated") · 100호("fit the diffusion coefficient as a function of lithium-ion concentration … high accuracy even at a current density of 5 mA/cm²" · "accuracy of COMSOL simulations has been verified [8]") · 104호("[26, 29] … Through this extension, there has been an improved accuracy … [26]") 를 원문과 대조 — 무엇을 확장했나 · '정확도 개선' 의 지표와 비교 대상.
2. **(b) 매개변수 표 출처 층위 · 26호 '문헌값' 계보** — 표 2 값마다 측정 / 문헌(91호) / 적합 / 유도 · 26호 "적합 변수 10 개 중 7 개가 문헌값 ×1.0500" · `D_e⁻` 10 자릿수 어긋남의 원전이 이 편인가.
3. **(c) 적합 방법 · 잔차 · 불확실성 · 식별성(Q4)** — 계보의 'sensitivity = sweep' 관행과 대조 · 인쇄 표로 저자 그림이 다시 나오는가(재풀이).
4. **(d) Q1 · Q3 · 그 밖 칸** — 박막이라 복합 전극 접촉 손실(θ)은 해당 없음일 가능성 — 그 이유.
5. **(e) 후속 후보.**

⚠ **표기 규약**: `[인쇄]` = 원문이 실제로 쓴 것 · `[도표]` = 그림을 눈으로 읽은 값(판독 폭 표시) · **`[도표·화소]`** = 그림이 전부 래스터 JPEG(1423 px 폭 = ≈300 dpi)라 PDF 에서 **원본 래스터를 꺼내 축 틀 · 눈금(또는 눈금 이름표) 화소로 선형 · 로그 보정**하고 선 색 화소로 읽은 값(그림마다 보정 근거를 적는다) · `[재현]` = 인쇄 수치 · 식으로 우리가 계산(스크립트는 `scratchpad/assb5/k115/` 에만 — 커밋 안 함) · `[재현·가정]` = 인쇄되지 않은 값 · 단순화를 가정해 계산(가정 명시) · `[재현·대수]` = 인쇄 식 위의 대수 · `[재현·외부 값]` = 원문 밖 상수(조밀 LiCoO₂ 5.05 g cm⁻³ · 97.87 g mol⁻¹ — 91 · 104호 digest 와 같은 외부값) · `[해석]` = 우리 판단. **`[데이터]` 표시 0** — 원자료 공개 0. **'0' 표기**('인쇄 0' · '비교 0' · '… 0 회' · '자기 실험 0' 등)는 **이 지면(본문 · 그림 · 표 · 참고문헌)에 인쇄되지 않았다 · 그 낱말이 나오지 않는다**는 뜻이다 — 저자가 하지 않았다거나 그런 자료 · 계산이 어디에도 없다는 주장이 아니다(114호 digest 의 규약과 같음).

⚠ **측정 · 인용 · 모형 · 적합 구분**: 이 편 안의 수치는 ① **측정 0** — 저자 실험 0(2절 "Experimental data used in this paper are represented by two datasets available in literature") ② **인용(문헌)** — DNN 곡선 · 셀 치수(91호 [7]) · NDB 곡선 · 셀 치수([22]) · 표 1 · 그림 2a 의 문헌 확산계수([12]–[17] · [19]) ③ **모형 입력 · 적합** — 표 2 두 열(각주 0 — 출처 층위는 우리 대조로만 · §(b)) ④ **모형 출력** — 그림 4 · 5 의 모의 곡선 · 그림 6 농도 · D 단면 ⑤ **EMF** — 그림 3 의 평형 곡선(DNN 은 91호의 율 외삽 EMF 로 읽힘 · NDB 출처 미인쇄). 우리 재현은 ③ → ④ 를 인쇄 식(9) · (12) 로 시험한 것이다.

---

# 판정 먼저

1. ★★★★ **(a) 98호 지목 — "extended with an ionic concentration-dependent diffusion coefficient in the positive electrode" ✅ · 그러나 그 확장 하나만이 아니다 · "experimentally validated" ❌(검증 층위 아님).** `[인쇄]` "In the present study, the same charge transport mechanisms are used as in [7], but a new concentration dependent diffusion coefficient is taken into account" — D_Li(x) = 마디 넷(x 0.50 · 0.80 · 0.95 · 1.00)의 꺾은선(표 2 · 그림 2b · `[도표·화소]` 그림 5a — 마디 사이가 D 에 선형 ✅). 같은 지면이 말하지 않은 변화 둘: (i) **음극 Li 의 Butler–Volmer**(식 (2) · (4) · (6) · (14) 의 η_ct^Li · α_Li 0.5 — 91호는 음극 동역학을 "for convenience" 무시 — 91 · 98호 digest 전사) · (ii) **같은 DNN 자료(= 91호 곡선)에서 전해질 값을 다시 맞춤** — δ 0.18 → 0.04 · D_Li⁺ 0.90 → 6.0 ×10⁻¹⁵ · D_n⁻ 5.10×10⁻¹⁵ → 6.0×10⁻¹⁷ · `[재현]` t₊ 0.150 → 0.990 · σ 2.44×10⁻⁶ → 5.47×10⁻⁷ S cm⁻¹. "validated": 이 편의 `valid*` **0 회** — 모의는 **같은 자료에 맞춘 것**(DNN 열 ← DNN 곡선 · NDB 열 ← NDB 곡선)이고, 지면 안의 유일한 자료 사이 이전 시험(DNN D(x) → NDB)은 실패했다(`[인쇄]` "Apparently, the same parameters for diffusion coefficient cannot be used simultaneously for both datasets" · `[도표·화소]` 그림 5b 끝 용량 실험 대비 0.64 · 0.88 · 0.96 — 42C · 8C · 0.8C).
2. ★★★★ **(a) 100호 지목 — "fit the diffusion coefficient as a function of lithium-ion concentration" ✅ · "high accuracy even at a current density of 5 mA/cm²" 부분(초록 ✅ · 본문 · 그림 ❌) · "The accuracy of COMSOL simulations has been verified … [8]" ❌.** 초록은 "fit … up to 5 mA cm−2" 라 쓰지만 결과 절은 "this agreement declines towards very high discharge currents as Fig. 4b reveals" — `[도표·화소]` 그림 4b 의 5000 µA cm⁻²(42C): 모의 끝 **72.6 ↔ 실험 79.0 µAh cm⁻²(0.919)** · 평탄 전압 모의가 **30–80 mV 낮음**(Q 10–60). COMSOL 은 "was programmed in COMSOL Multiphysics 4.4" 한 문장 — 격자 · 허용 오차 · 해석해 대조 0 · 서론이 약속한 "other numerical solutions" 와의 비교도 지면 0(D10). ⇒ `[해석]` 100호의 'COMSOL 정확도 검증' 인용 묶음에서 이 편 지면이 주는 것은 수치 검증이 아니라 **모형 ↔ 실험 곡선 겹침(표본 내 적합)** 이다.
3. ★★★★ **(a) 104호 지목 — "[26, 29] … extended to include a concentration-dependent diffusion coefficient" 는 [26](이 편) ✅ · [29](= 91호) ❌(91호 D_Li 상수 1.76×10⁻¹⁵ — 91호 digest 전사) · "an improved accuracy … when compared to experimental data [26]" 부분.** 이 편 지면의 '개선' 비교는 **NDB 한 셀 · 세 율 · 표본 내**: 비교 대상 = 같은 NDB 곡선에 맞춘 **상수 D 하나(자유도 1)** ↔ D(x) 마디 넷 · 지표 0(그림만 · `RMS` · `error` · `residu*` 0 회). DNN(91호 자료)에서는 상수 D 모형과의 비교가 지면에 없다 — 91호 digest 의 재풀이(51.2C 모형 끝 용량 = 측정의 **73–78 %**)와 이 편 그림 4a(**95 %** — `[도표·화소]` 8.69 ↔ 9.13)를 이으면 고율 끝 용량은 좋아졌다(두 지면의 도표 대조 — `[도표·화소]` · 91호 digest 전사). ★ 그러나 `[재현·가정]`(끝 용량만 본 근사 모형 — 전압 곡선 비교 0) **그 개선은 D 의 x 의존 없이 D 크기만으로도 설명된다** — 양극 확산만 푼 우리 재풀이(아래 판정 5 의 대리 모형)에서 **상수 D 5.5–6.0×10⁻¹⁵ 가 DNN 세 율 끝 용량을 최대 오차 0.005–0.013(용량 분율)로 내고, 표 2 의 D(x) 는 0.035–0.045** 다(§(c) 4). NDB 에서는 어느 상수 D 도 세 율을 함께 못 낸다(42C 를 맞추는 4×10⁻¹⁴ 면 8C 0.926 ↔ 실험 0.811) — **x 의존이 자료로 요구되는 곳은 두꺼운 NDB(1.8 µm) 하나**이고, 그곳에서도 42C 는 −10 % 남는다.
4. ★★★★ **(b) 원장 질문 "26호 '문헌값' 의 바로 앞 단계인가" ❌ · "98호와 같은 상용 셀인가" ❌.** 26호 '문헌값' 10 = 98호 표 3(적합 9 + EMF 유도 1 — 98호 digest §(a) 전사). 이 편 표 2 ↔ 98호 표 3 같은 이름끼리: **같은 값은 α_Li 0.5 하나(대칭 기본값)** · c₀ 60,100 · 62,000 ↔ 61,141(1.4–1.7 % 차 — 같은 자릿수 · 같은 값 아님) · 나머지 k_r ×89 · δ ×16 · D_Li⁺ ×35–127 · D_n⁻ ×0.1–0.4 · c_max ×0.72–1.51 · 이 편에 **D_e⁻ 가 없다**("Assuming complete screening of Li ions in the cobalt oxide electrode" — 양극 = 단일 종 Fick) ⇒ **26호의 `D_e⁻` 10 자릿수 표류도 '×1.0500' 도 이 편에서 시작되지 않는다**(둘 다 98호 값이 기준 — 91 · 98호 digest 의 판정과 같은 결론을 이 편 원문으로 닫는다). 이 편에서 98호로 넘어간 것은 값이 아니라 **'양극 D 의 x 의존 + 2상 근거' 라는 구조 하나**이고 모양도 다르다(98호 β(x) 꺾임 ≈0.75 · ≈0.92 · x > 0.95 반등 0 — 98호 digest :129 ↔ 이 편 꺾임 0.80 · 0.95 · x 1.0 쪽으로 ×14 반등). 자료: DNN = **91호 자기 제작 셀**(Li₃PO₄ 1.5 µm · LCO 320 nm) · NDB = **[22] ORNL 셀**(Li 3 µm · LIPON 1 µm · LCO 1.8 µm) — 98호의 상용 0.7 mAh 셀(LiPON 3.62 · LCO 8.08 µm)과 다르다.
5. ★★★★ **(c) 재풀이 폐합 — 우리 근사 재풀이에서 인쇄 표로 그림의 끝 용량 열둘 · 그림 6a 농도가 다시 난다 · 전압 곡선은 표로 재풀이할 수 없다(k₁ˢ · k₂ˢ 미인쇄).** `[재현·가정]` 표 2 의 D(x) 꺾은선 · c_max · c⁰(x₀ 0.5) · 2절 두께(320 nm · 1.8 µm) · 인쇄 전류로 **양극 Fick(식 12)만** 풀고 표면 x 가 0.995 에 닿는 순간을 차단으로 두면(0.99–0.999 로 흔들어 폭 표시) 그림 4 · 5 의 끝 용량 **열둘을 −2.2 … +1.7 % 안**에서 다시 낸다 — DNN D(x) | DNN 8.68 · 9.64 · 9.84 ↔ 그림 8.69 · 9.74 · 9.95 · NDB D(x) | NDB 71.2 · 94.5 · 113.4 ↔ 72.6 · 95.4 · 113.7 · DNN D(x) | NDB 49.6 · 83.5 · 107.7 ↔ 50.7 · 84.0 · 108.7 · 상수 1.3×10⁻¹⁴ | NDB 30.8 · 93.4 · 114.1 ↔ 30.3 · 93.0 · 114.0 µAh cm⁻²(91호 상수 1.76×10⁻¹⁵ | DNN 51.2C 7.13 ↔ 91호 digest 재풀이 7.19 — 같은 대리 모형이 91호도 닫는다). 전해질 식 (9) 를 표 2 DNN 값 그대로 풀면 그림 6a 경계 농도를 **≤2 %**(30 s 2694 · 2114 ↔ ≈2650 · ≈2100 · 60 s 2817 · 1991 ↔ ≈2775 · ≈2015 mol m⁻³) · LCO 평균 농도 증가가 512 µA cm⁻² 와 **2 % 안**(−0.8 · −1.6 %). 못 하는 것: **k₁ˢ · k₂ˢ(식 5 · 6) 값이 표에 없다** · E_eq(x) 함수형 · T · A 미인쇄 ⇒ 전압 곡선 · 평탄 과전압 분해는 인쇄 표로 재풀이 불가 · 그림 6b 의 전류는 'comparable C-rate' 뿐(`[재현]` LCO 평균에서 6.0–6.1 · 전해질 경계에서 5.0–5.5 mA cm⁻² — 실험 최고 5 mA cm⁻² 이상).
6. ★★★★ **(c) Q4 — 0/115 · 백일곱 번째 성질.** 추정은 "Values for the concentration dependent diffusion coefficient and constant diffusion coefficient are the result of optimization on rough grid" **한 문장**(격자 · 목적 함수 · 움직인 매개변수 · 잔차 · 불확실성 0) · `identif*` · `uniqu*` · `uncertain*` · `confiden*` · `sensitiv*` · `error` · `±` · `residu*` · `correlat*` · `valid*` **본문 0**. 우리가 보인 것(`[재현·대수]` · `[재현]` — 저자 판정 아님): ① **끝 용량은 D(x)/M² 만 본다** — 양극 부분계의 끝 용량 분율은 G = j·M/(F·c_max·D) 하나의 함수이고 c_max·M 은 EMF 용량이 고정하므로, NDB 두께가 지면 안에서 1.8 µm(2절 · 그림 6b · 우리 폐합) ↔ **"3 μm"**(3절 두 번)로 갈리면 D 는 ×2.78 · c_max 는 ×0.6 로 같은 곡선을 낸다 — "different deposition process … which increased Li-ion diffusion" · "a higher packing density" 해석이 두께에 매달린다 ② **전해질 넷은 σ 하나로 접힌다** — 두 열 모두 D_n⁻ = D_Li⁺/100(t₊ 0.990)이라 51C DNN 의 전해질 손실 −140.4 → −140.8 mV 중 농도 몫 **−0.2 mV**(NDB 5 mA 에서 −0.9 mV) — δ · c₀ · D_Li⁺ · D_n⁻ 가 σ ∝ δc₀(D_Li⁺ + D_n⁻) 한 수로만 보인다 ③ **같은 자료 · 같은 연구실 · 두 표** — 91호(2011)와 이 편(2019)이 같은 DNN 곡선을 다른 모형 구조로 맞춰 전해질 값이 ×0.012–×6.7 · t₊ 0.15 ↔ 0.99 · 51.2C 전해질 손실 **−109 mV(시간에 따라 자람 · 농도 몫 68 %) ↔ −141 mV(일정 · 옴)** — 두 편 다 '일치' 로 닫았다(91호 digest 의 국소 CRB '전해질 넷 한 묶음' 의 야생 대조 — 단 모형 구조가 달라 같은 골짜기 위의 두 점은 아니다).
7. ★★★ **(주) "the cathode diffusion constant is a prime factor limiting the rate capability" — `[해석]` 차단 용량의 뜻으로는 이 모형 구성상 참 · 평탄 과전압의 뜻으로는 이 편 자기 매개변수에서 전해질(옴)이 55–77 %(`[재현]`).** `[재현]` 끝 용량은 양극 확산만으로 열둘이 다 닫힌다(판정 5) — 이 모형에서 끝 용량을 정하는 다른 항이 없다. `[재현]` + `[도표·화소]` 평탄 과전압(그림 3 EMF − 곡선): DNN 51C ≈173–188 mV 중 전해질 옴 140.5 mV(**77 %**) · NDB 42C 382–405 mV 중 249–265 mV(**≈65 %**) · NDB 8C 88 mV 중 48 mV(55 %). "ultrafast charging application where > 5C is desired" — **충전 모의 0**(`charging` 7 회 = ultrafast charging 2 · charging times 1 · discharging 4) · "enables a method to optimize thickness" — 최적화 계산 0.
8. ★★★ **c_max = 용량 ÷ (F·M·Δx 0.5) — '전기 활성' 이 한 수로 접힌다(카드 Q1 층).** `[재현]` DNN 23,300 = EMF ≈10.05 µAh cm⁻² ÷ (F · 320 nm · 0.5)(+0.6 %) = 91호 a_max · NDB 48,760 = ≈117.1 µAh cm⁻² ÷ (F · 1.8 µm · 0.5)(−0.4 %) · `[재현·외부 값]` 조밀 LCO 격자 Li 51.6 kmol m⁻³ 의 **45 % · 94.5 %**. 이 편은 그 차를 "a higher packing density and electro-activity obtained for NDB cells" 로 읽는다. `[재현·대수]` 1D 평면 모형에서 **고립된(전해질에 안 닿는) 면적 분율 f 는 c_max·f 로 정확히 흡수**된다(끝 용량 함수 G 와 EMF 용량이 둘 다 c_max·f 만 본다) — 밀도 · 비활성 물질 · 접촉 면적 손실이 이 모형에서는 같은 LAM 형 용량 스케일 한 자리다(그리고 BV 쪽에서는 미인쇄 k₁ˢ 와 곱).
9. ★★ **Q1 해당 없음(`θ(N)` 0/115) · Q2 없다 · Q5 해당 없음(Li 금속 — 음극 BV 만 신설) · Q6 해당 없음 · Q7 해당 없음 · Q8 층 하나** — 아래 §(f).
10. ★★ **SI 없음 · 자료 · 코드 공개 0** — 보충 언급 0(직접 셈 — `supplement*` · `supporting` · `appendix` · `video` 0) · `/Names` 의 `/EmbeddedFiles` · `/JavaScript` 둘 다 빈 사전(obj 520 `<<>>`) · 자료 = 문헌 곡선 두 묶음(디지타이즈 여부 미인쇄).

⚠ 어긋남 **20 건**(D1–D20 — 아래 절) · 공백 **14 건**(G1–G14).

---

# ★ 중심 표 — 지목 · 관련 digest 가 이 편에 건 것 ↔ 이 편 지면 (✅ 있다 · 부분 · ❌ 없다)

| # | 누가 · 무엇을 걸었나 | 이 편 지면 | 판정 |
|---|---|---|---|
| 1 | 98호 :182 · :421 — "Recently, the model developed by Danilov et al. [11] has been extended with an ionic concentration-dependent diffusion coefficient in the positive electrode [18]" | D_Li(x) 꺾은선(마디 넷 · 2상 경계 0.80 · 0.95) ✅ · 그 밖의 변화 — 음극 BV 신설(식 4 · 6 · 14 · α_Li 0.5 · k₂ˢ 미인쇄) · 같은 DNN 자료에서 전해질 재적합(δ ×0.22 · D_Li⁺ ×6.7 · D_n⁻ ×0.012) — 지면 서술 0 ("the same charge transport mechanisms are used as in [7]") | **✅ 확장 내용** · 단 확장은 하나가 아니다(D11) |
| 2 | 98호 :182 — "Their model simulations have been experimentally validated." | `valid*` 0 회 · 모의 = 같은 자료 적합(표본 내) · 이전 시험 하나(DNN D(x) → NDB) 실패 — 저자 인쇄 "cannot be used simultaneously" | **❌** 검증 층위 아님(표본 내 적합) |
| 3 | 98호 :683 · 원장 L229 — "그 매개변수 표 · 자료(같은 상용 셀인가) · 적합 방법 — 26호 '문헌값' 계보의 바로 앞 단계" | 표 2 두 열(각주 0) · 자료 = 91호 셀 + [22] ORNL 셀 · 방법 = "optimization on rough grid" 한 문장 · 98호 표 3 과 같은 값 = α_Li 0.5 하나 · D_e⁻ 없음 | **❌** 바로 앞 단계 아님(값 상속 0 · 구조 하나) · 상용 셀 ❌ |
| 4 | 100호 :185 — "Kazemi [8] fit the diffusion coefficient as a function of lithium-ion concentration … high accuracy even at a current density of 5 mA/cm2" | 초록 "fit … up to 5 mA cm−2" ✅ ↔ 결과 절 "agreement declines towards very high discharge currents" · `[도표·화소]` 42C 끝 0.919 · 평탄 −30 … −80 mV | **부분**(D 의 x 함수 ✅ · '고율 고정확' 은 초록만) |
| 5 | 100호 :201 — "The accuracy of COMSOL simulations has been verified by many researchers [8], [9], [18], [25], [29], [30]" | "programmed in COMSOL Multiphysics 4.4" 한 문장 · 수치 검증 · 격자 · 허용 오차 0 · 서론의 "other numerical solutions" 비교 0 | **❌** |
| 6 | 104호 :213 — "some modeling studies have been extended to include a concentration-dependent diffusion coefficient [26, 29]" | [26] = 이 편 ✅ · [29] = 91호 — 91호는 D_Li 상수(91호 digest 전사) | **부분**([26] ✅ · [29] ❌) |
| 7 | 104호 :213 — "Through this extension, there has been an improved accuracy of the predicted data when compared to experimental data [26]" | NDB 에서 상수 D(자유도 1) ↔ D(x)(마디 넷) 표본 내 비교 · 지표 0 · DNN 에서 비교 0 · `[재현·가정]` DNN 끝 용량은 상수 D ≈5.5×10⁻¹⁵ 로도 같거나 더 잘 남 · '예측(predicted)' = 같은 자료 적합 | **부분**(NDB 고율 개선 ✅ · '예측' ❌ · x 의존의 필요는 NDB 만) |
| 8 | 37호 :116 — "Kazemi [13] adopt a strategy of calibrating the diffusion coefficient" (서지 미전사) | 같은 편이라면: 자료 묶음(셀)마다 D(x) 를 다시 맞춤 ✅ · **율마다 맞춘 것은 아님**(한 셀 세 율에 D(x) 하나) — 37호의 D_p,ref(C-rate)(37호 digest :246)의 선례로는 부분 | **부분**(37호 원문 미열람 · 37호가 이 문장을 어디에 붙였는지는 digest 전사 한 줄) |
| 9 | 12호 :387 — Kouhestani 표 1 "Mathematical model [65,72,78] … ✗ (순방향)" 의 [72] = "Kazemi 박막 정확도"(12호 digest 해석 · 서지 미전사) | 열화 · SOH · RUL 0 · 순방향 모형 + 매개변수 적합 | **✅**(순방향) · [72] 가 이 편인지는 12호 원문 미열람 |
| 10 | 카드 Q4 · 개념 [[assb-sensitivity-sweep-vs-identifiability]] — 계보의 'sensitivity = sweep' · '곡선이 맞는다 = 식별' 관행 | 스윕 0 · 추정 한 문장 · 식별성 어휘 0 · 같은 자료 두 표(91 ↔ 이 편) | **❌ 식별성** · 새 성질 하나(판정 6) |
| 11 | 카드 Q1 · Q6 | 조밀 평면 박막 · 접촉 · 공극 · 압력 0 · `contact` 0 | **❌ 해당 없음**(층 하나 — 판정 8) |
| 12 | 5차 묶음 13 편 | 인용 0(참고문헌 [1]–[22] 전수 대조 — [6] 은 Takada **2013** *Acta Mater.* 61, 759 · 5차 #4 의 Takada 1996 *SSI* 86–88 과 다른 편) · 흡수 편 교차 둘([7] = 91호 · [17] = 102호) | 교차 둘 |

---

# 서지

| 항목 | 값 (`[인쇄]` — p. 111 · p. 116 · 정보 사전 · XMP) |
|---|---|
| 제목 | **"Modeling of all-solid-state thin-film Li-ion batteries: Accuracy improvement"**(지면) — 정보 사전 · XMP dc:title 은 콜론이 밑줄 "…batteries_ Accuracy improvement" · 책갈피 첫 줄은 콜론 |
| 저자 · 소속 | **Namdar Kazemi**ᵃ · **Dmitri L. Danilov**ᵇ'ᶜ\*(교신 — Forschungszentrum Jülich (IEK-9) · 메일 인쇄 — 옮기지 않음) · **Lucas Haverkate**ᵃ · **Nancy J. Dudney**ᵈ · **Sandeep Unnikrishnan**ᵃ · **Peter H.L. Notten**ᵇ'ᶜ'ᵉ — ᵃ Holst Centre/TNO, High Tech Campus 31, Eindhoven · ᵇ Eindhoven University of Technology · ᶜ Forschungszentrum Jülich (IEK-9) · ᵈ Oak Ridge National Laboratory · ᵉ University of Technology Sydney. **저자 여섯**(XMP dc:creator 여섯 · 정보 사전 author "Namdar Kazemi" 하나) — 원장 행 저자 목록과 같음 |
| 저널 | *Solid State Ionics* **334**(2019) **111–116** · doi `10.1016/j.ssi.2019.02.003` · ISSN 0167-2738 · 호 번호 인쇄 0 |
| 일정 | "Received 2 September 2018; Received in revised form 1 February 2019; Accepted 4 February 2019" · "Available online 18 February 2019" · `[재현]` 투고 → 수락 **155 일** · → 온라인 169 일 |
| 저작권 | "0167-2738/ © 2019 Elsevier B.V. All rights reserved."(p. 111) · XMP prism:copyright 같음 · xmpRights:Marked True · OA 표기 0 ⇒ **구독본으로 다룬다** |
| 키워드 | **인쇄 0**(지면 · 정보 사전 keywords 빈 문자열) |
| 자금 · 사사 | "Horizon 2020 program of the European Union under the grant of the AutoDrive project (Grant No. 737469), the DEMOBASE project (Grant No. 769900) and funding from TNO-Holst Centre" · "Declaration of interest: None." |
| 자료 | 공개 저장소 · SI · 코드 0 · 자료 = 문헌 두 묶음(91호 [7] · [22]) — 디지타이즈 방법 · 원자료 출처 미인쇄 |
| 분량 | PDF **6 쪽**(인쇄 111–116 · PageLabels 111 부터 = 인쇄 쪽 · 이 digest 의 "p. N" = 인쇄 쪽 · "PDF p. n" = n + 110) · 그림 **6**(전부 래스터 JPEG) · 표 **2** · 번호 식 **(1)–(14)** · 참고문헌 **[1]–[22]**(빠진 번호 0 · 22 개 모두 본문 · 표 인용 — [3] · [4] 는 서론 시장 문장) |
| 절 | 초록 · 1. Introduction · **1.1. Theoretical description**(이론이 서론의 하위 절) · 2. Experimental(자료 출처) · 3. Results and discussion · 4. Conclusions · Declaration of interest · Acknowledgement · References — 책갈피 9(제목 포함) |
| 셀(모형) | 1D(y) · Li 금속 음극(y < 0 · 농도 변수 0) \| LIPO(N) 해리 SE(0 ≤ y ≤ L) \| LiCoO₂ 평면 막(L ≤ y ≤ L + M) · 집전체 0 · 등온(T 미인쇄) · 면적 A 미인쇄 · COMSOL Multiphysics **4.4** |
| 셀(자료) | **DNN** = 91호 [7] "Li/LIPO/LiCoO2 thin-film solid state batteries with electrolyte thickness of 1.5 μm and a cathode thickness of 320 nm" · 32 · 128 · 512 µA cm⁻²(91호 여섯 율 중 셋 — G7) · **NDB** = [22] "a Li/LIPON/LiCoO2 cell was investigated with 3 μm of Li, 1 μm of LIPON and a cathode with thickness of 1.8 μm" · 100 · 1000 · 5000 µA cm⁻² · 두 묶음 모두 EMF + 방전 셋(그림 3) |
| 운전(모형) | 정전류 방전만 · 차단 3.0 V(그림 축 끝 — 본문 미인쇄) · 충전 · 휴지 · EIS 모의 0 |
| 식 | (1) LiCoO₂ ⇌ Li₁₋ₓCoO₂ + xLi⁺ + xe⁻(0 ≤ x ≤ 0.5) · (2) Li ⇌ Li⁺ + e⁻ · (3) · (4) BV(양극 · 음극) · (5) · (6) 교환 전류 I⁰ = F·A·kˢ·(농도 곱) · (7) Li⁰ ⇌ Li⁺ + n⁻(k_d · k_r) · (8) Nernst–Planck · (9) 앰비폴라 확산 + 반응 · 경계 ∂c/∂y = I/(2FAD_Li⁺) 양끝 · (10) 전기장 닫힌 꼴 · (11) η_mt = (RT/F)ln(c(L)/c(0)) − ∫E dy · (12) 양극 Fick D_Li(c) · 경계 D·∂c/∂y = I/(FA) · 집전체 0 · (13) η_d = E_eq(xˢ) − E_eq(x̄) · (14) E_bat = E_eq(x̄) + η_d + η_ct^LCO + η_ct^Li + η_mt |

**PDF 메타데이터 (이 실행에서 직접 읽음 · pymupdf)** — **1,591,722 B** · sha256 `74fc79d83f00c40bf9636546a6ba728b172c668e2f4e86f24df1a78e49e48802`(**호출자 명시값 ✅ — 직접 재계산 · 크기도 일치**) · 헤더 `%PDF-1.7` · 6 쪽 전부 **595.276 × 793.701 pt** · 암호 0 · 정보 사전: title "Modeling of all-solid-state thin-film Li-ion batteries_ Accuracy improvement" · author **"Namdar Kazemi"** · subject **"Solid State Ionics, 334 (2019) 111-116. doi:10.1016/j.ssi.2019.02.003"** · keywords 빈 문자열 · creator **"Elsevier"** · producer **빈 문자열** · 생성 = 수정 **D:20190323095050Z** · XMP **6,738 B**(dc:creator **여섯** · prism:doi · volume 334 · startingPage 111 · endingPage 116 · issn 0167-2738 · xmp:CreateDate = ModifyDate 2019-03-23T09:50:50Z · CreatorTool Elsevier · jav:journal_article_version **VoR** · pdfx:robots **noindex** · crossmark:MajorVersionDate 2010-04-23 · xmpRights:Marked True · dc:publisher Elsevier · dc:description = subject) · `%%EOF` **1** · startxref 1(증분 갱신 0) · 트레일러 ID [0F3F3925… · FE9A25DD…](두 값 다름) · 카탈로그 `/AcroForm`(Fields []) · `/Lang (en)` · `/Names` → `/Dests` · `/EmbeddedFiles` · `/JavaScript`(**뒤 둘은 같은 obj 520 = 빈 사전 `<<>>` — 임베디드 파일 0 · JS 0**) · `/OCProperties`(OCG 하나 "Layer 1") · `/OpenAction` FitH · `/Outlines`(책갈피 9) · `/PageLabels` `/S /D /St 111` · `/PageLayout /SinglePage` · `/PageMode /UseOutlines` · 래스터 **9**(p. 111 머리 셋 — JPEG 247×271 · 236×298 · PNG 192×191 — 출판사 로고 · 표지 · CrossMark 로 읽힘 / 그림 1 **JPEG 1034×1373 회색조** · 그림 2 JPEG 951×1152 · 그림 3 · 4 · 5 JPEG 1423×620 · 627 · 533 · 그림 6 JPEG 1423×1002 — `[재현]` 1423 px ÷ 341.5 pt × 72 = **300 dpi** · **전부 JPEG(손실)**) · 벡터 그림 0 · 글꼴 STIX Two Text / Math · STIX General · Charis SIL · Univers LT Std · URI 링크 39(refhub 참고문헌 · doi · CrossMark · mailto).

⚠ **텍스트 층**: NFKC 가 바꾸는 글자 **0** · 합자 0 · 줄 끝 하이픈 분철은 본문에 흔함(어휘 집계 전에 복원) · **식 (1)–(14) 와 표 2 의 첨자 · 분수는 낱글자로 흩어진다**(예: 식 (9) 가 "= + + = = = + + + + c t D D D D c y r …" 로 추출) → **식은 쪽 렌더(160 dpi — 판독용 · 커밋 안 함)로 읽었다** · 표 1 · 2 는 텍스트 층과 자동 크롭 이미지를 대조(✅).

---

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | **적합 방법** — "optimization on rough grid" 한 문장: 격자 범위 · 간격 · 목적 함수 · 율별 가중 · 움직인 매개변수(DNN · NDB 열 각각) · 두 열에서 같은 다섯(k_d · k_r · α_Li · α_LCO · δ)이 고정인지 결과인지 · 잔차 · 시작점 0 | '거친 격자' 의 칸 간격이 곧 값의 해상도인데 미인쇄 — 같은 값 다섯이 '움직이지 않은 것' 인지 '격자 한 칸 안' 인지 가를 수 없다(26호 G1 의 7/10 ×1.0500 과 같은 꼴의 물음) |
| **G2** | **k₁ˢ · k₂ˢ 값** — 식 (5) · (6) 의 표준 속도 상수가 표 2 에 없다(α 만 있음) · 음극 BV(식 2 · 4 · 6)를 새로 넣은 근거 · 값 0 | 교환 전류 i₀ 둘을 재현할 수 없다 → 평탄 과전압의 BV 몫 · 전압 곡선 재풀이 불가(판정 5) |
| **G3** | **E_eq(x) 의 함수형 · 출처** — 그림 3 의 EMF 곡선뿐 · DNN EMF 는 91호의 율 외삽 EMF 로 읽힘(끝 ≈10.05 ↔ 91호 10.10 — `[도표·화소]`) · **NDB EMF 의 출처 미인쇄**([22] 에 있던 곡선인가 · 이 편이 외삽했나) | 모형의 몸통(식 13 · 14)인데 재현 불가 · '같은 자료의 외삽 EMF 를 평형 곡선으로 되먹임' 관행(91 · 98호)이 이 편에도 이어지는지 확인 불가 |
| **G4** | **T · A · 1C 기준 용량 · 전류의 면적 기준** — 셋 다 미인쇄 · 율 이름표 반올림이 두 판에서 다름(D20) | 우리 재풀이는 면적당 양(µA cm⁻² · µAh cm⁻²)으로만 닫았다 · 온도는 RT/F 항에 들어간다(우리 298.15 K 가정) |
| **G5** | **NDB 양극 두께** — 2절 "1.8 μm" · 그림 6b "LCO : 1800 nm" ↔ 3절 "thicker films (e.g. 3 μm)" · "the NDB cathode with 3 μm thickness" · 원 [22] 의 값 | 우리 끝 용량 폐합은 1.8 µm 로만 닫힌다(저자 계산 = 1.8) · 실제 막이 3 µm 면 D ×2.78 · c_max ×0.6(판정 6 ①) — 'deposition 이 확산을 높였다' 해석의 크기가 바뀐다 |
| **G6** | **NDB 자료의 형태** — [22] 에서 어떻게 옮겼나(디지타이즈 · 원자료) · 온도 · 충전 조건 · 차단 · 셀 면적 · 같은 셀 세 율인가 | 이 편 비교의 실험 쪽 층위가 정해지지 않는다 |
| **G7** | **DNN 율 선택** — 91호 여섯 율(1.6–51.2C · 91호 digest 전사) 중 셋(3.2 · 12.8 · 51.2C)만 · 이유 0 | 맞춘 율과 안 맞춘 율을 가르면 표본 밖 시험이 될 수 있었는데 하지 않았다 |
| **G8** | **상수 D 1.3×10⁻¹⁴ 의 정체** — "average constant diffusion coefficient"(무엇의 평균?) ↔ "the result of optimization on rough grid" · DNN 자료에서 상수 D 비교 0 | '정확도 개선' 의 비교 대상이 공정한 최적 상수인지 가를 수 없다 · `[재현·가정]` NDB 에서 상수 D 1.3×10⁻¹⁴ 는 8C · 0.8C 를 맞추고 42C 를 0.26 로 버리는 점이다(§(c) 4) |
| **G9** | **그림 6b 의 전류** — 캡션 "comparable C-rate" 뿐 | `[재현]` 5.0–6.1 mA cm⁻² — 실험 최고 5 mA cm⁻² 이상의 외삽일 수 있다 |
| **G10** | **D(x) 마디의 출처** — x 0.80 · 0.95 경계와 1.00 끝값이 상도에서 온 것인지 적합인지 · "weighted sum of the single-phase diffusion coefficients … proportional to the amount of particular phase" 를 구현했는지(표 2 는 마디 넷뿐 — 지렛대 규칙이면 2상 구간은 끝 마디 사이의 선형과 같다) | 자유 매개변수 수(마디 넷 + 경계 둘?)가 미상 |
| **G11** | **수치 해법** — COMSOL 4.4 · 격자 · 시간 간격 · 허용 오차 · 서론이 약속한 "other numerical solutions" 와의 비교 0 | 100호가 이 편을 'COMSOL 정확도 검증' 근거로 든다 — 근거 0 |
| **G12** | **불확실성 · 반복** — 셀 하나씩(문헌) · 오차 막대 · 잔차 · 신뢰구간 0 | 표 2 두 열 차(×2–4)가 적합 폭보다 큰지 정할 기준이 없다 |
| **G13** | **그림 2a 계열의 원 자료 · x 축 변환** — Dokko(EIS · 'particle') · Jang(PITT · 'RF film (110)') · Tang(EIS · 'PLD film (003)') — 102호 digest 가 전사한 Xie 2008 의 Jang 소개는 "(003) oriented thin film using a solid state electrolyte" ↔ 이 편 '(110)' · 표 1 [13] · [14] 가 같은 범위 · 같은 x 구간(4·10⁻¹⁵–3·10⁻¹³ · 0.45 < x < 0.75) | 이 편 D(x) 모양(0.95 골)의 근거 계열이 무엇인지 · 원 [12] · [13] · [19] 미열람 |
| **G14** | **c₀(NDB 62,000 mol m⁻³) 의 출처** — LIPON 총 Li 농도 · 측정인가 · 문헌인가(DNN 60,100 = 91호 NDP 측정 — 91호 digest 전사) | 전해질 쪽 유일한 '측정형' 입력의 층위 |

---

# 보충 자료 — 받은 것 · 대조

**SI 없음 (원문에 보충 언급 0).** 호출자 대조와 같은 결과를 이 실행에서 직접 다시 셌다 — 본문 · 캡션 · 표 · 참고문헌 전문(줄 이음 뒤)에서 `supplement*` · `supporting` · `appendix` · `video` · `movie` **0 회** · 자료 문장은 2절 "Experimental data used in this paper are represented by two datasets available in literature" 하나. PDF 안 임베디드 파일 0(`/EmbeddedFiles` = 빈 사전). 원자료 · 코드 0 ⇒ 이 digest 의 재현은 **인쇄 수치 · 식 · 래스터 그림 화소**로만 했다(`[데이터]` 표시 0).

---

# 그림 · 표 — 자동 6 항목 + 수동 3, 실제로 연 것 **9/9**

크로퍼(`wiki/tools/extract_figures.py --dpi 200 --maxpx 2000` — 이번 묶음 방침)가 그림 1 · 2 · 3 · 4 와 표 1 · 2 를 잡고 그림 5(p. 114 '영역 없음') · 그림 6(p. 115 '그래픽 없음(img0/draw0)')을 제외했다(SI 판별 ✅ — 파일명 `…110._Modeling_of_…` 에 SI 표지 0 · `fig_S…` 0). 문제 셋을 수동으로 고쳤다(200 dpi · 파일명 `…_manual_p<PDF 쪽>.png` · `figures.json` `manual: true` + note · 쪽 번호는 PDF 쪽 — 인쇄 쪽 = PDF 쪽 + 110):

- **오크롭 하나** — 자동 `fig_4.png`: bbox 가 같은 쪽 위의 **그림 3 을 잡았다**(내용 = 그림 3 + 오른쪽 여백 — 110호 그림 폴더 `zhang2017_carbon-additives-lgps-ssb-decomposition` 의 선례대로 지우지 않고 note '⚠ 오크롭') → `fig_4_manual_p4.png`(그림 + 오른쪽 옆 캡션).
- **옆 캡션 누락 둘** — 그림 5(p. 4) · 그림 6(p. 5): Elsevier 오른쪽 옆 캡션(x 390–558 pt · 그림은 x 38–379)이라 크로퍼가 영역을 못 찾음 → `fig_5_manual_p4.png` · `fig_6_manual_p5.png`.
- 표 2 자동 캡션 필드에 표 본문 텍스트가 섞임(내용 손상 0 · note 표시).

**9 장 전부 이 실행에서 직접 열었다 — 안 본 그림 · 표 0.** 판독: 그림 3–6 은 **PDF 에서 원본 래스터(JPEG 1423 px 폭 · ≈300 dpi)를 꺼내** 축 틀(검정 행 · 열 합)과 눈금 · 눈금 이름표의 화소 중심으로 보정했다(`[도표·화소]` — 그림 3a x 48.9 px/(µAh cm⁻²) · y 332 px/V · 그림 3b 4.55 px/(µAh cm⁻²) · 그림 4a 46.75 px · 65.6 px/0.2 V · 그림 4b 5.11 px · 66 px/0.2 V · 그림 5a 로그 축 바깥 눈금 66.5 px/decade · x 109.2 px/0.1 · 그림 5b 90.25 px/20 µAh cm⁻² · 61 px/0.2 V · 그림 6 아래 판 좌 · 우 축 이름표 — 보정 잔차는 이름표 간격 ±1–2 px). 선은 색 분류(초록 · 빨강 · 파랑/하늘 · 검정)로 골랐고, 끝 용량은 3.00–3.14 V 띠 안 색 화소 열의 중심으로 읽었다(JPEG 번짐 · 선 굵기 ≈3–4 px — 판독 폭 ±0.1 µAh cm⁻²(DNN) · ±0.7(NDB)). 그림 1 · 2 는 `[도표]` 눈 판독 + 그림 1 SEM 열 평균 밝기 단면. 판독 배열 · 스크립트는 `scratchpad/assb5/k115/` 에만(커밋 안 함).

## Fig. 1 — SEM 단면 + 1D 모식 (p. 112 · 봤다 · 자동 · JPEG 회색조) ★★ D16

(위) SEM 단면 — 이름표 'Li' · 'LIPO' · 'LiCoO₂' · 밝은 경계 · 오른쪽 어두운 기판 · **축척 막대 0**. `[도표·화소]` 열 평균 밝기 단면으로 띠 폭: LIPO **≈228 px** · LiCoO₂ **≈264 px**(비 **≈1.2** · 경계 ±15 px) — 모의 셀 DNN 320/1500 nm = **0.21** · NDB 1.8/1.0 µm = **1.8** 어느 쪽과도 안 맞는다(D16). 91호 그림 1a(91호 digest: Li₃PO₄ ≈233 · LiCoO₂ ≈225 px · 비 ≈0.97 · 캡션 "An example of an SEM image")와 같은 자릿수의 비라 **같은 예시 SEM 으로 읽힌다**(`[해석]` — 화소 대조 0 · 이 편 캡션은 'example' 을 뺐다). (아래) 1D 모식 — Negative electrode: Li anode \| LIPO/LIPON electrolyte \| Positive electrode: LiCoO₂ cathode · y 축 0 · L · L+M · "Li⁺ → discharge" · "Li⁺ ← charge" · 집전체 미표시.

## Fig. 2 — 문헌 D(x) 세 계열 + 제안 D(x) 꺾은선 모식 (p. 113 · 봤다 · 자동 · JPEG) ★★★ (b) · D8 · G13

(위 판 — 캡션 (a)) D vs x(로그 10⁻¹⁶–10⁻¹⁰ m² s⁻¹ · x 0.5–1) — 범례 **Dokko (EIS)**(회색 사각 · 점선 · 이름표 'particle') · **Tang (EIS)**(회색 마름모 · 긴 파선 · 'PLD film (003)') · **Jang (PITT)**(검정 원 · 'RF film (110)') · 세로 점선 x 0.8 · ≈0.935 · ≈0.99. `[도표]`(눈 판독 ±0.2 decade): Dokko ≈5×10⁻¹²(x 0.5) → ≈1×10⁻¹²(0.8) → **골 ≈3×10⁻¹⁴(0.94)** → ≈2–4×10⁻¹³(0.97–0.99) · Jang ≈1.8×10⁻¹⁴ → ≈5×10⁻¹⁵(0.5–0.7 · 그 뒤 점 0) · Tang ≈1.5×10⁻¹⁵(0.53) → ≈3×10⁻¹⁶(0.78) → **골 ≈1×10⁻¹⁶(0.94)** → ≈5×10⁻¹⁶(0.97–0.99). ⇒ **같은 x 에서 세 계열이 4–5 자릿수 갈린다** — 골(≈0.94)과 x → 1 반등은 Dokko · Tang 두 계열에만. ⚠ 캡션 "Estimation of diffusion coefficient for different LiCoO2 cells by EIS measurements (a)" ↔ 범례 Jang **(PITT)** · 판 글자 (a)(b) 는 그림에 인쇄 0(D8).
(아래 판 — (b)) 제안 D(x) 모식: 세로 축 'D / m² s⁻¹' **눈금 0**(정성) · Phase II(0.5–≈0.8) 완만한 감소 → Phase I + Phase II '2상 공존'(≈0.8–≈0.95) 가파른 감소 → Phase I(≈0.95–1.0) 증가 · 경계 ≈0.8 · ≈0.95 · 1.0.

## Fig. 3 — EMF + 측정 방전 곡선 셋 × 두 셀 (p. 114 · 봤다 · 자동 · 화소) ★★★ (b) · Q8 · D20

`[도표·화소]` (a) **DNN**: EMF(검정) · 32 µA cm⁻²(초록 · '3C') · 128(빨강 · '13C') · 512(파랑 · '51C') · 3.0 V 끝 **EMF ≈10.05 · 9.97 · 9.78 · 9.13 µAh cm⁻²** — 91호 그림 3 의 녹색 외삽 EMF 10.10 · 3.2C 9.95 · 12.8C 9.76 · 51.2C 9.17(91호 digest 전사)과 **판독 폭 안에서 같은 자료**로 읽힌다 · 평탄 과전압(EMF − 곡선 · Q 2–6) 51C **173–188 mV** · 13C ≈51 mV(Q 4) · 3C ≈12 mV. (b) **NDB**: EMF · 100(초록 · '0.8C') · 1000(빨강 · '8C') · 5000(파랑 · '42C') µA cm⁻² · 3.0 V 끝 **EMF ≈117.1 · 113.6 · 95.4 · 79.0 µAh cm⁻²** · 42C 평탄 과전압 **382 · 392 · 405 mV**(Q 20 · 40 · 60) · 8C ≈88 mV(Q 20). `[재현]` 율 이름표 = I ÷ Q_EMF 인데 반올림이 다르다: 3.18 → '3C' · 12.7 → '13C' · 50.9 → '51C'(반올림) ↔ 0.85 → '0.8C' · 8.5 → '8C' · 42.7 → '42C'(버림)(D20). 캡션 "EMF and experimental voltage discharge curves" — EMF 의 출처 · 방법 미인쇄(G3).

## Fig. 4 — 측정 ↔ 모의(표 2 의 자기 열) (p. 114 · 봤다 · **수동** · 화소) ★★★★ (a) · 판정 2 · 3 · D1 · D3

`[도표·화소]` (a) DNN 3C · 13C · 51C — 실험(검정 점선) ↔ 모의(초록 실선): 모의 끝 **9.95 · 9.74 · 8.69** ↔ 실험(그림 3a) 9.97 · 9.78 · 9.13 µAh cm⁻² → 모의/실험 **0.998 · 0.996 · 0.952** · 51C 평탄 Q 2–7 에서 ±15 mV · 그 뒤 모의는 ≈8.2 까지 평탄하다가 **8.69 에서 수직 낙하** ↔ 실험은 ≈7.5 부터 완만히 내려가 9.13(끝 모양이 다르다 — 모의의 끝은 표면 포화 하나로 정해짐 · `[재현]` 판정 5). (b) NDB 0.8C · 8C · 42C: 모의 끝 **113.7 · 95.4 · 72.6** ↔ 실험 113.6 · 95.4 · 79.0 → **1.00 · 1.00 · 0.919** · 42C 평탄 모의가 실험보다 **−38 · −29 · −43 · −78 · −74 mV**(Q 10 · 20 · 30 · 50 · 60) · 0.8C 모의는 ≈105 부터 실험보다 먼저 휜다. ⚠ 캡션 "simulation model with diffusion coefficient taken from DNN fit – blue lines" — **그림 4(b) 에 파란 선이 없다**(범례 'Experiment' · 'Simulation' 둘 · D3). 본문 "almost perfect agreement … at low C-rates. However, this agreement declines towards very high discharge currents as Fig. 4b reveals" ✅(그림과 맞음) ↔ 초록 · 결론(D1).

## Fig. 5 — D(x) 세 가지 + NDB 에서 세 모의 (p. 114 · 봤다 · **수동** · 화소) ★★★★ (a) · 판정 3 · 5 · D3 · D5 · D12 · D13

(a) `[도표·화소]`(로그 축 66.5 px/decade · 판독 ±0.02 decade): 회색 'Experiments' = 그림 2a 세 계열 · **Const_D NDB(하늘색) 1.27×10⁻¹⁴**(본문 1.3×10⁻¹⁴) · **D(x) DNN(빨강)** 8.3×10⁻¹⁴(x 0.5) · 6.4(0.6) · 4.5(0.7) · 2.4×10⁻¹⁴(0.8) · 1.7×10⁻¹⁴(0.85) · 8.3×10⁻¹⁵(0.9) · **최소 ≈7×10⁻¹⁶ @x 0.955** · 4.1×10⁻¹⁵(0.98) · 6.3×10⁻¹⁵(0.995) · **D(x) NDB(초록)** 2.2×10⁻¹³ · 1.65 · 1.15 · 6.5×10⁻¹⁴(0.5 · 0.6 · 0.7 · 0.8) · 최소 ≈2.5×10⁻¹⁵ @0.952 · 8.9×10⁻¹⁵(0.98). `[재현]` 빨강은 표 2 DNN 마디 사이를 **D 에 선형**으로 이은 꼴과 맞는다(0.6 · 0.7 예측 6.5 · 4.5×10⁻¹⁴ · 0.85 · 0.9 예측 1.68×10⁻¹⁴ · 8.7×10⁻¹⁵ — '꺾은선' ✅ · 로그 축에서 휜다) · 초록은 표 2 NDB 마디보다 **+8–10 %**(판독 폭 경계 — 같은 판독의 빨강은 −3 … 0 %). 모델 D(x) 는 회색 계열 어느 것과도 크기가 같지 않다 — **x 0.5 에서 Jang 의 ×4.7(DNN) · ×11(NDB) · Dokko 의 1/59 · 1/25** — 'based on the experimental measurements' 의 몫은 **모양(골 · 반등)** 이고 크기는 적합이다(`[해석]`). "vertical shift of whole profile towards higher values in logarithmic scale" ↔ 표 2 마디 비 NDB/DNN **2.35 · 2.40 · 4.00 · 2.00**(한 배수가 아니다 — D5).
(b) `[도표·화소]` NDB 끝 용량(3.08–3.14 V 띠) — **Const_D 30.3 · 93.0 · 114.0 / DNN D(x) 50.7 · 84.0 · 108.7 / NDB D(x) 72.8 · 95.6 · ≈114.7 / 실험 ≈78.7 · ≈95.9 · (≈114)**(42C · 8C · 0.8C) → 실험(그림 3b) 대비 상수 D **0.38 · 0.975 · 1.00** · DNN D(x) **0.64 · 0.88 · 0.96** · NDB D(x) **0.92 · 1.00 · 1.01**. ⇒ **8C · 0.8C 에서는 상수 D 가 DNN D(x) 보다 실험에 가깝다** — 본문 "deviation from the experimental data reduces, but still remains strong"(상수 → DNN D(x))은 42C 에서만 맞는 문장이다(`[해석]`). Q 5 의 42C 전압: 실험 3.767 · 초록 3.745 · 빨강 3.653 · 하늘색 **3.532 V**(−235 mV — 상수 D 는 x 0.5 쪽에서 D 가 NDB D(x) 의 1/15 라 시작부터 확산 과전압이 크다). ⚠ 색 대응이 그림 4(b) 캡션과 다르다(4b: 파랑 = DNN D · 5b: 빨강 = DNN D · 파랑 = 상수 D — D3).

## Fig. 6 — 농도 단면 · D 단면 (p. 115 · 봤다 · **수동** · 화소) ★★★ (c) · 판정 5 · D2 · D6 · G9

`[인쇄]` (a) DNN 'LiPO : 1500 nm · LCO : 320 nm' · t = 0.01 · 30.0 · 60 s · (b) NDB '**LiPON : 1000 nm · LCO : 1800 nm**'(→ D2 의 1.8 µm 쪽) · t = 0.01 · 20.0 · 40.0 s · 위 삽도 D(x) vs 위치(로그 · 위치 눈금 0). `[도표·화소]` 전해질(왼 축): 기준선 ≈2400(a) · ≈2400(b) ↔ `[재현]` δc₀ 2404 · 2480 · (a) 경계 c(0) · c(L) **30 s ≈2650 · ≈2100 · 60 s ≈2775 · ≈2015** · (b) c(0) ≈3680(20 s) · ≈4280(40 s) · c(L) ≈1000 · ≈500. LCO(오른 축) 평균: (a) 11,540 → 16,473 → 21,333 mol m⁻³ · (b) 24,156 → 31,202 → 37,855. `[재현]` LCO 평균 증가 × M × F ÷ t = **(a) 0.508 · 0.504 mA cm⁻²**(= 512 µA cm⁻² — 캡션 '51C' ✅) · **(b) 6.12 · 5.95 mA cm⁻²** ↔ 전해질 식 (9) 재풀이로 (b) 경계 c(0) 을 맞추려면 5.0–5.5 mA cm⁻²(§(c) 3) — (b) 의 전류는 '**comparable C-rate**' 뿐(G9) · 두 읽기가 ±10 % 로 갈리지만 둘 다 실험 최고(5 mA cm⁻²) 이상. 위 삽도: (a) 60 s 녹색 D 가 전극 안에서 골(≈1×10⁻¹⁵)을 지나는 비단조 · LCO 단면 꺾임('kink') ✅ 본문 · (b) 40 s 녹색은 전해질 쪽 ≈4×10⁻¹⁵ → 집전체 쪽 ≈8×10⁻¹⁴ 단조 ✅ 본문. ⚠ 본문 "the beginning (red), the middle (blue) and the end (**red**) of 51C-rate discharging" ↔ 캡션 · 그림 초록(D6).

## Table 1 — 문헌 확산계수 (p. 113 · 봤다 · 자동 · 텍스트 층 대조 ✅) ★★★ (b) · D9 · G13

[12] LiCoO₂ 10⁻¹⁴–10⁻¹² · [13] LiₓCoO₂ 4·10⁻¹⁵–3·10⁻¹³(0.45 < x < 0.75) · [14] 같은 범위 · 같은 구간 · [15] 1·10⁻¹⁶(x > 0.75) · [16] 1·10⁻¹⁵–1·10⁻¹³(0.45–0.75) · 1·10⁻¹⁶(0.75–0.95) · "No data reported"(x > 0.95) · [17] (003) · (101) 두 열 — PITT 1.6·10⁻¹⁷ · 1.8·10⁻¹⁵ · GITT 1.9·10⁻¹⁷ · 3.2·10⁻¹⁵ · EIS 1.6·10⁻¹⁴ · 6.0·10⁻¹³ · "Thin Film · 003 Film (0.32 μm) · 101 Film (1.60 μm)"(m² s⁻¹). `[재현]` 102호 digest 전사(Xie 2008 = [17] · 단위 cm² s⁻¹ · 막 (003) **0.31** · (003/104) 0.77 · (104) **1.35 µm**)와 대조: **EIS (104) 최대 6.0×10⁻⁹ · EIS (003) 최대 1.6×10⁻¹⁰ cm² s⁻¹ = 이 표 6.0·10⁻¹³ · 1.6·10⁻¹⁴ m² s⁻¹** ✅(×10⁻⁴) · 나머지 넷은 102호 범위 안(칸 대응은 102호 digest 에 전사 0) · ⚠ **배향 '(101)' ↔ Xie '(104)' · 두께 0.32 / 1.60 ↔ 0.31 / 1.35 µm**(D9).

## Table 2 — 매개변수 두 벌 (p. 114 · 봤다 · 자동 · 텍스트 층 대조 ✅) ★★★★ (b) · D4 · D7 · G1 · G2

| 이름 | 단위 | DNN | NDB | NDB/DNN |
|---|---|---|---|---|
| c₀ | mol m⁻³ | 60,100 | 62,000 | 1.03 |
| δ | – | 0.04 | 0.04 | 1 |
| k_d | s⁻¹ | 9.0·10⁻⁷ | 9.0·10⁻⁷ | 1 |
| k_r | m³ mol⁻¹ s⁻¹ | 9.0·10⁻⁹ | 9.0·10⁻⁹ | 1 |
| D_Li⁺ | "m s⁻²"(D7) | 6.0·10⁻¹⁵ | 22.0·10⁻¹⁵ | **3.67**(본문 "3.5 times" — D4) |
| D_n⁻ | "m s⁻²" | 6.0·10⁻¹⁷ | 22.0·10⁻¹⁷ | 3.67 |
| c_max(LiCoO₂) | mol m⁻³ | 23,300 | 48,760 | 2.09 |
| c⁰(LiCoO₂) | mol m⁻³ | 11,650 | 24,380 | 2.09(= c_max/2 둘 다) |
| α_LiCoO₂ | – | 0.6 | 0.6 | 1 |
| α_Li | – | 0.5 | 0.5 | 1 |
| D_Li(x) | "m s⁻²" | 0.50: 8.5·10⁻¹⁴ · 0.80: 2.5·10⁻¹⁴ · 0.95: 5.0·10⁻¹⁶ · 1.00: 7.0·10⁻¹⁵ | 2.0·10⁻¹³ · 6.0·10⁻¹⁴ · 2.0·10⁻¹⁵ · 1.4·10⁻¹⁴ | 2.35 · 2.40 · 4.00 · 2.00 |

표에 **없는 것**: k₁ˢ · k₂ˢ(식 5 · 6 — G2) · T · A · L · M(두께는 2절 본문 · 그림 6 에만) · E_eq(x)(그림 3 에만) · 각주 · 출처 0.

## 본문 서술과 어긋난 그림 · 표 (요약)

- 그림 4(b) — 캡션의 '파란 선(DNN D)' 이 그림에 없다(D3).
- 그림 5(b) — 상수 D 가 8C · 0.8C 에서 DNN D(x) 보다 실험에 가깝다 ↔ "deviation … reduces"(42C 만).
- 그림 5(a) — 초록 = 빨강의 '수직 이동' 이 아니다(마디 비 2.0–4.0 — D5).
- 그림 6(b) — 두께 1800 nm(↔ 3절 '3 μm' — D2) · 전류 미인쇄(G9).
- 그림 6 — 본문 '끝 = 빨강' ↔ 초록(D6).
- 그림 2 — 캡션 'EIS' ↔ 범례 PITT 한 계열(D8).
- 그림 1 — SEM 띠 비 ≈1.2 ↔ 모의 셀 0.21 · 1.8(D16).

---

# 절별 해체 (본문)

## 초록 (p. 111)

위 "수집 목적" 전사. 주장 다섯: ① 기존 모형의 고율 정확도 저하를 "overcome" ② 1D 모형(계면 전하이동 · 전해질 확산 · 이동 · 삽입 전극 확산) ③ "A new definition of diffusion coefficient as a function of concentration, based on the experimental measurements" ④ "fit … at low and high discharge currents up to 5 mA cm−2" ⑤ "cathode diffusion constant is a prime factor limiting the rate capability … in particular for ultrafast charging applications". ④ ↔ 결과 절(D1) · ⑤ 의 '충전' ↔ 충전 모의 0(D15).

## 1. Introduction (p. 111–112)

`[인쇄]` 동기: 시장 · 안전(액체 LIB 열폭주 [5]) → 고체 [6] · 계보: "Danilov, et al. [7] developed an isothermal model for thin-film solid-state batteries (TFSSB), which includes diffusion and migration of ions in the electrolyte, the charge-transfer kinetics at the electrolyte/electrode interface and Li-ion diffusion in the intercalation cathode. A number of other modeling approaches followed [8–11]." · 핵심 전제: "Since the limiting factor in the performance of lithium-ion batteries is reaching the maximum concentration of lithium on the electrolyte-electrode interface, choosing the right value for the diffusion coefficient is of great importance." · 문헌 값 폭: "reported values vary between 10−7 to 10−13 cm2 s−1 [12–17]. The broad range of reported values are, in addition to different material properties, due to the different measurement techniques and different assumptions for geometrical factors used in the calculations." — **측정 D 가 방법 · 기하 가정의 라벨이라는 102호 판정을 저자가 한 문장으로 인정** · 문헌 소개 Van der Ven [18](제일원리 · Li₀.₅CoO₂ 에서 최소) · Jang [13](PITT · "two batteries with LiCoO2 cathodes") · Dokko [12](단일 입자 임피던스) · Tang [19](EIS · PITT · PLD (003)) · Bouwman [20](배향 · RF a-axis ↔ PLD). 이 편의 위치: "In the present study, the same charge transport mechanisms are used as in [7], but a new concentration dependent diffusion coefficient is taken into account to make the model more accurate compared to older models simulating batteries. The results are compared with the experimental data reported in the open literatures and other numerical solutions." — 뒤 절반('other numerical solutions')은 지면에 0(D10).

## 1.1. Theoretical description (p. 112–114 · 그림 1 · 식 1–14 · 표 1 · 그림 2)

- 셀: "metallic lithium foil (Li) and lithium cobalt oxide (LiCoO2 or LTO) … separated by a solid state lithium phosphate (Li3PO4 or LIPO)"('LTO' 약칭 — D17).
- (1) LiCoO₂ ⇌ Li₁₋ₓCoO₂ + xLi⁺ + xe⁻(0 ≤ x ≤ 0.5 — 여기 x 는 탈리튬 양 · 뒤의 x = c/c_max 와 다른 뜻 · D17) · (2) Li ⇌ Li⁺ + e⁻ · (3) · (4) BV 둘 · (5) I⁰_LCO = F·A·k₁ˢ(c̄_CoO₂ c̄_Li⁺)^α(c̄_LiCoO₂)^(1−α) · (6) I⁰_Li = F·A·k₂ˢ(c̄_Li⁺)^α_Li(c̄_Li)^(1−α_Li) · "k₁ˢ = (k₁⁰)^(1−α)(k₋₁⁰)^α … are the standard rate constants … A is the electrode surface area [m2]" — **k₁ˢ · k₂ˢ 값은 어디에도 없다**(G2).
- SE: "The ionic conductivity of the LIPO(N)-based solid-state electrolyte is caused by transport of Li+ ions only. According to the presented solid-state electrolyte model [7] Li in LIPO(N) matrix may reside in two types of states" · (7) Li⁰ ⇌ Li⁺ + n⁻ — "uncompensated negative charges (n−), which are associated to the nearest non-bridging oxygen atoms (nBO)"(91호 이름 그대로 · 98호의 'vacancy' 이전) · 평형 c_Li⁺ = c_n⁻ = δc₀ · r = k_d c_Li⁰ − k_r c_Li⁺ c_n⁻ · (8) Nernst–Planck · 전기중성 → (9) ∂c/∂t = [2D_Li⁺D_n⁻/(D_Li⁺ + D_n⁻)]∂²c/∂y² + r · c(y,0) = δc₀ · 양끝 ∂c/∂y = I(t)/(2FAD_Li⁺) · (10) E(y,t) 닫힌 꼴 · (11) η_mt. `[재현·대수]` 이 편 값에서는 D_n⁻ = D_Li⁺/100 이라 "Li⁺ ions only" 와 지면 값이 맞는다(t₊ 0.990) — 91호(t₊ 0.15 · D_n⁻ > D_Li⁺)의 D15 모순이 이 편에서는 값으로 풀렸다.
- 양극: "Assuming complete screening of Li ions in the cobalt oxide electrode one can expect that the mass transport of Li-ions inside the positive electrode can be described by the standard diffusion equation" · (12) ∂c/∂t = ∂/∂y(D_Li(c)∂c/∂y) · 경계 D·∂c/∂y(L) = I/(FA) · ∂c/∂y(L+M) = 0 · "D_Li = D_Li(c_LiCoO2(y,t)) … assumed to be concentration-dependent" · x = c/c_max · (13) η_d = E_eq(xˢ) − E_eq(x̄) · (14) 합.
- "Eq. (14) takes into account three main processes … the charge transfer reaction at the surface of LiCoO2 **and metallic Li electrodes**" — 음극 BV 가 들어온 자리(91호 대비 신설 — D11).
- D(x): "As it follows from the definition of the battery overvoltage during the discharge process, especially at the end, the diffusion of lithium in the cathode is the main limiting factor" — 결론이 아니라 **출발 전제**로 인쇄 · "There is extensive experimental evidence that the diffusion coefficient in solid-state batteries is changing with the local State-of-Charge (SoC), see [12–17]"(그중 [17] Xie 2008 은 액체 3전극 셀 — 102호 digest · D14) · 표 1 · 그림 2a → "three SoC regions, namely for 0.5 ≤x < 0.8, 0.8 ≤x < 0.95 and x > 0.95" · 상: x > 0.95 phase I(Li-rich 고용체) · 0.5–0.8 phase II · 0.8–0.95 2상 공존 · "one can formulate a simple dependence of the DLi(x) on x as given in Fig. 2b, i.e. as piecewise linear function which remains continuous, but change the slope at the boundaries of the two-phase coexistence region at x = 0.8 and x = 0.95. … it assumes that in the two-phase coexistence region the diffusion coefficient is a weighted sum of the single-phase diffusion coefficients with the weights proportional to the amount of particular phase at given x. This formulation of DLi(x) was used to simulate the voltage discharge curves for the two datasets described in the previous section and for estimation of two sets of parameters"('previous section' 은 뒤의 2절 — 순서 오기) · 액체 선례 [21](Farkhondeh & Delacourt — LFP) · "programmed in COMSOL Multiphysics 4.4".

## 2. Experimental (p. 115)

`[인쇄]` "Experimental data used in this paper are represented by two datasets available in literature. The first one is a set of discharge curves from the original Danilov, et al. [7] paper, and further denoted as DNN. The discharge voltage curves were measured for Li/LIPO/LiCoO2 thin-film solid state batteries with electrolyte thickness of 1.5 μm and a cathode thickness of 320 nm. … The second dataset represents discharge curves from paper [22], further denoted as NDB, where a Li/LIPON/LiCoO2 cell was investigated with 3 μm of Li, 1 μm of LIPON and a cathode with thickness of 1.8 μm. Again, the equilibrium voltage curve and 3 voltage discharge curves with comparable C-rates are shown." — 절 이름은 'Experimental' 이지만 **자기 실험 0**(측정 장비 · 온도 · 프로토콜 서술 0).

## 3. Results and discussion (p. 115–116 · 그림 4–6)

- 그림 4: "green solid lines correspond to the model with concentration dependent diffusion coefficient estimated from the same DNN dataset (DNN column in Table 2) … The green solid lines correspond to model with all coefficients estimated from the same NDB dataset (NDB column in Table II)" — **같은 자료 추정**을 저자가 명시 · "**Values for the concentration dependent diffusion coefficient and constant diffusion coefficient are the result of optimization on rough grid.** For all models, one can see an almost perfect agreement between the experimental data and simulations with estimated parameters at low C-rates. However, this agreement declines towards very high discharge currents as Fig. 4b reveals."
- 그림 5: "The blue line illustrates average constant diffusion coefficient of 1.3·10−14 m2 s−1. … Strong deviation from experimental results is apparent. The red line … as it comes out of estimation on DNN dataset. … deviation from the experimental data reduces, but still remains strong. **Apparently, the same parameters for diffusion coefficient cannot be used simultaneously for both datasets.** The green line … corresponds to the vertical shift of whole profile towards higher values in logarithmic scale … That formulation provides best agreement with experimental data."
- 값 해석: "kd, kr, αLi, αLiCoO2 and δ are the same for both set of simulations, some other have only minor differences, for example c0 … 3.5 times larger values of DLi+ and Dn− for the case of NDB can be explained by better performance of LIPON in comparison with LIPO. Difference in values of DLi are related to the different deposition process of the LCO material used for NDB cells, which increased Li-ion diffusion. This is further supported by the increased capacity and density of the material which appear from changes in c_max and c⁰, i.e. a higher packing density and electro-activity obtained for NDB cells is favorable for Li-ion diffusion." — `[해석]` c_max 는 같은 자료의 용량 ÷ 두께에서 나온 수라(판정 8) D 해석의 '독립 지지' 가 되지 못한다.
- 그림 6: 농도 단면 · D 단면(위 그림 절) · "the concentration profiles in Figs. 6 nicely illustrate that the diffusion coefficient of the cathode material is a main factor limiting rate performance when going to thicker films (e.g. 3 μm) and/or higher C-rates. As can be seen from Fig. 4, the extracted capacity drops much more for the NDB cathode with 3 μm thickness (even with a higher diffusion constant as appears from the simulation fitting) … These observations are relevant for ultrafast charging application where > 5C is desired: the improved model enables a method to optimize thickness of the cathode end electrolyte for both rate performance and high energy density TFSSB."

## 4. Conclusions · 사사 (p. 116)

`[인쇄]` "A simulation approach for TFSSB had been developed which overcomes the drawback of available mathematical models, i.e. the inaccuracy of existing models at high currents. … It was shown that the model and estimation procedure work well for two available datasets, providing good agreement with the experiments even up to very high C-rates. Therefore, introducing the functional dependence of the diffusion coefficient on the lithium concentration have shown to be a valuable improvement of the mathematical models for Li-ion TFSSB." — '두 자료에서 잘 된다' 는 **묶음마다 따로 맞춘 결과**이고, 같은 D 로 두 자료를 함께 맞추는 것은 저자가 스스로 안 된다고 적었다(결과 절).

---

# ★ (a) 지목 명제 판정 — 무엇을 확장했나 · '개선' 의 지표와 비교 대상

## 1. 91호 → 이 편: 바뀐 것 (`[인쇄]` 이 편 ↔ 91호 digest 전사)

| 축 | 91호 Danilov 2011(DNN 자료의 원 편) | 이 편 DNN 열 | 바뀜 |
|---|---|---|---|
| 양극 수송 | 단일 Fick · D_Li **1.76×10⁻¹⁵ 상수**(적합) | 단일 Fick · **D_Li(x) 꺾은선 마디 넷** | ✅ 지면이 말한 확장 |
| 양극 동역학 | BV · α 0.6 적합 · k₁ˢ 5.1×10⁻⁶(인쇄 단위로 i₀ 재현 불가 — 91호 digest) | BV · α 0.6 · **k₁ˢ 인쇄 0** | 값 사라짐(G2) |
| 음극 동역학 | **무시**("for convenience") | **BV 신설**(식 4 · 6 · 14 · α_Li 0.5 · k₂ˢ 인쇄 0) | 지면 서술 0(D11) |
| 전해질 운반체 | Li⁺ + n⁻(nBO) · δ 0.18 · D_Li⁺ 0.90×10⁻¹⁵ · D_n⁻ 5.10×10⁻¹⁵ · t₊ 0.15 | 같은 구조 · **δ 0.04 · D_Li⁺ 6.0×10⁻¹⁵ · D_n⁻ 6.0×10⁻¹⁷ · t₊ 0.990** | 같은 자료에서 재적합 · 지면 서술 0 |
| 해리 속도 | k_r 0.90×10⁻⁸(인쇄 · 91호 그림은 ×100) · k_d 표 없음(유도) | k_r 9.0×10⁻⁹(= 91호 인쇄 값) · **k_d 9.0×10⁻⁷ 인쇄**(`[재현]` = k_r δ²c₀/(1−δ) = 9.015×10⁻⁷ ✅) | k_r 인쇄값 상속 · k_d 표에 올라옴 |
| 전해질 c₀ | a₀ 6.01×10⁴(NDP 측정 — 91호 각주 b) | **60,100**(각주 0) | 같은 값 · 출처 표기 사라짐 |
| 용량 스케일 | a_max 2.33×10⁴(측정 용량 ÷ 설계 부피 · Δx 0.5) | **23,300** | 같은 값 · 같은 관행 |
| 평형 곡선 | 네 율 회귀 외삽(91호 그림 3 녹색) | 그림 3a EMF(끝 ≈10.05 — 같은 곡선으로 읽힘) | 출처 서술 0(G3) |
| 자료 | 여섯 율(1.6–51.2C) | 셋(3.2 · 12.8 · 51.2C) | 율 선택 이유 0(G7) |
| "일치" | "good fits … including discharge curves with high C-rates"(51.2C 모형 끝 = 측정 73–78 % — 91호 digest 재풀이) | "almost perfect agreement … at low C-rates … declines towards very high"(51C 0.952 — `[도표·화소]`) | 고율 끝 용량 개선 ✅(교차 digest 대조) |

⇒ **같은 값 넷(c₀ · c_max · k_r · α_LCO) · 바뀐 값 셋(δ · D_Li⁺ · D_n⁻) · 함수로 바뀐 것 하나(D_Li) · 새 항 하나(음극 BV — α_Li 0.5) · 사라진 값 하나(k₁ˢ) · 표에 올라온 유도값 하나(k_d).** "the same charge transport mechanisms are used as in [7]" 는 식 구조로는 맞고(해리 SE · 단일 Fick), 값과 음극 항으로는 맞지 않는다.

## 2. '정확도 개선' — 무엇을 무엇과 비교했나

| 항목 | 이 편 지면 | 판정 |
|---|---|---|
| 지표 | 그림 겹침뿐 — `RMS` · `error` · `residu*` · `deviat*`(정량) 0 · "almost perfect" · "strong deviation" · "best agreement" | 지표 0 |
| 비교 대상 | NDB 에서 ① 상수 D 1.3×10⁻¹⁴("average" · "optimization on rough grid" — G8) ② DNN D(x) ③ NDB D(x) | 셋 다 같은 NDB 곡선 위 · ①은 자유도 1 · ③은 마디 넷 |
| DNN 에서의 비교 | 없음(91호 상수 D 모형 · 이 편 상수 D 모두 그림 0) | — |
| 표본 내 / 밖 | ③ = 같은 자료 적합 · ② = 다른 자료에서 옮긴 것(유일한 표본 밖 시험) → **실패**(저자 인쇄) | '예측' 아님 |
| 고율 | 51C(DNN) 0.952 · 42C(NDB) 0.919 · 평탄 −30 … −80 mV(42C) | 초록 '5 mA cm⁻² 까지 fit' ↔ 결과 절 'declines'(D1) |

## 3. 판정 — 지목 셋

- **98호**: 확장 내용 ✅(D_Li(x)) · 불완전(음극 BV · 전해질 재적합 생략) · "experimentally validated" ❌(표본 내 · 이전 시험 실패 · `valid*` 0).
- **100호**: 'D 를 Li 농도 함수로 맞춤' ✅ · '5 mA cm⁻² 고정확' 초록만(본문 · 그림 ❌) · 'COMSOL 정확도 검증' ❌.
- **104호**: [26] ✅ · [29] ❌ · 'improved accuracy … compared to experimental data' 부분(NDB 표본 내 · 지표 0) — 그리고 `[재현·가정]` 끝 용량 기준으로는 x 의존이 필요한 곳은 NDB 하나(§(c) 4).

---

# ★ (b) 표 2 출처 층위 · 26호 '문헌값' 계보 — 이 편이 원전인가

## 1. 표 2 행별 출처 층위 (`[인쇄]` 각주 0 → 우리 대조)

| # | 이름 | DNN | NDB | 층위(우리 대조 — 지면 근거 0) |
|---|---|---|---|---|
| 1 | c₀ | 60,100 | 62,000 | DNN = **91호 NDP 측정 a₀**(91호 각주 b) 재사용 · NDB 출처 미인쇄(G14) |
| 2 | δ | 0.04 | 0.04 | **적합 또는 고정**(두 열 같음 · G1) — 91호 0.18 과 다름 |
| 3 | k_d | 9.0×10⁻⁷ | 9.0×10⁻⁷ | **유도** — `[재현]` k_r δ²c₀/(1−δ) = 9.015×10⁻⁷(DNN ✅) · 9.30×10⁻⁷(NDB — 인쇄값은 −3 % · 평형 δ 0.0394 · D18) |
| 4 | k_r | 9.0×10⁻⁹ | 9.0×10⁻⁹ | **91호 인쇄값 재사용**(91호 그림은 ×100 으로만 재현 — 91호 digest §5) |
| 5 | D_Li⁺ | 6.0×10⁻¹⁵ | 22.0×10⁻¹⁵ | **적합**(본문 'LIPON 이 낫다' 로 해석) |
| 6 | D_n⁻ | 6.0×10⁻¹⁷ | 22.0×10⁻¹⁷ | **D_Li⁺/100 — 두 열 같은 비**(`[해석]` 비 고정으로 읽힘 · 독립 적합이면 두 열이 같은 비일 이유 0) |
| 7 | c_max | 23,300 | 48,760 | **유도(같은 자료 용량)** — `[재현]` EMF 끝 ÷ (F·M·0.5): 23,437(+0.6 %) · 48,546(−0.4 %) · DNN = 91호 a_max |
| 8 | c⁰ | 11,650 | 24,380 | **가정** x₀ = 0.5(= c_max/2 정확히) |
| 9 | α_LCO | 0.6 | 0.6 | **91호 적합값 재사용** |
| 10 | α_Li | 0.5 | 0.5 | **새 값 · 대칭 기본값**(근거 0) |
| 11 | D_Li(x) 마디 넷 | 표 위 | 표 위 | **적합**("optimization on rough grid") · 모양 = 그림 2a 문헌 계열(골 · 반등) · 크기 = 적합(그림 5a) |
| — | k₁ˢ · k₂ˢ | — | — | **인쇄 0**(G2) |
| — | T · A · L · M | — | — | 본문 두께만(L · M) · T · A 0 |
| — | E_eq(x) | 그림 3a | 그림 3b | DNN = 91호 외삽 EMF 로 읽힘 · NDB 출처 0(G3) |

⇒ **열한 이름 × 두 열 = 측정 재사용 1(c₀ DNN) · 앞 편 값 재사용 2(k_r · α_LCO) · 유도 2(k_d · c_max) · 가정 2(c⁰ · α_Li) · 적합 3–4(δ? · D_Li⁺ · D_Li(x) · D_n⁻ 는 비 고정으로 읽힘) · 인쇄 0 인 모형 입력 2(k₁ˢ · k₂ˢ).** 각주 · 출처 0 — 측정 · 재사용 · 적합이 한 표에 섞여 표시 없이 인쇄됐다.

## 2. 26호 '문헌값' · 98호 표 3 와 같은 이름끼리 (26 · 98호 열은 각 digest 전사)

| 이름(이 편 ↔ 98호 · 26호) | 이 편 DNN · NDB | 98호 표 3(= 26호 '문헌') | 26호 '최적' | 관계 |
|---|---|---|---|---|
| k_r | 9.0×10⁻⁹ · 9.0×10⁻⁹ | 8.00×10⁻⁷ | 8.40×10⁻⁷ | ×89(이 편 = 91호 인쇄값 · 98호 = 91호 그림 자릿수) |
| δ | 0.04 · 0.04 | 0.64 | 0.64 | ×16 |
| c₀ ↔ a₀ | 60,100 · 62,000 | 61,141 | 64,198 | 1.7 · 1.4 % 차 — **같은 값 아님** |
| D_Li⁺ ↔ D_M⁺ | 6.0 · 22.0 ×10⁻¹⁵ | 1.73×10⁻¹⁶ | 1.8165×10⁻¹⁶ | ×35 · ×127 |
| D_n⁻ | 6.0 · 22.0 ×10⁻¹⁷ | 5.69×10⁻¹⁶ | 5.9745×10⁻¹⁶ | ×0.11 · ×0.39 |
| c_max ↔ a^max_M⊕ | 23,300 · 48,760 | 3.22×10⁴ | 3.381×10⁴ | ×0.72 · ×1.51(셋 다 '같은 자료 용량 ÷ 두께') |
| D_Li(x) ↔ D⁰_M⊕ · β(x) | 마디 넷(8.5×10⁻¹⁴ …) | D⁰ 1.21×10⁻¹³ · β 0.65–0.025(그림 5) | 1.2705×10⁻¹³ | 다른 모형(98호 = 쌍극 · 공통 β) · 98호 D(x 0.5–0.6) ≈7.9×10⁻¹⁴ 와 이 편 DNN 8.5×10⁻¹⁴ 는 **다른 셀**의 같은 자릿수 |
| — ↔ D⁰_e⁻ | **없음**(단일 종 · "complete screening") | 5.06×10⁻¹³ | **5.24×10⁻³** | — |
| α_LCO · α_Li ↔ α | 0.6 · 0.5 | 0.5 · 0.5(사전 고정) | — | **α_Li 0.5 만 같음**(대칭 기본값) |
| k₁ˢ · k₂ˢ | 인쇄 0 | 1.53×10⁻¹¹ · 1.09×10⁻⁹ | 1.60×10⁻¹¹ · 1.1445×10⁻⁹ | 대조 불가 |

- **같은 값 1 / 10(α_Li 0.5)** — 98호는 이 편의 표를 상속하지 않았다. 26호 '×1.0500' 비율표의 기준은 98호 값이고(98호 digest §(a) 2), `D_e⁻` 10 자릿수 표류의 기준값 5.06×10⁻¹³ 도 98호 적합이다 — **이 편에는 그 매개변수가 없다.**
- 이 편 → 98호로 넘어간 것: **구조 하나**(양극 D 의 x 의존 + 2상 근거 — 98호 "variable ionic and electronic diffusion coefficients that depend on the lithium concentration inside the positive electrode" (iii) · [18] 인용) · 그리고 계보 공통 관행 둘(용량 스케일 = 같은 자료 용량 ÷ 두께 · 평형 곡선 = 같은 자료의 EMF). 모양은 달라졌다(98호 꺾임 0.75 · 0.92 · 반등 0 ↔ 이 편 0.80 · 0.95 · x 1.0 쪽 ×14 반등).
- **91호 → 이 편 → 98호 세 표의 전해질 δ: 0.18 → 0.04 → 0.64** · t₊: **0.15 → 0.99 → 0.233** — 같은 이름 · 같은 식 구조에서 자료(셀)와 모형 꼴에 따라 값이 자릿수로 움직인다. 이 편은 DNN 이 91호와 **같은 자료**라 셋 중 유일한 '같은 자료 두 표' 쌍을 만든다(§(c) 5).

## 3. 판정

**원장 "26호 '문헌값' 의 바로 앞 단계" ❌ · "98호와 같은 상용 셀" ❌.** 26호 '문헌값' · ×1.0500 · `D_e⁻` 의 원전은 98호(값)이고, 이 편은 계보에 **값이 아니라 D(x) 구조 하나**를 넘겼다. 이 편이 새로 시작한 것: ① **표에서 출처 표기가 사라짐**(91호 각주 a–c → 이 편 각주 0 — 측정 a₀ 가 무표시로 섞임) ② **BV 속도 상수의 인쇄 생략**(k₁ˢ · k₂ˢ 0 — 98호에서 회복) ③ **'일치' 의 비교 대상을 자유도 1 상수 D 로 둔 '개선' 서술**(104호가 '개선된 정확도' 로 옮김). 이어받은 것: 91호 인쇄 k_r(그림과 ×100 문제의 값) · 용량 맞춤 c_max · 같은 자료 EMF.

---

# ★ (c) 적합 · 재풀이 · 식별성 (Q4)

## 1. 어휘 (줄 끝 분철 복원 뒤 · 쪽 머리 · 바닥 제외 · 본문 = 제목 → 사사 · 초록 · 캡션 · 표 포함 \| 참고문헌 · NFKC 변화 0)

`identif*` 0 \| 0 · `uniqu*` 0 · `uncertain*` 0 · `confiden*` 0 · **`sensitiv*` 0** · `error` 0 · `±` 0 · `deviat*` 3(전부 정성 — "Strong deviation" · "deviation … reduces" · "deviations from the average value") · `residu*` 0 · `RMS` 0 · `least squares` 0 · `correlat*` 0 · `Fisher` · `Hessian` 0 · `degenera*` 0 · **`valid*` 0** · `verif*` 0 · `calibrat*` 0 · `fit*` 5(초록 "fit the available experimental data" · 그림 4 캡션 "DNN fit" · "fitted" · 그림 5 캡션 "best fit" · "simulation fitting") · `optimi*` 2("optimization on rough grid" · "optimize thickness") · `estimat*` 8 · `agree*` 4 · `accura*` 4(제목 · 초록 · 서론 "more accurate" · 결론 "inaccuracy") · `improv*` 6 · `predict*` 1(그림 5 캡션 "improvements in predicting") · `grid` 1 · `experiment*` 26 · `measur*` 12 · `literature` 3 · `contact` 0 · `pressure` · `MPa` · `stack` 0 · `degrad*` · `aging` · `cycl*` 0 · `capacity` 7 · `thickness` 5 · 'diffusion coefficient' 47 · `conductiv*` 1 · `resistan*` 0 · `impedance` 2 · `EIS` 4 · `GITT` 2 · `PITT` 4 · `COMSOL` 1 · `two-phase` 3 · `C-rate` 6 · `charging` 7(ultrafast charging 2 · charging times 1 · discharging 4) · `numerical` 1(약속된 비교) · `supplement*` · `appendix` · `video` 0.

## 2. 무엇에 · 어떻게 맞췄나

- **무엇에**: DNN 세 율 · NDB 세 율(그림 4) — 각 열을 자기 자료에. 충전 · 이완 · EIS 0.
- **어떻게**: "optimization on rough grid" — 그 밖 0(G1). 두 열에서 같은 다섯(k_d · k_r · α 둘 · δ)을 저자는 결과처럼 적는다("are the same for both set of simulations") — 그런데 k_r · α_LCO 는 91호 값 그대로 · k_d 는 그 둘과 δ 에서 유도 · α_Li 는 기본값이라, **'두 자료가 같은 값을 줬다' 가 아니라 '움직이지 않은 값' 일 가능성**이 크다(`[해석]` — G1 때문에 확정 안 함).
- **잔차의 흔적**(`[도표·화소]`): DNN 51C 모의 끝이 이르다(−4.8 %) · NDB 42C 모의 끝이 이르고(−8.1 %) 평탄이 낮다(−30 … −80 mV) — 부호 있는 잔차가 고율에서 같은 방향(모형이 고율 손실을 **많게** 본다 — 91호 digest 의 91호 잔차와 같은 방향 · 26호와 반대).

## 3. ★★★★ 재풀이 — 인쇄 표로 저자 그림을 다시 푼다 (`[재현]` · `[재현·가정]` · 스크립트 `scratchpad/assb5/k115/`)

**(i) 전해질(식 9)** — 유한체적 400 칸 · 암시적 Euler(Δt 0.02 s) · 반응 r = k_d(c₀ − c) − k_r c² 선형화 · 경계 ∂c/∂y = −j/(2FD_Li⁺) 양끝(방전) · T 298.15 K(가정). 같은 풀이로 91호 digest 의 91호 재풀이(k_r ×100: 15 · 30 · 50.4 · 64.9 s 전해질 합 −71.4 · −86.9 · −101.4 · −109.1 mV)를 **소수 첫째 자리까지 다시 낸다**(풀이 검증).

| 비교 | 그림 6 `[도표·화소]` | 표 2 그대로 | k_r(+k_d) ×100 |
|---|---|---|---|
| DNN 512 µA cm⁻² · 30 s · c(0) · c(L) | ≈2650 · ≈2100 | **2694 · 2114** | 2680 · 2126 |
| 60 s | ≈2775 · ≈2015 | **2817 · 1991** | 2781 · 2023 |
| NDB · 20 s(전류 가정 5.0 · 6.0 mA cm⁻²) | ≈3680 · ≈1000 | 3705 · 1255 \| 3950 · 1010 | — |
| NDB · 40 s | ≈4280 · ≈500 | 4218 · 741 \| 4566 · 393 | — |

- DNN: 인쇄 표 그대로 **≤2 %** — 그림 6a 는 표 2 로 닫힌다. **k_r 는 이 그림으로 갈리지 않는다**(인쇄 · ×100 둘 다 ≤2 % — 반응 이완 시간 1/(k_d + 2k_rδc₀) = **22,640 s**(인쇄) · 226 s(×100) 둘 다 방전 60 s 보다 길다) — 91호(이완 4,628 s ↔ 46 s)에서 ×100 이 그림을 갈랐던 것과 다르다.
- 경계층 두께 √(D_amb t): DNN 60 s 84 nm · NDB 40 s 132 nm(`[재현]` D_amb = 2D_Li⁺D_n⁻/(D_Li⁺ + D_n⁻) = 1.19 · 4.36 ×10⁻¹⁶ m² s⁻¹) — 그림 6 의 얇은 경계층 ✅.
- 전해질 손실(식 11 · 우리 분해 = 농도 몫 2t₋(RT/F)ln(c(L)/c(0)) + 옴 적분): **DNN 51C −140.4(0⁺) → −140.8 mV(64.9 s) · 농도 몫 −0.19 mV** · NDB 5 mA −241.6 → −264.6 mV(40 s) · 농도 −0.9 mV ↔ 91호 값(같은 풀이) −32.0 → −109.1 mV · 농도 −73.9 · 옴 −35.2(64.9 s). `[재현]` σ = (F²/RT)δc₀(D_Li⁺ + D_n⁻): DNN **5.47×10⁻⁷ S cm⁻¹ · R(1.5 µm) 274.2 Ω cm²** · NDB 2.07×10⁻⁶ · R(1.0 µm) 48.3 Ω cm² ↔ 91호 2.44×10⁻⁶ · 61.5 Ω cm²(91호 digest 와 같음).

**(ii) 양극(식 12) — 끝 용량** — 유한체적 120–160 칸 · 암시적 + Picard 셋 · 면 D = D(면 양쪽 평균 x) · D(x) = 표 2 마디 사이 D 에 선형(그림 5a 판독으로 확인) · x₀ 0.5 · 차단 = 표면 x ≥ 0.995(0.99 · 0.999 로 흔들어 폭) · 다른 과전압은 차단 시각에 넣지 않음(`[재현·가정]` — E_eq 가 x → 1 에서 3.9 → 3.0 V 로 ≈0.01 안에 떨어지는 그림 3 꼴에 기댄 근사).

| 경우 | 율 | 재풀이 끝(µAh cm⁻² · x_s 0.995 · [0.99–0.999]) | 그림 끝 `[도표·화소]` | 차 |
|---|---|---|---|---|
| DNN D(x) \| DNN | 51C · 13C · 3C | 8.68 [8.57–8.78] · 9.64 [9.46–9.76] · 9.84 [9.74–9.93] | 8.69 · 9.74 · 9.95(그림 4a) | −0.1 · −1.0 · −1.1 % |
| NDB D(x) \| NDB | 42C · 8C · 0.8C | 71.2 [70.5–71.3] · 94.5 [93.7–95.3] · 113.4 [111.6–114.8] | 72.6 · 95.4 · 113.7(그림 4b) · 72.8 · 95.6 · ≈114.7(5b) | −2.1 · −0.9 · −0.3 % |
| DNN D(x) \| NDB | 같은 셋 | 49.6 · 83.5 · 107.7 | 50.7 · 84.0 · 108.7(5b 빨강) | −2.2 · −0.6 · −0.9 % |
| 상수 1.3×10⁻¹⁴ \| NDB | 같은 셋 | 30.8 · 93.4 · 114.1 | 30.3 · 93.0 · 114.0(5b 하늘색) | +1.7 · +0.4 · +0.1 % |
| (91호) 상수 1.76×10⁻¹⁵ \| DNN | 51.2C | 7.13 [7.03–7.21] | 91호 digest: 재풀이 7.19 · 91호 그림 6.72 | 같은 대리 모형이 91호도 닫음 |

⇒ **그림 4 · 5 의 끝 용량 열둘(+ 91호 하나)이 양극 확산 하나로 ±2.2 % 안에서 닫힌다** — 저자 계산의 두께는 1.8 µm(3 µm 아님 — D2) · 마디 값 · c_max 는 표 2 그대로다. 그리고 **이 모형에서 끝 용량을 정하는 다른 항이 없다** — 전해질 · BV · 음극 매개변수는 평탄 전압만 움직인다.

**(iii) 못 하는 것**: 전압 곡선(k₁ˢ · k₂ˢ · E_eq(x) · T 미인쇄) · 평탄 과전압의 BV · η_d 몫 · 그림 6 의 양극 단면(차단 전 시각 · 전류는 맞음).

## 4. ★★★★ x 의존이 자료로 요구되는가 — 상수 D 쓸기 (`[재현·가정]` · 위 (ii) 대리 모형 · 끝 용량 분율 = 끝 ÷ c_max·M·F/2)

자료 분율(그림 3 끝 ÷ 9.99 · 117.6 µAh cm⁻²): DNN **0.914 · 0.979 · 0.998**(51C · 13C · 3C) · NDB **0.672 · 0.811 · 0.966**(42C · 8C · 0.8C).

| D | DNN 51C · 13C · 3C(x_s 0.995 / 0.999) | 최대 \|오차\| | NDB 42C · 8C · 0.8C | 최대 \|오차\| |
|---|---|---|---|---|
| 표 2 D(x) | 0.869/0.879 · 0.965/0.976 · 0.985/0.993 | **0.045 / 0.035** | 0.603/0.604 · 0.804/0.810 · 0.964/0.976 | **0.069 / 0.068** |
| 상수 4.5×10⁻¹⁵ | 0.882/0.890 · 0.963/0.971 · 0.983/0.991 | 0.032 / 0.024 | — | — |
| 상수 5.0×10⁻¹⁵ | 0.893/0.901 · 0.966/0.974 · 0.984/0.992 | 0.021 / 0.013 | — | — |
| 상수 5.5×10⁻¹⁵ | 0.902/0.910 · 0.968/0.976 · 0.984/0.992 | **0.013 / 0.005** | — | — |
| 상수 6.0×10⁻¹⁵ | 0.909/0.917 · 0.970/0.978 · 0.985/0.993 | **0.013 / 0.005** | — | — |
| 상수 1.3×10⁻¹⁴ | — | — | 0.262/0.266 · 0.794/0.802 · 0.970/0.978 | 0.410 / 0.406 |
| 상수 3.0×10⁻¹⁴ | — | — | 0.568/0.576 · 0.905/0.913 · 0.981/0.989 | 0.104 / 0.102 |
| 상수 4.0×10⁻¹⁴ | — | — | 0.672/0.679 · 0.926/0.934 · 0.984/0.992 | 0.115 / 0.123 |

⇒ `[재현·가정]` **DNN(320 nm): 상수 D ≈5.5–6×10⁻¹⁵ 가 표 2 의 D(x) 보다 세 율 끝 용량을 잘 낸다** — 91호(1.76×10⁻¹⁵)에서 이 편으로 온 고율 개선은 D 의 **크기**(×3)로도 설명되고, 끝 용량은 x 의존을 요구하지 않는다(전압 곡선은 비교 0). **NDB(1.8 µm): 어느 상수 D 도 세 율을 함께 못 낸다**(42C 를 맞추면 8C 가 +0.115) — x 의존(또는 율에 따라 달라지는 다른 기구)이 요구되는 곳은 두꺼운 셀 하나이고, D(x) 마디 넷으로도 42C 가 −0.068(−10 %) 남는다. ⚠ 한계: 끝 용량만 · 전압 곡선은 비교하지 않음(상수 D 는 x 0.5 쪽 확산 과전압을 키우는데 — 그림 5b Q 5 에서 −235 mV — 그것을 전해질 · BV 가 흡수할 수 있는지는 표 2 로 못 정함) · 이 대리 모형은 저자 그림 열둘을 ±2.2 % 로 다시 낸다는 것까지가 검증이다.

## 5. ★★★ 같은 자료 · 두 표 — 91호(2011) ↔ 이 편(2019) DNN

| 양 | 91호 표 II(91호 digest 전사) | 이 편 DNN 열 | 비 |
|---|---|---|---|
| δ | 0.18 | 0.04 | ×0.22 |
| D_Li⁺ | 0.90×10⁻¹⁵ | 6.0×10⁻¹⁵ | ×6.7 |
| D_n⁻ | 5.10×10⁻¹⁵ | 6.0×10⁻¹⁷ | **×0.012** |
| t₊ `[재현]` | 0.150 | 0.990 | — |
| σ `[재현]` | 2.44×10⁻⁶ S cm⁻¹ | 5.47×10⁻⁷ | ×0.22 |
| R_ohm(1.5 µm) | 61.5 Ω cm² | 274.2 Ω cm² | ×4.5 |
| 51.2C 전해질 손실(우리 같은 풀이 · 64.9 s) | −109.1 mV(농도 −73.9 · 옴 −35.2 · 시간에 따라 자람) | −140.8 mV(농도 −0.2 · 일정) | — |
| 평탄 과전압 중 전해질 몫(51.2C · 그림 3a 평탄 ≈183 mV) | ≈60 %(65 s 기준) | **≈77 %** | — |
| D_Li | 1.76×10⁻¹⁵ 상수 | 마디 넷 | — |
| 음극 BV | 0 | 있음(k₂ˢ 미인쇄) | — |
| "일치" | "good fits … including discharge curves with high C-rates" | "almost perfect agreement … at low C-rates" | 둘 다 |

- `[해석]` 같은 연구실이 같은 곡선을 두 모형으로 맞췄고, 모형 구조(D(x) · 음극 BV)가 바뀌자 전해질 값이 자릿수로 움직였으며(특히 D_n⁻ ×0.012 · t₊ 0.15 → 0.99 — '이원 해리 전해질의 농도 분극' 이 '거의 단일 이온 옴' 으로), 두 편 모두 '일치' 로 닫았다 ⇒ **전해질 넷의 값은 물질 상수가 아니라 모형 조건부 적합값**이다. 91호 digest §8 의 국소 CRB('전해질 넷 \|ρ\| ≥ 0.98 한 묶음 · 가장 약한 방향 δ↑ · D_Li⁺ · D_n⁻ · k_r ↓')와 견주면 이 편의 이동(ln 좌표 δ −1.50 · D_Li⁺ +1.90 · D_n⁻ −4.44 · k_r 0)은 그 약한 방향과 거의 직교(cos ≈ −0.08)다 — **같은 골짜기 위의 두 점이 아니라 다른 모형이 다른 곳에 앉은 것**이다(`[재현]` · CRB 는 91호 모형 위의 국소 계산).
- 그리고 91호 결론 "transport limitations in the solid-state electrolyte … at least half of the total overpotential"(91호 digest 전사)은 이 편 값에서도 성립하지만 기구가 다르다(농도 분극 → 옴).

## 6. ★★★ 묶음 (`[재현·대수]` — 인쇄 식 (9) · (11) · (12) 위)

- **양극**: u = c/c_max · s = (y − L)/M · τ = D_ref t/M² 로 쓰면 식 (12) 는 ∂u/∂τ = ∂/∂s(d(u)∂u/∂s) · 경계 d∂u/∂s = G ≡ j·M/(F·c_max·D_ref) · 집전체 0 — 끝 용량 분율 = 2Gτ_end(G) 로 **G 하나의 함수**. EMF 용량이 c_max·M 을 고정하므로 G = j·M²/(2Q_full·D_ref) ⇒ **자료가 정하는 것은 D_ref/M²** · NDB 두께 1.8 ↔ 3 µm 이면 D ×(3/1.8)² = **×2.78** · c_max ×0.6 로 같은 곡선.
- **고립 면적**: 활성 면적 분율 f(나머지는 전해질에 안 닿고 옆 수송 0) → 국소 전류 j/f · 용량 f·c_max·M — G 와 EMF 용량이 **c_max·f** 만 본다 ⇒ 1D 평면 모형에서 접촉(고립) 손실 ≡ c_max(LAM 형 용량 스케일) · BV 쪽은 k₁ˢ·f 곱(105호 A_f·i₀ 와 같은 자리 · 이 편 k₁ˢ 미인쇄).
- **전해질**: 식 (11) = (RT/F)·2t₋·ln(c(L)/c(0)) − (j·RT/(F²(D_Li⁺ + D_n⁻)))∫dy/c — t₋ = 0.010 이면 첫 항 → 0(−0.2 mV) · 둘째 항 ≈ j·L/σ · σ ∝ δ·c₀·(D_Li⁺ + D_n⁻) ⇒ **δ · c₀ · D_Li⁺ · D_n⁻ 넷이 σ 하나로**(그리고 D_n⁻/D_Li⁺ 는 경계층 두께 √(D_amb t) 로만 — 끝 용량 · 평탄에 안 보임).
- **직렬 합**: 평탄 과전압 = 전해질 옴(R 274 Ω cm²) + BV 둘(k₁ˢ · k₂ˢ 미인쇄) + η_d — DC 방전 하나로는 직렬 저항 합의 배분이 갈리지 않는다(98호가 DC + AC 를 함께 맞춘 동기 — "DC 만으로 맞추면 AC 가 안 맞는다" · 98호 digest 전사).

## 7. 판정 — Q4 0/115 · 백일곱 번째 성질

**백일곱 번째 성질 = "계보 가운데 편 — 같은 연구실의 같은 자료(91호 DNN 곡선)를 모형 구조를 바꿔(D(x) · 음극 BV) 다시 맞추자 전해질 값이 자릿수로 움직였는데(δ ×0.22 · D_n⁻ ×0.012 · t₊ 0.15 → 0.99 — 우리 대조) 두 표 모두 '일치' 로 닫혔고, 추정은 'optimization on rough grid' 한 문장(손실 · 잔차 · 불확실성 · 식별성 어휘 0)이며, '정확도 개선' 의 비교 대상은 같은 자료에 맞춘 자유도 1 의 상수 D 였고, 자료 사이 이전 시험 하나(DNN D(x) → NDB)는 저자 스스로 실패라 적었다 — 그리고 끝 용량 열둘은 양극 확산 하나(D(x)/M²)로 닫히는데 그 안에서 x 의존이 요구되는 것은 두꺼운 NDB 하나다(DNN 은 상수 D 로 더 잘 남 — 우리 재풀이)."** 매개변수 추정 ✅(한 문장) · 식별성 · 불확실성 계산 0 ⇒ **누적 0.5 그대로**. ★ 이 편이 Q4 에 주는 것은 계산이 아니라 **야생 표본 둘**: ① 같은 자료 두 표(모형 조건부 값) ② 지면 안 두께 불일치가 확산계수 해석에 ×2.78 로 번지는 D/M² 묶음.

---

# ★ (d) 물리 · 가정 · (주) 결론

1. **"cathode diffusion constant is a prime factor limiting the rate capability"** — (주) 다섯 칸: ① 무엇 = 차단 용량(끝 용량) — 평탄 과전압이 아니다 ② 시간 기준 = 3.0 V 차단 ③ 조건 = "thicker films (e.g. 3 μm) and/or higher C-rates" — 두께는 지면 안에서 1.8 ↔ 3 µm(D2) ④ 정의 · 문턱 0 ⑤ 손잡이 = D 하나(같은 묶음의 두께 · 율은 따로 흔들지 않음). `[재현]` 이 모형의 끝 용량은 양극 확산 하나로만 정해진다(§(c) 3 (ii)) → `[해석]` **'양극 확산이 한계' 는 끝 용량의 뜻으로는 이 모형 구성상 참**이고, 서론에서 이미 전제로 인쇄됐다("As it follows from the definition of the battery overvoltage … the diffusion of lithium in the cathode is the main limiting factor"). 평탄 과전압의 뜻으로는 이 편 자기 값에서 전해질 옴이 55–77 %(판정 7).
2. **전해질 = 거의 단일 이온** — 지면 "caused by transport of Li+ ions only" 와 값(t₊ 0.99)이 맞는다. 해리 SE 구조(식 7 · 9 · 10 — 원전은 101호 액체 이온쌍 · 91호 이식)는 남았지만 **D_n⁻ = D_Li⁺/100 이 그 이원 농도 분극을 값으로 껐다**(−0.2 mV) — 같은 이식 구조의 결론이 값에 따라 켜지고 꺼진다(104호 판정 8 · §3-b (혀) 의 반대쪽 표본).
3. **2상 근거의 D(x)** — 모양(골 · 반등)은 문헌 두 계열(Dokko · Tang)에서, 크기는 적합 · 경계 0.80 · 0.95 는 상도 서술("According to the literature …" — 상도 원전 인용 0). 98호의 같은 근거 β(x)는 경계 0.75 · 0.92 · 반등 0 — **같은 연구실 두 편이 같은 LCO 상도에 다른 꺾임을 썼다.**
4. **용량 스케일** — c_max = 같은 자료 용량 ÷ 두께(91 · 98호와 같은 관행) · "packing density and electro-activity" 해석은 그 수의 이름일 뿐 독립 측정이 아니다(판정 8).
5. **음극** — Li 금속 · BV 하나(α_Li 0.5 · k₂ˢ 미인쇄) · 농도 · 재고 · 형상 변화 0.
6. **충전 · 두께 최적화 결론** — 모의 0(D15).

---

# (e) 박막 ↔ 복합 전극 이식성 (`ASSB_TRANSFER_NOTE.md` 를 읽기만 · `[해석]`)

- 조밀 평면 박막(입자 · 공극 · 양극 안 SE 0)이라 복합 전극의 접촉 면적 손실 θ · 퍼콜레이션 · 응력 축이 **구조적으로 없다** — Q1 해당 없음의 이유는 '안 쟀다' 가 아니라 '자리가 없다' 다.
- 그러나 1D 평면 모형의 대수(§(c) 6)는 그대로 옮는다: 고립 면적 ≡ c_max(LAM 형) · 접촉 면적 ↔ k₁ˢ 곱 · 확산은 D/L² 로만. 복합 전극으로 가면 L 이 입자 반경 · 굴곡도와 섞여 이 묶음이 더 커진다(104호 L_eff ≈1 µm 와 같은 꼴).
- 우리 `degradation-degeneracy/` 물음("곡선이 맞는다 ≠ 분해가 맞다")에는 **같은 자료 두 표**(§(c) 5)가 가장 직접적인 야생 표본으로 읽힌다(`[해석]`)(우리 수치는 `degradation-degeneracy/docs/RESULTS*.md` 정본 — 옮기지 않음).

---

# (f) Q1–Q8 — 채움표 칸 (닻 카드 수집 지침)

| Q | 칸 | 이 편 |
|---|---|---|
| Q1 정량 | **해당 없음 — `θ(N)` 0/115** | 조밀 평면 박막 · 접촉 · 공극 · 입자 변수 0 · `contact` 0 · 열화 0 · 층 하나 `[재현·대수]`: 1D 평면 모형에서 고립(비접촉) 면적 분율 f 는 c_max·f(LAM 형 용량 스케일)로 정확히 흡수되고 BV 에서는 k₁ˢ·f 곱 — 이 편이 c_max 차(×2.09)를 "packing density and electro-activity" 로 읽은 자리가 그 한 수 |
| Q2 분리 관측 | **없다** | 관측 = 방전 곡선 셋 × 두 셀(문헌) · EMF(같은 자료) · EIS · 이완 · 기준극 · 두께 측정 0 · 그림 6 농도 단면은 모형 출력 |
| Q3 라벨 층위 | **칸 없음 · 층 하나** | "계보 가운데 편 — 표 2 두 열(각주 0) = 91호 측정 a₀ · 인쇄 k_r · α 0.6 재사용 + 같은 자료 용량 c_max + 유도 k_d + 기본값 α_Li 0.5 + 적합 D_Li⁺ · D_Li(x) 마디 넷 + 비 고정으로 읽히는 D_n⁻ = D_Li⁺/100 · k₁ˢ · k₂ˢ 인쇄 0 · 끝 용량 열둘 재풀이 폐합 ✅(1.8 µm) · 그림 6a 폐합 ✅ · 전압 곡선 재풀이 불가 · 같은 자료 두 표(91 ↔ 115) 전해질 ×0.012–×6.7 · 98호 표 3 과 같은 값 = α_Li 0.5 하나" |
| Q4 유일성 | **0/115 — 백일곱 번째 성질** | 위 §(c) 7 · `identif*` · `sensitiv*` · `uncertain*` · `valid*` 0 · "optimization on rough grid" 한 문장 · 누적 0.5 그대로 |
| Q5 Li-In | **해당 없음** | Li 금속 음극 · 기준극 0 · 음극 BV 신설(α_Li 0.5 · k₂ˢ 미인쇄) · 음극 전위 = Li⁺/Li 그대로 |
| Q6 압력 | **해당 없음** | `pressure` · `MPa` · `stack` 0 · 박막 |
| Q7 Li 재고 | **해당 없음** | Li 금속(NDB 3 µm — [22] 인용 값) · 재고 · dead Li 변수 0 · 한 방전 |
| Q8 OCP · 평형 곡선 | **층 하나** | 그림 3 EMF 둘 — DNN = 91호 율 외삽 EMF 로 읽힘(끝 ≈10.05 ↔ 10.10) · NDB 출처 미인쇄 · E_eq(x) 함수형 인쇄 0 · x 축 = 같은 자료 용량으로 정한 c_max · D(x) 꺾임(0.80 · 0.95)은 상도 서술 · EMF 평탄(DNN Q ≈6–9.8 = x ≈0.80–0.99)과 D 골(0.95)의 대응 서술 0 |

**누적 ≈20.0 → ≈20.0 (새 칸 0).**

---

# 재현 (`[재현]` — 인쇄 수치 · 식 · 래스터 그림 화소로 우리가 계산 · 가정 표시 · 스크립트는 `scratchpad/assb5/k115/` 에만)

| # | 대상 | 방법 | 결과 |
|---|---|---|---|
| R1 | 표 2 DNN ↔ 91호 표 II | 91호 digest 전사 대조 | 같은 값 넷(c₀ 60,100 · c_max 23,300 · k_r 9.0×10⁻⁹ · α_LCO 0.6) · 바뀐 셋(δ ×0.22 · D_Li⁺ ×6.7 · D_n⁻ ×0.012) · D_Li 상수 → 마디 넷 · 음극 BV 신설 · k₁ˢ 사라짐 |
| R2 | k_d 평형 관계 | k_r δ²c₀/(1−δ) | DNN 9.015×10⁻⁷ ✅ · NDB 9.30×10⁻⁷(인쇄 9.0 — −3 % · 평형 δ 0.0394) |
| R3 | 전도도 · 운반수 | σ = (F²/RT)δc₀(D₊ + D₋) · t₊ = D₊/(D₊ + D₋) | DNN 5.47×10⁻⁷ S cm⁻¹ · 274.2 Ω cm² · NDB 2.07×10⁻⁶ · 48.3 Ω cm² · t₊ 0.990 둘 다 · NDB/DNN σ ×3.78 · 91호 2.44×10⁻⁶ · 61.5 Ω cm² · t₊ 0.150 |
| R4 | 전해질 식 (9) | FV 400 · 암시적 Euler · T 298.15 K | DNN 30 · 60 s 2694/2114 · 2817/1991 ↔ 그림 ≤2 % · k_r ×100 2680/2126 · 2781/2023 · NDB 5.0 mA 3705/1255 · 4218/741 · 6.0 mA 3950/1010 · 4566/393 · 91호(×100) 재풀이 −71.4 · −86.9 · −101.4 · −109.1 mV ✅(91호 digest 와 같음) |
| R5 | 그림 6 LCO 평균 → 전류 | Δc̄·M·F/t | DNN 0.508 · 0.504 mA cm⁻²(= 512 µA ✅) · NDB 6.12 · 5.95 mA cm⁻² |
| R6 | 전해질 손실 | 식 (11) 분해 | DNN 51C −140.4 → −140.8 mV(농도 −0.19) · NDB 5 mA −241.6 → −264.6(40 s · 농도 −0.9) · 91호 값 −32.0 → −109.1(농도 −73.9 · 옴 −35.2) |
| R7 | 평탄 과전압 몫 | 그림 3 EMF − 곡선 ↔ R6 | DNN 51C 173–188 mV · 전해질 77 % · NDB 42C 382–405 mV · ≈65 % · 8C 88 mV · 55 % · DNN 3C ≈12 mV(판독 ±3 mV) · 8.8 mV(≈73 %) |
| R8 | 양극 끝 용량 열둘 | FV · 표면 x 0.995 차단(0.99–0.999) | §(c) 3 (ii) 표 — 그림 4 · 5 와 −2.2 … +1.7 % · 91호 51.2C 7.13 ↔ 7.19 |
| R9 | 상수 D 쓸기 | 같은 대리 모형 | DNN 상수 5.5–6×10⁻¹⁵ 최대 오차 0.005–0.013 ↔ D(x) 0.035–0.045 · NDB 상수 최선 ≈0.10 ↔ D(x) 0.068 |
| R10 | c_max ↔ 용량 | EMF 끝 ÷ (F·M·0.5) | DNN 23,437(+0.6 %) · NDB 48,546(−0.4 %) · `[재현·외부 값]` 격자 51.6 kmol m⁻³ 의 45 · 94.5 % |
| R11 | 묶음 | 무차원화(§(c) 6) | 끝 용량 분율 = f(G) · G = j·M/(F·c_max·D) · NDB 3 µm 이면 D ×2.78 · c_max ×0.6 · 고립 면적 f ≡ c_max·f |
| R12 | 마디 비 | 표 2 | NDB/DNN D_Li 2.35 · 2.40 · 4.00 · 2.00 · D_Li⁺ · D_n⁻ 3.67(본문 3.5) |
| R13 | 확산 시간 | M²/D | DNN x 0.5 1.2 s · 0.8 4.1 s · 0.95 205 s · 1.0 14.6 s · NDB 16.2 · 54 · 1620 · 231 s ↔ 51C ≈70 s · 42C ≈84 s 방전 |
| R14 | 그림 5a 꺾은선 | 로그 축 화소 ↔ 마디 사이 D 선형 | 빨강 −3 … 0 % · 초록 +8–10 % · 최소 x 0.955 · 0.952 |
| R15 | 그림 1 SEM 띠 비 | 열 평균 밝기 | LIPO ≈228 · LCO ≈264 px · ≈1.2 ↔ 0.21 · 1.8 |
| R16 | 율 이름표 | I ÷ Q_EMF | 3.18 · 12.7 · 50.9 → 3 · 13 · 51(반올림) ↔ 0.85 · 8.5 · 42.7 → 0.8 · 8 · 42(버림) |
| R17 | 경계층 · 이완 | √(D_amb t) · 1/(k_d + 2k_rδc₀) | 84 · 132 nm · 22,640 s(인쇄) · 226 s(×100) |
| R18 | 91 → 115 이동 ↔ 91호 CRB 약한 방향 | ln 좌표 내적 | cos ≈ −0.08(거의 직교) |
| R19 | 일정 | 인쇄 날짜 | 투고 → 수락 155 일 · → 온라인 169 일 |

---

# 참고문헌 22 번호 — 우리 축에 닿는 것 (번호는 PDF p. 116 목록에서 직접 확인 · 빠진 번호 0)

| 번호 | 서지(`[인쇄]`) | 이 편에서의 쓰임 | 우리 축 · 위키 |
|---|---|---|---|
| [7] | D. Danilov, R.A.H. Niessen, P.H.L. Notten, *J. Electrochem. Soc.* 158 (2011) A215–A222 | 모형 원형 · DNN 자료 | **= 91호** — 교차 |
| [8] | S.D. Fabre, D. Guy-Bouyssou, P. Bouillon, F. Le Cras, C. Delacourt, *J. Electrochem. Soc.* 159 (2012) A104–A115 | "A number of other modeling approaches followed [8–11]" | 원장 L232(98 · 99 · 100 · 103 · 104 · 106 = 6) · **배경 목록 인용이라 재지목 안 함**(☆) |
| [9] | M. Jagannathan, K.S.R. Chandran, K.S. Ravi, *J. Power Sources* 247 (2014) 667–675 | 같은 목록 | 행 0 · ☆ |
| [10] | R. Chandrasekaran, *J. Power Sources* 262 (2014) 501–513 | 같은 목록 | 행 0 · ☆ |
| [11] | R. Behrou, K. Maute, *J. Electrochem. Soc.* 164 (12) (2017) A2573–A2589 | 같은 목록 | 98호 ☆ · 행 0 |
| [12] | K. Dokko, M. Mohamedi, Y. Fujita, T. Itoh, M. Nishizawa, M. Umeda, I. Uchida, *J. Electrochem. Soc.* 148 (5) (2001) A422–A426 | 표 1 · **그림 2a 'Dokko (EIS) particle' — D(x) 골 · 반등 모양의 주 근거** | 행 0 · ★ 새 |
| [13] | Y. Jang, B.J. Neudecker, N.J. Dudney, *Electrochem. Solid-State Lett.* 4 (6) (2001) A74–A77 | 표 1 · 그림 2a 'Jang (PITT) RF film (110)' · "two batteries with LiCoO2 cathodes, using PITT" | 원장 L267(99 · 102 · 107 = 3) · 재지목 → 4(그림 2a · 표 1 의 구체적 쓰임) · G13(배향 이름표) |
| [14] · [15] | J. Barker, R. Pynenburg, R. Koksbang, M.Y. Saidi, *Electrochim. Acta* 41 (15) (1996) 2481–2488 · M. Okubo, E. Hosono, T. Kudo, H.S. Zhou, I. Honma, *Solid State Ionics* 180 (2009) 612–615 | 표 1 행 | 행 0 · ☆(원장 Okubo 2007 · 2008 행과 다른 편) |
| [16] | N.J. Dudney, Y. Jang, *J. Power Sources* 119–121 (2003) 300–304 | 표 1 행(x 구간 셋 · x > 0.95 'No data') | 행 0 · ☆(같은 ORNL 계열) |
| [17] | J. Xie, N. Imanishi, T. Matsumura, O. Yamamoto, *Solid State Ionics* 179 (9) (2008) 362–370 | 표 1 (003) · (101) 행 | **= 102호**(저자 목록 넷만 인쇄 — 102호 digest 는 여섯 · Hirano · Takeda 빠짐) — 교차 · D9 |
| [18] | A. Van der Ven, G. Ceder, *Electrochem. Solid-State Lett.* 3 (7) (2000) 301–304 | 제일원리 확산 · Li₀.₅ 최소 | 행 0 · ☆ |
| [19] | S.B. Tang, M.O. Lai, L. Lu, *J. Alloys Compd.* 449 (2008) 300–303 | 그림 2a 'Tang (EIS) PLD film (003)' — 골 · 반등 둘째 근거 | 102호 ☆ · 행 0 · ☆ |
| [20] | P.J. Bouwman, B.A. Boukamp, H.J.M. Bouwmeester, P.H.L. Notten, *J. Electrochem. Soc.* 149 (2002) A699 | 서론 배경(배향 · RF a-axis ↔ PLD) | 원장 L292(102 = 1) · **서론 배경 인용이라 재지목 안 함**(☆) |
| [21] | M. Farkhondeh, C. Delacourt, *J. Electrochem. Soc.* 159 (2) (2012) A177–A192 | 액체 LFP 농도 의존 D 선례 | 행 0 · ☆ |
| [22] | B.J. Neudecker, N.J. Dudney, J.B. Bates, *J. Electrochem. Soc.* 147 (2) (2000) 517–523 | **NDB 자료 전부**(곡선 · 셀 치수) | 행 0 · **★★ 새**(제목 미인쇄) |
| [1]–[6] | Tarascon & Armand 2001 *Nature* · **Ramadesigan … Subramanian 2012 *JES* 159, R31** · Nazri & Pistoia 2009(Ch. 1) · 시장 보고서 · Spotnitz & Franklin 2003 *JPS* · Takada 2013 *Acta Mater.* 61, 759 | 서론 일반 | [2] = 원장 L372(★★ · 27 = 1) — 이 편 쓰임은 일반 서론 문장 하나라 ☆(지목 칸 그대로) · 나머지 행 0 |

⚠ 목록 오기 · 특이: [3] "G.A. Nazri, G. Pistoia (Eds.), Manthiram, Lithium Batteries…"(편자 · 장 저자 뒤섞임) · [17] 저자 넷만(102호 원문은 여섯 — 102호 digest 전사) · 제목 인쇄 0(Elsevier 형식 — 전 항목).

**5차 묶음 13 편과의 관계**: 이 편은 13 편 중 **아무것도 인용하지 않는다**(22 번호 전수 대조 — [6] Takada 2013 *Acta Mater.* 은 #4 Takada 1996 *SSI* 와 다른 편). **흡수된 편(교차)**: [7] = 91호 · [17] = 102호.

---

# 인용 대조

## 1. 이 편을 지목 · 인용한 우리 digest — 그 쓰임 ↔ 이 편이 실제로 주는 것

| digest | 쓰임(digest 전사) | 이 편 | 판정 |
|---|---|---|---|
| 98호 `raijmakers2020_thin-film-assb-model-double-layer-dc-ac-joint-fit` :182 · :421 · :535 · :683 | [18] "extended with an ionic concentration-dependent diffusion coefficient in the positive electrode … experimentally validated" · 후속 ★★★ "농도 의존 D 를 처음 넣은 편 · 그 매개변수 표 · 자료(같은 상용 셀인가) · 적합 방법 — 26호 '문헌값' 계보의 바로 앞 단계" | D(x) ✅ · 음극 BV · 전해질 재적합 서술 0 · validated ❌ · 상용 셀 ❌ · 26호 앞 단계 ❌ · 적합 = 한 문장 | 확장 ✅ · 나머지 ❌(중심 표 1–3) |
| 100호 `deng2021_assb-reduced-order-model-pade-polynomial` :185 · :201 · :335 · :415 · :568 | [8] "fit the diffusion coefficient as a function of lithium-ion concentration … high accuracy even at a current density of 5 mA/cm2" · 'COMSOL 정확도' 묶음 첫째 · 후속 ★★★ "이 편이 ROM 에 쓰지 않은 개선(고율 끝 용량 결손 — 그림 9)" | D(x) ✅ · 5 mA 고정확은 초록만 · COMSOL 검증 0 · 고율 끝 용량 개선은 D 크기로 설명(§(c) 4) | 부분 · 부분 · ❌ |
| 104호 `ansah2021_assb-fem-parametric-sweep-thickness-diffusivity` :213 · :413 · :561 | [26] "[26, 29] … improved accuracy … [26]" · 후속 ★★ | [26] ✅ · [29] ❌ · 개선 = NDB 표본 내 · 지표 0 | 부분 |
| 37호 `li2024_assb-composite-cathode-model-contact-area-edl` :116 | "Kazemi [13] adopt a strategy of calibrating the diffusion coefficient"(어휘 표 · 서지 미전사) | 셀마다 D(x) 재적합 ✅ · 율마다 ❌ | 부분 · 같은 편 확정 0 |
| 12호 `kouhestani2022_phm-solid-state-batteries-perspective` :202 · :387 | 표 1 'Mathematical model [65,72,78]' — "Kazemi 박막 정확도"(12호 해석) · :202 "Kodama [71] … [72]와 일치" | 순방향 + 적합 ✅ · :202 는 Kodama [71] 에 대한 Kouhestani 의 서술 — 이 편 지면에 Kodama · 응력 해석 0(무엇과 '일치' 인지 이 편으로 확인 불가) | ✅(순방향) · [72] = 이 편인지 미확인 |
| 105호 `barai2021_…` :561 | 5차 묶음 관계 문장 — 인용 0 | — | 셈 밖 |
| 116호 예정(5차 묶음 #12 Shao 2022 *Energy* — 이 digest 봉인 때 위키 반영 전 · 그 초안 전사) [40] | "no additional electrochemical reaction occurs in SE [36,40]" · 재지목 안 함(교차) | 그 문장은 이 편 지면에 0 · SE 안 반응 = 해리 · 재결합(식 7 · 9) 하나 · 전기화학 부반응 항 0 은 모형 구성으로만 | 부분(구성 ✅ · 문장 ❌) |

## 2. 이 편이 인용한 우리 digest

- **91호** `danilov2011_thin-film-assb-model-weak-electrolyte-parameter-fit` — [7] — 모형 원형 + DNN 자료. 91호 판정이 이 편에서 어떻게 됐나: ① 인쇄 k_r(그림과 ×100)는 그대로 재사용 — 이 편 그림 6a 는 k_r 를 가르지 못한다 ② k₁ˢ 단위 관례 문제는 값이 사라져 대조 불가 ③ 51.2C 끝 용량 결손(73–78 %)은 D 크기 변화로 95 % 로 줄었다 ④ 이원 전해질 가정의 몫(≈71 %)은 t₊ 0.99 로 꺼졌다 ⑤ 국소 CRB 의 '전해질 넷 한 묶음' 은 같은 자료 두 표로 야생 대조를 얻었다(다른 모형 — §(c) 5).
- **102호** `xie2008_lco-thin-film-orientation-diffusion-gitt-pitt-eis` — [17] — 표 1 의 (003) · (101) 행. 102호 판정(측정 D 는 방법 · 기하 라벨 · 액체 셀)은 이 편 서론의 "different measurement techniques and different assumptions for geometrical factors" 한 문장과 맞고, 이 편은 그 폭을 모양 근거로만 썼다 · 이름표 (101) · 0.32 / 1.60 µm 는 102호 원문 값((104) · 0.31 / 1.35 µm)과 다르다(D9).

---

# 곱 축퇴 처방 — 아흔여덟 번째 적용 ([[assb-lampe-contact-product-degeneracy]])

## 입력 점검

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | EIS · 이중층 · 축전기 0 · 저항 = 전해질 옴 + BV 둘(k 미인쇄) | ❌ |
| **2단계** (18 · 25호) | + 면적을 아는 대조군 | A 미인쇄 · 두 셀(320 nm · 1.8 µm)은 다른 연구실 · 다른 SE · 따로 맞춤 | ❌ |
| **3단계-a** (19호) | `Ea` | T 미인쇄 · 한 온도 | ❌ |
| **3단계-b** (19호) | `C` 물리 상한 | — | ❌ |
| **4단계** (20 · 24호) | 시간 영역 | 정전류 방전만 · 휴지 · 이완 0 | ❌ |
| 율 스윕 · `J^T J` 줄 | — | 셀마다 세 율(×16 · ×50) + 두 두께 — **자료 위의 율 · 두께 쓸기** · 그러나 셀마다 따로 맞춤 · J^T J 0 | 부분 |

### ★ 곱 문장 — 셋 (`[인쇄]` → `[재현·대수]` → `[해석]`)

- ① `[재현·대수]` **확산 · 두께 · 용량 스케일** — 끝 용량 분율은 G = j·M/(F·c_max·D) 하나의 함수이고 c_max·M 은 EMF 용량이 고정한다 ⇒ 자료가 정하는 것은 **D/M²** 와 **c_max·M**. 이 편 지면 안에서 NDB 두께가 1.8 ↔ 3 µm 로 갈려(D2) D ×2.78 · c_max ×0.6 의 폭이 그대로 열려 있고, 저자의 물리 해석 둘("different deposition process … increased Li-ion diffusion" · "a higher packing density and electro-activity")이 모두 그 두께 위에 선다. 우리 재풀이는 저자 계산이 1.8 µm 였다는 것까지만 정한다(끝 용량 열둘 폐합).
- ② `[재현·대수]` **고립 면적 ≡ 용량 스케일(LAM 형)** — 1D 평면 모형에서 전해질에 안 닿는 면적 분율 f 는 c_max·f 로 정확히 흡수되고, BV 쪽에서는 k₁ˢ·f(105호 A_f·i₀ 와 같은 곱)로 들어간다 ⇒ 이 편의 c_max 차 ×2.09(45 % ↔ 94.5 % 격자 밀도)는 '밀도' · '전기 활성' · '접촉 면적' 어느 이름으로도 같은 곡선이다 — 카드 물음(`LAM_PE` ↔ 접촉 손실)의 박막판 축퇴.
- ③ `[재현]` **전해질 넷 → σ 하나 · 직렬 합** — t₊ 0.990 에서 농도 몫 −0.2 mV · 손실 = j·L/σ — δ · c₀ · D_Li⁺ · D_n⁻ 가 σ 한 수로 접히고, σ 는 BV 둘(k₁ˢ · k₂ˢ — 미인쇄)과 평탄 과전압의 직렬 합을 나눈다. 같은 곡선에 91호는 σ 2.44×10⁻⁶ + 이원 농도 분극, 이 편은 σ 5.47×10⁻⁷ + 단일 이온 옴을 앉혔다(같은 자료 두 표 — 51.2C 전해질 −109 ↔ −141 mV).

### ⚠ 이것이 곱을 푼 것은 아니다

- 모형 편 · 자료는 문헌 곡선 · 저자 구현 미공개 — 위는 인쇄 식 위 대수 · 양극 · 전해질 부분계 재풀이(표 2 값) · 래스터 화소 판독이다. 전압 곡선은 k₁ˢ · k₂ˢ · E_eq 미인쇄로 풀지 않았다.
- 후보 메모(처방 표로 올리지 않음 · 결정 대기): **"같은 자료를 같은 연구실이 다른 모형 구조로 다시 맞춘 표가 있으면, 같은 이름 값의 비와 모형이 실제로 보는 조합(σ · t₊ · D/L² · 용량 스케일)의 비를 나란히 적는다 — 이름 값이 자릿수로 움직이고 조합이 덜 움직이면 그 이름은 식별되지 않은 것으로 읽는다(115호: DNN 전해질 ×0.012–×6.7 · σ ×0.22 · t₊ 0.15 → 0.99)"**. 새 줄 0.

---

# 보류 결정 (가)–(규) — 이 편이 주는 근거 (결정 안 함 · 2026-11-17 사용자 결정 — 5차 묶음 뒤 일괄)

**근거(강)**

- **(세)** 인쇄 매개변수 표의 재풀이 폐합 — 표 2 + 2절 두께로 끝 용량 열둘(−2.2 … +1.7 %) · 그림 6a 전해질(≤2 %) · LCO 평균(≤2 %) ✅ · k₁ˢ · k₂ˢ · E_eq · T 미인쇄라 전압 곡선 불가 · 그림 6b 전류 미인쇄 · 계보 '첫 표'(91호)의 인쇄 k_r 를 재사용하면서 그 값을 가르지 못하는 그림만 냄.
- **(여)** 표에 적힌 값 ↔ 계산에 쓰인 값 · 출처 번호 — 각주 0 표에 91호 측정 a₀ · 인쇄 k_r · α 재사용이 무표시 · 표 1 [17] 행 이름표(배향 (101) · 두께 0.32 / 1.60 µm) ↔ 102호 원문 · NDB 두께 1.8 ↔ 3 µm(저자 계산 = 1.8 — 재풀이로 확정).
- **(제)** 모형 '일치' 의 율별 끝 용량 잔차 — DNN 0.998 · 0.996 · **0.952** · NDB 1.00 · 1.00 · **0.919** · 평탄 −30 … −80 mV(42C) · 91호(51.2C 73–78 %)와 비교 가능 · 초록 · 결론의 '고율까지 일치' ↔ 결과 절 'declines'.
- **(햐)** '계산 ↔ 실험 일치' 의 측정 몫 · 비교 축 — 자료 = 문헌 곡선 · 비교 = 같은 자료 적합 · 비교 대상 = 자유도 1 상수 D · 지표 0.
- **(며)** 'validated' 의 자료 층위 — 98호 'experimentally validated' 의 원전에 `valid*` 0 · 표본 내 적합 · 이전 시험 실패(저자 인쇄).
- **(텨)** '실험 검증' 그림의 자료 경로 — DNN = 91호 셀 곡선(같은 연구실 · 율 셋 선택) · NDB = [22](ORNL — 공저자 Dudney) 곡선 · 옮긴 방법 · NDB EMF 출처 0.
- **(탸)** 요약 수치 ↔ 표 · 그림 — 초록 '5 mA cm⁻² 까지 fit' ↔ 42C 0.919 · '3.5 times' ↔ 3.67 · '3 μm' ↔ 1.8 µm · 'vertical shift' ↔ 마디 비 2.0–4.0 · 'ultrafast charging' ↔ 충전 모의 0.
- **(냐)** 모형 결론의 회고 인용 — 98(validated) · 100(5 mA 고정확 · COMSOL 검증) · 104(improved accuracy · [29]) · 37(calibrating) · 12([72] 박막 정확도) 다섯 편이 조건(표본 내 · 이전 실패 · 고율 저하 · 지표 0)을 떼고 옮김.
- **(주)** 'X-limited' 명제 — "cathode diffusion constant is a prime factor limiting the rate capability": ① 끝 용량 ② 3.0 V ③ 두께(1.8 ↔ 3 µm) · 고율 ④ 문턱 0 ⑤ D 하나 — 끝 용량은 이 모형에서 양극 확산만 보므로(`[재현]`) 구성상 참(`[해석]`) · 평탄 과전압은 전해질 55–77 % · 서론에서 전제로 인쇄.
- **(뎌)** '문헌값 일치' 의 자료 독립성 — D(x) 'based on the experimental measurements' 의 몫은 모양뿐(크기 = 적합 · x 0.5 에서 Jang ×4.7–11 · Dokko 1/25–1/59) · 같은 ORNL 계열 PITT(Jang [13])의 ×11 을 NDB 적합값으로 둠 · c_max 를 D 해석의 '지지' 로 씀(같은 자료 용량).
- **(먀)** 한 편을 다른 편 현상의 원전으로 지목할 때의 기구 층위 — 원장 '26호 문헌값의 바로 앞 단계' ❌(값 상속 0 · D_e⁻ 없음 · 구조 하나만 98호로).
- **(료)** 측정 확산계수의 방법 · 역모형 · 기하 가정 — 표 1 · 그림 2a 가 방법(EIS · PITT · GITT) · 시료(입자 · 막 배향)가 다른 값을 한 축에 놓음(4–5 자릿수) · 캡션 'EIS' ↔ PITT 계열 · 서론이 그 폭을 "measurement techniques and … geometrical factors" 로 인정.

**근거(중)**

- **(뇨)** 한 지면 그림들의 매개변수 상태 — 그림 4b · 5b 의 끝 용량은 같은 표로 닫힘(72.6 ↔ 72.8) ✅ · 그러나 그림 4b 캡션의 파란 선 0 · 색 대응 다름 · 그림 6b 전류 미인쇄(5.0–6.1 mA cm⁻²).
- **(이)** 모형 값 인용 규칙 — 적합 D(x) 가 'based on the experimental measurements' 로 소개되고 하류(104호)가 '개선된 정확도' 로 옮김 · 모형 입력(두께 · c_max)이 같은 자료에서 나옴.
- **(치)** 모형 결론 옆 배제 가정 — '확산이 한계' 는 t₊ 0.99(농도 분극 0) · k 미인쇄 · M 1.8 µm · 끝 용량을 양극만 정하는 구성 위.
- **(뱌)** 재매개화 · 묶음의 최소성 — 우리 대수: D/M² · c_max·M · σ ∝ δc₀(D₊ + D₋) · 고립 면적 ≡ c_max — 저자 0.
- **(혀)** 이식된 수송 식의 원전 계 · 닫음 — 해리 이원 SE 구조(101 → 91호)가 남았는데 값(D_n⁻ = D_Li⁺/100)이 그 농도 분극을 끔 — 같은 이식의 결론이 값에 따라 켜지고 꺼지는 표본(104호와 반대쪽).
- **(체)** 평형 곡선의 출처 층위 — DNN EMF = 91호 외삽으로 읽힘 · NDB EMF 출처 0 · E_eq(x) 함수형 0.
- **(에)** 속도 상수의 i₀ 환산 — k₁ˢ · k₂ˢ 인쇄 0(α 만) — i₀ 둘 재현 불가.
- **(펴)** 출력에 안 보이는 성분 — 과전압 분해 그림 0 · 우리 계산으로 전해질 옴 55–77 % · BV · η_d 몫은 미인쇄 k 에 매달림.
- **(효)** 쓸기 결론의 무차원 영역 폐합 — '두꺼운 막에서 확산 한계' 를 D/M² 로 닫아 봄 · NDB 1.8 µm 로 닫힘 · 3 µm 면 D ×2.78.
- **(대)** C-rate 의 기준 용량 — 이름표 반올림 규칙이 두 판에서 다름 · 1C 기준 · A 미인쇄 · 그림 6 '51C' · 'comparable C-rate'.

**약**: **(다)** 28호 분모 — ASSB 추정 계보 가운데 편도 식별성 도구 0 한 점 · **(가)** 정적 ↔ 동적 — 같은 자료 EMF(정적)를 두고 동적만 적합(91 · 98호와 같은 관행 · 결정 재료 아님) · **(챠)** 최종 표 ↔ 물리 범위 — c_max 45 · 94.5 % 격자 · D(x) 가 그림 2a 범위 안 · **(셔)** 인쇄 식 ↔ 그림 항 — 식 (14) 의 음극 η_ct 는 k₂ˢ 미인쇄로 확인 불가 · 식 (9) 는 그림 6a 와 닫힘 · **(겨)** 처방 효과 측정 — 'optimize thickness' · 'ultrafast charging' 계산 0 · **(샤)** 다중 시작 — '거친 격자' 한 번 · **(규)** 백분율 기준 — '3.5 times' ↔ 3.67. **(마)** 근거 0 · **(라)(바)(사)** 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**.

## 새 판단 거리 (넷 — 글자는 호출자가 붙인다)

1. **같은 자료 두 적합표의 대조 표기** ((뎌) · (여) 의 계보판으로 묶어도 됨) — 같은 연구실(또는 계보)이 같은 자료(곡선)를 모형 구조를 바꿔 다시 맞춘 표가 둘 이상이면, 카드 · 개념 · truth 로 옮길 때 같은 이름 값의 비와 모형이 실제로 보는 조합(σ · t₊ · D/L² · 용량 스케일)의 비를 같이 적고, 이름 값이 자릿수로 움직인 이름은 '모형 조건부' 로 표시할지 — 115호: DNN(91호 자료) δ 0.18 → 0.04 · D_Li⁺ ×6.7 · D_n⁻ ×0.012 · t₊ 0.15 → 0.99 · σ ×0.22 · 51.2C 전해질 −109 → −141 mV(농도 몫 68 % → 0.1 %) · 두 편 다 '일치'.
2. **'정확도 개선' 비교의 자유도 · 표본 내 · 이전 시험 표기** ((햐) · (며) · (제) 의 개선판으로 묶어도 됨) — '모형 X 가 Y 보다 정확하다' 를 옮길 때 ① 두 모형의 맞춘 자유도(상수 D 1 ↔ 마디 4) ② 같은 자료에 맞췄는지(표본 내) ③ 지표(끝 용량 · 전압 잔차 · 없음) ④ 자료 사이 이전 시험의 결과 ⑤ 기준 모형을 그 자료에 다시 맞춰 봤는지(91호 상수 D 를 DNN 에 다시 맞추면 — 우리 재풀이로 ≈5.5×10⁻¹⁵ 가 D(x) 보다 나음)를 같이 적게 할지 — 115호: NDB 한 셀 · 지표 0 · DNN D(x) → NDB 이전 0.64 · 0.88 · 0.96(실패 인쇄) · 8C 에서 상수 D 가 DNN D(x) 보다 가까움.
3. **두께 · 확산 · 용량 스케일 묶음 표기 (박막판)** ((뱌) · (효) 의 하위로 묶어도 됨) — 평면 박막 적합의 D · c_max 를 옮길 때 끝 용량이 정하는 것이 D/M² 와 c_max·M 뿐이라는 것과 쓴 두께의 출처(설계 · SEM · 문헌)를 같이 적고, 지면 안에 두께가 둘이면 그 비가 D(×(M₁/M₂)²) · c_max(×M₂/M₁)에 주는 폭을 값 옆에 적게 할지 — 115호: NDB 1.8 µm(2절 · 그림 6b · 재풀이) ↔ 3 µm(3절 두 번) → D ×2.78 · c_max ×0.6 · 'deposition 이 확산을 높였다' · 'packing density' 해석이 두께에 매달림.
4. (선택) **결론의 운전 방향 · 범위 외삽 표기** ((주) · (탸) 의 하위로 묶어도 됨) — 방전 곡선 적합에서 '충전(ultrafast charging)' · '두께 최적화' 결론을 낸 편이면 방향(충전 ↔ 방전) · 범위(실험 최고 전류 ↔ 모의 전류) 외삽과 계산 유무를 값 옆에 적게 할지 — 115호: 충전 모의 0 · 'enables a method to optimize thickness'(최적화 0) · 그림 6b 전류 미인쇄(5.0–6.1 mA cm⁻² ≥ 실험 최고 5).

---

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것

| # | 어긋남 | 근거 |
|---|---|---|
| **D1** | 초록 "fit … at low and high discharge currents up to 5 mA cm−2" · 결론 "good agreement with the experiments even up to very high C-rates" ↔ 결과 절 "this agreement declines towards very high discharge currents as Fig. 4b reveals" | `[도표·화소]` 42C(5 mA cm⁻²) 끝 0.919 · 평탄 −30 … −80 mV |
| **D2** | NDB 양극 두께 — 2절 "1.8 μm" · 그림 6b "LCO : 1800 nm" ↔ 3절 "thicker films (e.g. 3 μm)" · "the NDB cathode with 3 μm thickness" | `[재현]` 끝 용량 열둘은 1.8 µm 로 닫힘 · 3 µm 이면 같은 곡선에 D ×2.78 |
| **D3** | 그림 4 캡션 "simulation model with diffusion coefficient taken from DNN fit – blue lines" ↔ 그림 4b 에 파란 선 0 · 그림 5b 는 빨강 = DNN D · 파랑 = 상수 D | 그림 판독 |
| **D4** | "3.5 times larger values of DLi+ and Dn−" ↔ 표 2 22.0/6.0 | ×3.67 |
| **D5** | "the vertical shift of whole profile towards higher values in logarithmic scale" ↔ 표 2 마디 비 | 2.35 · 2.40 · 4.00 · 2.00 |
| **D6** | "the beginning (red), the middle (blue) and the end (red) of 51C-rate discharging" ↔ 그림 6 캡션 · 그림 | 끝 = 초록 |
| **D7** | 표 2 D_Li⁺ · D_n⁻ · D_Li 단위 "m s−2" | m² s⁻¹(본문 · 식 8 은 m² s⁻¹) |
| **D8** | 그림 2 캡션 "by EIS measurements (a)" ↔ 범례 "Jang (PITT)" · 판 글자 (a)(b) 인쇄 0 | 그림 판독 |
| **D9** | 표 1 [17] "(101) · 003 Film (0.32 μm) · 101 Film (1.60 μm)" ↔ Xie 2008 | 102호 digest 전사 — (003) 0.31 · (104) 1.35 µm |
| **D10** | 서론 "The results are compared with the experimental data … and other numerical solutions" ↔ 지면 | 다른 수치해와의 비교 0 |
| **D11** | "the same charge transport mechanisms are used as in [7]" ↔ 식 (2) · (4) · (6) · (14) 의 음극 BV(91호에 없음 — 91 · 98호 digest 전사) · 같은 자료 전해질 재적합 | §(a) 1 |
| **D12** | 본문 "The black dots and curves in Fig. 5a" ↔ 캡션 "grey lines and dots" · 그림 회색 | 그림 판독 |
| **D13** | "average constant diffusion coefficient of 1.3·10−14" ↔ "Values for … constant diffusion coefficient are the result of optimization on rough grid" | '평균' 인가 '적합' 인가 |
| **D14** | "extensive experimental evidence that the diffusion coefficient in solid-state batteries is changing with the local State-of-Charge (SoC), see [12–17]" ↔ [17] = 액체 3전극 셀 | 102호 digest 전사 |
| **D15** | 초록 · 3절 "ultrafast charging application where > 5C is desired" · "enables a method to optimize thickness" ↔ 지면 | 충전 모의 0 · 최적화 계산 0 |
| **D16** | 그림 1 SEM(캡션 "a Li/LIPO/LiCoO2 solid state battery") ↔ 모의 셀 | 띠 비 ≈1.2 ↔ DNN 0.21 · NDB 1.8 · 축척 막대 0 |
| **D17** | 기호 · 오자 — 식 (1) x(탈리튬 0–0.5) ↔ x = c/c_max(리튬화도) · "LiCoO2 or LTO" · "Table II" ↔ "Table 2" · "two datasets described in the previous section"(뒤 절) · "systematically growth" · "the cathode end electrolyte" · 그림 6 캡션 "are comparable C-rate" · 참고문헌 [3] 편자 · 장 저자 뒤섞임 | 지면 |
| **D18** | "kd, kr, αLi, αLiCoO2 and δ are the same for both" ↔ 평형 관계 | `[재현]` k_d = k_r δ²c₀/(1−δ): DNN ✅ · NDB 9.30×10⁻⁷(인쇄 9.0 · −3 %) |
| **D19** | "deviation from the experimental data reduces, but still remains strong"(상수 → DNN D(x)) ↔ 그림 5b | 8C · 0.8C 에서 상수 D(0.975 · 1.00)가 DNN D(x)(0.88 · 0.96)보다 가까움 — 42C 에서만 맞는 문장 |
| **D20** | 율 이름표 반올림 — DNN 3C · 13C · 51C(I/Q_EMF 3.18 · 12.7 · 50.9 반올림) ↔ NDB 0.8C · 8C · 42C(0.85 · 8.5 · 42.7 버림) | `[재현]` |

---

# 이 편이 우리 프로젝트에 주는 것 (정리)

- **같은 자료 · 두 표 — '곡선이 맞는다 ≠ 값이 맞다' 의 직접적인 야생 표본(`[해석]`).** 같은 연구실이 같은 DNN 곡선을 2011 · 2019 에 다른 모형 구조로 맞췄고 전해질 값이 ×0.012–×6.7 · t₊ 0.15 ↔ 0.99 로 움직였으며 둘 다 '일치' 다 — 우리 `degradation-degeneracy/` 물음과 같은 꼴(우리 수치는 `degradation-degeneracy/docs/RESULTS*.md` 정본 — 옮기지 않음).
- **'정확도 개선' 은 자유도 · 표본 내 · 기준 모형 재적합을 같이 봐야 한다** — 상수 D(자유도 1)와 D(x)(마디 넷)의 같은 자료 비교 · 지표 0 · `[재현·가정]` 끝 용량 기준으로는 DNN 에서 상수 D 로도 남는다(x 의존이 요구되지 않음 — 전압 곡선 비교 0) · 이전 시험은 실패(저자 인쇄).
- **박막 묶음 D/M² · c_max·M** — 끝 용량은 이 두 조합만 본다. 지면 안 두께 불일치(1.8 ↔ 3 µm)가 확산계수 해석을 ×2.78 흔든다 · 1D 평면에서 고립 면적은 c_max(LAM 형)와 구별되지 않는다(카드 물음의 박막판).
- **계보 정리** — 26호 '문헌값' · ×1.0500 · D_e⁻ 의 원전은 98호이고 이 편이 아니다 · 이 편은 D(x) 구조 하나를 넘겼다 · 91호 인쇄 k_r 를 재사용했고 그 값을 가르지 못하는 그림만 냈다.
- **이 편이 주지 않는 것**: 자기 실험 · 접촉 · 박리 · 압력 · LAM · LLI 분해 · 적합 방법 · 잔차 · 불확실성 · 식별성 · k₁ˢ · k₂ˢ · E_eq 함수 · T · A · 원자료 · 코드 — 그리고 115 편 누적 `θ(N)` 0.

---

# 후속 후보 (원전 우선 — 지목 수는 위키 digest 의 후속 절 grep 으로 센 값)

| 등급 | 서지 (PDF 목록 번호) | 지목 (후속 절) | 왜 | 축 |
|---|---|---|---|---|
| ★★ | **Neudecker B.J., Dudney N.J., Bates J.B. 2000** — *J. Electrochem. Soc.* **147**(2), 517–523([22] · 제목 미인쇄) | **115** = 1(새) | **NDB 자료 전부의 원전** — 셀 치수(이 편 Li 3 µm · LIPON 1 µm · LCO 1.8 µm ↔ 3절 '3 µm')· 면적 · 온도 · 율 · EMF 출처 · 같은 셀 세 율인가(G5 · G6) | Q3 · (텨) |
| ★ | Jang Y.-I., Neudecker B.J., Dudney N.J. 2001 — *Electrochem. Solid-State Lett.* **4**(6), A74–A77([13]) | 99 · 102 · 107 · **115** = **4**(재지목 — 원장 3 + 1) | 그림 2a 'Jang (PITT) RF film (110)' — 같은 ORNL 계열 PITT 측정이 NDB 적합 D(x 0.5) 의 1/11 · 배향 이름표 (110) ↔ 102호 전사 (003)(G13) | Q3 · (뎌) |
| ★ | Dokko K., Mohamedi M., Fujita Y., Itoh T., Nishizawa M., Umeda M., Uchida I. 2001 — *J. Electrochem. Soc.* **148**(5), A422–A426([12]) | **115** = 1(새) | 그림 2a 'Dokko (EIS) particle' — **이 편 D(x) 모양(x ≈0.94 골 · x → 1 반등)의 주 근거** · 단일 입자 · 셀 형식 · 전해질은 이 지면에 인쇄 0 | Q3 · (료) |
| ☆ | [8] Fabre … Delacourt 2012 *JES* 159, A104(원장 L232 — 이 편 쓰임은 배경 목록 '[8–11]') · [20] Bouwman … Notten 2002 *JES* 149, A699(원장 L292 — 서론 배경 소개) · [2] Ramadesigan 2012 *JES* 159, R31(원장 L372 — 일반 서론) · [9] Jagannathan 2014 *JPS* 247 · [10] Chandrasekaran 2014 *JPS* 262 · [11] Behrou & Maute 2017 *JES* 164(98호 ☆) · [14] Barker 1996 *EA* 41 · [15] Okubo 2009 *SSI* 180 · [16] Dudney & Jang 2003 *JPS* 119–121 · [18] Van der Ven & Ceder 2000 · [19] Tang 2008 *JAC* 449(102호 ☆) · [21] Farkhondeh & Delacourt 2012 *JES* 159 · [1] · [3]–[6] | 원장 행 있음 셋(L232 · L292 · L372) · 나머지 행 없음 — 지목 칸 그대로(재지목 안 함) | 배경 목록 · 서론 · 표 1 행 · 일반 | — |

**지목 누락 0** — 이 편 22 번호 중 ★ 이상으로 앞 호 후속 절에 있던 편은 Fabre(L232) · Jang 2001(L267) · Bouwman 2002(L292) 셋이고 모두 원장 행이 있다 — 이 편에서의 쓰임이 구체적인 Jang(그림 2a · 표 1 자료)만 재지목으로 세고, 배경 목록 '[8–11]' 의 Fabre 와 서론 배경 소개의 Bouwman 은 ☆ 로 둔다(일반 · 배경 인용은 세지 않는다는 5차 묶음 규칙). ☆ 로만 오른 편(Behrou & Maute 2017 — 98호 · Tang 2008 — 102호)은 이번에도 ☆ 라 행을 만들지 않는다 · [2] Ramadesigan 2012 는 원장 행(L372)이 있으나 이 편 쓰임이 일반 서론이라 재지목으로 세지 않는다. **흡수된 편(교차)**: [7] = 91호 · [17] = 102호 — 셈 밖.

---

# 이 digest 가 주장하지 않는 것

- **D(x) 가 물리적으로 틀렸다고 하지 않는다** — LCO 의 상전이와 확산계수의 조성 의존은 문헌에 흔하다; 걸린 것은 이 편 자료(끝 용량)가 DNN 에서 그 x 의존을 요구하지 않는다는 것(우리 재풀이)과, 크기가 적합이고 모양만 문헌이라는 것이다.
- **우리 대리 모형이 저자 모형과 같다고 하지 않는다** — 양극 확산만 풀고 표면 x 0.995 를 차단으로 둔 근사다. 검증은 저자 그림의 끝 용량 열둘을 ±2.2 % 로 다시 낸다는 데까지이고, 상수 D 비교(§(c) 4)는 끝 용량만 본 것이다 — 전압 곡선까지 상수 D 로 맞는다고 하지 않는다.
- **NDB 두께가 실제로 1.8 µm 라고 확정하지 않는다** — 저자 계산이 1.8 µm 였다는 것까지다(원 [22] 미열람).
- **그림 6b 의 전류를 확정하지 않는다** — 두 읽기(6.0–6.1 · 5.0–5.5 mA cm⁻²)가 갈리고, 둘 다 실험 최고 이상이라는 것까지다.
- **91호 → 이 편의 전해질 값 이동이 91호 CRB 골짜기 위의 이동이라고 하지 않는다** — 모형 구조가 달라 다른 곳이며, 이동 방향은 91호 CRB 약한 방향과 거의 직교다(우리 계산).
- **두 열의 같은 값 다섯이 '움직이지 않은 값' 이라고 확정하지 않는다** — 91호 재사용 · 유도 · 기본값이라 그렇게 읽힐 뿐 G1 때문에 정하지 않는다.
- **그림 1 SEM 이 91호 그림 1a 와 같은 사진이라고 확정하지 않는다** — 띠 비가 같은 자릿수라는 것까지다(화소 대조 0).
- **이 편을 Q1 · Q4 · Q6 칸 이동 근거로 쓰지 않는다** — 접촉 · 식별성 계산 · 압력 0.
- **원 참고문헌(12 · 37 · 91 · 98 · 100 · 102 · 104호 인용분 · [12] · [13] · [19] · [22])을 다시 열지 않았다** — 대조는 각 digest 전사로 했다.

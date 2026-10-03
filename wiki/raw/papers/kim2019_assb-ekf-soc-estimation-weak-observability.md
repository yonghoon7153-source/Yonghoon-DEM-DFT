---
title: "Kim Y., Lin X., Abbasalinejad A., Kim S.U., Chung S.H. 2019 — On state estimation of all solid-state batteries (Electrochim. Acta 317, 663–672)"
source_url: local-upload/59._On_state_estimation_of_all_solid-state_batteries.pdf
source_url_note: "본문 PDF 10 쪽(Electrochimica Acta 317 (2019) 663–672 · 인쇄 쪽 663–672 · PageLabels 663 부터 · 그림 9 — 벡터 6 · 래스터 2 · 혼합 1 · 표 2 · 식 (1)–(28) · 참고문헌 23) 1,903,854 B · 업로드 접두사 11632c88 · 4차 묶음 파일 59 · SI 없음(보충 언급 0) · 원자료 · 코드 공개 0 · 실험 0(모형 + 합성 추정 편)"
source_doi: 10.1016/j.electacta.2019.06.023
source_license: "© 2019 Elsevier Ltd. All rights reserved.(인쇄) · CC · 오픈 액세스 표기 0 · 구독본으로 다룬다 — 이 digest 는 인용 · 요약 · 재현 계산만 담는다(그림 크롭은 위키 관례대로 raw/figures 에 — 변형 없는 잘라내기)"
pdf_sha256: a11bdbcbc01e8fb47cf94ab93e977793f5ebb6a2c06f683c8602da11dd494bbf
ingested: 2026-10-03
sha256: efac82b38c070fdcb30fbf50a15c8a56eb81470e89321c485690a74b6778fe90
---
# 수집 목적

`assb` 섹션 **99호** — **4차 묶음 파일 59**(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 요청 14 편 중 아홉째 · 2026-10-02 사용자 공급 · 파일 51–64 = 91–104호를 받은 순서대로). 닻은 `questions/assb-contact-loss-vs-lampe.md` 의 **Q4(유일성 · 식별성)** 와 원장 §2 **구조적 공백 1번**("역문제 · 식별성을 다루는 ASSB 논문" — 후보 목록의 "Kim 2019 (Danilov 모델 상태추정)")이고, 이 편이 직접 닿는 곳은 ① **12호**(Kouhestani 2022 — 이 편을 "Table 1 에서 유일한 SSB 상태추정 — 관측 가능성/식별성이 다뤄졌는지 확인 (Q4)" 로 지목) ② **37호**(Li 2024 — "ASSB 상태 추정(EKF) — 추정기에서 접촉/용량 손잡이 처리") ③ **26호**(Iwakiri 2024 — 같은 계보인데 이 편을 인용하지 않음) ④ **91호**(Danilov 2011 — 이 편이 "the model presented in Ref. [10]" 로 쓰는 원 모형) · **98호**(Raijmakers 2020 — 같은 계보의 2020 판) ⑤ 개념 [[assb-sensitivity-sweep-vs-identifiability]] · [[constrained-crb-identifiability]] · [[data-window-identifiability]] 다. 우리 쪽 수치(`degradation-degeneracy/` · `mode-observability`)는 `degradation-degeneracy/docs/RESULTS*.md` 가 정본이고 여기 옮기지 않는다.

University of Michigan-Dearborn(기계공학) + University of Ontario Institute of Technology + Washington State University Vancouver(**Y. Kim**(교신) · **X. Lin** · **A. Abbasalinejad** · **S.U. Kim** · **S.H. Chung**)의 *Electrochim. Acta* 2019 편. `[인쇄]` 초록이 스스로 적는다: "This paper studies the state estimation of a solid-state battery modeled as a partial differential equation system. Three assumptions simplifying the battery model underlie the study of state estimation: (1) neglecting the generation/recombination of Li-ions in the solid electrolyte; (2) assuming the charge transfer number of 0.5; and (3) the uniform electrolyte concentration. Results of a sensitivity study show the validity of the approaches to model simplification for the voltage prediction. … Simulation results show that the state-of-charge of the battery can be reasonably well estimated by the EKFs. However, the inaccuracy of the state estimation in low SOC range (0.1 < SOC < 0.4) due to weak observability cannot be addressed without including the diffusion dynamics in the electrolyte. This inclusion leads in a 40% reduction in state-of-charge estimation error, from 9% to 5% error for the considered case." 이 편이 실제로 한 것은 **91호 Li | Li₃PO₄ 1.5 µm | LiCoO₂ 320 nm 박막 모형(COMSOL 5.3a)을 '전체 모형' 으로 두고, 단순화 셋을 차례로 얹은 모형 2–4 의 전압 오차를 10C 정전류 · 10C 펄스에서 재고(표 2 — 매개변수 다섯을 하나씩 ×1/100 · ×100), 모형 3(전해질 포함 · 상태 7) · 모형 4(양극만 · 상태 4)의 유한차분 판에 EKF 를 얹어 같은 모형 계열의 합성 플랜트(SOC 0.99 · 잡음 섞인 전압)에서 SOC 를 추정한 것**이다. **실험 자료 0** · 열화 · 접촉 · 압력 · 온도 축 0(`contact*` · `degrad*` · `pressure` 본문 0 회).

들어온 경로: 원장 행(도착 표시 전 원문 그대로) "| ★★ | **Kim·Lin·Abbasalinejad·Kim·Chung 2019** — *Electrochim. Acta* **317**, 663 | 12 · 37 | **2** | **Q4** | 같은 Danilov 모델 위의 **상태추정** — 12호가 Q4 후보로 지목했는데 26호는 인용하지 않는다. **구조적 공백 1번 후보** · 37호: ASSB 상태 추정기가 접촉·용량 손잡이를 어떻게 두는가 |". 위키 grep(`Abbasalinejad` · `electacta.2019.06.023` · `317, 663` · `317** (2019) 663` · `663–672` · `Kim·Lin` · `Kim 2019` · `Youngki` · "state estimation of all")으로 각 digest 의 **후속 절**을 다시 셌다: **12호 후속 표(:510 · ★★ 3 · [62] — 등급 칸 있음) · 37호 §14(:414 · [21] — 등급 칸 없는 후속 표 · 98호가 Raijmakers 를 셀 때와 같은 처리) = 2 — 원장 "2" 와 일치**(정정 없음). 교차 기록(지목 아님): 91호 :618 "교차 참조 (지목 아님 — 이 편 이후 편)" · 26호 :390 "이 편이 인용하지 않는다" 메모 · 27 · 93 · 95 · 96 · 98호 "인용하지 않는 것 · 4차 묶음 13 편과의 관계" 문장 · 카드 · 로그의 12 · 37호 항(digest 후속 절 아님). 이 편은 우리 digest **하나**를 인용한다([10] = 91호) · 4차 묶음 다른 13 편 중 **[10](파일 51)** 하나만 인용한다(23 번호 전수 대조 — 나머지는 이 편보다 뒤이거나 인용 0).

이 digest 의 일 (지시):

1. **(a) 모형과 단순화 셋** — 원 모형의 출처(표 1 "[15]" ↔ 본문 "[10]") · 단순화의 근거와 오차(표 2).
2. **(b) 관측성** — "weak observability" 를 무엇으로 보였나 · ASSB 에서 식별성 / 관측성을 수치로 잰 첫 표본인가 · Q4 어휘 전수 · "n 번째 성질".
3. **(c) EKF 설계** — 상태 · 잡음 공분산 · 초기 오차 · 자료.
4. **(d) 접촉 · 용량 손잡이** — 37호 물음.
5. **(e) 후속 후보.**

⚠ **표기 규약**: `[인쇄]` = 원문이 실제로 쓴 것 · `[도표]` = 그림을 눈으로 읽은 값(판독 폭 표시) · **`[도표·벡터]`** = PDF 벡터 경로 좌표를 축 프레임 · 눈금 선으로 보정해 읽은 값(그림 2–6 · 8 — 저자 원자료가 아니다 · 판독 폭은 선 폭 ≈1 pt = 그림 3 에서 ≈1.8 mV · 그림 2 에서 ≈5.8 mV 이나 경로 꼭짓점은 그 중심이라 실제 폭은 그보다 좁다) · **`[도표·화소]`** = 래스터 그림(7 · 9)의 화소 좌표를 축 프레임으로 보정해 읽은 값(그림 7 SOC 1 화소 = 0.0031 · 전압 1 화소 = 2.44 mV · 그림 9 아래 판 1 화소 = 0.29 mV — 선 폭 · 점선 틈 · 색 겹침만큼 넓다) · `[재현]` = 원문 수치 · 식으로 우리가 다시 계산 · `[재현·가정]` = 가정이 붙은 재현(가정을 같이 적는다) · `[재현·대수]` = 인쇄된 식만으로 한 대수 · `[재현·외부 값]` = 원문 밖 값을 쓴 재현(91호 digest 전사 값 포함) · `[해석]` = 우리 해석 · **"(N호 digest 전사)"** = 이 세션에서 그 원문을 다시 열지 않고 우리 digest 의 전사로 대조한 것. **`[데이터]` 0** — 예치 원자료 · 코드 공개 진술 0.

⚠ **측정 · 인용 · 모형 · 적합 구분**: 이 편 안의 수치는 ① **측정 0** — 실험 자료가 한 점도 없다(그림 2 옆 "This is in compliance with experimental discharge profiles of solid-state batteries" 는 비교 그림 · 인용 0) ② **인용**(표 1 의 값 열한 개 — 머리 출처 "[15]" · 본문 "the validity of the parameters was experimentally demonstrated in Ref. [10]" — 91호 표 II 의 '설계 · NDP 측정 · model optimization' 값들(91호 digest 전사) · 식 (22) 평형 전위 = "[11]" 의 실험 곡선 함수) ③ **모형 출력**(그림 2–6 · 표 2 · 그림 7–9 의 플랜트 · 추정치 — 전부 계산) ④ **조율(tuning)**(P0 · Q_w · R_v "tuned … through repeated simulations") 넷이다. 적합(데이터 맞춤)은 이 편에 없다 — 매개변수 추정 0.

⚠ **쪽 표기**: PDF 10 쪽 = 인쇄 쪽 663–672(바닥 "Y. Kim et al. / Electrochimica Acta 317 (2019) 663–672" + 쪽 번호 · PageLabels 663 부터). 이 digest 는 인쇄 쪽 **"p. 667"** 로 적는다(PDF 쪽 = 인쇄 쪽 − 662).

⚠ **기호 충돌**: 이 편의 **θ** 는 양극 정규화 농도 c_Lis/c_Lis,max(식 19 — 텍스트 층에는 "q" 로 찍힘)이고, 카드 · 개념의 **`θ`(접촉 · 활성 분율)** 와 다른 양이다. 이 digest 에서 이 편의 것은 θ_s(표면) · θ̄(벌크)로만 쓴다.

---

# 판정 먼저

1. ★★★★ **(b) "weak observability" 는 계산이 아니라 논증 + 합성 실행 하나다 — 관측성 행렬 · Gramian · 야코비안 값 · CRB 0. 그리고 9 % 오차는 분산이 아니라 편향이다: 축약 모형의 출력 오차(≈−7 … −11 mV)가 OCV 평탄 기울기(0.07–0.09 V/SOC)로 증폭된 값과 같은 크기다(우리 재현).** `[인쇄]` "in the SOC range of 0.1–0.4, the equilibrium potential has a plateau, making the Jacobian to be almost zero and hence the battery system becomes very weakly observable. Second, as shown in Fig. 9, the contribution of the mass-transfer overpotential to the total overpotential is not insignificant, which makes the EKF4 finds incorrect state values by accounting for this error." `[재현]` 식 (22) 의 |dE/dSOC| 는 SOC 0.28 에서 최소 **0.072 V/SOC**(θ 0.859 · 3.901 V) · SOC 0.1–0.4 중앙 **0.126** ↔ 0.4–0.99 중앙 **0.658**(×5.2) · 1 mV 당 SOC 0.0134(SOC 0.3) ↔ 0.0010(SOC 0.99) — 평탄은 실재하고 "거의 0" 은 고 SOC 의 1/12.5 다. `[도표·화소]` 그림 9 EKF4 Δη_total ≈−7 … −11 mV(100–850 s) ÷ 그 SOC 의 기울기 = **예측 편향** 600 s −0.045 ↔ 그림 7 실측 −0.048 · 800 s −0.084 ↔ −0.087 · 750 s −0.123 ↔ −0.084 · 850 s −0.046 ↔ −0.068(×0.7–1.5 안). 반면 **EKF3 의 남은 −0.018 … −0.046 은 출력 오차(≈−1.6 … +0.7 mV → 예측 ≤0.02)로 설명되지 않는다** — 저자 설명("modeling error caused by coarse discretization")과 같은 방향: 출력(표면)이 맞아도 벌크(SOC)가 어긋나는 축(`[해석]`). ⇒ **Q4 0/99 — 아흔한 번째 성질**(아래 §(b) 3) · 원장 §2 공백 1번 후보 목록의 Kim 2019 는 **식별성 편이 아니다**(75 · 92호와 같은 닫음 형식 — 상태 추정 · 매개변수 식별 0 · 열화 손잡이 0).
2. ★★★★ **(a) '전체 모형' 은 인쇄 식 (14) 그대로 계산되지 않았다 — 그림의 η_mt 와 전압에 Nernst 농도 항 (RT/F) ln(c(L)/c(0)) 이 없다.** `[도표·벡터]` 그림 4 의 같은 조건 농도 단면(10C · 1 · 10 · 50 · 100 · 300 s)으로 식 (14) 를 항별로 풀면 둘째 항 −∫E dy = **−6.76 · −8.56 · −11.92 · −14.45 · −19.18 mV** ↔ 그림 3 η_mt **−6.99 · −8.83 · −12.19 · −14.73 · −19.55**(±0.3 mV) · 첫째 항(Nernst) −1.01 · −3.62 · −8.37 · −11.93 · **−18.44 mV** 는 그림에 없다(식 (14) 전체면 −7.77 … **−37.62 mV**). `[재현]` 그림 2 의 10C 전압 − Eeq(θ̄ · 쿨롱 계산) = 그림 3 η_total **±0.02–0.41 mV**(1–300 s) — 전압 자체에도 그 항이 없다. 그리고 우리 재풀이(표 1 + 아래 가정 · Nernst 항 없이)가 10C V · η_ct · η_mt · η_d 를 1–300 s 에서 **±0.5 mV** 로 다시 낸다(100 s: 3.9950 ↔ 3.9948 V · η_mt −14.73 ↔ −14.73 mV · 3.4 V 도달 5 · 10 · 20C 691.6 · 335.8 · 157.8 ↔ 689.4 · 334.6 · 157.2 s). ⇒ 플랜트가 전해질 분극의 ≈절반(300 s 에서 18.4 / 37.6 mV)을 빼고 계산됐다 — `[재현]` 식 (14) 그대로 넣으면 모형 4 오차(10C 정전류)는 우리 재풀이 기준 RMS **13.0 → 27.6 mV** · 최대 39.0 → 58.3 mV(펄스 3.4 → 8.0 · 8.6 → 18.9 mV — 표 2 인쇄는 14.3 · 43.5 · 4.9 · 9.9)로 ≈두 배가 된다(D1 · 코드 미공개라 구현 확정은 아님).
3. ★★★★ **(a) 표 1 은 출처 · 값 · 단위가 셋 다 흔들린다 — 머리 출처 "[15]"(Tian & Qi 2017 접촉 면적 손실 모의)는 본문 "[10] 모형" 과 다르고, D_n⁻ 2.1×10⁻¹⁵ 는 그림이 쓴 값이 아니며(5.1×10⁻¹⁵), k_pos 는 91호 값의 ×100 에 단위가 다르다.** `[재현]` 정전류 시작 순간 전해질이 균일하므로 η_mt(0⁺) = −I L RT / (δc₀ F² A (D_Li⁺ + D_n⁻)) — D_n⁻ **5.1×10⁻¹⁵ 이면 −6.15 mV ↔ 그림 3 −6.21 mV** · 표 1 의 2.1×10⁻¹⁵ 이면 −12.3 mV(재풀이 1 s −12.74 ↔ 그림 −6.99) ⇒ 그림 · 표 2 기준값 · 91호 표 II(5.10×10⁻¹⁵ — 91호 digest 전사)가 같은 값이고 **표 1 이 다르다**. L · M · A · c₀ · δ · k_r · D_Li⁺ · D_Li · α 는 91호 표 II 와 같은 수(91호 digest 전사) · `k_pos` 5.1×10⁻⁴ m³ mol⁻¹ s⁻¹ ↔ 91호 k₁ˢ 5.1×10⁻⁶ m^2.8 mol^−0.6 s⁻¹. `[재현·대수]` 식 (17) i₀ = F·A·k_pos × (무차원 비) 는 인쇄 단위로 C m⁵ mol⁻² s⁻¹ 이라 전류가 아니지만, A 를 m² 로 넣으면 **i₀ 0.277 mA(SOC 0.99) · ≈0.88 mA(중간)** — 91호가 Danilov 그림 8 에서 되읽은 i₀ ≈0.9–1.0 mA(91호 digest 전사)와 같은 자릿수 · 그리고 이 값으로 아래 4 의 0.0027 V 가 정확히 나온다. `k_r` 0.9×10⁻⁸ 은 91호 인쇄값 그대로 — 91호가 Danilov 자기 그림을 닫으려면 ×100 이 필요하다고 보인 값이다(91호 digest 전사).
4. ★★★★ **(a) 표 2 의 '민감도 분석' 은 식별성 분석이 아니라 축약 오차의 OAT 견고성이다 — 그리고 단순화 (1) 이 기대는 k_r · δ 는 흔들지 않았다.** `[인쇄]` 동기는 "it has been widely used in studies on assessing parameter identifiability or estimability [19,20]" · 방법은 "One-Factor-At-A-Time" · 출력은 Model 1 − Model k 전압 차의 Max · RMS(매 1 ms). `[도표·벡터]` 그림 5 · 6 오차 곡선 = 표 2 기준 행 그대로(M2 0.0005/0.0002 · M3 0.0233/0.0025 · M4 0.0435/0.0143 V · 펄스 M3 0.0027/0.0005 · M4 0.0099/0.0049) — 같은 계산. `[재현]` **펄스 Model 3 의 "0.0027"(표 2 열 행 중 일곱 행이 같은 값)은 t = 0⁺ 한 순간의 값이다**: SOC 0.99 · c⁺/c⁺₀ = δ · 10C(99.9 µA)에서 α 0.6 ↔ 0.5 의 η_ct −9.57 ↔ −12.25 mV → **2.68 mV** ↔ 그림 6 첫 점(t = 0.009 s) +2.68 mV — 매개변수를 흔들어도 같은 값인 이유(D·L·D_Li⁺ 는 첫 순간에 안 보인다). `[재현]` 단순화 (1)(생성 · 재결합 무시)의 오차는 **k_r 에 매달린다**: 10C 정전류 M1 − M2 최대 / RMS = **0.49 / 0.19 mV(인쇄 k_r 0.9×10⁻⁸ — 논문 0.5 / 0.2 ✅)** → 0.9×10⁻⁷ 4.19 / 1.62 → **8.0×10⁻⁷(98호 값) 14.82 / 6.50 → 0.9×10⁻⁶(91호 그림 일치 값) 15.33 / 6.77 mV**(M1 η_mt(300 s) −19.54 → −11.29 mV) — 표 2 에 k_r · δ 행이 없다(본문 "six critical parameters" ↔ 표 다섯). 단순화 (2)(α 0.5)는 k_pos ×1/100 에서 86.9 mV 로 깨지는데 저자는 "these extreme parameters are typically not physically realistic" 로 배제했다 — 열화로 A·k_pos 가 줄면 도달하는 방향이다(`[해석]` · (d)).
5. ★★★ **(d) 37호 물음 — 이 추정기에는 접촉 손잡이도 용량 손잡이도 없다.** 상태 = 농도 마디뿐(EKF4 양극 4 · EKF3 전해질 3 + 양극 4) · 매개변수 = 표 1 고정(+ 미인쇄 c_max · c_min · T) · SOC 는 고정된 c_max − c_min 으로 정의 · 면적 A 는 모든 플럭스 경계(식 3 · 4 · 11)와 식 (17) F·A·k_pos 에 한 값. ⇒ 플랜트에서 접촉(A_eff)이나 활성 용량이 변하면 추정기에는 **모형 불일치**로만 들어오고, 그것은 위 1 의 통로(Δη ÷ OCV 기울기)로 **SOC 편향**이 된다 — `[재현·가정]` A_eff ×0.5(10C · 중간 SOC i₀ 0.88 mA)면 Δη_ct ≈−2.9 mV → 평탄(0.072 V/SOC)에서 SOC −0.040 · SOC 0.4 위(0.658)에서 −0.0044. 접촉 손실과 LAM 은 이 추정기 안에서 **같은 편향 통로**를 쓴다(카드 물음의 상태 추정 층 표본).
6. ★★★ **(c) EKF 시험은 합성 한 번이다 — 잡음 · Δt · 실현 수 미인쇄, 상태 차원 · 초기값 목록이 인쇄 정의와 어긋나고, 그림 7 의 C-rate 기준이 그림 2–6 과 다르다.** `[인쇄]` P0 = I₇ₓ₇ · Q_w = Diag(10⁻³I₃ₓ₃, 9·10³, 10⁴I₃ₓ₃)(EKF3) · P0 = I₄ₓ₄ · Q_w = 10 I₄ₓ₄(EKF4) · R_v = 10⁻³ · 초기 SOC 플랜트 0.99 ↔ EKF 0.8 · "ĉ_Li⁺(0) = 1.1c_Li⁺(0)" 이 **EKF4 줄**에 인쇄되고 바로 다음 문장이 "initial conditions of the electrolyte are not required for the EKF4" — `[도표·벡터]` 그림 8 에서 **EKF3** 의 마디 셋이 11,880 = 1.1 δc₀ 에서 출발한다(D6). 인쇄 상태 정의(Me − 1 + Mp − 1 = 4 + 4 = 8) ↔ P0 7×7 — `[도표·벡터]` 그림 8 의 여섯 마디 합이 플랜트 · EKF3 모두 **64,908 = 6 δc₀** 로 보존돼(t = 0 · 990 s) 독립 전해질 상태 3 + 양극 4 = 7 로 읽힌다(D7). `[도표·화소]` 그림 7 전류 5.04C · 2.50C 인데 Actual SOC 300 · 600 · 900 s = 0.708 · 0.435 · 0.156 ↔ 그림 2–6 기준 쿨롱 0.740 · 0.490 · 0.240 → **전류 ×1.10–1.11** 이면 V · SOC 둘 다 맞는다(600 s 3.908 ↔ 3.911 V · SOC RMS 0.050 → 0.009 — D8). "9 % → 5 %" 는 SOC 절대 %p(그림 7 삽도 ≈0.085 · ≈0.045)이고 "40 % reduction" 은 (9 − 5)/9 = **44 %**(D10).
7. ★★ **(e) 계보 — 이 편은 91호 적합값(인쇄 k_r 포함)에 91호와 다른 평형 곡선(Fabre [11] 의 유리함수)을 끼운 혼성이다.** 91호는 같은 셀 방전 곡선의 율 외삽 EMF 로 일곱을 맞췄고(91호 digest 전사) 이 편은 그 값으로 Fabre OCV 를 돌린다 — "the validity of the parameters was experimentally demonstrated in Ref. [10]" 는 이 조합에 옮겨지지 않는다. `[재현]` 식 (22) 는 θ ∈ [0.5, 1] 에서 단조 · 3.4 V = θ 0.99924 · **분자 영점 θ 1.00319 · 분모 극 θ 1.00369** — 물리 범위 바로 위에 극이 있어 θ_s 가 1 을 넘는 추정치(EKF 갱신)에서는 함수가 뒤집힌다(`[해석]` — 그림 7 의 900–960 s 스파이크와의 관계는 확인 안 함).
8. **채움표** — Q1 해당 없음(`θ(N)` 0/99 · 층 하나: F·A·k_pos 곱 · k_pos ×1/100 '비현실' 배제) · Q2 없다(전압 하나 · 처방 = 모형 구조 + 미래 과제 '궤적 창') · Q3 층 하나("합성 플랜트 = 같은 계열 PDE · 인쇄 식 (14) 의 Nernst 항 없이 계산 · 표 1 ↔ 그림 D_n⁻ · 91호 적합값 + Fabre OCV 혼성") · **Q4 0/99 — 아흔한 번째 성질** · Q5 해당 없음(Li 금속 · 음극 전하이동 무시) · Q6 해당 없음(`pressure` 0) · Q7 해당 없음 + 공백(c_max · c_min 미인쇄) · Q8 층 하나(Fabre 유리함수 · 평탄 창 = 관측성 창 · 물리 범위 바로 위 극). **누적 ≈20.0 → ≈20.0 (새 칸 0).**

---

# 서지

| 항목 | 값 (`[인쇄]` — p. 663 · p. 672 · XMP) |
|---|---|
| 제목 | **"On state estimation of all solid-state batteries"**(지면 · 정보 사전 · XMP 같음) |
| 저자 · 소속 | **Youngki Kim**ᵃ,\* · **Xianke Lin**ᵇ · **Armin Abbasalinejad**ᶜ · **Sun Ung Kim**ᶜ · **Seung Hyun Chung**ᶜ — ᵃ Department of Mechanical Engineering, University of Michigan-Dearborn, Dearborn, 48128 USA · ᵇ Department of Automotive, Mechanical and Manufacturing Engineering, University of Ontario Institute of Technology, Oshawa, Ontario, L1G 0C5, Canada · ᶜ School of Engineering and Computer Science, Washington State University, Vancouver, WA 98686, USA · 교신 Y. Kim(메일 인쇄 — 옮기지 않음) |
| 저널 | *Electrochimica Acta* **317** (2019) **663–672** · doi `10.1016/j.electacta.2019.06.023` · ISSN 0013-4686 · XMP `prism:coverDate` 2019-09-10("10 September 2019") |
| 일정 | Received **15 April 2019** · revised **4 June 2019** · Accepted **4 June 2019** · online **10 June 2019** · `[재현]` 접수 → 수락 **50 일**(수정본 접수일 = 수락일) |
| 저작권 | "© 2019 Elsevier Ltd. All rights reserved." · CC · OA 표기 0 ⇒ **구독본으로 다룬다** — 이 digest 는 인용 · 요약 · 재현 계산만 담고 그림 크롭은 위키 관례대로 `raw/figures/`(변형 없는 잘라내기) |
| 키워드 | All-solid-state battery · Model simplification · Sensitivity analysis · State estimation · Extended Kalman filter |
| 자금 · 감사 | "Y. Kim would like to acknowledge the financial support from the University of Michigan through Research Initiation & Development Grant." · 이해 상충 진술 0 |
| 코드 · 자료 | **공개 진술 0** · 전체 모형 "COMSOL Multiphysics 5.3a"(1 회) · 모형 2–4 · EKF 구현 도구 미인쇄 |
| 분량 | 10 쪽 · 그림 **9**(벡터 6 = 그림 2–6 · 8 / 래스터 2 = 그림 7 · 9 / 혼합 1 = 그림 1) · 표 **2** · 번호 식 **(1)–(28)**(+ 번호 없는 반응식 둘 · SOC 정의 · c̄ 정의 · EKF 갱신 다섯 줄) · 참고문헌 **[1]–[23]**(빠진 번호 0 — p. 672 목록에서 직접 셈) |
| 절 | 1. Introduction · 2. Solid-state battery model(2.1 Electrolyte · 2.2 Cathode · 2.3 Overpotential computations · 2.4 Model performance · 2.5 Model simplification) · 3. Battery state estimation(3.1 Control-oriented model · 3.2 EKF-based state estimation — 3.2.1 Cathode only (EKF4) · 3.2.2 Electrolyte included (EKF3) · 3.3 Performance comparison) · 4. Conclusions · Acknowledgment · References — ⚠ 서론의 안내문은 "Section 2 … In Section 3, approaches to model simplification … in Section 4, EKF-based estimators … section 5 draws the conclusions" 로 실제 절 번호(2.5 · 3 · 4)와 다르다(D12) |
| 셀 | **모형만** — Li 금속 | 비정질 **Li₃PO₄ 1500 nm** | **LiCoO₂ 320 nm** · 면적 **1 cm²**(표 1 · 그림 1) — 91호 셀의 설계값과 같다(91호 digest 전사: 공칭 10 µAh) · 셀 제작 · 측정 0 |
| 모의 | 전체 모형(COMSOL 5.3a) · 5 · 10 · 20C 정전류 → 3.4 V(그림 2) · 10C 정전류 + 10C 1 분 펄스 / 4 분 휴지 ×4(그림 5 · 6 · 표 2 — 비교는 "for every 1 ms") · EKF 시험 = 5C 60 s / 2.5C 240 s 되풀이 1000 s(그림 7–9) |
| 모형 | 1D · 등온(T 미인쇄) · 음극 = Li 금속(옴 · 전하이동 무시) · 전해질 = Li⁰ ⇌ Li⁺ + n⁻ 해리(k_r · k_d) + 이원 확산(식 1–8) · 양극 = Fick(식 9–12 · 이동항 무시) + BV(식 16–17 · α_pos 0.6) · 과전압 = η_ct + η_mt + η_d(식 13–18) · Vt = Eeq(θ̄) + η_tot(식 23) · Eeq(θ) = [11] 의 유리함수(식 22) · 열화 · 이중층 · 축전기 0 |

**PDF 메타데이터 (이 실행에서 직접 읽음 · pymupdf)** — 1,903,854 B · sha256 `a11bdbcbc01e8fb47cf94ab93e977793f5ebb6a2c06f683c8602da11dd494bbf`(호출자 명시값 ✅ — 직접 재계산) · 헤더 `%PDF-1.7` · 10 쪽 전부 595.3 × 793.7 pt · 암호 0 · 정보 사전: title **"On state estimation of all solid-state batteries"** · author **"Youngki Kim"** · subject **"Electrochimica Acta, 317 (2019) 663-672. doi:10.1016/j.electacta.2019.06.023"** · keywords "" · creator **"Elsevier"** · producer **"Acrobat Distiller 8.1.0 (Windows)"** · 생성 **D:20190723171216+05'30'** · 수정 **D:20190723171246+05'30'**(호출자 메모와 같음 ✅ — 생성 30 초 뒤 · 온라인 2019-06-10 보다 여섯 주 뒤 = 권 · 쪽 확정판으로 읽힘 · 판정 안 함) · 트레일러 ID [55841ACB6FA282128943901ADBDC00EC · 59E2AC54D46CA64496D962305D5BCB2E] · XMP **7,164 B**(`dc:creator` 다섯 · `dc:subject` 키워드 다섯 · `dc:publisher` Elsevier Ltd · `prism:volume` 317 · `pageRange` 663-672 · `coverDisplayDate` 10 September 2019 · `prism:copyright` "© 2019 Elsevier Ltd. All rights reserved." · `pdfx:doi` · crossmark `MajorVersionDate` **2010-04-23**(98호와 같은 Elsevier 틀 값) · `CrossmarkDomainExclusive` true · `jav:journal_article_version` VoR · `pdfx:robots` noindex · `xapRights:Marked` True · `xap:CreateDate` 2019-07-23T17:12:16+05:30 · `ModifyDate` = `MetadataDate` 17:12:46 · `xapMM:DocumentID` uuid:43663c94-ab51-44f4-913e-6dbe43539d83 · `InstanceID` uuid:bb64a01c-8990-488a-87cd-7f53eed8bcc1) · 카탈로그 `/StructTreeRoot`(태그 PDF) · `/Threads` · `/Outlines` · `/PageMode /UseOutlines` · `/PageLayout /SinglePage` · `/OpenAction` FitH · **PageLabels 십진 663 부터**(= 인쇄 쪽) · `%%EOF` 1 · 래스터: p. 663 셋(CrossMark 단추 120×119 · Elsevier 로고 254×278 · 저널 표지 237×299 — 그림 아님) · p. 664 그림 1 조각 셋(374×469 · 389×469 · 3×466) · **그림 7**(1328×1037) · **그림 9**(1422×1094) · 벡터 그림 여섯(그림 2–6 · 8 — 경로 · 글리프 · 눈금 글자도 글리프 경로).

⚠ **텍스트 층**: 합자 **65**(NFKC 로 복원) · 빼기 부호가 빈칸으로 빠진다("0:9  108" = 0.9×10⁻⁸ — 표 1 지수 부호는 쪽 렌더로 확인) · 그리스 문자 대체(θ → "q" · η → "h" · α → "a" · δ → "d" · β → "b" · γ → "g" · Δ → "D") · "þ" = "+" · "¼" = "=" · 범위 대시가 "e" 로("0.1e0.4" = 0.1–0.4 · "663e672" = 663–672 · "[6e9]" = [6–9]) · 줄 끝 하이픈은 Elsevier 분철(복원 뒤 셈). 식 (1)–(17) · (22) · (25)–(28) · EKF 갱신 · 조율 값 · 초기값 목록 · 표 1 · 2 는 **쪽 렌더 조각으로 읽었다**(200–300 dpi · 판독용 · 커밋 안 함).

---

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | **양극 농도 한계 · 초기값** — SOC 정의(p. 665)가 쓰는 c_Li,max · c_Li,min 과 식 (10) c_Lis,0 이 표 1 에 없다 · 용량 · 1C 전류 값 0(각주 1 "A 1C rate means that the discharge current will discharge the entire battery in 1 h." 뿐) | SOC · θ · 전류의 절대 크기가 정해지지 않는다 — `[재현·외부 값]` 91호 a_max 2.33×10⁴ mol m⁻³(91호 digest 전사) · c_min = c_max/2(반응식 "0 ≤ z ≤ 0.5") · SOC₀ 0.99 로 두면 그림 4 양극 초기(≈1.177×10⁴ = c_min + 0.01Δ) · 그림 2–3 전압 폐합(±0.4 mV)이 함께 맞는다 → Q = 9.99 µAh · 1C = 9.99 µA(R3) |
| **G2** | **온도 T** — RT/F 가 식 (14)–(17) · (24) · (28) 에 들어가는데 값 0 | `[재현·가정]` 298.15 K(91호 측정 25 ℃)로 폐합 — 다른 T 면 η_mt · η_ct 크기가 비례로 움직인다 |
| **G3** | **플랜트 측정 잡음** — 그림 7 V_meas 에 더한 잡음의 분포 · 크기 · 시드 0 · 필터의 R_v = 10⁻³(단위 미인쇄)만 | `[도표·화소]` 잡음 띠 p5/p95 −63 / +68 mV — σ 로 ≈30–40 mV 수준(선 연결로 넓게 잡힘) ↔ R_v 10⁻³ V² 면 σ 31.6 mV · 필터가 참 잡음을 알았는지(맞춤 R) 모른다 |
| **G4** | **이산화 시간 간격 Δt** — 식 (27) A_d · B_d 의 시간 이산화 · 측정 주기 미인쇄(공간 Me = Mp = 5 만) | 같은 Q_w(10 · 10⁴)라도 Δt 에 따라 과정 잡음의 실제 크기가 다르다 — 조율 값을 다른 구현으로 옮길 수 없다 |
| **G5** | **상태 차원 · 배열 · 단위** — x^e = [c_1 … c_{Me−1}] · x^s = [c_1 … c_{Mp−1}] · Me = Mp = 5(→ 8) ↔ EKF3 P0 I₇ₓ₇ · Q_w 3 + 1 + 3 · 어느 상태가 어느 Q_w 블록인지 · 보존된 전해질 총량 처리 · P0 · Q_w 단위 0 | `[도표·벡터]` 그림 8 여섯 마디 합 보존(64,908 = 6 δc₀)으로 '독립 전해질 3 + 양극 4' 로 읽힌다(R17 · D7) — 구현 확정 아님 |
| **G6** | **EKF4 출력 함수 h̃ 의 η_ct** — "the output function h̃ is different from h in computing the charge transfer overpotential in Eq. (27)" 만 · 무엇이 다른지(c_Li⁺ 에 δc₀ 를 쓰는지) 미인쇄 | EKF4 의 모형 불일치에 η_ct 몫이 얼마인지 가를 수 없다(그림 9 Δη_ct 는 두 EKF 가 거의 같다 — ≲1–2 ×10⁻³ V) |
| **G7** | **오차 지표 정의 · 실행 수** — "9% error" · "5% error" 의 정의(최대 · 구간 평균 · 절대 %p ↔ 상대) · 실행 · 잡음 실현 · 초기 오차 변형 수 0(그림 7 하나) | `[도표·화소]` 9 % ≈ SOC 절대 −0.084 … −0.087(750–800 s) · 5 % ≈ −0.043 … −0.046 — 산포 · 신뢰구간 없는 단일 실행 값 |
| **G8** | **계산 비용** — "real-time" 동기 한 번뿐 · 계산 시간 · 연산량 0(12호 Kouhestani 의 "the efficiency of the algorithm has not been determined" 가 지면으로 확인됨 — 12호 digest 전사) | 모형 4 를 고른 이유("much simpler")의 이득이 수치로 없다 |
| **G9** | **모형 2–4 의 구현** — 전체 모형만 COMSOL 로 명시 · 모형 2–4 가 같은 COMSOL 인지 · 유한차분인지 · 격자 · 허용오차 미인쇄 | 표 2 오차에 수치 차가 섞였는지 못 가른다 — `[재현]` 우리 재풀이는 M2 를 ±0.02 mV 로 닫지만 그림 6 의 M3 휴지 구간 −0.1 … −0.8 mV 표류와 M4 의 ≈1.3–2.1 mV 차는 다시 나오지 않는다(R10) |
| **G10** | **표 1 의 출처 층위** — 머리 "[15]"(Tian & Qi 2017) ↔ 본문 "[10]" · 열 이름 "Estimated value" · D_n⁻ 2.1 ↔ 표 2 5.1 · k_pos 의 값 · 단위가 91호와 다름 · k_r 인쇄값의 ×100 문제(91호) 무언급 | 하류가 이 표를 '문헌값' 으로 옮기면 그림이 쓴 값과 다른 값이 퍼진다(D2 · D3) — [15] 미열람이라 2.1 · 5.1×10⁻⁴ 가 그 편에서 왔는지 모른다 |
| **G11** | **평형 곡선의 정체** — 식 (22) "the following nonlinear function from experimentally obtained equilibrium potential of the cathode in Ref. [11]" — 측정 셀 · 방법(GITT · 저율 · 외삽) · 맞춤 범위 · θ 정규화 기준 · θ → 1 근처 타당성 0 | 관측성 창(평탄)의 위치 · 폭이 이 함수로 정해진다 — `[재현]` 분모 극 θ 1.00369 · 분자 영점 1.00319(물리 범위 바로 위) · 91호(같은 셀의 율 외삽 EMF)와 다른 곡선을 같은 매개변수와 짝지었다(판정 7) |
| **G12** | **'weak observability' 의 정량 근거** — 관측성 행렬 · 랭크 · Gramian · 야코비안 값 · 조건수 · CRB · 잡음 대비 감도 · Monte Carlo 0 | Q4 칸이 움직이지 않는 이유 — 평탄 기울기 · 편향 사상 · 단일 점 감도는 우리 `[재현]`(R2 · R15 · R16)이다 |

---

# 보충 자료 — 받은 것 · 대조

**SI 없음 (원문에 보충 언급 0).** 호출자 대조와 같은 결과를 이 실행에서 직접 다시 셌다 — 본문 · 캡션 · 표 · 참고문헌 전문(NFKC · 줄 끝 분철 복원 뒤)에서 `supplement*` · `supporting information` · `appendix` · `data availab*` · `video` · `movie` · `zenodo` · `github` · `code` **0 회**(본문 `COMSOL` 1 회 — 도구 이름). 원자료 예치 0 · 코드 0 ⇒ 이 digest 의 재현은 **인쇄 수치 + 벡터 경로 + 래스터 화소 + 우리 재풀이** 네 층뿐이다.

---

# 그림 · 표 — 자동 10 항목 + 수동 6, 실제로 연 것 **16/16**

크로퍼(`wiki/tools/extract_figures.py`)가 본문 그림 1 · 2 · 4–9 를 `fig_1` · `fig_2` · `fig_4 … fig_9` 로, 표 1 · 2 를 `tab_1` · `tab_2` 로 잡았다(SI 판별 ✅ — 파일명 `59._On_state_estimation_of_all_solid-state_batteries` 의 `SI_TAG` False · 실행 뒤 이름을 눈으로 확인 · `fig_S…` 0). 수동 크롭 6(300 dpi · `*_manual_p*.png` — 파일명의 p 숫자는 PDF 쪽): **그림 2 · 그림 3(분리) · 그림 5 · 6(왼쪽 축 포함) · 표 1 · 표 2 단독**. 자동 크롭 점검(`figures.json` `note` 에 적음 — 자동 파일은 지우지 않았다):

- **병합 · 누락 하나** — `fig_2` 가 같은 줄의 그림 2(왼쪽) · 그림 3(오른쪽)을 한 항목으로 잡고 캡션 필드도 둘을 이어 붙였다 → 그림 3 이 자동에서 빠졌다 → 수동 둘로 분리.
- **잘림 셋** — `fig_2`(그림 2 의 y 축 제목 'Voltage (V)' 왼쪽 끝) · `fig_5` · `fig_6`(세 판의 y 눈금 글자 · 제목이 잘려 끝 자리만 보임) → 수동 셋.
- **과대 둘** — `tab_1`(p. 664 쪽 전체 — 그림 1 · 본문 두 단 · 표 1 · 각주) · `tab_2`(p. 669 쪽 전체 — 표 2 · 그림 7 · 본문) → 표만 수동 둘(표 2 는 첫 수동 크롭이 각주 a · b 를 잘라 영역을 넓혀 다시 렌더).
- **캡션 필드 오염 · 잘림** — `tab_1`(표 1 글자 전부 + 각주 1 이 섞임) · `tab_2`(표 2 글자가 섞이고 900 자에서 잘림) · `fig_9`('.Dh ¼ hplant  hest' = 'Δη = η_plant − η_est') · 그림 캡션의 'Liþ' = Li⁺ — 캡션 원문은 PDF 가 정본.
- 나머지(`fig_1` · `fig_4` · `fig_7` · `fig_8` · `fig_9`) 라벨 · 내용 온전 · 잘림 0 · 과대 0.

**16 장 전부 이 실행에서 직접 열었다 — 안 본 그림 · 표 0.** (p. 663 래스터 셋은 로고 · 표지 · CrossMark 라 그림이 아니다.) 판독: 그림 2–6 · 8 은 **벡터 경로 좌표**(축 프레임 선 · 눈금 선 위치로 보정 — 그림 2 x 56.87–276.39 pt = 0–700 s · y 532.84 = 4.4 V · 705.87 = 3.4 V / 그림 3 x 330.92–545.52 = 0–350 s · y 537.18 = 0 · 706.32 = −0.3 V / 그림 4 x 175.0 · 277.21 · 379.42 · 440.75 = 0 · L/2 · L · L+M · y 701.64 = 0.6×10⁴ · 475.78 = 2.4×10⁴ / 그림 5 오차 판 0.05 · 0 · −0.05 = y 255.54 · 273.61 · 291.67 / 그림 6 오차 판 0.01 · 0 · −0.01 = y 539.74 · 561.27 · 582.8 / 그림 8 x 174.79–452.48 = 0–1000 s · y 77.74 = 1.4×10⁴ · 296.62 = 0.8×10⁴), 그림 7 · 9 는 **화소 좌표**(내장 래스터 원본 해상도 — 프레임 선 · 색 마스크 · 열별 중앙값)다. 판독 · 재현 코드 · 렌더 조각은 `scratchpad` 에만(커밋 안 함).

## Fig. 1 — 셀 도식 (p. 664 · 봤다 · 래스터 조각 + 벡터) ★ (a)

Li metal (Anode) | Li₃PO₄ (Solid-Electrolyte) | LiCoO₂ (Cathode) · L = 1500 nm · M = 320 nm · y = 0 · 1500 · 1820 nm · 방전 중 Li → Li⁺(y = 0) · Li⁺ → Li_s(y = L) · 외부 Load · 전류 i(왼쪽 화살) · e⁻(양극 쪽). **91호 셀(Li₃PO₄ · 320 nm · 1500 nm)과 같은 기하** — 98호의 LiPON 상용 셀이 아니다. 면적 · 집전체 · 계면 접촉 표시 0.

## Fig. 2 — 5 · 10 · 20C 방전 (p. 666 · 봤다 · 수동 분리 · 벡터 판독) ★★★ (a)

`[도표·벡터]` 시작 4.2728 · 4.2644 · 4.2482 V · 3.4 V(축 바닥 = 컷오프) 도달 **689.40 · 334.56 · 157.18 s**(명목 3600/C 의 0.958 · 0.929 · 0.873 — SOC₀ 0.99 기준 이용 몫 0.967 · 0.939 · 0.882) · 10C 100 · 200 · 300 s 3.9948 · 3.8885 · 3.8301 V · 5C 평탄 ≈3.88–3.90 V(400–550 s). 본문 "At higher C-rates, a sharp drop in voltage occurred, followed by a small plateau and a drop at the end" 와 맞는다. ⚠ 같은 문단 "The model captures most of the basic characteristics of the solid state battery which include relative absence of a plateau at nominal voltage" 는 이 그림의 3.88 V 평탄과 문장으로 어긋난다(D20). `[재현]` 재풀이 3.4 V 도달 691.63 · 335.77 · 157.84 s(+0.3 · +0.4 · +0.4 %).

## Fig. 3 — 10C 과전압 성분 (p. 666 · 봤다 · 자동 누락 → 수동 · 벡터 판독) ★★★★ (a) · D1 · D2

`[도표·벡터]` η_mt(검정 일점쇄선) 첫 점 −6.21 → 1 s −6.99 → 10 s −8.83 → 100 s −14.73 → 300 s −19.55 → 335 s −19.92 mV(거의 직선으로 커짐) · η_ct(파랑) 첫 점 −8.99 → 100 s −3.42 → 300 s −7.98 → 335 s −49.6(끝 −81.7) · η_diff(빨강 점선) 최저 −47.6 mV @≈20–25 s → 240 s −4.1 → 333 s −257.7 · η_total(자홍) = 세 성분 합(25 s −61.8 · 240 s −27.5 mV). ★ η_mt(0⁺) −6.2 mV 는 **D_n⁻ 5.1×10⁻¹⁵ 의 균일 농도 옴 강하**(`[재현]` −6.15)이고 표 1 의 2.1×10⁻¹⁵ 면 −12.3 이다(D2). ★ 이 곡선은 그림 4 단면으로 계산한 식 (14) **둘째 항만**과 ±0.3 mV 로 같다 — 첫째 항(Nernst)이 없다(D1 · R5).

## Fig. 4 — 10C 농도 단면 (p. 667 · 봤다 · 벡터 판독) ★★★★ (a) · G1

`[도표·벡터]` 전해질 초기 10,818 mol m⁻³(= δc₀ · 인쇄 식 (2)) · 300 s c(0) 14,531 · c(L/2) 10,813 · c(L) 7,089(본문 "the mobile lithium concentration in the electrolyte region at the mid-node point becomes constant" ✅ — 1–300 s 에서 10,813–10,818) · 양극 1 s 11,766(뒷면)–12,015(표면) → 300 s 21,514–22,394. x 축은 척도가 아니다(L/2 · L · L+M 눈금 간격 102.2 · 102.2 · 61.3 pt — M/L 을 0.30 으로 그림 · 실제 0.213). ★ 양극 초기 ≈1.177×10⁴ 은 c_max 2.33×10⁴ · c_min = c_max/2 · SOC 0.99 의 c_min + 0.01Δ 와 같다 — 이 편이 인쇄하지 않은 c_max · c_min 이 91호 a_max 임을 그림이 드러낸다(G1 · R3).

## Fig. 5 — 모형 1–4 · 10C 정전류 (p. 668 · 봤다 · 수동(왼쪽 축) · 벡터 판독) ★★★ (a)

세 판 — 'Current (C-rate)' 10 · 'Voltage (V)' 3.4–4.4 · 'Voltage Error (V)' ±0.05 · x 제목 인쇄 그대로 **'Time (t)'**. 모형 4(자홍)가 모형 1 위에 뜬다 → 오차 = V₁ − V_k 부호(본문 정의 0). `[도표·벡터]` 곡선 끝 334.50 s · M2 최대 0.0005 · RMS 0.0002 · M3 0.0233 · 0.0025 · M4 0.0435 · 0.0143 V = **표 2 기준 행 그대로** · M3 0.5 s +1.13 → 300 s −2.66 → 334 s −20.3 mV · M4 0.5 s −1.23 → 100 s −10.66 → 300 s −18.70 → 334 s −40.1 mV. `[재현]` 재풀이 M2 ±0.02 mV · M3 300 s 까지 ±0.05 mV · M4 는 그림이 ≈1.3–1.7 mV 더 음(R10).

## Fig. 6 — 모형 1–4 · 10C 펄스 이완 (p. 668 · 봤다 · 수동(왼쪽 축) · 벡터 판독) ★★★ (a)

10C 1 분 + 휴지 4 분 ×4 · 1200 s · 오차 ±0.01 V. `[도표·벡터]` M2 최대 1×10⁻⁴ · **M3 최대 0.0027 V @t = 0.009 s(첫 점)** · RMS 0.0005 · M4 최대 0.0099 @960 s · RMS 0.0049 = 표 2 기준 행. ★ M3 의 최대는 **켜는 순간 한 점**이다 — `[재현]` α 0.6 ↔ 0.5 의 t = 0⁺ 차 2.68 mV(R8) — 표 2 펄스 M3 열 행 중 일곱 행이 0.0027 인 이유. ⚠ M3 휴지 구간(61 · 150 · 299 · 450 · 1100 · 1199 s) −0.23 · −0.13 · −0.11 · −0.36 · −0.81 · −0.80 mV 표류 · M4 첫 점 +0.59 mV(M3 와 같아야 할 t = 0⁺ 에서 −2.09 mV 차)는 우리 재풀이(휴지 중 M3 = M2 ≈+0.05–0.08 mV)에 없다 — 원인 미확정(G9).

## Fig. 7 — EKF 성능: 전류 · 전압 · SOC (p. 669 · 봤다 · 래스터 화소 판독) ★★★★ (b) · (c) · D8

(위) 'Current (C-Rate)' — `[도표·화소]` **5.04C 60 s / 2.50C 240 s** 되풀이(0 · 300 · 600 · 900 s 시작) · 1000 s (가운데) V_meas(파랑 · 잡음) · V_t(검정) · EKF4(빨강 파선) · EKF3(초록 일점쇄선) — 두 EKF 의 전압은 ≈4.09 V 에서 출발해 ≈100 s 안에 V_t 로 붙는다 (아래) SOC Actual · EKF4 · EKF3 + 삽도(600–950 s · 0.1–0.45). `[도표·화소]`(x 140 → 1286.5 px = 0 → 1000 s · SOC y 595.5 → 923 px = 1 → 0) Actual 300 · 600 · 900 · 990 s = **0.708 · 0.435 · 0.156 · 0.064** · EKF 출발 ≈0.77–0.78(인쇄 0.8) · EKF4 오차 200 · 400 · 600 · 750 · 800 · 850 s = −0.021 · −0.034 · −0.048 · −0.084 · −0.087 · −0.068 · EKF3 −0.021 · −0.018 · −0.024 · −0.045 · −0.046 · −0.046 · 900–960 s 초록 스파이크 · 끝에서 둘 다 Actual 로. ★ **Actual SOC 가 그림 2–6 의 1C(9.99 µA) 기준 쿨롱 계산보다 빨리 떨어진다**(0.740 · 0.490 · 0.240 · 0.136 ↔ 위 값) — `[재현]` 전류 ×1.10–1.11(SOC₀ 0.99 고정 · 자유 적합이면 SOC₀ 0.980 · ×1.084)이면 SOC RMS 0.050 → 0.008–0.009 · 재풀이 V 100 · 500 · 600 · 800 · 900 s 4.149 · 3.931 · 3.908 · 3.888 · 3.867 ↔ 그림 4.151 · 3.931 · 3.911 · 3.888 · 3.869 V(R14 · D8). V_meas 잡음 띠 p5/p95 −63 / +68 mV(G3).

## Fig. 8 — EKF3 의 전해질 농도 (p. 671 · 봤다 · 벡터 판독) ★★★ (c) · D6 · D7

Plant(실선) 6 곡선 · EKF3(점선) 6 곡선 — 마디 여섯(경계 둘 포함 · 가운데 마디 없음) · 'Interface between anode and electrolyte' · '… cathode and electrolyte' 표지. `[도표·벡터]` Plant t = 0 **10,904 · 10,818 ×4 · 10,732** · EKF3 t = 0 **11,880 ×3**(= 1.098 δc₀ — 인쇄 "1.1c_Li⁺(0)") + 9,558 · 8,694 · 11,016 · **여섯 마디 합 64,908 = 6 δc₀**(Plant · EKF3 모두 · t = 0 과 990 s — 990 s Plant 64,887 · EKF3 64,908) · 990 s EKF3 ↔ Plant ±70 mol m⁻³(12,155 ↔ 12,147 · 9,499 ↔ 9,482). ★ 1.1 배 초기값은 **EKF3** 의 것이다(인쇄 목록은 EKF4 줄 — D6) · 총량 보존이 마디 하나 이상을 정해 '독립 전해질 상태 3' 으로 읽힌다(P0 7×7 과 맞음 · 인쇄 Me − 1 = 4 와 다름 — D7 · `[해석]`). 5C 펄스 중 경계 마디 EKF3 이 Plant 를 넘거나 못 미친다(`[도표]` +≈250 · −≈200 mol m⁻³).

## Fig. 9 — 과전압 예측 오차 Δη = η_plant − η_est (p. 671 · 봤다 · 래스터 화소 판독) ★★★★ (b)

네 판 Δη_diff(±0.02) · Δη_mt(+0.01 … −0.02) · Δη_ct(×10⁻³ · +1 … −2) · Δη_total(±0.02 V) · EKF3(초록) · EKF4(빨강 점선). `[도표·화소]`(x 171 → 1381 px = 0 → 1000 s · 아래 판 y 839 = +0.02 · 975 = −0.02 — 1 화소 0.29 mV · 선 폭 ±0.6 mV) **EKF4 Δη_mt ≈−7 … −11 mV 지속**(50 s −7.4 · 400 s −10.0 · 700 s −10.6 · 900 s −9.9) · Δη_total 100–800 s −7.3 … −10.9 mV(850 s −6.5) · **EKF3 Δη_mt 300 s 뒤 ≈−1.1 … +0.2 · Δη_total −1.6 … +0.7 mV** · Δη_ct 두 EKF 거의 같음(≲−2×10⁻³ · 끝 ≈−1.5×10⁻³) · 900–960 s 초록 스파이크(+0.02). 본문 "the contribution of the mass-transfer overpotential to the total overpotential is not insignificant, which makes the EKF4 finds incorrect state values" 의 근거 그림 — 이 오차 ÷ OCV 기울기가 그림 7 의 EKF4 SOC 오차와 같은 크기다(R15).

## Table 1 — 매개변수 (p. 664 · 봤다 · 수동 단독 · 렌더로 지수 확인) ★★★★ (a) · D2 · D3

머리 "All Solid-State Battery Model Parameters **[15]**." · 열 'Parameters · Dimension · **Estimated value**' · 11 행: L 1500 nm · M 320 nm · A 1 cm² · c_Li⁺,0 6.01×10⁴ mol m⁻³ · δ 0.18 · k_r 0.9×10⁻⁸ m³ mol⁻¹ s⁻¹ · D_Li⁺ 0.9×10⁻¹⁵ · **D_n⁻ 2.1×10⁻¹⁵** · D_Li 1.76×10⁻¹⁵ m² s⁻¹ · **k_pos 5.1×10⁻⁴ m³ mol⁻¹ s⁻¹** · α_pos 0.6. 없는 것: c_Lis,max · c_Lis,min · c_Lis,0 · T · 1C 전류(G1 · G2). §(a) 1 에 행별 대조.

## Table 2 — 단순화 오차의 OAT (p. 669 · 봤다 · 수동 단독(각주 포함 재렌더)) ★★★★ (a) · (b)

열 'Parameter (Unit) · Reference Value · Sensitivity Range · Error · 10-C Constant(Model 2 · 3 · 4) · 10-C Pulse Relaxation(Model 2 · 3 · 4)' · 행 = 기준 + D_Li(1.76E-17 · 1.76E-13) · D_n⁻(**기준 5.1E-15** · 5.1E-17 · 5.1E-13) · k_pos(5.1E-4 · 5.1E-6 · 5.1E-2) · L(1.5E-6 · 1.1E-6 · 1.9E-6 m) · D_Li⁺(0.9E-15 · 0.9E-17 "Not converged" · 0.9E-13) × Max. Abs. · RMS(V). 각주 a "Comparison of the full-order model (Model 1) and Models 2, 3, and 4 for the reference values." · b "Convergence issue. It can be due to unrealistic values of diffusion coefficient of Li ions in electrolyte for lower than reference value." ⚠ k_r · δ 행 0 · L 만 ±27 %(나머지 ×10^±2) · `[재현]` D_Li⁺ ×1/100 이면 10C 에서 전해질 양극 쪽 마디가 ≈26 s 안에 고갈(정상 한계 전류 0.25C — 인쇄 값은 25.1C)이라 "Not converged" 는 물리적 고갈 구간이다(R13 · D21).

## 본문 서술과 어긋난 그림 · 표 (요약)

| 자리 | 서술 | 그림 · 표 | 판정 |
|---|---|---|---|
| 식 (14) ↔ 그림 3 · 2 | η_mt = (RT/F) ln[c(L)/c(0)] − ∫E dy | 그림 η_mt = −∫E 만(±0.3 mV) · 전압 폐합 ±0.4 mV | ❌ Nernst 항 없음(D1) |
| 표 1 ↔ 표 2 ↔ 그림 3 | D_n⁻ 2.1×10⁻¹⁵ | 표 2 기준 5.1E-15 · 그림 η_mt(0⁺) = 5.1 의 값 | ❌ 표 1 오기 또는 다른 출처(D2) |
| 초기값 목록 ↔ 다음 문장 ↔ 그림 8 | 1.1c_Li⁺(0) 이 EKF4 줄 · "not required for the EKF4" | EKF3 셋이 11,880 출발 | ❌ 줄 바뀜(D6) |
| 상태 정의 ↔ P0 | Me = Mp = 5 → 4 + 4 | P0 7×7 · Q_w 3 + 1 + 3 · 그림 8 총량 보존 | ⚠ 차원 7 의 근거 미인쇄(D7) |
| 그림 7 ↔ 그림 2–6 | 전류 5C · 2.5C(같은 1C 정의) | Actual SOC 가 ×1.10–1.11 빠름 | ⚠ C-rate 기준 다름(D8) |
| 초록 · 결론 "40% reduction … from 9% to 5%" | 40 % | (9 − 5)/9 = 44 % · % = SOC 절대 %p | ⚠ 반올림 · 정의(D10) |
| 본문 "six critical parameters" | 여섯 | 표 2 다섯 · 바로 앞 문장도 다섯 | ⚠(D11) |
| 본문 "Model 3 is more accurate than Model 4 … as shown in Figs. 4–7" | 그림 4–7 | 그림 4 = 농도 단면 · 그림 7 = EKF | ⚠ 참조 범위(D13) |
| 2.4 "relative absence of a plateau at nominal voltage" | 평탄 없음 | 그림 2 의 ≈3.88 V 평탄 · 식 (22) 평탄 SOC 0.1–0.4 | ⚠ 문장(D20) |
| 표 2 각주 b | "unrealistic values … convergence issue" | `[재현]` ≈26 s 고갈 · 한계 전류 0.25C | ⚠ 물리 고갈(D21) |
| 그림 5 · 6 x 축 | — | 'Time (t)' | 표기 |

---

# 절별 해체 (본문)

## 초록 · 1. Introduction (p. 663–664)

`[인쇄]` 동기: 액체 LIB 의 안전 문제 → 고체 전지("superiority in terms of thermal stability with their improved power and energy density, and cycle life [4]") · 고체 전지 모형화가 적다("not much effort has been spent on modeling solid-state battery systems") — 선행 셋: [10](Danilov — "one-dimensional mathematical model for a Li|Li3PO4|LiCoO2 cell … validated using galvanostatic discharging of a micro-battery with a capacity of **10 mAh**" ↔ 91호 공칭 **10 µAh**(91호 digest 전사 — ×1000 · D9)) · [11](Fabre — Li|LiPON|LiCoO2 마이크로배터리 · GITT · EIS 로 매개변수 · 정전위 · 정전류 검증) · [12](Nesro & Elfadel — 국소 · 전역 전기중성 가정의 단순화 · 유한차분 · 1C 에서 [10] 과 비교 — "the accuracy of this modeling approach was not investigated at high C-rate"). 기여 둘: ① 단순화 접근과 전압 예측 성능 ② EKF 로 SOC 추정 — "the effectiveness of the EKF-based SOC estimation for a solid-state battery system has not been studied yet to the best of authors knowledge." 서론에 관측성 · 식별성 · 열화 낱말 0.

## 2. Solid-state battery model · 2.1 Electrolyte (p. 664–665 · 그림 1 · 표 1 · 식 1–8)

`[인쇄]` "To capture the dynamics of the solid-state battery, the model presented in Ref. [10] is used in this study" · "this modeling approach assumes that Ohmic drops across the Li metal anode and the current collectors are insignificant and hence ignored [10]" · "Table 1 provides the parameters of the considered solid-state battery. It should be noted that the validity of the parameters was experimentally demonstrated in Ref. [10]." 전해질: Li⁰ ⇌ Li⁺ + n⁻(k_r · k_d) · 식 (1) ∂c/∂t = [2D_Li⁺D_n⁻/(D_Li⁺ + D_n⁻)] ∂²c/∂y² + r · (2) c(y, 0) = δc_Li⁺,0 · (3)(4) 두 끝 모두 ∂c/∂y = −i/(2FAD_Li⁺) · (5) r = αc² + βc + γ · (6) α = −k_r · (7) β = −k_r c_Li⁺,0 δ²/(1 − δ) · (8) γ = k_r c_Li⁺,0 δ²/(1 − δ). `[재현·대수]` r(δc₀) = 0 이 되려면 γ = k_r c₀² δ²/(1 − δ) 여야 한다 — 인쇄 (8) 은 c₀ 하나가 빠져 차원(s⁻¹)이 r(mol m⁻³ s⁻¹)과 다르다(D5). 그리고 (5)–(6) 의 α 는 BV 의 α_pos 와 같은 글자다(D17).

## 2.2 Cathode (p. 665 · 식 9–12 · SOC)

`[인쇄]` "LiCoO2 ⇌ Li1−zCoO2 + zLi⁺ + ze⁻ (0 ≤ z ≤ 0.5)" · "Only diffusion of Li⁺ ions due to concentration gradient is considered in the cathode" · (9) Fick · (10) c(y, 0) = c_Lis,0 · (11) D_Li ∂c(L, t)/∂y = −i/(FA) · (12) 뒷면 0 · SOC(t) = (c_Li,max − c̄(t))/(c_Li,max − c_Li,min) · c̄ = (1/M)∫_L^{L+M} c dt(**dt** — dy 의 오기 · D14). c_Li,max · c_Li,min 값 0(G1).

## 2.3 Overpotential computations (p. 665–666 · 식 13–23)

`[인쇄]` η_t = η_ct + η_mt + η_d(13) · (14) η_mt = (RT/F) ln[c(L,t)/c(0,t)] − ∫₀ᴸ E dy · (15) E = (RT/F)(1/c)(i/(2FAD_Li⁺) + [(D_Li⁺ − D_n⁻)/(D_Li⁺ + D_n⁻)][∂c/∂y + i/(2FAD_Li⁺)]) — `[재현·대수]` 이원 전기중성 Nernst–Planck 에서 n⁻ 차단 경계를 두고 유도하면 같은 꼴이 나온다(부호 ✅) · "The charge transfer overpotential η_ct cannot be simply computed by inverting the Butler-Volmer equation (16) since α_pos is 0.6; therefore, η_ct needs to be numerically determined using a root-finding scheme." · (16) i = −i₀(e^{αFη/RT} − e^{−(1−α)Fη/RT}) · (17) i₀ = FAk_pos[(c_max − c)c_Li⁺/((c_max − c_min)c_Li⁺,0)]^α[(c − c_min)/(c_max − c_min)]^{1−α} — `[재현·대수]` 인쇄 단위(k_pos m³ mol⁻¹ s⁻¹)로 F·A·k_pos = C m⁵ mol⁻² s⁻¹ 이라 전류가 아니다(D4) · c_Li⁺/c_Li⁺,0 의 c_Li⁺,0 은 표 1 의 총 농도(6.01×10⁴)라 t = 0 에서 비 = δ = 0.18(R8 이 이 해석으로 닫힌다) · (18) η_d = Eeq(θ_s) − Eeq(θ̄) · (19)–(21) θ 정의 · (22) Eeq(θ) = (−219.027 + 322.003θ² − 198.242θ⁴ + 354.911θ⁶ − 467.807θ⁸ + 207.168θ¹⁰)/(−44.337 + 36.643θ² − 3.430θ⁴ + 113.081θ⁶ − 182.567θ⁸ + 80.3097θ¹⁰) — "from experimentally obtained equilibrium potential of the cathode in Ref. [11]" · (23) V_t = Eeq(θ̄) + η_tot.

## 2.4 Model performance (p. 666 · 그림 2 · 3)

`[인쇄]` "terminal voltage profiles at different discharge currents are obtained by solving the governing equations with the COMSOL Multiphysics 5.3a (see Fig. 2). This is in compliance with experimental discharge profiles of solid-state batteries." — 비교 실험 그림 · 인용 0((햐)). 그림 3: "Diffusion overpotential is the major contributing factor to the shape of the total overpotential" · "Charge transfer overpotential on the other-hand … has a very low value" · "The value of charge transfer at the negative electrode is neglected as the negative electrode is Li metal [10]."

## 2.5 Model simplification (p. 666–669 · 식 24 · 그림 4–6 · 표 2)

`[인쇄]` 모형 1 = 전체 · 2 = r 없음 · 3 = 2 + α_pos 0.5 · 4 = 3 + c_Li⁺ 상수. 근거: ① r 은 c 의 2차라 비선형 — 없으면 "the PDE (1) can be converted into a set of simple linear ordinary differential equations via numerical discretization" ② 경계 (3)(4) 때문에 "the mobile lithium concentration in the electrolyte region at the mid-node point becomes constant as shown in Fig. 4" · "Under the assumption that there is no side reaction occurring between the negative electrode-electrolyte-cathode, the total number of lithium ions deposited into the electrolyte at L = 0, equal to the total number of lithium ions deposited at the interface between the electrolyte and cathode" ③ α 0.5 → (24) η_ct = (2RT/F) sinh⁻¹(i/(2i₀)) — "the Jacobian matrix of the output function can be analytically expressed and hence an EKF can be applied" ④ 모형 4 = "Reducing the number of state variables is another important aspect when developing and implementing real-time estimation algorithms" · "the contribution of the mass-transfer overpotential to the total overpotential is small in the relatively high SOC (or voltage) ranges (see Fig. 3)" — 그림 3 의 η_mt 는 −6 … −20 mV 로 η_total(−28 … −62 mV)의 15–68 %(1–300 s)라 '작다' 는 SOC 구간 · 시간에 걸린다(`[도표·벡터]`). 오차: 10C 정전류 RMS 0.0002 · 0.0025 · 0.0143 V · 최대 0.0005 · 0.0233 · 0.0435 · 펄스 RMS 6.9E-05 · 0.0005 · 0.0049 · 최대 8.9E-05 · 0.0027 · 0.0099 V · "the accuracy of Model 4 in predicting voltage is still less than 45 mV and it could be small when the battery is moderately charged, i.e., SOC > 0.4." 감도: "kpos, DLi+, Dn, DLi and L are critical parameters … the variation range estimated from the previous literature can be several orders of magnitude [10,11,16–18]" · "Fabre et al. in Ref. [11] claim that the lithium diffusion coefficient in Li2CoO2 is one to two orders of magnitude lower than usual values reported for this material [16]"('Li2CoO2' 인쇄 그대로 — D15) · "Sensitivity analysis is typically performed to understand the influence of uncertainty in model parameters on the output of a mathematical model, and hence it has been widely used in studies on assessing parameter identifiability or estimability [19,20]" · OAT [22, 23] · 결론 "these extreme parameters are typically not physically realistic, so it can be concluded that the simplifications described in this paper are acceptable for most of actual performance calculation of a battery."

## 3.1 Control-oriented model (p. 670 · 식 25–27)

`[인쇄]` 유한차분("similarly to that used in Ref. [7]") — (25) 전해질 마디 · (26) 양극 마디 · "j = 1, …, Ne and l = 1, …, Ns − 1" · "The boundary conditions (3) and (4) are applied to the two extreme node points" · "the term r in Eq. (5) … is not included" · (27) x_{k+1} = A_d x_k + B_d u_k · y_k = h(x_k, u_k) · x = [x^e, x^s] · x^e = [c_Li⁺,1 … c_Li⁺,Me−1] · x^s = [c_Lis,1 … c_Lis,Mp−1] · "Me = Mp = 5". 인덱스 이름이 N_e · N_s ↔ M_e · M_p 로 두 벌이다 · Δt 0(G4).

## 3.2 EKF-based state estimation (p. 670 · 식 28)

`[인쇄]` 표준 EKF(시간 갱신 x̄_k = A_d x̂_{k−1} + B_d u_{k−1} · P̄_k = A_d P_{k−1} A_dᵀ + Q_w^s / 측정 갱신 K_k · x̂_k = x̄_k + K_k(y_k^m − y_k) · P_k = [I − K_k C_k]P̄_k) · "Covariance matrices Q_w^s and R_v are determined by zero-mean Gaussian noise in process and measurement respectively. The matrix C_k is the Jacobian matrix of partial derivatives of h(·) with respect to x." · 3.2.1 EKF4: 모형 4 · x^s 만 · "the output function h̃ is different from h in computing the charge transfer overpotential in Eq. (27) and the mass transfer overpotential from the following:" (28) η_mt,k = −LRT/(c_Li⁺F²A(D_Li⁺ + D_n⁻)) u_k(균일 농도 옴 강하) · 3.2.2 EKF3: 모형 3 · "the contribution of mass transfer in the electrolyte to the total overpotential becomes significant for long discharge (or charge) battery operation."

## 3.3 Performance comparison (p. 670–671 · 그림 7–9)

`[인쇄]` "In battery simulation, a discharge operation shown in Fig. 7 is considered: the applied current and output voltage are measured and used for both EKF estimators. The Li-ion concentration of the plant model (or the original PDE model) is used to verify the accuracy of the state estimation." 초기값: Plant SOC₀ 0.99 · c_Li⁺(0) = δc_Li⁺,0 / EKF3 SOĈ₀ 0.8 / EKF4 SOĈ₀ 0.8 · ĉ_Li⁺(0) = 1.1c_Li⁺(0) — "Note that initial conditions of the electrolyte are not required for the EKF4 and hence the nominal value is used" · "The initial condition of the error covariance matrices P0, Qw and Rv for the EKFs are tuned in consideration of the tradeoff between noise rejection and convergence rate through repeated simulations" · 결과 문장은 판정 1 에 전사 · "EKF3 can estimate properly the electrolyte concentration as seen from Fig. 8. Consequently, the prediction accuracy of corresponding overpotentials can be significantly improved, leading to better accuracy in SOC estimation (5% error) even in the weakly observable SOC range (see Fig. 9). Nonetheless, EKF3 still suffers from weak-observability in the low SOC range due to modeling error caused by coarse discretization of the control-oriented model, which will be investigated as future work."

## 4. Conclusions (p. 672)

`[인쇄]` "Sensitivity analysis demonstrated that the simplified models have sufficient accuracy in the voltage prediction" · "Nonetheless, the battery system's inherent characteristics, a plateau in the low SOC ranges (0.1 < SOC < 0.4), make the state estimation to be challenging. This challenge can be addressed by including the diffusion dynamics at the electrolyte for better accuracy in estimation. Specifically, a 40% improvement (from 9% to 5% error) in state-of-charge estimation could be achieved for the considered simulation study." · "Future work will investigate approaches to improving the performance of state estimation by using a trajectory of voltage measurement over a time interval instead of a single point measurement to address weak unobservability." — 마지막 문장이 [[data-window-identifiability]] 의 '창' 처방과 같은 말이다(`[해석]` · 실행 0).

---

# ★ (a) 모형과 단순화 셋 — 출처 · 근거 · 오차

## 1. 표 1 행별 — 출처 층위 (`[인쇄]` 표 1 ↔ 91호 표 II(91호 digest 전사) ↔ 이 편 그림이 요구하는 값(`[재현]`))

| 행 | 표 1(이 편) | 91호 표 II(층위) | 그림 · 재풀이가 요구하는 값 | 판정 |
|---|---|---|---|---|
| L · M · A | 1500 nm · 320 nm · 1 cm² | 같음 · 각주 "Design parameters" | 같음(그림 1 · 4) | 설계값 상속 |
| c_Li⁺,0 | 6.01×10⁴ | 같음 · **NDP 측정** | 같음(그림 4 초기 δc₀ 10,818) | 측정값 상속 |
| δ | 0.18 | 같음 · model optimization | 같음 | 91호 적합값 |
| k_r | 0.9×10⁻⁸ m³ mol⁻¹ s⁻¹ | 같음 · model optimization · **91호 재풀이: Danilov 자기 그림은 ×100 필요** | 0.9×10⁻⁸ 이어야 표 2 M2 0.5/0.2 mV 가 나온다(R11) | 91호 인쇄값 그대로 — ×100 문제 상속 |
| D_Li⁺ | 0.9×10⁻¹⁵ | 같음 · 적합 | 같음 | 91호 적합값 |
| **D_n⁻** | **2.1×10⁻¹⁵** | **5.10×10⁻¹⁵** · 적합 | **5.1×10⁻¹⁵**(R4 · 표 2 기준) | ❌ 표 1 만 다름(D2) |
| D_Li | 1.76×10⁻¹⁵ | 같음 · 적합 | 같음(그림 2 끝 시각 · R7) | 91호 적합값 |
| **k_pos** | **5.1×10⁻⁴ m³ mol⁻¹ s⁻¹** | k₁ˢ **5.1×10⁻⁶ m^2.8 mol^−0.6 s⁻¹** · 적합 · 인쇄 단위로 i₀ 재현 불가 | F·A·k_pos 수치(A m²)로 i₀ 0.28–0.88 mA — R8 이 0.0027 V 를 정확히 냄 | ⚠ ×100 · 단위 변경 · 출처 미인쇄(D3 · D4) |
| α_pos | 0.6 | 같음 · 적합 | 같음(R8) | 91호 적합값 |
| c_max · c_min | **미인쇄** | a_max 2.33×10⁴ = 공칭 10 µAh ÷ (F · 0.5 · M · A)(용량 맞춤 유도) | 2.33×10⁴ · c_max/2(그림 4 · R3) | 91호 유도값 — 표에서 빠짐(G1) |
| T | **미인쇄** | 25 ℃(측정 조건) | 298.15 K(R7) | 공백(G2) |
| 평형 곡선 | 식 (22) — **[11] Fabre** | 같은 셀 방전 곡선 네 율 회귀 외삽 | 식 (22) 로 V − Eeq 폐합 ±0.4 mV(R6) | ⚠ 곡선 교체 — 매개변수는 91호 EMF 로 맞춘 값(판정 7) |

⇒ **표 1 은 91호의 설계 3 · 측정 1 · 적합 6 · (유도 1 누락) 위에 값 하나(D_n⁻)가 다르고 하나(k_pos)가 다른 관례로 바뀐 표**다. 머리 "[15]" 는 Tian & Qi 2017 *JES* 164, E3512(접촉 면적 손실 모의 — 미열람)이다. 본문 "the validity of the parameters was experimentally demonstrated in Ref. [10]" 의 [10] 검증은 91호 모형 · 91호 EMF · 91호 셀 자료 위의 것이고(91호 digest 전사: 그 '좋은 일치' 도 고율 끝 용량 22–27 % 미달 · k_r ×100), 이 편 조합(다른 평형 곡선 · 다른 D_n⁻ 표기 · 다른 k_pos 관례)으로 옮겨지지 않는다 — 이 편은 그 차이를 언급하지 않는다(G10 · G11).

## 2. 단순화 셋 — 근거와 오차 (`[인쇄]` 표 2 · 본문 → `[재현]`)

| 단순화 | 인쇄 근거 | 인쇄 오차(10C 정전류 · 펄스 — 최대 / RMS V) | `[재현]` 조건 | 판정 |
|---|---|---|---|---|
| (1) SE 안 생성 · 재결합 무시(모형 2) | r 이 2차라 비선형 · 모형 1 과 "no significant changes" | 0.0005 / 0.0002 · 8.9E-05 / 6.9E-05 | 인쇄 k_r 에서 0.49 / 0.19 mV ✅ · **k_r ×10 → 4.19 / 1.62 · 8.0×10⁻⁷ → 14.82 / 6.50 · ×100 → 15.33 / 6.77 mV** · 펄스 ×100 → 2.89 / 1.89 · 표 2 에 k_r · δ 행 0 | ⚠ 인쇄 k_r(91호 그림과 ×100 어긋난 값)에서만 '무시 가능' — `[재현·가정]` 재결합 시간 1/(2k_rδc₀ + k_d) 77 분(인쇄) ↔ 46 s(×100) — 10C 방전 6 분보다 길면 무시되고 짧으면 아니다 |
| (2) α_pos 0.5(모형 3) | BV 를 sinh⁻¹ 로 풀어 해석 야코비안 · "no significant impact on the kinetic" | 0.0233 / 0.0025 · 0.0027 / 0.0005 | 펄스 최대 0.0027 = t = 0⁺ 한 점(SOC 0.99 — R8) · 정전류 최대 = 방전 끝(c → c_max) · I/i₀ 가 작을수록 차가 작다(k_pos ×100 → 0.0002) · k_pos ×1/100 → **0.0869** | ✅ 기준 근방 · ⚠ 오차가 I/i₀ 에 매달린다 — 열화로 A·k_pos ↓ 면 커지는 방향을 '비현실' 로 배제 |
| (3) 전해질 균일 농도(모형 4) | 상태 수 감소 · 고 SOC 에서 η_mt 몫 작음 | 0.0435 / 0.0143 · 0.0099 / 0.0049 | 식 (14) 그대로(Nernst 항 포함)면 **58.26 / 27.61 · 18.85 / 7.96 mV**(R12) · 그림판(우리 재풀이) 39.0 / 13.0 · 8.6 / 3.4 mV | ⚠ 플랜트의 항 누락이 오차를 ≈절반으로 보이게 한다(D1) |

## 3. 재풀이 폐합 (`[재현]` — 우리 수치 풀이 · 저자 코드 아님 · 스크립트는 scratchpad)

입력: 표 1(단 D_n⁻ = 5.1×10⁻¹⁵) · c_max 2.33×10⁴ · c_min = c_max/2 · SOC₀ 0.99 · T 298.15 K · 1C = F·A·M·(c_max − c_min)/3600 = 9.99 µA · i₀ = 식 (17) 수치(A m²) · 전해질 유한체적 120 칸 · 양극 60 칸 · BDF · η_mt = 식 (14) **둘째 항만**(그림이 그렇다 — R5).

| 시각(10C) | V 재풀이 ↔ 그림 2 | η_ct ↔ 그림 3 | η_mt ↔ 그림 3 | η_d ↔ 그림 3 |
|---|---|---|---|---|
| 1 s | 4.2456 ↔ 4.2456 | −5.98 ↔ −5.97 | −7.00 ↔ −6.99 | −20.02 ↔ −20.04 |
| 10 s | 4.1976 ↔ 4.1975 | −4.38 ↔ −4.38 | −8.83 ↔ −8.83 | −44.19 ↔ −44.21 |
| 50 s | 4.0950 ↔ 4.0949 | −3.58 ↔ −3.57 | −12.18 ↔ −12.19 | −44.34 ↔ −44.36 |
| 100 s | 3.9950 ↔ 3.9948 | −3.42 ↔ −3.42 | −14.73 ↔ −14.73 | −34.66 ↔ −34.67 |
| 200 s | 3.8887 ↔ 3.8885 | −4.00 ↔ −4.00 | −17.88 ↔ −17.89 | −9.84 ↔ −9.81 |
| 300 s | 3.8310 ↔ 3.8301 | −7.95 ↔ −7.98 | −19.54 ↔ −19.55 | −24.75 ↔ −25.20 |

3.4 V 도달 5 · 10 · 20C 691.63 · 335.77 · 157.84 ↔ 그림 2 689.40 · 334.56 · 157.18 s. ⇒ **인쇄 표 1 은 D_n⁻ 하나만 고치고(그리고 빠진 c_max · c_min · T 를 91호에서 가져오면) 저자 그림을 닫는다 — 단 인쇄 식 (14) 가 아니라 그 둘째 항만으로.** Nernst 항을 넣으면 같은 입력으로 300 s V 가 18.7 mV 낮고(3.8123 V) 3.4 V 도달이 335.59 s 다 — 그림 2 · 3 과 안 맞는다.

---

# ★ (b) 관측성 — 무엇으로 보였나 · Q4

## 1. 이 편이 보인 것 (`[인쇄]`)

- **논증 하나** — "the equilibrium potential has a plateau, making the Jacobian to be almost zero and hence the battery system becomes very weakly observable"(p. 671). 관측성 행렬 · 랭크 · Gramian · 조건수 · 야코비안 값 · CRB **0**.
- **합성 실행 하나** — 그림 7(SOC 오차) · 그림 9(과전압 오차). 플랜트 = 같은 모형 계열의 PDE · 측정 잡음 값 미인쇄 · 실현 · 실행 수 미인쇄(G3 · G7).
- **처방 둘** — ① 전해질 동역학 포함(EKF3) ② 미래 과제: "a trajectory of voltage measurement over a time interval instead of a single point measurement".
- 대상은 **상태(SOC · 농도 마디)** 다 — 매개변수(열화 · 접촉 · 용량)의 식별성은 다루지 않는다. 식별성 낱말은 한 문장("assessing parameter identifiability or estimability [19,20]")에서 표 2 의 동기로만.

## 2. 우리가 공급하는 것 (`[재현]` — 지면에 없는 계산)

| 무엇 | 값 | 뜻 |
|---|---|---|
| 평탄 위치 · 기울기(식 22 · θ = 1 − SOC/2) | \|dE/dSOC\| 최소 **0.072 V/SOC @SOC 0.28** · SOC 0.1–0.4 중앙 0.126(0.072–0.693) · 0.4–0.99 중앙 0.658 · 0.7–0.99 중앙 0.845 · ≤0.17 V/SOC 인 창 SOC 0.195–0.399(≤0.10 은 0.233–0.340) | 평탄 창의 위 끝은 인쇄 범위(0.4)와 같고 아래 끝은 0.2 쪽 · "거의 0" = 고 SOC 의 1/12.5(∂E/∂θ 0.143 ↔ 1.79 V) |
| 단일 점 감도(분산 쪽 · `[재현·가정]` σ_V 31.6 mV = R_v 10⁻³ V² 가정) | σ_SOC = σ_V/\|dE/dSOC\| — SOC 0.28 **0.44** ↔ SOC 0.9 **0.035** | 점 하나로는 평탄에서 SOC 를 못 정한다 — 필터는 과정 모형(쿨롱 적분)으로 버틴다 |
| 편향 사상(편향 쪽) | ΔSOC ≈ Δη_total/\|dE/dSOC\| — EKF4 600 s −0.045 ↔ −0.048 · 750 s −0.123 ↔ −0.084 · 800 s −0.084 ↔ −0.087 · 850 s −0.046 ↔ −0.068 · 200–400 s −0.010 … −0.022 ↔ −0.021 … −0.034 | **9 % 는 모형 불일치의 증폭** — 분산이 아니다 |
| EKF3 의 남은 오차 | 예측 ≤0.02(Δη ≈−1.6 … +0.7 mV) ↔ 실측 −0.018 … −0.046 | 출력이 맞아도 벌크가 어긋나는 축 — 저자의 '거친 이산화의 모형 오차' 설명과 같은 방향(`[해석]`) |

⇒ `[해석]` **약한 관측성은 오차의 원천이 아니라 증폭기다.** 같은 모형 불일치(≈10 mV)가 SOC 0.9 에서는 ≈0.011, SOC 0.28 에서는 ≈0.14 의 편향이 된다. 미래 과제의 '궤적 창' 은 분산(σ_SOC)을 줄이지만 **모형 불일치가 만든 편향은 창으로 줄지 않는다** — 창 안의 모든 점이 같은 쪽으로 어긋나기 때문이다([[data-window-identifiability]] 99호 절).

## 3. 어휘 (NFKC · 줄 끝 분철 복원 뒤 · 쪽 머리 · 바닥 제외 · 본문 = 제목 → 사사 앞 · 초록 · 캡션 · 표 포함 | 참고문헌)

| 낱말 | 본문 | 참고문헌 | 쓰임 |
|---|---|---|---|
| `observab*` | **5**(그중 `unobservab*` 1) | 0 | 초록 "weak observability" · "very weakly observable" · "weakly observable SOC range" · "weak-observability" · 결론 "weak unobservability" |
| `identif*` · `estimab*` | 1 · 1 | 0 | 같은 한 문장 — "assessing parameter identifiability or estimability [19,20]" |
| `Jacobian` | 3 | 0 | 해석 야코비안의 이점 · C_k 정의 · "Jacobian to be almost zero" |
| `sensitiv*` | 14 | 2 | 키워드 · 초록 · 표 2 제목 · 열 이름 · OAT · "sensitive to kpos …" |
| `uncertain*` | 1 | 0 | "influence of uncertainty in model parameters" |
| `covarian*` · `noise` | 3 · 2 | 0 | EKF 공분산 · "zero-mean Gaussian noise" · "noise rejection" |
| `uniqu*` · `confiden*` · `±` · `residu*` · `correlat*` · `Fisher` · `Hessian` · `Gramian` · `rank` · `variance` · `bias` · `Monte` | **0** | (`bias` · `variance` 각 1 = [19] 제목) | — |
| `error*` · `RMS` · `accura*` | 24 · 14 · 14(+`inaccura*` 1) | 1 · 0 · 0 | 모형 오차 · SOC 오차 |
| `validat*` · `valid*` | 3 · 7 | 0 | "the validity of the parameters was experimentally demonstrated in Ref. [10]" · "show the validity of the approaches" · "In order to validate these four models" — 비교 축 = 모형 1(계산 ↔ 계산) |
| `experiment*` · `measur*` · `simulat*` | 4 · 5 · 7 | 0 · 0 · 2 | 실험 자료 0 — "experimentally" 는 남의 편 소개 · "measured" 는 합성 측정 |
| `plateau` · `weak*` | 5 · 5 | — | — |
| `contact*` · `degrad*` · `ag(e)ing` · `pressure` · `temperature` | **0** · 0 · 0 · 0 · 0 | 1(Tian & Qi 제목) · 0 · 0 · 0 · 2 | 열화 · 접촉 축 0 |
| `capacity` | 1 | 0 | "[10] … a capacity of 10 mAh" |
| `real-time` · `comput*`(시간 뜻) | 1 · 0 | — | 계산 비용 보고 0(G8) |

## 4. 판정 — Q4 0/99 · 아흔한 번째 성질 · 공백 1번 후보 확인

- 위키 grep(`observab*`) 기준 **ASSB 대상 1차 계산 편 가운데 관측성을 추정 실패의 원인으로 인쇄한 첫 편**이다 — 앞의 셋(34호 논평 · 8호 종설 · 96호 액체 도구)은 1차 ASSB 계산이 아니고, 27호의 'observable' 은 '눈에 보인다' 뜻 · 92호는 34호 문장의 전사다. 그러나 Q4 의 기준(이 조합이 이 데이터로 유일하게 정해지지 않음을 **계산으로** 보인 편)에는 닿지 않는다: 계산 0 · 대상이 상태 · 열화 손잡이 0.
- **아흔한 번째 성질** = **"관측성(observability)을 ASSB 지면에 처음 인쇄한 1차 계산 편 — 그러나 관측성 행렬 · Gramian · 야코비안 값 · CRB 0: 근거는 OCV 평탄 논증과 같은 모형 계열 합성 플랜트 위 EKF 실행 하나(잡음 · Δt · 실현 수 미인쇄)이고, 대상은 상태(SOC)이지 열화 매개변수가 아니며, 9 % 는 분산이 아니라 축약 모형의 출력 오차(≈−7 … −11 mV)가 평탄 기울기(0.07–0.09 V/SOC)로 증폭된 편향이다 — 그리고 '민감도 분석' 은 식별성 문헌([19, 20])을 동기로 들고 축약 오차의 OAT 견고성만 쟀다."** — 26호 열아홉 번째 성질("평탄을 스스로 계산해 놓고 평탄 위의 점을 값으로 인쇄")의 **상태 추정판**: 평탄을 이름 붙였으나 재지 않았다.
- **원장 §2 공백 1번 — 후보 목록의 Kim 2019 는 식별성 편이 아니다**(75호 Naik · 92호 Firouz 닫음과 같은 형식): 상태 추정 · 관측성 계산 0 · 매개변수 식별 0 · 열화 손잡이 0 → Q4 0/99(분모 +1 · 채움 0). 목록에서 지우지 않고 이 확인으로 닫는 것을 제안한다(wiki 밖 — 호출자 몫).
- 누적 0.5 그대로.

---

# ★ (c) EKF 설계 — 상태 · 잡음 · 초기 오차 · 자료

| 축 | EKF4(양극만) | EKF3(전해질 포함) | 근거 · 판정 |
|---|---|---|---|
| 모형 | 모형 4 — 양극 확산 유한차분 + 식 (28) 옴 η_mt | 모형 3 — 전해질 + 양극 유한차분(r 없음 · α 0.5) | `[인쇄]` |
| 상태 | x^s 넷(Mp − 1) | 인쇄 x^e(Me − 1 = 4) + x^s(4) = 8 ↔ P0 **7×7** | ⚠ D7 · `[도표·벡터]` 총량 보존 → 독립 전해질 3 + 4 = 7 로 읽힘 |
| 출력 · 야코비안 | V_t · C_k 해석(α 0.5 덕분 — 식 24) · h̃ 의 η_ct 차이 미인쇄 | V_t · C_k 해석 | G6 |
| P0 | I₄ₓ₄ | I₇ₓ₇ | 단위 미인쇄 · 초기 오차(SOC 0.19 ≈ 2,200 mol m⁻³)에 비해 아주 작다 — 실제 수렴은 Q_w 가 연다(`[해석]`) |
| Q_w | 10 I₄ₓ₄ | Diag(10⁻³I₃ₓ₃, 9·10³, 10⁴I₃ₓ₃) | "tuned … through repeated simulations" · Δt 미인쇄(G4) |
| R_v | 10⁻³ | 10⁻³ | 플랜트 잡음 미인쇄(G3) · 그림 띠 σ ≈30–40 mV 수준 |
| 초기 | SOĈ₀ 0.8(플랜트 0.99) | SOĈ₀ 0.8 · 전해질 마디 셋 1.1 δc₀(그림 8) | 인쇄 목록은 1.1 배를 EKF4 줄에(D6) |
| 자료 | 합성 — 플랜트 "original PDE model" + 측정 잡음 · 실험 0 | 같음 | 실행 하나 · 산포 0(G7) |
| 결과(그림 7 `[도표·화소]`) | ≈100 s 수렴 · SOC 0.1–0.4 오차 −0.084 … −0.087(인쇄 "9%") | ≈150 s 수렴 · −0.043 … −0.046(인쇄 "5%") | "40%" = 44 %(D10) |

⇒ `[해석]` **합성 진실 = 축약 모형의 더 큰 판**이다(같은 매개변수 · 같은 평형 곡선 · 같은 1D) — 추정기와 플랜트의 차는 r · α · 전해질 단면 · 이산화뿐이고, 매개변수 불일치 · 열화 · 잡음 모형 불일치는 시험되지 않았다. 그리고 플랜트 자체가 식 (14) 의 Nernst 항 없이 계산돼(D1) 전해질 분극의 ≈절반이 두 추정기 모두에서 '시험 밖' 이다.

---

# ★ (d) 접촉 · 용량 손잡이 — 37호 물음

| 손잡이 | 이 편 모형의 자리 | 추정기에서 | 판정 |
|---|---|---|---|
| **용량**(LAM · 활성 질량) | c_max − c_min · M · A(전부 고정 · c_max · c_min 미인쇄) · SOC 정의의 분모 | 상태 아님 · 매개변수 추정 아님 | **손잡이 없음** — 플랜트 용량이 줄면 쿨롱 적분과 전압이 어긋나 농도 상태가 움직이는 것으로만 흡수된다(`[해석]`) |
| **접촉**(A_eff · 표면 피복) | A 한 값이 식 (3) · (4) · (11)(플럭스 밀도)과 식 (17) F·A·k_pos(교환 전류) 모두에 | 상태 아님 · 매개변수 추정 아님 | **손잡이 없음** — `[재현·가정]` A_eff ×0.5 → 10C 중간 SOC Δη_ct ≈−2.9 mV → SOC 편향 평탄 −0.040 · SOC 0.4 위 −0.0044 |
| 동역학 상수 k_pos | 표 1 고정 · 표 2 ×1/100 행(모형 3 오차 86.9 mV)을 '비현실' 로 배제 | — | 열화 방향의 견고성 미시험 |
| 전해질 수송(D_Li⁺ · D_n⁻ · L) | 표 1 고정 · 표 2 OAT | EKF3 상태 = 농도 단면 | 전해질 열화(전도도 ↓)도 손잡이 없음 |

⇒ **37호 물음의 답: 이 추정기는 접촉 · 용량을 상태로도 매개변수로도 두지 않는다 — 둘 다 '모형 불일치' 라는 한 통로로만 들어오고, 그 통로의 출구는 SOC 편향(평탄에서 ×10 증폭)이다.** 카드 물음(OCV 맞춤이 LAM_PE 와 접촉 손실을 가르는가)의 상태 추정 층 표본: 전압 하나 · 고정 매개변수 추정기에서는 둘이 같은 편향 통로를 쓴다(`[해석]` · 이 편은 열화를 다루지 않는다).

---

# (e) Q1–Q8 — 채움표 칸 (닻 카드 수집 지침)

| Q | 칸 | 이 편 |
|---|---|---|
| Q1 정량 | **해당 없음 — `θ(N)` 0/99** | 조밀 평판 · 열화 0 · `contact*` 본문 0 · 층 하나: 식 (17) F·A·k_pos — 면적 · 속도 상수 한 곱(접촉 손실이 들어갈 자리는 k_pos 이름) · 표 2 k_pos ×1/100 영역(α 0.5 단순화 실패 86.9 mV)을 '비현실' 로 배제 |
| Q2 분리 관측 | **없다** | 관측 = 전압 하나(+ 전류) · 관측 추가 0 · 처방은 모형 구조(전해질 포함)와 미래 과제(궤적 창) |
| Q3 라벨 층위 | **칸 없음 · 층 하나** | "합성 플랜트 = 같은 계열 1D PDE(COMSOL) · 인쇄 식 (14) 의 Nernst 항 없이 계산(그림 3 · 4 · 2 폐합 ±0.3–0.4 mV · 재풀이 ±0.5 mV) · 표 1 출처 [15] ↔ 본문 [10] · D_n⁻ 표 1 2.1 ↔ 그림 5.1 · 91호 적합값(인쇄 k_r 포함) + Fabre OCV 혼성 · 실험 0" |
| Q4 유일성 | **0/99 — 아흔한 번째 성질** | 위 §(b) 4 · 관측성 논증 + 합성 실행 하나 · 계산 0 · 대상 상태 · 누적 0.5 그대로 |
| Q5 기준 전위 | **해당 없음** | Li 금속 · "The value of charge transfer at the negative electrode is neglected as the negative electrode is Li metal [10]" |
| Q6 압력 | **해당 없음** | 박막 · `pressure` 0 |
| Q7 Li 재고 | **해당 없음 + 공백** | Li 금속 무한 원천 · c_max · c_min · c_Lis,0 미인쇄(G1) |
| Q8 OCP · 평형 곡선 | **층 하나** | 식 (22) = Fabre [11] 의 θ 유리함수(10 차 · 측정 방법 미인쇄) · 평탄 창 SOC 0.1–0.4(\|dE/dSOC\| 0.072–0.17 V) = 관측성 창 · 분자 영점 · 분모 극 θ 1.0032 · 1.0037(물리 범위 바로 위) · 91호 EMF(율 외삽)를 바꿔 끼움 |

**누적 ≈20.0 → ≈20.0 (새 칸 0).**

---

# 재현 (`[재현]` — 인쇄 수치 · 식 · 그림 좌표로 우리가 계산 · 가정 · 외부 값 표시 · 스크립트는 `scratchpad` 에만)

| # | 무엇 | 입력 | 결과 | 대조 |
|---|---|---|---|---|
| R1 | 식 (22) 모양 | 인쇄 계수 | θ ∈ [0.5, 1] 단조 · E(0.5) 4.2908 · E(0.505) 4.2812 V · 3.4 V = θ 0.99924 · 3.0 V 는 θ 1.00137(물리 밖) · 분자 영점 θ 1.00319 · 분모 극 θ 1.00369 | 그림 2 시작 4.2728 V(η 포함) |
| R2 | 평탄 지도 | θ = 1 − SOC/2 | \|dE/dSOC\| 최소 0.072 @SOC 0.28 · 0.1–0.4 중앙 0.126 · 0.4–0.99 중앙 0.658 · 1 mV → SOC 0.0134(0.3) ↔ 0.0010(0.99) · ∂E/∂θ 0.143 ↔ 1.79 V(×12.5) | 인쇄 "0.1 < SOC < 0.4" ✅ |
| R3 | 용량 · 1C | `[재현·외부 값]` 91호 a_max 2.33×10⁴ · c_min = c_max/2 · M · A | Q 9.99 µAh · 1C 9.99 µA · 10C 99.9 µA | 그림 4 양극 초기 ≈1.177×10⁴ = c_min + 0.01Δ ✅ · 그림 4 300 s · 쿨롱 SOC 0.157 |
| R4 | η_mt(0⁺) | −I L RT/(δc₀F²A(D_Li⁺ + D_n⁻)) · T 298.15 | D_n⁻ 5.1×10⁻¹⁵ −6.15 · 2.1×10⁻¹⁵ −12.30 mV | 그림 3 −6.21 ✅(5.1) |
| R5 | 식 (14) 항별 | 그림 4 단면(벡터) · D_n⁻ 5.1 · I 99.93 µA | −∫E −6.76 · −8.56 · −11.92 · −14.45 · −19.18 / Nernst −1.01 · −3.62 · −8.37 · −11.93 · −18.44 mV(1 · 10 · 50 · 100 · 300 s) | 그림 3 η_mt −6.99 · −8.83 · −12.19 · −14.73 · −19.55 = 둘째 항만 ✅ |
| R6 | 전압 폐합 | 그림 2 10C − Eeq(θ̄ · 쿨롱) | 1 · 10 · 50 · 100 · 150 · 200 · 250 · 300 s 차 0.02 · −0.04 · −0.12 · −0.18 · −0.18 · −0.13 · −0.11 · −0.41 mV ↔ 그림 3 η_total | ✅ Nernst 항 없음 |
| R7 | 재풀이(모형 1) | 위 §(a) 3 | 1–300 s ±0.5 mV · 3.4 V 691.63 · 335.77 · 157.84 s | 그림 2 689.40 · 334.56 · 157.18 ✅ |
| R8 | α 0.6 ↔ 0.5 순간값 | SOC 0.99 · c⁺/c⁺₀ = δ · F·A·k_pos 수치 · I 100 µA | i₀ 0.277 ↔ 0.208 mA · η_ct −9.57 ↔ −12.25 mV → **2.68 mV** | 표 2 펄스 M3 0.0027 ✅ · 그림 6 첫 점 +2.68 ✅ · c⁺/c⁺₀ = 1 로 읽으면 1.88 mV ✗ |
| R9 | i₀ 자릿수 · 차원 | 식 (17) | 중간 SOC ≈0.88 mA · 단위 C m⁵ mol⁻² s⁻¹(인쇄 k_pos 단위로) | 91호 그림 8 요구 0.9–1.0 mA(91호 digest 전사) · D4 |
| R10 | 그림 5 · 6 ↔ 표 2 ↔ 재풀이 | 벡터 오차 곡선 | 그림 = 표 2 기준 행 · 재풀이 M2 ±0.02 mV · M3 전류 구간 ✅ / 휴지 −0.1 … −0.8 mV 표류 ✗ · M4 그림이 ≈1.3–2.1 mV 더 음(t = 0⁺ +0.59 ↔ 2.68) · 거친 격자(5/5 · 4/4 · 6/6) 가설 기각 | 원인 미확정(G9) |
| R11 | k_r 감도(M1 − M2) | 10C 정전류 · 펄스 | 0.9e-8 0.49/0.19 · 0.9e-7 4.19/1.62 · 8.0e-7 14.82/6.50 · 0.9e-6 15.33/6.77 mV · 펄스 0.08/0.07 → 2.89/1.89 · M1 η_mt(300 s) −19.54 → −11.29 | 표 2 M2 0.0005/0.0002 ✅(인쇄 k_r) |
| R12 | 식 (14) 그대로 | Nernst 항 포함 | M1 η_mt(300 s) −38.30 · V ≤−18.7 mV · 3.4 V 335.59 s · M1 − M4 58.26/27.61(정전류) · 18.85/7.96 mV(펄스) · M1 − M3 21.0/2.29 | 표 2 M4 43.5/14.3 · 9.9/4.9 |
| R13 | 한계 전류 · 고갈 | 인쇄 값 · r 없음 | 정상 한계 4FAD_Li⁺δc₀/L = 250.5 µA = 25.1C · D_Li⁺ ×1/100 → 0.25C · 10C 에서 ≈26 s 고갈 | 표 2 "Not converged" |
| R14 | 그림 7 C-rate 기준 | 화소 SOC · 쿨롱 | ×1.10–1.11(SOC₀ 0.99 고정 · RMS 0.0084–0.0090) · 자유 SOC₀ 0.980 · ×1.084 · 재풀이 V(×1.111) 600 s 3.908 ↔ 3.911 | D8 |
| R15 | 편향 사상 | 그림 9 Δη_total ÷ R2 기울기 | EKF4 −0.045 · −0.123 · −0.084 · −0.046(600 · 750 · 800 · 850 s) ↔ 실측 −0.048 · −0.084 · −0.087 · −0.068 · EKF3 예측 ≤0.02 ↔ −0.018 … −0.046 | 판정 1 |
| R16 | 단일 점 감도 | `[재현·가정]` σ_V 31.6 mV | σ_SOC 0.44(SOC 0.28) ↔ 0.035(SOC 0.9) | — |
| R17 | 그림 8 총량 | 벡터 여섯 마디 | 합 64,908 = 6 δc₀(t = 0 · 990 s) · EKF3 셋 11,880 = 1.098 δc₀ | D6 · D7 |
| R18 | 손잡이 편향 예시 | `[재현·가정]` A_eff ×0.5 · 10C · i₀ 0.88 mA | Δη_ct −2.92 → −5.82 mV(−2.9) → SOC −0.040(평탄) ↔ −0.0044(SOC 0.4 위) | §(d) |
| R19 | "40 %" | (9 − 5)/9 | 44.4 % | D10 |
| R20 | 일정 | 2019-04-15 → 06-04 | 50 일 | — |

---

# 참고문헌 23 번호 — 우리 축에 닿는 것 (번호는 PDF p. 672 목록에서 직접 확인 · 빠진 번호 0)

| 번호 | 서지(지면 그대로 요약) | 이 편에서 쓰인 자리 | 우리 축 |
|---|---|---|---|
| [10] | Danilov D., Niessen R.A., Notten P.H., "Modeling all-solid-state li-ion batteries" 158 (3) (2011) A215–A222 — **저널 이름이 빠진 채 인쇄**(doi 10.1149/1.3521414 = *J. Electrochem. Soc.*) | 원 모형 · "validity of the parameters" · Li 금속 옴 · 전하이동 무시 근거 | **91호 = 4차 묶음 파일 51**(흡수됨) |
| [11] | Fabre S., Guy-Bouyssou D., Bouillon P., Le Cras F., Delacourt C., *J. Electrochem. Soc.* 159 (2) (**2011** 인쇄) A104–A115 | **식 (22) 평형 곡선의 출처** · D_Li 문헌 범위 · 마이크로배터리 매개변수 · 검증 | 원장 ★★(98 \| 1 — 원장 행 표기 2012 · 같은 권 · 쪽) · **재지목** |
| [12] | Nesro M.S., Elfadel I.A.M., "A simplified computational model for solid-state lithium microbatteries", 2013 IEEE ICECS, 727–730 | 전기중성 단순화 · 1C 비교 — 단순화 계보의 앞 편 | 새 ★ |
| [7] | Di Domenico D., Stefanopoulou A., Fiengo G., *J. Dyn. Syst. Meas. Control* 132 (2010) 061302 — "… state of charge and critical surface charge estimation using an electrochemical model-based extended kalman filter" | 유한차분 · EKF 의 방법 원형("similarly to that used in Ref. [7]") | 새 ★ |
| [13] | Wang Y., Fang H., Zhou L., Wada T., *IEEE Control Syst. Mag.* 37 (4) (2017) 73–96 — EKF SOC 재검토 | SOC 추정 종설 | 새 ★ |
| [14] | Lin X., Kim Y., Mohan S., Siegel J.B., Stefanopoulou A.G., *Annu. Rev. Control, Robotics, Autonomous Syst.* 2 (2019) 393–426 — "Modeling and estimation for advanced battery management" | SOC 추정 종설(같은 저자군) | 새 ★★ |
| [15] | Tian H.-K., Qi Y., *J. Electrochem. Soc.* 164 (11) (2017) E3512–E3521 — "Simulation of the effect of contact area loss in all-solid-state li-ion batteries" | **표 1 머리의 출처**(본문은 [10] 모형) | 원장 ★★★ · **재지목** |
| [16] | Jang Y.-I., Neudecker B.J., Dudney N.J., *Electrochem. Solid State Lett.* 4 (6) (2001) A74–A77 — "Lithium diffusion in LixCoO2 (0.45 < x < 0.7) intercalation cathodes" | D_Li 의 "usual values" | 새 ★ |
| [19] | Lin X., *IEEE Trans. Ind. Electron.* 65 (9) (2018) 7138–7148 — "Theoretical analysis of battery soc estimation errors under sensor bias and variance" | "assessing parameter identifiability or estimability [19,20]" | 새 ★★(편향 ↔ 분산 — 판정 1 의 언어) |
| [20] | Mohan S., Kim Y., Stefanopoulou A.G., *IEEE Trans. Control Syst. Technol.* 24 (5) (2016) 1643–1654 — "Estimating the power capability of li-ion batteries using informationally partitioned estimators" | 같은 자리 | 새 ★★(정보 분할 추정기 — 추정 가능성) |
| [21] · [22] · [23] | Pannell 1997 *Agric. Econ.* · Saltelli · Chan · Scott 2000 *Sensitivity Analysis*(Wiley) · Kim Y., Mohan, Siegel, Stefanopoulou, Ding 2014 *IEEE TCST* 22, 2277 | 감도 분석 일반 · OAT | ☆ |
| [1]–[6] · [8] · [9] · [17] · [18] | Ozawa 1994 · Mrgudich 1960 · Owens & Skarstad 1992 · Kim J.G. 외 2015 *JPS* 282 종설 · Zheng F. 외 2018 *JPS* 389 종설 · Smith & Wang 2006 *JPS* 160, 662 · Li J. 외 2017 *JES* 164 A874 · Perez 외 2017 *JES* 164 A1 · Huggins 2010 · Julien & Nazri 2013 | 서론 · 배경 · 액체 모형 예 | ☆ |

---

# 인용 대조

## 1. 이 편을 지목 · 인용한 우리 digest — 그 쓰임 ↔ 이 편이 실제로 주는 것

| digest | 쓰임(digest 전사) | 이 편 | 판정 |
|---|---|---|---|
| **12호** Kouhestani 2022 [62] | "★ Kim [62] … 그 모델 위에 상태추정 BMS 알고리즘 제안 — `[인쇄]` 'However, the equation order of this method is higher, and the efficiency of the algorithm has not been determined.'" · 표 1 "[62]만 상태추정(SOC), 열화 데이터 ✗" · 후속 ★★ 3 "관측 가능성/식별성이 다뤄졌는지 확인 (Q4)" | Danilov(91호) 모형 위 ✅(단 표 1 출처는 [15] · 평형 곡선은 [11]) · 상태 4 / 7 · 계산 비용 보고 0 ✅ · 열화 0 ✅ · 관측성 = 논증 + 합성 실행 · 식별성 계산 0 | 12호 서술 대체로 ✅ · Q4 물음의 답은 **'다뤘으나 재지 않았다'** |
| **37호** Li 2024 [21] | 후속 표(§14 · 등급 칸 없음): "ASSB 상태 추정(EKF) — 추정기에서 접촉/용량 손잡이 처리" | 손잡이 둘 다 없음 · 모형 불일치 → SOC 편향 통로 하나(§(d)) | 답: **없다 — 편향으로만** |
| **26호** Iwakiri 2024 | "Kim … 2019 … 는 이 편이 인용하지 않는다 — 같은 모델 계보인데" | 26호와 같은 Danilov 계보 · 26호보다 앞 | 인용 0 확인(26호 쪽 사실 — 원장 "구조적 공백 1번 후보") |
| 91호 Danilov 2011 | 교차 참조(지목 아님) — "같은 계보 모형 위의 상태추정" | [10] 모형 · 값 상속(D_n⁻ · k_pos 제외) · 인쇄 k_r ×100 문제 그대로 · 평형 곡선은 교체 | 91호 표 II 의 하류 첫 사용처 — 91호가 찾은 k_r 문제를 이 편 표 2 가 '단순화 (1) 무시 가능' 의 근거로 쓴다(R11) |

## 2. 이 편이 인용한 우리 digest

- **[10] = 91호**(흡수됨) — 이 편의 쓰임: 원 모형 · 매개변수 검증 · 음극 무시 근거 · 서론 소개("10 mAh" — 91호 공칭 10 µAh 의 ×1000 · D9).
- 4차 묶음 13 편 중 인용: **[10](파일 51 · 91호) 하나** — 나머지(Firouz 2020 · Bielefeld 2023 · Schmidt 2024 · Khalik 2021 · Lu 2022 · Koerver 2018 · Raijmakers 2020 · Deng 2021 · Danilov & Notten 2008 · Xie 2008 · Shao 2022 · Ansah 2021) 인용 0(23 번호 전수 대조 — 대부분 이 편보다 뒤 · Koerver 2018 · Danilov & Notten 2008 · Xie 2008 은 앞이나 인용 0). Deng 2021(파일 60 · 100호 예정 — 원장 행 저자 "Deng·Hu·**Lin**·Xu·Li·Guo")은 이 편 공저자 X. Lin 의 후행 편으로 읽힌다(서지 표기 일치만 · 미확인).

---

# 곱 축퇴 처방 — 여든두 번째 적용 ([[assb-lampe-contact-product-degeneracy]])

⚠ 이 편은 접촉 · 노화 0 인 신품 모형 + 합성 추정 편이다 — 처방의 입력 점검은 대부분 ❌ 이고, 남는 것은 **곱의 자리가 추정기 안에서 어떻게 되는가** 다.

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| **1단계**(16호) | `R` 과 `C` 를 같이 | 축전기 0 · 이중층 0 | ❌ |
| **2단계**(18 · 25호) | + 면적을 아는 대조군 | 평판 박막 기하 면적 A = 1 cm²(설계) 하나 | ❌ |
| **3단계-a**(19호) | `Ea` | T 미인쇄 · 등온 | ❌ |
| **3단계-b**(19호) | `C` 물리 상한 | — | ❌ |
| **4단계**(20 · 24호) | 시간 영역 | 펄스 이완(모의 · 10C 1 분 + 4 분) · EKF 펄스 열 | ⚠ 모의만 — 이완이 A·k_pos 와 전해질을 가르는지 시험 0 |
| 처방 표 "율 스윕" | 여러 율 | 5 · 10 · 20C(그림 2) | ⚠ 모의 |
| 처방 표 "`J^T J` 최소 고유벡터" | 적합점 야코비안 | EKF 의 C_k 는 상태 야코비안 · 값 미인쇄 | ❌ |

## ★ 곱 문장 — 셋 (`[인쇄]` → `[해석]`)

- ① `[인쇄]` 식 (17) "i₀,pos = FAk_pos(…)" — 면적 A 와 속도 상수 k_pos 가 **한 곱**으로만 들어가고 A 는 같은 값이 플럭스 경계(식 3 · 4 · 11)에도 들어간다 ⇒ `[해석]` 접촉 면적 손실은 이 모형에서 k_pos(또는 A 전체)의 이름으로만 표현된다(91호 식 8 · 98호 식 9 와 같은 자리).
- ② `[인쇄]` 표 2 k_pos ×1/100 → 모형 3 오차 0.0869 V · "these extreme parameters are typically not physically realistic" ⇒ `[해석]` A·k_pos 가 열화로 줄어드는 방향은 이 추정기 설계(α 0.5 해석 야코비안)의 근거가 무너지는 방향이다 — 신품 박막에서 '비현실' 인 값이 열화 셀에서는 시험 대상이 된다.
- ③ `[재현·가정]` 손잡이가 없는 추정기에서 곱의 변화(A_eff ×0.5 → Δη_ct ≈−2.9 mV @10C)는 SOC 편향(평탄 −0.040)으로 나온다 — **곱의 어느 인자인지(면적 ↔ k)도, 그것이 용량(LAM)인지도 추정기 출력에서는 갈리지 않는다**.
- ⇒ 처방 표에 **새 줄은 없다**. 후보 메모 하나: "상태 추정기의 SOC 오차를 접촉 · LAM 진단 신호로 쓰기 전에, 그 추정기가 접촉 · 용량을 상태 · 매개변수로 두는지와 평탄 창에서의 편향 증폭(1 / \|dE/dSOC\|)을 적는다" — 새 판단 거리 첫째와 묶는다.

## ⚠ 이것이 곱을 푼 것은 아니다

- 열화 · 접촉 · 온도 · 면적 대조가 모두 0 이다 — 위 자리는 **모형 구조**이고 측정이 아니다. A_eff ×0.5 예시는 i₀ 0.88 mA(중간 SOC · 10C) 한 점 위의 `[재현·가정]` 이다.

---

# 보류 결정 (가)–(히) · (개)–(해) · (게)–(헤) · (갸)–(햐) · (겨)–(며) — 이 편이 주는 근거 (결정 안 함)

| # | 결정 (요약) | 99호 근거 | 세기 |
|---|---|---|---|
| **(세)** | 인쇄 매개변수 표의 재풀이 폐합 검사 | 재풀이가 그림 2 · 3 을 ±0.5 mV 로 닫는다 — **단 표 1 D_n⁻ 을 5.1 로 고치고 빠진 c_max · c_min · T 를 91호에서 가져오고 식 (14) 의 Nernst 항을 빼야** 닫힌다(R4–R7) · 표 2 펄스 M3 0.0027 = t = 0⁺ 한 점(R8) · 인쇄 k_r 이 '단순화 (1) 무시 가능' 을 만든다(×100 이면 M2 15.3 / 6.8 mV — R11) | **강** |
| **(치)** | 모형 결론 옆 '배제 가정' 표기 | "simplifications … acceptable for most of actual performance calculation" — 배제: k_r · δ 미시험 · k_pos ×1/100 '비현실' · 플랜트 Nernst 항 없음(모형 4 오차 RMS 우리 재풀이 13.0 → 27.6 mV · 표 2 인쇄 14.3) | **강** |
| **(쟈)** | '식별 가능' 주장의 층 표기 | "weakly observable" — 구조 논증(야코비안 ≈0 · 값 0) + 실제적 합성 실행 하나 · 대상 상태 · 관측성 행렬 · Gramian · CRB 0 · `[재현]` 기울기 ×1/12.5 · 편향 사상 | **강** |
| **(대)** | C-rate 의 기준 용량 표기 | 용량 · 1C 전류 미인쇄(c_max · c_min 없음) · 서론 [10] "10 mAh"(91호 10 µAh · ×1000) · 그림 7 C-rate 기준 = 그림 2–6 의 ×0.9(전류 ×1.10–1.11 — R14) | **강** |
| **(체)** | 평형(OCV) 곡선의 출처 층위 표기 | 식 (22) = [11] Fabre 의 '실험 평형 전위' 유리함수(측정 방법 · 범위 미인쇄) · 91호 EMF(같은 셀 율 외삽)와 다른 곡선을 91호 적합값과 짝지음 · 극 θ 1.0037 · 평탄 창 = 관측성 창 | **강** |
| **(며)** | 'validated' 의 자료 층위 표기 | "the validity of the parameters was experimentally demonstrated in Ref. [10]" — 91호 자료 · 91호 평형 곡선 위의 검증(이 편 조합 아님) · "validate these four models" = 모형 1 대비(계산 ↔ 계산) · 실험 0 | **강** |
| (뎌) | '문헌값 일치' 의 자료 독립성 표기 | 표 1 '문헌값' = 91호 적합값(설계 3 · NDP 1 · 적합 6) 을 [15] 경유로 표기 · 같은 셀 · 같은 곡선의 적합값을 다른 평형 곡선과 다른 시험에 씀 | 중 |
| (이) | 모형 값 인용 규칙 | 표 1 값 ↔ 그림이 쓴 값(D_n⁻) · k_pos 관례 변경 · 출처 번호 [15] ↔ [10] | 중 |
| (탸) | 요약 수치 ↔ 같은 편 표 · 그림 축 | "40%" ↔ 44 % · "six critical parameters" ↔ 표 다섯 · 표 1 ↔ 표 2 D_n⁻ | 중 |
| (챠) | 최종 매개변수 표 ↔ 물리 범위 폐합 | D_n⁻ 표 간 불일치 · D_Li⁺ ×1/100 = 물리 고갈(한계 전류 0.25C — R13) · L 범위만 ±27 % | 중 |
| (먀) | '모형 원전' 지목 때 기구 층위 확인 | 12호 "그 모델 위에" ✅(단 표 1 출처 [15] · 평형 곡선 [11]) · 37호 "접촉/용량 손잡이 처리" → 손잡이 0 | 중 |
| (냐) | 모형 결론 회고 인용 — 조건 복원 | 초록 · 결론 "40% reduction" — 조건(합성 한 번 · 같은 계열 플랜트 · Nernst 항 없는 플랜트 · 잡음 미인쇄)이 초록에 없음 | 중 |
| (햐) | '계산 ↔ 실험 일치' 의 측정 몫 · 비교 축 | "This is in compliance with experimental discharge profiles of solid-state batteries"(그림 2) — 비교 대상 · 인용 0 · 측정 몫 0 | 중 |
| (샤) | 다중 시작 · 합성 참값 시험의 일관성 ↔ 정확성 | EKF 시험 = 합성 참값 하나 · 잡음 실현 하나(값 미인쇄) · 초기 오차 하나 · 실행 하나 — '9 % → 5 %' 의 산포 0 | 중 |
| (무) | j₀(x) 모양 선택지 | 식 (17) α 0.6 ↔ 0.5 차 = SOC 0.99 순간 2.68 mV · 방전 끝 23 mV · k_pos ×1/100 87 mV — 같은 √ 꼴 계열 안 선택의 크기 | 중 |
| (에) | 속도 상수의 i₀ 환산 표기 | k_pos 5.1×10⁻⁴ m³ mol⁻¹ s⁻¹ — 식 (17) 차원 불일치 · 수치(A m²) i₀ 0.28 · 0.88 mA · 91호 k₁ˢ 5.1×10⁻⁶ m^2.8 mol^−0.6 s⁻¹ 의 ×100 | 중 |
| (겨) | 처방 효과의 측정 여부 | "This inclusion leads in a 40% reduction in state-of-charge estimation error" — 모의 한 번 | 중 |
| (다) | 28호 액체셀 도구를 ASSB Q4 분모에 | ASSB 상태 추정 편도 관측성 계산 0 — 분모에 ASSB 한 점 더(이 편은 ASSB) | 약 |
| (차) | PyBaMM 면적 노브 / j₀ 노브 분리 forward | 식 (17) F·A·k_pos 한 곱 · A 가 플럭스 경계에도 — 추정기에서 둘 다 편향 통로 하나 | 약 |
| (페) | '입력 설계' 의 목적 표기 | EKF 시험 전류(5C / 2.5C 펄스 열)는 설계 목적 미인쇄 · 미래 과제는 입력 설계가 아니라 측정 창 | 약 |
| (루) | SOC 축 신품 j₀(x) 기준선 | i₀ 0.277 mA(SOC 0.99) → ≈0.88(중간) → 0(끝) — 신품 박막의 i₀(SOC) 모형 표본 | 약 |
| (뱌) | 재매개화 · 묶음의 최소성 | 모형 4 식 (28) — L · δc₀ · (D_Li⁺ + D_n⁻) 가 옴 상수 하나로 · 전해질 확산 둘의 개별 정보 0(EKF4) | 약 |
| (녀) | 계면 반응 방향의 재풀이 폐합 | 방향 문제 아님 — 같은 '인쇄 식 ↔ 그림' 대조에서 **항 누락**(식 14)이 잡혔다(새 판단 거리 둘째) | 약 |
| (헤) | 측정 입력의 역모형 층위 | L · M · A = 91호 설계값 · c₀ = NDP — 측정 입력은 남의 셀 것 | 약 |
| (갸) | '단순성' 근거 명제의 척도 | 모형 4 "much simpler … good candidate" — 척도 = 상태 수(4 ↔ 7) · 대가(평탄 편향)는 같은 지면 그림 7 에 | 약 |
| (가) | 29호 Q4 +0.5(정적 ↔ 동적) | 정적(평탄 OCV) ↔ 동적(전해질 분극)의 혼동이 편향으로 나타나는 상태 추정 표본 — 결정 재료 아님 | 약 |
| (리) | 요구치 계보의 남은 다리 요청 묶음 | Tian & Qi 2017 재지목 → 6 · 이유 추가(표 1 머리 출처) | 약 |
| (마) | 37호 "ASSB truth 5조건" — **결정 · 반영(2026-09-23)** | 근거 0(이 편은 truth 조건 R1–R8 어느 것도 다루지 않는다) | — |

나머지 — (라)(바)(사) 결정 · 반영됨(이 편 근거 0), 그 밖의 글자는 **근거 0**(압력 · 기준극 · 3전극 · 노화 사이클 · LLI 실측 · θ 판정 · 상 분율 · 입도 · 피복률 · 프로토콜 비교 · 원자료 예치 · DRT · 축전기가 이 편에 없다). **결정 안 함.**

## 새 판단 거리 (넷 — 글자는 호출자가 붙인다)

1. **'관측성 · 관측 불가' 주장의 산출물 표기 (상태 추정판)** ((쟈) 의 상태판으로 묶어도 됨) — 편이 '약한 관측성 · 관측 불가' 를 쓸 때 카드 Q4 · 개념 · 합성 truth 로 옮기기 전에 ① 대상(상태 ↔ 매개변수) ② 근거 층(구조 논증 · 관측성 행렬 / Gramian / CRB 계산 · 합성 추정기 실행) ③ 오차의 성격(분산 = 잡음 ÷ 기울기 ↔ 편향 = 모형 불일치 ÷ 기울기) ④ 합성 시험 설계(플랜트가 추정 모형과 같은 계열인지 · 잡음 값 · Δt · 실현 수)를 적게 할지 — 99호: 대상 SOC · 근거 = 평탄 논증 + EKF 실행 하나 · `[재현]` EKF4 '9 %' ≈ Δη(−7 … −11 mV) ÷ \|dE/dSOC\|(0.07–0.09 V/SOC) 편향 · 잡음 · Δt 미인쇄.
2. **인쇄 식 ↔ 그림의 항 폐합 (식에 있는 항이 계산에 들어갔는가)** ((세) 의 항판 · (녀) 와 같은 가족으로 묶어도 됨) — 모형 편의 '전체 모형' 을 truth · 비교 기준 · 하네스로 옮기기 전에, 그림 값(농도 단면 · 성분 곡선)으로 인쇄 식의 각 항을 다시 풀어 모든 항이 계산에 들어갔는지 확인하고 결과(항별 mV)를 적게 할지 — 99호: 식 (14) 의 Nernst 항이 그림 3 · 2 에 없다(그림 4 단면으로 −1.0 … −18.4 mV · 전압 폐합 ±0.4 mV) → 모형 4 오차가 ≈절반으로 보인다(우리 재풀이 RMS 27.6 ↔ 13.0 mV · 표 2 인쇄 14.3).
3. **표에 적힌 값 ↔ 계산에 쓰인 값 대조 + 매개변수 표의 출처 번호 거슬러 확인** ((챠) · (뎌) · (이) 의 하위로 묶어도 됨) — 매개변수 표를 옮길 때 그 값이 같은 지면 그림을 다시 내는지(값 하나씩 진단 가능한 그림 특징 — 균일 옴 강하 · 첫 순간 값 등) 확인하고, 표 머리 출처가 원 편이 아니면(재인용 · 변환) 원 편까지 거슬러 값 · 단위 · 층위를 대조해 적게 할지 — 99호: D_n⁻ 표 1 2.1 ↔ 그림 · 표 2 5.1 · 머리 "[15]"(Tian & Qi) ↔ 본문 "[10]"(91호) · k_pos 91호 ×100 · 다른 단위.
4. (선택) **축약 모형 검증 표의 견고성 범위 — 흔들지 않은 매개변수 · '비현실' 배제 영역의 열화 도달성 표기** ((치) 의 축약판으로 묶어도 됨) — 단순화 오차 표(OAT)를 합성 truth · 추정기 설계 근거로 옮길 때 단순화가 기대는 매개변수(단순화 (1) 이면 k_r · δ)를 흔들었는지, '비현실' 로 배제한 영역(k_pos ×1/100)이 열화 · 접촉 손실로 도달 가능한지 적게 할지 — 99호: 표 2 에 k_r · δ 행 0 · `[재현]` k_r ×100(91호 그림 일치 값)이면 모형 2 오차 15.3 / 6.8 mV · k_pos ×1/100 모형 3 86.9 mV 를 "not physically realistic" 로 배제.

---

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것

| # | 어긋남 | 근거 |
|---|---|---|
| **D1** ★★★★ | 식 (14) η_mt = (RT/F) ln[c(L)/c(0)] − ∫E dy ↔ 그림 3 η_mt = −∫E 만(그림 4 단면으로 ±0.3 mV · Nernst 항 −1.0 … −18.4 mV 없음) · 그림 2 전압도 같다(±0.4 mV) · 재풀이 ±0.5 mV 도 둘째 항만으로 | R4–R7 · 코드 미공개 |
| **D2** ★★★ | 표 1 D_n⁻ 2.1×10⁻¹⁵ ↔ 표 2 기준 5.1E-15 ↔ 그림 η_mt(0⁺) = 5.1 의 값(−6.15 ↔ −6.21 mV · 2.1 이면 −12.3) ↔ 91호 5.10×10⁻¹⁵ | R4 · 표 렌더 |
| **D3** ★★★ | 표 1 머리 "[15]"(Tian & Qi 2017 — 접촉 면적 손실 모의) ↔ 본문 "the model presented in Ref. [10] … the validity of the parameters was experimentally demonstrated in Ref. [10]" · k_pos 5.1×10⁻⁴ m³ mol⁻¹ s⁻¹ ↔ 91호 k₁ˢ 5.1×10⁻⁶ m^2.8 mol^−0.6 s⁻¹ | 표 1 · 91호 digest 전사 |
| **D4** ★★ | 식 (17) i₀ = F·A·k_pos × 무차원 비 — 인쇄 k_pos 단위로 C m⁵ mol⁻² s⁻¹(전류 아님) · 수치로는 A m² 일 때 0.28–0.88 mA | `[재현·대수]` · R8 · R9 |
| **D5** ★★ | 식 (8) γ = k_r c_Li⁺,0 δ²/(1 − δ) — r(δc₀) = 0 이려면 c_Li⁺,0² · 인쇄는 차원 s⁻¹ ↔ r 은 mol m⁻³ s⁻¹ | `[재현·대수]` · 식 렌더 |
| **D6** ★★ | 초기값 목록 "EKF4 SOĈ₀ = 0.8, ĉ_Li⁺(0) = 1.1c_Li⁺(0)" ↔ 다음 문장 "initial conditions of the electrolyte are not required for the EKF4" ↔ 그림 8 EKF3 셋 11,880 출발 | R17 · 쪽 렌더 |
| **D7** ★★ | x^e(Me − 1) + x^s(Mp − 1) · Me = Mp = 5 → 8 ↔ EKF3 P0 I₇ₓ₇ · Q_w 3 + 1 + 3 · 인덱스 이름 N_e · N_s ↔ M_e · M_p | 쪽 렌더 · R17 |
| **D8** ★★ | 그림 7 전류 5C · 2.5C ↔ Actual SOC 가 그림 2–6 기준보다 ×1.10–1.11 빨리 떨어짐(1C 정의 하나뿐 — 각주 1) | R14 |
| **D9** ★★ | 서론 [10] "a micro-battery with a capacity of 10 mAh" ↔ 91호 공칭 10 µAh(×1000) | 91호 digest 전사 |
| **D10** ★★ | 초록 · 결론 "40% reduction … from 9% to 5%" ↔ (9 − 5)/9 = 44 % · '%' = SOC 절대 %p(그림 7 삽도) · 정의 미인쇄 | R19 · G7 |
| **D11** ★ | "six critical parameters"(p. 668) ↔ 표 2 다섯 · 바로 앞 문장 "kpos, DLi+, Dn, DLi and L are critical parameters"(다섯) | 표 2 |
| **D12** ★ | 서론 안내 "In Section 3 … model simplification · Section 4 … EKF · section 5 … conclusions" ↔ 실제 2.5 · 3 · 4 | 절 머리 |
| **D13** ★ | "Table II"(본문 두 번) ↔ "Table 2" · "as shown in Figs. 4–7, Model 3 is more accurate than Model 4" ↔ 그림 4 = 농도 단면 · 그림 7 = EKF | 본문 |
| **D14** ★ | SOC 정의 c̄ = (1/M)∫_L^{L+M} c dt — dy 의 오기 | 쪽 렌더 |
| **D15** ★ | "lithium diffusion coefficient in Li2CoO2"(p. 667) — LiCoO₂ · LixCoO₂ 의 오기로 읽힘 · 초록 · 결론 "charge transfer number of 0.5" = 전하 이동 계수 α_pos(이원 전해질 편에서 '수송수' 와 헷갈리는 낱말) | 본문 |
| **D16** ★ | 그림 5 · 6 x 축 'Time (t)' · 오차 부호(V₁ − V_k) 본문 정의 0 | 그림 |
| **D17** ★ | 식 (5)–(6) 계수 α(= −k_r) ↔ BV 전하 이동 계수 α_pos — 같은 글자 | 식 렌더 |
| **D18** ★★ | 그림 6 M3 휴지 구간 −0.1 … −0.8 mV 표류 · M4 t = 0⁺ +0.59 mV(M3 2.68 과 달라야 할 이유 없음) — 인쇄 식 · 표 1 재풀이에 없음 | R10 · G9 |
| **D19** ★ | 참고문헌 [10] 저널 이름 누락("Modeling all-solid-state li-ion batteries 158 (3) (2011) A215–A222") · [11] 연도 2011 인쇄(원장 행 2012 — 같은 권 · 쪽) | p. 672 |
| **D20** ★ | 2.4 "relative absence of a plateau at nominal voltage" ↔ 그림 2 ≈3.88 V 평탄 · 같은 문단 "a small plateau" · 3.3 의 평탄 논증 | 그림 2 · R2 |
| **D21** ★ | 표 2 각주 b "unrealistic values … convergence issue" ↔ `[재현]` D_Li⁺ ×1/100 은 10C 에서 ≈26 s 고갈(한계 전류 0.25C) — 물리 고갈 구간 | R13 |

---

# 이 편이 우리 프로젝트에 주는 것 (정리)

- **'약한 관측성' 은 증폭기다 — 편향과 분산을 가른다.** 우리 `degradation-degeneracy/` 의 물음("곡선이 맞는다 ≠ 매개변수가 맞다")에는 축퇴(분산 · 근최적 폭)와 모형 불일치(편향)가 같이 있다. 이 편의 9 % 는 평탄 기울기로 증폭된 편향이었고(R15), 창(데이터 궤적)은 분산은 줄여도 그 편향은 줄이지 못한다. 근최적 폭 측정([[near-optimal-set-width-measurement]])이 재는 것은 분산 쪽이라는 구분을 상태 추정 표본으로 받친다(우리 수치는 `degradation-degeneracy/docs/RESULTS*.md` 정본 — 옮기지 않음).
- **합성 truth 구현 경고 둘** — ① 계보 모형을 truth 로 이식할 때 인쇄 식 (14) 와 저자 그림이 다르다(Nernst 항 — D1) — 어느 쪽을 truth 로 삼았는지 적어야 한다 ② 표 1 의 D_n⁻ 은 그림이 쓴 값이 아니다(D2) — 98호 D1(음극 방향)과 같은 '인쇄 식 묶음 ↔ 그림' 대조의 둘째 표본.
- **37호 물음의 답(상태 추정판)** — 접촉 · 용량 손잡이 없는 추정기에서 둘은 같은 편향 통로를 쓴다. 우리 쪽 '관측을 더해 가른다' 물음에 대해: 이 편은 관측을 더하지 않고 모형을 키웠다(EKF4 → EKF3) — 편향의 한 성분(전해질 분극)만 줄었다.
- **평탄 창 = 관측성 창** — LCO 평형 곡선의 0.1–0.4 SOC 평탄이 상태 추정에서 SOC 오차를 ×10 키운다. 반쪽전지 OCV 창 맞춤 계보([[data-window-identifiability]])의 '창 위치' 축과 같은 현상의 상태 추정 쪽 표본이다.
- **이 편이 주지 않는 것**: 실험 · 열화 · 접촉 · 압력 · LLI · LAM · 매개변수 식별 · 관측성 계산 · 잡음 모형 · 원자료 · 코드 — 그리고 99 편 누적 `θ(N)` 0.

---

# 후속 후보 (원전 우선 — 지목 수는 위키 digest 의 후속 절 grep 으로 센 값)

| 등급 | 서지 (PDF 목록 번호) | 지목 (후속 절) | 왜 | 축 |
|---|---|---|---|---|
| ★★★ | Tian H.-K., Qi Y. 2017 — "Simulation of the effect of contact area loss in all-solid-state li-ion batteries", *J. Electrochem. Soc.* **164**, E3512–E3521([15]) | 12 · 81 · 94 · 97 · 98 · **99** = **6**(재지목) | **표 1 머리의 출처** — 표 1 의 D_n⁻ 2.1×10⁻¹⁵ · k_pos 5.1×10⁻⁴ m³ mol⁻¹ s⁻¹(91호와 다른 값 · 단위)가 그 편에서 왔는지 · 그 편이 접촉 면적 손실을 식 (17) 의 A 로 넣는지(A_eff 곱 자리의 원전) | Q1 · Q6 · 곱 · (a) |
| ★★ | Fabre S., Guy-Bouyssou D., Bouillon P., Le Cras F., Delacourt C. — "Charge/discharge simulation of an all-solid-state thin-film battery using a one-dimensional model", *J. Electrochem. Soc.* **159**(2), A104–A115(인쇄 2011 · 원장 2012)([11]) | 98 · **99** = **2**(재지목) | **식 (22) 평형 곡선의 원전** — 측정 방법(GITT · 저율) · 맞춤 범위 · θ 정규화 · 평탄(SOC 0.1–0.4 = 관측성 창)의 측정 근거 · θ → 1 근처(극 1.0037) | Q8 · (체) · (b) |
| ★★ | Lin X. 2018 — "Theoretical analysis of battery SOC estimation errors under sensor bias and variance", *IEEE Trans. Ind. Electron.* **65**(9), 7138–7148([19]) | 99 = **1**(새) | 이 편이 식별성 · 추정 가능성 근거로 든 편 — **편향 ↔ 분산을 SOC 추정 오차에서 가르는 이론**(판정 1 의 언어) · OCV 기울기 · 센서 편향의 사상 | Q4 · 방법 |
| ★★ | Mohan S., Kim Y., Stefanopoulou A.G. 2016 — "Estimating the power capability of li-ion batteries using informationally partitioned estimators", *IEEE Trans. Control Syst. Technol.* **24**(5), 1643–1654([20]) | 99 = **1**(새) | 같은 자리 — 정보 분할 추정기(어느 상태 · 매개변수를 어느 자료가 정하는가)의 액체 판 | Q4 · 방법 |
| ★★ | Lin X., Kim Y., Mohan S., Siegel J.B., Stefanopoulou A.G. 2019 — "Modeling and estimation for advanced battery management", *Annu. Rev. Control, Robotics, Autonomous Syst.* **2**, 393–426([14]) | 99 = **1**(새) | 같은 저자군 종설 — 관측성 · 식별성 · 추정기 설계의 표준 서술(이 편이 생략한 계산의 출처 후보) | Q4 · 방법 |
| ★ | Di Domenico D., Stefanopoulou A., Fiengo G. 2010 — *J. Dyn. Syst. Meas. Control* **132**, 061302([7]) | 99 = 1(새) | 전기화학 모형 EKF SOC 의 방법 원형(유한차분 "similarly to that used in Ref. [7]") — 액체셀 | 방법 |
| ★ | Wang Y., Fang H., Zhou L., Wada T. 2017 — *IEEE Control Syst. Mag.* **37**(4), 73–96([13]) | 99 = 1(새) | EKF SOC 재검토 — 관측성 · 조율의 액체 기준선 | 방법 |
| ★ | Nesro M.S., Elfadel I.A.M. 2013 — IEEE ICECS, 727–730([12]) | 99 = 1(새) | 전기중성 단순화 계보의 앞 편 — 단순화 오차를 1C 에서만 봤다는 이 편의 비판 대상 | (a) |
| ★ | Jang Y.-I., Neudecker B.J., Dudney N.J. 2001 — *Electrochem. Solid-State Lett.* **4**, A74–A77([16]) | 99 = 1(새) | LixCoO₂(0.45 < x < 0.7) D_Li 측정 — 표 2 D_Li 범위(×10^±2)의 근거 | Q3 |
| 도착 | **Danilov D., Niessen R.A.H., Notten P.H.L. 2011** — *J. Electrochem. Soc.* **158**, A215([10]) | — | **91호로 흡수됨**(4차 묶음 파일 51) — 교차 | 모형 |
| 도착 | **Deng · Hu · Lin · Xu · Li · Guo 2021** — *IEEE Trans. Transp. Electrif.* **7**, 464 | (이 편 이후 편 · 인용 0) | **4차 묶음 파일 60 · 100호 예정** — 이 편 공저자 X. Lin 의 후행 축약 모형(서지 표기 일치만 · 미확인) · 교차 참조(지목 아님) | Q4 |
| ☆ | Ozawa 1994([1]) · Mrgudich 1960([2]) · Owens & Skarstad 1992([3]) · Kim J.G. 외 2015 종설([4]) · Zheng F. 외 2018 종설([5]) · Smith & Wang 2006 *JPS* 160, 662([6]) · Li J. 외 2017([8]) · Perez 외 2017([9]) · Huggins 2010([17]) · Julien & Nazri 2013([18]) · Pannell 1997([21]) · Saltelli 2000([22]) · Kim Y. 외 2014([23]) | 행 없음 | 서론 · 배경 · 액체 모형 예 · 감도 분석 일반 | — |

**지목 누락 0** — 이 편 참고문헌 중 앞 호 후속 절에 ★ 이상으로 있던 편은 Tian & Qi 2017(원장 행 있음) · Fabre(98호 ★★ · 원장 행 있음)뿐이다. 등급 칸 없는 옛 후속 표에만 있던 편 0. **흡수된 편(교차)**: [10] = 91호. **4차 묶음 도착 편**: [10] 하나(인용) · 파일 60 Deng 2021(교차 · 인용 0).

---

# 이 digest 가 주장하지 않는 것

- **이 편의 EKF 결론(전해질 동역학을 넣으면 평탄 구간 오차가 준다)이 틀렸다고 하지 않는다** — 우리 편향 사상(R15)은 같은 방향을 지지한다; 걸린 것은 '관측성' 의 근거 층(계산 0) · 플랜트의 Nernst 항 부재 · 표 1 ↔ 그림 값 · 실행 하나다.
- **Nernst 항 부재(D1)를 구현의 사실로 확정하지 않는다** — 코드 미공개다. 확정인 것은 그림 3 · 4 · 2 가 인쇄 식 (14) 의 둘째 항만으로 서로 ±0.3–0.4 mV 에서 닫히고, 같은 가정(c_max 2.33×10⁴ · c_min = c_max/2 · SOC₀ 0.99 · T 298.15 K — 91호 값과 우리 가정)의 재풀이가 둘째 항만으로 ±0.5 mV 에서 닫힌다는 것까지다(그림 3 · 4 의 비교는 이 가정과 무관하게 선다).
- **D_n⁻ 의 참값을 주장하지 않는다** — 그림이 5.1×10⁻¹⁵ 로 계산됐다는 것(R4 — 균일 농도 순간값이라 다른 매개변수에 거의 무관)까지이고, 표 1 의 2.1 이 오기인지 [15] 의 값인지는 [15] 미열람이라 모른다.
- **9 % 전부가 편향이라고 단정하지 않는다** — 준정적 사상(Δη ÷ 기울기)이 화소 판독 위에서 ×0.7–1.5 안에 맞는 것까지다(EKF 동역학 · 잡음 · 내부 단면 미재현). EKF3 의 남은 오차가 출력 오차로 설명되지 않는다는 것도 같은 판독 위다.
- **모형 4 오차의 그림 ↔ 재풀이 차(≈1.3–2.1 mV)와 모형 3 휴지 표류의 원인을 주장하지 않는다** — 모형 2–4 의 구현이 미인쇄다(G9).
- **그림 7 의 C-rate 기준 ×1.10–1.11 을 저자 설정으로 확정하지 않는다** — 화소 SOC · 전압이 그 배수에서 함께 맞는다는 것까지다(SOC₀ 를 풀면 ×1.084).
- **이 편을 Q4 · Q1 칸 이동 근거로 쓰지 않는다** — 관측성 · 식별성 계산 0 · 열화 0. 평탄 지도 · 편향 사상 · 손잡이 편향 예시는 우리 `[재현]` · `[재현·가정]` 이다.
- **원 참고문헌(12 · 26 · 37 · 91 · 98호 인용분)을 다시 열지 않았다** — 대조는 각 digest 전사로 했다.

---
title: "Barai P., Rojas T., Narayanan B., Ngo A.T., Curtiss L.A., Srinivasan V. 2021 — Investigation of Delamination-Induced Performance Decay at the Cathode/LLZO Interface (Chem. Mater. 33, 5527–5541) + SI"
source_url: local-upload/100._Investigation_of_delamination-induced_performance_decay_at_the_cathodeLLZO_interface.pdf + 100._Sup_Investigation_of_delamination-induced_performance_decay_at_the_cathodeLLZO_interface.pdf
source_url_note: "본문 PDF 15 쪽(Chem. Mater. Article · 인쇄 5527–5541 · 그림 11 + 초록 그래픽 — 전부 Flate 래스터 · 표 0 · 식 (1) · 참고문헌 1–74) 4,587,614 B · 업로드 접두사 ed45bcee + SI PDF 25 쪽(Word → macOS Quartz · 식 (S1)–(S8) · 표 S-I · S-II · 그림 S1–S6 JPEG · SI 참고문헌 1–51) 2,068,023 B · 업로드 접두사 7afb4d94 · 5차 묶음 #1 · 사용자 파일 100 · 원장 §1 L17 ★★★★ · 지목 53 · 75 · 83 · 94 · 모형 편(DFT 계면 파괴 에너지 하나 + 2D 격자 스프링 메조 모형) · 자기 측정 0 · 실험 대조 = Wang 2019 R_ct 디지타이즈 하나 · 자동 크롭 11(본문 그림 1–11) + 수동 9(초록 그래픽 · 표 S-I · S-II · 그림 S1–S6 — SI 캡션 콜론 형식 미인식) = 20 전부 봤다 · 본문 그림은 원본 래스터 화소 판독 · 예치 원자료 · 코드 0"
source_doi: 10.1021/acs.chemmater.0c04656
source_license: "© 2021 UChicago Argonne, LLC, Operator of Argonne National Laboratory. Published by American Chemical Society(p. 5527 · XMP dc:rights) · CC · 오픈 액세스 표기 0 — 구독본으로 다룬다 — 이 digest 는 인용 · 요약 · 재현 계산만 담는다(그림 크롭은 위키 관례대로 raw/figures 에 — 변형 없는 잘라내기)"
pdf_sha256: 75f07352cb0706a42065d9162141a6a3652d3251549f604c7b1923812110cae7
si_sha256: 698bde5ed05db070f69bcd0364b9f9ef92338e49843770977de6de3032ea3a63
ingested: 2026-11-17
sha256: 590f15ca0aa136171ff20b9d5c98edc0719afe0a34acc6312eb8f298ff6ff94a
---
# 수집 목적

`assb` 섹션 **105호** — **5차 묶음 #1**(원장 `bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1 L17 · ★★★★ · 지목 53 · 75 · 83 · 94 = 4 · 2026-11-17 사용자 공급 **파일 100** — ⚠ 사용자 파일 번호와 호 번호는 다르다: 파일 100 = 105호, `ASSB_TRANSFER_NOTE.md` §6-3-k). **모형 편 — Argonne(ANL) · Louisville 의 다중 규모 계산: DFT(AIMD + GGA+U)로 NMC | LLZO 계면 파괴 에너지 하나(2.0 J m⁻²)를 내고, 2D 삼각 격자 스프링(lattice spring) 메조 모형에서 양극 판(NMC · LCO) | LLZO(입내 GI · 입계 GB) 계면 요소가 변형 에너지 문턱을 넘으면 지워지는 '박리' 를 풀어 첫 사이클 · 10 사이클 방전 용량을 본 편 · 자기 측정 0 · 실험 대조 = 다른 편(Wang 2019) R_ct 곡선 하나.**

Argonne National Laboratory(Lemont) + University of Illinois at Chicago(화공) + University of Louisville(기계) — **Pallab Barai** · **Tomas Rojas** · **Badri Narayanan** · **Anh T. Ngo**(교신 \*) · **Larry A. Curtiss** · **Venkat Srinivasan**(교신 \*)의 *Chemistry of Materials* 2021 편 + SI 25 쪽. `[인쇄]` 초록이 스스로 적는다: "The extent of delamination, and its impact on impedance rise and capacity fade, is determined by a number of material properties, including cathode molar volume change and state-of-charge dependence, mechanical properties of the cathode and SSE, SSE grain boundary microstructure, fracture threshold of the interface, and interfacial exchange current density. The goal of this paper is to develop multiscale mathematical models to link these material properties to performance and provide guidance on possible approaches to minimize delamination, impedance rise, and capacity fade. … Density functional theory (DFT) is used to determine fundamental material properties at the interface, while mesoscale models are used to link these properties to macroscopic performance. Model results suggest that SSEs with smaller grains and low Young's modulus and cathodes with low molar volume changes provide opportunities for minimizing delamination."

들어온 경로: 원장 행(흡수 전 원문 그대로) "| ★★★★ | **Barai·…·Srinivasan 2021** — *Chem. Mater.* **33**, 5527 | 53 · 75 · 83 · 94 | **4** | **Q1** | **사이클 축 박리 모델** — 'mechanical detachment 에 의한 용량 감쇠가 10 사이클 동안 포화 없이 지속' — 53호 종설이 가리킨 **유일한 θ(N) 모델 원전**(53호 공저자의 자기 인용). 합성 truth 의 θ(N) 형태(계단형 vs 점진형) 결정 근거 후보 · 75호 [48] 재지목 … · 83호 [13] 재지목 … · 94호 [20] 재지목 … |". 지목 현황: 위키 grep(`Barai` · `5527` · `Chem. Mater.* 33` · `Srinivasan`)으로 다시 셌다 — **후속 절에 오른 것은 53호 [127](★★★★) · 75호 [48](지목 +1) · 83호 [13](후속 표) · 94호 [20](★★★★) = 4 = 원장 일치** · 49호(Barai 2018 *Sci. Rep.* — 같은 제1저자 · **다른 편 · 액체셀**)는 셈 밖.

이 digest 의 일 (지시):

1. **(a) `θ(N)`** — 계보가 가리킨 유일한 `θ(N)` 모형 원전인가: 박리 분율이 사이클에 따라 어떻게 진화하나(계단형 ↔ 점진형) · 그것이 모형 출력인지 측정인지 · 측정 검증이 있는지.
2. **(b) 접촉 손실 ↔ `LAM_PE`** — 별개 손잡이인가, 곱(`A_eff · j₀` 류)으로만 들어가는가 — 곱 축퇴 처방의 대상.
3. **(c) 합성 truth 요구 R1–R8** 중 무엇을 충족 · 위반하는가.
4. **(d) 다중 규모 방법** — 원자 계산 → 계면 강도 → 연속체 · 입력 출처 · 실험 비교.
5. **(e) 원장 행 지목 명제 넷(53 · 75 · 83 · 94)을 원문과 대조**.
6. (지시 밖 · 이 digest 가 덧붙인 축) **(f) 같은 조건 그림 사이 산포**(한 실현 · 문턱 확률성) · **(g) 인쇄 식 · 표 재풀이**.

⚠ **표기 규약**: `[인쇄]` = 원문이 실제로 쓴 것 · `[도표]` = 그림을 눈으로 읽은 값(판독 폭 표시 · SI 그림은 JPEG 라 눈 판독) · **`[도표·화소]`** = 본문 그림이 전부 Flate(무손실) 래스터라 PDF 에서 **원본 래스터를 꺼내** 축 틀 · 눈금 화소로 선형 보정하고 표지는 속 빈 표지 형판(사각 · 원 · 마름모 · 역삼각) 맞춤으로 중심을 읽은 값(그림마다 보정 잔차 · 판독 폭을 적는다) · `[재현]` = 인쇄 수치 · 식으로 우리가 계산(스크립트는 `scratchpad/p105/` 에만 — 커밋 안 함) · `[재현·가정]` = 인쇄되지 않은 값을 가정해 계산(가정 명시) · `[재현·대수]` = 인쇄 식 위의 대수 · `[외부 값]` = 원문 밖 상수 · `[해석]` = 우리 판단. **`[데이터]` 표시 0** — 원자료 · 코드 공개 0.

⚠ **측정 · 인용 · 모형 · 적합 구분**: 이 편 안의 수치는 ① **측정 0** — 저자 실험 0 ② **인용 측정** — 그림 5 의 R_ct 점(Wang 2019 [17] 에서 "extracted") · 그림 10(a) · S2 의 부분 몰부피 점("Exp. Data: EES 2018 2142" = Koerver 2018 = 97호) · SI 의 R_ct 2500 · 250 Ω cm²([23] Wang 2019 · [24] Ohta 2012) ③ **계산 입력** — DFT 계면 파괴 에너지 2.0 J m⁻²("This work") · 표 S-II 나머지(문헌 · 같은 연구실 앞 편 · 가정) ④ **보정** — i₀ 를 R_ct 에서 `RT/(R_ct F)` 로 내고 "The magnitudes of reaction rate (k_ref) have been scaled accordingly" ⑤ **모형 출력** — 그림 2–9 · 10(b) · 11 · S4–S6 전부.

---

# 판정 먼저

1. ★★★★ **(a) `θ(N)` — 이 편의 N 축은 '방전 용량' 이고 박리 분율이 아니다 · 53호의 "without showing saturation" 은 이 편 문장이 아니다.** `[인쇄]` "All of the results discussed until now reported the extent of delamination, and subsequent capacity fade for only one charge−discharge cycle. … Capacity retention demonstrated by NMC and LCO over 10 cycles is depicted in Figure 9a,b … both the cathode materials experience more capacity fade with increasing number of cycles. This can be attributed to the increase in interfacial delamination and subsequent increase in interfacial resistance, with increasing number of cycles." — 그림 9 · 10(b) 는 **용량만** 그린다(10 사이클 · 1 A m⁻² · CCCV 충전 / CC 방전). **박리 분율은 N = 1 값만 인쇄**(그림 8 · S4 · S5(b) · S6(c) — '첫 충전' · '첫 사이클 뒤') · 사이클별 박리 분율 · 끊긴 요소 수 · 사이클별 R_ct 0. `saturat*` 본문 · SI **0 회**. `[도표·화소]` 10 사이클 궤적은 **계단 + 멈춤**: LCO 큰 입자 114.41 → 79.66 mAh g⁻¹(사이클 7 → 8 에 −11.45 한 번 · **8–10 평탄 79.93 · 79.52 · 79.66**) · NMC 큰 입자 ≈171.4 → 159.59(**5–8 멈춤** 164.07 · 164.07 · 163.72 · 163.31 → 9 · 10 에 −1.45 · −2.27). ⇒ **`θ(N)` 측정 0/105 · 모형 `θ(N)` 곡선 0** · 원장 이유의 '사이클 축 박리 모형' ✅ · '포화 없이 지속' 은 53호의 요약(이 편 지면 0 · 한 곡선은 끝 세 사이클 평탄) · '`θ(N)` 원전' 은 **N 축 박리 모형 원전 ✅ / `θ(N)` 곡선 원전 ❌**.
2. ★★★★ **(b) 접촉 손실이 들어가는 자리 = 계면 활성 면적 하나(`φ` 형) · 출력에는 곱 `A_f · i₀` 로만 · 결손은 η 형 — `LAM` · 고립 · Li 손실 0.** `[인쇄]` 식 (1) **"R_ct = (A₀/A_f)·(R_g T/i₀ F)"** · SI "Broken lattice spring elements cannot carry force or transfer ions through it. Effectively, the removal of a lattice-spring elements from the interface decreases the electrochemically active surface area." · 양극은 **평면 판 하나**(`[도표]` 그림 3 · 4 축 x 200–300 nm = 두께 100 nm) — 남은 계면이 판 전체에 Li 를 대므로 고립(`u`) 이 구성상 0, `ε_p` · 재고 변수 0. `[인쇄]` 그림 8 "the extent of delamination is independent of the current density. However, the capacity fade increases with increasing current density" · 그림 S4 "interfacial delamination is independent of the exchange current density. However, increasing exchange current helps to minimize the activation overpotential, and effectively leads to smaller capacity fade" ⇒ 결손은 **컷오프에서 보이는 동역학 결손**(η 형 — §3-b (랴)). `[재현·대수]` 그런데 NMC 는 i₀ 0.2 A m⁻² · 1–7 A m⁻² 라 **i/i₀ = 5–35(Tafel 영역)** — 박리 몫 Δη ≈ (2RT/F)·ln(A₀/A_f) 는 **전류와 무관**하다: 그림 8(a) 의 분율 그대로면 1 · 3 · 5 · 7 A m⁻² 에서 Δη **86.8 · 49.0 · 55.4 · 44.1 mV**(대칭 BV · 남은 면 균일 전류 가정) — 인쇄 설명 "η_intf = i_app·R_intf"(선형)는 이 편 자신의 동역학 영역과 맞지 않고, 감쇠는 16.97 → 19.28 mAh g⁻¹(×1.14 · 전류 ×7)로 거의 율 무관이다. ⇒ **면적형 접촉 손실을 율 스윕으로 '물질 손실' 과 가르려면 i ≪ i₀·A_f/A₀(선형 영역)까지 내려가야 한다**(NMC 박리 0.82 면 0.036 A m⁻² ≈ 0.4 C 상당 — `[재현·가정]` 아래 8).
3. ★★★★ **(c) 그림 5 '실험 비교' — 모형의 출발 R_ct 는 같은 실험에서 보정됐고, 중간 x 에서 실험은 모형 기구와 반대 방향이다.** `[인쇄]` SI "The value of R_ct for NMC/LLZO²³ and LCO/LLZO²⁴ interfaces have been experimentally estimated to be around 2500 Ω−cm² and 250 Ω−cm² … These charge transfer resistances lead to approximate exchange current densities of 0.2 A/m² and 2.0 A/m²" — [23] = 본문 [17] Wang 2019 = 그림 5 실험 점의 출처. `[재현]` i₀ = RT/(R_ct F)(T 300 K)는 **0.1034 · 1.034 A m⁻²** — 인쇄 0.2 · 2.0 은 **×1.93**. 그 i₀ 로 모형 R_ct ≈1293 Ω cm² → `[도표·화소]` 그림 5 모형 충전선 x 0.50–0.75 **1337–1455** ↔ 실험 충전 점 **2247 · 2424**(x 0.52 · 0.59 — 모형의 0.55–0.63 배) · 실험 방전 점 **2078 · 2103 · 2205**(x 0.52 · 0.59 · 0.68) ↔ 모형 방전선 2921–3325 · **실험은 중간 x 에서 방전 ≤ 충전(0.92 · 0.87) ↔ 모형 방전/충전 2.2–2.6**(충전 끝 박리의 결과). 그림이 '맞아 보이는' 것은 x > 0.9 의 급상승 — 모형 i₀(x) ∝ √((c_max − c)·c) 의 모양(박리 전 충전 첫머리 x 0.98 에서도 ≈5000)과 실험 점 6500–6750 이 같이 오르는 자리다(`[해석]` — §3-b (루)). 본문 "This increase in charge-transfer resistance occurs within both the experimental and computational framework, which compares very well with each other in Figure 5."
4. ★★★★ **(d) 같은 조건 그림 사이 산포가 주장된 효과보다 크다 — 그림마다 한 실현 · 문턱 확률 분포 미인쇄.** `[도표·화소]` NMC · 150 nm · 1 A m⁻² · 3.2–4.5 V · CCCV/CC: 첫 사이클 감쇠 **16.97**(그림 8(a)) · **≈17.0**(S4(a) · i₀ 0.2) ↔ **11.50**(그림 6(c)) · **≈11.7**(그림 6(a) 끝 170.0 ↔ 아주 작은 입자 181.7 · 그림 3 의 3.2 V 지점 170.1 ↔ 181.8). LCO · 150 nm · 1 A m⁻² · 3.2–4.1 V: **2.97**(8(b)) · **≈4.9**(S4(b)) · **≈5.8**(그림 4 · 3.3 V 지점) · **6.35**(6(c)) · 그림 6(b) 끝 109.2 ↔ 그림 4 무파괴 ≈120 이면 **≈10.8**. LCO 박리 분율 **0.468**(8(b)) ↔ **≈0.78**(S4(b)). 기준 경우 박리 40 · 75 nm **0.21 · 0.43**(S5(b) 자유 경계 "as shown in Figure 1(d)") ↔ **0.11 · 0.25**(S6(c) 공극 0). ⇒ NMC 의 '전류 효과'(+2.3 mAh g⁻¹)는 같은 조건 두 값 차(5.5)보다 작다. `[인쇄]` "The minor variation in interfacial delamination is attributed to the randomness of the fracture threshold used in the present simulations" · S5 "No statistically significant difference" — 분포 · 실현 수 · 통계 0.
5. ★★★★ **(e) 인쇄 식 · 표로는 저자 계산이 나오지 않는다 — 다섯 자리.** ① 표 S-I **(C5) "∇·(D_Cathode ∇c_Li) = 0"(시간 항 0) + (C7) x = L_x 에서 "−D_Cathode ∇c_Li = I_app/F"**(집전체 경계 Li 유속) — 글자 그대로면 유입 = 유출 정상 상태라 양극 Li 량이 변하지 않는다(그림 3 · 4 의 SOC 쓸기 불가 · `[재현·대수]`) · 행 이름 "at the top of SSE"(C10 은 좌 · 우 경계) · "**at Li/SSE interface**"(양극 모형에 Li 금속 계면 이름 — 같은 연구실 Li 금속 모형 [47][59] 의 틀로 읽힘 `[해석]`). ② **(S5) V̄_NMC 인쇄 다항식 ≠ 그림 S2(a) · 10(a) 'Polynomial fit'**: `[재현]` y 0.26 · 0.30 · 0.40 · 0.50 · 0.75 · 1.0 에서 **7.04 · 5.12 · 2.11 · 0.89 · 1.13 · 2.40** ↔ `[도표]` 그림 ≈15.5 · ≈11 · ≈4.5 · ≈2.8 · ≈1.7 · ≈2.0 cm³ mol⁻¹(낮은 x 에서 ×2–3) — (S6) LCO 는 그림 S2(b) 와 맞음(꼭지 −4.17 @y 0.766 ↔ ≈−4.3 @≈0.75). ③ **(S4) "ε_Li = (1/3)·V̄_Cathode·c_s"** — V̄ 가 c 에 따라 변하면 ∫V̄ dc 가 아니다: 인쇄 (S5) · (S6) 를 그대로 넣으면 V̄(y)·y/3 이 **NMC y 0.559 · LCO y 0.796 에서 꺾이는 비단조** — NMC 는 4.4 V 충전 끝(y 0.56 → 0.35)에서 오히려 **팽창**, LCO 는 방전 끝(y 0.80 → 0.99)에서 팽창 — 본문 서사("x < 0.4 … substantial shrinkage" · LCO 방전 중 수축)와 반대 · 적분꼴이면 둘 다 단조 ✅(`[재현·대수]`). ④ **(S7) 4.4 V ↔ x 0.348**(본문 "from 1.0 to 0.3" · `[도표·화소]` 그림 10(a) 빨간 선 **x 0.309 = (S7) 로 4.52 V**) · 4.1 V ↔ 0.468(본문 0.45 · 녹선 0.464 ✅) · **(S8) U_LCO(0.7) = 3.933 V**(본문 "around 3.8 V" — (S8) 로 3.8 V 는 x 0.963) · V̄_LCO 꼭지 y 0.766(본문 "around … 0.7"). ⑤ **표 S-II κ_LLZO|GI 1.1×10⁻⁵ S m⁻¹ · GB 0.4×10⁻⁵** 를 글자 그대로 쓰면 SE 200 nm 옴 **182 · 500 Ω cm²** — LCO R_ct(i₀ 2.0 → 129 Ω cm²)보다 크고 7 A m⁻² 에서 **127 · 350 mV** — 본문 "the electrochemical performance is not limited by the ionic conductivity within the LLZO phase" 와 어긋난다(S cm⁻¹ 로 읽으면 1.8 Ω cm² — 단위 의심 `[해석]`).
6. ★★★ **(d) 다중 규모 = DFT 한 수가 연속체로 · 나머지는 문헌 · 같은 연구실 앞 편.** `[인쇄]` NMC622 (101̄0) · NMC811 (101̄4) | Li 종단 LLZO (100) 계면 · 384 원자 · 격자 불일치 5.71 · 6.66 % · AIMD NVT 300 K ≈2 ps(Nose–Hoover) · GGA(PBE)+U(Ni 6.37 · Mn 4.84 · Co 5.14 eV) · 파괴 에너지 **≈2.0**(101̄0) · **2.4 J m⁻²**(101̄4) — "To keep the analysis conservative, parameters from the lowest energy surface are used" → 표 S-II "Fracture threshold energy at cathode/LLZO interface 2.0 · **This work**"(NMC · LCO 공통 — **LCO/LLZO 계면 계산 0**) · 계면 파괴 에너지 산출 정의 · 슬랩 · 수렴 미인쇄. GB 성질(κ · Y · 두께 10 nm) · LLZO 파괴 5.3 J m⁻² 은 [1, 20, 21](SI) = 같은 연구실 Barai 2020 *JES* · Yu & Siegel 2017 · 2018 · 본문은 "conductivity and elastic modulus of the LLZO GB domain … have been estimated using the lower-length-scale simulations" 라 쓰지만 이 편에서 새로 계산한 것은 계면 파괴 에너지 하나다. 입도 효과의 기둥은 **Y_GI 141 ↔ Y_GB 120 GPa(−15 %)** — `[도표]` 그림 7 최대 정규 변형 에너지 **1.16 · 1.11 · 1.04 · 0.72**(150 · 100 · 75 · 40 nm) ↔ 그림 6(c) NMC 감쇠 **11.50 · 5.20 · ≈1.0 · ≈0.4** — 문턱(정규 1) 근처 확률 파괴가 작은 응력 차를 크게 키운다(`[해석]` — 결론이 문턱 분포에 매달림 · 분포 미인쇄).
7. ★★★ **(g) 압력 · 구속 — `pressur*` · `MPa` · `stack` 본문 0** · SI 'local pressure'(부호 규약) 하나. 기계 경계(표 S-I C10 · 그림 1(d)) = **x 양끝 u_x = 0**(SE 왼쪽 · 양극 오른쪽 — 전체 길이 고정 = 정변위 · 무한 강성) + 양극 오른쪽 가운데 u_y = 0 + 위 · 아래 자유. 양극이 줄면 길이가 고정이라 계면이 당겨진다 — **인장 박리의 발생원이 이 구속**이고(`[해석]`), SI 그림 S5 는 **y 경계만** 바꿨다(x 경계 대안 0 · 그림 S1 의 '반경 방향 수축 W₂ < W₁' 과 다른 구속). 실셀 스택 압력 · 정하중 구속의 모형판은 지면 0(Q6 해당 없음 · 층 하나).
8. ★★★ **실셀과의 거리** — `[인쇄]` 계산 영역 "60 nodes along both horizontal and vertical directions … 5 nm … around 300 nm" · GB 두께 10 nm · 입도 40–150 nm("may appear much smaller than realistically observed LLZO grains") · thk 10⁻² m "Assumed" · "polycrystalline cathode particles are not being investigated" · 음극 0. `[도표]` 양극 판 100 nm · SE 200 nm · 높이 ≈260 nm(`[재현]` 60 × 5 nm × sin 60° = 259.8 nm ✅). `[재현·가정]`(ρ 4.75 g cm⁻³ `[외부 값]` · 172 mAh g⁻¹ · 100 nm) 1 A m⁻² = **≈12 C 상당**(7 A m⁻² ≈86 C) — 본문 "relatively low applied current densities, ∼1 A/m²" 는 면적 전류로 낮고 C-rate 로 높다 · C/10 이면 같은 박리 0.82 의 Δη 는 ≈4.8 mV(1 A m⁻² 의 1/18). `[도표]` 초록 그래픽은 **입자 복합 양극 + Li 음극 '여러 사이클 뒤'** 를 그린다 — 계산은 평면 판 하나 · 음극 0 · 10 사이클.
9. ★★ **Q4 — 해당 없음 · `assb` 0/105 · 아흔일곱 번째 성질** — 아래 §(g) Q4 칸.
10. ★★ **SI 받음 · 대조 ✅** — 본문이 부르는 "eq S1 · S2 · S3" · "Figure S2a,b · S2c · S3 · S4 · S6" · "Table S-II" 가 SI 안에 다 있다(그림 S1 · S5 는 SI 본문만 부름) · 자료 · 코드 공개 0.

⚠ 어긋남 **27 건**(D1–D27 — 아래 절) · 공백 **14 건**(G1–G14).

---

# ★ 중심 표 — 지목 넷 · 관련 digest 가 이 편에 건 것 ↔ 이 편 지면 (✅ 있다 · 부분 · ❌ 없다)

| # | 누가 · 무엇을 걸었나 | 이 편 지면 | 판정 |
|---|---|---|---|
| 1 | 원장 L17 이유 — "사이클 축 박리 모델 — mechanical detachment 에 의한 용량 감쇠가 10 사이클 동안 포화 없이 지속 — 53호 종설이 가리킨 **유일한 θ(N) 모델 원전**" | 10 사이클 용량 궤적(그림 9 · 10(b)) ✅ · 박리 분율 vs N 0 · `saturat*` 0 · LCO 큰 입자 8–10 평탄 | **부분** — N 축 박리 모형 ✅ · `θ(N)` 곡선 ❌ · '포화 없이' ❌(53호의 요약) |
| 2 | **53호 [127]** — `[인쇄]` "capacity fade cause[d] by mechanical detachment persists for ten cycles without showing saturation" | 그림 9 — 넷 입도 × 두 양극 모두 10 사이클 감쇠 ✅ · 10 사이클 뒤 기울기: NMC 큰 −2.27 · 중간 −0.42 · 작은 −0.76 · 아주 작은 0.00 / LCO 큰 **+0.14** · 중간 −0.41 · 작은 −1.38 · 아주 작은 −0.41 mAh g⁻¹(사이클 9 → 10 · `[도표·화소]`) | **부분** — '10 사이클 지속' ✅ · '포화 없이' 는 이 편 문장 아님 · 곡선 여덟 중 둘은 끝에서 평탄 |
| 3 | 53호 [127] — "LLZO with smaller grains, softer electrolytes (e.g., sulfides), or better interfacial adhesion … may help to minimize interfacial de-bonding" | 입도 ✅(그림 6 · 7 · 9) · 연한 SE ✅(그림 11 상 지도) · 접착 — "interphase layers … higher fracture energies between the cathode and the interphase layer"(추측 · 계산 0) | **✅**(모형 결론 · 접착은 계산 0) |
| 4 | 53호 G2 — "θ 를 무엇으로(면적 · 연결 분율 · 균열 길이), 10 사이클 곡선의 수치" | **면적 분율**("fractional interfacial delamination" — 끊긴 계면 격자 요소 비율 0–1) · N = 1 만 · 10 사이클 수치는 용량만 | **답** — 면적 · 첫 사이클만 · 수치는 §(a) 표 |
| 5 | 원장 이유 — "합성 truth 의 θ(N) 형태(계단형 vs 점진형) 결정 근거 후보" | 비가역 결합 제거의 누적 · 용량 궤적 = 계단 + 멈춤 · 용량 ↔ 면적 사상이 로그(Tafel) | **부분** — 형태 후보 하나 더(결합 제거형) · 용량 궤적으로 `θ` 궤적을 읽을 수 없음(§(a) 3) |
| 6 | **75호 [48]** — "Large volume fluctuations of the AM over cell operation can exacerbate this scenario by further depleting the electrical contact between the AM and SE particles.43,45−48" | 부피 변화(부분 몰부피 × Δc) → 계면 인장 → 계면 요소 파괴 → 활성 면적 ↓ ✅ · 입자 0(평면 판) · 줄어드는 것은 이온 전달 계면(전자 경로 γ 1 S m⁻¹ 는 그대로) | **✅ 기구** · 단 '입자' · '전기 접촉' 은 아님 |
| 7 | **83호 [13]** — 산화물 SE 공소결 예시 "[6,13-14]" | 서론 `[인쇄]` "Synthesis of cathodes with SSEs involves a high-temperature sintering process … During cooling … thermal expansion coefficient … has the potential to delaminate [34]" · "co-sintering Ta:LLZO with LCO even at 1050 °C did not lead to any interdiffusion [31]" · 모형은 소결 뒤 완전 접합에서 시작("This lattice mismatch strain is already there as soon as the surface is formed during the sintering process") | **✅ 서론 맥락** — 83호 판정('다른 자리') 확인 · 공소결 실험 0 |
| 8 | 58 · 83호가 비운 'CAM\|SE × N 축' 칸(원장 행 · 개념 R8) | 2D 삼각 격자 스프링 · 계면 한 층 요소 · 문턱 초과 시 제거(연화 없는 취성 · 응집 영역 모형 아님) · 10 사이클 | **✅ 모형**(측정 0) |
| 9 | **94호 [20]** — "the delamination of cathode active material and solid electrolyte upon cycling" 2D 모형 셋의 첫째 | 2D ✅ · 사이클 ✅ · 비가역 ✅ — 94호(무접착 가역 Signorini · 예압 스프링 · 반 사이클)와 대비 ✅ · 둘 다 결손은 η 형(94호 입자 안 농도 · 이 편 계면 동역학) | **✅** — 대비 성립 · 이 편 구속은 정변위 |
| 10 | 개념 [[assb-synthetic-truth-contact-loss-requirements]] R8 — "Barai 2021(원장 ★★★★, 사이클 축 박리 모델 — 미흡수)" | 위 1 · 5 | R8 후보 — 결합 제거형 누적(§ 합성 truth 대조) |
| 11 | 원장 §2 공백 — "`θ(N)` 측정량 0/104" | 측정 0 · `[인쇄]` "Due to the limited experimental efforts in visualizing the extent of interfacial delamination observed at the C/SSE interface,16,17 it is not possible to directly compare the extent of delamination experienced by NMC/LLZO and LCO/LLZO interfaces with experimental observations." | **0/105** — 저자 스스로 측정 공백을 인쇄 |
| 12 | 원장 §3-b (키) — "피로 응집 영역 모형 형 N 축" 메모(83호) | N 축 = 사이클당 하중(SOC 스윙 — 차단 전압) × 문턱(확률 · 분포 미인쇄) × 결합 제거 | **✅ 둘째 표본**(CAM\|SE 판 · 결합 제거형) |
| 13 | 카드 Q1 · Q2 · Q6 | Q1 모형 면적 분율(N = 1) · Q2 독립 관측 0 · Q6 압력 0(정변위 구속 층) | 층 하나 · 없다 · 해당 없음 |

---

# 서지

| 항목 | 값 (`[인쇄]` — p. 5527 · 5538 · SI p. 1 · 정보 사전 · XMP) |
|---|---|
| 제목 | **"Investigation of Delamination-Induced Performance Decay at the Cathode/LLZO Interface"**(지면 = XMP dc:title · 정보 사전 title 은 조판 이름 "cm0c04656 1..15") · SI 표지 "Supplementary Information for: Investigation of Delamination Induced Performance Decay at the Cathode/LLZO Interface"(하이픈 0) |
| 저자 · 소속 | **Pallab Barai** · **Tomas Rojas** · **Badri Narayanan** · **Anh T. Ngo**\* · **Larry A. Curtiss** · **Venkat Srinivasan**\* — Argonne National Laboratory, Lemont, Illinois 60439 · Department of Chemical Engineering, University of Illinois at Chicago(Ngo · Srinivasan) · Department of Mechanical Engineering, University of Louisville(Narayanan · Srinivasan) · 교신 메일 인쇄(옮기지 않음) · ORCID 넷(Barai · Narayanan · Curtiss · Srinivasan — XMP dc:creator 여섯 중 같은 넷) |
| 저널 | *Chem. Mater.* **2021**, **33**(14), **5527−5541** · Article · doi `10.1021/acs.chemmater.0c04656` · ISSN 0897-4756 · eISSN 1520-5002(XMP) |
| 일정 | "Received: December 5, 2020 · Revised: May 6, 2021 · Published: July 8, 2021" · `[재현]` 접수 → 출판 **215 일** · 수정 → 출판 63 일 · SI 표지 "Revised version for re-submission in Chemistry of Materials · April 2021"(SI PDF 생성 2021-05-14) |
| 저작권 | "© 2021 UChicago Argonne, LLC, Operator of Argonne National Laboratory. Published by American Chemical Society"(p. 5527 · XMP dc:rights · xmpRights:Marked True) · CC · OA 표기 0 ⇒ **구독본으로 다룬다** — 이 digest 는 인용 · 요약 · 재현 계산만 담고 그림 크롭은 위키 관례대로 `raw/figures/`(변형 없는 잘라내기) |
| 자금 · 사사 | "Vehicle Technologies Office (VTO), Department of Energy (DOE), USA, through the Battery Materials Research (BMR) program" · ANL 계약 DE-AC02-06CH11357 · "computing resources provided on Bebop … Laboratory Computing Resource Center at Argonne" · 이해 상충 없음 |
| 자료 · 코드 | 공개 저장소 · 코드 0 · SI = 방법 · 식 · 표 · 그림 S1–S6 |
| 분량 | 본문 PDF **15 쪽**(인쇄 5527–5541 · PageLabels 1–15 = PDF 쪽 · 이 digest 의 "p. N" = 인쇄 쪽 · PDF 쪽 + 5526) · 그림 **11** + 초록 그래픽 1(전부 Flate 래스터) · 표 0 · 번호 식 **(1)** 하나 · 참고문헌 **1–74**(빠진 번호 0) / SI **25 쪽**(Word → macOS Quartz) · 식 **(S1)–(S8)** · 표 **S-I**(식 C1–C12) · **S-II**(매개변수 21 행) · 그림 **S1–S6**(JPEG) · SI 참고문헌 **1–51** |
| 절 | 본문: Abstract · INTRODUCTION · METHODOLOGY · RESULTS AND DISCUSSION(Results from Atomistic Calculations · Investigation of Mechanism behind C/SSE Interfacial Delamination · Delamination-Induced Resistance Growth and Capacity Fade in NMC and LCO · Impact of LLZO Grain Size on C/SSE Delamination · Effect of Applied Current Density on Delamination and Capacity Fade · Delamination-Induced Capacity Fade over Multiple Cycles · Strategies to Mitigate C/SSE Delamination) · CONCLUSIONS · ASSOCIATED CONTENT · AUTHOR INFORMATION · ACKNOWLEDGMENTS · REFERENCES / SI: Methodology(Atomistic calculations · Mesoscale simulations) · Open circuit potential curves · Results and Discussion(Impact of exchange current density · Influence of mechanics boundary condition · Influence of nanopores) · References · Table S-I · S-II · Figures S1–S6 |
| 계(모형) | 2D(x · y) · 왼쪽 LLZO(x 0–200 nm · GI + GB 10 nm) \| 오른쪽 양극 판(x 200–300 nm — NMC 또는 LCO) · 높이 ≈260 nm · 삼각 격자 스프링(5 nm · 배위수 6 · 계면 한 층 요소) · 전하 · 질량 = 검사 체적 · 힘 = 격자 스프링 · T 300 K · 음극 0(φ_LLZO\|x=0 = 0) |
| 운전(모형) | CCCV 충전 + CC 방전 · 1 A m⁻²(전류 쓸기 1 · 3 · 5 · 7) · NMC 3.0–4.5(그림 3) · 3.2–4.5(그림 6 · 8 · S4) · 3.2–4.4(그림 9 · 10) · 3.2–4.1 V(그림 10(b) 점선) · LCO 3.2–4.1 V · CV 종료 조건 미인쇄 · 출력 "Discharge Capacity [mAh/g]"(분모 · 밀도 미인쇄) |
| 식 | 본문 (1) R_ct = (A₀/A_f)·(R_g T/i₀F) / SI (S1) BV + 응력 항 · (S2) i₀,ref = F·k_ref·(c_e)^αc·(c_s,max − c_s)^αc·c_s^αa · (S3) Δμ_e⁻ = −V̄·(Ψ/Vol_e) · (S4) ε_Li = (1/3)V̄·c_s · (S5)(S6) V̄_NMC · V̄_LCO 다항식 · (S7)(S8) U_NMC · U_LCO · 표 S-I (C1)–(C12) |

**PDF 메타데이터 (이 실행에서 직접 읽음 · pymupdf)** — **본문** **4,587,614 B** · sha256 `75f07352cb0706a42065d9162141a6a3652d3251549f604c7b1923812110cae7`(호출자 명시값 ✅ — 직접 재계산) · 헤더 `%PDF-1.3` · 15 쪽 전부 **625.436 × 818.362 pt** · 암호 0 · 정보 사전: title **"cm0c04656 1..15"** · author · subject · keywords 빈칸 · creator **"Arbortext Advanced Print Publisher 11.2.5208/W Library-x64"** · producer **"Acrobat Distiller 8.1.0 (Windows); modified using iTextSharp.LGPLv2.Core 3.7.4.0"** · 생성 **D:20210719091903-04'00'**(출판 11 일 뒤) · 수정 **D:20261117012644+00'00'**(내려받기 날 — 아래 각인과 같은 날) · XMP **3,817 B**(dc:title = 지면 제목 · dc:creator **여섯**(ORCID 넷) · publisher ACS · dc:relation SI URL · prism volume 33 · issue 14 · 5527–5541 · publicationDate 07/08/2021 · versionIdentifier "Issue" · xmpRights Owner "UChicago Argonne, LLC") · `%%EOF` 1 · startxref 1 · EmbeddedFiles 0 · 책갈피 0 · 래스터 **13**(p. 1 초록 그래픽 958×528 · 학술지 표지 축소판 298×397 · 그림 1–11 각 하나: 1350×819 · 850×1433 · 850×1033 · 850×1032 · 667×578 · 1917×522 · 1496×546 · 667×1113 · 667×1078 · 667×1035 · 583×576 — 전부 Flate RGB) · 쪽마다 바닥 각인 "Downloaded from pubs.acs.org/cmatex/article-pdf/33/14/5527/… by [기관 이름 — 옮기지 않음] user on 17 November 2026". **SI** **2,068,023 B** · sha256 `698bde5ed05db070f69bcd0364b9f9ef92338e49843770977de6de3032ea3a63`(✅ 재계산) · `%PDF-1.3` · 25 쪽 **612 × 792 pt** · title **"Microsoft Word - SI_NMC_LLZO_Multiscale_Revised_NOT_Highlighted.docx"** · creator "Word" · producer **"macOS Version 10.14.6 (Build 18G9028) Quartz PDFContext; modified using iTextSharp.LGPLv2.Core 3.7.4.0"** · 생성 **D:20210514204840Z** · 수정 D:20261117012658+00'00' · XMP 1,547 B(xmp:CreateDate 2021-05-14T20:48:40Z · DocumentID uuid:7f206b02-… · InstanceID uuid:525d81d0-…) · `%%EOF` 1 · EmbeddedFiles 0 · 래스터 **6**(그림 S1–S6 · JPEG ICCBased) · 쪽마다 같은 각인(article-supplement/389554/pdf/cm0c04656_si_001).

⚠ **텍스트 층**: 본문 합자(ﬁ · ﬂ · ﬀ · ﬃ) · 줄 끝 하이픈 · 식 (1) 이 낱글자로 흩어짐("= · R A A R T i F ( / ) ( / ) ct 0 f g 0 (1)") → **식 (1) 은 쪽 렌더로 읽었다**. SI 는 수학 글꼴이 깨져 식 (S1)–(S8) · 표 S-I · S-II 의 지수 · 기호가 엉뚱한 글자로 추출된다(예: "1.0 × 10*)D" · "6.6 × 10*):" · 변수 아래첨자 "𝑉$;38<=>&") → **식 · 표는 쪽 렌더 · 수동 크롭으로 읽었다**(렌더: 1.0×10⁻¹⁴ · 6.6×10⁻¹² 등).

---

# 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | **사이클별 박리 분율 · 끊긴 요소 수 · 사이클별 R_ct** — 그림 9 · 10(b) 는 용량만 · 분율은 N = 1(그림 8 · S4 · S5(b) · S6(c)) | `θ(N)` 형태를 이 편으로 정할 수 없다 — 용량 궤적은 면적 궤적의 로그 사상(Tafel)을 거친다(§(a) 3) |
| **G2** | **문턱 확률성** — "the randomness of the fracture threshold used in the present simulations" 의 분포 · 폭 · 실현 수 · 씨앗 · 그림마다 같은 실현인지 0 | 같은 조건 그림 사이 산포(판정 4)가 효과 크기와 같은 자릿수 — 어느 차이가 의미 있는지 기준이 없다 |
| **G3** | **요소 문턱 환산** — Ψ̄_t 는 J m⁻²(면적당) · Ψ = ½ f·u 는 J — 곱한 면적(l·thk?) · 정규화 그림(2(c) · 7)의 분모 미인쇄 · GB 파괴 문턱 행 0(본문은 "the fracture energy at the LLZO grain boundaries can also be smaller" 라고만) | 문턱 한 수가 결론(입도 · 상 지도)의 경계를 정한다 |
| **G4** | **c_s,max · c_e(GI · GB) · 초기 SOC · 양극 밀도 · CV 종료 조건** 미인쇄 | (S2) i₀ · (S4) 변형 · mAh g⁻¹ 를 다시 풀 수 없다 — k_ref 값만으로 i₀ 0.2 · 2.0 이 나오는지 확인 불가 |
| **G5** | **양극 · SE 두께** — 본문은 "∼300 nm" 영역만 · 그림 3 · 4 축으로 100 · 200 nm 로 읽힘 · 전류의 C-rate 환산 0 | '낮은 전류' 의 실제 율(≈12 C 상당 `[재현·가정]`) · 실셀 이식의 조건 |
| **G6** | **그림 5 실험 자료 경로** — Wang 2019 [17] 에서 "extracted"(디지타이즈 방법) · "normalized by the electrode cross-sectional area"(면적 값) · 전압 → x 환산 방법 · 셀(NMC 조성 · 입도) 0 | 검증 그림의 무엇이 측정인지 · 축 변환이 무엇에 기댔는지 |
| **G7** | **DFT 파괴 에너지 정의** — 분리 일(work of separation)인지 · 슬랩 두께 · 진공 · k 점 · 수렴 · AIMD 뒤 정적 계산 여부 · LCO/LLZO 계산 0 | 연속체 문턱 2.0 J m⁻² 하나가 이 편 다중 규모의 유일한 새 연결 |
| **G8** | **시간 적분 · 파괴 반복** — 시간 단계 · 표 S-I (C5) 의 시간 항 · 격자 스프링의 화학 변형 구현(열팽창 유비?) · (S4) 적분꼴 여부 · 파괴 알고리즘(SI [15] Nukala 2005 인용) 반복 규칙 | 인쇄 식 그대로는 SOC 가 안 변한다(판정 5 ①) |
| **G9** | **응력 → Δμ 결합 몫** — (S1) · (S3) 의 응력 항이 전압 · 박리에 준 크기 · 꺼 본 대조 0 | '접촉 손실 몫' 과 '응력 평형 몫'(103호 (쵸))이 같은 곡선에 섞인다 |
| **G10** | **그림 11 상 지도 계산** — 격자 점 수 · '박리 큼 ↔ 무시' 판정 문턱 · Y_Li 값 · 오차 막대 범위 정의 | 상 지도는 첫 사이클 · 큰 입도 하나의 결과인데 처방(연한 SE · 영변형 양극)의 근거로 쓰인다 |
| **G11** | **나노 공극(S6) 의 면적 · 용량 효과** — 공극이 활성 면적을 줄인 몫("these interfacial pores also decrease the electrochemically active surface area") 계산 0 · 'fractional delamination' 에 초기 공극이 들어가는지 0 | 25 % 공극이 '더 많은 박리' 인지 '처음 넣은 공극' 인지 갈리지 않는다 |
| **G12** | **x 방향 구속** — 양끝 u_x = 0(정변위 · 무한 강성)의 근거 · 대안(유한 강성 · 정하중) 0 | 인장 박리의 크기를 이 구속이 정한다(판정 7) |
| **G13** | **κ_LLZO 단위 · GB 두께 근거** — 표 S-II S m⁻¹ · GB 10 nm 는 [47][63](본문 [63] = Schwaiger 2003 '나노결정 니켈 변형률 속도 민감도') | 옴 몫 판정('not ohmically limited')이 단위에 매달린다 |
| **G14** | **OCP 함수 출처 대응 · NMC 조성** — (S7)(S8) "obtained from existing literature18, 47"(SI [18] Guo 2011 SPM 열 · [47] Awarke 2013 파우치 SEI — 어느 것이 어느 쪽인지 0) · NMC 조성: DFT NMC622 · 811 ↔ 그림 S2(c) 표지 "Cathode: NMC111" ↔ 부분 몰부피 자료(97호 판독 대조로 NCM-622 끝점에 가까움 `[해석]`) | 양극 화학 · 평형 곡선이 한 셀의 것인지 정해지지 않는다(Q8) |

---

# 보충 자료 — 받은 것 · 대조

**SI 받음(25 쪽 · `7afb4d94` · sha256 698bde5e… ✅).** 본문이 부르는 SI 자리 대조(본문 · SI 전문 grep — NFKC · 줄 이음 뒤):

| 본문 자리 | 부른 것 | SI 안 | 대조 |
|---|---|---|---|
| p. 5528 "(see Figure S2a,b in the SI)" | NMC · LCO 부분 몰부피 | 그림 S2(a)(b) | ✅ |
| p. 5529 "as seen in Figure S3" | DFT 계면 둘 | 그림 S3 | ✅(캡션 면 지수 어긋남 — D21) |
| p. 5530 "eq S1 · eq S2 · eq S3 in the SI" | BV · i₀ · 응력 항 | 식 (S1)–(S3) | ✅ |
| p. 5531 "(see Figure S6)" | 나노 공극 | 그림 S6 | ✅ |
| p. 5533 "(magnitude provided in Table S-II in the SI)" | GB 전도도 | 표 S-II | ✅ |
| p. 5533 "(see Figure S4 in the SI)" | i₀ 효과 | 그림 S4 | ✅ |
| p. 5533 캡션 "(as shown in Figure S2c)" | 미세구조 넷 | 그림 S2(c) | ✅ |
| p. 5537 "Figure S2b" | LCO 비단조 V̄ | 그림 S2(b) | ✅ |
| SI 본문만 | 그림 S1 · S5 · 표 S-I | 있음 | ✅ |

`video` · `movie` · 원자료 · 코드 언급 0 · 임베디드 파일 0 ⇒ 재현은 **인쇄 수치 · 식 · 래스터 그림 화소**로만 했다(`[데이터]` 표시 0).

---

# 그림 · 표 — 자동 11 항목 + 수동 9, 실제로 연 것 **20/20**

크로퍼(`wiki/tools/extract_figures.py --clean`)가 본문 그림 1–11 을 잡았다(캡션 인식 ✅ · 잘림 0). **SI 는 0** — 캡션이 "Figure: S1." · "Table: S-I." 처럼 **콜론 형식**이라 캡션으로 안 잡힘(`SI_TAG` 판별은 실행 전 정규식으로 확인 — 본문 False · SI True). 수동 9(300 dpi · 파일명 `…_manual_p<PDF 쪽>.png` · `figures.json` `manual: true` + note): `fig_TOC_manual_p1` · `tab_S-I_manual_p18` · `tab_S-II_manual_p19` · `fig_S1_manual_p20` … `fig_S6_manual_p25`. p. 1 의 둘째 래스터(298×397)는 학술지 표지 축소판이라 크롭하지 않았다.

**20 장 전부 이 실행에서 직접 열었다 — 안 본 그림 · 표 0.** 판독: 그림 3 · 4 · 5 · 6 · 8 · 9 · 10 은 **PDF 에서 원본 래스터(Flate)를 꺼내** 축 틀(회색 · 검정 행 · 열 합)과 눈금(틀에 수직인 짧은 선)으로 선형 보정했다(`[도표·화소]` — 그림 8(a) 85.9 px/(mAh g⁻¹) · 429.5 px/분율 · 눈금 잔차 ≤0.003 / 8(b) 42.95 px · ≤0.009 / 9(a) 14.5 px · ≤0.03 / 9(b) 7.25 px · ≤0.07 / 10(b) 8.68 px · ≤0.07 / 10(a) 470 px/x / 6(c) 31.25 px/(mAh g⁻¹) · 3.2 px/nm / 6(a)(b) 2.57 · 3.42 px/(mAh g⁻¹) / 5 755 px/x · 59.33 px/(1000 Ω cm²) · ≤5 Ω cm² / 3 3.545 · 4 4.74 px/(mAh g⁻¹)). 표지는 속 빈 형판 맞춤(사각 21–27 px · 원 22–32 px · 마름모 24 · 역삼각 27 — 그림마다 실측) · 표지 중심 ±1–2 px. 겹쳐 가려진 표지는 '가려짐' 으로 적었다. SI 그림(JPEG)은 눈 판독(`[도표]` · 폭 표시). 판독 배열 · 스크립트는 `scratchpad/p105/` 에만(커밋 안 함).

## TOC — 초록 그래픽 (p. 5527 · 봤다 · 수동) ★★ 판정 8 · D23

왼쪽 "Pristine Cell"(Lithium Anode \| LLZO Solid State Electrolyte \| 둥근 "Cathode Particles") → "After Many Cycles" → 오른쪽 "Interfacial Delamination"(입자 둘레 초승달 틈 · "Cathode/Electrolyte Detachment") · 오른쪽 V–Q 모식 "With Cathode/LLZO Interfacial Delamination"(빨강) ↔ "No Cathode/LLZO Interfacial Detachment"(검정) · "Delamination Induced Capacity Fade". 자료점 0 — **입자 복합 양극 · Li 음극 · 많은 사이클의 그림**이고 계산은 평면 판 하나 · 음극 0 · 10 사이클(D23).

## Fig. 1 — 박리 모식 · 초기 배치 · 경계 (p. 5528 · 봤다 · 자동) ★★★ 판정 7 · G12

(a) Famprikis 2019 [2] 재수록(파괴 K_Ic · 접착 σ_adh · 박리 ε_electrochemical) (b) 초기 배치 — 점 격자(삼각) · LLZO GI(빨강) · GB(노랑) · 양극(주황) · 계면 (c) 수송 경계 — SSE 왼쪽 "Potential ∼ 0V" · 양극 오른쪽 I_app · 위 · 아래 "Zero flux/current" · 계면 i_BV · 충 · 방전 화살표 (d) **역학 경계 — 왼쪽 · 오른쪽 "u_X ∼ 0" · 오른쪽 가운데 녹색 점 "u_Y ∼ 0" · 위 · 아래 "Free boundary" · "Displacement continuity at interface"** (e) "Broken-Bonds and Delamination After Cycling" — × 표지(입계 · 입내) + 계면 띠 "Detachment at Interface".

## Fig. 2 — 응력 기구 둘 · 계면 전류 · 변형 에너지 (p. 5530 · 봤다 · 자동) ★★★ (b) · D26

(a) 흐름도 — "Stress Induced by Change in Bulk Concentration within Cathode" ↔ "Stress Induced by Concentration Gradient because of Microstructural Heterogeneity" (b) 계면 전류 밀도 vs y(I_app ∼1 A m⁻²) — `[도표]` 방전(빨강 ○) ≈0.84 고르게 · 충전(검정 □) ≈0.55–0.95(위 · 아래 끝 낮음) · GB 띠(y ≈115–137 nm) 집중 ≈1.13(방전) · ≈1.22(충전) A m⁻². `[재현]` 평균이 1 이 아니라 ≈0.85 인 것은 삼각 격자 요소 간격(5 nm × sin 60° = 4.33 nm)을 요소 길이 5 nm 로 나눈 꼴(1 × 0.866)과 맞는다(`[해석]` — 정규화 규약 미인쇄). (c) 정규 변형 에너지(색 0–1.16) — 계면 열(x 200 nm)이 높음 · 위 · 아래 끝 노랑 (d) 이질성 기구 — 거의 0.

## Fig. 3 — NMC 충 · 방전 · 박리 유무 (p. 5531 · 봤다 · 자동 · 화소) ★★★★ (b) · 판정 2 · 4 · D1 · D2

위 미세구조 셋(A 처음 · B 충전 뒤 · C 방전 뒤) — **축 x 0–300 nm 중 LLZO 0–200 · NMC 200–300 · y 0–≈260 nm** · B · C 계면 열에 검은 점(끊긴 결합) 거의 같음. 아래 V–Q(창 **3.0–4.5 V** 표기 · I_app 1 A m⁻² · CCCV/CC): 충전 3.45 → 3.75 V 시작 · 4.1 V 위에서 실선(박리)이 점선(무파괴)을 앞질러 4.5 V 도달(빨간 원 "Substantial delamination occur at the end of charge") · 방전은 실선이 점선보다 ≈0.1 V 낮게 평행(시작 4.27 ↔ 4.40 V). `[도표·화소]` 3.2 V 지점 실선 **170.1** · 점선 **181.8** mAh g⁻¹(ΔQ 11.7) · 3.3 V 168.5 · 181.1 · 3.4 V 161.1 · 179.7 — 본문 "ΔQ_NMC" 값 인쇄 0.

## Fig. 4 — LCO 충 · 방전 · 박리 유무 (p. 5532 · 봤다 · 자동 · 화소) ★★★★ (b) · 판정 4 · D11

미세구조 셋 — B(충전 뒤) 끊긴 결합 적음 · C(방전 뒤) 계면 열 + 입계에 많음. V–Q(3.2–4.1 V): 충전 3.27 V → 4.0 V 평탄 → 4.1 V(Q ≈107) → CV 끝 Q ≈127 · 방전 Q ≈55–80 에 실선 **계단**(빨간 원 "Substantial delamination occur during discharge") 뒤 ≈3.73 V 평탄. `[도표·화소]` 3.3 V 지점 실선 **114.2** · 점선 **120.0**(ΔQ_LCO ≈5.8) · 3.25 V 실선 114.5. 무파괴도 충전 ≈127 ↔ 방전 ≈120(CC 방전의 동역학 결손 · `[해석]`).

## Fig. 5 — R_ct: 실험(Wang 2019) ↔ 계산 (p. 5532 · 봤다 · 자동 · 화소) ★★★★ (c) · 판정 3 · D5 · D6

축 R_ct [Ω cm²] 0–8000 vs "x" in Liₓ(NMC)O₂ 0.3–1 · 범례 "Experiments (Wang et al., ACS AMI 2019, 11, 4954)". `[도표·화소]` **모형 충전선**: x 0.95 ≈2640–2940 · 0.90 1952 · 0.85 1674 · 0.75 1455 · 0.70 1421 · 0.62 1370 · 0.55 1337 · 0.50 1353 · 0.45 1589(계단) · 0.35 ≈2525 → x ≈0.345 에서 ≈3000 · **모형 방전선**: 0.35 3056 · 0.40 2980 · 0.45 2938 · 0.50 2921 · 0.55 2938 · 0.62 3031 · 0.70 3325 · 0.75 3528 · 0.85 4261 · 0.90 5078 · 0.95 ≈6660 → ≈7100 @0.96 / **실험 충전 ○**: (0.519, 2247) · (0.589, 2424) · (0.809, 2575) + `[도표]` (0.42, ≈1880) · (0.465, ≈1700) · (0.95–0.98, ≈2760–3330) / **실험 방전 □**: (0.520, 2078) · (0.590, 2103) · (0.680, 2205) · (0.810, 3022) · (0.931, 4480) · (0.940, 5373) + `[도표]` (0.95–0.96, ≈6500–6750). ⇒ 모형 방전/충전 x 0.50 2.16 · 0.62 2.21 · 0.75 2.42 · 0.90 2.60 ↔ 실험 x 0.52 **0.92** · 0.59 **0.87** · 0.81 1.17.

## Fig. 6 — 입도 넷 × 두 양극 (p. 5533 · 봤다 · 자동 · 화소) ★★★★ 판정 4 · 6 · D3 · D4

(a) NMC(창 3.2–4.5 V 표기) · (b) LCO(3.2–4.1 V) · 색: 큰(검정) · 중간(빨강) · 작은(파랑) · 아주 작은(자주). `[도표·화소]` 방전 끝(3.25 V 지점) — (a) **170.0 · 176.8 · 180.9 · 181.7** · (b) **109.2 · 112.1 · 119.4 · 120.3** mAh g⁻¹(판독 폭 ±0.5). (b) 큰 입자는 Q ≈80 에 3.66 → 3.62 V 큰 계단. (c) 감쇠 vs 입도 — NMC **150 nm 11.50 · 100 nm 5.20** · 75 · 40 nm 는 LCO 원에 가려 `[도표]` **≈1.0 · ≈0.4** / LCO **6.35 · 1.49 · 0.98 · 0.69**. ⚠ (b) 의 끝 용량 차(아주 작은 120.3 기준 큰 ≥11.1 · 중간 ≥8.2)와 (c) LCO(6.35 · 1.49)가 맞지 않는다(D4).

## Fig. 7 — 입도별 정규 변형 에너지 (p. 5534 · 봤다 · 자동) ★★★ 판정 6

LLZO 영역(x 100–200 nm) 색 지도 · 그림 안 인쇄 "Max. Norm. Energy ∼ **1.16 · 1.11 · 1.04 · 0.72**"(150 · 100 · 75 · 40 nm) · LLZO 안 0.2–0.5 · 계면 열 최대 · 위 · 아래 끝이 높음. NMC 4.5 V 충전 끝 · 1 A m⁻².

## Fig. 8 — 전류 쓸기: 감쇠 · 박리 분율 (p. 5535 · 봤다 · 자동 · 화소) ★★★★ (b) · 판정 2 · 4 · D7 · D8

`[도표·화소]` (a) NMC(150 nm · 3.2–4.5 V): I_app 1 · 3 · 5 · 7 A m⁻² → 감쇠 **16.97 · 17.10 · 17.80 · 19.28** mAh g⁻¹ · 박리 분율 **0.820 · 0.614 · 0.658 · 0.574** (b) LCO(3.2–4.1 V): **2.97 · 5.12 · 6.10 · 8.64** · **0.468 · 0.624 · 0.489 · 0.563**(표지 중심 ±1 px → ±0.012 · ±0.023 mAh g⁻¹ · ±0.002). 그림 안 문구 "Interfacial delamination independent of current density" · "Capacity fade increases with applied current".

## Fig. 9 — 10 사이클 방전 용량 (p. 5536 · 봤다 · 자동 · 화소) ★★★★ (a) · 판정 1 · D9 · D10

`[도표·화소]`(형판 맞춤 · 판독 폭 (a) ±0.15 · (b) ±0.3 mAh g⁻¹):

| 사이클 | NMC 큰 | NMC 중간 | NMC 작은 | NMC 아주 작은 | LCO 큰 | LCO 중간 | LCO 작은 | LCO 아주 작은 |
|---|---|---|---|---|---|---|---|---|
| 1 | (가려짐 ≈171.4) | 171.45 | 172.55 | 173.31 | 114.41 | 118.69 | 119.66 | 120.76 |
| 2 | 170.34 | 170.76 | 172.41 | 172.97 | 114.00 | 118.28 | 119.10 | 120.76 |
| 3 | 168.48 | 170.76 | 171.79 | 172.97 | 112.62 | 117.17 | 118.69 | 120.34 |
| 4 | 166.69 | 170.00 | 171.79 | 172.55 | 104.48 | 116.07 | 118.83 | 120.34 |
| 5 | 164.07 | 169.59 | 171.03 | 172.21 | 97.03 | 115.93 | 118.00 | 120.34 |
| 6 | 164.07 | 168.90 | 170.28 | 172.21 | 94.00 | 114.41 | 117.59 | 120.34 |
| 7 | 163.72 | 168.14 | 169.93 | 171.86 | 91.38 | 110.69 | 117.17 | 120.34 |
| 8 | 163.31 | 165.17 | 169.59 | 171.86 | 79.93 | 108.90 | 117.17 | 120.34 |
| 9 | 161.86 | 162.97 | 169.24 | 171.45 | 79.52 | 106.69 | 116.90 | 119.93 |
| 10 | 159.59 | 162.55 | 168.48 | 171.45 | 79.66 | 106.28 | 115.52 | 119.52 |

`[재현]` 10 사이클 손실(사이클 1 → 10) · 평균 기울기(9 구간): NMC **11.8(6.9 %) · 1.31 / 8.9 · 0.99 / 4.07 · 0.45 / 1.86 · 0.21** · LCO **34.75(30.4 %) · 3.86 / 12.41 · 1.38 / 4.14 · 0.46 / 1.24 · 0.14** mAh g⁻¹(cycle⁻¹). 계단: LCO 큰 구간 감소 −0.41 · −1.38 · **−8.14 · −7.45** · −3.03 · −2.62 · **−11.45** · −0.41 · +0.14 · NMC 큰 −1.1 · −1.86 · −1.79 · −2.62 · **0.00 · −0.35 · −0.41** · −1.45 · −2.27.

## Fig. 10 — 부분 몰부피 · 창 줄이기 (p. 5536 · 봤다 · 자동 · 화소) ★★★★ D12 · D13 · D14

(a) V̄ [cm³ mol⁻¹] vs x — "Exp. Data: EES 2018 2142"(○) + "Polynomial fit"(빨간 선) · `[도표]` x 0.26 ≈15.5 · 0.30 ≈11 · 0.40 ≈4.5 · 0.50 ≈2.8 · 0.75 ≈1.7 · 1.0 ≈2.0 · `[도표·화소]` 빨간 세로선(4.4 V – 3.2 V) **x 0.309** · 녹선(4.1 V – 3.2 V) **x 0.464**. (b) 방전 용량 10 사이클 — 실선(4.4 V) = 그림 9(a) 와 같은 값(±0.2 — 같은 실행으로 읽힘) · 점선(4.1 V): 큰 (가려짐 ≈139.7) · 138.85 · 138.50 · 137.81 · 137.01 · 136.66 · 136.66 · 136.31 · 135.97 · ≈135.5(가장자리) / 중간 (가려짐 ≈139.6 × 4) · 138.39 · 137.70 · 137.35 · 137.35 · 137.01 · 135.85 / 작은 139.88 · 139.88 · 139.88 · 139.54 · 139.54 · 139.54 · 139.19 · 139.19 · 138.85 · ≈139.0. `[재현]` 4.1 V 평균 기울기 큰 ≈0.47 · 중간 ≈0.43 · 작은 ≈0.10(±0.05) ↔ 4.4 V 1.31 · 0.99 · 0.45 → **비 2.8 · 2.4 · 4.5**.

## Fig. 11 — 상 지도 (p. 5537 · 봤다 · 자동) ★★★ G10 · D15

축 V̄ [cm³ mol⁻¹] 0.2–50(로그) vs YM_SSE/YM_Li 1–20(로그) · 청록 "Negligible Delamination" ↔ 노랑 "Extensive Interfacial Delamination" · 경계 둘 "Ψ_t,C/LLZO ∼2.0 J/m²"(위) · "Ψ_t,C/Sulfides ∼0.8 J/m²"(아래) · `[도표]` 경계 x 1 에서 ≈3.1 · ≈1.7 → x 20 에서 ≈0.75 · ≈0.53 · 표지: LCO/Sulfides · NMC/Sulfides(x ≈2.2) · LCO/LLZO · NMC/LLZO(x ≈14.5) — LCO 표지 ≈6.5(막대 ≈2.8–35) · NMC ≈2.0(막대 ≈1.0–4.2). `[재현·외부 값]` Y_LLZO|GI 141 GPa 를 x ≈14.5 에 놓으면 Y_Li ≈9.7 GPa(값 미인쇄 · G10).

## Table S-I — 식 · 경계 (SI p. 18 · 봤다 · 수동) ★★★★ (e) · 판정 5 · D16 · D17

(C1) ∇·(κ_LLZO∇φ_LLZO) = 0 · ∇·(γ∇φ) = 0 · (C2) 위 · 아래 전류 0 · (C3) 왼쪽(LLZO) · 오른쪽(양극) −κ∇φ\|x=0 = I_app · −γ∇φ\|x=Lx = I_app · (C4) 계면 = i_BV · **(C5) "No diffusion of Li⁺ within LLZO" · 양극 ∇·(D_Cathode∇c_Li) = 0** · (C6) 계면 −D∇c = i_BV/F · **(C7) x = L_x 에서 −D∇c = I_app/F** · (C8) φ_LLZO\|x=0 = 0 · (C9) ∇·σ = 0 · **(C10) "Displacement boundary condition at the top of SSE": u_x(x = 0, y) = 0 · u_x(x = L_x, y) = 0 · u_y(x = L_x, y = L_y/2) = 0** · "Displacement boundary condition at **Li/SSE interface**: Continuity in force and displacement" · (C11) 축 · 전단 스프링 f = k·u · (C12) k_a = Y(1+ν)·thk/(2√3(1−ν²)) · k_s = Y(1−3ν)·thk/(2√3(1−ν²)).

## Table S-II — 매개변수 21 행 (SI p. 19 · 봤다 · 수동) ★★★★ (d) · (e)

γ_Cathode **1.0 S m⁻¹** [47] · D_Cathode **1.0×10⁻¹⁴ m² s⁻¹** [47, 51] · κ_LLZO\|GI **1.1×10⁻⁵ S m⁻¹** · κ_LLZO\|GB **0.4×10⁻⁵** [1, 20, 21] · V̄_Cathode **m³ mol⁻¹** "See Eqs. (S5) and (S6)" [27] · F 96485 · R 8.314 · **T 300 K** · α_a = α_c **0.5** [18] · k_ref NMC/LLZO **6.6×10⁻¹³** · LCO/LLZO **6.6×10⁻¹²** (m s⁻¹)·(mol m⁻³)^−½ [23] · [24] · Y_Cathode **120 GPa** · ν 0.3 [31–34](NMC · LCO 공통) · Y_LLZO\|GI **141** · ν 0.2 · Y_LLZO\|GB **120** · ν 0.2 [1, 21] · Ψ̄_t,LLZO **5.3 J m⁻²** [1] · Ψ̄_Cath/LLZO **2.0 J m⁻²** "This work" · thk **10⁻² m** "Thickness of solid state electrolyte" · "Assumed". 행 없음: c_s,max · c_e · 초기 SOC · 밀도 · 문턱 분포 · GB 파괴 문턱(G3 · G4).

## Fig. S1 — 계산 영역의 수축 도식 (SI p. 20 · 봤다 · 수동) ★★ 판정 7

구 입자 표면의 작은 상자 · "Delithiation induced shrinkage" · "R₂ < R₁ · L₂ < L₁ · W₂ < W₁" · "During shrinkage of a sphere, its radial as well as azimuthal dimensions decrease." — 그런데 모형은 반경(x) 양끝을 u_x 0 으로 묶는다(판정 7 · `[해석]`).

## Fig. S2 — 부분 몰부피 · 미세구조 넷 (SI p. 21 · 봤다 · 수동) ★★★★ D12 · D20

(a) NMC "V̄_NMC > 0" · "Range of operation" 녹선 x ≈0.33 · 자료 x 0.26–1.0 (b) LCO "V̄_LCO < 0" · 녹선 x ≈0.47 · 자료 x 0.20(≈21) → 0 @≈0.53 → 최소 ≈−4.3 @≈0.75 → ≈0 @1.0 (c) 미세구조 넷 d_Grains ∼150 · 100 · 75 · 40 nm — 각 판 표지 **"Cathode: NMC111"**.

## Fig. S3 — DFT 계면 둘 (SI p. 22 · 봤다 · 수동) ★★★ D21

왼쪽 "NMC (811)" · 오른쪽 "NMC (622)" 위 · "LLZO" 아래 · 범례 La(청록) · Co(파랑) · Mn(자주) · Ni(회색) · Li(연두) · O(빨강) · Zr(주황). `[도표]` **위쪽(표지 'NMC')에 La · Zr 다면체, 아래쪽(표지 'LLZO')에 Ni · Co · Mn** — 표지가 뒤바뀐 것으로 읽힌다 · 캡션 "a) … (101̄4) surface of NMC811. b) … (101̄4) surface of NMC622" ↔ 본문 "(101̄0) and (101̄4) surfaces of NMC622 and NMC811, respectively".

## Fig. S4 — 교환 전류 쓸기 (SI p. 23 · 봤다 · 수동) ★★★★ (b) · 판정 2

`[도표]`(±0.2 mAh g⁻¹ · ±0.01) (a) NMC 3.2–4.5 V: i₀ ≈0.2 · 2.0 · 3.0 · 5.25 A m⁻² → 감쇠 ≈17.0 · 15.6 · 13.4 · 10.8 · 박리 ≈0.82 · 0.79 · 0.75 · 0.77 (b) LCO 3.2–4.1 V: i₀ ≈0.2 · 0.4 · 2.0 → ≈15.2 · 13.3 · 4.9 · ≈0.76 · 0.78 · 0.78. 캡션 "interfacial delamination is independent of the exchange current density. However, increasing exchange current helps to minimize the activation overpotential, and effectively leads to smaller capacity fade."

## Fig. S5 — y 경계 자유 ↔ 고정 (SI p. 24 · 봤다 · 수동) ★★★ 판정 4 · 7 · D18

(a) 위 · 아래 "Fixed boundary, u_Y ∼ 0" · 좌우 u_X ∼ 0 그대로 (b) `[도표]` 첫 충전 박리 — 자유 40 · 75 · 100 · 150 nm ≈**0.21 · 0.43 · 0.62 · 0.82** · 고정 ≈0.12 · 0.38 · 0.62 · 0.86 · 캡션 "No statistically significant difference".

## Fig. S6 — 나노 공극 (SI p. 25 · 봤다 · 수동) ★★★ D18 · D19 · G11

(a) 공극 없음 "Fractional Delamination ∼ 70%" (b) 녹색 × 공극 · "∼ 35%" (c) `[도표]` 첫 충전 박리 — 공극 0: **≈0.11 · 0.25 · 0.65 · 0.85**(40 · 75 · 100 · 150 nm) · 10 %: ≈0.17 · 0.26 · 0.39 · 0.35 · 25 %: ≈0.36 · 0.43 · 0.49 · 0.47.

## 본문 서술과 어긋난 그림 · 표 (요약)

| 그림 · 표 | 본문 서술 | 그림 · 재현 | 자리 |
|---|---|---|---|
| 그림 5 | "compares very well" | 중간 x 실험 방전 ≤ 충전(0.92 · 0.87) ↔ 모형 2.2–2.6 · 모형 충전선 = 실험의 0.55–0.63 배 | D5 · D6 |
| 그림 6(b) ↔ 6(c) | 같은 실행의 감쇠 | (b) 큰 ≥11.1 · 중간 ≥8.2 ↔ (c) 6.35 · 1.49 | D4 |
| 그림 8 ↔ 6(c) · S4 | 같은 기준 조건 | NMC 16.97 ↔ 11.50 · LCO 2.97 ↔ 6.35 · 박리 0.468 ↔ ≈0.78 | D3 · D7 |
| 그림 8 | "the extent of fractional interfacial delamination is found to be constant" | NMC 0.574–0.820 · LCO 0.468–0.624 | D8 |
| 그림 9 · 10(b) | "0.5−1.0 · 0.1−0.3 mAh/(g cycle)" · "4×" | 0.45–1.31 · 0.10–0.47 · 비 2.4–4.5 | D9 · D10 |
| 그림 10(a) | 4.4 V ↔ "1.0 to 0.3" | 빨간 선 x 0.309 = (S7) 4.52 V · 4.4 V 는 x 0.348 | D13 |
| 그림 S2 · 10(a) | "(S5) polynomial fit used in the computational simulations" | 인쇄 (S5) 가 그림 맞춤선과 ×2–3 다름 | D12 |
| 그림 11 | "error bars indicate the range of lithium partial molar volume" | NMC 막대 ≈1.0–4.2 ↔ 창 안 V̄ ≈1.7–≈11 · LCO ≈2.8–35 ↔ 창 안 \|V̄\| ≤4.2 | D15 |
| 그림 S3 | 본문 (101̄0) NMC622 | 캡션 둘 다 (101̄4) · NMC/LLZO 표지 뒤바뀜(원소 색) | D21 |
| 그림 S2(c) | DFT NMC622 · 811 | 표지 "NMC111" | D20 |
| TOC | — | 입자 · Li 음극 · 많은 사이클 ↔ 계산 평면 판 · 음극 0 · 10 사이클 | D23 |

---

# 절별 해체 (본문)

## Abstract (p. 5527)

`[인쇄]` 박리 정도와 임피던스 · 용량에 대한 영향을 정하는 물성 목록(양극 몰부피 변화와 SOC 의존 · 양극 · SE 역학 · SE 입계 미세구조 · 계면 파괴 문턱 · 계면 교환 전류) · 목적 "develop multiscale mathematical models to link these material properties to performance" · 양극 둘(LiNi₀.₈Mn₀.₁Co₀.₁O₂ "with a positive molar volume change" · LiCoO₂ "with a negative molar volume change") vs Li₇La₃Zr₂O₁₂ · DFT → 메조 · 결론 "SSEs with smaller grains and low Young's modulus and cathodes with low molar volume changes provide opportunities for minimizing delamination." — ⚠ 초록의 NMC 는 **811**(DFT 의 한 계면)인데 계산 문턱은 622 계면 값이고 미세구조 표지는 111(D20).

## INTRODUCTION (p. 5527–5529)

- 계면 문제 셋 `[인쇄]`: "(i) lack of interfacial contact between the cathode and SSE due to their low deformability · (ii) interdiffusion of ions … passivation layer · (iii) interfacial delamination between the cathode and solid electrolyte that effectively decreases the electrochemically active surface area.16" — 이 편은 (iii) 만.
- 소결 박리 · 사이클 박리 구분 `[인쇄]`: "Interfacial delamination can occur during the synthesis processes, as well as at the time of cell cycling" · 열팽창 불일치 [34] · "the cathode and SSE materials are selected to match the thermal expansion coefficients.31" · "co-sintering Ta:LLZO with LCO even at 1050 °C did not lead to any interdiffusion of ions or formation of passivation layers.31"(83호 [13] 의 '공소결 예시' 자리 — 중심 표 7).
- 실험 근거 `[인쇄]`: "Several researchers have reported delamination at the C/SSE interface during charge/discharge operations.16,17,35"([16] = 23호 Koerver 2017 · [17] Wang 2019 · [35] Walther 2019 ToF-SIMS) · "Shrinkage of the cathode leads to the formation of tensile stress at the C/SSE interface, which can eventually result in delamination.16,35" · "even with small cathode particles, interfacial impedance increased by **600 Ω-cm²** during the first charge−discharge cycle … 17"(D6).
- 변수 목록(부분 몰부피 [36] · 양극 강성 [37, 38] · SE 강성 [38, 39] · 계면 파괴 에너지 [37, 40]) · "A large number of controlling parameters lend themselves to a computational approach, whereby each effect can be systematically studied."
- 기여 주장 `[인쇄]`: "Here, for the first time, a multiscale computational methodology has been developed to analyze the kinetics and dynamics of the C/SSE interfacial delamination … Some earlier publications looked into the mechanism of delamination at the C/SSE interface,38,39,43,44 but none of them studied the time evolution of the detachment phenomena."([44] = Tian & Qi 2017 — 5차 묶음 #2) · "All of the parameters required for the present analysis have been adopted from the experimental literature or estimated using lower-length-scale atomistic simulations."

## METHODOLOGY (p. 5529)

`[인쇄]` "delamination between the cathode and LLZO SSE means physical detachment between the electrode and solid electrolyte, which leads to a decrease in electrochemically active surface area and an increase in the interfacial resistance" · **배제**: "The formation of a passivation layer through interdiffusion of chemical species, or blockage of ion transport by the existence of inert impurities (such as Li₂CO₃), has not been taken into account in the present model." · "the studied delamination process is very much a mechanical phenomenon" · "conductivity and elastic modulus of the LLZO GB domain, and interfacial fracture energy between the cathode and LLZO, have been estimated using the lower-length-scale simulations"(이 편 SI 에서 새로 낸 것은 계면 파괴 에너지 — 판정 6).

## RESULTS AND DISCUSSION — 머리 (p. 5529)

`[인쇄]` 일곱 갈래 목록 · "the majority of the analysis has been conducted under relatively low applied current densities, ∼1 A/m²" · "Discharge capacity has been used as the metric to compare various cases" · "The constant current−constant voltage (CCCV) charge and constant current (CC) discharge protocols have been adopted to extract the maximum amount of discharge capacity."

## Results from Atomistic Calculations (p. 5529)

`[인쇄]` NMC622 (101̄0) · NMC811 (101̄4) | LLZO (100)(Li 종단) · 384 원자 · 불일치 변형 5.71 · 6.66 % · 전이금속 48(811: Ni 38 · Mn 5 · Co 5 / 622: Ni 28 · Mn 10 · Co 10) · 파괴 에너지 ≈2.0 · 2.4 J m⁻² · 보수적으로 2.0 · "even though the lattice mismatch strain … is quite large, around 5−6%, which is similar to the volume expansion/contraction-induced strains … their impact on the extent of interfacial delamination is expected to be negligible. This lattice mismatch strain is already there as soon as the surface is formed during the sintering process … The influence of lattice mismatch strain is automatically incorporated within the surface energies".

## Investigation of Mechanism behind C/SSE Interfacial Delamination (p. 5529–5531 · 그림 2)

`[인쇄]` 기구 둘 — "(a) … stress induced by the change in bulk concentration within the cathode-active material · (b) … tensile stress due to concentration gradients within the cathode induced by microstructural heterogeneities" · GB 전류 집중 이유 둘(GB 의 높은 Li 농도 → i₀,ref,GB > i₀,ref,GI · 응력 유도 전기화학 퍼텐셜 차) · 정규화 "a value of unity, or greater than unity, would indicate the initiation of fracture" · (b) 기구는 변형 에너지 ≈0 — "relatively higher diffusion coefficient of Li within the cathode particles (∼10⁻¹⁴ m²/s) and very thin GB regions, around 10 nm … gets smeared very quickly, within a fraction of a second"(`[재현]` (10 nm)²/10⁻¹⁴ = 0.01 s ✅) · ⇒ "**all of the delamination that occur at the interface … is due to the stress induced by the change in bulk concentration within the cathode side. In other words, changing the state of charge (SOC) within the cathode causes detachment**" · "may have a substantial impact under higher current densities (for example, extreme fast charge conditions) but will not be investigated further". 가장자리 응력 "the edges are free to move and the center is less mobile" · 공극: "nanopores can help to relax the stress … However, these interfacial pores also decrease the electrochemically active surface area" · "pores within the LLZO microstructure, which are located far away from the cathode particles, is not expected to influence".

## Delamination-Induced Resistance Growth and Capacity Fade in NMC and LCO (p. 5531–5533 · 그림 3–5 · 식 1)

- NMC(그림 3): 충전 중 수축 → 인장 → 미세 균열 → "This detachment … decreases the electrochemically active surface area, and the interfacial resistance increases" · 방전 중 팽창 → 압축 → "further delamination should not occur" · "**The inset image C in Figure 5** demonstrates the distribution of microcracks at the end of discharge"(그림 3 의 C — D24) · "the already delaminated region during charge process is unable to cause any charge transfer, and the effective interfacial resistance remains very high" ⇒ "NMC cathodes experience delamination during charge process, which results in discharge capacity fade."
- LCO(그림 4): 충전 중 팽창 → "Very minor evolution of microcracks" · 방전 중 수축 → "majority of the LCO/LLZO detachment occurred in the middle of the discharge process".
- 실험 대조(그림 5): "As demonstrated in an earlier publication by Wang et al.,17 the interfacial charge-transfer resistance between NMC and LLZO increases by approximately **1600 Ω**, during the first charge−discharge cycle" · "have been extracted from Wang et al." · "normalized by the electrode cross-sectional area before plotting" · 식 (1) · "The initial charge-transfer resistances are normalized using the electrode cross-sectional area, which is similar to the total electrochemically active surface area for the computational model because of the planar cathodes being analyzed here" · "compares very well".

## Impact of LLZO Grain Size on C/SSE Delamination (p. 5533–5534 · 그림 6 · 7)

`[인쇄]` 입도 ∼150 · 100 · 75 · 40 nm · NMC "operation has been maintained within 3.2−4.5 V"(그림 3 은 3.0–4.5 — D2) · "NMC cathodes with larger LLZO particles experience enhanced delamination" · "Due to the extremely small size of the computational domain (∼300 nm), the electrochemical performance is not limited by the ionic conductivity within the LLZO phase. Increase in grain boundaries with decreasing LLZO grain size does not add any substantial amount of extra ohmic resistance."(D25) · "**the extent of delamination in LCO is either equal or even larger than that of NMC**. In spite of the equality in delamination, since the exchange current density of the NMC/LLZO interface is lower than … LCO/LLZO,17,25 the delamination-induced impedance growth is more severe at the NMC/LLZO interface"(D11) · 실험 공백 "it is not possible to directly compare the extent of delamination … with experimental observations"(중심 표 11) · 기구 "The elastic modulus of GB is smaller than that of the GI … Softer GBs can better accommodate the volume change" · 입계 균열 "Evolution of microcracks within the grain boundaries of LLZO can impact the overall ionic conductivity … but does not influence the interfacial delamination" · "experimental studies reveal that the fracture toughness of LLZO solid electrolytes remains either independent of grain size or increase with decreasing grain size.68".

## Effect of Applied Current Density on Delamination and Capacity Fade (p. 5534–5535 · 그림 8)

`[인쇄]` "The CCCV charge ensures that the cathode gets fully charged even at higher current densities … the bulk lithium concentration, or SOC, of the cathode is the same at the fully charged state under all of the applied current densities" · "the magnitude of stress differs for NMC- and LCO-type cathodes … (a) Their partial molar volumes are different (b) They are charged to different upper cutoff voltages" · "the extent of fractional interfacial delamination is found to be constant for all of the current densities. The minor variation in interfacial delamination is attributed to the randomness of the fracture threshold used in the present simulations." · "**the interfacial overpotential (η_intf) depends on the product of applied current density (i_app) and interfacial resistance (R_intf), η_intf = i_app·R_intf**. Hence, even though the delamination-induced interfacial resistance is similar for all of the current densities, the total potential drop increases with increasing current."(판정 2 · D26).

## Delamination-Induced Capacity Fade over Multiple Cycles (p. 5535–5536 · 그림 9)

`[인쇄]` NMC 3.2–4.4 V · LCO 3.2–4.1 V · ∼1 A m⁻² · CCCV/CC · "Charging the cells using CCCV is important to avoid any spurious loss in discharge capacity due to incomplete lithiation" · "both the cathode materials experience more capacity fade with increasing number of cycles. This can be attributed to the increase in interfacial delamination and subsequent increase in interfacial resistance, with increasing number of cycles." · "decreasing the LLZO grain size helps to minimize the extent of interfacial delamination and subsequent capacity fade"(분율 · R_ct 의 사이클 값 0 — G1).

## Strategies to Mitigate C/SSE Delamination (p. 5536–5538 · 그림 10 · 11)

- NMC 창: `[인쇄]` "the partial molar volume of Li within NMC is relatively small for … x > 0.4 … for … x < 0.4 … increases sharply" · "Within this potential window [3.2−4.4 V] … changes from 1.0 to 0.3" · "if the NMC cathodes are cycled between 4.1 and 3.2 V … from 1.0 to 0.45" · "with an upper cutoff voltage of 4.4 V, the rate of delamination-induced capacity fade is around **0.5−1.0 mAh/g/cycle**, whereas if the upper cutoff voltage is lowered to 4.1 V … **0.1−0.3 mAh/g/cycle**. Hence … around **four times (4×)** improvement" · "lowers the achievable capacity from ∼170 to ∼140 mAh/g" · "the very small grains have not been analyzed because they already demonstrated minimal capacity fade".
- LCO: "nonmonotonic trend in the partial molar volume … reaches a maximum at around Li stoichiometry of 0.7" · "At a Li stoichiometry of around 0.7, the open-circuit potential (OCP) of LCO is around 3.8 V. If the upper cutoff voltage of LCO is kept below 3.8 V, the achievable capacity will be so small" ⇒ "LCO/LLZO interfaces cannot be stabilized by altering the potential window".
- 상 지도(그림 11): "The extent of interfacial delamination obtained after the first cycle has been plotted in the phase map. The electrolyte microstructure is assumed to contain large-sized grains (∼150 nm)" · 황화물 경계 ≈0.8 J m⁻² [69, 70] · "Even though the conductivities for the sulfide electrolytes are assumed to be similar to that of LLZO, it does not influence … owing to the extremely small size of the computational domains" · "both NMC and LCO cathodes demonstrate severe interfacial delamination with LLZO SSEs" · "sulfide-based solid electrolytes, with Young's modulus only two/three times (2×/3×) larger than that of Li,71 are potentially better options" · "LCO/sulfides should experience severe delamination, whereas NMC/sulfide interfaces reside close to the boundary" · "Experimentally, interfacial delamination has been observed even for NMC/sulfide systems.16" · 영변형 양극 "(V̄_Cathode < 0.5 cm³/mol)" [72] · 계면층 "LBCO … or LNTO … where 100 cycles can be achieved without any significant capacity fade"([23] Han 2018 · [19] Zhang W. 2017 = 63호).

## CONCLUSIONS (p. 5538)

`[인쇄]` 요약(원자 계산 → GI · GB · 계면 성질 "Atomistic calculations have been conducted to estimate the electrochemical, mechanical, and transport properties at the grain interior and grain boundaries of LLZO-based ceramic SSEs.52,53") · "decreasing the upper cutoff voltage of operation from 4.4 to 4.1 V can result in a 4-fold improvement" · "These strategies to minimize delamination and improve capacity retention are applicable over multiple cycles" · 영변형 양극 · 연한 SE("sulfide-based LGPS, LPS") · 한계: "only the physical detachment between the cathode and SSE has been investigated, other mechanisms can lead to impedance growth … interdiffusion … passivation layer" · "Examining the impact of interdiffusion and the effect of interfacial layers will be the subject of subsequent studies." — `[해석]` 결론의 '입도 효과 · 4배 · 연한 SE' 옆에 조건(첫 사이클 · 큰 입도 · 한 실현 · 정변위 · 300 nm · ≈12 C 상당)이 빠진다(§3-b (치) · (냐)).

## SI 절별 (SI p. 2–13)

- **Atomistic**: AIMD NVT 300 K ≈2 ps · 1 fs · Nose–Hoover · GGA(PBE) · PAW · VASP · GGA+U(U 는 [10] Zhou 2004 의 층상 LiNiO₂ · LiMnO₂ · LiCoO₂ 삽입 전압 맞춤값).
- **Mesoscale**: 전하 · 질량 = 검사 체적 · 힘 = 격자 스프링 [11, 14, 15] · BV (S1) "used as boundary condition in Eqs. (C4) and (C6)" · (S2) i₀,ref · "the definition of Butler-Volmer reaction current density (i_BV) and the exchange current density (i₀,ref) use the local electrochemically active surface area, which, in the present context, is equivalent to the planar electrode cross sectional area" · GI ↔ GB Li 농도 차 반영 · i₀ ← R_ct(판정 3) · (S3) Δμ 부호 규약 "positive … under compressive loading (p > 0), and negative … under tensile loading (p < 0)" · "As the volume of the LLZO SSEs are fixed" · (S4) · 문턱 초과 요소 제거 "which manifests itself as a microcrack within the continuum" · "Removal of multiple lattice spring elements located at the interface between cathode and SSE leads to separation … characterized as delamination" · y 경계 자유의 이유(그림 S1) · "Adoption of a periodic or zero displacement boundary condition along the y-direction … can lead to different magnitudes of stress. However, the evolution of maximum stress at the C/SSE interface should remain the same." · 입도 넷 · GB 10 nm · "polycrystalline cathode particles are not being investigated here because the cathode primary particle sizes are usually larger than 300 nm" · 60 node · 5 nm · 300 nm · 삼각 격자 · "A single layer of lattice spring elements has been assumed to exist at the interface … Rupture of any of these elements is assumed to cause delamination … Broken lattice spring elements cannot carry force or transfer ions".
- **OCP**: (S7) U_NMC · (S8) U_LCO "obtained from existing literature18, 47".
- **i₀ 효과**(그림 S4): "Since the magnitude of delamination is dictated by the change in bulk lithium concentration, or SOC, of the cathode, it does not depend on the exchange current density … R_ct ∝ (1/i₀). Hence, the magnitude of capacity fade increases for smaller exchange current densities. This trend … is clearly observed in both Figures S4(a) and **A1(b)**"(D27) · "Development of models that couple the physical delamination and chemical interdiffusion of ions … will be adopted as future research."
- **경계 조건**(그림 S5): "the real cathode particles are partially constrained by the surrounding domain, which makes the implementation of the free boundary condition not fully accurate" · "fractional delamination appears to be independent of the boundary condition along the y direction" · "**The conclusions reported in this article should be applicable to larger cathode particles embedded within thicker LLZO electrolytes as well.**"(계산 0 — §3-b (치)).
- **나노 공극**(그림 S6): "pre-existing microcracks … characterized as 'nanopores', which are also assumed to be randomly distributed according to a uniform distribution" · 70 % → 35 % · "having some nanopores definitely help … but addition of excessive microcracks aggravates the situation … There should be an optimum amount … However, such an optimization study is out of the scope" · "large pores tend to act as stress concentrators".

---

# ★ (a) `θ(N)` — 이 편의 N 축이 실제로 무엇인가 (지목 53 · 원장 R8)

## 1. 무엇이 N 에 따라 그려졌나 (`[인쇄]` → `[도표·화소]`)

- 그림 9(a)(b) · 10(b) — **방전 용량**(mAh g⁻¹) vs 사이클 1–10 · 입도 넷(10(b) 는 셋) · 1 A m⁻² · CCCV/CC. 값은 위 그림 9 표.
- N 축 위에 **없는 것**: 박리 분율 · 끊긴 요소 수 · R_ct · 전압 곡선(사이클별) · 휴지 · 저율 용량 — 전부 0(G1).
- N = 1 의 분율: 첫 충전(그림 S5(b) · S6(c)) · 첫 사이클(그림 8 · S4 · 11 "after the first cycle") — NMC 150 nm(4.5 V) **0.57–0.86** · LCO 150 nm 0.47–0.78. **4.4 V 사이클(그림 9 · 10)의 N = 1 분율은 인쇄 0**.

## 2. 형태 — 계단 + 멈춤 (`[도표·화소]` → `[해석]`)

- 넷 입도 × 두 양극 = 곡선 여덟 모두 10 사이클 뒤가 처음보다 낮다 — '10 사이클 동안 감쇠' ✅(53호 앞 절반).
- 그런데 증분이 고르지 않다: LCO 큰 입자 한 구간 −11.45(7 → 8) · 뒤 두 구간 −0.41 · +0.14(평탄) · NMC 큰 입자 5 → 8 세 구간 합 −0.76 뒤 −1.45 · −2.27. `[해석]` 계면 한 층 요소(높이 ≈260 nm · 행 간격 4.33 nm → 계면을 가로지르는 결합 ≈60–120 개 — 하나가 면적의 ≈0.8–1.7 % · 그림 8 분율 0.658 · 0.574 · 0.468 · 0.624 는 1/120 배수에 가깝다 `[도표·화소]`)를 확률 문턱으로 지우는 구성이라 증분이 이산 · 확률적이다 — **한 실현의 계단 열**이지 매끄러운 점진형이 아니고, '포화 없이' 는 10 사이클 · 한 실현으로 판정할 수 없다(곡선 둘은 끝 세 사이클 평탄).
- 53호 문장 "persists for ten cycles without showing saturation" 은 **이 편 지면에 0**(`saturat*` 0) — 53호(Ren · Danner 2023 Perspective · 공저자 Barai · Srinivasan 포함)가 그림 9 를 요약한 말이다.

## 3. ★★★★ 용량 궤적은 면적 궤적이 아니다 — 로그 사상 (`[재현·대수]`)

- 이 편의 결손은 동역학(판정 2): NMC(i₀ 0.2 · 1 A m⁻² · Tafel)에서 박리 몫 Δη ≈ (2RT/F)·ln(A₀/A_f) — 남은 면적 A_f/A₀ 가 0.18 → 0.09 로 반이 되면 ln 항이 1.71 → 2.41 로 커져 Δη **88.7 → 124.5 mV**(+36 mV). 0.82 → 0.91 의 9 %p 추가 박리가 0 → 0.82 의 첫 82 %p 만큼의 전압 몫 중 40 % 를 더한다.
- ⇒ **같은 면적 증분이 사이클 후반일수록 큰 용량 계단을 낸다** — 용량 궤적의 모양(계단 · 가속)은 `θ(N)` 의 모양이 아니라 `ln θ(N)` × OCP 기울기의 모양이다. 합성 truth R8(계단형 ↔ 점진형)을 이 편 그림으로 정하려면 박리 분율 궤적(G1)이 필요하다.
- LCO(i₀ 2.0 · i/i₀ 0.5–3.5)는 선형 ↔ Tafel 사이 — 사상이 전류에 따라 바뀐다.

## 4. 판정 — 원장 지목 명제 넷

| 지목 | 명제 | 판정 |
|---|---|---|
| **53** | "capacity fade cause[d] by mechanical detachment persists for ten cycles without showing saturation" · 유일한 `θ(N)` 모델 원전 | **부분** — 10 사이클 감쇠 ✅ · '포화 없이' 는 53호 요약(이 편 0 · 곡선 둘 끝 평탄) · N 축 박리 모형 ✅ · `θ(N)` 곡선 ❌(용량만 · 로그 사상) |
| **75** | "Large volume fluctuations of the AM … depleting the electrical contact between the AM and SE particles" 묶음 | **✅ 기구**(부피 변화 → 계면 인장 → 결합 제거 → 활성 면적 ↓) · 입자 0 · 이온 계면(전자 경로 불변) |
| **83** | 산화물 SE 공소결 예시 | **✅**(서론 · 소결 박리 · Ta:LLZO–LCO 공소결 [31]) · 모형은 공소결 뒤 완전 접합에서 시작 · 83호 '다른 자리' 판정 확인 |
| **94** | "delamination of cathode active material and solid electrolyte upon cycling" 2D 첫째 · 94호 가역 법칙과 대비 | **✅**(2D · 사이클 · 비가역 결합 제거 · 정변위 구속) · 둘 다 η 형 결손 |

---

# ★ (b) 접촉 손실의 자리 — `φ`(면적) · 곱 `A_f · i₀` · η 형 (곱 축퇴 · R1 · R7)

## 1. 모형 안의 경로 (`[인쇄]`)

SOC 변화 → (S4) 화학 변형 → 격자 스프링 응력(정변위 구속) → 계면 요소 Ψ > Ψ_t 면 제거 → 남은 계면만 BV 전류 → (식 1) R_ct = (A₀/A_f)·RT/(i₀F). 역방향 결합 둘: (S1)(S3) 응력 항(전류 분포) · 전류 집중(GB) — 둘 다 박리 크기를 거의 안 바꾼다고 인쇄(그림 2(d) · S4).

## 2. ★★★★ 곱 (`[재현·대수]`)

- 남은 면에 전류가 고르면 총전류 I = A_f · i₀ · g(η) → **η 는 I/(A_f·i₀) 하나에만 매달린다**(대칭 BV · Δμ 무시). 방전 곡선에서 박리 분율 d 와 i₀ 의 (1 − d) 배 감소는 **같은 곡선**을 낸다 — 이 편은 두 손잡이를 **구성으로만** 가른다(d 는 역학이 계산 · i₀ 는 입력 — 그림 S4 가 i₀ 를 바꿔도 d 가 그대로임을 보인다).
- 카드의 곱 `A_eff · k`(37호)와 같은 자리 — 접촉 손실 ≡ 계면 화학 열화(출력 수준). `LAM_PE`(용량 스케일) · `θ_AM`(통째 고립)은 이 모형에 자리가 없다(평면 판 하나 · D 1×10⁻¹⁴ · 100 nm → L²/D 1.0 s ≪ 방전 ≈300 s `[재현]`).

## 3. ★★★★ η 형인데 율에 둔하다 — Tafel (`[재현·대수]` · `[재현·가정]`)

| 조건 | i/i₀ | 박리 d(`[도표·화소]`) | Δη 정확(BV) | Tafel ln 꼴 | 감쇠(`[도표·화소]`) |
|---|---|---|---|---|---|
| NMC 1 A m⁻² | 5 | 0.820 | **86.8 mV** | 88.7 | 16.97 |
| NMC 3 | 15 | 0.614 | 49.0 | 49.2 | 17.10 |
| NMC 5 | 25 | 0.658 | 55.4 | 55.5 | 17.80 |
| NMC 7 | 35 | 0.574 | 44.1 | 44.1 | 19.28 |
| LCO 1 | 0.5 | 0.468 | 10.7 | (선형 11.4) | 2.97 |
| LCO 7 | 3.5 | 0.563 | 39.8 | (선형 116.6) | 8.64 |

- NMC 의 박리 몫은 분율이 정하고 전류는 거의 안 정한다 — 인쇄 설명 "η_intf = i_app·R_intf"(선형 — 같은 분율이면 ×7)는 이 편 동역학 영역과 맞지 않는다(D26). 감쇠가 ×1.14 로만 오르는 것과 같은 방향.
- ⇒ **율 스윕이 면적형 접촉 손실을 '율 의존 결손' 으로 드러내려면 선형 영역(i ≪ i₀·A_f/A₀)까지 내려가야 한다**: NMC d 0.82 면 0.036 A m⁻² — `[재현·가정]`(100 nm · 172 mAh g⁻¹ · ρ 4.75 g cm⁻³ `[외부 값]` → 1 A m⁻² ≈12.2 C) ≈0.44 C 상당 · C/10(0.0082 A m⁻²)이면 같은 박리의 Δη ≈4.8 mV. Tafel 영역 안의 율 쓸기(1–7 A m⁻²)에서는 율 무관 결손(물질 손실)처럼 보인다(`[해석]` — 곱 축퇴 처방 '율 스윕' 줄 · 압력 연산자 '율 먼저' 의 조건).

## 4. 판정

접촉 손실 ↔ `LAM_PE` 는 이 모형에서 **별개 손잡이가 아니다** — `LAM_PE` 가 없고, 접촉 손실은 곱 `A_f · i₀` 의 한쪽으로만 출력에 들어간다. 갈림은 **구성(역학이 d 를 계산)**과 **동역학 영역(선형에서만 율 의존)** 두 곳에서만 일어난다.

---

# ★ (c) '실험 비교' 그림 5 — 자료 경로 · 보정 · 무엇이 맞았나

## 1. 자료 경로 (`[인쇄]`)

본문 [17] = SI [23] Wang D.W. … Sun X.L. 2019 *ACS AMI* 11, 4954 — 그림 5 의 실험 점("extracted from Wang et al.") · R_ct 증가 "approximately 1600 Ω"(본문 p. 5532) · "600 Ω-cm²"(서론 p. 5528) · SI 의 NMC/LLZO R_ct "around 2500 Ω−cm²"(i₀ 보정) — **같은 출처에서 세 수 · 두 단위**(D6). 디지타이즈 방법 · 면적 · 전압 → x 환산 0(G6).

## 2. 보정과 비교가 같은 자료다 (`[재현]`)

- i₀ = RT/(R_ct F) — 2500 Ω cm²(= 0.25 Ω m²) · T 300 K → **0.1034 A m⁻²** ↔ 인쇄 0.2(×1.934) · LCO 250 → 1.034 ↔ 2.0(×1.934). k_ref 는 "scaled accordingly to provide desired values of i₀".
- 모형의 박리 전 R_ct = RT/(F·0.2) = **1293 Ω cm²** ↔ 그림 5 모형 충전선 중간 x 1337–1455 ✅(모형은 인쇄 i₀ 로 계산됨) ↔ Wang 의 2500 · 그림 5 실험 충전 점 2247 · 2424 — **모형 출발점이 보정 출처의 ≈0.55 배**.
- ⇒ 그림 5 에서 모형이 예측한 것은 **비 A₀/A_f 와 i₀(x) 모양**이고, 절대 크기는 같은 실험의 R_ct 로 맞춘 i₀(×1.93 산술 차 포함)다.

## 3. 무엇이 맞고 무엇이 안 맞나 (`[도표·화소]` → `[해석]`)

- 맞는 것: x > 0.9 의 급상승 — 모형 두 선 · 실험 두 무리 모두 2700–7100 Ω cm² 로 오른다. 모형에서 이것은 i₀(x) ∝ √((c_max − c)·c) 의 x → 1 발산(충전 첫머리 박리 전 x 0.98 에서도 ≈5000)이다 — **SOC 축 신품 j₀(x) 기준선**(§3-b (루))이 '일치' 의 대부분을 낸다.
- 안 맞는 것: 이 편 기구의 서명인 **방전/충전 비** — 모형 2.16–2.60(충전 끝 박리 뒤 방전 내내 면적이 작음) ↔ 실험 x 0.52 · 0.59 에서 **0.92 · 0.87**(방전이 더 낮음) · 0.81 에서 1.17. 실험 자료는 중간 SOC 에서 '충전 중 박리 → 방전 R_ct 상승' 을 보이지 않는다.
- 판정: "compares very well" 은 **증명 그림이 아니다** — 출발 크기는 보정 · 급상승은 i₀(x) 기준선 · 기구 서명(비)은 어긋남(§3-b (햐) · (텨) · (루)).

---

# ★ (d) 같은 조건 그림 사이 산포 — 한 실현 · 문턱 확률성

| 기준 조건 | 그림 | 값(`[도표·화소]` · `[도표]`) |
|---|---|---|
| NMC · 150 nm · 1 A m⁻² · 3.2–4.5 V · i₀ 0.2 — 첫 사이클 감쇠 | 8(a) · S4(a) ↔ 6(c) · 6(a) · 3(3.2 V 지점) | **16.97 · ≈17.0** ↔ **11.50 · ≈11.7 · 11.7** mAh g⁻¹ |
| LCO · 150 nm · 1 A m⁻² · 3.2–4.1 V · i₀ 2.0 — 첫 사이클 감쇠 | 8(b) · S4(b) · 4 · 6(c) · 6(b) | **2.97 · ≈4.9 · ≈5.8 · 6.35 · ≈10.8**(6(b) 끝 109.2 ↔ 그림 4 무파괴 ≈120) |
| LCO · 150 nm — 첫 사이클 박리 분율 | 8(b) ↔ S4(b) | **0.468** ↔ **≈0.78** |
| NMC · 150 nm · 4.5 V — 첫 충전 박리 | 8(a) · S4(a) · S5(b) · S6(c) · S6(a) | 0.820 · ≈0.82 · ≈0.82 · ≈0.85 · "∼70%" |
| NMC · 40 · 75 nm — 첫 충전 박리(기준 경우) | S5(b) 자유 ↔ S6(c) 공극 0 | **0.21 · 0.43** ↔ **0.11 · 0.25** |

- 주장된 효과 크기와 견주면: NMC 전류 효과 +2.31(1 → 7 A m⁻²) < 같은 조건 두 무리 차 5.47 · S5 '경계 효과 없음'(차 ≤0.09) < 같은 기준 경우 두 그림 차(0.10–0.18) · LCO 그림 6(b) ↔ 6(c) 는 한 그림 안에서도 안 맞는다(D4).
- `[인쇄]` 산포의 설명은 "randomness of the fracture threshold" 하나 · 분포 · 실현 수 · 반복 0 · "No statistically significant difference" 는 통계 0 위에 선다(G2).
- `[해석]` 결론의 방향(작은 입도 · 낮은 상한 · 연한 SE 가 유리)은 산포보다 큰 축(입도 150 → 40 nm 에서 11.5 → ≈0.4)에서는 서지만, 전류 · 경계 조건 · 나노 공극 25 % 같은 작은 효과의 판정은 한 실현으로 정해지지 않는다.

---

# ★ (e) 인쇄 식 · 표 재풀이 (`[재현]` · `[재현·대수]`)

## 1. (C5) · (C7) — 정상 상태 확산과 집전체 Li 유속

(C5) ∇·(D∇c) = 0 은 시간 항이 없다. (C6) 계면 유속 i_BV/F · (C7) x = L_x(집전체) 유속 I_app/F — 정상 상태에서 두 유속은 같아야 하고(∮ = 0) 양극 Li 총량은 변하지 않는다. 글자 그대로면 충 · 방전이 SOC 를 못 바꾼다 → 그림 3 · 4 · 6 · 9 의 SOC 쓸기와 양립 불가. 실제 구현은 ∂c/∂t 를 넣고 집전체 Li 유속을 0 으로 뒀을 것(`[해석]` — 인쇄 0 · G8). 행 이름 "Li/SSE interface" · "at the top of SSE"(C10 은 좌우 경계)는 같은 연구실 Li 금속 | LLZO 모형([47] · [59])의 표 틀로 읽힌다.

## 2. (S5) ≠ 그림 맞춤선 · (S4) 의 꼴

| y = c_s/c_s,max | (S5) 인쇄 | 그림 S2(a) · 10(a) `[도표]` | (S6) 인쇄 | 그림 S2(b) `[도표]` |
|---|---|---|---|---|
| 0.20 | 10.91 | — | 23.28 | ≈21 |
| 0.26 | 7.04 | ≈15.5 | — | — |
| 0.30 | 5.12 | ≈11 | — | — |
| 0.40 | 2.11 | ≈4.5 | — | — |
| 0.50 | 0.89 | ≈2.8 | 1.89 | ≈1.5 |
| 0.75 | 1.13 | ≈1.7 | −4.15 | ≈−4.3 |
| 1.00 | 2.40 | ≈2.0 | 0.51 | ≈0 |

(S5) 최소 0.674 @y 0.580 · 그림은 ≈1.7 @≈0.75 — 인쇄 다항식은 그림의 'Polynomial fit' 이 아니다(D12). (S4) ε = (1/3)V̄(c)·c(in c_s,max × 10⁻⁶ 단위 — c_s,max 미인쇄): 인쇄 꼴 NMC y 1.0 · 0.70 · 0.559 · 0.45 · 0.348 → **0.801 · 0.220 · 0.128 · 0.200 · 0.39**(비단조 — 0.559 아래에서 다시 커짐 = 충전 끝 팽창) · 적분꼴 (1/3)∫₀^y V̄ dy → 2.068 · 1.909 · 1.87 · 1.841 · 1.765(단조 수축 ✅). LCO 인쇄 꼴 y 0.53 → 0.796 → 1.0: 0.107 → **−1.087** → +0.170(방전 끝 팽창) · 적분꼴 3.42 → 3.17 → 3.01(단조 수축 ✅). ⇒ 인쇄 (S4)+(S5)+(S6) 그대로는 본문 서사와 반대 부호 구간이 생긴다 — 구현은 적분꼴이거나 V̄ 상수였을 것(`[해석]` — 인쇄 0).

`[재현]` 창 안 부피 변화(적분 · c_s,max 단위): NMC y 1 → 0.348 ∫V̄dy = 0.908 · 1 → 0.31 1.061 · 1 → 0.468 0.660 cm³ mol⁻¹ — 인쇄 (S5) 로는 4.1 V 창이 4.4 V 창 부피 변화의 **73 %**(그림 맞춤선이면 낮은 x 몫이 커서 더 작아짐 `[해석]`) · LCO y 0.53 → 0.988 −1.224.

## 3. (S7) · (S8) — 창 ↔ x

`[재현]` U_NMC: 4.5 V ↔ x **0.3162** · 4.4 V ↔ **0.3482** · 4.1 V ↔ **0.4683** · 3.2 V ↔ 0.9915 · U_NMC(0.30) 4.554 · (0.309) 4.52 · (0.45) 4.139. U_LCO: 4.1 V ↔ x 0.534 · 3.8 V ↔ **0.963** · 3.2 V ↔ 0.988 · U_LCO(0.7) **3.933** · (0.766) 3.911 · (0.9) 3.897. ⇒ 본문 "3.2−4.4 V … from 1.0 to 0.3" 와 그림 10(a) 빨간 선(x 0.309)은 (S7) 로 4.5 V 쪽 · 4.4 V 면 0.348(그 x 의 V̄ 는 그림으로 ≈7 — 0.31 의 ≈10.5 보다 작다) · 응력 항 Δμ 가 평형을 옮기면 달라질 수 있다(인쇄 0 · D13) · "At a Li stoichiometry of around 0.7, the open-circuit potential (OCP) of LCO is around 3.8 V" ↔ (S8) 3.93 V(D14).

## 4. 동역학 · 옴 (`[재현]`)

i₀ ↔ R_ct ×1.934(§(c) 2). LLZO 옴(200 nm · 표 S-II κ 그대로): GI 0.01818 Ω m² = **182 Ω cm²**(1 A m⁻² 18.2 mV · 7 A m⁻² 127 mV) · GB 전부면 500 Ω cm²(50 · 350 mV) ↔ NMC R_ct 1293 · **LCO R_ct 129 Ω cm²** — LCO 에서는 SE 옴이 전하이동보다 크다(D25). 계면 전류 평균 0.866(그림 2(b) 해석 — 위).

---

# ★ (f) 다중 규모 — 무엇이 원자 계산에서 왔나 (`[인쇄]` → `[해석]`)

| 입력 | 값 | 출처 층위 |
|---|---|---|
| 계면 파괴 문턱 Ψ̄_Cath/LLZO | 2.0 J m⁻² | **DFT 이 편** — NMC622 (101̄0) \| LLZO (100) · 811 (101̄4) 2.4 는 버림 · LCO 계산 0 |
| LLZO 파괴 문턱 | 5.3 J m⁻² | 같은 연구실 앞 편 [1](SI) = Barai 2020 *JES* 167, 100537 |
| GB 성질 κ · Y · ν · Li 농도 | 0.4×10⁻⁵ S m⁻¹ · 120 GPa · 0.2 | [1, 20, 21] = Barai 2020 · Yu & Siegel 2017 · 2018(원자 계산 문헌) |
| GI 성질 | 1.1×10⁻⁵ S m⁻¹ · 141 GPa · 0.2 | 같음 |
| 양극 Y · ν | 120 GPa · 0.3 | [31–34] Qi 2014 · Sun & Zhao 2017 · Xu 2016 · Zhao 2010 — NMC · LCO 공통 |
| V̄(x) | (S5)(S6) | [27] Koerver 2018(= 97호) 디지타이즈 + 다항식(인쇄 ≠ 그림 — D12) |
| i₀ | 0.2 · 2.0 A m⁻² | 측정 R_ct([23] Wang 2019 · [24] Ohta 2012)의 RT/(R_ct F)(×1.93) |
| D · γ | 1×10⁻¹⁴ m² s⁻¹ · 1 S m⁻¹ | [47](SI) Awarke 2013 · [51] Wu 2012(액체셀 문헌) |
| OCP | (S7)(S8) | [18] Guo 2011 · [47] Awarke 2013(액체셀 모형 문헌) |
| thk · GB 두께 · 입도 | 1 cm · 10 nm · 40–150 nm | 가정 · [47][63](나노결정 Ni) · 생성 미세구조 |

`[해석]` '다중 규모' 의 새 고리는 **DFT 계면 파괴 에너지 한 수**다 — 그 수가 결론의 경계(상 지도 · 입도 효과)를 정하고(문턱 근처 확률 파괴 — 판정 6), 응집 · 연화 · 피로 없이 '문턱 넘으면 제거' 로만 쓰인다. LCO 는 그 수를 NMC622 에서 빌린다.

---

# (g) Q1–Q8 — 채움표 칸 (닻 카드 수집 지침)

| Q | 칸 | 이 편 |
|---|---|---|
| Q1 정량 | **층 하나 — `θ(N)` 0/105** | 모형 출력 '분율 계면 박리'(끊긴 계면 격자 요소 비율 · 면적형 `φ`) — **N = 1 값만**(NMC 150 nm 4.5 V 0.57–0.86 · LCO 0.47–0.78 · 입도 40 nm ≈0.11–0.21) · 10 사이클은 용량만(계단 + 멈춤 · LCO 큰 입자 −30.4 %) · 측정 0 · 저자 스스로 "it is not possible to directly compare the extent of delamination … with experimental observations" · 용량 ↔ 면적 로그 사상(Tafel) |
| Q2 분리 관측 | **없다** | 모형 · 실험 대조 = Wang 2019 R_ct 디지타이즈 하나(출발값 보정에도 씀) · EIS 시뮬 · 전압 이완 · 단면 0 · 박리 분율은 모형 안에서만 보임 |
| Q3 라벨 층위 | 칸 없음 · **층 하나: "DFT 한 수(2.0 J m⁻² — NMC622 계면 · LCO 에도) + 같은 연구실 앞 편 · 원자 계산 문헌 GB 성질 + 측정 R_ct 의 ×1.93 i₀ 보정 + 인쇄 ≠ 그림 다항식(S5) + 정상 상태로 인쇄된 확산 식(C5 · C7) · 같은 조건 그림 사이 산포(NMC 11.5 ↔ 17.0 · LCO 2.97–6.35 · 박리 0.468 ↔ ≈0.78) · 한 실현 · 문턱 분포 미인쇄"** |
| Q4 유일성 | **해당 없음 — `assb` 0/105 · 아흔일곱 번째 성질** | **"다중 규모 forward 모형 — 원인(박리)을 구성으로 아는데 관측 쪽 식별성은 묻지 않고, 출력에서 박리 분율은 i₀ 와 곱(A_f·i₀ — 식 1)으로만 보이며, 같은 입력의 그림 사이 산포(한 실현 · 확률 문턱)가 전류 · 경계 효과보다 크다"** · `identif*` · `sensitiv*` · `uncertain*` 0 · 누적 0.5 그대로 |
| Q5 Li-In | **해당 없음** | 음극 0(φ_LLZO\|x=0 = 0 · 전위 기준은 양극 OCP 함수) · `indium` 0 |
| Q6 압력 | **해당 없음 · 층 하나** | `pressur*` · `MPa` · `stack` 0 · 역학 구속 = x 양끝 u_x 0(정변위 · 무한 강성 — 인장 박리 발생원) · y 경계만 쓸기(S5) |
| Q7 Li 재고 | **해당 없음** | 음극 0 · Li 재고 변수 0 · 박리는 Li 를 가두지 않음(평면 판 · 고립 0) |
| Q8 OCP · 평형 곡선 | **층 하나** | (S7) U_NMC · (S8) U_LCO = 액체셀 모형 문헌 함수([18] · [47]) · NMC 조성 셋(DFT 622 · 811 ↔ 표지 111 ↔ V̄ 자료 622 끝점 근사) · `[재현]` 4.4 V ↔ x 0.348(본문 0.3) · U_LCO(0.7) 3.93(본문 3.8) · OCV 측정 0 |

**누적 ≈20.0 → ≈20.0 (새 칸 0).**

---

# 재현 (`[재현]` — 인쇄 수치 · 식 · 래스터 화소로 우리가 계산 · 가정 표시 · 스크립트는 `scratchpad/p105/` 에만)

| # | 대상 | 방법 | 결과 |
|---|---|---|---|
| R1 | i₀ ← R_ct | RT/(R_ct F) · T 300 K(RT/F 0.025851 V) | 2500 Ω cm² → **0.1034** · 250 → **1.034 A m⁻²** ↔ 인쇄 0.2 · 2.0(×1.934) · 인쇄 i₀ → R_ct 1293 · 129 Ω cm² |
| R2 | 그림 5 모형 ↔ 실험 | 화소(755 px/x · 59.33 px/1000) | 모형 충전 1337–1455(x 0.50–0.75) · 방전 2921–3528 · 비 2.16–2.42 ↔ 실험 충전 2247 · 2424 · 2575 · 방전 2078 · 2103 · 2205 · 3022 · 비 0.92 · 0.87 · 1.17 |
| R3 | BV 박리 몫 | 대칭 BV · 남은 면 균일 | NMC Δη 86.8 · 49.0 · 55.4 · 44.1 mV(Tafel ln 꼴 88.7 · 49.2 · 55.5 · 44.1) · LCO 10.7 · 38.7 · 30.0 · 39.8 · S4(a) i₀ 0.2 · 2.0 · 3.0 · 5.25 → 86.8 · 39.4 · 23.7 · 15.9 mV |
| R4 | C-rate 환산 | `[재현·가정]` 100 nm · ρ 4.75 `[외부 값]` | 172 mAh g⁻¹ → 294 C m⁻²(8.2 µAh cm⁻²) → 1 A m⁻² = 12.2 C(ρ 5.05 면 11.5 C) · 140 → 15.0 C · 120 → 17.5 C · C/10 = 0.0082 A m⁻² → Δη(d 0.82) 4.8 mV |
| R5 | 확산 시간 | L²/D · D 10⁻¹⁴ | 100 nm 1.0 s · 10 nm 0.01 s · 260 nm 6.8 s ≪ 방전 ≈300 s |
| R6 | LLZO 옴 | 200 nm/κ | GI 182 Ω cm²(18.2 · 127 mV @1 · 7 A m⁻²) · GB 500 Ω cm²(50 · 350 mV) |
| R7 | (S5) ↔ 그림 | 다항식 계산 | y 0.26 · 0.30 · 0.40 · 0.50 · 0.75 · 1.0 → 7.04 · 5.12 · 2.11 · 0.89 · 1.13 · 2.40 ↔ 그림 ≈15.5 · ≈11 · ≈4.5 · ≈2.8 · ≈1.7 · ≈2.0 · 최소 0.674 @0.580 |
| R8 | (S6) | 다항식 | 꼭지 y 0.7662 · −4.174 · 근 0.5454 · 0.9869 · y 0.2 23.28 · 1.0 0.509 |
| R9 | (S4) 꼴 | 인쇄 V̄(c)c/3 ↔ ∫V̄dc/3 | NMC 인쇄 최소 @0.559(비단조) · 적분 단조 · LCO 인쇄 최소 @0.796 · 적분 단조 · ∫ 창 NMC 0.908(4.4) · 1.061(4.5) · 0.660(4.1) · LCO −1.224 cm³ mol⁻¹ |
| R10 | (S7)(S8) 창 | 이분법 | 4.5 · 4.4 · 4.1 · 3.2 V ↔ x 0.3162 · 0.3482 · 0.4683 · 0.9915 · LCO 4.1 · 3.8 · 3.2 V ↔ 0.534 · 0.963 · 0.988 · U_LCO(0.7) 3.933 V |
| R11 | 그림 10(a) 세로선 | 화소(470 px/x) | 빨강 x 0.309(= (S7) 4.52 V) · 녹 0.464(= 4.11 V) |
| R12 | 격자 기하 | 60 × 5 nm × sin 60° | 259.8 nm(그림 3 y 축 ≈260 ✅) · 계면 결합 ≈60–120(하나 ≈0.8–1.7 % — 분율 넷이 1/120 배수 ±0.002 안: 79 · 69 · 56 · 75/120) · 계면 전류 정규화 0.866(그림 2(b) ≈0.85) |
| R13 | 그림 9 · 10(b) 기울기 | 화소 표 | 4.4 V NMC 1.31 · 0.99 · 0.45 · 0.21 · LCO 3.86 · 1.38 · 0.46 · 0.14 · 4.1 V NMC ≈0.47 · ≈0.43 · ≈0.10 · 비 2.8 · 2.4 · 4.5 mAh g⁻¹ cycle⁻¹ |
| R14 | 로그 사상 | Tafel | A_f/A₀ 0.18 → 0.09: Δη 88.7 → 124.5 mV(+36 mV) |
| R15 | 같은 조건 산포 | 화소 · 눈 | NMC 감쇠 16.97 · ≈17.0 ↔ 11.50 · 11.7 · LCO 2.97 · 4.9 · 5.8 · 6.35 · ≈10.8 · LCO 박리 0.468 ↔ ≈0.78 |
| R16 | 그림 6(b) ↔ (c) | 화소 | (b) 끝 109.2 · 112.1 · 119.4 · 120.3 → 아주 작은 기준 차 11.1 · 8.2 · 0.9 ↔ (c) 6.35 · 1.49 · 0.98(−0.69 기준) |
| R17 | 상 지도 Y_Li | `[재현·외부 값]` 141 GPa ÷ 14.5 | 9.7 GPa(값 미인쇄) |
| R18 | 일정 | 인쇄 | 접수 → 출판 215 일 · 수정 → 출판 63 일 |

---

# 어휘 집계 (NFKC · 줄 이음 뒤 · 쪽 머리 · 바닥 각인 제외 · 본문 = 제목 → 사사 · 캡션 포함 \| 본문 참고문헌 \|\| SI 본문(표 · 캡션 포함) \| SI 참고문헌)

`delaminat*` 167 \| 0 \|\| 57 \| 1 · `detach*` 20 \| 0 \|\| 3 \| 0 · `cycl*` 48 \| 2 \|\| 4 \| 1 · **`saturat*` 0 \| 0 \|\| 0 \| 0** · `irreversib*` · `reversib*` 0 · `pressur*` 0 \|\| 1(부호 규약) · `MPa` · `stack` 0 · `experiment*` 15 \| 1 \|\| 2 \| 1 · `validat*` · `agree*` 0 · **`identif*` 0 · `sensitiv*` 0(참고문헌 [63] 제목 1) · `uncertain*` 0** · `error` 3(그림 11 '오차 막대' — 부분 몰부피 범위) · `fit*` 0 \|\| 2(U 맞춤 · 다항식) · `calibrat*` 0 · `estimat*` 9 \|\| 7 · `statistic*` 0 \|\| 1("No statistically significant") · `random*` 1("randomness of the fracture threshold") \|\| 3(공극) · `isolat*` 0 · `LAM` · 'active material loss' · `inventor*` 0 · `contact` 8 · `impedance` 11 · `EIS` · `OCV` 0 · `OCP` 1 · `open-circuit` 1 \|\| 3 · `particle` 21 \|\| 16 · `composite` 2 · `relax*` 1 \|\| 3 · `recover*` · `heal*` 0 · `first time` 1.

---

# 참고문헌 74 번호 (+ SI 51) — 우리 축에 닿는 것 (번호는 PDF p. 5539–5541 · SI p. 14–17 목록에서 직접 확인 · 빠진 번호 0)

| 번호 | 서지(`[인쇄]`) | 이 편에서의 쓰임 | 우리 축 · 위키 |
|---|---|---|---|
| [2] (SI 29) | Famprikis T., Canepa P., Dawson J.A., Islam M.S., Masquelier C. *Nat. Mater.* 18, 1278(2019) | 그림 1(a) 재수록 · 박리 정의 | ☆ 행 0 |
| [16] | Koerver R., Aygun I., … Janek J. *Chem. Mater.* 29, 5574(2017) | 사이클 박리 보고 · 'NMC/sulfide 에서도 박리' | **= 23호**(큐 22) — 교차 |
| [17] (SI 23) | Wang D.W., Sun Q., Luo J., Liang J.N., Sun Y.P., Li R.Y., Adair K., Zhang L., Yang R., Lu S.G., Huang H., Sun X.L. *ACS Appl. Mater. Interfaces* 11, 4954−4961(2019) | **그림 5 실험 점 · R_ct 2500 Ω cm² → i₀ 보정 · '600 Ω-cm²' · '1600 Ω' · 작은 양극 입자** | **원장 행 0 → 새 행 ★★★** |
| [19] | Zhang W.B., Weber D.A., … Janek J. *ACS AMI* 9, 17835(2017) | LNTO 계면층 '100 사이클' | **= 63호** — 교차 |
| [21] | Hamann T., … Wachsman E. *Adv. Funct. Mater.* 30, 1910362(2020) | 복합 양극 활성 면적 서론 목록 | 원장 L465(54 = 1) · ☆(서론 목록) |
| [22] | Shi T., … Ceder G. *Adv. Energy Mater.* 10, 1902881(2020) | 같은 목록 | **= 77호** — 교차 |
| [23] | Han F.D., Yue J., Chen C., Zhao N., Fan X.L., Ma Z.H., Gao T., Wang F., Guo X.X., Wang C.S. *Joule* 2, 497−508(2018) | LBCO 계면층 LCO/LLZO '100 cycles … without any significant capacity fade' | 원장 행 0 → **새 행 ★**(모형 'LCO/LLZO 심한 박리' 의 실험 반대편) |
| [25] (SI 24) | Ohta S., Kobayashi T., Seki J., Asaoka T. *J. Power Sources* 202, 332−335(2012) | **LCO/LLZO R_ct 250 Ω cm² → i₀ 2.0** | 원장 행 0 → **새 행 ★** |
| [31] | Tsai C.L., Ma Q.L., … Guillon O. *Sustainable Energy Fuels* 3, 280−291(2019) | Ta:LLZO–LCO 1050 °C 공소결 상호확산 없음 | 원장 L468(53 = 1) · **재지목 → 2** |
| [35] | Walther F., Koerver R., Fuchs T., Ohno S., Sann J., Rohnke M., Zeier W.G., Janek J. *Chem. Mater.* 31, 3745−3755(2019) | **"reported delamination … during charge/discharge"** · 수축 → 인장 | 원장 L185(4) · **재지목 → 5**(ToF-SIMS 분해 계면층 편을 박리 보고로 인용 — 확인처) |
| [36] (SI 27) | Koerver R., Zhang W.B., de Biasi L., … Janek J. *Energy Environ. Sci.* 11, 2142(2018) | 부분 몰부피 · 그림 10(a) · S2 자료 | **= 97호** — 교차 |
| [37] (SI 12) | Bucci G., Swamy T., Chiang Y.-M., Carter W.C. *J. Mater. Chem. A* 5, 19422(2017) | 앞선 이론(부피 변형 · 양극 강성 · 계면 파괴) | 원장 L460(Bucci 2) · **재지목 → 3** |
| [38] (SI 28) | Bucci G., Talamini B., Balakrishna A.R., Chiang Y.M., Carter W.C. *Phys. Rev. Mater.* 2, 105407(2018) | 같음 · 박리 기구 문헌 | 원장 L470(Bucci 2018 1) · **재지목 → 2** |
| [39] (SI 35) | Hao F., Mukherjee P.P. *J. Electrochem. Soc.* 165, A1857(2018) | 같음 | 원장 L124(75 = 1) · **재지목 → 2** |
| [43] | Tian H.-K., Chakraborty A., Talin A.A., Eisenlohr P., Qi Y. *JES* 167, 090541(2020) | 박리 기구 문헌 · 가장자리 박리 | 원장 L302(103 = 1) · **재지목 → 2** |
| [44] | Tian H.-K., Qi Y. *JES* 164, E3512(2017) | "none of them studied the time evolution of the detachment" 의 앞선 편 | 원장 L173(8) · **재지목 → 9** · 5차 묶음 #2 |
| [45] (SI 31) | Qi Y., Hector L.G., James C., Kim K.J. *JES* 161, F3010(2014) | 양극 Y · ν | 원장 L360(97 = 1) · **재지목 → 2** |
| [47] (SI 11) | Barai P., Higa K., Ngo A.T., Curtiss L.A., Srinivasan V. *JES* 166, A1752−A1762(2019) | **격자 스프링 · 전류 집중 · 입계 파괴 방법 원전** · GB 10 nm · 부호 규약 | 원장 행 0 → **새 행 ★★** |
| [52] · [53] (SI 20 · 21) | Yu S., Siegel D.J. *Chem. Mater.* 29, 9639(2017) · *ACS AMI* 10, 38151(2018) | GB Li 농도 · **GB 연화(Y_GB)** — 입도 효과의 기둥 | 원장 행 0 → **새 행 ★**(묶음) |
| [56] (SI 14) | Barai P., Mukherjee P.P. *JES* 160, A955(2013) | 확률 손상 · 화학 변형 (S4) | ☆ |
| [59] (SI 1) | Barai P., Ngo A., Narayanan B., Higa K., Curtiss L.A., Srinivasan V. *JES* 167, 100537(2020) | **LLZO GI · GB 성질 · 파괴 5.3 J m⁻²** · 표면 에너지 | 원장 행 0 → **새 행 ★★** |
| [5] · [61] (SI 17 · 16) | Monroe C., Newman J. *JES* 152, A396(2005) · 151, A880(2004) | 응력–동역학 결합 (S1) | 원장 L362(2005 · 2) · **재지목 → 3**(2004 는 ☆) |
| [63] | Schwaiger R., Moser B., Dao M., Chollacoop N., Suresh S. *Acta Mater.* 51, 5159(2003) | **LLZO GB 두께 10 nm 의 근거**(나노결정 니켈) | ☆ — G13 |
| [65] (SI 48) | Zhu J., Chen G. *J. Mater. Chem. A* 7, 5463(2019) | NMC 창 | ☆ |
| [66] (SI 22) | Rahn C.D., Wang C.-Y. *Battery Systems Engineering*(2013) pp. 23−48 | 식 (1) · i₀ = RT/(R_ct F) | ☆ |
| [68] | Sharafi A., Haslam C.G., Kerns R.D., Wolfenstine J., Sakamoto J. *J. Mater. Chem. A* 5, 21491−21504(2017) | **LLZO 파괴 인성이 입도와 무관하거나 작은 입도에서 커짐** — 입도 처방의 실험 근거 | 원장 행 0 → **새 행 ★** |
| [69] · [70] | Haruyama J., Sodeyama K., Han L., Takada K., Tateyama Y. *Chem. Mater.* 26, 4248(2014) · Okuno Y., Haruyama J., Tateyama Y. *ACS AEM* 3, 11061(2020) | **황화물 계면 파괴 에너지 ≈0.8 J m⁻²**(상 지도 아래 경계) | Haruyama 원장 L202(2) · **재지목 → 3** · Okuno ☆ |
| [71] | Deng Z., Wang Z., Chu I.-H., Luo J., Ong S.P. *JES* 163, A67(2016) | 황화물 Y = Li 의 2–3 배 | 원장 L287(2) · **재지목 → 3** |
| [72] | Lee E., Kwon B.J., Dogan F., Ren Y., Croy J.R., Thackeray M.M. *ACS AEM* 2, 6170(2019) | 영변형 양극 | ☆ |
| [74] (SI 45) | Xie H., Li Y., Goodenough J.B. *Mater. Res. Bull.* 47, 1229(2012) | 20 nm 입방 LLZO 합성 | ☆ |
| SI [15] | Nukala P.K.V.V., Simunovic S., Guddati M.N. *Int. J. Numer. Methods Eng.* 62, 1982−2008(2005) | **손상 누적 알고리즘**(격자 요소 제거 · 문턱 무작위) | 원장 행 0 → **새 행 ★**(N 축 형태를 정하는 규칙의 확인처) |
| SI [18] · [47] | Guo M., Sikha G., White R.E. *JES* 158, S11(2011) · Awarke A., Pischinger S., Ogrzewalla J. *JES* 160, A172(2013) | OCP (S7)(S8) · α · D · γ | ☆ — G14 |
| 나머지 | [1] · [3](Kato 2016 — 원장 L253) · [4] · [6]–[15] · [18](Yu C. 2017 — 원장 L390) · [20] · [24] · [26]–[30] · [32]–[34] · [40]–[42] · [46] · [48]–[51] · [54] · [55] · [57] · [58] · [60] · [62] · [64] · [67] · [73] | 서론 목록 · 방법 · 문헌 값 | ☆ · 행 변화 0 |

⚠ 목록 · 인용 오기: [62] "Single-Particle Model for a Lithium-Ion Cell: Thermal Behavior (vol 158, pg A122, 2011)" = 정오표 S11 · [67] "Li6. 25Al0. 25La3Zr2O12"(띄어 씀) · [73] Sharafi 2017 *Chem. Mater.*('surface chemistry … ultra-low interfacial resistance')를 결론의 "fracture energy … obtained from the lower-length-scale analysis.73" 자리에 인용(내용 무관으로 읽힘 `[해석]`).

**5차 묶음 13 편과의 관계**: 이 편은 **#2 Tian & Qi 2017(= [44])** 하나를 인용한다. 나머지 열하나(Ruess 2020 · Takada 1996 · Neumann 2020 · Zhang W. 2017 *ACS AMI* 35888 · Kasemchainan 2019 · Kim 2017 · Han 2021 · Jung 2020 · Kazemi 2019 · Shao 2022 *Energy* · Wang & Sakamoto 2018) 인용 0(74 + 51 번호 전수 대조 — [19] Zhang W. 2017 은 *ACS AMI* 9, **17835**(63호)이고 #6 의 35888 과 다른 편).

---

# 인용 대조

## 1. 이 편을 지목 · 인용한 우리 digest — 그 쓰임 ↔ 이 편이 실제로 주는 것

| digest | 쓰임(digest 전사) | 이 편 | 판정 |
|---|---|---|---|
| 53호 `ren2023_oxide-ssb-composite-cathode-architecture-perspective` :39 · :72 · :313 | [127] "capacity fade cause[d] by mechanical detachment persists for ten cycles without showing saturation" · `θ(N)` 모델 원전 · G2 '형태 · 수치' | 10 사이클 용량 ✅ · '포화 없이' 0 · 면적 분율 N = 1 | 부분(§(a) 4) |
| 75호 `naik2022_kinetics-vs-transport-ssb-cathode-mesoscale-regime-map` :331–334 | [48] 부피 변화 → 접촉 고갈 묶음 · 75호 모형은 접촉 진화 0 | 기구 ✅ · 평면 판 · 이온 계면 | ✅ 기구 |
| 83호 `jiao2023_electro-chemo-mechanical-se-modulus-conductivity-intergranular-czm` :244 · :530 | [13] 공소결 예시 '[6,13-14]' · 원장 이유와 다른 자리 | 서론 소결 · 공소결 [31] ✅ · 모형은 소결 뒤 시작 | ✅(83호 판정 확인) |
| 94호 `schmidt2024_nitsche-contact-delamination-resolved-ssb-cathode` :266 · :576 · :711 | [20] 2D 'delamination … upon cycling' 첫째 · R8 · 94호 가역 법칙과 대비 | 2D · 비가역 · 10 사이클 · 정변위 | ✅ |

53호 본문에서 [127] 이 실린 문장 · 표 칸은 53호 digest 전사로 대조했다(53호 원 PDF 는 이 세션에서 다시 열지 않음).

## 2. 이 편이 인용한 우리 digest

- **23호** `koerver2017_capacity-fade-interphase-chemomechanical-ncm811-lps` — [16] — "Several researchers have reported delamination at the C/SSE interface during charge/discharge operations.16,17,35" · "Experimentally, interfacial delamination has been observed even for NMC/sulfide systems.16". 23호 판정(원장 §3 — "접촉 손실의 **실험** 원전은 맞지만 **정량** 원전은 아니다(틈 치수 · 분율 · 용량 몫 0)" · 23호 원문 "contact loss should only occur during the initial charge" — R8 계단형 출처)이 이 편 인용에 그대로 걸린다 — 이 편은 23호를 '박리 관찰' 로만 부르고 23호의 '첫 충전에만' 형태는 옮기지 않는다(이 편 모형은 매 사이클 증분).
- **97호** `koerver2018_chemo-mechanical-expansion-molar-volume-ocv-pressure-stress` — [36] / SI [27] — 부분 몰부피 자료. 97호 판정이 옮아온다: ① 97호 V̄m 은 **격자 층위(액체 파우치 operando XRD)** · 층상 산화물 ×≈3 배수 의심(97호 §(a) 3) ② 97호 그림 2(b) 판독 NCM-811 0.30 ≈12.5 · 0.275 ≈16 · NCM-622 ≈15.6 @≈0.265(끝점) — 이 편 NMC 자료 끝(x 0.26 ≈15.5)은 **NCM-622 끝점**에 가깝다(`[해석]` · 97호 digest 판독 대조) ③ 97호 LCO 곡선(0 @≈0.59 · +20 @0.47)과 이 편 그림 S2(b) LCO 자료(0 @≈0.53 · ≈21 @0.20)는 양의 가지 x 위치가 다르다 · 음의 가지(최소 ≈−4.3 @≈0.74–0.75)는 같다(D22).
- **63호** `zhang2017_interfacial-eis-cathode-composition-lco-lgps-assb`(— [19] Zhang W. 2017 *ACS AMI* 17835) — LNTO 계면층 '100 사이클 무감쇠' 예시 하나.
- **77호**(Shi T. 2020 *AEM* — [22]) — 서론 목록 하나.

---

# 곱 축퇴 처방 — 여든여덟 번째 적용 ([[assb-lampe-contact-product-degeneracy]])

## 입력 점검

| 단계 | 요구 | 이 편 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | R_ct 만(식 1) · 이중층 · 축전 0 | ❌ |
| **2단계** (18 · 25호) | + 면적을 아는 대조군 | 모형 안에서 A_f/A₀ 를 계산(박리 분율) — 면적을 아는 판 ✅(모형) · 실험 면적 0 | 부분(모형 안) |
| **3단계-a** (19호) | `Ea` | T 300 K 하나 | ❌ |
| **3단계-b** (19호) | `C` 물리 상한 | — | ❌ |
| **4단계** (20 · 24호) | 시간 영역 | CCCV/CC 만 · 휴지 · 이완 0 | ❌ |
| 율 스윕 · `J^T J` 줄 | — | 모형 율 넷(1 · 3 · 5 · 7 A m⁻²) · i₀ 쓸기 넷(S4) — 박리 그대로 · 감쇠만 움직임 | 부분(모형 안 · Tafel 영역 — 아래 ②) |

### ★ 곱 문장 — 셋 (`[인쇄]` → `[재현·대수]` → `[해석]`)

- ① `[인쇄]` 식 (1) **R_ct = (A₀/A_f)·(R_g T/i₀F)** — 박리는 i₀ 와의 **곱 A_f·i₀** 로만 저항에 들어간다 · `[재현·대수]` 남은 면 전류가 고르면 I = A_f·i₀·g(η) 라 η 는 I/(A_f i₀) 하나에 매달린다 — 방전 곡선에서 박리 d 와 i₀ 의 (1 − d) 배 감소는 같다. 이 편은 둘을 **구성(역학이 d 를 계산)** 으로만 가른다(그림 S4: i₀ 를 26 배 바꿔도 d 0.75–0.82). 카드 곱(`A_eff · k` — 37호)의 forward 실례 · `LAM_PE`(용량 스케일)는 자리 0.
- ② `[재현·대수]` NMC 는 i/i₀ 5–35 의 Tafel 영역 — 박리 몫 Δη ≈ (2RT/F)·ln(A₀/A_f) 는 **전류와 무관한 상수 이동**(1 · 3 · 5 · 7 A m⁻² 에서 86.8 · 49.0 · 55.4 · 44.1 mV — 분율이 정함) ⇒ 처방의 '율 스윕' 줄이 면적형 접촉 손실을 율 의존 결손으로 드러내려면 **i ≪ i₀·A_f/A₀ 의 선형 영역**이 필요하다 — Tafel 영역 안의 율 쓸기에서는 감쇠가 율 무관(×1.14 / 전류 ×7)이라 물질 손실처럼 읽힌다.
- ③ `[해석]` 사이클 축에서는 같은 면적 증분이 ln(A₀/A_f) 를 점점 크게 키운다(A_f 0.18 → 0.09: +36 mV) — **용량 궤적의 계단 · 가속은 박리 궤적의 모양이 아니다**. 곱의 한쪽(A_f)이 시간에 따라 움직이는 표본에서, 출력 궤적만으로는 A_f(N) 와 i₀(N)(계면층 · 상호확산 — 이 편이 뺀 기구)의 몫도 가를 수 없다(이 편 결론 "other mechanisms can lead to impedance growth … interdiffusion" 이 바로 그 짝).

### ⚠ 이것이 곱을 푼 것은 아니다

- 모형 편 · 측정 0 · 한 실현 · 문턱 분포 미인쇄 — 위는 인쇄 식 위 대수 · 래스터 화소 판독이다. 저자 계산의 실제 확산 식(G8) · Δμ 몫(G9)을 정하지 않았다.
- 후보 메모(처방 표로 올리지 않음 · 결정 대기): **"면적형 접촉 손실(`A_eff`)의 율 판별은 선형 영역(i ≪ i₀·A_f/A₀)에서만 — Tafel 영역에서는 박리 몫이 율 무관 상수 이동 (2RT/F)·ln(A₀/A_f) 라 율 스윕이 물질 손실과 가르지 못한다(105호: NMC i/i₀ 5–35 · 감쇠 ×1.14 / 전류 ×7)"**. 새 줄 0.

---

# 합성 truth 요구 R1–R8 대조 ([[assb-synthetic-truth-contact-loss-requirements]])

| ID | 요구 | 이 편 | 판정 |
|---|---|---|---|
| R1 | 용량에 곱해지되 `ε_p` 와 별개인 `θ` | 접촉 손실 = 계면 면적 A_f 하나 · 출력에 i₀ 와 곱으로만 · 용량 스케일 `θ` 0 · `ε_p` 0 | **위반** — `A_eff` 자리(37호 꼴) · 다만 `LAM_PE` 와 같은 파라미터도 아님(`LAM` 자체가 0) |
| R2 | 비연결 입자가 자기 SOC 의 Li 를 붙든다 | 평면 판 하나 · 고립 0 | **해당 없음**(구성상 고립 불가) |
| R3 | 죽은 부피가 전해질이 되지 않는다 | 끊긴 요소는 힘 · 이온 둘 다 0 | ✅(형식 — 입자 규모 죽은 부피 0) |
| R4 | `θ` 에만 반응하는 조작 | 조작 = 입도 · 상한 전압(박리 · 창 둘 다) · i₀(**동역학만 — d 불변**) · 전류 — `θ`-전용 0 | **위반** — 대신 **R4 의 짝(i₀ 전용 조작)** 이 모형 안에 있다(그림 S4) |
| R5 | 면적에 비례하는 이중층 | 축전 항 0 | **위반** |
| R6 | OCV 관측의 이완 시간 | 휴지 · 이완 0 · CV 종료 미인쇄 | **위반** |
| R7 | `φ` 와 `u` 를 별개 변수 | `φ` 만(동적 · 비가역) · `u` ≡ 0(기하) | **위반**(변수 하나) — 94호(`φ` 가역)와 짝: 같은 `φ` 자리의 비가역판 |
| R8 | `θ(N)` 형태를 명시적 가정으로 | 결합 제거 누적(비가역) · 사이클당 하중 = SOC 스윙(차단 전압) · 문턱 확률(분포 미인쇄) · 정변위 구속 · 첫 충전 큰 계단(4.5 V · 150 nm 0.57–0.86) + 사이클별 이산 증분 · `θ(N)` 곡선 인쇄 0 · 용량 궤적 = 계단 + 멈춤(로그 사상) | **후보 하나 — 결합 제거형** · 계단형(23호 '첫 충전만') ↔ 점진형 사이: 첫 충전 큰 계단 + 이산 누적 · 결정 근거로는 부족(곡선 0 · 한 실현) |

`[해석]` 이 편은 R8 의 **셋째 형태 후보**(23호 첫 충전 계단 · 94호 SoC 주기 가역 · 83호 입계 피로 다음 — '비가역 결합 제거 + 확률 문턱')를 주고, R7 의 `φ` 가 사이클 축에서 비가역으로 누적되는 첫 모형판이다. R1 은 이 편에서도 위반 — 계보의 모든 모형이 위반한다는 기존 판정 그대로.

---

# 보류 결정 (가)–(규) — 이 편이 주는 근거 (결정 안 함 · 2026-11-17 사용자 결정: 5차 묶음 13 편 뒤 일괄)

**근거(강)**

- **(랴)** '접촉 손실 → 용량 손실' 모형 결과의 결손 꼴 — η 형 · 면적 `φ` · 고립 0 · 그림 8(박리 고정 · 감쇠 ↑ 전류) · S4(박리 고정 · 감쇠 ↓ i₀) · 휴지 · 저율 계산 0 · NMC Tafel 영역이라 율 무관 꼴(Δη 86.8 → 44.1 mV · 감쇠 ×1.14) — η 형인데 율 스윕에 둔한 판.
- **(먀)** '모형 원전' 지목의 기구 층위 — 53호 '`θ(N)` 모델 원전' ↔ 이 편 기구 = 이온 계면 면적 `φ`(비가역 결합 제거) · N 축 출력 = 용량(분율 0).
- **(냐)** 회고 인용 조건 복원 — 53호 'without showing saturation'(이 편 0 · 곡선 둘 끝 평탄) · 조건(1 A m⁻² ≈12 C 상당 · 한 실현 · 4.4 / 4.1 V · 150 nm) 탈락.
- **(키)** R8 N 축 형태 메모 — 둘째 표본(CAM\|SE 판 · 결합 제거형): 사이클당 하중(SOC 스윙) · 문턱 분포(미인쇄) · 고장 정의(요소 제거)가 형태를 정함 · 용량 궤적 ≠ 면적 궤적(로그).
- **(뇨)** 한 지면 그림들의 매개변수 상태 — NMC 16.97 · ≈17.0 ↔ 11.50 · 11.7 · LCO 2.97 · 4.9 · 5.8 · 6.35 · ≈10.8 · 박리 0.468 ↔ ≈0.78 · 그림 6(b) ↔ 6(c) 한 그림 안 · S5(b) ↔ S6(c) 기준 경우.
- **(셔)** 인쇄 식 ↔ 계산 — (C5) 시간 항 0 + (C7) 집전체 Li 유속(SOC 불변) · (S4) V̄(c)·c 비단조 · (S5) ≠ 그림.
- **(세)** 인쇄 매개변수 표의 재풀이 폐합 — i₀ ×1.93 · 그림 5 모형선 = 인쇄 i₀ ✅ · κ 그대로면 옴 182 Ω cm² > LCO R_ct 129.
- **(여)** 표 값 ↔ 계산 값 · 출처 거슬러 — k_ref 출처 [23] = R_ct 실험 편(속도 상수 아님) · i₀ ×1.93 · Ψ̄ 2.0 = NMC622 값을 LCO 에도 · V̄ 단위 m³ ↔ cm³.
- **(햐)** '계산 ↔ 실험 일치' 의 측정 몫 · 비교 축 — 그림 5: 출발 R_ct = 같은 실험 보정 · 예측은 비 A₀/A_f · i₀(x) 모양 · 기구 서명(방전/충전 비) 어긋남(모형 2.2–2.6 ↔ 실험 0.87–0.92).
- **(텨)** '실험 검증' 그림의 자료 경로 — "extracted from Wang et al." · 면적 정규화 값 · x 환산 0 · 같은 출처 세 수(600 Ω cm² · 1600 Ω · 2500 Ω cm²).
- **(루)** SOC 축 신품 j₀(x) 기준선 — 그림 5 의 x > 0.9 급상승이 모형 i₀(x) ∝ √((c_max − c)c) 의 발산(박리 전 x 0.98 ≈5000)이고 실험 일치의 대부분을 냄.
- **(치)** 모형 결론 옆 배제 가정 — 상호확산 · 계면층 배제(인쇄) · 정변위 구속 · 평면 판 · 300 nm · GB 연화(−15 %) + 문턱 근처 확률 파괴 · LCO 문턱 = NMC622 값 · "applicable to larger cathode particles embedded within thicker LLZO"(계산 0).
- **(탸)** 요약 수치 ↔ 그림 — '0.5−1.0 · 0.1−0.3 mAh/g/cycle' ↔ 0.45–1.31 · 0.10–0.47 · '4×' ↔ 2.4–4.5 · '∼70%' ↔ ≈0.85 · 'LCO 박리 ≥ NMC' ↔ 그림 8 LCO 가 넷 중 셋(1 · 5 · 7 A m⁻²)에서 작음 · "4.4 V … 1.0 to 0.3" ↔ (S7) 0.348.
- **(죠)** 부분 몰부피 입력의 층위 사슬 — 97호 격자 V̄ → 디지타이즈(NCM-622 끝점 근사 · 표지 NMC111) → 다항식 (S5)(인쇄 ≠ 그림) → (S4) 변형(적분꼴 아님) → 격자 스프링.

**근거(중)**

- **(댜)** 모형 '스택 압력' 의 구속 강성 — 압력 0 · x 양끝 u_x 0(정변위 · 무한 강성)이 인장 박리의 발생원 · y 경계만 쓸기.
- **(요)** 모형 응력 성분 · 구속 — 계면 법선(x) 인장 · Δμ 는 요소 변형 에너지 Ψ(축력 부호)로 · σ_h 아님 · 구속은 정변위.
- **(이)** 모형 값 인용 규칙 — 입력 구조(평면 100 nm · 300 nm 영역 · thk 1 cm · GB 10 nm) ≠ 실셀 · 'X mAh g⁻¹ 감쇠' 는 ≈12 C 상당 전류의 값.
- **(대)** C-rate 기준 용량 — 1 A m⁻² ≈12 C 상당(`[재현·가정]`) · "relatively low applied current densities" · C-rate 표기 0.
- **(주)** 'X-limited' — "not limited by the ionic conductivity within the LLZO phase" ↔ 인쇄 κ 로 옴 182–500 Ω cm²(LCO R_ct 129) · 단위 의심.
- **(쵸)** '용량 변화' 의 기구 — 이 편 감쇠는 동역학 결손(η) · 응력 평형 항 Δμ 의 몫은 분리 0(G9).
- **(펴)** 출력에 안 보이는 성분 — 그림 9 감쇠를 "increase in interfacial delamination and subsequent increase in interfacial resistance" 로 배정하면서 둘 다 그리지 않음.
- **(헤)** measure-don't-fit — "adopted from the experimental literature or estimated using lower-length-scale atomistic simulations" ↔ i₀ 는 R_ct 역산 + k_ref "scaled accordingly"(보정 단계).
- **(뎌)** '문헌값 일치' 의 자료 독립성 — 그림 5 의 보정과 비교가 같은 출처(Wang 2019).
- **(체)** 평형 곡선 출처 층위 — (S7)(S8) = 액체셀 모형 문헌 함수 · 어느 출처가 어느 양극인지 0 · 본문 수치와 ±0.05–0.13 V 어긋남.
- **(차)** PyBaMM 면적 / j₀ 노브 분리 forward — 이 편은 두 노브를 입력에서 분리(역학 d · 입력 i₀)하고 출력에서 곱으로 합침(식 1) — forward 분리판의 표본.
- **(무)** j₀(x) 모양 선택지 — α 0.5 의 √ 꼴(PyBaMM 계열과 같음) · 그림 5 의 U 자 R_ct(x) 가 그 꼴의 귀결.
- **(두)** θ 판정의 시간 궤적 조건 — 휴지 · 저율 · CV 방전 0 · η 형이라 그 조건에서 사라질 결손(계산 0).
- **(노)** 양극 부피 변화 층위 — 격자 층위 V̄(97호) 하나 · 입자 층위 0.
- **(퍄)** 유도 열역학량 기준 · 단위 — V̄ 단위(m³ ↔ cm³) · LCO 부호(창 안 일부 양수 x 0.53–0.55) · 그림 11 '범위' 가 창 안 범위와 다름.
- **(겨)** 처방 효과 측정 — 작은 입도 · 낮은 상한 · 영변형 · 연한 SE · 나노 공극 — 전부 모형 · 실험은 나노 LLZO 합성 [74] · 계면층 100 사이클 [19][23] 인용뿐(입도 → 박리 실험 0).
- **(효)** 쓸기 결론의 무차원 폐합 — 입도 · 전류 · i₀ · 상한 쓸기를 L²/D(1 s ≪ 300 s) · i/i₀(5–35 Tafel) · 옴 ↔ 전하이동 비로 거르면 '전류 효과' 해석(선형 R·i)이 영역과 안 맞음.
- **(규)** 백분율 · 비용량 기준 — mAh g⁻¹ 분모(밀도 · c_max) 미인쇄 · '4×' 는 절대 mAh g⁻¹ cycle⁻¹(4.4 · 4.1 V 용량 171 ↔ 140 — 사이클당 % 로는 ×2.3–3.6).
- **(교)** 과전압 성분 이름 — "η_intf = i_app·R_intf"(선형 정의) ↔ 이 편 BV 영역(Tafel)에서 박리 몫은 로그 · 'activation overpotential' 과 'interfacial resistance' 가 한 이름에.

**약**: **(투)** 'Wa 영역 선결' — "not ohmically limited" 를 300 nm 로 정당화 · **(그)** 신품 θ₀ — 완전 접합 출발 · 나노 공극 10 · 25 % 를 초기 결함으로(면적 효과 0) · **(러)** θ → `LAM_PE` 결합 항 — 이 모형은 결합 0(음성 표본) · **(저)** 첫 충전 상한 — CCCV 로 충전 SOC 를 같게 둬 비대칭 검사 불가 · **(에)** 속도 상수 i₀ 환산 — k_ref 단위 인쇄 · c_e · c_max 0 이라 재현 불가 · **(됴)** 닫힌 꼴 '측정 → 매개변수' — i₀ = RT/(R_ct F)(선형 · 균일 계면 조건 · ×1.93) · **(료)** D 1×10⁻¹⁴ 를 NMC · LCO 공통으로 · **(녀)** (S3) 부호 규약(인장 Ψ > 0 → Δμ < 0) · **(쿄)** 결합 항(Δμ)의 관측 꼴 미분리 · **(툐)** 다사이클 상태 — 모형의 사이클별 상태(끊긴 요소)도 인쇄 0 · **(표)** '일치' 지표 0(눈으로 'compares very well') · **(다)** 28호 분모 — ASSB 모형 편 식별성 0 한 점 · **(리)** Tian & Qi 2017 재지목 → 9(5차 묶음 #2) · **(추)** Hao & Mukherjee 2018 재지목 → 2 · **(네)** 유지율 기준 — 사이클 1 기준 절대 기울기 · **(레)** 두 창 비교의 정규화 — 사이클당(전하 처리량 171 ↔ 140 무시). **(마)** 근거 0 · **(라)(바)(사)** 결정 · 반영됨 · 나머지 근거 0 — **결정 안 함**.

## 새 판단 거리 (셋 — §3-b 에 행을 더할지는 호출자 · 사용자 판단: 155 건 일괄 처리 결정 뒤라 추가하지 않았다)

1. **용량 궤적 ↔ 접촉 궤적 사상 표기** ((키) · (랴) 의 N 축판으로 묶어도 됨) — 모형의 '사이클별 용량 감쇠' 를 R8(`θ(N)` 형태) · 카드 Q1 로 옮길 때 그 용량이 접촉 변수에 어떤 사상(선형 · 로그 · 컷오프 기하)으로 매달리는지와 접촉 변수 궤적 자체의 인쇄 여부를 같이 적게 할지 — 105호: 용량만 인쇄 · Tafel 에서 Δη ∝ ln(A₀/A_f)(A_f 0.18 → 0.09: +36 mV).
2. **율 판별의 동역학 영역 조건** ((랴) · (투) 와 묶어도 됨) — '율 의존이면 η 형 · 율 무관이면 물질 손실' 판정을 카드 · 곱 축퇴 처방 · 압력 연산자로 옮길 때 i/i₀(남은 면적 기준) 영역을 같이 적게 할지 — 105호: NMC i/i₀ 5–35(Tafel) · 박리 몫 율 무관 · 선형 영역 문턱 ≈0.036 A m⁻²(≈0.4 C 상당 `[재현·가정]`).
3. (선택) **확률 모형의 같은 조건 산포 표기** ((뇨) 의 확률판으로 묶어도 됨) — 확률 문턱 · 무작위 미세구조 모형의 그림 값을 옮길 때 실현 수와 같은 입력 그림 사이 산포를 적고, 산포보다 작은 효과는 '한 실현' 으로 표시할지 — 105호: NMC 11.5 ↔ 17.0 · LCO 2.97–6.35 · 전류 효과 +2.3 · 경계 효과 ≤0.09.

---

# 어긋남 (D) — 지면 안에서 서로 맞지 않는 것

| # | 어긋남 | 근거 |
|---|---|---|
| **D1** | NMC 창 셋 — 그림 3 "3.0V – 4.5V" ↔ 그림 6 · 8 · S4 "3.2–4.5 V" ↔ 그림 9 · 10 "3.2–4.4 V" · 본문 그림 6 설명 "3.2−4.5 V" | 같은 '첫 사이클' 비교가 창 셋 위 |
| **D2** | 그림 3 캡션 "window of 3.0−4.5 V" ↔ 본문 그림 6 "potential window of operation has been maintained within 3.2−4.5 V" | 기준 그림과 쓸기 그림의 창 |
| **D3** | NMC 150 nm · 1 A m⁻² · 3.2–4.5 V 감쇠 — 그림 8(a) 16.97 · S4(a) ≈17.0 ↔ 그림 6(c) 11.50 · 그림 6(a) · 3 ≈11.7 | `[도표·화소]` |
| **D4** | 그림 6(b) 끝 용량 109.2 · 112.1 · 119.4 · 120.3 ↔ 같은 그림 (c) LCO 감쇠 6.35 · 1.49 · 0.98 · 0.69 | (b) 로는 큰 ≥11.1 · 중간 ≥8.2 |
| **D5** | 그림 5 "compares very well" ↔ 중간 x 실험 방전/충전 0.92 · 0.87(모형 2.16–2.42) · 모형 충전선 = 실험 충전의 0.55–0.63 | `[도표·화소]` |
| **D6** | 같은 출처([17] = SI [23]) 세 수 — 서론 "600 Ω-cm²" · p. 5532 "approximately 1600 Ω" · SI "around 2500 Ω−cm²" | 단위 둘 · 값 셋 |
| **D7** | LCO 150 nm · 1 A m⁻² 감쇠 2.97(8(b)) · ≈4.9(S4(b)) · ≈5.8(그림 4) · 6.35(6(c)) · 박리 0.468 ↔ ≈0.78 | `[도표·화소]` · `[도표]` |
| **D8** | "the extent of fractional interfacial delamination is found to be constant" ↔ NMC 0.574–0.820 · LCO 0.468–0.624 | 평균의 ±18 % · ±14 % |
| **D9** | "0.5−1.0 mAh/(g cycle)"(4.4 V) · "0.1−0.3"(4.1 V) ↔ 1.31 · 0.99 · 0.45 · ≈0.47 · ≈0.43 · ≈0.10 | 4.4 V 큰(1.31) · 작은(0.45) · 4.1 V 큰(≈0.47) · 중간(≈0.43)이 범위 밖 |
| **D10** | "around four times (4×) improvement" · 결론 "4-fold" ↔ 비 2.8 · 2.4 · 4.5(입도별) | `[재현]` |
| **D11** | "the extent of delamination in LCO is either equal or even larger than that of NMC" ↔ 그림 8 넷 중 셋에서 LCO 가 작음(1 · 5 · 7 A m⁻² — 0.468 · 0.489 · 0.563 ↔ 0.820 · 0.658 · 0.574) · 3 A m⁻² 만 비슷(0.624 ↔ 0.614) · S4 비슷(≈0.76–0.82) | `[도표·화소]` |
| **D12** | (S5) "The polynomial fit used in the computational simulations" ↔ 그림 S2(a) · 10(a) 'Polynomial fit' 선 | x 0.26–0.50 ×2–3 |
| **D13** | "3.2−4.4 V … changes from 1.0 to 0.3" · 그림 10(a) 빨간 선 x 0.309 ↔ (S7) 4.4 V = x 0.348 · 0.309 = 4.52 V | `[재현]` |
| **D14** | "At a Li stoichiometry of around 0.7, the open-circuit potential (OCP) of LCO is around 3.8 V" ↔ (S8) 3.933 V · "maximum at around Li stoichiometry of 0.7" ↔ (S6) 꼭지 0.766 | `[재현]` |
| **D15** | 그림 11 "error bars indicate the range of lithium partial molar volume" ↔ NMC 막대 ≈1.0–4.2(그림 10(a) 창 안 ≈1.7–≈11) · LCO 막대 ≈2.8–35 · 표지 ≈6.5(창 안 \|V̄\| ≤4.2 · (S6)) | `[도표]` |
| **D16** | 표 S-I (C5) 시간 항 0 + (C7) 집전체 Li 유속 I_app/F ↔ 그림의 SOC 쓸기 | `[재현·대수]` |
| **D17** | 표 S-I 행 이름 "Displacement boundary condition at the top of SSE"(내용은 좌 · 우 경계) · "at Li/SSE interface"(양극 계면) · 표 S-II "Thickness of solid state electrolyte" thk ↔ SI 본문 "overall thickness of the computational domain" | 표 틀 |
| **D18** | S5(b) 자유 경계 40 · 75 nm 0.21 · 0.43 ↔ S6(c) 공극 0 0.11 · 0.25(같은 기준 경우) · S5 "No statistically significant difference"(통계 0) | `[도표]` |
| **D19** | S6(a) "Around 70% delamination" ↔ S6(c) 150 nm ≈0.85 · 그림 8(a) 0.820 | `[도표]` |
| **D20** | NMC 조성 — 초록 NMC811 · DFT 문턱 NMC622 · 그림 S2(c) 표지 "Cathode: NMC111" | 지면 |
| **D21** | 그림 S3 캡션 a · b 둘 다 (101̄4) ↔ 본문 NMC622 = (101̄0) · 그림 S3 의 'NMC' 표지 쪽에 La · Zr(범례 색) | `[도표]` |
| **D22** | 그림 S2(b) LCO 자료(0 @≈0.53 · ≈21 @0.20) ↔ 97호 그림 2(b) LCO 판독(0 @≈0.59 · +20 @0.47) — 같은 출처 표기 "EES 2018 2142" | 97호 digest 전사 대조 · 원 그림 미열람 |
| **D23** | 초록 그래픽(입자 복합 양극 · Li 음극 · "After Many Cycles") ↔ 계산(평면 100 nm 판 · 음극 0 · 10 사이클) | 지면 |
| **D24** | "The inset image C in **Figure 5**"(p. 5531) ↔ 그 삽도는 그림 3 의 C | 지면 |
| **D25** | "the electrochemical performance is not limited by the ionic conductivity within the LLZO phase" ↔ 표 S-II κ 그대로면 옴 182–500 Ω cm² > LCO R_ct 129 Ω cm² · 7 A m⁻² 127–350 mV | `[재현]` |
| **D26** | "η_intf = i_app·R_intf … the total potential drop increases with increasing current" ↔ 이 편 BV(NMC i/i₀ 5–35 Tafel): 그림 8(a) 분율로 박리 몫 86.8 → 44.1 mV(전류 ↑ 에 감소) | `[재현·대수]` |
| **D27** | SI "observed in both Figures S4(a) and **A1(b)**"(S4(b)) · 본문 "Figure 916"(마침표 · 인용 번호 붙음) · 참고문헌 [62] 정오표 표기 · [73] 인용 자리 | 지면 |

---

# 이 편이 우리 프로젝트에 주는 것 (정리)

- **'사이클 축 접촉 손실 모형' 의 실물은 용량 궤적만 남긴다** — 계보가 유일한 `θ(N)` 모형 원전으로 기대한 편이 박리 분율의 사이클 궤적을 그리지 않았다. 합성 truth R8 은 이 편으로 정해지지 않는다 — 형태 후보 하나(비가역 결합 제거 · 첫 충전 큰 계단 + 이산 누적)와, **용량 궤적 ≠ 접촉 궤적**(Tafel 로그 사상)이라는 경고를 준다.
- **면적형 접촉 손실은 출력에서 i₀ 와 곱이다(식 1)** — 카드 곱 축퇴(`A_eff · k`)의 forward 실례. 모형이 둘을 가르는 것은 구성(역학이 면적을 계산)뿐이다 — 우리 `degradation-degeneracy/` 물음("곡선이 맞는다 ≠ 분해가 맞다")의 ASSB 접촉판 근거(우리 수치는 `degradation-degeneracy/docs/RESULTS*.md` 정본 — 옮기지 않음).
- **율 스윕 판별의 영역 조건** — Tafel 영역에서는 면적 손실의 전압 몫이 율 무관 상수라 '율 의존이면 η 형' 판정이 실패한다. 하네스 · 압력 연산자의 '율 먼저' 처방에 i/i₀(남은 면 기준) 조건을 붙일 근거(새 판단 거리 2).
- **확률 모형의 산포가 결론 크기와 같다** — 한 실현의 그림을 truth 기준 · 카드 수치로 옮기지 않는다(새 판단 거리 3).
- **이 편이 주지 않는 것**: 측정 · 박리 분율의 사이클 궤적 · `LAM` · LLI · 고립 · 압력 · 음극 · OCV 측정 · 식별성 · 반복 · 원자료 · 코드 — 그리고 105 편 누적 `θ(N)` 측정 0.

---

# 후속 후보 (원전 우선 — 지목 수는 위키 digest 의 후속 절 grep 과 원장으로 센 값)

| 등급 | 서지 (PDF 목록 번호) | 지목 (후속 절) | 왜 | 축 |
|---|---|---|---|---|
| ★★★ | Wang D.W., Sun Q., Luo J., Liang J.N., Sun Y.P., Li R.Y., Adair K., Zhang L., Yang R., Lu S.G., Huang H., Sun X.L. 2019 — *ACS Appl. Mater. Interfaces* **11**, 4954−4961([17] · SI [23]) | **105** = 1(새) | **이 편 유일의 실험 고리** — 그림 5 R_ct(x) 점 · i₀ 보정 2500 Ω cm² · '600 Ω-cm²' · '1600 Ω' · "decreasing the size of the cathode particles can help to minimize the delamination-induced increase in charge-transfer resistance" — 박리 배정이 측정으로 서는지(R_ct 만인지 · 단면 · 압력 · 셀 수) · 중간 SOC 방전 ≤ 충전의 정체 | Q1 · Q2 |
| ★★ | Tian H.-K., Qi Y. 2017 — *J. Electrochem. Soc.* **164**, E3512([44]) | 12 · 81 · 94 · 97 · 98 · 99 · 100 · 104 · **105** = **9**(재지목) | "none of them studied the time evolution of the detachment" 의 앞선 편 — 5차 묶음 #2(도착 · 106호) | Q1 · Q6 |
| ★★ | Barai P., Higa K., Ngo A.T., Curtiss L.A., Srinivasan V. 2019 — *J. Electrochem. Soc.* **166**, A1752−A1762([47] · SI [11]) | **105** = 1(새) | **격자 스프링 · 전류 집중 · 입계 파괴 방법 원전** — 문턱 무작위 분포 · 요소 문턱 환산(J m⁻² ↔ J) · 화학 변형 구현(G2 · G3 · G8)의 확인처 | Q1 · Q3 |
| ★★ | Barai P., Ngo A., Narayanan B., Higa K., Curtiss L.A., Srinivasan V. 2020 — *J. Electrochem. Soc.* **167**, 100537([59] · SI [1]) | **105** = 1(새) | LLZO GI · GB 성질 · 파괴 5.3 J m⁻² 의 출처 — '원자 계산 → 연속체' 고리의 실제 위치 | Q3 |
| ★★ | Tsai C.L., Ma Q.L., … Guillon O. 2019 — *Sustain. Energy Fuels* **3**, 280([31]) | 53 · **105** = **2**(재지목) | 공소결 Ta:LLZO–LCO 실셀(원장 행: 100 사이클 감쇠 + 사후 균열) — 이 편 'LCO/LLZO 심한 박리' 예측의 실험 쪽 | Q1 |
| ★★ | Bucci G., Talamini B., Balakrishna A.R., Chiang Y.M., Carter W.C. 2018 — *Phys. Rev. Mater.* **2**, 105407([38]) | 53 · **105** = **2**(Bucci 2018 재지목) | 계면 불안정 · 박리 문턱 7.5 %(원장) — 이 편 상 지도와 같은 축(부피 변형 × SE 강성) | Q1 |
| ★★ | Bucci G., Swamy T., Chiang Y.-M., Carter W.C. 2017 — *J. Mater. Chem. A* **5**, 19422([37]) | 58 · 75 · **105** = **3**(Bucci 2017 재지목) | ASSB 기계 파손 · 부피 변형 이론 앞선 편 | Q1 · Q3 |
| ★★ | Hao F., Mukherjee P.P. 2018 — *J. Electrochem. Soc.* **165**, A1857([39]) | 75 · **105** = **2**(재지목) | 박리 기구 메조 모형 앞선 편 — 접촉 진화의 다른 판 | Q1 · 곱 |
| ★ | Tian H.-K., Chakraborty A., Talin A.A., Eisenlohr P., Qi Y. 2020 — *J. Electrochem. Soc.* **167**, 090541([43]) | 103 · **105** = **2**(재지목) | 응력 · 가장자리 박리 앞선 편 | Q1 · Q6 |
| ★ | Han F.D., Yue J., Chen C., Zhao N., Fan X.L., Ma Z.H., Gao T., Wang F., Guo X.X., Wang C.S. 2018 — *Joule* **2**, 497−508([23]) | **105** = 1(새) | LBCO 계면층 LCO/LLZO '100 사이클 무감쇠' — 모형 예측(LCO/LLZO 심한 박리)의 실험 반대편 | Q1 |
| ★ | Ohta S., Kobayashi T., Seki J., Asaoka T. 2012 — *J. Power Sources* **202**, 332−335([25] · SI [24]) | **105** = 1(새) | LCO/LLZO R_ct 250 Ω cm²(i₀ 2.0 보정)의 출처 · 면적 · 온도 | Q3 |
| ★ | Sharafi A., Haslam C.G., Kerns R.D., Wolfenstine J., Sakamoto J. 2017 — *J. Mater. Chem. A* **5**, 21491−21504([68]) | **105** = 1(새) | LLZO 입도 ↔ 파괴 인성 · 탄성 — 입도 처방의 실험 전제 | Q1 · DEM |
| ★ | Yu S., Siegel D.J. 2017 — *Chem. Mater.* **29**, 9639 · 2018 — *ACS Appl. Mater. Interfaces* **10**, 38151([52] · [53] · SI [20] · [21]) | **105** = 1(새 · 묶음) | GB Li 농도 · GB 연화(Y_GB 120 ↔ GI 141) — 입도 효과의 유일한 기둥 | Q3 |
| ★ | Nukala P.K.V.V., Simunovic S., Guddati M.N. 2005 — *Int. J. Numer. Methods Eng.* **62**, 1982−2008(SI [15]) | **105** = 1(새) | 손상 누적 알고리즘 — 격자 요소 제거 · 문턱 무작위의 규칙(N 축 형태를 정하는 것) | Q1 |
| ★ | Qi Y., Hector L.G., James C., Kim K.J. 2014 — *J. Electrochem. Soc.* **161**, F3010([45] · SI [31]) | 97 · **105** = **2**(재지목) | 양극 Y · ν 120 GPa · 0.3 의 출처 중 하나(NMC · LCO 공통) | Q6 · DEM |
| ★ | Monroe C., Newman J. 2005 — *J. Electrochem. Soc.* **152**, A396([5] · SI [17]) | 61 · 97 · **105** = **3**(재지목) | (S1) 응력–동역학 결합 항의 원전 | Q6 · Q7 |
| ★ | Haruyama J., Sodeyama K., Han L., Takada K., Tateyama Y. 2014 — *Chem. Mater.* **26**, 4248([69]) | 50 · 84 · **105** = **3**(재지목) | 황화물 계면 파괴 ≈0.8 J m⁻²(상 지도 아래 경계 — [70] Okuno 2020 과 짝) | Q8 · DEM |
| ★ | Deng Z., Wang Z., Chu I.-H., Luo J., Ong S.P. 2016 — *J. Electrochem. Soc.* **163**, A67([71]) | 18 · 97 · **105** = **3**(재지목) | 황화물 Y = Li 의 2–3 배(상 지도 x 위치) | Q6 · DEM |
| ★ | Walther F., Koerver R., Fuchs T., Ohno S., Sann J., Rohnke M., Zeier W.G., Janek J. 2019 — *Chem. Mater.* **31**, 3745([35]) | 82 · 86 · 87 · 90 · **105** = **5**(재지목) | 이 편이 '사이클 박리 보고' 로 인용한 ToF-SIMS 분해 계면층 편 — 박리 보고인지 확인처 | Q1 · Q8 |
| ☆ | [2] Famprikis 2019 · [3] Kato 2016(원장 L253) · [18] Yu C. 2017(원장 L390) · [21] Hamann 2020(원장 L465) · [56] Barai 2013 · [61] Monroe 2004 · [63] Schwaiger 2003 · [65] Zhu 2019 · [66] Rahn & Wang · [70] Okuno 2020 · [72] Lee 2019 · [74] Xie 2012 · SI [18] Guo 2011 · [47] Awarke 2013 · 나머지 서론 | 행 변화 없음 | 서론 목록 · 방법 · 문헌 값 | — |

**지목 누락 0** — 이 편 74 + 51 번호 중 앞 호 후속 절에 ★ 이상으로 있던 편은 위 재지목 열하나(Tian & Qi · Tsai 2019 · Bucci 2018 · Bucci 2017 · Hao & Mukherjee · Tian 2020 · Qi 2014 · Monroe & Newman 2005 · Haruyama 2014 · Deng 2016 · Walther 2019)이고 모두 원장 행이 있다 · ☆ 로 둔 원장 행 셋(Kato 2016 · Yu C. 2017 · Hamann 2020)은 이 편에서 서론 목록이라 지목 수를 올리지 않는다. **흡수된 편(교차)**: [16] = 23호 · [19] = 63호 · [22] = 77호 · [36] = 97호 — 셈 밖.

---

# 이 digest 가 주장하지 않는 것

- **이 편의 결론 방향(작은 LLZO 입도 · 낮은 상한 전압 · 연한 SE · 영변형 양극이 박리를 줄인다)이 틀렸다고 하지 않는다** — 방향은 큰 축(입도 150 → 40 nm)에서 그림이 지지한다; 걸린 것은 `θ(N)` 곡선 부재 · 같은 조건 산포 · 실험 비교의 자료 경로 · 인쇄 식과 계산의 불일치 · 요약 수치의 범위다.
- **박리 분율이 사이클에 따라 어떻게 진화하는지 추정하지 않는다** — 용량 궤적과 로그 사상까지다(분율 궤적 인쇄 0).
- **'53호가 이 편을 잘못 요약했다' 고 단정하지 않는다** — '포화 없이' 는 곡선 여섯에서 맞고 둘에서 안 맞으며, 10 사이클 · 한 실현으로는 어느 쪽도 판정할 수 없다는 것까지다.
- **저자 구현이 인쇄 식(C5 · C7 · S4 · S5)과 다르다고 확정하지 않는다** — 인쇄 식 그대로면 그림이 안 나온다는 대수(`[재현·대수]`)와 그림 맞춤선 판독까지다. 코드 미공개.
- **Tafel 대수(Δη · 선형 영역 문턱 · C-rate 환산)를 저자 계산의 값으로 쓰지 않는다** — 대칭 BV · 균일 계면 전류 · 응력 항 무시 · ρ 4.75 g cm⁻³(`[외부 값]`) 가정 위의 `[재현·대수]` · `[재현·가정]` 이다.
- **Wang 2019 의 측정이 박리를 보이지 않는다고 하지 않는다** — 그림 5 디지타이즈 점(이 편이 옮긴 것)에서 중간 x 방전 ≤ 충전이라는 것까지다(Wang 원문 미열람).
- **i₀ 의 ×1.93 을 저자 오류로 확정하지 않는다** — RT/(R_ct F) 산술과 인쇄값의 비이고, 다른 규약(예: 두 계면 · 다른 R_ct 값)의 가능성은 지면에서 가를 수 없다.
- **κ_LLZO 단위를 S cm⁻¹ 로 고쳐 읽지 않는다** — 인쇄 그대로의 옴 몫과 단위 의심까지다.
- **그림 S3 표지 뒤바뀜을 계산 오류로 쓰지 않는다** — 그림 표지와 범례 색의 대응이 맞지 않는다는 것(`[도표]`)까지다.
- **이 편을 Q4 · Q2 칸 이동 근거로 쓰지 않는다** — 식별성 · 독립 관측 0.
- **원 참고문헌(23 · 53 · 63 · 75 · 77 · 83 · 94 · 97호 인용분)을 다시 열지 않았다** — 대조는 각 digest 전사로 했다.

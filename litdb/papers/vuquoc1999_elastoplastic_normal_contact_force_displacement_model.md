<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     꼴 = thorntonning1998_adhesive_elastoplastic_contact.md (같은 축 · 이 논문이 FEA 로 '너무 무르다' 고 평가한 Thornton (1997) 법칙의 점착판) ·
     스캔 판 꼴 = walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem.md · 고른 의도를 적은 카드 = morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis.md (그 학위논문 그림 3.7 = 이 논문 그림 16).
     쪽 표기: p.N = 인쇄 쪽 4013–4044 · 원문 PDF = JSTOR 판 33 쪽 (PDF 1 쪽 = JSTOR 표지 · PDF 쪽 p ↔ 인쇄 쪽 4011 + p · 보충 자료 안내 없음).
     원문 = 1999 년 조판의 **스캔** (쪽마다 600 dpi 1 비트 JBIG2 한 장 + OCR 글 층 · 25 쪽만 그림 18 을 따로 실은 300 dpi 사진 한 장) — OCR 글 층은 식 · 기호를 거의 다
     깨뜨린다 (예: 식 앞 문장의 R* = ½R 를 'R* - R' 로) → 식 · 숫자 · 기호는 전부 원 래스터 크롭 (litdb/figures/<slug>/ · 97 장) 에서 읽었고, 산문은 글 층과 크롭을 대조했다.
     값 표지: [인쇄] = 본문 · 캡션 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 67 행 ·
     tools/litdb/vuquoc1999_nfd_reproduce.py --digitize · 원 래스터 600 dpi · 틀 · 눈금 막대 보정 · 표지 = 범례 표지 틀 맞춤 · 방법은 각 행 note ·
     ⚠ PDF 11 · 13 · 15 · 23 쪽 스캔은 세로선이 기울어 있다 (틀 dx/dy ≈ −0.009 ~ −0.013 · 가로선은 수평 = 가로 전단) → 높이에 따라 x 보정이 달라
     x 판독은 그 축 가까이에서 · 14 · 24 · 30 쪽은 기울기 없음) ·
     [재현] = 이 카드가 식 (3.7)–(3.22) · 알고리즘 3.2 / 3.3 · §4 충돌을 그대로 다시 짜서 낸 값 (같은 도구 --selftest = 원문 인쇄값 15 개 재현 PASS) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 추론] = 이 카드의 해석 · [다른 카드] = 정본 다른 카드의 값 (slug 병기) ·
     [우리] = 우리 쪽 값 (CLAUDE.md 출처) · [미확인] = 원문 32 쪽에 없음. -->
# 탄소성 구의 법선 접촉력–변위 (NFD) 법칙 — 접촉 반지름을 탄성 + 소성으로 더하고 (a^ep = a^e + a^p · a^p = C_a⟨P − P_Y⟩) 접촉 곡률을 고친다 (R*_p = C_R R* · C_R = 1 + K_c⟨P − P_Y⟩) · ABAQUS 축대칭 FEA (알루미늄 합금 구 R 0.1 m · E 70 GPa · σ_Y 100 MPa · P ≤ 1500 N = P/P_Y ≤ 41) 에 맞춘 상수 둘 (C_a 2.33 × 10⁻⁷ m/N · K_c 2.69 × 10⁻⁴ N⁻¹) · Thornton (1997) 의 선형 소성 가지는 *"much too soft"* (α 1.56 × 10⁻⁵ m 에서 770.5 vs 1500 N) · 변위 구동 DEM 알고리즘 + 단일 구 충돌 (e 0.84 → 0.48) — 다입자 · 압밀 · 조밀 영역 · 입자 형상 변화 · 다른 재료 없음 — Vu-Quoc & Zhang (Proc. R. Soc. Lond. A 1999)

> slug `vuquoc1999_elastoplastic_normal_contact_force_displacement_model` · DOI `10.1098/rspa.1999.0488` · type `DEM contact law (elastoplastic normal force-displacement, displacement-driven, additive contact-radius decomposition + curvature correction, 2 FEA-fitted constants) + nonlinear FEA (ABAQUS 5.4 axisymmetric sphere vs frictionless rigid plane, elastic-perfectly plastic Al alloy) + single-sphere normal collision (leap-frog) vs Thornton 1997 · no packing / compaction / multi-contact / particle shape change / SE / NCM` · PDF `VuQuoc_Zhang_1999_ProcRSocLondA455_4013_elastoplastic_normal_contact_displacement_driven.pdf` · digested `2026-11-17` · status ✅
>
> **저자**: **Loc Vu-Quoc** · **Xiang Zhang** — Department of Aerospace Engineering, Mechanics and Engineering Science, University of Florida, Gainesville, FL 32611, USA (p.4013) · *Proc. R. Soc. Lond. A* **455** (1999) **4013–4044** (JSTOR 표지: *"Proceedings: Mathematical, Physical and Engineering Sciences, Vol. 455, No. 1991 (Nov. 8, 1999), pp. 4013-4044"* · Stable URL `https://www.jstor.org/stable/53544`) · 접수 1998-03-19 · 수정 1998-10-26 · 승인 1999-02-18 (p.4013) · ⚠ **DOI 는 이 JSTOR 판 어디에도 인쇄돼 있지 않다** — 메타줄의 `10.1098/rspa.1999.0488` 은 고른 의도를 적은 `morrissey2013_…` 참고문헌 줄 (L447) 의 값 [원문 대조 못 함] · 감사: *"We thank Lee Lesburg for his discussions. The support of the US National Science Foundation is gratefully acknowledged."* (p.4043) · 키워드: granular flow; discrete-element method; force–displacement models; normal direction; contact mechanics; elastoplasticity (p.4013).
> **짝 논문 (원문이 *"(Submitted.)"* · *"(In the press.)"* 로 적은 것 — 이 카드 시점 서지는 원문 목록 그대로)**: 힘 구동판 = Vu-Quoc, Zhang & Lesburg 1999a (ASME J. Appl. Mech., submitted · K_c 의 자세한 근거) · 접선 탄소성판 = Vu-Quoc & Zhang 1999b (submitted) · 더 많은 FEA = Vu-Quoc & Lesburg 1999 (submitted) · 실험으로 상수 뽑기 = Zhang & Vu-Quoc 1999 (Int. J. Plasticity, submitted) · 나머지 경우 = Zhang 1998 박사논문 (Univ. Florida) — 모두 정본 카드 없음 (§12).
> **이웃 카드 (링크만)**: [`thorntonning1998_adhesive_elastoplastic_contact`](thorntonning1998_adhesive_elastoplastic_contact.md) (이 논문이 *"too soft"* 라 한 Thornton (1997) 법칙의 1998 점착판 · 같은 4 단계 꼴) · [`morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis`](morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis.md) (고른 의도 · 그림 3.7 = 이 논문 그림 16) · [`kogutetsion2002_ep_sphere_rigid_flat`](kogutetsion2002_ep_sphere_rigid_flat.md) (같은 문제의 FEM 기준선 · 평균압 1.0 → 2.8 Y) · [`jacksongreen2005_fem_elastoplastic_hemispherical_contact`](jacksongreen2005_fem_elastoplastic_hemispherical_contact.md) (H 가 a/R 에 따라 내려감) · [`mesarovicfleck2000_dissimilar_elastoplastic_indentation`](mesarovicfleck2000_dissimilar_elastoplastic_indentation.md) · [`storakers1997_similarity_inelastic_contact`](storakers1997_similarity_inelastic_contact.md) · [`luding2008_cohesive_frictional_contact_models`](luding2008_cohesive_frictional_contact_models.md) (우리 `hooke/hysteresis` = Walton–Braun 계열) · [`walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem`](walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem.md) (⚠ 같은 저자 · 같은 해 **다른** 글 — 이 논문의 'Walton (1993)' 은 Roco 편 책 25 장, §12) · [`varkey2026_multicontact_elastoplastic_dem`](varkey2026_multicontact_elastoplastic_dem.md) (Thornton–Ning + 다접촉) · [`zunker2024_mdr_contact_model_partI`](zunker2024_mdr_contact_model_partI.md) (큰 겹침 접촉) · [`silbert2001_chute_flow_bagnold_spring_dashpot_hertz_dem`](silbert2001_chute_flow_bagnold_spring_dashpot_hertz_dem.md) (참고 [31] 서지 대조 · §0-1).
> **판독 · 재현 원자료**: `litdb/figures/vuquoc1999_elastoplastic_normal_contact_force_displacement_model/digitized.csv` (67 행 — 그림 20 표지 40 · 그림 10 / 16 의 하중 0 마지막 점 4 · 그림 10 α_max 점선 3 (ADE · AFG = 인쇄 1.14 · 1.56 × 10⁻⁵ 와 맞음 = 판독 검증) · 그림 11 접촉 반지름 절점 6 + Hertz 확인 3 (식 1.7 과 ±0.0013 × 10⁻³) · 그림 12 FEA 제하 점 4 + 모델 직선 · 점선 6 · 그림 17 일점쇄선 1) · `tools/litdb/vuquoc1999_nfd_reproduce.py` (모델 · Thornton · 충돌 재구현 + 판독 · `--selftest` 15/15 PASS) · 크롭 **97 장** (그림 25 = 21 + 패널 4 · 알고리즘 상자 2 · 번호 식 50 (식마다 한 장) · 근거 문단 20 · 도구가 찾은 11 장은 쪽 너비 띠라 **전부** 다시 자름 + 손 크롭 다시 자름 10) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 단일 접촉에서 탄소성 구 (탄성–완전소성 알루미늄 합금 · E/σ_Y = 700) 를 마찰 없는 강체 평판에 눌렀다 떼는 축대칭 FEA 를 보고, Hertz 접촉 반지름 위에 **선형으로 자라는 '소성 반지름'** a^p = C_a⟨P − P_Y⟩ 을 더하고 접촉 곡률 반지름을 C_R(P) = 1 + K_c⟨P − P_Y⟩ 배로 키운 뒤 Hertz 기하 2α = (a^ep)²/(C_R R*) 로 α ↔ P 를 잇는 **법선 접촉 법칙** (제하 = 곡률 · 소성 반지름을 P_max 값에 고정한 Hertz) 을 만들고, 그 두 상수를 같은 FEA 에 맞추면 P–α 곡선 · 반발계수가 FEA 와 0.3 · 2.3 % 안에서 맞는 반면 **Thornton (1997) 의 '압력 캡 1.61σ_Y + 직선 소성 가지' 는 같은 변위에서 힘을 절반 (51–56 %) 만 낸다** — 다만 이것은 **한 재료 · 한 크기 · 단일 접촉 · 작은 변형 (겹침 ÷ 지름 ≤ 1.6 × 10⁻⁴)** 에서의 결론이고 다입자 · 조밀 압밀 · 입자 형상은 다루지 않는다.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 항복 뒤 힘–변위 꼴 (본 세션 까닭 ①) | **암묵식**: F(P) = (P − P_Y) + c₁P^(1/3) − (1/C_a){C_R(P) R α}^(1/2) = 0 (식 3.15 · 같은 구 두 개 · α = 접근의 반) → 뉴턴 (식 3.16–3.18 · 상대 증분 ≤ 0.005 · 최대 2 회 [인쇄]) · **직선도 Hertz 도 아님** — FEA 가 *"the P–α curves are not straight lines as assumed in Thornton (1997)"* (p.4023) · FEA 범위 안에서 Hertz 보다 무르고 (α 1.56 × 10⁻⁵ m: FEA 1500 N ↔ Hertz 1998 N [카드 산술 · 식 3.10]) Thornton 보다 단단하다 (770.5 N [인쇄]) · 범위 밖 (P ≫ 8.8 × 10³ N) 에선 P ≈ K_c R α / C_a² (기울기 ≈ 5.0 × 10⁸ N/m) 로 다시 직선이 된다 [카드 산술 · 외삽] | [인쇄] 식 3.10–3.18 · p.4023 · p.4034 · [카드 산술] |
| ② 접촉 반지름 (면적) 식 | **a^ep = a^e + a^p** (식 2.3) · a^e = Hertz (1.3)/(1.7) · a^p = C_a⟨P − P_Y⟩ (2.5) · 정렬 **a_Th > a_FE > a_Hz** (2.2 · 같은 힘) · 1500 N 에서 a^ep 1.476 × 10⁻³ m ↔ FEA 1.449–1.497 × 10⁻³ (마지막 p > 0 절점 ↔ 첫 p = 0 절점) [판독 그림 11] ↔ Hertz 1.135 × 10⁻³ [카드 산술] → **평균 접촉압 P/π(a^ep)² = 1.99 · 2.15 · 2.19 σ_Y (500 · 1000 · 1500 N)** [카드 산술] · FEA 절점 구간으로는 1.88–2.03 · 2.03–2.16 · 2.13–2.27 σ_Y [판독 + 카드 산술] · FEA 압력 분포는 세 힘 모두 **평평한 꼭대기 ≈ 2.25 × 10⁸ N m⁻² > 2.00σ_Y** (Thornton 캡 1.61σ_Y 보다 높고, 힘에 따라 *"not fixed"*) | [인쇄] p.4024–4025 · 식 2.2–2.5 · [판독] · [카드 산술] |
| ③ 제하 · 잔류 겹침 (본 세션 까닭 ②) | 제하 = **Hertz, 곡률은 C_R(P_max)R 에 고정 · a^p 는 a^p_max 에 고정** (식 3.19–3.22) → α_res = α_max − (a^e_max)²/(C_R(P_max)R) · 정적 한 주기 [재현]: P_max 500 · 1000 · 1500 N → α_res 1.62 · 3.94 · 6.39 × 10⁻⁶ m (되돌아옴 몫 0.77 · 0.67 · 0.59) · ★ FEA 의 하중 0 마지막 점 [판독 그림 10 · 16] **2.0 · 4.5 · 7.1 × 10⁻⁶ m** (되돌아옴 0.70 · 0.60 · 0.55) · 같은 α_max (FEA) 를 넣은 변위 구동 [재현] 1.48 · 3.74 · 6.37 × 10⁻⁶ → 모델 잔류는 FEA 보다 **26 · 18 · 10 % 작다** (되돌아옴을 크게 본다) · 같은 이력의 Thornton (R_p* 제하) 은 **47 · 39 · 35 % 크다** [카드 산술 · R_p* 식은 이 논문에 없어 Thornton–Ning 1998 식 28 을 빌림] · 원문은 잔류 변위를 숫자로 비교하지 않는다 | [인쇄] 식 3.19–3.22 · [판독] · [재현] · [카드 산술] |
| ④ FEA 대조 범위 | 하중 경로 셋 ABC · ADE · AFG = P_max **500 · 1000 · 1500 N** (P/P_Y **14 · 27 · 41** [카드 산술]) · α_max ≈ **6.8 × 10⁻⁶ [판독] · 1.14 × 10⁻⁵ · 1.56 × 10⁻⁵ m [인쇄]** (α/α_Y ≈ 6.3 · 10.5 · 14.4 · 겹침 ÷ 지름 ≤ 1.6 × 10⁻⁴ · a/R ≤ 0.015) · 비교 결과: AFG e 0.7541 vs 0.7372 (2.3 %) · P_max 1495 vs 1500 N (0.3 %) · ADE 0.7994 vs 0.7757 (3.1 %) · 962.1 vs 1000 N (3.8 %) · ABC = *"Similar results"* (숫자 없음 · Zhang 1998) · ⚠ 두 상수를 **같은 FEA** 에 맞추고 같은 FEA 로 비교 (표본 밖 검증 아님) · FEA 기준 자체는 다른 FEM (Kogut–Etsion 2002 맞춤식) 이 같은 α 에서 521 · 1002 · 1488 N (+4 · +0.2 · −0.8 %) 으로 다시 낸다 [다른 카드 식 · 카드 산술 · §3-4b] · 충돌 모의 0.06–0.20 m/s 는 P_max 2.3 × 10³–1.04 × 10⁴ N (P/P_Y 64–286) 로 **맞춘 범위 밖** [재현] | [인쇄] p.4021 · p.4027 · p.4029 · p.4034–4035 · [판독] · [카드 산술] · [재현] |
| ⑤ 못 하는 것 (본 세션 까닭 ③) | 다입자 · 충전 · 조밀 영역 · 다접촉 상호작용 · 접선 (짝 논문 몫) · 점착 · 가공 경화 (재료) · 재재하 가지 · 속도 효과 (*"time-independent plasticity"* p.4038) · 입자 형상 변화 (곡률 보정은 접촉의 대리 · 입자는 여전히 구) · 큰 변형 (FEA 는 a/R ≤ 0.015) · 다른 재료 · 크기 (*"One should not use these values for other examples without verifying their validity"* p.4030) — 우리 SE 압밀 겹침 (≈ 7.4–11 % of d [우리 · 7.4 % = 복합 침대 ⟨δ⟩ 0.0739 µm 를 SE 지름 1 µm 로 나눈 어림]) 은 이 범위의 **≈ 470–700 배** · α/α_Y 로 **≈ 80 – 4 × 10³** (LPSCl E 22 GPa · ν 0.36 · σ_y 0.05–0.30 GPa [미확인 · 카드 없음] 대입 [카드 산술]) | [인쇄] p.4030 · p.4038 · p.4042–4043 · [카드 산술] |

**절대값 전이**: ⛔ 안 된다 — 재료 = 알루미늄 합금 (E 70 GPa · σ_Y 100 MPa) · 크기 = R 0.1 m · 단일 접촉 · 작은 변형.  C_a · K_c 는 저자 스스로 *"particular to the present geometry and material"* (Remark 2.1 · 3.1).  전이되는 것 = **법칙의 꼴 (반지름 더하기 · 곡률 보정 · 고정 제하) · 무차원 비 (평균압 ≈ 2σ_Y · Thornton 결손의 분해) · 검증 방식 (P–α + e 둘 다 · Remark 4.2)**.

---

## 0-1. ★ 고른 의도 대조 (위시 11-17 보탬 · `morrissey2013_…` n 줄 + 본 세션 까닭 셋)

의도 원문 (위시): *"FEA 로 '선형 · Thornton 탄소성 접촉은 고응력에서 너무 무르다' (그림 3.7 · p.48 · p.77) — 점접촉 법칙이 깨지는 범위 (질문 e · k · l) · 후보 C′"* — 여기서 그림 3.7 · p.48 · p.77 은 **Morrissey 학위논문** 의 자리다.

| 의도 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| ① FEA 로 Thornton 탄소성 접촉이 너무 무르다 | **채움** | p.4019 *"We will show later that the Thornton (1997) NFD model produces FD curves that are too soft compared with the FEA results."* · p.4034 *"The P–α curve produced by the Thornton (1997) NFD model is, however, much too soft"* — α_max ≃ 1.56 × 10⁻⁵ m 에서 (P_max)_Th **770.5 N** = FEA **1500 N** 의 *"about half"* · e_Th 0.5641 vs e_FE 0.7372 (*"about 23.5 %"*) · ADE: 559.6 N vs 1000 N (*"by 44 %"*) at α_max ≃ 1.14 × 10⁻⁵ m (p.4035) · 조건 = 준정적 FEA (힘 구동 · 30 단계 넘게) 의 변위 이력을 두 모델에 넣은 **변위 구동 비교** (MATLAB · p.4033–4034) · 단일 알루미늄 구 ↔ 강체 평판 · 마찰 없음 |
| ② '선형' 모델이 너무 무르다 (모델 일반) | **일부** | FEA 와 견준 '선형' 은 **Thornton (1997) 의 직선 소성 가지 하나** (*"Thornton (1997) believes that there is a linear relationship between the normal displacement α and the normal contact force P after the incipient plastic deformation"* p.4017 · 그림 4 *"Linear P versus α relationship for P > P_Y"*) · Walton–Braun 이중 선형 (식 1.9) · 스프링–대시포트는 FEA 와 **견주지 않았다** — 다른 이유로 비판: W–B = e 가 속도와 무관 (*"not in agreement with experimental results: e is not a material property"* p.4017) · 대시포트 = *"There is no solid basis for obtaining the coefficient of the dashpot"* · *"primitive NFD model"* (p.4019) |
| ③ '고응력에서' | **일부** | FEA 비교는 P_max 500 · 1000 · 1500 N (P/P_Y 14–41 [카드 산술]) 세 점뿐 · Thornton/FEA 힘 비 = 0.56 (1000 N) · 0.51 (1500 N) [카드 산술] — 그림 16 에서 두 곡선 사이가 하중과 함께 벌어진다 [판독] · '고응력' 의 문턱 · 범위를 원문이 정하지 않았다 |
| ④ 그림 3.7 · p.48 · p.77 (2 차 인용) | **채움 (대조 일치)** | Morrissey 그림 3.7 (`morrissey2013_…` 크롭 `fig_3_7.png`) = **이 논문 그림 16 과 같은 그림** (같은 범례 · e_FE 0.7372 · e_pm 0.7541 · e_Th 0.5641 · (P_max) 1500 · 1495 · 770.5 N) — 그 카드 L273 *"Vu-Quoc–Zhang 1999b 가 Thornton 모델이 FEA 보다 "too soft" (그림 3.7)"* 는 원문과 맞다 · L249 *"these linear models maybe too soft at higher stresses" (Vu-Quoc · Zhang 1999b 의 FEA)* 는 Morrissey 자신의 말 (p.77) 이고 원문이 보인 것 (Thornton 직선 가지) 보다 넓다 (②) · L447 서지 (권 455 · 호 1991 · 4013–4044) = 원문과 같음 · DOI 는 JSTOR 판에 인쇄 안 됨 (대조 못 함) · ⚠ 'Vu-Quoc and Zhang 1999b' 라는 꼬리표는 **Morrissey 의 목록 기준** — 이 논문 자신의 참고문헌에서 'Vu-Quoc & Zhang 1999b' 는 **접선** 탄소성 논문 (submitted) 이다 (혼동 주의 · 카드 문제 아님) |
| ⑤ 점접촉 법칙이 깨지는 범위 (질문 e) | **일부** | 깨지는 쪽 하나는 분명: **Hertz 는 P_Y 위에서 깨진다** (*"(i) When the normal force P is smaller than the incipient yield normal force P_Y, the P–α curve obtained from FEA agrees very well with Hertz theory"* p.4023 · P_Y 36.4 N · α_Y 1.08 × 10⁻⁶ m [카드 산술]) · Thornton 직선 가지는 P/P_Y 27–41 에서 힘을 절반으로 본다 · **큰 변형 · 조밀 · 다접촉에서 깨지는 범위 = 없음** (단일 접촉 · a/R ≤ 0.015) |
| ⑥ 질문 k (DEM 한계) · l (소성이 어려운 이유) | **일부** | k: 접촉 법칙 층의 한계 문장 (대시포트 · W–B · Thornton 무검증 — 각주 *"In fact, there was no validation of the theory proposed in Thornton (1997) until now"* p.4019) 은 있다 · 구 모양 · 조밀 영역 · 접촉 독립 가정 = **말 없음** · l: 우회 = FEA 를 보고 접촉 반지름을 쪼갬 · 상수 둘을 재료 · 크기마다 FEA (또는 실험) 로 · *"Further theoretical work can be done to relate these model parameters to other basic parameters"* (p.4030 · p.4042) · 비균질 입자 = *"it is impossible to use FEA in this case"* (p.4043) · 계산 비용 (FEA 시간) [미확인] |
| ⑦ 후보 C′ (항복 캡 탄소성 접촉 DEM) | **채움 (대안 + 반증 자료)** | (a) C′ 의 대표 (Thornton 꼴 p_y 캡) 가 단일 접촉에서 이미 2 배 무르다는 FEA 자료 · (b) 대안 법칙 = 맞춘 상수 **2** (C_a · K_c) + 재료 입력 4 (R · E · ν · σ_Y) · A_Y(ν) (ν 0.3 에서 1.61) · (c) DEM 구현 비용 = 뉴턴 ≤ 2 회 / 단계 (Δt 1.0 × 10⁻⁶ s · 허용 0.005) [인쇄 p.4038] |
| 본 세션 까닭 ① 항복 뒤 꼴 · FEA 대조 범위 · 반지름 (면적) 식 | **채움 (작은 변형 한정)** | §0 표 ① ② ④ · §3-3 · §3-4 · §4-2 |
| 본 세션 까닭 ② 제하 곡선 · 잔류 변위 → 언로딩 키트 · 탈압 해석 기준? | **일부** | 제하 법칙 꼴 (식 3.19–3.22) 은 있다 · 잔류 변위 수치는 원문에 **없고** 그림 판독뿐 (FEA 2.0 · 4.5 · 7.1 × 10⁻⁶ m) · 모델은 FEA 보다 잔류를 10–26 % 작게 본다 [카드 산술] · 다입자 · 조밀 · 우리 변형 깊이 (α/α_Y ≈ 80 – 4 × 10³) 에서는 검증 없음 → **단일 접촉 단위 시험 (U3 꼴) 의 기준값** 으로는 쓸 수 있고 침대 탈압의 해석 기준으로는 못 쓴다 (§8 단계 6 · U3) |
| 본 세션 까닭 ③ 못 하는 것 | **채움 (한계 목록)** | §0 ⑤ · §4-4 · §11 |

**가리킨 카드 · 2 차 인용 대조** (고치지 않음 · 카드 문제 아님): `morrissey2013_…` L249 · L273 · L447 (위 ④) · `demirtas2021_mpfem_hollow_sphere_die_compaction` L536 의 *"[24] = Vu-Quoc 2001"* · `harthong2009_high_density_compaction_dem_voronoi_contact_law` L329 · L498 의 *"Vu-Quoc, Zhang, Lesburg 2001 … IJSS 38, 6455–6489"* = **같은 저자 다른 논문** (2001 접선 · 이 카드와 섞지 말 것 · 둘 다 원문 서지와 모순 없음) · `silbert2001_…` L473 · L492 가 *"[31] (Vu-Quoc & Zhang) 과 [32] (Vemuri 외) 가 같은 'Mech. Mater. 31, 235 (1999)' — 둘 중 하나는 틀렸다"* 고 남긴 것: 이 논문 참고문헌 (p.4043) 이 **"Vu-Quoc, L. & Zhang, X. 1999a An accurate and efficient tangential force–displacement model for elastic-frictional contact in particle-flow simulations. Mech. Mater. 31, 235–269."** 라 적는다 → [31] 쪽이 이 목록과 맞는다 ([32] Vemuri 의 원문은 [미확인]).

---

## 1. 한 줄 요약

DEM 의 법선 접촉 법칙을 **연속체 탄소성의 꼴 (변형률 = 탄성 + 소성)** 에 빗대어 **접촉 반지름 = 탄성 (Hertz) + 소성 (P − P_Y 에 선형)** 으로 쪼개고, 소성이 접촉면을 평평하게 만드는 것을 **곡률 반지름 배수 C_R(P)** 로 넣어 Hertz 기하를 일반화한 **변위 구동판** NFD 모델 (입력 α → 뉴턴으로 P) — 두 상수 (C_a · K_c) 를 ABAQUS 축대칭 탄소성 FEA (알루미늄 합금 구 · 강체 평판 · P ≤ 1500 N) 에서 뽑아 같은 FEA 의 P–α · 반발계수를 0.3–3.8 % 안에서 다시 내고, 같은 FEA 대비 Thornton (1997) 의 직선 소성 가지는 힘 절반 · e 22–24 % 낮음을 보였으며, 단일 구 충돌 (0.02–0.20 m/s) 에서 e 가 속도와 함께 줄어드는 것 (0.84 → 0.48) 을 냈다.

## 2. 메타

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 저자 · 소속 | Loc Vu-Quoc · Xiang Zhang — Dept. of Aerospace Engineering, Mechanics and Engineering Science, Univ. of Florida | [인쇄] p.4013 |
| 학술지 | *Proc. R. Soc. Lond. A* (1999) **455**, 4013–4044 · JSTOR = Vol. 455 No. 1991 (1999-11-08) | [인쇄] p.4013 · JSTOR 표지 |
| DOI | `10.1098/rspa.1999.0488` | ⚠ 원문 (JSTOR 판) 에 인쇄 안 됨 — `morrissey2013_…` L447 값 |
| 일정 | 접수 1998-03-19 · 수정 1998-10-26 · 승인 1999-02-18 | [인쇄] p.4013 |
| 연구 유형 | DEM 접촉 법칙 이론 + 단일 접촉 비선형 FEA (보정 · 검증) + 단일 구 충돌 모의 | — |
| 재료 | 알루미늄 합금 (탄성–완전소성) · E 70 GPa · ν 0.3 · σ_Y 100 MPa · ρ 2.699 × 10³ kg m⁻³ — SE · NCM · 분말 없음 | [인쇄] p.4021 · p.4036 |
| 크기 | 구 반지름 R = 0.1 m (질량 11.306 kg) · 단분산 · 한 개 | [인쇄] p.4021 · p.4036 |
| 차원 | FEA = 축대칭 (3D 구 · 2D 메시) · 충돌 = 1 자유도 (법선 · 회전 · 접선 · 중력 없음) | [인쇄] p.4020 · p.4036 |
| 압력 · 힘 | 접촉력 P_max 500 · 1000 · 1500 N (FEA) · 충돌 P_max 635–10 431 N [재현] — '압력' (분체 응력) 은 없다 | [인쇄] 그림 7 · [재현] |
| 보충 자료 | 안내 없음 | — |

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 입력 · 설정

| 항목 | 값 | 표지 · 위치 |
|---|---|---|
| FEA 코드 · 요소 | **ABAQUS ver. 5.4** · 축대칭 반구 **2141 개 6 절점 삼각형 (CAX6) · 4442 절점** · 접촉면 = 1 차원 2 절점 축대칭 면 요소 (IRS22A) · 마찰 없는 강체 평판 · Saint-Venant 원리로 점선 사각형 안만 이산화 (그림 5 · 6) | [인쇄] p.4020 · 크롭 `txt_p9_…` |
| FEA 해상도 | 접촉 근처 요소 · 접촉 요소 크기 **~2.3 × 10⁻⁵ m** ↔ 접촉 반지름 **~1.1 × 10⁻³ m** (≈48 요소 / 접촉 반지름 [카드 산술]) · 한 주기 (적재 + 제하) **30 단계 넘게** | [인쇄] p.4020 |
| 대칭 | 같은 구 두 개의 법선 접촉 = 구 하나 ↔ 마찰 없는 강체 평판 (대칭) | [인쇄] p.4020 |
| 재료 | E = 7.0 × 10¹⁰ N m⁻² · ν = 0.3 · σ_Y = 1.0 × 10⁸ N m⁻² · *"The perfectly plastic material model was selected"* · von Mises | [인쇄] p.4021 · `txt_p10_…` |
| P_Y | **36.4 N** (본문) · 그림 12 · 17 은 **36.45 N** · 식 (3.7) 재계산 36.447 N [재현] | [인쇄] p.4021 · 그림 12 · 17 |
| A_Y(ν) | **A_Y(0.3) ≈ 1.61** — Hertz 응력장에서 J₂ 가 가장 큰 점에 von Mises (각주 p.4031) → (σ_Y)_Th = 1.61σ_Y (= 항복 시작 때 최대 접촉압 p₀ · Johnson 1985 p.155 인용) | [인쇄] p.4019 · p.4031 |
| 하중 경로 | ABC (P_max 500 N) · ADE (1000 N) · AFG (1500 N) — 시간축 t 는 0 → 4 (단위 없음 · 그림 7) | [인쇄] 그림 7 |
| 모델 상수 | **C_a = 2.33 × 10⁻⁷** (인쇄 단위 'N m⁻¹' — 식 2.5 로는 m N⁻¹ · §3-8) · 최소제곱 맞춤 · **K_c = 2.69 × 10⁻⁴ N⁻¹** (FEA 에서 · 자세한 것은 Vu-Quoc et al. 1999a) | [인쇄] p.4027 · p.4029 |
| 충돌 | ρ 2.699 × 10³ kg m⁻³ → m = **11.306 kg** · Δt = **1.0 × 10⁻⁶ s** · leap-frog · 뉴턴 허용 **0.005** (상대 증분) · 반복 최대 **2** · v_in 0.02–0.20 m s⁻¹ (10 점 [판독]) · v_Y = 1.67 × 10⁻³ m s⁻¹ (식 1.12) → v_in/v_Y 12–120 · 같은 구 두 개면 2v_Y ≃ 3.34 × 10⁻³ | [인쇄] p.4036–4040 · 각주 p.4040 |

### 3-2. 탄성 검증 (그림 8 · 9 · §2(a))

- AFG 경로를 **항복 없이** 풀어 Hertz (1.6)–(1.8) 과 대조: *"Our FEA results showed excellent agreement"* (p.4022).
- 1500 N 에서 Hertz 반지름 **a_Hz = 1.14 × 10⁻³ m** ↔ FEA **[1.13, 1.17] × 10⁻³ m** · 차이 **< 2.7 %** · 중심 (r = 0) 에서 FEA 압력이 뚝 떨어지는 것은 *"numerical characteristics of the finite-element modelling of our axisymmetric problem"* 탓으로 돌림 (p.4022) · Hertz p₀ ≈ 5.6 × 10⁸ N m⁻² [판독 그림 8 · 카드 산술 식 1.6 = 5.56 × 10⁸].
- 그림 9: a(P) 적재 · 제하 모두 Hertz 와 맞음 (탄성이면 제하가 같은 길).

### 3-3. ★ 탄소성 FEA (그림 10 · 11 · 12 · §2(b) · (c))

- **P–α (그림 10)**: P < P_Y 는 Hertz 와 같고, P > P_Y 의 곡선은 **직선이 아니다** (p.4023 (i) (ii)) · 모두 Hertz 아래 (같은 α 에서 FEA 가 무르다) — α 1.56 × 10⁻⁵ m 에서 FEA 1500 N ↔ Hertz 1998 N · α 1.14 × 10⁻⁵ m 에서 1000 ↔ 1248 N [카드 산술 식 3.10].
- **반발계수 (식 2.1 = 면적비의 제곱근)**: e_ABC **0.841** · e_AFG **0.737** (*"14 % decrease"*) [인쇄 p.4024] · e_ADE **0.776** [인쇄 · 그림 10 범례만] — *"The higher the maximal normal force, the smaller the corresponding coefficient of restitution."*
- **최대 변위** [판독 그림 10 · α_max 점선을 직선 맞춤해 P = 0 틀 높이에서 읽음 · 13 쪽 스캔 전단 때문]: ABC **6.79 × 10⁻⁶** (틀 전단 기울기를 강제하면 6.77) · ADE 1.140 × 10⁻⁵ · AFG 1.559 × 10⁻⁵ m — 뒤 둘은 본문 p.4034–4035 의 α_max 1.14 · 1.56 × 10⁻⁵ 와 맞아 판독 검증이 된다 · ABC 값은 원문에 인쇄 안 됨 → α/α_Y ≈ 6.3 · 10.5 · 14.4 [카드 산술 · α_Y = 1.081 × 10⁻⁶ m].
- **★ 잔류 변위 (하중 0 마지막 점)** [판독 · digitized.csv · 원 래스터에서 P = 0 틀선 위에 걸친 표지의 x 중심]: ABC **2.01 × 10⁻⁶** · ADE **4.55 × 10⁻⁶** · AFG **7.09 × 10⁻⁶ m** (그림 16 의 같은 런 7.08 × 10⁻⁶ — 두 그림이 맞음) → 되돌아온 몫 (α_max − α_res)/α_max ≈ **0.70 · 0.60 · 0.55** [카드 산술] — 원문 본문에는 잔류 변위 숫자가 **없다**.
- **압력 분포 (그림 11)**: 세 힘 모두 **평평한 꼭대기 (σ_z)_max ≃ 2.25 × 10⁸ N m⁻² > 2.00σ_Y** [인쇄 p.4024] (그림에선 ABC ≈2.1–2.2 · ADE ≈2.3 · AFG ≈2.4 × 10⁸ 쯤 [판독 · 거칠게]) · *"the maximum normal stress is, however, not fixed, and is much larger than predicted by Thornton (1997)"* (p.4024–4025) · Hertz 최대압보다는 늘 낮다 → **a_Th > a_FE > a_Hz** (식 2.2).
- **접촉 반지름 (그림 11)** [판독 · 표지 잉크 중심 · 14 쪽은 기울기 없음 · Hertz 곡선의 p = 0 점 0.786 · 0.991 · 1.134 × 10⁻³ = 식 (1.7) 과 ±0.0013 × 10⁻³ (보정 확인)]: FEA 반지름은 마지막 p > 0 절점과 첫 p = 0 절점 사이 = **0.885–0.921 · 1.213–1.253 · 1.449–1.497 × 10⁻³ m** (500 · 1000 · 1500 N) ↔ Hertz 0.787 · 0.992 · 1.135 × 10⁻³ [카드 산술 식 1.7] ↔ 모델 a^ep 0.895 · 1.216 · 1.476 × 10⁻³ [카드 산술 식 2.3 · 2.5] = **세 구간 모두 안** (맞춘 것이니 당연) · FEA 평균압 P/πa² = 1.88–2.03 · 2.03–2.16 · 2.13–2.27 σ_Y [카드 산술] · 마지막 p > 0 절점의 압력 ≈ 0.91 · 1.02 · 1.55 × 10⁸ N m⁻² [판독].
- **소성 반지름 a^p(P) (그림 12 · AFG)**: 적재 중 P > P_Y 에서 *"approximately linear"* · 제하 중 *"mostly constant during much of the unloading phase"* (p.4026) — 그림에서 FEA 제하 점 (∘) 은 P_max 근처 (P ≈ 1490 N · ∘ 와 + 가 겹친 무리) **3.21 × 10⁻⁴ m** → 제하 중간 (P ≈ 654 · 750 N) **4.34 × 10⁻⁴** 로 오히려 오르고 → 마지막 점 (P ≈ 15 N) **2.12 × 10⁻⁴** 로 떨어진다 [판독 · 표지 잉크 중심 · 1 눈금 = 1 × 10⁻⁴ 로 읽음 · §3-8 축 라벨 주의 · 15 쪽 전단으로 P ±5 N] ↔ 모델 (3.20) 은 3.41 × 10⁻⁴ 고정 → 제하 대부분에서 ±30 % 안 · 끝에서 −38 % = '제하 중 a^p 고정' 은 FEA 의 근사 [카드 산술].
- ★ **재료는 완전소성인데 접촉은 경화처럼 군다**: *"even though elastic–perfectly plastic material is used in our FEA, the resulting behaviour of the contact radius, when decomposed into an elastic part and a plastic part, behaves in a similar manner to an elastic–plastic material with hardening. The reason is certainly due to the influence of the mechanics of contact and the spherical geometry on top of the material behaviour."* (p.4023) — 그래서 식 (3.2) (선형 등방 경화) 와 식 (2.5) 를 짝짓는다 (그림 13 ↔ 14).

### 3-4. ★ 모델 대 FEA (그림 16 · 17 · §3(c))

| 경로 | 지표 | FEA | 이 모델 | Thornton (1997) | 표지 |
|---|---|---|---|---|---|
| AFG (1500 N) | P at α_max ≃ 1.56 × 10⁻⁵ m | **1500 N** | **1495 N** (0.3 %) | **770.5 N** (*"about half"*) | [인쇄] p.4034 · [재현] 1495.3 · 770.8 |
| AFG | e | **0.7372** | **0.7541** (2.3 %) | **0.5641** (≈23.5 %) | [인쇄] p.4034–4035 |
| ADE (1000 N) | P at α_max ≃ 1.14 × 10⁻⁵ m | **1000 N** | **962.1 N** (3.8 %) | **559.6 N** (44 %) | [인쇄] p.4035 · [재현] 959.1 · 558.4 |
| ADE | e | **0.7757** | **0.7994** (3.1 %) | **0.6091** (≈22 %) | [인쇄] p.4035 |
| ABC (500 N) | — | *"Similar results"* (Zhang 1998) | — | — | [인쇄] p.4035 · 숫자 [미확인] |
| AFG | 잔류 α (P = 0) | ≈ 7.09 × 10⁻⁶ m [판독] | 6.37 × 10⁻⁶ (−10 %) [재현] | 9.58 × 10⁻⁶ (+35 %) [카드 산술 · TN98 식 28] | 원문 숫자 없음 |
| ADE | 잔류 α | ≈ 4.55 × 10⁻⁶ [판독] | 3.74 × 10⁻⁶ (−18 %) | 6.30 × 10⁻⁶ (+39 %) | 같은 |
| ABC | 잔류 α | ≈ 2.01 × 10⁻⁶ [판독] | 1.48 × 10⁻⁶ (−26 %) (α_max 6.79 × 10⁻⁶ [판독] 입력 · P_max 468 N) | 2.95 × 10⁻⁶ (+47 %) (P_max 325 N) | 같은 |

- 비교 방법: FEA 는 **힘 구동** (힘 경로 입력 → 변위 출력) · 그 변위 α_FE 를 **변위 구동** 두 모델 (MATLAB) 에 넣어 P 를 계산 (p.4033–4034 · `txt_p22_p23_…`).
- 그림 16 의 모델 제하 곡선은 FEA 마지막 변위 (7.09 × 10⁻⁶ m) 에서 P ≈ 30–35 N 으로 끝난다 [판독] — 모델의 α_res (6.37 × 10⁻⁶) 가 더 작아 아직 닿아 있기 때문 [재현 · 그 α 에서 모델 P 32.5 N].
- **그림 17** (모델 a^ep · a^e · a^p vs P): a^e = Hertz (1.7) · a^p = (2.5) · a^ep = 합 · 1500 N 에서 a^p 일점쇄선 ≈ 3.38 × 10⁻⁴ m [판독] = C_a × (1500 − 36.45) = 3.41 × 10⁻⁴ [카드 산술] (그림 12 와 달리 인쇄 C_a 와 맞음 · §3-8).
- ⚠ **표본 밖 검증이 아니다**: C_a = *"least-square fit of the FEA results"* (그림 12 = AFG) · K_c = *"For the contact problems presented in § 2 b, the value of K_c extracted from the FEA results"* (세 경로 모두 §2(b)) → AFG · ADE 비교는 맞춘 자료 위의 재현이다 [카드 추론].

### 3-4b. ★ FEA 기준 자체의 독립 대조 — Kogut–Etsion 2002 (ANSYS) 의 맞춤식 [다른 카드 식 · 카드 산술]

이 논문의 FEA 를 다른 코드의 같은 문제 (탄성–완전소성 구 ↔ 마찰 없는 강체 평판 · 작은 변형) 와 견준다 — `kogutetsion2002_ep_sphere_rigid_flat` 의 식: ω_c = (πKH/2E)²R · K = 0.454 + 0.41ν · H = 2.8Y · P_c = (4/3)ER^(1/2)ω_c^(3/2) · 6 ≤ ω/ω_c ≤ 110 에서 P/P_c = 1.40(ω/ω_c)^1.263 (eq8) · p/Y = 1.61(ω/ω_c)^0.117 (eq6) · A/A_c = 0.94(ω/ω_c)^1.146 (eq8) — 그 카드 §3.  구 ↔ 평판이면 ω = 이 논문의 α (같은 구 두 개의 '접근의 반').
- 항복 시작 정의가 같다: KE 의 K·H (ν 0.3) = **1.616 Y** ↔ 이 논문 A_Y(0.3) ≈ **1.61** (식 3.7 각주 · J₂ 최대점 von Mises) → ω_c = 1.088 × 10⁻⁶ m ↔ α_Y 1.081 × 10⁻⁶ · P_c 36.8 ↔ P_Y 36.4 N.
- 같은 α_max 에서 KE 식의 힘: ABC (α 6.79 × 10⁻⁶ [판독] · ω/ω_c 6.24) **521 N** (FEA 500 · +4 %) · ADE (1.140 × 10⁻⁵ · 10.5) **1002 N** (1000 · +0.2 %) · AFG (1.559 × 10⁻⁵ · 14.3) **1488 N** (1500 · −0.8 %).
- 같은 자리의 평균압 p/Y = **2.00 · 2.12 · 2.20** ↔ 이 논문 FEA (그림 11 절점 구간) 1.88–2.03 · 2.03–2.16 · 2.13–2.27 σ_Y = 세 구간 모두 안 · 면적 몫 A/(πRω) = 1.23 · 1.33 · 1.39 ↔ FEA a²/(Rα) 1.15–1.25 · 1.29–1.38 · 1.35–1.44 = 모두 안.
- ⇒ ABAQUS 5.4 (이 논문) 와 ANSYS 5.7 (KE · 맞춤식) 두 FEM 이 같은 무차원 깊이에서 힘 4 % · 평균압 · 면적 구간 안에서 맞는다 → **'Thornton 꼴은 너무 무르다' 의 FEA 기준은 한 코드의 인공물이 아니다** (실험 검증은 아님 · 둘 다 마찰 없음 · 탄성–완전소성 · 작은 변형).  그리고 KE 식으로도 평균압은 이 범위에서 1.61Y 캡보다 1.24–1.37 배 높다 (ω/ω_c 110 에서 2.79 ≈ 2.8Y 로 간다 — 그 카드).

### 3-5. ★ Thornton (1997) 가 왜 절반인가 — 접촉 면적과 평균압의 두 몫 [카드 산술 · 원문 숫자 + 그림 11 판독]

원문 진단 = (a) 압력 캡이 너무 낮다 (FEA 꼭대기 2.25 × 10⁸ > 1.61σ_Y = 1.61 × 10⁸ N m⁻² · p.4024–4025) (b) 접촉 반지름 · 곡률 (식 2.2 · 3.3).  같은 α 에서 힘 비를 정확히 세 인자로 나눌 수 있다 (항등식 · p̄ = P/πa² · Thornton 소성 가지 P_Th = P_Y + πp_yR(α − α_Y) · 구 ↔ 평판 R* = R):

**P/P_Th = [a²/(Rα)] × [p̄/p_y] × [πp_yRα/P_Th]** (면적 몫 × 평균압 몫 × Thornton 가지 상수항 몫)

| α (경로) | 쪽 | 면적 몫 a²/(Rα) | 평균압 몫 p̄/p_y (p̄/σ_Y) | 상수항 몫 | 곱 ↔ 힘 비 |
|---|---|---|---|---|---|
| 1.56 × 10⁻⁵ m (AFG) | FEA (a = 1.449–1.497 × 10⁻³ [판독]) | 1.35–1.44 | 1.41–1.32 (2.27–2.13) | 1.024 | 1.946 ↔ 1500/770.5 = 1.947 |
| 같은 | 모델 (a^ep · 식 3.5 에서 = C_R) | 1.39 | 1.36 (2.19) | 1.024 | 1.940 ↔ 1495/770.5 |
| 1.14 × 10⁻⁵ m (ADE) | FEA (a = 1.213–1.253 × 10⁻³ [판독]) | 1.29–1.38 | 1.35–1.26 (2.16–2.03) | 1.033 | 1.791 ↔ 1000/559.6 = 1.787 |
| 같은 | 모델 | 1.25 | 1.33 (2.15) | 1.033 | 1.718 ↔ 959/558 |

- ⇒ Thornton 의 '절반' = **넓어진 접촉 (곡률 평평해짐 · ×1.3–1.4) 과 높은 평균압 (×1.3–1.4) 이 거의 반반** — 둘 다 단일 접촉의 기하 · 재료 문제이지 다접촉 효과가 아니다 [카드 추론].  ⚠ 원문의 '평평한 꼭대기 2.25 × 10⁸' 은 최대값이지 평균이 아니다 — 2.25/1.61 × C_R (= 1.398 × 1.394 = 1.948) 이 1.947 과 맞는 것은 우연 (평균압은 2.13–2.27 σ_Y) 이라 그 꼴로 쓰지 않는다.
- Thornton 직선 기울기 πp_yR* = 5.06 × 10⁷ N/m [카드 산술] — 모델의 큰 힘 쪽 점근 기울기 K_cR/C_a² ≈ 5.0 × 10⁸ N/m (§0 ①) 의 1/10 (외삽 쪽에서는 두 법칙이 더 벌어진다).  `varkey2026_…` 가 적은 *"Thornton–Ning 단독은 고밀도서 FEM 을 UNDER-predict"* [다른 카드] 의 적어도 일부는 **이미 단일 접촉에서** 생긴다는 뜻 (재료 · 크기가 달라 크기는 못 옮긴다).

### 3-6. ★ 제하 · 잔류 · 되돌아옴 [재현 · 판독 · 카드 산술]

| 정적 한 주기 (식 2.3 · 2.5 · 3.5 · 3.19) | 500 N | 1000 N | 1500 N |
|---|---|---|---|
| a^e (1.7) [m] | 7.870 × 10⁻⁴ | 9.916 × 10⁻⁴ | 1.135 × 10⁻³ |
| a^p (2.5) [m] | 1.080 × 10⁻⁴ | 2.245 × 10⁻⁴ | 3.410 × 10⁻⁴ |
| C_R (3.6) | 1.125 | 1.259 | 1.394 |
| α_max (3.5) [m] | 7.12 × 10⁻⁶ | 1.175 × 10⁻⁵ | 1.563 × 10⁻⁵ |
| α_res (3.19) [m] | 1.62 × 10⁻⁶ | 3.94 × 10⁻⁶ | 6.39 × 10⁻⁶ |
| 되돌아옴 (α_max − α_res)/α_max | 0.77 | 0.67 | 0.59 |
| 평균 접촉압 P/π(a^ep)² ÷ σ_Y | 1.99 | 2.15 | 2.19 |

- 제하 힘은 (3.21)+(3.22) 를 합치면 **P = [4E C_R(P_max)^(3/2) R^(1/2) / (3(1 − ν²))] (α − α_res)^(3/2)** [카드 산술] — 원래 Hertz 강성의 C_R^(3/2) 배 (1500 N 에서 1.65 배).  식 (3.22) 가 a^e 에서 힘을 낼 때 원래 R 을 쓰기 때문이다 — 곡률 반지름 C_R R 을 쓴 '일관된' Hertz 제하 (Thornton 꼴 · 반지름 R_p) 라면 배수는 C_R^(1/2) (1500 N 1.18) 이라 이 모델의 제하가 C_R 배 더 가파르다 [카드 산술 · 원문은 이 차이를 말하지 않음].
- 잔류 접촉 반지름 (P → 0) = a^p_max (식 3.20) = 3.41 × 10⁻⁴ m (1500 N) [카드 산술] · 원문 그림 14 의 a_res.
- 분리: *"when P is decreasing and reaches zero, the sphere is considered separated from the surface. Consequently, P is then set to be zero thereafter, even though the normal displacement may not be zero"* (p.4037).
- **재재하 가지는 없다** — 알고리즘 3.2 는 Δα > 0 이면 언제나 처녀 적재식 (줄 9–21) 을 쓴다 → 부분 제하 뒤 다시 누르면 힘이 처녀 곡선으로 튄다 [카드 추론 · 원문 언급 없음].

### 3-7. ★ 충돌 모의 (그림 19 · 20 · §4) — 재현과 범위

| v_in [m/s] | v_in/v_Y | 이 모델 e [재현] | 판독 (그림 20b) | P_max [N] · P/P_Y [재현] | Thornton e [재현] = 식 (1.11) | 판독 |
|---|---|---|---|---|---|---|
| 0.02 | 12.0 | 0.838 | 0.838 | 635 · 17 | 0.631 | 0.631 |
| **0.04** | 24.0 | **0.759** (인쇄 0.7587) | 0.759 | **1433** (인쇄 1435) · 39 | **0.533** (인쇄 0.5331) | 0.533 |
| 0.06 | 35.9 | 0.701 | 0.701 | 2337 · 64 | 0.482 | 0.482 |
| 0.08 | 47.9 | 0.654 | 0.654 | 3330 · 91 | 0.449 | 0.449 |
| 0.10 | 59.9 | 0.615 | 0.614 | 4396 · 121 | 0.425 | 0.425 |
| 0.12 | 71.9 | 0.580 | 0.580 | 5522 · 152 | 0.406 | 0.406 |
| 0.14 | 83.8 | 0.550 | 0.550 | 6697 · 184 | 0.391 | 0.391 |
| 0.16 | 95.8 | 0.523 | 0.523 | 7912 · 217 | 0.378 | 0.378 |
| 0.18 | 107.8 | 0.499 | 0.499 | 9159 · 251 | 0.367 | 0.367 |
| 0.20 | 119.8 | 0.478 | 0.477 | 10 431 · 286 | 0.358 | 0.358 |

- 인쇄값 (v_in 0.04): v_out −0.0304 (이 모델) · −0.0214 (Thornton) · e 0.7587 · 0.5331 · P_max 1435 · 957 N · 접촉 시간 τ_ep ≃ 1.00 × 10⁻³ s · τ_Th ≃ 1.20 × 10⁻³ s (p.4038–4039) ↔ [재현] v_out 0.0304 · 0.0214 · P_max 1433 · 956 N · τ 1.003 · 1.214 × 10⁻³ s · 뉴턴 최대 2 회 (0.20 m/s) — **전부 맞는다** (`--selftest` 15/15).
- ★ **맞춘 범위 밖**: 두 상수는 P ≤ 1500 N (P/P_Y ≤ 41) FEA 에 맞췄는데, 0.06 m/s 위 충돌은 P_max **2.3 × 10³ – 1.04 × 10⁴ N** (P/P_Y 64–286) [재현] — 그림 20 의 대부분은 **외삽** 이다 (원문 언급 없음) [카드 추론].
- 원문 결론: *"Since (i) both models are quasi-static models, and (ii) quasi-static FEA results agree with the proposed elastoplastic NFD model, while the Thornton (1997) NFD model produces softer P–α relations in all tests, the proposed NFD model is the more accurate and reliable of the two."* (p.4040) — 충돌 실험 (측정 e) 과의 대조는 **없다**.
- 접촉 시간 차 (Remark 4.1 · 식 4.9): 2mv_in = P̄_Th τ_Th = P̄_ep τ_ep (*"Assume that we are working with linear models to simplify the discussion"*) → Thornton 이 무르니 평균 힘이 작고 시간이 길다.
- Remark 4.2 (식 4.10 · 그림 21): *"It is not guaranteed that an NFD model that produces an acceptable coefficient of restitution e can produce an accurate NFD relationship … Hence, it is not sufficient to use the coefficient of restitution to compare the accuracy of NFD models. A combination of both NFD relationship and coefficient of restitution is necessary"* (p.4040).

### 3-8. 원문 안 어긋남 (인쇄 그대로 · 고치지 않음)

1. **C_a 단위**: *"C_a = 2.33 × 10⁻⁷ N m⁻¹"* (p.4027) ↔ 식 (2.5) a^p (m) = C_a⟨P − P_Y⟩ (N) → m N⁻¹ 이어야 한다 · 재현은 m/N 로 원문 모든 수를 낸다.
2. **식 (3.17)** 둘째 항 *"(1/3)c₁(P_n^(i−1))(P_n^(i−1))^(−2/3)"* 에 P 가 한 번 더 붙음 — (3.15) 의 미분은 (1/3)c₁P^(−2/3) · 해에는 영향 없음 (뉴턴 수렴만).
3. **식 (4.7)** 둘째 꼴이 **loading 합 / unloading 합** (첫째 꼴 unloading / loading 의 역수) 이고 사다리꼴 첨자도 (α_i − α_(i−1))(P_i + P_(i+1)) 로 한 칸 어긋남 · 본문은 (4.6) · (4.7) 이 같은 수를 냈다고만 적음 (p.4038).
4. **그림 12 세로 눈금 라벨**: '4 × 10⁻⁴' 는 0 에서 넷째 눈금 · '−2 × 10⁻⁴' 는 아래 둘째 눈금인데 '2 × 10⁻⁴' 가 **첫째** 눈금에 있다 (다른 둘은 1 눈금 = 1 × 10⁻⁴) · 1 × 10⁻⁴ 로 읽으면 모델 직선 기울기 ≈ 2.5 × 10⁻⁷ m/N · 제하 점선 ≈ 3.70 × 10⁻⁴ m 로 인쇄 C_a 식보다 ≈ 8 % 높다 [판독] — 그림 17 (같은 모델) 은 인쇄 C_a 와 맞음 (3.38 × 10⁻⁴).
5. **알고리즘 3.3** 은 *"while F(P_n^i) > Tol"* (잔차) 로 도는데 p.4038 의 판정은 상대 증분 (식 4.8) · P_Y 는 본문 36.4 N · 그림 36.45 N.
6. 그림 20b 범례 *"v_Y ≃ 1.67 × 10⁻³"* · 캡션 = 식 (1.12) · 재현 1.6697 × 10⁻³ (맞음).

## 4. ★ 방법

### 4-1. FEA (§2) — 무엇을 풀었나

- 탄성–완전소성 (von Mises) 알루미늄 합금 구 (R 0.1 m) 를 **마찰 없는 강체 평판** 에 힘 경로 ABC · ADE · AFG 로 눌렀다 뗌 (힘 구동 · 30 단계 넘게) — 같은 구 두 개의 법선 접촉과 대칭으로 같음.
- 출력 = 접촉 반지름 a^ep(P) (적재 · 제하) · 압력 분포 p(r) · P–α.  큰 변형 (기하 비선형) 설정 · 해석 시간은 적혀 있지 않다 [미확인].
- 쓰임 둘 (p.4014–4015): *"1. To observe the behaviour of the contact radius under elastoplastic contact, and from that observation, to help create a model by introducing the additive decomposition of the contact radius and by generalizing Hertzian contact mechanics to account for plastic deformation … 2. To obtain the values of the model parameters for a specific material and geometry of a particle."*

### 4-2. ★ 모델 식 (식 번호마다 크롭 · 위에서 아래로 계산 사슬)

**Hertz (§1(a))**: E* := [(1 − ((i)ν)²)/(i)E + (1 − ((j)ν)²)/(j)E]⁻¹ (1.1) · R* := (1/(i)R + 1/(j)R)⁻¹ (1.2) · a = (3PR*/(4E*))^(1/3) (1.3) · 2(ij)α = a²/R* = [9P²/(16R*(E*)²)]^(1/3) (1.4) — α 는 두 중심이 다가선 거리의 **반** (각주) · p = p₀[1 − (r/a)²]^(1/2) (1.5) · p₀ = 3P/(2πa²) = [6P(E*)²/(π³(R*)²)]^(1/3) (1.6) · 같은 구: E* = E/2(1 − ν²) · R* = ½R → a = [3PR(1 − ν²)/(4E)]^(1/3) (1.7) · (ij)α = a²/R = [9P²(1 − ν²)²/(16RE²)]^(1/3) (1.8).

**기존 법칙 (§1(b))**: Walton–Braun P = K₁α (적재) · K₂(α − α₀) (제하) (1.9) · e = √(ABC/AOC) = √(K₁/K₂) (1.10) · Thornton e(v_in) (1.11) · v_Y = 3.194[(σ_Y)⁵_Th(R*)³/((E*)⁴m*)]^(1/2) (1.12) · m* = (i)m(j)m/((i)m + (j)m) (번호 없음).

**FEA 정리 (§2)**: e = √(제하 곡선 아래 면적 / 적재 곡선 아래 면적) (2.1) · a_Th > a_FE > a_Hz (2.2) · **a^ep = a^e + a^p** (2.3) · a^p = a^ep − a^e (2.4) · **a^p = C_a⟨P − P_Y⟩ (적재) · C_a⟨P_max − P_Y⟩ (제하)** (2.5) · ⟨x⟩ = 0 (x ≤ 0) · x (x > 0) (2.6).

**연속체 짝 (§3(a))**: ε^ep = ε^e + ε^p (3.1) · ε^p = K⟨σ − σ_Y⟩ (적재) · K⟨σ_max − σ_Y⟩ (제하) (3.2) · **R*_p = C_R(P)R*** (3.3) · 2(ij)α = (a^ep)²/R*_p = (a^ep)²/(C_R(P)R*) (3.4) · (ij)α = (a^ep)²/(C_R R) (3.5) · **C_R(P) = 1.0 (P ≤ P_Y) · 1.0 + K_c⟨P − P_Y⟩ (P > P_Y)** (3.6).

**변위 구동 알고리즘 (§3(b))**: P_Y = π³R²(1 − ν²)²[A_Y(ν)σ_Y]³/(6E²) (3.7) · a_Y = [3P_YR(1 − ν²)/(4E)]^(1/3) (3.8) · α_Y = (a_Y)²/R (3.9) · α_n ≤ α_Y: P_n = [4ER^(1/2)/(3(1 − ν²))] α_n^(3/2) (3.10) · α_n > α_Y: α_n = (a^ep_n)²/(C_R(P_n)R) (3.11) · [1.0 + K_c(P_n − P_Y)]Rα_n = (a^e_n + a^p_n)² (3.12) · {[1.0 + K_c(P_n − P_Y)]Rα_n}^(1/2) = [3R(1 − ν²)/(4E)]^(1/3)P_n^(1/3) + C_a(P_n − P_Y) (3.13) · c₁ := (1/C_a)[3R(1 − ν²)/(4E)]^(1/3) (3.14) · **F(P_n) = (P_n − P_Y) + c₁P_n^(1/3) − (1/C_a){[1.0 + K_c(P_n − P_Y)]Rα_n}^(1/2) = 0** (3.15) · 뉴턴 P_n^i = P_n^(i−1) − F/F′ (3.16) · F′ (3.17 · §3-8 의 2) · 첫 추정 = 앞 두 걸음 외삽 (3.18) · 제하: α_res = α_max − (a^e_max)²/(C_R(P_max)R) (3.19) · a^p_n = a^p_max (3.20) · a^e_n = [C_R(P_max)R(α_n − α_res)]^(1/2) (3.21) · P_n = [4E/(3R(1 − ν²))](a^e_n)³ (3.22).

**알고리즘 3.2 (34 줄 · 크롭 `alg_3_2_…`)**: 자료 R · E · ν · σ_Y → P_Y · α_Y → Δα_n = 0 이면 그대로 · Δα_n > 0 (적재): α_n ≤ α_Y 면 (3.10) · a^p = 0 / α_n > α_Y 면 알고리즘 3.3 (뉴턴) → a^e (1.7) · a^p (2.5) · a^ep (2.3) · Δα_n < 0 (제하): 돌아서는 첫 걸음에 P_max = P_(n−1) · α_max = α_(n−1) · a^p_max · α_res (3.19) 를 정하고 → a^p = a^p_max (3.20) · a^e (3.21) · P (3.22) · a^ep (2.3).  **알고리즘 3.3 (7 줄)**: Tol → P_n^0 (3.18) → F > Tol 동안 (3.16).

### 4-3. 충돌 DEM (§4(a))

- 구 ↔ 마찰 없는 강체 평판 · 법선만 (접선 · 회전 · 중력 없음) · leap-frog: x_n = x_(n−1) + v_(n−1/2)Δt (4.2) · α_n = R − x_n (4.3) · v̇_n = −P_n/m (4.4) · v_(n+1/2) = v_(n−1/2) + v̇_nΔt (4.5) · e := −v_out/v_in (4.6) · 또는 면적비 (4.7) · 뉴턴 판정 (P_n^i − P_n^(i−1))/P_n^i ≤ 0.005 (4.8).
- 대칭: 구 ↔ 평판 = 같은 구 두 개의 상대 속도 2v_in (p.4036).
- 두 모델 다 *"time-independent plasticity"* → *"the similarity between the FD relationships and coefficients of restitution depends only on the maximum value of the normal force, and not the rate of loading and unloading"* (p.4038).

### 4-4. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압 (CURATOR_BRIEF (i)–(iv))

- **(i) DEM 한계 문장 (원문)**: 스프링–대시포트 *"In DEM simulations, however, the energy dissipation in the spring–dashpot model depends, highly on the dashpot coefficient and the relative velocity in a collision. There is no solid basis for obtaining the coefficient of the dashpot for these kinds of NFD models. The dependence of the model on the collision velocity also prevents the use of quasi-static simulation to correctly evaluate the energy dissipation caused by plastic deformation. For the above reasons, the spring–dashpot NFD model is regarded as a primitive NFD model for DEM simulations."* (p.4019) · Walton–Braun *"e is not a material property, but depends on the plastic deformation incurred at impact"* · *"two of the three parameters (e, K₁ and K₂) need to be extracted from experimental data"* (p.4017) · W–B 의 법선 (소성 있음) ↔ 접선 (Mindlin–Deresiewicz 탄성) 이 *"inconsistency"* (p.4017) · Thornton 무검증 (각주 p.4019).  **입자 모양 · 조밀 영역 · 접촉 독립 가정 · 겹침 상한에 대한 말은 없다.**
- **(ii) 소성을 넣기 어려운 이유와 우회 · 비용**: 원문은 '어렵다' 를 따로 논하지 않는다.  우회 = 입자를 강체 구로 두고 **접촉 법칙에** 소성을 넣는다 — FEA 로 본 접촉 반지름을 탄성 + 소성으로 쪼개고 (2.3) 곡률을 고친다 (3.3) · 상수는 재료 · 크기마다 FEA · 실험 (*"the model parameters … are to be measured for different materials and geometry of the particles"* p.4014 · Remark 2.1 · 3.1 · p.4030) · 해석 연결은 *"future publication"* (Remark 2.1) · 비균질 입자 (콩) 는 *"it is impossible to use FEA in this case, since it is very difficult to model accurately the inhomogeneous material inside the particle"* (p.4043) · 비용: FEA 시간 [미확인] · DEM 쪽 = 걸음마다 뉴턴 ≤ 2 회 (p.4038).
- **(iii) 차원**: FEA 축대칭 (3D 구) · 충돌 1 자유도 · 2D → 3D 전이 말 없음 (해당 없음).
- **(iv) 압력을 뺄 때**: 단일 접촉 제하 (힘 → 0) 를 다룬다 — FEA 제하 · 모델 제하 (3.19–3.22) · 잔류 변위 (그림 16 *"residual normal displacement due to plastic deformation"* p.4037) · 다입자 침대의 탈압 · 되돌아옴은 없다.
- **입자 처리 판정**: rigid 구 + **접촉 탄소성 (CONTACT plasticity)** — 곡률 보정 C_R 은 평평해진 접촉면의 **대리** 이고 입자 SHAPE 흐름은 없다 (`thorntonning1998_…` §4 와 같은 층) · 단분산 · 한 입자.

### 4-5. 기법 미니 용어집

- **NFD / TFD** = normal / tangential force–displacement (법선 / 접선 접촉력–변위 법칙).
- **변위 구동 (displacement-driven)** = 입력 변위 α → 출력 힘 P (DEM 걸음마다 필요한 꼴) · **힘 구동 (force-driven)** = 입력 힘 → 변위 (FEA · 짝 논문 1999a).
- **Macaulay 괄호 ⟨x⟩** = max(x, 0) (원문 인쇄 'MacCauley').
- **C_a** = 소성 반지름이 (P − P_Y) 에 비례하는 기울기 · **K_c** = 곡률 반지름 배수 C_R 이 (P − P_Y) 에 비례하는 기울기.
- **A_Y(ν)** = Hertz 응력장의 J₂ 최대점에 von Mises 를 건 '항복 시작 때 p₀ / σ_Y' (ν 0.3 → 1.61).
- **v_Y (yield velocity)** = 그 아래 충돌은 소성이 안 생기는 입사 속도 (식 1.12).
- **e (coefficient of restitution)** = −v_out/v_in = √(돌려받은 일 / 저장된 일).

## 5. Figure set ★

| 그림 | 내용 | 우리가 참고할 점 |
|---|---|---|
| 1 | 두 구 법선 접촉 · 2(ij)α · a | α = 접근의 반 (우리 DEM 겹침 δ = 2α) |
| 2 | Walton–Braun 이중 선형 (K₁ · K₂ · α₀) | 우리 `hooke/hysteresis` 와 같은 계열의 그림 (`luding2008_…`) |
| 3 | Thornton 압력 캡 (σ_Y)_Th | 캡 = 첫 항복 p₀ (1.61σ_Y) — FEA 는 2.25σ_Y |
| 4 | Thornton NFD (직선 소성 가지 · R_p* 제하) | 그림 2 · 16 과 견줄 꼴 |
| 5 · 6 | FEA 모형 (구 ↔ 강체 평판 · 축대칭 메시 · 접촉부 촘촘) | 단위 시험 U1 · U3 의 구성 그림 |
| 7 | 하중 경로 ABC · ADE · AFG | 500 · 1000 · 1500 N |
| 8 | 1500 N 탄성 압력 분포 (FEA ↔ Hertz) | 해상도 검증 (반지름 < 2.7 % · 중심 압력 떨어짐 = 수치 인공물) |
| 9 | 탄성 a(P) (FEA 적재 · 제하 ↔ Hertz) | 같음 |
| ★ 10 | 탄소성 FEA P–α 세 경로 + Hertz · e 0.841 · 0.776 · 0.737 | **잔류 변위 판독 원천** (2.0 · 4.5 · 7.1 × 10⁻⁶ m) · 직선 아님 |
| ★ 11 | 세 힘의 압력 분포 (FEA 평평한 꼭대기 ↔ Hertz) | 평균압 ≈ 2σ_Y · a_FE > a_Hz — Stage-E 면적 판정의 단일 접촉 자료 |
| 12 | a^p(P) FEA (+ 적재 · ∘ 제하) + 모델 (실선 · 점선) | a^p 적재 ≈ 선형 · 제하 중 고정은 근사 · ⚠ 눈금 라벨 (§3-8) |
| 13 · 14 | ε^p–σ (선형 경화) ↔ a^p–P (탄소성 접촉) | 법칙의 착안 (가공 경화 짝) |
| 15 | 소성이 곡률 반지름을 키움 (R → R_p · a^e · a^p · a^ep) | 접촉 평평해짐의 대리 |
| ★ 16 | AFG 변위 이력으로 Hertz · FEA · 이 모델 · Thornton 의 P–α | **'Thornton 은 너무 무르다' 의 그림** (= Morrissey 그림 3.7) |
| 17 | 모델 a^ep · a^e · a^p vs P | 그림 12 와 다른 눈금 — 인쇄 C_a 와 맞음 |
| 18 | 구 ↔ 강체 평판 충돌 개념도 | — |
| 19 (a · b) | v_in 0.04 m/s 의 P(t) · P–α (두 모델) | 재현 표적 (모두 재현) |
| 20 (a · b) | v_out(v_in) · e(v_in/v_Y) 10 점씩 | 판독 40 점 = 재현과 ±0.001 |
| 21 | 다른 법칙 · 같은 e (식 4.10) | 한 숫자 맞춤 ≠ 법칙 검증 |
| 알고리즘 3.2 · 3.3 | 변위 구동 의사 코드 · 뉴턴 | 구현 그대로 (재현 도구) |

## 6. Post-processing ★

- e = √(면적비) (2.1 · 4.7) 또는 속도비 (4.6) — 두 값이 같았다 (p.4038).
- a^p = a^ep(FEA) − a^e(Hertz) 로 FEA 에서 소성 반지름을 뽑아 (2.4) 최소제곱 직선 (C_a) · K_c 도 FEA 에서.
- 압력 분포 · 반지름을 그림으로만 보고 (표 없음) · 수치는 그림 안 글자 (e · P_max).
- 이 카드의 후처리: 원 래스터 판독 67 행 (표지 틀 맞춤 · P = 0 틀선 위 표지 · 잉크 중심 · 점선 직선 맞춤 · 격자선 보정 · 스캔 전단 고려) + 식 재구현으로 원문 인쇄값 15 개를 다시 냄 (`tools/litdb/vuquoc1999_nfd_reproduce.py`).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (우리 수치는 CLAUDE.md · `comparison_vs_ours_DEM.md` 출처)

### 7-1. 비교표

| 항목 | 이 논문 | 우리 | 차이 / 관계 |
|---|---|---|---|
| 접촉 법칙 | 탄소성 NFD (반지름 더하기 + 곡률 보정 · 제하 Hertz 고정 곡률) · 실제 E (70 GPa) | LIGGGHTS `hooke/hysteresis` (적재 k₁ · 제하 k₂ · 잔류 δ₀ · 캡 없음) · E_eff 1.35 GPa (24 → 18 배 연화) [우리] | 우리 = Walton–Braun 계열 (원문이 'e 상수' 로 비판한 꼴) · 이 논문 = 경로 A 쪽 (실제 E + 접촉 소성) |
| 항복 | P_Y (3.7) · 캡 없음 (평균압이 2.0 → 2.2σ_Y 로 오름) | 없음 (DEM) · MPM J2 σ_y 0.30 GPa [우리] | — |
| 보정 | 상수 2 (C_a · K_c) ← 같은 재료 · 크기 FEA | 1 (E_eff ← 300 MPa 기공률) [우리] | R5 (모델마다 맞춤 값 하나) 기준이면 이 법칙은 둘 |
| 범위 | 단일 접촉 · P/P_Y ≤ 41 · δ/d ≤ 1.6 × 10⁻⁴ · a/R ≤ 0.015 | 침대 · δ/d ≈ 7.4–11 % (SE) [우리] | ≈ 470–700 배 깊다 · a/R ≈ 0.3 [카드 산술 a/R ≈ √(δ/d)] |
| 탈압 | 단일 접촉 잔류 · 되돌아옴 0.55–0.70 (FEA) [판독] | 언로딩 키트 (침대) [우리] | 단위 시험 기준 (U3) 으로만 |
| 수송 · 형상 · 다입자 | 없음 | σ 삼중항 · MPM 형상 | frame[5] 의 접촉 법칙 층 한 칸 |

### 7-2. ★ 랩 기준과 나란히 (판정 없이)

랩 표준 (순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³) 옆에 놓을 숫자 = **없다** (기공률 · 밀도 · SE · 분말이 없는 단일 접촉 논문).

### 7-3. 접촉 법칙 층 — 세 꼴 나란히 (같은 단일 접촉)

| 단계 | Walton–Braun / 우리 hooke/hysteresis 계열 | Thornton (1997) · Thornton–Ning (1998) | Vu-Quoc–Zhang (1999) |
|---|---|---|---|
| 처음 적재 | K₁α (선형) | Hertz | Hertz (P ≤ P_Y) |
| 항복 뒤 | (구분 없음) | P = P_Y + πp_yR*(α − α_Y) · p_y = 1.61σ_Y 캡 | F(P) = 0 (3.15) — 반지름 + C_a(P − P_Y) · 곡률 × C_R |
| 제하 | K₂(α − α₀) 선형 | Hertz · 반지름 R_p* | Hertz · 곡률 C_R(P_max)R 고정 · a^p 고정 |
| 잔류 | α₀ (1 − K₁/K₂ 꼴) | α_p (R_p* 에서) | α_res (3.19) |
| 맞춤 값 | 2 / 3 (e · K₁ · K₂) | 0 (σ_Y 만) | 2 (C_a · K_c) + σ_Y |
| FEA 대비 (이 논문) | 비교 안 함 | 힘 ½ · e −22–24 % · 잔류 +35–47 % [카드 산술] | 힘 −0.3 · −3.8 % · e +2.3 · +3.1 % · 잔류 −10–26 % [카드 산술] |

### 7-4. ★ 적용 범위 — 우리 변형 깊이는 이 FEA 의 몇 배인가 [카드 산술]

- 겹침 ÷ 지름: 이 논문 2α/2R = α/R ≤ 1.56 × 10⁻⁴ ↔ 우리 순수 SE (1.35 GPa) ⟨δ⟩ ≈ 11 % of d · 복합 ⟨δ⟩ 0.0739 µm (SE 지름 1 µm 이면 7.4 % · ⟨δ⟩ 이 어느 접촉 종류의 평균인지 · 기준 지름은 [우리] 기록에서 미확인) [우리 · CLAUDE.md E_SE 보정] → **≈ 470–700 배** (δ/d 0.074 · 0.11 기준).
- 무차원 항복 깊이: 식 (1.6) · (1.7) 에서 a_Y/R = π(1 − ν²)A_Yσ_Y/(2E) · α_Y/R = (a_Y/R)² — 이 논문 1.08 × 10⁻⁵ · LPSCl (E 22 GPa · ν 0.36 · σ_y 0.05–0.30 GPa [미확인 · 카드 없음] · A_Y 1.61 (ν 0.3 값 그대로)) **2.5 × 10⁻⁵ – 9.0 × 10⁻⁴** → 우리 α/R ≈ 0.074–0.11 은 α/α_Y ≈ **80 – 4 × 10³** (이 논문 FEA ≤ 14).
- 연화 E 의 효과: α_Y ∝ (σ_Y/E)² → E 를 18 배 낮추면 같은 σ_Y 에서 α_Y 는 ≈ 316 배 [카드 산술 (24/1.35)²] — '연화 E' 와 '실제 E + 접촉 소성' 은 같은 겹침에서 전혀 다른 항복 깊이를 뜻한다 (`thorntonning1998_…` §7.1 경로 A 의 논거와 같은 쪽).
- ⇒ C_a · K_c 를 우리 SE 에 쓰려면 **우리 깊이 (a/R ≈ 0.3) 까지** 새 FEA (또는 MPM 단일 접촉) 가 필요하다 — 이 논문의 작은 변형 FEA 는 그 범위를 다루지 않는다 (`jacksongreen2005_…` : H 가 a/R 에 따라 2.84 → 1σ_y 로 내려감 [다른 카드]).

### 7-5. ★ Stage-E 면적 · 평균압

- 우리 Stage-E 의 면적 사다리 (A_hertz · A_tabor = F/H · A_volume · A_geom) [우리] 에서 이 논문이 주는 것 = 단일 접촉 · 작은 변형의 **FEA 면적**: 1500 N 에서 πa_FE² = 6.60–7.04 × 10⁻⁶ m² [판독 절점 구간] ∋ π(a^ep)² 6.85 × 10⁻⁶ [카드 산술] ↔ Hertz 4.05 × 10⁻⁶ (0.59 배) ↔ F/(3σ_Y) 5.0 × 10⁻⁶ (0.73 배) ↔ Thornton 꼴 F/(1.61σ_Y) 9.3 × 10⁻⁶ (1.36 배) [카드 산술].
- 평균압 (모델) 1.99 → 2.19σ_Y (P/P_Y 14 → 41) · FEA 절점 구간 1.88–2.27 σ_Y [판독] · `kogutetsion2002_…` eq6 로 같은 깊이 2.00 · 2.12 · 2.20 (§3-4b) [다른 카드 식] — KE 의 첫 항복 1.0–1.08Y → 완전소성 2.8Y (ω/ω_c ≈ 110) 사이 '탄소성 2단'.  우리 깊이 (α/α_Y ≈ 80 – 4 × 10³) 는 대부분 KE 의 완전소성 진입 (110) 근처나 그 위 → ≈ 2.8σ_y 쪽 또는 a/R 이 커지며 평균압이 내려가는 쪽 (`jacksongreen2005_…` eq 17 H_G/σ_y = 2.84[1 − exp(−0.82(a/R)^(−0.7))] → 우리 a/R 0.26–0.33 이면 2.36–2.49 [다른 카드 식 · 카드 산술]) 이 맞을 것 [카드 추론] — Tabor H ≈ 3σ_y 는 이 논문 범위에선 면적을 ≈ 27 % 작게 본다 [카드 산술].

### 7-6. ★ 탈압 · 되돌아옴 (언로딩 키트 · 단계 6)

- 단일 접촉 되돌아옴 몫 = E/σ_Y · ν · P/P_Y 의 함수 [카드 추론 · 차원 해석 — 탄성–완전소성 · 작은 변형이면 길이 척도는 R 하나] — 이 논문 (E/σ_Y 700) FEA 0.55–0.70 [판독 · 카드 산술] · 모델 0.59–0.78 · Thornton 0.39–0.57.
- 우리 MPM 챔피언 (E 1.53 · σ_y 0.30 · ν 0.49 [우리] · ⚠ 우리 σ_y 는 Hencky 편차 변형 문턱이라 문헌 일축 항복과 그대로 견주지 않는다 [우리 · SELF-160]) 은 E/σ_y ≈ 5 → 식 (3.9) 꼴로 α_Y/R ≈ 0.14 (A_Y(0.49) [미확인] 자리에 1.61 그대로) [카드 산술 · 어림] — 단일 접촉 기준으로 **항복 전 탄성 겹침이 실제 LPSCl (α_Y/R 2.5 × 10⁻⁵ – 9 × 10⁻⁴) 의 100 배 이상** → 탈압 때 탄성 되돌아옴이 부풀 수 있다 [카드 추론 · 시험 전] → 언로딩 키트 · MPM 탈압 결과를 실측 되돌아옴 (`miss2026_insitu_conductivity_porosity_pressure_compaction` 300 MPa 에서 놓았을 때 다이 안 두께 회복 SE (Li₅.₅PS₄.₅Cl₁.₅ 단일상) 1.6 % · pc-NMC622 7.9 % [다른 카드 · 그 카드의 재계산 값 · 단계마다 놓았다 다시 누른 이력]) 과 견줄 때 **연화 E 의 몫을 먼저 따로 적는다**.

### 7-7. frame[5] — 어느 반쪽인가

- 이 논문 = DEM 의 **접촉 법칙 층** (단일 접촉 역학) 만 — 수송 · 충전 · 형상 · 다입자 0.  MPM (형상 소성) 과 겹치는 곳은 '단일 접촉의 소성' 하나이고, 그것도 입자를 구로 둔 대리.
- frame[4]: 이 법칙은 **FEA 에 맞추고 같은 FEA 로 확인** 했다 — 실험 대조 (충돌 측정 e · 실측 P–α) 는 짝 논문 (Zhang & Vu-Quoc 1999) 몫이고 이 논문에 없다.

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나

| 이름 | 주는 것 | 못 주는 것 |
|---|---|---|
| 단계 0 | Remark 4.2 · 식 4.10 · 그림 21: **한 숫자 (e · 한 점 기공률) 맞춤 ≠ 법칙 검증** → 결과 전 대조 항목은 곡선 (P–α · σ–ε · 적재 + 제하) 으로 등록 | 기공 연산자 · 판정값 |
| 단계 1 | — | 메모리 · 장 수 |
| 단계 2 | 단위 시험 표적 하나: 탄소성 구 ↔ 강체 평판 (마찰 없음 · E/σ_Y 700 · ν 0.3) 의 P–α · a(P) · p(r) · 잔류 — 그림 판독 67 행 + 재구현 | 표 형태의 FEA 원자료 (Zhang 1998 [미확인]) |
| 단계 3 | 강체 판 경계 (마찰 없음) 아래 단일 입자 P(α) 기준 — 한 속도장 ↔ 입자별 장의 판 힘을 견주기 전 '단일 입자 + 판' 이 Hertz (P < P_Y) · FEA (P > P_Y) 를 내는지 | 다입자 · 입자끼리 접촉 |
| 단계 4 | 항복 시작 깊이 공식 α_Y/R = [π(1 − ν²)A_Yσ_Y/(2E)]² — LPSCl 이면 2.5 × 10⁻⁵ – 9.0 × 10⁻⁴ [카드 산술] → 300 MPa 압밀의 SE 접촉은 모두 깊은 소성 (α/α_Y ≈ 80 – 4 × 10³) — 탄성 접촉 법칙으로는 형상 · 면적이 안 나온다는 R6 의 단일 접촉 근거 | 기공률 · σ_y 값 · 실험 기준 |
| 단계 5 | — | 복합 · 하중 분담 |
| 단계 6 | 단일 접촉 제하 법칙 꼴 (Hertz + 고정 곡률 · 고정 a^p) · 잔류 · 되돌아옴 몫 (FEA 0.55–0.70) · MPM 연화 E 가 되돌아옴을 부풀릴 수 있다는 어림 (§7-6) | 침대 탈압 · 우리 깊이의 되돌아옴 |
| 단계 7 | 접촉 면적 법칙 a^ep = a^e + C_a⟨P − P_Y⟩ (작은 변형) · 평균압 ≈ 2σ_Y — Stage-E 면적의 단일 접촉 대조 | 우리 깊이의 면적 · 수송 |
| 후보 D0 | 우리 `hooke/hysteresis` 와 같은 계열 (W–B 이중 선형) 에 대한 원문 비판 둘 (e 속도 무관 · 매개변수 실험 필요) · 준정적 압밀에선 e 자체보다 **P–α 꼴** 이 문제 | 우리 연화 E 의 근거 |
| 후보 A′-0 | 마찰 없는 강체 평판 · 분리 규칙 (P → 0 이면 이후 0 · 잔류 변위 있어도) — A′-0 판 경계의 단일 접촉 기준 | 미끄럼 |
| 후보 A · A′ | (반대 기하) 강체 AM 이 무른 SE 를 누르는 것과 '무른 구 ↔ 강체 평판' 은 Hertz 영역만 같다 · 다물체 없음 | 값 |
| 후보 B | 입자별 FE 비용 단서: 접촉 반지름당 ≈ 48 요소 · 한 주기 > 30 단계 · 접촉부만 촘촘 (그림 6) · 비균질 입자엔 FE 불가 (p.4043) | 계산 시간 [미확인] |
| 후보 C | MDR 류 큰 변형 법칙의 필요성 (이 법칙은 a/R ≤ 0.015 에서만 검증) | — |
| ★ 후보 C′ | Thornton 꼴 p_y 캡이 단일 접촉에서 힘 ½ · 그 결손 = 넓어진 접촉 (×1.3–1.4) × 높은 평균압 (×1.3–1.4) 이 거의 반반 (§3-5) · 대안 = 상수 2 (C_a · K_c) 를 FEA 로 · 구현 = 걸음당 뉴턴 ≤ 2 · 재재하 가지 · 우리 깊이 검증 · 재료 전이 없음 | LPSCl · NCM 상수 |
| 후보 M0 | — | — |
| U0 | — | — |
| ★ U1 | 단일 입자 압축 (강체 판) 의 기준 곡선 + 해상도 규칙 (접촉 반지름당 ≈ 48 요소 → 탄성 반지름 < 2.7 % · 중심 압력 인공물) → MPM 이면 접촉 반지름을 몇 셀로 푸는지 먼저 적는다 (지름 30 셀 · a/R 0.3 이면 a ≈ 4.5 셀 [카드 산술]) | MPM 해상도 값 |
| U2 | — (마찰 없음) | 경사면 마찰 |
| ★ U3 | 기하는 반대 (무른 구 ↔ 단단한 평판) 이나 같은 양: 분리 · 잔류 변위 · 되돌아옴 몫 · 잔류 접촉 반지름 (a^p_max) 을 E/σ_Y · P/P_Y 에 묶은 기준값 | 강체 구 ↔ 소성 블록 값 |
| U4 | 분리 판정 (P → 0 이면 이후 0) | 판 분리 힘 |
| ★ U5 | 같은 구 두 개 충돌 = 구 ↔ 평판 (대칭 · 상대 속도 2v_in · 2v_Y 3.34 × 10⁻³) 의 e(v_in) 10 점 (재현 · 판독) | 다물체 |
| U6 | — | 조밀 충전 수렴 |
| R1 · R3 · R7 | — | — |
| R2 | 마찰 없는 분리만 | 미끄럼 |
| R4 | 단일 접촉 되돌아옴 (위) | 침대 |
| R5 | 이 법칙은 맞춤 값 둘 (C_a · K_c) — R5 '모델마다 하나' 와 어긋남 · Thornton 은 0 이지만 2 배 무름 | — |
| R6 | 곡률 보정 = 접촉 평평해짐의 대리일 뿐 (입자 형상 불변) · 항복 깊이 공식 (단계 4) | 형상 변형 |

## 9. 적용 인사이트 (내 연구에 어떻게)

1. **C′ 를 고를 때 p_y 를 첫 항복값 (1.61σ_y) 에 두지 않는다** — 이 FEA 범위에서도 평균압은 ≈ 1.9–2.3σ_y (그림 11 절점 구간) 로 오르고 접촉은 곡률 평평해짐으로 넓어진다 (§3-5 의 두 몫 · 거의 반반).  Thornton–Ning 을 쓰면 단일 접촉에서 먼저 힘이 절반이 되고, 다접촉 보정 (β) 이 그걸 메우는 것처럼 보일 수 있다 → 단일 접촉 오차와 다접촉 효과를 **따로** 잰다.
2. **법칙 검증은 곡선 둘 (P–α 적재 + 제하) + 소산 (e) 을 함께** — 한 숫자 맞춤 (e · 300 MPa 기공률 한 점) 은 서로 다른 법칙도 통과시킨다 (식 4.10 · 그림 21) → 우리 E_eff 한 점 보정 · DEM ↔ MPM 비교의 등록 항목에 그대로.
3. **언로딩 · 탈압 결과에서 연화 E 의 몫을 분리** — 단일 접촉에서 탄성 되돌아옴 변위 α_max − α_res = (a^e)²/(C_R R) (식 3.19) 이고 a^e ∝ (PR/E)^(1/3) (식 1.7) 이라 같은 힘에서 E^(−2/3) 로 커진다 · 항복 깊이도 α_Y ∝ (σ_y/E)² → 연화 E (MPM 1.53 GPa · E/σ_y ≈ 5) 는 같은 하중에서 되돌아옴을 키우는 쪽 [카드 산술 · 카드 추론] · ⚠ DEM `hooke/hysteresis` 의 겹침 되돌아옴 몫은 k₁/k₂ 로 정해져 이 식과 다르다 (침대 두께 되돌아옴의 절대값은 연화로 커지는 쪽 — 시험 전).
4. **해상도는 지름이 아니라 접촉 반지름으로 센다** (U1) — FEA 는 접촉 반지름당 ≈ 48 요소로 탄성 반지름 2.7 % · 중심 압력은 그래도 인공물.
5. **재구현 도구** (`tools/litdb/vuquoc1999_nfd_reproduce.py`) 를 C′ · U3 · U5 시험의 손 계산 기준으로 바로 쓸 수 있다 (원문 인쇄값 15 개 재현).

## 10. 인용 가능 문장 (deck/paper 용 — 표지 그대로)

- *"We will show later that the Thornton (1997) NFD model produces FD curves that are too soft compared with the FEA results."* (Vu-Quoc & Zhang 1999, p.4019) · *"The P–α curve produced by the Thornton (1997) NFD model is, however, much too soft"* — 770.5 N vs 1500 N at α_max ≃ 1.56 × 10⁻⁵ m (p.4034).
- *"When the normal forces P exceed P_Y, the P–α curves are not straight lines as assumed in Thornton (1997)."* (p.4023)
- *"There is no solid basis for obtaining the coefficient of the dashpot … the spring–dashpot NFD model is regarded as a primitive NFD model for DEM simulations."* (p.4019)
- *"even though elastic–perfectly plastic material is used in our FEA, the resulting behaviour of the contact radius … behaves in a similar manner to an elastic–plastic material with hardening."* (p.4023)
- *"One should not use these values for other examples without verifying their validity."* (p.4030)
- *"it is not sufficient to use the coefficient of restitution to compare the accuracy of NFD models. A combination of both NFD relationship and coefficient of restitution is necessary"* (p.4040)
- 영어 정리 문장 (우리 덱): "In a single-contact FEA of an elastic–perfectly plastic sphere (E/σ_Y = 700, P/P_Y ≤ 41), the Thornton-type pressure cap (1.61σ_Y) with a linear plastic branch under-predicts the contact force by about a factor of two; the deficit factorises into a too-low pressure plateau (FEA ≈ 2.25σ_Y) and the neglected flattening of the contact curvature (Vu-Quoc & Zhang 1999)."

## 11. 주의/한계 (over-claim 방지 · 원문 비판)

- **재료 · 크기 하나**: 알루미늄 합금 (E 70 GPa · ν 0.3 · σ_Y 100 MPa · 완전소성) · R 0.1 m — C_a · K_c 는 이 경우에만 (저자 스스로).  LPSCl · NCM · 분말 값으로 쓰지 않는다.
- **작은 변형 · 단일 접촉**: δ/d ≤ 1.6 × 10⁻⁴ · a/R ≤ 0.015 · P/P_Y ≤ 41 — 우리 압밀 접촉 (δ/d ≈ 7.4–11 % · a/R ≈ 0.3 · α/α_Y ≈ 80 – 4 × 10³) 은 범위 밖 · 이웃 접촉의 상호작용 · 조밀 영역 · 기하 비선형 (FEA 설정 [미확인]) 없음.
- **표본 안 검증**: 두 상수를 맞춘 FEA 로 비교 (0.3–3.8 %) — 표본 밖 · 실험 대조 없음 (짝 논문 몫) · ABC 숫자 없음.
- **외삽**: 충돌 0.06–0.20 m/s (P/P_Y 64–286) 는 맞춘 범위 밖인데 그림 20 은 그대로 그린다 [재현].
- **잔류 변위는 원문 수치가 아니다** — 판독 (FEA 2.0 · 4.5 · 7.1 × 10⁻⁶ m) 과 재현 · Thornton 잔류는 이 논문에 없는 R_p* 식 (TN98 식 28) 을 빌린 계산 (그 식으로 원문 e_Th 0.5331 · 식 1.11 이 재현되므로 같은 꼴로 보임 [카드 추론]).
- **제하 근사**: FEA 의 a^p 는 제하 중 고정이 아니다 (그림 12 · ≈4.3 → 2 × 10⁻⁴ m [판독]) · 재재하 가지 없음 · 점착 · 마찰 · 경화 재료 · 속도 효과 없음.
- **원문 인쇄 어긋남 다섯** (§3-8) — 값 · 식을 옮길 때 단위 (C_a) · (3.17) · (4.7) · 그림 12 눈금을 고쳐 읽은 것을 밝힌다.
- **DOI 미확인** (JSTOR 판에 인쇄 없음).

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)

| 원문 목록 | 왜 | litdb |
|---|---|---|
| Thornton, C. 1997 Coefficient of restitution for collinear collisions of elastic perfectly plastic spheres. ASME Jl Appl. Mech. 64, 383–386. | 이 논문이 '너무 무르다' 한 법칙의 원전 (p_y = 1.61σ_Y · 직선 소성 · R_p* 제하 · 식 1.11 · 1.12) — C′ (e · k · l) | 카드 없음 (`morrissey2013_…` · `nase2001_…` · `harthong2009_…` 언급만 · 점착판 = `thorntonning1998_…`) |
| Vu-Quoc, L., Zhang, X. & Lesburg, L. 1999a A normal force–displacement model for contacting spheres accounting for plastic deformation: force-driven formulation. ASME Jl Appl. Mech. (Submitted.) | 힘 구동판 · K_c 근거 (*"see Vu-Quoc et al. (1999a) for more details"* p.4029) | 카드 없음 |
| Vu-Quoc, L. & Lesburg, L. 1999 Contact force–displacement relations for spherical particles accounting for plastic deformation. (Submitted.) | 더 많은 FEA · A_Y (3.7) 유도 · 메시 | 카드 없음 (서지 일부만) |
| Zhang, X. & Vu-Quoc, L. 1999 A method to extract the mechanical properties of particles in collision based on a new elastoplastic normal force–displacement model. Int. J. Plasticity. (Submitted.) | 실험으로 C_a · K_c 뽑기 (FEA 없이 · 콩) — 보정 경로 (l) | 카드 없음 |
| Zhang, X. 1998 On computer simulation of dry particle systems using discrete element method and the development of DEM contact force–displacement models. PhD thesis, University of Florida. | ABC 경로 숫자 · v_in 0.02 · 0.10 결과 · FEA 원자료 | 카드 없음 |
| Walton, O. R. & Braun, R. L. 1986 Viscosity, granular-temperature, and stress calculations for shearing assemblies of inelastic, frictional disks. J. Rheology 30, 949–980. | 이중 선형 NFD 원전 (식 1.9 · 1.10) | ⛔ 후보 표 N-72 첫째 = 1저자 '내려받기 불가' 제외 |
| Walton, O. R. 1993 Numerical simulation of inelastic, frictional particle–particle interactions. In Particulate two-phase flow (ed. M. C. Roco), ch. 25, pp. 884–911. | 비교 대상 FEA 메시 (*"a much finer mesh … than the discretization used in Walton (1993)"* p.4020) | ⚠ 정본 `walton1993_…` (Mech. Mater. 16) 과 **다른 글** · 카드 없음 |
| Vu-Quoc, L. & Zhang, X. 1999a … Mech. Mater. 31, 235–269. | 탄성 접선 개선판 (짝 TFD 의 출발점) | 카드 없음 (`silbert2001_…` [31] · `lommen2014_…` 이웃 언급) |
| Johnson, K. L. 1985 Contact mechanics, 2nd edn. Cambridge University Press. | 1.61 (p.155) 의 출처 | 책 · 카드 없음 |

## [미확인] 목록

- DOI (JSTOR 판에 인쇄 없음 — 메타줄 값은 `morrissey2013_…` L447).
- FEA 계산 시간 · 기하 비선형 설정 · 요소 수 수렴 시험 (원문 없음).
- ABC 경로 비교 숫자 (*"Similar results"* · Zhang 1998).
- 잔류 변위 · 잔류 반지름의 FEA 수치 (그림 판독뿐).
- A_Y(ν) 의 ν ≠ 0.3 값 (원문은 0.3 만) — §7-4 · §7-6 의 LPSCl (0.36) · MPM (0.49) 어림은 1.61 을 그대로 넣었다.
- LPSCl σ_y 범위 0.05–0.30 GPa (우리 CLAUDE.md 의 [미확인 · 카드 없음] 표지 그대로 · `SELF-160`).
- 짝 논문들의 출판 서지 (원문은 submitted / in the press).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-17)

- 32 쪽 본문 전부를 OCR 글 층으로 읽고, 식 50 개 · 알고리즘 2 개 · 그림 21 개 · 인용 문단 20 개를 원 래스터 크롭으로 다시 읽었다 (OCR 은 'R* = ½R' 를 'R* - R' 로, 'C_a' 를 '0a' 로 읽는 등 식 · 기호가 믿을 수 없다).
- 재구현 (`--selftest`): P_Y 36.447 N · m 11.3055 kg · v_Y 1.6697 × 10⁻³ · v_in 0.04 의 v_out 0.03036 · e 0.7589 · P_max 1433 N · τ 1.003 × 10⁻³ s · Thornton e 0.5330 · P_max 956 N · τ 1.214 × 10⁻³ s · 변위 구동 1495.3 · 770.8 · 558.4 N · 뉴턴 최대 2 → 원문 인쇄값과 모두 맞음 (Thornton 구 ↔ 평판 = R* = R · E* = E/(1 − ν²) 로 읽어야 맞는다).
- 판독 40 점 (그림 20) 은 재구현과 ±0.001 · 인쇄값 (0.04 m/s) 과 ±0.0005.
- 그림 10 과 그림 16 의 AFG 마지막 하중 0 점 (7.09 · 7.08 × 10⁻⁶ m) 이 서로 맞음.
- 그림 10 α_max 점선 판독 (P = 0 틀 높이) ADE 1.140 · AFG 1.559 × 10⁻⁵ m = 인쇄 1.14 · 1.56 × 10⁻⁵ (p.4034–4035) 와 0.1 % 안 → 같은 방법의 ABC 6.79 × 10⁻⁶ m 를 씀 (ABC 값은 원문에 인쇄 안 됨).
- 그림 11 Hertz 곡선의 p = 0 점 0.786 · 0.991 · 1.134 × 10⁻³ m = 식 (1.7) 0.787 · 0.992 · 1.135 × 10⁻³ (±0.0013 × 10⁻³) → 그 쪽 보정 확인.
- 스캔 전단: PDF 11 · 13 · 15 · 23 쪽은 틀 세로선이 기울고 (dx/dy −0.009 ~ −0.013) 가로선은 수평 — 판독할 때 x 는 그 높이의 축 가까이에서 읽었다 (14 · 24 · 30 쪽은 기울기 없음).
- `morrissey2013_…` 그림 3.7 크롭을 열어 이 논문 그림 16 과 같은 그림임을 확인.

## 🔗 관련 카드
- 이 논문이 '너무 무르다' 고 한 법칙의 계열: [`thorntonning1998_adhesive_elastoplastic_contact`](thorntonning1998_adhesive_elastoplastic_contact.md) · [`varkey2026_multicontact_elastoplastic_dem`](varkey2026_multicontact_elastoplastic_dem.md) · [`sangros2019_dem_calendering_lib_electrode`](sangros2019_dem_calendering_lib_electrode.md) (Thornton–Ning 항복을 쓴 DEM).
- 고른 의도: [`morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis`](morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis.md) (그림 3.7 = 이 논문 그림 16).
- 같은 문제의 FEM 기준선: [`kogutetsion2002_ep_sphere_rigid_flat`](kogutetsion2002_ep_sphere_rigid_flat.md) · [`jacksongreen2005_fem_elastoplastic_hemispherical_contact`](jacksongreen2005_fem_elastoplastic_hemispherical_contact.md) · [`mesarovicfleck2000_dissimilar_elastoplastic_indentation`](mesarovicfleck2000_dissimilar_elastoplastic_indentation.md) · [`storakers1997_similarity_inelastic_contact`](storakers1997_similarity_inelastic_contact.md).
- 우리 접촉 법칙 정의서 · 이중 선형 계열: [`luding2008_cohesive_frictional_contact_models`](luding2008_cohesive_frictional_contact_models.md) · [`walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem`](walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem.md) (⚠ 다른 Walton 1993).
- 같은 저자 다른 논문 (2001 접선 · 카드 없음) 을 인용한 카드: [`demirtas2021_mpfem_hollow_sphere_die_compaction`](demirtas2021_mpfem_hollow_sphere_die_compaction.md) · [`harthong2009_high_density_compaction_dem_voronoi_contact_law`](harthong2009_high_density_compaction_dem_voronoi_contact_law.md) · 1999a (Mech. Mater. 31) 를 인용한 카드: [`silbert2001_chute_flow_bagnold_spring_dashpot_hertz_dem`](silbert2001_chute_flow_bagnold_spring_dashpot_hertz_dem.md).
- 큰 변형 쪽: [`zunker2024_mdr_contact_model_partI`](zunker2024_mdr_contact_model_partI.md) · [`zunker2025_dem_large_deformation_compaction`](zunker2025_dem_large_deformation_compaction.md) · [`brodu2015_multiple_contact_dem_dense_granular`](brodu2015_multiple_contact_dem_dense_granular.md).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

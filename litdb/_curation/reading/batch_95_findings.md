# 배치 95 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-17 · 위시 W-1117-4)

카드 = `vuquoc1999_elastoplastic_normal_contact_force_displacement_model` (원문 = JSTOR 스캔판 33 쪽 (PDF p.1 = JSTOR 표지 · PDF p ↔ 인쇄 4011 + p) · 보충 자료 안내 없음 ·
그림 크롭 97 장 = 그림 21 + 패널 4 · 알고리즘 상자 2 · 번호 식 50 (식마다 한 장) · 근거 문단 20 — 도구가 찾은 11 장은 쪽 너비 띠라 전부 손으로 다시 자름 + 손 크롭 다시 자름 10 ·
판독 원자료 `litdb/figures/<slug>/digitized.csv` 67 행 · 재구현 `tools/litdb/vuquoc1999_nfd_reproduce.py` (`--selftest` = 원문 인쇄값 15 개 PASS)).
서지 (k · l 인용용) = Vu-Quoc L., Zhang X., *An elastoplastic contact force–displacement model in the normal direction: displacement-driven version*, Proc. R. Soc. Lond. A 455 (1999) 4013–4044 (DOI 10.1098/rspa.1999.0488 — JSTOR 판에 인쇄 없음 · `morrissey2013_…` L447 의 값).
⚠ 재료 = **알루미늄 합금 구 하나 (탄성–완전소성 · E 70 GPa · σ_Y 100 MPa · R 0.1 m) ↔ 마찰 없는 강체 평판** — 계산 = 단일 접촉 축대칭 FEA + 그 FEA 에 맞춘 DEM 법선 접촉 법칙 + 단일 구 충돌 (SE · NCM · 다입자 · 압밀 · 기공 없음).  쪽 = 인쇄 쪽 (4013–4044).

---

## a — 순수 SE 압력별 기공 곡선 · 진밀도 · 상태

이 배치에 없음 (기공 · 밀도 · SE 0 — 단일 Al 구 접촉 · 카드 §2).

## b — 압력을 뺄 때 되돌아오는 양 · 잰 방법

- [b] vuquoc1999_… | FEA (ABAQUS 5.4 · 정적 · 힘 구동 · 한 주기 30 단계 넘게) 의 하중 0 마지막 점 = 잔류 변위 **2.01 · 4.55 · 7.09 × 10⁻⁶ m** (P_max 500 · 1000 · 1500 N) → 되돌아온 몫 (α_max − α_res)/α_max **0.70 · 0.60 · 0.55** (α_max 6.79 × 10⁻⁶ [판독] · 1.14 · 1.56 × 10⁻⁵ m [인쇄]) | 카드 §3-3 · 그림 10 · 16 · p.4034–4035 | [판독 · P = 0 틀 위 표지 x 중심 · 그림 10 과 16 의 AFG 7.09 · 7.08 × 10⁻⁶ 이 서로 맞음] · [카드 산술] | 원문 본문에 잔류 변위 숫자 없음 · 단일 접촉 · Al · E/σ_Y 700 · 마찰 없음
- [b] vuquoc1999_… | 모델 제하 = 식 (3.19)–(3.22): a^p · C_R 을 P_max 값에 고정한 Hertz → P = [4E C_R(P_max)^(3/2) R^(1/2) / 3(1 − ν²)] (α − α_res)^(3/2) (원래 Hertz 강성의 C_R^(3/2) 배 · 1500 N 1.65) · 같은 α_max 를 넣은 잔류 **1.48 · 3.74 · 6.37 × 10⁻⁶ m** = FEA 보다 26 · 18 · 10 % 작음 · Thornton (R_p* 제하) **2.95 · 6.30 · 9.58 × 10⁻⁶** = 47 · 39 · 35 % 큼 | 카드 §0 ③ · §3-4 · §3-6 | [재현] · [카드 산술] | Thornton 의 R_p* 식은 이 논문에 인쇄 안 됨 (`thorntonning1998_…` eq28 을 빌림 · 그 꼴로 원문 e_Th 0.5331 재현) · 재재하 가지 없음 (알고리즘 3.2 는 다시 누르면 처녀 적재식)
- [b] vuquoc1999_… | 분리 규칙 *"when P is decreasing and reaches zero, the sphere is considered separated from the surface. Consequently, P is then set to be zero thereafter, even though the normal displacement may not be zero"* · 잔류 접촉 반지름 = a^p_max (식 3.20 · 1500 N 3.41 × 10⁻⁴ m [카드 산술]) | p.4026 · p.4037 · 카드 §3-6 | [인쇄] · [카드 산술] | FEA 의 a^p 는 제하 중 고정이 아니다: P ≈ 1490 N 3.21 → 654 · 750 N 4.34 → 15 N 2.12 × 10⁻⁴ m (모델 3.41 고정) [판독 그림 12 · 카드 §3-3]

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- [c] vuquoc1999_… | σ_Y 100 MPa = 탄성–완전소성 Al 의 일축 항복 (von Mises) · 항복 시작 = Hertz 응력장의 J₂ 최대점에 von Mises → 최대 접촉압 p₀ = A_Y(ν)σ_Y · **A_Y(0.3) ≈ 1.61** (= (σ_Y)_Th = 1.61σ_Y · Johnson 1985 p.155 인용) → P_Y = π³R²(1 − ν²)²[A_Yσ_Y]³/(6E²) = 36.4 N (식 3.7) | p.4019 · p.4031 (각주) · 카드 §3-1 | [인쇄] | **일축 환산 있음** (A_Y = 첫 항복 접촉압 ÷ 일축 σ_Y) · ν 0.3 값만 (다른 ν [미확인]) · 같은 정의 = `kogutetsion2002_…` K·H = 0.577 × 2.8Y = 1.616Y [다른 카드 · 카드 §3-4b]
- [c] vuquoc1999_… | 탄소성 구간의 '경도' (평균압 P/πa²) = **1.88–2.03 · 2.03–2.16 · 2.13–2.27 σ_Y** (500 · 1000 · 1500 N · 마지막 p > 0 절점 ↔ 첫 p = 0 절점 구간) · 압력 꼭대기 *"flat top at (σ_z)max ≃ 2.25 × 10⁸ (N m⁻²) > 2.00σ_Y"* · *"the maximum normal stress is, however, not fixed, and is much larger than predicted by Thornton (1997)"* · 모델 a^ep 로 1.99 · 2.15 · 2.19 | p.4024–4025 · 그림 11 · 카드 §3-3 · §3-6 | [인쇄] · [판독 그림 11 · Hertz 곡선 p = 0 점이 식 1.7 과 ±0.0013 × 10⁻³ 로 보정 확인] · [카드 산술] | 범위 α/α_Y ≤ 14 (KE eq6 2.00 · 2.12 · 2.20 와 구간 안 · 완전소성 2.8 은 ω/ω_c 110) · 이 범위에서 Tabor H ≈ 3σ_Y 는 면적을 ≈ 27 % 작게 본다 · 크리프 · 속도 효과 없음 (*"time-independent plasticity"* p.4038)

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

이 배치에 없음 (단일 접촉 · 혼합 · 하중 분담 0).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안

- [e] vuquoc1999_… | **Hertz 는 P_Y 위에서 깨진다** — *"(i) When the normal force P is smaller than the incipient yield normal force P_Y, the P–α curve obtained from FEA agrees very well with Hertz theory … (ii) When the normal forces P exceed P_Y, the P–α curves are not straight lines as assumed in Thornton (1997)"* · FEA 는 Hertz 보다 무르다 (α 1.56 × 10⁻⁵ m 에서 1500 ↔ Hertz 1998 N [카드 산술]) | p.4023 · 그림 10 · 카드 §3-3 | [인쇄] · [카드 산술] | P_Y 36.4 N · α_Y 1.08 × 10⁻⁶ m · 단일 접촉 · 작은 변형
- [e] vuquoc1999_… | **Thornton (1997) 항복 캡 + 직선 가지 (맞춘 값 0 · σ_Y 만)** = 같은 변위에서 FEA 힘의 **51–56 %** (770.5 · 559.6 N ↔ 1500 · 1000 N · *"much too soft"*) · e −22–24 % · 결손 = 넓어진 접촉 (a²/Rα ×1.3–1.4) × 높은 평균압 (×1.3–1.4) 이 거의 반반 | p.4034–4035 · 카드 §3-4 · §3-5 | [인쇄] · [카드 산술 · 항등식 P/P_Th = (a²/Rα)(p̄/p_y)(πp_yRα/P_Th)] | P/P_Y 27–41 · Al · 2.25/1.61 × C_R = 1.948 이 1.947 과 맞는 것은 우연 (평균압 ≠ 꼭대기)
- [e] vuquoc1999_… | **대안 (이 논문 NFD) = 맞춘 값 2 (C_a 2.33 × 10⁻⁷ m/N · K_c 2.69 × 10⁻⁴ N⁻¹ · 같은 FEA 에서)** · 재료 입력 4 (R · E · ν · σ_Y) + A_Y(ν) · 같은 FEA 대비 P −0.3 · −3.8 % · e +2.3 · +3.1 % · ABC 는 *"Similar results"* (숫자 없음) · 다른 법칙: Walton–Braun = 셋 중 둘 (e · K₁ · K₂) 을 실험에서 · 스프링–대시포트 = 감쇠 계수 근거 없음 | p.4017 · p.4019 · p.4027 · p.4029 · p.4034–4035 · 카드 §3-4 · §7-3 | [인쇄] | 표본 밖 검증 아님 · *"One should not use these values for other examples without verifying their validity"* (p.4030) · 충돌 0.06–0.20 m/s 는 맞춘 범위 밖 (P/P_Y 64–286 [재현])
- [e] vuquoc1999_… | FEA 기준 자체의 독립 대조: `kogutetsion2002_…` (ANSYS 5.7) eq8 이 같은 α 에서 **521 · 1002 · 1488 N** (FEA 500 · 1000 · 1500 · +4 · +0.2 · −0.8 %) · 평균압 · 면적 몫도 FEA 구간 안 → 'Thornton 은 너무 무르다' 의 기준은 한 코드의 인공물이 아님 | 카드 §3-4b | [다른 카드 식 · 카드 산술] | 둘 다 마찰 없음 · 탄성–완전소성 · 작은 변형 (실험 검증 아님) · 큰 변형 (a/R > 0.015) 범위는 어디에도 없음

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙

- [f] vuquoc1999_… | MPM 없음 · FEA 해상도 규칙: 접촉 요소 *"of the order of 2.3 × 10⁻⁵ m, which is much less than the contact radius … about 1.1 × 10⁻³ m"* (≈ 48 요소 / 접촉 반지름 [카드 산술]) · 한 주기 *"more than 30 steps"* · 탄성 검증: 반지름 [1.13, 1.17] × 10⁻³ ↔ Hertz 1.14 × 10⁻³ (*"less than 2.7%"*) · 중심 (r = 0) 압력 급락 = *"numerical characteristics of the finite-element modelling of our axisymmetric problem"* | p.4020 · p.4022 · 카드 §3-1 · §3-2 | [인쇄] · [카드 산술] | 요소 수 수렴 시험 없음 · 지름당 셀 수 규칙 없음 (접촉 반지름당 요소 수) · 해석 시간 [미확인]
- [f] vuquoc1999_… | DEM 수치: leap-frog · Δt 1.0 × 10⁻⁶ s · 뉴턴 판정 (P_n^i − P_n^(i−1))/P_n^i ≤ 0.005 (식 4.8) · *"the maximal number of Newton–Raphson iterations in our simulation was two"* · 강체 평판 · 구 1 개 · 중력 없음 | p.4036–4038 · 카드 §3-1 · §4-3 | [인쇄] · [재현 = 최대 2 회] | 다물체 · 접촉 탐색 비용 없음

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거

이 배치에 없음 (FEA = 축대칭 (3D 구를 2D 메시로) · 충돌 = 1 자유도 · 평면 2D ↔ 3D 에 대한 말 없음 · 카드 §4-4 (iii)).

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

이 배치에 없음 — 방향이 반대 (단일 접촉 FEA → DEM 접촉 법칙의 꼴 · 상수 · 시점 = 법칙을 만들 때 한 번 · *"The role of finite-element analysis (FEA) of contact problems in the development of the present NFD model is twofold"* p.4014 · 카드 §4-1).

## i — 복합 양극 (AM + SE) 의 압력별 기공

이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것

- [j] vuquoc1999_… | 상수의 재료 · 크기 묶임: *"the value of C_a cited above is particular to the present geometry and material of the sphere … For a different geometry and material, the value of C_a must be evaluated by various means: (i) FEA (as in the present paper); (ii) experiment (Zhang & Vu-Quoc 1999); or (iii) analysis (future publication)"* (Remark 2.1) · K_c 같음 (Remark 3.1) · *"Further theoretical work can be done to relate these model parameters to other basic parameters"* | p.4027 · p.4029 · p.4030 · p.4042 · 카드 §4-4 (ii) | [인쇄] | 우리 재료 (LPSCl · NCM) 상수 없음 · 우리 깊이 (a/R ≈ 0.3) FEA 없음
- [j] vuquoc1999_… | 비균질 입자: *"it is impossible to use FEA in this case, since it is very difficult to model accurately the inhomogeneous material inside the particle"* (콩 → 실험 두 가지로 상수) · 속도: *"time-independent plasticity"* | p.4038 · p.4042–4043 · 카드 §4-4 | [인쇄] | 다입자 · 탈압 침대 · 재재하 · 점착 · 마찰에 대한 한계 문장은 없다 (모델 밖) [카드 해석]

## k — DEM 의 한계 (원문 문장 · 위치)

- [k] vuquoc1999_… (Vu-Quoc & Zhang 1999, Proc. R. Soc. Lond. A 455, 4013–4044) | 스프링–대시포트: *"In DEM simulations, however, the energy dissipation in the spring–dashpot model depends, highly on the dashpot coefficient and the relative velocity in a collision. There is no solid basis for obtaining the coefficient of the dashpot for these kinds of NFD models. The dependence of the model on the collision velocity also prevents the use of quasi-static simulation to correctly evaluate the energy dissipation caused by plastic deformation. For the above reasons, the spring–dashpot NFD model is regarded as a primitive NFD model for DEM simulations."* | p.4019 · 카드 §4-4 (i) | [인쇄] | 접촉 법칙 층의 한계 (입자 모양 · 조밀 영역 · 접촉 독립 가정 = 말 없음)
- [k] vuquoc1999_… (Vu-Quoc & Zhang 1999, Proc. R. Soc. Lond. A 455, 4013–4044) | Walton–Braun 이중 선형 (우리 `hooke/hysteresis` 계열): *"The constancy of the coefficient of restitution e with respect to the incoming velocity of impact is, however, not in agreement with experimental results: e is not a material property, but depends on the plastic deformation incurred at impact"* · *"two of the three parameters (e, K1 and K2) need to be extracted from experimental data"* · 법선 (소성) ↔ 접선 (Mindlin–Deresiewicz 탄성) *"inconsistency"* | p.4017 · 카드 §4-4 (i) · §7-3 | [인쇄] | 보정값이 물성이 아니라는 직접 진술 (e) · 겹침 상한 · 밀도 상한 수치 없음
- [k] vuquoc1999_… (Vu-Quoc & Zhang 1999, Proc. R. Soc. Lond. A 455, 4013–4044) | 항복 캡 (Thornton 1997): *"In fact, there was no validation of the theory proposed in Thornton (1997) until now."* (각주) · *"We will show later that the Thornton (1997) NFD model produces FD curves that are too soft compared with the FEA results."* · FEA 대비 힘 51–56 % (p.4034–4035) | p.4019 · 카드 §0-1 ① | [인쇄] | 단일 접촉 · Al · P/P_Y ≤ 41 — 조밀 · 다접촉 영역의 과연 · 과강 수치는 없다

## l — 소성변형이 왜 어려운가 · 우회 · 값

- [l] vuquoc1999_… (Vu-Quoc & Zhang 1999, Proc. R. Soc. Lond. A 455, 4013–4044) | 접촉 기하가 재료 거동 위에 얹힌다: *"even though elastic–perfectly plastic material is used in our FEA, the resulting behaviour of the contact radius, when decomposed into an elastic part and a plastic part, behaves in a similar manner to an elastic–plastic material with hardening. The reason is certainly due to the influence of the mechanics of contact and the spherical geometry on top of the material behaviour."* → 압력 캡 하나로는 안 된다 (평균압 1.9–2.3σ_Y 로 계속 오르고 곡률이 평평해짐) | p.4023 · 카드 §3-3 · §3-5 | [인쇄] · [판독] | 단일 접촉 · 작은 변형 · 입자 형상 변화는 다루지 않음 (곡률 보정 = 대리)
- [l] vuquoc1999_… (Vu-Quoc & Zhang 1999, Proc. R. Soc. Lond. A 455, 4013–4044) | **우회 = 강체 구 + 접촉 법칙 안의 소성** (반지름 더하기 a^ep = a^e + a^p (식 2.3) · 곡률 C_R (식 3.3)) · 맞춘 값 **2** (C_a · K_c) · 무엇에 = 같은 재료 · 크기의 축대칭 FEA 세 하중 경로 (C_a = *"least-square fit of the FEA results"* p.4027) · 검증 = 같은 FEA (힘 0.3–3.8 % · e 2.3–3.1 %) · 비용 = DEM 걸음마다 뉴턴 ≤ 2 회 (Δt 1 µs) · FEA 시간 [미확인] · 상수 = 재료 · 크기마다 FEA 또는 실험 (*"the model parameters of the present elastoplastic NFD model are to be measured for different materials and geometry of the particles"* p.4014) | 카드 §1 · §3-4 · §4-2 · §4-4 (ii) | [인쇄] | 실험 대조는 짝 논문 (Zhang & Vu-Quoc 1999 · submitted) 몫 · 우리 깊이의 상수 없음

## m — 받아들일 통찰

- [m] **항복 캡 (후보 C′) 은 단일 접촉에서 먼저 시험한다** — 이 논문 범위 (P/P_Y ≤ 41) 에서도 1.61σ_Y 캡 + 직선 가지는 힘 ½ · 결손이 면적 (곡률) 과 평균압으로 거의 반반 → 다접촉 보정 (β) 이 이 단일 접촉 오차를 메우는 것처럼 보일 수 있으니 두 오차를 따로 잰다 · 자리: 후보 C′ · U1 · 결과 전 대조 항목 | 왜: p.4034–4035 · 카드 §3-5 · §9 | 카드 §8
- [m] **법칙 검증 = 곡선 (P–α 적재 + 제하) + 소산 (e) 함께** — Remark 4.2 *"it is not sufficient to use the coefficient of restitution to compare the accuracy of NFD models. A combination of both NFD relationship and coefficient of restitution is necessary"* (식 4.10 · 그림 21: 다른 두 법칙이 같은 e) → 우리 E_eff 한 점 (300 MPa 기공률) 보정 · DEM ↔ MPM 비교의 결과 전 등록에 곡선 항목을 둔다 · 자리: 단계 0 · 결과 전 대조 항목 | 왜: p.4040 | 카드 §3-7 · §9
- [m] **해상도는 접촉 반지름으로 센다** — 이 FEA 는 접촉 반지름당 ≈ 48 요소로 탄성 반지름 2.7 % · 그래도 중심 압력 급락 (수치 인공물) → MPM 단일 입자 압축 (U1) 은 '지름당 셀' 과 함께 '접촉 반지름당 셀' (지름 30 셀 · a/R 0.3 이면 a ≈ 4.5 셀 [카드 산술]) 을 적는다 · 자리: U1 · 단계 2 | 왜: p.4020 · p.4022 | 카드 §8 · §9
- [m] **단위 시험의 해석 기준은 독립 FEM 두 개로 교차 확인** — 이 논문 FEA 와 Kogut–Etsion 2002 맞춤식이 같은 α 에서 힘 ±4 % · 평균압 · 면적 구간 안 (카드 §3-4b) · 재구현 도구가 원문 인쇄값 15 개를 재현 → U1 · U3 · U5 기준 곡선으로 바로 쓸 수 있다 (Al · E/σ_Y 700 · 작은 변형 한정) · 자리: U1 · U3 · U5 · 단계 2 | 왜: 카드 §3-4b · `tools/litdb/vuquoc1999_nfd_reproduce.py` | 카드 §9

## n — 논문 에이전트 후보

- [n] Thornton, C. 1997 Coefficient of restitution for collinear collisions of elastic perfectly plastic spheres. ASME Jl Appl. Mech. 64, 383–386. (원문 목록 그대로) | e · k · l · m — 이 논문이 '너무 무르다' 고 한 법칙의 원전 (p_y = 1.61σ_Y 캡 · 직선 가지 · R_p* 제하 · 식 1.11 · 1.12 의 출처) — 이 카드는 R_p* 를 `thorntonning1998_…` eq28 에서 빌렸다 · 카드 §3-4 · §12 | litdb 확인: papers/ ls · 'collinear collisions' · 'Appl. Mech. 64' grep → `morrissey2013_…` L446 · `nase2001_…` L200 의 목록 줄뿐 → 카드 없음
- [n] Zhang, X. & Vu-Quoc, L. 1999 A method to extract the mechanical properties of particles in collision based on a new elastoplastic normal force–displacement model. Int. J. Plasticity. (Submitted.) (원문 목록 그대로 · 서지 일부만 — 권 · 쪽 없음) | l · m — FEA 없이 실험 두 가지로 C_a · K_c 를 뽑는 보정 경로 + *"A combination of both NFD relationship and coefficient of restitution is necessary"* 의 예 (p.4040 · p.4042–4043) — 우리 SE 상수를 실험으로 잡는 길 · 카드 §4-4 (ii) · §12 | litdb 확인: 'extract the mechanical properties of particles' · 'Int. J. Plasticity' grep 0 → 카드 없음
- [n] Vu-Quoc, L., Zhang, X. & Lesburg, L. 1999a A normal force–displacement model for contacting spheres accounting for plastic deformation: force-driven formulation. ASME Jl Appl. Mech. (Submitted.) (원문 목록 그대로 · 서지 일부만) | e · l — K_c 의 근거 (*"see Vu-Quoc et al. (1999a) for more details"* p.4029) · 힘 구동판 · 카드 §12 | litdb 확인: 'force-driven formulation' · 'force–driven formulation' grep 0 → 카드 없음
- [n] Vu-Quoc, L. & Lesburg, L. 1999 Contact force–displacement relations for spherical particles accounting for plastic deformation. (Submitted.) (원문 목록 그대로 · 서지 일부만) | c · f — A_Y(ν) (식 3.7) 유도 · 더 많은 FEA · 메시 (p.4022 · p.4023 · p.4031) · 카드 §12 | litdb 확인: 'Vu-Quoc & Lesburg' · 'Vu-Quoc, L. & Lesburg' grep 0 → 카드 없음
- [n] Zhang, X. 1998 On computer simulation of dry particle systems using discrete element method and the development of DEM contact force–displacement models. PhD thesis, University of Florida. (원문 목록 그대로) | b · e — ABC 경로 비교 숫자 (*"Similar results"* p.4035) · v_in 0.02 · 0.10 결과 · FEA 원자료 (잔류 변위 수치의 원천 후보) · 카드 §3-4 · §12 | litdb 확인: 'dry particle systems' grep 0 → 카드 없음

## 카드 문제

- `morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis` **L273 · L447** — 그림 3.7 = 원문 그림 16 (같은 범례 · e 0.7372 · 0.7541 · 0.5641 · P_max 1500 · 1495 · 770.5 N) · 서지 (권 455 · 호 1991 · 4013–4044) = 원문과 같음 (DOI 는 JSTOR 판에 인쇄 없음 — 대조 못 함) → 옮김은 맞다.  **L249** *"these linear models maybe too soft at higher stresses" (Vu-Quoc · Zhang 1999b 의 FEA)* 는 Morrissey 자신의 문장 (p.77) 을 옳게 옮겼으나, 원문이 FEA 와 견준 '선형' 은 **Thornton (1997) 직선 소성 가지 하나**다 (Walton–Braun · 스프링–대시포트는 FEA 비교 없이 다른 이유로 비판) — 'linear models' (복수 · 일반) 로 인용하면 원문보다 넓다.  'Vu-Quoc and Zhang 1999b' 꼬리표 = Morrissey 목록 기준 · 원문 자신의 목록에서 1999b 는 접선 탄소성판 (submitted) — 혼동 주의 (오류 아님).  → 그 카드는 고치지 않았다 · 🔗 절 끝에 한 줄로 새 카드를 가리켰다.
- `silbert2001_chute_flow_bagnold_spring_dashpot_hertz_dem` **L473 · L492** — [31] (Vu-Quoc & Zhang · Mech. Mater. 31, 235 (1999)) 과 [32] (Vemuri 외) 가 같은 권 · 쪽이라 *"둘 중 하나는 틀렸다"* 고 남긴 것: 이 원문 목록 (p.4043) 이 *"Vu-Quoc, L. & Zhang, X. 1999a An accurate and efficient tangential force–displacement model for elastic-frictional contact in particle-flow simulations. Mech. Mater. 31, 235–269."* 를 적는다 → [31] 쪽이 맞는다 ([32] 의 원문은 [미확인]).  그 카드는 고치지 않았다 · 🔗 절 끝 한 줄.
- `demirtas2021_mpfem_hollow_sphere_die_compaction` L536 · `harthong2009_high_density_compaction_dem_voronoi_contact_law` L329 · L498 — 'Vu-Quoc 2001' · 'Vu-Quoc, Zhang, Lesburg 2001 … IJSS' 는 **같은 저자 다른 논문** (이 카드와 섞지 말 것) · 두 카드 모두 원문 서지와 모순 없음 → 문제 없음 (demirtas2021 의 관련 카드 표에 '다른 논문' 표지 한 행).
- 원문 안 어긋남 (카드 §3-8 · 고치지 않음 · 카드 문제 아님): C_a 단위 'N m⁻¹' (식 2.5 로는 m N⁻¹) · 식 (3.17) 둘째 항 P 하나 더 · 식 (4.7) 둘째 꼴 분자 · 분모 뒤집힘 + 첨자 한 칸 어긋남 · 그림 12 세로 눈금 라벨 셋 중 하나 ('2 × 10⁻⁴' 가 첫 눈금) 어긋남 · 알고리즘 3.3 판정 (잔차) ↔ 본문 (상대 증분) · P_Y 36.4 (본문) ↔ 36.45 N (그림).
- 스캔 주의 (이 카드 판독): PDF 11 · 13 · 15 · 23 쪽 스캔의 세로선이 기울어 있다 (틀 dx/dy −0.009 ~ −0.013 · 가로선은 수평) — 높이에 따라 x 보정이 달라 이 원문 그림을 다시 판독할 때는 축 가까이에서 읽는다 (14 · 24 · 30 쪽 기울기 없음).

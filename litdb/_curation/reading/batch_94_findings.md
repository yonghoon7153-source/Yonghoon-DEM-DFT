# 배치 94 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-17 · 위시 W-1117-3)

카드 = `tian2017_contact_area_loss_assb_simulation` (원문 = 출판본 10 쪽 (PDF p.2–11 · p.1 = IOP 표지) · SI 안내 없음 · 그림 크롭 67 장 = 도구 6 (그림 1–6 — 6 장 모두 원 래스터에서 다시 자름) +
손 크롭 61 (표 3 · 패널 14 · 식 24 (번호 1–27 전부) · 근거 문단 20 — 이 회차 다시 자름 2) · 판독 원자료 `litdb/figures/<slug>/digitized.csv` 214 행).
서지 (k · l 인용용) = Tian H.-K., Qi Y., *Simulation of the Effect of Contact Area Loss in All-Solid-State Li-Ion Batteries*, J. Electrochem. Soc. 164 (11) (2017) E3512–E3521, DOI 10.1149/2.0481711jes.
⚠ 재료 = 전기화학 **Li | LiPON-like Li₃PO₄ | LiCoO₂ 박막** · 접촉 **Li₃PO₄–LiCoO₂ · LGPS–TiS₂** (LPSCl · NCM 없음) — 계산 = 1-D 전기화학 연속체 + Persson 탄성 · 무점착 접촉 (입자 · DEM · MPM · 소성 · 탈압 없음).  쪽 = PDF 쪽 (인쇄 쪽 = PDF 쪽 + 3510).

---

## a — 순수 SE 압력별 기공 곡선 · 진밀도 · 상태

이 배치에 없음 (기공 · 밀도 0 — SE 는 박막 Li₃PO₄ (1500 nm 연속 층) 와 접촉 계산의 LGPS 탄성 값뿐 · 카드 §3-2).

## b — 압력을 뺄 때 되돌아오는 양 · 잰 방법

- [b] tian2017_… | **하중 해제 · 되돌아옴 계산 · 측정 없음** — 그림 6 은 가압 곡선 하나 (탄성 · 무점착이라 경로 무관 [카드 해석]) · 사이클 효과는 *"(m, I) values were changed to mimic the effect interface roughening due to battery cycling"* (손 변경) | 카드 §0-1 · §3-5 · p.9 | [인쇄] | 'unload' · 'relax' · 'decompress' 0 회 · 'release' 1 회 (Li-ion *"generated and released"* · p.4 · 압력 뜻 아님)
- [b] tian2017_… | 재가압 회복 (계산): film 점 A (≈20 MPa · γ ≈0.70) → 거칠어짐 B (같은 압력 · ≈0.49 · *"around 20% of the contact area is lost"*) → C (*"increasing the contract pressure to 60 MPa will recover the contact area to 70% again"*) · 원 중심 22.4 / 22.7 / 56.9 MPa · 0.706 / 0.490 / 0.705 · 회복 배수 (c_검정/c_분홍)² = 2.58 (Persson 제곱 꼴이면 1.61) | 카드 §3-6 · p.10 · Fig. 6a | [인쇄] · [판독 원 중심] · [카드 산술] | 탄성 가역 · 용량 회복은 계산 아님 (그림 5 직선 역산 제안) · Koerver 2018 의 *"re-tightening … not sufficient"* 는 원문에 없는 문장 (원문 결론 = 더 높은 압력이면 회복)

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- [c] tian2017_… | 항복 · 경도 · 크리프 **값 없음** · 탄성만 (Table 3 = 원문 Table III): Li₃PO₄ E 103.4 GPa · ν 0.26 [36] · LiCoO₂ 171 [37] · 0.2 [69] · LGPS 21.7 · 0.37 [67 = Deng 2016] · TiS₂ 228 · 0.11 [68] → E* film 68.35 · bulk 22.67 GPa | 카드 §3-2 · p.7 | [인쇄] · [카드 산술 식 24] | 일축 환산 없음 · Li 금속: *"low hardness and exhibits creep behavior at room temperature"* (정성 · 계산에서 뺌)

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

이 배치에 없음 (입자 · 복합 압축 없음 — 계면 한 장의 평균장 접촉).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안

- [e] tian2017_… | *"The well-known Hertz, Greenwood-Williamson, and Bush models are not appropriate for large contact area (>50%) because they neglect the interaction between contacted asperities"* → 대안 = Persson 다척도 이론 (*"models the contact area variation from 0% to 100% as a function of applied pressure"*) · 맞춘 값 **0 개** (C(q) = Flys 2015 다른 시료 · E · ν 문헌 · ξ ≈2700 = 1 C Li 확산 길이 3.6 µm 논리 · 사이클 (m, I) 걸음 손 선택) | 카드 §4-3 · p.3 · p.5–7 | [인쇄] | 대상 = 한 계면의 미세돌기 (입자 DEM 아님) · ⚠ 그림 6 곡선은 인쇄 식 26 (1 제곱) 꼴 — 원문 식 22–23 (제곱) 을 적분한 Persson 꼴이면 같은 입력에서 20 MPa 실접촉 ≈1.4 % (그림 ≈70 %) [카드 산술 §3-5]

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙

- [f] tian2017_… | MPM 없음 · 연속체 쪽 '해상도' = 관찰 척도: *"This length scale is estimated to be 3.6 μm, based on √4Dt. So the lower limit of the q is defined by the magnification ξ of around 2700 for A0 = 1 cm2"* (√(4 × 9 × 10⁻¹⁶ × 3600) = 3.60 µm = 전해질 D_Li+ [카드 산술]) · 수치 오차 · 격자 수렴 없음 · FEM 프로그램 [미확인] | 카드 §3-5 · §4-4 · p.5 · p.10 | [인쇄] · [카드 산술] | 지름당 셀 수 규칙 없음 · 분리 조건 = 무점착 P(σ < 0) = 0 (p.7)

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거

- [g] tian2017_… | 1-D → 2-D/3-D: *"The linear relationship may be due to the simplified 1D model and the assumption of worst scenario … more sophisticated 2D and 3D models that can describe the local concentration change and the amount of accessible cathode material more accurately are being developed"* (p.9) · *"For future work, 2-D or 3-D continuum models need to be developed to capture the 2-D and 3-D diffusion of Li in the positive electrode after losing contact"* (p.10) | 카드 §4-5 (iii) | [인쇄] | 2D ↔ 3D 수치 비교 없음 · 같은 그룹 후속 = `tian2020_…` (2.5D 축대칭 · 다른 주제)

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

이 배치에 없음 (DEM 없음).

## i — 복합 양극 (AM + SE) 의 압력별 기공

이 배치에 없음 (기공 없음 · bulk-type 은 그림 2a 개념도와 LGPS–TiS₂ 계면 접촉 비율뿐).

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것

- [j] tian2017_… | 원문 한계 두 문단: *"One limitation of the current 1D model is that it assumes the loss of contact area leads to inaccessible positive electrode materials, which is the worst scenario"* · *"it inherited many assumptions and electrochemical equations derived in liquid electrolyte systems"* (결함 수송 · 분극 · Butler–Volmer) | 카드 §11 · p.10 | [인쇄] | 탈압 · 소성 · 박리 · 이력 · 협착 · 전자 경로는 원문이 한계로도 적지 않음 (모델 밖) [카드 해석]
- [j] tian2017_… | 두 계산이 결합되지 않음: 그림 4–5 의 γ (1 → 0.75) ↔ 그림 6 의 A · B (0.70 · 0.49) · γ ≥ 0.99 는 그림 6a 검은 곡선에서 ≈130 MPa 위 [카드 산술] | 카드 §3-6 · §11 | [판독] · [카드 해석] | '용량 → 잃은 접촉 → 회복 압력' 두 단계 절차 (p.10) 는 외삽 포함

## k — DEM 의 한계 (원문 문장 · 위치)

- [k] tian2017_… (Tian & Qi 2017, J. Electrochem. Soc. 164, E3512) | **말 없음 (DEM 을 쓰지 않음)** · 가까운 문장 (거친 면 미세돌기 모델): *"The well-known Hertz, Greenwood-Williamson, and Bush models are not appropriate for large contact area (>50%) because they neglect the interaction between contacted asperities"* (p.3) · *"a perfect contacted interface at macroscopic view may not be 100% in contact at the nanometer scale"* (p.3) | 카드 §4-5 (i) | [인쇄] | 입자 DEM 의 '접촉끼리 독립' 과 같은 논리 · 대상은 다르다 [카드 해석]

## l — 소성변형이 왜 어려운가 · 우회 · 값

- [l] tian2017_… (Tian & Qi 2017, J. Electrochem. Soc. 164, E3512) | 소성을 '어렵다' 고 하지 않고 **빼는 근거** 로 쓴다: *"Since Li metal has low hardness and exhibits creep behavior at room temperature, it is more likely to maintain a good contact with the solid-electrolyte due to plastic deformation"* (p.2–3 → Li 쪽 계면 제외) · *"The different properties of the contact, such as elastic contact, adhesion or elastoplastic contact can be addressed by changing the initial and boundary conditions of Equation 22. Since both Li3PO4 and LiCoO2 are ceramic materials, the contact is considered to be elastic without adhesion in this study"* (p.7) | 카드 §4-3 · §4-5 (ii) | [인쇄] | 우회 = 평균장 탄성 접촉 (맞춘 값 0 · 비용 언급 없음 · 반해석) · 탄소성 경계 조건은 실행 안 함

## m — 받아들일 통찰

- [m] 접촉 손실을 **두 장부** (반응 면적 i₀ ∝ γ → R_ct ∝ 1/γ · 닿지 않은 물질 → 용량 ∝ γ · 최악) 로 따로 적고 차단 전압 · 율로 어느 쪽이 지배하는지 가른다 · 흐름 밖: A10 사이클 접촉 원장 '접촉-기계 몫 vs 화학 몫' · 단계 6 (탈압 결과 → 성능 벌점) | 왜: 식 17 · 18 · p.8 (3.8 V = 물질 · 4.0 V = 표면 농도 · 확산) | 카드 §4-2 · §9
- [m] **기준 함정** — 4.0 V '기울기 0.34 → 0.26' 은 0.1 C 깊은 용량 기준 · 같은 율 γ = 1 기준이면 상대 손실 24.8 → 36.2 % (접촉 −25 %) = 1.0–1.45 배 · 보고 · 덱에 분모를 적는다 · 흐름 밖: 보고 방식 | 왜: 그림 5 판독 + 카드 산술 | 카드 §3-4
- [m] **문헌 '압력 → 접촉' 법칙은 인쇄 식으로 한 곡선을 재현한 뒤에 쓴다** — 이 논문은 식 23 (제곱) ↔ 26 (1 제곱) 이 다르고 그림 6 이 26 을 따른다 (c 비 0.95–0.99 · 열 곡선) · 재현 없이 쓰면 50 배 다른 실접촉을 '이론값' 으로 들고 온다 · 자리: 결과 전 대조 항목 · 후보 M0 | 왜: 카드 §3-5 | 카드 §3-5 · §8 함정 1
- [m] **접촉 비율은 관찰 척도와 함께 정의** — 반응 · 확산이 고르게 퍼지는 길이 √(4Dt) 보다 작은 무늬는 접촉 비율에 넣지 않는다 (원문 3.6 µm · ξ ≈2700) · 우리 피복 띠 (0.14 µm) · 복셀 선택의 근거 문장으로 · 자리: 단계 0 · 단계 7 | 왜: p.5 | 카드 §3-5 · §9

## n — 논문 에이전트 후보

- [n] W. J. Li, M. Hirayama, K. Suzuki, and R. Kanno, Mater. Trans., 57(4), 549 (2016). (원문 ref 26 · 서지 원문 그대로) | b · R4 · i — 이 논문의 유일한 실험 앵커: 제조 · 운전 압력 19 ↔ 228 MPa (p.2) / 19 ↔ 230 MPa (p.10) 의 사이클 유지율 (In-Li / TiS₂ / Li₁₀GeP₂S₁₂) — 우리 탈압 · 재가압 결과 전 대조 후보 · 카드 §3-6 · §12 | litdb 확인: papers/ ls · 'Mater. Trans' · 'Hirayama, K. Suzuki' · '57(4), 549' grep → 카드 없음 (wishlist 0 회)
- [n] B. N. J. Persson, Surf. Sci. Rep., 61(4), 201 (2006). (원문 ref 49) | e · l · m — 식 25–26 의 원 꼴 (E*/σ₀ 제곱 여부) 확인 + 탄소성 · 점착 경계 조건 (p.7 문장의 근거) — 카드 §3-5 · §12 | litdb 확인: 'Surf. Sci. Rep' grep 0 · 'Persson' 은 다른 Persson (Materials Project) 뿐 → 카드 없음
- [n] B. N. Persson, The Journal of Chemical Physics, 115(8), 3840 (2001). (원문 ref 62) | e · f — 식 22 (ξ 방향 확산 방정식) 의 원전 — 카드 §4-3 · §12 | litdb 확인: '115, 3840' · 'Chem. Phys., 115' grep 0 (wishlist 의 '3840' 1 회는 다른 논문 JES 164 A3840) → 카드 없음
- [n] J. Greenwood and J. Williamson, in "Proceedings of the Royal Society of London A: Mathematical, Physical and Engineering Sciences", Vol. 295, p. 300. The Royal Society, 1966. (원문 ref 43) | e · k — '큰 접촉 (> 50 %) 에서 미세돌기 독립 가정이 깨진다' 의 대상 모델 · 카드 §4-5 (i) · §12 | litdb 확인: 'Greenwood and J. Williamson' · 'nominally flat' grep 0 · 정본 `greenwood1966_constriction_resistance_microcontact_cluster_real_area` 는 다른 논문 (Br. J. Appl. Phys. 17, 1621) → 카드 없음
- [n] O. Flys, S. Kallberg, G. Ged, Z. Silvestri, and B. G. Rosen, Surf. Topogr.-Metrol. Prop., 3(4), 10 (2015). (원문 ref 47) | m — C(q) (RMS 15 · 120 nm) 의 원전 · 정규화 · RMS 범위 확인 (인쇄 (m, I) 로 그린 범위 RMS 112 · 444 nm ↔ 표지 15 · 120 nm [카드 산술]) — 카드 §3-5 · §12 | litdb 확인: 'Flys' · 'Surf. Topogr' grep 0 → 카드 없음

## 카드 문제

- `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` **L29 ⓒ · L178 · L358 · L380** — Koerver 원문의 *"Calculations by Tian et al. have shown that re-tightening a cell is not sufficient to recover capacity fade due to contact loss of materials"* (p.2151) 를 **옳게 옮겼다** (카드 잘못 아님).  다만 L358 (*"쓸 수 있는 문장은 … re-tightening (Tian & Qi 계산 인용)"*) · L380 (*"'re-tightening a cell is not sufficient' 의 원전"*) 처럼 쓰면 귀속이 원문과 어긋난다 — Tian & Qi 2017 원문 10 쪽에 'tighten' · 'sufficient' 0 회 · 원문 결론은 *"increasing the contract pressure to 60 MPa will recover the contact area to 70% again"* · *"suggest how much pressures should be applied to recover the contact area and capacity loss"* (p.10).  같은 압력으로는 접촉이 회복되지 않는다 (점 A → B) 는 좁은 뜻으로만 맞다.  → 그 카드는 고치지 않았다 · 관련 카드 한 줄 (그 카드 🔗 절 끝) 로 새 카드를 가리켰다.
- `ohashi2020_stress_distribution_composite_electrode_sulfide_assb` L339 · `tian2020_electrochemo_mechanical_stress_assb` L606 — 서지 · 주제만 (숫자 옮김 없음) · 문제 없음 (ohashi2020 [7] 의 'Electrochem. Soc.' 는 Ohashi 원문 목록의 꼴 · 그 카드에 이미 적힘).

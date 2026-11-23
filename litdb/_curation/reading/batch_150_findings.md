# batch 150 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-23 · 후보 표 N-112 둘째 · 새 카드)

대상: `li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation` — Hongming Li · J. J. McCarthy\*, "Phase diagrams for cohesive particle mixing and segregation", *Phys. Rev. E* 71 (2), 021305 (2005) · DOI 10.1103/PhysRevE.71.021305.
액체 다리 (물 ≈1 vol%) 로 점착한 이원 유리 · 아크릴 구 (반지름 0.25–1.0 mm) 를 반 채운 준 2D 회전 드럼 (≈14 cm × 2 cm · 308 mL · 6–9 rpm) 에서 ≈30 바퀴 돌린 점근 상태를 사진 농도 표준편차 IS 로 재고, 쌍별 입상 Bond 수의 비 ℜ1 = Bo_g11/Bo_g12 · ℜ2 = Bo_g22/Bo_g12 (식 3–6) 와 인쇄된 경계식 (식 7–8) 으로 M 상 (점착이 분리를 줄임) · E 상 (키움) 을 예측 · 검증하고 3D DEM (Hertz–Mindlin + Lian–Thornton) 두 쌍으로 교차 확인한 논문 (PRL 2003 = 정본 `li2003_…` 의 긴 판) — 압밀 · 고체전해질 없음.
쪽 = PDF 쪽 p.1–8 (인쇄 021305-1 … -8) · SI 없음 · 고른 의도 대조 = **일부** (점착 모델 · ℜ · 인쇄 경계식 · 상태도 · 실험 · DEM · IS 채움 / 'Bo 축' = Bo 비 ℜ 축으로만 (그림 6 · 그림 2 등고선) / 회전 속도 효과 · 절대 Bo 범위 없음 · 카드 §0-1).
인용 서지 (질문 k · l 용): H. Li, J. J. McCarthy, *Phys. Rev. E* 71, 021305 (2005), DOI 10.1103/PhysRevE.71.021305.
⚠ 이 PDF 의 글자 층은 '≈' 를 '<' 로 뱉는다 — 숫자는 모두 렌더에서 확인 (≈1 % · θ ≈20° · ≈60°).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 압밀 · 고체전해질 없음 (중력 아래 회전 드럼 혼합 · 유리 / 아크릴 구 · 카드 §0 · §3-4).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 압력 · 탈압 없음 (카드 §4-3 ④).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 기계 물성 값 0 (강체 mm 구 · DEM 의 강성 값도 인쇄 없음 · 카드 §3-7).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 압축 · 하중 몫 없음.  가장 가까운 것은 크기 · 밀도가 다른 두 종의 점착 쌍 비 (하중 아님): 작은 쪽이 더 무거우면 (αβ³ > 1) ℜ2 > 1 이 늘 참 — *"the 'mixing' interaction is always weaker than the interaction of the two largest particles"* (식 7 · p.2 · 카드 §3-2).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation | 큰 변형 · 대안 법칙 논의 **없음** — DEM 접촉 = *"the collisional forces are modeled after the work of Hertz and Mindlin [28]"* · 점착 = *"modeled after the work of Lian and Thornton [29,30]"* · 다리는 접촉 순간 생기고 끊김 간격까지 유지 · 다리 액량 상수 = *"0.1% of the volume of the largest particle"* (≈4.19 × 10⁻³ mm³ [카드 산술]) · 맞춘 값 0 개 (인쇄된 맞춤 없음) · 강성 값 · 마찰 · 반발 [미확인] | 카드 §3-7 · p.6 · `txt_p6_dem_hertz_mindlin_lian_thornton_bridge_01pct.png` | 인쇄 · 카드 산술 | 점착 법칙이 우리 SJKR 과 다르다 (액체 다리 vs 건식 표면 에너지) · 소성 접촉 아님

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 — MPM 없음.

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation | **증거 하나 (약함)** — 실험 IS = 준 2D 드럼 앞면 사진 · DEM IS = 3D 전체: *"the method of IS calculation differs between the computations (which can probe the full three-dimensional flow) and the optical technique used for experiments (which is limited to surface and wall measurements). Nevertheless, there is a surprising degree of agreement between the simulated IS percentage changes"* — 두 쌍 7b +23 ↔ 4i +24 % · 7d −29 ↔ 5b −29 % · 이전 규칙 · 경고 없음 | 카드 §3-7 · §4-3 ③ · p.7 · `txt_p6_p7_dem_cases_stiffness_lowered_is_3d_vs_surface.png` | 인쇄 | 변화 % 만 맞음 (IS 절대값 · 무늬 아님) · 쌍 둘 · 우리 3D DEM 드럼 (반지름 13.14 mm · Fr 0.0827) 과 회전 세기 다름

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 — DEM 만 (넘김 없음).

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — 전지 재료 · 압력 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation | 원문 스스로 적은 한계 넷 — (i) *"geared toward systems where the liquid bridges act only pairwise (i.e., the system is in the pendular regime)"* (p.2) (ii) *"directly comparing pairwise particle interactions neglects both multiparticle interactions as well as the reality that for small size ratios the probability of the three types of pairwise interactions may be very different (so some scaled comparison would be warranted)"* · 0.25 (16 : 1) 까지 확인 (p.2) (iii) E 쪽 거시 줄무늬 *"beyond our expectation"* (p.4–5) (iv) *"we have expressly avoided the effect of both liquid-bridge viscosity [9] and volume [10,11]"* (p.7) | 카드 §3-9 · §11 · p.2 · p.4–5 · p.7 | 인쇄 | 가압 · 탈압과 직접 닿지 않는다 — 압밀 DEM 의 **초기 배치 (혼합 상태)** 단계의 한계 (점근 · 느린 회전 · 쌍별)

## k — DEM 의 한계
- [k] li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation (H. Li · J. J. McCarthy, *Phys. Rev. E* 71, 021305, 2005) | **말 있음 (셋 · 소성 · 큰 변형 한계는 아님)** — ① 강성 연화: *"the particle stiffness is lowered to facilitate more rapid computations without affecting kinematic results [33]"* (p.6 · 값 · 겹침 미인쇄) — ★ 근거 [33] = O. R. Walton, Mech. Mater. 16, 239 (1993) 의 정본 카드 (`walton1993_…` p.246) 는 *"An unanticipated finding is the pronounced sensitivity of the velocity and character of the deeper flows to the effective stiffness"* (얕은 흐름만 둔감 · 동적 겹침 ≈0.5 % of d) → '운동학 불변' 은 조건부 · 이 논문은 조건을 확인할 숫자를 적지 않았다 ② 다리 단순화: *"For simplicity, bridges form at the instant of interparticle contact and persist until the separation between surfaces is sufficient to rupture the bridge. Also, the liquid content of each bridge is assumed to be a constant"* (p.6) ③ 관측 차원: 계산 = 3D 전체 ↔ 실험 = 표면 · 벽 (p.7) | 카드 §3-7 · §4-3 ① · p.6–7 · `txt_p6_p7_dem_cases_…` · `txt_p6_dem_hertz_…` | 인쇄 · 카드 해석 (정본 카드 대조) | 연화 근거를 이 논문 + Walton 으로 인용할 때 '깊은 흐름 · 큰 겹침에서는 강성이 운동학을 바꾼다' 를 함께 적는다

## l — 소성변형이 왜 어려운가 · 우회 · 값 · 비용
- [l] li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation (H. Li · J. J. McCarthy, *Phys. Rev. E* 71, 021305, 2005) | **논의 없음** — 강체 mm 유리 · 아크릴 구 · Hertz–Mindlin 탄성 · 식 (2) 에 탄성 · 소성 항 없음 · 우회 = 계산 속도를 위한 강성 낮춤 하나 (값 · 맞춤 대상 · 비용 [미확인]) | 카드 §4-3 ② · §3-7 | 인쇄 · 카드 해석 | 소성 · 큰 변형 문헌이 아니다

## m — 받아들일 통찰
- [m] li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation | **ℜ (Bo 비) → 상 → 혼합 변화 부호를 결과 전에 적는 꼴** — 같은 처음 상태 · 점착만 다른 짝 (마름 ↔ 젖음) 의 IS 변화 부호가 11/11 로 예측 상과 같았다 (그림 6 사분면 · Pearson 평균 ℜ −0.91 [카드 산술]) → 우리 B2-U ↔ B2-C: 기하평균으로 SE/AM_P · SE/AM_S 부분계 U = E (ℜ1 1.76 · 1.98) · C = M (0.556 · 0.625) [우리 산술] — SE 군집 분율 · AM–SE 접촉 분율의 기대 방향을 판독 전에 | 흐름 밖: Ⓒ 믹서 (결과 전 대조 항목) — 왜: 판독이 ℜ 분류를 따르면 교차 확인 · 어긋나면 (건식 · 충돌 · 벽 · 거친 입자) 정보 (카드 §3-6 · §7-3 · §9-1 · p.6)
- [m] li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation | **B1 과 B2 는 ℜ 가 같다** — ℜ 는 모든 쌍을 같은 배율로 키우면 변하지 않는다 (B2 = B1 × 100) → B1 ↔ B2 차이는 '상' 이 아니라 **절대 Bo** 효과 (B1 = 모든 쌍 < 1 · 원문 시험 쌍은 1.5–107 [우리 산술 · γ 가정]) | 흐름 밖: Ⓒ 믹서 · 다음 팔 설계 — 왜: 상 (M ↔ E) 을 가르려면 γ_AM/γ_SE (U ↔ C) 를, 점착이 드러나는 문턱을 보려면 절대 배율 (B1 ↔ B2) 을 바꾼다 — 두 노브의 몫을 섞지 않는다 (카드 §7-3 · p.2)
- [m] li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation | **작은 크기비에서는 쌍 확률을 넣는다** — 원문 검증 하한 0.25 (*"interaction probability ratios of 16 to 1"*) · *"some scaled comparison would be warranted"* ↔ 우리 SE/AM_P 0.111 (81 : 1 [카드 산술]) | 흐름 밖: Ⓒ 믹서 판독 — 왜: ℜ 만으로 SE/AM_P 를 분류하지 말고 군집을 무작위 대비로 잰다 (논지 §2-3 ⚠ 와 같은 결론) (카드 §3-2 · §9-5 · p.2)
- [m] li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation | **연화 근거는 인용이 아니라 시험** — '강성을 낮춰도 운동학 불변 [33]' 이 근거 문헌 (Walton 1993 · 깊은 흐름 강성 민감) 과 긴장 | 후보 D0 · 믹서 덱 강성 배율 (겹침 계약 · 민감도 팔) — 왜: 같은 인용 사슬을 우리 덱 정당화에 쓰면 반례가 그 원전 안에 있다 (카드 §3-7 · §9-6 · p.6)

## n — 논문 에이전트 후보
- [n] D. Geromichalos, M. Kohonen, F. Mugele, and S. Herminghaus, Phys. Rev. Lett. 90, 168702 (2003). (원문 참고 [11] · 서지 일부만 — 목록에 제목 없음) | j · m (G3) — 흐름 세기 (forcing velocity) 에 따른 젖은 입자 혼합 / 분리 상 · 이 논문이 자기 흐름을 그 *"mixing" phase* 에 놓고 회전 축을 뺀 근거 → 우리 rpm (Fr) 축의 문헌 자리 (카드 §0 ⑨ · §7-4 · §12) | litdb 확인: papers/ 619 목록 (이 카드 포함) · 'geromich' ls 0 · '168702' · 'Geromichalos' grep 0 · wishlist 0 → 카드 없음
- [n] G. Lian, C. Thornton, and M. J. Adams, J. Colloid Interface Sci. 161, 138 (1993). (원문 참고 [29] · 서지 일부만) | e · m — 이 논문 DEM 의 액체 다리 힘 · 끊김 모델 (점착 법칙의 대안 · 다리 생성 / 끊김 규칙) (카드 §3-7 · §12) | litdb 확인: ls 'lian' = liang2025 · liang2026 (다른 논문) · 'Interface Sci. 161' grep = nase2001 카드의 인용뿐 → 카드 없음
- [n] D. V. Khakhar, A. V. Orpe, and S. K. Hajra, J. Phys. A 318, 129 (2003). (원문 참고 [23] · 서지 일부만 · 학술지 표기는 원문 목록 그대로 — 확인 필요) | j · m — 점착 차이 → 시간에 따라 변하는 표면 각 → 거시 줄무늬 (그림 4 d–f 의 설명 후보 · 우리 Lacey 칸 판독이 비반경 무늬에 어떻게 반응하는지) (카드 §3-5 · §12) | litdb 확인: 'khakhar' ls 0 · 'J. Phys. A 318' · 'Orpe' grep 0 → 카드 없음
- [n] A. Samadani and A. Kudrolli, Phys. Rev. E 64, 051301 (2001). (원문 참고 [10] · 서지 일부만) | j — 사이 액량 효과 (이 논문이 결론에서 뺐다고 적은 축 · 같은 저자 PRL 85, 5102 (2000) = [9] 는 batch 149 의 n 으로 이미 wishlist) (카드 §12) | litdb 확인: 'samadani' ls 0 · '051301' grep 0 → 카드 없음
- [n] T. Mikami, H. Kamiya, and M. Horio, Chem. Eng. Sci. 53, 1927 (1998). (원문 참고 [31] · 서지 일부만) | e · k — 다리 단순화 (접촉 때 생김 · 상수 액량) 를 *"consistent with existing literature [30–32]"* 라 한 근거의 하나 (카드 §3-7 · §12) | litdb 확인: 'mikami' ls 0 · 'Eng. Sci. 53, 1927' grep 0 ('Mikami' grep = morrissey2013 · paulick2015 의 인용뿐) → 카드 없음

## 카드 문제
- `jarray2019_cohesion_driven_mixing_segregation_drum` **L322** (참고문헌 표 ref 14 · 20 의 '왜' 칸) — *"점착 혼합 상태도 (Bo 축)"* : 이 PRE (ref 20) 의 상태도 축도 **크기비 R1/R2 × 젖음비 cos θ1/cos θ2 (판 = 밀도비)** 이고, Bo 는 **비 ℜ_i = Bo_gii/Bo_g12** 로만 축에 나온다 — 그림 2 왼쪽 점선 등고선 값 · **그림 6 의 가로축** (원문 p.3 *"the left-most plot in Fig. 2 shows dashed lines corresponding to various values of ℜi > 1"* · p.6 *"Figure 6 shows the variation of the mixing extent change [Eq. (10)] as a function of ℜi"*) · 절대 Bo 값은 없다 → **일부** ('Bo 비 (ℜ) 축' 이라야 맞다).  서지 (*"Phys. Rev. E 71, 021305 (2005)"*) · *"점착으로 분리 조절"* 은 원문과 같다.  (PRL 쪽은 batch 149 카드 문제 절에 이미 적힘 · 같은 문구가 후보 표 S8 N-112 '왜' 칸에도 있다 — 후보 표 · 카드 아님.)
- `li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy` — **문제 아님 (기록)**: L48 · L64 의 *"PRE 2005 … [미확인]"* 은 이번 원문 확인으로 풀렸다 (위 줄과 같은 판정) · §3-3 의 카드 유도 경계 (c = 2/(1+r) · (1+r)(ρ1/ρ2)r²/2) = 이 논문 식 (8) 과 같다 · §3-7 의 PRL 그림 4a 판독 (실선 0.557 · 점선 ≈2.10) 과 이 논문 그림 2 오른쪽 판독 (0.535 · 1.88) 이 다른 것은 두 논문이 같은 그림을 다른 밀도비로 다시 그린 것 (각 논문 안의 어긋남) — 고치지 않았고 🔗 관련 카드 한 줄 (L389) 만 이 slug 로 바꿨다.
- 그 밖: 정본에서 이 논문을 인용한 카드는 jarray2019 · li2003 둘 (papers/ 618 목록 (이 카드 뺀) + '021305' · 'PhysRevE.71' · 'Phase diagrams for cohesive' · 'McCarthy' grep).

## 공백 검사 G1–G4 (★ 이 카드의 핵심 산출 · 카드 §0-2 와 같은 판정)
- **G1 — 점착 대비를 설계 변수로 혼합 결과 (덮임 ↔ 뭉침 · 섞임 ↔ 분리) 를 예측** → **반례** (섞임 ↔ 분리 · 정량 부호까지) · **일부** (덮임 ↔ 뭉침) | 근거: 초록 *"manipulation of surface properties and/or size/density ratios provides a method to control cohesive particle mixing and segregation"* (p.1) · 젖음비 λ = 상태도 축 (그림 2) · 식 (8) · 11 쌍의 IS 변화 부호 = 예측 상 (표 II · 그림 6 · p.6 *"Our theory would predict that all experiments should lie in either the upper left or lower right quadrants (as our critical values do)"*) · 덮임 ↔ 뭉침은 말로만 (*"the smaller ones will adhere to the larger ones (a simple physical example might be sand sticking to a bowling ball)"* p.3 · *"larger particles cluster together and exclude smaller ones"* p.2) — 덮임 관측량 없음 | 좁힐 문장: "점착 대비로 섞임 ↔ 분리 상을 예측하고 혼합 변화의 **부호** 를 11 쌍 + DEM 2 쌍으로 맞춘 선례 = Li & McCarthy 2003 / 2005 (액체 다리 · mm 구 · 준 2D)" → 우리 몫 = **건식 표면 에너지 (결합 규칙) · µm 3 상 (크기비 0.111 = 검증 밖) · '덮임' 정량 (AM–SE 접촉 분율 · SE 군집 분율 무작위 대비)**.
- **G2 — 점착 입력을 따로 재고 (AFM · IGC · 접촉각 등) 혼합 결과를 미리 예측** → **반례** (접촉각 입력 → 상 · 변화 부호) | 근거: p.4 *"The wetting angles of beads are measured by inspection of magnified images of roughly microliter sized droplets on actual particle surfaces."* · 표 I θ (20° · 60° · 50° · 70°) → 식 (5)–(6) → 표 II ℜ (카드 재계산과 같음) → 상 · 변화 부호 · 한정: 힘 · 표면 에너지 측정 없음 · γ 값 없음 · 혼합쌍 min 가정 · 사전 등록 표지 없음 · 반복 없음 | 좁힐 문장: "따로 잰 점착 입력 (접촉각) → 혼합 변화 부호 예측의 선례가 있다" → 우리 몫 = **같은 SE 탐침 AFM 힘 비 (또는 IGC γ) 로 W_AS 를 결합 규칙 없이 재고, ℜ 와 DEM 판독의 크기를 결과 전에 등록**.
- **G3 — 회전 속도 최적을 입자 수준 맞교환 (덩어리 풀림 ↔ 벽 부착 손실 등) 으로 설명** → **없음** | 근거: p.1 *"we operate the tumbler in the continuous flow regime, yet at a sufficiently slow rotation rate that the shearing force is considerably smaller than the particle weight"* · p.3 *"Experimentally we restrict the rotation speed such that it is sufficiently small (6–9 rpm)"* · p.7 *"we have expressly avoided the effect of both liquid-bridge viscosity [9] and volume [10,11]"* · 벽 = 소수성 실란 (p.3) · 흐름 세기 의존은 Geromichalos [11] 인용 (p.1) | 좁힐 필요 없음 (이 논문 기준) · ⚠ ℜ 이론 = 느린 회전 (Fr 0.0028–0.0063 [카드 산술]) 극한 ↔ 우리 Fr 0.0827 — 다음 대조 = 후보 표 N-151 (Li & McCarthy 2006 전단 판) · n 의 Geromichalos 2003.
- **G4 — 공정 × 재료 상태도 (회전 세기 × 점착 · Bond 수 등) 가 다른 재료로 옮겨 감** → **일부** | 근거: 상태도 = 재료 × 재료 (β × λ · 판 α) · 유리–유리 (크기비 0.25–1) → 아크릴–유리 (α 0.56) → 3D DEM 짝 (7a–7d) 으로 옮겨 맞춤 (p.4–7) · 공정 축 (회전 · 충전 · 액량) 없음 · 원문 적용 한계 *"works well even down to size ratios of 0.25 (i.e., interaction probability ratios of 16 to 1)"* (p.2) | 좁힐 문장: "ℜ 상태도 (재료 축) 의 재료 · DEM 이전은 선례가 있다" → 우리 몫 = **회전 세기 (Fr · Co) 를 더한 공정 × 재료 지도 + 크기비 < 0.25 에서 쌍 확률을 넣은 비교 + 건식 µm 3 상**.

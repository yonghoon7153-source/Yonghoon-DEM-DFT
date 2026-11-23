# batch 158 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-24 · 후보 표 N-153 · 새 카드)

대상: `liu2013_wet_cohesive_particles_transverse_mixing_rotating_drum_circulation_period` — P. Y. Liu, R. Y. Yang, A. B. Yu, "DEM study of the transverse mixing of wet particles in rotating drums", *Chem. Eng. Sci.* **86** (2013) 99–107 · DOI 10.1016/j.ces.2012.06.015.
같은 구 (1.3 mm · 색만 다름 · 15,000–47,000 개) 를 좌우로 나눠 넣은 3D 드럼 (70 × 26 mm) 에 정적 액교 모세관력 (모든 쌍 · 벽 같은 표면장력 0–0.093 N/m · 액량 0.5 %) 을 넣은 in-house DEM 으로 표면장력 · 회전 속도 (5–35 rpm · Fr 0.001–0.05) · 충전율 (30–92 %) 에 따른 가로면 Lacey 지수 M(t) = M∞ erf(kt) 를 재고, 마른 입자의 64 % 충전 이상 (최저) 을 순환 주기 표준편차의 최소로 설명한 뒤 Ding 2002 의 회전 영역 모형을 흐름선별 순환 주기로 넓힌 해석 식 (7 · 부록 A) 으로 평균 · 표준편차를 예측한다.
쪽 = 인쇄 p.99–107 (PDF p.1–9) · 그림 13 (패널 포함 · 그림 2 · 4 · 7 = 래스터 (글자는 벡터) · 나머지 벡터) · 표 2 · 번호 식 17 (본문 7 + 부록 10) · SI 없음 · 계산 = DEM · 실험 0 · 고른 의도 대조 = **일부** (점착 (액교) × 회전 속도 × 충전율 DEM · '점착은 대체로 혼합을 낮춤' · '64 % 에서 마른 입자 최악' = 채움 / '우리 드럼과 같은 꼴의 공정 축 선례' = 일부 (드럼 · 충전율 규약은 같고 점착 대비 · 크기 · Fr · 처음 배치가 다름 · rpm 축 3 점) / G4 = 일부 / 가리킨 카드 없음 (1저자 업로드)).
인용 서지 (질문 k · l 용): P. Y. Liu, R. Y. Yang, A. B. Yu, *Chem. Eng. Sci.* **86** (2013) 99–107.
⚠ 글자 층은 그리스 문자 · 기호를 깨뜨린다 (γ→g · ω→o · β→b · µ→m · '='→'¼' · '−' 빠짐) — 인용문 · 식 · 숫자는 전부 200–400 dpi 렌더 (크롭 = 번호 식 17 + 문장 안 식 7 + 표 1 줄 4 + 근거 문단 19) 에서 옮겼다 · 그림 값은 벡터 마커 판독 (digitized.csv 357 행).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (고체전해질 · 압밀 · 기공 없음 — 액교 점착 유리구의 회전 드럼 혼합).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 (압력 · 탈압 없음).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 (기계 물성 측정 0 — E 1.0 × 10⁷ Pa · ν 0.29 · 감쇠 · 마찰은 DEM 접촉 입력이고 출처 · 근거 미기재 · 표 2).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (압축 · 하중 분담 없음 — 같은 입자 이원).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 (겹침이 작다 — 최대 모세관력에서 2.0 µm (0.16 % d) · 40 % 바닥 무게에서 3.2 µm (0.24 % d) [카드 산술 · 카드 §4-4 (i)] · 접촉 법칙은 Hertz + 비선형 감쇠 그대로 · 대안 논의 없음).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 없음).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] liu2013_… | (흐름 밖: 믹서) **3D DEM 의 가로면 결과를 2D 해석 모형이 재현한 정도** — 순환 주기 평균 ⟨T⟩ 는 *"the agreements between simulation results and theoretical predications are quite well for the mean circulation period"* (p.105) · 표준편차는 *"at least qualitatively"* · 낮은 충전에서 *"the model consistently over-estimates s(T) for low filling levels"* (p.105) — 원인 = *"the model does not consider the diffusive motion of particles which is more prominent at low filling levels"* (p.106) · 크기: ⟨T⟩ 낮은 충전 −2.5 – −9 % · f_d ≥ 0.66 에서 0 – +2 % · σ(T) 모형 / 시뮬레이션 마름 1.82–1.93 · 젖음 1.99–2.40 (f_d ≤ 0.69 · 최소 자리 포함 — 위치는 맞고 값은 ≈2 배) ↔ 0.85–1.18 (f_d ≥ 0.75) [카드 산술] · 3D 쪽 장치 = 끝벽 마찰 0.05 (*"To minimise the effect of end wall in the current study, the particle–end wall sliding friction is reduced to 0.05, as suggested by Taberlet et al. (2006)."* p.100) · 칸 = 드럼 길이 전체 (가로면만) | 카드 §3-9 · §4-4 (iii) | [인쇄] · [카드 산술] | 2D 모형은 같은 3D 시뮬레이션에서 잰 ε · f_d 를 입력으로 쓴다 · 축 방향 혼합 · 끝벽 효과의 크기 미측정

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] liu2013_… | **가압 · 탈압과 닿는 한계 없음** — 원문이 스스로 남긴 것은 믹서 쪽: *"it is not clear why filling level at 64% has the smallest standard deviation. It is also unclear if the current results can be extended to other systems."* (p.104) · 정적 다리만 (*"The current study considered only the static capillary force while the dynamic effect of liquid bridge due to moving particles was neglected."* p.100) · 모형에 확산 없음 (p.106) | 카드 §3-8 · §3-9 · §4-4 · §11 | [인쇄] | 압밀 계산과 무관 — 믹서 판독에만

## k — DEM 의 한계
- [k] liu2013_… (P. Y. Liu, R. Y. Yang, A. B. Yu, *Chem. Eng. Sci.* 86, 99–107, 2013) | **단단한 구 · 점접촉 · 접촉 독립 자체의 한계는 말 없음** — 점착 (액교) 모델의 한계 문장만: *"We also note that, while the capillary force for two particles is well established, its calculation is much more complicated for a moving bed due to lack of the knowledge of particle wetting and liquid distribution."* (p.101) · *"In the present study, the minimum separation distance was treated as a fitting parameter."* (p.101) · *"Note that we did not consider the deformation of liquid bridge in the simulation and always assumed the liquid bridge to be symmetric against the line contacting the centres of two particles."* (p.101) · 맞춘 값 = S_min 5 µm · 다리 액량 몫 5 % (*"these assumptions with S_min of 5 µm and 5% of liquid contributing to liquid bridges compared with the experimental results quite well"* p.101 · 맞춘 대상 = Liu 2011 의 흐름 꼴 · 최대 흐름 안식각 · 무너짐 빈도 p.100) · E = 1.0 × 10⁷ Pa 의 근거 · 연화 여부는 미기재 (같은 그룹 chandratilleke2010 은 '계산 시간 때문' 연화라고 적음) | 카드 §3-2 · §4-1 · §4-4 (i) · §11 | [인쇄] | DEM 접촉 한계의 근거로는 못 쓴다 · '점착 모델 매개변수는 맞춤 값' 의 근거로 인용

## l — 소성변형이 왜 어려운가 · 우회 · 값 · 비용
- [l] liu2013_… (같은 서지) | **논의 없음** (혼합 흐름 · 겹침 < 0.3 % d [카드 산술] · 소성 · 압축 없음) — 비용만 인쇄: *"it took about 4–15 CPU hours to simulate 1 s real time on an Intel 2.0 GHz Xeon PC"* (p.101 · 15,000–47,000 입자 · E 10⁷ Pa) → 15 rpm 10 바퀴 = 160–600 CPU h [카드 산술] | 카드 §3-1 · §4-4 (ii) | [인쇄] · [카드 산술] | 소성 · 큰 변형 문헌이 아니다

## m — 받아들일 통찰
- [m] liu2013_… | **rpm 팔은 회전당 k 와 시간당 k 를 함께 보고한다** — 시간당으로는 모든 경우 회전이 빠를수록 빨리 섞이지만 (*"particle mixing is faster with increasing rotation speed for both dry and wet particles"* p.102) 회전당으로는 마른 입자만 줄고 (0.471 → 0.387 rev⁻¹ · 5 → 35 rpm · Fr ×49 · −18 %) 젖은 입자는 평평 (−3 – +6 %) [판독 · 그림 6] — 같은 '2 바퀴' 비교는 회전당이다 · 저자 해석 = 미끄럼 (*"the bed turn-over time does not proportionally decrease with increasing rotation speed"* p.102 · 자료 없음) | 흐름 밖: Ⓒ 믹서 rpm 공정 축 (G3) | 카드 §3-6 · §9 항목 1 | [인쇄] · [판독] | 40 % 한 충전 · 세 점 · 반복 없음
- [m] liu2013_… | **rpm 축 수준 = 문헌과 겹치는 Fr 두 점 + 지금 덱** — 우리 드럼 (R 12.583 mm) 에서 Fr 0.0088 (이 논문 15 rpm) = 25.0 rpm · 0.048 (35 rpm) = 58.4 rpm · 0.0827 = 76.7 rpm · 2 바퀴 벽시계 ≈77 · 33 · 25.1 시간 (B1-U 실측 25.13 h 를 rpm 비례 · 충전 · 정착 몫이 고정이면 느린 쪽은 더 짧다 · 25 rpm 은 48 h 상한 초과 → 재개 계획) · 기대 효과 (마름 환산 2 바퀴 ΔM ≈ 0.05–0.1) ≈ B1 프레임 간 SD (U 0.073–0.088 · C 0.060–0.078) → 시드 · 프레임 반복을 먼저 정한다 | 흐름 밖: Ⓒ 믹서 rpm 공정 축 (G3 · G4) | 카드 §3-10 · §9 항목 2 | [카드 산술] · [우리 산술] | 이 논문은 Co·λ² ≫ 1 (젖음) 영역만 · 우리 B2-U 는 Co ≈ 1 근처 (k 에 따라) — 영역 경계는 이 논문이 시험하지 않음
- [m] liu2013_… | **충전율 규약이 우리 덱과 같다 · 우리 30 % 에는 비혼합 핵이 없다** — 정의 *"the bulk volume of dry based packed bed (with packing density of 0.6) to the drum volume when the drum is in a static state"* (p.101) = `make_mixer_deck.py` 의 fill 0.30 · pack 0.60 · 30 % 칸은 모든 점착 수준에서 M(10 바퀴) ≥ 0.966 (그림 8a [판독]) · 부록 모형 (A.1 · δ0 = cos φ + ε) 에서 핵은 cos φ < −ε 일 때만 = 동적 충전 > 50 % 에서만 [카드 산술] → 64 % 이상 · 핵 · 92 % 붕괴 같은 고충전 결과를 우리 해석에 끌어오지 않는다 | 흐름 밖: Ⓒ 믹서 판독 해석 | 카드 §3-7 · §3-9 · §9 항목 5 | [인쇄] · [판독] · [카드 산술] | 모형은 회전 (구르기) 영역 · 미끄럼 없음 가정
- [m] liu2013_… | **순환 주기 ⟨T⟩ · σ(T) 와 반지름 변위 Δr 를 덤프에서 낸다 + Lacey 시간 법칙을 erf · 지수 둘 다 맞춘다** — 바닥 이등분선 통과 기록 하나로 ⟨T⟩ · σ(T) (대류 성분) · Δr 가우스 폭 (확산 성분 · γ 0 → 0.073 에 σ_Δr 2.28 → 1.21 d [판독 · 정규 가정]) 이 나온다 · *"smaller standard deviation means particles moving with similar pace which is unfavourable to mixing"* (p.104) · erf 가 지수 꼴보다 rms 1.4–1.8 배 작음 (그림 5a 재맞춤 [카드 산술]) → 점착 대비 (U ↔ C) 가 SE 의 흐름층 통과 빈도 · 반지름 확산을 어떻게 바꾸는지로 'M 이 왜 다른가' 를 쪼갠다 | 흐름 밖: Ⓒ 믹서 판독 관측량 (G3) | 카드 §3-5 · §3-8 · §9 항목 3 · 4 | [인쇄] · [판독] · [카드 산술] | 이원 같은 입자 · 정상 흐름에서 잼 · 우리 3 상 parcel 에서 이등분선 정의는 새로 정해야

## n — 논문 에이전트 후보
- [n] Liu, P.Y., Yang, R.Y., Yu, A.B., 2011. Dynamics of wet particles in rotating drums: effect of liquid surface tension. Phys. Fluids 23, 013304. (원문 참고 목록 · 저자-연도) | ★ k · m (G2) — 이 논문 점착 모델의 **맞춤 근거** (S_min 5 µm · 다리 액량 몫 5 % 를 흐름 꼴 · 최대 흐름 안식각 · 무너짐 빈도 실험에 맞춤 · p.100–101) · 표면장력별 흐름 영역 (그림 3 의 연속 ↔ 무너짐 전이) 의 원 자료 → 점착 DEM 매개변수를 어떤 관측량에 어떻게 맞췄는가 (우리 SJKR CED 를 AFM W 에서 바로 낼지의 대조) | litdb 확인: papers/ 에 카드 없음 (`git grep` '013304' · 'Dynamics of wet particles' 0) · wishlist 없음
- [n] Ding, Y.L., Forster, R., Seville, J.P.K., Parker, D.J., 2002. Granular motion in rotating drums: bed turnover time and slumping-rolling transition. Powder Technol. 124, 18–27. (원문 참고 목록) | m (G3) — **바닥 회전 시간 (bed turnover time)** 과 무너짐–구르기 전이 · 이 논문 모형 (식 7 · 부록 A) 의 바탕 (p.105) · 회전당 k 의 rpm 의존을 '미끄럼 → 회전 시간' 으로 읽은 저자 제안 (p.102) 의 측정 근거 후보 → 우리 rpm 팔의 영역 판정 (Fr 0.0827 이 구르기인가) | litdb 확인: papers/ 에 카드 없음 (`git grep` 'bed turnover' 0 · 'Ding, Y' = matsusaka2010 의 다른 공저 목록뿐) · wishlist 없음
- [n] Finnie, G.J., Kruyt, N.P., Ye, M., Zeilstra, C., Kuipers, J.A.M., 2005. Longitudinal and transverse mixing in rotary kilns: A discrete element method approach. Chem. Eng. Sci. 60, 4083–4091. (원문 참고 목록) | m (G3) — 비점착 DEM 의 회전 속도 · 충전율에 따른 가로 · 축 혼합 (이 논문이 지수 시간 법칙의 출처로 인용 · p.102) → rpm 축 비점착 기준선 (N0 꼴) 의 DEM 선례 · 시간 법칙 (지수 ↔ erf) 대조 | litdb 확인: papers/ 에 카드 없음 (`git grep` 'Finnie' 0 · 'rotary kiln' = khakhar1999 의 다른 논문 (Henein) 뿐) · wishlist 없음
- [n] Brewster, R., Grest, G.S., Levine, A.J., 2009. Effects of cohesion on the surface angle and velocity profiles of granular material in a rotating drum. Phys. Rev. E 79, 011305. (원문 참고 목록) | m (G3 · G4) — 점착이 표면 각을 키우고 흐름층을 두껍게 한다는 근거 (이 논문 그림 3 · 6d → 8d 와 같다고 인용 · p.101–102) · 흐름층 속도 · 두께 측정 → Co 의 k (흐름층 두께 ÷ 반 현) 를 점착 수준별로 정하는 근거 (khakhar1999 카드 §3-9 의 k ≳ 0.1 추정 보완) | litdb 확인: papers/ 에 카드 없음 (`git grep` 'Brewster' · '011305' 0) · wishlist 없음
- [n] Dury, C.M., Ristow, G.H., 1999. Competition of mixing and segregation in rotating cylinders. Phys. Fluids 11, 1387–1394. (원문 참고 목록) | m (G1) — 크기가 다른 입자의 드럼 혼합 · 분리 경쟁 · 가장 나쁜 충전율 ≈65 % (이 논문 p.103 의 인용) → 우리 3 상 (크기 대비 9 배) 드럼의 분리 몫 대조 (이 논문은 같은 입자라 분리 0) | litdb 확인: papers/ 에 카드 없음 (`git grep` 'Dury' · 'Competition of mixing' 0) · wishlist 없음
- (후보 수 밖 메모) McCarthy 2003 (Powder Technol. 138, 63–67 · 적당한 점착이 혼합을 돕는다 — 이 논문과 반대) · Alexander 2006 (Powder Technol. 164, 13–21) · Shinbrot 1999 (Nature 397, 675–678) · Khakhar 1997 (Phys. Fluids 9, 31–43) = wishlist 에 이미 있음 · Rabinovich 2005 · Lambert 2008 (액교 힘 식 — 우리 SJKR 과 다른 법칙) · Figueroa · Vargas · McCarthy 2010 (Chem. Eng. Sci. 65, 1045–1054 · 50 % 최저 · 정본 figueroa2009 와 다른 논문) — 다섯 밖.

## 카드 문제
없음 — 가리킨 카드 없음 (1저자 업로드) · 정본에 이 논문을 인용한 카드도 없음 (papers/ grep 'Liu, P.Y' · 'ces.2012.06.015' 0) · 이 논문의 2 차 인용 ↔ 정본 카드 대조 = 같음: Chaudhuri 2006 (Bond 0.1 에서 조금 빨라짐 · 마개 흐름 · Bond 120 에서 회전 빠를수록 조금 증가 · p.100 · p.102) ↔ `chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed` 카드 · Nase 2001 (최소 간격 관행 · p.101) ↔ `nase2001_granular_bond_collision_number_wet_cohesion` 카드 (같은 관행 · 값은 다름) · Lacey 1954 (식 5) ↔ `lacey1954_particle_mixing_theory_index` 카드.

## 공백 검사 G1–G4 (★ 이 카드의 핵심 산출 · 카드 §0-2 와 같은 판정)
- **G1 — 점착 대비를 설계 변수로 혼합 결과 (덮임 ↔ 뭉침 · 섞임 ↔ 분리) 를 예측** → **없음** | 근거: *"The particles have identical properties other than colours."* (p.101) · 모세관력을 *"also applied to particle–wall interaction"* (표 1 · p.100) — 모든 쌍 · 벽이 같은 γ = 대비 0 · 결과 변수 = 혼합 속도 · 정도뿐 · 점착이 만드는 *"cluster together"* (p.102) 는 상 구분 없는 뭉침 | 좁힐 필요 없음 · 가져올 것 = 대비 0 · 균일 점착의 기준선 (모든 쌍을 같이 키우면 회전당 k −42 % · rpm 의존 사라짐) → B1-U → B2-U (균일 세기 축) 와 U ↔ C (대비 축) 의 몫을 나눠 적는다
- **G2 — 점착 입력을 따로 재고 (AFM · IGC · 접촉각 등) 혼합 결과를 미리 예측** → **없음** | 근거: γ 는 고른 값 · θ_c = 0 가정 · *"In the present study, the minimum separation distance was treated as a fitting parameter."* (p.101) · S_min 5 µm · 다리 액량 몫 5 % = Liu 2011 실험 흐름에 맞춤 (p.100–101) · 혼합 결과의 사전 예측 없음 · 순환 주기 모형의 입력 (ε 6d · 8d · f_d) 은 같은 시뮬레이션에서 잼 (*"determined from the simulations"* p.105) | 좁힐 필요 없음 · 주의점 = 점착 모델의 맞춤 매개변수가 '따로 잰 입력' 과 섞이면 G2 의 '미리 예측' 이 무너진다 → 우리 SJKR CED 를 맞춤 없이 W (AFM) 에서 내는지 등록에 적는다
- **G3 — 회전 속도 최적을 입자 수준 맞교환 (덩어리 풀림 ↔ 벽 부착 손실 등) 으로 설명** → **일부** | 근거: 회전 의존의 입자 수준 기전을 '제안' — 마름 *"the bed turn-over time does not proportionally decrease with increasing rotation speed"* · 젖음 *"suggesting that the cohesion reduces the slipping of particles against the drum so the bed turn-over time also decreases with increasing drum speed"* (p.102) — 미끄럼 · 회전 시간 자료 없음 · 최적 rpm 없음 (3 점 · 단조) · 덩어리 풀림 · 벽 부착 손실의 맞교환 없음 (벽 점착은 미끄럼을 줄여 돕는 쪽으로만) | 우리 문장을 좁힌다: "회전당 혼합 속도의 rpm 의존을 벽 미끄럼 · 바닥 회전 시간으로 읽는 제안 (Liu 2013) 은 있으나 자료 · 최적 · 맞교환은 없다 — 우리는 rpm 최적을 덩어리 크기 · 벽 접촉 몫 · 미끄럼 속도 (덤프 관측량) 로 입자 수준에서 보인다"
- **G4 — 공정 × 재료 상태도 (회전 세기 × 점착 · Bond 수 등) 가 다른 재료로 옮겨 감** → **일부** | 근거: 공정 × 점착 지도 = rpm 3 × γ 3 (40 % · 그림 6) · 충전 7 × γ 3 (15 rpm · 그림 8 · 11) — 축 = 차원값 (rpm · N/m · Bond 는 '0–약 7' 범위만 · 정의 미인쇄) · 한 재료 (1.3 mm · 액량 0.5 %) · *"It is also unclear if the current results can be extended to other systems."* (p.104) · 모형은 *"a general method to predict the mixing performance at different operational conditions"* (p.106) 로 제안되나 입력이 같은 시뮬레이션 측정 | 우리 문장을 좁힌다: "공정 (rpm) × 균일 점착 세기 지도 (차원 축 · 한 재료) 는 선례 (Liu 2013) 가 있다 — 우리 몫은 축을 무차원 (Bo · Co · Fr) 으로 · 점착 대비를 셋째 축으로 · 다른 재료 · 크기 (실입경 ↔ parcel) 로 옮겨 가는지를 보이는 것"

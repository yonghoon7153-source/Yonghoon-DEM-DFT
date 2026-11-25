# batch 120 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 표 N-69)

대상: `stershic2015_fabric_tensor_calendering_nmc_xct_dem` — A.J. Stershic · S. Simunovic · J. Nanda, "Modeling the evolution of lithium-ion particle contact distributions using a fabric tensor approach", *Journal of Power Sources* **297** (2015) 540–550 · DOI 10.1016/j.jpowsour.2015.07.088 · 11 쪽 · SI 안내 없음 (부록 A · B 는 본문 안)
Ebner 2013 의 공개 싱크로트론 X 선 CT (복셀 370 nm · 단면 ≈330 µm) 에서 NMC111 액체 LIB 양극 네 조성의 압연 전 (0 bar) · 뒤 (≈2000 bar = 200 MPa 명목) 접촉 벡터를 다섯 판정 (구 · 타원체 중심 벡터 / 접촉 법선 · 복셀 중심 벡터 / 접촉면 법선) 으로 뽑아 fabric tensor (N · F · D · 0 · 2 · 4 차 · Kanatani χ² 99 %) 와 Δf 장미도로 견주고, 같은 입도 분포의 LIGGGHTS 헤르츠 구 DEM (μ 0.15 / 0 · 중력 침강 + 판 압축) 과 대조한 논문.
쪽 = 학술지 쪽 p.540–550 (PDF 쪽 = 학술지 쪽 − 539) · 판독 원자료 = `litdb/figures/stershic2015_fabric_tensor_calendering_nmc_xct_dem/digitized.csv` (24 행 · Fig 5 왼 · Fig 7 X-Z · Fig 8) · 고른 의도 = '조건 R7 — zhang2026 저자 결론 "큰 입자일수록 접촉점이 많고 힘이 커서 파쇄에 더 취약하다 — X-CT 에서도 관측 (ref 30)" 의 근거' (zhang2026_xct L38 · L222) → **일부** (X-CT 큰 입자 파쇄 = 정성 · Fig 8 한 장 · 원 관측 Ebner 2013 · '큰 입자 = 접촉 많음' = 서술 (교과서 [36]) · '힘이 크다' · 크기별 접촉 수 · 파쇄 통계 = 없음)

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — SE 없음 (액체 LIB 양극 · NMC 상만).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 탈압 계산 · 측정 없음.  반면교사 하나:
- [b] stershic2015_fabric_tensor_calendering_nmc_xct_dem | CT 는 압연 **뒤** (하중 뺀 뒤 · 에폭시 함침 55 °C 24 h) · DEM 은 *"When each of the pressure levels is attained … the list of contact vectors is assembled"* (누른 채) — 두 상태를 같은 '2000 bar' 칸에서 견줌: NMC 부피 분율 CT 0.50–0.55 ↔ DEM 0.69–0.71 (표 3) · 원문은 상태 차를 어긋남 후보로 들지 않는다 | 카드 §0 ⑧ · §3-5 · §4-1 · p.541 · p.544 · 표 3 | [인쇄] · [카드 관찰] | 되돌아옴 양 없음 · 우리 언로딩 키트로 누른 채 ↔ 뺀 뒤 Δf 를 따로 재야 가를 수 있다

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 항복 · 경도 · 크리프 없음 (탄성 헤르츠만).
- [c] stershic2015_… | DEM NMC E **113 GPa** · ν 0.25 · ρ 4750 kg/m³ · 강 200 GPa · 0.3 · Al 69 GPa · 0.32 (표 2 · 출처 인용 없음) · NMC–NMC 헤르츠 E* = E/(2(1 − ν²)) = 60.3 GPa | 카드 §3-1 · p.545 표 2 | [인쇄] · [카드 산술] | 다른 카드의 NMC E 142–144 GPa 와 다름 · 일축 항복 환산 없음

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 한 상 (NMC) · DEM 에 CBD 상 없음 · 힘 · 하중 몫 없음.  접촉 수만:
- [d] stershic2015_… | 배위수 z = n_c/n_p (표 4): CT 0 bar 0.32–1.61 → 2000 bar 0.94–1.53 (96 % 복셀만 1.605 → 1.530 감소 = *"an indication of particle splitting"*) · DEM (f) 1.91–2.39 → 5.40–6.39 · (f′) 1.33–2.15 → 5.41–6.38 · CT 가 *"6–8"* 보다 작은 것은 워터셰드 빈 띠 · 쌍당 접촉 하나 탓 (저자) | 카드 §3-4 · p.545–546 · 표 4 | [인쇄] | z 정의 (쌍 세기) [미확인] · 상별 · 크기별 없음

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] stershic2015_… | 헤르츠 + 마찰 · *"This choice is not expected to have a significant impact on the NMC particle packing, as other models have shown to yield similar results for granular packing simulations [11]"* (p.544) · 대안 (권고만) = 다구 입자 (*"already implemented in LIGGGHTS"*) · 부착 / 반데르발스 · 파쇄 — 맞춘 값 **0 개** (표 2 값 출처 없음 · 마찰 0.15 / 0 두 팔) · 마찰로는 방향 진화가 안 바뀐다 (p.546) | 카드 §3-1 · §3-7 · §4-2 · p.544–546 | [인쇄] | 큰 변형 · 소성 접촉 법칙 논의 없음

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 — MPM 없음.  격자 쪽 이웃 하나:
- [f] stershic2015_… | 복셀 접촉 방향은 *"only possible in 26 discrete directions"* (3 × 3 × 3 · L∞ 한 복셀) · *"depends heavily on the resolution of the tomography"* · 완화 = 중심 벡터 · 접촉면 이웃 벡터 평균 (p.542 · p.549) | 카드 §3-2 · §8 U0–U6 | [인쇄] | 해상도 수렴 시험 없음 · 우리 STEP3 · MPM 상 격자에서 접촉 · 계면 방향을 셀 때 같은 양자화

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] stershic2015_… | FT 정규화는 *"Γ is a unit circle in 2-D or unit sphere 3-D"* (p.542) 로 둘 다 정의하지만 계수 (15/2 · 315/8 · 식 3–4) 와 결과는 **3D 만** · 2D ↔ 3D 전이 진술 없음 | 카드 §3-3 ⚠ · §4-3 (iii) | [인쇄] · [미확인] 2D 계수 | 우리 2D (단계 3) 에 쓰려면 원전 Kanatani 1984 [18]

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 — 넘김 없음.  구상 둘:
- [h] stershic2015_… | *"these models must be upscaled to the continuum scale in order to be of a practical use, and methods of scaling are yet to be developed for electrode structures"* (p.541) · 결론 *"Analysis of the evolution of the fabric tensors can be used to build corresponding damage tensors to represent the particle assembly in continuum mechanical models [25,47]"* (p.549) | 카드 §3-7 · §8 후보 M0 | [인쇄] | 구상만 · 식 · 결과 없음

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — SE 없음.  액체 LIB 양극의 NMC 부피 분율만:
- [i] stershic2015_… | 표 3 CT (압연 뒤) 0.38 · 0.39 · 0.44 · 0.49 → 0.50 · 0.52 · 0.54 · 0.55 · DEM (누른 채 · *"overlapping volumes subtracted so that the volume is counted only once"*) 0.44 · 0.51 · 0.51 · 0.60 → 0.69 · 0.69 · 0.70 · 0.71 (90 · 92 · 94 · 96 wt% · 0 → 2000 bar) · 같은 ETHZ 자료의 `ebner2013_…` 식 1 φ_NMC (0.409–0.521 → 0.586–0.625) 보다 CT 값이 0.03–0.09 낮다 | 카드 §3-5 · p.544–545 · 표 3 | [인쇄] · [카드 산술 · 두 카드] | 랩 표준과 다른 문헌 값 (재료 · 상태 · 연산자 다름) · CT 계산법 [미확인]

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압과 닿는 것)
- [j] stershic2015_… | CT (뺀 뒤) ↔ DEM (누른 채) 상태 섞임 · '2000 bar' = 롤 명목 ↔ 판 압력 · z 정의 [미확인] · 결과는 0 · 2000 bar 만 (300 · 600 bar 목록은 만들었다면서 결과 없음 p.544) · DEM 입자 수 · 시간 간격 · 판 속도 · 감쇠 · 시드 [미확인] · 장미도 정규화 · 칸별 축척 미인쇄 · Φ_RCP 인쇄 값 = 상수 0.634 로 재현 (식 0.637 ↔ 값) · Parteli 0.38 ↔ r̄ 6 µm 면 0.455 · '0.06–0.11' ↔ 92 % 0.12 | 카드 §11 · [미확인] 목록 | [카드 산술] · [미확인] | 이 논문 DEM 으로 탈압 · 상태 차를 가를 수 없다

## k — DEM 의 한계 (서지: A.J. Stershic, S. Simunovic, J. Nanda, J. Power Sources 297 (2015) 540–550)
- [k] stershic2015_… (Stershic · Simunovic · Nanda 2015, J. Power Sources 297) | *"These results do not follow the experimental trends, which indicates that the particle size distribution alone is not a sufficient measure for the electrode microstructures in DEM simulations."* | p.540 초록 · 카드 §3-7 | [인쇄] | 액체 LIB NMC · 헤르츠 구 (연화 없음)
- [k] stershic2015_… (같은 서지) | *"The FT is a critical metric for accurate models of anisotropic phenomena, such as electronic transport through the active particle matrix of an electrode; by failing to capture or reproduce the mechanical directionality, namely the evolution of inter-particle contacts with increasing pressure, using a DEM model of this type has limited utility."* | p.546 · 카드 §3-7 | [인쇄] | 스칼라 z 증가는 맞춘다 (*"The higher z in the DEM simulation itself is not worrisome"*) — 방향만 틀린다
- [k] stershic2015_… (같은 서지) | *"Potential flaws in the DEM simulation could be the initial placement of the particles, since the exact particle positions could not be replicated, or that the compression of spherical particles does not correctly capture the trends in the contact distribution."* · *"does not include interaction forces from adhesion or van der Waals effects"* · *"the influence of the friction parameter μNMC is insufficient to significantly change the character of the evolution"* | p.546 · 카드 §3-7 | [인쇄] | 원인 미확정 (후보 목록)
- [k] stershic2015_… (같은 서지) | *"the common discrete element method model for this problem falls short … More accurate methods for particle shape representation and the models for interaction between the particles may be warranted."* · 연속체 상향 *"yet to be developed for electrode structures"* (p.541) | p.548 · p.541 · 카드 §3-7 | [인쇄] | —
- [k] stershic2015_… (같은 서지) | 겹침의 부피 효과: *"the existence of overlapping particles can increase the packing fraction beyond the predictions which assume that particles cannot overlap"* — DEM 2000 bar Φ 0.69–0.71 > Φ_RCP 0.684–0.686 (0.004–0.026 [카드 산술]) | p.545 · 카드 §3-5 | [인쇄] · [카드 산술] | 겹친 부피는 한 번만 셌다 (합집합)

## l — 소성변형이 왜 어려운가 · 택한 우회와 값
- [l] stershic2015_… (Stershic · Simunovic · Nanda 2015, J. Power Sources 297) | **소성 논의 없음** — NMC 를 탄성 헤르츠 구 (E 113 GPa) 로만 · 큰 변형의 대체 기전으로 **파쇄** 를 들고 그 어려움을 정리: *"A drawback to these solutions is a trade-off between conserving mass and having spatially disparate fragments [26,36]. If the particle to be split is replaced with a series of particles that are spatially disparate … then the mass of the particle is not conserved … if the particles are split into fragments which conserve mass but overlap … then artificial interaction forces, essentially a false 'fissile' energy, are induced [36]."* | p.548 · 카드 §3-8 · §4-3 (ii) | [인쇄] | 파쇄는 계산하지 않음 (권고)
- [l] stershic2015_… (같은 서지) | 우회 = 형상 (다구 입자 · *"can be implemented with minimal additional coding and is already implemented in LIGGGHTS"*) · 맞춘 값 0 개 · 검증 = CT 와 Φ · z · Δf 대조 · 계산 비용 · 입자 수 [미확인] · 타원체 근사 동기 *"the particles deform in response to applied loads and the matrix around them"* (p.549 · 변형량 없음) | p.546 · p.549 · 카드 §4-2 · §4-3 | [인쇄] · [미확인] | —

## m — 받아들일 통찰
- [m] stershic2015_… | **접촉 방향 분포 (fabric tensor) 를 우리 접촉망 지표로**: 접촉 단위 벡터 → N⁽²⁾ · N⁽⁴⁾ (식 2) → F · D (식 3–4) → Kanatani χ² (99 %) 로 유의 차수 → Δf 장미도 · 우리 DEM 접촉 덤프 (pair/gran/local) 에서 상 쌍별 · 압력 단계별 · 누른 채 ↔ 뺀 뒤로 계산 | 단계 7; 흐름 밖: 접촉망 방향 지표 (배위수가 같아도 방향이 다른 침대를 가름 · 원문 'FT … electronic transport') | 근거 식 2–4 · 부록 B · Fig 4 · 6 · p.546
- [m] stershic2015_… | **판정법 안에서만 견준다** — 같은 90 % · 0 bar 자료에서 복셀 (Fig 3 · 수직 적음) ↔ 타원체 중심 벡터 (Fig 4 왼 · 수직 많음) 의 '절대' 방향 분포가 반대 · 진화 Δf 만 다섯 판정이 일치 → 우리 DEM ↔ CT · SEM 대조는 같은 판정법의 상태 차끼리 | 단계 7; 결과 전 대조 항목 | 근거 Fig 3 · 4 · 6 (카드 §3-6 ⚠ [판독 · 카드 관찰])
- [m] stershic2015_… | **압력 + 상태 + 연산자 + 배위수 정의를 한 줄에 등록** — 이 논문은 CT (롤 · 뺀 뒤) 와 DEM (판 · 누른 채 · 합집합) 을 같은 '2000 bar' 칸에 넣었고 z = n_c/n_p 의 쌍 세기를 적지 않아 german2014 (N_C = 2 + 11f²) 와도 두 상태가 함께 안 맞는다 | 단계 0 | 근거 표 3 · 표 4 · p.542 · p.544 (카드 §3-4 · §3-5)
- [m] stershic2015_… | **R7 인용 사슬을 끝까지** — '큰 입자 = 접촉 많음 = 잘 깨짐' 은 zhang2026 → 이 논문 (서술) → 교과서 [36] · X-CT 관측 원전 = Ebner 2013 (정성) → 우리 파괴 판정 근거로는 크기 정규화 실측 (wheatcroft2023 · zhang2026 카드 §12 D7b) 을 쓴다 | 조건 R7 | 근거 p.548 (카드 §0-1 · §3-8)

## n — 논문 에이전트 후보
- [n] K.-I. Kanatani, Distribution of directional data and fabric tensors, Int. J. Eng. Sci. 22 (2) (1984) 149–164. | m · g · 단계 3 · 7 — fabric tensor 식 (3) · (4) · χ² 균일성 검정의 원전 · 2D (단위원) 계수 (이 논문은 3D 계수만 · 카드 §3-3 ⚠) | papers/ ls (kanatani* 없음) · grep 'Distribution of directional data' · 'Kanatani' = du2025 · sangros2019 의 인용뿐 → 카드 없음
- [n] T. Pöschel, T. Schwager, Computational Granular Dynamics: models and Algorithms, Springer Science & Business Media, 2005. (교과서) | k · l · 조건 R7 — '큰 입자 = 접촉 많음 = 같은 하중에서 잘 깨짐' · 파편 질량 보존 ↔ 거짓 에너지 맞바꿈의 출처 (zhang2026 → 이 논문 → [36] 사슬 끝 · 카드 §0-1 · §3-8) | papers/ ls · grep 'Computational Granular Dynamics' · 'Pöschel' → 카드 없음
- [n] G. R. McDowell, J. P. de Bono, On the micro mechanics of one-dimensional normal compression, Geotechnique 63. (서지 일부만 — 쪽 · 연도 없음) | e · l · 조건 R7 — 깨지는 입자 DEM 의 일축 압축 (겹친 파편 = 질량 보존 쪽) · 카드 §3-8 | papers/ ls (mcdowell* 없음) · grep 'one-dimensional normal compression' 0 건 → 카드 없음 (같은 저자 다른 논문 de Bono & McDowell 2016 은 wishlist 에 있음)
- [n] S. Lobo-Guerrero, L.E. Vallejo, Crushing a weak granular material: experimental numerical analyses, Geotechnique 55 (4) (2005) 245–249. | l · 조건 R7 — 입자 쪼개기 DEM (떨어진 파편 = 질량 비보존 쪽) · 카드 §3-8 | papers/ ls (lobo* 없음) · grep = song2025 의 인용뿐 · wishlist 에 '참고 · 후보로 세지 않음' 한 줄 → 카드 없음
- [n] L. Yi, K. Dong, R. Zou, A. Yu, Coordination number of the packing of ternary mixtures of spheres: DEM simulations versus measurements, Ind. Eng. Chem. Res. 50 (14) (2011) 8773–8785. | d · m · 단계 7 — 세 크기 구 혼합의 배위수 DEM ↔ 측정 (우리 12:4:1 접촉망 · 부분 배위수의 측정 대조) · 이 논문 경계 조건 · 배위수 문헌 [50] | papers/ ls · grep 'ternary mixtures of spheres' 0 건 → 카드 없음
- (세지 않음) [12] Ebner 2014 Tortuosity anisotropy · [31] Parteli 2014 = wishlist 에 이미 있음.

## 카드 문제
1. **`zhang2026_xct_dem_cathode_calendering_peel_calibration` L222 (와 L38)** — 카드는 Zhang 원문 (PDF p.12) 을 충실히 옮겼다.  그러나 Zhang 원문이 ref 30 (= 이 논문) 에 실은 내용 가운데 **'larger particles … sustain substantially higher contact forces'** 와 **'smaller particles tend to alleviate stress concentration through local rearrangement or sliding'** 은 이 원문에 없고, **'greater number of contact points'** 는 이 원문에서도 측정이 아닌 서술 (*"which tend to have more particle contacts"* · 교과서 [36]) 이다 → **Zhang 원문의 인용 문제** (그 카드는 고치지 않음 · '관련 카드' 한 줄만 더함).  L38 의 *"Stershic 2015 (ref 30) … 이번에 읽지 않았다"* 는 이 카드로 해소.
2. **`ge2022_xct_initial_structure_dem_calendering_nmc333` L95 · L393** — Ge 2022 표 1 의 μ_p,s **0.25** 출처 [16,20] 가운데 [20] = 이 논문 · 카드 L393 '직물 텐서 선행 · μ 0.25 의 다른 출처' ↔ 이 원문 표 2 마찰 = **0.15** (NMC–NMC · NMC–강 · NMC–Al · f′ 는 0) — 0.25 는 이 원문에 없다 (Ge 원문의 인용 문제 · 카드는 원문대로).
3. **`du2025_dem_fem_force_chain_collector_damage_calendering` L144 · L147 · L148** — Du 2025 표 1 의 E 출처 [72] = 이 논문 · AM **142 GPa** · Al 68.9 GPa · 강 **182 GPa** ↔ 이 원문 표 2: NMC **113** · Al 69 · 강 **200 GPa** — 142 · 182 는 이 원문에 없다 (Du 원문의 인용 문제 · 카드는 원문대로).
4. **`ngandjong2021_dem_calendering_digital_twin` L61** — *"ref [42]=Stershic(fabric tensor + DEM, CBD 없는 토모그래피 출발)"* 은 모호하다: 이 원문의 DEM 은 토모그래피 **입도 분포** 로 무작위 침강 구조를 새로 만든다 (*"the exact particle positions could not be replicated"* p.546) · 토모그래피에서 출발한 것은 fabric 분석뿐.
5. 이 카드 (stershic2015) 자체 — 없음 (원문 쪽 결함은 카드 §11 에 15 항목).

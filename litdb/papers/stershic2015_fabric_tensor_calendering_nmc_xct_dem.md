<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     형식 본 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md · 같은 계보 (같은 Ebner 2013 공개 CT 자료) = ebner2013_srxtm_nmc_cathode_microstructure_open_dataset_segmentation.md (자료 원전) ·
     ge2022_xct_initial_structure_dem_calendering_nmc333.md · zhang2026_xct_dem_cathode_calendering_peel_calibration.md (이 논문 = 그쪽 ref 30) · 배위수 ↔ 상대밀도 대조 = german2014_coordination_number_powder_densification.md.
     쪽 표기 = 학술지 쪽 p.540–550 (PDF 쪽 = 학술지 쪽 − 539) · 크롭 파일 이름 · figures.json 의 page 는 PDF 쪽.  보충 자료 (SI) 안내 없음 (본문 11 쪽 텍스트 층에
     'Supplementary' · 'Supporting' · 'Appendix' 가운데 'Appendix' 만 = 본문 끝 부록 A · B).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv · 원 래스터 (300 dpi) 의 눈금 · 축척 막대로
     선형 · 로그 보정 · 방법은 행마다) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 관찰] · [카드 추론] = 이 카드의 해석 ·
     [미확인] = 원문 (본문 11 쪽 전수) 에 없음.  11 쪽 텍스트 층 전부와 식 · 표 · 그림을 렌더로 직접 읽었다 (그림은 박힌 원 래스터 · 식 · 표는 벡터 400 dpi). -->
# 압연한 NMC111 양극 X 선 CT (Ebner 2013 공개 자료) 의 활물질 접촉 방향 분포를 fabric tensor (N · F · D · 2 · 4 차) 로 — 압연하면 접촉이 수직에서 수평으로 옮겨 간다 (다섯 판정법 모두) · 같은 입도 분포의 구 DEM (LIGGGHTS · 헤르츠 + 마찰 0.15 / 0) 은 그 변화를 못 낸다 · 배위수 z 0.32–1.61 (CT) ↔ 1.33–6.39 (DEM) · 큰 입자 파쇄는 서술 · 그림 한 장뿐 — Stershic · Simunovic · Nanda (J. Power Sources 2015)

> slug `stershic2015_fabric_tensor_calendering_nmc_xct_dem` · DOI `10.1016/j.jpowsour.2015.07.088` · type `image-data analysis + DEM (fabric tensor of the NMC111 AM contact network in calendered liquid-LIB cathodes from the open SRXTM data of Ebner 2013 · contact detection by sphere / ellipsoid overlap and voxel adjacency · LIGGGHTS Hertz spheres with the tomography PSD · gravity settling + plate compression 0–2000 bar · no SE · no binder phase in DEM · no particle plasticity or fracture · no unloading)` · PDF `16526032-69._Modeling_the_evolution_of_lithium-ion_particle_contact_distributions_using_a_fabric_tensor_approach.pdf` · digested `2026-11-16` · status ✅
>
> **저자**: **A.J. Stershic\*** (교신 · andrew.stershic@duke.edu · Department of Civil and Environmental Engineering, Duke University, Durham, NC) · **S. Simunovic** · **J. Nanda** (Oak Ridge National Laboratory, TN) · *J. Power Sources* **297** (2015) 540–550 (11 쪽 · SI 안내 없음) · 접수 2015-04-07 · 수정 07-24 · 승인 07-28 · 온라인 08-25 · 연구비 = Stershic 의 DOE Computational Science Graduate Fellowship (DE-FG02-97ER25308) · Nanda = DOE EERE Vehicle Technologies Program · ORNL 계약 DE-AC05-00OR22725 (p.549) · 핵심어 Fabric tensor · Lithium-ion battery · NMC · DEM (p.540).
> **이웃 카드 (링크만)**: [`ebner2013_srxtm_nmc_cathode_microstructure_open_dataset_segmentation`](ebner2013_srxtm_nmc_cathode_microstructure_open_dataset_segmentation.md) (이 논문 [13] = 쓴 CT 자료의 원전 · 2000 bar 큰 입자 파쇄의 원 관측) · [`zhang2026_xct_dem_cathode_calendering_peel_calibration`](zhang2026_xct_dem_cathode_calendering_peel_calibration.md) (그 논문 ref 30 = 이 논문 · 고른 의도의 출처) · [`ge2022_xct_initial_structure_dem_calendering_nmc333`](ge2022_xct_initial_structure_dem_calendering_nmc333.md) (그 논문 [20] = 이 논문) · [`song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage`](song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage.md) (그 논문 [18]) · [`du2025_dem_fem_force_chain_collector_damage_calendering`](du2025_dem_fem_force_chain_collector_damage_calendering.md) (그 논문 [72]) · [`ngandjong2021_dem_calendering_digital_twin`](ngandjong2021_dem_calendering_digital_twin.md) (그 논문 [42]) · [`german2014_coordination_number_powder_densification`](german2014_coordination_number_powder_densification.md) (배위수 ↔ 상대밀도 식).
> **판독 원자료**: `litdb/figures/stershic2015_fabric_tensor_calendering_nmc_xct_dem/digitized.csv` (24 행 — Fig 5 왼 (입도 분포) · Fig 7 (DEM 진화 장미도 X-Z 꽃잎 끝) · Fig 8 (축척 막대 · 금 간 입자 크기)) · 그림 크롭 68 장 (그림 8 + 그래픽 초록 1 + 패널 24 · 표 4 · 식 11 · 근거 문단 20) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: ETH Zurich 가 공개한 싱크로트론 X 선 CT (Ebner 2013 · 복셀 370 nm · 단면 ≈330 × 330 µm) 의 **압연 전 (0 bar) · 압연 뒤 (2000 bar = 200 MPa 명목)** NMC111 양극 네 조성 (NMC : 카본블랙 : PVDF = 90:5:5 – 96:2:2) 에서, 분할된 입자 사이의 **접촉 벡터** 를 다섯 가지로 뽑아 (구 겹침 · 타원체 겹침 (중심 잇는 벡터 / 접촉 법선) · 복셀 이웃 (중심 잇는 벡터 / 접촉면 평균 법선)) **fabric tensor (방향 분포의 다항 근사)** 를 만들고 0 → 2000 bar 차이 Δf 를 장미도로 그리면 **다섯 판정법 모두 접촉이 수직에서 줄고 수평에서 는다** — 같은 입도 분포로 중력 침강 + 판 압축을 한 **구 DEM (LIGGGHTS · 헤르츠 + 마찰)** 은 그 변화를 크기 · 모양 모두 재현하지 못하므로, 저자는 *"the particle size distribution alone is not a sufficient measure for the electrode microstructures in DEM simulations"* (p.540) 라 결론하고 입자 모양 · 상호작용 · **파쇄** 를 넣으라고 권한다.  **입자 크기 ↔ 접촉 수 ↔ 파쇄** 는 이 논문에서 **측정되지 않았다** — 교과서 [36] 를 인용한 서술 한 문장과 CT 단면 그림 한 장 (Fig 8) 뿐.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① fabric tensor 정의 (방향 분포를 어떻게 숫자로) | 접촉 단위 벡터 n 의 모멘트 N⁽⁰⁾ · N⁽²⁾ᵢⱼ = (1/N)Σnᵢnⱼ · N⁽⁴⁾ (식 2) → 제2 종 F (최소제곱 · 식 3) · 제3 종 (편차) D (식 4) · f(n) ≈ (1/4π)(D⁽⁰⁾ + D⁽²⁾ᵢⱼnᵢnⱼ + D⁽⁴⁾ᵢⱼₖₗnᵢnⱼnₖnₗ + …) (식 1) · 차수 유의성 = Kanatani χ² (부록 B · 99 %) · 비교량 Δf⁽ᵃ'ᵇ⁾ = f(F⁽ᵇ⁾₂₀₀₀) − f(F⁽ᵃ⁾₀) | [인쇄] p.542–543 · p.546 · p.550 |
| ② 접촉 판정 (영상에서 무엇을 접촉으로 셌나) | (a) 구 근사 (입자 중심 · 부피 보존 구가 **겹치면** 접촉) (b · c) 타원체 근사 (powercrust 표면 → 최소제곱 타원체 · Perram–Wertheim 접촉 함수 μ ≤ 1) (d · e) 복셀 (워터셰드 표지가 다른 이웃 복셀 = 접촉 · 13 이웃) · **쌍마다 접촉 하나** · 워터셰드가 입자 사이에 빈 띠를 넣어 접촉을 덜 센다 | [인쇄] p.542 · p.549 · p.546 |
| ③ 배위수 (압력별) | 표 4 — CT 0 bar 0.32–1.61 → 2000 bar 0.94–1.53 · DEM 1.33–2.39 → 5.40–6.39 · 정의 **z = n_c/n_p** (흔한 '이웃 수' 와 2 배 차 가능 — 원문은 쌍을 몇 번 셌는지 적지 않음 [미확인]) | [인쇄] p.542 · p.546 표 4 |
| ④ 이방성 (압연 → 방향) | CT 다섯 판정법: 수직 −, 수평 + (Fig 4 · 6 a–e) · DEM: 90–94 % 는 **수직 · 수평 +, 대각선 −** (작음) · 96 % 만 CT 와 같은 방향인데 크기가 아주 작다 · 마찰 0 (f′) 도 같음 | [인쇄] p.546 · Fig 6 · 7 · [판독] Fig 7 (꽃잎 끝 0.25 → 0.045 축 단위) |
| ⑤ 부피 분율 (NMC) | 표 3 — CT 0.38–0.49 (0 bar) → 0.50–0.55 (2000 bar) · DEM 0.44–0.60 → 0.69–0.71 (겹친 부피 한 번만 셈 · Φ_RCP 0.684–0.686 을 넘음) | [인쇄] p.545 표 3 |
| ⑥ DEM 한계 (원문 문장) | *"using a DEM model of this type has limited utility"* (p.546) · *"the common discrete element method model for this problem falls short"* (p.548) · 초기 배치 · 구 압축 · 부착 · 반데르발스 · 다구 입자 · **파쇄** (§3-7) | [인쇄] p.540 · p.546 · p.548 |
| ⑦ 입자 파쇄 (조건 R7) | *"mean fragment size decreases and sphericity … decreases as pressure increases"* (숫자 없음) · *"Larger particles, which tend to have more particle contacts, may be more likely to fracture … [36]"* · *"The tendency of larger particles to be more likely to fracture is evident in the NMC tomography"* · Fig 8 (92 % · 2000 bar 단면) · 크기별 접촉 수 · 파쇄 통계 **없음** | [인쇄] p.546–548 · [판독] Fig 8 금 간 입자 단면 ≈14–33 µm |
| ⑧ 압력을 뺄 때 | **다루지 않음** — CT 는 압연 **뒤** (하중 뺀 뒤 · 에폭시 함침) · DEM 은 판 압력 **도달 순간** (누른 채) 의 접촉 목록 — 원문은 이 상태 차이를 언급하지 않는다 [카드 관찰] | [인쇄] p.541 · p.544 |
| ⑨ 차원 · 계산 비용 | 측정 · DEM 모두 **3D** · DEM 영역 340 × 340 × 220 µm (Fig 5 캡션) · 입자 수 · 시간 간격 · 판 속도 · 감쇠 · 계산 시간 [미확인] | [인쇄] p.545 · [미확인] |

⛔ **한정어 (떼지 말 것)**: ① 재료 = **NMC111 (3M) + Super C65 + PVDF (Kynar 761) 액체 LIB 양극** — 고체전해질 없음 ② 압력 = **롤 압연 명목 ≈300 · 600 · 2000 bar (30 · 60 · 200 MPa)** · 결과 비교는 **0 ↔ 2000 bar 두 상태뿐** (300 · 600 bar 는 결과 없음) ③ CT = **압연 뒤 (뺀 뒤)** · DEM = **누른 채** — 같은 압력 이름이 다른 상태다 ④ DEM 에 카본 · 바인더 상 없음 (마찰 0 팔 f′ 가 '윤활' 대리) ⑤ 배위수 정의 z = n_c/n_p — 쌍을 몇 번 셌는지 [미확인] · CT 배위수는 워터셰드 탓에 작게 나온다 (저자) ⑥ 장미도의 크기는 축 단위로만 (정규화 미인쇄) · Fig 6 의 칸마다 축척 [미확인] ⑦ '큰 입자 파쇄' = 서술 (교과서 [36]) + 그림 한 장 · 크기 의존 통계 없음.
⇒ **절대값 전이**: 우리 재료 (NCM + LPSCl · SE 가 소성으로 흐름) 로 옮길 값은 **없다**.  옮길 것은 **방법** — 접촉 방향 분포를 fabric tensor (식 2–4) + χ² 차수 선택 + Δf 장미도로 재는 법 · 접촉 판정법마다 배위수 · 0 bar 방향 분포 '절대값' 이 갈리고 (§3-6 ⚠) **같은 판정법의 상태 간 차 (Δf) 만 견고하다** 는 함정 · DEM 을 CT 와 견줄 때 '누른 채 ↔ 뺀 뒤' 와 배위수 정의를 먼저 맞춰야 한다는 점.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-69 의 '왜' 칸)

의도 원문: *"조건 R7 — 저자 결론 '큰 입자일수록 접촉점이 많고 힘이 커서 파쇄에 더 취약하다 — X-CT 에서도 관측 (ref 30)' 의 근거"* (근거 칸 = b13 · `zhang2026_xct_dem_cathode_calendering_peel_calibration` L38 · L222).

인용한 쪽 원문 (zhang2026 PDF p.12 · 그 카드 §3.8 의 Fig 9 문단 · 직접 대조): *"Under high calendering pressures, stress concentration at particle contacts is significantly intensified, particularly for larger particles. For a given external load, larger particles typically exhibit a greater number of contact points and sustain substantially higher contact forces than smaller particles. The resulting interfacial stresses may induce surface defects and crack initiation, making larger particles more susceptible to fracture. In contrast, smaller particles tend to alleviate stress concentration through local rearrangement or sliding. This phenomenon was observed in X-CT, further confirming that larger particles exhibit a higher tendency to fracture during the calendering process.³⁰"* — ref 30 = *"A.J. Stershic, S. Simunovic, and J. Nanda, J. Power. Sources 297, 540 (2015)"* (zhang2026 참고문헌 목록 · 그 논문 전체에서 ref 30 은 이 한 곳에만 쓰임).

이 논문의 대응 문장 (p.546 오른쪽 끝 → p.548 왼쪽 · 크롭 `txt_p7_p9_fracture_larger_particles_more_contacts.png`): *"A critical model improvement would be to account for the effect of particle fracture. In the ETHZ data-sets, it is observed that the mean fragment size decreases and sphericity (a measure of how round the particle is) decreases as pressure increases — indications that particle fracture is prevalent; this can be confirmed by visual examination of the tomography [13] (see Fig. 8). Experimental studies have found that crushing a material requires more energy as the particle size decreases [4] and have confirmed that larger particles are more likely to break than smaller particles under the same load [36]. Larger particles, which tend to have more particle contacts, may be more likely to fracture because a larger portion of the particle will be in the vicinity of a contact point, and therefore have a critical stress that might cause cracks to initiate from surface flaws [36]. The tendency of larger particles to be more likely to fracture is evident in the NMC tomography."*

| 의도 · 인용 문장의 조각 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "큰 입자일수록 **접촉점이 많고**" (zhang: *"greater number of contact points"*) | **일부** | p.548 *"Larger particles, which tend to have more particle contacts"* — **서술 (경향) · 측정 없음** · 문장 끝 인용 [36] = T. Pöschel, T. Schwager, *Computational Granular Dynamics* (Springer 2005, 교과서).  이 논문의 배위수는 **조성 · 압력 · 판정법별 평균 z** (표 4) 뿐 — 입자 크기별 접촉 수 · 크기–배위수 상관 **없음** |
| "**힘이 커서**" (zhang: *"sustain substantially higher contact forces than smaller particles"*) | **없음** | 이 논문은 접촉력을 재지도 · 보고하지도 않는다 (CT 는 힘이 없고 · DEM 의 힘 · 응력 출력 없음).  파쇄 기전도 '힘' 이 아니라 *"a larger portion of the particle will be in the vicinity of a contact point … cracks to initiate from surface flaws"* (결함 · 면적 논리) — 힘 크기 진술은 zhang2026 자신의 DEM (그 논문 Fig 9) 에서 나온 것 |
| "파쇄에 더 취약하다" (zhang: *"making larger particles more susceptible to fracture"*) | **채움 (서술)** | p.548 *"have confirmed that larger particles are more likely to break than smaller particles under the same load [36]"* · *"may be more likely to fracture"* — 근거 = 교과서 [36] (*"Experimental studies"* 라 쓰고 붙인 출처는 [4] 시추 교과서 · [36] 계산 입상 역학 교과서) |
| "작은 입자는 재배열 · 미끄럼으로 응력 집중을 푼다" (zhang 원문 · 카드 L222 에는 없음) | **없음** | 이 논문에 없다 |
| "**X-CT 에서도 관측**" (zhang: *"This phenomenon was observed in X-CT"*) | **채움 (정성 · 그림 한 장)** | p.548 *"The tendency of larger particles to be more likely to fracture is evident in the NMC tomography"* · *"mean fragment size decreases and sphericity … decreases as pressure increases"* (**숫자 없음**) · *"for each electrode composition, the tomography shows an increasing number of particles with increasing pressure"* (p.546 · 숫자 없음) · Fig 8 = **92 % wt · 2000 bar** 단면 한 장 (저자가 고른 두 확대) — 금 간 입자 단면 ≈14–24 µm (아래 확대) · ≈30–33 µm (위 확대) [판독 · 축척 막대 50 · 10 µm] ↔ 입도 분포 봉우리 ≈8–10 µm [판독 Fig 5] · 조건 = 압연 **뒤** · 에폭시 함침 · 상온.  관측의 원전 = [13] Ebner 2013 (정본 `ebner2013_…` §0 ⑦: *"increased numbers of fractured large particles"* · 수 · 분율 [미확인]) |
| (의도 전체) 조건 R7 의 근거 | **일부** | 'X-CT 에서 큰 입자 파쇄가 보인다' (정성) 와 '큰 입자는 접촉이 많은 경향' (서술) 은 있다 · **'힘이 크다' · 크기별 접촉 수 · 파쇄 확률 · 통계 · 압력 의존 숫자는 없다** |
| 가리킨 카드 L222 의 2 차 인용 *"큰 입자일수록 접촉점이 많고 힘이 커서 파쇄에 더 취약하다 — X-CT 에서도 관측(ref 30)"* | **카드 = zhang2026 원문 그대로 · 원문 쪽의 인용 과대** | 카드는 zhang2026 문장을 충실히 옮겼다.  다만 zhang2026 이 ref 30 에 실은 내용 가운데 **'접촉력이 훨씬 크다' · '작은 입자는 재배열 · 미끄럼으로 푼다'** 는 이 논문에 없고, **'접촉점이 많다'** 는 이 논문에서도 측정이 아닌 서술이다 (**Zhang 원문의 인용 문제** — 카드 문제 절에 적음 · 그 카드는 고치지 않음) |
| 가리킨 카드 L38 *"Stershic 2015 (ref 30) 원문은 … 이번에 읽지 않았다"* | **해소 (이 카드)** | 서지 = zhang2026 [30] *"J. Power. Sources 297, 540 (2015)"* = 이 PDF 첫 쪽 (권 · 첫 쪽 · 연도 같음) |
| (덧붙임) 다른 카드의 2 차 인용 — `ge2022_…` L242 *"By purely considering the electrode structure and AM particle size distribution, the DEM simulations could not predict the evolution of inter-particle contacts"* ([20] = 이 논문) | **채움** | 초록 p.540 · 결론 p.548 과 같은 뜻 (Ge 2022 원문의 요약) |
| (덧붙임) `ge2022_…` L95 · L393 — Ge 2022 표 1 **μ_p,s 0.25** 의 출처 칸 [16,20] · 카드 'μ 0.25 의 다른 출처' | **원문과 다름** | 이 논문 표 2: NMC–NMC · NMC–강 · NMC–Al 마찰 **0.15** (f′ 는 0) — **0.25 는 이 논문에 없다** (Ge 2022 원문의 인용 문제 · 카드는 원문대로 옮김) |
| (덧붙임) `du2025_…` L144 · L147 · L148 — Du 2025 표 1 의 E 출처 [72] = 이 논문: AM **142 GPa** · Al 68.9 · 강 182 GPa | **일부 (Al 만)** | 이 논문 표 2: NMC **113 GPa** · Al **69 GPa** · 강 **200 GPa** — 142 · 182 는 이 논문에 없다 (Al 69 ≈ 68.9 만 반올림 수준 같음) · AM 밀도 4750 kg/m³ 는 Du 2025 가 [75] 에 붙였지만 이 논문 표 2 에도 같은 값 (Du 2025 원문의 인용 문제 · 카드는 원문대로) |
| (덧붙임) `ngandjong2021_…` L61 *"ref [42]=Stershic(fabric tensor + DEM, CBD 없는 토모그래피 출발)"* | **모호** | 이 논문의 DEM 은 토모그래피 **입도 분포** 로 무작위 침강 구조를 새로 만든다 — 입자 위치는 옮기지 않았다 (*"the exact particle positions could not be replicated"* p.546) · 토모그래피에서 출발한 것은 fabric 분석뿐 |

⇒ **의도 대조 결과: 일부** — X-CT 에서 큰 입자 파쇄가 보인다 (정성 · Fig 8 · 원 관측 Ebner 2013) · 큰 입자가 접촉이 많은 경향 (서술 · 교과서 [36]) 은 있다; **접촉력이 크다는 진술 · 크기별 접촉 수 · 파쇄 통계는 없다.**

---

## 1. 한 줄 요약
입자 크기 분포와 기공률만으로는 압연이 전극 안 접촉망을 어떻게 바꾸는지 못 잡는다는 동기 (p.541) 에서, 입상 역학 · 손상 역학의 **fabric tensor** (접촉 방향 분포의 텐서 근사) 를 Ebner 2013 의 공개 CT (NMC111 네 조성 × 0 · 2000 bar) 에 적용해 **압연하면 접촉이 수직에서 수평으로 옮겨 간다** 는 것을 다섯 접촉 판정법이 한목소리로 보이고 (*"very likely, this is the true effect imparted on the cathode assembly by calendaring"* p.546), 같은 입도 분포의 **구 DEM** (LIGGGHTS · 헤르츠 · 마찰 0.15 / 0) 은 배위수 증가 경향은 따라가도 **방향 변화의 모양 · 크기를 못 낸다** — 그래서 입자 모양 (다구 입자) · 상호작용 (부착 · 반데르발스) · **파쇄** 를 DEM 에 넣어야 한다고 권한다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| A.J. Stershic\* (Duke) · S. Simunovic · J. Nanda (ORNL) | J. Power Sources 297 (2015) 540–550 · 11 쪽 | 10.1016/j.jpowsour.2015.07.088 | **SE 없음** — NMC111 (3M · 구형) + Super C65 (TIMCAL) + PVDF Kynar 761 (Arkema) · 액체 LIB 양극 · 조성 90:5:5 · 92:4:4 · 94:3:3 · 96:2:2 wt% (표 1) | **공개 CT 자료 분석** (자기 측정 없음 · ETHZ 분할 결과 사용) + **DEM** (LIGGGHTS · 구 · 헤르츠 + 마찰) — 압밀 역학의 실험 측정 · FEM · MPM 없음 |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 자료 · 재료 · DEM 상수 (p.541–545 · 표 1–2)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| CT 자료 | Ebner 외 [13] 싱크로트론 X 선 단층 현미경 (SRXTM) · ETHZ 가 워터셰드 분할 (Saadatfar [40] 방식) · ETH 도서관 공개 [21] (원 영상 · 충전 시계열 · 입자 표) | [인쇄] p.541 |
| CT 압력 | *"earlier calendared at pressures of approximately 300, 600, and 2000 bar (30, 60, and 200 MPa, respectively) as well as uncalendared samples (0 bar, 0 MPa)"* — 이 논문 결과는 **0 · 2000 bar 만** | [인쇄] p.541 |
| CT 시료 준비 | 지름 15 mm 원통 틀 · 에폭시 함침 · **55 °C 24 h 진공** · 선반으로 지름 0.7 mm 원기둥 | [인쇄] p.541 |
| CT 단면 · 복셀 | 단면 ≈ **330 × 330 µm** · 복셀 **370 nm** 정육면체 (= 한 변 ≈ 892 복셀 [카드 산술]) | [인쇄] p.541 |
| 재료 | NMC (3M) · Super C65 (TIMCAL) · Kynar 761 PVDF (Arkema) · *"selected due to the high sphericity of the particles"* (Chung [6]) | [인쇄] p.541 |
| 입도 | *"distributed log-normally in size with a mean radius of r̄ = 6 µm and a polydispersity of δ = 0.6r̄"* (p.542) ↔ *"average radius 6 µm and a polydispersity of 0.4"* (p.545 · Chung [6]) — **두 표기가 다르다** (§11) · Fig 5 왼: 질량 밀도 q₃ 봉우리 ≈ 0.080–0.081 µm⁻¹ @ 지름 ≈ 8.4–9.7 µm · 범위 ≈ 0.7–46 µm [판독] | [인쇄] p.542 · p.545 · [판독] Fig 5 |
| 조성 (표 1) | NMC : 카본블랙 : PVDF = **90:5:5 · 92:4:4 · 94:3:3 · 96:2:2** (wt%) | [인쇄] p.542 표 1 |
| DEM 코드 · 접촉 | **LIGGGHTS** (DCS Computing · LAMMPS 기반) [19,35] · *"The Hertzian contact model with friction"* · 반데르발스 · 모세관 · 정전기 힘 무시 | [인쇄] p.544 |
| DEM 재료 (표 2) | NMC: ρ **4750 kg/m³** · E **113 GPa** · ν **0.25** · μ (NMC 와) **0.15** · 강 (위판 = 롤): 7750 · 200 GPa · 0.3 · 0.15 · 알루미늄 (아래 = 집전체): 2700 · 69 GPa · 0.32 · 0.15 · 셋 다 헤르츠 — **E 113 GPa 의 출처 인용 없음** | [인쇄] p.545 표 2 · [미확인] 출처 |
| DEM 헤르츠 유효 탄성률 (NMC–NMC) | E* = E/(2(1 − ν²)) = 113/(2 × 0.9375) = **60.3 GPa** | [카드 산술] |
| DEM 경계 | 아래 알루미늄 · 위 강 · 옆 주기 경계 ([50] 따라) | [인쇄] p.544 |
| DEM 영역 | **340 × 340 × 220 µm** (Fig 5 오른 · 96 % · 300 bar 그림 캡션) | [인쇄] p.545 |
| DEM 마찰 팔 | (f) μ_NMC **0.15** · (f′) μ_NMC **0** (*"extremely well-lubricated assembly … potentially-lubricative effect of the carbon black and PVDF binder"*) | [인쇄] p.546 |
| DEM 입자 수 · 시간 간격 · 판 속도 · 감쇠 (반발 계수) · 구름 마찰 · 계산 시간 · 시드 수 | **원문에 없음** | [미확인] |

### 3-2. ★ 접촉 판정 — 영상에서 접촉을 어떻게 셌나 (p.542 · 부록 A p.549 · 표 4 키)
| 키 | 방법 | 접촉 기준 | 접촉 벡터 | 원문이 적은 약점 |
|---|---|---|---|---|
| (a) | **구 근사** | 입자 표의 중심 · 부피로 만든 구가 **겹치면** 접촉 (*"overlap of the spheres is a proxy for contact as those particles in deformed adjacency due to contact in reality would likely show as overlapping"*) · 중심 거리 < 반지름 합 | 중심 잇는 벡터 | 이심률 · 방향 정보를 버림 |
| (b) | **타원체 근사 · 중심 벡터** | 입자 복셀 → powercrust 삼각 표면 [1,2] → 표면 단순화 [16] → **최소제곱 타원체** [34] (부피가 크게 다르면 구로 대체) · Perram–Wertheim 접촉 함수 [33] (Donev [10] 판): 크기 배율 μ 로 키우거나 줄여 접하게 함 — **μ ≤ 1 이면 접촉** | 중심 잇는 벡터 (branch vector) | 이심률이 크면 접촉 법선과 어긋남 |
| (c) | **타원체 근사 · 접촉 법선** | (b) 와 같은 접촉 쌍 | 접촉 함수가 준 접촉면 법선 | 접촉 알고리즘 정확도에 전부 기댐 |
| (d) | **복셀 · 중심 벡터** | 표지 영상에서 복셀마다 26 이웃 가운데 **13 개** (중복 피함) 를 보고 **표지가 다르고 배경이 아니면 접촉** | 두 입자 중심 잇는 벡터 | *"contact is only possible in 26 discrete directions"* (p.542) |
| (e) | **복셀 · 접촉면 법선** | (d) 와 같은 접촉 쌍 | 그 쌍의 모든 이웃 복셀 벡터의 **평균** | 같음 · 해상도에 크게 기댐 |
| (f) · (f′) | **DEM** | LIGGGHTS 접촉 목록 (각 압력 도달 때) | [미확인] (DEM 의 접촉 벡터가 중심 벡터인지 법선인지 원문에 없음 — 구 사이는 둘이 같다 (부록 A.2 *"This approximation works exactly for spherical particles"*)) | — |
- 공통: *"all of these approximations may understate the contact count by assuming at most one contact between each particle pair"* (p.546) · *"the watershedding process tends to shrink particles as it separates particles by adding a minimal zone of void material between identified particles. This may decrease the occurrence of adjacent voxels of different particles"* (p.549).
- 표 4 에서 (b) · (c) 는 같은 z · (d) · (e) 도 같은 z — 접촉 쌍은 같고 **방향 벡터만 다르다** [인쇄 표 4 키].
- 계산 도구: MMTensor [27] (MATLAB) (p.542).

### 3-3. ★ fabric tensor 정의 식 (식 1–4 · 본문 식 · 부록 B — 크롭 `eq_*`)
| 식 | 내용 (인쇄 그대로) | 쪽 · 크롭 |
|---|---|---|
| 배위수 | **z = n_c/n_p** (n_c = 접촉 수 · n_p = 입자 수) — *"contains no directional information"* | p.542 · `eq_in_p3_coordination_number_z.png` |
| 제3 종 ← 제2 종 | **D⁽ᵏ⁾ = F⁽ᵏ⁾ − δ⁽²⁾F⁽ᵏ⁻²⁾** [37] · 대칭 f(n) = f(−n) · 정규화 ∮_Γ f(n) dΓ = 1 (Γ = 2D 단위원 · 3D 단위구) | p.542 · `eq_in_p3_third_kind_symmetry_normalisation.png` |
| (1) | f̂(n) ≈ f⁽ᵏ⁾(n) = (1/4π)(F⁽ᵏ⁾ᵢ₁…ᵢₖ nᵢ₁…nᵢₖ) = (1/4π)(D⁽⁰⁾ + D⁽²⁾ᵢⱼnᵢnⱼ + D⁽⁴⁾ᵢⱼₖₗnᵢnⱼnₖnₗ + … + D⁽ᵏ⁾ᵢ₁…ᵢₖ nᵢ₁…nᵢₖ) | p.542 · `eq_01_directional_distribution_expansion.png` |
| (2) | 제1 종 (모멘트): N⁽⁰⁾ = (1/N)Σ1 = 1 · **N⁽²⁾ᵢⱼ = (1/N)Σ_α nᵢ^α nⱼ^α** · N⁽⁴⁾ᵢⱼₖₗ = (1/N)Σ_α nᵢ^α nⱼ^α nₖ^α nₗ^α | p.543 · `eq_02_moment_tensors_first_kind_N.png` |
| (3) | 제2 종: F⁽⁰⁾ = 1 · **F⁽²⁾ᵢⱼ = (15/2)(N⁽²⁾ᵢⱼ − (1/5)δᵢⱼ)** · F⁽⁴⁾ᵢⱼₖₗ = (315/8)(N⁽⁴⁾ᵢⱼ[sic] − (2/3)δᵢⱼN⁽²⁾ₖₗ + (1/21)δᵢⱼδₖₗ) | p.543 · `eq_03_fabric_tensors_second_kind_F.png` |
| (4) | 제3 종 (편차): D⁽⁰⁾ = 1 · **D⁽²⁾ᵢⱼ = (15/2)(N⁽²⁾ᵢⱼ − (1/3)δᵢⱼ)** · D⁽⁴⁾ᵢⱼₖₗ = (315/8)(N⁽⁴⁾ᵢⱼ[sic] − (6/7)δᵢⱼN⁽²⁾ₖₗ + (3/35)δᵢⱼδₖₗ) | p.543 · `eq_04_deviatoric_tensors_third_kind_D.png` · 세 식 함께 `eq_02_04_tensor_set.png` |
| 비교량 | **Δf⁽ᵃ'ᵇ⁾ = f(F⁽ᵇ⁾₂₀₀₀) − f(F⁽ᵃ⁾₀)** (a · b = 0 · 2000 bar 텐서의 유의 차수) · f⁽⁰⁾ = ∮f dΓ/∮dΓ = 1/4π → Δf 의 '평균' 은 0 | p.543 · `eq_in_p4_density_difference_delta_f.png` |
| 유의성 (부록 B) | Kanatani '균일성 검정': 2 차 λ = (2N/15)D⁽²⁾ᵢⱼD⁽²⁾ₖₗ[sic] ↔ χ²_c(5, α) · 4 차 λ = (8N/315)(D⁽⁴⁾ᵢⱼₖₗD⁽⁴⁾ᵢⱼₖₗ − (8/11)D⁽⁴⁾ᵢⱼₖₗD⁽⁴⁾ᵢⱼₖₘD⁽²⁾ₗₘ) ↔ χ²_c(9, α) · 이 논문은 **99 %** 수준 · 4 차까지 유의한 가장 높은 차수를 씀 | p.550 · p.546 · `eq_in_p11_kanatani_significance_statistic.png` |
- [카드 산술] 인쇄된 계수의 자기 일관성: D⁽²⁾ = F⁽²⁾ − δF⁽⁰⁾ = (15/2)N⁽²⁾ − (3/2 + 1)δ = (15/2)(N⁽²⁾ − (1/3)δ) ✓ · D⁽⁴⁾ = F⁽⁴⁾ − δF⁽²⁾ 의 δN 계수 −(315/8)(2/3) − 15/2 = −33.75 = −(315/8)(6/7) ✓ · δδ 계수 (315/8)(1/21) + (15/2)(1/5) = 3.375 = (315/8)(3/35) ✓ · 등방 분포 (N⁽²⁾ = δ/3 · N⁽⁴⁾nnnn = 1/5) 에서 F⁽²⁾ᵢⱼnᵢnⱼ = 1 · F⁽⁴⁾nnnn = (315/8)(1/5 − 2/9 + 1/21) = 1.000 → f = 1/4π ✓ (Fig 3 오른쪽 F⁽²⁾ 표면 반지름 ≈ 1 [판독] 과 맞음).
- ⚠ 인쇄 표기 둘: 식 (3) · (4) 의 N⁽⁴⁾ 아래첨자가 'ij' 만 (식 (2) 정의는 ijkl) · 부록 B 2 차 λ 의 D⁽²⁾ᵢⱼD⁽²⁾ₖₗ (스칼라가 되려면 같은 첨자끼리) [카드 관찰].
- ⚠ 계수 15/2 · 315/8 은 **3D** (단위구) 값 — 2D (단위원) 계수는 이 논문에 없다 [미확인] → 우리 2D MPM (단계 3) 에 쓰려면 원전 [18] Kanatani 1984 를 봐야 한다.

### 3-4. ★ 배위수 z — 조성 · 압력 · 판정법별 (표 4 · p.545–546)
| 판정법 | 90 % z₀ → z₂₀₀₀ (비 · 차) | 92 % | 94 % | 96 % |
|---|---|---|---|---|
| (a) 구 | 0.510 → 0.937 (1.836 · 0.427) | 0.466 → 1.071 (2.298 · 0.605) | 0.662 → 1.062 (1.605 · 0.400) | 0.939 → 1.171 (1.246 · 0.231) |
| (b · c) 타원체 | 0.321 → 1.086 (3.378 · 0.764) | 0.331 → 1.065 (3.214 · 0.733) | 0.422 → 0.937 (2.219 · 0.515) | 0.656 → 1.172 (1.786 · 0.516) |
| (d · e) 복셀 | 1.294 → 1.443 (1.115 · 0.149) | 1.261 → 1.520 (1.205 · 0.259) | 1.452 → 1.516 (1.044 · 0.065) | 1.605 → 1.530 (**0.953 · −0.076**) |
| (f) DEM μ 0.15 | 1.962 → 5.404 (2.754 · 3.442) | 1.913 → 5.715 (2.987 · 3.801) | 2.355 → 6.191 (2.629 · 3.836) | 2.392 → 6.389 (2.671 · 3.997) |
| (f′) DEM μ 0 | 2.078 → 5.413 (2.605 · 3.335) | 1.333 → 5.553 (4.165 · 4.220) | 2.153 → 6.116 (2.840 · 3.963) | 2.140 → 6.375 (2.979 · 4.235) |
- 전부 [인쇄] 표 4 · 비 · 차 열을 [카드 산술] 로 다시 계산 — 24 행 모두 셋째 자리 반올림 안에서 같다.
- 원문 해석 (p.545–546): ① *"the coordination number at 2000 bar (z₂₀₀₀) is higher than that at 0 bar (z₀) indicating that there are more contacts per particle with increasing pressure"* ② 예외 = 96 % 복셀 (z 감소) — *"both the number of particles and contacts have still increased; the number of particles increased more than the number of contacts, an indication of particle splitting"* ③ CT 값이 *"significantly less than the coordination numbers of other random packings of spherical particles, which tend to average 6–8"* — *"approximation error in the tomographic analysis and weakness of the segmentation algorithm"* 탓 ④ DEM 이 더 높은 것은 *"not worrisome"* · *"the ratios of z₂₀₀₀/z₀ for the DEM simulations fall well within the range of the ratios for the tomography-based methods"* ⑤ DEM 은 입자 수가 일정 (CT 는 압력과 함께 입자 수 증가 = 파편) 이라 z₂₀₀₀ 이 높게 나오는 것이 *"to be expected"*.
- [카드 산술] 원문 문장 대조: *"average around 2 when unloaded"* — (f) 평균 z₀ 2.16 · (f′) 1.93 ✓ · *"exceed 6 after 2000 bar"* — (f) 5.40 · 5.72 · **6.19 · 6.39** (평균 5.92) · (f′) 5.41 · 5.55 · **6.12 · 6.38** (평균 5.86) → **6 을 넘는 것은 8 런 중 4** · *"ratios … fall well within the range"* — CT 비 범위 0.953–3.378 ↔ (f) 2.63–2.99 (안) · (f′) 2.61–**4.17** (92 % f′ 가 범위 밖).
- [카드 산술 · german2014 식 (9) N_C = 2 + 11f² 대입 · 그 식은 단분산 위주 · '이웃 수' 정의] DEM 의 Φ (표 3) 에서 기대 이웃 수: 0 bar Φ 0.44 · 0.51 · 0.51 · 0.60 → **4.1 · 4.9 · 4.9 · 6.0** · 2000 bar Φ 0.69 · 0.69 · 0.70 · 0.71 → **7.2 · 7.2 · 7.4 · 7.5** ↔ DEM z (f) 1.9–2.4 → 5.4–6.4 · 2z 면 3.8–4.8 → 10.8–12.8.  어느 정의로 읽어도 두 상태가 함께 맞지 않는다 → **z 의 정의 (쌍을 한 번 / 두 번) 가 이 논문에서 [미확인]** 인 것이 대조를 막는다 [카드 관찰].
- [카드 관찰] 92 % f′ 의 z₀ 1.333 은 나머지 DEM 일곱 런 (1.91–2.39) 보다 0.6 낮다 · 원문 설명 없음.

### 3-5. ★ NMC 부피 분율 Φ (표 3 · p.544–545) — 누른 채 (DEM) ↔ 뺀 뒤 (CT)
| 조성 | CT 0 bar | CT 2000 bar | DEM 0 bar | DEM 2000 bar | DEM − CT [카드 산술] |
|---|---|---|---|---|---|
| 90 % | 0.38 | 0.50 | 0.44 | 0.69 | +0.06 · +0.19 |
| 92 % | 0.39 | 0.52 | 0.51 | 0.69 | **+0.12** · +0.17 |
| 94 % | 0.44 | 0.54 | 0.51 | 0.70 | +0.07 · +0.16 |
| 96 % | 0.49 | 0.55 | 0.60 | 0.71 | +0.11 · +0.16 |
- [인쇄] 표 3 (열 머리 'Tomography % vol. NMC' · 'DEM % vol. NMC' 인데 값은 분율).  원문: *"The volume fraction of this particle packing at 0 bar is within 0.06–0.11 of the volume fraction estimates of the tomography"* (p.544) — 92 % 는 **0.12** [카드 산술].
- DEM 연산자: *"the volume fractions in Table 3 have been measured with the overlapping volumes subtracted so that the volume is counted only once"* (p.545) = 겹친 구의 **합집합** (우리 ε_union 쪽) · 2000 bar 에서 Φ_RCP 를 *"by a small margin"* 넘는 것은 겹침 탓 (*"the existence of overlapping particles can increase the packing fraction beyond the predictions which assume that particles cannot overlap"*) — 넘는 양 0.004–0.026 [카드 산술: 0.69–0.71 − 0.684–0.686].
- Φ_RCP (Desmond [9]): **Φ_RCP = 0.637 + 0.0658·δ + 0.0857·S·δ²** · Chung 입도 (δ 0.4 · S 1.264) → **0.678** · DEM 실제 δ {0.443 · 0.441 · 0.438 · 0.437} · S {1.371 · 1.353 · 1.315 · 1.316} → {0.686 · 0.686 · 0.684 · 0.684} [인쇄 p.545].  ⚠ [카드 산술] 인쇄 식에 인쇄 입력을 넣으면 0.681 · 0.689 · 0.689 · 0.687 · 0.687 = **인쇄 값보다 0.003 크다** · 상수를 **0.634** 로 두면 다섯 값이 모두 정확히 재현된다 (식 · 값 어긋남) · S 1.264 = 로그정규 왜도 3δ + δ³ (δ 0.4) ✓.
- Parteli [31] 침강 경험식: **Φ = 0.64 − 0.99/(2r̄)^0.676** → 원문 *"this yields an estimation of the pre-compacted volume fraction of Φ = 0.38, which well matches that observed"* (p.545).  ⚠ [카드 산술] r̄ = 6 µm (µm 단위 가정) 를 넣으면 **0.455** · 0.38 이 나오려면 r̄ ≈ 3.6 µm · '맞는다' 는 관측값 = DEM 0 bar 0.44–0.60 이면 맞지 않고 CT 0 bar 0.38–0.49 쪽에 가깝다 (어느 쪽을 가리켰는지 [미확인]).
- 원문 비유: *"The volume fraction observed before and after loading is similar to those of experimental random loose packing and random dense packing of steel spheres, as summarized by Brouwers et al. [5]"* (p.545).
- ⚠ **같은 자료 · 다른 연산자** [카드 산술 · 두 카드]: 정본 `ebner2013_…` §3 이 같은 ETHZ 자료의 기공률 (그림 3a 판독) 을 식 1 로 거꾸로 낸 φ_NMC = 0 bar **0.409 · 0.431 · 0.470 · 0.521** · 2000 bar **0.586 · 0.607 · 0.595 · 0.625** (90 · 92 · 94 · 96 %) ↔ 이 논문 표 3 CT 0.38 · 0.39 · 0.44 · 0.49 · 0.50 · 0.52 · 0.54 · 0.55 → 이 논문이 **0.03–0.04 (0 bar) · 0.05–0.09 (2000 bar) 낮다**.  이 논문의 '단층촬영 부피 분율' 계산법 (영역 · 분할 입자 부피인지 이진 영상인지) 은 원문에 없다 [미확인] · 워터셰드 수축은 원문이 말한 방향 (입자를 작게) 과 같다 [카드 추론].
- 압력 이름 ⚠: CT 의 '2000 bar' = 롤 압연 명목 (선압에서 환산 · `ebner2013_…` §0 ③) · 압연 **뒤** · DEM 의 '2000 bar' = 평판 일축 **도달 압력** · 누른 채 [카드 관찰].

### 3-6. ★ 이방성 — 압연에 따른 접촉 방향 변화 (Fig 3 · 4 · 6 · 7 · p.543 · p.546)
| 계열 (Fig 6 줄) | 90 % | 92 % | 94 % | 96 % | 방향 (원문 · 그림) |
|---|---|---|---|---|---|
| (a) 구 | Δf⁽⁴'⁴⁾ | Δf⁽⁴'⁴⁾ | Δf⁽⁴'⁴⁾ | Δf⁽⁴'⁴⁾ | 수직 − · 수평 + (96 % 는 아주 작음) |
| (b) 타원체 중심 벡터 | ⁽⁴'⁴⁾ | ⁽⁴'⁴⁾ | ⁽⁴'⁴⁾ | ⁽⁴'⁴⁾ | 수직 − · 수평 + |
| (c) 타원체 접촉 법선 | ⁽⁴'⁴⁾ | ⁽⁴'⁴⁾ | ⁽⁴'⁴⁾ | ⁽⁴'⁴⁾ | 수직 − (크게) · 수평 + |
| (d) 복셀 중심 벡터 | ⁽⁴'²⁾ | ⁽²'²⁾ | ⁽⁴'⁴⁾ | ⁽⁴'²⁾ | 수직 − · 수평 + |
| (e) 복셀 접촉 법선 | ⁽²'²⁾ | ⁽⁴'²⁾ | ⁽²'²⁾ | ⁽⁴'²⁾ | 수직 − · 수평 + |
| (f) DEM μ 0.15 | ⁽⁴'⁴⁾ | ⁽²'⁴⁾ | ⁽²'⁴⁾ | ⁽²'²⁾ | 90–94 %: **수직 + · 수평 + · 대각선 −** · 96 %: 수직 − · 수평 + (아주 작음) |
| (f′) DEM μ 0 | ⁽²'⁴⁾ | ⁽⁴'⁴⁾ | ⁽²'⁴⁾ | ⁽²'⁴⁾ | (f) 와 비슷 — *"a very small magnitude of directional density differences and inconsistent rose diagram shape"* |
- 위 첨자 = 그림 칸 안 인쇄 (a = 0 bar 텐서 차수 · b = 2000 bar 텐서 차수 · χ² 99 % 로 유의한 최고 차수) [인쇄 Fig 6 · 크롭 `fig_6a` … `fig_6f2`].
- 원문 (p.546): *"the overwhelming trend is that the spatial distribution of contacts decreases in the vertical direction and increases in the lateral direction as pressure increases. This agreement of these five models indicates that very likely, this is the true effect imparted on the cathode assembly by calendaring."* · 결론 (p.548): *"inter-particle contacts become increasingly lateral in proportion as the pressure increases on the matrix."*
- DEM 크기 (Fig 7 · X-Z 옆 보기 · 축 단위 그대로 [판독 · digitized.csv]): 90 % 수직 + 꽃잎 끝 ≈0.25 · 수평 + ≈0.22 · 대각선 − ≈0.2 · 92 % 수직 ≈0.17 · 수평 ≈0.13 · 94 % 수직 ≈0.11 · 수평 ≈0.14 · 96 % 수직 (−) ≈0.045 · 수평 (+) ≈0.03.  CT 쪽 크기는 3D 투시 그림 (Fig 4 · 6) 이라 축 단위로 읽을 수 없다 — 원문: *"The magnitude of the density differences is so small compared to those of the tomographic approximations that the color scale for these rose diagrams only varies from a yellow–green/chartreuse to a blue-green/viridian"* (p.546 · 색 = 공통 크기 척도).
- Fig 3 (90 % · 0 bar · 복셀): N⁽²⁾ *"ellipsoidal and nearly spherical … nearly uniform"* · N⁽⁴⁾ *"relatively more contacts in the diagonal directions and fewer in the vertical direction"* (p.543).
- ⚠ [판독 · 카드 관찰] **0 bar 방향 분포의 '절대값' 이 판정법에 갈린다**: 같은 90 % · 0 bar 자료에서 복셀 (Fig 3 가운데 N⁽⁴⁾) 은 **수직이 적고** (높이 ≈ ±0.15 · 폭 ≈ ±0.2 [판독]), 타원체 중심 벡터 (Fig 4 왼 F⁽⁴⁾₀) 는 **수직이 많다** (높이 ≈ ±1.5 · 폭 ≈ ±0.6 [판독]) — 원문은 이 차이를 다루지 않고 진화 Δf 의 일치만 근거로 삼는다 → 우리가 방향 분포를 쓸 때 **같은 판정법 안의 상태 차** 만 견준다.

### 3-7. ★ DEM ↔ 실험 어긋남 — 원문 문장 (질문 k)
| 위치 | 원문 (그대로) | 무엇을 말하나 |
|---|---|---|
| p.540 초록 | *"These results do not follow the experimental trends, which indicates that the particle size distribution alone is not a sufficient measure for the electrode microstructures in DEM simulations."* | 입도 분포만 맞춘 구 DEM 은 압연의 접촉 진화를 못 낸다 |
| p.540 하이라이트 | *"DEM models built from particle size distribution do not reflect experimental data."* | 같음 |
| p.541 | *"these models must be upscaled to the continuum scale in order to be of a practical use, and methods of scaling are yet to be developed for electrode structures."* | DEM → 연속체 이음 미개발 |
| p.546 (5.2) | *"the contact evolution observed in the DEM simulations (series (f) and (f′)) does not well represent the contact evolution observed in the imagery-based methods (series (a) through (e)). The FT is a critical metric for accurate models of anisotropic phenomena, such as electronic transport through the active particle matrix of an electrode; by failing to capture or reproduce the mechanical directionality, namely the evolution of inter-particle contacts with increasing pressure, using a DEM model of this type has limited utility."* | ★ 방향성 (이방성) 을 못 내면 전자 수송 모형으로 쓸모가 줄어든다 |
| p.546 | *"the influence of the friction parameter μ_NMC is insufficient to significantly change the character of the evolution of the DEM contact distribution results."* | 마찰 (0.15 ↔ 0) 로는 못 고친다 |
| p.546 (5.3) | *"Potential flaws in the DEM simulation could be the initial placement of the particles, since the exact particle positions could not be replicated, or that the compression of spherical particles does not correctly capture the trends in the contact distribution."* | 초기 배치 · 구 압축 자체 |
| p.546 | *"the DEM model employed, though commonly used, does not include interaction forces from adhesion or van der Waals effects which have proven critical to some packing problems [31]."* | 부착 · 반데르발스 없음 |
| p.546 | *"An improvement … would be to use the multi-sphere method … the shape of the particles is better represented, so the contacts of the particles might also be better represented … already implemented in LIGGGHTS [19]."* | 다구 입자 (형상) |
| p.546 | *"A critical model improvement would be to account for the effect of particle fracture."* | ★ 파쇄 |
| p.548 (6) | *"the common discrete element method model for this problem falls short. When evaluating the DEM results for directional quantities, such as the inter-particle contacts, the fabric tensor analysis reveals that the DEM model does not accurately reproduce the behavior observed in the tomography. More accurate methods for particle shape representation and the models for interaction between the particles may be warranted."* | 결론 |
| p.546 (5.1) | *"The higher z in the DEM simulation itself is not worrisome … confirming that the DEM model captures the trend of the coordination number evolving with pressure."* | 스칼라 (z 증가 경향) 는 맞춘다 — 방향만 틀린다 |

### 3-8. ★ 파쇄 — 크기 ↔ 접촉 수 ↔ 파쇄 (조건 R7 · p.546–548 · Fig 8)
- 원문 전문 = §0-1 인용 (p.546–548).  파쇄 근거의 층: ① 관측 (ETHZ 자료 · *"mean fragment size decreases and sphericity … decreases"* · 숫자 없음 · 원 관측 = [13] Ebner 2013) ② 일반론 (*"Experimental studies"* [4] 시추 교과서 · [36] 계산 입상 역학 교과서) ③ 기전 서술 (큰 입자 = 접촉 많음 → 접촉점 근처 몫 큼 → 표면 결함에서 균열) ④ 그림 Fig 8 (92 % · 2000 bar · 위에서 본 단면 · 입자마다 회색 · 두 확대).
- [판독 · digitized.csv · 축척 막대 = 원 래스터 흰 띠 길이] 위 보기 100 µm = 125 화소 (패널 폭 ≈ 336 µm = 단면 330 µm 와 맞음) · 아래 확대 50 µm = 302 화소 · 위 확대 10 µm = 48 화소 · **어두운 금이 보이는 입자** 단면 겉 크기: 아래 확대 ≈ 23.5 × 21.2 · 19.9 × 20.4 · 13.7 × 16.6 µm · 위 확대 ≈ 31.9 × 33.3 · 30.2 × 33.3 µm (±1.5–2 µm) ↔ Fig 5 입도 봉우리 ≈8–10 µm (`ebner2013_…` 카드 D50 ≈ 11.7 µm (부피 가중 · 지름)) → 그림에 고른 금 간 입자는 중앙값의 ≈1.2–3 배 [판독 · 카드 산술] — ⚠ 단면 한 장 · 저자가 고른 확대 · 2D 단면 지름 ≤ 참 지름 · **통계 아님**.
- 모형화 방법 (p.548 · 원문 비판 포함): *"a particle could be split into two or more pieces once a splitting stress criterion is met [24,26]"* · 파편 크기 분포 [36] · 다구 입자 묶음을 끊기 [15] · *"A drawback to these solutions is a trade-off between conserving mass and having spatially disparate fragments [26,36]. If the particle to be split is replaced with a series of particles that are spatially disparate, as proposed by Lobo-Guerrero et al. [24], then the mass of the particle is not conserved … In contrast, if the particles are split into fragments which conserve mass but overlap, as proposed by McDowell et al. [26], then artificial interaction forces, essentially a false 'fissile' energy, are induced [36]."*
- 이 논문은 파쇄를 **계산하지 않았다** (권고만).

---

## 4. ★ 방법 — 자료 사슬 · DEM · 비교

### 4-1. 자료 사슬 (재구성)
ETHZ CT (Ebner [13] · SRXTM · 370 nm) → ETHZ 워터셰드 분할 · 입자 표 (중심 · 부피) · 표지 영상 [21] → 다섯 접촉 판정 (§3-2) → 접촉 벡터 목록 (단위 벡터만 · *"we are interested in only the direction of the contact vectors"* p.542–543) → N · F · D (0 · 2 · 4 차 · 식 2–4 · MMTensor) → Kanatani χ² (99 %) 로 0 · 2000 bar 각각의 최고 유의 차수 → Δf⁽ᵃ'ᵇ⁾ 장미도 (Fig 6) · z (표 4).
- **압력을 뺄 때**: CT 시료는 압연 **뒤** 에폭시로 굳힌 것 — 되돌아옴 · 하중 아래 구조는 이 자료에 없다.  DEM 은 *"When each of the pressure levels is attained (0 bar, 300 bar, 600 bar, 2000 bar), the list of contact vectors is assembled"* (p.544) = **누른 채** · 판을 올리는 계산 없음.

### 4-2. DEM 사슬 (p.544–545)
ETHZ 입도 분포 (Fig 5 왼) → 무작위 다분산 구 생성 → **중력 침강** (*"packing the domain until the desired sample is created"* — 멈춤 기준 [미확인]) → 재료 값 부여 (표 2) → 아래로 움직이는 강 판 → 0 bar 값 = *"after the particles settle but before the plate contacts the assembly"* → 각 압력 도달 때 접촉 목록 → FT.
- 맞춘 값: **없음** (표 2 의 재료 값은 출처 없음 · 마찰 0.15 / 0 은 두 팔) · 검증 = CT 와 Φ (표 3) · z (표 4) · Δf (Fig 6) 대조.
- 초기 침강 Φ 를 Parteli 식 · Desmond Φ_RCP 와 견줌 (§3-5).
- 계산 비용 · 입자 수 · 시간 간격 · 판 속도 · 감쇠 [미확인].

### 4-3. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM 한계 진술** = §3-7 표 (원문 문장 열 개) — 핵심: 구 · 입도 분포만으로는 압연 접촉 진화를 못 낸다 · 마찰로 못 고친다 · 형상 (다구) · 상호작용 (부착 · 반데르발스) · **파쇄** 필요 · 연속체로 올리는 법 미개발.
- **(ii) 소성 · 큰 변형을 넣기 어려운 이유** = **소성 논의 없음** — NMC 를 **탄성 헤르츠 구** 로만 둔다 (E 113 GPa).  큰 변형의 대체 기전으로 **파쇄** 를 들고, 파쇄를 DEM 에 넣는 어려움 (질량 보존 ↔ 파편 겹침의 거짓 에너지 맞바꿈) 을 [24 · 26 · 36] 으로 정리한다 (§3-8).  타원체 근사의 동기 문장에 *"the particles deform in response to applied loads and the matrix around them"* (p.549) 이 있을 뿐 · 변형량 [미확인].
- **(iii) 차원**: CT · DEM 모두 **3D** · FT 계수는 3D (단위구) · *"Γ is a unit circle in 2-D or unit sphere 3-D"* (p.542) 라고만 · 2D 계수 · 2D ↔ 3D 전이 진술 없음.
- **(iv) 탈압**: 없음 (§4-1).

### 4-4. 기법 미니 용어집
- **fabric tensor (직물 텐서)** = 입자 집합의 방향 정보 (여기선 접촉 방향) 를 담은 텐서 — 접촉 단위 벡터의 외적 평균 (N) 과 그로부터 만든 다항 근사 계수 (F · D).
- **장미도 (rose diagram)** = 방향마다 분포 크기를 반지름으로 그린 극 그림 (3D 에서는 닫힌 곡면).
- **Δf (밀도 차)** = 두 상태의 방향 분포 근사의 차 · 평균 0 · 양 (노랑 → 빨강) = 그 방향 접촉이 는다 · 음 (초록 → 파랑) = 준다.
- **branch vector (중심 잇는 벡터)** ↔ **contact normal (접촉 법선)** — 구는 같고 타원체 · 불규칙 입자는 다르다 (Fig 1).
- **워터셰드 분할** = 거리 지도의 '골' 을 따라 붙은 입자를 나누는 영상 처리 — 나눈 자리에 빈 띠가 생겨 접촉이 줄어든다.
- **Kanatani 균일성 검정** = 높은 차수 텐서 성분이 표본 수에 따른 우연인지 χ² 로 가르는 검정 (λ 통계).
- **다분산 지수 δ** = 입도 분포의 변동계수 (표준편차 / 평균) (Desmond [9]).
- **Φ_RCP** = 무작위 조밀 충전 부피 분율 (단분산 ≈0.64 · FCC/HCP 0.74 — p.544).

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| GA | 그래픽 초록 — Li-NMC CT → 복셀 · 구 · 타원체 · (입도 분포 → DEM) → 진화 장미도 | 방법 흐름 한 장 |
| 1 | 두 타원체 접촉 · 중심 벡터 (파랑) ↔ 접촉 법선 (빨강) | 접촉 벡터 정의 그림 (단계 7) |
| 2 (a–d) | 92 % · 0 bar — CT 원 영상 (확대 상자) · 메쉬 입자 · 구 근사 · 타원체 근사 | 영상 → 입자 근사의 실물 비교 |
| 3 (a–c) | 90 % · 0 bar · 복셀: N⁽²⁾ (거의 구) · N⁽⁴⁾ (위 · 아래 오목) · F⁽²⁾ (파랑) ↔ F⁽⁴⁾ (빨강) | 2 차 ↔ 4 차 표현력 (원문: 2 차는 흔히 모자람 [37]) |
| 4 (a–c) | 90 % · 타원체 중심 벡터: F⁽⁴⁾₀ · F⁽⁴⁾₂₀₀₀ · Δf (수직 − · 수평 +) | ★ Δf 정의의 예시 그림 |
| 5 (a · b) | ETHZ 입도 분포 q₃ (지름 · 로그 축) · DEM 96 % 300 bar (340 × 340 × 220 µm) | 입도 · 영역 크기 [판독] |
| 6 (a–f′) | ★ 네 조성 × 일곱 계열 Δf 장미도 · 칸마다 유의 차수 | CT 다섯 계열 일치 ↔ DEM 두 계열 불일치 |
| 7 (a · b) | DEM (f) 확대 · X-Z (옆) · X-Y (위) · 칸마다 축척 다름 | DEM 진화의 크기 (축 단위 [판독]) |
| 8 (a–c) | 92 % · 2000 bar 단면 · 입자마다 회색 · 아래 · 위 확대 (금 간 입자) | R7 정성 증거 · 금 간 입자 단면 크기 [판독] |
| 표 1 | 조성 넷 | — |
| 표 2 | DEM 재료 값 (ρ · E · ν · μ · 헤르츠) | E 113 GPa (출처 없음) · μ 0.15 — 다른 카드 인용 대조 (§0-1) |
| 표 3 | NMC 부피 분율 CT ↔ DEM (0 · 2000 bar) | 연산자 · 상태 함정 (§3-5) |
| 표 4 | 배위수 z (일곱 계열 × 네 조성 × 0 · 2000 bar) | 배위수 정의 함정 (§3-4) |
| 식 크롭 11 장 | `eq_01` (식 1) · `eq_02` · `eq_03` · `eq_04` (식 2–4 따로) · `eq_02_04_tensor_set` (함께) · `eq_in_p3_*` (z · D⁽ᵏ⁾ 관계 · 정규화) · `eq_in_p4_*` (Δf) · `eq_in_p6_*` (Φ_RCP · Parteli) · `eq_in_p11_*` (Kanatani λ) | 보고서에 붙일 정의식 |
| 근거 문단 20 장 | `txt_p1_*` (초록) · `txt_p2_*` (DEM 상향 · CT 자료 · 재료 입도) · `txt_p3_*` (접촉 벡터 · 26 방향) · `txt_p5_*` (DEM 설정 · 경계 · 압력 단계) · `txt_p6_*` (Φ 겹침 · z 경향 · 쪼개짐 · 워터셰드) · `txt_p7_*` (χ² · 수평 경향 · DEM f/f′ · 쓸모 제한 · 비판) · `txt_p7_p9_*` (★ 큰 입자 파쇄) · `txt_p9_*` (파쇄 모형화 맞바꿈 · 결론) · `txt_p10_*` (부록 A.1–A.3) | 원문 인용용 |

## 6. Post-processing ★
- **무엇을**: 접촉 벡터 (다섯 판정 + DEM) → N · F · D (0 · 2 · 4 차) → χ² 차수 선택 → Δf 장미도 · z = n_c/n_p · Φ (CT · DEM) · Φ_RCP · Parteli 비교.
- **안 한 것**: 접촉 면적 · 접촉 크기 가중 (결론: *"account for the contact size between two particles, rather than simply its existence"* 는 후속 과제 p.548–549) · 크기별 배위수 · 상별 (AM–CBD) 접촉 · 300 · 600 bar 결과 · 기공 (*"further examination of the interstitial void space"* 는 후속 p.549) · 접촉력 · 응력 · 수송 계산 · DEM 반복 시드 · 오차 막대 · Δf 크기의 수치 지표 (장미도 그림뿐).
- **이 카드의 후처리**: 표 4 비 · 차 재계산 (24/24 일치) · 원문 문장 대조 (평균 z · '6 초과' · '비 범위') · Φ_RCP 재계산 (상수 0.634 로 재현) · Parteli 재계산 · german2014 식 (9) 대입 · ebner2013 카드 φ_NMC 와 표 3 대조 · Fig 5 입도 · Fig 7 꽃잎 끝 · Fig 8 축척 · 금 간 입자 판독 (digitized.csv 24 행).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 가지에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처를 병기)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 재료 | NMC111 + C65 + PVDF · 액체 LIB · SE 없음 | NCM811 + LPSCl (+ 첨가제) · 전고체 | 재료 · 계 다름 — SE 의 소성 흐름이 우리 접촉망을 정한다 |
| 압력 · 상태 | 롤 압연 0 · 2000 bar (200 MPa 명목) · CT = 뺀 뒤 · DEM = 누른 채 | 일축 300 MPa · DEM 가압 중 (판 고정 이완) · 언로딩 키트 진행 | 압력 ⅔ · 롤 ↔ 일축 · 상태 섞임 (이 논문) |
| DEM 접촉 | 헤르츠 + 마찰 (μ 0.15 / 0) · NMC E 113 GPa · 연화 없음 | LIGGGHTS hooke/hysteresis · SE E_eff 1.35 GPa (18 배 연화) · AM 140 GPa (CLAUDE.md) | 같은 코드 계열 · 접촉 법칙 · 연화 다름 |
| 출발 구조 | 입도 분포 → 중력 침강 (위치 복제 없음) | 입도 설계 → 침강 · 압밀 (real_14 등) | 같은 부류 (위치 복제 없음) |
| 배위수 | z = n_c/n_p · CT 0.3–1.6 · DEM 1.3–6.4 | SE–SE · AM–SE 배위수 열 (σ_ion 식의 CN² · 코퍼스 사례 CN 2.7 · 3.3 · 'CN ≥ 7 자료 공백' — CLAUDE.md σ_ionic 절) | 정의 (쌍 세기) 를 맞춰야 비교 가능 · 우리 값 정의는 웹앱 열 사전 기준 [이 카드는 확인 안 함] |
| 방향 분포 | ★ fabric tensor N · F · D + Δf | **없음** (접촉 덤프는 있음 — `pair/gran/local` · CLAUDE.md f_AM 측정 절) | 우리 쪽 미계산 = 흡수할 지표 (§7-3) |
| 부피 분율 연산자 | DEM = 겹친 부피 한 번 (합집합) | DEM 기본 ε_sphere (구 부피 합 · 재료 보존) · ε_union 은 상한 점검 | 다른 연산자 — 높은 압력에서 갈린다 |
| 파쇄 | 권고만 (계산 없음) | DEM Auerbach 파괴 판정 (CLAUDE.md frame[5]) | 우리가 앞선다 (단 크기 정규화 점검 = zhang2026 카드 §12 D7) |
| 탈압 | 없음 | DEM 언로딩 키트 (H0–H5 PASS · CLAUDE.md 10-14) | 우리 쪽에서 '누른 채 ↔ 뺀 뒤' 방향 분포를 둘 다 낼 수 있다 |

### 7-2. ★ 랩 기준과 나란히 (판정 없이)
| 출처 | 재료 | 압력 · 상태 | 분모 | 값 |
|---|---|---|---|---|
| **랩 표준** | LPSCl (순수 SE) | 300 MPa | 진밀도 **1.64 g/cm³** (고정) | 기공 **10–13 %** |
| 이 논문 CT (표 3) | NMC111 액체 LIB 양극 (NMC 상만) | 200 MPa 명목 롤 · 뺀 뒤 | 영상 부피 (계산법 [미확인]) | NMC 부피 분율 0.50–0.55 (CBD · 기공 합 0.45–0.50) |
| 이 논문 DEM (표 3) | NMC 구만 | 2000 bar 판 · 누른 채 | 합집합 부피 | 0.69–0.71 |
| 우리 DEM 순수 SE | LPSCl | 300 MPa · 가압 중 | 구 부피 합 | ε_union ≈ 10 % · 겹침 11–12 % (CLAUDE.md 2026-06-06) |
- **랩 표준과 다른 문헌 값** — 이 논문은 SE 가 없어 기공 비교의 자리가 아니다 · NMC 분율은 다른 재료 · 다른 상태 · 다른 연산자.

### 7-3. ★ 우리 DEM 접촉망의 배위수 · 방향 분포 (일축 압축 이방성) · 단계 7 ↔ 이 논문
- **우리가 이미 가진 것**: 접촉 쌍 덤프 (`pair/gran/local` — CLAUDE.md 'f_AM 측정' 절이 AM–AM 규약 측정에 쓴 것) · 상별 배위수 열.  **없는 것**: 접촉 방향 분포 (fabric).  ⇒ 식 (2) N⁽²⁾ = (1/N)Σnn 은 접촉 쌍의 중심 벡터 (구라서 = 접촉 법선) 만으로 바로 계산된다 — **상 쌍별 (SE–SE · AM–SE · AM–AM)** · **누른 채 ↔ 뺀 뒤 (언로딩 키트)** · 압력 단계별로.
- **결과 전 대조 항목 (등록 후보 · 판정 아님)**: (1) 이 논문 CT 다섯 계열의 방향 (압연 뒤 · 수직 − · 수평 +) ↔ 우리 DEM 뺀 뒤 AM–AM Δf 의 **부호** (2) 우리 DEM 누른 채 ↔ 뺀 뒤의 Δf — 이 논문이 섞은 두 상태의 차를 우리 계산 안에서 직접 잰다 (3) 배위수는 정의를 먼저 등록 (쌍 한 번 / 두 번 · german2014 의 '이웃 수' 와 같은 쪽으로).
- **한정어**: ① 재료 (NMC 액체 LIB ↔ NCM + 무른 LPSCl — 우리 SE 는 겹침으로 흐름을 대리) ② 롤 ↔ 일축 ③ 이 논문 DEM 의 결과 (수직 + · 수평 +) 는 **연화 없는 헤르츠 구 · CBD 없음** 의 결과라 우리 DEM 결과의 예측이 아니다 ④ 방향 분포 '절대값' 은 판정법에 갈린다 (§3-6 ⚠) — 우리 DEM 은 겹침 > 0 하나로 고정해 상태 간 차만 본다.
- **수송과의 연결**: 원문 *"The FT is a critical metric for accurate models of anisotropic phenomena, such as electronic transport through the active particle matrix"* (p.546) — 우리 Kirchhoff 망은 두께 (z) 방향 σ 만 푼다 → 접촉이 수평으로 옮겨 가면 같은 배위수에서도 z 방향 σ 가 낮을 수 있다 [카드 추론] · 방향별 tortuosity 의 원 연구 = [12] Ebner 2014 (wishlist 에 있음).

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 실측 3D 구조 위의 **접촉망 방향 지표** (DEM 쪽 관측량) · 구 DEM 이 그 지표를 못 낸다는 직접 증거.
- **없는 것**: 소성 · 형상 변화 (MPM 반쪽) · 수송 계산 · 탈압 · 힘.  ⇒ DEM 쪽에 '방향 지표 + 판정법 함정' 을, 형상 쪽에는 '구 · 탄성만으론 압연 접촉 진화가 안 나온다 → 형상 · 파쇄 필요' 라는 독립 근거 (frame[5] 의 분업을 지지하는 문헌 문장) 를 준다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ (1) 같은 ETHZ 자료의 NMC 분율이 연산자에 따라 0.03–0.09 갈린다 (이 논문 표 3 ↔ ebner2013 식 1 · §3-5) — 연산자 이름을 결과 전에 적는다 (2) DEM Φ = 겹친 부피 한 번 (합집합) — 우리 ε_sphere 와 다른 쪽임을 표에 적는다 (3) 같은 '2000 bar' 가 CT (롤 · 뺀 뒤) ↔ DEM (판 · 누른 채) 두 상태 — **상태 칸** 을 등록 항목에 둔다 (4) 배위수 정의 (쌍 세기) 를 등록 | 순수 SE · 진밀도 · 기공 곡선 없음 |
| **단계 1** (3D 메모리 · 장 수) | DEM 영역 340 × 340 × 220 µm · CT 단면 330 × 330 µm · 복셀 370 nm (한 변 ≈ 892) [카드 산술] — 크기 감각뿐 | 입자 수 · 메모리 · 시간 [미확인] |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | 접촉 방향 분포를 견줄 지표 후보 (입자별 속도장이면 입자 쌍 접촉이 정의됨) · ⚠ 2D 계수는 이 논문에 없음 (원전 [18] 필요) | 2D 식 · 2D 결과 없음 |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 없음 (SE 없음) | — |
| **단계 5** (3D 복합 압밀) | 구 DEM (입도만 맞춤) 이 압연 접촉 진화를 못 낸다는 실측 대조 — 출발 구조 · 형상 · 파쇄 · 부착이 결과를 가른다 (원문 후보 목록) | 우리 계 (SE 소성) 결과 예측 아님 |
| **단계 6** (탈압 · 되돌아옴) | 반면교사: CT (뺀 뒤) 와 DEM (누른 채) 을 같은 압력으로 견줌 — 탈압이 접촉 방향을 바꾸는지 이 논문으로는 가를 수 없다 → 우리 언로딩 키트로 누른 채 ↔ 뺀 뒤 Δf 를 재면 그 몫을 직접 볼 수 있다 | 되돌아옴 양 · 탈압 계산 없음 |
| **단계 7** (형상 · 피복 · 수송) | ★ fabric tensor (식 2–4) · χ² 차수 선택 · Δf 장미도 = 접촉망 **방향** 지표 · 접촉 판정법 다섯과 약점 (26 방향 양자화 · 워터셰드 수축 · 쌍당 접촉 하나) · *"FT is a critical metric … electronic transport"* · 결론의 후속 과제 = 접촉 **크기** 가중 (우리 Holm 면적 가중과 같은 방향) | 수송 계산 · 접촉 면적 없음 |
| **후보 D0** (지금 DEM) | 같은 부류 (구 · 접촉 법칙 · LIGGGHTS) 가 압연 접촉 방향 진화에서 실패한 기록 · 마찰로 못 고침 · 파쇄 · 형상 필요 | 우리 18 배 연화 · hooke/hysteresis 와 다른 법칙 (헤르츠 · 연화 없음) |
| **후보 A′-0 · A · A′** (MPM 접촉 · 강체 AM · 입자별 속도장) | 없음 | — |
| **후보 B** (입자별 FE) | 없음 | — |
| **후보 C · C′** (큰 변형 · 항복 캡 DEM) | 다구 입자 · 파쇄 (질량 보존 ↔ 파편 겹침 거짓 에너지 맞바꿈) 의 정리 | 소성 접촉 법칙 논의 없음 |
| **후보 M0** (균질화 압밀) | 결론의 제안 *"build corresponding damage tensors to represent the particle assembly in continuum mechanical models [25,47]"* — fabric → 손상 텐서 → 연속체 (구상만) | 식 · 결과 없음 |
| **U0–U6** | U1 · U6 (해상도): 복셀 접촉 방향은 26 방향으로 양자화 · 방향 정확도가 영상 해상도에 기댄다 (원문) — 우리 STEP3 · MPM 상 격자에서 접촉 · 계면 방향을 셀 때 같은 함정 | 수렴 시험 없음 |
| **R1–R7** | **R7** (AM 파괴): 정성 (CT · 큰 입자 · Fig 8) + 서술 ([36]) · 파쇄 모형화의 맞바꿈 · **R2** (미끄럼): 마찰 0.15 ↔ 0 이 방향 진화를 못 바꾼다 | R1 · R3 · R4 · R5 · R6 없음 · R7 의 통계 · 확률 없음 |
| **결과 전 대조 항목** | CT 다섯 계열 Δf 부호 (수직 − · 수평 + · 압연 뒤) · z 비 z₂₀₀₀/z₀ (CT 0.95–3.38 · 96 % 복셀만 감소 · DEM 2.61–4.17 [표 4]) — 재료 · 상태 · 정의 표지와 함께 | 크기 비교 금지 (축척 · 정규화 · 정의가 다름) |

- **재료 · 차원 · 조건 차이**: NMC111 액체 LIB ↔ 우리 NCM811 + LPSCl 전고체 · 롤 200 MPa 명목 ↔ 일축 300 MPa · CT 뺀 뒤 / DEM 누른 채 ↔ 우리 누른 채 (+ 언로딩) · 3D = 같음 · CBD 상 없음 (DEM) ↔ 우리 SE · 첨가제 상 있음.

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **접촉 방향 분포를 단계 7 지표로 더한다** — 우리 DEM 접촉 덤프에서 상 쌍별 N⁽²⁾ · N⁽⁴⁾ · D (식 2–4) 와 Kanatani χ² (부록 B) 로 유의 차수를 고르고 Δf 를 압력 단계 · 누른 채 / 뺀 뒤로 그린다 — 배위수 (스칼라) 가 같은데 방향이 다른 침대를 가를 수 있다 (원문 *"FT is a critical metric for … electronic transport"*).
2. **판정법 안에서만 견준다** — 같은 자료에서 복셀 · 타원체 판정의 0 bar 방향 분포가 반대였다 (§3-6 ⚠) · 우리 DEM ↔ CT · SEM 대조는 '같은 판정법으로 만든 상태 차' 끼리만.
3. **'2000 bar' 를 상태와 함께 적는다** — CT 는 뺀 뒤 · DEM 은 누른 채 · 이 논문은 둘을 같은 압력 칸에 넣었다 → 우리 표는 압력 + 상태 (누른 채 / 뺀 뒤) + 연산자 + 배위수 정의를 한 줄에.
4. **R7 근거를 인용할 때 사슬을 끝까지 탄다** — '큰 입자 = 접촉 많음 = 파쇄' 는 zhang2026 → 이 논문 (서술) → 교과서 [36] 의 2 차 · 3 차 인용이고, X-CT 관측의 원전은 Ebner 2013 (정성) 이다 → 우리 Auerbach 판정의 근거로는 Wheatcroft 2023 류 (크기 정규화 실측) 를 쓴다 (zhang2026 카드 §12 D7b).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Fabric-tensor analysis of synchrotron X-ray tomography of NMC111 cathodes (four compositions, uncalendered vs. ≈2000 bar) shows that inter-particle contacts become less vertical and more lateral after calendering, consistently across five contact-detection approximations; spherical-particle DEM with the same size distribution does not reproduce this evolution (Stershic, Simunovic & Nanda, J. Power Sources 297 (2015) 540–550)."
- "*'The FT is a critical metric for accurate models of anisotropic phenomena, such as electronic transport through the active particle matrix of an electrode; by failing to capture or reproduce the mechanical directionality … using a DEM model of this type has limited utility.'* (Stershic et al. 2015, p.546)"
- 국문: *"입도 분포만 맞춘 구 DEM (헤르츠 · 마찰 0.15 / 0) 은 압연 뒤 CT 의 접촉 방향 변화 (수직 → 수평) 를 크기 · 모양 모두 재현하지 못했다 (Stershic 2015)."*
- 국문 (R7 · 한정어 필수): *"큰 입자가 압연 중 더 잘 깨진다는 것은 X-CT 에서 정성적으로 관측되었다 (Ebner 2013 · Stershic 2015 Fig. 8) — 크기별 파쇄 통계는 보고되지 않았다."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **배위수 정의 z = n_c/n_p** — 쌍을 몇 번 세는지 없음 · '이웃 수' 정의 (2n_c/n_p) 와 2 배 차 가능 · DEM *"exceed 6"* 는 8 런 중 4 · *"ratios fall well within the range"* 는 92 % f′ (4.17) 에서 틀림 [카드 산술].
2. **상태 섞임** — CT = 압연 뒤 (하중 뺀 뒤 · 에폭시 · 55 °C 24 h) ↔ DEM = 압력 도달 순간 (누른 채) · 원문은 어긋남 후보로 들지 않는다.
3. **압력 정의 섞임** — CT 2000 bar = 롤 압연 명목 · DEM 2000 bar = 평판 압력.
4. **Φ_RCP 식 ↔ 값** — 인쇄 상수 0.637 로는 인쇄 값 다섯이 0.003 씩 크게 나오고 0.634 면 정확히 재현 [카드 산술].
5. **Parteli 추정 0.38** — r̄ 6 µm 로는 0.455 [카드 산술] · '맞는다' 는 관측값이 어느 것인지 불명.
6. **'0.06–0.11'** (DEM − CT, 0 bar) — 92 % 는 0.12 [카드 산술].
7. **입도 표기 둘** — p.542 *"δ = 0.6r̄"* ↔ p.545 *"polydispersity of 0.4"* (같은 Chung [6] 인용) · DEM 실제 δ 0.437–0.443.
8. **E_NMC 113 GPa** — 표 2 에 출처 없음 · 다른 카드의 NMC E 142–144 GPa 와 다름 · 후속 논문 (Du 2025) 이 이 논문에 142 GPa 를 귀속 (§0-1).
9. **장미도 크기** — Δf 의 정규화 (f ↔ 4πf) 미인쇄 · Fig 6 칸마다 축척 [미확인] · CT 쪽 크기는 3D 투시 그림이라 숫자로 읽을 수 없다.
10. **'Experimental studies have found …' [4,36]** — 붙인 출처 둘이 교과서 (시추 · 계산 입상 역학) · 1 차 실험 논문 아님.
11. **파쇄 관측** — *"mean fragment size decreases and sphericity … decreases"* · *"increasing number of particles"* 모두 숫자 · 그림 없음 (Fig 8 은 예시 한 장).
12. **결과는 0 · 2000 bar 두 상태만** — 300 · 600 bar 접촉 목록을 만들었다면서 (p.544) 결과 없음.
13. **식 표기** — 식 (3) · (4) N⁽⁴⁾ᵢⱼ (ijkl 이어야) · 부록 B 2 차 λ D⁽²⁾ᵢⱼD⁽²⁾ₖₗ (첨자) · 표 3 열 머리 '%' 인데 값은 분율.
14. **참고문헌 목록 결함** — [11] *J. Manuf. Sci. Eng. 136 (2) (1966) 89–90* (권 136 ↔ 1966 년) · [24] *Geotechnique 55 (4)* ↔ 붙은 주소 '55.3.245' · [26] McDowell · de Bono *Geotechnique 63* (쪽 · 연도 없음) · [31] Parteli *Sci. Rep. 4* (쪽 없음) · [37] 'granlar' · 'calendaring' (전체 표기).
15. **DEM 입자 수 · 시간 간격 · 판 속도 · 감쇠 · 시드 · 반복** 없음 → 재현 불가.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 13 | M. Ebner, F. Geldmacher, F. Marone, M. Stampanoni, V. Wood, X-ray tomography of porous, transition metal oxide based lithium ion battery electrodes, Adv. Energy Mater. 3 (2013) 845–850. | 쓴 CT 자료 · 큰 입자 파쇄의 원 관측 | `ebner2013_srxtm_nmc_cathode_microstructure_open_dataset_segmentation` |
| 18 | K.-I. Kanatani, Distribution of directional data and fabric tensors, Int. J. Eng. Sci. 22 (2) (1984) 149–164. | 식 (3) · (4) · χ² 검정의 원전 · 2D 계수 | 없음 (papers/ ls · grep) |
| 36 | T. Pöschel, T. Schwager, Computational Granular Dynamics: models and Algorithms, Springer Science & Business Media, 2005. | '큰 입자 = 접촉 많음 = 잘 깨짐' · 파편 맞바꿈의 출처 (R7 사슬 끝) | 없음 |
| 26 | G. R. McDowell, J. P. de Bono, On the micro mechanics of one-dimensional normal compression, Geotechnique 63. | 깨지는 입자 DEM 일축 압축 (파편 겹침) | 없음 (서지 일부만) |
| 24 | S. Lobo-Guerrero, L.E. Vallejo, Crushing a weak granular material: experimental numerical analyses, Geotechnique 55 (4) (2005) 245–249. | 입자 쪼개기 DEM (질량 비보존 쪽) | 없음 |
| 50 | L. Yi, K. Dong, R. Zou, A. Yu, Coordination number of the packing of ternary mixtures of spheres: DEM simulations versus measurements, Ind. Eng. Chem. Res. 50 (14) (2011) 8773–8785. | 3 크기 혼합 배위수 DEM ↔ 측정 (우리 12:4:1 접촉망) | 없음 |
| 12 | M. Ebner, D.-W. Chung, R.E. García, V. Wood, Tortuosity anisotropy in lithium-ion battery electrodes, Adv. Energy Mater. 4 (5) (2014), http://dx.doi.org/10.1002/aenm.201301278. | 방향별 tortuosity (접촉 방향 ↔ 수송) | 없음 (wishlist 에 있음) |
| 6 | D.-W. Chung, M. Ebner, D.R. Ely, V. Wood, R.E. García, Validity of the Bruggeman relation for porous electrodes, Model. Simul. Mater. Sci. Eng. 21 (7) (2013) 074009. | 입도 (r̄ 6 µm · δ 0.4) 출처 · Bruggeman 검토 | 없음 |
| 31 | E. J. Parteli, J. Schmidt, C. Blümel, K.-E. Wirth, W. Peukert, T. Pöschel, Attractive particle interaction forces and packing density of fine glass powders, Sci. Rep. 4. | 침강 Φ 경험식 · 부착 효과 | 없음 (wishlist 에 있음) |
| 9 | K.W. Desmond, E.R. Weeks, Influence of particle size distribution on random close packing of spheres, Phys. Rev. E 90 (2) (2014) 022204. | Φ_RCP(δ, S) 식 | 없음 |

---

## [미확인] 목록
- 배위수 n_c 를 쌍마다 한 번 셌는지 두 번 셌는지 · DEM 접촉 벡터 종류.
- CT 'NMC 부피 분율' (표 3) 의 계산 영역 · 방법.
- DEM 입자 수 · 시간 간격 · 판 속도 · 감쇠 · 구름 마찰 · 침강 멈춤 기준 · 시드 · 계산 시간 · 300 · 600 bar 결과.
- E_NMC 113 GPa · 표 2 다른 값의 출처.
- Δf 장미도의 정규화 · Fig 6 칸별 축척 · CT 쪽 크기 숫자.
- 파편 크기 · 구형도 · 입자 수의 압력별 숫자 · 크기별 파쇄 통계.
- 2D fabric tensor 계수 (원전 [18]).
- Parteli 식에 넣은 r̄ · '맞는다' 의 비교 대상.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-16)
- 서지: 1저자 메모 (A. J. Stershic, S. Simunovic, J. Nanda, 제목 · J. Power Sources 297 (2015) 540–550 · DOI) = 원문 첫 쪽 · PDF 메타데이터 (subject 줄) 와 같음.  zhang2026 원문 [30] *"A.J. Stershic, S. Simunovic, and J. Nanda, J. Power. Sources 297, 540 (2015)"* · ge2022 카드 [20] (이름 머리글자 'A.' 만) · song2025 카드 [18] — 권 · 쪽 · 연도 같음.
- 숫자: 텍스트 층 + 렌더로 대조 — 300 · 600 · 2000 bar · 30 · 60 · 200 MPa · 15 mm · 24 h · 55 °C · 0.7 mm · 330 µm · 370 nm · r̄ 6 µm · δ 0.6r̄ · 0.4 · 표 1 · 2 · 3 · 4 전부 · 340 × 340 × 220 µm · 0.06–0.11 · 0.64 · 0.74 · Φ_RCP 식 · 0.678 · δ · S 네 값 · 0.686 · 0.684 · Parteli 식 · 0.38 · 6–8 · 2 · 6 · 26 · 13 · 99 % · χ²(5) · χ²(9) — 전부 위치 확인.
- 'plastic' 0 회 · 'unload' = 0 bar 상태 뜻으로만 (Fig 4 캡션 *"unloaded assembly"* · p.546 *"when unloaded"*) · 'release' · 'springback' 0 회 · 'Supplementary' 0 회.
- 인용한 쪽 대조: zhang2026 PDF (같은 inbox) 텍스트 층에서 ref 30 은 p.12 한 곳 (Fig 9 문단 끝) — 문장 전문을 §0-1 에 옮김.
- 정본 중복 확인: papers/ 목록 (stershic* 없음) · DOI · 'fabric tensor approach' · 'Stershic' · 'Simunovic' grep — 카드 없음 (zhang2026 · ge2022 · song2025 · du2025 · ngandjong2021 = 인용만).

## 🔗 관련 카드
- 이 논문을 인용한 카드: `zhang2026_xct_dem_cathode_calendering_peel_calibration` (ref 30) · `ge2022_xct_initial_structure_dem_calendering_nmc333` ([20]) · `song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage` ([18]) · `du2025_dem_fem_force_chain_collector_damage_calendering` ([72]) · `ngandjong2021_dem_calendering_digital_twin` ([42]).
- 같은 CT 자료 (Ebner 2013): `ebner2013_srxtm_nmc_cathode_microstructure_open_dataset_segmentation` (원전) · `ge2022_…` (같은 자료 위 EEPA DEM) · `zhang2026_…` (같은 자료 출발 DEM).
- 배위수 · 충전: `german2014_coordination_number_powder_densification` (N_C = 2 + 11f²) · `onoda1990_random_loose_packing_uniform_spheres_dilatancy_onset`.
- 입자 파쇄 (R7): `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem` · `song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage` · `heenan2020_nmc811_calendering_defects_cycling_cracking_multiscale_xct`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

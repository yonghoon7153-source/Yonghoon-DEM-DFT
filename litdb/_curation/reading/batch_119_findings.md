# batch 119 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 표 N-67)

대상: `ge2022_xct_initial_structure_dem_calendering_nmc333` — R. Ge · D. J. Cumming · R. M. Smith, "Discrete element method (DEM) analysis of lithium ion battery electrode structures from X-ray tomography-the effect of calendering conditions", *Powder Technology* **403** (2022) 117366 · DOI 10.1016/j.powtec.2022.117366 · CC BY · 10 쪽 · SI 안내 없음
Ebner 2013 의 싱크로트론 X 선 CT (복셀 0.37 µm) 가 분할 · 표지한 미압연 NMC333 : C65 : PVDF = 90 : 5 : 5 양극에서 입자 5106 개의 위치 · 지름을 가져와 구로 바꾸고, CBD 부피만큼 Potyondy–Cundall 결합을 건 뒤 EEPA (n 1.5) 접촉 · 강철 윗판 0.01 m s⁻¹ 로 0 → 2000 bar 를 눌러 같은 압력의 CT 와 AM 밖 부피 · 굴곡 인자 (TauFactor) 를 견주고, 힘 망 · 직물 · 응력 텐서와 수준집합 바인더 생성의 τ 를 보고한다 — 탈압 · 파괴 · 형상 변화 없음.
쪽 = 학술지 논문 번호 117366 의 p.1–10 (PDF 쪽 = 인쇄 쪽) · 판독 원자료 = `litdb/figures/ge2022_xct_initial_structure_dem_calendering_nmc333/digitized.csv` (91 행 · Figs 1c · 4 · 7 · 10 · 11 · 12 · 13c) · 고른 의도 = '단계 5 (출발 상태) — X-CT 미압연 구조를 DEM 에 넣어 공극 · 접촉망 · 응력을 분석 · 판 속도 0.01 m s⁻¹ · he2026 [39] 와 같은 논문인지' (zhang2026_xct L38 · L96 · L139) → **채움** (he2026 [39] 귀속은 일부 — μ 0.25 만 이 논문에 있다).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — SE 없음 (액체계 LIB 양극).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 탈압 계산 없음 (판을 내리는 가압만 · EEPA 제하 가지 k2 · δp 는 법칙 식 (4) 에만).  반면교사 하나:
- [b] ge2022_xct_initial_structure_dem_calendering_nmc333 | DEM 구조 (판 압력 도달 · 제하 없음) 와 Ebner CT (압연 뒤) 를 같은 압력 점으로 견준다 (Fig 7 · 12) — 상태가 다른 두 칸 · 0 bar DEM 0.628 ↔ CT 0.599 (+0.029) · 2000 bar 0.417 ↔ 0.419 | 카드 §3-3 · §0-1 · p.4–5 · Fig 7 | [인쇄] 판 0.01 m s⁻¹ · [판독 · 벡터] CT 값 · [카드 추론] DEM 상태 = 누른 채 | 되돌아옴 양 없음 · 같은 Ebner 자료로 제하를 한 것은 zhang2026_xct (200 MPa 하중 중 ≈0.152 → 제하 ≈0.319 [다른 카드])

## c — 항복 · 경도 · 크리프 값과 정의
- [c] ge2022_… | 항복 값 없음 — EEPA 접촉 소성 비 λp = 1 − k1/k2 (식 6) 는 정의만 · 값 미인쇄 · k1 = (4/3)√R* E* (n 1.5 · 식 5) · 결합 인장 강도 σ_n = 3 × 10⁸ Pa · 결합 강성 k_b = 1.5 × 10¹⁴ N m⁻³ (*"based on calibration results as illustrated in the following Fig. 4"* — Fig 4 는 공극 계산법 오차 그림 · 보정 대상 [미확인]) · 일축 항복 환산 없음 | 카드 §3-2 · §4-2 · p.2–4 · 식 (4)–(6) · (25)–(26) | [인쇄] | 결합 = CBD 대리 · SE · AM 의 항복이 아니다

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 상별 하중 몫 없음 (AM 한 상 + 결합).  정성만:
- [d] ge2022_… | 힘 망 (Fig 9 · 식 35 = 상태마다 자기 최대로 정규화) *"With increased calendering stress, the particle contact force becomes more obvious, and force chains are formed."* (p.6) · 결합 힘 ↔ 접촉 힘 몫 · 배위수 숫자 없음 | 카드 §3-6 · p.6 · Fig 9 | [인쇄] (정성) | 그림 사이 굵기로 절대 힘을 견줄 수 없다

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] ge2022_… | 대안 = EEPA (원전 Thakur 2014 · n 1.5 · 적재 k1 · 제하 k2 · 점착 k_adh · 식 3–16) + Potyondy–Cundall 결합 (식 17–26) — **맞춘 값** = 결합 둘 (k_b · σ_n · 대상 미기재) + 결합 생성 배수 둘 (ζ_b 1.67 · λ_b 0.5 = 모든 입자 결합 + 결합 부피 = CBD 부피) · 나머지 (E 144 GPa · ν 0.25 · μ_s 0.25 · μ_r 0.01 · e 0.5) 문헌 · EEPA λp · f₀ · k_adh · 표면에너지 값 미인쇄 → 보정된 세트로 못 쓴다 | 카드 §3-2 · §4-3 · 표 1 · p.2–4 | [인쇄] · [미확인] | 깨지는 범위 (겹침 · 밀도 상한) 진술 없음 · 다접촉 보정 없음
- [e] ge2022_… | ⚠ 귀속 함정: he2026 [39] · du2025 [25] 가 이 논문에 단 값 (구름 0.014 · COR 0.25 · EEPA 표면에너지 8 J m⁻² · λp 0.96 · f₀ 1.5 × 10⁻⁵ N) 가운데 원문에 있는 것은 μ_s 0.25 (와 du2025 의 μ_r 0.01) 뿐 · 원문 e = **0.5** · 'surface energy' · 'pull-off' · '0.96' · '0.014' 낱말 0 건 | 카드 §0-1 · 표 1 · 원문 대조 기록 | [인쇄] | he2026 원문 참고문헌 목록은 보지 못함 (카드 문제 ① · ②)

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 MPM 없음 (공극 점 세기의 해상도 규칙만 — m 둘째).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — DEM · 복셀 τ 모두 3D (2D 는 표시용 단면 Fig 8 · 13a–b).

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
- [h] ge2022_… | 넘김 = 각 압력 점의 DEM 구조 → 격자 복셀 (0.5 µm · 150 × 150 µm × 전체 두께 ∼30–70 µm) → TauFactor 정상 확산 해 (영상 계산 · 역학 넘김 아님) · 대표 부피 20–100 % 에서 τ 차 < 5 % · 반대 방향 선례 = 분할 · 표지된 CT 입자 → DEM 처음 구조 | 카드 §4-1 · §3-8 · p.2–3 · p.5–6 | [인쇄] | FE · MPM 넘김 아님 · 넘긴 시점 = 판 압력 도달 구조 (제하 전)

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — SE 없음.  LIB 양극 (AM + CBD) 의 압력별 공극 (참고 · 랩 표준 옆에 놓지 않음):
- [i] ge2022_… | AM 밖 부피 (공극 + CBD) DEM 0.628 · 0.601 · 0.570 · 0.417 ↔ Ebner CT 0.599 · 0.611 · 0.559 · 0.419 · CBD 를 조밀 고체로 뺀 ε_Pore 0.525 · 0.49 · 0.45 · 0.255 (0 · 300 · 600 · 2000 bar) · 두께 h_c ≈75 · 56.3 · 49 · 36.5 µm | 카드 §3-3 · §3-4 · 표 2 · Fig 6 · 7 | [인쇄] 표 2 · Fig 6 · [판독 · 벡터] Fig 7 · [카드 산술] 1 − φ_Par | SE 없음 · 공극 = AM 밖 (진밀도 분모 없음) · 상태 섞임 · φ_Par·h_c 가 0 bar 만 27.9 ↔ 21.1–22.5 µm

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] ge2022_… | 원문: 구 근사 · 파괴 미포함 → *"These limitations may affect model prediction, especially under high calendering pressures"* (p.9) · 바인더 나노 기공 미분해 (p.8) · 다음 일 = 비구형 입자 · CT 로 분해한 CBD 를 DEM 에 · 입도 분포 · 바인더 부피 효과 · 전기화학 해석 (p.9) | 카드 §0 ⑨ · §4-4 | [인쇄] | 탈압 · 되돌아옴은 한계 목록에도 없다
- [j] ge2022_… | 카드가 본 것: 결합 '보정' 대상 미기재 (Fig 4 오참조) · 응력 텐서 V 미기재 (σzz = 명목 0.38–0.46) · 같은 양이 Fig 12 ↔ Fig 13c 에서 1.74 ↔ 1.63 (2000 bar) · 'mono-sized' ↔ 다분산 · '0 bar to 400 bar' (400 bar 상태 없음) · 0 bar φ·h 어긋남 · 식 (22) · (24) 단위 · Fig 1c 입도 꼬리 ≈41 µm ↔ DEM 색 막대 28 µm | 카드 §11 | [판독] · [카드 산술] | —

## k — DEM 의 한계 (원문 문장 · 인용 서지 = Ge, Cumming & Smith 2022, Powder Technol. 403, 117366)
- [k] ge2022_… (Ge, Cumming & Smith 2022, Powder Technol.) | *"Due to the soft particle model used in DEM simulations, the AM particles undergo deformations during calendering, and overlaps between AM particles can occur. Therefore, the accurate calculation of porosity is non-trivial and cannot be directly calculated using an analytical method."* (p.4) | 카드 §4-4 (i) · `txt_p4_porosity_soft_particle_overlap_nontrivial.png` | [인쇄] | 믿을 수 있는 겹침 상한 숫자 없음
- [k] ge2022_… (Ge et al. 2022) | *"Firstly, when using spherical approximations of AM particles in DEM simulations there is some volume loss."* (p.5) | 카드 §3-3 · `txt_p5_porosity_definition_agreement_volume_loss.png` | [인쇄] | 손실량 숫자 없음
- [k] ge2022_… (Ge et al. 2022) | *"The slight discrepancy may be due to plastic deformation and breakage of AM particles in calendering experiments, which was not captured in the simulation results here [12]. Another cause for discrepancy reason is the non-uniform, non-spherical shape of AM particles, which cannot be captured by current DEM simulations."* (p.7) | 카드 §4-4 (i) · `txt_p7_tortuosity_dem_vs_xct_plastic_breakage_shape.png` | [인쇄] | —
- [k] ge2022_… (Ge et al. 2022) | *"It is important to emphasise that spherical particle approximations were used in this work, and the effect of particle fracture is not considered. These limitations may affect model prediction, especially under high calendering pressures."* (p.9) | 카드 §4-4 (i) · `txt_p9_conclusions_spherical_no_fracture.png` | [인쇄] | '고압' 의 문턱 없음
- [k] ge2022_… (Ge et al. 2022) | 앞선 가상 구조 DEM 에 대해: *"By purely considering the electrode structure and AM particle size distribution, the DEM simulations could not predict the evolution of inter-particle contacts."* · *"The virtual structures in previous works with an incorrect calculation of volume fractions will therefore provide an unrealistic representation of the calendering process"* (p.2) | 카드 §4-4 (i) · `txt_p2_intro_virtual_structures_unrealistic.png` | [인쇄] | —

## l — 소성변형이 왜 어려운가 · 우회 · 비용 (인용 서지 = Ge, Cumming & Smith 2022, Powder Technol. 403, 117366)
- [l] ge2022_… (Ge et al. 2022, Powder Technol.) | '왜 어려운가' 를 설명하는 문장은 없다 · 택한 우회 = **접촉 법칙 안의 소성** (EEPA: 소성 겹침 δp · 제하 강성 k2 > k1 · λp — 입자 모양은 구 그대로 · 겹침 δ 가 변형 대리 *"soft particle model … overlaps between AM particles can occur"*) + 바인더 = 결합 (부피 = CBD) · 비용 = 겹친 구라 공극을 해석으로 못 세서 점 세기 (Monte Carlo · 격자 · Fig 4 오차 사다리) · 빠진 것 = AM 소성 형상 변화 · 파괴 · 비구형 (p.7 · p.9 스스로 적음) · 맞춘 값 = 결합 둘 (대상 미기재) + 생성 배수 둘 · 계산 비용 · 시간 간격 미기재 | 카드 §4-4 (ii) · p.2–5 · 7 · 9 | [인쇄] · [카드 추론] | MPM · 입자별 FE · 다접촉 보정 언급 없음

## m — 받아들일 통찰
- [m] ge2022_… | **부피 평균 응력은 판 (벽) 반력과의 비를 함께 적는다** — 이 논문 σzz (식 38) 는 명목 판 압력의 0.455 · 0.439 · 0.383 인데 원문은 견주지 않는다 · song2025_insitu_ct 0.51–0.57 [다른 카드] · 우리 MPM 은 같은 함정 (wallP 1.08 ↔ 부피 평균 0.09 GPa) 으로 판독을 wallP 로 바꿨다 · V 가 약분되는 측압 비 (σxx+σyy)/2σzz (0.16 → 0.54) 를 우선 | 단계 0 (관측량 칸) · 흐름 밖: DEM LW · virial ↔ c_strs 점검 | 카드 §3-7 · §7-3 · Fig 11 [판독] · [카드 산술]
- [m] ge2022_… | **공극 연산자 단위 시험의 꼴** — 겹치지 않는 구 (2–30 µm · 한 변 50 µm 정육면체) 의 해석 합 ↔ 점 세기 (격자 · Monte Carlo) 를 점 수 사다리로: 9.8 × 10⁵ 점에서 격자 2.07 % ↔ Monte Carlo 0.027 % · 격자 0.81–0.40 µm 에서 1.85–2.07 % 로 평평 (격자를 줄여도 안 준다) → 우리 정확 union MC · ε_sphere 연산자를 같은 시험으로 | U0 · 단계 0 | 카드 §3-5 · Fig 4 [판독 · 벡터 좌표]
- [m] ge2022_… | **공극 칸에 정의 · 측정 상태 · 고체 보존을 결과 전에 등록** — 같은 구조에서 'AM 밖 (CBD = 빈 곳)' ↔ 'CBD 조밀' 이 0.10–0.16 갈리고 · DEM (누른 채) ↔ CT (뺀 뒤) 가 한 그림에 놓이고 · φ_Par·h_c 가 0 bar 만 27.9 ↔ 21.1–22.5 µm 로 어긋난다 | 단계 0 · 결과 전 대조 항목 | 카드 §3-3 · §3-4 [인쇄 · 카드 산술]
- [m] ge2022_… | **실측 출발 상태 경로 (분할 · 표지된 CT 입자 → 부피 같은 구 → 무른 상 부피만큼 결합 → 옆 주기 · 판 압축)** — 남이 분할한 자료를 쓸 때는 입도 (Fig 1c 꼬리 ≈41 µm ↔ DEM 색 막대 28 µm) · 영역 · 두께 (0 bar φ·h) 가 서로 맞는지부터 점검 · 판 속도 0.01 m s⁻¹ 는 우리 DEM 판 속도 (0.01 mm s⁻¹) 의 1000 배 · 준정적 점검 원문 없음 | 단계 5 | 카드 §3-1 · §3-9 · §8

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드 없음 · papers/ ls + grep 확인)
- [n] [37] Luca Orefice, Johannes G. Khinast, Deformable and breakable DEM particle clusters for modelling compression of plastic and brittle porous materials — Model and structure properties, Powder Technology 368 (2020) 90–104, https://doi.org/10.1016/j.powtec.2020.04.035. (원문 목록 그대로) | 이 논문 공극 계산법 (식 29–30 · Fig 3) 의 출처 · 변형 · 파괴 가능한 DEM 입자 묶음으로 소성 · 취성 다공 재료 압축 — l · e · 후보 C · R7 | litdb 확인: papers/ 에 orefice* 없음 · 'Orefice' grep = du2025_dem_fem_… (인용만)
- [n] [16] R. Ge, M. Ghadiri, T. Bonakdar, Q. Zheng, Z. Zhou, I. Larson, K. Hapgood, Deformation of 3D printed agglomerates: multiscale experimental tests and DEM simulation, Chem. Eng. Sci. 217 (2020) 115526. (원문 목록 그대로) | 표 1 μ_p,s 0.25 의 이 논문 쪽 출처 ([16,20]) · 같은 저자의 결합 DEM 보정 계보 — e · 카드 문제 ① | litdb 확인: papers/ 에 ge2020* 없음 · '115526' grep 0
- [n] [26] D.O. Potyondy, P. Cundall, A bonded-particle model for rock, Int. J. Rock Mech. Min. Sci. 41 (8) (2004) 1329–1364. (원문 목록 그대로) | 결합 모델 원전 — 이 논문 식 (22) · (24) · (26) 의 단위 · 극관성 표기 대조 — e · R2 · R7 | litdb 확인: papers/ 에 potyondy* 없음 · 'Potyondy' grep = he2026 · lyu2025 · lyu2026 · morrissey2013 · otani2025 · schreiner2020 등 (인용만)
- [n] [35] B.L. Trembacki, D.R. Noble, M.E. Ferraro, S.A. Roberts, Mesoscale effects of composition and calendering in lithium-ion battery composite electrodes, J. Electrochem. Energy Convers. Stor. 17 (4) (2020). (서지 일부만 — 쪽 · DOI 없음) | 수준집합 바인더 생성 (식 39) 의 원전 · 조성 · 압연의 메소 효과 — m · 단계 7 | litdb 확인: papers/ 에 trembacki* 없음 · 'Trembacki' grep = benhadjali2025 · chouchane2021 · park2019 · park2020 · tjaden2018 (인용만)
- [n] [22] I. Srivastava, D.S. Bolintineanu, J.B. Lechman, S.A. Roberts, Controlling binder adhesion to impact electrode mesostructures and transport, ACS Appl. Mater. Interfaces 12 (31) (2020) 34919–34930. (원문 목록 그대로) | 점착으로 전극 메소구조 · 수송을 조절한 DEM — e · 단계 7 · 믹서 Ⓒ 의 점착 축 | litdb 확인: papers/ 에 srivastava* 없음 · '34919' grep 0 · 'Srivastava' grep = lippke2023 · ngandjong2021 · zhang2026_xct (언급만)
- (이미 다른 자리에 있음 — 새로 올리지 않음) [12] Ebner 2013 = 후보 표 N-66 · [20] Stershic 2015 = N-69 · [28] Usseglio-Viretta 2018 = wishlist L75 · 같은 그룹 후속 Ge 2023 *Chem. Eng. J.* 465, 142749 = wishlist L326 (이 논문은 인용하지 않음 · he2026 [39] 귀속을 가를 후보).

## 카드 문제
- ① `he2026_dem_calendering_inhomogeneity_areal_density` **L94–L98** — [39] Ge 2022 로 단 구름 **0.014** · COR **0.25** · EEPA 표면에너지 **8 J m⁻²** · λp **0.96** · f₀ **1.5 × 10⁻⁵ N** (L98 = [39–41]) 이 이 논문 (본문 · 표 · 그림 10 쪽) 에 숫자로 없다 — 원문 표 1 = μ_s 0.25 · μ_r **0.01** · e **0.5** · λp · f₀ · k_adh 는 식 기호만 · **L262** *"([39] Ge 2022 에서 그대로 가져옴)"* (EEPA 매개변수 재사용) 도 같은 문제 · L93 의 μ 0.25 만 같다.  he2026 원문 참고문헌 목록은 보지 못해 [39] 가 이 논문인지는 판정하지 않는다 (고치지 않음 · 새 카드 끝에 관련 카드 한 줄만).
- ② `du2025_dem_fem_force_chain_collector_damage_calendering` **L151** (반발 계수 0.25 = [25] Ge 2022) · **L73** (*"COR 0.25 (모두 [25] Ge 2022)"*) · **L486** ([25] 설명 *"μ 0.25 · μr 0.01 · COR 0.25"*) — 이 논문 표 1 e = **0.5** (μ_s 0.25 · μ_r 0.01 은 같다).  그 카드는 Du 2025 원문 표 1 을 옮긴 것으로 보여 Du 원문의 귀속 문제일 가능성 (관찰 · 고치지 않음).
- ③ (같음 · 기록) `zhang2026_xct_dem_cathode_calendering_peel_calibration` **L96** (Ge = X-CT 미압연 구조 → DEM · 공극 · 접촉망 · 응력) · **L139** (0.01 m s⁻¹ · ref 18 과 일관) · **L54** (X-CT → DEM 은 ref 18 이 먼저) — 원문과 같다 (zhang2026 원문 p.2 · p.4–5 · 참고 18 직접 대조).  단 L139 의 '가압·제하 동일' 의 제하는 zhang2026 자신의 절차이고 이 논문에는 제하가 없다 (zhang2026 원문도 인용 18 을 속도에만 붙인다) — 문제 아님.  **L38** *"정본 카드가 없고 이번에 읽지 않았다"* = 이 카드로 해소.
- ④ (같음) `lyu2026_two_layer_gradient_electrode_calendering_dem_fem` **L349** ([60] Ge 2022 = 마찰 0.25 출처) — 표 1 μ_p,s 0.25 와 같다 (단 이 논문 자신은 [16,20] 을 출처로 단다 · 2 차 출처).
- ⑤ (관찰 · 이 논문 쪽) 표 1 E 144 GPa 의 출처 [19,27] — `sangros2019_dem_calendering_lib_electrode` L34 의 Giménez 2019 = **142 GPa** · `devasconcelos2016_grid_indentation_nmc532_cbpvdf_composite_electrode` L50 의 de Vasconcelos 2016 = **138.73 GPa** — 어느 쪽과도 같지 않다 (그 두 카드는 맞음 · 고칠 곳 없음).

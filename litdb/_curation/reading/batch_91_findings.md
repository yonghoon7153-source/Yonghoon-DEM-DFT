# batch 91 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `clemmer2024_bpm_elastic_grain_compaction_beyond_jamming` — J. T. Clemmer, J. M. Monti, J. B. Lechman, "A soft departure from jamming: the compaction of deformable granular matter under high pressures", *Soft Matter* 20 (2024) 1702–1718 · DOI 10.1039/D3SM01373A (이 PDF = 2024-08-30 정정판 · 식 (3) · (4) 정정).
입자 하나를 점 입자 ~5000 개 결합망 (BPM · LAMMPS) 으로 풀어 선형 탄성 단분산 구 1024 개를 등방 · 주기로 재밍 너머 (P/E_eff ~1 · φ_MC → 1) 까지 누르고 마찰계수만 φ_c 에 맞춘 Hertz DEM 과 견준 3D 계산 논문 — 실험 · 전지 재료 · 소성 · 탈압 없음.
쪽 = PDF 쪽 p.1–17 (인쇄 쪽 = PDF 쪽 + 1701) · ESI 없음 · 판독 원자료 = `litdb/figures/clemmer2024_bpm_elastic_grain_compaction_beyond_jamming/digitized.csv` (275 행 · 래스터 300 dpi · 방법은 note 열).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (재료 없음 — 있는 것은 무차원 선형 탄성 단분산 구 침대의 P/E_eff ↔ φ_MC 곡선 (Fig. 6b) 뿐 · 진밀도 · 질량 기공 없음).  카드 §7-3 이 그 곡선에 LPSCl DFT 탄성 (E 22.06 · ν 0.360) 을 넣어 계산한 "300 MPa → φ_MC ≈ 0.74–0.75" 는 [카드 산술] (등방 · 단분산 · 탄성만) 이지 SE 측정이 아니다 — 랩 표준 (10–13 % · 1.64 g/cm³) 과 같은 표에 넣지 않는다.

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
- [b] clemmer2024_… | 탈압 · 되돌아옴은 **하지 않았다** — 대신 압밀 중 저장한 상태에서 침대 탄성률을 작은 변형으로 잼: 10⁵ 걸음 이완 뒤 부피 0.06 % (10⁻⁸ τ⁻¹) · 전단 0.04 % (2×10⁻⁸ τ⁻¹) · 실현 5 개 중 2 개 · K_P ∝ (φ − φ_c)^{1/2} · G_P ∝ (φ − φ_c) → 가속 · ν_P 1/2 (재밍) → 최소 ~1/4 (φ − φ_c ≈ 0.1) → 상승 | 카드 §3-9 · p.13 · Fig. 14 · [판독] ν_P 최소 0.26 (ν −0.11) · 0.29 (0.4) · 0.30 (0.25) · 끝 0.32–0.39 | 인쇄 + 판독 | 탈압 곡선 아님 · 선형 탄성 (소성 잔류 없음) · Fig. 14 세로축 단위 [미확인]

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 (항복 · 경도 · 크리프 없음 — 선형 탄성만 · 보정은 탄성률 맞춤식 G/K ≈ 0.6 + 0.475 a_B/(kd) · K = 1.365 k/d − 0.14 k²(a_B + 1.168kd)⁻¹ (카드 §3-2 · p.5) 뿐).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (한 상 · 단분산 — 재밍 자체 (φ_c 0.5979 / 0.5836 · Z_c ~5.2 / ~5.05) 는 있으나 하중 몫 없음).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] clemmer2024_… | 단일 입자: 매끈한 BPM 구를 두 벽 사이에서 누르면 Hertz (3/(8R²E_eff)) f = (δ/R)^{3/2} 와 *"well described … up to significant overlaps of 25% of the radius"* · 거친 입자는 더 약함 (요철) · 양 끝 ν 에서 조금 벗어남 · FEM 연구는 큰 압입에서 Hertz 가 힘을 과소 예측 (ref 68) | 카드 §3-4 · p.7 · p.9 · Fig. 4 | 인쇄 | 탄성 · 무차원
- [e] clemmer2024_… | 침대: φ − φ_c ≈ 0.1 에서 DEM 이 BPM 과 갈라짐 — *"contact forces are no longer accurately described as Hertzian due to elastic interactions between contacts"* · 그래도 같은 φ_MC 로 *"differences never exceeded a factor of two"* ([판독] P_BPM/P_DEM 1.1–1.8 · DEM 이 더 무름) | 카드 §3-6 · §3-7 · p.10 · p.14 · Fig. 6b · 7 | 인쇄 + 판독 | 선형 탄성 · ν −0.11–0.4 한정
- [e] clemmer2024_… | 대안 = 비국소 DEM (refs 27 Gonzalez 2012 · 75 Giannis 2021) *"would likely improve DEM results"* — 시험 안 함 · 갈림점은 Harthong 2012 MPFEM 의 접촉 독립 깨짐 φ ≈ 0.7 과 같은 자리 · 맞춘 값 수: BPM = 결합 계수 둘 (k_B · a_B — 탄성률 맞춤식) + 고정 a_P = 50k/d² · Γ = √(km) / DEM = 마찰 셋 {μ_s, μ_r, μ_t} 를 φ_c 에만 맞춤 (입자 종류마다 두 짝) | 카드 §3-2 · §3-6 · p.5 · p.9 · p.14 | 인쇄 | 대안 법칙의 정량 없음

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
- [f] clemmer2024_… | MPM 아님 — 입자 해상 (BPM) 의 해상도 규칙: 덩어리 탄성률 |K(L)/K(200) − 1| ∝ L⁻² · 산포 σ_K/K ∝ L⁻³ᐟ² · 비affine 변형률 ∝ L⁻¹ · L ~ 16 (점 ~5000) 에서 물성 산포 < 1 % · 입자 안 국소 변형률 0.1–0.01 % · 압밀 곡선은 입자 반지름 2.5 · 5 · 7.5 · 10d 사다리에서 수렴 (7.5d ↔ 10d 차 < 표지 크기) · 선형 탄성 벗어남 ≈ 10 % at 변형률 10 % · 부피 변형률 50 % 에서 압력 ~2 배 | 카드 §3-3 · p.5 · p.6 · p.9 · p.15 · Fig. 15 · 16 | 인쇄 | MPM 격자 규칙 (지름당 셀 수) 으로 그대로 옮기지 않는다 — 보고 꼴 (사다리 · 기울기) 만

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] clemmer2024_… | Cauchy 관계: 쌍 중심력만 쓰는 무질서 충전의 ν 는 **2D 1/3 · 3D 1/4** 로 묶인다 — 이산 모형의 ν 제약이 차원에 따라 다르다 | 카드 §3-1 · p.3 · `txt_p3_cauchy_poisson_2d_3d.png` | 인쇄 | 이산 결합 모형 한정
- [g] clemmer2024_… | *"most simulations have either been limited to two dimensions or only explored comparisons in compaction curves to experiments"* · 2D (Vu 2021 JMPS) 에서도 E_eff 척도가 ν 차를 설명했다 = 3D 결과와 같은 결론 | 카드 §0 표 ⑥ · p.1 · p.11 | 인쇄 | 2D → 3D 수치 전이 없음

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
- [h] clemmer2024_… | **DEM → 입자 해상 (BPM) 넘김**: 전통 DEM 으로 입자 1024 개 · 부피분율 57 % 의 **느슨한 틀** 을 만든 뒤 그 자리에 BPM 입자를 놓고 (주기 경계 넘어 점 · 결합 재배치) → 이완 · 살짝 팽창해 접촉을 모두 끊고 → 결합 평형 길이를 재설정해 **재밍 바로 아래 무응력 상태**에서 압밀 시작 | 카드 §3-5 · p.7 · Fig. 5a · b · `txt_p7_compaction_protocol.png` | 인쇄 | 넘긴 시점 = 재밍 전 (접촉 응력 0) — 압밀된 DEM 상태를 넘긴 것이 아니다 (우리 DEM → MPM 은 300 MPa 뒤 상태를 넘김)

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] clemmer2024_… | *"This comparison also assumes there is no plastic deformation or fracture in the system"* · *"many applications also depend on the activation of inelastic mechanisms not modeled here such as plasticity and cohesion as previously studied using MPFEM"* | 카드 §3-10 · p.14 · `txt_p14_conclusion_dem_factor_two_no_plasticity.png` · `txt_p14_limitations_idealized.png` | 인쇄 | 소성 · 응집 없음
- [j] clemmer2024_… | *"a rigorous characterization of deviations from linear elasticity at large volumetric strains ≳10% and frictional forces are uncharacterized"* · 마찰 ↔ 요철 대응 · 마찰계수 상한 / 하한 모름 (p.6) · 탈압 안 함 | 카드 §3-10 · §13 · p.6 · p.14 | 인쇄 | 큰 변형 · 마찰 미통제
- [j] clemmer2024_… | ν 실용 상한 ≲ 0.46 (순 다체력 0 구속이면 ~0.48) — 우리 MPM 의 ν 0.49 는 이 모형 범위 밖 | 카드 §3-2 · p.5 | 인쇄 | 비압축 근처 불안정

## k — DEM 의 한계
(인용 서지 = Clemmer, J. T., Monti, J. M., Lechman, J. B. (2024). A soft departure from jamming: the compaction of deformable granular matter under high pressures. Soft Matter 20, 1702–1718. doi:10.1039/D3SM01373A)
- [k] clemmer2024_… (Clemmer · Monti · Lechman 2024 · Soft Matter) | *"However, to explicitly model elastic deformation one inevitably needs to add internal degrees of freedom to grains to describe the internal strain field."* | p.2 · `txt_p2_dem_internal_dof_bpm_pros_cons.png` | 인쇄 | 입자 모양이 안 변한다는 한계의 원리 문장
- [k] clemmer2024_… (같은 서지) | *"At very high pressures in DEM simulations, deficiencies in the above definition of φ_sphere are apparent in Fig. 6(a) as it exceeds unity. … While this effect is negligible in the hard-particle limit typically studied using DEM, it is significant in the high pressure limit."* · [판독] P/E_eff ≈ 0.1 에서 φ_sphere 1.045 ↔ φ_MC 0.899 | p.9 · `txt_p9_phi_sphere_exceeds_unity_factor_two.png` · Fig. 6 | 인쇄 + 판독 | 구 부피 합 연산자의 한계 (겹침 이중 셈)
- [k] clemmer2024_… (같은 서지) | *"Of course, DEM simulations fail to account for elastic interactions between contacts such that more advanced nonlocal DEM contact models might provide even stronger agreement."* · *"This threshold may therefore mark the end of the assumption that grain–grain interactions are two-body."* (φ − φ_c ≈ 0.1) | p.9 · p.13 · `txt_p13_packing_poisson_minimum_two_body.png` | 인쇄 | 접촉 독립 가정이 깨지는 밀도 = φ − φ_c ≈ 0.1 (φ ≈ 0.69–0.70)
- [k] clemmer2024_… (같은 서지) | *"In traditional DEM simulations, Poisson's ratio only affects the stiffness of Hertzian contact force. Thus, DEM simulations produce trivially identical results as stresses are simply scaled by a constant factor, E_eff."* · 그래도 *"the predictions from DEM are still within a factor of two from the BPM simulations … assuming systems are nearly linear elastic"* | p.10 · `txt_p10_zc_deviation_factor_two_dem_poisson.png` | 인쇄 | 오차 크기 = 압력 ≤ 2 배 (선형 탄성 한정 · 같은 φ_MC 지표)
- [k] 말 없음: 보정값이 물성이 아니라는 고백 · 믿을 수 있는 겹침 상한 (DEM 쪽) — 원문 전수에 없음 (단일 입자 Hertz 일치 겹침 25 % 는 BPM 입자의 성질로 적힘).

## l — 소성변형이 왜 어려운가
- [l] clemmer2024_… (Clemmer · Monti · Lechman 2024 · Soft Matter) | 세 길의 비교: FEM (MPFEM · NSCD) = *"meshed-based methods can suffer from mesh entanglements at severe deformations … and may struggle to represent other discontinuous behavior relevant to compacted grains such as fragmentation"* · 메시 없는 연속체 (peridynamics · MPM) = *"fairly complex and computationally expensive"* · BPM = *"it is not always known apriori how to design or calibrate bond forces. Unlike FEM, there is also little information on convergence"* | p.2 · `txt_p2_dem_internal_dof_bpm_pros_cons.png` | 인쇄 | 소성 자체는 넣지 않음
- [l] clemmer2024_… (같은 서지) | 우회 = 탄성까지만 — *"elastic deformation always serves as a precursor to potential plastic deformation or fracture and is therefore an important limit to establish before overlaying such additional inelastic mechanisms"* · 패키지에 결합 기준 상태 · 변형률 이력 (*"to model plasticity"*, ref 64) · 끊김 (파괴) 기능만 | p.2 · p.8 · `txt_p8_dem_matching_lammps_cost.png` | 인쇄 | 소성 계산 없음
- [l] clemmer2024_… (같은 서지) | 비용 · 맞춘 값 · 검증: 점 ~5×10⁶ · 2×10⁷ 걸음 · ~40 h × 288 (다체 없음) / 480 (다체) 프로세서 · 다체 항 = 힘 계산 ~2 배 · 회전 자유도 = ~10 배 · 맞춘 값 = 결합 계수 (k_B · a_B → K · G 맞춤식 · 덩어리 변형률 0.5 %) · 검증 = 단일 입자 Hertz (겹침 25 %) · 해상도 사다리 (L⁻² · 반지름 7.5d 수렴) | p.4 · p.5 · p.7–9 · `txt_p4_volume_proxy_cost.png` · `txt_p5_gk_k_fits_poisson_limit.png` | 인쇄 | 탄성 한정 · 실험 검증 없음

## m — 받아들일 통찰
- [m] clemmer2024_… | **기공 연산자는 '입자가 부피를 보존하나' 로 고른다** — DEM φ_sphere 는 고압에서 1 을 넘는다 ([판독] Δφ = φ_sphere − φ_MC 0.004 (P/E_eff 6×10⁻³) → 0.018 (2×10⁻²) → 0.074 (6×10⁻²) → 0.146 (0.1)) · 탄성 압축 입자에는 합집합 (φ_MC = 점 d/2 구 ∪ 입자 볼록 껍질 · 10⁷ 점) · 우리 비압축 소성 SE 의 ε_sphere 정당화와 반대 경우 → 우리 쪽 어디에: **단계 0** (결과 전 등록에 연산자 선택 이유 + 이 크기) · 왜: p.8–9 · Fig. 6a ↔ 6b
- [m] clemmer2024_… | **탄성 한정 벤치마크가 이미 있다** — 단분산 탄성 구 1024 개 등방 주기 압축의 P/E_eff(φ_MC) (Fig. 6b: φ 0.75 ↔ 2.5×10⁻² · 0.85 ↔ 8.2×10⁻² · 0.90 ↔ 0.14 [판독 · 매끈]) → 우리 쪽 어디에: **U6 변형** (MPM 을 σ_y → ∞ 로 두고 등방 주기 모드로 같은 곡선을 내는지 · 지름당 셀 수 사다리) · 왜: 갈림점 · 2 배 · 해상도 수렴 (반지름 7.5d) 이 같이 보고됨 (p.9 · Fig. 6 · 7)
- [m] clemmer2024_… | **U1 시험 꼴** — 구 하나를 매끈한 두 벽 사이에서 대칭으로 누르고 (벽 속도 5×10⁻⁴ τ⁻¹) 두 벽 법선력 평균 · 질량 중심을 약한 스프링으로 붙듦 · 접촉 0 = 힘이 처음 10⁻³ E_eff R² 를 넘는 순간 · 방향을 바꾼 여러 표본 평균 → (3/(8R²E_eff)) f = (δ/R)^{3/2} 와 대조 → 우리 쪽 어디에: **U1** (MPM 입자 하나 압축) · 왜: p.6–7 · Fig. 4 · 식 (6)
- [m] clemmer2024_… | **"탄성만이면 φ ≈ 0.75"** — LPSCl DFT 탄성 (E 22.06 · ν 0.360 → E_eff 12.67 GPa) 을 Fig. 6b 에 넣으면 300 MPa (P/E_eff 0.024) 에서 φ_MC ≈ 0.74–0.75 · ε_V ≈ 1.6–2.4 % · α − α₀ ≈ 0.4–0.6 % [카드 산술 · 등방 · 단분산] → 우리 쪽 어디에: **단계 4** 의 기준선 (σ_y 하나가 메우는 몫 = 0.75 → 0.87–0.90) · **R6** (SEM 의 SE 형상 변화는 소성) · 왜: 카드 §7-3

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
litdb 확인 = 정본 `litdb/papers/` 파일 목록 (`git ls-tree` · 이 커밋 전 원격 끝 `f0940c23d` · 566 장) + `git grep` (권쪽 · 제1 저자 성 · 제목 낱말 · 파일 이름) — 아래 다섯 모두 자기 카드 없음.
- [n] B. Harthong, J.-F. Jérier, V. Richefeu, B. Chareyre, P. Dorémus, D. Imbault and F.-V. Donzé, Int. J. Mech. Sci., 2012, 61, 32–43. (원문 참고문헌 그대로 · ref 29) | e · k — MPFEM 탄소성 입자에서 접촉 독립이 φ ≈ 0.7 근처에서 깨진다 (원문 p.14 이 이 논문의 갈림점 φ − φ_c ≈ 0.1 과 같은 자리로 인용) · 카드 §0-1 (질문 e) · §12 | 정본 `harthong2009_high_density_compaction_dem_voronoi_contact_law` 는 다른 논문 (IJSS 2009) · '61, 32' · 'Harthong' grep = 2012 판 카드 없음
- [n] Q. Ku, J. Zhao, G. Mollon and S. Zhao, Powder Technol., 2023, 421, 118455. (원문 참고문헌 그대로 · ref 19) | l · 후보 B — 응집 소성 입자를 MPFEM 으로 큰 충전율까지 압밀 (이 논문이 다루지 않은 소성 · 응집의 선행 연구로 p.2 · p.14 에서 인용) · 카드 §12 | '118455' · 'Ku, ' grep = 카드 없음
- [n] J. T. Clemmer, K. N. Long and J. A. Brown, Mech. Mater., 2023, 184, 104693. (원문 참고문헌 그대로 · ref 64) | l · 후보 B — BPM 결합에 기준 상태 · 변형률 이력을 두어 **소성**을 넣는 방법 · 비affine 운동과 비선형 탄성 (p.6 · p.8) — "결합입자 소성" 의 원전 · 카드 §3-5 · §12 | '104693' · 'Mech. Mater., 2023' grep = 카드 없음
- [n] T. L. Vu, S. Nezamabadi and S. Mora, J. Mech. Phys. Solids, 2021, 146, 104201. (원문 참고문헌 그대로 · ref 16) | f · g — 2D MPM 변형 입자 압밀 · E_eff 척도가 ν 차를 설명 (p.11) · 카드 §0 표 ⑥ · §12 | '104201' grep = 카드 없음 (`vu2019_soft_grain_compression_beyond_jamming_dic` 는 PRE 2019 실험)
- [n] M. L. Hentschel and N. W. Page, J. Mater. Sci., 2007, 42, 1261–1268. (원문 참고문헌 그대로 · ref 80) | b · 단계 6 — 압밀 분말 (구리 · 강 · 알루미늄 · 유리) 의 포아송 비 최소 ~1/4 또는 조금 위 (실험 · p.13) — 탈압 강성 · 옆 팽창의 실측 · 카드 §3-9 · §12 | 'Hentschel' grep = 카드 없음

## 카드 문제
- 가리킨 카드 `sankar2026_fiber_scale_dem_carbon_felt_manufacturing` **L726** · **L45** · **L67** (고치지 않음): ref 73 Clemmer 2024 를 *"`bpm/rotational` 의 인용처"* · *"`bpm/rotational` (refs 72–73)"* 로 적었다 — 원문은 LAMMPS **BPM 패키지**를 소개한 논문이고 자기 계산은 **회전 없는 점 입자** 모형이다 · 회전 자유도 DEM 입자 + 전단 · 토크 결합 모형은 패키지에 *"as well as a more common model based on DEM particles with rotational degrees of freedom and bonds that transmit shear forces and torques.[51]"* 로 들어 있고 그 식은 **ref 51 (Y. Wang, Acta Geotechnol., 2009, 4, 117–127)** 에 귀속된다 · style 이름 'bpm/rotational' 은 원문에 0 회 → 패키지 인용으로는 맞고 회전 결합 식의 출처로는 아니다 (일부).  서지 값 (Soft Matter 20, 1702 · 2024) 은 원문과 같다 · 제목은 부제만 (*"A soft departure from jamming:"* 빠짐) · 저자 3 명 (Clemmer · Monti · Lechman).  L726 의 *"결합입자로 변형 입자를 고압 압밀한다면 우리 SE 18 배 연화의 대안 경로"* 는 원문이 **선형 탄성만** 다룬다는 한정이 필요하다 (소성 · 파괴 없음, p.14).
- `zunker2025_dem_large_deformation_compaction` L41 · L197 · L645 — 감사절의 Joel Clemmer (LAMMPS 구현 도움 · GRANULAR) 는 이 논문의 인용이 아니다 (문제 없음).

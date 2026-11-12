# batch 69 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `du2025_dem_fem_force_chain_collector_damage_calendering` — H. Du, Y. Zhang, X. Du, K. Yang, L. Zhao, "Force chain-induced collector damage in calendering: A DEM-FEM study", *Journal of Energy Storage* **138** (2025) **118688** · DOI 10.1016/j.est.2025.118688 (후보 표 N-27 · 고른 의도 = d · h · he2026 L689 · L99).
NMC532 : CB : PVDF = 90 : 5 : 5 액체계 LIB 양극의 롤 압연 (압하율 10–40 %) 을 평판 근사 EEPA DEM (단단한 구 · 3D RVE 100 µm) 으로 누르고 접촉력을 한 방향으로 Al 박 FEM 에 넘겨 집전체 응력 · 박힘을 계산한 논문 — SE 없음.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (SE 없음 · LIB 양극).  곁 정보: 실험 기공 연산자 = 질량 몫 · 진밀도로 고체 부피 ÷ 면적 질량 · 두께로 기하 부피 (*"the ratio of solid volume to the coating's geometric volume [79]"* p.7) · 어느 진밀도를 썼는지 미기재 (p.3 NMC 2.42 ↔ 표 1 4750) · 상태 = 압연 뒤 (카드 §3-5).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 (전극 되돌아옴 값 없음 · DEM 탈압 단계 서술 없음).  곁 정보:
- [b] du2025_dem_fem_force_chain_collector_damage_calendering | 접촉 수준만 — EEPA λp 0.96 → k₂ = 25 k₁ · δp/δmax 0.96 → 접촉 겹침의 4 % 만 회복 (n = 1 가정) | 표 1 · 식 A.7 · 카드 §3-2 · §14 D17 | [인쇄] · [카드 산술] | 전극 두께 회복 아님 · n 값 미기재
- [b] du2025_… | 되돌아옴 원전은 이 논문이 인용한 정본 카드 둘 — [10] Diener 2022 (`diener2022_roll_gap_springback_calendering`) · [75] Giménez 2019 (`sangros2019_dem_calendering_lib_electrode` · 시뮬 ER 10.25 → 17 %) | 카드 §8 단계 6 · §7-3 | [다른 카드] | 이 논문 값 아님

## c — 항복 · 경도 · 크리프 값과 정의. 일축 항복 세기와 견줄 환산이 카드에 있는가
이 배치에 없음 (항복 · 경도 · 크리프 없음 · FEM Al 의 구성식 · 항복 응력 미기재).  곁 정보: 표 1 E · ν — AM 142 GPa · 0.25 · CB 0.45 GPa · 0.2 · Al 68.9 GPa · 0.33 · 강철 182 GPa · 0.3 (출처 [72] · [73] · [74]) · FEM 응력 = Mises (그림 10p · 11i 축) (카드 §3-2 · §3-4).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
- [d] du2025_dem_fem_force_chain_collector_damage_calendering | **상별 · 쌍 종류별 하중 몫 없음** — '강한 사슬 몫' 21.49 · 11.06 · 10.59 · 9.73 % (압하율 10–40 %) = 평균 힘을 넘는 (f > 1) 접촉의 **수** 몫 · 같은 그림 P(f) (식 8 · 분모 = 입자 수) 의 f 1.08–1.42 세 칸만 합 0.128 > 0.0973 → 재현 안 됨 | 그림 6i · 6k · 식 7 · 8 · p.9 · 카드 §3-6 · §7-2 | [인쇄] · [판독] · [카드 산술] | 무른 상 = CB (E 0.45 GPa · 5 wt% · AM 1 개당 ≈2.8) · SE 없음 · 하중 몫 정의 없음
- [d] du2025_… | 식 9 σ_ij = (1/2V)Σ(r₁ᵢF₁ⱼ + r₂ᵢF₂ⱼ) = Love–Weber / Christoffersen 대칭 두 입자 꼴 — 우리 f_AM (b) 상별 virial 과 같은 꼴이나 **계 전체만** 보고 · σzz 3.09 → 25.55 MPa = DEM 판 압력의 0.25 → 0.095 (40 %: 25.55 / 270.5) | 그림 6m · p.9 · 카드 §3-6 · §14 D10 | [판독] · [카드 산술] | σ 정의 · V 미기재 · 같은 꼴의 `zhang2026_xct_…` 은 σzz/판 ≈ 1.0 [다른 카드]
- [d] du2025_… | 재밍 정성: *"The particles close to the collector are restricted in movement, exhibiting almost no displacement due to the significant reduction of local porosity after compression, which limits their ability to rearrange. However, they still form part of the force chain structure by transmitting contact forces through static interparticle contacts."* | p.11 · 그림 7d–f | [인쇄] | 정량 없음

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안 (multi-contact · MDR · EEPA · Thornton-Ning · Storåkers). 대안마다 맞춘 값이 몇 개인가
- [e] du2025_dem_fem_force_chain_collector_damage_calendering | EEPA 를 *"large deformation"* 용으로 씀 (*"the Edinburgh Elasto-Plastic Adhesive contact model (EEPA) is used to reproduce the contact between the particles and the mechanical behaviors when undergoing large deformation [27,84,85]"*) — **범위 · 상한 없음** · λp 0.96 · γ AM–AM 8 · CB–CB 60 · AM–CB 20 J/m² · f₀ 10⁻⁵ N · μ 0.25 · μr 0.01 · COR 0.25 · **맞춘 값 0 개** (전부 문헌 · 조정 서술 없음) · 최대 입자–벽 겹침 0.847 µm ≈ D50 반지름의 0.24 | p.4 · 표 1 · 그림 9 · 카드 §3-2 · §3-3 · §14 D21 | [인쇄] · [카드 산술] | AM 단독 · 기공 ≥ 17 % (조밀 영역 아님) · 벽 접촉 · k · n 미기재
- [e] du2025_… | 판 압력–두께 맞춤 곡선 (DEM − 실험)/실험 = +4.9 · −6.5 · −17.7 · −41.7 % (60 · 70 · 80 · 90 µm) — 원문 '편차 3.66 % · 0.073 %' 는 정의 없음 (0.073 % = 두 곡선 교점 근처) | 그림 5c · p.6 · 카드 §3-5 | [판독] · [카드 산술] | 실험 압력 환산식 미기재
- [e] du2025_… | 부록 식 표기 결함: A.3 · A.4 분모 = 반지름 · A.6 둘째 가지 δᵖ · 점착 가지 지수 n (EEPA 원전은 X) · A.8 ϕ 정의 없음 (원전 ψ = 3/2) · λp 를 '탄성 대 소성 비' 로 설명 | p.16–17 · 카드 §3-3 | [인쇄] · [다른 카드 `morrissey2013_…` L31–L32] | —

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 (지름당 셀 수). 수치 오차를 어떻게 추정했나
이 배치에 없음 (MPM 없음).  곁 정보: DEM → FEM 계면 격자 3 µm = AM D50 지름당 2.4 칸 · D10 1.2 칸 · 계산 구멍 지름 2.90 µm < 한 칸 [카드 산술] — 수렴 시험 없음 (카드 §3-4 · §14 D22).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 (계산은 3D · 2D → 3D 말 없음).  곁 정보: 실험 구멍 = CLSM **2D 선 주사** (*"A line scan along the calendering direction was performed to obtain two-dimensional cross-sectional profiles"* p.11) · *"Fig. 8j-l represent typical values obtained from a single line scan, while the maximum pit depth and diameter were determined by comparing measurements across multiple line scans"* — 3D 계산 구멍과 2D 단면 측정을 견줌 (카드 §3-8).

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
- [h] du2025_dem_fem_force_chain_collector_damage_calendering | **한 방향 DEM → FEM**: EDEM 2021 접촉력 (법선 + 접선) · 좌표 → axdt 파일 → ANSYS 2022 Al 박 RVE 100 × 100 × 17 µm³ (C3D8R · 정적 · 바닥 고정) · *"A uniform interfacial mesh of 3 μm ensures one-to-one mapping between DEM contact points and FEM nodes"* · **넘긴 시점 = 압력 단계 (압하율 10 · 20 · 30 · 40 %) 마다 따로 돌린 DEM 의 누른 상태** (*"Separate DEM simulations are conducted for each pressure level"*) · DEM 의 집전체 = 단단한 stl | p.5–6 §3.2 · 그림 4 · 카드 §3-4 | [인쇄] | Al 구성식 미기재 · FEM 변형은 DEM 으로 안 돌아감
- [h] du2025_… | 넘김의 비용: '박힘' 이 DEM 입자–면 겹침 (≤ 0.847 µm · 그림 9) ↔ FEM 구멍 (≤ 1.84 µm · 그림 8n) 둘로 갈림 (2.18 배) · 실험 CLSM 구멍이 6 칸 중 5 칸 더 큼 (본문 *"simulated values … exceed the experimental values"* 와 반대) | 그림 8n–o · 9 · 카드 §3-8 · §14 D19 · D20 | [판독] · [카드 산술] | 측정 = 손 선 따기
- [h] du2025_… | 선례 둘 (원문 서론): [29] Song 2023 *"a DEM-FEM bidirectional coupled model to simulate particle embedding in the current collector"* · [49] Yang 2023 *"incorporated load distributions from DEM into a crystal plasticity finite element model (CPFEM)"* (집전체 결정립) — 둘 다 카드 없음 → n | p.2 · 카드 §8 후보 B · §12 | [인쇄] | —

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 (SE 없음).  곁 정보 (AM + CB + PVDF 액체계 양극 · 두께 목표 압연): 두께 90 · 80 · 70 · 60 µm ↔ DEM 판 압력 (맞춤) ≈12 · 58 · 140 · 270 MPa ↔ 기공 DEM 48.3 · 36.5 · 27.6 · 18.9 % · 실험 45.4 · 37.7 · 25.9 · 16.9 % (그림 5c · 5d [판독]) · 고체 보존 산술과 DEM −3.5 · −3.9 %p (20 · 30 %) · crude Heckel P_y 실험 ≈236 · DEM ≈285–333 MPa (섞인 상태) (카드 §3-5 · §14 D14 · D15) — 랩 표준 (순수 SE 10–13 % · 1.64 g/cm³) 과 다른 재료 · 같은 표에 넣지 않음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] du2025_dem_fem_force_chain_collector_damage_calendering | 저자 한계: *"Since the platen-based DEM model cannot capture the full dynamics of calendering, future research will focus on the effects of roller rotation on stress transfer and its relationship with the current collector's elongation properties."* · *"the lack of a quantifiable threshold for contact damage penetration into the current collector necessitates further investigation through mechanical testing"* · 집전체 거칠기 미반영 · 손 선 따기 편향 · CB 입도 고정 | p.16 · p.11 · p.13 · 카드 §3-11 | [인쇄] | —
- [j] du2025_… | 카드가 찾은 원문 안 어긋남 15 — 식 2 cos θ ↔ 서술 (A 최대 · B 0) · θ < 1° [75] ↔ 이 롤 1.62° (40 %) · 접촉 +76.5 ↔ +74.7 % · F′zz 감소를 '수직 정렬' 로 · 9.73 % ↔ P(f) · σ 정의 없음 (σzz ≈ 판 × 0.1) · 그림 7 캡션 10/20/30 ↔ 본문 20/30/40 % · 20 % 'smooth' ↔ 구멍 379 (그림 ≈443) · '계산 > 실험' ↔ 그림 · '평균' 깊이 1.43 · 1.86 = 한 줄의 가장 깊은 골 · 그림 8a–c strain ↔ Depth · 그림 11h 범례 · 11g 표준편차 짝 · 식 A.3/A.4/A.6/A.8 · 밀도 두 벌 · 참고문헌 중복 셋 | 카드 §3-11 | [카드 관찰] | 판정 아님
- [j] du2025_… | 원문에 없는 계산 조건 (카드 §13): 입자 수 · 시드 · 시간 간격 · 판 속도 · k₁ · k₂ · k_adh · n · 감쇠 · 벽 접촉 매개변수 · DEM 기공 연산자 · 상태 · FEM Al 구성식 | 카드 §13 | [미확인] | —

## k — DEM 의 한계
인용 서지: **Du, Zhang, Du, Yang, Zhao (2025), Journal of Energy Storage 138, 118688 (EEPA DEM + 한 방향 FEM · NMC532 액체계 양극).**
- [k] du2025_dem_fem_force_chain_collector_damage_calendering (Du · Zhang · Du · Yang · Zhao · 2025 · J. Energy Storage 138, 118688) | *"However, DEM has limitations in describing the macroscopic mechanical behavior of materials (e.g., stress distribution, continuum deformation of materials). To address this, the coupled method of DEM and finite element method (FEM) has gradually become an effective tool …"* | p.2 · `txt_p2_dem_limitation_and_song29_bidirectional.png` · 카드 §4-3 | [인쇄] | 수치 한계 없음
- [k] du2025_… (Du et al. 2025 · J. Energy Storage 138) | *"For porous electrodes, the DEM has limitations in obtaining the stress distribution of the current collector. Relying solely on the FEM faces challenges due to the difficulty in capturing the complex properties of the current collector."* | p.5–6 · 카드 §4-3 | [인쇄] | —
- [k] du2025_… (Du et al. 2025 · J. Energy Storage 138) | *"the simplified particle interactions and spherical morphology in the DEM model yield fewer compact contacts and simulated volume loss"* · *"This deviation may be attributed to the simplified particle-particle interactions in the DEM model."* | p.7 · p.6 · 카드 §3-5 | [인쇄] | 판독으로는 DEM 기공이 실험보다 낮은 칸도 있음 (20 %)
- [k] du2025_… (Du et al. 2025 · J. Energy Storage 138) | *"Since the platen-based DEM model cannot capture the full dynamics of calendering …"* · 평판 근사 근거 *"the maximum value of θ always remains less than 1° [75]"* — 이 논문 롤 (지름 200 mm) 에서는 40 % 에서 1.62° [카드 산술] | p.16 · p.4 · 카드 §3-4 | [인쇄] · [카드 산술] | —

## l — 소성변형이 왜 어려운가
- [l] du2025_dem_fem_force_chain_collector_damage_calendering (Du · Zhang · Du · Yang · Zhao · 2025 · J. Energy Storage 138, 118688) | 이유 = k 의 연속체 변형 · 구 형상 문장 · **우회 = 접촉 법칙의 소성 + 집전체만 연속체**: *"the EEPA model represents the deformation and elastic recovery of particles during the coating's loading and unloading processes through the plastic contact ratio (λp)"* (λp 0.96 · k₂ = 25 k₁) · 바인더 = *"indirectly represented by adjusting the surface energy parameter (γ) and the adhesion force (f0) in the contact model [27]"* · 집전체 = 한 방향 정적 FEM · **맞춘 값 0** (문헌 값) · 비용 = *"To reduce computational costs, a cubic representative volume element (RVE) with dimensions of 100 × 100 × 100 μm3 was constructed"* (입자 수 · 계산 시간 미기재) | p.4–5 · 카드 §4-3 (ii) | [인쇄] · [카드 산술] | 입자 형상 소성 · 다접촉 보정 · 항복 캡 없음 (EEPA = 캡 없는 이력 [다른 카드 `schreiner2020_…` L71])

## m — 받아들일 통찰
- [m] du2025_dem_fem_force_chain_collector_damage_calendering | **응력 텐서 자기 점검** — 접촉 합 Love–Weber σzz 를 판 압력과 견준다 (이 논문 0.095 = 실패 · 같은 꼴 `zhang2026_xct_…` ≈1.0) → 우리 DEM 침대마다 결과 전 점검 칸 (`stress_cv_lw` 계열 옆) | 후보 D0; 결과 전 대조 항목 | 카드 §3-6 · §14 D10
- [m] du2025_… | **힘 사슬 출력의 정의 넷을 결과 전에** — 강한 사슬 (f > 1) 의 수 몫과 하중 몫 둘 다 · P(f) 분모 = 접촉 · 직물 편차 부호 (⟨n_z²⟩ = 1/3 + F′zz) · 응력 정규화 부피 V → 우리 f_AM (a) · (b) 옆에 둘 때 '같은 이름 · 다른 양' 을 막는다 | 단계 0; 후보 D0 | 카드 §7-2
- [m] du2025_… | **함정 — 2 차 인용이 원문에 없는 값을 만든다**: he2026 이 이 논문 출처로 단 입자–Al 마찰 0.61 / 0.12 / 0.65 · JKR 1.5 J/m² 가 원문 표 1 에 없다 (입자–입자 8 줄뿐) → 문헌 매개변수 원장에 '원문 표 · 쪽 · 줄' 칸 · 벽 접촉 매개변수 등록 칸 | 후보 A′-0; 단계 0 | 카드 §0-1
- [m] du2025_… | **한 방향 넘김의 비용이 숫자로 남는다** — 변형이 돌아오지 않아 '박힘' 이 겹침 (0.847) ↔ 구멍 (1.84 µm) 으로 갈림 → [DEM 우선 (수영)] 방향 메모의 '후처리 ↔ 결합' 사례 | 흐름 밖: [DEM 우선 (수영)] 방향 메모 · 후보 A | 카드 §7-4 · §8

## n — 논문 에이전트 후보
- [n] Y. Song, K. Gao, C. He, Y. Wu, S. Yang, N. Li, et al., Exploring particle-current collector contact damage in Li-ion battery using DEM-FEM scheme, Appl. Energy 351 (2023) 121904, https://doi.org/10.1016/j.apenergy.2023.121904. | h · 후보 B — **양방향** DEM-FEM 입자 박힘 (이 논문의 직계 선행 · 카드 §8 후보 B · §12 [29]) | litdb 확인: papers/ ls `song2023*` 없음 · grep "apenergy.2023.121904" = `song2025_insitu_ct_…` 의 인용 줄뿐 → 카드 없음 (wishlist L107 에 이미 있음)
- [n] N.P. Kruyt, On weak and strong contact force networks in granular materials, Int. J. Solids Struct. 92–93 (2016) 135–140, https://doi.org/10.1016/j.ijsolstr.2016.02.039. | d — f = 1 강 · 약 망 문턱의 원전 · 강한 망이 지는 응력 몫의 정의 (이 논문은 수 몫만 · 카드 §3-6 · §12 [100]) | litdb 확인: `kruyt*` 없음 · grep "Kruyt" · "ijsolstr.2016.02.039" · "weak and strong contact" 0 건 → 카드 없음
- [n] A. Mazor, L. Orefice, A. Michrafy, A. De Ryck, J.G. Khinast, A combined DEM & FEM approach for modelling roll compaction process, Powder Technol. 337 (2018) 3–16, https://doi.org/10.1016/j.powtec.2017.04.053. | h · 후보 M0 — DEM + FEM 롤 압밀 (카드 §8 후보 M0 · §12 [78]) | litdb 확인: `mazor*` 없음 · grep "Mazor" · "powtec.2017.04.053" · "roll compaction" 0 건 → 카드 없음
- [n] J. Zhang, J. Sun, H. Huang, C. Ji, M. Yan, Z. Yuan, Deformation and fracture mechanisms in the calendering process of lithium-ion battery electrodes, Appl. Energy 373 (2024) 123900, https://doi.org/10.1016/j.apenergy.2024.123900. | h · R7 — 도막 · 집전체 결합 모델 · 전극 파괴 에너지 (*"Zhang et al. [56] developed a coupled modeling framework for the coating and current collector"* p.2 · 카드 §12 [56]) | litdb 확인: `zhang2024*` 없음 · grep "apenergy.2024.123900" 0 건 → 카드 없음
- [n] R. Ge, D.J. Cumming, R.M. Smith, Discrete element method (DEM) analysis of lithium ion battery electrode structures from X-ray tomography-the effect of calendering conditions, Powder Technol. 403 (2022) 117366, https://doi.org/10.1016/j.powtec.2022.117366. | e — 입자–입자 μ 0.25 · μr 0.01 · COR 0.25 의 출처 (이 논문 표 1 · he2026 L92–L94 공통) · 힘 정규화 (식 4–5) (카드 §3-2 · §12 [25]) | litdb 확인: `ge2022*` 없음 · grep "powtec.2022.117366" 0 건 → 카드 없음

## 카드 문제
- `he2026_dem_calendering_inhomogeneity_areal_density` **L99 · L100** (가리킨 카드): 입자–Al 집전체 μ / 구름 / COR **0.61 / 0.12 / 0.65** 와 JKR 표면에너지 **1.5 J m⁻²** 를 *"[41] Du 2025"* 로 단 줄 — 이 논문 (Du 2025) 에 **없다**: 표 1 (p.5) 은 재료 넷의 ρ · E · ν + 입자–입자 8 줄뿐이고 입자–Al · 입자–강철 줄이 없으며, 19 쪽 글자 층에 "0.61" · "0.65" · "0.12" · "JKR" · "1.5 J" 0 건 · 접촉 법칙은 EEPA (JKR 아님).  he2026 원문 PDF 가 이 트리에 없어 he2026 의 [41] 이 정말 Du 2025 인지 · 값의 실제 출처는 [미확인].  고치지 않음.
- `he2026_…` **L98**: f₀ **1.5 × 10⁻⁵ N** *"[39–41]"* ↔ 이 논문 표 1 f₀ = **10⁻⁵ N** ([88] Schreiner 2023) — [41] 이 이 논문이면 값이 다르다.  고치지 않음.
- `he2026_…` **L368 · L689** (N5): *"진짜 force-chain 정량 논문 · 우리 AM-AM 하중분담과 비교 가능한 유일 후보"* — 원문의 힘 사슬 정량은 접촉 쌍 수 · 직물 편차 · P(f) · 강한 사슬 **수** 몫 (21.49 → 9.73 %) 이고 **상별 · 쌍 종류별 하중 몫은 없다** (식 9 는 상별로 나눌 수 있는 꼴이지만 전체만 보고) → '비교 가능' 은 원문으로 서지 않는다.  서지 (*J. Energy Storage* 138, 118688 · 제목) 는 맞다 (제목 *"A DEM-FEM study"* 대소문자만).  고치지 않음.
- (관찰 · 카드 문제 아님) `he2026_…` L92–L96: 입자–입자 μ 0.25 · COR 0.25 · 8 J/m² · λp 0.96 의 출처를 [39] Ge 2022 · [40] 로 · 구름 0.014 — 이 논문 표 1 은 같은 값 넷을 [25] Ge 2022 · [86] · [27] 로, 구름은 0.01 로 적는다 (he2026 원문 확인 불가) · L80–L83 he2026 표 1 의 SP 줄 (2250 · 0.45 · 0.20) · AL · Steel 밀도 · ν 는 이 논문 표 1 과 같은 수 (NCM 밀도 4570 ↔ 4750 · E 47 ↔ 142 · 70 ↔ 68.9 · 200 ↔ 182 만 다름).
- (참고 · 원문끼리) 이 논문 표 1 의 AM–AM 표면 에너지 8 J/m² 의 출처 [86] = Schreiner 2020 인데 그 정본 카드 (`schreiner2020_dem_calendering_lib` L42) 의 값은 NMC–NMC **5** J/m² (PVDF–NMC 20 · PVDF–PVDF 60 은 이 논문의 AM–CB 20 · CB–CB 60 과 같은 수 · 이 논문은 [87] 로 인용) — 카드는 고치지 않음.
- (참고 · 카드 아님) 후보 표 `litdb/_curation/S8_candidates.md` N-27 서지 = 저자 성만 (*"Du 2025"*) · 제목 *"… a DEM-FEM study"* — 원문 저자 다섯 (He Du · Yuxin Zhang · Xiaozhong Du · Kaiyue Yang · Le Zhao) · 제목 *"A DEM-FEM study"* (대소문자만) · 권 · 논문 번호 · 연도 · DOI 같음.
- (참고 · 카드 아님) `litdb/figures/_sources.json`: 이 배치의 `extract_figures.py` 가 다른 카드 줄 셋 (choi2018 `figures` 8 → 32 · devasconcelos2019 `pdfs` 목록을 다시 씀 · heenan2020 `figures` 16 → 39) 을 바꿨으나 HEAD 값으로 되돌리고 이 카드 줄만 더했다 (batch_58 · batch_62 · batch_67 와 같은 현상).

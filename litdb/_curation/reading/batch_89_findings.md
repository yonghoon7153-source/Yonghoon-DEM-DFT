# batch 89 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `morenoatanasio2007_contact_stiffness_surface_energy_fluidization_cohesive_dem` — R. Moreno-Atanasio, B.H. Xu, M. Ghadiri, "Computer simulation of the effect of contact stiffness and adhesion on the fluidization behaviour of powders", *Chemical Engineering Science* 62 (2007) 184–194 · DOI 10.1016/j.ces.2006.08.036 (후보 표 N-49 · 가리킨 카드 = `roessler2019_dem_cohesive_aor_cylinder_lift_calibration` L238).
CFD-DEM (CCDM) 으로 98 µm 모의 입자 45,000 개 (의사 3D 단층) 를 중력 침강 → 기체 유동화시키며 선형 접촉 스프링 κ (50 · 50,000 N/m) × 표면 에너지 γ (0.37 · 3.7 mJ/m²) 2 × 2 를 견준 계산 논문 — 실험 · 압밀 · 소성 · 탈압 없음.
쪽 = 인쇄 p.184–194 (PDF 쪽 N = 인쇄 183 + N) · SI 없음 · 판독 원자료 = `litdb/figures/morenoatanasio2007_contact_stiffness_surface_energy_fluidization_cohesive_dem/digitized.csv` (955 행 · 벡터 그림 9 장 + 래스터 그림 2 · 방법은 note 칸).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (SE · 압력 축 · 진밀도 없음 — 있는 것은 중력 침강 충전율 0.507–0.55 (의사 3D · 모의 입자 · 표 3) 뿐 · 같은 침대에 연산자별 숫자 셋 (인쇄 · 3D 두께 재계산 0.528–0.566 · 2D 면적 1.5 배) [카드 §3-7] · 랩 표준 (순수 SE 10–13 % · 1.64 g/cm³) 과 다른 물질 · 다른 하중의 값).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 (압축 하중 · 탈압 없음 · 반발 계수 0.97 (표 1) 만).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 (항복 · 경도 값 없음 — *"hardness of particle materials"* 는 vdW 추정을 어렵게 하는 요인으로만 언급 · p.185).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (단일 물질 · 단분산).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] morenoatanasio2007_… | 선형 스프링 (Cundall–Strack) 을 쓴 이유 = 비용: *"more complicated contact laws need longer time to simulate, which is especially true when large numbers of particles are present in the system"* · 대안으로 Kafui et al. (2002) 탄소성 접촉 · Di Renzo & Di Maio (2004) 의 *"linear and non-linear models start to deviate"* 를 인용만 | 카드 §4-4 (ii) · p.185 | 인쇄 | 맞춘 값 0 (κ 두 값 = *"to cover the range of values found in the literature"* p.186 · 실험 없음) · 큰 변형 범위의 말 없음
- [e] morenoatanasio2007_… | 선형 모델의 결과: 침강 중 힘이 κ 큰 쪽에서 *"three orders of magnitude larger … a consequence of the linear model used, where the interparticle contact force is proportional to the particle stiffness"* — 판독 봉우리 비는 107–116 배 | 카드 §3-2 · p.187 · Fig. 2 | 인쇄 · 판독 | 98 µm · 중력 · 동적

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 없음 · 기체 격자 1 mm × 1 mm 의 해상도 시험도 없음).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] morenoatanasio2007_… | 의사 3D: *"To account for the discrepancy in porosity calculations between 2D and 3D, the concept of pseudo-3D (Xu and Yu, 1997) is used in the present work so that ΔV = 2ΔxΔyR_i"* · 층 두께 = 입자 지름 (표 1) · 과립 온도 θ = (2θ_x + θ_Y)/3 — *"performed in two dimensions"* 라 수평 성분을 2 배로 셈 (식 20) | 카드 §4-3 · §4-4 (iii) · p.186 · p.189 | 인쇄 · [카드 해석] 세 번째 성분 = 수평과 같다고 둠 | 2D → 3D 결과 전이에 대한 말 없음 · 같은 침대 충전율이 2D 면적이면 1.5 배 [카드 산술]

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] morenoatanasio2007_… | *"the effect of elastic and plastic particle properties has not adequately accounted for"* · 지도 경계는 *"needs to be better specified"* | 카드 §4-4 (i) · §3-6 · p.192 | 인쇄 | 유동화 문맥 (압밀 아님)
- [j] morenoatanasio2007_… | 실제 분말의 vdW 는 *"surface geometry of contacting particles, local deformation of contact areas, hardness of particle materials and gas adsorption onto particle surfaces"* 때문에 *"difficult to quantify"* | 카드 §4-4 (i) · p.185 | 인쇄 | 점착 크기 지정의 한계 (γ 하나로 대리)

## k — DEM 의 한계
(인용 서지 = Moreno-Atanasio, R., Xu, B.H., Ghadiri, M. (2007). Chemical Engineering Science 62, 184–194.)
- [k] morenoatanasio2007_… (Moreno-Atanasio · Xu · Ghadiri 2007 · Chem. Eng. Sci.) | *"Previous applications of CCDM to the analysis of cohesive powders have been focused mainly on coarse particles due to the limitation of computing power."* | p.184 · `txt_p1_intro_coarse_particles_computing_power.png` | 인쇄 | 계산 비용 한계
- [k] morenoatanasio2007_… (같은 서지) | *"This is a consequence of the linear model used, where the interparticle contact force is proportional to the particle stiffness."* | p.187 · `txt_p4_settling_force_deformation.png` | 인쇄 | 선형 모델의 인공물 · 크기는 판독과 어긋남 (세 자릿수 ↔ 두 자릿수)
- [k] morenoatanasio2007_… (같은 서지) | *"the contact stiffness could influence the behaviour of systems in which particles are subjected to breakage"* | p.189 · `txt_p6_low_cohesivity_conclusion_breakage.png` | 인쇄 | 파괴 판정의 힘이 강성에 묶인다는 경고 (계산은 없음)
- [k] morenoatanasio2007_… (같은 서지) | ★ 강성 × 점착: 같은 떼는 힘 (F_OFF = 3πγR* 0.854 µN [카드 산술]) 에서 κ 50 ↔ 50,000 이 점착 침대의 유동화 여부를 가름 · *"When the surface energy has the value of 3.7 mJ/m2 and for low contact stiffness (system C) the particles are lifted as a block and fluidization is never achieved."* | p.191 · 카드 §0 · §3-5 | 인쇄 · 판독 | 연화 강성 (보정 · 속도 손잡이) 이 점착 거동을 바꾼다는 직접 사례 · 유동화 · 98 µm
- [k] morenoatanasio2007_… (같은 서지) | *"The effect of contact stiffness, representing the elastic deformation, has been widely ignored in the literature due to the experimental difficulty of varying it."* | p.192 · `txt_p9_mechanism_deformation_energy_ignored.png` | 인쇄 | —
- [k] 말 없음: 단단한 구 · 점접촉 · 겹침 상한 · 조밀 영역 과강성 · 보정값이 물성이 아니라는 고백 — 원문 전수에 없음 (카드 §4-4).

## l — 소성변형이 왜 어려운가
- [l] morenoatanasio2007_… (Moreno-Atanasio · Xu · Ghadiri 2007 · Chem. Eng. Sci.) | 소성 · 형상 변화 계산 없음 · 이유 = 비용 (*"more complicated contact laws need longer time to simulate"* p.185) · 탄소성 접촉 선례 Kafui et al. (2002) 는 인용만 · 우회 = 선형 탄성 스프링 + 감쇠 + z_min 에서 멈춘 vdW (γ 로 지정 · 식 6–8) · 결론 *"so far the effect of elastic and plastic particle properties has not adequately accounted for"* (p.192) | 카드 §4-4 (ii) · p.185 · p.192 | 인쇄 | 맞춘 값 0 · 검증 0 (실험 없음) · 비용 = 입자 45,000 · 계별 ≈1 s · CPU 시간 [미확인] · Δt [미확인] (κ 50,000 접촉 시간 3.56 × 10⁻⁷ s [카드 산술])

## m — 받아들일 통찰
- [m] morenoatanasio2007_… | **떼는 힘 (F₀) 보존 ≠ 거동 보존** — 같은 F_OFF 에서 결과가 갈렸다 → 믹서 E 재척도 (×20 · ×40 · F₀ 쌍별 보존) 의 결과 전 대조 항목에 쌍별 분리 일 W_sep = (81/80)π⁵CED⁵R*³/E*⁴ (F₀ 보존 아래 ∝ E*^{−2/3} → ÷7.37 · ÷11.7 [우리 산술]) 과 평형 겹침을 Bo 와 나란히 · 떼는 힘 ↔ 분리 에너지는 함께 지킬 수 없다 (N-48 `haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem` = 분리 에너지 일정 규칙 · 이 논문 = 떼는 힘 일정의 반례 → 우리 F₀ 보존은 이 논문 쪽) | 흐름 밖: 믹서 점착 (후보 D0) | 카드 §7-2 · p.190–192
- [m] morenoatanasio2007_… | **정적 평균 힘은 하중 균형, 동적 힘은 강성** — 표 3 네 층의 평균 힘 *"within the same order of magnitudes"* (p.187) · 끝 변형은 κ 비만큼 (≈1,170 · 1,300 배 [판독]) · 유동 중 힘 ≈117 배 [판독] → 연화 DEM 의 파괴 판정 (Auerbach) 은 준정적 하중 균형 힘으로, 충돌 봉우리는 연화에 묶인다고 적는다 | R7 · 후보 D0 | 카드 §3-2 · §3-4 · §8
- [m] morenoatanasio2007_… | **겹침 문턱은 점착을 지키지 못한다** — 네 계 모두 끝 평균 변형 ÷ R < 0.1 % (Lommen 문턱 0.3 % 아래) 인데 γ 3.7 에서 C ↔ D 가 갈림 → 연화 무해 판정에 점착 도달 거리 (z_min) 와 평형 겹침 δ_eq = F_OFF/κ 의 비를 따로 등록 | 후보 D0 · 단계 0 | 카드 §7-3
- [m] morenoatanasio2007_… | **육안이 같아도 숫자는 다르다** — *"Systems A and B look visually very similar although the quantitative analysis indicates differences in the average contact force and in the coordination number"* (p.191) → 접촉 표현 비교의 등록 관측량은 배위수 · 힘 분포 (스냅숏 아님) | 단계 3 | 카드 §8

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
litdb 확인 = 정본 `litdb/papers/` 파일 목록 (`git ls-tree` · 이 커밋 전 원격 끝 `2f127b4fc` · 565 장) + `git grep` (제1 저자 성 · 제목 낱말 · 권쪽) — 아래 다섯 모두 자기 카드 없음 · `_curation/wishlist.md` · 후보 표에도 없음.
- [n] Xu, B.H., Yu, A.B., Zulli, P., 2001. The effect of interparticle forces on powder fluidization behaviour. In: Kishino, Y. (Ed.), Powders and Grains. AA Balkema Publishers, Rotterdam, pp. 577–580. (원문 참고문헌 그대로) | k · m — 낮은 κ (50 N/m) 의 '문헌 범위' 근거 (p.186) · γ 9 mJ/m² · H 5.2 × 10⁻¹⁹ Nm 로 C 와 같은 거동 (p.191) — 카드의 분리 일 산술이 z_min 을 이 값에서 빌렸다 (카드 §3-7) · 굴림 마찰 식 10 의 출처 | litdb 확인: ls xu2001* 없음 · grep 'Zulli' · '577–580' 없음
- [n] Di Renzo, A., Di Maio, F.P., 2004. Comparison of contact-force models for the simulation of collisions in DEM-based granular flow codes. Chemical Engineering Science 59, 525–541. (원문 참고문헌 그대로) | e · U5 — 선형 ↔ 비선형 접촉 모델의 충돌 힘 이력 차 (p.185 인용) · `paulick2015_elastic_…` L656 · L660 이 [62] 로 표 5 를 옮겨 둠 (자기 카드 없음) | litdb 확인: ls direnzo* · renzo* 없음 · grep 'Di Renzo' = 인용만 (paulick2015 · shi2019)
- [n] Kafui, K.D., Thornton, C., Adams, M.J., 2002. Discrete particle-continuum fluid modelling of gas–solid fluidized beds. Chemical Engineering Science 57, 2395–2410. (원문 참고문헌 그대로) | e · l · 후보 C′ — CFD-DEM 에 탄소성 (점착) 접촉을 넣은 선례 (p.185) · `thorntonning1998_adhesive_elastoplastic_contact` 의 다수 입자 적용 | litdb 확인: ls kafui* 없음 · grep 'Kafui' 없음
- [n] Xu, B.H., Yu, A.B., 1997. Numerical simulation of the gas–solid flow in a fluidized bed by combining discrete particle method with computational fluid dynamics. Chemical Engineering Science 52, 2785–2809. (원문 참고문헌 그대로) | g · k — CCDM 원전 · 의사 3D 기공 (ΔV = 2ΔxΔyR) · 실제 접촉 시간 Δt_c (식 5) 정의 · 이 카드의 [미확인] (Δt · 감쇠) 을 채울 수 있는 곳 | litdb 확인: ls xu1997* 없음 · grep '2785' 없음
- [n] Tsuji, Y.T., Kawaguchi, T., Tanaka, T., 1993. Discrete particle simulation of two-dimensional fluidized bed. Powder Technology 77, 79–87. (원문 참고문헌 그대로) | k — 비점착 유동층의 낮춘 강성 선례 (κ 800 N/m · *"no large differences appeared in the behaviour of the systems when the contact stiffness was varied"* p.191) | litdb 확인: ls tsuji* 없음 · grep '79–87' 없음 · wishlist 의 Tsuji, Tanaka & Ishida (1992) 는 다른 논문

## 카드 문제
- `paulick2015_elastic_particle_properties_dem_review` **L408** (표 행 14 · 같은 원문 [63] · 고치지 않음): *"유동화 (점착 없을 때) · CFD–DEM · k 50 vs 50,000 N/m · 차이 없음"* — 원문의 약한 점착 계는 **γ 0.37 mJ/m² (0 아님 · F_OFF ≈ 무게의 6.8 배 [카드 산술])** 이고 비점착 입자 계산은 κ 50 침강 한 번 (Fig. 4) 뿐이라 강성 비교가 없다 · *"does not significantly influence the quality of fluidization"* (p.189) 는 질에 대한 말이고 정상 배위수 0.67 ↔ 0.004 · 평균 힘 *"about two orders of magnitude"* (p.189) 는 다르다 → '점착 없음' ✗ · '차이 없음' = 질에 한정 (리뷰 원문 p.73 의 표기는 이 카드가 보지 않음 [미확인]).
- 가리킨 카드 `roessler2019_dem_cohesive_aor_cylinder_lift_calibration` **L238**: 서지 (저자 셋 · 제목 · Chem. Eng. Sci. 62 · 184–194 · 2007) 는 원문 첫 쪽과 같다 — 호 *"(1–2)"* 는 PDF 에 인쇄되어 있지 않아 원문으로 확인 불가 (틀림 아님) · 그 줄의 '카드 없음' 은 이 카드로 낡았다 (고치지 않음).
- `paulick2015_elastic_…` L384 (행 13) · L679 · `paulick2015_particle_contact_stiffness_two_particle_method` L309 · L513 — 원문과 같다 (문제 없음).

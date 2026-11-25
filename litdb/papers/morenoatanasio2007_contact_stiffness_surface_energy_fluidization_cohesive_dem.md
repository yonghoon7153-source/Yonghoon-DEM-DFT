<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 후보 표 N-49 · 정독 89) 에서 꼭 뽑으라고 한 항목.
     본 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표) · lommen2014_dem_speedup_contact_stiffness_reduction_bulk_behavior.md (같은 묶음 N-47 · DEM 계산 논문의 3 · 4 절 꼴).
     원문 = 출판본 PDF (Chem. Eng. Sci. 62 (2007) 184–194 · 11 쪽).  쪽 표기 = 인쇄 쪽 p.184–194.  크롭 파일 이름의 pN 과 figures.json 의 page 는 PDF 쪽 (PDF p.N = 인쇄 p.183 + N).
     보충 자료 (SI) 없음 · 그림 13 · 표 3 · 번호 붙은 식 20 · 참고문헌 31.
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 955 행 — 그림 1 · 3 · 4 · 6 · 7 · 8 · 10 · 11 · 12 는 벡터 경로 (PyMuPDF get_drawings · 큰 눈금 최소제곱 맞춤 · 곡선 꼭짓점 · 표지 중심) · 그림 2 는 내장 래스터 (1032 × 804 px) 화소 (안쪽 눈금 표시로 로그 축 맞춤) · 방법은 csv 의 note 칸) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [우리 산술] = 우리 쪽 값과 견주는 계산 (원문에 없다) · [미확인] = 원문 11 쪽 전수에 없음.
     원문 11 쪽은 글자 층 추출 (블록 좌표) + 쪽 렌더로 전부 읽었다 (식 · 그리스 문자 · 위첨자 · µ 는 글자 층이 깨져 렌더에서 옮겼다).  계산 = CFD-DEM (CCDM) · 실험 없음. -->
# 점착 분말 CFD-DEM 에서 접촉 강성 선택이 점착 거동을 바꾸는가 — 선형 스프링 κ 50 ↔ 50,000 N/m × 표면 에너지 γ 0.37 ↔ 3.7 mJ/m² (d 98 µm · 45,000 입자 · 의사 3D 한 입자 두께): γ 0.37 은 κ 와 무관하게 0.2 s 안에 유동화 (그래도 정상 상태 배위수 0.67 ↔ 0.004 · 평균 힘 ≈117 배 [판독]) · γ 3.7 은 κ 50 이면 덩어리로 들려 채널만 뚫리고 유동화가 안 되며 κ 50,000 이면 덩어리가 부서져 유동화 (0.3 m/s · 배위수 3.59 → 0.35 [판독]) — 떼는 힘 F_OFF = 3πγR\* (0.854 µN [카드 산술]) 이 같은데 결과가 갈린다 · 저자 기전 = "무른 접촉일수록 변형이 커 떼는 데 에너지가 더 든다" — Moreno-Atanasio · Xu · Ghadiri (Chem. Eng. Sci. 2007)

> slug `morenoatanasio2007_contact_stiffness_surface_energy_fluidization_cohesive_dem` · DOI `10.1016/j.ces.2006.08.036` · type `CFD-DEM (CCDM = combined continuum and discrete model, Xu & Yu 1997 · pseudo-3D bed one particle thick · linear spring–dashpot contact (Cundall–Strack) + Coulomb sliding + rolling friction · van der Waals attraction capped at z_min, parameterized by surface energy via the JKR pull-off force · modified Di Felice drag · SIMPLE finite-volume gas · 2 contact stiffnesses x 2 surface energies (systems A–D) · gravity settling then gas at 0.1 / 0.3 m/s — no experiments)` · PDF `dacdd31a-49._Computer_simulation_of_the_effect_of_contact_stiffness_and_adhesion_on_the_fluidization_behaviour_of_powders.pdf` · SI 없음 · digested `2026-11-12` · status ✅
>
> **저자**: R. Moreno-Atanasio · B.H. Xu · **M. Ghadiri\*** — Institute of Particle Science and Engineering, University of Leeds (Leeds LS2 9JT, UK) — \* 교신 · *Chemical Engineering Science* **62** (2007) **184–194** · *"Available online 26 August 2006"* (접수 · 수정 · 수락 날짜는 인쇄 없음) · © 2006 Elsevier Ltd. · 키워드 *Fluidization · Powders · Multiphase flow · Cohesion · Computer simulation · DEM* · 지원 = Nexia Solutions [인쇄 p.193 감사].
> **이웃 카드 (링크만)**: [`roessler2019_dem_cohesive_aor_cylinder_lift_calibration`](roessler2019_dem_cohesive_aor_cylinder_lift_calibration.md) (참고문헌 L238 = 이 논문 · 가리킨 카드) · [`paulick2015_elastic_particle_properties_dem_review`](paulick2015_elastic_particle_properties_dem_review.md) (ref [63] = 이 논문 · 표 행 13 L384 · 행 14 L408 · L679) · [`paulick2015_particle_contact_stiffness_two_particle_method`](paulick2015_particle_contact_stiffness_two_particle_method.md) (ref [40] = 이 논문 · L309 · L513) · [`lommen2014_dem_speedup_contact_stiffness_reduction_bulk_behavior`](lommen2014_dem_speedup_contact_stiffness_reduction_bulk_behavior.md) (같은 묶음 N-47 · 비점착 연화의 겹침 문턱) · [`haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem`](haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem.md) (같은 묶음 N-48 · 연화하면 분리 에너지를 지키는 JKR 재척도 γ_mod = γ(E_mod/E)^{2/5} · SJKR 분리 에너지 L212) · [`johnson1971_jkr_surface_energy_contact_elastic_solids`](johnson1971_jkr_surface_energy_contact_elastic_solids.md) (식 7 의 원전 · 우리 SJKR 대응식 §7-1) · [`thorntonning1998_adhesive_elastoplastic_contact`](thorntonning1998_adhesive_elastoplastic_contact.md) (점착 탄소성 접촉 = 후보 C′) · [`luding2008_cohesive_frictional_contact_models`](luding2008_cohesive_frictional_contact_models.md) · [`alizadeh2018_dem_adhesion_calibration_segregation_heap`](alizadeh2018_dem_adhesion_calibration_segregation_heap.md) (N-48 Hærvig 2017 서지 L265).
> **판독 원자료**: `litdb/figures/morenoatanasio2007_contact_stiffness_surface_energy_fluidization_cohesive_dem/digitized.csv` (955 행 — Fig. 1 53 · Fig. 2a–2d 48 · Fig. 3 187 · Fig. 4 137 · Fig. 6 46 · Fig. 7 46 · Fig. 8 105 · Fig. 10 106 · Fig. 11 93 · Fig. 12a 48 · Fig. 12b 86 · 스냅숏 그림 5 · 9 와 정성 지도 그림 13 은 판독 없음) · 크롭 **63 장** (그림 · 표 22 = 도구 15 (다시 자름 5 = 그림 2 · 그림 9 · 표 1 · 2 · 3 · 캡션 고침 10) + 손 7 (그림 5 · 패널 2a–2d · 12a · 12b) · 식 21 · 근거 문단 20) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 같은 입자 (d 98 µm · ρ 2600 kg/m³ · 45,000 개) 에 **선형 스프링 강성 κ 를 50 과 50,000 N/m (1000 배)** 로, **표면 에너지 γ 를 0.37 과 3.7 mJ/m²** 로 준 네 계 (A–D) 를 CFD-DEM 으로 중력 침강 → 기체 유동화시킨 결과, **γ 0.37 에서는 강성이 유동화의 질을 바꾸지 않았지만 (A · B 모두 0.2 s 안에 유동화), γ 3.7 에서는 κ 50 (C) 이 덩어리로 들려 채널만 뚫고 끝내 유동화되지 않았고 κ 50,000 (D) 은 덩어리가 부서져 유동화됐다** — 저자 결론 *"the more cohesive the powder is, the larger are the differences in the behaviour of systems with different contact stiffnesses"* (p.184 초록).
**떼는 힘 F_OFF = 3πγR\* (식 7) 는 κ 와 무관하게 같다** — 같은 떼는 힘에서 결과가 갈린 것이 이 논문의 핵심이고, 우리 믹서의 *"떼는 힘 (F₀) 을 지키며 강성을 바꾸는"* 규칙이 거동을 지킨다는 보증이 될 수 없다는 근거다 (§7-2).

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 무엇을 계산했나 | **CCDM** (Xu & Yu 1997): 입자 = DEM (식 1–10 · **선형 스프링–감쇠 (Cundall–Strack) · Coulomb 미끄럼 μ_s 0.3 · 굴림 마찰 · 반발 계수 0.97**) + 기체 = 국소 평균 Navier–Stokes (식 16–19 · SIMPLE · 엇갈린 격자 1 mm × 1 mm) · **점착 = van der Waals 힘 HR\*/(6z²) (식 6) 을 접촉 중에는 z_min 에서 멈춤 · 크기는 γ 로 지정 (γ = H/(18πz_min²) · 식 8)** · 의사 3D (층 두께 = 입자 지름 98 µm · ΔV = 2ΔxΔyR) · 층 25 mm × 45 mm · 네 계 = κ {50 · 50,000} × γ {0.37 · 3.7} (표 1 · 2) · 무작위 배치 → 중력 침강 → 기체 0.3 m/s (A · B) · 0.1 · 0.3 m/s (C · D) | [인쇄] p.185–187 · 표 1 · 2 |
| ② ★ 강성 × 점착 연동 (의도의 중심) | **γ 3.7**: C (κ 50) = *"the particles are lifted as a block and fluidization is never achieved"* (p.191) · 0.3 m/s 배위수 2.92 → 2.52 (−14 % [판독] · 본문 *"about 15%"*) · D (κ 50,000) = 덩어리 → 무리 이탈 → 유동화 · 0.3 m/s 배위수 3.59 → **0.35 (−90 %)** · 0.1 m/s 3.77 → 2.43 (−36 %) [판독 Fig. 10] / **γ 0.37**: *"does not significantly influence the quality of fluidization"* (p.189) — 그러나 정상 상태 배위수 A 0.67 ↔ B 0.004 (Fig. 6) · 평균 힘 A 0.37 ↔ B 43 µN (기하평균 · ≈117 배 · Fig. 7) [판독] | [인쇄] p.189–192 · [판독] |
| ③ ★ 침강 (packed bed) | 배위수 끝값 A 3.07 · B 3.57 · C 2.92 · D 3.90 [판독 Fig. 1] · 충전율 0.537 · 0.538 · **0.507** · 0.55 · 층 높이 16.8 · 16.32 · **17.15** · 16.00 mm · 평균 압축력 2.00 · 1.65 · 1.22 · 0.97 µN · 접촉 수 76,719 · 89,216 · 72,913 · 94,971 [인쇄 표 3] · 침강 중 힘은 κ 큰 쪽이 *"three orders of magnitude larger"* (p.187 · 판독은 봉우리 ≈107–116 배) · 끝 변형 A 0.040 ↔ B 3.4 × 10⁻⁵ µm (≈1,170 배) [판독 Fig. 2] | [인쇄] p.187–188 · [판독] |
| ④ ★ 저자 기전 | *"likely to be due to the larger deformation of particles with lower stiffness in the packed bed state … need more energy to break the interparticle contacts"* (p.192) — 카드 산술: 평형 겹침 δ_eq = F_OFF/κ = **17.1 nm (C) ↔ 0.017 nm (D)** · 분리 일 ≈ F_OFF²/(2κ) + F_OFF·z_min → C/D ≈ **9.4 배** (z_min ≈ 1.0 nm 가정 — 이 논문에 z_min 값 없음) | [인쇄] p.192 · [카드 산술] §3-7 |
| ⑤ ★ DEM 한계 문장 (k) | 여러 곳 (§4-4) — 선형 모델이라 힘이 강성에 비례 (p.187) · 복잡한 접촉 법칙은 계산 시간 (p.185) · 실제 분말의 vdW 추정은 표면 기하 · 접촉 국소 변형 · 경도 · 기체 흡착 때문에 *"difficult to quantify"* (p.185) · 거친 입자만 다뤄 온 이유 = 계산 능력 (p.184) · 강성 · *"elastic and plastic particle properties"* 는 문헌에서 *"not adequately accounted for"* (p.192) | [인쇄] |
| ⑥ ★ 소성 · 큰 변형 (l) | **계산에 없음** — 접촉 = 선형 탄성 + 감쇠 · 소성은 *"Kafui et al. (2002) … elasto-plastic contact"* 를 인용만 하고 쓰지 않은 이유 = *"more complicated contact laws need longer time to simulate"* (p.185) · 결론에서 소성 물성은 *"not adequately accounted for"* (p.192) 한 줄 | [인쇄] |
| ⑦ ★ 2D / 3D | **의사 3D (pseudo-3D)** = 한 입자 두께 층 (표 1 bed thickness 9.8 × 10⁻⁵ m) · 기공률만 3D 꼴로 (ΔV = 2ΔxΔyR · p.186) · 과립 온도는 *"performed in two dimensions"* 라 수평 성분을 2 배로 셈 (식 20 · p.189) · 2D → 3D 전이에 대한 말 없음 | [인쇄] |
| ⑧ ★ 탈압 | **다루지 않음** — 압축 하중이 없다 (중력 침강 · 기체 항력).  가장 가까운 것 = 기체가 점착 층을 들어 올릴 때 덩어리 (C) ↔ 해체 (D) | 원문 전수 |
| ⑨ 절대값 전이 | **안 된다** — 재료 이름 없는 모의 입자 (98 µm · 2600 kg/m³) · 선형 스프링 (κ 는 물성이 아님 — 같은 겹침에서 Hertz 할선 E\* 로 바꾸면 A · C ≈ 38–46 MPa · B · D ≈ 1.3–1.7 TPa [카드 산술 §3-7]) · 하중 = 중력 (층 바닥 ≈0.23 kPa [카드 산술]) ↔ 우리 300 MPa (1.3 × 10⁶ 배) · 유동화 (기체) · 단층 · 계별 1 회 계산.  옮길 것 = **규칙과 경고** (떼는 힘 보존 ≠ 거동 보존 · 분리 일 · 정적 힘은 하중 균형으로 정해지고 동적 힘은 강성을 따른다) 뿐 | §7 |

⛔ **한정어 (떼지 말 것)**: ① 결과는 **유동화 (기체 항력)** 의 질 — 압밀 · 믹싱 결과가 아니다 ② **2 × 2 네 점 · 계별 한 번** (반복 · 시드 산포 없음 [미확인]) — 결과 지도 (그림 13) 는 *"Qualitative map"* 이고 경계는 *"needs to be better specified"* (p.192) ③ γ 0.37 의 *"강성 무영향"* 은 **유동화의 질 (육안 · 과립 온도)** 에 대한 말 — 배위수 · 힘은 크게 다르다 ④ 저자 기전 (변형 에너지) 은 *"likely"* (가설) — 카드의 분리 일 산술은 z_min 을 이 논문 밖 (Xu 2001 값) 에서 빌렸다 ⑤ 힘의 계 순서가 표 3 · 그림 2 ↔ 그림 3 · 4 에서 반대다 (§3-8 ③ — 어느 쪽이 맞는지 [미확인]) ⑥ 시간 간격 · 감쇠 계수 η · 굴림 마찰 μ_r · z_min · H · 계산 시간은 [미확인].

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-49 의 '왜' 칸)

의도 원문: *"k (근거 약함) — "강성 · 점착 연동 — 카드 없음" → 강성 선택이 점착 거동에 미치는 영향 (N-47 · N-48 과 같은 부류 (종합 · 조수 판단))"* (가리킨 카드 = `roessler2019_dem_cohesive_aor_cylinder_lift_calibration` L238)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "강성 · 점착 연동" | **채움** | 실험 설계 자체가 2 × 2 (κ 50 · 50,000 N/m × γ 0.37 · 3.7 mJ/m² · 표 2 · p.186–187) · 결론 *"a combined influence of surface energy and contact stiffness"* (p.192 · 결론 p.192) · 정성 지도 그림 13 (강성 ↑ · 표면 에너지 ↓ = 좋은 유동화 · D 는 전이선 위) · 조건 = 98 µm · 중력 + 기체 (U/U_mf 5.9 · 17.6 [카드 산술]) · 온도 · 압력 개념 없음 · 누른 채 / 뺀 뒤 해당 없음 |
| "강성 선택이 점착 거동에 미치는 영향" | **채움** | γ 3.7: C (κ 50) 덩어리 · 채널 · *"fluidization is never achieved"* (p.191) ↔ D (κ 50,000) 덩어리 붕괴 → 유동화 (p.190 · Fig. 9) · 배위수 0.3 m/s: C 2.92 → 2.52 · D 3.59 → 0.35 [판독 Fig. 10] · 과립 온도 0.3 m/s 뒤쪽 평균 D 123 ↔ C 48 cm²/s² [판독 Fig. 12b] · 침강 충전율 C 0.507 (가장 낮음 · p.187 표 3) / γ 0.37: 질 같음 (p.189) · 배위수 · 힘은 다름 (Fig. 6 · 7) |
| "k" (DEM 한계를 문헌으로 말하기) | **일부** | 한계 문장은 있다 — 선형 모델 (힘 ∝ 강성 · p.187) · 접촉 법칙 비용 (p.185) · vdW 추정 어려움 (p.185) · 계산 능력 (p.184) · 탄성 · 소성 물성 미반영 (p.192) (§4-4 전문).  그러나 **단단한 구 · 점접촉의 한계 (겹침 상한 · 입자 모양 · 조밀 영역)** 에 대한 문장은 없다 |
| "(근거 약함)" — 후보 표 자기 표지 | **원문이 직접 다룬다** (근거 약함 아님) · 단 **얇다** | 이 논문의 주제가 바로 강성 × 점착이다 (p.185 *"a feature which has not been yet reported in the literature"*).  얇은 점: 네 점 · 계별 1 회 · 시간 간격 · 감쇠 미기재 · 기전은 *"likely"* |
| "N-47 · N-48 과 같은 부류" | **일부** | N-47 (Lommen 2014) = 비점착 · 계산 속도용 연화 · 겹침 문턱.  이 논문의 낮은 κ 는 **속도 목적이 아니라** *"chosen to cover the range of values found in the literature (Kaneko et al., 1999; Xu et al., 2001; Ye et al., 2005)"* (p.186) — 연화의 이유 · 시간 간격 이득은 말하지 않는다.  N-48 (`haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem` — 분리 에너지를 지키는 재척도 γ_mod = γ(E_mod/E)^{2/5} · 대가 = 떼는 힘 감소) 의 **물음 (연화하면 점착을 어떻게 고쳐야 하나) 을 낳는 관측** 은 주지만, **환산 규칙은 없다** (κ 를 바꾸며 γ 고정 = F_OFF 고정 · 이것이 거동을 지키지 못함을 보였을 뿐) — 두 카드를 겹치면 이 논문 = '떼는 힘을 지킨 반례' · N-48 = '분리 에너지를 지키는 규칙' [카드 해석 · §7-2] |
| (가리킨 카드의 서지) roessler2019 L238 | **채움** | *"Moreno-Atanasio, R., Xu, B. H., & Ghadiri, M. (2007). Computer simulation of the effect of contact stiffness and adhesion on the fluidization behaviour of powders. Chemical Engineering Science, 62(1–2), 184–194."* = 원문 첫 쪽 (저자 셋 · 제목 · 권 · 쪽 · 연도) 과 같다 · **호 '(1–2)' 는 PDF 에 인쇄되어 있지 않다** (머리글 = *"Chemical Engineering Science 62 (2007) 184–194"*) · 그 카드의 '카드 없음' 은 이 카드로 낡았다 (고치지 않음) |

**같은 원문을 2 차로 옮긴 카드 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `roessler2019_…` L238 | 서지 + "강성 · 점착 연동" | 같은 서지 (호만 인쇄 없음) · 같은 주제 | **채움** |
| `paulick2015_elastic_…` L384 (표 행 13) | "유동화 (점착 있을 때) · CFD–DEM, 표면에너지 0.37·3.7 mJ/m² · k_n 50 vs 50,000 N/m · 저강성+고점착 = **유동화 안 됨**; 고강성 = 층 부상 후 붕괴" | C: *"lifted as a block and fluidization is never achieved"* · D: *"initially lifted as a block, but the block is weak and collapses"* (p.191) ✓ | **채움** |
| `paulick2015_elastic_…` L408 (표 행 14) | "유동화 (**점착 없을 때**) · k 50 vs 50,000 N/m · **차이 없음**" | 원문의 '약한 점착' 계는 **γ 0.37 mJ/m² (0 이 아님 · F_OFF ≈ 무게의 6.8 배 [카드 산술])** · 비점착 입자 계산은 **침강 한 번 (κ 50 만 · Fig. 4)** 이라 강성 비교가 없다 · *"does not significantly influence the quality of fluidization"* (p.189) 는 **질** 에 대한 말이고 정상 배위수 0.67 ↔ 0.004 · 힘 ≈ 두 자릿수 (*"about two orders of magnitude"* p.189) 는 다르다 | **일부** (점착 없음 ✗ · 차이 없음 = 질에 한정) |
| `paulick2015_elastic_…` L679 | "[63] Moreno-Atanasio (점착 결합 시 강성이 유동화 여부를 가름)" | ✓ | **채움** |
| `paulick2015_particle_contact_…` L309 | ref [40] = *"a reduced contact stiffness … can influence the simulation result in an undesirable manner"* 의 근거 (유동층) | C ↔ D (p.190–192) ✓ | **채움** |
| `paulick2015_particle_contact_…` L513 | 서지 (호 62(1–2) · DOI 포함) + "낮춘 강성이 결과를 바꾼 예" | ✓ (호는 인쇄 없음) | **채움** |

⇒ **의도 대조 결과: 채움** (주 의도 = 강성 선택이 점착 거동을 바꾼다 — γ 3.7 에서 κ 가 유동화 여부를 가름 · p.190–192 · Fig. 9–12 · 표 3) — 단 **k 의 DEM 한계 문장은 선형 모델 · 비용 · vdW 추정 쪽만 (일부)** · **N-48 류 연화 환산 규칙 · 시간 간격 · 반복은 없음**.  2 차 인용 카드 가운데 `paulick2015_elastic_…` L408 한 줄이 '점착 없음 · 차이 없음' 으로 원문보다 넓다.

---

## 1. 한 줄 요약
CFD-DEM (Xu & Yu 의 CCDM) 으로 98 µm 입자 45,000 개를 한 입자 두께 층에 침강시킨 뒤 기체로 유동화하면서, 선형 접촉 스프링 κ (50 · 50,000 N/m) 와 표면 에너지 γ (0.37 · 3.7 mJ/m²) 의 2 × 2 를 바꿨다.
γ 가 작으면 κ 는 유동화의 질을 바꾸지 않았지만 (배위수 · 힘은 크게 다름), γ 가 크면 κ 50 은 덩어리째 들려 채널만 뚫리고 끝내 유동화되지 않았고 κ 50,000 은 덩어리가 부서져 유동화됐다 — 떼는 힘 (3πγR\*) 이 같은데도.
저자는 이를 "무른 접촉은 침대에서 더 크게 변형돼 떼는 데 에너지가 더 든다" 로 설명하고, 강성을 크기 · 밀도 · 점착과 나란히 유동화 분류의 변수로 넣자고 했다 (정성 지도 그림 13).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| R. Moreno-Atanasio · B.H. Xu · M. Ghadiri\* (Leeds, Institute of Particle Science and Engineering) | Chem. Eng. Sci. 62 (2007) 184–194 · 온라인 2006-08-26 · 키워드 *Fluidization · Powders · Multiphase flow · Cohesion · Computer simulation · DEM* | 10.1016/j.ces.2006.08.036 | 모의 입자 (재료 이름 없음 · d 9.8 × 10⁻⁵ m · ρ_p 2600 kg/m³ · 단분산) + 공기 꼴 기체 (μ 1.8 × 10⁻⁵ kg/m s · ρ 1.205 kg/m³) — 배터리 재료 없음 | CFD-DEM 파라미터 연구 (2 × 2) · 실험 없음 |

- **1저자 메모 · 후보 표와의 대조**: 후보 표 N-49 · roessler2019 L238 의 서지 (저자 · 제목 · Chemical Engineering Science, 62(1–2), 184–194 · 2007) — **같다**.  덧붙임 ① 호 *"(1–2)"* 는 PDF 머리글 · 첫 쪽 어디에도 **인쇄되어 있지 않다** (머리글 *"Chemical Engineering Science 62 (2007) 184–194"*) — 틀린 것은 아니고 원문으로 확인할 수 없다 [미확인] ② 접수 · 수정 · 수락 날짜가 없고 *"Available online 26 August 2006"* 뿐 ③ PDF 문서 정보 Title = DOI 문자열 · Author 빔 ④ 영국식 철자 *"behaviour"* (제목) ✓.
- **글의 꼴**: 1 서론 (p.184–185) → 2 CCDM (2.1 입자 · 식 1–10 · 2.2 기체 · 식 11–19 · 2.3 풀이 · 경계 · p.185–186) → 3 결과 (3.1 침강 · Fig. 1–4 · 표 1–3 · 3.2 유동화 · 3.2.1 A · B (Fig. 5–8 · 식 20) · 3.2.2 C · D (Fig. 9–12) · p.186–191) → 4 논의 (Fig. 13 · p.191–192) → 5 결론 (p.192) → 기호표 · 감사 · 참고문헌 31 (p.192–194).  그림 13 · 표 3 · 식 20 · SI 0.
- 같은 그룹 앞 연구: Xu, Yu, Zulli (2001) (κ 50 N/m · γ 9 mJ/m² 점착 유동화 — 이 논문의 C 와 같은 거동 · p.191) · Xu & Yu (1997 · 1998) (CCDM 원전) — 카드 없음 (§12).

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 매개변수 — 표 1 · 2 (p.187 · `tab_1.png` · `tab_2.png` · `txt_p3_stiffness_values_literature.png` · `txt_p4_settling_protocol_gas_velocities.png`)
| 항목 | 값 | 표지 |
|---|---|---|
| 입자 수 · 지름 · 밀도 | **45,000** (표 1 은 *"45.000"* 으로 인쇄 · 본문 *"45 000"*) · 9.8 × 10⁻⁵ m · 2600 kg/m³ | [인쇄] 표 1 · p.188 |
| 접촉 | 스프링 상수 **50 · 50,000 N/m** · 미끄럼 마찰 **0.3** · 반발 계수 **0.97** · 표면 에너지 **0.37 · 3.7 mJ/m²** | [인쇄] 표 1 |
| 기체 · 층 | 점도 1.8 × 10⁻⁵ kg/m s · 밀도 1.205 kg/m³ · 층 너비 2.5 × 10⁻² m · 층 높이 4.5 × 10⁻² m · **층 두께 9.8 × 10⁻⁵ m (= 입자 지름)** · 격자 1.0 × 10⁻³ × 1.0 × 10⁻³ m · 최소 유동화 속도 **0.017 m/s** | [인쇄] 표 1 |
| 네 계 | A = 50 N/m · 0.37 / B = 50,000 · 0.37 / C = 50 · 3.7 / D = 50,000 · 3.7 (표 2 머리는 *"Surface energy (J/m2)"* — 단위 어긋남 §3-8 ①) | [인쇄] 표 2 |
| 강성 두 값의 이유 | *"The lower limit was chosen to cover the range of values found in the literature (Kaneko et al., 1999; Xu et al., 2001; Ye et al., 2005)."* (p.186) — 낮은 값 (50) 의 이유만 · 높은 값 (50,000) 의 근거와 시간 간격과의 관계는 [미확인] | [인쇄] |
| 기체 속도 | 0.3 m/s (A · B) · 0.1 · 0.3 m/s (C · D) — 분배판 기공률 0.4 · 균일 유입 | [인쇄] p.186–187 |
| 기체 속도 비 | U/U_mf = 0.1/0.017 = **5.9** · 0.3/0.017 = **17.6** | [카드 산술] |
| 미기재 | 시간 간격 Δt · 감쇠 계수 η (식 4) · 굴림 마찰 μ_r (식 10) · z_min · H · 벽 마찰 · 계산 시간 · 반복 수 | [미확인] |

### 3-2. ★ 침강 — 배위수 · 힘 · 변형 · 충전 (Fig. 1 · 2 · 표 3 · p.187–188 · `fig_1.png` · `fig_2a–2d.png` · `tab_3.png` · `txt_p4_settling_cn_three_stages.png` · `txt_p4_settling_force_deformation.png` · `txt_p4_table3_packing_force_surface_energy.png`)
- **배위수 세 단계** (Fig. 1 · p.187): 접촉 없음 → 선형 증가 (*"except for system C"*) → 점근 최대.  *"The systems with larger stiffness take more time to reach the stable state than those with lower stiffness"* (p.187).

| 계 | 첫 접촉 (CN > 0.05) | CN 끝값 (곡선 끝 시각) | 끝값 95 % 도달 t₉₅ | 표 3 층 높이 · 충전율 · 평균 압축력 · 접촉 수 [인쇄] |
|---|---:|---:|---:|---|
| A (50 · 0.37) | 0.018 s | **3.069** (0.200 s) | 0.133 s | 0.0168 m · **0.537** · 2.00 µN · 76,719 |
| B (50,000 · 0.37) | 0.035 s | **3.569** (0.250 s) | 0.159 s | 0.01632 m · **0.538** · 1.65 µN · 89,216 |
| C (50 · 3.7) | 0.0095 s | **2.923** (0.200 s) | 0.121 s | 0.01715 m · **0.507** · 1.22 µN · 72,913 |
| D (50,000 · 3.7) | 0.028 s | **3.900** (0.239 s) | 0.175 s | 0.01600 m · **0.55** · 0.97 µN · 94,971 |

  (판독 = 벡터 곡선 꼭짓점 1,708–2,345 개 · 눈금 맞춤 잔차 x 3.1 × 10⁻⁵ s · y 2.0 × 10⁻³ [판독 · 카드 산술 (t₉₅ · 첫 접촉 = 꼭짓점에서 문턱 교차)])
- 본문 (p.187 표 3 설명): C 가 *"clearly has the lowest packing fraction (and the largest value of bed height), suggesting that surface energy has had a more important role in the settling of the particles than in the other three cases"* · 네 층의 평균 법선 힘은 *"within the same order of magnitudes despite the large differences in contact stiffnesses and cohesive forces"* — *"the weight of the bed is balanced by the interparticle contact forces with some differences probably due to frictions at container walls and the co-ordination number"*.
- **침강 중 힘 · 변형 (Fig. 2 · 로그 축 · 래스터 판독)**:

| 계 | 끝 평균 접촉력 (0.15–0.20 s 중앙) | 끝 평균 변형 | 초기 봉우리 (t ≤ 0.05 s 위 테두리 · 하한) | 0.005–0.02 s 중앙 힘 |
|---|---:|---:|---:|---:|
| A | **2.08 µN** | **0.0402 µm** | 3.79 µN | 1.04 µN |
| B | **1.73 µN** | **3.43 × 10⁻⁵ µm** | 438 µN | 7.92 µN |
| C | **1.26 µN** | **0.0268 µm** | 5.34 µN | 0.711 µN |
| D | **1.00 µN** | **2.07 × 10⁻⁵ µm** | 570 µN | 53.9 µN |

  - 끝 힘 판독 ÷ 표 3 인쇄 = 1.04 · 1.05 · 1.03 · 1.03 (같은 값을 다른 시각 · 방법으로 읽은 차) [카드 산술] · 끝 변형 비 A/B **1,171** · C/D **1,297** (κ 비 1,000) [카드 산술].
  - 본문 *"During the second stage, the average interparticle force is three orders of magnitude larger for the cases of larger stiffness (Figs. 2a and c). This is a consequence of the linear model used, where the interparticle contact force is proportional to the particle stiffness."* (p.187) — 판독 봉우리 비는 **B/A 116 · D/C 107** (두 자릿수) · 0.005–0.02 s 중앙 비 7.6 · 76 [카드 산술] → '세 자릿수' 는 판독과 맞지 않는다 (§3-8 ⑥).
  - *"By the end of the settling process the average interparticle force seems to converge to a stable value independent of the contact stiffness (Figs. 2a and c). However, the final average particle deformation is significantly different from each other (Figs. 2b and d)."* (p.187)

### 3-3. ★ 높이별 힘 — 4 지름 구간 (Fig. 3 · 4 · p.187–189 · `fig_3.png` · `fig_4.png` · `txt_p5_fig4_noncohesive_comparison.png`)
| 계 | 구간 평균 (표지 43–46 개) | 맨 아래 구간 (h 0.039 cm) | 맨 위 구간 (높이) | 맨 위 ÷ F_OFF |
|---|---:|---:|---:|---:|
| A | 1.12 µN | 1.47 | 0.092 µN (1.80 cm) | 1.08 |
| B | 0.85 | 1.14 | 0.084 (1.76 cm) | 0.98 |
| C | **1.92** | **2.79** | **0.922** (1.80 cm) | 1.08 |
| D | 1.58 | 1.95 | 0.832 (1.69 cm) | 0.97 |

  [판독 Fig. 3 표지 중심 · 평균 = 카드 산술 · F_OFF = §3-7]
- 본문: *"the average interparticle contact force increases with the surface energy and at any given height"* (p.187) ✓ (C · D > A · B).
- Fig. 4 (A · C · 같은 κ 50 의 **비점착 45,000 개 침강 한 번**): 평균 A 1.17 · C 1.98 · 비점착 1.00 µN · 맨 위 0.129 · 0.955 · **0.020 µN** (비점착 맨 위 ≈ 입자 무게 0.0126 µN 의 1.6 배 [카드 산술]) [판독] · *"The small difference in the magnitude between system A (0.37 mJ/m2) and the system of non-cohesive particles suggests that cohesion should not be too important for system A. Instead, the importance of cohesion seems much larger for the case of system C with (37 mJ/m2)"* (p.188 — '37' 은 3.7 의 오기로 보임 §3-8 ②).
- ★ **맨 위 구간 힘 ≈ 그 γ 의 떼는 힘** (0.97–1.08 배) [카드 산술] — 하중이 없는 표면에서 접촉마다 스프링 힘이 상한 vdW 인력 (= F_OFF · 식 6–8) 과 맞서는 평형이라는 뜻 [카드 해석].  구간 평균 − F_OFF = A 1.04 · B 0.76 · C 1.06 · D 0.72 µN → **γ 가 달라도 같은 κ 끼리 같다** (무게 몫은 κ 에만 걸림) [카드 산술].

### 3-4. ★ 유동화 — 낮은 점착 A · B (0.3 m/s · Fig. 5–8 · p.189–190 · `fig_5.png` – `fig_8.png` · `eq_20_granular_temperature_2d.png` · `txt_p6_AB_fluidization_cn_mobility.png` · `txt_p6_AB_force_two_orders.png` · `txt_p6_low_cohesivity_conclusion_breakage.png`)
- 스냅숏 (Fig. 5 · 0 · 0.1 · 0.2 · 0.30 · 0.40 · 0.50 s · 세로 0–0.06 m): *"No visual differences were found between the dynamics of the two systems. In both cases the particles seem to fluidize well within 0.2 s."* (p.189)
- 배위수 (Fig. 6): 시작 A 3.05 · B 3.28 → 0.4–1.0 s 평균 **A 0.667 · B 0.0045** [판독] · *"the coordination number for the case of larger stiffness is much smaller … the particles in the systems with larger stiffness have more mobility probably due to a smaller contact time"* (p.189).
- 평균 접촉력 (Fig. 7 · 로그 축): 0.3–0.95 s 중앙 **A 0.355 · B 47.3 µN** (비 133) · 기하평균 0.369 · 43.0 (비 **116**) · 최대 A 1.21 (0.84 s) · B 116 µN (0.69 s) [판독] · *"a large difference of about two orders of magnitude appears with time"* (p.189) ✓.
- 과립 온도 (Fig. 8 · 식 20): 봉우리 **A 227 (0.22 s) · B 215 cm²/s² (0.24 s)** · 0.3–1.0 s 평균 **A 119 · B 129 cm²/s²** [판독] · *"very similar for both systems"* (p.189) ✓.
- 저자 정리: *"the interparticle contact stiffness does not significantly influence the quality of fluidization of powders with low cohesivity. However, the differences in order of magnitude of the interparticle contact force suggest that the contact stiffness could influence the behaviour of systems in which particles are subjected to breakage."* (p.189)

### 3-5. ★ 유동화 — 높은 점착 C · D (Fig. 9–12 · p.189–192 · `fig_9.png` – `fig_12b.png` · `txt_p7_CD_block_channels_cn_drop.png` · `txt_p7_D_air_velocity_fig11_force.png` · `txt_p8_discussion_C_never_fluidizes_D_slight_drop.png`)
- 스냅숏 (Fig. 9 · 0.3 m/s · 0.1–0.7 s): *"During the initial 0.15 s the particles are lifted as a large block. After this moment, for system D (50 000 N/m) clusters of particles detach from the block and they disintegrate leading to the particle fluidization. … In contrast, for system C (50 N/m) the initial block breaks into a number of smaller blocks which fall and collapse developing channels through which the fluidizing gas passes."* (p.190)
- **배위수 (Fig. 10)** [판독 · 변화율 = 카드 산술]:

| 계 · 속도 | 첫 꼭짓점 · 곡선 최대 | 0.5–1.0 s 평균 | 변화 (첫 꼭짓점 기준) | 최소 (시각) |
|---|---:|---:|---:|---:|
| C · 0.1 m/s | 2.915 · 2.935 | 2.907 | −0.3 % | 2.84 (0.44 s) |
| C · 0.3 m/s | 2.884 · 2.915 | 2.517 | **−12.7 %** (최대 기준 −13.7 %) | 2.37 (0.91 s) |
| D · 0.1 m/s | 3.768 · 3.800 | 2.432 | **−35.5 %** | 1.87 (0.33 s) |
| D · 0.3 m/s | 3.586 · 3.747 | **0.351** | **−90.2 %** | 0.088 (0.33 s) |

  본문: C 는 *"roughly the same as in the packed bed for both values of superficial velocity"* · 0.3 m/s 에서 *"a small drop of about 15%"* (p.190) ✓ · D 는 *"a drop in the coordination number is observed indicating that the particles are getting fluidized for both values of superficial air velocity"* · *"this drop is greater for the case of higher air velocity"* (p.190) ✓ — 그러나 §4 (p.191) 는 D · 0.1 m/s 를 *"only a very slight drop"* 라 한다 (판독 −36 % · §3-8 ⑦).
- **평균 접촉력 (Fig. 11)**: 0.5–1.0 s 평균 C 0.832 · D 0.904 (0.1 m/s) · C 1.033 · **D 1.488 µN** (0.3 m/s) · 봉우리 C · 0.3 = 3.73 µN (0.448 s = 무너짐) · D · 0.3 = 6.32 µN (0.332 s) [판독] · 본문 *"at the value of superficial air velocity of 0.3 m/s the average contact force for system D (50 000 N/m) is larger than for system C whilst no differences appear at the values of air velocity of 0.1 m/s"* · C 의 작은 봉우리는 *"coincides in time with the collapse of the particle cluster to the bottom of the bed"* (p.190) ✓.
- **과립 온도 (Fig. 12)**: 0.1 m/s (12a) — 봉우리 D 28.0 (0.30 s) · C 8.35 (0.43 s) · 0.6–1.0 s 평균 **D 2.79 · C ≈ 0 (−0.008)** cm²/s² / 0.3 m/s (12b) — 봉우리 D 251 (0.24 s) · **C 539 (0.47 s = 덩어리 무너짐 충돌)** · 0.6–0.92 s 평균 **D 123 · C 48** cm²/s² [판독] · *"The level of granular temperature is very different for the two superficial air velocities"* (p.190).
- 논의 (p.191): *"When the surface energy has the value of 3.7 mJ/m2 and for low contact stiffness (system C) the particles are lifted as a block and fluidization is never achieved."* — Xu et al. (2001) 의 *"cohesive particles with 50 µm radius, 50 N/m contact stiffness, 1440 kg/m3 particle density and value of surface energy of 9 mJ/m2 (H=5.2×10−19 Nm)"* 와 같은 거동 · D 는 0.3 m/s 에서 *"fluidize in a very similar way to systems A and B"*.

### 3-6. 정성 지도 (Fig. 13 · p.192 · `fig_13.png` · `txt_p9_map_boundary_conclusions.png`)
- 가로 = *"Increasing stiffness (N/m)"* · 세로 = *"Surface Energy (J/m²)"* (축 단위는 J · 점 이름표는 mJ/m2) · 숫자 눈금 없음 · 왼쪽 위 C (*"POOR FLUIDIZATION"*) · 오른쪽 아래 B · 왼쪽 아래 A (*"GOOD FLUIDIZATION"*) · **D 는 왼쪽 아래 → 오른쪽 위로 오르는 빗금 '전이 영역' 선 위** · 화살표 *"Decreasing fluidization quality"* = 왼쪽 위 방향.
- *"However, the boundary between good and poor fluidization needs to be better specified and the combined effects of stiffness and other parameters."* (p.192 · 문장 그대로 — 동사가 빠져 있다).

### 3-7. ★ 카드 산술 — 떼는 힘 · Bond 수 · 평형 겹침 · 분리 일 · 접촉 시간 · 충전율 · 배위수 분모
(입자 반지름 R = 49 µm · 입자–입자 R\* = R/2 = 24.5 µm · 입자–벽 R\* = R (식 6 정의) · m = ρπd³/6 = **1.281 × 10⁻⁹ kg** · mg = **0.01257 µN** · g = 9.81)

| 양 | 식 | A (50 · 0.37) | B (50,000 · 0.37) | C (50 · 3.7) | D (50,000 · 3.7) |
|---|---|---:|---:|---:|---:|
| 떼는 힘 (입자–입자) | F_OFF = 3πγR\* (식 7) | 0.0854 µN | 0.0854 | **0.854** | **0.854** |
| 떼는 힘 (입자–벽) | R\* = R | 0.171 | 0.171 | 1.709 | 1.709 |
| Bond 수 (입자–입자) | F_OFF/mg | **6.80** | 6.80 | **68.0** | 68.0 |
| 평형 겹침 | δ_eq = F_OFF/κ | 1.71 nm | 0.0017 nm | **17.1 nm** | 0.017 nm |
| δ_eq ÷ R | — | 3.5 × 10⁻³ % | 3.5 × 10⁻⁶ % | 3.5 × 10⁻² % | 3.5 × 10⁻⁵ % |
| 끝 평균 변형 ÷ R (Fig. 2 판독) | — | **0.082 %** | 7.0 × 10⁻⁵ % | **0.055 %** | 4.2 × 10⁻⁵ % |
| 접촉 안 탄성 일 | F_OFF²/(2κ) | 7.30 × 10⁻¹⁷ J | 7.30 × 10⁻²⁰ | **7.30 × 10⁻¹⁵** | 7.30 × 10⁻¹⁸ |
| 접촉 밖 vdW 꼬리 일 (z_min ≈ 1.01 nm 가정) | F_OFF·z_min | 8.64 × 10⁻¹⁷ | 8.64 × 10⁻¹⁷ | 8.64 × 10⁻¹⁶ | 8.64 × 10⁻¹⁶ |
| 분리 일 합 | 위 둘 | 1.59 × 10⁻¹⁶ | 8.64 × 10⁻¹⁷ | **8.16 × 10⁻¹⁵** | 8.71 × 10⁻¹⁶ |
| 탄성 ÷ 꼬리 | δ_eq/(2z_min) | 0.85 | 0.00085 | **8.45** | 0.0085 |
| 할선 Hertz E\* (끝 평균 변형에서 · 가정) | κ/[(4/3)√(R\*δ)] | 3.8 × 10⁷ Pa | 1.3 × 10¹² | 4.6 × 10⁷ | 1.7 × 10¹² |

- **분리 일 산술의 근거**: 선형 스프링 (식 3) 반발 + 접촉 중 상한에 묶인 vdW 인력 F_v(z_min) = HR\*/(6z_min²) = F_OFF (식 6 · 7 · 8 을 합치면 같다) → 순 인력 F_OFF − κδ 가 δ_eq = F_OFF/κ 에서 0 · 떼는 일 = ∫₀^δeq (F_OFF − κδ) dδ = F_OFF²/(2κ) · 접촉을 떠난 뒤 꼬리 ∫ HR\*/(6z²) dz (z_min → ∞) = F_OFF·z_min [카드 산술 — 원문은 에너지 식을 쓰지 않는다].  z_min 은 이 논문에 없다 → Xu et al. (2001) 의 H 5.2 × 10⁻¹⁹ Nm · γ 9 mJ/m² (p.191) 를 식 8 에 넣은 **z_min = 1.01 nm** 를 빌렸다 [카드 산술 · 가정].
  ⇒ **분리 일 비 C/D = 9.37 · A/B = 1.84** — 같은 F_OFF 에서 **κ 가 1000 배 무르면 γ 3.7 은 떼는 일이 9 배, γ 0.37 은 1.8 배** · 지배 수 = **δ_eq/z_min ∝ γ/κ** (C 에서만 탄성 몫이 꼬리보다 크다) → 저자 기전 (*"larger deformations … need more energy"*) 의 방향과 크기 차를 이 산술이 뒷받침한다 [카드 해석].
  ⚠ 분리 일은 입자 무게 × 지름 (m g d = **1.23 × 10⁻¹² J**) 의 7 × 10⁻⁵ (B) – 7 × 10⁻³ (C) 배다 [카드 산술] — 저자 기전은 덩어리 (다수 접촉 · 집단 운동) 수준의 서술로 읽어야 하고, 한 접촉의 에너지 비교만으로 C 의 '덩어리 유지' 가 닫히지는 않는다 [카드 해석].  분리 변위 (δ_eq + z_min ≈ 18 nm ↔ 1.0 nm) 로 읽으면 C 의 접촉은 *늘어나도 끊기지 않는* 연성 접촉이다 [카드 해석].
- **γ 의 뜻**: 식 7 F_OFF = 3πγR\* 는 JKR 떼는 힘 (3/2)πWR\* 에서 **W = 2γ (γ = 한 표면의 표면 에너지)** 로 읽힌다 — `johnson1971_…` L28 (JKR 원문의 γ = 두 표면 합 접착일) 과 2 배 차이 [카드 해석 · 다른 카드 대조].
- **접촉 시간 (선형 스프링 · 감쇠 무시)** t_c = π√(m\*/κ) (m\* = m/2): κ 50 → **1.12 × 10⁻⁵ s** · κ 50,000 → **3.56 × 10⁻⁷ s** (√1000 = 31.6 배) [카드 산술] — 저자 *"more mobility probably due to a smaller contact time"* (p.189) 의 크기.  충돌 봉우리 힘 ∝ √κ 이면 31.6 배인데 판독 봉우리 비는 107–116 배 (§3-2) — 선형 '힘 ∝ 강성' (1000 배) 과 √κ 사이 [카드 해석].
- **충전율 재계산** (N(π/6)d³ ÷ (W · H · d) · 의사 3D 부피): A **0.539** · B **0.555** · C **0.528** · D **0.566** ↔ 인쇄 0.537 · 0.538 · 0.507 · 0.55 (A 만 맞음 · B · C · D 는 인쇄가 2.8–4.1 % 낮다) · 2D 면적 분율 (N(π/4)d² ÷ W · H) = 0.808 · 0.832 · 0.792 · 0.849 = **3D 꼴의 정확히 1.5 배** [카드 산술] → 같은 침대에 숫자 셋 (§3-8 ⑤).
  - ★ κ × γ 연동이 침강 충전에도 보인다: 같은 κ 에서 γ 를 올리면 **κ 50 은 충전이 내려가고 (A 0.537 → C 0.507) · κ 50,000 은 올라간다 (B 0.538 → D 0.55)** [인쇄 · 재계산도 같은 방향 0.539 → 0.528 · 0.555 → 0.566].
- **배위수 분모**: 2N_c/45,000 = 3.41 · 3.97 · 3.24 · 4.22 ↔ Fig. 1 끝 3.07 · 3.57 · 2.92 · 3.90 · 2N_c/**50,000** = **3.069 · 3.569 · 2.917** · 3.799 → A · B · C 는 소수 셋째 자리까지 맞고 D 만 다르다 [카드 산술] → 배위수 정의 (분모 · 벽 접촉 셈) [미확인] (§3-8 ④).
- **층 바닥 응력 (중력 · 벽 마찰 무시)** φρgH ≈ 0.537 × 2600 × 9.81 × 0.0168 = **230 Pa** (A) · 222 Pa (C) [카드 산술] → 우리 300 MPa 의 1/(1.3 × 10⁶).
- **Xu et al. (2001) 계의 Bond 수** (R 50 µm · ρ 1440 · γ 9 mJ/m²): F_OFF 2.12 µN ÷ mg 0.0074 µN ≈ **287** [카드 산술] — 이 논문 C (68) 의 4 배.

### 3-8. 원문 안 어긋남 (카드가 본 것 — 고치지 않고 적는다)
1. **γ 단위**: 표 1 *"Surface energy (mJ/m2) 0.37, 3.7"* ↔ 표 2 머리 *"Surface energy (J/m2)"* 에 같은 숫자 0.37 · 3.7 ↔ 그림 13 세로축 *"(J/m²)"* (점 이름표는 mJ/m2) — 본문 · 초록 · 결론은 전부 mJ/m² → 표 2 · 그림 13 축의 단위가 오기로 보인다 [카드 해석].
2. p.188 *"system C with (37 mJ/m2)"* — 다른 모든 곳은 3.7 [인쇄].
3. ★ **힘의 계 순서가 반대**: 표 3 · Fig. 2 끝값 = A 2.00 > B 1.65 > C 1.22 > D 0.97 µN ↔ Fig. 3 · 4 구간 평균 = **C 1.92 > D 1.58 > A 1.12 > B 0.85** (본문도 *"increases with the surface energy"* · p.187).  F_OFF 를 뺀 '무게 몫' 으로 보면 표 3 인쇄 그대로는 A 1.92 · B 1.57 · C 0.37 · D 0.12 µN (같은 무게인데 13 배 차) · **A↔C · B↔D 를 바꾸면 1.14 · 0.89 · 1.15 · 0.80** (같은 κ 끼리 같음 · Fig. 3 의 1.04 · 0.76 · 1.06 · 0.72 와 같은 꼴) · 무게 몫 × 접촉 수도 바꾸면 75,559–87,042 µN 로 고르고 인쇄 그대로면 10,979–146,883 [카드 산술] ⇒ **표 3 의 힘 행과 Fig. 2 의 (a)(b) ↔ (c)(d) 계 이름표가 서로 바뀌었을 가능성** [카드 해석 · 판정 아님 — 표 3 의 충전율 · 층 높이 · 접촉 수와 Fig. 1 은 본문 (C 가 가장 성김) 과 맞는다 · 어느 쪽이 맞는지 [미확인]].
4. **배위수 분모**: §3-7 — Fig. 1 끝값이 2N_c/50,000 과 A · B · C 에서 맞고 D 만 다르다 · 입자 수는 45,000 [미확인].
5. **충전율**: 표 3 인쇄 (B · C · D) 가 같은 표의 층 높이로 다시 계산한 값보다 2.8–4.1 % 낮다 · 충전율 · 층 높이의 정의 (표면 요철 · 측정 위치) [미확인] — 맨 위 구간 (Fig. 3) 높이도 표 3 층 높이보다 0.085–0.132 cm 위다 [판독].
6. **'세 자릿수'**: p.187 *"three orders of magnitude larger"* ↔ Fig. 2 판독 봉우리 107–116 배 · 같은 구간 중앙 7.6 · 76 배 (봉우리 판독은 가는 스파이크를 놓칠 수 있어 하한).
7. **D · 0.1 m/s**: §3.2.2 (p.190) *"a drop in the coordination number is observed indicating that the particles are getting fluidized for both values of superficial air velocity"* ↔ §4 (p.191) *"system D experienced only a very slight drop in the coordination number indicating poor mobility and mixing of the material and therefore a poor fluidization"* ↔ 판독 3.77 → 2.43 (−36 % · 최소 1.87 = −51 %) — 같은 그림을 두 절이 다르게 말한다.
8. p.190 *"as shown in Figs. 12a and 11b"* → 12b 의 오기로 보인다 [카드 해석].
9. 기호표 *"χ … equation coefficient defined in Eq. (12)"* → χ 는 식 (13) 에서 정의된다.
10. 식 (18) 점성 응력 *"μ_f[(∇u) + (∇u)^−1]"* — 전치 (∇u)ᵀ 의 인쇄 오류로 보인다 [카드 해석 · `eq_18_viscous_stress.png`].
11. 스냅숏 (Fig. 5 · 9) 세로축 0–0.06 m ↔ 표 1 *"Bed height (m) 4.5 × 10⁻²"* [판독 · 인쇄].
12. Fig. 6 의 시작 배위수 B 3.28 ↔ 침강 끝 (Fig. 1) 3.57 (8 % 낮음) [판독] — 침강 끝과 기체 시작 사이의 처리 [미확인].
13. 참고문헌: *"Di Felice, 1994 … Chemical Engineering Science 50"* · *"Ye … 2005 … Chemical Engineering Science 69"* (같은 목록의 2005 년 CES 인 Tatemoto 는 권 60) — 연도 · 권이 서로 맞지 않아 보인다 [카드 해석 · 미확인].
14. 표 1 의 입자 수 *"45.000"* (점) ↔ 본문 *"45 000"*.

---

## 4. ★ 방법 — 계산 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 계산 사슬 (CCDM · p.184–186)
- 입자 = DEM (뉴턴 운동 · 명시적 시간 적분 · Cundall & Strack 1979) · 기체 = 국소 평균 Navier–Stokes (Anderson & Jackson 1967) · 두 상은 *"modelled at different time and length scales"* 이고 *"coupled via the application of Newton's third law of motion"* (p.185) — 입자 항력의 합을 격자 칸 부피로 나눠 기체 운동량에 되먹임 (식 17).
- 순서: 무작위 배치 → 중력 침강 (*"The settling of the particles is considered to have finished once the coordination number and average interparticle forces do not change with time."* p.187) → 바닥 분배판으로 기체 유입 (0.1 · 0.3 m/s) → 배위수 · 평균 힘 · 과립 온도 기록 (~1 s).

### 4-2. 입자 처리 — 식 1–10 (p.185–186 · `eq_01_newton_translation.png` – `eq_10_rolling_friction_torque.png` · `eq_06_08_vdw_surface_energy_set.png`)
| 식 | 내용 | 비고 |
|---|---|---|
| (1) · (2) | m_i dv_i/dt = f_pf,i + m_i g + Σ_j f_ij · I_i dω_i/dt = Σ_j T_ij | 입자–기체 힘 · 중력 · 접촉 힘 / 토크 |
| (3) | **f_c,ij = −κ_i δ_ij** (선형 스프링 · Cundall & Strack 1979) | 법선 · 접선 모두 (p.185) |
| (4) | f_d,ij = −η_i v_ij (점성 감쇠) | η 값 [미확인] · 반발 0.97 (표 1) 과의 관계 [미확인] |
| (5) | Δδ_ij = v_ij Δt_c (Δt_c = Xu & Yu 1997 의 실제 접촉 시간) | 변위 이력 |
| — | \|f_ct\| > μ_s\|f_cn\| 이면 미끄럼 · \|f_ct\| = μ_s\|f_cn\| | μ_s 0.3 |
| (6) | **f_v,ij = H R\*_ij/(6z²)** (Israelachvili 1985) · R\* = R_i (벽) · R_iR_j/(R_i + R_j) (입자) | 접촉 중에는 z = z_min 에서 멈춤 (특이점 회피) |
| (7) | **F_OFF = 3πγR\*_ij** (Johnson et al. 1971) | 떼는 힘 |
| (8) | **γ = H/(18π z_min²)** (식 6 = 식 7 at z_min) | *"From now on, we will use the surface energy model to describe the level of cohesion"* (p.185) |
| (9) | T_c,ij = R_i × (f_ct,ij + f_dt,ij) | 접선 힘 토크 |
| (10) | \|T_r,ij\| = μ_r\|f_cn,ij\| (굴림 마찰 · Xu et al. 2001 · Zhou et al. 1999 · 2001) | μ_r 값 [미확인] |

### 4-3. 기체 · 풀이 · 경계 — 식 11–20 (p.186 · p.189 · `eq_11_drag_voidage_correction.png` – `eq_20_granular_temperature_2d.png` · `txt_p3_pseudo3d_porosity.png` · `txt_p3_solution_schemes_boundary_conditions.png`)
- 항력 (11)–(15): f_pf,i = f_pf0,i ε_i^{−(χ+1)} (Di Felice 1994 수정 · Xu & Yu 1998) · f_pf0 = 0.5c_d0 ρ_f πR² ε²\|u − v\|(u − v) · χ = 3.7 − 0.65 exp[−(1.5 − log₁₀Re_p)²/2] · c_d0 = (0.63 + 4.8/Re_p^0.5)² · Re_p = 2ρ_f R ε\|u − v\|/μ_f · 부력 무시.
- 기체 (16)–(19): 연속 · 운동량 (국소 평균) · 점성 응력 (식 18 인쇄 §3-8 ⑩) · **ε = 1 − Σ V_i/ΔV · 의사 3D ΔV = 2ΔxΔyR_i** (*"To account for the discrepancy in porosity calculations between 2D and 3D, the concept of pseudo-3D (Xu and Yu, 1997) is used"* p.186).
- 풀이: SIMPLE (Patankar 1980) · 유한체적 · 균일 엇갈린 격자 · 압력 구배 · 발산 2 차 중심 · 대류 3 차 상류 (유계) · 시간 2 차 Crank–Nicolson · 입자 = 명시적 적분 (p.186).
- 경계: 벽 미끄럼 없음 · 위 출구 법선 구배 0 · 바닥 균일 분배판 기공률 0.4 · *"The wall is assumed to be rigid and no displacement and movement of the wall results from this interaction."* (p.186).
- 과립 온도 (식 20 · p.189): **θ = (2θ_x + θ_Y)/3 = [2⟨v_X² − ⟨v_X⟩²⟩ + ⟨v_Y² − ⟨v_Y⟩²⟩]/3** — *"The reason for the factor 2 multiplying the average of the horizontal component of the velocity is due to the fact that the simulations reported here are performed in two dimensions."*

### 4-4. ★ 이 묶음의 네 질문 (원문 문장과 위치)
**(i) DEM 한계를 말한 문장** (인용 = Moreno-Atanasio, Xu & Ghadiri 2007, Chem. Eng. Sci. 62, 184–194)
- p.184 (`txt_p1_intro_coarse_particles_computing_power.png`): *"Previous applications of CCDM to the analysis of cohesive powders have been focused mainly on coarse particles due to the limitation of computing power."*
- p.185 (`txt_p2_complex_contact_laws_cost.png`): *"Although the linear contact model has been used in the interparticle interactions, it is not inherent to the CCDM. … The linear and non-linear models start to deviate from each other when examining the evolution of forces during a collision. However, generally speaking, more complicated contact laws need longer time to simulate, which is especially true when large numbers of particles are present in the system."*
- p.185 (`eq_06_08_vdw_surface_energy_set.png`): *"In practice the estimation of the van der Waals force acting on real powders is complicated by factors such as the surface geometry of contacting particles, local deformation of contact areas, hardness of particle materials and gas adsorption onto particle surfaces. These factors can change the magnitude of the van der Waals force significantly and are difficult to quantify."*
- p.187 (`txt_p4_settling_force_deformation.png`): *"This is a consequence of the linear model used, where the interparticle contact force is proportional to the particle stiffness."*
- p.189 (`txt_p6_low_cohesivity_conclusion_breakage.png`): *"the contact stiffness could influence the behaviour of systems in which particles are subjected to breakage."*
- p.192 (`txt_p9_mechanism_deformation_energy_ignored.png`): *"The effect of contact stiffness, representing the elastic deformation, has been widely ignored in the literature due to the experimental difficulty of varying it. … However, so far the effect of elastic and plastic particle properties has not adequately accounted for."*
- p.191 (논의 첫 문단): 배위수 · 접촉력은 *"difficult to determine experimentally"* — 모델이 주는 미시량이 실험으로 검증되지 않았다는 고백이기도 하다 [카드 해석].
- **말하지 않은 것**: 단단한 구 · 점접촉 · 겹침 상한 · 조밀 영역의 과강성 · 보정값이 물성이 아니라는 말 — 없음.

**(ii) 소성 · 큰 변형을 넣기 어려운 이유 · 우회 · 비용**
- 이유 (원문): 복잡한 접촉 법칙은 계산 시간이 길다 (p.185) · 실제 분말의 vdW 는 *"local deformation of contact areas, hardness of particle materials"* 등으로 정량이 어렵다 (p.185).  탄소성 접촉의 선례 = Kafui et al. (2002) *"elasto-plastic contact force–deformation relationship"* — 인용만 (p.185).
- 우회 (원문): 선형 탄성 스프링 + 감쇠 + 접촉 중 상한 고정 vdW (γ 로 지정) — 소성 · 입자 모양 변화 · 부피 보존 유동 · 가공 경화 · 이웃 접촉 상호 영향 · 하중 이력 없음 (선형이라 이력 없음 · 감쇠 손실만).
- 비용: 입자 45,000 · 계별 ≈1 s 물리 시간 · CPU 시간 [미확인] · 시간 간격 [미확인] — κ 50,000 의 접촉 시간 3.56 × 10⁻⁷ s [카드 산술] 이라 κ 50 보다 √1000 = 31.6 배 짧은 시간 간격이 필요했을 것 [카드 해석 · 원문 말 없음].

**(iii) 2D / 3D** — 의사 3D (한 입자 두께 · ΔV = 2ΔxΔyR · p.186) · 과립 온도는 2D 로 계산하고 세 번째 성분을 수평 성분과 같다고 둠 (식 20 · p.189) [카드 해석] · 2D → 3D 결과 전이에 대한 말 없음 · 입자 운동이 평면에 묶였는지의 명시 없음 (*"performed in two dimensions"* 로 미루어 그렇다 [카드 해석]).

**(iv) 탈압** — 다루지 않음.  압축 하중 자체가 없다 (중력 · 기체).  덩어리가 기체에 들려 갈라지는 과정 (C 채널 · D 해체) 이 '점착 침대를 떼는' 유일한 장면 [카드 해석].

### 4-5. 기법 미니 용어집
- **CCDM** (combined continuum and discrete model): 입자 = DEM · 기체 = 격자 평균 Navier–Stokes · 뉴턴 3 법칙 결합 (= 흔히 CFD-DEM).
- **의사 3D (pseudo-3D)**: 2D 입자 층을 한 입자 두께의 얇은 판으로 보고 칸 부피를 ΔxΔy × 2R 로 잡아 3D 꼴 기공률을 얻는 처리.
- **z_min**: 접촉 중 vdW 힘의 특이점을 피하려 두는 최소 간격 — 이 거리에서의 vdW 힘 = 떼는 힘 (식 6–8).
- **과립 온도**: 입자 속도 요동의 분산 (식 20).
- **U_mf**: 최소 유동화 속도 (0.017 m/s · 표 1).
- **Geldart A · C 분류**: A = 기포 전 팽창 · C = 점착 · 채널 · 완전 유동화 안 됨 (p.184).

---

## 5. Figure set ★
| 파일 | 원문 | 내용 | 비고 |
|---|---|---|---|
| `fig_1.png` | Fig. 1 · p.187 | 침강 중 배위수 (A–D) | 판독 53 행 |
| `fig_2.png` · `fig_2a.png` – `fig_2d.png` | Fig. 2 · p.188 | 침강 중 평균 접촉력 (a · c · µN 로그) · 평균 변형 (b · d · µm 로그) | 다시 자름 (여백) · 패널 4 = 손 크롭 · 래스터 판독 48 행 |
| `fig_3.png` | Fig. 3 · p.188 | 4 지름 구간 평균 접촉력 vs 높이 (A–D) | 판독 187 행 |
| `fig_4.png` | Fig. 4 · p.189 | 같은 그림 (A · C · 비점착 50 N/m) | 판독 137 행 |
| `fig_5.png` | Fig. 5 · p.189 | A (위) · B (아래) 스냅숏 0–0.50 s · 0.3 m/s | 손 크롭 (도구가 놓침) |
| `fig_6.png` · `fig_7.png` · `fig_8.png` | Fig. 6–8 · p.190 | A · B 배위수 · 평균 힘 (로그) · 과립 온도 | 판독 46 · 46 · 105 행 |
| `fig_9.png` | Fig. 9 · p.191 | C (위) · D (아래) 스냅숏 · 0.3 m/s | 다시 자름 (도구는 그림 10 + 11 을 잡았다) |
| `fig_10.png` · `fig_11.png` | Fig. 10 · 11 · p.191 | C · D 배위수 · 평균 힘 (0.1 · 0.3 m/s) | 판독 106 · 93 행 |
| `fig_12.png` · `fig_12a.png` · `fig_12b.png` | Fig. 12 · p.192 | C · D 과립 온도 (a 0.1 · b 0.3 m/s) | 패널 = 손 크롭 · 판독 48 · 86 행 |
| `fig_13.png` | Fig. 13 · p.192 | 강성 × 표면 에너지 정성 유동화 지도 | 숫자 눈금 없음 |
| `tab_1.png` · `tab_2.png` · `tab_3.png` | 표 1 · 2 (p.187) · 표 3 (p.188) | 매개변수 · 네 계 · 침강 침대 성질 | 셋 다 다시 자름 (도구가 쪽 통째) |

- **식 크롭 21** (`eq_*` · 손 크롭 · 300 dpi): `eq_01_newton_translation` · `eq_02_newton_rotation` · `eq_03_linear_spring_contact_force` · `eq_04_viscous_damping_force` · `eq_05_displacement_increment` · `eq_06_van_der_waals_force` · `eq_07_jkr_pull_off_force` · `eq_08_surface_energy_hamaker_zmin` · `eq_06_08_vdw_surface_energy_set` (식 6–8 과 그 문단) · `eq_09_contact_torque` · `eq_10_rolling_friction_torque` · `eq_11_drag_voidage_correction` · `eq_12_isolated_particle_drag` · `eq_13_di_felice_exponent` · `eq_14_drag_coefficient` · `eq_15_particle_reynolds` · `eq_16_fluid_continuity` · `eq_17_fluid_momentum` · `eq_18_viscous_stress` · `eq_19_cell_porosity_pseudo3d` · `eq_20_granular_temperature_2d`.
- **근거 문단 크롭 20** (`txt_*` · 이 카드가 인용한 문장만): p.184 초록 · 거친 입자 / 계산 능력 · p.185 목적 (강성 × 점착 미보고) · 접촉 법칙 비용 · p.186 의사 3D · 풀이 · 경계 · 강성 값 이유 · p.187 침강 방법 · 기체 속도 · 배위수 세 단계 · 힘 · 변형 (세 자릿수 · 선형 모델) · 표 3 설명 · p.188 비점착 비교 (Fig. 4 · '37 mJ/m2') · p.189 A · B 육안 · 배위수 이동성 · 힘 두 자릿수 · 낮은 점착 결론 + 파괴 문장 · p.190 C · D 덩어리 · 채널 · 15 % · D 속도 · 힘 · p.191 논의 (Tsuji 800 N/m · C 유동화 안 됨 · D 0.1 m/s 'very slight drop') · p.192 기전 · 문헌 무시 · 소성 · 지도 경계 · 결론 — 파일 이름 · 한 줄 뜻 = `figures.json`.

## 6. Post-processing ★
- 벡터 그림 (1 · 3 · 4 · 6 · 7 · 8 · 10 · 11 · 12): PDF 경로를 PyMuPDF `get_drawings` 로 꺼내 큰 눈금 위치에 최소제곱으로 맞춤 (잔차 = csv note) · 색으로 계열을 나눔 · 곡선 = 꼭짓점 · 표지 = 경로 상자 중심 · 창 평균 = 창 안 꼭짓점 산술 평균 (중앙 · 최소 · 최대 · 기하평균은 note).
- Fig. 2 (내장 래스터 1032 × 804 px · ≈200 dpi): 패널 틀 = 어두운 선 · 큰 눈금 = 안쪽 눈금 표시 ≥ 5 px → 로그 10 진 맞춤 · 검정 · 녹색 화소 열별 중앙 · 범례 상자 · 틀 옆 13 px 제외 · 봉우리 = 위 테두리 화소 (가는 스파이크를 놓칠 수 있어 **하한**).
- 이 카드의 계산 (§3-7): 떼는 힘 · Bond 수 · 평형 겹침 · 분리 일 · 접촉 시간 · 충전율 재계산 · 배위수 분모 · 계 순서 점검 — 식은 표 안에.
- 판독하지 않은 것: 스냅숏 (Fig. 5 · 9) 의 덩어리 · 채널 크기 · Fig. 13 (정성).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · 정본 카드 출처를 병기해 적는다)

### 7-1. 비교표 (모든 행에서 **재료 · 크기 · 응력 영역 · 과정이 다르다**)
| 항목 | 이 논문 | 우리 | 견줄 수 있나 |
|---|---|---|---|
| 입자 | 재료 이름 없음 · 98 µm 단분산 · ρ 2600 · 45,000 | LPSCl SE (µm 급) + NCM · 3D (CLAUDE.md) | 아니오 |
| 접촉 법칙 | 선형 스프링 κ + 점성 감쇠 + Coulomb · 굴림 + 상한 vdW | 압밀 DEM = LIGGGHTS hooke/hysteresis (frame [2]) · 믹서 = Hertz 반발 + SJKR 인력 (`johnson1971_…` §7-1) | 꼴만 |
| 강성 | κ 50 · 50,000 N/m (물성 아님 · 할선 Hertz E\* 로 38–46 MPa ↔ 1.3–1.7 TPa [카드 산술]) | DEM E_eff **1.35 GPa** (벌크 24 의 18 배 연화) · MPM E **1.53 GPa** · ν 0.49 · σ_y 0.30 GPa (CLAUDE.md) | 아니오 (정의가 다름) |
| 점착 | γ 0.37 · 3.7 mJ/m² → F_OFF 0.085 · 0.85 µN · Bo 6.8 · 68 [카드 산술] | 믹서 Bo_code (예: LH AM–AM 38.4 = 내부 탐색값 · dev-bo 384 · 1152 · CLAUDE.md) — Bo_code 는 평형 인력 기준 (= 떼는 힘 기준의 6.75 배 · `johnson1971_…` L197) | 정의를 맞춘 뒤에만 |
| 하중 | 중력 (바닥 ≈0.23 kPa) + 기체 항력 (U/U_mf 5.9 · 17.6) | 압밀 300 MPa · 믹서 = 회전 드럼 | 아니오 (10⁶ 배) |
| 차원 | 의사 3D 단층 | DEM 3D · MPM 2D / 3D | 아니오 |
| 기공 | 침강 충전율 0.507–0.55 (기공 45–49 %) | **랩 표준 순수 SE 기공 10–13 % (300 MPa) · 진밀도 1.64 g/cm³ — 고정 · 판정하지 않음** | 랩 표준과 다른 문헌 값 (중력 · 단층 · 다른 물질) |
| 탈압 | 없음 | 단계 6 | — |

### 7-2. ★ 같은 떼는 힘 · 다른 분리 일 — 이 논문의 선형 + 상한 vdW ↔ 우리 믹서 SJKR [우리 산술]
- **이 논문**: F_OFF = 3πγR\* 는 κ 와 무관 · 분리 일 = F_OFF²/(2κ) + F_OFF·z_min → κ 를 1000 배 올리면 탄성 몫이 1/1000 · 꼬리 몫은 그대로 (§3-7) → γ 3.7 에서 9.4 배 · γ 0.37 에서 1.8 배 차 [카드 산술 · z_min 가정].
- **우리 믹서 SJKR** (`johnson1971_…` §7-1 L196–200): 인력 = CED × 2πR\*δ · 반발 = Hertz (4/3)E\*√R\*δ^{3/2} · 떼는 힘 F_po = (2/3)π³R\*²CED³/E\*² · 평형 겹침 δ_eq = (9/4)π²CED²R\*/E\*².  δ_eq 에서 0 까지 순 인력을 적분한 **분리 일 W_sep = πCED R\* δ_eq²/5 = (81/80)π⁵ CED⁵ R\*³/E\*⁴** [우리 산술 — 이 카드가 적분] · SJKR 은 δ = 0 에서 힘이 0 이라 꼬리가 없다 (`johnson1971_…` L222).
- **F₀ 보존 규칙** (CED ∝ E\*^{2/3} · `johnson1971_…` L214 · L220 = JKR 등가 W (J/m²) 보존) 아래에서 **W_sep ∝ E\*^{−2/3}** → 우리 믹서 v2.6 의 **E_ref ×20 → W_sep ÷7.37 · ref2 ×40 → ÷11.7** [우리 산술 · 덱 값은 CLAUDE.md 믹서 줄 (E_ref ×20 · ref2 ×40 · F₀ 쌍별 보존)].
  - 같은 결론을 JKR 쪽에서: 떼는 힘 (3/2)πWR\* 는 E 무관 (`johnson1971_…` 식 21) · 무하중 접근 δ₀ = a₀²/(3R\*) (L221) · a₀³ = R·P₁/K (식 9) 에 P₁(P₀ = 0) = 6γπR (식 18 · L223) → a₀³ ∝ WR\*²/E\* → 분리 에너지 규모 F·δ₀ ∝ **W^{5/3}R\*^{4/3}E\*^{−2/3}** [카드 산술 · 차원] — 실제 JKR 에서도 같은 W 라면 무를수록 떼는 에너지가 크다 (그래서 이 논문의 기전 방향은 물리적이다).  문제는 **E 가 계산 · 보정 손잡이일 때** 분리 에너지가 손잡이를 따라간다는 것 [카드 해석].
- ★ **두 불변량은 함께 지킬 수 없다** [카드 해석 · 두 카드 종합]: 강성을 바꿀 때 **떼는 힘** 을 지키면 (이 논문 · 우리 F₀ 규칙) 분리 에너지가 E\*^{−2/3} 로 움직이고, **분리 에너지** 를 지키면 (`haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem` 식 23–24 · 부록 A: γ_mod = γ(E_mod/E)^{2/5} · 그 카드 L212 의 SJKR W_sep 식 = 이 절의 식) 떼는 힘이 (E_mod/E)^{2/5} 로 줄어든다.  SJKR 로 옮기면 분리 에너지 일정 = **CED ∝ E\*^{4/5}** (그 카드의 유도) ↔ 우리 F₀ 규칙 = **CED ∝ E\*^{2/3}** (W_sep ∝ CED⁵/E\*⁴ · F_po ∝ CED³/E\*² 에서 바로 나온다 [카드 산술]).  N-48 은 분리 에너지 일정으로 단일 충돌의 붙음 / 되튐을 지켰고 (그 카드 한 문장 · 그림 8 · 13), 이 논문은 떼는 힘 일정에서 점착 침대의 유동화가 갈렸다 → 우리 믹서의 F₀ 보존은 **이 논문 쪽 불변량** 이다.
- ⇒ 쓸 수 있는 말: *"떼는 힘 (또는 JKR 등가 W) 을 지키며 강성을 바꾸는 재척도는 점착 거동의 보존을 보증하지 않는다 — Moreno-Atanasio et al. (2007) 은 같은 떼는 힘에서 강성 1000 배 차가 점착 침대의 유동화 여부를 갈랐다 — 그래서 분리 일 (또는 평형 겹침 ÷ 힘 도달 거리) 도 함께 적는다"*.
  ⛔ 넘지 말 것: *"이 논문이 우리 믹서 결과가 바뀐다는 것을 보였다"* (유동화 ↔ 드럼 믹싱 · 선형 ↔ Hertz + SJKR · 98 µm ↔ parcel · 네 점 한 번씩) · *"×20 이면 결과가 7 배 바뀐다"* (W_sep 비는 거동 비가 아니다) · 이 논문의 γ · κ 값을 LPSCl · NCM 값처럼 쓰기.

### 7-3. ★ 겹침 문턱 (Lommen 0.3 %) 과 나란히 — 점착에서는 겹침 문턱이 거동을 지키지 못한다 [카드 해석]
- `lommen2014_…` 의 판정선 = 평균 법선 겹침 < 반지름의 0.3 % 면 안식각 · 관입이 크게 변하지 않음 (비점착 · mm 구).
- 이 논문의 끝 평균 변형 ÷ R = A 0.082 % · C 0.055 % · B 7 × 10⁻⁵ % · D 4 × 10⁻⁵ % [판독 · 카드 산술] — **네 계 모두 문턱 아래**인데 γ 3.7 에서 C ↔ D 의 거동이 갈렸다.  ⇒ 점착이 있으면 비점착 연화의 겹침 기준만으로는 '연화가 결과를 바꾸지 않는다' 를 말할 수 없다 · 점착의 길이 (z_min · 힘 도달 거리) 와 δ_eq 의 비가 따로 필요하다 [카드 해석].

### 7-4. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = DEM 쪽 (접촉망 · 점착 · 기체) 만 · MPM 쪽 (입자 형상 · 소성 유동) 은 *"plastic particle properties … not adequately accounted for"* (p.192) 로 비워 둔다.
- 우리 쪽에서 닿는 곳 = 후보 D0 의 믹서 (SJKR 연화 · 재척도) 와 R7 (파괴 판정의 힘) — 압밀 MPM 과는 닿지 않는다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 = 98 µm 모의 입자 · 중력 + 기체 · 의사 3D — 모든 행에 "재료 · 응력 · 과정 다름".)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ ① **같은 침대에 충전율 숫자 셋** — 인쇄 0.507–0.55 · 층 높이로 다시 계산 (3D 두께) 0.528–0.566 · 2D 면적 분율 = 1.5 배 (0.79–0.85) [카드 산술] → 연산자 (차원 · 높이 정의) 를 결과 전에 적어야 한다 · 기공 식 = 식 19 (ΔV = 2ΔxΔyR) ② 정지 기준을 미리 글로 (*"finished once the coordination number and average interparticle forces do not change with time"* p.187) | 압력 곡선 · SE 없음 · 기공 45–49 % 는 랩 표준 (10–13 %) 과 다른 물질 · 다른 하중의 값 |
| **단계 1** (3D 메모리 · 장 수) | 없음 | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 (CFD-DEM) | — |
| **단계 3** (2D 접촉 표현 비교) | 관측량 교훈 — *"Systems A and B look visually very similar although the quantitative analysis indicates differences in the average contact force and in the coordination number"* (p.191) · *"features such as the granular temperature and coordination number need to be determined"* (p.192) → 접촉 표현을 바꿔 견줄 때 그림 (스냅숏) 이 아니라 배위수 · 힘 분포를 등록 관측량으로 [카드 해석] | MPM · 압축 없음 · 점착을 켠 비교만 |
| **단계 4** (3D 순수 SE 붓기 · 누르기 · σ_y 하나 맞춤) | 붓기 (침강) 상태가 κ × γ 에 같이 걸린다 — 같은 κ 에서 γ 를 올리면 κ 50 은 충전 ↓ (0.537 → 0.507) · κ 50,000 은 ↑ (0.538 → 0.55) [인쇄 표 3] → SE 점착을 켤 경우 '느슨한 출발 상태' 는 연화 강성의 선택에 묶인다 [카드 해석] | 압축 · 항복 · LPSCl 없음 · 우리 압밀 DEM 의 점착 설정은 이 카드에서 [미확인] |
| **단계 5** (3D 복합 압밀) | 없음 | — |
| **단계 6** (탈압 · 되돌아옴) | 간접 — 저자 기전 (*"larger deformation … more energy"* p.192) 과 같은 산술: 같은 힘에서 겹침 · 저장 탄성 에너지는 **선형 스프링이면 ∝ 1/k (k ∝ E 이면 18 배 연화에 18 배) · Hertz 면 ∝ E^{−2/3} → 6.9 배** [우리 산술 · 우리 hooke 의 k–E 관계는 이 카드에서 [미확인]] → 연화 DEM 의 되돌아오는 양은 연화 몫을 떼어 등록해야 한다 | 탈압 계산 · springback 숫자 없음 |
| **단계 7** (형상 · 피복 · 수송) | 없음 (배위수 · 힘 분포만) | — |
| **후보 D0** (지금 DEM) | ★★ ① **정적 평균 접촉력은 하중 균형이 정한다** (표 3 네 층이 *"within the same order of magnitudes"* · 끝 힘이 κ 와 무관하게 수렴 p.187) · **변형은 κ 를 따른다** (끝 변형 비 1,171 · 1,297 [카드 산술]) → 압밀 DEM 의 18 배 연화는 정적 힘보다 겹침 · 면적 쪽을 바꾼다 [카드 해석] ② **동적 힘 (충돌 · 유동) 은 강성을 따른다** (봉우리 107–116 배 · 유동 중 평균 ≈117 배 [판독]) ③ ★ **믹서 (SJKR) 연화 · 재척도**: 떼는 힘 보존 ≠ 거동 보존 → 분리 일 W_sep ∝ E\*^{−2/3} (×20 → ÷7.37 · ×40 → ÷11.7) 을 결과 전 대조 항목에 Bo 와 나란히 [우리 산술 · §7-2] | 98 µm · 선형 · 유동화 · 네 점 · 우리 E_eff 1.35 GPa · 1.53 GPa 와 같은 축의 숫자 없음 (κ 는 물성 아님) |
| **후보 A′-0** (MPM 판 · 벽 · AM 접촉 규칙) | 벽 점착 = R\* = R (식 6) → 같은 크기 입자 쌍의 **2 배** (F_OFF,wall 0.171 · 1.709 µN [카드 산술]) · *"The wall is assumed to be rigid"* (p.186) → 판 분리 규칙에 점착을 넣으면 벽 몫을 따로 적는다 | 벽 점착의 효과를 따로 보지 않음 |
| **후보 A · A′** (MPM 강체 AM · 입자별 속도장) | 없음 | — |
| **후보 B** (MPFEM · NSCD) | 없음 | — |
| **후보 C** (MDR 류) | 없음 | — |
| **후보 C′** (Thornton–Ning · 다접촉) | 가리킴만 — Kafui et al. (2002) 의 탄소성 접촉 (CFD-DEM) · 쓰지 않은 이유 = 계산 시간 (p.185) · Di Renzo & Di Maio (2004) 선형 ↔ 비선형 힘 이력 차 (p.185) · 정본 = `thorntonning1998_adhesive_elastoplastic_contact` | 비교 숫자 없음 |
| **후보 M0** (균질화 압밀) | 없음 | — |
| **U0 · U1 · U2 · U6** | 없음 (U2 = Coulomb μ_s 0.3 · 굴림 마찰 식 10 — 시험 없음) | — |
| **U3** (단단한 구를 소성 블록에 눌렀다 떼기) | ★ 떼기 시험은 **떼는 힘과 분리 일을 함께** 보고해야 한다 — 같은 F_OFF 에서 분리 일이 κ 로 9.4 배 갈림 (§3-7) [카드 해석] | 소성 · 압흔 없음 |
| **U4** (판 분리) | 벽 점착 2 배 (위 A′-0) | — |
| **U5** (비슷한 강성 입자 충돌 · 다물체) | 선형 스프링 접촉 시간 t_c = π√(m\*/κ) = 1.12 × 10⁻⁵ s (κ 50) · 3.56 × 10⁻⁷ s (κ 50,000) [카드 산술] · 반발 0.97 · 봉우리 힘 비가 √κ (31.6) 와 κ (1000) 사이 (107–116 [판독]) | Δt · η [미확인] |
| **R1** (AM 이 움직이고 하중을 나눔) | 없음 (단일 물질) | — |
| **R2** (미끄럼 · 분리) | 점착 침대의 분리 = 덩어리 들림 → 갈라짐 (C 채널 · D 해체 · Fig. 9) · κ 가 분리 양상을 바꿈 | 정량 (덩어리 크기 · 분리 시각) 없음 |
| **R3** (SE 입자 경계 기억) | 없음 | — |
| **R4** (탈압 · 되돌아옴) | 없음 (반발 계수 0.97 · 위 단계 6 의 산술만) | — |
| **R5** (맞추는 값은 모델마다 하나) | ★ 경고 — 점착이 있으면 **κ 와 γ 가 떨어지지 않는다** (γ 0.37 은 κ 무관 · γ 3.7 은 κ 가 결과를 가름) → 연화 강성을 쓰면서 점착 값 하나를 떼는 힘으로만 맞추면 '맞춘 값 하나' 가 거동을 지키지 못할 수 있다 [카드 해석] | 이 논문은 아무것도 맞추지 않았다 (κ = 문헌 범위 · 실험 없음) |
| **R6** (SE 형상 변형) | 없음 — *"elastic and plastic particle properties has not adequately accounted for"* (p.192) | — |
| **R7** (AM 파괴) | *"the contact stiffness could influence the behaviour of systems in which particles are subjected to breakage"* (p.189) — 동적 상태의 힘이 κ 로 두 자릿수 차 → 힘 기반 파괴 판정 (우리 Auerbach) 은 **준정적 압밀의 하중 균형 힘** 으로 하고, 충돌 · 유동의 봉우리 힘은 연화에 묶인다고 적는다 [카드 해석] | 파괴 계산 없음 |
| **결과 전 대조 항목** | 제안 — 믹서 E 재척도 (×20 · ×40 · F₀ 쌍별 보존) 전후의 **쌍별 분리 일 · 평형 겹침** 을 결과 전 표에 Bo 와 함께 적어 둔다 (값은 우리 덱에서 · 이 논문의 숫자는 쓰지 않는다) | — |

## 9. 적용 인사이트 (행동)
1. **믹서 (흐름 밖 · 후보 D0)**: 떼는 힘 (F₀) 보존 재척도를 쓴 모든 팔에 쌍별 분리 일 W_sep = (81/80)π⁵CED⁵R\*³/E\*⁴ 를 같이 계산해 둔다 · 어느 불변량 (떼는 힘 ↔ 분리 에너지 · §7-2 · `haervig2017_…`) 을 지켰는지를 결과 전에 적는다 — 등록 문서는 이 카드가 고치지 않는다 (제안).  ⛔ 이 논문으로 우리 믹서 결과를 예측하지 않는다.
2. **보고 문구**: *"같은 Bond 수 = 같은 점착"* · *"F₀ 를 지켰으니 점착 거동은 같다"* 를 쓰지 않는다 — 이 논문이 같은 F_OFF · 같은 Bo 에서 반대 결과를 낸 사례다.
3. **파괴 판정 (R7)**: 연화 DEM 의 힘은 정적 (하중 균형 · κ 무관) 과 동적 (κ 에 묶임) 을 나눠 쓴다.
4. **기공 연산자 (단계 0)**: 2D · 의사 3D · 3D 충전율을 이름으로 구분해 적는다 (같은 침대에 1.5 배 차).
5. **비교 관측량 (단계 3)**: 육안이 같아도 배위수 · 힘이 다르다 — 등록 관측량은 숫자로.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- *"These results suggest that the influence of the contact stiffness on the behaviour of powders depends on the cohesivity of the powders: the more cohesive the powder is, the larger are the differences in the behaviour of systems with different contact stiffnesses."* (p.184 초록) [인쇄]
- *"When the surface energy has the value of 3.7 mJ/m2 and for low contact stiffness (system C) the particles are lifted as a block and fluidization is never achieved."* (p.191) [인쇄]
- *"For the same value of cohesive forces, in the case of low stiffness, the particles have larger deformations and therefore need more energy to break the interparticle contacts as compared to the case of high stiffness; therefore, the particles remain agglomerated even after the air flow is switched on."* (p.192) [인쇄 · 저자 가설 *"likely"*]
- *"This is a consequence of the linear model used, where the interparticle contact force is proportional to the particle stiffness."* (p.187) [인쇄]
- *"However, generally speaking, more complicated contact laws need longer time to simulate, which is especially true when large numbers of particles are present in the system."* (p.185) [인쇄]
- 카드 산술 문장 (원문 아님 · 표지 붙여): *"같은 떼는 힘 (0.854 µN) 에서 분리 일은 κ 50 이 κ 50,000 의 약 9 배 (z_min ≈ 1 nm 가정) [카드 산술]"*.

## 11. 주의/한계 (over-claim 방지)
- **실험 없음** · 네 점 · 계별 1 회 (반복 · 시드 산포 [미확인]) — '유동화 안 됨' 은 한 실현의 관측이다.
- 강성 두 값은 보정이 아니라 *"to cover the range of values found in the literature"* (p.186) — 어느 κ 가 어떤 실제 물질에 해당하는지 말하지 않는다 · κ 는 물성이 아니다 (§3-7 할선 E\*).
- 선형 스프링이라 접촉 시간 · 봉우리 힘의 강성 의존이 Hertz 와 다르다 (선형 t_c ∝ κ^{−1/2} · Hertz 는 충돌 속도에도 의존 — `lommen2014_…` 의 접촉 시간 ∝ G^{−0.40} [그 카드 판독]) — 결과를 Hertz · SJKR 연화에 옮길 때 지수가 다르다 [카드 해석].
- 시간 간격 · 감쇠 계수 · 굴림 마찰 · z_min · H 가 없다 → 재현 불가 · 분리 일 산술은 z_min 을 빌렸다.
- 힘의 계 순서 (표 3 · Fig. 2 ↔ Fig. 3 · 4) 가 반대 — 힘 숫자를 인용할 때 어느 그림인지 같이 적는다 (§3-8 ③).
- D · 0.1 m/s 의 서술이 두 절에서 다르다 (§3-8 ⑦) — 이 조건을 '유동화' 나 '불량' 어느 한쪽으로 인용하지 않는다.
- 의사 3D 단층 · 98 µm · 중력 kPa 이하 — 300 MPa 압밀 · 3D · µm SE 로 옮기지 않는다.
- 저자 기전은 *"likely"* — 이 카드의 분리 일 산술도 한 접촉 수준이라 덩어리 거동을 닫지 못한다 (§3-7 ⚠).

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 서지 (원문 목록 그대로) | 이유 | litdb |
|---|---|---|
| Xu, B.H., Yu, A.B., Zulli, P., 2001. The effect of interparticle forces on powder fluidization behaviour. In: Kishino, Y. (Ed.), Powders and Grains. AA Balkema Publishers, Rotterdam, pp. 577–580. | κ 50 N/m · γ 9 mJ/m² · H 5.2 × 10⁻¹⁹ 의 원전 (z_min 산출 · C 와 같은 거동) · 낮은 κ 의 '문헌 범위' 근거 | 카드 없음 (§n 후보) |
| Di Renzo, A., Di Maio, F.P., 2004. Comparison of contact-force models for the simulation of collisions in DEM-based granular flow codes. Chemical Engineering Science 59, 525–541. | 선형 ↔ 비선형 접촉 모델 차 (e · U5) | 카드 없음 (§n 후보) |
| Kafui, K.D., Thornton, C., Adams, M.J., 2002. Discrete particle-continuum fluid modelling of gas–solid fluidized beds. Chemical Engineering Science 57, 2395–2410. | CFD-DEM 의 탄소성 접촉 선례 (C′ · l) | 카드 없음 (§n 후보) |
| Xu, B.H., Yu, A.B., 1997. Numerical simulation of the gas–solid flow in a fluidized bed by combining discrete particle method with computational fluid dynamics. Chemical Engineering Science 52, 2785–2809. | CCDM 원전 · 의사 3D · 실제 접촉 시간 Δt_c 정의 (g · 방법 [미확인] 칸) | 카드 없음 (§n 후보) |
| Tsuji, Y.T., Kawaguchi, T., Tanaka, T., 1993. Discrete particle simulation of two-dimensional fluidized bed. Powder Technology 77, 79–87. | 비점착 유동층 κ 800 N/m 연화 선례 (k) | 카드 없음 (§n 후보) |
| Johnson, K.L., Kendall, K., Roberts, A.D., 1971. Surface energy and the contact of elastic solids. Proceedings of the Royal Society London A 324, 301–313. | 식 7 원전 | `johnson1971_jkr_surface_energy_contact_elastic_solids` |
| Cundall, P.A., Strack, O.D.L., 1979. A discrete numerical model for granular assemblies. Géotechnique 29, 47–65. | 선형 접촉 원전 | 카드 없음 (후보로 세지 않음) |
| Kaneko, Y., Shiojima, T., Horio, M., 1999. DEM simulations of fluidised beds for gas-phase olefin polymerization. Chemical Engineering Science 54, 5809–5821. | 낮은 κ 의 문헌 범위 근거 (하나) | 카드 없음 (후보로 세지 않음) |
| Geldart, D., 1973. Types of gas fluidization. Powder Technology 7, 285–292. | 분류 A–D | 카드 없음 (`geldart2006_…` 은 다른 논문) |

## 13. [미확인] 목록 (원문 11 쪽 전수에 없음)
- 시간 간격 Δt · 점성 감쇠 η · 굴림 마찰 μ_r · z_min · Hamaker H · 벽 마찰 · 벽 점착을 따로 다룬 값.
- 계산 시간 (CPU · 하드웨어) · 계별 반복 수 · 시드.
- 입자 재료 (ρ 2600 의 물질 이름).
- 배위수 정의 (분모 · 벽 접촉) · 충전율 · 층 높이의 측정 정의 (§3-8 ④ ⑤).
- 표 3 힘 행 · Fig. 2 이름표와 Fig. 3 · 4 가운데 어느 쪽이 맞는지 (§3-8 ③).
- 침강 끝과 기체 시작 사이의 처리 (Fig. 6 시작 배위수 차 §3-8 ⑫).
- 호 번호 (1–2) — PDF 에 인쇄 없음.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- PDF 11 쪽을 글자 층 추출 (블록 좌표 · µ · 그리스 문자 · 위첨자 깨짐 → 렌더로 확인) + 쪽 렌더 + 크롭 300 dpi 렌더로 읽음.  서지 = p.184 머리글 (*"Chemical Engineering Science 62 (2007) 184–194"*) · 제목 · 저자 · 소속 · *"Available online 26 August 2006"* · 초록 · 키워드 · 바닥 (DOI · 0009-2509 · © 2006) · p.193 감사 (Nexia Solutions) · 참고문헌 31 (p.193–194).  SI 없음.
- 그림 크롭 **63 장** = 도구 15 (그림 1 · 3 · 4 · 6 · 7 · 8 · 10 · 11 · 12 · 13 그대로 + 캡션 합자 고침 10 · **다시 자름 5** = 그림 2 (여백) · 그림 9 (도구는 그림 10 + 11 을 잡음) · 표 1 · 2 · 3 (쪽 통째)) + 손 48 (그림 5 (도구가 놓침) · 패널 2a–2d · 12a · 12b · 식 21 · 근거 문단 20).  전부 직접 열어 봄.
- 판독: 벡터 그림 9 장 + 래스터 그림 2 → digitized.csv 955 행 (방법은 note 칸).
- 2 차 인용 대조: `roessler2019` L238 (가리킨 카드) · `paulick2015_elastic_…` L384 · L408 · L679 · `paulick2015_particle_contact_…` L309 · L513 — 고치지 않았다 (카드 문제 = 정독 출력 batch_89 의 "카드 문제" 절).
- 정본 litdb 중복 확인: `git ls-tree` (papers/ 564 장 · rebase 뒤 N-48 `haervig2017_…` 이 들어와 565 장) + `git grep` (DOI `ces.2006.08.036` · 'Moreno-Atanasio' · 'contact stiffness and adhesion') — 카드 없음 (인용만: roessler2019 · paulick2015 두 장) (2026-11-12).

## 🔗 관련 카드
- 이 논문을 인용한 카드: `roessler2019_dem_cohesive_aor_cylinder_lift_calibration` (참고문헌 L238) · `paulick2015_elastic_particle_properties_dem_review` (ref [63]) · `paulick2015_particle_contact_stiffness_two_particle_method` (ref [40]).
- 같은 묶음 (강성 연화 · 점착 환산): `lommen2014_dem_speedup_contact_stiffness_reduction_bulk_behavior` (N-47 · 비점착 겹침 문턱) · `haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem` (N-48 · 분리 에너지 일정 재척도 — 이 카드 = 떼는 힘 일정의 반례 · §7-2).
- 점착 접촉 법칙: `johnson1971_jkr_surface_energy_contact_elastic_solids` (식 7 · 우리 SJKR 대응식) · `thorntonning1998_adhesive_elastoplastic_contact` · `thorntonyin1991_oblique_impact_elastic_spheres_adhesion` · `luding2008_cohesive_frictional_contact_models` · `morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis`.
- 점착 · 믹싱 · Bond 수: `jarray2019_cohesion_driven_mixing_segregation_drum` · `deng2021_mechanical_surface_energy_tester_bond_number` · `alizadeh2018_dem_adhesion_calibration_segregation_heap`.
- 강성 실측 · 보정: `paulick2015_particle_contact_stiffness_two_particle_method` · `coetzee2017_dem_calibration_review`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 형식 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md (절 번호 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표) ·
     믹싱 · 점착 절 구성 = jarray2019_cohesion_driven_mixing_segregation_drum.md · 같은 묶음 이웃 = khakhar1999_… (§0-2 공백 검사 꼴) · chaudhuri2006_… · li2006_… · nase2001_….
     쪽 표기 = 인쇄 쪽 "p.N" (Chem. Eng. Sci. 86 (2013) 99–107 · PDF n 쪽 = 인쇄 p.(98 + n) · figures.json 의 page 와 크롭 이름 txt_p<n> 은 PDF 쪽).  SI · 부록 파일 없음 (본문 9 쪽 = 부록 A 포함 전수).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자 / [판독] = 벡터 그림의 마커 · 곡선 꼭짓점 (PyMuPDF get_drawings · 눈금선 직선 맞춤 · 재현 = litdb/figures/<slug>/digitized.csv · 정밀도 y ≈ 0.001) /
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산 (식 · 가정 병기) / [우리 산술] = 원문 밖 값 (우리 덱 · 리포 문서 · 다른 정본 카드) 과 엮은 계산 / [카드 추론] · [추정] = 이 카드의 해석 / [미확인] = 원문 9 쪽 전수에 없음.
     ⚠ 글자 층은 그리스 문자 · 수식을 깨뜨린다 (γ→g · ω→o · Ω→O · θ→y · δ→d · ε→e · '='→'¼' · '−' 빠짐 · 'µm' → 'mm' — S_min 은 렌더로 '5 µm' 확인) — 인용한 숫자 · 식은 전부 200–400 dpi 렌더로 확인했다. -->
# 젖은 (액체 다리) 입자의 회전 드럼 가로 혼합 DEM — 1.3 mm 같은 구 15,000–47,000 개 · 드럼 70 × 26 mm · 표면장력 0–0.093 N/m (액량 0.5 % · 원문 '이른바 Bond 수 0–약 7') × 5–35 rpm (Fr 0.001–0.05) × 충전율 30–92 % · Lacey 지수 M(t) = M∞ erf(kt) — 점착은 회전당 혼합 속도 k 를 줄이고 (0.410 → 0.236 rev⁻¹ · 40 % · 15 rpm [판독]) · 회전당 k 는 마른 입자만 rpm 따라 줄며 (−18 %) 젖은 입자는 평평 · 마른 입자는 64 % 충전에서 가장 나쁘고 (k 0.058) 그 구간에서만 점착이 혼합을 돕는다 · 순환 주기의 평균 · 표준편차 모형 (Ding 2002 확장) 이 σ(T) 최소 67 · 74 % 를 냄 — Liu · Yang · Yu (Chem. Eng. Sci. 2013)

> slug `liu2013_wet_cohesive_particles_transverse_mixing_rotating_drum_circulation_period` · DOI `10.1016/j.ces.2012.06.015` · type `DEM (in-house soft-sphere: Hertz + nonlinear viscous damping normal · μ_s-capped 3/2-power tangential · rolling friction μ_r 10⁻³ · static pendular capillary force at fixed bridge volume (Rabinovich 2005 revised by Lambert 2008) · S_min 5 µm fitted · rupture (1 + 0.5θ)V^(1/3)) · 3D rotating drum 70 × 26 mm (end walls μ 0.05) · monosized 1.3 mm spheres 15,000–47,000 · colour-only binary side by side · γ 0–0.093 N/m × 5–35 rpm × filling 30–92 % · Lacey index (2d × 2d) · error-function fit · circulation-period analysis + analytical model (extension of Ding 2002) · no experiment in this paper (calibration = Liu 2011) · no compaction` · PDF `3d03ba82-DEM_study_of_the_transverse_mixing_of_wet_particles_in_rotating_drums.pdf` · digested `2026-11-24` · status ✅
>
> **원제**: *DEM study of the transverse mixing of wet particles in rotating drums* (p.99)
> **저자**: P.Y. Liu · **R.Y. Yang\*** (교신, r.yang@unsw.edu.au) · A.B. Yu — Laboratory for Simulation and Modelling of Particulate Systems, School of Materials Science and Engineering, The University of New South Wales, Sydney, NSW 2052, Australia (p.99) · *Chemical Engineering Science* **86** (2013) **99–107** · 접수 2011-10-06 · 수정본 접수 2012-05-29 · 승인 2012-06-08 · 온라인 2012-06-16 · 키워드 *Discrete element method · Rotating drum · Wet particles · Transverse mixing · Circulation period · Particle flow* · 연구비 Australia Research Council (p.106).
> **이웃 카드 (링크만)**: [`nase2001_granular_bond_collision_number_wet_cohesion`](nase2001_granular_bond_collision_number_wet_cohesion.md) (S_min 관행 · Bond / 충돌 수 · 이 논문 참고문헌) · [`khakhar1999_chaotic_mixing_granular_2d_tumbling_mixers_flowing_layer`](khakhar1999_chaotic_mixing_granular_2d_tumbling_mixers_flowing_layer.md) (흐름층 기구학 · 이 논문은 같은 그룹 1997 판을 인용) · [`chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed`](chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed.md) (이 논문이 Bond 0.1 · 120 · 마개 흐름을 인용) · [`li2006_cohesive_mixing_shear_cell_collision_number_phase_diagram`](li2006_cohesive_mixing_shear_cell_collision_number_phase_diagram.md) (전단 세기 · 충돌 수) · [`lacey1954_particle_mixing_theory_index`](lacey1954_particle_mixing_theory_index.md) (식 5 의 원전 · 인용) · [`chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer`](chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer.md) · [`chandratilleke2012_particle_scale_mixing_index`](chandratilleke2012_particle_scale_mixing_index.md) (같은 UNSW · Yu 그룹 DEM) · [`jarray2019_cohesion_driven_mixing_segregation_drum`](jarray2019_cohesion_driven_mixing_segregation_drum.md) · [`figueroa2009_vdw_adhesion_mixing_segregation_bond_number_phase_diagram`](figueroa2009_vdw_adhesion_mixing_segregation_bond_number_phase_diagram.md) (McCarthy 계보 · 이 논문은 같은 그룹 2010 판을 인용).
> **판독 원자료**: `litdb/figures/liu2013_wet_cohesive_particles_transverse_mixing_rotating_drum_circulation_period/digitized.csv` (357 행 — 그림 5a · 5b · 6 · 8a · 8b · 10a · 10b · 11a · 11b · 12a · 12b 의 마커 + 그림 3a 각도 통계 + 그림 12 이론선 극값) · 크롭 **75 장** (그림 13 = 전부 다시 자름 · 그래픽 초록 1 · 패널 12 · 표 2 (표 1 = 도구가 놓쳐 손 크롭 · 표 2 = 쪽 전체 → 다시 자름) · 식 28 = 번호 식 17 + 문장 안 식 7 + 표 1 줄 4 · 근거 문단 19) — `figures.json`.
> **이 카드가 서랍에 들어온 이유**: 후보 표 N-153 (1저자 11-23 업로드) — 우리 믹서 드럼 (B1 · B2 · 39 각형 · Fr 0.0827) 의 **회전 속도 (rpm) 공정 축** 과 **균일 점착 세기 축** (B1-U → B2-U = 모든 쌍 ×100) 을 같은 꼴의 DEM 으로 먼저 돌린 선례 — 액교 점착 × 회전 속도 × 충전율.

> ★★ **한 줄로 왜 중요한가**: (i) 점착을 **모든 쌍에 같은 세기로** 키우면 (γ 0 → 0.093 N/m) 회전당 혼합 속도가 42 % 줄어든다 — 우리 B1-U → B2-U (상대비 고정 · 모든 쌍 ×100) 와 같은 꼴의 대조 (방향만).  (ii) 회전당 k 는 **마른 입자만** rpm 에 따라 줄고 (Fr 0.001 → 0.048 에서 −18 %), 젖은 입자는 평평 — 저자는 '마른 입자는 드럼에 미끄러지고 점착은 미끄럼을 줄인다' 로 읽는다 (자료 없는 제안).  (iii) 64 % 충전의 마른 이상은 순환 주기 **표준편차** 의 최소와 맞고, 이 카드가 부록 모형을 다시 풀어 보면 그 최소는 흐름층 가장 깊은 점이 드럼 중심을 막 지난 자리 (비혼합 핵이 생기기 시작) 다 — **충전율 ≤ 50 % 면 이 모형에 핵이 없다** (우리 30 %).  (iv) 우리 드럼의 충전율 정의 (정지 충전 밀도 0.6 의 겉보기 부피 ÷ 드럼) 가 이 논문과 **글자 그대로 같고**, 우리 0.29–0.30 은 이 논문의 **최저 칸 (30 %)** 이다.
> ⚠ 단 **점착 대비가 없다** (두 입자 = 색만 다름 · 모든 쌍 · 벽이 같은 γ) — 우리 논지의 '점착 비' 질문 (γ_AM/γ_SE) 에는 아무것도 주지 않는다 · mm 단분산 유리 같은 구 · 액교 (건식 vdW 아님) · Fr ≤ 0.05 (우리 0.0827 = 1.7 배 밖) · 좌우 초기 배치 (우리 층상) · 실험 대조는 이 논문에 없다.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 지름 1.3 mm · ρ 2500 kg/m³ · E 1.0 × 10⁷ Pa 의 같은 구를 색만 바꿔 좌우로 나눠 넣고 (70 × 26 mm 드럼 · 15,000–47,000 개), 모든 접촉에 물 같은 액체 다리 (액량 0.5 vol% · 접촉각 0 · 표면장력 0–0.093 N/m · 최소 간격 5 µm 아래는 힘 일정 · 파단 거리 (1 + 0.5θ)V^{1/3}) 를 정적 모세관력으로 넣은 DEM 에서 가로면 Lacey 지수를 재면, 혼합은 M(t) = M∞ erf(kt) 를 따르고 (식 6 · 지수 함수보다 잘 맞음), 점착은 거의 모든 조건에서 k 를 줄이며 (40 % · 15 rpm 에서 γ 0 → 0.093 N/m 이 0.410 → 0.236 rev⁻¹ [판독]), 회전당 k 는 마른 입자만 rpm 에 따라 줄고 (0.471 → 0.387 · 5 → 35 rpm [판독]), 충전율 > 50 % 에서는 모두 급락하되 마른 입자만 64 % 에서 바닥을 찍고 (k 0.058 · M(10 바퀴) 0.52 [판독]) 그 구간 (60–70 %) 에서만 젖은 입자가 더 잘 섞인다 — 저자는 이를 순환 주기 T 의 평균 (길수록 나쁨) 과 **표준편차 (작을수록 나쁨)** 로 설명하고, Ding 2002 의 회전 영역 모형을 흐름선별로 넓힌 해석 식 (7) 로 σ(T) 의 최소 (동적 충전율 ≈ 67 · 74 %) 와 둘째 봉우리 (84 %) 를 재현한다 (평균은 잘 · 표준편차는 정성적으로 · 낮은 충전에서 과대).

| 우리 질문 (지시서 · 꼭 뽑을 것) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① DEM 힘 모델 (접촉 · 액교 · 파단 거리) | 뉴턴 식 (1) · (2) + **표 1**: 법선 = Hertz (2/3)(Y/(1−σ̃²))√R̄ ξ_n^{3/2} − 비선형 감쇠 γ_n(Y/(1−σ̃²))√R̄√ξ_n(v·n̂) · 접선 = −sgn(ξ_s)μ_s‖F^n‖[1 − (1 − min(ξ_s, ξ_s,max)/ξ_s,max)^{3/2}] · **모세관 = 4πR̄γcosθ_c / (1 + 1/[√(1 + V/(πR̄S²)) − 1])** (Rabinovich 2005 → Lambert 2008 · 다리 부피 V 로) · 같은 식을 벽에도 (반지름 ∞) · 구름 마찰 μ_r R_i‖F^n‖ω̂ · 점성력 식 (3)–(4) 은 계산해 보고 버림 (법선 에너지 손실 < 5 % · 접선 < 미끄럼 마찰의 2 % — 5 cm/s · d 1.3 mm · γ 0.073 · μ 0.001 Pa s) · **S_min = 5 µm (맞춤 매개변수)** · 다리에 들어가는 액량 = 5 % · 파단 S_rup = (1 + 0.5θ_c)V^{1/3} (Lian 1993) · 다리 변형 · 동적 (점성) 다리 무시 | [인쇄] p.100–101 · 표 1 · 식 1–4 · `eq_t1_*` |
| ② 입자 · 드럼 · 공정 | 표 2: 입자 15,000–47,000 · 드럼 D × L = **70 × 26 mm** · d **1.3 mm** · ρ 2.5 × 10³ kg/m³ · **E 1.0 × 10⁷ Pa** · ν 0.29 · γ_n 1.0 × 10⁻⁶ (단위 's⁻¹' 인쇄) · μ_s 입자–입자 0.4 · 입자–원통벽 0.5 · 입자–끝벽 **0.05** · μ_r 10⁻³ · 충전율 30–92 % · 5–35 rpm · 액량 0.5 % · θ_c 0 · γ 0–0.093 N/m · 처음 = 좌우로 갈라 넣음 (그림 2a) · 색 말고 같은 입자 · 계산 비용 4–15 CPU 시간 / 실제 1 초 (Intel 2.0 GHz Xeon) | [인쇄] p.101 · 표 2 · `txt_p3_setup_…` |
| ③ 표면장력 범위의 무차원화 (Bond · Froude) | *"This corresponds to the so-called Bond number from 0 to around 7"* — **Bond 수의 정의 · 식 · 평가 거리 미인쇄** · Fr = ω²R/g = **0.001–0.05** (5–35 rpm · R = 드럼 반지름) · 이 카드: Nase 식 26 (최대 모세관력 ÷ 무게 = 3γ/(2R²ρg)) 로는 γ 0.093 → **13.5** (원문 '≈7' 의 1.9 배) — S_min 에서의 힘 + 접촉당 다리 부피 (입자당 다리 1–6 개 가정) 로는 9.6–5.5 → '≈7' 이 그 범위 안 [카드 산술 · 가정] | [인쇄] p.101 · §3-3 |
| ④ 혼합 지수 · 혼합 시간 | **Lacey M = (σ0² − σt²)/(σ0² − σr²)** · σ0² = q(1−q) · σr² = q(1−q)/p (식 5) · 칸 = **2d × 2d** (2d–4d 감도 '아주 작음' · 그림 없음 · Deen 2010 방법과 비슷) · 칸은 가로면 격자 × 드럼 길이 전체 [판독 · 그림 2b] · **M(t) = M∞ erf(kt)** (식 6 · Finnie 2005 의 지수 꼴보다 잘 맞음 — 이 카드 재맞춤 rms 0.019–0.025 ↔ 0.034–0.046) · M = 0.95 까지 2.6–5.3 바퀴 [카드 산술] | [인쇄] p.101–102 · [카드 산술] §3-5 |
| ⑤ ★ 점착 × 회전 속도 | 40 % · 회전당 k (rev⁻¹): 마름 0.471 · 0.410 · 0.387 / γ 0.033 0.314 · 0.325 · 0.306 / γ 0.073 0.270 · 0.261 · 0.276 (5 · 15 · 35 rpm [판독 그림 6]) · 원문: 시간으로는 모두 회전이 빠를수록 빨리 섞임 · **회전당으로는 마름만 감소** (bed turnover time 이 회전에 비례해 줄지 않음 = 미끄럼) · 젖음은 *"largely unaffected"* (점착이 미끄럼을 줄인다는 '제안') | [인쇄] p.102 · [판독] 그림 6 |
| ⑥ ★ 점착 × 충전율 | 15 rpm · 10 바퀴: M · k 가 50 % 위에서 급락 · 젖음은 단조 감소 · **마름만 64 % 최저** (M 0.521 · k 0.058) → 83 % 회복 (0.782 · 0.107) → 93 % 다시 하강 · 60–70 % 에서만 젖음이 더 잘 섞임 (64 %: M 0.646 · 0.810 · k 0.067 · 0.091) [판독 그림 8] · 비혼합 핵 (60 % 위) | [인쇄] p.102–103 · [판독] 그림 8 |
| ⑦ 순환 주기 모델 식 | 식 (7) = 식 (A.6): **T = (1/π)[arccos(δ/√(x² + δ²)) + 2εx/(2δε + h² − 2h)]** · δ = δ0 − (ε/l²)x² (A.1 · 포물선 흐름층) · ⟨T⟩ = f_d/(1 − δ0²) (A.7) · σ(T) (A.8) · 핵이 있으면 ⟨T⟩ = f_d (A.9) · (A.10) · 가정 = 회전 (rolling) 영역 · 미끄럼 없음 · 흐름 안 확산 없음 · 최대 층 두께 ε = **6d (마름) · 8d (젖음)** (시뮬레이션에서 잼) · 동적 충전율 f_d 는 영상 분석 | [인쇄] p.105–107 · 식 7 · A.1–A.10 |
| ⑧ ★ 우리 드럼 위치 | Fr: 우리 0.0827 = 이 논문 최대 (0.048) 의 **1.7 배** · 주 조건 (15 rpm · 0.0088) 의 9.4 배 · 충전율: **같은 정의**로 우리 0.29–0.30 = 이 논문 **30 % 칸** · 점착: 이 논문 Bo '0–7' (모든 쌍 같음) ↔ 우리 SE–SE Bo_code 0.21 (B1) · 21.2 (B2) + 쌍 대비 (γ_AM/γ_SE 0.1 · 1) · 충돌 수: 이 논문 젖음 Co·λ² ≈ 6 × 10² – 1.4 × 10³ ↔ B2-U 0.04–58 (k 에 따라) — 이 논문의 젖음은 우리보다 훨씬 '점착 지배' 쪽 [우리 산술] | §3-10 |
| ⑨ '점착 비 기준' · 코팅 DEM | **없음** — 두 입자 = 색만 다름 · 쌍 대비 · 덮임 · 상별 뭉침 · 코팅 과정 0 | — |
| ⑩ DEM 한계 · 소성 · 2D/3D · 탈압 | 단단한 구 · 점접촉의 한계 **말 없음** — 점착 모델의 한계만 (액체 분포 모름 · S_min 맞춤 · 정적 다리 · 다리 대칭) · E 10⁷ Pa 의 근거 없음 · 소성 **논의 없음** · 3D 드럼 (끝벽 μ 0.05 로 끝벽 효과 줄임) · 가로면 분석 · 해석 모형은 2D · 탈압 없음 | §4-4 |
| ⑪ 절대값 전이 | **안 된다** — mm 단분산 · 액교 · Fr ≤ 0.05 · 좌우 처음 배치 · 이원 같은 입자 ↔ 우리 µm parcel · SJKR 쌍별 · 3 상 · Fr 0.083 · 층상.  옮길 것 = **회전당 / 시간당 k 를 같이 보는 보고 방식 · erf 시간 법칙 · 순환 주기 관측량 (평균 · 표준편차) · 충전율 규약 · '균일 점착 ↑ → k ↓' 의 방향** | §7 · §8 |

⛔ **한정어 (떼지 말 것)**: ① 계산만 (이 논문 안에 실험 0 · S_min 5 µm 와 액량 5 % 는 2011 년 논문에서 흐름 꼴 · 최대 흐름 안식각 · 무너짐 빈도에 맞춘 값) ② 입자 = 색만 다른 **같은 구** — 점착 대비 · 분리 · 덮임은 범위 밖 ③ 점착 = **액체 다리 (모세관)** — 건식 반데르발스 · JKR 이 아니다 · 같은 식을 **벽에도** (같은 γ) ④ Bond 수 정의 미인쇄 ('≈7' 은 이 카드가 다시 내면 정의에 따라 5.5–13.5) ⑤ k · M 은 **10 바퀴** 자료의 맞춤 · 반복 (시드) · 오차 막대 없음 ⑥ 회전 속도는 40 % 한 충전율에서 세 값 · 충전율은 15 rpm 한 속도에서 일곱 값 ⑦ Fr ≤ 0.05 · 회전 (구르기) 영역 가정.
⇒ **절대값 전이**: 없다 (재료 · 점착 · 크기 · Fr · 처음 배치 · 지수 정의가 모두 다르다).  **방향 · 보고 방식 · 관측량 · 규약**만 옮긴다 (§7 · §8 · §9).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-153 의 '왜' 칸)

의도 원문: *"드럼에서 점착 (액교) × 회전 속도 × 충전율을 DEM 으로 (점착은 대체로 혼합을 낮춤 · 64 % 충전에서는 마른 입자가 가장 나쁨 — 하이라이트) = 우리 드럼과 같은 꼴의 공정 축 선례 (G4 일부 후보)"* · 근거 칸 = *"1저자 11-23 업로드 (메인 세션 검색 제안 → 1저자 PDF)"* → **가리킨 카드 없음** (2 차 인용 대조 대상 없음) · 지시서 덧붙임 (꼭 뽑을 것 = 힘 모델 · 입자 · 드럼 · 표면장력 무차원화 · 혼합 지수 · 혼합 시간 · 순환 주기 식 · 회전 × 점착 표 · 우리 드럼 위치 / 우리 질문 = '점착 비 기준' · rpm 공정 축 · 코팅 과정 DEM / 공백 검사 G1–G4).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "드럼에서 점착 (액교) × 회전 속도 × 충전율을 DEM 으로" | **채움** | 세 변수를 바꾼다: *"The effects of three variables, cohesion, rotation speed and filling level, on particle mixing were investigated."* (p.101) · 점착 = 표면장력 0–0.093 N/m (액량 0.5 % 고정) · 회전 5–35 rpm · 충전율 30–92 % · 다만 **완전 요인 설계가 아니다**: γ 축 = 40 % · 15 rpm 에서 6 값 (그림 5b) · rpm 축 = 40 % 에서 3 값 × γ 3 (그림 6) · 충전율 축 = 15 rpm 에서 7 값 × γ 3 (그림 8 · 11) [판독] |
| "(점착은 대체로 혼합을 낮춤)" | **채움** | Highlights *"Interparticle cohesion in general reduces mixing performance."* · 초록 *"The presence of the capillary force in general reduced mixing performance."* · 40 % · 15 rpm: k 0.410 · 0.376 · 0.325 · 0.281 · 0.260 · 0.236 rev⁻¹ (γ 0 · 0.013 · 0.033 · 0.053 · 0.073 · 0.093 [판독 그림 5b]) = **−42 %** (단조) · 예외 = 60–70 % 충전 (마른 입자가 더 나쁨) — 조건: 계산 · 10 바퀴 맞춤 · 반복 없음 |
| "64 % 충전에서는 마른 입자가 가장 나쁨 — 하이라이트" | **채움** | Highlights *"Dry particles have the poorest mixing performance at 64% filling level."* · 그림 8 (15 rpm · 10 바퀴): 마름 M 0.521 · k 0.058 (그 마름 계열의 최저) · 같은 64 % 에서 젖음 M 0.646 (0.033) · 0.810 (0.073) · k 0.067 · 0.091 → '64 % 에서 마름이 셋 중 가장 나쁨' 과 '마름 계열에서 64 % 가 가장 나쁨' 둘 다 성립 [판독] · 그림의 충전율 점 = 0.30 · 0.40 · 0.52 · 0.64 · 0.73 · 0.83 · 0.93 [판독] (본문 마지막 값 '92 %' ↔ 그림 0.93) |
| "= 우리 드럼과 같은 꼴의 공정 축 선례" | **일부** | 같은 꼴 = 3D 회전 드럼 · 가로 혼합 · 점착 DEM · 회전 속도 축 · 충전율 규약이 우리 덱과 같다 (§3-10) · 다른 꼴 = 액교 · 단분산 mm · 이원 같은 입자 (쌍 대비 없음) · Fr ≤ 0.05 (우리 0.0827 밖) · 좌우 처음 배치 (우리 층상) · 회전 속도 축은 한 충전율 (40 %) 의 세 점뿐 |
| "(G4 일부 후보)" | **일부 (맞음)** | 공정 × 점착 지도 = 회전 3 × γ 3 (40 %) · 충전 7 × γ 3 (15 rpm) — 축이 차원값 (rpm · N/m) · 한 재료 · *"It is also unclear if the current results can be extended to other systems."* (p.104) — §0-2 G4 |
| (꼭 뽑을 것) 힘 모델 · 파단 거리 | **채움 (파단 거리 = 식만)** | 표 1 · 식 1–4 · S_rup = (1 + 0.5θ_c)V^{1/3} (p.101) — **다리 부피 V 의 값 · 접촉당 나누는 수 [미확인]** → S_rup 숫자는 원문에 없다 (입자당 다리 1–6 개 가정이면 36–66 µm = 0.028–0.051 d [카드 산술]) |
| (꼭 뽑을 것) 입자 · 드럼 · Fr · 충전율 | **채움** | 표 2 · p.101 (§3-1) |
| (꼭 뽑을 것) 표면장력 범위 (무차원화) | **일부** | γ 0–0.093 N/m = *"so-called Bond number from 0 to around 7"* — 정의 · 식 미인쇄 (§3-3) |
| (꼭 뽑을 것) 혼합 지수 정의 · 혼합 시간 | **채움** | 식 5 · 6 · 2d × 2d 칸 · k (rev⁻¹) · M∞ |
| (꼭 뽑을 것) 순환 주기 모델 식 | **채움** | 식 7 · 부록 A.1–A.10 (§3-9 · 이 카드가 다시 풀어 그림 12 이론선을 재현) |
| (꼭 뽑을 것) 회전 속도 × 점착 결과 표 | **채움 (그림만)** | 숫자는 본문 · 표에 없고 그림 6 · 5b 만 → [판독] 표 §3-6 |
| (꼭 뽑을 것) 우리 드럼 (Froude · 충전율) 위치 | **카드가 채움** | §3-10 [우리 산술] |
| (우리 질문) '점착 비 기준' (γ_AM/γ_SE · 같은 SE 탐침 AFM 힘 비) | **없음** | 모든 쌍 · 벽이 같은 γ — *"The particles have identical properties other than colours."* (p.101) |
| (우리 질문) 회전 속도 (rpm) 공정 축 | **일부** | 40 % 에서 3 rpm × γ 3 · 회전당 ↔ 시간당 k 의 구분 · 미끄럼 기전 제안 (자료 없음) |
| (우리 질문) 코팅 과정 DEM | **없음** | — |
| 가리킨 카드의 2 차 인용 값 | **해당 없음** | 근거 칸 = 1저자 업로드 (가리킨 카드 없음) · 정본 카드 가운데 이 논문을 인용한 카드도 없다 (papers/ 전수 grep 'Liu, P.Y' · 'Phys. Fluids 23' · 'ces.2012.06.015' = 0 건) |
| (덧붙임) 이 논문의 2 차 인용 ↔ 정본 카드 | **같음** | Chaudhuri 2006 *"slight increase in mixing rate at a small cohesive force (the Bond number of 0.1) … plug flow in the cascading layer"* (p.100) · *"Bond number 120 … mixing only slightly increased with increasing rotation speed"* (p.102) ↔ `chaudhuri2006` 카드 (K 0.1 = 5 바퀴 끝에서만 조금 나음 · K 120 = 빠른 회전이 회전당 조금 나음 · L160 마개 흐름) — 같은 방향 · Nase 2001 = S_min 관행 (p.101) ↔ `nase2001` 카드 L65 (최소 간격 S_o ≈ 10⁻⁶ m · 거칠기) — 같은 관행, 값은 다름 (이 논문 5 µm = 맞춤) · Lacey 1954 식 = `lacey1954` 카드 (s₀² = P(1−P) · s_r² = P(1−P)/n) 와 같음 |

⇒ **의도 대조 결과: 일부** — 점착 (액교) × 회전 속도 × 충전율 DEM · '점착은 대체로 혼합을 낮춤' · '64 % 에서 마른 입자가 가장 나쁨' 은 **채움** (원문 하이라이트 그대로 · 그림 값으로 확인) · '우리 드럼과 같은 꼴의 공정 축 선례' 는 **일부** (드럼 · 규약은 같고 점착 대비 · 크기 · Fr · 처음 배치가 다름 · rpm 축은 3 점) · G4 는 **일부** (지도는 있으나 한 재료 · 저자 스스로 이전 불명) · 우리 '점착 비' · 코팅 DEM 은 **없음**.

---

## 0-2. ★ 공백 검사 G1–G4 — 우리 믹서 논지 문장을 이 논문이 이미 했나 (정독 출력 batch_158 끝 절과 같은 판정)

| # | 우리 공백 문장 (11-23 지시) | 판정 | 근거 (쪽 · 문장) | 반례 · 일부면 우리 문장을 이렇게 좁힌다 |
|---|---|---|---|---|
| **G1** | 점착 대비를 설계 변수로 혼합 결과 (덮임 ↔ 뭉침 · 섞임 ↔ 분리) 를 예측 | **없음** | *"The particles have identical properties other than colours."* (p.101) · 모든 쌍 · 벽이 같은 표면장력 (표 1 *"also applied to particle–wall interaction"* p.100) → 대비 = 0 · 결과 변수는 혼합 속도 · 정도뿐 (덮임 · 상별 뭉침 · 분리 없음) · 점착이 *"cluster together"* 를 만든다는 말 (p.102 · 그림 4) 은 **같은 상 · 다른 상 구분 없는** 뭉침 | 좁힐 필요 없음.  가져올 것 = **대비 0 · 균일 점착의 기준선** — '모든 쌍을 같이 키우면 회전당 k 가 줄고 회전 의존이 사라진다' 를 우리 B1-U → B2-U (모든 쌍 ×100 · 대비 고정) 의 비교 기준으로 쓴다 (대비 효과는 그 위의 몫) |
| **G2** | 점착 입력을 따로 재고 (AFM · IGC · 접촉각 등) 혼합 결과를 미리 예측 | **없음** | γ 는 고른 값 (0.073 = 물 · 최대 0.093) · θ_c = 0 가정 · *"In the present study, the minimum separation distance was treated as a fitting parameter."* · *"these assumptions with S_min of 5 µm and 5% of liquid contributing to liquid bridges compared with the experimental results quite well"* (p.101 · 맞춤 대상 = 2011 년 논문의 흐름 꼴 · 최대 흐름 안식각 · 무너짐 빈도 (p.100)) · 혼합 결과의 사전 예측 없음 · 순환 주기 모형은 입력 (ε 6d · 8d · f_d) 을 **같은 시뮬레이션에서** 잰다 (p.105) | 좁힐 필요 없음.  주의점 하나를 가져온다 — **점착 모델의 맞춤 매개변수 (S_min · 다리 액량 몫) 가 '따로 잰 입력' 과 섞이면 G2 의 '미리 예측' 이 무너진다** → 우리 SJKR CED 도 맞춤 없이 W (AFM) 에서 바로 내는지 등록 문서에 적는다 |
| **G3** | 회전 속도 최적을 입자 수준 맞교환 (덩어리 풀림 ↔ 벽 부착 손실 등) 으로 설명 | **일부** | 회전 의존의 **입자 수준 기전을 제안**은 한다: 마름 = *"the bed turn-over time does not proportionally decrease with increasing rotation speed"* (미끄럼) · 젖음 = *"suggesting that the cohesion reduces the slipping of particles against the drum so the bed turn-over time also decreases with increasing drum speed"* (p.102) — 그러나 ① 미끄럼 · 회전 시간 자료 없음 (제안) ② **최적 rpm 없음** (3 점 · 단조) ③ 덩어리 풀림 · 벽 부착 손실의 맞교환 없음 (벽 점착은 미끄럼을 줄여 '돕는' 쪽으로만 언급) | 우리 문장을 이렇게 좁힌다: *"회전 속도에 따른 **회전당** 혼합 속도 변화를 벽 미끄럼 · 회전 시간으로 읽는 제안 (Liu 2013) 은 있으나 자료 · 최적 · 맞교환은 없다 — 우리는 rpm 최적을 덩어리 크기 · 벽 접촉 몫 · 미끄럼 속도 (덤프 관측량) 로 입자 수준에서 보인다"* |
| **G4** | 공정 × 재료 상태도 (회전 세기 × 점착 · Bond 수 등) 가 다른 재료로 옮겨 감 | **일부** | 공정 × 점착 지도 = rpm 3 × γ 3 (그림 6) · 충전 7 × γ 3 (그림 8 · 11) — 축이 차원값 (rpm · N/m · Bond 는 범위만 언급) · 한 재료 (1.3 mm · 액량 0.5 %) · *"It is also unclear if the current results can be extended to other systems."* (p.104) · 순환 주기 모형은 *"a general method to predict the mixing performance at different operational conditions"* (p.106) 로 제안되나 입력 (ε · f_d) 이 같은 시뮬레이션 측정 | 우리 문장을 이렇게 좁힌다: *"공정 (rpm) × 균일 점착 세기 지도 (차원 축 · 한 재료) 는 선례 (Liu 2013) 가 있다 — 우리 몫은 축을 무차원 (Bo · Co · Fr) 으로 · 점착 **대비** 를 셋째 축으로 · 다른 재료 · 크기 (실입경 ↔ parcel) 로 옮겨 가는지를 보이는 것"* |

---

## 1. 한 줄 요약

**같은 구를 색만 바꿔 좌우로 넣은 3D 회전 드럼 (70 × 26 mm) 에 정적 액체 다리 점착을 켜고, 표면장력 · 회전 속도 · 충전율을 바꿔 가로면 Lacey 지수를 잰 DEM 9 쪽 논문.**  혼합은 erf(kt) 로 진행하고, 점착은 대체로 k 를 줄이며 (회전당으로는 마른 입자만 rpm 에 민감), 마른 입자의 64 % 충전 이상 (최저) 을 순환 주기 표준편차의 최소로 설명한 뒤, Ding 2002 의 회전 영역 모형을 흐름선별 순환 주기로 넓혀 평균 · 표준편차를 예측한다.

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| P.Y. Liu · R.Y. Yang\* · A.B. Yu (UNSW · Laboratory for Simulation and Modelling of Particulate Systems) | *Chem. Eng. Sci.* 86 (2013) 99–107 · 9 쪽 (부록 A 포함) | 10.1016/j.ces.2012.06.015 (p.99 아래 인쇄) | 지름 1.3 mm 같은 구 (액량을 *"the volume of glass beads"* 로 정의 → 유리구 계 · ρ 2500 · E 1.0 × 10⁷ Pa · ν 0.29) · 물 같은 액체 (μ 0.001 Pa s · γ 0–0.093 N/m · θ 0) · SE · AM · 전극 재료 없음 | **DEM + 해석 모형** (실험 0 · 압밀 0) |

> ★ **계보**: 같은 그룹 (UNSW · Yu) 의 in-house DEM (Yang · Zou · Yu 2000 PRE 62 · 정본 `chandratilleke2010` 의 '표 1 = Yu 그룹 힘 · 토크 식' 과 같은 계열) · 점착 모델 = Liu · Yang · Yu 2011 *Phys. Fluids* 23, 013304 (실험 대조 · S_min 맞춤 — 정본 카드 없음) · 액교 힘 = Rabinovich 2005 + Lambert 2008 · 파단 = Lian · Thornton · Adams 1993 · 점성 = Pitois 2000 · Goldman 1967 · 흐름층 · 혼합 = Khakhar 1997 · Ottino & Khakhar 2000 · Ding 2002 (모형 바탕) · 점착 혼합 선행 = Shinbrot 1999 · McCarthy 2003 · Chaudhuri 2006.

---

## 3. 핵심 수치 · 식 (★ 전부 쪽 · 표지 병기)

### 3-1. 입자 · 드럼 · 공정 (표 2 · p.101 · `tab_2.png` · `txt_p3_setup_…`)
| 항목 | 값 | 표지 |
|---|---|---|
| 입자 수 | 15,000–47,000 (충전율 따라) — 카드 산술 (충전 밀도 0.6 · 드럼 100.06 cm³ · 입자 1.150 mm³) 30 % 15,660 · 40 % 20,880 · 92 % 48,020 | [인쇄] · [카드 산술] |
| 드럼 | **D × L = 70 × 26 mm** · 원통 + 끝벽 둘 · D/d 53.8 · L/d 20.0 [카드 산술] | [인쇄] |
| 입자 | 지름 **1.3 mm** · ρ 2.5 × 10³ kg/m³ · E **1.0 × 10⁷ Pa** · ν 0.29 · 모두 같은 성질 · 색만 다른 두 종 (노랑 · 빨강) | [인쇄] p.101 |
| 감쇠 · 마찰 | γ_n 1.0 × 10⁻⁶ (단위 's⁻¹' 인쇄 — 표 1 감쇠항의 차원으로는 s 여야 함 [카드 산술 · §3-11]) · μ_s 입자–입자 0.4 · 입자–원통벽 0.5 · **입자–끝벽 0.05** (*"To minimise the effect of end wall"* · Taberlet 2006) · μ_r 10⁻³ (무차원 — 토크 팔 μ_rR_i = 0.65 µm [카드 산술]) | [인쇄] |
| 액체 | 부피 액량 V_f **0.5 %** (*"the liquid volume to the volume of glass beads"*) · θ_c **0°** · γ **0.0–0.093 N/m** (그림 5b 점 = 0 · 0.013 · 0.033 · 0.053 · 0.073 · 0.093 [판독]) · 점성 0.001 Pa s (점성력 계산에만) | [인쇄] · [판독] |
| 회전 · Fr | **5–35 rpm** · *"Froude number (Fr = ω²R/g) ranging from 0.001 to 0.05"* — 카드 산술 (R 35 mm): 5 rpm 9.8 × 10⁻⁴ · 15 rpm **8.8 × 10⁻³** · 35 rpm 0.048 · ω/ω_c 0.031 · 0.094 · 0.219 | [인쇄] · [카드 산술] |
| 충전율 | *"defined as the bulk volume of dry based packed bed (with packing density of 0.6) to the drum volume when the drum is in a static state"* · 30–92 % (그림 점 0.30 · 0.40 · 0.52 · 0.64 · 0.73 · 0.83 · 0.93 [판독]) · 주 조건 **40 %** | [인쇄] p.101 |
| 처음 상태 | *"initially separated side by side (Fig. 2a)"* — 좌 · 우 (세로 경계) | [인쇄] p.101 · 그림 2 |
| 계산 비용 | *"it took about 4–15 CPU hours to simulate 1 s real time on an Intel 2.0 GHz Xeon PC"* → 10 바퀴 = 5 rpm 480–1,800 · 15 rpm **160–600** · 35 rpm 69–257 CPU 시간 [카드 산술 · 1 초당 비용이 rpm 과 무관하다고 가정] | [인쇄] · [카드 산술] |
| 시간 간격 · 기록 간격 · 반복 (시드) | 원문에 없음 (Rayleigh 시간 5.6 × 10⁻⁵ s — E 10⁷ · ν 0.29 · ρ 2500 · R 0.65 mm [카드 산술]) | [미확인] |

### 3-2. 힘 모델 (식 1–4 · 표 1 · p.100–101 · `eq_01`–`eq_04` · `eq_t1_*` · `tab_1.png`)
| 식 | 내용 | 표지 |
|---|---|---|
| (1) | m_i dv_i/dt = Σ_j (F^n_ij + F^s_ij + F^cap_ij) + m_i g | [인쇄] p.100 |
| (2) | I_i dω_i/dt = Σ_j (R_i × F^s_ij − μ_r R_i ‖F^n_ij‖ ω̂_i) — R_i = 중심 → 접점 벡터 · μ_r = 구름 마찰 계수 | [인쇄] p.100 |
| 표 1 법선 | F^n_ij = [(2/3)(Y/(1 − σ̃²))√R̄ ξ_n^{3/2} − γ_n (Y/(1 − σ̃²))√R̄ √ξ_n (v_ij · n̂_ij)] n̂_ij — 같은 재료 두 구의 Hertz (= (4/3)E\*√R\* δ^{3/2} with E\* = Y/(2(1 − σ̃²)) [카드 산술]) + 겹침 의존 비선형 감쇠 (Langston 1995 · Brilliantov 1996 · Yang 2000) | [인쇄] p.100 |
| 표 1 접선 | F^s_ij = −sgn(ξ_s) μ_s ‖F^n_ij‖ [1 − (1 − min(ξ_s, ξ_s,max)/ξ_s,max)^{3/2}] · ξ_s,max = μ_s[(2 − σ̃)/2(1 − σ̃)]ξ_n | [인쇄] |
| 표 1 모세관 | **F^cap_ij = 4πR̄γcosθ_c / (1 + 1/[√(1 + V/(πR̄S²)) − 1]) n̂_ij** — *"To explicitly link the capillary force and the volume of liquid bridge instead of the half filling angle β (Fig. 1), the model proposed by Rabinovich et al. (2005) and later revised by Lambert et al. (2008) was adopted."* · R̄ = R_iR_j/(R_i + R_j) · S = 떨어진 거리 · V = 다리 부피 · S → 0 이면 4πR̄γcosθ = 같은 구에서 2πRγ (Nase 의 최대 모세관력과 같음 [카드 산술]) · **벽 = 반지름 ∞** (R̄ → R_i · 같은 γ 면 벽 최대 힘 = 입자–입자의 2 배 [카드 산술]) | [인쇄] p.100 |
| (3) | F^n_vis = 6πμR̄²(v_n/S)(1 − 1/√(1 + V/πR̄S²))² (Pitois 2000) — 계산만 | [인쇄] p.101 |
| (4) | F^t_vis = 6πμR̄v_t[8/15 ln(R̄/S) + 0.9588] (Goldman 1967) — 계산만 | [인쇄] p.101 |
| 점성력을 버린 근거 | *"at the relative collision velocity of 5 cm/s, the energy loss in the normal direction due to liquid viscosity was less than 5% of total energy loss and the tangential viscous force was less than 2% of sliding friction"* (d 1.3 mm · γ 0.073 N/m · μ 0.001 Pa s) | [인쇄] p.101 |
| 액체 분포 가정 | *"(i) the liquid was distributed evenly to individual particles and equally divided to contact points between particles; (ii) only part of liquid contributed to the formation of liquid bridge; and (iii) a minimum separation distance S_min was adopted below which the capillary force is set to be a constant value."* · **S_min = 5 µm · 다리에 든 액량 5 %** (2011 년 논문의 실험 대조로 고름) | [인쇄] p.101 |
| 파단 거리 | **S_rup = (1 + 0.5θ_c)V^{1/3}** (Lian 1993) — θ_c 0 이면 V^{1/3} · V 의 값 · 접촉당 나누는 수 [미확인] → 입자 액량 5.75 × 10⁻¹² m³ 의 5 % (2.88 × 10⁻¹³ m³) 를 다리 1 · 2 · 3 · 6 개로 나누면 S_rup 66 · 52 · 46 · 36 µm (0.051 · 0.040 · 0.035 · 0.028 d) [카드 산술 · 가정] | [인쇄] · [카드 산술] |
| 무시한 것 | 동적 (점성) 다리 · 다리 변형 (*"always assumed the liquid bridge to be symmetric against the line contacting the centres of two particles"*) | [인쇄] p.100–101 |

### 3-3. 무차원 수 — Bond · Froude · (이 카드) 충돌 수
- 원문: *"The interparticle cohesion was controlled by varying the liquid surface tension from 0.0 to 0.093 N/m while the volumetric liquid content … was fixed at 0.5% for all the cases. This corresponds to the so-called Bond number from 0 to around 7."* (p.101) — **정의 · 식 · 힘을 잰 거리 미인쇄**.
- 같은 V · S 에서 모세관력 ∝ γ 이므로 원문 척도는 Bo ≈ 7γ/0.093: γ 0.013 · 0.033 · 0.053 · 0.073 → **0.98 · 2.48 · 3.99 · 5.49** [카드 산술 · '≈7' 이 근사라 ± 표기 필요].
- Nase 2001 식 26 (Bo_g = 최대 모세관력 2πRγ ÷ 무게 = 3γ/(2R²ρg)) 로 다시 내면 γ 0.013 · 0.033 · 0.053 · 0.073 · 0.093 → **1.88 · 4.78 · 7.67 · 10.57 · 13.46** (입자 무게 2.82 × 10⁻⁵ N) [카드 산술] — 원문 '≈7' 의 1.9 배.
- '≈7' 을 재현하는 한 가지 읽기 [카드 산술 · 가정]: 힘을 S_min (5 µm) 에서 · 다리 부피를 입자 액량의 5 % ÷ 입자당 다리 수 Z 로 두면 γ 0.093 의 Bo = 9.62 (Z 1) · 8.24 (2) · 7.29 (3) · 5.53 (6) — **정의가 다르면 같은 계의 Bo 가 2 배 넘게 달라진다** (우리 Bo_code = SJKR 평형 떼는 힘 ÷ 자기 무게 와 직접 견주지 않는다).
- **충돌 수** (이 카드 · Nase 식 34 꼴 Co·λ² = (8/3)·Bo_g·g·k⁴/(R ω²) · R = **입자** 반지름 0.65 mm (Fr 의 드럼 반지름과 다름) · k = 흐름층 최대 두께 ÷ 반 현 길이 · 젖음 k = 8d/L = 0.301 (40 %) · λ² 미정 · `khakhar1999` 카드 §3-9 와 같은 식) [카드 산술]: 15 rpm 에서 γ 0.033 → **639** · 0.073 → **1,413** (Nase 식 29 꼴이면 절반 320 · 707) · k 를 고정하면 ∝ 1/ω² → 5 rpm ×9 · 35 rpm ×0.18 (γ 0.073: 1.27 × 10⁴ · 260) → **이 논문의 젖은 조건 전부 Co·λ² ≫ 1** (λ² ~ 1 이면 점착 지배 영역) — 젖은 입자의 회전당 k 가 rpm 에 둔감한 것과 같은 방향 [카드 추론].

### 3-4. 흐름 영역 (그림 3 · p.101–102 · `fig_3a` · `fig_3b` · `txt_p3_p4_flow_regime_…`)
| γ (N/m) | 원문 | 각도 (t 0.5–2.5 바퀴) [판독 · 벡터 꺾은선] |
|---|---|---|
| 0 | 연속 흐름 (빠른 흐름층 + 고체처럼 도는 바닥) · *"The dynamic angle of repose is about 30°."* | 평균 30.3° · sd 0.6 · 28.7–31.9 |
| 0.033 | 연속 흐름 유지 · *"an increased angle of repose (~37°)"* · 표면이 더 볼록 · 흐름층 두꺼워짐 (Brewster 2009 와 맞음) | 평균 37.1° · sd 1.3 · 33.6–40.2 |
| 0.073 | **무너짐 (avalanching) 영역** · 각이 강하게 진동 · 무너지기 전 = 고체처럼 회전 · 무너질 때 = 마개 흐름 (plug flow · Rognon 2008) | 25.6–54.7° 진동 · 평균 41.9 · 봉우리 17 개 / 2 바퀴 = **≈8.5 회 / 바퀴 (≈2.1 Hz at 15 rpm)** [카드 산술] |
- 조건 = 40 % · 15 rpm · 그림 3b 속도장 축척 = 0.2 m/s 화살표 · 이 카드의 질량 보존 어림 (흐름층 평균 속도 u = ωL/(2k) · L = 반 현 34.6 mm · 마름 k 0.226) u ≈ 0.12 m/s · 표면 ≈ 0.24 m/s [카드 산술 · `khakhar1999` 식 5–7] — 축척 화살표와 같은 자릿수.

### 3-5. 혼합 지수 · 시간 법칙 · 점착 (식 5–6 · 그림 4–5 · p.101–102)
- **식 (5)** Lacey: M = (σ0² − σt²)/(σ0² − σr²) · σ0² = q(1 − q) (완전 분리) · σr² = q(1 − q)/p (완전 혼합 · p = 칸당 평균 입자 수) · 칸 = 2d × 2d · *"we carried out the sensitivity test using different cell sizes from 2d to 4d. The results (not shown here) indicated that the effect is quite minimal"* (p.101) · 그림 2b 의 칸은 가로선만 → 칸 = 2d × 2d × 드럼 길이 L (가로면 혼합만 봄) [판독] → 칸당 입자 ≈ 92 (충전 0.6 이면 4 d² × 20 d × 0.6 / (π/6 d³) [카드 산술]).
- **식 (6)** M(t) = M∞ erf(kt) · *"Finnie et al. (2005) used an exponential function … Our work, however, shows that such relationship is better fitted by an error function"* (p.102) · 40 % 에서 M∞ = 1 (모든 γ).
- 이 카드의 재맞춤 (그림 5a 마커 41 개 × 3 · M∞ 자유) [판독 · 카드 산술]: erf → k **0.408 · 0.324 · 0.261** (M∞ 0.969 · 0.962 · 0.955 · rms 0.019 · 0.025 · 0.025) ↔ 1 − e^{−kt} → k 0.639 · 0.491 · 0.378 (rms 0.034 · 0.044 · 0.046) — erf 가 rms 1.4–1.8 배 작다 · erf 의 k 는 그림 5b 값 (0.410 · 0.325 · 0.260) 과 같다.
- 그림 5a 마커 (γ 0 · 0.033 · 0.073) [판독]: 1 바퀴 M 0.408 · 0.283 · 0.216 · **2 바퀴 0.764 · 0.647 · 0.496** · 3 바퀴 0.882 · 0.830 · 0.733 · 5 바퀴 0.951 · 0.933 · 0.904 · 10 바퀴 0.979 · 0.970 · 0.961.
- **그림 5b k(γ)** (40 % · 15 rpm) [판독]: γ 0 · 0.013 · 0.033 · 0.053 · 0.073 · 0.093 → **0.410 · 0.376 · 0.325 · 0.281 · 0.260 · 0.236 rev⁻¹** (비 1 · 0.92 · 0.79 · 0.69 · 0.63 · 0.58) · *"the mixing rate k decreases with the surface tension monotonously"* · *"The present study did not observe the increase in mixing rate with moderate cohesion for filling level below 50%"* (McCarthy 2003 과 다름 — *"different capillary force model and did not provide the simulation conditions"*).
- M = 0.95 까지 (erf(kt) = 0.95 → kt = 1.386) [카드 산술]: 40 % 3.38 · 4.27 · 5.31 바퀴 / 30 % (그림 8b k) 2.62 · 3.97 · 5.06 바퀴.
- 그림 4 (1 · 5 바퀴 단면): 1 바퀴 뒤 모든 경우 서로 스며드는 꼴 · γ 0.073 은 *"the particles cluster together in similar paces as the cohesion restricts the diffusion of particles"* (같은 상 · 다른 상 구분 없음 — Chaudhuri 2006 의 층 · 덩어리 꼴과 같다고 인용).

### 3-6. ★ 회전 속도 × 점착 (그림 6 · p.102 · 40 % · `fig_6.png` · `txt_p4_rotation_speed_…`)
| rpm (Fr) | γ 0 | γ 0.033 | γ 0.073 |
|---|---|---|---|
| 5 (9.8 × 10⁻⁴) | **0.471** rev⁻¹ · 0.039 s⁻¹ · M 0.95 까지 35 s | 0.314 · 0.026 · 53 s | 0.270 · 0.023 · 62 s |
| 15 (8.8 × 10⁻³) | 0.410 · 0.102 · 14 s | 0.325 · 0.081 · 17 s | 0.261 · 0.065 · 21 s |
| 35 (0.048) | **0.387** · 0.226 · 6.1 s | 0.306 · 0.178 · 7.8 s | 0.276 · 0.161 · 8.6 s |
- rev⁻¹ = [판독 그림 6] · s⁻¹ = k × rpm/60 · 시간 = 1.386/k_s [카드 산술].
- 원문: *"particle mixing is faster with increasing rotation speed for both dry and wet particles"* (시간) · *"When the mixing rate is represented in terms of the number of revolutions … it actually decreases with increasing rotation speed for the dry particles … because the bed turn-over time does not proportionally decrease with increasing rotation speed"* · *"For the wet particles, the mixing rate is largely unaffected by the rotation speed, suggesting that the cohesion reduces the slipping of particles against the drum so the bed turn-over time also decreases with increasing drum speed"* (p.102).
- 크기 [카드 산술]: 마름 Fr ×49 (5 → 35 rpm) 에 회전당 k **−18 %** (2 바퀴 M 으로는 erf(2k) 0.817 → 0.726 · **−0.09**) · 젖음은 5 → 35 rpm 에 0.033 −3 % · 0.073 +2 % (사이 15 rpm 에서 각각 +3 · −3 % — 이웃 rpm 사이 최대 6 %) · 2 바퀴 erf 환산 M 의 rpm 간 폭 0.029 (0.033: 0.626 · 0.642 · 0.612) · 0.025 (0.073: 0.556 · 0.540 · 0.565) — 마름 폭 0.09 의 ⅓ 이하 · 단조 아님 — 점착이 클수록 '회전당 rpm 무관' 에 가깝다.
- ⚠ 반복 · 오차 없음 · 세 점 · 40 % 한 충전율 · 미끄럼 · 회전 시간은 **재지 않았다** (기전 = 제안).

### 3-7. ★ 충전율 × 점착 (그림 7–8 · p.102–103 · 15 rpm · 10 바퀴 · `fig_8a` · `fig_8b`)
| f (그림 점) | M γ 0 | M 0.033 | M 0.073 | k γ 0 | k 0.033 | k 0.073 |
|---|---|---|---|---|---|---|
| 0.30 | 0.976 | 0.971 | 0.966 | **0.529** | 0.349 | 0.274 |
| 0.40 | 0.977 | 0.973 | 0.963 | 0.410 | 0.325 | 0.263 |
| 0.52 | 0.966 | 0.954 | 0.946 | 0.243 | 0.218 | 0.179 |
| **0.64** | **0.521** | 0.646 | 0.810 | **0.058** | 0.067 | 0.091 |
| 0.73 | 0.717 | 0.564 | 0.480 | 0.093 | 0.059 | 0.050 |
| 0.83 | 0.782 | 0.546 | 0.320 | 0.107 | 0.050 | 0.033 |
| 0.93 | 0.631 | 0.247 | 0.067 | 0.058 | 0.021 | 0.011 |
- 전부 [판독 · 벡터 마커] · 원문: 50 % 아래는 모두 M ≈ 1 (*"the dry particles can reach better mixed states than the wet particles"*) · 50 % 위 급락 = 흐름층 몫 감소 + **비혼합 핵** (Gray 2001 · 그림 7 의 64 · 83 % 단면) · *"while the mixing index for the wet particles decreases monotonously, the mixing index of dry particles decreases and reaches a minimum at f=64% beyond which the mixing index increases until f=83% and then decreases again at f=92%"* · *"for filling level between 60% and 70%, the wet particles actually have better mixing performance"* (p.103).
- 선행과 다른 점 (원문): 가장 나쁜 충전이 50 % (Hogg & Fuerstenau 1972 · Figueroa 2010 · Metcalfe 1995 의 모형) 가 아니라 64 % (Dury 1999 는 크기 다른 입자에서 ≈65 %) · 적당한 점착이 혼합을 돕는다는 McCarthy 2003 과 달리 단조 감소 (60–70 % 만 예외).
- ⚠ 그림 8b 의 y 축 맨 위 글자 '0.6' 이 0.55 자리에 있다 (다른 간격의 절반) — 판독은 일정한 0.1 간격 눈금선으로 했다 · 그래픽 초록 왼쪽 그림도 같다.
- ⚠ 마지막 충전율: 본문 · 표 2 = 92 % ↔ 그림 점 0.93 [판독].

### 3-8. 기전 — 반지름 변위 · 순환 주기 (그림 9–11 · p.103–104 · `fig_10a` · `fig_10b` · `fig_11a` · `fig_11b`)
- 그림 9: 한 입자의 5 바퀴 궤적 — *"the particle in all cases follows a uniform circular motion in the solid bed and only changes its motion streamlines when it passes through the rapid flow layer"* · 점착이 커질수록 궤적이 모인다 (흐름층 확산 감소).
- **반지름 변위 Δr** = 바닥의 이등분선을 연속 두 번 지날 때 반지름 위치 차 · 분포 = 가우스 (그림 10a) · 점착 ↑ → 좁아짐 · 봉우리 P(0) 0.175 · 0.233 · 0.329 (γ 0 · 0.033 · 0.073) [판독] → 정규 분포면 σ_Δr **2.28 · 1.71 · 1.21 d** · 분산 비 1 : 0.56 : 0.28 [카드 산술 · 정규 가정].
- **순환 주기 T** = *"the number of drum revolutions required for a particle to complete a circulation"* (그림 10b) · 왼쪽으로 치우침 · 젖을수록 길고 넓음 (*"the capillary force reduces the flowability of wet particles in the rapid flow layer"*) · 봉우리 칸 T **0.55 · 0.60 · 0.65 rev** (P 7.34 · 6.23 · 5.73 · 칸 폭 0.05 rev) [판독].
- 그림 11 (15 rpm) [판독]:

| f | ⟨T⟩ γ 0 | ⟨T⟩ 0.033 | ⟨T⟩ 0.073 | σ(T) γ 0 | σ(T) 0.033 | σ(T) 0.073 |
|---|---|---|---|---|---|---|
| 0.30 | 0.480 | 0.519 | 0.560 | 0.068 | 0.070 | 0.127 |
| 0.40 | 0.505 | 0.539 | 0.577 | 0.063 | 0.065 | 0.103 |
| 0.52 | 0.571 | 0.604 | 0.640 | 0.051 | 0.048 | 0.076 |
| **0.64** | 0.651 | 0.688 | 0.722 | **0.020** | 0.028 | 0.039 |
| 0.73 | 0.734 | 0.773 | 0.800 | 0.044 | 0.040 | 0.028 |
| 0.83 | 0.822 | 0.860 | 0.885 | 0.066 | 0.047 | 0.031 |
| 0.93 | 0.912 | 0.943 | 0.958 | 0.059 | 0.028 | 0.008 |
- 원문의 읽기: ⟨T⟩ ↑ (충전 · 점착 — *"probably due to the cohesion induced bed dilation"* Alexander 2006) → 느림 · *"smaller standard deviation means particles moving with similar pace which is unfavourable to mixing"* → 마름 σ(T) 최소 (64 %) = 마름 혼합 최저 · 64 % 에서 σ(T) 가 점착과 함께 커짐 = 젖음이 더 나음 · 0.073 의 큰 σ(T) 는 무너짐 / 안 무너짐 두 상태 탓이고 마개 흐름 안 입자는 같은 속도라 혼합은 나쁨 · 92 % 에서 모두 다시 작아짐 = *"a total un-mixing when the drum is fully filled"* (p.104).
- 저자 스스로: *"it is not clear why filling level at 64% has the smallest standard deviation. It is also unclear if the current results can be extended to other systems."* (p.104).

### 3-9. ★ 순환 주기 모형 (식 7 · 부록 A · 그림 12–13 · p.105–107) — 원문 + 이 카드의 재풀이
- 가정 (부록 A): *"the flow is in the rolling regime with non-slipping and no diffusive motions inside the flow. Furthermore, the rapid flow layer is assumed to be a parabolic shape"* (Nakagawa 1993 · Khakhar 1997 · Shinbrot 1999) · 드럼 반지름 1 · 원점 = 드럼 중심 (그림 13).
- 식: δ = δ0 − (ε/l²)x² (A.1 · ε = 최대 층 두께 · l = 반 현 · δ0 = 가장 깊은 층 경계의 y) · dQ = (v·n̂)ds (A.2) · 바닥 속도 v_x = −ωδ · v_y = ωx · dQ = 2πx(2εδ/l² − 1)dx (A.3 · 시간 = 바퀴 → ω 무관) · dA = L_f dδ − L_s dr (A.4 · L_f = −2x · L_s = 2r arccos(δ/r)) · (A.5) · **T = dA/dQ** (A.6 = 식 7) · ⟨T⟩ = f_d/(1 − δ0²) (A.7) · σ(T) (A.8 · Q = π(1 − δ0²)) · δ0 < 0 (층 전체가 중심 위) 이면 비혼합 핵 (드럼과 같이 돈다고 가정) → ⟨T⟩ = f_d (A.9) · (A.10) · 동적 충전율 f_d = (φ − sinφcosφ)/π · h = 1 − cos φ (φ = 반 충전 각).
- 원문 입력 · 결과: ε = **6d (마름) · 8d (젖음 0.033)** *"determined from the simulations"* · f_d = 정상 흐름 영상 분석 · ⟨T⟩ *"quite well"* · σ(T) *"at least qualitatively"* · 모형 최소 **f_d ≈ 67 % (마름) · 74 % (젖음)** · 둘째 봉우리 **84 %** · 낮은 충전에서 σ(T) 과대 (*"the model does not consider the diffusive motion of particles which is more prominent at low filling levels"*) · 핵이 있으면 ⟨T⟩ 가 층 두께와 무관 (p.105–106).
- 시뮬레이션 점의 동적 충전율 [판독 그림 12]: 마름 0.332 · 0.431 · 0.543 · 0.657 · 0.747 · 0.839 · 0.922 · 젖음 0.361 · 0.455 · 0.578 · 0.689 · 0.783 · 0.871 · 0.953 (정지 0.30 … 0.93 에 대응 · 젖음이 더 부풂).
- **이 카드의 재풀이** [카드 산술 · 식 A.6–A.10 수치 적분 (x 4,000–20,000 칸) · ε/R = 6 × 1.3/35 = 0.2229 · 8 × 1.3/35 = 0.2971 · δ0 = cos φ + ε (A.1 의 양 끝 x = ±l 에서 층 두께 0 → 자유 표면 = y = 1 − h)]:

| 양 | 마름 (ε 6d) | 젖음 (ε 8d) | 그림 12 이론선 [판독] |
|---|---|---|---|
| σ(T) 최소 · 위치 | **0.0360 @ f_d 0.675** (δ0 −0.056) | **0.0412 @ 0.745** (δ0 −0.098) | 0.0360 @ 0.674 · 0.0412 @ 0.740 |
| 둘째 봉우리 | 0.0633 @ 0.836 | 0.0488 @ 0.850 | 0.0634 @ 0.834 · 0.0490 @ 0.848 |
| 왼쪽 끝 (f_d 0.298) | 0.1240 | 0.1405 | 0.1238 · 0.1403 |
| ⟨T⟩ @ f_d 0.40 | 0.468 | 0.504 | 0.4676 · 0.5038 |
| 비혼합 핵이 생기는 f_d (δ0 = 0 · cos φ\* = −ε) | **0.641** | **0.686** | — |
- ⇒ 이론선은 **재현된다** — 단 핵이 있을 때 (A.10) 의 가중을 **전체 유량 π** (= Q + 핵 넓이 πδ0²) 로 나눠야 한다: 인쇄 그대로 1/Q (Q = π(1 − δ0²)) 로 나누면 둘째 봉우리가 0.0675 @ f_d 0.851 (마름) · 0.0512 @ 0.861 (젖음) 로 커지고 오른쪽으로 옮겨 그림 (0.0634 @ 0.834 · 0.0490 @ 0.848 [판독]) 과 맞지 않는다 (핵이 없는 낮은 충전은 두 정규화가 같고 · 최소는 거의 같다 — 0.0360 ↔ 0.0361 @ 0.675 · 0.0412 ↔ 0.0414 @ 0.745 · 0.744) [카드 산술 · §3-11].
- ⇒ **σ(T) 최소 = 흐름층 가장 깊은 점이 드럼 중심을 막 지난 자리** (핵 시작 f_d 0.641 · 0.686 의 바로 뒤) [카드 산술 · 해석] — 원문이 *"not clear why … 64%"* 라고 남긴 자리의 기하 읽기.  같은 식에서 cos φ\* = −ε ≤ 0 이므로 **f_d ≤ 0.5 면 어떤 층 두께에서도 핵이 없다** [카드 산술].
- 모형 ↔ 시뮬레이션 [카드 산술 · 시뮬레이션 점의 f_d 에서 모형 재계산]: ⟨T⟩ 낮은 충전에서 모형이 작음 (마름 f_d 0.33 · 0.43 −8.9 · −4.1 % · 젖음 0.36 · 0.45 −5.1 · −2.5 %) · f_d ≥ 0.66 에서 0 – +2 % · σ(T) 모형 / 시뮬레이션 = 마름 1.82–1.93 · 젖음 1.99–2.40 (f_d ≤ 0.69 — **최소 자리 포함: 최소의 위치는 맞고 값은 ≈2 배** (모형 0.036 · 0.041 ↔ 시뮬레이션 0.020 · 0.028)) ↔ 0.85–1.18 (f_d ≥ 0.75) — 원문 *"consistently over-estimates"* 는 '낮은 충전' 이라 적었지만 과대는 최소 자리까지 이어진다.

### 3-10. ★ 우리 드럼 믹서에 대입 [우리 산술 · 카드 추론]
우리 값 (읽기만): `docs/reviews/mixer_b2_u_development_20261122/README.md` (Bo_SE B1-U 0.21244 · B2-U 21.244 · γ_AM/γ_SE 0.1 · γ_W/γ_SE 0.00256 · B1-U 한 팔 실측 25 시간 7 분 43 초 · 48 시간 상한) · B2-U `deck_meta.json` (`docs/reviews/mixer_first8_launch_preparation_20261106/planned_assets/PRECAL_R1_B2_U/` — 76.6765 rpm · 주기 0.7825 s · 2 바퀴 · CGF 151.4 · 법칙 W_ij = 2√(γ_iγ_j)) · `scripts/make_mixer_deck.py` (FR_ANCHOR 0.0827 · `plan(…, fill=0.30, pack=0.60)` · 현재 덱 = `plan(100000, cgf=151.4, stiffen_se=20., dens_gen='lab20261014')` (fill 기본)) · `docs/reviews/mixer_b1_pair_return_20261122/README.md` (B1 개발 판독 M) · 기하 · 입자 수 = 정본 `khakhar1999` 카드 §3-9 의 덱 판독 (39 각형 꼭짓점 반지름 12.583 mm · 축 길이 5.033 mm · 고체 440 mm³ · 드럼 2,493 mm³ · SE / AM_S / AM_P 99,158 · 708 · 134 개).

| 항목 | 이 논문 | 우리 B1 · B2 | 비 · 뜻 |
|---|---|---|---|
| Fr = ω²R/g | 9.8 × 10⁻⁴ · **8.8 × 10⁻³** · 0.048 | **0.0827** (76.68 rpm · R 12.583 mm) | 이 논문 최대의 **1.7 배** · 주 조건의 9.4 배 — 측정 범위 밖 |
| ω/ω_c | 0.031–0.219 | 0.288 | |
| 충전율 (**같은 정의** — 정지 충전 밀도 0.6 의 겉보기 부피 ÷ 드럼) | 30–92 % (주 40 %) | 0.177 / 0.6 = **0.29** · 덱 계획값 0.30 | 이 논문 **최저 칸 (30 %)** — 모든 계열이 M∞ ≈ 1 · 비혼합 핵 없음 (§3-9 · f ≤ 0.5) |
| 입자 · 크기 | 단분산 1.3 mm · 이원 같은 입자 · D/d 53.8 · L/d 20 | parcel SE 0.151 · AM_S 0.606 · AM_P 1.363 mm (실입경 1 · 4 · 9 µm) · 2R/d_SE ≈ 166 · L/d_SE 33 (AM_P 18.5 · 3.7) | 다분산 3 상 · 크기 대비 9 배 |
| 점착 | 액교 · 모든 쌍 · 벽 같은 γ · Bo '0–≈7' (Nase 정의 0–13.5) | SJKR 쌍별 · Bo_SE 0.21 (B1) · 21.2 (B2) · γ_AM/γ_SE 0.1 (U) · 1 (C) · 벽 0.00256 | 우리 = 대비 + 매우 약한 벽 (이 논문 = 대비 0 · 벽 = 입자 2 배 힘) |
| 충돌 수 Co·λ² (Nase 식 34 꼴 · λ² 미정) | 젖음 15 rpm 639 (0.033) · 1,413 (0.073) · 5 rpm ×9 · 35 rpm ×0.18 | B2-U SE–SE 0.040–58 (k 0.024–0.15 · 0.1 이면 11) · B1-U ≤ 0.58 (`khakhar1999` 카드 §3-9) | 이 논문의 젖음은 **우리보다 1–2 자릿수 더 점착 지배** — 우리 B2-U 는 Co ≈ 1 근처 (k 에 따라) |
| 흐름층 두께 ÷ 반 현 (k) | 마름 0.226 · 젖음 0.301 (40 % · 15 rpm · 6d · 8d) · 30 % 0.235 · 0.314 [카드 산술] | 질량 보존상 ≳ 0.1 추정 (`khakhar1999` §3-9 · 덤프 측정 전) | 이 논문 (L/d 26.6 · Fr 8.8 × 10⁻³) 이 Khakhar 그림 4 (0.024–0.069) 보다 3–12 배 두꺼움 = 작은 L/d 쪽 |
| 순환 주기 (모형 · f_d 0.30 · k 0.05–0.31) | 30 % 마름 시뮬레이션 ⟨T⟩ 0.480 · σ 0.068 | 모형 ⟨T⟩ 0.347–0.484 rev · σ(T) 0.080–0.140 (모형은 f_d ≤ 0.69 에서 σ 를 1.8–2.4 배 과대 · 그림 12b) [카드 산술] | 2 바퀴 = 흐름층 통과 ≈4.1–5.8 회 [카드 산술 · 모형 가정] |
| 처음 배치 | 좌우 (세로 경계) | 층상 (가로 경계) | 다름 — 같은 k 라도 M(t) 가 다를 수 있다 (원문 다루지 않음) |
| 회전 수 · 지수 | 10 바퀴 · Lacey 이론 분모 · 2d × 2d × L 기둥 칸 (가로면만) | 2 바퀴 · M = (초기 분산 − 관측)/(초기 − E0 기준 분산) · 3D 격자 16×16×4 · 12×12×3 · 8×8×2 | 정의 다름 — 숫자 직접 대조 금지 |
| 회전 뒤 M (크기 감각만) | 2 바퀴 — 40 %: 0.764 · 0.647 · 0.496 (γ 0 · 0.033 · 0.073 [판독]) · 30 %: erf(2k) 0.865 · 0.676 · 0.562 [카드 산술] | 2 회전 런의 bin1 100 프레임 평균 (개발 판독 `mixer_b1_pair_return_20261122`): N0 (점착 0) 0.860–0.958 · U 0.837–0.949 · C 0.846–0.968 (세 격자) | **크기 감각만** (지수 정의 · 처음 배치 · 시점이 다르다) — 30 % 마름 (0.87) 과 우리 N0 (0.86–0.96) 이 같은 자릿수 |
- **회전 속도 (rpm) 공정 축 설계 — Froude 두세 수준** [카드 산술 · 같은 dt · 회전당 step ∝ 1/rpm · B1-U 실측 25.13 시간 (층상 충전 · 정착 포함 전체) 을 통째로 rpm 비례 — 충전 · 정착 몫이 고정이면 느린 rpm 은 이 어림보다 짧고 (상한 쪽) 빠른 rpm 은 길다 (하한 쪽)]:

| Fr | 우리 rpm | 이 논문 대응 | 회전당 step (76.68 rpm 대비) | 2 바퀴 벽시계 어림 |
|---|---|---|---|---|
| 0.0088 | 25.0 | 15 rpm (주 조건) | ×3.07 | ≈77 시간 (**48 시간 상한 초과** → 나눠 돌리기 · 재개 필요) |
| 0.048 | 58.4 | 35 rpm (최대) | ×1.31 | ≈33 시간 |
| 0.0827 | 76.7 | 밖 (1.7 배) | ×1 | 25.1 시간 (B1-U 실측) |
| 0.3 | 146 | 밖 | ×0.53 | ≈13 시간 (구르기 영역 가정 깨질 수 있음 · 이 논문 모형 범위 밖) |
- ⇒ 이 논문 결과로 본 기대 크기 [카드 추론]: 회전당 k 의 rpm 의존은 **점착이 약할수록 크다** (마름 −18 % / Fr ×49 · 젖음 평평) → 우리 B1-U (Co ≪ 1 · '마름' 쪽) 는 Fr 0.0088 ↔ 0.0827 에서 2 바퀴 M 차가 ≈0.05–0.1 정도일 수 있고 (이 논문 마름 erf 환산 −0.09 / Fr ×49) — 이는 B1 개발 판독의 프레임 간 SD (U 0.073–0.088 · C 0.060–0.078) 와 같은 크기라 **여러 프레임 · 시드 없이는 못 가른다** · B2-U (Co ≈ 1 근처) 는 rpm 이 Co 를 ×9.4 (Fr 0.0088 ↔ 0.0827 · k 고정) 바꿔 영역 경계를 넘을 수 있다 — 이 논문 (Co ≫ 1 전부) 은 그 경계를 시험하지 않았다.
- ⇒ **균일 점착 축 (B1-U → B2-U · 모든 쌍 ×100 · 대비 고정)** 은 이 논문 그림 5b (γ 0 → 0.093 · 모든 쌍) 와 같은 꼴 — 방향 = 회전당 k ↓ (−42 % · Bo 0 → ≈7–13) · 크기 · 문턱은 옮기지 않는다 (액교 ↔ SJKR · Co 영역 다름 · 처음 배치 다름).

### 3-11. 원문 안 어긋남 (§11 에 다시)
① 초록 *"The Lacey mixing index showed an exponential increase with mixing time"* ↔ 본문 · 결론 = erf 가 지수 꼴보다 잘 맞음 (p.102 · p.106) ② Bond 수 '≈7' 의 정의 미인쇄 (Nase 식이면 13.5) ③ 표 2 γ_n 단위 's⁻¹' ↔ 표 1 감쇠항 [N] = γ_n × (Y/(1−σ̃²))√R̄√ξ_n v 이므로 γ_n 의 단위는 s [카드 산술 · 차원] ④ 그림 8b · 그래픽 초록 y 축 맨 위 '0.6' 이 0.55 자리 ⑤ 마지막 충전율 본문 92 % ↔ 그림 0.93 ⑥ 부록 *"l=2h−h²"* ↔ 반지름 1 원의 반 현 l² = 2h − h² (식 A.6 의 분모 2δε + h² − 2h = 2δε − l² 가 제곱을 요구) [카드 산술] ⑦ 식 A.10 의 앞 계수 1/Q (Q = π(1 − δ0²)) ↔ 그림 12b 이론선은 전체 유량 π 로 나눈 값과 맞음 [카드 산술 · §3-9] ⑧ n̂ = (dδ/dx − 1)/√(1 + (dδ/dx)²) — 벡터 (dδ/dx, −1) 을 스칼라처럼 인쇄 ⑨ '64 % 가 왜 최소인지 모른다' (p.104) ↔ 같은 논문 모형이 최소를 재현 — 원문은 기하 (핵 시작) 로 잇지 않았다 (이 카드 §3-9 의 해석).

---

## 4. ★ 방법 — 모델 · 측정 사슬 · 계산

### 4-1. 계산 (in-house DEM · p.100–101)
| 항목 | 내용 | 표지 |
|---|---|---|
| 코드 | *"An in-house developed DEM program as detailed in our previous papers (Yang et al., 2000; Liu et al., 2011)"* | [인쇄] |
| 접촉 | 탄성 (Hertz) + 겹침 의존 비선형 감쇠 · μ_s 상한 3/2 승 접선 · 구름 마찰 (μ_r R_i‖F^n‖) — 표 1 · 식 (2) | [인쇄] |
| 점착 | 정적 펜듈러 액교 · 다리 부피 V 로 쓴 모세관력 (Rabinovich 2005 / Lambert 2008) · S < S_min (5 µm) 이면 상수 · S > S_rup 이면 끊김 · 벽 = R → ∞ · 점성 다리 무시 | [인쇄] |
| 기하 · 경계 | 원통 드럼 + 끝벽 둘 (끝벽 마찰 0.05 — 끝벽 효과 줄이기) · 회전 = 정해진 속도 | [인쇄] |
| 처음 상태 | 좌우로 갈라 채운 뒤 회전 시작 (채우는 절차 · 정착 시간 [미확인]) | [인쇄] · [미확인] |
| 출력 | 가로면 Lacey M(t) (2d × 2d 칸) · 정상 흐름 속도장 · 표면 각 · 입자 궤적 · 이등분선 통과 위치 → Δr · T | [인쇄] |
| 맞춘 값 | **S_min 5 µm · 다리 액량 몫 5 %** — 2011 년 논문 (흐름 꼴 · 최대 흐름 안식각 · 무너짐 빈도) 에 맞춤 · E · 감쇠 · 마찰 · μ_r 의 출처 [미확인] | [인쇄] p.100–101 |
| 비용 | 4–15 CPU 시간 / 1 초 (Intel 2.0 GHz Xeon) · 15,000–47,000 개 | [인쇄] |

### 4-2. 측정 사슬 (재구성)
좌우 채움 → 회전 (5–35 rpm) → 매 시각 가로면 칸 (2d × 2d × L) 마다 한 색 몫 → 분산 σt² → Lacey M (식 5) → 10 바퀴 M(t) 에 erf 맞춤 (k · M∞) / 정상 흐름에서: 입자가 바닥 이등분선을 지날 때마다 반지름 기록 → Δr 분포 (가우스) · 연속 통과 사이 바퀴 수 → T 분포 · ⟨T⟩ · σ(T) / 영상 → 동적 충전율 f_d · 최대 층 두께 ε → 식 (7) · A.7–A.10.

### 4-3. 해석 모형 (부록 A)
§3-9 — Ding 2002 의 '바닥 회전 시간' 모형 (평균만) 을 흐름선별 순환 주기 T(x) 로 넓혀 분포의 평균 · 표준편차를 낸다 · 입력 = ε · f_d (둘 다 같은 시뮬레이션에서 잼) · 맞춤 값 0 · 회전 (구르기) · 미끄럼 없음 · 확산 없음 · 2D (가로면).

### 4-4. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM 한계 진술 = 단단한 구 · 점접촉 자체에 대해서는 말 없음** — 점착 모델의 한계만 적는다: *"We also note that, while the capillary force for two particles is well established, its calculation is much more complicated for a moving bed due to lack of the knowledge of particle wetting and liquid distribution."* (p.101) · *"In the present study, the minimum separation distance was treated as a fitting parameter."* (p.101) · *"The current study considered only the static capillary force while the dynamic effect of liquid bridge due to moving particles was neglected."* (p.100) · *"Note that we did not consider the deformation of liquid bridge in the simulation and always assumed the liquid bridge to be symmetric against the line contacting the centres of two particles."* (p.101).  **E = 1.0 × 10⁷ Pa** 의 근거 · 실제 재료값 대비 연화 여부는 쓰지 않는다 (같은 그룹 `chandratilleke2010` 은 '계산 시간 때문' 10⁹ → 2.16 × 10⁶ Pa 라고 적었다).  이 E 로 겹침은 작다 — 최대 모세관력 (γ 0.093 · 3.8 × 10⁻⁴ N) 에서 2.0 µm (0.16 % d) · 40 % 바닥 무게 (깊이 29.5 mm · p·d² 7.3 × 10⁻⁴ N) 에서 3.2 µm (0.24 % d) [카드 산술 · 표 1 Hertz 식].
- **(ii) 소성 · 큰 변형 = 논의 없음** (혼합 흐름 · 겹침 < 0.3 % d · 압밀 없음).
- **(iii) 차원**: 계산 = **3D** (드럼 길이 26 mm = 20 d · 끝벽 둘) · 분석 = 가로면 (칸이 길이 전체를 덮음) · 해석 모형 = 2D (가로면 흐름선) · 2D ↔ 3D 전이 진술 없음 — 끝벽 효과는 마찰 0.05 로 줄였다고만 (*"To minimise the effect of end wall in the current study, the particle–end wall sliding friction is reduced to 0.05, as suggested by Taberlet et al. (2006)"* p.100).
- **(iv) 탈압**: 해당 없음.

### 4-5. 기법 미니 용어집
- **가로 (transverse) 혼합** = 드럼 축에 수직인 면 안에서의 혼합 (축 방향 혼합은 느린 자기 확산 — p.99).
- **Lacey 지수** = (완전 분리 분산 − 지금 분산) ÷ (완전 분리 분산 − 무작위 혼합 분산) — 0 (분리) → 1 (무작위 혼합).
- **오차 함수 erf(x)** = 2/√π ∫₀ˣ e^{−s²} ds — erf(kt) 는 처음에 거의 직선 (기울기 2k/√π) 으로 오르고 지수 꼴보다 빨리 포화.
- **흐름층 (rapid flow layer)** = 자유 표면 아래 얇게 흘러내리는 층 · 그 아래 바닥은 드럼과 함께 강체 회전.
- **순환 주기 T** = 한 입자가 바닥을 돌아 흐름층을 지나 다시 같은 자리로 오는 데 걸리는 바퀴 수.
- **비혼합 핵 (non-mixing core)** = 충전이 높아 흐름층이 닿지 않는 중심 부분 — 드럼과 같이 돌 뿐 섞이지 않는다.
- **동적 충전율 f_d** = 정상 흐름 중 바닥 (고체 부분) 부피 ÷ 드럼 부피 (부풂 포함) ↔ 정지 충전율 f (충전 밀도 0.6 의 겉보기 부피 ÷ 드럼).
- **Bond 수** = 점착력 ÷ 무게 (정의는 논문마다 다름 — 최대 힘 · 특정 거리의 힘 · 떼는 힘) · **충돌 수 Co** = 점착력 ÷ Bagnold 충돌력 (Nase 2001).
- **S_min** = 모세관력을 상수로 자르는 최소 간격 (겹침 · 0 거리에서 힘 · 점성 발산을 막는 장치 — 맞춤 값).

---

## 5. Figure set ★ (크롭 75 장 = `litdb/figures/liu2013_wet_cohesive_particles_transverse_mixing_rotating_drum_circulation_period/`)
| Fig | 내용 | 우리 활용 |
|---|---|---|
| GA (`fig_GA`) | 그래픽 초록 — 그림 8b (k vs f) + 그림 12b (σ(T) vs f_d · 이론선) | — |
| 1 | 힘 도식 (접촉 i–j · 액교 i–k · S · θ_c · β) | 액교 기호 |
| 2 (a · b) | 처음 상태 (좌우) + Lacey 칸 격자 (끝면 · 옆면 — 옆면은 가로선만 = 길이 전체 칸) | 칸 정의 · 처음 배치 차 |
| 3a · 3b | ★ 표면 각 시계열 (30° · 37° · 무너짐 진동) · 속도장 (흐름층 · 무너짐 전 / 중) | 영역 판별 (구르기 ↔ 무너짐) · 우리 덤프에서 같은 시계열 |
| 4 | 1 · 5 바퀴 혼합 단면 × γ 셋 | 정성 (점착 = 뭉침 · 늦은 혼합) |
| 5a · 5b | ★ M(t) + erf 맞춤 · k(γ) | 균일 점착 축 (B1 → B2) 의 방향 · 시간 법칙 |
| 6 | ★ k (rev⁻¹) vs rpm × γ | rpm 공정 축 (회전당 / 시간당) |
| 7 | 10 바퀴 단면 × 충전율 (30 · 40 · 64 · 83 %) — 비혼합 핵 | 우리 30 % = 핵 없음 |
| 8a · 8b | ★ M · k vs 충전율 × γ | 우리 충전율 자리 (30 %) |
| 9 | 한 입자 5 바퀴 궤적 (흐름선 · 시간 색) | 우리 덤프로 같은 궤적 |
| 10a · 10b | Δr 분포 (가우스) · T 분포 | 확산 · 대류 분해 관측량 |
| 11a · 11b | ★ ⟨T⟩ · σ(T) vs 충전율 × γ | 순환 주기 관측량 |
| 12a · 12b | ★ 모형 ↔ 시뮬레이션 (f_d) | 이 카드가 재현 (§3-9) |
| 13 | 모형 좌표 (중심 o · 현 · 층 경계 δ(x) · ε · h · φ · dA · ds) | 식 A.1–A.10 의 기호 |
| 표 1 (`tab_1`) | 힘 식 (법선 · 접선 · 모세관) + 기호 | 액교 DEM 식 원본 |
| 표 2 (`tab_2`) | 매개변수 | §3-1 |
| 식 크롭 28 장 | `eq_01`–`eq_07` · `eq_A1`–`eq_A10` · `eq_inline_a`–`g` (Fr · S_rup · erf · f_d · l 인쇄 그대로 · n̂ · L_f L_s) · `eq_t1_1`–`4` (표 1 줄) | 보고서 믹서 절에 붙일 식 |
| 근거 문단 19 장 | `txt_p1_…` (하이라이트 · 초록) · `txt_p2_*` (점착 혼합 선행 · 힘 모델 · 점성 무시) · `txt_p3_*` (액체 가정 · 설정 · Lacey · 흐름 영역) · `txt_p4_*` (erf · rpm · 충전) · `txt_p5_*` · `txt_p6_*` (기전 · 64 % · 이전 불명) · `txt_p7_*` (식 7 · 6d · 8d · 모형 최소) · `txt_p8_*` (결론 · 부록 가정) | 원문 인용용 |

## 6. Post-processing ★
- **무엇을**: Lacey M (2d × 2d · 칸 크기 감도 2d–4d) · erf 맞춤 (k · M∞) · 표면 각 시계열 · 정상 흐름 속도장 · 단일 입자 궤적 · Δr · T 분포 (가우스 맞춤) · ⟨T⟩ · σ(T) · 영상으로 f_d · ε · 해석 모형.
- **안 한 것**: 반복 (시드) · 오차 막대 · 축 방향 혼합 · 처음 배치 바꾸기 · rpm × 충전율 교차 · 미끄럼 속도 · 벽 접촉 · 덩어리 크기 · 실험 대조 · 칸 감도 그림.
- **이 카드의 후처리**: 벡터 그림 11 개 패널의 마커 · 곡선 꼭짓점을 눈금선 맞춤으로 판독 (357 행) · erf ↔ 지수 재맞춤 · 시간 · 회전 단위 환산 · Bond 수 정의 비교 · 다리 부피 가정별 S_rup · Bo · 충돌 수 · 질량 보존 흐름층 속도 · **부록 모형 수치 재풀이 (이론선 재현 · 정규화 판정 · 핵 시작 f_d)** · 우리 드럼 대입 · rpm 축 비용.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 리포 문서 출처를 병기)

### 7-1. 비교표 (믹서 드럼 DEM)
| 항목 | 이 논문 | 우리 (믹서 B 덱) | 같음 / 다름 · 왜 |
|---|---|---|---|
| 코드 · 접촉 | in-house · Hertz + 비선형 감쇠 · 3/2 승 접선 · 구름 μ_r 10⁻³ (무차원) | LIGGGHTS Hertz–Mindlin · SJKR 점착 · 구름 (CDT) | 같은 '탄성 Hertz + 점착 항' 계열 · 점착 법칙 다름 |
| 점착 | 액교 (부피 V · S_min 5 µm 맞춤 · 파단 V^{1/3}) · 모든 쌍 · 벽 같은 γ | SJKR CED (쌍별 · W_ij = 2√(γ_iγ_j)) · 벽 γ_W/γ_SE 0.00256 | 이 논문 = 대비 0 · 거리 있는 힘 / 우리 = 대비 · 접촉 중에만 |
| 영률 | 1.0 × 10⁷ Pa (근거 없음) | 상별 연화 · SE 경화 ×20 (첫 8 덱) | 둘 다 실제 재료값 아님 |
| 입자 | 1.3 mm 단분산 · 이원 같은 입자 | 3 상 parcel (CGF 151.4) | 다름 |
| 드럼 | 원통 70 × 26 mm · 끝벽 마찰 0.05 | 39 각형 (R 12.583 mm) · 축 5.033 mm · 끝판 같이 회전 | 둘 다 짧은 3D · 우리가 L/d_AM_P 3.7 로 훨씬 짧다 |
| Fr · 충전율 · 바퀴 | 0.001–0.048 · 30–92 % · 10 | 0.0827 · 0.29–0.30 (같은 정의) · 2 | Fr 밖 · 충전율 같은 칸 |
| 처음 배치 | 좌우 | 층상 | 다름 |
| 지수 | Lacey 이론 분모 · 2d × 2d × L | E0 기준 분모 · 3D 격자 셋 | 다름 |
| 관측량 | M(t) · k · ⟨T⟩ · σ(T) · Δr | M · SE 군집 몫 · AM 접촉 SE · 초기 AM 보존율 | 이 논문의 순환 주기 · Δr 은 우리 판독에 없음 |

### 7-2. ★ 세 카드의 틀에 대조 (지시서 · Bond 수 · 충돌 수 · 흐르는 층)
- **Bond 수 (`nase2001`)**: 정지 · 호퍼는 Bo_g ≈ 1 에서 급변 · 드럼 동적 각은 Bo_g 에 완만 (그 카드 ③ · 임계 회전의 10 %) ↔ 이 논문 15 rpm (ω/ω_c **0.094** = Nase 드럼과 거의 같은 상대 회전) 에서 Bo_g (Nase 정의) 0 → 4.8 → 10.6 에 각 30.3 → 37.1° → **무너짐 영역 (25.6–54.7°)** [판독] — 이 사이 (Bo_g 4.8–10.6) 에서 흐름 영역이 바뀐다 (연속 → 무너짐) · 무너짐의 마개 흐름 = Chaudhuri 2006 의 강한 점착 기전과 같은 말 [카드 추론].
- **충돌 수 (`nase2001` · `li2006`)**: 이 논문 젖은 조건 Co·λ² ≈ 59–1.3 × 10⁴ (γ 0.033 · 0.073 × 5–35 rpm · k 고정 · 식 29 / 34) — 모두 ≫ 1 → 점착 지배 → **회전당 혼합이 rpm 에 둔감** (그림 6) 은 Li06 의 '느린 영역 (정적 상태도)' 과 같은 쪽 [카드 추론] · 마른 계 (Co = 0) 에서 회전당 k 가 rpm 에 따라 줄어드는 것은 Khakhar 영 모형 (회전당 불변) 에서 벗어난 몫 = 저자는 미끄럼으로 읽음.
- **흐르는 층 (`khakhar1999`)**: 이 논문 최대 층 두께 6d · 8d (40 % · 15 rpm) → k = ε/L **0.226 · 0.301** [카드 산술] · Khakhar 그림 4 (Fr 1.6–6.2 × 10⁻⁴ · L/d 39–245) 의 0.024–0.069 보다 3–12 배 → 우리 드럼 'k ≳ 0.1' (그 카드 §3-9 추정) 과 같은 방향의 DEM 근거 (작은 L/d · 큰 Fr) [카드 추론] · 점착이 층을 두껍게 (6d → 8d · Brewster 2009 와 같음) · 이 논문 모형 = Khakhar 의 반 채움 틀을 **아무 충전율 + 비혼합 핵** 으로 넓힌 판 (Ding 2002 경유) · 회전당 결과가 ω 와 무관한 꼴 (식 A.3 · *"time is in unit of number of revolutions so that the flow rate is made independent of ω"*) 은 Khakhar 영 모형과 같다 → rpm 은 ε(Fr) · f_d (부풂) · 미끄럼으로만 들어온다.

### 7-3. 랩 기준과 나란히
- 이 논문은 압밀 · 기공 · 진밀도가 없다 → 랩 표준 (순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³) 과 **나란히 놓을 숫자가 없다**.

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 혼합 공정 (회전 드럼) 의 DEM 쪽 — 점착 · 회전 · 충전율 → 혼합 속도 · 정도 · 입자 운동 관측량 (Δr · T).
- **없는 것**: 압밀 · 수송 · MPM · 실험 · 점착 대비 · 다상 · 코팅 과정 ⇒ 우리 Ⓒ 코팅 활물질 믹싱 (혼합 상태 → 압밀 → 수송) 의 **첫 단계 (혼합) 의 방법 · 관측량** 만 준다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문은 압밀 계획 바깥 (흐름 밖: Ⓒ 믹서) 이다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | 없음 (기공 없음) — 다만 **판정 기준을 결과 전에 적는 꼴** 의 반면교사: 점착 모델 매개변수 (S_min) 를 실험에 맞춘 뒤 같은 모델로 결론 (맞춘 값과 결과의 분리 표지 없음) | — |
| **단계 1–3** (3D 메모리 · 2D MPM 코드 · 2D 접촉 표현 비교) | 없음 | — |
| **단계 4–6** (3D 순수 SE · 복합 압밀 · 탈압) | 없음 | — |
| **단계 7** (형상 · 피복 · 수송) | 없음 (혼합 상태만 — 압밀 · 수송으로 넘기지 않음) | — |
| **후보 D0** (지금 DEM) | 탄성 Hertz + 점착의 **혼합 DEM 계보** (같은 Yu 그룹) · E 10⁷ Pa 처럼 근거 없는 연화가 흔하다는 사례 · 겹침 < 0.3 % d [카드 산술] | 연화 정당화 · 압밀 거동 없음 |
| **후보 A′-0 · A · A′ · B · C · C′ · M0** | 없음 | — |
| **U0–U6** | 단위 시험 꼴 한 가지: 버리는 항 (점성력) 을 **같은 조건에서 계산해 크기를 적고** 버린다 (5 cm/s · < 5 % · < 2 %) — 우리 '무시한 항' 기록 방식 | 다물체 접촉 · 해상도 시험 없음 |
| **R1–R7** | 없음 (압밀 조건) | — |
| **결과 전 대조 항목** (흐름 밖: Ⓒ 믹서) | ① **균일 점착 ↑ → 회전당 k ↓** (그림 5b · −42 % · 방향만) ↔ B2-U vs B1-U 의 2 바퀴 M ② **rpm ↑ → 회전당 k: 약점착 감소 · 강점착 평평** (그림 6) ↔ rpm 팔 ③ **충전 ≤ 50 % = 모든 계열 M∞ ≈ 1 · 비혼합 핵 없음** (그림 8 · 모형) ↔ 우리 30 % ④ M(t) 시간 법칙 = erf (그림 5a) ↔ 우리 M(t) 곡선 꼴 | 크기 · 문턱 전이 금지 (액교 · mm · Fr ≤ 0.05 · 좌우 처음 배치 · Lacey 정의 다름) |

- **재료 · 차원 · 조건 차이**: 유리 같은 1.3 mm 단분산 · 물 액교 ↔ 우리 NCM · LPSCl parcel (실입경 1–9 µm) · SJKR · 3D 같음 · 가로면 분석 ↔ 우리 3D 격자 · Fr 0.001–0.05 ↔ 0.0827 · 10 ↔ 2 바퀴.

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **rpm 팔은 회전당 k 와 시간당 k 를 둘 다 보고한다** — 이 논문에서 시간당은 모두 빨라지고 회전당은 약점착만 줄어든다 (그림 6) · 같은 2 바퀴 비교는 '회전당' 이다 → rpm 팔의 결론 문장에 단위를 붙인다 (Ⓒ 믹서 rpm 축 · G3).
2. **rpm 축 수준 = Fr 0.0088 · 0.048 (이 논문 조건과 겹침) + 0.0827** — 문헌 대조가 되는 두 점을 넣되 25 rpm 팔은 2 바퀴에 ≈77 시간 (48 시간 상한 초과 → 재개 계획 필요) [카드 산술] · 효과 크기 (2 바퀴 M 차 ≈0.05–0.1) 가 프레임 간 SD 와 비슷하므로 **같은 rpm 에서 여러 프레임 · 시드** 로 오차를 먼저 잰다.
3. **M(t) 에 erf 와 지수 꼴을 함께 맞춰 시간 법칙을 보고한다** — erf 는 처음 직선 · 빠른 포화 (확산형) · 이 논문에서 rms 1.4–1.8 배 작음 → 우리 층상 처음 배치에서도 같은지가 '확산 지배인가' 의 단서 (Lacey 1954 의 확산 ↔ 대류 구분과 이어짐).
4. **순환 주기 · Δr 를 덤프에서 낸다** — 바닥 이등분선 통과 기록만으로 ⟨T⟩ · σ(T) · Δr 분포가 나온다 · 점착 대비 (U ↔ C) 가 SE 의 흐름층 통과 빈도 · 반지름 확산을 어떻게 바꾸는지 = '혼합이 왜 다른가' 를 입자 수준으로 쪼개는 관측량 (G3 의 덩어리 · 미끄럼 관측량과 함께).
5. **충전율 규약을 이 논문과 같다고 명시한다** — 우리 0.29–0.30 (정지 충전 밀도 0.6) = 이 논문 30 % 칸 · 모형상 f ≤ 0.5 면 비혼합 핵이 없다 → 64 % 이상 같은 고충전 이상은 우리 결과 해석에 끌어오지 않는다.
6. **Bond 수 정의를 문장마다 적는다** — 같은 계에서 최대 힘 · S_min 힘 · 다리 부피 가정에 따라 5.5–13.5 (×2.4) → 우리 Bo_code (SJKR 떼는 힘 ÷ 자기 무게) 와 문헌 Bo 를 견줄 때 정의 칸 필수.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In a DEM rotating-drum study with a static liquid-bridge capillary force on all contacts, the per-revolution mixing rate of the Lacey index decreased monotonically from 0.41 to 0.24 rev⁻¹ as the surface tension rose from 0 to 0.093 N/m (40 % filling, 15 rpm; digitized from Liu, Yang & Yu, Chem. Eng. Sci. 86 (2013) 99–107, Fig. 5b)."
- "Per drum revolution, mixing of dry particles slowed with rotation speed (5 → 35 rpm, Fr 0.001 → 0.05) whereas wet particles were largely insensitive; in physical time all cases mixed faster (Liu et al. 2013, Fig. 6)."
- "Dry particles mixed worst at 64 % filling, where the standard deviation of the circulation period was smallest; only between 60 % and 70 % filling did cohesion improve mixing (Liu et al. 2013)."
- 국문: *"회전당 혼합 속도는 점착이 약한 계에서만 회전 속도에 따라 줄었고 (마름 −18 % · Fr 0.001 → 0.048), 액교 점착 계는 평평했다 (Liu 2013 판독)."*
- 국문: *"Liu 2013 의 Bond 수 '0–약 7' 은 정의가 인쇄되지 않았다 — 최대 모세관력 기준이면 0–13.5 (이 카드 산술)."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **실험 0** — 혼합 결과는 전부 계산 · 점착 모델 매개변수 (S_min 5 µm · 액량 몫 5 %) 는 2011 년 논문에서 흐름 꼴 · 각 · 무너짐 빈도에 맞춘 값.
2. **점착 대비 없음** — 두 입자가 색만 다르다 · 모든 쌍 · 벽이 같은 γ → '점착 비' · 분리 · 덮임 주장 불가.
3. **Bond 수 정의 미인쇄** — '≈7' 은 정의에 따라 5.5–13.5 [카드 산술].
4. **반복 · 오차 없음** — k · M · T 는 한 런 · 10 바퀴 맞춤 · rpm 3 점 · 충전 7 점.
5. **교차 설계 아님** — rpm 은 40 % 에서만 · 충전율은 15 rpm 에서만 · γ 6 값은 40 % · 15 rpm 에서만.
6. **회전 기전 = 제안** — 미끄럼 · 바닥 회전 시간 자료 없음.
7. **초록 '지수 증가' ↔ 본문 · 결론 'erf'** (§3-11 ①).
8. **그림 8b · 초록 그림 축 글자 '0.6' 위치 오류 · 충전 92 ↔ 0.93** (④ ⑤).
9. **부록 식 인쇄 오류 둘** — 'l = 2h − h²' (제곱 빠짐) · A.10 의 1/Q 정규화 (그림과 안 맞음) [카드 산술].
10. **γ_n 단위 's⁻¹'** — 감쇠항 차원으로는 s.
11. **E = 1.0 × 10⁷ Pa · 감쇠 · 마찰 출처 없음** — 액교 힘과 접촉 강성의 비가 연화로 바뀌는지 논의 없음.
12. **모형 입력이 같은 시뮬레이션 측정** (ε 6d · 8d · f_d) → '일반 예측 방법' 은 그 입력을 따로 낼 때만 예측 · 모형 σ(T) 값은 f_d ≤ 0.69 에서 시뮬레이션의 1.8–2.4 배 (최소의 **위치** 만 맞음) [카드 산술].
13. **처음 배치 하나 (좌우)** — 층상 · 다른 배치에서 같은 k 인지 미시험.
14. **Fr ≤ 0.05 · 구르기 영역 가정** — 우리 0.0827 은 밖.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|
| Liu, P.Y., Yang, R.Y., Yu, A.B., 2011. Dynamics of wet particles in rotating drums: effect of liquid surface tension. Phys. Fluids 23, 013304. | 점착 모델 맞춤 (S_min 5 µm · 액량 5 %) 의 실험 대조 · 흐름 꼴 · 무너짐 빈도 (G2 · m) | 없음 (papers/ grep 'Phys. Fluids 23' 0) |
| McCarthy, J.J., 2003. Micro-modeling of cohesive mixing processes. Powder Technol. 138, 63–67. | '적당한 점착이 혼합을 돕는다 (< 50 %)' — 이 논문과 반대 (G1 · G3) | 없음 |
| Ding, Y.L., Forster, R., Seville, J.P.K., Parker, D.J., 2002. Granular motion in rotating drums: bed turnover time and slumping-rolling transition. Powder Technol. 124, 18–27. | 바닥 회전 시간 · 모형의 바탕 · 무너짐–구르기 전이 (rpm 축 · G3) | 없음 |
| Finnie, G.J., Kruyt, N.P., Ye, M., Zeilstra, C., Kuipers, J.A.M., 2005. Longitudinal and transverse mixing in rotary kilns: A discrete element method approach. Chem. Eng. Sci. 60, 4083–4091. | 지수 시간 법칙 · 회전 · 충전에 따른 혼합 속도 감소 (DEM · rpm 축) | 없음 |
| Rabinovich, Y.I., Esayanur, M.S., Moudgil, B.M., 2005. Capillary forces between two spheres with a fixed volume liquid bridge: theory and experiment. Langmuir 21, 10992–10997. | 쓴 모세관력 식의 원전 (다리 부피 형) | 없음 |
| Lambert, P., Chau, A., Delchambre, A., Regnier, S., 2008. Comparison between two capillary forces models. Langmuir 24, 3157–3163. | 그 식의 수정판 | 없음 |
| Khakhar, D.V., McCarthy, J.J., Shinbrot, T., Ottino, J.M., 1997. Transverse flow and mixing of granular materials in a rotating cylinder. Phys. Fluids 9, 31–43. | 흐름층 모형 (포물선) — 같은 그룹 1999 판 = 정본 `khakhar1999` | 없음 (1997 판) |
| Chaudhuri, B., Mehrotra, A., Muzzio, F.J., Tomassone, M.S., 2006. Cohesive effects in powder mixing in a tumbling blender. Powder Technol. 165, 105–114. | Bond 0.1 · 120 · 마개 흐름 | `chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed` |
| Nase, S.T., Vargas, W.L., Abatan, A.A., McCarthy, J.J., 2001. Discrete characterization tools for cohesive granular material. Powder Technol. 116, 214–223. | S_min 관행 · Bond / 충돌 수 | `nase2001_granular_bond_collision_number_wet_cohesion` |
| Lacey, P.M.C., 1954. Developments in the theory of particle mixing. J. Appl. Chem. 4, 257–268. | 식 5 | `lacey1954_particle_mixing_theory_index` |
| Shinbrot, T., Alexander, A., Muzzio, F.J., 1999. Spontaneous chaotic granular mixing. Nature 397, 675–678. | 점착이 혼합을 돕는 stick-slip | 없음 (wishlist 에 이미 있음) |
| Figueroa, I., Vargas, W.L., McCarthy, J.J., 2010. Mixing and heat conduction in rotating tumblers. Chem. Eng. Sci. 65, 1045–1054. | 50 % 최저 · 회전 따라 빨라짐 (같은 McCarthy 그룹 · 정본 `figueroa2009` 와 다른 논문) | 없음 |
| Deen, N.C., Willem, G., Sander, G., Kuipers, J.A.M., 2010. Numerical analysis of solids mixing in pressurized fluidized beds. Ind. Eng. Chem. Res. 49, 5246–5253. | Lacey 칸 크기 감도 방법 | [미확인 — 정본 카드 여부 미판정] |

---

## [미확인] 목록
- Bond 수의 정의 · 식 · 힘을 잰 거리 · 다리 부피 V 의 값 · 접촉당 나누는 수 → 파단 거리 숫자.
- 시간 간격 · 기록 간격 · 채우는 절차 · 정착 시간 · 반복 수 · 칸당 입자 수 p 의 값.
- E · 감쇠 · 마찰 · μ_r 의 출처 · 연화 여부.
- 미끄럼 속도 · 바닥 회전 시간 (rpm 기전의 자료).
- 흐름층 두께 ε 를 잰 방법 (6d · 8d 의 정의 · 오차) · rpm 별 ε.
- 이 논문 안의 실험 (없음) · 2011 년 맞춤의 세부 (그 논문).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-24)
- 서지: 후보 표 N-153 · 지시서 메모 (P.Y. Liu, R.Y. Yang, A.B. Yu · 제목 · Chem. Eng. Sci. 86 (2013) 99–107 · DOI 10.1016/j.ces.2012.06.015) = 원문 첫 쪽과 같음 (DOI 는 p.99 아래 'http://dx.doi.org/10.1016/j.ces.2012.06.015' 인쇄) · 교신 = R.Y. Yang · 날짜 4 개 · 키워드 6 개 · 연구비 ARC 확인 · SI 안내 없음 (9 쪽 글자 층 전수).
- 숫자: 글자 층 + 렌더로 대조 — 70 × 26 · 1.3 · 2.5 × 10³ · 1.0 × 10⁷ · 0.29 · 1.0 × 10⁻⁶ (s⁻¹) · 0.4 · 0.5 · 0.05 · 10⁻³ · 30~92 · 5~35 · 0.5 · 0 · 0.0~0.093 (표 2 220 dpi) · S_min 5 µm (글자 층 '5 mm' ↔ 렌더 µm) · 5 % · 0.001–0.05 · 0.6 · 15,000–47,000 · 4–15 CPU · 2.0 GHz · 2d–4d · 2d × 2d · 30° · ~37° · 40 % · 15 rpm · 64 · 83 · 92 % · 6d · 8d · 67 · 74 · 84 % · 5 cm/s · 5 % · 2 % · 0.073 · 0.001 Pa s.
- 그림: 11 개 벡터 패널의 마커 = PyMuPDF 경로 (사각 · 원 · 삼각 · 범례 제외) · 눈금선 직선 맞춤 (그림 5b · 6 · 8b · 11 · 12 의 같은 자료가 서로 0.003 안에서 일치: 40 % · 15 rpm 의 k 0.410 · 0.325 · 0.261 이 그림 5b · 6 · 8b 에 공통) · 그림 12 이론선 = 꺾은선 꼭짓점.
- 정본 중복 확인: papers/ 파일 목록 · DOI · 'transverse mixing of wet' · 'Liu, P.Y' · 'Phys. Fluids 23' grep — 카드 없음 · 같은 해 다른 'liu2013' 카드 (`liu2013_cage_methane_adsorption_hydrate_nucleation`) 는 다른 저자 · 분야.

## 🔗 관련 카드
- 점착 혼합 · Bond · 충돌 수: `nase2001_granular_bond_collision_number_wet_cohesion` · `li2006_cohesive_mixing_shear_cell_collision_number_phase_diagram` · `li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy` · `li2005_cohesive_mixing_phase_diagrams_bond_ratio_dem_validation` · `figueroa2009_vdw_adhesion_mixing_segregation_bond_number_phase_diagram` · `chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed` · `jarray2019_cohesion_driven_mixing_segregation_drum` · `capece2015_multicomponent_granular_bond_number_cohesive_blend_flow_function`.
- 흐름층 · 회전 드럼 기구학: `khakhar1999_chaotic_mixing_granular_2d_tumbling_mixers_flowing_layer`.
- 같은 UNSW · Yu 그룹 DEM: `chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer` · `chandratilleke2012_particle_scale_mixing_index`.
- 혼합 지수: `lacey1954_particle_mixing_theory_index` · `egermann1980_ordered_vs_random_adhesion_pseudorandom_mixture_homogeneity` · `nadeem2023_gnn_mixing_index`.
- 믹서 DEM 리뷰 · 전극 믹싱 DEM: `jadidi2023_dem_batch_solid_mixers_review` · `hare2026_dem_pept_dry_mixing_nmc622_eirich` · `lischka2025_dem_eirich_intensive_mixer_dry_mixing`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

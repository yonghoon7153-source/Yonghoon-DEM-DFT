<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 형식 이웃 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md (절 · 머리 상자 · 의도 대조) ·
     계산 (DEM) 방법 절 꼴 = cantor2020_compaction_model_highly_deformable_particles.md · 같은 접촉 법칙 계보 = luding2008_cohesive_frictional_contact_models.md (우리 hooke/hysteresis 정의서) ·
     같은 문제 (경사 슈트 흐름) 의 8 년 뒤 판 = silbert2001_chute_flow_bagnold_spring_dashpot_hertz_dem.md (이 논문을 ref 23 으로 인용).
     쪽 표기: p.N = 학술지 인쇄 쪽 239–247 (PDF 9 쪽 = 인쇄 9 쪽 · PDF 1 쪽 = p.239 … PDF 9 쪽 = p.247 · 본문 p.239–246 · 참고문헌 p.246–247 · 보충 자료 안내 없음).
     원문 = 1993 년 옛 조판의 **스캔 PDF** (쪽마다 1 비트 래스터 한 장 · 300 dpi · OCR 텍스트 층) — 텍스트 층은 기호가 깨져 (α → a · K₁ → Kl · μ → /x · ≈ → -= 등) 식 · 숫자 · 기호는 전부 쪽 렌더로 확인했다.
     p.243 (PDF 5 쪽) 스캔은 ≈1.0–1.5° 기울어 있다 (축 맞춤 실측) — 판독은 기울기를 되돌린 뒤 했다.
     값 표지: [인쇄] = 본문 · 캡션 · 그림 안 글자 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 113 행 · 원 래스터 300 dpi · 안쪽 눈금 직선 보정 · 방법은 각 행 note) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 추론] = 이 카드의 해석 · [미확인] = 원문 9 쪽에 없음. -->
# 경사 슈트 (17°) 중력 흐름의 3D DEM — Walton–Braun (WB) 이력 법선 접촉 (재하 K₁α · 제하 K₂(α − α₀) · e = √(K₁/K₂) · 충돌 속도 무관) 의 3D 판 + 2D 면 증분 접선 마찰 (식 (1) K_T · 기억 T* · 평행 / 수직 분해 · μF_N 절단 · γ = 0 이면 선형 = TRUBALL) · "깊은 흐름은 강성에 뚜렷이 민감" (무른 구 정적 겹침 ≈0.5 % · 동적 ≤5 % of d) — ⚠ 단분산 1 mm 구 · 흐름 · 고압 압밀 아님 · 탈압 없음 — O. R. Walton (Mech. Mater. 1993)

> slug `walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem` · DOI `[미확인]` · type `DEM (자체 코드 · 3D 구 · 단분산 1 mm · WB 이력 선형 법선 K₁ / K₂ + 2D 면 증분 접선 (Mindlin 1949 근사 · T* 기억) + μF_N 절단 · leap-frog 6 자유도 · 쿼터니언 방향 · 중력 경사면 흐름 · 옆 4 면 주기 + 마찰 바닥 판 · N 63–1000 · 실험 없음)` · PDF `0ccc9050-72._Numerical_simulation_of_inclined_chute_flows_of_monodisperse_inelastic_frictional_spheres.pdf` · digested `2026-11-16` · status ✅
>
> **저자**: **Otis R. Walton** (단독) — Lawrence Livermore National Laboratory, Livermore, CA, USA (교신: Energy Program, L-207, LLNL, P.O. Box 808, Livermore, CA 94550) · *Mechanics of Materials* **16** (1993) 239–247 · Elsevier · Received 28 April 1992 · accepted 7 August 1992 · 0167-6636/93/$06.00 © 1993 Elsevier Science Publishers B.V. · **DOI 는 원문에 인쇄돼 있지 않다** (PDF 메타데이터 제목 = 'PII: 0167-6636(93)90048-V' — 인쇄 아님) · 자금 = US DOE (LLNL Contract No. W-7405-Eng-48) · DOE Advanced Research and Technology Development, Solids Transport Program (Pittsburgh Energy Technology Center) (p.246).
> **이웃 카드 (링크만)**: 이 논문을 인용한 카드 — [`pfeffer2001_dry_particle_coating_engineered_particulates`](pfeffer2001_dry_particle_coating_engineered_particulates.md) (참고 116 · L300 = 고른 의도의 출처 · L144 걸쇠 스프링 식) · [`silbert2001_chute_flow_bagnold_spring_dashpot_hertz_dem`](silbert2001_chute_flow_bagnold_spring_dashpot_hertz_dem.md) (참고 23 · L50 · L494) · [`paulick2015_elastic_particle_properties_dem_review`](paulick2015_elastic_particle_properties_dem_review.md) ([25] · L239 · L395 · L552 · L744 · L868 — ⚠ 귀속 문제 §0-1) — 우리 압축 덱 접촉 법칙의 정의서 [`luding2008_cohesive_frictional_contact_models`](luding2008_cohesive_frictional_contact_models.md) (Walton–Braun 1986 의 공개 대체판).
> **판독 원자료**: `litdb/figures/walton1993_chute_flow_hysteretic_normal_3d_tangential_contact_dem/digitized.csv` (113 행 — Fig. 2 23 행 · Fig. 1.1–1.6 의 a · b 90 행) · 크롭 47 장 (그림 9 = 쪽 묶음 2 + 행 6 + Fig. 2 · 식 19 · 근거 문단 19 · 전부 손 크롭 — 도구가 스캔 PDF 에서 0 개) — `figures.json`.
>
> ⚠⚠ **먼저 읽을 것 — 다섯 겹의 전이 금지**: ① **중력으로 흐르는 정상 상태 (17° 경사면 · chute)** 이지 판으로 누르는 준정적 고압 압밀이 아니다 — **탈압 계산도 없다** · ② **단분산 1 mm 구** (질량 1.492 × 10⁻⁶ kg → 밀도 ≈2850 kg/m³ [카드 산술] · 재료 이름 없음) · ③ 강성 K 는 그림 범례의 **숫자 (100 · 1000 · 10000 · '100+') 뿐** — 어느 강성 (K₁ · K₂ · K₀) 인지 · K₀ · γ · Δt 를 원문이 적지 않았다 [미확인] · ④ 접촉 소성은 **법칙 안의 잔류 겹침 α₀ 하나** (입자 형상은 고정 · 항복 · 캡 · 점착 없음) · ⑤ 결과는 첫 조사 ('Initial scoping calculations') 이고 실험 비교 그림 · 수렴 · 오차 막대가 없다.
> ⇒ **절대값 전이 0 건.**  가져오는 것 = (a) **이력 법선 (K₁ · K₂ · α₀ · e = √(K₁/K₂)) 과 증분 접선 (식 (1) · T* 기억 · 평행 / 수직 · μF_N 절단) 의 원문 식과 알고리즘 순서** (우리 `hooke/hysteresis` 의 조상 계보) (b) "**강성은 중립이 아니다** — 무른 구의 겹침이 동적으로 ≈5 % of d 에 이르면 깊은 흐름의 속도 · 전단층이 바뀐다" 는 원문 진술과 Fig. 2 크기 (N/σ² 20 에서 K 100 ↔ 1000 속도 비 ≈1.33 [판독 · 카드 산술]) (c) 단위 시험 기대값 (U5: e = √(K₁/K₂) 의 속도 무관 · α₀ = (1 − e²)α_max [카드 산술]) (d) 단분산 · 매끈한 바닥 · 작은 칸의 결정화 함정과 "2D 가 3D 보다 훨씬 더 결정화" 진술.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: Walton–Braun (1986) 의 **2D 원판** 접촉 법칙 (재하 K₁α · 제하 K₂(α − α₀) 의 **이력 선형 법선** + Mindlin 근사 **증분 접선**) 을 **3D 구로 넓히고** (접선을 접촉면 안의 평행 · 수직 두 성분으로 나눠 기억 T* 를 법선력에 비례해 바꾸고 방향이 뒤집히면 −T* 로 · 벡터 합을 μF_N 으로 자름), 그 코드로 **1 mm 단분산 구가 17° 마찰 평판을 흐르는 정상 상태**를 깊이 N/σ² = 1.24–40 · e 0.6–0.95 · μ 0.4–1.0 · K 100–10000 에서 훑어 — μ < tan θ 면 끝없이 가속 · μ ≫ tan θ 면 정지 · 깊은 흐름은 얇은 전단층 위에 결정 같은 비전단 덩어리가 타고 · **더 탄성적인 입자가 더 느리고** · **강성을 10–100 배 올리면 깊은 흐름이 느려지고 전단층이 두꺼워진다** (무른 구의 동적 겹침 ≤5 % of d) 고 보고한 짧은 (9 쪽) 첫 조사 논문.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 이력 법선 접촉의 원문 식 (D0 계보) | **F_N = K₁α (재하) · K₂(α − α₀) (제하)** · K₂ > K₁ · α₀ = 제하 힘이 0 이 되는 겹침 (*"due to inelastic deformation of the surfaces"*) · **e = √(K₁/K₂)**, *"independent of the relative velocity of impact"* — *"identical to the WB model"* | [인쇄] p.240 · 식 크롭 `eq_04` · `eq_05` |
| ② 접선 (증분 미끄럼 · 마찰) 의 원문 식 | **식 (1)**: K_T = K₀(1 − (T − T*)/(μF_N − T*))^γ (T 증가) · K₀(1 − (T* − T)/(μF_N + T*))^γ (T 감소) · γ ≈ 1/3 (Mindlin 닮음) · γ 1–2 (접촉부 소성 닮음) · 평행 / 수직 분해 · T*′ = T*\|F_N^n/F_N^{n−1}\| · 뒤집힘이면 T* → −T* · T_⊥ = K₀Δs_⊥ · \|T′\| ≤ μF_N | [인쇄] p.241 · p.244 · `eq_06`–`eq_18` |
| ③ 강성 값 · 맞춘 값 | 그림 2 범례의 **K = 100 · 1000 · 10000 · '100+'** (MKS → N/m 로 읽힘) 뿐 · K* = Kσ/mg ≈ 68.4K (p.245) → K* ≈ 6.8 × 10³ · 6.8 × 10⁴ · 6.8 × 10⁵ [카드 산술] · K 가 K₁ 인지 K₂ 인지 · K₀ · γ · Δt · 적분 단계 수 [미확인] · 맞춤 없음 (매개변수 훑기) | [인쇄] Fig. 2 · p.245 · [미확인] |
| ④ 강성 (연화) 은 결과를 바꾸나 | ★ **바꾼다 (깊은 흐름)**: *"An unanticipated finding is the pronounced sensitivity of the velocity and character of the deeper flows to the effective stiffness"* · 무른 구 = 정적 겹침 ≈ *"one half of one percent of a particle diameter"* (N/σ² 40) · 동적 *"up to 5%"* · 강성 ×10–×100 → 전단층 두꺼워지고 속도 ↓ (N/σ² > 10) · 얕은 흐름 (< 5) 은 둔감 | [인쇄] p.246 · `txt_p246_stiffness_*` · Fig. 2 [판독] |
| ⑤ 크기 (Fig. 2) | N/σ² 20: K 100 **3.61** · K 1000 **2.72** · K 10000 **2.80 m/s** → 무른 쪽이 1.29–1.33 배 빠름 · N/σ² 10: 1.82 vs 1.70 (1.07 배) · N/σ² 5 이하는 겹쳐 가를 수 없음 | [판독 · 카드 산술] §3-3 |
| ⑥ 탈압 · 되돌아옴 | **없음** (흐름) — 접촉 하나의 제하 가지 (K₂ · α₀) 만 있다 → 이 꼴이 주는 잔류 겹침 α₀ = (1 − e²)α_max [카드 산술] | §7-4 |
| ⑦ DEM 한계 · 소성 | 입자 = *"nearly-rigid"* 구 · 형상 고정 · 에너지 손실 = **이력 + 미끄럼뿐** (감쇠 없음) · 소성 = 접촉 법칙의 α₀ (와 γ 1–2) 로만 · *"assumes that the displacements from one time step to the next are relatively small"* · 결정화는 단분산 · 매끈한 바닥 · 작은 칸 탓일 수 있다 | [인쇄] p.239 · p.240 · p.241 · p.245 |
| ⑧ 2D ↔ 3D | 2D WB 모델의 3D 확장 · *"The propensity to form crystalline regions is much more pronounced in two-dimensions than in three"* | [인쇄] p.240 · p.245 |

⛔ **한정어 (떼지 말 것)**: ① 흐름 (17° · 중력 · 정상 상태) — 압밀 · 탈압 아님 ② 단분산 1 mm 구 · 재료 미지정 · 밀도 ≈2850 kg/m³ [카드 산술] ③ K 의 정체 · K₀ · γ · Δt [미확인] — Fig. 2 의 'K' 를 우리 k₁ 이나 E 로 옮기지 않는다 ④ 무차원 강성 K* 는 **중력 기준** (Kσ/mg) — 우리 300 MPa 압밀의 무차원 수 (겹침 / 지름 · P/E) 와 같은 축이 아니다 ⑤ 판독 값 (Fig. 1 · 2) 은 스캔 그림에서 읽은 것 — 저자 수치 파일 아님 ⑥ Fig. 1 의 K 는 그림 제목 · 캡션 · 본문 어디에도 없다 [미확인].
⇒ **절대값 전이**: 없다.  옮길 수 있는 것은 **법칙의 꼴 · 알고리즘 · 단위 시험 · '강성은 중립이 아니다' 의 정성 근거** 다.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-72 의 '왜' 칸 · 둘째 논문)

의도 원문: *"후보 D0 (이력 접촉 계보) — '걸쇠 스프링 접촉 — 카드 없음'"* · 근거 = `pfeffer2001` L300 (*"105 · 116 | O.R. Walton, R.L. Braun, J. Rheol. 30 (1986) 949–980 · O.R. Walton, Mech. Mater. 16 (1993) 239–247. | 걸쇠 스프링 접촉 — 카드 없음"*) · 덧붙임 지시: 하중 / 제하 강성이 다른 이력 법선 (K₁ · K₂ · 반발 계수와의 관계) 과 접선 (증분 미끄럼 · 마찰) 의 식을 번호별로 자르고 값 표 · 우리 hooke/hysteresis (K₁ · K₂ · k_c) 와 견줄 자리 · 탈압 (단계 6 · R4) 에서 잔류 겹침의 뜻.

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "후보 D0 (이력 접촉 계보)" — 이력 법선 접촉의 원문 | **채움** | p.240 §2.1: F_N = K₁α (loading) · K₂(α − α₀) (unloading) · K₂ > K₁ · α₀ = *"the relative 'overlap' where the unloading force is set to zero (due to inelastic deformation of the surfaces)"* · *"identical to the WB model"* — 조건 = 두 구의 겹침 α (지름 1 mm · 흐름 중 동적 충돌 · 지속 접촉) |
| "K₁ · K₂ · 반발 계수와의 관계" | **채움** | p.240: *"This normal-force model produces binary collisions with a constant coefficient of restitution given by e = √(K₁/K₂), independent of the relative velocity of impact"* · 그 근거 (실험 · FE) = *"discussed in Walton (1992)"* (p.241) — 이 논문 안에는 없다 |
| "걸쇠 스프링 (latching spring)" 이라는 이름 | **없음** | 이 논문 9 쪽에 'latch' 낱말이 없다 (텍스트 층 · 렌더 전수) — 원문 이름 = *"displacement-dependent hysteretic loading/unloading paths"* (p.239) · *"WB model"* (p.240).  '부분 걸쇠 스프링' 은 `pfeffer2001` (그 논문 p.59) 의 이름 — 원 출처 [미확인] (WB 1986 또는 Walton 1992 일 수 있다 [추정]) |
| "접선 (증분 미끄럼 · 마찰) 모델" | **채움** | p.241 식 (1) · p.244 의 갱신 순서 9 단계 (§4-2) · μF_N 절단 · *"When the exponent, γ, is set to zero, the model becomes linear"* → Cundall–Strack TRUBALL 과 *"essentially identical results"* (Trent and Walton, 1987 — 사신) |
| "식을 번호별로" | **채움 (번호는 하나뿐)** | 원문이 번호를 단 식은 **(1) 하나** — 나머지 18 개는 번호 없는 전시식 · 본문 식 → 이 카드가 인쇄 순서대로 `eq_01`–`eq_19` 로 잘랐다 |
| "값 표" | **일부** | 값 = Fig. 2 범례 K 100 · 1000 · 10000 · '100+' (단위 · 어느 강성인지 미기재) · e 0.6 · 0.85 · 0.95 · μ 0.4 · 1.0 · Fig. 1 은 e 0.85 · μ 0.4 (판도 0.4) · d 1 mm · m 1.492 × 10⁻⁶ kg · g 9.8 (p.245).  **K₀ · γ (쓴 값) · K₂/K₁ (e 로만) · Δt · 감쇠 = [미확인]** |
| "우리 hooke/hysteresis (K₁ · K₂ · k_c) 와 견줄 자리" | **채움 (견줄 꼴)** | §4-5 표 — 재하 · 제하 꼴은 같다 · **K₂ 상수 (e 상수)** ↔ 우리 k₂ 는 δ_max 에 따라 k₁ → k̂₂ 로 보간 (Luding eq 8) · **점착 k_c · 소성 깊이 φ_f 는 이 논문에 없다** |
| "탈압 (단계 6 · R4) 에서 잔류 겹침의 뜻" | **일부 (접촉 하나)** | 원문은 접촉 하나의 제하 가지만 — 계 (침대) 의 탈압 계산은 없다.  꼴에서 나오는 것: 접촉을 끝까지 풀면 α₀ = (1 − K₁/K₂)α_max = (1 − e²)α_max 가 남는다 [카드 산술 — 제하선이 (α_max, K₁α_max) 를 지난다는 조건] · e 0.85 → 최대 겹침의 **27.8 %** 가 남음 · 72.2 % 회복 |
| `pfeffer2001` L300 서지 "O.R. Walton, Mech. Mater. 16 (1993) 239–247" · "제목 카드에 없음" | **채움 (제목 보충)** | 첫 쪽: *Mechanics of Materials* 16 (1993) 239–247 · 제목 = *"Numerical simulation of inclined chute flows of monodisperse, inelastic, frictional spheres"* · 단독 저자 Otis R. Walton |
| `pfeffer2001` L144 의 **2 차 인용 값** — 적재 N_l = K₁·α · 제하 N_u = K₂·(α − α₀) | **같음** | 원문 F_N (기호만 N ↔ F_N) |
| 〃 e = √(K₁/K₂) "(속도 무관 가정)" | **같음 · 표현 하나 다름** | 원문은 '가정' 이 아니라 이 선형 이력 법칙이 **낳는 성질** (*"produces binary collisions with a constant coefficient of restitution … independent of the relative velocity of impact"*) |
| 〃 "α₀ = 유한 소성 변형" | **같음** | *"due to inelastic deformation of the surfaces"* |
| 〃 "접선 = Mindlin–Deresiewicz 단순형" | **일부** | 이 논문은 **Mindlin (1949)** 만 인용 (*"Walton and Braun's one-dimensional approximation to Mindlin's (1949) elastic frictional sphere contact force model"*) — Deresiewicz 이름 · 문헌 없음 |
| 〃 K_T = K₀(1 − (T − T\*)/(μN − T\*))^γ (T 증가) | **같음** | 식 (1) 첫 줄 |
| 〃 K_T = K₀(1 − (T − T\*)/(μN + T\*))^γ (T 감소 · "인쇄 그대로") | **다름** | 이 논문 식 (1) 둘째 줄의 분자는 **T\* − T** (`eq_06` 렌더 확인).  `pfeffer2001` 카드는 Pfeffer 원문 인쇄를 그대로 옮기고 L284 에 *"원 Walton 형과의 대조 [미확인]"* 이라 적었다 → **그 [미확인] 하나가 여기서 풀린다** (Pfeffer 2001 원문의 옮김 차이 · 그 카드의 옮김 잘못 아님 — 카드 문제 아님) |
| 〃 "γ ≈ 1/3" | **같음 + 덧붙임** | *"γ is a fixed parameter often set to 1/3 to make the model resemble Mindlin's elastic frictional sphere theory"* · *"A value of 1 or 2 for γ more closely mimics the behavior of frictional contacts involving plastic deformation in the contact region (Drake and Walton, 1992)"* (p.241) |
| 〃 "T′ = T + K_T·ΔS" | **같음** | T_∥ = T + K_TΔs_∥ (p.244 · 평행 성분) |
| (덧붙임) `silbert2001` L494 "3D chute DEM · 마찰 방향 기억 (D0)" · L50 *"…we do not differentiate between frictional directions at the same contact point at different time steps as does Walton [23]"* | **같음** | 3D 슈트 흐름 · 평행 / 수직 분해와 T* 의 부호 기억 (p.244) — Silbert 의 말과 맞는다 |
| (덧붙임) `paulick2015_elastic_particle_properties_dem_review` [25] Walton 1993 — *"the flow pattern … is not affected by a reduced elasticity as long as the overlap stays within a range of 1–10 %"* (L552) · 겹침 1–10 % (L239 · L395 · L744) · *"이 리뷰 전체의 상한"* (L868) | **원문에 없음 (반대 방향)** | 이 논문 9 쪽에 '1–10 %' · 'not affected' · 'reduced elasticity' 가 없다 (텍스트 층 grep + 렌더).  겹침에 관한 문장은 p.246 하나뿐 — 무른 구 **정적 ≈0.5 % · 동적 ≤5 % of d** · 깊은 흐름은 강성에 **뚜렷이 민감** · 얕은 흐름 (< 5 per σ²) 만 둔감.  ⇒ **카드 문제로 보고** (Paulick 원문이 그렇게 귀속했는지 · 카드 옮김인지는 Paulick PDF 대조 [미확인] — 카드는 고치지 않음) |

⇒ **의도 대조 결과: 일부** — 이력 법선 (K₁ · K₂ · α₀ · e = √(K₁/K₂)) 과 증분 접선 (식 (1) · T* · 평행 / 수직 · μF_N) 의 원문 식은 **채움**; '걸쇠 스프링' 이름은 **없음**; 값 표는 **일부** (K 의 정체 · K₀ · γ · Δt [미확인]); 1986 원판 (2D) 이 아니라 그 **3D 확장**이다.

---

## 0-2. ★ 첫째 논문 (Walton & Braun 1986) 을 이 논문이 어디까지 다시 적나 — 원문에 있는 것만

⛔ **Walton & Braun, J. Rheol. 30 (1986) 949–980 원문은 보지 못했다** (1저자 내려받기 불가 · 후보 표 N-72 첫째 제외) — 아래 '1986 대조' 칸은 전부 **[미확인]** 이다.  이 논문 참고문헌의 서지 = *"Walton, O.R., and R.L. Braun (1986), J. Rheol. 30 (5), 949–980."* (p.247 · 제목 없음).

| 항목 | 이 논문 (1993) 이 WB 1986 에 대해 적은 것 | 위치 | 1986 원문 대조 |
|---|---|---|---|
| 차원 | WB = **2 차원** 접촉력 모델 · 적분식 → 이 논문 = *"a straight forward extension to 3-dimensions"* | p.240 §2 | [미확인] |
| 법선 | F_N 식 전체 (K₁α · K₂(α − α₀)) = *"identical to the WB model"* · e = √(K₁/K₂) | p.240 §2.1 · `eq_04` · `eq_05` | [미확인] |
| 접선 | WB = Mindlin (1949) 의 **1 차원 근사** · *"the effective tangential stiffness of a contact decreases with tangential displacement until it is zero when full sliding occurs"* · 평행 성분은 *"treated almost identically with the 1-dimensional WB model with the exception that the value of T is always positive"* | p.241 · p.244 | [미확인] — 식 (1) 의 두 가지 꼴 (T* · γ) 이 1986 에 그대로 있었는지 원문 문장으로는 단정할 수 없다 |
| 결정화 | 2D 계산에서 결정화가 자주 보였다 — *"(see for example Walton and Braun (1986))"* | p.245 | [미확인] |
| 그림 · 표 · 값 | WB 1986 의 그림 · 표 · 매개변수 값 (K₁ · K₂ · K₀ · γ · μ) 은 **다시 싣지 않았다** | — | [미확인] |

**이 논문이 1986 판에 더한 것 (원문 서술 기준)**: 3D 확장 · 접선의 **2D 면 처리** (평행 · 수직 분해 → 벡터 합 → μF_N 절단) · 옛 마찰력을 새 접평면에 투영하고 크기 보존 · T* 를 **법선력 변화에 비례**해 다시 잼 · 평행 성분 뒤집힘 판정 (T* → −T*) · 수직 성분은 '새 변위' (K₀) · 6 자유도 leap-frog · 쿼터니언 방향 (p.240–241 · p.244).

---

## 1. 한 줄 요약
실험 슈트 (고정 질량 유량 · 길이 제한) 와 달리 **입자 수 / 면적을 고정**하고 옆 네 면을 주기 경계로 둔 계산 칸에서 (p.239), WB 이력 법선 + 2D 면 증분 접선의 3D DEM 으로 1 mm 단분산 구가 17° 마찰 평판을 흐르는 **정상 상태**를 훑는다 — μ < tan θ (0.306) 면 끝없이 가속 · N/σ² 0.5 도 가속 · μ ≫ tan θ (예: 2 배 넘게) 면 정지 (μ 1.0 → v ≈ 0 [판독]) · 깊어질수록 빠르고 (N/σ² 40 ≈4.1 m/s [판독]) 얇은 바닥 전단층 위에 결정 같은 비전단 덩어리 (충전율 ≈0.72–0.75 [판독]) · 더 탄성적인 입자가 느리고 전단층이 깊다 · **강성을 올리면 깊은 흐름이 느려진다** (무른 구의 동적 겹침 ≤5 % 가 바닥층 위를 '미끄러져 넘게' 해 에너지를 덜 위로 보낸다 — 저자 해석).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| Otis R. Walton (LLNL · 단독) | Mech. Mater. 16 (1993) 239–247 · 9 쪽 | [미확인] (인쇄 없음 · PDF 메타 PII 0167-6636(93)90048-V) | **배터리 재료 아님** — 단분산 1 mm 구 (재료 이름 없음 · m 1.492 × 10⁻⁶ kg) · 마찰 평판 | 계산 (자체 3D DEM 코드 · Fortran — p.244 *"standard Fortran"*) · 실험 없음 (기존 실험과의 일치 진술만) |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 입력 · 설정 (p.239–245 · [인쇄])
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 입자 | 단분산 구 · 지름 **1 mm** · 질량 **1.492 × 10⁻⁶ kg** · 재료 이름 없음 | [인쇄] p.245 |
| 밀도 | ≈ **2850 kg/m³** (= m / (πd³/6)) | [카드 산술] |
| 중력 | g = **9.8 m/s²** · 경사 **17°** (tan 17° = 0.306) | [인쇄] p.245 · p.239 · [카드 산술] |
| 계산 칸 | 옆 네 면 = 정지 주기 경계 · 바닥 = 마찰 평판 (거칠기 없음 · *"perfectly smooth, though frictional"*) · 위 = 자유면 · 옆벽 효과 없음 · *"only 5 or 10 particles across"* | [인쇄] p.239 · p.245 |
| 입자 수 (그림 제목) | n = 63 · 125 · 250 · 501 · 500 · 1000 ↔ n/A = 1.24 · 2.5 · 5 · 10 · 20 · 40 (Figs. 1.1–1.6) → 칸 넓이 A = 50.8 · 50 · 50 · 50.1 · 25 · 25 σ² | [인쇄] Fig. 1 제목 · [카드 산술] |
| 출발 상태 | 칸 위쪽에 무작위 배치 · **처음 고체 충전율 ≤ 0.4** · 작은 무작위 속도 + 기대 정상 속도보다 조금 빠른 평균 속도 · 속도 · 밀도 기울기 없음 · 중력을 기울여 흐름을 '켠다' | [인쇄] p.239 |
| 측정 | 평균 흐름 속도 · 질량 유속 · 밀도 · 속도 단면 · 정상 상태 뒤 시간 평균 (그림: 실선 = 순간 · 점선 = 누적 시간 평균) | [인쇄] p.239 · Fig. 1 캡션 |
| 접촉 매개변수 (Fig. 1) | e = **0.85** · 입자 간 μ = **0.4** · 판과의 μ = 0.4 (같은 값) · K [미확인] | [인쇄] p.245 |
| 접촉 매개변수 (Fig. 2 범례) | □ e 0.6 · μ 0.4 · K 100 / ○ e 0.85 · μ 0.4 · K 100 / ⊕ e 0.85 · μ 0.4 · K 10000 / ● e 0.85 · μ 0.4 · K 1000 / ■ e 0.95 · μ 0.4 · **K 100+** / ⊞ e 0.85 · μ **1.0** · K 100 — '+' 의 뜻 [미확인] | [인쇄] Fig. 2 |
| 단위 · 무차원 | 그림 값 = MKS · t* = t√(g/σ) · l* = l/σ · m* = m/m_p · **v* = v/√(gσ) ≈ 10.1v** · **K* = Kσ/mg ≈ 68.4K** | [인쇄] p.245 · `eq_19` |
| 확인 | √(gσ) = 0.0990 m/s → 1/√(gσ) = 10.10 · mg/σ = 0.01462 N/m → σ/mg = 68.39 · 시간 단위 √(σ/g) = 0.0101 s | [카드 산술] — 인쇄값 재현 |
| K* | K 100 → **6.84 × 10³** · 1000 → 6.84 × 10⁴ · 10000 → **6.84 × 10⁵** (mg/σ 단위) | [카드 산술] |
| 흐름 시간 (그림의 'time=') | 20 · 8 · 10 · 10 · 6.0 · 2.75 (Figs. 1.1–1.6 · MKS 라 s 로 읽힘) → t* ≈ 1980 · 792 · 990 · 990 · 594 · 272 | [인쇄] Fig. 1 · [카드 산술] |
| 적분 | leap-frog · 6 자유도 · 쿼터니언 방향 (Evans 1977 변형) · **Δt · 단계 수 · 계산 시간 [미확인]** | [인쇄] p.240 · [미확인] |

### 3-2. 결과 — 원문 문장 (p.239 · p.244–246)
- **마찰 대 경사**: *"for all cases when the coefficient of friction, μ, is less than the tangent of the angle of inclination, then the entire assembly of spheres simply accelerates unboundedly"* (p.244) · 초록: μ 가 tan θ 보다 *"somewhat greater"* 면 정상 · *"greatly exceeding … (e.g., by more than a factor of 2)"* 면 정지 (p.239).  μ/tan θ = 1.31 (μ 0.4) · 3.27 (μ 1.0) [카드 산술].
- **깊이**: N/σ² 0.5 (*"very sparse"*) = 가속 · 1–2 = 다른 깊이보다 느린 정상 속도 · 평균 속도는 깊이와 함께 증가 · < 5 = 단조 증가 속도 단면 · 깊으면 *"a non-shearing region riding over the top of a relatively thin shearing layer"* · < 2.5 = 높이와 함께 단조 감소 밀도 · 중간 = 흐름 안 최대 충전율 · 가장 깊으면 *"an essentially uniform (random close packed or crystal) non-shearing region above a lower density shearing region"* (p.244–245).
- **결정**: 깊이 10 · 20 · 40 의 결정 비전단 영역은 실험보다 두드러질 것 — 같은 크기 · 매끈한 바닥 · 작은 칸 (5 또는 10 입자 폭) · 그래도 실험 관찰 (MacRae and Gray 1961 · Owe Berg et al. 1969) 로 보아 *"may not be that unusual"* (p.245).
- **탄성**: *"the more elastic particles flow slower and have a deeper shearing layer at the bottom than do less elastic particles"* · 에너지 소산은 전단층 깊이와 엮인다 · 깊은 흐름이 빠른 이유 = 전체 중 소산하는 층의 몫이 작다 · *"significant implications for long run-out landslides and avalanches"* (p.245–246).
- ★ **강성**: *"An unanticipated finding is the pronounced sensitivity of the velocity and character of the deeper flows to the effective stiffness of the nearly-rigid contact normal force model. Assemblies with relatively soft particles (that would result in static "overlaps" on the order of one half of one percent of a particle diameter due to the large overburden load of the deepest flows, e.g., 40 per unit area) produce dynamic loads in the rapid shearing lower layer with up to 5% of a diameter overlap. This large overlap allows the particles immediately above the bottommost rolling layer to glide over them with less vertical motion than stiffer particles experience. … Increasing the stiffness by 1 or 2 orders of magnitude significantly increased the depth of the shearing layer and produced lower mean flow velocities for the flows deeper than 10 per unit area. The shallow flows (less than 5 per σ² area) were relatively insensitive to the stiffness of the spheres, since even the softest particles simulated only experienced dynamic overlaps of one half of one percent of a particle diameter."* (p.246 · `txt_p246_stiffness_*`).
- **실험과**: *"The flows reported here appear to differ qualitatively from the experimental flows of Johnson et al. (1990)"* · 평판의 완벽한 평평함이 원인인지 불분명 · 거칠기를 넣을 예정 (p.246).

### 3-3. ★ Fig. 2 판독 — 평균 흐름 속도 (m/s) vs 깊이 N/σ² (p.245 · [판독] · `digitized.csv` 23 행)
| 계열 (범례 그대로) | 1.24 | 2.5 | 5 | 10 | 20 | 40 |
|---|---|---|---|---|---|---|
| □ e 0.6 · μ 0.4 · K 100 | 0.60 | 0.70 | **1.59** | — | — | — |
| ○ e 0.85 · μ 0.4 · K 100 | (겹침) | (겹침) | ≈0.85 (● 와 겹침) | **1.82** | **3.61** | 틀 안에 없음 |
| ● e 0.85 · μ 0.4 · K 1000 | ≈0.43 (겹침 ±0.05) | ≈0.48 (겹침 ±0.05) | 0.84 | **1.70** | **2.72** | **3.72** |
| ⊕ e 0.85 · μ 0.4 · K 10000 | (겹침) | (겹침) | (겹침) | (겹침) | **2.80** | **4.12** |
| ■ e 0.95 · μ 0.4 · K 100+ | ≈0.36 (겹침) | ≈0.38 (겹침) | 0.67 | 1.38 | 2.20 | 2.84 |
| ⊞ e 0.85 · μ **1.0** · K 100 | ≈0 | ≈0 | ≈0 | — | — | — |
- 방법: 원 래스터 300 dpi · 바깥 틀 x 304.68–486.2 pt (N/σ² 0–40) · 안쪽 눈금 직선 맞춤 (x 잔차 ≤ 0.3 pt · y 0–5 m/s, 오른쪽 축 0.5 pt 높음 = 스캔 기울기 보간) · 표식 = ±2 pt 상자 안 잉크 무게중심 (600 dpi) · N 40 의 표식은 오른쪽 틀에 반쯤 잘려 x 를 40 으로 둠 · N 1.24 · 2.5 의 ●/○/⊕/■ 는 한 덩어리로 겹쳐 덩어리 위 · 아래 끝에서 표식 반지름으로 추정 (±0.05).
- ⚠ **설명 없는 점**: ○ (K 100) 계열 맨 왼쪽 위 **N/σ² ≈ 1.0 (측정 0.98) · v ≈ 4.90 m/s** — 거의 세로인 파선으로 N 1.24 덩어리에 이어진다 · 본문에 N 1.0 흐름 언급 없음 · 가속 중 (정상 아님) 값인지 [미확인].
- **크기 [카드 산술]**: N/σ² 20 — K 100 ÷ K 1000 = **1.33** · K 100 ÷ K 10000 = **1.29** · N/σ² 10 — K 100 ÷ K 1000 = 1.07 · ⇒ 원문 *"flows deeper than 10 per unit area"* 와 같은 방향 · 얕은 쪽 (≤ 5) 은 계열이 겹쳐 차이를 읽을 수 없다 (원문 *"relatively insensitive"*).  K 1000 ↔ 10000 은 N 20 에서 2.72 ↔ 2.80 · N 40 에서 3.72 ↔ 4.12 (강성 ×10 에서 단조가 아님 — 원문은 이 쌍을 따로 말하지 않는다).
- **탄성 [카드 산술]**: N 5 — e 0.6 (1.59) ÷ e 0.85 (K 1000 · 0.84) = 1.89 · N 20 — e 0.95 (2.20) ÷ e 0.85 (K 1000 · 2.72) = 0.81 · N 40 — 2.84 ÷ 3.72 = 0.76 → "더 탄성적이면 더 느리다" 와 맞는다 (단 ■ 는 K 가 '100+' 라 강성도 다르다).

### 3-4. ★ Fig. 1 판독 — 속도 · 충전율 단면 (p.242–243 · [판독] · 순간 단면 = 실선 위 검은 원 · `digitized.csv` 90 행)
| Fig · N/σ² · 'time=' | 바닥 칸 속도 (높이) | 위쪽 (판) 속도 | 최대 충전율 (높이) | 바닥 칸 충전율 | 칸 두께 |
|---|---|---|---|---|---|
| 1.1 · 1.24 · 20 | 0.38 (0.5 d) | 0.68 (6.5–8.5 d) | **0.32** (0.5 d · 위로 단조 감소) | 0.32 | 1 d |
| 1.2 · 2.5 · 8 | 0.36 (0.5 d) | 0.71 (6.5 d) | **0.40** (0.5 d) | 0.40 | 1 d |
| 1.3 · 5 · 10 | 0.55 (0.5 d) | ≈1.00 (6.5 d) | **0.52** (2.5 d · 안쪽 최대) | 0.40 | 1 d |
| 1.4 · 10 · 10 | 1.31 (1 d) | **1.79** (3–9 d) | **0.745** (4.9 d) | 0.42 | 2 d |
| 1.5 · 20 · 6.0 | 2.42 (1 d) | **2.97** (3–15 d) | **0.73** (5–13 d) | 0.34 | 2 d |
| 1.6 · 40 · 2.75 | 3.75 (1.7 d) | **4.16–4.17** (4.5–34 d) | **0.72–0.73** (4.5–10 d) · 가운데 0.59–0.62 (13–31 d) | 0.51 | ≈3 d |
- 방법: 쪽마다 기울기 (p.242 1–2 행 0.75–0.85° · 3 행 ≈0° · p.243 1.25°) 를 회전으로 되돌리고 안쪽 눈금으로 직선 맞춤 (x 잔차 ≤ 0.002 · y ≤ 0.04 지름) · 검은 원 = 2 px 침식 뒤 연결 성분 무게중심 · 점선 (누적 평균 · 열린 마름모) 은 읽지 않음.
- 읽는 법 [카드 산술 · 추론]: 깊은 흐름 (1.4–1.6) 은 속도가 바닥 1–2 칸에서만 바뀌고 (1.31 → 1.75 · 2.42 → 2.98 · 3.75 → 4.16) 위는 거의 같다 = 원문의 '얇은 전단층 위 비전단 덩어리' · 최대 충전율 0.73–0.745 는 면심입방 최대 π/(3√2) = 0.7405 [카드 산술] 에 가깝다 = 원문의 *"crystal"*.
- ⚠ **Fig. 1 의 K 는 원문 어디에도 없다 [미확인]** — 판 속도 (N 20 ≈2.97 · N 40 ≈4.16) 가 Fig. 2 의 K 10000 (2.80 · 4.12) 쪽에 가깝다 [카드 추론 · 판독 — 평균 속도와 판 속도는 다른 양].

### 3-5. [카드 산술] 확인 계산 (원문 식 아님 · 가정 병기)
| 양 | 식 · 가정 | 값 |
|---|---|---|
| 정적 겹침 (N/σ² 40 · 바닥) | δ/d ≈ N cos θ / K* — 한 σ² 기둥의 무게 법선 성분을 바닥 접촉 하나가 받는다고 놓은 자릿수 · K 를 재하 강성 K₁ 로 | K 100: **0.56 %** · 1000: 0.056 % · 10000: 0.0056 % — 원문 *"on the order of one half of one percent"* 와 같은 자릿수 · K 가 K₂ 라면 (K₁ = e²K) 0.77 % — 둘 다 '반 퍼센트 자릿수' 라 **K 의 정체는 이것으로 못 가른다** |
| 잔류 겹침 | α₀ = (1 − K₁/K₂) α_max = (1 − e²) α_max — 제하선이 (α_max, K₁α_max) 를 지남 | e 0.6: **64 %** · 0.85: **27.8 %** · 0.95: 9.8 % (최대 겹침 대비) |
| K₂/K₁ | 1/e² | e 0.6: 2.78 · 0.85: 1.38 · 0.95: 1.11 |
| 충돌 시간 | t_c = (π/2)√(m*/K₁)(1 + e) · m* = m/2 · K = K₁ 가정 · 감쇠 없음 | K 100 · e 0.85: **2.5 × 10⁻⁴ s** (0.025 t*) · K 1000: 7.9 × 10⁻⁵ s · K 10000: 2.5 × 10⁻⁵ s — Δt 와의 비 [미확인] |
| 다른 카드와 같은 축 | Silbert 2001 표준 k_n = 2 × 10⁵ mg/d (그 카드 표 I) → 이 논문 K 단위 (d 1 mm · m 같다고 놓으면) ≈ **2.9 × 10³ N/m** | Walton 의 K 1000 과 10000 사이 |

### 3-6. ★ 이 논문에 **없는** 값 (찾으러 갔다가 없다고 확인)
- K 가 K₁ · K₂ · K₀ 가운데 무엇인지 · K₀ 값 · K₀/K₁ · 계산에 쓴 γ · Δt · 단계 수 · 계산 시간 · 감쇠 (없다고 초록이 말함 — 에너지 손실 = 이력 + 미끄럼뿐) · 재재하 (reloading) 경로 · 판과의 접촉 강성 · 입자 재료 · 'K = 100+' 의 '+' · Fig. 1 의 K · 오차 막대 · 반복 수 · 수렴 · 칸 가로 · 세로 (A 만 산출).

---

## 4. ★ 방법 — 접촉 법칙 · 적분 · 경계

### 4-1. 법선 — WB 이력 (p.240 · `eq_04` · `eq_05`)
```
F_N = K₁ α            (loading)
F_N = K₂ (α − α₀)     (unloading)        K₂ > K₁ ,  e = √(K₁/K₂)  (충돌 속도 무관)
```
| 기호 | 원문 정의 | 우리 말 |
|---|---|---|
| α | *"the 'overlap' between the contacting spheres"* | 겹침 (우리 δ) |
| K₁ | 재하 강성 | 우리 k₁ |
| K₂ | 제하 강성 · K₂ > K₁ | 우리 k₂ (단 상수) |
| α₀ | *"the relative 'overlap' where the unloading force is set to zero (due to inelastic deformation of the surfaces)"* | 잔류 겹침 (우리 δ₀) — 원문은 α₀ 를 α_max 로 쓰는 식을 적지 않았다 (→ §3-5 [카드 산술]) |
| e | *"a constant coefficient of restitution given by e = √(K₁/K₂), independent of the relative velocity of impact"* | 이력이 낳는 반발 계수 (점성 감쇠 없이) |
- 근거: *"Experimental evidence for this model, and finite element calculations that this model mimics, are discussed in Walton (1992)."* (p.241) — 이 논문 안에는 실험 · FE 가 없다 → 정독 출력 n 후보.
- 원문에 없는 것: 재재하 경로 · α₀ 의 갱신 규칙 (여러 번 재하 · 제하) · 끌어당김 (점착) · 항복 · 캡 · 힘 상한.

### 4-2. 접선 — 2D 면 증분 마찰 (p.241 · p.244 · 갱신 순서)
1. **접촉 법선**: k̂_ij = (r_j − r_i)/\|r_j − r_i\| (`eq_07`) · *"The simulation model assumes that the displacements from one time step to the next are relatively small"* (p.241).
2. **옛 마찰력 투영**: T₀ = k̂_ij × T_old × k̂_ij = T_old − k̂_ij(k̂_ij · T_old) (`eq_08`).
3. **크기 보존 ('starting' 마찰력)**: T = \|T_old/T₀\| T₀ (`eq_09`) · 단위 벡터 t̂ = T/\|T\| (`eq_10`).
4. **표면 상대 변위**: Δs^{n−1/2} = [k̂_ij × (v_j − v_i) × k̂_ij + r_i(ω_i × k̂_ij) + r_j(ω_j × k̂_ij)]Δt ≈ Δr_ij − k̂_ij(k̂_ij · Δr_ij) + [r_i(ω_i × k̂_ij) + r_j(ω_j × k̂_ij)]Δt (`eq_11` · Δr_ij = r_ij^n − r_ij^{n−1}).
5. **분해**: Δs_∥ = (Δs^{n−1/2} · t̂) t̂ · Δs_⊥ = Δs^{n−1/2} − Δs_∥ (`eq_12` · `eq_13`).
6. **기억 다시 재기**: 법선력이 바뀌면 T*′ = T*\|F_N^n/F_N^{n−1}\| (`eq_14`).
7. **평행 성분**: K_T = 식 (1) (T*′ 사용) → T_∥ = T + K_TΔs_∥ (`eq_06` · `eq_15`) · **뒤집힘**: Δs^{n−1/2}·t̂ < 0 이고 T + (Δs^{n−1/2}·t̂)K_T < 0 이면 T* → −T* (다음 단계 · 매끄러운 기울기) (`eq_16`).
8. **수직 성분**: *"assumed to have no pre-existing surface strain"* → T_⊥ = K₀Δs_⊥ (`eq_17`).
9. **합 · 절단**: T′ = T_∥ + T_⊥ (`eq_18`) · \|T′\| > μF_N 이면 크기를 μF_N 으로 줄인다 (p.244).
- **식 (1)** (`eq_06`): K_T = K₀(1 − (T − T*)/(μF_N − T*))^γ (T 증가) · K_T = K₀(1 − (T* − T)/(μF_N + T*))^γ (T 감소) · K₀ = 처음 접선 강성 · T = 지금 접선력 크기 · T* = 0 에서 시작해 증가 ↔ 감소가 바뀔 때마다 그때의 T 로 · γ = 1/3 (Mindlin 닮음) · **γ = 1 또는 2 = 접촉부 소성 닮음** (Drake and Walton, 1992) (p.241).
- **선형 극한**: γ = 0 → K_T = K₀ (선형) · 복잡한 2D 경로에서 Cundall–Strack TRUBALL 선형 모델과 *"essentially identical results"* (Trent and Walton, 1987 — 사신) (p.244).

### 4-3. 적분 · 방향 (p.240 · `eq_01`–`eq_03`)
- leap-frog (Allen and Tildesley 1987) · 6 자유도: ẋ^{n+1/2} = ẋ^{n−1/2} + (F_x^n/m + g_x)Δt · x^{n+1} = x^n + ẋ^{n+1/2}Δt · ω̇_x^{n+1/2} = ω̇_x^{n−1/2} + (N_x^n/I_0)Δt (인쇄 기호 그대로 — 각속도에 점이 찍혀 있다).
- 구라서 힘 계산에 방향 (오일러 각) 이 필요 없지만 *"in anticipation of utilizing non-spherical particles in future calculations"* · 시각화 때문에 쿼터니언 (Evans 1977 변형) 으로 방향을 추적 — 세부는 *"a subsequent paper"* (p.240).

### 4-4. 계 · 경계 · 출발 · 측정 (p.239–240)
- 칸 = 옆 네 면 정지 주기 · 바닥 마찰 평판 · 위 자유면 · x 축 = 평판 · 중력을 17° 기울임 · 입자 수 / 면적 고정 (입력) · 옆벽 없음.
- 출발 = 처음 충전율 ≤ 0.4 무작위 · 작은 무작위 속도 + 정상보다 조금 빠른 평균 속도 · 정상 (평균 속도 · 시간 평균 단면이 시간에 일정) 뒤 평균.
- 주기 경계 때문에 *"only 'steady-state' conditions are physically meaningful"* (p.239) · 실험 슈트는 고정 유량 · 길이 제한이라 다르다 (p.239–240).
- **검증 진술 (그림 · 숫자 없음)**: 사실상 2D 슈트 (두 벽 사이 한 입자 폭) 실험과 속도 · 밀도 단면 *"good agreement"* (Drake 1988; 1992) · Couette 응력 일치 (Savage and Sayed 1984; Campbell 1986; Walton 1990) · 마찰을 뺀 계산은 운동론과 합리적 일치 (Lun et al. 1984; …) → *"give us confidence"* (p.240).

### 4-5. ★ 우리 LIGGGHTS `hooke/hysteresis` 와 한 표 (우리 쪽 = `luding2008` 카드 §2.3.2 · §7.1)
| 항목 | Walton 1993 (WB 3D) | 우리 압축 덱 `hooke/hysteresis` | 같음 / 다름 |
|---|---|---|---|
| 재하 | F = K₁α (선형) | k₁δ (k₁ 은 LIGGGHTS 가 E · 반경에서 — SE E_eff 1.35 GPa = 18 배 연화 · AM 140 GPa) | 같은 꼴 |
| 제하 | K₂(α − α₀) · **K₂ 상수** | k₂(δ − δ₀) · **k₂ 는 δ_max 에 따라 k₁ → k̂₂ 보간** (Luding eq 8) · k̂₂/k₁ = 1.5 (AM–AM) · 3.0 (AM–SE) · 5.0 (SE–SE) (`luding2008` §7.1 의 coefficientMaxElasticStiffness 를 비로 읽음) | 다름 — 우리는 겹침이 클수록 더 '소성' |
| 반발 | e = √(K₁/K₂) 상수 · 감쇠 없음 | 이력 몫 √(k₁/k₂(δ_max)) + 점성 γ₀ — k̂₂ 에 닿으면 이력 몫만 √(1/1.5) = **0.82** · √(1/3) = **0.58** · √(1/5) = **0.45** [카드 산술] | 다름 — 우리 COR 입력과 k̂₂ 의 정합은 따로 점검할 일 (`silbert2001` 카드 F-P5 와 같은 할 일) |
| 잔류 겹침 | α₀ = (1 − e²)α_max [카드 산술] | δ₀ = (1 − k₁/k₂)δ_max (`luding2008` §2.3.2) → k̂₂ 에서 **33 % · 67 % · 80 %** of δ_max [카드 산술] | 같은 꼴 · 우리 SE–SE 는 훨씬 '소성' |
| 점착 | 없음 | −k_c δ 가지 (k_c 1e5 · 2e5 · 1e6) | 우리만 |
| 항복 · 캡 | 없음 | 없음 (φ_f = k̂₂ 에 닿는 깊이일 뿐 · 힘 캡 아님 — `luding2008` 카드 *"경도 (H) / 항복압 캡 없음"*) | 둘 다 없음 |
| 접선 | 식 (1) 비선형 감소 강성 (γ 1/3) · T* 기억 · 평행 / 수직 · μF_N 절단 | `tangential history` (선형 접선 변위 + Coulomb 절단 — `silbert2001` 카드) | 우리 ≈ Walton 의 **γ = 0 극한** (선형 = TRUBALL) [카드 추론] — 투영 · 크기 보존 · T* 의 법선력 비례 같은 세부 대조는 LIGGGHTS 소스 확인 전 [미확인] |
| 입자 · 형상 | 단분산 1 mm 구 · 형상 고정 | AM ⌀4–9 µm · SE ⌀≈1 µm 구 · 형상 고정 | 둘 다 구 |
| 하중 | 중력 · 흐름 · 겹침 ≈0.5 % (정적) · ≤5 % (동적) of d | 300 MPa 압밀 · 순수 SE (하중지지 침대) 평균 겹침 ⟨δ⟩ ≈ 지름의 11–12 % (`coetzee2017_dem_calibration_review` 카드 L811 의 우리 값) | 우리 겹침이 이 논문 '큰 겹침' 의 두 배 이상 |

### 4-6. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM 한계 진술**: *"nearly-rigid particles interacting via contact forces and gravity"* (p.239) · ★ *"An unanticipated finding is the pronounced sensitivity of the velocity and character of the deeper flows to the effective stiffness of the nearly-rigid contact normal force model"* (p.246) — 결과가 **인공 강성** 에 달린다는 고백 · *"The simulation model assumes that the displacements from one time step to the next are relatively small"* (p.241) · 결정화는 같은 크기 · 매끈한 바닥 · 작은 칸 탓으로 *"probably more pronounced than would be typical in a physical test"* (p.245) · 실험 (Johnson et al. 1990) 과 정성적으로 다르다 (p.246) · 구만 (비구형은 앞으로).
- **(ii) 소성 · 큰 변형**: 소성은 **접촉 법칙 안** 에만 — 제하 강성 K₂ > K₁ 이 남기는 α₀ (*"due to inelastic deformation of the surfaces"*) 와 접선 γ 1–2 (*"frictional contacts involving plastic deformation in the contact region"*) · 입자 형상 변화 · 부피 보존 흐름 · 이웃 접촉의 상호 영향 · 가공 경화 = 없음 · 법칙의 근거 (실험 · FE) 는 Walton (1992) 로 미룸 · 맞춘 값 = 없음 (훑기) · 비용 = 입자 63–1000 개 · 시간 [미확인].
- **(iii) 차원**: 3D (2D WB 의 3D 확장) · 2D ↔ 3D 진술 = *"The propensity to form crystalline regions is much more pronounced in two-dimensions than in three and such crystallizations have often been seen in past simulation calculations (see for example Walton and Braun (1986))"* (p.245) · 비교 실험 (Drake) 은 *"essentially 2-dimensional chute flows (between two vertical walls, one particle diameter apart)"* (p.240).
- **(iv) 탈압**: 계 단위 탈압 계산 **없음** — 접촉 하나의 제하 가지 (K₂ · α₀) 만.

### 4-7. 기법 미니 용어집
- **슈트 흐름 (chute flow)** = 경사면을 중력으로 흘러내리는 입자층 · 여기서는 주기 칸이라 '무한히 긴 경사면' 의 정상 상태.
- **이력 선형 스프링 (WB 법선)** = 누를 때 K₁ · 뗄 때 더 가파른 K₂ 로 다른 길을 가는 스프링 → 한 번 누르고 떼면 겹침 α₀ 가 남고 그 넓이만큼 에너지를 잃는다 · 반발 계수 e = √(K₁/K₂) 가 충돌 속도와 무관.
- **증분 접선 강성 (식 (1))** = 미끄러질수록 접선 강성이 줄어 완전 미끄럼에서 0 이 되는 꼴 (Mindlin 1949 의 1D 근사) · T* = 마지막으로 방향이 바뀐 때의 접선력 ('기억').
- **2D 면 (surface) 처리** = 접촉면 안에서 옛 마찰력 방향과 평행 / 수직으로 변위를 나눠 따로 다룬 뒤 벡터로 합침.
- **TRUBALL** = Cundall–Strack 의 원조 DEM 코드 (선형 접촉) — γ = 0 극한의 대조 대상.
- **K* = Kσ/mg** = 중력 하중 기준 무차원 강성 (압밀 압력 기준이 아님).
- **leap-frog** = 속도는 반 단계, 위치는 정수 단계에서 엇갈려 적분하는 2 차 명시 방법.

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 (`fig_1.png` · p.242 묶음 + 캡션) · 1 continued (`fig_1_cont.png` · p.243) | Figs. 1.1–1.6 — 각 행 (a) 속도 · (b) 충전율 단면 · (c) 칸 그림 · e 0.85 · μ 0.4 · N/σ² 1.24–40 | 흐름 영역 지도 (얕음 = 전체 전단 · 깊음 = 얇은 전단층 + 결정 덩어리) |
| 1.1–1.3 (`fig_1_1`–`fig_1_3`) | 얕은 흐름 — 속도 단조 증가 · 충전율 감소 (1.1 · 1.2) · 안쪽 최대 0.52 (1.3) | 단분산 구의 낮은 충전율 흐름 예 |
| 1.4–1.6 (`fig_1_4`–`fig_1_6`) | ★ 깊은 흐름 — 판 속도 1.79 · 2.97 · 4.16 m/s · 충전율 0.72–0.745 (결정) [판독] | ⚠ **결정화 함정** (단분산 · 매끈한 바닥 · 작은 칸) — 2D 벤치마크 (단계 3) 설계 경고 |
| 2 (`fig_2.png`) | ★ 평균 속도 vs 깊이 — e · μ · K 훑기 | ★ **강성 민감** 의 크기 (N 20: K 100 ↔ 1000 = 1.33 배) · μ 1.0 정지 · e 효과 |
| 식 크롭 19 장 | `eq_01`–`eq_03` leap-frog · `eq_04` 법선 · `eq_05` e · `eq_06` 식 (1) · `eq_07`–`eq_18` 접선 갱신 · `eq_19` 무차원 단위 | 보고서 접촉 법칙 절에 붙일 원문 식 (D0 계보) |
| 근거 문단 19 장 | `txt_p239_*` (초록 · 칸 · 출발) · `txt_p240_*` (검증 · WB 3D 확장 · 쿼터니언 · 법선 + e + FE 근거) · `txt_p241_*` (접선 · γ 소성 · 작은 변위 가정) · `txt_p244_*` (평행 · 수직 · TRUBALL · 결과 영역) · `txt_p245_*` (매개변수 · 결정 · 2D ↔ 3D · 탄성) · `txt_p246_*` (강성 민감 · 실험과 다름) | 원문 인용용 |

## 6. Post-processing ★
- **원문이 한 것**: 시간 평균 (누적) 단면 (속도 · 충전율) · 평균 흐름 속도 · 질량 유속 · 칸 그림 · 깊이별 평균 속도 그림.
- **안 한 것**: 응력 · 배위수 · 접촉 수 · 겹침 분포 (문장 두 개뿐) · 에너지 수지 숫자 · 오차 막대 · 반복 (시드) · 칸 크기 시험 · 강성 수렴 · 시간 간격 시험 · 실험과의 직접 대조 그림.
- **이 카드의 후처리**: 스캔 래스터 판독 (Fig. 2 23 행 · Fig. 1 a · b 90 행 · 쪽 기울기 회전 보정 · 안쪽 눈금 직선 맞춤 · 겹친 표식은 덩어리 끝에서 반지름 추정) · 무차원 단위 재현 · 정적 겹침 자릿수 · e ↔ α₀ · 충돌 시간 · 칸 넓이 · Silbert 강성 환산.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 COMMON 지시 · 정본 카드 (`luding2008` §7.1 · `coetzee2017_dem_calibration_review` L811) 에서 옮겼다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 접촉 법선 | WB 이력 선형 · K₂ 상수 · 감쇠 없음 | `hooke/hysteresis` (Luding eq 6) · k₂(δ_max) · 점착 k_c · 점성 γ₀ | **조상 ↔ 후손** — 꼴 같음 · 우리 쪽이 일반화 |
| 접선 | 식 (1) 비선형 · T* 기억 · 2D 면 | `tangential history` (선형 + Coulomb) | 우리 ≈ γ = 0 극한 [카드 추론] |
| 입자 | 단분산 1 mm 구 | 다분산 µm 구 (AM + SE) | 다름 |
| 하중 | 중력 흐름 · 겹침 ≈0.5–5 % | 300 MPa 압밀 · 겹침 ≈11–12 % (순수 SE) | 영역이 다르다 |
| 강성 | K 100–10000 훑기 → 깊은 흐름 민감 | E_eff 1.35 GPa (18 배 연화 · 실험 기공에 맞춤) | §7-3 |
| 탈압 | 없음 (접촉 하나의 제하 가지만) | DEM 언로딩 키트 (진행) · MPM 제하 없음 | §7-4 |
| 2D ↔ 3D | 3D · 2D 가 더 결정화 | DEM 3D · MPM 2D (단계 2–3) · 3D | 2D 벤치마크 경고 같은 방향 (`silbert2001` 카드와 둘째 근거) |

### 7-2. ★ 랩 기준과 나란히 (판정 없이)
| 출처 | 재료 · 입자 | 상태 | 진밀도 분모 | 기공 / 충전 |
|---|---|---|---|---|
| **랩 표준** | LPSCl 순수 SE | 300 MPa | **1.64 g/cm³** (고정) | 기공 **10–13 %** |
| 이 논문 (Fig. 1 [판독]) | 단분산 1 mm 구 (재료 미지정 · ≈2850 kg/m³ [카드 산술]) | 중력 흐름 · 정상 상태 · 압력 없음 | 해당 없음 (구 부피 / 칸 부피) | 단면 최대 충전율 0.32 (N/σ² 1.24) – 0.745 (N/σ² 10) = 기공 68–25.5 % [카드 산술] |
- **"랩 표준과 다른 문헌 값"** — 재료 · 입자 · 하중 (흐름) · 정의 (칸 안 충전율) 가 다 다르다 · 견줄 축이 없다.

### 7-3. ★ 강성 연화 (frame [2]) — Walton 의 '강성 민감' 과 우리 18 배 연화
- 원문은 **"겹침이 작으면 강성은 상관없다"** 가 아니라 **"깊은 흐름에서는 무른 구 (동적 겹침 ≤5 % of d) 가 결과를 바꿨다 · 얕은 흐름 (동적 ≈0.5 %) 만 둔감"** 이라고 적는다 (p.246) — 강성은 중립인 수치 손잡이가 아니다.
- 우리 순수 SE 압밀 (하중지지 침대) 의 평균 겹침 ⟨δ⟩ ≈ 지름의 11–12 % (`coetzee2017_dem_calibration_review` 카드 L811 의 우리 값) 는 Walton 의 '큰 겹침' (≤5 %) 의 두 배 이상 [카드 산술] → **이 논문은 '연화해도 된다' 의 근거가 될 수 없다** (오히려 반대 방향의 증거) · 단 흐름 (충돌 · 미끄러져 넘기) 의 기전이라 압밀로 크기를 옮기지 않는다.
- 우리 쪽 정당화는 여전히 frame [2] (재배열 · 입계 미끄럼 · 미세 파괴를 접어 넣은 **실험 기공 맞춤** · MPM 독립 확인) 이고, 이 논문이 주는 것은 *"강성을 바꾸면 무엇이 바뀌는지를 보고하라"* 는 보고 의무 (겹침 분포 · 강성 ×10 민감도) 다.
- ⚠ `paulick2015` 카드의 *"[25] Walton 1993 의 1–10 % … 이 리뷰 전체의 상한"* (L868) 은 이 원문에 없다 (§0-1) — 우리 11–12 % 를 문헌 상한과 견줄 때 그 줄을 쓰지 않는다.

### 7-4. ★ 탈압 (단계 6 · R4) — 이 접촉 꼴이 주는 잔류 겹침의 뜻
- 이 꼴에서 접촉 하나를 끝까지 풀면 **회복되는 겹침 = (K₁/K₂)α_max = e²α_max · 남는 겹침 = (1 − e²)α_max** [카드 산술].  e 0.85 → 72 % 회복 · 28 % 잔류.
- 우리 덱에서 SE–SE 접촉이 k̂₂ (= 5k₁) 에 닿았다면 **20 % 만 회복 · 80 % 잔류** [카드 산술 · 가정 = δ_max ≥ δ*_max] — ⇒ DEM 침대의 탈압 되돌아옴 (springback) 은 재료 탄성 (E · ν) 이 아니라 **덱 계수 k̂₂/k₁ 와 침대 기하** 가 정한다 [카드 추론].  게다가 k₁ 은 18 배 연화된 값이라 최대 겹침 자체가 크다.
- ⇒ 단계 6 의 결과 전 등록에 넣을 문장: *"DEM 탈압 회복량은 k̂₂/k₁ (이력 비) 에 묶인 출력이다 — 실험 되돌아옴과 견줄 때 그 비를 같이 보고하고, 맞추는 값 (R5) 과 섞지 않는다."*
- 이 논문 자체는 계의 탈압을 계산하지 않았다 — 위는 법칙의 꼴에서 나온 산술이다.

### 7-5. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: DEM 접촉 법칙 (법선 이력 · 접선 기억) 의 원문 · 흐름 영역 · 강성 민감의 첫 보고.
- **없는 것**: 압밀 · 탈압 · 수송 · 소성 형상 변화 · 실험 대조 그림.  ⇒ D0 (지금 DEM) 의 **법칙 계보 · 단위 시험** 쪽에만 쓴다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | 충전율 = 칸 높이 칸 (1–3 d) 안의 구 부피 분율 (그림 정의 [카드 추론]) · 겹침이 큰 연화 강성에서는 구 부피 합 연산자가 겹침 부피를 두 번 센다는 경고는 **이 논문에 없다** | 기공 연산자 원문 정의 [미확인] |
| **단계 1** (3D 메모리 · 장 수) | 없음 (N ≤ 1000) | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 접선 기억 알고리즘 (§4-2 의 9 단계 — 투영 · 크기 보존 · 분해 · T* 비례 · 뒤집힘 · 절단) = MPM 의 판 · 벽 마찰 접촉에 이력 마찰을 넣을 때의 점검표 | MPM 자체 없음 |
| **단계 3** (2D 접촉 표현 비교) | ★ **"2D 가 3D 보다 훨씬 더 결정화"** + 단분산 · 매끈한 바닥 · 작은 칸이 결정을 키운다 (p.245) → 2D 침대는 다분산 · 결정화 점검을 결과 전에 (`silbert2001` 카드 F ④ 와 같은 결론 · 둘째 근거) | 2D 결과 숫자 없음 |
| **단계 4** (3D 순수 SE · σ_y 맞춤) | 없음 | — |
| **단계 5** (3D 복합 압밀) | 없음 | — |
| **단계 6** (탈압 · 되돌아옴) | ★ 접촉 하나의 회복 = e²α_max · 잔류 (1 − e²)α_max [카드 산술] → DEM 탈압 회복은 k̂₂/k₁ 에 묶인 출력 (§7-4) | 계 탈압 계산 없음 |
| **단계 7** (형상 · 피복 · 수송) | 없음 | — |
| **후보 D0** (지금 DEM) | ★★ 법선 이력 (K₁ · K₂ · α₀ · e) 의 3D 원문 · 접선 기억의 원문 · **강성 민감 진술** (깊은 흐름 · 동적 겹침 5 %) · Silbert 2001 과 이 논문의 계보 (Cundall–Strack → WB 1986 → Walton 1993 → Luding 2008 = 우리 덱 · Silbert 2001 = 법선 이력을 뺀 판) | 압밀 · 고겹침 영역 검증 없음 · K 의 정체 [미확인] |
| **후보 A′-0** (판 · 벽 · AM 접촉 규칙) | 마찰 판 경계 (μ 판 = μ 입자) · 접선 기억의 갱신 순서 (§4-2) | 판의 강성 · 거칠기 없음 |
| **후보 A · A′** (MPM 강체 AM / 입자별 속도장) | 없음 | — |
| **후보 B** (입자별 FE) | 없음 — 법칙 근거의 FE 계산은 Walton (1992) 로 미룸 | — |
| **후보 C · C′** (MDR · 항복 캡 DEM) | 대조군 꼴 — **캡 · 항복 · 점착 없는 이력 선형** 이 출발점이라는 것 · γ 1–2 = 접촉 소성의 접선 쪽 손잡이 (Drake and Walton 1992) | 항복값 · 캡 없음 |
| **후보 M0** (균질화 압밀) | 없음 | — |
| **U0–U6** | ★ **U5** (두 입자 충돌): 이력 선형이면 e = √(K₁/K₂) 가 충돌 속도와 무관 · 접촉 시간 (π/2)√(m*/K₁)(1 + e) · 잔류 α₀ = (1 − e²)α_max [카드 산술] — 우리 덱에서 k̂₂/k₁ = 5 · 3 · 1.5 이면 이력 몫 e 0.45 · 0.58 · 0.82 (δ_max ≥ δ*_max) 가 기대값 · **U2** (경사면 마찰 회귀): μ < tan θ → 끝없이 가속 · μ ≈ 3.3 tan θ → 정지 (Fig. 2 · 집합체) · γ = 0 극한 = TRUBALL 선형 일치 (원문 대조 방식) | 단위 시험 숫자 · 시간 간격 [미확인] |
| **R1–R7** | **R4** (탈압): 접촉 하나의 잔류 겹침 꼴 (§7-4) · **R2** (미끄럼 · 분리): 접선 절단 · 기억 · 2D 면 처리 · **R5** (맞추는 값 하나): 이 논문은 맞춤 없음 — 단 '강성' 이 결과를 바꾸므로 강성을 맞추는 값으로 쓰면 다른 관측량이 함께 움직인다는 경고 · **R6 · R7**: 없음 (형상 고정 · 파괴 없음) | R1 · R3 없음 |
| **결과 전 대조 항목** | 없음 (재료 · 하중 영역이 다름) — Fig. 2 · Fig. 1 판독은 **흐름 DEM 의 재현 시험** (같은 법칙 · 단분산 1 mm · 17°) 으로만 | 배터리 · 압밀 대조 불가 |

- **재료 · 차원 · 조건 차이**: 1 mm 단분산 구 (재료 미지정) ↔ µm AM + SE · 중력 흐름 ↔ 300 MPa 압밀 · 겹침 0.5–5 % ↔ 11–12 % · 3D = 같음 · 접촉 꼴 = 조상.

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **D0 덱의 인용 사슬을 고친다** — 법선 이력 = Walton–Braun (2D, 1986) → **Walton 1993 (3D · 이 카드)** → Luding 2008 (점착 · k₂ 보간 · 우리 덱) · 접선 기억 = Walton 1993 (식 (1) · γ = 0 이면 선형) · Silbert 2001 = 법선 이력을 뺀 줄인 판 (D0).
2. **U5 를 바로 짤 수 있다** — 두 입자 정면 충돌로 e(v_impact) 가 평평한지 · α₀ = (1 − e²)α_max 인지 · 접촉 시간을 덱 계수 (k₁ · k̂₂ · γ₀) 로 다시 센 기대값과 견준다 (단위 시험 U5).
3. **강성 보고 의무** — 연화한 DEM 결과마다 겹침 분포 (평균 · 최대 · 동적) 와 강성 ×10 민감도를 함께 적는다 (Walton 은 그 둘로 깊은 흐름 결론이 바뀜을 보였다 · frame [2] 정당화와 별개의 보고 의무).
4. **탈압 회복 = 이력 비의 출력** — 단계 6 등록 문서에 k̂₂/k₁ 를 같이 적고 회복량을 그 비와 짝지어 해석 (§7-4).
5. **2D 벤치마크 결정화 경고의 둘째 원문** — 단분산 · 매끈한 벽 · 작은 칸은 결정을 키우고 2D 가 3D 보다 심하다 (p.245).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "The hysteretic linear normal contact force — F_N = K₁α on loading and K₂(α − α₀) on unloading with K₂ > K₁, giving a constant coefficient of restitution e = √(K₁/K₂) independent of impact velocity — was extended from the 2D Walton–Braun model to 3D spheres together with an incremental two-dimensional surface friction model (Walton, Mech. Mater. 16 (1993) 239–247)."
- "In 3D DEM of monodisperse spheres flowing down a 17° incline, the velocity and character of deep flows were pronouncedly sensitive to the contact stiffness: soft particles with static overlaps of ~0.5 % and dynamic overlaps up to 5 % of a diameter flowed faster with thinner shear layers (Walton 1993, p. 246)."
- 국문: *"Walton (1993) 은 강성을 10–100 배 올리면 깊은 슈트 흐름이 느려지고 전단층이 두꺼워진다고 보고했다 — 연화 강성은 중립이 아니다 (동적 겹침 ≤5 % of d)."*
- 국문: *"이력 선형 법선 (K₁ 재하 · K₂ 제하) 에서 접촉 하나를 끝까지 풀면 최대 겹침의 (1 − e²) 가 남는다 (Walton 1993 의 법칙에서 산술)."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **K 의 정체 미기재** — Fig. 2 범례의 K (100 · 1000 · 10000 · '100+') 가 K₁ · K₂ · K₀ 가운데 무엇인지 · 단위 (MKS 라 N/m 로 읽힘) · '+' 의 뜻이 없다.
2. **K₀ · γ (계산값) · Δt · 감쇠 · 단계 수 · 계산 시간 미기재** — 식 (1) 의 γ 는 "흔히 1/3" 이라고만.
3. **그림 판독 한계** — N 1.24 · 2.5 의 표식이 겹쳐 계열을 가르지 못한다 · N 40 표식은 틀에 반쯤 잘림 · ○ 계열의 N ≈ 1.0 · 4.9 m/s 점은 설명이 없다.
4. **Fig. 1 의 K 미기재** — 판 속도가 Fig. 2 의 K 10000 쪽에 가깝다는 것은 이 카드의 추론.
5. **검증 진술에 그림 · 숫자가 없다** — 2D 슈트 · Couette · 운동론 일치는 다른 문헌 인용 (p.240).
6. **실험과 정성적으로 다르다** (Johnson et al. 1990 · p.246) — 매끈한 평판의 영향 미정.
7. **결정화 과장 가능성** — 저자 스스로 단분산 · 매끈한 바닥 · 작은 칸을 든다 (p.245).
8. **참고문헌 불일치** — 본문 *"(Drake, 1988; 1992)"* (p.240) ↔ 목록에는 Drake (1988) 과 Drake and Walton (1992) 만 (Drake 단독 1992 없음).
9. **식 (1) 의 접선 강성은 '평행 방향' 에만** — 수직 성분은 늘 K₀ (새 변위) 로 다룬다 (p.244) — 대각 경로에서의 정확성은 TRUBALL 선형 극한 (γ = 0) 으로만 대조됐다.
10. **각속도 기호** — 적분식의 각속도가 점 찍힌 ω̇ 로 인쇄 (본문은 'angular velocity') — 옮겨 적을 때 ω 로 읽는다.
11. **2 차 인용 주의** — `paulick2015` 카드가 전하는 '1–10 % · not affected' 는 이 원문에 없다 (§0-1) · `pfeffer2001` 의 감소 가지 분자 (T − T*) 는 이 원문의 (T* − T) 와 다르다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 서지 (원문 그대로 · p.246–247) | 왜 | 정본 카드 |
|---|---|---|
| Walton, O.R., and R.L. Braun (1986), J. Rheol. 30 (5), 949–980. | 2D 원판 (법선 이력 · 1D 접선) | 없음 — ⛔ 후보 표 N-72 첫째 제외 (내려받기 불가) · 공개 대체판 = `luding2008` |
| Walton, O.R. (1992), Numerical simulation of inelastic frictional particle–particle interactions, in: Roco, ed., Particulate Two-Phase Flow, Ch. 25, Butterworth–Heinemann, Boston. | ★ 이력 법선의 **실험 근거 · FE 계산** (p.241 이 미룬 곳) — 질문 e · l | 없음 (papers/ ls · grep 'Particulate Two-Phase Flow') |
| Drake, T.G. and O.R. Walton (1992), Comparison of Experimental and Simulated Grain Flows, J. Appl. Mech., submitted. | γ = 1–2 (접촉부 소성) 의 근거 · 실험 ↔ 계산 슈트 흐름 | 없음 |
| Cundall, P.A. and O.D.L. Strack (1979b), A discrete numerical model for granular assemblies, Geotechnique 29, 47–65. | D0 계보의 원점 (선형 접촉 · TRUBALL) | 없음 (인용만 — `silbert2001` 등) |
| Mindlin, R.D. (1949), Compliance of elastic bodies in contact, J. Appl. Mech., Trans. ASME 16, 259–268. | 증분 접선 강성의 원전 | 없음 (`morrissey2013` 이 인용) |
| Johnson, P.C., P. Mott and R. Jackson (1990), Frictional–collisional equations of motion for particulate flows and their application to chutes, J. Fluid Mech. 210, 501–535. | 계산과 정성적으로 다른 실험 슈트 흐름 | 없음 |
| Zhang, Y. and C.S. Campbell (1992), The interface between fluid-like and solid-like behavior in two-dimensional granular beds, J. Fluid. Mech., 237, 541–568. | 2D 결정 ↔ 유체 경계 (2D 결정화 근거) | 없음 |
| Trent, B.C. and O.R. Walton (1987), Private Communication, Los Alamos National Laboratory and Lawrence Livermore National Laboratory. | γ = 0 ↔ TRUBALL 대조의 근거 — **사신 (출판물 아님)** | — |

---

## [미확인] 목록
- DOI (원문 인쇄 없음) · 입자 재료.
- Fig. 2 의 K 가 K₁ · K₂ · K₀ 가운데 무엇인지 · 단위 · 'K = 100+' 의 '+' · Fig. 1 의 K.
- 계산에 쓴 K₀ · K₀/K₁ · γ · Δt · 단계 수 · 계산 시간 · 판과의 접촉 강성.
- 재재하 경로 · α₀ 의 다회 갱신 규칙 (이 논문에 없음).
- 칸의 가로 · 세로 (넓이 A 만 산출 · '5 또는 10 입자 폭').
- ○ (K 100) 계열 N ≈ 1.0 · 4.9 m/s 점의 뜻.
- '부분 걸쇠 스프링 (partially latching spring)' 이름의 원 출처 (이 논문에 없음).
- Walton & Braun 1986 원문 대조 전부 (§0-2) · Walton (1992) 의 실험 · FE 근거.
- `paulick2015` [25] 귀속 문장의 Paulick 원문 (이 카드는 Paulick PDF 를 보지 않았다).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-16)
- 서지: 메인 세션 메모 (O. R. Walton · 제목 · Mechanics of Materials 16 (1993) 239–247 · Received 28 April 1992 · accepted 7 August 1992 · PDF 9 쪽 · 스캔) = 원문 첫 쪽과 같음 · 저자 이름 전체 = **Otis R. Walton** (첫 쪽) · DOI 인쇄 없음 (9 쪽 전수) · 보충 자료 안내 없음.
- 후보 표 · `pfeffer2001` L300 서지 (O.R. Walton, Mech. Mater. 16 (1993) 239–247) = 원문과 같음 · 제목은 카드에 없었고 여기서 보충.
- 숫자 · 식: 9 쪽 렌더 (110–1800 dpi) 로 확인 — 17° · 0.4 · 0.5 · 1–2 · 2.5 · 5 · 10 · 20 · 40 per σ² · factor of 2 · 1 mm · 1.492 × 10⁻⁶ kg · 9.8 · 10.1 · 68.4 · 1/3 · 1 or 2 · one half of one percent · 5% · 1 or 2 orders · 0.85 · 0.4 · 5 or 10 particles · Fig. 2 범례 · Fig. 1 제목 (n · n/A · fmu · elast · time) — 전부 위치 확인.
- 'latch' · 'Deresiewicz' · '1–10' · 'not affected' · 'reduced elasticity' 낱말 = 원문 0 회 (텍스트 층 grep + 겹침 문단 렌더).
- 판독 보정: 쪽별 기울기 (p.242 1–2 행 0.75–0.85° · p.243 ≈1.25°) 를 축선 맞춤으로 재고 회전으로 되돌림 · 안쪽 눈금 직선 맞춤 잔차 (x ≤ 0.002 단위 · y ≤ 0.04 지름 · Fig. 2 x ≤ 0.3 pt) · 겹친 표식은 덩어리 끝 기준.
- 정본 중복 확인: papers/ 목록 (walton* 없음) · 'inclined chute flows' 0 건 · 'Mech. Mater. 16' = `pfeffer2001` (인용) · `silbert2001` (참고 23) · 'Walton' grep = 인용 · 언급만 → 카드 없음.

## 🔗 관련 카드
- 이 논문을 인용한 카드: `pfeffer2001_dry_particle_coating_engineered_particulates` (참고 116 · 고른 의도) · `silbert2001_chute_flow_bagnold_spring_dashpot_hertz_dem` (참고 23) · `paulick2015_elastic_particle_properties_dem_review` ([25] · 귀속 문제 §0-1).
- 접촉 법칙 계보 · 우리 덱: `luding2008_cohesive_frictional_contact_models` (hooke/hysteresis 정의서 · Walton–Braun 대체판) · `thakur2014_eepa_adhesive_elastoplastic_dem` (k_t = 2/7 k₁ 을 Walton–Braun 으로 인용) · `morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis` (Walton–Braun 1986 · Walton–Johnson 2009 서지) · `pasha2014_linear_elastoplastic_adhesive_contact` · `thorntonning1998_adhesive_elastoplastic_contact` · `zunker2024_mdr_contact_model_partI` (제하 비교).
- 강성 낮추기 · 겹침 한계: `paulick2015_elastic_particle_properties_dem_review` · `lommen2014_dem_speedup_contact_stiffness_reduction_bulk_behavior` · `coetzee2017_dem_calibration_review` (Walton–Braun 이력 spring head-to-head).
- 슈트 흐름 · 결정화: `silbert2001_chute_flow_bagnold_spring_dashpot_hertz_dem`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

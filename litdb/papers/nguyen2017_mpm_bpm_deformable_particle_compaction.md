<!-- digest 표준 양식. COMPREHENSIVE / paper-level STANDALONE digest. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · pycompact2025_dem_mpfem_workflow.md -->
# 변형 입자 압밀을 두 방식으로 — 암시적 MPM+CD (탄성 연속체 입자) vs BPM (강체 1차입자 응집체 · 소성) · 2D 300 입자 · 마찰 0/0.5 · Z−Z0 ∝ (Φ−Φ0)^0.5 ★ Nezamabadi 2022 의 전신 — Nguyen (EPJ Web Conf. 2017)

> slug `nguyen2017_mpm_bpm_deformable_particle_compaction` · DOI `10.1051/epjconf/201714005013` · type `MPM+CD vs BPM (2D; implicit MPM + contact dynamics vs bonded-particle aggregates of rigid primaries; conference paper)` · PDF `6c4da2a7-5._Compaction_of_granular_materials_composed_of_deformable_particles.pdf` · digested `2026-11-09` · status ✅
>
> ⚠⚠ **소재 · 차원 경고**: 전부 **2D 원판** · 재료는 일반 "무른 입자" **E = 10 MPa · ν = 0.45 · ρ = 990 kg/m³** · 입자 지름 **mm 급**.
> Φ 는 2D 면적 분율.  ⇒ **LPSCl + NCM811 3D 기공률로 절대 전이 0 건** — 방법론 · 무차원 경향만.
>
> ⚠⚠ **그림 범례 모순 — 인용 전에 §5.2 를 읽을 것**: Fig 2 범례는 **빨간 원 = MPM · 검은 삼각형 = BPM** 인데 Fig 3 범례는
> **빨간 원 = BPM · 검은 삼각형 = MPM** 이다.  마찰 거동 · 본문 기전 문장 · 2022 후속 논문은 Fig 3 쪽 (= Fig 2 범례 뒤바뀜) 을 가리키지만
> Fig 2 바로 옆 본문은 인쇄된 범례대로 쓰여 있다.  ⇒ **Fig 2 의 "어느 방법이 어느 곡선인가" 는 추정으로만 인용**하고, 값은 **표식 (빨간 원 /
> 검은 삼각형)** 으로 적는다.
>
> ⚠ 이 논문의 MPM 은 **탄성뿐**이다 (소성은 BPM 쪽).  ⇒ "MPM vs BPM" 비교가 **표현 방식 (연속체 / 응집체)** 과 **재료 거동 (탄성 / 소성)** 을
> **동시에** 바꾼다 (교란).  MPM 에 소성을 넣은 후속 = 짝 카드.
>
> ⚠ `> elements:` / `> methods:` 태그를 **의도적으로 생략**했다 (화학 원소 축 카드 아님).
>
> 짝 카드: `nezamabadi2022_mpm_cd_plastic_particle_compaction` — **같은 그룹 (LMGC · IATE Montpellier) 의 후속 저널 논문** (MPM 에 이선형 경화 소성 ·
> 해석 압밀식 · 정규화 Z 법칙).  ⚠ 그 논문은 이 학회 논문을 인용하지 않는다 (BPM 원 논문 *Granular Matter* 19, 8 (2017) 은 인용).

---

## 0. 우리에게 왜 중요한가 (한눈 위치)

| 우리가 필요한 것 | 이 논문이 주는 것 |
|---|---|
| **입자 간 마찰**을 MPM 에서 켰을 때 무엇이 바뀌나 | MPM-CD 를 **μ = 0 / 0.5** 로 — Φ(ε) 는 같고, Z 는 마찰 없을 때 **0.2–0.3 높다** (digitized), 응력은 "little effect" — Fig 2 · 3 |
| **절대 배위수** (짝 논문은 정규화만) | 재밍 (응력 시작) ε ≈ 0.08 에서 **Z ≈ 3** · Φ ≈ 0.75 / Φ0 = 0.8 에서 **Z ≈ 3.7–4.5** / 최대 **Z ≈ 5.2–5.5** — Fig 3a |
| "점접촉 (Hertz) 은 대변형에서 깨진다" 의 수치 | 단일 원판 MPM 이 2D Hertz 직선을 **ε > 0.05 에서 이탈**, ε > 0.15 에서 낮은 기울기 · *"Above 20% of deformation … contacts can no more be modeled as point contacts"* — Fig 1 · §4 |
| DEM 틀 안에서 **변형 입자**를 만드는 대안 (MPM 의 경쟁자) | **BPM** = 강체 1차입자 ≥ 200 개 응집체 + 장거리 인력 (CD) → 소성 평탄 σ ≈ F0/⟨a0⟩ — 그리고 그 결함 셋 (§8-④) |
| 제하 (unloading) 의 입자 수준 거동 | BPM 단일 입자를 ε 0.1 · 0.3 에서 제하 — **거의 수직** (회복 변형 ≈ 0.008–0.009, digitized) — 이 짝에서 유일한 제하 자료 |
| DEM 한계의 제3자 문장 | *"the only degrees of freedom considered in these techniques are those of particles (displacements and rotations).  For soft particles … it is necessary to take into account the internal degrees of freedom of each individual particle as well as the contact interactions."* |

⇒ [DEM 우선 (수영)] 관점: **후보 A′ (접촉을 푼 MPM) 에 마찰 시험의 기준점**을, **후보 C 계열 (DEM 틀의 변형 입자)** 에는 BPM 이라는
반례 · 대조군을 준다.  ⚠ 3D · 강체 AM 혼합 · 집합체 제하 · 실험 검증 없음.

---

## 1. 한 줄 요약 (bilingual)

**KR:** 무른 입자 집합체를 두 가지로 표현해 — (i) 입자마다 **암시적 MPM 연속체 (선형 탄성)** + 접촉은 **Contact Dynamics**, (ii) **BPM** (강체 · 무마찰
1차입자들의 응집체를 장거리 인력으로 묶어 CD 로 푼다 → 깨지지 않는 **소성** 입자) — 2D 원판 300 개를 위 벽 5 m/s 로 일축 압축했다 (μ = 0 · 0.5).
형상 변화가 RCP 를 넘는 치밀화를 지배하고, 입자 간 마찰은 변형에 영향이 작으며, **Φ0 ≈ 0.8 이후 Z−Z0 ∝ (Φ−Φ0)^0.5** 가 두 방법 · 마찰 유무에 걸쳐
성립한다 (거품 · 에멀전과 같은 지수).

**EN:** Soft-particle packings are represented either as implicit-MPM elastic continua coupled to Contact Dynamics, or as a Bonded
Particle Model (aggregates of rigid frictionless primary particles held by a long-range attraction and solved with CD, which deform
plastically without rupture).  Uniaxial compaction of 300 2D particles (top wall 5 m/s, μ = 0 or 0.5) shows that particle shape change
dominates densification beyond RCP, inter-particle friction has little effect on the deformation, and beyond Φ0 ≈ 0.8 the mean
coordination number follows Z − Z0 ∝ (Φ − Φ0)^0.5 for both methods, as in emulsions and foams.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **Thanh Hai Nguyen** (1,2) · **Saeid Nezamabadi** (2) · **Jean-Yves Delenne** (3) · **Farhang Radjai** (2,4) |
| 소속 | 1 The University of Danang – University of Science and Technology, 54 Nguyen Luong Bang, Danang, Vietnam · 2 LMGC, UMR 5508 CNRS, Université de Montpellier, Montpellier, France · 3 IATE, UMR1208, INRA, Université de Montpellier, Cirad, SupAgro, Montpellier, France · 4 ⟨MSE⟩², UMI 3466 CNRS-MIT, CEE, Massachusetts Institute of Technology (MIT), Cambridge, USA |
| 연락 (인쇄된 그대로) | nthai@dut.udn.vn · saeid.nezamabadi@umontpellier.fr · jean-yves.delenne@supagro.inra.fr · franck.radjai@umontpellier.fr (교신 표시 없음) |
| 저널 | **EPJ Web of Conferences 140, 05013 (2017)** — *Powders & Grains 2017* (학회 논문) |
| DOI | **10.1051/epjconf/201714005013** |
| 라이선스 | Open access · **CC BY 4.0** (© The Authors, EDP Sciences) |
| 접수 / 게재일 | **[미확인]** (PDF 에 없음) |
| 분량 | **4 쪽** · Fig 1–4 · 식 (1)–(2) · 참고문헌 14 · 표 · SI 없음 |
| 연구유형 | 수치 (2D 암시적 MPM + CD · BPM + CD) · **실험 없음** |
| 코드 · 계산 자원 · 런타임 | **[미확인]** |
| 자금 | University of Danang, University of Science and Technology, project T2017-02-02-91 (T. H. Nguyen) |
| 방법 원 논문 (인쇄된 참고문헌 — **우리 미열람**) | [5] Nezamabadi, Radjai, Averseng, Delenne, *J. Mech. Phys. Solids* 83, 72 (2015) — MPM + CD · [6] Nezamabadi, Nguyen, Delenne, Radjai, *Granular Matter* 19, 8 (2017) — BPM · CD 원전 [3] Moreau, *Eur. J. Mech. A Solids* 13, 93 (1994) · [4] Radjai & Richefeu, *Mech. Mater.* 41, 715 (2009) · [10] Radjai & Dubois (eds.), *Discrete-element Modeling of Granular Materials* (Iste-Wiley 2011) |

---

## 3. 핵심 수치 — stated / digitized / derived(ours)

> ⚠ `digitized` = 그림의 **벡터 경로**에서 꺼낸 표식 · 선 좌표를 축 눈금으로 환산 (눈금 맞춤 잔차 ≤ 1.5 × 10⁻³ 데이터 단위).  **추세 · 비교 전용.**
> `derived(ours)` = 논문 값으로 내가 계산한 것.

### 3.1 수치 설정 (stated · 쪽 = 논문 쪽)

| 항목 | 단일 입자 (§3, p.2) | 집합체 (§4, p.3) |
|---|---|---|
| 차원 | 2D (MPM 은 **평면변형** 명시) | 2D 원판 |
| 입자 수 | 1 | **300** |
| 크기 | 반지름 **R = 5 mm** | 지름 **∈ [1.4, 2.4] mm** (약한 다분산 · 장거리 질서 방지) |
| 상자 · 하중 | 아래 벽 고정 · 위 벽 **0.2 m/s** 하강 | 폭 L 의 직사각 상자 (**L 값 미기재**) · 위 벽만 **5 m/s** 하강 |
| 시간 간격 | **[미기재]** | **δt = 0.1 µs** |
| 중력 · 벽 마찰 | — | **0 · 0** (응력 구배 방지) |
| 입자 간 마찰 | — | **μ = 0** 또는 **μ = 0.5** (두 경우) |
| MPM | 4 절점 사각형 요소 · 요소당 물질점 4 · **Δr/R = 0.029** (Δr = 물질점 평균 간격) | *"The same material parameters"* — 해상도는 **미기재** |
| MPM 재료 | **선형 탄성 E = 10 MPa · ν = 0.45 · ρ = 990 kg/m³** — *"We chose a high value of Poisson's ratio in order to get nearly constant volumes of the particles as in BPM particles"* | 같음 |
| BPM | 강체 · 무마찰 1차입자 **1750 개** · 지름 **∈ [0.16, 0.26] mm** · 식 (1) **F0 = 100 N · γ = 7** · 차단 거리 **δ = a0** (1·2 번째 이웃만 상호작용) · 같은 입자 안 1차입자 마찰 **0** | 입자당 1차입자 **최소 200 개** (1차입자 크기 · F0 **미기재** — §11) |
| 시간적분 | CD (비평활 · 암시적) · MPM 은 암시적 [5] | 같음 |
| 판독 | **σ = F/L** (L = 그 순간 입자의 수평 지름) · **ε = ln(1 + d/R)** (d = 입자 중심 변위) | σ = 바닥 벽 힘 / σ0 · **ε′ = ln(1 + Δh/h0)** (기준 상태 Φ0 = 0.8 부터) · ε = 시작부터 · Z · Φ |

### 3.2 derived(ours)

| 양 | 값 | 근거 |
|---|---|---|
| E/(1−ν²) (평면변형 계수) | **12.54 MPa** | |
| 2D Hertz 원판 선의 σ–ε 기울기 (σ = F/2R) | **(π/8)·E/(1−ν²) = 4.92 MPa** | Fig 1 점선을 벡터로 재면 **4.92 MPa** ⇒ 그림은 σ = F/(2R) 로 그렸다 ✓ |
| c_P · c_S (ρ 990) | **195.7 · 59.0 m/s** · c_P/c_S = 3.32 | 탄성 상수 |
| 재하 Mach V/c_P · V/c_S | 단일 0.001 · 0.0034 · **집합체 0.026 · 0.085** | 우리 MPM V/c_P 0.03 → V/c_S ≈ 0.21 (CLAUDE.md "MPM 재하율 함정") |
| MPM 해상도 | R/Δr ≈ **34.5** → 원판당 물질점 ≈ **3,700** (2D) · 요소 ≈ 930 | Δr/R = 0.029 |
| BPM 소성 문턱 | **σ_I = F0/⟨a0⟩ = 100 N / 0.2 mm = 0.5 MPa** (단위 깊이당) | stated 정의 · ⟨a0⟩ ≈ 0.2 mm |
| γ = 7 차단 거리에서 남는 인력 | (1+1)^−7 = **F0 의 0.78 %** | 식 (1) |
| 단일입자 1차입자 크기로 지름 1.4 mm 입자를 채우면 | ≈ **40–45 개** (2D) — "최소 200 개" 와 안 맞음 | ⇒ 집합체 BPM 은 1차입자를 줄였을 것 (미기재) |
| Φ = Φ′0 e^ε (Φ′0 = 0.7) 를 ε = 0.45 에 | **1.10** (> 1) | 그림은 0.99 — 선형화 근사로만 성립 (§11) |

### 3.3 결과 수치

| 항목 | 값 | 종류 |
|---|---|---|
| MPM 단일 원판: 선형 (Hertz) 이탈 | **ε > 0.05** · ε > 0.15 에서 더 낮은 기울기의 직선 | stated |
| 〃 σ (ε 0.1 · 0.2 · 0.3 · 0.5) | ≈ **0.39 · 0.65 · 0.83 · 1.16 MPa** · ε > 0.15 기울기 ≈ **1.8 MPa** | digitized |
| BPM 단일 입자: 선형 구간 | 변형 **≈ 2 %** 까지 (그림의 안내선 기울기 **25 MPa**) | stated / digitized |
| 〃 소성 평탄 | **σ_I = F0/⟨a0⟩ = 0.5 MPa** (정의) · 그림 평균 **≈ 0.54 MPa** (sd 0.04, ε 0.05–0.49) | stated / digitized |
| 〃 제하 | ε **10 % · 30 %** 에서 · *"stress decreases linearly … slope … increase slightly with strain"* · 안내선 기울기 **≈ 52 → ≈ 109 MPa** (2 배) · 잔류 ε ≈ 0.092 · 0.294 → **회복 ≈ 0.008–0.009** | stated / digitized |
| 기준 상태 | **Φ0 = 0.8** (재밍 시작) · σ0 = 그때의 응력 (**절대값 미기재**) · 시작 **Φ′0 = 0.7** | stated |
| 재밍 (응력 시작) | **ε ≈ 0.08 · Z ≈ 3 · Φ ≈ 0.75** — *"the assembly remains fragile (rearrangements of particles) until … Φ0 ≃ 0.8"* | stated |
| Φ0 = 0.8 의 ε (Fig 3a 점선) | **≈ 0.157** · 그때 Z: 빨간 원 ≈ **3.7** · 검은 삼각형 ≈ **4.2–4.5** | digitized |
| 최대 Z | *"5.5 in all simulations … reflects the low size polydispersity"* · 그림: 빨간 원 **5.52–5.53** · 검은 삼각형 **5.23 (마찰) / 5.42 (무마찰)** | stated / digitized |
| 마찰의 Z 효과 (Fig 3 범례로 MPM) | 무마찰 − 마찰 ≈ **+0.30 (ε 0.157) · +0.28 (0.25) · +0.19 (0.45)** · BPM 은 ≈ 0 | digitized |
| Φ(ε) | 0.70–0.71 → **0.99** (ε 0 → 0.45) · 선형 맞춤 기울기 **0.67** (빨간 원) · **0.62** (검은 삼각형) | digitized |
| Fig 2 σ/σ0 끝값 | 빨간 원 **≈ 3.6–3.8** (ε′ 0.28) · 검은 삼각형 **≈ 15–17.5** (ε′ 0.25–0.26) · ε′ 0.20 에서 2.8–3.0 vs 5.3–6.2 | digitized |
| Z 붕괴 (Fig 4) | (Z−Z0)/(Z1−Z0) ∝ **(Φ−Φ0)^0.5** · Z0 @ Φ ≈ 0.8 · Z1 @ Φ ≈ 1 · Φ−Φ0 축 0–0.19 | stated |
| 〃 마찰별 편차 (√(x/0.19) 기준) | 무마찰 평균 **≈ 0.00 / −0.01** · 마찰 **−0.06 / −0.08** (rms 0.05–0.14) | digitized |
| BPM 내부 공극 한계 | *"40% of deformation and a packing fraction of 0.93"* | stated |

---

## 4. 시뮬레이션 방법 ★

### 4.1 MPM + CD (탄성 연속체 입자)
- 물질점 정보를 배경 격자에 투영 → 격자에서 운동방정식 → 격자 해로 물질점 갱신.
- *"The important point for the treatment of soft particles with MPM is the **necessity of coupling it with the CD approach** for a rigorous treatment
  of frictional contacts.  More details of this procedure can be found in [5]."* — 접촉 알고리즘 세부는 이 4 쪽에 **없다** (짝 논문 §4.2 = 다중 격자 +
  공통 격자).
- 재료: **선형 탄성뿐** (E 10 MPa · ν 0.45 · ρ 990).  ν 0.45 의 근거 = BPM 과 부피 보존을 맞추려고 (물성 근거 아님).

### 4.2 BPM (Bonded Particle Model) — DEM 틀의 변형 입자
- 입자 하나 = **강체 1차입자들의 응집체**.  1차입자 사이 힘 = 장거리 인력 F_a + 단거리 반발 F_r.
- **인력 (식 1)**: `F_a = −F0 (1 + δ/a0)^(−γ)`, a0 = a1 + a2 (두 1차입자 반지름 합), δ = 간격, F0 = 접촉 (δ = 0) 에서의 최대 인력 [8 Israelachvili, 9 Ioannidou].
  *"The choice of the exponent γ is not crucial for this study"* · 시멘트 · 점토의 평균력 퍼텐셜을 나타낼 수 있다 [9].
- **반발**: 1차입자가 **완전 강체**라 F_r 는 닿을 때 (δ = 0) 만 작동 ⇒ 합력 F 는 δ > 0 에서 인력만, δ = 0 에서 [−F0, +∞] 의 값 — **CD 의 비평활 ·
  암시적 적분**으로 계산 [3, 4, 10].
- **같은 입자 안 1차입자 마찰 = 0** — *"To avoid strain shear localization and volume change within aggregates"*.
- 구현: 차단 거리 δ = a0 (γ = 7 이면 그 너머 인력은 무시 가능 → 1·2 번째 이웃만).
- 결과 거동: *"the resulting behavior is plastic"* — 깨지지 않고 (응집체 분산 없이) 소성 변형.  장점 = *"it uses the framework of the DEM"*.

### 4.3 단일 입자 직경 압축 (§3)
- R = 5 mm · 아래 벽 고정 · 위 벽 0.2 m/s.  BPM 1750 개 (지름 0.16–0.26 mm) · F0 100 N · γ 7.  MPM 2D 평면변형 · 4 절점 사각형 · 요소당 물질점 4 ·
  Δr/R = 0.029.
- σ = F/L (L = 수평 지름), ε = ln(1 + d/R) (d = 입자 중심 변위).
- 2D Hertz (원판): `F = (π/4)·E/(1−ν²)·R·ε` (식 2) — 3D 구의 지수 3/2 와 달리 원판은 **선형**.

### 4.4 집합체 일축 압축 (§4)
- 원판 300 개 · 폭 L 상자 · 위 벽 5 m/s · δt 0.1 µs · 지름 1.4–2.4 mm · 중력 0 · 벽 마찰 0 · 입자 간 μ = 0 / 0.5 · BPM 입자당 1차입자 ≥ 200 · 재료 같음.
- 응력 = 바닥 벽 힘 · σ0 (Φ0 = 0.8 의 "consolidation stress") 로 정규화 · ε′ = ln(1 + Δh/h0) (기준 상태부터).
- Z = 평균 배위수 — *"Above 20% of deformation, the particles are so much deformed that the contacts can no more be modeled as point contacts.  In this regime,
  the particle shapes are well approximated by polygons, and Z then represents the number of sides of these polygons."*

### 4.5 ★ 입자 처리 (우리 "무질서 처리" 의 DEM 대응)

| 축 | MPM 쪽 | BPM 쪽 |
|---|---|---|
| 형상 | 원판 (2D 연속체) | 원판 모양 응집체 |
| 소성 표현 | **없음 (탄성)** — 형상 변화는 탄성 대변형 | **응집체 재배열 = 소성** (1차입자는 강체) — 재료 σ_y 아님, 문턱 = F0/⟨a0⟩ |
| 접촉 | CD (μ 0 / 0.5) | 입자 간 = 1차입자 간 CD 접촉 (μ 0 / 0.5) · 입자 안 = 무마찰 + 인력 |
| 크기 분포 | 약한 다분산 [1.4, 2.4] mm | 같음 |
| 부피 보존 | ν 0.45 (거의 비압축) | 1차입자 강체 — 단 응집체 내부 공극이 있다 (Φ 0.93 한계) |
| 파괴 · 결합상 · 강체 입자 혼합 | 없음 | 없음 (깨지지 않게 설계) |
| 무작위성 | 시드 앙상블 · 오차막대 **없음** | 같음 |

---

## 5. 결과 — 절별

### 5.1 단일 입자 (Fig 1)
- MPM: 작은 변형에서 Hertz 직선과 일치 → **ε > 0.05 이탈** → **ε > 0.15 이후 낮은 기울기 (≈ 1.8 MPa, digitized) 의 직선**.  ε 0.5 에서 ≈ 1.16 MPa.
  저자: Hertz 범위 (3D 지수 3/2) 는 *"generally used in molecular dynamics simulations of granular materials … by assuming small contact strains [11, 12]"*.
- BPM: ≈ 2 % 까지 선형 → **σ ≈ 0.5 MPa 평탄 소성** (그림 평균 ≈ 0.54).  ε 0.1 · 0.3 제하 → 선형 하강, 회복 ≈ 0.008–0.009 (digitized) · 제하 기울기는
  "slightly" 커진다고 했지만 안내선으로는 **≈ 2 배** (52 → 109 MPa).
- derived(ours): MPM 단일 원판의 비선형은 같은 E · ν 를 쓴 짝 논문 Fig 1 (ε_yy < 0.17 직선) 과 다르다 — **판독 정의 차이** (σ = F/L vs σ_yy 미정의) 로
  보인다.  두 그림을 나란히 인용하지 말 것.

### 5.2 ★ 집합체 응력 (Fig 2) — 그리고 범례 모순
- stated (Fig 2 바로 옆 본문): *"In the MPM simulations, the relationship between stress and the cumulative strain is linear whereas in the BPM simulations,
  a non-linear increase of stress with ε′ is observed. … in the BPM simulations, the vertical stress grows at an increasing rate with ε′ as in the compaction
  of metallic powders [13].  Moreover, in both cases, the friction between particles has little effect on the deformation."* — **인쇄된 Fig 2 범례와 일치**.
- digitized: **빨간 원** ≈ 직선 (ε′ 0.28 에서 3.6–3.8 σ0, 열린 · 채운 원이 겹침) · **검은 삼각형** ≈ ε′ 0.25 에서 **15–17.5 σ0** 로 발산 (무마찰 열린 삼각형이
  ε′ 0.15–0.24 에서 마찰 있는 쪽보다 10–20 % 위).
- **그런데** Fig 3 범례는 반대 (빨간 원 = BPM) 이고, 다음 넷이 **"Fig 2 범례가 뒤바뀌었다"** 쪽을 가리킨다:
  1. **마찰 기전**: 저자 스스로 BPM 은 *"the friction force … can not be mobilized because these primary particles can rotate freely without dissipation"* —
     BPM 이면 마찰 / 무마찰 곡선이 겹쳐야 한다.  Fig 2 에서 겹치는 쪽은 **빨간 원**, 갈라지는 쪽은 **검은 삼각형**.
  2. **Fig 3 범례** (빨간 원 = BPM) 로 Fig 3a 를 읽으면 본문 서술 (BPM 마찰 무관 · MPM 무마찰 Z ↑) 과 **정확히 맞는다**.
  3. **Fig 3 문단의 기전 문장**: *"In the case of MPM particles, the behavior is linear elastic, and therefore the remaining small pores … can only be filled
     at much higher stresses … However, in the BPM simulations, the pores can be filled more efficiently by plastic deformation … for a much lower stress level."*
     → 발산하는 쪽 = MPM.
  4. **2022 후속 논문 (짝 카드)**: 같은 E · ν 의 **탄성 MPM** 원판 충전체에서 σ−σc 가 Φ → 0.98 근처에서 **발산**.
  - 반대 근거 1: Fig 2 바로 옆 본문 (위 인용).
  - ⇒ **판정 (추정)**: Fig 2 범례가 뒤바뀌었을 가능성이 크다 (근거 4 대 1) — 확정 불가.  어느 쪽이든 **두 본문 문단 중 하나는 틀렸다**.
- ⚠ 그리고 **σ/σ0 정규화**: σ0 가 방법마다 다르고 절대값이 없어, *"much higher stresses"* (Fig 3 문단) 를 Fig 2 로 검산할 수 없다.

### 5.3 배위수 · 충전율 vs 변형 (Fig 3)
- stated: Z 는 ε 와 함께 증가 · BPM 은 마찰 무관 · **MPM 은 무마찰에서 Z 가 약간 높다** · Φ 는 마찰과 무관하게 같다 · 최대 Z 5.5 · 재밍 ε ≈ 0.08 (Z ≈ 3,
  Φ ≈ 0.75) · Φ0 ≈ 0.8 까지 "fragile" (재배열).
- digitized: §3.3 표.  Φ(ε) 선형 맞춤 기울기 0.67 (빨간 원) vs 0.62 (검은 삼각형) — 검은 삼각형 (= Fig 3 범례로 MPM 탄성) 이 같은 ε 에서 덜 치밀
  (탄성 입자의 면적 감소로 읽힘 · 추정).
- derived(ours): Φ0 = 0.8 에서 Z ≈ **3.7–4.5** = 2D 무마찰 원판의 **등정 (isostatic) 값 4** 근처 — 저자의 "재밍 ε ≈ 0.08 (Z ≈ 3)" 은 **응력이 오르기 시작하는 점**이고
  √ 법칙의 기준 (Φ0 0.8) 이 실제 등정 재밍에 가깝다 (우리 해석 · 논문은 등정을 말하지 않는다).

### 5.4 배위수 붕괴 (Fig 4)
- stated: Z−Z0 을 Z1−Z0 로 정규화하면 *"all data points collapse on a function well-fitted by a power law.  Beyond Φ0, Z increases as (Φ − Φ0)^0.5 as in the
  case of emulsions and foams [1, 14] … quite robust and almost independent of the interaction potential, polydispersity and friction [14]."*
- digitized: **무마찰 계열은 √ 선 위 (평균 편차 ≈ 0)**, **마찰 계열은 평균 0.06–0.08 아래** — "almost independent of friction" 의 "almost" 가 이 크기다.

### 5.5 결론 (stated)
- RCP 를 넘는 일축 압축을 MPM · BPM 으로 분석 → 탄성 · 소성 입자 집합체 사이 *"several significant differences"* · Φ–Z 의 단순 멱법칙 (에멀전과 같음).

---

## 그림별 (원 캡션 요지 + MPM 관점)

> 그림 파일 = `litdb/figures/nguyen2017_mpm_bpm_deformable_particle_compaction/` · 300 dpi · 캡션 제외 · 벡터 그림.

1. **`fig_1.png`** — *원 캡션 요지*: 단일 입자 직경 압축의 수직 응력–누적 축 변형 (BPM · MPM).
   *MPM 관점*: MPM (탄성 E 10 MPa · ν 0.45) 은 작은 변형에서 2D Hertz 직선 (F = (π/4)E/(1−ν²)Rε, 그림 점선 기울기 4.92 MPa) 을 따르다 ε > 0.05 에서 벗어나고
   ε > 0.15 에서 더 낮은 기울기로 간다; BPM (강체 1차입자 1750 개 응집체) 은 ε ≈ 2 % 뒤 σ ≈ 0.54 MPa (digitized, 문턱 정의 F0/⟨a0⟩ = 0.5 MPa) 의 평탄 소성이고,
   ε 0.1 · 0.3 에서 제하하면 회복 변형 ≈ 0.008–0.009 뿐 (digitized).  점접촉 법칙이 대변형에서 깨지는 범위를 보여 후보 C (MDR) 의 단일입자 대조 대상이고,
   재설계 MPM 은 이런 단일입자 하중–제하 시험부터 검증해야 한다 (MPM 쪽 제하는 이 그림에 없다).
2. **`fig_2.png`** — *원 캡션 요지*: 응집 응력 σ0 (Φ0 = 0.8 기준) 로 정규화한 수직 응력 vs 기준 상태부터의 누적 수직 변형 ε′, 무마찰 · 마찰 충전체 (BPM · MPM).
   *MPM 관점*: 한 계열은 거의 직선 (ε′ 0.28 에서 ≈ 3.6–3.8 σ0), 다른 계열은 ε′ ≈ 0.25 에서 15–17 σ0 로 발산한다 (digitized).  ⚠ 인쇄된 범례 (빨간 원 = MPM) 가
   Fig 3 범례 (빨간 원 = BPM) 와 반대이고, 마찰 효과가 보이는 쪽 · Fig 3 문단의 기전 문장 · 2022 후속 논문의 탄성 MPM 발산 곡선은 모두 "발산 = MPM 탄성,
   직선 = BPM 소성" 을 가리킨다 → 방법 귀속은 추정으로만 인용.  탄성 입자는 마지막 작은 공극을 채우려 응력이 폭증하고 소성 입자는 완만하다는 대비는
   재설계 MPM 이 Φ → 1 근처 응력 곡선에서 점검할 두 극한이다.
3. **`fig_3.png`** — *원 캡션 요지*: (a) 평균 배위수 Z, (b) 충전율 Φ 를 시작부터의 누적 수직 변형 ε 의 함수로 (무마찰 · 마찰, BPM · MPM).
   *MPM 관점*: 재밍 ε ≈ 0.08 (Z ≈ 3, Φ ≈ 0.75), Φ = 0.8 은 ε ≈ 0.157, 최종 Z ≈ 5.2–5.5 (digitized).  MPM 은 마찰 없을 때 Z 가 0.2–0.3 높고 BPM 은 마찰 무관
   (1차입자가 자유 회전해 마찰이 동원되지 않음); Φ(ε) 는 입자 부피 보존에서 오는 운동학적 곡선이라 방법 비교로는 약하다.  우리 단일 속도장 MPM 에는 Z 자체가
   없으므로, A′ 에서 μ 를 바꿔 Z 를 보는 것이 접촉 처리의 첫 판별 시험이 된다.
4. **`fig_4.png`** — *원 캡션 요지*: 평균 배위수를 충전율의 함수로 (정규화 (Z−Z0)/(Z1−Z0) vs Φ−Φ0), 선 = (Φ−Φ0)^0.5 맞춤.
   *MPM 관점*: 정규화 초과 배위수가 두 방법 · 마찰 유무에 걸쳐 대체로 √ 곡선에 모인다 (거품 · 에멀전과 같은 지수) — 다만 digitized 로는 마찰 있는 계열이
   맞춤선보다 평균 0.06–0.08 아래.  재설계 MPM (A′) 과 DEM 이 같은 Z(Φ) 지수를 내는지가 교차검증 관측량이 되고, 우리 단일 속도장 MPM 은 이 관측량을 낼 수 없다.

**식 크롭** (선택 — 같은 폴더):
- `eq_01_bpm_attraction.png` — 식 (1) F_a = −F0(1+δ/a0)^(−γ).  *MPM 관점*: BPM 의 소성 문턱은 재료 σ_y 가 아니라 F0/⟨a0⟩ 로 정해지는 **수치 매개변수** —
  SE 에 쓰려면 σ_y 대신 F0 를 보정해야 하고, 입자당 1차입자 ≥ 200 개라 비용이 크다.
- `eq_02_hertz_disk.png` — 식 (2) F = (π/4)·E/(1−ν²)·R·ε.  *MPM 관점*: 2D 원판은 힘이 변형에 선형 — MPM 단일입자 곡선이 ε > 0.05 에서 이 직선을 벗어난다는 것이
  "점접촉 법칙은 대변형에서 못 쓴다" 의 수치 근거.  3D 구 (지수 3/2) 로 직접 옮기지 않는다.

---

## 6. Post-processing ★
- **응력**: 바닥 벽 힘 → σ0 정규화 (σ0 절대값 미기재).  단일 입자는 σ = F/L (L = 현재 수평 지름).
- **변형**: ε′ = ln(1 + Δh/h0) (기준 상태부터) · ε (시작부터) · 단일 입자 ε = ln(1 + d/R).  ⚠ 부호 · Δh 정의 미기재.
- **Φ**: 입자 부피 (면적) / 전체 — BPM 의 "입자 부피" 를 1차입자 합으로 보는지 응집체 외곽으로 보는지 **미기재** (내부 공극이 있으므로 중요).
- **Z**: 평균 배위수 — 20 % 변형 넘어서는 다각형 변 수로 해석.  접촉 판정 기준 **미기재**.
- ⛔ 없는 것: 격자 수렴 · 시드 앙상블 · 오차막대 · 곡률 · 응력장 · 힘사슬 · 집합체 제하 · 전달물성.

---

## 7. ★★ 우리 DEM + MPM 대비 (같음 · 다름 · 왜) → `our_dem_baseline.md`

| 축 | **이 논문** | **우리 DEM (LIGGGHTS)** | **우리 MPM (Taichi MLS)** | 판정 |
|---|---|---|---|---|
| 변형 입자의 표현 | (i) MPM 연속체 (탄성) · (ii) 강체 1차입자 응집체 (BPM) | 강체 구 + 겹침 δ | SE 물질점 (한 격자) · AM 격자 장애물 | 그들은 **두 가지를 같은 시험대에서** 비교 |
| 접촉 | CD · μ 0 / 0.5 · 입자 경계 유지 | hooke/hysteresis + 점착 · 마찰 있음 | **단일 속도장 — 닿으면 붙음** | ⚠ 우리 MPM 만 접촉이 없다 |
| 마찰 효과 | Φ(ε) 무관 · Z 에 0.2–0.3 · 응력 "little" | 접촉 마찰 (보정값) | 사실상 "무한 마찰 + 결합" | ⚠ 그들 시험 범위 (0 ↔ 0.5) 밖이 우리 MPM |
| 소성 | MPM 은 **없음** · BPM 은 응집체 재배열 | ✗ (δ 프록시 + 18× 연화) | ✅ J2 (완전소성) | |
| 단일 입자 곡선 | 탄성 MPM vs 2D Hertz (ε > 0.05 이탈) | 3D Hertz 형 접촉식 (hooke/hysteresis 선형) | — | DEM 접촉식의 대변형 한계 경고 |
| 배위수 | **절대 Z** (재밍 ≈ 3 · Φ0 ≈ 3.7–4.5 · 최대 5.2–5.5) + √ 법칙 | SE–SE CN 등 (3D) | ✗ | 2D ↔ 3D 숫자 비교 금지 · 지수만 |
| 제하 | BPM 단일 입자만 (회복 ≈ 0.008–0.009) | 진행 중 (DEM 언로딩 트랙 P1) | 부분 (300 → 90 MPa 재시작 기능) | 집합체 제하 자료 없음 |
| 전달물성 | ✗ | ✅ 접촉망 σ 삼중항 | ✅ STEP3 (CONTACT_FREE 가지) | 우리 고유 |
| 재하 Mach V/c_S | 0.085 (집합체) | — | ≈ 0.21 | 우리 쪽이 더 동적 |

**전이되는 것**: 입자별 접촉 MPM 에서 마찰 0 ↔ 0.5 의 효과 크기 (작다) · Z ∝ √(Φ−Φ0) 지수 · 점접촉 법칙의 대변형 이탈 (ε > 0.05, 2D) · BPM 의 구조적 결함.
**전이 금지**: Z 절대값 (2D) · Φ 값 · σ/σ0 (σ0 미기재) · F0 · γ · 1차입자 크기.

---

## 8. ★★ 깊은 인사이트

**① 마찰은 2 차, "붙음" 이 1 차일 가능성 (가설).**  입자별 접촉을 가진 MPM 에서 μ 0 ↔ 0.5 는 Φ(ε) 를 바꾸지 않고 Z 를 0.2–0.3, 응력을 "조금" 바꾼다.
우리 단일 속도장 MPM 은 그 범위 밖 — **분리 불가 + 결합 (인장 전달)** — 에 있다.  ⇒ A′ 설계에서 **마찰 계수 보정은 후순위**, **"붙음" 을 없애는 것
(입자별 장) 이 1 순위**다.  (짝 카드 §8-② 의 "결합 골격 → 연화 필요" 가설과 같은 방향.  2D · 재밍 직전 시작 조건의 결과임.)

**② Φ(ε) 는 방법을 가르지 못한다 — σ(Φ) 와 Z(Φ) 로 가른다.**  벽 변위 제어에서 입자 부피가 보존되면 Φ ≈ Φ′0 e^ε 는 **질량 보존 산술**이다 (저자 식).
네 계열이 Fig 3b 에서 겹치는 것은 모델 일치가 아니다.  우리 scaffold MPM 의 "기공률이 DEM 과 일치" 가 독립 정보가 아니었던 것 (`CDX-16`) 과 **같은 함정**.
⇒ 재설계 MPM 의 판별 관측량 = **σ(Φ) · Z(Φ) · 제하 되돌아옴**, 기공률 단독 일치는 증명서가 아니다.

**③ "재밍" 은 두 개다 — 지수를 쓰려면 먼저 정의를 고정한다.**  응력이 오르기 시작하는 점 (ε ≈ 0.08 · Z ≈ 3 · Φ ≈ 0.75) 과 √ 법칙의 기준 Φ0 = 0.8 (Z ≈ 4,
등정 근처 — 우리 해석) 이 다르다.  우리 DEM · A′ 에서 Z−Zc ∝ (Φ−Φc)^0.5 를 맞출 때 Φc · Zc 를 어느 정의로 잡는지가 지수를 바꾼다 → **결과 전에 등록**.

**④ BPM 은 SE 모델로 쓰지 않는다 — 결함 셋이 이 논문에 스스로 적혀 있다.**  (a) 소성 문턱 = F0/⟨a0⟩ — 재료 σ_y 가 아니라 수치 매개변수 · (b) 1차입자가 자유 회전해
**입자 간 마찰이 동원되지 않는다** (μ 를 넣어도 무효) · (c) **Φ ≈ 0.93 (변형 40 %)** 에서 응집체 내부 공극이 입자 사이 공극과 같은 크기가 되어 판독이 오염된다.
여기에 입자당 1차입자 ≥ 200 개 → 우리 SE 32,832 개면 ≥ 6.6 × 10⁶ 1차입자 (derived).  ⇒ "DEM 틀의 변형 입자" 대안은 **기각 사유와 함께 기록**만.

**⑤ 제하의 주역은 입자 내부 탄성이 아니라 접촉 열림일 수 있다 (카드 간 종합 · 우리 추론).**  이 논문의 BPM 소성 입자는 제하 시 변형의 ≈ 0.008–0.009 만 회복한다
(입자 수준).  `pycompact2025_dem_mpfem_workflow` 의 MPFEM 루프는 P → 0 에서 기공이 크게 반등하고 단면에서 **접촉 틈이 벌어진다**.  ⇒ 집합체 되돌아옴이 접촉 분리로
생긴다면, **분리가 불가능한 단일 속도장 MPM 은 제하를 원리적으로 과소평가**한다 — [DEM 우선 (수영)] 의 "가압부터 탈압까지" 목표가 A′ 를 요구하는 두 번째 이유.

**⑥ 비교 설계의 교훈 — 한 번에 한 축만.**  MPM (탄성) vs BPM (소성) 은 표현과 재료를 동시에 바꿨다.  2022 후속이 MPM 에 소성을 넣어 그 교란을 풀었다.
⇒ 우리 A′ 시험도 **재료 (E · ν · σ_y) 를 고정하고 접촉 표현만** 바꾼다 (짝 카드 §9 행동 1).

**⑦ 범례 모순은 우리 규율의 외부 사례.**  pycompact 의 (g)/(h) 패널 뒤바뀜과 같은 부류 — **방법 귀속을 인용할 때는 물리 (마찰 거동) 로 범례를 교차 확인**한다.

---

## 9. [DEM 우선 (수영)] 트랙 — 후보별 행동

| 후보 | 이 논문이 | 이유 |
|---|---|---|
| **A** (우리 MPM + 움직이는 강체 AM) | 약화 (간접) | 마찰보다 "붙음" 이 1 차라는 가설 (§8-①) 이 맞다면 A 는 핵심 결함 (SE–SE 결합) 을 그대로 둔다 |
| **A′** (다물체 / 다속도장 접촉 MPM) | **지지** | MPM + CD 에서 μ 0 / 0.5 가 실제로 돌아간다 (2D 300 입자) · 마찰 효과 크기의 기준점 · 접촉 세부는 [5] (미열람) |
| **B** (NSCD + FE) | 부분 지지 | 같은 CD 접촉 |
| **C** (MDR DEM) | 정보 제공 | 점접촉 (Hertz) 이 ε > 0.05 에서 깨지는 단일입자 곡선 (2D) — MDR 이 다루려는 영역의 문제 제기.  3D 대조는 아님 |
| **C′** (두 재료 항복캡 DEM) | 근거 없음 | BPM 은 항복캡 접촉식이 아니라 응집체 — 다른 축 |
| **(BPM 형 응집체 DEM)** | **기각 권고** | §8-④ 결함 셋 + 비용 |
| **D0** (LIGGGHTS 2세대) | 정의 경고 | Z(Φ) 지수를 맞추기 전 재밍 정의 고정 (§8-③) |

**구체 행동 (제안 — 1저자 비준 전)**
1. 짝 카드 행동 1 (2D 벤치마크) 에 **마찰 팔 μ = 0 / 0.5** 를 더한다 — 이 논문 설정 (원판 300 · 지름 1.4–2.4 mm · 위 벽 5 m/s = V/c_S 0.085 · Φ′0 0.7) 에서
   **A′ 의 무마찰 Z 가 마찰보다 0.2–0.3 높은지** (digitized 기준점) 가 접촉 알고리즘의 첫 판별 시험.  단일 속도장은 Z 를 못 내므로 이 팔은 A′ 전용.
2. **단일 입자 하중–제하 시험** (Fig 1 꼴) 을 재설계 MPM 의 첫 검증에 넣는다 — 회복 변형을 재고, 집합체 제하에서 **입자 회복 ↔ 접촉 열림**의 몫을 나눠 보고
   (§8-⑤ 가설의 시험).
3. Z(Φ) 지수 분석 (DEM · A′) 전에 **재밍 정의 (응력 시작 / 등정 Z / 맞춤 Φc) 를 결과 전 등록**.
4. Fig 2 를 인용할 때는 **표식으로** 적고 범례 모순을 함께 적는다.
5. BPM 형 응집체는 SE 후보에서 **기각 기록** (§8-④).

---

## 10. 인용 가능 문장 (deck / paper 용)
- DEM 의 자유도 (p.1): *"Discrete Elements Methods (DEM) (like Contact Dynamics (CD) [3, 4]) often used for hard particles, are based on the approximation of small strains of
  contacts between particles.  Thus, the only degrees of freedom considered in these techniques are those of particles (displacements and rotations).  For soft particles, in
  contrast, it is necessary to take into account the internal degrees of freedom of each individual particle as well as the contact interactions."*
- MPM 은 접촉 처리가 따로 필요 (p.2): *"The important point for the treatment of soft particles with MPM is the necessity of coupling it with the CD approach for a rigorous
  treatment of frictional contacts."*
- 점접촉의 끝 (p.3): *"Above 20% of deformation, the particles are so much deformed that the contacts can no more be modeled as point contacts."*
- 우리 1-liner (defensible): *"입자별 접촉을 가진 2D MPM 에서 입자 간 마찰 (0 ↔ 0.5) 은 충전율–변형 관계를 바꾸지 않고 배위수를 0.2–0.3 바꿀 뿐이다 (Nguyen 2017) —
  단일 속도장 MPM 의 문제는 마찰 부재가 아니라 접촉의 '붙음' 일 수 있다 (가설)."*

---

## 11. 주의 · 한계 · PDF 가 말하지 않는 것

- **Fig 2 범례 ↔ Fig 3 범례 모순**, 그리고 **Fig 2 문단 ↔ Fig 3 문단** 의 서술 충돌 (§5.2).  어느 쪽이 맞는지 PDF 만으로 확정 불가.
- **σ0 절대값 없음** — 정규화 응력으로는 두 방법의 절대 응력 비교 불가.
- **MPM 은 탄성뿐** → "탄성 vs 소성" 과 "MPM vs BPM" 이 교란.
- **Φ = Φ′0 e^ε** 는 ε = 0.45 에서 1.10 (> 1) 이 되어 그림 (0.99) 과 맞지 않는다 — 선형화로만 쓰라 · ε · ε′ 의 Δh 부호 · 정의 미기재.
- "40 % of deformation ↔ Φ 0.93" 은 Fig 3b (ε 0.40 → Φ ≈ 0.96) 와 맞지 않는다 — "deformation" 의 정의 미기재 (입자 변형으로 읽어야 할 수도).
- 집합체 **MPM 해상도 · 상자 폭 L · BPM 1차입자 크기 · F0** 미기재 — 단일 입자 1차입자 크기로는 지름 1.4 mm 입자에 ≈ 40–45 개뿐이라 "최소 200 개" 와 맞지 않는다
  (derived) → 집합체에서 1차입자를 줄였다면 σ_I = F0/⟨a0⟩ 가 바뀌는지 알 수 없다.
- "Maximum Z 5.5 in all simulations" ↔ digitized 검은 삼각형 5.2–5.4.  "friction has little effect" ↔ Fig 2 검은 삼각형 무마찰이 중간 구간 10–20 % 위 ·
  Fig 4 마찰 계열이 맞춤선 평균 0.06–0.08 아래 — "little" · "almost" 의 크기.
- 단일 입자 시험의 **시간 간격 미기재** · F0 의 2D 단위 (깊이당?) 미기재.
- 4 쪽 학회 논문 — 방법 세부는 [5] · [6] (미열람).  실험 검증 · 집합체 제하 · 3D · 강체 입자 혼합 없음.
- frame[4]: 이 논문 곡선은 **보정 표적이 아니다** (코드 검증 기준점) · frame[5]: 전달물성 (DEM 고유) 은 다루지 않는다.

---

## 12. 관련 카드 (중복 서술 금지 — 겹치면 넘김)
- `nezamabadi2022_mpm_cd_plastic_particle_compaction` — **짝 (같은 그룹 후속)**: 다중 격자 접촉 설명 · MPM 소성 · 해석 압밀식 · σ(Φ) 수치 · 우리 연화 기전 가설.
- `pycompact2025_dem_mpfem_workflow` — 하중–제하 기공 루프 · 제하 시 접촉 틈 벌어짐 (§8-⑤).
- `demirtas2021_mpfem_hollow_sphere_die_compaction` — MPFEM 마찰 · recoil · 접촉 개구.
- `zunker2024_mdr_contact_model_partI` · `zunker2025_dem_large_deformation_compaction` — 대변형 접촉 DEM (후보 C).
- `paulick2015_elastic_particle_properties_dem_review` — CD (강체) vs 연질 DEM 의 전단 비교 사례 (재배열이 탄성보다 지배).
- `devaucorbeil2020_mpm_after_25_years_review` — MPM 접촉 알고리즘 계보 (Bardenhagen 다물체).

---

## 🗨️ Q&A 로그
- (비어 있음)

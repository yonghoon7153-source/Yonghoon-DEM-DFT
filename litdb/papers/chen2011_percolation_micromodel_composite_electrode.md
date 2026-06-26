# 다분산 입경 복합전극의 유효물성 예측 — *해석적* percolation 미시모델 (CN·percolation·TPB·σ_inter/intra·hydraulic pore 닫힌식) — Chen (J. Power Sources 2011)

> slug `chen2011_percolation_micromodel_composite_electrode` · DOI `10.1016/j.jpowsour.2010.11.107` · type `continuum (analytic percolation micro-model — closed-form, NO mesh/particle sim)` · PDF `Chen_2011_JPowerSources_PercolationMicromodel_CompositeElectrode_PolydispersedPSD.pdf` · digested `2026-06-26` · status ✅
>
> ⚠ **맥락 = 고체산화물 연료전지(SOFC) 복합전극** (LSM 음극 / Ni–YSZ 양극, 전자전도 ed-상 + 이온전도 el-상 + 기공). **우리 배터리(LPSCl+NMC811) 가 아님.** 그러나 핵심은 **재료-무관 *해석적 percolation 미시모델***: **다분산 PSD**(정규분포)에 대한 percolated TPB 길이·hydraulic pore 반경·intra/inter-입자 전도도·**배위수(coordination number)·percolation 확률**의 *닫힌 해석식*. → **CN/percolation/PSD 물리는 우리 σ_ionic 의 CN²·φc·다중-크기 percolation 으로 직접 전이.**
>
> ★ **이 digest 의 핵심 위치(3줄):**
> (1) **Bielefeld 2019 의 *해석적 짝*.** Bielefeld = *수치* percolation(GeoDict stochastic-placement + Hoshen–Kopelman); Chen = **닫힌식** percolation 미시모델(random-packing 재구성의 *해석적 확장*, Bielefeld 의 ref[20] Kenney 와 검증). 두 논문이 같은 percolation 물리를 *수치 vs 해석* 두 길로 푼다.
> (2) **★ 우리 backlog-B3 의 *해석적-prior* 후보.** Chen 은 **다분산 binary 혼합의 배위수 Z_{k,ℓ}**(Eq 2), **percolation 확률 P**(Eq 7, Bouvard 계열의 일반화), **inter-입자 이온전도 σ^ter,eff**(Eq 10)를 *명시 닫힌식*으로 준다 → 우리 *측정* CN·percolation 의 **literature 해석적 교차검증 / analytic prior**.
> (3) **★ 다분산 핵심 결과(general-physics, 전이 가능):** 다분산(정규분포 σ'=σ/r̄=0.4) → percolated TPB 가 단분산 대비 **~32 % 감소**(σ'=0.6 → 48 % 감소). **큰 평균반경 + 좁은 PSD → 높은 inter-입자 이온전도 + 낮은 percolation 임계**. ⇒ "분산이 percolation 망을 *약화*시킨다 + 재료-간 입경 대비가 임계를 낮춘다" 라는 **분포 효과의 해석적 정량** = Bielefeld 가 *비운 칸*(단봉만), 우리 bimodal 12:4:1 과 대조.
>
> 데이터 CSV: `docs/data/chen2011_percolation_micromodel.csv` (해석식 파라미터·CN·임계·TPB·σ vs PSD/조성). ⚠ SOFC 절대값(TPB, σ_YSZ)은 *재료-특이* → 배터리 절대 전이 금지; **CN/percolation/PSD *추세·해석식*만**.

---

## 1. 한 줄 요약 (bilingual)

**KO** — Chen 등(Jiangsu Univ. of Science & Technology + USTC + Colorado School of Mines, Robert J. Kee 그룹과 연계)이 **다분산 입경**을 가진 SOFC 복합전극의 유효물성(percolated TPB 길이·hydraulic pore 반경·intra/inter-입자 전도도)을 **해석적 percolation 미시모델**로 예측. 임의 M-성분 random-packed 구 혼합의 **배위수 Z_k = Σ Z_{k,ℓ}**(Eq 1–2, Bouvard/Suzuki 계열) + **다중-크기 percolation 확률 P**(Eq 7, mono-binary Eq 의 *n-크기 일반화*) 위에, percolated TPB(Eq 5–8)·effective intra-particle σ(Eq 9, Bruggeman ξ_el)·inter-particle σ(Eq 10, interface area + δ)·hydraulic pore 반경(Eq 11)을 *닫힌식*으로 유도. PSD 는 **정규분포(평균 r̄, 표준편차 σ)를 9개 크기로 이산화**(Eq 12–15)해 다룬다. **핵심 결론:** (i) 다분산(σ'=0.4)은 최대 percolated TPB 를 단분산 대비 **~32 % 낮춤**(σ'=0.6 → 48 %); (ii) **작은 평균입경 + 좁은 PSD → 높은 λ_TPB**(전극화학활성↑); (iii) **큰 r̄_el/r̄_ed 비 + 넓은 PSD → 높은 inter-입자 이온전도 + 낮은 percolation 부피임계**(Ni 응집 억제·장기내구성↑). 모든 물성을 *무차원 형태*로 제시(일반성). ⚠ **압밀역학·소성·형상변화 *전혀 없음*** — random-packing 기하 위의 해석 percolation 만.

**EN** — Chen et al. (Jiangsu Univ. of Science & Technology + USTC + Colorado School of Mines, linked to the R. J. Kee group) develop an **analytic percolation micro-model** to predict the effective properties (percolated triple-phase-boundary [TPB] length, hydraulic pore radius, intra/inter-particle conductivities) of a SOFC composite electrode with **poly-dispersed particle sizes**. On top of the **coordination number Z_k = Σ Z_{k,ℓ}** of an arbitrary M-component random-packed sphere mixture (Eq 1–2, Bouvard/Suzuki lineage) and a **multi-size percolation probability P** (Eq 7, generalizing the mono-binary expression to *n* sizes), it derives closed-form expressions for percolated TPB (Eq 5–8), effective intra-particle σ (Eq 9, Bruggeman ξ_el), inter-particle σ (Eq 10, interface area + thickness δ), and hydraulic pore radius (Eq 11). The PSD is a **normal distribution (mean r̄, std σ) discretized into 9 sizes** (Eq 12–15). **Headlines:** (i) a poly-dispersed electrode (σ'=0.4) has its maximum percolated TPB **~32 % lower** than the mono-sized case (σ'=0.6 → 48 % lower); (ii) **small mean radius + narrow PSD → higher λ_TPB** (more electrochemically active); (iii) **large r̄_el/r̄_ed ratio + broad PSD → higher inter-particle ionic conductivity + lower percolation volume-fraction threshold** (suppresses Ni agglomeration, improves durability). All properties are given in *non-dimensional form*. ⚠ There is **no compaction mechanics / no plasticity / no shape change** — only analytic percolation on a random-packing geometry.

**이 논문의 위치 (우리 기준):** **Bielefeld 2019 의 해석적 형제.** Bielefeld 은 *수치* GeoDict 으로 percolation 클러스터를 *세고*, Chen 은 같은 percolation 물리를 **닫힌 해석식**으로 *계산*한다(random-packing 재구성의 해석적 확장, Bielefeld 의 검증 출처 Kenney ref[20] 와 동일 계보). ⇒ **우리 σ_ionic 의 CN²·φc·다중-크기 percolation 의 *해석적 cross-check / analytic prior*.** 단 (a) **SOFC 맥락**(TPB·이온/전자/기공 삼상; 우리 배터리는 TPB 가 직접 양 아님), (b) **σ 를 실제로 *닫힌식으로 푼다*** — 그러나 그건 *재료 intrinsic σ × percolation/geometry 인자* 형태의 **mean-field 근사**이지 우리 Kirchhoff/Holm 의 *각 접촉 저항을 푸는 exact 망 해*가 아님(frame[4] 위치). → **우리 DEM 이 *측정*하는 것(실제 CN·percolation·constriction σ)을 Chen 은 *해석적으로 근사*; 그 닫힌식 PSD-의존이 우리 cross-check.**

---

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (전극계) | 연구유형 |
|---|---|---|---|---|
| **Daifen Chen**ᵃ\*, Liu Luᵇ, Jiayu Liᵃ, Zidong Yuᵇ, Wei Kongᵇ, **Huayang Zhu**ᶜ | J. Power Sources **196** (2011) 3178–3185 | 10.1016/j.jpowsour.2010.11.107 | **SOFC 복합전극** — ed-상(전자전도, LSM 음극 또는 Ni 양극) + el-상(이온전도, YSZ) + 기공. **재료-무관 *해석 모델***(LSM/YSZ·Ni/YSZ 예시) | **해석적 percolation 미시모델** (closed-form; random-packing 재구성의 해석적 확장). **순수 이론**(실험 없음; Kenney et al. ref[20] 수치 random-packing 결과와 검증) |
| ᵃ School of Naval Architecture and Ocean Engineering, **Jiangsu University of Science and Technology**, Zhenjiang 212003, China (corr. dfchen@mail.ustc.edu.cn) · ᵇ Dept. of Physics, **University of Science and Technology of China (USTC)**, Hefei 230026 · ᶜ Engineering Division, **Colorado School of Mines**, Golden, CO 80401, USA |

- 수신/수정/게재: 2010-09-22 / 2010-11-19 / 2010-11-22; online 2010-11-27.
- 감사: Jiangsu Univ. of Science and Technology grant 35011005; **Prof. Zijing Lin (USTC)** + **Prof. Robert J. Kee (Colorado School of Mines)** 의 percolation 이론 SOFC 응용 토론 감사 → Kee 그룹(SOFC 전산모델링 대가)과 연계.
- Keywords: Solid oxide fuel cell · Composite electrode · **Coordination number** · **Percolation theory** · Inter-particle conductivity · Triple phase boundary.
- **선행 자기 논문 Chen et al. ref[9] (J. Power Sources 191 (2009) 240)** = 3-성분 random-packed 시스템(LSM coarse/fine YSZ)의 percolation 미시모델 일반화 → **이 2011 논문 = 그것을 *다분산(연속분포)* 으로 확장**.

---

## 3. 핵심 수치 (numbers)

> ★ = digitized 아님, **본문/식 stated**. SOFC 라 "물성"은 percolated TPB(λ)·intra/inter-입자 σ(무차원)·hydraulic pore 반경·배위수·percolation 임계. **σ 절대값은 SOFC(YSZ) 라 배터리 전이 불가** — *추세·해석식·무차원형*만.

| 양 | 값 | 조건 | stated/digitized | 식·그림 |
|---|---|---|---|---|
| **★ 다분산 TPB 감소 (σ'=0.4)** | **~32 % 낮음** (vs 단분산) | r̄_ed=r̄_el, ψ_ed=0.5, max λ̃ | **stated** (본문 p.3181) | Fig 4 |
| **★ 다분산 TPB 감소 (σ'=0.6)** | **~48 % 낮음** (vs 단분산) | 〃 | **stated** | Fig 4 |
| ★ 비대칭 PSD TPB 감소 (σ'_ed=0.4, σ'_el=0) | **21 % 낮음** | 〃 | **stated** | Fig 4 |
| **★ 평균 배위수 (전체 입자)** ★ | **Z̄ = 6** | random-packing 가정 | stated (널리 채택) | Eq 2 (refs 21,22,33,34) |
| **★ percolation 임계 (mono-binary, 위 식)** | Z_{k,k} ≈ **1.764** (한 종끼리 접촉 1.764 → percolate) | 식 P_{el₁}=[1−((3.764−Z_{el₁,el₁})/2)^2.5]^0.4 | stated | (mono-binary, ref 22) |
| **★ percolation 임계 정수 (3.764)** | **3.764** (= 2×1.882 계열 상수) | Eq 7 분자 상수 | stated | Eq 7 |
| **★ percolation 부피임계 범위 (σ'=0)** | **ψ_ed ∈ [0.30, 0.70]** (단분산) | 양 상 percolate | stated 본문 | Fig 4 |
| **★ percolation 부피임계 범위 (σ'=0.4)** | **ψ_ed ∈ [0.20, 0.80]** (넓어짐) | 넓은 PSD | **stated** | Fig 4 |
| ψ^t_ed (σ'=0.4 비대칭 r̄_el/r̄_ed=0.5 예) | 0.46–0.82 (r̄비별 4종, 본문) | Fig 5 | stated | Fig 5 |
| ★ max λ̃_TPB 위치 이동 (r̄_el/r̄_ed↑) | ψ_ed *낮은*값→*높은*값 이동 | r̄_el>r̄_ed | stated | Fig 5 |
| ★ max λ̃_TPB (σ'_ed=σ'_el=0.4) vs mono | **25/32/25/25 % 낮음** (r̄_el/r̄_ed=0.5/1/2/4) | ψ_ed=0.5 | **stated** | Fig 5 |
| **★ percolation 임계 이동 (σ'=0→0.6)** | ψ^t_ed **0.30→0.18** 하강 (넓은 PSD) | Fig 6 | **stated** | Fig 6 |
| ★ intra σ̃ 회복 (ψ^t 낮아져) | σ̃^tra,eff_ed **0.59→0.72** | σ'=0→0.6, ψ_ed=0.18 채택 | **stated** | Fig 6 |
| ★ broad-PSD inter-σ 10 % 효과 | σ̃^ter,eff 약 **10 % 증가** (σ'=0.6 vs 0) | 넓은 PSD | **stated** | Fig 8 |
| ★ inter-σ 표준편차 효과 (좁은 PSD) | σ'≤0.4 **약함**, σ'=0.6 **무시 못 함** | Fig 8 | stated | Fig 8 |
| **★ 검증 조건 (Fig 3)** | θ=29.5°, φ_g=30 %, r̄_ed=r̄_el=0.25 µm | Kenney ref[20] 비교 | stated | Fig 3 |
| ★ 예시 λ_TPB,per 절대값 | **11.6 × 10¹² m⁻²** | θ=29.5°, φ_g=0.3, ψ_ed=0.5, r̄=0.25µm, σ'=0.4 | stated | Fig 5b |
| ★ YSZ specific inter-σ (Chan ref[21]) | σ^ter,0_el ≈ **0.05 S m⁻¹** @945 °C (비저항 20 Ω·m) | YSZ | stated (인용) | §3.4 |
| ★ inter-σ 두께 δ (YSZ) | **δ ≈ 5 nm** | YSZ 입계계면 | stated | §3.4 |
| ★ 예시 effective σ (945 °C) | intra σ^tra,eff_ed=**1953 S m⁻¹** / ion σ^ter,eff_el=**1.3 S m⁻¹** | φ_g=0.3, ψ_ed=0.5, r̄_ed=r̄_el=0.25µm, σ'=0.4 | stated | Fig 7+9 |
| ★ Chan ref[21] intrinsic σ (945 °C) | LSM σ^tra,0=**10⁴ S m⁻¹**(비저항 10⁻⁴ Ω·m) / YSZ σ^tra,0=**6.7 S m⁻¹**(비저항 0.15 Ω·m) | 945 °C | stated (인용) | §3.4 |
| 접촉각 θ | 29.5° (예시; θ는 자유 파라미터) | edₖ–elₗ 접촉 | stated | Eq 8, Fig 1 |
| PSD 이산화 | **9개 크기** (정규분포, 범위 −√2σ'+1 ~ √2σ'+1, step 2√2σ'/9) | Eq 12–15, Fig 2 | stated | Table 1, Fig 2 |
| PSD 9-크기 확률 (σ'=0.2) | 6.77/9.53/12.2/14.1/**14.8**/14.1/12.2/9.53/6.77 % | Table 1 (정규분포 이산) | stated | Table 1 |
| 무차원 표준편차 정의 | **σ' = σ/r̄** | PSD 폭 | stated | §3.1 |

**소재 주의:** SOFC(LSM/Ni–YSZ). **TPB(삼상경계 = 전자상·이온상·기공이 만나는 선)는 우리 배터리의 직접 양이 *아님*** (우리는 SE–CAM 면접촉·SE–SE 이온망). σ 절대값(YSZ 0.05–6.7 S/m)은 *재료-특이* → 배터리 전이 금지. **전이 가능한 것 = 배위수 해석식(Eq 1–2)·percolation 확률(Eq 7)·percolation 임계의 PSD 의존(Fig 4–6)·"넓은 PSD → 낮은 임계·약한 percolation" 라는 *분포 물리***.

---

## 4. 시뮬레이션 방법 ★

> ⚠ **이건 시뮬레이션이 아니라 *해석적 닫힌식* 모델이다.** mesh 없음·입자 동역학 없음·MC 없음. random-packing 통계(배위수)를 *해석식*으로 받아 percolation 확률·TPB·σ·pore 반경을 *대수적으로* 계산.

- **code / version**: **없음 (해석식).** 닫힌 해석식을 직접 평가(아마 in-house 스크립트, 미명시). **GeoDict·LIGGGHTS·FEM 류 *전혀 없음*.** ⇒ Bielefeld(GeoDict 수치) 와의 *방법론적 대척점* — 같은 percolation 물리를 *수치 vs 해석* 으로.
- **DEM 접촉법칙**: **없음.** 입자 간 힘·압밀 *전혀 없음*. 미시구조는 **random-packing 으로 *가정*** 되고(배위수 Z̄=6), porosity φ_g·부피분율 ψ 는 **입력**. 압력→porosity 관계 없음.
- **재료 파라미터**: percolation/기하 부분은 *재료-무관*. σ 계산에만 intrinsic 값 인용(YSZ σ^ter,0=0.05 S/m·δ=5 nm; LSM/YSZ intra σ Chan ref[21]). **E·ν·μ·COR·σ_y *전혀 없음*** (역학 모델 아님).
- **bond/binder 모델**: **없음** (SOFC — carbon/binder 무관; ed/el/pore 삼상만).
- **MPM/continuum**: **소성·형상변화 *전혀 없음*.** 입자 = *영원한 강체 구*. 단 **연속 PSD(정규분포)** 를 다룬다는 점이 Bielefeld(단봉) 와 차별 — 그러나 그건 *크기 분포*이지 *변형*이 아님.
- **전달 솔버 (σ)** ★ — ★ **핵심: σ 를 *닫힌식으로 푼다*, 단 mean-field.** Bielefeld(σ 안 풂) 와의 핵심 차이.
  - **Intra-particle (입자 내부) σ (Eq 9):** `σ^tra,eff_el / σ^tra,0_el = [ξ_el]^µ`, ξ_el = percolated electrolyte-입자의 **effective relative density** (Bruggeman 지수 µ). 단순 EMT/Bruggeman 형 — *입자 내부* 전도(전자/이온).
  - **Inter-particle (입자 간) σ (Eq 10):** `σ^ter,eff_el / σ^ter,0_el = Σ_k Σ_ℓ [2·a_{elₖ,elₗ}·n^V_{elₖ}·Z_{elₖ,elₗ}·P_{elₖ}] / δ`, a = 두 el-입자 간 **접촉 표면적**(πmin(r,r)²sin²θ), δ = 입계 계면 두께(YSZ 5 nm). ★ **이게 "접촉면적/두께"형 inter-입자 저항 = 우리 constriction 의 *해석적 사촌*** (단 우리 Holm R=1/(2σr_c) 의 *수렴저항 기하*가 아니라 *면적/두께* 박막 저항).
  - **Percolated TPB 길이 (Eq 5, 8):** `λ^V_TPB,per = Σ_k Σ_ℓ l_{edₖ,elₗ}·n^V_{edₖ}·Z_{edₖ,elₗ}·P_{edₖ}·P_{elₗ}`, l = 접촉 둘레(2π·min(r_ed,r_el)·sinθ). = 두 상이 *모두 percolate* 한 곳의 TPB 만 셈.
  - **Hydraulic pore 반경 (Eq 11):** `r_g = (2/3)·[φ_g/(x(1−φ_g))]·(Σψ_{edₖ}/r_{edₖ} + Σψ_{elₗ}/r_{elₗ})⁻¹` — Dusty-Gas 다공질 가스수송용(SOFC); x = 고체표면-기공 경계면적 분율(조정 인자).
  - ⚠ **모두 "intrinsic σ × percolation/geometry 인자" 의 *mean-field* 형** — *각 접촉의 저항을 풀어 Kirchhoff 로 합치는 우리 망 해가 아님.* frame[4] 에서 *해석적 근사 ≠ exact 망 해.*
- **입자 처리** ★ (DEM판 "무질서 처리" 대응):
  - **구 입자만 (random-packed), *다분산 PSD*.** ★ **Bielefeld 와의 핵심 차별 = 연속 PSD.** 각 재료(ed·el)의 입경을 **정규분포(평균 r̄, 표준편차 σ)로 가정 → 9개 크기로 이산화**(Eq 12–15, Fig 2; 범위 −√2σ'+1 ~ √2σ'+1, step 2√2σ'/9). 각 크기의 정규화 확률 p_k(Table 1)·부피분율 ψ_k(Eq 15) 산출. ⇒ **다분산을 *명시적으로 다루는* percolation 미시모델** (mono+binary 의 *n-크기 일반화*).
  - **rigid 입자만 — CONTACT 소성도, SHAPE 소성도 *없음*.** percolation 은 *배위수 통계 + 확률식*이지 *접촉 변형*이 아님. 겹침·overlap 개념조차 없음(접촉 = 둘레/면적 기하).
  - **배위수 = 통계 가정.** 전체 평균 Z̄=6(random dense-pack, refs 21,22,33,34) → 종별 Z_{k,ℓ}(Eq 2)·종합 Z_k(Eq 1) 해석식. **percolation 확률 P(Eq 7)** 는 Z 의 함수 — *공간 클러스터 라벨링(Hoshen–Kopelman) 안 함*, 순수 *해석식*. (Bielefeld 은 *실제 클러스터를 라벨링*; Chen 은 *확률식으로 추정*.)
  - **percolation 식별 = 확률식(Eq 7).** "전체 입자와의 평균 접촉수 Z_{elₖ}=Σ_ℓ Z_{elₖ,elₗ} 가 임계(≈1.764 same-type 또는 일반화)를 넘으면 percolated cluster 에 속함." Bouvard 계열(ref[32])·Suzuki(ref[31]) random-packing 연구의 *확률 닫힌식* — Kenney ref[20] 수치 결과로 검증(Eq 7).
- **도메인/RVE / seeds / 압력범위**: **없음** (해석식 — RVE·seed·압력 무관). 단 검증(Fig 3)은 Kenney et al. ref[20] 의 *수치 random-packing 재구성* 결과(points)와 *해석 모델*(lines)을 비교.
- **특이사항/튜닝**: (i) 모든 물성을 **무차원 형태**(λ̃_TPB, σ̃, r̄_el/r̄_ed)로 — 특정 입경·재료 무관 일반성; 물리값은 r̄·θ·φ_g·intrinsic σ 지정 시 추출. (ii) PSD 9-크기 이산화 시 누적확률<1 → 정규화 p_k/Σp_ℓ(Table 1 합 ≠ 100 % 보정). (iii) percolation 부피임계 ψ^t_ed < ψ_ed < 1−ψ^t_el (양 상 percolate 구간) — σ' 커질수록 *넓어짐*(Eq 7 의 Z 분포 평활화).

---

## 5. 섹션별 결과 — ALL numbers

### 5.0 Introduction / 동기 (p.3178–3179)
- SOFC 복합전극(전자전도 + 이온전도 재료 혼합)이 **반응영역을 dense electrolyte 에서 전극 내부로 확장** → 성능↑. **percolated TPB**(전자·이온·기공 삼상이 만나고 *모두* 망에 연결된 곳)에서만 전기화학반응. "percolated" 정의 = 전 구조를 가로지르는 *연속 연결*.
- 선행 3 부류: (i) **실험**(stereological/FIB-SEM, refs 10,11,14–16,25–29) — 비싸고 hard-to-access; (ii) **random-packing 재구성**(refs 17–20) — 구 입자 random-packing 으로 미시구조 재구성, *수치*(Ali ref19, Schneider ref18, Golbert ref17; **Kenney ref20 = 다분산 binary 재구성** = 이 논문 검증 출처); (iii) **percolation 미시모델**(refs 7,9,21–24) — percolation 이론 + 배위수로 random-packing 의 미시구조-물성 관계를 *해석식*으로. → "**미시모델 = random-packing 재구성의 *해석적 확장*, 충분히 정확하고 cell-level 모델 결합에 편리.**"
- **초기 연구(Costamagna ref22, Chan ref21, Janardhanan ref24)는 *단분산*만.** 그러나 SOFC 세라믹 분말은 *넓은 입경분포* → 유효물성에 큰 영향. **이 논문 = 다분산 입경(분포) 복합전극의 percolated TPB·intra/inter-입자 σ·미시구조 파라미터를 *해석적으로* 예측 + Kenney random-packing 으로 검증.** 모든 물성 *무차원형*.

### 5.1 배위수 & 미시구조 파라미터 (Theory §2.1.1, p.3179)
- **Eq 1 — 종합 배위수:** k-종 입자와 *모든* 이웃 입자 간 평균 접촉수 `Z_k = Σ_{ℓ=1}^{M} Z_{k,ℓ}` (M = 전체 입경 종류 수, ed+el 합).
- **Eq 2 — 종-간 배위수(핵심 해석식):**
  `Z_{k,ℓ} = 0.5·(1 + r_k²/r_ℓ²)·Z̄·(ψ_ℓ/r_ℓ) / Σ_{k=1}^{M}(ψ_k/r_k)`
  — r_k = k-종 반경, **Z̄ = 전체 입자 평균 배위수 = 6**(random dense-pack, 널리 채택 refs 21,22,33,34), ψ_k = 전체 입자 중 k-종 부피분율. ⇒ **큰 입자(r_k↑) 가 작은 이웃(r_ℓ↓)을 더 많이 접촉**(1+r_k²/r_ℓ² 항); 작은 입자가 많을수록(ψ_ℓ/r_ℓ↑) 큰 입자 배위수↑. = **다분산 binary 의 배위수 닫힌식.**
  - ★ **이게 우리 측정 ⟨z⟩ 의 *해석적 사촌*** — Suzuki–Oshima(ref 31) random-packing 통계 기반. 우리 DEM 은 *실제 접촉 수*를 세고, Chen 은 *PSD 로부터 해석적으로 예측*.

### 5.2 유효물성 & percolation 확률 (Theory §2.1.2, p.3179–3180)
- 2-상: el(이온, YSZ) + ed(전자, Ni/LSM). 각각 *m·n개 크기*로 이산: ed₁..edₘ, el₁..elₙ (m+n=M). 부피분율 **ψ_ed = Σ ψ_{edₖ}, ψ_el = Σ ψ_{elₖ}** (Eq 3); 상 내부 상대분율 ψ⁰_{edₖ}=ψ_{edₖ}/ψ_ed (Eq 4).
- **Eq 5 — percolated TPB(부피당):** `λ^V_TPB,per = Σ_k Σ_ℓ l_{edₖ,elₗ}·n^V_{edₖ}·Z_{edₖ,elₗ}·P_{edₖ}·P_{elₗ}`
  - l_{edₖ,elₗ} = 접촉 둘레 ≈ **2π·min(r_{edₖ}, r_{elₗ})·sinθ** (Fig 1, θ=접촉각); n^V = 단위부피당 입자수; Z = 배위수(Eq 2); **P = percolation 확률**(양 상 *모두* percolate 해야 TPB 활성).
- **Eq 6 — 단위부피당 입자수:** `n^V_{edₖ} = (1−φ_g)·ψ_{edₖ} / (4π r³_{edₖ}/3)` (φ_g = porosity).
- **Eq 7 — 다중-크기 percolation 확률(핵심):**
  `P_{elₖ} = [ 1 − ((3.764 − Σ_{ℓ=1}^{n} Z_{elₖ,elₗ}) / 2)^2.5 ]^0.4`
  — **mono-binary 식 `P_{el₁}=[1−((3.764−Z_{el₁,el₁})/2)^2.5]^0.4`(Costamagna ref22)의 *n-크기 일반화*.** 여기서 분모의 **Z_{elₖ}=Σ_ℓ Z_{elₖ,elₗ}** = elₖ-입자가 *같은 상의 모든 크기* el-입자와 갖는 평균 접촉수. **상수 3.764** = percolation 임계 상수(같은 종끼리 ~1.882 접촉 × 2). ⇒ **Z_{elₖ} 가 임계 미만이면 P→0**(percolate 안 함), 넘으면 P→1. **Kenney ref[20] 수치 결과로 *검증***(Eq 7 validated).
- **Eq 8 — dense electrolyte 표면당 TPB:** `λ^S_TPB,per = Σ_k (2π r_{edₖ} sinθ)·n^S_{edₖ}·P_{edₖ}`; n^S_{edₖ}=(1−φ_g)ψ_{edₖ}·2π r²_{edₖ}/3 — *전극/dense-electrolyte 계면*의 TPB(전기화학반응은 *복합전극 내부 + 계면* 양쪽).
- **Eq 9 — effective intra-particle σ:** `σ̃^tra,eff_el = σ^tra,eff_el / [σ^tra,0_el·(1−φ_g)^µ] = [ξ_el]^µ` (Eq 18 무차원형), ξ_el = percolated el-입자의 effective 상대밀도, **µ = Bruggeman 인자**(tortuous 전도경로). σ^tra,0 = intrinsic. ⇒ *입자 내부* 전도(전자·이온 동형).
- **Eq 10 — effective inter-particle 이온 σ(핵심):**
  `σ̃^ter,eff_el = σ^ter,eff_el / [σ^ter,0_el·sin²θ·(1−φ_g)/δ] = Σ_k Σ_ℓ 2·a_{elₖ,elₗ}·n^V_{elₖ}·Z_{elₖ,elₗ}·P_{elₖ}` (Eq 19 무차원형)
  - a_{elₖ,elₗ} = 두 el-입자 간 **접촉 표면적** = π·(min(r_{elₖ},r_{elₗ})·sinθ)²; **δ = 입계 계면 두께**(YSZ 5 nm). ★ **= "접촉면적 × 접촉수 / 두께" 형 inter-입자 저항** — *세라믹(YSZ)에서 입자-간 이온전도가 입계저항·계면면적·두께에 강의존*(특히 중저온, ref 35). ⇒ **우리 Holm constriction 의 *해석적 사촌*(단 박막-면적형, 수렴저항형 아님).**
- **Eq 11 — hydraulic pore 반경:** `r_g = (2/3)·[φ_g/(x(1−φ_g))]·(Σ_k ψ_{edₖ}/r_{edₖ} + Σ_ℓ ψ_{elₗ}/r_{elₗ})⁻¹` (Dusty-Gas 다공질 가스수송용; x = 조정 인자).

### 5.3 다분산 PSD 처리 (Theory §2.2, p.3180–3181)
- 실 복합전극은 ed·el *둘 다 불균일 PSD*. **정규분포 채택**(다른 분포도 동형 가능):
  - **Eq 12 — 확률밀도:** `f = (1/(σ√2π))·exp[−(r−r̄)²/(2σ²)]` (평균 r̄, 표준편차 σ).
  - **Eq 13 — 구간확률:** `p = ∫_{r1}^{r2} f(r)dr`; **Eq 14 — 무차원형:** r/r̄ 변수로, `p = ∫ f'(r/r̄)d(r/r̄)`, **무차원 표준편차 σ' = σ/r̄**.
  - **Fig 2 + Table 1 — 9-크기 이산화:** σ'=0.2 예시. **범위 −√2σ'+1 ~ √2σ'+1 을 9구간**(step 2√2σ'/9; 양 끝에서 f'(−√2σ'+1)=f'(√2σ'+1)=(1/e)f'(1) 이 되도록). Table 1: 9-크기 무차원 반경 r/r̄ = [1−8√2σ'/9, ..., 1, ..., 1+8√2σ'/9], 확률 p = **6.77/9.53/12.2/14.1/14.8/14.1/12.2/9.53/6.77 %**(중앙 최대 14.8 %, 정규분포 이산).
  - **누적<1 보정:** 9-크기 cumulative <1 → 정규화 **p_k/Σ_{ℓ=1}^9 p_ℓ**.
  - **Eq 15 — 크기별 부피분율:** `ψ_k = p_k r²_k / Σ_{ℓ=1}^9 p_ℓ r²_ℓ` (확률 × 반경²로 가중 — 부피~r³이나 여기선 r² 가중 정규화; 표면적/접촉 기반).
- ⇒ **단 2 파라미터(r̄, σ')로 각 재료 PSD 완전 지정** → 다분산 유효물성 *해석 계산*. **이게 Bielefeld 가 *미룬* 분포 처리를 *명시적으로* 한 부분.**

### 5.4 모델 검증 (Results §3.1, Fig 3, p.3181)
- **Fig 3:** percolated TPB λ^V_TPB,per vs ed-상 부피분율 ψ_ed. **조건: σ'_ed·σ'_el 각각, r̄_ed=r̄_el=0.25 µm, θ=29.5°, φ_g=30 %.** 3 곡선(σ'_LSM=σ'_YSZ=0 / σ'_LSM=0.4,σ'_YSZ=0 / σ'_LSM=σ'_YSZ=0.4) — *해석 모델*(lines) vs **Kenney ref[20] random-packing 재구성**(points). **good agreement** → 미시모델이 미시구조-물성 관계를 *정확히* 재현 확인.
- ★ **다분산 곡선의 *다중 전이*(transitions):** σ'_ed=0.4 또는 σ'_el=0.4 곡선에 *여러 transition* 출현 — **각 재료 PSD 가 9-크기로 표현되고 각 크기가 *다른 percolation 부피임계*(Eq 7)** 를 가져 발생. *더 많은 크기*로 표현하면 사라짐(이산화 인공물). σ'_ed=σ'_el=0.4 가 max λ̃ 를 단분산 대비 **32 % 낮춤**(피크값 비교).

### 5.5 percolated TPB 길이 (Results §3.2, Fig 4–5, p.3181–3182)
- 무차원: **Eq 16** `λ̃^V_TPB,per = Σ_k Σ_ℓ (3/2)·min(r_{edₖ},r_{elₗ})/r³_{edₖ}·(1−φ_g)·sinθ·ψ_{edₖ}·...·P·P` ; **Eq 17** `λ̃^V_TPB,per = λ^V_TPB,per/[(1−φ_g)sinθ/r̄²_ed]` — *r̄·θ·φ_g 무관*, σ'_ed·σ'_el·ψ_ed·(r̄_el/r̄_ed)만의 함수.
- **Fig 4 — σ'_ed·σ'_el 효과 (r̄_el/r̄_ed=1):**
  - σ' 증가 → **max λ̃ 유의 감소.** σ'_ed=σ'_el=**0.4 → 32 % 낮음**, **0.6 → 48 % 낮음** (vs σ'=0 단분산, 같은 r̄·ψ_ed=0.5). σ'_ed=0.4·σ'_el=0 (비대칭) → **21 % 낮음.**
  - r̄_ed=r̄_el·σ'_ed=σ'_el 면 **max λ̃ 위치 = ψ_ed=0.5**(대칭). σ'_ed≠σ'_el 면 이동: σ'_ed>σ'_el → ψ_ed>0.5 로, σ'_ed<σ'_el → ψ_ed<0.5 로.
  - **percolation 부피임계 ψ^t_ed < ψ_ed < 1−ψ^t_el** (양 상 percolate). **σ' 증가 → 임계범위 *넓어짐*:** σ'=0 → **[0.30, 0.70]**, σ'=0.4 → **[0.20, 0.80]**. (= 넓은 PSD 가 *더 넓은 조성*서 양 상 percolate 허용.)
- **Fig 5 — ψ_ed·r̄_el/r̄_ed 효과 (σ'_ed=σ'_el=0 [a] vs 0.4 [b]):**
  - r̄_el/r̄_ed↑ → max λ̃ 위치 ψ_ed 가 *높은→낮은* 값으로 이동(Fig 5a,b). **넓은 PSD(σ'=0.4) + 큰 r̄_el/r̄_ed → 더 넓은 percolation 부피임계 범위 ψ^t_ed~(1−ψ^t_el):** r̄_el/r̄_ed=0.5/1/2/4 → 0.46–0.82 / 0.30–0.70 / 0.18–0.54 / 0.10–0.37 (σ'=0) ; 넓은 PSD 면 0.32–0.89 / 0.20–0.80 / 0.11–0.68 / 0.06–0.51.
  - max λ̃ (σ'_ed=σ'_el=0.4) vs 단분산 = **25/32/25/25 % 낮음** (r̄_el/r̄_ed=0.5/1/2/4).
  - 절대값 예: θ=29.5°, φ_g=0.3, ψ_ed=0.5, r̄_ed=r̄_el=0.25µm, σ'_ed=σ'_el=0.4 → λ^V_TPB,per = **11.6 × 10¹² m⁻²** (Eq 17 역산).
  - **결론:** 작은 평균입경(r̄_ed,r̄_el) + 좁은 PSD → 높은 λ̃_TPB,per → 전극화학활성↑(SOFC 음극은 TPB 단위당 교환전류 낮아 *높은 λ_TPB 필요*) → **작은 평균입경·좁은 PSD 가 최적**(전극화학).

### 5.6 effective intra-particle σ (Results §3.3, Fig 6–7, p.3182–3183)
- 무차원 **Eq 18** σ̃^tra,eff_ed = σ^tra,eff_ed/[σ^tra,0_ed(1−φ_g)^µ]; 이온도 동형(σ̃^tra,eff_el).
- **Fig 6 — σ̃^tra,eff vs ψ_ed·σ'_ed·σ'_el (r̄_el/r̄_ed=1):**
  - ψ_ed↑ → σ̃^tra,eff_ed↑(전자); percolation 부피임계 ψ^t_ed 아래는 σ̃=0. σ'↑ → **ψ^t_ed *하강*** (예 σ'=0→0.6 → **ψ^t_ed 0.30→0.18**). ⇒ 넓은 PSD = *낮은 임계*서 percolate.
  - ★ **이온전도(σ̃^tra,eff_el)는 ψ_ed↓(=ψ_el↑) 면 증가.** SOFC 음극(Ni/YSZ)은 항상 *높은 이온전도* 위해 ψ^t_ed *근방* 채택. 넓은 PSD 가 ψ^t_ed 를 낮춰(0.30→0.18) → **낮은 ed-분율서도 양 상 percolate** → 이온전도 회복: **σ̃^tra,eff_ed 0.59→0.72**(ψ_ed=0.18 채택 시).
- **Fig 7 — σ̃^tra,eff vs ψ_ed·r̄_el/r̄_ed (σ'_ed=σ'_el=0.4):** r̄_el/r̄_ed↑ → 주어진 ψ_ed 서 σ̃^tra,eff_ed↑(Fig 7a), σ̃^tra,eff_el↓(Fig 7b). r̄_el/r̄_ed=1→4 → ψ^t_ed 0.22→0.1 로 더 하강 → 낮은 ψ^t_ed 서 높은 intra σ.
- ★ **예시 절대값(945 °C):** φ_g=0.3, ψ_ed=0.5, r̄_ed=r̄_el=0.25µm, σ'_ed=σ'_el=0.4 → **σ^tra,eff_ed = 1953 S m⁻¹**(전자, LSM intra 10⁴ 기준 Fig 7a) / **σ^tra,eff_el = 1.3 S m⁻¹**(이온, YSZ intra 6.7 기준 Fig 7b). (Chan ref21 intrinsic: LSM 10⁴ S/m·비저항 10⁻⁴ Ω·m / YSZ 6.7 S/m·비저항 0.15 Ω·m.)

### 5.7 effective inter-particle σ (Results §3.4, Fig 8–9, p.3183–3184)
- 전자상(ed)은 inter-입자 저항 *무시 가능*(금속/전자전도 좋음, ref9); 그러나 **이온상(el, YSZ) inter-입자 이온전도는 *전체 이온전도에 결정적***(특히 중저온, ref35) — 입경·도핑·계면면적·두께(δ)에 강의존.
- 무차원 **Eq 19** σ̃^ter,eff_el = σ^ter,eff_el/[σ^ter,0_el·sin²θ·(1−φ_g)/δ] (δ_YSZ=5 nm).
- **Fig 8 — σ̃^ter,eff_el vs ψ_ed·σ'_ed·σ'_el (r̄_el/r̄_ed=1):** ψ_ed↑ → σ̃^ter,eff_el↓ (el-분율↓). **좁은 PSD(σ'≤0.4) → σ' 효과 *약함*; 넓은 PSD(σ'=0.6) → *무시 못 함*** (broad-PSD 가 mono 대비 **약 10 % 증가**). + percolation 임계 1−ψ^t_el 한계(그 위 σ̃^ter,eff_el=0) 도 σ'=0→0.6 면 *상승*.
- **Fig 9 — σ̃^ter,eff_el vs ψ_ed·r̄_el/r̄_ed (σ'_ed=σ'_el=0.4):** r̄_el/r̄_ed↑ → σ̃^ter,eff_el *증가*(주어진 ψ_ed). 무차원형은 입경 무관이나 **물리 σ^ter,eff_el ∝ 평균입경**(접촉면적 ~r²) → **큰 평균 el-입경 → 높은 inter-입자 이온전도.**
- ★ **예시(Chan ref21):** YSZ specific inter-σ σ^ter,0_el≈**0.05 S m⁻¹**(비저항 20 Ω·m, 945 °C). θ=29.5°, φ_g=0.3, ψ_ed=0.5, r̄_ed=r̄_el=0.25µm, σ'=0.4 → **σ^ter,eff_el = 0.87 S m⁻¹**(Fig 9). ⇒ inter-입자 이온전도(0.87)가 intra-입자 이온전도(1.3 S/m)와 *같은 자릿수* → **inter-입자가 전체 이온전도에 *결정적 역할*.**
- **결론(Itoh ref40, Kim ref41 와 정합):** **큰 r̄_el/r̄_ed + 넓은 PSD(σ'↑) → 높은 σ^ter,eff_el + 낮은 percolation 부피임계 ψ^t_ed** → **Ni 입자 응집 억제 + 장기 내구성↑.** 단 큰 r̄_el/r̄_ed·넓은 PSD 는 *낮은 λ_TPB*(전극화학활성↓) → **trade-off**: σ^tra,eff·σ^ter,eff 는 큰 r̄_el/r̄_ed·σ'↑ 가 유리(ψ^t_ed↓·σ^ter,eff↑), λ_TPB 는 작은 입경·좁은 PSD 가 유리.

### 5.8 Summary & conclusions (p.3184–3185)
- 다분산 SOFC 복합전극 유효물성(intra/inter-입자 σ, percolated TPB λ^V/λ^S, hydraulic pore r_g) 의 *해석 percolation 미시모델* 확립; 미시구조 물리(평균입경·표준편차·intrinsic σ·porosity)에 의존; cell-level 모델 결합 편리; **Kenney random-packing 으로 검증.**
- ★ **3 핵심 설계 결론:**
  1. **작은 평균입경 + 좁은 PSD → 높은 λ_TPB,per** (전극화학활성↑).
  2. **다분산은 max λ_TPB 를 단분산 대비 ~32 %(σ'=0.4) 낮춤** — *분포가 percolated TPB 를 약화*.
  3. **큰 r̄_el/r̄_ed + 넓은 PSD → 높은 inter-입자 이온전도 + 낮은 percolation 부피임계** → Ni 응집 방지·내구성↑(Itoh/Kim 정합).

---

## 6. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | 복합전극 모식(coarse/fine el-입자 + ed-입자) + edₖ–elₗ 겹침 확대(접촉각 θ, 접촉 둘레/면적) | 접촉 둘레 l=2π·min(r)·sinθ·면적 a=π(min(r)sinθ)² — *접촉 기하* 정의(우리 Holm r_c 와 대비) |
| **2** | 정규분포 확률밀도 vs r/r̄ (σ'=0.2), 9구간 색분할 이산화 | ★ **다분산 PSD 처리법** — Bielefeld 가 *미룬* 분포를 *명시 이산화*. 우리 AM_P/AM_S/SE 다중-크기와 대조 |
| **3** ★ | percolated TPB λ^V vs ψ_ed; *해석 모델(lines)* vs *Kenney random-packing(points)* 검증; 3 σ' 조합; 다분산 곡선 *다중 transition* | ★ **해석식이 수치 random-packing 과 일치** = Chen 모델 신뢰 근거; 다중-transition=9-크기 임계 이산 인공물 |
| **4** ★ | λ̃^V_TPB,per vs ψ_ed·σ'_ed·σ'_el (r̄비=1) — σ'↑ → max 32 %(0.4)/48 %(0.6) 감소, 임계범위 [0.30,0.70]→[0.20,0.80] 확대 | ★ **다분산이 percolation 약화 + 임계 *넓힘*의 정량** = Bielefeld 단봉 빈 칸; 우리 bimodal dip 과 *반대 방향*(분산↓ vs 우리 분산↑ packing 이득) |
| **5** ★ | λ̃^V_TPB,per vs ψ_ed·r̄_el/r̄_ed (σ'=0 [a]/0.4 [b]) — r̄비↑ → max 위치 이동·임계범위 확대; max 25/32/25/25 % 감소 | ★ **재료-간 입경 대비(r̄_el/r̄_ed)가 임계·최적조성 이동** = 우리 SE/AM 입경비(12:4:1) percolation 효과의 해석 대응 |
| **6** ★ | σ̃^tra,eff vs ψ_ed·σ'_ed·σ'_el — σ'↑ → ψ^t_ed 0.30→0.18 하강, σ̃^tra,eff_ed 0.59→0.72 회복 | ★ **넓은 PSD → 낮은 percolation 임계 φc** = 우리 φc 의 PSD-의존 해석 근거(우리 φc_S=0.195/φc_P=0.200 = mono 가정) |
| **7** | σ̃^tra,eff vs ψ_ed·r̄_el/r̄_ed (σ'=0.4) — r̄비↑ → intra σ_ed↑·σ_el↓, ψ^t_ed 0.22→0.1 | 입경비가 intra σ·임계 이동; 예시 절대 σ_ed=1953·σ_el=1.3 S/m@945°C |
| **8** | σ̃^ter,eff_el vs ψ_ed·σ'_ed·σ'_el — broad PSD(σ'=0.6) inter-σ +10 %, 좁으면 약함 | inter-입자 이온전도(YSZ) = 우리 Holm constriction 의 *해석 사촌*(면적/δ형) |
| **9** | σ̃^ter,eff_el vs ψ_ed·r̄_el/r̄_ed (σ'=0.4) — 큰 r̄_el/r̄_ed → inter-σ↑; 예시 σ^ter,eff_el=0.87 S/m@945°C | ★ **큰 평균 el-입경 → 높은 inter-입자 σ** + inter≈intra 자릿수(결정적) = 우리 SE 입경↑ 이온전도 대조 |
| Table 1 | 정규분포 9-크기 무차원 반경(r/r̄)·확률 p (σ' 함수): 6.77/9.53/12.2/14.1/14.8/... % | PSD 이산화 수치 — 우리 다중-크기 가중과 대조 |

> 모든 그림이 *percolation/기하/해석* — **σ 곡선은 *무차원형*(σ̃) 또는 예시 절대값(945 °C SOFC).** ⇒ 우리 σ_ionic(mS/cm)·Bazzoun 0.137 과 **직접 수치 비교 불가**(SOFC·YSZ·무차원). *추세·해석식·PSD 의존*만.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md`

| 항목 | 이 논문 (Chen 2011) | 우리 | 차이 / 이유 |
|---|---|---|---|
| 모델 종류 | **해석적 닫힌식** percolation 미시모델(random-packing 통계 위) | **수치 DEM(LIGGGHTS) + MPM(Taichi) + Kirchhoff/Holm 망 해** | analytic mean-field vs explicit-network — 우리는 *각 접촉을 푼다* |
| 구조 생성 | **random-packing *가정***(배위수 Z̄=6); porosity·조성=입력 | **process-physics**(DEM 압밀로 porosity *예측*; MPM 소성흐름) | 통계가정 vs bottom-up 형성 — 우리 NOVELTY |
| 압밀 역학 | **없음**(φ_g 지정) | DEM 접촉력·Heckel(P_y 138)·MPM J2 | 그들 porosity 는 *입력* → 우리 15.6 % 와 절대비교 금지 |
| 배위수 Z | **해석식 Z_{k,ℓ}=0.5(1+r_k²/r_ℓ²)Z̄·(ψ_ℓ/r_ℓ)/Σ(ψ_k/r_k)** (Eq 2); Z̄=6 가정 | **DEM 측정 ⟨z⟩**(실제 접촉 카운트) | ★ 그들 Z = *PSD 로부터 예측*, 우리 = *측정* → **frame[4] 해석적 cross-check** |
| percolation | **확률식 P=[1−((3.764−ΣZ)/2)^2.5]^0.4** (Eq 7); 임계=Z 함수 | **f_perc_x/y/z + f_p³ isotropy** (실제 spanning 검사) | 그들 = 확률 닫힌식, 우리 = 실제 클러스터; 임계 정량은 교차검증 |
| σ 산출 | **닫힌식으로 *푼다***(Eq 9 intra Bruggeman·Eq 10 inter 면적/δ) — 단 mean-field | **Kirchhoff Σ(φ_i−φ_j)/R=0 + Holm R=1/(2σr_c) 삼중항** | ★ 둘 다 σ 풂; 그들=mean-field 근사, 우리=exact 망 해 + 수렴저항 |
| inter-입자 저항 | **면적/두께형** a/δ (YSZ 입계 박막, Eq 10) | **constriction형** Holm 1/(2σr_c) (수렴저항) | 다른 저항 기하(박막 vs 수렴) — 우리 Stage-E 소성면적이 더 물리적 |
| 전달 채널 | 이온(el)·전자(ed) intra+inter + TPB | σ_ionic + σ_e + **σ_thermal** 삼중항 | 우리 열 우위(SOFC 도 열 안 풂) |
| 접촉면적 | **기하** a=π(min(r)sinθ)² (변형 없음) | **Stage-E 소성 접촉면적**(Tabor+volume) | 그들=기하상한; 우리=소성변형 면적 |
| 입자 형상 | rigid 구, **소성 없음** | DEM rigid + **MPM 진짜 SHAPE 소성** | morphology = 우리 MPM 고유 |
| PSD | ★ **다분산 명시(정규분포 9-크기 이산)** — Bielefeld 보다 *앞섬* | **bimodal 12:4:1** + 정량 Furnas dip | 둘 다 분포 처리; 그들=연속 정규분포, 우리=이산 bimodal+dip |
| 분포 효과 | **분산↑ → percolated TPB↓(~32 %) + 임계 *넓힘*** | **bimodal → packing↑(porosity↓)·dip** | ★ *방향 다름*: 그들 TPB(연결성)는 분산이 약화, 우리 packing(밀도)은 bimodal 이 강화 — *다른 양* |
| 검증 | **Kenney random-packing(수치)** 와 일치(Fig 3) | solver=ground truth + Bazzoun/Minnmann 실험 앵커 | 그들=수치 cross-check, 우리=실험 앵커 |
| 소재 | **SOFC LSM/Ni–YSZ**(TPB·삼상) | NMC811+LPSCl(SE–CAM 면접촉) | ★ TPB 는 우리 직접 양 아님; σ 절대 전이 금지 |

**핵심 차이 3줄:** (1) **둘 다 percolation+σ 를 다루나, 그들은 *해석적 mean-field*(배위수 통계 → 확률식 → intrinsic σ × 인자), 우리는 *exact 망 해*(각 SE–SE 접촉을 Holm 저항으로 → Kirchhoff)** — frame[4] 에서 Chen 닫힌식 = 우리 *측정* CN·percolation·σ 의 *해석적 근사/교차검증*; (2) **그들 inter-입자 저항은 *면적/두께 박막형*(YSZ 입계), 우리는 *수렴저항형*(Holm)** — 다른 저항 기하; (3) **PSD: 그들은 *연속 정규분포*를 명시(Bielefeld 단봉보다 앞섬), 우리는 *이산 bimodal 12:4:1*; 단 분포 효과의 *방향이 다르다* — 그들 "분산↑→percolated TPB↓"(연결성 약화)는 우리 "bimodal→packing↑·dip"(밀도 강화)와 *다른 양*(TPB 연결성 ≠ packing 밀도).** ⚠ **SOFC 맥락 + TPB 가 우리 직접 양 아님 + σ 절대값 SOFC** → percolation/CN/PSD *해석식·추세*만 전이.

---

## A. 우리 DEM+MPM 대비 (comparison vs ours) — 심층

### A.1 그들의 *해석적 배위수·percolation* vs 우리 *DEM-측정 CN·percolation + Kirchhoff σ*

**Chen 의 강점 = 닫힌식.** 그는 다분산 binary/n-크기 혼합의 **배위수**(Eq 2)·**percolation 확률**(Eq 7)·**inter-입자 σ**(Eq 10)를 *명시 대수식*으로 준다. random-packing 통계(전체 Z̄=6, Suzuki–Oshima ref31 계열)를 입력받아, 공간 시뮬레이션 *없이* 미시구조-물성을 계산. **Kenney et al.(ref20)의 수치 random-packing 재구성과 일치(Fig 3)** → 해석식이 *수치 결과를 재현*함을 검증.

우리 파이프라인은 *그것을 측정·정밀화*한다:
- **배위수:** Chen Eq 2 는 ⟨z⟩ 를 *PSD 로부터 해석적으로 예측*(Z̄=6 가정 위). 우리 DEM 은 압밀 후 **실제 접촉을 카운트**해 ⟨z⟩ 를 *측정* → Chen 식은 우리 측정값의 **literature 해석적 cross-check / analytic prior**. (우리 측정 ⟨z⟩ 가 Chen Eq 2 예측과 같은 부호·범위면 frame[4] 교차검증.)
- **percolation:** Chen Eq 7 은 percolation *확률*을 Z 의 닫힌식으로 추정(임계 상수 3.764). 우리는 **실제 spanning cluster** 를 검사(f_perc_x/y/z)·f_p³ isotropy. ⇒ Chen 임계 = 우리 φc·percolation 의 *해석적 근사*.
- **σ:** ★ **여기서 Chen 은 Bielefeld 와 다르다 — σ 를 *닫힌식으로 푼다*.** 그러나 (i) intra-입자 = **Bruggeman ξ^µ**(EMT), (ii) inter-입자 = **Σ(면적·접촉수·P)/δ**(박막 면적형) — *각 접촉을 풀지 않는 mean-field*. 우리는 **각 SE–SE 접촉을 Holm R=1/(2σr_c)(수렴저항)로 환산 → Kirchhoff Σ(φ_i−φ_j)/R=0 으로 푼다**(exact 망). ⇒ **Chen σ = 우리 σ 의 *해석적 mean-field 사촌*; 우리는 그 위 한 층(exact network + constriction).**

> 대응 매핑: 그들 **Z_{k,ℓ}(Eq 2)** ↔ 우리 **측정 ⟨z⟩ + CN²항**; 그들 **percolation 확률 P(Eq 7, 임계 3.764)** ↔ 우리 **f_perc/f_p³ + φc**; 그들 **inter-입자 σ(Eq 10, 면적/δ)** ↔ 우리 **Holm constriction(수렴저항)**; 그들 **intra-입자 σ(Eq 9, Bruggeman ξ^µ)** ↔ 우리 **σ_grain × percolation 백본**; 그들 **percolated TPB(Eq 5)** ↔ (우리 직접 대응 *없음* — 배터리는 TPB 가 양 아님; 가장 가까운 건 *active interface/coverage*).

### A.2 우리 σ_ionic CN² 항 vs Chen 의 배위수·percolation 닫힌식

- **우리 σ_ionic (T1, LOOCV 0.975):** `σ = σ_grain·Cronau(r_SE)·(φ_eff)^½·**CN²**·cov_Hertz^½·f_p³·C(τ)` — 여기 **CN²**(배위수 제곱 = Kirchhoff #paths × bond-strength, 데이터-locked 91/91) + **(φ_eff)^½**(mean-field 3D percolation, φc_S=0.195/φc_P=0.200).
- **Chen 대응:** 배위수 Z 가 percolation 확률 P(Eq 7)·TPB·σ 를 *직접* 구동 → "배위수↑ → percolate·전도↑" 가 *해석식으로* 박혀 있음. 우리 CN² 의 *물리적 정당화* = "배위수가 전도경로 수를 정한다" — **Chen Eq 7(P∝Z)·Eq 5(TPB∝Z·P)·Eq 10(σ_inter∝Z·P) 가 그 *해석적 근거*.**
- ★ **인용법:** "The coordination number directly drives percolation probability and inter-particle conductivity in the analytic micro-model (Chen 2011, Eq 2/7/10: P, λ_TPB, σ_inter all ∝ Z·P(Z)), underpinning our CN² term in σ_ionic." ⚠ 단 **우리 CN² 지수 2 = Chen 식과 *등치 주장 금지*** — Chen 은 P=[1−((3.764−ΣZ)/2)^2.5]^0.4 (다른 함수형); 우리 CN² 는 *데이터-locked*. "배위수가 percolation·전도를 구동한다는 *물리*의 해석적 근거" 까지만.

### A.3 percolation 임계 φc 의 PSD-의존 — 우리 mono φc vs Chen 의 "넓은 PSD → 낮은 임계"

- **우리:** φc_S=0.195 / φc_P=0.200 (FROZEN) — **구-SE *단봉* 가정**의 percolation 임계. CLAUDE.md 가 "φc 절대 재screen 금지" 명시.
- **Chen (Fig 4, 6):** ★ **넓은 PSD(σ'↑) → percolation 부피임계 *하강·범위 확대*** — σ'=0 → ψ^t_ed=0.30(범위 [0.30,0.70]); σ'=0.6 → ψ^t_ed=0.18(범위 [0.20,0.80] 이상). *해석적으로* "분산이 임계를 낮춘다"(작은 입자가 저-분율서 연결 다리 놓음, Eq 2 의 ψ_ℓ/r_ℓ 항).
- ★ **인사이트:** 우리 φc(mono)는 *단봉 가정*의 임계 — **다분산(우리 SE PSD 폭, AM_P/AM_S/SE 다중-크기)이면 Chen 해석식대로 *임계가 낮아질* 수 있다.** 우리 σ_ionic 의 **g_phys(power gate, r_AM_eff 의존)** 가 이미 *조성-가중 입경* 으로 φc_eff 를 움직이는데(φc_eff=(1−g)φc_P+g·φc_S), **Chen 의 "넓은 PSD→낮은 임계"가 그 *방향의 해석적 근거*.** ⚠ 절대값 전이 금지(SOFC·무차원) — *민감도 방향*(분산↑→φc↓)만. Bielefeld(단봉)는 이 분포 효과를 *비웠고*, Chen 이 *해석적으로 채운다*.

### A.4 다분산 vs 우리 bimodal — *다른 양*임을 명시 (over-claim 방지)

- **Chen 다분산 효과 = percolated TPB↓ (연결성 약화):** σ'↑ → max λ_TPB **~32 %↓**. 이유 = PSD 가 넓어지면 각 크기의 percolation 임계가 흩어져 *동시에 percolate 하기 어려워짐* → percolated TPB(양 상 *모두* 연결된 곳) 감소.
- **우리 bimodal 12:4:1 효과 = packing↑/porosity↓ + Furnas dip (밀도 강화):** 작은 SE 가 큰 AM 공극을 *기하 충전* → porosity↓ → σ↑. *밀도/패킹* 효과.
- ⇒ ★ **두 "분포 효과"는 *다른 양*이다.** Chen 의 λ_TPB(percolation 연결성)는 분산↑ 면 *약화*; 우리 packing(porosity)은 bimodal(특정 큰 입경비)면 *강화*. **모순 아님** — (i) Chen 은 *연속 정규분포 폭(σ')*, 우리는 *이산 2-모드(큰/작은 비)*; (ii) Chen 측정량 = TPB *연결성*, 우리 = *밀도*. 둘은 *직교 축*. 비교 시 *반드시* "TPB 연결성(Chen) ≠ packing 밀도(우리)" 명시. 실제로 Chen 도 **큰 r̄_el/r̄_ed(=큰 입경비, 우리 bimodal 의 *비* 축) → 낮은 임계·높은 inter-σ**(Fig 5,9)라 했으니, *입경비 축*에서는 우리 bimodal packing 이득과 *같은 방향*(큰 비 = 유리). ⇒ **"분산 폭(σ')은 TPB 를 약화시키나, 큰 *입경비*(r̄_el/r̄_ed)는 임계↓·inter-σ↑로 유리" = Chen 의 두 분포 축; 우리 bimodal 은 후자(입경비) 축에 해당.**

---

## B. 적용가능성 (applicability to our LIGGGHTS DEM model)

### B.1 ★ backlog-B3 의 *해석적-prior* 후보 (Bielefeld 수치 앵커와 짝)

우리 backlog-B3 는 "우리 √(φ−φc)·CN²·f_p³ percolation 지수를 *literature* 로 정당화"를 요구. **Bielefeld 2019(수치, β=0.41·p_c=7.83·ln(d)+36.67)가 1차 앵커**라면, **Chen 2011 은 *해석식* 짝**:

1. **배위수 해석식 Z_{k,ℓ}(Eq 2)** = 우리 측정 ⟨z⟩ 의 *analytic prior*. 다분산 binary 의 종-간 배위수를 닫힌식으로 → 우리 DEM 측정 ⟨z⟩ 와 부호·범위 비교(frame[4]). 인용:
   > "The analytic binary coordination number Z_{k,ℓ}=0.5(1+r_k²/r_ℓ²)·Z̄·(ψ_ℓ/r_ℓ)/Σ(ψ_k/r_k) (Chen 2011 Eq 2, Z̄=6 random-pack) provides an analytic prior for the DEM-measured ⟨z⟩ entering our CN² term."
2. **percolation 확률 P(Eq 7, 임계 3.764)** = 우리 f_perc/φc 의 *해석적 근거*. P∝Z → "배위수가 percolation 을 구동" 의 닫힌식. ⚠ 우리 (φ_eff)^½ 지수 0.5 ≠ Chen P 함수형 — *물리 방향*만.
3. **inter-입자 σ(Eq 10, 면적/δ·접촉수·P)** = 우리 σ_ionic 의 "배위수·접촉면적·percolation 이 σ 를 정한다"의 *해석적 mean-field 형*. 우리 CN²·cov_Hertz^½·f_p³ 의 곱-구조와 *질적 동형*(σ ∝ Z·a·P). 인용:
   > "The inter-particle ionic conductivity σ_inter ∝ Σ a·Z·P (Chen 2011 Eq 10) is the analytic mean-field counterpart of our σ_ionic ∝ CN²·cov^½·f_p³ — both make σ a product of coordination, contact area, and percolation probability; our Kirchhoff/Holm solve replaces the mean-field with an explicit constriction-resistance network."

### B.2 다분산-PSD 처리 → 우리 다중-크기(AM_P/AM_S/SE) percolation 의 해석 근거

- Chen 은 **연속 정규분포 PSD 를 9-크기로 이산화**(Eq 12–15, Table 1)해 percolation·σ 를 계산. 우리는 **AM_P·AM_S·SE 의 이산 다중-크기**(12:4:1)를 다룬다 — *구조적으로 같은 다중-크기 percolation 문제.*
- ★ **그들 결과가 우리 다중-크기 percolation 에 주는 해석:**
  - "넓은 PSD → percolation 임계 *하강*(ψ^t 0.30→0.18)" → 우리 SE 가 *분포 폭*을 가지면(또는 SE/AM 다중-크기) *임계가 낮아질* 수 있음 → 우리 φc_eff 의 g_phys(조성-가중 입경) 게이트와 같은 방향.
  - "큰 r̄_el/r̄_ed(입경비) → 임계↓·inter-σ↑" → 우리 **SE(작은)·AM(큰) 의 큰 입경비(12:1)** 가 *유리*(같은 방향) → 우리 bimodal packing 이득의 percolation 측 해석 근거(Bazzoun "작은 SE→σ↑", Minnmann "fine SE→σ_eff↑" 과 합류).
- ⚠ **SOFC→battery 매핑:** Chen 의 el(이온, YSZ)≈우리 SE(LPSCl), ed(전자, Ni/LSM)≈우리 AM(NMC811). 단 (i) **TPB 는 우리 양 아님**(우리 SE–CAM 면접촉·SE–SE 이온망), (ii) σ 절대값·δ(5 nm YSZ)·intrinsic σ 전이 금지. *CN·percolation·PSD 의 해석식·추세*만.

### B.3 우리 percolation feature 로의 매핑 (요약)

| 우리 feature | Chen 2011 대응 | 인용 근거 |
|---|---|---|
| 측정 ⟨z⟩ + CN² 항 | 배위수 Z_{k,ℓ} (Eq 2, Z̄=6) | 다분산 binary 배위수 *해석적 prior* |
| (φ_eff)^½ / φc | percolation 확률 P(Eq 7, 임계 3.764)·ψ^t | "Z 가 percolation 구동" 닫힌식 |
| φc 의 PSD-의존(g_phys) | 넓은 PSD → ψ^t 0.30→0.18 (Fig 6) | 분산↑→임계↓ *해석 근거* |
| f_p³ (3D isotropy) | percolated cluster(양 상 모두 연결) | percolation 존재 정의 |
| σ_ionic ∝ CN²·cov^½·f_p³ | inter-σ ∝ Σ a·Z·P (Eq 10, 면적/δ) | σ=배위수·면적·percolation 곱 *mean-field 동형* |
| Holm constriction(수렴저항) | inter-입자 박막저항 a/δ (Eq 10) | 다른 저항 기하(박막 vs 수렴) — 우리가 더 물리적 |
| SE/AM 입경비(12:1) 이득 | 큰 r̄_el/r̄_ed → 임계↓·inter-σ↑ (Fig 5,9) | 큰 입경비 유리 *같은 방향* |
| bimodal packing/porosity↓ | (Chen 양 아님 — 그는 TPB 연결성) | ⚠ *다른 양*(연결성≠밀도) — 동일시 금지 |

---

## C. frame[4]/positioning — 해석적 미시모델 (DEM 경쟁자 아님)

> evidence-based, over-claim 금지. Chen 은 **해석적 mean-field 모델** → DEM 의 *경쟁자*가 아니라 *해석적 짝/cross-check*. 우리 DEM 이 *측정·정밀화*하는 것을 Chen 이 *닫힌식으로 근사*한다.

**우리 DEM 이 *측정*하고 Chen 이 *해석적으로 근사*하는 것:**

1. **배위수 ⟨z⟩.** Chen Eq 2 = *PSD 로부터 예측*(Z̄=6 가정 위, random-packing 통계). 우리 DEM = 압밀 후 *실제 접촉 카운트*(압력·소성·재배열 반영). ⇒ Chen 식 = 우리 측정의 *해석적 prior/cross-check*; 우리 측정 = 그 가정(Z̄=6, random-pack)을 *압밀-특이*로 정밀화.
2. **percolation.** Chen Eq 7 = *확률 닫힌식*(공간 클러스터 라벨링 없음). 우리 = *실제 spanning cluster*(f_perc_x/y/z)·f_p³. ⇒ Chen 임계(3.764, ψ^t) = 우리 φc 의 *해석적 근사*; 우리는 *실제 망의 연결*을 본다.
3. **σ.** ★ **Chen 은 σ 를 *닫힌식으로 푼다*(Bielefeld 와 다름) — 단 mean-field:** intra=Bruggeman ξ^µ(EMT), inter=Σ a·Z·P/δ(박막 면적형). 우리 = **각 SE–SE 접촉 → Holm R=1/(2σr_c)(수렴저항) → Kirchhoff Σ(φ_i−φ_j)/R=0**(exact 망). ⇒ **Chen σ = 우리 σ 의 *해석적 mean-field 사촌*; 우리는 exact network + 수렴저항 + Stage-E 소성면적.**

**Chen 이 *해석적으로 제공*하는 cross-check (우리가 *측정*으로 확인):**

- ★ **닫힌식 PSD-의존.** Chen 은 percolation 임계·TPB·σ 의 *PSD(r̄, σ', r̄_el/r̄_ed) 의존을 명시 닫힌식*으로 → 우리 다중-크기(12:4:1)·SE-분포의 percolation/φc 효과를 *해석적으로 예측*하는 prior. (우리 DEM 은 *측정*으로, Chen 은 *닫힌식*으로 — 두 길이 같은 방향이면 frame[4] 교차검증.)
- ★ **"배위수가 percolation·σ 를 구동"의 해석적 증명.** Eq 2/7/10 이 Z→P→TPB·σ 를 *연쇄 닫힌식*으로 → 우리 CN² 항의 *물리적 정당화*.
- ★ **"넓은 PSD→낮은 임계 / 큰 입경비→낮은 임계·높은 inter-σ"** = 우리 g_phys(조성-가중 입경)·SE/AM 입경비 이득의 *해석 방향 근거*.

**Chen 이 *앞서는/가진* 것 (정직):**

- **닫힌식 = 빠르고 cell-level 결합 편리.** 공간 시뮬 없이 즉시 평가 — 우리 DEM(압밀+망 해)보다 *연산 비용*에서 압도적. (단 우리 σ predictor 스케일링 법칙[σ_ionic LOOCV 0.975 등]이 *우리* 즉시-평가 층 → 흡수보다 *해석적 prior 근거*로 사용.)
- **다분산 PSD 명시 처리.** ★ **Bielefeld(단봉)보다 *앞섬*** — 연속 정규분포를 9-크기로 이산화해 percolation/σ 의 *분포 의존*을 정량. = 우리 다중-크기 percolation 의 *해석 근거*.
- **σ 를 *닫힌식으로 푼다*(Bielefeld 와 차별).** intra(Bruggeman)·inter(면적/δ)·TPB 의 *분석적* σ — Bielefeld 가 "σ=future work" 로 미룬 것을 Chen 은 *해석적으로* (단 mean-field). ⇒ **percolation 모델 중 σ 를 푼 쪽** = 우리 Kirchhoff/Holm 의 *해석적 선행 형*.
- **SOFC percolation 미시모델의 정량 토대(2011).** random-packing 재구성의 *해석적 확장* + Kenney 검증 — 다분산 percolation 미시모델의 foundational 닫힌식.

**우리가 *앞서는* 것 (우리 DEM↔MPM novelty):**

1. ★ **exact 망 해 + 수렴저항.** Chen = mean-field(intrinsic σ × 인자); 우리 = **각 접촉 Holm R=1/(2σr_c) → Kirchhoff** (exact). + **Stage-E 소성 접촉면적**(Chen 면적은 기하·박막; 우리는 소성변형). 다른 저항 *물리*(수렴 vs 박막).
2. ★ **full 삼중항(열 포함).** Chen = 이온·전자(SOFC, mean-field). 우리 = **σ_ionic 0.975 + σ_e 0.953 + σ_thermal 0.903** *실값*. SOFC 도 *열전도(σ_thermal) 없음*.
3. ★ **압밀역학(porosity *예측*).** Chen porosity=입력(가정 random-pack). 우리 = **DEM 압밀(Heckel P_y 138) + MPM J2 소성**으로 porosity·CN·percolation 이 *압력→구조로 emerge*. Chen Z̄=6 random-pack 가정을 우리는 *압밀-특이 측정*으로 대체.
4. ★ **DEM↔MPM 소성 morphology.** Chen 입자=영원한 강체. 우리 MPM = SE 진짜 SHAPE 소성·void-fill·변형장 Σdg(SEM 일치).
5. ★ **재료-grounded σ_grain.** Chen σ=SOFC intrinsic(YSZ 0.05–6.7 S/m). 우리 = **Cronau 3.0 mS/cm × Cronau(r_SE) GB × Trevisanello NCM(r)** = 실제 LPSCl/NMC811 재료 σ.
6. ★ **fracture-aware + predictor.** Chen = 균열 없음·정적. 우리 = f_intact·Auerbach + 솔버→스케일링 법칙(LOOCV 압축)→ML predictor→2D 합성.

> **포지셔닝 한 줄:** "Chen 2011 provides the *analytic* percolation micro-model — closed-form coordination number Z_{k,ℓ} (Eq 2), multi-size percolation probability P (Eq 7), and inter-particle conductivity σ_inter ∝ Σ a·Z·P (Eq 10) for poly-dispersed PSDs, validated against numerical random packing (Kenney). It is the *analytic counterpart* of our DEM-measured CN/percolation and the *mean-field cousin* of our Kirchhoff/Holm conductivity solve. Where Chen approximates σ as intrinsic-σ × percolation/geometry factors on an *assumed* random-packing (Z̄=6, input porosity), our DEM *measures* CN/percolation/σ on a *compaction-predicted* structure and solves an *explicit constriction-resistance network* — plus the full ionic/electronic/thermal triad, Stage-E plastic contact area, MPM plastic morphology, and fracture-awareness that the SOFC analytic model (necessarily) omits. ⚠ SOFC context: TPB is not a direct battery quantity; the transferable physics is the CN/percolation/PSD analytic structure, not the absolute σ/TPB."

---

## 8. 적용 인사이트 (내 연구에 어떻게)

- ① ★ **B3 해석적-prior 확정·인용:** Chen Eq 2(배위수)·Eq 7(percolation 확률, 임계 3.764)·Eq 10(inter-σ ∝ a·Z·P) 을 우리 CN²·φc·f_p³ 의 *해석적 mean-field 근거*로 paper/deck 에 인용(Bielefeld 수치 앵커와 *짝*: "Bielefeld 수치 GeoDict + Chen 해석 닫힌식 = 같은 percolation 물리의 두 길"). ⚠ "우리 CN² 지수 2 = Chen P 함수형" 등치 금지 — *물리 방향*만. `docs/data/chen2011_percolation_micromodel.csv`.
- ② **φc 의 PSD-의존 방향:** Chen "넓은 PSD → ψ^t 0.30→0.18 하강"(Fig 6)·"큰 r̄_el/r̄_ed → 임계↓·inter-σ↑"(Fig 5,9) = 우리 g_phys(조성-가중 입경 게이트)·SE/AM 입경비(12:1) 이득의 *해석 방향 근거*. ⚠ 절대값 전이 금지(SOFC·무차원) — *민감도 방향*(분산↑→φc↓, 입경비↑→φc↓)만.
- ③ **다분산 vs bimodal *다른 양* 명시:** Chen 의 "분산↑→percolated TPB↓(~32 %)"(연결성 약화)는 우리 "bimodal→packing↑·dip"(밀도 강화)와 *직교 축* — 비교 시 *반드시* "TPB 연결성(Chen) ≠ packing 밀도(우리)" 병기. 단 *입경비* 축(r̄_el/r̄_ed↑ 유리)에서는 우리 bimodal 과 *같은 방향*.
- ④ **inter-입자 저항 기하 대비:** Chen Eq 10(면적/δ 박막형, YSZ 입계) vs 우리 Holm(수렴저항) — "우리는 더 물리적인 *수렴저항*(Holm 1967) + 소성 접촉면적(Stage-E)" 차별점 문장화. (Bazzoun RNM 도 Holm 형 → 우리·Bazzoun = 수렴저항 계보, Chen = 박막 계보.)
- ⑤ **포지셔닝:** "percolation 미시모델 = Chen(2011, 해석 닫힌식·σ 풂·다분산) → Bielefeld(2019, 수치 GeoDict·σ 안 풂·단봉) → Bazzoun(2026, RNM/Holm σ+실험) → 우리(exact 망 σ 삼중항 + MPM)" — 우리는 *해석적 mean-field 와 수치 percolation 둘 다의 위*(exact network + 수렴저항 + 소성 + 삼중항). Chen 이 *해석적으로* 푼 σ 가 우리 exact 망 해의 *상한/근사*임을 frame[4] 로.

---

## 9. 인용 가능 문장 (deck/paper용)

- "Chen et al. (J. Power Sources 2011) develop an *analytic* percolation micro-model for poly-dispersed composite electrodes — closed-form coordination number (Eq 2), multi-size percolation probability P=[1−((3.764−ΣZ)/2)^2.5]^0.4 (Eq 7), and inter-particle conductivity σ_inter ∝ Σ a·Z·P (Eq 10) — validated against numerical random-packing reconstruction (Kenney). It is the analytic counterpart of our DEM-measured coordination/percolation and the mean-field cousin of our Kirchhoff/Holm conductivity solve."
- "The analytic micro-model makes percolation probability and inter-particle conductivity explicit functions of coordination number (Chen 2011, P, λ_TPB, σ_inter all ∝ Z·P(Z)), providing the literature basis for the CN² term in our σ_ionic scaling law (note: physical direction only — our data-locked exponent ≠ the analytic functional form)."
- "A poly-dispersed PSD (normal, σ'=0.4) lowers the maximum percolated TPB by ~32 % vs mono-sized, while broad PSD and large mean-radius ratio (r̄_el/r̄_ed) lower the percolation volume-fraction threshold (ψ^t 0.30→0.18) and raise inter-particle ionic conductivity (Chen 2011, Figs 4–9) — the analytic basis for our φc dependence on composition-weighted particle size (g_phys gate) and the SE/AM size-ratio benefit. ⚠ TPB connectivity (Chen) is a distinct quantity from our packing density / Furnas dip."
- "Chen's analytic model approximates conductivity as intrinsic-σ × percolation/geometry factors on an *assumed* random packing (Z̄=6, input porosity); our DEM measures coordination/percolation on a *compaction-predicted* structure and solves an *explicit constriction-resistance network* (Holm 1967), extended by the full ionic/electronic/thermal triad, Stage-E plastic contact area, MPM plastic morphology, and fracture-awareness."

---

## 10. 주의/한계 (over-claim 방지)

- **SOFC 맥락 + TPB 는 우리 직접 양 아님.** 이 논문은 LSM/Ni–YSZ 고체산화물 연료전지 — **percolated TPB(전자·이온·기공 삼상 경계)는 우리 배터리의 양이 *아니다*** (우리는 SE–CAM 면접촉·SE–SE 이온망; 가장 가까운 대응은 active interface/coverage 정도). σ 절대값(YSZ 0.05–6.7 S/m·δ 5 nm)·intrinsic σ 는 *재료-특이* → **배터리(LPSCl/NMC811) 절대 전이 금지**. **전이 가능 = 배위수 해석식(Eq 2)·percolation 확률(Eq 7)·percolation 임계의 PSD 의존·"분산↑→임계↓·입경비↑→임계↓·inter-σ↑" 라는 *분포 물리*** 뿐.
- **σ 직접 비교 *불가*.** Chen σ 는 *무차원형(σ̃)* 또는 SOFC 945 °C 예시(σ^tra,eff_ed 1953 / σ^ter,eff_el 0.87 S/m) — 우리 σ_ionic 0.04–0.18 mS/cm·Bazzoun 0.137 과 *수치 직접 비교 금지*. 비교 가능한 건 *percolation 임계·CN·PSD 의존·해석식 구조*만.
- **mean-field ≠ exact 망 해.** Chen σ(Eq 9 Bruggeman·Eq 10 면적/δ)는 *intrinsic σ × percolation/geometry 인자*의 mean-field 근사 — *각 접촉을 푸는 우리 Kirchhoff/Holm exact 망 해가 아님*. "Chen 도 σ 를 푼다"는 *해석적 mean-field*로서 — 우리의 *상한/근사*로만(frame[4]). inter-입자 저항도 *박막 면적형*(a/δ)이지 *수렴저항형*(Holm)이 아님 — 다른 물리.
- **random-packing *가정* ≠ 우리 압밀(측정/예측) 구조.** Chen 배위수 = Z̄=6 random-dense-pack *가정*; porosity φ_g = *입력*. 우리 ⟨z⟩·porosity 는 *DEM 압밀로 측정/예측*(압력·소성 반영). **Chen 의 가정 구조를 우리 압밀 구조와 동일시 금지** — 우리 15.6 %(DEM)·16.7 %(MPM)는 *예측*값.
- **다분산 효과의 *양* 구분.** Chen "분산↑→percolated TPB↓(~32 %)"는 *TPB 연결성* 약화; 우리 bimodal 이득은 *packing 밀도*(porosity↓). **두 양이 다르다** — 비교 시 명시. (단 *입경비 r̄_el/r̄_ed↑ 유리* 축에서는 우리 bimodal 과 같은 방향.) Chen 의 분산-약화는 *연속 정규분포 폭*; 우리 bimodal 은 *이산 2-모드 입경비*.
- **압밀 역학·소성·형상 *전혀 없음*** → frame[1]/[2] 의 우리 MPM 영역(SHAPE 소성·void-fill·변형장)은 *완전히 그들 밖*. frame[5] 분업에서 Chen 은 *transport-구조 절반*(해석적 mean-field σ + percolation)만; *역학·morphology·exact 망·삼중항·fracture*는 우리.
- **digitized vs stated:** 다분산 감소율(32/48/21/25 %)·임계범위([0.30,0.70]→[0.20,0.80])·ψ^t 이동(0.30→0.18)·예시 σ(1953·0.87·1.3 S/m)·Eq 1–19·Table 1·θ=29.5°·δ=5 nm·Z̄=6·임계 3.764 = 모두 *본문/식/Table stated*. Fig 의 정확한 곡선 값은 *digitized 추세*. CSV 에 source_type 으로 구분.
- **해석식 ≠ 우리 경쟁자.** Chen 은 *해석적 mean-field 모델* — DEM 의 경쟁이 아니라 *해석적 짝/prior*. "흡수"가 아니라 *우리 CN²·φc 의 literature 해석 근거 + 우리 exact 망/소성/삼중항의 차별점 대조*로 사용. 소프트 novelty framing(over-claim 금지).

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

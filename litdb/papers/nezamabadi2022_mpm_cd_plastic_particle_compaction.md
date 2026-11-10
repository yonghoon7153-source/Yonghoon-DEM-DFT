<!-- digest 표준 양식. COMPREHENSIVE / paper-level STANDALONE digest. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · pycompact2025_dem_mpfem_workflow.md · demirtas2021_mpfem_hollow_sphere_die_compaction.md -->
# 입자마다 자기 배경격자를 둔 암시적 MPM + Contact Dynamics 로 소성 원판 300 개 압축 — 재밍 뒤 다공 연속체 압밀식 · Z−Zc ∝ √(Φ−Φc) ★★ 단일 속도장 MPM 에 없는 입자 간 접촉의 선례 (후보 A′) — Nezamabadi (Comput. Part. Mech. 2022)

> slug `nezamabadi2022_mpm_cd_plastic_particle_compaction` · DOI `10.1007/s40571-021-00391-4` · type `MPM+CD (2D implicit MPM · multi-mesh contact dynamics · elastic / bilinear-hardening von Mises disks · analytic compaction model)` · PDF `5f9aa0aa-4._Modelling_the_compaction_of_plastic_particle_packings.pdf` · digested `2026-11-09` · status ✅
>
> ⚠⚠ **소재 · 차원 경고 — 먼저 읽을 것**: 계산은 전부 **2D 원판** (cylindrical particles) 이고 재료는 식품 · 제약 맥락의
> 일반 "무른 입자" 값 **E = 10 MPa · ν = 0.45 · ρ = 1000 kg/m³ · σ_y = 0.4 MPa**, 입자 지름은 **mm 급**이다.  Φ 는 **2D 면적 분율**,
> 재밍 Φc ≈ 0.8 도 2D 값이다.  ⇒ **LPSCl + NCM811 3D 기공률로 절대 전이 0 건.**  가져오는 것은 무차원 비 (σ/σ_y · E/σ_y · ν) ·
> 경향 · **접촉 처리 방법론**뿐이다.
>
> ⚠ **PDF 판본**: White Rose Research Online (Leeds) 저장 **accepted manuscript** (`Version: Accepted Version`, © OWZ 2021).
> PDF 1 쪽이 저장소 표지라 **PDF 쪽 = 논문 쪽 + 1**.  출판본과 조판 · 문구가 다를 수 있다.
>
> ⚠ `> elements:` / `> methods:` 태그를 **의도적으로 생략**했다 — 화학 원소 축 카드가 아니다 (주기율표 뷰 오탐 방지).
>
> 짝 카드: `nguyen2017_mpm_bpm_deformable_particle_compaction` — **같은 그룹 (LMGC · IATE Montpellier) 의 2017 학회 4 쪽 전신**
> (MPM-CD 는 탄성만, 소성은 BPM 으로).  이 논문은 **MPM 쪽에 소성 (이선형 경화) 을 넣은 후속**이다.

---

## 0. 우리에게 왜 중요한가 (한눈 위치)

우리 MPM (Taichi MLS-MPM · J2 · SE E 1.53 GPa / ν 0.49 / σ_y 0.30 GPa) 은 **단일 속도장**이라 닿은 SE 입자가 한 덩어리로 붙는다
(입자 간 미끄럼 · 분리 없음).  우리 기록은 *"이 연속체 MPM 은 연화 없이는 분말 압밀을 재현하지 못했다"* 이고, 그 막다른 길 탐색
(DPC cap · shear-jam · bulk-jam — `docs/mpm_dpc_cap_crosscheck.md`) 은 전부 **단일 속도장 안에서 구성식만 바꾼** 것이었다.
**이 논문은 그 탐색에 없던 축 — 접촉 표현 — 을 바꾼다.**

| 우리가 필요한 것 | 이 논문이 주는 것 |
|---|---|
| 입자 간 접촉 (미끄럼 · 분리 · 마찰) 을 **MPM 안에서** 푸는 실제 구현 | **다중 격자 접촉** (입자마다 자기 배경격자 · 접촉점은 공통 배경격자) + **Contact Dynamics** (암시적 · 비평활) — 논문 §2 · 이 카드 §4.2 |
| 연화 없이 소성 입자 압밀이 되는가 | **E/σ_y = 25 (연화 없음)** 로 Φ 0.78 → 0.99 (2D) — Fig 3 |
| 재설계 MPM 이 맞춰야 할 관측량 | Φ–σ 곡선 (바닥 벽 반력) · 최대 곡률 κ · 배위수 Z(Φ) — Fig 3 · 5 |
| 압밀 체제 구분 | **Φc ≈ 0.8** 에서 재배열 → 형상 변화 체제 전환 · σ ≈ 0.35 MPa (= **0.875 σ_y**) 에서 소성/탄성 분기 — 논문 §4 |
| 압밀 곡선 함수형 (Heckel 외 대안) | 재밍 뒤를 **다공 연속체**로 본 해석식 (Kováčik 형 유효계수 → P 파 계수) — 식 (5)–(17) |
| "DEM 만으로는 왜 부족한가" 의 제3자 문장 | *"Hertz … only valid up to about 10% of strain … this assumption is too crude"* — 논문 §1 (이 카드 §10 에 원문) |

⇒ [DEM 우선 (수영)] 후보 중 **A′ (다물체 / 다속도장 접촉 MPM) 의 실현 가능성 선례** (2D · 300 입자 · 단일 재료).  동시에
**B (NSCD+FE) 의 접촉 알고리즘 (CD = 비평활 접촉 동역학)** 을 MPM 몸체에 붙인 **혼성**이기도 하다.
⚠ **3D · 우리 규모 (SE 32,832 + AM 457) · 강체 AM 과의 혼합 · 제하 (unloading) · 실험 검증은 이 논문에 없다.**

---

## 1. 한 줄 요약 (bilingual)

**KR:** 입자 하나하나를 **자기 배경격자 위의 암시적 MPM 연속체** (선형 탄성, 또는 속도 무관 von Mises + **이선형 등방 경화**) 로 두고,
입자 사이 접촉은 **Contact Dynamics (CD)** 로 풀어 — **2D 원판 300 개**를 Φ **0.78 → 0.97–0.99** 까지 일축 압축했다.  소성 입자는 탄성보다
**낮은 응력으로 공극을 채우고** (경화 H 가 작을수록 더 낮게), **Φc ≈ 0.8 (재밍)** 뒤에는 재배열이 무시되고 **형상 변화가 압밀을 지배**한다.
그 구간을 **다공 연속체**로 본 해석식 (맞춤 매개변수 4 개 + 재밍점) 이 MPM 을 Φ ≈ 0.97 까지 따라가고 (digitized: 소성 ±7 % · 탄성은
Φ 0.85 에서 −21 % 로 시작), 초과 배위수는 탄성 · 소성 무관하게 **(Φ−Φc)^0.5** 를 따른다.

**EN:** Each particle is an implicit-MPM continuum on its own background mesh (linear elastic, or rate-independent von Mises with
bilinear isotropic hardening); inter-particle contacts are solved with Contact Dynamics through a common background mesh.  In 2D plane
strain, 300 disks are compressed uniaxially from Φ = 0.78 to Φ ≈ 0.97–0.99 by a wall moving at 2 m/s.  Plastic packings need less
stress than elastic ones to fill the pores, and less when hardening is small; beyond jamming (Φc ≈ 0.8) particle shape change
controls densification, an analytic porous-continuum model with four fitted parameters follows the MPM curves up to Φ ≈ 0.97, and
Z − Zc scales as (Φ − Φc)^0.5 independent of the material behaviour.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **Saeid Nezamabadi** (1,2,3) · **Mojtaba Ghadiri** (3) · **Jean-Yves Delenne** (2) · **Farhang Radjai** (1) |
| 소속 | 1 LMGC, Université de Montpellier, CNRS, Montpellier, France · 2 IATE, CIRAD, INRA, Montpellier SupAgro, Université de Montpellier, F-34060 Montpellier, France · 3 School of Chemical and Process Engineering, University of Leeds, Leeds LS2 9JT, UK |
| 교신 | saeid.nezamabadi@umontpellier.fr (논문 1 쪽 각주) |
| 저널 | **Computational Particle Mechanics 9 (1), pp. 45–52 (2022)**, ISSN 2196-4378 — 저장소 표지에 인쇄된 서지 |
| DOI | **10.1007/s40571-021-00391-4** |
| 판본 | Accepted Version (author produced) · White Rose eprint 172185 · © OWZ 2021 |
| 접수 / 게재일 | **[미확인]** — 원고의 `Received: date / Accepted: date` 는 빈 자리 표시 |
| 키워드 | Material point method · Contact dynamics · Granular materials · Powders · Plastic particles |
| 분량 | 본문 8 쪽 (PDF 9 쪽 = 표지 1 + 8) · **Fig 1–5** · 식 (1)–(22) · 부록 1 · 참고문헌 21 · 표 없음 · SI 없음 |
| 연구유형 | 수치 (2D 암시적 MPM + CD) + 해석 모델 (맞춤) · **실험 없음** |
| 코드 | 이름 · 공개 여부 **[미확인]** (병렬 암시적 MPM — 이전 논문 [10][11] 의 구현이라고만 적음) |
| 계산 자원 | Genotoul bioinformatics platform Toulouse Midi-Pyrénées (감사의 글) · 코어 수 · 런타임 **[미확인]** |
| 자금 | ANR *Investissements d'avenir* ANR-10-LABX-001-01 Labex Agro (project ID 1502-607) · Agropolis Fondation · I-SITE MUSE (ANR-16-IDEX-0006) |
| 이해상충 | 없음 (선언) |
| 방법 계보 (인쇄된 참고문헌 — **우리 미열람**) | [10] Nezamabadi, Radjai, Averseng, Delenne, *J. Mech. Phys. Solids* 83, 72 (2015) — 암시적 MPM + CD · [9] Nezamabadi, Nguyen, Delenne, Radjai, *Granular Matter* 19, 8 (2017) — 무른 입자 (BPM) · [11] Nezamabadi, Frank, Delenne, Averseng, Radjai, *Comput. Phys. Commun.* 237, 17 (2019) — 병렬 · 유한변형 MPM |

---

## 3. 핵심 수치 — stated / digitized / derived(ours) 구분

> ⚠ `digitized` = **그림의 벡터 경로에서 꺼낸 표식 좌표**를 축 눈금으로 환산한 값 (눈금 맞춤 잔차 < 10⁻³ 데이터 단위 · 삼각형 표식은
> 외접 상자 중심이 점에서 ~0.3–0.5 pt 어긋남).  **그래도 그림에서 읽은 값 = 추세 · 비교 전용**이다.  거짓 정밀도로 인용 금지.
> `derived(ours)` = 논문 값으로 **내가** 계산한 것 — 논문에 없는 수다.

### 3.1 수치 설정 (전부 stated · 쪽 = 논문 쪽)

| 항목 | 단일 입자 (§3, p.3) | 집합체 (§4, p.3–4) |
|---|---|---|
| 차원 | **2D 평면변형** (명시) | 2D 원판 — 평면변형은 §3 에만 명시, §4 는 *"The same material responses as for the single particle analysis"* |
| 입자 수 | 1 | **300** |
| 크기 | 지름 **D = 60 mm** | *"a uniform distribution of the particles by volume fractions in the range [2, 4] mm"* — 지름인지 반지름인지 **미기재** (짝 논문이 지름 [1.4, 2.4] mm 를 쓰므로 지름으로 추정) |
| 초기 상태 | — | **DEM 으로 준비** (DEM 코드 · 접촉식 **미기재**) · **Φ0 = 0.78** (Fig 2a 라벨) |
| 상자 | 두 강체 벽 사이 | 직사각 상자 · **위 벽만 이동** (상자 치수 **미기재**) |
| 하중 | 위 벽 **0.5 m/s** 하강 · 아래 벽 고정 | 위 벽 **2 m/s** 하강 (일축) |
| 중력 | — | **0** (*"to avoid stress gradients"*) |
| 마찰 | **미기재** | *"no friction is introduced"* (입자–입자 · 입자–벽 모두로 읽힘) |
| 요소 | **4 절점 사각형 요소** | (같은 설정으로 읽힘) |
| 물질점 | 요소당 처음 **4 개** | (같음) |
| 보간 | **cubic spline** — 물질점 값을 양방향 **최대 2 격자 절점**까지 사상 [13] | (같음) |
| 격자 간격 · 입자당 요소 수 | **[미확인]** | **[미확인]** — 수렴 시험도 없음 |
| 시간적분 | 암시적 MPM + 암시적 CD · **Δt = 0.1 µs** | **Δt = 0.1 µs** |
| 탄성 | **E = 10 MPa · ν = 0.45 · ρ = 1000 kg/m³** | 같음 |
| 소성 | 속도 무관 **von Mises + 이선형 등방 (일) 경화** [12 = ANSYS 이론서] · **σ_y = 0.4 MPa · H = 0 / 1 / 3 MPa** | 같음 |
| 변형 이론 | **미소변형 이론** (구성식) + 물질점 부피는 **유한변형 갱신** `V_p(t+Δt) = det(I + ∇u_p)V_p(t)` (식 4) | 같음 |
| 판독 | σ_yy vs ε_yy (**정의 미기재**) | σ = **바닥 벽에 걸리는 접촉력**에서 · Φ = V_S/V · κ · Z |
| 병렬 | *"parallel implicit"* | 같음 |

### 3.2 무차원 비 — derived(ours)

| 비 | 이 논문 | 우리 3D MPM | 비고 |
|---|---|---|---|
| E/σ_y | **25** | 1.53/0.30 = **5.1** (연화) · 실재 E 24/0.30 = 80 | 그들은 **연화 없음** |
| H/E · 접선계수 E_p = EH/(E+H) | 0 · 0.1 · 0.3 → E_p **0 · 0.909 · 2.31 MPa** | **경화 없음** (Hencky J2 반환 사상, 일정 σ_y — `scripts/mpm3d_compaction.py` 반환 사상 판독) ⇒ 그들 **H = 0** 극한 | |
| 체적계수 K/σ_y | 2D K = λ+µ = 34.5 MPa → **86** (3D 식 λ+2µ/3 = 33.3 → 83) | 25.5/0.30 = **85** | ★ 우연히 같은 자릿수 (§8-③) |
| 전단계수 µ/σ_y | µ = 3.45 MPa → **8.6** | 0.513/0.30 = **1.7** (실재 DFT µ 8.11 → 27) | 우리는 전단만 크게 연화 |
| c_P/c_S (ν 만의 함수) | **3.32** (ν 0.45) | **7.14** (ν 0.49) | |
| 재하 Mach V/c_P · V/c_S | 단일: 0.0026 · 0.0085 · 집합체: **0.0103 · 0.034** (c_P 194.8 · c_S 58.7 m/s) | V/c_P **0.03** (기본) → V/c_S **0.21** (CLAUDE.md "MPM 재하율 함정" real_14 실측 0.031 · 0.22) | ★ 같은 V/c_P 라도 ν→0.5 면 전단 Mach 가 2 배 넘게 커진다 |
| 탄성 원판 기울기 (Fig 1) vs E/(1−ν²) | digitized ≈ 12.6 MPa vs 평면변형 계수 **12.54 MPa** | — | §5.1 해석 |

### 3.3 결과 수치

| 항목 | 값 | 종류 |
|---|---|---|
| 초기 / 최종 스냅샷 Φ | **0.78 → 0.97** (Fig 2) | stated |
| 곡선 끝 Φ (Fig 3b) | H0 **0.991** @ 1.74 MPa · H1 0.989 @ 1.84 · H3 0.986 @ 1.94 · 탄성 0.985 @ 2.41 MPa | digitized |
| 소성/탄성 분기 응력 | **σ ≳ 0.35 MPa** (< σ_y 0.4 — *"not all the particles … undergo plastic deformation at the same time"*) | stated |
| 재밍 (체제 전환) | **Φc ≃ 0.8** | stated |
| Φ = 0.8 의 응력 σc | ≈ **0.18–0.19 MPa** (네 계열 공통) | digitized (Fig 3b) |
| Φ 0.90 에 필요한 σ | H0 **0.68** · H1 0.71 · H3 0.75 · 탄성 **0.89** MPa | digitized |
| Φ 0.95 에 필요한 σ | H0 **1.11** · H1 1.17 · H3 1.26 · 탄성 **1.53** MPa | digitized |
| Φ 0.97 에 필요한 σ | H0 **1.38** · H1 1.46 · H3 1.59 · 탄성 **2.00** MPa | digitized |
| 위를 σ_y 단위로 (Φ 0.95 / 0.97) | H0 **2.8 / 3.5** · 탄성 **3.8 / 5.0** σ_y | derived(ours) |
| σ = σ_y (0.4 MPa) 에서의 Φ | H0 · H1 **0.841** · H3 0.839 · 탄성 0.836 (= 재밍 + 0.04) | digitized |
| 탄성/H0 응력비 (같은 Φ) | Φ 0.95 **1.38** · 0.97 **1.45** · 0.98 **1.49** | derived(ours) |
| H3/H0 응력비 (같은 Φ) | Φ 0.95 **1.13** · 0.97 **1.15** | derived(ours) |
| 최대 곡률 κ (Fig 3a, 정규화) | 시작 **1.00** → 끝 H0 **6.6** · H1 5.8 · H3 4.8 · 탄성 **2.9** | digitized |
| 같은 σ (1.74 MPa) 의 κ | H0 6.6 · H1 5.5 · H3 4.5 · 탄성 2.5 | digitized |
| 해석식 매개변수 (맞춤) | **f_E = f_Ep = 1.2 · f_G = f_Gp = 0.2 · p_c = 0.201 (≃ 1−Φc) · c1 = c1p = 1 · c2 = c2p = 0.23 (≃ −ln Φc) · α = 2.5** | stated |
| 해석식 대 MPM (σ−σc) | 소성 세 계열: Φ 0.85–0.97 에서 **±7 % 안** · 탄성: Φ 0.85 **−21 %** · 0.90 −13 % · 0.95 −5 % · 0.97 +6 % (모델이 낮다가 높아짐) · 마지막 MPM 점 (Φ 0.989–0.993) 에서 모델 **+23 % (H0) · +38 % (H1) · +33 % (H3)** · 탄성 모델은 Φ ≈ 0.98 앞에서 그림 위로 벗어남 | digitized |
| MPM 끝 σ−σc (Fig 4) | 탄성 **2.26** · H0 **1.46** · H1 **1.69** · H3 **1.80** MPa · ε−εc 끝 0.25–0.27 | digitized |
| Z 법칙 | **(Z−Zc)/(Z1−Zc) = √((Φ−Φc)/(Φ1−Φc))** — 탄성 · 소성 통합 | stated (식 17) |
| Z 법칙 산포 | 네 계열 모두 √ 선에서 **rms ≈ 0.05** · 최대 \|편차\| 0.10–0.14 (정규화 축) | digitized |
| 절대 Z (Zc · Z1) | **미기재** — 정규화 값만 | — |
| f_p (소성 부피 분율) 모델값 | α ln(Φ/Φc) → Φ 0.90 **0.29** · 0.95 **0.43** · 0.97 **0.48** · 0.99 **0.53** | derived(ours) — **MPM 측정값 아님** |
| 다공 유효계수 E_eff/E (식 8 · 맞춤값) | p 0.05 **0.71** · 0.10 **0.44** · 0.15 **0.19** · 0.17 **0.11** · 0.18 **0.067** · 0.19 **0.031** | derived(ours) |

---

## 4. 시뮬레이션 방법 ★

### 4.1 지배식 + MPM 이산화 (식 1–4)
- 질량 보존 `∂ρ/∂t + ∇·(ρ v) = 0` (1) · 운동량 `∇·σ + b = ρ a` (2).
- 물질점 질량 고정 ⇒ (1) 자동 만족.  *"The MPM can be considered as a finite element method (FEM) with moving integration points"* —
  적분은 Dirac 델타로 이산화.
- **접촉력이 따로 들어간 격자 운동량식**: `M a_node(t) = f^int(t) + f^ext(t) + f^C(t)` (3),
  `M = Σ_p m_p N_p` (lumped) · `f^int = −Σ_p G_p σ_p V_p` · `f^ext = Σ_p N_p b_p + f^S` (그림 `eq_03`).
- (3) 은 **암시적 MPM** 으로 푼다 [10] — 절점 해를 물질점에 투영해 갱신.  소성 구성식 구현은 *"similar to the finite element method"*.
- 물질점 부피: `V_p(t+Δt) = det(I + ∇u_p^{t→t+Δt}) V_p(t)` (4) — 유한변형 MPM 정식 [11].

### 4.2 ★★ 접촉: 다중 격자 (multi-mesh) + Contact Dynamics — 이 카드의 핵심 (원문)
> *"the nodal contact forces f^C between deformable particles are computed using a **multi-mesh contact algorithm** coupling with the
> contacts dynamics method.  In the context of multi-mesh algorithm, **each soft particle maps in its proper background mesh**.  A contact
> point at the interface between two particles may be treated by **introducing a common background mesh** with the same type of grids for
> the transfer of nodal quantities from proper meshes to the common mesh.  Considering an implicit MPM procedure, the CD method, which is
> based on an **implicit time-stepping scheme**, is a natural choice for the treatment of contact points."* (p.3)

- 즉 **입자 수만큼의 장 (field)** — 한 입자의 물질점은 자기 격자에만 사상된다 ⇒ 두 입자가 같은 공간에 와도 **속도가 합쳐지지 않는다**.
- 접촉 판정 · 힘은 **공통 격자**로 옮긴 절점량 위에서 CD (비평활 접촉 동역학) 로 — 상세는 [10, 9, 11] 로 넘김 (**우리 미열람**).
- CD 는 비평활 · 암시적 방법이다 (CD 원전 = 짝 논문 refs [3] Moreau 1994 · [4] Radjai & Richefeu 2009).  짝 논문의 설명대로 반발력은
  **닿을 때 (δ = 0) 만** 작동하고 그 값이 [−F0, +∞] 의 집합값으로 정해진다 — 즉 **접촉 강성 (penalty) 으로 겹침 δ 에서 힘을 만드는 우리 DEM 과
  다르다** (MPM-CD 의 접촉 절차 세부는 [10] 미열람).  마찰은 이 논문 집합체에서 **꺼져 있다** (μ = 0).  마찰 μ = 0.5 시험은 짝 논문 (2017) 에 있다.
- ⚠ **비용 · 확장성 정보 0** — 입자당 격자를 두는 방식의 메모리 · 시간이 우리 규모 (입자 3.3 만) 에서 어떻게 되는지 이 논문으로는 모른다.

### 4.3 구성식
- **선형 등방 탄성** 또는 **속도 무관 탄소성 · 이선형 등방 경화** (von Mises + 등방 일 경화): 응력–변형 곡선이 두 직선 —
  탄성 기울기 E, 항복점 σ_y, 소성 기울기 H (*"hardening modulus"*).  출처 = ANSYS 이론서 [12].
- **미소변형 이론** 안의 소성 (*"in the context of the infinitesimal strain theory"*) — 그러나 큰 형상 변화 (원 → 다각형) 를 그린다.
  물질점 부피만 유한변형으로 갱신 (식 4).  ⇒ 큰 회전 · 큰 변형률에서 객관성 (objectivity) 처리 **미기재**.
- 우리 3D MPM 과의 차이: 우리는 **Hencky (로그) 변형률 공간 반환 사상 · 경화 없음** (§3.2).

### 4.4 단일 입자 시험 (§3)
- 지름 60 mm 원판을 두 강체 벽 사이에서 직경 압축 · 위 벽 0.5 m/s · 아래 벽 고정 · 2D 평면변형 · Δt 0.1 µs.
- 4 절점 사각형 요소 · 요소당 물질점 4 · cubic spline.
- 재료 4 종: 탄성 / 탄소성 H = 0 · 1 · 3 MPa (σ_y 0.4 MPa).

### 4.5 집합체 (§4)
- 원판 300 개 · 직사각 상자 · 위 벽만 2 m/s 하강 (일축) · 초기 배치는 **DEM 으로** · 크기 [2, 4] mm (부피 분율 균등) — *"To avoid
  long-range ordering"* · Δt 0.1 µs · **마찰 없음** · **중력 0**.
- Φ = V_S/V (입자 부피 / 전체 부피 — 2D 면적).
- σ = 바닥 벽 접촉력 (경계 반력) ⇒ **우리 MPM `wallP` (판 반력) 와 같은 계열의 판독**.
- 곡률 κ = *"the mean value of maximum curvature of the particles"* · 정규화 = *"by their mean diameter < d >"* (⚠ §11 정의 모호).
- 초기 Φ0 = 0.78 은 2D 재밍 (0.8) **바로 아래** — 이 논문의 집합체는 **느슨한 충전에서 시작하지 않는다**.

### 4.6 해석 압밀 모델 (식 5–22) — 재밍 뒤를 다공 연속체로
**가정**: 재밍점 위에서는 재배열이 무시되므로 *"the packing behaviours beyond the jamming point are almost like a continuum medium"*.
- 탄성: `σ − σc = M^eff (ε − εc)` (5), `ε = ln(h/h_i)` (누적 수직 변형률).
- Z 를 넣은 형태: `σ = − M^eff / (1 + M^eff/(c1 K Z Φ)) · (ln Φ + c2)` (6), K = 입자 체적계수 (2D 에서 **K = λ + µ**).
  · 부록 유도: `σ = M^eff ε` (18) · `K dV_S/V_S = −dσ_S` (19) · `σ = c1 Z Φ σ_S` (20) · `dε = dV_S/V_S − dΦ/Φ` → 미분식 (21) → 적분 (22) = (6).
- 유효 P 파 계수 (이전 [11] 의 Voigt `M^eff = ΦM` 대신 다공 매질식): `M^eff = G^eff(4G^eff − E^eff)/(3G^eff − E^eff)` (7),
  `E^eff = E (1 − p/p_c)^{f_E}` (8, Kováčik [14]) · `G^eff = G (1 − p/p_c)^{f_G}` (9, Kováčik [15]) · p = 1 − Φ ·
  **p_c = 유효계수가 0 이 되는 임계 기공률 (재밍 근처)**.
- 소성: `σ = (1 − f_p) σ_e + f_p σ_p` (10), f_p = 소성 영역 부피 / 입자 전체 부피 — 재밍 전 0, 뒤에서는 수직 변형률 (곧 Φ) 에 비례
  ⇒ `f_p = α ln(Φ/Φc)` (11) · `σ_p = σ_y + M_p^eff (ε − εc)` (12) · `σ_p = σ_y − M_p^eff/(1 + M_p^eff/(c1p K_p Z Φ)) · (ln Φ + c2p)` (13) ·
  (14)–(16) = (7)–(9) 의 소성판 · `E_p = EH/(E+H)` (접선계수) · `G_p = E_p/2(1+ν_p)` · **ν_p = ν** (*"assuming that the volume change due to
  plastic deformation is negligible"*).
- Z 법칙 (식 17): `(Z − Zc)/(Z1 − Zc) = √((Φ − Φc)/(Φ1 − Φc))`, Z1 · Φ1 = 재밍 뒤 아무 상태 [refs 19–21 = O'Hern 2003 · van Hecke 2010 · Zhang 2010].
- 맞춤 순서: 탄성 런으로 탄성 매개변수 → 그것을 고정하고 소성 런 하나로 소성 매개변수.  결과 = §3.3 표.
  *"one needs to determine **four parameters** in the analytical models as well as the jamming state"* — 어느 넷인지는 명시 안 됨
  (우리 읽기: f_E · f_G · c1 · α; p_c ≃ 1−Φc · c2 ≃ −ln Φc 는 재밍점에 묶임).  소성 쪽 값이 f_Ep = f_E · f_Gp = f_G · c1p = c1 · c2p = c2 로
  탄성과 같으므로 소성 런에서 새로 맞춘 것은 사실상 **α 하나**로 읽힌다.
- ⚠ derived(ours) 세 가지:
  ① 식 (6) 은 `ln Φ + c2 = ln(Φ/Φc)` (c2 ≃ −ln Φc) 라 **Φ = Φc 에서 0** — 사실상 σ − σc 의 식이다.  부호는 압축 음수 규약으로 보이며
     그림은 크기로 그린다 (규약 미기재).
  ② (21) → (22) 적분은 **M^eff · Z 를 상수처럼** 다루고 우변의 σ 비례 항을 버린 형태로 보인다 (논문은 근사 여부를 말하지 않는다).
  ③ **K_p (식 13) 는 정의되지 않았다.**

### 4.7 ★ 입자 처리 (우리 "무질서 처리" 의 DEM 대응)

| 축 | 이 논문 |
|---|---|
| 형상 | **원판 (2D)** — *"Obviously, the disks do not represent real particle shapes … But the developed approach can be easily applied to more complex particle shapes [10]."* |
| 크기 분포 | 단봉 · 부피 분율 균등 [2, 4] mm (장거리 질서 방지용) — bimodal 없음 |
| 소성 표현 | **★ 진짜 입자 형상 소성** — 입자 내부를 물질점으로 이산화 + J2 이선형.  δ-겹침 프록시 **아님** |
| 접촉 | **입자별 장 + CD** — 입자 경계가 끝까지 남는다 (Fig 2).  융합 · 결합 없음 |
| 강체 / 변형체 | 입자 = 변형체, 벽 = 강체.  **강체 입자 (우리 AM) 혼합 없음** |
| 파괴 · 결합상 | 없음 |
| 상 수 | 1 상 (한 재료) — **AM + SE 복합 없음** |
| 무작위성 | DEM 초기 배치 1 개 · **시드 앙상블 · 오차막대 0** |

⇒ 우리 층위 지도 (`comparison_vs_ours_DEM.md` §C 의 층 (1)–(3) 표) 기준: **층 (3) 자유형상 소성**을 하면서 **접촉 (층 (1)(2)) 은 CD 로 따로** 푼다.
pycompact · demirtas (MPFEM) 와 같은 층, 이산화만 **MPM** 이다 (메시 왜곡 없는 대신 접촉은 다중 격자로 해결).

---

## 5. 결과 — 절별

### 5.1 §3 단일 원판 직경 압축 (Fig 1)
- stated: 탄성 원판은 *"linear behaviour … though the particle has a cylindrical shape.  It may be explained by the small imposed deformation;
  i.e., ε < 0.17"*.  탄소성은 *"a linear response until σyy ≃ 0.4 MPa, which corresponds to the yield stress σy and a linear plastic
  behaviour beyond.  The slope of the plastic parts increases as hardening augments."*
- digitized: 탄성 기울기 ≈ **12.6 MPa** (ε_yy 0.165 에서 σ_yy 2.09 MPa) · 꺾임 ≈ **0.40–0.42 MPa @ ε_yy ≈ 0.035–0.04** ·
  ε_yy ≈ 0.17 에서 σ_yy **0.53 (H0) · 0.69 (H1) · 0.93 (H3) MPa** · 꺾인 뒤 기울기 ≈ **0.7 · 1.9 · 3.7 MPa**.
- derived(ours) 해석 둘:
  ① 꺾인 뒤 기울기가 접선계수 E_p (0 · 0.91 · 2.31 MPa) 보다 **≈ 0.7–1.3 MPa 크다** — 접촉면이 넓어지는 **기하 경화**로 읽힌다 (H = 0 에서도 0.7).
  ② 탄성 기울기 12.6 ≈ **평면변형 계수 E/(1−ν²) = 12.54 MPa** (0.5 % 안).  σ_yy · ε_yy 가 **입자 부피 평균량**이라면, 측면이 자유로운
     선형 탄성체의 평균 응력–평균 변형률은 **모양과 무관하게 정확히 직선**이다 (평균 Hooke 법칙) ⇒ 저자의 "작은 변형이라서" 라는 설명이
     필요 없을 수 있다.  **정의 미기재라 확정 불가** — 짝 논문 Fig 1 (σ = F/L) 은 같은 재료의 원판이 ε > 0.05 에서 **비선형**이다 (정의 차이).

### 5.2 §4 집합체 형상 (Fig 2)
- (a) 초기 Φ = 0.78 · (b)–(e) **Φ = 0.97** 의 탄성 / H = 3 · 1 · 0 MPa 스냅샷 + 오른쪽 아래 창 확대.
- stated: *"Due to particle shape changes, the whole space is nearly filled at the end"* · *"the shapes of the particles change gradually from
  circular to polygonal and the plastic particles at the end have a polygonal shape with larger curvatures in comparison with the elastic
  particles"* · *"the plasticity allows these particles overfill the pores for much lower stress than the elastic ones."*
- 관찰 (그림): Φ 0.97 에서도 **입자 경계 (검은 틈) 가 모든 입자 사이에 남는다** — 융합 없음.  남은 공극은 **세 입자가 만나는 모서리**의
  작은 삼각형이다.

### 5.3 곡률 · Φ 대 응력 (Fig 3)
- stated: 소성 입자는 **더 작은 σ 로 더 큰 κ** · H 가 작을수록 κ ↑ (*"one needs less applied stress to fill the pores … when the hardening
  of plastic particles is small"*) · 탄성 압축에는 *"a larger force"* 필요 · **σ ≳ 0.35 MPa 에서 분기** · **Φ ≈ 0.8 에서 체제 전환 = 재밍**.
- digitized 표는 §3.3.  요점: 같은 Φ (0.95–0.98) 에 탄성은 H0 의 **1.4–1.5 배**, H3 는 H0 의 **1.13–1.15 배** 응력이 든다.
- σ_y 단위로 읽으면 (derived): **σ = σ_y 에서 Φ ≈ 0.84 (재밍 + 0.04)**, Φ 0.95 · 0.97 에 **2.8 · 3.5 σ_y (H0)** — 접촉을 풀고 연화하지 않은
  소성 충전체는 **σ_y 의 수 배**가 되어야 고밀도에 닿는다 (2D).

### 5.4 해석 모델 대 MPM (Fig 4)
- stated: *"the predictions of the elastic and plastic models are in good agreement with all MPM simulations"* (§3.3 매개변수) ·
  *"at high packing fractions, a divergence between the models and the numerical simulations is noticeable.  To reproduce well the
  predictions, the particles discretisation may be refined in order to resolve correctly the **small radii of curvature at the contact zones**
  between particles."* · 일반 형태는 산업 압밀 곡선과 비슷 [16–18, 5] · *"this model still needs to be validated with a more detailed and
  quantitative comparison between simulations and experiments."*
- digitized: **소성 세 계열**은 Φ 0.85–0.97 에서 (모델 − MPM)/MPM = **−4 % ~ +7 %**, 마지막 MPM 점에서 **+23 / +38 / +33 %** (H0 / H1 / H3).
  **탄성**은 Φ 0.85 에서 모델이 **21 % 낮고** (0.25 vs 0.32 MPa) 0.90 −13 % · 0.95 −5 % · 0.97 +6 % 로 뒤집힌 뒤 Φ ≈ 0.98 앞에서
  모델이 그림 틀 (2.5 MPa) 위로 나간다.
- ⇒ "모델이 맞는다" 는 **Φ ≲ 0.97 (2D)** 범위의 서술이다.  그 위는 **격자 해상도 문제라고 저자가 스스로 의심**하는 구간.

### 5.5 배위수 (Fig 5)
- stated: 재밍 뒤 초과 배위수가 **(Φ−Φc)^0.5** 로 탄성 · 소성을 하나로 묶는다 (*"unified … independent of the material behaviours"*) —
  이전 연구 [19–21, 11] 와 같은 형태.
- digitized: 네 계열 rms ≈ 0.05 · 탄성 (네모) 이 고 Φ 끝에서 √ 선 아래로 처진다 (x 0.92–0.98 에서 0.89–0.94).
- ⚠ 절대 Zc · Z1 이 없어 **우리 DEM Z 와 숫자로 대조할 수 없다** — 지수만 비교 가능.

---

## 그림별 (원 캡션 요지 + MPM 관점)

> 그림 파일 = `litdb/figures/nezamabadi2022_mpm_cd_plastic_particle_compaction/` · 300 dpi · 캡션 제외 · 벡터 그림 (내장 래스터 없음).

1. **`fig_1.png`** — *원 캡션 요지*: 단일 탄성 · 탄소성 (경화 여러 값) 원판의 직경 압축 응력–변형 곡선.
   *MPM 관점*: 단일 원판 (D 60 mm) 직경 압축 — 탄성은 ε_yy < 0.17 에서 직선 (기울기 ≈ 12.6 MPa, digitized), 소성은 σ_yy ≈ 0.40 MPa (= σ_y) 에서
   꺾이고 꺾인 뒤 기울기는 H = 0 / 1 / 3 MPa 에 ≈ 0.7 / 1.9 / 3.7 MPa.  입자가 하나뿐이라 단일 속도장과 다물체 접촉의 차이가 드러나지 않는
   시험이므로 재설계 MPM (A · A′) 의 첫 검증으로 그대로 재현할 수 있다 (σ_yy · ε_yy 정의 미기재 · 2D 평면변형 · 벽 접촉 조건을 맞춰야 함).
   우리 3D MPM 은 경화 없는 J2 (H = 0 에 해당) 라, "H 를 올리면 같은 Φ 에 필요한 응력이 커진다" 는 이 논문 결론이 보정 손잡이 하나를 더 준다.
2. **`fig_2.png`** — *원 캡션 요지*: (a) 초기 배치 Φ 0.78, (b)–(e) 탄성 · H = 3 · 1 · 0 MPa 집합체의 Φ = 0.97 스냅샷 + 오른쪽 아래 창 확대.
   *MPM 관점*: 원판이 원 → 다각형으로 바뀌지만 입자 경계가 끝까지 남는다 (입자마다 자기 격자 + CD 접촉).  우리 MPM 은 단일 속도장이라 닿은 SE 가
   한 덩어리로 붙어 이런 경계 · 입자별 곡률 · 배위수를 정의할 수 없다 → 입자 정체성을 유지하려면 후보 A′ 가 필요하다.  "소성 입자가 탄성보다
   모서리가 날카롭다 (곡률 ↑)" 는 A′ 가 재현해야 할 정성 표적이다.
3. **`fig_3.png`** — *원 캡션 요지*: 입자 최대 곡률의 평균 κ (정규화) 와 Φ 를 가한 응력 σ 의 함수로 — 탄성 · 탄소성.
   *MPM 관점*: Φ 0.95 에 필요한 σ = H0 ≈ 1.11 · H1 ≈ 1.17 · H3 ≈ 1.26 · 탄성 ≈ 1.53 MPa (digitized) = σ_y 의 2.8–3.8 배이고, σ = σ_y 에서는
   Φ ≈ 0.84 로 재밍 바로 위다 — 연화 없이 (E/σ_y = 25) 나온 곡선.  판독이 경계 벽 반력이라 우리 wallP 와 같은 축에 겹칠 수 있지만 2D 면적 분율 ·
   무차원 비교만 (절대 전이 없음).  재설계 MPM 에서는 "연화된 E" 대신 "σ/σ_y > 1 구간에서 치밀화" 가 일어나는지가 첫 판별점이다.
4. **`fig_4.png`** — *원 캡션 요지*: 초과 응력 σ−σc 를 Φ 와 초과 변형 ε−εc 의 함수로 (MPM 점 · 해석식 선), σc · εc = 재밍점 Φc ≃ 0.8.
   *MPM 관점*: 재밍 뒤를 다공 연속체로 본 해석식 (Kováčik 형 E_eff = E(1−p/p_c)^f → P 파 계수) 이 소성 MPM 을 Φ 0.85–0.97 에서
   ±7 % 안에서 따라가고 (탄성은 Φ 0.85 에서 −21 % 로 시작) 그 위에서 23–38 % 과대 (digitized), 맞춤 매개변수 4 개 + 재밍점이 필요하다.  이 식의 핵심은 유효 강성이 재밍 기공률 p_c 에서 0 으로 사라진다는
   것 — 닿으면 붙는 우리 단일 속도장 골격에는 그 소멸이 없으므로, 우리 E 연화 (≈ 1/16–1/18) 는 재밍 근처 유효계수 감소를 상수로 박아 넣은 것일
   수 있다 (우리 추론 · 이 식으로 p 0.17–0.18 에서 E_eff/E ≈ 1/9–1/15).  A′ 가 연화 없이 같은 곡선을 내는지가 이 가설의 시험이다.
5. **`fig_5.png`** — *원 캡션 요지*: 재밍 뒤 초과 평균 배위수 Z−Zc 를 초과 충전율 Φ−Φc 의 함수로, 실선 = (Φ−Φc)^0.5 맞춤.
   *MPM 관점*: (Z−Zc)/(Z1−Zc) 가 탄성 · 소성 무관하게 √ 한 곡선에 모인다 (digitized rms ≈ 0.05, 절대 Z 는 미기재).  단일 속도장 MPM 은 SE–SE
   접촉 자체가 없어 이 관측량을 낼 수 없다 → A′ 로 가면 DEM (LIGGGHTS) 의 Z(Φ) 와 같은 축에서 비교할 미세구조 관측량이 생긴다 (교차검증용, 보정 표적 아님).

**식 크롭** (선택 — 같은 폴더):
- `eq_03_mpm_momentum_contact.png` — 식 (3) + M · f^int · f^ext 정의.  *MPM 관점*: 격자 운동량식에 **접촉 절점력 f^C** 가 따로 들어간다 — 우리
  MLS-MPM 에는 이 항이 없고 같은 셀의 운동량을 한 속도로 합쳐 접촉이 "붙음" 이 된다.  A′ 의 핵심 변경점이 바로 이 항이다.
- `eq_06_elastic_compaction_law.png` — 식 (6) σ(Φ, Z).  *MPM 관점*: 우리 MPM · DEM · 실험 Φ–σ 곡선을 같은 함수형으로 맞춰 비교하는 틀
  (Heckel 대안) — 단 c1 · c2 는 맞춤값.
- `eq_07_09_pwave_kovacik_moduli.png` — 식 (7)–(9).  *MPM 관점*: 비결합 충전체의 유효 강성은 재밍 기공률 p_c 에서 0 — 닿으면 붙는 단일 속도장
  골격에는 없는 성질 (우리 연화의 기전 후보 · 우리 추론).
- `eq_10_12_plastic_split.png` — 식 (10)–(12).  *MPM 관점*: f_p = α ln(Φ/Φc) 는 **측정이 아닌 가정** — 우리 MPM 은 항복 부피 분율을 직접 셀 수 있어
  이 가정을 시험할 수 있다.
- `eq_13_16_plastic_moduli.png` — 식 (13)–(16).  *MPM 관점*: H = 0 이면 E_p = 0 → σ_p = σ_y 고정 — 우리 완전소성 J2 와 같은 극한.
- `eq_17_coordination_power_law.png` — 식 (17).  *MPM 관점*: A′ · DEM 공통 미세구조 검증 관측량 (단일 속도장 MPM 에는 Z 가 없다).

---

## 6. Post-processing ★
- **응력**: 바닥 벽 접촉력 합 / 길이 (2D) — 경계 반력.  우리 `wallP` (판 반력 직합) 와 같은 계열이다 (우리 쪽은 위 판).
- **Φ**: V_S/V — 입자 면적 합 / 상자 면적.  물질점 부피 갱신 (식 4) 을 쓰므로 V_S 는 **변형된 입자 부피**로 읽힌다 (정의 상세 미기재).
  탄성 입자는 ν 0.45 라 약간 압축된다 ⇒ "초기 구 부피 합" (우리 ε_sphere 규약) 과 **같은 양인지 미확인**.
- **κ**: 입자별 최대 곡률의 평균 (곡률 추출 알고리즘 **미기재**).
- **Z**: 평균 배위수 (접촉 판정 기준 **미기재** — CD 접촉점 수로 추정).
- **해석식 맞춤**: 탄성 런 → 탄성 매개변수 · 소성 런 하나 → 소성 매개변수 (맞춤 방법 · 오차 지표 **미기재**).
- ⛔ 없는 것: 격자 수렴 · 시드 앙상블 · 오차막대 · 힘사슬 통계 (결론의 *"weaker stress chains"* 는 그림 없이 서술만) · 제하 · 전달물성.

---

## 7. ★★★ 우리 DEM + MPM 대비 (같음 · 다름 · 왜) → `our_dem_baseline.md`

### 7.1 나란히 표
| 축 | **이 논문 (MPM-CD)** | **우리 DEM (LIGGGHTS)** | **우리 MPM (Taichi MLS)** | 판정 |
|---|---|---|---|---|
| 차원 · 규모 | 2D · 300 원판 · mm | 3D · SE 32,832 + AM 457 (real_14) · µm | 3D · DEM 끝 상태 위 SE 만 | 규모 · 차원 모두 다름 |
| 입자 표현 | 입자 = MPM 연속체 (자기 격자) | 강체 구 | SE = 물질점 (한 격자) · AM = 격자 장애물 (속도 0) | |
| 접촉 | **CD (비평활 · 암시적 · 겹침 없음) · 마찰 0** | hooke/hysteresis + 점착 (겹침 δ 로 힘) | **없음 — 단일 속도장 = 닿으면 붙음 (no-slip + 결합)** | ⚠ **그들만 접촉을 푼다** |
| 형상 소성 (층 3) | ✅ J2 이선형 | ✗ (δ 프록시 + 18× 연화) | ✅ J2 완전소성 (Hencky) | 그들 ≈ 우리 MPM |
| 연화 | **없음 (E/σ_y 25)** | E_SE 24 → 1.35 GPa (18×) | E 1.53 GPa (E/σ_y 5.1) | ⚠ **연화 필요성의 차이가 핵심** (§8) |
| 비압축성 | ν 0.45 (2D K/σ_y 86) | ν 0.3 (접촉식 입력) | **ν 0.49 (K/σ_y 85)** | ★ 무차원 체적강성 같은 자릿수 |
| 시작 상태 | DEM 충전 Φ0 0.78 (2D 재밍 바로 아래) | 삽입 → 침강 → 압축 (느슨한 데서) | **DEM 300 MPa 끝 상태** (real_14 씨앗 공극 19.8 %) | 그들은 재밍 직전, 우리 MPM 은 재밍 한참 뒤 |
| 압밀 체제 | 재배열 (Φ<0.8) → 형상 변화 (Φ>0.8) **한 모델에서** | 재배열 + δ 프록시 | **형상 변화만** (재배열은 DEM 이 함 · 한 방향 순차 연계) | |
| 응력 판독 | 바닥 벽 반력 | 판 응력 | wallP (판 반력) | 같은 계열 ✓ |
| Φ / 기공 규약 | V_S/V (변형 부피로 추정) | ε_sphere (Σ 원 구 부피) | MPM union 부기 (ε_sphere 와 1.251 %p 차) | 비교 전 규약 정렬 필요 |
| 재하 Mach | V/c_P 0.010 · **V/c_S 0.034** | — | V/c_P 0.03 · **V/c_S ≈ 0.21** | ⚠ 우리 전단 Mach 가 6 배 높다 |
| 배위수 | ✅ Z(Φ) √ 법칙 | ✅ SE–SE CN 등 | ✗ (SE–SE 접촉 미정의) | A′ 가 메울 칸 |
| 제하 | ✗ | 진행 중 (DEM 언로딩 트랙 P1) | 부분 (300 → 90 MPa 재시작 기능 · 0 까지 대조한 적 없음) | 실험 대조된 제하는 셋 다 없음 |
| 전달물성 σ | ✗ | ✅ 접촉망 σ 삼중항 | ✅ STEP3 복셀 FV (CONTACT_FREE 가지) | ★ 우리 고유 |
| 실험 검증 | ✗ (*"needs to be validated"*) | 외부 앵커 다수 | 앵커 일부 철회 (CL-94) | |

### 7.2 같은 것
- **층 (3) 자유형상 소성을 연속체로** 푼다 (우리 MPM 과 같은 층).  void-fill 이 형상 변화로 일어난다 — Fig 2 의 다각형화 = 우리 MPM 의 경계 평탄화 무늬와 같은 계열.
- **경계 반력 판독** (wallP 계열) · **거의 비압축 입자** (ν 0.45 ↔ 우리 0.49) — 압밀 연속체 설계가 독립적으로 같은 쪽을 골랐다
  (단 그들의 ν 근거는 짝 논문에서 "BPM 과 부피 보존을 맞추려고" 이지 물성이 아니다).

### 7.3 다른 것 — 그리고 왜
1. **접촉**: 그들은 입자별 장 + CD, 우리는 단일 속도장.  ⇒ 그들 입자는 미끄러지고 (μ = 0) 떨어질 수 있고 경계가 남는다; 우리 SE 는 붙는다.
2. **연화**: 그들은 E/σ_y = 25 로 Φ 0.99 까지 간다 (σ ≈ 4.3 σ_y).  우리 MPM 은 연화 (E/σ_y 5.1) 없이는 RCP 근처에 멈췄다 (CLAUDE.md:
   E 24 GPa → 33–38 % · "σ_y barely matters").  **같은 "연속체 소성 입자" 인데 결과가 갈린 차이 = 접촉 표현** (§8-①).
3. **시작점**: 그들은 Φ0 0.78 (재밍 직전) 에서 압축 전체를 한 모델로, 우리 MPM 은 **DEM 끝 상태에서 짧은 재압축**만
   (`docs/reviews/dem_mpm_one_way_sequential_definition_20261109.md` §1).
4. **전단 재하 속도**: 그들 V/c_S 0.034 vs 우리 ≈ 0.21 — ν → 0.5 에서 c_P/c_S 가 7.1 이 되므로 V/c_P 만 맞추면 전단은 준정적이 아닐 수 있다
   (CLAUDE.md "MPM 재하율 함정" 의 같은 지적을 독립 수치로 재확인).
5. **항복 정의 (우리 코드 판독 — 이 논문 밖 사실 · 11-09 메인 세션 정정)**: 우리 `--sigma-y` 는 **Hencky 편차 변형 노름 문턱** (`dg = |dev ε_H| − σ_y/(2µ)`,
   `scripts/mpm3d_compaction.py` 반환 사상) 이고 응력은 **fixed-corotated** (같은 파일 P2G: τ = 2µ(F−R)Fᵀ + λJ(J−1)I) 다.  그래서 단축 항복응력은
   재료 강성 · 하중 부호에 따라 다르다: σ_y 0.30 이면 생산 연화 재료 (E 1.53 · ν 0.49) 압축 **0.318** · 인장 0.454 GPa, 실제 강성 (E 22.06 · ν 0.36)
   압축 0.363 · 인장 0.372 GPa [우리 산술 · 코드 식을 그대로 풂].  √(3/2)·σ_y = 0.367 GPa 는 작은 변형 극한일 뿐이다.  ANSYS 이선형 (그들) 의 σ_y 는
   단축값으로 읽히므로 σ/σ_y 를 나란히 놓을 때는 **우리 쪽 재료 · 하중 부호의 값으로 환산**한다 (생산 연화 재료 압축이면 300 MPa = 0.94 σ_y,uniaxial).
   ⛔ 처음 판의 "단축 = √(3/2)·σ_y · 1.22 배 보정" 은 응력 모형을 보지 않은 판독이라 철회.

### 7.4 전이되는 것 / 안 되는 것
- ✅ 전이 (방법 · 경향 · 무차원): 입자별 접촉의 실현 가능성 · 재밍 뒤 형상 변화 지배 · 소성 < 탄성 응력 (1.4–1.5 배) · 경화 ↑ → 응력 ↑ (~15 %) ·
  거시 항복 개시 < 입자 σ_y (0.875 배) · Z−Zc ∝ (Φ−Φc)^0.5 · 고 Φ 에서 접촉부 곡률 해상도 요구.
- ⛔ 전이 금지: Φ 값 (2D 면적 분율) · Φc = 0.8 (2D) · 응력 MPa 절대값 · 맞춤 매개변수 (f_E 1.2 · f_G 0.2 · α 2.5) — 재료 · 차원마다 다시 맞춰야 함 ·
  "σ = σ_y 에서 Φ 0.84" 를 3D 기공률로 옮기는 것.

---

## 8. ★★ 깊은 인사이트

**① "연화는 줄일 수 없다" 의 범위를 좁혀야 한다.**  우리 기록 (DPC cap · shear-jam · bulk-jam 세 경로 실패 → "softening irreducible") 은
**단일 속도장 MPM 안에서 구성식만 바꾼** 탐색이었다.  이 논문은 **접촉 표현을 바꾼** MPM 이 E/σ_y = 25 (연화 없음) 로 Φ 0.99 (2D) 에
닿는다는 것을 보인다.  ⇒ 정확한 문장은 *"**단일 속도장** MPM 에서는 연화를 구성식으로 대체할 수 없었다"* 이고, **접촉을 푼 MPM (A′)
에서의 필요성은 시험된 적이 없다**.  (⚠ 이 논문은 2D · 단일 재료 · 재밍 직전 시작이라 우리 3D 에서 연화가 사라진다는 증거는 **아니다**.)

**② 연화의 기전 후보 — 재밍 기공률에서 사라지는 유효 강성 (우리 추론).**  식 (8) 의 E_eff = E(1 − p/p_c)^{f_E} 에서 **p_c 는 재밍 기공률**이다:
비결합 충전체는 재밍 근처에서 거시 강성이 0 으로 떨어진다 (맞춤값으로 p 0.17 → E_eff/E ≈ 1/9.4 · p 0.18 → 1/15 · p 0.19 → 1/33, derived).
닿으면 붙는 단일 속도장 MPM 의 골격은 **결합된 다공 고체**라 같은 기공률에서 그 소멸이 없다 → 너무 뻣뻣 → 우리는 재료 E 를 ~1/16–1/18 로
낮춰 맞췄다.  **두 숫자의 자릿수가 겹친다**는 것 자체가 가설의 근거이고, 동시에 **상수 연화는 기공률 · 압력에 따라 0 → 1 로 바뀌는 인자를 한
점에서 맞춘 것**이라는 경고다 — 기공이 닫힐수록 강성이 E 로 돌아오는 효과가 빠지므로 **고밀도에서 너무 무르다** (다압력 · 제하로 전이되지
않을 수 있다).  우리 R1 의 정직한 압축이 ε_sphere 1.125 % 까지 과압축된 것과 **방향이 같다** (단 R1 의 주원인은 얼린 AM 이 하중을 0 지는 것이라
이 기여의 크기는 미상).
**시험**: §9 행동 1 (2D 벤치마크, 단일 속도장 vs 입자별 장).

**③ 무차원 체적 강성은 이미 같은 자리에 있다.**  K/σ_y — 그들 83–86 · 우리 MPM 85 (ν 0.49 로 K 25.5 GPa).  우리가 ν 를 0.49 로 올린 이유
(체적 연화로 0 % 까지 무너지던 것 — 코드 도움말 *"nu<=0.45 over-crushes to 0 porosity"*) 가, E/σ_y 25 의 그들에게는 ν 0.45 로 이미 충족된다.
⇒ 우리 MPM 과 그들의 차이는 **전단 강성 (µ/σ_y 1.7 vs 8.6)** 과 **접촉 표현** 둘로 좁혀진다.  (우연의 일치일 수 있다 — 그들은 K 를 목표로 고르지 않았다.)

**④ 거시 항복 개시는 입자 항복보다 먼저 온다 (0.875 σ_y) — 하중 분담의 이질성.**  모든 입자가 동시에 항복하지 않는다는 저자 설명은 우리
AM 하중 차폐 (load-shielding) 서사와 같은 계열이다.  재설계 MPM 은 이 비를 **관측량**으로 낼 수 있어야 한다 (단일 속도장에서도 물질점에 입자 번호를
붙이면 입자별 항복 시점은 셀 수 있지만, 융합된 이웃과 하중 경로가 섞여 "입자 하나가 받는 접촉 하중" 이 정의되지 않는다).

**⑤ "재밍 뒤는 연속체처럼" 은 우리 한 방향 순차 연계를 반쯤 지지하고 반쯤 깬다.**  지지: 재밍 뒤에는 재배열이 무시되고 거시 거동이 다공
연속체 식으로 서술된다 — DEM 끝 (재밍 한참 뒤) 에서 연속체로 넘기는 구조 자체는 이 체제 구분과 맞는다.  깸: 그 연속체의 유효계수는
**접촉이 열려 있는 충전체**의 것이다 (p_c 에서 0).  우리 MPM 은 접촉을 닫아 버리므로 같은 "연속체" 가 아니다.

**⑥ 고 Φ 실패의 원인이 우리 격자 규칙과 같은 말이다.**  저자는 Φ > 0.97 의 모델–MPM 불일치를 *"small radii of curvature at the contact zones"*
의 해상도 부족으로 의심한다 — 우리 `d_h/dx ≳ 3.5` 규칙 · CL-41 (격자 미수렴) 과 같은 병.  입자별 장 MPM 은 접촉부를 더 잘게 풀어야 하므로
3D 비용이 커진다 (§9 행동 4).

---

## 9. [DEM 우선 (수영)] 트랙 — 후보별 행동

| 후보 | 이 논문이 | 이유 |
|---|---|---|
| **A** (우리 MPM + 움직이는 강체 AM) | **약화 (간접)** | A 는 AM 을 움직이게 할 뿐 SE–SE 는 여전히 붙는다 → §8-② 의 결합 골격 문제 · Z · 입자 경계 부재가 그대로.  이 논문은 A 를 직접 시험하지 않았다 |
| **A′** (다물체 / 다속도장 접촉 MPM) | **★ 강하게 지지 (실현 가능성)** | 입자별 장 + 접촉력 f^C 로 300 입자 · Φ 0.99 (2D) · 연화 없음.  단 3D · 규모 · 강체 혼합 · 제하 미시험 |
| **B** (입자 분해 FE / NSCD+FE) | **부분 지지** | 접촉 알고리즘 (CD = NSCD) 이 같다; 몸체를 FE 대신 MPM 으로 둔 혼성 = B 의 메시 왜곡 문제를 피하는 변형 |
| **C** (MDR 접촉 DEM) | **중립 ~ 약화** | 서론: Hertz 는 ~10 % 변형까지만 · *"too crude"* — 점접촉 법칙의 한계 진술 (MDR 은 그 한계를 다루려는 시도이나 이 논문은 다루지 않음) |
| **C′** (두 재료 항복캡 DEM) | **근거 없음** | — |
| **D0** (LIGGGHTS 2세대) | **관측량 하나 제공** | Z−Zc ∝ (Φ−Φc)^0.5 를 기존 DEM 압력 스윕 자료에 대어 볼 수 있다 (새 런 0) |

**구체 행동 (우선순위 순 · 전부 제안 — 1저자 비준 전)**
1. **2D 검증 벤치마크 (A′ 의 첫 판별 시험)**: 이 논문의 설정 (원판 300 · E 10 MPa · ν 0.45 · σ_y 0.4 MPa · H 0/1/3 · 마찰 0 · 위 벽 2 m/s =
   V/c_P 0.010 · V/c_S 0.034 · Φ0 0.78 · Δt 0.1 µs 는 암시적 기준) 을 **(i) 우리 단일 속도장 MLS-MPM** 과 **(ii) 입자별 장 시제품**으로 돌려
   Fig 3b 의 σ(Φ) (Φ 0.95 → H0 ≈ 1.11 · 탄성 ≈ 1.53 MPa, digitized) 와 Fig 5 의 √ 법칙에 대 본다.
   - **결과 전 등록할 예측 (§8-②)**: 단일 속도장은 같은 Φ 에 **더 큰 σ** 가 들고 (결합 골격), 입자별 장은 논문 곡선 근처.
   - ⚠ 지위 = **코드 대 코드 검증 (verification)**.  frame[4] 의 **보정은 여전히 실험 (기공 10–13 % @ 진밀도 1.64 g/cm³) 에만** 한다 — 이 논문
     곡선에 맞추지 않는다.  우리 쪽은 명시 (explicit) 적분이라 Δt · 접촉 알고리즘이 다르다는 한정을 함께 적는다.
2. **재하 속도를 V/c_S 로 정한다**: ν 0.49 에서는 V/c_P 0.03 이 V/c_S ≈ 0.21 이다.  재설계 MPM 의 판 속도는 V/c_S (예: ≤ 0.05) 기준으로 등록하고
   V/c_P 와 함께 기록 — 그들 집합체 V/c_S 0.034 가 참고점.
3. **질량 보존 씨앗 = 입자별 장의 공짜 이득**: 입자마다 자기 장을 가지면 각 SE 가 **원 구 질량 전부**를 들고 시작한다 → 지금의 복셀 합집합 씨앗이
   겹침 부피를 잃는 문제 (ε_sphere ↔ union 1.251 %p) 가 구조적으로 사라진다.  대신 **초기 겹침이 있으면 가짜 접촉력**이 생기므로 시작 상태는
   **겹침 없는 느슨한 충전**이어야 한다 — 11-09 1저자 결정 ("MPM 은 느슨한 충전에서 시작 · SE 질량 보존 씨앗") 과 정확히 같은 방향.
4. **3D 비용 어림 (derived(ours) — 결정 전 재확인)**: 짝 논문의 단일 원판 해상도 R/Δr ≈ 34.5 를 3D 구에 쓰면 SE 하나 ≈ 1.7 × 10⁵ 물질점 ×
   32,832 = **5.6 × 10⁹** (불가).  R/Δr 8 이면 7.0 × 10⁷ · 10 이면 1.4 × 10⁸ (우리 512 격자 런 ≈ 1.15 × 10⁸ 점과 같은 자릿수).  여기에
   **입자별 격자 (장) 의 메모리**가 더해진다 — 입자 3.3 만 개에 격자 3.3 만 벌은 그대로는 안 된다.  **우리 추론 (논문 밖)**: 닿을 수 있는 입자끼리만
   다른 번호를 주는 "장 색칠 (field colouring)" 로 장 수를 O(10) 으로 줄이는 설계를 검토 — A′ 설계 메모의 질문으로 올린다.
   ⇒ A′ 시범은 **2D 또는 작은 3D RVE (SE 수백 ~ 수천)** 부터.
5. **해석식 (5)–(17) 을 공통 맞춤 틀로**: 우리 MPM · DEM · (있다면) 실험 압밀 곡선에 같은 함수형을 맞춰 **p_c 를 비교** — 단일 속도장 MPM 에서
   맞춘 p_c 가 재밍 기공률보다 크게 나오면 §8-② 가설의 간접 증거.  선결: 우리 MPM 곡선이 재밍점을 포함해야 한다 (지금 씨앗은 재밍 한참 뒤).
6. **f_p(Φ) 측정**: 우리 MPM 은 누적 소성 변형 (`dg_acc`) 으로 항복 부피 분율을 셀 수 있다 → 식 (11) f_p = α ln(Φ/Φc) 가정을 시험하는 값싼 산출물.
7. **D0 (새 런 0)**: 기존 순수 SE 압력 스윕 · LHS 코퍼스의 (Φ, SE–SE CN) 로 Z−Zc ∝ (Φ−Φc)^0.5 를 맞춰 지수를 기록 — DEM 미세구조의
   재밍 물리 정합 점검 (보정 아님).
8. **제하는 이 논문에서 얻을 것이 없다** — 하중–제하 루프 근거는 `pycompact2025_dem_mpfem_workflow` (Fig 4b) · `demirtas2021_mpfem_hollow_sphere_die_compaction`
   (recoil) 쪽을 쓴다.

---

## 10. 인용 가능 문장 (deck / paper 용)
- DEM 한계 (p.1): *"In DEM, particles are assumed to be slightly deformable through different contact theories such as the Hertz contact theory,
  which is only valid up to about 10% of strain.  However, in the context of compaction process modelling, this assumption is too crude.  For
  realistic simulation of compaction, it is hence primordial to combine a continuum representation of the particles, allowing for their deformation
  according to a prescribed constitutive model, with appropriate contact interactions between particles [8, 9]."*
- 재밍 뒤 체제 (p.5): *"Above this point, particle rearrangement is negligible and the particle shape change controls essentially the packing
  evolution.  One can hence assume that the packing behaviours beyond the jamming point are almost like a continuum medium."*
- 우리 1-liner (defensible): *"입자마다 자기 배경격자를 두고 접촉을 Contact Dynamics 로 푼 MPM 은 연화 없이 (E/σ_y = 25) 2D 소성 원판을 Φ ≈ 0.99
  까지 압밀한다 (Nezamabadi 2022) — 우리 단일 속도장 MPM 의 연화 필요성은 구성식이 아니라 접촉 표현의 문제일 수 있다 (가설, 2D 근거)."*

---

## 11. 주의 · 한계 · PDF 가 말하지 않는 것 (over-claim 방지)

**전이할 때의 한계**
- 2D 원판 · 단일 재료 · mm 급 · E 10 MPa — Φ · Φc · MPa 절대값 전이 금지.
- 시작 Φ0 0.78 은 2D 재밍 직전 — **느슨한 충전의 재배열 단계는 이 논문이 거의 다루지 않는다** (0.78 → 0.8).  우리 재설계 요구 (느슨한 데서 시작)
  의 가장 어려운 구간이 비어 있다.
- 마찰 0 (집합체) · 강체 입자 혼합 없음 · 제하 없음 · 전달물성 없음.

**이 논문 자체의 약점**
- **격자 간격 · 입자당 요소 수 · 수렴 시험 없음** — 고 Φ 불일치를 해상도 탓으로 의심만 한다.
- **비용 (코어 · 시간) 미기재** — "parallelised" 라고만.
- **σ_yy · ε_yy 정의 미기재** (Fig 1) · **κ 정규화 모호** — 라벨은 κ/⟨d⟩ 인데 원 상태 값이 정확히 1.000 (digitized) 이라, 라벨대로라면 단위가
  맞지 않는다 (초기 곡률로 나눈 값에 가깝다 · [미확인]).
- 해석식: 매개변수 4 개 + Φc 를 **같은 MPM 곡선에 맞춘 뒤** "good agreement" — 예측력 시험 (맞춤에 안 쓴 런) 은 소성 3 개 중 2 개뿐 (소성 매개변수는
  "one of the plastic simulation results" 로 맞춤) 이고 어느 런인지 미기재.
- f_p = α ln(Φ/Φc) 는 **측정 없이 가정** · K_p 미정의 · 식 (22) 적분의 근사 미언급 · 부호 규약 미기재.
- 결론의 *"weaker stress chains between particles"* 는 **그림 · 수치 없는 서술**.
- 절대 Zc · Z1 미기재 → 다른 모델과 숫자 대조 불가.
- Fig 3 과 Fig 4 는 Φ ≥ 0.8 구간의 표본 점 수가 다르고 (탄성 31 vs 32 · 소성 30 vs 33) 끝 Φ 도 약간 다르다 (탄성 0.985 vs 0.990, digitized).
  Fig 3 의 σ(Φ) 에서 Fig 4 의 σ−σc 를 빼면 **σc ≈ 0.17–0.19 MPa (중앙값)** 로 맞물려 큰 모순은 없다 — 두 그림이 같은 런의 다른 표본으로 보인다 (미기재).
- accepted manuscript 판 — 출판본 그림 · 수치와 다를 수 있다.
- DEM 초기 배치 생성 (코드 · 접촉식 · 다짐 방법) 미기재 · 상자 치수 미기재 · [2, 4] mm 의 뜻 (지름/반지름) 미기재.

**frame 규율 재확인**
- frame[4]: 이 논문 곡선은 **보정 표적이 아니다** — 코드 검증 기준점일 뿐.  우리 각 모델은 실험 (기공 10–13 %) 에 따로 보정한다.
- frame[5]: 이 논문은 MPM 쪽 (형상 · 기계) 을 **접촉까지** 넓힌 예다.  전달물성 (DEM 고유) 은 전혀 다루지 않는다.

---

## 12. 관련 카드 (중복 서술 금지 — 겹치면 넘김)
- `nguyen2017_mpm_bpm_deformable_particle_compaction` — **짝 (같은 그룹 2017 전신)**: MPM-CD (탄성) vs BPM (소성) · 마찰 μ 0.5 · 절대 Z.
- `pycompact2025_dem_mpfem_workflow` · `demirtas2021_mpfem_hollow_sphere_die_compaction` — 같은 층 (3) 을 **MPFEM** 으로 · 제하 루프 근거.
- `zunker2024_mdr_contact_model_partI` · `zunker2024_bulk_elastic_partII` · `zunker2025_dem_large_deformation_compaction` — 후보 C (MDR).
- `giannis2021_stress_based_multicontact_dem` · `varkey2026_multicontact_elastoplastic_dem` — DEM 쪽 다중 접촉 보정 (평균장).
- `devaucorbeil2020_mpm_after_25_years_review` — MPM 접촉 (Bardenhagen 다물체) 의 리뷰 위치 · 우리 scaffold = 내재 no-slip 접촉의 최소 활용.
- `arzt1982_particle_coordination_densification_spheres` — 3D 구 치밀화의 배위수–밀도 기하 (Z(Φ) 의 3D 대조).
- `martinbouvard2003_dem_composite_cold_compaction` · `bouvard2000_hard_soft_powder_densification` — 강체 + 무른 입자 혼합 (이 논문에 없는 축).

---

## 🗨️ Q&A 로그
- (비어 있음)

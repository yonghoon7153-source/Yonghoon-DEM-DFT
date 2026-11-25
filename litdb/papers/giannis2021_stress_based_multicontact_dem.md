# 입자 응력텐서 trace 로 모든 접촉을 서로 묶은 non-binary DEM 접촉모델 (MC-stress) — Giannis (Granular Matter 2021)

> slug `giannis2021_stress_based_multicontact_dem` · DOI `10.1007/s10035-020-01060-8` · type `DEM (contact-LAW theory, non-binary multi-contact)` · PDF `Stress_based_multicontact_model_for_discreteelement_simulations.pdf` · digested `2026-08-25` · status ✅
> ★★ **이것이 Varkey 2026 `F_mc` 의 원전이고, 우리 `elasto_plastic_feasibility.md` §1 의 "경로 B" 정의서다.**
> ★★ **공저자에 S. Luding** — 우리 LIGGGHTS `hooke/hysteresis` 정의서(`luding2008_cohesive_frictional_contact_models`)의 저자.
> ★★ **구현 플랫폼이 LIGGGHTS 다** (본문 §3.2 명시). 우리와 같은 코드.
> ⚠⚠ **이 카드의 가장 중요한 판정: MC-stress 는 우리 18× 연화의 "물리적 대체"가 아니다 — 부호가 반대다.** §7-3 참조.

---

## 0. 왜 이 논문을 지금 읽는가 (먼저 읽을 것)

우리 litdb 는 이 모델을 두 곳에서 이미 참조하고 있었지만 **원전을 안 읽고 Varkey 2026 의 2차 인용으로만** 갖고 있었다.

| 어디 | 무엇이라 적혀 있었나 | 이 카드의 판정 |
|---|---|---|
| `elasto_plastic_feasibility.md` §1 경로 B | "F_mc = ρ>0.7 **치밀영역 과강성** — 우리 18× 연화가 노리는 증상의 물리적 대안" | ⚠ **부호가 틀렸다.** 원전이 고치는 증상은 과강성이 아니라 **under-stiffness**(고변형에서 힘 과소예측)이고, F_mc 는 **힘을 더한다** = 침대를 **더 뻣뻣하게** 만든다. 우리 연화는 침대를 **무르게** 만든다. **같은 증상 다른 처방이 아니라 반대 방향 처방이다.** |
| `varkey2026_multicontact_elastoplastic_dem.md` §7 | "multi-contact F_mc(구속항) ↔ 우리 18× E 연화 — 같은 증상(과강성) 다른 처방" | 같은 정정. 단 그 카드의 **Supplementary 절**(FEM Fig S1 요약)은 이미 "TN 단독은 고변위서 FEM 을 **under-predict**" 라고 옳게 적어 두었다 — 본문 표와 SI 절이 **서로 모순**이었다. |
| `contact_models_layer_map.md` §1 | multi-contact 는 표에 없음 (항복캡 축만 있음) | ⇒ **층위 표에 축이 하나 빠져 있다**: 층위 ① 안에 **binary ↔ non-binary** 축. §7-1 에 제안. |

그리고 이 논문 자체에 우리가 몰랐던 세 가지가 있다:
1. **구현이 LIGGGHTS 다.** Varkey 는 Ansys Rocky(상용)를 썼기 때문에 우리 litdb 는 "경로 B = 상용 또는 C++ 커스텀"으로 적어 뒀는데, **원전은 우리와 같은 코드에 넣었고 부록에 pseudo-code 를 공개**했다. 이식 난이도 판정이 바뀐다(§7-5).
2. **부록 pseudo-code 의 계수가 본문 식과 2배 다르다** (본문 `1/3`, pseudo-code `1/6`). §4-4.
3. **β 는 "재료마다 보정" 이라고만 적혀 있는데, 우리가 계산해 보니 `β·ν` 는 E 가 280만 배 변하는 동안 0.79→1.24 로 거의 안 움직인다.** 저자들은 이 조합을 보고하지 않았다. §4-6 — **이게 이 카드에서 가장 값진 발견**이고, 사실이면 β 가 자유변수가 아니게 된다.

---

## 1. 한 줄 요약

고전 DEM 의 **"접촉은 서로 독립"이라는 가정**을 깨기 위해, 입자별 응력텐서 σᵖ = (1/Vᵖ)Σ lᶜ⊗fᶜ 의 **trace**(= 정수압)를
Hertz 법선력에 **덧셈 보정항 (β·ν·A_ij)·P_ij** 로 얹어 **한 입자의 모든 접촉을 서로 의존하게 만든** 접촉법칙.
LIGGGHTS 에 2-pass 로 구현했고, 하이드로겔/고무/유리 구의 **단축 구속압축**에서 고전 DEM 이 놓치는 **고변형 비선형 강화**를
실험 수준으로 회복한다. **자유변수는 β 하나(경험적 보정)** — 물성에서 유도되지 않는다.
⚠ **소성은 전혀 없다** (기반 법칙이 순수 Hertz). 저자들 스스로 "고응력 탄소성은 향후 과제"라고 outlook 에 적었다.

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **K. Giannis¹²**, C. Schilde¹², J.H. Finke¹², **A. Kwade¹²**, **M.A. Celigueta³**, K. Taghizadeh⁴⁵, **S. Luding⁴** | **Granular Matter 23:17 (2021)**, 14 pp. Received 2019-08-16 / Accepted 2020-09-19 / Online 2021-02-19 | **10.1007/s10035-020-01060-8** | **배터리 소재 아님** — 하이드로겔·고무·유리 구. LPSCl/NMC811 데이터 **0** | **DEM 접촉 LAW 이론 + 구현(LIGGGHTS) + 실험 검증** |

- ¹ iPAT, TU Braunschweig / ² PVZ, TU Braunschweig / ³ **CIMNE Barcelona**(Kratos 계열) / ⁴ **Multi-Scale Mechanics, U. Twente**(Luding) / ⁵ Inst. Applied Mechanics, U. Stuttgart.
- 자금: EU Marie Skłodowska-Curie ITN FP7 **ITN607453 TMAPPP**.
- ⚠ **라이선스**: 우리가 받은 PDF 본문에 **Creative Commons / Open Access 문구가 없다** (Luding 2008 과 달리). © Springer-Verlag. → 그림 재사용 시 확인 필요.
- **계보**: Kwade/Schilde(TU-BS) = Varkey 2026·Sangrós 계열 / Celigueta = CIMNE(Oñate) DEM-FEM / Luding = 우리 접촉법칙 정의서 저자 / Taghizadeh = Luding 그룹 micro-macro.

## 3. 핵심 수치

### 3.1 재료 파라미터 (Table 1, [21,23,24] 인용) — stated

| | **Hydrogel** | **Rubber** | **Glass** | (참고) 우리 LPSCl |
|---|---|---|---|---|
| ρ (kg/m³) | **11.5** ⚠ | 2000 | 2500 | 1640 (Bazzoun) |
| 직경 (cm) | 2 | 2 | 0.4 | 0.0001 (1 µm) |
| **E (Pa)** | **23.3 × 10³** | **1.85 × 10⁶** | **65 × 10⁹** | **22–24 × 10⁹** (real) / 1.35 × 10⁹ (우리 E_eff) |
| **ν** | **0.5** | **0.46** | **0.24** | **0.37** (Bazzoun) / 0.360 (우리 DFT) / 0.3 (우리 DEM 입력) |
| COR | 0.95 | 0.7 | 0.98 | 0.4 (Bazzoun) |
| μ | 0.03 | 0.5 | 0.2 | 0.4 (Bazzoun) |

- ⚠ **ρ_hydrogel = 11.5 kg/m³ 는 실물 하이드로겔(≈1000)보다 2 자릿수 낮다.** 다만 이 값으로 논문의 접촉시간
  t_c = 0.0018 s 를 재계산하면 **우리 검산 1.56 × 10⁻³ s 로 맞아떨어진다** ⇒ 오타가 아니라 **실제로 그 값을 썼다**.
  스케일링 이유는 논문에 설명 없음. (물리 결론에는 영향 없음 — 준정적 압축 결과는 밀도에 둔감.)
- ★ **E 스팬이 2.8 × 10⁶ 배**(23.3 kPa → 65 GPa). **우리 LPSCl(22–24 GPa)은 유리 쪽 끝에 붙어 있다**(유리의 1/2.7).
  ⇒ 우리에게 전이 가능한 유일한 케이스는 **유리(§4.9, Fig 16)** 이고 하이드로겔/고무는 참고용이다.

### 3.2 ★ 보정 prefactor — 이 논문의 **유일한 자유변수** (stated)

| 케이스 | 재료 (ν) | **γ (MC-strain)** | **β (MC-stress)** | 보정 방식 |
|---|---|---|---|---|
| 단일 고무 구 vs Tatara 1989 실험 (δ/r → 40 %) | rubber (0.46) | **0.55** | **1.71** | **최대변형점 1점에 fit**, 사이 경로는 검증 |
| 514 하이드로겔 침대 (naive) | hydrogel (0.5) | 1.0 | 1.0 | 무보정 참조 |
| 514 하이드로겔 침대 (보정) | hydrogel (0.5) | **1.12** | **1.65** | 실험 곡선에 fit |
| **1921 이봉 하이드로겔 침대** | hydrogel (0.5) | 1.12 | 1.65 | ★ **재보정 없이 전이** = 논문 유일의 예측 시험 |
| 514 고무 침대 | rubber (0.46) | **0.53** | **1.74** | ⚠ **실험 없음** (수치 비교만) |
| **17 유리 구슬** | glass (0.24) | **4.5** | **5.17** | 저자 자체 실험에 fit |

- MC-strain 의 γ 에는 **이론 앵커가 있다**: 비압축(ν→0.5) γ=0.5, 압축성(ν→0) γ=1 [41 Greaves 2011]. 고무(ν=0.46)는
  **0.53–0.55 로 이론값과 일치**하지만 **유리는 4.5 로 이론에서 ~6× 벗어난다** (저자 설명: δ_{k→c} ∝ 1/E 라 뻣뻣할수록 γ↑).
- **MC-stress 의 β 에는 이론 앵커가 없다.** 본문 표현 그대로 *"β is an **adjustable dimensionless empirical** geometric prefactor"*.

### 3.3 결과 수치 (전부 그림에서 digitized — TREND only, ± 표시 없음)

| 그림 | 조건 | Experiment | Classical DEM | MC-strain | MC-stress | classical 과소배율 |
|---|---|---|---|---|---|---|
| Fig 4 | 단일 고무 구, δ/r = 40 % | **≈ 433 kPa** | **≈ 245 kPa** | ≈ 433 (γ=0.55) | ≈ 433 (β=1.71) | **1.77×** |
| Fig 11a | 514 하이드로겔, ε = 13.4 % | **≈ 555 Pa** | **≈ 245 Pa** | ≈ 455 (γ=1) | ≈ 400 (β=1) | **2.27×** |
| Fig 11b | 〃 (보정 후) | ≈ 555 | ≈ 245 | ≈ 525 (γ=1.12) | **≈ 555 (β=1.65)** | — |
| Fig 14 | **1921 이봉 하이드로겔, ε = 10 %** (전이) | **≈ 440 Pa** | **≈ 200 Pa** | ≈ 430 | **≈ 445** | **2.2×** |
| Fig 15 | 514 고무, ε = 28 % | **없음** | ≈ 148 kPa | ≈ 258 (γ=0.53) | ≈ 280 (β=1.74) | (실험 없음) |
| Fig 16 | **17 유리 구슬, ε = 2.64 %** | **≈ 45 MPa** | **≈ 35 MPa** | ≈ 45 (γ=4.5) | ≈ 45 (β=5.17) | **1.29×** |
| Fig 16 | 〃, ε = 2.0 % (중간) | ≈ 23.5 | ≈ 17.5 | ≈ 18.7 | ≈ 20.5 MPa | 1.34× |

- ★ **stated 임계값 하나**: *"Hertz theory is applicable only for small deformation with an **upper limit of δ/r ≤ 0.1 (10 %)**"* (§3.3).
- ⚠ **논문 전체 최대 응력 = 유리 45 MPa.** 우리 성형압 300 MPa 의 **1/6.7**. porosity·상대밀도는 **논문 어디에도 없다**.

### 3.4 계산비용 (Table 2, stated) + 우리가 계산한 배율

| Model | T-hydrogel [s] | T-rubber [s] | T-glass [s] |
|---|---|---|---|
| Classical | 38 | 84 | 22 |
| MC-strain | 668 | 1568 | 45 |
| **MC-stress** | **216** | **538** | **29** |

| 배율 (우리 계산) | hydrogel(514) | rubber(514) | glass(17) |
|---|---|---|---|
| **MC-stress / classical** | **5.68×** | **6.40×** | 1.32× |
| MC-strain / classical | 17.6× | 18.7× | 2.05× |
| MC-strain / MC-stress | 3.09× | 2.91× | 1.55× |

⚠ **하드웨어·코어수·벽시계 측정 규약이 논문에 없다** → 표 **내부의 상대비교만** 유효. 유리(17 입자)는 입자수가 적어
오버헤드가 희석된 것이지 "유리에서 싸다"는 뜻이 아니다.

---

## 4. 시뮬레이션 방법 ★★★ — 모델을 식 수준으로

### 4.1 기반 (classical) DEM — §2

- **운동방정식 (eq 1)**: `m_i r̈_i = F_i + m_i g`, `I_i ω̇_i = τ_i`, `τ_i = Σ_c (l^c_i × F^c_i + q^r_i + q^t_i)`. **중력은 무시**(g 항 비활성).
- **겹침 (eq 2)**: `δ_n = (r_i + r_j) − (r_i − r_j)·n > 0`, `n = (r_i − r_j)/|r_i − r_j|`.
- **법선력 (eq 3) = Hertz + 점성**:
  ```
  f_n = f_n^el + f_n^visc = (4/3)·E*·√(r_ij·δ_n)·δ_n  +  η_n·√(r_ij·δ_n)·δ̇_n
  r_ij = r_i r_j /(r_i + r_j)          (환산반경)
  1/E* = (1−ν_i)/(2G_i) + (1−ν_j)/(2G_j)   [= (1−ν_i²)/E_i + (1−ν_j²)/E_j 와 동일 — 우리 검산 확인]
  ```
- **접선력 (eq 4–6)**: Mindlin 증분, Tsuji 형 `Δf_t = k_t Δδ_t + η_t Δv_t`, `k_t = 8G*√(r_ij δ_n)`,
  `1/G* = (2−ν_i)/G_i + (2−ν_j)/G_j`, Coulomb `f_t ≤ μ f_n`, `μ_d = μ_s`, `Δδ_t ≅ v_t Δt`.
- ⚠ **소성·항복캡·점착 전부 없음.** 순수 탄성 Hertz + 점성 감쇠. **이것이 우리 hooke/hysteresis 와 다른 첫 지점**
  (우리 것은 Luding eq 6 의 piecewise-선형 이력 + k_c 점착 + δ₀ 영구겹침을 갖고 있다).

### 4.2 비교대상 — MC-strain (Brodu, Dijksman, Behringer, Phys. Rev. E 91 (2015) [23]) — §3.1

한 접촉 k 가 만드는 변위장을 다른 접촉 c 위치에서 평가해 **겹침을 더한다**:
```
                (1+ν) f^c_k    ⎡                                   (3−4ν)n_k·n_c − (1−2ν)(n_k + u_kc)·n_c ⎤
δ_{k→c} = −γ · ───────────── · ⎢ (n_k·u_kc)(n_c·u_kc) + ───────────────────────────────────────────────── ⎥   (eq 7)
                 2πE·d_kc      ⎣                                          1 + n_k·u_kc                     ⎦

f_n^el = (4/3)·E*·√r_ij·( δ_n + Σ_k δ_{k→c} )^{3/2}                                                         (eq 8)
```
- `d_kc` = 접촉점 사이 거리, `n_k`·`n_c` = 각 접촉면 법선, `u_kc` = 접촉 간 단위벡터 (Fig 1).
- **γ**: 비압축(ν→0.5) 0.5, 압축성(ν→0) 1 [41].
- ★ **구조적 비용**: 입자마다 **모든 접촉 쌍 (k,c)** 의 상대 기하가 필요 = **O(C²)**. 그리고 원리적으로 **반복(iterative)**.
  Brodu 는 준정적 가정으로 **1회 반복**만 하는데, Giannis 는 *"fast compression 과 large applied engineering strain 에서는
  반복이 불가피하다 — 다음 스텝의 입자 가속도가 **엄청나져 불안정**해진다"* 고 명시(§1).

### 4.3 ★★★ MC-stress — 이 논문의 모델 (§3.2)

**(a) 입자 응력텐서 (eq 9)** — 정의 자체는 Luding [9]·Zhang [42]·Labra [43] 의 표준 coarse-grain 형태:
```
σ^p = (1/V_p) · Σ_{c=1}^{C^P}  l^c ⊗ f^c                                        (eq 9)
```
`V_p` = 입자 부피, `C^P` = 그 입자의 접촉 수, `l^c` = **branch vector**, `f^c` = 접촉력, `⊗` = 다이애딕(2계 텐서).

**(b) 보정된 법선력 (eq 10) — 모델 본체**:
```
f_n^el = (4/3)·E*·√(r_ij·δ_n)·δ_n  +  ( β · ν · A_ij ) · P_ij                   (eq 10)

  P_ij = (1/3)·( tr(σ_i) + tr(σ_j) )        [본문 + Fig 2 박스]
  tr(σ) = σ_xx + σ_yy + σ_zz
  β    = 무차원 **조정 가능한 경험적 기하 prefactor**  ← 자유변수
  ν    = Poisson 비  (★ ν = 0 이면 모델이 자동으로 꺼진다)
  A_ij = 활성 접촉쌍의 계면 접촉면적
```

**(c) `A_ij` 의 정의** — 본문 §3.2 에는 *"접촉면적"* 이라고만 적혀 있고, **해석해 절(§3.4.3)에서야 명시**된다:
```
A_ij = π · r_ij · δ            (= Hertz 접촉면적 πa², a² = R*δ)
```
⇒ **탄성 Hertz 면적**이다. 소성 면적(우리 Stage-E Tabor/volume)도, 실제 평탄화 면적도 아니다.

**(d) 저자들이 밝힌 설계 동기 4가지** (§3.2 그대로):
1. **단순성/속도** — MC-strain 처럼 모든 쌍의 상대 방위를 안 본다, **반복 없음**.
2. **물성 내장** — ν 가 식에 있어 **ν=0 이면 모델이 비활성**.
3. **접촉 기하 A_ij 는 어차피 이미 계산되어 있다**.
4. **평균 응력이 한 입자 주변 접촉의 개수와 세기를 함께 담는다**.

### 4.4 ⚠⚠ **정규화가 논문 안에서 세 번 서로 다르다** (원전 결함 — β 전이 시 치명적)

| 출처 | P_ij 정의 | 본문값 대비 |
|---|---|---|
| **본문 eq 10 + Fig 2 박스** | `(1/3)(tr σ_i + tr σ_j)` = **두 입자 압력의 합** | **1.0×** (기준) |
| **부록 pseudo-code (line 15)** | `(1/6)(StressTrace[i] + StressTrace[j])` = **두 입자 압력의 평균** | **0.5×** |
| **해석해 eq 11** | `P_4 = (4/V)·f·d` = 단일 입자 tr σ (1/3 도, 쌍평균도 없음) | **1.5×** (동일 입자 기준) |

⇒ **β 값은 어느 정규화로 보정됐는지와 반드시 함께 인용해야 한다.** 논문의 β = 1.65/1.71/1.74/5.17 은 실제 계산이
**부록 pseudo-code(1/6)** 로 돌았다면 본문 식(1/3) 기준으로는 **절반**을 써야 같은 물리가 된다.
⚠ 추가로 **`l^c` 가 중심→접촉점(≈a) 인지 중심→중심(=d) 인지 논문이 명시하지 않는다.** eq 11 이 `d` 를 쓴 것으로 보아
중심→중심으로 읽히는데, eq 9 의 "particle stress tensor" 표준 정의는 중심→접촉점이다. **두 규약은 2배 차이.**
⇒ **정규화 × branch-vector 조합으로 총 6배(k = 0.25 … 1.5)의 모호성**이 β 안에 흡수돼 있다 (§7-4 에서 정량).

### 4.5 ★ 부록 pseudo-code — 실제 알고리즘 (2-pass)

> ⚠ 이 블록은 PDF 에 **벡터 아웃라인**으로 그려져 텍스트 추출이 안 된다. 아래는 우리가 **페이지를 렌더해 읽은 것**이다.

```
 1  for i = 1 to Nparticles do
 2      for j = 1 to Nneighbours do
 4          ForcesLocal[i,j] = Forces( Overlap[i,j] );
 6          StressTrace[i] += Stress( ForcesLocal[i,j], BranchVector[i,j] );
 8          StressTrace[j] += Stress( ForcesLocal[i,j], BranchVector[i,j] );
 9      end
10  end
11
12  for i = 1 to Nparticles do
13      for j = 1 to Nneighbours do
15          PressureSum[i,j] ← (1/6)( StressTrace[i] + StressTrace[j] );
17          ForcesGlobal[i,j] ← Forces( Overlap[i,j], PressureSum[i,j] );
18      end
19  end
```
- **PASS 1** = 고전 힘 계산 + 두 입자의 stress trace 누적 (Newton 3법칙: 같은 `l⊗f` 를 i·j 양쪽에 더한다 —
  `tr(l⊗f) = l·f` 는 l,f 가 동시에 부호를 뒤집어도 불변이라 성립).
- **PASS 2** = 같은 이웃 리스트를 **다시 훑어** 압력 보정을 넣은 힘으로 **재계산**.
- ⇒ **시간 지연 없음**(같은 timestep 안에서 완결) = 명시적 lag 불안정성이 없다. 대신 **이웃 스윕이 2배**.
- ⇒ 실측 오버헤드 5.7–6.4× (Table 2) 는 "스윕 2배" 보다 크다 ⇒ **PASS 2 가 Newton 3법칙 반쪽 계산을 못 쓰고
  힘을 통째로 재계산**하는 구조로 보인다(논문에 명시 없음).

### 4.6 ★★★ 우리가 발견한 것 — `β·ν` 는 거의 상수다 (논문에 없는 분석)

eq 10 에서 β 와 ν 는 **항상 곱으로만 등장**한다. 논문의 4개 보정값을 그 곱으로 다시 쓰면:

| 케이스 | E | ν | β | **β·ν** |
|---|---|---|---|---|
| 단일 고무 구 | 1.85 MPa | 0.46 | 1.71 | **0.787** |
| 514 고무 침대 | 1.85 MPa | 0.46 | 1.74 | **0.800** |
| 514 하이드로겔 침대 | 23.3 kPa | 0.50 | 1.65 | **0.825** |
| 17 유리 구슬 | 65 GPa | 0.24 | 5.17 | **1.241** |

**E 가 2.8 × 10⁶ 배 변하는 동안 β·ν 는 0.787 → 1.241 (1.58× 폭) 안에 들어온다.** 셋은 **0.79–0.83 (±2.4 %)** 로 뭉친다.
- 저자들의 설명("뻣뻣한 재료는 접촉면적이 작으니 β 를 키워야 한다")은 **β 단독의 3.1× 차이를 설명하려는 것**인데,
  그 차이의 **2.08배는 그냥 ν(0.5 → 0.24)** 이다. 남는 것은 1.5× 뿐이다.
- ⚠ **남은 1.5× 를 물리로 귀속할 수 없다** — 유리 케이스는 **입자 17개(원통 안)** 라 배위수 C 가 514-입자 침대보다
  낮을 것이고, §7-4 에서 보이듯 보정항은 **C 에 비례**한다. **논문이 C 를 한 번도 보고하지 않아** 분리 불가.
- ⇒ ★ **가설(우리 것, 미검증)**: `β·ν ≈ 0.8` 이 준-보편 상수라면 β 는 자유변수가 아니라 `β ≈ 0.8/ν` 로 **유도된다**.
  우리 LPSCl(ν = 0.37)에 대입하면 **β ≈ 2.1–3.4** (밴드 0.79–1.24 기준) — **새 보정 없이 쓸 수 있는 예측값**.
  ⚠ **논문의 주장이 아니다. 4점·3재료·C 미보고 → 근거가 약하다. 인용 시 반드시 "우리 재분석"으로 표기.**

### 4.7 입자 처리 ★ (DEM 판 "무질서 처리")

- **구(sphere)만.** 형상 변화 **0**. 비구형 언급 없음.
- **PSD**: 514 침대는 "polydisperse, 평균 직경 2.1 cm"(분포폭 미기재) / **1921 침대는 명시적 이봉**(1573개 ⌀1.6 cm +
  348개 ⌀2.1 cm, **크기비 1.31**) / 유리 17개는 사실상 mono(3.8–4.0 mm).
  ⚠ 크기비 1.31 은 **Furnas/McGeary 영역(7:1)이 아니다** — 우리 12:4:1 이봉 패킹과 비교 불가.
- **강체 구 + 힘법칙 보정.** 층위(1) CONTACT LAW 만. **층위(2) 접촉면적 소성도, 층위(3) 형상 소성도 없다.**
  ★ 특히 **여기엔 CONTACT 소성조차 없다** (기반이 Hertz) — Varkey 가 Thornton–Ning 을 붙여서야 탄소성이 된다.
- **seed / 실현 수**: 앙상블 없음. 각 케이스 **1회 실현**으로 보인다 (반복·산포 보고 없음).

### 4.8 도메인 / 프로토콜

| 케이스 | 도메인 | 입자수 | 프로토콜 |
|---|---|---|---|
| 3·5 입자 충돌 | 자유공간 | 3 / 5 | **초기속도 10 m/s 대향 충돌**. hydrogel t_c = 0.0018 s, Δt = 1×10⁻⁵ s; rubber t_c = 0.0025 s, Δt = 2×10⁻⁵ s |
| 5 입자 해석해 | bbox [−0.03,0.03]²×[−0.01,0.01] → [−0.025,0.025]²×[−0.01,0.01] | 5 | 등방 공학변형률 부여 |
| 514 하이드로겔 | 0.165 × 0.165 × **0.167** m³ | 514 (⌀̄ 2.1 cm) | z 단축 압축 → **ε_max 13.4 %** → **감압(decompression)** |
| 1921 하이드로겔 | 0.165 × 0.165 × **0.147** m³ | **1573 + 348** | z 단축 → ε_max **10.2 %** |
| 514 고무 | 위와 동일 | 514 | z 단축 → ε_max **28 %** |
| 17 유리 | 원통 **⌀12 mm × h 10.5 mm** | 17 (⌀̄ 3.9 mm) | z 단축 → ε_max **2.64 %** |

- **변위 제어(공학변형률)**, 서보/PID 정압 제어 **아님** ⇒ 우리 300 MPa 정압 servo 프로토콜과 **BC 자체가 다르다**.
- 주기경계 **없음** (실제 상자/원통 벽).
- ⚠ **3·5 입자 데모의 겹침이 δ ≈ 0.016 m (r = 0.01 m)** 까지 간다 = **δ/r ≈ 1.6, 구가 서로의 중심을 통과**.
  이 영역에는 어떤 접촉모델도 물리가 없다. **데모는 "모델이 다르게 반응한다"는 정성 시연이지 검증이 아니다.**
- ⚠ Fig 6–9 의 x축 라벨이 `[µs]` 인데 범위가 0–2.5 다. **t_c = 1800 µs 이므로 라벨은 ms 여야 한다** (논문 내부 불일치).

### 4.9 구현

- **플랫폼 = LIGGGHTS-DEM [44 = Kloss 2012]** (★ 우리와 같은 코드).
- **Newton 3법칙 pair-once 최적화 [45 = Plimpton 1995]** 를 유지하며 넣었다고 명시:
  *"we can integrate our new formula without violating the momentum balance [F^c_ij = −F^c_ji]"*.
- 참고문헌 **[49] = Kloss, "Source code for MC-DEM simulations and simulation setup for hydrogel multicontact example",
  github.com/CFDEMproject/LIGGGHTS-PUBLIC (2017)** — **MC-DEM 이 LIGGGHTS-PUBLIC 에 공개 예제로 존재**한다
  (γ = 1.12 를 "[49] 가 제안한 값"이라고 인용하므로 최소한 **MC-strain** 쪽 구현·예제가 공개).
- **MPM / continuum / 전달 솔버**: 전부 **없음**.

---

## 5. Figure set ★ (전 16그림 + 2표)

| Fig | 무엇을 보여주나 | 우리가 쓸 점 |
|---|---|---|
| **1** | MC-strain 기하: 한 접촉이 다른 접촉에 주는 변위장. `d_kc`, `n_k`, `n_c`, `u_kc`. **접촉점이 구 표면에 구속되지 않는다**(변형과 일관) [Brodu 23 에서] | MC-strain 이 왜 O(C²)·반복인지 한 장 설명 |
| **2** ★ | **MC-stress 개념도**: 좌 "Conventional DEM → binary, F=f(δ)" / 우 "Alternative → F=f(δ, P_ij)", 박스에 `P_ij = (tr σ_i + tr σ_j)/3`. 붉은 입자 i·푸른 입자 j | **경로 B 설명 슬라이드 1순위** (단 라이선스 확인) |
| **3** | 고무 구가 두 강체 평판 사이에서 압축되는 3D 렌더 (a) 초기 (b) 압축 | — |
| **4** ★★ | **보정 그림**: 단일 고무 구, 압력 F/πr² [kPa] vs δ/r [%] 0–40. Experiment(Tatara 1989) / Classical / MC-strain γ=0.55 / MC-stress β=1.71 | **"Hertz 는 δ/r ≤ 10 % 까지만"의 stated 근거.** 우리 pure-SE ⟨δ⟩/d ≈ 11 % (= δ/r ≈ 22 %) 는 **이 한계 밖** |
| **5** | 3입자·5입자 테스트 배치 모식 | — |
| **6** | E_kin(t), 하이드로겔 3·5입자 | MC 계열이 **더 빨리 에너지 감소, 최대겹침 더 일찍 도달** |
| **7** | 중앙입자 겹침 δ(t), 하이드로겔 3·5 | ★ **MC-strain 이 최대겹침 최대, MC-stress 가 최소** — 두 모델이 **반대 방향으로 겹침을 바꾼다** |
| **8** | E_kin(t), 고무 3·5 | 구속이 커지면 두 MC 의 에너지 감소가 같아지고, 반등은 MC-strain 이 더 큼 |
| **9** | 겹침 δ(t), 고무 3·5 | Fig 7 과 같은 서열 재확인 (재료 독립) |
| **10** | **해석해 vs MC-stress**, Force 0–0.45 N vs δ 0–0.003 m (5입자 정사각 격자) | ⚠ **구현 검증**(코드 = 식)이지 **물리 검증이 아니다**. 논문은 "accuracy of the model"까지 주장 — over-claim |
| **11** ★★ | 514 하이드로겔 **압축-감압** 응력-변형, (a) β,γ=1 (b) β=1.65, γ=1.12. 0–600 Pa × 0–13.4 % | **고전 DEM 이 실험의 44 %** (245/555). 보정 후 MC-stress 가 실험 위에 겹침 |
| **12** | 접촉력망(force chain) — (a) 초기 배치 (b) 최대변형 @ classical Hertz. 색 = |f_n| | 정성 |
| **13** | 최대변형 접촉력망 — (a) MC-strain γ=1.12 (b) MC-stress β=1.65 | ⚠ **정량 없음**(힘 PDF·fabric 텐서·이방성 없음) = 미시역학 비교가 **눈으로만** |
| **14** ★★★ | **1921 이봉 하이드로겔** 응력-변형, **β·γ 재보정 없이 전이**. 0–450 Pa × 0–10.2 % | **논문 유일의 진짜 예측 시험**. MC-stress ≈ 실험(끝점), 중간구간 −10~15 %. classical 은 2.2× 과소 |
| **15** | 514 고무 압축+감압, 0–300 kPa × 0–28 % | ⚠ **Experiment 곡선이 없다** — "고하중 검증"으로 인용 금지 |
| **16** ★★ | **17 유리 구슬**, 0–60 MPa(곡선 ~45) × 0–2.64 %. 저자 자체 실험 | **우리에게 유일하게 전이 가능한 강성 케이스.** classical 이 **작은 변형에서부터** 어긋남. 단 β=5.17 은 **이 데이터에 fit** |
| **Table 1** | 재료 파라미터 3종 | §3.1 |
| **Table 2** | 계산시간 | §3.4 |
| **Appendix** | **2-pass pseudo-code** (본 카드 §4.5 에 전사) | ★ **이식 스펙 그 자체** |

## 6. Post-processing ★

- **무엇을 계산했나**: 벽 반력/단면적 → 공학 응력, 공학 변형률(변위 제어) → **응력-변형 곡선**; 운동에너지 시계열;
  중앙입자 **겹침 시계열**; **접촉력망 시각화**(선 색 = |f_n|); 정사각 격자 **해석해**(eq 11); **벽시계 시간**.
- **도구**: LIGGGHTS(시뮬), gnuplot 계열 플롯(추정 — 명시 없음), 시각화 도구 미기재.
- ★★ **계산하지 않은 것 (프레임[5] 판정에 결정적)**:
  **porosity·상대밀도 0 · 배위수 0 · tortuosity 0 · 힘 분포 PDF 0 · fabric/이방성 0 · Heckel 0 ·
  σ_ionic/σ_e/σ_thermal 0 · 형상·morphology 0 · 변형장 0.**
  ⇒ 이 논문은 **역학 절반조차 소유하지 않는다 — 소유하는 것은 "접촉 힘-변위 법칙" 한 칸뿐**이다.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` · `contact_models_layer_map.md` · `elasto_plastic_feasibility.md`

### 7-1. 층위 판정 — **① 접촉 힘-변위 LAW**, 그 안의 **non-binary 축**

| 층위 (`elasto_plastic_feasibility.md §0`) | 이 논문 | 근거 |
|---|---|---|
| **(1) 접촉 힘-변위 LAW** | ✅ **여기** — 단 **탄성 non-binary** 확장 | eq 10 이 f_n 을 바꾼다 |
| (2) 접촉 AREA 소성 | ✗ | `A_ij = πr_ijδ` 는 **탄성 Hertz 면적**이고, 힘식의 계수로만 쓰인다. 전달·소성 면적 산출 없음 |
| (3) 입자 SHAPE 소성 | ✗ | 구는 끝까지 구 |
| **항복캡(p_y/H)** | ✗ **없음** | 기반이 순수 Hertz. **"elasto-plastic" 이라는 단어가 논문에 없다** |

⚠⚠ **multi-contact 는 항복캡이 아니다.** 이 둘은 **같은 층(①)의 서로 다른 두 축**이다:

```
층위 ① 접촉 힘-변위 LAW
 ├─ 축 A: 탄성 ─→ 탄소성(항복캡)        Hertz | Luding-hysteresis(캡 없음, =우리) | Thornton–Ning(p_y) | So(H)
 └─ 축 B: binary ─→ non-binary          Hertz·Luding·TN 전부 binary | Gonzalez–Cuitiño | Brodu(MC-strain) | **Giannis(MC-stress)**
```
⇒ **`contact_models_layer_map.md §1` 에 축 B 행 추가 제안.** Varkey 2026 = **A(TN) × B(MC-stress) 동시 적용**의 유일 사례.

### 7-2. ★ 우리 접촉법칙 위에 그대로 얹을 수 있나 (사용자 질문 (가)) — **수식 수준 판정**

**결론: 수학적으로는 그대로 얹힌다. 물리적으로는 네 개의 가드가 필요하다.**

보정항 `(β ν A_ij) P_ij` 는 **기반 법칙의 함수형을 참조하지 않는다.** 필요한 입력은 (i) δ (→ A_ij), (ii) 그 스텝의 접촉력
(→ tr σ), (iii) ν, (iv) β 뿐이다. 우리 `hooke/hysteresis` 에 넣으면:
```
f_n = f^hys(δ, δ_max ; k₁, k₂(δ_max), k_c, φ_f)  +  γ₀·v_n  +  β·ν·A_ij·P_ij
                    └── Luding 2008 eq 6 (우리 m6/m7/m8) ──┘   └── Giannis eq 10 둘째 항 ──┘
```
- ★ **구성요소는 이미 LIGGGHTS 에 있다**: 입자별 `Σ l⊗f` 는 LAMMPS/LIGGGHTS 의 **`compute stress/atom`** 그 자체다
  (per-atom virial). 쌍 기여를 `½(r_i−r_j)⊗F_ij` 로 양쪽에 나눠 담으므로 **branch vector = 중심→접촉점(≈a) 규약과 일치**
  (§4.4 의 k = 0.25/0.5 가지). ⚠ 단 `stress/atom` 은 **V_p 로 나누지 않고**(압력×부피 단위), **부호 규약이 통상 응력의
  음(−)** 이다 → 이식 시 두 가지 모두 확인 필요.
- ⚠ **가드 ① 이력(hysteresis) 충돌**: 우리 법칙은 경로의존(δ_max 기억)이라 **제하(unloading) 가지에서 힘이 급락**한다.
  거기에 양의 P 항을 더하면 총 힘이 **재하 가지 위로 올라가** 모델 자신의 `k₁ ≤ k₂ ≤ k̂₂` 서열을 깬다.
  Giannis 의 기반은 경로무관 Hertz 라 이 문제가 없다. → **보정을 재하 가지에만 적용하거나 f_n ≤ k̂₂-가지로 clamp** 필요.
- ⚠ **가드 ② 점착 가지**: 인장(f^hys = −k_c δ)에서 tr σ 가 음이 되면 보정항이 **인장을 증폭**한다. 논문에는 인장이 없다(k_c=0).
  → **δ₀ 아래(점착 분기)에서는 보정 OFF** 가 안전.
- ⚠ **가드 ③ 중복 계상**: Luding eq 8 의 `k₂(δ_max) = k₁ + (k̂₂−k₁)δ_max/δ*_max` **자체가 이미 겹침의존 강화 장치**다
  (우리 m6 `maxElasticStiffness`, m8 `plasticityDepth`). MC-stress 와 **부분적으로 같은 일을 한다** → 둘 다 켜면
  강화가 이중 계상된다. **한쪽을 재보정해야 한다.**
- ⚠ **가드 ④ Stage-E 와 분리**: `A_ij` 는 **역학용 탄성 면적**, Stage-E 면적은 **전달용 소성 면적**이다. 절대 섞지 말 것
  (섞으면 β 의 보정 의미가 바뀌고 σ 삼중항이 오염된다).

★ **그래서 MC-stress 가 우리에게 *새로* 주는 정보는 딱 하나다**: `ΔF/F ∝ C` — **배위수 의존 접촉강성**.
Hertz 도 hooke/hysteresis 도 **한 입자에 접촉이 몇 개인지 모른다.** 같은 겹침이라도 잘 구속된 입자의 접촉이 더 뻣뻣하다는
물리는 우리 모델에 **전혀 없다.** 우리 연구의 절반(Furnas dip·배위수·패킹)이 바로 C 축이므로, 이건 **패킹 → 역학 커플링**을
여는 유일한 문헌 장치다. ⇒ 이게 이 논문의 진짜 가치이지, "연화 대체"가 아니다.

### 7-3. ★★★ 세 처방 나란히 (사용자 요청 표) — **증상도 부호도 다르다**

| 처방 | 누구 | 무엇을 고치나 (증상) | 물리적 근거 | 자유변수 | **우리 침대에 대한 부호** |
|---|---|---|---|---|---|
| **E 18× 연화** (24 → 1.35 GPa) | **우리 DEM** | real E 로는 300 MPa 에서 **덜 압밀**(porosity 과대) | ✗ **경험적 lumping** (재배열·GB-slide·micro-fracture) | **1** (E_eff) — ⚠ **측정된 물성 자리를 덮어쓴다** | **침대를 무르게** → porosity ↓ |
| **경도 항복캡** | **So 2021/2022**, Thornton–Ning 1998 | 접촉이 **항복 없이 무한정 뻣뻣**해짐 | ✅ **국소 접촉압 ≤ H ≈ 3σ_y** (물성) | **0** — 단 LPSCl σ_y 밴드 0.05–0.30 GPa 자체가 **6× 폭** | **침대를 무르게** → porosity ↓ |
| **multi-contact 응력항** | **이 논문** (Varkey 가 채택) | 고변형에서 **힘 과소예측**(Hertz 가 too soft) | △ **Poisson 결합**(한 접촉의 정수압이 다른 접촉으로 전달) — 형태는 물리, **크기는 경험적** | **1** (β) **+ 미기재 규약 2개**(§4.4, 6× 모호) | ⚠ **침대를 뻣뻣하게** → **porosity ↑** |

⇒ ★★★ **정정**: `elasto_plastic_feasibility.md §1 경로 B` 와 `varkey2026 §7` 의 *"같은 증상(과강성) 다른 처방"* 은 **틀렸다.**
- 원전의 문장 그대로: *"The new multi-contact approach is able to provide a **higher force at a given displacement** than
  the classical DEM"* (§5 결론). Fig 7·9 도 **MC-stress 가 최대겹침을 가장 작게** 만든다.
- 우리 18× 연화는 **겹침을 늘리려는** 장치다. **두 처방은 반대 방향이다.**
- **올바른 짝짓기**: 항복캡(경로 A)은 치밀영역을 **과도하게 물러지게** 만들고(Varkey SI Fig S1: Thornton–Ning 단독이
  5 mm 에서 FEM 9.7 vs 5.7 × 10⁴ N 로 **과소**), **F_mc 는 바로 그것을 되돌리는 짝**이다.
  ⇒ **F_mc 는 연화의 경쟁자가 아니라 경로 A 의 파트너다.** Varkey 의 스택(TN + F_mc)이 이미 조립된 레시피.

### 7-4. ★★ 우리 침대에 대입하면 얼마인가 (우리 유도 — **논문 수치 아님**)

동일 구·배위수 C·접촉당 법선력 f·겹침 δ 가정으로 eq 9–11 을 풀면 **상대 강화**는 E 와 무관한 닫힌 형태가 된다:
```
ΔF/F  =  k · β · ν · C · (δ/d)          k = 정규화·branch-vector 규약 (§4.4)
        k = 0.25 (pseudo-code 1/6, l=a) | 0.5 (본문 1/3, l=a) | 1.0 (본문 1/3, l=d) | 1.5 (eq 11 문자 그대로)
```
검산: k=1.5, C=4 를 넣으면 논문 eq 11 의 `1 + 6βν(δ/d)` 와 정확히 일치 ✓ (구현 확인용).

**입력** — ν = 0.37(real LPSCl; **우리 DEM 입력 0.3 이면 전부 ×0.81**), C ≈ 6.5(우리 SE-SE 배위수 대역; Luding 6.19–7.16),
β = **1.65 … 5.17**(논문 전 범위; LPSCl 실측 **n/a**), δ/d = 우리 값.

| 우리 침대 | δ/d | **ΔF/F 범위** | 힘 배율 | 같은 압력에서 **겹침 배율** | **필요 연화가 18× → 얼마로** |
|---|---|---|---|---|---|
| **pure-SE**(SE 하중지지, Cronau ⟨δ⟩ ≈ 11 % of d) | 0.11 | **+11 % … +205 %** | ×1.11 … ×3.05 | ×0.93 … ×0.48 | **20× … 55×** |
| **production 복합**(AM 차폐, ⟨δ⟩ = 1.75 %) | 0.0175 | **+2 % … +33 %** | ×1.02 … ×1.33 | ×0.99 … ×0.83 | **18× … 24×** |

★★★ **판정 (우리에게 불리한 쪽 그대로)**:
1. **MC-stress 를 지금 우리 LIGGGHTS 에 넣으면 연화가 줄지 않고 늘어난다** — 18× → 20–55×(pure-SE) / 18–24×(복합).
   *경로 B 는 18× 연화를 제거하지 못한다. 반대로 악화시킨다.*
2. **크기가 애초에 부족하다.** 힘 축에서 최대 3.05× vs 연화 18× (log 로 39 %), 겹침 축에서 최대 ÷2.1 vs ×6.87 (log 로 24 %).
3. **우리 production 복합에서는 사실상 무시할 수준(+2 … +33 %)** — AM 골격이 SE 를 차폐해 ⟨δ⟩ 가 작기 때문(우리 AM-shielding
   결과와 자기일관). ⇒ **복합 양극에 대해서는 이 보정을 도입할 동기가 거의 없다.**
4. 단 **pure-SE separator/펠릿**(SE 가 하중을 다 받는 케이스)에서는 +11 … +205 % 로 **무시할 수 없다.**
   ⇒ 도입한다면 **separator·pure-SE 쪽이 먼저**다.
5. ⚠ **β_LPSCl 는 측정되지 않았다.** 위 범위는 논문의 하이드로겔–유리 전 범위를 그대로 쓴 것이다.
   §4.6 의 β·ν ≈ 0.8–1.24 가설을 쓰면 β_LPSCl ≈ 2.1–3.4 로 좁혀지고, 그때 pure-SE ΔF/F ≈ +14 … +135 % 다.

### 7-5. 항목별 대조표

| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| 코드 | **LIGGGHTS** | **LIGGGHTS** | ✅ **같음** — Varkey(Rocky)와 달리 이식 경로가 직결 |
| 기반 법선법칙 | Hertz + 점성 (eq 3) | **hooke/hysteresis**(Luding eq 6, 캡 없음) | 우리 쪽이 **이력·점착·영구겹침을 더 갖는다**. 보정항은 법칙-무관이라 얹힘(§7-2) |
| 접촉 결합 | **non-binary** (입자 응력 trace) | **binary** | ⚠ **우리에게 없는 축.** ΔF/F ∝ C = 배위수 의존 강성 |
| 항복캡 | ✗ | ✗ | **둘 다 없다** — 우리가 18× 연화로, 논문은 β 로 각각 다르게 메운다 |
| 소성 | **전무**(순수 탄성) | CONTACT 소성 프록시(δ₀)+Stage-E 면적 / MPM 진짜 형상소성 | **우리가 두 층 더 갖는다** |
| E 취급 | **real E 유지** (23.3 kPa / 1.85 MPa / 65 GPa) | **E 를 18× 낮춤** | ★ 그들은 물성을 안 건드리고 **보정항을 격리**했다 — 구조적으로 더 깨끗 |
| 자유변수 | **β 1개** + 미기재 규약 2개 | **E_eff 1개** (+Stage-E 계열) | **개수는 같다.** 차이는 **어디에 놓느냐** (§7-6) |
| 보정 앵커 | 실험 응력-변형 끝점 | Minnmann pure-SE porosity ~10 % @300 MPa | 다른 관측량 |
| 압력 범위 | **최대 45 MPa**(유리) | **300 MPa** | **6.7× 밖** |
| 변형 범위 | ε 2.64 / 10.2 / 13.4 / 28 % | ε ≈ 24 %(porosity 36→15.6 %) | ✅ **변형 축은 안에 든다**(고무 28 %) |
| 접촉 겹침 | 단일 구 δ/r 40 % 까지 보정 | pure-SE δ/r ≈ 22 %, 복합 δ/r ≈ 3.5 % | ✅ **겹침 축도 안에 든다** |
| porosity/상대밀도 | **보고 0** | 우리 핵심 관측량 | ⚠ **porosity 축으로 전이 불가** |
| 전달 σ | **0** | σ_ionic + σ_e + σ_thermal 삼중항 | frame[5] 전달 절반 전부 우리 것 |
| 형상 / morphology / 변형장 | **0** | MPM 고유 | 저자들이 §1 에서 **MPM 을 "형상은 되지만 입자 수에서 비용이 막는다"** 고 직접 적음 ⇒ frame[5] 외부 확증 |
| 소재 | 하이드로겔·고무·유리 | LPSCl + NMC811 | **배터리 아님.** 전이는 **유리(E 65 GPa)만** 부분적으로 |
| 검증 | 실험 4건(1건은 저자 자체) + FEM **없음** | Minnmann·Cronau·Bazzoun 앵커 | 그들 유일 blind 전이 = Fig 14 |

### 7-6. 정직한 fudge 대 fudge 판정 (사용자 질문 2)

**질문: β 는 물성에서 유도되는가, 아니면 이쪽도 fudge 인가? → 논문 상태로는 fudge 다.** 본문 문장 그대로
*"an **adjustable dimensionless empirical** geometric prefactor"*, 결론 *"we included a prefactor β which must be
**carefully calibrated depending on the type of the material**"*, outlook *"For calibration, it would be interesting to
provide these parameters **by detailed finite element simulations**"* ⇒ **저자 스스로 유도되지 않았음을 인정**한다.

그러나 **같은 fudge 라도 구조가 다르다** — 이건 우리에게 유리한 방향이 아니라 **그들에게 유리한** 방향이다:

| 축 | 우리 E_eff = 1.35 GPa | 그들 β |
|---|---|---|
| 개수 | 1 | 1 (+ 미기재 규약 2개) |
| 위치 | ⚠ **측정된 물성(E)의 자리를 덮어쓴다** | ✅ **별도 항** — E·ν 는 실측값 그대로 |
| 오염 범위 | ⚠ **E 를 쓰는 모든 하위 계산**(Hertz 접촉반경·k_n·k_t·파속·timestep·Stage-E 입력)이 함께 오염 | ✅ **그 한 항 안에 격리**. δ→0 또는 ν→0 이면 **자동 소멸** |
| 물리적 소멸조건 | 없음 | ✅ ν=0 이면 모델 OFF (물성 게이트) |
| 보편성 | 케이스별 재보정 | △ **β·ν ≈ 0.8** 이 준보편일 가능성(§4.6, 미검증) |

⇒ **정직한 결론**: *"multi-contact 는 우리 연화보다 물리적이다"* 는 **절반만 맞다.** 크기(β)는 똑같이 보정이지만,
**보정을 물성 자리에서 빼내 격리한 것은 구조적으로 우리보다 낫다.** 우리 18× 연화의 진짜 약점은 "경험적"이라는 것보다
**"E 라는 측정 가능한 물성을 덮어써서 하위 계산 전체를 오염시킨다"** 는 데 있다.
이 약점을 없애는 것은 **경로 A(항복캡, 자유변수 0, real E 유지)** 이지 경로 B 가 아니다.

### 7-7. MC-strain vs MC-stress (사용자 질문 4)

| | **MC-strain** (Brodu, Dijksman, Behringer, PRE 91 (2015) 032201) | **MC-stress** (이 논문) |
|---|---|---|
| 무엇을 더하나 | **겹침** δ_{k→c} (eq 7–8) | **힘** (βνA)P (eq 10) |
| 필요 기하 | 접촉 **쌍**의 상대 방위 d_kc·n_k·n_c·u_kc = **O(C²)** | 입자 하나의 **trace(스칼라)** = **O(C)** |
| 반복 | **원리적으로 iterative**; 준정적 가정으로 1회. **빠른 압축·큰 변형에서는 반복 불가피, 안 하면 가속도 폭주 → 불안정** | **반복 없음** (2-pass 확정) |
| prefactor 이론앵커 | ✅ γ=0.5(ν→0.5), γ=1(ν→0) — **고무는 맞고 유리는 6× 벗어남** | ✗ 없음 |
| 방향성 | 방향 정보 보존(변위장이 텐서적) | ⚠ **등방 성분만** (trace) — 저자도 "anisotropic deformation 을 설명할 수 있다"고 쓰지만 실제로 쓰는 건 **정수압 스칼라 하나** |
| 실측 속도 | 17.6–18.7× classical | **5.7–6.4× classical** (2.9–3.1× 더 빠름) |
| 최대겹침 | **증가**(겹침을 더하니까) | **감소**(저항을 더하니까) |
| 정확도(Fig 11b/14/16) | 대체로 MC-stress 보다 약간 아래 | 약간 위 (유리에서 "slightly better") |

⇒ 저자 주장 *"MC-stress 가 더 낫다"* 의 실체 = **속도 ~3× + 반복 제거 + 안정성**. **정확도 우위는 근소하고 fit 후 비교다.**
⚠ 그리고 **trace 만 쓰므로 이방성을 못 담는다** — §3.2 의 "anisotropic deformation can be accounted for" 는 **과한 표현**이다
(방위 정보는 A_ij 와 접촉별 δ 에만 남는다).

---

## 8. 적용 인사이트 (우리 연구에 어떻게)

- ① ★★★ **`elasto_plastic_feasibility.md` §1 경로 B 서술을 부호까지 고쳐 쓸 것.** F_mc 는 "치밀영역 과강성"을 고치는
  장치가 **아니다**. 고치는 것은 **under-stiffness**(힘 과소예측)이고, 우리 침대에서는 **연화를 18× → 20–55× 로 늘린다**.
  ⇒ **경로 B 의 위치를 "연화 대체 후보"에서 "경로 A 채택 시 필요한 짝"으로 재분류.** (§7-3, §7-4)
- ② ★★ **경로 A 우선순위가 강화된다.** 세 처방 중 **부호가 맞고 자유변수가 0인 것은 항복캡뿐**이다.
  경로 A 를 먼저 넣고, 그 다음 **치밀영역에서 under-stiff 가 나타나면** 그때 F_mc 를 얹는다(Varkey 스택 재현).
- ③ ★★ **배위수 의존 접촉강성 = 우리에게 없는 축.** `ΔF/F ∝ C` 는 **패킹 → 역학 커플링**이다. 우리는 C 를 전달
  (σ_ionic ∝ CN²)에는 쓰지만 **역학에는 전혀 안 쓴다**. ⇒ 새 예측: MC-stress 를 켜면 **SE-rich(고 C) 침대가 AM-rich 보다
  더 뻣뻣해져 Furnas dip 의 SE-rich 쪽 flank 가 올라간다.** 우리 dip 이 순수 기하라는 판정(frame[3])에 대한 **직교 시험**.
- ④ ★ **β·ν ≈ 0.8 가설을 우리가 검증할 수 있다.** 논문은 4점밖에 없고 C 를 보고하지 않았다. 우리는 침대의 C 를 정확히
  알고 있으므로, `ΔF/F = kβνC(δ/d)` 를 우리 침대에 걸고 **β 를 C-보정해 재추출**하면 논문이 못 한 분리를 할 수 있다.
  → 성공하면 **"β 는 자유변수가 아니다"** 는 결과이고, 그건 **원저자보다 앞선 기여**다.
- ⑤ ★ **이식 스펙이 이미 손에 있다**: §4.5 pseudo-code + LIGGGHTS `compute stress/atom`(= Σl⊗f 이미 존재) +
  LIGGGHTS-PUBLIC 의 MC-DEM 예제[49]. 비용 견적 = **classical 대비 5.7–6.4×**(514 입자 기준) ⇒ 우리 36k–73k 입자
  침대에서는 **실질적 부담**. 먼저 pure-SE separator 소형 침대에서 시험할 것.
- ⑥ ★ **"Hertz 는 δ/r ≤ 10 % 까지"** 라는 stated 문장은 우리 문서에 바로 쓸 수 있는 인용이다.
  우리 pure-SE 는 δ/r ≈ 22 % 로 **그 한계 밖에서 Hertz 계열 법칙을 쓰고 있다** — 18× 연화의 정당화가 아니라
  **"우리가 어느 영역에 있는지"의 문헌 좌표**로 쓸 것.
- ⑦ ★ **frame[5] 외부 확증 한 줄 추가**: 저자들이 §1 에서 MPM·MPFEM·FEM-DEM 을 *"단일 입자의 이방성 변형과 변형 후
  임의 형상을 다룰 수 있는 방법 — 그러나 계산비용이 많은 입자 수에서 사용을 막는다"* 라고 정리했다.
  ⇒ **우리 접촉법칙의 저자(Luding)가 공저한 논문이 "형상은 MPM, 규모는 DEM"을 명시**한 것 = 우리 분업의 외부 근거.

## 9. 인용 가능 문장 (deck/paper 용)

- "The multi-contact correction of Giannis et al. (Granular Matter 23:17, 2021) — the origin of the `F_mc` term used by
  Varkey et al. (2026) — **adds** force at a given overlap (`f_n += β ν A_ij P_ij`, with `P_ij` the mean trace of the two
  particle stress tensors). It therefore acts in the **opposite direction** to our 18× modulus softening: applied to our
  bed it would *increase*, not remove, the required softening."
- "Its single prefactor β is, in the authors' own words, an *adjustable dimensionless empirical geometric prefactor* that
  *must be carefully calibrated depending on the type of the material*; the authors defer its derivation to future FEM
  work. The multi-contact route is therefore **not** a parameter-free replacement for an empirical modulus — the honest
  difference is that β is an isolated additive term while our E_eff overwrites a measured material property."
- "Giannis et al. state that Hertz theory is applicable only up to δ/r ≤ 0.1; our pure-SE contacts sit at δ/r ≈ 0.22,
  i.e. outside the classical binary-Hertz range — which is the literature coordinate of the regime our effective-modulus
  softening is compensating for."
- "The same group that defines our LIGGGHTS `hooke/hysteresis` contact law (Luding, co-author) classifies MPM/MPFEM as the
  methods able to represent anisotropic single-particle deformation and arbitrary deformed shapes, but notes their cost
  prevents use with large particle numbers — an external statement of the DEM(scale)/MPM(shape) division of labour."
- (우리 재분석, 표기 필수) "Re-expressed as the product βν — the only combination that enters the force law — the four
  calibrations of Giannis et al. cluster at 0.79 / 0.80 / 0.83 / 1.24 across a 2.8 × 10⁶-fold span in Young's modulus,
  suggesting the prefactor may be closer to a material-independent constant than the paper claims. **This is our
  re-analysis, not the authors' claim**, and it cannot be separated from the unreported coordination number."

## 10. 주의 / 한계 (over-claim 방지)

**논문 자신의 한계 (저자 명시)**
- **β 는 재료마다 보정해야 한다** (결론 §5). 유도 안 됨. FEM 기반 유도는 **outlook**.
- **고응력 탄소성은 이 모델에 없다** — outlook: *"one can think of investigating the dependence of the model parameters on
  … the **elasto-plastic behaviour at high stress levels**"*. ⇒ **우리 300 MPa 영역은 저자들이 명시적으로 미래로 미룬 곳.**
- 유리 케이스는 *"since glass beads are brittle, **the elastic part is the only focus here**"* ⇒ **탄성 영역만 검증됐다.**
- MC-strain 은 빠른 압축·큰 변형에서 불안정(반복 필요). MC-stress 는 "더 안정할 것으로 기대한다(expected)" — **증명 아님**.
- 더 다양한 재료로 실험을 넓혀야 한다고 스스로 적음.

**우리가 추가로 다는 한계**
- ⚠ **적용 상대밀도 한계가 논문에 없다.** porosity·상대밀도·배위수를 **한 번도 보고하지 않았다.**
  "ρ > 0.7 에서만 유효"는 **Varkey 2026 의 서술이지 Giannis 의 것이 아니다** — 이 카드로 그 출처를 분리한다.
- ⚠ **정규화가 세 곳에서 다르다**(본문 1/3 · pseudo-code 1/6 · eq 11) + branch vector 미정의 ⇒ **β 전이 시 최대 6× 오차**.
  Varkey 가 **β = 0.5** 를 쓴 것도 Giannis 의 1.65–5.17 과 크게 다른데, **어느 정규화인지 확인 없이 두 값을 비교하지 말 것.**
- ⚠ **Fig 10 "해석해 검증"은 구현 검증**(코드=식)이다. 논문의 *"validates … also the accuracy of the model"* 은 over-claim —
  같은 식을 손으로 푼 것과 코드가 맞는다는 뜻일 뿐 물리와 맞는다는 뜻이 아니다.
- ⚠ **"고응력에서 강한 비선형을 잡는다"(초록)의 실증 기반이 얇다**: 고하중 케이스는 (i) 고무 침대 28 % — **실험 없음**,
  (ii) 유리 45 MPa — **β 를 그 데이터에 맞춘 것**. **독립(blind) 검증은 Fig 14 이봉 하이드로겔 1건뿐**이고 그건 450 Pa 이다.
- ⚠ **모든 결과 수치는 digitized** (본문에 표로 준 것은 Table 1 물성과 Table 2 시간뿐) → **추세만**, 절대값 인용 금지.
- ⚠ **소재가 배터리가 아니다.** LPSCl 로 전이 가능한 것은 (a) **형식(식)**, (b) **유리(E 65 GPa)의 정성 추세**,
  (c) β·ν 밴드(가설) 뿐. **porosity·σ·응력 절대값은 전이 불가.**
- ⚠ **1921 침대의 이봉 크기비 1.31 은 Furnas 영역이 아니다** (우리 12:4:1 과 비교 금지).
- ⚠ **앙상블/시드 없음** — 케이스당 1회 실현으로 보인다. 산포 미보고.
- ⚠ **계산시간에 하드웨어·코어수 없음** → 표 내부 배율만.
- ⚠ **논문 내부 불일치 2건**: ρ_hydrogel = 11.5 kg/m³ (t_c 검산으론 자기일관이나 물리적으로 이상) · Fig 6–9 시간축 라벨
  `[µs]` 가 t_c=1800 µs 와 모순(ms 여야 함).
- ⚠ **"2입자 상호작용에서는 multi-contact 가 classical 과 차이가 없다"(§3.4)** 는 **eq 10 과 pseudo-code 어디에도 근거가 없다**
  (C^P>1 게이트가 없고, 접촉 1개여도 tr σ ≠ 0). 실제로 §3.3 의 단일 구 + 2 평판(접촉 2개)은 β=1.71 로 명백히 달라진다.
  **저자 진술이 도출되지 않는다.**

---

## 11. 기술 미니 용어집 (이 카드를 혼자 읽기 위한)

- **binary / non-binary 접촉**: 고전 DEM 은 접촉 하나의 힘을 그 쌍의 δ 만으로 정한다(binary). non-binary(= multi-contact,
  nonlocal)는 **같은 입자의 다른 접촉들이 이 접촉의 힘을 바꾼다**. 물리적 이유: 실제 입자는 한 곳이 눌리면 전체가 변형·
  가압되어 다른 접촉면까지 밀어낸다(Poisson 결합).
- **branch vector `l^c`**: 응력 텐서를 만들 때 쓰는 지레팔 벡터. **입자 중심 → 접촉점**(입자 응력 표준) 또는
  **중심 → 중심**(쌍 응력, Love–Weber). 둘은 접촉 구에서 **2배** 차이. 이 논문은 명시하지 않는다.
- **`tr σ` (응력 trace)**: σ_xx+σ_yy+σ_zz. 3으로 나누면 **정수압(평균 수직응력)**. 방향 정보가 없는 **스칼라**.
- **P_ij**: 이 논문에서 접촉쌍이 느끼는 대표 압력. 정의가 세 번 다르다(§4.4).
- **`A_ij = π r_ij δ`**: Hertz 접촉면적. 접촉반경 `a = √(R*δ)` 의 원 면적 πa². **탄성 면적**이며 우리 Stage-E 의
  소성 면적(Tabor/volume cap)과 **다른 물건**.
- **`E*`, `G*`**: 두 입자의 탄성을 합친 유효 계수. `1/E* = (1−ν_i²)/E_i + (1−ν_j²)/E_j`.
- **`r_ij = r_i r_j/(r_i+r_j)`**: 환산반경 (구-구). 같은 구면 `r/2 = d/4`.
- **`t_c` 접촉지속시간**: Hertz 충돌의 특성시간. `Δt ≪ t_c` 여야 적분이 안전 — DEM timestep 상한의 근거.
- **공학변형률(engineering strain)** 프로토콜: 벽을 정해진 변위로 밀고 반력을 읽는다(변위 제어).
  ↔ 우리 300 MPa **정압 servo**(응력 제어). **같은 곡선을 다른 축으로 읽는 것이라 BC 가 다르다.**
- **MC-strain / MC-stress**: 각각 변위장 기반 / 응력 기반 multi-contact. 이 논문이 붙인 이름.
- **prefactor γ / β**: MC-strain / MC-stress 의 유일한 자유 계수. γ 는 ν 극한에서 이론값이 있고, β 는 없다.
- **Tatara 1989 [46]**: 큰 변형 탄성 구의 힘-접근 관계 실험/이론. Fig 4 실험 곡선의 출처.
- **Brodu 2015 [23] / Barés 2020 [50]**: 하이드로겔 구 패킹의 광탄성 3D 실험 데이터 공개 논문. Fig 11 / Fig 14 실험 출처.
- **Gonzalez–Cuitiño [24] · Frenning [25] · Celigueta [26] · GEM(Karanjgaokar) [27]**: 접촉 의존성을 다룬 선행 4계열.
  Frenning 은 **truncated sphere + 법선응력 합 × 접촉면적**(이 논문과 가장 가까운 stress-based 선행),
  Celigueta 는 **고려 접촉에 수직인 접촉만** 결합, GEM 은 **다목적 최적화**로 입자간 힘을 역산.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

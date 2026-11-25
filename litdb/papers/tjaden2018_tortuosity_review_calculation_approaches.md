<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 기준 = taufactor_tortuosity_factor_tomography_tool.md.
     이 논문은 물리 모델이 아니라 *정의·계산법 리뷰* 다 → §4 = 리뷰 구조 정독, §7 뒤에
     "§ tortuosity 정의 대조표" · "§ 우리 τ 이름 권고" 를 둔다 (이 카드의 본업 = 우리 τ 열 이름의 명명 정본).
     쪽 표기 = 학술지 쪽 (PDF n쪽 = 학술지 46+n쪽). 식 번호 = 원문 번호.
     수식·표는 원문 PDF 를 그림으로 렌더해 대조했다 (텍스트 추출은 τ→t, ε→1, κ→k 로 깨뜨린다). -->
# Tortuosity in electrochemical devices: a review of calculation approaches — τ·κ(=τ²)·N_M·Bruggeman 정의와 기하/flux/실험/상관식 계산법 분류 (우리 τ 명명 정본) — Tjaden (Int. Mater. Rev. 2018)

> slug `tjaden2018_tortuosity_review_calculation_approaches` · DOI `10.1080/09506608.2016.1249995` · type `review (tortuosity 정의·계산법 — geometric vs flux-based · porosity–tortuosity · microstructure)` · PDF `2. Tortuosity in electrochemical devices a review of calculation approaches.pdf` · digested `2026-10-02` · status ✅
>
> ★ **이 카드의 역할 = 우리 tortuosity 열 이름의 명명 정본.** 리뷰의 명명: **τ = tortuosity** (식 1 = 최단경로 길이 ÷ 끝점 거리) · **κ = τ² = tortuosity factor** (식 2, Epstein [11]) · **D_eff = (ε/κ)·D_bulk** (식 3, "이온·전자 전도에도 유효") · **ε/τ² = diffusibility / effective relative diffusivity** · **N_M = σ_bulk/σ_eff = τ²/ε** (식 5, MacMullin) · **τ² = γ·ε^(1−α), 표준 α = 1.5** (식 6·8, Bruggeman). 계산법은 **geometric-based** (최단경로: FMM · 거리전파 · pore centroid) 와 **flux-based** (voxel: Laplace · LBM · random walk / mesh: FEM·CFD 열유속) 로 가르고, **같은 시료에서 flux 값이 기하 값보다 높다** (p.61–62).
>
> ★ **판정 요약**: 우리 **τ_Lap,eff = √(φ_SE·σ_grain/σ_full) = 리뷰 식 3 의 τ (= √κ, flux 기반)** · **τ_Dij · τ_Dij,all · 벽 τ = 리뷰의 geometric τ** (식 1 계열, SE 접촉 그래프 판) · **τ_Lap,geom 은 'geometric' 이 아니다** — Kirchhoff 해의 협착 0 (CONTACT_FREE) 가지라 이름이 리뷰 분류와 충돌한다. **COMSOL 의 τ_F (f = ε/τ_F) 는 리뷰의 κ (= τ², 인계 계획의 T)** 다 — 웹앱·COMSOL 내보내기가 "COMSOL input" 이라 적는 √ 값 (τ_Lap,eff) 과 거듭제곱이 다르다 (§ 대조표 D15).
>
> ⚠ 범위: SOFC · 액체 Li-ion · PEM · 산소수송막의 **기공상** τ 를 다룬다. 전고체 (SE 입자상) · 접촉저항 · 저항망 (RNM / pore-network) 계산법은 **나오지 않는다** (본문 전체 검색 확인 — 'network' 는 "complex porous networks" 와 Zamel [18] 의 기체 확산 저항망 문맥뿐).

---

## 1. 한 줄 요약
'Tortuosity' 라는 한 이름 아래 문헌은 (i) 최단경로 길이비 τ (기하, 식 1), (ii) 그 제곱 κ = τ² (tortuosity factor, 식 2–3 으로 유효 수송계수에서 역산), (iii) 묶음 양 ε/τ² (diffusibility) · τ²/ε (MacMullin N_M), (iv) Bruggeman 류 porosity 상관식 (식 6–8) 을 섞어 쓰고, 계산법 — **상관식 · 확산셀/전기화학 실험 · 3D 영상의 기하 알고리즘 · flux 알고리즘** — 에 따라 **같은 시료에서도 값이 체계적으로 다르다**: flux 기반이 기하 기반보다 높고 (p.61–62), Bruggeman 은 구형·균질 구조에서만 맞으며 (p.51, p.62), 실험 τ 는 그 실험 조건·모형의 적합 매개변수다 (p.54, p.62). 리뷰는 Epstein 의 κ/τ 구분을 채택해 문헌값을 환산하고 (p.48) 표 4·5 에 **τ² 와 τ 를 나란히** 싣는다. ⇒ 우리에게 주는 규칙: **τ 열 이름에 (거듭제곱 · 계산 계열 · 이산화) 를 함께 붙여야 한다** — 리뷰 자신도 기하 τ 와 √κ_flux 를 **같은 기호 τ** 로 쓰기 때문에, 리뷰 기호만 따라서는 혼동이 풀리지 않는다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (다룬 시료) | 연구유형 |
|---|---|---|---|---|
| **Bernhard Tjaden**, Dan J. L. Brett, **Paul R. Shearing** (교신) — Electrochemical Innovation Lab, Dept. of Chemical Engineering, University College London | **International Materials Reviews 63(2), 47–67 (2018)** | **10.1080/09506608.2016.1249995** | 소재 무관 리뷰. 예시 시료 = SOFC (Ni-YSZ 음극, LSCF·LSC/CGO 양극), Li-ion (LiCoO₂·LiFePO₄·LiMn₂O₄·graphite·MCMB 전극, PVdF·Celgard 분리막), PEM GDL (carbon paper), 산소수송막 YSZ 지지층. **전고체 없음** | **FULL CRITICAL REVIEW** (정의·계산법 리뷰, 참고문헌 159) |

- 접수 2016-07-04, 승인 2016-10-11 (DOI 는 2016 판, 권호는 2018). © 2016 The Author(s), Informa UK (Taylor & Francis), **CC BY 4.0 오픈액세스**.
- 키워드: Tortuosity; microstructure; diffusion; tomography; modelling.
- 연구비: EPSRC (EP/K005030/1, EP/M009394/1, EP/M014045/10), Royal Academy of Engineering, Praxair (B.T. 학생 지원). 사의: Donal Finegan, Samuel Cooper.
- 원본 위치: `litdb/inbox/tortuosity_20261003/` (21쪽). 그림 15장 = `litdb/figures/tjaden2018_tortuosity_review_calculation_approaches/` (Fig. 1–10, Table 1–5).
- 관련 정본 카드: **TauFactor** (`taufactor_tortuosity_factor_tomography_tool`) 는 이 리뷰의 참고문헌 [122] 이다. 같은 묶음 형제 카드 (같은 worktree 에서 동시 작성, 이 카드 작성 시점에 커밋 전): `landesfeind2016_tortuosity_eis_electrodes_separators` (리뷰 [24], inbox #5) · `nguyen2020_electrode_tortuosity_factor` (inbox #6 — 리뷰 이후의 'electrode tortuosity factor τ_e').

## 3. 핵심 수치 (이 리뷰가 주는 것)
> 이 리뷰는 소재 물성 앵커 (porosity@P · σ_ion/e/thermal · E_SE · coverage · Z · Heckel) 를 **주지 않는다** → 전부 n/a. 주는 것은 ① 정의식 (§ 대조표), ② 상관식 매개변수 모음 (Table 1), ③ 같은 시료에서 방법별 τ 차이 (Table 2–5), ④ 실험 τ 의 조건 의존 사례.
> 표기: **stated** = 원문 숫자 · **판독** = 그림에서 읽은 근사 (TREND only) · **우리 산술** = 원문 숫자로 우리가 계산한 값.

### 3-A. 본문 수치 (쪽 순)
| 항목 | 값 | 조건 / 시료 | 쪽 · 출처 | 구분 |
|---|---|---|---|---|
| Bruggeman 표준 지수 | **α = 1.5** (식 6) | 일반형 τ² = ε^(1−α) | p.49 | stated |
| Thorat [47] 적합 | 지수 **−0.53 ⇒ α = 1.53**, **γ = 1.8**; "tortuosities" 가 표준 Bruggeman 예측의 **거의 2 배** → γ 도입. 지수 −0.53 = 1 − α 이므로 그래프에 올린 양은 **τ²** 다 (원문은 'tortuosity values' 라고만 씀 — 우리 해석) | LiFePO₄·LiCoO₂ 양극 (AC impedance + polarisation-interrupt) | p.49 | stated (+ 해석) |
| Zacharias [53] | **γ = 2.5 / 2.6, α = 1.27 / 1.28** (조성 함수로 둠: graphite·carbon black·PVdF 건조 질량분율) | LiCoO₂ 전극 | p.50 | stated |
| Chung [56] | 16 개 **LiNi₁/₃Mn₁/₃Co₁/₃O₂** 전극 (조성비 변화, X-ray synchrotron) — 계산 τ 는 Bruggeman 보다 **"always slightly above"**; 합성 충전에서 **완전 정렬 입자 → Bruggeman 근접** | Fick 수송 시뮬레이션 | p.50 | stated |
| Tjaden [85] (확산셀) | CH₄–N₂ 상온: CH₄ 확산 기준 τ **≈ 2.3**, N₂ 기준 **≈ 2.5**; 온도↑ 시 전 기체쌍 평균 τ **2.36 → 2.73** | 산소수송막 YSZ 지지층 | p.52 | stated |
| Zamel [18] (Loschmidt) | 25 → 80 °C: D_bulk **≈ 0.2 → 0.275 cm² s⁻¹**, D_eff **≈ 0.05 → 0.075 cm² s⁻¹**, **ε/τ² 0.252 → 0.281 (+11.5 %)** (일정 ε 이면 τ 가 같은 정도로 감소) | O₂–N₂, carbon paper GDL | p.52–53 | stated |
| 상관식 vs 측정 | 모든 상관식 (Bruggeman 포함) 이 D_eff 를 **과대** = τ 를 **과소** 추정 | Zamel [18], Tjaden [85] | p.53 | stated |
| Jiang & Virkar [16] | 800 °C 평균 τ: **H₂–H₂O 2.23** (최저) · **H₂–CO₂–H₂O 2.73** (최고) | 한계전류 i_lim + Bosanquet 역산 | p.53 | stated |
| Brus [72] | 700·800 °C, **H₂ 2.5–90 % in N₂**; 실험 τ 는 H₂ 농도마다 다르고 RW 는 단일값; **저 H₂ (농도분극 큼) 에서만 RW 와 일치** | button SOFC + FIB-SEM 음극 | p.53–54 | stated |
| Brus [72] Fig. 4 | 실험 τ **≈ 2–3 (저 H₂) → ≈ 10–14 (90 % H₂)**, FIB-SEM (RW) **≈ 2** | 같은 시료 | p.54 | 판독 |
| Tsai & Schmidt [88] | 전극 **두께는 τ 에 영향 없음** (정상상태 기대대로) | SOFC 음극 | p.54 | stated |
| Bae [92] | 채널 간격 ≤ 전극 두께에서 τ 최저; 가장 촘촘한 채널 시료 **≈ 8 mAh cm⁻² @ 1C·2C** | co-extrusion LiCoO₂ | p.54 | stated |
| Chen-Wiegart [114] | 국소 기하 τ **1 – 2.5** (단면) | LiCoO₂ 양극 기공상, 거리전파 | p.56 | stated |
| Cooper [111] | pore centroid 가 두 상·두 온도 모두 **최저**, Bruggeman 에 근접; flux 계열은 서로 일치 (열유속 ~ RW 사이); 기공 평균 τ **≈ 1.21** (세 방향, 두 온도) | LSCF, 14 °C·695 °C, synchrotron nano CT | p.57 | stated (1.21 이 어느 방법의 평균인지 문장이 모호) |
| Grew [120] | 고체상 τ 가 기공상보다 **최소 1.2 배** | Ni-YSZ 음극, Laplace | p.58 | stated |
| Iwai [103] RW | walker **100,000**, time step **10,000,000** | Table 2 의 정확도 확보 | p.59 | stated |
| Joos [147] RVE | 시료 1·3: **l_cat > 10 µm** 에서 평탄; 시료 2 LSCF 는 **거의 2 배** 두께 필요 | LSCF SOFC 양극, ParCell3D | p.59–60 | stated |
| Cooper [63] | **8.8 µm** 정육면체, adaptive polyhedral mesh, StarCCM+ 열유속, **8 개** 비중첩 부분부피 → 식 21·22 | LiFePO₄ 양극, synchrotron nano CT | p.60 | stated |
| Kehrwald [51] | 12 개 부분부피 (StarCD, Fick): 국소 τ **3 배** 차 | Li-ion 복합 전극 | p.60 | stated |
| Shearing [106] | 픽셀 **597 / 65 nm**, 부피 **10,434,731 / 75,164 µm³**, ε **36.3 / 38.0 %**, 기하 τ (pore centroid) **2.0 / 1.9**, 비표면적 **0.6 / 1.3 µm² µm⁻³** (×2 이상) | 같은 상용 Li-ion 양극, micro vs nano CT | p.61 | stated |
| Wilson [102] vs Iwai [103] | 같은 형 시료·같은 영상법·비슷한 픽셀 — Iwai 부피가 **9 배** 커도 τ **차이 없음** | Ni-YSZ 음극 | p.62 | stated (부피비 972.4/105.2 = 9.24 — 우리 산술) |
| Izzo [81] vs Wilson [102] | Izzo τ 가 더 높은데 기공률이 **1.5 배** 높다 → "τ 만으로는 미세구조 전체를 못 본다" | Ni-YSZ 음극 | p.62 | stated (0.300/0.195 = 1.54 — 우리 산술) |
| σ_ion · σ_e · κ_th · porosity@P · E_SE · coverage · Z · Heckel | **n/a** | — | — | 리뷰는 소재 물성을 내지 않는다 |

### 3-B. Table 1 — Bruggeman 지수 α · 척도 γ 모음 (p.50, 식 8 의 τ² = γ·ε^(1−α))
| 시료 | γ | α | 출처 | κ(ε=1) = γ (우리 산술) |
|---|---|---|---|---|
| Battery electrode LiMn₂O₄ | 1 | 3.3 | Doyle [48] | 1 |
| Battery separator PVdF | 1 | 4.5 | Doyle [48] | 1 |
| Battery separator PVdF | 1 | 2.4 | Arora [32] | 1 |
| Battery electrode MCMB 2528 and LiMn₂O₄ | 1 | 5.2 | Arora [32] | 1 |
| Battery electrode LiFePO₄ and LiCoO₂ | 1.8 | 1.53 | Thorat [47] | 1.8 (ε=1 에서 τ≠1) |
| Battery graphite electrode | 0.115 | 3.2111 | Kehrwald [51] | 0.115 (κ<1 ⇔ ε > 0.376) |
| Battery graphite electrode | 0.1146 | 3.159 | Kehrwald [51] | 0.115 |
| Battery electrode LiCoO₂ | 2.5 | 1.27 | Zacharias [53] | 2.5 |
| Battery electrode LiCoO₂ | 2.6 | 1.28 | Zacharias [53] | 2.6 |
| Battery separator Celgard 2400 | 0.667 | 2.43 | Cannarella [52] | 0.667 |
| Battery separator Celgard 3501 | 0.58 | 3.33 | Cannarella [52] | 0.58 |
| Battery separator GMB 500 mAh | 1.77 | 1.77 | Cannarella [52] | 1.77 |

- 리뷰 판정 (p.50): "even for this small class of materials, values for α and γ differ significantly" — 일부는 고공극률로 외삽하면 **τ < 1** (정의 위반), **ε = 100 % 에서 τ = 1** 을 못 지키는 것도 있다 → "usefulness 에 의문", α·γ 해석은 조심.
- 우리 산술: Kehrwald 두 행은 κ = 1 을 **ε ≈ 0.376** 에서 이미 넘어선다 (고공극률만의 문제가 아님). 원 논문의 적합 형식·환산 여부는 [미확인].

### 3-C. Table 2 · Table 3 — 같은 시료, 다른 flux 알고리즘 (p.59)
| Table | 시료 · 상 | 축 | 방법 A | 방법 B | 차 (우리 산술) |
|---|---|---|---|---|---|
| 2 (Iwai [103]) | SOFC 음극 · **기공** | x / y / z | RW 1.43 / 1.41 / 1.33 | LBM 1.42 / 1.44 / 1.35 | ≤ 0.03 |
| 2 | · **Ni** | x / y / z | RW 4.70 / 5.43 / 2.63 | LBM 4.66 / 5.43 / 2.63 | ≤ 0.04 |
| 2 | · **YSZ** | x / y / z | RW 5.28 / 3.87 / 3.14 | LBM 5.26 / 3.85 / 3.14 | ≤ 0.02 |
| 3 (Tariq [137]) | MCMB 음극 · **graphite** | x / y / z | RW 1.57 / 1.92 / 2.59 | FVM 1.56 / 1.89 / 2.57 | ≤ 0.03 |
| 3 | · **기공** | x / y / z | RW 1.42 / 1.19 / 2.39 | FVM 1.42 / 1.18 / 2.37 | ≤ 0.02 |

- 값은 **τ** (표 4 의 같은 행 τ² 와 일치: Iwai 기공 LBM τ² 2.03/2.06/1.83 → τ 1.42/1.44/1.35).
- Iwai: 고체상 이방성이 커서 **시료 부피가 유효 이온·전자 전도도를 내기에 부족** 하다고 결론 (p.58). Tariq: z 축 기공 τ 가 높음 — RVE 분석으로 지속 여부 확인 필요; RW 계산 시간은 FVM 의 일부 (p.59).

### 3-D. Table 4 (flux 기반, p.61) · Table 5 (기하 기반, p.62) — 기공상, 축별 τ² · τ
| 표 | 방법 | 시료 | 영상 | 픽셀 [µm] | 부피 [µm³] | ε | τ² (x / y / z) | τ (x / y / z) | 출처 |
|---|---|---|---|---|---|---|---|---|---|
| 4 | Laplace equation | Ni-YSZ SOFC 음극 | FIB-SEM | 0.0417 | 105.2 | 0.195 | 2.10 / 2.20 / 1.90 | 1.45 / 1.48 / 1.38 | Wilson [102] |
| 4 | Laplace equation | Ni-YSZ SOFC 음극 | X-ray | 0.0427 | 250.0 | 0.300 | 2.94 / 3.28 / 3.15 | 1.71 / 1.81 / 1.77 | Izzo [81] |
| 4 | Laplace equation | Ni-YSZ SOFC 음극 | X-ray | 0.008 | 13.8 | 0.180 | 1.77 / 1.51 / (z 미제시) | 1.33 / 1.23 / — | Grew [120] |
| 4 | Finite volume method | MCMB 전지 전극 | X-ray | 0.016 | 1,100.0 | 0.451 | 2.01 / 1.39 / 5.61 | 1.42 / 1.18 / 2.37 | Tariq [137] |
| 4 | Lattice Boltzmann | Ni-YSZ SOFC 음극 | FIB-SEM | 0.062 | 972.4 | 0.496 | 2.03 / 2.06 / 1.83 | 1.42 / 1.44 / 1.35 | Iwai [103] |
| 4 | Random walk | Ni-YSZ SOFC 음극 | FIB-SEM | 0.062 | 972.4 | 0.496 | 2.05 / 1.99 / 1.78 | 1.43 / 1.41 / 1.33 | Iwai [103] |
| 4 | Random walk | MCMB 전지 전극 | X-ray | 0.016 | 1,100.0 | 0.451 | 2.03 / 1.41 / 5.72 | 1.42 / 1.19 / 2.39 | Tariq [137] |
| 4 | Heat flux simulation | LiFePO₄ 전지 전극 | X-ray | 0.020 | 3,000 | 0.410 | 2.70 / 2.19 / 3.32 | 1.64 / 1.48 / 1.82 | Cooper [63] |
| 4 | Heat flux simulation | YSZ 다공 지지층 | FIB-SEM | 0.030 | 421.9 | 0.350 | 2.82 / 2.72 / 3.10 | 1.68 / 1.65 / 1.76 | Tjaden [85] |
| 4 | Heat flux simulation | YSZ 다공 지지층 | X-ray | 0.0325 | 314.4 | 0.410 | 3.13 / 2.25 / 2.96 | 1.77 / 1.50 / 1.72 | Tjaden [85] |
| 4 | Heat flux simulation | LiMn₂O₄ 전지 전극 | X-ray | 0.597 | 10,434,731 | 0.363 | 8.29 / 2.31 / 4.97 | 2.88 / 1.52 / 2.23 | Shearing [106] |
| 4 | Heat flux simulation | LiMn₂O₄ 전지 전극 | X-ray | 0.065 | 75,164 | 0.380 | 6.50 / 2.22 / 3.96 | 2.55 / 1.49 / 1.99 | Shearing [106] |
| 4 | Laplace equation | LSCF SOFC 양극 | FIB-SEM | 0.035 | 144.7 | 0.483 | 1.82 / 1.83 / 1.88 | 1.35 / 1.35 / 1.37 | Joos [147] |
| 4 | Laplace equation | YSZ 다공 지지층 | X-ray | 0.060 | 46,656 | 0.470 | 2.30 / 2.80 / 2.60 | 1.52 / 1.67 / 1.61 | Laurencin [150] |
| 5 | FMM | LiCoO₂ 전지 전극 | X-ray | 0.65 | 17,487,363 | 0.431 | 1.16 / 1.12 / 1.02 | 1.08 / 1.06 / 1.01 | Taiwo [2] |
| 5 | FMM | Graphite 전지 전극 | X-ray | 0.65 | 28,080,838 | 0.484 | 1.10 / 1.11 / 1.03 | 1.05 / 1.05 / 1.01 | Taiwo [2] |
| 5 | FMM | LiMn₂O₄ 전지 전극 | X-ray | 0.65 | 27,529,606 | 0.453 | 1.14 / 1.11 / 1.02 | 1.07 / 1.05 / 1.01 | Taiwo [2] |
| 5 | FMM | YSZ 다공 지지층 | FIB-SEM | 0.030 | 421.9 | 0.350 | 1.42 / 1.25 / 1.23 | 1.19 / 1.12 / 1.11 | Tjaden [85] |
| 5 | FMM | YSZ 다공 지지층 | X-ray | 0.0325 | 314.4 | 0.410 | 1.44 / 1.25 / 1.19 | 1.20 / 1.12 / 1.09 | Tjaden [85] |
| 5 | Pore centroid method | LiFePO₄ 전지 전극 | X-ray | 0.020 | 3,000 | 0.410 | 1.46 / 1.41 / 1.58 | 1.21 / 1.19 / 1.26 | Cooper [63] |

### 3-E. ★ 같은 시료에서 방법만 바꾼 쌍 — "방법별로 값이 얼마나 다른가" (우리 산술, 원문 표값으로 계산)
| 시료 (ε) | flux τ (x / y / z) | 기하 τ (x / y / z) | flux ÷ 기하 | τ_C flux / 기하 (식 21) | Bruggeman τ (α=1.5) |
|---|---|---|---|---|---|
| Tjaden [85] YSZ, FIB-SEM (0.350) | 열유속 1.68 / 1.65 / 1.76 | FMM 1.19 / 1.12 / 1.11 | **1.41 / 1.47 / 1.59** | 1.695 / 1.139 (×1.49) | 1.30 |
| Tjaden [85] YSZ, X-ray (0.410) | 열유속 1.77 / 1.50 / 1.72 | FMM 1.20 / 1.12 / 1.09 | **1.48 / 1.34 / 1.58** | 1.655 / 1.135 (×1.46) | 1.25 |
| Cooper [63] LiFePO₄ (0.410) | 열유속 1.64 / 1.48 / 1.82 | pore centroid 1.21 / 1.19 / 1.26 | **1.36 / 1.24 / 1.44** | 1.635 / 1.219 (×1.34) | 1.25 |

- ⇒ 같은 단층촬영에서 **flux τ 가 기하 τ 의 1.24–1.59 배** (축별). τ² 로는 1.5–2.5 배. **flux 알고리즘끼리는 ≤ 0.04** 차 (3-C) — "flux 알고리즘 선택은 시료 준비·영상 매개변수·구조 자체보다 영향이 작다" (p.62).
- Bruggeman (ε^(−0.25)) 과 비교: 기하 τ (1.09–1.26) 는 Bruggeman 근처·아래, flux τ (1.48–1.82) 는 위 — 리뷰가 Cooper [111] 에 대해 적은 "pore centroid 는 Bruggeman 을 가깝게 따른다" (p.57) 와 같은 그림이다.
- ⚠ **표 4 전체 vs 표 5 전체를 통째로 비교하지 말 것** — 표 5 의 Taiwo [2] 세 행은 픽셀 0.65 µm 의 다른 시료라 τ ≈ 1.01–1.08 로 낮다. 시료·해상도가 섞인다. 깨끗한 비교는 위 세 쌍뿐이다.
- 식 22 대조 (우리 산술): κ_geo = 0.5 ln κ_flux + 1 ⇔ **τ_geo = √(1 + ln τ_flux)**. Cooper [63] 의 열유속 τ 를 넣으면 1.22 / 1.18 / 1.26 → 실측 pore centroid 1.21 / 1.19 / 1.26 과 **±0.01** 로 맞는다. Tjaden [85] (FMM) 에 넣으면 **0.04–0.15 과대** — 식 22 는 **그 시료·그 기하 알고리즘 전용** 경험식이다.

---

## 4. 리뷰 구조와 방법 (정독) ★
> 이 논문은 시뮬레이션 논문이 아니라 정의·계산법 리뷰다. DEM 양식의 "시뮬레이션 방법" 칸 (code · 접촉법칙 · E·ν·μ · 서보 · RVE · seed) 은 **해당 없음** — 대신 리뷰가 정리한 **각 계산법이 무엇을 재는가** 를 절 순서대로 적는다.

### 4.1 정의 (p.48–49, Fig. 1)
- **식 (1)** τ = Δl/Δx — "the fraction of the shortest pathway through a porous structure Δl and the Euclidean distance between the starting and end point of that pathway Δx" (Fig. 1 에서 Δx = 시료 두께). **τ ≥ 1** 항상.
- "there exists only one shortest pathway and one tortuosity value. From this geometric perspective, **constrictions or bottlenecks of the pore structure are not considered**." (p.48)
- 수송 분야에서는 τ 를 최단경로 척도보다 넓게, **흐름에 대한 저항** 을 기술하는 데 쓴다. **Epstein (1989) [11]** 이 모세관 모형으로 'tortuosity' 와 'tortuosity factor' 를 구분: **식 (2) κ = τ²**. tortuosity factor 는 "**추가 경로 길이와 속도 변화를 둘 다** 담는다".
- **식 (3)** D_eff = (ε/κ)·D_bulk = (ε/τ²)·D_bulk — "which is **also valid for ionic and electronic conductivities**." ★ **"The nomenclature distinguishing between κ and τ is adopted in this review, and values are converted accordingly, where necessary."** (p.48)
- **식 (4)** D_eff = (ε·δ/τ)·D_bulk — van Brakel & Heertjes [12] 의 **constrictivity δ** (경로를 따라 기공 지름이 변하는 효과). 원문은 분모를 **τ** 로 인쇄 (τ² 아님 — §원문 대조 기록 ②).
- Holzer [13]: **τ² 는 실험에서 나온 높은 τ 를 설명하려고 도입** 됐다 → 두 종류로 구분 [13,14]: **τ_exp** (실험 자료로부터 간접 계산) vs **τ_geo** (재구성 3D 볼륨에서 기하 알고리즘).
- 기체 확산은 기구 (ordinary · Knudsen · viscous) [15] 와 기체 종 [16] 에 따라 지배 τ 가 다르다 — 종마다 평균자유행로가 달라 Knudsen 수와 확산 경로가 다르고, "**for each species and each transport regime, a different tortuosity value is dominating**" (p.49).
- 실험에서는 τ 를 따로 밝히지 않고 **'diffusibility' [17,18] · 'effective relative diffusivity' [19,20] = ε/τ²** 로 묶어 쓴다 (p.49; 기호표 p.47 도 ε/τ²).
- 배터리 분야: **식 (5) N_M = σ_bulk/σ_eff = τ²/ε** (MacMullin number) [21–24].
- ★ "**geometric-based tortuosity takes only the shortest path length into account, while flux-based values rather account for the path of least resistance. Hence, the resulting values differ appreciably.**" (p.49)
- τ 의 쓰임 (p.48): Newman 형 전지 모형 [9] 과 Adler–Lane–Steele 전극 반응 모형 [10] 의 **입력 매개변수**.

### 4.2 Porosity–tortuosity 관계 (p.49–51, Table 1, Fig. 2)
- **식 (6)** τ²_Bruggeman = ε^(1−α), 표준 **α = 1.5**. Shen & Chen [25] 리뷰 중 전기화학에서 가장 널리 쓰임 [26]. 저자들이 Bruggeman 원 수식을 번역·해설 [27].
- 역사: Hoogschagen [17] 유리구 기체 확산 — **labyrinth factor (1/τ²)** 가 Maxwell 과 Bruggeman 사이, Bruggeman 쪽에 더 가까움. **식 (7)** τ²_Maxwell = (3 − ε)/2. De La Rue & Tobias [30]: ZnBr₂ 전해액에 비전도 유리구 — 역시 Maxwell–Bruggeman 사이.
- 배터리 [31–35] · PEM [36–45] 에 표준처럼 쓰이고, **COMSOL Multiphysics 에도 표준 기능으로 구현** [24] (p.49).
- 실험과 안 맞는 일이 많아 [24,46] α 를 고쳐 맞추고, Thorat [47] 는 척도 γ 도 넣음: **식 (8)** τ²_Bruggeman = γ·ε^(1−α) (γ = 1.8, α = 1.53).
- Zacharias [53]: α·γ 를 조성 함수로 (γ 2.5/2.6, α 1.27/1.28). Table 1 · Fig. 2 = 산포 큼, τ < 1 외삽, ε = 1 에서 τ ≠ 1 → 의문 (§3-B).
- Chung [56]: 16 개 NMC111 전극 → 계산 τ 가 Bruggeman 보다 늘 약간 위; 합성 충전에서 방향·충전을 바꾸면 **완전 정렬 입자** 는 전 공극률 범위에서 Bruggeman 근접.
- **BruggemanEstimator** [58] (Wood 그룹): 2D 영상 두 장 (윗면 · 단면) 에서 **차원별 α** 를 differential effective medium approximation 으로 추출 — 수치 τ 와 잘 맞음 [58], 실사용 [59]. 입체해석학 (stereology [60]) 과 비슷 — 그러나 Taiwo [2]: stereology 값은 3D 측정과 **상당히 어긋날 수 있다**.
- 단층촬영 대비 Bruggeman 타당성은 시료마다 엇갈림 (맞음 [34,56] / 크게 어긋남 [45,61–63]): "**spherical structures … adhere to the correlation. The correlation, however, is less suitable for connected solid phases and complex porous networks.**" (p.50) 기하 τ 와 수송 제한 τ 의 구분 (또는 그 부재) [64] 도 문제를 키움. 다층 분리막 [52] 은 균질 가정이 깨짐.
- ★ 절 결론 (p.51): "**porosity–tortuosity relationships are only applicable and reliable when executed across homogeneous microstructures which are similar to the microstructure used to derive the respective relationship.**"

### 4.3 실험으로 얻는 τ (p.51–54, Fig. 3, Fig. 4)
**(a) 확산셀 (diffusion cell)** — He [73] 리뷰. 다공 시료를 위·아래 기체 채널 사이에 끼우고 농도차로 상호 확산 → 질량수지로 확산 유량 (Fig. 3, Wicke–Kallenbach) → **확산 모형을 적용해** 유효 이원 확산계수와 τ 를 얻는다. 모형 선택은 확산 기구에 달림 [15,74,75]:
| 식 (p.52) | 형태 (원문 그대로) | 역할 |
|---|---|---|
| (9) | D_i,K = −(2/3)·r_P·(ε/τ²)·√(8RT/(πM)) | Knudsen 확산계수 (원문에 음수 부호 인쇄) |
| (10) | D_eff,i = (1/D_eff,ij + 1/D_i,K)⁻¹ | Bosanquet 결합 |
| (11) | J_i,D = −(1/(RT))·(D_eff,ij ∇p_i + (B_O c_i/μ) ∇p) | Darcy 점성 유동 포함 = advective–diffusion 모형 [76] |
| (12) | J_i,D = −D_eff,i·(p/(RT))·M_i M_j/[w_i(M_j − M_i) + M_i]·∇w_i | Mills [77] 등질량 (equimass) 확산 |
| (13) | J_i,D/D_i,K + Σ_(j≠i) (x_j J_i,D − x_i J_j,D)/D_eff,ij = −p∇x_i/(RT) + (x_i∇p/(RT))·(1 + B_O p/(μ D_i,K)) | Dusty Gas Model (DGM) [74] |
| (14) | Σ_(j≠i) (x_j J_i,D − x_i J_j,D)/D_eff,ij = −(p/(RT))∇x_i | Maxwell–Stefan (Knudsen 무시) |
- SOFC 음극 농도분극 비교에서 **DGM 정확도 최고** [79,80], Fick 은 단순하나 덜 정확. ★ 그러나 "**tortuosity is usually used as a fitting parameter** … the extracted tortuosity values are **highly dependent on the accuracy of the applied model**." (p.52)
- Tjaden [85]: τ 가 **기체 종에 따라 다름** (CH₄ ≈2.3, N₂ ≈2.5), 온도↑ 시 평균 2.36 → 2.73. Zamel [18]: 반대로 온도↑ 시 τ 감소 (ε/τ² +11.5 %) — 원인 후보 = 구조 차 (연결된 고체상의 YSZ vs 무작위 섬유 carbon paper, 기공 크기 분포·평균 지름·공극률).

**(b) 전기화학 실험** (p.53–54)
- 연료 소비 **식 (15)** ṅ_fuel = iA/(nF) [7]. 고전류에서 농도분극 → 확산 이론으로 τ 역산.
- Jiang & Virkar [16]: Fick 을 한계전류로 다시 써서 **식 (16)** D_eff = i_lim / [(2 F p⁰_fuel/(R T d)) − (i_lim/(R T δ))·(A p/ṅ_fuel)] (원문 인쇄: 첫 항 d, 둘째 항 δ). 2·3 원 연료 혼합 → Bosanquet (식 10) 역산 τ: 800 °C H₂–H₂O 2.23, H₂–CO₂–H₂O 2.73.
- Brus [72] (Fig. 4): 같은 방법 + FIB-SEM 재구성 RW. **실험 τ 는 H₂ 농도·온도마다 다른 값, RW 는 하나**. 저 H₂ (농도분극 큼) 값만 대표값으로 간주 — 그때 RW 와 잘 맞음. "under standard fuel cell operating regimes, where activation and Ohmic losses dominate, concentration losses, and thus the tortuosity of the porous layers affect the performance only slightly." (p.53–54)
- ★ "**experimental-based tortuosity values are valid only for the specific experiment at hand**" (p.54). 온도↑ → τ↓ (촉매 활성·확산 속도). Tsai & Schmidt [86–88]: 두께 영향 없음.
- 배터리: Thorat [47] — polarisation-interrupt (restricted diffusion) [89–91] 로 LiFePO₄·LiCoO₂ 활물질 막 τ, **AC impedance 로 분리막 전해액 유효 전도도 → MacMullin 수 / τ** (앞의 검증용). 결과가 γ = 1.8, α = 1.53. Bae [92]: Doyle–Newman 수정 모형 [93] 으로 주기 채널 전극의 τ 계산 → co-extrusion LiCoO₂ 로 검증 (§3-A).
- 절 결론 (p.54): 실험 τ 는 **적합 매개변수라 모형에 강하게 의존**. 연료전지는 운전 조건이 다양하지만 배터리는 그렇지 않아 "**it appears to be easier to extract an overall valid tortuosity value for a battery layer than a fuel cell layer.**"

### 4.4 3D 볼륨에서 τ 계산 (p.54–60)
- 영상: FIB-SEM slice-and-view [95] · X-ray CT [96,97] — 원리는 다르나 **같은 해상도면 같은 자료** [85,98,99]. FIB-SEM 은 EDS·EBSD·SIMS 병행 (화학·결정 정보), X-ray 는 비파괴라 in-situ/operando (4D) [101]. 합성 3D 볼륨 [34,56,107,108] 으로 공극률·기공 크기 분포·입자 모양·충전 방향의 효과를 직접 평가 (Fig. 5).
- ★ "**There remains some confusion in the literature regarding the different definitions of tortuosity for the purpose of image-based modelling**" (p.55) → 리뷰의 분류:

| 분류 (p.55) | 하는 일 | 대표 알고리즘 |
|---|---|---|
| (1) **Geometric-based** | 기하만 보고 최단경로 길이 | pore centroid [63,106,109–111] · FMM [2,112,113] · distance propagation [114] · 기타 최단경로 탐색 [115,116] |
| (2a) **Flux-based, voxel** | 분할된 voxel 영역에서 직접 수송 모사 (재메싱 없음) | Laplace (FD, TauFactor) · LBM · random walk · (sub-grid) FVM |
| (2b) **Flux-based, mesh** | 체적 메시 생성 후 CFD/FEM | FEMLAB/COMSOL · ParCell3D · StarCCM+ · StarCD · Cast3M · Batts3d |

#### 4.4.1 기하 알고리즘 (p.55–57, Fig. 6, Fig. 7)
- voxel 위에서 바로 돌아 메시 불필요, 결과가 **식 1 정의를 그대로 따라** 해석이 쉽다. pore centroid 외에는 **distance map** (각 픽셀의 출발면까지 거리) 을 만들어 최단경로뿐 아니라 **τ 히스토그램** 을 준다.
- **FMM**: 한 면에서 반대 면으로 전진하는 파면의 도달 시간 → 거리지도 → "tortuosity is calculated by dividing the shortest path length between two opposing planes by the **Euclidean distance of the two endpoints of that path**." (p.56) Jørgensen [112]: LSC/CGO 상별 τ 히스토그램 — 단일 평균보다 더 많은 정보 (부피분율에 맞게 LSC τ > CGO τ).
- **distance propagation**: Chen-Wiegart [114] — τ 의 **3D 공간 분포** (Fig. 6, LiCoO₂ 국소 1–2.5) → 반응성 낮은 영역, 불균일 충전, 열화 위치를 짚는다. Shearing [115]: 같은 크기 타일 모자이크로 τ·비표면적·공극률 지도 — 대개 고공극 = 저 τ 이나 **저공극·저 τ 타일** 도 있음 ("counterintuitive").
- ★ Chen-Wiegart 의 비교: LiCoO₂ 기공상은 거리전파 ≈ 확산 시뮬레이션. 그러나 SOFC 두 시료의 기공·YSZ 상은 **기하 τ 가 확산 τ 보다 일관되게 낮음** — "**the geometrically shortest path through a structure is not always the path of least resistance for a flux, owing to the presence of constrictions and pore necks.**" (p.56)
- **pore centroid** (Fig. 7): 2D 단면마다 상의 무게중심을 셋째 축으로 이어 **축마다 τ 하나** (히스토그램·분포 없음). Amira·Avizo (FEI) 의 기본 기능이라 빠른 비교용. Cooper [111]: LSCF 를 열유속 · Avizo XLab · 확산 · RW · pore centroid 로 같은 시료 (14 °C·695 °C) — **pore centroid 최저·Bruggeman 근접, flux 계열끼리 일치**. 불균질성이 크면 요동. ★ Cooper [118]: "if the analysed characteristic feature becomes small compared to the control volume, the centroid of each 2D plane will tend towards the centre, resulting in a **tortuosity of unity**" → 적용성에 의문 (p.57).

#### 4.4.2 flux 알고리즘 — voxel (p.57–59, Fig. 8, Table 2, Table 3)
- ★ 기하 알고리즘의 한계 (p.57): "**small connections consisting only of one voxel would contribute only a negligible amount to the overall flux of transported species, while they are fully included in the above calculation methods.**"
- **Laplace**: Izzo [81] (X-ray CT SOFC 음극, 기공상) → Grew [120] 고체상으로 확장 (식 3 대로 이온·전자 전도도도 τ 에 묶이므로 고체상 τ 도 중요; **고체 τ ≥ 1.2 × 기공 τ**) → RVE [121]. **TauFactor** [118,122–124] (MATLAB, 2상 분할 3D tiff, 축별·상별 τ, Fig. 8) — Avizo XLab Thermo · 열유속과 비슷한 결과 (p.58).
- **LBM** (식 17): 입자분포함수 f(x, e, t) 의 streaming + collision (충돌항 Ω) [119,132]. 기체·이온·전자 수송 모두 모사 가능해 연료전지에서 널리 [103,126–131]. Iwai [103]: FIB-SEM + EDX 로 Ni/YSZ 구분, 상별 유효 확산·이온·전자 전도도 → Table 2. 고체 τ > 기공 τ (Chen-Wiegart [114] 와 같은 결론). Vivet [133] (유한차분): Ni τ 높음, YSZ 분율이 커서 YSZ τ 는 Iwai 보다 낮음.
- **Random walk** (식 18): 비흡착 walker 를 상에 뿌리고 매 step 이웃 voxel 선택 — 같은 상이면 이동, 다른 상이면 제자리 → 평균제곱변위 r²(t) → **D_eff = (V_phase/6)·dr²/dt** → 빈 공간의 bulk D 와 비교해 τ. 1990 년대 정식화 [5,138,139], 다공 암석 [140] → 전기화학은 Kishimoto [134]. ⚠ **walker 수·step 수에 결과가 의존** → Iwai: 10⁵ walker · 10⁷ step. Tariq [137]: RW ≈ sub-grid FVM [141] (Table 3), RW 가 계산 시간 훨씬 짧음.

#### 4.4.3 flux 알고리즘 — mesh (p.59–60, Fig. 9, Fig. 10)
- 메시 생성 시 smoothing · surface repair · 메시 매개변수가 결과에 영향 → "**care must be taken … and sensitivity analyses should be carried out**" (p.59) [85].
- Wilson [102]: FIB-SEM SOFC 음극 → FEMLAB (현 COMSOL) 유한요소로 Laplace. Ivers-Tiffée 그룹 ParCell3D [142–146]; Joos [147]: LSCF·기공 두 상의 RVE (공극률·비표면적·τ, Fig. 9) — 시료 1·3 은 l_cat > 10 µm 평탄, 시료 2 LSCF 는 거의 두 배 필요. ★ "**To follow the nomenclature of this review, it has to be pointed out that τ in Figure 9 ought to be replaced by τ²**" (p.60, 원문 인쇄는 "τ [2]" — §원문 대조 기록 ③).
- 그 밖: COMSOL [148,149] · Cast3M [150] · 장치 전용 Batts3d [34,56,151].
- **열유속 유비** (Fourier ↔ Fick): **식 (19)** J_eff = −D_bulk·(ε/τ²)·(c₁ − c₂)/d, **식 (20)** q̇_eff = −λ_bulk·(ε/τ²)·(T₁ − T₂)/d — 온도를 농도로 읽는다 [85,106,152–154]. Cooper [63]: LiFePO₄, 8.8 µm 정육면체, adaptive polyhedral mesh, StarCCM+ (Fig. 10 은 YSZ 지지층 예).

#### 4.4.4 τ_C 와 κ_geo–κ_flux 관계 (p.60)
- **식 (21)** τ_c = 3·[(τ_x⁻¹) + (τ_y⁻¹) + (τ_z⁻¹)]⁻¹ — 세 축 **조화평균** 'characteristic tortuosity' [63,85].
- Cooper [63] 8 부분부피: 기하 (pore centroid) 와 열유속의 characteristic **tortuosity factor** 를 비교 → **식 (22)** κ_geo = 0.5·ln(κ_flux) + 1. "**the simulation-based tortuosity factor (and as such, tortuosity) is always higher than the geometric-based value of the same sample in cases where either value is >1.**" 이유 = 한 voxel 지름 연결도 기하 계산에는 온전히 들어가지만 flux 로는 거의 안 흐름 (p.60).

#### 4.4.5 부분부피 (sub-volume) 분석 (p.60)
- 볼륨을 작은 부분으로 나눠 각각 flux τ → 히스토그램·분포지도와 비슷한 정보 + 균질도 [51,147,155]. Kehrwald [51] (StarCD, 12 부분부피): 국소 τ **3 배** 차 → Li⁺ 가 고 τ 영역을 피하고 저 τ 영역으로 몰림 → 충방전 비효율, 성능·열화의 공간 분포, 미세구조 불균질이 고장·파괴 원인일 수 있음 [51,155].

### 4.5 Summary 절 (p.60–62, Table 4, Table 5)
- ★ "**Calculation approaches, which take flux-like behaviour into account (cf. Table 4), arrive at higher tortuosity values compared to purely geometric-based algorithms (cf. Table 5). It is thus imperative to distinguish between these two approaches as otherwise, misinterpretation may ensue.**" (p.61)
- 같은 종류 시료에서도 값이 다른 이유 = **영상 해상도** (고해상 → 작은 기공·연결성 드러남). 단 매개변수마다 해상도 감도가 다르다: Shearing [106] — 공극률·기하 τ 는 micro/nano CT 에서 일치, **비표면적은 nano 가 2 배 이상** (Mandelbrot [156] 해안선 비유).
- 시료 부피가 **대표성** 을 가질 만큼 커야 [157] — 고해상·대부피일수록 정확·대표적. 배터리처럼 여러 길이척도가 중요한 구조에서는 이것이 제약 [158].
- Wilson [102] vs Iwai [103]: 부피 9 배 차이에도 τ 차이 없음; Laurencin [150] vs Tjaden [85] 도 비슷 — 균질 시료는 작은 부피로도 대표값. 같은 '시료 종류' 가 구조적으로 같다는 뜻은 아님.
- 서로 다른 flux 알고리즘은 비슷한 결과 (같은 시료 [103,137]) → "**the choice of a flux-based computation algorithm has a smaller effect on the results than sample preparation technique, imaging parameters and the structure of the sample itself, which includes pore size distribution and volume fractions of the constituent phases.**" (p.62)
- Wilson vs Izzo: Izzo τ 가 더 높은데 공극률은 1.5 배 → "**the tortuosity itself does not give a full picture of the microstructure and the performance**" — 다른 미세구조 특성과 함께 평가 [115,159].
- Knudsen 을 고려하지 않는 **순수 연속체 모형** (열유속 시뮬레이션 등) 은 실험과 차이를 낼 수 있다 [85].

### 4.6 Concluding remarks = 리뷰의 권고 (p.62–63)
| # | 권고 (원문 요지) | 쪽 |
|---|---|---|
| R1 | 경향: porosity–tortuosity 상관식 (Bruggeman) 은 **배터리·PEM** 에서, flux 알고리즘은 **SOFC** 에서 흔하다 | p.62 |
| R2 | "**the Bruggeman relationship is valid only for spherical structures and is generally unfit to predict accurate values for complex porous networks**" | p.62 |
| R3 | 영상 기반 알고리즘도 조심 — **기하 vs flux τ 의 차이와 의미를 알고** 써야 한다; "**Results of either calculation procedure differ visibly, where geometric values lie below flux-based algorithms.**" | p.62 |
| R4 | 실험 τ 는 **그 실험에만 유효** (온도·셋업·기체 조성), 대개 **적합 매개변수** 라 **계산 모형에 강하게 의존** | p.62 |
| R5 | 비슷한 시료끼리 flux 결과를 비교하면 τ 는 미세구조 매개변수의 복잡한 함수 → **기공 크기 분포·구성상 부피분율과 함께 해석** | p.62–63 |
| R6 | Knudsen 효과를 빼는 순수 연속체 모형은 시뮬레이션–실험 불일치의 원인일 수 있어 조심 | p.63 |
| R7 | (정의 절) **κ 와 τ 를 구분** 하고 필요하면 환산해 보고 — 리뷰 스스로 그렇게 함 | p.48 |
| R8 | (기법 절) 메시 매개변수 감도 분석 (p.59) · RW 의 walker·step 수 명시 (p.59) · RVE 확인 (p.58–60, p.61) · 해상도 명시 (p.61) | p.58–61 |

### 4.7 입자 처리 ★ (DEM 양식 항목)
- **해당 없음.** 리뷰는 입자 모형을 다루지 않는다 (영상 · 메시 · 상관식). 구 vs 형상 · mono/bi/poly-PSD · 강체 vs 접촉 소성 vs 형상 소성 축은 n/a.
- 구와 관련된 언급만 있다: ① Bruggeman 은 **구형 구조** 에서 잘 맞는다 (p.50, p.62); ② Chung [56] 합성 입자 충전에서 **완전 정렬** 이면 Bruggeman 근접 (p.50); ③ 유리구 실험 (Hoogschagen [17], De La Rue & Tobias [30]) 은 Maxwell–Bruggeman 사이 (p.49).
- **접촉 저항 · 점접촉 협착은 나오지 않는다.** 협착은 '기공 목 (pore neck)' 의 기하 (δ, 식 4) 로만 다룬다. ⇒ 우리 Holm 접촉 협착은 이 리뷰의 분류 **밖** 에 있다 (§7).

### 4.8 기법 미니 용어집
| 용어 | 리뷰 설명 (쪽) | 우리 쪽 대응 |
|---|---|---|
| geometric tortuosity τ | 최단경로 ÷ 끝점 유클리드 거리 (식 1, p.48) | τ_Dij · τ_Dij,all · 벽 τ |
| tortuosity factor κ | κ = τ² (식 2, p.48); 리뷰는 기하 τ 에도 κ_geo = τ_geo² 로 같은 제곱을 쓴다 (p.60) | 인계 계획의 T |
| constrictivity δ | 경로를 따른 기공 지름 변동 인자 (식 4, p.48) | 대응 없음 (우리 협착 = 접촉 Holm) |
| diffusibility · effective relative diffusivity | ε/τ² (p.47, p.49) | f = σ_eff/σ₀ |
| labyrinth factor | 1/τ² (Hoogschagen, p.49) | 1/T |
| MacMullin number N_M | σ_bulk/σ_eff = τ²/ε (식 5, p.49) | 1/f |
| Bruggeman exponent α · scaling factor γ | τ² = γ·ε^(1−α) (식 8) | `sigma_bruggeman` = φ^1.5 (α = 1.5, γ = 1) |
| BruggemanEstimator | 2D 두 장에서 차원별 α (p.50) | 없음 |
| Knudsen · Bosanquet · DGM · MSM · advective–diffusion · equimass | 기체 확산 모형 (식 9–14, p.52) | 없음 (고체 이온 전도) |
| Wicke–Kallenbach · Loschmidt cell | 확산셀 (Fig. 3, p.52–53) | 없음 |
| polarisation-interrupt (restricted diffusion) | 활물질 막 τ (p.54) | 없음 |
| FMM · distance propagation | 거리지도 기반 기하 τ (p.56) | τ_Dij,all (다중 출발 Dijkstra) 이 가장 가깝다 |
| pore centroid | 단면 무게중심 사슬, 축당 하나 (p.57) | 없음 |
| voxel Laplace (TauFactor) · LBM · random walk · FVM | flux τ (p.57–59) | STEP3 복셀 FV (MPM 킷) 가 같은 종류 |
| mesh FEM/CFD · heat flux analogy | flux τ (p.59–60, 식 19–20) | 없음 |
| characteristic tortuosity τ_C | 세 축 조화평균 (식 21) | 없음 (우리는 z 한 축) |
| RVE · sub-volume | 대표 부피·국소 τ 분포 (p.58–60) | τ_Dij,all per-source 값 (지도화 안 함) |

---

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | 식 1 모식: 구 충전 사이 **기공** 을 지나는 굽은 최단경로 Δl, 두께 Δx | τ_Dij 정의의 그림. 단 ASSB 에서는 전도상이 고체 입자라 우리 경로는 입자 **사이** 가 아니라 SE 입자 **안** 의 중심 꺾은선 — 위상이 뒤집혀 있다 |
| 2 | Table 1 의 α·γ 로 그린 **κ = τ² – ε** 곡선 (위: 전극 7, 아래: 분리막 5) 과 Bruggeman (α=1.5, γ=1). 축 라벨 'κ = τ² [-]' | 상관식 산포가 크다; γ ≠ 1 이면 ε = 1 에서 κ ≠ 1, Kehrwald 곡선은 ε ≈ 0.38 부터 κ < 1. 우리 `sigma_bruggeman` 기준선을 "하나의 상관식" 으로 일반화하지 말 것 |
| 3 | Wicke–Kallenbach 확산셀 질량수지 (기체 1·2 채널, 시료 통과 확산 유량) | 해당 없음 (기체). "실험 τ = 모형 적합값" 의 출발점 |
| 4 | Brus [72]: 수소 % 에 따른 실험 τ (Virkar 모형 / Fick + 표면확산, 700·800 °C) vs **FIB-SEM (overall) ≈ 2** (판독). 축 라벨 'Tortuosity' (τ 인지 τ² 인지 리뷰가 밝히지 않음) | 실험 τ 는 조건 의존 적합 매개변수 → EIS-TLM τ² 대조 시 모형·조건 병기. 저농도 (분극 큰) 조건에서만 영상값과 일치 |
| 5 | 다중 길이척도 단층 재구성 (100 µm → 10 µm → 2.5 µm 축척) — 고해상이 있어야 확산에 영향 주는 특징이 보인다 | 우리 d_h/dx ≳ 3.5 규칙 · STEP3 복셀 해상도 감도와 같은 메시지 |
| 6 | Chen-Wiegart [114]: LiCoO₂ 기공상 기하 τ 공간분포 (yz·xz·xy 단면, 색 1.0–2.5) | τ_Dij,all 의 출발점별 값 (`per_source`) 으로 같은 지도를 그릴 수 있다 — 지금은 평균만 보고 |
| 7 | pore centroid 모식 — 단면 n 과 n+1 의 무게중심 거리 d(n) | 우리 미사용. 특징 크기가 작으면 τ → 1 (Cooper [118]) |
| 8 | TauFactor 결과: 이진 지도 · 초기 선형 농도 · 정상상태 농도 | STEP3 복셀 FV 와 같은 종류의 계산 (TauFactor 카드) |
| 9 | Joos [147] RVE: 세 볼륨의 LSCF·기공 'Tortuosity τ' vs 전극 두께 l_cat; 평탄값 ≈ 1.9–2.0 (판독, 시료 2 LSCF ≈ 2.15–2.2) | ★ **τ/τ² 혼동 실례** — 리뷰가 "τ 는 τ² 로 읽으라" 고 주석 (p.60). 실제로 평탄값 (판독 ≈ 1.9–2.0) 이 Table 4 의 Joos τ² (1.82–1.88) 에 가깝고 τ (1.35–1.37) 와는 멀다 (표 4 행이 그림의 어느 볼륨인지는 리뷰가 밝히지 않음) |
| 10 | 산소수송막 YSZ 다공 지지층 기공상의 온도 분포 (열유속 유비) | 식 19–20: ε/τ² 가 열·물질 공통 → 우리 σ_thermal 망에도 같은 정의 적용 가능. ⚠ figures/ 의 `fig_10.png` 크롭에 식 (19)(20) 이 함께 들어 있다 |
| Table 1 | Bruggeman α·γ 12 행 (§3-B) | 같은 '전극' 범주 안에서도 α 1.27–5.2 · γ 0.115–2.6 |
| Table 2 | Iwai [103] RW vs LBM, 기공·Ni·YSZ 축별 τ (§3-C) | flux 알고리즘끼리 ≤ 0.04 |
| Table 3 | Tariq [137] RW vs FVM, graphite·기공 축별 τ (§3-C) | 같음 |
| Table 4 | flux 기반 14 행, τ² 와 τ 병기 (§3-D) | 보고 형식의 본보기 (축별 · τ² 와 τ · 픽셀 · 부피 · ε) |
| Table 5 | 기하 기반 6 행 (§3-D) | 같은 시료 쌍 3 개가 방법 차이의 직접 증거 (§3-E) |

## 6. Post-processing ★ (리뷰가 보이는 계산·보고 관행)
- **무엇**: 축별 (x/y/z) τ 와 τ² 를 함께 (Table 4·5) · 세 축 τ_C 조화평균 (식 21) · 기하 τ 히스토그램과 공간 분포지도 (Fig. 6, Shearing [115] 타일) · flux τ 의 부분부피 배열 (Kehrwald [51], Joos [147]) · RVE 곡선 (Fig. 9) · 기하–flux 상관 (식 22) · 상관식 적합 (α, γ; Table 1).
- **도구**: Amira · Avizo (FEI; XLab plugin / XLab Thermo), TauFactor (MATLAB), BruggemanEstimator, FEMLAB/COMSOL, StarCCM+ · StarCD (CD-adapco), ParCell3D, Cast3M, Batts3d, LBM · RW 자체 코드.
- **수치화 규약**: 문헌값을 κ ↔ τ 로 환산해 한 표에 (p.48 "values are converted accordingly, where necessary") — 단 **어느 행을 환산했는지는 표시하지 않는다** (§10).
- **품질 점검 항목**: RW walker·step 수 (p.59) · 메시 매개변수 감도 (p.59) · 픽셀 크기와 부피 (Table 4·5 에 열로 둠) · RVE (p.58–61).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md`
> 이 리뷰는 물리 모델 경쟁자가 아니라 **명명·계산법 기준** 이다. frame[5] 로 보면 수송 기술자 (transport descriptor) 쪽 — **DEM 반쪽** 의 일 (접촉망 σ · 경로) 에 해당하고, 역학·형상 (MPM 반쪽) 은 없다. frame[4]: 리뷰의 flux/기하 격차를 우리 모델에 **맞추라는 뜻이 아니다** — 우리 τ 들이 어떤 범주의 양인지 이름을 정하는 데만 쓴다.

| 항목 | 이 리뷰 | 우리 | 같은 점 / 다른 점 · 이유 |
|---|---|---|---|
| 전도상 | **기공** (액체 전해액·기체) — 연속상 | **SE 고체 입자상** (이온), AM 입자상 (전자), 전 입자 (열) | 위상이 뒤집혔다 — 기공 목 대신 **입자 접촉** 이 병목 |
| 미세구조 | 단층촬영 (FIB-SEM · X-ray CT), 일부 합성 | LIGGGHTS DEM 구 충전 (강체 + 겹침), MPM 스캐폴드 | 우리는 영상 해상도 대신 **접촉 기하** (겹침 δ → 접촉 반경 a) 가 병목 크기를 정한다 |
| 기하 τ | voxel 위 FMM · 거리전파 · pore centroid | SE 접촉 그래프 Dijkstra (중심 꺾은선): τ_Dij · τ_Dij,all · 벽 τ | **같은 범주** (식 1). 이산화가 다르다 (그래프 vs voxel) |
| flux τ | voxel (Laplace · LBM · RW · FVM) · mesh (FEM/CFD 열유속) | **Kirchhoff 접촉망** (FULL = 원기둥 R_bulk + Holm/Mikic R_c · CF = R_c 0) + STEP3 복셀 FV (MPM 킷) | 접촉망 flux 는 리뷰 분류에 **없는 세 번째 이산화**. STEP3 은 리뷰의 voxel Laplace 와 같은 종류 |
| 협착 | 기공 목 — flux 해에 자연히 포함, δ 로 따로 쓰기도 | Holm R_c = 1/(2σa) **접촉 단위 저항** (FULL 에만) | 리뷰의 "한 voxel 연결은 기하에는 온전히, flux 로는 거의 0" (p.57) ↔ 우리 "작은 a 접촉은 Dijkstra 에는 온전한 간선, Kirchhoff 에선 큰 R_c" — **같은 논리, 더 극단적인 형태** |
| 축 | x / y / z + τ_C | **z (두께 방향) 하나** | 문헌 τ_C 와 우리 τ_z 를 바로 비교하면 안 된다 |
| 보고 | τ² 와 τ 를 같이 | 웹앱·내보내기는 √ (τ_Lap,eff) 중심, τ² 열 없음 | § 우리 τ 이름 권고 |
| 상관식 | Bruggeman 비판 (구형·균질 한정) | `sigma_bruggeman` = φ^1.5 를 기준선으로 출력 | 우리 SE 는 점접촉 입자상 — Bruggeman 의 전제 (연속 매질 + 분산 구) 와 구조가 다르다 |
| 실험 τ | 확산셀·전기화학, 적합 매개변수 | EIS-TLM 문헌 τ² (Minnmann 2021 등) 와 대조 | 리뷰 R4: 실험 τ 는 그 실험·모형 전용 |
| 범위 경고 | SOFC · 액체 Li-ion 기공상 수치 | LPSCl SE 상 | 표 4·5 의 **절대값을 우리 τ 기대값으로 쓰지 말 것** (상·전도 기구·해상도가 다름). 가져올 것은 **정의와 방법 간 비** 뿐 |

---

## ★ § tortuosity 정의 대조표 (리뷰 정의 ↔ 우리 τ)
> **우리 기호** (코드로 확인, 2026-10-02):
> - φ = φ_SE = Σ_SE (4/3)π r³ ÷ (box_x·box_y·plate_z) — 구 부피 합 (`scripts/network_conductivity.py:1120–1123`)
> - σ₀ = σ_grain (웹앱 `_sigma_grain_context`, 25 °C 기본 3.0 mS/cm — **펠릿값**, 원장 CL-91) · 솔버 정규화 σ_bulk
> - σ_full = FULL 해 (간선 = R_bulk + R_constriction), **전체 단면 box_x·box_y 로 정규화** (`network_conductivity.py:853–857`, 출력 `:1156`)
> - σ_CF = `sigma_bulk_net` = CONTACT_FREE 해 (R_constriction = 0) (`:1157`)
> - R_bulk = (d/2)/(π r₁²) + (d/2)/(π r₂²) — 중심선 원기둥 (`:401–403`)
> - τ_Lap,eff = √(φ·σ_grain/σ_full) (`webapp/app.py:2610`) · τ_Lap,geom = √(φ·σ_grain/σ_bulk_net) (`app.py:2613`)
> - τ_Dij = `tortuosity_mean` — 바닥·위 관통 SE 무작위 ≤ 200 쌍의 (중심 꺾은선 최단 길이 ÷ 두 끝 중심의 Δz), [1, 20) 만 (`scripts/dem_analysis_core.py:569`)
> - τ_Dij,all = `tortuosity_all_mean` — 바닥 관통 SE **전부** 에서 다중 출발 Dijkstra 로 가장 가까운 위쪽 SE 까지, τ_i = L_i/Δz_i, 절단 없음 (`dem_analysis_core.py:654`)
> - 벽 τ = `tortuosity_SE_wall` — 바닥 벽·플래튼 띠 (두께 r_SE,max), 같은 성분 안 무작위 쌍, 규칙은 τ_Dij 와 같음 (`scripts/lhs_descriptor_harvest.py:229`, `N_TAU_PAIRS = 200`, `TAU_LO, TAU_HI = 1.0, 20.0`)
> - 인계 계획 (메인 전달): f = σ_eff/σ₀ · T = φ/f · τ = √T
> - COMSOL 5.6 Eq 6-6 (메인 전달, 이 카드에서 매뉴얼 원문 미대조): f_e = ε_p/τ_F, Bruggeman τ_F = ε_p^(−1/2)

| # | 리뷰 정의 (식 · 쪽) | 리뷰가 말하는 뜻 | 우리 대응 | 같은 양인가 | 환산 (우리 기호) |
|---|---|---|---|---|---|
| D1 | **τ = Δl/Δx** (식 1, p.48) | 기하 τ — 최단경로 하나 ÷ 끝점 유클리드 거리 (Fig. 1 은 두께). ≥ 1, 협착 무시 | **τ_Dij · τ_Dij,all · 벽 τ** | **같은 범주** (기하), 이산화 다름 | 그대로 τ. 차이 셋: ① 경로 = SE 중심 꺾은선 — SE 합집합 안의 측지선보다 **길거나 같다** (접촉한 두 구의 중심 선분은 두 구 안에 있으므로; 우리 산술) ② 분모 = 두 끝 중심의 **Δz** — 식 1 본문 (끝점 유클리드 거리) 보다 작아 옆으로 어긋난 쌍에서 우리 값이 크다 (Fig. 1 의 두께 해석과는 맞음) ③ 경로 하나가 아니라 **표본 평균** (τ_Dij·벽 τ) / **출발점 전부의 평균** (τ_Dij,all) — 리뷰의 '히스토그램' 쪽 |
| D2 | **κ = τ²** (식 2, p.48), 'tortuosity factor' (Epstein [11]) | 경로 연장 + 속도 변화를 함께 담는 인자. 리뷰는 기하 τ 에도 κ_geo = τ_geo² 를 쓴다 | **T** (인계 계획) = τ_Lap,eff² | **같은 양** (FULL 가지, flux) | κ_flux,FULL = T = φ·σ₀/σ_full |
| D3 | **D_eff = (ε/κ)·D_bulk = (ε/τ²)·D_bulk** (식 3, p.48) — "이온·전자 전도에도 유효" | flux 기반 τ 의 정의식 | **τ_Lap,eff** | **같은 양** (ε→φ_SE, D→σ, D_bulk→σ_grain) | τ_flux,FULL = √κ = √(φ·σ₀/σ_full) |
| D3′ | (같은 식 3 을 협착 0 가지에 적용 — 리뷰에 없는 가지) | — | **τ_Lap,geom** (웹앱 한글 라벨) = τ_Laplace,bulk (영문 라벨) = `tau_Laplace_bulk` (COMSOL 내보내기) | **flux 범주** — 리뷰의 'geometric' (D1) 이 **아니다** | τ_flux,CF = √(φ·σ₀/σ_CF). ⚠ 곧은 단일 사슬 (같은 r, d = 2r) 에서 원기둥 R_bulk 모형은 f = π r²/A, φ = (2/3)π r²/A → **τ²_CF → 2/3 < 1** (N 큰 극한, 우리 산술). 겹쳐서 중심 거리 d < 2r 이면 τ²_CF → (4/3)·r/d — d > 4r/3 인 한 여전히 1 미만. 리뷰의 "곧은 경로 = 1, 항상 ≥ 1" 정규화를 따르지 않는다 (원인: 원기둥 단면 π r² > 구의 평균 단면 (2/3)π r², φ 는 구 부피 합) |
| D4 | **D_eff = (ε·δ/τ)·D_bulk** (식 4, p.48) · constrictivity δ (van Brakel [12]) · τ_exp vs τ_geo (Holzer [13,14]) | 기공 지름 변동을 δ 로 분리; τ² 는 높은 실험 τ 를 설명하려는 장치 | 별도 δ 없음. FULL 은 Holm 협착을 κ **안에** 묶는다 | **다른 양** (δ = 기공 지름 기하 / 우리 = 접촉 Holm 저항) | 같은 망에서 협착 몫 = κ_FULL/κ_CF = σ_CF/σ_full (= 솔버 출력 `R_brug_over_full` — 이름과 달리 CF/FULL, 원장 L2-07). τ 로는 √ |
| D5 | **ε/τ²** = 'diffusibility' / 'effective relative diffusivity' (p.47 기호표, p.49) | τ 를 따로 밝히지 않는 묶음 양 | **f** (인계 계획) | **같은 양** (전도 판) | f = σ_full/σ₀ = φ/κ |
| D6 | **1/τ²** = 'labyrinth factor' (Hoogschagen [17], p.49) | ε 없는 묶음 | 1/T | 같은 양 | 1/κ = f/φ — ⚠ D5 와 ε 하나 차이, 혼동 주의 |
| D7 | **N_M = σ_bulk/σ_eff = τ²/ε** (식 5, p.49) | MacMullin 수 (배터리) | σ₀/σ_full | **같은 양** | N_M = 1/f = κ/φ |
| D8 | **τ² = ε^(1−α), α = 1.5** (식 6) · **τ² = γ·ε^(1−α)** (식 8) (p.49) | 상관식 — 구형·균질 구조에서만 신뢰 | `sigma_bruggeman` = φ^1.5 (`network_conductivity.py:1125`) | **같은 관계** (α = 1.5, γ = 1) | κ_Brug = φ^(−0.5), τ_Brug = φ^(−0.25). ⚠ Landesfeind [24] 는 같은 관계를 τ = ε^(−α), **α = 0.5** 로 쓴다 (그쪽 τ = 리뷰 κ) — 지수 이름 α 가 문헌마다 1.5 / 0.5 |
| D9 | **τ² = (3 − ε)/2** (식 7, Maxwell, p.49) | 상관식 | 없음 | — | — |
| D10 | **τ_c = 3·[(τ_x⁻¹) + (τ_y⁻¹) + (τ_z⁻¹)]⁻¹** (식 21, p.60) | 세 축 조화평균 | 없음 — 우리는 z 한 축 | 다른 양 | 문헌 τ_C 와 우리 τ_z 직접 비교 금지 |
| D11 | **κ_geo = 0.5·ln(κ_flux) + 1** (식 22, p.60; 기호표 p.47 은 κ_geo · **κ_CFD**) | Cooper [63] 한 시료 (LiFePO₄, 8 부분부피) 의 경험식 | (τ_Dij², τ_Lap²) 쌍과 같은 범주 | 범주만 같음 | ⇔ τ_geo = √(1 + ln τ_flux). **이식 불가** — 다른 시료 (Tjaden [85]) 에서 이미 0.04–0.15 어긋남 (§3-E) |
| D12 | 실험 τ — 확산셀 (식 9–14) · 전기화학 (식 15–16) · AC impedance / polarisation-interrupt (p.51–54) | 모형 적합 매개변수, 그 실험에만 유효 | EIS-TLM 문헌값 (예: Minnmann 2021 τ²) | D3·D7 정의를 거쳐 같은 양이나 **모형·σ₀ 의존** | κ_exp ↔ κ_flux,FULL — **σ₀ (단결정·펠릿·벌크) 규약을 맞춘 뒤에만** |
| D13 | Random walk **D_eff = (V_phase/6)·dr²/dt** (식 18, p.59) | voxel flux | 없음 | — | — |
| D14 | 열·물질 유비 **J_eff, q̇_eff 에 ε/τ²** (식 19–20, p.60) | 열유속으로 κ | σ_thermal 망 (thermal channel) — τ 열 없음 | 정의는 적용 가능 | κ_th = φ·k₀/k_eff — 단 열 망은 **다상** (AM–AM · AM–SE · SE–SE) 이라 φ 와 k₀ 를 무엇으로 둘지 따로 정해야 한다 |
| D15 | (리뷰 밖) **COMSOL f_e = ε_p/τ_F, Bruggeman τ_F = ε_p^(−1/2)** — 메인 전달 Eq 6-6. 같은 내용을 Landesfeind [24] p.A1374 가 "COMSOL … **ε/τ = ε^1.5**" 로 적는다 (원문 확인) | 연속체 전지 모형의 입력 | 웹앱 표 머리 "COMSOL input = τ_Lap_eff" (`app.py:2615`) · 내보내기 `tau_Laplace_eff` "★ 3D tortuosity (COMSOL/EIS input)" (`scripts/export_comsol_2d.py:104`) | **τ_F = κ = T = τ_Lap,eff²** | √ 값 (τ_Lap,eff) 을 τ_F 칸에 넣으면 f = ε_p/τ_F 가 **τ_Lap,eff 배 과대** 가 된다 — 확인 필요 (§ 우리 τ 이름 권고) |

**문헌 사이 이름 환산표** — 같은 κ 를 무엇이라 부르나
| 문헌 (근거) | 그 문헌의 기호 · 이름 | 리뷰 기호로 | 비고 |
|---|---|---|---|
| Tjaden 2018 (이 카드) | κ = τ², tortuosity factor | κ | 표 4·5 는 'τ²' 와 'τ' 두 열 |
| Epstein 1989 [11] (리뷰 경유, 원문 미대조) | κ = τ², tortuosity factor | κ | 모세관 모형 |
| TauFactor, Cooper 2016 (정본 카드) | τ = ε·D/D_eff, 'tortuosity factor τ' | κ | 이름은 τ 인데 양은 κ |
| Duquesnoy 2020 (정본 카드, TauFactor 카드 역링크) | TauFactor τ 를 CSV 에 저장, 그림은 √ | CSV = κ · 그림 = τ | 한 논문 안에서 두 거듭제곱 |
| Landesfeind 2016 = 리뷰 [24] (원문 p.A1374 확인) | N_M = τ/ε (Eq 5), 'effective tortuosity τ'; Bruggeman τ = ε^(−α), α = 0.5 (Eq 6); "τ in Eq. 5 appears often as τ²" | κ | 리뷰는 그 논문을 인용하며 N_M = τ²/ε 로 쓴다 |
| Minnmann 2021 (원문 PDF 5쪽 확인) | τ_i², 'tortuosity factor' (Eq 4) | κ | 인쇄된 Eq 4 는 분수가 뒤집혀 있다 (§원문 대조 기록 ⑨) |
| Bielefeld 2020 (정본 카드) | σ_eff = (ε_SE/τ²)·σ_bulk → τ² | κ | — |
| COMSOL (메인 전달 Eq 6-6) | τ_F (f = ε/τ_F) | κ | — |
| Nguyen 2020 (형제 카드 `nguyen2020_electrode_tortuosity_factor` — 이 카드 작성자는 원문 미열람) | 'conventional tortuosity factor τ' (관통 flux, Eq 1) · 'electrode tortuosity factor **τ_e**' (차단 대칭셀 임피던스, Eq 2) | τ = κ · τ_e 는 **리뷰에 없는 새 양** | 전극 (P2D) 매개변수로는 τ_e 를 쓰라는 권고 — 리뷰 이후의 정의라 이 대조표의 D 행에는 없다 |
| 우리 웹앱 | τ_Lap_eff = √(φσ₀/σ_full) | √κ = τ | 머리말 "COMSOL input" 과 거듭제곱 불일치 (D15) |

### ★ 우리 τ 별 판정 (요약)
| 우리 τ | 리뷰 범주 | 판정 | 걸리는 것 |
|---|---|---|---|
| τ_Dij (`tortuosity_mean`) | geometric (식 1), 그래프 판 | ✅ 대응 | 표본 ≤ 200 쌍 · Δz 분모 · [1, 20) 절단 · 무작위 쌍의 옆 우회 |
| τ_Dij,all (`tortuosity_all_mean`) | geometric — FMM 거리지도 쪽 (출발점마다 하나) | ✅ 대응 | Δz 분모. 절단 없음 |
| 벽 τ (`tortuosity_SE_wall`) | geometric | ✅ 대응 — 배포본의 "Tortuosity (기하학적)" 표기는 리뷰 분류와 맞다 | README 문구 "수송 τ (tortuosity factor) 가 아니다" 는 'tortuosity factor' 를 '수송 τ' 와 동일시 — 리뷰에서 tortuosity factor 는 **τ² (방법 무관)** 이다 |
| τ_Lap,geom (CF) | **flux** (협착 0) | ⚠ **이름 충돌** — 'geom' · 'geometric' 은 리뷰에서 최단경로 계열 전용 | 원기둥 정규화라 τ ≥ 1 보장 없음 (D3′) |
| τ_Lap,eff (FULL) | **flux** (Holm 협착 포함) | ✅ **같은 양** (식 3 의 τ = √κ) | σ₀ = 펠릿값 (CL-91) 이라 κ 는 "펠릿 대비" · 접촉면적 모드 셋 (Hertz / Physics / Stage-E Physics) 이 한 이름을 공유 |
| f · T · τ (인계 계획) | ε/τ² · κ · τ | ✅ 리뷰와 정확히 맞는다 | 기호 T 는 우리 코드에서 두께·온도로 이미 쓰인다 |
| COMSOL τ_F | κ | ⚠ 입력 = T (= τ_Lap,eff²) | 웹앱·내보내기 문구 |
| `sigma_bruggeman` | 상관식 (α = 1.5, γ = 1) | ✅ | 리뷰 R2: 구형·균질 한정 |
| `τ_Lap_eff / τ_Dij` 행 ("Constriction overhead") | flux ÷ 기하 | ⚠ 해석 과잉 | 리뷰에서 flux/기하 격차는 **협착이 없는 연속 기공상에서도** 1.24–1.59 (§3-E) — 이 비는 협착 + 정의 차 + 원기둥 정규화가 섞인 양 |

---

## ★ § 우리 τ 이름 권고
### 원칙 (리뷰 근거)
| # | 원칙 | 근거 |
|---|---|---|
| N1 | **'tortuosity factor' 는 τ² (κ) 에만**, 'tortuosity' 는 τ 에만 쓴다. 값을 낼 때는 **τ 와 τ² 를 둘 다** 싣는다 | 식 2 · p.48 "nomenclature distinguishing between κ and τ" · Table 4·5 의 두 열 |
| N2 | **계산 계열 꼬리표를 이름에 넣는다**: `geo` (최단경로) / `flux` (수송 해). 리뷰 자신도 두 계열을 같은 기호 τ 로 쓰므로 기호만으로는 구분이 안 된다 | p.61 "imperative to distinguish … otherwise, misinterpretation may ensue" |
| N3 | **'geometric' 은 최단경로 계열에만.** flux 해에서 협착을 끈 가지는 geometric 이 아니다 | p.55 분류 · p.49 "path of least resistance" |
| N4 | flux τ 에는 **이산화** (`net` = DEM 접촉망 Kirchhoff / `vox` = STEP3 복셀 FV) 와 **가지** (`full` / `cf`) 를 붙인다 | 리뷰는 voxel·mesh 를 나눈다 (p.55); 접촉망은 그 분류 밖의 세 번째 |
| N5 | flux τ 는 **σ₀ 와 φ 의 정의를 메타로** 함께 낸다 — κ = φσ₀/σ_eff 라 σ₀ 에 정비례 | 식 3 · 식 5 의 σ_bulk |
| N6 | **축을 적는다** (우리 = z). 3 축 τ_C 와 섞지 않는다 | 식 21 · Table 4·5 |
| N7 | 실험 대조값 (EIS-TLM 등) 에는 **모형과 조건** 을 붙인다 | R4 · p.54 · p.62 |

### 권고 이름표
| 양 | 리뷰 이름 | 권고 열 키 (예) | 권고 표시 라벨 | 지금 이름 | 바꿀 것 |
|---|---|---|---|---|---|
| σ_eff/σ₀ | diffusibility / effective relative diffusivity (ε/τ²) | `f_ion_net_full` | f = σ_eff/σ₀ (= φ/τ²) | 인계 계획 f | 그대로 + σ₀·φ 메타 |
| σ₀/σ_eff | MacMullin number | `NM_ion_net_full` | N_M = σ₀/σ_eff (= τ²/φ) | 없음 | 선택 |
| φσ₀/σ_full | tortuosity factor κ | `tau2_flux_ion_net_full` | τ² (tortuosity factor · flux · 접촉망 · 협착 포함) | 인계 계획 **T** | **T → `tau2`** — T 는 두께 (T/d_AM) · 온도와 겹치고, κ 는 우리 문서에서 열전도도 기호라 둘 다 피한다 |
| √(φσ₀/σ_full) | tortuosity τ | `tau_flux_ion_net_full` | τ (flux · 접촉망 · 협착 포함) = √τ² | τ_Lap_eff · `tau_Laplace_eff` | "COMSOL input" 문구를 **τ²** 쪽으로 옮긴다 (D15) |
| φσ₀/σ_CF | (리뷰에 없음 — flux, 협착 0) | `tau2_flux_ion_net_cf` | τ² (flux · 접촉망 · 협착 0 = CONTACT_FREE) | — | 신설 |
| √(φσ₀/σ_CF) | (같음) | `tau_flux_ion_net_cf` | τ (flux · 접촉망 · 협착 0) | 한글 **τ_Lap_geom (Laplace, GB 제외)** · 영문 τ_Laplace,bulk · 내보내기 `tau_Laplace_bulk` "3D **geometric** tortuosity (no constriction)" | **'geom' · 'geometric' 삭제** (N3). 영문 라벨 'τ_Laplace,bulk — Laplacian without constriction' 은 이미 맞다 |
| 중심 꺾은선 / Δz, 쌍 표본 | geometric tortuosity | `tau_geo_SE_dij` | τ_geo (기하 · SE 중심 최단경로 · 표본 쌍 · Δz) | `tortuosity_mean` · τ_Dij (Dijkstra, 기하만) | 라벨은 이미 '기하' — 키에 `geo` 를 넣을지는 선택 |
| 같은 것, 출발점 전부 | geometric | `tau_geo_SE_dij_all` | τ_geo,all | `tortuosity_all_mean` | 같음 |
| 같은 것, 벽 띠 | geometric | `tortuosity_SE_wall` (**배포 키 유지**) | Tortuosity (기하학적) | 배포 v1.1 | README 문구만: "수송 τ (tortuosity factor) 가 아니다" → "flux 기반 τ 도, 그 제곱 (tortuosity factor) 도 아니다" |
| τ_FULL/τ_CF | — | `tau_ratio_net_full_over_cf` | 접촉 협착 배수 (같은 망, R_c 만 켜고 끔) | — | 신설 권고 — **협착 배수는 이것으로 정의** |
| τ_flux/τ_geo | — | `tau_ratio_flux_over_geo` | flux ÷ 기하 (정의 차 + 협착 + 정규화) | 'τ_Lap_eff / τ_Dij' = "Constriction overhead" | 'Constriction overhead' 라벨을 위 비로 옮긴다 |
| STEP3 복셀 | voxel Laplace 계열 | `tau2_flux_ion_vox` | τ² (flux · 복셀 FV · 접촉 저항 항 0) | 없음 | 만들 때 `vox` 꼬리표 — CL-81: 복셀 σ 는 CONTACT_FREE 가지 위 → `net_cf` 와 같은 부류이나 교차검증 상대가 아님 |
| 상관식 | Bruggeman (α = 1.5) | `sigma_bruggeman` 유지 | Bruggeman (α = 1.5, γ = 1; τ² = φ^−0.5) | — | 라벨에 α 관례 (1.5 형) 를 적는다 — Landesfeind 형 (α = 0.5) 과 혼동 방지 |

- 같은 규칙을 전자 (`_el_`) · 열 (`_th_`) 채널에도 쓴다. ⚠ 전자 채널 꼬리표로 `_e_` 를 쓰지 않는다 — Nguyen 2020 의 **electrode tortuosity factor τ_e** (형제 카드) 와 겹친다. 그 양을 언젠가 우리 망에서 낸다면 `tau2e_…` 처럼 따로 둔다. 접촉면적 모드는 메타 (`area_mode` = hertz / physics / stageE_physics) 로 붙인다 — 지금 τ_Lap,eff 한 이름이 세 모드를 공유한다 (웹앱 표 Hertz·Physics 두 칸, COMSOL 내보내기는 Stage-E Physics 우선, `export_comsol_2d.py:69–70`).
- ⚠ 이 카드는 이름을 **권고** 할 뿐 코드·웹앱·배포본을 고치지 않았다. 고칠 때는 CLAUDE.md 의 "코드 → 웹앱 순차 반영" 규칙대로 툴팁 (`app.py:1944–1948`, `:2050`, `:2134–2143`) · COMSOL 내보내기 · 배포 README 를 같은 묶음에서.

---

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① ★ **COMSOL 입력의 거듭제곱을 먼저 확인한다.** COMSOL 의 τ_F 가 f = ε/τ_F 의 τ_F 라면 (메인 전달 Eq 6-6, Landesfeind p.A1374 의 "ε/τ = ε^1.5" 와 일치) 넣을 값은 **T = τ_Lap,eff²** 다. 지금 웹앱 머리말과 내보내기 설명은 τ_Lap,eff (√) 를 "COMSOL input" 이라 적는다. 실제로 COMSOL 에 어떤 값이 들어갔는지 (넣은 기록이 있다면) 확인 대상.
- ② **EIS 대조도 거듭제곱을 맞춘다.** Minnmann 2021 은 τ² (예: τ_ion² = 4.3 @ 42 vol% NCM, 정본 카드) 를 낸다 → 우리 쪽은 τ_Lap,eff² 와 비교하고, σ₀ 규약 (그들 σ_i,0 vs 우리 펠릿값 3.0, CL-91) 을 맞춘 뒤에만 수치를 나란히 둔다 (리뷰 R4·N5).
- ③ **협착 배수는 같은 망의 FULL/CF 로 정의한다.** 리뷰가 보인 flux/기하 격차 (협착 없는 연속 기공상에서도 τ 로 1.24–1.59, §3-E) 를 생각하면, τ_Lap,eff/τ_Dij 를 "Constriction overhead" 라 읽는 것은 과하다. 순수 접촉 협착은 τ_FULL/τ_CF (= √(σ_CF/σ_full)) 다. σ_CF/σ_full 의 코퍼스 배수는 CLAUDE.md 의 CL-81 절 (원장 `CL-81`) 에 있다 — 재계산되지 않은 값이라는 그 절의 한정어 그대로 쓰고, 이 카드에는 옮겨 적지 않는다.
- ④ **CF 가지의 정규화를 시험으로 고정한다.** 코드 식으로 따지면 곧은 단일 SE 사슬에서 τ²_CF → 2/3 (§ 대조표 D3′, 우리 산술). 리뷰 정의라면 1 이어야 한다. "곧은 사슬 셋 → τ_geo,all = 1" 시험 (`webapp/test_tortuosity_all.py`) 처럼 CF 쪽에도 곧은 사슬 selftest 를 두면 이 차이가 기록된다 (규율 ②: 재현 시험 먼저).
- ⑤ **Bruggeman 기준선은 '구형·균질' 전제를 달고 쓴다** (R2). 우리 SE 는 점접촉 입자상이라 Bruggeman 의 전제 (연속 매질 + 분산 구, Hoogschagen·De La Rue 실험계) 와 구조가 다르다. CF/FULL 과 Bruggeman/FULL 이 서로 반대쪽에 서는 사례 (원장 L2-07 의 Codex 반례) 가 이미 있다.
- ⑥ **공간 분포와 부분부피** (리뷰 §4.4.1·4.4.5): τ_Dij,all 은 출발점별 값 (`detail=True` 의 `per_source`) 을 이미 계산한다 → Fig. 6 형 지도나 히스토그램은 새 계산 없이 그릴 수 있다. flux 쪽은 부분부피 Kirchhoff 가 필요 (미구현).
- ⑦ **해상도 감도의 방향** (Shearing [106]): τ 는 해상도에 둔감, 비표면적은 2 배 이상 변한다 — 우리 STEP3 복셀 τ 를 낼 때 τ 보다 면적·coverage 가 먼저 흔들릴 것이라는 예측과 같은 방향 (d_h/dx ≳ 3.5 규칙, TauFactor 카드 Fig. 7 주의).
- ⑧ **채널마다 τ 가 다르다** — 리뷰 p.49 의 "종·수송 영역마다 지배 τ 가 다르다" 는 기체 얘기지만, 우리 이온 (SE 망) · 전자 (AM 망) · 열 (전 입자 망) 도 망 자체가 달라 κ 가 셋이다. 하나의 'tortuosity' 열로 묶지 말 것.

## 9. 인용 가능 문장 (deck/paper용)
- "Following the distinction between tortuosity τ and tortuosity factor κ = τ² adopted by Tjaden et al. (Int. Mater. Rev. 2018), we report both: the flux-based κ = φ_SE·σ₀/σ_eff from the Kirchhoff contact-network solution and its square root τ, kept separate from the geometric (shortest-path) tortuosity obtained by Dijkstra search on the SE contact graph."
- "Geometric and flux-based tortuosities are not interchangeable: on the same tomograms compiled by Tjaden et al., flux-based values exceed geometric ones by factors of about 1.2–1.6 in τ (our ratio of their tabulated values), because the shortest path is not the path of least resistance in the presence of constrictions."
- "Bruggeman-type porosity–tortuosity correlations are reliable only for homogeneous, sphere-like microstructures similar to those used to derive them (Tjaden et al., 2018); we therefore use the Bruggeman curve (α = 1.5) only as a reference line, not as a predictor."
- "In continuum models that write σ_eff = σ₀·ε/τ_F (Bruggeman: τ_F = ε^−1/2), the input τ_F is the tortuosity factor κ = τ², not the tortuosity τ."

## 10. 주의/한계 (over-claim 방지)
- ⚠ **리뷰 범위**: 2016 년 원고 (게재 2018). SOFC · 액체 Li-ion · PEM · 산소수송막의 **기공상**. 전고체 SE · 접촉저항 · 저항망 계산법은 없다 → 우리 접촉망 τ 의 **정확한 대응 이름** 은 리뷰에서 바로 나오지 않고, 리뷰의 정의 (식 2–3) 를 우리 망에 적용한 **우리 판단** 이다.
- ⚠ **표 4·5 는 다른 논문 값의 모음** 이다. 리뷰가 κ ↔ τ 로 환산했다고 밝히지만 (p.48) **어느 행을 환산했는지는 표시하지 않는다**. 원 논문 규약을 행별로 확인하지 않았다 [미확인].
- ⚠ 표 4 전체와 표 5 전체를 통째로 비교하면 시료·해상도가 섞인다 — 방법 차이의 근거로 쓸 수 있는 것은 같은 시료 쌍 3 개 (§3-E) 다. 그 비 (1.24–1.59) 는 **우리 산술** 이다.
- ⚠ 식 22 는 **한 시료** (LiFePO₄, 8 부분부피) 경험식 — 다른 시료에 넣으면 0.04–0.15 어긋난다 (우리 산술).
- ⚠ Fig. 4 · Fig. 9 의 수치는 **판독값** (TREND only). Fig. 4 축 'Tortuosity' 가 τ 인지 τ² 인지 리뷰는 밝히지 않는다.
- ⚠ 우리 쪽 해석 중 **코드 식에서 끌어낸 산술** (곧은 사슬 τ²_CF → 2/3, 중심 꺾은선 ≥ 측지선) 은 실행 시험으로 확인하지 않았다.
- ⚠ COMSOL Eq 6-6 은 **메인 전달** 이고 이 카드에서 COMSOL 매뉴얼 원문을 보지 않았다. 같은 관례를 Landesfeind 원문이 적는 것만 확인했다.
- ⚠ 우리 코퍼스의 τ_Lap,eff/τ_Dij · τ_FULL/τ_CF 분포는 계산하지 않았다 (이 환경에 케이스 코퍼스 없음) → 리뷰의 1.24–1.59 와의 수치 대조는 **미실행**.
- ⚠ 리뷰 본문의 내부 불일치 (아래 기록) 가 있으니 원문 숫자를 인용할 때 표와 본문을 둘 다 본다.

---

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것)
**리뷰 안의 불일치**
1. 기호표 (p.47) 는 flux 기반 characteristic tortuosity factor 를 **κ_CFD**, 본문 식 22 (p.60) 는 **κ_flux** 로 쓴다 — 같은 양, 이름 둘.
2. 식 (4) (p.48) 는 D_eff = (εδ/**τ**)·D_bulk 로 인쇄 — 리뷰 자신의 κ = τ² 규약 (식 2–3) 과 맞추려면 εδ/κ 로 읽어야 일관 [해석 · van Brakel [12] 원문 미대조].
3. 그림 9 주석 (p.60) 은 "τ in Figure 9 ought to be replaced by **τ [2]**" 로 인쇄 — 2 가 인용 링크 (파란색) 로 조판됐다. 그림 캡션 ('tortuosity factor') 과 판독값 (≈ 1.9–2.0 ↔ 표 4 Joos τ² 1.82–1.88) 으로 보아 **τ²** 의 뜻이다.
4. 표 4 는 Shearing [106] 두 행을 **Heat flux simulation** 으로 적는데, 본문 (p.61) 은 [106] 이 **pore centroid 기하 τ 2.0 / 1.9** 를 계산했다고 적는다. 표 4 의 축별 τ 를 식 21 로 묶으면 **2.06 / 1.92** (우리 산술) — 본문 값과 맞는다. 방법 라벨 중 하나가 틀렸을 수 있다 [미확인].
5. 표 4·5 의 Cooper [63] 부피 **3,000 µm³** 와 본문 (p.60) 의 "**8.8 µm** 정육면체" (= 681 µm³, 우리 산술) 가 맞지 않는다 [미확인].
6. 식 (9) 의 음수 부호, 식 (16) 의 첫 항 d · 둘째 항 δ — 원문 인쇄 그대로 옮겼다.

**같은 묶음의 다른 원문 (inbox `tortuosity_20261003/`) 에서 확인한 것**
7. **Landesfeind 2016** (리뷰 [24], J. Electrochem. Soc. 163(7) A1373–A1387) p.A1374: "N_M = τ/ε [5]" (empirical 'effective tortuosity τ'), "τ = ε^(1−m) = ε^(−α) [6]", 구형 Bruggeman **α = 0.5**, "implemented in commercial software packages (e.g., Comsol Multiphysics), where it is expressed terms of **ε/τ = ε^1.5**", "the tortuosity τ in Eq. 5 appears often as τ²". ⇒ 그쪽 τ = 리뷰 κ. 리뷰는 같은 [24] 를 근거로 N_M = τ²/ε 를 적는다 — **인용한 쪽과 인용된 쪽의 기호가 다르다.**
8. 위 7 은 D15 (COMSOL τ_F = κ) 의 독립 근거다.
9. **Minnmann 2021** (inbox #1, PDF 5쪽) Eq 4 인쇄: τ_i² = (σ_i,eff/σ_i,0)·φ_i. 인쇄 그대로면 σ_eff ≤ σ_0 · φ < 1 이라 τ² < 1 인데 보고값은 τ² = 4.3 (이온) · 7.4 (전자) → **분수가 뒤집혀 인쇄** 된 것이다 (물리적으로는 (σ_i,0/σ_i,eff)·φ_i). 정본 카드 `minnmann2021_jes_charge_transport_bottlenecks` 는 l.44 에 물리적으로 맞는 형태, l.158 에 인쇄 그대로의 형태를 적어 **카드 안에서 두 형태가 공존** 한다 (이 카드에서는 그 카드를 고치지 않았다 — 메인 보고).

**그림 파일**
10. `litdb/figures/tjaden2018_tortuosity_review_calculation_approaches/fig_10.png` 크롭 위쪽에 식 (19)(20) 이 함께 들어 있다 (그림 영역은 정상).

---

## 참고문헌 — 우리가 더 볼 것 (리뷰 목록의 서지 그대로)
> 리뷰 목록에 **전고체 논문은 없다.** 아래는 우리 세 축 (① τ 정의·협착, ② flux vs 기하, ③ 입자 충전·접촉) 에 닿는 것만 골랐다.

| 축 | 서지 (원문 그대로) | 왜 |
|---|---|---|
| ① 정의 | [11] Epstein N. On tortuosity and the tortuosity factor in flow and diffusion through porous media. Chem Eng Sci. 1989;44(3):777–779. | κ = τ² 의 원출처 — 우리 τ/τ² 이름의 근거를 리뷰 경유가 아니라 원문으로 |
| ① 협착 | [12] van Brakel J, Heertjes P. Analysis of diffusion in macroporous media in terms of a porosity, a tortuosity and a constrictivity factor. Int J Heat Mass Transfer. 1974;17(9):1093–1103. | constrictivity δ 원출처 — 식 4 의 τ / τ² 인쇄 확인, 우리 접촉 협착 배수와의 관계 정리 |
| ① 협착 | [13] Holzer L, Wiedenmann D, Münch B, et al. The influence of constrictivity on the effective transport properties of porous layers in electrolysis and fuel cells. J Mater Sci. 2013;48(7):2934–2952. | τ_exp vs τ_geo 구분 + 협착 정량 — 우리 τ_flux,FULL / τ_flux,CF / τ_geo 셋의 분해 틀로 가장 가깝다 |
| ① 협착 | [14] Wiedenmann D, Keller L, Holzer L, et al. Three-dimensional pore structure and ion conductivity of porous ceramic diaphragms. AIChE J. 2013;59(5):1446–1457. | 3D 구조 → 이온 전도도를 기하 τ·협착으로 잇는 식 (Landesfeind 가 N_M 식으로 인용) — 우리 φ·τ_geo·협착 → σ 예측식 후보 |
| ① 정의 | [5] Clennell B. Tortuosity: a guide through the maze. Geol Soc Lond Spec Publ. 1997;122(1):299–344. | τ 정의 총정리 — Landesfeind 가 "τ 가 τ² 로 나타나는 이유" 로 인용 |
| ① 정의 | [6] Ghanbarian B, Hunt AG, Ewing RP, et al. Tortuosity in porous media: a critical review. Soil Sci Soc Am J. 2013;77(5):1461. | 기하·전기·확산·수력 τ 분류 — 이름표의 다른 분야 대조 |
| ① 상관식 | [27] Tjaden B, Cooper SJ, Brett DJL, et al. On the origin and application of the Bruggeman correlation for analysing transport phenomena in electrochemical systems. Curr Opin Chem Eng. 2016;12:44–51. | Bruggeman 원 수식 해설 — α = 1.5 / 0.5 관례 혼동을 정리할 원문 |
| ② flux vs 기하 | [63] Cooper SJ, Eastwood DS, Gelb J, et al. Image based modelling of microstructural heterogeneity in LiFePO4 electrodes for Li-ion batteries. J Power Sour. 2014;247:1033–1039. | 식 21·22 원출처 — 같은 시료의 κ_geo vs κ_flux, 부분부피 방법 |
| ② flux vs 기하 | [64] Zhang Y, Chen Y, Yan M, et al. New formulas for the tortuosity factor of electrochemically conducting channels. Electrochem Commun. 2015;60:52–55. | "geometrical vs transport limiting tortuosity" 구분 (p.50) — 전도 채널의 tortuosity factor 식 |
| ② flux vs 기하 | [114] Chen-Wiegart Y, DeMike R, Erdonmez C, et al. Tortuosity characterization of 3D microstructure at nano-scale for energy storage and conversion materials. J Power Sour. 2014;249(0):349–356. | 거리전파 vs 확산을 같은 시료에서 — 기하 < flux 의 원 자료, τ 공간지도 |
| ② flux | [118] Cooper SJ. Quantifying the transport properties of solid oxide fuel cell electrodes. Ph.D. Thesis, London, 2015. | TauFactor 원 구현·pore centroid 비판 — 우리 STEP3 복셀 τ 를 낼 때의 기준 |
| ② RVE | [147] Joos J, Ender M, Carraro T, et al. Representative volume element size for accurate solid oxide fuel cell cathode reconstructions from focused ion beam tomography data. Electrochim Acta. 2012;82:268–276. | flux τ 의 RVE 판정 방법 — 우리 RVE (≥ 7.5× 최대 입자) 경험칙의 정량화 |
| ③ 입자 충전 | [56] Chung D-W, Ebner M, Ely DR, et al. Validity of the Bruggeman relation for porous electrodes. Modell Simul Mater Sci Eng. 2013;21(7):74009. | 합성 입자 충전 (방향·정렬 변화) 에서 Bruggeman 타당성 — 우리 DEM 구 충전과 가장 가까운 설정 |
| ① 상관식 | [29] Chueh CC, Bertei A, Pharoah JG, et al. Effective conductivity in random porous media with convex and non-convex porosity. Int J Heat Mass Transfer. 2014;71(0):183–188. | 무작위 다공 매질의 유효 전도도 — 볼록/비볼록 **공극** 형태 효과. 리뷰는 Maxwell 관계의 근거로 인용 ([28,29], p.49) — 우리 `sigma_bruggeman` 외의 기준선 후보 |
| ③ 접촉 | [61] Stephenson DE, Hartman EM, Harb JN, et al. Modeling of particle-particle interactions in porous cathodes for lithium-ion batteries. J Electrochem Soc. 2007;154(12):A1146. | 입자–입자 상호작용 모형 — 리뷰 목록에서 접촉망에 가장 가까운 것 (Bruggeman 불일치 사례 [45,61–63] 로 인용) |
| ③ 입자 | [62] Gupta A, Seo JH, Zhang X, et al. Effective transport properties of LiMn2O4 electrode via particle-scale modeling. J Electrochem Soc. 2011;158(5):A487. | 입자 단위 모형으로 유효 수송 — 우리 DEM→σ 경로의 선례 |
| ③ 입자 | [34] Vijayaraghavan B, Ely DR, Chiang Y-M, et al. An analytical method to determine tortuosity in rechargeable battery electrodes. J Electrochem Soc. 2012;159(5):A548. | 합성 전극 (Batts3d) 에서 해석적 τ — 우리 스케일링 식과 비교 |
| ③ 열 | [55] Vadakkepatt A, Trembacki B, Mathur SR, et al. Bruggeman's exponents for effective thermal conductivity of lithium-ion battery electrodes. J Electrochem Soc. 2016;163(2):A119. | 열전도 Bruggeman 지수 — 우리 σ_thermal 에서 Bruggeman EMT 가 실패한 기록과 대조 |
| 실험 | [24] Landesfeind J, Hattendorff J, Ehrl A, et al. Tortuosity determination of battery electrodes and separators by impedance spectroscopy. J Electrochem Soc. 2016;163(7):A1373. | EIS 로 τ — 형제 카드 `landesfeind2016_tortuosity_eis_electrodes_separators` (같은 묶음 inbox #5) |
| 실험 | [46] DuBeshter T, Sinha PK, Sakars A, et al. Measurement of tortuosity and porosity of porous battery electrodes. J Electrochem Soc. 2014;161(4):A599. | 배터리 전극 τ 측정법 — EIS 계열 비교 |
| 실험 | [47] Thorat I, Stephenson DE, Zacharias N, et al. Quantifying tortuosity in porous Li-ion battery materials. J Power Sour. 2009;188(2):592–600. | γ = 1.8, α = 1.53 원출처 — 실험 'tortuosity' (지수로 보아 τ² 양) 가 Bruggeman 예측의 약 2 배인 대표 사례 |
| 실험 | [53] Zacharias NA, Nevers DR, Skelton C, et al. Direct measurements of effective ionic transport in porous li-ion electrodes. J Electrochem Soc. 2013;160(2):A306. | 조성 함수 α·γ — 우리 조성 의존 스케일링과 형식 비교 |

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

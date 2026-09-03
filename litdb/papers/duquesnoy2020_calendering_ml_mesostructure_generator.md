<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md.
     ★★ 이 카드는 **논문 + MIT 라이선스 MATLAB 소스코드**를 함께 읽은 digest다.
     소스 21파일/34 KB 를 Script_Main.m 부터 호출그래프로 전수 독해했고,
     그 결과가 §4·§5·§13 이다 — 논문·SI 만 읽어서는 나오지 않는 내용이 절반이다. -->
# 캘린더링(압연)을 "porosity 를 **입력**으로 받는" 확률적 전극 생성기 + TauFactor + SISSO 로 — 실험 54셀 → 8,800 in-silico 전극 → 해석식 — Duquesnoy (J. Power Sources 2020)

> slug `duquesnoy2020_calendering_ml_mesostructure_generator` · DOI `10.1016/j.jpowsour.2020.229103` · type `hybrid (exp 54-electrode 다항회귀 → MATLAB voxel 확률생성기 → TauFactor → SISSO ML)` · PDF `Duquesnoy_2020_JPowerSources_DataDriven_Calendering_ML.pdf` (+ `mmc1.docx` SI · `mmc2.xlsx` exp · `mmc3/mmc4.csv` 880행) · digested `2026-09-03` · status ✅
>
> ★ **Duquesnoy 2023(EnSM, 우리 카드 `duquesnoy2023_ml_multiobjective_manufacturing_optimization`)의 직계 선행 논문**이자, Li-S ASSB 논문(`cronk2026_lis_positive_electrode_geometry_fem`)의 **ref 67**.
> ★★ 이 카드의 존재이유 = **코드**. 논문 본문은 "trend 서술"이 대부분이고, 방법의 실체(=우리가 쓸 수 있는 것과 쓰면 안 되는 것)는 전부 `Script_Main.m → ML__gap.m → Study_Structure_2.m → GenStructure_.m → {sampleSpheresV2_opti, AddSurf3}` 안에 있다. **MIT 라이선스 = 재사용 법적으로 가능.**

---

## 1. 한 줄 요약

실험 **54개 캘린더링 전극**(14조건)에서 `ε_cal = f(AM%, ε_init, 두께 T, 롤 gap)` **5차원 다항식**(R²=0.97)을 뽑고, 그 식을 **MATLAB voxel 확률 전극 생성기**에 심어 (**porosity 를 계산하는 게 아니라 *입력으로 강제*하는**) 8,800개 in-silico 전극을 만들고, 각각을 **TauFactor**(τ_liq·τ_sol)·집전체면 피복률(%CC-AM/%CC-CBD)·active surface 로 분석한 뒤, **SISSO**(symbolic regression)로 "공정변수 → 전극물성" **해석식 5개**(Eq. S4–S8)를 얻은 논문. NMC111 + CBD + **액체 전해질 LIB 양극**.

**우리에게 이 논문의 값은 두 갈래로 완전히 갈린다.**
- **방법론(전이 가능)** — ★ `probaId`/`probaAM` 두 스칼라로 **CBD 형태를 cluster↔film 축으로 파라미터화**하는 성장 알고리즘(§4.2 의사코드)은 우리 `additive_dispersion`에 **지금 없는 축**이고 즉시 이식 가능하다. MIT 라이선스.
- **값(전이 불가)** — ⚠ 생성기는 **1 µm/voxel** 인데 CBD 는 nm 급이다. §5 감사 결과: ① CBD 는 **나노공극 47 %를 포함한 domain 부피**(ρ_eff=0.95 g/cm³)로 잡히고 그 전체가 **불투과 고체**로 복셀화된다 = 실제로 막는 부피 대비 **×1.9** ② 1 µm 껍질로는 AM 표면의 **~25–40 %** 밖에 못 덮는다(실제 100–300 nm 막이면 같은 부피로 100 % 이상) ③ 그들 자신의 데이터 컬럼으로 계산한 **d_h/dx ≈ 1.0** (우리 규칙 `d_h/dx ≳ 3.5` 의 1/3.5) ④ 그 결과 τ 가 **같은 그룹의 같은 소재 EIS 실측 대비 2.4–2.7배** 높다.
- ★★ 그리고 **ML 타깃이 거의 1차원으로 축퇴**해 있다 — `active_surface` 는 **ε_cal/(1−ε_cal) 의 항등식**(R²=**0.9964**, 내 산출), log τ_liq·log τ_sol 은 log ε_cal 의 2차식으로 **97.6 / 96.4 %** 설명된다. ⇒ SISSO 의 R²=0.98–0.995 는 **해석적 ε_cal 다항식을 재학습한 것**에 가깝고, ε_cal 로 설명 안 되는 유일한 출력(%CC-AM, R²_vs_ε=0.19)이 **정확히 SISSO 가 실패한 출력**(0.766)이다. 우리 리포는 이 함정을 **이미 밟고 닫았다**(`use_porosity_pct` REJECT — ε = C − φ_SE − φ_AM 항등식, raw DEM 닫힘 1.0000±0.0000). 그들은 안 닫았다.

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| **Marc Duquesnoy**, Teo Lombardo, **Mehdi Chouchane**(코드 저자), Emiliano N. Primo, **Alejandro A. Franco**(교신) — LRCS/UPJV Amiens · RS2E · ALISTORE-ERI · IUF | **J. Power Sources 480 (2020) 229103**, online 2020-11-04, **CC BY-NC-ND 오픈액세스** | 10.1016/j.jpowsour.2020.229103 | **NMC111**(Umicore) + **CBD** = C-NERGY super C65 CB(IMERYS) : Solef PVdF(Solvay) = **1:1 질량비**; 용매 NMP(BASF); **액체 전해질 LP30**(σ_bulk=1.119 S/m @25 °C) — **LIB 습식 양극, ASSB 아님** | 실험(54셀) + 다항회귀 + **확률적 voxel 생성기(MATLAB)** + TauFactor + **SISSO ML** |

- ERC ARTISTIC (H2020 #772873, Franco). 코드 Zenodo `10.5281/zenodo.3901459`, SISSO `10.5281/zenodo.3901441`. GitHub 리포 `MarcDuquesnoy/Battery_Combining_In_Silico`, **MIT License**, 21 파일 / 34 KB, 저자 표기 **Mehdi Chouchane**. `Image Processing Toolbox` + **TauFactor 앱 사전 실행 필요**.
- 계보: **Ngandjong 2021**(`ngandjong2021_dem_calendering_digital_twin`, 같은 그룹, DEM 압연) 과 **같은 소재·같은 해**이나 **완전히 다른 도구** — Ngandjong = LIGGGHTS DEM 물리, 여기 = 실험식+확률배치. **Duquesnoy 2023** 은 여기의 확률생성기를 **물리 CGMD+DEM 사슬로 교체**하고 BO 를 얹은 후속.
- CRediT: M.D.=DNN·SISSO·실험데이터 fitting(§S1b·S4·S5), **M.C.=전극 생성·분석(§S3)**, E.N.P.=실험, T.L.=집필.

## 3. 핵심 수치

### 3.1 실험 앵커 (`mmc2.xlsx`, 내가 전수 파싱 — stated)
| 항목 | 값 |
|---|---|
| 비-캘린더 전극 | **29셀**, 4조성 |
| 캘린더 전극 | **54셀**(= xlsx CALENDERED 시트 54 데이터행, 본문 서술과 일치), **14 조건** = 4조성 × gap 3~4점 (내가 재구성해 14 확인) |
| 조성 (AM:CB:PVdF wt%) | 96:2:2 · 95:2.5:2.5 · 94:3:3 (solid content 60) · 94:3:3 (solid content 69) |
| 초기 두께 T (평균) | **180 / 170 / 138 / 178 µm** |
| 초기 porosity ε_init | **42.5±0.3 / 47.5±0.3 / 48.9±0.5 / 46.1±0.5 %** |
| 실측 롤 gap | **1, 5, 25, 27, 44, 100 µm** |
| 캘린더 후 ε_cal (실측 범위) | **22.1 – 36.4 %** |
| ⚠ SI 내부 불일치 | 본문 "**54** electrodes / 14 conditions" vs SI S1b "**66** different electrodes in 14 conditions". xlsx 는 **54행** — 본문 쪽이 데이터와 일치 |

**공정 조건 (전부 기록됨 — "조건 미기록" 아님)**: 믹싱 Dispermat CV3-PLUS high-shear **2 h, 25 °C** 수냉 / 코팅 comma-coater PDL250(People&Technology), **gap 300 µm, 속도 0.3 m/s**, Al 집전체 **22 µm** / 건조 2단 오븐 **80 → 95 °C** / 캘린더 BPN250 lap press, **2-roll Ø25 cm**, **line speed 0.54 m/min**, **roll temperature 60 °C**, 압력은 **롤 gap 으로 제어**. 압력 환산은 **Tekscan FlexiForce 힘센서 필름**으로 별도 교정(Fig. S2).

### 3.2 gap → 압력 교정식 (Fig. S2, stated — 그림 안에 식이 인쇄돼 있다)
```
P [MPa] = 189 · exp( − cal_gap / (0.21 · elect_thick) )      elect_thick = 압연 전 두께 (집전체 포함)
```
교정점 4개: gap/T = 0.005 / 0.135 / 0.232 / 0.511 ↔ P ≈ 175 / 86 / 56 / 6 MPa (figure-read ≈, TREND).
⇒ ★ **압력은 gap 의 단조 재라벨링일 뿐**이다. 생성기 루프변수는 gap 이고 압력은 사후 환산 → ML 입력 "pressure" 는 gap 이 갖지 않은 정보를 **하나도** 갖지 않는다.

### 3.3 ε_cal 다항식 — **이 논문의 유일한 실험-앵커 물리** (코드가 정본)
`ML__gap.m:20-21` (계수 12자리 그대로):
```
ε_cal = 0.843501332857·AM%  − 0.723464511643·ε_init  − 0.001324143727·T
        − 0.003060811370·Gap + 0.000005836202·Gap²  + 0.007198782820·ε_init·Gap
        (AM%, ε 는 분율; T·Gap 은 µm; 결과 ×100 = %)
```
- ⚠⚠ **SI Eq. S2 의 두께항 부호가 오타다** — SI 인쇄본은 `+0.001×T`, 코드는 **`−0.001324…×T`**. 코드 부호로 계산하면 실험을 재현하고(아래), SI 부호로는 ε_cal ≈ 69 % 라는 비물리 값이 나온다. **SI 식만 보고 재구현하면 틀린다.**
- ★ **내 검증 — 코드 다항식이 실험을 재현한다** (`mmc2.xlsx` 원자료 대조, 5조건):

| 조건 | 다항식 | 실측 평균 |
|---|---|---|
| AM94, ε_init 48.9, T 138, gap 1 | 25.7 % | 25.6 % (n=4) |
| AM94, ε_init 48.9, T 138, gap 100 | 36.1 % | 36.1 % (n=4) |
| AM94, ε_init 46.1, T 178, gap 1 | 22.4 % | 22.8 % (n=4) |
| AM95, ε_init 47.5, T 170, gap 1 | 23.3 % | 23.1 % (n=4) |
| AM96, ε_init 42.5, T 180, gap 100 | 32.2 % | 32.1 % (n=3) |

- ⚠⚠ **그런데 생성기는 T = 100 µm(시뮬레이션 박스 높이)를 넣는다** (`ML__gap.m:20` 이 `dimension(1,3)` 를 참조; `Script_Main.m` 의 `dimension=[50 50 100]`). 실험 T 범위는 **138–180 µm** → **28 % 아래로 외삽**이고, 두께계수 −0.001324/µm 때문에 **ε_cal 이 계통적으로 +10.3 %p 위로** 옮겨간다 (AM94/ε46 에서 T=178 → 22.5 % vs T=100 → 32.8 %). 데이터셋 ε_cal 이 **29.1–42.0 %** 로 실측 22.1–36.4 % 보다 통째로 높은 이유가 이것이다. **논문·SI 어디에도 언급 없다** (이 항목은 내 분석).
- ⚠ **두께 갱신식이 질량보존이 아니다** (`ML__gap.m:29`): 코드는 `z = z₀·(1 − (ε_i − ε_c))` 를 쓰는데 고체부피 보존은 `z = z₀·(1−ε_i)/(1−ε_c)` 다. ε_i=0.46→ε_c=0.33 에서 **고체량 +7.9 %**, ε_i=0.50→0.29 에서 **+12.2 %** 어긋난다 ⇒ **압력축을 따라 면적당 로딩이 조용히 증가**한다. τ·%CC·AS 는 무차원이라 영향이 작지만, **출력 텍스트의 z 컬럼으로 로딩을 계산하면 최대 ~12 % 틀린다.**

### 3.4 in-silico 데이터셋 (`mmc3.csv`/`mmc4.csv` — 내가 전수 프로파일)
- ★ **"4400 케이스" 의 실체**: 각 CSV = **440 데이터포인트** (헤더 포함 441행). 각 포인트 = **확률 시드 10회 평균** ⇒ 440×10 = **4,400 mesostructures**. 그런 세트가 **둘**(train+test / validation) ⇒ 논문 서술대로 **총 8,800 전극 · 880 데이터포인트**. **CSV 자체는 440행씩이다** (4400행 아님).
- 설계격자: **압력 10점 × AM 4점(93/94/95/96 wt%) × ε_init 11점(40…50 %) = 440** ✓ 완전 factorial.
- 컬럼 10개: `Pressure [MPa], AM wt.%, CBDwt.%, porosity_init, tliq, tsol, CC/AM, CC/CBD, porosity_cal, active_surface`

| 컬럼 | mmc3 (train+test) | mmc4 (validation) | 뜻 |
|---|---|---|---|
| Pressure | 10.53 – 174.21 MPa (10점) | 8.83 – 156.21 MPa (10점) | gap 사다리의 재라벨 |
| tliq | **3.71 – 39.75** | 3.53 – 36.65 | ★ TauFactor **tortuosity FACTOR** (= 논문 그림의 τ_liq **제곱**) |
| tsol | **1.699 – 2.472** | 1.708 – 2.512 | 〃 (AM∪CBD 합친 상) |
| CC/AM | 28.58 – 42.29 % | 27.70 – 41.99 % | z=1 슬라이스의 AM **면적**분율 |
| CC/CBD | 11.24 – 25.58 % | 11.10 – 24.29 % | 〃 CBD |
| porosity_cal | 29.1 – 42.0 % | 29.3 – 42.3 % | ⚠ **다항식의 목표값**(측정값 아님) |
| active_surface | 40.90 – 70.86 % | 41.01 – 72.80 % | ★ 실질 = **ε/(1−ε)** (§7.3) |

- ★★ **단위 규약 함정 (재사용 시 필수)**: 논문 §3 "the τ values correspond to the **square root of the tortuosity factor**". 코드는 `Results.Tau_*3.Tau` 를 **그대로** 저장한다 ⇒ **CSV 의 `tliq`/`tsol` = tortuosity factor**, **논문 그림의 τ = √(CSV 값)**. 검증: CSV tsol 1.699–2.512 → √ = **1.30–1.585** = Fig. 4 세로축(1.30–1.55) ✓. MacMullin `N_M = σ_bulk/σ_eff = τ²/ε = tliq/ε_cal`, `σ_eff = 1.119·ε_cal/tliq [S/m]`.
- ⚠ **validation 세트는 out-of-distribution 이 아니다** — 내가 ε_cal 을 다항식으로 역산하니 mmc3 의 gap 사다리 ≈ {1.2, 10.6, 22.0, 30.9, 41.3, 51.4, 61.3, 71.1, 80.8, 91.1 µm}, mmc4 ≈ {4.7, 15.6, 25.7, 35.6, 45.3, 54.9, 65.4, 74.7, 84.9, 94.9 µm} = **같은 사다리를 ~4 µm 밀어 끼워넣은 것**. 같은 설계상자 안 **보간**이고 조성·ε_init 격자는 **동일**하다. ⇒ "440 unseen points" 의 R²=0.98–0.995 는 **외삽 능력이 아니라 생성기 평균응답의 매끄러움 + 시드잡음**을 잰 값이다.
- ★ 이 역산이 곧 **"공개 코드 = 생산 코드" 증명**이다: 역산된 gap 이 ~10 µm 간격의 깨끗한 단조 사다리로 나왔다(우연히 그럴 확률 없음). 즉 `ML__gap.m` 의 다항식·`T=100` 이 **published dataset 을 실제로 만든 그 코드**다.

### 3.5 SISSO 정확도 (Table S2, stated)
| 출력 | R² (test, 5 시드 평균) | R² (validation 440) | ★ ε_cal 로 설명되는 몫 (내 산출, n=880) |
|---|---|---|---|
| τ_liq | 0.978 | 0.985 | **0.976** (log-log 2차) |
| τ_sol | 0.994 | 0.995 | **0.964** |
| %CC-AM | **0.766** | 0.790 | **0.191** ← 유일하게 독립 |
| %CC-CBD | 0.980 | 0.983 | 0.442 (조성이 지배: ρ(AM%)=−0.919) |
| Active surface | 0.995 | 0.993 | **0.9964** ← 사실상 **항등식** |

### 3.6 상관행렬 (SI Table S3, stated — 전부 전사)
| | P | AM% | ε_init | τ_liq | τ_sol | %CC-AM | %CC-CBD | AS | ε_cal | σ_eff |
|---|---|---|---|---|---|---|---|---|---|---|
| **압력 P** | — | 0 | 0 | +0.594 | −0.708 | +0.497 | +0.259 | −0.677 | −0.678 | −0.637 |
| **AM%** | 0 | — | 0 | −0.415 | +0.178 | +0.593 | **−0.919** | +0.346 | +0.350 | +0.462 |
| **ε_init** | 0 | 0 | — | +0.460 | −0.470 | +0.305 | +0.192 | −0.453 | −0.460 | −0.419 |
| **τ_liq** | | | | — | −0.854 | +0.290 | +0.698 | −0.898 | −0.913 | −0.878 |
| **τ_sol** | | | | | — | −0.549 | −0.520 | **+0.984** | **+0.979** | **+0.952** |
| **AS** | | | | | | | | — | **+0.997** | **+0.989** |
| **ε_cal** | | | | | | | | | — | **+0.985** |

⚠ 표 자체에 대칭성 오타 1건: `ε_init↔τ_sol` 이 상삼각 −0.470 / 하삼각 +0.470. Fig. 4·Fig. 8 이 모두 역상관을 보이므로 **−0.470 이 맞다**.
★ 아랫블록의 +0.95~+0.997 이 §1 의 "타깃 1차원 축퇴"의 정본 증거다 (그들 자신의 표다).

## 4. 방법 — **소스코드 전수 독해** ★★

### 4.0 호출 그래프 (내가 정리)
```
Script_Main.m                       사용자 진입점 (opt1, gap, compo, porosity, dimension, res, N)
└─ ML__gap.m                        ← 실험 다항식 + gap 스크리닝 루프 + 결과 텍스트 기록
   └─ Study_Structure_2.m           ← 조건마다 N회 반복 생성 + TauFactor 3회 + 면 피복률 + active surface
      ├─ GenStructure_.m            ← AM 채우고 → CBD 얹기
      │  ├─ sampleSpheresV2_opti.m  ← AM 구 배치 (voxel 카운트 목표까지)
      │  │  ├─ sampleSpheres.m      ← 사전충전 (해석 부피 목표 1.333N)
      │  │  │  ├─ randomSphere2.m   ← 실험 PSD 에서 r 추출 + 균등 위치
      │  │  │  └─ nonOver2.m        ← 겹침 판정 (β=0.7)
      │  │  └─ SliceV5.m            ← 복셀화
      │  │     ├─ Periodic_Condition_XYZ.m   ← x·y·**z 전부** 주기 이미지 추가
      │  │     └─ Slice_V3.m        ← z-슬라이스별 원판 래스터 (floor!)
      │  └─ AddSurf3.m              ★ CBD 성장 (probaId / probaAM)
      │     └─ findNeighboursSEI.m  ← 26-이웃 (경계에서 잘림, 주기 아님)
      ├─ TauFactor('InLine',…)      ← 외부 툴 (litdb `taufactor_tortuosity_factor_tomography_tool`)
      └─ Contact_pixel.m            ← active surface
         └─ findNeighboursMat26.m   ← 26-이웃 (⚠ §13 결함 D)
```

### 4.1 ★ AM 배치 — porosity 가 **입력**이다 (질문 ③)

**핵심: 압밀 물리가 전혀 없다. 목표 복셀수에 도달할 때까지 구를 던지는 RSA(random sequential adsorption)다.**

1. `GenStructure_.m:2-5` — `Ntot = x·y·z·res⁻³`, `Nam = Ntot·φ_AM` = **AM 이 차지해야 할 복셀 수**. 즉 φ 가 목표다.
2. `sampleSpheresV2_opti.m:29` — 1단계 사전충전: **해석적 구 부피 합**이 `round((1+res/3)·N)` = res=1 에서 **1.333·N** 이 될 때까지 `sampleSpheres` 로 던진다.
3. `sampleSpheresV2_opti.m:34-46` — 2단계 보충: 복셀화한 뒤 `n = #(Im==1)` 를 세고 **`while n < N`** 이 될 때까지 구를 **한 개씩** 추가·복셀화·누적. 목표 도달하면 정지.
4. **겹침 판정** `nonOver2.m:10` — `all(center_dist >= (r_i+r_j)·β)`, **β = 0.7** (`sampleSpheresV2_opti.m:8` 이 기본값 0.8 을 덮어씀).
   - ⚠⚠ **SI 서술과 코드가 다르다.** SI S3: *"if the radii intersection a is lower than **30 % of the smallest radius**"*. 코드: 침투깊이 ≤ **0.3·(r_i+r_j)** = **반지름 합의 30 %**. r=4.0 과 r=0.75 쌍에서 SI 는 0.225 µm 허용, 코드는 **1.425 µm** = **6.3배 관대**하다. 실제로 `d_min = 0.7·4.75 = 3.325 < 4.0` 이므로 **작은 입자의 중심이 큰 입자 안으로 들어갈 수 있다.**
   - 겹친 부피는 복셀 union 으로 **한 번만** 세어진다 (`Im(Im>1)=1`) — SI 의 *"the overlapped AM fraction was considered only once"* 가 이것.
5. `randomSphere2.m:9-14` — `rmin_am == 0` 이면 **실험 PSD 파일**(`Distribution_diameter_emi_nmc111.dat`) 을 로드. **이때 `rmax_am = 4` 는 완전한 no-op** 이다(분포경로에서 rmax 를 안 씀). 위치는 `c = (dims − r)·rand + r` → **c ∈ [r, dims]**, 즉 구가 **+면으로만 삐져나오고 −면으로는 안 나온다**(비대칭).
6. **실패하면?** — `while` 루프에 **최대반복·타임아웃·수렴판정이 하나도 없다.** 목표 φ 에 도달 못 하면 **무한루프**다. SI 가 β=0.7 을 정당화하는 문장(*"at low porosities and high AM content, stochastic algorithms can be stuck"*)이 정확히 이 위험을 말한다 — 대책이 **겹침 허용을 늘리는 것뿐**이다.
7. ⚠ **생성된 구조의 porosity 는 한 번도 측정되지 않는다.** `ML__gap.m:46` 이 기록하는 `output_porosity` 는 다항식의 **목표값 `new_porosity`** 다. 사전충전이 목표를 넘겨버리면(§13 결함 B) 아무도 모른다.

> **우리와의 대비 (frame[1]/[2])**: 우리는 porosity 를 **산출**한다 — DEM 은 300 MPa servo 압밀 후 ε_sphere 로, MPM 은 `--protocol hold` 정지 두께에서. 여기는 porosity 를 **강제**하고 기하만 채운다. ⇒ 이 생성기는 **압밀 모델이 아니라 "주어진 φ 를 만족하는 무작위 배치기"**다. 압밀 물리는 전부 **실험 다항식 한 줄**에 응축돼 있고, 그래서 **외삽이 불가능**하다(다른 소재·다른 압력·다른 두께 = 식을 다시 재야 함). 우리 DEM/MPM 은 반대로 소재상수(E, σ_y)만 주면 새 조성에서 φ 를 낸다.

### 4.2 ★★ CBD 형태 파라미터화 — `AddSurf3.m` 의사코드 (질문 ②)

**두 스칼라 `probaId`(=SI 의 pB) / `probaAM`(=SI 의 pA) 가 cluster ↔ film 축을 만든다.**

```text
INPUT   IM      : 3D 라벨 배열 {0=pore, 1=AM, 2=CBD}
        N       : 추가할 CBD 복셀 수 (= φ_CBD · N_total)
        Id=2, Id_AM=1
        probaId, probaAM ∈ [0,1)
        method  : 'pixel' | 'voxel'

p_reject_AMonly ← probaId          # 코드: proba_Id ← 1 − probaId, 수용확률로 씀
p_reject_CBDonly ← probaAM
indPore ← find(IM == 0)            # ⚠ 루프 내내 갱신되지 않는다 (stale 허용)
i ← 0

while i < N:
    repeat:                                    # ── 거부 샘플링
        ind ← indPore[uniform_random]          # 균등 무작위 pore 후보
        if IM[ind] ≠ 0: continue               # 이미 채워진 자리면 다시
        nb ← 26-neighbourhood(ind)             # 경계에서 잘림 (주기 아님)
        if all(IM[nb] == 0): continue          # ★ 고체에 안 닿으면 무조건 기각
                                               #    ⇒ CBD 는 공극 한복판에서 핵생성 못 한다
        touches_CBD ← (Id   ∈ IM[nb])
        touches_AM  ← (IdAM ∈ IM[nb])
        if   not touches_CBD:  accept with prob (1 − p_reject_CBDonly)   # AM 에만 닿음
        elif not touches_AM :  accept with prob (1 − p_reject_AMonly)    # CBD 에만 닿음
        else               :  accept with prob 1                         # ★ AM·CBD 둘 다 = 무조건
    until accepted

    if method == 'pixel':                      # 논문이 쓴 모드
        IM[ind] ← Id ;  i ← i + 1              # 정확히 한 복셀
    else:  # 'voxel'
        void ← {n ∈ nb : IM[n] == 0}
        IM[ind ∪ void] ← Id ;  i ← i + 1 + |void|      # 최대 27 복셀 뭉치
```

**왜 이 두 확률이 형태를 만드는가 (기전):**
- `probaId` ↑ → **AM 에만** 닿는 자리가 자주 기각 → CBD 는 **이미 있는 CBD 옆에만** 자란다 → **덩어리(cluster)**.
- `probaAM` ↑ → **CBD 에만** 닿는 자리가 자주 기각 → CBD 는 **항상 AM 을 물고** 자란다 → **막(film)**.
- **AM·CBD 를 동시에 접하는 자리는 무조건 수용** → 삼중선(triple line)이 항상 전진 = 막이 AM 표면을 따라 **퍼져나가는 동력**.
- `probaId = probaAM = 0.5` (논문 설정) → 단일접촉 자리는 절반 수용, 혼합자리는 전부 수용 = **AM/CBD 경계선 편향의 중간 거동**.
- ⚠ **`probaId = 1` 은 데드락**이다. 시작 시점에 CBD 가 하나도 없으므로 모든 후보가 "CBD 미접촉" → 수용확률 0 → `repeat` 무한루프. **시드 메커니즘이 없다.** Script_Main 주석의 "Number between 0 and 1" 은 상한 포함이 아니다.
- ⚠ Mistry 2018(ACS AMI, SI ref 5)은 **에너지맵 + 계수 ω 하나**로 같은 축을 만든다. 여기는 **접촉종류별 거부확률 두 개**로 바꾼 것 — 에너지 모델이 필요없다는 게 장점이고, 대신 **물리적 의미가 없는 순수 형태 노브**라는 게 단점이다(표면에너지·건조속도 같은 실험량과 연결되지 않는다).

> **우리에게 왜 값진가**: 우리 `seed_sdcp` / `seed_sheath` / `additive_dispersion` 은 **위치 분산**은 다루지만 **형태 축(film↔cluster)이 없다**. 위 알고리즘은 phase grid 위에서 **20줄이면 이식**되고, 우리 STEP3 σ_e 는 첨가제 형태에 민감할 것이 확실하다(같은 부피, 다른 연결성). MIT 라이선스라 legal blocker 없음. ★ **단, 우리 격자에서 하려면 §5 의 함정을 반드시 함께 옮겨야 한다** — 형태 축을 스캔하는 것은 "표현부피가 참부피와 같다"는 전제 위에서만 뜻이 있다.

### 4.3 캘린더링 gap 이 기하에 들어가는 자리 (질문 ④)

**gap 은 기하에 *직접* 들어가지 않는다. 실험 다항식을 통해 ε_cal 로 바뀌고, ε_cal 이 (a) 박스 높이 (b) 상 부피분율 두 곳에 들어간다.**
```
gap ──[실험 다항식 §3.3]──► ε_cal ──┬──► z_box = 100·(1 − (ε_init − ε_cal))      (ML__gap.m:29)
                                     └──► φ_AM, φ_CBD = (1−ε_cal)·{...}          (ML__gap.m:40)
```
- 판정: **우리 `--protocol hold`(변위 정지)와 같은 부류인가? — 아니다, 더 약하다.**
  - 같은 점: 제어량이 **압력이 아니라 변위(gap)** 이고, 최종 상태가 **기하학적 정지조건**으로 정해진다.
  - 다른 점: 우리 `hold` 는 플래튼을 내리며 **재료가 응력을 쌓아** 300 MPa 에서 멈추는 **동역학**이 있다. 여기는 **동역학이 없다** — gap 은 오직 실험 회귀식의 입력숫자일 뿐이고, 압축 과정(재배열·소성·파쇄)은 **표현되지 않는다**. 압연 전후 구조 사이에 **어떤 연속성도 없다**(각 ε_cal 마다 완전히 새 박스를 처음부터 채운다).
- ★ **"정지 규약이 값을 정한다"는 우리 취약점을 공유하는가? — 취약점의 *종류*가 다르다.**
  - 우리(플래튼 정본 rev1–6): 정지 **프레임**이 porosity 를 정하고 속도 사다리에서 수렴하지 않는다 = **동역학이 있는데 정지 판정이 임의적**.
  - 그들: 정지 판정이 **실험식 한 줄**로 대체돼 있어 임의성이 없다 — 대신 **그 식 밖으로 한 발도 못 나간다**. T=100 µm 외삽(§3.3)이 정확히 그 대가다.
  - ⇒ **frame[5] 로 읽으면**: 그들은 "압밀 물리"를 아예 소유하지 않는다(실험에 outsource). 우리는 소유하지만 **정지 규약을 아직 못 닫았다**. 어느 쪽도 완결이 아니고, 우리 쪽이 **반증 가능**하다.

### 4.4 주기경계 (질문 ⑥)
- `Periodic_Condition_XYZ.m` — **x, y, z 세 축 전부**에 대해 경계를 넘는 구의 **거울 이미지를 추가**한다(`rowX1/X2, rowY1/Y2, rowZ1/Z2` 6면 전부 처리). `SliceV5.m:21-27` 에서 AM 에는 **2중 중첩 적용**(1차 이미지가 또 다른 면을 넘는 경우 처리), CBD 구에는 1회.
- ⚠⚠ **z 주기성은 이 물리에 맞지 않는다.** 코드 자신이 `z=1` 슬라이스를 **집전체(CC)**, `z=end` 를 **분리막**으로 읽는다(§4.5). z 를 주기로 감으면 위로 삐져나온 AM 캡이 **바닥(집전체 면)에 다시 나타난다**. §4.1 에서 본 대로 구는 **+면으로만** 삐져나오므로 이 되감김은 **한 방향으로만** 일어나 %CC-AM 을 계통적으로 부풀린다. (논문이 %CC-AM 의 큰 분산을 "AM 3–10 µm vs CC 50×50 µm² 라 표본이 작다"로만 설명한 것 — 그 설명은 맞지만 **전부는 아닐 수 있다.** 이 항목은 내 분석이고 논문은 언급 없음.)
- ⚠ **그리고 주기성이 배치에서 끝난다** — `AddSurf3`(CBD 성장), `Contact_pixel`(active surface), TauFactor 는 전부 **비주기**(경계에서 이웃이 잘림 / 측면 반사 BC). ⇒ **배치는 주기, 분석은 비주기** = 규약 불일치.
- **우리 대비 (#28 STEP3 periodic)**: 우리 periodic 은 **σ 솔브 자체**(x·y 측면)를 감고 z 는 집전체/분리막이라 **의도적으로 열어 둔다**. 즉 우리는 *분석*을 주기로 만들고 그들은 *배치*만 주기로 만들었다 — **정확히 반대**이고, 물리적으로 우리 규약이 맞다.

### 4.5 ★ 출력 4개의 실제 정의 (질문 ⑤) — 논문 서술과 코드가 어긋나는 자리

| Script_Main 변수명 | 실제로 받는 값 | 코드 정의 | 우리 대응 |
|---|---|---|---|
| `tortuosity_electrolyte` | ML__gap 출력 #1 ✓ | `TauFactor(im, PhaDir1).Tau_B3.Tau` — **phase 0 = pore**, **z 방향만** | τ_Laplace,bulk (TauFactor 카드 §매핑) |
| `tortuosity_solid` | 출력 #2 ✓ | `im(im==2)=1` **후** `Tau_W3` — **AM∪CBD 합친 상**, z 방향 | 우리엔 없음 (우리는 상별 σ) |
| `Percentage_CC_solid` | ⚠ **출력 #3 = `Percentage_CC_AM`** | `100·Σ(im(:,:,1)==1)/(nx·ny)` | 집전체 **접촉 면적분율** |
| `Percentage_Sep_electrolyte` | ⚠⚠ **출력 #4 = `Percentage_CC_CBD`** | `100·Σ(im(:,:,1)==2)/(nx·ny)` | 〃 (CBD) |

- ⚠⚠ **`Script_Main.m:25` 는 반환값 4개를 잘못 이름 붙인다.** `ML__gap.m:1` 의 출력 순서는 `[tortuosity_electrolyte, tortuosity_solid, %CC_AM, %CC_CBD, %Sep_electrolyte, IM]` 인데 Script_Main 은 앞 4개만 받으면서 3·4번째를 `Percentage_CC_solid`·`Percentage_Sep_electrolyte` 로 부른다 ⇒ **워크스페이스 변수 두 개가 실제로는 CC-AM 과 CC-CBD 다.** (파일로 쓰이는 텍스트 출력의 컬럼 헤더 `CC/AM CC/CBD El/Sep` 는 정확하다 — 오류는 진입점 스크립트에만 있다. 하지만 **진입점이 사용자가 보는 유일한 파일**이다.)
- ★★ **판정 (사용자 질문의 핵심): 이 두 값은 우리 `f_perc` / `electronic_active_fraction` 과 *대응하지 않는다*.**
  - 그들 것: **경계면 한 장(z=1)의 2-D 면적분율**. **연결성 검사가 0 이다.** 집전체 위에 떠 있는 고립된 CBD 섬 하나도 그대로 계수된다.
  - 우리 `electronic_active_fraction` (`network_conductivity.py:1046-1052`): 접촉 그래프의 연결성분 중 **바닥면(집전체)에 도달하는 성분**에 속한 입자 비율 = 3-D 그래프 연결성. `percolating_fraction` 은 바닥·상단 **둘 다** 닿는 성분.
  - ⇒ 대응관계는 **f_perc 가 아니라 우리 STEP3 의 "집전체 접촉 밴드"**(`step3_sigma.py` 의 bottom band Dirichlet 접촉 면적) 쪽이다. 그것도 우리는 밴드 규약(`wetted/primer` vs `0.5·vox+0.1` crown-only)을 따로 스캔하는데, 그들은 **한 복셀 층 = 접촉**으로 고정이다.
  - ⚠ `Percentage_Sep_electrolyte` (= `100·Σ(im(:,:,end)==0)/(nx·ny)`) 도 마찬가지로 **연결성 없는 면적분율**이다. 그 pore 가 전극 내부로 이어지는지 검사하지 않는다.
  - ★ 그리고 **TauFactor 는 percolation fraction 을 돌려주는데 코드가 버린다** (`.Tau` 만 읽음). 즉 이 파이프라인에는 **퍼콜레이션 판정이 존재하지 않는다.**
- **이웃 규약**: `findNeighboursSEI(…, 26)`(CBD 성장) 과 `findNeighboursMat26`(active surface) 둘 다 **26-이웃**(면 6 + 모서리 12 + 꼭짓점 8). 6-이웃 아님. `findNeighboursMat26` 은 `multiply_weight`(대각선 √2 가중)를 계산하지만 **쓰이지 않는다**.
- **active surface**: `Contact_pixel(im, 1, 0)` = `(고체에 26-인접한 고유 pore 복셀 수) / (고체 복셀 수) × 100`.
  - ⚠ **논문은 이것을 "% of AM surface in contact with the electrolyte" 라 부르지만**, 코드에서는 이미 `im(im==2)=1` 이 실행된 뒤라 **AM∪CBD 합친 고체의 표면**이다 (CBD–pore 계면 포함).
  - ⚠ 그리고 **분모가 표면이 아니라 고체 *부피*** 다 ⇒ 이것은 피복률이 아니라 **비표면적(S/V) 프록시**이고 원리상 100 % 를 넘을 수 있다.

### 4.6 ML — SISSO (질문 ⑦)
- 알고리즘 **SISSO**(Ouyang 2018) — 원 입력의 비선형 조합으로 descriptor 를 만들고 sparsifying operator 로 고른다. 연산자 집합(Eq. S3): `{I, +, −, ×, ÷, exp, log, |·|, √, ⁻¹, ⁻², ⁻³}`, **차원 n = 3**.
- **분할**: 440 포인트를 **80 / 20** train/test. test R² 는 **시드 5개 평균**. 추가로 **440 포인트 validation** 세트.
- **얻은 해석식** (SI Eq. S4–S8, 내가 docx OMML 에서 선형화 추출 — 기호 재현이므로 **재구현 시 원 SI 확인 필수**):
  - `τ_liq = (0.0013·(1−AM%)·ε_init³/AM%)·√P − 0.016·((AM%−2ε_init)/(AM%−ε_init))·(…) + 0.014·(…) + 1.56`
  - `τ_sol = (−30.52·lnP/(AM%−ε_init))·P^(1/9) + (60.97·√(lnP)/(AM%−ε_init) + ε_init/AM%) + 0.000067·CBD%²·(…) + 1.189`
  - `%CC-CBD = 0.018·AM%·CBD%·√ε_init·(…) − 0.961·CBD%·lnP + (CBD%·ε_init/ln ε_init) − 1.33`
  - `%CC-AM = 0.0351·ε_init·lnP·ε_init^(1/3) − √CBD%·(…) + 2.951·((AM%+CBD%−2ε_init)/(CBD%·P^(2/3))) − 0.00126·(e^(P/ε_init)·CBD%^(4/3))/P + 27.42`
  - `active surface = −0.005397·lnP·ε_init²·(…) − 0.011614·(AM%·ε_init/lnP) + (ε_init³/(CBD%−ε_init)) + 2.827·lnP − ln ε_init² + 97.15`
- **계산비용** (stated): 8,800 전극 생성+분석 ≈ **7일** (i7-8700 @3.2 GHz, 32 GB) / SISSO 학습 ≈ **24 h** (Xeon E5-2680v4 ×9, 128 GB).
- ⚠ CRediT 와 Table S2 헤더가 **DNN 도 학습했음**을 드러내지만("both test (DNN and SISSO)") **DNN 결과는 논문에 없다.**

**★ 우리 `ml_design_structure.py` 규율과 정면 대조 (판정)**

| 축 | 그들 (2020) | 우리 | 판정 |
|---|---|---|---|
| 교차검증 | 80/20 단일분할, 시드 5개 평균 | **해석적 LOOCV(hat) + 중첩 CV**(항·λ·기저족을 폴드 안에서 재선택) | **우리가 엄격** — 그들의 test R² 는 항·연산자 선택이 **분할 밖에서** 이뤄진 값이라 선택편향이 남는다 |
| n/k | 미보고 (SISSO 는 billions 후보를 스캔) | **탐욕 전방선택 + n/k ≥ 15:1** 강제 | **우리가 엄격** |
| 외삽 게이트 | 없음 | **leverage 외삽 게이트** | **우리가 엄격** |
| 불확실도 | 없음 (점추정 R² 만) | **Laplace 사후 PI + 경험 커버리지** | **우리가 엄격** |
| **타깃 축퇴 검사** | **없음** ← §7.3 | **있고 실제로 걸렀다**: `use_porosity_pct` REJECT (ε = C−φ_SE−φ_AM 항등식, raw 닫힘 1.0000±0.0000 ⇒ "φ 너머 정보 0", 학습·노출 금지) | **우리가 엄격, 그리고 결정적** |
| 유도량 곱항 | 무제한 (SISSO 연산자 전조합) | **자유노브 6개끼리로 제한**(`free_products=True`) — 유도량 곱 70개가 "정보 없이 후보만 늘리는 과적합 연료"임을 291 케이스로 실측 | **우리가 엄격** |
| **해석식 산출** | ★ **있다** (SISSO 가 식을 뱉는다 = 물리해석·전이 가능) | 우리는 σ 삼중항에 **스케일링법칙**(수기 물리형), 구조 예측은 회귀 | **그들이 앞선다** — 우리 구조 predictor 는 식을 안 뱉는다 |
| 차원해석 | ★ SISSO 가 **입력 차원을 명시적으로 취급** | 우리 회귀는 무차원화 안 함 | **그들이 앞선다** |
| 다목적 최적화 | 없음 (2023 논문에서 추가) | 순차 D-최적 배치제안 | 무승부 |

## 5. ★★ 해상도 감사 — CBD 표현부피 (질문 ①)

**`res = 1 µm/pixel` 인데 CBD 를 pixel 단위로 얹는다. 실물 CBD 는 nm 급이다. 세 겹으로 왜곡된다.**

### (a) 부피분율 자체는 **강제되므로 맞다** — 우리 CL-25 형 오차는 없다
`GenStructure_.m:12` → `N_bis = φ_CBD · N_total`, `AddSurf3` 는 `method='pixel'` 에서 **정확히 N_bis 복셀**을 채운다(i 가 1씩 증가). ⇒ 이미지의 CBD 복셀분율 = 목표 φ_CBD, **오차 0**.
★ 이것이 우리 SDCP 함정과 **결정적으로 다른 점**이다: 우리 SDCP 는 입자당 한 셀만 찍어 표현부피/참부피가 vox 0.4 → 0.15 에서 **4.311 → 1.866 → 1.090 → 0.238 (18.1배 변동, CL-25)** 했고, `--step3-sdcp-sphere-d`(참직경 구 스탬프)로 **0.986** 에 착지시켜 닫았다. 그들은 **부피를 카운트로 강제**해 이 축을 원천봉쇄했다 — 설계상 우수한 선택이고 우리가 배울 점이다.

### (b) ⚠ 그런데 **강제되는 그 목표 자체가 "나노공극 포함 domain"** 이다 — 전달축에서 ×1.9
`ML__gap.m:6` 의 **주석 없는 매직넘버**:
```matlab
ratio_mass = (compo(:,1)*0.95) ./ (compo(:,2)*4.65);   % = V_AM / V_CBD
```
⇒ **ρ_AM = 4.65 g/cm³** (NMC111), **ρ_CBD = 0.95 g/cm³**. 논문·SI 어디에도 이 값이 없다.
★ **같은 그룹의 자매논문이 이 숫자의 출처를 확정해 준다** — 우리 카드 `ngandjong2021_dem_calendering_digital_twin` §3(stated): *"ρ_CBD,solid **1.81 g/cm³** (CB+PVdF 평균), 압축 CBD 입자 ρ **0.95 g/cm³** → CBD **inner-porosity ≈ 47 %** (FIB-SEM)"*. 내 독립 산출도 같다: CB:PVdF=1:1 질량비, ρ_CB 1.8–2.1 / ρ_PVdF 1.78 → dense CBD **1.79–1.93** → `0.95/dense` = 0.49–0.53 ⇒ **내부 공극 47–51 %**.

| AM:CBD wt% | V_AM/V_CBD | **φ_CBD / φ_solid** |
|---|---|---|
| 93:7 | 2.714 | **26.9 %** |
| 94:6 | 3.201 | **23.8 %** |
| 95:5 | 3.882 | **20.5 %** |
| 96:4 | 4.903 | **16.9 %** |

⇒ **전달 관점의 표현부피비 = 1.81/0.95 ≈ ×1.9.** 이미지의 CBD 상은 실제 탄소+바인더 고체보다 **1.9배 큰 부피를 막는다**. ε_cal=33 %, 94:6 예: φ_CBD=0.159 중 **0.077 이 전해질로 채워졌어야 할 나노공극인데 불투과 고체로 그려진다** ⇒ 모델의 전해질 부피가 실제보다 **상대 23 % 부족**.
- ★ **그들은 이것을 인지하고 있고, 부분적으로 보고한다.** 본문 p.6 (stated): *"the calculation of τliq performed with TauFactor **does not take into account the microporosity of the CBD phase**, which is expected to affect the results herein reported. Indeed, this would imply a higher volume fraction of smaller pores, leading to an even more marked increase of τliq for high-CBD-content electrodes."*
- ⚠ **침묵하는 부분 3가지**: ① ρ_CBD=0.95 의 출처·의미가 **논문에도 SI 에도 없다**(코드 매직넘버) ② 크기를 **정량하지 않는다**(×1.9 는 내 산출) ③ **부호 주장이 논쟁적**이다 — 나노공극을 *전도상으로* 넣으면 전해질 상의 부피·연결성이 늘어 **합쳐진 이온경로의 τ 는 내려간다**(Ngandjong 2021 이 실제로 47 % 내부공극을 τ 계산에 **포함**시켜 τ_z ≈ 1.55–1.95 를 얻는다). 그들의 "τ_liq 가 더 오른다"는 **매크로공극만의 τ** 를 두고 하는 말이라 정의가 다르다. 논문은 그 구분을 하지 않는다.

### (c) ⚠⚠ **막 두께가 표현 불가** — film 끝이 원리적으로 막혀 있다
1 µm 복셀에서 **최소 CBD 특징 크기 = 1 µm 정육면체**다. 실물 CBD 막은 **~50–300 nm**.
- **AM 표면적 예산 (내 산출, 그들의 `active_surface`·`porosity_cal` 컬럼 사용, n=440)**: 1-복셀 두께 껍질로 덮을 수 있는 고체표면 비율의 **상한 = 23.9 – 65.8 %, 중앙값 39.0 %**.
- 같은 CBD 부피가 **150 nm** 실물 막이면 같은 면적을 **6.7배** 덮는다(= 완전 피복 + 잉여). **50 nm** 면 20배.
- ⇒ ★ **`probaAM → 1`(film 끝)을 아무리 밀어도 도달 가능한 피복률이 물리값의 1/3 이하에 갇혀 있다.** 형태 축 스캔은 **cluster 쪽 절반만 물리적으로 유효**하다. 이 논문은 `probaAM=probaId=0.5` 한 점만 썼으므로 **축을 실제로 쓰지도 않았다**(축을 만들어만 놓았다).
- **시각 증거**: Fig. S5 의 4개 생성구조에서 CBD(파랑)는 AM(빨강) 표면의 **막이 아니라 1 µm 얼룩**으로 흩어져 있다.

### (d) ⚠⚠ **d_h/dx ≈ 1.0** — 우리 규칙(≳3.5)의 1/3.5
우리 정본 규칙(`docs/se_curve_transfer_verdict_20260806.md` §⑤, 2026-08-06): `d_h/dx = (V_free/S)/dx ≳ 3.5` 여야 좁은 채널 물리를 믿을 수 있다. 실측 근거는 **3.43셀에서 격자 2.25배 정밀화 시 +4.0 % vs 1.18셀에서 +23.8 %**.
그들의 880행 전부에 대해 그들 자신의 컬럼으로 계산하면:
```
d_h = ε_cal / (active_surface·(1−ε_cal))  =  1.00 – 1.03 µm      (n=880, 중앙값 1.013)
d_h / dx = 1.00 – 1.03            (dx = 1 µm)
```
⇒ **모든 구조가 정확히 "채널 폭 1 복셀"** 이다. porosity 도 조성도 바뀌는데 d_h 가 안 움직인다는 것 자체가 **포화의 증거**다(§7.3 참조).
⚠ **자기비판**: 우리 3.5 규칙은 **MPM 응력 readout** 으로 교정됐고 τ 는 아니다. 기전의 부호도 반대다 — 역학에서는 미해상 협착이 사라져 재료가 통과(σ 과소), τ 에서는 미해상 목이 **끊겨** τ 과대. 그래서 이것은 **증명된 문턱이 아니라 자릿수 경고**로만 옮긴다. **그런데 아래 (e) 가 독립적으로 같은 결론을 준다.**

### (e) ★ 독립 교차검증 — 같은 그룹의 **실측 EIS** 대비 τ 가 2.4–2.7배 높다
| 출처 | 조건 | τ (= √tortuosity factor) |
|---|---|---|
| **이 논문**, AM96 | ε_cal 31–33 % | **3.30 – 3.77** (CSV, stated) |
| 이 논문, 전 조성 | ε_cal ≈ 31.5 % | 3.62 – 4.81 |
| **Ngandjong 2021** DEM (같은 그룹·NMC111·CBD 47 % 내부공극 **포함**) | ε = 31.5 % | ≈ 1.8 (digitized, **TREND only**) |
| **Ngandjong 2021 실험 EIS-TLM** | ε = 31.5 % | **1.3808** (stated) |

⇒ **같은 그룹이 같은 소재·같은 porosity 에서 실측한 τ 의 2.4–2.7배.** MacMullin 으로 보면 `N_M = tliq/ε_cal` = **10 – 73** (전형적 NMC 전극 실측 10–25) — 저 porosity 끝에서 완전히 벗어난다.
⚠ 완전 통제비교는 아니다(조성·구조생성기가 다르고 Ngandjong 은 DEM 물리압밀). 그러나 **(b) CBD 나노공극 미표현**과 **(d) 채널 1복셀**이라는 두 독립 원인이 **같은 방향**을 가리키고 실측이 그 방향에서 벗어나 있으므로, 판정은 명확하다: **τ_liq·σ_eff·N_M 의 절대값은 전이 금지, 추세만 사용.**

### (f) 그 밖의 해상도 부작용 (내 산출)
- **PSD 절단**: `sampleSpheresV2_opti.m:17` 의 `A(A>9)=[]` 가 직경 >9 µm 를 버린다 = **개수의 8.6 %** 인데 **측정 PSD 부피의 50.7 %**. 부피가중 중앙직경 **9.0 → 7.0 µm**. SI 는 *"explicitly considers the experimental AM particle size distribution"* 이라고만 쓰고 절단을 언급하지 않는다.
- **구 래스터화 손실**: `Slice_V3.m:27` 이 슬라이스별 반경을 `floor` 한다 ⇒ 해석부피 대비 복셀부피비가 **R=1.0 µm 에서 0.51, R=4.0 에서 0.67, PSD 가중 평균 0.694** (내 계산, 20개 sub-voxel z-offset 평균). 게다가 **비단조**(R=1.25 에서 1.06) ⇒ **PSD 의 *모양*이 왜곡된다**, 단순 축척이 아니다. 코드의 사전충전 계수 `1+res/3 = 1.333` 이 내가 계산한 필요배수 **1.44** 와 가깝다 — 이 손실을 알고 튜닝한 흔적이다(주석은 없다).
- **PSD 원자료** (`Distribution_diameter_emi_nmc111.dat`, SEM 계수): **409개** 직경 1.28–16.22 µm → 절단 후 **374개**, 0.25 µm 간격 반지름 빈 14개(0.75–4.00). **개수** 평균반지름 **2.16 µm**, **부피가중** 평균반지름 **3.18 µm**. 샘플링은 **개수빈도** 기준.

## 6. Figure set ★

| 그림 | 무엇을 보여주나 | 우리가 재사용할 것 |
|---|---|---|
| **Fig. 1** | 하이브리드 방법론 전체 흐름 A(실험/모델)→B(생성기)→C(데이터셋)→D(AI: regression/classification). 하단 A 에 **슬러리→건조→압연 CGMD 스냅샷**(파랑 CBD, 빨강 AM) | **우리 5-Phase 로드맵 그림의 원형.** 발표에서 "이 구조는 2020년에 published archetype 이 있다"의 근거 |
| **Fig. 2** | 캘린더링 특화 워크플로 (A 실험식 → B 생성기 → C 물성 → D/E ML 맵) | Fig. 1 의 구체판 |
| **Fig. 3** | **ε_cal vs P**, 4패널(ε_init 42/44/46/48 %), 곡선색 = AM 93→96 %. ε_init 42 %: 0.41→0.373(AM96)/0.39→0.349(AM93); ε_init 48 %: 0.40→0.331 / 0.378→0.305 (figure-read ≈, **TREND**) | ★ **압력-porosity 곡선의 실험앵커**(단 LIB·NMC111). 우리 Heckel P_y=138 MPa knee 와 비교 — 여기도 **~100 MPa 이후 포화** |
| **Fig. 4** | **τ_sol vs P**, 4패널. 1.30–1.55. P↑ → τ_sol↓; AM↑ → τ_sol↑. 각 십자에 ε_cal 병기 | 고체상 연결성의 압력의존. 우리 σ_e 와 **부호만** 대응(그들은 σ_e 를 안 낸다) |
| **Fig. 5 A–D** | **τ_liq vs P**, 2.0–5.2. P↑ → τ_liq↑, CBD 많을수록 가파름. ε_init 48 %·AM93 이 160 MPa 에서 τ≈5.1 (ε_cal 0.307) vs AM96 ≈3.2 | ★ **σ_ion↔압력의 반대부호 축**(LIB: 압축=이온 나쁨 / ASSB: 압축=이온 좋음). **위상 반전의 교과서 예시** |
| **Fig. 5 E–H** | **σ_eff vs ε_cal**, 0.02–0.11 S/m. σ_bulk(LP30)=1.119 S/m | N_M 계산의 원자료 |
| **Fig. 6** | **%CC-CBD vs P**, 12–24 %. AM 이 지배(ρ=−0.919), ε_init 영향 거의 없음, 압력에 **점근 포화** | 집전체 접촉저항 프록시 |
| **Fig. 7** | **active surface vs P**, 40–70 %. P↑ → AS↓ (압축하면 표면 잃음) | ⚠ §7.3 — 이 값은 **ε/(1−ε) 항등식**이므로 물리 정보가 없다 |
| **Fig. 8** | ★ **7 출력 × 4 입력 상관 요약맵** + 최적화 방향(min/max). 초록=정, 빨강=역, 원 크기=|ρ| | ★ **우리 comparison_vs_ours 요약그림의 좋은 서식.** 그리고 ε_cal 열의 큰 원들이 **타깃 축퇴의 시각 증거** |
| **Fig. S2** | gap↔압력 교정곡선 + **식 P = 189·exp(−gap/(0.21·T))** | 우리가 gap-제어 문헌을 압력축으로 옮길 때 쓸 수 있는 유일한 공개 교정식 |
| **Fig. S3** | NMC111 PSD 히스토그램 (직경 1–17 µm, 3–4 µm 최빈, n≈409) | 코드의 `.dat` 원자료와 **완전 일치** 확인 |
| **Fig. S4** | 허용 겹침 a 의 모식도 | ⚠ §4.1 — 이 그림의 정의(작은 반지름의 30 %)와 **코드(반지름 합의 30 %)가 다르다** |
| **Fig. S5** | ★ 생성 구조 4개 (50×50×~85–100 µm; 빨강 AM·파랑 CBD·초록 pore) | ★★ **1 µm 복셀의 시각 증거** — AM 이 구가 아니라 얼룩이고 CBD 가 막이 아니라 점이다 |

## 7. Post-processing ★

### 7.1 무엇을 쓰나
| 후처리 | 도구 | 어떻게 수치화 |
|---|---|---|
| τ_liq · τ_sol (·τ_am) | ★ **TauFactor** (Cooper 2016, litdb `taufactor_tortuosity_factor_tomography_tool`) InLine 모드 | `TauFactor('InLine',1,0,0, im, PhaDir, [1 1 1])` — **z 방향(dir 3)만**. 상매핑: `PhaDir` 행 1/2/3 = **black/green/white** = 라벨 **최소/중간/최대** |
| σ_eff (이온) | 수기 | **MacMullin** `N_M = σ_bulk/σ_eff = τ²/ε` (Eq. 1), σ_bulk = **1.119 S/m** (LP30 @25 °C) |
| %CC-AM · %CC-CBD | 수기 | z=1 슬라이스 면적분율 (§4.5) |
| active surface | `Contact_pixel.m` | 26-이웃 고체–pore 인접 (§4.5) |
| 통계 | 수기 | 조건당 **N=10 반복 평균**, SD 를 그림 캡션에 보고 |
| 상관 | Pearson + **PCA**(첫 2주성분 = 분산 85 %) | Table S3 / Fig. S10 |
| 다항회귀 선택 | **AIC** 최소화(4개 후보식 비교) + **Goldfeld-Quandt**(등분산) + **Durbin-Watson**(잔차 자기상관), 임계 10 % | SI S1b |

### 7.2 ★ 코드는 계산하는데 논문이 버리는 것
- **`tortuosity_am`** — AM 상만의 τ (`Tau_G3`). 텍스트 출력 `tam` 컬럼에 **기록되지만** 공개 CSV 에도 논문에도 **없다**.
- **`Percentage_Sep_electrolyte`** — 분리막 면 pore 분율. 출력 파일 `El/Sep` 컬럼에 있으나 **논문 분석 없음**, Script_Main 은 **받지도 않는다**(§4.5).
- **TauFactor 의 percolation fraction** — 반환되지만 `.Tau` 만 읽고 버린다 ⇒ **퍼콜레이션 판정 부재**.

### 7.3 ★★ 발견 — `active_surface` 는 물리량이 아니라 **항등식**이다 (내 산출)
880행 전부에 대해:
```
active_surface  ≈  100 · ε_cal / (1 − ε_cal)
   R² = 0.9964 ,  잔차 평균 −0.73 %p , sd 0.40 %p , 최대 |1.71| %p
   관측 40.90–72.80 %   vs   항등식 41.04–73.31 %
```
**뜻**: `Contact_pixel` 의 분자(고체에 인접한 고유 pore 복셀 수)가 **거의 모든 pore 복셀**이다 — 즉 **pore 상에 "속(bulk) 복셀"이 사실상 없다**. 1 µm 복셀·~4 µm 입자·33 % 공극에서 공극이 **어디서나 1복셀 두께 막**이라는 뜻이고, §5(d) 의 `d_h/dx ≈ 1.0` 과 **같은 사실의 두 표현**이다.
⇒ 세 가지가 따라 나온다:
1. **"AM 표면 중 전해질과 접한 %" 라는 해석이 성립하지 않는다** — 포화돼서 형태를 구별하지 못한다.
2. 그들 표의 **ρ(AS, ε_cal) = +0.997 은 물리가 아니라 대수**다.
3. SISSO 의 **R²(active surface) = 0.995 는 ε_cal 다항식을 재발견한 것**이다. τ_liq(0.976)·τ_sol(0.964)도 대부분 같다.
★ 우리 리포는 **정확히 이 종류의 함정을 이미 판정하고 닫았다**: `use_porosity_pct` REJECT — "porosity 는 회귀 말고 **ε = C − φ_SE − φ_AM 로 계산**(raw DEM 닫힘 1.0000±0.0000 = 정확한 항등식 → φ 너머 정보 0)". 같은 교훈, 독립 도달. **frame[4] 식으로 말하면 이것은 우리 ML 규율의 외부 검증이다.**

## 8. 우리 DEM+MPM 대비 → `our_dem_baseline.md`

### 8.1 같은 것
- **목표 구조가 같다**: 제조변수 → 미세구조 → 물성 → ML 해석식. 우리 5-Phase 로드맵과 동형(2020년판).
- **τ 를 voxel Laplace 로 푼다** — 그들 TauFactor, 우리 STEP3 `voxel_conductivity.py`/`step3_sigma.py` (∇·(σ∇φ)=0 유한체적). **같은 종류의 계산**이고 TauFactor 카드가 이미 매핑을 확정해 뒀다(그들 τ ↔ 우리 **τ_Laplace,bulk**, Holm 협착 **없음**).
- **압력 포화**: 그들 ε_cal 이 ~100 MPa 이후 평평 ↔ 우리 Heckel **P_y = 138 MPa** knee, Bazzoun σ-vs-P 400 MPa 포화. **세 독립 소스가 같은 자릿수**.
- **CBD/첨가제 형태가 성능을 좌우한다는 전제** — 그들 probaId/probaAM, 우리 SDCP/VGCF/PTFE 배선.

### 8.2 다른 것 (그리고 왜)
| 축 | 그들 | 우리 | 왜 |
|---|---|---|---|
| **porosity** | **입력** (실험 다항식이 정함) | **산출** (DEM servo 압밀 ε_sphere / MPM `hold` 정지) | 그들은 압밀물리를 실험에 outsource. **소재를 바꾸면 식을 다시 재야 한다** |
| **입자 취급** ★ | **강체 구, 소성 0**. 게다가 겹침 β=0.7 을 **속도를 위해** 허용 (물리적 소성 아님) | DEM = 강체 구 + **접촉** 소성(hooke/hysteresis, E_eff **1.35 GPa** = 18배 연화) / MPM = **진짜 형상 소성**(J2, E_eff 1.53, σ_y 0.15) | frame[1]/[2]. 그들의 "겹침"은 δ-프록시조차 아니고 **탐색 가속 장치**다 |
| **이온 위상** | pore = 전해질 = 이온전도체. **압축 = 이온 나쁨** | pore = 절연. SE = 이온전도체. **압축 = 이온 좋음** | ⚠⚠ **부호가 반대다.** τ_liq·σ_eff·N_M 의 **어떤 절대값도 우리로 전이 불가** |
| **σ 삼중항** | **이온만**(그것도 τ→MacMullin 환산). σ_e·k_thermal **없음** | σ_ionic + σ_e + σ_thermal (접촉망 Kirchhoff/Holm **및** STEP3 복셀 FV) | **우리가 앞선다** |
| **접촉망** | 없음 (복셀 연속체뿐) | DEM 접촉망 = 접촉당 Holm 협착 1/(2σr_c) + Stage-E 소성면적 | **우리가 앞선다** |
| **퍼콜레이션** | **판정 자체가 없다** (TauFactor 의 percolation 을 버림) | f_perc·electronic_active_fraction·percolating_fraction | **우리가 앞선다** |
| **해상도** | 1 µm/voxel 고정, **수렴 시험 0** | 격자 사다리 상주(128/192/288, vox 0.4/0.3/0.25/0.15/0.125/0.115), `d_h/dx ≳ 3.5` 규칙, 표현부피 원장 | **우리가 크게 앞선다** — 그리고 우리도 **아직 수렴 못 했다**(CL-41: 이득 +12.32/+14.38/+15.54 % 가 vox 0.15/0.125/0.115 에서 **단조 증가, 멱법칙 미성립, 외삽 무의미**) ⇒ 우리는 그 사실을 **보고**하고 그들은 시험하지 않았다 |
| **실험 앵커** | ★ **54셀 + 29셀, 조건 완전기록** | pure-SE Minnmann 10 %@300 MPa, Cronau overlap, Bazzoun EIS | **그들이 앞선다**(캘린더링 압력-porosity 다점 실측) — 단 LIB 소재 |
| **ML 해석식** | ★ **SISSO 가 식을 뱉는다** | 우리 구조 predictor 는 식 없음 | **그들이 앞선다** |
| **ML 규율** | 단일분할·축퇴 미검사 | 중첩 CV·n/k 15:1·leverage 게이트·PI 커버리지·**타깃 축퇴 판정** | **우리가 앞선다** |

### 8.3 ⚠ 전이 판정 (혼동 방지 — 무엇이 진짜 차이이고 무엇이 방법 인공물인가)
| 관측 | 판정 |
|---|---|
| 그들 τ_liq(2–6) ≫ 우리 τ_Laplace | ⚠ **방법 인공물 + 위상 반전 둘 다**. ① pore-τ 와 SE-τ 는 **다른 상**이다 ② 그들 τ 는 §5(e)에서 실측 대비 2.4–2.7배 과대 |
| 그들 ε_cal(29–42 %) ≫ 우리 ASSB(10–16 %) | **진짜 차이** — LIB 는 전해질이 공극을 채우므로 30–40 % 를 **원한다**. ASSB 는 공극이 곧 손실 |
| 그들 "압력↑ → 이온 나쁨" vs 우리 "압력↑ → 이온 좋음" | **진짜 차이 (위상 반전)**. 인용할 때 반드시 병기 |
| 그들 active surface 40–70 % vs 우리 coverage 48–52 % | ⚠ **비교 금지** — 그들 값은 항등식 ε/(1−ε)(§7.3), 우리 것은 Tabor/Hertz 밴드 기하 피복률. **다른 양이다** |
| 그들 %CC-AM/CBD vs 우리 f_perc | ⚠ **대응 아님**(§4.5). 우리 STEP3 집전체 밴드와 견줄 것 |
| ~20 % 가 강체구 floor 라는 우리 명제 | 그들은 **porosity 를 입력**하므로 이 명제를 **시험할 수 없다** — 반례도 증거도 아님 |

## 9. 적용 인사이트 (우리 모델에 무엇을 할 것인가)

1. ★★ **`probaId/probaAM` 형태 축을 우리 첨가제 배치에 이식** (MIT, 20줄). 후보 진입점: `seed_sdcp` / `seed_sheath` / `additive_dispersion`. 스캔 = `{cluster, mixed, film} × {SDCP, VGCF}` 에서 **STEP3 σ_e 감도**. ⚠ **전제조건**: 우리는 이미 `--step3-sdcp-sphere-d` 로 **표현부피를 0.986** 에 고정했으므로 형태 축이 부피 축과 교란되지 않는다 — 그들에겐 그 보장이 없다(§5c). **부피를 고정한 채 형태만 바꾸는 것**이 이식의 핵심 계약이고, `--compare-dir --expect-differ` 로 강제할 것.
2. ★ **타깃 축퇴 진단을 우리 predictor 에 상주시킨다.** §7.3 을 일반화: 학습 전에 **각 타깃이 다른 타깃/입력의 대수적 함수인지** 검사하고 R² > 0.99 면 회귀 금지·항등식 사용. 우리는 `use_porosity_pct` 하나를 수동으로 잡았는데, **자동 게이트**로 만들 근거가 이 논문이다(그들은 못 잡아서 R²=0.995 를 물리로 보고했다).
3. ★ **`d_h/dx` 사전점검을 문헌 카드에도 적용한다.** 이번에 그들 CSV 두 컬럼만으로 d_h/dx ≈ 1.0 이 나왔다 = **논문의 원자료만으로 해상도 신뢰성을 판정하는 절차**가 성립한다. 우리 규칙(≳3.5)을 문헌 스크리닝 체크리스트로 승격할 것.
4. **Fig. 8 형식의 요약 상관맵**을 우리 comparison_vs_ours_DEM 의 각 축(A–G) 헤더 그림으로 채택 검토.
5. ⚠ **하지 말 것**: 그들의 τ_liq·σ_eff·N_M·active surface 절대값을 우리 표에 올리는 것. ε_cal–압력 곡선(Fig. 3)만 "LIB 대조군"으로 인용 가능.

## 10. 인용 가능 문장 (deck/paper용)

- "Duquesnoy et al. (J. Power Sources 480, 229103, 2020) combined 54 calendered NMC111 electrodes with a stochastic voxel mesostructure generator and SISSO symbolic regression, producing 8,800 in-silico electrodes and closed-form input–property equations — the published archetype of the manufacturing-to-property ML loop."
- "In that work the **porosity is an input**: an experimentally fitted 5-D polynomial (R² = 0.97) maps (AM wt%, ε_init, thickness, roll gap) to ε_cal, and the generator then fills a box to that target. Compaction mechanics is outsourced to the regression, so the model cannot extrapolate to a new material system. Our DEM/MPM instead **computes** porosity from material constants."
- "Their generator resolves the carbon-binder domain at **1 µm/voxel** while a real CBD film is 50–300 nm. With their own reported CBD-domain density (0.95 g/cm³ vs 1.81 g/cm³ dense, i.e. ~47 % internal nanoporosity), the represented, transport-blocking CBD volume is **≈1.9×** the true solid, and a one-voxel shell can cover at most **~25–40 %** of the AM surface."
- "The paper explicitly acknowledges that TauFactor 'does not take into account the microporosity of the CBD phase', but does not quantify it; consistently, the resulting tortuosities are **2.4–2.7× the same group's own EIS-derived τ** for the same material at the same porosity (Ngandjong et al. 2021, τ_TLM = 1.38 at ε = 31.5 %)."
- ⚠ 내부용(원고 금지, 우리 분석): "Across all 880 published data points the reported *active surface* equals 100·ε/(1−ε) with R² = 0.996 — it is an algebraic restatement of porosity, not an independent microstructural descriptor; the ML R² of 0.995 on that target is therefore not evidence of learned structure–property physics."

## 11. 주의 / 한계 (over-claim 방지)

1. ⚠⚠ **소재계가 다르다** — NMC111 + **액체 전해질 LIB**. 우리 LPSCl/NMC811 ASSB 와 **이온 위상이 반대**(pore 가 전도체 vs 절연체). **방법론 전이 / 값 비전이.**
2. ⚠ **강체 구 · 소성 0**. 겹침 β=0.7 은 물리가 아니라 **탐색 가속**이다. Varkey 2026 조차 "contact 소성"은 있었는데 여기는 그것도 없다. frame[1] 의 빈칸을 **더 크게** 갖는다.
3. ⚠ **격자 수렴 시험이 없다** — 1 µm 단일 해상도, 논문·SI·코드 어디에도 res 스윕이 없다. §5(d)(e) 로 볼 때 절대값은 신뢰구간이 없다.
4. ⚠ **생성 구조의 porosity 가 측정되지 않는다** — 보고되는 것은 **목표값**이다(§4.1-7). 사전충전 초과(§13-B)를 검출할 수단이 없다.
5. ⚠ **T = 100 µm 외삽** — 실험 138–180 µm 밖. ε_cal 이 +10.3 %p 계통 이동(§3.3). 논문 미언급.
6. ⚠ **질량 비보존 두께식** — 최대 +12.2 % 로딩 드리프트(§3.3). 논문 미언급.
7. ⚠ **validation 세트가 같은 격자의 보간**이다(§3.4) ⇒ R² 0.98–0.995 를 "일반화 성능"으로 읽으면 안 된다.
8. ⚠ **타깃 축퇴**(§7.3) — 출력 7개 중 5개가 ε_cal 의 매끄러운 함수. 실질 학습 대상은 1 차원 + %CC-AM 이고, 후자는 실패(0.766)했다.
9. ⚠ **문서-코드 불일치 4건**: SI Eq. S2 두께항 **부호 오타** / SI 의 겹침 정의(작은 반지름 30 %) vs 코드(반지름 합 30 %, **6.3배 관대**) / 논문의 "AM surface" vs 코드의 **AM∪CBD surface** / Script_Main 반환값 **이름 2개 오류**.
10. ⚠ **SI 내부 불일치**: 본문 54 electrodes vs SI 66; Table S3 대칭성 오타 1건; SI 그림번호 "S2" 중복.
11. ⚠ **digitized 표시**: Fig. 3/4/5/6/7 에서 읽은 수치는 전부 **figure-read ≈ TREND only**. CSV 에 있는 값(§3.4)은 stated.
12. **우리 쪽 정직**: 우리도 격자 수렴을 못 닫았다(CL-41 — vox 0.15/0.125/0.115 에서 이득 **+12.32 / +14.38 / +15.54 %**, 증분비 1.773 이라 `R=R∞−C·h^p` 가 요구하는 최소 2.187 을 만족하는 **p>0 이 없다** ⇒ Richardson 외삽 무의미, 보고값은 **하한**). 차이는 **우리는 사다리를 돌리고 보고했다**는 것뿐이다. 이 카드의 §5 비판은 그 자각 위에서만 유효하다.

## 12. 데이터셋 재사용 판정 ★

**판정: 재사용 가능 — 단 "생성기 응답면"으로만. 실험 데이터로 취급 금지.**

| 파일 | 행 | 재사용 |
|---|---|---|
| `mmc2.xlsx` NON-CALENDERED | **29** | ✅ **실측**. AM/CB/PVdF·solid content·두께·porosity. 우리 "건조 후 초기 porosity" 문헌값으로 인용 가능(LIB) |
| `mmc2.xlsx` CALENDERED | **54** | ✅ **실측**. gap(1/5/25/27/44/100 µm) → 두께 → porosity. ★ **gap-제어 압밀의 공개 원자료** — 드물다 |
| `mmc3.csv` | **440** | 🔶 **모델 출력**. `tliq/tsol` = tortuosity **factor**(√ 필요), `porosity_cal` = **목표값**, `active_surface` = **ε/(1−ε) 항등식** |
| `mmc4.csv` | **440** | 🔶 위와 같음 + **독립 검증세트 아님**(같은 격자 보간) |
| `Distribution_diameter_emi_nmc111.dat` | **409** | ✅ **실측 NMC111 PSD**(SEM 계수). 우리 PSD 문헌 대조에 바로 사용 가능. ⚠ 코드가 >9 µm 를 버린다는 점 유의 |
| MATLAB 소스 21파일 | 34 KB | ✅ **MIT License — 개작·재배포·상업이용 가능**(저작권 고지 유지). §4.2 알고리즘 이식에 법적 장애 없음 |

## 13. ★ 코드 결함 원장 (내가 잡은 것 — 크기까지 정량)

| # | 위치 | 결함 | 크기 (내 산출) |
|---|---|---|---|
| **A** | `Script_Main.m:25` | 반환값 3·4번을 `Percentage_CC_solid` / `Percentage_Sep_electrolyte` 로 오명명. 실제는 **CC_AM / CC_CBD** | **치명(사용자 대면)** — 텍스트 출력 헤더는 정확 |
| **B** | `sampleSpheresV2_opti.m:29-31` | 사전충전이 해석부피 1.333N 을 채운 뒤 `n=#(Im==1)` 을 세는데, 이때 **최소반지름 구가 SliceV5 에서 라벨 2(CBD)로 찍혀 있어** n 에서 빠진다. 이후 `Im(Im>1)=1` 이 그것들을 AM 으로 되돌려 **목표 초과**가 가능 | **작다** — 최소빈(r=0.75)이 개수 **1.6 %**, 부피 **0.043 %**, 구당 ~1.5 복셀 ⇒ AM 부피 초과 **≲0.05 %**. **하지만 검출수단이 없다**(porosity 미측정) |
| **C** | `SliceV5.m:8-16` | `length(unique(radius))>1` 이면 **최소반지름 구 전부를 CBD 로 분류**. 이 파이프라인에서는 CBD 를 구로 넣지 않으므로 **오발화** | B 와 동일 사건. 다른 사용경로에서는 의도된 분기 |
| **D** | `findNeighboursMat26.m:102-103` | `temp = NeighboursInd(:,2) − NeighboursInd(:,1)` 로 **이웃의 선형인덱스**와 **입력 리스트의 행번호**를 뺀다(범주 오류). `temp<0` 행을 삭제 → 이웃쌍 일부 소실 | **작다** — `list1(i)−i`(i번째 고체 앞의 비고체 개수)가 최대 오프셋 nx·ny+nx+1≈2551 을 넘으면 무효화되므로, 33–42 % 공극에서 **리스트 앞 ~5 % 구간만** 영향. **위치가 z≈0(집전체 면)에 몰린다.** active_surface 잔차 **−0.73 %p**(§7.3)의 일부가 이것 |
| **E** | `AddSurf3.m:19-42` | `probaId = 1` 이면 **무한루프**(CBD 시드 없음). 문서는 "0 to 1" | **치명(도달 가능)** — 형태 축 스캔의 한쪽 끝이 막힘 |
| **F** | `AddSurf3.m:12` | `indPore` 를 루프 밖에서 한 번만 계산 → 채워진 자리를 계속 뽑는다(`IM(ind)==0` 로 걸러냄) | 성능만 (O(N²) 경향) |
| **G** | `AddSurf3.m:43,45` | `sum(method=='pixel')==5` 문자열 비교 — 길이가 다르면 **MATLAB 오류** | 견고성 |
| **H** | `Contact_pixel.m` | `multiply_weight`(대각 √2) 를 계산하고 **안 쓴다**. 26-이웃을 등가중 취급 | 정의의 문제(의도적일 수 있음) |
| **I** | `ML__gap.m:29` | 두께 갱신이 **질량 비보존** (§3.3) | **최대 +12.2 %** 로딩 드리프트 |
| **J** | `ML__gap.m:20` | 다항식에 **박스 높이(100 µm)** 를 전극 두께로 대입 = 교정범위 밖 외삽 | **ε_cal +10.3 %p** 계통 이동 |
| **K** | 전역 | `sampleSpheres`/`AddSurf3` 의 `while` 에 **최대반복·타임아웃 없음** | 무한루프 위험(SI 가 스스로 언급) |
| **L** | `Script_Main.m:19` | `rmax_am = 4` 는 `rmin_am = 0`(실험 PSD) 경로에서 **완전 무시** | 사용자 오해 유발 |

## 14. 상호참조

- **`duquesnoy2023_ml_multiobjective_manufacturing_optimization`** (EnSM 56, 50–61, DOI 10.1016/j.ensm.2022.12.040) — **같은 1저자·같은 그룹의 3년 뒤 후속. 다른 논문이다.**

  | | **2020 (이 카드)** | **2023** |
  |---|---|---|
  | 구조 생성 | **확률적 voxel 배치기**(실험 다항식이 φ 를 강제) | **물리기반 사슬** CGMD 슬러리 → 건조 → **DEM 압연** |
  | 공정변수 | AM% · ε_init · **롤 gap**(→압력) | AM% · **SC%**(슬러리 고형분) · **CD%**(압축률) |
  | DOE | **완전 factorial** 10×4×11 | **Sobol/Saltelli space-filling** |
  | ML | SISSO (해석식) | SISSO **+ 베이지안 다목적최적화**(GP + GP-Hedge) |
  | 출력 | τ_liq · τ_sol · %CC-AM/CBD · active surface | tortuosity · **σ_e** · active surface · density |
  | 루프 닫힘 | ✗ (맵만 제시) | ✅ **역설계 → 실제 전극 제작 → 실험 검증** |
  | 전달 계산 | TauFactor (τ만) | **GeoDict**(σ_e 포함) |
  ⇒ **2020→2023 에서 바뀐 것**: ① 구조 생성이 **경험식 → 물리 시뮬**로 ② DOE 가 격자 → **space-filling** 으로(⇒ §3.4 의 "validation=보간" 문제 해소) ③ **σ_e 가 추가**(2020 은 이온만) ④ ML 이 **기술(descriptive) → 최적화(prescriptive)** 로 ⑤ **실험 재현 검증**이 붙음. **바뀌지 않은 것**: SISSO, NMC111+CBD 액체 LIB, 접촉망 부재, 격자 수렴 미시험.
- **`taufactor_tortuosity_factor_tomography_tool`** (Cooper 2016, SoftwareX) — **이 코드가 실제로 호출하는 외부 툴**(`Script_Main.m` 주석: *"To operate, please launch the App TauFactor first"*). 그 카드의 매핑이 여기 그대로 적용된다: TauFactor τ ≡ 우리 **τ_Laplace,bulk**, **Holm 협착 없음**. 그 카드가 경고한 **voxel 표면적 과대추정(단일구=단일복셀 → SA ×2, 다복셀 구 → 최소 ×1.5)** 이 §5·§7.3 의 정확한 근본원인이다 — 즉 **툴 카드가 3년 전에 예고한 함정을 이 논문이 밟았다.**
- **`ngandjong2021_dem_calendering_digital_twin`** — 같은 그룹·같은 소재·같은 해의 **DEM 압연 물리 모델**. ★ ρ_CBD 0.95 / 1.81 / 내부공극 47 % 의 **출처**이자, §5(e) τ 교차검증의 **실측 상대**(τ_EIS-TLM = 1.3808 @ε=31.5 %).
- **`alabdali2023_cgmd_wet_manufacturing_ssb_cathode`** — 같은 그룹이 이 방법을 **ASSB 로 옮긴** 버전 (구형 AM, GeoDict).
- **`lim2025_virtual_calendering_framework`** · **`lyu2025_3d_dem_drying_calendering_lib`** · **`sangros2019_dem_calendering_lib_electrode`** · **`schreiner2020_dem_calendering_lib`** — 캘린더링 계보. 이들은 **압밀을 물리로 푼다**; 이 논문만 **실험식으로 우회**한다.
- **`varkey2026_multicontact_dem`** — "elasto-plastic 이라 쓰지만 강체구"의 다른 예. 이 논문은 **그보다도 아래**(접촉법칙조차 없음).
- **`cronk2026_lis_positive_electrode_geometry_fem`** — 이 논문을 **ref 67** 로 인용.
- Mistry, Smith, Mukherjee, *ACS Appl. Mater. Interfaces* **10** (2018) 6317 — SI ref 5. **film↔cluster 를 계수 ω 하나로** 다룬 선행. §4.2 알고리즘의 직접 조상. (아직 우리 litdb 에 없음 — 첨가제 형태 축을 이식하면 digest 후보.)
- Laue, Wolff, Röder, Krewer, *Energy Technology* (2020) — SI ref 4. **ASSB 전극의 mixing 전략 → 미세구조** 확률 생성기. 저자들이 "우리 방법과 유사"라고 지목. (litdb 미보유, ASSB 라 우선순위 높음.)

---

## 🗨️ Q&A 로그

**Q. (2026-09-03) `res = 1 µm/pixel` 인데 CBD 를 pixel 단위로 넣는다 — 표현부피/참부피는?**
A. §5. 세 층으로 나눠야 한다. **① 부피분율은 정확하다**(카운트로 강제, 우리 CL-25 형 오차 없음 — 오히려 우리보다 안전한 설계). **② 그러나 목표 자체가 나노공극 47 % 를 포함한 CBD *domain* 부피**이고 그 전체가 불투과 고체로 그려진다 ⇒ 전달 관점 표현부피비 **≈×1.9**. **③ 그리고 1 µm 최소 특징크기 때문에 막 두께가 표현 불가** ⇒ 같은 부피로 덮을 수 있는 AM 표면이 실물의 **1/3~1/7** (내 산출: 상한 23.9–65.8 %, 중앙값 39.0 %). 저자들은 **②를 정성적으로만 인정**하고(본문 p.6, τ_liq 에 한해) **①③ 은 언급하지 않으며**, ρ_CBD=0.95 라는 매직넘버는 논문·SI 어디에도 없다(자매논문 Ngandjong 2021 에만 있다). 결과 검증: 그들 τ 는 같은 그룹 실측의 **2.4–2.7배**, 그들 자신의 컬럼으로 계산한 **d_h/dx ≈ 1.0**.

**Q. porosity 가 입력이면 실패하면 어떻게 되나?**
A. **무한루프다** (§4.1-6, §13-K). 최대반복도 타임아웃도 수렴판정도 없다. SI 가 겹침 β=0.7 을 "안 그러면 stuck 된다"로 정당화하는 문장이 그 위험의 자백이다. 그리고 성공하든 실패하든 **생성 구조의 porosity 는 한 번도 측정되지 않는다** — 보고값은 다항식의 목표다.

**Q. 이 논문의 압력축은 우리 `--protocol hold` 와 같은 부류인가?**
A. §4.3. **변위(gap) 제어라는 점은 같지만 동역학이 없어 더 약하다.** 우리 `hold` 는 재료가 응력을 쌓다가 멈추고, 그래서 **정지 프레임이 값을 정한다는 우리 취약점**이 생긴다. 그들은 그 단계를 **실험 회귀식으로 대체**해 임의성을 없앤 대신 **식 밖으로 못 나간다**(T=100 µm 외삽이 그 대가). 어느 쪽도 완결이 아니지만 **우리 쪽이 반증 가능하다**.

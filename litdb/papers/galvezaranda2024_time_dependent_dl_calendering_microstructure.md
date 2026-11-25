<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md / vijay2025_hybrid_cgmd_dl_slurry_microstructure.md -->
# **압연(calendering) DEM 궤적**을 1D-CNN 시간-surrogate 로 대체하다 — 3 프레임 lag → 다음 프레임 3D 복셀 미세구조, NMC111 96 % / CBD 4 %, CD 20–50 % — Galvez-Aranda / Le Dinh / **Vijay** / Zanotto / Franco (Advanced Energy Materials 2024)

> slug `galvezaranda2024_time_dependent_dl_calendering_microstructure` · DOI `10.1002/aenm.202400376` · type `DL 시간-surrogate(1D-CNN, TensorFlow/Keras) on DEM 압연 궤적 + GeoDict DiffuDict 후처리` · PDF `main.pdf` (+ SI `si.pdf` + 보충영상 4편 mp4) · digested `2026-09-11` · status ✅

> elements: Li
> methods: elastic

---

## 0. 이 논문이 우리에게 *왜* 중요한가 — 그리고 **정확히 어디까지만** 중요한가 (positioning)

**한 문장**: 이것은 `vijay2025_hybrid_cgmd_dl_slurry_microstructure` 의 **자매편**이고,
그 카드가 *"우리 축과 직접 겹치는 것은 [Vijay25] 가 아니라 이쪽"* 이라고 지목한 바로 그 논문이다
(§12-1 · `comparison_vs_ours_DEM.md` F-DL3).  **지목은 옳았다 — 그러나 인용문은 절반만 사실이다.**

- **위치**: Franco 그룹(LRCS Amiens / ARTISTIC ERC)의 제조 디지털트윈 사슬에서
  **압연(DEM) 단계 위에 얹은 DL 한 층**.  물리 엔진은 전부 ref **[36] Xu 2023 (JPS 554, 232294)**
  소유이고, 그 계보 위쪽이 정본 카드 `ngandjong2021_dem_calendering_digital_twin` (= 본문 ref [25]) ·
  `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` (= 본문 ref [18]) 다.
  ⇒ **이 논문의 신규성은 DL 층 하나뿐이고, DEM 물리 파라미터는 한 줄도 안 적혀 있다.**
- **우리 축과의 겹침**: [Vijay25] 와 달리 **압밀(compaction) 단계 그 자체**를 다룬다 ⇒
  frame[5] 상 **우리 STEP1(DEM 압밀) · STEP2(MPM 압밀)와 같은 자리**다.  네 양
  (**접촉면적 · porosity · 확산도 · springback**)이 전부 **우리가 직접 재는 양**이다.
- ★★ **그러나 인용문 검증 결과 = 절반만 사실** (§3-A 전수 표):
  - **porosity ✅** (n=11 평균 상대오차 **3.45 %**, 최대 7.24 %) — 진짜로 예측한다.
  - **접촉면적 ⚠** (평균 **8.99 / 10.54 / 13.76 %**, 최대 **16.76 %**) — 예측하되 **네 양 중 가장 부정확**하고,
    게다가 **우리 Tabor/Stage-E 접촉면적과 같은 양이 아니다** (복셀 상-경계 면 수 ≠ 접촉당 A(δ)).
  - **확산도 ⚠⚠ — DL 이 예측하는 것이 아니다.**  DL 은 **복셀 격자 하나**만 뱉고,
    확산도·τ 는 그 격자 위에서 **GeoDict DiffuDict 유한체적 솔브를 따로 돌려** 얻는다.
    그 솔브 비용은 **논문 어디에도 없고 DL 이든 DEM 이든 똑같이 든다** ⇒ *"훨씬 낮은 비용"* 이 아니다.
  - **springback ⛔ — 숫자가 하나도 없다.**  *"remarkably capture"* 는 Fig 5b/6a/6c 의
    **부피궤적 육안 일치**가 전부다.  회복률 %, 두께 회복 µm, 오차 — **전무**.
    (우리가 그림에서 직접 뽑았다: §3-C, `derived(ours)` **CD 25/35/45 % 에서 4.8 / 7.6 / 10.1 %p**.)
- ⇒ **정정된 인용문**: *"DL 은 **압연 중 3D 복셀 미세구조 한 개**를 DEM 대비 188× 싸게 낸다.
  porosity·접촉면적은 그 격자에서 **세기만 하면** 나오고, 확산도·τ 는 **별도 FV 솔브가 더 필요**하며,
  springback 은 **정성적으로만** 재현됐다."*
- **⛔ 전이 금지**: **액체계 LIB**(NMC111 + C65 + PVdF, porosity = GOOD) · **압력 축 없음**
  (CD = 두께감소율 %) · **실험 신규 0건**(검증은 ref [36] 상속) · **DEM 물성 0건** ·
  σ 삼중항 0 · 소성 형상변화 0 · 데이터/코드 비공개(*"Research data are not shared"*).

---

## 1. 한 줄 요약

DEM 압연 시뮬레이션 **35 런 · 855 프레임**(4 + 1 전극 × CD 20/25/30/35/40/45/50 %)을 0.4 µm 복셀
(76×76×125 = **722,000 복셀**, 라벨 0=pore/1=CBD/2=AM/4=void)로 바꾸고, **직전 3 프레임 → 다음 프레임**을
학습하는 **1D-CNN**(663.7 M 파라미터, **150-차원 병목**)을 세워, 압연 전 구간의 미세구조 시계열과
**spring-back 까지** 재현한다.  검증은 (i) 복셀 R²(프레임당, 평균 ≈95 %) (ii) 상-쌍 접촉면적
(iii) GeoDict 로 낸 porosity·확산도·τ.  **DL 15 s/step vs DEM ≈47 min/step = 188×.**

---

## 2. 메타

| 저자 / 소속 | 지면 | DOI | 소재계 | 방법 |
|---|---|---|---|---|
| **Diego E. Galvez-Aranda**, Tan Le Dinh, **Utkarsh Vijay**, Franco M. Zanotto, **Alejandro A. Franco**\* — LRCS (UPJV, Amiens) / RS2E / ALISTORE-ERI / IUF | ***Advanced Energy Materials* 14, 2400376 (2024)**, 13 pp (접수 2024-01-23, 수정 02-16, 온라인 03-05, **open access CC BY**) | `10.1002/aenm.202400376` | **NMC111 96 wt% + C65 2 wt% + PVdF 2 wt%** (= 시뮬 상으로는 **AM 96 % + CBD 4 %**), **액체계 LIB 양극** | **1D-CNN**(TensorFlow 2 / Keras, Python 3.9, Adam, Optuna 500 trial) 위에 **DEM 압연**(ref [36] Xu 2023) 데이터.  전달물성 = **GeoDict 2023 DiffuDict**(Math2Market).  가시화 = **OVITO** |
| 구성 | Fig 1–7 · Table 1–3 · refs 51 · SI = Table S1–S2 + Fig S1–S2 + **보충영상 4편** | | | 자금: ERC 772873 ARTISTIC · ERC PoC 101069244 SMARTISTIC · ANR-22-PEBA-0002 BATMAN · MSCA COFUND 945357 (DESTINY, U.V.) · Horizon 101069686 PULSELiON |

**계보** (전부 정본 카드 있음 / 있어야 함):
`alabdali2023_cgmd_wet_manufacturing_ssb_cathode` (ref [18]) ·
`ngandjong2021_dem_calendering_digital_twin` (ref [25]) ·
`duquesnoy2020_calendering_ml_mesostructure_generator` (ref [26]) ·
**`vijay2025_hybrid_cgmd_dl_slurry_microstructure`** (자매편, 이 논문을 ref [28] 로 인용) ·
`lim2025_virtual_calendering_framework` · `hong2026_cbd_viscoelasticity_springback` (springback 축 인접).

---

## 3. 핵심 수치

### 3-A. ★★ **[Vijay25] 인용문 검증 — 네 양 전수 감사** (이 카드의 최우선 산출물)

> [Vijay25] 의 인용: *"접촉면적 · porosity · 확산도 · 탄성회복(springback)을 훨씬 낮은 비용으로 예측한다"*

| 양 | DL 이 **직접 예측**하나? | **무엇과** 대조? | 정확도 (n / 출처) | **우리 대응물과 같은 양인가?** | 판정 |
|---|---|---|---|---|---|
| **porosity** | ⚠ 간접 — DL 은 복셀격자를 내고 porosity 는 그 격자에서 **센다** | **DEM 테스트 격자** (실험 아님) | **평균 3.45 % · 최대 7.24 % · 최소 0.65 %** (n=11, SI Table S2, `derived(ours)` 계산) | **부분적** — 우리는 ε_sphere(구 부피합) 규약, 이쪽은 복셀-union 계열 ⇒ §10-② 의 규약 어긋남 실측 | **인용 ✅ 사실** |
| **접촉면적** (contact surface area) | ⚠ 간접 — 예측격자에서 **상-쌍 복셀 면 수**를 센다 | DEM 테스트 격자 | **Pore–CBD 8.01/16.76/14.23/16.05 %** (평균 **13.76**) · **Pore–AM 3.81/13.06/12.97/12.34** (평균 **10.54**) · **AM–CBD 6.65/3.85/16.63/8.84** (평균 **8.99**) — n=4 (Table 3) | **아니다** — 복셀 면적(voxel²)은 **상 경계의 기하 면적**이고 우리 Tabor/Stage-E 는 **접촉당 소성 접촉면 A(δ)**(Holm 협착이 걸리는 자리).  이름만 같다 | **인용 ⚠ 과장** — *"예측한다"* 는 맞지만 **네 양 중 최악(최대 16.76 %)** 이고 저자 자신이 결론에서 인정한다 |
| **확산도 (+ τ)** | ⛔ **아니다** | DEM 테스트 격자 | **확산도 평균 6.63 % · 최대 14.71 %** · **τ 평균 4.92 % · 최대 12.41 %** (n=11, `derived(ours)`) | 우리 σ_ion 과 **위상은 같으나** 이쪽은 **공극상 Fick 확산**(Li⁺ in 전해질)이고 우리는 **SE 고체상 이온전도** | **인용 ⚠⚠ 과장** — DL 출력 위에서 **GeoDict DiffuDict FV 솔브를 새로 돌려야** 나온다.  그 비용은 **미보고**이고 **DEM 경로와 동일** ⇒ *"훨씬 낮은 비용"* 이 이 양에는 **성립하지 않는다** |
| **springback (탄성회복)** | ✅ 궤적으로 재현 | DEM 부피궤적 (Fig 5b/6a/6c) | **숫자 0건.** 논문 전체에 회복률·두께·오차 **없음**.  `derived(ours)` 디지타이즈 = **CD 25/35/45 % → 4.8 / 7.6 / 10.1 %p** (§3-C) | 우리 MPM springback 축과 **직접 대응** (CLAUDE.md *"springback validation pending"*) | **인용 ⚠ 미검증** — *"remarkably capture"* 의 근거가 **육안 궤적 일치뿐** |

★ **[Vijay25] 의 과장이 어디서 왔는지도 특정된다**: **Fig 3 의 출력 상자**가
`Output: μStructure Morphology (s₄ → s_m), **Porosity, Diffusivity**` 라고 적어
**세 가지를 모두 CNN 출력처럼 보이게** 한다.  본문 §2.6 을 읽어야 확산도·τ 가
**GeoDict DiffuDict 로 따로 계산**된다는 것이 드러난다.  ⇒ **그림만 보고 인용하면 정확히 그 과장이 나온다.**

⇒ ★ **한 줄 판정**: **인용은 방향은 맞고 정밀도는 틀렸다.**
DL 이 예측하는 것은 **한 가지 — 다음 프레임의 복셀 격자**다.  네 양은 전부 그 격자의
**후처리**이고, 그 중 둘(확산도·τ)은 **별도 물리 솔버를 더 돌려야** 하며,
하나(springback)는 **정량화되지 않았다**.

### 3-B. 모델 · 데이터 · 비용 (전부 stated, 계산은 `derived(ours)` 표기)

| 항목 | 값 | 출처 |
|---|---|---|
| 복셀 격자 | **76 × 76 × 125 = 722,000** 복셀, **0.4 × 0.4 × 0.4 µm** | stated §2.2 |
| 복셀 라벨 | **0 = pore · 1 = CBD · 2 = AM · 4 = void**(전극 위 빈 공간) | stated §2.2 |
| 해상도 근거 | 0.4 µm = *"가장 작은 입자의 거의 1/4"* ⇒ **최소 입자 ⌀ ≈ 1.6 µm** | stated §4 (`derived(ours)` 환산) |
| 프레임 간격 | **75 µs** / 프레임 | stated §2.1 |
| 프레임 수 | CD 20/25/30/35/40/45/50 % → **14/18/21/24/28/31/35** | stated §2.1 |
| **압축률** | **≈1.43 %-두께 / 프레임** (20/14 … 50/35 전부 1.39–1.46) ⇒ *"constant compression rate"* 자기일관 | `derived(ours)` |
| 전극 수 | **4 개 × 7 CD = 28 런** + *"추가로 순수 테스트용 7 CD 1 전극"* = **총 35 런** | stated §2.1 · §2.4 (⚠ §10-⑥ 불일치) |
| 시계열(TS) 분할 | **train 24 / test 11** (Table 2: I@45, II@35, III@25·45, **IV 전부 7**) | stated §2.4 · §3.2 |
| 총 프레임 | **855** (train 580 / test 275) | `derived(ours)` |
| 슬라이딩윈도 샘플 | **train 508 / test 242** (m−3 per TS) | `derived(ours)` |
| **파라미터 수** | **663,729,862** (trainable 663,728,326) | stated Table S1 |
| **★ 정보 병목** | flatten 512 → **dense 150** → dense **722,000** ⇒ **전체 3D 미세구조가 150 개 실수에서 복호된다 (4,813 : 1)** | `derived(ours)` from Table S1 |
| ★ 표본당 파라미터 | **663.7 M / 508 = 1,306,555 param per training sample** | `derived(ours)` |
| 학습 | Adam, MSE 손실, **1000 epoch**, Optuna **500 trial**(MatriCS HPC) | stated §2.4 · §3.1 |
| 최종 MSE / MAE | train **0.0088** / val **0.0085**; MAE train **0.0689** / val **0.0662** | stated Table 1 · §3.1 |
| **DL 추론** | **15 s / step** (wall) | stated §4 |
| **DEM** | **≈47 min / step** (wall) | stated §4 |
| **가속 배수** | **188×** per step | `derived(ours)` = 2820/15 |
| 하드웨어 | ⛔ **미보고** (GPU/CPU/코어 수 없음; MatriCS 는 Optuna 문맥에서만 언급) | — |

### 3-C. 압연 결과 수치 (SI Table S2, 전부 stated)

| 미세구조 | CD % | porosity DEM-test | porosity DL | 확산도 DEM-test (×10⁻¹² m²/s) | 확산도 DL | τ DEM-test | τ DL |
|---|---|---|---|---|---|---|---|
| I | 45 | 19.07 | 18.54 | 1.83 | **1.83** ⚠ | 34.01 | **34.01** ⚠ |
| II | 35 | 20.01 | 20.14 | 2.24 | 2.09 | 35.70 | 36.58 |
| III | 25 | 28.06 | 27.04 | 10.58 | 10.34 | 9.74 | 10.16 |
| III | 45 | 19.89 | 19.56 | 1.09 | 0.94 | 64.54 | 68.68 |
| **IV** (전 구간 hold-out) | 20 | 30.66 | 29.43 | 15.26 | 14.41 | 10.63 | 11.27 |
| IV | 25 | 26.54 | 27.87 | 11.00 | 11.94 | 10.88 | 11.53 |
| IV | 30 | 24.78 | 23.54 | 3.40 | 2.90 | 28.68 | 32.24 |
| IV | 35 | 21.04 | 20.42 | 2.14 | 2.24 | 34.65 | 36.73 |
| IV | 40 | 20.02 | 18.57 | 1.48 | 1.60 | 40.03 | 41.44 |
| IV | 45 | 19.04 | 18.66 | 1.04 | 1.06 | 67.58 | 69.98 |
| IV | 50 | 19.87 | 19.27 | 0.90 | 0.96 | 85.29 | 88.24 |

⚠ **micro-I @45 % 행은 확산도·τ 가 DEM-test 와 DL 이 소수 둘째/넷째 자리까지 완전히 같다**
(1.83 vs 1.83, 34.01 vs 34.01) — porosity 만 다르다(19.07 vs 18.54).  **전사(轉寫) 오류로 의심**된다.
그 행을 빼면 평균 오차가 porosity 3.52 / 확산도 **7.29** / τ **5.41 %** 로 **올라간다** (§10-③).

**★ 물리 추세 (stated)**: CD↑ → porosity↓ · 확산도↓ · τ↑.  **확산도의 급락은 CD 20→30 % 구간**에
집중되고(예: micro IV 15.26 → 3.40 = **4.5배 붕괴**) 그 뒤로는 완만.  **porosity 는 CD 40 % 에서 바닥**
(≈19–20 %)을 치고 그 위에서는 **±2 % 진동**하며 단조성이 깨진다 ⇒ 저자 해석 = *"전극이 기계적
압축 한계에 도달"*.  **≈20 % porosity 하한**은 실험 보고(2차 NMC 입자 파쇄 때문에 그 아래로 못 간다,
refs [15,48,49])와 **정성적으로 일치**한다고 적는다.

### 3-D. ★ spring-back 정량화 (`derived(ours)` — 논문에 숫자가 없어 우리가 뽑았다)

Fig 5b / 6a / 6c 의 **void 복셀 수**를 디지타이즈해 두께 h = (722,000 − void)/(76×76) 로 환산:

| 미세구조 @ CD | void 최대 → 완화 (×10⁵ vox) | 압축 최저 h (vox) | 완화 h (vox) | **CD_peak** | **CD_final** | **spring-back** | 압축두께 대비 회복 |
|---|---|---|---|---|---|---|---|
| III @ **25 %** | 1.63 → 1.28 | 96.8 | 102.8 | 22.6 % | 17.7 % | **4.8 %p** | **+6.3 %** |
| II @ **35 %** | 2.45 → 1.90 | 82.6 | 92.1 | 33.9 % | 26.3 % | **7.6 %p** | **+11.5 %** |
| I @ **45 %** | 3.10 → 2.37 | 71.3 | 84.0 | 42.9 % | 32.8 % | **10.1 %p** | **+17.7 %** |

⚠ **digitized — TREND only** (읽기 오차 ±0.05×10⁵ vox ≈ ±0.9 vox ≈ ±0.7 %p).
CD_peak 이 목표 CD 보다 2–3 %p 낮게 나오는 것이 디지타이즈 오차의 크기다.
★ **그럼에도 살아남는 것**: **spring-back 은 CD 에 단조 증가**하고 (4.8 → 7.6 → 10.1 %p),
**압축 두께 대비 회복률이 6 → 18 %** 로 3배 가까이 커진다.  ⇒ *"세게 누를수록 더 많이 되튄다"*.
이것이 이 논문에서 **우리 MPM springback 축에 직접 쓸 수 있는 유일한 정량 정보**다.

---

## 4. 시뮬레이션 방법 ★

### 4-1. DEM (압연) — ⛔ **이 논문에는 파라미터가 한 줄도 없다**

| 항목 | 이 논문이 적은 것 |
|---|---|
| 코드 | ⛔ **미기재** (LIGGGHTS/LAMMPS 등 이름 없음).  *"the DEM code used in her past work"* = **Jiahui Xu**, ref [36] |
| 접촉법칙 | ⛔ **미기재** (Hertz / GH / Thornton–Ning 등 언급 없음) |
| E · ν · µ · COR | ⛔ **전부 미기재** |
| 결합/binder 모델 | ⛔ **미기재** (CBD 는 복셀 라벨 1 로만 등장) |
| **압축 도구** | ★ *"the calendering roll (**represented in the DEM model as a planar press**)"* — **롤이 아니라 평면 프레스** |
| **★ 압축 축 단위** | **CD = 건조전극 대비 두께 감소율 %** (20–50 %).  **압력(MPa) · line load 는 논문 전체에 0건** |
| 재하 | **일정 압축 속도**, **z 축 top→bottom** 단방향, `derived(ours)` **≈1.43 %-두께/프레임** |
| 완화 | 목표 CD 도달 시 **press 해제** → spring-back 구간 |
| 입자 형상 | **CT(Computer Tomography)에서 얻은 실제 AM 입자 크기·형상** (구가 아님) — ref [36] 상속 |
| 초기 구조 | **CGPD(coarse-grained particle dynamics)로 슬러리+건조를 돌린 결과** — ref [36] 상속 |
| 검증 | ⛔ **이 논문에서 신규 실험 0건.**  *"already validated by experiments … in electrode functional metrics such as tortuosity factor and porosity"* = **ref [36] 상속**.  ⚠⚠ **2026-09-11 갱신** — 그 ref [36] 이 정본에 들어왔다(`papers/xu2023_realistic_am_shape_cgmd_calendering.md`) 그리고 **상속의 절반이 깨진다**: **porosity 는 독립 검증(exp 8 점)** 이지만 **τ 는 아니다** — Xu 2023 SI 가 dilation–erosion 인자를 **τ 의 µ-XCT 값에 맞춰** 골라 **모든 결과에 적용**했다.  ⇒ *"τ 가 실험 검증됐다"* 를 재인용할 때 이 문장을 병기 |
| 비용 | **≈47 min / 75 µs step** (하드웨어 미기재) |

**⚠ 우리가 쓸 수 있는 DEM 물성은 이 논문에서 얻을 수 없다.**  계보의 정본 카드
`ngandjong2021_dem_calendering_digital_twin` 이 같은 그룹·같은 조성(NMC111 96/2/2)에 대해
LIGGGHTS · GH(Granular-Hertz)+SJKR · **E_AM 200 GPa · E_CBD 2 GPa · ν_AM 0.3 / ν_CBD 0.5 ·
e(COR) 0.15 · X_µ 0.001** · plate 속도 2×10⁻³ µm/µs · timestep **0.1 ns** · **압력 축 0–156 MPa** 를 적고 있다 —
⚠ **그러나 그것은 그 카드의 값이지 이 논문의 값이 아니다.**  ref [36](Xu 2023 JPS 554, 232294)이
그 사이에 무엇을 바꿨는지는 **이 PDF 로 알 수 없다**.  인용할 때 반드시 출처를 분리할 것.

> ⚠ **정정 2026-09-11 (Ngandjong 카드 2판 재판독)** — 위 줄은 원래 *"ν 0.3"* · *"0–160 MPa"* 였다.
> **ν 0.3 은 AM 값이고 CBD 는 0.5(비압축)** 다 — 그 카드 1판이 Table 2 의 ν 행을 한 값으로 뭉갠 것이
> 여기로 전파됐다.  **COR 행(0.15)** 도 1판에 아예 빠져 있었고 **timestep 은 1e-5 µs 로 10배 틀려** 있었다.
> 압력축 최댓값의 실측 디지타이즈는 **156 MPa** 다(160 은 축 눈금).
> ★ 그 2판은 이 카드가 *"springback 숫자 0건"* 이라 적은 축에 **정량 표적을 공급한다**:
> 압입 언로딩 잔류깊이 **exp ≈ 0.84 · sim ≈ 0.75 d_max** ⇒ **탄성회복 16 % vs 25 %**
> (⚠ 압입 회복이지 압연 springback 이 아니다).
> ⛔ 그리고 **그 압력축의 전이 판정은 "입구이자 벽"** 이다 — densification 의 **99 %가 86 MPa 안에서** 끝나
> **우리 post-knee 구간(≥ P_y 138 MPa)에 점이 0 개**이고, 86 → 156 MPa 에서 곡선이 평평하다(Δε 0.1 %p)
> (`ngandjong2021_dem_calendering_digital_twin` §3-B).

### 4-2. 복셀화

- DEM 입자 좌표 → **연속공간을 복셀 셀로 이산화**하고 각 입자를 좌표가 떨어지는 셀에 배정.
- 4 상: pore(0) · CBD(1) · AM(2) · **void(4)** — void 는 *"압연 과정에서 전극 위쪽에 생기는 영역"*.
  ⇒ **초기 프레임에서 void = 0** (전극이 격자 125 복셀을 꽉 채운다).
- 스크립트 제공자 = Dennis Weitze (사사).  가시화 = OVITO.

### 4-3. ★ DL 모델 — 아키텍처를 Table S1 산술로 복원

```
input   : 722,000-채널 × (lag 축)            ← 3D 76×76×125 를 1D 배열로 reshape
conv1d  : filters 256, kernel 3   → (None, 2, 256)   param 554,496,256 = 3·722000·256 + 256  ✓
batchnorm ×1                                           1,024
maxpool : pool 1, stride 1        → ★ 항등(no-op)          0
conv1d_1: filters 256, kernel 1   → (None, 2, 256)      65,792 = 256·256 + 256  ✓
batchnorm + maxpool(1,1)                               1,024 / 0
conv1d_2: filters 256, kernel 1   → (None, 2, 256)      65,792
batchnorm + maxpool(1,1) + dropout 0.2                 1,024 / 0 / 0
flatten                           → (None, 512)              0
dense   : 150, relu                                     76,950 = 512·150 + 150  ✓
dense_1 : 722,000, relu                            109,022,000 = 150·722000 + 722000  ✓
--------------------------------------------------------------------
TOTAL                                              663,729,862  ✓ (표 합과 정확히 일치)
```

★★ **우리가 이 산술에서 얻은 세 가지 (논문이 말하지 않는 것)**:
1. **정보 병목 = 150 실수.**  722,000 복셀짜리 3D 미세구조 전체가 **150 차원 잠재변수에서 복호**된다
   (**4,813 : 1**).  ⇒ 이 모델은 원리적으로 **프레임당 150 자유도 이상의 구조 변화를 표현할 수 없다.**
   **이것이 왜 벌크 지표(porosity·τ)는 ~3–5 % 인데 상-경계 접촉면적은 10–17 % 인지**의 구조적 이유다.
2. **max-pooling 3 개가 전부 항등 연산**이다 (pool size = stride = 1).  논문은 *"계산 복잡도를 줄인다"*
   고 쓰지만 **아무 것도 안 한다**.
3. ★ **CD 는 "네 번째 lag 슬롯" 으로 들어간다 — 산술로 확정했고 Fig 3 이 확인해 준다.**
   커널 3 의 출력 길이가 **2** 이므로 `padding='valid'` 에서 **입력 시퀀스 길이는 4** 여야 한다.
   본문은 **3-lag** 만 말하고 **Fig 2 도 입방체 3 개만 그린다** — 한 칸이 비는데,
   **Fig 3 의 입력 상자가 그 칸을 채운다: `Input: s₁ · s₂ · s₃ · CD %`.**
   ⇒ `4 − 3 + 1 = 2` 로 Table S1 의 `(None, 2, 256)` 과 **정확히 닫힌다**.
   ⚠ 그러면 **CD(스칼라)가 722,000-길이 상수 배열로 broadcast 되어 프레임 한 칸을 통째로 차지**해야
   한다 (`derived(ours)` — 본문은 CD 주입 방식을 **끝까지 설명하지 않는다**).
   ⇒ **조건화가 매우 거칠다**: 전체 입력의 1/4 이 상수이고, 파라미터의 1/4(≈138 M)이 그 상수에 붙는다.

**학습 데이터 구성** (§2.3): TS `S_n = [s_1 … s_m]` 을 3-lag 슬라이딩윈도로
`X = [s_k, s_{k+1}, s_{k+2}] → Y = s_{k+3}` 으로 펼친다.

**하이퍼파라미터 탐색** (§3.1, Table 1): Optuna 500 trial, 2 단계(층 수 → 활성함수).
A(2conv LeakyReLU + 2FC tanh, drop 0.372) MSE 0.1681/0.1348 · B(3 mish + 2 LeakyReLU, 0.364) 0.1176/0.1312 ·
C(3 mish + 2 mish, 0.200) 0.0357/0.0257 · **D(3 relu + 2 relu, 0.200) 0.0088/0.0085 ← 채택**.

### 4-4. 후처리 / 평가 지표

- **데이터 지표**: MSE · MAE · **복셀 R²** — 식 (3)(4).  ⚠ **분모가 프레임 내부 복셀값의 *공간* 분산**
  `Σ(v_g − v̄)²`, v̄ = 그 프레임 ground-truth 복셀값 평균.  ⇒ §10-① 참조.
- **접촉면적**: 상-쌍 복셀 경계 면 수 (단위 voxel²), Pore–CBD / Pore–AM / AM–CBD 3 종.
- **전달**: **GeoDict 2023 DiffuDict** 로 공극망 Fick 정상상태 확산.
  x·y **주기**, z 양끝에 **Li⁺ 0 mM / 1 mM** 고정.  `D_eff = −J × length / 1 mM` (식 5).
  bulk 확산계수(pore·CBD)는 **Chouchane & Franco (ref [45])** 값.
  τ 는 **McMullin 수** `τ = (σ_bulk/σ_eff) × ε` (식 6).

### 4-5. ★ 입자 처리 (DEM판 "무질서 처리")

- **형상**: CT 유래 **비구형 실제 AM 입자** (ref [36] 상속) — [Vijay25]·Ngandjong 의 구 근사보다 **위**.
- **소성**: ⛔ 이 논문에는 **어떤 소성 서술도 없다**.  압밀은 **DEM 접촉 + 재배열** 이고
  **입자 SHAPE 는 안 변한다** (frame[1]/[2] 의 rigid-sphere/rigid-shape 층).
  ⚠ 단 **복셀 라벨 층에서는 AM 부피가 보존되지 않는다** — §10-② 실측.
- **분산/seed**: ⛔ **없다.**  4(+1) 개 초기 미세구조가 있을 뿐 **seed 반복 0**,
  **오차막대 0**, **불확실도 0**.  DL 앙상블도 없다 ([Vijay25] 는 4-모델 앙상블이었다).

---

## 5. 결과 — 절별 전수

### 5-1. §3.1 CNN 최적화
Optuna 500 trial → Model D.  MSE train 0.0088 ↔ val 0.0085 (**val 이 더 낮다**) ⇒ 저자 판정
*"과적합 없음"*.  MAE 1000 epoch 후 0.0689 / 0.0662.  Fig 4 의 손실곡선은 매끄럽게 수렴.
⚠ **train/val 차이가 없다는 것은 val 이 *같은 궤적의 이웃 프레임*이라는 뜻이기도 하다** — 3 프레임
간격 75 µs 로 거의 동일한 구조라 **train/val 분리가 실질적이지 않다** (§10-⑤).

### 5-2. §3.2 데이터 지표 평가
- **micro I @45 %**: Fig 5a 가 DEM ↔ DL 을 6 프레임(0/5/10/15/20/25) 나란히 놓고,
  **압축 → spring-back → 완화**를 육안으로 보여준다.  Fig 5b 는 4 상 부피 궤적, Fig 5c 는 프레임별 R².
  저자: *"R² 가 모든 프레임에서 90 % 이상"*.
  ⚠ **이 문장은 micro I 에만 참이다** — Fig 6b(micro II @35 %)의 최저점은 **≈87.2 %** 로 90 아래다 (§10-④).
- **micro II @35 %, III @25 %, III @45 %**: 같은 방식.  저자: *"평균 R² ≈ 95 %"*.
- ★ **R² 궤적의 모양이 결정적이다** (§10-⑤ / §7-2): 프레임 0·1·2 가 **정확히 100**(= 입력 lag),
  프레임 3–5 에서 95.6 → 93.7 → **92.2** 로 떨어졌다가 **프레임 9 에서 다시 정확히 100 으로 복귀**,
  spring-back 근방(16–18)에서 **91.7** 로 최저, 이후 프레임 21 부터 **96.7–96.9 로 평탄**.
  ⇒ 오차가 **누적되지 않고 회복한다** = **teacher-forcing(매 프레임 실제 DEM lag 3 개를 먹인다)의 서명**이지
  **free-running rollout 의 서명이 아니다.**

### 5-3. §3.3 전극 기능 지표 평가
- **접촉면적** (Table 3): 위 §3-A.  저자 자평 *"평균 10 % 안팎이면 상들의 기하 배치를 정확히
  예측하는 것"*, 그러나 결론에서 *"상 경계는 아직 개선 여지가 있다"* 고 인정하고
  **해법으로 복셀 축소를 제시**(학습비용 증가와 trade-off).
- **porosity·확산도** (Fig 7, 8 패널): 저자 주장 *"상대오차가 0.5 %–9.8 % 사이에서 진동"*.
  ⚠ **자기 SI 와 모순** — 확산도 오차가 **13.76 %(III@45)** 와 **14.71 %(IV@30)** 로 두 건이 9.8 을 넘는다 (§10-③).
- **τ** (Table S2 / Fig S2): 저자 주장 *"±5 %"*.
  ⚠ **11 건 중 5 건이 5 % 초과**, 최대 **12.41 %**(IV@30) (§10-③).
- **물리 해석** (stated): porosity 는 CD 40 % 까지 단조 감소하고 그 위에서 ±2 % 진동 ⇒ *"기계적 압축한계"*;
  **≈20 % 하한**이 실험의 *"2차 NMC 입자 파쇄 때문에 그 아래로 못 간다"* 와 부합.
  확산도의 큰 낙차는 **CD 20→30 %** 에 있고 그 위는 완만.  τ 는 CD 와 함께 단조 증가.
- **저자 스스로 단 τ 경고**: CBD 분포 결정이 어려워 실험 τ 는 과소평가될 수 있고, Fickean 가정 때문에
  계산 τ 는 과대평가될 수 있다 ⇒ *"이 연구의 목표는 DEM 결과를 더 빠른 ML 로 재현하는 것"*.
  ★ **이것은 정직한 서술이고 동시에 결정적 한계다 — 기준선이 실험이 아니라 DEM 이다.**

### 5-4. §4 결론 / 전망
- 15 s vs 47 min ⇒ *"계산비용을 엄청나게 줄였다"*.
- 한계 자인 3 건: (i) **상 간 접촉면 오차 10–15 %** vs 전체 기능지표 <5 % ⇒ 계면은 개선 필요;
  (ii) **CD 20–50 % 밖의 외삽은 비물리적 거동을 낼 수 있다 — 외삽에 부적합**;
  (iii) 프레임 수·격자 해상도는 **미탐색 하이퍼파라미터**.
- 전망: transfer learning 으로 graphite/LFP/blend 확장, **4D-CT 시계열**로 확장.

---

## 6. Figure set ★ (전수 + 우리가 쓸 것)

| # | 무엇을 보여주나 | **우리가 재사용할 것** |
|---|---|---|
| **1a** | 습식 제조 3 단계 모식도(슬러리 → 코팅·건조 → **압연 2-롤**) + 압연 전후 단면 복셀 스냅샷(노랑 pore·빨강 CBD·파랑 AM·회색 void) | **4상 색규약**.  압연 전후 단면 대비 = 우리 STEP2 morphology 그림의 포맷 참고 |
| **1b** | ★ **프레임워크**: 두께 h 의 미압연 전극 → (lag 슬랩 2 개 + CNN) → h_cal, **CD 와 Sb(spring-back)를 화살표로 표기** | **우리 MPM 압밀 그림에 Sb 화살표를 넣는 포맷** — 우리는 지금 springback 을 그림에 안 그린다 |
| **2** | 1D-CNN 도해.  ★ 직접 확인: **입력 입방체 3 개만** 그려져 있고(= CD 슬롯 누락), Conv1D(256,**3**) → Conv1D(256,**1**) → Conv1D(256,**1**), **MaxPooling(1,1) ×3**, Dropout 0.2, Flatten, **Dense(150) → Dense(722000)** | ★ **Table S1 산술의 그림 확인판** — 150-차원 병목과 항등 pooling 이 그림에도 그대로 있다.  ⚠ Fig 3 과 입력 개수가 다르다 |
| **3** | ★★ 전체 워크플로.  좌: DEM → 복셀화(76×76×125, pore 노랑/CBD 빨강/AM 파랑).  중: **Calendering DATASET S₁(50 % CD, m=35) … S₂₈(20 % CD, m=14)**.  우상: 3-lag 슬라이딩윈도 행렬.  우하: **`Input: s₁ s₂ s₃ CD %` → CNN → `Output: μStructure Morphology (s₄ → s_m), Porosity, Diffusivity`** | ★★ **두 가지를 여기서 확정했다**: ① **CD 가 네 번째 입력 슬롯** = Table S1 의 출력길이 2 와 닫힘(§4-3-③) ② **출력 상자가 rollout(s₄→s_m)을 명시** = §10-⑤ 의 한쪽 증거.  ★ 그리고 **출력 상자에 "Porosity, Diffusivity" 가 적혀 있는 것이 [Vijay25] 인용 과장의 출처**다 — 실제로는 §2.6 대로 **GeoDict 가 따로 계산**한다 |
| **4a,b** | 학습곡선 MSE / MAE (train 파랑 · val 주황), 1000 epoch | — |
| **5a** | ★ **DEM ↔ DL 미세구조 6 프레임 병렬**(0/5/10/15/20/25) + spring-back 세로선 | ★ **시간축 비교 패널 포맷** |
| **5b** | ★★ **4 상 복셀 수 궤적** (실선 DEM, 파선 DL), micro I @45 % | ★★ **우리가 §3-D springback 을 뽑은 원천.**  또한 §10-② 의 **AM 비보존** 증거 |
| **5c** | ★ 프레임별 R² (y축 **90–100**) | ★ **teacher-forcing 판별의 증거** (§10-⑤).  ⚠ 축 스팬이 좁아 시각적으로 완벽해 보인다 |
| **6a,c,e** | 부피 궤적: micro II @35 %, III @25 %, III @45 % | springback 3 점 추세 (§3-D) |
| **6b,d,f** | 프레임별 R² (y축 **80–100** — **5c 와 다른 스팬**) | ⚠ **6b 최저 ≈87.2 %** = 본문 *"항상 90 이상"* 반증 |
| **7a,c,e,g** | ★ **porosity vs CD** (DEM_train ▲ · DEM_test ● · DL ✕), micro I/II/III/**IV** | ★ **CD-porosity 곡선 4 개** (`derived(ours)` trivial baseline 대조의 원천, §10-⑦) |
| **7b,d,f,h** | ★ **확산도 vs CD**, 같은 4 개.  **y 선형 0–20** | ⚠ **h 패널이 Table S2 와 계열이 뒤바뀌어 있다** (§10-⑧).  ⚠ **선형축이 CD≥30 % 의 큰 상대오차를 완전히 가린다** |
| **S1** | DL 예측 미세구조 시간전개(25 % CD), 상 분리 표시 | — |
| **S2 a–d** | τ vs CD, micro I–IV | §3-C 표의 그림판 |
| **Table 1** | CNN 후보 A–D 의 MSE | — |
| **Table 2** | ★ **train/test CD 분할표** | ★ **누출 점검의 원천** — micro IV 만 완전 hold-out |
| **Table 3** | ★ **상-쌍 접촉면적 DEM vs DL + 오차 %** | ★ 인용검증표 §3-A |
| **Table S1** | ★★ **CNN 층별 파라미터** | ★★ **150-차원 병목**을 여기서 복원 (§4-3) |
| **Table S2** | ★★ **porosity·확산도·τ 전수** | ★★ 우리 오차 재계산·trivial baseline 의 원천 |

> ★ **내가 실제로 *열어 본* 그림** (캡션만 읽지 않았다는 공개): **Fig 1 · 2 · 3 · 5(a,b,c 확대) ·
> 6(a–d) · 7(전 패널 + 7h 확대)**.  **열어 보지 않은 것: Fig 4(손실곡선) · Fig S1 · Fig S2.**
> 표(Table 1·2·3·S1·S2)는 PDF 텍스트로 읽었다 (그림보다 정확하다).
> 본문에서 `digitized` 로 표시한 값(§3-D · §10-②)은 **Fig 5b/6a/6c 를 확대해 눈으로 읽은 것**이다.

### 6-B. 보충 영상 4 편 (읽을 수 없음 — 존재와 추정 대응만 기록)

| 파일 | 용량 | 길이 |
|---|---|---|
| `aenm202400376-supp-0002-videos1.mp4` | 4.42 MB | 3.16 s |
| `aenm202400376-supp-0003-videos2.mp4` | 3.44 MB | 2.48 s |
| `aenm202400376-supp-0004-videos3.mp4` | 2.79 MB | 1.88 s |
| `aenm202400376-supp-0005-videos4.mp4` | 4.53 MB | 3.16 s |

⚠ **SI PDF 에 영상 캡션이 없다.**  본문의 유일한 언급은 §3.2 끝
*"Videos of the DEM versus DL microstructure evolution during calendering are available in the
supporting information section."* 이고, **바로 앞 문단이 테스트 4 건(I@45 · II@35 · III@25 · III@45)을
차례로 다룬다** ⇒ **영상 1–4 = 그 4 건의 DEM↔DL 병렬 전개**로 **추정**된다 (`inferred`, 확정 아님).
★ 길이비(3.16 : 2.48 : 1.88 : 3.16 s)가 프레임 수(31 : 24 : 18 : 31)와 **정확히 비례**한다
(31/3.16 = 9.81 · 24/2.48 = 9.68 · 18/1.88 = 9.57 · 31/3.16 = 9.81 fps) ⇒ **이 추정을 강하게 뒷받침**하고,
**영상 1 과 4 가 둘 다 31 프레임 = I@45 와 III@45** 임을 시사한다.

---

## 7. 우리 DEM+MPM 대비 ★  →  `our_dem_baseline.md` · `comparison_vs_ours_DEM.md`

### 7-1. frame[5] 상 어디에 서는가

| | 이 논문 | 우리 |
|---|---|---|
| **압밀 물리** | DEM(ref [36] 상속), **입자 형상 안 변함** | DEM(hooke/hysteresis, 형상 안 변함) **+ MPM(진짜 SHAPE 소성)** |
| **압밀 축** | ⛔ **CD = 두께감소율 %** (20–50) | **압력 300 MPa** (Heckel P_y = 138 MPa) |
| **재하** | 평면 프레스, 일정 속도, ≈1.43 %-두께/프레임 | DEM: servo/hold · MPM: `--protocol servo/hold` + `--platen-mach` |
| **완화/springback** | ✅ **명시적으로 모델 안에 있다** (press 해제 구간) | ⚠ **우리 hold 프로토콜은 정지 후 고정** — springback 축이 **미검증**(CLAUDE.md) |
| **transport** | 공극상 **Fick 확산**(GeoDict FV) → D_eff·τ.  **σ 삼중항 0** | DEM 접촉망 σ_ion/σ_e/k (Kirchhoff+Holm) **+** MPM 복셀 FV σ (STEP3) |
| **접촉면적** | 복셀 상-경계 면적 | **접촉당** Tabor/Stage-E 소성 접촉면 A(δ) (Holm 협착이 걸리는 자리) |
| **DL 층** | ✅ **시간-surrogate**(프레임 → 프레임) | ⛔ 없다.  우리 ML 은 **설계→구조 정적 예측기**(`ml_design_structure.py`) |
| **실험 앵커** | ⛔ **신규 0건** (ref [36] 상속 + porosity 20 % 정성 일치) | Minnmann 10 %@300 MPa · Cronau overlap 11–12 % · Bazzoun EIS σ · Lee2025 σ_e |

⇒ **frame[5] 판정**: 이 논문은 **우리 STEP1/STEP2(압밀)와 같은 칸에 서 있고**,
그 칸에서 **DEM 이 소유한 절반(이산 패킹·재배열)** 만 갖는다.
**MPM 이 소유한 절반(진짜 소성 형상변화·void-fill 유동·소성변형장)은 이 논문에 없다.**
그 대신 **우리에게 없는 것 하나를 갖는다 — 압밀의 *시간축* 을 배우는 surrogate.**

### 7-2. ★★ 그 surrogate 를 우리에게 붙일 수 있는가 — **아직 아니다, 두 겹의 선결조건**

**① 그들 쪽 선결조건 — 추론 프로토콜에 대해 그림 두 장이 서로 다른 말을 한다.**
- **Fig 3 (rollout 이라고 명시)**: 출력 상자가 `Output: μStructure Morphology (**s₄ → s_m**)` 이다.
  즉 **s₁·s₂·s₃ + CD % 만 주고 궤적 끝까지 자기회귀로 굴린다**는 뜻이다.  Fig 1b 도 그렇게 그려져 있다.
- **⚠ Fig 5c (rollout 답지 않은 모양)**: R² 가 0·1·2 = **정확히 100**(입력 lag) → 3/4/5 = 95.6/93.7/**92.2**
  → **프레임 9 에 다시 정확히 100 으로 복귀** → 16–18 = 91.7 최저 → 21 이후 96.7–96.9 평탄.
  Fig 6b 도 87.2 → **99.5–99.8 복귀**.  **자기회귀는 보통 오차가 단조 누적되어 이런 완전 복귀를
  내지 않는다.**  ⇒ (a) 실제로는 **one-step-ahead(teacher-forced)로 채점**했거나,
  (b) 진짜 rollout 인데 **CD 조건화(§4-3-③)가 궤적을 끌어당겨 자기보정**했거나 둘 중 하나다.
  ★ (b)가 원리적으로 불가능하지는 않다 — 입력의 1/4 이 "목표 CD" 라는 **절대 좌표**이므로
  모델이 표류했다가 되돌아올 통로가 있다.  ⇒ **단정하지 않는다.**
- ⚠⚠ **그러나 (a)라면 188× 는 surrogate 가속이 아니다** — 프레임 m 을 내려면 DEM 프레임
  m−3·m−2·m−1 이 필요하고, 그러면 DEM 을 어차피 돌려야 한다.
  **이 한 가지가 이 논문 전체의 가치를 가르는데 Methods 에 한 줄도 없다.**
⇒ 우리가 따라 하려면 **rollout / teacher-forcing 을 명시하고 *둘 다* 보고**하고,
**rollout R² 가 프레임에 따라 단조 감소하는지**를 1번 그림으로 낸다.

**② 우리 쪽 선결조건 — 우리 타깃이 아직 인공물이다.**
우리 MPM scaffold 압밀의 **정착 porosity 는 플래튼 *정지 시점*의 함수**다:
속도 사다리 `--sub` 40/80/160 에서 porosity 14.38 → 12.76 → **11.08 %** 로 계속 내려가고 수렴하지 않으며,
sub=80 궤적의 **frame 15 가 정확히 15.93 %**(우리가 "앵커" 로 썼던 값), frame 17 이 14.38 % 다
(`docs/mpm_platen_kinematic_stop_defect.md` rev3 §17 · rev4 §22 · rev6 §31).
게다가 R1 완주는 준정적 답이 **ε_sphere 1.13 %** (실험 15.6 % 대비 **14.5 %p 과압축**)임을 보였고
(`docs/reviews/fam_platen_prereg_20260812.md` §11-1 · CL-04), 플래튼 결함이 그것을 **우연히 상쇄**하고 있었다.
⇒ ★ **이 축이 닫히기 전에 시간-surrogate 를 학습시키면, surrogate 는 물리가 아니라
"우리 플래튼이 어느 프레임에서 멈추는가" 를 배운다.**  그리고 이 논문처럼 **프레임별 지표**로
검증하면 그 인공물이 **완벽한 R²로 재현되어 보이기까지 한다**.
⇒ **SR 트랙 2(플래튼 정지 결함 × AM 하중분담)가 닫힌 뒤에만 착수.**
(이 판정은 `vijay2025` 카드 §12-3 과 동일하고, 이 논문이 **압밀 단계**라서 **더 직접적으로 걸린다**.)

**③ 그리고 우리 쪽에는 "정지 프레임" 문제의 *쌍둥이* 가 이미 있다 — 복셀 규약.**
§10-② 가 실측한 것: 이들의 **복셀 라벨 porosity 가 Table S2 porosity 와 프레임 0 에서 8.5 %p,
완화 상태에서 16.4 %p 어긋난다**.  이것은 우리가 이미 두 번 밟은 지뢰다 —
`MPM관례(16.877) − ε_sphere(15.626) = 1.251 %p` (CLAUDE.md 2026-08-12 정정) 와
STEP3 SDCP **표현부피/참부피 18.1배 변동** (CL-25).  ⇒ ★ **surrogate 를 붙이기 전에
"학습 타깃의 porosity 규약" 을 명시적으로 고정하는 게이트가 필요하다.**

### 7-3. 항목별 same / different / why

| 축 | 이 논문 | 우리 | 판정 |
|---|---|---|---|
| **porosity 절대값** | **19–31 %** (CD 20–50 %), 하한 ≈20 % | ASSB **10–16 %** (real_14 15.6 %, pure-SE 10 %@300 MPa) | ⛔ **절대비교 금지** — 액체계 LIB 는 porosity 를 **원한다**.  방향도 반대(그들에겐 낮을수록 나쁨) |
| **porosity 하한의 *기전*** | *"2차 NMC 입자 파쇄"* (refs [15,48,49]) | **rigid-sphere floor ≈20 %**(Varkey 카드) · **소성 유동이 그 아래로 내린다**(MPM) | ★ **다른 기전이 우연히 같은 숫자**.  그들의 20 % 는 **AM 파쇄 한계**, 우리 20 % 는 **형상 소성 부재**.  ⚠ 같은 숫자를 같은 근거로 쓰지 말 것 |
| **압축 축** | **CD %** | **MPa** | ⛔ **원리적으로 안 겹친다** — Heckel `ln(1/(1−D)) = K·P + A` 에 넣을 점이 **0 개**.  [Vijay25] 와 같은 벽.  ⚠ **단 계보 위쪽 `ngandjong2021` 은 0–160 MPa 축을 갖는다** ⇒ 압력축이 필요하면 진입점은 **그쪽** |
| **압밀 모드** | **압연(평면 프레스 근사) + 해제** | **cold-press 단축 + hold** | 경로가 다르다.  ⚠ 그러나 **평면 프레스 근사**라 롤보다 **우리 쪽에 가깝다** — [Ngandjong21] 카드의 *"압연 ≠ 단축프레싱"* 경고가 **약간 완화**된다 |
| **springback** | ✅ 모델에 있음, `derived(ours)` **4.8/7.6/10.1 %p @ CD 25/35/45** | ⚠ **미검증 축** | ★★ **여기가 이 논문의 최대 기여** — 우리에게 없는 축의 **정성 추세(CD↑ → 회복↑, 6→18 %)** 를 준다.  ⚠ 단 LIB·CBD 계이고 `hong2026_cbd_viscoelasticity_springback` 이 보였듯 **springback 은 CBD 점탄성이 지배** ⇒ **ASSB(PTFE·SE)로 값 전이 금지, 추세만** |
| **접촉면적** | 복셀 상-경계 면적, 오차 **최대 16.76 %** | **Tabor/Stage-E 접촉당 A(δ)**, 5-regime 캡 | ⛔ **같은 양이 아니다.**  그들 것은 **기하 표면적**, 우리 것은 **협착저항이 걸리는 전도 면적**.  ★ 그러나 **"DL surrogate 는 계면을 가장 못 맞춘다"** 는 **정성 결론은 우리에게 그대로 전이**된다 |
| **τ / 확산도** | 공극상 **Fick**, τ **9.7 → 85.3** (CD 20→50 %) | SE 고체상 σ_ion, τ_Laplace ~1.3–3.5 | ⛔ **위상이 반대** (그들의 전달상 = 공극, 우리 = 고체 SE).  ★ 그러나 **τ 가 압밀과 함께 급등한다**는 방향은 `ngandjong2021` (1.55→1.95) 과도, 우리 σ_ion-vs-ε 와도 **정합** |
| **DEM 물성** | ⛔ 0건 | E_eff 1.35 GPa(연화 프록시) | 비교 불가 |
| **소성** | ⛔ 0 | MPM 진짜 SHAPE 소성 (champion E 1.53 / σ_y 0.15) | **frame[5] 재확인** — 2024 AEM 급 논문도 **압밀의 소성 절반이 없다** |
| **불확실도** | ⛔ seed 0 · 오차막대 0 · 앙상블 0 | LOOCV · Bayesian PI · nested CV · bootstrap band | ★ **우리가 명백히 앞선다.**  [Vijay25] 는 앙상블 4-모델이라도 있었다 |
| **실험** | ⛔ 신규 0 | Minnmann · Cronau · Bazzoun · Lee2025 | ★ **우리가 앞선다.**  ⚠ 그들 DL 의 기준선이 DEM 이므로 **DL 오차는 DEM-vs-실험 오차 *위에* 쌓인다** — 그 크기는 이 논문에 **없다** |

### 7-4. ★ 방법 규율로 흡수할 것 (숫자가 아니라 이것)

1. **"두 층 검증"(Fig 3) 을 그대로 채택** — 픽셀/복셀 지표(MSE·R²)와 **물리 기능지표**(porosity·τ·접촉면적)를
   **항상 같이** 보고한다.  이 논문이 잘한 일이고, 그 대비에서 *"기능지표 <5 % 인데 계면 10–15 %"* 라는
   **자기 한계가 스스로 드러났다**.  우리 예측기(§8)에도 같은 이중 보고를 건다.
2. **hold-out 을 *구조 단위* 로** — micro IV 는 **7 CD 전부** 테스트다.  우리 코퍼스의 case-level
   hold-out(같은 침대의 다른 압력)보다 **엄격**하다.  ⇒ 우리 ML 도 **침대 단위 hold-out** 을 하나 두자.
3. **외삽 금지 구간을 논문에 적는다** — 저자가 *"CD 20–50 % 밖은 비물리적일 수 있다"* 고 스스로 적었다.
   우리 Stage 22.5 의 **φ_AM < 0.3 외삽 금지** 가드(CLAUDE.md)와 같은 규율.

---

## 8. 적용 인사이트 (내 연구에 어떻게)

1. **★★ springback 추세를 우리 MPM 의 *반증 가능한 표적* 으로 등재.**
   `derived(ours)` **CD 25/35/45 % → spring-back 4.8 / 7.6 / 10.1 %p** (압축두께 대비 6.3/11.5/17.7 %).
   ⚠ LIB·CBD 계라 **값은 전이 금지, 부호와 곡률만**: *"압축이 깊을수록 회복률(%)이 커진다"*.
   우리 `--protocol hold` 는 **정지 후 고정**이라 이 축을 **원리적으로 못 낸다** ⇒
   `--protocol release`(목표 도달 후 플래튼 상승) 팔이 필요하다.  **플래튼 정지 트랙이 닫힌 뒤.**
2. **★ 150-차원 병목 = surrogate 설계의 경고등.**  우리가 나중에 시간-surrogate 를 만들면
   **"잠재차원 / 복셀 수" 비를 먼저 적어라.**  이 논문은 4,813:1 이고, 그 결과가
   **벌크 3–5 % / 계면 10–17 %** 의 이원적 정확도다.  우리가 재는 것(**접촉면적·coverage·협착**)은
   전부 **계면 쪽**이므로 **같은 아키텍처를 쓰면 우리 축에서 가장 크게 틀린다.**
3. **★ trivial baseline 을 *반드시* 같이 싣는다** (§10-⑦ 실측).  micro IV(완전 hold-out) porosity 에서
   **"다른 전극들의 같은 CD 평균"** 이라는 3 초짜리 기준선이 DL 을 **이긴다**(4.01 % vs 4.18 %).
   ⚠ **동시에 반대 방향도 기록**: 확산도·τ 에서는 DL 이 **압도적으로 이긴다**(7.17 vs 30.32 % · 5.85 vs 13.79 %).
   ⇒ **양 없이 "DL 이 잘한다/못한다" 를 말하면 둘 다 틀린다.**  우리 예측기 보고서에 같은 표를 붙인다.
4. **가속 배수 인용 규약의 두 번째 사례** (§10-⑨).  [Vijay25] 는 배수를 **한 번도 안 썼고** 유도하면
   사슬 전체 1.1× 였다.  이쪽은 **188× 를 썼고 단계 단위로는 사실**이다 —
   그러나 `derived(ours)` **손익분기 = 583 step = 3.4 전극-스윕 = 학습셋 자신의 크기**,
   그리고 **GeoDict 솔브 · CGPD 상류 · Optuna 500 trial 은 분모에 없다**.
   ⇒ 우리 규약: *"배수 = (분자 단계 / 분모 단계), 손익분기, 남는 물리비용"* 3 개를 항상 같이.
5. **복셀 규약 게이트** (§7-2-③).  우리가 MPM/DEM 구조를 복셀로 넘길 때
   **"이 복셀 porosity 는 ε_sphere 인가 union 인가"** 를 매니페스트에 적는 키를 하나 둔다.
   이 논문은 그것을 안 적어서 **자기 본문(19.07 %)과 자기 그림(≈2.7 %)이 어긋난 채 출판됐다**.

---

## 9. 인용 가능 문장 (deck / paper 용)

> **[안전 — stated]**
> "Galvez-Aranda et al. (Adv. Energy Mater. 2024, 2400376) trained a 1D-CNN on 3-frame lags of
> voxelised DEM calendering trajectories (76×76×125 voxels at 0.4 µm) of an NMC111 96 % / CBD 4 %
> electrode and reproduced the microstructure evolution — including the spring-back on platen
> release — at 15 s per step versus ≈47 min per step for the DEM."

> **[안전 — stated]**
> "Their DL-predicted microstructures reproduced DEM porosity, pore-network diffusivity and
> tortuosity factor to within a few percent, while the phase-boundary contact areas carried the
> largest error (up to 16.8 %); the authors themselves note that the interfaces between phases
> 'can still be improved'."

> **[우리 프레임 — 가장 쓸모 있는 문장]**
> "A state-of-the-art DL surrogate of the calendering stage reproduces BULK descriptors (porosity,
> tortuosity) to ~3–5 % but phase-INTERFACE descriptors only to ~10–17 %. Since the quantities our
> transport model depends on (Tabor/Stage-E contact area, Holm constriction, SE coverage) are all
> interface quantities, this asymmetry — not the headline accuracy — is the transferable result."

> **[비판 — 반드시 `derived(ours)` 로 표시]**
> "`derived(ours)`: on the single fully-held-out electrode (microstructure IV, 7 CD values), a
> trivial baseline — the mean porosity of the other electrodes at the same compression degree —
> matches the DEM test data as well as the DL model does (4.01 % vs 4.18 % mean relative error).
> The DL model earns its keep on diffusivity and tortuosity (7.2 % vs 30.3 % and 5.9 % vs 13.8 %),
> not on porosity."

> ⛔ **쓰면 안 되는 문장**
> - *"DL 이 접촉면적·porosity·확산도·springback 을 훨씬 싸게 예측한다"* — §3-A 가 반박한다
>   (확산도는 별도 FV 솔브, springback 은 숫자 없음).
> - *"R² 가 항상 90 % 이상"* — Fig 6b 최저 ≈87.2 % (§10-④).
> - *"오차가 0.5–9.8 %"* — 자기 SI 에 13.76 · 14.71 % 가 있다 (§10-③).
> - *"τ 오차 ±5 %"* — 11 중 5 건이 초과, 최대 12.41 % (§10-③).
> - **porosity 19–31 % 를 우리 ASSB 값과 나란히 놓기** — 액체계 LIB.

---

## 10. 주의 / 한계 — over-claim 방지 + **내가 잡은 내부 불일치 전수**

### ① ★ **R² 정의가 구조 충실도를 증명하지 못한다** (trap #2 — 사용자 지시 검사)
식 (3)의 분모는 `Σ(v_g − v̄)²` = **그 프레임 복셀 라벨의 *공간* 분산**이고, 라벨은 **0/1/2/4** 다.
**void = 4** 가 전극 위 큰 덩어리를 차지하므로 **분산의 큰 몫이 "전극이 어디까지 차 있나"(= 두께)** 에서 나온다.
⇒ **두께와 spring-back 만 맞히면 R² 의 대부분을 벌 수 있다.**
논문은 **전극 내부로 한정한 R² 도, 상별 R² 도, IoU/Dice 같은 형태 지표도** 보고하지 않는다.
★ **그리고 실제로 그 패턴이 데이터에 있다** — 벌크 3–5 % vs 계면 10–17 %.
⚠ **축 스팬 직접 확인 결과**: Fig 5c 는 **y 90–100**, Fig 6b·6d 는 **y 80–100** 로 패널마다 다르고,
둘 다 *"거의 100"* 처럼 보이게 한다.  Fig 7 확산도는 **선형 0–20** 인데 값은 **17 → 0.9 (19배)** 로 붕괴하므로
**CD ≥ 30 % 의 모든 점이 축 아래 5 % 에 뭉친다**: micro IV @30 % 의 **14.71 % 상대오차는 축 높이의 2.5 %**,
micro III @45 % 의 **13.76 % 는 0.75 %** 로 **눈에 보이지 않는다**.  ⇒ **로그축이면 드러날 오차가 가려져 있다.**

### ② ★★ **복셀 라벨 부기가 자기 자신의 porosity 표와 안 맞는다** (내가 잡은 가장 큰 불일치)
Fig 5b (micro I @45 %) 를 디지타이즈하면 (`digitized — TREND only`):

| 시점 | AM | CBD | Pores | Void | 합 |
|---|---|---|---|---|---|
| 프레임 0 | 4.40 | 1.19 | 1.63 | 0 | **7.22 ×10⁵ = 722,000 ✓** |
| 최대압축(≈15) | **3.42** | 0.65 | **≈0.00** | 3.10 | 7.17 |
| 완화(30) | 3.95 | 0.78 | 0.13 | 2.37 | 7.23 |

- **(a) AM 복셀이 보존되지 않는다**: 4.40 → **3.42**(−22.3 %) → 3.95(−10.2 %).
  AM 은 고체상이고 복셀 부피는 고정인데 **22 % 가 사라졌다 되돌아온다** ⇒
  **복셀이 겹침(union)을 세고 있다**는 서명.  이것은 우리가 아는 **ε_union vs ε_sphere 규약 문제**
  (CLAUDE.md: `MPM관례 − ε_sphere = 1.251 %p`) 의 **같은 병, 훨씬 큰 크기**다.
- **(b) 라벨 porosity 와 Table S2 porosity 가 안 맞는다**:
  프레임 0 = 1.63/7.22 = **22.6 %** vs Table S2 의 micro-I @CD20 **31.09 %** (−8.5 %p);
  완화 = 0.13/4.86 = **2.7 %** vs Table S2 @CD45 **19.07 %** (**−16.4 %p, 7배**).
  ⇒ **어긋남이 압축과 함께 *커진다*.**
- ⇒ ★ **결론**: Table S2 의 porosity/확산도/τ 는 **CNN 이 실제로 내는 76×76×125 라벨 격자와
  같은 표현 위에서 계산된 것일 수 없다.**  (다른 해상도인지, void 를 공극에 넣는지, CBD 내부
  나노공극을 더하는지 — **논문이 말하지 않는다.**)
  ⚠ **이것은 치명적이다** — *"기능지표 오차 <5 %"* 라는 검증이 **CNN 출력에서 한 단계 떨어진
  표현 위에서** 이뤄졌다는 뜻이기 때문이다.

### ③ **자기 SI 가 자기 본문을 반박한다 (오차 크기)**
- 본문: *"relative error … oscillates in the order of 0.5 % – 9.8 %"* (porosity·확산도).
  **SI 실측**(n=11, `derived(ours)`): porosity 0.65–**7.24** % (✅ 범위 안) ·
  확산도 0.00–**14.71** % (**2 건이 9.8 초과**: III@45 13.76, IV@30 14.71).
- 본문: *"tortuosity … error of ± 5 %"*.  **SI 실측**: **11 중 5 건 초과**, 최대 **12.41 %**(IV@30).
  평균 4.92 %.
- 결론부: *"기능지표 오차는 5 % 미만"* — **위 두 줄로 반박된다.**

### ④ **"R² always above 90 %" 가 그림과 안 맞는다**
§3.2 의 문장은 micro I 에 대한 것인데 §3.2 마지막이 이를 *"the different microstructures"* 로 일반화한다.
**Fig 6b(micro II @35 %)의 최저점이 ≈87.2 %** 로 90 선 아래에 명확히 찍혀 있다 (spring-back 직전 프레임).

### ⑤ ★★ **추론 프로토콜 — Fig 3 과 Fig 5c 가 서로 다른 말을 한다** (§7-2-① 상세)
- **Fig 3 은 rollout 이라고 쓴다**: 출력 상자 `Output: μStructure Morphology (s₄ → s_m)`
  + 입력 상자 `s₁ s₂ s₃ CD %`.  즉 **세 프레임 + CD 만으로 궤적 끝까지**.
- **Fig 5c 의 R² 궤적은 rollout 답지 않다**: 0/1/2 = **정확히 100**(입력 lag) → 3/4/5 = 95.6/93.7/**92.2**
  → **프레임 9 = 정확히 100 복귀** → 16–18 = **91.7** → 21 이후 **96.7–96.9 평탄**.
  Fig 6b 도 **87.2 → 99.5–99.8 복귀**.  자기회귀는 **보통 오차가 단조 누적**된다.
- **두 읽기**: (a) 실제 채점은 **one-step-ahead(teacher-forced)** 였다 —
  그렇다면 **DEM 을 어차피 돌려야 하므로 "188×" 의 surrogate 해석이 무너진다**;
  (b) 진짜 rollout 인데 **CD 조건화가 자기보정 통로를 준다** (§4-3-③: 입력의 1/4 이 목표 CD 상수).
  ★ (b)도 원리적으로 가능하므로 **단정하지 않는다.**
- ⚠ **Methods (§2.3–2.5·2.7) 에 어느 쪽인지 한 줄도 없다.**  ⇒ **인용 시 반드시 이 불확실성을 함께 적을 것.**
- ★★ **갱신 2026-09-11 — 자매편(건조)에서 *rollout 의 실측 서명* 을 확보했다.  읽기 (a) 가 강화된다, 단 단정은 아니다.**
  정본: `galvezaranda2025_paml_vgg16_dem_slurry_drying` (§0 · §4-4).  그쪽은 **명백한 free-running rollout** 이다 —
  본문이 *"the DL is fed using the following 4 microstructures (TF = 2, 3, 4, and **5**)"* 라고 적고(TF 5 = **모델 자신의 출력**),
  **Fig 3 이 색으로 못 박는다**: 검은 원 = DEM 참값은 **1,2,3,4 네 개뿐**이고 5\*/5/6\*/6/…/21 이 **전부 회색(모델 산출)**.
  ★ **그리고 그 rollout 의 R² 는 단조 붕괴한다** (nDEM=0 팔: 0.83 → TF 16–19 에서 **≈0.0**; nDEM=5000 도 TF 19 에서 0.69 까지).
  ⇒ **여기 Fig 5c 의 "92.2 → 프레임 9 에 정확히 100 복귀" 와 Fig 6b 의 "87.2 → 99.5 복귀" 는 그 서명과 정반대 모양**이다.
  ⚠⚠ **그렇다고 이 논문이 teacher-forced 라고 단정하지 않는다** — 다른 논문·다른 조건화이고, 읽기 (b)(CD 상수가
  입력의 1/4 를 차지해 자기보정 통로를 준다)가 **원리적으로 여전히 가능**하다.  그리고 이쪽은 **복셀 격자**를,
  저쪽은 **입자 좌표**를 뱉으므로 누적 기전 자체가 다를 수 있다.
  ⇒ **판정 = "미해결, 단 (a) 쪽으로 기울었다."**  **인용 규약**: *"추론 프로토콜 미기재 — 자매편(건조)의 rollout 서명과
  R² 모양이 어긋난다"* 를 함께 적고, **188× 를 surrogate 가속으로 쓸 때는 그 조건을 명시**한다.
- ⚠ 참고로 **train/val 손실이 사실상 같다는 것(§5-1)도 같은 방향의 경고**다 — 3-lag 이웃 프레임끼리는
  거의 동일한 구조라 val 분리가 실질적이지 않다.

### ⑥ **데이터셋 개수 부기가 세 군데에서 어긋난다**
- §2.1: *"Four synthetic electrodes … seven CD … total of 28 calendering simulations"*
- §2.4: *"divided randomly into training (24) and testing (4). **An additional dataset** … 7 calendering
  degrees for the same initial microstructure"*
- §3.2 / Table 2: *"testing dataset consists of **11 TS** … four different initial microstructures"*,
  그 중 **micro IV 는 training 칸이 비어 있다**(7 CD 전부 테스트).
⇒ **자기일관 독법**: 전극 **5 개**(28 + 7 = **35 런**), train 24 / test **11**, micro IV = 추가 5번째 전극.
⚠ **"Four synthetic electrodes" 라는 §2.1 문장과 어긋난다** (train 전용 4번째 전극은 Table 2 에 안 나온다).
- **검증 분할도 모순**: §2.3 *"20 % of the training dataset … as validation"* vs
  §2.4 *"training and validation in a ratio of 90 to 10"*.  **80:20 vs 90:10.**

### ⑦ ★★ **trivial baseline 이 없다 — 그래서 내가 두 개 만들어 돌렸다** (사용자 지시 검사 #1)
논문은 **어떤 기준선도 제시하지 않는다** (persistence / 선형보간 / 전극평균 / 상수).
`derived(ours)` 로 두 개를 구성해 **micro IV(완전 hold-out, n=7)** 에서 비교:

**기준선 B1 = "다른 전극들의 *같은 CD* 훈련값 평균"** (미세구조를 아예 안 본다)

| 양 | **DL 평균 상대오차** | **B1 평균 상대오차** | 승자 |
|---|---|---|---|
| **porosity** | **4.18 %** | **4.01 %** | ⛔ **B1** (7 점 중 3 점에서 DL 이 진다; CD 40 % 는 0.97 vs **7.24 %** 로 대패) |
| 확산도 | **7.17 %** | 30.32 % | ✅ DL (4.2배) |
| τ | **5.85 %** | 13.79 % | ✅ DL (2.4배) |

**기준선 B2 = "같은 전극 안에서 CD 선형보간"** (I@45, II@35, III@25, III@45, n=4)

| 양 | DL | B2 | 승자 |
|---|---|---|---|
| porosity | **2.18 %** | 5.14 % | ✅ DL |
| 확산도 | **5.68 %** | 17.01 % | ✅ DL |
| τ | **3.30 %** | 29.41 % | ✅ DL |

⇒ ★★ **정확한 판정 (양방향)**:
**porosity 에서는 DL 이 3 초짜리 기준선을 못 이긴다** — porosity 는 사실상 **CD 만의 함수**라
전극 정체를 몰라도 맞힐 수 있다.  **반면 확산도·τ 에서는 DL 이 크게 이긴다** — 이 둘은
CD 20→30 % 에서 **퍼콜레이션성 붕괴**를 겪어 전극마다 다르므로, **미세구조를 보는 모델만 맞힐 수 있다.**
⚠ 공정하게: DL 은 micro IV 의 **실제 프레임을 lag 로 본다**(B1 은 안 본다) ⇒ **정보가 더 많다.**
**더 많은 정보를 가지고도 porosity 에서 지는 것**이 여기서 진짜 의미 있는 관측이다.
⚠ **B3(persistence = 직전 프레임 복사)는 우리가 못 돌렸다** — 프레임별 복셀 데이터가 없다.
그러나 **`derived(ours)` 프레임당 두께 변화가 1.43 % 뿐**이므로 persistence 는 R² 축에서
**매우 강한 경쟁자**이고, **논문은 그것을 시험하지 않았다.**  ⇒ **R² ≈95 % 의 의미는 미정.**

### ⑧ **Fig 7h 와 Table S2 가 계열이 뒤바뀌어 있다**
micro IV 확산도: **Table S2** = CD20 (test 15.26, DL 14.41) · CD25 (11.00, 11.94) · CD30 (3.40, 2.90).
**Fig 7h** 는 세 점 모두 **빨간 ✕(DL)가 초록 ●(DEM_test) 반대편**에 찍혀 있다 (CD20 에서 DL 이 위, CD25 에서 아래, CD30 에서 위).
**Fig 7g(porosity, 같은 전극)는 Table S2 와 일치**하므로 **불일치는 7h 에 국한**된다.
⇒ 값의 **크기**는 두 곳이 같으므로 §3-A/§10-⑦ 의 오차 크기는 유효하지만,
**DL 편향의 *부호* 는 확산도 축에서 판정할 수 없다.**

### ⑨ ★ **가속 배수의 분모** (사용자 지시 검사 #3)
**논문이 준 것**: DL 15 s/step, DEM ≈47 min/step ⇒ **188×** (단계 단위, 하드웨어 미기재).
**논문이 주지 않은 것** (`derived(ours)`):
- **학습 데이터 생성 비용**: train 580 프레임 × 47 min = **454 h = 18.9 일** (직렬).
  전체 35 런은 855 프레임 × 47 min = **670 h = 27.9 일**.
- **손익분기**: 절감 = 2805 s/step ⇒ **583 step 을 대체해야 본전** = **3.4 전극-스윕**
  = ★ **학습셋 자신의 크기(24 TS = 3.4 스윕)와 정확히 같다.**
  ⇒ *"이 surrogate 는 자기가 먹은 만큼 더 만들어야 본전이고, 그 다음부터 이익"*.
  **[Vijay25] 의 1.1× 보다 훨씬 낫다 — 이것은 정직한 긍정 평가다.**
- **분모에 없는 것 3 가지**: (i) **GeoDict DiffuDict 솔브** — 확산도·τ 를 얻으려면 DL 출력에도
  똑같이 돌려야 하고 **비용 미보고**; (ii) **상류 CGPD 슬러리+건조** — 대체되지 않음;
  (iii) **Optuna 500 trial × 1000 epoch + 663.7 M 파라미터 학습** — **비용 미보고**.
- **(iv) 그리고 ⑤ 가 맞다면 188× 는 surrogate 가속이 아니다.**

### ⑩ 기타 한계 (저자 자인 포함)
- **외삽 불가**: CD 20–50 % 밖은 *"비물리적 거동"* 가능 (저자).  우리 300 MPa 축과 매핑 불가.
- **전이 미검증**: 조성 1 종(NMC111 96/2/2) 전용.  graphite/LFP/blend 는 *"ongoing work"*.
- **데이터·코드 비공개**: *"Research data are not shared."*  ⇒ **재현 불가.**
- **seed/앙상블/오차막대 0**.  **불확실도 정량 0.**
- **실험 신규 0** — 검증 전체가 **DEM 대비**.  DEM-vs-실험 오차는 ref [36] 에 있고
  **이 논문에 재인용되지 않는다** ⇒ **DL 의 실제 물리 오차는 이 논문으로 알 수 없다.**
- **CBD 를 단일 라벨로** 다룬다 — 나노공극·점탄성 없음 (`hong2026_cbd_viscoelasticity_springback`
  이 보인 **시간의존 spring-back 의 지배 기전**이 모델에 아예 없다).

---

## 11. 기술 미니-용어집 (이 논문을 읽는 데 필요한 것만)

- **CD (Compression Degree)** — *건조* 전극 두께 대비 감소율 %.  **압력이 아니다.**
  압연 현장에서 실제로 설정하는 양(롤 갭)에 가깝다.  ⇒ Heckel 축(P)과 **직접 변환 불가**.
- **Spring-back (Sb)** — 압력 해제 후 전극이 되튀는 탄성 회복.  실무에서 목표 밀도를 맞출 때
  **과압축(over-calendering)으로 보상**해야 하는 양.
- **CBD (Carbon-Binder Domain)** — 카본블랙 + 폴리머 바인더를 **하나의 유효상**으로 뭉뚱그린 것.
  Franco 그룹 표준.  내부 나노공극(보통 40–50 %)을 **가정**으로 넣는 경우가 많다.
- **CGPD (Coarse-Grained Particle Dynamics)** — 슬러리·건조를 조립화 입자로 푸는 MD 계열.
  이 사슬에서 DEM 압연의 **초기구조 공급자**.
- **1D-CNN 시간-surrogate** — 3D 격자를 1D 배열로 펴서 **시간 축에만** 컨볼루션을 거는 구조.
  공간 국소성은 conv 가 아니라 **출력 dense 층**이 암기한다 ⇒ **150-차원 병목**이 곧 표현력 상한.
- **Teacher forcing vs free-running rollout** — 시계열 모델 평가의 두 방식.
  전자는 매 스텝 **실제** 과거를 먹이고(오차 누적 없음), 후자는 **자기 예측**을 먹인다(누적).
  **surrogate 를 주장하려면 후자여야 한다.**
- **McMullin 수** — `N_M = σ_bulk/σ_eff`.  `τ = N_M × ε` (식 6).
  ⚠ 문헌에 `τ = N_M · ε` 와 `τ² = N_M · ε` 두 규약이 섞여 있어 **τ 절대값 비교 시 규약 확인 필수**.
  이 논문의 τ 가 **9.7 → 85.3** 으로 매우 큰 것도 규약과 CBD 처리에 크게 걸린다.
- **GeoDict DiffuDict** — Math2Market 의 복셀 기반 확산 유한체적 솔버.
  우리 STEP3 (`voxel_conductivity.py` / `step3_sigma.py`)와 **원리적으로 같은 종류**.
- **Optuna** — 베이지안 하이퍼파라미터 탐색 프레임워크(TPE).  trial = 한 세트 평가 1 회.

---

## 12. 미해결 / 다음에 할 것

1. ✅ ★★ **digest 완료 2026-09-11 — 자매편 3 (건조)**: Galvez-Aranda, Fernandez, Franco,
   *"Physics-Assisted Machine Learning for the Simulation of the Slurry Drying in the Manufacturing Process of
   Battery Electrodes: A Hybrid Time-Dependent VGG16-DEM Model"*, ***ACS Appl. Mater. Interfaces* 17 (2025)
   32150−32162**, DOI `10.1021/acsami.4c23103` (특집 *Machine Learning for Materials Chemistry*).
   → **정본 카드 `papers/galvezaranda2025_paml_vgg16_dem_slurry_drying.md`** · 비교노트 **F-DL5**.
   ⚠ 이 PDF 의 참고문헌 51 편에 없던 것이 맞다 (2024-01 접수 vs 2025-01 접수) — **서지는 이제 확정**이다.
   ★★ **여기서 확인하라고 적어 둔 세 가지가 전부 답해졌다**:
   - ① **VGG16 은 DEM 루프 *안*** — 단 힘 계산 대체가 아니라 **프레임 건너뛰기**다.
     DL 이 **한 칸(1,500,000 step = 75 µs)** 을 통째로 점프시키고 **nDEM(5,000–10,000) 진짜 DEM step** 이
     그 pseudo-구조를 물리 위로 **투영**한다 = **predictor–corrector / multiple-time-stepping**.
   - ② **rollout 확정** (= 위 §10-⑤ 갱신의 근거).  **teacher forcing 이 아니다.**
   - ③ **압력/응력 축 ⛔ 없다** — 본문·SI 전수 grep 에서 `MPa` **0회**, `stress` **0회**, `pressure`(응력) **0회**.
     공정 축은 **시간 프레임(75 µs/칸)** 뿐.  ⇒ ★ **이로써 이 사슬 3편(슬러리·건조·압연) 어느 것도 MPa 를
     들지 않는 것이 확정**됐고, 우리 300 MPa·`P_y = 138 MPa` 로의 전이점은 **여전히 0 개**다.
   ★ 그 카드가 추가로 준 것: 🧮 **정직 end-to-end 가속 4.77× · Amdahl 천장 6.67×**(시드 프레임 15 %) ·
   🧮 **손익분기 13.9 런**(학습셋 11 런의 1.27배) · ⚠⚠ **"exceptional generalization" 근거 그림(Fig 8)이
   학습 조성 그림(Fig 6)의 행 치환 복사본**(32 칸 중 23 칸) · ⚠ **MAE 단위 미기재(1,000 배 갈림)** ·
   ★ **길이-1 conv · 항등 max-pool 3 개** 라는 **이 카드가 잡은 것과 똑같은 구조 병리의 재발**.
2. ✅✅ **확보·digest 완료 2026-09-11 → 정본 카드 `papers/xu2023_realistic_am_shape_cgmd_calendering.md`**
   (ref [36] Xu, Ngandjong, Liu, Zanotto, Arcelus, Demortière, Franco, *J. Power Sources* 554 (2023) 232294)
   — ⚠ **그 카드가 이 카드의 상속 서술 두 곳을 바꾼다**:
   ① **압력축은 거기에도 없다** — 본문·SI 전수 `MPa` **0 회**, 유일한 `Pa` 는 슬러리 배로스탯 10⁵ Pa,
      공정 축은 **CD 0–42.2 %** 뿐이고 **포화하지 않은 채 끝난다**(dε/dCD ≈ −0.9 %p/%) ⇒ **floor 판정도 불가**.
      ⇒ 아래 ③ 의 *"이 사슬 3편 어느 것도 MPa 를 들지 않는다"* 는 **물리 엔진 원점까지 포함해 확정**됐고,
      계보에서 MPa 축을 가진 것은 **`ngandjong2021_dem_calendering_digital_twin` (0–156 MPa) 하나뿐**이다.
   ② ⛔ **상속받은 "τ 실험 검증" 은 독립 검증이 아니다** — Xu 2023 SI 가 **dilation–erosion 인자를 {1,2,3} 복셀 중
      τ 의 µ-XCT 값(2.65)에 가장 가까운 **2**(τ = 2.47)로 고르고 *"to process **all** the results"* 라고 적는다.
      ⇒ 이 카드 §4-1·§10 의 *"already validated … tortuosity factor and porosity"* 인용에 **이 문장을 병기**할 것.
      (**porosity 상속은 유효**하다 — dilation–erosion 은 부피보존이라 porosity 에 거의 무관하고, exp 8 점 대조가 독립이다.)
   ③ ★ **거기서 얻는 것은 형상 축**: Krumbein 구형도 모드가 CD 36–42 % 에 **−0.04 ~ −0.06** 만 이동 ·
      같은 porosity 에서 실형상 τ 가 구 근사의 **1.55–2.40배** · 전체볼륨 대비 서브볼륨 **RVE 편향 +5.1 → +12.0 %**.
   (아래는 확보 전 기록 — 지우지 않는다.)
   ✅ **서지 교차확인 완료 2026-09-11**: 자매편(건조)에서는 **ref [33]** 번호로 같은 논문을 인용하고,
   제목은 *"Lithium ion battery electrode manufacturing model accounting for 3D realistic shapes of active
   material particles"* 다.  그 논문 감사문에 *"Jiahui Xu … the **DEM code used in her PhD thesis work**"* 로
   적혀 있어 **이 사슬 3편의 DEM 물리가 전부 그 한 편 소유**임이 확정됐다.
   이 논문의 **DEM 물리 전체**(접촉법칙·E·ν·µ·COR·CT 입자형상)와
   **유일한 실험 검증**(τ·porosity)이 거기 있다.  ⇒ **DEM 파라미터가 필요하면 진입점은 그쪽.**
   `ngandjong2021_dem_calendering_digital_twin`(ref [25], 압력축 0–160 MPa 보유)과 **어디가 바뀌었는지**를
   대조하는 것이 우리에게 가장 값진 후속.
3. ⬜ **persistence 기준선(B3)** — ⚠ **자매편(건조)에서도 똑같이 판정 불가였다**(그쪽 §10-⑧: 프레임별 좌표
   미공개).  ⇒ **이 그룹 두 편 연속으로 trivial baseline 이 0 개**다.  프레임별 복셀 데이터가 공개되지 않아 못 돌렸다.
   ⇒ 우리 자신의 시간-surrogate 를 만들 때는 **B3 를 1번 기준선으로 고정**한다
   (프레임당 두께 변화 1.43 % ⇒ B3 는 매우 강하다).
4. ⬜ **우리 `--protocol release` 팔** (§8-①) — springback 축을 낼 수 있게 플래튼 상승 구간 추가.
   ⚠ **선결: SR 트랙 2(플래튼 정지 결함) 종결** (`docs/mpm_platen_kinematic_stop_defect.md` ·
   `docs/reviews/fam_platen_prereg_20260812.md`).
5. ⬜ **복셀 porosity 규약 키** (§8-⑤) — 매니페스트에 `porosity_convention: {sphere_sum|union|voxel_label}`
   을 강제.  이 논문의 §10-② 가 그 부재의 교과서 사례다.

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

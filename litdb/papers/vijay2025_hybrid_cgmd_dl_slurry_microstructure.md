<!-- digest 표준 양식. ★ = 사용자가 특히 원한 항목. COMPREHENSIVE / paper-level STANDALONE digest. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md / alabdali2023_cgmd_wet_manufacturing_ssb_cathode.md -->
# CGMD 슬러리 궤적의 **앞 절반**을 보고 **평형 미세구조를 예측**하는 딥러닝 surrogate(Slurry-NN)를 ARTISTIC CGMD/DEM 제조 사슬에 끼워 넣다 — NMC-111 / LFP / **ASSB(NMC-622+argyrodite)** 3계 — Vijay / Galvez-Aranda / Zanotto / Le-Dinh / Alabdali / Asch / Franco (Energy Storage Materials 2025)

> slug `vijay2025_hybrid_cgmd_dl_slurry_microstructure` · DOI `10.1016/j.ensm.2024.103883` · type `CGMD(LAMMPS, LJ + granular-Hertz) + DEM 압연 + 지도학습 DL 시간-surrogate(CNN×2 + MLP×2 앙상블, "Slurry-NN")` · PDF `43b5cb04-______simulation_deep_learning_2025_ESM.pdf` (+ SI `1s2.0S2405829724007098mmc1.docx`) · digested `2026-09-11` · status ✅

> elements: Li
> methods: elastic

---

## 0. 이 논문이 우리에게 *왜* 중요한가 — 그리고 **어디까지만** 중요한가 (positioning)

**한 문장**: 이 논문은 **우리 파이프라인의 *상류*(슬러리·건조)에 대한 *시간-surrogate*** 이고,
**우리의 두 반쪽(DEM=접촉망 transport / MPM=소성 morphology) 중 어느 쪽도 하지 않는다.**

- **소재계 접점**: 세 chemistry 중 하나가 **ASSB = NMC-622 + argyrodite** 로 우리 족과 같다.
  ⚠ 그러나 **ASSB 는 슬러리 단계에서만 등장**한다 — 이 논문에서 압연(DEM)까지 간 것은
  **NMC-111(액체계 LIB)** 뿐이다.  **ASSB porosity 는 단 한 개도 보고되지 않는다.**
- **계보 접점**: Franco 그룹(LRCS, ARTISTIC) 라인이다.  정본 카드 **`alabdali2023_cgmd_wet_manufacturing_ssb_cathode`**
  (= 본 논문 ref **[36]**, ASSB 슬러리의 출처)와 **`ngandjong2021_dem_calendering_digital_twin`**
  (= ref **[35]**, 압연 DEM 의 출처)의 **직계 후속**이다.  즉 물리 엔진은 전부 그 두 편이 소유하고,
  **이 논문의 신규성은 그 위에 얹은 DL 한 층뿐**이다.
- **우리에게 쓸모 있는 층**: 물리가 아니라 **방법 규율**이다 — ① *"trivial baseline(부피 스케일링)을
  같이 싣고 DL 이 지는 칸을 그대로 보고한다"*, ② *"NN 이 뱉은 입자배치는 겹침 때문에 후속 물리
  솔버를 깨뜨린다"* 는 **실패 모드의 1차 기록**, ③ RDF↔**Fréchet 거리**라는 값싼 구조유사도 게이트.
- **⛔ 우리에게 쓸모 **없는** 층**: σ 삼중항 0, τ 0, 접촉면적 0, coverage 0, 압력 0, Heckel 0,
  소성 0, 실험 0, 코드·데이터 공개 0.  **porosity 41–54 %** 는 액체 전해질 LIB 가 *원하는* 값이라
  우리 ASSB 10–16 % 와 **절대비교 금지**.

⇒ **한 줄 판정**: *"우리가 흡수할 것은 이 논문의 **숫자**가 아니라 **세 개의 음성 결과**다 —
(a) 위치-MAE 를 최소화하는 DL 은 **수가 많은 작은 상(CBSA)** 을 맞추고 **AM–AM 상관을 잃는다**
(ASSB 에서 trivial 스케일링에 **1.80× 진다**), (b) ★ **그림을 직접 보면 더 세다 — 예측 RDF 와
trivial 아핀-스케일 RDF 가 9/9 패널에서 겹치고 둘 다 타깃과 반위상이다**(DL 이 줄인 격차는 남은
Fréchet 의 **≤9 %**) ⇒ *"구조 완화를 배웠다"가 아니라 "아핀 축소를 재현했다"*, (c) 저자들이 초록에
쓴 "accelerate" 는 **한 번도 수치로 제시되지 않는다** (유도 상한 = 슬러리 단계 **≈2×**, 사슬 전체 **≈1.1×**).*

⚠ **반대 방향의 정정도 하나 있다 (비판은 양방향)**: LFP 전이 실패(부피 39 %)는 **신경망 탓이 아니다** —
Fig 4d 잔차 기울기 **+0.127** 이 Table 6 의 선형 부피오차 **11.3 %** 와 정확히 닫힌다 ⇒
**옆에 붙은 2-파라미터 해석식** `f(t)=a+b·t^(−1/6)` 하나가 100 % 원인이다 (§5-3-3).

---

## 1. 한 줄 요약

LAMMPS **CGMD**(bead = AM / SE / CBSA)로 만든 전극 **슬러리** 궤적 20 프레임 중 **앞 10 프레임**만
주고, **20번째(평형) 프레임의 입자 좌표 (x,y,z)** 를 예측하는 앙상블 신경망 **Slurry-NN**
(CNN 2개 + MLP 2개)을 학습해, 그 예측 미세구조를 **점도(NEMD) → 건조(CGMD) → 압연(DEM)** 로
이어지는 기존 ARTISTIC 사슬에 **그대로 투입**해도 최종 물성이 깨지지 않음을 보인 논문.
학습 = **NMC-111 슬러리 50 런**(32/8/10 분할), 전이 시험 = **LFP 10 런 + ASSB 10 런**.
결과: 정규화 위치 **MeanAE 0.017(NMC-111 test) / 0.018(LFP) / 0.020(ASSB)**,
점도 **2.398 → 2.359 Pa·s (−1.63 %)**, 압연 porosity 는 두 방법의 **95 % CI 가 전 압축도에서 겹침**
(단 5/5 압축도에서 hybrid 가 일관되게 **더 높다**, 평균 **+0.67 %p**).

---

## 2. 메타

| 항목 | 값 |
|---|---|
| 제목 | **A hybrid modelling approach coupling physics-based simulation and deep learning for battery electrode manufacturing simulations** |
| 저자 | **Utkarsh Vijay**ᵃ·ᵇ, **Diego E. Galvez-Aranda**ᵃ·ᶜ, **Franco M. Zanotto**ᵃ·ᶜ, **Tan Le-Dinh**ᵃ·ᶜ, **Mohammed Alabdali**ᵃ·ᶜ, **Mark Asch**ᵈ, **Alejandro A. Franco**ᵃ·ᵇ·ᶜ·ᵉ·\* |
| 소속 | ᵃ **LRCS** UMR CNRS 7314, Université de Picardie Jules Verne, Amiens · ᵇ **ALISTORE-ERI** FR CNRS 3104 · ᶜ **RS2E** FR CNRS 3459 · ᵈ **LAMFA** CNRS UMR 7352 (수학) · ᵉ **Institut Universitaire de France** |
| 교신 | **Alejandro A. Franco** (alejandro.franco@u-picardie.fr) |
| 저널/년 | **Energy Storage Materials 75 (2025) 103883** · received 19 Jul 2024 · revised 15 Oct 2024 · accepted 3 Nov 2024 · online 3 Nov 2024 |
| DOI / PII | **10.1016/j.ensm.2024.103883** / **S2405829724007098** |
| 라이선스 | **CC BY (open access)** — 2405-8297 © 2024 The Authors, Elsevier |
| 키워드 | Li-ion batteries · Electrode manufacturing process · Electrode microstructure · Physics-based simulation · **Physics-informed deep learning** |
| 자금 | EU H2020 **MSCA-COFUND DESTINY** #945357 · **ERC PoC #101069244 (SMARTISTIC)** · France 2030 **ANR-22-PEBA-0002 (PEPR BATMAN)** · Horizon Europe **#101069686 (PULSELiON)** · Région Hauts-de-France · IUF |
| 감사문 | **Marc Duquesnoy** 의 ML 기여를 명시 (현 소속 이전) |
| 연구유형 | **순수 시뮬레이션 + ML**.  ⚠ **이 논문에서 수행한 실험은 0건** (FF 보정에 쓰인 유변학·밀도 실측은 ref [39] Lombardo 2020 / [36] Alabdali 2023 에서 상속) |
| 모델 시스템 | ① **NMC-111** 슬러리(LIB) ② **LFP** 슬러리(LIB) ③ **ASSB = NMC-622 / argyrodite** 슬러리 — 전부 **양극** |
| 상(phase) | **AM** / **SE**(ASSB 만) / **CBSA**(carbon–binder–solvent aggregate; 건조 후 **CBD**) + 공극 |
| 코드/데이터 공개 | ⛔ **없음** — data availability 문장 자체가 없고, 저장소 링크·학습 스크립트·입력 파일 어느 것도 제공되지 않는다 |
| SI | `mmc1.docx` (5쪽 상당) — S1.1 FF 정의식, S1.2 입력변수 근거, **Table S1** BO 범위, **Table S2** k-fold CV, **Figure S1** 손실곡선, **Table S3** 런별 metric 30행 |

### 2-1. 정본 litdb 안 형제 카드 (중복 판정 근거)

`git ls-tree FETCH_HEAD litdb/papers/` **전수 목록(252편)** 과 `git grep -i 'S2405829724007098|103883|Vijay|hybrid modelling|CBSA'`
로 확인 — **본 논문의 카드는 정본에 없었다**(신규).  인접 카드는 아래 4편:

| 본 논문에서의 역할 | 정본 카드 |
|---|---|
| ref **[36]** = ASSB 슬러리 모델의 출처 (같은 그룹 "0번 원기") | `alabdali2023_cgmd_wet_manufacturing_ssb_cathode` |
| ref **[35]** = 압연 DEM 의 출처 | `ngandjong2021_dem_calendering_digital_twin` |
| 같은 그룹의 ML-생성기 계열 (porosity 를 *입력*으로 쓰는 반대 방향) | `duquesnoy2020_calendering_ml_mesostructure_generator`, `duquesnoy2023_ml_multiobjective_manufacturing_optimization` |
| 같은 그룹의 ASSB 제조모델 후속 (구형 AM → 실형상) | `wet_processing_resolved_am_ssb_cathode_manufacturing` |

⚠ ref **[28]** (Galvez-Aranda, *Adv. Energy Mater.* 2400376, "Time-dependent deep learning
manufacturing process model") = **압연 단계의 DL 자매편**이고 **정본 litdb 에 아직 없다** →
`_INDEX_proposals.md` 후보 (§12).

---

## 3. 핵심 수치 (전부 **stated**; `derived(ours)` 는 명시)

### 3-1. DL 성능 (Table 5 · Table 7 · Table S3)

| 양 | NMC-111 | LFP | ASSB | 비고 |
|---|---|---|---|---|
| 학습/검증/시험 런 수 | **32 / 8 / 10** | — / — / **10** | — / — / **10** | 분할 비 64/16/20 % |
| Avg. **MeanAE** (train) | **0.010** | — | — | 정규화 좌표 |
| Avg. MeanAE (validation) | **0.010** | — | — | |
| Avg. **MeanAE (test)** | **0.017** | **0.018** | **0.020** | ★ 헤드라인 |
| Avg. MedianAE (test) | 0.009 | 0.015 | 0.011 | |
| Avg. **MSE** (test) | **0.307** | **0.198** | **0.441** | ⚠ §10-C — **MeanAE 와 같은 척도일 수 없다** |
| 대표 단일 런 (Table 7) | 0.013 / 0.007 / 0.319 | 0.018 / 0.015 / 0.199 | 0.019 / 0.010 / 0.456 | MeanAE/MedianAE/MSE |
| k-fold CV MeanAE (Table S2) | 3-fold **0.994** / 5 **0.993** / 7 **0.991** (train) · **0.998 / 0.996 / 0.996** (val) | — | — | ⚠ **비정규화**(µm) 척도 |
| 🧮 `derived(ours)` **물리 단위** 위치오차 | train/val **≈ 1.0 µm** · **test ≈ 1.7 µm** | ≈ 2.2 µm | ≈ 1.4 µm | §10-D — **figure-read 로 좌표 스팬을 확정한 뒤** 재유도 (구 "55 µm 정육면체 가정" 판은 폐기) |

### 3-2. 부피·밀도 외삽 (Table 6) — **DL 이 아니라 해석식 `f(t)=a+b·t^(−1/6)` 의 성적**

| chemistry | V_target [10⁵ µm³] | V_extrap | %diff | ρ_target [g/cm³] | ρ_extrap | %diff |
|---|---|---|---|---|---|---|
| NMC-111 (test) | 1.63 | 1.64 | **0.82** | 0.872 | 0.865 | **0.80** |
| **LFP** (test) | 1.71 | **1.18** | **38.91** ⚠ | 2.011 | **2.890** | **35.87** ⚠ |
| **ASSB** (test) | 1.79 | 1.80 | **0.76** | **1.415** | 1.400 | **1.06** |

- 🧮 `derived(ours)`: 질량 보존이므로 **ρ 오차는 V 오차의 역수 재표현일 뿐 독립 검증이 아니다**
  (대칭 %diff 는 역수 불변: `%diff(1/a,1/b) = %diff(a,b)`; 표의 0.82↔0.80 / 38.91↔35.87 차이는 3자리 반올림).
- 🧮 `derived(ours)` + **figure-read (Fig 4)**: parity plot 축이 **비정규화**이고 좌표가
  NMC-111 **±50** · LFP **±60** · ASSB **±35** 까지 간다 ⇒ **가로 스팬 ≈ 100 / 120 / 70 µm**.
  부피와 합치면 상자는 **정육면체가 아니라 얇은 슬래브**다 — 예: NMC-111 이 100×100 이면 두께
  `1.63e5/1e4` ≈ **16.3 µm** (전극 캐스팅 기하로 타당).  ⚠ **논문은 상자 치수를 한 번도 주지 않는다.**

### 3-3. 슬러리 유변 (§3.3)

| 양 | 값 |
|---|---|
| 전단율 | **24 s⁻¹** |
| η (CGMD only) | **2.398 Pa·s** |
| η (Slurry-NN + CGMD) | **2.359 Pa·s** |
| 차이 | **1.63 %** |
| ⚠ 전제 | **예측 구조를 그대로 NEMD 에 넣으면 입자 손실(particle loss)** → **CGMD 평형화 1 스텝이 필수** |

### 3-4. 압연 porosity (Table 9, **NMC-111 × 8 시드 쌍**)

| 압축도 | CGMD (S) 평균 | S 표준편차 | Slurry-NN+CGMD (P) 평균 | P 표준편차 | 🧮 Δ = P−S |
|---|---|---|---|---|---|
| **0 %** | 53.53 | 0.70 | 53.71 | 0.64 | **+0.18** |
| **15 %** | 49.65 | 1.15 | 50.70 | 0.99 | **+1.05** |
| **20 %** | 47.14 | 1.26 | 48.02 | 1.30 | **+0.88** |
| **25 %** | 44.50 | 1.31 | 44.85 | 1.33 | **+0.35** |
| **30 %** | 41.14 | 1.25 | 42.02 | 1.23 | **+0.88** |

- 저자 판정: *"95 % 신뢰구간이 각 압축도에서 겹친다 → 두 방법 평균 사이에 유의한 차이 없음."*
- 🧮 `derived(ours)`: **부호가 5/5 모두 +** (평균 **+0.67 %p**).  ⚠ §10-E — 8개 **짝지어진**(같은 시드)
  런인데 **대응표본 검정을 하지 않고** 독립평균 CI 중첩으로 판정했다 = **가장 약한 검정**을 골랐다.

### 3-5. 계산비용 (Table 2 + §1) — **가속 배수는 논문에 없다**

| 단계 | wall time | 출처 |
|---|---|---|
| 슬러리 CGMD | **9 h** (NMC-111·LFP) / **10 h** (ASSB) · 본문은 "8–12 h" | Table 2 / §1 |
| 건조 CGMD | **24–36 h** | §1 |
| 압연 DEM | **≈ 6 h** | §1 |
| HPC | MatriCS (UPJV) 1 노드, 128 GB RAM, **Intel Xeon E5-2680 v4 @2.40 GHz × 2 (14 core)** | §2.1 |
| DL 학습·추론 | **노트북** i7-12700H @2.30 GHz, 32 GB RAM, Windows 10 Pro — ⛔ **학습시간·추론시간 미보고, GPU 언급 없음** | §2.3 |
| **가속 배수** | ⛔ **본문·SI 어디에도 없다** | — |
| 🧮 `derived(ours)` 상한 | 슬러리 단계 **≤ 2.0×** (20 프레임 중 10 프레임만 물리로 → 9 h → 4.5 h) · **사슬 전체 ≈ 1.10–1.13×** (39–51 h → 34.5–46.5 h) — 그나마 NEMD 전 **평형화 1 스텝**과 미보고 추론시간을 빼기 전 값 | — |

### 3-6. CGMD Force-Field (Table 1 **전문 전사**) — 단위는 LAMMPS `units micro`

> ε [pg µm² µs⁻²] = **1 fJ** · σ, r_c [µm] · k_n [pg µm⁻¹ µs⁻²] = **1 kPa** · γ_n [µm⁻¹ µs⁻¹] · X_µ 무차원
> (**1 pg µm⁻¹ µs⁻² = 1 kPa** 환산은 `alabdali2023…` 카드에서 이미 확립된 정본 환산)

| chemistry | 파라미터 | mean | std | lower | upper |
|---|---|---|---|---|---|
| **NMC-111** | AM(ε) | 1 | 0.088 | 0.834 | 1.263 |
| | AM(σ) [µm] | 0.879 | 0.082 | 0.634 | 1.029 |
| | AM(r_c) [µm] | 1.47 | 0.101 | 1.285 | 1.734 |
| | **Ø CBD solid** | **1.3** | – | – | – |
| | **Ø CBD (liquid)** | **7** | – | – | – |
| | ρ_CBD [g/cm³] | 0.9 | – | – | – |
| | CBD(ε) | 1 | 0.089 | 0.842 | 1.202 |
| | CBD(σ) | 0.989 | 0.107 | 0.924 | **0.930** ⚠ | *(평균 > 상한)* |
| | CBD(r_c) | 2.2 | – | – | – |
| | **k_n** | **3.31** | 1.04 | 1.697 | 5.460 |
| | **γ_n** | 29.70 | 2.56 | 25.028 | 36.216 |
| | **X_µ (마찰)** | **0.014** | 0.0008 | 0.013 | 0.017 |
| **LFP** | AM(ε) | 0.006 | 0.009 | 0.0003 | 0.03 |
| | AM(σ) | 0.18 | 0.16 | 0.1 | 0.6 |
| | AM(r_c) | 1.2 | – | – | – |
| | Ø CBD solid / liquid | 1.3 / **6.2** | – | – | – |
| | ρ_CBD | 0.95 | – | – | – |
| | CBD(ε) | **31.4** | 6.86 | 22 | 42 |
| | CBD(σ) | 0.315 | 0.29 | 0.100 | 0.850 |
| | CBD(r_c) | 2.8 | – | – | – |
| | **k_n** | **7.5** | – | – | – |
| | γ_n | 100 | – | – | – |
| | **X_µ** | **0.015** | – | – | – |
| **ASSB** | AM(ε) | 2.59 | 2.44 | 0.879 | 8.399 |
| | AM(σ) | 0.78 | 0.107 | 0.705 | 0.993 |
| | AM(r_c) | 1.5 | – | – | – |
| | **SE(ε)** | **46.46** | 45.73 | 0.973 | 89.824 |
| | **SE(σ)** | 0.910 | 0.105 | 0.711 | 0.987 |
| | **SE(r_c)** | 1.5 | – | – | – |
| | Ø CBD solid / liquid | 1.3 / **6.2** | (std 0) | – | – |
| | **ρ_CBD (liquid)** | **0.05** ⚠ | – | – | – | *(단위 공란; 타 chemistry 0.9–0.95 대비 19×↓)* |
| | CBD(ε) | 1.19 | 0.350 | 0.658 | **0.882** ⚠ | *(평균 > 상한)* |
| | CBD(σ) | 1.02 | 0.27 | 0.795 | 1.541 |
| | CBD(r_c) | 2.2 | – | – | – |
| | **k_n** | **5.65** | 2.40 | 1.342 | 9.829 |
| | γ_n | 30.05 | 8.20 | 26.018 | 52.607 |
| | **X_µ** | **0.012** | 0.005 | 0.0007 | 0.017 |

🧮 `derived(ours)` — **접촉 강성의 물리 크기**: `k_n ≡ (4/3)E*` 규약으로 읽으면
**E\*(NMC-111) ≈ 2.48 kPa · E\*(LFP) ≈ 5.63 kPa · E\*(ASSB) ≈ 4.24 kPa**.
⇒ 우리 AM(140 GPa)·Bazzoun E_CAM(161.5 GPa) 대비 **≈7.6 자릿수 아래**.
**이것은 "연화된 재료"가 아니라 *애초에 재료가 아닌* 유변학 피팅 계수**다 (§7-2, §10-G).

---

## 4. 시뮬레이션 방법 ★

### 4-1. 물리 엔진 = **CGMD (LAMMPS)** — 이 논문의 신규성 아님

- 앙상블 **NPT** (슬러리 평형), timestep **0.001 µs**, 총 **2×10⁷ step** = **20,000 µs**.
- 상호작용 **두 겹**:
  - **Lennard-Jones 12-6** (비접촉 인력·반발): `V(r) = 4ε[(σ/r)¹² − (σ/r)⁶]`, cutoff `r_c`.
  - **Granular Hertz (GH)** (접촉력): 법선 탄성 `k_n` + 접선 탄성 `k_t` + 점성감쇠 `γ_n, γ_t`
    + 접선변위 이력 + `X_µ` = 법선력 대비 접선력 최대비(= Coulomb 마찰계수).
    겹침 `θ` 가 0 이하이면 **힘 0**(SI Eq. 2 정의 그대로).
- 🧮 `derived(ours)` **pair style 동정**: 보고된 단위 지문 — `k_n` = 압력(pg µm⁻¹ µs⁻²),
  `γ_n` = **1/(길이·시간)** (µm⁻¹ µs⁻¹), `X_µ` 무차원 — 은 LAMMPS **`pair_style gran/hertz/history`**
  + **`units micro`** 와 정확히 일치한다.  ⚠ 논문은 pair style 이름을 **한 번도 쓰지 않는다**.
- **FF 보정 앵커**: *"슬러리 **밀도와 점도**를 실험에 맞춰 FF 를 피팅"* (ref [39] Lombardo 2020,
  PSO 기반).  ⇒ **이 논문 자체의 실험은 0건**, 앵커는 전부 상속.
- **데이터셋 다양성 주입**: AM 함량(**AM%**), 고형분(**SC%**), FF 파라미터 값을 실험 피팅값 주변
  **가우시안**으로 흔들었다.  ⛔ **AM%·SC% 의 실제 값과 범위는 어디에도 없다** — Table 1 은
  **FF 계수만** 싣는다 (§10-B).

### 4-2. 건조·압연 — **이 논문은 파라미터를 하나도 주지 않는다**

- **건조**: CBSA(용매 포함) bead 를 **수축**시켜 용매 증발을 흉내 → CBD.
  NMC-111 **Ø7 → 1.3 µm**, LFP·ASSB **Ø6.2 → 1.3 µm** (Table 1 에서 읽힘).
- **압연(calendering)**: **DEM**, 압축도 **15 / 20 / 25 / 30 %**.
  ⛔ **DEM 접촉법칙·E·ν·μ·반발계수(COR)·플래튼 속도·압력 — 전부 미보고.**  ref [35] Ngandjong 2021 로만 인용.
  ⇒ **압축 축이 "두께 감소율" 이라 우리 300 MPa / Heckel P_y 와 원리적으로 겹칠 수 없다.**
- **점도**: **NEMD**(비평형 MD) 전단, 24 s⁻¹, 설정은 ref [39] 의 것을 그대로 사용.

### 4-3. 입자 처리 ★ (= 우리 "무질서 처리"의 DEM 판)

| 축 | 이 논문 |
|---|---|
| 형상 | **구(bead)만**.  형상 자유도 0 |
| PSD | **AM = 실험 PSD 를 따름**(값 미보고, ref [39]) · **CBSA/CBD = 단분산**(1.3 / 6.2–7 µm) · **SE = 크기 미보고** |
| 강체 vs 소성 | **강체 구 + 순수 탄성 접촉**.  **항복 캡 없음 · 잔류겹침 없음 · 형상변화 없음** |
| 소성 사다리에서의 위치 | ⚠ **우리 DEM(hooke/hysteresis + Stage-E 소성면적)보다도 *아래*** — Thornton–Ning/EEPA 류의 **접촉 소성조차 없다** |
| 마찰 | **X_µ = 0.012–0.015** = 사실상 **무마찰**.  Bazzoun μ=0.4 대비 **≈30배 낮다** (슬러리 윤활 상태라 물리적으로는 타당하나, **압연 FF 는 별개**이고 미보고) |
| 결합/바인더 모델 | **없음**.  바인더는 **CBSA bead 의 LJ 우물**로 뭉뚱그려짐 (Sangrós 류 bond 모델 없음) |
| 주기경계 | x·y·z 주기 (image flag `ix,iy,iz` 가 입력 특징으로 쓰일 만큼 명시적) |
| 시드 | **초기 좌표 시드만 8개** (비교 실험용).  ⛔ FF 앙상블·격자수렴·오차막대 없음 |

### 4-4. ★★ 딥러닝이 *정확히* 무엇을 대체하나

> **답: force field 도 아니고, 초기배치 생성기도 아니다.
> → 한 CGMD 궤적의 *뒤 절반*을 건너뛰는 "시간-surrogate(forecaster)" 다.**

| 항목 | 내용 |
|---|---|
| **대체 대상** | 슬러리 CGMD 궤적 **frame 11 → 20** (평형까지의 뒷절반).  물리는 **frame 1–10 을 여전히 돌려야 한다** |
| **입력** | 입자 **n 개 × 10 프레임**: `X1 = (x,y,z)` · `X2 = (r, type)` (시간불변) · `X3 = (ix,iy,iz)` 이미지 플래그 |
| **출력** | **frame 20 의 (x₂₀, y₂₀, z₂₀)** — **좌표만**.  반경·타입은 그대로 복사, **상자 부피는 NN 이 아니라 해석식**이 준다 |
| **구조** | 앙상블 4개: **CNN M1**(위치, 3@10) · **MLP M2**(r·type) · **CNN M3**(이미지 플래그, 3@10) → 출력 concat → **MLP M4** → 예측 |
| **하이퍼파라미터** (Table 4, BO 선정) | M1: conv층 3, 필터 3, 커널 3 · M3: conv층 3, 필터 3, 커널 3 · M2: 층 1, 뉴런 **37** · M4: 층 2, 뉴런 **285** |
| **BO 탐색범위** (Table S1) | 커널 M1 **2–5** · 층 M2 **0–5** · 뉴런 M2 **2–50** · 커널 M3 **2–4** · 층 M4 **1–5** · 뉴런 M4 **75–300**.  ⚠ **conv 층수·필터수는 탐색범위에 없다**(Table 4 는 3 으로 보고) |
| **BO 설정** | scikit-optimize, **GP 회귀** 대리모델, **LHS** 초기표본 + 랜덤 후보샘플링.  ⛔ **BO 반복수·목적함수·BO 용 분할 미보고** |
| **최적화/손실** | **Adam**, lr **10⁻³**(기본), **200 epoch** 컷오프, 손실 = **MeanAE** |
| **왜 3갈래로 쪼갰나** | 특징 성질이 달라서(공간/범주/PBC) — 저자 표현으로 **ensemble learning** [42]; 과적합 방지 명분 |
| **전처리** | 전 데이터셋 **min–max 정규화 [0,1]** ("data snooping 회피" 목적이라 서술) |
| **후처리** | ① 상자 부피를 `f(t) = a + b·t^(−1/6)` 로 외삽(2-파라미터 피팅) ② 상자 밖 입자는 **가장자리로 wrap** ③ LAMMPS dump 포맷 재조립 ④ **OVITO** 시각화 |

⚠ **"physics-informed" 은 키워드에만 있다** — 손실에 물리항이 없고, 에너지/운동량 보존 제약도 없다.
저자 스스로 결론에서 *"energy conservation constraints [51] 같은 물리 제약을 넣으면 평형화 단계를
없앨 수 있을 것"* 이라고 **미래과제로** 적는다.  ⇒ **현행 모델은 순수 지도학습 회귀**다.

### 4-5. 검증 규약 ★

| 층 | 내용 | 판정 |
|---|---|---|
| **hold-out** | 시뮬레이션 단위 32/8/10 (NMC-111) | ✅ 누수 없는 분할 (입자 단위가 아니라 **런 단위**로 쪼갰다) |
| **k-fold CV** | 3 / 5 / 7-fold, Table S2 | ⚠ 값이 **0.991–0.998** 로 거의 안 움직인다 = **평균의 안정성**만 보이고 일반화 폭은 못 보인다.  게다가 **비정규화 척도**라 Table 5(0.010–0.017)와 나란히 못 읽는다 |
| **chemistry 전이** | LFP 10런 · ASSB 10런 **전량 test** | ✅ 가장 강한 검증층.  MeanAE 0.017 → 0.018 / 0.020 으로 **거의 안 나빠진다** |
| **trivial baseline** | frame-10 좌표를 외삽 부피로 **아핀 스케일링**("norm") | ✅✅ **이 논문의 가장 훌륭한 규율** — 그리고 **지는 칸을 그대로 싣는다**(§5-4) |
| **하류 물리 검증** | 점도(NEMD) · porosity(건조+압연) | ✅ 개념은 맞다.  ⚠ **NMC-111 만** |
| ⛔ 없는 것 | 학습곡선 대 데이터양 · 불확실도(UQ) · 앙상블 시드 · 물리 제약 · ablation(4갈래 중 무엇이 기여하나) | — |

---

## 5. 결과 — 절별 전수

### 5-1. §3.1 Slurry-NN 성능
train 0.010 ≈ val 0.010 < test 0.017 → 저자 판정 *"심한 과적합 증거 없음"*.
전이: LFP 0.018 · ASSB 0.020 "약간 높다".  Figure S1 의 손실곡선은 train/val 이 수렴·분기 없음.

### 5-2. §3.2.1 부피 외삽
NMC-111 0.82 % · ASSB 0.76 % 로 훌륭하고, **LFP 만 38.91 %** 로 무너진다.
⇒ 저자 스스로 §3.2.2 에서 LFP parity plot 의 이탈을 *"상자 크기 외삽 함수의 오차"* 로 귀속한다.
**즉 chemistry 전이의 실패는 DL 이 아니라 그 옆에 붙은 2-파라미터 해석식에서 났다.**
★ 우리가 **Fig 4d 를 직접 읽어 이 귀속을 정량적으로 닫았다**: LFP 잔차 띠의 기울기 **≈ +0.127**
= 선형 스케일 오차 **11.3 %** = `(1.18/1.71)^(1/3)` 에서 나오는 **11.28 %** 와 일치 (§5-3-3).

### 5-3. §3.2.2 위치 parity (Fig 4) — ★ **그림을 직접 보면 저자보다 많은 것이 나온다**

저자 서술: NMC-111·ASSB 는 45° 선에 잘 붙고 LFP 가 약간 벌어지며, 공통 이상점은 **PBC 를 넘나든 입자**.
아래는 우리가 `litdb/figures/…/fig_4.png` 를 **실제로 보고** 읽은 것 (`figure-read ≈`):

1. ★ **축이 비정규화(µm)** 이고 스팬이 **±50 / ±60 / ±35** 다 → §3-2 의 슬래브 기하와 위치오차 재유도의 근거.
2. ★ **이상점은 산포가 아니라 *딱 4개의 조밀한 덩어리*** 이고, 그 잔차 크기가 **상자 스팬과 같다**
   (NMC ≈ ±100, LFP ≈ ±115, ASSB ≈ ±50/±70).  ⇒ *"경계 반대편으로 감긴(wrapped) 입자"* 라는
   저자 귀속이 **정량적으로 확인**된다 (오차가 랜덤이 아니라 **정확히 한 상자 길이**).
3. ★★ **LFP 의 잔차는 무작위가 아니라 *기울어진 띠*** (Fig 4d): predicted −55 에서 잔차 ≈ −7,
   +55 에서 ≈ +7 ⇒ **기울기 ≈ +0.127** ⇒ target = predicted × 1.127 ⇒ **예측 좌표가 선형으로 11.3 % 작다.**
   🧮 이것은 Table 6 의 부피오차와 **정확히 닫힌다**: `(1.18/1.71)^(1/3) = 0.8872` ⇒ **11.28 % 작음**.
   ⇒ **LFP 열화의 100 % 가 상자-부피 외삽식 탓이고 신경망 탓이 아니다.**  (NMC·ASSB 의 잔차 띠는
   **기울기 없이 평평**하며, 이는 부피오차 0.82 / 0.76 % 와 정합.)
   ★ 이 항목은 **DL 에 유리한 방향의 정정**이다 — 비판은 양방향으로 정확해야 한다.
4. ⚠ **그런데 parity plot 자체가 오해를 부른다**: 동적 범위가 **상자 전체(±50 µm)** 인데 잔차 띠는
   **±2 µm** 폭이라 그림은 "거의 완벽"해 보인다.  그러나 그 ±1.7 µm 는 **최근접 접촉거리(RDF 1st peak
   ≈ 2.5 µm)의 약 68 %** 다.  ⇒ **Fig 4 는 구조 충실도의 증거가 아니다.  Fig 6 이 증거이고, Fig 6 은
   1st shell 너머가 틀렸다고 말한다** (§5-4).  ★ 우리 predictor 보고 규약에도 같은 함정이 있다 —
   parity/R² 는 **동적 범위를 크게 잡으면 항상 좋아 보인다.**

### 5-4. ★★ §3.2.3 RDF + Fréchet 거리 (Fig 6, Table 8) — **우리에게 가장 중요한 절**

RDF 3종(전체 AM+CBSA / AM–AM / CBSA–CBSA) × 3 chemistry, Gaussian σ=2 평활,
Δr_RDF = 0.075(전체·CBSA) / 0.600(NMC AM) / 0.500(LFP AM) / **0.400(ASSB AM)**.
**Fréchet 거리(FD)** 로 곡선 유사도 정량 — **낮을수록 유사**.

| chemistry | 비교 | 전체 입자 | **AM–AM** | CBSA–CBSA |
|---|---|---|---|---|
| **NMC-111** | Norm vs Target | 0.514 | 0.256 | 0.531 |
| | **Pred vs Target** | **0.471** ✅ | **0.209** ✅ | **0.485** ✅ |
| **LFP** | Norm vs Target | 0.570 | **0.194** | 0.657 |
| | **Pred vs Target** | **0.550** ✅ | **0.233** ❌ | **0.638** ✅ |
| **ASSB** | Norm vs Target | 0.439 | **0.314** | 0.492 |
| | **Pred vs Target** | **0.403** ✅ | **0.564** ❌❌ | **0.447** ✅ |

- ✅ = DL 이 trivial 스케일링을 이김 / ❌ = **짐**.  **9칸 중 2칸에서 지고, 둘 다 AM–AM 이며, 둘 다 전이 chemistry 다.**
- ★ **ASSB(= 우리 소재족)에서 DL 의 AM–AM FD 0.564 는 trivial 스케일링 0.314 의 1.80배**.
- 저자 서술: *"CBSA 입자는 수가 많아 전체 분포를 지배한다"*, *"짧은 거리에선 target 에 잘 붙고
  거리가 멀어질수록 벌어진다 … 단거리 상관은 잘 배웠으나 장거리는 추가 국소환경 정보가 필요"*.

#### ★★★ 그림을 직접 보고서야 보이는 것 (`fig_6.png`·`fig_7a.png` 를 실제로 열어 읽음, `figure-read ≈`)

**FD 표만 보면 "DL 이 7:2 로 이겼다" 로 읽히는데, 곡선을 보면 이야기가 다르다.**

1. ★★★ **9개 패널 전부에서 Normalized(빨강)와 Predicted(파랑)가 사실상 겹쳐 있다.**
   그리고 **둘 다** Target(초록)과 **첫 번째 배위껍질 너머에서 위상이 어긋난다**.
   ⇒ **DL 은 "궤적 뒷절반의 구조 완화"를 배운 것이 아니라 사실상 *아핀 축소*를 재현했다.**
   🧮 여백 크기로 확인: 잔여 FD(≈0.40–0.66) 대비 DL−norm 개선폭은 **0.020–0.046** =
   **남은 격차의 최대 ≈9 %** 뿐이다 (NMC 전체 8.4 % · LFP 3.5 % · ASSB 8.2 % · CBSA 8.7/2.9/9.1 %).
   ⇒ **정확한 문장은 "DL 이 이겼다"가 아니라 "DL 과 trivial 이 같은 답을 냈고, 둘 다 타깃에서 멀다"** 이다.
2. ★★ **어긋남의 *형태*가 특정된다 — 중거리 껍질이 ~10–15 % 부풀어 있다.**  Fig 6a·7a (NMC-111, AM+CBSA):
   **1st peak 는 위치(r ≈ 2.5 µm)·높이(≈2.05)가 세 곡선 모두 일치**하는데, 2번째 이후 껍질은
   Target 이 ≈4.4 / 6.3 / 8.3 / 10.2 µm(간격 ≈1.9–2.0), 예측·norm 이 ≈5.0 / 7.2 / 9.4 / 11.6 µm
   (간격 ≈2.2) 에 온다.  ⇒ **접촉거리는 맞고 중거리 구조만 팽창**해 있다 = **메소 스케일에서 덜 조밀하다.**
   ★ 이 부호가 **§5-6 의 porosity 결과와 일치한다** — hybrid 가 5/5 압축도에서 **더 높은 porosity**
   (덜 조밀).  두 독립 관측이 같은 방향을 가리킨다.
3. ★★ **평형화 1 스텝은 이 어긋남을 고치지 못한다** (Fig 7a): "Before"(파랑)와 "After"(빨강)가
   **육안으로 구분 불가**이고 둘 다 Target 과 여전히 반위상이다.  ⇒ 평형화는 **겹침만 푼다**.
4. ⚠ **LFP 의 AM–AM 패널(6e)은 사실상 잡음이다** — y 축이 **0.98–1.025**, 즉 g(r) 이 1 에서 **±2 %**
   밖에 안 벗어난다.  ⇒ 거기서의 FD 0.194 vs 0.233 비교는 **구조가 아니라 잡음 두 곡선의 비교**다.
5. ★ **ASSB 의 AM–AM 패널(6h)에는 진짜 구조가 있다** — 1st peak Target ≈2.45, norm ≈2.1,
   **predicted ≈2.0** (r ≈ 1.5–2 µm), 이어 깊은 최소 ≈0.38 (r ≈ 4), 2nd peak ≈1.25 (r ≈ 7), r>15 에서 평탄.
   ⇒ **DL 이 AM–AM 첫 배위껍질의 높이를 가장 크게 과소평가**하고 그것이 FD 0.564 로 나타난다.
   ✔ 즉 ASSB 의 ❌ 는 **실체가 있는 패배**다 (LFP 의 ❌ 와 달리).
6. ⚠ **FD 계산 규약이 미보고다** — 패널마다 x 범위가 **15 / 80 / 100 / 120 µm** 로 다른데
   축 스케일링(무차원화) 방법을 밝히지 않는다.  ⇒ **패널 간 FD 비교는 방어 불가**,
   **같은 패널 안의 norm↔pred 비교만** 유효 (다행히 우리가 쓰는 비교가 그쪽이다).
7. ⚠ **6b·6e 의 x 축(120 / 100 µm)이 상자 스팬(≈100 / 120 µm)의 절반을 크게 넘는다.**
   최소이미지 규약에서 `r > L/2` 의 g(r) 은 의미가 없다 ⇒ 그 구간의 ±0.02 진동은 유한크기 잡음이다.

- 🧮 **우리 해석 (§8-①)**: **위치 MAE 한 개를 최소화하면 *수가 많은 상*이 손실을 지배한다.**
  AM 은 소수·대형이라 MAE 에 거의 기여하지 않고, 그래서 **패킹·퍼콜레이션을 정하는 바로 그 상관이
  학습신호에서 사라진다.**  전체·CBSA 지표만 보면 "DL 승"으로 보이는 것이 함정이고,
  **위 1번(= DL ≈ trivial)** 이 그 함정의 가장 강한 형태다.

### 5-5. §3.3 점도
2.398 → 2.359 Pa·s (**−1.63 %**).  ⚠ **단, 예측 구조를 바로 NEMD 에 넣으면 입자 손실이 나서
CGMD 평형화 1 스텝이 필수**였다.  저자 귀속: *"예측 위치가 서로 너무 가까워 겹침 → 입자간 힘 불균형 → 내부 충돌"*.
평형화 전후 분포 차이는 작다(Fig 7a).

### 5-6. §3.3 porosity (Fig 7b, Table 9)
두 방법 모두 압축도↑ → porosity↓ 단조.  95 % CI 전 구간 중첩 → *"유의차 없음"*.
결론 절에서 저자 스스로 *"순수 물리 방법이 hybrid 보다 약간 **낮은** 값을 준다"* 고 인정 (= 우리 §3-4 Δ 부호와 일치).

---

## 6. Figure set ★ (전수 + 우리가 쓸 것)

> 🖼 크로핑본 = `litdb/figures/vijay2025_hybrid_cgmd_dl_slurry_microstructure/` (fig_1…7 + tab_1,3,7,8,9).
> **👁 = 이번 digest 에서 이미지를 *실제로 열어 본* 그림** (Fig **4 · 6 · 7**).  나머지는 **캡션·본문 기준**이며
> 그 행에는 그림에서만 읽은 값을 적지 않았다.

| Fig | 무엇을 보이나 | 우리가 쓸 수 있는 것 |
|---|---|---|
| **1a** | 기존 ARTISTIC 사슬: 슬러리(CGMD) → 건조(CGMD) → 압연(DEM) → porosity·**tortuosity factor** | 우리 STEP1→STEP2→STEP3 과 1:1 대응시킬 **공정-사슬 도식**의 외부 선례.  ⚠ τ 는 **그림 라벨에만** 있고 이 논문은 숫자를 안 낸다 |
| **1b** | 새 사슬: 슬러리 앞 10프레임 → **Slurry-NN** → 예측 구조 → 점도/건조/압연 | ★ 우리가 MPM 시간-surrogate 를 그릴 때 그대로 베낄 **삽입 지점 도식** |
| **2a–c** | 데이터 텐서 구성: `X`(런×입자×10프레임×특징) → `X1`(좌표)/`X2`(r,type)/`X3`(image flag), `Y`(frame 20 좌표) | ★ **특징을 물리 의미별로 쪼개 별도 망에 먹이는 설계**의 그림 설명 — 우리 predictor 의 "유도량 곱 금지" 규율과 같은 계열의 사고 |
| **3** | Slurry-NN 구조도 (CNN M1 · MLP M2 · CNN M3 → concat → MLP M4) | 앙상블 배선도 |
| 👁 **4a–f** | target-vs-pred / residual-vs-pred 산점도 ×3 chemistry.  **축은 비정규화 µm**(±50/±60/±35) | ★ **세 가지를 우리가 직접 읽었다** (§5-3): 스팬 → 슬래브 기하 · 이상점 4덩어리의 잔차 = **정확히 한 상자 길이**(PBC wrap) · **LFP 잔차 기울기 +0.127 = 부피외삽 11.3 % 오차와 닫힘**.  ⚠ 동시에 **parity plot 의 함정**(범위가 상자라 ±1.7 µm 오차가 완벽해 보임) 의 교보재 |
| **5a–c** | 3D 미세구조 3종 비교(target / norm / predicted) + AM 분포, 차이나는 곳에 **원 표시** | ⚠ 저자도 *"눈으로는 차이가 유의하지 않다"* 고 적는다 ⇒ **3D 스냅샷은 검증이 아니다**는 좋은 반례 |
| 👁 **6a–i** | RDF 9패널 (전체 / AM–AM / CBSA–CBSA) × 3 chemistry.  범례 = Normalized / Predicted / Target | ★★★ **이 논문에서 가장 값진 그림.**  §5-4 의 7개 figure-read 가 전부 여기서 나온다 — **빨강·파랑이 겹치고 둘 다 초록과 반위상**, **1st peak 만 일치**, **중거리 껍질 간격 2.2 vs 1.9–2.0 µm**, LFP AM–AM 은 **±2 % 잡음**, ASSB AM–AM 은 **진짜 구조(1st peak 2.45 vs 예측 2.0)** |
| 👁 **7a** | 예측 구조의 평형화 **전/후** + **Target** 을 RDF 로 비교 (캡션은 Target 을 언급 안 함) | ★ **"평형화는 겹침만 풀고 구조는 못 고친다"** — Before/After 가 육안 구분 불가이고 둘 다 Target 과 반위상 |
| 👁 **7b** | porosity vs 압축도, S(파랑)/P(빨강) 평균 + 오차막대 + CI 밴드 | ⚠ 값 자체는 LIB 라 전이 불가.  ★ 그림에서 **P 밴드가 전 구간 S 밴드 위**에 있는 것이 보인다 = §3-4 의 Δ 5/5 양수와 같은 관측 |
| **S1** | 학습/검증 손실곡선 (200 epoch) | ⚠ **비정규화 MAE** 라 본문 Table 5 와 척도가 다르다고 캡션이 직접 밝힌다 |

---

## 7. 우리 DEM+MPM 대비 ★  →  `our_dem_baseline.md` · `comparison_vs_ours_DEM.md`

### 7-1. 축별 대조

| 축 | 이 논문 | 우리 | 판정 / 이유 |
|---|---|---|---|
| **역할 (frame[5])** | **어느 반쪽도 아님** — 우리 파이프라인의 **상류**(슬러리·건조)와 그 위의 **메타층**(surrogate) | DEM = 접촉망 transport / MPM = 소성 morphology | **보완적이지만 겹치지 않는다.**  "누가 이긴다"의 문제가 아니다 |
| **압밀 제어** | **변위(두께 감소율 15–30 %)** · 압력 **0건** | DEM servo **300 MPa** · MPM `hold`(응력-정지) | ⛔ **Heckel·P_y·σ-vs-P 어느 것과도 겹칠 수 없다** |
| **porosity** | **53.5 → 41.1 %** (NMC-111 + 액체 전해질) | ASSB **10–16 %** (real_14 15.6) | ⛔ **절대비교 금지.** LIB 는 30–40 % 공극을 *원한다*(전해질 자리) — `comparison_vs_ours_DEM.md` §A 의 [Duquesnoy20] 항목과 **같은 게이트** |
| **접촉법칙** | LJ + **Hertz(순수 탄성)** + 이력 접선 + Coulomb `X_µ`.  **항복 캡 없음** | hooke/hysteresis(캡 없음) + **Stage-E 소성면적 재유도**(Tabor+volume) | 우리가 **한 층 위**.  이 논문은 접촉 소성조차 없다 |
| **재료 물성** | ⛔ **E·ν·σ_y·COR 한 개도 없다.**  `k_n` 3.31–7.5 **kPa** 급 유변 피팅계수뿐 | E_CAM 140 · E_SE real 24 / **eff 1.35**(DEM) / **1.53**(MPM) · σ_y 0.15–0.30 GPa | ★★ **철학이 다르다**: 그들 = 물성 없음, 우리 = **물성 명시 + 물리적 연화 프록시**.  §7-2 |
| **마찰** | **0.012–0.015** (사실상 무마찰) | Bazzoun 계열 μ = 0.4 | 슬러리라 타당하나 **압연 FF 는 미보고** ⇒ 그들 porosity 의 패킹 해석 자체가 불가 |
| **입자 형상** | **구만** | DEM 구 / **MPM 은 진짜 형상 소성** | 우리 MPM 이 메우는 바로 그 구멍 (frame[1]/[2]) |
| **전달 (σ_ion/σ_e/κ)** | ⛔ **0건** | 접촉망 Kirchhoff+Holm 삼중항 + STEP3 복셀 FV | **우리 압승**.  이 논문은 transport 를 재지 않는다 |
| **tortuosity** | Fig 1a 라벨에만 존재, **수치 0건** | τ_Laplace / τ_Dijkstra / pore-τ | — |
| **접촉면적·coverage** | ⛔ 0건 | Hertz/Tabor 2밴드 + Stage-E | — |
| **실험 앵커** | ⛔ **이 논문 0건** (FF 앵커는 ref [39]/[36] 상속) | Minnmann 10 %@300 · Cronau overlap · Bazzoun EIS | **우리 앵커가 더 두껍다** |
| **ML 방법론** | hold-out + 3/5/7-fold + **chemistry 전이 test** + **trivial baseline 동봉** | 해석적 LOOCV(hat) · **중첩 CV**(항·λ·기저족 전부 폴드 안) · leverage 게이트 · Laplace PI | 우리가 규율은 더 엄격.  ⚠ **그들이 우리에게 앞서는 한 칸 = trivial baseline 을 *항상* 같이 싣고 지는 칸을 보고한다** |
| **재현성** | ⛔ 코드·데이터·입자수·AM%·SC%·PSD·DEM 파라미터 전부 미제공 | 리포·prereg·원장·digest | **재현 불가** |

### 7-2. ★ frame[2] "유효 프록시" 3종 분류 (이 논문이 세 번째 종을 채운다)

| 종 | 정체 | 예 |
|---|---|---|
| **(i) 실재 물성을 *연화*** | 물성이 있고, 빠진 기전(재배열·GB 슬립·미세파괴)을 **E 로 lumping** | **우리 DEM E_SE 24 → 1.35 GPa (18×)**, MPM 1.53 |
| **(ii) 단계마다 FF 를 *교체*** | 물성이 없고, 공정 단계 사이에 상호작용 계수를 통째로 갈아끼움 | **[Alabdali23]** 슬러리→건조 LJ 우물 ×19–455, k_n ×1000, µ ×780 |
| **(iii) 애초에 물성이 *존재하지 않음*** | bead 강성이 **유변학(밀도·점도) 피팅 파라미터**.  탄성률로 읽을 의도 자체가 없음 | **이 논문** — `k_n` 3.31–7.5 kPa (`derived` E\* ≈ 2.5–5.6 kPa) |

⇒ **우리 18× 연화를 방어할 때 이 3종 표가 유용하다**: 우리는 *물성을 명시하고 그 위에 프록시를
얹었기 때문에 **반증 가능**하다*.  (ii)·(iii)은 어떤 실험 물성과도 대조할 수 없다.

### 7-3. ★★ 가져다 쓸 수 있는 것 / 못 쓰는 것 (칼같이)

**✅ 쓸 수 있다 (전부 *방법*, 값 0개)**

1. **시간-surrogate 라는 삽입 지점 자체** — "앞 절반 프레임 → 평형 프레임" 회귀.
   우리 MPM 압밀(수 시간~수십 시간 GPU)에 같은 자리가 있다.
   ⚠ **선행조건**: 우리의 정지 프레임 문제(`docs/mpm_platen_kinematic_stop_defect.md` rev1–6,
   prereg `fam_platen_prereg_20260812.md`)가 **아직 안 닫혔다** — surrogate 는 *타깃*을 배우는데
   우리 타깃(정착 porosity)이 **정지 시점의 함수**다.  ⇒ **그 축이 닫히기 전에 학습하면
   인공물을 학습한다.**  이건 이 논문의 결함이 아니라 **우리 쪽 선결조건**이다.
2. **trivial baseline 동봉 규율** — "DL 을 쓸 근거는 DL 이 *단순식을 이겼다*는 표"다.
   우리 `ml_design_structure.py`(free-knob 곱항 판정)와 같은 정신이고, **보고 양식**을 가져올 수 있다.
3. **구조 유사도 게이트 = RDF + Fréchet 거리** — 5-phase 계획 **Phase 4**(예측 수치 → 2D/3D 미세구조 합성,
   `extract_2d_microstructure.py synthesize_microstructure`)의 **합격 기준**으로 바로 쓸 수 있다.
   ★ 단 **상별로 따로** 재야 한다 (§8-①).
4. **음성 결과 ①: NN 산출 좌표는 물리 솔버에 바로 못 들어간다** (겹침 → 입자 손실 → 평형화 1스텝 필수).
   우리 대응물: 합성/예측 구조를 `network_conductivity.py` 나 STEP3 에 넣으면 겹침이
   **Holm 접촉반경 `r_c`** 와 **ε_sphere** 를 동시에 오염시킨다 ⇒ **겹침 검사 게이트**가 선행돼야 한다.
5. **음성 결과 ②: 좌표만 예측하면 부족하다** — 상자 부피를 별도 해석식에 맡겼고 **거기서 깨졌다**(LFP 39 %).
   우리 판: **porosity 를 회귀로 예측하지 말고 `ε = C − φ_SE − φ_AM` 로 계산하라**는 기존 규율
   (CLAUDE.md, `use_porosity_pct` 학습 금지)과 **같은 교훈의 독립 사례**.

**⛔ 못 쓴다**

1. **모든 porosity 값** (41–54 %, 액체계 LIB).  2. **모든 FF 계수** (kPa 급 유변 피팅, 물성 아님).
3. **"가속" 주장** — 배수가 없고, 유도 상한이 사슬 전체 **1.1×** 다.  4. **ASSB 관련 어떤 압밀·전달값**
(ASSB 는 슬러리에서 멈춘다).  5. **σ/τ/접촉면적/coverage** — 없다.  6. **압력 축** — 없다.
7. **DEM 파라미터** — 없다.  8. **실험 대조** — 없다.

---

## 8. 적용 인사이트 (내 연구에 어떻게)

**① ★★★ 점-오차(MAE)는 구조를 보증하지 않는다 — 상별 구조지표를 surrogate 의 *합격 기준*으로 못박는다.**
이 논문이 실측으로 보여준 것 두 겹:
- (표 층) 전역 위치-MAE 를 최소화하면 **개수가 많은 상**이 손실을 지배해 **소수·대형 상(AM)의 상관이
  무너진다** — ASSB 에서 AM–AM FD **0.564 vs trivial 0.314**.
- (그림 층, 우리가 직접 확인) 그보다 더 강한 사실 — **예측 RDF 와 trivial 아핀-스케일 RDF 가 9/9 패널에서
  겹치고, 둘 다 1st shell 너머에서 타깃과 반위상이다.**  DL 이 줄인 격차는 **남은 FD 의 ≤9 %**.
  ⇒ *"DL 이 물리를 배웠다"* 가 아니라 *"DL 이 아핀 축소를 재현했다"* 가 정확한 서술이다.
우리 Phase 3–4(설계→전-메트릭 예측 → 미세구조 합성)에서 **정확히 같은 함정**이 기다린다:
우리 침대의 개수 분포는 SE ≫ AM (real_14 = SE 32,832 vs AM 457 ≈ **72:1**) 이라 **개수비가 이 논문보다
더 극단**이고, 우리는 그 AM 골격 위에서 **퍼콜레이션과 σ 를 읽는다.**
⇒ **게이트 (제안)**: 합성·예측 구조는
 (a) **AM–AM** · (b) **SE–SE** · (c) **AM–SE** RDF 를 *따로* 재고,
 (d) **trivial baseline**(아핀 스케일 / RSA 재배치)을 **셋 다** 이겨야 하며,
 (e) 잔여 FD 자체가 baseline 대비 **의미 있는 비율**로 줄어야 한다 (이 논문의 ≤9 % 는 "사실상 동률"),
 (f) 우리에겐 **전달 게이트**가 추가로 붙는다 — 배위수 **Z** · 퍼콜 **f_p** · **σ_ion** 이 같이 통과해야 한다.
⚠ 그리고 **parity plot/R² 로는 이 실패가 안 보인다** (§5-3-4): 동적 범위를 상자 전체로 잡으면
±1.7 µm 오차도 완벽해 보인다.  **우리 predictor 대시보드의 parity 패널에도 같은 경고를 붙일 것.**

**② ★★ "가속 배수"는 *기준선을 명시*하지 않으면 보고하지 않는다.**
이 논문은 초록·서론·결론에서 "accelerate" 를 4번 쓰지만 **배수를 한 번도 쓰지 않는다**.
유도해 보면 슬러리 단계 **≤2×**, **사슬 전체 ≈1.10–1.13×** 이고, 그마저 평형화 1스텝과
미보고 추론시간을 빼기 전이다.  ⇒ 우리 쪽 대응 규약: **RNM-vs-FEM 32–98×**(Bazzoun),
**STEP4 AMG 래치 15–34 % 절감**, **TabPFN 3,000–5,140×** 같은 배수를 인용할 때
**분모(무엇 대비)·포함범위(전체 사슬인가 한 단계인가)·잔여 물리비용**을 **항상 같이 적는다.**

**③ ★ 신뢰구간 중첩은 짝지은 실험의 검정이 아니다.**
8개 **같은 시드 쌍**을 놓고 독립평균 CI 중첩으로 "차이 없음"을 선언했는데,
차이 부호는 **5/5 모두 +**(평균 +0.67 %p)다.  ⇒ 우리 prereg 규약(대응표본 SE, 쌍대응 %p,
8/8 수렴 보고 — CL-33/34/41 방식)이 **이미 옳은 방향**이라는 외부 반례.
우리가 이 형태를 인용할 때 *"문헌은 짝을 안 지었다"* 를 같이 적을 것.

**④ 상류 사슬(슬러리·건조)은 여전히 우리에게 없다.**
`comparison_vs_ours_DEM.md` **§F**(못 하는 것)에 이미 있는 항목이고, 이 논문은 그 구멍을
*메우지 않는다* — 오히려 그 구멍 위에 **또 한 층(surrogate)** 을 얹었다.
우리가 그 축으로 갈 이유가 생긴다면 진입점은 **[Alabdali23]** 이지 이 논문이 아니다.

---

## 9. 인용 가능 문장 (deck/paper 용)

- "A supervised deep-learning surrogate has been coupled to the ARTISTIC CGMD/DEM electrode-manufacturing
  chain to forecast the equilibrium slurry microstructure from the first half of the trajectory
  (Vijay et al., *Energy Storage Mater.* **75** (2025) 103883), reaching a normalised position
  MeanAE of 0.017–0.020 across NMC-111, LiFePO₄ and an NMC-622/argyrodite solid-state slurry."
- "⚠ Critically, that surrogate **loses to a trivial affine-rescaling baseline on the AM–AM radial
  distribution function** in both transferred chemistries (Fréchet distance 0.233 vs 0.194 for LFP and
  **0.564 vs 0.314 for the solid-state composite**), while winning on the numerically dominant
  carbon-binder statistics — a direct demonstration that a position-error loss preferentially fits the
  most numerous phase and degrades precisely the large-particle correlations that set packing and percolation."
- "⚠ Inspection of their Fig. 6 shows the stronger statement: **the predicted and the trivially rescaled
  RDFs superpose in all nine panels and both are out of phase with the target beyond the first
  coordination shell**, the network closing at most ~9 % of the residual Fréchet distance — i.e. the
  surrogate reproduces an affine contraction rather than the structural relaxation it was trained to
  forecast." *(our reading of their figure; the paper reports only the Fréchet table)*
- "⚠ The reported acceleration is never quantified; the surrogate replaces the second half of the slurry
  step only, so the derivable bound is ≈2× on that step and ≈1.1× on the full slurry→drying→calendering
  chain (9 h + 24–36 h + 6 h)." *(derived by us from their Table 2 / §1 — not a claim of the paper)*

---

## 10. 주의 / 한계 — over-claim 방지 + **내가 잡은 내부 불일치 전수**

### A. 범주적 한계 (논문 설계상)
- **압력 축 없음** · **전달 없음** · **소성 없음** · **실험 없음** · **코드·데이터 없음**.
- **ASSB 는 슬러리에서 끝난다** — 압연·porosity 는 **NMC-111 전용**.  ASSB 로 내려간 물성은 **밀도 1.415 g/cm³ (슬러리)** 하나뿐.
- **`physics-informed`** 은 키워드·제목 수사이고 **손실·구조에 물리 제약이 없다**(저자도 미래과제로 적음).

### B. 재현성 공백 (⛔ 이 값들이 없어 재구현 불가)
- **입자 수** 미보고 (전 chemistry) → 학습행 수(= 실제 데이터셋 크기)를 **알 수 없다**.
- **AM% · SC%** 의 값·범위 미보고 — 데이터 다양성의 두 축인데 Table 1 은 **FF 계수만** 싣는다.
- **AM PSD 수치** 미보고(ref [39] 로만), **SE 입자 크기** 미보고.
- **DEM 압연**: 접촉법칙·E·ν·μ·COR·플래튼 속도 **전부 미보고**.
- **상자 형상/치수** 미보고(부피만).  **BO 반복수·목적함수** 미보고.  **학습·추론 시간** 미보고.
- **data availability 문장 자체가 없다.**

### C. ★ 산술적으로 성립하지 않는 지표 — **MSE 열은 쓸 수 없다**
오차가 정규화 구간 [0,1] 안에 있으면 `e² ≤ |e|` 이므로 **MSE ≤ MeanAE 여야 한다**.
그런데 보고값은 **MSE/MeanAE = 18.1×(NMC) · 11.0×(LFP) · 22.1×(ASSB)** 다.
SI Table S3 제목은 세 지표를 모두 *"Normalized"* 라고 적는다 ⇒ **세 열이 같은 척도일 수 없다**
(3좌표 합산이거나 비정규화일 가능성이 크나 **논문은 밝히지 않는다**).
⇒ **결과적으로 "큰 오차를 드러내려고" 넣은 바로 그 지표가 무의미해졌고, 꼬리(heavy tail)는
정량되지 않은 채 남는다.**  (본문은 PBC 통과 입자를 이상점으로 언급만 한다.)

### D. ★ 물리 단위로 환산한 위치오차 = **최근접 접촉거리의 ~70 %** `derived(ours)` + `figure-read`
- **스팬 확정**(Fig 4, 비정규화 축): NMC-111 **±50 ⇒ 100 µm** · LFP **±60 ⇒ 120** · ASSB **±35 ⇒ 70**.
- **환산**: NMC-111 train/val 0.010 × 100 = **1.0 µm** · **test 0.017 × 100 ≈ 1.7 µm** ·
  LFP 0.018 × 120 ≈ **2.2 µm** · ASSB 0.020 × 70 ≈ **1.4 µm**.
- ✔ **독립 교차확인**: SI Table S2 의 **명시적 비정규화** CV MeanAE = **0.991–0.998 µm** 이
  위 train/val 환산 **1.0 µm** 와 **1 % 안에서 일치**한다.  ⇒ 스팬 추정이 맞다.
- **비교 대상**: RDF **1st peak(최근접 접촉거리) ≈ 2.5 µm** (Fig 6a) · **건조 CBD 직경 1.3 µm**.
  ⇒ **test 위치오차 1.7 µm = 접촉거리의 ≈68 %, 건조 bead 지름의 ≈1.3배.**
- ⇒ **이 크기가 §5-5 의 "겹침 → 입자 손실" 과 §5-4 의 "1st shell 너머 구조 붕괴" 를 동시에 설명한다.**
- ⚠ 전제: min–max 정규화의 분모가 **각 chemistry 자신의 좌표 스팬**이라고 가정했다.  단일 전역
  스케일러(NMC 로 적합)를 LFP·ASSB 에 그대로 썼다면 LFP/ASSB 환산은 각각 ×0.83 / ×1.43 만큼 바뀐다.
  **논문은 스케일러 적합 범위를 밝히지 않는다.**
- ⚠ 구 판(`0.93 µm`, "55 µm 정육면체 가정")은 **폐기** — Fig 4 를 직접 보고 스팬이 100 µm 임을
  확인하기 전의 추정이었다.  (부피만으로 세제곱근을 취한 것이 오류였고, 상자는 **슬래브**다.)

### E. 통계 검정 선택 (§3-4)
8개 **짝지은** 런인데 **대응표본 검정 없이** 독립평균 95 % CI 중첩으로 "유의차 없음" 판정.
Δ 부호는 **5/5 양수**(평균 +0.67 %p).  ⇒ *"차이가 없다"* 가 아니라 *"쓴 검정이 못 잡는다"* 가 정확한 서술.

### F. Table 1 내부 불일치 3건
1. **NMC-111 `CBD(σ)`**: mean **0.989** 인데 bounds **[0.924, 0.930]** — 평균이 상한 **밖**.
2. **ASSB `CBD(ε)`**: mean **1.19** 인데 bounds **[0.658, 0.882]** — 평균이 상한 **밖**.
3. **ASSB `Density CBD (liquid) = 0.05`** — **단위 공란**이고 NMC-111 0.9 / LFP 0.95 g/cm³ 대비 **19배 낮다**.

### G. Table 2 산술 불일치
`Total steps 2×10⁷` · `frame interval 10⁵ steps` 이면 프레임은 **200개**여야 하는데 같은 표가
`Total number of frames = 20` 이라고 적는다.  본문(*"1 ms 간격 → 20 프레임"*)과 SI(*"20 프레임의 50 %"*)는
**간격 = 10⁶ step = 1000 µs** 를 함의한다 ⇒ **Table 2 의 두 `frame storage interval` 행이 10× 틀렸다.**
(입력비율 50 % 는 영향 없음 — 절대 시간축만 모호해진다.)

### H. 표기 오류
§2.3 *"The dimension of the CNN is 3@10 for each of **M1 and M2**"* — 뒤 문장이 M3 를 설명하므로
**M2 → M3 오타**.  M2 는 MLP 다.

### I. ⚠ 형제 논문과의 파라미터 불일치 (`derived(ours)`, 두 논문 모두 언급 안 함)
본문은 *"ASSB 슬러리 10런을 [36](= Alabdali 2023)** 대로 돌렸다"* 고 쓰는데, 정본 카드
`alabdali2023_cgmd_wet_manufacturing_ssb_cathode` §FF 표의 **슬러리** 값과 Table 1 의 ASSB 값이 어긋난다:

| 파라미터 | [Alabdali23] 슬러리 | 본 논문 ASSB | 비 |
|---|---|---|---|
| `k_n` | **0.1 kPa** | **5.65 kPa** | **×56.5** |
| `X_µ` | 0.016 | 0.012 | ×0.75 (근사 일치) |
| Ø CBD 습윤 → 건조 | **7.5 → 3.0 µm** | **6.2 → 1.3 µm** | 다름 |

두 편이 같은 모델의 서로 다른 세대일 수도 있으나, **어느 쪽도 변경을 밝히지 않아 전이 주장을 검증할 수 없다.**
⇒ 이 불일치는 **우리 litdb 내부 교차대조로만 보이는 것**이고, 두 논문 어느 쪽의 주장도 아니다.

### J. 전이성 게이트 (우리 규약)
- **chemistry 게이트**: NMC-111·LFP = **액체 전해질 LIB** ⇒ `FORM/METHOD-ONLY`.
  ASSB(NMC-622/argyrodite) = 우리 족이지만 **슬러리 단계 한정** ⇒ 압밀·전달로 전이 **불가**.
- **2D/3D**: 해당 없음(3D).  다만 RVE 는 `figure-read` 로 **≈100×100×16 µm 슬래브**(NMC-111)로 추정될 뿐
  **논문이 치수를 안 준다**.  ⚠ 그리고 RDF 를 **r > L/2 까지** 그린다(Fig 6b 는 120 µm) — 그 구간은
  최소이미지 규약상 의미가 없고, **입자수 미보고**라 유한크기 논의 자체가 불가능하다.
- **digitized vs stated**: 이 카드의 모든 수치는 **표·본문 stated** 다.  `derived(ours)` 표시가 있는 것만 우리 계산.

---

## 11. 기술 미니-용어집 (이 논문을 읽는 데 필요한 것만)

| 용어 | 뜻 | 우리 대응물 |
|---|---|---|
| **CGMD** (coarse-grained MD) | 원자를 묶어 µm 급 "bead" 하나로 취급하는 MD.  bead = AM 입자 / SE 입자 / CBSA 덩어리 | 우리 DEM 입자와 **기하적으로는 같고**, 적분기(NPT MD)와 힘(LJ 우물)이 다르다 |
| **CBSA / CBD** | Carbon-Binder-**Solvent** Aggregate(슬러리) → 용매가 빠지면 Carbon-Binder Domain | 우리 VGCF + PTFE (+ SDCP) 첨가제 상 |
| **Granular Hertz (GH)** | LAMMPS 과립 접촉력: 법선 Hertz + 접선 이력 스프링 + 점성감쇠 + Coulomb 상한 `X_µ` | 우리 `hooke/hysteresis` 의 탄성 사촌 (단 **소성 캡 없음**) |
| **`units micro`** | LAMMPS 단위계: 질량 pg · 길이 µm · 시간 µs ⇒ **압력 1 pg µm⁻¹ µs⁻² = 1 kPa**, 에너지 1 pg µm² µs⁻² = 1 fJ | — |
| **image flag** `ix,iy,iz` | 입자가 주기경계를 몇 번 넘었는지 세는 정수 — 좌표를 "펼치는" 데 필요 | 우리 periodic RVE 처리 |
| **NEMD** | 비평형 MD.  전단을 걸어 점도를 잰다 | 우리엔 없음 (유변학 축 부재) |
| **RDF** `g(r)` | 한 입자에서 거리 r 에 다른 입자가 있을 확률 밀도 — **패킹 구조의 지문** | 우리 배위수 Z·접촉망 통계의 연속판 |
| **Fréchet 거리 (FD)** | 두 곡선의 "개줄(dog-leash) 거리" — 점의 **순서까지** 고려하는 유사도.  **작을수록 유사**, 무차원 | 우리엔 아직 없음 → **§8-① 로 도입 제안** |
| **MeanAE / MedianAE / MSE** | 평균절대오차 / 중앙값절대오차 / 평균제곱오차.  MedianAE 는 이상점에 강건, MSE 는 큰 오차를 드러냄 | 우리 LOOCV·nested CV 계열과 **다른 축**(여긴 CV 가 아니라 점오차) |
| **Bayesian Optimization (BO)** | 목적함수의 확률모델(여기선 GP)을 세워 적은 시행으로 하이퍼파라미터 최적점을 찾기 | 우리 `ml_design_loop.py` 의 BO 와 같은 도구(skopt) |
| **LHS** | Latin Hypercube Sampling — 다차원 공간을 고르게 덮는 초기 표본 설계 | 우리 IBB LHS 큐 |
| **calendering degree** | 압연 두께 감소율 (%).  **압력이 아니다** | 우리 `--protocol hold`(응력-정지)와 **다른 종류의 제어** |

---

## 12. 미해결 / 다음에 할 것

1. ✅ **ref [28] Galvez-Aranda 2024 (*Adv. Energy Mater.* 14, 2400376) — DIGEST 완료 2026-09-11**
   → 정본 카드 **`galvezaranda2024_time_dependent_dl_calendering_microstructure`**.
   **압연 단계의 DL 자매편**이 맞았고, 우리 축(접촉면적·porosity·τ·springback)과 직접 겹친다.
   ★★ **그러나 이 카드의 위 인용문은 전수 검증 결과 "방향은 맞고 정밀도는 틀렸다"** (그쪽 §3-A):
   DL 이 예측하는 것은 **한 가지 — 다음 프레임의 복셀 격자**이고 네 양은 전부 그 후처리다.
   **porosity ✅** (n=11 평균 3.45 %) · **접촉면적 ⚠** (평균 8.99/10.54/13.76 %, 최대 **16.76 %** =
   네 양 중 **최악**이고 우리 Tabor/Stage-E A(δ)와 **같은 양이 아니다**) ·
   **확산도 ⚠⚠ DL 이 예측하는 게 아니라** 예측격자 위에서 **GeoDict DiffuDict FV 솔브를 새로 돌려**
   얻는다 (비용 미보고 · DEM 경로와 동일 ⇒ *"훨씬 낮은 비용"* 이 **이 양에는 불성립**) ·
   **springback ⛔ 숫자 0건** (우리가 그림에서 뽑았다: CD 25/35/45 % → **4.8/7.6/10.1 %p**).
   ⇒ **이 카드(§12-1)의 서술을 그대로 인용하지 말고 그쪽 §3-A 표를 인용할 것.**
   ★ 대조되는 긍정 평가 하나: **가속 배수를 그쪽은 썼고(188×/step) 손익분기도 정직하다**
   (`derived(ours)` 583 step = 3.4 전극-스윕 = 학습셋 자신 크기) — **이 논문의 1.1× 보다 훨씬 낫다.**
   ⚠ 다만 그쪽은 **추론 프로토콜을 공개하지 않아 teacher-forcing 의혹**이 남는다 (그쪽 §10-⑤).

1-b. ✅ ★★ **ref [26?] 사슬의 세 번째 편 — 건조(drying) — DIGEST 완료 2026-09-11**
   → 정본 카드 **`galvezaranda2025_paml_vgg16_dem_slurry_drying`** ·
   Galvez-Aranda, Fernandez, Franco, ***ACS Appl. Mater. Interfaces* 17 (2025) 32150−32162**,
   DOI `10.1021/acsami.4c23103` · 비교노트 **F-DL5**.
   ★★ **이로써 Franco/ARTISTIC 의 DL 사슬 3편이 계보로 닫혔다**:
   **슬러리 = 이 카드 [Vijay25]** → **건조 = [Galvez25]** → **압연 = [Galvez24]**.
   (이 논문은 그쪽 **ref [42]**, 압연편은 그쪽 **ref [23]** 으로 인용된다.)
   ★ **그 카드가 이 카드의 두 지적을 각각 확장/재확인한다**:
   - **가속 분모 규율(§10-③ · F-DL2)의 세 번째 사례이자 가장 정량적인 판**: 그쪽은 배수를 쓰긴 하지만
     (**684 → 48 min = 14.25×**) **4-lag 시드 프레임의 pure DEM 비용 102.6 min(전체의 15 %)을 분모에서
     뺐다** ⇒ 🧮 **정직 end-to-end 4.77×**, **Amdahl 천장 6.67×**.  🧮 **손익분기 13.9 런**.
     ⚠ 게다가 **초록(615→36 = 17.1×)이 본문(14.25×)과 안 맞는다.**
   - ⚠⚠ **이 카드 §10-D 의 "정규화 오차 함정" 이 세 논문 연속 재발한다**: 여기서 `MeanAE 0.017 → 실제
     1.7 µm = 접촉거리의 68 %` 를 잡았듯, 그쪽은 **MAE ≈ 0.105 의 단위를 아예 안 적는다** —
     원시 µm 읽기(0.105 µm)는 자기 RDF 와 모순이고, min-max 읽기(**3.2–5.2 µm = 최근접거리 1.45 µm 의
     2.2–3.6배**)만 자기일관하다.  ⇒ **같은 그룹 3편 모두 "정규화 손실값"을 단위 없이 보고**한다.
   - ★ **건조 규약 대조점**: 이 카드는 건조를 **CBSA bead 수축**(NMC-111 **Ø7 → 1.3 µm**)으로 흉내낸다고
     명시하는데, **[Galvez25] 는 건조 물리를 한 줄도 적지 않는다**(용매·수축·응집 램프 전부 미기재).
     게다가 그쪽 DL 은 **출력이 (x,y,z) 3개뿐이라 `r` 을 얼린다** ⇒ **bead 수축을 원리적으로 표현 못 하고,
     DEM 투영자도 그것을 못 고친다**(위치만 완화).  ⇒ ⬜ **미해결 질문**: 그 사슬의 건조가 여기와 같은
     수축 규약이라면 surrogate 가 그 축을 어떻게 옮기는가?  **답은 ref [33] Xu 2023 (JPS 554, 232294)** 에만 있다.
     ✅✅ **2026-09-11 해결 — 정본 카드 `papers/xu2023_realistic_am_shape_cgmd_calendering.md`.**
     **답: 같은 수축 규약이다** — Xu 2023 도 건조를 **CBD bead Ø6.2 → 1.3 µm 순간 수축**으로 흉내내고
     (`ngandjong2021` 과 **완전히 같은 값**), 동시에 **force field 를 전면 교체**한다(LJ 우물 CBD **×10⁶**,
     AM–AM 인력 0 → 켜짐).  ⇒ **[Galvez25] 의 출력이 (x,y,z) 뿐인 surrogate 는 그 축을 원리적으로 얼린다**는
     이 카드의 판정이 **확정**됐다 — 사슬의 건조 물리 자체가 **`r` 의 변화**이기 때문이다.
     ★ 부가로 그 카드가 준 것: **압력축은 거기에도 없고**(`MPa` 전수 0 회, CD 0–42.2 % 뿐) ·
     **상속된 "τ 실험 검증"은 독립이 아니며**(dilation–erosion 인자를 τ 표적에 맞춰 선택) ·
     **AM 형상 축**(Krumbein 구형도 모드 −0.04 ~ −0.06)이 새로 열린다.

2. ⬜ **Fréchet-RDF 게이트 구현** (§8-①) — `scripts/` 에 상별 RDF + FD 계산기.  의존성 없이 numpy 로 가능.
3. ⬜ 우리 시간-surrogate 는 **플래튼 정지 프레임 트랙(SR track 2)** 이 닫힌 뒤에만 착수 (§7-3-1).

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

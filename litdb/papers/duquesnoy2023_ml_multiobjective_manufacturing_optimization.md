# 물리기반 시뮬 합성데이터 + ML(SISSO+베이지안 다목적최적화)로 LIB 전극 제조 역설계 — Duquesnoy (Energy Storage Mater. 2023)

> slug `duquesnoy2023_ml_multiobjective_manufacturing_optimization` · DOI `10.1016/j.ensm.2022.12.040` · type `mixed (CGMD+DEM physics-sim + SISSO ML + Bayesian multi-objective optimization + exp 검증)` · PDF `Duquesnoy_2023_EnergyStorageMater_ML_MultiObjective_ManufacturingOptimization_main.pdf` (+ `_SI.pdf`) · digested `2026-07-10` · status ✅

## 1. 한 줄 요약
**우리 프로젝트 전체 비전(설계수치 입력 → ML이 full-metric 예측 → 미세구조 그림 → 최적화/역설계)의 *published archetype*.**
Franco 그룹(ARTISTIC, Amiens)이 **물리기반 제조 시뮬(CGMD 슬러리 → 건조 → DEM 캘린더링)** 으로 합성 데이터셋을 만들고,
**Sobol(+Saltelli) DOE**로 제조 파라미터 공간(AM%·SC%·CD%)을 space-filling 샘플링한 뒤, **SISSO**(symbolic regression)로 각
전극 물성 = f(제조 파라미터) *해석식*을 자동 발견하고, 그 대리모델 위에서 **베이지안 다목적최적화(GP + GP-Hedge acquisition +
스칼라화 C_f)** 로 **min tortuosity · max σ_e · max active-surface · max density** 를 동시 만족하는 최적 제조조건을 역설계 →
**실제 전극을 만들어 실험 검증**. ⇒ 우리 5-Phase 로드맵을 *한 논문에 통째로* 구현했다.  단, **LIB *습식* NMC111 양극**
(이온위상 우리 ASSB와 반대: pore=전해질=이온전도체)이고, **전달을 tortuosity/GeoDict 연속체 proxy로**만 다루며(**명시적
접촉망 σ 삼중항·MPM 소성 morphology 없음**) — 우리가 채우는 *구조→σ 기계론* 절반이 그들에게 없다.  **frame[5] 분업의 거울:
그들 = 최적화 loop 소유 / 우리 = 구조-transport 기계론 소유.**  우리는 그들의 loop 기계장치(Sobol DOE·SISSO 교차검증·GP-Hedge BO·
스칼라화)를 *우리의 더 풍부한 구조 predictor 위에* 흡수해야 한다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| M. Duquesnoy, C. Liu, D. Zapata Dominguez, V. Kumar, E. Ayerbe, A. A. Franco (LRCS/UPJV Amiens · ALISTORE-ERI · CIDETEC · Umicore · IUF · RS2E) | Energy Storage Materials **56** (2023) 50–61 | 10.1016/j.ensm.2022.12.040 | **NMC111** LiNi₁/₃Mn₁/₃Co₁/₃O₂ (Umicore) + **CBD**(carbon-binder domain: C45 CB + PVDF) + 액체 전해질 — **LIB 습식 양극** (ASSB 아님) | 물리시뮬(CGMD+DEM) 합성데이터 → SISSO ML → 베이지안 다목적최적화 → **실험 fabrication 검증** |

- **프로젝트 계보:** ERC ARTISTIC (Franco). 물리기반 3D-resolved 제조 모델 사슬(슬러리→건조→캘린더링→전해질침투 LBM→4D echem)이
  이미 존재하고 실험 파일럿 라인에 보정·검증됨. 온라인 계산기(브라우저)로 배포, 2022-11 기준 515명 사용.  본 논문 = 그 사슬을
  **ML 대리모델 + 최적화 loop 로 감싸** high-throughput 역설계를 실현.
- **우리와의 관계:** 우리(Hanyang, DEM+MPM+STEP3)와 **같은 대분류**(제조 시뮬 → 미세구조 → 물성 → ML 예측 → 최적화)지만
  **재료(LIB≠ASSB)·전달물리(pore-Bruggeman≠SE-Holm)·구조 다룸(black-box surrogate≠기계론적 구조→σ)** 이 다르다.  가장 가까운
  peer 는 우리 corpus 의 Ngandjong 2021·Lyu 2025·Sangrós 2019(같은 LIB 캘린더링 DEM 계보) + Bielefeld/Bazzoun(구조-σ).

## 3. 핵심 물성 (수치)

### 3.0 입력 3 · 출력 4(+porosity)
| 축 | 이름 | 범위 (Fig 2 축 = digitized) | 우리 대응 |
|---|---|---|---|
| **입력 1** | **AM%** (active material 무게분율) | ~**86–96 %** | 우리 AM wt% / f_CAM |
| **입력 2** | **SC%** (슬러리 solid content) | ~**40–71 %** | 우리엔 없음 (습식 슬러리 전용; 건조 후 CBD 부피 결정) |
| **입력 3** | **CD%** (calendering compression degree = 두께감소율) | **0–40 %** | 우리 **λ_dz 두께감소 / 압력** (변위제어 = MPM `hold`) |
| **출력 1 (min)** | **tortuosity factor** (pore network) | 최적 1.47 | 우리 τ_Laplace — 단 **그들의 이온 proxy**(LIB pore) |
| **출력 2 (max)** | **effective σ_e** [S/m] | 최적 0.175 | 우리 σ_electronic (단 그들 GeoDict 연속체) |
| **출력 3 (max)** | **active surface AM/electrolyte** [%] | 최적 54–56 | 우리 coverage (단 그들 AM-pore, 우리 AM-SE) |
| **출력 4 (max)** | **density** [g/cm³] | 최적 2.45 | 우리 density / (1−porosity) |
| (파생) | **porosity** [%] | 최적 ~24–29 | 우리 porosity |

### 3.1 최적 제조조건 (Table 2, BO 예측)
| AM% | SC% | CD% |
|---|---|---|
| **90.4** | **58.1** | **28.4** |
→ 제조 파라미터 범위의 *극값이 아닌* 균형점(다목적 최적).  실험 fabrication 시 **90 / 58 / 30** 으로 반올림.

### 3.2 최적 전극 물성: 대리모델 예측 vs 물리모델 재생성 (Table 3)
| 물성 | SISSO 예측 | 물리모델(재생성) | 일치도 |
|---|---|---|---|
| Tortuosity | **1.4700** | 1.5286 | −3.8 % |
| σ_e [S/m] | **0.1724** | 0.1750 | −1.5 % |
| Active surface [%] | **54.0522** | 55.7230 | −3.0 % |
| Density [g/cm³] | **2.4459** | 2.4456 | +0.01 % |
→ 대리모델이 물리모델을 잘 재생성 = **loop 가 물리적으로 self-consistent** (frame[4]-형 내부 교차검증).

### 3.3 SISSO 검증 지표 (Table 1 = testing 20 %, Table S1 = training 80 %)
| 물성 | Test RMSE% | Test R²_score | Test CI95 (75-seed) | Train RMSE% | Train R² |
|---|---|---|---|---|---|
| **Tortuosity** | 1.48 | ⚠0.933* | **[0.941; 0.950]** | 6.88 | 0.978 |
| **σ_e [S/m]** | 7.80 | ⚠0.933* | **[0.978; 0.981]** | 1.91 | 0.966 |
| **Active surface [%]** | 1.41 | 0.911 | [0.885; 0.914] | 1.41 | 0.909 |
| **Density [g/cm³]** | 1.87 | 0.968 | [0.962; 0.971] | 1.87 | 0.985 |
- **⚠ * = 논문 표 오류로 판단:** Table 1 이 tortuosity·σ_e 의 R²_score 를 **둘 다 0.933** 으로 인쇄(인접 행 동일값 = copy 오류
  개연) — 그리고 그 0.933 은 자신들의 CI95([0.941,0.950]/[0.978,0.981])를 **벗어남**(내부 모순).  ⇒ 신뢰할 값은 **CI95**:
  tortuosity ≈ 0.945, σ_e ≈ 0.98.  active-surface(0.911)·density(0.968)는 각자 CI95 안 → 그 둘은 인쇄값 신뢰.
- **⚠ RMSE% tortuosity↔σ_e 가 train/test 간 뒤바뀐 듯:** train(σ_e 1.91 < tort 6.88) vs test(tort 1.48 < σ_e 7.80).
  active/density RMSE 는 두 표 동일(1.41/1.87). → 표 사이 행 스왑 가능성 flag(원문 그대로 기록, 해석은 보수적으로).
- **결론(정직):** 네 물성 모두 **R² 0.91–0.985, RMSE% 1.4–7.8 %** 로 잘 맞음 = SISSO 대리모델은 제조사슬을 초 단위로 대체 가능.
  CI95 는 75회 재분할로 산정 → seed-robust.

### 3.4 극단 케이스 4종 (Table S2 + Fig 6) — "한 물성만 극대화" 반면교사
| 극단 케이스 | AM% | SC% | CD% | porosity | 특징 (Fig 6) |
|---|---|---|---|---|---|
| **High conductivity** | 86.3 | 57.0 | 33.1 | **26.55 %** | CBD↑·AM↓ → 전자망↑ but AM-pore active surface↓ → 반응과전압↑ (CBD가 AM 덮음, CBD 유효 σ·D = bulk 의 **5 %**) |
| **Low tortuosity** | 88.8 | 56.8 | **2.24** | **42.35 %** | 거의 uncalendered → τ 낮음 but CBD 연결 나빠 σ_e 급락 → 용량 심각 저하 |
| **High active surface** | 96.5 | 60.3 | 9.11 | **35.97 %** | AM↑·CBD↓ → active surface↑ but σ_e **2× 이상 낮음** (porosity 40 % 유지 대가) |
| **High density** | 94.5 | 71.0 | **36.36** | **24.11 %** | 큰 압축 → 밀도 최고 but τ 급증·active surface 급감·**AM 입자 파쇄 위험**(CEI/TM 용해·비활성화; 현 모델 미반영) |
- **최적 케이스(90.4/58.1/28.4)** = 위 극단들의 *균형* — "moderate calendering" (프로토타이핑 라인 실용 영역).

### 3.5 실험 검증 전극 (Table 4) — ML 최적조건(90/58/30) fabrication
| 물성 | Pristine (uncalendered) | Calendered 30 % |
|---|---|---|
| Mass loading [mg/cm²] | 6.7 ± 0.3 | 6.7 ± 0.3 |
| Thickness [µm] | 68 ± 4 | **48 ± 4** |
| Density [g/cm³] | 1.6 ± 0.4 | **2.6 ± 0.3** |
| Tortuosity factor | 3.5 ± 0.5 | **1.8 ± 0.4** |
| Porosity [%] | 60 ± 3 | **29 ± 0.7** |
- **모델 예측 최적(density 2.45 / τ 1.47 / porosity ~24 %)** ↔ **실측(2.6 / 1.8 / 29 %)** = *reasonable* 일치(σ_e 는 실험 미측정).
  discrepancy 원인(그들 명시): (i) 물리모델은 **spherical 입자 + clustered CBD**(단순화) ≠ 실제 CB+binder 개별 조성; (ii) 슬러리
  formulation 차.  그럼에도 슬러리 점도·밀도·건조/캘린더 porosity 가 실험과 satisfactory match(ref 13,20,24).

### 3.6 SI Table S3 — Liu et al. 2023(ESM 54:156-163, 물리모델 보정용)과의 실험 물성 비교
| AM% | SC% | CD% | mass loading | thickness µm | density | tortuosity | porosity % | σ_e [S/m] |
|---|---|---|---|---|---|---|---|---|
| 85 | 46 | 0 | 15.79 | 121.6 | 1.55 | 1.94 | 59.53 | 0.029 |
| 85 | 46 | 10 | 15.44 | 108.83 | 1.73 | 2.365 | 55.82 | 0.0928 |
| 85 | 46 | 20 | 15.52 | 98.5 | 2.03 | 2.66 | 50.91 | 0.478 |
| 90 | 55 | 0 | 15.58 | 91.67 | 1.89 | 1.78 | 53.03 | 0.00242 |
| 90 | 55 | 10 | 14.94 | 82.32 | 2.02 | 1.78 | 49.835 | 0.0432 |
| 90 | 55 | 20 | 15.09 | 72.1 | 2.33 | 2.77 | 42.145 | 0.14 |
| 95 | 67 | 0 | 15.46 | 77.8 | 1.09 | 1.57 | 51.544 | 0.000743 |
| 95 | 67 | 10 | 15.37 | 68.2 | 2.37 | 1.75 | 45.0 | 0.00145 |
| 95 | 67 | 20 | 15.11 | 61.7 | 2.58 | 2.47 | 40.26 | 0.00164 |
| **90** | **58** | **30** | **6.7** | **48** | **2.6** | **1.8** | **29** | N/A (최적/실험) |
- 마지막 행 = 본 논문 최적 전극(90/58/30) = Table 4 calendered.  나머지는 Liu 2023 의 3×3(AM 85/90/95 × CD 0/10/20).
- **Liu 2023 결론:** **90 % 조성이 85·95 % 보다 우수** — CBD 연속성 유지 + thinner + 집전체-전극 계면저항 낮음. ⇒ **최적 AM 90.4 %
  와 정합**(SISSO 가 Liu 의 실험 최적을 *독립 재발견*).  ★ CD% 오를수록 σ_e **급상승**(85 %: 0.029→0.478, 16×!) = 캘린더링이
  전자 접촉망을 극적으로 개선(우리 압밀→σ↑ 와 같은 방향, 단 LIB pore-이온위상은 반대).

## 4. 시뮬레이션 방법 ★

### 4.1 물리기반 제조 사슬 (합성데이터 생성기)
- **code:** **LAMMPS** (CGMD 슬러리 + DEM 캘린더링 모두). 메싱 = MATLAB. 물성추출 = Python(자체) + **GeoDict**(σ_e) + **TauFactor**(τ).
- **① 슬러리 (CGMD, Coarse-Grained Molecular Dynamics):** NMC111 = **구형** coarse-grained 입자(NMC111엔 충분, 그들 선행연구).
  **AM–CBD 물리화학 상호작용 Force-Field(FF)** 로 슬러리 평형화 (top-down 접근).  총질량 **0.1 µg**(작은 전극부피, 바닥면적
  400–900 µm²) — 계산비 절감 + mass loading 이 실험(~15–40 mg/cm²)에 맞도록.  CBD = **clustered entity**(카본블랙+바인더를 한 상으로
  단순화).
- **② 건조 (drying):** **CBD 입자를 균일하게 shrink** 해 용매 제거 모사 → 평형 dried 미세구조.  ⚠ 이것은 **부피 연산이지 소성 아님**.
- **③ 캘린더링 (DEM):** dried 미세구조를 **DEM 으로 기계적 압축** (LAMMPS).  압축된 calendered 미세구조 산출.
- **계산자원:** MatriCS 클러스터(UPJV), 8 노드(각 384 GB RAM), 2× Intel Xeon Gold 6148 @2.40 GHz, 20 core.
  슬러리 1건 ~**150 h**, calendered 전극 1건 ~**8 h**.  전체 합성데이터셋 = **174 제조조건**, 생성에 **2개월**.

### 4.2 DOE — Sobol 저-discrepancy 수열 (+ Saltelli 확장) ★
- **방법:** quasi-random **Sobol** sequences + **Saltelli** extension → (AM%, SC%, CD%) hyper-rectangle 를 **space-filling** 샘플링.
- **왜 Sobol:** low-discrepancy = 데이터 점이 적을 때도 공간을 *균일*하게 채움 (Gaussian/uniform 대비).  **Fig S1** = Sobol vs
  Gaussian vs uniform 을 N=10/20/50/100/200 에서 2D 비교 → 파란 Sobol 이 가장 고르게 채움을 시각 입증. Cervellera et al. 인용
  (수열 생성 전략이 ML/최적화 결과를 크게 좌우).
- **DOE 단축(중요):** 슬러리(~150 h) ≫ 캘린더링(~8 h) → **AM%·SC%(슬러리 입력)는 제한된 개수만** 생성하고, quasi-random 으로 뽑은
  **CD% 값들을 그 슬러리들에 random 하게 associate**.  ⇒ "다양한 슬러리 몇 개 × 각 슬러리에 여러 캘린더 조건" 형태의 shortened
  quasi-random DOE.  대표성은 유지(Fig 2)하면서 계산시간 절감.
- **Fig 2:** 3D(AM/SC/CD) scatter + 2D(CD vs SC) — Sobol 의 quasi-randomness(빈틈 없이 채우되 격자 아님) 시각화.

### 4.3 SISSO — deterministic learning (symbolic regression) ★★
- **SISSO = Sure Independence Screening + Sparsifying Operator** (Ouyang/Ghiringhelli 계열; ref 61–63). 회귀법 — 입력 파라미터와
  하나의 출력 물성 사이 *해석식*을 얻되, 고차원에서 입력들의 **비선형 조합(descriptor)** 에 초점.
- **최종 형태 (Eq 1 / SI Eq S1):**  **y = Σ_{i=0}^{n} c_i · d_i,  c_i ≠ 0**  ((d_i)=descriptor, (c_i)=계수).
  = 출력물성이 **descriptor 들의 선형결합**, descriptor 자체는 입력의 비선형 조합.
- **두 축:**
  - **(A) Feature space 구성 (descriptor 생성):** 연산자 집합
    **Ĥ^(m) := {I, +, −, ×, |−|, ⁻¹, √, ², ³, exp, log}[φ₁, φ₂],  (φ₁,φ₂) ∈ Φ²**  (SI Eq S2) 를 현재 feature space 원소쌍에
    재귀 적용 → 깊이(rung)마다 더 복잡한 비선형 조합 생성.  마지막 iteration n: **Φ_n = ∪_{i=1}^n H^(m)[φ₁,φ₂], (φ₁,φ₂)∈Φ²_{n−1}**
    (Eq S3).  feature space 가 급격히 커짐 → **wide 행렬 D** 로 `Y = D × C` 문제화.  (m) = **차원해석**(단위 일관 descriptor 유지);
    본 사례는 입력 3개 모두 **무차원** → 단순화.
  - **(B) Solution algorithm (오차 최소화):** D 가 너무 크므로 **descriptor 를 좁힌다** — 각 descriptor 를 metric(예: **상관 크기**)
    으로 scoring → top-ranked 만 유지(=γ) → 잔차 **Δ = Y − D_γ × c_γ** 최소화 → **l₀-norm 또는 l₁-norm 정규화**.
- **본 사례 setting (SI B.1):** 각 전극물성 **개별 fit**.  **descriptor 차원 = 3 고정**.  대수연산 **(+, −, ×, ², ³, ⁻¹, log(), exp(),
  √, ³√)**.  best descriptor set 선정 시 **l₀-norm 정규화** 사용.
- **검증:** 174건을 80/20(train/test) random 분할, **75회 재분할** → R²_score 의 **CI95** 산정(Table 1).  Fig S2 = parity plot 4종.
- **역할:** SISSO 해석식으로 **제조사슬 전체(슬러리→건조→캘린더)를 초 단위 예측식으로 대체** → 이후 최적화 loop 를 물리시뮬 없이 돌림.

### 4.4 베이지안 다목적최적화 (BO) — 역설계 loop ★★
- **문제화 (Eq 2):**  **x* = argmin C_f(x)** — 최적 제조 파라미터 x* 를 찾음.
- **스칼라화 (Eq 3):** 다목적 → 단일목적.  각 물성을 [0,1] 로 스케일(y_{i,s}), 최소화군 Y_m·최대화군 Y_M 로 나눠
  **C_f = (1/4) × [ Σ_{y∈Y_m} (y_{i,s})² + Σ_{y∈Y_M} (1 − y_{i,s})² ]**.  **등가중치 1/4**(proof-of-concept; 무제약).
  최소화=tortuosity(Y_m), 최대화=σ_e·active surface·density(Y_M).  스케일링 = 물성 절대크기 차로 인한 bias 제거.
  ★ C_f 는 **SISSO 해석식으로 조립** → 물리시뮬 없이 빠른 비선형 예측 조합.
- **GP surrogate (SI B.3):** BO 가 C_f 를 **Gaussian Process** 로 근사.  prior **C̄_f ~ GP(μ₀, Σ₀)** (Eq 6) → posterior
  **(C_f|D) ~ GP(μ_*, Σ_*)** (Eq 7), hyperparameter Eq 8(표준 GP conditioning: μ_* = Σ₀(x,X)Σ₀(X,X)⁻¹(μ₀−μ₀(X))+μ₀(x) 등).
  매 스텝 D 갱신.
- **Acquisition = GP-Hedge (SI B.4):** **LCB(lower confidence bound) · EI(neg. expected improvement) · PI(neg. probability of
  improvement) 3종을 조합** ("Gaussian Process Hedge").  각 스텝: (i) 3 acquisition 이 각각 후보 x̄_i 제안 → (ii)
  **softmax(η, g_i)** 확률선택으로 x* 결정 → (iii) (x*, y*) 로 GP 갱신 → (iv) gain **g_i ← g_i − μ₀(x̄_i)** 갱신.
  = exploitation(근처 minima)↔exploration(먼 minima) 균형을 3-acquisition 앙상블로.
- **수렴:** **300 iteration** cut-off. **Fig S3** = min(C_f) 가 **~step 100 에서 plateau**(초반 급감).
- **해석 (Fig 4):** 2D **Partial Dependence Plot(PDP)** — GP 예측에 대한 각 제조 파라미터의 marginal 영향(나머지 평균).
  입력들이 uncorrelated 라 PDP 유효.  **최적해(노란 별)** = SC%·CD% 의 low-partial-dependence 영역 근처.  AM% 는 >92 %에서
  영향이 덜 뚜렷/독립적(고-AM 변동성↑).  BO 후보(검은 점)들이 최적해 영역에 몰림 = BO 의 빠른 수렴.

### 4.5 입자 처리 ★ (DEM판 "무질서 처리")
- **구형만** (spherical NMC111 coarse-grained; NMC111엔 충분하다고 그들 명시).  CBD = clustered entity(형상 없는 한 상).
- **캘린더링 DEM = rigid-ish 강체구 압축** — **진짜 SHAPE 소성 없음**(morphology 변화 없음).  건조의 CBD-shrink 는 부피 연산.
  ⇒ **Varkey/Bazzoun 과 같은 frame[1]/[2] 한계** — 우리 MPM 이 메우는 *형상-소성 절반*이 여기도 빠짐.
- PSD: 슬러리 CGMD 는 구형 분포지만 본문은 **단일 CAM 상**(bi/tri-modal PSD·Furnas dip 논의 없음; 그들 perspective 는 향후 비구형
  입자 언급 ref 79).

### 4.6 물성 추출 (Fig 3: 소프트웨어 사슬)
- **LAMMPS(구조) → MATLAB(meshing) → {Python: active surface·density·thickness·porosity | GeoDict: σ_e | TauFactor: τ}**.
- **active surface** = AM 입자 ↔ pore 접촉면적(pore 는 전해질로 fully filled 가정) = **반응 계면**.  in-house Python.
- **σ_e (GeoDict):** voxel 연속체 전도 solver(Bielefeld 2020 계열, ConductoDict).  CBD 유효 σ = bulk 의 5 %.
- **τ (TauFactor):** voxel pore 망에서 **Laplace 정상확산**(finite volume) → 유효확산율 → τ = porosity/effective-diffusivity.
  (SI: 이상화 매질, 유체물성 무관.)  = 우리 corpus 의 `taufactor_tortuosity_factor_tomography_tool` 도구와 동일 원리.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | 전체 파이프라인 모식: DOE → 제조 물리모델(슬러리·건조·캘린더) → 전극물성 → deterministic learning → 다목적최적화 → 최적화된 물성 → 실험 셀 설계 (닫힌 loop) | ★ **우리 5-Phase 로드맵의 그림 버전** — Phase1(물성 예측)~Phase5(최적화/역설계)를 한 사이클로. 우리 그림틀 벤치마크. |
| **2** | DOE Sobol 수열: 3D(AM/SC/CD) + 2D(CD vs SC) scatter | Sobol space-filling 시각화 = 우리 다음 sim batch DOE 설계 템플릿 |
| **3** | 소프트웨어 사슬 LAMMPS→MATLAB→Python/GeoDict/TauFactor | 물성추출 파이프라인 = 우리 STEP3(Kirchhoff)·τ_Laplace·coverage 와 1:1 대조 |
| **4** | GP 모델 2D PDP 3장 + 최적해(노란 별) + BO 후보(검은 점) | 최적화 해석법(PDP) = 우리 Phase-3 predictor 민감도 해석에 흡수 |
| **5A** | 최적 전극 물성 radar + KDE(각 물성의 합성데이터 분포 내 위치) | radar+KDE = 다목적 균형 시각화; "한 물성 극값 불가"를 KDE 로 |
| **5B** | 최적 조건 3D 미세구조: 슬러리→건조→캘린더 3단계 | 우리 DEM/MPM 미세구조 렌더와 대응(단 그들 구형·CBD 상) |
| **6** | radar: 최적 vs 4 극단(고-σ_e/저-τ/고-active/고-density) | ★ **다목적 최적 = 균형점** 논증; 극단 반면교사(우리 whatif 축과 대응) |
| **S1** | Sobol vs Gaussian vs uniform (N=10~200) | low-discrepancy 우월성 근거 |
| **S2** | 4물성 parity plot (real vs predicted) | SISSO 대리모델 goodness-of-fit |
| **S3** | BO 수렴(min C_f vs step, ~100 plateau) | 300 iter 충분·수렴속도 |
| **S4** | EIS Nyquist(uncalendered R_ion/3=43 Ω vs calendered 30 %=25 Ω) + T=AεR_ion σ/2d | τ 실험추출(Landesfeind) = 우리 τ 실험검증법 |

## 6. Post-processing ★
- **무엇:** (i) **SISSO** symbolic regression(각 물성 y=Σc_i·d_i, 3-descriptor, l₀-norm); (ii) **베이지안 다목적최적화**
  (GP surrogate + GP-Hedge acquisition + 스칼라화 C_f); (iii) **PDP**(2D partial dependence, GP 해석); (iv) **KDE**(합성데이터
  물성분포 내 최적값 위치); (v) 물성추출 — **TauFactor**(τ, Laplace-FVM), **GeoDict**(σ_e voxel 연속체), Python(active surface=
  AM-pore, density, porosity, thickness); (vi) 실험 **EIS-Landesfeind**(τ, R_ion/3 절편 + transmission-line).
- **도구:** LAMMPS(CGMD+DEM), MATLAB(meshing), Python(자체), GeoDict, TauFactor, scikit-optimize류 BO(GP-Hedge = skopt 계열),
  SISSO(Fortran/자체).  실험: Dispermat 믹서, comma-coater PDL250, lap-press BPN250, MTZ-35 impedance(BioLogic).
- **검증지표:** RMSE%(상대잔차 (y−ỹ)/ỹ 의 RMS, Eq 4) + R²_score(Eq 5) + 75-seed CI95.  → Table 1/S1, Fig S2.
- **수치화·기록:** 174건 합성데이터 → SISSO 식 4개 → C_f 조립 → 300-iter BO → Table 2 최적조건 → 물리모델 재생성 검증(Table 3)
  → 실험 fabrication(Table 4) + Liu2023 비교(Table S3).

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`

### 7.0 전체 구도 — frame[5] 의 *거울*
| 층 | 이 논문 (Duquesnoy/ARTISTIC) | 우리 (Hanyang DEM+MPM+STEP3) | 판정 |
|---|---|---|---|
| **최적화 loop** | ★ **소유** (Sobol DOE→SISSO→GP-Hedge BO→역설계→실험검증, 닫힌 loop **완성·published**) | Phase 3–5 **미완**(predictor·2D synth·layering 계획만) | **그들 우위 — 흡수 대상** |
| **구조→σ 기계론** | 없음 (제조→물성 **black-box surrogate**, 구조 우회) | ★ **소유** (DEM+MPM 구조 → Kirchhoff/Holm σ 삼중항 → 스케일링) | **우리 우위** |
| **전달 transport** | tortuosity(pore, 이온 proxy) + GeoDict σ_e(연속체) — **σ_ionic·σ_thermal·접촉망 없음** | σ_ionic/σ_e/σ_thermal 삼중항 + Stage-E 소성 접촉면적 + 명시 Kirchhoff 접촉망 | **우리 우위 (삼중항·constriction)** |
| **역학/morphology** | rigid-ish DEM 캘린더링(**형상소성 없음**), CBD-shrink 건조 | ★ MPM 진짜 소성 형상변화(SEM 일치)·void-fill·Σdg 변형장 | **우리 우위 (frame[5])** |
| **패킹/dip** | 단일 CAM 상(bi/tri-modal·Furnas dip 없음) | ★ bimodal 12:4:1 + 정량 Furnas dip(AM 70–85 wt%) | **우리 우위** |
| **실험 fabrication** | ★ **소유** (ML 최적전극 제작·EIS 검증) | 실험 앵커는 문헌 차용(Minnmann/Bazzoun/Doux) | **그들 우위** |

### 7.1 방법 항목별 대조
| 항목 | 이 논문 | 우리 | 차이 / 이유 |
|---|---|---|---|
| **스케일링 법칙 도출** | **SISSO 자동 symbolic regression** (y=Σc_i·d_i, 3-descriptor, l₀) | **손유도 물리폼 + OLS/Ridge** (σ_grain·Cronau·√φ·CN²·√cov·f_p³·C(τ) 등) | 같은 목표(해석식), 다른 방법. SISSO=auto/우리=physics-prior LOCKED. **교차검증·Phase-3 후보** |
| **입력 차원** | 제조 3개(AM/SC/CD), **무차원** | 제조 knob(AM/P:S/r_SE/P) → **구조 5–14 descriptor** → σ | 그들 = 제조→물성 직결(얕음); 우리 = 제조→구조→σ(깊음). 그들이 더 end-to-end, 우리가 더 기계론 |
| **DOE** | ★ **Sobol+Saltelli space-filling** (174건, 대표성 보장) | ad-hoc design-point + multi-seed; active_learning=exploit corner | **Sobol DOE 흡수 1순위** (구조 gap CN≥7·중간두께 채우기) |
| **다목적최적화** | ★ **GP + GP-Hedge + 스칼라화 C_f(등가중)** | 없음(Phase-3~5 미착수) | **BO 기계장치 흡수** (우리 predictor 위에) |
| **σ_e** | GeoDict 연속체(constriction 없음=상한, Bielefeld2020 계열) | Kirchhoff 접촉망 + Holm constriction + Stage-E 소성면적 | 우리가 constriction 소유(더 물리적, granular) |
| **σ_ionic** | ❌ 없음 — **tortuosity 로 대체(pore 이온 proxy)** | ★ σ_ionic(LOOCV 0.975, Holm/Kirchhoff SE망) | **위상 반대**: 그들 pore=이온전도체(Bruggeman) / 우리 SE망=이온전도체(Holm). 절대·부호 전이 금지 |
| **σ_thermal** | ❌ 없음 | ★ σ_thermal(0.90 Ridge, multi-pathway) | 우리 고유 |
| **압축 제어** | **CD% = 두께감소율**(변위제어) | 300 MPa 압력(servo) / λ_dz(hold) | CD% ↔ 우리 λ_dz(변위). MPM `hold` = 그들 CD 방식 |
| **입자 소성** | rigid-ish(CONTACT도 명시 약함), CBD-shrink | DEM CONTACT-소성(δ 프록시)+18×연화 / MPM 진짜 SHAPE 소성 | 그들 morphology 없음 = 우리 MPM 이 메움 |
| **검증** | ★ 실험 fabrication + EIS(τ) + 물리모델 재생성(Table 3) | solver=ground truth + 문헌 실험앵커 | 그들 자체 실험 fabrication 보유 |

### 7.2 이온위상 반전 ⚠ (가장 중요한 caveat)
- **그들(LIB 습식):** 이온은 **pore(전해질)** 로 흐른다 → **tortuosity↓ = 이온수송↑**.  압밀↑(CD↑) → porosity↓ → **tortuosity↑**
  (pore 좁아짐) → 이온 나빠짐 BUT 전자 σ_e↑·density↑.  = Bruggeman 계열 trade-off.
- **우리(ASSB 건식):** 이온은 **SE 접촉망** 으로 흐른다 → **σ_ionic ∝ SE percolation/Holm** → 압밀↑ → 접촉↑ → **σ_ionic↑**.
  pore 는 *죽은 공간*.
- ⇒ **그들 tortuosity(이온 proxy)와 우리 σ_ionic 은 압력의존 *부호가 반대*** — 절대값·추세 직접 전이 **절대 금지**.  비교 가능한 건
  *방법론*(τ 계산=TauFactor, σ_e=voxel)과 *최적화 loop 기계장치*뿐, transport 물리 결론 아님.

## 8. ★ APPLICATION to our framework (우선순위 action items)

> 이 논문은 우리 프로젝트의 *published archetype* → "무엇을 흡수 / 어디서 우리가 앞서나 / open question" 을 concrete 하게.

### 8.A 흡수(ADOPT) — 그들 loop 기계장치를 우리 구조 predictor 위에
1. **★★ Sobol(+Saltelli) DOE = 다음 sim batch 설계 (즉시 적용 가능, 최저비용/최고효과).**
   - 현재 우리 corpus 는 ad-hoc design-point + multi-seed, `active_learning_suggest.py` 는 **exploit corner 로 수렴**(realistic 영역
     이미 커버됨을 스스로 인정).  → **exploration 이 약함.**
   - 흡수: 우리 설계공간 **(AM wt%, P:S, r_SE, 압력)** hyper-rectangle 에 **Sobol low-discrepancy** 를 깔아 space-filling.  σ_ionic
     close-out 이 지목한 **구조 gap(CN≥7, 중간 thickness)** 을 균일하게 채우는 데 최적.  Fig S1 이 근거(적은 점에서 Sobol 우월).
   - 우리 도구: `scripts/active_learning_suggest.py` 에 **Sobol seed 모드** 추가(exploit BO 와 병용 = explore+exploit).
2. **★★ SISSO = σ 스케일링 법칙의 *교차검증* + Phase-3 full-metric predictor 후보.**
   - 우리 σ_ionic/σ_e/σ_thermal 은 **손유도 물리폼 + OLS/Ridge**(physics prior LOCKED: Cronau·Holm·Trevisanello·Bruggeman).
   - SISSO 를 우리 corpus(structure descriptor → σ)에 돌려 **"우리 폼을 재발견하나?"** 검증:
     - 재발견하면(√φ_eff·CN²·√cov 류가 나오면) = **손유도 폼의 독립 확증**(frame[4]-형, 강력한 paper 서사).
     - 다른 걸 찾으면 = 놓친 항 후보(단, 우리 close-out 이 이미 정보이론 ceiling 이라 판정 → over-fit 경계).
   - ⚠ **한계 예측:** SISSO 형태 `y=Σc_i·d_i` = descriptor 의 **선형결합** = 우리가 σ_thermal 에서 **실패로 판정한 "단일 backbone/
     pure power-law"**(LOOCV ceiling 0.59, Ridge 필요).  ⇒ σ_thermal 은 SISSO 도 고전 예상 → **multi-pathway 는 SISSO 로도 안 됨**
     이 우리 논지를 *강화*.  σ_ionic/σ_e(단일 backbone)는 SISSO 궁합 좋을 것.
   - Phase-3: 우리 목표 "설계 knob → full metric set 예측" 에서 SISSO 를 **per-metric 해석식 엔진**으로(우리 hand-form 과 병렬 fit,
     둘 다 CV R² 비교).  그들처럼 **각 물성 개별 fit + 3-descriptor + l₀** 로 시작.
3. **★★ GP 다목적 BO + 스칼라화 C_f + GP-Hedge = Phase 3–5 역설계 loop 청사진.**
   - 그들 **Eq 3 스칼라화**(등가중, [0,1] 스케일, min/max 군 분리)를 그대로 채택하되 **가중치는 application 별로**(그들도 "energy
     density 강조 시 density 가중↑, power 강조 시 τ·σ_e↑" 라 명시).  우리 metric set(σ_ionic/σ_e/σ_thermal·porosity·coverage·dip)
     에 확장.
   - **GP-Hedge**(LCB+EI+PI 앙상블 + softmax gain) = skopt 로 즉시 구현 가능.  300-iter, ~100 plateau 가 규모 참고.
   - ⇒ Phase-3(predict)→Phase-4(2D synth, `scripts/extract_2d_microstructure.py synthesize_microstructure`)→Phase-5(layered) 를
     **하나의 BO loop 로 감싸** "설계수치→최적 미세구조" 를 닫는다.  ★ 이 논문이 그 loop 가 *작동하고 실험검증됨*을 증명 = 우리
     로드맵의 de-risking.
4. **PDP + KDE 해석법 흡수:** Phase-3 predictor 의 민감도(어느 knob 이 어느 metric 지배)를 **2D PDP** 로, 최적값의 corpus 내 위치를
   **KDE** 로 → 그들 Fig 4/5A 스타일 대시보드 패널(우리 webapp group-compare 에 추가).
5. **radar + 극단 반면교사(Fig 6) 흡수:** "한 metric 만 극대화 = 다른 것 파괴" 를 우리 whatif 축(σ_e↑↔σ_ionic↓ trade-off,
   PTFE↑↔양쪽↓)에 radar 로 시각화 = 다목적 균형 서사.

### 8.B 우리가 앞서는 것(WE LEAD) — 인용/positioning 무기
1. **★ 구조→σ 기계론 (그들은 black-box).** 그들 SISSO 는 제조→물성 *직결* → **왜 그런지(구조 원인) 못 말함**.  우리는 DEM+MPM
   구조 → Kirchhoff/Holm σ → 스케일링 → **구조 descriptor(φ,CN,cov,τ,percolation)가 인과를 설명**.  positioning: "그들 =
   surrogate, 우리 = mechanistic; 우리 SISSO-흡수는 *구조 descriptor 위에서* 돌아 해석성 유지."
2. **★ 전달 삼중항 σ_ionic/σ_e/σ_thermal + Holm constriction + Stage-E 소성면적.** 그들 = tortuosity(이온 proxy 1채널) +
   GeoDict σ_e(연속체 상한).  우리 = 3채널 + 접촉망 constriction + 소성 접촉면적 보정.  **ASSB SE-망 이온수송은 그들 pore-Bruggeman
   과 위상 반대 → 우리만이 ASSB 이온을 옳게 다룸.**
3. **★ MPM 진짜 소성 morphology (frame[5]).** 그들 캘린더링 DEM = rigid 구(형상불변), CBD-shrink = 부피연산.  우리 MPM = SEM
   일치 형상변화 + void-fill flow + Σdg 변형장.  ⇒ **Varkey/Bazzoun/Duquesnoy 모두 구형-한계** = frame[5] 분업의 *3중 독립확증*
   (제조 시뮬 최전선이 다 형상소성 없음 → 우리 MPM 이 그 칸을 메우는 게 옳음).
4. **★ Furnas dip + bimodal 12:4:1 정량.** 그들 단일 CAM 상 → dip 없음.  우리 DEM/de Larrard 정량 dip(AM 70–85 wt%).
5. **DEM↔MPM 상보 프레임 [1]–[5].** 그들은 단일 파이프라인.  우리는 transport(DEM)·mechanics(MPM)를 각각 실험보정 후 교차검증 —
   수렴=검증/발산=정량화된 한계.  방법론적 엄밀성에서 우위.

### 8.C Open questions (토론 대상)
- **Q1.** SISSO 를 *구조 descriptor* 위에 돌릴까(우리 폼 교차검증), 아니면 그들처럼 *제조 knob* 직결 surrogate 로 돌릴까?
  → 전자가 우리 기계론 정신에 맞고 해석성 유지; 후자가 그들과 apple-to-apple 이고 Phase-3 end-to-end.  **둘 다 해서 CV R² 비교** 제안.
- **Q2.** 우리 σ_thermal 은 Ridge(multi-pathway) → SISSO 의 `Σc_i·d_i` 로는 원리상 한계 예상.  **SISSO 의 rung/complexity 를 높이면**
  (descriptor 차원 3→더, 연산자 확장) multi-pathway 를 잡나?  아니면 우리 "Ridge irreducible" 논지가 SISSO 로도 재확인되나?
- **Q3.** 스칼라화 가중치를 **application(fast-charge/high-energy/durability)별로** 어떻게 설정?  그들은 등가중 proof-of-concept.
  우리는 σ_ionic/σ_e/σ_thermal/porosity/dip/coverage 6+ metric → 가중 설계가 Phase-5 핵심 결정.
- **Q4.** 그들 CD%(두께감소 변위제어) ↔ 우리 압력(servo).  최적화 축을 **압력으로** 둘까 **λ_dz 로** 둘까?  MPM `hold`(변위) = 그들 CD,
  `servo`(압력) = 실제 press.  역설계 출력이 "압력 X MPa" 여야 실용적(제조라인 제어변수).

## 9. 인용 가능 문장 (deck/paper용)
- "The ARTISTIC pipeline (Duquesnoy et al. 2023) is the published archetype of the manufacturing-to-property inverse-design loop we
  target: physics-based simulations (CGMD slurry → drying → DEM calendering) seed a synthetic dataset sampled by Sobol low-discrepancy
  sequences, SISSO symbolic regression yields analytic property = f(AM%, SC%, CD%) surrogates, and Bayesian multi-objective optimization
  (GP + GP-Hedge acquisition + a scalarizing objective) inverse-designs the manufacturing parameters, experimentally validated on a
  fabricated NMC111 cathode."
- "Where Duquesnoy et al. map manufacturing parameters *directly* to properties through a black-box SISSO surrogate, our framework
  resolves the intermediate structure (DEM+MPM microstructure → Kirchhoff/Holm contact-network σ), so that structural descriptors
  (φ, CN, coverage, tortuosity, percolation) carry the causal explanation — we can adopt their optimization machinery (Sobol DOE,
  SISSO cross-check, GP-Hedge BO, scalarization) *on top of* a mechanistic predictor."
- "Their transport treatment — pore-network tortuosity as the ionic proxy plus a GeoDict continuum electronic conductivity — is
  topologically inverted from our all-solid-state case (SE contact network as the ionic conductor, Holm constriction), and carries no
  σ_ionic or σ_thermal channel; the ionic pressure-dependence sign is opposite, so only the loop methodology transfers, not the
  transport physics."
- "Like Varkey (2026) and Bazzoun (2026), the ARTISTIC calendering DEM uses rigid spheres with no true particle-shape plasticity —
  a third independent state-of-the-art confirmation of the frame[5] gap that our MPM plastic-morphology half fills."

## 10. 주의/한계 (over-claim 방지)
- **★ LIB *습식* NMC111 양극 (ASSB 아님) — 이온위상 반전:** 이온 = pore(전해질), tortuosity 가 이온 proxy.  우리 ASSB = SE망 이온.
  **압밀→이온 부호 반대**(그들 CD↑→τ↑→이온↓ / 우리 P↑→σ_ionic↑).  transport 절대값·추세·부호 **직접 전이 절대 금지** — loop 방법론만.
- **σ_ionic·σ_thermal 자체가 없음.** tortuosity·σ_e(GeoDict 연속체)만.  σ_e 는 constriction 없는 **연속체 = 상한**(Bielefeld2020 계열).
- **rigid-ish 구형 DEM 캘린더링 — 진짜 SHAPE 소성 없음.** CBD-shrink 건조 = 부피연산.  morphology·void-fill·변형장 없음(우리 MPM 소유).
- **black-box surrogate (구조 우회):** SISSO 가 제조→물성 직결 → 구조적 인과 없음.  "왜" 를 못 답함 = 우리 기계론이 채우는 칸.
- **단일 CAM 상:** bi/tri-modal PSD·Furnas dip 없음(향후과제 ref 79 언급).
- **NMC111 (≠ NMC811):** CAM 다름(단 spherical rep OK, Franco 그룹).  절대 σ_e·density 소재-특이값 전이 주의.
- **등가중 스칼라화 = proof-of-concept:** 실제 application 가중은 미결정(그들도 인정).
- **digitized vs stated:** 대부분 table=stated.  **입력 범위(AM 86–96·SC 40–71·CD 0–40)는 Fig 2 축에서 digitized(추세)**.
  최적/극단/실험/Table S3 = stated.
- **⚠ Table 1 R²_score 표 오류:** tortuosity·σ_e 를 둘 다 0.933 으로 인쇄(CI95 벗어남) — 신뢰값은 **CI95**(≈0.945/0.98).
  train/test RMSE% 도 tort↔σ_e 스왑 의심.  네 물성 전체는 R² 0.91–0.985 로 잘 맞음(메시지 불변).
- **mass loading 불일치:** 본문 "~15–40 mg/cm²"(시뮬 타깃 범위) vs 실험 Table 4 **6.7 mg/cm²**(실제 제작 전극).  절대 비교 주의.
- **성능(σ) 절대 검증 부분적:** 실험은 porosity·density·thickness·mass loading·τ 만; **σ_e 실험 미측정**(부적절한 실험조건 명시).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

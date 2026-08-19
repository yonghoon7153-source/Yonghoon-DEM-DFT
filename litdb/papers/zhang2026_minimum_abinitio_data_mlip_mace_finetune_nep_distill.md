# Constructing machine learning interatomic potentials with minimum amount of ab initio data — Zhang et al. (npj Comput. Mater. 2026)

> slug `zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill` · DOI `10.1038/s41524-026-02023-y` · type `DFT` (AIMD + MLIP 방법론) · PDF `e670ed15-61.…pdf` (+ SI `66fc5be9-…pdf`, 25 p) · digested `2026-08-19` · status ✅
> elements: Li, Ge, P, S, Al, Ti, O, Y, Cl
> methods: DFT, AIMD, MD, MLIP, NEB
> **저자**: Wentao Zhang¹, Xingxing Wu², Chen Wang³, Siyu Hu³, Yueyang Liu⁴, **Lin-Wang Wang**¹\* — ¹중국과학원 반도체연구소, ²Beijing Lonxun Quantum, ³중국과학원 계산기술연구소, ⁴반도체물리·칩기술 국가중점연구실 · npj Comput. Mater. **12**, 174 (2026), 접수 2025-09-24 / 게재 2026-03-17 · Open Access (CC BY-NC-ND 4.0)
> **코드**: MACE 학습 `https://github.com/hyjwpk/ELoRA` · NEP 학습 `https://github.com/LonxunQuantum/MatPL`
> 자금: National Key R&D Program of China 2024YFA1408200

---

## 0. 이 digest 를 읽는 법

이건 **전해질 물성 논문이 아니라 MLIP 제작 방법론 논문**이다. σ·ESW·기계·밴드갭 숫자를 캐러
오면 안 나온다. 대신 나오는 건 **"범용 MLIP 를 언제 믿고 언제 못 믿는가"의 정량 기준**이고,
그게 우리가 지금(2026-08-19) UMA 로 하고 있는 것과 정확히 겹친다.

읽는 순서 추천: §1 → §3(숫자) → §5.2(왜 평균 RMSE 가 거짓말하나) → §10(우리 적용 판정).
§8 은 repo 를 직접 읽고 쓴 **실행 가능성 실사**다 — 여기만 봐도 "우리가 할 수 있나"는 답이 난다.

⚠ **단위·정의 주의 3개** (아래 본문에서 반복 확인):
1. RMSE 0.25 eV 는 **셀 전체 총에너지** RMSE 다 (평균 73원자) → **≈3.4 meV/atom**. 원자당으로
   바꿔 놓으면 "훌륭한 모델"로 보이고, 그게 이 논문의 함정 논증의 출발점이다.
2. `RRMSE` 는 **RMSE ÷ 참값의 RMS**(평균도 range 도 아님) × 100 %. 목표량이 작으면 부풀려진다.
3. `Fig. 5c` y축 `log(D cm²/s)` 는 **자연로그(ln)** 다 — 아래 §6 에서 검산으로 확인했다.

---

## 1. 한 줄 요약

사전학습 범용 MLIP(MACE-MP-0)는 **총에너지·힘 RMSE 로는 훌륭한데**(0.25 eV/셀 ≈ 3.4 meV/atom,
0.16 eV/Å) **이온 이동 물성에서는 크게 틀린다**(CI-NEB 전이상태 상대에너지 RRMSE ≈ **22.8 %**,
Li 확산계수 RRMSE ≈ **60.8 %**). 저자들은 능동학습 루프를 **전부 없애고**, 사전학습 MACE 로
고온 MD 를 돌려 DIRECT 로 **~200 개**만 추린 뒤 그것으로 MACE 를 파인튜닝하고
(→ NEB RRMSE 7 %대·D RRMSE 13 %대), 다시 그 파인튜닝 MACE 를 **교사**로 삼아 DFT 없이
2000-구조 pseudo-dataset 을 만들어 경량 **NEP 로 증류**해 대규모 MD(1620원자·10 ns)를 돌린다.

**한 문장**: *"MLIP 의 평균 오차가 좋다는 것은 그 MLIP 로 잰 장벽이 맞다는 뜻이 아니다 —
목표 물성으로 직접 검증하고, 안 맞으면 능동학습 없이 수백 개 DFT 로 고칠 수 있다."*

---

## 2. 메타 / 동기

| 항목 | 내용 |
|---|---|
| 검증 계 3종 | **LGPS** Li₁₀GeP₂S₁₂ (황화물, σ_RT ~12 mS/cm) · **LATP** Li₁.₁₆Al₀.₁₆Ti₁.₈₄(PO₄)₃ (NASICON 산화물, x=0.3 에서 ~1 mS/cm) · **LYC** Li₃YCl₆ (할라이드, 넓은 ESW) |
| 왜 이 3종 | 황화물·산화물·할라이드 = SSE 주요 3계열 전부 → "bulk SSE 벤치마크" 커버 주장 |
| 사전학습 모델 | **MACE-MP-0** (uMLIP 대표), 체크포인트 `2024-01-07-mace-128-L2_epoch-199.model` (repo README 확인) |
| 경량 모델 | **NEP** (neuroevolution potential, GPUMD 계열) via MatPL |
| 문제의식 | ① 능동학습은 DFT 수만 회를 요구 ② 범용 uMLIP 는 궤적은 맞아도 목표 물성 정량이 틀림 ③ 큰 모델은 MD 가 느리고 메모리를 먹음 |
| 선행연구와의 위치 | PFD(ref 15, Wang 2025) 도 pre-train→fine-tune→distill 3단이지만 **데이터가 능동학습에서 나온다**는 점이 다르다고 주장. Radova 2025(ref 16, frozen transfer learning)도 인용. ⚠ **둘 다 정면 비교는 없다** (§13) |

---

## 3. 핵심 수치 총정리

### 3.1 MACE-MP-0 out-of-box 정확도 (`Fig. S1`, AIMD 유래 test set)

| 계 | Energy MAE | **Energy RMSE** | Force MAE | **Force RMSE** |
|---|---|---|---|---|
| LGPS | 0.256 eV | **0.322 eV** | 0.131 eV/Å | **0.182 eV/Å** |
| LATP | 0.195 eV | **0.247 eV** | 0.160 eV/Å | **0.220 eV/Å** |
| LYC | 0.133 eV | **0.167 eV** | 0.055 eV/Å | **0.073 eV/Å** |
| **평균** | — | **0.245 ≈ 0.25 eV** ✔ | — | **0.158 ≈ 0.16 eV** ✔ |

> ✔ = 내가 `Fig. S1` 세 패널 제목의 인쇄 숫자로 재계산해 본문의 "0.25 eV / 0.16 eV" 를 **재현**했다.
> ⚠ 이건 **셀 총에너지** RMSE 다. 평균 73원자로 나누면 **3.4 meV/atom** — 논문이 *"These look
> very good"* 이라고 쓴 이유이자, 다음 표가 반전을 만드는 이유다.

### 3.2 그런데 목표 물성은 (`Fig. S6`, MACE-MP-0 기준선)

| 계 | CI-NEB 상대에너지 **RRMSE** | Li 확산계수 D **RRMSE** |
|---|---|---|
| LGPS | figure-read ≈ **35.3 %** | figure-read ≈ **66 %** |
| LATP | figure-read ≈ **9.7 %** | figure-read ≈ **40 %** |
| LYC | figure-read ≈ **23.7 %** | figure-read ≈ **76 %** |
| **평균** | **22.9 %** (본문 "~22.8 %") ✔ | **60.7 %** (본문 "~60.8 %") ✔ |

> ✔ **검산 성공**: 본문의 두 헤드라인 숫자(22.8 %, 60.8 %)는 `Fig. S6` a·c 의 빨간 점선
> (MACE-MP-0 기준선) **3계 산술평균**이다. 내 그림 판독 정밀도 안에서 정확히 재현된다.
> ⇒ **인용해도 안전한 숫자.** 다만 "22.8 %" 는 계마다 **9.7 %~35.3 %로 3.6배 흔들린다** —
> "uMLIP 은 장벽이 ~23 % 틀린다"로 일반화하면 안 된다 (LATP 는 10 % 밖에 안 틀렸다).

### 3.3 파인튜닝 후 (200 configuration, `Table S4–S6`)

| 지표 | LGPS | LATP | LYC | 평균 |
|---|---|---|---|---|
| MACE **ELoRA** Energy RMSE (eV) | 0.06 | 0.05 | 0.02 | 0.043 |
| MACE **ELoRA** Force RMSE (eV/Å) | 0.04 | 0.04 | 0.01 | 0.030 |
| MACE **ELoRA** Force RRMSE (%) | 4.48 | 2.39 | 2.04 | 2.97 |
| **NEB RRMSE (%)** — ELoRA | **10.66** | **2.67** | **7.98** | **7.10** |
| NEB Pearson — ELoRA | 0.996 | 0.999 | 0.999 | — |
| **D RRMSE (%)** — ELoRA | **15.95** | **11.35** | **12.37** | **13.22** |
| RDF RMSE (×10⁻³) — ELoRA | 10.02 | 4.21 | 9.54 | — |

> ⚠ **본문 오기 발견**: 본문은 *"200 configurations … RRMSE … to average **10.7 %** and 13.2 %"*
> 라고 쓴다. `Table S4–S6` 로 직접 계산하면 D 는 (15.95+11.35+12.37)/3 = **13.22 %** ✔ 로 맞는데,
> NEB 는 (10.66+2.67+7.98)/3 = **7.10 %** 다. **10.7 % 는 평균이 아니라 LGPS 단독값(10.66)** 이다.
> 논문이 자기를 과소평가한 방향의 실수라 결론은 안 바뀌지만, **우리가 인용할 땐 7.1 % 를 쓰거나
> "계별 2.7–10.7 %" 로 쓴다.** ("평균 10.7 %"는 틀린 인용이 된다.)

### 3.4 증류 후 NEP (`Table S4–S6`, `Fig. 5a`)

| 지표 | 베이스라인 NEP (200 DFT) | **증류 NEP** (2000 pseudo) | 교사 MACE ELoRA |
|---|---|---|---|
| Energy RMSE 평균 (eV) | 0.137 | 0.107 | 0.043 |
| Force RRMSE 평균 (%) | 7.58 | 6.71 | 2.97 |
| NEB RRMSE 평균 (%) | 17.79 | **12.08** | 7.10 |
| D RRMSE — LGPS / LATP / LYC (%) | – / – / 11.72 | 15.98 / **24.56** / 12.21 | 15.95 / 11.35 / 12.37 |

- 본문 주장 대비 내 검산: **힘 RMSE −11.0 %** → Force RRMSE 로 재계산하면 −**11.1 %** ✔ **재현**.
- **에너지 RMSE −17.1 %** → 표(소수 2자리 반올림)로 재계산하면 −**20~22 %** 가 나온다.
  반올림 폭 안이라 모순은 아니지만 **정확히 재현되지 않는다** — 표 정밀도 부족.
- **NEB 상대에너지 −29.8 %** → 표로는 −**32 %** (RRMSE 평균 17.79 → 12.08). 대체로 재현.
- **LATP 증류 NEP 의 "53.8 % 불일치"**: 본문이 정의를 안 준다. (24.56 − 11.35)/24.56 = **53.8 %**
  로 정확히 떨어지므로 *교사 대비 상대 열화*로 보이지만 — **논문이 명시하지 않았다. 미기재.**
- **베이스라인 NEP 는 LGPS·LATP 에서 D 칸이 비어 있다** — MD 가 불안정해 D 를 못 냈기 때문
  (`Fig. 5a` 캡션: "For models with unstable MD … not included in the comparison"). 즉
  **"증류가 D 를 개선했다"가 아니라 "증류해야 D 를 잴 수라도 있다"** 가 정확한 서술이다.

### 3.5 속도·크기 (`Fig. 5b,c`)

| 항목 | 값 | 출처 |
|---|---|---|
| 추론속도 NEP vs MACE (ASE) 1×1×2 | figure-read ≈ 470 vs 40 steps/s (**~12×**) | `Fig. 5b` |
| 〃 2×2×4 | figure-read ≈ 230 vs 15 (**~15×**) | `Fig. 5b` |
| 〃 3×3×6 | figure-read ≈ 93 vs 4.6 (**~20×**) | `Fig. 5b` + 본문 "20×" |
| LAMMPS/GPUMD 배포 시 (1620원자) | **~600 steps/s, GPU 메모리 ~0.8 GB** | 본문 |
| ⇒ 10 ns MD | 10⁷ step @1 fs ÷ 600 = **4.6 h** ✔ 본문 "a few hours" 와 일치 | 내 검산 |
| LYC 3×3×6 셀 | **1620 원자** (⇒ 1×1×2 는 60 원자 — 내 역산, 논문 미기재) | 본문 |
| σ_RT (LYC, 증류 NEP 외삽) | 대형셀 **~0.3 mS/cm** (실험 0.51) vs 소형셀 **~2.0 mS/cm** | 본문 + `Fig. 5c` |

> ⚠ **"20× 빠르다"는 가장 큰 셀에서만 참이다.** 작은 셀에서는 12× 다 — 우리가 쓰는 셀 크기에
> 따라 이득이 달라진다. 그리고 20× 는 ASE 인터페이스 기준이고, LAMMPS/GPUMD 로 가면
> 93 → ~600 steps/s (6.5× 추가) 다. **속도 이득의 대부분은 엔진 교체에서 온다.**

---

## 4. 논증 흐름 — 섹션별 상세

### 4.1 문제 제기: 두 가지 장애물

서론이 uMLIP 의 두 문제를 못 박는다.
1. **정확도**: *"the universal big models are very often not accurate enough for a given system to
   simulate a particular physical property (e.g., ion migration barriers, thermal conductivities,
   phase transitions). This means the big models might have overall correct shapes (e.g., the
   correct trajectories), but lack the desired quantitative accuracy (perhaps due to the lack of
   the property specific training configurations)."*
2. **속도/메모리**: 큰 모델은 MD 가 느리고 대형계를 못 돌린다.

전통적 해법(능동학습)은 DFT **수천~수만 회**를 먹는다. 이 논문의 표적이 정확히 그 비용이다.

### 4.2 1단계 — 고온 MD 샘플링 전략

**왜 MACE-MD 로 샘플링하나** (AIMD 대신):
- 먼저 AIMD 를 3계에 대해 100 ps 돌리고(LGPS 1500 K, LATP 1500 K, LYC 1200 K), 1000-프레임
  부분집합을 **DIRECT**(dimensionality-reduced encoded clusters with stratified sampling,
  ref 27 Qi/Ong 2024)로 추려 대표 test set 을 만든다.
- ⚠ **에너지 정렬 보정**: uMLIP 예측과 DFT 의 **평균값을 맞춘 뒤** 오차를 평가한다
  (uMLIP 학습 DFT 설정과 우리 DFT 설정이 달라 생기는 계통 시프트 제거). 이걸 안 하면
  총에너지 RMSE 가 무의미해진다 — **우리가 UMA vs QE 를 비교할 때 반드시 따라해야 하는 절차.**
- 그 결과가 §3.1 (좋아 보임) → 그런데 §3.2 (나쁨).

**MACE-MD 궤적이 AIMD 를 대체할 수 있나** (`Fig. 1`, `Fig. S2`):
- Li 확률밀도 등가면: 3계 모두 **3차원 연결성이 유사**, 고에너지 경로에서만 밀도가 줄어듦.
- 특징공간 겹침을 **coverage ratio** 로 정량 (Method Eq 4–5): **M3GNet** 사전학습 모델을
  feature extractor 로 써서 각 구조를 고정길이 벡터로 만들고 → 정규화 → PCA(고유값>1 성분만)
  → 차원별 히스토그램 bin 겹침 → 차원평균. **MACE-MD 가 AIMD 공간의 90 % 를 덮는다.**
- 추가로 `Supplementary Note 4`: CI-NEB 의 **전이상태(TS) 이미지 좌표와 MACE-MD 스냅샷을
  1.0 Å 유클리드 허용오차로 매칭**해, MACE-MD 가 모든 이동 TS 를 **반복적으로 방문**함을 확인
  (`Fig. S10–S12`). 협동 이동은 참여 이온이 **동시에** 조건을 만족해야 매칭으로 센다.
  → *"MD 가 희귀사건을 실제로 밟았는가"를 세는 방법.* 우리가 그대로 차용 가능.
- `Table S1–S3`: 같은 크기 데이터셋을 **AIMD 로 뽑았을 때 vs MACE-MD 로 뽑았을 때** MACE
  from-scratch 성능. 예) LGPS 800개 test Energy RMSE 0.054(AIMD) / 0.041(MACE-MD),
  LATP 800개 0.025 / 0.030. **서로 엎치락뒤치락 = 유의한 차이 없음** → "MACE-MD 로 샘플링해도
  된다"의 근거. (LATP 만 MACE-MD 쪽이 일관되게 약간 나쁘다 — 표를 보면 보인다.)

⚠ **온도가 두 벌이다.** Results 는 "LGPS 1500 K, LATP 1500 K, LYC 1200 K" 라고 쓰고,
Discussion 과 `Fig. 1` 캡션은 "**1050 K** LGPS, 1500 K LATP, **1050 K** LYC" 라고 쓴다.
모순이 아니라 **2단계다**: 1차 고온 스크리닝은 1500/1500/1200 K, 그 다음
**reliability verification** 에서 *비-Li 골격 원자의 MSD* 를 보고 **인위적 골격 융해**
(uMLIP "softening", ref 29 Deng 2025)를 걸러 **최종 샘플링 온도를 1050/1500/1050 K 로 낮췄다.**
→ 이 단계가 이 논문에서 **우리에게 가장 실용적인 한 줄**이다 (§10 Test C).

### 4.3 2단계 — 마이크로 데이터셋에서의 모델 선택 (`Fig. 2`)

데이터셋 크기 10/50/100/200/400/800 로 MACE·NEP 를 **from scratch** 학습.
(train·valid 는 MACE-MD 궤적, **test 는 AIMD 궤적** — 서로 독립.
valid 100 configs, test 1000 configs 고정.)

- `Fig. 2a,b` (에너지·힘 RMSE): **MACE 가 NEP 를 압도**. 심지어 **10–50개**만으로도
  사전학습 MACE-MP-0 의 빨간 점선을 뚫고 내려간다. → *"micro-dataset 에서는 단순한 모델이
  낫다"는 통념(ref 31 matbench)에 반례.* 유일한 NEP 우세 구간은 LYC 10-configs.
- `Fig. 2c` (CI-NEB 상대에너지 RMSE): MACE 가 더 낮고 **더 매끄럽게** 준다. NEP 는
  비단조 — LATP NEP 는 100개에서 0.091 eV 로 **튄다**(50개보다 나쁨).
- `Fig. 2d` (**안정 지속시간**, 100 ps 만점) — 이 논문의 핵심 반전:
  - **LGPS: 800개를 써도 MACE 중앙값 figure-read ≈ 57 ps (박스 52–64), NEP ≈ 20 ps.
    100 ps 를 아무도 못 채운다.**
  - LATP: MACE 는 50개부터 100 ps 도달. NEP 800개 ≈ 88 ps.
  - LYC: MACE 는 200–400개부터 100 ps. NEP 는 800개에서야.
  ⇒ **정확도는 800개로 충분해지는데 안정성은 안 된다.** 이 괴리가 파인튜닝으로 가는 이유.

### 4.4 3단계 — 파인튜닝으로 안정성 확보 (`Fig. 3`)

세 전략 비교: **ELoRA** / **Full fine-tuning** / **From scratch**.

- `Fig. 3a` (에너지 좌축 실선, 힘 우축 파선): ELoRA ≈ Full FT **< From scratch**, 특히
  10-configs 에서 격차 최대(LATP 는 from-scratch 가 배 이상 나쁨). 800개에서 셋이 수렴.
  ⇒ **파인튜닝은 소데이터에서만 이득이다.**
- `Fig. 3b` (CI-NEB 상대에너지 RMSE): ⚠ **여기서는 파인튜닝이 일관되게 이기지 않는다.**
  LGPS 50-configs 에서 from-scratch 0.012 eV 가 ELoRA 0.024 · Full 0.028 을 **이긴다**.
  → 파인튜닝의 이득은 *NEB 정확도 자체*가 아니라 **MD 안정성**에 있다. 본문이 이걸
  명시적으로 인정하지 않는다 (§13 비판).
- `Fig. 3c` (확산계수 RMSE): MACE-MP-0 빨간 점선 대비 파인튜닝이 **LGPS ~4×, LYC ~6× 개선**.
  **from-scratch 는 아예 선이 없다** — MD 가 불안정해 D 를 못 잰다.
  ⚠ **비단조**: LATP ELoRA 는 200개에서 최저(~0.5×10⁻⁵)였다가 400개에서 ~1.5×10⁻⁵ 로 **튄다**.
  "~200개에서 수렴" 이라는 본문 주장과 어긋난다 (§13).
- 본문 요약: *"Models fine-tuned on 200 configurations match the accuracy of models
  trained-from-scratch on 400 configurations."* → **데이터 효율 2×.**

### 4.5 왜 from-scratch 는 MD 가 터지는가 — 메커니즘 (`Fig. 4`)

이 절이 이 논문에서 물리적으로 가장 예쁜 부분이다.

- **통념**: MLIP-MD 실패는 아키텍처 고유 성질이다(ref 34). **저자 주장**: 아니다, 같은 모델·같은
  데이터에서도 파인튜닝 여부가 안정/불안정을 가른다 ⇒ **학습 방식의 문제**다.
- **메커니즘**: MD 붕괴는 두 원자가 너무 가까워질 때 일어난다. MD 로 샘플링한 데이터셋에는
  그런 극단 구조가 **없다**(uncovered region) → 모델이 짧은 거리에서 **낮은 에너지**를 예측 →
  원자들이 한 점으로 **붕괴**한다.
- **진단 지표 = diatomic energy curve**. Li 원자 2개만 든 셀에서 거리 0.1–5.0 Å 를 0.1 Å 씩
  스캔(`Supplementary Note 2`). **turning point** = 힘이 반발→인력으로 급변하는 점
  (판정: 인력이 5 eV/Å 초과 **또는** 연속 3점 인력).
- `Fig. 4b` 판독: **From scratch** 중앙값 figure-read ≈ **1.75 Å**(박스 1.5–1.95, 최대 2.6 Å) —
  **매끄러운 모델이 하나도 없다**(최솟값도 1.2 Å). **Finetuning** 중앙값 ≈ **0.6 Å**(박스 0.1–0.8) —
  박스 하단이 0.1 이라는 건 **최소 25 % 는 완전히 매끄럽다**는 뜻(0.1 = "turning point 없음"의
  약속값). MACE-MP-0 는 0.1(완전 매끄러움).
  ⇒ **파인튜닝은 사전학습 모델의 "매끄러운 단거리 PES"를 상속한다.** 이게 안정성의 정체다.
- **ZBL 로는 못 고친다**: 반발 pair 항(ZBL)을 붙여도 `Fig. S7–S9` 에서 여전히 불안정.
  NEP-ZBL(LATP, 10 configs)은 **2.5 Å 에 turning point** 가 남아 3–5 ps 에서 MD 가 죽는다.
  일부 NEP-ZBL 은 곡선은 매끄러운데 **RDF 가 AIMD 와 크게 달라** 여전히 "불안정" 판정.
  ⇒ *"단거리 반발만 때워서는 PES 매끄러움을 못 산다."*
- 왜 Li–Li 인가: **협동 이동이 Li–Li 반발로 매개**되기 때문(ref 35 He 2017) — 초이온 전도체에서
  이 pair 가 특히 중요하다.

### 4.6 4단계 — 증류로 속도 확보 (`Fig. 5`)

- 파인튜닝된 MACE(ELoRA, 200 configs)를 **교사**로 HT MD 를 돌려 **2000 구조 pseudo-dataset**
  생성. **이 pseudo-dataset 에는 DFT 가 한 번도 안 들어간다** (라벨이 교사 MACE 예측값).
- 그걸로 **NEP 학생**을 학습 → 세 모델 비교: ① 200-DFT 로 학습한 베이스라인 NEP,
  ② 2000-pseudo 로 학습한 증류 NEP, ③ 교사 MACE ELoRA.
- 결과(`Fig. 5a` 레이더, `Table S4–S6`): 증류 NEP 는 교사 대비 에너지·힘이 조금 떨어지지만
  **NEB·RDF·D 는 실용 수준**을 유지하고, **20× 빠르다**.
- `Fig. 5c` — **셀 크기 효과**(LYC, 증류 NEP): ln D vs 1000/T.
  - 400 K 이상(1000/T < 2.5)에서는 **1×1×2 와 3×3×6 이 완전히 겹친다**.
  - 400 K 아래에서 **갈라진다**: 대형셀은 기울기가 급해지고(초이온 전이를 포착),
    소형셀은 완만한 채로 남는다.
  - 300 K 외삽(빈 심볼): 1×1×2 figure-read ≈ **ln D = −17.5**, 3×3×6 ≈ **ln D = −19.4**.
  - ⇒ 소형셀은 σ_RT 를 **~7배 과대평가**한다 (2.0 vs 0.3 mS/cm; 실험 0.51).
  - **저자 결론**: *"This highlights the needs for using large supercells in mobility calculations."*

### 4.7 5단계 — 워크플로 종합 (`Fig. 6`)

```
[데이터셋 구축]   MACE-MP-0 → HT MD 샘플링 → Micro dataset (~200, DFT 라벨링)
[모델 최적화]     Micro dataset → 모델 파인튜닝 → HT MD 샘플링 → Medium dataset(2000, DFT 없음)
                                       └─(내부 루프) 고온 MD → 신뢰성 검증 → 재샘플링
                  → NEP 증류 → 효율적 대규모 MD
```
⚠ `Fig. 6` 오른쪽 파란 박스에 **"고온 MD → 신뢰성 검증 → 재샘플링" 루프가 실제로 있다.**
"single-shot, active learning 루프 없이"라는 주장은 **DFT 를 다시 호출하지 않는다**는 뜻이지
**반복이 없다는 뜻이 아니다.** 인용할 때 이 구분을 지켜야 한다.

### 4.8 Discussion — 저자 스스로 인정한 한계

- 워크플로는 **bulk SSE 상**에서만 검증됐다. **charged system 으로의 확장은 어렵다** —
  현 MLIP 아키텍처가 point charge 프레임워크가 없고 분극을 무시하기 때문(ref 43).
- **이종 셀 확장**(grain boundary, surface)은 새 상·도메인을 만들어 **외삽 실패** 가능.
  LYC bulk 는 `Fig. S13` 로 괜찮다고 봤지만 *"more heterogeneous configurations may lead
  to model extrapolation failures. Assessing the robustness of our workflow in such complex
  systems remains a key focus of future research."*

---

## 5. DFT / 계산 방법 ★

### 5.1 DFT (라벨 생성)
- **code**: **VASP**, **PAW**
- **functional**: **PBE** (LGPS, LATP) — PBE 가 이 두 계의 실험 전도도와 잘 맞는다고 알려져 있고
  MLIP 학습에 널리 쓰이므로(ref 47–49). **LYC 만 optB88-vdW** — PBE-AIMD 가 격자상수를
  과대평가해 σ 외삽이 실험보다 크게 나오는 문제(ref 36) 때문에 비국소 상관 보정(ref 38).
  ⇒ **범함수가 계마다 다르다.** 계간 절대 비교 금지.
- **ecut**: **600 eV** plane-wave, 전 계 공통
- **k-points**: Γ-centered, **KSPACING = 0.25 Å⁻¹**. 단 **AIMD 는 Γ-only**.
- **supercell / nat**: 정확한 셀은 미기재. `Fig. S1` 총에너지 범위와 본문 "average 73 atoms"
  로부터: LGPS ≈ −204 eV, LATP ≈ −812 eV, LYC ≈ −163 eV 급. LYC 3×3×6 = **1620원자**(MD용).
- **DFT+U**: **미기재** (Ti(LATP)·Y(LYC) 에 +U 를 썼는지 안 썼는지 언급 없음 — 재현성 구멍)
- **총 DFT 비용**: **미기재**. 코어시간·wall-time 이 논문 어디에도 없다
  (`core-hour`/`CPU`/`wall` 문자열 0회 — 내가 전문 검색). §10 비용 비교에 직접 못 쓴다.

### 5.2 AIMD / MD
- **ensemble**: NVT, **Nosé–Hoover** thermostat (ref 52, 53)
- **프로토콜**: VASP 로 먼저 이완 → **10 ps velocity scaling 으로 목표온도까지 가열** →
  각 온도에서 **100 ps**, **앞 10 ps 는 평형화로 버림**, **dt = 2 fs**
- **통계**: 각 조건마다 **초기속도가 다른 독립 궤적 3개**
- **저온 LYC(NEP-MD)**: 총 **10 ns**, **dt = 1 fs**, 앞 **500 ps** 버림
- **HT 샘플링 온도**: 1차 1500/1500/1200 K → **신뢰성 검증 후 최종 1050/1500/1050 K** (§4.2)

### 5.3 CI-NEB (`Supplementary Note 1`)
- **climbing-image NEB** (ref 28 Henkelman 2000), **중간 이미지 16개** (우리 SEI NEB 은 7 total)
- 수렴기준·셀 크기·spring constant: **미기재**
- 계별 경로 설계 (**단일 경로가 아니라 다중 채널**이 핵심):
  - **LGPS** (`Fig. S3`): c-방향 채널을 **완전점유(quadruple-ion migration)** vs **공공 포함
    (triple-ion migration)** 두 시나리오 + ab-평면 고에너지 채널 + **c-ab 협동 메커니즘**
  - **LATP** (`Fig. S4`): **단위셀 전체를 관통**하는 경로 — 6개 채널이 연결되고
    **다중 이온 협동 이동**에 의존
  - **LYC** (`Fig. S5`): 층내 Oct–Tet–Oct(side channel) + 층간 Oct–Oct(c 방향) + 고에너지 채널 몇 개
- ⇒ **"장벽 하나"가 아니라 "TS 구조들의 상대에너지 집합"을 RRMSE 로 평가한다.** 이 설계 자체가
  우리 §10 Test A 의 청사진이다.

### 5.4 MLIP 학습
**MACE** (ELoRA repo 기준):
- 사전학습 체크포인트 **MACE-MP-0 `2024-01-07-mace-128-L2_epoch-199.model`**
  (`--model=ScaleShiftMACE`, `num_interactions=2`, `correlation=3`, `max_ell=3`, `r_max=6.0`,
  `max_L=2`, `num_channels=128`, `num_radial_basis=10`, `MLP_irreps=16x0e`)
- 손실 `ef`, `energy_weight=1`, **`forces_weight=1000`**, `lr=0.005`, `weight_decay=1e-8`,
  `batch_size=5`, `amsgrad`, `ema (decay 0.995)`, `lr_factor=0.8`, `scheduler_patience=5`,
  `clip_grad=100`, `E0s=average`, `scaling=rms_forces_scaling`
- **early stopping**: 200 에폭마다 validation loss 확인, **patience 30 에폭** 동안 개선 없으면 종료
  (⚠ "200 에폭마다 확인 + patience 30 에폭"은 문자 그대로면 모순 — 아마 "patience 30 **회 확인**".
  논문 표현 그대로 옮겨 적었고, **해석은 미확정**)
- **ELoRA rank R = 4** (SI 명시)

**NEP** (MatPL):
- MatPL **기본값** + **은닉층 뉴런 100 개로 증가**
- **ZBL "outer" cutoff = 1.8 Å**
- 학습 요동이 커서 **validation 확인 주기 1000 에폭, patience 200 에폭** 로 완화
- MatPL NEP 기본값(내가 소스에서 확인): `cutoff = [8.0, 4.0] Å` (radial/angular), `n_max = [4, 4]`

### 5.5 무질서 처리
**해당 없음 / 미기재.** 세 계 모두 **단일 결정 배열**로 보이고, SQS·enumeration·점유 decorate
언급이 전혀 없다. LATP 의 Al/Ti 무질서(Li₁.₁₆Al₀.₁₆Ti₁.₈₄)와 LYC 의 Li 부분점유를 어떻게
배치했는지 **명시가 없다** — 우리 argyrodite(S/Cl 4a/4d 무질서)와 대조할 때 이 구멍이 중요하다.

---

## 6. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리 활용 |
|---|---|---|
| 1a–c | 좌: Li 확률밀도 등가면(파랑 MACE-MD / 노랑 AIMD, 점선으로 반씩). 우: PC1–PC2 산점도(주황 AIMD / 파랑 MACE-MD). LGPS 1050 K, LATP 1500 K, LYC 1050 K | **MLIP-MD 가 AIMD 를 대체 가능한지 보이는 표준 2단 증명**(밀도맵 + 특징공간 PCA). 우리 UMA-MD 정당화 그림으로 그대로 차용. ⚠ 판독: 겹침이 완전하지 않다 — AIMD(주황)가 −PC1 쪽으로 더 뻗고 MACE-MD(파랑)가 +PC1 로 치우친다. "90 % 겹침"은 100 % 가 아니다 |
| 2a,b | from-scratch MACE(초록) vs NEP(보라) 에너지·힘 RMSE vs 데이터셋 크기(10–800), MACE-MP-0 빨간 점선 | **micro-dataset 에서 큰 모델이 작은 모델을 이긴다**는 반통념 근거. 우리가 "작은 모델부터"로 갈 유혹을 차단 |
| 2c | CI-NEB 상대에너지 RMSE vs 데이터셋 크기 | MACE 가 더 매끄럽게 수렴. NEP 는 비단조(LATP 100개에서 0.091 eV 로 튐) — **비단조는 위험신호**라는 판정 기준 |
| 2d | **안정 지속시간**(100 ps 만점) 박스플롯 | ⭐ **LGPS 는 800개로도 MACE 중앙값 ~57 ps** — 정확도가 좋아져도 안정성이 안 온다는 핵심 증거. 우리 MD 신뢰성 판정에 "RDF 기반 안정시간" 지표 도입 근거 |
| 3a | ELoRA / Full FT / From scratch 의 에너지(좌축 실선)·힘(우축 파선) RMSE | ELoRA ≈ Full FT ≪ From scratch (소데이터 구간). **파라미터 효율 파인튜닝이 전체 파인튜닝과 동급** |
| 3b | 같은 3전략의 CI-NEB 상대에너지 RMSE | ⚠ **파인튜닝이 일관되게 안 이긴다**(LGPS 50개에서 from-scratch 가 이김). 파인튜닝의 이득은 NEB 정확도가 아니라 안정성 — 인용 시 반드시 구분 |
| 3c | 확산계수 RMSE vs MACE-MP-0 점선 | 파인튜닝이 D 를 LGPS ~4×·LYC ~6× 개선. from-scratch 는 선 자체가 없음(MD 불안정). ⚠ LATP ELoRA 200→400 에서 튐 = "200 수렴" 주장 반증 |
| 4a,b | 좌: 안정/불안정 모델의 diatomic 곡선 모식도(uncovered 영역). 우: **turning point 위치** 박스플롯 | ⭐⭐ **MLIP 안정성의 진단 도구**. Li–Li 2원자 셀 0.1–5.0 Å 스캔은 우리도 **한 시간이면 만든다**. from-scratch 중앙 ~1.75 Å vs 파인튜닝 ~0.6 Å vs MACE-MP-0 0.1 |
| 5a | 레이더차트(Energy/Force/NEB/MD RDF/Diffusivity) — NEP / NEP 증류 / MACE ELoRA | 다지표 동시 비교 양식. ⚠ 정규화가 "최고 모델 대비 상대 %" 라 **절대 성능을 못 읽는다** — 숫자는 `Table S4–S6` 로 |
| 5b | 추론속도(steps/s, log) NEP vs MACE, 셀 1×1×2 / 2×2×4 / 3×3×6 | **속도 이득이 셀 크기에 따라 12→20× 로 커진다.** "20×" 를 작은 셀에 적용하면 과장 |
| 5c | ln D vs 1000/T, LYC 증류 NEP, **1×1×2 vs 3×3×6** | ⭐⭐ **소형셀이 σ_RT 를 ~7× 과대평가.** 우리 MLIP-MD 셀 크기 정당화/반성의 직접 근거. 축 라벨이 `log` 인데 실제로는 **ln** (내 Nernst–Einstein 역산으로 확인) |
| 6 | 워크플로 모식도 (데이터셋 구축 / 모델 최적화 2단) | 레시피 한 장. ⚠ 오른쪽에 "신뢰성 검증 → 재샘플링" **루프가 실재**한다 — "single-shot" 은 DFT 재호출이 없다는 뜻 |
| S1 | MACE-MP-0 out-of-box parity plot (에너지·힘), 3계 | 본문 "0.25 eV / 0.16 eV" 의 **원본 숫자**. 계별 MAE/RMSE 가 제목에 인쇄돼 있어 인용 정확도 최상 |
| S6 | RRMSE(NEB) · Pearson(NEB) · RRMSE(D) vs 데이터셋 크기, 4전략 | ⭐ **본문 헤드라인 22.8 %·60.8 % 의 출처.** 빨간 점선 3계 평균으로 내가 재현 성공 |
| S13 | LYC 원자수준 coverage — 소형셀 HT MACE-MD(파랑) vs 대형셀 RT NEP-MD(주황), 원소별 PCA + coverage bar | ⚠ **판독 주의**: 파랑(소형·1050 K)이 주황(대형·300 K)보다 훨씬 넓다. "99.3 % 덮는다"는 당연한 결과 — **뜨거운 소형셀이 차가운 대형셀을 덮는 것**이지 셀 크기 무관을 뜻하지 않는다. `Fig. 5c` 와 정면으로 대비해 읽어야 한다 |
| Table S1–S3 | AIMD-샘플링 vs MACE-MD-샘플링 데이터셋의 from-scratch 성능 (크기 6단계 × valid/test × E/F) | "MACE-MD 로 뽑아도 된다"의 근거. 값이 엎치락뒤치락 = 유의차 없음 |
| Table S4–S6 | 최종 모델 3종(MACE ELoRA / NEP / NEP 증류) 전 지표 수치 | ⭐ **인용용 원본 수치표.** §3.3·3.4 는 전부 여기서 나왔다 |

**내가 실제로 본 그림 (9장)**: `Fig. 1`, `Fig. 2`, `Fig. 3`, `Fig. 4`, `Fig. 5`, `Fig. 6`,
`Fig. S1`, `Fig. S6`, `Fig. S13`.
**안 본 그림 (9장)**: `Fig. S2`(coverage 점수), `S3`–`S5`(이동 채널 구조도), `S7`(ZBL 안정시간),
`S9`(RDF 비교), `S10`–`S12`(TS 매칭 카운트). 캡션과 `Supplementary Note` 본문으로만 서술했다.
**크로핑 실패 1장**: `Fig. S8`(turning point 박스플롯, SI p13) — 벡터 여백이 커서
추출기가 "거의 백지"로 판정해 제외. SI 본문에 축 라벨이 텍스트로 남아 있어 내용은 확인했다
(y축 turning point position 0–2.5 Å, MACE/NEP-ZBL 비교).

---

## 7. Post-processing ★

| 무엇 | 어떻게 | 도구 | 우리 대응 |
|---|---|---|---|
| **CI-NEB** | 채널당 중간 이미지 16개, 계당 2–6 채널. 결과를 **상대에너지 집합**으로 만들어 RRMSE·Pearson 으로 평가 | VASP + CI-NEB (ref 28) | 우리 `tools/sei/` NEB 은 7 images·단일 경로 |
| **RRMSE** (Eq 1) | `RRMSE = RMSE / sqrt(mean(y_ref²)) × 100` — 분모가 **참값의 RMS** | 자체 | 방법 비교의 무차원 지표로 차용 가능 |
| **RDF** (Eq 2) | `g(r) = (1/V_r)(2V/(N(N−1))) ΣΣ δ(r−r_ij)`, 궤적 전체 프레임 평균 | 자체 | — |
| **MD 안정성** (Eq 3) | `∫|⟨g(r)⟩ − ⟨g_t(r)⟩_{t=T}^{T+τ}| dr > Δ` 가 되는 시각 = 안정 지속시간. **τ = 1 ps 창, Δ = 0.5** | 자체 | ⭐ **우리 MLIP-MD 에 없는 지표.** 200 ps 생산 궤적이 끝까지 물리적인지 아무도 안 봤다 |
| **coverage ratio** (Eq 4–5) | **M3GNet** feature → 정규화 → PCA(고유값>1) → 차원별 히스토그램 bin 겹침 → 차원평균 | pretrained M3GNet | UMA-MD ↔ AIMD 정합 증명에 그대로 차용 |
| **원자수준 coverage** (`Note 5`) | MACE-MP-0 **마지막 conv 층의 L₀차 회전불변 특징**을 국소환경 기술자로, **원소별로 따로 PCA**(원소 차이가 PCA 를 지배하지 않도록), 5000 프레임(10-step 간격) 다운샘플, **원자 수 가중합** | 자체 | 가중합 검산: 0.3(0.9986)+0.1(1.0)+0.6(0.9890) = **0.99298 = 99.3 %** ✔ 재현. "atomic number" 는 Z 가 아니라 **원자 개수** |
| **희귀사건 샘플링 검증** (`Note 4`) | CI-NEB TS 이미지의 이동 Li 좌표와 MD 스냅샷을 **1.0 Å 유클리드 허용오차**로 매칭, 협동 이동은 참여 이온 **전부 동시** 만족 시에만 카운트 | 자체 | ⭐ "우리 MD 가 그 안장점을 실제로 밟았나"를 세는 법 |
| **diatomic energy curve** (`Note 2`) | Li 2원자 셀, 0.1–5.0 Å 를 0.1 Å 간격 스캔. **turning point** 판정: 인력 >5 eV/Å **또는** 연속 3점 인력 | 자체 | ⭐ 가장 싸고 즉시 실행 가능한 진단 |
| **DIRECT 재샘플링** | dimensionality-reduced encoded clusters + stratified sampling (ref 27) → 클러스터 수로 데이터셋 크기 제어, **클러스터당 1개** 선택 | ref 27 (Ong 그룹) | 200개 고르는 방법의 원전 |
| **확산계수** | MSD → D. **창 길이·자유절편 여부 미기재** | 미기재 | ⚠ 우리 규약(2–50 ps 고정창)과 대조 불가 |

---

## 8. 코드 실사 — 우리가 돌릴 수 있나 ★★

> 두 repo 를 읽기전용으로 클론해 직접 확인했다. **우리 repo 에 복사하지 않았다.**

### 8.1 ELoRA — `hyjwpk/ELoRA`, HEAD **`d97be7d16b4360f71426f753e0e3f22c3ae818d0`** (2025-07-01)

**정체**: MACE 가 아니라 **e3nn 포크**다. LoRA 를 `o3/_tensor_product/_tensor_product.py`,
`o3/_linear.py`, `nn/_fc.py` 세 곳의 가중치 경로에 심었다. MACE 는 **별도 브랜치**로 배포된다.

**브랜치 3개** (README):
| 브랜치 | 내용 | 설치 |
|---|---|---|
| `main` | ELoRA 가 들어간 **e3nn** | `pip install git+…/ELoRA.git@main` |
| `MACE_baseline` | 전체 파라미터 파인튜닝용 **MACE 포크** | `pip install git+…/ELoRA.git@MACE_baseline` |
| `MACE_ELoRA` | ELoRA 파인튜닝용 **MACE 포크** | `pip install git+…/ELoRA.git@MACE_ELoRA` |
⚠ 우리 클론은 `main` 만 받았다(원격에도 `main` 만 보임 — 나머지 두 브랜치는 별도 fetch 필요).

**의존성**: Python ≥3.7, **PyTorch ≥1.12** (float64 학습은 2.1 불가, **2.2+ 필요**),
numpy/scipy/matplotlib/ase/opt_einsum/prettytable/pandas. e3nn 자체는 sympy·scipy·
`opt_einsum_fx≥0.1.4`. **CUDA 컴파일 없음 — 순수 파이썬.** 설치 난이도 **낮음**.

**사용법**: baseline 과 ELoRA 가 **명령줄이 완전히 동일**하고 **conda env 만 바꾼다**.
진입점은 표준 `mace_run_train` (§5.4 에 전체 플래그 기록).

**사전학습 체크포인트 필요? → 예, 필수.**
`--foundation_model="2024-01-07-mace-128-L2_epoch-199.model"`. MACE-MP-0 는 **게이트가 없어**
공개 다운로드 가능 (UMA 와 대비되는 실질적 장점).

**⚠ 발견한 불일치 (재현성)**: SI `Supplementary Note 3` 은 *"R is the rank of LoRA, which is set
to 4 during this work"* 라고 쓰는데, 클론한 `main` 브랜치 코드에는 **세 파일 모두 하드코딩**돼 있다:
```python
self.alpha = 16
self.r     = 16
```
(`e3nn/nn/_fc.py:22-23`, `e3nn/o3/_linear.py:229-230`,
 `e3nn/o3/_tensor_product/_tensor_product.py:393-394`)
**CLI 플래그도 환경변수도 없다** (`getenv`/`environ`/`argparse` 0회 — 내가 grep). 즉 **논문의
r = 4 를 재현하려면 소스 3곳을 손으로 고쳐야 한다.** `MACE_ELoRA` 브랜치가 덮어쓸 가능성은
남아 있지만(미확인), 공개된 기본값은 16 이다. → **논문 수치를 그대로 재현하려는 사람은 반드시
확인해야 하는 함정.**

**동결 메커니즘**: `main` 브랜치에 `requires_grad=False` 설정이 **없다**. 즉 "베이스 가중치를
얼리고 LoRA 만 학습"하는 코드는 `MACE_ELoRA` 브랜치 쪽에 있어야 하는데 **우리가 확인 못 했다**.
LoRA 의 파라미터 절감 효과가 실제로 얼마인지 **repo 로는 검증 불가** (모델 repr 에
`{LoRA_weight_numel} ELoRA_weights` 를 찍기는 한다).

**LoRA 병합**: `merge_LoRA()` 가 있어 `W ← W + (α/r)·BA` 로 흡수하고 LoRA 텐서를 지운다
→ **추론 시 오버헤드 0**. 배포에 유리.

### 8.2 MatPL (PWMLFF) — `LonxunQuantum/MatPL`, HEAD **`8056b31ead780ddf736c9e5f231f62525d08c8fc`** (2026-07-13)

**의존성** (`requirements.txt`): **`torch==2.2.0+cu118`** (핀 고정!), numpy 1.26.2,
setuptools 68.0.0, ase, tqdm, **cmake 3.30.3**, pyyaml, pandas, scikit-learn-intelex,
matplotlib, **pwdata**, **pwact**, **pybind11**, charset_normalizer 3.3.2, psutil.

**빌드 필요? → 예.** `src/build.sh` 가 있고 하위에
`feature/nep_find_neigh`(CPU), **`feature/NEP_GPU`**(CUDA), **`op/`**(`CMakeLists.txt` +
`kernel/` + `register_op.cpp` = 커스텀 torch CUDA 연산자)를 컴파일한다.
옵션 `-m nn` 이면 **Fortran** 까지 컴파일(NN/Linear 모델용, NEP 에는 불필요).
⇒ **nvcc + cmake 툴체인이 필요하다.** ELoRA 보다 설치 난이도가 확실히 높다.

**실행 형태**: `main.py` + **JSON 설정파일** (`nep_train.json` / `nep_test.json`).
```json
{ "model_type": "NEP", "atom_type": [8, 72], "format": "pwmlff/npy",
  "train_data": ["../pwdata/init_000_50/", ...], "valid_data": [...] }
```
NEP 기본 하이퍼파라미터(내가 `src/user/nep_param.py` 에서 확인):
`cutoff = [8.0, 4.0] Å` (radial/angular), `n_max = [4, 4]`, `zbl` 은 기본 None(명시해야 켜짐),
`type_weight` 는 원소별 1.0. 논문은 여기서 **은닉층 100 뉴런** + **ZBL 1.8 Å** 만 바꿨다.

**LAMMPS 연동**: `src/lmps/` + `example/HfO2/nep_demo/nep_lmps`, `nep_lmps_deviation`
(모델 편차 기반 불확실도까지) 존재. **ASE 연동**도 있다 —
`from src.ase.calculate import MatPL_calculator; calc = MatPL_calculator("nep_to_lmps.txt")`
(또는 `.ckpt`). → 우리 기존 ASE 기반 MD 스크립트에 **계산기만 갈아끼우면** 된다.

**보너스**: `example/LiGePS/` 가 실제로 들어 있다(`100_1200k_movement` + `train.json`/`test.json`).
**황화물 계 예제가 배포판에 있다** — 우리한테 유리한 출발점.

### 8.3 우리 환경 대조

| 환경 | ELoRA(MACE FT) | MatPL(NEP) | 판정 |
|---|---|---|---|
| **gabia** A6000 48 GB, QE-GPU + fairchem/UMA | ✅ 순수 파이썬, torch 2.2+ 별도 env 로 격리 가능 | ⚠ nvcc/cmake 빌드 필요, **torch 2.2.0+cu118 핀**이 기존 `uma`(torch 2.8+cu128)와 충돌 → **반드시 별도 conda env** | 둘 다 가능하나 env 분리 필수 |
| **kgy** RTX 3090 24 GB | ⚠ MACE-MP-0 L2 파인튜닝에 24 GB 는 빠듯 — batch_size 축소 필요 | ⚠ 동일 빌드 이슈 | 가능하나 좁다 |
| **KISTI** neuron, Slurm | ✅ (pip 설치형) | ⚠ 빌드 노드 툴체인 확인 필요 | 미확인 |
| ⛔ **공통 제약** | — | — | **gabia 에서 pw.x 와 GPU 학습 동시 실행 금지**(CLAUDE.md, VRAM 47/48 GB 선례). 파인튜닝은 추론보다 훨씬 무거우므로 **DFT 라벨링과 파인튜닝을 직렬로** 잡아야 한다 — §10 비용 계산에 반영 |

### 8.4 ⭐ UMA 에도 같은 수법이 되나 — **된다. 확인했다.**

> `facebookresearch/fairchem` 을 sparse clone 해 직접 읽었다 (HEAD `de5db01588da…`, 2026-08-17).

**결론: fairchem 은 UMA 파인튜닝을 공식 지원한다. MACE 를 새로 도입할 필요가 없다.**

경로 (`docs/core/common_tasks/fine_tuning.md`):
```bash
# ① ASE-LMDB 데이터셋 + 파인튜닝 YAML 템플릿 생성
python src/fairchem/core/scripts/create_uma_finetune_dataset.py \
    --train-dir <train traj/xyz/cif dir> --val-dir <val dir> \
    --output-dir /tmp/bulk --uma-task=omat --regression-tasks ef

# ② 학습 (기본 1 GPU 로컬)
fairchem -c /tmp/bulk/uma_sm_finetune_template.yaml

# ③ 하이드라 오버라이드로 파라미터 조정
fairchem -c …/uma_sm_finetune_template.yaml epochs=2 lr=2e-4 job.run_dir=… +job.timestamp_id=…
```
추론은 기존과 거의 동일 — 우리 MD 스크립트는 **계산기 생성 두 줄만** 바뀐다:
```python
from fairchem.core.units.mlip_unit import load_predict_unit
predictor = load_predict_unit("…/checkpoints/final/inference_ckpt.pt")
calc = FAIRChemCalculator(predictor, task_name="omat")   # ⚠ 파인튜닝에 쓴 task 와 동일해야 함
```

**중요한 제약과 이점**:
- ✅ `--uma-task=omat` — **우리가 이미 쓰는 omat task 와 일치**. (선택지: omol/odac/oc20/oc22/oc25/omat/omc)
- ⛔ **한 번에 한 task 만** 파인튜닝 가능. 멀티태스크 불가.
- ✅ `--regression-tasks efs` 로 **stress 까지** 학습 가능 → **부피/밀도 편향 교정에 직결**(§10 ②).
- ✅ 커스텀 체크포인트 지정 가능:
  `model._target_ = fairchem.core.units.mlip_unit.mlip_unit.initialize_finetuning_model`,
  `checkpoint_location: /path/to/uma-s-1p1.pt` → **게이트된 HF 를 안 거치고 로컬 uma-s-1p1 사용 가능.**
  (기본 `base_model_name` 은 `uma-s-1p2`.)
- ⛔ **LoRA/ELoRA 는 fairchem 에 없다** — `grep -rni lora src/fairchem/core/` **0건**.
  즉 우리가 UMA 로 가면 **전체 파라미터 파인튜닝**뿐이다. 이 논문의 `Fig. 3a` 가
  "ELoRA ≈ Full FT" 를 보였으므로 **정확도 손해는 없다** — 다만 GPU 메모리·시간이 더 든다.
- ⚠ 부분동결은 `models/base.py` 의 `freeze_backbone` 뿐인데, 이건 **backbone 전체를
  `requires_grad=False`** 로 만들고 head 만 학습한다. **단거리 PES 를 못 고친다** — 이 논문이
  고치려는 바로 그 부분이 backbone 이므로 **우리 목적에는 쓸 수 없다.**
- ⚠ 메모리 레버: `max_neighbors` 기본 300, 문서가 **"메모리가 부족하면 100 이면 대개 충분,
  PES 매끄러움은 유지된다"** 고 명시. 3090(24 GB)에서 쓸 수 있는 손잡이.
- ⚠ 문서는 `--regression-task`(단수), 스크립트 실제 인자는 **`--regression-tasks`(복수)**.
  문서/코드 불일치 — 실행할 사람은 알고 있어야 한다.
- ⚠ Hydra YAML 은 `_target_` 로 임의 코드를 실행한다(공식 문서가 danger 경고). 외부 YAML 금지.
- ⚠ 로깅은 **W&B 만** (Tensorboard 지원 중단), `job.debug=False` 여야 동작.

**⇒ "MACE 를 새로 도입해야 한다"는 비용은 발생하지 않는다.** 이 논문의 워크플로는
모델을 UMA 로 갈아끼운 채 **개념만 그대로** 우리 환경에서 실행 가능하다.
(NEP 증류 단계는 별개 — 그건 MatPL 빌드가 필요하고, 우리에겐 우선순위가 낮다. §10 ③.)

---

## 9. 우리 DFT/MLIP 대비 → `../our_dft_baseline.md`

| 항목 | 이 논문 | 우리 | 차이 / 이유 — **진짜 차이인가 방법 artifact 인가** |
|---|---|---|---|
| 사전학습 모델 | **MACE-MP-0** (L2, 128ch) | **UMA-s-1p1** (omat task) | 다른 uMLIP. **이 논문의 22.8 %/60.8 % 를 UMA 에 그대로 이식할 근거는 없다** — 논문에 UMA 실험이 0건(내가 전문 검색: `UMA` 0회, `SevenNet` 0회, `OMat24` 0회). ⚠ **정성적 경고로만 인용** |
| 참조 DFT | VASP PAW, PBE(LGPS/LATP) · optB88-vdW(LYC), 600 eV, KSPACING 0.25 | QE, PBE | 코드·범함수 축이 다르다. **총에너지 RMSE 는 상호 비교 불가** |
| Ea (황화물) | LGPS 는 RRMSE 만 보고, **절대 Ea 미기재** | comp1 **0.253 eV** · modelc **0.224 eV** (MLIP-MD, 3점 아레니우스) | 직접 비교 대상 없음 |
| NEB | CI-NEB, **중간 16 이미지**, 계당 **2–6 채널**, **협동 다이온 경로 포함** | UMA NEB inter-cage **0.528 eV**, **단일 경로** / SEI DFT NEB `num_of_images=7` | ⭐ **여기가 핵심 차이.** 우리는 채널 1개·이미지 5개(가동). 저자들은 채널 여러 개·이미지 16개 + **협동 이동을 명시적으로 모델링**. 우리 0.528 은 거의 확실히 **단일-Li 홉**이다 |
| **우리 0.528 vs 0.253 (2.1×, ≈109 %)** | uMLIP NEB RRMSE **22.8 %** | 109 % | ⚠ **논문의 효과 크기로는 우리 격차를 설명 못 한다.** 22.8 % 로는 0.253→0.31 까지밖에 못 간다. ⇒ **UMA 탓으로 돌리면 안 된다.** 주원인은 **경로 선택(단일 vs 협동·percolation)** 쪽일 가능성이 훨씬 크다. §10 Test A/B 로 가른다 |
| MD 온도 | 최종 샘플링 **1050 K**(LGPS 황화물) — 1500 K 는 **골격이 인위적으로 녹아서 기각** | 아레니우스 **600/800/1000 K** (400/500 K 제외) | ⚠ **우리 1000 K 가 그들의 1050 K 기각선 바로 아래다.** 황화물 골격(P·S·Cl)의 MSD 를 우리가 확인한 적이 없다. **즉시 확인 대상** (§10 Test C) |
| MD 길이/통계 | AIMD 100 ps(앞 10 ps 폐기) × **독립 3궤적**; NEP-MD 10 ns | 평형 5 ps / 생산 200 ps, **MSD 창 2–50 ps 고정**, 600 K 3-시드 | 우리 생산길이는 충분. **다만 "궤적이 끝까지 물리적인가"를 재는 지표가 우리에겐 없다** — 그들의 RDF 기반 안정시간(Eq 3)이 그 구멍을 메운다 |
| 셀 크기 | LYC 3×3×6 = **1620원자**. 소형셀은 σ_RT **~7× 과대** | 우리 MLIP-MD 셀 크기는 이 digest 범위 밖 | ⭐ **우리 σ 절대값 금지 규율(CLAUDE.md)과 같은 방향의 외부 근거.** 이 논문이 "왜 절대값을 믿으면 안 되는지"를 정량으로 준다 |
| σ 주장 방식 | **절대값을 주장한다** (LYC ~0.3 mS/cm vs 실험 0.51) — 단, 대형셀 + 증류 NEP + 10 ns 를 갖춘 뒤에만 | 우리는 **절대값 인용 금지**, 비율도 멀티시드만 | 우리가 더 보수적. **그들의 조건(1620원자·10 ns·NE)을 우리가 못 갖췄으므로 규율 유지가 맞다** |
| 무질서 | **미기재** (SQS/enumerate 언급 0) | 우리는 4a/4d S·Cl 무질서가 결론을 가르는 축 | 그들 계는 무질서가 우리만큼 지배적이지 않다. **"200개면 된다"가 우리 무질서 계에도 성립하는지는 미검증** |
| DFT 총비용 | **미기재** (core-hour 0회) | — | §10 비용 비교를 **논문 숫자로 못 한다** — 우리 실측으로만 |

---

## 10. ⭐⭐ 우리 cascade · NEB 적용 판정

> 1저자 지시에 따른 진단·처방·비용 절. **코드는 건드리지 않았다.**

### 10.0 먼저 — 이 논문이 우리 문제 3개 중 무엇을 고치나

| 우리 문제 | 이 논문이 고치나 | 판정 |
|---|---|---|
| ① UMA NEB 장벽 부정확 (0.528 vs MD 0.253) | **부분적으로만** | ⚠ 논문의 효과크기(22.8 %)가 우리 격차(109 %)를 **설명 못 한다**. 먼저 원인부터 갈라야 한다 |
| ② cascade `screen_de_per_atom` 축 신뢰도 | **개념적으로 정확히** | ⭐ 가장 잘 맞는 표적. 단 진짜 병목은 **부피/softening**이고, 그건 `--regression-tasks efs` 파인튜닝의 직접 사정권 |
| ③ SEI 확산장벽 DFT 4종 (종당 5일) | **거의 안 고친다** | ⛔ 비용이 손익분기 근처. 아래 산수 참조 |

### 10.1 ① 을 가르는 법 — **두 원인을 섞지 마라**

우리 격차의 후보 원인은 둘이고, 논문은 그중 하나만 다룬다.

- **원인 A (경로)**: NEB 는 *우리가 고른 한 안장점*을 재고, MD Ea 는 *네트워크 전체의
  percolation 율속*을 잰다. argyrodite 전도는 **협동 이동**이고(우리 kb: inter-cage 병목이 율속),
  단일-Li 홉 NEB 는 원래 더 높게 나온다. 논문의 `Fig. S3` 가 LGPS 에서 정확히
  **quadruple-ion vs triple-ion migration** 을 나눠 계산한 이유가 이것이다.
- **원인 B (퍼텐셜)**: UMA 의 안장점 에너지 자체가 틀렸다. 논문이 다루는 건 **이쪽만**이고,
  그 크기는 ~23 % 다.

**Test B 를 먼저 한다 — 가장 싸고 가장 정보량이 크다.**
> 이미 있는 UMA NEB 경로에서 **이미지 5–10개를 뽑아 QE 로 single-point** 를 찍는다.
> 같은 기하 위에서 UMA 프로파일 vs DFT 프로파일을 겹친다.
> **비용: SCF ~10회 = 수 시간.** 새 DFT 캠페인도, 파인튜닝도 필요 없다.
> - 두 프로파일이 20 % 안에서 겹치면 → **원인 B 는 기각**, 0.528 은 경로 문제다. 끝.
> - 크게 어긋나면 → 그때 비로소 파인튜닝이 정당화된다. 그리고 이 10개 SCF 가
>   **파인튜닝 데이터셋의 첫 10개**가 되므로 버려지지 않는다.

**Test A (원인 A 격리, DFT 0회)**: 같은 UMA 계산기로 comp1 의 **대칭적으로 구별되는 경로를
여러 개** NEB 한다 — intra-cage doublet / intra-cage 48h–48h / inter-cage window /
**협동 다중-Li 변형**. 최소경로 또는 percolation 율속 장벽이 0.25 eV 쪽으로 내려오면 원인 A 확정.
논문의 `Fig. S3`–`S5` + `Supplementary Note 1` 이 그대로 설계도다.

**Test C (⭐ 즉시, 비용 0)**: 기존 UMA-MD 궤적에서 **비-Li 골격 원자(P·S·Cl)의 MSD** 를 온도별로
그린다. 1000 K 에서 골격 MSD 가 평탄화되지 않고 기어오르면 우리 아레니우스의 고온 앵커가
오염된 것이고, 그러면 **Ea 가 낮은 쪽으로 편향**된다 — 0.253 이 너무 낮은 이유가 될 수 있다.
논문은 MACE-MP-0 가 LGPS 골격을 1050–1500 K 사이 어딘가에서 인위적으로 녹인다고 실측했고,
**우리 1000 K 는 그 경계 바로 아래다.** 이건 새 계산 없이 **기존 궤적 후처리만으로** 끝난다.

> 순서: **Test C(공짜) → Test B(수 시간) → Test A(UMA만)** → 그래도 안 풀리면 파인튜닝.
> 이 순서를 지키면 파인튜닝을 시작하기 전에 원인이 확정된다.

### 10.2 ② cascade — 여기가 진짜 표적이다

`kb/projects/cascade_pipeline_fixes_2026_08_19.md` 의 실측: **UMA 이완 baseline 이
27.478 Å³/atom = 입력 CIF 대비 +32.7 %, 실험 Li₆PS₅Cl 대비 +49.1 %.** 그래서 `screen_dV_over_V0`
게이트가 **실험 밀도에 도달한 구조를 골라서 버린다.**

이 논문은 그 현상에 이름과 인용을 준다: **uMLIP "systematic softening"** (ref 29, Deng et al.,
npj Comput. Mater. **11**, 1–9, 2025). 저자들은 이걸 **고온 MD 에서의 인위적 골격 융해**로
만났고, **비-Li MSD 검사**로 우회했다. 우리는 같은 병을 **이완 부피**에서 만났다.

**처방**: 우회가 아니라 **교정**이 가능하다 — fairchem 파인튜닝이 `--regression-tasks **efs**`
로 **stress 라벨을 학습**하기 때문이다(§8.4). 부피 편향은 정확히 stress 축의 오차다.
- 데이터: 우리는 이미 **DFT 이완 구조를 갖고 있다**(`modelC` 19.42, `b2o3_relaxV0` 19.034 —
  UMA 가 이 둘은 각각 +0.92 %, −0.00 % 로 **정확히 맞춘다**). 즉 UMA 는 **일부 조성에서만**
  틀린다 → 파인튜닝이 메울 대상이 명확하다.
- 이게 왜 최고 표적인가: cascade 는 한 모델을 **3,615회 이상** 쓴다. 파인튜닝 비용이
  구조 하나당으로 나뉘면 사실상 0 이다. **규모의 경제가 유일하게 성립하는 곳.**
- ⚠ 단, 이 논문은 **부피/EOS 교정을 직접 검증하지 않았다**. `Fig. 3` 은 에너지·힘·NEB·D 만 본다.
  stress 파인튜닝이 부피를 고친다는 건 **우리 추론**이지 논문의 결과가 아니다. 소규모 파일럿
  (조성 3–5개 × ~50 구조)으로 먼저 확인하는 게 맞다.

### 10.3 ③ SEI 확산장벽 — **비용 산수: 손익분기 근처, 권하지 않는다**

**주어진 값**: DFT NEB 4종 × 5일 = **20일** (gabia, QE-GPU 1대).
**우리 NEB 규모** (`kb/projects/sei_products_2026_08_06.md`, `tools/sei/collect_neb.py`):
`num_of_images = 7`(끝점 포함 ⇒ 가동 이미지 5), min_l = 8 Å →
Li₂S 23원자/93e · Li₃P 63/221 · Li₃PO₄ γ 127/605.

**비용 모델** (SCF 1회 = `c`):
```
DFT NEB 1종 = (가동 이미지 5) × (밴드 스텝 50–100) ≈ 250–500 SCF  = 5일  (주어짐)
           ⇒ c ≈ 5일 / (250–500)                                 ≈ 14–29 분/SCF
Zhang 레시피 1종 = 200 SCF (같은 셀, 정적)                        ≈ 2.0–4.0일
                 + uMLIP HT MD 샘플링 (수 시간)
                 + 파인튜닝 (200 config, 1 GPU, 수 시간)
                 + 파인튜닝 모델로 NEB (사실상 공짜, 분 단위)
                 ≈ 2.5–4.5일
```
**4종 합계: 20일 → 10–18일.** 절감 **~2배**, 최선의 가정에서도 그렇다.
그리고 여기에 **직렬화 비용**이 붙는다: gabia 는 **pw.x 와 GPU 학습을 동시에 못 돌린다**
(CLAUDE.md). DFT 라벨링 끝난 뒤에야 파인튜닝을 시작할 수 있어 실제 벽시계는 더 길다.

**⇒ 판정: ③ 에는 적용하지 않는다.** 이유:
1. **규모의 경제가 없다.** 논문은 LGPS·LATP·LYC 를 **각각 따로** 파인튜닝했다 —
   한 모델이 세 계를 커버한다는 증거가 **논문에 없다**. 우리도 4종이면 파인튜닝 4번이다.
   그런데 우리가 종당 원하는 건 **장벽 1–2개**뿐이다. 모델을 만들어 한 번 쓰고 버리는 꼴.
2. **~200 이라는 수가 우리 계에서 검증된 적이 없다.** 논문의 3계는 무질서 처리가 미기재이고,
   우리 Li₃PO₄ γ(127원자)·Li₃P 같은 계에서 200개가 충분한지는 아무도 모른다. 모자라면
   추가 DFT 가 붙어 절감분이 사라진다.
3. **Li₃P 는 애초에 UMA 금지 대상 후보다.** 우리 규율은 Li₃N 에 UMA 금지(2026-06 결정론적 편향)이고
   `sei_products` 카드가 Li₃P 를 같은 Li-pnictide 계열로 보고 **UMA 를 안 쓴다**고 못 박았다.
   파인튜닝이 그 편향을 고칠 수도 있지만 **그걸 증명하는 게 또 하나의 캠페인**이다.

**단, ③ 을 하기로 한다면 붙는 반론 두 개는 정직하게 적어 둔다:**
- **위험 프로파일이 다르다.** 200개 단일점은 **완전 병렬·재시작 가능·수렴 babysitting 불필요**.
  NEB 은 직렬이고 우리 `collect_neb.py` 가 **인용 게이트 3개**(수렴 / CI 켜짐 / 정·역 장벽차
  <0.02 eV)를 강제한다 — 하나만 어겨도 5일이 통째로 날아간다. 실패해도 부분 데이터셋은 남는다.
- **셀 크기를 키울 수 있다.** 같은 예산으로 200 단일점을 **min_l = 10–12 Å** 에서 찍으면
  우리 카드가 남겨둔 "유한 셀 오차" 숙제를 동시에 해결한다. 8 Å NEB 은 그게 안 된다.

### 10.4 그래서 우선순위

| 순위 | 무엇 | 비용 | 근거 |
|---|---|---|---|
| **1** | **Test C** — 기존 UMA-MD 궤적의 비-Li 골격 MSD 를 600/800/1000 K 에서 확인 | **0** (후처리만) | 우리 1000 K 가 논문의 1050 K 기각선 바로 아래. Ea 편향 여부가 걸려 있다 |
| **2** | **Test B** — UMA NEB 이미지 5–10개를 QE 로 single-point | 수 시간 | 0.528 vs 0.253 의 원인을 가른다. 버려지는 계산이 없다 |
| **3** | **diatomic Li–Li 곡선** (`Fig. 4` 방식) 을 UMA-s-1p1 에 적용 | ~1시간 | UMA 의 단거리 PES 가 매끄러운지 = 우리 MD 신뢰의 기반. 지금까지 아무도 안 봤다 |
| **4** | **RDF 기반 MD 안정시간** (Eq 3) 을 기존 200 ps 궤적에 적용 | 후처리 | "생산 궤적이 끝까지 물리적인가"를 우리가 재는 지표가 없다 |
| **5** | **cascade 부피 편향 파인튜닝 파일럿** — `--regression-tasks efs`, 조성 3–5개 × ~50 구조 | 수일 | 규모의 경제가 성립하는 유일한 표적. 단 stress-FT 가 부피를 고친다는 건 **우리 추론** |
| **—** | SEI 4종 파인튜닝 | 10–18일 | ⛔ 손익분기 근처, 재사용 없음 → **권하지 않음** |

1–4는 **DFT 도 파인튜닝도 필요 없고 오늘 있는 데이터로 끝난다.** 이게 이 논문에서 우리가
가져갈 실질의 대부분이다.

---

## 11. 적용 인사이트

- ① **"평균 RMSE 는 목표 물성을 보증하지 않는다"를 우리 언어로 못 박는다.** 3.4 meV/atom 인데
  장벽이 23 %, D 가 61 % 틀린다. 우리가 UMA 를 쓸 때마다 붙여야 할 면책조항이고, 동시에
  **"그러니 목표 물성으로 직접 검증하라"**는 처방이다. 우리 경우 그 검증축은 NEB·D·부피 셋이다.
- ② **MD 안정성과 정확도는 다른 축이다.** `Fig. 2d` 는 800개로도 LGPS 가 100 ps 를 못 채우는 걸
  보여준다. 우리는 200 ps 생산 궤적을 "돌았으니 됐다"로 취급해 왔다 — **RDF 기반 안정시간
  지표를 도입하면 이 가정이 검사 가능해진다.**
- ③ **소형셀은 σ 를 과대평가한다** (`Fig. 5c`, LYC ~7×). 우리 "σ 절대값 인용 금지" 규율의
  외부 정량 근거로 인용 가능. 반대로 **비율 비교는 400 K 이상에서 셀 크기에 둔감**하다는
  것도 같은 그림이 보여준다 — 우리가 600/800/1000 K 에서 비율만 쓰는 게 방어된다.
- ④ **파인튜닝의 진짜 이득은 "사전학습 모델의 매끄러운 단거리 PES 상속"** (`Fig. 4`).
  from-scratch 는 손댈 수 없는 병(ZBL 로도 안 고쳐짐)이 있고, 파인튜닝은 그 병을 안 앓는다.
  → 우리가 언젠가 자체 MLIP 를 만든다면 **from scratch 는 시작부터 지는 선택**이다.
- ⑤ **UMA 파인튜닝 경로가 열려 있다** (§8.4). MACE 도입 비용 0. `--uma-task=omat` 이
  우리 기존 task 와 같고, 추론 코드는 두 줄만 바뀐다. **언제든 시작할 수 있는 상태**라는 것 자체가
  의사결정을 바꾼다 — "할 수 있나"가 아니라 "할 가치가 있나"만 남았다.

---

## 12. 인용 가능 문장

- "Out-of-box MACE-MP-0 reproduces DFT total energies and forces of three benchmark solid
  electrolytes to 0.25 eV per cell (≈3.4 meV/atom, average 73 atoms) and 0.16 eV/Å, yet its
  CI-NEB transition-state relative energies and Li diffusion coefficients deviate by
  ~22.8 % and ~60.8 % RRMSE respectively [Zhang 2026]." — **평균 오차 ≠ 물성 정확도**
- "Fine-tuning a pretrained MACE model on only ~200 DFT configurations, selected in a single
  shot by DIRECT sampling of a MACE-driven high-temperature MD trajectory and without any
  active-learning iteration, matches the accuracy of a from-scratch model trained on 400
  configurations while retaining the MD stability of the pretrained model [Zhang 2026]."
- "MD instability of from-scratch MLIPs originates from an unsmooth short-range potential
  energy surface: diatomic Li–Li curves of from-scratch models show a repulsion-to-attraction
  turning point at ~1.75 Å (median), which fine-tuned models inherit away from the pretrained
  model, and which adding a ZBL repulsive term does not fix [Zhang 2026]."
- "Li₃YCl₆ room-temperature conductivity extrapolated from a 1×1×2 cell overestimates the
  1620-atom 3×3×6 supercell result by roughly an order of magnitude (~2.0 vs ~0.3 mS/cm,
  experiment 0.51 mS/cm), the two agreeing only above the ~400 K superionic transition
  [Zhang 2026]." — **셀 크기 정당화**
- ⛔ **쓰면 안 되는 문장**: "fine-tuning on 200 configurations reduces NEB RRMSE to 10.7 % on
  average" — 본문 오기다(§3.3). 정확히는 **평균 7.1 %**, 계별 2.7–10.7 %.

---

## 13. 주의 / 한계 (over-claim 방지)

**내가 검산한 것 (재현 성공 ✔)**
- 본문 22.8 % / 60.8 % = `Fig. S6` 빨간 점선 3계 평균 → 22.9 % / 60.7 % ✔
- 본문 0.25 eV / 0.16 eV = `Fig. S1` 인쇄값 3계 평균 → 0.245 / 0.158 ✔
- 증류 힘 개선 11.0 % = Force RRMSE 상대 감소 평균 11.1 % ✔
- coverage 99.3 % = 원자 개수 가중합 0.3(0.9986)+0.1(1.0)+0.6(0.9890) = 0.99298 ✔
- 10 ns / 600 steps/s = 4.6 h ("a few hours") ✔
- `Fig. 5c` y축은 **ln** 이다: Nernst–Einstein 역산(n_Li ≈ 1.4×10²² cm⁻³)으로
  ln D = −19.4 → 0.32 mS/cm, ln D = −17.5 → 2.2 mS/cm — 본문의 ~0.3 · ~2.0 과 **둘 다 일치**.
  log₁₀ 로 읽으면 10⁻²⁰ cm²/s 급이 되어 물리적으로 불가능하다. **축 라벨 오기.**

**재현 실패 / 내부 불일치 (⚠)**
1. ⚠ **본문 "average 10.7 %" 는 평균이 아니다.** `Table S4–S6` 로는 7.10 % 이고
   10.66 % 는 LGPS 단독값이다. 논문이 자기를 과소평가한 방향이라 결론은 안 바뀌지만 **오기**.
2. ⚠ **증류 에너지 개선 "17.1 %" 가 표에서 재현되지 않는다** (내 재계산 20–22 %).
   표가 소수 2자리라 반올림 폭 안일 수는 있으나 **검증 불가**.
3. ⚠ **"53.8 % 불일치"의 정의가 없다.** (24.56−11.35)/24.56 = 53.8 % 로 정확히 떨어지지만
   그건 내 추측이다. **미기재.**
4. ⚠ **ELoRA rank 가 SI(4) 와 공개 코드(하드코딩 16) 에서 다르다** (§8.1). CLI 오버라이드 없음.
5. ⚠ **본문이 "Fig. 6c" 라고 쓴 곳은 `Fig. 5c` 다** (`Fig. 6` 은 패널 없는 모식도). 사소한 오타.
6. ⚠ **샘플링 온도가 두 벌**(Results 1500/1500/1200 vs Discussion·`Fig. 1` 1050/1500/1050).
   모순은 아니고 2단계지만, Results 만 읽으면 잘못 재현한다.

**방법·주장의 약점 (§10 판정에 반영됨)**
7. ⛔ **다른 uMLIP 를 전혀 안 봤다.** `UMA` 0회 · `SevenNet` 0회 · `OMat24` 0회 · `eSEN` 0회
   (내 전문 검색). CHGNet·M3GNet·Orb-v3 는 **인용만** 되고 실험되지 않았다. 2026년 논문인데
   **2024–2025 세대 uMLIP(OMat24 학습 모델 포함)이 완전히 빠져 있다.** MACE-MP-0(2023-12/2024-01
   체크포인트)는 이미 구세대이고, "uMLIP 은 장벽이 부정확하다"는 일반 주장의 근거로는
   **표본이 1개**다. → **우리가 UMA 에 이 숫자를 이식하면 안 되는 결정적 이유.**
8. ⛔ **DFT 총비용이 없다.** core-hour/CPU/wall 0회. "훨씬 싸다"는 주장이 **정량화되지 않았다**.
   우리 §10.3 비용 비교를 논문 숫자로 못 하고 우리 실측으로만 해야 했다.
9. ⚠ **ML 학습의 시드 통계가 없다.** `seed` 0회(MD 의 "independent trajectories 3개"는 있다).
   `Fig. 2d`·`Fig. 3` 의 박스플롯은 **데이터셋 크기별 여러 모델**의 분산이지 **같은 데이터·다른
   시드**의 분산이 아니다. `Fig. 3b`·`Fig. 3c` 의 비단조 요동(LATP ELoRA 200→400)이
   **실제 효과인지 학습 시드 노이즈인지 구별할 수 없다.** → "200개에서 수렴"은 **약한 주장**이다.
10. ⚠ **파인튜닝이 NEB 정확도를 일관되게 개선하지 않는다** (`Fig. 3b`: LGPS 50-configs 에서
    from-scratch 가 이김). 본문은 이 반례를 언급하지 않고 넘어간다. 파인튜닝의 이득은
    **MD 안정성**이며, 그것만 주장해야 정직하다.
11. ⚠ **`Fig. S13`(99.3 % coverage)은 셀 크기 문제의 답이 아니다.** 비교 대상이
    **1050 K 소형셀 vs 300 K 대형셀**이라 뜨거운 쪽이 넓은 게 당연하다. `Fig. 5c` 가 같은 계에서
    σ 를 7배 틀리게 준다는 걸 감안하면, "국소환경은 덮지만 **집단적/percolative 물리는 다르다**"가
    정확한 해석이다. 논문은 이 긴장을 명시하지 않는다.
12. ⚠ **베이스라인 NEP 의 D 칸이 LGPS·LATP 에서 비어 있다**(MD 불안정). `Fig. 5a` 레이더에서
    NEP 가 나빠 보이는 정도가 **실제보다 관대하게** 그려진다 — 못 잰 항목은 그냥 빠졌다.
13. ⚠ **DFT+U 미기재.** Ti(LATP)·Y(LYC) 에 U 를 썼는지 안 썼는지 없다. 재현성 구멍.
14. ⚠ **무질서 처리 미기재.** LATP 의 Al/Ti 배치, LYC 의 Li 부분점유를 어떻게 정했는지 없다.
    **우리 argyrodite 처럼 무질서가 지배적인 계에서 "200개면 된다"가 성립할지 미검증.**
15. ⚠ **범함수가 계마다 다르다**(PBE vs optB88-vdW). 계간 절대 비교 금지.
16. ⚠ **선행연구 PFD(ref 15)와 정면 비교가 없다.** PFD 도 pre-train→fine-tune→distill 3단이다.
    저자들은 "PFD 는 데이터가 능동학습에서 나온다"고 구분하지만 **head-to-head 벤치마크는 없다.**
    워크플로 자체의 신규성은 좁고, 실질 기여는 **① 단일샷 MACE-MD+DIRECT 샘플링
    ② MD 불안정의 diatomic-PES 진단 ③ 3계 정량 벤치마크** 세 가지로 보는 게 맞다.
17. ⚠ **저자 본인 인정**: charged system(계면·전기화학)으로 확장 불가(점전하·분극 없음),
    이종 구조(입계·표면)는 외삽 실패 가능. **우리 계면/SEI 문제에는 이 워크플로가 그대로 안 온다.**
18. ⚠ **"single-shot / no active learning"은 절반만 맞다.** `Fig. 6` 에 "고온 MD → 신뢰성 검증 →
    재샘플링" 루프가 실재한다. 정확한 주장은 **"루프 안에서 DFT 를 다시 호출하지 않는다"**.

---

## 14. 기법 용어 미니사전

- **uMLIP (universal MLIP)**: 원소 대부분을 한 모델로 커버하도록 대형 DFT DB(Materials Project 등)
  로 사전학습한 기계학습 퍼텐셜. MACE-MP-0 · CHGNet · M3GNet · **UMA** · Orb-v3 등.
  강점은 "아무 조성이나 바로 돌아간다", 약점은 **특정 계의 특정 물성 정량**.
- **MACE**: 고차 등변(equivariant) 메시지 패싱 GNN. 원자 환경을 회전 대칭성을 지키는 텐서
  (irreps)로 표현하고 **텐서곱**으로 상호작용을 만든다. `max_L=2`는 각운동량 2차까지 씀.
- **NEP (neuroevolution potential)**: 체비셰프/르장드르 기저 기술자 + 얕은 신경망의 **경량** 퍼텐셜.
  메시지 패싱이 없어 훨씬 빠르고 GPUMD/LAMMPS 에서 대규모 MD 에 쓰인다. 정확도는 MACE 아래.
- **LoRA (Low-Rank Adaptation)**: 큰 가중치 `W₀` 를 얼려 두고 저랭크 보정만 학습 —
  `h = W₀x + (α/r)·BAx`, `A ∈ ℝ^{r×d}` 가우시안 초기화, `B ∈ ℝ^{k×r}` **0 초기화**.
  `B=0` 이라 학습 시작 시점에는 원 모델과 **완전히 동일**하다(그래서 안전하다).
- **ELoRA (Equivariant LoRA)**: MACE 의 주 연산인 **완전연결 텐서곱**은 경로 `(l₁,l₂,l₃)` 마다
  별도 가중치를 갖는다. 각 경로에 **따로** LoRA 를 붙여 **등변성을 깨지 않는다**:
  `W^{l₁l₂l₃} + ΔW^{l₁l₂l₃} = W + B^{l₁l₂l₃}A^{l₁l₂l₃}`. 논문 설정 **rank R = 4**
  (⚠ 공개 코드 기본값은 16 — §8.1). 추론 전에 `merge_LoRA()` 로 흡수하면 오버헤드가 사라진다.
- **지식 증류 (knowledge distillation)**: 크고 정확한 **교사** 모델로 라벨을 대량 생성해
  작고 빠른 **학생** 모델을 학습. 여기서는 교사 = 파인튜닝된 MACE, 학생 = NEP,
  pseudo-dataset 2000개 — **DFT 가 한 번도 안 들어간다**는 게 핵심.
- **DIRECT sampling**: *DImensionality-Reduced Encoded Clusters with sTratified sampling*.
  구조 → 특징벡터 → PCA → 클러스터링 → **클러스터당 1개** 선택. 클러스터 개수로 데이터셋
  크기를 직접 제어하고, 구성공간을 고르게 덮는다 (ref 27, Qi/Ong npj Comput. Mater. 2024).
- **RRMSE**: `RMSE ÷ sqrt(mean(y_ref²)) × 100 %`. 분모가 **참값의 RMS**라 스케일이 작은 양
  (전이상태 상대에너지 등)에서 잘 부풀려진다. 절대 RMSE 와 반드시 같이 봐야 한다.
- **CI-NEB (climbing-image NEB)**: 이미지 사슬로 최소에너지경로를 찾되, 최고 에너지 이미지만
  스프링을 풀고 **에너지 언덕을 타고 올라가** 안장점을 정확히 집는다. 이 논문은 중간 16 이미지.
- **turning point (diatomic curve)**: 2원자 에너지 곡선에서 힘이 **반발 → 인력**으로 뒤집히는 거리.
  물리적으로는 있으면 안 된다(가까워질수록 밀어내야 한다). 있으면 MD 에서 원자가 붕괴한다.
  판정: 인력 >5 eV/Å **또는** 연속 3점 인력. 매끄러운 모델은 관례상 0.1 Å 로 표기.
- **ZBL potential**: Ziegler–Biersack–Littmark 경험적 원자쌍 **반발** 항. 짧은 거리에서 억지로
  밀어내게 만든다. 이 논문의 결론은 **이걸로는 PES 매끄러움을 못 산다**는 것.
- **coverage ratio**: 두 구조 집합의 특징공간 겹침. 차원마다 히스토그램을 그려
  `C_d = (A·B 둘 다 채운 bin 수) / (B 가 채운 bin 수)` 를 계산하고 차원평균.
  **비대칭 지표**다 — "A 가 B 를 덮는가"이지 그 반대가 아니다 (§13-11 이 이 함정).
- **systematic softening (uMLIP)**: 사전학습 uMLIP 이 PES 를 계통적으로 **너무 평평하게** 예측하는
  현상 (ref 29 Deng 2025). 결과: 부피 과대, 탄성 과소, 고온에서 인위적 융해.
  **우리 cascade 의 +32.7 % 부피 팽창이 바로 이 병이다.**

---

## 15. INDEX / comparison 에 넣을 항목 (⚠ 파일 충돌 회피 — 다른 에이전트가 반영)

> `litdb/INDEX.md`·`comparison_vs_ours.md`·`comparison_vs_ours_DEM.md` 는 이번에 **건드리지 않았다**
> (`kb/methodology/litdb_shared_branch_convention_2026_08_19.md`).

**INDEX.md 행 (제안)**
```
| 61 | Zhang 2026 | Constructing MLIPs with minimum amount of ab initio data | npj Comput. Mater. 12, 174 | DFT/MLIP 방법론 | LGPS·LATP·LYC | ✅ | zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill |
```

**comparison_vs_ours.md — 축 A (이온전도) 에 추가**
- **[Zhang 2026]** 사전학습 uMLIP(MACE-MP-0)은 총에너지 3.4 meV/atom·힘 0.16 eV/Å 인데도
  **CI-NEB 전이상태 상대에너지 RRMSE 22.8 %(계별 9.7–35.3 %)·확산계수 RRMSE 60.8 %**.
  → **우리 UMA 기반 Ea/D 에 붙일 외부 면책조항.** ⚠ 단 논문은 UMA 를 시험하지 않았다
  (표본 = MACE-MP-0 단일) → **정성적 경고로만** 인용, 숫자 이식 금지.
- **[Zhang 2026]** Li₃YCl₆ 소형셀(1×1×2) 외삽 σ_RT ~2.0 mS/cm vs 대형셀(3×3×6, 1620원자)
  ~0.3 mS/cm (실험 0.51). **400 K 이상에서는 두 셀이 일치.**
  → 우리 **"σ 절대값 인용 금지 · 비율만"** 규율의 정량 근거. 고온 비율 비교는 방어된다.
- **[Zhang 2026]** MACE-MP-0 는 황화물(LGPS) 골격을 고온에서 **인위적으로 녹인다** —
  1500 K 샘플링을 기각하고 비-Li MSD 검사 후 **1050 K** 로 낮췄다.
  → **우리 아레니우스 1000 K 앵커의 건전성을 확인해야 한다** (골격 P·S·Cl MSD 평탄화 여부).

**comparison_vs_ours.md — 방법론/도구 축에 추가**
- **[Zhang 2026]** MLIP-MD 신뢰성 3종 세트: ① **RDF 기반 안정 지속시간**
  (∫|⟨g(r)⟩−⟨g_t(r)⟩|dr > 0.5, τ=1 ps 창) ② **Li–Li diatomic 곡선의 turning point**
  (인력 >5 eV/Å 또는 연속 3점 인력) ③ **비-Li 골격 MSD**. 셋 다 **새 DFT 없이** 기존 궤적/
  계산기만으로 돌아간다 → 우리 UMA-MD 에 즉시 이식 가능.
- **[Zhang 2026 + fairchem 실사]** UMA 파인튜닝 경로 확인:
  `create_uma_finetune_dataset.py --uma-task=omat --regression-tasks efs` → `fairchem -c …yaml`.
  **LoRA 는 fairchem 에 없음(전체 파라미터만)**, `freeze_backbone` 은 head-only 라 단거리 PES 교정에
  부적합. **stress 라벨(efs) 학습이 cascade 부피 편향(+32.7 %) 교정의 후보.**

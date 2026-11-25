# Performance-Based Selection of Machine Learning Interatomic Potentials for Studying Solid-State Electrolytes — Chang, Taqieddin & Laskowski (Chem. Mater. 2026)

> slug `chang2026_performance_based_mlip_selection_sse` · DOI `10.1021/acs.chemmater.5c02352` · type `MLIP 벤치마크 (방법론) + DFT 기준생성 + AIMD + MLIP-MD` · PDF `6a57d51c-105._PerformanceBased_Selection…pdf` (+SI `e4ff4110-105._Sup_…pdf`) · digested `2026-09-09` · status ✅
> elements: Li, P, S, Cl, Br, O
> methods: DFT, AIMD, MD, MLIP
> **서지 (표지 대조 완료 · ✏ 사전 정보 2건 정정)**: **Donghee Chang**, **Amir Taqieddin**, **Forrest Laskowski\*** — **3인 전원이 Solid Power Operating Inc.**, Materials Informatics and Modeling Division (486 S Pierce Ave Suite E, Louisville, CO 80027). 교신 `forrest.laskowski@solidpowerbattery.com`.
> ***Chem. Mater.* 2026, 38 (7), 3133–3144** · 접수 **2025-09-04** / 개정 2026-03-17 / 수락 2026-03-23 / 게재 **2026-04-02** · 본문 **12 pp** (Fig 1–4 · Table 1–3 · refs 65) · SI **16 pp** (Fig S1–S4 · Table S1–S5 · refs 6).
> ✏ **화면에서 본 서지의 정정 2건**: ① 저자에 **"K. Tageddin" 은 없다** — `Amir Taqieddin` 1인이고 이름이 두 번 세어진 것으로 보인다. ② **"외" 가 없다 — 저자는 정확히 3인**이다. 저널·연도(`Chem. Mater. 2026`)는 맞다.
> 자원: **ACCESS / SDSC Expanse** allocation MAT240093 (NSF #2138259 외). 저자 이해충돌 신고 **없음**.
> 🎤 **관련 발표**: **해당 없음.** `litdb/talks/lee2026_skku_mlip_materials_design.md` §99-10 의 인입 대기열(6건+3건)을 전수 확인했고 **이 논문은 그 표에 없다**. talk 역링크 대상이 아니다.

---

## 0. 이 digest 를 읽는 법

- 이 편은 **물성 논문이 아니라 "어떤 MLIP 를 골라야 하나" 논문**이다. 여기 나오는 σ·D·Ea 는 *고른 모델이 잘 도는지 보여주려고* 낸 시연값이고, 조성 최적화를 주장하는 값이 아니다. **우리 `db/properties/*` 절대값과 같은 표에 놓지 않는다.**
- ⚠ **저자 3인 전원이 Solid Power(전고체 배터리 제조사) 소속**이다. 논문 성격은 학술 벤치마크라기보다 **산업 연구팀의 프로덕션 엔진 선정 기록**에 가깝다 — 그래서 "fine-tuning 없이 as-is 로 쓴다", "추론 속도·메모리를 잰다" 같은 실무 축이 살아 있고, 반대로 통계적 엄밀성(시드·오차막대·표본수 관리)은 느슨하다(§10).
- **표기 규약**: 본문/표에 인쇄된 수 = 그대로. 내가 잘라낸 그림 눈금에서 읽은 수 = **`figure-read ≈`**. 내가 이 논문 수로 계산한 것(원논문에 없음) = **`digest 계산 (원논문 미보고)`**.
- **★ 이 편의 핵심이 §10-1 과 §13 에 있다.** 논문의 결론 자체는 우리에게 유리하지만, **Table 3 의 단위 오기 · Boltzmann 가중의 per-atom 오용 · 표본수 3중 불일치**를 잡지 않으면 그 결론을 인용할 수 없다. 그 셋 다 **내가 산술로 재현해서 확인**했다.

---

## 1. 한 줄 요약

Li₆PS₅Cl argyrodite 를 시험대로, **사전학습 범용 MLIP 5종을 fine-tuning 없이 as-is 로** DFT(VASP/PBE) 에 대고 재보니 — **정적 지표(형성에너지 MAE)에서는 다섯 모델이 전부 DFT 자체 불확도(10 meV/atom) 안에 들어와 서로 구분이 안 되고**, 구분은 **동역학**에서 갈린다. 힘을 에너지의 기울기로 얻지 않는 **비보존(direct-force) 모델(ORB v2 · EqV2)** 은 NVT MD 에서 총에너지가 **단조 상승**하고(1100 K 10 ps 에 `figure-read ≈` **+0.4–0.6 eV/atom**), **보존(conservative) 모델(SevenNet · DPA3/DeePMD)** 은 드리프트가 없다. 그래서 **Matbench Discovery 리더보드 순위(ORB v2·EqV2 상위)가 우리 응용의 순위와 일치하지 않는다**는 것이 이 논문의 헤드라인이고, 저자들의 선택은 **SevenNet-l3i5** 다.

부수 결과로 SevenNet-MD 를 S/Cl 자리무질서 6배열에 돌려 **σ 가 2자릿수(0.05 → 41 mS/cm) 벌어진다**는 것과, **cage 간 Li 점프 빈도**가 그 차이를 설명한다는 것을 보인다.

---

## 2. 이 논문이 던지는 질문 (Introduction 의 구조)

저자들이 명시적으로 이탤릭으로 던진 두 질문(p.3134):

> *"Can these models reliably capture subtle energetic trends arising from minor compositional changes or resolve energetic differences associated with local disorder in complex material? Do universal MLIPs faithfully capture the migration pathways and configurational preferences that govern ionic conductivity in real materials?"*

동기의 논리 사슬:
1. argyrodite 튜닝은 **Br, I, F, Se, O, Si, Ge, Sn, As, Sb, Na, Mg, Al 및 그 조합**을 훑어야 하고, 조성마다 anion/Li 부격자 무질서를 **명시적으로 열거·표본추출**해야 한다 ⇒ 유한온도 자유에너지까지 가려면 **수천 배열** ⇒ DFT 로는 불가능.
2. 범용 MLIP 는 그걸 가능하게 하지만, **표준 벤치마크는 "범용 정확도"를 재지 "응용 적합성"을 재지 않는다**(ref 23 = Matbench Discovery).
3. 역전파는 **가장 큰 잔차를 만드는 조성차이**를 우선 학습한다 ⇒ 범용 데이터셋에서 좋은 점수가 **작고 미묘한 배열 차이**에서의 결함을 가릴 수 있다.
4. ⇒ **DFT 바닥상태 탐색(거친 초기구조 → 총에너지 최소화)** 을 기준선으로 삼아 MLIP 를 재자.

저자들이 명시적으로 **fine-tuning 을 안 한 이유** 2가지 (p.3134):
- (a) 산업·소규모 그룹이 **자체 학습데이터 준비 없이** 사전학습 모델을 그대로 쓰는 실제 시나리오를 반영,
- (b) fine-tuning 이 **fine-tuning 데이터셋 쪽으로 편향**을 넣어 탐색적 신물질 연구에서 일반화를 떨어뜨릴 수 있음.
  → ⚠ 이 (b) 는 `tompa2026_finetuning_mlip_foundation_strategies` 가 **정량화한 바로 그 대가**다(비-argyrodite 힘 MAE 1.7배 악화). 두 편이 같은 방향을 가리킨다.

---

## 3. ★1 — 어느 MLIP 를 비교했나 (그리고 **UMA 는 없다**)

### 3.1 모델 5종 (본문 `Table 2` + SI §2)

| 모델 (논문 표기) | 정확한 체크포인트 | 아키텍처 | **사전학습 코퍼스** | **참조 범함수** | 파라미터 | cutoff | 손실 가중 | **힘 = 보존적?** |
|---|---|---|---|---|---|---|---|---|
| **EqV2** | `eqV2 S DeNS` | EquiformerV2 (FAIR Chemistry) | **MPtrj** (+ 학습구조 denoising, DeNS) | **PBE**(MP 설정) | 31.2 M | 12 Å | MAE / E:20, F:20, stress:5, density:10 | ⛔ **direct (비보존)** |
| **DeePMD** | `DPA3-v1-MPtrj` | deep potential NN (DPA3) | **MPtrj** | **PBE** | 4.81 M | 6 Å | R1: MAE E 0.2→20, F 100→20, virial 0 · R2: Huber E 15, F 1, virial 2.5 | ✅ conservative |
| **ORB v2** | `ORB v2 MPtrj` | GNN (비등변, 데이터 주도) | **MPtrj + Alexandria** (pretrain=denoising diffusion, 그 뒤 fine-tune) | **PBE** | 25.2 M | 10 Å | MAE / E:10, F:1, stress:0.1 | ⛔ **direct (비보존)** |
| **SevenNet** | `SevenNet-l3i5` | **NequIP 계열 E(3)-등변 GNN**, spherical harmonics **l=3**, self-interaction layer | **MPtrj** | **PBE** | **1.17 M** (최소) | **5 Å** (최소) | Huber δ=0.01 / E:1, F:1, stress:0.01 | ✅ conservative |
| **MACE** | `MACE-MP-0` | ACE 기반 message-passing NN | **MPtrj** | **PBE** | 4.69 M | 6 Å | MAE / E:1, F:1 | ✅ conservative |

선정 근거(SI §2 원문): *"selected based on their top rankings on the Matbench leaderboard **as of the first quarter of 2025**"*, 전부 **as-is, fine-tuning 없음**, ASE 래퍼로 통합.

### 3.2 ⇒ ★1 의 답 — **UMA / eSEN / OMat24 계열은 들어 있지 않다**

- **UMA 는 피고 목록에 없다.** `uma`·`eSEN`·`OMat24 학습 모델` 전부 부재.
- **가장 가까운 것이 `eqV2 S DeNS`** 다. 이건 UMA 와 **같은 FAIR Chemistry(Meta) 계보**의 직계 조상 아키텍처(EquiformerV2 → eSEN → UMA)이고, SI 참고문헌 (1) 이 **OMat24 논문(Barroso-Luque et al.)** 이다.
  ⚠ **그러나 이 논문이 쓴 eqV2 S DeNS 는 `Table 2` 에 명시된 대로 MPtrj 학습본**이고 **direct-force(비보존)** 다.
  ⇒ **우리 UMA-s-1p1 과는 학습 코퍼스(MPtrj vs OMat24)·힘 형식(direct vs conservative) **양쪽이 다르다**.
  ⇒ ⛔ **"EqV2 가 드리프트했으니 UMA 도 드리프트한다" 는 이 논문으로 말할 수 없다.** 오히려 이 논문의 논거를 그대로 적용하면 **UMA-S 는 보존적이므로 "좋은 쪽"에 배치된다**(§13).
- **피고 5종 전부 참조 범함수가 PBE(MPtrj/Alexandria)** 다. `wang2025_pretrained_deep_potential_sulfide_sse` 때 걸렸던 *"피고가 전부 MPtrj 세대"* 문제가 **여기서도 그대로 반복된다** — 다만 이 논문은 **자기 기준선도 PBE** 라 내부 정합성은 있다(§4).

---

## 4. ★4 — DFT 기준(reference)이 무엇인가

| 항목 | 값 | 출처 |
|---|---|---|
| 코드 | **VASP** (refs 27, 28) | Methods |
| **범함수** | **PBE (GGA)** — *"consistent with widespread use in SSE modeling"* | Methods |
| **평면파 cutoff** | **520 eV** — *"set to match those used in the Materials Project data set"* | Methods |
| **k-점 밀도** | **MP 표준 밀도** (구체 수치 없음) | Methods |
| 수렴 기준 | **MP standard convergence criteria** (구체 수치 없음) | Methods |
| vdW 보정 | ⛔ **없다** (ref 61 = Grimme D3 는 *"PBE 가 격자상수를 과대평가한다"* 논의에서만 인용) | 본문 p.3141 |
| DFT+U | ⛔ **언급 없음** (Li–P–S–Cl–Br–O 라 불필요) | — |
| PAW / POTCAR 셋 | ⛔ **명시 없음** ("MP 설정과 맞춤"으로만) | Methods |
| 스핀 | ⛔ **명시 없음** | — |
| **AIMD 설정** | ⛔⛔ **전혀 없다** — 앙상블(NVT)·길이(10 ps)·온도(500/700/1100 K)·초기구조(SevenNet 평형화본) 외에 **cutoff·k-점·시간간격·thermostat 종류 모두 미기재** | Methods |

### ⇒ ★4 의 답 — **PBE 다. PBEsol 이 아니다.**

**이것이 우리 벤치와의 비교가능성을 결정한다:**
- 이 논문의 라벨 = **VASP / PBE / 520 eV / MP 설정**.
- 우리 `db/properties/mlip_bench_li3ps4_uma.json` 의 라벨 = **PET-MAD Li₃PS₄ (QE / SSSP / **PBEsol** / non-magnetic / vdW 없음)**.
- ⇒ ⛔ **두 벤치의 에너지 오차(meV/atom)를 같은 표에 놓을 수 없다.** 힘은 참조 오프셋에 둔감하므로 "자릿수 비교"까지는 가능하지만, 이 논문은 **힘 오차를 아예 보고하지 않는다**(§10-6). 결국 **직접 비교 가능한 숫자가 하나도 없다.**

논문 스스로도 이 축을 알고 있다 (p.3141):
> GGA-PBE 는 격자상수를 계통적으로 과대평가하고 → Li 이동도를 인위적으로 높인다. **r2SCAN 라벨로 학습한 SevenNet**(ref 53 = Lee et al. ACS AMI 2024)은 50% anion-mixed 구조에서 **~5 mS/cm @300 K** 로 실험과 일치했고, **같은 SevenNet 아키텍처를 GGA-PBE 로 학습한 경우**(ref 52 = Kim et al. JACS 2025)는 **~44 mS/cm @350 K** 였다.
> ⇒ **아키텍처가 아니라 학습 범함수가 σ 를 ~10배 가른다.** 이건 우리 `tools/ionic/mlip_committee.py` docstring 이 이미 적어둔 규율(*"세 모델이 일치해도 절대 σ 인용 금지"*)의 **외부 재확인**이다.

---

## 5. 벤치마크 데이터셋 — 어떻게 만들었나 (`Fig. S4`, SI §1·§3)

### 5.1 모구조와 치환 자리
- 모구조: **Li₇PS₆ argyrodite** (ref 24, Kong 2010).
- 자리 (`Fig. S4a`): **S1 = 16e**(PS₄ 의 S) · **S2 = 4a** · **S3 = 4c** · **Li = 48h**.
- 치환: 할라이드 **Cl⁻, Br⁻ → 4a / 4c**; 산화물 **O²⁻ → 4a, 4c, 또는 16e**(실험 보고와 일치시키려고).

### 5.2 무질서 처리 — **두 갈래**
1. **Li 부격자**: 48h 자리에 **50% 점유(24개)** 를, **Li–Li 거리를 최대화**하도록 골라 저에너지 배열을 근사. ⛔ **전수열거 안 함** — 대표 1배열.
2. **음이온 부격자**: **대칭적으로 유일한 배열을 전수열거**. 총 **S²⁻/X⁻ 102 배열 + Cl⁻/Br⁻ 74 배열** 을 이완.

### 5.3 🔴 **사전선별(prescreening) — 이 논문 최대의 구조적 약점**
전수열거한 배열을 **ORB v2 와 MACE 두 모델로 먼저 이완시켜, 각 모델이 찾은 최저에너지 구조만** DFT 벤치마크 집합에 넣었다 (`Fig. S4c`, `_B`=BFGS · `_F`=FIRE 옵티마이저 표기).
- 살아남은 것: **S²⁻/Cl⁻ 18 · S²⁻/Br⁻ 16 · Cl⁻/Br⁻ 12**.
- 최종 **129 배열** (`Fig. S4b`): Br 치환 16 · Cl 치환 18 · Cl/Br 공치환 49 · **O + Cl/Br 46**.
- SI 가 스스로 인정: *"the resulting set of configurations might be slightly more favorable to ORB v2"*.
- ⛔ **우리 판정 — SI 의 자백보다 더 심각하다.** 이건 "약간 유리"가 아니라 **평가집합의 정의를 피고 2명이 정한 것**이다. SevenNet·EqV2·DPA3 는 *자기가 골랐을 구조가 아닌 것* 위에서 채점됐다. **어느 모델이 4a/4c 바닥상태를 맞추는가** 라는 질문은 이 설계에서 원리적으로 답할 수 없다(§8).

### 5.4 확장 데이터셋 (SI §3, `Table S3`) — **129 → 253**
SI 가 밝히는 사연: S/Cl/Br 혼합 4a/4c 정렬 배열들이 *"inadvertently excluded"* 되어 있었다. 추가분:
- Li₆PS₅X · Li₅.₇₅PS₅X₁.₂₅ 의 Cl⁻ 전 배열 **+29**, Br⁻ 전 배열 **+29**
- Cl/Br 공도핑 Li₅.₇₅PS₅XY₀.₂₅ **+66**
- 최종 (`Table S3`): Br 45 · Cl 47 · Cl/Br 115 · O+할라이드 46 = **253**

---

## 6. ★2 — "performance-based selection" 의 판정 기준은 정확히 무엇인가

⚠ **먼저 결론**: 이 논문에는 **가중합 스칼라 점수도, 문턱도 없다.** 제목의 "performance-based selection" 은 **정량 스코어링 절차가 아니라 서술적 논증**이다. 우리가 `tools/ionic/combine_rankings.py` 에서 걱정하는 *"가중치 근거 없는 스칼라 합성"* 은 **여기선 아예 존재하지 않는다** — 좋은 소식이자, 동시에 **이식할 알고리즘이 없다**는 뜻이다.

### 6.1 실제로 쓰인 지표 전수 (표)

| # | 지표 | 정의 | 어느 계에서 | 문턱 | 어떻게 합쳤나 |
|---|---|---|---|---|---|
| 1 | **compound formation energy MAE / RMSE** | 전이완 후 총에너지로 계산한, **Li₂S·P₂S₅·LiCl·LiBr 전구체 기준** 형성에너지. **각 MLIP 이 자기 PES 로 전구체까지 재계산**(자기정합) | argyrodite 129 + 비-argyrodite 29 (`Table 1`), 확장판 253+29 (`Table S4`) | *"< 10 meV/atom = DFT 자체 불확도"* 를 **서술적 합격선**으로 언급 (ref 38) — **탈락 규칙은 없음** | 합치지 않음 |
| 2 | **R², Spearman rank, Pearson, 회귀 slope, slope 의 R²** | 패리티 회귀 통계 | 위와 동일 | 없음 | 합치지 않음 |
| 3 | **오차 분포의 대칭성·중심성** (box plot) | 중앙값·IQR·수염 (`Fig. 1b,c`) | 위와 동일 | 없음 | **눈으로 판정** |
| 4 | **Ehull 편차** | MLIP 자기 convex hull 기준 energy-above-hull − DFT Ehull | Cl/Br 조성격자 (`Fig. 2d–f`) | 없음 (*"모두 hull 50 meV 이내"* 는 물리 서술) | 합치지 않음 |
| 5 | **구조유형별 분해** | ① MP 유래 비-argyrodite ② Li₇PS₆ 프로토타입에서 치환·재배열 후 전이완한 argyrodite | `Table S1` / `Table S5` | 없음 | **이 분해가 사실상의 판정** — ②에서 SevenNet 이 이긴다 |
| 6 | **E(T) 열전이성** | 10 ps NVT 평균 총에너지 vs T, AIMD 대비 (`Fig. 3a`) | Li₆PS₅Cl 52원자, 500/700/1100 K | 없음 | **눈으로 판정** |
| 7 | **에너지 드리프트** | 10 ps NVT 총에너지 시계열의 단조 상승 (`Fig. S3`) | 위와 동일 | 없음 | **여기가 실질 탈락 기준** |
| 8 | **추론 효율** | atom-steps/s, ns/day, s/step, MaxRSS (`Table S2`) | 1100 K NVT 10 ps, 52원자 | 없음 | 별도 보고 |

### 6.2 실제 선택 논리 (논문 결론부의 문장 순서 그대로)
> 정적 지표는 **전부 합격선 안이라 변별력이 없다** → 그래서 **오차 분포 형태**와 **Ehull 재현**을 본다 → 그래도 ORB v2 가 절대정확도 1등이다 → **동역학으로 넘어가니 ORB v2·EqV2 가 드리프트한다** → 원인을 **보존/비보존 형식**으로 귀속 → **SevenNet 채택**.

⇒ **이식 가능한 것은 "지표 목록과 그 순서"이지 "점수식"이 아니다.** 그리고 이 순서 자체가 우리에게 유용하다(§13-4).

---

## 7. 결과 ① — 형성에너지와 상안정성 (정적 지표)

### 7.1 두 가지 기준 상태
- **formation energy** = 원소 기준 (`Fig. S2`) — 조성 무관 본질적 안정성
- **compound formation energy** = **Li₂S · P₂S₅ · LiCl · LiBr 전구체 기준** (`Fig. 1a`, `Fig. 2a–c`) — **합성 실현가능성**. 음수 = 합성경로가 열역학적으로 유리.
- ★ 두 경우 모두 **전구체 에너지를 각 MLIP 이 자기 PES 로 다시 계산**한다 ⇒ 균일 오프셋은 상쇄되고 **상대 경향만 남는다**는 것이 저자들의 방어 논리.

### 7.2 `Table 1` — 원 데이터셋 (argyrodite 129 + 비-argyrodite 29 = **158**)

| 지표 | EqV2 | DeePMD | **ORB v2** | **SevenNet** | MACE |
|---|---|---|---|---|---|
| MAE [meV/atom] | 6.487 | 6.842 | **4.686** ← 최저 | 4.916 | 9.610 |
| RMSE [meV/atom] | 7.888 | 7.930 | **5.547** ← 최저 | 9.245 | 12.22 |
| R² | 0.986 | 0.985 | **0.993** | 0.980 | 0.965 |
| Spearman | 0.975 | 0.976 | **0.978** | 0.945 ← 최저 | 0.969 |
| Pearson | 0.995 | 0.995 | **0.998** | 0.993 | 0.993 |
| slope | 0.964 | 0.962 | **0.992** | 0.927 ← 최저 | 0.950 |
| slope R² | 0.990 | 0.990 | **0.995** | 0.986 | 0.986 |

- 다섯 모델 **전부 MAE < 10 meV/atom** = DFT 자체 불확도 수준 ⇒ *"전부 고속 스크리닝에 충분하다"*.
- MACE 만 눈에 띄게 나쁘다. 저자 가설: **ACE 의 국소·유한 cutoff 표현이 argyrodite 의 장거리 무질서 상관을 못 담는다** — 스스로 *"further systematic analysis needed"* 라고 단다.
- 🔎 **digest 계산 (원논문 미보고)** — **SevenNet 의 RMSE/MAE = 1.88** 로 유일하게 2에 가깝다(ORB v2 는 1.18). 즉 **SevenNet 은 평균은 좋은데 꼬리가 두껍다.** 논문은 이 점을 한 번도 언급하지 않는다.

### 7.3 `Table S1` — 구조유형별 분해 (이게 결정적이다)

| 구조군 | 모델 | MAE | RMSE | Spearman | Pearson |
|---|---|---|---|---|---|
| **비-argyrodite (MP 유래, 29개)** — Li₂S, LiCl, LiBr, P₂S₅, Li₂O 계 안정상 | EqV2 | 5.588 | 9.985 | 0.9965 | 0.9949 |
| | DeePMD | 5.661 | 8.998 | 0.9913 | 0.9953 |
| | **ORB v2** | **2.198** | **3.430** | 0.9985 | 0.9993 |
| | SevenNet | **10.247** | **19.090** ← 최악 | 0.9904 | 0.9820 |
| | MACE | 10.582 | 17.856 | 0.9899 | 0.9839 |
| **Li₆PS₅X argyrodite (129개, 프로토타입에서 치환→전이완)** | EqV2 | 6.689 | 7.334 | 0.9550 | 0.9955 |
| | DeePMD | 7.107 | 7.669 | 0.9606 | 0.9928 |
| | ORB v2 | 5.246 | 5.920 | 0.9622 | 0.9955 |
| | **SevenNet** | **3.717** ← 최저 | **4.772** ← 최저 | **0.8999** ← 최저 | 0.9943 |
| | MACE | 9.392 | 10.550 | 0.9465 | 0.9926 |

✅ **검산 완료 (digest, 원논문 미보고)**: 두 군의 가중평균이 `Table 1` 을 **다섯 모델 모두 소수 셋째 자리까지 정확히 재현**한다 — 예 SevenNet (29×10.247 + 129×3.717)/158 = **4.916** ✓, ORB v2 → **4.686** ✓, EqV2 → **6.487** ✓, DeePMD → **6.842** ✓, MACE → **9.611** ✓.
⇒ **`Table 1` 의 실제 표본수 N = 158 이다.** 이건 `Fig. 1` 캡션의 "209" 와 `Fig. S2` 캡션의 "206" 을 **산술로 부정한다**(§10-2).

**해석 (논문 + 우리)**:
- ORB v2·EqV2·DPA3 는 **이미 이완된 MP 구조**에서 강하다 = 리더보드가 재는 것 그대로.
- SevenNet 은 **거친 프로토타입에서 출발해 바닥상태를 찾는** 과제에서 이긴다 = **우리가 실제로 하는 일**.
- 🔴 **우리 추가 지적**: SevenNet 의 최악 구조군이 **하필 전구체 화합물군(Li₂S·LiCl·LiBr·P₂S₅·Li₂O)** 이다. 그런데 그 화합물들이 바로 **compound formation energy 의 기준 상태**다. 자기정합 참조로 상당부분 상쇄된다는 저자 논리는 맞지만, **"기준선을 가장 못 맞히는 모델을 기준선 기반 지표로 1등 뽑는" 구조**라는 점은 남는다.

### 7.4 `Fig. 1` — 내가 본 것 (figure-read)

- **`Fig. 1a`** 패리티: x = *Formation energy from benchmark (eV/atom)* **−0.16 … +0.18**, y = 동일 축 MLIP 값, 검은 점선 = DFT-benchmark(y=x). 데이터가 **이봉(bimodal)** 이다 — **−0.16 ~ −0.03 에 조밀한 덩어리**(argyrodite) + **+0.14 ~ +0.18 의 작은 덩어리**와 그 사이 산발점. **MACE(보라) 회귀선만 양의 끝에서 눈에 띄게 패리티 아래로 내려간다.** x≈0.15 에서 y≈0.07 인 이상점 몇 개가 보인다(= 박스플롯 수염에서 제외된 outlier).
  ⚠ **주의**: 조밀한 덩어리 폭이 ~130 meV/atom 인데 모델 간 MAE 차이는 ~5 meV/atom 이라 **이 그림으로는 모델을 구분할 수 없다.** 저자들이 곧바로 박스플롯으로 넘어가는 이유가 이것이다.
- **`Fig. 1b`** Ehull 편차 (y: **Prediction Errors**, −20 … +11 meV/atom): 중앙값 `figure-read ≈` EqV2 **+0.3** · DeePMD **−0.5** · ORB v2 **+0.2** · **SevenNet −2.5** · **MACE −5**. 상자(IQR) EqV2 0~5.5 · DeePMD −0.5~6.5 · ORBv2 0.2~6.8 · SevenNet −4.5~−0.8 · MACE −9~−1. 수염 최악은 MACE(−19).
- **`Fig. 1c`** compound formation energy 편차: 중앙값 `figure-read ≈` EqV2 **+5.2** · DeePMD **+6.2** · ORB v2 **+4.2** · **SevenNet −2.0** · **MACE −9.5**.
  ⇒ **SevenNet 이 0 에 가장 가깝다**는 저자 주장은 그림상 맞다. 다만 **정확히 0 이 아니라 −2 근처**이고, **부호는 음(과소평가)** 이다 — 본문 서술이 이 부호를 세 번 뒤집는다(§10-1).

### 7.5 `Fig. 2` — Cl/Br 조성격자 위의 상안정성

축: x = **4a/4c 자리의 Cl 개수(0–8)**, y = **Br 개수(0–8)**, 삼각 영역(Cl+Br ≤ 8). 8 = 슈퍼셀의 음이온 자리 총수.
- 상단 (a) DFT / (b) ORB v2 / (c) SevenNet — 컬러바 **compound formation energy −0.070 … −0.025 eV/atom**.
  - (a) DFT `figure-read ≈`: 전역이 **−0.045 ~ −0.055** 의 청록. **(Cl=1, Br=1) 에 밝은(−0.035 부근) 국소 극대**, **(Cl=3, Br=1)** 에 작은 것 하나 더. 사변(Cl+Br=8) 쪽이 상대적으로 밝다.
  - (b) ORB v2 `figure-read ≈`: 전체가 **초록(−0.038 ~ −0.043)** 으로 **위로 밀리고 평평해졌다** — 대비 축소.
  - (c) SevenNet `figure-read ≈`: 전체가 **더 어둡다(Br-rich 좌상단이 −0.060 ~ −0.065)** — 대비는 크지만 **DFT 보다 깊다**.
  - 🔴 **그림 vs 본문 긴장**: 본문은 *"SevenNet more accurately captures the shape and depth of the DFT energy contours"* 라고 쓰는데, **컬러 스케일상 SevenNet 은 DFT 보다 확실히 더 깊다**(과대 결합). 맞는 것은 **모양(Br-rich 가 더 음)** 이고, **깊이는 맞지 않는다.** ORB v2 는 반대로 얕고 평평하다.
- 하단 (d) DFT / (e) ORB v2 / (f) SevenNet — 컬러바 **hull distance 0.000 … 0.048 eV/atom**.
  - (d) DFT `figure-read ≈`: 대부분 **0.010–0.025**, (1,1)·(3,1) 에 주황 극대 ≈0.037, 사변 쪽도 주황. **가장 hull 에 가까운 곳은 Br-rich 좌상단(≈0.005–0.012)**.
  - (e) ORB v2 `figure-read ≈`: **전역 0.030–0.040 주황** — 계통적으로 **Ehull 과대**.
  - (f) SevenNet `figure-read ≈`: **0.010–0.028** — DFT 범위와 겹친다.
  ⇒ **Ehull 축에서는 SevenNet 이 확실히 낫다는 저자 주장이 그림으로 뒷받침된다.** ✅
- 물리 결론: **모든 Cl/Br argyrodite 가 전구체 대비 음(합성 유리)** 이지만 **어느 것도 global hull 위에 있지 않고(전부 metastable, 50 meV 이내)**, 알려진 분해상(Li₃PS₄, Li₂S, LiCl, LiBr; refs 45, 46)과 일관.

### 7.6 왜 ORB v2 는 절대값을 잘 맞히면서 상대안정성은 놓치나 (저자 논증)

1. **ORB v2 = 비보존.** E, F, stress 를 **세 개의 독립 출력층**이 한 번의 forward pass 로 예측 ⇒ **F ≠ −∇E**, 에너지 보존 미보장 (refs 48, 49).
2. 통일된 PES 가 없으면 이완 중 **물리적으로 일관되지 않은 힘 방향**이 생겨 거친 초기구조에서 올바른 극소로 못 간다.
3. Bigi et al. (ref 49) 인용: 힘은 **원자중심(국소) 량**이고 에너지는 **전역 량**이므로, 힘을 에너지 기울기로 얻는 모델이 **자동으로 더 넓은 맥락**을 반영한다.
4. **SevenNet = NequIP 계열**, 전 층에서 **E(3) 등변성** 강제 + **l=3 구면조화** + self-connection 대신 **self-interaction layer**(원자 정체성을 층마다 덮어쓰지 않고 유지) ⇒ 미묘한 조성 변화를 넓은 화학적 환경 위에서 포착.
5. **계통 과소안정성(softening)** 은 Deng et al. (ref 42) 이 진단한 일반현상 — 학습셋이 **평형 근처에 치우쳐** PES 곡률이 물러지고, 비평형(결함·표면·무질서) 구조의 에너지를 과소평가한다.
   ⚠ 이 softening 논거는 우리가 이미 `wang2025_pretrained_deep_potential_sulfide_sse` 에서 본 것과 같은 계보다. **다만 이 논문은 UMA 를 시험하지 않았고, 우리 J-1 실측은 UMA 에 대해 그 알리바이를 이미 철회시켰다.**

---

## 8. ★3 — argyrodite 에 대해 **실제로** 무엇을 쟀나 (그리고 무엇을 안 쟀나)

★3 의 전제 3개 중 **2개가 이 논문의 내용이 아니다.** 원문 대조 결과를 먼저 적는다.

| ★3 의 전제 | 원문에서의 실제 위치 | 판정 |
|---|---|---|
| *"anion site preferences"* | p.3134 **Introduction 마지막 문장**의 *동기 열거*: *"…subtle chemical effects such as disorder, **anion site preferences**, dopant-induced charge redistribution, or metastable configurations play a critical role…"* | 🟡 **부분적으로만 측정** — 아래 8.1 |
| *"dopant-induced charge"* | **같은 문장 안**. 논문에 전하 해석은 **한 건도 없다** (`Bader` 0회 · `charge density` 0회 · 전하분석 절 없음). 유일한 전하 언급은 Minafra(ref 3)의 *"anion site disorder → charge inhomogeneity"* **인용** | ⛔ **측정 안 했다** |
| *"a descriptor for the computational screening of argyrodite"* | **참고문헌 (62) 의 제목**이다: *Jun, B.; Lee, S. U. "Designing a descriptor for the computational screening of argyrodite-based solid-state superionic conductors: uniformity of ion-cage size", J. Mater. Chem. A 2022, 10, 7888* | ⛔ **이 논문의 descriptor 가 아니다.** 그 논문은 **우리가 이미 갖고 있다** → `litdb/papers/jun2022_argyrodite_ion_cage_size_descriptor.md` |

### 8.1 음이온 자리선호(4a/4c) — **DFT 로만 쟀고, MLIP 은 채점되지 않았다**

`Table 3` 의 ΔE 열은 **VASP DFT 값**이다 (본문: *"The relative stabilities of these configurations are evaluated using DFT calculations performed with VASP"*). Li₂₄P₄S₂₀Cl₄ (conventional cell, 4 f.u.) 의 **음이온 자리 배열 전수탐색** 결과:

| 배열 # | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| Cl 의 **4a** 점유 | 0% | 25% | 50% | 50% | 75% | **100%** |
| Cl 의 **4c** 점유 | 100% | 75% | 50% | 50% | 25% | 0% |
| **ΔE [meV/atom]** (DFT) | **39.72** | 22.48 | 24.73 | 27.52 | **3.28** | **0 (기준)** |

- **Cl 이 4a 를 100% 점유하는 배열이 바닥상태** — 문헌과 일치 (refs 53, 55).
- **75% 4a 배열이 3.28 meV/atom 밖에 안 높다** = 사실상 축퇴.
- 완전 반자리(4c 100%)만 39.72 로 확연히 불리; 나머지는 **25 meV/atom 이내** ⇒ 상온 접근 가능.
- 실험 대조: Minafra(ref 3) Rietveld — **4a 평균 점유 ~50%**.

🔴 **⇒ ★3-① 의 답: "어느 모델이 4a/4c 를 맞추고 어느 모델이 틀리나" 는 이 논문이 답하지 않는다.**
`Table 3` 에 MLIP 의 ΔE 열이 없고, 6배열의 MLIP 상대에너지 순위도 어디에도 없다. 게다가 §5.3 의 사전선별 때문에 **평가집합 자체를 ORB v2·MACE 가 골랐다** ⇒ 이 질문은 이 설계에서 구조적으로 답할 수 없다. **우리가 직접 재야 한다** (§14 절차 초안).

### 8.2 논문이 실제로 제시한 유일한 정량 descriptor = **cage 간 Li 점프 빈도**

정의 (본문 p.3141, 원문 그대로):
> Li 이온이 **S²⁻ / Cl⁻ 를 중심으로 cage 구조**를 이룬다 → 각 4a/4c 음이온 자리마다 **최근접 Li 수**를 궤적 내내 추적 → **20 fs 샘플링 간격**으로, 어떤 자리 주변의 Li 개수가 **직전 프레임과 다르면 intercage hopping 카운터를 1 증가**.

⛔ **재현에 필요한 값이 빠져 있다**: "최근접(nearest-neighbor)" 의 **cutoff 반경이 명시되지 않았다.** 이게 없으면 빈도의 절대값을 재현할 수 없다.
⚠ **정의 자체의 약점**: 이 카운터는 **배위수 변화**를 세는 것이라, cutoff 경계에서의 rattling·즉시 되돌아옴(recrossing)도 전부 "점프"로 센다. 진짜 자리간 이동(hop)의 상한이지 hop 수가 아니다.

---

## 9. 결과 ② — 보존 vs 비보존: MD 안정성 (★5 의 절반)

### 9.1 MD 규약 전수 (★5 요구 항목)

| 항목 | **MLIP 비교용 (`Fig. 3a`, `Fig. S3`)** | **전도도용 (`Fig. 3b,c`, `Fig. 4`, `Table 3`)** |
|---|---|---|
| 셀 | Li₆PS₅Cl **52 원자** (`Table S2`) | **conventional cell 의 1×2×2 슈퍼셀** — 본문은 *"(containing four formula units)"* 라고 씀 ⚠ (§10-4) |
| 평형화 | **SevenNet 으로만** 수행: 100 K → 목표T, **4.0 fs 마다 1 K** 램프 → NVT **≥20 ps**, dt **2.0 fs** | 동일 램프 → 평형화 **최대 50 ps** |
| 평형 판정 | 마지막 10% 구간 평균 T 가 목표의 **±5%** 이내 | 동일 |
| **초기구조** | **SevenNet 평형화 구조를 전 모델 + AIMD 가 공유** | 배열마다 별도 |
| 생산 | **NVT 10 ps** (모델별) | **NVT 300–450 ps** |
| 온도 | **500 / 700 / 1100 K** | **700 / 900 / 1100 / 1300 K** |
| thermostat | ⛔ **종류·파라미터 미기재** (ASE 사용만 명시) | ⛔ 동일하게 미기재 |
| dt | 2.0 fs (평형화 명시; 생산은 미기재) | ⛔ 미기재 |
| **시드 수** | ⛔ **1** (복수시드 언급 없음) | ⛔ **1** |
| MSD 창 | — | *"fitting the linear region of the MSD (**typically τ > 100 ps**)"* |
| 절편 | ⛔ 미기재 (pymatgen `DiffusionAnalyzer` 사용만 명시) | 동일 |
| **Haven 비** | — | ⛔ 미기재 — **그러나 우리 검산상 실질 Haven = 1** (§9.4) |
| 불확도 | — | **MSD 의 x, y, z 3성분에서 구한 SEM** (등방 가정) |
| AIMD 기준 | 동일 초기구조·NVT·10 ps·같은 온도 | — |

### 9.2 `Fig. 3a` — E(T) 열전이성 (내가 본 것)

y = *Average of total E during 10 ps* (eV/atom) **−4.15 … −3.35**, x = Temperature (K), 실측점 **500 / 700 / 1100 K 3개뿐**.

| 모델 | 500 K | 700 K | 1100 K | 1100 K 오차막대 |
|---|---|---|---|---|
| **BenchMark (AIMD)** | ≈ **−4.105** | ≈ −4.075 | ≈ **−4.015** | 아주 작다 |
| SevenNet | ≈ −4.040 | ≈ −3.970 | ≈ −3.845 | 작다 |
| DeePMD | ≈ −4.030 | ≈ −3.970 | ≈ −3.840 | 작다 |
| **EqV2** | ≈ −4.000 | ≈ −3.925 | ≈ **−3.530** | **≈ −3.35 … −3.72 (거대)** |
| **Orb** | ≈ −3.975 | ≈ −3.885 | ≈ **−3.660** | ≈ −3.60 … −3.77 (큼) |

(전부 `figure-read ≈`)

🔎 **digest 계산 (원논문 미보고)** — 500→1100 K 기울기 dE/dT:
- AIMD **≈1.50×10⁻⁴ eV/atom/K** (≈1.7 k_B/atom — 퍼텐셜에너지만 보는 조화극한 1.5 k_B 와 정합)
- SevenNet **≈3.22×10⁻⁴** · DeePMD **≈3.13×10⁻⁴** ⇒ **AIMD 의 ≈2.1배**
- Orb ≈5.3×10⁻⁴ · EqV2 ≈7.8×10⁻⁴ (드리프트 오염됨)
⇒ ⚠ **"좋은" 두 모델조차 E(T) 기울기가 AIMD 의 2배다.** 논문은 이걸 언급하지 않고 *"minimal drift"* 로만 넘어간다. 열용량류 양을 이 모델들로 뽑으면 안 된다는 뜻이다.

⚠ **절대 세로 오프셋(모든 MLIP 이 AIMD 보다 60–170 meV/atom 위)은 모델 오차로 읽지 말 것.** 우리 `tools/mlip/bench_against_dft.py` docstring 이 이미 적은 대로, **서로 다른 DFT 설정 간 절대 총에너지는 원소별 상수만큼 어긋나며 선형 참조보정 없이는 무의미**하다. 이 논문은 그 보정을 하지 않는다 ⇒ **`Fig. 3a` 의 오프셋은 해석 불가, 기울기만 해석 가능.**

### 9.3 `Fig. S3` — 드리프트 시계열 (내가 본 것)

3패널 (a) 500 K (b) 700 K (c) 1100 K, x = Time 0–10 ps, y = Total E (eV/atom).

| | 500 K | 700 K | **1100 K** |
|---|---|---|---|
| BenchMark(AIMD) | ≈−4.10 에서 **요동만**(±0.01), 드리프트 0 | ≈−4.07 요동만 | ≈−4.01 요동만 |
| **Orb** | −4.022 → **−3.918** (**≈+104 meV/atom / 10 ps**) | −3.952 → −3.795 (**≈+157**) | −3.845 → **−3.42** (**≈+425**) |
| **EqV2** | −4.02 → −3.965 (**≈+55**, 아래로 큰 스파이크 다수) | −3.99 → −3.79 (**≈+200**, 매우 노이지) | −3.845 → **−3.255** (**≈+590**) |
| SevenNet | **완전 수평** −4.038 | 수평 −3.972 | 수평 −3.845 |
| DeePMD | **완전 수평** −4.028 | 수평 −3.972 | 수평 −3.840 |

(전부 `figure-read ≈`, 드리프트 값은 digest 계산)

⇒ **비보존 두 모델의 인공적 에너지 획득이 1100 K 에서 0.4–0.6 eV/atom/10 ps** 다. 52원자면 셀 전체로 **20–30 eV / 10 ps**. 이건 미세한 결함이 아니라 **계를 가열시키는 규모**다. 저자 지적: 이 드리프트가 **Li⁺ 가 겪는 PES 를 왜곡해 확산을 인위적으로 키운다.**

🔴 **내가 본 이상 소견 (논문 미언급)**: **SevenNet·DeePMD 곡선에 열적 요동이 전혀 없다** — 완전한 직선이다. AIMD 검은 선은 ±0.01 eV/atom 요동하는데, 같은 NVT 에서 순간 퍼텐셜에너지가 요동을 안 하는 것은 물리적으로 이상하다. **이 두 곡선만 이동평균/스무딩을 걸었거나 샘플링이 거칠 가능성**이 있고, 그렇다면 드리프트 비교가 부분적으로 서로 다른 처리 위에서 이뤄진 셈이다. 논문은 이에 대해 아무 말이 없다.

### 9.4 `Table S2` — 추론 효율 (1100 K NVT 10 ps, **52원자**, SDSC Expanse)

| 모델 | atom-steps/s | ns/day | s/ps | s/step | MaxRSS |
|---|---|---|---|---|---|
| EqV2 S DeNS | 51 | 0.168 | 514.8 | 1.0296 | 3.922 GB |
| DPA3-v1-MPtrj | 80 | 0.266 | 324.7 | 0.6494 | 3.989 GB |
| **ORB v2 MPtrj** | **462** | **1.535** | **56.3** | **0.1126** | **0.826 GB** |
| SevenNet-l3i5 | 117 | 0.390 | 221.8 | 0.4436 | 1.116 GB |

- **ORB v2 가 SevenNet 보다 4.0배 빠르고 메모리도 1/1.4** ⇒ **정확도 때문이 아니라 물리적 일관성 때문에 4배 느린 쪽을 고른 것**이 이 논문의 실질적 선택이다.
- **MACE 는 이 표에 없다** — MD 를 돌리지 않았다(§10-3).
- ⛔ **하드웨어 미기재**: Expanse 는 CPU 노드(AMD EPYC)와 GPU 노드(V100) 둘 다 있는데 **어느 쪽인지, 코어 수가 몇인지 없다.** 52원자에서 0.39 ns/day 는 GPU 치고 매우 느리다 ⇒ **이 수치는 상대비교용으로만**.

---

## 10. 결과 ③ — 이온수송: D · Ea · σ (★5 의 나머지)

### 10.1 기준 배열의 Arrhenius (`Fig. 3b`, 내가 본 것)

- x = **1000/T (K⁻¹) 0.75 … 3.5**, y = **Diffusivity (cm²/s), log 1e-9 … 1e-4**.
- 붉은 원 **4개**: 1000/T ≈ 0.77 / 0.91 / 1.11 / 1.43 = **1300 / 1100 / 900 / 700 K**.
  값 `figure-read ≈` **6.5×10⁻⁵ / 4.3×10⁻⁵ / 1.35×10⁻⁵ / 3.0×10⁻⁶ cm²/s**.
- 주황 별 = **300 K 외삽점**, ≈ **3.6×10⁻¹⁰ cm²/s** (= `Table 3` 배열 5 값 ✓).
- **인쇄된 값: Ea = 0.41 ± 0.02 eV.**
- ⚠ **최저 측정온도가 700 K 이고 300 K 까지 400 K 를 외삽한다.** 우리 규약(600/800/1000 K, 400/500 K 제외)보다 **더 높고 더 좁은 창**이다.

### 10.2 🔴🔴 `Table 3` 의 **단위 오기** — 그림이 표를 부정한다

`Table 3` 은 **Ea 열의 단위를 `[meV]`** 로 인쇄했다:

| 배열 # | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 4a / 4c (Cl) | 0/100% | 25/75% | 50/50% | 50/50% | 75/25% | 100/0% |
| ΔE [meV/atom] (DFT) | 39.72 | 22.48 | 24.73 | 27.52 | 3.28 | 0 |
| **Ea [meV]** ← 인쇄된 대로 | 26.8 | 20.7 | 20.1 | **19.7** | 23.9 | **40.6** |
| D₃₀₀K [cm²/s] | 2.4×10⁻⁸ | 1.9×10⁻⁷ | 1.7×10⁻⁷ | **2.7×10⁻⁷** | 7.1×10⁻⁸ | **3.6×10⁻¹⁰** |
| σ₃₀₀K [mS/cm] | 3.75 | 30.06 | 27.10 | **41.02** | 10.86 | **0.05** |

**⇒ 이 단위는 틀렸다. 실제 단위는 eV 다.** 근거 3개(전부 내가 확인):
1. **`Fig. 3b` 에 `Ea = 0.41 ± 0.02 eV` 라고 인쇄돼 있고**, 그 그림은 100%-0% 배열(= 배열 5)의 Arrhenius 다. 표의 **40.6** ↔ 그림의 **0.406 eV**. **1000배 차이.**
2. Ea = 40.6 **meV** 라면 D(700 K)/D(300 K) 가 겨우 2.4배여야 하는데, `Fig. 3b` 는 **약 8000배**를 보여준다.
3. 검산: Ea = 0.406 eV, D₃₀₀ = 3.6×10⁻¹⁰ → **D₀ = 2.4×10⁻³ cm²/s, D(700 K) = 2.8×10⁻⁶** — `Fig. 3b` 의 `figure-read ≈ 3.0×10⁻⁶` 와 일치. meV 로 읽으면 전혀 안 맞는다.

⇒ **인용 시 반드시 "표에는 meV 로 인쇄돼 있으나 실제는 eV" 라고 밝혀야 한다.** 그러면 배열별 Ea 는 **0.197 – 0.406 eV** 범위이고, 이건 argyrodite 문헌·우리 값(comp1 0.253 / modelc 0.224 eV)과 같은 자릿수다.

### 10.3 σ ↔ D 관계 — **Nernst–Einstein, Haven = 1** (검산 완료)

논문은 Haven 비를 안 밝힌다. 내가 역산했다 (`digest 계산 (원논문 미보고)`): Li₆PS₅Cl conventional cell(a ≈ 9.86 Å, Li 24개) 의 Li 밀도로 σ = n q² D / k_BT 를 계산하면

| D₃₀₀K | NE(Haven=1) σ | 논문 σ |
|---|---|---|
| 2.4×10⁻⁸ | **3.73** | 3.75 |
| 3.6×10⁻¹⁰ | **0.056** | 0.05 |
| 2.7×10⁻⁷ | **41.9** | 41.02 |

⇒ **2% 이내로 재현.** 즉 σ 는 **Haven 비 1 의 Nernst–Einstein** 이다 (pymatgen `DiffusionAnalyzer` 기본). 우리 규약과 **동일**하다.

### 10.4 🔴🔴 앙상블 평균 σ = 14.67 mS/cm 의 **가중치가 잘못됐다**

논문 (p.3141):
> *"By applying Boltzmann weighting based on the relative formation energies of each configuration at room temperature (300 K), a statistically averaged ionic conductivity of **14.67 mS/cm** is determined. This ensemble-averaged value compares favorably with the experimentally reported conductivity of **~5 mS/cm** for polycrystalline Li₆PS₅Cl."*

내가 재현했다 (`digest 계산`):
- **원자당 ΔE 를 그대로 지수에 넣으면**: w = exp(−ΔE[meV/atom]/k_BT) → w = {0.215, 0.419, 0.384, 0.345, 0.881, 1.000} → **가중평균 σ = 14.666 mS/cm** ✅ **논문의 14.67 과 정확히 일치.**
- **물리적으로 옳은 셀당(구성당) 가중이면**(같은 셀 52원자 → ΔE×52): **가중평균 σ = 0.065 mS/cm**.

⇒ **논문은 세기변수(per-atom)를 크기변수(per-configuration)처럼 Boltzmann 지수에 넣었다.** 지수가 **52배 축소**돼 있어, 실제로는 상온에서 사실상 무시돼야 할 고전도 무질서 배열들이 거의 같은 무게로 들어갔다. **225배 차이**다.
- ⇒ **"14.67 이 실험 ~5 mS/cm 와 잘 맞는다" 는 주장은 이 오류에 의존한다.** 올바른 가중이면 0.065 mS/cm 로 **실험보다 2자릿수 낮게** 나온다.
- ⚠ 다만 **올바른 답이 0.065 라는 뜻도 아니다.** 실제 argyrodite 는 (i) 배열이 셀 단위로 균질하지 않고 국소적으로 섞이며, (ii) 각 배열의 **다중도(configurational degeneracy)** 가 가중치에 들어가야 하고(논문은 이것도 빼먹었다), (iii) 합성 시 **동결된(quenched) 무질서**라 300 K 평형분포가 아니다. ⇒ **정확한 앙상블 평균은 이 논문 데이터로는 계산할 수 없다.**
- ⛔ **인용 금지 항목**: `14.67 mS/cm` 및 *"실험과 3배 이내"* 서술.

### 10.5 `Fig. 4a` — 배열별 Arrhenius (내가 본 것)

x = 1000/T 0.75–3.5, y = D (cm²/s) log 1e-9 … 1e-4. 6곡선, 라벨은 **`4a%`-`4c%`-mixing**.
- 측정점은 **4개 온도(700/900/1100/1300 K)**, 300 K 는 전부 **외삽**.
- 1300 K 에서는 여섯 배열이 **6×10⁻⁵ ~ 1×10⁻⁴ 로 거의 겹친다** — 즉 **고온에서는 무질서가 안 보인다.**
- 300 K 로 갈수록 부채꼴로 벌어져 **최대 ~2자릿수**(검정 100%-0% 가 최저, 자홍/연두 50%-50% 가 최고).
- 🔴 **여기가 이 그림의 진짜 메시지다**: 배열 간 차이는 **기울기(Ea)** 차이이고, **측정 구간(700–1300 K)에서는 거의 구분이 안 되는데 외삽 구간에서 2자릿수로 벌어진다.** ⇒ **σ₃₀₀K 의 2자릿수 스프레드는 대부분 외삽의 산물**이다. 우리 규율(600 K 이상 3점 아레니우스, 절대값 인용 금지)이 왜 필요한지 보여주는 좋은 예다.

### 10.6 `Fig. 4b` — cage 간 점프 빈도 (내가 본 것)

x = 음이온 자리 색인, 왼쪽 **S²⁻ 자리 0–15**, 오른쪽(연두 음영) **Cl⁻ 자리 0–15**. y = **Inter-cage jump freq. [freq/ps] 0–8**. 700 K.

| 배열 | S²⁻ 자리 `figure-read ≈` | Cl⁻ 자리 `figure-read ≈` |
|---|---|---|
| **100%-0%** (검정, σ 최저 0.05) | **0.1 – 0.2** (거의 0) | **7.7 – 7.9** (최고) |
| 0%-100% (파랑, σ 3.75) | 0.7 – 1.0 | 6.1 – 6.5 |
| 25%-75% (주황, σ 30.06) | 2.1 – 2.6 | 4.2 – 5.5 |
| 50%-50% (연두/자홍, σ 27–41) | 1.7–1.8 (자리 0–7) → 3.2–3.6 (자리 8–15) | 4.0 – 5.7 |
| 75%-25% (보라, σ 10.86) | 1.0–1.3 (0–11) → 4.5–4.7 (12–15) | 2.4–2.5 (0–3) → 6.8–6.9 (4–15) |

논문 결론: *"고무질서 배열이 S²⁻ 자리 주변 점프를 크게 늘린다 — 4a 자리에 S²⁻ 가 부분 치환되면서 국소 Li-cage 를 불안정화한다."* Minafra(ref 3)의 **전하 비균질 → Li 분포 확산 → 장벽 저하** 그림과 Jun(ref 62)의 cage 상관과 일관.

🔴 **그림 vs 본문 긴장 2건**:
1. 본문은 *"the overall conductivity is found to correlate with the frequency of intercage hopping events"* 라고 뭉뚱그리는데, **그림상 상관은 S²⁻ 자리에서만 성립하고 Cl⁻ 자리에서는 정확히 반대다** — σ 가 가장 낮은 100%-0% 배열이 **Cl 자리 점프 빈도는 최고**(7.8/ps)다. 즉 이 지표는 **"어느 자리에서 재느냐"에 부호가 달려 있고**, 논문은 그 조건을 명시하지 않는다.
2. 계단 구조(자리 8 또는 12 에서 값이 점프)는 캡션의 *"4c 다음 4a 순서"* 정렬 때문인데, **계단 위치가 배열마다 다르다**(50%-50% 는 8, 75%-25% 는 12) — 즉 x축이 배열마다 다른 의미를 갖는다. 캡션에 설명이 없다.

### 10.7 `Fig. S1` — MSD 수렴 (내가 본 것) ★ 우리 MSD 창 규약에 직결

대상 = **100%-0% 배열**(가장 느린 것). (a) 선형: MSD (Å²) vs lag τ (ps).
- 700 K: 370 ps 에 **≈22 Å²** · 900 K: **≈110** · 1100 K: **≈265** · 1300 K: 300 ps 에 **≈365**.
- 음영 = x,y,z 3성분에서 구한 SEM. **1100 K 의 음영이 가장 넓다**(±40 Å² 수준) — 등방 가정이 가장 안 맞는 구간.
- (b) log-log: 장시간에서 기울기 ≈1(정상확산) 확인. **★ 700 K 곡선은 τ ≈ 10–70 ps 에서 뚜렷한 평탄부(MSD ≈ 4–5 Å²)** 를 보이고 그 뒤에야 다시 오른다.

🔴 **우리에게 직결되는 사실**: 이 계·이 온도에서 **τ = 10–70 ps 는 "케이지 갇힘(caged) 구간"** 이다. 그래서 저자들이 **τ > 100 ps** 에서만 피팅한다. **우리 규약은 MSD 창 2–50 ps 고정**이다 — 우리 창은 여기 그림 기준으로 **평탄부 한가운데**다.
⚠ **다만 그대로 "우리가 틀렸다"로 넘어가면 안 된다.** 조건이 다르다:
- 이 그림은 **가장 느린 완전정렬 배열**이고, 우리 계(modelc = Cl-rich Li₅.₄PS₄.₄Cl₁.₆)는 **무질서·공공이 많은 빠른 쪽**이다. `Fig. 4a` 에서 50-50 배열은 700 K D 가 100-0 배열의 **~7배**라 평탄부가 훨씬 짧다.
- 우리 최저 온도는 **600 K** 로 더 낮다 ⇒ **우리 쪽이 더 위험하다**.
⇒ **판정: 이건 "확인해야 할 것"이지 "이미 틀린 것"이 아니다.** 우리 궤적으로 **log-log MSD 를 그려 2–50 ps 구간의 기울기가 1 인지** 보는 것이 유일한 답이다(§13-5).

### 10.8 기준값과 문헌 대조 (논문이 스스로 적은 것)
- **D₃₀₀K = 3.6×10⁻¹⁰ cm²/s** (완전정렬 배열) — *"기존 AIMD 연구(refs 54, 55)와 대체로 일관하나 **실험보다는 낮다**"*(refs 56, 57).
- 부분 Cl/S 혼합이면 **최대 2자릿수** 높은 σ 가능 (refs 3, 55).
- `Fig. 3c`: **300 ps / 700 K** 궤적의 Li 확률밀도 등가면 — PS₄ 사면체(연보라), S²⁻(노랑), Cl(초록) 주위로 **cage 형 호핑망**이 3차원으로 연결돼 있다. 정성적으로 문헌의 cage-hopping 그림 그대로.

---

## 11. ★6 — 거짓 음성(false negative) 검증을 했나

### ⇒ **답: 안 했다. 그리고 이 논문의 설계상 할 수도 없었다.**

- 탈락시킨 모델(ORB v2, EqV2)로 **σ·D·Ea 를 계산해 SevenNet/AIMD 와 비교한 적이 없다.** 전도도 계산은 **SevenNet 단독**이다.
- 즉 *"드리프트가 실제로 D 를 얼마나 부풀리는가"* 는 **측정되지 않았고 추론으로만 서술된다** (*"can distort the underlying PES … leading to artificially enhanced diffusion as shown in the following subsection"* — 그런데 following subsection 에는 ORB/EqV2 의 D 가 없다. **본문이 없는 결과를 가리킨다**).
- **MACE 는 정적 지표에서 최하위였는데 동역학 시험을 아예 받지 않았다** ⇒ MACE 에 대해서는 거짓 음성 가능성이 그대로 열려 있다. MACE 는 보존적이므로 이 논문의 논거대로면 **MD 에서는 괜찮았을 수도 있다.**
- 역방향(거짓 양성)도 미검증: **SevenNet 이 AIMD 와 같은 D 를 주는지**를 확인한 적이 없다. `Fig. 3a` 의 E(T) 비교가 전부고, **AIMD 로 D 를 뽑아 대조하지 않았다**(10 ps AIMD 로는 D 를 못 뽑는 것이 이유겠지만, 그렇다면 그 한계를 적었어야 한다).

---

## 12. ★8 — SI 에만 있는 것 (본문에 없음)

| # | 항목 | 내용 | 왜 중요한가 |
|---|---|---|---|
| S-1 | **데이터셋 구성 절차 전문** (SI §1, `Fig. S4`) | Li 48h 50% 점유 선택 규칙(Li–Li 거리 최대화), 음이온 전수열거(S/X 102 + Cl/Br 74), 살아남은 18/16/12 | **재현의 유일한 근거.** 본문엔 "compact yet representative" 한 줄뿐 |
| S-2 | 🔴 **ORB v2·MACE 사전선별 자백** (SI §2 끝) | *"the resulting set of configurations might be slightly more favorable to ORB v2"* | **본문에 이 문장이 없다.** 1등 결과의 해석을 바꾸는 정보가 SI 에만 있다 |
| S-3 | 🔴 **누락 배열 사고와 데이터셋 확장** (SI §3) | S/Cl/Br 4a/4c 정렬 배열이 *"inadvertently excluded"* → **129 → 253** 재분석 | 본문 `Table 1` 이 **불완전한 집합** 위에서 계산됐다는 뜻 |
| S-4 | **확장 벤치마크 `Table S4`/`Table S5`** | 아래 12.1 | **순위가 바뀐다** |
| S-5 | **추론 효율 `Table S2`** | ORB v2 가 SevenNet 의 4.0배 속도 | 실무 선택의 진짜 대가 |
| S-6 | **구조유형별 분해 `Table S1`** | §7.3 | 논문의 결론을 실제로 떠받치는 표 |
| S-7 | **MSD 수렴 진단 `Fig. S1`** | §10.7 | 우리 MSD 창 규약에 직결 |
| S-8 | **드리프트 시계열 `Fig. S3`** | §9.3 | 본문 `Fig. 3a` 는 평균만 보여준다 |
| S-9 | **원소기준 형성에너지 `Fig. S2`** | §12.2 | MACE 의 실패가 여기서 가장 극적 |

### 12.1 확장 데이터셋 결과 (`Table S4` = 253 argyrodite + 29 비-argyrodite = **282**)

| 지표 | EqV2 | DeePMD | ORB v2 | SevenNet | MACE |
|---|---|---|---|---|---|
| MAE [meV/atom] | 6.664 | 6.965 | 5.907 | **5.763** | 12.752 |
| RMSE | 8.010 | 8.139 | **6.836** | 9.497 | 15.233 |
| R² | 0.976 | 0.975 | **0.982** | 0.966 | 0.912 |
| Spearman | 0.944 | 0.949 | **0.963** | 0.954 | **0.963** |
| Pearson | 0.989 | 0.989 | **0.993** | 0.989 | 0.986 |
| slope | 0.949 | 0.945 | **0.984** | 0.917 | 0.923 |

`Table S5` (구조유형별, argyrodite 253개분): EqV2 **6.787** · DeePMD **7.114** · ORB v2 **6.332** · **SevenNet 5.249** · MACE **13.001**.
(✅ 가중평균 검산 — SevenNet (29×10.247 + 253×5.249)/282 = **5.763** ✓ 등 다섯 모델 전부 `Table S4` 재현.)

🔴 **SI 본문의 사실오류**: SI §4 는 *"Despite the **slight reduction** in the overall MAE of SevenNet upon the inclusion of the additional configurations…"* 라고 쓴다. **틀렸다 — MAE 는 늘었다.** 전체 4.916 → **5.763**(+17%), argyrodite 만 보면 3.717 → **5.249**(+41%).
그리고 **순위도 바뀐다**: 확장셋에서 SevenNet 과 ORB v2 의 전체 MAE 는 **5.763 vs 5.907 로 사실상 동률**(2.4% 차)이고, RMSE 는 **ORB v2 가 이긴다**(6.836 vs 9.497). ⇒ **본문 `Table 1` 이 준 "SevenNet 이 argyrodite 에서 압도" 그림은 확장셋에서 상당히 옅어진다.** 저자들은 *"relative performance ranking remains consistent"* 라고만 쓰고 넘어간다.
✅ SI 가 옳게 적은 것 하나: SevenNet 의 Spearman 이 **0.899 → 0.938** 로 개선 — 표본이 적을 때 순위상관이 과민했던 것.

### 12.2 `Fig. S2` — 원소기준 형성에너지 (내가 본 것)
- (a) 패리티: x, y **−2.75 … 0 eV/atom**. EqV2·DeePMD·ORB v2·SevenNet 네 회귀선은 **패리티와 육안 구분 불가**. **MACE(보라)만 명확히 위로 벗어나고**(과소안정), x ≈ −0.4 부근에 **+0.2 ~ +0.3 eV/atom** 짜리 이상점이 여러 개.
- (b) box: EqV2·DeePMD·ORB v2·SevenNet 상자가 **±0.01–0.02 eV/atom 안**에 납작하게 붙어 있고, **MACE 만 −0.015 ~ +0.065(수염 −0.035 ~ +0.178)** 로 압도적으로 넓다.
⇒ **원소기준 축에서는 MACE 만 탈락, 나머지 넷은 구분 불가.** 즉 이 논문에서 **모델을 가르는 정보는 "compound formation energy + 동역학" 에만 있다.**

---

## 13. §7 — 우리 baseline 과의 대조

기준: `litdb/our_dft_baseline.md` · `db/properties/mlip_bench_li3ps4_uma.json` · `tools/ionic/mlip_committee.py` · `litdb/comparison_vs_ours.md` §J.

### 13.1 방법 축 — 같은 것 / 다른 것

| 축 | **Chang 2026** | **우리** | 판정 |
|---|---|---|---|
| **엔진** | SevenNet-l3i5 (1.17 M, cutoff 5 Å, MPtrj) 채택 | **UMA-s-1p1 (omat)** | ⚠ 다르다. **UMA 는 이 논문의 피고에 없다** |
| **힘 형식** | 이 논문의 **핵심 판정축**. 보존 ✅ vs 비보존 ⛔ | **UMA-S = 보존적**(`uma2026…` §Table 1·4·16, NVE ✓) + 우리 유한차분 프로브 독립 확인(0.198% @ δ=0.005) | ⭕⭕ **우리가 "합격" 쪽에 있다** — §13.4 |
| **사전학습 코퍼스** | 전 모델 **MPtrj**(ORB v2 만 +Alexandria) | **OMat24** | ⚠ 다르다. OMat24 세대는 MPtrj 세대의 softening 을 개선한 것으로 측정돼 있다(`db/external/omat24/README.md`) ⇒ **이 논문의 softening 논거를 UMA 에 그대로 이식할 수 없다** |
| **참조 범함수** | **PBE** (VASP, 520 eV, MP 설정) | 우리 DFT 정본 = **PBE**(QE/USPP, 60/480 Ry) / 우리 MLIP 벤치 라벨 = **PBEsol**(PET-MAD) | 🟡 **DFT 축은 같은 PBE 계열**이라 정성 비교 가능. **MLIP 벤치 축은 PBEsol 이라 수치 비교 불가** |
| **무질서 처리** | 음이온 **전수열거**(대칭유일) + Li 48h **50% 단일배열**(거리최대화) | comp1/modelc **단일 배열** | ⚠ 우리가 더 얕다. 다만 이 논문도 **Li 부격자는 단일배열**이다 |
| **MD 온도** | 700 / 900 / 1100 / 1300 K | **600 / 800 / 1000 K** (400/500 K 제외 판정) | 🟡 우리가 더 낮고, 그래서 caging 위험이 더 크다 |
| **생산 길이** | **300–450 ps** | **200 ps** (평형 5 ps) | 🟡 그쪽이 길다 |
| **MSD 창** | *"τ > 100 ps"* | **2–50 ps 고정** | 🔴 **정면 충돌** — §13.5 |
| **σ 산출** | pymatgen NE, **Haven=1**(우리 역산 확인) | NE, **Haven=1** | ⭕ 동일 |
| **시드** | **1** | modelc 600 K **3-시드**(Ea 0.197±0.032) | ⭕ **우리가 낫다** |
| **오차막대** | MSD 의 x,y,z 3성분 SEM | 3-시드 | ⭕ **우리 쪽이 통계적으로 방어 가능** (그쪽은 독립표본이 아니다) |
| **committee** | ⛔ 없음 (모델 비교는 하지만 UQ 아님) | M=3 이종 committee | — |

### 13.2 값 축 — **비교 가능한 것이 거의 없다**

| 물성 | Chang 2026 | 우리 | 비교 가능? |
|---|---|---|---|
| **Ea** | 0.197 – 0.406 eV (배열별, ⚠ 표에는 meV 로 오기) · `Fig. 3b` 0.41±0.02 eV | comp1 **0.253** / modelc **0.224**(3-시드 0.197±0.032) eV | 🟡 **자릿수·범위가 겹친다.** 단 엔진(SevenNet vs UMA)·조성(LPSC vs Cl-rich)·온도창이 달라 **"같은 범위" 까지만** |
| **D₃₀₀K** | 3.6×10⁻¹⁰ ~ 2.7×10⁻⁷ cm²/s (외삽) | D(600 K) comp1 3.09×10⁻⁶ / modelc 7.90×10⁻⁶ | ⛔ **온도가 달라 직접 비교 불가** |
| **σ₃₀₀K** | 0.05 – 41.02 mS/cm (배열별) · 앙상블 14.67 ⛔ | 우리는 **σ 절대값 인용 금지 규율** | ⛔ 비교하지 않는다 |
| **형성에너지 오차** | MLIP vs PBE, **4.7–12.8 meV/atom** | 우리 UMA 에너지 MAE **13.45 meV/atom**(PBEsol 라벨, 선형 원소보정 후) | ⛔ **범함수·기준상태·평가집합 전부 다르다.** 같은 표 금지 |
| **힘 오차** | ⛔ **보고 안 함** | UMA 힘 **MAE 30.0 / RMSE 44.6 meV/Å** | ⛔ 대응물 없음 |
| **4a/4c ΔE** (DFT) | 0 / 3.28 / 22.48 / 24.73 / 27.52 / **39.72** meV/atom | ⛔ **우리는 안 쟀다** | 🔴 **우리가 재야 할 것** |
| Ehull (Cl/Br argyrodite) | 전부 **50 meV/atom 이내 metastable**, Br-rich 가 hull 에 더 가까움 | ⛔ 없음 | 🟡 참고 |

### 13.3 ⛔ 방법 의존성 경고 (실제 차이 vs 방법 산물)

- **Ea 0.41 eV(그들, 완전정렬) vs 0.224 eV(우리 modelc)** 를 "Cl-rich 가 낫다"의 증거로 쓰면 안 된다. **엔진·온도창·조성·무질서 배열이 전부 다르다.** 이 논문 자신의 `Table 3` 안에서도 배열만 바꿔 **0.197 ↔ 0.406 eV** 로 2배 갈린다 ⇒ **배열 선택이 조성 효과보다 크다.**
- **σ 절대값**은 이 논문이 스스로 *"PBE 학습 → 격자 과대 → σ 과대"* 를 인정하고, r2SCAN 학습 시 **~9배** 낮아진 사례(ref 53 vs 52)를 제시한다 ⇒ **σ 절대값은 학습 범함수의 함수**다. 우리 금지 규율과 일치.
- **band gap · ESW · 탄성 · 포논 · NEB**: 이 논문은 **하나도 다루지 않는다.** 전문 문자열 검색(본문 12 pp + SI 16 pp): `band gap`/`bandgap` **0회** · `elastic` **0회** · `phonon` **0회** · `Bader` **0회** · `charge density` **0회** · `electrochemical` 2회는 **전부 참고문헌 제목** · `NEB` 1회는 **`nebDFT2k` 데이터셋 이름**. ⇒ **물성 4축(A/B/C/D) 표에 넣을 값이 없다.** `comparison_vs_ours.md` 의 **`🔧 방법 원전` 블록에만** 들어간다.

### 13.4 ★★★ **§ 우리 UMA 선택에 주는 것** — 판정 초안

> **질문: 우리가 UMA 를 쓰는 것을 이 논문으로 방어할 수 있는가?**

**판정: 🟡 부분적으로만. 이 논문은 "UMA 를 쓰라"고 말해주지 않지만, "우리가 고른 종류의 모델을 쓰라"고는 말해준다.**

**✅ 방어에 쓸 수 있는 것 (3개)**
1. **"보존적 모델을 써라" 가 이 논문의 1차 판정축이고, UMA-s-1p1 은 보존적이다.**
   - 이 논문: 비보존(ORB v2 · EqV2) → 1100 K 10 ps 에 **+0.4–0.6 eV/atom 드리프트**, 결론에서 *"conservative models … are more accurate for assessing dynamic properties"*.
   - 우리: `uma2026_family_of_universal_models_for_atoms` §Table 1/4/16 — **UMA-S 는 conservative, NVE 에너지 보존 ✓** (비보존은 UMA-L 뿐, 우리는 안 쓴다). + 우리 자체 **유한차분 프로브**로 이중 확인.
   - ⇒ **"우리는 이 논문이 탈락시킨 범주에 속하지 않는다"** 는 **정당한 방어**다. **argyrodite 에서 직접 측정된** 근거라는 점이 값지다.
2. **"리더보드 순위 ≠ 응용 적합성" 이라는 논거가 우리를 돕는다.** UMA 가 Matbench Discovery 상위라는 것은 우리 선택의 근거가 될 수 없다 — 이 논문이 그 추론을 금지한다. 대신 **우리 J-1 실측(Li₃PS₄ 힘 MAE 30.0 meV/Å, 미학습 test set)** 이 이 논문이 요구하는 *"focused validation study"* 의 우리 판본이다.
3. **σ 절대값 금지 규율의 외부 재확인.** 학습 범함수(PBE vs r2SCAN)가 σ 를 ~9배 가른다는 이 논문의 인용은 우리 `mlip_committee.py` 규율과 **독립적으로 같은 결론**이다.

**⛔ 방어에 쓸 수 없는 것 (4개)**
1. **UMA 를 시험하지 않았다.** *"Chang 2026 이 UMA 를 검증했다"* 는 **거짓 진술**이다. 가장 가까운 `eqV2 S DeNS` 도 **MPtrj 학습 + direct force** 라 우리 모델이 아니다.
2. **argyrodite 에서 UMA 의 형성에너지 오차·4a/4c 순위·에너지 드리프트는 여전히 미측정**이다. 우리가 가진 것은 **Cl 없는 Li₃PS₄ 힘 오차** 하나뿐이다(J-1 이 이미 *"Cl 이 없다"* 를 한계로 적어 놓았다).
3. **이 논문의 승자는 SevenNet 이지 UMA 가 아니다.** 누가 *"그럼 SevenNet 으로 바꿔야 하는 것 아니냐"* 고 물으면, 우리의 답은 **"이 논문의 SevenNet 은 MPtrj 학습본이고, OMat24 세대가 MPtrj 세대의 알려진 결함을 고친 것"** 이어야 하는데, **그 비교(SevenNet-MPtrj vs UMA-OMat24)를 한 논문은 아직 없다.**
4. **σ·D 절대값은 어느 쪽도 방어하지 않는다.**

> **⇒ 무엇을 재야 하는가 (우선순위)**

| # | 재야 할 것 | 왜 | 비용 | DFT 필요? |
|---|---|---|---|---|
| **A1** | **UMA 로 `Table 3` 6배열의 ΔE 를 재현** — DFT 값(0 / 3.28 / 22.48 / 24.73 / 27.52 / 39.72 meV/atom)이 이미 있다 | **★ 가장 값싸고 결정적.** *"UMA 가 4a/4c 자리선호를 맞추는가"* 에 즉답. Cl 이 들어간 우리 계 | **매우 낮음** — UMA relax 6회 | ⛔ **0회** (논문 DFT 를 정답으로 씀) |
| **A2** | **UMA NVT 10 ps, 1100 K, Li₆PS₅Cl 52원자 총에너지 드리프트** | `Fig. S3` 와 **직접 겹치는 시험**. 보존성 주장을 이 계에서 확인 | 낮음 | ⛔ 0회 |
| **A3** | **우리 궤적의 log-log MSD** (comp1·modelc, 600/800/1000 K) — 2–50 ps 구간 기울기가 1인지 | `Fig. S1` 이 제기한 유일한 실질 위협. **기존 궤적 재분석이면 새 MD 불필요** | 매우 낮음 | ⛔ 0회 |
| A4 | UMA 로 Cl/Br 조성격자(`Fig. 2`) 재현 | 상안정성 축 대조 | 중간 | 0회 |
| A5 | `Table 3` 6배열의 **UMA-MD σ 비율** (절대값 아님) | 무질서 민감도 비교 | 높음 (6배열×4온도) | 0회 |

**⚠ A1–A3 는 전부 DFT 0회이고 기존 도구로 된다.** A1 은 **`tools/mlip/bench_against_dft.py` 를 확장**하는 것이 새 파일보다 낫다(코드 규율). **단, 새 물리량을 정의하는 A5 는 `kb/templates/estimand_card.md` 를 먼저 채운다.**

### 13.5 🔴 MSD 창 규약 — 이 논문이 우리에게 던진 유일한 실질 위협

| | Chang 2026 | 우리 규약 |
|---|---|---|
| 피팅 창 | **τ > 100 ps** | **2–50 ps 고정** |
| 근거 | `Fig. S1b` log-log 에서 **700 K, 100%-0% 배열이 τ ≈ 10–70 ps 에 평탄부** | 여러 파일에 복사된 물리 규약 (`tools/convention_check.py` 로 관리) |
| 최저 온도 | 700 K | **600 K** |
| 계 | 완전정렬 LPSC (가장 느림) | comp1(정렬) · **modelc(Cl-rich, 빠름)** |

⇒ **결론: 규약을 지금 바꾸지 않는다. 대신 A3 로 검증한다.**
- 이 논문의 평탄부는 **가장 느린 배열·700 K** 라는 최악 조건에서 관측됐고, 우리 modelc 는 그보다 빠르다.
- 그러나 **우리 최저 온도가 600 K 로 더 낮다** ⇒ 위험이 상쇄되지 않는다.
- **comp1(정렬 LPSC) 600 K 가 가장 위험한 조합**이다. 여기서 2–50 ps 기울기가 1 이 아니면 **comp1 의 D(600 K)=3.09×10⁻⁶ 와 Ea=0.253 eV 가 흔들린다.**
- ⛔ 규약 변경은 `tools/convention_check.py` 가 관리하는 다중 파일 규약이므로, **A3 결과 없이 손대지 않는다.**

---

## 14. ★3 의 descriptor — **우리 계에서 계산하는 절차 초안**

⚠ 먼저: **이 논문에는 이름 붙은 descriptor 가 없다.** 아래는 §8.2 의 *"cage 간 Li 점프 빈도"* 를 우리가 재현 가능하게 재구성한 것이고, **미기재 파라미터(cutoff)를 우리가 정해야 한다**는 점을 명시한다.

**정의 (우리 판본)**
```
입력  : MLIP-MD 궤적 (NVT), 20 fs 마다 프레임
자리   : 4a·4c Wyckoff 자리를 점유한 모든 음이온 (S²⁻ 또는 Cl⁻/Br⁻/O²⁻)
        ⇒ 우리 modelc(Li5.4PS4.4Cl1.6)는 4a+4c 에 S 와 Cl 이 섞여 있다
단계 1 : 각 프레임 t, 각 자리 i 에 대해 n_i(t) = |{ Li : |r_Li − r_i| < R_c }|
        🔴 R_c 가 논문에 없다. 우리는 **Li–S / Li–Cl 동경분포함수(RDF)의 제1 최소**로 정한다
          (계·온도마다 따로 정하고 그 값을 기록한다 — 자의적 상수 금지)
단계 2 : f_i = ( Σ_t [ n_i(t) ≠ n_i(t−Δ) ] ) / T_total     [jump/ps],  Δ = 20 fs
단계 3 : 보고는 **자리별 산점도**로 — 음이온 종(S/Cl) × Wyckoff(4a/4c) 로 층화
        ⛔ 하나의 스칼라로 평균내지 않는다 (§10.6: 부호가 자리별로 뒤집힌다)
```

**우리 구현 경로 (코드 규율 — 새 파일 전에 기존 것 확장)**
1. 궤적 I/O·MSD·자리할당은 이미 `tools/ionic/` 에 있다 ⇒ **거기에 `--intercage-jumps` 플래그를 붙인다.**
2. `R_c` 는 **입력이 아니라 궤적에서 유도**하고(RDF 제1 최소), 유도 실패 시 **시작하지 않는다** (`run_force_check_scf.sh` 선례).
3. `--selftest` 에 **음성경로**를 넣는다: 완전 정지(frozen) 궤적 → f = 0 이 나와야 하고, 무작위 좌표 → f 가 포화해야 한다.
4. ⛔ **이건 새 물리량이다** ⇒ 계산 전에 **`kb/templates/estimand_card.md`(보고량 카드) §1–3 을 채운다.** 특히 *"admissible state 가 여럿인가"* — **R_c 선택이 곧 상태선택 규칙**이라 여기서 걸린다.

**⚠ 더 나은 대안이 이미 우리 litdb 에 있다**: `jun2022_argyrodite_ion_cage_size_descriptor`(= 이 논문의 ref 62) 의 **ion-cage 크기 균일도** descriptor 는 **정적 구조만으로** 계산되고 정의가 완결돼 있다. **MD 궤적이 필요 없다.** 자리선호 스크리닝 목적이면 **그쪽이 먼저**다.

---

## 15. ★7 — 우리가 그대로 쓸 수 있는 것 / 못 쓰는 것

### 15.1 코드·데이터 공개 여부
| 항목 | 상태 |
|---|---|
| **저자 코드** | ⛔ **없다.** Data Availability 절 자체가 없다. GitHub·Zenodo·저장소 링크 **0건** |
| **벤치마크 구조/DFT 라벨 (129 또는 253개)** | ⛔ **공개 안 함** |
| **MD 궤적** | ⛔ 공개 안 함 |
| **라이선스** | ACS 표준 저작권 (OA 아님). SI 는 무료 열람 |
| **쓰인 도구** | 전부 공개 오픈소스: **VASP**(상용) · **ASE** · **FrechetCellFilter** · **FIRE** · **pymatgen** · 각 MLIP 공개 체크포인트 |
| ⇒ | **논문의 수치는 재현 불가, 절차는 재현 가능.** `Table 3` 의 DFT ΔE 6개는 **표에 인쇄돼 있으니 우리가 정답으로 쓸 수 있다**(§13.4 A1) |

### 15.2 그대로 가져올 수 있는 것
1. ✅ **"보존/비보존" 을 1차 선별축으로 삼는 것** — argyrodite 에서 직접 측정된 근거.
2. ✅ **"거친 프로토타입에서 이완시켜 채점" 하는 평가설계** — 이완된 MP 구조로 채점하면 리더보드를 재현할 뿐이다.
3. ✅ **10 ps NVT 총에너지 드리프트 시험** — 싸고, DFT 0회, 우리 A2.
4. ✅ **log-log MSD 로 확산영역을 먼저 확인하고 피팅창을 정하는 절차** — 우리 A3.
5. ✅ **`Table 3` 의 DFT ΔE 6값** (4a/4c 자리선호의 외부 정답).
6. ✅ **자기정합 참조**(전구체 에너지를 각 MLIP 이 자기 PES 로 재계산) — 우리 `bench_against_dft.py` 의 선형 원소보정과 목적이 같은 다른 해법.

### 15.3 ⛔ 가져오면 안 되는 것
1. ⛔ **`14.67 mS/cm` 앙상블 평균** 및 *"실험 ~5 mS/cm 와 3배 이내"* 서술 — **가중치 오류**(§10.4).
2. ⛔ **`Table 3` 의 Ea 를 meV 로** — **eV 다**(§10.2).
3. ⛔ **σ·D 절대값 전부** — PBE 학습 편향 + 400 K 외삽 + 단일시드.
4. ⛔ *"모든 MLIP 이 10 meV/atom 안에 든다"* 를 **UMA 로 확장** — UMA 는 시험되지 않았다.
5. ⛔ *"MACE 는 argyrodite 에 부적합"* — **MACE 는 동역학 시험을 안 받았다**(§11).
6. ⛔ **`Fig. 1a`/`Fig. S2a` 의 표본수 209/206** — 실제 158(`Table 1`), 확장판 282(`Table S4`)(§12.1).
7. ⛔ **`Fig. 3a` 의 절대 세로 오프셋을 모델 오차로** — 참조보정이 없다(§9.2).

---

## 16. §10 — 비판 (우리 지적)

### 16-1. 🔴🔴 **부호 서술이 세 번 뒤집힌다** (그림 vs 본문)
`Fig. 1c` 는 명확하다: **EqV2·DeePMD·ORB v2 = 양의 편향**(형성에너지 과대 = 안정성 과소), **SevenNet(−2)·MACE(−9.5) = 음의 편향**. 그런데 본문은:
- p.3137 ✅ *"EqV2, DeePMD, and ORB v2 … showed a consistent positive bias, tending to overestimate formation energies"* — **그림과 일치**.
- p.3137 ⛔ *"ORB v2 tends to systematically overestimate formation energies … **Its underestimation** leads to overpredicted Ehull values"* — **한 문단 안에서 자기모순**.
- p.3137 ⛔ *"although SevenNet **slightly overestimates** absolute formation energies"* — **그림과 반대**(SevenNet 은 과소).
- p.3138 ⛔ *"ORB v2 exhibits an MAE of 5.3 … along with a tendency to **underestimate** compound formation energies"* — **그림과 반대**.
⇒ 결론(SevenNet 이 Ehull 을 더 잘 맞힌다)은 `Fig. 2d–f` 로 살아남지만, **부호 서술을 인용하면 안 된다.**

### 16-2. 🔴 **표본수가 세 곳에서 다르다**
`Table 1` 캡션 **129 + 29 = 158** vs `Fig. 1a` 캡션 **209** vs `Fig. S2` 캡션 **206 (126 + 80)**. 내가 `Table S1` 가중평균으로 **`Table 1` 의 N = 158 임을 다섯 모델 전부 재현**해 확인했다 ⇒ **209 와 206 중 최소 하나는 오기**다. 게다가 `Fig. S2` 는 argyrodite 를 **126** 이라 하는데 다른 곳은 전부 129/253 이다.

### 16-3. 🔴 **동역학 시험에서 MACE 가 빠졌다** — 논증의 구멍
논문의 결론은 *"보존 > 비보존"* 인데, MD 를 돌린 보존모델은 **SevenNet·DPA3 둘뿐**이다. **MACE 도 보존적**이고 정적 지표는 최하위였다. MACE 를 넣어 "보존적인데도 나쁘다"가 나왔으면 논증이 무너지고, "보존적이라 괜찮다"가 나왔으면 논증이 강해졌을 것이다. **어느 쪽인지 모른 채 결론이 났다.** `Table S2` 에 MACE 행이 없는 것이 그 흔적.

### 16-4. 🔴 **평가집합을 피고 두 명이 골랐다** (§5.3) — SI 만 자백
그리고 SI §3 은 *"S/Cl/Br 배열들이 inadvertently excluded 됐다"* 고 인정한다. 즉 **본문 `Table 1` 은 (a) 경쟁자가 고른 (b) 불완전한** 집합 위의 결과다.

### 16-5. 🔴 **Boltzmann 가중이 per-atom** (§10.4) — 재현으로 확정 (14.666 vs 논문 14.67)
게다가 **배열 다중도(degeneracy)** 가 가중치에 안 들어갔고, **quenched vs annealed 무질서** 구분도 없다.

### 16-6. 🔴 **`Table 3` Ea 단위 오기** (§10.2) — `Fig. 3b` 가 부정한다.

### 16-7. 🔴 **SI §4 의 "slight reduction in MAE" 는 사실과 반대** (§12.1) — 실제로는 argyrodite MAE 가 **3.717 → 5.249 (+41%)**.

### 16-8. 🔴 **통계적 뒷받침이 얇다**
- MD **시드 1개**, 오차막대는 **x,y,z 3성분 SEM** — 이건 **독립표본이 아니다.** 등방계에서 3성분은 같은 궤적의 세 투영이라 상관돼 있다. `mccluskey2025_accurate_diffusion_coefficients_uncertainties`·`pranami2015_estimating_error_diffusion_coefficients_md`·`maginn2019_best_practices_transport_selfdiffusivity_viscosity` 가 전부 이 방식이 불확도를 **크게 과소평가**한다고 적는다.
- `Fig. 3b` 의 **Ea = 0.41 ± 0.02 eV** 는 **4점 선형회귀의 표준오차**일 뿐 시드 변동을 포함하지 않는다.
- **700 K 최저점에서 300 K 로 400 K 외삽**한다. `Fig. 4a` 는 배열 간 차이가 **측정구간에서 거의 안 보이고 외삽구간에서만 2자릿수**로 벌어지는 것을 보여준다.

### 16-9. 🟠 **AIMD 설정이 통째로 없다** (§4) — 이 논문의 **유일한 ground truth 동역학 기준**인데 cutoff·k-점·dt·thermostat 이 하나도 없다.

### 16-10. 🟠 **`Fig. S3` 에서 SevenNet·DeePMD 곡선에 열요동이 없다** (§9.3) — 같은 NVT 인데 AIMD 만 요동한다. 처리 차이를 의심할 근거이고, 논문은 설명하지 않는다.

### 16-11. 🟠 **"depth" 주장이 그림과 안 맞는다** (§7.5) — SevenNet 은 DFT 보다 **더 깊다**.

### 16-12. 🟠 **cage 점프 빈도의 cutoff 미기재** (§8.2) + 본문의 상관 주장이 **Cl 자리에서 반대**(§10.6).

### 16-13. 🟡 **셀 크기 서술 혼동** — 전도도 계산은 *"a 1×2×2 supercell of the conventional cell (containing four formula units)"* 인데, `Fig. 4b` 의 자리 개수(S 16 + Cl 16)는 **16 f.u.** 를 뜻한다. "four formula units" 는 슈퍼셀이 아니라 **conventional cell** 을 수식하는 것으로 읽어야 앞뒤가 맞는다. 문장이 모호하다.

### 16-14. 🟡 **`Table 2` 오타 다수** — `viroal`/`vivoral`(virial), `OBR v2`, `BGFS`(BFGS), `Li6P5Cl`(Table 3 제목), `s0.938`(Table S5), *"energy conversion"*(conservation), *"Further systematic and analysis"*. 편집 품질이 낮다.

### 16-15. ✅ **공정하게 인정할 것**
- **as-is, no fine-tuning** 이라는 전제를 처음부터 명시하고 지켰다.
- **자기정합 참조**(각 MLIP 이 자기 전구체를 재계산)는 올바른 설계다.
- **초기구조를 전 모델·AIMD 가 공유**하도록 통제한 것은 좋은 실험설계다.
- **자기 데이터셋의 편향(ORB v2 유리)을 SI 에서 스스로 밝혔다.**
- **결론이 자기에게 불편한 방향**이다 — 가장 빠르고(4배) 정적 정확도 1등인 모델을 버리고 느린 쪽을 골랐다.

---

## 17. 기법 미니 용어집

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **conservative / non-conservative force** | 힘을 **F = −∇E** (autograd) 로 얻으면 보존적. 별도 출력층이 직접 예측하면 비보존 | **이 논문의 판정축.** 비보존은 닫힌 궤적에서 일을 하므로 NVT/NVE 에서 에너지가 표류 |
| **MPtrj** | Materials Project 이완 궤적 데이터셋(~158만 구조, VASP/PBE) | 5모델 전부의 사전학습 코퍼스 |
| **Matbench Discovery** | MLIP 를 **미지 결정의 안정성 예측**으로 줄세우는 리더보드 | *"이 순위가 우리 응용 순위와 다르다"* 가 논문의 헤드라인 |
| **compound formation energy** | 원소가 아니라 **실제 합성 전구체**(Li₂S, P₂S₅, LiCl, LiBr) 기준 형성에너지 | 음수 = 합성경로가 열역학적으로 유리 |
| **E_hull (energy above hull)** | convex hull 로부터의 거리. 0 = 절대안정, >0 = 준안정 | 전 argyrodite 가 **50 meV/atom 이내 준안정** |
| **PES softening** | 학습셋이 평형 근처에 치우쳐 PES 곡률이 물러지는 현상 (Deng ref 42) | 계통적 안정성 과소평가의 원인으로 지목 |
| **FrechetCellFilter** | ASE 에서 **격자 + 이온위치를 동시에** 최적화하게 해주는 필터 | DFT 의 전이완을 흉내내려고 사용 |
| **FIRE / BFGS** | ASE 구조 최적화 알고리즘 | 사전선별에서 둘 다 사용(`_F`/`_B`) |
| **DeNS (Denoising Non-Equilibrium Structures)** | 비평형 구조에 잡음을 넣고 되돌리도록 학습하는 보조과제 | `eqV2 S DeNS` 의 이름이 여기서 옴 |
| **E(3) 등변성** | 회전·병진·반사에 대해 출력이 올바르게 변환되는 성질 | NequIP/SevenNet 이 전 층에서 강제 |
| **intercage hopping** | 서로 다른 음이온 중심 Li-cage 사이의 이동 | 이 논문의 유일한 정량 무질서-수송 연결고리 |
| **Haven 비 (H_R)** | 추적자 확산 ↔ 전하 확산의 비. NE 식에서 H_R=1 가정이 흔하다 | 명시 없으나 **우리 역산으로 H_R = 1 확인** |

---

## 18. Figure set

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a | 5모델 × DFT 화합물 형성에너지 패리티 (x,y = −0.16…+0.18 eV/atom, 점선 = y=x). 데이터가 이봉이고 MACE 만 양의 끝에서 패리티 아래 | ⚠ **모델 구분에는 못 쓴다** — 데이터 폭 130 meV/atom vs MAE 차 5 meV/atom. 캡션의 표본수 "209" 는 오기(실제 158) |
| 1b | Ehull 편차 box plot (−20…+11 meV/atom). 중앙값 `figure-read ≈` EqV2 +0.3 / DeePMD −0.5 / ORB v2 +0.2 / **SevenNet −2.5** / **MACE −5** | ORB v2·EqV2 가 **Ehull 을 과대평가** ⇒ 준안정상 오분류 위험 |
| 1c | 화합물 형성에너지 편차 box plot. 중앙값 `figure-read ≈` EqV2 +5.2 / DeePMD +6.2 / ORB v2 +4.2 / **SevenNet −2.0** / **MACE −9.5** | **본문 부호 서술 3곳을 부정하는 그림**(§16-1). SevenNet 이 0 에 가장 가깝지만 **음의 편향** |
| 2a–c | Cl(0–8) × Br(0–8) 격자 위 화합물 형성에너지 등고선. (a) DFT (b) ORB v2 (c) SevenNet. 컬러바 −0.070…−0.025 eV/atom | (b) 는 **평평하고 위로**, (c) 는 **DFT 보다 깊다** ⇒ *"SevenNet 이 depth 까지 맞춘다"* 는 본문 주장은 **그림이 지지하지 않는다** |
| 2d–f | 같은 격자의 Ehull (0.000…0.048 eV/atom) | ⭕ **여기서는 SevenNet 이 확실히 DFT 범위와 겹친다**(0.010–0.028 vs ORB v2 0.030–0.040). Br-rich 좌상단이 hull 에 가장 가깝다 |
| 3a | 10 ps NVT 평균 총에너지 vs T (500/700/1100 K, 3점). AIMD 대비 EqV2·Orb 가 1100 K 에서 급등 + 거대 오차막대 | **드리프트 판정의 요약도.** ⚠ **절대 오프셋은 참조보정이 없어 해석 불가, 기울기만 유효** — AIMD 1.50e-4 vs SevenNet 3.22e-4 eV/atom/K (**2.1배**, digest 계산) |
| 3b | SevenNet-MD Arrhenius (1000/T 0.75–3.5, D 1e-9…1e-4). 4점(1300/1100/900/700 K) + 300 K 외삽 별. **인쇄값 Ea = 0.41 ± 0.02 eV** | 🔴 **`Table 3` 의 "Ea [meV]" 단위 오기를 확정하는 증거.** 400 K 외삽 폭 주의 |
| 3c | 700 K 300 ps Li 확률밀도 등가면 (PS₄ 사면체·S²⁻·Cl 표시) | cage 형 3차원 호핑망. 정성적 참고 |
| 4a | 6배열 Arrhenius. 1300 K 에서 거의 겹치고 300 K 로 갈수록 2자릿수로 벌어짐 | 🔴 **σ 2자릿수 스프레드의 대부분이 외삽의 산물**임을 보여준다. 우리 아레니우스 규율의 근거로 인용 가능 |
| 4b | 자리별 cage 간 점프 빈도 (S²⁻ 0–15 / Cl⁻ 0–15, 0–8 jump/ps, 700 K) | 🔴 **σ 와의 상관이 S 자리에서만 성립하고 Cl 자리에서는 반대**(100%-0% 가 σ 최저인데 Cl 점프는 7.8/ps 최고). 본문 서술보다 조건부다 |
| S1 | 100%-0% 배열 MSD vs τ, 700–1300 K. (a) 선형 (b) log-log | 🔴 **우리 MSD 창 2–50 ps 에 대한 유일한 실질 위협** — 700 K 에서 τ≈10–70 ps 가 평탄부. 우리 A3 검증의 근거 |
| S2 | 원소기준 형성에너지 패리티 + box (eV/atom 단위) | **MACE 만 탈락**(수염 −0.035…+0.178), 나머지 4모델은 구분 불가 ⇒ 이 축엔 정보가 없다 |
| S3 | 500/700/1100 K 총에너지 시계열 10 ps | 🔴 **드리프트의 원자료.** Orb +104/+157/+425, EqV2 +55/+200/+590 meV/atom (digest 계산). ⚠ SevenNet·DeePMD 는 **열요동이 아예 없다**(설명 없음) |
| S4 | (a) Li₇PS₆ 모구조 + Wyckoff(S1 16e / S2 4a / S3 4c / Li 48h) (b) 129배열 구성표 (c) ORB v2·MACE 사전선별 산점도 | 🔴 **평가집합을 피고가 골랐다는 증거.** 또한 (c) 에서 **같은 조성 안 배열 스프레드가 40–50 meV/atom** = MLIP MAE(5–10)의 5–10배 ⇒ 무질서가 모델오차보다 크다 |
| Table 1 | 5모델 회귀통계 (N=158) | 다섯 모델 전부 MAE < 10 meV/atom. SevenNet RMSE/MAE=1.88 (꼬리 두꺼움, 논문 미언급) |
| Table 2 | 모델 사양 (학습셋·파라미터·아키텍처·손실·cutoff·**보존성**) | **★1 의 답이 이 표에 있다.** UMA 없음, 전부 MPtrj/PBE |
| Table 3 | 6배열 DFT ΔE + SevenNet-MD Ea·D·σ | 🔴 **Ea 단위 오기(meV→eV)** · ✅ **ΔE 6값은 우리가 A1 정답으로 쓸 수 있다** |
| Table S1 | 구조유형별 오차 분해 (원 데이터셋) | **논문 결론을 실제로 떠받치는 표.** SevenNet 이 argyrodite 3.717 로 1등, 비-argyrodite 는 10.247 로 꼴찌 |
| Table S2 | 추론 효율 (52원자, 1100 K, 10 ps) | ORB v2 가 SevenNet 의 **4.0배 속도**. **MACE 없음**(=MD 미실행 증거). ⛔ 하드웨어 미기재 |
| Table S3 | 확장 데이터셋 구성 (253) | Br 45 / Cl 47 / Cl-Br 115 / O+할라이드 46 |
| Table S4 | 확장셋 회귀통계 (N=282) | 🔴 **SevenNet 5.763 vs ORB v2 5.907 = 사실상 동률**, RMSE 는 ORB v2 승 ⇒ 본문 그림이 옅어진다 |
| Table S5 | 확장셋 구조유형별 분해 | argyrodite: SevenNet **5.249**(3.717 에서 **+41%**) · ORB v2 6.332 · MACE 13.001 |

---

## 19. 후속 확보 대상 (이 논문이 가리키는 곳)

| 우선 | 문헌 | 왜 |
|---|---|---|
| 🔴 **1** | **ref 53** — Lee, J.; Ju, S.; Hwang, S.; You, J.; Jung, J.; Kang, Y.; Han, S. *"Disorder-Dependent Li Diffusion in Li₆PS₅Cl Investigated by Machine-Learning Potential"*, **ACS Appl. Mater. Interfaces 2024, 16 (35), 46442** | **r2SCAN 학습 SevenNet 으로 ~5 mS/cm 를 낸 원전.** *"σ 를 가르는 건 아키텍처가 아니라 학습 범함수"* 의 정본. **우리 litdb 에 없다** |
| 🔴 **2** | **ref 52** — Kim, J. 외 (Han, S.) *"Data-Efficient Multifidelity Training for High-Fidelity MLIP"*, **JACS 2025, 147, 1042** | 같은 아키텍처 PBE 학습 → **~44 mS/cm @350 K**. 위와 짝. 우리 litdb 에 없다 |
| 🟠 3 | **ref 49** — Bigi, Langer, Ceriotti, *"The dark side of the forces: assessing non-conservative force models"*, arXiv:2412.11569 | **보존/비보존 논거의 원전.** 우리 UMA 방어의 이론적 근거 |
| 🟠 4 | **ref 50** — Fu, Wood, Barroso-Luque, Levine, Gao, Dzamba, Zitnick (2025), *"Learning smooth and expressive interatomic potentials…"* | **eSEN 논문 = UMA 의 직계 선행.** UMA 의 NVE 보존 시험 방법이 여기서 온다 |
| 🟠 5 | **ref 42** — Deng 외, PES softening | softening 진단의 원전 |
| 🟡 6 | ref 62 — Jun & Lee 2022 | ✅ **이미 있다**: `litdb/papers/jun2022_argyrodite_ion_cage_size_descriptor.md` |
| 🟡 7 | ref 18 — Dembitskiy 외, npj Comput. Mater. 2025, nebDFT2k | SevenNet 의 "균형 잡힌 오차" 를 독립 확인한 벤치 |
| 🟡 8 | ref 3 — Minafra 외, Inorg. Chem. 2020 (4a 점유 ~50% Rietveld) | 실험 자리무질서 기준값 |

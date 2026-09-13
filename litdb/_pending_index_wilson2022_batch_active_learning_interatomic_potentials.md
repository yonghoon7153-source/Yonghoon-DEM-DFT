# 📥 PENDING — `wilson2022_batch_active_learning_interatomic_potentials` 인덱스/비교 반영 대기
> ✅ **① INDEX.md 병합 2026-09-13** (조율 세션) — 변형: 4열 → 3열 (3·4열을 " · " 로 합침, 내용 손실 없음). ⏳ **②③ `comparison_vs_ours.md` 블록은 미병합** — 절 번호 충돌(J-11/J-12)·기존 판정 개정 요청이 섞여 있어 큐레이터 판단이 필요하다.

> 작성 2026-09-09 · litdb-curator (동시 실행 6개라 `INDEX.md`·`comparison_vs_ours.md` 직접 편집 금지)
> **사람이 확인한 뒤 아래 덩이를 각각 옮겨 붙이고, 이 파일을 지운다.**
>
> ⚠ **이 편은 물성값이 0건이다** (σ·Ea·ESW·gap·탄성 전부 없음, 재료계 = 단층 GeSe).
> ⇒ ⛔ **물성 4축(A/B/C/D) 표에 넣지 않는다.** 붙일 곳은 **두 군데**:
> ① **§J-7 `🔧 방법 원전`** — 배치 AL 알고리즘의 정의 원본
> ② **§J-9 능동학습 축** 에 **J-9c 소절 신설** — `[Cho25AL]`(실험 PSO) · `[Ma25AL]`(GP-EI) ·
>    `[Ou26MS]`(MTP γ local-AL) 에 이어지는 **네 번째 형식 = 풀 기반 배치 AL**
>
> ⚠ **형제 편과의 관계**: 오늘 들어온 UQ 다발(`carrete2023` · `kurniawan2025` · `grasselli2025` ·
> `imbalzano2021`)의 pending 이 **J-11 신설**을 제안하고 있다. 이 편은 **UQ 자체가 아니라 UQ 를
> 쓰는 루프(AL)** 라서 **J-9 가 맞다**. 다만 §J-9c 표의 "불확실도" 행이 J-11 과 맞닿으므로
> **병합자가 J-9c ↔ J-11 상호참조 한 줄을 걸어 두면 좋다.**

---

## 1. `INDEX.md` — 붙일 위치: `## 🤖 MLIP 방법론 — **우리 UMA 스택을 재는 축** (2026-08-19 신설)` 표

| `papers/wilson2022_batch_active_learning_interatomic_potentials.md` **(본문 9 pp + SI 7 pp 전문 정독 · 그림 8점 실제 판독)** | **[외부·methods·⛔물성 4축 아님·★배치 능동학습 원전]** **Nathan Wilson**/D. Willhelm/**Xiaoning Qian**/**Raymundo Arróyave\***/**Xiaofeng Qian\*** (전원 **Texas A&M**), "**Batch active learning for accelerating the development of interatomic potentials**" (***Comput. Mater. Sci.* 208, 111330 (2022)**, DOI `10.1016/j.commatsci.2022.111330`, 접수 2021-12-27/수락 2022-03-01; **⛔ OA 아님 © Elsevier**; **코드·데이터 비공개** — 원문 *"cannot be shared at this time"*). **재료계 = 단층 GeSe 하나** (2D 강유전-강탄성체; Li·P·S·Cl **0**). **자체 DFT 0회** — 라벨 13,006개를 **Yang et al. 2021 (*Adv. Mater.* 33, 2103469)** 의 기존 DB 에서 꺼내 쓴다 ⇒ **wall-clock·core-hour 절감 실측이 논문에 0건**. **핵심 = 배치를 어떻게 고르는가**: 점수 `S_i = 0.9·(U_i/Ū) + 0.1·(D_i/D̄)`, **U = 10-멤버 bagging(라벨셋 80 % 부표본) 앙상블의 에너지 표준편차**(식 1), **D = 이번 배치 선택집합까지 유클리드 거리의 *합***(식 2). **⭐ top-k 가 아니다 — greedy 조건부**: 한 개 뽑을 때마다 **D 만** 전 미라벨에 대해 재계산(U 는 배치 내 고정), `N_SB`=10 이 찰 때까지. **모델 = AGNI 서술자 121차원(2체 24 + 3체 96 + 상수 1, R_c 5.5 Å) + 선형커널 KRR(=ridge, sklearn, λ=1e-4, 표적 = 원자당 에너지)** ⇒ **⭐★6 답: D-optimality/leverage(MTP γ) 에 의존하지 않는다** — 저자 명시 *"model-agnostic … estimates the uncertainty internally by using the predictions from multiple models"*, Podryabinkin/Gubaev 는 **인용만 하고 채택 안 함** ⇒ **우리 `mlip_committee.py` 를 막고 있던 "γ 는 선형모형 전용" 장벽이 이 처방엔 없다**. **결과 (전부 `N_S`=10 시드 × AL·random 2 arm)**: 에너지 RMSE(un-sampled) `figure-read` **AL 0.00128 vs random 0.00160 eV/atom**(≈19 % 개선, **절대 이득은 작다**) · 힘 RMSE `figure-read` **AL 0.168 vs random 0.255 eV/Å @1,000 구조**(1.52×), **AL@1,000 < random@3,000 ⇒ digest 도출 데이터효율 ≥3×(⚠ 논문 미보고)** · **121 계수 전부가 AL 은 ~2,000 구조(~200 배치)에 수렴, random 은 3,000 에서도 산포**(Fig. 3 + **SI Fig. S1/S2**) · 포논 시드 산포 AL@3,000 육안 소멸 vs random@3,000 잔존 · MD(LAMMPS, 20×20 = **1,600원자**, NPT 계단승온 50→450 K, 40 ps/온도) 로 **상전이 300–350 K** 재현. **🔴 비판 6건 (digest §10)**: ① **다양성 항이 배치 후반에 1/j 로 희석된다** — `D` 가 *합*이라 10번째 선택 시 완전중복의 페널티가 ≈1/9 × β(0.1) ≈ **1 %** ⇒ 저자가 든 동기(중복 회피)를 정작 못 막는다. **min 거리/DPP/local penalization 이면 배치크기 무관** ② **`Fig. 3a,b` 는 "AL 이 더 정확"을 지지하지 않는다** — `figure-read` batch 300 에서 AL 0.22–0.28(조밀) vs random **0.15–0.55**(산포), **random 상위 시드가 모든 AL 시드보다 낮다** ⇒ 정직한 서술은 **분산 축소**뿐 ③ **`Fig. 5` 에 DFT 기준 포논이 없다** — 정밀도만 보이고 정확도는 안 보인다. 실제로 `figure-read` **AL 평탄가지 1,000→3,000 구조에서 ≈1.2 → ≈1.35 THz 로 평균이 아직 이동 중**(= 낮은 분산 + 미해소 편향) ⇒ ⛔ **"committee 가 일치했다"를 정확도 근거로 쓰면 안 된다** ④ **원자평균 특징벡터**(digest 추론: 표적이 원자당 에너지 + 구조당 121차원)라 **국소 희소 사건(도펀트 1개·계면 1층)이 평균에 묻힌다** — 우리 도펀트 문제엔 `[Ou26MS]` 의 `--al_mode=nbh`(원자환경 AL) 쪽이 맞다 ⑤ **결정적 ablation 부재 — `β=0`(순수 top-k) arm 이 없다** ⇒ *"다양성 항이 top-k 를 이긴다"* 가 **증명되지 않았다**; **배치크기 k 민감도도 없다**(k=10 고정, 근거 = "DFT 병렬 던지기" 정성 동기뿐) ⑥ **중단조건 = 고정 예산 3,000 구조** — 피팅오차도 목표물성도 아니다(*"convergence threshold of desired physical properties"* 는 **가능성만 언급, 미구현**) ⇒ **`[Ou26MS]`(목표물성 수렴 실구현) > 이 편**, 우리 **보고량 카드**가 셋 중 가장 앞선다. 기타: 힘 RMSE **0.157–0.255 eV/Å 는 우리 눈금(MTP 자체학습 0.073·SevenNet-0 0.070)의 2–4배** ⇒ AL 이득이 파운데이션 정확도 영역에서도 남는지 미검증 · 거짓음성 직접시험 없음(미표집 RMSE·parity 이상치 부재의 **간접 증거만**, 꼬리 분석 0) · SI Fig. S1/S2 **y축 눈금 라벨 없음**(정성 전용) · 2D 단층의 a=b 상을 반복해 *"cubic"* 이라 부름(정방이 맞다). **✏ 서지 정정 2건**: *"X. Qian"* 은 **두 사람**(Xiaoning Qian 3저자 ≠ Xiaofeng Qian 마지막·교신), 마지막 저자는 **Arróyave 가 아니라 Xiaofeng Qian**(교신은 둘 다) | ✅ `papers/wilson2022_batch_active_learning_interatomic_potentials.md` (§11 ★1–★8 직답 · §14 우리 cascade·UQ 처방) | **🔧 방법 원전 — 배치 능동학습 획득함수·배치 다양성.** ⛔ 재료계 겹침 **0**(GeSe). 물성값 이전 **0건**. 축 A–I 해당 없음 — **J-7 + J-9c** |

---

## 2. `comparison_vs_ours.md` — 절 초안

### 2-a. `## 📑 Reference key` 표에 추가할 행

| **[Wilson22BAL]** ★ | **N. Wilson**/D. Willhelm/**Xiaoning Qian**/**R. Arróyave\***/**Xiaofeng Qian\*** 2022 ***Comput. Mater. Sci.* 208, 111330** (Texas A&M 단일기관; DOI 10.1016/j.commatsci.2022.111330; **⛔ 비-OA · 코드·데이터 비공개**) — "**Batch active learning for accelerating the development of interatomic potentials**". **풀 기반(pool-based) 배치 능동학습**: 13,006 구조 풀에서 **에너지 불확실도(10-멤버 bagging) + 특징거리**의 가중합으로 **greedy 조건부**로 배치(10개)를 채운다. **⭐ D-optimality/leverage 를 쓰지 않는 model-agnostic 처방** — MTP γ 가 UMA 로 안 넘어가는 문제의 **유일한 우회로 원전**. ⛔ **재료계 = 단층 GeSe**(Li·P·S·Cl 0), **자체 DFT 0회**(라벨은 Yang 2021 DB 재활용), **물성값 이전 0건**, **비용 절감 실측 0건** | ✅ `papers/wilson2022_batch_active_learning_interatomic_potentials.md` | **MLIP 방법론 (계산 100 %) · 참조 DFT = VASP/PBE (남이 돌린 것)** — **방법 원전 전용, 축 A–I 제외** |

### 2-b. `### J-7. 🔧 방법 원전` 블록에 추가 (⚠ **물성 4축 표에 넣지 않는다**)

**[Wilson22BAL] `wilson2022_batch_active_learning_interatomic_potentials` — 배치 능동학습 획득함수의 정의 원본**

> ⛔ **σ·Ea·D·ESW·탄성·gap 이 0건**이고 재료계도 겹치지 않는다(GeSe). 여기 있는 것은
> **"배치를 어떻게 고르는가"의 식**이고, 그것 하나가 이 편의 전부다.
> ⭐ **`[Shapeev16]` 블록 바로 아래 놓는 것이 맞다** — `[Shapeev16]` 이 *"우리가 못 쓰는 길(선형 설계행렬)"*
> 을 정의하고, 이 편이 *"그 가정 없이 가는 길"* 을 정의한다. 두 블록을 붙여 놓아야 축이 보인다.

| 항목 | [Wilson22BAL] | 우리 (`tools/ionic/mlip_committee.py` · cascade Stage 07/08) | 판정 |
|---|---|---|---|
| **불확실도 정의** | **query-by-bagging** — 같은 모델을 라벨셋 **80 % 부표본**으로 `N_M`=10회 재학습, 예측 에너지의 **표본표준편차**(식 1, Bessel `N_M−1`) | **이종 committee** UMA-s-1p1(OMat24) / MACE-MP-0(MPtrj) / SevenNet-0(MPtrj), **M=3** | 🔴 **재는 것이 다르다.** 배깅 = **데이터 표집 분산**, 우리 = **아키텍처+훈련셋 편향**이 섞인 것. **숫자를 나란히 못 놓는다** |
| **선형 설계행렬 `X` 의존** | ⛔ **없다.** 저자 명시 *"model-agnostic … estimates the uncertainty internally by using the predictions from multiple models"*. Podryabinkin 2017[28]·Gubaev 2019[27] 은 **인용만 하고 미채택** | 쓸 수 없음(`X` 부재 — `[Shapeev16]` 블록) | ⭕⭕ **이 축에서 제일 큰 소득.** `mlip_committee.py` docstring 의 장벽이 **이 처방엔 존재하지 않는다** ⇒ **UMA 이식 가능** |
| **획득함수** | `S_i = α(U_i/Ū) + β(D_i/D̄)`, **α=0.9 / β=0.1**, Ū·D̄ = 미라벨 전체 평균 | 없음 (순차 게이트만) | ⭕ **이식 후보 (T1, 계산 0회).** 평균정규화 덕에 α·β 가 단위 없이 의미를 갖는다 |
| **배치 다양성** | **greedy 조건부** — 하나 뽑을 때마다 **D 만** 재계산(U 는 배치 내 고정). ⇒ **top-k 아님** ✔ | 없음 | ⭕ 이식하되 **🔴 식을 고쳐서**: `D_i = Σ_j‖·‖`(합) → **`min_j‖·‖`**. 합은 배치 후반에 중복 페널티가 **1/j** 로 희석된다(digest §10-①) |
| **배치 크기 k** | **10 고정.** 근거 = *"DFT 를 병렬로 던지려고"* 정성 동기뿐, **민감도 시험 없음** | 정의 안 돼 있음 | 🔶 **논문의 10 을 베끼지 않는다** — 우리는 **KISTI QOS 동시제출 한도**로 정하는 것이 정직하다 |
| **특징공간 χ⃗** | **수제 121차원, 라운드 간 고정**(AGNI 2체 24 + 3체 96 + 상수 1) | 없음 | 🔴 **UMA 임베딩은 fine-tune 마다 좌표계가 바뀐다** ⇒ **동결 서술자**(SOAP 또는 고정 readout)를 따로 둬야 라운드 간 거리가 비교된다 |
| **특징의 입도** | **원자평균**(digest 추론: 표적 = 원자당 에너지 + 구조당 121차원) | — | 🔴 **국소 희소 사건이 묻힌다.** 도펀트/계면은 `[Ou26MS]` 의 **`--al_mode=nbh`(원자환경 AL)** 쪽이 맞다 |
| **불확실도 채널** | **에너지만.** 힘 불확실도는 계산조차 안 한다 | 우리 보고량은 **D·Ea**(힘/궤적) | 🔴 간극. 에너지 산포가 힘·D 오차의 대리인지 **이 논문이 답하지 않는다** → `[Carrete23UQ]` 축 |
| **재학습 경제성** | `N_M × N_B` = **시드당 3,000회 KRR 피팅**이 무료 | UMA 재학습 = **fine-tune 필요** | 🔴 **진짜 이식 장벽은 알고리즘이 아니라 비용이다.** 저자도 §4 에서 *"NN 은 비싸진다"* 인정 |
| **시드 반복 보고** | ⭕ **`N_S`=10, 모든 그림에 산포** | 🔴 단일 궤적(Ea 3-seed 뿐) | ⭕⭕ **형식 이식 1순위** (`our_dft_baseline.md` 의 상시 약점) |
| 힘 RMSE 눈금 | **0.157–0.255 eV/Å** | MTP 자체학습 0.073 · SevenNet-0 0.070 | 🔴 **그들 모델이 2–4× 부정확** ⇒ AL 이득이 파운데이션 정확도 영역에서도 남는지 **미검증** |

### 2-c. `### J-9. 능동학습(AL) 축` 에 추가할 소절 — **J-9c. [Wilson22BAL] — 풀 기반 배치 AL (선형모형 가정 없음)**

> **왜 여기 놓나 (네 번째 형식)**: J-9a `[Cho25AL]` = 실험 PSO(대리모델 없음) · J-9b `[Ma25AL]` = GP-EI
> 순차 · `[Ou26MS]` = MTP γ 기반 **생성형** local-AL. **이 편은 풀 기반 *선택형* 배치 AL** 이다.
> ⭐ **우리 도펀트 cascade 는 구조적으로 이 형식에 가장 가깝다** — 후보 풀을 먼저 만들어 놓고 시작한다.

| 항목 | **[Wilson22BAL]** | [Ou26MS] | [Carrete23UQ] | 우리 |
|---|---|---|---|---|
| AL 종류 | **풀 기반 선택형(batch)** | 생성형 on-the-fly(local) | 생성형 적대적 | 순차 게이트 |
| 불확실도 | **bagging 앙상블 σ_E, M=10** | **D-optimality γ (단일 모델)** | 앙상블 분산 | 🔴 없음 |
| **선형모형 의존** | ⛔ **없음 (model-agnostic)** | ⭕ **있음 (MTP 전용)** | ⛔ 없음 | — |
| acquisition | `0.9·U/Ū + 0.1·D/D̄` | MaxVol, γ_select 1.4 / 채택 >1.7 | `σ²_f·exp(−E/k_BT)` | 없음 |
| **배치 다양성** | ⭐ **greedy 조건부 + 가산형 거리 보상** (top-k 아님) | 배치 개념 대신 라운드당 4 독립시드 | — | — |
| 배치 크기 | **10**, 근거·민감도 **없음** | — | — | — |
| 오라클 | **DFT(PBE)** — ⚠ **이미 라벨된 풀에서 꺼냄** | DFT(VASP) 실제 실행 | DFT(GPAW) | **UMA-MD 대리값** |
| **중단조건** | 🔴 **고정 예산 3,000 구조** | ⭐ **목표 물성 수렴** | 오차 수렴 | 예산 |
| **무작위 대조군** | ⭕⭕ **있다 — AL·random 각 10 시드** | ⛔ 없음(대조군 = global-AL) | ⛔ 없음 | ⛔ 없음 |
| **top-k 대조군(β=0)** | 🔴 **없다** | — | — | — |
| 절감 배수 | 🔴 **논문에 없다.** digest 도출 **≥3×**(힘 RMSE, `Fig. 4a`) | 5.4×(사전학습 6.4 × 획득 1.8) | — | — |
| 거짓음성 시험 | 🔴 없음 (미표집 RMSE·parity 이상치 부재 = **간접 증거만**) | — | — | — |
| 시드 반복 | ⭕ **10** | 5(MTP 산포) | 12(MD 궤적) | 3(Ea 600 K) |

**⇒ J-9 에 추가할 판정 3줄**

- **J9-j ⭕⭕ "AL 이 랜덤보다 낫다"를 실제로 대조한 첫 편이다.** J-9 머리의 판정
  *"두 편 다 AL 이 랜덤보다 낫다를 증명하지 않았다"* 의 **첫 예외**. 다만 이겨 낸 것은
  **평균 정확도가 아니라 시드 재현성**이다(digest §10-②) — **인용할 때 그 단서를 뗄 수 없다.**
- **J9-k ⭐⭐ 배치 다양성 강제의 최소 처방을 얻었고, 그 결함까지 같이 얻었다.**
  greedy 조건부는 가져오되 **거리항을 합 → min 으로 바꾼다.** 그리고 **`β=0`(top-k) arm 을
  우리가 넣어야 한다** — 논문에 없어서 *"다양성 항이 값을 하는가"* 가 미해결이다.
- **J9-l 🔴 중단조건은 이 편에서 가져오지 않는다.** 고정 예산은 우리가 이미 하는 것이고,
  `[Ou26MS]` 의 목표물성 수렴 + 우리 **보고량 카드**(`kb/templates/estimand_card.md` §4:
  검증 게이트를 **결과 보기 전에** 박는다)가 둘 다보다 앞선다.

### 2-d. `### J-9` (또는 신설 J-11 UQ 축) 에 걸 **M 판정 한 덩이**

> ⚠ **먼저 정직하게: 이 논문은 우리 M 문제를 풀어 주지 않는다.** M=10 을 **근거 없이** 썼고
> (선택 이유가 논문에 **없다**), **M 민감도 실험도 없다**. 아래는 이 편 + 기존 판정을 겹쳐 세운 것이다.

**M-1. 질문을 둘로 쪼갠다 — 이 편이 그 구분을 실물로 보여준다.**

| 용도 | M=3 이 되는가 | 근거 |
|---|---|---|
| **(a) 랭킹** (argmax 로 다음 라벨 고르기) | 🔶 **된다, 단 잡음이 크다** | [Wilson22BAL] 이 하는 것이 정확히 이것 — **캘리브레이션 0**. **Grasselli 식 (27) 의 `M≥4` 는 캘리브레이션 요건이지 랭킹 요건이 아니다** |
| **(b) 정량 보고** (σ 를 값으로 쓰거나 오차와 대조) | ⛔ **안 된다** | 식 (27) 에서 `(M−3)/(M−1)=0` → `α² = −1/3 < 0`. **기존 판정 유지** |

**M-2. 판정 초안 3줄**

1. **⭕ M=3 으로 지금 진행해도 되는 용도가 있다 — 배치 랭킹.**
   ⛔ 단 **σ 값을 문장에 쓰지 않고**(기존 인용금지 유지), **근소차는 무작위로 처리**하며
   그 자리를 **다양성 항(2-b 의 min 거리)** 에 맡긴다. M 이 작을수록 거리항의 상대 가치가 커진다.
2. **🔶 올린다면 목표는 `M≥4` 가 아니라 "잡음 절반"이다.**
   🔎 digest 계산(가우시안 잔차, 표본표준편차의 상대표준오차 `1/√(2(M−1))`):
   **M=3 → 50.0 % · M=4 → 40.8 % · M=10 → 23.6 %.**
   ⇒ **3→4 는 9 %p 뿐** — *"M=4 로 올려 캘리브레이션한다"* 는 형식만 만족하고 실익이 적다.
   할 거면 **M ≈ 8–10**(= Wilson 자리)까지 가야 의미가 있다.
3. **⭐ 이 편이 연 것은 M 의 숫자가 아니라 *멤버 제조법* 이다 — bagging.**
   우리 M=3 은 **이종 파운데이션이 3개뿐**이라서 3 이다. Wilson 의 M=10 은 **같은 모델을
   데이터 80 % 부표본으로 10번 학습**해 만든다 — **새 아키텍처가 필요 없다.**
   ⇒ `[Tompa26]` 으로 UMA fine-tune 경로가 열리면 **부표본 M개 fine-tune** 으로 M 을 늘릴 수 있고,
   **⭐ 이 경로는 "높은 EMA(0.999~0.9999)가 snapshot ensemble 을 죽인다"는 우리 긴장을 우회한다** —
   배깅 멤버는 **독립 학습런**이라 EMA 평균이 멤버 간 차이를 지울 수 없다.
   **snapshot 이 아니라 bagging 이 답이다.**
   ⚠ 대가 = 라운드마다 M회 fine-tune(재학습 비용이 새 병목). 절충안 = **N 배치마다 한 번만 committee 갱신**
   — ⛔ **이 절충의 타당성은 논문에 없다. 우리가 시험해야 한다.**

**M-3. ⛔ 이 편으로 답할 수 없는 것 (명시해서 남긴다)**
- M 을 몇으로 해야 하는가 → **논문에 없다.**
- 에너지 앙상블 산포가 **힘·D** 오차의 좋은 대리인가 → **논문에 없다**(에너지만 쓴다).
- 파운데이션 정확도 영역(0.07 eV/Å)에서도 AL 이득이 남는가 → **논문 밖**(그들 모델은 0.157–0.255).
- **committee 가 조밀하면 정확한가 → 아니다.** `Fig. 5` 가 반례다(digest §10-③):
  **시드 산포는 이미 사라졌는데 평균 포논은 아직 이동 중**(`figure-read` ≈1.2 → ≈1.35 THz).
  ⇒ ⛔ **"우리 3개 모델이 일치했다"를 정확도 근거로 쓰지 않는다** — 기존 규율 재확인.

### 2-e. ⛔ 이 편으로 **하면 안 되는 것**

- ⛔ **"AL 로 DFT 를 N배 아꼈다" 근거로 인용** — 그 배수가 논문에 **없고**, **DFT 를 실제로 돌리지도 않았다**
  (라벨을 기존 DB 에서 꺼냈다). core-hour·wall-clock **0건**.
- ⛔ **"배치 다양성 항이 top-k 보다 낫다"로 인용** — `β=0` ablation 이 **없다**.
- ⛔ **"AL 퍼텐셜이 더 정확하다"** → **"더 재현적이다"** 로만. `Fig. 3b` 에서 **random 상위 시드가 이긴다.**
- ⛔ **DFT 세팅(k-mesh·ecut·PAW) 근거로 인용** — 이 논문에 **없다**(Yang 2021 을 봐야 한다).
- ⛔ **물성 4축(A/B/C/D) 표에 행 만들기** — 물성값 **0건**이라 전부 `n/a` 가 된다.

---

## 3. `properties/` · `db/` 갱신

- **`litdb/properties/`** — repo 에 없음.
- **`db/`** — ⛔ **이번 세션 수정 금지 지시라 손대지 않았다** (읽기만 했다).
  값이 바뀔 일은 없다 — **이 편은 물성값을 하나도 주지 않는다.**
- 사람이 반영할 때 검토할 것 (**값 변경 아님, 라벨만**):
  `db/properties/canonical_registry.json` 의 MLIP-MD 항목에 **"단일 궤적 · 시드 반복 없음"** 이
  이미 주석돼 있는지 확인. [Wilson22BAL] 은 **`N_S`=10 시드 산포 보고**가 표준임을 보여주는
  외부 선례이므로, 그 주석의 **근거 링크**로 쓸 수 있다.

## 4. 🎤 talk 역링크 — **불필요 (확인 완료)**

`grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → **`talks/lee2026_skku_mlip_materials_design.md` 하나뿐.**
그 **§99-10 대기열**(9행: Kim2026 hydrolysis · 자료집 목차 · **Shapeev2016 / Gubaev2019 / Podryabinkin2017 /
Novikov2021 / Podryabinkin2023(MLIP-3)** · Merchant GNoME · Park SevenNet · Luo cryo-TEM · Shin BH₄ ·
KimYS moisture · KimYH GA-MLIP)에 **Wilson / Willhelm / Arróyave / Qian / Texas A&M / GeSe / batch active
learning 없음** ⇒ **양방향 링크 대상 아님.**

> 🔗 단, **간접 연결 하나**: 그 대기열의 **3b·3b′·3c·3c′(Shapeev/Gubaev/Podryabinkin/Novikov)** 는
> **MTP γ(D-optimality) 계보**이고, **[Wilson22BAL] 은 그 계보를 명시적으로 인용하면서 채택하지 않는
> 대안 계보**다(ref [27],[28] = Gubaev 2019 · Podryabinkin 2017). 이미 있는
> `papers/shapeev2016_moment_tensor_potentials.md` 와 **상호링크 한 줄**을 걸면
> *"선형 설계행렬이 있는 길 vs 없는 길"* 이 litdb 안에서 대비된다.
> ⇒ 병합자가 `shapeev2016` digest 에 한 줄 추가하면 즉시 연결된다.

## 5. 그 밖

- **`litdb/pdf_map.tsv`** — 필요하면 행 추가:
  `wilson2022_batch_active_learning_interatomic_potentials` ↔
  `98._Batch_active_learning_for_accelerating_the_development_of_interatomic_potentials.pdf`
  (+ SI `98._Sup_…pdf`). **`litdb/figures/_sources.json` 에는 추출 도구가 이미 기록했다**
  (203편째로 추가 — ⚠ 동시 실행 중이라 다른 큐레이터 항목과 병합 확인 필요).
- **`litdb/inbox/`** — ⛔ **복사하지 않았다.** 업로드 경로에서 직접 `--pdf` 로 크로핑했다
  (동시 실행 6개라 공유 폴더를 안 건드리는 쪽을 골랐다). 사람이 원하면
  `98. …pdf` / `98. Sup) …pdf` 로 넣으면 된다.
- **`litdb/figures/wilson2022_…/`** — **13점**(본문 `fig_1`–`fig_6` + `tab_1` · SI `fig_S1`–`fig_S6`).
  **실제 판독 9점**(fig 1–6 + S1 + S2 + tab_1), **미판독 4점**(`fig_S3`–`fig_S6` = GeSe 원자구조 렌더,
  수치·축 없음). 추출 오탐 **0건**, 누락 **0건**.

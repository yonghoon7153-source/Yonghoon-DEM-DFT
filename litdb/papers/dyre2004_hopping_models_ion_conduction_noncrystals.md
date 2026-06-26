# Hopping models for ion conduction in noncrystals — Dyre & Schrøder (arXiv cond-mat/0407083, 2004; based on Rev. Mod. Phys. 72 (2000) 873)

> slug `dyre2004_hopping_models_ion_conduction_noncrystals` · arXiv `cond-mat/0407083` (no journal DOI; this is the short proceedings/lecture companion to the full review **Rev. Mod. Phys. 72 (2000) 873**) · type `theory/review (analytic + Monte-Carlo lattice hopping simulation)` · PDF `82ea256b-…12._Hopping_models…noncrystals.pdf` (mixed into the `82ea256b` upload folder) · digested `2026-06-26` · status ✅ (filed as **[외부] / theory framework**)
> **저자**: Jeppe C. Dyre, Thomas B. Schrøder — Department of Mathematics and Physics (IMFUFA), Roskilde University, DK-4000 Roskilde, Denmark (dyre@ruc.dk)

---

## ⚠ 이 논문의 위치: 외부 THEORY FRAMEWORK — argyrodite 논문도, 우리 그룹 논문도 아님

> **이 논문은 *비결정질*(유리·고분자·비정질 반도체)에서의 이온/전자 hopping 전도 일반 이론 리뷰다.** Li₆PS₅Cl argyrodite를 다루지 **않으며**, σ/Ea의 *수치*를 우리 재료에 주지도 않는다.
> - **무대 = noncrystals(disordered solids)**: 유리, 고분자, 비정질 반도체. **argyrodite는 *결정질*** — 그래서 이 논문은 우리에게 **수치 전이 0**, **"개념 어휘"로만** 차용한다(아래 §7).
> - **보관 이유 = 단 하나**: 우리가 동시에 digest하는 **site-percolation 논문의 *수송이론 짝(transport-theory complement)***. 즉 "Li가 어디로 *갈 수 있나*(percolation/geometry)"의 짝으로 "Li가 *어떻게 hop하나*(σ(ω) 분산·Arrhenius Ea·Haven 비)"의 **개념 vocabulary**를 준다.
> - **comparison_vs_ours.md 물성 4축(A 이온/B 산화/C 기계/D 전자)에 *수치로* 넣지 않는다.** 축 A(Li 이동도)에 **"framework note"** 한 줄로만 등재 — 우리 σ_NE/Ea/Haven/dopant-blocking을 *해석할 때 쓰는 말*로서.
> - **[우리 그룹] 태그 금지. 수치 대조·"일치" 주장 금지.**

---

## 0. 이 digest를 읽는 법

이 논문이 답하는 질문은 단 하나다: **"유리·고분자·비정질처럼 *무질서한* 고체에서 이온(또는 전자)이 hopping으로 움직일 때, 실험에서 보편적으로 관찰되는 네 가지 사실 — ① dc 전도도가 Arrhenius다, ② ac 전도도 σ(ω)가 지수 < 1의 거듭제곱 분산을 보인다, ③ 그 σ(ω)가 시간-온도 중첩(time-temperature superposition)을 따른다, ④ 서로 다른 물질이 거의 같은 ac 응답을 보인다(준-보편성) — 을 *가장 단순한* 하나의 모델로 동시에 설명할 수 있는가?"** 저자들의 답은 **"있다 — random barrier model(RBM)이 그 '이상기체 모델(ideal gas model)'이고, 그 모든 보편성의 열쇠는 *percolation*(스미기)이다."**

핵심 통찰 두 가지:
1. **dc 전도도가 Arrhenius인 *진짜* 이유는 "장벽 분포가 좁아서"가 아니라, 정확히 그 반대 — 장벽 분포가 *넓을* 때 percolation이 *하나의 병목 장벽(bottleneck barrier)*을 골라내기 때문이다.** 저온에서 이온은 작은 장벽만 골라 뛰지만 무한히 멀리 가려면 percolation cluster 위의 *가장 큰* 장벽을 반드시 넘어야 한다 → 그 단일 병목이 dc 활성화에너지가 된다.
2. **ac 전도도의 보편성(σ(ω) 거듭제곱·시간-온도 중첩·물질 무관)도 같은 percolation에서 나온다.** 저온에서 ac 전류도 주로 percolation cluster 위를 흐르고, "유일하게 의미 있는 수"는 dc 활성화에너지에서의 장벽 확률밀도 p(E) 값 하나뿐이며, 그마저도 데이터를 무차원 변수로 스케일하면 "씻겨 나간다(scaled away)". 그래서 모든 무질서 이온전도체가 같은 곡선으로 모인다.

우리에게 이것이 왜 중요한가: **우리 argyrodite는 *결정질*이라 이 논문의 결론을 *그대로* 가져올 수 없다.** 하지만 (a) argyrodite의 **anion-sublattice disorder**(S²⁻/Cl⁻가 4a/4c 자리를 무질서하게 점유)와 (b) 우리 AIMD가 보는 **correlated/concerted Li hopping**(Haven 비 < 1)은, 이 논문이 제공하는 **"장벽 분포 → percolation 병목 → Arrhenius Ea"** 와 **"correlated hopping → Haven 비"** 라는 *어휘*로 깨끗하게 *서술*된다. 즉 이 논문은 우리 숫자를 *검증*하지 않지만, 우리 σ_300K·Ea·Haven·Nd-blocking을 *말로 설명*하는 표준 vocabulary를 준다.

## 1. 한 줄 요약

비결정질 이온/전자 전도의 보편적 4대 실험사실(Arrhenius dc σ · σ(ω) 거듭제곱 분산 · 시간-온도 중첩 · 물질-무관 준보편성)을 **단 하나의 random barrier model(RBM)**(단순입방 격자 위, 상호작용 없는 입자, 장벽만 무질서)로 동시에 재현하며, **그 모든 보편성의 열쇠는 percolation** — dc Ea는 percolation cluster 위의 *최대 병목 장벽*, ac 보편성은 그 병목 근처 장벽들이 지배 — 임을 해석·시뮬레이션으로 보인다. RBM = 이온전도의 "이상기체 모델".

## 2. 메타 / 동기

| 항목 | 내용 |
|---|---|
| 저자 | Jeppe C. Dyre, Thomas B. Schrøder (Roskilde University, IMFUFA, Denmark) |
| 형식 | 짧은 리뷰/강의노트 (8 pp, ~25 refs). **풀 리뷰 = Rev. Mod. Phys. 72 (2000) 873** [ref 10] — 본문이 반복 인용 |
| arXiv | **cond-mat/0407083** (저널 DOI 없음 — preprint/proceedings) |
| 시스템 | **noncrystals**: 유리(glasses), 고분자(polymers), 비정질 반도체(amorphous semiconductors) — *결정질 아님* |
| 연구유형 | **이론** (master-equation 선형화 해석 + RBM의 **Monte-Carlo lattice hopping 시뮬레이션**, 3D) |
| 동기 | 1950년대에 "장벽 분포(distribution of barriers)" 아이디어가 *세 가지 실험 논거*로 기각됐는데(§아래), percolation(1957 이후 발전)이 그 논거들을 **무효화**함을 보이는 것 |
| 핵심 주장 | RBM = 이온전도의 **이상기체 모델**(ideal gas model) — 디테일을 버리고 *보편 물리만* 담는 최소 모델 |

저자가 "이해하고 싶은 보편 사실" 4가지(intro, ref 5–10):
1. **dc 전도도는 Arrhenius 온도의존**.
2. **ac 전도도는 지수 < 1의 근사 거듭제곱**을 따르고, 고정 주파수창에서 보면 그 지수가 *온도가 절대영도로 갈수록 1로* 간다.
3. **ac 전도도는 시간-온도 중첩(scaling)을 따른다** — 온도가 달라도 같은 ac 응답이 log-log plot에서 *평행이동*만 한다.
4. **서로 다른 고체가 거의 같은 ac 응답**을 보인다 = (준)보편성.

## 3. 핵심 정량/정성 내용 (수치·스케일링 총정리)

> 단위 주의: 이 논문은 **무차원 양**(scaled σ̃, scaled ω, 역온도 β)과 **확률밀도 p(E)** 중심이다. eV·S/cm·Li 같은 우리 절대값은 **존재하지 않는다.** 아래는 *프레임·스케일링 법칙·정성 임계*다.

### 3.1 random barrier model (RBM)의 정의 (§2)
- **격자**: 단순입방(simple cubic) 위 이온 자리.
- **입자**: **완전 비상호작용**(non-interacting) — Coulomb 반발 *무시*, 그리고 **self-exclusion(자기배제)도 무시**(즉 한 자리에 한 이온만 들어간다는 제약도 버림). 저자 강조: "비현실적으로 보이지만 더 일반적인 master equation을 선형화하면 이 식이 나온다"(ref 10).
- **에너지 landscape**: 모든 *극소(minima)는 등에너지*(equal minima) — 즉 자리 에너지 무질서는 *없고*, **장벽(barrier)만 무질서**. 장벽 높이 E가 격자 link마다 확률밀도 **p(E)** 에 따라 *무작위·무상관*(uncorrelated)으로 분포(Fig 1).
- 외부 전기장이 걸리면 landscape가 기울어 전류가 흐름. 단 fluctuation–dissipation 정리에 의해 **dc σ ∝ 영(0)-장(場)에서의 단위시간당 평균제곱변위(MSD)** 이므로, 본문은 영-장에서만 논함.

### 3.2 "장벽 분포는 좁아야 한다"는 1950년대 3대 논거 — 그리고 그 반박 (§"Three classical arguments")
무질서 고체에 장벽 분포가 있는 게 자연스러운데, 다음 3가지가 "분포는 극도로 좁아야 한다(사실상 단일 장벽)"는 근거로 쓰였다:
1. **(Arrhenius dc)** 장벽이 여러 크기면 *어느* 장벽이 dc Ea여야 하나? → non-Arrhenius일 것이다(저온=작은 Ea, 고온=큰 Ea가 점점 개입).
2. **(onset 주파수 Ea < dc Ea)** ac 전도는 *짧은* 거리 이온운동, dc는 *긴* 거리 → ac는 더 작은 장벽 관여 → ac onset 주파수의 Ea가 dc Ea보다 *작아야* 한다(저자: "이건 *맞다*").
3. **(시간-온도 중첩 위배)** 장벽 분포가 있으면 log-log plot에서 응답이 *온도 내릴수록 넓어져야* 한다(저온일수록 더 많은 decade의 jump rate 관여) → 중첩 위배.

→ **저자**: 이 "그럴듯한" 논거들이 percolation 때문에 *틀렸다*. (상세 = ref 10.)

### 3.3 dc 전도도가 Arrhenius인 이유 = percolation 병목 (§3, Fig 2) — **핵심**
- 장벽 E가 link마다 p(E)로 무작위. **저온**(분포 폭 ≫ k_BT) 가정.
- 작은 장벽 = 큰 jump rate → 이온은 작은 장벽을 *선호*. 대부분의 hop은 작은 장벽을 넘는다.
- **그러나 무한히 멀리(=dc 전류) 가려면**, 작은 장벽만으로 이루어진 연결망이 *전체를 관통(percolate)*해야 한다. 장벽을 *작은 것부터* 차례로 "표시(mark)"해 가면, 어느 순간 **percolation threshold**에서 표시된 link들이 *무한 cluster(percolation cluster)*를 이룬다(Fig 2: 2D square lattice, 위=threshold 아래(무한 cluster 없음), 아래=threshold 위(무한 cluster 생김)).
- **이때 넘어야 하는 *가장 큰* 장벽 = percolation cluster 위 최대 장벽 = dc 활성화에너지.** 이보다 큰 장벽은 dc 전류엔 불필요.
- **왜 Arrhenius인가**: percolation이 *하나의 명확한 병목 장벽*을 골라주기 때문. 저온에선 그 병목 위 jump rate가 여러 decade에 걸쳐 가장 느리므로 *전체 운동을 완전히 지배* → 단일 Ea → Arrhenius.
- **역설적 강조**: "percolation은 *넓은* 장벽 분포일 때만 의미가 있다. 분포가 좁아야 한다는 1950년대 논거는 정확히 거꾸로 — *넓을* 때만 Arrhenius dc가 나온다."

> 🔑 이 §3가 이 논문의 심장이다: **무질서(넓은 장벽 분포) → percolation → *단일 병목 장벽* → Arrhenius dc Ea.** "Ea = percolation cluster 위 최대 장벽"이 정량적 정의.

### 3.4 ac 전도도 — RBM의 예측 (§4, Fig 3, 4)
3D RBM의 Monte-Carlo 시뮬레이션(Fig 3, uniform 장벽 분포):
- **(a)** 실수부 σ'(ω) vs 각주파수 ω를, 역온도 β = 20, 40, 80, 160 별로 그림 → 저주파 평탄(=dc) + 고주파 상승(=ac 분산).
- **(b)** 그 데이터를 **하나의 master curve로 스케일** 가능 → **RBM은 시간-온도 중첩(scaling)을 따른다.** 온도 내릴수록 그 master curve가 onset 주파수 둘레 *더 넓은* 주파수창에 적용됨.
- **결론(§4)**: RBM은 (위 §3.2 논거 3과 달리) 시간-온도 중첩을 *재현한다* → "장벽 분포가 중첩을 위배한다"는 고전 논거를 반증. 또 시뮬레이션은 **onset 주파수가 dc 활성화에너지와 *같은* 온도의존**을 가짐을 보임 — 이것이 유명한 **Barton–Nakajima–Namikawa(BNN) 관계** [ref 17–19]의 발현.

### 3.5 ac 보편성(universality) — RBM (§4–5, Fig 4)
- Fig 4: **여러 장벽 분포 p(E)** (p(E)=1 on (0,1); (2/π)^{1/2}exp(−E²/2); (2/π)/(1+E²); exp(−E); 3(1+E)^{−4} …)에 대해 RBM 시뮬레이션 → ac 전도도(σ̃ = σ/σ_dc)를 *스케일된 주파수*의 함수로 그리면 **모두 거의 한 곡선으로 모인다** = **ac 보편성**.
- 점선(slope 1) + **EMA(effective medium approximation)** 실선과 비교: 저온 극한에서 σ(ω)는 *정확한* 거듭제곱이 *아니라* **지수 < 1의 근사 거듭제곱**이고, (스케일된) 주파수 → ∞에서 지수가 천천히 1로 간다.
- **왜 보편적인가(저자의 물리적 설명)**: ac 전류의 보편 부분도 percolation cluster 위를 흐르고, 보편적 거동은 *dc Ea 근처 장벽들이 지배*. "유일하게 의미 있는 수 = dc Ea에서의 p(E) 값 하나"이고, master curve로 스케일하면 *그마저 씻겨 나간다*. 저온 극한("extreme disorder limit")에선 장벽 분포가 *사실상 평탄(flat)* 처럼 작동 → 시간-온도 중첩의 근원("온도를 내리는 건 jump rate 값만 바꿀 뿐, 그들의 *상대* 확률은 안 바꾼다").

### 3.6 NCL(nearly constant loss) (§4 끝)
- 저온/초고주파에서 지수가 **1에 가까운**(NCL, nearly constant loss) 영역 — 이것도 RBM이 재현. 단 저자는 정직하게 "NCL엔 다른 설명들도 있다(ref 24–25)"고 단서.

### 3.7 실험과의 비교 (§5, Fig 5)
- Fig 5: **Sodium Germanate glasses (Na₂O)ₓ(GeO₂)₁₋ₓ** (x=0.003–0.100) [ref 21] ac 데이터 ▽▢△◇(open=실험) vs RBM-보편성 예측(●=full symbol). "Hopping DCA"(diffusion cluster approximation, ref 10) / "macroscopic DCA"와 비교.
- **결과**: 데이터가 *완전히* 동일하진 않아 저자는 "보편성"보다 **"준보편성(quasi-universality)"** 이 적절하다고 함. 그래도 **대부분의 데이터가 RBM으로 합리적으로 fit** 되고, "**ac 전도도 예측에 *피팅 파라미터가 하나도 없는데도*** (무차원 변수로 쓰면) 잘 맞는다"는 점을 강조.

### 3.8 결론과 미해결 문제 (§6) — 우리에게 중요한 "이 모델의 한계" 명세
RBM = dc·ac 이온전도의 본질 물리를 담는 *이상기체 모델*. 그러나 **미해결 3가지**(저자 명시):
1. **Coulomb 상호작용 + self-exclusion**을 넣어 더 현실적으로 만들면 예측이 어떻게 바뀌나? [ref 3, 22]
2. **자리 에너지(site energy)가 다른** 경우(=RBM의 등에너지 가정을 깨고 random-energy 도입)로 일반화하면 ac 보편성이 유지되나?
3. percolation cluster가 전류를 나른다는 물리적 통찰을 어떻게 *정밀한 정량 예측*으로 만드나?

> 🔑 §6의 한계 #1·#2가 우리에게 직접 관련: **RBM은 Coulomb·self-exclusion·자리에너지 무질서를 *전부 끈* 최소 모델**이다. 실제 Li⁺(상호 Coulomb 반발·자리 점유 제약·correlated/concerted 운동)은 RBM의 *비상호작용* 가정을 깬다. 그래서 RBM의 *수치*가 아니라 *개념(percolation 병목·장벽 분포·중첩)* 만 우리에게 전이된다(§7·§10).

## 4. "방법" — 모델/시뮬레이션 (DFT 아님) ★

> 우리 양식의 §4(DFT 방법)에 해당하는 것이 *없다* — 이 논문엔 DFT/AIMD/MLIP/pseudo/k-point/functional이 **전무**하다. 대신 *모델 정의 + 격자 hopping 시뮬레이션*이 그 자리를 차지한다.

- **code/version**: 명시 안 됨(자체 Monte-Carlo). 풀 디테일은 **Rev. Mod. Phys. 72 (2000) 873** [ref 10].
- **모델(우리의 'Hamiltonian/functional' 대응물)**: **RBM** — 단순입방 격자 + 비상호작용 입자 + 등에너지 자리 + link별 무작위 장벽 E~p(E). master equation을 선형화해 얻은 비상호작용 운동방정식.
- **시뮬레이션(우리의 'AIMD' 대응물)**: 3D 격자에서 **hopping Monte-Carlo / master-equation 풀이**로 σ'(ω, β) 계산(Fig 3). 여러 p(E)에 대해 반복(Fig 4).
- **해석 도구**: **percolation 이론**(threshold·infinite cluster·bottleneck barrier, Broadbent–Hammersley ref 14; Shklovskii–Efros ref 15; Ambegaokar–Halperin–Langer ref 16), **EMA(effective medium approximation)**, **DCA(diffusion cluster approximation)** [ref 10].
- **"무질서 처리"(우리의 SQS/enumerate 대응)**: 무질서를 *명시적 SQS*로 decorate하지 않고, **장벽 확률밀도 p(E)** 자체를 입력으로 받아 link마다 무작위 샘플(quenched disorder). 여러 p(E) 함수형을 바꿔 보편성 검증.
- **특이/강조**: ac 전도도 예측엔 **자유 파라미터가 0** (무차원 변수로 표현 시) — "a priori 기대보다 훨씬 잘 맞는다"의 근거.

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 메시지 / (우리에게 전이 가능한 개념 — vocabulary-only) |
|---|---|---|
| **1** | RBM의 전형적 1D 퍼텐셜 — *등에너지 극소* + *무작위 높이 장벽*. 화살표 = 두 가능한 hop. | RBM 정의 시각화: **자리에너지 무질서 0, 장벽만 무질서**. *개념*: "Li hop landscape = 장벽들의 무작위 집합"이라는 사고 틀(우리 BVSE 장벽 분포·li_li_disorder_std의 *추상화*). |
| **2** | 2D square lattice percolation. 위 그림 = threshold *아래*(무한 cluster 없음), 아래 그림 = threshold *위*(무한 cluster 생김). caption: "percolation cluster 위 *최대 장벽* = dc Ea". | **dc Ea = percolation 병목 장벽** 의 그림 정의. *개념(핵심)*: Li가 "*갈 수 있는* 연결망"이 percolate해야 dc 전류가 흐르고, 그 망의 *가장 큰 장벽*이 σ를 율속 — 우리 **site-percolation 짝**의 수송 버전, 그리고 우리 **inter-cage hop = rate-limiting 장기 hop**(§7). |
| **3** | (a) 3D RBM σ'(ω) vs ω, β=20/40/80/160. (b) 같은 데이터를 *하나의 master curve*로 스케일. | **시간-온도 중첩(scaling)** 직접 시연 + **BNN 관계**(onset 주파수 ~ dc σ). *개념*: σ(ω) 분산은 *온도로 평행이동*하는 보편 곡선 — 우리 Arrhenius(σ vs 1/T)의 *주파수영역 짝*. |
| **4** | 여러 장벽 분포 p(E) 5종에 대한 ac σ̃ vs 스케일 주파수 → 거의 한 곡선. EMA 실선, slope-1 점선. | **ac 보편성** — *장벽 분포의 형태와 무관*하게 같은 곡선. *개념*: "*어떤* 무질서든(분포 형태 무관) 같은 σ(ω) 보편성" → 무질서 *세부*보다 *percolation 병목*이 지배. |
| **5** | (Na₂O)ₓ(GeO₂)₁₋ₓ glass 실험 ac 데이터(x=0.003–0.1, open) vs RBM-보편성 예측(full) + DCA. | **실험 검증** — 피팅 파라미터 없이 준보편성 재현. *개념*: RBM이 *실제* 유리 ac 전도를 잡는다 = "보편 vocabulary"의 실증(단 noncrystal glass — 우리 결정질엔 직접 적용 아님). |

## 6. Post-processing / 분석 도구 ★

> 우리 BVSE/NEB/Bader/COHP/grand-potential과 *대응물*은 다음(이론적 분석 장치):
- **percolation 분석**: 장벽을 작은 것부터 표시 → 무한 cluster 출현 임계 → cluster 위 최대 장벽 추출 = dc Ea. (우리 site-percolation·migration network 분석의 *수송 이론* 짝.)
- **σ(ω) 스케일링**: σ'(ω, T)를 무차원 (σ̃, scaled ω)로 변환 → master curve 붕괴(collapse) 확인 = 시간-온도 중첩 검증. (우리 Arrhenius collapse의 주파수영역 확장.)
- **EMA / DCA**: 격자 hopping의 평균장/cluster 근사로 σ(ω) 해석곡선 산출(Fig 4 실선).
- **BNN 관계**: onset 주파수와 dc σ의 비례 — ac/dc 일관성 진단.
- **수치화·기록 방식**: log₁₀σ̃ vs log₁₀(scaled ω); log₁₀σ' vs log₁₀ω(β별); percolation cluster 그림(Fig 2). 모두 *무차원/스케일* 표현.

## 7. ★★ "우리 연구로의 연결" (CONNECTION TO OUR WORK) — vocabulary-only, 검증 아님

> **이 문단이 사용자가 이 논문을 남긴 이유다.** site-percolation 논문이 "Li가 *어디로 갈 수 있나*(기하·연결성)"를 준다면, 이 논문은 "Li가 *어떻게 hop하나*(σ(ω)·Arrhenius Ea·Haven 비)"의 **표준 어휘**를 준다. **단 argyrodite는 *결정질*, 이 논문은 *noncrystals* → 전이는 *disorder + concerted-hop 개념*으로만, *수치로는 절대 아님*.**

### 7.1 우리 argyrodite는 어느 hopping regime인가? — **correlated/concerted, *not* independent**
우리 li_transport.json·AIMD가 말하는 사실:
- **Haven 비 H_R = D*/D_σ ≈ 0.3–0.7 (<1)** — SE 일반(우리 method_notes 명시). H_R<1 = **correlated/concerted motion**(여러 Li가 *함께* 움직임), *independent*(비상관) hopping 아님.
- 우리 σ_NE는 **H_R=1(비상관) 가정의 *보수적 하한*** — 실제 intrinsic σ = σ_NE/H_R 은 *더 높다*.

이 논문의 hopping-model 언어로 번역:
- **RBM의 *비상호작용*(non-interacting) 가정 = "independent hopping"의 극단** — Coulomb·self-exclusion·correlation을 *전부 끈* regime. 우리 Li⁺는 정확히 그 반대편(correlated/concerted)에 있다.
- 따라서 우리 argyrodite는 **RBM이 *명시적으로 미해결로 남긴* 영역(§6 한계 #1: "Coulomb + self-exclusion을 넣으면?")** 에 속한다. RBM은 우리에게 *baseline 어휘*(percolation 병목·Arrhenius Ea·σ(ω) 중첩)를 주지만, 우리 H_R<1·concerted 운동은 **RBM이 *아직 못 푸는* 보정**이다.
- **"jump-relaxation / correlated hopping" 그림이 우리 Ea·Haven에 주는 말**: correlated hopping(한 Li의 hop이 이웃 Li의 *후속 relaxation*을 유발 = jump-relaxation, Funke 계열 — 이 논문은 RBM으로 같은 보편현상을 설명)에서, *겉보기* dc Ea는 *단일 hop 장벽*이 아니라 **percolation 병목 + 이웃 재배열의 *유효* 장벽**이다. 우리 AIMD Ea(comp1 0.253 / modelc 0.224 eV)는 *correlated* 궤적의 유효 Ea이고, H_R<1은 그 correlation의 직접 지표 → **둘은 같은 "협동 hopping" 동전의 양면**으로 *서술*된다(이 논문이 준 어휘로).

### 7.2 intra-cage vs inter-cage hopping ↔ percolation 병목 (Liu2013 멘탈모델과의 결합)
우리 argyrodite Li 전도의 mental model(Liu2013 analogy entry + GG Fig 1e,f):
- **intra-cage hop**(PS₄-cage *내부* doublet/triplet 회전·국소 jump) = 빠른·작은 장벽 — 이 논문 §3의 "대부분의 hop은 작은 장벽을 선호"에 대응.
- **inter-cage hop**(cage *사이* 장기 이동, 그 "창(window)"이 율속) = **rate-limiting 장기 hop** — 이 논문 §3·Fig 2의 **"무한히 멀리 가려면 반드시 넘어야 하는 percolation cluster 위 최대 병목 장벽"** 에 *정확히* 대응.
- 즉 **inter-cage hop = dc Ea를 정하는 percolation 병목** 이라는 *서술*이 자연스럽다: intra-cage가 아무리 빨라도 dc σ(장거리 전도)는 inter-cage 병목이 율속. 우리 D(600K) 차이(comp1 3.09 vs modelc 7.90e-6)·Ea 차이(0.253→0.224)는 "Cl-rich disorder가 inter-cage *병목 장벽*을 낮춘다"로 *말로* 설명된다.
- **Liu2013(창 크기 → trap-vs-cross 장벽) + Dyre(percolation 병목 = dc Ea)** 를 합치면: *inter-cage 창이 좁으면(병목 장벽 큼) → percolation 병목이 높아 dc Ea↑·σ↓; 창이 넓으면 → 병목 낮아 σ↑*. 두 외부 멘탈모델이 같은 결론으로 수렴(둘 다 *검증 아님*, 서술용).

### 7.3 cascade dopant effects (Nd σ-drop)를 hopping-model 언어로
우리 li_transport.json의 Nd2O3-doped 결과:
- **σ300 ratio(nd/modelc) = 0.52**, D ratio 0.62 — Nd³⁺ + O@PS4가 Li 이동도를 떨어뜨림.
- 분해: **D0 prefactor 0.65 × n_Li carriers 0.90 × Ea factor 0.88**(Ea 0.224→0.227, 사실상 *불변*). **지배 = D0 prefactor 감소**("Nd가 Li 경로를 좁히고/attempt-frequency를 낮춤"), Ea barrier는 거의 안 변함.

hopping-model vocabulary로:
- 이 논문 frame에서 **dopant가 inter-cage 병목 *위/근처*에 앉아 percolation cluster의 *최대 장벽을 올리거나 경로를 좁히면***, 두 방식으로 σ를 떨어뜨릴 수 있다: (i) **Ea↑**(병목 장벽 자체가 높아짐 → Arrhenius slope↑) 또는 (ii) **prefactor/연결성↓**(병목 *수·경로 단면*이 줄어 attempt frequency·percolation 강도↓).
- 우리 Nd 결과는 **(i)이 아니라 (ii) — prefactor-dominant** 다. 즉 **"Nd는 *병목 장벽 높이*는 거의 안 바꾸고, 대신 percolation 경로/창을 *좁혀*(prefactor·연결성↓) σ를 0.52×로 떨군다"** 가 이 논문 어휘로 본 가장 정확한 서술. ← 이는 Liu2013 `dopant_blocking_fraction`("dopant가 창을 좁힌다")과 *같은 방향*이고, Dyre의 percolation 언어로는 "병목을 막되 *Ea가 아니라 경로 단면*으로 막는다"가 된다.
- **σ(ω) 함의(가정적 서술)**: 만약 우리가 ac 전도(분산)를 본다면, Ea를 거의 안 바꾸는 prefactor-blocking은 *master curve의 형태(중첩·지수)는 보존*하되 *scale만 내릴* 것이라 *예상*된다(RBM 중첩 논리) — 단 이건 우리가 *계산하지 않은* ac 영역의 *추정*이며, 결정질 argyrodite엔 RBM 중첩이 *그대로* 성립한다는 보장 없음(§10).

### 7.4 disorder가 Ea를 낮춘다(우리 disorder_ensemble) ↔ "넓은 분포 → percolation Arrhenius"
우리 disorder_ensemble_2026_06_09: 거의 *ordered* comp1은 600–800 K에서 *얼어붙어* Ea가 인위적으로 폭발(1.17 eV, 저온 undersampling artifact)하지만, **현실적 Cl/S anti-site disorder를 넣으면 Ea = 0.177 eV**(실험 LPSCl 범위)로 내려간다.
- 이 논문 §3의 핵심 명제 — **"넓은 장벽 분포일 때*만* percolation이 단일 병목을 골라 Arrhenius dc가 나온다; 분포가 좁으면(=ordered) 오히려 Arrhenius가 무너진다"** — 와 *정성적으로 정합*: ordered(좁은 분포)는 운동학적으로 *접근 불가*(얼어붙음)이고, disorder(넓은 분포)가 *접근 가능한* percolation Arrhenius 전도를 *연다*. 우리 결과를 *서술*하는 정확한 어휘.
- **단 방향 주의**: 이 논문은 "넓은 분포 → *Arrhenius가 성립*"을 말하지 "넓은 분포 → *Ea가 낮다*"를 직접 말하진 않는다. 우리 disorder→Ea↓(Minafra/Kraft narrative)는 *추가* 물리(disorder가 병목 장벽 *값* 자체를 낮춤)이고, Dyre는 *Arrhenius성*만 보증. **"Dyre가 disorder→Ea↓를 증명"이라 말하면 과대.**

### 7.5 σ_NE 절대값이 실험보다 높은 것 ↔ Haven은 *반대 부호* (재확인)
우리 method_notes 강조: σ_NE(H_R=1)가 실험 펠릿보다 3–5× 높은 건 (1) UMA D* overshoot + (2) bulk vs pellet(미세구조 저항) 때문이고, **Haven은 *반대* 부호**(실제 H_R<1 → intrinsic σ=σ_NE/H_R *더 높음*). 이 논문의 RBM은 *bulk 단결정 격자*(미세구조 없음)이므로 RBM도 우리 σ_NE처럼 *device보다 높은 잠재 σ*를 줄 뿐, "*실험보다 왜 높나*"를 설명하지 않는다. → **Haven/correlation은 σ *해석 어휘*이지 over-experiment overshoot의 원인이 아님**을 RBM 관점에서도 재확인.

## 8. 적용 인사이트 (우리 연구에 — vocabulary 채택)

1. **"우리 argyrodite는 correlated/concerted-hopping regime(H_R<1)이고, 이는 RBM이 *비상호작용*으로 끈 영역(§6 한계 #1)이다"** — Li 전도 서술 시 표준 문장. RBM = *independent* baseline, 우리 = *correlated* 보정.
2. **"inter-cage hop = percolation 병목 = dc Ea 율속"** 어휘 확정 — intra-cage(빠름) vs inter-cage(율속 병목)을 Dyre §3·Fig 2 언어로 *말로* 설명(Liu2013 창-크기 멘탈모델과 결합). 우리 site-percolation 짝의 *수송* 짝.
3. **Nd σ-drop(0.52×) = "Ea가 아니라 percolation 경로/prefactor를 막는 blocking"** — Dyre 어휘로 "병목 장벽 높이 불변, 경로 단면↓"으로 서술(우리 prefactor-dominant 분해와 일치). dopant blocking의 두 모드(Ea-mode vs prefactor/connectivity-mode) 구분에 RBM percolation 언어 차용.
4. **disorder→Arrhenius성**(우리 disorder_ensemble의 ordered-frozen→disordered-Arrhenius)을 Dyre §3("넓은 분포 → percolation 단일 병목 → Arrhenius")로 *정성* 정당화. 단 disorder→Ea↓는 *추가* 물리(Dyre 밖).
5. **σ(ω) 시간-온도 중첩·BNN**은 *우리가 아직 안 본 ac 영역*의 표준 예측 — 향후 우리가 impedance/ac를 본다면 비교 틀로 비치(현재는 dc/Arrhenius만).

## 9. 인용 가능 문장 (vocabulary framing 전용 — "materials comparison"으로 인용 금지)

- *(개념 어휘로만)* "In the hopping-transport picture for disordered conductors (Dyre & Schrøder), the long-range dc activation energy is set by the *largest bottleneck barrier on the percolation cluster* — for argyrodite this is the *inter-cage* hop, while fast *intra-cage* motion does not limit dc σ. (Conceptual vocabulary only: the model treats *noncrystals* with *non-interacting* carriers, whereas argyrodite is crystalline and our Li⁺ are *correlated/concerted*, H_R≈0.3–0.7<1.)"
- *(개념 어휘로만)* "Our Nd-doping σ drop (0.52× at 300 K) is, in hopping-model language, a *connectivity/prefactor* blocking — the bottleneck barrier height (Ea 0.224→0.227 eV) is essentially unchanged while the percolation pathway is narrowed — rather than an Ea-raising barrier effect."
- *(논문 자체)* "The random barrier model reproduces, with *no fitting parameters* (in scaled variables), the four universal features of disordered-solid ion conduction — Arrhenius dc σ, sub-unity power-law σ(ω), time-temperature superposition, and quasi-universality — with *percolation* (a single bottleneck barrier on the percolation cluster) as the common origin."

## 10. 주의/한계 (over-claim 방지) — **비판적으로**

- **결정질 vs 비결정질**: 이 논문은 *noncrystals*(유리·고분자·비정질). **argyrodite는 결정질** — RBM의 보편성(σ(ω) 중첩·물질-무관)이 결정질에 *그대로* 성립한다는 보장 없음. **수치 전이 0**; 개념(percolation 병목·correlated hopping 어휘)만.
- **RBM은 *비상호작용*(Coulomb·self-exclusion·correlation OFF) 최소 모델** — 우리 Li⁺(상호반발·자리 점유·concerted, H_R<1)는 RBM이 *명시적으로 미해결로 남긴*(§6 #1) 영역. **RBM이 우리 correlated 운동을 *푼다*고 말하면 틀림** — baseline 어휘일 뿐.
- **"disorder → Ea↓"는 Dyre가 증명하지 않음**: Dyre는 "넓은 분포 → *Arrhenius성*"만 보증. 병목 장벽 *값*이 disorder로 *낮아진다*는 우리(Minafra/Kraft) narrative는 *추가* 물리. 혼동 금지.
- **σ_NE over-experiment는 Haven으로 설명 안 됨**(반대 부호) — RBM 관점에서도 동일. Haven/correlation = σ *해석 어휘*이지 overshoot 원인 아님.
- **준보편성**: 저자 스스로 Fig 5에서 데이터가 *완전* 동일하진 않아 "universality"보다 "quasi-universality"라 함 — 이 모델의 *근사성*을 정직히 인정. 우리도 "정확한 정량 도구"가 아니라 "정성 어휘"로만 인용.
- **NCL 등 일부 현상은 대안 설명 존재**(ref 24–25) — RBM이 유일 정답 아님.
- **단위·양 무관**: 이 논문 무차원 σ̃·scaled ω·p(E) vs 우리 eV·S/cm·Li. **절대 같은 표·"일치"로 인용 금지.**

## 11. 기법 용어 미니사전

- **Hopping conduction**: 이온/전자가 자리 사이를 열활성 *도약(hop)*으로 이동하는 전도. 무질서 고체의 표준 그림.
- **RBM (random barrier model)**: 단순입방 격자 + *비상호작용* 입자 + *등에너지* 자리 + link별 *무작위 장벽*. 이온전도의 "이상기체 모델"(Dyre).
- **Random-energy model / Miller–Abrahams**: 자리 *에너지*가 무질서한 경우(RBM은 *장벽*만 무질서). 본문 §6에서 "RBM을 자리에너지 무질서로 일반화"가 미해결 문제로 언급.
- **VRH (variable-range hopping, Mott)**: 저온에서 가까운 높은 장벽보다 *먼* 낮은 장벽으로 뛰는 게 유리해지는 regime(전자계 표준). 본문은 명시 안 하나 같은 hopping 계보.
- **Percolation (스미기)**: 무작위로 link를 표시할 때 *무한 cluster*가 처음 생기는 threshold 현상(Broadbent–Hammersley 1957). **dc Ea = percolation cluster 위 최대 병목 장벽**(이 논문 핵심).
- **Percolation cluster / bottleneck barrier**: 전류를 나르는 무한 연결망 / 그 위에서 *반드시* 넘어야 하는 가장 큰 장벽(=율속).
- **dc / ac conductivity**: 직류(장거리, ω→0) / 교류(주파수 ω, 단거리 분산) 전도도. σ(ω)=σ' (실수부).
- **Time-temperature superposition (scaling)**: σ(ω,T)가 무차원화하면 *하나의 master curve*로 붕괴(온도=평행이동). RBM이 재현.
- **(Quasi-)universality**: 서로 다른 무질서 고체가 거의 같은 ac 응답. "준"보편성 = 근사적.
- **BNN (Barton–Nakajima–Namikawa) relation**: ac onset 주파수 ∝ dc σ. ac/dc 일관성.
- **NCL (nearly constant loss)**: 저온/고주파에서 σ(ω) 지수≈1(손실 거의 일정) 영역.
- **EMA / DCA**: effective medium approximation / diffusion cluster approximation — 격자 hopping σ(ω)의 평균장/cluster 해석 근사.
- **Jump-relaxation (Funke)**: 한 ion의 hop이 이웃의 *후속 재배열(relaxation)*을 유발 = correlated hopping. 본문이 RBM으로 같은 보편현상을 설명(Funke 계열 모델의 대안/보완).
- **Haven ratio H_R = D*/D_σ**: tracer 확산 D*와 전도도 확산 D_σ의 비. H_R<1 = correlated/concerted 운동(우리 SE ≈0.3–0.7). RBM의 *비상호작용* 극단은 H_R=1(비상관).
- **fluctuation–dissipation**: 평형 요동(영-장 MSD)과 응답(σ)의 관계 — 본문이 dc σ를 영-장 MSD로 환원하는 근거.

---
*(EXTERNAL / theory framework. argyrodite 물성 4축에 *수치로* 넣지 않음 — comparison_vs_ours.md 축 A에 framework note 한 줄로만. §7 연결은 *vocabulary-only*, 검증·수치 전이 0. RBM = noncrystals·비상호작용 최소 모델 ↔ 우리 = 결정질·correlated.)*

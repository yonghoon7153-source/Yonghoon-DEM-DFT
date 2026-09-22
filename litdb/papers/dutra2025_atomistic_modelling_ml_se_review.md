<!-- digest 표준 양식 (paper-level STANDALONE).
     2026-09-22 초판. 1저자 지정 읽기축 = 「우리 방법이 이 필드 표준 문서에서 어디에 놓이나」 7문.
     ★ 이 digest 의 제일 값있는 소득은 "리뷰가 말한 것" 이 아니라 **리뷰가 말하지 않은 것**이다 (§3-0). -->

# Understanding solid-state battery electrolytes using atomistic modelling and machine learning — Dutra, Goldmann, Islam & Dawson (*Nature Reviews Materials* **10**, 566–583 (2025))

> slug `dutra2025_atomistic_modelling_ml_se_review` · DOI `10.1038/s41578-025-00817-y` · type `리뷰 (자체 계산 0 · 자체 실험 0 — 전량 2차 인용)` · PDF `litdb/inbox/128. NatRevMater_2025_Dutra_Islam_Dawson_Understanding_SSB_electrolytes_atomistic_modelling_ML_REVIEW_MAIN.pdf` (본문 14 pp + 참고문헌 4 pp · **SI 없음** · 그림 **6장** · 표 **0장** · refs **252**) · 온라인 **2025-06-24** · digested `2026-09-22` · status ✅ · 태그 **[외부·리뷰·필드표준]**

> elements: Li, Na, P, S, Cl, Br, I, O, F, N, La, Zr, Ti, Ge, In, Y, Al, Sc, Ta, Nb, Sn, Sb, Hf, Mg, Ca, Zn, Er
> methods: DFT, AIMD, MD, MLIP, NEB, DOS, PDOS, ESW

> **저자**: Ana C. C. Dutra¹, Benedek A. Goldmann², **M. Saiful Islam**\*³⁴, **James A. Dawson**\*¹⁴ — ¹Newcastle Univ. 화학 · ²Univ. of Bath 화학 · ³**Univ. of Oxford** 재료 · ⁴**The Faraday Institution**. 교신 `saiful.islam@materials.ox.ac.uk` / `james.dawson@newcastle.ac.uk`
> 🎤 관련 발표: **없음** — `litdb/talks/*.md` 인입 대기열(`lee2026_skku_mlip_materials_design` §99-10, 6건)에 이 논문은 **없다**(2026-09-22 확인). 역링크 불필요.

---

## 0. 이 digest 를 읽는 법 — ⚠ 먼저 읽을 경고

이 편은 **Islam·Dawson 그룹의 *Nature Reviews Materials* 리뷰**라서 "필드 표준 문서" 로 취급하고 싶어진다.
그건 맞다. **하지만 우리가 물으려던 7문 중 4문에 이 리뷰는 답을 갖고 있지 않다.** 그리고
답이 없다는 사실 자체가 우리에게 제일 중요한 정보다. 순서를 지켜 읽어라:

1. **§3-0 「이 리뷰에 *없는* 것」 을 먼저 본다.** MSD 창 · 불확실도 · 검증 사다리 · 파운데이션
   모델 — 전부 **전문 0회**다. 이 리뷰를 우리 규약의 외부 근거로 인용하려던 계획은 **여기서 끝난다.**
2. **§3-3 · §7a (hull 기반 ESW 비판)** 가 이 편에서 우리에게 실제로 값있는 곳이다.
3. **§7c (`Fig. 5b` 는 이미 우리가 가진 [Zhu15] 의 재수록이다)** — 새 앵커로 착각하지 마라.
   대신 **우리 픽셀 판독 규약이 ±0.05 V 로 검증됐다**는 부수 소득이 있다.
4. **§10-④ (`Fig. 3b` 스케일 기준)** 가 제일 아픈 대목이다. 우리 MLIP-MD 가 이 리뷰의
   *MLIP* 칸이 아니라 *AIMD 참조데이터* 칸에 앉아 있다.

⛔ **이 리뷰에는 DFT 파라미터가 한 줄도 없다** — `k-point`·`cutoff`·`PBE`·`VASP`·`pseudopotential`
전문 **0회**(§4). 방법 재현 목적으로 인용할 수 없다.

---

## 1. 한 줄 요약

무기 결정질 고체전해질(산화물·황화물·할라이드, Li계+Na계)을 **① 빠른 이온전도 기전 ② 상형성/안정성/분해
③ 계면** 세 축으로 나눠 원자단위 계산 문헌 252편을 정렬한 **개념 지도형 리뷰**다. 계산 방법론 절(§Materials
modelling and ML methods)은 **4쪽 중 1.5쪽**이고, ML 은 **"AIMD 로 만든 데이터로 전용 퍼텐셜을 피팅해
더 큰 셀·더 긴 시간을 돌린다"** 는 2020년대 초반 서사에서 멈춘다 — **범용 파운데이션 모델(UMA·MACE-MP·
CHGNet·M3GNet·SevenNet)은 한 번도 등장하지 않는다.**

우리에게 남는 실질 소득은 세 가지뿐이다:
- **`Fig. 3b` 의 스케일 기준** — *reference data = DFT/AIMD **<500 원자*** → *ML potentials = **>10,000 원자 · >1 ns***.
  우리 UMA-MD(**558 원자 · 200–400 ps**)는 **오른쪽 칸이 아니라 왼쪽 칸**에 앉는다.
- **hull/분해산물 기반 ESW 의 구조적 한계를 이름 붙여 준다** — 운동학 부재 + *"분해산물 생성에너지로
  창을 예측하면 관측값을 **과소평가**할 수 있다"* + Schwietert 의 **간접 경로(탈리튬 중간상)** 논증.
- **`Fig. 4c`(Morgan 2021)** — 아지로다이트에서 **음이온 자리무질서가 Li 하부격자를 풀어 cage 간
  경로를 잇는다**는 기전 도식. 우리 disorder-ensemble MD 의 개념적 정당화.

---

## 2. 메타 / 이 리뷰가 스스로 그은 범위

| 항목 | 내용 |
|---|---|
| 범위 **안** | 무기 **결정질** 고체전해질 (Li·Na), 원자단위 계산(DFT/AIMD/FF-MD/MLIP) + ML 스크리닝 |
| 범위 **밖** (저자 명시) | 실험적 특성분석 · 실제 디바이스 · **메조/연속체 스케일** · **폴리머/하이브리드** — "available elsewhere⁴⁻⁹,¹⁴⁻²¹" |
| 자체 계산 | **0건** |
| 자체 실험 | **0건** |
| 그림 | 6장 (전부 재수록 또는 개념 도식). `Fig. 1`·`Fig. 3` 만 저자 자작 도식 |
| 표 | **0장** |
| 구조 | Introduction → Fundamentals → 재료군(산화물/황화물/할라이드) → **방법** → **① 수송기전** → **② 상형성·안정성** → **③ 계면** → Future perspectives |

**저자 진영**: Islam(Oxford) + Dawson(Newcastle) 은 **입계(GB)·안티페로브스카이트·포텐셜 기반 MD** 계보다.
리뷰의 무게중심이 거기로 쏠린다 — **GB 절이 유난히 두껍고**(ref 29, 196, 220, 230–236),
반대로 **황화물 아지로다이트는 21줄 한 문단**이다. 우리 계가 중심이 아니다.

---

## 3. ★★ 1저자 지정 7문에 대한 직답

### 3-0. ⛔ 먼저 — **이 리뷰에 아예 없는 것** (전문 문자열 검색, 본문 14 pp)

| 우리가 찾던 것 | 전문 등장 횟수 | 판정 |
|---|---|---|
| `mean square displacement` / `MSD` | **0** | ⛔ MSD 창 규약 **없음** |
| `Haven` | **0** | ⛔ Nernst–Einstein 보정 규약 **없음** (⚠ *참고문헌*엔 있다 — ref 140 Marcolongo & Marzari) |
| `uncertainty` / `error bar` | **0** | ⛔ 불확실도 보고 규약 **없음** |
| `foundation` / `universal` / `MACE` / `CHGNet` / `M3GNet` / `GNoME` / `UMA` | **0** | ⛔ 파운데이션 모델 **언급 0** |
| `phonon` | **0** | ⛔ (`quasiharmonic approximation` 만 1회, ref 206) |
| `extrapolation` | **0** | — |
| `radial distribution function` | **1** | "MD 는 구조 정보도 준다" 예시 한 마디뿐 |
| `validation` 어근 | **3** | 전부 **한 문장짜리 훈계** (§3-2) |
| `k-point`·`cutoff`·`PBE`·`VASP`·`pseudopotential` | **0** | ⛔ DFT 파라미터 **0줄** |

> 🔑 **이 표가 이 digest 의 제1 소득이다.** *Nature Reviews Materials* 2025 가 이 필드를 정리하면서
> MSD 창·UQ·파운데이션 모델을 **한 번도 안 다룬다**는 것은 두 가지 중 하나를 뜻한다 —
> (a) 그 문제들이 아직 "리뷰에 실릴 만큼" 정착하지 않았거나, (b) 이 리뷰의 관심이 기전·재료 쪽이라서다.
> 우리 판단은 **(a)+(b) 둘 다**이고, 그렇다면 **우리 규약의 외부 근거는 이 편이 아니라
> 이미 litdb 에 있는 전용 편들**(`maginn2019…` · `mccluskey2025…` · `zaby2026…` · `grasselli2025…` ·
> `makino2026…`)이다. **이 리뷰를 그 자리에 인용하면 틀린다.**

---

### 3-1. ⭐ MSD 창·확산영역 판정 관례 — **이 리뷰는 규정하지 않는다**

**리뷰가 실제로 말하는 전부** (§Interatomic-potential-based methods, p. 571):
- *"The chosen timestep for an MD simulation must be shorter than the typical time associated with
  important processes, such as an atomic vibration, with values of **1 or 2 fs** often used."*
- *"Substantial computing resources are required to run MD simulations that provide **reliable
  statistics** that can be directly compared with experimental results⁹¹."*
- *"potential-based MD simulations can easily reach the **nanosecond** timescale with simulation boxes
  containing **tens of thousands of atoms**."*

즉 **dt 규약(1–2 fs)만 있고, 적합 구간(fit window) 규약은 없다.** "reliable statistics" 의 내용은
각주 **ref 91 = He, Zhu, Epstein & Mo, *npj Comput. Mater.* **4**, 18 (2018), "Statistical variances of
diffusional properties from AIMD"** 로 **위임**되고, MD 확산 분석 절차는 **ref 92 = de Klerk, van der Maas
& Wagemaker** 로 위임된다.

**우리 2–50 ps 창의 정당성 판정**:
- ✅ **dt 2 fs 는 리뷰 표준 그대로**다.
- ⚠ **창 자체는 이 리뷰로 정당화되지 않는다.** 정당화의 출처는 여전히 우리 내부 규약 + 이미 digest 한
  `maginn2019_best_practices_transport_selfdiffusivity_viscosity`(*"D 의 적합 구간 선택에는 객관적 기준이
  아직 없으니, 고른 방법과 그 선택이 만드는 변동폭을 반드시 보고하라"* §5.2.3)다.
- 🔴 **사용자가 본 0.4–1.9 ns 창과의 대조**: 이 리뷰는 그 대조에 쓸 수 없다. 대신 **간접 압박**을 준다 —
  리뷰가 "MLIP-MD 는 **ns** 스케일" 이라고 못박으므로, **ns 궤적에서 0.4–1.9 ns 창을 쓰는 것이
  리뷰가 가정하는 전형**이고, **200 ps 궤적에서 2–50 ps 창을 쓰는 우리**는 그 전형의 **1/5 스케일**에서
  같은 *비율*(창 ≈ 궤적의 10–25 %)을 쓰고 있는 셈이다. ⇒ **창/궤적 비율은 정합, 절대 길이는 미달.**
  🔑 이 프레이밍이 우리가 쓸 수 있는 유일한 정직한 문장이다.
- ⛔ **`ref 91`(He/Mo 2018)은 아직 우리 litdb 에 없다** — §11 구해야 할 논문 #1.

---

### 3-2. ⭐ MLIP 검증 사다리 — **사다리가 없다. 훈계 두 문장이 전부다**

리뷰의 검증 관련 진술 **전문**:
1. (`Fig. 3b` 워크플로 2단계) *"ML potentials are **validated** and then applied for MD simulations…"*
   — 무엇을 검증하는지 **안 말한다**.
2. (§ML approaches) *"the accuracy of these models depends upon the quality and diversity of the
   training data; for example, **special care is needed to make sure that ion diffusion hops and
   pathways are appropriately sampled**."*
3. (§Future perspectives) *"special care is required to make sure that there is diverse and appropriate
   sampling in the training configurations, and that there is **rigorous validation of the accuracy of
   the fitting**; indeed, without appropriate training data, the old adage **'garbage in, garbage out'** applies."*

**⇒ "fitting 의 정확도" 수준에서 멈춘다.** RDF·VDOS·상전이 온도·포논 같은 **성질 수준(property-level)
검증 목록을 이 리뷰는 제시하지 않는다.**

**우리 RDF 0건 · VDOS 0건 · 상전이T 0건 이 얼마나 큰 결손인가 — 판정**:
- **이 리뷰 기준으로는 결손이 아니다.** 리뷰가 요구하는 것은 "학습 데이터에 확산 홉이 포함됐는가" 뿐이다.
- 🔴 **그러나 이 리뷰 기준을 방패로 쓰면 안 된다.** 우리 litdb 의 **더 최신·더 전문적인 편들이 정확히
  반대로 말한다**:
  - `makino2026_mlip_battery_materials_review` §3.5–3.7 — *정적 오차는 내삽 정확도일 뿐이고, 안정한 MD 를
    보증하는 힘-오차 문턱은 존재하지 않으며, **검증은 성질 수준(장벽·아레니우스 기울기·포논·RDF)에서
    따로 해야 한다***.
  - `chang2026_performance_based_mlip_selection_sse` — 정적 지표로는 5개 모델이 **구분이 안 되고**
    동역학(에너지 드리프트)에서만 갈린다.
  - `wang2025_pretrained_deep_potential_sulfide_sse` — 범용 MLIP 가 **안장점 에너지를 과소평가**해
    황화물 σ 를 **1–2 자릿수 과대평가**한다.
- ⇒ **정확한 문장**: *"우리 RDF/VDOS 결손은 **이 필드 표준 리뷰가 요구하는 수준은 넘지만**,
  **MLIP 전문 문헌이 2026 년에 요구하는 수준에는 미달**한다."* 리뷰가 낡은 쪽이다.
  ⛔ **"Nature Reviews 도 RDF 를 요구 안 한다" 를 면죄부로 쓰지 마라** — 그 리뷰는 ML 방법론 전문지가 아니다.

---

### 3-3. ⭐⭐ hull 기반 계면·ESW 스크리닝을 어떻게 평가하나 — **여기가 이 편의 본전이다**

리뷰는 우리 §B 방법의 **원전 두 편을 모두 이름으로 인용**한다:
- **ref 217 = Richards, Miara, Wang, Kim & Ceder, *Chem. Mater.* **28**, 266–273 (2016)** → 우리 `[Rich16]`
  *"In a **pioneering** DFT study²¹⁷, a methodology was developed to examine the thermodynamics of formation
  of solid electrolyte interfacial phases and therefore establish electrochemical windows. **Thiophosphate
  electrolytes were predicted to have especially narrow electrochemical stability windows**, and several
  known electrolytes were found to be inherently stable but reactive with electrodes, with the potential
  to form **passivating but ionically conducting barrier layers**."*
- **ref 216 = Zhu, He & Mo, *ACS AMI* (2015)** → 우리 `[Zhu15]`. `Fig. 5b` 가 이 논문에서 왔다.

**그리고 곧바로 한계를 명명한다** (p. 576, 원문 그대로):

> *"For many solid electrolytes, **predicting the electrochemical stability window by using the formation
> energies of the solid electrolyte decomposition products may underestimate observed values**²¹¹,²¹⁶⁻²¹⁸.
> As the **kinetic barriers for decomposition reactions are not considered** in thermodynamic
> investigations, elucidating the mechanisms related to the decomposition of solid electrolytes is challenging."*

이어서 **두 겹의 더 날카로운 지적**:

| # | 지적 | 출처 | 우리에게 |
|---|---|---|---|
| **(i)** | 분해 경로가 **직접적이지 않고 *간접***이다 — SE 의 **(탈)리튬화 중간상**을 거쳐 더 안정한 분해산물로 간다. *"Consequently, the electrochemical stability window is **usually wider** than that determined by solely considering the stability of the decomposition products."* | **ref 211 = Schwietert et al., *Nat. Mater.* **19**, 428–435 (2020)** (아지로다이트·가넷·NASICON 실측 + DFT + XRD + ssNMR) | 🔴 **우리 2.256 V 는 하한이라는 판정의 *두 번째* 근거.** 종전 근거([Xiao20Rev] *"worst-case scenario"*)는 "운동학이 빠져서" 였는데, 이건 **열역학 안에서도** 경로 선택 때문에 창이 넓어진다는 더 강한 지적이다 |
| **(ii)** | *"the electrochemical stability windows are **not always controlled by the decomposition products** but instead often arise from the **intrinsic stability of the solid electrolyte itself**"* (`Fig. 5c`: 상분리 = 핵생성 장벽 있는 이중우물 / 고용체 = 장벽 없는 단조 하강) | **ref 218 = Schwietert, Vasileiadis & Wagemaker, *JACS Au* **1**, 1488–1496 (2021)** | 🔴 **우리 방법의 전제를 정면으로 건드린다.** grand-potential 은 *분해산물 조합의 최저 에너지*로 창을 정의한다 — (ii) 는 **그 정의 자체가 옳은 보고량이 아닐 수 있다**고 말한다 |

**§B 방법 한계 — 리뷰가 지적하는 것 총정리 (4가지)**
1. **운동학(핵생성 장벽) 부재** — 이미 우리 원장에 있음(`[Xiao20Rev]` worst-case, `[Famprikis19]` ±0.5 V 과전압).
2. **분해산물 기반 예측이 관측을 과소평가**(창을 좁게 준다).
3. **경로가 간접**(탈리튬 중간상 경유) ⇒ 실제 창은 더 넓다. ← **우리 원장에 없던 논거**
4. **창이 산물이 아니라 SE 자신의 고유 안정성에서 올 수 있다** ⇒ 보고량 정의 문제. ← **우리 원장에 없던 논거**

⛔ **단, ③④ 는 리뷰의 *요약*이고 원전은 Schwietert 2020/2021 이다.** 우리 원고에 쓸 땐 **원전을 인용**한다
(리뷰는 이 두 편을 각각 한 문단으로만 다룬다). → §11 구해야 할 논문 #2, #3.

📎 **이미 우리 원장에 있는 같은 방향의 비판과 이어붙일 것**:
`comparison_vs_ours.md` **§J-20** (`[Wu26MLIF]` *"볼록껍질 열역학에만 기대는 것은 모델의 현실성을 제한한다"*)
· **§J-21** (`[Guo25Kin]` 원전 확인) — **이 리뷰가 그 축의 세 번째 독립 진술**이고,
**계보상 가장 권위 있는 자리**(*Nature Reviews Materials*, Islam·Dawson)에서 나온 것이다.

---

### 3-4. 범용 foundation model 을 어떻게 보나 — **⛔ 언급 0회. 우리 UMA 선택에 문헌 근거를 주지 않는다**

리뷰의 ML 퍼텐셜 분류(§ML approaches)는 **회귀 알고리즘 3분류**에서 끝난다:
1. **인공신경망** — Behler–Parrinello(ref 108), 대칭함수 기반
2. **커널 회귀**(ref 109) — GAP, 그리고 AIMD 에 물린 **on-the-fly** 퍼텐셜
3. **선형 피팅** — **moment tensor potential**(ref 110 = Shapeev 2016 → 우리 `shapeev2016_moment_tensor_potentials`)

그리고 워크플로는 **`Fig. 3b` 3단**: *DFT/AIMD 참조데이터(<500 원자) → **전용 ML 퍼텐셜 학습** → 대규모 MD*.

> 🔴 **이 서사에는 "이미 학습된 범용 모델을 그냥 쓴다" 는 칸이 없다.** `pretrained`·`transfer`·
> `fine-tune`·`foundation`·`universal` 이 전문 0회다. 즉 **2025년 6월 *Nature Reviews Materials* 기준
> 필드의 표준 상은 여전히 "계마다 퍼텐셜을 직접 판다"** 이다.

**우리 UMA-s-1p1 선택의 문헌상 위치 — 정직한 정리**:
- ❌ **이 리뷰는 근거가 아니다.** "리뷰도 MLIP 를 권한다" → ✅ 맞다. "리뷰가 파운데이션 모델을 권한다" → ⛔ **거짓**.
- ✅ 근거는 이미 우리 litdb 안에 있다 — `liu2026_finetuning_umlip_tutorial` · `tompa2026_…` ·
  `alghamdi2026_…` · `petmad2026_…` · `chang2026_performance_based_mlip_selection_sse`(우리 계 LPSCl 에서
  범용 5종 as-is 비교) · `wang2025_pretrained_deep_potential_sulfide_sse`(**범용의 실패 모드**를 수치로).
- 🔴 **오히려 리스크 신호로 읽어야 한다**: 리뷰가 *"special care is needed to make sure that **ion diffusion
  hops and pathways are appropriately sampled**"* 라고 못박는데, **우리는 UMA 의 학습 데이터(omat)에 우리 계의
  Li 홉이 들어 있는지 확인한 적이 없다** — 파운데이션 모델을 쓰면 이 점검이 자동으로 면제되는 게 아니라
  **확인 불가능해진다**. 이게 `wang2025…`(안장점 과소평가 → σ 1–2 자릿수 과대) 가 경고한 바로 그 구멍이다.
  ⇒ 우리 **절대값 인용 금지** 정책이 이 구멍을 (우연히) 막고 있다.

---

### 3-5. σ·D·Ea 보고 관례 — **절대/상대 지침 없음. 다만 "설계 문턱" 두 개를 준다**

- **실용 문턱**(§Fundamentals): *"ensuring that the bulk solid electrolyte material has practical
  room-temperature ion conductivity (**>10⁻³ S cm⁻¹**) remains fundamental"*
- **설계원리 문턱**(§Design approaches): *"fast-ion behaviour, which is typically a room-temperature
  conductivity of **>1 mS cm⁻¹** and an **activation energy of <0.3 eV**"*
- **불확실도**: **0회**. 오차막대·복제·시드·신뢰구간 지침 **없음**. `statistics` 2회 중 1회는
  ref 91 로의 위임, 1회는 "충분한 자원이 필요하다" 는 일반론.
- **Nernst–Einstein**: 본문 **0회**, **참고문헌에만** — **ref 140 = Marcolongo & Marzari,
  *Phys. Rev. Mater.* **1**, 025402 (2017), "Ionic correlations and **failure of Nernst–Einstein relation**
  in solid-state electrolytes"**. 리뷰가 이 논문을 **본문에서 논하지 않고 인용만 한다**.

**우리 1저자 인용정책(2026-09-18, "절대값 안 쓰고 상대차만")의 외부 근거가 되는가 — 판정**:
- ❌ **직접 근거는 아니다.** 리뷰는 보고 관례를 아예 논하지 않는다.
- ✅ **간접 지지 1개**: 리뷰가 제시하는 판정 도구가 **문턱(σ>1 mS/cm, Ea<0.3 eV)** 이지 절대값 대조가
  아니다 ⇒ **"필드가 실제로 쓰는 것은 문턱 통과 여부와 계 간 순위"** 라는 우리 정책과 **방향이 같다**.
  우리 comp1 0.253 eV · modelc 0.224 eV 는 **둘 다 <0.3 eV 문턱을 통과**한다(⚠ 이건 문턱 판정이지
  절대값 인용이 아니다 — 이렇게 쓰는 것은 정책 위반이 아니다).
- ✅ **더 강한 지지는 이미 우리 litdb 에 있다** — `zaby2026_reliable_conductivity_estimates_md`
  (NE 가 1.3–2.1× 과대, 불확실도는 replica 간 산포가 지배) · `lynch2026_greenkubo_mlip_conductivity_thesis`
  (350 K 에서 모델 시드만으로 σ 4.3×) · `mccluskey2025_…`(OLS 가 자기 오차를 10–26× 과소평가).
  **이 편들이 정책의 정본이고, 이 리뷰는 아니다.**
- 🔴 **다만 리뷰가 ref 140 을 실어 둔 것은 쓸 수 있다** — *"필드 표준 리뷰조차 NE 실패 논문을 참고문헌에
  올려 둔다"* 는 우리 Haven=1 가정의 **경고 표지** 로. (⚠ 리뷰 본문 주장이 아님을 반드시 명시)

---

### 3-6. 그들이 미해결로 꼽은 과제 — **우리가 메우는 칸 3개**

`Future perspectives` 는 **3개 테마**뿐이다 (p. 578–579):

| 테마 | 리뷰의 요구 | 우리가 메우나 |
|---|---|---|
| **A. 계면·안정성** | 전해질↔전극 계면 반응·양립성 심층 이해 · **계면 저항이 충방전 중 이온수송에 미치는 영향** · 입계 저항 · ***"Further advances in **thermodynamic models for electrochemical stability and interfacial reactivity** are important to help guide intrinsic voltage limits"*** | ✅ **직접 해당.** 우리 §B(grand-potential + `InterfacialReactivity`) 가 바로 그 "열역학 모델" 이다. ⚠ 단 §3-3 의 비판 4가지를 우리가 **아직 안 고쳤다** |
| **B. 새 재료 설계·최적화** | HT 데이터 주도 도구 + 실험 · 조성변화·화학 도핑 · **⭐ *"there is **no single unified design principle** that facilitates superionic behaviour, and that **diverse design factors** can be used to optimize a particular family"*** | ⭕ 부분. 우리 cascade 도핑 스크리닝이 이 칸. ⚠ 이 문장은 **우리 서사의 방패이자 칼**이다 — §8 참조 |
| **C. ML·기법 개발** | 더 큰 계 · 학습데이터 다양성 · **엄격한 피팅 검증** · 계산↔실험 결합(**NMR·비선형광학·중성자산란**) · **멀티스케일**(원자→연속체) | ⚠ **우리가 제일 약한 칸.** 실험 결합 0 · 멀티스케일 0 · 검증 얕음 |

**🔑 positioning 에 바로 쓸 수 있는 칸 = A.** 리뷰가 **"intrinsic voltage limits 를 안내할 열역학 모델의
추가 발전이 필요하다"** 고 명시적으로 요구하는데, 우리 **Nd·O 도핑 × grand-potential onset 의 matched
factorial**(`oxidation_matched_factorial.json`, 11종)은 정확히 그 요구에 대한 응답이다.

---

### 3-7. ⭐ 선행연구 점검 — **우리 §D(Li 예산) · §2b(보호율 식) · §E(dual compatibility) 가 여기 있나**

| 우리 구성물 | 리뷰 전문 검색 | 판정 |
|---|---|---|
| **§D — Li 예산 (Li budget)** | `budget` **0회**. Li 수지/재고 개념 **0** | ✅ **선점 없음** |
| **§2b — 보호율 식 (protection ratio)** | `protect` **0회**, `passivation` **1회**(ref 217 요약 문장 안 *"passivating but ionically conducting barrier layers"* 뿐) | ✅ **선점 없음**. 정성 개념만 존재 |
| **§E — dual compatibility (양극·음극 동시 양립)** | `dual` 0회(본문). `compatibility` 3회 — 전부 **정성 서술**(Li₀.₃₈₈Ta₀.₂₃₈La₀.₄₇₅Cl₃ 의 *"excellent interfacial compatibility with lithium metal"* / "이온전도와 계면 양립성에 더해 상형성도 되어야" / Future §A). **양 끝을 동시에 점수화하는 지표 없음** | ✅ **선점 없음** |

**⚠ 다만 "인접한 경쟁 정식화" 2개는 있다 — 원고에서 차별화가 필요하다**:
- **ref 243 = Wang, Panchal, Sai Gautam & Canepa, *JMCA* **10**, 19732 (2022)** — SE 분해산물 20종+ 이
  Li/Na 금속과 만드는 계면의 **work of adhesion** 을 "계면 안정성 정량화의 핵심" 으로 제시.
  **우리 §2b(보호율)와 같은 목적, 다른 관측량.** → §11 구해야 할 논문 #4.
- **ref 208 = Sjølin et al., *Batter. Supercaps* **6**, e202300041 (2023)** — **multitarget multifidelity
  워크플로**: 이온·전자전도도 + 열역학·전기화학 안정성을 **동시에** 평가, NEB 를 대리모형으로 대체.
  **우리 cascade 와 목적이 같다.** ⚠ 단 대상은 **안티페로브스카이트**(우리 계 아님).
  📎 이미 우리 원장 **§J-22**(`[Park26ML]` 선점 판정)·**§J-12**(`[Basu26MFB]` 다중충실도)와 같은 축.

---

## 4. DFT / 계산 방법 ★ — **⛔ 이 리뷰에는 없다**

| 항목 | 내용 |
|---|---|
| 코드 | **미기재** (VASP·QE·CASTEP 전문 0회) |
| functional / vdW | **미기재** (PBE·HSE·SCAN·D3 전문 0회) |
| pseudo/PAW | **미기재** |
| k-points / ecut | **미기재** |
| supercell / nat | **개념만** — `Fig. 3b`: DFT/AIMD 참조 **<500 원자** → MLIP-MD **>10,000 원자** |
| DFT+U | **미기재** |
| AIMD | 서술만: *"computationally expensive and typically limited to **<500 ions** and timescales of **hundreds of picoseconds**"* (ref 85) |
| MD 시간간격 | **1 또는 2 fs** (유일한 정량 규약) |
| MLIP | 회귀 3분류(NN / kernel·GAP·on-the-fly / linear·MTP). **파운데이션 모델 0** |
| **무질서 처리** | ⛔ **SQS·enumeration·single-config 전부 0회.** 무질서는 *현상*(아지로다이트 음이온 무질서, `Fig. 4c`)으로만 등장하고 **계산 처리 규약은 안 준다** |
| 장거리 정전기 | ⚠ **문제로 명명**: *"Another challenge is the treatment of **long-range electrostatic interactions** by ML potentials, as … requires simulating charged species, with **possible changes in effective charge state along a diffusion path**"* (refs 106 Gao&Remsing / 107 Shaidu). **최근 2–3년 개발 중** |

> 🔴 **마지막 줄이 우리에게 직접 걸린다.** 우리 UMA-MD 는 **전하 상태를 명시하지 않는 단거리 GNN**이다.
> 리뷰가 *"확산 경로를 따라 유효 전하 상태가 바뀔 수 있다"* 를 미해결 문제로 꼽는데, 우리는 그 가정을
> 점검한 적이 없다. ⇒ **우리 D·Ea 의 계통오차 후보로 기록**(§H 정직 목록 후보).

---

## 5. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 전고체전지 도식 — 음극/전해질/양극 + 4개 난제(음극계면·입계·양극계면·이온수송) | ⛔ 활용 없음 (순수 도식). **본 digest 에서 유일하게 안 본 그림** |
| 2a | 대표 SE 결정구조 12종 (Li: garnet·perovskite·NASICON·LGPS·**argyrodite Li₆PS₅Cl**·Li₃InCl₆·Li-LaCl₃ / Na: β-alumina·NASICON·Na₃PS₄·Na₁₁Sn₂PS₁₂·Na₃ErCl₆·Na₂ZrCl₆) | 우리 계가 "12종 표준 목록" 에 이름으로 들어간다는 위치 확인용 |
| 2b | Li·Na SE 의 σ 아레니우스 (log σ −1.5 ~ −4.5 S cm⁻¹, 1000/T 2.4–4.0 K⁻¹) + **상용 액체전해질 점선**(LiPF₆–EC/DMC · NaPF₆–EC/PC) 병기. Li 계 11종에 **Li₆PS₅Br** 포함(Cl 은 없음) | **문헌 σ 지형 기준선.** ⛔ 우리 UMA σ 와 같은 표 금지(소환값·실험값). 액체전해질 점선이 "목표선" 으로 그려진다는 관례만 차용 |
| 3a | 실험(합성·회절·전기화학·분광·현미경) ↔ 모델링(ab initio·퍼텐셜·ML) → 산출물 6칸(구조·이온수송·도핑결함·안정성·계면·재료설계) | 우리 캠페인이 6칸 중 **4칸**(이온수송·도핑결함·안정성·계면)에 있고 **구조·재료설계는 약함**을 자기점검 |
| **3b** ★★ | MLIP 워크플로 3단 + **스케일 명문**: *Reference data = DFT/AIMD **<500 atoms*** → *ML potentials = MD applied to **>10,000 atoms and >1 ns*** → *Properties(수송·안정성·계면)* | 🔴 **우리 MLIP-MD 감사 기준.** 우리 = **558 원자 · 200–400 ps** ⇒ **왼쪽 칸**. §7b·§10-④ |
| 4a | 이동 기전 3종 도식 — vacancy / direct interstitial / **concerted(interstitialcy, knock-on)** | 우리 inter-cage hop 서술의 표준 어휘 |
| 4b | LLZO·LGPS·LATP 의 AIMD Li⁺ 확률밀도 (등면 6ρ₀·6ρ₀·2ρ₀; 내부 등면은 외부의 2배 밀도) | 우리 BVSE 채널 그림의 **문헌 대응물**. ⚠ 등면 기준이 *평균 확률밀도의 배수*(ρ₀)라는 관례 — 우리 iso 절대값 관례와 다름 |
| **4c** ★ | **아지로다이트 음이온 무질서 효과** (ref 162 = Morgan 2021). 좌: S/X **ordered** + Li **pseudo-ordered** → cage 안에서만 회전(**Slow**) / 우: S/X **disordered** + Li **disordered** → cage 사이를 잇는 화살표(**Superionic**) | 🔑 **우리 disorder-ensemble MD 의 개념 정당화.** "무질서 배열마다 다르게 나오는 것이 잡음이 아니라 물리" 라는 우리 규약의 그림 근거 |
| 4d | 할라이드 Li₃YCl₆(hcp)·Li₃YBr₆(fcc) 구조 + Li⁺ 확률밀도(노랑 등면) + Oct(빨강)/Tet(파랑) 경로 | 우리 계 아님 |
| 4e | fcc 산화물 Oct–Tet–Oct 경로: **face-sharing Li 없음 → 깊은 이중우물(높은 장벽)** vs **face-sharing 있음 → 얕은 단일 봉우리** | 개념(자리에너지 겹침 → 장벽↓). 우리 Cl-rich disorder 서사와 **같은 논리 계열** |
| 5a | NASICON 합성가능성 HT 깔때기: **3,881 → (E_hull − S_ideal·T ≤ 0, T = 1,000 K) 641 → (SO₄²⁻-free) 242 → (Na₃ 화학량론) 23 → (기보고 제거) 17 → 합성 8종** + 금속쌍 히트맵(최대 Mg–Hf 28) | 🔑 **깔때기 문법의 문헌 사례.** 특히 **`E_hull − S_ideal·T ≤ 0` (이상혼합 엔트로피로 hull 을 완화)** 규약 — 우리 cascade 의 hull 컷과 대조 가치. 📎 §J-10(`[Jain26Rev]` 깔때기) 에 붙는다 |
| **5b** ★★ | **계산 ESW 막대** — 빨강 = Li-이원화합물 7종, 파랑 = SE 11종. 진한색 = 고유 창, 연한색 = **완전 탈리튬까지의 연장**. 출처 **ref 216 = Zhu/He/Mo 2015** | 🔴 **§7c 참조 — 이건 우리가 이미 `[Zhu15]` 로 SI 수준까지 가진 그림의 재수록이다.** 새 앵커 아님. 대신 **우리 픽셀 판독 규약의 ±0.05 V 검증**이 됐다 |
| 5b(우) | 음극/인터페이즈/SE 를 가로지르는 **μ_Li · μ̃_Li⁺ · μ̃_e⁻** 도식 — 인터페이즈에서 μ̃_e⁻ 가 꺾여 오르고 SE 환원을 막는 그림 | 우리 SEI-gap(전자절연) 서사의 **개념 원전 도해**. 📎 `[Zhu15]` §6 과 같은 논리 |
| **5c** ★ | 분해 자유에너지 도식 2종 — **상분리**(SE → 중간체 → 산물, **핵생성 장벽** 있는 이중우물) vs **고용체**(장벽 없이 단조 하강). 출처 ref 218 = Schwietert 2021 | 🔴 **우리 grand-potential 이 못 보는 것의 그림.** 우리는 최종 산물 조합만 본다 — 중간체·장벽·고용체 경로가 전부 안 보인다. §7a·§10-② |
| 6a | 계면 3종 도식 — **Surface / Grain boundaries / Electrode–electrolyte** (각각 빨간 점선으로 관심영역 표시) | 우리 슬랩 축의 표준 분류. ⚠ 우리는 **surface 만** 있고 GB·explicit 전극계면은 0건 |
| 6b | Li₃InCl₆ 8개 면 표면에너지(0.23–0.47 J m⁻², 산포 **0.240**) vs 고엔트로피 Li₂.₈In₀.₂Sc₀.₂Yb₀.₂Lu₀.₂Zr₀.₂Cl₆(산포 **0.134**) + Wulff 형상(**층상 → 구형**) | 우리 계 아님. 다만 **"고엔트로피화 → 면간 이방성↓ → 구형 입자"** 논리는 우리 도핑 서사에 이식 가능한 *형태* 논거 |
| **6c** ★ | **입계 PDOS + 밴드갭** (ref 196 = Quirk & Dawson 2023). 막대에 값이 **인쇄**돼 있다: Li₃OCl 6.06 / Σ3{112} 5.91 / Σ5{310} **4.58** · Li₂OHCl 6.61 / 6.28 / **5.52** · **Li₃PS₄ 3.21 / Σ3{121} 2.55 / Σ5{210} 2.49** · Li₃InCl₆ 3.28 / 2.66 / **2.53** | 🔴 **우리 밴드갭 축의 경계선.** 황화물 Li₃PS₄ 가 **bulk 3.21 → Σ5 2.49 eV (−0.72 eV, −22 %)**. 우리 gap 은 **bulk 주기셀 값**이라 다결정 전자누출을 과대평가한다. §7d |
| 6d | LLZTO(001) 계면 형성에너지 — **Li −0.97 / Li₃N −1.47 / LiSi₂N₃ −1.82 J cm⁻²** (ref 239) | 우리 계 아님. ⚠ 단위가 **J cm⁻²** 로 인쇄돼 있다(통상 J m⁻²) — 인용 시 원전 확인 필요 |

> **본 digest 에서 실제로 본 그림**: `Fig. 2`, `Fig. 3`, `Fig. 4`, `Fig. 5`(+ `Fig. 5b` 600 dpi 확대),
> `Fig. 6` — **5장**. **안 본 그림**: `Fig. 1`(순수 개념 도식, 우리 축과 무관).
> ⚠ `extract_figures.py` 는 이 PDF 에서 **`Fig. 1` 만** 잘라냈다 — *Nature Reviews* 레이아웃이 캡션을
> **옆 단**(Fig 2·4·6) 또는 **다음 쪽**(Fig 5)에 두기 때문에 "캡션 위 영역" 휴리스틱이 빈 영역을 짚는다.
> 나머지 5장은 **벡터 drawing 의 union 영역**으로 다시 렌더해 `figures.json` 에 `note` 를 달아 등록했다.

---

## 6. Post-processing ★ — 리뷰가 언급하는 기법 목록

리뷰 자신은 후처리를 하지 않는다. **언급되는 기법**만 정리:

| 기법 | 등장 | 도구 | 우리 대비 |
|---|---|---|---|
| **NEB** (nudged elastic band) | 5회 — LGPS(장벽 0.15 eV, bcc 음이온골격) · LATP · LLTO 코팅(0.23–0.39 eV) · ref 208 이 **대리모형으로 대체** | 미기재 | ⛔ **우리 NEB 0건.** 우리 Ea 는 전부 MD 아레니우스 |
| **AIMD 확률밀도(probability density)** | `Fig. 4b`, `Fig. 4d` — 등면을 **ρ₀(평균 확률밀도)의 배수**로 | 미기재 | 우리 BVSE 채널%와 **다른 양** (BVSE=결합원자가 에너지면, 이건 궤적 점유밀도) |
| **PDOS / 밴드갭** | `Fig. 6c` 입계 | 미기재 | ✅ 우리 fixed-occ nscf 와 같은 양(⚠ functional 미기재라 값 비교 금지) |
| **grand-potential / 볼록껍질** | §Predicting phase formation 전반 + `Fig. 5b` | **미기재** (pymatgen 언급조차 없음) | ✅ 우리 방법의 원전 2편(216·217)을 이름으로 인용 |
| **Wulff 작도** | `Fig. 6b` — 표면에너지 → 입자 형상 | 미기재 | ⛔ 우리 0건 |
| **준조화 근사(quasiharmonic)** | ref 206 (안티페로브스카이트 안정화온도 ↔ 격자왜곡 선형관계) | 미기재 | ⛔ 우리 포논 0건 |
| **비지도 landmark 분석** | ref 133 — MD 에서 Li 점프 자동 검출(LLZO) | 미기재 | 📎 우리 `hops_per_ion.py`(inter-cage hop 계수)의 문헌 형제 |
| **kinetic Monte Carlo** | ref 152 — Na-NASICON >2,000 회 | 미기재 | ⛔ 우리 0건 |
| **Bader / COHP / ELF / BVSE** | **전부 0회** | — | 🔑 **우리 LOBSTER ICOHP · BVSE 는 이 리뷰의 도구 목록에 없다** = 우리 고유 축 |

> 🔑 **부수 소득**: 리뷰가 **ICOHP·Bader·ELF·BVSE 를 한 번도 안 쓴다.** 즉 우리 **LOBSTER ICOHP(Li–Cl −1.86/−2.10)**
> 와 **BVSE 채널%** 는 이 필드 표준 리뷰가 커버하지 않는 관측량이다 — **차별화 요소**로 쓸 수 있다.
> ⚠ 단 "아무도 안 한다" 가 아니라 "이 리뷰가 안 다룬다" 다. 과장 금지.

---

## 7. 우리 DFT 대비 (comp1 / modelc) ★★ → `../our_dft_baseline.md`

### 7a. 축 B (산화안정) — **같은 방법, 그리고 리뷰가 지적하는 한계 4개**

| 항목 | 우리 | 리뷰 | 판정 |
|---|---|---|---|
| 방법 | grand-potential ESW + `InterfacialReactivity`(pymatgen, MP2026 hull) | **ref 216(Zhu15) + ref 217(Rich16) 을 "pioneering" 으로 명명** | ✅ **같은 계보. 우리가 필드 정본 방법을 쓰고 있음이 최상위 리뷰에서 확인된다** |
| 황화물 판정 | onset **2.256 V**(LiS₄ 제외) / 2.14(포함), S²⁻-limited | *"Thiophosphate electrolytes were predicted to have **especially narrow** electrochemical stability windows"* | ✅ 방향 일치 |
| 한계 ① 운동학 | 이미 원장에 있음 | *"kinetic barriers … are **not considered**"* | ✅ 기지 |
| 한계 ② 과소평가 | — | *"**may underestimate observed values**"* | ✅ 우리 "하한" 프레이밍 강화 |
| **한계 ③ 간접 경로** | ⛔ **우리 원장에 없음** | ref 211 — (탈)리튬화 중간상 경유 ⇒ *"window is **usually wider**"* | 🔴 **신규. §H 로** |
| **한계 ④ 보고량 정의** | ⛔ **우리 원장에 없음** | ref 218 — 창이 **산물이 아니라 SE 고유 안정성**에서 올 수 있다(`Fig. 5c`) | 🔴 **신규. 보고량 카드 재검토 사유** |

### 7b. 🔴 MLIP-MD 스케일 — **`Fig. 3b` 기준으로 우리는 "왼쪽 칸" 이다**

| | 리뷰 `Fig. 3b` 기준 | 우리 실제 |
|---|---|---|
| 참조데이터 칸 | DFT/AIMD **<500 원자**, 수백 ps (ref 85) | — |
| **MLIP 생산 칸** | **>10,000 원자 · >1 ns** | **558 원자**(lpsocl 62원자 셀 × 3×3×1) · **equilib 5 ps + prod 200 ps**(일부 400 ps) |
| 판정 | | 🔴 **원자수 18× 미달 · 시간 2.5–5× 미달.** 558 은 AIMD 상한(500)을 갓 넘은 값이다 |

**같은 계에서의 문헌 대조** — 리뷰가 인용하는 **ref 241 = Chaney, Golov, van Roekeghem, Carrasco & Mingo,
*ACS AMI* **16**, 24624 (2024)**: **Li|Li₆PS₅Cl** 계면의 SEI 성장을 **>30,000 원자 · 10 ns** MLIP-MD 로.
⇒ **우리와 정확히 같은 물질계에서 원자수 ~54× · 시간 ~50×.**

> 🔑 **정직한 자기평가**: 우리가 UMA(파운데이션 MLIP)를 쓰는 **명분은 스케일**인데, 실제로는 **AIMD 로도
> 돌릴 수 있는 크기**를 돌리고 있다. 이건 "틀렸다" 가 아니라 **"MLIP 를 쓰는 이유를 우리가 아직
> 현금화하지 않았다"** 는 뜻이다. ⛔ 원고에 *"MLIP 덕분에 AIMD 로 불가능한 규모를 봤다"* 라고 쓰면
> `Fig. 3b` 와 ref 241 에 정면으로 걸린다.
>
> ⚠ **단 이것이 우리 Ea·D 의 *상대차* 를 무효화하지는 않는다.** 600/800/1000 K 3점·멀티시드·동일 규약
> 비교는 셀 크기와 무관하게 성립한다. 무효화되는 것은 **"규모 우위" 라는 서사**뿐이다.

### 7c. ⚠⚠ `Fig. 5b` 는 **새 외부 앵커가 아니다** — 이미 우리가 가진 `[Zhu15]` 의 재수록

`Fig. 5b` 를 600 dpi 로 렌더해 **축 캘리브레이션 후 픽셀 측정**(왼축 눈금 0–6 V 선형회귀,
`y(0)=482.13 pt`, 잔차 0.004 V)한 결과와, 우리 원장의 `[Zhu15]` SI 실물 검증값 대조:

| 화학종 | 본 digest `figure-read` (Dutra `Fig. 5b`) | 우리 원장 `[Zhu15]` (SI 실물 검증) | 차 |
|---|---|---|---|
| **Li₆PS₅Cl** | **1.70 – 2.00 V** (연장 **2.88 V**) | **1.71 – 2.01 V** (dashed **2.88 V**) | **0.01 V** |
| Li₃PS₄ | 1.70 – 2.29 | 1.71 – 2.31 | 0.02 |
| LGPS | 1.70 – 2.14 | 1.71 – 2.14 | 0.01 |
| LLZO | 0.05 – 2.90 | 0.05 – 2.91 | 0.01 |
| LiF | 6.34 | 6.38 | 0.04 |
| **LiCl** | **4.21** | **4.21** | **0.00** |
| Li₂O | 2.91 (연장 3.29) | 2.90 (dashed 3.32) | 0.01 |
| LiI | 2.46 | 2.46 | 0.00 |
| **Li₂S** | **1.99** | **2.00** | **0.01** |
| Li₃P | 0.86 (연장 1.29) | 0.85 | 0.01 |
| Li₃N | 0.49 (연장 1.66) | 0.45 | 0.04 |

**두 겹의 독립 검증이 통과했다**: ① 본문 서술 *"LGPS 와 LLZO 의 창은 **1.71–2.14 V** 와 **0.05–2.91 V**"*
(ref 214) ↔ 내 측정 1.70–2.14 / 0.05–2.90 ② 우리 원장 `[Zhu15]` 11종 전체 ↔ 내 측정, **최대 차 0.04 V**.

**⇒ 결론 3개**:
1. ⛔ **`Fig. 5b` 를 "새로운 독립 확증" 으로 인용하면 안 된다.** 같은 데이터의 10년 뒤 재수록이다.
   (우리 원장의 진짜 독립 확증은 `[Wang26IF]` `Fig. S2` 1.78–2.30 V 와 `[Rich16]` 2.06–2.32 V 다.)
2. ✅ **쓸 수 있는 것**: *"2015년의 grand-potential 창이 2025년 *Nature Reviews Materials* 에 **그대로
   재수록된다** = 필드가 이 값을 여전히 정본으로 취급한다"* 는 **권위 인용**.
3. ✅ **부수 소득 — 우리 픽셀 판독 규약이 검증됐다.** 축 캘리브레이션 기반 figure-read 가 **11종에서
   ≤0.04 V** 로 SI 실물값을 맞혔다. 앞으로 `figure-read ≈` 표기의 신뢰도 근거로 이 표를 인용할 수 있다.

**🔑 그리고 axis ①(S²⁻-limited) 의 *세 번째* 간접 증거**: 같은 그림에서
**Li₂S 상한 1.99 V ≈ Li₆PS₅Cl 상한 2.00 V** (차 **0.01 V**), 반면 **LiCl 은 4.21 V**.
⇒ *"Cl 은 창의 상한을 못 올린다 — 상한을 잡는 것은 S 다"* 가 **한 장의 그림 안에서** 읽힌다.
⚠ **이건 우리가 두 막대를 겹쳐 읽은 것이지 리뷰의 진술이 아니다**(`[Wang26IF]` Li₂S 2.30 ↔ LPSCl 2.30,
`[Rich16]` Li₂S 2.32 ↔ LPSCl 2.32 에 이은 **세 번째 동일 패턴** — 세 독립 hull 세대에서 모두 성립).

### 7d. 축 D (밴드갭) — **우리 bulk gap 은 다결정 전자누출을 과대평가한다**

| | 우리 | `Fig. 6c` (ref 196 = Quirk & Dawson 2023) |
|---|---|---|
| 값 | comp1 **2.066** / modelc **2.099** / +B₂O₃ 1.9671 / LPSOCl 2.2309 eV (PBE, **fixed-occ nscf**) | **Li₃PS₄**: bulk **3.21** → Σ3{121} **2.55** → Σ5{210} **2.49** eV |
| 계 | Li₆PS₅Cl 계, **bulk 주기셀** | Li₃PS₄, **bulk + 입계 슈퍼셀** |
| functional | PBE (과소평가 ~1 eV) | **미기재** (리뷰가 안 준다) |

- ⛔ **절대값 비교 금지** — 물질도 다르고 functional 도 모른다.
- ✅ **쓸 수 있는 것 = 기울기**: 같은 황화물에서 **입계가 갭을 −0.72 eV (−22 %) 깎는다.**
  우리 gap 은 전부 **bulk 주기셀**이므로, 실제 다결정 펠릿에서의 **전자 차단 능력을 낙관 쪽으로 준다.**
- 🔴 **우리 §H(정직 목록)에 추가**: *"우리 밴드갭 축은 입계를 못 본다. 문헌(Quirk & Dawson 2023)은
  황화물에서 입계 갭이 bulk 대비 20 % 이상 낮아지고 **폴라론 확산이 입계 누설전류에 기여**한다고 한다."*
- 📎 이미 있는 §J-19(미세구조·입계 축, `[Ou26MS]`)에 **전자구조 쪽 형제**로 붙는다.

### 7e. 축 A (이온전도) — **문턱 판정만 가능**

| | 우리 | 리뷰 |
|---|---|---|
| 설계 문턱 | comp1 Ea **0.253** / modelc **0.224** eV (MLIP-MD 아레니우스) | *"fast-ion behaviour … **Ea < 0.3 eV**"* |
| 판정 | ✅ **둘 다 통과** (문턱 판정 — 절대값 인용 아님, 정책 위반 아님) | |
| σ | ⛔ **절대값 인용 금지**(1저자 정책) | *"practical RT σ **>10⁻³ S cm⁻¹**"* · `Fig. 2b` 문헌 σ 지형 |
| 아지로다이트 Ea 문헌값 | — | ref 160: **~0.15 eV** (무질서가 cage 간 거리를 줄여 경로 연결) | ⚠ **소환값.** 우리 0.224–0.253 과 같은 표에 놓지 않는다(방법·정의 다름) |

### 7f. 무질서 처리 — **`Fig. 4c` 가 우리 앙상블 규약을 개념적으로 지지한다**

`Fig. 4c`(Morgan 2021, ref 162)는 아지로다이트에서 **S/X 자리무질서 → Li 하부격자 무질서 → cage 간
경로 연결 → superionic** 을 도식화한다. 본문은 ref 160(무질서가 cage 간 점프거리를 줄이고 cage 를
확장해 경로를 잇는다, Ea ~0.15 eV) · ref 167(S/X 균형 분포가 거시 σ 를 최적화) 로 보강한다.

- ✅ **우리 disorder-ensemble MD(s2/s3/s4 … 배열별 독립 궤적)는 이 그림의 직접적 구현이다.**
- 🔴 **그러나 리뷰는 무질서를 *어떻게 계산에 넣는지* 를 안 준다** (SQS·enumeration 0회).
  ⇒ 우리 앙상블 규약의 방법론 근거는 여전히 `[Adeli]`(중성자 점유율) + `chang2026…`(S/Cl 6배열 σ 2자릿수 산포)다.
- ⚠ **`chang2026…` 이 같은 계에서 σ 를 0.05 → 41 mS/cm (2자릿수) 벌린다고 보고했다** —
  리뷰의 `Fig. 4c` 는 그 산포가 **잡음이 아니라 물리**임을 말해 주지만, 동시에 **단일 배열 결과를
  인용하면 안 된다**는 경고이기도 하다.

---

## 8. 적용 인사이트 — 원고·positioning 에 바로 쓰는 것

1. **⭐ Future §B 의 "no single unified design principle" 은 양날이다.**
   - ✅ **방패**: 우리가 Cl-rich·Nd·O·B₂O₃ 를 **여러 축으로 흩어서** 최적화하는 것이 필드 합의에 부합한다.
   - 🔴 **칼**: *"단일 설계원리가 없다"* 는 곧 **"우리 도핑 하나로 보편 원리를 주장할 수 없다"** 는 뜻이다.
     우리 결론을 **Li₆PS₅Cl 계 한정**으로 쓰는 것이 리뷰와 정합한다.
2. **⭐ Future §A 가 우리 §B 를 직접 호명한다** — *"Further advances in **thermodynamic models for
   electrochemical stability and interfacial reactivity** are important to help guide **intrinsic voltage
   limits** for practical operation"*. 우리 matched factorial 이 그 응답이다. **인트로 마지막 문단의
   gap 문장으로 이 문장을 그대로 쓸 수 있다.**
3. **`Fig. 3b` 를 우리 방법 절의 자기규율로 쓴다** — 우리 셀·시간을 리뷰 기준과 **명시적으로 대조**해
   적으면(558 원자 / 200 ps vs 권고 >10,000 / >1 ns), 리뷰어가 먼저 지적하기 전에 우리가 선언하는 셈이다.
   그리고 **왜 그래도 되는가**(상대차만 인용 · 동일 규약 · 멀티시드)를 같은 자리에 붙인다.
4. **ICOHP·BVSE 는 이 리뷰의 도구 목록에 없다** ⇒ 차별화 문장 가능:
   *"…which are not covered in recent field reviews of atomistic modelling for solid electrolytes."*
   ⚠ 과장 금지 — "리뷰가 안 다룬다" 까지만.
5. **Schwietert 2020/2021 을 읽고 §B 의 보고량 카드를 다시 본다** (§11 #2·#3). 특히 ref 218 의
   *"창이 산물이 아니라 SE 고유 안정성에서 온다"* 는 **우리 onset 정의의 admissibility** 문제다 —
   `kb/templates/estimand_card.md` §2(집계 규칙) 재검토 사유.

---

## 9. 인용 가능 문장 (영문 초안)

- Scale standard — *"Recent reviews place machine-learning interatomic-potential MD in the regime of
  **>10,000 atoms and >1 ns**, with DFT/AIMD reference data limited to **<500 atoms** (Dutra et al.,
  Nat. Rev. Mater. 10, 566–583, 2025, Fig. 3b)."*
- Thermodynamic-window limitation — *"Predicting the electrochemical stability window from the formation
  energies of decomposition products **may underestimate observed values**, since kinetic barriers are not
  considered and decomposition often proceeds **indirectly via (de)lithiated intermediates** (Dutra et al.,
  2025, and references therein)."*
- Open challenge we answer — *"Further advances in **thermodynamic models for electrochemical stability and
  interfacial reactivity** are important to help guide intrinsic voltage limits for practical operation"*
  (Dutra et al., 2025, Future perspectives).
- Design-principle pluralism — *"There is **no single unified design principle** that facilitates superionic
  behaviour, and diverse design factors can be used to optimize a particular family of solid electrolyte
  material"* (Dutra et al., 2025).
- Grain-boundary electronics — *"Reduced bandgaps are found in the vicinity of grain boundaries of Li₃PS₄
  (**3.21 eV bulk → 2.49 eV at Σ5{210}**), with polaron diffusion contributing to leakage current"*
  (Dutra et al., 2025, Fig. 6c; original: Quirk & Dawson, Adv. Energy Mater. 13, 2301114, 2023).

---

## 10. 비판 — 이 리뷰의 약한 곳 ★

1. **⭐ ML 절이 시대에 뒤져 있다.** 2025년 6월 게재인데 ML 퍼텐셜 분류가 **Behler–Parrinello / GAP / MTP**
   3분류에서 끝나고, **파운데이션 모델·전이학습·fine-tuning 이 전문 0회**다. 우리 litdb 만 봐도
   `liu2026`·`tompa2026`·`alghamdi2026`·`petmad2026`·`chang2026`·`wang2025` 여섯 편이 이 칸을 다룬다.
   ⇒ **이 리뷰를 MLIP 방법론 근거로 쓰면 안 된다.** (필드 지도로만)
2. **⭐ §Predicting phase formation 절이 스스로 모순에 가깝다.** 한편으로 hull 기반 예측의 성공 사례를
   나열하고(NASICON 8종 합성·garnet 3종·Na 황화물 3종), 다른 한편으로 *"분해산물 기반 창 예측은
   관측을 과소평가할 수 있다"* 고 쓴다. **두 진술을 어떻게 화해시킬지는 안 준다** —
   *"어느 hull 결과는 믿고 어느 것은 믿지 말라"* 는 판정 기준이 없다.
   ⇒ 우리가 §B 를 방어할 때 이 리뷰만 인용하면 **양쪽으로 다 읽힌다.**
3. **정량이 거의 없다.** 본문 14 pp 에 **표 0장**, 수치는 Ea 몇 개(0.15/0.23–0.39/0.25–0.31/0.27/0.30–0.32/0.48 eV)와
   σ 자릿수뿐이다. `Fig. 5b`·`Fig. 6c` 의 숫자도 전부 재수록. **자체 계산 0 · 자체 실험 0** 이므로
   **모든 수치가 소환값**이다 — 우리 표에 넣을 때 반드시 원전으로 갈아 끼운다.
4. **🔴 `Fig. 3b` 의 스케일 수치에 근거가 없다.** *">10,000 atoms and >1 ns"* 는 **도식 안의 캡션 문구**이고
   출처 인용이 안 붙어 있다. 우리를 재는 자로 쓰긴 좋지만, **인용할 땐 "리뷰의 도식 문구" 라고 밝혀야 한다**
   (권고 기준이지 검증된 문턱이 아니다).
5. **아지로다이트가 21줄 한 문단이다.** 우리 계인데 **Li₆PS₅Cl 이 본문에 4회**(그중 2회는 계면 절),
   **Li₆PS₅Cl 의 창·σ·Ea 수치는 0개**. `Fig. 2b` 의 아지로다이트는 **Br** 이고 Cl 이 아니다.
   ⇒ "이 리뷰가 우리 계를 다뤘다" 고 쓰면 과장.
6. **입계 편향.** Dawson 의 전문 분야(GB)가 과대표집돼 있다 — 계면 절 3소절 중 GB 가 가장 두껍고,
   저자 자신의 논문(ref 196 Quirk & Dawson, ref 220 Dawson)이 `Fig. 6c` 를 차지한다. ⚠ COI 고지는 없다
   (리뷰에 competing-interests 절이 PDF 본문에 보이지 않음).
7. **`Fig. 6d` 단위 의심** — 계면 형성에너지가 **J cm⁻²** 로 인쇄돼 있다(−0.97/−1.47/−1.82).
   통상 J m⁻² 이고, J cm⁻² 라면 값이 4자릿수 크다. **원전(ref 239 Du et al.) 확인 없이 인용 금지.**
8. **`Fig. 2b` 의 Li₃OCl 선이 다른 것과 섞여 읽기 어렵다** — 범례 11종을 색으로만 구분하는데
   보라/자주 계열이 3개다. figure-read 정량은 권하지 않는다(본 digest 도 `Fig. 2b` 에서 수치를 뽑지 않았다).

---

## 11. 중복 지도 — **이미 litdb 가 더 깊이 다루는 대목** (반복 서술 금지)

| 리뷰의 대목 | 이미 다루는 digest | 깊이 비교 |
|---|---|---|
| ML 퍼텐셜 분류·워크플로 | `makino2026_mlip_battery_materials_review` (147편 2축 분류 + 한계 3절) | **makino 이 압도** |
| MTP | `shapeev2016_moment_tensor_potentials` (원전) | 원전 보유 |
| fine-tuning / 파운데이션 | `liu2026_finetuning_umlip_tutorial` · `tompa2026_…` · `alghamdi2026_…` · `petmad2026_…` | **리뷰엔 아예 없음** |
| 범용 MLIP 선택·검증 | `chang2026_performance_based_mlip_selection_sse`(우리 계 LPSCl) · `wang2025_pretrained_deep_potential_sulfide_sse` | **리뷰엔 아예 없음** |
| 불확실도 | `grasselli2025_uncertainty_era_ml_atomistic` | **리뷰엔 아예 없음** |
| MSD·확산 규약 | `maginn2019_…` · `mccluskey2025_…` · `deklerk2018_…`(= 리뷰 ref 92!) · `zaby2026_…` · `pranami2015_…` | **리뷰는 위임만** |
| Green–Kubo·Haven | `lynch2026_greenkubo_mlip_conductivity_thesis` · `jeon2026_concerted_li_motion_argyrodite_assi`(§J-7-N) | **리뷰엔 아예 없음** |
| ML 스크리닝 | `sendek2017_…` · `fujimura2013_…` · `jain2026_…` | 리뷰는 한 문단(refs 93,111–121) |
| pseudo-binary 계면 | `richards2016_interface_stability_pseudobinary` (= 리뷰 **ref 217**) | **우리가 SI 343행까지 검증** |
| grand-potential ESW | `zhu2015_esw_grand_potential_origin` (= 리뷰 **ref 216**, `Fig. 5b` 출처) | **우리가 SI 실물 대조 완료** |
| 계면 리뷰 | `wu2026_ml_driven_electrolyte_interface_design_review`(§J-20) · `liang2026_…` · `xiao2020_interface_stability_ssb_review` | **xiao2020 이 압도**(같은 저널·같은 형식·refs 250) |
| 미세구조·입계 | `ou2026_microstructural_multiscale_fast_ion_transport`(§J-19) | ou2026 이 정량 |
| 아지로다이트 무질서 | `chang2026_…`(S/Cl 6배열) · `fang2022_…` · `jeon2026_…` · `[Adeli]` | 리뷰는 도식만 |

### 📥 추가로 구해야 할 논문 (이 digest 가 발굴한 것, 우선순위 순)

| # | 논문 | 왜 |
|---|---|---|
| **1** ⭐⭐ | **Schwietert et al., *Nat. Mater.* **19**, 428–435 (2020)** "Clarifying the relationship between redox activity and electrochemical stability in solid electrolytes" (리뷰 ref 211) | **우리 §B 의 가장 강한 반론.** 아지로다이트 포함 · 간접 분해경로 ⇒ 창이 실제로 더 넓다. DFT+XRD+ssNMR+전기화학 |
| **2** ⭐⭐ | **Schwietert, Vasileiadis & Wagemaker, *JACS Au* **1**, 1488–1496 (2021)** "First-principles prediction of the electrochemical stability and reaction mechanisms of solid-state electrolytes" (ref 218) | **보고량 정의 문제** — 창이 산물이 아니라 SE 고유 안정성에서 온다. `Fig. 5c` 원전 |
| **3** ⭐ | **He, Zhu, Epstein & Mo, *npj Comput. Mater.* **4**, 18 (2018)** "Statistical variances of diffusional properties from AIMD" (ref 91) | 리뷰가 "reliable statistics" 를 통째로 위임한 곳. **우리 MSD 창·시드 규약의 빠진 앵커** |
| **4** ⭐ | **Chaney, Golov, van Roekeghem, Carrasco & Mingo, *ACS AMI* **16**, 24624 (2024)** "Two-step growth mechanism of the SEI in argyrodite/Li-metal contacts" (ref 241) | **우리 계(Li|Li₆PS₅Cl) MLIP-MD 30,000 원자 · 10 ns** — 스케일 벤치마크 + 비정질 아지로다이트 중간상(우리 비정질 유리 축) |
| **5** | **Quirk & Dawson, *Adv. Energy Mater.* **13**, 2301114 (2023)** "Design principles for grain boundaries in solid-state Li-ion conductors" (ref 196) | `Fig. 6c` 원전. **황화물 입계 갭 + 폴라론 누설** — 우리 축 D 의 경계 |
| **6** | **Wang, Panchal, Sai Gautam & Canepa, *JMCA* **10**, 19732 (2022)** "The resistive nature of decomposing interfaces…" (ref 243) | **work of adhesion** = 우리 §2b 보호율의 인접 정식화. 선점 확인 필요 |
| **7** | **Morgan, *Chem. Mater.* **33**, 2004 (2021)** "Mechanistic origin of superionic lithium diffusion in anion-disordered Li₆PS₅X" (ref 162) | `Fig. 4c` 원전. 우리 disorder-ensemble 규약의 1차 근거 후보 |
| 8 | Marcolongo & Marzari, *Phys. Rev. Mater.* **1**, 025402 (2017) (ref 140) | Nernst–Einstein 실패 — 우리 Haven=1 가정 |
| 9 | Sjølin et al., *Batter. Supercaps* **6**, e202300041 (2023) (ref 208) | multitarget multifidelity 워크플로 = cascade 선점 확인 |

---

## 12. 기법 용어 미니사전 (이 리뷰에 나오는 것만)

- **Concerted / interstitialcy (knock-on) migration** — 이동하는 격자간 이온이 이웃 격자 이온을 밀어
  인접 자리로 보내는 상관 이동. 단일 vacancy·interstitial 홉과 달리 **여러 이온이 함께** 움직인다(`Fig. 4a`).
  우리 inter-cage hop 계수가 세는 것은 이 범주의 이벤트다.
- **Paddlewheel effect** — 복합 음이온(OH⁻·BH₄⁻·NH₂⁻ 등)의 **회전 운동**이 양이온 이동을 돕는 기전.
  ⚠ 리뷰는 BH₄-치환 아지로다이트에서 *"paddlewheel 증거 없음"*(ref 168) 이라고 명시한다 —
  우리 계에는 회전 가능한 복합 음이온이 PS₄³⁻ 뿐이고 이 효과는 기대하지 않는다.
- **bcc-like anion framework** — 음이온 골격이 체심입방에 가까우면 사면체 자리 사이 **직접 홉**이 가능해
  장벽이 최저(LGPS 0.15 eV)가 된다는 설계원리(ref 139 = Wang et al. *Nat. Mater.* 2015).
  hcp/fcc 는 팔면체–사면체 경유가 필요해 더 높다.
- **Wulff shape** — 면별 표면에너지로부터 평형 결정 형상을 작도하는 방법(`Fig. 6b`).
  표면에너지 산포가 작을수록 구형에 가까워진다.
- **Σ3 / Σ5 grain boundary** — CSL(coincidence site lattice) 표기. Σ 값이 작을수록 두 결정립의
  격자점 일치도가 높아 "정합" 입계다. Σ3 가 Σ5 보다 정합이고, `Fig. 6c` 에서 갭 감소도 Σ3 < Σ5.
- **E_hull − S_ideal·T ≤ 0** (`Fig. 5a`) — 볼록껍질 위 에너지를 **이상혼합 엔트로피**로 상쇄해
  "유한온도에서 합성 가능" 을 판정하는 완화된 컷. T = 1,000 K 사용. ⚠ 우리 cascade 의 hull 컷은
  0 K 기준이라 **더 보수적**이다.
- **Landmark analysis** (ref 133) — MD 궤적에서 이온 점프를 **비지도 학습**으로 자동 검출하는 기법.
  임계거리를 손으로 정하지 않는다는 점이 우리 `hops_per_ion.py` 와 다르다.
- **Space-charge layer** (ref 244) — 산화물 양극 | 황화물 전해질 계면에서 화학퍼텐셜 차이로 생기는
  Li⁺ 고갈/축적층. ⚠ 우리 0 K hull 은 이 층을 못 본다.

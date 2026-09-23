---
title: "Bizeray, Kim, Duncan, Howey 2019 — Identifiability and Parameter Estimation of the Single Particle Lithium-Ion Battery Model (IEEE Trans. Control Syst. Technol. 27(5), 1862)"
source_url: local-upload/27._Identifiability_and_Parameter_Estimation_of_the_Single_Particle_Lithium-Ion_Battery_Model.pdf
source_url_note: "16쪽(본문 14 + 참고문헌·저자 약력), 참고문헌 45편, SI 없음. 액체셀 SPM 식별성 논문 — assb 번호는 Q4 방법 원전이라서 붙였다. 크로퍼가 본문 그림 9장을 잡았다(표 제외) — 9장 전부 직접 봤다, 안 본 그림 0장. Table II 는 쪽 렌더로, Fig. 9 는 벡터 경로 좌표로 읽었다. PDF 는 커밋하지 않는다."
source_doi: 10.1109/TCST.2018.2838097
source_license: "IEEE 저작권(2018) — 비 OA, 기관 구독 다운로드본"
pdf_sha256: 714992e6e46adbc48c1ae5d6bcf17d04465e12d9e7008703875f9c3805c5d64c
ingested: 2026-09-23
sha256: 32999bbc58ebeedfb06b6559b36db7e25f6bd3a5a8efd23960ed1abaef2b2aae
---

# 수집 목적

`assb` 섹션 **28호**. 큐 **27번** (27호 = 큐 26 Sinzig 2024, 26호 = 큐 25 Iwakiri 2024). 닻은 `questions/assb-contact-loss-vs-lampe.md`.
큐 문서(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3)의 등록 축은 **"방법론 원전 (액체셀)"** 이고, 25~29 낱말 지문 표는 이 편을
`identifiab` **9** · `uniqu` 3 · `sensitiv` 7 · `Sobol` 0 · `GITT` — · `OCV` — 로 적었다.

⚠ **이 편은 ASSB 논문이 아니다.** 액체 전해질 Li-ion 셀(합성: LCO 문헌 파라미터 · 실험: Kokam 740 mAh NMC 파우치)의 **단일 입자 모델(SPM)** 식별성 논문이다.
`all-solid-state` 0 · `solid electrolyte` 0 · `solid` 5(전부 "solid-phase" · "solid solution") · `LAM` 0 · `LLI` 0 · `contact` 3(전부 "contact resistance" = 옴 저항).
이 digest 를 `assb` 번호에 넣는 이유는 **Q4(유일성·식별성)의 방법 원전**이라서이고, 26호(Iwakiri)·27호(Sinzig) **둘 다 이 편을 인용하지 않는다**
(26호 digest §참고문헌 · 27호 digest §12 — 두 편의 참고문헌 목록 모두 Bizeray 0 회). 그 인용 0 자체가 기록할 사실이다: ASSB 모델 문헌은 식별성 원전을 가리키지 않는다.

**원문 16 쪽을 전수로 다시 셌다.** 원문은 IEEE 조판(Aspose PDF 재생성본)이고 `ﬁ`(U+FB01) **182 개** · `ﬂ`(U+FB02) **16 개**의 합자를 쓴다.

| 낱말 | 추출 그대로 | **NFKC 정규화 뒤** | 비고 |
|---|---:|---:|---|
| `identifiab` | 9 | **54** | ★ 추출 그대로의 9 는 **전부 대문자 제목·쪽 머리글**("IDENTIFIABILITY AND PARAMETER ESTIMATION …", 합자 없음). **본문 소문자 출현은 추출 그대로 0 — 전부 `ﬁ` 합자 안에 있다.** 정규화 뒤 = 본문 42 + 머리글 9 + 참고문헌 3 |
| `identif*` | 15 | 83 | identifiability · identifiable · identification · identified · identify |
| `unidentif*` | — | 7 | |
| `uniqu` | 3 | 3 | 초록 2 · 정의 1("unique solution") |
| `sensitiv` | 7 | 7 | 전부 국소 서술("much more sensitive to the cathode diffusion") — Sobol·OAT 표 없음 |
| `Sobol` | 0 | 0 | |
| `GITT` | 2 | 2 | 전극 OCV 측정(Fig. 5d) |
| `OCV` | 67 | 67 | 큐 표는 "—"(미집계) |
| `fit` | 0 | 14 | 합자로 0 이 되는 두 번째 낱말 |
| `profile` | 0 | 3 | "loading profile" 류 — 프로파일 가능도 아님 |
| `Fisher` | 0 | 1 | 참고문헌 [18] Forman 2012 제목("fisher identifiability analysis")뿐 — 이 편은 FIM 을 안 쓴다 |
| `Hessian`·`Jacobian`·`covarian`·`correlat`·`confidence`·`bootstrap`·`degenera`·`non-unique`·`Cram` | 0 | 0 | |
| `Kalman` | 4 | 4 | 서론 · 참고문헌 |
| `EIS` · `impedance` · `transfer function` | 35 · 49 · 19 | 같음 | |
| `pressure` · `degrad` · `aging` | 0 · 7 · 1 | 같음 | `degrad` 7 = 서론 3 · 참고문헌 제목 1 · 저자 약력 3. `aging` 1 = 서론. **열화 데이터 0** — 결론의 향후 과제 "evolution of cell parameters as a battery ages" |

⇒ **큐 지문의 `identifiab` 9 는 우연히 방향만 맞았다.** 그 9 는 본문 문장을 **하나도** 세지 않았고(쪽 머리글 9), 실제 본문 밀도는 **6 배**다.
27호가 적은 지문 도구 맹점 ⑦(IOP/ECS `ﬁ` 합자)이 **IEEE 조판에서도 같고, 여기서는 더 세다** — 27호는 0 → 1 이었고 이 편은 "대문자만 센 9" → 54 다.
**합자 맹점은 출판사 특이가 아니라 PDF 추출 일반의 문제**로 다룬다(28호 발견).

> ★★★★ **Q4 판정을 먼저 적는다.**
> 1. **세 줄 중 어디인가 — 셋째 줄(식별성)이다. 계보에서 처음으로 이 줄에 선 편이다.** 구조적 식별성(Bellman–Åström 정의, 전달함수 유일성, `[인쇄]` Definition 1)과
>    실제적 식별성(손실 함수 등고선의 모양, 합성 + 실험 EIS)을 **둘 다** 한다. 26호(OAT 스윕 = 첫 줄) · 27호(Sobol = 첫 줄의 전역판)와 층위가 다르다.
>    단 **정량 도구는 없다** — FIM · 조건수 · 프로파일 가능도 · 신뢰구간 · 근최적 폭의 수치 **전수 0**. 실제적 식별성은 **등고선 그림을 눈으로 읽은 것**이다(Fig. 2 · 3 · 5a–c · 8).
> 2. **그러나 ASSB 명제가 아니다 — 도구 칸만 채운다.** 대상은 액체셀 SPM 이고, ASSB·고체전해질·접촉 손실·Li-In 은 지면에 없다.
>    더 결정적인 것: **이 편이 식별한 집합 `θ̃ = (τ_d⁺, τ_d⁻, R_ct)` 에는 용량이 없다.** 전극 이론 용량 `Q_th,i = ε_i δ_i c_max,i F A` (= LAM 과 접촉 손실이 둘 다 사는 자리)는
>    `[인쇄]` OCV 기울기 `β_i = α_i / Q_th,i` 안으로 흡수되어 **입력(반쪽전지/기준극 측정값)으로 가정**되고, 초기 화학량론 `x_i⁰` (= 전극 정렬, LLI 가 사는 자리)도 **안다고 가정**한다(`[인쇄]` 식 27 아래 "assuming that the initial electrode stoichiometries `x_i⁰` … are known").
>    ⇒ `[해석]` **식별성 원전은 열화 모드 축(전극별 용량 스케일 · 정렬 오프셋)을 전부 입력으로 두고, 동역학 축만 식별했다.** 카드가 묻는 "`LAM_PE` 와 접촉 손실이 하나로 정해지나" 는
>    이 편의 식별 집합 **밖**에 있다.
> 3. **"any lithium-ion battery model" 이라는 범위 문장이 있어도 반 칸을 주지 않는다.** `[인쇄]` "the parameter identifiability of any lithium-ion battery model … is largely conditional on the slope of each electrodes' OCV …
>    A flat OCV curve overshadows all dynamics and results in parameter unidentifiability." — 범위는 보편 명제로 인쇄됐다. 그러나 이 명제가 말하는 것은 **평탄 전극의 확산(동역학) 파라미터**이고,
>    ASSB 에 옮기면 **Li-In/Li 음극의 동역학이 안 보인다**(카드 물음과 무관 — 그 음극에는 식별할 확산이 없다)가 된다. 카드의 물음(양극 **용량** 안의 LAM ↔ 접촉 분할)에는 닿지 않는다.
>    그것을 카드 물음으로 끌고 가는 것은 **우리의 옮김**이다 ⇒ 26호 선례(보인 것이 우리 `[재현]`·`[해석]` 이면 접는다)대로 **접는다.**
> 4. ★★★★ **Q4 스물한 번째 성질 = "도구는 있고 대상이 없다 — 식별성을 (구조적·실제적) 잰 계보 첫 편이지만 액체셀이고, 카드가 묻는 방향(용량 스케일)은 입력으로 뺀 채 쟀다."**
>    ASSB 판정: **0/28**. 계보 전체에서 "식별성을 잰 편" 은 **1/28(이 편, 액체셀)**. 채움표 누적 **≈15.5 → ≈15.5**.

# 판정 한 줄

**방법 원전으로는 계보의 빈칸(셋째 줄)을 처음 채우고, ASSB 명제로는 아무 칸도 안 움직인다.** 그러나 이 편의 파라미터 묶음(식 17–19 · 26–27)에 카드 물음을 올려놓으면
`[해석]` **입자 통째 비연결(`1 − u`)은 `ε` 에 곱해지고 `ε` 는 `Q_th` 안에만 있으므로 SPM 에서 LAM 과 구조적으로 같은 파라미터**이고(근사가 아니라 항등),
**표면 일부 접촉 손실(`A_eff`)은 `a = 3ε/R` 을 통해 `k` 와 곱으로만 들어가 `τ_k/(3Q_th)` → `R_ct` → `R0`(옴 · 접촉 · 피막과 합침)로 사라진다.**
26호의 `k₁≡k₂` 는 이 편 식 (50) 과 **같은 구조**이고, 27호의 오프셋 `1 − u` 는 이 편의 `Q_th` 손잡이와 **같은 자리**다 — 둘 다 우리 대조이지 원문 명제가 아니다.

---

# 0. 원문에 없어서 확인이 필요한 것 (공백)

- **불확실성 수치 0.** 신뢰구간 · 표준오차 · FIM · Hessian · 프로파일 · 조건수 전부 없다. "uncertainties … are large" 는 **등고선 모양의 서술**이다.
- **실험 셀의 전극별 OCV 기울기 `β_i⁰` 값이 인쇄되지 않았다** (Kokam 셀). 합성(LCO)의 `β` 만 Fig. 1 · 2 에 인쇄. 실험의 10 · 50 · 80 % `β` 는 Fig. 5d 곡선에서 우리가 미분해야 한다(미실행).
- **실험 셀의 `x_i⁰`(선형화점 화학량론) 값 없음.** 식 (50) `R_ct(x⁰)` 를 쓰려면 필요하다.
- **`R_ct` 단독 값 없음** — 인쇄된 것은 `R0`(= `R_ct` + 옴 + 접촉 + 피막, Fig. 7) 뿐.
- **실험 추정의 최적화기 · 탐색 상자 · 초기값 미기재.** "PE algorithm" (Fig. 8 캡션)의 정체가 없다. 등고선 격자 범위(Fig. 5: `τ_d⁺` 0–20 ×10³ s · 0–100 ×10³ s)만 보인다.
- **셀 수·반복 0.** EIS 셀 · OCV(기준극 삽입) 셀 · 시간 영역 셀의 관계: `[인쇄]` "different cells were used for OCV measurements compared to EIS and time domain data" — EIS 와 시간 영역이 같은 셀인지는 "same Kokam cell type" 이라고만 적었다.
- **시간 영역 검증의 온도 미기재** (EIS 는 20 °C).
- **셀 이력(신품 여부 · 사이클 수) 미기재.** 열화 0.
- **합성 파라미터(Table I)의 출처는 자기 이전 논문 [1]** (Bizeray 2015 *JPS* 296) — 원출처 대조 안 함. 그 표와 그림이 안 맞는다(§13 D1–D3).
- **추정 코드 비공개.** 시간 영역 SPM 솔버만 [45] Zenodo(Spectral_Li-Ion_SPM)로 인용.

---

# 1. 서지·모델 사양

| 항목 | 값 |
|---|---|
| 서지 | Adrien M. Bizeray, Jin-Ho Kim, Stephen R. Duncan, David A. Howey, "Identifiability and Parameter Estimation of the Single Particle Lithium-Ion Battery Model", *IEEE Trans. Control Syst. Technol.* **27**(5), 1862–1877, Sept. 2019. DOI 10.1109/TCST.2018.2838097 |
| 이력 | 접수 2017-07-12 · 수정 2018-01-19 · 채택 2018-05-10 · 온라인 2018-06-14 |
| 소속 | Oxford 공학과(Energy and Power Group) 3 · **Samsung Advanced Institute of Technology**(Kim) 1 |
| 연구비 | EPSRC EP/K002252/1 · EP/N032888/1 · **Samsung Electronics** |
| 모델 | SPM(Atlung 1979 → Ning & Popov 2004), 전해질 동역학 무시, `α = 0.5` BV, `c_e` 상수 |
| 데이터 ① 합성 | 선형화 SPM 자체로 생성한 **무잡음** EIS, LCO 문헌 파라미터(Table I, 출처 [1]), DoD 5 · 25 · 75 · 95 % |
| 데이터 ② 실험 EIS | **Kokam SLPB533459H4 740 mAh NMC**(흑연 음극으로 보임 — `[인쇄]` "graphite negative electrode" 는 일반론 문장에서만), BioLogic SP-150, 20 °C 챔버, GEIS 100 mA p-p · DC 0, **5 kHz → 200 µHz, 6 점/decade**, 측정 전 휴지 3 h, DoD 당 ≈9 h, DoD 10–90 % 9 점 |
| 데이터 ③ 전극 OCV | 같은 형식의 **다른 셀**에 리튬 코팅 구리선 기준극 삽입([35] McTurk 2015), **GITT** 14.8 mAh 증분 @ C/10, 이완 1 h, **50 점** |
| 데이터 ④ 시간 영역 | EV 주행 유래 동적 부하 1 Hz, 최대 4.4 A(≈6C), ≈10 분, DoD 10 → 20 % |
| 추정 | 복소 임피던스 최소제곱(식 62–66), 고주파 반원 제외, `R0` 는 45° 직선 절편 회귀(식 67–70) |

---

# 2. 모델과 파라미터 묶음 (§II)

## 2-1. SPM 식 (`[인쇄]` 식 1–9)

- 전극 `i ∈ {+, −}` 마다 구형 입자 Fick 확산 `∂c/∂t = D/r² ∂/∂r (r² ∂c/∂r)`, 중심 대칭 · 표면 플럭스 `D ∂c/∂r|_R = −j`.
- 플럭스 = 전류 비례: `j₋ = +I/(a₋δ₋FA)`, `j₊ = −I/(a₊δ₊FA)`, **`a_i = 3ε_i/R_i`** (활성 비표면적, `[인쇄]` "specific active surface area"). `A` = 전극 면적(두 전극 같다고 가정).
- 전압 `V = U₊(x_s⁺) − U₋(x_s⁻) + η₊ − η₋`, `i₀ = kF√c_e √(c_s(c_max − c_s))`, `α = 0.5` 로 `η = (2RT/F) sinh⁻¹(jF/2i₀)`.

## 2-2. ★ 여섯 묶음 (`[인쇄]` 식 17–19 · 26–27)

무차원화(`r̄ = r/R`, `x = c/c_max`, `x̄ = x − x⁰`) 후 **전극마다 셋**:

| 묶음 | 식 | 뜻 |
|---|---|---|
| `τ_d,i = R_i²/D_i` | (17) | 확산 시간상수 |
| `τ_k,i = R_i/(2k_i√c_e)` | (18) | 동역학 시간상수 |
| `Q_th,i = ∓ε_i δ_i c_max,i F A` | (19) | 이론 전극 용량 (`Q_th⁺` 는 음수 규약) |

그리고 **한 번씩만 나타나는** 재모수화 `θ = [τ_d⁺, τ_d⁺/(3Q_th⁺), τ_k⁺/(3Q_th⁺), τ_d⁻, τ_d⁻/(3Q_th⁻), τ_k⁻/(3Q_th⁻)]ᵀ ∈ ℝ⁶` (식 26), 역사상 식 (27) 은 일대일.
`[인쇄]` 결론: "excluding open-circuit voltage (OCV), there are only six independent parameters". 전제: **`x_i⁰` 과 `U_i(x)` 를 안다.**

`[해석]` 원래 물리 파라미터(전극마다 `R · D · k · ε · δ · c_max`, 공통 `A · c_e`)가 **14 개**인데 여섯 묶음만 보인다. 곱으로 묶이는 조합:
`R²/D` · `R/(k√c_e)` · `ε δ c_max A`. 즉 **`ε`(활물질 분율)는 `Q_th` 에만 있다** — 이것이 §8-5 의 출발점이다.

---

# 3. 구조적 식별성 (§III)

## 3-1. 정의 (`[인쇄]` Definition 1, [31] Bellman–Åström 1970 · [32] Ljung · [33] Alavi 2016)

전달함수 `H(s, θ) = H(s, θ*)` (거의 모든 `s`)의 해가 유일 → 전역 식별 · 유한 개 → 국소 식별 · 무한 → 비식별. **무잡음 · 데이터 무관**의 성질이다.
SPM 은 비선형(BV · OCV)이라 **DoD 한 점 근방에서 선형화**해야 이 정의를 쓸 수 있다. `[인쇄]` "The subject of identifiability and parameter estimation of the nonlinear kinetics term … would be an interesting topic for further research." — **비선형 모델의 식별성은 하지 않았다.**

## 3-2. 전달함수 (`[인쇄]` 식 29–58)

확산 전달함수 `H_d(s) = (τ_d/3Q_th) · tanh√(sτ_d) / (tanh√(sτ_d) − √(sτ_d))` (식 38), 선형화 전압 `V̄ = α₊ x̄_s⁺ − α₋ x̄_s⁻ − R_ct I` (식 49),

`R_ct(θ) = −(2RT/F) [ θ₃ √((1 − x₊⁰)/x₊⁰) − θ₆ √((1 − x₋⁰)/x₋⁰) ]` (식 50)

⇒ **비식별 ① — 두 전극 동역학의 합.** `[인쇄]` "only the difference between the parameters θ₃ and θ₆ … appears … there are an infinite number of pairs (θ₃, θ₆) that will yield the same transfer function and only the lumped parameter `R_ct` can be estimated using the linearized model **at a given DoD**." → 6 → **5**.
(`Q_th⁺ < 0` 규약이라 `θ₃ < 0`; 식의 "차" 는 크기로는 **합**이다 — `[해석]`.)

⇒ **비식별 ② — 용량이 OCV 기울기 안으로 들어간다.** `[인쇄]` `α_i = dU/dx` 는 직접 못 잰다("OCV can only be measured with respect to capacity … not against stoichiometry"). `δx = δQ/Q_th` (식 53) 이므로
`β_i⁰ = α_i⁰/Q_th,i = dU_i/dQ` (식 54) 로 바꾸면 `H⁰(s) = β₊⁰ f(s, τ_d⁺) − β₋⁰ f(s, τ_d⁻) − R_ct` (식 55–58), `f(s,θ) = (θ/3) tanh√(sθ)/(tanh√(sθ) − √(sθ))`.
**`Q_th` 는 따로 남지 않는다.** `β` 는 `[인쇄]` "measurable and assumed known … This requires access to **half-cell or reference electrode cell data**" · "In the absence of individual electrode OCV data, it is **not possible to parametrize the SPM directly**" → 5 → **3**: `θ̃ = (τ_d⁺, τ_d⁻, R_ct)` (식 57).

## 3-3. 식별성 판정과 두 예외 (`[인쇄]` 식 59–61)

`R_ct` 는 `s` 무관 가산항이라 바로 같고, 남는 식 (61) 은 "f 가 `s` 의 비자명 함수이므로" 일반적으로 `τ_d⁺ = τ_d⁺*`, `τ_d⁻ = τ_d⁻*` ⇒ **선형화 SPM 은 구조적으로 식별된다.** 예외 둘:

1. **`β_i⁰ = 0`(평탄 OCV) → 그 전극의 `τ_d` 비식별.** `[인쇄]` "a 'flat' OCV function hides any diffusion dynamics effect of that electrode".
2. **`β₊⁰ = −β₋⁰` → 두 전극의 `τ_d` 를 맞바꿔도 같다** → 순서를 정해야(ordered) 식별.

`[인쇄]` 처방: "identification may be performed using data at several DoDs, ensuring the OCV functions have a significant slope in each electrode."

`[해석]` 판정의 논증은 **증명이 아니라 서술**이다("Since f is a nontrivial function of s, this equality holds … if and only if …"). `f` 의 두 인스턴스가 서로 다른 `β` 가중으로 겹칠 때의 해 집합을 구성적으로 보이지 않았다. 예외 2 는 그 틈에서 나온 것이고, 저자도 §V-A 에서 **"두 국소 최소가 거의 안 보이게" 남는다**고 적는다(아래 5-2).

---

# 4. 추정 (§IV)

- 한 DoD: `L_j(θ) = Σ_ω |Z_j(ω) − H_j(ω, θ)|²` (식 63–64, 실부·허부 제곱합, "least-squares (the maximum likelihood) sense").
- 여러 DoD: `L = Σ_j L_j` (식 66). `[인쇄]` 가정 — **확산 파라미터는 DoD 무관**. 대가: `R_ct` 가 `x⁰` 에 의존하므로 DoD 마다 `R_ct` 가 하나씩 늘어난다.
- ★ **`R0` 분리 회귀** (§IV-C): 고주파 반원(`R_ct ∥ C_dl`)은 **버린다** — `[인쇄]` "Although the SPM could be extended to account for double-layer capacitance effects, this is beyond the scope of this paper. Therefore, the semicircle … is ignored."
  남은 저주파 점에 **기울기 45° 고정 직선**(`y = x + β₀`)을 맞춰 실축 절편 `R0 = −β₀` 를 얻고(식 67–70), **`R²` 가 0.98 을 넘을 때까지 가장 낮은 주파수 점을 하나씩 뺀다.**
  `R0` = `R_ct` + 셀 옴 저항 + **접촉 저항** + 피막 저항의 합(`[인쇄]`).

`[해석]` ① **데이터 선택 규칙이 추정량의 일부다** — 어느 점까지 버리느냐가 `R0` 를 정하는데, 그 규칙은 `R²` 문턱 하나다. ② **식 (50) 에 `θ₃`·`θ₆` 를 가르는 정보가 있다** —
`R_ct(x⁰)` 는 두 미지수 `θ₃`·`θ₆` 에 대해 **선형**이고 회귀변수 `√((1−x₊⁰)/x₊⁰)` · `√((1−x₋⁰)/x₋⁰)` 가 DoD 마다 다르게 움직이므로, `R_ct` 를 두 DoD 이상에서 알면 원리적으로 둘을 가른다.
저자는 이 DoD 의존을 **추정할 것이 늘어나는 비용**으로 읽고, `R_ct` 를 옴 · 접촉 · 피막과 합친 `R0` 로 DoD 마다 따로 잡아 **그 정보를 버렸다.** (이 가름은 `R_ct` 가 다른 저항과 분리돼야 하므로 공짜는 아니다 — 대수이지 계산 결과가 아니다.)

---

# 5. 합성 데이터 (§V-A, Table I · Fig. 1–3)

## 5-1. Table I 과 Fig. 1

`[인쇄]` Table I (LCO, 출처 [1]): 음극/양극 두께 73.5/70.0 µm · 반지름 12.5/8.5 µm · `ε` 0.4382/0.3000 · **`D` 5.5×10⁻¹⁴ / 1.0×10⁻¹¹ m² s⁻¹** · `k` 1.764×10⁻¹¹ / 6.667×10⁻¹¹ · `c_max` 30 555 / 51 555 mol m⁻³ · "Electrode surface concentration `A`" 982 cm⁻² · `c_e` 1000 mol m⁻³.

Fig. 1 (직접 봤다): DoD 25 % 선형화 SPM 의 Nyquist, `τ_d⁺`(왼쪽) · `τ_d⁻`(오른쪽)을 ±50 %. `[인쇄]` 판 안 `β₊⁰ = +0.248 V/(Ah)` · `β₋⁰ = −0.036 V/(Ah)`.
`[도표]` 곡선은 ≈40 mΩ 에서 출발해 45° 꼬리 → 저주파 수직 점근선(용량성, 입자 평균 농도 변화). 왼쪽은 점근선이 −50 % ≈58 · 기준 ≈75 · +50 % ≈88–90 mΩ 로 크게 벌어지고, 오른쪽은 세 곡선이 ≈73–76 mΩ 로 겹친다.
`[인쇄]` "the frequency response is much more sensitive to the cathode diffusion than the anode diffusion at this DoD because of the flat anode OCV".

★ `[재현]` **Table I 의 `D₊` 는 그림과 10³ 배 안 맞는다.** `τ_d⁺ = R₊²/D₊ = (8.5 µm)²/1.0×10⁻¹¹ = 7.2 s` 인데 Fig. 2·3 의 참값 표지는 `τ_d⁺ ≈ 7200 s` 에 있다.
Fig. 1 로 판정: 식 (56) 의 저주파 전개 `f ≈ −1/s − τ/15` 에서 실축 점근선은 `R_ct + β₊τ_d⁺/15 + |β₋|τ_d⁻/15`. `τ_d⁺ = 7225 s`(= `D₊` 1.0×10⁻¹⁴)면 양극 몫 **33.2 mΩ** → 점근선 ≈40 + 33 + 3 = **≈76 mΩ**,
±50 % 는 ≈59 / ≈92 mΩ — 그림(≈58 / ≈75 / ≈88–90)과 맞는다. `τ_d⁺ = 7.2 s` 면 양극 몫 0.03 mΩ 로 **왼쪽 판의 벌어짐이 생길 수 없다.** ⇒ 그림은 `D₊ ≈ 1.0×10⁻¹⁴` 로 그려졌다(D1).
`τ_d⁻ = (12.5 µm)²/5.5×10⁻¹⁴ = 2841 s` 인데 Fig. 2·3 참값 표지는 `τ_d⁻ ≈ 4000 s`(×1.41, D2). Fig. 1 오른쪽 판의 음극 몫은 ±1–2 mΩ 이라 이것으로는 판정 불가.

## 5-2. Fig. 2 — DoD 넷의 `ln L_j(τ_d⁺, τ_d⁻)` (`R_ct` 는 안다고 둠) — 직접 봤다

| DoD | `[인쇄]` `β₊⁰` / `β₋⁰` (V/Ah) | `\|β₋/β₊\|` `[재현]` | `[도표]` 골짜기 모양 |
|---|---|---:|---|
| 5 % | +0.5737 / −0.0480 | 0.084 | **거의 수직** — `τ_d⁺ ≈ 7200` 에 고정, `τ_d⁻` 는 0–10 000 전체가 골짜기 |
| 25 % | +0.2482 / −0.0359 | 0.145 | 수직, 아래쪽이 약간 넓다 |
| 75 % | +0.1171 / −0.1222 | 1.04 | **대각선 골짜기에 최소 둘** — 참값 (≈7200, ≈4000) 과 **맞바꾼 점 (≈4000, ≈7100)** |
| 95 % | +0.1162 / −1.1728 | 10.1 | **거의 수평** — `τ_d⁻ ≈ 4000` 고정, `τ_d⁺` 0–10 000 전체 |

`[인쇄]` 5 · 25 · 95 % 에서도 "the loss function still features two local minima, although barely visible due to the narrow loss function along one axis" — `[도표]` 우리 크롭(300 dpi)에서는 **둘째 최소가 안 보인다**(D6).
`[인쇄]` 설명: "the measured voltage is the difference between the anode and cathode OCV and not the absolute voltage of the electrode with respect to a reference electrode."
★ `[해석]` **2전극 측정의 전극 맞바꿈 대칭** — 카드 계열 전체(16–21호의 3전극·기준극 논문들)가 싸우는 "어느 전극 몫인가" 의 비식별이 **액체 SPM 전달함수에서 식으로 나온다.**

## 5-3. Fig. 3 — 4 DoD 합 (직접 봤다)

`[인쇄]` 5 · 25 · 75 · 95 % 합 → **단일 전역 최소 = 참값.** `[도표]` 등고선은 참값(노란 네모, ≈7200/≈4000)을 중심으로 **닫힌 타원**, `τ_d⁺` 쪽으로 약간 길다.
`[인쇄]` 처방: "complementary DoD values, where each electrode in turn presents a large OCV slope while the other is negligible, should be combined" — 예: 5 % + 95 % 의 두 골짜기 교차.

`[해석]` ⚠ **역범죄(inverse crime)** — 합성 데이터를 **추정에 쓰는 바로 그 선형화 SPM** 으로, **무잡음**으로 만들었다. Fig. 2·3 은 구조적 식별성의 그림이지 실제적 식별성의 증거가 아니다.
(우리 `degradation-degeneracy/` 는 PyBaMM 합성 truth 로 기존 fitting 코드를 채점한다 — 같은 "합성 참값 복원" 설계이고, 이 편은 그 설계를 **같은 모델 · 무잡음**으로 한 판이다.)

---

# 6. 실험 데이터 (§V-B, Fig. 4–8 · Table II)

## 6-1. Fig. 4 — Kokam 셀 Nyquist 9 DoD (직접 봤다)

`[도표]` 5 kHz 에서 실축 ≈22–25 mΩ(`[인쇄]` "approximately equal to 25 mΩ"), 눌린 반원(전하이동) 뒤 **≈1 Hz 부근 골**(10 % ≈67 — Fig. 6 · 70 % ≈113 · 80 % ≈135 mΩ 근처), 45° 꼬리, 200 µHz 끝에서 수직 상승.
끝점 `−Z″` 는 DoD 에 따라 ≈105(50 %) ~ ≈575 mΩ(90 %) — 가장 짧은 꼬리가 **양극·음극이 둘 다 평탄한 50 %** 다. 반원은 DoD 가 클수록 커진다(70–90 % ≈40 mΩ 높이). **이 반원을 추정에서 버린다.**

## 6-2. Fig. 6 · Fig. 7 — `R0` 회귀 (직접 봤다)

Fig. 6(10 % DoD): `[인쇄]` 모든 저주파 점 회귀 `R² = 0.525` → 저주파 점을 차례로 빼서 `R² = 0.995`. `[도표]` 버린 저주파 점 4 개가 보이고(+ 보이지 않게 뺀 3 개, 캡션), 채택 점 ≈11 개, 절편 `R0` ≈62 mΩ.
Fig. 7: `[도표]` `R0` = **≈62(10 %) · 67 · 66 · 70 · 80 · 79 · 104 · 123 · 123 mΩ(90 %)** — 신품 셀에서 DoD 에 따라 **≈2 배**. `[인쇄]` "consistent with previously reported Kokam NMC cell EIS data [40]".

## 6-3. Fig. 5 — 한 DoD 씩 (10 · 50 · 80 %) (직접 봤다, 이 편의 중심 그림)

Fig. 5d `[도표]`: 셀 OCV 4.19 → 3.03 V, 양극(점선) ≈4.27 → 3.64 V, 음극(적색, 오른쪽 축) ≈0.09 → 0.55 V. **음극은 DoD ≈0–60 % 가 ≈0.09–0.13 V 로 평탄**, 양극은 **≈45–65 % 가 ≈3.91 V 로 평탄**. DoD 10 · 50 · 80 % 에 세로선.
`[인쇄]` "At 10% DoD, only the cathode OCV shows a significant slope, at 50% DoD both the cathode and anode OCV are flat, and at 80% DoD both electrodes feature a significant OCV slope."

| DoD | `[인쇄]` 추정 `τ_d⁺` / `τ_d⁻` (s) | `[도표]` 등고선 | Table II 단독 RMS / Max (mΩ) |
|---|---|---|---|
| 10 % | **1820 / 48 992** | 좁은 **수직** 골짜기 `τ_d⁺ ≈ 1–3 ×10³`; 붉은 점은 `τ_d⁻ ≈ 49×10³`(격자 상한 60×10³ 근처) — **`τ_d⁻` 는 골짜기 위 아무 점** | 3.28 / 5.60 |
| 50 % | **50 147 / 50 779** | `τ_d⁺ ≈ 45–62 ×10³` 의 넓은 **수직** 띠, `τ_d⁻` 무반응 | 9.56 / 21.36 |
| 80 % | **4718 / 1985** | 원점 근처 최소, 골짜기가 `τ_d⁻` 방향으로 길다 | 6.48 / 11.32 |

`[인쇄]` 10 %: "the estimated anode diffusion time constant `τ_d⁻` is highly uncertain and cannot be estimated from this data set alone." — **저자가 그 5 자리 값을 스스로 불확실로 표시했다.**
(26호는 평탄 위의 점 `D_e⁻` 를 **표시 없이** 적합표에 올렸다 — 같은 모양, 반대 태도.)
`[인쇄]` 50 %: `τ_d⁺` 최소가 "centered around 60000 s … approximately an order of magnitude higher" — 판 안 수치는 **50 147 s**(D5). 원인 후보 셋을 인쇄: 확산계수의 DoD 의존([41] Ecker 2015 — 50 % 부근 한 자릿수 낮다) · OCV 기울기 측정 오차(수치 미분의 잡음 민감) · 평탄이라 영향 자체가 작다. ⇒ 50 % 는 **버린다.**

## 6-4. Fig. 8 — 10 % + 80 % 합 (직접 봤다)

`[인쇄]` 추정 **`τ_d⁺ = 2880 s`, `τ_d⁻ = 9033 s`**, "a single minimum, elongated along the anode parameter axis". `[도표]` 가장 안쪽 닫힌 등고선이 `τ_d⁻` ≈6–13 ×10³ s · `τ_d⁺` ≈2.5–3.3 ×10³ s (figure-read ≈).
`[인쇄]` 경고: "these results must be considered with caution … the two combined data sets at 10% and 80% DoDs … were chosen somewhat arbitrarily" · 50 % 예측 오차 **RMS 47.88 mΩ / Max 95.16**(단독 적합 9.56 의 5 배).
Table II 합 적합: 10 % 6.66 / 16.73 · 50 % 47.88 / 95.16 · 80 % 6.84 / 12.82 mΩ.

`[재현]` **추정값의 흩어짐(인쇄 값끼리)**: `τ_d⁺` 는 10 % 1820 · 80 % 4718 · 합 2880 (×2.6 폭), `τ_d⁻` 는 80 % 1985 ↔ 합 9033 (**×4.6**) — 80 % 는 `[인쇄]` "both electrodes feature a significant OCV slope" 인 점인데도 합 적합의 `τ_d⁻` 가 그 단독값의 4.6 배다.
⇒ `[해석]` 저자가 인쇄한 원인 후보(DoD 의존 확산 · `β` 오차)와 양립하고, **"DoD 무관 상수 `τ_d`" 가정이 합 적합의 전제**라는 것을 보여 준다. 저자도 결론에서 이것을 "fruitful avenues" 로 남겼다.

---

# 7. 시간 영역 (§V-C, Fig. 9) — 직접 봤고 벡터 경로를 추출했다

- 선형화 SPM 을 시간 영역에서 풀려면 `Q_th,i` 가 필요한데 `[인쇄]` "**Unfortunately, `Q_th,i` is unknown**" → 변수 치환 `û = Q_th ū`, `x̂ = Q_th x̄` 로 소거. "to run the SPM with nonlinear OCV would require knowledge of `Q_th,i`."
- `[인쇄]` 초기 시뮬레이션이 "a consistent increasingly negative offset" → "most likely due to the assumed OCV slope at this DoD being inaccurate, and was **adjusted by multiplying the linearized cathode OCV slope by a factor of 0.78**."
- `[인쇄]` 결과: "max 20 mV and rms 10 mV" (초록: "a maximum voltage error of 20 mV").

`[재현]` Fig. 9 는 벡터다(쪽 14 경로 782 개). 오차 판의 눈금(−60/−40/−20/0/20 mV)으로 적색("Adjusted")·청색("Simulated") 곡선 좌표를 환산:

| 곡선 | 최대 | **최소** | RMS | 평균 |
|---|---:|---:|---:|---:|
| Adjusted (×0.78) | +20.6 mV | **−42.9 mV** (t ≈104 s) | **10.3 mV** | −2.1 mV |
| Simulated (보정 전) | +13.0 | −67.1 (t ≈373 s) | 21.3 | −17.7 |

⇒ **RMS 10 mV 는 맞고, "max 20 mV" 는 양의 최대만이다 — 절대 최대 오차는 ≈43 mV**(D4). 전류 경로 적분: 0–545 s, 최대 4.40 A · 최소 −1.13 A, **순 방전 72.5 mAh = 740 mAh 의 9.8 %** — 캡션 "10 % → 20 % DoD" 와 맞는다.

★ `[해석]` **×0.78 이 어느 묶음에 걸리는가.** `β₊ = α₊/Q_th⁺` 이므로 양극 OCV 기울기 ×0.78 은 (`α₊` 가 맞다면) **양극 용량 `Q_th⁺` ×1.28** 과 구별되지 않는다. 즉 검증 데이터 위에서 사후로 돌린 손잡이가 **이 편이 식별 집합에서 뺀 바로 그 용량 스케일**이다.
저자는 그것을 "OCV 기울기 부정확" 으로 배정했다(원인 검사 없음; 기준극 셀 ≠ 측정 셀). 그리고 보정은 **검증에 쓴 같은 데이터**로 했다 — 이 그림은 독립 검증이 아니다.

---

# 8. ★ Q4 본론

## 8-1. 세 줄 중 어디인가

`[[assb-sensitivity-sweep-vs-identifiability]]` 의 표(설계 민감도 / 추정 민감도 / 식별성)로 **셋째 줄**. 26호(첫 줄 OAT) · 27호(첫 줄 전역판 + 모델 불일치 민감도)가 가리킨 빈 자리의 원전이다.
단 **"잰다" 의 도구가 그림뿐**이다 — 등고선 = 2 차원 근최적 집합의 **그림**. 카드 Q4 의 도구 목록(조건수 · 근최적 폭 · 프로파일) 중 **근최적 폭을 정성으로** 한 셈이다.

## 8-2. ASSB 명제인가, 도구인가 — 도구다 (수집 목적의 판정 1–4 참조)

반 칸 검토 기준(10호 선례: 분야가 **ASSB 에 대해** 비유일성을 명제로 인쇄 → 이동 / 26·27호 선례: 보인 것이 우리 `[재현]` → 접음):
- 이 편의 명제는 **인쇄**다 ✓. 그러나 대상이 **액체셀**이고 ✗, 명제의 내용이 **동역학(`τ_d`) 파라미터**의 식별성이며 ✗, 카드가 묻는 **용량 스케일은 입력으로 가정**했다 ✗.
- ⇒ ASSB Q4 칸 **0/28**. 계보의 "도구 칸" 에는 처음으로 원전이 들어온다.

## 8-3. 26호의 비식별 방향 셋과 같은 구조인가

| 26호 방향 (`[재현]`, 26호 digest) | 이 편의 대응 (`[인쇄]` 식) | 같은가 | 치료 |
|---|---|---|---|
| `D_e⁻` 무반응(0 열) — 식 (30) 조화평균 `D_p` 가 `D_e⁻ ≫ D_M⊕` 에서 포화 → 하한만 | 예외 1: `β_i = 0` 이면 `τ_d,i` 가 전달함수에서 **0 곱** | **같은 부류(0 열), 다른 기구.** 이 편은 **관측 이득(OCV 기울기)** 이 0 → 작동점(DoD)을 바꾸면 풀린다. 26호는 **모델 구조의 포화** → 작동점으로 안 풀리고 한쪽 구간만 | 이 편 `[인쇄]` "complementary DoDs" ↔ 26호는 처방 없음 |
| `k₁ ≡ k₂` — 두 계면 `asinh(i/2i₀)` 가 몸통에서 합만 | 식 (50): 선형화점에서 `θ₃`·`θ₆` 가 `R_ct` 하나로 — `[인쇄]` "infinite number of pairs" | **같은 구조**(두 계면 동역학이 한 소신호 저항으로 합쳐짐) | `[해석]` 둘 다 **SOC 의존 차이**가 깬다 — 이 편은 `√((1−x)/x)` 가 전극마다 다르게 움직이고, 26호는 `i₀⁺` 만 `x` 의존(`i₀⁻` 는 Li 금속이라 SOC 무관). 이 편 저자는 그 정보를 `R0` 로 합쳐 버렸다 |
| `D_M⊕ · a_max` 한 조합 — `x` 좌표에서 양극 부분계가 `D·a_max/I` 만 봄(`I₀⁺ ∝ a_max` 만 깸) | `θ₂ = τ_d/(3Q_th) = R²/(3DQ_th)` — **수송 × 용량 스케일**이 한 묶음. 선형화 후 `Q_th` 는 `β = α/Q_th` 로 들어가 **따로 안 남는다** | **같은 부류: "용량 스케일은 동역학만으로는 안 보이고 화학량론–용량 사상(OCV)으로만 들어온다".** 짝은 다르다(26호는 `D` 와, 이 편은 `α` 와) | 26호: 동역학 항(`I₀ ∝ a_max`) · 이 편: 전극별 OCV 를 `Q` 로 잰 `β`(기준극) |

## 8-4. 27호의 오프셋 `1 − u` 와 같은 구조인가

27호 `[재현]`: resolved 모델의 비연결 입자(`u = 0.93`)가 초기 SOC 에 머물러 `SOC_end` 에 `1 − u = 0.07` 바닥 → P2D 와 대조하면 상수 오프셋, 27호 `[인쇄]` 처방은 `A_el-c` 로 **용량 깎기**.
이 편의 묶음에 올리면 `[해석]`: 비연결은 `ε → uε` 이고 **`ε` 는 `Q_th` 에만 있다**(식 19; `τ_d = R²/D` 에는 없다) ⇒ **입자 통째 비연결은 SPM 에서 `Q_th` 의 스케일 인자 하나** — 27호의 `A_el-c`(용량 손잡이)와 **같은 자리**.
그리고 이 편 자신이 그 자리를 **사후 보정 손잡이로 썼다**(§7 ×0.78 ≡ `Q_th⁺` ×1.28). 세 편이 같은 자리를 서로 다른 이름으로 돌린다: 27호 "homogenization 부족" · 이 편 "OCV 기울기 부정확" · 카드 "접촉 손실 ↔ `LAM_PE`".

## 8-5. 카드 물음을 SPM 묶음에 올리면 (`[해석]` — 대수, 원문 명제 아님)

| 기구 | 물리 파라미터에서 | SPM 묶음에서 | 선형화 EIS 파이프라인에서 |
|---|---|---|---|
| 진짜 `LAM_PE` (재료 소실) | `ε₊ ↓` | `Q_th⁺ ↓` | `β₊ = α₊/Q_th⁺` ↑ — **입력으로 가정** |
| 입자 통째 비연결 (`1 − u`) | `ε₊,eff = uε₊` | `Q_th⁺ ↓` — **LAM 과 항등** | 같음 |
| 표면 일부 접촉 손실 (`A_eff`) | `a₊,eff = A_eff·3ε₊/R₊` | `τ_k⁺/(3Q_th⁺)` 안에서 `k₊·A_eff` 곱 | `θ₃` → `R_ct`(θ₆ 와 합) → `R0`(옴·접촉·피막과 합) — **파라미터로 남지 않는다** |
| 크기 선택적 비연결 (작은/큰 입자 우선) | 남은 입자의 유효 `R₊` 변화 | `τ_d⁺ = R₊²/D₊` 이동 | `τ_d⁺` 는 **식별 집합 안** — 유일한 후보 채널 `[추론]` (LAM 도 크기 선택적일 수 있어 판별력 미정) |

⇒ `[해석]` **SPM 판에서 카드 물음의 답은 "구조적으로 못 가른다" 가 근사가 아니라 항등**이다(입자 통째 비연결의 경우). 가를 입력은 모델 **밖**(DEM `θ` · 회절 상 분율 · 기준극)에 있어야 한다 — 카드의 전제(DEM 이 독립 라벨)와 같은 결론을 **묶음 대수**로 얻는다.
이 편 저자는 이 대응을 **하지 않았다.**

## 8-6. 판정

**0/28 (ASSB). 스물한 번째 성질 = "도구는 있고 대상이 없다."** 반 칸 검토 후 접음 — 명제는 인쇄지만 대상(액체) · 내용(동역학) · 카드 방향(용량, 입력으로 가정) 셋이 다 어긋난다.
대조 셋(§8-3 · 8-4 · 8-5)은 전부 우리 `[해석]` 이다.

---

# 9. 곱 축퇴 처방 — 열한 번째 적용 (`[[assb-lampe-contact-product-degeneracy]]` 1–4단계)

**입력 점검** — 실험 데이터가 있다(9 DoD EIS · 전극 OCV · 시간 영역). 그러나:
- **1단계(같은 상태축의 `R`·`C`)** ❌ — `C_dl` 을 **설계로 버린다**(`[인쇄]` 반원 "is ignored", "beyond the scope"). `R0(DoD)` 9 점은 있으나(Fig. 7) `R_ct` 는 옴·접촉·피막과 합쳐져 있다.
- **2단계(면적을 아는 대조군)** ❌ — 셀 하나, 입도·면적 변화 없음.
- **3단계(`C` 물리 상한 · `Ea`)** ❌ — `C` 없음, 20 °C 한 온도(`[인쇄]` 향후 과제 "effects of temperature").
- **4단계(시간 영역 `C = τ/R`)** ❌ — Fig. 9 는 있으나 성분 분해 없음.

**기여는 처방 적용이 아니라 곱의 구조적 원형이다**: `a = 3ε/R` 과 `k` 는 `τ_k/(3Q_th)` 안에서만 만난다(식 18 · 26) — `A_eff·k` 곱 축퇴의 **액체 SPM 판 증명**이 식으로 인쇄돼 있다(저자는 곱 축퇴라는 이름을 안 쓴다).
그리고 ★ `[해석]` **이 방법의 파이프라인은 처방이 쓰는 채널(`R_CT · C_dl`)을 입구에서 버린다** — 식별성 원전을 그대로 ASSB 에 옮기면 처방 1단계가 설계로 막힌다.

---

# 10. Q5 (기준극 계보) — 해당 없음, 그러나 형태 하나

- Li-In · 고체 기준극 없음 ⇒ **Q5 칸 해당 없음.**
- 방법의 **전제가 기준극**이다: `[인쇄]` `β_i` 는 "half-cell or reference electrode cell data" 가 있어야 하고, 없으면 "not possible to parametrize the SPM directly". 기준극 = **리튬 코팅 구리선**, 상용 파우치에 최소 침습 삽입([35] McTurk 2015 *ECS Electrochem. Lett.* 4, A145).
- `[인쇄]` 한계: "The OCV measurements were performed on a different cell … modified by inserting a reference electrode … may slightly modify the cell behavior" · 온도 · 이력(hysteresis)이 OCV 에 영향.
- `[해석]` **형태 = 21호의 여섯 번째 형태("교정 이식")의 액체셀 선례 + 사후 배율** — 기준극 셀에서 잰 전극 곡선을 다른 셀로 옮기고, 맞지 않으면 기울기에 ×0.78 을 곱했다. ASSB Q5 형태 번호에는 넣지 않는다(Li-In 아님).

---

# 11. 우리 `degradation-degeneracy/` 와의 접점

(우리 쪽 수치는 `degradation-degeneracy/docs/RESULTS*.md` 가 정본 — 여기 옮기지 않는다.)
- **보완 관계** `[해석]`: 우리 프로젝트는 full-cell OCV 곡선에서 **모드 축(전극별 용량 스케일 · 정렬 = LAM_PE · LAM_NE · LLI)** 이 하나로 정해지는가를 묻는다. 이 편은 그 축을 **전부 입력으로 두고** 동역학 축을 식별한다.
  같은 셀의 두 절반이다 — 이 편의 `β = α/Q_th` 입력이 틀리면(모드가 바뀐 노화 셀) 이 편의 `τ_d` 추정이 따라 틀린다. 저자가 향후 과제로 남긴 "evolution of cell parameters as a battery ages" 가 정확히 그 결합이다.
- **전극 맞바꿈 대칭**(Fig. 2 75 %): 2전극 측정이 "어느 전극 몫인가" 를 못 정하는 구조 — 22p 물음(LAM_PE ≈ LAM_NE)과 **형식이 같은 대칭**의 동역학 판(`[해석]`, 모드 축이 아니다).
- **합성 참값 복원 설계**(§5)는 우리와 같고, 이 편은 **같은 모델 · 무잡음**(역범죄)으로 했다. 우리가 이 편에 줄 수 있는 것: 모드 축까지 열어 둔 상태의 폭(`[[near-optimal-set-width-measurement]]`)을 재면 "`β` 를 안다" 는 가정의 비용이 나온다(미실행).

---

# 12. 채움표 행 (Q1–Q8)

| Q1 정량 | Q2 독립관측 | Q3 라벨층위 | Q4 유일성 | Q5 Li-In | Q6 압력 | Q7 dead Li | Q8 화학·OCP |
|---|---|---|---|---|---|---|---|
| **없다 — 액체셀.** `contact` 3 회 = 전부 옴 "contact resistance"(`R0` 에 합침). `θ(N)` **0/28** | **없다** (ASSB 관측 0). 액체셀 기준극으로 **전극별 OCV** 를 잰 것은 방법 전제 | **fitted(EIS 최소제곱) + 합성 참값 복원(같은 모델 · 무잡음 = 역범죄)** — 불확실성은 **등고선 그림뿐**, CI 0 · 셀 1 · 반복 0 | **★ 있다 — 단 액체셀(도구 칸).** 구조적(전달함수 유일성) + 실제적(손실 등고선). 정량 도구 0. **ASSB 0/28** · 스물한 번째 성질 "도구는 있고 대상이 없다" | **해당 없음** — 기준극은 방법의 전제(리튬 코팅 Cu 선, 다른 셀), 사후 ×0.78 | **없다** (`pressure` 0, 상용 파우치) | **해당 없음** | **해당 없음(액체)** — Kokam NMC/흑연 740 mAh, 전극 OCV GITT 50 점(Fig. 5d) · 합성 LCO |

**누적 ≈15.5 → ≈15.5 (새 칸 0).** Q3 에 층 하나(**합성 참값 복원 — 같은 모델 · 무잡음**).

---

# 13. 어긋남 (D-목록)

| # | 어디 | 원문 | 그림/계산 | 판정 |
|---|---|---|---|---|
| D1 | Table I `D₊` | `[인쇄]` 1.0×10⁻¹¹ m² s⁻¹ → `τ_d⁺` = 7.2 s | Fig. 2·3 참값 ≈7200 s · `[재현]` Fig. 1 저주파 점근선은 `τ_d⁺ ≈ 7225 s` 일 때만 맞음(≈76 mΩ, ±50 % ≈59/92) | **표가 10³ 틀림**(그림은 1.0×10⁻¹⁴ 로 그려짐) |
| D2 | Table I `D₋`, `R₋` | `τ_d⁻` = 12.5²/5.5×10⁻¹⁴ = 2841 s | Fig. 2·3 참값 표지 ≈4000 s | ×1.41 불일치, 원인 미상 |
| D3 | Table I `A` 행 | "Electrode surface **concentration**", cm⁻² | 식 (4) 의 `A` 는 전극 **면적**(m²) | 이름·단위 오기(982 cm² 로 읽힘) |
| D4 | 초록 · §V-C | "maximum voltage error of **20 mV**" | `[재현]` 벡터: Adjusted 최대 +20.6 · **최소 −42.9 mV**, RMS 10.3 | 양의 최대만 인쇄 — 절대 최대 ≈43 mV |
| D5 | §V-B-3 | 50 % `τ_d⁺` 최소 "centered around **60000 s**" | Fig. 5b 판 안 **50 147 s**, 붉은 점 ≈50×10³ | 본문 ↔ 그림 |
| D6 | §V-A | 5 · 25 · 95 % 에도 둘째 국소 최소 "barely visible" | 300 dpi 크롭에서 안 보임 | 확인 불가(주장만) |
| D7 | §V-C | 시간 영역 "validation" | ×0.78 를 **같은 데이터**로 보정 | 독립 검증 아님 |
| D8 | 식 (50) · §IV-C | DoD 의존 `R_ct` 를 "adds `N_DoD` … to identify" 로 서술 | 식 (50) 은 `θ₃`·`θ₆` 에 선형, DoD 마다 다른 회귀변수 | 가르는 정보를 비용으로 읽음(`[해석]`) |

(모두 그림·식 대조이며 저자에게 확인하지 않았다.)

---

# 14. 그림 — 무엇을 봤나

크로퍼(`wiki/raw/figures/bizeray2019_spm-identifiability-parameter-estimation/`)가 본문 그림 **9 장**을 잡았다(표는 크롭 안 됨, SI 없음). **9 장 전부 직접 봤다 — 안 본 것 0 장.**
- Fig. 1(크롭에 Table I 이 함께 들어 있다) · Fig. 2 · 3 · 4 · 5 · 6 · 7 · 8 · 9.
- Table II 는 쪽 12 를 200 dpi 로 따로 렌더해 읽었다. Fig. 9 는 벡터 경로(오차 판 적·청 곡선 544/545 점, 전류 곡선 374 점)를 추출했다.
- 본문과 어긋난 그림: **Fig. 1·2·3 ↔ Table I (D1·D2)** · **Fig. 9 ↔ "max 20 mV" (D4)** · **Fig. 5b ↔ "60000 s" (D5)** · Fig. 2 둘째 최소(D6, 확인 불가).

---

# 15. 참고문헌 중 후속 후보 (45 편 중)

| ★ | 서지 | ref | 왜 |
|---|---|---|---|
| ★★★★ | **Forman, Moura, Stein, Fathy 2012** — "Genetic identification and **Fisher identifiability** analysis of the Doyle–Fuller–Newman model …", *J. Power Sources* **210**, 263–275 | [18] | DFN(P2D) 전체에 **FIM 으로 식별성을 수치로** 잰 원전 — 이 편이 안 한 정량 도구. ASSB P2D(9·26·27호)로 옮길 도구 후보 |
| ★★★ | **Alavi, Mahdi, Payne, Howey 2016** — "Identifiability of generalised Randles circuit models", arXiv 1505.00153 | [33] | **등가회로(Randles) 식별성** — ASSB EIS 논문들(16·18·20·21·23호)이 전부 등가회로를 맞춘다. Q4 를 EIS 쪽에서 채울 도구 |
| ★★★ | **Santhanagopalan, Guo, White 2007** — "Parameter estimation and **model discrimination** for a lithium-ion cell", *J. Electrochem. Soc.* **154**, A198 | [30] | 27호의 "모델 적합성" 을 식별성 언어(모델 판별)로 잇는 원전 |
| ★★ | **McTurk, Birkl, Roberts, Howey, Bruce 2015** — *ECS Electrochem. Lett.* **4**, A145 | [35] | 액체셀 선형 기준극 — Q5 계보의 액체 쪽 뿌리(21호 금선 기준극과의 비교) |
| ★★ | **Ecker 외 2015** — "Parameterization of a physico-chemical model … I", *J. Electrochem. Soc.* **162**, A1836 | [41] | 확산계수의 SOC 의존 실측 — "`τ_d` 상수" 가정이 깨지는 근거 |
| ★ | Birkl 외 2015 — parametric OCV model, *JES* **162**, A2271 | [34] | 전극 OCV 측정 방법 |

⚠ 이 편은 ASSB 를 하나도 인용하지 않는다(2019). **26·27호도 이 편을 인용하지 않는다** — 계보가 서로를 안 가리킨다.

---

# 16. 이 digest 가 주장하지 않는 것

- **Q4 가 움직였다고 하지 않는다.** 이 편은 식별성을 쟀지만 액체셀이고, 카드 방향(용량 스케일)은 입력이다.
- **"SPM 에서 접촉 손실 ≡ LAM" 을 원문의 주장으로 적지 않는다** — 식 19 묶음 위의 우리 대수(`[해석]`)이고, 입자 통째 비연결에만 해당한다. 표면 일부 접촉은 다른 자리로 간다.
- **이 편의 방법이 ASSB 에 그대로 적용된다고 하지 않는다** — SPM 은 전해질 수송을 무시하고(`[인쇄]` 유효 1–2C 이하), 27호가 ASSB 복합양극에서 `κ`(고체전해질 이온전도)를 지배 인자로 보였다. ASSB 에서 SPM 의 전제부터 검사해야 한다.
- **Table I 오류(D1·D2)로 이 편의 결론이 틀렸다고 하지 않는다** — 그림은 자기 일관적이고(`τ_d⁺ ≈ 7225`), 구조적 결론은 파라미터 값과 무관하다.
- **Fig. 8 의 `τ_d` 값을 인용하지 않는다** — 셀 하나, CI 0, DoD 선택이 "somewhat arbitrarily"(`[인쇄]`), 단독값과 ×4.6 어긋남.

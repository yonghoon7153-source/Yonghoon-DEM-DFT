---
title: "Conforto, Ruess, Schröder, Trevisanello, Fantin, Richter, Janek 2021 — Quantification of the Impact of Chemo-Mechanical Degradation on the Performance and Cycling Stability of NCM-Based Cathodes in Solid-State Li-Ion Batteries (J. Electrochem. Soc. 168, 070546)"
source_url: local-upload/37._Editors__Choice_Quantification_of_the_Impact_of_Chemo-Mechanical_Degradation_on_the_Performance_and_Cycling_Stability_of_NCM-Based_Cathodes_in_Solid-State_Li-Ion_Batteries.pdf
source_url_note: "PDF 12 쪽(IOP 표지 1 + 본문 9 + 참고문헌 1, 58 편). SI 는 받지 않았다(Fig. S1-S9 미열람). 크로퍼가 본문 Fig. 1-9 를 잡았고 6 장 봤다(Fig. 4 · 5 · 6 · 7 · 8 · 9, Fig. 9 는 패널 확대). 원자료는 커밋하지 않는다. 9호(Huo 2025)의 ref [30], 37호가 Q1 1 순위로 넘긴 편."
source_doi: 10.1149/1945-7111/ac13d2
source_license: "(c) 2021 The Author(s), OPEN ACCESS, CC BY 4.0"
pdf_sha256: 256d89b805dd0d52f15858e65256f6f3292ea324702f4d7df5ec5a86e3aad1d9
ingested: 2026-09-23
sha256: 5becabb36c2ed5e69d1668a7cf04b7ac76da98b2aec34d9b0239c1e7cee8603a
---

# 수집 목적

`assb` 섹션 **38호**. 큐 **37번** (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-e — "Q1 을 깰 1 순위", **큐의 마지막 편**).
닻은 `questions/assb-contact-loss-vs-lampe.md`. 9호(Huo 2025) digest 가 ref [30] 으로 "정량한 몇 안 되는 문헌" 으로 지목하고 기각한 편이고,
37호(Li 2024) 가 Q1 정량 1 순위로 넘긴 편이다.

Gioele Conforto, **Raffael Ruess**(교신), Daniel Schröder, Enrico Trevisanello, Roberto Fantin, Felix H. Richter, **Jürgen Janek**(교신) —
**"Editors' Choice—Quantification of the Impact of Chemo-Mechanical Degradation on the Performance and Cycling Stability of NCM-Based Cathodes in Solid-State Li-Ion Batteries"**,
*J. Electrochem. Soc.* **168** (2021) 070546, doi `10.1149/1945-7111/ac13d2`.
`[인쇄]` 투고 2021-05-18 · 수정 2021-06-28 · 게재 2021-07-21. **OPEN ACCESS, CC BY 4.0**. 소속: JLU Giessen 물리화학연구소 + 재료연구센터(Conforto · Ruess · Trevisanello · Fantin · Richter · Janek), TU Braunschweig InES(Schröder).
`[인쇄]` 자금: Volkswagen AG(R.R., J.J.) + BMBF FESTBATT 03XP0177A · AdamBatt 03XP0305C · FLiPS 03XP0261. **양극 분말(PC · SC NCM811) 제공 = Volkswagen AG.**
`[인쇄]` "Supplementary material for this article is available online" — **SI 는 받지 않았다**(Fig. S1–S9 전부 미열람, §0).

PDF **12 쪽** = IOP 표지 1 쪽 + 본문 9 쪽 + 참고문헌 1 쪽(58 편). sha256 은 frontmatter. 원자료는 커밋하지 않는다.
계보: Janek 그룹 — 23호 Koerver 2017(= 이 편 ref 20) · 22호 Strauss 2018(= ref 45) 과 같은 연구소, 29호 Yanev 2024 가 인용한 Ruess 2020(ref 26)이 이 편의 ref 19(`D̃` · `∂E/∂x` · OCP 표류 수치의 출처).

> ⚠ **표기**: `[인쇄]` = 지면에 문자 그대로 있는 것 · `[도표]` = 그림을 열어 눈으로 읽은 값(figure-read ≈) ·
> `[재현]` = 지면의 수치 · 식으로 이 위키가 다시 계산한 것 · `[해석]`/`[추론]` = 이 위키의 해석. 표시가 없는 서술은 원문이 실제로 말한 것이다.

---

# 판정 (먼저)

> ★★★★ **Q1 — 칸 이동 없음. `θ(N)` 0/38.** 그러나 이유가 지금까지의 0 과 다르다: **이 편은 사이클마다 무언가를 쟀다** — 그것이 `θ` 가 아니라
> **"OCP 에 기여하는 질량"** 이고, 그것은 카드가 가르려는 두 항(`LAM_PE` · 입자 통째 비연결)의 **합**이다.
>
> **(a) 무엇을 정량했나.** 두 채널을 사이클마다(40 회) 잰다.
> ① **활성 질량** `m_act = Q_meas / q_act` (식 7) — `q_act` 는 방전 전후의 **이완 OCP 두 점**을 액체 반쪽전지 기준 곡선(OCP–x)에 대 `Δx` 로 바꾼 값.
> `[인쇄]` "NCM particles that are disconnected from the electronic network **cannot contribute to the OCP any longer and can be considered inactive**."
> ② **Li 확산 경로 길이 분포** `L_diff`(EIS-PSD) — 저주파 꼬리를 원통 입자 앙상블의 유한공간 Warburg 합(식 5)으로 GA 적합.
> 측정인가? **①은 측정이되 용량에서 역산한 값**(22호 반 칸의 기준 "용량에서 역산한 이름표가 아니라 구조 측정" 에 **걸린다**), ②는 적합.
> **잔차 배정인가? — 아니다, 더 직접적이다**: 합을 재고 **전부를 접촉 손실로 이름 붙인다**. 배정 근거는 `[인쇄]` "**We suggest** that the chemo-mechanical evolution … is the main cause"
> + 형태 대조(SC ↔ PC) + 상전이 몫은 **액체셀 TEM 인용 한 편**(ref 14 Lin 2014, "only a 2 nm thin surface layer … after 20 cycles")으로 "low" 처리.
> ⇒ **곱 축퇴(`θ·ε_p`)는 그대로다.** `m_act(N)` 은 우리 α 적합이 내는 `LAM_PE` 라벨과 **같은 층**의 양이다(`[해석]` §3.3).
>
> **(b) 접촉 손실 ↔ `LAM_PE` 를 실험으로 가르나 — 아니다.** 비연결 입자의 리튬 보유: `[인쇄]` "cannot contribute to the OCP" 까지 — 얼어붙은 SOC · 보유 리튬 **0 자**.
> 재가압 회복 0(운전 ≈70 MPa 고정) · 저율 회복 0(대신 **이완 OCP 자체가 율 무관 게이지**다 — 29호 `Q_M` 과 같은 자리, 그리고 같은 한계: `θ`+LAM 한 칸).
> `LLI` 는 **설계상 용량에 안 보인다** — `[재현]` In/InLi 음극 Li 재고 ≈5.15 mAh ↔ 첫 충전 이동 전하 ≈1.87 mAh(×2.75). "exclusively chemo-mechanical" 결론의 대안 공간은 처음부터 LLI 를 뺀 것이다.
>
> **(c) `θ` 전용 조작 — 부분.** **단결정(SC) ↔ 다결정(PC)** 대조가 있다(37호 다섯 요구 중 넷째 "`θ` 에만 반응하는 조작" 의 후보). 그러나 `θ` 전용이 아니다 —
> SC 는 입도가 다르고(`[도표]` Fig. 4 PC 2차 입자 직경 ≈10 µm ↔ SC ≈1–3 µm), **에탄올 초음파 + 750 °C O₂ 6 h 재소성**을 거쳤다(표면 화학이 바뀐 시편). 압력 되돌림 0.
> `[해석]` 오히려 이 대조가 저자가 안 쓴 논거를 준다: 표면 재구성형 LAM 이면 비표면적이 큰 SC 가 **더** 잃어야 하는데 덜 잃었다 — 단 재소성이 표면을 바꿨으므로 결정적이지 않다.
>
> **(d) 모델에 흡수되나 — 예, 두 곳에.** 연속체 모델은 없다(등가회로 + 해석식). 전자 비연결은 **`C_diff` 의 질량 인자**(= `ε_p`, 37호 두 갈래 중 둘째)로,
> SE 접촉 손실 · 균열은 **`L_diff`** 로 간다. `[해석]` 반무한 영역에서 꼬리가 정하는 것은 `L/(C_diff·√D̃)` 하나 — 저자는 `C_diff`(OCP 질량)와 `D̃`(신품 Warburg + BET 면적)를 고정하고 `L` 을 읽는다.
> 37호 `A_eff·k_p` 곱의 **확산 판**이다(§9).
>
> **θ(N) — 0/38. 그러나 첫 "`θ·(1−LAM)` 합 계열" 1/38**: `[도표]` Fig. 6 활성 질량(정규화) N = 40 에서 PC ≈0.63(low-V) · ≈0.62(high-V), SC ≈0.91 · ≈0.90. 조건당 셀 1 개 · 오차 막대 0.

> ★★★ **Q2 — +0.5 (이 편이 움직인 유일한 칸).** 한 셀 · 한 사이클 안에서 **두 물리 채널**(이완 OCP ↔ 저주파 임피던스 꼬리)이 겉보기 용량 손실을
> "OCP-비활성 질량(`θ` ∪ LAM)" 과 "확산 경로 연장(`η_diff`)" 으로 가른다 — 22호가 신품에서 준 `θ ↔ η` 분할의 **노화판, 사이클 해상**.
> 반 칸인 이유: 카드의 핵심 분할(전자 비연결 ↔ 진짜 LAM)은 **하지 않는다** · 두 채널이 **설계상 묶여 있다**(EIS 적합이 OCP 질량을 고정 입력으로 받는다) ·
> `[재현]` 이완 1 h 가 PC 후반의 확산 시상수(≈13–17 h)보다 **한 자릿수 짧아** 동역학 손실이 질량 채널로 새는 방향이 있다(§3.2) · 조건당 셀 1 개.

> ★★★ **9호의 기각 문장은 그림으로 선다.** 9호: `[인쇄]` "the error between the experimental result and the quantitative analysis is **relatively large**".
> 이 편 본문: `[인쇄]` "the measured specific capacity is reproduced **in good agreement for all the samples**". `[도표]` Fig. 9: (b)(c) 는 맞고,
> **(a) 는 모델이 실측보다 전 구간 +12…+27 mAh g⁻¹ 위**, **(d) 는 N = 40 에서 −14 · N = 1 에서 −28**. 9호가 옳고 본문이 그림과 어긋난다(D1).
> 이 편 자신의 "fitting error is relatively large (Fig. S8)" 는 **다른 문장**(high-V ↔ low-V `L_diff` 증가율 비교)이다 — 9호 문장의 출처가 아니다.

> ★★★ **Q4 — 0/38, 서른 번째 성질: "식별 한계를 식으로 인쇄하고, 결론의 수를 그 한계 밖에 두었다."**
> `[인쇄]` "a limit for reliably determined particle sizes of `L_i < √(D̃/f_min)` … `L_i`(25 °C) < 1.8 µm or `L_i`(60 °C) < 4.5 µm … Above this limit, diffusion is semi-infinite, resulting in a gradual increase of the uncertainty of the fit".
> `[도표]` Fig. 7d 신품 PC 중앙 반경 **4.8 µm**(25 °C 적합 포함) · Fig. 8 사이클 뒤 `L_diff,50` **4.8–5.6 µm**(PC). `[추론]` 사이클 적합의 `D̃` = 10⁻¹¹ cm² s⁻¹(= 25 °C 값, §4.4) ⇒ 한계 1.8 µm.
> 식별 집합에 **용량 스케일이 없다**(`C_diff` 는 OCP 질량으로 고정 입력) — 29호 반 칸의 기준(저자 진단 + 용량 스케일 포함)에 못 미친다. 다중 시작(GA 10 · 25 회) 폭은 **신품 한 판에만** 그려졌다.

---

# 0. 원문에 없어서 확인이 필요한 것

| # | 공백 | 왜 중요한가 |
|---|---|---|
| G1 | **SI 전부(Fig. S1–S9) 미열람** — S3(활성 질량 절차) · S4(`D̃` 추출) · S5(SEM · 원심 PSD 대조) · S6(대표 임피던스) · S7(굴곡도) · **S8(적합 오차)** · **S9(용량 계산)** | 활성 질량 절차와 Fig. 9 가는 선의 구성이 S3 · S9 에만 있다 |
| G2 | **방전 뒤 이완 시간** — 충전 뒤는 `[인쇄]` "one hour", 방전 뒤는 "followed again by a OCP relaxation"(시간 0) | `Δx` 의 두 번째 점이 평형인지 판정 불가 |
| G3 | **40 사이클 실험(Fig. 6 · 8 · 9)의 온도** — 방법 절은 "either 25 °C or 60 °C" | EIS-PSD 신뢰 한계가 1.8 µm 인지 4.5 µm 인지가 여기서 갈린다. `[추론]` 25 °C(§4.4) |
| G4 | **셀 수 `n`** — 조건당 몇 셀인지 0 자 | `[도표]` 그림마다 계열 하나. Fig. 5d ↔ Fig. 9a(같은 공칭 조건)가 N = 40 에서 ≈37 mAh g⁻¹ 다르다(D4) |
| G5 | **기준 OCP–x 곡선** — "reference data that were obtained from a LEB"(값 · 그림 0, S3) | 액체 반쪽전지의 OCP–x 를 황화물 셀에 쓴다 — 이력 · 계면 전위차 0 가정 |
| G6 | **In/InLi 전위의 사이클 표류** — `[인쇄]` −0.62 V vs Li(ref 42) 상수 | 활성 질량의 모든 점이 이 상수 위에 있다(§10) |
| G7 | **`R_ct` · `C_dl` 의 사이클 값** — 등가회로에 있고 적합됐으나 인쇄 0 | 계면 저항 증가의 용량 몫(과전압 → 컷오프 조기 도달)이 Fig. 9 분해에 없다 |
| G8 | **Fig. 9 "full reversible capacity" 네 값(200 · 190 · 205 · 195 mAh g⁻¹)의 출처** — SC 를 높게 둔 이유만 `[인쇄]` "can be charged to a higher SoC" | 닫힘의 자유 손잡이 |
| G9 | **SEM 단면(Fig. 4 하단)의 사이클 수 · 조건** | 화살표 5 개 — 수 · 면적 · 분율 0 |

---

# 1. 서지 · 낱말 지문

규칙 = **NFKC 정규화 뒤 · 대소문자 구분 · 낱말 경계 · 본문(참고문헌 전, IOP 표지 쪽 제외)**. 공백 정규화 뒤 셌다.

| 열 | NFKC 전 | NFKC 뒤 | 줄끝 하이픈 이음 | 대소문자 무시 |
|---|---:|---:|---:|---:|
| `identifiab` | 0 | 0 | 0 | 0 |
| `uncertaint` | 2 | 2 | 2 | 2 |
| `confidence interval` | 0 | 0 | 0 | 0 |
| `Bayes` | 0 | 0 | 0 | 0 |
| `posterior` | 0 | 0 | 0 | 0 |
| `calibrat` | 0 | 0 | 0 | 0 |
| `LLI` | 0 | 0 | 0 | 0 |
| `LAM`(또는 `loss of active material`) | 0 | 0 | 0 | 0 |
| `degradation mode` | 0 | 0 | 0 | 0 |
| **`contact loss`** | **13** | **13** | **13** | **13** |
| `MPa` | 2 | 2 | 2 | 2 |

- NFKC 가 바꾸는 글자 **121 자** = 합자 `ﬁ` 102 · `ﬂ` 5 + 결합 물결 `˜` 14(`D̃` 의 머리표). **지문 열을 바꾼 것 0** — `ﬁ` 가 가린 열이 없다(34호 `identifiab` 류 가림 없음).
- **소프트 하이픈(U+00AD) 0** — IOP 조판(37호 Elsevier 81 개와 다르다). 줄끝 하이픈 이음도 열 변화 0.
- 대신 쓰이는 어휘 `[인쇄]`: `active mass` 31 · `mass loss` 8 · `contact` 17 · `crack*` 13 · `inactive` 6 · `disconnect*` 3 · `relax*` 10 · `In/InLi` 6 · `LEB` 7 · `percolat*` 1 · `uncertain*` 2 · `error*` 1(= "fitting error") · `reliabl*` 4 · `precision` 2.
- `[해석]` 우리 모드 어휘(`LLI` · `LAM` · `degradation mode`)는 **0** 이고 같은 양을 `active mass` 31 회로 부른다 — 이 편에서 **"active mass loss" 가 곧 `LAM_PE`** 이다(정의 · 측정법 모두, §3.3).

---

# 2. 셀 · 실험 (`[인쇄]`)

- **CAM**: 상용 NCM811(LiNi₀.₈Co₀.₁Mn₀.₁O₂) **PC**(구형 다결정) · **SC**(단결정) — Volkswagen AG 제공. SC 는 응집 분리: 에탄올 분산 · 초음파 2 h · 원심 3 min · **750 °C O₂ 흐름 6 h 재소성**(ref 41 Fantin 2021).
- **SE** Li₆PS₅Cl(NEI) · **탄소** VGCF. 양극 복합체 CAM : SE : VGCF = **70 : 30 : 01** 질량비(무결착). 12 mg 복합체를 80 mg SE 펠릿 한 면에, **380 MPa 1 min** 가압.
  면적 0.785 cm² → 활물질 담지 "around 11 mg cm⁻²"(`[재현]` 12 × 70/101 = 8.32 mg → **10.6 mg cm⁻²** ✓).
- **음극 In/InLi**: In 박 64 mm² × 0.1 mm + Li 박 12.5 mm² × 0.2 mm → `[인쇄]` "approximately 67 at% In and 33 at% Li"(`[재현]` **32.1 at%** ✓).
- **운전 압력**: 알루미늄 틀 "constant pressure of around **70 MPa** … maintained during the electrochemical experiments".
- **대조 액체셀(LEB)**: CR2032, CAM : PVDF : Super-P = 90 : 05 : 05, 담지 ≈12 mg cm⁻², Li 금속, 1 M LiPF₆ EC/DMC.
- **전위 환산**: 양극 전위 = 셀 전압 + 0.62 V(`[인쇄]` "−0.62 V vs In/InLi", ref 42 Santhosha 2019). 1C = 200 mA g⁻¹. 온도 25 °C 또는 60 °C.
- **사이클 프로토콜(40 사이클)**: 0.1 C 또는 0.3 C 로 3.77 V 까지 CC → 3.77 V CV(0.01 C 까지) → **EIS**(1 MHz–10 mHz 10 mV · 10–3 mHz 5 mV · 3–1 mHz 4 mV · 1–0.3 mHz 3 mV + 다중 사인; 측정 중 이동 전하 < 1 mAh g⁻¹) →
  CC 로 4.25 V(**low-V**, 0.1 C) 또는 4.5 V(**high-V**, 0.3 C) → **1 h 이완** → 같은 전류로 2.6 V 까지 방전 → OCP 이완(시간 미기재).
- **SEM**: FIB(Xe, 1.8 µA 절삭 · 200 nA 연마) 단면 BSE 5 kV. 분말 SE 는 Zeiss Merlin.

---

# 3. 방법 A — 이완 OCP 로 잰 활성 질량 (식 7)

## 3.1 원문 (`[인쇄]`)

- XRD 격자 상수로 SOC 를 재는 방법(ref 47 Bartsch 2019)이 있으나 "requires expensive operando XRD equipment" — 대신 **평형 OCP** 로 SOC 를 잰다:
  "the equilibrium OCP of a cell with an NCM cathode (**and an In/InLi anode with fixed potential**) follows a well determined OCP function vs x".
- 전제: "the OCP of the cell is stable and not affected by self-discharge" — 첫 사이클 뒤 "a drift of only a few mV per day"(ref 19).
- 절차: 방전 전후 이완 OCP → `Δx` → 실제 비용량 `q_act`(**LEB 기준 곡선**, "known to have an almost ideal Faradaic efficiency", Fig. S3) → `m_act = Q_meas / q_act`.
- 해석: "NCM particles that are disconnected from the electronic network cannot contribute to the OCP any longer and can be considered inactive."
- 대안 기구 처리: "Other mechanisms that can cause a loss of active mass are decomposition reactions and fatigue of the NCM itself. While they certainly occur … **the associated loss of active mass can be considered as low**. TEM investigations have shown that even after 20 cycles only a 2 nm thin surface layer …"(ref 14).
- high-V 에서는 저자도 가르지 않는다: "either caused by the increased strain … **or** by the structural transformation into electrochemically inactive phases as a result of oxygen loss at high potentials."

## 3.2 ★★★ 비판 — 이 게이지의 조건 셋

1. **이완 시간 ≥ 확산 시상수.** `[재현]` 이 편 자신의 식 1(`τ = L²/D̃`)과 사이클 계산용 `D̃` = 5 × 10⁻¹² cm² s⁻¹ 로:
   `L_diff,50` 1.6 µm(PC, N = 1) → **1.4 h**, 5.6 µm(PC low-V, N = 40) → **17.4 h**, 4.8 µm → 12.8 h; SC 1.3 → 0.9 h, 2.6 → 3.8 h.
   충전 뒤 이완은 **1 h**. ⇒ PC 후반의 "relaxed OCP" 는 **입자 내부 평형 전의 표면 가중 전위**다.
   `[추론]` 방향: 충전 뒤 표면이 속보다 탈리튬 → OCP 높게 → `x` 낮게 읽힘; 방전 뒤 반대 ⇒ **겉보기 `Δx` 가 크게 → `q_act` 크게 → `m_act` 작게 → 질량 손실 과대**.
   그리고 이 편향은 **`L_diff` 가 클수록 커진다** — 동역학 손실이 질량 채널로 새는 경로이고, 두 채널의 독립성이 **PC 후반에서 가장 약하다**.
2. **상대극 기준이 상수.** `[재현]` 3.77 V 의 인쇄 기울기 `∂E/∂x` = 0.38 V 로 환산하면 **OCP 10 mV 오차 ≈ `Δx` 0.026 ≈ 활성 질량 ±3.8–4.4 %**(`Δx` 0.6–0.7 가정).
   17호가 잰 In+LiIn 평탄 폭 상한 ±10 mV([[assb-li-in-reference-potential-window]])는 **SC 의 40 사이클 손실(≈9–10 %)의 절반 크기**다. 끝점은 3.77 V 가 아니므로 환산은 자릿수만.
3. **기준 곡선이 액체셀.** 황화물 셀과 액체셀의 OCP–x 가 같다는 가정(계면 전위차 · 이력 0). 검증 0.
- ⚠ **방법 바닥**: `[도표]` Fig. 6 SC low-V 가 N ≈ 6–9 에서 **≈1.005**(공칭 질량 초과) — 정의상 1 을 넘을 수 없는 양이 넘는다 ⇒ 방법 오차 ≥ 0.5 %, 본문 언급 0(D7).

## 3.3 ★★★★ `[해석]` 이것은 우리 α 측정이다 — 그래서 카드 물음을 풀 수 없다

- 상대극이 평탄(고정 전위)이면 셀 OCV 곡선 = 양극 OCP 곡선이고, `m_act = ΔQ / (Δx · q_unit)` 는 **양극 용량 스케일 — 우리 α 적합의 `α_PE`** 를 두 점으로 읽는 것이다.
  우리 degeneracy(`LAM_PE` ↔ `LAM_NE` ↔ `LLI`)는 음극 곡선과 오프셋 β 가 있어야 생기는데, **이 설계는 셋 다 지운다**(평탄 상대극 · Li 과잉 ×2.75). 그래서 α 가 두 점으로 식별된다.
- 그러나 카드의 물음은 **α 안**에 있다: `α_PE ∝ ε_p · θ`. 이 편은 α 를 재고 그 전부를 `θ` 에 이름 붙였다.
  ⇒ **"접촉 손실을 정량한 원전" 이 실제로 한 것은 OCV 기반 `LAM_PE` 측정에 기구 이름을 붙인 것**이다. 카드의 For 쪽(§"OCV 만으로는 못 가른다")에 **방법의 전제로 인쇄된 표본**이 붙는다.
- 우리 코드의 `LAM_PE` 형태는 `degradation-degeneracy/docs/07_LAM_LLI.md` §2 가 정본이다(수치 복사 없음).

---

# 4. 방법 B — EIS-PSD: 저주파 꼬리에서 확산 경로 분포를

## 4.1 모델 (`[인쇄]`)

- 유한공간 Warburg(“Warburg-open”) — 평판(식 2) `Z = (τ_i/C_diff,i)·coth√(iωτ_i)/√(iωτ_i)`, 구(식 3). `C_diff = ∂Q/∂E = F c_o V ∂x/∂E`.
- 크기 분포: 입자 수 가중 병렬(식 4) → 부피 분율 `ΔQ_i` 형(식 5 원통 · 식 6 구). 빈 **16 개**, 로그 간격 **40 nm–40 µm**.
- 고주파부(1 MHz–10 mHz)를 **L–R–(R)(P)–(R)(P)–(R)(P)–W–C**(FMG 형)로 먼저 맞추고 빼서 꼬리를 고립 → 꼬리를 식 5/6 으로 **Matlab `patternsearch` + `ga`**(TimeLimit 300 s · 종료 허용 10⁻⁷), 분포마다 10 회(Fig. 8), Fig. 7 은 25 회 반복 → 중앙값.
- 등가회로(Fig. 7a) 가정 셋: (i) 전자 전도 비율속 (ii) 이온 수송 저항 < 계면 전하이동 저항(얇은 ≈60 µm 양극) (iii) 전하이동 시상수 ≪ 확산 시상수.
- **`D̃` 는 신품에서 한 번**: 반무한부 FMG 적합의 Warburg 계수 + **BET 면적 0.2 m² g⁻¹** → 3.77 V 에서 `D̃` = **10⁻¹¹**(25 °C) · **6 × 10⁻¹¹ cm² s⁻¹**(60 °C).
- `C_diff/m` = **520 mAh V⁻¹ g⁻¹**(ref 19 의 `∂E/∂x` = 0.38 V, x = 0.66 @ 3.77 V).
- **사이클 적합에서는 형상을 원통으로 바꾸고**, "`L_diff` = 원통 두께 = Li 확산 경로 길이" — "should not be confused with the actual particle size which should be significantly larger".
  그리고 `[인쇄]` "we used the electrochemically active mass, as determined above for each cycle, **as fixed input parameter for the fitting**".

## 4.2 ★★★ 신뢰 한계 — 저자가 식으로 인쇄한 식별 경계

`[인쇄]` `L_i < √(D̃/f_min)`, `f_min` = 0.3 mHz → 25 °C **1.8 µm** · 60 °C **4.5 µm**(`[재현]` 1.83 · 4.47 ✓). "Above this limit, diffusion is semi-infinite, resulting in a gradual increase of the uncertainty of the fit with larger particles."
- `[도표]` Fig. 7d: 신품 PC 중앙 반경 **4.8 µm**(25 °C · 60 °C 두 적합이 중앙값에서 겹친다). 음영(25 회 최대 편차)은 중앙값 높이에서 25 °C ≈3–8 µm · 60 °C ≈4–5.5 µm.
  ⇒ 25 °C 적합의 **중앙값이 25 °C 한계의 2.7 배**이고, 그래도 60 °C 와 "good" 일치 — `[해석]` 반무한 영역에서는 분포의 모양이 아니라 한 곱(§4.3)만 정해지므로, 일치는 **그 곱의 일치**일 수 있다.
- `[도표]` Fig. 8 `L_diff,50`: PC low-V **1.6 → 5.6 µm** · PC high-V **1.6 → 4.8 µm** · SC low-V **1.3 → 2.1 µm** · SC high-V **1.3 → 2.6 µm**. 신품 PC 가 이미 한계(1.8 µm) 근처에서 출발해 **한계 밖으로 이동**한다.
  `[도표]` N = 40 PC 곡선의 1.8 µm 누적 부피 ≈0.15–0.25 ⇒ **부피의 ≈75–85 % 가 자기 한계 밖**.

## 4.3 ★★★★ `[해석]` 꼬리가 실제로 정하는 곱

식 2 에서 `ωτ ≫ 1` 이면 `coth → 1` 이고 `Z ≈ √τ / (C_diff √(iω)) = L / (C_diff · √D̃ · √(iω))`.
⇒ **반무한 영역(PC 사이클 결과의 대부분)에서 꼬리가 정하는 것은 `L / (C_diff·√D̃)` 하나**다. `C_diff ∝ m_act`(OCP 채널에서 고정) · `D̃`(신품 고정) · `L`(읽음).
- 부피/길이 = 면적이므로 `C_diff / L ∝ 접촉 면적` — **반무한 꼬리는 "접촉 면적 × √D̃" 를 잰다.** 저자의 `L_diff` 증가는 이 영역에서 `A·√D̃` 감소와 같은 말이다.
- 세 방향이 한 곱에: (1) `D̃` 감소(저자도 언급하는 표면 암염/스피넬 층 — 확산 장벽)가 `L` 증가로 읽힌다 — 유한공간 영역에서도 `τ = L²/D̃` 라 "`L_diff` ×3–4" = "`τ` ×9–16 또는 `D̃` ÷9–16" ·
  (2) 활성 질량 `m_act` 를 과대 손실로 읽으면(§3.2) `C_diff` 가 작아지고 같은 꼬리에 `L` 이 **작게** 맞는다 — 두 채널이 **곱으로 거래**한다 ·
  (3) 신품 `D̃` 는 BET 면적 전부가 접촉했다는 가정 위(`D̃ ∝ 1/(σ·A)²`) — 신품 접촉 분율 `f` 가 1 보다 작으면 `L` 의 절대값이 `1/f` 배.
- **독립 교차 검사가 있었다** — 용량성 극한(`ωτ ≪ 1`, `Z → 1/(iωC_diff)`)은 `C_diff` 단독 = **OCV 와 독립인 활성 질량**이다. 그러나 이 편은 `C_diff` 를 OCP 질량으로 **고정**했고, 25 °C · 0.3 mHz 로는 PC 에서 그 극한에 닿지 않는다.

## 4.4 `[추론]` 사이클 EIS 의 온도

`[인쇄]` 용량 계산 절: "we assume an effective diffusion coefficient of 5∙10⁻¹² cm² s⁻¹ …, which is lower than **the 10⁻¹¹ cm² s⁻¹ taken for the fitting of the distribution** of lithium diffusion pathways". 10⁻¹¹ 은 25 °C 값(60 °C 는 6 × 10⁻¹¹).
⇒ 사이클 적합은 25 °C 값으로 했다 — 측정도 25 °C 였을 가능성이 높고(G3), 그러면 신뢰 한계는 **1.8 µm**.

---

# 5. 결과 — 그림에서 읽은 것

## 5.1 Fig. 5 — 신품 비교와 100 사이클

- `[도표]` (a) SSB 첫 사이클 0.05 C · 25 °C · 2.6–4.25 V: PC 충전 ≈225 / 방전 ≈174, SC ≈235 / ≈197 mAh g⁻¹. (b) LEB: PC ≈248 / ≈198, SC ≈228 / ≈197. (c) 격차 PC ≈24 · SC ≈0 mAh g⁻¹.
  `[인쇄]` "only the SC-NCM morphology allows to access the full capacity" — 원인은 동역학: `[재현]` `√(t_c·D̃)` = √(20 h × 5 × 10⁻¹² cm² s⁻¹) = **6.0 µm** ✓(인쇄 "≈ 6 µm").
- `[도표]` (d) 100 사이클 0.1 C: PC 152 → ≈73(**48 %** 인쇄) · SC 183 → ≈167(**91 %** 인쇄). ⚠ PC 곡선에 **계단 두 곳**(≈31 · ≈58 사이클) — 설명 0.
- `[도표]` (e)(f) dQ/dV: PC 는 H1/M 봉우리 ≈3.74 → ≈3.85 V 로 이동 · 면적 급감, M/H2(≈4.0 V) 도 줄어든다. SC 는 첫 사이클 뒤 거의 불변.
  `[인쇄]` 논거: 컷오프 근처 봉우리(H1/M · H2/H3)는 질량 손실과 동역학 둘 다에 반응하지만 "the M/H2 transition should always be completed for all the active mass in the cell, thus being **independent on kinetic limitations**" → M/H2 축소 = 질량 손실의 **정성적** 판정.
  `[해석]` 이것은 **전압 창 가운데의 동역학 불변 특징으로 `θ·ε_p` 를 `η` 와 떼는** 싼 채널이다(카드 Q2 부류). 단 봉우리가 옮겨 다니는 PC 에서 "완결" 은 가정이고, 정량 0.

## 5.2 Fig. 6 — 활성 질량(정규화) vs 사이클 ★ 정량 그림

`[도표]` 채움 = low-V, 빈 = high-V. 조건당 계열 1 개, 오차 막대 0.

| 조건 | N = 1 | N = 10 | N = 20 | N = 40 |
|---|---:|---:|---:|---:|
| PC low-V | ≈1.00 | ≈0.905 | ≈0.765 | **≈0.63** |
| PC high-V | ≈0.975 | ≈0.875 | ≈0.77 | **≈0.62** |
| SC low-V | ≈1.00 (N 6–9 ≈1.005) | ≈1.00 | ≈0.975 | **≈0.91** |
| SC high-V | ≈0.98 (N = 2 ≈0.955) | ≈0.95 | ≈0.935 | **≈0.90** |

- PC low-V 계열에 불연속(N 3–4 ≈0.96 → 0.97 · N 9–10 평탄 뒤 급락). PC 두 조건은 **N = 40 에서 거의 같다**(0.63 ↔ 0.62) — 본문 "active mass loss appears to be enhanced by the harsh high-V conditions" 는 PC 에서 초기 오프셋만큼이다(D8).
- SC high-V 는 **첫 두 사이클에 ≈4.5 %** 를 잃고 이후 완만 — 기계적 누적보다 초기 사건(첫 사이클 분해 · 접촉 재배열)의 모양이다(`[해석]`, 원문 서술 0).

## 5.3 Fig. 7 — EIS-PSD 검증(신품 PC)

- (a) 등가회로 그림의 라벨은 **`R_int` · `C_int`**, 본문은 `R_ct` · `C_dl`(D5). `R_ion` 사다리 + `Z_diff` + `R_0` + `(R_a C_a)`.
- `[도표]` (b) 60 °C: 호 ≈10 → 33 Ω, 꼬리 −Im 51 Ω 까지. (c) 25 °C: 호 ≈42 → 130 Ω, 꼬리 −Im ≈70 Ω 까지 — **마지막 저주파 점이 적합선 밖**. (d) §4.2.
- 본문: SEM 화상 분석 PSD · 원심 PSD 와 "very good agreement"(Fig. S5 — 미열람).

## 5.4 Fig. 8 — `L_diff` 누적 부피 분포, 40 사이클 · 네 조건 ★ 정량 그림

§4.2 표. `[인쇄]` "Within 40 cycles, the median value of Ldiff … of PC-NCM increases approximately by a factor 3 to 4" — `[재현]` 5.6/1.6 = **3.5** · 4.8/1.6 = **3.0** ✓.
"SC-NCM … **only by a factor of <2**" — `[재현]` 2.1/1.3 = 1.6 ✓ · **2.6/1.3 = 2.0** ✗(D3). 모든 곡선이 40 µm(빈 상한)에서 1.0 에 고정된다 — 상한 빈이 누적의 끝을 정한다.

## 5.5 Fig. 9 — 용량 분해의 닫힘 ★ 정량 그림 (패널 a · d 는 확대해서 봤다)

`[인쇄]` 굵은 선 = 측정 용량, 가는 선 = 활성 질량 손실(OCP), 점 = `L_diff` 손실까지 더한 계산. 계산 가정: "full reversible capacity" 200 / 190(PC high-V / low-V) · 205 / 195(SC), `D̃` = 5 × 10⁻¹²(적합값의 절반, "expected to drop strongly when approaching the (de)lithiated state"),
그리고 `[인쇄]` "the capacity calculated by this approach can only be considered as a **rough approximation**".

| 패널 | 측정 N = 1 → 40 | 가는 선 N = 1 → 40 | 점(모델) vs 측정 |
|---|---|---|---|
| (a) PC low-V | ≈147 → **≈70** | ≈151 → ≈113 | **전 구간 위**: N = 1 +27(≈174) · N = 20 ≈+20 · N = 30 ≈+12 · N = 40 ≈+14. 점이 N < 11 에서 **가는 선보다 위**(경로 손실이 음수) |
| (b) PC high-V | ≈148 → ≈70 | ≈148 → ≈110 | 대체로 겹침(±5–10), N = 4 한 점 ≈162 |
| (c) SC low-V | ≈174 → ≈160(**N = 38** 에서 끝) | ≈176 → ≈170 | 겹침(±5) |
| (d) SC high-V | ≈179 → ≈138 | (N ≈ 12 부터 보임) ≈157 → ≈152 | N = 1 ≈151(**−28**) · 중반 겹침 · N = 40 ≈124(**−14**) |

- ⇒ **"good agreement for all the samples" 는 (b)(c) 에서만 선다.** (a) 의 N = 40 잔차 ≈14 는 그 조건 전체 감쇠(≈77)의 **≈18 %**, (d) 의 −14 는 전체 감쇠(≈41)의 **≈34 %** — 부호가 반대라 한 방향 누락 항으로도 설명되지 않는다.
- ⚠ **가는 선의 상대 감소가 Fig. 6 과 다르다**(D2): (a) 113/151 = **0.75** ↔ Fig. 6 **0.63** · (b) 110/148 = **0.74** ↔ **0.62** · (c) 170/176 = **0.97** ↔ **0.91**. 가는 선이 `q_full · m_act` 도 아니다(N = 1 에서 190 이 아니라 ≈151).
  구성은 Fig. S9(미열람)에 있다 — **본문만으로는 두 그림의 활성 질량이 같은 양인지 확인되지 않는다.**
- `[해석]` 닫힘의 자유 손잡이는 넷(full capacity 두 값 · `D̃` 5 × 10⁻¹² · "rough" 계산)이고 조건마다 따로 정할 수 있다. 계면 저항(`R_ct`) 의 용량 몫은 분해에 **항이 없다**(G7) — (a) 의 양의 잔차가 그 자리일 수 있고, (d) 의 음의 잔차는 그것으로 설명되지 않는다.

## 5.6 Fig. 4 — SEM (정성)

`[도표]` 분말: PC 구형 2차 입자 직경 ≈8–12 µm · SC 분리된 결정 ≈1–3 µm. 단면: 신품 PC 입자 경계 치밀, 사이클 뒤 PC 에 입계 균열(검정) · 입자 간 전자 접촉 손실(빨강 ×2) · NCM–SE 박리(파랑 ×1); SC 에도 빨강 · 파랑 각 1.
**분율 · 면적 · 사이클 수 0** — 존재 증명이다(23호와 같은 층).

---

# 6. ★★★ 9호의 인용 · 기각 대조

| 9호 `[인쇄]` | 이 편 | 판정 |
|---|---|---|
| "quantified the changes of active material in the cathode and tracked the length of the lithium diffusion path in a 40-cycle charge/discharge by means of relaxed open-circuit potential and EIS-PSD" | §3 · §4 · Fig. 6 · 8 | ✅ 정확 |
| "Their findings corroborated the predominant influence of chemical-mechanical evolution on battery capacity degradation" | `[인쇄]` "well explained by exclusively chemo-mechanical effects" | ✅ (단 "exclusively" 가 "predominant" 로 약해졌다 — 9호 쪽이 더 조심스럽다) |
| "**the error between the experimental result and the quantitative analysis is relatively large**" | 본문 "good agreement for all the samples" ↔ `[도표]` Fig. 9 (a) +12…+27 · (d) −14…−28 mAh g⁻¹ | ✅ **9호가 그림에 맞고 본문이 그림과 어긋난다.** 크기는 우리가 처음으로 읽었다 |
| "it is only a quantitative method without a corresponding aging model" | 연속체 모델 0 | ✅ |

`[해석]` 9호의 기각은 정당하다 — 그러나 9호 자신의 대안(적합으로 지분을 정하는 결합 모델)은 **같은 합(`θ·ε_p`)을 파라미터 하나로** 받는다(9호 digest · 37호 §9). 이 편은 적어도 두 채널을 **따로 쟀다.**

---

# 7. `[재현]` 검산 — 맞는 것과 안 맞는 것

| 항목 | 인쇄 | 재현 | 판정 |
|---|---|---|---|
| 활물질 담지 | ≈11 mg cm⁻² | 12 × 70/101 ÷ 0.785 = 10.6 | ✓ |
| 음극 조성 | ≈33 at% Li | Li 1.335 mg = 0.192 mmol · In 46.8 mg = 0.407 mmol → 32.1 at% | ✓ |
| 첫 충전 뒤 음극 조성 | — | + 0.0698 mmol(≈225 mAh g⁻¹ × 8.32 mg) → **39.1 at%** | In+LiIn 2상역 안(18호 37.7–40 · 17호 40 과 같은 대역) |
| Li 재고 / 이동 전하 | — | 5.15 / 1.87 mAh = **×2.75** | LLI 가 용량에 안 보이는 설계 |
| `√(t_c D̃)` (0.05 C, 20 h) | ≈6 µm | 6.0 µm | ✓ |
| 신뢰 한계 | 1.8 / 4.5 µm | 1.83 / 4.47 | ✓ |
| `L_diff,50` 배수 PC | "3 to 4" | 3.5 · 3.0 | ✓ |
| `L_diff,50` 배수 SC | "<2" | 1.6 · **2.0** | ✗ 절반 |
| `C_diff/m` | 520 mAh V⁻¹ g⁻¹ | `F/M`(NCM811, M = 97.28) = 275.5 mAh g⁻¹ ÷ 0.38 V = **725** | ✗ ×0.72 — 520 × 0.38 = 198 mAh g⁻¹ 즉 **실용 용량 ≈200 을 `x` 단위로 쓴 값**으로 보인다(정의 미기재, D6) |
| 이완 1 h vs 확산 시상수 | — | PC N = 40: 12.8–17.4 h (`D̃` 5 × 10⁻¹²) · 6.4–8.7 h (10⁻¹¹) | 이완이 **한 자릿수 짧다** |
| OCP 10 mV → 활성 질량 | — | 0.01/0.38/Δx(0.6–0.7) = **3.8–4.4 %** | SC 40 사이클 손실의 절반 크기 |

`[해석]` `C_diff` 가 ×0.72 작게 들어갔다면 반무한 영역의 `L = (측정 곱)·C_diff·√D̃` 도 ×0.72 — **절대 `L_diff` 는 불확정, 비(×3–4)는 이 오차에 불변**이다(오차가 사이클 불변이면).

---

# 8. ★★★★ Q1 상세 — 37호 "ASSB truth 가 카드 물음을 시험하려면 필요한 5 가지" 와의 대조

| 37호 요구 | 이 편 | 판정 |
|---|---|---|
| ① 용량에 곱해지되 `ε_p` 와 별개인 `θ` | `m_act` 는 `θ·ε_p` 합 하나 | ❌ |
| ② 비연결 입자가 자기 SOC 의 리튬을 붙듦(`_li`) | "cannot contribute to the OCP" 까지, 보유 리튬 0 자 · LLI 는 설계상 안 보임 | ❌ |
| ③ 죽은 부피가 전해질이 되지 않음 | 해당 없음(모델 0) | — |
| ④ `θ` 에만 반응하는 조작 | SC ↔ PC 형태 대조(입도 · 재소성 교락) · 압력 되돌림 0 | ⚠ 부분 |
| ⑤ 면적에 비례하는 이중층 | 회로에 `C_int`(= `C_dl`) 있음, 사이클 값 0 | ❌ (재료는 있었다) |

⇒ **1/5 부분.** 그러나 이 편이 새로 주는 것 — **요구 ⑥ 후보**(`[해석]`): **이완 게이지의 평형 조건**. 활성 질량을 이완 OCP 로 재는 순간 이완 시간 ≥ `L²/D̃` 가 요구되고, 접촉 손실(`L` 증가)이 그 조건을 스스로 깬다.
Truth 설계에서는 "OCV 관측이 몇 시간 이완 뒤의 것인가" 를 파라미터로 두어야 `θ` 손실이 **질량 채널과 동역학 채널 사이에서 어떻게 새는지**를 시험할 수 있다.

---

# 9. ★★★ 곱 축퇴 처방 — 스물한 번째 적용

`[인쇄]` 곱의 원천: `θ·ε_p`(활성 질량) · `L²/D̃`(확산 시상수) · 반무한 `L/(C_diff√D̃)`. 셀: NCM811 PC/SC | Li₆PS₅Cl | In/InLi, 40 사이클 × 4 조건.

### 입력 점검

- **1단계 `R_CT·C_dl`** — ⚠ 재료는 있고 값이 없다. 회로(Fig. 7a)에 `R_int ∥ C_int` 가 있고 매 사이클 적합됐다(고주파부). **인쇄 0**(G7).
- **2단계 면적 대조군** — SC ↔ PC 가 면적(입도)을 바꾸지만 BET 는 PC 만(0.2 m² g⁻¹). ❌
- **3단계 `Ea`** — 25 · 60 °C 두 온도가 **신품 `D̃`** 에만(10⁻¹¹ ↔ 6 × 10⁻¹¹). 사이클 전후 ❌.
- **4단계 `C` 상한** — `C_diff/m` 520 mAh V⁻¹ g⁻¹ 은 인쇄, `C_dl` 0. ❌
- **율 스윕 줄** — low-V 0.1 C ↔ high-V 0.3 C 는 **컷오프와 교락**(4.25 ↔ 4.5 V). ❌ 대신 **이완 OCP 두 점**이 율 무관 게이지로 `η` 를 뗀다(아래 새 줄).
- **SOC 추종 상 분율(22호 줄)** — 이 편이 `[인쇄]` 로 **대안으로 언급만** 한다(ref 47 operando XRD, "requires expensive … equipment"). ❌
- **외부 액체 기준 줄** — **기준 OCP–x 곡선을 액체셀에서** 수입(G5) — 29호(`D_LIB`)와 **다른 인자**를 수입한 표본: 곱의 인자가 아니라 **게이지의 눈금**을 액체에서 가져왔다.

### ★★★ 이 적용이 처방에 더하는 것

1. **새 줄 — 이완 OCP 두 점 = 연결 질량(`ΔQ/Δx`)**: 평탄 상대극 셀에서 방전 전후 이완 OCP 로 `θ·ε_p` 를 **율과 무관하게** 사이클마다 잰다 → 곱에서 `η` 를 뗀다(율 스윕 줄의 대체).
   **조건**: (i) 이완 ≥ `L²/D̃`(이 편 1 h ↔ PC 후반 ≈13–17 h ✗) (ii) 상대극 평탄 폭 ≪ 질량 분해능(±10 mV ≈ ±4 %) (iii) 기준 OCP–x 가 같은 계면계. **`θ` 와 `ε_p` 는 여전히 한 칸.**
2. **새 줄(↳ 경고) — 저주파 꼬리의 반무한 곱 `L/(C_diff·√D̃)`**: 꼬리가 용량성 극한에 닿지 않으면 확산 경로 · 활성 질량 · 확산계수가 **한 곱**이고, `C_diff` 를 다른 채널에서 고정하면 두 채널이 **곱으로 거래**한다.
   용량성 극한(`C_diff` 단독)에 닿으면 그것이 **OCV 와 독립인 활성 질량** — 이완 게이지의 교차 검사가 된다(이 편은 닿지 않았고, 고정했다).
3. `[해석]` 37호 `A_eff ↔ k` 항등의 **확산 판**: 반무한 꼬리에서 `C_diff/L ∝ 접촉 면적` 이므로 면적 손실 ↔ `D̃` 감소가 `A·√D̃` 곱이다(30호 Randles–Ševčík · 31호 ICI 와 같은 부류, 이번에는 **사이클 해상**).

### ⚠ 이것이 곱을 푼 것은 아니다

두 채널은 `θ·ε_p` 합과 `η_diff` 를 가른다 — 카드의 곱(전자 비연결 ↔ 진짜 LAM)은 한 채널 안에 그대로 있다.

---

# 10. Q5 — 열네 번째 형태 "고정 전위가 게이지의 영점이다"

- `[인쇄]` "an In/InLi anode **with fixed potential**" — 기준 전위 상수가 **측정 원리의 전제**로 인쇄된 첫 편(지금까지는 환산 상수 · 차감 · 무시였다). 값 −0.62 V(ref 42), 검증 0.
- `[재현]` 조성은 32.1 → ≈39.1 at% 로 2상역 안(조건 (1) ✓). 조건 (2)(분리막 쪽 LiIn 국소 고갈)는 판정 불가 — **Li 박 12.5 mm² 가 In 박 64 mm² 의 1/5 면적**이고 합금 균질화 확인 0.
- `[재현]` 평탄 폭 상한 ±10 mV(17호) ⇒ 활성 질량 ±≈4 % — **SC 의 전체 신호(9–10 %)와 같은 자릿수**. PC(37–38 %)에서는 작다.
- 칸 이동 없음(기준을 재지도 소거하지도 않았다).

---

# 11. 채움표 행 (Q1–Q8)

| Q | 판정 |
|---|---|
| **Q1 정량** | **이동 없음 — `θ(N)` 0/38.** 측정 계열은 있다(`m_act(N)`, Fig. 6) — 그러나 `θ·ε_p` 합이고 **용량에서 역산**(22호 기준 미달), 배정은 "We suggest" + 형태 대조 + 액체셀 TEM 인용. **첫 `θ·(1−LAM)` 합 계열 1/38**. SEM 은 존재 증명 |
| **Q2 독립관측** | **+0.5** — 이완 OCP ↔ 저주파 EIS 꼬리 두 채널이 사이클마다 "OCP-비활성 질량" 과 "확산 경로 연장" 을 가른다(22호 신품 `θ ↔ η` 의 **노화 · 사이클 해상판**) + 동역학 불변 M/H2 봉우리(정성). 반 칸: 카드 핵심 분할 0 · 채널이 `C_diff` 입력으로 묶임 · 이완 1 h ≪ `τ` · n = 1 |
| **Q3 라벨층위** | 층 하나 — **measured-electrochemical(두 점 이완 OCP, 액체 기준 곡선 수입) + fitted(GA 다중 시작, 중앙값 ± 최대 편차 — 신품 한 판에만)**, 조건당 셀 1 개, Fig. 6 · 8 · 9 오차 막대 0, **닫힘 그림에 잔차 0** |
| **Q4 유일성** | **0/38 — 서른 번째 성질 "식별 한계를 식으로 인쇄하고, 결론의 수를 그 한계 밖에 두었다"**. 식별 집합에 용량 스케일 없음(`C_diff` 고정) · 다중 시작 폭은 신품만 · Fig. S8 미열람 |
| **Q5 Li-In** | 이동 없음 — **열네 번째 형태 "고정 전위가 게이지의 영점이다"**(§10) |
| **Q6 압력** | 이동 없음 — 제작 380 MPa 1 min · 운전 ≈70 MPa 고정 유지(보고 · 통제, 한 값) |
| **Q7 dead Li** | 해당 없음(In/InLi) |
| **Q8 화학·OCP** | 이동 없음 — NCM811 PC/SC(기존 화학). `∂E/∂x` = 0.38 V @ x = 0.66(3.77 V) **한 점, ref 19 에서 빌림**; `C_diff/m` 이 그 정의와 ×0.72 어긋남(D6) |

---

# 12. 어긋남 (실제로 어긋난 것만)

| # | 어디 | 무엇 |
|---|---|---|
| **D1** | 본문 p. 11 ↔ Fig. 9a · 9d | "reproduced in good agreement for **all** the samples" ↔ (a) 모델 +12…+27 · (d) −14…−28 mAh g⁻¹ `[도표]`. 9호 "relatively large" 가 그림에 맞다 |
| **D2** | Fig. 9 가는 선 ↔ Fig. 6 | 가는 선의 상대 감소 0.75 · 0.74 · 0.97 ↔ Fig. 6 활성 질량 0.63 · 0.62 · 0.91 `[도표]`. 구성(S9) 미열람 |
| D3 | 본문 p. 10 ↔ Fig. 8d | "SC … only by a factor of <2" ↔ 1.3 → 2.6 µm = 2.0 |
| **D4** | Fig. 5d ↔ Fig. 9a | 같은 공칭 조건(PC · 0.1 C · 2.6–4.25 V)인데 N = 40 용량 ≈107 ↔ ≈70 mAh g⁻¹ `[도표]` — 셀 간 차 또는 프로토콜 차(9a 는 매 사이클 3.77 V CV + EIS + 1 h 이완) 언급 0. 이 차(≈37)는 Fig. 9a 의 경로 손실 몫(≈29)보다 크다 |
| D5 | Fig. 7a ↔ 본문 | 라벨 `R_int` · `C_int` ↔ 본문 `R_ct` · `C_dl` |
| **D6** | p. 8 `C_diff/m` | 520 mAh V⁻¹ g⁻¹ ↔ 자기 정의(`F c_o V ∂x/∂E`) + 인쇄 0.38 V 로 725 — ×0.72 |
| D7 | Fig. 6 SC low-V | 정규화 활성 질량 ≈1.005(N 6–9) — 1 초과, 본문 0 |
| D8 | 본문 p. 8 ↔ Fig. 6 | "active mass loss appears to be enhanced by the harsh high-V conditions" ↔ PC N = 40 에서 0.62 ↔ 0.63(차는 초기 오프셋) |
| D9 | Fig. 9c | 캡션 "over 40 cycles" ↔ 패널 (c) 는 ≈38 사이클에서 끝남 |
| D10 | 방법 p. 5 | 조성비 "70:30:01"(합 101) |
| D11 | Fig. 5d | PC 곡선 계단 두 곳(≈31 · ≈58 사이클), 설명 0 |

---

# 13. 그림 — 무엇을 봤나

크로퍼 9 장(본문 Fig. 1–9, SI 0). **6 장 봤다: Fig. 4 · 5 · 6 · 7 · 8 · 9**(Fig. 9 는 패널 a · d 를 확대해서 한 번 더, b · c 도 확대).
**안 본 것: Fig. 1(모식도) · 2(원통/구 확산 스케치) · 3(모사 임피던스)** — 셋 다 정량 주장을 떠받치지 않는 모식 · 모사 그림이다. SI 그림 S1–S9 는 파일이 없다.
본문과 어긋난 그림: **Fig. 9(D1 · D2 · D9) · Fig. 8d(D3) · Fig. 5d ↔ 9a(D4) · Fig. 7a(D5) · Fig. 6(D7 · D8)**.
정량 그림(Fig. 6 · 8 · 9)은 전부 봤다.

---

# 14. 참고문헌 중 후속 후보 (58 편 중, 제목 · 서지 기준 — 미열람)

| 서지 | ref | 왜 | 축 |
|---|---|---|---|
| **Bartsch, Kim, Strauss, de Biasi, Teo, Janek, Hartmann, Brezesinski, *Chem. Commun.* 55, 11223 (2019)** | 47 | 이 편이 **대안으로 기각한 operando XRD 활성 질량** — OCV 와 독립인 `θ·ε_p` 게이지(22호 계보). 같은 양을 두 게이지로 재면 이완 편향(§3.2)을 잰다 | Q1 · Q2 |
| **Ruess, Schweidler, Hemmelmann, Conforto, Bielefeld, Weber, Sann, Elm, Janek, *JES* 167, 100532 (2020)** | 19 | `D̃` · `∂E/∂x` 0.38 V · OCP 표류 "few mV per day" 의 출처, 29호 ref 26 과 같은 편 | Q5 · Q8 |
| Fantin, Trevisanello, Ruess, Pokle, Conforto, Richter, Volz, Janek, *Chem. Mater.* 33, 2624 (2021) | 41 | SC 분리 · 재소성 절차 — SC ↔ PC 대조가 `θ` 전용인지(표면 화학 변화) | Q1 (c) |
| Lin, Markus, Nordlund, Weng, Asta, Xin, Doeff, *Nat. Commun.* 5, 3529 (2014) | 14 | 상전이형 LAM 을 "low" 로 뺀 **유일한 근거** — 액체셀 TEM 2 nm | Q1 배정 |
| Han, Jung, Kwak, Jun, Kwak, Lee, Hong, Jung, *Adv. Energy Mater.* (2021) 2100126 | 9 | "(electro-)chemical side reactions can also influence the contact area" — 계면 화학 ↔ 접촉 면적 얽힘 | Q1 · Q2 |
| Schönleber & Ivers-Tiffée, *Electrochem. Commun.* 61, 45 (2015) · Schönleber et al., *Electrochim. Acta* 243, 250 (2017) | 32 · 31 | DDC(미분 용량 분포) 원전 — 분포 역문제의 식별성 | Q4 |
| Jung, Kim, Kim, Jun, Yoon, Jung, Sun, *Adv. Energy Mater.* 10, 1903360 (2019) | 8 | NCM 형태 · 접촉 손실(황화물) | Q1 |
| Santhosha, Medenbach, Buchheim, Adelhelm, *Batteries & Supercaps* 2, 524 (2019) | 42 | In/InLi −0.62 V 의 출처 | Q5 |

큐 38 · 39 는 인용되지 않는다(38 번 Yu 2024 · 39 번 Lai 2025 모두 이 편 뒤).

---

# 15. 이 digest 가 주장하지 않는 것

1. **이 편의 결론(PC 의 용량 감쇠가 화학-기계 열화 때문)이 틀렸다고 하지 않는다.** 주장은 "그 절차가 접촉 손실을 `LAM_PE` 와 가려낸 절차가 아니다" 와 "닫힘이 두 패널에서 안 맞는다" 까지다.
2. **이완 1 h 편향의 크기를 쟀다고 하지 않는다.** 방향과 자릿수(`τ` ≈13–17 h)만 `[추론]` 이다 — 입자 사이 리튬 교환 · 방전 뒤 이완 시간(G2)이 모르는 채로 있다.
3. **Fig. 9 가는 선과 Fig. 6 의 불일치를 오류라고 하지 않는다** — 구성이 S9 에 있고, 보지 않았다.
4. **사이클 EIS 가 25 °C 였다고 단정하지 않는다** — 적합에 쓴 `D̃` 에서 추론했다.
5. **`C_diff/m` 520 이 틀렸다고 하지 않는다** — `x` 의 정의(이론 ↔ 실용 창)가 미기재다.
6. **SC ↔ PC 대조가 표면 재구성 가설을 반박한다고 하지 않는다** — 비표면적 논거는 우리 것이고, 재소성이 그 논거를 약하게 한다.

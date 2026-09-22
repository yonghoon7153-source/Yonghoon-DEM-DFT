---
title: "Yu, Choi, Dunham, Ghahremani, Liu, Lindemann, Garver, Barchiesi, Farahati, Kim 2024 — Time-resolved impedance spectroscopy analysis of aging in sulfide-based all-solid-state battery full-cells using distribution of relaxation times technique (J. Power Sources 597, 234116)"
source_url: local-upload/38._Time-resolved_impedance_spectroscopy_analysis_of_aging_in_sulfide-based_all-solid-state_battery_full-cells_using_distribution_of_relaxation_times_technique.pdf
source_url_si: local-upload/38._Sup_Time-resolved_impedance_spectroscopy_analysis_of_aging_in_sulfide-based_all-solid-state_battery_full-cells_using_distribution_of_relaxation_times_technique.docx
source_url_note: "본문 8 쪽 + SI 가 **.docx** (7,607 자 + 그림 S1-S5 5 장). 크로퍼는 .docx 를 못 읽으므로 zipfile 로 word/media/image1-5.png 를 직접 꺼내 fig_s1-s5.png 로 등록했다 (figures.json 14 항목 = Fig. 1-8 + Table 1 + Fig. S1-S5, **누락 0**). 산업체(Schaeffler) 주도 논문이고 `[인쇄]` 'The authors do not have permission to share data.' — 파라미터 표가 아예 없다."
source_doi: 10.1016/j.jpowsour.2024.234116
source_license: "(c) 2024 Elsevier B.V. All rights reserved (open access 아님)"
pdf_sha256: 407b42abfe5275791998a7acf9b1a8f6f81bdfe6b1d2050eb312d448302d209e
si_sha256: fd7ffdc06ebd5280d17a7c203083248d944783e2a421651b981895b4ac28e98f
ingested: 2026-09-22
sha256: 5ea4dcc369821bf954266d209740a94754080e61774eba0e12a0fa65913257b3
---

# 수집 목적

**Chan-Yeop Yu ᵃ,\*** (교신, `yucny@schaeffler.com`), **Junbin Choi ᵇ**, **Joshua
Dunham ᵃ**, **Raziyeh Ghahremani ᵃ**, **Kewei Liu ᵃ**, **Paul Lindemann ᵃ**,
**Zaine Garver ᵃ**, **Dominic Barchiesi ᵃ**, **Rashid Farahati ᵃ**,
**Jung-Hyun Kim ᵇ,\*\*** (교신, `kim.6776@osu.edu`)
— 소속 [a] **Corporate Competence Center – America, Schaeffler Transmission
Systems LLC., Wooster, OH 44691, USA** (산업체) · [b] Department of Mechanical
and Aerospace Engineering, **The Ohio State University**, Columbus, OH 43210.

**"Time-resolved impedance spectroscopy analysis of aging in sulfide-based
all-solid-state battery full-cells using distribution of relaxation times
technique"**, *Journal of Power Sources* **597** (2024) 234116,
doi `10.1016/j.jpowsour.2024.234116`.
`[인쇄]` Received 1 August 2023; revised 19 January 2024; accepted 22 January
2024; available online 6 February 2024. `[인쇄]` "0378-7753/© 2024 Elsevier
B.V. **All rights reserved.**" (**open access 아니다**).
`[인쇄]` Funding: "The funding grant was **internally funded by the Schaeffler
group**." `[인쇄]` "The authors declare that they have **no known competing
financial interests**…"
★★ `[인쇄]` Data availability: **"The authors do not have permission to share
data."**

본문 **8 쪽** + **SI(`.docx`) 7,607 자 + 그림 S1–S5** 전문의 절별 해체분석.

> ⚠ **이 digest 의 표기 4분**: `[인쇄]` = 지면(본문 또는 SI)에 문자 그대로 있는 것.
> `[도표]` = 그림을 실제로 열어 눈으로 읽은 것(판독 오차를 같이 적는다).
> `[재현]` = 원문의 값으로 우리가 계산한 것. `[해석]` = 우리가 추론한 것.
> **`[재현]`·`[해석]` 은 원문에 없다.**

★ **크로핑 결과와 실제로 본 것**:
- 본문 PDF → `wiki/tools/extract_figures.py` 가 **9 장**(Fig. 1–8 + Table 1).
  논문의 도표는 **Figure 1–8 + Table 1 이 전부**이므로 **누락 0**.
- ★★ **SI 는 `.docx` 라 크로퍼가 읽지 못한다.** `zipfile` 로 `word/media/`
  에서 **image1–5.png 5 장을 직접 꺼내** `fig_s1.png`–`fig_s5.png` 로 넣고
  `figures.json` 에 caption 과 함께 등록했다 (총 **14 항목**). SI 의 그림
  개수도 **Figure S1–S5 = 5 장**으로 정확히 일치한다.
- **실제로 열어 본 것은 13 장 중 12 장** — 본문 **Fig. 1 · 2 · 3 · 4 · 5 · 6 ·
  7 · 8** (8/8 전부) + SI **Fig. S1 · S2 · S3 · S4 · S5** (5/5 전부).
  Table 1 은 이미지로 읽지 않았다(PDF 텍스트가 정확 — §11 에 전문 전사).
- 추가로 **Fig. 2 의 DRT 패널 (a)(b)**, **Fig. 3(c)**, **Fig. 4(d)**,
  **Fig. S3 의 DRT 두 패널**을 **확대 렌더로 다시** 읽었다 — 봉우리 **개수와
  높이**가 이 흡수의 본체이기 때문이다. 그 확대가 §5·§9·§13 의 근거다.

---

# 0. 원문에 없어서 확인이 필요한 것 (먼저 적는다)

| # | 공백 | 왜 걸리는가 |
|---|---|---|
| **G1** | ★★★ **정규화 파라미터(λ)가 없다. 정규화라는 단어 자체가 없다.** 본문 + SI 전수에서 `regulariz*` **0 회** · `lambda`/`λ` **0 회** · `L-curve` **0 회** · `GCV` **0 회** · `cross-valid*` **0 회** · `RBF`/shape factor **0 회** · discretization 선택 **0 회**. DRT 계산에 대해 적힌 것은 `[인쇄]` "DRT was computed via **MATLAB-based DRT calculation code developed by T.H. Wan et al. [16]**" 한 줄과 SI 의 같은 한 줄뿐이다 | **10호(Vadhva 2021) 가 남긴 공백 G4 를 이 논문은 메우지 않는다 — 공백의 존재조차 인지하지 않는다.** DRTtools 는 λ 와 RBF shape factor 를 **사용자가 넣어야** 돌아간다. 즉 **이 논문의 모든 봉우리 개수·높이는 보고되지 않은 두 개의 손잡이에 달려 있다** |
| **G2** | ★★★ **K–K(Kramers-Kronig) 검증이 없다.** `Kramers` **0 회** · `Kronig` **0 회** · `Lin-KK` **0 회** · `linearity`/`causality`/`stationar*` **0 회** | 10호의 처방 **첫 단계**다 (`[인쇄]` "their application is **recommended** to avoid … **erroneous parameter estimation**"). 10호는 `[인쇄]` "DRT analysis is **also very sensitive to experimental errors**, meaning practical precautions and data evaluation, such as K–K analysis **are essential**" 라고 적었다. **38호는 그 "essential" 을 건너뛴다** |
| **G3** | ★★★ **불확실성 어휘가 전수 0 이다.** `uncertaint*` · `confidence` · `error bar` · `standard deviation` · `uniqu*` · `identifiab*` · `ill-posed` · `condition number` · `Fisher` · `Bayes*` · `posterior` · `overfit*` · `degenerac*` · `replicate` — **본문 8 쪽 + SI 전수 14/14 항목 모두 0 회** | Q4 를 **재지 않았다**. 그런데 §13 에서 보듯 **잴 재료는 SI 에 인쇄해 놓았다** |
| **G4** | **셀 수가 어디에도 없다.** `n =` 본문 0 회 (SI 의 2 회는 수식의 `n` 차수다). 반복 측정 0, 산포 0 | 최소 **6 종의 셀**(완전지 · NMC 반쪽 · graphite 반쪽 · nano-SE 양극 · micro-SE 양극 · bare NMC 양극)이 등장하는데 **각 종에 몇 개인지 없고, 그림 사이에 같은 셀이 이어지는지도 없다** |
| **G5** | ★★ **파라미터 표가 아예 없다.** 미공개: **어느 셀이 Cl 이고 어느 셀이 Br 인지**(논문 전체가 `Li₆PS₅X (X = Cl and Br)` 로만 쓴다) · NMC:SE:AB:binder **조성비** · binder **종류** · 면적 용량/로딩(`mg cm⁻²` **0 회**) · 전극 두께 · SE 층 두께 · **N/P 비** · NMC 입도 · LiNbO₃ 코팅 두께 · **Fig. 3 의 `Ω mg⁻¹` 정규화에 쓴 질량** · 측정 온도(Table 1 의 `@ RT` 뿐) | ⚠ **산업체 주도 논문이다.** 9호(Huo 2025)는 최소한 Table 3 에 6 개 값을 `[인쇄]` "not disclosed" 로 **찍어 두었다**. **38호는 표가 없어서 구멍을 셀 기준조차 없다** — provenance 측면에서 9호보다 **뒤**다 |
| **G6** | ★★ **압력 계측 수단이 없다.** `[도표]` Fig. S1(b) 의 고정구는 **볼트·너트**다. 로드셀 · 스프링(디스크 스프링/원뿔 스프링) · 토크 규격 · 교정 **전부 없다**. 그런데 `[인쇄]` "the operating pressures of the cells **remained constant at 20 MPa**" 라고 적는다 | **볼트·너트는 정변위(constant displacement) 구속이지 정하중이 아니다.** 스택 두께가 변하면 압력이 변한다 — 5호(Doux)가 Instron 교정 로드셀을 쓴 것과 정반대. `[해석]` "20 MPa 가 일정했다" 는 **측정된 사실이 아니라 설계 의도**다 |
| **G7** | ★ **DRT 전처리가 두 가지로 서술되고 그림마다 다르게 적용됐다.** (i) Fig. 2 캡션 `[인쇄]` "DRT peaks were computed **based on the simulated Nyquist curves (green solid-line)** after subtracting the low-frequency data" (ii) SI `[인쇄]` "the fitted model is **subtracted from the measurement data**" / Fig. S5 `[인쇄]` "subtraction the diffusion tails **from the original Nyquist plot**" | **(i) 은 적합 곡선 위에서 DRT 를 돌리는 것이고 (ii) 는 실측에서 꼬리만 빼는 것이다.** 전혀 다른 절차다 → §13 D1. 그리고 **Fig. 1(b) 에는 Warburg 가 빼지지 않은 채 그려져 있다**(`Li-ion diffusion` 봉우리가 살아 있다) |
| **G8** | **열화 모드 어휘가 0 이다.** `LLI` · `LAM` · `degradation mode` · `incremental capacity` · `differential voltage` · `OCV` · `open circuit` · `GITT` · `contact loss` · `percolat*` · `tortuos*` — **전수 0 회** | 8호·10호와 같다. **이 논문의 건강도 끝까지 저항이고, 저항이 모드로 번역되지 않는다.** `contact` 은 쓰지만 `contact loss` 라는 복합어가 아니라 `contact impedance` 다 — **단위가 Ω 이지 무차원 분율이 아니다** |
| **G9** | ★ **같은 셀을 시간축으로 따라간 DRT 계열이 최장 6 점이고, 500 사이클 구간에는 DRT 가 2 점밖에 없다.** 사이클 격자가 그림마다 다르다: Fig. 2 = 4/15/48 · Fig. 3(b) = 4/26/59/81 · Fig. 3(c) = 3/29/55/81 · Fig. 5 = 4/15/26/37/48 · Fig. 6 = 3/29/55/81/107/133 · Fig. 4(b,d) = "aged(>500)" + 재가압 2 점 · Fig. 7(b,d) = "aged(500)" + 재가압 1 점 | **제목이 `Time-resolved` 다.** 그런데 **분해된 시간축의 최대 도달점은 133 사이클**이고, 500 사이클은 **끝점 2 개**로만 존재한다. `[해석]` 제목이 약속하는 것과 그림이 주는 것이 다르다 |

---

# 1. 무엇을 묻고 무엇을 답하는가

**묻는 것**: 황화물(아지로다이트 `Li₆PS₅X`, X = Cl, Br) 기반 **NMC | SE |
graphite 완전지**의 노화에서, EIS 의 겹친 시상수를 **DRT 로 풀어** 각 임피던스
원(源)을 **어느 주파수에** 귀속시킬 수 있는가.

**답의 구조**:
- §3.1 완전지 ↔ NMC 반쪽전지 ↔ graphite 반쪽전지 **세 구성을 같이 재서** DRT
  봉우리를 전극에 귀속시킨다 (Fig. 2)
- §3.2 양극 쪽 — **SE 입도 스윕**(nano ≤1 µm vs micro ≤20 µm, Fig. 3) ·
  **재가압 개입**(150 / >500 MPa, Fig. 4) · **코팅 유무**(LiNbO₃ vs bare, Fig. 5)
- §3.3 음극 쪽 — graphite 반쪽전지 (Fig. 6) + 완전지 재가압 (Fig. 7)
- §4 결론 + **Fig. 8 + Table 1 의 주파수 ↔ 물리 귀속 지도** (이 논문의 산출물)

`[인쇄]` Highlights 3 줄:
> • EIS coupled with DRT offers **non-destructive** analysis of all-solid-state batteries.
> • Identified impedance sources of **NMC/Li₆PS₅X (X = Cl, Br)/graphite full-cells**.
> • EIS – DRT combination **thoroughly elucidate** the degradation mechanisms.

`[인쇄]` 초록의 문제 진술: "Although EIS provides abundant information over cell
performance, its interpretation is often found to be **challenging due to
overlapping of time constants**. To address the complexity … the **distributions
of relaxation times (DRT) technique is employed, which facilitates
deconvolutions of the frequency domains**."

`[인쇄]` 서론의 같은 진술: "complexities in the frequency domains may cause
**misinterpretation** of the data. For example, **overlaps of neighboring
semi-circles are often misled into missing features** during analysis of Nyquist
plots [7]." (ref. [7] = Gaberšček, *Nat. Commun.* 12 (2021) 6513)

`[인쇄]` 이 연구의 자리: "Researchers have extensively utilized DRT analysis to
estimate the intrinsic properties (bulk and grain boundary) of solid electrolyte
materials and interface resistances at electrode/electrolyte configurations.
**However, limited studies have been reported for full-cell construction in
all-solid-state devices with graphite anode.**"

★★ `[해석]` **이 논문이 우리에게 특별한 이유가 이 문장에 있다.** `assb` 1–10 호의
음극은 Li-In · Li 금속 · 무음극 · Li-Si 였다. **38호가 계보 최초의 graphite 음극
ASSB 완전지다** — 즉 **액체셀 갈래(`bms-balancing/`)의 음극과 같은 재료**다.
→ §14 Q8.

---

# 2. §2 실험 — 셀과 측정 (p. 2–3)

## 2.1 재료·조립 (`[인쇄]`)

| 항목 | 값 |
|---|---|
| 양극 활물질 | **LiNbO₃-coated LiNi₀.₆Mn₀.₂Co₀.₂O₂ (NMC)** = NMC622 |
| 음극 활물질 | **graphite** |
| 고체전해질 | **argyrodite-type Li₆PS₅X (X = Cl and Br)** — 전해질층 + 전극 내 이온전도 성분 |
| 양극 슬러리 | NMC + Li₆PS₅X + **Acetylene Black** + **polymer binder** → **Al 박**에 코팅, overnight 건조 |
| 음극 슬러리 | graphite + Li₆PS₅X + binder + solvent → **Cu 박**에 코팅 |
| 분위기 | **Ar glovebox** 전 공정 |
| SE 량 | **100 mg** 을 in-house die cell 에 투입 (Fig. S1) |
| 전극 | **직경 10 mm** 로 컷 |
| 제작 압력 | `[인쇄]` **"high-uniaxial pressure (over 500 MPa)"** |
| 운전 압력 | `[인쇄]` **"a relatively low pressure of 20 MPa"** (cell fixture 로 조임) |
| 반쪽전지 | 상대극을 **indium-lithium (In–Li)** 로 교체 |

## 2.2 전기화학 (`[인쇄]`)

| 항목 | 값 |
|---|---|
| 사이클 | **C/3** (Arbin **LBT20184**) |
| 전압창 — 완전지 | **2.7–4.2 V** |
| 전압창 — 양극 반쪽 | **2.1–3.7 V** |
| 전압창 — 음극 반쪽 | **−0.595 – 0.9 V** |
| EIS 주파수 | **2 MHz – 0.1 Hz** |
| EIS 진폭 | **정전압 10 mV** (Gamry **Interface 5000E**) |
| EIS SOC | **50 % SOC 를 매 측정마다 유지** |
| EIS 연결 2 종 | (i) potentiostat **직결** (ii) **battery cycler 를 거쳐** 사이클 절차 뒤 자동 측정 |
| DRT | `[인쇄]` **"MATLAB-based DRT calculation code developed by T.H. Wan et al. [16]"** (= DRTtools) |

★ `[재현]` **Li–In 오프셋이 숫자로 들어와 있다.** 음극 반쪽전지 하한이
**−0.595 V vs In–Li** 인데, graphite 완전 리튬화가 ≈0.005–0.02 V vs Li/Li⁺
이므로 In–Li 기준의 2상 공존 전위를 **≈0.60–0.62 V vs Li/Li⁺** 로 두면 맞는다.
양극 반쪽 **2.1–3.7 V vs In–Li** 에 같은 오프셋을 얹으면 **≈2.72–4.32 V vs
Li/Li⁺** 이고, 완전지 창 **2.7–4.2 V** 와 정합한다.
⚠ **그러나 논문은 이 오프셋을 한 번도 적지 않는다** — `indium` **1 회**(조립 문장),
`In–Li` **7 회**, 그리고 **기준 전위의 안정성 논의 0**. 4호(Shi 2020)가 0.6 V 를
고정 가정한 것과 **같은 형태**다. → §14 Q5.

⚠⚠ `[인쇄]` 진폭이 **정전압 10 mV** 다 — 10호의 선형성 기준 `[인쇄]` "typically
<50 mV" 를 **지킨다**. (10호가 Kamaya 2011 의 100–500 mV 를 비판한 것과 대조.)
**이 항목 하나는 38호가 잘 했다.** 다만 **K–K 로 확인하지 않았다**(G2).

## 2.3 ★★★ SI 의 DRT "이론" — 이 논문의 방법론적 구멍이 여기 있다

SI `[인쇄]` 전문 요약 (Eq. 1–9, Fig. S4):
> "The DRT calculation method is considered based on **establishing the
> equivalent circuit model (ECM)**. … This charge barrier can be modeled as an
> ECM, which is an RC circuit. Individual RC circuit has different time
> constants, so we can **distinguish** the cell's internal impedance …"
>
> Eq. (1) `Z(ω) = R₀ + Z₁ + Z₂ + Z₃ + ⋯ + Zₙ`
> Eq. (5) `Z = γ(τ) / (1 + jωτ)`
> Eq. (6) `Z(ω) = R₀ + Σₙ γ(τₙ)/(1+jωτₙ)`
> Eq. (7) `Z(ω) = R₀ + ∫₀^∞ γ(τ)/(1+jωτ) dτ`
> Eq. (8) 이상: `τ = RC` · Eq. (9) 실제: `τ = RQₙ` (CPE)

그리고 ★★★ **이 문장이 나온다**:
> `[인쇄]` "From the obtained experimental values, real impedance (Z′), imaginary
> impedance (Z″), and frequency (ω) are given … And we can compute the simulated
> value of `Z_DRT` … **by fitting the given observational data, `Z_EXP`. The
> well-fitted `Z_DRT` can represent the actual physics in the system**, and it is
> able to provide the relaxation time. … **The detailed approximation theory has
> been described by many researchers, and this document does not cover the
> theory.**"

★★★★ `[해석]` **이것이 10호가 경고한 바로 그 지점의 정반대 진술이다.**
10호: `[인쇄]` "data inversion is **mathematically ill-posed, requiring
regularization methods**" · "**very sensitive to experimental errors**".
38호 SI: DRT 를 **보통의 적합 문제**로 소개하고, **"잘 맞으면 그것이 계의 실제
물리를 나타낸다"** 고 쓴다. 그리고 **이론은 다루지 않겠다고 선언한다.**
→ **역문제의 비유일성이 이 논문의 인식 지평에 없다.** §13 · §14 Q4.

⚠ 그리고 이것은 10호가 `[인쇄]` "the inclusion of more elements will tend to
improve the fit" 로 미리 적어 둔 함정과 **같은 함정의 연속형**이다 — Eq. (7) 의
`γ(τ)` 는 **무한 차원**이므로 적합도는 항상 개선될 수 있고, 무엇이 답을 유한하게
만드는가가 **정규화**인데, 그 단어가 이 논문에 없다.

## 2.4 SI 의 전처리 — Warburg 빼기

`[인쇄]` "The acquired EIS curves were employed **directly** in the DRT
calculation; **however, multiple EIS curves underwent additional processing
steps** in case the EIS curve has a large Warburg element."
`[인쇄]` "recognizing that the Warburg element **is not considered an intrinsic
component of the cell impedance**, it is recommended to **exclude** the Warburg
element during the DRT calculation."
`[인쇄]` 2 단계: ① 실측 곡선을 "a **specified** model" 로 적합 ② 적합 모델을
측정 데이터에서 뺀다.

`[도표]` **Fig. S5** (실제로 봤다): 3 칸 만화. (1) 원 Nyquist — **원호 2 개 +
꼬리** (2) `Z_W` 를 점선으로 적합 (3) 빼고 난 결과(파란 점선).
★ **(3) 에서 파란 점선은 꼬리만 달라진 것이 아니라 두 번째 원호의 우측 절반도
원본(빨강)에서 벗어난다.** `[해석]` **Warburg 빼기가 중주파 원호의 모양까지
바꾼다** — 10호의 `[인쇄]` "the data must be bounded (via **somewhat arbitrary
data preprocessing**)" 가 그림으로 실현된 것이다.
⚠ 그리고 `[인쇄]` "a **specified** model" 이 무엇인지 끝내 안 적는다 — 어떤
Warburg 형(유한/반무한), 어떤 회로에 얹어서, 어떤 가중으로 적합했는지 0.

---

# 3. §3.1 세 구성으로 봉우리를 전극에 귀속시킨다 (Fig. 2)

## 3.1 본문이 말하는 것 (`[인쇄]`)

| 구성 | Nyquist | DRT 봉우리 (본문 서술) |
|---|---|---|
| **NMC/graphite 완전지** | "two distinct semi-circles at the intermediate frequency and a straight line at low frequency". 1st: **>50 kHz**, 2nd: **50 kHz → 100 Hz** ("rapid growth with increasing cycle numbers") | **P1 ≈ 1.2 × 10⁵ Hz** (1st 원호), **P2 ≈ 5 kHz**, **P3 ≈ 500 Hz** (둘 다 2nd 원호). "**The P3 exhibits significant growth** … majority of the impedance growth was attributed to the increase of P3" |
| **NMC/In–Li 반쪽** | "similar pattern with the full-cell result" | **P1 (~10 kHz)**, **P2 (10⁴–10³ Hz)**, **P3 (10³–10² Hz)**. "the growth of P3 being notable" |
| **graphite/Li 반쪽** | — | "**two major DRT peaks**: **P1 (1.3 × 10⁵ Hz)** … and **P2 (10⁴–10³ Hz)**. **P3 is still observed** in the half-cell, but its magnitude remains relatively small" |

`[인쇄]` P1 의 귀속: "(i) impedance from solid electrolyte and (ii) **an
artificial effect due to electrical noise or resistance from instrument set up
such as cable resistances**." 근거 둘 — **Fig. S2**(−20 °C 단순 SE 셀에서
grain-boundary 원호가 >100 kHz) 와 **Fig. S3**(배선을 바꾸면 P1 이 고주파로
이동; `[인쇄]` "This phenomenon has also been reported by Ke et al. [17]").

`[인쇄]` P2·P3 의 귀속: "Both P2 and P3 are considered as **interfacial
impedance of each electrode** since they are in the intermediate frequency
ranges. The significant growth of P3 impedance was **predominantly attributed to
cathode**."

## 3.2 ★★★ `[도표]` Fig. 2 — 실제로 열어서 확대해 본 것

**(a) 완전지** (Nyquist `Z_real` 0–90 Ω, `Z_imag` 0 – −30 Ω; 사이클 4 / 15 / 48;
`simulated` 녹색 실선 병기; 화살표 **50 kHz**, **100 Hz**)
DRT 축: `g(τ) / Ω`, 0–40; `Frequency / Hz`, 10⁶ → 10⁻².

| 특징 | 4 cycle (검정) | 15 cycle (빨강) | 48 cycle (파랑) |
|---|---|---|---|
| P1 ≈ **8 × 10⁴ Hz** | 23 | **27.5** | 21 |
| P2 ≈ **2.5–4 × 10³ Hz** | 6.3 | 7.8 | 7.5 |
| P3 ≈ **6–8 × 10² Hz** | 2.2 (어깨) | 2.3 (어깨) | **8.0 (봉우리)** |
| 무표기 ≈ **4 × 10¹ Hz** | 평탄 ~0.8 | 평탄 ~0.9 | **1.5 (봉우리)** |
| 무표기 ≈ **3 × 10⁰ Hz** | ~0.6 | **2.3 (봉우리)** | **3.0 (봉우리)** |
| 무표기 ≈ **1 × 10⁰ Hz** | — | 1.6 | — |

(판독 오차 세로 ±0.5, 가로 ≈ 1/4 자릿수)

★★★ **여기서 세 가지가 동시에 나온다.**

**(가) 분해된 극대점이 라벨보다 많다.** 48 사이클 곡선에 **국소 극대가 최소 5 개**
(P1, P2, P3, ~40 Hz, ~3 Hz)인데 **라벨은 3 개**다. 본문은 `[인쇄]` "Its
corresponding DRT curves present **three major peaks**" 라고 쓴다 — "major" 라는
단서가 붙어 있으므로 **거짓은 아니지만**, 나머지 둘은 본문·Table 1·Fig. 8 어디에도
없다.

**(나) ★★★ 봉우리 개수가 사이클에 따라 늘어난다.** 4 사이클에서 **P3 는
봉우리가 아니라 P2 의 어깨**이고, 10²–10⁰ 구간은 **평탄**이다. 48 사이클에서
**P3 가 독립 극대가 되고, ~40 Hz 와 ~3 Hz 에 새 극대가 생긴다.**
`[재현]` **완전지의 분해 가능한 극대 수: 4 사이클 ≈2–3 → 48 사이클 ≈5.**
→ **10호가 재인용으로만 전한 Larfaillou 2016 의 관측(신품 3 RQ, 노화 4 RQ)이
여기서 1 차 데이터로 확인된다.** §7 에서 두 번 더 확인된다.

**(다) `[인쇄]` "P1 (~10 kHz)" 가 자기 그림과 한 자릿수 어긋난다.** (b) 의 P1 은
`[도표]` **≈8 × 10⁴ Hz** 이고 (a)·(c) 와 같은 자리다. 본문이 (b) 만 "~10 kHz"
라고 적었다 → §13 D2.

**(b) NMC/In–Li 반쪽** (`Z_real` 0–90 Ω; 화살표 50 kHz, 100 Hz)

| 특징 | 4 cycle | 15 cycle | 48 cycle |
|---|---|---|---|
| P1 ≈ 8 × 10⁴ Hz | 23 | 26.5 | **33** |
| P2 ≈ 3 × 10³ Hz | 7.5 | 9 | **11.3** |
| P3 ≈ 2.5 × 10² Hz | 2.0 | 3.0 | **14.0** |
| 무표기 ≈ 3 × 10¹ Hz | ~1.0 | ~1.3 | **3.8** |
| 무표기 ≈ 3 × 10⁰ Hz | ~0.8 | ~1.3 | **3.4** |
| 무표기 ≈ 3 × 10⁻¹ Hz | ~1.5 | ~1.7 | **2.8** |

`[재현]` **48 사이클 곡선의 국소 극대 ≈6 개, 라벨 3 개.**

**(c) graphite/In–Li 반쪽** (`Z_real` 0–90 Ω; 화살표 10 kHz)
P1 ≈ 8 × 10⁴ Hz (20 → **23**), P2 ≈ 1.5 × 10⁴ Hz (5.5 → **7.0**), 그 아래
10³–10⁰ 에 **높이 ~1 의 낮은 극대 3–4 개**. 세 사이클 곡선이 **거의 겹친다.**
→ `[인쇄]` "two major DRT peaks" 는 **라벨 기준으로 맞고**, `[인쇄]` "P3 is still
observed" 는 **라벨이 없어서 그림에서 확인할 수 없다** (P3 라 부를 후보가
10³–10² 에 있으나 표시가 없다).

★★ `[해석]` **(a)(b)(c) 의 P1 이 전부 같은 ≈8 × 10⁴ Hz 에 같은 높이(20–33)로
있다.** 완전지든 NMC 반쪽이든 graphite 반쪽이든 **동일**하다. 논문 자신이
`[인쇄]` P1 을 "**artificial effect due to … cable resistances**" 로 절반
귀속한다. → `[해석]` **이 논문 전체에서 가장 크고 가장 재현성 높은 DRT 봉우리가
셀의 것이 아닐 수 있다**, 그리고 §13(Fig. S3)이 그것을 확인해 준다.

## 3.3 ★★★ Fig. 2 캡션의 한 줄 — 이 논문의 순환

> `[인쇄]` "The DRT peaks were **computed based on the simulated Nyquist curves
> (green solid-line)** after subtracting the low-frequency data (i.e.,
> Warburg-type diffusion)."

★★★★ `[해석]` **Fig. 2 의 DRT 는 측정 데이터가 아니라 적합(모델) 곡선 위에서
계산됐다.** 그러면:
1. DRT 가 분해할 수 있는 시상수의 수는 **적합에 쓴 모델의 차수에 의해 위에서
   막힌다.** 데이터가 말하는 개수가 아니라 **모델이 허락한 개수**가 나온다.
2. DRT 를 도입한 명분이 `[인쇄]` "ECM 이 겹친 시상수를 놓친다" 였는데,
   **그 ECM 을 DRT 의 입력으로 넣었다.**
→ **10호의 `[인쇄]` "A powerful tool to **guide ECM selection** is the DRT
technique" 와 순서가 정확히 반대다.** 10호의 정답 절차(Pang 2019)는
**K–K → DRT 로 개수 결정 → 그 개수만큼 ECM** 인데, 38호는 **ECM 적합 → 그
곡선으로 DRT** 다.
⚠ 단, **이 순환이 Fig. 2 에만 해당하는지 전 그림에 해당하는지 원문에 없다** —
SI 는 "**실측에서** 꼬리를 뺀다" 고 쓴다(G7 · D1). Fig. 3·5·6 캡션에는
`simulated` 언급이 없고, Fig. 4(c)·7(c) 에는 `simulated` 곡선이 그려져 있지 않다.

---

# 4. §3.2 양극 — SE 입도 스윕 (Fig. 3)

## 4.1 본문 (`[인쇄]`)

가설: ref. [18] **Minnmann 2022** (우리 위키의 2호 Clausnitzer 가 인용한 바로 그
Minnmann 계열)을 근거로, `[인쇄]` "using **micro-sized SE** for cathode
fabrication could potentially result in an **increased amount of voids** between
solid particles".

설계: `[인쇄]` "two cells were prepared using **identical procedures and
conditions, but with different SE particle sizes in the cathodes only**. Here,
(1) the particle size of the argyrodite **in electrolyte remains unchanged** and
(2) the cells were operated at **20 MPa**."
**nano ≤1 µm** vs **micro ≤20 µm**.

결과: `[인쇄]` "**intensities of all the P1, P2, and P3 peaks increase** when
using micro-sized SE … the cathode with micron-sized SE exhibits a **relatively
rapid growth of the P3 impedance region** compared to the cathode with nano-sized
SE. This observation provides **compelling evidence that the P3 impedance is
associated with the physical contact between CAM and SE**."
보조 근거: `[인쇄]` "consistent with previous DRT analyses on conventional Li-ion
batteries, reporting the P3 impedance at similar frequency ranges (**slightly
above 10³ Hz**) as **solid-solid contact impedance of LiFePO₄/Al and
nano-Si/Cu current-collectors** [19,20]."

★★ 그리고 `[인쇄]` **"Our result unambiguously demonstrates that the major
degradation mode observed in the cathodes is the contact impedance growth
between CAM and SE."**

## 4.2 `[도표]` Fig. 3 — 실제로 열어서 확대해 본 것

축: `γ(τ) / **Ω mg⁻¹**`, 0–20; 10⁶ → 10⁰ Hz. (⚠ Fig. 2 는 `g(τ) / Ω` — **기호도
정규화도 다르다**, §13 D5.)

**(b) nano-scale SE** (cycles **4 / 26 / 59 / 81**)
P1 ≈ 1.5 × 10⁵ Hz, 높이 **4.5** (네 곡선 겹침, 변화 없음).
그 다음이 문제다 — **P2 와 P3 가 하나의 넓은 혹**이다. P2 ≈ 1 × 10⁴ (≈2.1),
P3 ≈ 2–3 × 10³ (cycle 4 에서 **1.0, 어깨**; cycle 81 에서 **1.9, 완만한 극대**).
★ `[해석]` **nano 셀에서 "P3 가 자란다" 는 서술은 분해된 봉우리가 아니라
어깨의 높이 변화를 읽은 것이다.**

**(c) micro-scale SE** (cycles **3 / 29 / 55 / 81**)
P1 ≈ 1.5 × 10⁵ Hz, 높이 **14.8** (네 곡선 겹침).

| 사이클 | 10⁵–10³ Hz 구간의 국소 극대 |
|---|---|
| **3 (검정)** | **하나** — ≈9 × 10³ Hz 에 5.8. 그 아래는 **단조 감소**(P3 자리에 극대 없음) |
| **29 (빨강)** | **둘** — P2 ≈1.8 × 10⁴ (5.2) · **P3 ≈2.8 × 10³ (6.7)** |
| **55 (파랑)** | 둘 — P2 5.3 · **P3 7.5** |
| **81 (녹색)** | 둘 — P2 5.5 · **P3 8.1** |

★★★★ `[재현]` **micro-SE 셀의 분해 가능한 중주파 봉우리 개수: 사이클 3 에 1 개
→ 사이클 29 부터 2 개.** 그리고 P1 을 합치면 **2 → 3**.
→ **10호가 Larfaillou 2016 재인용으로 전한 "노화가 RQ 를 3 → 4 로 바꾼다"
(= 모델 차수가 상태변수다)가 이 논문의 1 차 데이터에서 두 번째로 확인된다.**
⚠ **논문은 이것을 알아채지 못한다** — `[인쇄]` "Both cells showed the **growth of
P3 (10⁴–10³ Hz) peak intensities** during cycling" 라고, 없던 봉우리가 생긴 것을
**있던 봉우리가 커진 것**으로 적는다.

⚠⚠ **그리고 검정(cycle 3)의 극대가 ≈9 × 10³ Hz 인데 나머지 세 곡선의 P2 는
≈1.8 × 10⁴ Hz 다.** `[해석]` **"같은 봉우리가 자랐다" 가 아니라 "봉우리가 하나
쪼개지면서 위치가 옮겨갔다"** 고 읽는 편이 그림에 맞는다. 봉우리에 이름을 붙여
시계열로 따라가는 이 논문의 방법이 **여기서 성립하지 않는다.**

⚠⚠⚠ **세로축이 `Ω mg⁻¹` 인데 정규화에 쓴 질량이 논문 어디에도 없다** (G5).
`[인쇄]` "intensities of all the P1, P2, and P3 peaks **increase** when using
micro-sized SE" 는 **(b) 4.5 ↔ (c) 14.8 (P1)** 처럼 **3.3 배** 차이인데,
`[해석]` **두 셀의 양극 질량이 다르면 이 비교는 성립하지 않는다.**
그리고 **P1 은 논문 자신이 "SE 벌크/입계 + 케이블" 이라고 한 항이다** — 양극 내
SE 입도를 바꿨는데 **전해질 층은 안 바꿨다**(`[인쇄]` "(1) … in electrolyte
remains unchanged")면서 **P1 이 3.3 배**인 것은 설명되지 않는다. 논문은 이
불일치를 언급하지 않는다. → §13 D6.

## 4.3 `[도표]` Fig. 4(a) — nano-SE NMC 반쪽전지 100 사이클

`Specific Capacity / mAh g⁻¹` 150–190 vs `Cycle number` 0–100.
`[도표]` 데이터 점이 **≈11 개**(사이클 1, 2, 14, 25, 36, 47, 58, 69, 80, 91, 102).
`[인쇄]` "171.9 mAh/g at the 1st cycle and **171 mAh/g at the 100th** …
capacity retention value of **99.5 %**".
`[도표]` 궤적은 **단조가 아니다** — 170.5 → **174 (사이클 25)** → 171 로 내려온다.
`[해석]` 3 mAh g⁻¹ 의 비단조 변동이 있는 계열에서 "99.5 % 유지" 를 두 끝점으로
계산한 것이다. 산포 표기 0.

---

# 5. §3.2 ★★ 재가압 개입 (Fig. 4b–d) — 이 논문의 Q6 본체

## 5.1 본문 (`[인쇄]`)

> "we attempted to **rehabilitate the interfaces of over 500-times cycle-aged
> cells by re-compressing them at high pressures, such as 150 MPa and >500 MPa.
> It should be noted that the operating pressures of the cells remained constant
> at 20 MPa regardless of the re-compression procedure.** For example, the cycled
> cell was meticulously removed from the pressure jig to eliminate the operating
> pressure of 20 MPa. Subsequently, the cell was re-compressed at 150 MPa or >500
> MPa. Before performance measurements, the cells were compressed once again at
> their operating pressure of 20 MPa."

| 상태 | 방전 용량 (`[인쇄]`) | `[재현]` aged 대비 |
|---|---:|---:|
| aged (>500 사이클) | **165.0 mAh g⁻¹** | — |
| **150 MPa 재가압** | **166.9** | **+1.9 = +1.15 %** |
| **>500 MPa 재가압** | **173.1** | **+8.1 = +4.91 %** |

`[인쇄]` "After the re-compression at **150 MPa**, both the EIS and DRT analysis
exhibited **minimal changes** … However, upon re-compressing the cell at **>500
MPa**, significant changes in DRT profile were observed. **Particularly
discernible change was the reduction of P3 intensity** … This result **reinforces
the strong correlation between P3 and the mechanical contact of the CAM-SE
interface**. The DRT results observed during the re-compression **agree with
previous report by Ceder et al. [21]**, where a decrease in resistance in the
mid-frequency range indicated a **recovery of contact area** as a result of
external pressure."

★ ref. **[21] = T. Shi, Y.-Q. Zhang, Q. Tu, Y. Wang, M.C. Scott, G. Ceder,
*J. Mater. Chem. A* 8 (2020) 17399** — **우리 위키의 `assb` 4호**다.

## 5.2 ★★★ `[도표]` Fig. 4(c)(d) — 실제로 열어서 확대해 본 것

**(c) Nyquist**: `Z_real` −40 → 200 Ω. ⚠ **`Z_imag` 축에 눈금이 하나도 없다** —
좌상단에 빨간 `Same Scale` 상자와 **`20` × `20`** 이라는 스케일바만 있다. 세 곡선은
**세로로 오프셋되어 있다**(비교를 위해 띄운 것). `[해석]` **Nyquist 의 허수축을
정량적으로 읽을 수 없다.** 주파수 라벨은 1 MHz / 100 kHz / 10 kHz / 1 kHz /
100 Hz / 10 Hz / 1 Hz / 0.1 Hz.
★ **aged 곡선 아래에 점선 원호 3 개**(분홍 ≈ −5 → 12 Ω, 노랑 ≈12 → 38 Ω,
연두 ≈38 → 98 Ω)가 그려져 있다 — **P1/P2/P3 에 대응하는 ECM 분해**다.
⚠ **1 MHz 점의 `Z_real` 이 음수(≈ −5)** 다 — 배선 인덕턴스/보정 잔여.

**(d) DRT**: `γ(τ) / Ω` 0–50, x 축 **10⁷ → 10⁻³ Hz** (아래에 파란 글씨로
`10MHz … 0.001Hz` 병기). 색칠된 띠 3 개(분홍/노랑/연두)에 라벨
**160 kHz**, **8 kHz**, **1.3 kHz**.

| 봉우리 | aged | 150 MPa | **>500 MPa** | `[재현]` aged→>500 |
|---|---:|---:|---:|---:|
| **160 kHz (P1)** | ≈33 | ≈32.5 | ≈29.5 | **−11 %** |
| **8 kHz (P2)** | ≈20 | ≈19.5 | ≈18 | **−10 %** |
| **1.3 kHz (P3)** | ≈32 | ≈31 | ≈27 | **−16 %** |
| **무표기 ≈3 × 10⁻² Hz** | ≈11 | ≈9.7 | ≈8 | **−27 %** |

(세로 판독 오차 ±1)

★★★★ **네 가지가 이 표에서 나온다.**

**(가) 재가압이 P3 만 줄이지 않는다 — 스펙트럼 전체가 10–27 % 줄어든다.**
`[인쇄]` "Particularly discernible change was the **reduction of P3 intensity**"
는 **그림이 지지하지 않는다.** 상대 감소가 가장 큰 것은 **무표기 ≈0.03 Hz 봉우리
(−27 %)** 이고, **P1 도 −11 %** 줄어든다. **P1 은 논문 자신이 "SE 입계 + 케이블"
이라고 귀속한 항이다** — 양극 접촉을 회복시키는 조작이 SE 입계 저항을 11 % 줄일
이유가 논문에 없다. → §13 D3.

**(나) ★★★ 물리 귀속의 직교성이 깨진다.** Table 1 은 P2 = **화학적** 접촉(SEI/CEI),
P3 = **기계적** 접촉이라고 가른다. 재가압은 **기계적 조작**이다. 그런데 P2 도
**−10 %** 다. `[해석]` **"화학" 과 "기계" 라벨은 압력 연산자 아래에서 분리되지
않는다** — 이것이 우리 어휘의 **축퇴**이고, 논문은 이 숫자를 그려 놓고 말하지
않는다.

**(다) 가장 큰 저주파 봉우리가 측정 대역 밖에 있다.** EIS 하한이 `[인쇄]`
**0.1 Hz** 인데 이 봉우리는 `[도표]` **≈3 × 10⁻² Hz** — **0.5 자릿수 아래**다.
그리고 x 축은 **10⁻³ Hz 까지** 그려져 있다. `[해석]` **대역 끝 정규화 인공물의
전형**이고, 라벨이 없어 본문·Table 1·Fig. 8 어디에도 나타나지 않는다.

**(디) 용량 회복이 4호 대비 한 자릿수 이상 작다.**
| | 4호 (Shi 2020, In 음극 NMC532) | **38호 (Yu 2024, In–Li 음극 NMC622)** |
|---|---|---|
| 재가압 | **300 MPa** (1 회) | **150 MPa · >500 MPa** (2 점) |
| 사이클 | 50 | **>500** |
| 회복 | `[도표]` ≈2 → `[인쇄]` **80 mAh g⁻¹** (`[재현]` **+60.5 %p**) | `[인쇄]` 165.0 → **173.1** (`[재현]` **+4.91 %**) |
`[인쇄]` 38호는 이것을 "**agree with previous report by Ceder et al.**" 라고만
적고 **크기를 비교하지 않는다.** `[해석]` **두 셀의 "접촉 손실 지분" 이 한
자릿수 이상 다르다** — 즉 `θ_AM` 의 크기는 셀·공정의 함수이고, 한 편의 값을
다른 편으로 옮길 수 없다. → [[assb-pressure-reapplication-separation-test]].

⚠⚠ **그리고 Fig. 4(a) 와 4(b) 의 셀이 다르다.** (a) 는 **100 사이클, 171 mAh g⁻¹,
99.5 % 유지**이고 (b) 의 aged 는 **>500 사이클, 165.0**. `[재현]` 재가압 후
**173.1 > (a) 의 1 사이클 171.9**. `[해석]` **"회복" 값이 다른 셀의 신품 용량을
넘는다** — 두 셀을 이어 읽을 수 없다는 뜻이고, 논문은 둘을 같은 그림에 놓는다.

---

# 6. §3.2 코팅 유무 — bare NMC (Fig. 5)

`[인쇄]` "the Nyquist plots reveal a **significant growth of the second
semi-circle**, corresponding to the low-frequency domain **between 500 Hz and 1
Hz** … With increasing cycle numbers, most impedance sources become enlarged,
particularly **P5 (at around 10 Hz)** showing the most significant growth. This
frequency range **aligns well with charge-transfer resistance of the NMC CAM
reported in literature [26,27]**."
`[인쇄]` 부산물: "**NiS, CoS, MnS, Li₂S, Li₃PO₄, LiPxCly and LiCl** [25,28]".
`[인쇄]` 대조: "In stark contrast, the LiNbO₃-coated NMC cathode only shows
**minimal charge-transfer impedance** over repeated cycles, **as shown in Fig.
4(d)**."

## `[도표]` Fig. 5 (실제로 봤다)

**(a) Nyquist 2 패널** (사이클 4/15/26/37/48).
- 위 확대: `Z_real` 0–210 Ω, `Z_imag` 0 – −75 Ω. 마젠타 화살표 **40 kHz**(4th
  사이클 원호 꼭대기), **500 Hz**(두 곳).
- 아래 전체: `Z_real` **0–2500 Ω**, `Z_imag` 0 – **−1500 Ω**. 마젠타 **10 Hz**,
  **1 Hz**. 4 사이클 원호 지름 ≈**850 Ω** → 48 사이클 ≈**2300 Ω**.

★★ `[해석]` **코팅 없는 NMC 반쪽전지는 코팅 셀(Fig. 2b, `Z_real` 0–90 Ω)보다
임피던스가 ≈25 배 크다.** 같은 48 사이클에서 **88 Ω ↔ 2300 Ω**.

**(b) DRT**: `γ(τ) / Ω` **0–1000** (Fig. 2 는 0–40, Fig. 4 는 0–50), 10⁶ → 10⁻² Hz.

| 특징 | 4 cycle | **48 cycle** |
|---|---:|---:|
| ≈6 × 10⁴ Hz (P1 자리) | 130 | **215** |
| ≈1.5 × 10⁴ Hz | 30 | **38** |
| ≈4 × 10³ Hz | 22 | **28** |
| ≈1 × 10² Hz | 30 | **72** |
| **P5 ≈ 1 × 10¹ Hz** | **280** | **920** |
| ≈1.5 × 10⁰ Hz | 45 | **160** |
| ≈2 × 10⁻¹ Hz | 40 | **190** |

`[재현]` **국소 극대 ≈7 개, 라벨 1 개(P5).**
★ `[인쇄]` "most impedance sources become enlarged" 는 맞다 — **전부 자란다.**
`[재현]` 4 → 48 사이클 배율: P1 자리 **1.65×**, ≈100 Hz **2.4×**, P5 **3.3×**,
≈1.5 Hz **3.6×**, ≈0.2 Hz **4.75×**.
★★ `[해석]` **가장 빨리 자라는 것은 P5 가 아니라 그 아래 두 봉우리다.**
`[인쇄]` "particularly P5 … showing the **most significant growth**" 는 **절대
증가분(+640 Ω)으로는 맞고 배율로는 틀린다.** 논문은 어느 쪽인지 밝히지 않는다.

★★★ `[해석]` **§6 의 "대조" 는 통제된 비교가 아니다.** `[인쇄]` "In stark
contrast, the LiNbO₃-coated NMC cathode only shows minimal charge-transfer
impedance … **as shown in Fig. 4(d)**" 인데:
- Fig. 4(d) 는 **세로축 0–50 Ω**, Fig. 5(b) 는 **0–1000 Ω** — **20 배 다른 축**
- Fig. 4(d) 는 **500 사이클 + 재가압 3 상태**, Fig. 5(b) 는 **4–48 사이클 5 점**
- Fig. 4(d) 의 저주파 봉우리는 ≈**11 Ω @ 0.03 Hz** 이고 **라벨이 없다**;
  Fig. 5(b) 의 P5 는 ≈**920 Ω @ 10 Hz**
→ **두 그림은 사이클 수도, 축 눈금도, 봉우리 위치도 다르다.** "minimal" 은
**다른 셀의 다른 축에서 읽은 것**이다. → §13 D4.
⚠ 그리고 **Table 1 의 P5 증거 칸이 `[인쇄]` "Coating-free NMC half-cell (Fig. 4)"
라고 적는다 — bare NMC 는 Fig. 5 다.** → §13 D7.

---

# 7. §3.3 음극 — graphite 반쪽전지 (Fig. 6)

`[인쇄]` "the graphite anode half-cell exhibits a good cycle stability, with a
notably high **Coulombic efficiency >99.99 %**. … The corresponding DRT profiles
reveal **negligible changes in P1 – P3** (in a range of **300 kHz–200 Hz**).
However, **P4 (in a range of 100 Hz–1 Hz)** … exhibits a **gradual increase** …
The frequency range of the 2nd semicircle is associated with the
**charge-transfer impedance of graphite anodes** in Li-ion batteries [30]."
`[인쇄]` 기구: "the absence of surface coating on graphite can lead to the
**reduction of the argyrodite SE** … the electrochemical stability of this SEI
layer **has not been as well-developed** as … conventional Li-ion batteries …
**Non-uniform thickness of the electrode, cracks, and decompositions** of
electrolyte are involved in ill-constructed SEI layer [32]."

## `[도표]` Fig. 6 (실제로 봤다)

**(a)** 좌축 `Specific capacity / mAh g⁻¹` **300–400**, 우축 `Coulombic
efficiency` **90–105 %**, x = 0–120 사이클.
`[도표]` 용량: 1 사이클 ≈**332** → ≈**325** (사이클 ≈106). **데이터 점 6 개**
(≈1, 3, 28, 54, 80, 106). CE 는 **연속선**이고 첫 점이 ≈**104 %**, 이후 ≈**100 %**
에 붙어 있으며 **사이클 ≈65 에 ≈98.5 % 로 한 번 떨어진다** (그 밖에 ≈99.7 %
정도의 작은 하강 3 회).
★ `[해석]` **`[인쇄]` ">99.99 %" 는 이 그림에서 읽을 수 없다** — 세로 눈금이
5 %p 간격이라 **0.01 % 를 분해하지 못한다**. 그리고 **사이클 65 의 98.5 % 는
">99.99 %" 라는 무조건 서술과 어긋난다**. `[재현]` 용량 궤적에서 역산하면
332 → 325 (105 사이클) ⇒ 평균 **≈99.98 %/cycle** 로, **평균값으로는 정합**한다.
→ §13 D8.

**(b) Nyquist**: 6 사이클(3/29/55/81/107/133) 곡선이 **세로로 오프셋**되어 있고
**`Z_imag` 축에 눈금이 없다**(`Same Scale` **20 × 20** 상자만). `Z_real` −20 → 100 Ω.
`[도표]` 3 사이클 곡선의 `Z_real` 범위 ≈2 → 36 Ω, 133 사이클 ≈2 → 63 Ω.

**(c) DRT**: `γ(τ) / Ω` **0–15** (⚠ P1 이 **잘려서 화면 밖으로 나간다** — 높이를
읽을 수 없다), 10⁶ → 10⁻¹ Hz. **라벨 P1 · P2 · P3 · P4 — 네 개.**

| 봉우리 | 위치 | 3 cycle | **133 cycle** |
|---|---|---:|---:|
| P1 | ≈2 × 10⁵ Hz | (잘림, >15) | (잘림, >15) |
| P2 | ≈3 × 10⁴ Hz | 4.6 | **6.1** |
| P3 | ≈2 × 10³ Hz | 2.2 | **2.8** |
| **P4** | ≈1 × 10¹ Hz | ≈1.5 (평탄) | **5.5 (봉우리)** |
| 무표기 | ≈2 × 10² Hz | ≈1.7 | ≈2.0 |
| 무표기 | ≈1 × 10⁰ Hz | ≈1.3 | ≈2.6 |
| 무표기 | ≈3 × 10⁻¹ Hz | ≈1.5 | ≈3.2 |

★★★★ **세 가지가 여기서 나온다.**

**(가) 같은 종류의 셀에서 라벨된 봉우리 수가 2 (Fig. 2c) ↔ 4 (Fig. 6c) 로 다르다.**
Fig. 2(c) = graphite/In–Li, 4/15/48 사이클, `[인쇄]` "**two major DRT peaks**".
Fig. 6(c) = graphite 반쪽, 3–133 사이클, **P1–P4 네 개 라벨**.
`[해석]` **사이클 범위를 늘렸더니 봉우리가 늘었다** — 또는 **같은 데이터를 다르게
셌다.** 논문은 두 그림을 연결하지 않는다.

**(나) ★★★ P4 가 없던 자리에서 생긴다.** 3 사이클에서 10²–10⁰ 구간은
**평탄(≈1.5)** 이고, 133 사이클에서 **≈10 Hz 에 명확한 극대(5.5)** 가 선다.
→ **Larfaillou 확인 세 번째.** `[인쇄]` 논문은 "P4 … exhibits a **gradual
increase in peak intensity**" 라고 쓴다 — **없던 봉우리가 생긴 것을 있던 봉우리가
커진 것으로 적는 패턴이 Fig. 3(c) 와 동일하다.**

**(다) ★★★★ P4 의 극대가 ≈10 Hz 인데, Table 1 은 P5(양극 CT)를 `~10 Hz` 로
둔다.** Table 1 의 P4 는 `10²–10⁻¹ Hz`, P5 는 `~10 Hz`. `[도표]` Fig. 6(c) 의
P4 극대는 **≈1 × 10¹ Hz** 로 **P5 자리 한가운데**다.
→ `[해석]` **반쪽전지에서는 상대극이 In–Li 라 "양극 CT" 후보가 없으므로 이 봉우리는
음극의 것이라고 단정할 수 있다. 완전지에서는 그 단정이 불가능하다** — 같은
주파수에 두 전극의 CT 가 있기 때문이다. **그리고 Fig. 8 이 바로 그렇게 그린다**(§8).

---

# 8. §3.3 완전지 500 사이클 + 재가압 (Fig. 7) · §3.4 지도 (Fig. 8 · Table 1)

## 8.1 본문 (`[인쇄]`)

> "the cycle life of the NMC/graphite full-cell is demonstrated, exhibiting an
> **initial capacity of 192.4 mAh/g** and, after the **200th cycle, the capacity
> reaches 179.8 mAh/g. After 500 cycles**, the full-cell delivers a specific
> discharge capacity of **169.9 mAh/g**. … the aged full-cell underwent
> re-compression at **>500 MPa** … the re-compressed full-cell delivered slightly
> increased capacity (**~1.2 %**)."
>
> "The DRT peak at approximately **160 kHz**, labeled as **P1**, corresponds to
> the first semi-circle, which was **identified as the grain-boundary impedance
> of the SE**. The second and third DRT peaks correspond to the second
> semi-circle … The **low-frequency domain (10–0.1 Hz) is identified as the
> charge transfer impedance region**, forming a distinct arc in the EIS curve."
>
> "**Although the P3 peak is also present in the graphite anode, it remains
> stable over repeated cycles.** This observation indicates that the contact
> impedance of the LiNbO₃-coated NMC cathode has a more significant impact …
> The **large charge-transfer impedance at low frequency is attributed to the
> graphite anode**, as evidenced by the rapid growth … in the graphite anode
> half-cell, whereas the charge transfer impedance remained relatively stable in
> the cathode half-cell."

## 8.2 `[도표]` Fig. 7 (실제로 봤다)

**(a)** `Specific Capacity / mAh g⁻¹` **160–200** vs 사이클 **0–200**.
`[도표]` 192.4 (1) → **≈181 (25)** → ≈180 평탄 → ≈179.8 (200). **첫 25 사이클에
−11.4 mAh g⁻¹ 의 계단**이 있고 그 뒤 175 사이클 동안 ≈−1. 점 **≈17 개**.
★ **200 사이클까지만 그려진다.** `[인쇄]` "After 500 cycles … 169.9" 는
**(b) 의 막대 하나**로만 존재한다.

**(b)** aged **169.9** → Re-compressed **171.7**. `[재현]` **+1.8 = +1.06 %**
(`[인쇄]` 는 "~1.2 %" — §13 D9).

**(c)** Nyquist, `Z_real` −40 → 200 Ω. ⚠ 또 **`Z_imag` 눈금 없음**(`Same Scale`
20 × 20). aged 곡선 아래 **점선 원호 3 개**(분홍 ≈0–11, 노랑 ≈11–19, 연두 ≈19–55 Ω).
주파수 라벨 1 MHz … 0.1 Hz.

**(d) DRT**: `γ(τ) / Ω` 0–50, x 축 **10⁷ → 10⁻³ Hz**. 색칠 띠 **4 개**:
분홍 **160 kHz**, 노랑 **6 kHz**, 연두 **0.9 kHz**, ★ **하늘색 0.25 Hz**.

| 봉우리 | Aged | Re-compressed (>500 MPa) | `[재현]` Δ |
|---|---:|---:|---:|
| **160 kHz (P1)** | ≈21.5 | ≈21 | −2 % |
| **6 kHz (P2)** | ≈8.5 | ≈5.5 (극대가 거의 사라짐) | **−35 %** |
| **0.9 kHz (P3)** | ≈13.5 | (**독립 극대가 사라지고 단조 어깨가 됨**) | — |
| **0.25 Hz (P4)** | ≈**40** | ≈**30** | **−25 %** |

★★★★★ **이 표가 이 논문에서 우리에게 가장 중요한 숫자다.**

**(가) 완전지에서 가장 큰 DRT 봉우리는 P1 도 P3 도 아니라 P4(0.25 Hz)다** —
40 Ω 로 P1(21.5)의 **1.9 배**. 그런데 `[인쇄]` 결론은 `[인쇄]` "particularly
**P3**, which represents the mechanical contact" 를 지목한다.

**(나) ★★★ 재가압이 P4 를 25 % 줄인다.** Table 1 은 P4 = **"Charge transfer
impedance: graphite anode"** 다. 전하 이동 저항은 **화학·동역학** 양이고, 양극
복합체의 **기계적** 접촉을 회복시키는 조작이 이것을 25 % 줄일 이유가 논문에 없다.
`[해석]` **압력 연산자가 "기계 항" 만 지우지 않는다.**
→ 우리 어휘로: **[[assb-pressure-reapplication-separation-test]] 가 가정한
"압력이 `θ_AM` 만 되돌린다" 가 이 데이터에서 성립하지 않는다.** 이것은 4호에
붙는 **반례이자 경고**이고, 이 흡수의 두 번째 수확이다.

**(다) 재가압이 P3 의 봉우리를 없앤다 — 줄인 것이 아니라 없앤다.** 회복된 곡선은
0.9 kHz 에 극대가 없고 6 kHz 의 어깨로 이어지는 단조 감소다.
`[재현]` **재가압 후 완전지의 분해 가능한 극대 수: 4 → 3.**
→ **Larfaillou 확인 네 번째 — 그리고 이번엔 방향이 반대다.** **봉우리 개수는
노화로 늘고 개입으로 준다.** `[해석]` 즉 **모델 차수는 노화의 함수일 뿐 아니라
조작의 함수다.**

## 8.3 ★★★ `[도표]` Fig. 8 — 이 논문의 결론 지도 (실제로 봤다)

가로 주파수 축(High ω 왼쪽 → Low ω 오른쪽), 눈금 `> 10⁶ · 10⁵ · 10⁴ · 10³ ·
10² · 10¹ · 10⁰ · 10⁻¹`. 봉우리 7 개:

| 표기 | 물리 | 위치 | 색/전극 태그 |
|---|---|---|---|
| **(P1′)** | **Bulk Li-ion diffusion** | `>10⁶` 왼쪽 | ★ **회색 점선** (= 관측 안 됨) |
| (P1) | Grain-boundary Li-ion diffusion | `>10⁶` 부근 | 분홍 |
| (P2) | **Chemical contact impedance** | ≈3 × 10⁴ | ★ **Cathode(빨강) + Anode(파랑) 둘 다** |
| (P3) | **Mechanical contact impedance** | ≈3 × 10³ | ★ **Cathode + Anode 둘 다** |
| (P4) | CT impedance **from anode** | 넓게 ≈10²–10⁰ | 파랑(Anode) |
| (P5) | CT impedance **from cathode** | ≈10¹ | 빨강(Cathode) |
| W_diffusion | — | ≈10⁻¹ 오른쪽 | 회색 |

★★★★★ **이 한 장이 이 논문의 Q4 답이다 — 논문이 말하지 않는 방식으로.**

1. **P2 와 P3 는 전극을 가르지 않는다.** 논문 자신이 두 봉우리에 **Cathode 와
   Anode 를 같이 찍었다.** 즉 **"P3 가 자랐다" 는 것은 "어느 전극에서 접촉이
   나빠졌는지" 를 말해 주지 않는다.** 본문이 그것을 반쪽전지로 보완하지만
   (`[인쇄]` "predominantly attributed to cathode"), **완전지 스펙트럼 하나로는
   불가능하다** 는 것이 그림의 내용이다.
2. ★★★ **P4 와 P5 의 봉우리가 서로 겹쳐 그려져 있다.** 파란 P4(넓음)의 한가운데에
   빨간 P5(좁음)가 ≈10 Hz 에 얹혀 있다. → **양극 CT 와 음극 CT 는 주파수로
   분리되지 않는다.** 이것이 그림으로 인쇄된 **축퇴**다.
3. **(P1′) 은 점선이다** — `[해석]` **측정 대역(2 MHz) 위에 있어서 못 본 봉우리**를
   지도에 그려 넣었다. 그리고 **`P1′` 라는 표기는 본문·Table 1 어디에도 없다.**
4. **P1 의 위치가 `> 10⁶ Hz`** 인데, **본문은 1.2 × 10⁵ · 160 kHz 라 하고 Fig. 2·
   4(d)·7(d) 는 ≈8 × 10⁴ – 1.6 × 10⁵ Hz 를 보여 준다.** → §13 D2 (자릿수 어긋남).

---

# 9. ★★★ 봉우리 개수 — 이 논문이 실제로 몇 개를 분해하는가 (총괄)

9호(Huo 2025)가 남긴 질문에 대한 직접 답이다. **라벨된 개수**와 **그림에서 우리가
센 국소 극대 개수**를 갈라 적는다.

| 그림 | 셀 | 사이클 | `[인쇄]` 라벨 수 | `[도표]` 국소 극대 수 (최종 사이클) | 대역 밖 특징 |
|---|---|---|---|---|---|
| Fig. 2(a) | NMC/graphite 완전지 | 4 → 48 | **3** (P1–P3) | **2–3 → 5** | — |
| Fig. 2(b) | NMC/In–Li 반쪽 | 4 → 48 | **3** | **3 → 6** | ≈0.3 Hz 봉우리 (대역 내) |
| Fig. 2(c) | graphite/In–Li 반쪽 | 4 → 48 | **2** | ≈**5–6** (낮은 것 포함) | — |
| Fig. 3(b) | nano-SE NMC 반쪽 | 4 → 81 | **3** | **2** (P3 는 끝까지 **어깨**) | — |
| Fig. 3(c) | micro-SE NMC 반쪽 | 3 → 81 | **3** | **2 → 3** | ≈1.5 × 10² 어깨 |
| Fig. 4(d) | NMC 반쪽 (>500, 재가압) | — | **3** (띠 3 개) | **4** | ★ **≈3 × 10⁻² Hz (0.1 Hz 하한 아래)** |
| Fig. 5(b) | **bare** NMC 반쪽 | 4 → 48 | **1** (P5) | ≈**7** | ≈2 × 10⁻¹ Hz (경계) |
| Fig. 6(c) | graphite 반쪽 | 3 → 133 | **4** (P1–P4) | ≈**7** (P1 은 잘림) | ≈3 × 10⁻¹ Hz (경계) |
| Fig. 7(d) | 완전지 (500, 재가압) | — | **4** (띠 4 개) | **4 → 3** (재가압 후) | 없음 |
| Fig. 1(b) | 완전지 (= Fig. S3 하단) | — | **4** (P1·P2·P3·**P_Low**) | ≈**6** | ★ **≈2 × 10⁻² Hz** |
| Fig. S3 상 | 같은 셀, Arbin+Gamry | — | 0 | **7** | ★ **≈3 × 10⁻² Hz** |
| Fig. S3 하 | 같은 셀, Gamry 직결 | — | 0 | **6** | ★ **≈3 × 10⁻² Hz** |
| **Fig. 8 (지도)** | — | — | **7** (P1′·P1·P2·P3·P4·P5·W) | — | ★ **P1′ 은 점선(미관측)** |

★★★ **결론 네 개** (`[해석]`, 그림에서 직접 센 것):

**① 9호의 등가회로는 차수 미달이다.** 9호는 **분해 가능한 원호 1 개**에
`R_b` + (`R_SEI`∥CPE) + (`R_ct`∥CPE) + `W` = **RC 2 개 + Warburg**를 맞췄다.
**38호는 같은 화학(황화물 아지로다이트 + NMC)의 완전지에서 DRT 로 최소 4–5 개,
지도로는 6 개(+diffusion)를 주장한다.** 9호가 가정한 2 개는 **최소 2–3 배 모자란다.**
⚠ 단, **38호의 개수가 절대 기준이 아니라는 것이 같은 표에서 보인다** (아래 ②③④).

**② 개수는 사이클의 함수다 (노화로 증가).** 세 사례 — Fig. 2(a) 2–3 → 5 ·
Fig. 3(c) 2 → 3 · Fig. 6(c) P4 신생. 세 번 다 **논문은 "봉우리가 커졌다" 고 적고
"봉우리가 생겼다" 고 적지 않는다.** → **10호가 재인용으로 전한 Larfaillou 2016
(신품 3 RQ, 노화 4 RQ)의 1 차 재현이고, 그것도 세 겹이다.**

**③ 개수는 조작의 함수다 (개입으로 감소).** Fig. 7(d): 재가압 후 **4 → 3**.
`[해석]` **노화가 올리고 개입이 내리는 양이라면, 그것은 "모델 차수" 가 아니라
"상태" 다.** 고정 회로로 노화 시계열을 적합하는 관행 전체에 대한 반례다.

**④ ★★★ 개수는 계측 장비의 함수다.** `[도표]` Fig. S3 상단(Arbin+Gamry)에는
≈2 × 10⁴ Hz 에 분해된 어깨가 **하나 더** 있고 하단(Gamry 직결)에는 없다.
**같은 셀, 같은 물리, 다른 케이블 → 다른 봉우리 수.** → §13.

---

# 10. ★★★★ Fig. 1 = Fig. S3 하단 — 본문의 "예시" 가 실측이고, 그 실측이 이 논문을 반박한다

★ **발견 경위**: Fig. 1 은 `[인쇄]` 캡션이 "**Illustration** of (a) EIS and (b)
DRT techniques" 이고 본문도 `[인쇄]` "Fig. 1 shows **an example**" 라고 쓴다.
그런데 SI 의 **Fig. S3 하단(Gamry 직결)** 과 대조하면 **같은 데이터다**:

| | Fig. 1 | Fig. S3 하단 (Gamry) |
|---|---|---|
| Nyquist 시작 주파수 | `[도표]` **2 MHz** | `[도표]` **2 MHz** |
| `Z_real` 범위 | ≈20 → 400 Ω | ≈20 → 405 Ω |
| DRT 1 봉 | **105 @ ≈3.5 × 10⁵ Hz** | **105 @ ≈3.5 × 10⁵ Hz** |
| DRT 2 봉 | **43 @ ≈5 × 10⁴** | **43 @ ≈5 × 10⁴** |
| DRT 3 봉 | **66 @ ≈3 × 10³** | **66 @ ≈3 × 10³** |
| 중간 평탄 | ≈14–16, 10³–10⁰ | ≈14–16, 10³–10⁰ |
| 저주파 봉 | **≈19 @ ≈5 × 10⁻¹** | **≈19 @ ≈5 × 10⁻¹** |
| 최저 봉 | **≈77 @ ≈2 × 10⁻²** | **≈76 @ ≈3 × 10⁻²** |

→ `[해석]` **동일 데이터셋이다** (판독 오차 안에서 완전 일치).

## 10.1 `[도표]` Fig. 1 이 실제로 보여 주는 것

**(a)** `Z_imag` 0 – −200 Ω, `Z_real` 0–400 Ω. 위쪽에 **회로 박스**:
`R — [P1] — [P2] — [P3] — [P_Low] — [W_diff]` (각 박스에 R∥CPE 기호).
= **R₀ + RQ 4 개 + Warburg**.
아래 Nyquist 에는 **점선 반원이 6 개**(분홍 1 · 노랑 1 · 연두 1 · **연보라 3**)
와 회색 Warburg 쐐기가 그려져 있다.
★ `[재현]` **그려진 원호(6) > 회로의 RQ(4).**

**(b)** `γ(τ) / Ω` 0–120, x 축 10⁶ → 10⁻². 라벨 **P1 · P2 · P3 · P_Low ·
"Li-ion diffusion"**.

★★★★ **세 개의 큰 문제가 이 한 장에 있다.**

**(가) 본문이 자기 그림을 잘못 묘사한다.**
> `[인쇄]` "As shown in Fig. 1 (b), DRT method identified **more than 3
> barriers**, while the resistive responses are convoluted and represented as **a
> single flattened semi-circle in the Nyquist curve**."

`[도표]` **Fig. 1(a) 의 Nyquist 는 단일 편평 반원이 아니다.** ≈1 kHz 에
**뚜렷한 골(−Z″ 가 −65 → −45 로 내려간다)** 이 있고 ≈1 Hz 에 두 번째 최저점이
있다 — **육안으로 원호 2 개 + 꼬리**다. → §13 D10.
`[해석]` **이 논문의 동기 문장(Nyquist 로는 못 본다 → 그래서 DRT)이 근거로 드는
그림이 그 주장을 지지하지 않는다.**

**(나) `P_Low` 라는 라벨이 이 그림에만 있다.** 본문·Table 1·Fig. 8 전부 0 회.
그리고 **Fig. 8 에만 `P1′` 가 있다.** `[재현]` **이 논문은 봉우리 명명 체계를
세 벌 쓴다** — Fig. 1 (P1, P2, P3, P_Low, W_diff) · 본문/Table 1 (P1–P5) ·
Fig. 8 (P1′, P1, P2, P3, P4, P5, W_diffusion). **셋 사이의 대응표가 없다.**

**(다) ★★★ 두 번째로 큰 봉우리("Li-ion diffusion", ≈77 Ω @ ≈2 × 10⁻² Hz)가
측정 대역 밖이다.** `[인쇄]` 측정 하한은 **0.1 Hz** 이고, Fig. 1(a) 의 가장 낮은
주파수 라벨도 **0.1 Hz** 다. 이 봉우리는 그보다 **≈0.7 자릿수 아래**에 있다.
`[해석]` **DRT 역변환이 대역 끝에서 만들어 낸 특징**이고, 이 논문에서 **두 번째로
큰 "임피던스 원(源)"** 으로 그려져 있다.
⚠⚠ 게다가 SI 는 `[인쇄]` Warburg 를 **빼고** DRT 를 돌리라고 권하는데
(**§2.4**), **Fig. 1(b) 에서는 빼지 않았다** — "Li-ion diffusion" 이 그대로 있다.
**전처리가 그림마다 다르다.**

---

# 11. Table 1 전문 전사 (`[인쇄]`) — 그리고 그것과 그림의 대조

> **Table 1.** Summary of proposed impedance sources, observed frequency ranges,
> and supporting experimental evidences/references in sulfide-type solid-state
> battery full-cells.

| Label | Impedance Sources | Frequency (@ RT) | Evidence or Ref. |
|---|---|---|---|
| **P1** | Bulk and grain-boundary impedance from solid electrolyte, **and/or artificial effect due to the cable** | **> 10⁶ Hz** | Ref. (J.G. Lyagaeva et al.) · Simple SE EIS (Fig. S2) · Diff. Connection (Fig. S3) |
| **P2** | **Chemical contact impedance: SEI and CEI** | ~10⁴ Hz | Aging mechanism (Figs. 2–7) |
| **P3** | **Mechanical contact impedance of active material/SE and/or electrode/current-collector** | ~10³ Hz | Diff. Size of SE (Fig. 3) · Cycling test, and re-compressing (Figs. 5–7) |
| **P4** | Charge transfer impedance: **graphite anode** | 10²–10⁻¹ Hz | Anode half-cell cycling test (Fig. 6) |
| **P5** | Charge transfer impedance: **NMC cathode / Imperfect LiNbO₃ coating layer and CEI degradation** | ~10 Hz | **Coating-free NMC half-cell (Fig. 4)** |

★ **Table 1 과 그림·본문의 대조** (`[재현]`):

| 항목 | Table 1 | 본문 | `[도표]` 그림 | 어긋남 |
|---|---|---|---|---|
| P1 위치 | **> 10⁶ Hz** | 1.2 × 10⁵ (§3.1) · **160 kHz** (§3.3) · **~10 kHz** (§3.1 NMC 반쪽) | ≈**8 × 10⁴ – 1.6 × 10⁵ Hz** | ★★ **최대 2 자릿수** |
| P2 위치 | ~10⁴ | **~5 kHz** (§3.1) · 10⁴–10³ | **6 kHz** (7d) · **8 kHz** (4d) · ≈3 × 10³ (2a) | ≈0.5 자릿수 |
| P3 위치 | ~10³ | **~500 Hz** (§3.1 완전지) · **10³–10² Hz** (§3.1 NMC 반쪽) · **10⁴–10³ Hz** (§3.2) · **~1 kHz** (§3.3) | **0.9 kHz** (7d) · **1.3 kHz** (4d) · ≈7 × 10² (2a) · ≈2.8 × 10³ (3c) | ★★ **1.3 자릿수** |
| P5 증거 | "Fig. 4" | bare NMC 는 **Fig. 5** | Fig. 5 | ★ **오기** |
| P3 증거 | "Figs. 5–7" | 재가압은 **Fig. 4 와 Fig. 7** | — | ★ **오기** |
| P1′ | **없음** | 없음 | **Fig. 8 에 있다** | ★ |
| P_Low | **없음** | 없음 | **Fig. 1(b) 에 있다** | ★ |

★★★★ `[재현]` **P3 의 위치가 논문 안에서 500 Hz ~ 10⁴ Hz 에 걸쳐 있다 = 1.3
자릿수.** 그런데 **P2 와 P3 의 실제 간격은 0.8 자릿수**다 (Fig. 7d: 6 kHz vs
0.9 kHz → `log₁₀(6000/900) = 0.82`; Fig. 4d: 8 kHz vs 1.3 kHz → `0.79`).
→ ★★★★★ `[해석]` **이름표의 위치 불확정성(1.3 자릿수)이 이름표끼리의 간격
(0.8 자릿수)보다 크다.** 즉 **"이것이 P2 인가 P3 인가" 를 논문 자신의 기준으로
결정할 수 없다.** 그리고 P2 = 화학, P3 = 기계이므로 **화학 열화와 기계 열화의
분리가 바로 이 자리에서 무너진다.** 이것이 우리가 찾던 형태의 **축퇴**이고,
이 논문은 그것을 재지 않는다 (`uniqu*` 0 회).

---

# 12. SI Fig. S2 — P1 을 입계에 귀속시킨 근거는 데이터가 없는 구간의 외삽이다

`[인쇄]` SI: "100 mg of argyrodite-type SE powder, Li₆PS₅X (where X = Br and Cl)
… compressed **over 500 MPa** … measured with potentiostatic EIS mode in the
frequency range **from 1 MHz to 1 kHz at −20 °C**."
`[인쇄]` "The obtained EIS curve was **fitted** using the impedance analysis
software, **ZView4**. In this work, **it was assumed there exist only two
impedance: (i) bulk, and (ii) grain-boundary impedance**. In our assumption,
grain-boundary impedance appears at a relatively lower frequency, and
bulk-impedance at a higher frequency. Therefore, **the distance of the
semi-circle … is assumed** the resistance attributed to … grain-boundary, and
the area ahead is **considered** as … bulk-type Li-ion migration."

## `[도표]` Fig. S2 (실제로 봤다)

축: `−Im(Z) (Ω)` 0–100, `Re(Z) (Ω)` 0–250. 좌상단에 die-cell 인셋.
**두 개의 치수선**: `105 Ω` (0 → ≈105) 과 `90 Ω` (≈105 → ≈193).
- **실험 점(초록 사각형)은 `Re(Z) ≈ 172` 에서 시작한다.** 172 → 207 Ω 구간에
  ≈20 점. 최저점 ≈(193, 4).
- **점선 "Fit"(파랑)은 ≈105 → ≈193 Ω 에 걸친 반원**을 그린다. 꼭대기 ≈(148, 35).

★★★★ `[해석]` **이 논문이 P1 을 "입계" 라고 부르는 유일한 1 차 근거가 이 그림인데,
입계 반원으로 지정된 90 Ω 구간 중 실측 점이 있는 곳은 오른쪽 끝 ≈20 %(172–193 Ω)
뿐이다. 반원의 꼭대기도, 왼쪽 절반도, 그리고 "bulk" 라 부르는 105 Ω 도 데이터가
전혀 없는 구간이다.**
- 측정 대역이 `[인쇄]` **1 MHz – 1 kHz = 3 자릿수**뿐이고, 반원의 꼭대기가 그 안에
  들어왔다는 증거가 그림에 없다.
- `[인쇄]` **"it was assumed there exist only two impedance"** — 개수를 **가정**하고
  그 가정대로 적합했다.
→ **이것이 9호가 한 일(원호 1 개에 RC 2 개)과 같은 일이고, 여기서는 원호가 0 개다.**
그리고 **그 결과가 본문의 P1 귀속과 Table 1 의 `>10⁶ Hz` 를 떠받친다.**

⚠ 그리고 **−20 °C 에서 >100 kHz 에 보였다는 것을 상온의 `>10⁶ Hz` 로 옮기는 데
활성화에너지도 Arrhenius 외삽도 없다** — `[인쇄]` "The semi-circle associated with
grain-boundary impedance appeared at a high frequency of **>100 kHz at −20 °C**,
and it can be **identified as P1**."

---

# 13. ★★★★★ SI Fig. S3 — 이 논문이 인쇄해 놓고 하지 않은 뺄셈

`[인쇄]` SI 캡션: "Figure S3. Impedance spectroscopy examined using **(top)
battery cycler-connected potentiostat**, and **(bottom) potentiostat (direct
connection)**."
`[인쇄]` 본문의 용도: "**different wire connections can create changes of
resistance and inductance, which may result in P1 shifting to the high-frequency
range** (shown in Fig. S3)."

## `[도표]` Fig. S3 (실제로 열어 확대해 봤다)

**Nyquist(왼쪽 두 패널)**: 위 `Cycler + Potentiostat` — `Z_real` ≈ −15 → 390 Ω,
최고 주파수 라벨 **1 MHz**. 아래 `Potentiostat (Direct connection)` — `Z_real`
≈ +20 → 405 Ω, 최고 주파수 라벨 **2 MHz**. **두 Nyquist 는 형태가 거의 같다**
(같은 위치에 같은 크기의 원호 2 개 + 꼬리; 1 kHz 와 1 Hz 라벨 위치가 일치).

**DRT(오른쪽 두 패널)**: `Gamma(tau) / Ohm` **0–140**, x 축 10⁶ → 10⁻³ Hz
(위에 녹색으로 `1 MHz … 0.001 Hz` 병기).

| 봉우리 위치 | **Arbin-Gamry** (위) | **Gamry 직결** (아래) | `[재현]` Δ |
|---|---:|---:|---:|
| ≈3.5 × 10⁵ Hz | **117** | **105** | **−10 %** |
| ≈5 × 10⁴ Hz | **44** | **43** | ≈0 % |
| ★ ≈2 × 10⁴ Hz | **39 (분해된 어깨)** | **(없음 — 단조)** | **특징 1 개 차이** |
| ≈3 × 10³ Hz | **78** | **66** | **−15 %** |
| ≈2 × 10² Hz | ≈16 | ≈15 | −6 % |
| ≈5 × 10⁻¹ Hz | ≈16 | ≈19 | **+19 %** |
| ★ ≈3 × 10⁻² Hz | **45** | **76** | ★★ **+69 %** |

(세로 판독 오차 ±3, 가로 ≈1/4 자릿수)

★★★★★ **이 표가 이 흡수의 최대 수확이다.** 이유:

**① 같은 셀이다(로 보인다).** Nyquist 두 개가 형태·크기·주파수 라벨 위치까지
겹친다. `[해석]` 셀은 그대로이고 **바뀐 것은 계측 경로뿐**이다.
⚠ 단 **SI 가 "같은 셀" 이라고 명시하지 않는다** — 이것도 공백이다(G4 계열).
⚠⚠ 그리고 **최고 주파수가 1 MHz vs 2 MHz 로 다르다** — 대역이 완전히 같지 않다.
그러나 **저주파 쪽 대역은 같고, +69 % 가 난 봉우리는 저주파 쪽이다.**

**② 물리가 그대로인데 DRT 봉우리가 −15 % ~ +69 % 움직인다.**
→ **10호가 `[인쇄]` "DRT analysis is also **very sensitive to experimental
errors**" 라고 적은 것의 1 차 실증이다.** 그리고 **Nyquist 는 거의 안 움직였는데
DRT 가 움직였다** — 즉 **차이를 만든 것은 데이터가 아니라 역변환이다.**

**③ ★★★★ 이 인공물의 크기가 본문의 주요 효과와 같거나 크다.**

| 본문에서 해석된 변화 | 크기 | Fig. S3 의 배선 인공물 |
|---|---:|---|
| Fig. 4(d) 재가압(>500 MPa)이 **P3** 를 줄임 | **−16 %** | **같은 P3 자리(≈3 kHz)가 배선만으로 −15 %** |
| Fig. 4(d) 재가압이 P1(160 kHz)을 줄임 | −11 % | 같은 자리가 배선만으로 −10 % |
| Fig. 4(d) 재가압이 P2(8 kHz)를 줄임 | −10 % | ≈2 × 10⁴ 자리는 **봉우리 유무가 바뀐다** |
| Fig. 7(d) 재가압이 **P4**(0.25 Hz)를 줄임 | −25 % | **저주파 봉우리가 배선만으로 +69 %** |
| Fig. 3(b) nano 셀 P3 가 81 사이클에 자람 | `[도표]` 1.0 → 1.9 (+90 %) | — |

★★★★★ `[해석]` **이 논문은 자기 방법의 재현성 하한을 SI 에 인쇄해 놓고,
본문에서 그보다 작거나 비슷한 변화를 물리적 열화·회복으로 해석한다.**
**뺄셈을 하지 않는다.** 그리고 `uncertaint*`·`error bar`·`uniqu*`·`regulariz*`
전수 0 회이므로 **이 비교를 할 어휘 자체가 논문에 없다.**

★★ `[해석]` **우리 어휘로 번역하면**: Fig. S3 은 **nuisance 변수(계측 경로)를
하나 흔들었을 때 추정량이 움직이는 폭**이다 — 즉
[[near-optimal-set-width-measurement]] 가 재는 것의 **아주 거친 1 점 판**이다.
**논문은 그것을 재고도 "폭" 이라고 부르지 않고, 본문의 점추정 옆에 놓지 않는다.**
7호(Spencer-Jolly)의 `LLI` 뺄셈과 **같은 형태의 미완**이다.

⚠ **공정하게 적는다**: (a) 배선이 바뀌면 인덕턴스·접촉저항이 실제로 바뀌므로
**변화의 일부는 진짜 물리**다. (b) 두 측정의 최고 주파수가 다르다. (c) 같은 셀이라는
명시가 없다. **그러므로 "인공물 69 %" 는 상한이지 확정값이 아니다.**
그러나 **상한조차 본문 효과보다 크다**는 것이 요점이고, 그 판단을 논문이
독자에게 넘긴 것이 아니라 **아예 제기하지 않았다**는 것이 문제다.

---

# 14. Q1~Q8 (닻 `questions/assb-contact-loss-vs-lampe.md` 의 수집 지침)

| # | 38호의 답 |
|---|---|
| **Q1 접촉 손실 정량** | **부분 — 단위가 Ω 다.** `contact loss`·`percolat*`·`tortuos*`·`θ` **0 회**. 대리량 = **P3 DRT 봉우리 높이** (`Ω` 또는 `Ω mg⁻¹`). ★ **이 계보 최초로 (i) 주파수로 국소화되고 (ii) 시계열이 있고 (iii) 조작으로 되돌려지는** 접촉 손실 대리량이다. ⚠ 세 가지가 막는다 — ① **무차원 분율이 아니다**(용량으로 가는 사상 0) ② **전극을 가르지 않는다**(Fig. 8 이 P3 에 Cathode+Anode 둘 다 찍는다) ③ **Table 1 이 P3 를 `active material/SE` **and/or** `electrode/current-collector`** 로 둔다 — `[인쇄]` 로 **복합양극 내부 접촉과 집전체 접촉을 안 가른다** |
| **Q2 독립 관측** | **★★ 있다 — 네 개의 조작, 그러나 전부 임피던스 안에서다.** ① **반쪽전지 분해**(완전지 ↔ NMC/In–Li ↔ graphite/In–Li — **계보 최초**) ② **SE 입도 스윕**(nano ≤1 µm vs micro ≤20 µm) ③ **코팅 유무**(LiNbO₃ vs bare) ④ **재가압**(150 / >500 MPa). ⚠⚠ **형태학·화학 관측이 0 이다** — SEM·TEM·FIB 토모·XRD·XPS·ToF-SIMS **전수 0**. **접촉 손실을 임피던스 밖에서 확인한 관측 0 건.** 4호(Shi 2020)가 FIB-SEM 으로 void 를 실측한 것과 정반대 |
| **Q3 라벨 층위** | ★★ **새 층위: `inverted-nonunique`.** 라벨이 **ill-posed 역변환의 봉우리 높이**이고, 그 역변환의 정규화 설정이 **보고되지 않았다**(G1). 그 위에 **Fig. 2 는 적합 곡선 위에서 DRT 를 돌렸다**(§3.3) → **ECM 을 입력으로 받은 DRT**. 오차막대 **0** · 셀 수 **0** · 반복 **0**. ★ `[인쇄]` "**The authors do not have permission to share data.**" ⚠ **파라미터 표가 없다** — 9호는 6 개를 "not disclosed" 로 **찍었는데** 38호는 구멍을 셀 기준조차 없다 |
| **Q4 유일성** | **0 (11/11 편).** 18 개 검색어 전수 0 회. ★★★ **그러나 성질이 다섯 번째로 바뀐다** — §15 |
| **Q5 Li-In** | **부분 — 값은 들어왔고 검토는 0.** `[인쇄]` 반쪽전지 전압창 **−0.595 – 0.9 V** (음극) · **2.1–3.7 V** (양극). `[재현]` 완전지 창 **2.7–4.2 V** 와 맞추면 **오프셋 ≈0.60–0.62 V vs Li/Li⁺** 가 함의된다 — **계보 최초로 오프셋이 소수 셋째 자리까지 암시된 편**이다. ⚠ **명시·인용·안정성 논의 전부 0**(`indium` 1 회). ⚠⚠ 그리고 10호의 경고 — `[인쇄]` "방전 중 In 음극 계면 저항이 리튬화도로 크게 증가" — 를 38호는 **검토하지 않는다**: In–Li 반쪽전지 DRT 의 P1·P2 변화에 **SoC 분과 노화 분이 섞여 있을 수 있다**(모든 EIS 가 `[인쇄]` 50 % SOC 이므로 **완전지 기준 50 %** 이고, **반쪽전지의 In–Li 리튬화도는 통제되지 않았다**) |
| **Q6 압력** | **★★★ 이 계보에서 가장 넓다 — 그리고 처음으로 "압력 → DRT 봉우리" 사상이다.** 제작 `[인쇄]` **>500 MPa** · 운전 `[인쇄]` **20 MPa** · 재가압 **150 / >500 MPa**. `MPa` **48 회**. ★ **압력 → 용량 3 점**(165.0 / 166.9 / 173.1, 반쪽) + **2 점**(169.9 / 171.7, 완전지) — **`assb` 10/10 편이 못 준 "압력 → 용량 곡선" 을 처음으로 준다.** ★★ 그리고 **압력 → 봉우리별 Δ** (§5.2 · §8.2). ⚠ **효과가 4호의 1/12** (+4.9 % vs +60.5 %p). ⚠⚠ **계측 수단 0**(볼트·너트, G6). ⚠⚠⚠ ★★ **선택성이 없다** — 재가압이 P1(−11 %) · P2(−10 %) · P3(−16 %) · P4(−25 %) 를 **전부** 줄인다 |
| **Q7 dead Li** | **해당 없음** (graphite 음극). `dead li`·`isolated`·`plating` **0 회**. ★ 인접 하나 — `[인쇄]` graphite 반쪽 CE ">99.99 %" 인데 `[도표]` Fig. 6(a) 에 **≈98.5 % 로 떨어지는 사이클이 하나 있다**(D8) |
| **Q8 화학·OCP** | **★★★ 계보 최초의 graphite 음극 완전지.** LiNbO₃-코팅 **NMC622** + **graphite** + Li₆PS₅X, 완전지 **2.7–4.2 V**, C/3, **192.4 → 179.8 (200 cy) → 169.9 (500 cy) mAh g⁻¹**. `OCV`·`open circuit`·`GITT` **0 회**, **V–Q 곡선 0 장** (10호와 같다). ⚠ **어느 셀이 Cl 이고 어느 셀이 Br 인지 끝까지 안 밝힌다** |

★★★★ **Q8 이 이 카드의 전제를 정면으로 깬다.**
이 카드는 `[해석]` "전고체 음극(Li-In · Li · 무음극)은 **OCP 가 평탄** → 완전지
OCV 가 사실상 양극 곡선 하나 → **5 → 3 파라미터 붕괴**" 를 출발점으로 삼는다.
**38호의 음극은 graphite 다 — 액체셀과 같은 재료이고, 스테이지 평탄역이 여럿인
구조 있는 OCP 다.** 그러면:
- **`LAM_NE` 축이 되살아난다** (9호의 Li-Si 에 이어 **두 번째 반례**이고, 이쪽은
  **상용 흑연**이라 더 직접적이다).
- **액체셀 갈래의 최악 축퇴 `LAM_NE ↔ γ_Si` 는 Si 가 없으므로 안 온다.** 그러나
  **`LLI ↔ LAM_NE` 의 흑연 쪽 축퇴는 그대로 온다.**
- `[해석]` **즉 "ASSB 라서 문제가 3 개로 줄어든다" 는 것은 음극 재료의 함수이지
  ASSB 의 성질이 아니다.** 닻 카드의 §"지금까지 아는 것" 표(5 → 3 붕괴)는
  **Li-In/Li 금속/무음극 셀에만** 유효하다고 단서를 달아야 한다.

---

# 15. ★★★ Q4 의 다섯 번째 변신 — "쟀다" 가 아니라 "잴 재료를 인쇄하고 뺄셈을 안 했다"

**계보의 형태 변화** (닻 카드에 기록된 것 + 이 편):
1. **1–7 호** — 안 쟀다 (`identifiab*` 0 회)
2. **8 호 (Li 2026)** — **이름이 로드맵의 실패 모드 목록에** 올랐다
   (`Unidentifiable pulse response`)
3. **9 호 (Huo 2025)** — **지문이 자기 표 안에** 있고 다르게 불린다
   (`R_SEI` +37 % / −80 %, `[인쇄]` "적합 오차" 탓)
4. **10 호 (Vadhva 2021)** — **방법 자체의 비유일성이 분야의 공식 문장**이 됐다
   (`[인쇄]` "no solution to an EIS spectrum is unique")
5. ★★★ **11 호 = 38 호 (Yu 2024)** — **축퇴의 크기를 실제로 잴 재료를 SI 에
   인쇄해 놓고, 본문의 효과와 나란히 놓지 않는다.**

**정확히 무엇이 "재료" 인가** (전부 `[도표]`, §9 · §11 · §13):
- **폭 재료 1 — nuisance 하나에 대한 추정량 변동**: 같은 셀, 배선만 바꿔
  DRT 봉우리가 **−15 % ~ +69 %** (Fig. S3).
- **폭 재료 2 — 이름표의 위치 불확정성이 이름표 간격보다 크다**: P3 의 보고 위치가
  **500 Hz – 10 kHz (1.3 자릿수)** 인데 P2–P3 간격은 **0.8 자릿수**.
- **차수 불확정성**: 분해되는 극대 수가 **사이클(↑)·조작(↓)·계측 경로**의 함수
  (§9 의 ②③④).
- **선택성 부재**: 기계적 조작(재가압)이 "화학" 봉우리(P2) 와 "전하 이동"
  봉우리(P4) 를 **함께** 줄인다.

**그리고 무엇이 "뺄셈 없음" 인가**:
- `uncertaint*`·`error bar`·`uniqu*`·`regulariz*`·`ill-posed`·`identifiab*` 전수 **0 회**
- Fig. S3 의 변동폭을 본문 어디에서도 **비교 대상으로 쓰지 않는다**
- `[인쇄]` **"Our result unambiguously demonstrates…"** — 이 논문에서 유일하게
  나오는 확신 부사가 **`unambiguously`** 이고, `uniqu*` 는 0 회다.
- `[인쇄]` Highlights **"EIS – DRT combination thoroughly elucidate the
  degradation mechanisms"**

★★ `[해석]` **7호(Spencer-Jolly)의 Q7 과 정확히 같은 형태다** — "수치가 계산
가능한데 논문이 그 뺄셈을 하지 않는다". 다만 **축이 Q7 이 아니라 Q4 이고, 재료가
본문이 아니라 SI 에 있으며, 그 재료가 논문 자신의 결론을 침식한다**는 점이
다르다. **Q4 는 여전히 0/11 이다 — 잰 편은 없다.**

---

# 16. 어긋남 원장 (`[도표]`·`[재현]` 로 확인한 것만)

| # | 어긋남 | 좌표 | 확인 방법 |
|---|---|---|---|
| **D1** | ★★ **DRT 전처리가 두 가지로 서술된다.** Fig. 2 캡션 `[인쇄]` "computed based on the **simulated Nyquist curves**" ↔ SI `[인쇄]` "the fitted model is **subtracted from the measurement data**" / Fig. S5 "subtraction … from the **original** Nyquist plot" | Fig. 2 캡션 · SI §"DRT calculation" · Fig. S5 | 두 텍스트 대조 + Fig. S5 열람 |
| **D2** | ★★★ **P1 의 주파수가 최대 2 자릿수 어긋난다.** Table 1 · Fig. 8 = **`>10⁶ Hz`** ↔ 본문 §3.1 = **1.2 × 10⁵** · §3.3 = **160 kHz** · §3.1(NMC 반쪽) = **~10 kHz** ↔ `[도표]` Fig. 2·4(d)·7(d) = **8 × 10⁴ – 1.6 × 10⁵ Hz** | Table 1 · Fig. 8 · Fig. 2 · 4(d) · 7(d) | 그림 확대 판독 |
| **D3** | ★★★ **"P3 만 줄었다" 가 그림에 없다.** `[인쇄]` "Particularly discernible change was the reduction of **P3** intensity" ↔ `[도표]` Fig. 4(d) 는 P1 −11 % · P2 −10 % · P3 −16 % · 무표기 0.03 Hz **−27 %** — **전부 줄고 최대는 무표기 봉우리** | §3.2 ↔ Fig. 4(d) | 확대 판독 |
| **D4** | ★★ **통제되지 않은 대조를 "stark contrast" 로 부른다.** `[인쇄]` bare NMC(Fig. 5b, 축 0–1000 Ω, 4–48 cy) ↔ coated NMC(**Fig. 4d**, 축 0–50 Ω, >500 cy + 재가압) | §3.2 마지막 문단 | 두 그림 축 대조 |
| **D5** | **DRT 세로축 기호·정규화가 그림마다 다르다.** Fig. 2 = `g(τ) / Ω` · Fig. 3 = `γ(τ) / Ω **mg⁻¹**` · Fig. 4·5·6·7 = `γ(τ) / Ω` · Fig. S3 = `Gamma(tau) / Ohm`. **정규화 질량은 어디에도 없다** | Fig. 2·3·4·5·6·7·S3 | 축 라벨 대조 |
| **D6** | ★★ **입도만 바꿨다는 두 셀에서 P1 이 3.3 배 다르다.** `[인쇄]` "the particle size of the argyrodite **in electrolyte remains unchanged**" ↔ `[도표]` P1 = **4.5**(nano) vs **14.8**(micro) `Ω mg⁻¹`. P1 은 논문 자신이 "SE 벌크/입계 + 케이블" 로 귀속한 항이다. 논문은 언급하지 않는다 (정규화 질량이 다르면 설명되나 질량이 없다 — G5) | Fig. 3(b)(c) | 확대 판독 |
| **D7** | **Table 1 의 증거 칸 오기 2 건.** P5 증거 `[인쇄]` "Coating-free NMC half-cell (**Fig. 4**)" → 실제 **Fig. 5**. P3 증거 "Cycling test, and re-compressing (**Figs. 5–7**)" → 재가압은 **Fig. 4 와 7** | Table 1 | 본문 대조 |
| **D8** | **CE 서술과 그림.** `[인쇄]` "notably high Coulombic efficiency **>99.99 %**" ↔ `[도표]` Fig. 6(a) 의 CE 축 눈금은 **5 %p 간격**이라 0.01 % 를 분해하지 못하고, **사이클 ≈65 에 ≈98.5 % 로 떨어지는 점**이 있다. `[재현]` 용량 궤적 역산 평균은 **≈99.98 %/cycle** 로 정합 | §3.3 ↔ Fig. 6(a) | 그림 판독 + 역산 |
| **D9** | **재가압 회복률.** `[인쇄]` "slightly increased capacity (**~1.2 %**)" ↔ `[인쇄]` 169.9 → 171.7 ⇒ `[재현]` **+1.06 %** | §3.3 ↔ Fig. 7(b) | 산술 |
| **D10** | ★★★ **본문이 자기 Fig. 1 을 잘못 묘사한다.** `[인쇄]` "the resistive responses are convoluted and represented as **a single flattened semi-circle** in the Nyquist curve" ↔ `[도표]` Fig. 1(a) 는 **뚜렷한 원호 2 개 + 꼬리**(≈1 kHz 에 골) | §1 ↔ Fig. 1(a) | 그림 열람 |
| **D11** | ★★ **Fig. 1 은 "Illustration" 이 아니라 Fig. S3 하단의 실측이다.** 7 개 특징이 판독 오차 안에서 일치 | Fig. 1 ↔ Fig. S3 | 봉우리 위치·높이 대조 (§10) |
| **D12** | ★★ **봉우리 명명 체계가 세 벌이고 대응표가 없다.** Fig. 1 = `P1·P2·P3·P_Low·W_diff` · 본문/Table 1 = `P1–P5` · Fig. 8 = `P1′·P1·P2·P3·P4·P5·W_diffusion`. `P_Low` 와 `P1′` 는 각각 한 그림에만 있다 | Fig. 1 · Table 1 · Fig. 8 | 전수 대조 |
| **D13** | ★★ **DRT 가 측정 대역 밖에 큰 봉우리를 놓는다.** 측정 하한 `[인쇄]` **0.1 Hz** ↔ `[도표]` Fig. 1(b) ≈**2 × 10⁻² Hz** (77 Ω, 2 번째로 큰 봉우리) · Fig. 4(d) ≈**3 × 10⁻² Hz** (11 Ω) · Fig. S3 ≈**3 × 10⁻² Hz** (45 / 76 Ω). x 축은 **10⁻³ Hz 까지** 그려져 있다 | Fig. 1(b) · 4(d) · S3 | 확대 판독 |
| **D14** | **Fig. 4(a) 와 4(b) 는 다른 셀인데 한 그림에 있다.** (a) 100 cy, 171.9 → 171 ↔ (b) aged(>500 cy) 165.0, 재가압 후 **173.1 > (a) 의 1 사이클 171.9** | Fig. 4 | 산술 |
| **D15** | **`Z_imag` 축에 눈금이 없는 Nyquist 가 3 장이다** (Fig. 4c · 6b · 7c) — `Same Scale` **20 × 20** 스케일바만 있고 곡선이 세로 오프셋되어 있다 | Fig. 4(c) · 6(b) · 7(c) | 그림 열람 |
| **D16** | ★ **`P_Low`/`Li-ion diffusion` 이 Fig. 1(b) 에 살아 있다** — SI 가 `[인쇄]` Warburg 를 **빼라**고 한 것과 어긋난다. Fig. 2 는 뺐다고 캡션에 적는다 | Fig. 1(b) ↔ SI §"DRT calculation" | 대조 |
| **D17** | **`[인쇄]` Fig. 8 에 `W_diffusion` 봉우리가 그려져 있는데 Table 1 에 W 항목이 없다** (Table 1 은 P1–P5 다섯 줄) | Fig. 8 ↔ Table 1 | 대조 |
| **D18** | **`[인쇄]` "we have used the LiNbO₃ coated cathodes in the provided data (e.g., **Figs. 1–3**)"** — Fig. 1 은 데이터가 아니라 "Illustration" 이라고 캡션에 적혀 있다 (D11 과 맞물린다) | §3.2 ↔ Fig. 1 캡션 | 대조 |

★ **18 건.** 10호(6 건)·7호(13 건)보다 많고 8호(10 건)보다 많다. `[해석]`
**그중 D1·D2·D3·D10·D11·D13 은 이 논문의 주장을 직접 약화시킨다** — 나머지는
편집 수준이다.

---

# 17. 9호(Huo 2025) §5.1 에 대한 답 — 정리

**9호가 남긴 것**: 분해 가능한 원호 **1 개**에 `R_b` + (`R_SEI`∥CPE) +
(`R_ct`∥CPE) + `W` = `[재현]` **자유 파라미터 9 개**를 맞췄고, `R_SEI` 분해가
동일 공정 두 셀에서 **+37.1 % / −79.7 %** 로 **부호까지** 어긋났으며, 논문은
그것을 `[인쇄]` "장비 정확도 · **적합 과정이 넣은 오차** · 열평형" 탓으로 넘겼다.

**38호가 주는 답 세 개**:

**(A) DRT 는 같은 화학의 완전지에서 2 개보다 훨씬 많이 분해한다 — 9호의 회로는
차수 미달이다.**
- `[인쇄]` Table 1 = **P1–P5 다섯 개** + Fig. 8 = **P1′ 포함 여섯 개 + W**
- `[도표]` 완전지 실측 국소 극대 = **48 사이클에 5 개**, 500 사이클 재가압 전 **4 개**
- 9호의 RC 2 개는 **최소 2–3 배 모자란다**. 그리고 9호가 `R_SEI` 라 부른 것은
  38호의 지도에서 **P2(화학 접촉, SEI+CEI)** 에 대응하는데, **38호는 그 P2 에도
  `Cathode` 와 `Anode` 를 둘 다 찍는다** — 즉 **9호의 `R_SEI` 는 전극 귀속조차
  되지 않는 양이다.**

**(B) ★★ 그러나 38호의 개수도 절대 기준이 아니다 — 그리고 그것이 더 중요한
답이다.** §9 에서 센 대로 개수는 **사이클(↑) · 조작(↓) · 계측 경로**의 함수다.
`[해석]` **"올바른 RC 개수" 라는 것이 데이터에서 유일하게 정해지지 않는다.**
→ 9호의 문제는 "2 개 대신 5 개를 썼어야 한다" 가 아니라
**"개수를 고르는 규칙이 문헌에 없다"** 이고, 그 규칙의 후보(**AIC**)를 10호가
`[인쇄]` "only recently applied to **simulated** data … validation against
experiment in the context of ASBs is **desirable**" 로 열어 두었으며,
**38호도 쓰지 않았다**(`AIC`·`Akaike`·`information criterion` 전수 0 회).

**(C) 9호의 `R_SEI` 부호 반전과 같은 크기의 인공물이 38호 SI 에 있다.**
9호: 동일 공정 두 셀에서 `R_SEI` 분해 **+37 % / −80 %**.
38호: **같은 셀**, 배선만 바꿔 DRT 봉우리 **−15 % ~ +69 %** (Fig. S3).
`[해석]` **9호가 "적합 오차" 라 부른 것의 크기가, 38호에서는 "셀을 건드리지도
않았을 때의 변동" 으로 나타난다.** → **9호의 부호 반전은 셀 간 차이가 아니라
역문제의 폭일 수 있다** 는 가설에 38호가 **독립적인 크기 근거**를 준다.
⚠ 두 양은 **같은 양이 아니다**(9호는 ECM 파라미터, 38호는 DRT 봉우리 높이;
9호는 두 셀, 38호는 한 셀 두 배선). **크기의 자릿수가 같다는 것까지만 말한다.**

---

# 18. 10호(Vadhva 2021) 처방표에 대한 채점

10호가 준 처방 6 개에 38호를 대조한다.

| 10호의 처방 (`[인쇄]`) | 38호 | 근거 |
|---|---|---|
| **K–K / Lin-KK 사전 검증** (`[인쇄]` "essential" for DRT) | ❌ **0** | `Kramers`·`Kronig` 0 회 |
| **DRT 로 시상수 개수를 먼저 정하고 그 개수만큼 ECM** | ⚠ **역순** | Fig. 2 는 `[인쇄]` **적합 곡선 위에서** DRT 를 돌린다 (§3.3) |
| **상보 대칭셀 쌍으로 기여 분리** | ⚠ **대칭셀 아님, 반쪽전지 쌍** | NMC/In–Li + graphite/In–Li. **계보 최초의 전극별 분해**이지만 대칭셀은 아니다 |
| **저온으로 시상수 벌리기** (ref. 82 Bron) | ⚠ **1 회, 다른 목적** | `[인쇄]` Fig. S2 의 **−20 °C** 단순 SE 셀. **입계를 동정하려고** 썼고, `[도표]` **데이터가 없는 구간의 외삽**이다 (§12). 실온 적합의 **구속으로 되가져오지 않는다** |
| **가압으로 큰 시상수 제거 / 분해능 연산자** | ✅ **있다, 그리고 확장한다** | 150 / >500 MPa 재가압 → 봉우리별 Δ (§5.2 · §8.2). ⚠ **선택적이지 않다** |
| **4 단자** | ❌ **0** | `four-point`·`4-point` 0 회 |
| **AIC 로 회로 순위** | ❌ **0** | `AIC`·`Akaike` 0 회 |
| **λ 선택 규칙** (10호의 공백 G4) | ❌ **0 — 공백이 더 커졌다** | `regulariz*`·`λ`·`L-curve`·`GCV` 0 회. SI 는 DRT 를 **보통의 적합**으로 소개한다 (§2.3) |
| **DRT 불확실성 (Bayesian DRT, Huang 2020)** | ❌ **0** | `Bayes*`·`posterior`·`credible` 0 회. **오차막대 0** |
| **일반화 DRT (Danzer 2019)** | ⚠ ★ **인용은 하고 안 쓴다** | ref. **[33] = M.A. Danzer, "Generalized distribution of relaxation times analysis…", *Batteries* 5 (2019) 53** 를 **케이블 인공물 문장에** 매단다 — 방법으로 쓰지 않는다 |
| **2D DRT (Mertens 2017)** | ⚠ **인용은 하고 안 쓴다** | ref. [10] Mertens 는 **LATP 초이온 전도도** 논문으로 인용된다 |
| **삼중 측정 / 산포 보고** (10호의 Ohno 권고) | ❌ **0** | 셀 수·반복·오차막대 전부 0 |
| **<50 mV 소진폭** | ✅ **지킨다** | `[인쇄]` **10 mV** |
| **다변수(온도·압력·SoC) 시험** (10호 제언 2) | ⚠ **압력만** | SoC 는 `[인쇄]` **50 % 고정**, 온도는 **RT 고정**(−20 °C 는 SE 단독 셀만) |

★ `[재현]` **14 항목 중 ✅ 2 · ⚠ 5 · ❌ 7.**
★★★ `[해석]` **10호의 λ 공백(G4)은 메워지지 않았다 — 오히려 이 논문이 그 공백이
얼마나 깊은지 보여 준다.** 10호는 **문제를 알고 원 논문으로 넘겼고**, 38호는
**문제가 있다는 것을 모른 채 방법을 썼다.** SI 의 `[인쇄]` "The well-fitted `Z_DRT`
can represent the **actual physics** in the system" 이 그 증거다.

---

# 19. 우리 프로젝트와의 접점

**(1) 우리가 이 논문에 공급할 수 있는 것 — 그리고 그것이 크다.**
38호가 가진 것: 같은 셀에 대한 **nuisance 1 점 변동**(Fig. S3), **조작 하나**(압력),
**시계열 6 점**. 38호가 없는 것: **정규화 설정** · **불확실성** · **개수 선택 규칙**.
→ [[near-optimal-set-width-measurement]] 의 기계는 **이 문제에 그대로 붙는다**:
`λ` 를 격자로 흔들고 각 `λ` 에서 봉우리 개수·위치·높이가 어떻게 변하는지를 재면,
**Fig. S3 의 1 점이 곡선이 된다.** `[해석]` 그것이 **"DRT 로 잰 저항 증가분" 에
폭을 붙이는 최소 절차**이고, 우리 저장소의 폭 측정 논리가 **화학·방법에 무관**하다는
것이 여기서 다시 확인된다.

**(2) 가져올 수 있는 관측 — 하나 있고, 조건이 붙는다.**
**"압력 재가압 전후의 스펙트럼 차"** 는 우리가 찾던 종류의 **분리 연산자**다.
⚠ 그러나 38호가 보여 준 것은 **연산자가 직교하지 않는다**는 것이다 — 재가압이
P2(화학)·P4(전하이동)도 10–25 % 줄인다. → [[assb-pressure-reapplication-separation-test]]
의 `Q_apparent = θ_AM(P,N) · η(i) · Q_material(N)` 에서 **`P` 가 `θ_AM` 에만
들어간다는 가정에 반례가 붙는다.**

**(3) 라벨의 층위 — 38호의 라벨은 우리 degeneracy 에 정면으로 걸린다.**
P3 봉우리 높이를 "기계적 접촉 손실" 이라 부르는 것은 **fitted-label 을 measured
처럼 쓰는 전형**이다. 그리고 **그 fitted 의 자유도(λ, RBF shape, 전처리, ECM
차수)가 하나도 보고되지 않았다.** 9호의 `fitted-single-parameter` 위에
**`inverted-nonunique`** 층위를 얹는다.

**(4) ★ Q8 이 닻 카드의 전제를 깬다** (§14) — graphite 음극이면 5 → 3 붕괴가
성립하지 않는다.

**(5) 우리 수치와의 관계**: 이 digest 의 수치는 **전부 38호의 것**이다.
우리 연구 수치의 정본은 artifact + `degradation-degeneracy/docs/RESULTS*.md` 이며
여기에 복사하지 않았다.

---

# 20. 후속으로 받아야 할 원 논문 (우선순위)

| # | 논문 | 왜 |
|---|---|---|
| **1** | ★★★ **T.H. Wan, M. Saccoccio, C. Chen, F. Ciucci, "Influence of the Discretization Methods on the DRT Deconvolution: Implementing Radial Basis Functions with DRTtools", *Electrochim. Acta* 184 (2015) 483** (ref. [16] / SI [2]) | **38호의 DRT 가 전부 이 코드다.** λ 와 RBF shape factor 가 **이 논문의 인터페이스**이고, 그 두 손잡이가 봉우리 개수를 어떻게 바꾸는지가 여기 있다. **G1 을 닫는 유일한 경로** |
| **2** | ★★★ **S. Hori, R. Kanno, … E. Ivers-Tiffée, "Understanding the impedance spectra of all-solid-state lithium battery cells with sulfide superionic conductors", *J. Power Sources* 556 (2023) 232450** (ref. [14]) | **같은 재료계(LPSCl/LGPS + LNO-LCO + In–Li)의 EIS–DRT 를 Ivers-Tiffée 그룹이 한 것.** 38호의 봉우리 귀속을 **외부에서 검증**할 수 있는 유일한 후보 |
| **3** | ★★★ **M.A. Danzer, "Generalized distribution of relaxation times analysis for the characterization of impedance spectra", *Batteries* 5 (2019) 53** (ref. [33]) | **10호가 개선 경로로 지목했고 38호가 인용만 하고 안 쓴 것.** 10호의 세 경로 중 이 계보에 **이미 인용으로 들어와 있는 유일한 편** |
| **4** | ★★ **F. Ciucci, "Modeling electrochemical impedance spectroscopy", *Curr. Opin. Electrochem.* 2019** (10호 ref. 50) + **Huang, Papac, O'Hayre, Bayesian DRT (2020)** (10호가 지목) | **DRT 의 ill-posedness 와 불확실성 정량.** G1·G3 을 닫는다 |
| **5** | ★★ **K. Pan, F. Zou, M. Canova, Y. Zhu, J.-H. Kim, "Comprehensive EIS study of Si-based anodes using DRT analysis", *J. Power Sources* 479 (2020) 229083** (ref. [17]) | **38호 교신저자(J.-H. Kim)의 선행 DRT 연구**이고 **케이블 인공물(P1 이동)의 1 차 근거**다. 우리 `pvs-sev` 계열(Si 음극)과도 겹친다 |
| **6** | ★★ **J. Illig, M. Ender, T. Chrobak, J.P. Schmidt, D. Klotz, E. Ivers-Tiffée, "Separation of charge transfer and contact resistance in LiFePO₄-cathodes by impedance modeling", *JES* 159 (2012) A952** (ref. [9]) + **J.P. Schmidt et al., *J. Power Sources* 196 (2011) 5342** (ref. [19]) | ★ **P3 = "solid-solid contact impedance" 라는 귀속의 원전이다.** 38호가 이 두 편만 근거로 **액체셀 LFP/Al 집전체 접촉저항의 주파수대**를 황화물 ASSB 양극 복합체에 옮겨 쓴다 — **그 이식이 정당한지 원전에서 확인해야 한다** |
| **7** | ★ **P. Minnmann, … J. Janek, "Designing cathodes and cathode active materials for solid-state batteries", *Adv. Energy Mater.* 12 (2022) 2201425** (ref. [18]) | 38호의 입도 가설의 출처. 우리 2호(Clausnitzer)가 인용한 Minnmann 2021 의 후속 |
| **8** | **M. Gaberšček, "Understanding Li-based battery materials via EIS", *Nat. Commun.* 12 (2021) 6513** (ref. [7]) | `[인쇄]` "overlaps of neighboring semi-circles are often **misled into missing features**" 의 출처 — **"원호를 눈으로 세면 안 된다" 의 정식 근거** |
| **9** | **L. Höltschi et al., "Performance-limiting factors of graphite in sulfide-based all-solid-state Li-ion batteries", *Electrochim. Acta* 389 (2021) 138735** (ref. [32]) | **graphite 음극 ASSB 의 열화 기구** — 38호가 Q8 에서 연 새 축(흑연 음극)의 후속 |
| **10** | **T. Shi, … G. Ceder (2020)** (ref. [21]) | **이미 우리 위키에 있다** (`assb` 4호). 38호가 "agree with" 라고 쓴 상대이고 **회복 크기가 12 배 다르다** — 대조는 이미 §5.2 에 적었다 |

---

# 21. 한 줄 요약

**황화물 ASSB 완전지의 EIS 를 DRT 로 풀어 P1–P5 의 주파수 ↔ 물리 지도를 만든
산업체·대학 공동 논문이고, `assb` 계보 최초로 (i) graphite 음극 완전지 (ii) 완전지
↔ 두 반쪽전지 분해 (iii) 압력 → 용량 + 압력 → DRT 봉우리 사상을 준다.
동시에, 그 지도 자체가 축퇴를 그림으로 인쇄한다 — P2·P3 에 양극과 음극이 같이
찍혀 있고, P4 와 P5 가 ≈10 Hz 에서 겹쳐 그려져 있으며, P3 의 보고 위치가 논문
안에서 1.3 자릿수에 걸쳐 흔들려 P2 와의 간격(0.8 자릿수)보다 크다.
그리고 SI Fig. S3 이 같은 셀에서 배선만 바꿔 DRT 봉우리를 −15 % ~ +69 % 움직여
놓았는데, 본문의 재가압 효과(−10 ~ −25 %)가 그 폭 안에 들어간다 — 논문은 그
뺄셈을 하지 않고, `regulariz*`·`uniqu*`·`uncertaint*`·`Kramers` 를 한 번도 쓰지
않는다.**

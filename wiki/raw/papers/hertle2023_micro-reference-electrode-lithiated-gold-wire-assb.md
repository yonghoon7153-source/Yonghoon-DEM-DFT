---
title: "Hertle, Walther, Mogwitz, Schröder, Wu, Richter, Janek 2023 — Miniaturization of Reference Electrodes for Solid-State Lithium-Ion Batteries (J. Electrochem. Soc. 170, 040519)"
source_url: local-upload/7._Miniaturization_of_reference_electrodes_for_solid-state_lithium-ion_batteries.pdf + 7._Sup_Miniaturization_of_reference_electrodes_for_solid-state_lithium-ion_batteries.pdf (SI)
source_url_note: "본문 PDF 10 쪽(1 쪽 = IOP 표지, 논문 9 쪽, 참고문헌 40) + SI 5 쪽(Fig. S1-S7 · Table S1, 교차참조 결손 5 곳). 크로퍼 21 장(본문 그림 13 + SI 그림 7 + 표 1) 중 그림 15 장을 봤다(Fig. 1 · 3-13 · S1 · S5 · S7), 안 본 것 Fig. 2 · S2 · S3 · S4 · S6. 화소 판독 Fig. 7(두 패널) · Fig. 10(주파수 범위) · Fig. 13 아래 패널. 원자료 · PDF 는 커밋하지 않는다. 16호(Ramanayagam 2026)가 μ-RE 0 V 를 인용한 원전 · 21호가 '0 V 리튬화 금선 관례의 출처' 로 지목."
source_doi: 10.1149/1945-7111/accb6f
source_license: "CC BY-NC-ND 4.0, (c) 2023 The Author(s), published on behalf of The Electrochemical Society by IOP Publishing — open access"
pdf_sha256: 2986b17772b55bcfed7a2f01856d0ed5ad623e4fb8bae74f21244893723d6f76
si_sha256: 9c39f6530af4e2ce262500b14d50430a87a6654ebc2b5c77ad6f6a58f8884cf9
ingested: 2026-09-23
sha256: a5495a03242ce4e2632b4890a7a98e1a1b9775d2327ffe39ad0844c6dd6137b1
---

# 수집 목적

`assb` 섹션 **45호**. 큐 **46번**(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g, 2차 묶음 일곱째 편).
닻은 `questions/assb-contact-loss-vs-lampe.md` 의 **Q5**. 원장 ★★★ · 지목 2 회:
16호(Ramanayagam 2026) 가 자기 μ-RE 의 기준 전위를 **이 편의 "stable potential of 0 V vs Li"** 로 놓았고(16호 G6 —
자기 셀의 기준 전위 안정성을 재지 않음), 21호(Sedlmeier 2023) 가 **"0 V 로 놓은 리튬화 금선" 관례의 출처**로 지목하며
16호 셀 간 0.11 V 어긋남 가설(21호 §5-2) 검증을 이 편에 걸었다.

같은 계보에서 이미 본 것: 40호 R-LTO(원전 · 상호 증언) · 41호 Nam(기준극 교체 대조, 배면형 기준극) · 42호 Santhosha(0.62 V 액체 원전) ·
43호 Fukunishi(공통 모드 표류 ≈−14 mV · 합 일치로 "proves" — 범주 오류). 이 편은 **JLU Giessen(Janek) + BASF** — 16호(Marburg) ·
21호(TUM) 와 **다른 연구실**이다.

> 표기: `[인쇄]` 본문 · SI 명시 · `[도표]` 그림에서만 읽은 값(`figure-read ≈`, 판독 오차 붙음) ·
> `[재현]` 우리가 지면의 숫자로 계산한 값 · `[해석]` 우리 해석.
> **`[해석]` 표시 없는 문장은 원문이 실제로 말한 것이다.**

---

# 판정 (먼저)

## (1) Q5 — "0 V vs Li" 를 무엇으로 정했나

| 물음 | 이 편 | 판정 |
|---|---|---|
| **Li 금속 대조(41호형 기준극 교체)?** | **없다 — 대신 기준극 자체가 Li 금속이다.** `[인쇄]` "After complete lithiation of gold to AuLi₃, lithium metal is plated on the μ-RE leading to another plateau of 0 V vs Li⁺/Li". 0 V 는 **상(相) 정체**(도금 Li)로 정해진다. 상 정체의 증거는 **Fig. 7 의 평탄 사다리**(Au/AuLi → AuLi/AuLi₃ → 도금) 하나이고, 사후 단면에서는 `[인쇄]` "the metallic lithium cannot anymore be detected" | ⚠ **간접** — 사다리 판독(아래)은 우리 것 |
| **측정된 수 하나** | `[인쇄]` Fig. 7 캡션 "a stable potential of **–618 mV vs In/InLi**" — **측정 축 `U_R-A` 그대로**(환산 축 아님) · `[인쇄]` "the In/InLi anode … exhibited a stable potential of **618 mV** vs Li⁺/Li"(인용 **없음**, ± 없음) | ★ **계보 첫 인쇄 수: ASSB 셀 안에서 Li 금속(도금) ↔ In/InLi = 0.618 V** — 42호 액체 0.622 · 41호 SI `[도표]` ≈0.621(수 미인쇄) 와 3–4 mV. 단 **문장은 가정형**("was assembled with the appropriate lithium/indium ratio and **therefore** exhibited") — 측정된 것은 **차 −0.618 V 하나**다(21호와 같은 구조) |
| **`[재현]` 사다리 내부 눈금** | `[도표]` 화소 판독(Fig. 7 위 패널, 눈금 3.33 mV/px): AuLi/AuLi₃ **개방회로** 평탄 **−0.485 V** · 도금 평탄 **−0.618 ± 0.001 V**(18–32 h, 96 열) ⇒ 간격 **0.133 V** ↔ `[인쇄]` 문헌 E(AuLi/AuLi₃) = **134 mV** vs Li | ✅ **In/InLi 값에 기대지 않는 교차 검사가 한 번 선다**(우리 판독) — 마지막 평탄이 AuLi/AuLi₃ 보다 134 mV 아래 = Li. 단 134 mV 자체가 인용값(refs 20 · 33–35)이고, Au/AuLi 전류 중 평탄은 −0.365 … −0.375 V(→ +0.24–0.25 V, 문헌 0.215 와 ≈+30 mV) |
| **시간 안정성(드리프트 값 · 기간)** | `[인쇄]` "a mean thickness of 4 μm … leading to a stable potential of 0 V vs Li⁺/Li **for at least 8 days**" · "the μ-RE was **typically stable for about 8 days**". **그림 0 · mV 기준 0 · 표류 수 0**(`drift` 0 회). 지면의 유일한 개방회로 추적은 **AuLi/AuLi₃ 평탄 위 ≈5 h**(`[도표]` −0.485 → ≈−0.48 V) — **Li 평탄의 개방회로는 32 h 끝 점 몇 개뿐** | ❌ **값이 없다.** "안정" 의 판정 기준이 인쇄되지 않았다 |
| **점검 방법** | `[인쇄]` "The stability of the lithiated μ-RE was controlled between the various experiments by measuring the voltage U_RE-A between the μ-RE and the In/InLi anode" · 장기 시험은 "**refreshed**"(추가 도금) 또는 "checked regularly (against the In/InLi anode) and … quickly relithiated" | ⚠ 점검 상대가 **실험 중 전류를 나르는 상대극**(In/InLi)이고, 그 전위가 618 mV 로 **가정**된다 — 21호 Fig. A·1 과 같은 순환(측정된 것은 차 하나). 단 **실험 사이** 개방회로 점검이라 20호 "3전극은 자기 표류를 못 본다" 의 P10 처방(알려진 2상 평탄 대조)을 **절차로는** 한다 — 결과 수치는 없다 |
| **누설(원장 구조적 공백 3)** | `leak` **0** · 자가 소비 측정 0 · 대신 **기구를 문장으로**: `[인쇄]` 얇은 Li 는 "reacts completely with the SE which then results in a different potential" · Au–Li 평탄은 "reductive degradation of the solid electrolyte around it, which led to quick depletion of lithium in the wire" | ❌ **누설 직접 측정 0/45.** `[재현]` 수명이 Li 소진으로 끝난다면 평균 소비 **≈39 nA ≈ 12.5 µA cm⁻²**(도금 7.57 µAh ÷ 192 h) — 21호 GWRE 간접 상한 < 4.3 nA 의 ≈9 배 |
| **리튬화량(µAh) ↔ 수명** | `[인쇄]` 처방 한 점: **1 µA × 8 h = 8 µAh**(와이어 면적 3.14 × 10⁻³ cm² → 2.55 mAh cm⁻²) ⇒ Li 두께 "4.3 μm"(= "4 μm" = "5 μm", 세 값) ⇒ "≥8 일". 정성 규칙: 얇으면 SE 와 반응해 전위가 바뀌고, 두꺼우면 오래가지만 임피던스 질이 떨어진다("compromise") | ⚠ **처방 한 점, 곡선 0.** `[재현]` 20호 (5′)(재고/(소비 × 시간) ≥ 10)을 걸면 이 처방은 **≤ ≈19 h 실험**까지만 보증 — 저자의 "refresh" 가 이 공백의 실무 해법이다 |

⇒ **Q5 스물한 번째 형태 — "셀 안 도금 Li: 영점을 상 정체(평탄 사다리)로 정하고, 기준극을 수명 있는 소모품으로 인쇄했다(재리튬화 '새로고침')"**.
계보 앞 형태와의 차: 41호(교체 대조 · 셀 간 · 수 미인쇄) · 21호(교정 셀 → 이식) 와 달리 **측정 셀 안에서** Li 금속 대비의 차(−618 mV)를
**측정 축으로** 인쇄했다(P11 의 ASSB 판 — 42호 주석 "측정 셀 안 = ASSB 안" 을 처음 충족). 그러나 **표류 값 · 누설 · 반복 0**.

## (2) 16호 이식(∅25 µm, 5 µA × 30 min) — **조건 밖이다**

| 항목 | 이 편(원전) | 16호 | 판정 |
|---|---|---|---|
| 와이어 | Au 도금 W **∅10 µm**, 3–5 wt% Au(Goodfellow) | Au 도금 W **∅25 µm**(Au 분율 미인쇄) | 2.5 배 |
| 상대극(리튬화) | **In/InLi**(`[인쇄]` "making use of the excess lithium and the stable potential") | **NMC 복합양극**(신품) | ⚠ 상대극이 평탄이 아니면 **사다리를 읽을 수 없다** |
| 전하 | 8 µAh / ≈1 cm = **8 µAh cm⁻¹** · 면적당 **2.55 mAh cm⁻²** | 2.5 µAh / ≈1.2 cm = **2.1 µAh cm⁻¹** · 면적당 **0.27 mAh cm⁻²** | 길이당 1/3.8 · 면적당 1/9.6 |
| AuLi₃ 채우는 전하 | `[인쇄]` 0.43 µAh(∅10) | `[재현]` 같은 Au 분율이면 Au 량 ∝ d²·L: 인쇄 비율 그대로 **3.2 µAh**(> 2.5) · 3–5 wt% 로 **1.4–2.3 µAh** | **도금 Li 여분 ≤ 1.1 µAh → 없을 수도 있다** |
| 도금 Li 두께 | 인쇄 4–5 µm · `[재현]` 원통 ≈6.9 µm | `[재현]` **0 – ≈0.55 µm** | ≥ 1/10 |
| 리튬화 곡선 | Fig. 7: 두 평탄 + 도금 평탄(−618 mV) | 16호 Fig. S1: **평탄 없이 560 mV 표류** | 원전 기준(도금 평탄 도달)을 **충족했다는 증거 없음** |
| 점검 · 새로고침 | 실험 사이 In/InLi 대비 | 0 | — |

⇒ `[해석]` **16호의 "0 V (Hertle 인용)" 은 원전의 조건을 물려받지 않는다.** 원전 자신의 문장("thin layers … react completely … different potential")이
16호 쪽을 가리킨다. `[재현]` 원전 처방의 면적당 소비율(≈12.5 µA cm⁻², 수명 = 소진 가정)을 16호 여분(≤0.12 mAh cm⁻²)에 대면 **≤ ≈9 h** —
16호 임피던스는 **2 번째 사이클 SOC50**(0.1 C 로 ≥ ≈25 h 뒤)에서 쟀다.
★ **16호 셀 간 0.11 V 의 새 후보** `[해석]`: 원전 사다리에서 도금 Li 가 소진되면 기준극은 **AuLi/AuLi₃ 칸(+0.133 V, 우리 판독)** 으로 올라선다.
그러면 In–Li 는 0.618 − 0.133 = **0.485 V** 로 읽힌다 ↔ 16호 한 셀 **0.47 V**(15 mV). 다른 셀 0.58 V 는 기준극 +0.04 V — 사다리의 칸이 아니다
(소진 중 · 혼합 전위 후보). 즉 **0.11 V ≈ 사다리 한 칸(0.133 V) − 23 mV**. 21호 후보(순수 Au 선의 이완 경로 0 → 0.31 V)와 **양립하며 더 좁다**
— 16호 와이어는 21호(순수 Au)가 아니라 **이 편과 같은 Au 도금 W** 다. **가설이지 결론이 아니다**(16호 Au 분율 · SE · 측정 시점 미확인).

## (3) "3E 합 ≈ 2E" 검증 — 범주 오류인가, >10 kHz 편차는 무엇인가

- `[인쇄]` 식 (1) `Z(E_C − E_RE) + Z(E_RE − E_A) = Z(E_C − E_A)` · 식 (2) 잔차 · Fig. 10 "residuals are below 1% for the real part and below 10% for the imaginary
  part demonstrating very good agreement … and **validating the results of the reference electrode concept and construction**" · 결론 "The proper function of the μ-RE is
  firstly demonstrated by impedance analysis of 2E and 3E cells … Their combination **agrees perfectly**".
- `[해석]` **합 일치가 보는 것과 못 보는 것.** 같은 셀에서 잰 세 스펙트럼이면 식 (1) 은 **키르히호프 항등식**이다(20호 DC 판과 같은 구조). 그래서
  (i) 기준극의 **DC 전위 · 표류는 임피던스에 들어가지 않는다** — 0 V 가 맞는지와 무관하게 통과한다; (ii) **기준극 위치 artifact**(40호가 짚은
  Ender · Ivers-Tiffée 2017 계열 — 분리막 · 전극 임피던스를 두 반쪽에 **재분배**하는 것)는 **합에서 상쇄된다** — 합 일치는 위치 artifact 의 부재를 증명하지 못한다;
  (iii) 보는 것은 **측정 사슬**(기준극 채널의 고임피던스 × 표유 용량 · 순차 측정 사이의 비정상성)뿐이다. 판별력은 0 이 아니지만 **과녁이 다르다.**
- **같은 셀인가** — 지면은 말하지 않는다. `[재현]` Fig. 10 의 고주파 실수부 ≈62 Ω(≈48.7 Ω cm²)는 2E 레시피(60 mg, 최소 ≈29 Ω cm²) · 3E 레시피(200 mg,
  완전 밀도 · 1.4 mS cm⁻¹ 에서 **97.5 Ω cm²**) 어느 쪽과도 안 맞고, **서로 다른 두 펠릿이 전 대역 <1 % 로 겹치는 것은 분리막 두께 산포만으로도 어렵다**
  ⇒ `[해석]` 같은 셀의 C–A ↔ C–R + R–A 비교일 가능성이 크다(= 항등식). 그리고 **Fig. 10 셀은 Fig. 5 · 11 · 12 · S7 셀과 다르다**(아래 §6).
- **>10 kHz 편차의 원인**: `[인쇄]` 원인 서술 없음(일반론 "natural noise, … temperature or pressure" 뿐). `[도표]` 허수부 잔차 ≲1 %(<10 kHz) → **≈4–8 %**(30–100 kHz) ·
  실수부 ≲0.5 %. `[해석]` (ii) 에 의해 **위치 artifact 는 합 편차의 원인일 수 없다**(상쇄된다). 남는 후보는 **기준극 채널 측정 artifact** — ∅10 µm × 1 cm 의
  작은 면적(3.14 × 10⁻³ cm²)이 만드는 높은 기준극 임피던스 · 표유 용량의 저역 통과. ★ 그리고 **양극 반쪽 스펙트럼에만 있는 고주파 호 #1**(Fig. 11 · 12,
  `[도표]` −Im ≈19.5 Ω at 100 kHz, 원문 배정 "SE separator") 이 같은 부류의 후보다 — `[재현]` 호 모양으로 τ ≈0.6 µs, R ≈57 Ω(가정) ⇒ C ≈10 nF ↔ 분리막 반쪽
  기하 용량 ≈10–100 pF(ε_r 10–100 가정) — **×100–1000** 크다(§10 3-b). 2E 스펙트럼(Fig. 10 · 5)에는 이 높이의 호가 없다.
- ⇒ **계보의 합 일치 검증 계열**(20호 DC 항등식 · 40호 임피던스 합 · 43호 "proves the stability") **에 이 편이 들어간다** — 이 편은 DC 전위를 합으로 "증명" 한다고
  쓰지는 않는다(0 V 는 사다리 · 개방회로 점검으로 따로 논한다). 그러나 결론이 합 일치를 "proper function" 의 첫 근거로 둔다. **16호는 이 검사를 원전에서 가져가
  자기 검증으로 썼다**(16호 칸 이동 근거 중 "자기 검증" 부분은 이 판별력 한계를 그대로 물려받는다 — 칸 자체(전극 분해 관측)는 유지).

## (4) 칸 이동 — **≈19.0 → ≈19.5 (Q5 +0.5)**

근거는 **논문의 측정 + 인쇄된 명제**다: Fig. 7 측정 축 `U_R-A` 위 도금 평탄 −618 mV(셀 안 Li 금속 ↔ In/InLi) · 인쇄 수명("at least 8 days") ·
인쇄 실패 기구(얇은 Li 소진 → 다른 전위 · Au–Li 평탄은 SE 환원으로 불안정) · 인쇄 유지 절차("refreshed", 실험 사이 In/InLi 대비 점검).
**반 칸인 이유**: 표류 값 0 · 8 일 그림 0 · 누설 0 · n 미인쇄 · 618 mV 의 문장 지위가 가정형 · 사다리 교차 검사는 우리 판독 · 8 µAh 처방의 리튬화 곡선이
어느 패널인지 불명(G4).
안 움직인 칸: Q1(`θ(N)` 0/45 — 신품, 접촉 0) · Q2(반 칸 검토 후 접음 — 2E 적합 비유일성을 S7 이 가른다는 것은 **우리 판독**, 상대극 Li 소진 → 용량 귀속은 20 · 17 · 41호와 같은 층) ·
**Q4 0/45 — 서른일곱 번째 성질** · Q6(제조 382/374 MPa · 운전 63.7 MPa 명시, 스윕 0) · Q7 해당 없음 · Q8(NCM851005, OCP 0).

## (5) 가장 날카로운 것 넷

1. ★★★★ **"0 V" 의 원전은 인용이 아니라 상 정체다 — 그리고 그 상은 소모품이다.** 도금 Li 가 있는 동안만 0 V 이고, 떨어지면 기준극은 **양자화된 칸**
   (AuLi/AuLi₃ **+0.133 V** · Au/AuLi ≈+0.215–0.25 V)으로 올라선다. 기준 이동이 연속 표류가 아니라 **계단**이다 — 완전지 분해에서 **일정한 오프셋**으로
   숨는 종류(`LLI`/`LAM_PE` 흉내, [[assb-li-in-reference-potential-window]] "왜 중요한가 1").
2. ★★★★ **16호는 원전 조건 밖이다**(와이어 2.5 배 · 면적당 전하 1/9.6 · 상대극 NMC · 평탄 무 · 점검 무) — 16호 0.11 V 에 **사다리 한 칸(0.133 V)** 이라는 새 후보가 붙는다.
3. ★★★ **2E 임피던스 분할의 비유일성을 저자가 인쇄했다** — `[인쇄]` "Both sets of parameters fit the experimental data equally well using the same equivalent circuit"
   (Table S1: `R_anode` **14 ↔ 3.9 Ω cm²**, ×3.6). `[재현]` 같은 셀 3E 반쪽(S7, 음극 호 ≈12–13 Ω cm²)이 **Fit 1 을 고른다** — 저자는 고르지 않았다.
   그러나 3E 에서 양극은 TLM ↔ 직렬 R-CPE 두 모델이 **둘 다 맞고**, "physically meaningful" 로 골랐다 — **비유일성이 파라미터에서 모델 구조로 옮겨 갔다.**
4. ★★★ **율 시험의 "2E 방전 용량 부족" 은 상대극 Li 소진이다** — `[인쇄]` "LTO is delithiated when assembling the cell and no lithium excess is present" ·
   "side reactions that are consuming Li". `[도표]` 0.1 C: 2E 방전 ≈165 ↔ 3E ≈193 mAh g⁻¹, 음극이 **≈160–165 mAh g⁻¹ 에서 1.55 → 3.2 V** 로 뛴다.
   2전극만 보면 **양극 용량 손실처럼 보이는 `LLI`** — 카드 물음의 반대편(`LLI` → 겉보기 `LAM_PE`, 17호 · 21호)이 **LTO 상대극**에서 다시 선다.
   ⚠ 3E 의 193 에서 165 너머 ≈28 mAh g⁻¹(≈0.21 mAh)는 **음극이 2.5–3.2 V 로 끌려가는 동안** 흐른 전하다 — `[해석]` 음극 쪽 산화 부반응(SE 산화 후보)이
   Li⁺ 원천이다. 양극이 받은 용량은 실제지만, 그 셀은 그 구간에서 **상하고 있다**.

---

# 0. 원문에 없어서 확인이 필요한 것

| # | 공백 | 왜 걸리나 |
|---|---|---|
| **G1** | **기준 전위 표류의 수 0.** "at least 8 days" · "typically stable for about 8 days" 에 그림 · mV 판정 기준 · 표류값이 없다(`drift` 0 회) | Q5 의 핵심. "안정" 이 ±1 mV 인지 ±30 mV 인지 모른다 |
| **G2** | **누설 · 자가 소비 측정 0**(`leak` 0 회) | 원장 구조적 공백 3 — **0/45** |
| **G3** | **618 mV 의 지위.** 인용 없음 · ± 없음 · 문장은 가정형("assembled with the appropriate lithium/indium ratio and therefore exhibited") | 측정값(Fig. 7)인지 전제인지가 문장으로 갈리지 않는다. 비리튬화 환산은 0.62 · 0.63(D15) |
| **G4** | **Fig. 7 두 패널의 와이어 직경 · 전류 · 전하 미인쇄.** 본문은 Fig. 7 을 ∅10 µm 와 ∅100 µm 두 경우에 다 건다. `[인쇄]` ∅10 µm 는 첫 평탄이 "barely visible" 인데 두 패널 모두 첫 평탄이 뚜렷하다 | **8 µAh 처방(실제 쓴 μ-RE)의 리튬화 곡선이 어느 것인지 모른다.** `[재현]` 아래 패널의 도금 도달 ≈0.37–0.38 h 는 1 µA 에서 ≈0.37 µAh ≈ 인쇄 `Q_AuLi3` 0.43 µAh 와 가깝다(∅10 µm · 1 µA 와 양립) — 그러나 캡션은 "faster lithiation" |
| **G5** | **리튬화량 ↔ 수명의 곡선 0** — 처방 한 점(8 µAh ≈ 8 일) | (5′) 를 설계할 수 없다 |
| **G6** | **셀 수 n · 반복 · 산포 0**(`reproducib*` 0) | 8 일 · 618 mV · 합 잔차가 모두 대표 한 셀인지 모른다 |
| **G7** | **Fig. 10(검증) 셀이 어느 레시피인지, 2E 와 3E 가 같은 셀인지 미인쇄** — `[재현]` Fig. 10 고주파 ≈48.7 Ω cm² ↔ Fig. 5 · 11 · S7 셀 ≈97 Ω cm² | 검증한 셀과 분석한 셀이 다르다 |
| **G8** | **3E TLM 파라미터 표 없음** — 본문 "These parameters can be found in Table S1" 이지만 Table S1 은 **2E 두 적합**이다. 3E 는 σ_ion(eff) 0.145 mS cm⁻¹ · R_CT 17.8 Ω cm² 두 값뿐, ± 0 | 1단계(`R`·`C`) 입력 없음 |
| **G9** | **복합체 조성 미인쇄** — 양극 NCM : SE 비 · LTO/SE/C65 비 · LTO 질량 · LTO 3E 셀 조립 절차 | `[재현]` 1 C = 1.44 mA ÷ 190 mA g⁻¹ ⇒ NCM 7.58 mg = 12 mg 의 **63 wt%**(LTO 셀) |
| **G10** | **Fig. 13 의 2E 가 별도 셀인지 · 같은 셀의 다른 사이클인지 미인쇄**, 사이클 번호 미인쇄 | "33 % 높다" 가 셀 간 산포를 포함하는지 모른다. Fig. 4(2E LTO) 값과도 다르다(D17) |
| **G11** | **TSRE 리튬화 절차 없음** — Fig. 3b "In/InLi" ↔ 조립 문단은 In 박(∅3 mm)만 | TSRE 전위의 정체 미정 |
| **G12** | **사후 분석에서 Li 금속 층 미검출** — `[인쇄]` "the metallic lithium cannot anymore be detected. The original thickness of the plated lithium metal is expected to be 5 μm" | 0 V 상 정체의 직접 증거 0 — 사다리(G4 조건부)만 |
| **G13** | **온도** — Fig. 4 캡션 "θ = 25 °C" 한 곳 | 3-a 불가 |

---

# 1. 서지 · 낱말 지문

| 항목 | 값 |
|---|---|
| 서지 | **Jonas Hertle**¹², Felix Walther¹², Boris Mogwitz¹², Steffen Schröder¹², Xiaohan Wu³, Felix H. Richter¹², **Jürgen Janek¹²(교신)** — "Miniaturization of Reference Electrodes for Solid-State Lithium-Ion Batteries", ***J. Electrochem. Soc.* 170 (2023) 040519**, `10.1149/1945-7111/accb6f` |
| 소속 | ¹ Institute of Physical Chemistry, **JLU Giessen** · ² ZfM, JLU Giessen · ³ **BASF SE**, Ludwigshafen |
| 일정 | 투고 2023-01-31 · 수정 2023-03-13 · 게재 2023-04-19 |
| 지원 | BASF SE(International Network for Batteries) · BMBF FESTBATT(03XP0177A) |
| 라이선스 | **CC BY-NC-ND 4.0** · © 2023 The Author(s), ECS/IOP — 오픈액세스 |
| 쪽 | PDF 10 쪽 = IOP 표지 1 + 논문 9(참고문헌 40). SI 5 쪽(Fig. S1–S7 · Table S1, Word 원고 그대로 — 교차참조 "Error! Reference source not found." **5 곳**) |

**낱말 지문** (NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문(참고문헌 전); SI 는 괄호):

| `identifiab` | `uncertaint` | `conf.interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM` | `degradation mode` | `contact loss` | `MPa` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 0 | **7** (SI 0) |

NFKC 변경 본문 **67 자**(`ﬁ` 54 · `ﬂ` 13) · SI 0 — **열 변화 0**. 소프트 하이픈 0 · 줄끝 하이픈 15 곳(이으면 `unequivoc*` 2 → 3 · 열 변화 0).
⚠ IOP 조판 추출에서 **양쪽 정렬 줄이 낱말 하나씩 줄바꿈**된다("in\nthe\nfield") — 공백 정규화 뒤 셌다. 식 (1)–(5)는 글자 조각으로 흩어져 렌더로 읽었다.
`MPa` 7 = 제조 382 · 382 · 40 · 40 · 374 + 운전 **63.7 · 63.7**.

Q5 보조: `leak` **0** · `drift` **0** · `calibrat` **0** · `assum*` 2(둘 다 기준 전위 아님 — "Assuming 100% coulomb efficiency" · 2E 음극 과전압 "This assumption, however, is usually
neither checked nor confirmed") · `stable` **16**(μ-RE 관련 11, 수치 판정 0) · `stable potential` 14 · `0 V` 4 · `618` 2 · `0.62` **0** · `1.55` 6 · `refresh*` 2 · `8 days` 2 ·
`lithium metal` 6 · `SEI` 2 · `prove` 1("we present and prove the function") · `valid*` 2 · `residual*` 6(SI 1) · `ambigu*` 2(SI 1) · `unequivoc*` 3 · `reproducib*` 0.
곱 축퇴 보조: `contact` 6(물리 접촉 3 — "worse contact" · "good contact" · "contact to the AuLi₃ phase") · `pressure` 8 · `capacitan*` **0** · `fit*` 18(SI 10) · `degrad*` 5(열화 연구 아님 — SE 분해 · 기준극 열화) ·
`side reaction*` 2 · `consum*` 2(1 은 "Li 를 소비하는 부반응") · `isolat*` · `percolat*` · `loss` 1(서론 "loss in performance").
⇒ **열화 논문이 아니다** — 방법 논문(신품, 율 시험 · 임피던스). `[해석]` **가정은 `assum*` 에 안 걸리고 "therefore exhibited" 에 들어 있다**(21호 "calculated based on" · 18호 "Suppose" 와 같은 부류).

---

# 2. 셀 · 실험 (`[인쇄]`, 괄호 안 `[재현]`)

| 항목 | 값 |
|---|---|
| SE | Li₆PS₅Cl, **1.4 mS cm⁻¹**(NEI 판매값 — 자체 측정 0) |
| 양극 | NCM851005(BASF), 250 °C 12 h 진공 건조 · 복합체 = 마노 유발 15 min 손 혼합 · **12 mg**(NCM : SE 비 미인쇄; LTO 셀은 `[재현]` NCM 63 wt%) |
| 음극 | **In/InLi**: In 박 ∅9 mm × 100 µm + Li 박 ∅4 mm × "∼100 μm"(재료 절은 "∼200 μm", D19) + 강박 ∅10 mm (`[재현]` 전체 Li **19 at%**(100 µm) / 32 at%(200 µm) — 42호 창 ≈1–47 at% 안 · Li ≈2.6 mAh ≫ 양극 ≈1.4 mAh; ⚠ Li 박 아래 국소 Li/In ≈1.2 — 균질화 전) · **LTO/Li₆PS₅Cl/C65**(조성 · 질량 미인쇄) |
| 셀 틀 | PEEK 내경 10 mm(0.785 cm²), 황동 하우징 + 알루미늄 틀 — **운전 63.7 MPa**(2E · 3E 같음) |
| 2E | SE **60 mg** 382 MPa 예압 → 양극 12 mg → 382 MPa 45 s → In/InLi (Fig. 3a: 음극 ≈120 · 분리막 ≈400 · 양극 ≈60 µm; `[재현]` 60 mg 완전 밀도 1.865 g cm⁻³ → **410 µm** ✓) |
| TSRE | 2E 셀을 열어 집전체를 PEEK 절연 중공 원통으로 교체 → SE 10 mg → In 박 ∅3 mm. `[인쇄]` "little to no pressure is applied to the cell during cycling" |
| 3E | SE **100 mg** ≈40 MPa 예압 → 강판으로 평탄화 → Au 선 부착 PEEK 반쪽 → SE **100 mg** ≈40 MPa → 양극 12 mg → **374 MPa** 45 s → In/InLi. (`[재현]` 분리막 200 mg → **1.37 mm**(완전 밀도) — 2E 의 **3.3 배**, "essentially unchanged" 와 D11) |
| μ-RE | Au 도금 W **∅10 µm**, Au **3–5 wt%**(Goodfellow), 60 °C 진공 건조 · PEEK 인렛 양쪽에 Kapton 으로 고정, **분리막 지름 전체를 가로지르는 선형 RE**(SI Fig. S1) · 황동 하우징으로 인출 · 투영 면적 **<0.13 %**(Fig. 1a; `[재현]` 10 µm × 10 mm / 78.5 mm² = 0.127 %) |
| 리튬화 | In/InLi 상대극, **1 µA × 8 h**(A = 3.14 × 10⁻³ cm² — `[재현]` = ∅10 µm × 1 cm 옆면 · 0.32 mA cm⁻²) |
| EIS | VMP-300 · 충방전 뒤 **3 h 휴지** · **300 kHz – 100 mHz**, 15 점/decade, 10 mV · 주파수당 2 주기 대기 + 6 주기 평균 · 2E = 완전지 / 3E = 양극 · 음극 **따로**(각각 μ-RE 대비) |
| 사이클 | 3E: 양극 4.3 / 2.5 V vs Li(1 C = 190 mA g⁻¹_NCM) · 2E In/InLi 3.7 / 1.8 V · 2E LTO 2.75 / **0.95 V**(결과 절 0.9 V, D2) · 율 시험 3E(LTO): **2.9–4.3 V vs Li**, 0.1 · 0.2 · 0.5 · 1.0 C × 2 사이클, **1.0 C = 1.44 mA**(`[재현]` 1.83 mA cm⁻²) |
| 사후 | 펠릿을 수평으로 쪼개 μ-RE 노출 · Leica VCT500 무대기 이송 · Xe 플라즈마 FIB(Tescan XEIA3) · SEM(Zeiss Merlin) · EDS · ToF-SIMS(IONTOF 5–100, Bi₃⁺, 45° 크레이터 측벽, 122 nm) |

---

# 3. 절별 해체

## 3.1 서론 (p1–2)

- `[인쇄]` 2E 는 두 전극 기여를 "hardly can be separated without additional analytical efforts [13]"(ref 13 = **38호 Conforto 2021**) · 임피던스도 저주파에서 겹친다 ·
  셀 조합 · 전극 체계 변화로 가르는 것은 "time-consuming and necessarily not unequivocal or even not possible".
- `[인쇄]` 고체 3E 의 어려움: **기준극 위치**(액체의 Haber-Luggin 모세관 같은 것이 없다) · **소형화** · 고온 처리 시 기준극 열화.
- `[인쇄]` 선례 분류: **두 부류** — "pseudo-reference electrochemical double cells where an electrode is placed on top of a normal cell separated by an SE layer [29]"
  (ref 29 = **41호 Nam 2018** — 41호 digest 의 "배면형 기준극") · "a third (reference) electrode is placed in the middle between anode and cathode [28,30]"
  (ref 28 = **40호 Ikezawa** "LTO covered metal meshes" · ref 30 = **20호 Chang** "indium strips"). 액체의 점형 Au 접점 = ref 20 **Solchenbach 2016**(큐 48).
  "we are aware of only two examples and in only of these impedance data were shown [28,30]"(문장 결손, D16).
- Fig. 1 — 투영 면적 비: 이 편 **<0.13 %** · Chang **"≈1.3 %"(캡션 1.26 %)** · Ikezawa **≈49 %**(저자 사진 화소 계수). `[재현]` Chang 은 폭 1.39 mm × ⌀14 mm
  띠라 **≈12.6 %**(20호 digest 는 11.2 %) — **소수점 한 자리 어긋남(×10, D5)**. 이 편의 주장 방향(μ-RE 가 가장 작다)은 오히려 강해진다.

## 3.2 2전극 셀 (Fig. 4 · 5 · Table S1)

- `[인쇄]` Fig. 4(2E NCM|LTO, 25 °C, 0.1–1.0 C): "From these data alone it is not clear whether this capacity decrease is mainly due to the kinetics of the cathode or the anode" ·
  음극 과전압이 작다는 가정은 "usually neither checked nor confirmed" · "impedance data often do not allow unequivocal deconvolution of cathode and anode partial impedances".
  `[도표]` Fig. 4: 충/방 ≈205/161(0.1 C) · ≈163/153(0.2) · ≈143/136(0.5) · ≈108/103 mAh g⁻¹(1.0 C) · 창 **2.75 / 0.95 V**(곡선 끝; 본문 0.9 V, D2) · 0.1 C 충전 시작 ≈0.4 V.
- ★★★ `[인쇄]` Fig. 5 · Table S1 — **"Due to the overlap of the cathode and anode contributions fitting the data is ambiguous. Both sets of parameters fit the experimental data equally
  well using the same equivalent circuit."** · 캡션 "Deciding which fit represents the system more accurately requires additional experiments. The detailed fit parameters and a separated
  fit for the anode are given in Table SI and Fig. S7".
  Table S1(`[인쇄]`, Fit 1 / Fit 2): `R_SE` 98 / 97 Ω cm² · **`R_Anode` 14 / 3.9 Ω cm²** · `Q_Anode` 4.49 / 3.3 × 10⁻² · `α_Anode` 0.60 / 0.68 · `R_ion` 9.07 / 12.6 × 10³ "Ωcm²" ·
  `R_CAM` 0.24 / 0.27 · `Q_CAM` 3.87 / 5.18 × 10⁻² · `α_CAM` 0.74 / 0.73 · `Q_diff` 9.07 / 7.66 · `α_diff` 0.45 / 0.37. **잔차 수는 Table S1 에 없다**(본문 "exact fit values and
  residuals … are given in Table SI" — D8).
  `[도표]` Fig. 5: 두 적합 모두 98 → 165 Ω cm²; (a) 양극 호 98–145 · 음극 호 ≈145–150 / (b) 양극 98–138 · 음극 138–152. ⇒ `[재현]` **Table S1 의 Fit 1(`R_Anode` 14)이
  Fig. 5b, Fit 2(3.9)가 Fig. 5a** — 순서가 엇갈린다(D6, 우리 판독).
- 회로(Fig. 5 아래): SE 저항 + 음극 (R)(CPE) + 양극 Z 형 TLM(`R_ion` · `R_el` 두 경로, 계면 (R)(CPE)–CPE) — SI Fig. S4 캡션과 같다.

## 3.3 TSRE — 배면형 의사 기준극 (Fig. 6 · S6)

- `[인쇄]` 0.1 C 에서 완전지 · 양극 곡선에 날카로운 봉우리 · 골짜기, 음극(vs TSRE)은 평탄 — "the problem of this cell clearly arises from the cathode". 원인: 이 배치는
  "does not allow applying high pressure … little to no pressure is applied to the cell during cycling leading to a poor performance".
  `[인쇄]` "This setup is a good demonstration on how to use 3E setups for failure diagnosis in cells. Unfortunately, comparison to already existing systems using standard 2E cells are
  difficult because the outer parameters such as pressure … are changed."
- `[도표]` Fig. 6: 충 ≈148 / 방 ≈98 mAh g⁻¹ · 음극 vs TSRE 충전 ≈−0.04 V 평탄 · 방전 +0.04 → +0.11 V(`[인쇄]` "overvoltage of about 40 mV during charge. During discharge the
  overvoltage is rising constantly, probably due to worse contact as the lithium is depleted").
- `[해석]` **41호(Nam) 형 배면 기준극을 이 연구실이 재현하면 압력을 못 건다** — 41호 셀은 74 MPa 운전이었다(41호 digest). 같은 형태라도 셀 틀이 결과를 정한다.

## 3.4 μ-RE 리튬화 (Fig. 7) — Q5 본체

- `[인쇄]` 비리튬화 μ-RE: "an unstable potential of around 1.73 V–2.13 V vs Li⁺/Li (1.11 V–1.50 V vs In/InLi) after assembly, as expected. Lithiation is required to form a proper RE
  with stable and thermodynamically defined electrode potential." · Au–Li 안정 금속간 상 AuLi · AuLi₃, "E(AuLi/AuLi₃) = 134 mV and E(Au/AuLi) = 215 mV vs Li⁺/Li in OCV,
  respectively [20,33–35]" · ∅10 µm 에서는 첫 평탄이 "barely visible", **∅100 µm** 로 하면 "better resolved" · AuLi₃ 뒤 도금 → "another plateau of 0 V vs Li⁺/Li".
- `[인쇄]` 설계 절충: 얇은 Li → "reacts completely with the SE which then results in a different potential" · 두꺼운 Li → 오래 안정, 그러나 "increases the size of the reference
  electrode, thus decreasing the quality of the measured impedance spectra" ⇒ "a mean thickness of 4 μm … stable potential of 0 V vs Li⁺/Li for at least 8 days".
- `[인쇄]` Au–Li 평탄을 기준으로 쓰는 길: 가능하지만 "still lead to reductive degradation of the solid electrolyte around it, which led to quick depletion of lithium in the wire and
  therefore an unstable potential". In/InLi 선: 얇은 In 선이 상용품으로 없고, In 도금은 "easier corroded". SEI: "will not influence the potential of the RE, as long as the SEI is
  primarily ion-conducting".
- **Fig. 7 화소 판독**(`[도표]`, 위 패널 눈금 −0.25/−0.50/−0.75 V = y 206.5/281.5/356.5 → 3.33 mV/px, 안내선 −0.48 · −0.62 가 −0.4817 · −0.6183 으로 재현; 시간 22.0 px/h):

| 구간(위 패널, 시각) | `U_R-A` (vs In/InLi) | vs Li(`[재현]` +0.618) | 문헌 |
|---|---|---|---|
| 리튬화 전(0–4.3 h) | 1.15 → 1.49 V 상승 표류 | 1.77 → 2.11 V | 본문 "1.73–2.13" |
| Au/AuLi(전류 중, 4.5–8.2 h) | −0.365 → −0.41 V(기울어짐) | +0.25 → +0.21 | 0.215 |
| AuLi/AuLi₃(전류 중, 8.5–11 h) | −0.488 → −0.505 V | +0.13 → +0.11 | — |
| **AuLi/AuLi₃ 개방회로(11.8–≈16.5 h)** | **−0.485 V**(→ ≈−0.48) | **+0.133** | **0.134** |
| 재리튬화(17.0–18.2 h) | −0.50 → −0.53 → 낙하 | — | — |
| **도금(18.2–≈31.5 h) + 끝 개방회로(≈32 h)** | **−0.618 ± 0.001 V**(96 열 σ 1.4 mV) | 0 | 0 |

  아래 패널("faster lithiation", 0–2 h, 2.25 mV/px): Au/AuLi ≈−0.375 V(0–0.16 h) · AuLi/AuLi₃ ≈−0.489 V(≈0.19–0.23 h) · 도금 도달 **≈0.37–0.38 h** · 도금 −0.618 … −0.621 V.
- `[인쇄]` 캡션: "it is also possible to stop the lithiation at the AuLi₃ potential plateau and observe a stable OCV. As the required amount of lithium is quite small even minor side
  reactions can lead to an unstable potential of the RE. Therefore, lithium metal is plated on the μ-RE … leading to a stable potential of –618 mV vs In/InLi." · 캡션 "Au/AuLi and
  **Au/AuLi₃** two-phase systems"(→ AuLi/AuLi₃, D14).
- `[해석]` **지면의 유일한 개방회로 안정성 추적은 AuLi/AuLi₃ 칸 ≈5 h(+≈5 mV)** 다 — 본문은 그 칸을 "unstable over a prolonged period" 로 기각하고, 실제로 쓴 Li 칸의 개방회로 추적은
  보이지 않는다.

## 3.5 사후 분석 (Fig. 8 · 9 · S2)

- `[인쇄]` 반으로 쪼갠 펠릿 SEM: "A few cracks are visible in the Li₆PS₅Cl around the wire. Otherwise the SEM images show a good contact of the μ-RE to the SE." · Au 층은 "cracked and
  delaminated from the tungsten core at some points. This could be due to the volume expansion of 269% upon lithiation to AuLi₃ [36,37]" · "the SE is preventing complete delamination" ·
  Li 금속은 FIB 뒤 검출 불가, 원래 두께 "expected to be 5 μm".
- `[도표]` Fig. 8b/c(5 µm 막대): ∅≈10 µm 원판, BSE 밝은 W 심 가장자리에 불규칙한 밝은 조각(≲1 µm) — **4–5 µm Li 껍질은 보이지 않는다**(원문 설명대로).
  Fig. 9(10 µm 막대, 45° 시야): WOₓ⁻ 심 · Au⁻ **점선형 얇은 고리**(`[인쇄]` "not fully dense") · ⁶Li⁻ + ⁷Li⁻ **확산된 고리**(`[인쇄]` "lithium rich degradation products of Li₆PS₅Cl … The
  thickness is on the order of magnitude that is expected") · PO₃⁻ 는 선에서 떨어진 입계에(`[인쇄]` 산화 분해물).
- `[해석]` Li 고리는 **SE 환원 생성물**로 배정됐다 — 기준극의 Li 재고가 **SE 와 반응해 줄어든 흔적**이 사진에 있다(기준극 자신의 "`LLI`"). 양은 없다.

## 3.6 안정성 (본문 p6)

- `[인쇄]` 전문은 §판정 (1) 표. 요지: 실험 사이 `U_RE-A` 로 점검 · In/InLi = 618 mV("therefore exhibited") · "typically stable for about 8 days. This time span was enough to do most
  electrochemical testing" · 장기 시험은 사전 추가 도금 또는 주기 점검 + 재리튬화 · "long time experiments could thus be run without major issues".
- `[해석]` **"8 일" 은 수명(끝 시각)이지 표류 크기가 아니다.** 끝의 모양(계단 · 연속)도, 끝 뒤의 전위(사다리 어느 칸)도 인쇄되지 않았다.

## 3.7 임피던스 — 검증 (Fig. 10) · 적합 (Fig. 11 · 12 · S4 · S5 · S7)

- `[인쇄]` 검증 문장은 §판정 (3). 잔차 정의 식 (2) `e = Z³ᴱ(C−R) + Z³ᴱ(R−A) − Z²ᴱ(C−A)`. `[인쇄]` "the residuals for the imaginary part only get higher than about 1%, when the
  frequency increases beyond 10 kHz. Thus, the frequency range that is typically monitoring electrode impedances can be very well used".
- `[도표]` Fig. 10: Re 145 Ω(≈0.05 Hz) → ≈62 Ω(≈3 × 10⁵ Hz) · −Im 봉우리 ≈11.3 Ω(≈5 Hz) · ≈13.3 Ω(≈800 Hz) · Re 잔차 ≲0.5 % · Im 잔차 ≲1 %(<10 kHz), ≈4–8 %(30–100 kHz).
  데이터 저주파 끝 **≈0.05 Hz**(방법 "100 mHz", D10; Fig. 12 는 0.1 Hz 에서 시작).
- `[인쇄]` TLM: "one electronic pathway provided by the active material and one ionic pathway, provided by the SE … connected by the charge transfer" · 유한 Warburg 가 맞지만
  "only a part of the diffusion contribution is visible … not possible to fit the finite Warburg element reliably" ⇒ CPE 대체 · 직렬 R-CPE 적합은 "a very depressed semicircle … usually a
  sign that the model is not physically meaningful" · 결과 **σ_ion(eff) = 0.145 mS cm⁻¹**(벌크 1.4 의 ≈1/10) · **R_CT = 17.8 Ω cm²**("calculated as described by Braun et al. [38]").
- `[도표]` Fig. 11(= Fig. 12 스펙트럼, Ω cm²): 양극 vs μ-RE **45 → 100 Ω cm²**(`[재현]` Fig. 12 의 57 → 128 Ω × 0.785 ✓) · 호 #1("SE separator") 고주파에서 −Im ≈19 Ω cm² 까지
  솟음 · TLM #2 ≈47–87 · #3 확산 87 → · 직렬 적합 #2 49–73 · #3 73–87. Fig. 12: Re 잔차 ≲0.4 % · Im 잔차 **−5.5 … +6.5 %**.
  SI Fig. S5(교차참조 결손 — Fig. 5 인지 11 인지 불명): Re ±0.6 % · Im **최대 ≈7 %**(캡션 "below 5 %", D9).
  SI Fig. S7(음극 vs μ-RE, R-(R)(CPE)): **51.5 → ≈65 Ω cm²**, 호 ≈12–13 Ω cm², −Im 최대 ≈3.3. 캡션 문장 결손("The second contribution at low frequencies" 에서 끝남).

## 3.8 율 시험 (Fig. 13 · S3) — 2E vs 3E

- `[인쇄]` 식 (3)–(5): `U_C-A = E_C − E_A` · `E_C = E_C⁰ + η_C` · `E_A = E_A⁰ + η_A` — "the measured voltage of a full cell always contains the overpotential of the anode".
- `[인쇄]` LTO 복합음극 "exhibiting a potential of 1.55 V vs Li⁺/Li in OCV" · 2E 컷오프 "1.35 V and 2.9 V"(D2).
- `[인쇄]` 0.1 C: 충전 2E 198 · 3E 197 · 방전 "193 mAh g⁻¹, and 165 mAh g⁻¹, respectively"(→ 그림과 순서 반대, D1) · 음극이 "At around 160 mAh g⁻¹ … rising suddenly to as high
  as 3.2 V" · "as soon as the Li₇Ti₅O₁₂ phase is used up a steep increase" · **"Interestingly this increase is happening early indicating side reactions that are consuming Li."**
  1 C: 충전 2E **112** ↔ 3E **148** · 방전 **96.8** ↔ **146** · 음극 과전압 "up to 300 mV". 원인: "LTO is delithiated when assembling the cell and no lithium excess is present."
- `[도표]` Fig. 13b(기호: + 2E 충 · × 2E 방 · □ 3E 충 · ◇ 3E 방): 0.1 C ≈197/**165** · 198/**193** · 0.2 C 182/155 · 186/182 · 0.5 C 148/131 · 166/164 · 1 C 112(α)/97(β) ·
  148(γ)/≈145(δ). Fig. 13a 아래(음극 vs μ-RE): 0.1 C 충 · 방 모두 **1.55 V 안내선 위(±≈10 mV, 선 두께 수준)** · 0.1 C 방전 ≈160–165 에서 급등 → ≈3.2 V(193) ·
  1 C 충전 끝 ≈1.2 V(γ) · 1 C 방전 ≈1.6 → 2.0(≈130) → 3.3 V(δ, 146) · 사이클 시작 음극 ≈2.4 V(0.1 C) · ≈2.0 V(1 C) — **빈 LTO 로 시작**.
- `[인쇄]` 결론: "The 3E setup shows that the true rate capability of the cathode is **33% higher** than the one evaluated from the 2E cell." (`[재현]` 1 C 충전 148/112 = 1.32 ·
  방전 146/96.8 = 1.51 — 33 % 는 **충전** 쪽)

## 3.9 결론 (p9–10)

- `[인쇄]` "Their combination agrees perfectly with results from 2E cells" · "The physical separation of the anode and cathode impedances by our μ-RE is highly reliable and offers precise
  electrode data" · "can be applied to virtually every SSB cell setup with thiophosphate SEs or other mechanically not too rigid SEs" · "we encourage other researchers in the field to use of
  this type of reference electrodes" — **16호가 바로 그 채택 사례다.**

---

# 4. ★★★★ Q5 — 영점 계보에서의 자리

| | 16호 | 21호 | **45호(이 편, 원전)** |
|---|---|---|---|
| 와이어 | Au 도금 W ∅25 µm | **순수 Au** ∅50 µm, 노출 0.5 mm | Au 도금 W ∅10 µm, ≈1 cm |
| 리튬화 | NMC 상대, 5 µA × 30 min = 2.5 µAh | 3 µAh | **In/InLi 상대, 1 µA × 8 h = 8 µAh** |
| 면적당 | ≈0.27 mAh cm⁻² | ≈3.8 mAh cm⁻² | ≈2.55 mAh cm⁻² |
| Au 량 대비 Li(`[재현]`) | AuLi₃ 용량의 ≈0.8–1.8 배(가정 조건부) | 노출부 Li/Au ≈1.2(벌크 평형이면 AuLi/AuLi₃ 칸 — 0.31 V 와 안 맞는다) | AuLi₃ 용량의 **≈19 배**(인쇄 0.43 기준) |
| 놓은 영점 | 0 V(Hertle 인용) | **0.31 V**(Li\|Li 교정 셀에서 측정 → 이식) | **0 V = 도금 Li 상 정체** |
| 셀 안 측정 | 0 | 0(교정 셀) · A·1 순환 | **−618 mV vs In/InLi(측정 축)** |
| 표류 | 0 | **< 3 mV / 28 일** | **수 0**, "≥8 일" |
| 누설 | 0 | 간접 < 4.3 nA | 0 · `[재현]` 소진 가정 ≈39 nA |

- `[해석]` **"0 V ↔ 0.31 V" 두 관례는 이 편의 사다리 하나로 깔끔히 맞춰지지 않는다.** 박막 도금 Au(`[재현]` 3–5 wt% → ≈0.08–0.13 µm)는 µAh 급 전하로 AuLi₃ 를 넘어
  도금에 닿는다(이 편). 21호 GWRE 의 **0.31 V 는 이 편 사다리(0 · 0.134 · 0.215 V)의 어느 칸도 아니고**, 노출부 Li/Au ≈1.2 를 벌크 평형으로 읽으면 오히려
  AuLi/AuLi₃ 칸(0.134)이어야 한다 — 이완 경로(0 → 0.25 → 0.31 V) · SE 로의 Li 손실 · 문헌 평탄값 차 중 무엇인지는 두 지면으로 못 가린다. 공통 조상 후보 **Solchenbach 2016**
  (이 편 ref 20 = 큐 48)에서 확인할 것. 그리고 이 편의 "Au–Li 평탄은 SE 환원으로 불안정" 은 **박막 Au** 에서의 관찰이고, 21호(벌크 Au)는 0.31 V 에서 28 일 < 3 mV 였다 —
  **Au 재고 차이가 후보**다(가설).
- ⚠ 21호 digest 의 `[추론]` "**Schlenker 2020 → Hertle 2023 → 16호** 로 이어지는 **Marburg 계열** 금 도금 W 선" 은 이 편 지면에서 **지지되지 않는다** — 이 편은 **Giessen** 이고
  참고문헌 40 편에 **Schlenker 가 없다**. 이 편이 인용한 금선 선례는 **Solchenbach 2016**(ref 20, 액체, TUM — 큐 48) 하나다.
- ⇒ 계보: … → 공통 모드 표류 판독(43호) → GITT `ΔE_s` 안의 가정(44호) → **셀 안 도금 Li · 소모품 기준극(45호)**.
- **평탄 조건 목록에 붙일 것**(개념 페이지): (9) **도금형 기준극은 Li 층이 남아 있을 것** — 사다리 하한 도달 뒤의 여분 전하 ≥ 소비율 × 실험시간 × 10((5′) 의 기준극 판을
  Li 금속 기준극에 적용). 떨어지면 기준은 **연속이 아니라 칸 단위(+0.133 · ≈+0.215–0.25 V)** 로 옮겨 간다.

---

# 5. `[재현]` 16호 이식 — 계산

- 이 편: 와이어 옆면 π × 10 µm × 1 cm = 3.14 × 10⁻³ cm²(인쇄 A 와 일치) · 8 µAh → **2.55 mAh cm⁻²** · 도금분 7.57 µAh → Li 부피 3.67 × 10⁻⁶ cm³ → 평면 **11.7 µm** · 원통(r₀ = 5 µm) **6.9 µm** ↔ 인쇄 4.3 / 4 / 5 µm(D3).
- `Q_AuLi3`: W 와 Au 밀도가 같아(≈19.3) wt% ≈ vol% — ∅10 µm × 1 cm 에 3 / 5 / **7** wt% → **0.19 / 0.31 / 0.43 µAh** ⇒ 인쇄 0.43 은 **7 wt%** 에 해당(스펙 3–5 wt%, D4).
- 16호: ∅25 µm × ≈1.2 cm(CompreCell 12 지름 가정) → 면 9.4 × 10⁻³ cm² · 2.5 µAh → 0.27 mAh cm⁻² · Au 량 ∝ d²L(같은 Au 분율 **가정**): 3 / 5 / 7 wt% → AuLi₃ **1.4 / 2.3 / 3.2 µAh**
  ⇒ 여분 **+1.1 / +0.18 / −0.75 µAh** ⇒ 원통 Li **≤ 0.55 µm**(0.12 mAh cm⁻²) — 이 편의 **≤ 1/20**.
- 수명 척도: 이 편 소진 가정 소비 12.5 µA cm⁻² ⇒ 16호 여분 ≤ 0.12 mAh cm⁻² 는 **≤ ≈9 h**(SE 다름 — LPSClBr₀.₇ — 조건부).
- ⚠ 16호의 Au 분율 · 와이어 길이는 16호 digest 에 없다(가정). 결론의 방향(여분이 원전의 한 자릿수 이하)은 세 분율 모두에서 선다.

---

# 6. ★★★ 합 일치 검증의 판별력 — 셀 동정

| 그림 | 무엇 | 고주파 Re | 저주파 끝 Re | 셀 |
|---|---|---|---|---|
| Fig. 5 | "2E" 완전지 | **98 Ω cm²** | 165 Ω cm² | A |
| Fig. 11 · 12 | 양극 vs μ-RE | 45 Ω cm²(57 Ω) | 100 Ω cm²(0.1 Hz) | A |
| Fig. S7 | 음극 vs μ-RE | 51.5 Ω cm² | ≈65 Ω cm² | A |
| Fig. 10 | 2E ↔ 3E 합 | **≈62 Ω ≈ 48.7 Ω cm²** | ≈145 Ω ≈ 114 Ω cm² | **B** |

- `[재현]` **셀 A**: 양극 반쪽 + 음극 반쪽 = 45 + 51.5 = **96.5** ↔ Fig. 5 **98** · 저주파 100 + 65 = **165** ↔ **165** ✓ — Fig. 5 의 "2E" 는 **3E 셀 A 를 C–A 로 잰 것**(또는 합)이다.
  고주파 98 Ω cm² ↔ 200 mg · 완전 밀도 · 1.4 mS cm⁻¹ 최소 **97.5** ✓(3E 레시피) — 60 mg 2E 레시피면 ≥29. 분리막 몫 45 : 51.5 ↔ SE 질량 100 : 100(40호 새 줄 "3전극 옴 몫은
  기준극 위치가 정한다" 통과, 양극 반쪽에는 복합체 고주파 몫이 섞인다).
- `[재현]` **셀 B**(Fig. 10)는 A 가 아니다 — B 의 전체 고주파가 A 의 양극 반쪽 하나보다 겨우 크다(62 ↔ 57 Ω). 48.7 Ω cm² 는 **100 mg** 완전 밀도 최소(48.8)와 같은
  자리 — 어느 인쇄 레시피(60 · 200 mg)와도 안 맞는다(G7).
- ⇒ `[해석]` **검증(B)과 분석(A)이 다른 셀**이고, 둘 다 반쪽 · 전체를 **같은 셀에서** 잰 것으로 읽힌다 — 합 일치는 셀 안 항등식이다. 기준극 위치 artifact 는 합에서 사라지므로
  이 검증으로 **"두 반쪽의 분배가 맞다" 는 말할 수 없다.**
- ★ **호 #1**: 셀 A 양극 반쪽의 고주파 −Im ≈15 Ω cm²(100 kHz) — 셀 A 의 "2E"(Fig. 5) 고주파 첫 점 −Im ≈1.3 Ω cm², 음극 반쪽(S7) 고주파 −Im ≈0. 세 스펙트럼의
  주파수 끝점이 인쇄되지 않아 **같은 주파수에서 대조할 수는 없다** — 그러나 두 반쪽 중 하나에만 큰 호가 있고 합에는 안 보이면, 그것은 기준극 채널 쪽 후보다. 원문은 이 호를
  **"caused by the SE separator"** 로 물리 배정하고 TLM 적합의 첫 원소((R)(CPE))로 넣었다 — Fig. 5 회로(= SI Fig. S4 캡션)는 같은 셀 A 의 분리막을 **저항 하나**로 둔다.

---

# 7. ★★★ 2E 적합 비유일성 — 3E 반쪽이 파라미터는 고르고, 모델은 못 고른다

- 저자가 **인쇄로 인정한 비유일성**: 같은 회로 · 두 파라미터 집합 · "equally well". `R_Anode` ×3.6(14 ↔ 3.9) · `R_ion` ×1.39 · `α_diff` 0.45 ↔ 0.37.
- `[재현]` S7(같은 셀 A 의 음극 반쪽, 호 ≈12–13 Ω cm²)은 **Fit 1(14)과 맞고 Fit 2(3.9)를 배제**한다. 캡션이 S7 을 가리키지만 **어느 적합이 맞는지 본문은 말하지 않는다.**
- 3E 양극 반쪽: TLM(호 둘 + 확산) ↔ 직렬 R-CPE ×3 + CPE — **둘 다 데이터를 따라간다**(Fig. 11 (a) · (b) 적합선 모두 측정점 위, 잔차는 SI Fig. S5 — 교차참조 결손으로 어느 그림의 것인지 불명). 선택 기준은 `[인쇄]` "very depressed semicircles cannot be
  explained properly" · TLM 은 "directly yields physically meaningful parameters". ⇒ `[해석]` **3E 는 전극 간 분배의 비유일성을 풀고, 전극 안 모델 구조의 비유일성은 물리적
  타당성으로 고른다** — 그 선택의 폭(다른 TLM 변형 · 파라미터 상관)은 재지 않았다.
- Q4 **0/45 — 서른일곱 번째 성질 "두 적합 병치로 비유일성을 인쇄하고, 3전극에서는 '물리적 의미' 로 한 모델을 골랐다 — 어느 쪽에서도 폭을 재지 않았다"**. 반 칸 검토 후 접음:
  (i) 두 점 병치는 폭 · 프로파일이 아니다 (ii) 잔차 수가 지면에 없다(D8) (iii) 축이 전극 분배지 카드의 `LAM_PE` ↔ 접촉이 아니다.

---

# 8. ★★★ 율 시험 — 상대극 Li 소진이 2E 에서 양극 용량 손실로 보인다

- 사실(`[인쇄]` + `[도표]`): LTO 는 **빈 채로 조립**(Li 여분 0) → 충전 때 양극에서 받은 Li 로만 채워진다 → 부반응이 Li 를 먹으면 **방전 때 LTO 가 먼저 빈다**(≈160–165 mAh g⁻¹) →
  2E 는 그때 컷오프(165), 3E 는 양극 컷오프까지 계속(193).
- `[해석]` 카드 언어로: **2E 방전 용량 = Li 재고(`LLI` 로 줄어든) 한도**, 3E 방전 용량 = 양극 수용 한도. 2E 만 보면 0.1 C 방전 −15 %(193 → 165)가 **양극 쪽 용량 손실처럼**
  보이고, 원인은 **Li 를 먹는 부반응**(저자 문장)이다 — `LLI` → 겉보기 `LAM_PE`. 17호(Li-In 상대극) · 21호(NCM\|In, "cannot be assumed to stay invariant at 0.62 V") 와 같은 구조가
  **LTO 상대극**에서 선다. 칸은 안 움직인다 — 전극별 용량 귀속은 20 · 17 · 41호와 같은 층이고, 신품이다.
- ⚠ `[재현]` 3E 의 165 → 193 구간(≈28 mAh g⁻¹ × 7.58 mg ≈ **0.21 mAh**)은 음극이 **≈2.5 → 3.2 V vs Li** 로 끌려가는 동안 흐른 전하다. `[해석]` LTO 는 더 줄 Li 가 없으므로
  그 전하는 **음극 쪽 산화 부반응**(Li₆PS₅Cl 산화 · 탄소 계면 후보)이 공급했다 — "3E 방전 용량" 은 양극 성질로는 맞지만, 그 측정은 **음극을 산화 창으로 몰아넣는 프로토콜**이다.
  원문 언급 0.
- ★ 부수 사실 `[도표]`: **LTO 2상 평탄이 도금 Li 기준극 대비 1.55 V 안내선 위(±≈10 mV)** — R-LTO 가지(40 · 43호)의 1.55 V 가 **ASSB 안 Li 금속(도금) 대비**로 그려진 첫 그림이다.
  분해능은 **1.55 ↔ 1.57 을 못 가른다**(차 20 mV ≈ 선 두께 + 판독 오차). 원문은 "1.55 V vs Li⁺/Li in OCV" 를 **값으로만** 적고 개방회로 곡선을 보이지 않는다.

---

# 9. 우리 축 (Q1–Q8)

| | 판정 |
|---|---|
| **Q1 정량** | **없다 — `θ(N)` 0/45.** 신품 · `contact` 6 회 중 접촉 손실 0 · 사후 SEM 은 기준극 주변 균열 정성. 이동 없음 |
| **Q2 독립관측** | 반 칸 검토 후 접음 — ① 2E 적합 비유일성을 3E 반쪽(S7)이 가른다는 것은 **우리 판독**(저자 미판정) ② 상대극 Li 소진 → 2E 용량 귀속은 20 · 17 · 41호와 같은 층 ③ 열화 0 |
| **Q3 라벨층위** | 층 하나 — **in-cell plated reference: zero by phase identity, measured-axis difference printed, stability claimed by duration without trace** · 3E TLM 두 값 ± 0 · 율 시험 n 미기재 |
| **Q4 유일성** | **0/45 — 서른일곱 번째 성질**(§7). `identifiab` · `uncertaint` 0 · `ambigu*` 2 · `unequivoc*` 3 — 비유일성의 **낱말은 있고 양은 없다** |
| **Q5 Li-In** | **+0.5 — 스물한 번째 형태 "셀 안 도금 Li: 영점을 상 정체로 정하고, 기준극을 소모품으로 인쇄했다"**(§판정 (1) · §4). 누설 0/45 · 표류 수 0 · 618 mV 계보 첫 ASSB 안 인쇄 수 |
| **Q6 압력** | 제조 2E 382 MPa · 3E 40 → 374 MPa · **운전 63.7 MPa**(알루미늄 틀) 명시 · TSRE 는 "little to no pressure" → 성능 저하(정성). 스윕 0. 이동 없음 |
| **Q7 dead Li** | 해당 없음 |
| **Q8 화학 · OCP** | NCM851005(BASF) · OCP 0. 칸 밖: LTO 평탄 vs 도금 Li `[도표]` ≈1.55 V |

**누적**: ≈19.0 → **≈19.5 (Q5 +0.5)**.

---

# 10. ★★ 곱 축퇴 처방 — 스물여덟 번째 적용

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | 3E 양극 TLM: σ_ion(eff) · R_CT 두 값, `C`/CPE 미인쇄(Table S1 은 2E) · 한 상태 | ❌ |
| **2단계** 면적 대조군 | 없음 | ❌ |
| **3단계-a** `Ea` | 25 °C 한 점 | ❌ |
| **3단계-b** `C` 물리 상한 | ★ 호 #1("SE separator"): `[재현]` Fig. 12 −Im(100 kHz)/R ≈0.33 → ωτ ≈0.38 → τ ≈0.6 µs, R ≈57 Ω(양극 반쪽 고주파 Re 전부를 #1 로 둔 가정) ⇒ **C ≈10 nF** ↔ 분리막 반쪽(≈0.68 mm) 기하 용량 ≈10–100 pF(ε_r 10–100 가정) | ✅ **적용 — 배정 실패 ×100–1000**: 이 호는 SE 벌크의 기하 호가 아니다(입계 · 기준극 채널 후보). ⚠ R · ε_r · 호 모양 가정 |
| **4단계** 시간 영역 | LTO 1 C 과전압 ≈300 mV(1.83 mA cm⁻²) ↔ LTO 임피던스 미인쇄 · In/InLi: TSRE ±40 mV 는 다른 셀(무가압) | ❌ |

**새 줄 제안 — "합 일치는 분배를 검증하지 않는다: 반쪽 스펙트럼에만 있는 고주파 호는 3-b(`C` 상한)로 먼저 거른다"**: 3전극 반쪽의 합이 완전지와 맞아도 위치 artifact(재분배)는
상쇄돼 보이지 않는다. 반쪽 하나에만 있는 호는 `C` 를 분리막 기하 용량과 대고, 넘치면 물리 성분으로 적합하지 않는다. 40호 "3전극 옴 몫은 기준극 위치가 정한다"(분배의 크기) ·
41호 "배면형 기준극 → 상대극 채널"(분배의 극단)에 이은 **분배의 검증 불가성** 줄이다.
그리고 부수: **2E 적합 비유일성은 같은 셀 3E 반쪽이 고른다**(S7 → Fit 1) — 곱을 가르기 전에 **전극 간 분배부터** 3E 로 고정하는 순서가 처방의 전제다.

⇒ 이 적용이 곱을 푼 것은 아니다: 신품 · 한 상태 · `C` 미인쇄 · 열화 0. 기여는 **3전극 분배 자체의 검증 한계**와 **3-b 가 기준극 채널 artifact 의 거름망으로도 쓰인다**는 것.

---

# 11. `[재현]` 검산 장부

| # | 계산 | 결과 | 쓰임 |
|---|---|---|---|
| R1 | π × 10 µm × 1 cm | 3.14 × 10⁻³ cm² = 인쇄 A | 와이어 ≈1 cm |
| R2 | 1 µA / A · 8 µAh / A | 0.32 mA cm⁻² · 2.55 mAh cm⁻² | §판정 (2) |
| R3 | 7.57 µAh Li → 부피(13.0 cm³ mol⁻¹) | 평면 11.7 · 원통 6.9 µm ↔ 인쇄 4.3/4/5 | D3 |
| R4 | Au 3/5/7 wt% × ∅10 µm × 1 cm → AuLi₃ | 0.19 / 0.31 / 0.43 µAh | D4 |
| R5 | 7.57 µAh / 192 h | ≈39 nA · 12.5 µA cm⁻² | 소비율(소진 가정) |
| R6 | (5′) ≥ 10 | ≤ ≈19 h | 새로고침 주기 |
| R7 | Fig. 7 사다리 | −0.485 ↔ −0.618 ⇒ 0.133 V ↔ 134 mV | 상 정체 |
| R8 | 16호 ∅25 × 1.2 cm, 2.5 µAh | 면적당 0.27 mAh cm⁻² · 여분 ≤1.1 µAh · Li ≤0.55 µm · ≤ ≈9 h | §5 |
| R9 | SE 1.865 g cm⁻³ · 0.785 cm² | 60 mg 410 µm/29 Ω cm² · 100 mg 683 µm/48.8 · 200 mg 1.37 mm/97.5 | §6 · D11 · D12 |
| R10 | 셀 A 반쪽 합 | 45 + 51.5 = 96.5 ↔ 98 · 100 + 65 = 165 ↔ 165 | Fig. 5 = 셀 A |
| R11 | Chang 띠 1.39 mm × ⌀14 mm | ≈12.6 % ↔ 인쇄 1.26 % | D5 |
| R12 | 1.44 mA / 190 mA g⁻¹ | NCM 7.58 mg = 63 wt% · 1.83 mA cm⁻² · ≈1.44 mAh | G9 |
| R13 | In/InLi Li 비 | 19 at%(100 µm) / 32 at%(200 µm) · 국소 Li/In ≈1.2 | 42호 창 안 |
| R14 | 1 C 비 | 충전 1.32 · 방전 1.51 · 0.1 C 방전 1.17 | "33 %" = 충전 |
| R15 | 165 → 193 × 7.58 mg | ≈0.21 mAh | §8 음극 산화 전하 |
| R16 | 호 #1 τ · C | 0.6 µs · ≈10 nF ↔ 10–100 pF | §10 3-b |

---

# 12. 어긋남 (실제로 어긋난 것만)

| # | 어긋남 | 근거 |
|---|---|---|
| **D1** | 0.1 C 방전 "193 mAh g⁻¹, and 165 mAh g⁻¹, respectively"(2E, 3E 순) ↔ Fig. 13b **2E × ≈165 · 3E ◇ ≈193** · 다음 문장도 "why the discharge capacity is so much lower compared to the 3E setup" | 순서 반대 |
| **D2** | LTO 2E 컷오프: 실험 절 **0.95 V** ↔ 결과 절 "0.9 V corresponding to … 2.45 V" ↔ Fig. 4 곡선 끝 ≈0.95 V ↔ 율 시험 "1.35 V and **2.9 V**"(상한은 4.3 − 1.55 = 2.75 이어야) · 3E 하한 "2.5 V vs Li"(실험 절) ↔ "2.9 V"(율 시험) | 세 값 |
| **D3** | 도금 Li 두께 **4.3 µm**(p4) · **4 µm**(p6) · **5 µm**(p6) ↔ `[재현]` 6.9(원통)–11.7(평면) µm | 인쇄 셋 · 계산과 ×1.4–2.7 |
| **D4** | `Q_AuLi3` 0.43 µAh ↔ `[재현]` 3–5 wt% 에서 0.19–0.31 µAh(0.43 = 7 wt%) | 스펙과 불일치 |
| **D5** | Chang 띠 "≈1.3 %"/"1.26 %" ↔ `[재현]` ≈12.6 % | ×10 |
| **D6** | Table S1 Fit 1(`R_Anode` 14)/Fit 2(3.9) ↔ Fig. 5 (a) 작은 음극 호 · (b) 큰 음극 호 | 순서 엇갈림(우리 판독) |
| **D7** | Table S1 단위: `R_ion` 9.07/12.6 × 10³ "Ωcm²" ↔ Fig. 5 양극 호 전체 ≈40–47 Ω cm² · `α_CAM` "(Ωcm2)" · `Q` "(Ωsα)" · `Q_diff` 9.07 = `R_ion` 가수 9.07 | 단위 · 값 |
| **D8** | "These parameters [TLM] can be found in Table S1" · "exact fit values and residuals … are given in Table SI" ↔ Table S1 = 2E 두 적합 · 잔차 없음 | 가리킨 곳에 없다 |
| **D9** | SI Fig. S5 캡션 "below 5 % for −Im(Z)" ↔ 그림 최대 ≈7 % · SI 교차참조 결손 **5 곳**("Error! Reference source not found.") · S7 캡션 문장 결손 | SI 원고 상태 |
| **D10** | 방법 "300 kHz to 100 mHz" ↔ Fig. 10 저주파 끝 `[도표]` ≈0.05 Hz | 범위 |
| **D11** | 3E "geometry is essentially unchanged compared to the 2E setup" ↔ SE 60 → 200 mg(분리막 ×3.3) · 예압 382 → 40 MPa · 최종 382 → 374 MPa | 기하 · 공정 |
| **D12** | 검증 셀(Fig. 10, ≈48.7 Ω cm²) ↔ 분석 셀(Fig. 5 · 11 · S7, ≈97 Ω cm²) | 다른 셀, 레시피 미상 |
| **D13** | Fig. 3b TSRE "In/InLi" ↔ 조립 문단 In 박만 | 리튬화 절차 부재 |
| **D14** | Fig. 7 캡션 "Au/AuLi and **Au/AuLi₃** two-phase systems"(→ AuLi/AuLi₃) · 본문 ∅10 µm 첫 평탄 "barely visible" ↔ 두 패널 모두 뚜렷 · 패널별 직경 · 전류 미인쇄 | 캡션 |
| **D15** | 비리튬화 환산 1.73 ↔ 1.11(차 0.62) · 2.13 ↔ 1.50(차 0.63) ↔ In/InLi "618 mV" | 환산 상수 셋 |
| **D16** | "we are aware of only two examples and in only of these impedance data were shown" — 문장 결손 · 인용은 [28,30] 둘인데 앞 문장 분류는 [29] 포함 셋 | 서론 |
| **D17** | Fig. 4(2E LTO) 0.1 C ≈205/161 · 1 C ≈108/103 ↔ Fig. 13 2E 197/165 · 112/97 | 2E 셀 둘 이상(또는 다른 사이클), 미인쇄 |
| **D18** | "Their combination agrees perfectly" · "highly reliable" ↔ 자기 잔차 Im ≈4–8 %(>30 kHz) · Fig. 12 Im ±6.5 % | 수사 |
| **D19** | Li 박 "∼200 μm"(재료 절, 5 mg 압착) ↔ "∼100 μm"(셀 조립) | 두께 |

---

# 13. 그림 — 무엇을 봤나

크로퍼 **21 장**(본문 그림 13 + SI 그림 7 + 표 1). **그림 20 장 중 15 장 봤다**: Fig. 1 · 3 · 4 · 5 · 6 · **7(화소 판독 — 위 · 아래 패널)** · 8 · 9 · **10(주파수 범위 화소 판독)** · 11 · 12 ·
**13(아래 패널 확대 판독)** · S1 · S5 · S7. **안 본 것 5 장**: Fig. 2(셀 하우징 사진) · S2(EDS) · S3(0.2 · 0.5 C 곡선) · S4(회로 — 캡션과 Fig. 5 회로로 대신) · S6(TSRE 배선).
표 1 장(`tab_S1.png`)은 이미지로 안 읽고 PDF 텍스트로.
본문 서술과 어긋난 그림: **Fig. 13**(D1 방전 순서) · **4**(D2 0.95 V) · **1**(D5 Chang 1.3 %) · **5**(D6 적합 순서) · **7**(D14 첫 평탄 · 패널 미상) · **10**(D10 · D12 다른 셀) ·
**S5**(D9 7 %) · **11**(호 #1 배정 ↔ S4 저항). 판독값은 전부 `[도표]`/`figure-read ≈` — Fig. 7 화소 판독 ±≈2 mV(눈금 재현 검증), Fig. 13 V–Q 끝점 ±≈3 mAh g⁻¹, Nyquist ±≈1 Ω cm².

---

# 14. 참고문헌 중 후속 후보 (40 편 중 — 미열람, 서지는 지면 그대로)

| 순위 | ref | 왜 |
|---|---|---|
| ★★★ | **[20] Solchenbach, Pritzl, Kong, Landesfeind, Gasteiger, *JES* 163 (2016) A2265** | **큐 48** — 이 편이 인용한 유일한 금선 선례(액체) + Au–Li 평탄 134/215 mV 출처 중 하나. 21호 GWRE 0.31 V 관례와 이 편 0 V 관례의 **공통 조상** 후보 |
| ★★★ | **[33] Bach, Stratmann, Valencia-Jaime, Romero, Renner, *Electrochim. Acta* 164 (2015) 81** | Au–Li 상 평탄 전위의 측정 원전 — 134 mV(사다리 교차 검사의 기준)를 무엇 대비로 쟀나 |
| ★★ | [38] Braun, Uhlmann, Weiss, Weber, Ivers-Tiffée, *JPS* 393 (2018) 119 | TLM 에서 σ_eff · R_CT 를 뽑는 식 — 1단계 입력 형식 |
| ★★ | [19] Klink, Madej, Ventosa, Lindner, Schuhmann, La Mantia, *Electrochem. Commun.* 22 (2012) 120 | 3전극 임피던스 artifact(액체) — >10 kHz 편차 · 호 #1 원인 후보 |
| ★ | [34] Dey, *JES* 118 (1971) 1547 · [35] Pelton, *Bull. Alloy Phase Diagrams* 7 (1986) 228 | Li–Au 합금화 · 상도 |
| ★ | [27] Rosenkranz, Janek, *SSI* 82 (1995) 95 | 같은 연구실의 고체 기준극 선행 |
| — | [13] Conforto … Janek 2021 *JES* 168, 070546 = **38호** · [28] = **40호** · [29] = **41호** · [30] = **20호** | 이미 흡수 |

큐 47–59 인용: **48(Solchenbach 2016) 하나**. ⚠ 47 **Schlenker 2020 은 인용 0**(21호의 "Schlenker → Hertle" 계보 추론과 어긋남) · 55 Neumann 2021 아님(ref 6 은 Neumann 2020 *ACS AMI* 12, 9277 — 다른 편).

---

# 15. 우리 프로젝트와의 접점

- `degradation-degeneracy/` 의 물음(완전지 곡선에서 `LLI` ↔ `LAM` 가 한 조합으로 보이는가)에 이 편이 주는 것은 두 가지다 — ① **기준 이동이 계단형**(도금 Li 소진 → +0.133 V)이라
  3전극 분해 자체가 **일정 오프셋 오염**을 받을 수 있다; ② **2E 방전 용량이 상대극 Li 재고에서 끊긴 실례**(0.1 C 165 ↔ 193). 우리 수치는 `degradation-degeneracy/docs/RESULTS*.md` 가
  정본이고 여기서는 비교하지 않는다(다른 화학 · 신품 · n 미기재).

---

# 16. 이 digest 가 주장하지 않는 것

- **μ-RE 가 0 V 가 아니었다고 주장하지 않는다.** 사다리 교차 검사(0.133 ↔ 0.134 V)는 오히려 도금 Li 를 지지한다 — 다만 **그 검사는 우리 판독**이고, 저자는 그렇게 논증하지 않았다.
- **16호 0.11 V 가 AuLi/AuLi₃ 칸이라고 결론 내리지 않는다** — 후보다. 16호 와이어의 Au 분율 · 길이 · 측정 시점 · SE 가 다르고, 다른 셀(0.58 V)은 칸에 안 맞는다.
- **호 #1 이 기준극 artifact 라고 단정하지 않는다** — `C` 상한 위반(ε_r · R 가정)과 반쪽 하나에만 있다는 정황까지다. 입계 호일 수도 있다.
- **Fig. 10 이 같은 셀이라고 단정하지 않는다** — 지면은 말하지 않는다. 다른 두 셀이 전 대역 <1 % 로 겹칠 가능성이 낮다는 판단이다.
- **3E 의 193 mAh g⁻¹ 이 틀렸다고 하지 않는다** — 양극은 그만큼 받았다. 165 너머 전하의 Li 원천이 음극 쪽 산화라는 것은 LTO 에 Li 가 없다는 저자 문장에서 온 `[해석]` 이다.
- **소비율 ≈39 nA 를 측정값으로 쓰지 않는다** — "8 일 = Li 소진" 가정 위의 평균이다.

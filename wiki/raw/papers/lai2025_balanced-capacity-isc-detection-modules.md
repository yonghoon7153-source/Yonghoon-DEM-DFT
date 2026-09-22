---
title: "Lai, Ke, Tang, Zheng 2025 — Balanced capacity-based quantitative method for detecting internal short circuits in Lithium-ion battery modules (J. Energy Storage 123, 116622)"
source_url: local-upload/39._Balanced_capacity-based_quantitative_method_for_detecting_internal_short_circuits_in_Lithium-ion_battery_modules.pdf
source_dataset_url: https://github.com/xtangai/EST-D-24-12331
source_url_note: "본문 9 쪽, SI 없음. 큐 39번. ⚠ assb 가 아니다 — 액체셀 6S2P 18650 모듈의 ISC 검출·정량. `pack-fault` 섹션 1호. 데이터셋 조사(논문 없이 먼저 한 것)는 bms-balancing/docs/ISC_LEAKAGE_DATASET.md. 크로퍼 15 장(Fig. 1-8 + Table 1-7), Fig. A.1/A.2 누락 → p.7 렌더로 읽음."
source_doi: 10.1016/j.est.2025.116622
source_license: "(c) 2025 Elsevier Ltd. All rights are reserved (open access 아님)"
pdf_sha256: aef3b36ad07da00265a761de4e3f5bec18a5b088876ac0ce1d26c0e8770cb760
ingested: 2026-09-22
sha256: b813e4a2fb79baaa52d7ce62d886ff7c89e5d1cde5614c3133c4fde02ff5c701
---

# 수집 목적

**Xin Lai ᵃ**, **Yuehang Ke ᵃ**, **Xiaopeng Tang ᵇ,\*** (교신, `xiaopengtang@ln.edu.hk`,
`xtangai@connect.ust.hk`), **Yuejiu Zheng ᵃ** — 소속 [a] School of Mechanical
Engineering, **University of Shanghai for Science and Technology**, Shanghai 200093 ·
[b] Science Unit, **Lingnan University**, Tuen Mun, Hong Kong.

**"Balanced capacity-based quantitative method for detecting internal short circuits
in Lithium-ion battery modules"**, *Journal of Energy Storage* **123** (2025) 116622,
doi `10.1016/j.est.2025.116622`. `[인쇄]` Received 23 November 2024; revised 24 March
2025; accepted 7 April 2025; available online 23 April 2025. `[인쇄]` "2352-152X/©
2025 Elsevier Ltd. All rights are reserved" (open access 아니다).
`[인쇄]` Funding: NSFC **52277223 · 51977131**, Lingnan University **SUFRG2501 ·
DR25F1**, Shanghai Pujiang Programme **23PJD062**. 경쟁 이해 없음 선언.
★ `[인쇄]` Dataset link / Data availability: **`https://github.com/xtangai/EST-D-24-12331`**
— 교신저자 `xtangai` = Xiaopeng Tang. **우리가 논문 없이 먼저 조사한 그 저장소다**
(`bms-balancing/docs/ISC_LEAKAGE_DATASET.md`).

⚠ **이 논문은 `assb` 가 아니다.** 액체셀 **6S2P 18650 모듈**의 **내부단락(ISC) 검출·정량**
논문이고, 이 위키에서는 **`pack-fault` 섹션의 1호**다 (닻:
`wiki/questions/isc-detection-vs-balancing-masking.md`). 열화 모드(LLI/LAM) 지분과는
**물리량이 다르다** — 겹치는 것은 **문제의 모양**(두 원인 → 같은 관측, 그 위에 조작이
겹침)이다. 이 구분은 §8 에서 다시 적는다.

본문 **9 쪽** (SI 없음) 전문의 절별 해체분석. 7 개 물음(`ISC_LEAKAGE_DATASET.md` §5)에
대한 답은 **§4** 에 모아 두었다.

> ⚠ **이 digest 의 표기 4분**: `[인쇄]` = 지면에 문자 그대로 있는 것.
> `[도표]` = 그림을 실제로 열어 눈으로 읽은 것(판독 오차를 같이 적는다).
> `[재현]` = 원문의 값 **또는 공개 데이터셋**으로 우리가 계산한 것.
> `[해석]` = 우리가 추론한 것. **`[재현]`·`[해석]` 은 원문에 없다.**

★ **크로핑 결과와 실제로 본 것**:
- `wiki/tools/extract_figures.py` → **15 장** = Fig. 1–8 (8) + Table 1–7 (7).
- ⚠ **누락 2 장**: 논문의 도표는 **Fig. 1–8 + Fig. A.1 + Fig. A.2 + Table 1–7 = 17 항목**
  이다. 부록 그림 **Fig. A.1(IC 특징) · Fig. A.2(수동 균등화 중 셀 충전 전류)** 를
  크로퍼가 놓쳤다 (`Fig. A.` 캡션 패턴). **p.7 전체를 110 dpi 로 렌더해 눈으로 읽었다**
  (`scratchpad/p39/pages/p07.png`, 저장소 밖). 크롭으로는 등록하지 않았다.
- **실제로 열어 본 것: Fig. 1 · 2 · 3 · 4 · 5 · 6 · 7 · 8 (8/8 전부) + Fig. A.1 · A.2
  (페이지 렌더)**. Table 1–7 은 이미지로 읽지 않았다 (PDF 텍스트가 정확 — §2 에 전문 전사).
- ⚠ **Fig. 5(a) 크롭은 왼쪽 y 축 눈금 라벨이 잘려 있다** (`0 · 3 · 6 · 9 · 2` 만 보임
  — (b) 와 같은 `0 / −0.3 / −0.6 / −0.9 / −1.2` 로 읽었다). (a) 의 절대값은 판독 오차가
  크다고 표시한다.
- **µ 폰트 확인**: 본문·표·결론의 단위는 텍스트 추출에서 전부 `mA` 로 나오고, p.7 렌더의
  결론 문단에서도 `±1 mA` 로 보인다. **µA 탈락은 없다.** 균등화 전류는 **A 급**(수동
  `2.5 Ω` 저항 → ≈1.5 A, 능동 `≈2.7 A`), 누설 전류는 **mA 급**(11–66 mA)이다.
- ★ **공개 데이터셋과의 대조**(`[재현]`): `55_passive.xlsx` · `55_active.xlsx` 두 파일만
  openpyxl read_only 로 전수 스트리밍했다 (각 ≈15 s). 다른 7 개는 열지 않았다.

---

# 0. 원문에 없어서 확인이 필요한 것 (먼저 적는다)

| # | 공백 | 왜 걸리는가 |
|---|---|---|
| **G1** | ★★★ **불확실성·유일성 어휘가 전수 0 이다.** `identifiab*` **0** · `uniqu*` **0** · `confidence interval` **0** · `uncertaint*` **0** · `error bar` **0** · `standard deviation` **0** · `replicat*` **0** · `condition number` **0** · `Fisher` **0** · `regulariz*` **0** (9 쪽 전수, 이 digest 가 다시 셌다 — `ASSB_TRANSFER_NOTE.md` §6-3-f 의 예비 집계와 일치). **조건당 실행 1 회, 반복 0, 오차 막대 0.** | 제목이 "quantitative" 인데 **정량값의 폭이 없다.** 유일한 대체물은 §3.3 의 **SoH 하나를 흔든 1변수 민감도**(Fig. 6–8)이고, 그것은 불확실성 정량이 아니다 (§5) |
| **G2** | ★★★ **자기방전 산포와 ISC 누설을 가르지 않는다 — 가를 수 없다고 적지도 않는다.** `self-discharge` 는 **2 회**뿐이고 둘 다 서론에서 **타 방법(Sazhin [22])을 설명**하는 자리다. 식 (3) 에는 `I_pack + I_bal + I_leak` 세 항만 있고 자기방전 항이 없다 | `[인쇄]` 각주 2 "The proposed method focuses on the detection of battery **current leakage**, rather than the internal change of the battery characteristics" → **방법의 출력은 "한 셀의 초과 누설 전류" 이고, 그것이 ISC 인지 자기방전 편차인지는 정의상 묻지 않는다.** 닻 카드의 첫 물음이 바로 여기에 걸린다 |
| **G3** | ★★ **기준 누설 전류가 측정값이 아니라 계산값이다** — `[인쇄]` "The referenced leakage current can be obtained by **dividing the average battery voltage by the short-circuit resistance**". 병렬 저항의 **허용오차·실측값이 없다** (`accurate` 라는 형용사만). 어느 전압(단자? 평균 구간?)으로 나눴는지도 없다 | 라벨 층위가 **designed-R → derived-I** 다. Table 3/4 의 "Ref." 열은 **측정된 진실이 아니라 옴의 법칙**이다 (§4-7) |
| **G4** | ★★ **추정 SoH 로 돌린 결과가 Test 5 하나뿐이다** (Table 6: 수동 1 · 능동 1 = **2 개 숫자**). Tests 1–4 는 **참 SoH(Table 2)를 넣고** 돌렸다 (Table 3/4). Fig. 7 은 Tests 1–4 가 SoH 2 % 오차에 **100 % 이상** 튄다고 보이는데, **그 조건에서 추정 SoH 를 넣은 표가 없다** | 초록·결론의 "±1 mA regardless of active/passive" 는 **참 SoH 5 조건 + 추정 SoH 1 조건**의 합이다. ⚠ 그리고 그 추정-SoH 수동 1 개가 **공개 데이터에서 깨진 파일**(`165_passive`)에 해당한다 (§4-4) |
| **G5** | **ISC 셀 `l` 을 어떻게 고르는지 식으로 적지 않는다.** 식 (12) 에 `SoH_l` 이 곱해지는데 `l` 의 결정 규칙은 없다. `[인쇄]` "the internally short-circuited cell can be identified" 라고만 | `[해석]` 정규화 균등화 용량의 **최소 셀 = l** 로 읽히지만 명시가 없다. 두 셀이 비슷하면 어느 쪽인지, 그 오분류가 `i_L` 에 어떻게 전파되는지 없다 |
| **G6** | **Table 2 의 용량(SoH 기준값)을 어떻게 재었는지 없다** — 율·온도·컷오프·회수 전부 없음. 2P 각 셀 값(`4.197 = 2.091 + 2.106`)까지 적었는데 프로토콜이 없다 | 이 방법의 **가장 민감한 입력**(§3.3)의 기준값이 무방법이다 |
| **G7** | **"10 mV ≈ SoC 1 %" 의 근거가 없다** (`[인쇄]` "corresponding to a SoC difference of about 1%"). 어느 SoC 구간의 OCV 기울기인지 없다 | 이 환산이 §3.4 의 **검출 시간 하한**(10 mA → 5 h)과 §4-6 의 dead-band 논의를 전부 떠받친다 |
| **G8** | **Test 5 의 프로토콜이 그림으로만 있다.** 충전 C-rate·컷오프·FUDS 스케일·사이클 수가 본문에 없다. 수동 Test 5 의 길이도 본문에 없다 (`[도표]` ≈720 min) | `165` 조건이 왜 긴가(§4-4)는 그림으로만 답할 수 있다 |
| **G9** | **능동 균등화의 환류 경로가 셀 단위로 어떻게 배분되는지 없다** — `[인쇄]` "fed back to the entire battery pack via a DC–DC converter", 효율 70 % | `[재현]` 데이터가 답을 준다: **환류 전류(열 13)가 6 셀에 동일**하게 0.714 Ah 씩 들어간다 (§4-6). 논문에는 없는 정보 |
| **G10** | **데이터셋의 열 정의가 논문에 없다** (README 에만, 16 열) — 그리고 README 가 적지 않은 **17 번째 열**을 논문도 언급하지 않는다 | §4-3 |
| **G11** | **Appendix B 의 SoH 추정기 계수 단위가 맞지 않는다** — `[인쇄]` "when setting the unit of SoH as % and the unit of `s` as V, we have `a = 3.01` and `b = −0.10`" (식 B.2 `SoH = a·s + b`). `[도표]` Fig. A.1 의 `s`(두 번째 골 ≈3.85 V ↔ 세 번째 봉우리 ≈3.95 V) 는 **≈0.1 V** → `SoH = 3.01×0.1 − 0.10 ≈ 0.2 (%)`. SoH 를 분율로 읽어도 `s ≈ 0.33 V` 가 필요하다 | `[해석]` 단위 오기(`s` 가 mV 이거나 SoH 가 분율)로 보이나 **본문으로는 복원 불가.** Table 5 의 추정 SoH 는 이 식의 산물이다 |
| **G12** | **셀 화학을 캡션이 "NCM" 이라 적고 근거가 없다** (Fig. 1 캡션 `[인쇄]` "NCM battery pack (6S2P)", 본문에 `NCM` 1 회 · `NCA` 0 회). 셀 모델은 `[인쇄]` "SONY US18650VTC5" | 화학은 이 논문의 결론에 중요하지 않지만 (전압 기반 균등화가 되는 기울기 있는 화학이면 됨), **LFP 는 안 된다**고 결론이 스스로 적는다 (`[인쇄]` future work (3)) |

---

# 1. 한 문장 요약과 주장의 구조

> `[인쇄]` "By calculating the **theoretical balanced capacity** of each cell in the
> absence of an internal short circuit and comparing it with the **actual balanced
> capacity measured by the balancing system**, the internally short-circuited cell can
> be identified, and the internal short-circuit resistance can be determined."

`[해석]` 논리 사슬은 셋이다:
① **균등화가 제대로 되면 모든 셀의 ΔSoC 가 같다** (식 5–6) →
② 그러므로 **`(균등화 전하 + 팩 전하)/(Q_nom·SoH)` 가 모든 셀에서 같아야 한다** (식 8) →
③ 한 셀에서 이 정규화 값이 **작으면** 그 차이가 누설 전류다 (식 11–12).
즉 **균등화기가 셀에 실어 보낸 전하가 곧 센서 판독값**이다 — `[인쇄]` "convert battery
equalizers into the equivalent current sensor". 균등화가 관측을 **덮는** 것이 아니라
**관측 그 자체**라는 입장이다. 그러면 "덮는" 자리는 어디로 가는가 — **SoH 오차**(§3.3),
**dead-band**(§3.4), **전압≠SoC**(§3.4) 다. §6 에서 다룬다.

**세 가지 기여 주장** (`[인쇄]`, §1 끝):
- "quantitatively detect the ISC faults … typical estimation error of the leakage current
  caused by ISC is only **±1 mA**"
- "does **not rely on specific battery's load profiles**"
- "applicable in **both active and passive** equalization scenarios"

⚠ 두 번째 주장은 §3.4 가 스스로 좁힌다 — `[인쇄]` "it is **recommended** that the ISC
detection should be implemented with a **longer profile (e.g., > 10 h)**" 그리고 `[인쇄]`
"In the best case when the SoC change … is **approaching zero**". `[해석]` 프로토콜 무관이
아니라 **"어떤 프로토콜에서도 식은 성립하되, 정밀도는 프로토콜 함수"** 다 (§7 D3).

---

# 2. 절별 해체

## 2.1 서론 — ISC 검출의 3 분류와 자기 계보

`[인쇄]` 세 분류: **model-based · sensor-based · equalization(balancing)-based**. Table 1
(전문 전사):

| Method | Advantages | Disadvantages |
|---|---|---|
| Model-based | Applicable to various battery types; No reliance on additional hardware | Difficult to update model parameters under complex conditions; High detection errors |
| Sensor-based | High accuracy; Capable of capturing multi-dimensional signals (e.g., temperature, pressure) | High dependency on sensor precision; Costly and impractical for large-scale applications |
| Balancing-based | No additional hardware cost (use existing balancing systems); Effective for managing cell inconsistency | **Sensitivity to load profiles** (e.g., limited to specific charge/discharge curves) |

★ **자기 계보의 두 선행**이 이 논문이 넘으려는 벽이다:
- `[인쇄]` Ref. [15] (Lai 2023, *JPS* 573, 233109): "leakage current detection accuracy of
  **±1 mA**, but the method is only suitable for **float-charging** conditions"
- `[인쇄]` Ref. [27] (Tang 2023, *CEJ* 476, 146467): "accuracy of **2 %** … detection of
  internal-short-circuit **resistance**, but … only suitable for **'round-trip' profiles**,
  where the starting and terminating SoC … should be exactly the same"
- `[인쇄]` "Compared with the traditional sensor-based methods, our balancing-based methods
  are **less robust to general dynamic load profiles**."

`[해석]` 그러므로 이 논문의 **진짜 델타는 정밀도가 아니라 프로토콜 일반성**이다 — Table 7
이 그것을 정직하게 보인다 ([15] `<1 mA` ↔ 제안 `Typ. 1 mA`, §2.8).

경쟁 방법 중 우리 물음에 직접 걸리는 언급 둘:
- `[인쇄]` Song et al. [23]: "estimated the amount of retained charge … taking into account
  … **battery pack inconsistency** … However, this method still does not take into account
  the effects of **battery aging**."
- `[인쇄]` Table 7 의 Kong [39] (remaining charging capacity): Weakness "**Sensitive to
  balancing**" — ★ **균등화가 ISC 관측을 덮는다는 진술을, 경쟁 방법의 약점으로 인쇄한
  유일한 자리**다.

## 2.2 방법 §2.1 — 정의 (식 1–5)

- 식 (1) `SoH_j = Q_j / Q_nom` · 식 (2) `SoC_{j,k} = Q_{j,k} / (Q_nom · SoH_j)`
- 식 (3) `Q_{j,k} = Q_{j,0} + Σ_κ (I_pack_κ + I_bal_{j,κ} + I_leak_{j,κ}) · ΔT`
  — `[인쇄]` 부호 규약 "all currents **charging** the battery as **positive**, … discharging …
  **negative**". ★ 자기방전 항 없음 (G2).
- 식 (4) 수동 균등화 전류 `I_bal_{j,k} = V_{j,k} / R_bal` — ⚠ **균등화 전류도 측정이 아니라
  전압/저항 계산**이다. 능동은 `[인쇄]` "a typical balancing current is commonly available".
- 식 (5) `SoC_{1,k} = SoC_{2,k} = ⋯ = SoC_{n,k}` — **균등화의 정의**이자 방법의 **가정**.
  `[해석]` 실제 하드웨어는 10 mV dead-band 로 동작하므로 (Appendix A) 이 등식은 **±1 % SoC
  안에서만** 성립한다 (G7).

## 2.3 방법 §2.2 — ISC 전류 계산 (식 6–12)

- 식 (6)–(8): ISC 없으면 `Σ(I_bal_j + I_pack)/SoH_j` 가 모든 `j` 에 대해 동일.
- 식 (9a) `I_leak_j ∈ {0, i_L}`, (9b) `Σ_j I_leak_j = i_L` — `[인쇄]` "we assume that there
  is **only one battery** suffering from ISC in the pack with a **relatively stable** leakage
  current". 각주 1 `[인쇄]` "Here we assume the leakage current is **time-invariant**."
- 식 (10) 비용함수 `J = Σ_{j1,j2} |ΔSoC_{j1} − ΔSoC_{j2}|` — **쌍별 절댓값 합**.
- 식 (11): 정상 셀 `j` 와 ISC 셀 `l` 의 정규화 합 등식. `[인쇄]` "the leakage current is
  always discharging the battery and is therefore negative, the relationship
  `Σ(...)/SoH_j > Σ(...)/SoH_l` holds for all normal battery `j`".
- ★ 식 (12) — **닫힌 형태 "quick solution"**:

```
i_L = SoH_l · [ max_j( Σ_k (I_bal_{j,k}+I_pack_k) / SoH_j ) − min_j( Σ_k (I_bal_{j,k}+I_pack_k) / SoH_j ) ] / (k2 − k1)
```

`[인쇄]` "Eq. (12) implies that the difference in normalized balancing capacity is
introduced by the ISC leakage current. … the determination of the leakage current
**requires the information of battery SoH**."

`[해석]` 유일성 구조를 여기서 읽어 둔다 (§5 에서 다시):
(i) `J` 를 실제로 최소화하지 않고 **`max − min` 으로 대체**한다. `n = 6` 이면 `J` 는 15 쌍의
합인데 (12) 는 그중 **한 쌍**(최대·최소)만 쓴다. 두 값이 같은 최소화자를 준다는 증명은 없다.
(ii) `l` 은 암묵적으로 **min 셀**이다 (G5).
(iii) **SoH 6 개는 입력이다** — 추정치가 아니라 주어진 것. 이것이 §3.3 의 민감도 분석이
필요해진 이유이고, **동시에 이 논문의 유일한 "폭" 측정이다.**
(iv) 식 (12) 는 **max 셀과 min 셀이 바뀌는 지점에서 미분 불연속**이다 → `[도표]` Fig. 6–8
의 **꺾인 V 자**가 그 흔적이다 (§3).

## 2.4 실험 §3.1 — 플랫폼

`[인쇄]` **12 × SONY US18650VTC5**, **6S2P** (2P 를 먼저 묶고 6 직렬; 2P 한 쌍을 하나의
battery unit 으로 취급). **25 ± 2 °C** (에어컨). **공칭 2.5 Ah** (→ 단위 5 Ah). Yishengda®
**100 V / 20 A** 테스터. BMS 가 전압 취득 + 균등화 제어. **능동 균등화 에너지 효율 70 %.**
`[인쇄]` "More information … in our previous work Ref. [30]" (Tang 2021, *iScience*).

`[도표]` Fig. 1: (a) 캐비닛형 테스터(`EST-B100V/20A-12CH` 라벨) + PC; (b) BMS 보드(릴레이
열 + 스크류 터미널 + 붉은 전압 선 6+); (c) 토폴로지 — `I_pack` 이 `SW1` 을 지나 팩으로,
셀 탭들이 **Switch Array** 를 통해 **Equalizer** 로, **MCU** 가 Switch Array·Equalizer 를,
**Sensing** 이 전압 `v` 를 MCU 로, `SW2` 가 음극 쪽; (d) 녹색 18650 12 개가 3 열 × 2 단 홀더에
(6S2P); (e) 수동 균등화 보드(저항 배열 격자); (f) 능동 균등화 보드(`BAT−`/`BAT+` 표기,
DC–DC 모듈). ⚠ **사진 어디에도 셀 #1 에 병렬 저항이 달린 모습이 보이지 않는다** — 설명이
본문에만 있다.

## 2.5 실험 §3.2 — 주 결과 (Table 2·3·4, Fig. 2–5)

`[인쇄]` "we design **5 tests** for the cases of using passive and active balancing,
respectively. … Tests 1–4 used short-circuit resistances of **55 Ω, 110 Ω, 220 Ω, and
330 Ω**, respectively. The test conditions employed the **full FUDS discharge profile** …
Test 5 used a short-circuit resistance of **165 Ω**, with Fig. 2(c) conditions applied for
the active balancing scenario and Fig. 2(d) conditions for the passive balancing scenario."

★ `[인쇄]` "In each test, **the weakest battery, say, #1, is paralleled with an accurate
external short circuit resistance** to simulate the beginning stage of the battery ISC."
각주 2 `[인쇄]`: "Using paralleled resistance is one of the easiest and safest methods to
quickly generate controllable and repeatable current leakage without damaging the batteries
[8,31,32]. Further, the leakage current at the beginning stage of the ISC tend to be stable
[33]." → **시불변 가정(각주 1)의 실험적 근거는 자기 인용 [33]** (Lai 2018, *Electrochim.
Acta* 278).

**Table 2** — Capacity and SOH of the selected batteries (전문 전사):

| No. | Capacity (Ah) | SoH (%) |
|---|---|---|
| #1 | 4.197 = 2.091 + 2.106 | 83.94 |
| #2 | 4.393 = 2.207 + 2.186 | 87.86 |
| #3 | 4.493 = 2.247 + 2.246 | 89.86 |
| #4 | 4.676 = 2.353 + 2.323 | 93.52 |
| #5 | 4.857 = 2.429 + 2.428 | 97.14 |
| #6 | 4.866 = 2.432 + 2.433 | 97.32 |

`[재현]` `SoH = Capacity / 5.0 Ah` 가 6 행 모두 소수 둘째 자리까지 맞는다 (예 4.197/5 =
0.8394). 단위 #1 이 **가장 약하고** #6 과 **13.4 %p** 차이 — 노화 산포가 **의도적으로 큰**
팩이다 (`[인쇄]` 초록 "covering various aging conditions").

**Table 3** — ISC estimation results with **passive** balancing and **known SoH**:

| Test No. | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| R_isc (Ω) | 55 | 110 | 220 | 330 | 165 |
| Ref. I_leak (mA) | 66.37 | 33.24 | 16.65 | 11.09 | 22.01 |
| Est. I_leak (mA) | 65.65 | 32.77 | 15.79 | 11.69 | 21.17 |
| Error (mA) | 0.72 | 0.47 | 0.86 | −0.6 | 0.84 |

**Table 4** — ISC estimation results with **active** balancing and **known SoH**:

| Test No. | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| R_isc (Ω) | 55 | 110 | 220 | 330 | 165 |
| Ref. I_leak (mA) | 66.08 | 33.12 | 16.57 | 11.04 | 23.51 |
| Est. I_leak (mA) | 66.15 | 33.45 | 16.43 | 11.81 | 24.09 |
| Error (mA) | −0.07 | −0.33 | 0.14 | −0.77 | −0.58 |

`[인쇄]` "With known battery SoH, all errors of the estimated leakage current can be
controlled within ±1 mA."

`[재현]` **상대 오차** (논문은 절대값만 적는다):

| R_isc | 수동 | 능동 |
|---|---|---|
| 55 Ω | +1.08 % | −0.11 % |
| 110 Ω | +1.41 % | −1.00 % |
| 220 Ω | **+5.17 %** | +0.84 % |
| 330 Ω | **−5.41 %** | **−6.97 %** |
| 165 Ω (Test 5) | +3.82 % | −2.47 % |

→ **"±1 mA" 는 고저항(작은 누설)에서 5–7 % 다.** Table 7 이 경쟁 방법을 `R_isc` 의 `%`
로 비교하므로 (§2.8), 같은 단위로 놓으면 **330 Ω 에서 7 %** 가 이 논문의 숫자다.

`[재현]` **기준 전류가 함의하는 평균 전압** `V̄ = Ref·R`: 수동 Tests 1–4 **3.650 / 3.656 /
3.663 / 3.660 V**, 능동 **3.634 / 3.643 / 3.645 / 3.643 V**, Test 5 수동 **3.632 V**, Test 5
능동 **3.879 V**. → FUDS 완전방전의 평균 ≈3.65 V 로 일관되고, Test 5 능동만 높다 —
`[도표]` Fig. 2(c) 가 3.45–4.0 V 사이를 오르내리는 **충전 우세** 프로토콜이라 정합.
**기준값이 옴의 법칙임을 역으로 확인한다** (G3).

`[인쇄]` "It is also worth noting that in Tests 1∼4, we fully discharge the battery pack,
with a SoC change of about **−100 %**".

## 2.6 §3.3 — SoH 추정 오차의 영향 (Fig. 6–8)

`[인쇄]` "By changing **only one SoH value from 95 % to 105 %** of its referenced value and
keeping the others unaltered … It is straightforward that the proposed method is **sensitive
to SoH estimation**. As ISC always discharges the batteries, **a lower SoH estimation value
tends to have a bigger impact** … in a discharging process."

`[인쇄]` "the SoH estimation error **on the cell suffering from ISC** will have a greater
impact … signals generated from small leakage currents (high `R_isc`) are more likely to be
**submerged by the SoH estimation error**. When we have a **2 % SoH estimation error, the
error in leakage current may exceed 100 %**."

`[인쇄]` Test 5: "the method's sensitivity to SoH can be significantly reduced. As described
in Fig. 8, **in some cases**, the error of leakage current can be bounded within **±6 % when
SoH estimation error exceeds 20 %**. … In the best case when the SoC change … is approaching
zero, the estimation of SoH will not influence the determination of ΔSoC … Further, the
**direction of the curves in Fig. 8-(b) changes** with the overall change of SoC".

★ `[인쇄]` 이 절의 결론 문장: "the determination of the leakage current can be **jointly
influenced by the `R_isc`, SoH accuracy, and change in SoC** … In our framework, the
determination of the leakage current is **less influenced by the balancing method** (e.g.,
active or passive)."

## 2.7 §3.4 — 추정 SoH 로 검출 (Table 5·6)

`[인쇄]` "the controlling threshold of the balancing hardware is **10 mV**, corresponding to
a SoC difference of about **1 %**. When the leakage current … is small, e.g., **10 mA**, we
need at least **5 h** for the ISC current to create a 1 % difference in battery SoC in our
experimental settings (**5 Ah battery pack**)."

`[인쇄]` 세 가지 불확실 요인을 스스로 나열한다: "the battery's **sensing may not always be
accurate**, batteries with the **same voltage may not necessarily share same SoC** (i.e., the
assumption for voltage-based balancing may not always hold), and the **SoH estimation** for
battery pack with balancing, at this stage, can have a typical error of about **2 %**" →
`[인쇄]` "it is recommended that the ISC detection should be implemented with a **longer
profile (e.g., > 10 h)**".

**Table 5** — Results of the employed SoH estimator (Appendix B):

| Cell | #1 | #2 | #3 | #4 | #5 | #6 |
|---|---|---|---|---|---|---|
| Ref. (%) | 83.94 | 87.86 | 89.86 | 93.52 | 97.14 | 97.32 |
| Est. (%) | 83.98 | 88.25 | 89.73 | 91.75 | 96.85 | 97.36 |
| Err. (%) | 0.04 | 0.39 | −0.13 | **−1.77** | −0.29 | 0.04 |

**Table 6** — Results of using estimated SoH for **Test 5**:

| Balancing | Passive | Active |
|---|---|---|
| Referenced I_leak (mA) | 22.01 | 23.51 |
| Estimated I_leak (mA) | 21.70 | 24.09 |
| Error (mA) | 0.31 | −0.58 |

`[재현]` 셋을 나란히 놓으면:
- **능동 Test 5**: 참 SoH → 24.09 / −0.58 (Table 4), 추정 SoH → **24.09 / −0.58** (Table 6).
  **소수 둘째 자리까지 동일.** `[도표]` Fig. 8(a) 에서 #1 의 기울기 ≈0.13 %/% 이고 #1 의 SoH
  오차가 0.04 % 이므로 변화 ≈0.005 % → 0.001 mA. 동일한 것이 **정합**이다.
- **수동 Test 5**: 참 SoH → 21.17 / 0.84 (Table 3), 추정 SoH → **21.70 / 0.31** (Table 6).
  ★ **틀린 SoH 를 넣었더니 오차가 줄었다** (0.84 → 0.31 mA). `[도표]` Fig. 8(b) 에서 #1 의
  기울기는 ≈ −6 %/% 이므로 #1 의 +0.04 % SoH 오차는 −0.24 % ≈ −0.05 mA 만 설명한다. 나머지
  ≈ +0.5 mA 는 **#2–#6 의 SoH 오차(특히 #4 −1.77 %)** 가 만든 것이다. `[해석]` 오차가 **상쇄**
  로 줄어든 것이고, 기준값 자체(G3)의 폭이 이 차이보다 클 수 있다. **"추정 SoH 로도 ±1 mA"**
  는 이 두 숫자 위에 서 있다 (G4).

`[인쇄]` "with a general dynamic load profile, the proposed method still **stands a chance**
to achieve an ultra-low error of ±1 mA." — ⚠ 초록의 "bounded by ±1 mA" 보다 훨씬 약한
표현이다 (§7 D3).

`[인쇄]` 정밀도의 물리적 자리매김: "we need **10 h to create a 2 % SoC change for a 5 Ah
battery under 10 mA** current leakage, while a **2 % accuracy is the state-of-the-art for SoC
estimation** [36–38]. In this work, we managed to quantitatively detect the magnitude of
leakage currents with a typical precision of **1 mA within 10 h**." `[인쇄]` "If we only need
to check the **presence** of leakage current, the detection time can be shortened."

## 2.8 Table 7 — 경쟁 방법 비교 (전문 전사)

| Ref. | Method | Accuracy | Strength | Weakness |
|---|---|---|---|---|
| [35] Moeini 2018 | Transient voltage response | 10 %–15 % for R_isc | Fast, low-cost, requires only voltage measurement | Sensitive to noise and sampling speed |
| [39] Kong 2018 | Remaining charging capacity | 10 %–15 % on R_isc | Requiring only basic parameters available from BMS | For charging profile only. **Sensitive to balancing** |
| [15] Lai 2023 | Balanced capacity | **<1 mA for I_leak** | High accuracy, suitable for general batteries | For float-charging profile only |
| [40] Feng 2018 | Model-based | ∼10 % for R_isc | Consider both temperature and voltage | Computational complex |
| [41] Chen 2022 | Voltage reconstruction | <20 % for R_isc | Suitable for online application and large batteries | Low generalization, low accuracy |
| **Proposed** | Balanced capacity and SoH | **Typ. 1 mA for I_leak** | High accuracy, suitable for general load profiles | **Rely on SoH estimation**, although it is available from BMS |

`[해석]` 표가 **단위를 섞는다** — 넷은 `R_isc` 의 `%`, 둘은 `I_leak` 의 `mA`. §2.5 의 상대
오차 표로 환산하면 **제안 방법의 330 Ω 은 −7 %** 이고, 이는 [40] 의 "∼10 %" 와 같은
자릿수다. `[인쇄]` "illustrating the **superiority** of our method" 는 단위를 섞은 채 나온
문장이다.

## 2.9 결론 · Future work

`[인쇄]` "This method not only **identifies ISC battery cells** but also offers a
**quantitative estimation of the severity** of ISCs." · "the typical leakage current
estimation error can be controlled within ±1 mA" · "quantitative detection of **micro ISC**
faults in **voltage-balanceable** battery packs (regardless of active/passive balancing
implementations) without requiring additional sensors **under any working conditions**".

`[인쇄]` Future work 4 항: (1) SoH 추정 오차 감소 (2) **다중 셀 ISC** 정량 (3) **평탄 전압
화학(LFP · Li–S)** — "conventional voltage-based balancing might not be suitable" (4) **온도
변화** 하 검출. `[인쇄]` "more tests (such as using **real-vehicle data** and using **larger
batteries**) should be carried out".

`[해석]` (2)·(3)·(4) 는 각각 식 (9a)·식 (5)·§3.1 의 25 ± 2 °C 가 **가정으로 닫은 자리**다.
결론이 "under any working conditions" 라 적고 같은 문단에서 온도·화학·다중 셀을 빼 놓는다.

## 2.10 Appendix A — 균등화 방식

`[인쇄]` voltage-based: "If the voltage difference in a pack is greater than **10 mV**, then,
discharge the cell with the **highest voltage**. If … lower than **3 mV**, then, shut down
the balancing circuit and do nothing." (→ **히스테리시스 10/3 mV**)
`[인쇄]` 수동: "dissipated as heat through the discharging resistor (**2.5 Ω**)", 효율 "0 %".
능동: "fed back to the entire battery pack via a DC–DC converter", 효율 **70 %**, "the
discharging current is about **2.7 A**". "the operating cycle is **1000 ms**, and in each
cycle, the balancing system works for **800 ms**, leaving **200 ms** for the battery voltage
to stabilize before its measurement."

`[재현]` 공개 데이터(§4-6): `55_passive` 의 `max|열 12| = 1.566 A` ≈ `3.9 V / 2.5 Ω = 1.56 A`
(식 4 정합), `55_active` 의 `max|열 12| = 2.786 A` ≈ "about 2.7 A" 정합.

## 2.11 Appendix B — SoH 추정기

`[인쇄]` 식 (B.1) `IC_k ≈ ΔQ/ΔV = (Q_k − Q_{k−H}) / (V_k − V_{k−H})`, `H = 1200 s`. "The
voltage difference between the **second valley and the third peak** is selected as the feature
'`s`'." 식 (B.2) `SoH = a·s + b`, `a = 3.01`, `b = −0.10` (단위 문제 → G11).
`[인쇄]` "the incremental capacity is only defined on **constant-current** profiles. However,
… the charging currents of the single cells are **no longer constant**, as shown in Fig. A.2.
… we followed the method in Ref. [47] to **smooth** the signal".

`[해석]` ★ 이것은 **우리 본진과 같은 좌표**(dQ/dV 봉우리·골 위치)를 **SoH 스칼라 회귀**에만
쓴 것이다. LLI/LAM 귀속은 0 — `LLI`·`LAM`·`degradation mode` 어휘가 논문에 없다. 즉 이
논문의 "aging" 은 **용량 스칼라**다.

---

# 3. 그림 판독 (`[도표]`)

**Fig. 2 — 부하 프로파일.** (a) FUDS 셀 전압 6 개: 4.2 V 에서 시작해 ≈230 min 에 ≈3.3 V,
FUDS 펄스로 아래쪽 스파이크(최저 ≈2.9 V), 끝에 ≈2.7 V 까지 떨어지는 **딥 후 ≈3.3 V 휴지**.
(b) "Zoom of (d)" — **592–600 min**, 3.55–3.59 V: #1·#2·#3·#4 가 위쪽에 모여 있고
**≈594 min 과 ≈598 min 에 계단**(균등화 on/off 로 보이는 ≈5–10 mV 꺾임), #5·#6 은 ≈10–15 mV
아래에서 매끈하게 오른다. (c) 능동 Test 5: **충전(≈4.0 V 까지) + FUDS 방전(≈3.45 V 까지)
사이클 5 회**, 총 **≈870 min**. (d) 수동 Test 5: **충전(≈3.8 V) + 방전(≈3.0 V) 사이클 2 회**,
총 **≈720 min**. ★ (c)·(d) 는 **다른 프로토콜**이다 — 같은 "Test 5" 라는 이름 아래 능동과
수동이 **사이클 수·전압 창·길이가 다르다** (§7 D7).

**Fig. 3 — 능동 균등화의 balanced capacity (Ah), 0–250 min.** ★ **#1(파랑)만 양(+)이다**:
끝값 ≈ **+0.23 (55 Ω) · +0.12 (110) · +0.07 (220) · +0.05 (330)** — 누설이 클수록 #1 이 **더
많이 받는다**. 나머지는 SoH 순서로 음: #2 ≈ −0.23/−0.20/−0.18/−0.18, #3 ≈ −0.31/−0.28/
−0.26/−0.26, #4 ≈ −0.47/−0.42/−0.39/−0.40, **#5·#6 겹쳐서 ≈ −0.64/−0.61/−0.59/−0.60**.
판독 오차 ±0.02 Ah. `[해석]` 능동에서 #1 이 양인 이유는 §4-6 의 데이터 대조가 준다 —
**환류 전하(전 셀 공통 +0.71 Ah)가 #1 의 적은 방전량(−0.49 Ah)을 넘어서기 때문**이다.
⚠ **220 Ω 과 330 Ω 의 #1 곡선이 거의 구별되지 않는다** (≈0.02 Ah 차) — §5 의 dead-band
논의로 이어진다.

**Fig. 4 — 수동 균등화, 0–≈225 min.** 전부 음. **#1 이 가장 적게 방전**: ≈ **−0.08 (55) ·
−0.15 (110) · −0.18 (220) · −0.18 (330)**; #5·#6 ≈ −0.85/−0.79/−0.77/−0.77; #2 ≈ −0.49/−0.44/
−0.40/−0.39; #3 ≈ −0.56/−0.51/−0.48/−0.47; #4 ≈ −0.68/−0.62/−0.59/−0.59. ★ **§4-6 의 데이터
대조와 0.01 Ah 안에서 일치한다.** ⚠ 시간축이 Fig. 3(250 min)보다 짧다(≈225 min) — 데이터셋의
135,000 vs 150,000 행(3.75 vs 4.17 h)과 정합.

**Fig. 5 — Test 5 (165 Ω).** (a) 능동, 0–≈870 min: #1 이 **주기적으로 솟아오르며**(충전 구간
마다 +) 다른 다섯 위에 있다가 끝에 ≈ −0.25 (⚠ y 라벨 잘림, ±0.1); 나머지는 계단형으로 ≈ −0.6.
(b) 수동, 0–≈720 min: 전부 **계단**(균등화가 특정 구간에만 동작). 끝값 **#6 ≈ −0.86 · #1 ≈
−0.95 · #4 ≈ −0.97 · #3 ≈ −1.07 · #2 ≈ −1.12** (#5 는 #6 아래 숨은 듯). ★★ **수동 Test 5 에서는
#1 이 가장 적게 방전된 셀이 아니다** — Fig. 4 의 단순한 그림("ISC 셀 = 최소 방전")이
**충전 구간이 있는 프로파일에서 깨진다.** 본문은 이 반전을 언급하지 않는다 (§7 D8).
`[해석]` 충전 중에는 SoH 가 낮은 #1 이 먼저 고전압에 닿아 **더 많이 방전당한다** — 즉
"누설 셀의 서명" 이 **부하 방향에 따라 부호가 바뀐다.** 식 (12) 는 정규화 후 max−min 을
쓰므로 원리상 영향이 없어야 하지만, 그 정규화의 입력이 SoH 다.

**Fig. 6 — Test 1 (55 Ω), 셀 하나의 SoH 를 ±5 % 흔들 때 `I_leak` 오차(%).** #1 만 **원점을
지나는 직선**, 기울기 ≈ **+13–14 %/%** (−5 % → ≈ −66 % 능동 / ≈ −75 % 수동; +5 % → ≈ +66 % /
+70 %). #2–#6 은 **비대칭**: SoH 를 **올리면** 오차 ≈0 (평탄), **내리면** −5 % 에서 ≈ +66–72 %
로 튄다 (수동 #4 는 ≈ −1 % 에서 꺾임). `[해석]` 정상 셀의 SoH 를 내리면 그 셀의 정규화 합이
커져 **max 셀이 바뀐다** → 식 (12) 의 `max` 항이 튄다. 비대칭은 (12) 의 `max/min` 구조의
직접 흔적이다.

**Fig. 7 — Tests 1–4, #1 의 SoH 오차 ±5 % → `I_leak` 오차(%).** 55 Ω: ≈ ±70 % 직선. 110 Ω:
+5 % → ≈ +140 %, −5 % → ≈ −45 % (능동; ≈ −3.5 % 에서 꺾여 되오름). 220 Ω: +5 % → ≈ **+260 %**,
−5 % → ≈ +120 % (능동) / ≈ +160 % (수동), 최소 ≈ −45 % 가 ≈ −1 % 부근. 330 Ω: +5 % → ≈ **+400 %**,
−5 % → ≈ +270 % (능동) / ≈ +370 % (수동), 최소 ≈ −20 % 가 ≈ −1 % 부근; 수동 330 Ω 은 −1 ~ 0 %
에서 ≈ +5 % 평탄. ★ **−2 % SoH 오차에서 330 Ω 은 ≈ +100–150 %, 220 Ω 은 ≈ +40–100 %** →
본문 "may exceed 100 %" 와 정합. **V 자의 꺾임**은 max/min 셀 교대의 흔적.

**Fig. 8 — Test 5 (165 Ω).** (a) 능동, x = −30 ~ +30 %: #1 이 ≈ −1.5 % → ≈ **+6.2 %** (기울기
≈ **0.13 %/%**); #2–#6 은 양의 SoH 오차에서 ≈ +2.4 % 로 평탄(#6 은 ≈ +1.9 %), 음의 쪽에서
−30 % 에 ≈ +4 ~ +8 %. **여기가 "±6 % under >20 %" 의 출처**이고 (a) 에만 해당한다.
(b) 수동, x = **−10 ~ +10 %** (a 의 1/3 창): #1 이 ≈ **+57 % → ≈ −65 %** (기울기 ≈ **−6 %/%**,
**부호 반전**); #2–#6 은 음의 쪽에서 ≈ −3 % 평탄(#2 는 ≈ −12 %), 양의 쪽에서 +10 % 에
≈ +25 ~ +52 %. ★★ **능동과 수동의 SoH 민감도가 ≈45 배 다르다** (0.13 vs 6 %/%). 본문은 이를
"in some cases" 와 "direction … changes" 로 적는다. ⚠ 그러나 (a)·(b) 는 **프로토콜도 다르다**
(Fig. 2(c) vs (d)) → 균등화 방식의 효과와 프로토콜의 효과가 **분리되지 않는다** (§7 D7).

**Fig. A.1 (p.7 렌더).** `ΔQ/ΔV (Ah/V)` vs `Voltage (V)` 3.4–4.2 V: 봉우리 ≈3.65 V (≈9 Ah/V) ·
≈3.95 V (≈6.5); 골 ≈3.5 V · ≈3.85 V. `s` 는 **≈3.85 V 골 ↔ ≈3.95 V 봉우리** 사이 폭으로 표시
→ ≈0.1 V (G11 의 단위 문제).

**Fig. A.2 (p.7 렌더).** 수동 균등화 중 6 셀의 **충전 전류 (A), 0–350 min**: 설계 전류(주황
직선) ≈ **+0.83 A** 일정, 실측(파랑 점)은 균등화가 켜질 때 ≈ **−0.7 ~ −1.0 A** 로 떨어지는
**음의 채터링**. 빈도: **#1 은 ≈4 회로 드물고**, #2·#3·#4 는 조밀, #5·#6 은 2–3 묶음.
⚠ 이 충전이 어느 시험의 것인지 본문에 없다. `[재현]` 채터링 크기 ≈ 0.83 − 1.5 ≈ −0.7 A
(식 4 의 균등화 전류 ≈1.5 A 를 빼면) — 정합.

---

# 4. 우리 7 개 물음에 대한 답 (`ISC_LEAKAGE_DATASET.md` §5)

## 4-1. ISC 저항이 셀 #1 에 달렸는가 → **예** (`[인쇄]`)

`[인쇄]` "In each test, **the weakest battery, say, #1**, is paralleled with an accurate external
short circuit resistance". "weakest" = Table 2 의 최저 SoH(83.94 %). 데이터셋의 관측(첫·끝 행
최저 전압 = 1 번, `ISC_LEAKAGE_DATASET.md` §3)과 일치한다. ⚠ **모든 시험에서 ISC 를 가장 약한
셀에만 달았다** — 강한 셀(#6)의 누설은 시험되지 않았다. `[해석]` "약한 셀 + 누설" 은 두 원인이
**같은 방향**으로 전압을 내리는 가장 쉬운 배치다. 반대 배치(강한 셀에 누설)에서 식 (12) 의
정규화가 두 원인을 갈라 주는지는 이 논문에 없다.

## 4-2. 저항 단위·셀·팩 사양 → **Ω · SONY US18650VTC5 · 6S2P**

`[인쇄]` **55 / 110 / 220 / 330 Ω** (Tests 1–4) + **165 Ω** (Test 5). 셀 **SONY US18650VTC5**,
공칭 **2.5 Ah**, **6S2P**(단위 5 Ah, 실측 4.197–4.866 Ah), **25 ± 2 °C**, Fig. 1 캡션 "NCM".
데이터셋 파일명의 `55…330` 이 Ω 이고, 6 열 전압 4.09–4.11 V 시작이 만충 근방으로 정합.

## 4-3. 17 번째 열 → **논문 무언급 (n/a)**

논문에 열 정의가 없다(G10). `[재현]` 두 파일에서 17 열은 **1 씩 증가하는 카운터**
(`55_passive` 355,711 → 490,710 = 134,999 증가 = 행 수 −1; `55_active` 416,651 → 566,650
= 149,999). **파일마다 시작값이 다르고 두 범위가 겹친다**(355,711–490,710 ↔ 416,651–566,650)
→ 파일을 관통하는 단일 시각 카운터는 **아니다.** 16 열은 첫 행 `1`, 끝 행 `0` (되감김).
`[해석]` 세션 내 프레임 카운터로 보이나 **확인 불가**로 남긴다.

## 4-4. `165` 조건이 왜 3.5 배 긴가 → **설계다 (Test 5 = 다른 프로토콜)**

`[인쇄]` Test 5 만 Fig. 2(c)(d) 의 **충·방전 반복 프로파일**을 쓴다 — 목적은 §3.3 의 "ΔSoC 를
줄여 SoH 민감도를 낮춘다" 와 §3.4 의 "**>10 h** 프로파일 권고" 를 만족시키는 것.
`[도표]` 능동 ≈870 min = **14.5 h** ↔ 데이터셋 `165_active` **522,000 행 × 0.1 s = 14.50 h**
**정확히 일치.** `[도표]` 수동 ≈720 min = 12 h → 깨진 `165_passive` 는 **≈432,000 행**이었을
것으로 추정 (중앙 디렉터리 크기 35.9 MB 가 `165_active` 44.7 MB 의 80 % 인 것과 정합).

★★ **재현 불가 원장** — 공개 데이터셋에서 `165_passive.xlsx` 가 깨져 있으므로
(`ISC_LEAKAGE_DATASET.md` §1 실측) 다음이 **재현 불가**다:
- **Table 3 의 Test 5 열** (22.01 / 21.17 / 0.84 mA)
- **Table 6 의 Passive 열** (22.01 / 21.70 / 0.31 mA) — ★ **추정 SoH 로 돌린 수동 결과의 유일한
  숫자**(G4)
- **Fig. 2(b)·(d)**, **Fig. 5(b)**, **Fig. 8(b)** (수동 Test 5 의 모든 그림)
- 따라서 **"수동 균등화에서 SoH 민감도가 능동의 ≈45 배" (Fig. 8) 라는 이 논문의 가장 불편한
  관측도 공개 데이터로는 확인할 수 없다.**
나머지 8 조건(Tests 1–4 × 2 + 능동 Test 5)은 재현 가능하되 **Table 2 의 SoH 가 데이터셋에
없으므로 논문에서 옮겨 와야 한다.**

## 4-5. 검출인가 정량인가 — 유일성·오차막대 → **둘 다 하되, 폭은 없다**

- **검출**: ISC 셀 식별 (암묵적 min 셀, G5). **정량**: `i_L` (mA) 를 식 (12) 닫힌 형태로.
  ⚠ **`R_isc` 는 추정 출력이 아니다** — 조건 라벨로만 등장하고, 초록의 "the internal
  short-circuit resistance can be determined" 는 `[해석]` `R = V̄/i_L` 로 환산 가능하다는
  뜻으로 읽힌다(그 환산은 지면에 없다).
- **유일성 0 · 오차막대 0 · 반복 0** (G1). 조건당 실행 1 회.
- 유일한 "폭": §3.3 의 **SoH 1 변수 섭동**(Fig. 6–8). `[해석]` 우리 어휘로는 **nuisance 한 방향
  (SoH_1)의 근최적 폭 단면**이다 — 330 Ω 에서 ±2 % SoH → **>100 %** 폭. 논문은 이것을 "민감도"
  라 부르고 **점추정 옆에 놓지 않는다** (Table 3/4 는 오차 한 숫자만).
- **다른 원인과 갈리는지 시험했는가**:
  - **용량 편차** → **예, 이것이 방법의 본체다** (SoH 정규화, Table 2·5). 그리고 Fig. 6–8 이
    그 정규화의 취약성을 재고 있다.
  - **자기방전 산포** → **아니오, 정의상 묻지 않는다** (G2). 식 (3) 에 항이 없고 각주 2 가
    "current leakage" 검출이라 못 박는다.
  - **온도** → **아니오** (25 ± 2 °C 고정, future work (4)). 데이터셋의 4 개 온도 열은 논문에
    쓰이지 않는다. `[재현]` `55_active` 끝 행 환경 온도 **26.88 / 27.47 / 27.53 / 25.21 °C** —
    27.53 은 "25 ± 2" 상한을 0.5 °C 넘는다 (⚠ 첫·끝 행만 봤다, 전 구간 아님).
  - **다중 셀 ISC** → 식 (9a) 가 배제 (future work (2)).

## 4-6. 균등화 전략(passive/active)이 검출에 주는 영향 → **"거의 없다" 가 논문 입장, 그림은 다르게 말한다**

**논문의 입장** `[인쇄]`: "applicable in both active and passive" · "less influenced by the
balancing method" · 결론 "regardless of active/passive balancing implementations".
**논문의 그림**: (i) Fig. 3 vs 4 — **ISC 셀의 서명 부호가 반대**(능동 +, 수동 −); (ii) Fig. 8 —
**SoH 민감도 ≈45 배 차**(단 프로토콜 혼입). 논문은 (i) 를 설명하지 않고 (ii) 를 "in some cases"
로 적는다.

★★ **공개 데이터셋과의 대조** `[재현]` (`55_passive` · `55_active` 전수, 열 14 의 대상 셀 인덱스
`0..5` 별로 열 12 를 0.1 s 적분):

| 단위 | `55_passive` Σ열12 (Ah) | Fig. 4(a) 끝값 `[도표]` | `55_active` Σ열12 (Ah) | + Σ열13 (0.714 Ah) | Fig. 3(a) 끝값 `[도표]` |
|---|---|---|---|---|---|
| #1 | −0.088 | ≈ −0.08 | −0.485 | **+0.229** | ≈ +0.23 |
| #2 | −0.490 | ≈ −0.49 | −0.939 | **−0.225** | ≈ −0.23 |
| #3 | −0.566 | ≈ −0.56 | −1.029 | **−0.315** | ≈ −0.31 |
| #4 | −0.687 | ≈ −0.68 | −1.185 | **−0.471** | ≈ −0.47 |
| #5 | −0.853 | ≈ −0.85 | −1.348 | **−0.634** | ≈ −0.64 |
| #6 | −0.861 | ≈ −0.85 | −1.351 | **−0.637** | ≈ −0.64 |

→ **세 가지가 확정된다**: ① 데이터셋의 **열 14 인덱스 `0` = 논문의 셀 #1** (0-기반);
② 논문의 "balanced capacity" = **대상 셀 방전 전하(열 12) + 환류 전하(열 13)** 의 누적이고,
수동에서는 열 13 ≈ 0 (Σ = 0.004 Ah, `max` 0.005 A); ③ 능동에서 **환류는 6 셀에 동일**하게
Σ열13 = **0.714 Ah** 씩 들어간다 (G9 의 답). `[재현]` 총 방전 6.337 Ah × 6 셀 환류 0.714 ×
6 = 4.284 Ah → **전하 효율 67.6 %** ≈ `[인쇄]` 에너지 효율 70 %.
→ `ISC_LEAKAGE_DATASET.md` §3 의 "**177 배**" (수동 14.5 A·s ↔ 능동 2,572 A·s) 는 **정확히
이 환류 항의 유무**다.

**덮는가 — 논문이 인정한 기제 셋** (§3.4): dead-band **10 mV ≈ 1 % SoC** · **SoH 오차 2 %** ·
**같은 전압 ≠ 같은 SoC**. **논문이 적지 않은 것**: `[재현]` Test 4 (330 Ω, 수동 3.75 h) 에서
누설이 만든 총 SoC 격차는 `11.09 mA × 3.75 h / 4.197 Ah ≈ **1.0 %**` — **dead-band 와 같은
크기**다. 그런데 추정 오차는 0.6 mA (5 %). `[해석]` 균등화기가 dead-band 안에서 "안 본" 격차를
식 (12) 가 어떻게 5 % 안에서 복원하는지 논문은 설명하지 않는다 — **부하 중 IR 차이가 전압차를
키워 균등화를 더 자주 켜는 것**이 후보이지만 검증 없음. 이것이 닻 카드 물음 P3.

## 4-7. 누설 전류: 직접 측정인가 계산인가 → **계산(derived)**

`[인쇄]` "The referenced leakage current can be obtained by **dividing the average battery
voltage by the short-circuit resistance**." **누설 전류 센서는 없다.** 저항값은 설계값(허용오차
미기재, G3). 그리고 **비교 대상인 균등화 전류도 수동에서는 식 (4) 의 계산값**(`V/R_bal`)이고,
능동은 "typical balancing current commonly available". `[재현]` 데이터 열 12 의 `max` 1.566 A
가 `V/2.5 Ω` 와 맞는 것은 **계산값과도 측정값과도 정합**이라 둘을 가르지 못한다.

**라벨 층위표** (요구서 `NEW_MODEL_REQUIREMENTS.md` §5 형식):

| 양 | 층위 | 오차막대 |
|---|---|---|
| `R_isc` (55–330 Ω) | **designed** (설계·삽입값; 실측·허용오차 없음) | 없음 |
| Ref. `I_leak` | **derived** (`V̄ / R_isc`, 옴의 법칙) | 없음 |
| Ref. SoH (Table 2) | **measured** (용량 실측; 프로토콜 미기재 G6) | 없음 |
| Est. SoH (Table 5) | **fitted** (IC 특징 선형 회귀 2 파라미터; 교정 집합 미기재; 단위 불일치 G11) | 없음 (오차 열은 있음) |
| Est. `I_leak` | **derived** (식 12; 입력 = 팩 전류 측정 + 균등화 전류 계산/기록 + SoH) | 없음 |
| `I_bal` 수동 | **derived** (식 4) | — |
| `I_bal` 능동 | **recorded** ("commonly available" — 측정인지 설정값인지 불명) | — |

★ **이 계보에서 처음 보는 것**: 정답 라벨이 **설계값**이다 — 결함을 **알고 심었다**. 우리 본진의
"measured 라벨 없음" (`NEW_MODEL_REQUIREMENTS.md` §5·§8-6) 과 정반대의 위치. ⚠ 단 **우리 축의
라벨이 아니다** — 저항값은 LLI/LAM 과 무관하다.

---

# 5. 검출인가 정량인가 — 유일성의 구조 (`[해석]`)

식 (12) 를 우리 어휘로 다시 쓰면 **미지수는 `(l, i_L, SoH_1..6)` 8 개**이고 관측은 셀별 정규화
균등화 용량 6 개다. 논문은 **SoH 6 개를 외부에서 받고 `l` 을 min 으로 고정**해 `i_L` 하나를
닫힌 형태로 낸다. 그러므로:

1. **주어진 (l, SoH) 아래에서 `i_L` 은 유일하다** — 이것이 논문의 "quantitative".
2. **그 조건을 풀면 유일하지 않다** — Fig. 7 이 그것을 보인다: SoH_1 을 ±2 % 움직이면 330 Ω 에서
   `i_L` 이 **>100 %** 움직인다. 즉 **`(i_L, SoH_1)` 평면에 flat valley 가 있다** — 관측이 두 방향을
   가르지 못한다. 논문은 이를 "sensitivity" 라고 부르고, 그 폭을 결과 표에 붙이지 않는다.
3. **자기방전 방향은 정확 null 이다** — 셀 `l` 의 자기방전 증가 `δ` 와 `i_L` 은 식 (3) 에서 **같은
   항**이다. 관측으로는 원리적으로 안 갈린다. 논문은 이 방향을 **정의로 닫았다**(각주 2).
4. **비용함수 (10) 과 해 (12) 가 다르다.** (10) 은 15 쌍 절댓값 합, (12) 는 max−min 한 쌍. (10) 의
   최소화자가 (12) 와 같다는 보장은 없고, 절댓값 합의 최소화자는 일반적으로 **집합**이다.

**우리 계보와의 대응**:
- [[fitting-degeneracy]] 의 **flat valley** ↔ 여기 2번 (`i_L ↔ SoH_l`).
- [[near-optimal-set-width-measurement]] 의 **폭** ↔ Fig. 7 의 수직 폭 (논문은 재 놓고 이름
  붙이지 않았다 — `assb` 11호 Yu 2024 의 Fig. S3 와 **같은 형태**).
- `NEW_MODEL_REQUIREMENTS.md` §3 의 **후보 원인 칸** ↔ {ISC 누설, 자기방전 편차, 용량 편차}
  — 셋 중 **용량 편차만 칸으로 두고**, 자기방전은 **누설과 합쳐서** 한 칸, 그 합쳐진 칸을
  "ISC" 라 부른다.
- §4 의 **구분 시험** ↔ 이 논문에는 **T-계열이 없다.** 시불변성(각주 1)·단일 셀(9a)을 가정으로
  닫았고, 가정을 시험하는 절이 없다. 후보 시험 하나는 논문 자신이 준다: **부하 방향 반전**
  (Fig. 5(b) 에서 서명 부호가 바뀐다) — 누설은 방향과 무관하게 방전이므로, 방향을 바꿔도 남는
  성분이 누설이다. 미실행.

---

# 6. 균등화가 관측을 덮는가 — 논문의 입장 vs 우리 실측, 한 표로

| 물음 | 논문 | 우리 실측/재현 |
|---|---|---|
| 균등화는 센서인가 교란인가 | **센서** (`[인쇄]` "convert battery equalizers into the equivalent current sensor") | 데이터로 정합: 균등화 적분 = Fig. 3/4 그대로 (§4-6) |
| 수동 ↔ 능동의 서명 | "less influenced" | **부호가 반대**(#1: 능동 + / 수동 −), 차이 = 환류 0.714 Ah (전 셀 공통) |
| 수동 ↔ 능동의 SoH 민감도 | Fig. 8 "in some cases ±6 %" | `[도표]` 능동 0.13 %/% ↔ 수동 6 %/% — **≈45 배**, 프로토콜 혼입 |
| dead-band | 10 mV ≈ 1 % SoC, 10 mA 는 5 h | `[재현]` 330 Ω 수동 시험의 총 누설 SoC 격차 ≈1.0 % = dead-band 크기인데 오차 5 % — **왜 되는지 미설명** |
| 균등화 없는 대조군 | **없다** | — (방법이 균등화를 전제하므로 구조적으로 없음; 그러나 "균등화가 무엇을 가렸나" 는 이 대조군 없이는 못 잰다) |
| 자기방전 편차 | 정의로 배제 (각주 2) | 데이터로도 못 가른다 — 정확 null (§5-3) |
| 온도 | 25 ± 2 고정 | `[재현]` 끝 행 27.53 °C (첫·끝 행만) |

---

# 7. 어긋남 (D-계열) — 실제로 찾은 것만

| # | 어긋남 | 근거 |
|---|---|---|
| **D1** | **초록 "estimation errors bounded by ±1 mA"** ↔ §3.4 "**stands a chance** to achieve … ±1 mA" ↔ Table 7 "**Typ.** 1 mA" | 같은 숫자에 세 강도의 수식어 |
| **D2** | §3.2 `[인쇄]` "The **balanced current** of each tested scenario is shown in Figs. 3, 4, and 5" ↔ 그림의 y 축은 **Balanced Capacity (Ah)** | 어휘 |
| **D3** | 기여 ② "does **not rely on specific** … load profiles" ↔ §3.4 권고 "**longer profile (e.g., > 10 h)**" · "best case … SoC change approaching zero" ↔ Table 1 자기 분류의 약점 "Sensitivity to load profiles" | 식은 프로토콜 무관, **정밀도는 프로토콜 함수** |
| **D4** | 결론 "under **any** working conditions" ↔ 같은 절의 future work (3) LFP 불가 · (4) 온도 미검증 · (2) 다중 셀 미검증 | |
| **D5** | Table 7 이 `R_isc %` 와 `I_leak mA` 를 **한 열에 섞고** "superiority" 를 말한다 ↔ `[재현]` 제안 방법의 330 Ω 상대 오차 **−7 %** 는 [40] 의 ∼10 % 와 같은 자릿수 | §2.8 |
| **D6** | **명칭 셋**: 제목 "balanced capacity" · 결론 "balanced **charge**" · 결론 "balanced **electrical quantity**" | |
| **D7** | §3.3 "**less influenced by the balancing method**" ↔ `[도표]` Fig. 8(a)/(b) SoH 민감도 ≈45 배 차 · Fig. 3/4 서명 부호 반대. 그리고 Test 5 의 능동·수동이 **다른 프로토콜**(Fig. 2(c) 5 사이클 ≈870 min ↔ (d) 2 사이클 ≈720 min)이라 **균등화 효과와 프로토콜 효과가 분리되지 않는다** | |
| **D8** | `[도표]` Fig. 5(b) 수동 Test 5 에서 **#1 이 최소 방전 셀이 아니다** (#6 이 최소) ↔ Fig. 4 의 "ISC 셀 = 최소 방전" 그림 · 본문 무언급 | 서명 부호가 **부하 방향**에 따라 바뀐다 |
| **D9** | **Table 3 vs 6 수동 Test 5**: 참 SoH 오차 0.84 mA → **추정 SoH 오차 0.31 mA** — 틀린 입력이 결과를 **개선** | `[재현]` §2.7 — 상쇄 오차의 지문 |
| **D10** | **Appendix B 계수 단위** `a = 3.01`, `b = −0.10`, "SoH in %, s in V" → `[도표]` `s ≈ 0.1 V` 면 SoH ≈ 0.2 % | G11 |
| **D11** | Fig. 2 캡션 `[인쇄]` "Tests 1 4" (대시 누락 — 편집) · "(b): Zoom of (d)" 인데 (b) 가 (d) 보다 앞에 배치 | 편집 |
| **D12** | §3.4 "**5 Ah battery pack**" ↔ 실제는 5 Ah **단위(2P)** × 6 직렬 팩 | 어휘 |
| **D13** | Fig. 3 능동 시간축 **250 min** ↔ Fig. 4 수동 **≈225 min**, 캡션은 둘 다 "FUDS" 한 프로파일 | 데이터셋 150,000 ↔ 135,000 행과 정합 — 프로파일이 같아도 **길이가 다르다**, 본문 무언급 |
| **D14** | `[재현]` 데이터 끝 행 환경 온도 **27.53 °C** ↔ `[인쇄]` "25 ± 2 °C" | ⚠ 첫·끝 행만 확인 |

**어긋남 14 건.** 주장을 직접 약화시키는 것은 **D3 · D5 · D7 · D8 · D9** 다섯이다. 나머지는
어휘·편집이다.

---

# 8. 우리 프로젝트와의 접점 — 모양은 같고 물리량은 다르다

**다른 점을 먼저.** 이 논문의 출력은 **결함 전류(mA)** 이고, 우리 본진의 출력은 **열화 모드
지분(LLI/LAM_PE/LAM_NE)** 이다. 이 논문의 "aging" 은 **SoH 스칼라**(Appendix B) 이고
`LLI`·`LAM` 어휘가 0 이다. 그러므로 **이 논문은 `degradation-degeneracy/` 의 어떤 결론도
건드리지 않고**, `fitting-degeneracy` 페이지에 태그를 달지 않는다 (SCHEMA `pack-fault`
경계 ②).

**같은 점 — 문제의 모양.**
1. **두 원인 → 같은 관측**: {ISC 누설, 자기방전 편차} → 한 셀의 SoC 가 상대적으로 내려간다
   (§5-3 정확 null). {용량 편차} → 같은 방향, SoH 로 정규화 (flat valley §5-2).
2. **그 위에 조작이 겹친다**: 균등화기가 전하를 실어 보내 전압 격차를 지운다. 논문은 그 조작을
   **센서로 뒤집었다** — 우리 본진에서 `pOCV` 필터링이나 `dQ/dV` 항 추가가 관측을 바꾸는 것과
   같은 자리다. `assb` 계열의 조작 쌍(율 스윕 `i→0` · 재가압 `P↑`)에 대응하는 것이 여기서는
   **수동 ↔ 능동** 쌍이고, ⚠ **직교하지 않는다** (환류가 SoC 를 바꾸면 누설 `V/R` 도 바뀐다 —
   `ISC_LEAKAGE_DATASET.md` §4-3 의 우려가 데이터로 확인됨: 환류 0.714 Ah 는 5 Ah 의 14 %).
3. **유일성 미측정 + 잴 재료는 지면에 있음** (Fig. 7) — `assb` 11호와 같은 형태.

**우리가 이 논문에 공급할 수 있는 것** (식별 가능성 경계):
- Fig. 7 을 **`(i_L, SoH_1)` 평면의 근최적 집합**으로 다시 그리기 — 폭을 mA 로 보고. 재료는
  전부 있다 (식 12 + Table 2 + 공개 데이터 8 조건).
- **부하 방향 반전 시험**(§5 끝) — Fig. 5(b) 가 우연히 보여 준 서명 부호 반전을 **구분 시험**으로
  설계.
- **자기방전 방향이 정확 null 임을 명시** — 논문이 "ISC" 라고 부르는 것이 "한 셀의 초과 누설"
  임을 라벨에 적는 것.

**우리가 이 논문에서 가져올 수 있는 것**:
- ★ **설계된 결함 라벨**이라는 실험 설계 — 결함을 알고 심고 되찾는다. 우리 본진은 PyBaMM 합성
  truth 로 같은 일을 하지만 **실셀에서는 못 했다**(`NEW_MODEL_REQUIREMENTS.md` §8). 액체셀
  실팩에서 **measured 급 라벨을 갖는 유일한 데이터**가 이것이다 — 단 우리 축은 아니다.
- **8 조건 × 100 ms × 17 열의 팩 데이터** — 균등화 전류·팩 전류·셀 전압이 같은 시각축에 있다.
  `bms-balancing/` 의 균등화 축에는 직접 자료다.
- **관측 하나**: 균등화 적분(열 12 + 열 13)이 **셀별 SoH 순서를 그대로 재현**한다 (Fig. 3/4 의
  곡선 순서 = Table 2 순서). `[해석]` 균등화 적분 자체가 **SoH 관측**이고 (자기 인용 [28] 의
  아이디어), 그것으로 SoH 를 추정하고 그 SoH 로 누설을 정규화하면 **순환**이다 — 이 논문은
  SoH 를 IC 특징(Appendix B)에서 따로 얻어 순환을 피했다. 그 분리가 잘 됐는지가 Fig. 8(b) 의
   −6 %/% 이다.

---

# 9. 후속으로 받아야 할 원 논문 후보

| 우선 | 서지 | 왜 |
|---|---|---|
| ★★★ | **[27] Tang, Zhu, Lai, Zhou, Zheng, Gao, "An aging- and load-insensitive method for quantitatively detecting the battery internal-short-circuit resistance", *Chem. Eng. J.* 476 (2023) 146467** | 같은 그룹의 **`R_isc` 정량 2 %** · "round-trip" 제약 — 이 논문이 넘었다는 벽의 원전. **`aging-insensitive`** 를 어떻게 주장했는지가 우리 SoH 정규화 물음의 직접 자료 |
| ★★★ | **[15] Lai, Li, Tang, Zhou, Zheng, Gao, "A quantitative method for early-stage detection of the internal-short-circuit in lithium-ion battery pack under float-charging conditions", *JPS* 573 (2023) 233109** | **±1 mA 의 원전**, float-charging 한정. 이 논문의 Table 7 이 자기보다 낫다고 적은 유일한 행 |
| ★★ | **[39] Kong, Zheng, Ouyang, Lu, Li, Zhang, "Fault diagnosis and quantitative analysis of micro-short circuits for lithium-ion batteries in battery packs", *JPS* 395 (2018) 358** | Table 7 이 "**Sensitive to balancing**" 이라 적은 경쟁 방법 — **균등화가 ISC 관측을 덮는다는 진술의 1차 근거**. 닻 카드의 물음이 문헌에서 처음 인쇄된 자리일 가능성 |
| ★★ | **[28] Tang, Gao, Liu, Liu, Foley, "A balancing current ratio based state-of-health estimation solution for lithium-ion battery pack", *IEEE TIE* 69 (2022) 8055** | **균등화 전류로 SoH 를 추정** — §8 의 순환 우려의 원전. 이 논문이 왜 IC 특징(Appendix B)으로 우회했는지 |
| ★★ | **[8] Shen et al., "Detection and quantitative diagnosis of micro-short-circuit faults in lithium-ion battery packs considering cell inconsistency", *GEITS* 2 (2023) 100109** | **셀 불일치를 고려한** 경쟁 정량법 — 용량 편차 ↔ 누설의 분리를 다른 방식으로 |
| ★ | **[33] Lai, Zheng, Zhou, Gao, "Electrical behavior of overdischarge-induced internal short circuit in lithium-ion cells", *Electrochim. Acta* 278 (2018) 245** | **각주 1 시불변 가정의 근거** ("leakage current at the beginning stage … tend to be stable") |
| ★ | **[32] Liu, Feng, Zhang, Lu, Han, He, Ouyang, "Comparative study on substitute triggering approaches for internal short circuit", *Appl. Energy* 259 (2020) 114143** | **병렬 저항이 ISC 대리로 타당한가**의 근거 — 라벨 층위 "designed" 의 물리적 정당성 |
| ★ | **[23] Song, Park, Kim, "Model-free quantitative diagnosis of internal short circuit for lithium-ion battery packs under diverse operating conditions", *Appl. Energy* 352 (2023) 121931** | "**diverse operating conditions**" 를 주장하는 경쟁 정량법 — 이 논문이 "aging 미고려" 로 비판 |
| ★ | **[47] Lai, Yao, Tang, Zheng, Zhou, Sun, Gao, "Voltage profile reconstruction and state of health estimation … under dynamic working conditions", *Energy* 282 (2023) 128971** · **[30] Tang, Wang, Liu, Gao, *iScience* 24 (2021) 103103** | Appendix B 의 **IC 평활·재구성**과 **플랫폼 상세**의 원전 (G6·G11 을 닫을 유일한 경로) |

---

# 10. 이 digest 가 주장하지 않는 것

- **이 논문의 방법이 틀렸다고 주장하지 않는다.** 참 SoH 를 알면 ±1 mA 가 10 조건에서 재현됐고,
  공개 데이터로 8 조건은 검증 가능하다. 우리가 적은 것은 **폭이 없다**는 것과 **"ISC" 가 정의상
  "초과 누설"** 이라는 것이다.
- **자기방전 편차가 실제로 이 팩에 있었다고 주장하지 않는다.** 원리적으로 안 갈린다고만 적었다.
- **`165_passive` 가 깨진 원인**을 단정하지 않는다 (`ISC_LEAKAGE_DATASET.md` §1·§7).
- **데이터 온도 27.53 °C** 는 두 행 표본이다. 전 구간 통계는 내지 않았다.
- **17 번째 열의 뜻**을 단정하지 않는다.
- **이 논문이 우리 LLI/LAM 결론에 쓰인다고 주장하지 않는다.** 겹침은 문제의 모양과 라벨 설계다.

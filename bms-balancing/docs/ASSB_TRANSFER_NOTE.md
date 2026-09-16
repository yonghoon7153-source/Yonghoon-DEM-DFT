# ASSB 이식 — 가능성 메모 (2026-09-16)

> **보류 항목이다.** 2026-09-16 사용자 결정: **지금 프로젝트가 끝난 뒤에 한다.**
> 이 메모는 "그때 다시 생각할 때 처음부터 안 하도록" 남기는 것이고, 착수 지시가 아니다.
>
> ⚠ **실측과 추론을 갈라 읽어라.** §1 은 **이 저장소에서 돌려 본 것**이다.
> §2·§3 은 **일반 지식에서 나온 추론**이고 우리 실측이 아니다.

## 0. 물음

> 액체셀 α·β 열화 정량화 코드를 **ASSB** 에 적용할 수 있나. 셀이 필요한가.

전제 (사용자, 2026-09-16): ASSB 는 음극이 **Li-In · Li 금속 · 무음극**이다.
**`γ_Si` 블렌드는 쓰지 않는다.**

## 1. 실측 — 코드가 평탄 상대극을 **고치지 않고** 받는다

Li-In(두 상 공존)·Li 금속은 작동 구간에서 **OCP 가 평탄**하다. 그래서 상대극을
상수로 두고 합성셀을 만들어 현행 `Objective` 에 그대로 걸었다. **코드 수정 0** —
`Blend` 의 인터페이스가 `E(x, γ)` · `dv(x, γ)` 둘뿐이라 대체물을 끼우면 된다.

합성: `V(x) = E_PE((x−b_PE)/a_PE) − 0.62 V`, `p = [1.10, −0.06, 1.05, 0.00, 0.25]`,
`w_pocv=1 · w_dvdq=1 · w_dqdv=0`. `rmse_pocv(p_true) = 2.220e-17` (표현 오차 0).

| 흔든 축 | 크기 | `Δ obj` | 읽기 |
|---|---:|---:|---|
| `a_PE` | +0.02 | **+2.204e-01** | 잘 정해진다 |
| `b_PE` | +0.02 | **+4.399e-01** | 잘 정해진다 |
| `a_NE` | +0.20 | **+0.000e+00** | **데이터가 아무 말도 안 한다** |
| `b_NE` | +0.20 | **+0.000e+00** | 〃 |
| `γ_Si` | +0.20 | **+0.000e+00** | 〃 |

**5 → 3 붕괴가 실측으로 확인됐다.** 세 축의 민감도가 **정확히 0** 이다 (근사가 아니다 —
평탄 상대극에서는 `E_NE((x−b)/a)` 가 `a`·`b`·`γ` 와 무관한 상수라 해석적으로도 0이다).

**따라서 액체셀에서 우리를 가장 괴롭힌 축퇴 — `LAM_NE ↔ γ_Si` 보상 — 은 ASSB 에서
사라진다.** 측정이 어려워지는 게 아니라 **개념이 없어진다** (음극에 잃을 활물질이
과잉 Li 거나 아예 없다).

### 1-1. 그러나 현행 코드를 그대로 돌리면 안 된다

식별 불가 축 셋이 남아 있으면 optimizer 가 그 위를 헤매다 **상자 벽에 붙는다.**
`LB5`/`UB5` 가 5-벡터로 박혀 있고 `degradation_modes` 가 `p[0..3]` 을 쓴다.
→ **파라미터를 3 개로 줄인 판이 필요하다.** 작업량 자체는 작다.

`degradation_modes` 도 **재정의**가 필요하다 — `LAM_NE` 는 정의가 없고,
무음극에서 `LLI` 는 사실상 `b_PE` 의 **밀기** 하나다.

## 2. `[추론]` 어려움이 옮겨 가는 세 자리

없어진 축퇴 대신 생기는 것. **우리 실측이 아니다.**

| ID | 후보 원인 | 왜 OCV 로 못 가르나 |
|---|---|---|
| **A1** | **접촉 손실 / 퍼콜레이션** (복합양극 NCM+SE+카본) | 활물질이 SE 와의 접촉을 잃으면 **용량이 준 것처럼 보이는데 물질은 그대로**다. `a_PE` 를 직접 오염시킨다 → **`LAM_PE ↔ 접촉 손실` 이 새로운 최악의 축퇴** |
| **A2** | **Li-In 기준 전위 이동** | 평탄한 것은 **두 상 공존 영역 안에서만**이다. In 소모·조성 이탈이면 기준이 움직이고, 그것은 전체 곡선의 **밀기** — **`LLI` 와 같은 모양** |
| **A3** | **dead Li ↔ SEI Li** (무음극) | 둘 다 "재고에서 빠진 Li" 라 OCV 에 똑같이 들어온다 |

**그리고 전부 PE 곡선 모양에 달려 있다.** NMC 는 기울기가 있어 `a_PE`/`b_PE` 가 갈린다.
**LFP 는 평탄해서 논문 20 의 `(X1, X3)` 축퇴가 그대로 온다** —
`NEW_MODEL_REQUIREMENTS.md` §2 · `LIT_19_20_FOR_NEW_MODEL.md` §2-3 의 그것이다.

## 3. `[추론]` 셀이 필요한가 — 두 단계로 갈린다

**1단계 (식별성 판정) → 셀 0 개.** 3-파라미터면 우리가 이미 한 5-파라미터보다
**작은 문제**이고 기계는 그대로다. 물음이 하나로 좁혀진다:

> **무음극·Li-In ASSB 에서 OCV 적합이 `LAM_PE` 와 `접촉 손실`(A1) 을 가를 수 있는가?**

**그리고 이 저장소에 그 재료가 이미 있다.** DEM/MPM 이 복합양극의 **접촉 수·
퍼콜레이션**을 준다 — OCV 적합이 **못 보는 바로 그 양**이다.
⚠ DEM/MPM 계열(`kit_*` `ps_zips` `se_curve` `run_mpm.sh`)은 **다른 브랜치 소유**다
(루트 `CLAUDE.md` 하드룰 1). 이 메모는 **참조만** 하고 건드리지 않는다.

설계 골자: **DEM 이 예측한 접촉 손실 → 합성 forward model 에 주입 → OCV 적합이
되찾는지 본다.** 셀이 필요 없다. 답이 "못 가른다" 로 나오면 **"ASSB 열화 진단은
OCV 만으로 부족하고 미시구조 관측이 필요하다"** 가 **측정으로** 선다.

**왜 이게 액체셀보다 결론을 낼 수 있나**: 액체셀에서는 우리가 **measured 라벨이
없다**는 데서 막혔다 (`NEW_MODEL_REQUIREMENTS.md` §5 · §8-6). ASSB 의 A1 은
**DEM 이 독립 관측을 줄 수 있는 유일한 자리**다.

**2단계 (실셀 주장) → 셀 필요.** 그리고 **A2(Li-In 기준 안정성)를 반드시 통제**해야
한다 — 안 잡으면 LLI 숫자 전체가 의심스러워진다. **압력도 통제 변수**다
(액체셀에 없던 것). 그리고 접촉 손실의 **독립 라벨**이 없으면 §5 의 "라벨 출처"
문제가 그대로 반복된다.

## 4. 재사용 표 — 무엇이 넘어가나

| 층 | 이식 | 근거 |
|---|---|---|
| **하네스** (계약·서명·validator·난간·**폭 측정기**) | ✅ 거의 그대로 | 화학 무관. "출처를 붙이고 답이 유일한지 잰다" 는 어떤 적합에도 붙는다 |
| **forward model** (`E_PE − E_NE`, 아핀) | ✅ 구조는 그대로, **상대극만 교체** | §1 실측 — 코드 수정 0 으로 돌았다 |
| **파라미터 상자** (`LB5`/`UB5`) | ⚠ **3 개 판 필요** | §1-1 |
| **`degradation_modes`** | ❌ **재정의** | `LAM_NE` 가 없다 |
| **`γ_Si` / `fit_gamma_si` / `Blend`** | ❌ **안 쓴다** | 섞을 게 없다 |

## 5. 이 메모가 말하지 않는 것

- ASSB 셀의 실제 pOCV 를 **본 적이 없다.** §1 은 우리 합성 PE 곡선에 평탄 상대극을
  붙인 것이지 ASSB 자료가 아니다.
- **접촉 손실을 어떤 형태로 모델에 넣을지** 정하지 않았다 (용량 축 스케일? 별도 칸?).
  그것이 정해져야 §3 의 1단계가 설계된다.
- 우리 DEM 산출이 **어떤 접촉량을 어떤 단위로** 주는지 확인하지 않았다 (다른 브랜치).
- `chain rule` 결함(`dv_cell` 에 `1/a` 없음)은 **여기에도 그대로 따라온다.**
  이식할 때 같이 정리하지 않으면 새 프로젝트가 그 편향을 물려받는다.

---

## 6. 논문 수집 큐 (2026-09-16 개설 — 이 절이 큐의 정본이다)

사용자가 PDF 를 모아 **하나씩** 먹인다. 대화는 휘발성이므로 여기를 본다.
위키 쪽 정본은 `wiki/questions/assb-contact-loss-vs-lampe.md` 의 **Q1~Q8 채움표**이고,
이 절은 **아직 안 들어온 것**의 목록이다.

> ⚠ **순차로만 돌린다.** `wiki/tools/hooks/lint-on-edit.sh` 가 **전체 위키**를 lint 하므로
> 두 에이전트를 동시에 띄우면 서로의 미완성 페이지 때문에 빨개진다. 한 편에 ~18 분.

### 6-1. 처리 상태

| # | 논문 | 축 | 상태 |
|---|---|---|---|
| 01 | Bielefeld·Weber·Janek 2019 — Microstructural Modeling | Q1 | ✅ **흡수 완료** (`81aa240`) |
| 02 | Clausnitzer 외 2023 — Structure-Resolved Simulations (+SI) | Q1·**Q8** | ✅ **흡수 완료** (`2a2975ca`) |
| 03 | Role of grain-level chemo-mechanics 2024 (+SI) — **DAMASK v2.0.2** | Q1 | ⏸ 수령·대기 |
| 04 | Shi·Zhang·Tu 외 — Characterization of mechanical degradation (+SI) | Q1 | ⏸ 수령·대기 |
| 05 | **Doux 2020** — Stack Pressure Considerations (Adv. Energy Mater., DOI `10.1002/aenm.201903253`) · 본문 6p `f1fc5062a6e259cd` · SI 8p `daa3b7a141c2f571` | **Q6** | ⏸ 수령·대기 |
| 06 | **Lee 외 2020** — Ag–C 무음극 (**Samsung SAIT**, Nature Energy `10.1038/s41560-020-0575-z`) · 본문 10p `3452770465c31f45` · SI 18p `120d136d99668016` | **Q7** | ⏸ 수령·대기 |
| 07 | **Spencer-Jolly 외** — Structural changes in the Ag–C composite anode interlayer (**Joule** vol. 7) · 본문 13p `a59c7405b40a1f42` · SI 6p `28eddf6139c1b529` | Q7 | ⏸ 수령·대기 |
| 08 | From state estimation to active intelligence (**Frontiers in Chemistry**, `10.3389/fchem.2026.1960882`, Mini Review, 2026-09-15 게재) · 12p `a54b551671eea230` | Q3·Q4 | ⏸ 수령·대기 |
| 09 | **Huo 외** — Characterization of cathode degradation + **결합 전기화학-노화 모델** (sulfide ASSB, *JPS*) · 11p `9f2496907f7e65a0` | **Q2 · 전압축** | ⏸ 수령·대기 · **권장 1순위** |

| 10 | **Vadhva·Hu·Johnson·Stocker 외** — EIS for ASSB: Theory, Methods and Future Outlook · 18p `537a508716afd2b3` | **Q2 독립 관측** | ⏸ 수령·대기 |
| 11 | Sadegh Kouhestani 외 — PHM of Solid-State Batteries (*Energies* 2022) · 26p `912b3d1df0233ba4` | Q3·Q4 | ⏸ 수령·대기 |
| 12 | Zheng 외 — ASSB for the grid: A realistic appraisal · 10p `496f3b4580a81b9b` | Q3·Q4 | ⏸ 수령·대기 |
| 13 | **Maxwell Protocol for Non-Destructive Health Diagnosis** (*Angew. Chem. Int. Ed.* 2025, 64, e202514910, **Hot Paper**) · 본문 9p `fa35a5cdd5d3fcec` · **SI(.docx)** `ce0b9a35c96ef99c` | Q3·Q4 · **OCV 경쟁 접근** | ⏸ 수령·대기 |
| 14 | Enhancing RUL in Solid-State Batteries: Smart BMS (IISE Annual Conf. 2024) · 6p `0d99b00e6e8907a7` | Q3·Q4 | ⏸ 수령·대기 · **01 번을 인용한다** |

> ⚠ **보충자료가 아닌 파일 둘**: `07 Sup1`(2p)과 `09 Sup`(.docx)은 **학술지 제출
> 체크리스트/데이터 보고 양식**이지 내용이 아니다. 에이전트가 시간을 쓰지 않게 한다.
> `07` 의 진짜 보충자료는 **Sup2**(6p, *"Joule, Volume 7 Supplemental information"*)다.
> 반대로 **`13` 의 .docx 는 진짜 Supporting Information** 이다 (Wiley-VCH) — 읽어라.
>
> ⚠ **`.docx` 는 `pymupdf` 로 안 열린다.** `zipfile` 로 `word/document.xml` 을 풀어
> 태그를 걷어내면 본문이 나온다 (이 절의 지문도 그렇게 확인했다).

### 6-2. 사용자가 수집해 둔 것 (업로드 대기)

| # | 논문 | 겨냥하는 축 |
|---|---|---|
| 05 | **Doux 2020** — Stack Pressure Considerations (+SI) | **Q6 압력** |
| 06 | **Lee 2020** — High-energy long-cycling ASSB, Ag–C 복합 음극 (+SI) | **Q7 무음극** |
| 07 | Structural changes in the Ag–C composite anode (+SI ×2) | Q7 열화 경로 |
| 08 | From state estimation to active intelligence (Frontiers 2026) | Q3·Q4 "빈 자리" |
| 09 | **Huo 외 2025** — Characterization of cathode degradation + **결합 전기화학-노화 모델** (+SI) | **Q2 · 전압축** |
| 10 | **Vadhva 외 2021** — EIS for ASSB: theory, methods, outlook | **Q2 독립 관측** |
| 11 | PHM of Solid-State Batteries (Energies 2022) | Q3·Q4 |
| 12 | ASSB for the grid: A realistic appraisal (Energy 2026) | Q3·Q4 |
| 13 | Maxwell Protocol for Non-Destructive Health Diagnosis (Angew 2025) | Q3·Q4 · **OCV 경쟁 접근** |
| 14 | Enhancing RUL in Solid-State Batteries: Smart BMS (2024) | Q3·Q4 |

### 6-3. 추가 수령분 15~24 — **번호는 사용자 업로드 순서가 정본이다**

⚠ 2026-09-16: 내가 붙여 둔 후보 번호(15=Strauss·16=Koerver…)와 **사용자 파일 번호가
충돌**했다. 디스크의 PDF 가 사용자 번호를 달고 있으므로 **사용자 번호를 정본으로** 맞췄다.
아직 안 온 후보(6-3-b)에는 **번호를 붙이지 않는다** — 올라올 때 사용자가 정한다.

| # | 논문 | 겨냥 | 쪽·sha256 (본문 / SI) |
|---|---|---|---|
| **15** | **Ramanayagam·Miß·Leier** — Stack Pressure 가 ASSB 양·음극 임피던스에 미치는 영향, **3전극** 측정 (*Batteries & Supercaps*) | **Q2+Q5+Q6 교차** | 10p `5ce9a4259bdf46d0` / 6p `4b6180aacf267b3e` |
| **16** | **Yanev·Heubner·Nikolowski 외** — Editors' Choice: **Li-In 합금 음극**의 동역학 한계 완화 (*JES*, **open access**) | ★ **Q5** | 8p `8fb10ec47e613614` / 2p `5e3fdd576b865b2d` |
| **17** | **Fukunishi·Tabuchi·Ikezawa·Okajima 외** — **NCM523** 복합전극 3전극 AC 임피던스와 **열화** 거동 (*JPS* **564** (2023) 232864) | **Q2 + 양극 열화** | 10p `c0798ee510063429` / 6p `773e6fbca1d7b938` |
| **18** | **Yoshida·Ikezawa·Okajima·Arai** — 전고체 **4전극** 셀 (*Electrochim. Acta* **497** (2024) 144523, open access) | **Q5** — *"상대극 전위 변화가 선형이 아니다"* | 9p `a991f5351cb61a20` / 9p `774a121241a8d2dc` |
| **19** | **Chang·Choi·Kang·Park·Lim** — **매립 In 기준전극**으로 ASSB 제한 인자 규명 (*Ionics*, Short Comm.) | **Q5·Q2** — 전극별 전위 **동시 분리 측정** | 7p `b0c03e8eaeaa3521` / — |
| **20** | **Sedlmeier 외** — ASSB 파우치셀용 **미세 기준전극**, 전극 분해 임피던스·전위, **In-Li 음극** 적용 (*JES*, **open access**) | **Q5·Q2** | 13p `fb40909f2bfc4a98` / — |
| **21** | ★ **Strauss·Bartsch·de Biasi·Kim·Janek·Hartmann·Brezesinski** — **Impact of Cathode Material Particle Size on the Capacity of Bulk-Type ASSB** (*ACS Energy Lett.* 2018, 3, 992−996) | ★★ **Q2 의 measured 라벨** — 01 의 ref 13. **ex situ XRD 의 inactive AM 분율 = `1 − θ_AM`** | 5p `d3fa26699f0e158b` / 8p `5b23a700e4b26e29` |
| **22** | ★ **Koerver·Aygün·Leichtweiß·Dietrich·Zhang·Binder·Hartmann·Zeier·Janek** — **Capacity Fade in Solid-State Batteries** (*Chem. Mater.* 2017, 29, 5574−5582) | ★★ **접촉 손실의 실험 원전 + 전압·용량축** — 01 의 ref 7 | 9p `5be652c4d8383b90` / 7p `96534ee472de4205` |
| **23** | **Stavola·Sun·Guida·Bruck 외** — Thick NMC111-Argyrodite 양극의 **리튬화 구배·굴곡도** (*ACS Energy Lett.* 2023) | **Q1·Q2** — 01 이 "두께 효과는 유한 크기 인공물" 이라 한 자리를 **실측**으로 친다 | 8p `3b05d0e6a4f695e7` / **29p** `0e810a3fa2f097dc` |
| **24** | **Zhou·Lu·Mish·Chen·Feng·Kim 외** — Tailored Cathode Composite Microstructure, **저압 장수명** (*ACS Energy Lett.* 2025) | **Q1·Q6** — DEM 브랜치에 `tailored_cathode_low_pressure.csv` 앵커가 이미 있다 | 9p `107089537e2fc03f` / **30p** `56af662bea394b9c` |

| **25** | **"Introducing a new model for solid-state batteries: Parameter estimation and sensitivity analysis on diffusion, concentration, and electrochemical kinetics"** (*Electrochim. Acta* 2024) | **Q4 확인용** | 18p `a7f04355b1eb13b5` |
| **26** | **"Analysis of the Validity of P2D Models for Solid-State Batteries in a Large Parameter Range"** (*JES*, **open access**) | **Q4 확인용** | 14p `17507c15ac755444` |
| **27** | **Bizeray·Kim·Duncan·Howey** — Identifiability and Parameter Estimation of the **Single Particle** Li-ion Battery Model (*IEEE TCST* **27**(5) 2019, 1862) | **방법론 원전 (액체셀)** | 16p `714992e6e46adbc4` |
| **28** | **"Quantifying Resistive and Diffusive Kinetic Limitations of Thiophosphate Composite Cathodes in ASSB"** (*JES*, **open access**) | ★ **`η(i)` 항 그 자체 + OCV 곡선 최유력** | 11p `c0fc33c717c16634` |
| **29** | **Park, B.-N.** — Unraveling Asymmetric Electrochemical Kinetics in **Low-Mass-Loading** NMC111 Li-Metal ASSB | Q8 보조 | 10p `9a213dfb1f39b963` |

**★★ 25~29 의 단어 지문 — Q4 의 답이 거의 보인다** (digest 가 정본이고 이건 예비 지표다):

| | `identifiab` | `uniqu` | `sensitiv` | `Sobol` | `GITT` | `OCV` |
|---|---:|---:|---:|---:|---:|---:|
| 25 (제목이 "parameter estimation and **sensitivity analysis**") | **0** | **0** | 3 | 0 | 1 | **0** |
| 26 (**전역 민감도**를 제대로 한다) | **0** | **0** | 26 | **29** | 0 | **0** |
| 27 (액체셀 방법론 원전) | **9** | 3 | 7 | 0 | — | — |
| 28 | **0** | **0** | — | — | **20** | **0** |
| 29 | **0** | 1 | — | — | 0 | **0** |

- **26 은 Sobol 전역 민감도를 29 회 하면서 `identifiab` 은 0 회다.** 우리 위키
  `constrained-crb-identifiability` 가 갈라 놓은 **"민감도 ≠ 식별성"** 의 교과서적 실례다.
- **27 은 `identifiab` 9 회인데 `all-solid-state` 가 0 회다** — 도구는 액체셀에 있고
  **ASSB 로 안 건너왔다**는 것이 지문으로 확인된다.
- **★ 28 이 `GITT` 20 회** — ASSB 준평형 곡선의 최유력 후보. 단 `OCV` 0 · `open circuit` 1 이라
  **GITT 로 재면서 "OCV 곡선" 이라 부르지 않을** 수 있다. digest 로 확인한다.
- ⚠ **단어 수는 지표일 뿐이다.** 그림에 OCV 곡선이 있어도 본문 단어로는 안 잡힌다.
  추출 품질은 확인했다 (쪽당 3,900~5,100 자, 정상).

**★ Q5 가 0 편 → 다섯(15·16·18·19·20)으로 바뀌었다.** Li-In 기준 전위가 움직이면
`LLI` 숫자 전체가 의심스러워지는데, 그 축을 이제 실제로 잴 수 있다.
**★ 21·22 는 01 이 자기 참고문헌으로 가리킨 둘**이다 — `1 − θ_AM` 의 measured 라벨과
접촉 손실의 실험 원전(전압축 포함).

### 6-3-b. 아직 안 온 후보 (번호 없음 — 업로드 시 사용자가 정한다)

| 논문 | 왜 · 누가 가리켰나 |
|---|---|
| Hlushkou 외, *JPS* 2018, 396, 363−370 | 01 ref 16 — **FIB-SEM 실측 미시구조** (합성 기하와 대조) |
| **Ren·Danner·Finsterbusch·Latz 외, *Adv. Energy Mater.* 2022, 2201939** | 02 ref 17. **`θ(N)` 시간축의 입구** — `assb` 2/2 편이 동역학을 안 줬다 |
| **Neumann 외, *ACS Appl. Energy Mater.* 2021, 4, 4786** | 02 ref 38. **GB 저항 모형 원전** + **EIS 로 파라미터화된 measured 라벨**. Q2 |
| **역문제·식별성을 다루는 ASSB 논문 (미특정)** | ★ **구조적 공백.** 흡수분이 전부 **forward 전용**이면 **Q4 는 원리적으로 안 채워진다** |
| **ASSB 의 pOCV / 저율 OCV 곡선이 실린 논문 (미특정)** | ★ **구조적 공백.** 02 의 전압축은 전부 **1 mA/cm²(≈0.74 C) 부하 곡선**이고 **OCV 곡선은 0 편**이다 |

⚠ 위 둘(미특정)은 "그 논문 한 편" 이 아니라 **지금 목록에 없는 종류**를 가리킨다.
채워지면 그때 실제 서지로 바꿔 적는다.

### 6-4. 처리 순서 — **먹인 순서 그대로** (2026-09-16 사용자 지시, 확정)

```
03 → 04 → 05 → 06 → 07 → 08 → 09 → 10 → 11 → 12
   → 13 → 14 → 15 → 16 → 17 → 18 → 19 → 20 → 21 → 22 → 23 → 24
   → 25 → 26 → 27 → 28 → 29
```

**재배열하지 않는다.** 아래 6-4-a 는 내가 한때 권한 재배열인데 **채택되지 않았다** —
근거로만 남긴다. **27 편 × ~20 분 ≈ 9 시간**이고 순차로만 돈다(lint 훅이 전체 위키를
보므로 병렬 불가). 한 편이 끝날 때마다 **lint 0 errors 확인 → 커밋 → 다음 편 착수**.

### 6-4-a. (채택 안 됨) 내가 권했던 재배열

`03 → 04` (이미 손에 있음) → **`09 Huo`** → `05 Doux` → `06 Ag-C` → `17 Yanev` →
`15 Strauss` → `16 Koerver` → `10 Vadhva` → 나머지.

**`09 Huo` 를 앞으로 당기는 이유**: 지금 가진 것 중 **유일하게 전기화학(전압·용량축)과
양극 열화를 같이 가진** 논문이고, 01 이 세운 **곱셈 축퇴**가 실제 셀에서 어떻게
보이는지를 말해 줄 가능성이 가장 높다.

### 6-5. ⚠ DEM 브랜치에 이미 있는 것과 겹친다 (2026-09-16 조사)

`claude/stoic-knuth-NObVQ` 의 `docs/data/` **169 항목**을 훑었다(읽기만 — 하드룰 1).
우리 Q 축에 직접 걸리는 것이 **이미 디지타이즈돼 있다**:

- **Q6**: `doux2020_stack_pressure` · `cronau2021_stack_pressure_ionic` ·
  `varkey2026_ionic_vs_pressure` · `schneider2023_sigma_size_pressure` · `lee2024_dem_fem_pressure`
- **Q2**: **`minnmann2021_sigma_tau_porosity`** (*"NCM-622 + Li6PS5Cl (= our system). EIS +
  T-type TLM"* — 조성·공극률·압력 × σ_ion/σ_el/tortuosity) · `reisacher2023_percolation`
  (EIS+DC **실험** 퍼콜레이션) · `rint_eis_anchors` (R_ct, 3전극)
- **Q1**: `bielefeld2019_percolation` (01 번의 디지타이즈) · `chen2011_percolation_micromodel`

**앵커 ≠ digest 다.** 그쪽은 그림에서 점을 따 DEM 보정에 쓰는 데이터고, 우리는
**식별 가능성 축(Q1~Q8)으로 절별 독해**한다. 겹치는 것이 아니라 보완이므로
**PDF 는 여전히 필요하다.** 다만 **우선순위는 내려간다** (05 Doux · 10 Vadhva 등).

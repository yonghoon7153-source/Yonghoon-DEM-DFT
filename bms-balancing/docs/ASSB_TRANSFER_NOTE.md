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
  **→ 2026-09-22 정리됨 (⑥, `FINDINGS.md` §1-2-b)**: `Objective` 가 `objective_version ∈ {legacy_matlab, chain_rule_v2}`
  를 **필수**로 받는다(기본값 없음). 이식판은 `chain_rule_v2` 를 명시하면 되고, 편향을 물려받는 것은 이제 **적어 둔
  선택**일 때만이다. 합성 실측: legacy 가 LAM_NE 를 3~7 %p 편향, v2 는 0.5 %p 안 회수 — 다만 상대극이 평탄한 이식판에서
  `a_NE` 축은 데이터가 안 보므로(§1) v2 의 이득은 **`a_PE` 항의 1/a** 에서만 온다.

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
| 08 | From state estimation to active intelligence (**Frontiers in Chemistry**, `10.3389/fchem.2026.1960882`, Mini Review, 2026-09-15 게재) · 12p `a54b551671eea230` | Q3·Q4 | ✅ **흡수 완료** (`c90b7f67`) — 칸 0 추가. 실익은 **원 논문 후보 5편**(→ 31~35) 과 **종설 숫자가 우리 원전과 어긋난 실측**(Su 2024) |
| 09 | **Huo 외** — Characterization of cathode degradation + **결합 전기화학-노화 모델** (sulfide ASSB, *JPS*) · 11p `9f2496907f7e65a0` · SI(.docx) `cee297a20e00d37e` | **Q2 · 전압축** | ✅ **흡수 완료** (`dfc1fc78`) — **누적 ≈7.0 → ≈7.5 칸** (Q6 반 칸 + Q3 새 층위 `fitted-single-parameter`). **Q1·Q4 는 여전히 0** 이나 **Q4 의 성질이 세 번째로 바뀌었다**(지문이 자기 표 안에 있다). 새 개념 페이지 `assb-lampe-contact-product-degeneracy`. 후속 후보 1·2·3 순위 → **36·37·38** |

| 10 | **Vadhva·Hu·Johnson·Stocker 외** — EIS for ASSB: Theory, Methods and Future Outlook · 18p `537a508716afd2b3` | **Q2 독립 관측** → ★ **Q4 재조준** | ✅ **흡수 완료** (`5e4cf103`, assb 10호) — Q4 를 깼다, 단 "쟀다" 가 아니라 "분야가 비유일성을 명제로 인쇄했다". 9호의 "하나의 원호에서 두 시상수" 는 **38번(DRT, 당김 → 11호 `4aa0bce5`)** 이 받았다 |
| 11 | Sadegh Kouhestani 외 — PHM of Solid-State Batteries (*Energies* 2022) · 26p `912b3d1df0233ba4` | Q3·Q4 | ✅ **흡수 완료** (`21218008`, assb 12호) — **새 칸 0** (누적 ≈8.5/8 유지, Q4 0/12). 1차 측정 0 · 그림 7장 전부 타 논문 재수록(SSB 데이터 그림 0) · Table 1 의 SSB 실측 SOH/RUL 항목 **0/28**. 얻은 것: `[인쇄]` "LAM mainly stems from electrical contact loss" — PHM 어휘에서 **LAM ⊃ 접촉 손실**이 정의다(우리 분리 물음이 정의 차원에서 없는 체계) · `A_eff` 곱 축퇴의 계보 입구(Tian & Qi 2017 → Shao 2022 → 9호 Huo) · "단일 원호 → 이중 원호" 는 "모델 차수 = 상태변수" 의 세 번째 독립 인쇄. 후속 후보 → Tian & Qi 2017 *JES* · Shao 2022 *Energy* · Kim 2019 *EA* 317 |
| 12 | Zheng 외 — ASSB for the grid: A realistic appraisal (*Energy* 345 (2026) 140229) · 10p `496f3b4580a81b9b` | Q3·Q4 → **실제 접점 Q6·Q8** | ✅ **흡수 완료** (`174e14ce`, assb 13호) — **새 칸 0** (Q4 0/13). Perspective, "No data was used", 그림 5장 전부 모식도. 얻은 것: `<5 MPa` 는 8호 `<≈1`·12호 `0.4–1` 에 이은 **세 번째 독립 인쇄(원전 셋 다 다름)** · SOH 를 "true AM loss ↔ usable capacity ↓(임피던스)" 로 가르면서 **접촉 손실의 소속을 안 적음**(12호는 LAM 안, 13호는 미배정 → 분류 체계 셋) · 그리드 창 20–80 % SOC 는 "완전 OCV 불가" 를 스스로 인쇄 → 닻 물음의 적용 창이 설계상 닫힘. 후속 → Li Q. *Nat. Energy* 2025 · Zhang *Nat. Commun.* 2025 (무외압 Si) |
| 13 | **Oh⁺·Kim⁺·Kim·An·Kwon·Choi** — Maxwell Protocol for Non-Destructive Health Diagnosis (*Angew. Chem. Int. Ed.* 2025, 64, e202514910, **Hot Paper**) · 본문 9p `fa35a5cdd5d3fcec` · **진짜 SI(.docx)** `ce0b9a35c96ef99c` | Q3·Q4 · "OCV 경쟁 접근" → **판정: 경쟁이 아니라 OCV 의 관측 추가** | ✅ **흡수 완료** (`4f3886a0`, assb 14호) — **새 칸 0** (Q4 0/14), 층 셋(Q1·Q6·Q8). `E(x)` 를 적합하지 않고 같은 상태함수의 두 편미분을 잰다: `ΔS = −F(∂E/∂T)_P` (엔트로피메트리) · `ΔV = F(∂E/∂P)_T` (volumetry, 10→5 MPa 에서 42.7→34.7 µJ mol⁻¹ Pa⁻¹). ★ **우리 축에 준 실측**: void 2배 셀(공극률 4.5→9.8 %)과 +0.9 %p 셀의 용량 유지율이 86.0 ↔ 84.0 % — **접촉 손실 → 용량 사상이 문턱형**이고 문턱 아래에서 OCV 적합은 `LAM_PE ≈ 0` 을 정확히 보고하며 void 를 **놓친다(무감)**. 분리 후보는 volumetry 이고 엔트로피메트리가 아니다(논문 배치와 반대, 실측 0). 새 개념 `assb-maxwell-ocv-derivative-channels`. 후속 → **Oh…Choi *AEM* 2025**(13호 후속과 같은 연구실, 1순위 승격) · Bielefeld 2022 *JES*(pore 문턱 → 1호 `p_c` 실험판) |
| 14 | **Rahman·Lu** — Enhancing RUL in Solid-State Batteries: Smart BMS (*IISE Annual Conf. Proc.* 2024, 6p) · `0d99b00e6e8907a7` | Q3·Q4 | ✅ **흡수 완료** (`2815e7e1`, assb 15호) — **새 칸 0**, Q4 0/15 (**가장 얕은 0**: 추정기가 없어 역문제를 말할 대상이 없다). 1차 0 · 재인용 수치 0 · **그림 1장(그것도 액체셀 ANN 종설 [16] 에서 통째로 가져온 것)**. `RUL` 5회 전부 초록·키워드·서론, §2~결론 0회. `accuracy` 7 : 정확도 수치 0 : 불확실성 0. ★ **1호 인용 대조 결과 — 어긋난다**: 우리 1호를 "load balancing, SOC estimation, battery health monitoring" 의 근거로 인용하는데 원전에는 **셀 실험도 전압축도 없다**(서지도 2018·"W. Dominik A" 로 틀림). 12호의 자기 감사("SSB 실측 SOH/RUL 0/28")를 인용하면서 한 글자도 안 옮긴다. ★ **분류 체계 세 번째 표본 = 어휘 미도입**(`contact` 0회) → **접촉 손실 구분은 실험 층위에서 강제되고 종합 층위에서 소실된다** (잠정, 표본 3). 후속 → **Asheri 2023 *Comput. Mater. Sci.*** (이 편이 아는 유일한 SSB-ML, "interface damage") · Bielefeld 2020 *ACS AMI* (1호 직계 속편) |

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
| **15** | **Ramanayagam·Miß·Roling** — Stack Pressure 가 ASSB 양·음극 임피던스에 미치는 영향, **3전극** 측정 (*Batteries & Supercaps* **2026**, 9, e70315) | **Q2+Q5+Q6 교차** | 10p `5ce9a4259bdf46d0` / 6p `4b6180aacf267b3e` · ✅ **흡수 완료** (`2ccb1dd9`, assb 16호) — ★ **14편 만에 칸이 움직였다: ≈8.5 → ≈9.5** (Q2 +0.5 전극 분해 관측 · Q5 +0.5 기준극 실측). Q4 는 0/16 이나 성질이 새롭다 — "안 쟀다"도 "낱말이 없다"도 아닌 **"밟고 지나갔다"**. ★★★ **곱 축퇴의 실측 표본**: 식 (4) 가 *"in contact with"* 라 **이름 붙인** 면적을 접촉 분율 없이 완전구 기하로 계산 → 식별되는 것은 `j₀·ε_CAM/r_CAM` 한 조합(9호 `A_eff·ε_p/R_s` 와 같은 자리). 같은 Table 2 의 `Q_DL` 0.18→0.54(3배)를 면적으로 읽으면 **`j₀` 가 1.80 증가 → 0.60 감소로 뒤집히고**, 논문의 *문장*은 둘째 배정인데 *숫자*는 첫째를 쓴다. **우리 처방**: `R_CT·C_dl`(면적 소거) 과 `C_dl`(면적 비례) 을 같이 보고하면 θ 와 j₀ 가 갈린다 — 이 편은 두 값을 다 인쇄해 놓고 조합을 안 만든다. 그 밖: 평탄 OCP 구간 안에서 음극 임피던스가 **15배** 움직인다("무음극/In-Li 는 평탄" 전제가 열역학 축에서만 참) · `D_CAM` 이 압력으로 **3배**(재료 상수가 움직였는데 무언급 — 파라미터 교환 신호) · 두 압력이 **다른 셀**이고 둘 다 389 MPa 제작을 거쳐 97 MPa 은 **필연적으로 하강 분기**인데 대칭 비교처럼 쓴다(5호 이력 물음은 미답) · DRT λ 를 인쇄한 계보 첫 편(C1 통과, C2–C5 실패)인데 **3전극으로 가른 뒤 DRT 가 가법적이지 않다**(부분 4.6 > 전체 3.1). 후속 → Miß 2022 *ACS AMI*(TLM 원본) · Hertle 2023 *JES*(μ-RE 원본, Q5 최대 공백) · **ref [39] = 큐 17번**(이 편의 유일한 외부 실측 대조군이고 열화를 다룬다) |
| **16** | **Yanev·Heubner·Nikolowski 외** — Editors' Choice: **Li-In 합금 음극**의 동역학 한계 완화 (*JES* **171** (2024) 020512) | ★ **Q5** | 8p `8fb10ec47e613614` / 2p `5e3fdd576b865b2d` · ✅ **흡수 완료** (`397057c8`, assb 17호) — ★ **≈9.5 → ≈10.0, 두 편 연속 상승** (Q5 +0.5). Q1·Q4 는 여전히 0. ★★★ **Q5 평탄 전위의 실제 폭을 숫자로 받았다**: 열역학 평탄 `E_CE` 0.61–0.63 V(**±10 mV**) ↔ 과리튬화 **−200 mV**(Li₅In₄·Li₃In₂ 생성 → 컷오프가 4.3 대신 4.1 V) ↔ 국소 고갈 **+680~780 mV**(분리막 쪽 LiIn 고갈 → In-rich 층) = **전체 ≈980 mV**, 양 끝이 모두 "Li-In 음극" 이라 불린 셀이다. `[인쇄]` 저자 스스로 "이 가정은 **실험으로 확인된 적이 거의 없다**". ★★★★ **겉보기 LAM_PE 가 사실은 상대극인 것이 한 셀 안에서 실증됐다** — 3전극으로 보니 **양극 임피던스는 5 % 차로 동일**한데 2전극 용량차는 0.1C 6.6 % · CA 35 %. **율을 낮추면 줄지만 0 이 되지 않는다** → 저율 RPT 가 지우지 못한다. ⇒ 우리 3항 분해에 **네 번째 항이 아니라 축의 원점**이 필요하다: `E_cut^eff = E_cell,min + E_CE(i, x_Li, 제조법)`. `i→0` 극한에서도 `ΔE_CE = +0.73 V` 가 남으므로 "`i→0` 이면 `η→1`" 처방이 그 몫을 `θ_AM`·`Q_material` 로 밀어 넣는다 — 빼려면 **세 번째 전극**이 필요하다. **곱 축퇴 처방 적용은 "불가"**: 등가회로·`R_CT`·`C_dl`·`fit*` 전수 0회(`[인쇄]` "beyond the scope") → 조합을 만들 입력이 없다. 역설적으로 **가장 안전한 편** — 배정하지 않았으므로 잘못 배정할 수 없다(9호 곱을 적합 · 16호 곱 위에서 한쪽 끝 선택 · 17호 곱을 만들지 않음). ⚠ n=1·오차막대 0·조건마다 다른 셀·권장 조성(49 at%)은 전극 분해로 검증된 적 없음(3전극은 40 at%). 후속 → **Santhosha 2019**(0.62 V 가 태어난 자리) · **Nam 2018 *JMCA***(In-rich depletion layer 원전) · **Sedlmeier 2023 *JES***(Li 박 방향 뒤집기 = 16↔17호 대질 검증) — **셋 다 큐에 없다** |
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
| **30** | **"Rapid determination of solid-state diffusion coefficients in Li-based batteries via intermittent current interruption (ICI) method"** (*Nat. Commun.* 2023, `s41467-023-37989-6`, **OA**) · ⚠ **보충 데이터 ZIP 이 사용자 기계에 따로 있다** | ★ **"이 곡선이 얼마나 평형인가"** — `GITT` 94 · `ICI` 100 · `open circuit` 5 · `equilibrium` 4 | 9p `6763cb6487a62a02` / SI 26p `d5033997fdaba3a7` |

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

### 6-3-d. 추가 수령분 31~35 (2026-09-22) — **08 번이 낳은 다섯**

08 번(Frontiers 종설) digest 가 뽑아 낸 원 논문 후보 5편을 사용자가 **그날 바로** 다
올렸다. 번호 31~35 는 사용자 업로드 순서이고 6-3 과 같은 규칙으로 정본이다.
**SI 는 34 번만 있다** — 31·32·33·35 는 본문에 Supplementary/Supporting 선언이 없고
`Data availability` 만 있다 (직접 확인). 즉 이 다섯에 **누락된 첨부는 없다**.

| # | 논문 | 종류·쪽 | sha256(앞 32) | 겨냥 |
|---|---|---|---|---|
| **31** | **Biçer·Aksöz·Bakar·Odabaşı·Vonk·Soares 외** — Solid-State Batteries: Chemistry, Battery, and Thermal Management System, Battery Assembly, and Applications—**A Critical Review** (*Batteries* 2025, **11**, 212, `10.3390/batteries11060212`, CC BY) | **Review** 49p | `055eb542b3b5fb4b575e4b2afe3d0f52` | Q1·Q2 — 08 의 "접촉 손실 ↔ 보통 노화 분리 진단" 요구가 매단 **유일한** 인용 |
| **32** | **Zhang·Fu·Lu·Hu·Xia·Zhang 외, Wang·Sun(교신)** — Challenges and Strategies of **Low-Pressure** All-Solid-State Batteries (*Adv. Mater.* 2025, **37**, 2413499) | **Review** 22p | `6b3ed38fa4666c0986929173792e175b` | **Q6**·Q1 — 24 번(저압 장수명)과 짝 |
| **33** | **Liang·Tao·Shi·Lyu·Ji·Dong·Mo** — **Pulse excitation** for active battery management systems (*npj Clean Energy* 2026, **2**, 16) | ⚠ **Comment** 5p | `30e679dc37e5e7d1233bd48436eb2948` | Q4 설계 축 — 우리 폭 측정기의 **역방향** |
| **34** | **Roman·Saxena·Robu·Pecht·Flynn** — Machine learning pipeline for battery state-of-health estimation (*Nat. Mach. Intell.* 2021, **3**, 447–456) | **Article** 10p **+SI 18p** | 본문 `efab9d462848d75f158e71aef2bd16c6` / SI `b856d5919e0a8b6ad9997c8d899c1f6b` | **Q3** — 08 Table 2 여덟 행 중 **유일하게 신뢰구간을 보고** |
| **35** | **Thelen·Huan·Paulson·Onori·Hu·Hu** — **Probabilistic** machine learning for battery health diagnostics and prognostics—review and perspectives (*npj Mater. Sustain.* 2024, **2**, 14) | **Review** 33p | `5ab976ae18496b268a8a044bf473fc29` | **Q3·Q4** — 불확실성 **보정** |

**★ 단어 지문 — 순서를 다시 매겨야 한다** (digest 가 정본이고 이건 예비 지표다):

| | `identifiab` | `uncertaint` | `conf.interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM`¹ | `degradation mode` | `contact loss` | `MPa` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 31 | **0** | 3 | **0** | 0 | 0 | **0** | 0 | 0 | 1 | **0** | **0** |
| 32 | **0** | **0** | **0** | 0 | 0 | **0** | 0 | 0 | 0 | 4 | **50** |
| 33 | **0** | 3 | **0** | 1 | 0 | **0** | 0 | 0 | 0 | **0** | **0** |
| 34 | **0** | 26 | **10** | 9 | 0 | **39** | 0 | 0 | 0 | **0** | **0** |
| **35** | **0** | **205** | **0** | **53** | **28** | 8 | **5** | **5** | **38** | **0** | **0** |

¹ `LAM` 또는 `loss of active material`. 대소문자 무시 검사도 같이 돌렸다 —
**`identifiab` 은 다섯 편 전부 0 회**이고, `Cramér`/`Fisher` 는 33 번만 2 회, `credible` 은
전부 0 회다.

- **★★ 35 번이 이 다섯의 머리다.** `uncertaint` 205 · `Bayes` 53 · `posterior` 28 ·
  `degradation mode` 38 · `LLI` 5 · `LAM` 5 — **우리 축(열화 모드)과 불확실성 정량을
  한 문서에서 같이 쓰는 첫 자료**다. 08 번이 8/8 편에서 "보정된 불확실성 0" 이라고
  센 그 칸을, 이 편은 `calibrat` 8 회로 직접 다룬다.
- **34 번이 Q3 의 실물이다.** `confidence interval` 10 · `calibrat` 39. 08 Table 2 에서
  유일하게 신뢰구간을 보고한 행의 원전이 맞다는 것이 지문으로 확인된다. **SI 18p** 도 왔다.
- **⚠ 33 번은 원전이 아니라 Comment 5 쪽이다.** 내가 08 digest 를 받아 "active pulse
  원전" 이라고 추천했는데 **틀렸다** — 1 차 측정이 없는 전망 논평이다. Q4 설계 축의
  아이디어는 읽을 값이 있지만 **근거로는 08 번과 같은 급**이다. 순서를 앞으로 당기지 않는다.
- **⚠ 31 번에 `contact loss` 가 0 회다.** 08 번이 "diagnostics capable of distinguishing
  contact loss from ordinary electrochemical aging" 이라는 **요구를 매단 유일한 인용**인데,
  그 인용 대상에 그 낱말이 없다. 08 번 D-계열(인용 어긋남)의 **여섯 번째 사례**로 보이고,
  Q1 은 이 편으로 안 닫힌다. 49 쪽이라 비용도 크다 — 순서를 뒤로 내린다.
- **★ 32 번은 `MPa` 50 회로 Q6 을 실제로 다룬다.** `contact loss` 4 회도 있다. 다만 Review 다.
- ⚠ **다섯 중 1 차 측정 논문은 34 번 하나다.** 31·32·35 는 Review, 33 은 Comment.
  즉 **Q1(양극 접촉 손실 정량)과 Q4(유일성)의 0 은 이 다섯으로 깨지지 않을 가능성이
  높다** — 깨는 것은 여전히 21·22·23·28 쪽(1 차 측정)과 25·26·27(방법론)이다.

**아직 안 온 것 (2026-09-22 기준)**: 08 번이 인쇄한 `<≈1 MPa` 산업 요구치의 출처
**Xu, H.·Yang, S.·Li, B. (2024) — "Pressure effects and countermeasures in solid-state
batteries: a comprehensive review", *Adv. Energy Mater.* 14, 2303539,
`10.1002/aenm.202303539`** 는 아직 없다. ⚠ 그것도 Review 이므로 32 번과 겹친다 —
**32 번을 읽은 뒤에 필요한지 다시 판단**하는 게 맞다. 그 밖 미수령 후보는 6-3-b.

### 6-3-e. 추가 수령분 36~37 (2026-09-22) — **9호(Huo 2025)가 낳은 둘, 그리고 둘 다 1·2 순위였다**

09 번 digest 가 뽑은 후속 후보 1·2 순위를 사용자가 **그날 바로** 올렸다. 8호가 낳은
31~35 와 달리 이 둘은 **9호가 자기 본문에서 위임하거나 기각한 논문**이므로 성격이 다르다 —
**재인용 지도가 아니라 원전 추적**이다.

| # | 논문 | 종류·쪽 | sha256(앞 32) | 겨냥 |
|---|---|---|---|---|
| **36** | **Li, Fan, Zhang(교신), Han, Wang, Liu, Jia, Guo, Zhu, He** — Modeling of an all-solid-state battery with a **composite positive electrode** (*eTransportation* **20** (2024) 100315, Elsevier) | **Article** 15p **+ SI(.docx)** | 본문 `abab37041fc1f1982a6100150b8fabdd` / SI `20f8d0c333ef7fe8ff35fd12ff4dc06e` | ★★★ **9호가 모델·PSO·해법·`A_eff` 정의를 전부 위임한 곳.** 같은 연구실·같은 셀 계열 (9호 저자 8/10 중복). 9호 digest 의 공백 G1(OCP 출처)·G2(provenance)·G4(PSO 설정)의 답이 여기 있을 가능성이 가장 높다 |
| **37** | **Conforto, Ruess, Schröder, Trevisanello, Fantin, Richter, Janek** — Editors' Choice: **Quantification** of the Impact of Chemo-Mechanical Degradation on the Performance and Cycling Stability of NCM-Based Cathodes in Solid-State Li-Ion Batteries (*J. Electrochem. Soc.* **168** (2021) 070546, **OPEN ACCESS**) | **Article** 12p | `256d89b805dd0d52f15858e65256f6f3` | ★★★ **Q1 을 깰 1 순위.** 9호가 `[인쇄]` "정량한 몇 안 되는 문헌" 으로 지목하고 `[인쇄]` "the error … is relatively large" 로 **기각한다** — 그 오차의 크기를 우리가 직접 봐야 한다. 방법이 **relaxed OCP + EIS-PSD** 라 **우리 축(OCV 기반)과 직결**. Janek 그룹(22 번 Koerver 2017 과 같은 계보) |

**★ 36 번의 SI 는 텍스트가 1,136 자뿐이고 실체는 그림이다.** `zipfile` 로 열면
`word/media/image1.png`(★ **Supplementary note 1: SEM image of NCM811**) +
`image2~5.wmf`(수식 4 개)다. **텍스트만 긁으면 SI 의 유일한 데이터를 놓친다** —
`word/media/image1.png` 를 꺼내 **직접 봐야 한다**. (09 번 SI 는 제출 체크리스트라
내용이 없었지만 **36 번 SI 는 내용이 있다** — 반대 경우다.)

⚠ **36 번에 산업체 공저자가 있다** (Minghui He, *Shanghai Firm-lithium New Energy
Technology Co., Ltd.*) — 비공개 파라미터의 사유가 여기일 수 있다. 9호가 6 개 값을
`[인쇄]` "not disclosed" 한 것과 같은 계열인지 확인할 자리다.

| **38** | **Yu(교신), Choi, Dunham, Ghahremani, Liu, Lindemann, Garver, Barchiesi, Farahati, Kim(교신)** — **Time-resolved** impedance spectroscopy analysis of aging in sulfide-based ASSB full-cells using **distribution of relaxation times** (*J. Power Sources* **597** (2024) 234116) | **Article** 8p **+ SI(.docx)** | 본문 `407b42abfe5275791998a7acf9b1a8f6` / SI `fd7ffdc06ebd5280d17a7c203083248d` | ★★★ **9호 §5.1 의 "하나의 원호에서 두 시상수" 를 가르는 도구.** 9호가 자기 논거("접촉 손실이 심했다면 EIS 변화가 더 컸을 것")의 근거로 **두 번 인용**한다. **8호(Li 2026)의 DRT 처방**과 **10호(Vadhva 2021, EIS 방법론)** 와 **한 자리에서 만난다** |

**★ 38 번 SI 는 내용이 있다** — 텍스트 7,739 자 + `word/media/image1~5.png` **5 장**.
36 번과 같은 방식(`zipfile` → `word/document.xml` + `word/media/`)으로 둘 다 꺼내야 한다.

⚠ **38 번도 산업체 주도다** (Schaeffler Transmission Systems LLC + Ohio State).
36 번(Shanghai Firm-lithium)에 이어 둘이므로, **비공개 파라미터의 사유가 산업 소속인지**
두 편을 대조해 볼 수 있다.

**★★ 9호가 낳은 후속 후보 1·2·3 순위가 전부 도착했다 (36·37·38).** 세 편이 각각
9호의 다른 구멍을 겨냥한다 — 36 = 모델·PSO·`A_eff` 정의의 원전(공백 G1·G2·G4) ·
37 = Q1 정량(relaxed OCP + EIS-PSD, 9호가 기각한 오차의 크기) ·
38 = §5.1 EIS 축퇴를 가르는 도구(DRT).

**왜 이 셋을 순서 규칙의 예외로 볼 여지가 있는가 (판단은 사용자)**: 31~35 는 8호의
**재인용 지도**여서 늦게 읽어도 손실이 없다. 그러나 36·37·38 은 **이미 흡수한 9호의
공백을 직접 메우는 원전**이고, 특히 36 번은 9호 digest 가 **12 개 공백(G1~G12)의
답이 여기 있을 것**이라고 적어 둔 곳이다. 9호의 기억이 살아 있는 동안 읽는 것이
싸다. 그리고 **38 번은 10 번(Vadhva EIS 방법론)과 짝으로 읽는 것이 가장 싸다** —
10 번이 지금 처리 중이므로 이 짝은 **시간이 지나면 값이 떨어진다**.
**그래도 6-4 의 순서 규칙(먹인 순서)이 지문·편의보다 위이므로 꼬리에 붙였다** —
당길지는 사용자가 정한다.

### 6-3-f. 39 번 (2026-09-22) — ⚠ **이 큐에서 유일하게 `assb` 가 아니다**

사용자가 논문 세미나에서 받은 것. **먼저 데이터셋이 오고 논문이 나중에 왔다** —
데이터셋 조사는 이미 끝나 있다: `docs/ISC_LEAKAGE_DATASET.md`.

| # | 논문 | 종류·쪽 | sha256(앞 32) | 겨냥 |
|---|---|---|---|---|
| **39** | **Lai, Ke, Tang(교신), Zheng** — **Balanced capacity-based quantitative method** for detecting **internal short circuits** in Lithium-ion battery **modules** (*J. Energy Storage*, Research Papers, doi `10.1016/j.est.2025.116622`) · 상하이이공대 + **링난대(홍콩)** | **Article** 9p | PDF `aef3b36ad07da00265a761de4e3f5bec` (ZIP `49dff1db2587383b2aeae5ca28ec36ef`) | **결함 검출·정량** · **라벨 출처** · **Q4 유일성** |

⚠⚠ **태그 주의: 이 논문에 `assb` 를 붙이면 안 된다.** 액체셀 **모듈/팩** 논문이다
(`wiki/SCHEMA.md` 의 `assb` 경계 규칙 — "액체셀 계열 페이지에 이 태그를 붙이지
않는다"). 01~38 과 축이 다르고, Q1~Q8 채움표에도 **넣지 않는다**.

**★ 교신저자가 데이터셋 저장소의 주인이다** — `xtangai` = Xiaopeng Tang.
논문 첫 장의 `Dataset link` 가 `https://github.com/xtangai/EST-D-24-12331` 로
우리가 조사한 그 저장소를 정확히 가리킨다.

**★★ 낱말 지문 — 제목이 "quantitative" 인데 Q4 축이 전부 0 이다** (9 쪽 전수):

| `identifiab` | `uniqu` | `confidence interval` | `uncertaint` | `error bar` | `condition number` | `Fisher` | `regulariz` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| **0** | **0** | **0** | **0** | **0** | **0** | **0** | **0** |

(대조: `ISC` 49 · `leakage` 39 · `balanc` 79 · `passive` 28 · `active` 28 ·
`sensitiv` 11.) `[해석]` **`assb` 9/9 편에서 본 것과 같은 모양이 액체셀 팩
진단에서도 반복된다** — 다만 이것은 **예비 지표**이고 digest 가 정본이다.

#### 6-3-f-1. ★ 별도 섹션 설계 (2026-09-22 사용자 결정 — **착수 전에 이것부터 고정한다**)

**사용자 지시: "38 다음에 39 를 진행하고 이는 `assb` 랑 다른 섹션으로 해."**

`assb` 섹션이 2026-09-16 에 만들어진 방식을 그대로 따른다 (`wiki/SCHEMA.md` 의
`assb` 시드 선언 — 사용자 결정 + 경계 규칙 + 닻 페이지 한 장). 그것이 이 위키에서
섹션을 여는 유일한 선례다.

| 항목 | 값 |
|---|---|
| **새 태그** | `pack-fault` |
| **뜻** | 팩·모듈 레벨 **결함 검출** — 내부단락(ISC)·누설 전류·불균형, 그리고 **균등화가 그 위에 겹치는 문제**. **액체셀 팩**이다 |
| **닻** | `wiki/questions/isc-detection-vs-balancing-masking.md` (신설) |
| **경계 ①** | **`assb` 를 같이 붙이지 않는다.** 액체셀 팩이고 01~38 과 축이 다르다 |
| **경계 ②** | **열화 모드 지분(LLI/LAM) 페이지에 이 태그를 붙이지 않는다.** 결함 **검출**과 모드 **정량**은 다른 물음이다 — 섞으면 "무엇이 무엇의 근거인가" 를 다시 못 가른다 |
| **Q 축** | `assb` 의 Q1~Q8 을 **쓰지 않는다.** 이 섹션은 자기 물음 목록을 새로 연다 |

⚠ **태그 승격 기준(`SCHEMA.md`: 페이지 3 개 이상 모일 주제만)을 어떻게 맞추나.**
지금 확실한 것은 두 장이다 — 닻 카드 + 39 번 digest. 세 번째 후보는
`docs/ISC_LEAKAGE_DATASET.md` 를 근거로 한 **데이터셋 entity** 페이지다
(공개본이 깨져 있다는 실측과 재현 명령이 거기 있고, 위키에는 **참조만** 한다 —
mothership 특칙). **셋이 안 모이면 태그를 만들지 말고 닻 한 장으로 둔다** —
39 번 에이전트가 판단해서 보고한다.

**닻 카드가 물을 것 (초안)**:

> **팩에서 내부단락/누설을 검출·정량할 때, 균등화 전류가 그 관측을 덮는가.
> 덮는다면 무엇으로 가르는가.**

이것이 우리 본진과 **모양이 같은** 물음이다 — 두 원인(누설 vs 자기방전·용량 편차)이
같은 관측을 만들고, 그 위에 **조작(균등화)이 겹친다**. 다만 **물리량이 다르다**
(결함 검출 ≠ 열화 모드 지분). 그 구분을 닻 카드 머리에 박는다.

**에이전트에게 반드시 넘길 것**: `docs/ISC_LEAKAGE_DATASET.md` §5 의 **미해결
물음 7 개**. 그 문서는 **논문 없이 데이터만 보고** 쓴 것이라 7 개가 열려 있다 —
39 번 digest 가 그것을 닫아야 한다. 특히 ① ISC 저항이 셀 1 에 달렸는가(데이터는
그렇게 보인다) ② 17 번째 열이 무엇인가 ③ `165` 조건이 왜 3.5 배 긴가
④ 누설 전류를 **직접 측정**했는가 저항값에서 계산했는가(= 라벨 층위)
⑤ **검출인가 정량인가, 그리고 유일성을 다루는가**.
그리고 **공개 데이터셋의 `165_passive.xlsx` 가 깨져 있다**는 우리 실측을 논문
서술과 대조하게 한다 — 논문이 그 조건을 쓴다면 **재현 불가**다.

### 6-3-c. ⚠ 30 번의 보충 데이터 ZIP — **30 번 에이전트에게 반드시 넘길 것**

사용자 기계 `C:\Users\Administrator\Downloads\30. Sup) …zip` (82 MB, **이중 압축** —
안에 `zenodo.zip` 하나). 2026-09-16 에 WSL 로 훑었다. **저장소에 넣지 않는다**
(1.4 GB 원자료).

| | |
|---|---|
| 구성 | `.mpt` 10 개 **1,436 MB** (Bio-Logic EC-Lab 원시 계열) · `.xy` 54 (operando XRD) · `.R` 8 · `.inp` 9 (TOPAS) · `.csv` 1 |
| 셀 | ⚠ **액체다.** README 에 *"the **wetting** and 3 precycles"* — 전해액 적심이다. **ICI 검증은 액체셀에서 했다** |
| 구조 | ★ **3전극** (`three.electrode = TRUE`) — `E` 셀전압 · **`E_p` 양극 vs 기준** · **`E_n` 음극 vs 기준** 이 **분리돼 있다** |
| OCP | ★ **`E4` = 휴지 끝 이완 전위 = 준평형 OCP.** `E0` = 직전 사이클의 `E4`. **전극별 pOCV 가 있다** |
| ★★ | **같은 원시 데이터를 두 분석 창으로 처리해 둘 다 보관** — `gitt_1`(5–40 s) vs `gitt_1_150`(50–150 s). **"얼마나 평형인가" 를 그들이 변수로 만들었다** |
| ⚠ 함정 | `data_processing.R` 에 **`A = 1.5e4 cm²/g` 가 상수**로 박혀 있다 (`constant <- 4/pi*(V/A)^2`). **접촉 면적 고정 가정**이고 `D ∝ 1/A²` 이라 **제곱으로** 들어간다 |
| 도구 | `impedanceR` (github.com/mjlacey) → Lacey 계열로 보인다 |

**★ 우리 축에 걸리는 이유 셋**

1. **3전극 + `E_p`/`E_n` 분리**는 우리 α·β 가 완전지 곡선에서 **풀어내려는 바로 그 것**이
   측정으로 이미 갈라져 있는 경우다. "적합이 맞았나" 를 댈 수 있는 형태다.
2. **두 분석 창을 둘 다 보관**한 것은 액체셀 쪽 `U2`(pOCV 가 원자료인가 필터본인가)의
   **실험적 대응물**이다. 창을 바꾸면 답이 얼마나 움직이는지 **비교 자료가 이미 있다.**
3. ⚠ **`A` 상수 가정이 우리 `θ` 논의와 직결된다** — `θ` 가 줄면 유효 접촉 면적이 줄고,
   그러면 이렇게 뽑은 `D` 가 **과대평가**된다. 논문이 이 의존성을 다뤘는지가 digest 의 질문.

#### 6-3-c-1. `functions.R` 조회 결과 (2026-09-16)

**① GITT 와 ICI 는 같은 원시 데이터의 서로 다른 구간을 본다 — 시간 척도가 두 자릿수 다르다**

```r
GITT()    filter(state != "R", step.t >= tmin, step.t <= tmax)   # 펄스 중, 5–40 s / 50–150 s
ICI_np()  filter(state == "R",  step.t >= 0.1,  step.t <= 0.9)   # 휴지 중, 0.1–0.9 s
```
GITT: `Dr = (dE_q/s/tp)^2` (Weppner–Huggins, `dE_q = E4 − E0`).
ICI: 휴지 첫 0.1–0.9 s 를 `E ~ √t` 로 회귀해 `Δt=0` 으로 외삽 → `E0` (iR 보정 준평형 OCP),
`R = (E − E0)/I`, `k = −s/I`.
→ **액체셀 `U2`(pOCV 가 원자료인가 필터본인가)의 실험적 대응물이 바로 이 구조다** —
같은 셀·같은 raw 에서 창만 바꾼 두 답이 나란히 보관돼 있다.

**② ★★ 3전극 분해가 코드에 명시돼 있다 — 우리가 *풀어내려는* 것이 여기선 *측정으로* 갈라져 있다**

```r
E_p = 'Ewe/V'      # 양극 vs 기준전극
E_n = 'Ece/V'      # 음극 vs 기준전극
E   = E_p - E_n    # 셀 전압
```
`ICI_np()` 가 `R_p·k_p` / `R_n·k_n` 을 **전극별로 따로** 낸다 (음극은 부호 반전
`R_n = -1*(E_n - E0_n)/I`).
⚠ 단 **`GITT()` 는 양극만 본다** (`if(three.electrode){ E = E_p }`). ICI 만 셋 다 낸다.

**③ 오차 전파가 있다** — `mass.err = 0.02 mg` + `electr.err = 0.025`,
`Q.c.err <- Q.c*(mass.err+electr.err)/mass`, 회귀마다 `_err`(표준편차).
**`assb` 4/4 편이 오차막대 0 이었던 것과 정반대다.**

#### 6-3-c-2. ★★★ `SeqRef_003_1ph.csv` — 남의 공개 자료에 찍힌 **fitting degeneracy 의 지문**

41 스캔, NMC811 c 축 격자상수 정련 (충전 3.70→4.275 V 후 방전):

| scan | 전압 | `c_lp` | `c_lp_err` | `Rwp` | `GoF` |
|---|---|---|---|---|---|
| 13 | 4.275 | **13.95995** | 0.00471 | 11.69 | 3.79 |
| **14** | 4.230 | **13.95995** ← 동일 | **2.48123** (값의 **18 %**) | 12.35 | **4.04** |
| 23~29 | 4.044→3.909 | **14.44853 ×7 연속 동일** | 0.0018~0.52 | 7.0~8.4 | 2.3~2.8 |

**전압이 다른데 `c_lp` 가 얼어붙고, 같은 구간에서 오차가 폭발하며, `GoF` 가 가장 나쁘다**
(좋은 적합은 ≈1). 적합이 수렴 못 했거나 경계에 붙은 구간의 전형적 모양이다.

**★ 그리고 오차막대가 있어서 보인다.** 없었으면 `c_lp` 열만 보고 "매끄러운 격자 변화
곡선" 으로 읽었을 것이다. → 우리 요구서(`NEW_MODEL_REQUIREMENTS.md` §5)의 **"라벨에
오차막대를 붙여라"** 규율에 실증이 하나 더 붙는다: **오차막대는 장식이 아니라 적합이
실패한 지점을 드러내는 장치다.**

⚠ **이것은 우리 판독이지 논문의 주장이 아니다.** 30 번 digest 에서 확인한다.

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
   → 25 → 26 → 27 → 28 → 29 → 30
   → 31 → 32 → 33 → 34 → 35          ← 2026-09-22 추가 (6-3-d, 8호가 낳은 다섯)
   → 36 → 37 → 38                    ← 2026-09-22 추가 (6-3-e, 9호가 낳은 셋)
   → 39                              ← 2026-09-22 추가 (6-3-f, ⚠ assb 아님 — 액체셀 팩 ISC)
```

> **2026-09-22 사용자 결정: 38 번(DRT)만 앞으로 당긴다.** 10 번(Vadhva, EIS 방법론)이
> 끝나는 즉시 38 번을 돌린다 — 둘이 같은 EIS 축퇴를 다뤄 붙여 읽는 값이 크고,
> 떨어뜨리면 그 값이 사라지기 때문이다. **나머지는 순서 그대로다.**
> 즉 실제 실행 순서는 `… → 10 → 38 → 11 → 12 → …` 이다.

**재배열하지 않는다.** 아래 6-4-a 는 내가 한때 권한 재배열인데 **채택되지 않았다** —
근거로만 남긴다. **37 편 × ~20 분 ≈ 12.5 시간**이고 순차로만 돈다(lint 훅이 전체 위키를
보므로 병렬 불가). 한 편이 끝날 때마다 **lint 0 errors 확인 → 커밋 → 다음 편 착수**.

> 31~35 도 **먹인 순서 그대로 꼬리에 붙인다.** 6-3-d 의 지문은 35·34 가 앞서고
> 33·31 이 처지는 것을 가리키지만, **순서 규칙이 지문보다 위**다 (2026-09-16 사용자
> 지시). 지문은 "한 편만 먼저 볼 수 있다면 무엇인가" 를 묻게 될 때 쓰는 근거로만 남긴다.

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

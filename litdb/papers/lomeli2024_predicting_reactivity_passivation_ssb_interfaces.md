<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md · papers/wang2022_resistive_decomposing_interfaces_se_alkali_metal.md
     2026-09-22 초판. 1저자 지정 임무 = ① 보고량 해부 ② 선점 판정 ③ **부동태화 조작적 정의** ④ 스크리닝 데이터 전수 ⑤ 방법 ⑥ 불리한 결론.
     그림 14장 중 **7장 실독**(fig_1·fig_2·fig_3·fig_S2·fig_S3·fig_S4·tab_2(=Table 2+Fig 4 합본)) — 안 본 것은 fig_4(tab_2 안에서 이미 봄)·fig_S1·fig_S5·fig_S6·fig_S7·tab_1(PDF 텍스트로 전사).
     ⚠ 이 digest 안의 "✎ digest 재계산 / figure-read ≈" 표시는 **논문이 보고하지 않은 것을 우리가 그림·xlsx 에서 복원한 것**이다.
     ★ SI2(xlsx) 는 openpyxl 이 못 연다(strict OOXML) — zipfile+ElementTree 로 직접 파싱했다. §3f 참조. -->

# Predicting Reactivity and Passivation of Solid-State Battery Interfaces — Lomeli, Ransom, Ramdas, Jost, Moritz, Sendek, Reed & Devereaux (*ACS Appl. Mater. Interfaces* **2024**, 16, 51584–51594)

> slug `lomeli2024_predicting_reactivity_passivation_ssb_interfaces` · DOI `10.1021/acsami.4c06095` · type `calc 전용 (AIMD + 로지스틱 회귀 스크리너, 실험 0회 — 실험은 전부 인용)` · PDF `litdb/inbox/4. ACSAMI_2024_Lomeli_Predicting_reactivity_passivation_SSB_interfaces_MAIN.pdf` (본문 11 pp) + `litdb/inbox/4. Sup1) ACSAMI_2024_Lomeli_Predicting_reactivity_SI.pdf` (SI 8 pp, `Fig. S1`–`S7` · `Table S1`–`S2`) + **`litdb/inbox/4. Sup2) ACSAMI_2024_Lomeli_Predicting_reactivity_SI.xlsx` (기계판독 가능 예측표 3535행)** · digested `2026-09-22` · status ✅ · 태그 **[외부·음극측 스크리너·★★선점 판정 대상·⛔ 아르지로다이트 0회]**

> elements: Li, B, C, N, O, P, S, Cl, Si, Br, I, In, F
> methods: DFT, AIMD, MD, DOS, PDOS

> **저자**: **Eder G. Lomeli**\*¹², **Brandi Ransom**¹, **Akash Ramdas**¹, **Daniel Jost**², **Brian Moritz**², **Austin D. Sendek**\*¹, **Evan J. Reed**¹, **Thomas P. Devereaux**\*¹²³
> ¹ Dept. of Materials Science and Engineering, **Stanford University** · ² **SLAC** National Accelerator Laboratory (SIMES) · ³ Geballe Laboratory for Advanced Materials, Stanford
> 접수 2024-04-14 / 수정 2024-09-01 / 수락 2024-09-03 / 게재 2024-09-15 · **CC-BY-NC-ND 4.0** · 연구비 **US DOE BES, Materials Sciences & Engineering** · 계산자원 Stanford **Sherlock** + **NERSC** (award BES-ERCAP0027203)
> 🕯 Acknowledgments: 원 지도교수 **Evan J. Reed** 는 2022년 3월 암으로 별세. 논문이 그 사실을 적는다.
>
> **계보**: **Sendek et al.** (*EES* 2017, ref 23 — 12,000 후보 이온전도도 스크리닝, 이 논문의 **descriptor 22개의 원전**) → **Zhu/He/Mo** (*JMCA* 2016, ref 22 — ΔE_rxn / convex-hull 계면 안정성의 표준) → **Camacho-Forero & Balbuena** (*J. Power Sources* 2018, ref 17 — Li‖황화물 AIMD 10 ps 선례) → **본 논문**(AIMD 라벨 67계 + 로지스틱 회귀 → MP 3535 구조 외삽). 같은 그룹의 짝 논문 = **Ransom et al.** *ACS AMI* 2023, ref 11 (계면 **접착(adhesion)** 축 — 본 논문은 접착을 안 한다).
> **우리 litdb 안에서의 위치**: **[Wang22Res]** 가 *"분해가 끝난 뒤"* 를 맡는다면, 이 편은 **"분해가 시작되는 순간"** 을 맡는다. 둘 다 음극(Li 금속)측이고 **둘 다 아르지로다이트를 한 번도 계산하지 않는다.**

---

## 0. 이 digest 를 읽는 법 — 1저자 지정 읽기축 (2026-09-22)

| 순서 | 절 | 묻는 것 |
|---|---|---|
| ① | **§9-1** | **보고량이 정확히 무엇인가** — 스크리너인가 기전 연구인가, 스칼라는 무엇이고 문턱의 근거는 |
| ② | **§9-3** | **🔴 부동태화(passivation) 를 무엇으로 판정하나** — 조작적 정의 · 계산인가 가정인가 · 우리가 가져올 수 있나 |
| ③ | **§9-2** | **🔴 선점 판정** — 겹치는 칸 / 인접한 칸 / 비어 있는 칸 + **구분선 한 문장** |
| ④ | **§3f · §9-4** | **xlsx 전수 해부 + 우리 계 검색 결과** (`Li₆PS₅Cl` 은 **목록에 없다**) |
| ⑤ | **§10** | 방법 나란히 놓기 (판정하지 않고 병렬) |
| ⑥ | **§13 · §14** | 비판 · **우리에게 불리한 결론** |

⛔ **이 편의 수치는 전부 소환값이다.** 우리 `db/properties/*.json` 절대값과 같은 표에 놓지 않는다.
⛔ **`ΔE_rxn` 값을 우리 `interface_reactivity` / `ΔH_D`(−0.3227 eV/atom) 옆에 놓지 않는다** — 혼합분율 규약과 open/closed 규약이 논문에 **한 줄도 없다**(§10-2).
⛔ **`Norm. MSD` 는 이 논문 전용 단위이고 우리 MSD 창(2–50 ps)과 아무 관계가 없다.**

---

## 1. 한 줄 요약

Li 금속과 맞댄 **고체전해질 후보 67종**의 계면을 **550 K · 40–60 ps · ≤150원자 AIMD** 로 각 1회 돌려 눈으로 보고 `stable / passivating / reactive` **세 라벨**을 붙인 뒤(스칼라 대리지표 = 계면에 수직한 **정규화 MSD**), 그 50개를 **로지스틱 회귀 두 개**(SM: stable vs 나머지 · RM: reactive vs 나머지)로 학습해 **Materials Project 의 3535 구조**에 던진다. 결과: 기존 `|ΔE_rxn| < 100 meV/atom` 기준이 **229개**만 안정이라 하던 것을 **stable 533 + passivating 788 = 1321개**로 넓히고, 그중 **`LiB₁₃C₂`·`LiB₁₂PC`** 두 붕소화물을 추가 AIMD 로 확인해 *"Li 금속에 안정하면서 이온전도도가 높은 새 후보"* 로 내세운다. **홀드아웃 17종에서의 실제 오분류율은 35.3 %** 이고, 논문이 자랑하는 **CV 오분류 6–8 %** 는 **1.74 × 10⁶ 개 특징조합을 50점 위에서 뒤져 고른 최솟값**이다.

---

## 2. 메타 / 동기 / 질문

**동기.** SSE 계면 안정성 스크리닝의 업계 표준은 **DFT 전에너지 기반 convex-hull** 이다 — 순상의 `E_hull`, 또는 전극과의 **상호 반응에너지 `ΔE_rxn`** 을 구하고 **100 meV/atom (= 상온 `4 k_BT`)** 이라는 **전 물질 공통 kinetic-stabilization 문턱**으로 자른다. 저자들의 주장은 이렇다.

1. 그 문턱은 **모든 결정구조에 하나의 값**을 쓴다 — 물질마다 다른 반응 장벽·기구를 무시한다.
2. `ΔE_rxn` 은 **어떤 상이 생기는지에 대한 가정**(MP 상도의 최저에너지 조합)에 의존한다.
3. ⇒ **오라벨(false label)** 이 구조적으로 생긴다.

**이 논문이 묻는 것.**
- *"열역학적 구동력만으로 계면 반응성을 부를 수 있나 — 아니면 **유한온도 동역학**을 한 번은 봐야 하나?"*
- *"그 동역학을 **한 번만** 보고, 그 결과를 **값싼 구조 서술자**로 배워, 나머지 수천 개에 외삽할 수 있나?"*

**묻지 않는 것 (중요 — 우리 축과 직결).**
- **양극(cathode)측 계면**: 본문 전체에서 `cathode` 는 **1회**, 그것도 결론의 향후과제 문장(*"such as SSE|cathode interfaces"*)뿐이다.
- **아르지로다이트**: `argyrodite` **0회**, `Li6PS5` **0회**. `Li₆PS₅Cl` 은 훈련셋·검증셋·3535 스크린 **어디에도 없다**(§9-4).
- **계면상 두께·성장속도**: `thickness` **0회**, `self-limit` **0회**.
- **접합/접착(adhesion)·표면에너지**: `adhesion` **0회**, `surface energy` **0회** (같은 그룹의 ref 11 이 그 축이다).
- **전자전도도·면저항**: `electronic conductivity` 1회(= 후보 선별 문구 *"low electronic conductivity criteria (E_G > 0.8 eV)"*), `ASR`·`impedance`·`interphase`·`SEI` 전부 **0회**.
- **무질서(부분점유)**: `disorder`·`SQS` **0회**. 후보는 전부 MP/ICSD 의 **정렬된 단일 셀**이다.

---

## 3. 핵심 수치 총정리 ★

### 3a. ★★ 보고량의 정의 — `Norm. MSD` (본문 p.51585)

> 논문에 수식 번호가 붙은 식은 **딱 하나**(Eq. 1, 무작위추측 오분류율)이고, **정작 핵심 보고량에는 수식이 없다.** 아래는 산문을 우리가 식으로 옮긴 것이다.

**절차 (본문 그대로 5단계)**
1. 원자마다 **계면평면에 수직한 축(z)** 방향 MSD 를 구한다. ⇒ **1차원 MSD** 다 (3D 아니다).
2. **원래 계면의 위치**를 정의한다 — *"가장 바깥쪽 SSE 원자와 Li 금속 원자의 **중간 평면**"*. PBC 때문에 **셀 안에 계면이 2개**(가운데 1 + 가장자리 1)이고 **둘 다 센다**.
3. 그 평면을 **넘어간** 원자를 `reactive atom` 으로 표시한다.
4. `reactive` 인 **SSE sublattice 원자**(= Li 를 제외한 모든 원소)의 MSD 를 **평균**한다.
   - 단, **unstable 로 판정된 계**에서는 **계면을 넘어간 Li 도 평균에 포함**한다 (Li 가 SSE 안으로 들어가 반응하는 경우를 세기 위해).
5. 그 값을 **원래 SSE 의 z 방향 길이 `L_SSE` 로 나눈다** → 셀당 스칼라 1개.

```
Norm. MSD  =  ⟨ MSD_⊥ ⟩_(계면을 넘은 sublattice 원자)  /  L_SSE          [단위: Å² / Å = Å]
```

⚠⚠ **단위가 무차원이 아니다.** Å²/Å = **Å** 다. 논문은 축을 `Norm. MSD` 라고만 적고 단위를 **한 번도 쓰지 않는다**. §13-② 에서 이 정규화가 왜 부동태화 지표로 **역방향**인지 다룬다.

**문턱 3개와 그 근거**

| 문턱 | 값 | 어디에 쓰나 | **근거** |
|---|---|---|---|
| 열진동 배경 | **≈0.1 Å²** | 반응 판정의 하한 눈금 | ref 19 = **Jauncey & Bruce, *Phys. Rev.* 51, 1067 (1937), "Atomic Structure and Vibrations in **Zinc** Crystals"** — ⚠ **1937년 Zn 결정 X선 연구**다 |
| "반응했다" 판정 | **> 0.5 Å²** (계면을 넘은 뒤의 MSD) | 개별 원자 | *"we use a **higher threshold** of 0.5 Å²"* — 배경의 **5배**. 5배를 고른 이유는 **없다** |
| **stable 상한** | **Norm. MSD < 0.05** | 계 전체 라벨 | **근거 문장 없음.** 관측된 분리를 사후에 적은 것 |
| **passivating ↔ reactive 경계** | 🔴 **숫자가 논문에 없다** | 계 전체 라벨 | *"between the stable and reactive"* 라고만 한다. **figure-read ≈ 0.31** (§3b) |

🔴 **그리고 라벨의 1차 출처는 지표가 아니라 사람 눈이다.** `Fig. 1` 캡션: *"with colored labels assigned by **inspection of the simulation cells**"*. 본문도 *"Based on the results of these simulations, we **label** each SSE candidate…"* 가 먼저 오고 *"We **formalize** these three class labels by establishing a reactivity metric"* 가 뒤에 온다. ⇒ **`Norm. MSD` 는 라벨의 정의가 아니라 라벨의 사후 대리지표**다. (§9-1 에서 우리 보고량 규율에 걸어 본다.)

### 3b. ★★ 훈련셋 50종 전수 — **`Norm. MSD` 값 복원** (`Fig. 1` 막대 + `Fig. S2` 산점 + `Table 1`)

> ⭐ **이 표는 이 digest 의 자체 생산물이다.** 논문은 **`Norm. MSD` 값을 숫자로 한 번도 공개하지 않는다**(xlsx 에도 없다). 아래는 `Fig. 1` 막대 상단과 `Fig. S2` 산점 좌표를 **축 보정 후 픽셀 판독**해 복원한 것이다.
> 두 그림의 값이 **±0.005 이내로 일치**하므로 판독은 검증됐다 — **단 최상위 3계는 예외이고, 그것이 §13-① 의 발견이다.**

| # | 물질 | `Table 1` 라벨 | ΔE_rxn (eV/atom) | **`Fig. 1` 막대** (figure-read ≈) | **`Fig. S2` 산점** (figure-read ≈) |
|---|---|---|---|---|---|
| 1–19 | KLiS · Li₂PNO₂ · **Li₂S** · Li₂SiN₂ · Li₂TiO₃ · **Li₃N** · **Li₃P** · Li₃VO₄ · Li₄SiO₄ · Li₆NBr₃ · Li₇La₃Zr₂O₁₂ · Li₇PN₄ · Li₇VGeO₈ · Li(BH)₆ · LiMgN · LiSmS₂ · LiTaO₃ · RbLiS · Sr₂LiCBr₃N₂ | **stable** | 0.000 ~ −0.391 | **19개 전부 0.028** (막대 높이가 픽셀까지 동일) | **19개 전부 ≈0.015** (한 줄 수직 띠) |
| 20 | **Li₆WN₄** | passivating | 0.000 | 0.098 | 0.085 |
| 21 | Li₃Sc₂(PO₄)₃ | passivating | −0.501 | 0.113 | 0.114 |
| 22 | LiErSe₂ | passivating | −0.077 | 0.128 | 0.131 |
| 23 | Li₂TiSiO₅ | passivating | −0.251 | 0.138 | 0.137 |
| 24 | LiAlSiO₄ | passivating | −0.220 | 0.138 | 0.140 |
| 25 | LiHoS₂ | passivating | −0.110 | 0.158 | ≈0.167 |
| 26 | LiErS₂ | passivating | −0.097 | 0.172 | ≈0.167 |
| 27 | Li₆FeCl₈ | passivating | −0.332 | 0.203 | 0.203 |
| 28 | **LiDyS₂** 🔻경계 | passivating | −0.120 | **0.302** | **0.303** |
| 29 | **Li₆ZnGe₂O₈** 🔺경계 | reactive | −0.431 | **0.318** | **0.318** |
| 30 | Li₃BS₃ | reactive | −0.491 | 0.347 | 0.349 |
| 31 | LiLaTi₂O₆ | reactive | −0.210 | 0.362 | 0.367 |
| 32 | LiSO₃F | reactive | **−1.110** (최대 구동력) | 0.378 | 0.381 |
| 33 | LiSnPO₄ | reactive | −0.524 | 0.407 | 0.412 |
| 34 | **NaLiSe** 🔴 | **passivating** (Table 1) | −0.068 | **0.427 — 막대 색이 navy(reactive)** | **0.429 — 점 색이 navy(reactive)** |
| 35 | BaLiBS₃ | reactive | −0.529 | 0.472 | 0.475 |
| 36 | CsLi₂BS₃ | reactive | −0.409 | 0.517 | 0.515 |
| 37 | **Li₁₀GeP₂S₁₂** ⭐우리축 | reactive | −0.680 | 0.552 | 0.552 |
| 38 | Li₆TeO₆ | reactive | −0.616 | 0.568 | 0.568 |
| 39 | LiMnPO₄ | reactive | −0.546 | 0.623 | 0.622 |
| 40 | LiGa(PO₃)₄ | reactive | −0.759 | 0.632 | 0.630 |
| 41 | Li₃Fe₂(PO₄)₃ | reactive | −0.669 | 0.723 | 0.724 |
| 42 | LiScTl₂Cl₆ | reactive | −0.417 | 0.733 | 0.734 |
| 43 | Li₂B₂S₅ | reactive | −0.799 | 0.777 | 0.775 |
| 44 | Li₃ErCl₆ | reactive | −0.162 | 0.777 | 0.779 |
| 45 | **Li₃PS₄** ⭐우리축 | reactive | −0.708 | 0.818 | 0.819 |
| 46 | Li₃InCl₆ | reactive | −0.506 | 0.907 | 0.907 |
| 47 | **Li₇P₃S₁₁** ⭐우리축 | reactive | −0.805 | 0.912 | 0.911 |
| 48 | LiBiF₄ | reactive | −0.860 | **0.998 (잘림)** | **1.058** |
| 49 | Li₂GePbS₄ | reactive | −0.682 | **0.998 (잘림)** | **1.118** |
| 50 | **LiGaCl₃** | reactive | −0.607 | **0.998 (잘림)** | **1.547** 🔴 |

**이 표에서 읽히는 것 6가지**
1. 🔴 **`Fig. 1` 의 y축은 1.0 에서 잘려 있고 상위 3계가 클리핑됐다.** 진짜 값은 **1.058 / 1.118 / 1.547** 이다 (`Fig. S2` 에서 복원). `Fig. 1` 만 보면 *"reactive 의 상한이 1.0"* 으로 읽히지만 **실제 산포는 5 배 더 넓다.** 논문은 이 사실을 어디에도 적지 않는다. → §13-①
2. 🔴 **NaLiSe 는 `Table 1` 이 passivating, 그림 둘은 reactive 다.** 그림대로면 훈련셋 구성이 **19/9/22** 이고 본문·`Table 1` 대로면 **19/10/21** 이다. **어느 쪽으로 학습했는지 알 수 없다.** → §13-③
3. ⭐ **stable 19계가 막대 높이까지 전부 같다** (`Fig. 1` 0.028 · `Fig. S2` 0.015). 지표가 이 영역에서 **분해능이 없다** — "얼마나 안정한가"는 못 말한다.
4. 🔴 **passivating ↔ reactive 경계가 면도날이다**: LiDyS₂ 0.303 ↔ Li₆ZnGe₂O₈ 0.318, **간격 0.015** = passivating 띠 폭(0.085–0.303)의 **7 %**. 그리고 그 경계에는 **숫자가 없다** — 사람이 그림을 보고 그었다. `Fig. S1` 이 바로 이 두 계의 스냅샷이다.
5. ⭐ **`ΔE_rxn` 과 `Norm. MSD` 의 상관은 약하다** — LiSO₃F 는 구동력 최대(−1.110)인데 반응성은 32위(0.381)이고, Li₃ErCl₆ 는 구동력 −0.162 로 작은데 반응성 44위(0.779)다. **이것이 논문의 존재 이유**이고 `Fig. S2` 가 그 그림이다.
6. ⭐⭐ **우리 축 3개가 전부 reactive 상위권이다** — `Li₃PS₄` 0.819(45위) · `Li₇P₃S₁₁` 0.911(47위) · `Li₁₀GeP₂S₁₂` 0.552(37위). → §14-①

### 3c. ★ 검증셋(홀드아웃) 17종 전수 — `Table 2` **전사** (이미지 표라 PDF 텍스트로 안 나온다 → `tab_2.png` 실독 전사)

| 조성 | MP-ID | ΔE_rxn (eV/atom) | **AIMD 실제 라벨** | **모델 예측** | 판정 |
|---|---|---|---|---|---|
| LiCaAlN₂ | mp-1020031 | 0.000 | Stable | Passivating | 🟨 (useful 로 셈) |
| **LiSiB₆** \* | mp-973391 | −0.104 | Stable | **Stable** | ✅ |
| **LiB₁₂PC** \* | mp-1222458 | −0.152 | Stable | **Stable** | ✅ ⭐헤드라인 |
| **LiB₁₃C₂** \* | mp-655591 | −0.162 | Stable | **Stable** | ✅ ⭐헤드라인 |
| Li₇SbN₄ \* | mp-1029522 | −0.177 | Stable | **Stable** | ✅ |
| LiBeP \* | mp-9915 | −0.206 | Stable | Passivating | 🟨 |
| LiGe₂N₃ | mp-1020059 | −0.292 | Stable | Passivating | 🟨 |
| K₃LiSi₄ \* | mp-28316 | −0.172 | Passivating | Passivating | ✅ |
| Na₂LiAlP₂ \* | mp-9719 | −0.176 | Passivating | Passivating | ✅ |
| K₂LiAlP₂ \* | mp-6450 | −0.176 | Passivating | Passivating | ✅ |
| **LiMgP** | mp-36111 | −0.105 | **Reactive** | **Stable** | 🟥 **유일한 false-stable** |
| Li₂HIO | mp-643069 | −0.244 | Reactive | Reactive | ✅ |
| **LiAlH₄** | mp-1192061 | −0.303 | **Reactive** | Passivating | 🟥 |
| **LiGaH₄** | mp-1095586 | −0.334 | **Reactive** | Passivating | 🟥 |
| Li₄TiS₄ | mp-756811 | −0.338 | Reactive | Reactive | ✅ |
| Li₅BiS₄ \* | mp-755139 | −0.470 | Reactive | Reactive | ✅ |
| Li₄SnSe₄ \* | mp-1194700 | −0.489 | Reactive | Reactive | ✅ |
| | | | **Validation Misclassification Rate** | **35.3 %** | |
| | | | Random Guessing Misclassification | 63.7 % | |
| | | | Baseline Misclassification | 58.2 % | |

\* = Sendek et al.(ref 23) 이 **고이온전도 후보로도 예측**한 물질 (10/17).
⚠ **각주 단위 오류**: *"σ_Li > 10⁻⁴ **mS/cm**"* 라고 적혀 있으나 Sendek 문턱은 **10⁻⁴ S/cm** 다 (본문 결론은 S/cm 로 맞게 쓴다). 1000배 오기.
⚠ **검증셋이 무작위가 아니다** — 본문이 자인: *"we **chose materials predicted to be good Li ion conductors**"*. ⇒ **35.3 % 는 스크린 전체에 대한 불편추정치가 아니다**(§13-⑤).
⚠ **오류 6건 중 3건(🟨)을 "그래도 쓸 만하다"고 재분류해 17.6 % 로 다시 적는다** — 사후 재채점이다(§13-⑥).

### 3d. ★ 모델 계수 전수 — `Table S2` (정규화 계수, 훈련셋 평균으로 표준화)

> **부호 읽는 법 (논문이 직접 주는 앵커)**: 본문 p.51588 — *"the sublattice bond ionicity … having a **negative** linear coefficient and contributing to a **stable** prediction the higher the feature value"*. ⇒ **음수 = stable 방향 · 양수 = unstable 방향.**

**SM (8-feature, "Stable Model" — stable vs passivating+reactive)**

| feature | 훈련셋 평균 | 표준편차 | **정규화 계수** | 방향 해석 |
|---|---|---|---|---|
| **ΔE_rxn** (eV/atom) | −0.326 | 0.291 | **−1.258** ⭐최대 | ΔE_rxn 이 **더 음수** → 기여 **양수** → **unstable** ✓ |
| RBI (Li BI / sublattice BI) | 1.496 | 0.996 | −0.796 | 클수록 stable |
| **SBI** (sublattice bond ionicity) | 0.904 | 0.284 | **−0.791** | 클수록 stable ✓ (본문이 해설) |
| SLPE (straight-line path EN) | 2.747 | 0.740 | **+0.718** | 클수록 unstable |
| LLB (Li–Li bonds per Li) | 5.485 | 4.406 | −0.624 | 클수록 stable ⭐ **본문 미언급** |
| SLPW (straight-line path width) | 0.844 | 0.243 | **+0.621** | 경로가 넓을수록 unstable |
| **AAV** (average atomic volume, Å³) | 15.930 | 5.367 | **+0.616** | 클수록 unstable ✓ (= "밀하면 안정") |
| AASD (anion–anion 최단거리, Å) | 3.239 | 0.716 | **−0.301** 🔴 | 멀수록 stable — **AAV·SLPW 와 반대 방향** |

**RM (7-feature — `Table S2` 는 "Passivating Model" 이라 적는다 ⚠ · stable+passivating vs reactive)**

| feature | 평균 | 표준편차 | **정규화 계수** | 방향 |
|---|---|---|---|---|
| **ΔE_rxn** | −0.326 | 0.291 | **−2.145** ⭐압도적 | unstable |
| **LNC** (Li neighbor count) | 18.634 | 6.732 | **−0.960** | 많을수록 안정 |
| LBI (Li bond ionicity) | 1.191 | 0.503 | **+0.657** 🔴 | 클수록 **불**안정 — SM 의 SBI(−0.791)와 **부호가 반대** |
| SLPW | 0.844 | 0.243 | +0.633 | 넓을수록 불안정 |
| LLSD (Li–Li 최단거리) | 3.365 | 0.876 | −0.376 | 멀수록 안정 |
| AAV | 15.930 | 5.367 | +0.350 | 클수록 불안정 |
| **SPF** (sublattice packing fraction) | 0.266 | 0.163 | **+0.042** 🔴🔴 | **ΔE_rxn 의 1/51** — 사실상 0 인데 "최적 7개"에 들어 있다 |

**읽히는 것 4가지**
1. ⭐ **두 모델 다 `ΔE_rxn` 이 압도적 1위다.** RM 에서는 2위(LNC 0.960)의 **2.2배**. ⇒ *"구조가 열역학을 이긴다"* 가 아니라 **"열역학이 여전히 지배하고 구조가 보정한다"** 가 정확한 서술이다. 논문 서사는 전자에 가깝다.
2. 🔴 **AASD 가 밀도 서사와 반대 부호다.** AAV(+0.616, 크면 불안정)·SLPW(+0.621) 와 AASD(−0.301, 멀면 안정)는 둘 다 "열린 구조" 를 재는데 방향이 반대다. **다중공선 특징에서의 전형적 부호 뒤집힘**이고, 논문은 AASD 를 한 번도 해설하지 않는다.
3. 🔴 **SBI(−0.791, SM) 와 LBI(+0.657, RM) 의 부호가 반대다.** 둘 다 "결합 이온성" 이다(하나는 sublattice, 하나는 Li 결합). 본문은 SBI 만 물리로 해설하고 LBI 는 언급하지 않는다.
4. 🔴 **SPF 계수 0.042 는 잡음이다.** 그런 특징이 "CV 최소의 7-feature 조합"에 들어 있다는 것은 **특징 개수 선택이 신호가 아니라 잡음으로 결정됐다**는 직접 증거다(§13-④).
5. ⭐ **LLB(−0.624) 는 Sendek 이온전도 모델의 1위 서술자다.** 여기서도 *"많을수록 안정"* 으로 나온다 ⇒ **이온전도와 안정성이 같은 방향을 가리키는 드문 신호**인데 논문은 이걸 못 보고 지나간다(본문은 정반대로 *"high packing fraction 은 전도를 막는다"* 는 트레이드오프만 말한다).

### 3e. ★ 성능 수치 전수

| 지표 | **SM** (stable vs 나머지) | **RM** (reactive vs 나머지) | 출처 |
|---|---|---|---|
| 최적 특징 수 | **8** | **7** | 본문 + `Fig. 2` |
| **5-fold CV 오분류** | **8 %** (figure-read: N=8·9·10 모두 0.08 로 **동률**) | **6 %** (figure-read: N=7 과 N=10 이 동률 0.06) | `Fig. 2a,b` |
| 훈련 오분류 (figure-read ≈) | N=7–9 에서 **0.04**, N=10 에서 0.06 (다시 오른다) | N=7–10 에서 **0.02** | `Fig. 2a,b` |
| `ΔE_rxn` 100 meV/atom 단독 | **22 %** (figure-read 0.22) | **26 %** (figure-read 0.257) | 본문 + `Fig. 2` |
| Baseline(다수class) 오분류 | figure-read **0.385** | figure-read **0.42** | `Fig. 2` |
| Random guessing 오분류 | figure-read **0.47** | figure-read **0.487** | `Fig. 2` |
| **홀드아웃 17종 오분류** | — (두 모델 결합) | — | **35.3 %** (`Table 2`) |
| 정밀도·재현율 | — | — | **둘 다 76.9 %** (TP 10 / FP 3 / FN 3 ⇒ 10/13 ✎ 우리 역산 ✓) |
| "완전 음성" 오분류 (🟥 만) | — | — | **17.6 %** (3/17) |

✎ **digest 재계산 — 특징조합 탐색 규모**: 22개 특징에서 N=1..10 을 **전수 조합**하면 `Σ C(22,N) = 1 744 435` 개 모델이다. 훈련점이 **50개**이므로 5-fold CV 오분류의 **양자(quantum)는 1/50 = 0.02** 다. ⇒ **170만 개 후보 중 최솟값을 고르면 0.06–0.08 은 거의 결정적으로 나온다.** 이것이 CV 6–8 % 와 홀드아웃 35.3 % 사이 **4–6배 격차**의 가장 단순한 설명이다(§13-④).

### 3f. ★★★ **SI2 (xlsx) 전수 해부** — 1저자 지정 과제

> ⛔ **`openpyxl` 로는 못 연다.** 이 파일은 **strict OOXML**(`conformance="strict"`, 네임스페이스가 `purl.oclc.org/ooxml/...`)로 저장돼 있어 `openpyxl.load_workbook()` 이 `sheetnames == []` 를 돌려준다(경고 `File contains an invalid specification for 0`). ⇒ **`zipfile` + `xml.etree.ElementTree` 로 `xl/workbook.xml` · `xl/sharedStrings.xml` · `xl/worksheets/sheet{1,2,3}.xml` 을 직접 파싱**했다. 다음 사람이 같은 함정을 밟지 않게 적어 둔다.
> 저장 경로 메타: `/Users/elomeli/Documents/_GradSchool/Devereaux Group/interface_paper/review_2/submit_folder/` (리뷰 2라운드 제출본).

**시트 구조 — 3 시트 × 5 열**

| # | 시트 이름 | 데이터 행 | 열 수 | 열 이름 (1행) |
|---|---|---|---|---|
| 1 | **`stable_materials`** | **533** | 5 | `(무제목 인덱스)` · `Material` · `MP-ID` · `crystal_system` · `E_rxn` |
| 2 | **`passivating_materials`** | **788** | 5 | 〃 |
| 3 | **`reactive_materials`** | **2214** | 5 | 〃 |
| | **합계** | **3535** | | = 본문의 3535 후보 ✓ |

**대표 행 (각 시트 첫 3행 + 마지막 행, 원문 그대로)**

| 시트 | 인덱스 | Material | MP-ID | crystal_system | E_rxn |
|---|---|---|---|---|---|
| stable | 0 | `LiYbAlF6` | mp-10103 | trigonal | −0.25357499999999999 |
| stable | 1 | `BaNaLi3(BO2)6` | mp-1019555 | trigonal | −0.2642485 |
| stable | 2 | `CsLi(B3O5)2` | mp-1019715 | orthorhombic | −0.334603445694444 |
| stable | **532** (끝) | `Li3ClO` | mp-985585 | cubic | −0.0275734520000003 |
| passivating | 0 | `LiScS2` | mp-1001786 | trigonal | −0.12859999999999999 |
| passivating | 1 | `BaLi2Mg(PO4)2` | mp-1019547 | trigonal | −0.431435855714292 |
| passivating | 2 | `Cs2Li5(BO2)7` | mp-1019607 | orthorhombic | −0.251525236462058 |
| passivating | **787** (끝) | `LiBeP` | mp-9915 | tetragonal | −0.2062364 |
| reactive | 0 | `Li48P16S61` | mp-1001069 | monoclinic | −0.728991764981712 |
| reactive | 1 | `Cs2Li2B2P4O15` | mp-1019606 | triclinic | −0.5698799 |
| reactive | 2 | `K2Li3B(P2O7)2` | mp-1019778 | orthorhombic | −0.5366717 |
| reactive | **2213** (끝) | `LiSnCl3` | mp-998591 | trigonal | −0.632493535999999 |

**이 파일에서 우리가 뽑을 수 있는 것 / 없는 것**

| | |
|---|---|
| ✅ **있다** | 3535개 **구조별**(mp-id 고유, 중복 0) 최종 라벨 3분류 + `E_rxn`(eV/atom, 15–17자리) + 결정계. **정렬·조인·필터가 바로 되는 진짜 기계판독표**다 |
| ⛔ **없다** | **`Norm. MSD` 값 0개** (67계 AIMD 라벨의 원자료가 어디에도 없다) · 모델 **확률·결정함수 점수 0** · **22개 특징 값 행렬 0** · SM/RM **개별 예측 0**(결합 라벨만) · `E_hull`·`E_G` 0 · 코드·시드 0 |
| 🔎 **검산 통과** | `|E_rxn| < 0.1` 인 것이 stable **180** + passivating **31** + reactive **18** = **229** — 본문의 *"ΔE_rxn 단독 기준은 229개를 stable 이라 한다"* 와 **정확히 일치** ✓✓ (데이터셋 무결성 확인) |
| ✎ **재계산** | "새로 안정" = 533 − 180 = **353** (본문 *"over 300"* ✓) · passivating 중 열역학적으로 불리한 것 = 788 − 31 = **757** (초록 *"over 780 passivating … predicted to be thermodynamically unfavored"* 는 **788 을 말한 것** — 757 이 맞다. 3 % 과장) |
| 🔴 **결함** | **87개 조성이 다형(polymorph)에 따라 서로 다른 라벨을 받는다** — 예: `Li₃PO₄` mp-13725 **stable** / mp-2878 **passivating**; `CsLiCl₂` mp-1188344 **reactive** / (다른 다형) **stable**; `Li₃ErBr₆` mp-37873 **passivating** / mp-1222492 **reactive**; `LiNbO₃` 는 **stable 1 + passivating 8**. **조성 단위 집계 규칙이 선언돼 있지 않다**(§9-1) |

**통계 (✎ digest 재계산)**

| 시트 | n | `E_rxn` 최소 | 최대 | 평균 | 중앙값 | 최빈 구간(0.05 폭) |
|---|---|---|---|---|---|---|
| stable | 533 | −0.797 | 0.000 | −0.195 | −0.158 | **\|E\|≈0.025** (135개) |
| passivating | 788 | −0.853 | 0.000 | −0.375 | −0.400 | **\|E\|≈0.425** (181개) |
| reactive | 2214 | **−1.835** | 0.000 | −0.686 | −0.661 | **\|E\|≈0.625** (315개) |

⇒ 본문 *"passivating 의 피크가 stable 보다 약 300 meV/atom 높고 reactive 는 750 meV/atom 근처"* 를 검산하면 최빈구간 차이는 **0.425 − 0.025 = 0.400 eV/atom**(300 이 아니라 **400**) 이고 reactive 최빈은 **0.625**(750 이 아니라 **625**). 🔴 **본문 서술이 `Fig. S6` 원자료와 100–125 meV/atom 어긋난다** (✎ 우리 재계산, §13-⑧).
⇒ 본문의 *"high ΔE_rxn (as high as **796 meV/atom**) labeled as stable"* 은 xlsx 에서 `LiCaPrTeO₆` mp-40186 **−0.7967** 로 **정확히 확인** ✓.
⇒ *"as little as 0 meV/atom 인데 passivating/reactive"* 도 확인 ✓ — `CsLiCl₂` mp-1188344 **E_rxn = 0.000 인데 reactive**, `LiGdO₂`·`Li₂ThN₂`·`KLiTe`·`Li₄Ca₃(SiN₃)₂`·`LiDyO₂` 는 0.000 인데 **passivating**.

**화학군별 분포 (✎ digest 재계산 · 기저율 = stable 15.1 % / passivating 22.3 % / reactive 62.6 %)**

| 군 (조성식 정규식) | n | stable | passivating | reactive | 기저율 대비 stable |
|---|---|---|---|---|---|
| **질화물**(N 포함, Na/Nb/Nd/Ni 제외) | 159 | **79 (49.7 %)** | 54 (34.0 %) | 26 (16.4 %) | **3.3×** ⭐ |
| **염화물**(Cl 포함) | 120 | 14 (11.7 %) | 12 (10.0 %) | **94 (78.3 %)** | 0.78× |
| **황화물**(S 포함·O 없음) | 169 | **5 (3.0 %)** | 28 (16.6 %) | **136 (80.5 %)** | **0.20×** 🔴 |
| **붕산염**(Li + B + O) | 364 | 42 | 224 | 98 | 0.77× (단 passivating 이 **2.8×** 풍부) |

⛔ **이 비율은 MP 후보 구성 편향을 그대로 물려받는다 — 절대 인용 금지, 경향만.**

### 3g. 우리 계 · 관련 상의 xlsx 전수 조회 (1저자 지정 ④)

| 우리 축 물질 | xlsx 에 있나 | MP-ID | 결정계 | `E_rxn` (eV/atom) | **라벨** |
|---|---|---|---|---|---|
| **`Li₆PS₅Cl`** (comp1/modelc 모체) | 🔴🔴 **없다 (0행)** | — | — | — | — |
| **`Li₆PS₅Br`** | 🔴 **없다** | — | — | — | — |
| **`Li₆PS₅I`** | ✅ **2행** | mp-950995 / **mp-985582** | monoclinic / **cubic** | **−0.5486 / −0.5653** | **reactive / reactive** |
| `Li₇PS₆` | ✅ | **mp-1211324** ⚠ | orthorhombic | −0.5562 | **reactive** |
| `Li₅P(S₂Cl)₂` ← **유일한 Li–P–S–Cl 항목** | ✅ | mp-1040450 | orthorhombic | −0.5966 | **reactive** |
| `Li₃PS₄` | ✅ 2행 | mp-1097036 / mp-985583 | orthorhombic | −0.7000 / −0.6845 | **reactive / reactive** |
| `Li₇P₃S₁₁` | ✅ | mp-641703 | triclinic | −0.8054 | **reactive** |
| `Li₄₈P₁₆S₆₁` | ✅ | mp-1001069 | monoclinic | −0.7290 | **reactive** |
| `Li₁₀GeP₂S₁₂` | ❌ (스크린엔 없고 **훈련셋**에 있다) | mp-696138 | — | −0.680 | **reactive (AIMD)** |
| **0 V 분해산물 — `Li₂S`** | ✅ (훈련셋에도) | mp-1153 | cubic | **0.000** | **stable (AIMD 확인)** ⭐ |
| **0 V 분해산물 — `Li₃P`** | ❌ 스크린 밖 (**훈련셋**엔 있다) | mp-736 | — | **0.000** | **stable (AIMD 확인)** ⭐ |
| **0 V 분해산물 — `LiCl`** | ✅ 2행 | mp-22905 / mp-1185319 | cubic / hexagonal | −0.0205 / 0.000 | **stable / stable** ⭐ |
| `Li₂O` | ✅ | mp-1960 | cubic | 0.000 | **stable** |
| `Li₃N` | ❌ 스크린 밖 (**훈련셋**엔 있다) | mp-2251 | — | 0.000 | **stable (AIMD 확인)** |
| `LiF` | ✅ 2행 | mp-1138 / mp-1185301 | cubic / hexagonal | 0.000 / −0.0067 | **stable / stable** |
| **B₂O₃ 도핑축 — `Li₃BO₃`** | ✅ | mp-27275 | monoclinic | −0.0950 | **stable** ⭐ |
| **B₂O₃ 도핑축 — `Li₆B₄O₉`** | ✅ | mp-1020024 | monoclinic | −0.1809 | **stable** |
| `LiBO₂` | ✅ 2행 | mp-3635 / mp-14232 | monoclinic / tetragonal | −0.2109 / −0.2185 | **passivating / passivating** |
| `Li₂B₄O₇` | ✅ | mp-4779 | tetragonal | −0.3125 | **passivating** |
| `LiB₃O₅` | ✅ 2행 | mp-1020025 / mp-3660 | orthorhombic | −0.4112 / −0.3764 | **passivating / passivating** |
| 코팅 — `LiNbO₃` | ✅ **9행** | mp-3731 **stable** + 8개 **passivating** | 다형 | −0.321 ~ −0.357 | 🔴 **stable 1 / passivating 8** |
| 코팅 — `Li₂ZrO₃` | ✅ | mp-4156 | monoclinic | −0.0278 | **stable** |
| 코팅 — `LiAlO₂` | ✅ 2행 | mp-3427 / mp-8001 | tetragonal / trigonal | −0.0788 / −0.0946 | **stable / stable** |
| 코팅 — `Li₃PO₄` | ✅ 2행 | mp-13725 / mp-2878 | orthorhombic | −0.3436 / −0.3447 | 🔴 **stable / passivating** (같은 조성·같은 결정계) |
| `Li₇La₃Zr₂O₁₂` | ✅ (훈련셋에도) | mp-942733 | tetragonal | −0.006 | **stable (AIMD 확인)** |
| 할라이드 — `Li₃InCl₆` | ✅ (훈련셋에도) | mp-676109 | monoclinic | −0.5052 | **reactive (AIMD 확인)** |
| 할라이드 — `Li₃ErCl₆` | ✅ (훈련셋에도) | mp-676361 | trigonal | −0.1622 | **reactive (AIMD 확인)** |
| 할라이드 — `Li₃ScCl₆` | ✅ | mp-686004 | monoclinic | −0.2145 | **passivating** |
| `Li₂ZrCl₆` · `Li₃YCl₆` · `Li₃OCl` | ❌ 전부 없다 | — | — | — | — |
| **NCM / LiNiO₂ / LiCoO₂** | 🔴 **없다** (양극이라 SSE 후보군에 안 들어간다) | — | — | — | — |
| **Li-In** | 🔴 **없다** (합금 음극은 대상 아님) | — | — | — | — |
| **Li 금속** | 대상 아님 — **모든 셀의 상대 전극**이다 (mp-135) | — | — | — | — |

⭐⭐ **가장 값어치 있는 단일 발견 세 가지**
1. **`Li₆PS₅Cl` 이 3535 목록에 없다.** `Li₆PS₅I` 는 **두 다형 다 들어 있으므로** 구조형 자체가 배제된 것은 아니다. ⇒ 필터(`E_hull ≤ 100 meV/atom`, `E_G > 1.5 eV`) 중 하나에 걸렸거나 당시 MP 에 해당 정렬 항목이 없었던 것으로 보이는데 **논문이 이유를 밝히지 않아 확인 불가**. ⛔ *"이 논문이 LPSCl 을 reactive 로 분류했다"* 고 **말하면 안 된다.** 가장 가까운 대리값은 **`Li₆PS₅I` = reactive** 와 **`Li₅P(S₂Cl)₂` = reactive** 다.
2. ⭐ **아르지로다이트의 0 V 분해산물 3형제(`Li₂S`·`Li₃P`·`LiCl`)가 전부 "Li 금속에 stable"** 이다 — Li₂S·Li₃P 는 **40 ps AIMD 직접 확인**(`Fig. 1` 의 cyan 막대), LiCl 은 스크린 예측. ⇒ **[Wang22Res] 와 정확히 짝이 맞는다**: *산물은 Li 금속과 더 반응하지 않지만(이 논문), 붙지도 않고 통하지도 않는다(Wang22).* 두 편을 합치면 음극 계면 서사가 완성된다.
3. ⭐ **`Li₃P`·`Li₃N` 이 3535 스크린에서 빠진 이유가 `E_G > 1.5 eV` 필터다.** 우리 `sei_electronic.json` 의 fixed-occ nscf 값 **Li₃P 0.7092 eV**(= `conductor-LEAK`), Li₃N(MP 0.98/1.22) 과 **정합**한다. ⇒ *"우리가 전자누설 산물이라고 부른 두 상이, 남의 독립 스크리너에서도 '전해질로 쓸 수 없는 갭'으로 걸러졌다"* — **서열에 대한 외부 방증**(절대값 방증은 아니다).

### 3h. ★ 붕소화물 두 종 — 논문의 헤드라인 (`Fig. 4`, `tab_2.png` 안에서 실독)

| | **LiB₁₃C₂** | **LiB₁₂PC** |
|---|---|---|
| MP-ID | mp-655591 | mp-1222458 |
| ΔE_rxn vs Li | **−0.162** (본문은 "152 meV/atom" 이라 적는다 ⚠ `Table 2` 는 −0.152 가 LiB₁₂PC · −0.162 가 LiB₁₃C₂ — **본문이 두 값을 섞었다**) | −0.152 |
| 구조 | 붕소 icosahedron 격자 + **1D Li 채널** | 〃 (+ P) |
| 채널 최단폭 (figure-read, `Fig. 4c`) | **3.75 / 3.94 Å** (최단 **3.75**) | **3.52 / 3.70 / 3.85 Å** (최단 **3.52**) |
| **D_vac (300 K, cm² s⁻¹)** | **8.19 × 10⁻⁵** | **2.69 × 10⁻⁵** |
| **σ_Li (300 K, S cm⁻¹)** @ **vacancy 0.05 %** 가정 | **1.30 × 10⁻³** | **4.43 × 10⁻⁴** |
| AIMD 온도점 (`Fig. 4c` figure-read) | 1000/T ≈ **1.11 / 1.43 / 2.0** (= 900/700/500 K) + **3.33 (300 K) 는 외삽 마름모** | 〃 |
| 40 ps 계면 AIMD | 붕소 격자 **변화 없음** (`Fig. 4b`) | 〃 |
| 선행 합성 | Vojteer & Hillebrecht, *Angew* 2006 (ref 31) | Vojteer et al., *Chem. Eur. J.* 2011 (ref 32) |

✎ **digest 검산 (Nernst–Einstein 자기일관성)**: `σ = c_vac q² D /(k_B T)` 로 역산하면 LiB₁₃C₂ 의 `c_vac ≈ 2.6 × 10¹⁸ cm⁻³` ⇒ `n_Li ≈ 5.1 × 10²¹ cm⁻³` (Li 하나당 ≈195 Å³). 붕소탄화물 밀도(≈2.5 g cm⁻³)로 추정한 `n_Li ≈ 8.8 × 10²¹` 와 **같은 자릿수** ⇒ 산수는 자기일관적이다. ⛔ **단 `D_vac` 는 공공 하나의 확산계수이고 σ 는 `c_vac` 를 0.05 % 로 *가정*해 얻은 것**이다. 실제 공공농도는 미지다 — 논문도 *"a target to reach"* 라고 자인.
🔴 **방법 결함 1건**: 본문이 *"MSD 기울기로는 안 된다 — **1D 에서는 방향성 확산이 없어 net zero motion random walk** 가 되므로"* 라고 쓰는데, **1D random walk 의 MSD 도 시간에 선형이고 D 를 준다.** 진짜 문제는 1D 단일파일(single-file) 상관운동에서 **tracer D 와 jump D 가 갈리는 것**이지 "net zero motion" 이 아니다. **이유가 틀린 채로 (결과적으로 더 안전한) hopping-rate 방법을 골랐다.**

---

## 4. 계산 방법 — 우리가 같은 축을 흉내 낼 때 필요한 조건 전부 ★

### 4a. 후보 선별 (67종 AIMD 대상)

| 항목 | 값 |
|---|---|
| 출처 | **Materials Project 62종 + ICSD 5종** (ICSD 5종 = Li₆NBr₃ 84090 · Li₄SiO₄ 35169 · Li₆ZnGe₂O₈ 100167 · Li₃Fe₂(PO₄)₃ 98361 · **Li₃PS₄ 180318**) |
| 열역학 필터 | 🔴 **본문 안에서 세 번 다르게 적는다**: Results *"within **50 meV/atom** from the convex hull"* / Methods *"`E_hull` < **0.1 eV/atom**"* / 스크린 적용 *"within **100 meV/atom** of the convex hull"* |
| 전자 필터 | **E_G > 0.8 eV** (훈련셋). ⚠ **스크린 적용 시엔 E_G > 1.5 eV** 로 올린다 |
| ICSD 물질 | 실험 존재로 안정 인정 + **자체 DFT 로 밴드갭·ΔE_rxn 계산** |
| 구조 제약 | **직방(orthorhombic) 표현이 가능한 결정만** |
| 화학 다양성 | 산화물·할라이드·질화물·폴리음이온 × 전이금속·붕소·탄소·규소·알칼리/알칼리토 |

### 4b. 계면 셀 만드는 법

| 항목 | 값 |
|---|---|
| 상대 전극 | **Li (mp-135) 의 (100) 면** |
| 직방화 | `a₃` = **가장 긴 격자벡터**로 잡아 그 방향으로 자른다(= SSE 구간을 최대한 길게) → `a₂′ = n a₁ + m a₂` (n,m ∈ ℤ) 로 `a₂′·a₁ ≈ 0` 을 **5 % 허용오차** 안에서 찾는다 |
| 변형 | SSE 원 셀을 **5 % 초과로 변형하지 않음**. 계면 면내 셀 파라미터는 **Li 와 SSE 격자상수의 평균** |
| 크기 | **총 원자 < 150**, 셀 ≈ **8 × 8 × 40 Å³** |
| **면 선택 기준** | 🔴 **물리가 아니라 비용** — *"the SSE surface that **yields the smallest cell**"*, *"chosen as to **minimize strain**"*. 저자 자인: *"Variations of reactivity in some SSEs may exist based on surface terminations"* |
| 초기 간극 | **1.8–3.0 Å**, *"SSE 표면 원소에 따라"* (할라이드는 Li 결합이 길어서 크게). ⚠ **물질별 실제 값은 미공개** |
| 계면 개수 | **셀당 2개** (PBC — 가운데 1 + 가장자리 1), **둘 다 반응성 판정에 쓴다** |
| **계면 이완** | 🔴 **0 K 사전 이완에 대한 서술이 없다.** 이완 기술은 *"ICSD 물질에 대해"* 만 나온다(힘 0.02 eV/Å, SCF 1e−3 eV). 평형화·온도램프·초기속도 규약 **전부 미기재** |

### 4c. AIMD

| 항목 | 값 |
|---|---|
| 코드 | **VASP** (PAW, ref 38·39) |
| 범함수 | **PBE** + **전이금속 화합물에만 rotationally-invariant Hubbard +U** (Dudarev), **pymatgen MP `RelaxSet`** 기본값. ⛔ **vdW 없음** · ⛔ **스핀 상태 선언 없음**(자화·`NUPDOWN` 0회) |
| ⚠ 인용 오류 | PBE 를 **ref 40 = Perdew, Burke, **Wang**, *PRB* **54**, 16533 (1996)** 로 인용 — 그건 PBE **exchange-correlation *hole*** 논문이고 PBE 범함수 원전(PRL 77, 3865, Perdew–Burke–**Ernzerhof**)이 아니다 |
| ecut | **500 eV** |
| smearing | **Gaussian, 0.05 eV** |
| **k-점** | **1 × 1 × 1 Γ-중심** (*"to improve run time"*, 큰 셀이라 Γ로 충분할 것이라 서술) |
| 앙상블 | **NVT + Nosé–Hoover** (VASP 구현) |
| **온도** | **550 K**. SSE 가 녹으면 **400 K 로 대체** (어느 물질이 그랬는지 **미공개**) |
| dt | **2 fs** |
| 길이 | **40–60 ps** (`Fig. 1`·`Fig. 4b` 는 40 ps) |
| **Li 상태** | **액체** — Li 융점 453.65 K 보다 높다. 저자 주장: *"액체 Li 가 더 반응성이므로 고체 Li 에 대한 **더 엄격한 기준**"* |
| 시드·반복 | 🔴 **계당 1회.** `seed`·`random_state`·`error bar`·`uncertainty`·`confidence interval`·`bootstrap` **전부 0회** |
| 선행 근거 | ref 17 (Camacho-Forero & Balbuena) — *"300 K 에서 10 ps 면 황화물 반응성을 잡기에 충분했고 50 ps 까지 늘려도 차이 없었다"* |

### 4d. 사후 DFT (pDOS)

- AIMD **최종 배열**에 대한 **정적 DFT** 1점.
- 같은 셋업이되 **k-그리드 3 × 3 × 1** (가장 긴 축만 단일 k-점).
- 대상: **passivating 10계**(`Fig. S3`) + **reactive 21계**(`Fig. S4`).
- 🔴 **결과: 전부 금속성.** 본문 자인 — *"**all calculations depict an electronically conductive system**, arising from **amorphous Li** in the high temperature computational cell."* (실독 확인: `Fig. S3` 10패널 · `Fig. S4` 21패널 **전부** `E−E_F = 0` 에서 tDOS ≠ 0).

### 4e. 머신러닝

| 항목 | 값 |
|---|---|
| 특징 | **Sendek et al.(ref 23) 의 구조 서술자 20개 + `ΔE_formation` + `ΔE_rxn`** = **22개** (`Table S1` 전수: AASD·AAV·AFC·ENS·LASD·LBI·LLB·LLSD·LNC·PF·RBI·RNC·SBI·SDLC·SDLI·SLPE·SLPW·SNC·SPF·VPA·ΔE_form·ΔE_rxn) |
| `ΔE_rxn` 출처 | **MP API 의 각 화학공간 상도** — ⛔ **혼합분율 규약·open/closed 규약 미기재**(§10-2) |
| `ΔE_form` 출처 | MP API (ICSD 는 자체 VASP + MP 보정에너지) |
| 모델 | **scikit-learn `LogisticRegression`**, **L2**, **LBFGS**, **정규화 강도 = 기본값** (*"regularization strength was found to not affect the final model performance … significantly"*) |
| 검증 | **`StratifiedKFold` 5-fold CV**, 라벨 비율 유지 |
| 특징 선택 | **N = 1..10 전수 조합 탐색** → 각 N 에서 CV 최소 조합 채택 ⇒ ✎ **총 1 744 435 개 모델** |
| 대안 특징셋 | **matminer**(magpie 조성 + DensityFeatures·BondFractions·MinimumRelativeDistances) 로도 해 봄 — **차이 없음**(`Fig. S7`, 이쪽은 **L1** + 정규화 강도 스캔) |
| 시각화 | **t-SNE**(scikit-learn), `Fig. 3c,d`·`Fig. S5` |
| 무작위추측 오분류 | Eq.(1) `E(RG) = 1 − Σ_class P(class)·G(class)`, `P = G` = 테스트셋 class 비율 |
| Baseline 오분류 | 다수 class 만 찍었을 때의 오차 |

### 4f. 이온전도도 검증 (붕소화물 2종 전용)

- **AIMD 500 / 700 / 900 K**, 각 **380–400 ps**, 셀 안의 **두 채널에 각각 Li 공공 1개** ([100] 방향).
- D 를 **MSD 기울기가 아니라 `1D Fick 1법칙` + 공공 hopping rate** 로 추정 (이유 서술은 §3h 참조 — 틀렸다).
- σ 는 **Nernst–Einstein**, **공공농도 = 전 Li 자리의 0.05 % 가정**.

### 4g. ⛔ 이 논문이 **하지 않은** 계산
**NEB 0 · Bader 0 · COHP/ICOHP 0 · ELF 0 · phonon 0 · 탄성상수 0 · BVSE 0 · grand-potential/ESW 0 · 표면에너지 0 · 접합일(W_ad) 0 · 무질서(SQS/enumeration) 0 · 계면상 두께 0 · 성장속도 0 · 면저항 0 · 전자전도도 수치 0 · 다중 시드 0 · 오차막대 0.**

---

## 5. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | **상단**: Li₂PNO₂(stable)·LiDyS₂(passivating)·Li₃InCl₆(reactive) 의 **t=0 / t=40 ps** 스냅샷. **하단**: 훈련셋 50종의 **`Norm. MSD` 막대**(cyan/gold/navy) | ⭐⭐ **보고량의 유일한 원자료.** 우리가 값을 픽셀 복원했다(§3b). 🔴 **y축이 1.0 에서 잘려 상위 3계가 클리핑**돼 있고(진값 1.058/1.118/**1.547**) 🔴 **NaLiSe 막대 색이 `Table 1` 라벨과 반대**다. ⭐ stable 19개가 **전부 같은 높이** = 그 영역 분해능 0 |
| 2a | **SM** 의 특징 개수별 오분류 (Training / 5-fold CV / ΔE_rxn 기준선 / baseline / random) | CV 최소 **0.08 @ N=8**, 단 **N=9·10 과 동률**. ΔE_rxn 단독 **0.22**. 🔴 170만 조합에서 고른 최솟값이라는 점이 그림에 안 적혀 있다 |
| 2b | **RM** 같은 그림 | CV 최소 **0.06 @ N=7**, **N=10 과 동률**. 50점에서 CV 양자는 0.02 이므로 0.06 vs 0.08 = **훈련점 1개 차이** |
| 3a | **ΔE_rxn vs AAV** 2-feature 결정경계 (teal ★ stable / gold × passivating / navy ● reactive) + 자홍 점선 = −0.1 eV/atom | ⭐ **"밀하면 안정"의 그림 증거**: SM 경계가 AAV 7.5 Å³ 에서 ΔE_rxn ≈ **−0.36** → 25.5 Å³ 에서 ≈ **0.0** 으로 **상승**(figure-read) = 작은 AAV 일수록 더 큰 구동력을 견딘다 |
| 3b | **ΔE_rxn vs Packing Fraction** 같은 그림 | SM 경계가 PF 0.1 의 **−0.09** → 0.85 의 **−0.23** 로 **하강**(figure-read) — 방향은 맞지만 **기울기가 얕다.** 저 PF 영역에서는 100 meV/atom 기준선과 **사실상 구분되지 않는다** |
| 3c | **3535 후보의 t-SNE**, `|ΔE_rxn| < 100 meV/atom` 기준 라벨 (**stable 229**) | 기존 기준의 시야 |
| 3d | 같은 t-SNE, **결합 모델 라벨** (stable **533** / passivating **788** / reactive **2214**) | 논문의 헤드라인 그림. ⚠⚠ **범례 색이 (a),(b) 와 뒤바뀐다** — (a,b) teal=Stable·gold=Passivating 인데 (c,d) 는 **gold=Stable·teal=Passivating**. `Fig. 1` 과도 반대. **한 그림 안에서 색 규약이 갈린다** |
| 4a | LiB₁₃C₂ · LiB₁₂PC **결정구조** + 1D Li 채널 | 붕소 icosahedron 골격 |
| 4b | 두 붕소화물의 **Li 계면 AIMD 0 → 40 ps** | 격자 무변화 = stable 의 시각 증거 |
| 4c | **채널 폭**(3.52–3.94 Å) + **D_vac / σ_Li 아레니우스** (좌축 10⁻⁶–10⁻³ cm²/s, 우축 10⁻⁴–10³ S/cm, x = 1000/T 1.0–3.5) | 3점 적합 + **300 K 는 외삽(마름모)**. ⚠ **오차막대 없음**, 시드 1개 |
| S1 | LiDyS₂ vs Li₆ZnGe₂O₈ (passivating/reactive **경계 2계**) 스냅샷 | (안 봄 — 본문 서술로 충분. 경계 판정이 눈으로 이뤄졌다는 증거로 존재 자체가 의미) |
| S2 | **`Norm. MSD` vs ΔE_rxn 산점** (훈련셋 50) | ⭐⭐ **`Fig. 1` 의 클리핑을 여기서 잡았다.** x축이 **0 → 1.6** 까지 간다. 캡션은 *"ΔE_formation"* 이라 적는데 **y축 라벨과 본문은 ΔE_rxn** — 캡션 오기 |
| S3 | **passivating 10계의 최종 pDOS** | ⭐⭐ **부동태화 판정의 핵심 그림.** 실독: **10개 전부 E_F 에 유한 DOS** (Li₆FeCl₈ 는 Fe 3d 가 E_F 에 크게 걸린다). ⇒ **전자적 부동태 기준을 시도했다가 포기한 자리** |
| S4 | **reactive 21계의 최종 pDOS** | 실독: **21개 전부 E_F 에 유한 DOS.** Li\|Li₃PS₄·Li\|Li₇P₃S₁₁·Li\|Li₁₀GeP₂S₁₂ 에서 S(음이온) 기여는 −1 eV 위로 사라지고 E_F 의 상태는 **원소 투영이 없는 tDOS** = **액체 Li** 다 |
| S5 | 훈련셋의 **t-SNE 상 분포**(주황 = 훈련셋) | (안 봄 — 대표성 주장의 근거 그림) |
| S6 | 예측 3군의 **ΔE_rxn 히스토그램** | (안 봄 — **xlsx 원자료로 직접 계산하는 편이 정확**해서 그렇게 했다. §3f. 본문 서술과 100–125 meV/atom 어긋남 발견) |
| S7 | **matminer 특징셋 vs Sendek 특징셋** 학습 비교 (L1) | (안 봄 — 결론 *"차이 없다"* 는 본문에 명시) |
| Table 1 | 훈련셋 50종 (조성·ref·ΔE_rxn·라벨) | **PDF 텍스트로 전사** (표는 텍스트가 정확) |
| Table 2 | **검증셋 17종 + 예측 + 오분류율 3종** | ⭐ **이미지 표라 텍스트 추출이 안 된다** → `tab_2.png` 실독 전사(§3c). 같은 크롭에 `Fig. 4` 가 통째로 들어 있어 그것도 같이 읽었다 |

---

## 6. Post-processing ★

| 기법 | 썼나 | 도구·세부 |
|---|---|---|
| **계면수직 MSD + 평면교차 판정** | ✅ (**이 논문의 보고량**) | 자체 구현, 코드 미공개. §3a |
| **pDOS (정적, AIMD 최종배열)** | ✅ | VASP, **3×3×1 k**. `Fig. S3`·`S4`. **결과적으로 판정에 못 쓴다** |
| **convex hull / ΔE_rxn** | ✅ (남의 것) | **MP API 상도** — 직접 계산 아님. 혼합분율 규약 미기재 |
| **로지스틱 회귀 + 전수 특징탐색** | ✅ | scikit-learn, L2/LBFGS, 5-fold Stratified CV, **1.74 M 조합** |
| **t-SNE** | ✅ | scikit-learn, `Fig. 3c,d`·`Fig. S5` |
| **matminer 대안 특징** | ✅ | magpie + DensityFeatures/BondFractions/MinimumRelativeDistances, **L1** (`Fig. S7`) |
| **hopping-rate → 1D Fick → Nernst–Einstein** | ✅ (붕소화물 2종만) | 380–400 ps AIMD, **c_vac = 0.05 % 가정** |
| NEB · Bader · COHP · ELF · phonon · 탄성 · BVSE · ESW/grand-potential · 표면에너지 · W_ad | ❌ | **전부 0회** (§4g) |

---

## 7. 결과 — 섹션별 상세 (그림 실독 포함)

### 7.1 데이터셋 생성 (§"Generating the Data Set of Li|SSE", `Fig. 1`)
- 67종 중 50종을 훈련용으로 AIMD. 550 K 40 ps. 셀당 계면 2개.
- 세 라벨의 **정성 정의**:
  - **stable** — *"nearly **zero crossing** of non-Li('sublattice') atoms over the original interfaces"*
  - **passivating** — *"limited reactivity, or change in position of SSE sublattice atoms, **only near** the original interfaces"*
  - **reactive** — *"transport of SSE sublattice atoms **far from** the original interfaces, and also … Li metal atoms **flowing into** the SSE section, substantially changing the coordination environment"*
- ⭐ **정직한 자기한계 1**: *"Li₂PNO₂ 는 우리 AIMD 로는 stable 인데 **실험적으로는 passivating** 이다"* (ref 18, Schwöbel LiPON XPS). ⇒ **AIMD 라벨도 예측일 뿐**이라고 스스로 적는다.
- `Fig. 1` 상단 실독: Li₂PNO₂ 는 40 ps 뒤에도 P–N–O 골격이 그대로이고 녹색(Li 금속)만 무질서해진다. LiDyS₂ 는 Dy–S 격자가 유지되고 계면에서만 섞인다. **Li₃InCl₆ 는 40 ps 뒤 셀 전체가 녹색(Li) 그물이 되고 In(분홍)이 흩어진다** — 세 라벨의 시각 정의가 그림 하나에 다 들어 있다.

### 7.2 전자적 부동태를 확인하려 했고, 실패했다 (`Fig. S3`·`Fig. S4`)
- 동기 문장이 명시적이다: *"Previous … work has shown Li|SSE interfaces can be effectively stable by forming **passivating products that are electronically insulating**(refs 20–22). **Following this line of thinking**, we include results of pDOS …"* ⇒ **문헌의 부동태 정의(= 전자절연)를 적용해 보려 한 것이 맞다.**
- 결과: *"**all calculations depict an electronically conductive system**, arising from amorphous Li in the high temperature computational cell."*
- 그래서 pDOS 는 **원소별 기여로 "SSE 가 어떻게 변했나" 를 보는 보조 도구로 격하**된다. passivating 10계 중 **Li₆FeCl₈ 만** E_F 에 큰 Fe 상태를 보이고, 저자는 그것을 *"SSE 표면의 Fe 가 액체 Li 로 녹아 들어갔지만 나머지 SSE 는 그대로"* 라고 읽는다.
- reactive 쪽(`Fig. S4`)에 대해서는 더 결정적인 자인이 나온다: *"a few materials show **clear signs of being an insulator**. For these cases, **all of the original SSE cell reacts** … **due to our limited computational cell size** … **we do not capture a passivating behavior that may be present at larger computational cell sizes.** Hence we decide to predict these materials as **reactive out of caution**."*
  🔴 **즉 passivating/reactive 경계의 실질 결정자는 물리가 아니라 셀 크기다** — 저자 본인의 문장이다.

### 7.3 분류기 학습 (`Fig. 2`, `Table S2`)
- 두 개의 이진 분할: **SM**(stable | passivating+reactive) · **RM**(stable+passivating | reactive).
- ⚠⚠ **약어 정의가 논문 안에서 두 번 갈린다**:
  - **Results**: *"the 'stable model' (SM), which uses the stable vs passivating/reactive data split"* / *"the 'reactive model' (RM), which uses the stable/passivating vs reactive split"*.
  - **Methods & Conclusion**: *"one grouping passivating with reactive (a '**reactive model**') and one grouping passivating and stable (an '**unreactive model**')"* / 결론 *"a '**reactive model**' (**SM**) … and an '**unreactive model**' (**RM**)"*.
  ⇒ **Results 와 Methods/Conclusion 이 SM·RM 의 의미를 서로 바꿔 쓴다.** `Table S2` 는 7-feature 모델을 *"Passivating Model"* 이라 부른다 — **세 번째 이름**이다.
- ΔE_rxn 단독 대비 **3–4배 낮은 오분류**를 주장. (CV 기준으로는 맞다. 홀드아웃 기준으로는 35.3 % vs ΔE_rxn 22–26 % 로 **오히려 나쁘다** — §13-⑤.)

### 7.4 해석 (`Fig. 3a,b`)
- **밀도 서사**: *"The importance of **atomic density** to SSE interfacial stability suggests that **dense materials are more stable** against the driving force to mix with Li metal. This may be due to the **lower mobility of species**, and hence **limited reaction pathways**, in tightly packed lattices."*
- **이온성 서사**: SBI 가 반응성과 역상관 ⇒ *"**short and ionic bonding** in the SSE may be key to stabilizing the crystal when interfaced with Li metal."*
- ⭐ **그리고 트레이드오프를 스스로 적는다**: *"Since a **high packing fraction could lead to smaller and less accessible Li diffusion pathways** …, **optimizing for both stability and conductivity will be key**."* ← **우리에게 가장 불리한 문장**(§14-②).

### 7.5 스크린 확장 (`Fig. 3c,d`)
- 대상 **3535** = MP 의 Li 함유 화합물 중 `E_hull ≤ 100 meV/atom` **AND** `E_G > 1.5 eV`.
- **SM 단독**: stable **599** (기존 229 대비 크게 증가). 그중 **32개는 `|ΔE_rxn| < 100 meV/atom` 인데 새로 reactive 판정** = 기존 기준이 stable 이라 하던 것을 뒤집음.
- **RM 단독**: stable/passivating **1321**.
- **두 모델 불일치**: RM 이 reactive 라 한 것 중 **59개를 SM 은 stable** 이라 한다 — 저자가 *"seemingly contradicting each other"* 라 인정.
- **결합 규칙** (최종):
  1. **stable** = SM·RM 둘 다 stable → **533**
  2. **passivating** = SM 은 reactive, RM 은 stable → **788**
  3. **reactive** = RM 이 reactive → **2214**
  ⚠ 이 규칙은 **"SM stable & RM reactive"(59개)** 를 **reactive 로 흡수**한다 — 규칙 3이 규칙 1을 이긴다. 명시는 안 하지만 숫자가 그렇게 맞는다.
- ✎ **우리 검산**: 533+788+2214 = **3535** ✓ / `|ΔE_rxn|<0.1` 짜리 180+31+18 = **229** ✓ (§3f).

### 7.6 질화물 사례 3건 (논문이 제일 공들인 논증)
- `Li₆WN₄`(본문은 **"Li₆WN₂"** 로 오타) — ΔE_rxn = 0 인데 AIMD 가 계면에서 **LiN 계 종** 형성을 본다 ⇒ passivating 최저.
- `Mg₃N₂` (ΔE_rxn = **24 meV/atom**) · `BN` (**34 meV/atom**) — 구동력이 거의 없는데 **실험(XPS)에서 반응해 Li₃N 을 만든다** (refs 25, 26).
- `C₃N₄` (ΔE_rxn = **763 meV/atom**) — 구동력이 큰데도 **부분 반응 후 Li₃N 을 만들고 부동태화**한다 (ref 27).
- ⇒ *"ΔE_rxn 은 하나의 지표일 뿐"* 이라는 결론. ⭐ **이 세 예가 논문에서 가장 설득력 있는 부분이다** — 실험 앵커가 붙은 유일한 자리.
- ⚠ 단 **Mg₃N₂·BN·C₃N₄ 는 셋 다 훈련셋에도 검증셋에도 없다.** 논증은 문헌 인용이고 자체 계산이 아니다.

### 7.7 붕소화물 (`Fig. 4`) — §3h

---

## 8. 논증 흐름 종합

```
 [문제]  "|ΔE_rxn| < 100 meV/atom" 하나로 전 물질을 자른다 → 구조·기구 무시 → 오라벨
    │
    ▼
 [증거]  550 K · 40 ps AIMD 50계 × 1회
    │        └─ 사람이 스냅샷을 보고 stable / passivating / reactive 를 붙인다  ← ★ 라벨의 1차 출처
    │        └─ 그 뒤 Norm. MSD 로 "형식화"한다 (stable < 0.05 · 나머지 경계는 숫자 없음)
    │        └─ pDOS 로 전자적 부동태를 확인하려다 실패 (액체 Li 가 전부 금속성으로 만든다)
    ▼
 [모형]  22 특징 → 로지스틱 회귀 2개 (SM·RM), 1.74M 조합에서 CV 최소 선택
    │        └─ 지배 특징은 여전히 ΔE_rxn (계수 −1.26 / −2.15, 2위의 1.6–2.2배)
    │        └─ 구조 특징은 "밀하고 이온성이면 안정" 방향
    ▼
 [확장]  MP 3535 구조 → stable 533 · passivating 788 · reactive 2214
    │        └─ 229 → 1321 로 "살아남는 후보"를 5.8배 늘린다
    ▼
 [검증]  홀드아웃 17종 (단, 고전도 예측 물질로 편향 선택) → 오분류 35.3 %
    │        └─ 오류 6건 전부 "passivating" 예측에서 나온다
    │        └─ 그중 3건을 "그래도 쓸 만하다"로 재분류 → 17.6 % 로 다시 적는다
    ▼
 [산출]  LiB₁₃C₂ · LiB₁₂PC — Li 금속에 안정 + σ(300 K, 가정) 1.3e−3 / 4.4e−4 S/cm
```

**논문이 실제로 보여 준 것 / 보여 주지 못한 것**

| 주장 | 근거의 강도 |
|---|---|
| *"ΔE_rxn 단독 문턱은 불완전하다"* | ✅ **탄탄하다.** `Fig. S2` 의 산포 + 질화물 3건 실험 앵커 |
| *"유한온도 AIMD 가 추가 정보를 준다"* | ✅ 그럴듯하다 (단 1 시드·40 ps·≤150원자) |
| *"그 정보를 값싼 구조 서술자로 배울 수 있다"* | 🟡 **홀드아웃에서 35.3 %** — 무작위(63.7 %)보단 낫고 baseline(58.2 %)보단 낫지만, **ΔE_rxn 단독의 CV 22–26 % 보다 나은지는 증명되지 않았다**(같은 홀드아웃에서 ΔE_rxn 단독을 재 보지 않았다) |
| *"533개가 stable, 788개가 passivating"* | 🔴 **숫자의 신뢰구간이 없다.** 35.3 % 오분류를 그대로 적용하면 533 중 ~190개가 오라벨일 수 있다 |
| *"LiB₁₃C₂·LiB₁₂PC 가 유망하다"* | 🟡 **후보로는 설득력 있다.** σ 는 **가정된 공공농도**에 선형이고 40 ps AIMD 1회 뿐 |

---

## 9. ★★ 1저자 지정 임무 — ① 보고량 · ② 선점 · ③ 부동태화 · ④ 데이터

### 9-1. ① **보고량이 정확히 무엇인가** — 스크리너인가 기전 연구인가

**성격 판정: 압도적으로 스크리너다.** 기전은 없다.
- 반응 **경로**를 추적하지 않는다 (NEB 0, 중간체 동정 0, 결합수 분석 0, 전하이동 분석 0).
- 반응 **산물**을 동정하지 않는다 — 유일한 예외가 `Li₆WN₄` 의 *"LiN-type species"* 라는 한 구절이고 그조차 정량이 없다.
- 반응 **속도**를 재지 않는다 (동일 온도에서의 시간의존 곡선 0, Arrhenius 0 — 붕소화물 σ 는 별개 축).
- ⇒ **"이 계면이 반응하는가 예/아니오" 를 싸게 답하는 도구**다.

**예측하는 스칼라 = `Norm. MSD` (§3a)** — 계면수직 1D MSD 의, 계면을 넘은 sublattice(+조건부 Li) 원자 평균을, SSE 두께로 나눈 것. 단위 **Å**.
**그 스칼라 자체가 최종 출력은 아니다.** 최종 출력은 **3분류 라벨**이고, 스크린 단계에서는 **두 로지스틱 회귀의 결합 라벨**이다.

**문턱과 근거 (재정리)**

| 문턱 | 값 | 근거 | 우리 판정 |
|---|---|---|---|
| 열진동 배경 | ≈0.1 Å² | **1937년 Zn X선 논문**(ref 19) | 🟡 눈금으로는 쓸 수 있으나 **Li/황화물에 대한 값이 아니다** |
| 원자 "반응" 판정 | **0.5 Å²** | 배경의 5배, **배수 근거 없음** | 🟡 임의값 |
| stable 상한 | **0.05** | **근거 문장 없음** (관측 분리) | 🟡 사후 |
| **passivating ↔ reactive** | 🔴 **없음** | *"between"* + **눈으로 판정** | 🔴 **정의되지 않음** |
| (공격 대상) ΔE_rxn 문턱 | 100 meV/atom | *"4 k_BT at RT"* (= 103 meV) | — |

⚠ **아이러니**: 논문은 *"하나의 임의 문턱(100 meV/atom)"* 을 공격하면서 **두 개의 근거 없는 문턱(0.5 Å², 0.05)과 한 개의 숫자 없는 문턱(passivating/reactive), 그리고 사람의 눈**으로 대체한다.

**🔴 우리 규율에 걸어 보기 — *"admissible state 가 여럿인데 선택·집계 규칙이 없으면 스칼라 보고량은 정의되지 않는다"***

| admissible state 의 원천 | 논문이 선택·집계 규칙을 선언했나 |
|---|---|
| **표면 종단(termination) / 면방위** | 🟡 **부분 선언** — *"변형 최소 + 셀 최소"*. **물리적 선택규칙이 아니라 비용 규칙**이고, 저자가 *"종단에 따라 반응성이 다를 수 있다"* 고 자인한 뒤 *"대표한다고 **가정**한다"* 로 넘어간다 |
| **직방화 `a₂′ = n a₁ + m a₂` 의 (n,m) 선택** | 🟡 `a₂′·a₁ ≈ 0` 을 5 % 안에서 만족하는 것 — **유일하지 않은데 유일성 규칙이 없다** |
| **초기 간극 1.8–3.0 Å** | 🔴 *"표면 원소에 따라"* 만 있고 **물질별 값 미공개** ⇒ 재현 불가 |
| **MD 시드 / 궤적** | 🔴 **없다.** 계당 **1회**, 반복 0, 오차막대 0, 앙상블 평균 0 |
| **온도 (550 K vs 400 K)** | 🔴 *"녹으면 400 K"* — **어느 물질이 그랬는지 미공개** ⇒ 같은 표 안에 **두 온도의 값이 섞여 있는데 구분이 불가능** |
| **다형(polymorph)** | 🔴 **없다.** 스크린은 mp-id 단위로 라벨하고, **87개 조성이 다형에 따라 서로 다른 라벨**을 받는다(§3f). 조성 단위로 질문하면 답이 두 개다 |
| **개열 스핀/산화상태** (Fe·Mn·V·Ti·W 계) | 🔴 **없다.** `+U` 만 켰다고 적고 **스핀 상태·자화·`NUPDOWN` 을 한 번도 선언하지 않는다.** `Li₆FeCl₈` 는 논문이 직접 *"Fe states at the Fermi energy"* 를 논하는 **열린 껍질·산화환원 활성 계**다 |

⇒ **판정: 이 논문의 스칼라 보고량은 우리 규율 기준으로 정의되지 않았다.** 선언된 것은 **구조 선택 규칙 하나(비용 최소)** 뿐이고, **궤적 집계 · 다형 집계 · 상태 선택 규칙이 전부 없다.** 그리고 정작 최종 라벨은 스칼라가 아니라 **사람의 시각 판정**이다.
⭐ **`Li₆FeCl₈` 는 우리 `kb/methodology/estimand_before_running_2026_08_28.md` §2.1 의 교과서 사례다** — 열린 껍질 + 자성 + 산화환원 활성이 전부 있는데 상태 선언이 0. 우리 SDCP 8회 반려의 원인과 **같은 층위**다.

### 9-2. ② 🔴 **선점 판정 — 인접(adjacent)·겹침 거의 없음**

> **구분선 (한 문장)**
> **[Lomeli24] 는 *분해가 시작되는 순간* 을 550 K · 40 ps AIMD **한 번**으로 보고 그 라벨을 MP 3535 구조에 외삽하는 **넓고 얕은 음극측 스크리너**이고 — 그 3535 목록에 `Li₆PS₅Cl` 은 **아예 없다** — 우리는 *분해가 끝난 뒤의 산물·전자구조·역학* 을 도핑된 아르지로다이트 네 계에서 깊게 보는 쪽이므로, 두 연구는 같은 음극 계면의 **넓이와 깊이를 나눠 맡는다.****

| 우리가 하는/하려는 것 | [Lomeli24] 가 했나 | 판정 |
|---|---|---|
| **SE ‖ NCM (양극측)** 모든 것 | ❌ `cathode` **1회**(향후과제) | 🟢 **완전 무관** |
| SE **벌크** 이온수송·Ea·D (축 A) | ❌ (붕소화물 2종 예외) | 🟢 무관 |
| SE **ESW / grand-potential 산화창** (축 B) | ❌ **0회** — `ΔE_rxn` 은 **MP 에서 가져다 쓴 특징**이지 자체 계산이 아니다 | 🟢 무관 |
| SE **탄성 / EOS / phonon** (축 C) | ❌ | 🟢 무관 |
| SE **밴드갭·DOS·ICOHP·ELF·Bader** (축 D) | 🟡 pDOS 만, 그것도 **판정 실패** | 🟢 사실상 무관 |
| **아르지로다이트(`Li₆PS₅Cl`) 의 Li 금속 반응성** | 🔴 **목록에 없다.** 가장 가까운 것 = `Li₆PS₅I` **reactive**(예측), `Li₅P(S₂Cl)₂` **reactive**(예측) | 🟡 **인접 — 대리값만** |
| **`Li₃PS₄`·`Li₇P₃S₁₁`·`Li₁₀GeP₂S₁₂` 의 Li 금속 반응성** | ✅ **AIMD 로 직접 했다** (전부 reactive, `Norm. MSD` 0.55–0.91) | 🔴 **여기만 겹친다** — 우리가 같은 계를 AIMD 로 다시 하면 중복 |
| **0 V 분해산물(Li₂S·Li₃P·LiCl)의 Li 금속 안정성** | ✅ Li₂S·Li₃P 는 **AIMD stable**, LiCl 은 스크린 stable | 🔴 **겹친다** (우리 `sei_products.json` 의 *"어떤 상이 나오나"* 와는 다른 질문 — **그 상이 Li 와 더 반응하나**) |
| **Cl 함량(x)이 음극 반응성을 바꾸는 효과** | ❌ (Cl 스윕 0, 아르지로다이트 0) | 🟢 **공백** |
| **O / B₂O₃ / Nd 도핑 효과** | ❌ (단 `Li₃BO₃` **stable** · `LiBO₂`·`Li₂B₄O₇` **passivating** 이라는 산물측 정보는 있다) | 🟢 **공백 (+ 인접 참조값)** |
| **무질서(Cl/S 자리)** | ❌ **0회** — 정렬된 MP/ICSD 셀만 | 🟢 **공백** |
| **부동태화의 두께·성장속도·자기제한** | ❌ **0회** (§9-3) | 🟢 **공백 — 둘 다 못 한다** |
| **계면 접합/접착(W_ad)** | ❌ **0회** (같은 그룹의 ref 11 이 그 축) | 🟢 무관 ([Wang22Res] 가 그 자리) |
| 구조 서술자 기반 argyrodite 회귀 (우리 cascade descriptor v0) | 🟡 **같은 Sendek 22 특징을 쓴다** — 다만 타깃이 **Ea 가 아니라 계면 반응성 라벨** | 🟡 **인접 — 표현(representation) 재사용 가치 있음** (§J-17 `[Zhao21HECS]` 와 짝) |

**⇒ 최종 판정: 🟡 인접(adjacent).** 🔴 칸은 **둘뿐**이고 **둘 다 우리가 하려던 계가 아니다**(Li₃PS₄/Li₇P₃S₁₁/LGPS 는 비교군이지 주인공이 아니고, 분해산물의 "추가 반응성" 은 우리 산물표가 답하는 질문이 아니다). **우리 4축(A/B/C/D) 과의 중복은 0 이다.**

### 9-3. ③ 🔴🔴 **부동태화(passivation) 를 무엇으로 판정하나** — 1저자 최우선 질문

**(a) 조작적 정의**

> **passivating = 550 K · 40 ps AIMD 후에도 SSE sublattice 골격이 유지되고, 원자 재배치가 *원래 계면 근처에만* 머무르며, Li 가 SSE 안으로 들어가 완전 반응시키지 않은 상태. 스칼라로는 `Norm. MSD` 가 stable(<0.05)과 reactive(figure-read ≳0.31) 사이.**

핵심은 **"셀 안에서 반응영역이 공간적으로 갇혔나"** 하나다. 즉
- ✅ **전자전도도 기준이 아니다** — 시도했고 실패했다(§7.2).
- ✅ **두께 기준이 아니다** — `thickness` 0회.
- ✅ **이온/전자 수송비 기준이 아니다** — 두 수송 중 어느 것도 계면에서 계산하지 않는다.
- ✅ **자기제한(self-limiting) 기준이 아니다** — `self-limit` 0회, 시간의존 반응두께 곡선 0개.
- ✅ **성장속도 기준이 아니다** — `t = 0` 과 `t = 40 ps` 두 점뿐.

**(b) 계산으로 나온 양인가, 가정인가 — 층을 갈라야 한다**

| 층 | 계산? | 판정 |
|---|---|---|
| ① `Norm. MSD` 스칼라 | ✅ **계산이다** (궤적에서 직접) | 재현 가능한 양 (단 코드·원자료 미공개) |
| ② `stable / passivating / reactive` **3분류** | 🔴 **사람이 눈으로 붙였다** (`Fig. 1` 캡션 "by inspection") | 스칼라는 **사후 형식화** |
| ③ *"passivating = 실제 셀에서도 반응이 멈춘다"* | 🔴🔴 **순수 가정** | 논문 어디에도 근거 없음 |
| ④ *"passivating 층은 전자절연이다"* | 🔴🔴 **검사했고 확인 못 했다** (`Fig. S3` 10/10 금속성) | **문헌 정의를 빌려 왔다가 자기 데이터로 못 받친다** |
| ⑤ *"reactive 중 일부는 큰 셀에서는 passivating 일 것"* | 🔴 **저자가 직접 인정** (§7.2 인용) | ⇒ **경계가 셀 크기 의존** |

**(c) 우리가 그 정의를 가져올 수 있나 — 🟡 조건부 가능. 가져오려면 네 가지를 더해야 한다.**

| 가져올 것 (그대로 쓸 수 있는 부분) | 왜 쓸 만한가 |
|---|---|
| **양쪽 계면 주기셀 + "원래 계면 평면" 정의** (= 바깥 SSE 원자와 금속 원자의 중간면) | 애매함 없이 자동화된다. 우리 MLIP 슬랩에 그대로 이식 가능 |
| **계면수직(z) MSD + 평면교차 필터** | 계면 반응을 **벌크 확산과 분리**하는 값싼 방법. 우리 벌크 MSD 규약(2–50 ps)과 충돌하지 않는다 — **다른 양**으로 따로 둔다 |
| **sublattice(비-Li) 원자만 세는 것** | Li 의 정상 확산이 반응 신호를 가리는 것을 막는다 ⭐ **이 한 수가 영리하다** |
| **"unstable 이면 넘어온 Li 도 포함" 규칙** | Li 가 SSE 로 침투하는 반응(우리 Li₃P 생성 경로)을 잡는다 |

| 🔴 반드시 고쳐야 할 것 | 이유 |
|---|---|
| **① `L_SSE` 로 나누는 정규화를 버린다** | 🔴🔴 **부동태화 지표로서 방향이 반대다.** 반응 전선이 고정 깊이에서 멈추면(= 진짜 부동태) 분자는 상수인데 분모만 커지므로, **SE 를 두껍게 만들수록 같은 물질이 reactive → passivating 으로 이동한다.** 저자가 §7.2 에서 인정한 셀 크기 의존이 바로 이 정규화다. ⇒ **우리는 `L_reacted(t)` 를 Å 로 직접 보고한다** |
| **② 시간점을 최소 3개 이상 둔다** | 부동태화의 정의는 **`dL_reacted/dt → 0`** 이다. 두 점(0, 40 ps)으로는 원리적으로 판정 불가 |
| **③ SE 두께 수렴 시험** | *"반응 전선이 셀을 다 먹었다"* 와 *"정말 반응성이다"* 를 가르는 유일한 방법. [Wang22Res] `Fig. S10` 형식 |
| **④ 전자 기준을 *반응층에만* 투영한다** | 그들의 실패는 **고칠 수 있다** — 셀 전체 DOS 대신 **계면상 슬랩에만 투영한 PDOS**(또는 액체 Li 영역을 공간적으로 배제)로 보면 된다. 우리는 이미 `sei_electronic.json` 에서 산물별 갭을 갖고 있으므로 **상별 갭 + 연속성** 두 가지로 갈 수 있다 |

**(d) ⇒ 한 문장 결론**
**이 논문은 부동태화를 "반응이 셀 안에서 국소적으로 머무르나" 로 정의하고, 그 정의가 셀 크기에 의존한다는 것을 스스로 인정하며, 전자적 부동태 기준은 시도했다가 액체 Li 때문에 포기했다. ⇒ 우리가 "부동태화를 못 재고 있다" 는 공백은 이 논문으로 메워지지 않는다. 다만 *반응영역을 공간적으로 분리해 세는 기법* 은 그대로 빌릴 수 있고, 거기에 시간축·두께수렴·상별 전자기준을 붙이면 우리가 그들보다 먼저 진짜 부동태 지표를 가질 수 있다.**

### 9-4. 🔎 검색 실측 (PDF → 텍스트 전수, 본문 = 참고문헌 제외 / SI)

| 검색어 | **본문** | **SI** |
|---|---|---|
| `argyrodite` | **0회** | 0회 |
| `Li6PS5` | **0회** | 0회 |
| `Li3PS4` / `Li7P3S11` / `Li10GeP2S12` | 1 / 1 / 1 (전부 `Table 1` 행) | 0 |
| `passivating` / `passivation` | **60 / 1** | 7 / 1 |
| `thickness` | **0회** | 0회 |
| `self-limit` | **0회** | 0회 |
| `electronic conductivity` | **1회** (후보 선별 문구) | 0회 |
| `interphase` / `SEI` | **0 / 0** | 0 / 0 |
| `grand potential` / `ESW` / `electrochemical stability window` | **0 / 0 / 0** | 0 |
| `NEB` / `nudged` | **0 / 0** | 0 |
| `band gap` (`bandgap` 4회) | **0회** | 0 |
| `adhesion` / `surface energy` / `work of adhesion` | **0 / 0 / 0** | 0 |
| `ASR` / `area specific resistance` / `impedance` | **0 / 0 / 0** | 0 |
| `disorder` / `SQS` | **0 / 0** | 0 |
| `cathode` | **1회** (결론의 향후과제) | 0 |
| `Li-In` / `NCM` / `NMC` | **0 / 0 / 0** | 0 |
| `vdW` / `van der Waals` | **0 / 0** | 0 |
| `spin` / `magnet` | **0 / 0** | 0 |
| `Hubbard` / `+U` | 1 / 1 | 0 |
| `seed` / `error bar` / `uncertainty` / `confidence interval` / `bootstrap` | **0 / 0 / 0 / 0 / 0** | 0 |
| `melt` / `liquid Li` | 5 / 3 | 0 |
| `550 K` / `400 K` | 8 / 2 | 0 |
| `vacancy` | 14 (전부 붕소화물 σ 절) | 0 |

👉 **아르지로다이트는 한 번도 언급되지 않는다.** 그리고 **부동태화를 60번 말하면서 두께·전자전도도·자기제한은 0번 말한다.**

---

## 10. 우리 DFT / `db/properties` 대비 ★★ (판정하지 말고 나란히)

기준: `litdb/our_dft_baseline.md` + `db/properties/`.

### 10-1. 방법 대조표

| 항목 | **[Lomeli24]** | **우리** | 비고 (판정 아님) |
|---|---|---|---|
| 코드 | **VASP** (PAW) | **QE** (+GPU) | 총에너지 절대값 비교 불가 |
| 범함수 | **PBE** | PBE | 같은 층위 |
| **+U** | **전이금속 화합물에만**, pymatgen MP `RelaxSet` | 없음 (우리 계에 TM 없음) | 우리 계엔 해당 없음. 단 **그들 훈련셋의 Fe/Mn/V/Ti/W/Nb 계 10여 종은 +U 값이 어느 것인지 미기재** |
| vdW | **없음** | 없음 | 같다 |
| **스핀** | 🔴 **선언 없음** (자화·NUPDOWN 0회) | 우리도 비자성계라 해당 없음 | ⚠ 그들 쪽이 **열린 껍질 계를 포함**하는데 선언이 없다 |
| ecut | **500 eV** (≈36.7 Ry, PAW) | 70 / 560 Ry (norm-conserving 규약) | **규약이 달라 직접 비교 불가** |
| **k-점** | **Γ-only (1×1×1)** — 계면 AIMD 전량. pDOS 만 3×3×1 | 계별 지정 (예: `comp1_V0_k444`) | 🔴 **그쪽이 훨씬 성기다** |
| 셀 크기 | **< 150 원자**, ≈8×8×40 Å³ | MLIP-MD **558 원자** (box331), DFT 셀은 계별 | 🔴 그쪽이 작다 |
| **MD 종류** | **AIMD** (진짜 DFT 힘) | **MLIP** (UMA-s-1p1 omat) | ⭕ **그쪽이 원리적으로 정확**, 우리는 길이·크기·시드로 산다 |
| 앙상블 | NVT + **Nosé–Hoover** | **Langevin NVT** (friction 0.02) | 써모스탯이 다르다 |
| dt | **2 fs** | 2 fs | 같다 |
| **온도** | **550 K 단일** (일부 400 K, 어느 것인지 미공개) | **600 / 800 / 1000 K 3점** (400/500 K 제외 판정) | ⚠ 그들 550 K 는 **우리가 제외한 창**(600 K 미만)에 가깝다 |
| **길이** | **40–60 ps** (계면), 380–400 ps (붕소화물 σ) | 평형 5 ps + **생산 200 ps** (일부 400 ps) | 🔴 **우리가 5–10배 길다** |
| **시드 / 앙상블** | 🔴 **1** (반복 0, 오차막대 0) | **멀티시드 필수** (modelc 3-seed ±0.032 eV, 유리계는 구조시드 5 의 IQR) | ⭕⭕ **우리가 크게 낫다** |
| **무질서** | 🔴 **0** (정렬 MP/ICSD 셀) | SQS·disorder ensemble·시드 명시 | ⭕⭕ **우리가 낫다** |
| MSD 규약 | **계면수직 1D**, 평면교차 필터, `L_SSE` 정규화, **창 미기재** | **3D**, `MSD/6t`, **창 2–50 ps 고정**, 자유절편, MTO | 🔴 **완전히 다른 양** — 같은 표에 놓을 수 없다 |
| σ 산출 | 붕소화물만, **NE + 공공농도 0.05 % 가정** | NE(Haven=1), **절대값 인용 금지** | 둘 다 NE. 그쪽은 **농도 자체가 가정** |
| 재현성 | 🔴 코드·궤적·`Norm. MSD` 원자료·물질별 간극·400 K 대상 **전부 미공개**. 공개된 것은 **xlsx 라벨표 하나** | 우리 `db/properties/*.json` + `source_path` | ⭕ 우리가 낫다 |

### 10-2. 값 대조 — 무엇을 옮겨도 되고 무엇은 안 되나

| 양 | [Lomeli24] | 우리 | 이식 가능? |
|---|---|---|---|
| **`ΔE_rxn` (eV/atom)** | MP API 상도에서 가져온 값. 예: `Li₃PS₄` −0.708 · `Li₇P₃S₁₁` −0.805 · `Li₆PS₅I` −0.565 | `interface_reactivity` / ΔH_D 계열 (예 −0.3227 eV/atom) | 🔴🔴 **금지.** ⓐ **혼합분율 규약 미기재** (min over x 인지 x=0.5 인지) ⓑ **open/closed 규약 미기재** ⓒ MP 상집합 세대 미기재. **우리 값과 자릿수만 비슷하고 정의가 확인되지 않는다** |
| **`Norm. MSD`** | 0.015 ~ 1.547 (Å) | 없음 (우리는 벌크 MSD 만) | 🔴 **비교 대상 자체가 없다.** 우리가 계면 MD 를 시작하면 **§9-3(c) 의 수정판**으로 만든다 |
| **σ (S cm⁻¹)** | LiB₁₃C₂ 1.30e−3 · LiB₁₂PC 4.43e−4 (300 K, **c_vac 0.05 % 가정**) | comp1/modelc MLIP-MD σ — **절대값 인용 금지** | 🔴 **금지 — 양쪽 다 인용 불가 사유가 있다** |
| **D (cm² s⁻¹)** | D_vac 8.19e−5 / 2.69e−5 (300 K, **공공 1개의 확산계수**) | comp1 3.09e−6 / modelc 7.90e−6 @600 K (**tracer D**) | 🔴 **다른 양이다** (vacancy D vs tracer D · 1D vs 3D · 온도 다름) |
| **`E_G` 필터** | 훈련 0.8 eV / 스크린 **1.5 eV** (MP 값) | `sei_electronic.json` fixed-occ nscf: LiCl 6.2603 · Li₂O 4.986 · Li₂S 3.4379 · **Li₃P 0.7092** | 🟡 **절대값 비교 금지 (PBE·MP 세대 다름). 단 "Li₃P·Li₃N 이 1.5 eV 문턱 아래라 스크린에서 빠졌다" 는 사실은 우리 서열의 외부 방증** |
| **라벨 (stable/passivating/reactive)** | 3535 구조 | 없음 | ⭕ **정성 정보로는 쓸 수 있다** — *"Li₂S·LiCl·Li₃P·Li₂O·Li₃BO₃ 는 이 스크리너에서 Li 금속에 stable"*. **소환값·정성 표기 필수** |
| **W_ad · γ · ESW · 탄성 · gap** | **전부 없다** | 있음 | — **대조 불가** |

### 10-3. 우리 원장과의 접점 3건

1. ⭐ **`sei_products.json` 보강 — 산물의 "추가 반응성" 칸이 생긴다.** 우리 0 V 산물표는 *"어떤 상이 생기나"* 까지만 답한다. 이 논문은 그 상들이 **Li 금속과 더 반응하는가**에 대한 외부 AIMD/스크린 답을 준다: **Li₂S ✅stable(AIMD) · Li₃P ✅stable(AIMD) · LiCl ✅stable(예측) · Li₂O ✅stable(예측) · Li₃N ✅stable(AIMD) · Li₃BO₃ ✅stable(예측) · LiBO₂·Li₂B₄O₇ 🟡passivating(예측)**.
2. ⚠ **`Li₃P` 에 대한 두 원장의 긴장**: 우리는 `conductor-LEAK`(갭 0.709 eV) 라 부르고, 이 논문은 **Li 금속에 대해 stable** 이라 부른다. **모순이 아니다 — 다른 축이다**(화학 반응성 vs 전자 누설). 하지만 **같은 문장 안에 쓰면 독자가 헷갈린다** ⇒ 우리 서술에 축 이름을 반드시 붙인다.
3. ⭐ **cascade descriptor v0 (J-17 `[Zhao21HECS]`) 와의 접속**: 두 논문이 **같은 Sendek 22 특징 계열**을 쓰되 타깃이 다르다 — Zhao 는 **BVSE Ea**, Lomeli 는 **계면 반응성 라벨**. ⇒ **하나의 표현(representation)으로 두 타깃을 동시에 다룰 수 있다**는 실증이 두 편에서 나온다. 우리 descriptor 집합 v0 에 `AAV·PF·SBI·LBI·LLB·SLPW·SLPE` 를 넣을 근거가 하나 더 늘었다.

---

## 11. 기법 미니 용어집 (이 논문을 읽는 데 필요한 것만)

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **`E_hull`** (energy above hull) | 그 조성에서 가능한 최저에너지 상분해 대비 초과 에너지. 0 = 바닥상 | 후보 필터 (≤50 또는 ≤100 meV/atom — 본문이 갈린다) |
| **`ΔE_rxn`** (mutual / interfacial reaction energy) | 두 상을 섞었을 때의 에너지 변화. 보통 혼합분율 x 에 대해 최소를 취한다 | **가장 강한 단일 특징**. MP API 에서 가져옴. **규약 미기재** |
| **100 meV/atom 문턱** | *"4 k_BT at RT"* — 이 정도 구동력은 kinetic 하게 막힐 것이라는 업계 관행 | **논문이 공격하는 대상** |
| **`Norm. MSD`** | 이 논문 고유. 계면수직 MSD 를 계면교차 원자에 대해 평균하고 SE 두께로 나눈 것 (단위 Å) | **보고량**. §3a |
| **sublattice** | SSE 에서 **Li 를 뺀 모든 원소** | MSD 를 세는 대상 (Li 의 정상 확산을 배제) |
| **로지스틱 회귀 / L2 / LBFGS** | 선형 결정경계 + 릿지 벌점 + 준뉴턴 최적화 | 두 이진 분류기 |
| **Stratified 5-fold CV** | 라벨 비율을 유지한 채 5등분 교차검증 | 특징 선택의 기준 |
| **전수 특징탐색(combinatorial feature search)** | 가능한 모든 부분집합을 돌려 최고 점수를 고르는 것 | ✎ **1 744 435 조합**. 이 절차 때문에 CV 값이 **낙관 편향**된다 |
| **baseline vs random-guessing 오분류** | 전자 = 다수 class 만 찍기 / 후자 = class 비율대로 무작위 | `Fig. 2` 의 두 검은 점선 |
| **precision / recall** | TP/(TP+FP) / TP/(TP+FN) | **둘 다 76.9 %**. 다만 *positive* 가 무엇인지 정의를 안 쓴다 (✎ TP=10·FP=3·FN=3 로 역산됨) |
| **t-SNE** | 고차원 점들을 국소 이웃관계를 보존해 2D 로 내리는 비선형 임베딩 | `Fig. 3c,d`. ⚠ **거리·군집 크기에 물리적 의미가 없다** |
| **Sendek 서술자** | 단위셀 구조만으로 뽑는 20개 스칼라 (Li–Li 결합수, 음이온 골격 배위수, 결합 이온성, 직선경로 폭/전기음성도 등) | `Table S1`. 원전은 *EES* 2017 의 **이온전도도** 모형 |
| **Nernst–Einstein (여기서는)** | σ = c q² D /(k_B T). **c 를 알아야 한다** | 붕소화물 σ. **c = 0.05 % 를 가정**했다 |
| **1D Fick 1법칙 + hopping rate** | 공공의 도약 빈도에서 D 를 얻는 방법 | MSD 대신 이 경로를 씀. **고른 이유의 서술은 틀렸다**(§3h) |

---

## 12. 우리가 실제로 가져갈 것 (우선순위)

| # | 가져갈 것 | 어디에 |
|---|---|---|
| **1** | ⭐⭐⭐ **"계면수직 MSD + 평면교차 필터 + sublattice 만 세기"** 라는 **반응영역 분리 기법** | 우리 계면 MD 보고량 카드의 **초안 v0**. 단 **`L_SSE` 정규화는 버리고 `L_reacted(t)` [Å] 로**(§9-3c) |
| **2** | ⭐⭐ **xlsx 3535행 라벨표** — 우리 산물·코팅·도펀트 후보의 **Li 금속 반응성 외부 참조표** | `sei_products.json` 주석 · 코팅 후보 선별 |
| **3** | ⭐⭐ **"밀도 + sublattice 이온성" 서술자 방향** | cascade descriptor v0 (J-17 과 병합) |
| **4** | ⭐ **`Li₂S`·`Li₃P`·`LiCl`·`Li₂O`·`Li₃N` 이 Li 금속에 stable** 이라는 외부 AIMD/스크린 근거 | §E — [Wang22Res] 와 짝을 이루는 문장 |
| **5** | ⭐ **`Li₃BO₃` stable / `LiBO₂`·`Li₂B₄O₇` passivating** — B₂O₃ 도핑 서사의 산물측 외부 참조 | §F 도핑 축 |
| **6** | ⚠ **반면교사: "CV 최솟값을 성능으로 보고하지 않기"** — 170만 조합 + 50점 | 우리 ML/스크리너 작업 전반. **[Zhao21HECS] 의 R²=0.820 사례와 같은 계열** |
| **7** | ⚠ **반면교사: 검증셋을 다른 모델의 예측으로 고르지 않기** | 우리 group-out 규율 강화 근거 |
| **8** | 🔴 **경고: 액체 Li 를 포함한 셀의 DOS 는 부동태 판정에 못 쓴다** | 우리가 음극 계면 DOS 를 계획할 때 **공간투영 필수** |

---

## 13. 비판 (critical — 아첨하지 않는다)

**① 🔴 `Fig. 1` 의 y축이 1.0 에서 잘렸고 그 사실이 어디에도 없다.**
상위 3계(`LiBiF₄`·`Li₂GePbS₄`·`LiGaCl₃`)의 막대가 전부 정확히 1.0 에 닿아 있는데, **`Fig. S2` 를 축 보정해 읽으면 진값이 1.058 / 1.118 / 1.547** 이다. `LiGaCl₃` 는 **55 % 가 잘려 나갔다.** 결과적으로 `Fig. 1` 은 reactive 군의 산포를 **압축해 보여 준다** — 하필 그 그림이 **세 라벨의 분리를 보여 주는 유일한 그림**이다. (✎ 이 발견은 두 그림의 교차판독에서만 나온다.)

**② 🔴🔴 `L_SSE` 로 나누는 정규화가 부동태화 지표로서 방향이 반대다.**
반응 전선이 **고정 깊이에서 멈추는 것**이 부동태화인데, 그 경우 분자는 상수이고 분모(`L_SSE`)만 커진다 ⇒ **SE 를 두껍게 하면 같은 물질이 reactive → passivating 으로 이동한다.** 저자도 §7.2 에서 *"큰 셀에서는 passivating 일 수 있는데 우리 셀이 작아서 reactive 로 찍는다"* 고 인정하지만, **그 원인이 자기 정규화에 있다는 것은 짚지 않는다.** ⇒ **경계(0.31)는 물질 성질이 아니라 셀 설계 산물이다.**

**③ 🔴 `NaLiSe` 의 라벨이 표와 그림에서 다르다.**
`Table 1`·본문·Methods 는 **passivating**(훈련셋 19/10/21), `Fig. 1` 막대와 `Fig. S2` 점은 **navy = reactive**(19/9/22). `Norm. MSD` 0.427 은 passivating 띠(≤0.303) 밖이고 reactive 군 한가운데다. ⇒ **어느 라벨로 학습했는지 알 수 없고, 50점 데이터에서 한 점은 CV 오분류의 2 %p 다.**

**④ 🔴🔴 CV 6–8 % 는 성능이 아니라 선택된 최솟값이다.**
22개 특징에서 N=1..10 전수조합 = ✎ **1 744 435 개 모델**을 **50점** 위에서 5-fold CV 로 채점하고 **최솟값을 보고**한다. 50점에서 CV 오분류의 **양자는 1/50 = 0.02** 이므로 0.06–0.08 은 거의 결정적으로 도달한다. 증거 둘:
- `Fig. 2b` 에서 RM 의 CV 가 N=3..6 에서 **평평하게 0.08** 이다가 N=7 에서 0.06 으로 내려가고 N=8·9 에서 **다시 0.08** 로 오른다 — **훈련점 1개의 오르내림**이다.
- `Table S2` 의 RM 7-feature 중 `SPF` 계수가 **0.042**(ΔE_rxn 의 1/51)다 — **아무 기여도 없는 특징이 "최적 7개"에 들어 있다.**
⇒ **정직한 숫자는 홀드아웃 35.3 % 하나뿐이다.**

**⑤ 🔴 검증셋이 무작위가 아니고, 비교 기준선을 같은 검증셋에서 재지 않았다.**
*"we chose materials predicted to be good Li ion conductors"* — **다른 모델(Sendek σ)의 예측으로 고른 17종**이고 10/17 이 별표다. 그리고 결정적으로, **`ΔE_rxn` 단독 기준선을 이 홀드아웃 17종에서 재 보지 않았다.** 논문이 자랑하는 *"3–4배 개선"* 은 **CV 대 CV** 비교이고, **홀드아웃에서의 개선은 한 번도 보이지 않는다.** (참고: 17종의 `ΔE_rxn` 은 0.000 ~ −0.489 이고 100 meV/atom 문턱으로는 16/17 이 unstable 이 된다.)

**⑥ 🟡 오류를 사후에 재채점해 17.6 % 를 만든다.**
6건 오류 중 3건(stable → passivating 오분류)을 *"그래도 쓸 만한 예측"* 이라며 노란색으로 빼고 *"fully negative outcomes account for only a **17.6 %**"* 라 적는다. **결과를 본 뒤에 채점표를 고친 것**이다 — 우리 규율의 *"검증 게이트를 결과 보기 전에 정한다"* 에 정면으로 걸린다.

**⑦ 🔴 스칼라 보고량의 상태 선택 규칙이 없다 (§9-1).** 특히 **`Li₆FeCl₈`**: 논문 스스로 *"Fe states at the Fermi energy"* 를 논하는 **열린 껍질·산화환원 활성** 계인데, **스핀 상태·자화·`NUPDOWN` 선언이 0**이다. `LiMnPO₄`·`Li₃Fe₂(PO₄)₃`·`Li₃VO₄`·`Li₇VGeO₈`·`Li₆WN₄`·`LiLaTi₂O₆`·`Li₂TiO₃` 등도 같다. **"+U 를 켰다"는 상태 선언이 아니다.**

**⑧ 🔴 본문의 히스토그램 서술이 원자료와 어긋난다.**
*"passivating 피크가 stable 보다 약 **300 meV/atom** 높고, reactive 는 **750 meV/atom** 근처"* → ✎ xlsx 직접 계산: 최빈 구간이 stable **0.025** / passivating **0.425** / reactive **0.625** eV/atom ⇒ 차이는 **400**, reactive 피크는 **625**. **100–125 meV/atom 어긋난다.**

**⑨ 🟡 초록의 "over 780" 이 조건을 안 지킨다.** *"over 780 passivating solid electrolytes that are **predicted to be thermodynamically unfavored**"* — 788 중 **`|ΔE_rxn| ≥ 100 meV/atom` 인 것은 757 개**다. 3 % 과장.

**⑩ 🔴 같은 조성이 다형에 따라 반대 라벨을 받는데 집계 규칙이 없다.** ✎ **87개 조성.** `Li₃PO₄`(stable / passivating, **둘 다 orthorhombic**), `CsLiCl₂`(stable / reactive), `LiNbO₃`(stable 1 / passivating 8), `Li₃ErBr₆`(passivating / reactive). 사용자가 *"LiNbO₃ 는 어느 쪽이냐"* 고 물으면 **이 데이터는 답을 주지 못한다.**

**⑪ 🟡 그림 내부 색 규약이 갈린다.** `Fig. 3` 에서 (a),(b) 는 **teal = Stable / gold = Passivating**, (c),(d) 는 **gold = Stable / teal = Passivating**. `Fig. 1` 은 cyan = Stable / gold = Passivating. **한 그림 안에서 뒤집힌다.**

**⑫ 🟡 약어 정의가 세 번 갈린다.** SM/RM 이 Results 와 Methods/Conclusion 에서 **의미가 서로 바뀌고**, `Table S2` 는 RM 을 *"Passivating Model"* 이라 부른다(§7.3).

**⑬ 🟡 서지·표기 오류 묶음.**
- ref 40 = PBE 를 **exchange-correlation *hole* 논문**(Perdew–Burke–**Wang**, PRB 54, 16533)으로 인용 — PBE 범함수 원전이 아니다.
- **ref 8 과 ref 35 가 같은 논문**(Lv et al., *Cell Rep. Phys. Sci.* 2022, 3, 100706) — 중복 참고문헌.
- 본문 *"|ΔE_rxn| > 100 **eV**/atom"* (meV 오타).
- 본문 *"**Li₆WN₂**"* — `Table 1`·`Fig. 1` 은 **Li₆WN₄**.
- `Table 2` 각주 *"σ_Li > 10⁻⁴ **mS/cm**"* — S/cm 여야 한다 (1000배).
- 결론 *"LiB₁₂**CP**"* vs 본문 *"LiB₁₂**PC**"*.
- `Fig. S6` 캡션 *"Figure **5d** in the main text"* — **Figure 5 는 존재하지 않는다**(3d 여야 한다).
- `Fig. S2` 캡션 *"Relationship of **ΔE_formation**"* — 축과 본문은 **ΔE_rxn**.
- 본문 붕소화물 *"ΔE_rxn = 152 meV/atom"* 은 `Table 2` 에서 **LiB₁₂PC** 값이고, 문장은 **LiB₁₃C₂**(−162) 를 주어로 쓴다.
- 후보 필터가 본문 안에서 **50 / 100 / 100 meV/atom 세 번 다르게** 적힌다.

**⑭ 🔴 재현 불가 요소가 많다.** 물질별 **초기 간극(1.8–3.0 Å 중 어느 값)** · **400 K 로 내린 물질 목록** · **+U 값** · **`Norm. MSD` 원자료 67개** · **궤적** · **코드** · **시드** 전부 미공개. 공개 자산은 **xlsx 라벨표 하나**다.

**⑮ 🟡 좋은 점도 있다 (균형).**
- **정직한 자기한계를 여러 번 적는다** — Li₂PNO₂ 의 실험 불일치, 셀 크기 한계, 종단 의존성, AIMD 도 예측일 뿐이라는 것.
- **질화물 3건(Mg₃N₂·BN·C₃N₄)의 실험 앵커**는 논문의 논지를 실제로 받친다.
- **`Fig. S2` 를 SI 에 넣은 것** 덕분에 `Fig. 1` 의 클리핑을 외부에서 잡을 수 있었다 — **원자료를 더 보여 준 것이 자기 결함을 드러냈지만, 그것이 좋은 과학이다.**
- **xlsx 를 3535행 전수로 공개**한 것은 이 분야 평균보다 낫다.

---

## 14. 🔴 우리에게 불리한 결론 (따로 절로 — 1저자 지정 ⑥)

**① 우리 모체 계열이 이 논문의 AIMD 에서 "반응성" 이고, 그것도 상위권이다.**
`Li₃PS₄` **0.819 (45/50위)** · `Li₇P₃S₁₁` **0.911 (47/50)** · `Li₁₀GeP₂S₁₂` **0.552 (37/50)**. 그리고 `Li₆PS₅I` 는 스크린에서 **reactive**, `Li₅P(S₂Cl)₂` 도 **reactive**, `Li₇PS₆` 도 **reactive**. ⇒ **황화물 계열은 이 프레임에서 "부동태화" 조차 못 받는다.** 화학군 통계도 같은 방향이다 — **황화물(S 포함·O 없음) 169종 중 stable 은 5종(3.0 %)** 로 기저율(15.1 %)의 **1/5** 다.
⛔ **단 `Li₆PS₅Cl` 자체는 목록에 없으므로 "이 논문이 LPSCl 을 reactive 라 했다" 고 쓰면 안 된다.**

**② 그들의 구조 서술자 결론이 우리 설계 방향과 정확히 반대를 가리킨다.**
안정성은 **작은 AAV(밀함) + 높은 sublattice bond ionicity + 좁은 직선경로(SLPW)** 와 상관한다. 아르지로다이트는 **열린 골격 + 넓은 확산 채널 + 황화물(산화물보다 낮은 이온성)** 이고, 그 세 가지가 **바로 우리가 σ 를 위해 고르는 것**이다. 논문이 그 트레이드오프를 직접 적는다: *"a high packing fraction could lead to smaller and less accessible Li diffusion pathways in the SSE, thus **inhibiting Li ion conductivity**; **optimizing for both stability and conductivity will be key**."*
⇒ **"Cl-rich 가 빠르다" 는 우리 축 A 의 서사는, 이 논문의 안정성 축에서 도움이 되지 않는다.**

**③ Cl 을 늘리는 방향에 대한 직접 근거는 없지만, 간접 신호는 중립~약간 나쁘다.**
✎ 염화물 함유 120종: stable **11.7 %** (기저 15.1 %) · reactive **78.3 %** (기저 62.6 %). 질화물은 stable **49.7 %** 로 **3.3배 풍부**. ⇒ 이 스크리너의 화학 선호는 **질화물 ≫ 붕산염/산화물 > 염화물 ≳ 황화물** 이다. ⛔ **이 비율은 MP 후보 구성 편향을 그대로 물려받으므로 절대 인용 금지 — 경향만.**

**④ "부동태화를 못 재고 있다" 는 우리 공백이 이 논문으로 메워지지 않는다.**
이 논문도 **두께·성장속도·자기제한·전자절연 어느 것도 재지 못한다**(§9-3). ⇒ *"그건 문헌이 이미 했다"* 로 미룰 수 없고, **§H 의 공백 항목으로 남는다.** 오히려 **이 편이 그 공백의 어려움을 증명한다** — 정직하게 시도했고(pDOS), 액체 Li 때문에 실패했다.

**⑤ ⚠ 유리한 쪽도 하나 있다 (균형을 위해).**
우리 0 V 분해산물 **Li₂S · Li₃P · LiCl** 이 이 논문에서 **전부 "Li 금속에 stable"** 이다(앞 둘은 40 ps AIMD 직접 확인). [Wang22Res] 와 합치면 음극 계면 서사가 이렇게 정리된다 —
> **"아르지로다이트의 분해산물은 Li 금속과 *더 반응하지는 않는다*(Lomeli24). 문제는 그 산물이 Li 금속에 *붙지 않고*(W_adh 0.045–0.675, 두 문턱 다 미달) Li⁺ 를 *통과시키지 않는다*(400 K D\* 1.8e−9 ~ 3.0e−6)는 것이다(Wang22Res)."**
이 두 문장은 **서로 다른 두 그룹의 독립 계산**으로 받쳐진다. 원고에서 쓸 수 있는 조합이다.

---

## 15. 인용 규율 (이 편을 쓸 때 지킬 것)

1. ⛔ **"이 논문이 Li₆PS₅Cl 을 …라고 했다" 는 어떤 형태로도 금지.** 목록에 없다. 대리값은 `Li₆PS₅I`(reactive, **예측**)·`Li₅P(S₂Cl)₂`(reactive, **예측**)·`Li₃PS₄`/`Li₇P₃S₁₁`(reactive, **AIMD**)이고 **셋의 신뢰도가 다르다**(예측 vs AIMD).
2. ⛔ **`ΔE_rxn` 값을 우리 `interface_reactivity`/ΔH_D 옆에 놓지 않는다** — 혼합분율·open/closed 규약이 미기재다.
3. ⛔ **`Norm. MSD` 를 우리 MSD 와 같은 문단에 쓰지 않는다** — 1D·계면교차·SE두께 정규화이고 단위가 Å 다.
4. ⛔ **σ·D 절대값 인용 금지** (그쪽은 공공농도 가정, 우리 쪽은 1저자 정책).
5. ✅ **쓸 수 있는 것**: ⓐ 3분류 라벨을 **정성 참조**로 ⓑ *"ΔE_rxn 단독 문턱이 불완전하다"* 는 **주장과 그 질화물 3건 근거** ⓒ **반응영역 분리 기법** ⓓ **우리 산물 5종이 Li 금속에 stable** 이라는 외부 근거.
6. ⚠ **성능을 인용할 때는 반드시 홀드아웃 35.3 % 를 같이 쓴다.** CV 6–8 % 만 인용하면 우리가 그 편향을 승인하는 셈이 된다.
7. ⚠ **그림에서만 읽은 값은 전부 `figure-read ≈`** 로 표시했다 — 특히 §3b 의 `Norm. MSD` 50개는 **전부 픽셀 복원값**이다(논문은 숫자를 공개하지 않는다).

---

## 16. 실독 기록 (투명성)

**크로핑 결과**: `litdb/figures/lomeli2024_predicting_reactivity_passivation_ssb_interfaces/` — PNG **14장** (본문 `fig_1`·`fig_2`·`fig_3`·`fig_4`·`tab_1`·`tab_2` + SI `fig_S1`–`fig_S7`).

| 봤다 | 안 봤다 | 이유 |
|---|---|---|
| **`fig_1`** (+ 좌/우 2배 확대 재렌더) — 보고량의 유일한 원자료 | `fig_4` | **`tab_2.png` 크롭 안에 `Fig. 4` 전체가 같이 들어 있어 거기서 읽었다** (중복 회피) |
| **`fig_2`** — 성능 주장의 근거 | `fig_S1` | 경계 2계 스냅샷. 본문 서술로 충분하고 판정에 새 정보 없음 |
| **`fig_3`** — 결정경계 + t-SNE (논문 헤드라인) | `fig_S5` | 훈련셋 대표성 t-SNE. 판정에 영향 없음 |
| **`fig_S2`** — ⭐ 여기서 `Fig. 1` 클리핑을 잡았다 | `fig_S6` | **xlsx 원자료로 직접 계산하는 편이 정확**해서 그렇게 했다(§3f·§13-⑧) |
| **`fig_S3`** — 부동태 pDOS (임무 ③ 핵심) | `fig_S7` | matminer vs Sendek 특징 비교. 결론(*"차이 없음"*)이 본문에 명시 |
| **`fig_S4`** — reactive pDOS (21패널 전부 E_F 에 상태 있음 확인) | `tab_1` | **표는 PDF 텍스트가 정확** — 50행 전수 전사했다 |
| **`tab_2`** — 이미지 표라 텍스트 추출 불가 ⇒ 실독 전사 (+ `Fig. 4` 동봉) | | |

**⇒ 그림 7장 실독 + 확대 재렌더 2회 + 표 1장 텍스트 전사 + xlsx 3535행 직접 파싱.**

**본문 서술과 어긋난 것 (실독으로 잡은 것만)**: §13-① (Fig. 1 클리핑) · §13-③ (NaLiSe 색) · §13-⑧ (히스토그램 서술 vs xlsx) · §13-⑪ (Fig. 3 색 규약) · §7.2 (pDOS 가 부동태 판정에 못 쓰인다는 것의 직접 확인).

**크로핑 도구 결함 1건**: `fig_S2.png` 와 `fig_S3.png` 가 **바이트 동일**(md5 `599b637d…`)이다 — SI 4쪽에 `Fig. S2` 와 `Fig. S3` 가 같이 있는데 추출기가 같은 bbox 를 두 번 썼다. ⇒ **SI 4쪽을 통째로 재렌더해서 둘 다 읽었다.** (`--clean` 금지 지시라 파일은 그대로 뒀다. 다음에 재추출할 때 고칠 자리다.)

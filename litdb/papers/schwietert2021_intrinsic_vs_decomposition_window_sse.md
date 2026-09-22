<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     같은 축(ESW)의 직전 digest = papers/schwietert2020_redox_activity_vs_electrochemical_stability.md (이 논문의 ref 7).
     2026-09-22 신규. 1저자 지정 읽기축 = **`[Zhu15]` 3.4× 감사를 닫는 것**.
     크로핑 29장(그림 14 + 표 15) 중 그림 8장 실독(§9 에 본 것/안 본 것 명시).
     ⛔ 이 digest 의 수치는 전부 **소환값**이다. 우리 db 절대값과 같은 셀에 놓지 않는다. -->

# First-Principles Prediction of the Electrochemical Stability and Reaction Mechanisms of Solid-State Electrolytes — Schwietert, Vasileiadis & Wagemaker (*JACS Au* **1**, 1488–1496 (2021))

> slug `schwietert2021_intrinsic_vs_decomposition_window_sse` · DOI `10.1021/jacsau.1c00228` · type `DFT(VASP-PBE) 전용 + AIMD(σ) · 자체 실험 0건` · PDF `litdb/inbox/7. FirstPrinciples_prediction_ESW_reaction_mechanisms_SSE_MAIN.pdf` (본문 9 pp) + `7. Sup) FirstPrinciples_prediction_ESW_SI.pdf` (SI 11 pp · `Table S1`–`S13` · `Figure S1`–`S10` + 번호가 틀린 `Figure 11`) · digested `2026-09-22` · status ✅ · 태그 **[외부·🔴🔴 `[Zhu15]` 3.4× 감사의 열쇠·아지로다이트 포함]**

> elements: Li, P, S, Cl, Br, Ge, B, H, Y, O, N, La, Zr, Ti, Al
> methods: DFT, AIMD, DOS, ESW

> **저자**: **Tammo K. Schwietert**, **Alexandros Vasileiadis**, **Marnix Wagemaker\*** (m.wagemaker@tudelft.nl, ORCID 0000-0003-3851-1044)
> 전원 **TU Delft**, Storage of Electrochemical Energy, Department of Radiation Science and Technology, Faculty of Applied Sciences, Mekelweg 15, 2929JB Delft, NL
> 접수 **2021-05-22** · 게재 **2021-08-16** · ***JACS Au* 1(9), 1488–1496** · © 2021 The Authors, ACS (**오픈액세스**)
> 지원: NWO **VICI 16122** · eScience Centre + NWO 공동 CSER/eScience Energy **680.91.087** (= `[Schw20]` 과 동일 과제)
> **데이터 공개**: ⛔ **없다.** 리포지터리·입력파일·구조파일 0개. Data availability 절 자체가 없다.

> ✅ **서지 확인 완료 (PDF 표지·각주 직독)** — `[Dutra25Rev]` 의 **ref 218**("Schwietert, *JACS Au* **1**, 1488 (2021)")이 **이 편이 맞다**. 우리 `comparison_vs_ours.md` 1021행이 그 ref 에 달아 둔 `Fig. 5c` 는 **이 논문의 그림이 아니다** — 이 논문 본문 그림은 `Fig. 1`–`Fig. 3` **3장뿐**이다. 내용(*"상분리 이중우물 vs 고용체 단조하강"*)으로 보아 **리뷰 자신의 `Fig. 5c` 가 이 논문 `Fig. 3b,c` 를 옮긴 것**으로 보인다 (⚠ 리뷰 원문 재확인 전에는 이 귀속을 확정하지 말 것).

> 🎤 **관련 발표: 해당 없음** — `litdb/talks/lee2026_skku_mlip_materials_design.md` §99-10 인입 대기열(6건)에 이 논문 없음. grep 실측 0건.

> 🔗 **형제 digest (중복 서술 대신 링크)**: 이 논문의 **ref 7** = `papers/schwietert2020_redox_activity_vs_electrochemical_stability.md` (같은 1저자·교신, *Nat. Mater.* 19, 428). 기전 서사(간접 경로 · `Li₄PS₅Cl`/`Li₁₁PS₅Cl` 중간상 · XRD·NMR·AIMD 증거)는 **그쪽이 정본**이고 여기서는 반복하지 않는다. 이 편의 새로움은 **① 12종으로 확장 ② "decomposition window vs intrinsic window" 라는 이름과 조작적 정의 ③ 상분리/고용체 분기 ④ 준안정상의 부피·밴드갭·σ 표**다.

---

## 0. 이 digest 를 읽는 법 — 1저자 지정 읽기축

이 편을 여는 이유는 하나다:

> 🔴🔴 **우리 안정창 `1.242–2.256 = 1.014 V` 가 `[Zhu15]` 의 `0.30 V` 보다 3.4 배 넓다. 같은 방법 계열인데. 왜인가?**

답을 먼저 적는다 (근거는 **§7**, 이 digest 의 중심 절이다):

| 질문 | 답 |
|---|---|
| 이 논문이 `[Zhu15]` 계열인가 | ❌ **아니다 — `[Schw20]` 의 직계 후속이다.** 하지만 **`[Zhu15]` 의 창을 자기 손으로 다시 계산해 Table 2 에 싣는다** (캡션: *"Values in Agreement with the Calculations in Literature⁸"*, ref 8 = `[Zhu15]`) ⇒ **0.30 V 가 재현됐다. 전사 오류가 아니다.** |
| 창 정의가 우리와 같은 양인가 | ✅ **같은 양이다.** *"Li **grand potential** phase diagram"* · *"**the decomposition potential closest to the stable solid electrolyte phase** defines the reduction and oxidation redox potentials"* · 조성 = **`Li₆PS₅Cl`**(별도 행, `Li₃PS₄` 도 `Li₇P₃S₁₁` 도 아니다) · 참조에너지 = **Materials Project** |
| 그럼 3.4× 는 어디서 오나 | 🔴 **대부분 우리 쪽 라벨 오류다.** 저들 정의(= Li 교환이 0 인 구간의 양 끝)로 **우리 자신의 프로파일을 다시 읽으면 1.717–2.256 V = 0.539 V** 다. 우리가 "환원 한계" 라 불러 온 **1.242 V 는 *두 번째* 환원 평탄**(P → `LiP₇`)이고, 진짜 환원 가장자리는 우리가 "OCV" 라 불러 온 **1.717 V** 다 |
| 남는 진짜 격차는 | **산화 쪽 한 변, +0.246 V** (우리 2.256 ↔ 저들 2.01). 환원 쪽은 **−0.003 V = 사실상 동일**(우리 1.717 ↔ 저들 1.72) |
| 층①/층② 로 설명되나 | ❌ **아니다.** 이 논문이 이름 붙인 **decomposition window = 층①**, **intrinsic window = 층②** 인데, 우리 1.014 V 는 층② 가 **아니라 층① 을 잘못 읽은 값**이다. ⚠ 하필 저들 LPSC **층② 폭이 1.08 V** 라 우리 1.014 V 와 0.07 V 차다 — **이 우연을 "우리 hull 이 간접 경로를 이미 머금었다" 로 읽으면 안 된다** |
| 우리에게 불리한가 | ⚠ **불리하다.** ① 우리 `reduction_V` 라벨이 틀렸고 그 라벨이 **cascade 전수의 `window_V` 에 들어가 있다** ② 우리 산화 onset 2.256 V 는 같은 방법 계열의 **두 독립 계산(2015·2021)이 모두 2.01** 인 자리에서 혼자 0.25 V 높다 — 즉 우리 "worst-case 하한" 이 **가장 덜 보수적**이다 |

---

## 1. 한 줄 요약

**고체전해질의 전기화학 창은 두 개다.** 하나는 분해산물의 안정성이 정하는 **decomposition window**(= `[Zhu15]` 계열, 우리 2.256 V 가 여기), 다른 하나는 **전해질 자신이 골격을 유지한 채 Li 를 넣고 빼는 전압**이 정하는 **intrinsic window** 다. 12종 SE 를 같은 틀로 계산해 보니 **대부분(10/12) intrinsic 이 더 넓고**, 실측과 더 잘 맞는다. 다만 **LLTO·LATP 에서는 intrinsic 이 더 *좁다*** — 삽입반응이 분해보다 먼저 일어나는 계다. 그리고 hull 모양이 **V자면 상분리**, **볼록하면 고용체**로 갈라지며, 상분리 계에서만 "중간상 → 분해산물" 의 간접 경로가 작동한다.

---

## 2. 메타 / 동기 / 질문

**문제 상황 (서론 축자).** CV 실험은 창을 **과대평가**하고(refs 7, 8), 분해산물 형성에너지 예측은 **과소평가**한다(refs 7–9). CV 가 틀리는 이유는 *"small electrolyte−electrode contact area and the short time scale ... compared to low-current-density solid-state battery cycling"*(ref 10). 형성에너지 예측이 틀리는 이유는 *"the inability of capturing the reaction mechanism and the associated reaction energy barrier toward the decomposition products, which will kinetically hinder the decomposition"*.

**직전 결과(ref 7 = `[Schw20]`)를 저자 스스로 요약한 문장.** 산화·환원은 **탈리튬화·리튬화**와 짝지어 **준안정 SE 조성을 경유하는 간접 경로**를 제공하고, 그때 SE 는 **활물질(Li source/sink)처럼 행동**한다. **단 조건이 붙는다** — *"This is **only possible if the solid electrolyte is in contact with the electron-conducting network** of the electrode"* (음극/양극 근처, 또는 도전재 근처). "근처" 의 범위는 **SE 와 그 분해산물의 전자전도도**가 정한다.

**이 논문의 질문 3개.**
1. `[Schw20]` 의 방식을 **가장 많이 쓰이는 SE 전부**로 확장하면 어떤 그림이 나오나?
2. intrinsic 이 **항상** 더 넓은가? (답: **아니다** — LLTO·LATP)
3. 창 밖에서 일어나는 일이 **상분리인지 고용체인지**를 무엇이 가르나? (답: **hull 의 모양**)

**⚠ 이 논문의 위상 (중요).** `[Schw20]` 이 *"실험 + DFT + AIMD + XRD + NMR"* 의 종합편이라면, 이 편은 **순수 계산 확장편**이다. **자체 실험 0건**, 대조는 전부 **문헌 소환값**이다. 그래서 *"실험과 훌륭히 맞는다"* 는 주장의 무게가 `[Schw20]` 과 다르다 (§10-4).

---

## 3. 핵심 수치 총정리 ★

### 3a. `Table 2` — 두 창 전수 (이 논문의 중심 표)

> 원표 머리글은 **"decomposition ox/red (V)"·"intrinsic ox/red (V)"** 인데, **값은 `환원−산화`(낮은 값이 환원)** 로 적혀 있다. `Fig. 1` 실독과 본문 모든 서술이 그렇다 ⇒ **머리글 순서가 값과 어긋난다**(§10-6). 아래 표는 **환원 / 산화** 로 풀어 적었다. 폭(width)은 **우리 산수**.

| 계 | 조성 | **decomposition** 환원 / 산화 (V) | 폭 | **intrinsic** 환원 / 산화 (V) | 폭 | 창 변화 |
|---|---|---|---|---|---|---|
| **LPS** | `Li₃PS₄` | **1.72 / 2.30** | 0.58 | **1.24 / 2.47** | 1.23 | +0.65 |
| **LPSB** | `Li₆PS₅Br` | **1.72 / 2.01** | 0.29 | **1.09 / 2.23** | 1.14 | +0.85 |
| **🔴 LPSC** | **`Li₆PS₅Cl`** | **1.72 / 2.01** | **0.29** | **1.11 / 2.19** | **1.08** | **+0.79** |
| **LGPS** | `Li₁₀GeP₂S₁₂` | **1.63 / 2.14** | 0.51 | **1.19 / 2.38** | 1.19 | +0.68 |
| **LBH** | `LiBH₄` | 0.54 / 2.10 | 1.56 | **0.00 / 3.43** | 3.43 | +1.87 |
| **LYB** | `Li₃YBr₆` | 0.67 / 3.06 | 2.39 | **0.00 / 3.43** | 3.43 | +1.04 |
| **LOC** | `Li₃OCl` | 0.00 / 2.68 | 2.68 | 0.00 / 3.17 | 3.17 | +0.49 |
| **LIPON** | `Li₂PO₂N` | 0.68 / 2.64 | 1.96 | **0.00 / 4.12** | 4.12 | +2.16 |
| **LLZO** | `Li₇La₃Zr₂O₁₂` | 0.05 / 2.68 | 2.63 | **0.00 / 3.61** | 3.61 | +0.98 |
| **⚠ LLTO** | `Li₀.₃₃La₀.₅₆TiO₃` | 1.71 / 3.36 | 1.65 | **2.10 / 3.68** | **1.58** | **−0.07** |
| **⚠ LATP** | `Li₁.₅Al₀.₅Ti₁.₅(PO₄)₃` | 2.17 / 3.86 | 1.69 | **2.74 / 3.77** | **1.03** | **−0.66** |
| **LAGP** | `Li₁.₅Al₀.₅Ge₁.₅(PO₄)₃` | 2.71 / 3.98 | 1.27 | **2.31 / 4.30** | 1.99 | +0.72 |

🔑 **표에서 바로 읽히는 것 3개.**
1. **황화물 4종의 decomposition 환원한계가 전부 `1.72` 또는 `1.63`** 이다. `Li₃PS₄`·`Li₆PS₅Br`·`Li₆PS₅Cl` 셋이 **글자까지 같은 1.72** — 우연이 아니다. 세 계의 Li-보존 평형이 전부 **`Li₃PS₄` 를 포함**하고, 환원 가장자리를 정하는 것이 그 `Li₃PS₄` 이기 때문이다 (§7-2 의 핵심 논거).
2. **`Li₆PS₅Cl` 과 `Li₆PS₅Br` 의 decomposition 창이 완전히 같다**(1.72–2.01) — 즉 이 방법에서 **할로겐은 창에 안 들어온다**. 우리 comp1/modelc onset 이 둘 다 2.256 V 로 같은 것(= S-limited)과 **같은 현상**이다.
3. **intrinsic 이 좁아지는 계가 둘 있다** (LLTO·LATP) ⇒ *"간접 경로가 항상 창을 넓힌다"* 는 **일반명제가 아니다**.

### 3b. `Table 1` — 산화환원 원소와 이론용량

| 계 | 산화 시 redox 원소 | 산화 용량 (mAh/g) | 환원 시 redox 원소 | 환원 용량 (mAh/g) | **대응 Li 수 (우리 산수)** |
|---|---|---|---|---|---|
| LPS | S²⁻ | ⚠ **96.23** | P⁵⁺ | 1190.78 | 산화 ⚠ **0.65** / 환원 **8.00** |
| LPSB | S²⁻/Br⁻ | 514.01 | P⁵⁺ | 685.35 | **6.00 / 8.00** |
| **LPSC** | **S²⁻/Cl⁻** | **599.14** | **P⁵⁺** | **798.85** | **6.00 / 8.00** |
| LGPS | S²⁻ | 455.20 | P⁵⁺/Ge⁴⁺ | 1081.11 | **10.00 / 23.75** |
| LBH | ⚠ B⁵⁻ | 1230.55 | ⚠ H⁺ | 4922.22 | 1.00 / 4.00 |
| LYB | Br⁻ | 136.48 | Y³⁺ | 136.48 | 3.00 / 3.00 |
| LOC | O²⁻/Cl⁻ | 1112.40 | — (Li 만 환원 가능) | — | 3.00 / — |
| LIPON | N³⁻/O²⁻ | 589.95 | P⁵⁺ | 2359.80 | 2.00 / 8.00 |
| LLZO | O²⁻ | 223.41 | Zr⁴⁺/La³⁺ | 255.33 | 7.00 / 8.00 |
| LLTO | O²⁻ | 50.27 | Ti⁴⁺/La³⁺ | 559.03 | 0.33 / 3.67 |
| LATP | O²⁻ | 105.62 | P⁵⁺/Al³⁺/Ti⁴⁺ | 2147.69 | 1.50 / 30.5 |
| LAGP | O²⁻ | 96.23 | Ge⁴⁺/P⁵⁺/Al³⁺ | 1812.34 | 1.50 / 28.25 |

> **우리 산수**: `n_Li = C[mAh/g] × M[g/mol] / 26801.5`. 12행 중 **11행이 정수·반정수로 정확히 떨어진다** ⇒ 표는 **완전 분해**(산화 = Li 를 전부 뺀다 / 환원 = 최종 산물까지 넣는다)를 기준으로 계산됐다.
> 🔑 **LPSC 환원 용량 798.85 = 정확히 8.00 Li** 이고, 그 8 Li 는 **우리 `esw_lis4excluded.json` 의 0.0 V 단계 `Li₆PS₅Cl + 8 Li → Li₃P + 5 Li₂S + LiCl` 과 같은 수**다 ⇒ **저들 상집합과 우리 상집합이 최종 환원산물에서 일치한다** (§7-4).
> ⚠ **LPS 산화 용량 96.23 은 틀린 값으로 보인다** — `LAGP` 행과 **글자까지 같고**, `Li₃PS₄` 에서 3 Li 를 다 빼면 **≈446.6 mAh/g** 이어야 한다(우리 산수). **복사 오류 후보. 인용 금지.**
> ⚠ **`LiBH₄` 의 `B⁵⁻`/`H⁺`** 는 통상 형식전하(`BH₄⁻` 에서 H 가 더 전기음성 ⇒ `B³⁺`/`H⁻`)와 **반대**다. 형식 선택의 문제이지 계산의 오류는 아니지만, **그대로 옮겨 쓰면 안 된다**.

### 3c. `Table S2`–`S13` — 준안정 (탈)리튬화상의 부피·밴드갭·σ ★

> ⚠ **σ 는 AIMD 단일 온도 값이고 온도가 계마다 다르다** (황화물 아지로다이트·LGPS = **600 K**, 나머지 = **1000 K**). **MSD 창·궤적길이·시드·오차막대 0건** (§8).

**`Table S4` — `Li₆PS₅Cl` (우리 계)**

| 상 | 부피 (Å³) | **격자 a (우리 산수)** | 밴드갭 (eV) | σ (S/m, 600 K) |
|---|---|---|---|---|
| **`Li₆PS₅Cl`** (pristine) | **965.21** | **9.882 Å** | **1.984** | **95.78** |
| 탈리튬 **`Li₄PS₅Cl`** | 935.80 (**−3.05 %**) | 9.780 Å (**−1.03 %**) | **2.391** (**+0.41**) | 43.83 (**−54 %**) |
| 리튬화 **`Li₁₁PS₅Cl`** | 1168.50 (**+21.1 %**) | 10.534 Å (**+6.6 %**) | **1.219** (**−0.77**) | 59.53 (**−38 %**) |

> 🔑 **이 표가 `[Schw20]` 의 `Fig. S3`·XRD 결과를 숫자로 재현한다** (우리 산수): 격자 **−1.03 %** ↔ `[Schw20]` DFT **−1.0 %** ↔ 실측 XRD **−1.09 %**; 리튬화 **+6.6 %** ↔ `[Schw20]` **+6.6 %**. ⇒ **두 논문의 LPSC 구조는 같은 계산이다.**
> 🔴 **밴드갭이 *탈리튬화에서 올라간다*** (1.984 → 2.391 eV). 본문은 *"band gaps ... generally **decrease upon lithiation**"* 라고만 쓰고 이 상승은 언급하지 않는다. 우리 §D 축에 걸리는 값이다 (§7-7).

**나머지 계 (전수)**

| 계 | pristine V / gap / σ | 탈리튬 상 · V / gap / σ | 리튬화 상 · V / gap / σ | T |
|---|---|---|---|---|
| `Li₃PS₄` | 660.68 / **2.675** / 203.61 | `Li₁PS₄` 588.60 / 2.611 / 67.43 | `Li₈PS₄` 762.92 / **1.422** / 302.82 | 1000 K |
| `Li₆PS₅Br` | 1001.00 / **2.093** / 65.80 | `Li₄PS₅Br` 988.54 / 2.173 / 18.36 | `Li₁₀PS₅Br` 1174.62 / **1.391** / 33.57 | 600 K |
| `Li₁₀GeP₂S₁₂` | 982.70 / **2.242** / 68.85 | `Li₄GeP₂S₁₂` 975.99 / 2.124 / 14.27 | `Li₁₈GeP₂S₁₂` 1150.85 / **1.702** / 39.33 | 600 K |
| `LiBH₄` | 400.29 / **6.930** / 233.39 | `Li₀.₈₈BH₄` 316.35 / 6.763 / 243.08 | ⚠ "`Li₁BH₄`" 602.58 / **0** / 260.49 | 1000 K |
| `Li₃YBr₆` | 553.48 / **3.723** / 142.26 | `LiYBr₆` 578.99 / 1.745 / 22.71 | `Li₇YBr₆` 711.29 / **0** / 248.49 | 1000 K |
| `Li₃OCl` | 469.20 / **4.764** / 55.25 | `LiOCl` 406.88 / **0** / 58.55 | — (없음) | 1000 K |
| `Li₂PO₂N` | 942.68 / **5.536** / 5.75 | `LiPO₂N` 1025.14 / 3.037 / 18.21 | `Li₄PO₂N` 1330.15 (**+41 %**) / **0.873** / 128.84 | 1000 K |
| `Li₇La₃Zr₂O₁₂` | 2217.17 / **4.113** / 52.85 | ⚠ "`Li₇La₃Zr₂O₁₂`" 2211.57 / 3.920 / 0.81 | — (없음) | 1000 K |
| `Li₀.₃₃La₀.₅₆TiO₃` | ⚠ 행 순서 뒤섞임 | `Li₀.₁₈₇₅…` 948.47 / 1.793 / 4.04 | `Li₀.₃₇₅…` 933.45 / **0** / 0.86 | 1000 K |
| LATP | 1404.34 / **2.4735** / 104.46 | `Al₀.₅Ti₁.₅(PO₄)₃` 1403.86 / 2.129 / **\*** | `Li₃Al₀.₅Ti₁.₅(PO₄)₃` 1351.52 / 2.049 / 30.06 | 1000 K |
| LAGP | 1278.20 / **2.547** / 70.96 | `Li₁.₃₃…` 1272.84 / **3.318** / 53.98 | `Li₃.₅…` 1392.24 / 2.625 / 8.49 | 1000 K |

> `*` = "No Li in structure".
> ⚠ **SI 표 라벨 오류 4건** (§10-6): `Table S4` 캡션이 *"of Li₆PS₅**Br**"*(내용은 Cl) · `Table S6` 의 "리튬화 `Li₁BH₄`" 가 **pristine 과 같은 조성** · `Table S10` 의 "탈리튬 `Li₇La₃Zr₂O₁₂`" 가 **pristine 과 같은 조성** · `Table S11` 은 **첫 행이 `Li₀.₁₈₇₅` 인데 두 번째 행(`Li₀.₃₃`)에 "Delithiated" 가 붙어 있다**(pristine 이 `Li₀.₃₃`).
> ⚠ **본문의 일반화 두 개가 표와 어긋난다**: *"Most metastable phases show a significant volume **increase during lithiation**"* — LATP 는 리튬화에서 **부피가 준다**(1404.34 → 1351.52, **−3.8 %**), LLTO 도 준다. *"ionic conductivity ... **drops** for the (de)lithiated phases"* — `LiBH₄`·`Li₃OCl`·`Li₂PO₂N` 은 **오른다**(`Li₂PO₂N` 리튬화는 5.75 → **128.84 S/m, 22×**).

### 3d. 본문이 명시한 전압·문헌 대조

| 항목 | 값 | 출처 |
|---|---|---|
| 황화물 탈리튬화 = **S²⁻ → S⁰** | **2.2–2.5 V** vs Li/Li⁺ | 본문 p.1490 (*"similar to the potential of sulfur electrodes"*) |
| 황화물 리튬화 = **P⁵⁺ → P⁰** | **1.1–1.2 V** | 본문 p.1490 |
| 추가 환원 **P⁰ → P³⁻(`Li₃P`)** | **< 0.78 V** | ref 23 (Park & Sohn 2007) |
| LPS intrinsic 산화 2.47 V ↔ 실측 | **2.6 V** | ref 20 (Hakari 2015) |
| LGPS intrinsic 1.19–2.38 ↔ 실측 | **≈1.2–2.5 V** | refs 10, 11 (Han 2016 · Han 2015) |
| LPSB intrinsic 산화 2.23 ↔ 실측 | **≈2.5 V** | 본문(출처 미표기) |
| LBH intrinsic 0–3.43 ↔ 실측 | **0–3 V** | ref 18 (Takahashi 2013) |
| LIPON intrinsic 산화 4.12 ↔ 실측 | **≈4.3 V** | ref 27 (Put 2018) |
| LLZO intrinsic 0–3.61 ↔ 실측 | **3.6 V** + Li 금속 안정 | refs 10, 31, 32 |
| LATP 삽입 개시 실측 | **2.5 V** (`Li₁₊ₓTi₂₋ₓAlₓ(PO₄)₃`) | ref 34 (Arbi 2010) |
| LATP 리튬화 대칭 저하 | **R-3c → R-3** | ref 35 (Arbi 2014) |
| LATP 양극(NMC) 대면 안정 | 창 **밖에서도** 구조 안정 계면 | ref 36 (Liang 2018) |
| `Al₀.₅Ti₁.₅(PO₄)₃` 의 화학 안정성 근거 | `Ti₂(PO₄)₃` **0.013 eV/atom above hull** | ref 16 (MP) |
| LATP 첫 hull 점까지의 산화전압 | ⚠ **3.37 V** (Table 2 의 intrinsic 산화 **3.77 V** 와 다르다 — §10-5) | 본문 p.1491 |

---

## 4. 두 창의 조작적 정의 ★★ (감사 ①의 심장)

**decomposition window (printed, p.1490):**
> *"To determine the decomposition window, we calculated the formation energy of the most favorable decomposition products at a specific potential, which are determined from the **Li grand potential phase diagram**.⁸,⁹ **The decomposition potential closest to the stable solid electrolyte phase defines the reduction and oxidation redox potentials of the window.** It is essential to realize that this does not consider the decomposition route, and the associated reaction barrier may lead to an overpotential necessary to form the decomposition products."*

**intrinsic window (printed, p.1490):**
> *"The intrinsic window of a solid electrolyte is determined from the change in calculated formation energies upon Li insertion and extraction. Thus, the solid electrolyte structure is considered electrochemical active through Li insertion/extraction. The associated **average oxidation/reduction potential** is calculated by **referencing the formation energies to the Li-metal chemical potential similar to intercalation electrodes**.¹⁵ These (de)lithiated solid electrolyte phases often have a **higher formation energy compared to the most favorable decomposition products** ... and therefore represent **metastable or unstable phases**."*

**⇒ 축별 대조 (판정 아님, 나란히만)**

| 축 | 이 논문 **decomposition** | 이 논문 **intrinsic** | 우리 `esw_lis4excluded.json` |
|---|---|---|---|
| 열린 변수 | **μ_Li** (grand potential) | Li 조성 x (닫힌계, 전하중성) | **μ_Li** (grand potential) |
| 상공간 | Li–P–S–Cl **전체** (MP) | **아지로다이트 구조 안**의 Li 배열만 | Li–P–S–Cl **전체** (MP2020-corrected) |
| 전압식 | 분해전압 (μ_Li ↔ φ) | **Aydinol 평균 인터칼레이션 식** (ref 15) | μ_Li ↔ φ (`mu_Li_ref = −2.3867 eV`) |
| 한계의 정의 | **"SE 조성에 가장 가까운 분해전압"** | 첫 hull 점까지의 평균전압 (⚠ **셀 크기 의존**, §10-5) | **Li 교환이 0 인 구간의 양 끝** |
| pseudo-binary 인가 | ❌ 아니다 | (해당 없음 — 인터칼레이션) | ❌ 아니다 |
| 상도 스냅샷 | **MP, 판본 미기재** (ref 16 = Jain 2013) | (자체 DFT) | **MP2026** (`mp-aaaceqmj` 등 신 id) |
| `[Xiao20Rev]` 4층 | **층 ① (worst case)** | **층 ② (topotactic, best case)** | **층 ①** |

🔑 **"closest to the stable solid electrolyte phase"** 가 열쇠다. SE 조성에서 **양쪽으로 가장 가까운** 분해전압 = **Li 교환량이 0 에서 벗어나기 시작하는 두 전압** = 우리 프로파일에서 **Li 교환 0 인 구간의 양 끝**. **같은 양이다.**

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5a. 두 창의 전경 (`Fig. 1`) — **실독**

가로 막대 12행, x 축 **Voltage vs. Li/Li⁺ 0–4.5 V**. 색이 계열을 가른다: **노랑=황화물**(LPS·LPSB·LPSC·LGPS) · **파랑**(LBH·LYB) · **주황=산화물**(LOC·LIPON·LLZO·LLTO) · **초록=NASICON**(LATP·LAGP). 범례는 **진한색 = Decomposition window**, **연한색 = Intrinsic window**.

> 🔎 **그림이 범례와 정확히 일치하지 않는다 (실독으로만 잡힌다).** 기하학적으로 **진한 띠는 두 창의 *교집합***이다. 대부분의 행에서는 intrinsic ⊃ decomposition 이라 교집합 = decomposition 이므로 범례가 맞아 보인다. 그러나 **LLTO·LATP 에서는 intrinsic 이 더 좁아** 진한 띠가 **intrinsic** 이 된다 — LATP 행은 `figure-read ≈` **2.17–2.74 연초록 · 2.74–3.77 진초록 · 3.77–3.86 연초록**, 즉 진한 부분이 **2.74–3.77 = intrinsic** 이다. 캡션이 말하는 *"indicated by the solid line"* 은 그 두 경계(**≈2.74 · ≈3.77**)에 그어진 **세로 실선**이다. LLTO 도 같은 구조(세로 실선 **≈2.10**).
> ⇒ ⛔ **이 그림에서 "진한 띠 = decomposition" 으로 읽고 LLTO·LATP 값을 옮기면 틀린다.**

`figure-read ≈` 로 LPSC 행을 읽으면 연노랑 **≈1.11 → ≈2.19**, 진노랑 **≈1.72 → ≈2.01** — `Table 2` 인쇄값과 일치한다(그림에서 값을 캘 필요는 없다, 표가 있다).

### 5b. `Fig. S11` — **두 창이 한 그림 안에서 어떻게 갈리는가** (실독 · 이 digest 에서 가장 개념적으로 중요한 그림)

> ⚠ SI 캡션이 **"Figure 11"** 로 인쇄돼 있다(= `Figure S11`). 본문은 이 그림을 인용하지 않는다.

`Li_xPS₄` 의 formation energy(eV/f.u.) vs x (0–10). 파란 ✕ = 모든 Li 배열, 파란 선 = hull, **주황 동그라미 = hull 정점** — `figure-read ≈` **x = 0(0) · 0.5(−1.45) · 1(−2.2) · 3(−4.5) · 8(−4.05) · 9(−3.72) · 10(0)**. **굵은 검은 ✕ 두 개**에 이름이 붙어 있다:
- **`P₂S₅ + S`** at **x = 0, ≈−1.65 eV** (탈리튬 끝의 분해산물)
- **`P + Li₂S`** at **x = 8, ≈−6.4 eV** (리튬화 쪽 분해산물)

캡션이 방법을 한 문장으로 준다: *"**The slope between Li₃PS₄ (x = 3) and the phases on the convex the voltage can be determined.** The difference in slope between the decomposition products and Li₃PS₄ is smaller as the difference in slope between the most favorable (de)lithiated phases on the convex indicating a wider voltage window for the (de)lithiated phases."*

> 🔑 **우리 산수로 그 기울기를 실제로 재 보면 `Table 2` 가 나온다** (그림 좌표는 figure-read):
> · **산화**: pristine(3, −4.5) → 분해산물(0, −1.65) 기울기 **−0.95 eV/Li**; pristine → hull 첫 점(1, −2.2) 기울기 **−1.15 eV/Li** ⇒ 차 **0.20 V** ↔ `Table 2` 의 **2.47 − 2.30 = 0.17 V**
> · **환원**: pristine(3, −4.5) → 분해산물(8, −6.4) 기울기 **−0.38 eV/Li**; pristine → hull(8, −4.05) 기울기 **+0.09 eV/Li** ⇒ 차 **0.47 V** ↔ `Table 2` 의 **1.72 − 1.24 = 0.48 V**
> ⇒ ✅ **두 창 모두 "pristine 조성에서 목표점까지의 직선 기울기" 다.** 방법이 검산됐다. (형성에너지가 두 끝단 기준이라 기울기와 전압은 **상수만큼** 어긋나고, 그 상수가 두 경로에 공통이라 **차이는 그대로 전압차**가 된다.)

### 5c. `Fig. S2` — 아지로다이트 hull (실독) · ⚠ **캡션과 축이 다르다**

캡션은 *"Formation energies per formula unit for x in Li_xPS₅**Cl**"* 인데, **그림의 x 축 라벨은 `x in Li_xPS₅Br`** 다. hull 정점은 `figure-read ≈` **x = 0(0) · 1(−3.55) · 2(−4.13) · 4(−5.13) · 6(−5.80) · 11(−1.83) · 12(0)**.

> 🔴 **결론: 이 SI 에는 `Li₆PS₅Cl` 의 hull 그림이 없다** (있다면 이 그림이 Br 이므로 Cl 쪽이 통째로 빠진 것이고, 반대면 캡션이 틀린 것이다 — 둘 중 하나다). **LPSC 의 hull 정본은 `[Schw20]` `Fig. 2a` 다.** 두 그림의 정점 집합(**0, 1, 2, 4, 6, 11, 12**)은 **같다**.
> ⚠ 단 **`Table S3`(LPSB) 의 리튬화상은 `Li₁₀PS₅Br`** 이고 **`Table S4`(LPSC) 는 `Li₁₁PS₅Cl`** 이다 — hull 정점이 x=11 인 이 그림은 **Cl 쪽과 정합**한다. ⇒ **축 라벨(Br)이 틀렸을 가능성이 더 높다.** 확정은 못 한다.
> 본문은 *"The convex hulls of the additional solid electrolyte materials are shown in Figures S1−S7"* 라고 쓰는데, **추가 계는 10종인데 그림은 7장**이다 ⇒ **LLZO·LAGP 와 아지로다이트 한쪽의 hull 이 실리지 않았다.**

### 5d. `Fig. 2a,b` — LATP: 볼록 hull = 고용체 (실독)

**a**: `Li_xAl₀.₅Ti₁.₅(PO₄)₃`, x **0 → 3.67**. hull 정점이 `figure-read ≈` **0 · 0.67 · 1.33 · 1.5 · 1.67 · 1.92 · 2.5 · 3.0 · 3.67** 로 **촘촘하고 곡선이 매끄러운 사발 모양**이다. ✕ 구름이 hull 바로 위에 두껍게 깔린다 ⇒ **고용체**. 최저점은 `figure-read ≈` x **1.67–1.9 (≈−3.15 eV)** 로, **pristine x = 1.5 (≈−3.1) 가 hull 최저점이 아니다**.
**b**: x = 0 / 1.5 / 3 의 완화 구조 (빨강 O, 주황 P, 흰색 Ti, 파랑 Al, 분홍 Li). **세 구조 모두 능면체 골격이 유지**되고 `PO₄` 가 약간 회전할 뿐이다 — 상자 모양·PO₄ 연결이 눈으로 같다.

### 5e. `Fig. 2c,d` — LGPS: V자 hull = 상분리 (실독)

**c**: `Li_xGeP₂S₁₂`, x **0 → 22**. hull 정점 `figure-read ≈` **0(0) · 2(−5.05) · 4(−6.1) · 10(−9.05) · 18(−3.4) · 20(−1.65) · 22(0)**. **x = 4 → 10 → 18 이 두 개의 직선**으로, 꼭짓점이 **pristine x = 10** 에 정확히 있다 ⇒ 그 구간 전체가 **두 상 평탄** = **상분리**.
**d**: x = 4 / 10 / 22 구조. **x = 4 상자가 눈에 띄게 기울어져 있다**(각도 변화) 반면 x = 10 은 반듯하다. x = 4 에서 노란 S 끼리 붙은 **S–S** 가 보이고, x = 22 에서는 `PS₄`·`GeS₄` 가 깨져 분홍 Li 가 가득하다.

> 🔎 **본문과 그림이 어긋난다**: 본문은 *"In Figure 2d, the structures of the most stable configurations `Li₄GeP₂S₁₂` and **`Li₁₈GeP₂S₁₂`** are shown"* 라고 쓰는데, **그림과 캡션의 라벨은 `x = 4, 10, 22`** 다. `Table S5` 의 리튬화 준안정상도 **`Li₁₈GeP₂S₁₂`** 다 ⇒ **`Fig. 2d` 의 세 번째 패널은 hull 정점(x=18)이 아니라 완전리튬화 끝단(x=22)** 이다 (§10-5).

### 5f. `Fig. S9` — S–S RDF (실독)

`Li_xGeP₂S₁₂` 의 **S–S** RDF, x = **18**(파랑) · **10**(빨강) · **4**(노랑). 가로 r 0–10 Å, 세로 **Intensity (a.u.) — 눈금 없음**.
- **r ≈ 2.0 Å 에 x = 4 만 날카로운 봉우리**가 있다(`figure-read ≈` 최대봉의 **0.2 배**). x=10·x=18 은 그 자리에서 **정확히 0** 이다 ⇒ **탈리튬화가 S–S 결합을 만든다** = S²⁻ 산화의 구조 지문.
- x=10 은 **3.35 / 4.0 / 5.8 / 6.8 Å** 봉우리가 뾰족한데, x=4 는 **3.4 / 5.1 Å 근처로 뭉개지고**, x=18 은 **3.9 Å 하나로 넓어지며 꼬리가 9.5 Å 까지** 간다(셀 팽창) ⇒ **양쪽 다 비정질화**.

> ⇒ `[Schw20]` `Extended Data Fig. 1` 의 아지로다이트 결과(x=4 에만 r≈2.1 Å S–S)와 **같은 현상을 LGPS 에서 재현**한 것이다. **새 정보는 아니고 일반성 보강**이다.

### 5g. `Fig. S8` — 계산 경로 흐름도 (실독)

`Electrochemical stability` 에서 두 갈래.
- 왼쪽 **"Phase diagram of decomposition products"** → **Decomposition Window** → **Decomposition products**
- 오른쪽 **"Convex hull of (de)lithiated structure"** → **Intrinsic Window** → hull 모양으로 분기: **"Convex shape" → Solid Solution** / **"V-shape" → Phase separation**
- 아래쪽 주황 선: **Phase separation → (라벨 "Metastable phase") → Decomposition products**

> 🔑 **Solid Solution 상자에서는 분해산물로 가는 화살표가 없다.** 상분리 계에서만 간접 경로가 그려진다.
> 🔴 **그리고 이 흐름도 어디에도 "장벽/kinetics" 상자가 없다** — 운동학은 **가정으로만** 들어온다 (§10-1).

### 5h. `Fig. 3` — 셀 모식도 + 두 시나리오의 에너지 도식 (실독)

**a**: 복합전극 그림(주황 집전체 · 초록 활물질 · 베이지 전해질 입자 · 검정 도전재). 오른쪽 확대에 **"Stability Window"** 와 세로 **V** 화살표, 그 아래 **"Interfaces"** 육각 타일에서 **전해질‖활물질·전해질‖도전재 경계만 빨간 선**으로 칠해져 있다 ⇒ *"전위를 느끼는 것은 저 경계의 SE 뿐"*.
**b (Phase separation)**: Gibbs 자유에너지 vs x. 우물 두 개 — **x₁ 회색공 = Solid electrolyte**, **x₂ 노란공 = Intrinsic Intermediate**. 그 사이에 **점선 높은 봉우리 + 위로 향한 점선 화살표 = "Nucleation Barrier"**, 실선은 그보다 **낮은 봉우리**. x₂ 아래 **초록공 = Decomposition Products** 로 내려가는 짧은 화살표.
**c (Solid solution)**: 단조 감소하는 실선 위를 회색공(x₁) → 노란공(solid solution)이 **화살표를 따라 미끄러지고**, 초록공(분해산물)은 x₂ 에 **곡선에서 떨어져** 놓여 있다.

> 🔑 **이 두 그림이 이 논문의 "왜" 다**: 상분리면 *직접* 경로에 큰 핵생성 장벽이 있고 *간접* 경로는 Li 이동 장벽뿐이라 간접이 이긴다 / 고용체면 애초에 장벽 없이 조성이 미끄러지므로 **고용체의 끝을 정하는 것은 분해전압**이다.
> 🔴 **세로축에 눈금이 없다. eV 값 0개.** 이 그림은 **주장의 도해이지 계산 결과가 아니다** (§10-1).

### 5i. 계별 서사 (본문)

- **황화물 4종**: intrinsic 이 훨씬 넓다. 그 이유로 *"direct decomposition is kinetically hindered"* 를 **가정**하고, 근거로 **실측과의 일치**를 든다. ⚠ 실험압력 관련 단서 한 줄: 비교한 실험들은 *"performed without extra external pressure ... pressure differences of at most several MPa"* 이고 이는 *"low compared to the much larger pressures that would theoretically influence the stability window"*(ref 22 Fitzhugh 2019) ⇒ **압력 보정은 안 한다**.
- **CV 반박 재확인**: *"CV experiments using sulfide solid electrolytes report voltage ranges beyond 0−5;²⁴,²⁵ however, these experiments are performed **without conductive additive** mixed with the solid electrolyte and are thus **unable to capture the intrinsic electrochemical window**"* ⇒ ⭐ **우리가 `[Du22LMR]`·`[Zuo]` 의 CV onset 을 인용할 때마다 붙여야 할 문장**이다.
- **LBH·LYB**: intrinsic 은 **Li 금속까지 안정(0 V)** 이라 하는데, **LYB 는 실제로 Li 금속에 환원된다**(ref 17 Asano 2018) ⇒ 저자 스스로 *"in this case, the **decomposition window has a better predictive value**"* 라고 쓴다. 이유로 **조성 공간이 작아 핵생성 장벽이 작다**는 가설을 댄다. 🔑 **이 논문이 자기 방법의 실패 사례를 명시한 유일한 자리.**
- **LOC**: Li 가 유일한 환원 가능 원소 ⇒ 환원 decomposition 한계가 **Li 금속 전위와 같다**. 산화 실측값은 *"not reported"*.
- **LIPON**: intrinsic 0–4.12 V, 실측 산화 **≈4.3 V**(ref 27). Li 금속 대면 안정성은 **논쟁 중**이라고 쓰고(refs 3, 27–30), hull 위 안정 조성으로 **`Li₁PO₂N`·`Li₄PO₂N`**(`Fig. S6`)을 든다.
- **LLZO**: decomposition 0.05–2.68 → intrinsic 0–3.61, 실측 **3.6 V**. ⚠ **본문 문장이 산화/환원을 뒤바꿔 쓴다** (§10-6).
- **LLTO**: intrinsic 환원(2.10) > decomposition 환원(1.71) ⇒ **삽입이 분해보다 먼저**. 실측 근거는 **LLTO 의 인터칼레이션**(Ti⁴⁺→Ti³⁺, ref 33) — `Li₄Ti₅O₁₂` 와 같은 거동.
- **LATP**: 양쪽 다 intrinsic 이 안쪽 ⇒ **산화·환원 모두 삽입/추출이 분해보다 먼저**. 실험 근거 2건(ref 34 삽입 개시 2.5 V · ref 35 R-3c→R-3 가역). 저자의 결론 문장이 중요하다: ***"the structural stability of the solid electrolyte extends beyond the electrochemical stability window"*** — 그리고 (탈)리튬화는 **Li 이온전도를 떨어뜨리고 전자전도를 올려** 내부저항을 키우거나 SE 의 redox 활성을 촉진한다.
- **LAGP**: intrinsic 이 더 넓고 양쪽 다 **1차 상전이**(= 상분리) ⇒ 간접 경로로 분해산물이 만들어질 것으로 본다.

### 5j. 토론의 핵심 가설 — "복잡할수록 핵생성 장벽이 크다"

> *"A larger number of elements in a specific compound ... in general **raises the nucleation barrier** toward stable decomposition products, thus enabling the formation of intermediate metastable phases.²⁸ Additionally, the type of bonds, electronic structure, and **chemical disorder** can contribute to the chemical complexity ... Therefore, **for complex solid electrolytes, it is expected that the direct decomposition stability window is a lower limit** and that redox activity will take place at potentials dictated by intrinsic (de)lithiation."*

⭐ **이 문장이 우리 "2.256 V = worst-case 하한" 프레이밍의 가장 직접적인 외부 활자다.** 단 **하한의 값은 저들 기준 2.01 V 이지 2.256 V 가 아니다**(§7-5).
그리고 반대 방향의 문장도 같이 있다 — 단순한 계(이원 Li 염 등)는 확산거리가 짧아 장벽이 작고 *"the practical stability will approach the electrochemical decomposition window"*.
⚠ **이 "복잡도 → 장벽" 가설은 정량화되지 않는다.** 원소 수를 세는 것 말고 지표가 없고, 장벽 값은 0개다. 본문은 **`Li₃YB₆`** 라고 오타까지 낸다(= `Li₃YBr₆`).

---

## 6. 기전 — "intrinsic vs decomposition" 을 한 단계씩

### 6-1. 두 창은 서로 다른 질문의 답이다

| | **decomposition window** | **intrinsic window** |
|---|---|---|
| 묻는 것 | *"최종 평형 산물이 언제 유리해지나"* | *"SE 자신이 언제 Li 를 내놓/받나"* |
| 계산 | Li grand potential 상도 (MP 참조) | SE 구조 안 Li 배열 convex hull + Aydinol 평균전압 |
| 요구되는 원자 이동 | 음이온 골격 재배열 + 다상 **핵생성** | **Li 만** 움직임 |
| 장벽 | 클 수 있다 (미계산) | Li 이동 장벽 (미계산) |
| `[Xiao20Rev]` 층 | **① worst case** | **② topotactic best case** |
| LPSC 값 | **1.72–2.01 V** | **1.11–2.19 V** |

### 6-2. 창 밖에서 무슨 일이 일어나나 — hull 모양이 가른다 (이 논문의 *새로운* 기여)

`Fig. S8` + `Fig. 3b,c`:
- **V자 hull → 상분리(first-order)**: pristine 조성이 두 직선의 꼭짓점 ⇒ 두 상 평탄 ⇒ **중간 준안정상**이 생기고, 그 상이 **분해산물로 무너진다**. (LGPS·LAGP·아지로다이트)
- **볼록 hull → 고용체**: 조성이 연속적으로 변하고 전압도 연속적으로 변한다 ⇒ **중간 준안정상이라는 것이 없다.** 이때 *"the end of the solid solution reaction is most likely **determined by the decomposition potential**"*. (LATP·LLTO)

🔑 **여기서 나오는 실용적 함의 한 줄**: 고용체 계에서는 **구조 안정 범위가 전기화학 창보다 넓을 수 있고**, 그러면 SE 가 복합전극 용량에 **가역적으로 기여**한다(대신 국소 이온전도는 떨어진다).

### 6-3. 왜 간접이 이긴다고 보는가 — 논증 사슬 (그리고 그 사슬의 구멍)

1. SE 는 **Li 이동 장벽이 작게 설계된 물질**이다 ⇒ (탈)리튬화는 빠르다.
2. 골격 원소(P·S·Ge·…)는 **낮은 확산성**을 의도한 것이다 ⇒ 직접 분해는 느리다.
3. ⇒ 전위가 걸리면 **먼저 일어나는 것은 (탈)리튬화**이고, 관측되는 창은 intrinsic 이다.
4. 🔴 **1–3 어디에도 장벽 수치가 없다.** `Fig. 3b` 의 "Nucleation Barrier" 는 눈금 없는 도식이고, NEB·전이상태·핵생성 이론 계산은 **0건**이다 ⇒ **"kinetically hindered" 는 이 논문에서 가정이다** (§10-1).

---

## 7. 우리 DFT 와의 대조 ★★★ — **`[Zhu15]` 3.4× 감사**

> ⚠ 아래 문헌값은 전부 **소환값**이다. 우리 db 절대값과 같은 셀에 놓지 않는다. 우리가 뺀 값은 **(우리 유도, 논문 미보고)** 로 표시한다.
> 우리 쪽 원본: `db/properties/esw_lis4excluded.json` · `litdb/our_dft_baseline.md` L19–L27 · 도구 `tools/oxidation/constrained_esw.py:80–95` · `tools/oxidation/esw_cascade_batch.py:413–435`.

### 7-1. 🔴 먼저 확정 — **이 논문은 `[Zhu15]` 의 0.30 V 를 *재현한다***

`Table 2` 캡션 축자: *"Calculated Decomposition Electrochemical Stability Window, Assuming Direct Decomposition to the Most Stable Decomposition Products **(Values in Agreement with the Calculations in Literature⁸)**"*. **ref 8 = Zhu, Y.; He, X.; Mo, Y., *ACS Appl. Mater. Interfaces* 2015, 7 (42), 23685−23693** = 우리 `[Zhu15]`.

| | LPSC 환원 / 산화 | 폭 |
|---|---|---|
| `[Zhu15]` (우리 기록) | **1.71 / 2.01** | **0.30** |
| **이 논문 `Table 2`** | **1.72 / 2.01** | **0.29** |
| `[Schw20]` `Fig. 2b` 흑색 ✕ (우리 figure-read) | ≈1.70 / ≈2.01 | ≈0.31 |

⇒ **세 판이 같다.** ✅ **부수 소득 1**: `schwietert2020` digest 의 **figure-read ≈2.01 / ≈1.70 V 가 인쇄값으로 확인됐다** — 그 digest §9 의 불확실 표기를 해제할 수 있다.
⇒ 🔴 **따라서 3.4× 는 저쪽의 전사 오류가 아니다. 설명할 책임은 우리에게 있다.**

### 7-2. 🔑 저들 정의로 **우리 자신의 프로파일**을 다시 읽는다

우리 `esw_lis4excluded.json` comp1 의 `steps` 는 pymatgen `get_element_profile` 출력이다. 각 행은 **(임계 Li 교환량, 그 조성에서의 평형반응, 그리고 그 조성보다 *Li-rich 쪽* 평탄의 전압)** 이다. 이 대응으로 풀어 적으면:

| Li 교환 구간 (음수 = 방출) | **그 구간의 전압** | 그 구간 시작점의 평형 |
|---|---|---|
| −6 → −5 | 3.326 V | `→ 0.5 P₂S₇ + 0.5 S + SCl + 6 Li` |
| −5 → −2 | 2.385 V | `→ 0.5 P₂S₇ + LiCl + 1.5 S + 5 Li` |
| **−2 → 0** | **2.256 V** ← 🔴 **산화 한계** | `→ Li₃PS₄ + LiCl + S + 2 Li` |
| **0 → +5** | **1.717 V** ← 🔴 **환원 한계** | `→ Li₃PS₄ + Li₂S + LiCl` (**Li 교환 0**) |
| +5 → +5.143 | 1.242 V | `+ 5 Li → 5 Li₂S + LiCl + P` |
| +5.143 → +5.429 | 1.177 V | `+ 5.143 Li → 0.1429 LiP₇ + …` |
| +5.429 → +6 | 0.932 V | `+ 5.429 Li → 0.1429 Li₃P₇ + …` |
| +6 → +8 | 0.87 V | `+ 6 Li → LiP + 5 Li₂S + LiCl` |
| > +8 | **0.000 V** | `+ 8 Li → Li₃P + 5 Li₂S + LiCl` |

⇒ **Li 교환이 0 인 구간 = [1.717, 2.256] V, 폭 0.539 V** (우리 유도).

**이 읽기가 맞다는 독립 근거 3개** (pymatgen 내부 구현에 기대지 않는 것만 골랐다):

1. **0.000 V 행.** 완전환원(`+8 Li → Li₃P + 5Li₂S + LiCl`)이 정확히 **0.000 V** = Li 금속 전위에 놓인다. 평탄이 0 V 에 놓일 수 있는 유일한 경우는 **그 평탄이 "완전환원 그 너머"(Li 금속 석출)** 일 때다 ⇒ **행에 적힌 전압은 그 조성의 *Li-rich 쪽* 평탄**이다. 라벨 대응이 이것으로 고정된다.
2. **`Table 2` 의 1.72 가 세 계에서 같다.** `Li₃PS₄`·`Li₆PS₅Br`·`Li₆PS₅Cl` 의 환원한계가 **전부 1.72 V**. 물리적으로 그래야 한다 — 세 계의 Li-보존 평형이 전부 **`Li₃PS₄`** 를 품고, `Li₂S`·`LiCl`·`LiBr` 은 0 V 위에서 환원되지 않으므로 **환원 가장자리는 `Li₃PS₄` 가 정한다**. 그리고 **우리 1.717 V 행의 평형이 바로 `Li₃PS₄ + Li₂S + LiCl` 이고, 바로 아래 평탄이 `Li₃PS₄` 의 환원**(`Li₃PS₄ + 5 Li → 4 Li₂S + P`, 우리 식에 `Li₂S`·`LiCl` 을 더하면 글자까지 일치)이다.
3. **용량 검산.** `Table 1` 의 LPSC 환원용량 **798.85 mAh/g = 8.00 Li**(우리 산수) 는 **우리 0 V 단계의 8 Li 와 같다** ⇒ 두 상집합의 **최종 환원산물이 일치**한다. 산화용량 **599.14 = 6.00 Li** = 완전탈리튬.

> ⚠ **확정의 한계**: 이 컨테이너에는 `pymatgen` 이 없어 프로파일을 **재실행해 검증하지는 못했다**. 위 셋은 강한 정황이지 재실행 검증은 아니다. **닫는 행위는 재실행이다** (§7-8).

### 7-3. 🔴🔴 **그래서 3.4× 는 어디로 갔나**

| | 환원 한계 | 산화 한계 | 폭 |
|---|---|---|---|
| **우리 원장이 인쇄해 온 값** (`our_dft_baseline.md` L20) | **1.242 V** | 2.256 V | **1.014 V** |
| **저들 정의로 다시 읽은 우리 값** (우리 유도) | **1.717 V** | 2.256 V | **0.539 V** |
| **이 논문 `Table 2`** (= `[Zhu15]` 재현) | **1.72 V** | **2.01 V** | **0.29 V** |

- 전체 격차 **1.014 − 0.29 = 0.724 V** 중
  - **0.475 V (66 %)** = **우리 쪽 라벨 오류** — `reduction_V` 가 환원 *한계* 가 아니라 **두 번째 환원 평탄**(P → `LiP₇`)이다.
  - **0.246 V (34 %)** = **산화 쪽 진짜 차이** (2.256 ↔ 2.01).
- 환원 쪽 차이는 **1.717 − 1.72 = −0.003 V** ⇒ **사실상 같은 값**이다.
  🔑 그러므로 `kb/open_items.md` 가 *"우리 OCV 1.717 vs `[Zhu15]` 1.71 — 0.007 V 차인데 같은 양인지 미확인"* 이라 적어 둔 그 우연은 **우연이 아니다. 같은 양이다.**

**남은 0.246 V 의 후보 (우리 유도 · 확정 아님)**
1. **우리 상집합 배제의 몫 ≈0.116 V** — `our_dft_baseline.md` L19 가 *"LiS₄ 포함 시 2.14"* 라고 적는다. `esw_lis4excluded.json` 은 **`LiS₄`·`SCl₃`·`Li₅PS₄Cl₂` 3상을 뺐다**(Gil-González 2022 phase set). 상을 빼면 hull 이 올라가 **onset 이 높아진다** ⇒ 우리 2.256 은 배제 때문에 **위로 밀린 값**이다.
2. **MP 판본 드리프트 ≈나머지** — 저들 참조는 **MP(판본 미기재, 2021 이전)**, 우리는 **MP2026 + MP2020Compatibility 음이온 보정**. `[Schw20]` digest §7-4 가 같은 Li–P 사다리에서 **0.07–0.24 V** 의 판본 드리프트를 이미 쟀다.
3. ⚠ **나머지는 모른다.** 저들이 어떤 산화산물을 냈는지(`Li₃PS₄+S+LiCl` 인지 다른 조합인지) **논문에 없다** — `Table 2` 는 숫자만 준다.

> ⛔ **그러므로 감사는 "닫혔다" 가 아니라 "크기가 줄었다" 로 기록한다**: **3.4× → 1.86×**, 그리고 **어긋나는 변은 두 개가 아니라 하나(산화)** 다.

### 7-4. ✅ 상집합이 실제로 겹친다 (독립 확인)

| | 이 논문 | 우리 `esw_lis4excluded.json` |
|---|---|---|
| LPSC 최종 환원 Li 수 | **8.00 Li** (`Table 1` 798.85 mAh/g, 우리 산수) | **8 Li** (0.0 V 단계) |
| 최종 환원 산물 | `P⁵⁺ → P³⁻(Li₃P)` (본문 + `Fig. S11` 의 `P + Li₂S`) | `Li₃P + 5 Li₂S + LiCl` |
| 중간 환원 단계 | `P⁵⁺ → P⁰` **1.1–1.2 V**, `P⁰ → P³⁻` **< 0.78 V** (ref 23) | `P` 1.242 · `LiP₇` 1.177 · `Li₃P₇` 0.932 · `LiP` 0.87 · `Li₃P` 0.0 |
| 산화 시 redox 원소 | **S²⁻/Cl⁻** (`Table 1`) | **S²⁻ 우선**(2.256 V 에 원소 S), Cl 은 3.326 V 의 `SCl` 부터 |

🔑 **`P⁰ → P³⁻` 가 "0.78 V 아래" 라는 저들 문장은 우리 사다리와 정합**하다 — 우리 `LiP → Li₃P` 는 0.87 V 아래에서 일어난다. ⚠ 단 저들 0.78 V 는 **문헌 소환값**(ref 23, 흑린 전극)이지 자기 계산이 아니다.

### 7-5. ⚠ 우리에게 **불리한 것**을 먼저 적는다

1. 🔴🔴 **우리 `reduction_V` 라벨이 틀렸고, 그 라벨은 한 파일에만 있지 않다.**
   `tools/oxidation/constrained_esw.py:91–94` 와 `tools/oxidation/esw_cascade_batch.py:417–421` 이 **똑같이** `red = max(V | evolution > 0)` 을 쓴다. `evolution == 0` 행(= Li-보존 구간)이 **필터에서 빠지므로**, 환원 한계는 항상 **한 계단 아래**로 잡힌다. `esw_cascade_batch.py:435` 의 **`window_V = ox − red` 가 cascade 전수에 계통적으로 넓다.**
   ⇒ ⛔ **이 digest 로는 우리 db 를 못 고친다**(권한 밖). **`kb/open_items.md` 에 `HZ-esw-reduction-limit-label` 로 올려야 한다.**
2. 🔴 **우리 산화 onset 이 같은 계열에서 혼자 높다.** 2015(Zhu)·2021(이 논문) 두 독립 계산이 **둘 다 2.01 V** 인데 우리만 **2.256 V** 다. 우리 쪽에 **상 3개를 뺀 이력**이 있으므로, *"우리가 더 정확한 최신 상집합을 쓴다"* 는 주장은 **그 배제를 정당화하기 전에는 못 쓴다**.
3. ⚠ **우리 "worst-case 하한" 프레이밍은 살아 있지만 값이 바뀐다.** 이 논문이 *"the direct decomposition stability window is a lower limit"* 라고 활자로 지지해 준다 — **단 그 하한의 수치는 저들 기준 2.01 V** 다. 우리가 2.256 V 를 "하한" 이라 부를 때, **이 문헌에 대해서는 하한이 아니다**.
4. 🔴 **`[Schw20]` digest §7-3 의 "환원 쪽 −0.162 V" 가 이 라벨 위에 서 있다 ⇒ 재판정이 필요하다.**
   · 종전: 저들 간접 1.08 V vs 우리 1.242 V ⇒ −0.162 V
   · **정정(우리 유도)**: 저들 간접(이 논문 값) **1.11 V** vs 우리 층① 환원한계 **1.717 V** ⇒ **−0.607 V**
   · ✅ **그리고 그 −0.607 이 저들 자신의 층①→층② 차(1.72 → 1.11 = −0.61 V)와 같다** ⇒ 정정된 우리 값이 **저들 델타를 재현한다**. 라벨을 고치면 오히려 **정합이 좋아진다**.
5. ⚠⚠ **위험한 우연 하나.** 저들 LPSC **intrinsic(층②) 폭이 1.08 V** 이고 우리가 인쇄해 온 **1.014 V** 와 **0.07 V** 밖에 차이 나지 않는다. ⛔ **이 근접을 "우리 hull 이 간접 경로를 이미 포함한다" 로 읽으면 안 된다** — 우리 1.014 V 는 층② 가 아니라 **층①을 잘못 읽은 값**이고, 두 수가 가까운 것은 **아무 의미 없는 우연**이다.

### 7-6. 🎯 층①/층② 대응 — 3.4× 의 답은 **층 차이가 아니다**

| | 이 논문 이름 | `[Xiao20Rev]` 층 | LPSC 값 | 우리 대응 |
|---|---|---|---|---|
| 분해 개시 | **decomposition window** | **층 ①** worst case | **1.72–2.01 V** | 우리 2.256 V(산화) · **1.717 V**(환원, 정정) |
| 골격 보존 | **intrinsic window** | **층 ②** topotactic | **1.11–2.19 V** | **없음** (우리가 계산한 적 없다) |

- 이 논문이 잰 **층①→층② 보정** (LPSC): 산화 **+0.18 V**(2.01→2.19) · 환원 **−0.61 V**(1.72→1.11) · 폭 **0.29 → 1.08 V**.
  ⚠ `[Schw20]` 은 같은 물질에 **2.24 / 1.08 V** 를 적었다 ⇒ **같은 저자가 1년 만에 자기 층② 값을 0.05 / 0.03 V 바꿨다**. **층② 값의 재현성 스케일이 ≈0.05 V** 라는 뜻이다(우리 유도).
- ⇒ **3.4× 는 층①/층② 혼동이 아니다.** 우리 값은 처음부터 끝까지 층① 안에 있었고, 문제는 **층① 안에서 환원 가장자리를 잘못 골랐다**는 것이다.

### 7-7. §A·§D 축으로 넘어가는 것 (작지만 실물)

| 축 | 이 논문 값 (`Table S4`, 소환값) | 우리 값 | 쓸 수 있는 말 |
|---|---|---|---|
| **§D 전자구조** | `Li₆PS₅Cl` 밴드갭 **1.984 eV** (**DOS 판독**, k-mesh 증가 nscf) | comp1 **2.066 eV** (**fixed-occ nscf VBM/CBM**) | ⛔ **절대 비교 금지** — 저들은 우리 규율이 **금지한 DOS-threshold 판독**이고(우리 기준 ~0.3 eV 과소), 무질서 배열도 1개다. **"둘 다 wide-gap(≈2 eV급)"** 까지 |
| **§D 파생** | 탈리튬 `Li₄PS₅Cl` **2.391**(↑) · 리튬화 `Li₁₁PS₅Cl` **1.219**(↓) | — | ⭐ **방향 정보로만**: 리튬화가 갭을 닫아 **전자누출을 키운다** = 음극쪽 자기촉매 고리. **탈리튬화는 갭을 *올린다*** (본문 서술과 어긋남, §10-6) |
| **§A 이온전도** | 600 K AIMD σ: pristine **95.78** → 탈리튬 **43.83**(−54 %) → 리튬화 **59.53 S/m**(−38 %) | comp1 D(600 K) 3.09×10⁻⁶ cm²/s (MLIP-MD) | ⛔ **절대값 비교 금지**(AIMD ↔ MLIP-MD, 창·시드·열욕 전부 미기재). **"(탈)리튬화가 σ 를 절반 가까이 떨군다" 는 *부호*만** |
| **§C 기계** | 부피만 (`Table S2`–`S13`) | — | 격자 −1.03 % / +6.6 % (우리 산수) — `[Schw20]` XRD 대조와 **같은 값**이므로 **새 정보 아님** |

### 7-8. 🟡 판정과 조치

> **판정: 🟡 감사 축소 + 우리 쪽 정정 1건 (🔴 재계산은 아니다).**

**즉시 (권한 밖이라 제안만 · `_pending_index_*` 에 넣었다)**
1. **`HZ-esw-reduction-limit-label` 신설** — `our_dft_baseline.md` L20 의 *"환원 한계 1.242 V"* 와 `esw_lis4excluded.json` 의 `reduction_V`, 그리고 `esw_cascade_batch.py` 의 `window_V` 전수. **정정 전까지 `window_V` 인용 금지.**
2. **`kb/open_items.md` 의 "Zhu15 3.4× 감사" 갱신** — 3.4× → **1.86×**, 원인 분해(66 % 라벨 / 34 % 산화 한 변), 그리고 *"OCV 1.717 vs 1.71 은 우연이 아니라 같은 양"* 확정.
3. **`[Schw20]` digest §7-3 의 환원 델타 −0.162 V 정정** → **−0.607 V**(정정하면 저들 델타 −0.61 과 일치).

**닫는 계산 1건 (이게 감사를 실제로 닫는다)**
- `pymatgen` 으로 **comp1 프로파일을 재실행**해 `evolution == 0` 구간의 양 끝을 직접 출력한다. `LiS₄`·`SCl₃`·`Li₅PS₄Cl₂` **포함/배제 두 판**으로 돌려 산화 한계가 2.01 V 쪽으로 얼마나 내려가는지 본다.
  ⚠ 던지기 전에 `kb/templates/estimand_card.md` 를 채운다 — **"환원 한계" 의 보고량 정의가 바로 이 감사의 쟁점**이다. §1–3 에 적을 문장: *"환원 한계 ≡ Li 교환량이 0 에서 벗어나기 시작하는 가장 높은 φ"*.
- ⛔ **층② 계산은 이 감사와 별개다.** `[Schw20]` digest §7-9 가 이미 선택 항목으로 제안했고, **여기서 새로 요구하지 않는다**.

---

## 8. DFT/계산 방법 ★

| 항목 | 값 | 우리 규율에서의 코멘트 |
|---|---|---|
| **코드** | **VASP** (ref 14) | ⚠ **인용 오기**: ref 14 는 *Kresse & Hafner, PRB 47, 558 (1993)* = "Ab initio MD for liquid metals" 로, **PAW 논문이 아니다**(PAW = Blöchl 1994 / Kresse–Joubert 1999). 본문은 *"PAW pseudopotentials as implemented within ... VASP¹⁴"* 라고 쓴다 |
| **범함수** | **PBE GGA** (ref 13) | ⚠ **`[Schw20]` 과 똑같은 인용 오기**: ref 13 은 *Perdew, Burke & **Wang**, PRB **54**, 16533 (1996)* = 교환상관 hole 논문이지 PBE(PRL 77, 3865) 가 아니다. **두 논문이 같은 실수를 물려받았다** |
| **vdW** | **없음** | 우리도 없음 — 동일 |
| **ecut** | 🔴 **없다.** 본문은 *"The k-point mesh and **energy cutoff** values ... are reported in Table S1"* 라고 쓰는데 **`Table S1` 에 cutoff 열이 없다** | 🔴 **재현 불가 항목 1**. `[Schw20]` 값(280 eV / 산화물 500 eV)을 승계했다고 **추정할 수밖에 없다** — 활자 근거 0 |
| **k-점** | `Table S1`: LPS **5×3×3** · LPSB **4×4×4** · LGPS **3×3×3** · LBH **5×5×5** · LYB **5×5×5** · LOC **3×3×3** · LIPON **1×1×1** · LLTO **3×3×1** · LATP **3×3×1** | 🔴 **LPSC·LLZO·LAGP 행은 k-점이 "−"** = 미기재. **우리 계(LPSC)의 k-점이 이 논문에 없다** (ref [3] = `[Schw20]` 의 arXiv 판으로 넘긴다 ⇒ 4×4×4) · **LIPON 을 Γ점 하나로** 돌린 것은 약하다 |
| **셀** | `Table S1`: 대부분 **1×1×1**, LBH **1×2×1**, LOC **2×2×2**, LIPON **1×2×2**, LLTO **2×2×2**. LPSC·LLZO·LAGP **미기재** | 🔴 **셀 크기가 intrinsic 창의 분해능을 정한다 — 저자가 직접 그렇게 쓴다** (§10-5) |
| **구조 출처** | LPS `mp-985583` · LBH `mp-30209` · LOC `mp-985585` · LIPON `mp-1020019` (전부 MP) · LPSB ref 2(de Klerk 2016) · **LPSC·LLZO ref 3 = `[Schw20]` arXiv:1908.10144** · LGPS ref 4(Kuhn 2013) · LYB ref 5(Bohnsack 1997) · LLTO ref 6(Teranishi 2016) · LATP ref 7(Rettenwander 2016) · LAGP ref 8(Kang 2015) | ⚠ **LPSC 의 구조 출처가 자기들 preprint 다** — 외부에서 독립 재현하려면 그 preprint 를 봐야 한다 |
| **전하** | **전부 charge-neutral**, *"taking the oxidation and reduction of the material itself as typically performed for electrode materials"*(ref 15) | ⭐ `[Schw20]` 과 동일한 방법론적 선택 |
| **Li 배열 탐색** | 조성마다 **랜덤 10,000 배치** → **정전기(Coulomb) 에너지 최소화**로 선별 → **최저 10개만 DFT 완화** | ⚠ **`[Schw20]` 은 상위 *20* 개였다 — 이 논문은 10 으로 줄였다.** 정전기 사전선별이 DFT 순위를 보존한다는 검증은 **여전히 0건** |
| **Li 삽입 자리** | Wyckoff 자리를 따로 평가 (`Table S1` 의 "Inserted Li pos."): LPSC **48h** · LPS 4c,4a,8d · LGPS 1d,2d,4d,8e,16h · LLZO 8a,16f,32g · LATP 6a,6b,18e 등 | ⭐ **대칭 자리를 열거해 평가한 것은 `[Schw20]` 보다 나아진 점** |
| **참조 에너지** | *"Structures and formation energies used as references are obtained from the **Materials Project**"*(ref 16) | 🔴 **판본·스냅샷 날짜·보정 스킴(MP2020 여부) 전부 미기재** ⇒ **우리 MP2026 과의 드리프트를 정량할 수 없다** (§7-3) |
| **무질서 처리** | ⛔ **한 줄도 없다.** SQS·enumeration·앙상블·배열 민감도 **전부 0건** | 🔴 `[Schw20]` 은 최소한 *"S/Cl 배열을 하나로 고정했고 전압은 영향받지 않았다"* 는 **단언이라도** 했다. 이 편은 **그 문장조차 없다** |
| **DFT+U** | **없음** — LLTO(Ti)·LATP(Ti)·LAGP(Ge)·LLZO(Zr) 에도 없다 | 🔴 **Ti³⁺/Ti⁴⁺ 를 다루면서 U 를 안 쓴다.** LLTO·LATP 의 전 논지가 **Ti 환원**인데 국재화 처리가 없다 (§10-3) |
| **스핀** | **언급 없음** | ⚠ Ti³⁺(d¹)·산화된 S 라디칼 모두 스핀 문제다. 우리 보고량 규율(`estimand_card` §2)의 **"admissible state 가 여럿" 위험신호** 그 자체 |
| **온도/엔트로피** | **0 K**, 포논·진동엔트로피 **0건**, 압력 보정 **0건** (ref 22 를 인용만) | 우리와 동일 |
| **전압식** | **Aydinol 평균 인터칼레이션 전압** (ref 15) — 식은 **본문에 적혀 있지 않다** | ⚠ `[Schw20]` 은 식 (3) 으로 인쇄했다. 이 편은 **식 없음** |
| **AIMD** | `Table S2`–`S13` 의 σ 용. *"the mean squared displacement of Li is calculated using an ab-initio molecular dynamics simulation at the temperature specified"*, 해석은 **de Klerk 2018**(SI ref 9 = *ACS Appl. Energy Mater.* **1**, 3230) | 🔴 **온도만 있다**: 궤적길이·dt·열욕·시드·**MSD 적합창**·오차막대 **전부 0건**. 그리고 **온도가 계마다 다르다**(600 K vs 1000 K) ⇒ 계 간 σ 비교가 성립하지 않는다. ⭐ 단 **해석 원전이 우리 MSD 창 규약의 계보(de Klerk 2018 = `papers/deklerk2018_diffusion_analysis_md_beta_li3ps4.md`)와 같다** |
| **밴드갭** | *"determined from the **density of states** calculated by a DFT calculation with an increased k-point mesh"* | 🔴 **우리 규율이 금지한 DOS-threshold 판독**이다(CLAUDE.md: ~0.3 eV 과소). ⇒ 절대 비교 금지 |
| **NEB / 전이상태 / 핵생성 장벽** | ⛔ **0건** | 🔴 논문의 중심 가정이 *"direct decomposition is kinetically hindered"* 인데 **장벽을 안 쟀다** (§10-1) |
| **탄성·포논·COHP·Bader·ELF·BVSE** | ⛔ **전부 0건** | §C 축 값 0 |
| **자체 실험** | ⛔ **0건** | 전 대조가 문헌 소환값 |
| **재현성** | 리포지터리·입력파일·구조파일 **0개**, Data availability 절 **없음** | 🔴 `[Schw20]`(요청제)보다도 **후퇴**했다 |

---

## 9. Figure set ★

> **크로핑 29장 = 그림 14장(본문 3 + SI 11) + 표 15장.** 이 중 **그림 8장 실독**. 표 15장(`tab_*.png`)은 **PDF 텍스트로** 읽었다(그게 정확하다).
> **실독**: `Fig. 1` · `Fig. 2` · `Fig. 3` · `S2` · `S7` · `S8` · `S9` · `S11`.
> **미열람 6장**: `S1`(= `S11` 의 흑색 ✕ 없는 판) · `S3`(LBH) · `S4`(LYB) · `S5`(LOC) · `S6`(LIPON) · `S10`(LATP Ti–P RDF). **이유**: 전부 **우리 물질계 밖**(붕수소화물·할라이드·반페로브스카이트·LIPON·NASICON)이고, 우리 축(이온전도·산화안정·기계·전자구조) 판정에 들어오지 않는다.

| Fig | 내용 | 우리 활용 |
|---|---|---|
| **1** | ✅**실독** 12종 × (decomposition vs intrinsic) 가로막대, x = 0–4.5 V | 🔴 **이 digest 의 표지 그림.** LPSC 연노랑 ≈1.11–2.19 / 진노랑 ≈1.72–2.01 (표와 일치). ⚠ **진한 띠는 두 창의 *교집합*이다** — LLTO·LATP 에서 범례가 성립하지 않는다 |
| **2a** | ✅**실독** LATP hull (x 0–3.67) | **볼록 사발 = 고용체**. 정점 9개가 촘촘하고 ✕ 구름이 hull 바로 위. 🔎 **pristine x=1.5 가 hull 최저점이 아니다**(최저 `figure-read ≈` x 1.67–1.9) |
| **2b** | ✅**실독** LATP x = 0 / 1.5 / 3 완화 구조 | **능면체 골격이 세 조성 모두 유지** — *"구조 안정 범위 > 전기화학 창"* 주장의 시각 근거 |
| **2c** | ✅**실독** LGPS hull (x 0–22) | 🔑 **V자 = 상분리.** 꼭짓점이 **pristine x=10** 에 정확히 있고 **x 4–10, 10–18 이 직선** ⇒ 두 상 평탄. 우리 아지로다이트도 같은 부류(`[Schw20]` `Fig. 2a`) |
| **2d** | ✅**실독** LGPS x = 4 / 10 / 22 구조 | **x=4 상자가 눈에 띄게 전단**(각도 변화) · S–S 가시 · x=22 는 `PS₄`/`GeS₄` 파괴. 🔎 **본문은 x=18 이라 쓰는데 그림은 x=22** (§10-5) |
| **3a** | ✅**실독** 복합전극 모식도 + "Interfaces" 육각 타일 | ⭐ **전해질‖활물질·전해질‖도전재 경계만 빨간 선** = *"전위를 느끼는 SE 는 계면 근방뿐"*. 우리 §H(계면 국소성)에 쓸 도해 |
| **3b,c** | ✅**실독** 상분리 이중우물 vs 고용체 단조하강 (Gibbs vs x) | 🔑 **이 논문의 "왜".** `Fig. 3b` 에 **점선 높은 봉우리 = Nucleation Barrier**, 실선은 낮은 봉우리. 🔴 **세로축 눈금 없음 · eV 0개** ⇒ ⛔ *"장벽을 계산했다"* 로 인용 금지. ⭐ **`[Dutra25Rev]` `Fig. 5c` 의 원전 후보** |
| **S1** | ⛔**미열람** `Li_xPS₄` hull | `S11` 과 같은 계 (흑색 ✕ 없는 판으로 추정) |
| **S2** | ✅**실독** 아지로다이트 hull, 정점 **0,1,2,4,6,11,12** | 🔴 **캡션은 `Li_xPS₅Cl` 인데 축 라벨은 `Li_xPS₅Br`.** x=11 정점은 `Table S4`(Cl)와 정합하므로 **축 라벨 오류 쪽이 유력**. ⇒ **`[Schw20]` `Fig. 2a` 와 정점 집합 동일** |
| **S3–S6** | ⛔**미열람** LBH·LYB·LOC·LIPON hull | 우리 물질계 밖 |
| **S7** | ✅**실독** `Li_xLa₀.₅₆TiO₃` hull (x 0–0.44, y −0.25…0.05 eV) | 🔴 **캡션이 `Li_xPO₂N`(S6 복붙) 인데 실제 축은 LLTO** — 실독으로만 잡힌다. 정점 0 / 0.062 / 0.187 / 0.281 / 0.312 / 0.406 / 0.437 (`figure-read ≈`). **에너지 폭이 0.2 eV 로 다른 계보다 한 자릿수 작다** |
| **S8** | ✅**실독** 계산 경로 흐름도 | 🔑 **정의의 정본.** 좌 = 분해산물 상도 → decomposition window / 우 = (탈)리튬화 hull → intrinsic window → **볼록 = 고용체 / V자 = 상분리**, 상분리만 "Metastable phase" 로 분해산물과 이어진다. 🔴 **"장벽" 상자 없음** |
| **S9** | ✅**실독** LGPS S–S RDF (x = 4 / 10 / 18) | 🔑 **x=4 만 r ≈ 2.0 Å 에 새 봉우리**(`figure-read ≈` 최대봉의 0.2 배), x=10·18 은 그 자리 **0** ⇒ S²⁻ 산화의 구조 지문. 세로축 **눈금 없음(a.u.)** |
| **S10** | ⛔**미열람** LATP Ti–P RDF | 캡션: "minor structural changes" = 고용체 근거 |
| **S11** | ✅**실독** `Li_xPS₄` hull + 분해산물 흑색 ✕ 2개 | 🔑🔑 **방법을 그림 하나로 보여 주는 유일한 자리.** `P₂S₅+S` at x=0 ≈−1.65 / `P+Li₂S` at x=8 ≈−6.4 (`figure-read ≈`). **우리 산수로 기울기를 재면 `Table 2` 가 재현된다**(§5b). ⚠ 캡션 번호가 **"Figure 11"** 로 인쇄됨 |
| **Table 1** | (PDF 텍스트) redox 원소 + 이론용량 | **우리 산수로 Li 수 환산 → 11/12 행이 정수·반정수.** LPSC 환원 8.00 Li = 우리 0 V 단계와 일치. ⚠ **LPS 산화 96.23 은 LAGP 값과 동일 = 오류 후보** |
| **Table 2** | (PDF 텍스트) **두 창 전수** | 🔴🔴 **감사 ①의 정본.** LPSC **1.72–2.01 / 1.11–2.19**. ⚠ 머리글 "ox/red" 순서가 값(red−ox)과 어긋남 |
| **Table S1** | (PDF 텍스트) 구조·k-점·공간군·삽입자리·슈퍼셀 | 🔴 **cutoff 열이 없다**(본문은 있다고 쓴다) · **LPSC·LLZO·LAGP 는 k-점·슈퍼셀이 "−"** |
| **Table S2–S13** | (PDF 텍스트) 준안정상 부피·밴드갭·σ | §3c. ⚠ **라벨 오류 4건**(`S4` 캡션 Br/Cl · `S6` 리튬화상 = pristine · `S10` 탈리튬상 = pristine · `S11` 행 순서) |

---

## 10. 비판 — 이 논문의 약한 곳 ★

**10-1. 🔴🔴 중심 가정(운동학)이 또 측정되지 않았다 — `[Schw20]` 보다 *더* 얇다.**
논문 전체가 *"direct decomposition is kinetically hindered"* 위에 서 있고, 토론은 **"핵생성 장벽" 이라는 말을 9번** 쓴다. 그런데 **장벽 값이 하나도 없다** — NEB 0회, 전이상태 0회, 핵생성 이론(고전 CNT 조차) 0회, eV 단위 0개. `Fig. 3b` 의 봉우리는 **눈금 없는 손그림**이고 `Fig. S8` 흐름도에는 **장벽 상자 자체가 없다**. `[Schw20]` 은 최소한 400 K·100 ps AIMD 의 RDF 라도 있었는데, 이 편의 AIMD 는 **σ 를 내기 위한 것**이지 분해 운동학이 아니다.
⛔ **인용 금지**: *"Schwietert 2021 이 간접 경로의 장벽이 낮음을 보였다"* — 안 보였다.

**10-2. 🔴 "복잡할수록 장벽이 크다" 가설에 지표가 없다.**
논지의 두 번째 기둥이 *"a larger number of elements ... raises the nucleation barrier"* 인데, **원소 개수 말고 정량 지표가 없다**. 반례를 저자 스스로 든다 — LYB(4원소)가 실패하고 LPSB(4원소)가 성공한다면 **원소 수는 변수가 아니다**. 실제 구분선은 *"저화학량론 원소(Br, P)를 분리해 내기 어렵다"* 는 **사후 서술**이다.

**10-3. 🔴 Ti·Zr·Ge 를 다루면서 DFT+U 가 없다.**
LLTO·LATP 의 결론은 통째로 **Ti⁴⁺ → Ti³⁺ 환원**에 걸려 있고, 그것이 *"intrinsic 이 더 좁다"* 는 이 논문의 **가장 새로운 주장**이다. 그런데 **U 도 스핀 처리도 보고되지 않았다**. 순수 GGA 는 `d¹` 전자를 **비국재화**시켜 환원전압을 계통적으로 어긋나게 한다. ⇒ **LLTO·LATP 의 0.3–0.6 V 급 차이가 U 선택 안에서 사라지지 않는다는 보장이 없다.** 우리 규율로 말하면 **"기준과 대상이 같은 제약인가" 가 확인되지 않았다.**

**10-4. ⚠ "excellent agreement with experiment" 의 실제 크기.**
초록은 *"exhibiting excellent agreement with experimentally observed electrochemical stability"* 라고 쓴다. 실제로 세어 보면:
- 정량 대조가 있는 계: **LPS · LGPS · LPSB · LBH · LIPON · LLZO · LATP(삽입 개시) = 7** (12종 중)
- **대조 자체가 없는 계**: **LOC**(*"Accurate oxidation potentials are not reported"*)
- **intrinsic 이 실패한 계**: **LYB**(Li 금속에 환원됨 — 저자 자인)
- **LATP·LLTO 는 "삽입이 일어난다" 는 정성 확인**이지 창 전압의 대조가 아니다
- 그리고 **전 대조가 문헌 소환값**이고 **오차·측정법(CV? GITT? dC/dV?)이 표에 없다**
⇒ ⛔ *"12종에서 실험과 잘 맞았다"* 로 옮기면 안 된다. 정확히는 **"7종에서 한 자리 숫자 수준으로 비슷하고, 1종은 틀리며, 1종은 대조가 없다"**.

**10-5. 🔴 intrinsic 창의 값이 *셀 크기의 함수*라고 저자가 직접 쓴다.**
> *"it should be noticed that the **supercell size determines the Li-composition step** in the convex hull. **The intrinsic window limits in Figure 1 and Table 2 are thus artificially defined by the smallest composition step of the supercell considered.**"*

즉 `Table 2` 의 intrinsic 값은 **수렴된 물리량이 아니라 셀 선택의 산물**이다. 그런데 **수렴시험 0건**이고, `Table S1` 은 **LPSC·LLZO·LAGP 의 셀 크기를 아예 안 적는다**. ⇒ ⛔ **층② 값을 소수 둘째 자리로 인용하면 안 된다.**
같은 절에 **내부 불일치**도 있다 — 본문은 LATP 의 *"oxidation voltage toward the first point on the convex hull is **3.37 V**"* 라 쓰는데 `Table 2` 의 intrinsic 산화는 **3.77 V** 다. 어느 쪽이 "창" 인지 설명이 없다.
`Fig. 2d` 도 같은 종류다 — 본문 **x=18**, 그림·캡션 **x=22**.

**10-6. ⚠ 방향(산화/환원) 라벨이 논문 안에서 뒤집힌다 — 우리 도구 버그와 같은 종류의 실수.**
- `Table 2` 머리글은 **"decomposition ox/red (V)"** 인데 값은 **낮은 쪽이 환원**이다(모든 본문 서술·`Fig. 1` 실독과 정합) ⇒ **머리글 순서가 값과 반대**.
- 본문 p.1491: *"Garnet LLZO is predicted to have an **oxidation and reduction** potential of **0.05 and 2.68 V** ... respectively"* ⇒ **0.05 V 를 산화, 2.68 V 를 환원이라 불렀다. 뒤바뀐 것이다** (바로 다음 문단이 *"stable against Li metal and ... oxidation potential of 3.6 V"* 라며 스스로 반대로 쓴다).
- 그 밖: 본문 *"reduction of Ge⁴⁺ and **P³⁺**"*(앞 문장은 P⁵⁺) · `Li₃YB₆`(= `Li₃YBr₆`) · SI 캡션 `Li_xYBr₄`·`Li_xOCl₄` · `Figure S7` 캡션이 `S6` 복붙 · `Figure 11`(= `S11`) · `Table S4` 캡션 Br/Cl · `Table S6`·`S10` 의 (탈)리튬화 조성이 pristine 과 동일 · `Table S11` 행 순서.
⇒ 🔑 **우리에게 주는 교훈은 "따라 하면 된다" 가 아니라 그 반대다**: **이 논문도 방향을 사람이 손으로 적었고 그래서 틀렸다.** 기계가 읽을 수 있는 방향 표지는 **부호 있는 Li 교환량** 하나뿐이다 (§12-4).

**10-7. 🔴 무질서 처리가 한 줄도 없다.**
아지로다이트 두 종(LPSC·LPSB)을 다루면서 **S/Cl(Br) 자리무질서를 어떻게 처리했는지 안 적는다.** `[Schw20]` 은 *"배열 하나로 고정했다"* 는 **단언이라도** 했다. 무질서가 형성에너지를 수십 meV/atom 움직인다는 것은 **저자들 자신의 ref 2(de Klerk 2016)** 가 보인 바다.

**10-8. ⚠ 참조 상도의 판본이 없다.**
*"obtained from the Materials Project"* 한 줄뿐. 스냅샷 날짜·엔트리 id·보정 스킴 0개 ⇒ **누구도 이 decomposition window 를 재현 검증할 수 없다.** 우리 감사(§7-3)가 **0.246 V 중 얼마가 판본 드리프트인지 확정 못 하는 이유가 바로 이것**이다.

**10-9. ⚠ AIMD σ 가 계 간 비교에 못 쓰인다.**
온도가 **600 K(LPSB·LPSC·LGPS)와 1000 K(나머지 9종)** 로 갈리는데 표 어디에도 *"계 간 비교 금지"* 단서가 없다. 궤적길이·시드·MSD 창 0건. ⇒ ⛔ **이 σ 표에서 계 간 순위를 읽으면 안 된다.** (계 *안*의 pristine ↔ (탈)리튬화 비교는 같은 온도라 성립한다.)

**10-10. ⚠ 서지 오기 2건.** ref 13 이 PBE(PRL 77, 3865)가 아니라 *Perdew–Burke–**Wang**, PRB 54, 16533* (`[Schw20]` 과 같은 실수) · ref 14 가 PAW 논문이 아니라 *Kresse & Hafner 1993*.

**10-11. ⚠ 자기 값의 변경을 알리지 않는다.** LPSC intrinsic 이 `[Schw20]` 의 **2.24 / 1.08** 에서 이 편의 **2.19 / 1.11** 로 바뀌었는데 **본문은 *"already been shown ... agrees very well with experiments⁷"*** 라고만 쓰고 **값이 바뀐 것을 언급하지 않는다**. ⇒ 층② 값의 재현성이 **≈0.05 V** 라는 정보가 독자에게 전달되지 않는다.

---

## 11. 우리 원장 매핑 (요약표)

| 우리 원장 | 이 논문이 하는 일 | 조치 |
|---|---|---|
| `our_dft_baseline.md` L20 *"환원 한계 1.242 V"* | 🔴🔴 **라벨 오류를 드러낸다** — 저들 정의로는 **1.717 V** | **`HZ-esw-reduction-limit-label` 제안** (§7-5·§7-8) |
| `our_dft_baseline.md` L20 *"OCV 1.717 V"* | ✅ **이것이 환원 한계다** (저들 1.72 와 0.003 V) | 라벨 교체 제안 |
| `our_dft_baseline.md` L19 산화 onset **2.256 V** | ⚠ 저들 **2.01 V** — **우리가 0.246 V 높다** | §B① 에 **두 번째 독립 대조점**으로 행 신설 |
| `esw_lis4excluded.json` `excluded_formula` 3상 | 🔴 배제가 **onset 을 위로 민다**(LiS₄ 하나로 0.116 V) | 재실행 2판(포함/배제) 제안 |
| `tools/oxidation/esw_cascade_batch.py:420,435` | 🔴 `red = max(V \| evo>0)` ⇒ **cascade 전수 `window_V` 가 계통적으로 넓다** | **정정 전 `window_V` 인용 금지** |
| `kb/open_items.md` *"Zhu15 3.4× 감사"* | **3.4× → 1.86×**, 원인 66 % / 34 % 분해 | 갱신 제안 |
| `papers/schwietert2020_…md` §7-3 환원 델타 **−0.162 V** | 🔴 **−0.607 V 로 정정** (그러면 저들 델타 −0.61 과 일치) | 그 digest 정정 제안 |
| `papers/schwietert2020_…md` §9 `Fig. 2b` figure-read 1.70/2.01 | ✅ **인쇄값 1.72/2.01 로 확인됨** | 불확실 표기 해제 |
| `comparison_vs_ours.md` 1021행 `[Dutra25Rev]` ref 218 `Fig. 5c` | ⚠ **이 논문에 `Fig. 5` 가 없다**(본문 그림 3장) — 리뷰 자신의 그림일 것 | 귀속 재확인 제안 |
| §H *"층 ② 없음 — 상한이 없다"* | 층② 값 **1.11–2.19 V** 가 하나 더 생겼다(`[Schw20]` 1.08–2.24 와 0.03–0.05 V 차) | **층② 재현성 ≈0.05 V** 를 §H 에 부기 |
| §D 밴드갭 | `Li₆PS₅Cl` **1.984 eV**(DOS 판독) | ⛔ 절대 비교 금지, "wide-gap" 까지 |
| §A 이온전도 | (탈)리튬화가 σ 를 **−54 % / −38 %** | ⛔ 절대값 금지, **부호만** |
| `db/governance/decisions.json` | *"환원 한계"* 의 **보고량 정의가 원장에 없다** | `estimand_card` 신규 사유 |

---

## 12. 적용 인사이트 ★

1. **🔴 감사 ①은 "우리가 이겼다" 가 아니라 "우리가 한 변을 잘못 읽었다" 로 닫힌다.** 3.4× 중 **66 %가 우리 라벨**이다. 이 한 줄이 이 digest 의 실질 산출물이고, **우리에게 불리한 방향**이다.
2. **남은 격차는 한 변뿐이다 — 산화 0.246 V.** 그 중 **0.116 V 는 우리 자신의 상 배제**로 이미 설명되고(`LiS₄` 포함 시 2.14 V), 나머지 **≈0.13 V** 는 MP 판본 후보다. ⇒ **감사가 "원인 미상 3.4×" 에서 "원인 후보가 둘뿐인 0.13 V" 로 줄었다.**
3. **우리 "worst-case 하한" 프레이밍은 살아남되, 하한의 값이 우리 것이 아니다.** 이 논문이 활자로 *"the direct decomposition stability window is a lower limit"* 를 준다 — **인용할 때 우리 2.256 이 아니라 저들 2.01 이 그 하한이라는 것**을 같이 적어야 정직하다.
4. **⭐ 우리 도구 수정의 지침 (임무 ③의 답)** — 이 논문은 **따라 할 본보기가 아니라 반례**다. 방향을 사람이 손으로 적어서 **`Table 2` 머리글과 LLZO 문장이 뒤집혔다**. 기계가 읽을 수 있는 유일한 방향 표지는 **부호 있는 Li 교환량**이고, 이 논문에서 그것에 해당하는 것은 **`Table 1` 의 산화/환원 용량을 각각 다른 열에 둔 것**뿐이다.
   ⇒ **우리 `tools/oxidation/*.py` 에 넣을 것**: ① `evolution`(부호 있는 Li 수)을 **반드시 기록** ② 분기 라벨(`oxidation`/`reduction`)을 **`evolution` 의 부호에서 유도**하고 손으로 적지 않는다 ③ 반응식과 전압을 **`min |ΔV|` 로 짝짓지 않는다**(`esw_cascade_batch.py:433` 의 `rxn_at()`) — 행 안에서 이미 짝지어진 쌍만 쓴다 ④ **용량(mAh/g)을 같이 출력**하면 사람이 부호를 눈으로 검산할 수 있다(이 논문 `Table 1` 의 유일한 장점).
   ⇒ 이것이 `HZ-anode-b2o3-reaction-direction` 과 **같은 뿌리**다: 행의 전압은 그 행 조성의 **Li-rich 쪽 평탄**이고, 행의 반응식은 **그 조성 자체의 평형**이라 **둘이 서로 다른 것을 가리킨다**.
5. **층② 값의 재현성이 ≈0.05 V 라는 것을 이제 안다** (`[Schw20]` 2.24/1.08 ↔ 이 편 2.19/1.11, 같은 저자·같은 방법·1년 차). 우리가 층② 를 계산하게 되면 **0.05 V 이내를 "일치" 라고 부를 근거**가 생긴다.
6. **CV 반박 문장을 확보했다.** *"CV ... performed without conductive additive ... thus **unable to capture the intrinsic electrochemical window**"* ⇒ `[Du22LMR]`·`[Zuo]` 의 CV onset 을 우리 창과 나란히 놓을 때 **반드시 붙일 단서**.
7. **hull 모양이 예측 대상을 가른다는 규칙은 우리 cascade 에 바로 이식 가능하다.** V자면 상분리(간접 경로 있음) / 볼록이면 고용체(분해전압이 끝을 정함). **우리는 이미 조성별 hull 을 만든다** — 모양 판정 한 줄이면 각 후보가 어느 부류인지 라벨할 수 있다. ⚠ 단 **셀 크기 의존(§10-5)이 그대로 따라온다**.
8. **⛔ 쓰지 않을 것**: 이 논문의 σ 표로 계 간 순위 · 밴드갭 절대값 · LLTO/LATP 결론(U 없음) · *"12종에서 실험과 일치"*.

---

## 13. 인용 가능 문장 (영문 초안)

> **① 두 창의 구분 (안전)** — "Schwietert et al. distinguish two computed stability windows for solid electrolytes: the **decomposition window**, obtained from the Li grand-potential phase diagram of the most favourable decomposition products, and the **intrinsic window**, obtained from the average (de)lithiation potentials of the electrolyte structure itself [Schwietert 2021]."

> **② 아지로다이트 값 (정확)** — "For `Li₆PS₅Cl` the decomposition window is **1.72–2.01 V** vs Li/Li⁺ and the intrinsic window **1.11–2.19 V**; the corresponding values for `Li₆PS₅Br` are **1.72–2.01 V** and **1.09–2.23 V** [Schwietert 2021]."

> **③ 우리 위치 (필수 동반 문장 — 정정판)** — "Our grand-potential window for `Li₆PS₅Cl` is bounded by the highest potential at which no lithium is exchanged (**1.717 V**) and the onset of delithiation (**2.256 V**); the reduction bound coincides with the **1.72 V** reported by Schwietert et al. and by Zhu et al., while our oxidation bound is **0.25 V higher than their 2.01 V**, consistent with the phases excluded from our phase set and with Materials-Project vintage drift."

> **④ 하한 프레이밍 (저자 활자)** — "For compositionally complex electrolytes the direct-decomposition window is expected to be a **lower limit**, with the practical redox activity dictated by intrinsic (de)lithiation; for simple compositions such as `Li₃YBr₆` the decomposition window instead has the better predictive value [Schwietert 2021]."

> **⑤ 상분리 vs 고용체 (새 기여)** — "Whether decomposition proceeds through a metastable intermediate is set by the shape of the (de)lithiation convex hull: a **V-shaped hull implies phase separation** and an accessible intermediate (e.g. `Li₁₀GeP₂S₁₂`), whereas a **convex hull implies solid-solution behaviour** with no intermediate, so that the reaction terminates at the decomposition potential (e.g. `Li₁.₅Al₀.₅Ti₁.₅(PO₄)₃`) [Schwietert 2021]."

> **⑥ CV 단서 (방법 규율)** — "Cyclic voltammetry on sulfide electrolytes without a conductive additive cannot capture the intrinsic window and overestimates the stability range [Schwietert 2021]."

> **⑦ 한정 (필수)** — "The intrinsic window limits are **artificially defined by the smallest Li-composition step of the supercell used**, as the authors state; they should not be quoted to better than ~0.1 V."

---

## 14. 주의 / 한계 (인용 규율)

1. ⛔ **"이 논문이 간접 경로의 장벽이 낮음을 계산했다" 고 쓰지 않는다** — 장벽 수치 0건 (§10-1).
2. ⛔ **intrinsic 값을 소수 둘째 자리로 인용하지 않는다** — 저자 스스로 *"artificially defined by the smallest composition step of the supercell"* 라 쓴다 (§10-5).
3. ⛔ **`Table 2` 의 "ox/red" 머리글 순서를 그대로 옮기지 않는다** — 값은 **낮은 쪽이 환원**이다. LLZO 문단은 본문이 직접 뒤집어 쓴다 (§10-6).
4. ⛔ **`Table 1` 의 LPS 산화용량 96.23 mAh/g 을 쓰지 않는다** — LAGP 행과 같은 값이고, 3 Li 완전탈리튬이면 ≈447 mAh/g 이어야 한다(우리 산수).
5. ⛔ **`Table S2`–`S13` 의 σ 로 계 간 순위를 읽지 않는다** — 온도가 600 K 과 1000 K 로 갈린다 (§10-9).
6. ⛔ **밴드갭 절대 비교 금지** — 저들 값은 **DOS 판독**이고 우리 규율이 금지한 방법이다. "wide-gap" 까지.
7. ⛔ **LLTO·LATP 의 결론(intrinsic 이 더 좁다)을 우리 도판에 옮기지 않는다** — **DFT+U 없이 Ti 환원을 다뤘다** (§10-3).
8. ⛔ **"12종에서 실험과 훌륭히 일치" 로 옮기지 않는다** — 정량 대조 7종, 실패 1종(LYB), 대조 없음 1종(LOC) (§10-4).
9. ⚠ **`figure-read ≈` 값**(hull 정점 좌표, `Fig. 1` 막대 가장자리, RDF 봉우리 비, `Fig. S11` 기울기)은 **그림에서 읽은 것**이다. `Table 1`·`Table 2`·`Table S*` 인쇄값과 구분한다.
10. ⚠ **"우리 산수"** 로 표시한 것(Li 수 환산, 격자 a, 부피·σ 변화율, `Fig. S11` 기울기 검산, 창 폭)은 **논문이 인쇄하지 않은 우리 유도값**이다.
11. ⚠ **전부 소환값**이다. VASP·PBE·U 0·무질서 처리 미기재·0 K·MP 판본 미기재의 값이다. 우리 QE·MP2026 숫자와 **같은 셀에 놓지 않는다**.
12. ⚠ **§7 의 "저들 정의로 다시 읽은 우리 값 1.717 V" 는 *우리 유도*다.** 근거 3개(§7-2)는 강하지만 **pymatgen 재실행 검증은 아직 안 됐다**. 재실행 전까지 **"1.717 V 가 우리 환원 한계" 를 원고에 인쇄하지 않는다.**

---

## 15. 기법 용어 미니사전

- **decomposition window (분해 창)**: SE 조성을 Li 저장소에 열어 μ_Li 를 훑으면서, **Li 교환 없이 분해평형이 유지되는 μ_Li 구간**. 우리 `esw_*.json` 이 내는 양이고 `[Zhu15]`·`[Rich16]` 의 표준. `[Xiao20Rev]` 4층의 **층①**.
- **intrinsic window (고유 창)**: SE 가 **자기 골격을 유지한 채** Li 를 넣고 빼는 평균전압으로 정한 창. 인터칼레이션 전극과 같은 계산. **층②**.
- **Li grand potential phase diagram**: Li 를 저장소와 교환할 수 있게 열어 놓고(`μ_Li` 를 독립변수로) 만든 상도. `μ_Li = μ⁰_Li − eφ` 로 전압과 이어진다.
- **average intercalation voltage (Aydinol 식)**: `V = −[E(Li_x₂) − E(Li_x₁) − (x₂−x₁)E(Li)]/(x₂−x₁)`. 두 조성 **사이의 평균**이지 순간전압이 아니다 — 그래서 **조성 간격(= 셀 크기)이 값을 바꾼다**.
- **formation energy hull (조성 hull)**: 두 끝단(여기서는 완전탈리튬·완전리튬화)을 0 으로 잡은 조성-에너지 평면의 아래쪽 볼록껍질. **기울기가 전압**이고, 정점 사이의 직선 구간이 **두 상 평탄**이다.
- **V자 hull ↔ 볼록 hull**: V자면 pristine 이 꼭짓점이라 양옆이 직선(두 상 평탄) ⇒ **상분리(1차 상전이)**. 볼록하면 정점이 촘촘해 전압이 연속 ⇒ **고용체**.
- **nucleation barrier (핵생성 장벽)**: 새 상이 생길 때 계면을 만드는 데 드는 에너지 문턱. 이 논문의 핵심 개념인데 **계산되지 않았다**.
- **topotactic 반응**: 호스트 골격의 위상이 유지된 채 게스트(Li)만 드나드는 반응.
- **RDF g(r)**: 기준 원자에서 거리 r 에 다른 원자가 있을 확률밀도. **새 봉우리 = 새 결합**(여기선 r≈2 Å 의 S–S), **봉우리 뭉개짐 = 무질서화**.
- **DOS-threshold 밴드갭 판독**: 상태밀도가 0 에서 떠나는 지점으로 갭을 읽는 방식. **스미어링·격자 해상도에 따라 계통적으로 좁게 나온다** — 우리 규율은 금지하고 fixed-occupation nscf 의 VBM/CBM 고유값만 인정한다.
- **theoretical capacity (mAh/g)**: `C = n_Li × 26801.5 / M`. **부호 있는 Li 수의 사람용 표현**이라, 이 논문에서 산화/환원 방향을 기계적으로 검산할 수 있는 유일한 양이다.

---

## 16. 📌 도구 보고 (`tools/litdb/extract_figures.py`)

**문제 없음 — 이번엔 깨끗했다.** `--pdf` 로 두 파일을 명시해 돌렸고 `figures.json` 의 `sources` 가 **정확히 그 둘**이다(`--audit-src` 에서 이 slug 는 걸리지 않았다). 본문 3장 + SI 11장 + 표 15장 = **29장 전부 잡혔고 누락·빈 크롭 0건**.

참고 기록 2건 (도구 탓 아님, **원문 탓**):
1. **SI 캡션 번호가 원문에서 틀려 있다** — 마지막 그림 캡션이 `Figure S11` 이 아니라 **"Figure 11"** 이라 도구가 `fig_S11` 로 정규화했다. **결과는 맞다**(파일명 `fig_S11.png`).
2. **SI 2쪽이 완전 백지**다(텍스트 0 · 이미지 0 · 벡터 0). 원문이 그렇다 — 도구가 건너뛴 것이 맞다.

<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md
     같은 축(ESW 조작적 정의)의 오늘자 형제 digest = papers/schwietert2021_intrinsic_vs_decomposition_window_sse.md
     2026-09-22 신규. 1저자 지정 읽기축 = **우리 `red = max(V | evolution > 0)` 버그의 세 번째 외부 눈금**.
     크로핑 17장(그림 10 + 표 7) 중 그림 7장 실독(§9 에 본 것/안 본 것 명시).
     ⛔ 이 digest 의 수치는 전부 **소환값**이고 **전부 Na 계**다. 우리 Li db 값과 같은 셀에 놓지 않는다. -->

# Interfacial Stability and Design Strategies for Halide Solid Electrolytes in High-Voltage All-Solid-State Sodium-Ion Batteries — Jang, Kwon, Jeon, Kim & Yu (*Small Methods* **10**, e02179 (2026))

> slug `jang2026_halide_se_interfacial_stability_highv_na` · DOI `10.1002/smtd.202502179` · type `MP 데이터 + pymatgen 후처리 전용 (자체 DFT 0건 · 자체 실험 0건) · grand-potential ESW + pseudo-binary 계면 + 고속스크리닝 + PCA/K-means` · PDF `litdb/inbox/13. Interfacial_stability_halide_SE_highV_Na_ASSB_MAIN.pdf` (본문 10 pp) + `litdb/inbox/13. Sup) Interfacial_stability_halide_SE_highV_Na_SI.pdf` (SI 16 pp · `Figure S1`–`S2` · `Table S1`–`S7`) · digested `2026-09-22` · status ✅ · 태그 **[외부·🔴🔴 `HZ-esw-reduction-limit-label` 의 *세 번째* 외부 눈금 · ⛔⛔ Na 계 + 할라이드 SE → 물성 4축 *수치* 진입 금지]**

> elements: Na, Cl, F, O, Zr, Ta, Al, Y, La, S, P, Sb, Sn, B, Si, Ca, Mg, Nb, Ti, Ni, Mn, Co, Fe, V, Li
> methods: DFT, ESW

> **저자**: **Myeongcho Jang**^(a,b) · **Eunji Kwon**^a · **Chelin Jeon**^a · **Sooyeon Kim**^(c,\*) (skim@mju.ac.kr) · **Seungho Yu**^(a,d,\*) (shyu@kist.re.kr)
> ^a **KIST** Energy Storage Research Center, 5 Hwarang-ro 14-gil, Seongbuk-gu, Seoul 02792 · ^b 고려대 기계공학부 · ^c **명지대 화학과**, Yongin · ^d **UST** KIST School, Division of Energy & Environment Technology
> 접수 **2025-11-01** · 수정 **2025-12-26** · 수락 **2026-01-04** · ***Small Methods* 10(3), e02179** · **CC BY-NC (오픈액세스)** · © 2026 The Author(s), Wiley-VCH
> 지원: KIST 기관고유 **2E33941 · 2E33943** · NRF(MSIT) **RS-2024-00404414 · RS-2024-00427700** · **KISTI 슈퍼컴 KSC-2025-CRE-0062**
> **데이터 공개**: *"available in the supplementary material"* — 즉 **SI PDF 표가 전부**다. 리포지터리·코드·구조파일·스크립트 **0개**. 12 800 종 스크리닝의 중간 목록도 **없다**(`Table S5` 의 289종 이름만 있고 수치 없음).
> PDF 워터마크: *"Downloaded … by **Hanyang University Library** … on [21/09/2026]"* — 1저자가 21일에 받은 판본이다.

> 🎤 **관련 발표: 해당 없음** — `grep -l "논문 에이전트 인입 대기열" litdb/talks/*.md` → `lee2026_skku_mlip_materials_design.md` 하나뿐이고 그 대기열 6건에 이 논문 없음. `litdb/talks/` 전체에 `Jang`·`halide SE`·`ASSSIB`·`Na2ZrCl6` 검색 **0건**. ⇒ **역링크 작업 없음.**

> 🔗 **형제 digest (중복 서술 대신 링크)**: 같은 날 같은 축으로 읽은 `papers/schwietert2021_intrinsic_vs_decomposition_window_sse.md`. 그쪽은 **Li 계 · 층①/층② 이분법 · 방향 표기가 논문 안에서 뒤집히는 반례**였고, 이 편은 **Na 계 · 층①만 · 방향 표기가 그림 축으로 박혀 있는 정례**다. **두 편이 정확히 대칭이라 같이 읽어야 값이 나온다.**

---

## 0. 이 digest 를 읽는 법 — 1저자 지정 읽기축

이 편을 여는 이유는 하나다:

> 🔴🔴 **오늘 우리 도구에서 계통 오류를 찾았다.** `tools/oxidation/constrained_esw.py:91–93` 과 `tools/oxidation/esw_cascade_batch.py:417–418` 이 똑같이 `red = max(V | evolution > 0)` 을 쓴다. **Li 교환이 0 인 행(진짜 안정 구간의 아래 가장자리)이 필터에서 빠져** 환원 한계가 항상 한 계단 아래로 잡히고, `window_V` 가 cascade 356 행 전부에서 넓게 나온다 (중앙 **+0.475 V**). 원장 `HZ-esw-reduction-limit-label` (**BLOCKED**).
> **이 논문이 ESW 를 계산한다면, 그 관례가 우리 버그의 *세 번째 외부 눈금*이 되는가?**

답을 먼저 적는다 (근거는 **§4** 와 **§7**, 이 digest 의 두 중심 절이다):

| 질문 | 답 |
|---|---|
| 조작적 정의가 **활자로** 있는가 | ✅ **있다. 본문 p.2 한 문장**: *"**Within the electrochemical stability window, the decomposition energy remains zero** but increases upon reaching the reduction and oxidation potentials."* ⇒ **창 = ΔE_D 가 0 인 구간, 그 두 끝이 환원·산화 전위** |
| grand potential 인가 pseudo-binary 인가 | ⭐ **둘 다 쓰는데 *섞지 않는다*.** SE 자신의 창 = **Na grand potential** (`Methods` p.8) · SE‖양극 계면 = **pseudo-binary** ΔE_D(A,B,x) (식 1–2). **우리 `esw_*.json` ↔ `interface_reactivity` 분리와 같은 구조** |
| 어느 상도·스냅샷인가 | 🔴 **Materials Project, 판본·스냅샷 날짜·보정스킴(MP2020 여부) 전부 미기재.** ref 30–32 = pymatgen(2013)·Ong(2008)·Jain(2013) — **`[Schw21]` 과 똑같은 공백** |
| Na 흡수/방출 **방향**을 표기하는가 | ✅✅ **한다. 그것도 손으로 적은 산문이 아니라 *그림의 축*으로.** `Fig. 2e–h`·`Fig. S1d–f` 의 y축이 **`Na uptake per f.u.`** 이고 범위가 **−1 … +5**, 양의 방향에 **"Sodiation"**, 음의 방향에 **"Desodiation"** 화살표가 붙어 있다 ⇒ **부호 있는 교환량이 그림에 박혀 있다** |
| 🔴 **그 그림이 우리 버그를 그대로 보여 주는가** | ✅✅✅ **보여 준다.** `Fig. 2e` (`Na₂ZrCl₆`) 의 계단은 `… → 2 → **1** → 0(1.69–3.75 V) → −1.35 …` 다. **`max(V | uptake > 0)` 을 적용하면 uptake=1 인 계단의 시작 1.57 V 가 잡히고, 진짜 가장자리 1.69 V 를 놓친다** |
| 그 관례로 읽은 값이 몇인가 | **7종 전수 = §3a.** 환원 **1.49–2.18 V** / 산화 **3.75–3.77 V**. 그리고 **동역학 연장창**(ΔE_D > −25 meV/atom) 산화 **3.92–4.18 V** |
| ⭐ 우리 도구 수정이 **재계산인가 이름 바꾸기인가** | **이름 바꾸기다.** 우리 `esw_lis4excluded.json` 에 이미 `ocv_V = 1.717` 이 있고 **그것이 저들 정의의 환원 전위**다. 우리 `reduction_V = 1.242` 는 저들 `Table S2` 의 *"phase equilibria at the reduction potential"* 칸(= 가장자리 **아래 계단**)에 해당한다 ⇒ **두 값이 이미 다 있고 라벨만 뒤바뀌어 있다** (§7-2) |
| Na 계라는 게 걸리는가 | **정의·관례·기하는 전이된다 (이온종 무관). 값은 전이 안 된다.** 갈라 놓은 것이 **§7-6** |
| 할라이드라는 게 걸리는가 | ⚠ **통설이 이 논문 안에서 반쯤 깨진다.** 산화 창은 확실히 넓지만(3.76 vs 2.05 V), **계면 반응성에서는 O3 양극 상대로 할라이드 7종 범위(−194.5 … −255.0) 안에 황화물 둘이 들어온다** (§7-7 · §10-4) |
| 우리에게 불리한 게 있나 | ⚠ **둘.** ① 우리 `esw_*.json` 에 **ΔE_D(V) 열이 없어** 이들의 `Fig. 2a` 형 프로파일도, 동역학 연장창도 **우리 데이터로는 못 그린다**(§7-8, §H 제안) ② 계면 축에서 **저들 ΔE_D,mutual 식이 우리 `use_hull_energy=True` 와 대수적으로 동일**한데, 저들은 **혼합비 x 를 전 구간 훑어 최댓값**을 잡고 우리도 그렇게 한다 — 즉 **우리가 더 나은 게 없다. 동급이다** (§7-7) |

---

## 1. 한 줄 요약

**"할라이드 고체전해질은 고전압 양극과 궁합이 좋다" 는 통념을 같은 팀이 자기 계산으로 깎아내린 편이다.** Na 할라이드 7종의 **내재 전기화학 창은 확실히 넓다**(1.49–2.18 → 3.75–3.77 V, 동역학 연장 시 산화 ~4.1 V; 황화물은 산화가 1.66–2.05 V 라 양극 작동구간에 아예 못 들어온다). 그런데 **양극과 맞대면 상호 분해 구동력이 P2 −140 · O3 −220 meV/atom** 로 **전혀 작지 않다**. 그래서 12 800 종 Na 화합물을 훑어 **계면 구동력을 −20 … −40 meV/atom 으로 끌어내리는 코팅 11종(엄격) / 25종(실용)** 을 뽑았고, 대표로 **`NaB₃O₅`** 를 쓰면 `Na₂ZrCl₆`‖O3 의 −213/−224 가 **−33/−34** 로 떨어진다. ⛔ **슬랩은 한 장도 안 만들었다 — 전부 벌크 열역학이다.**

---

## 2. 메타 / 동기 / 질문

**문제 상황 (서론 축자).** 황화물 SE 는 이온전도가 **1–10 mS cm⁻¹** 로 좋지만 *"generally suffer from chemical instability when in contact with high-voltage cathode materials"*(refs 6, 7). 산화물 SE 는 화학안정성은 좋지만 *"often require high-temperature sintering to achieve intimate interfacial contact"*(refs 8, 9). 그래서 할라이드(HSE)가 *"favorable combination of high ionic conductivity, mechanical deformability, and chemical stability"*(refs 10–12)로 부상했다.

**Na 할라이드의 계보 (저자가 세는 방식).** Li 할라이드(refs 13–16: Asano 2018 · Li 2024 · Yin 2023 *Nature* LaCl₃ · Kwak 2023 *Nat. Commun.*)에 이어 Na 판이 나왔다 — Zr 염화물(`Na₀.₇La₀.₇Zr₀.₃Cl₄`), Ta 염화물(`NaTaCl₆`), 옥시염화물(`NaAlCl₂.₅O₀.₇₅`·`NaTaOCl₄`), 전부 **~1 mS cm⁻¹**(refs 17–22). 그리고 **불소 치환**(`Na₀.₅ZrCl₄F₀.₅`, refs 23, 24)이 *"an effective strategy for further enhancing oxidative stability, thereby enabling the use of **uncoated** high voltage cathodes"* 로 보고돼 있다. ⭐ **이 마지막 문장이 이 논문이 반박하려는 대상**이다.

**이 논문의 질문 3개.**
1. Na HSE 7종의 **전기화학 창**은 실제로 얼마이고, 황화물 대비 얼마나 넓은가?
2. 창이 넓다는 것이 **양극과의 화학적 궁합**을 보장하는가? (답: **아니다**)
3. 보장 못 한다면 **어떤 코팅**이 그 구동력을 죽이는가? (12 800 종 스크리닝)

**⚠ 이 논문의 위상 (아주 중요).** **자체 DFT 0건, 자체 실험 0건**이다. `Methods` 첫 문장이 *"Crystal structures, formation energies, and convex-hull stabilities were **obtained from the Materials Project database**"* 이고, 두 번째 문단이 *"The calculations were conducted **using data from** the Materials Project database, which provides **pre-computed** first-principles thermodynamic information"* 이다. ⇒ **이 논문에서 저자들이 직접 한 계산은 pymatgen 후처리와 scikit-learn 군집화뿐**이다. 범함수·cutoff·k점·슈퍼셀·무질서 처리가 **논문에 하나도 없는 것이 오기가 아니라 구조**다 (§8). 인용할 때 반드시 붙여야 할 단서다.

**선행 계보 (저자들의 자기 인용).** ref 27 = **Chun, Shim & Yu**, *ACS AMI* 14, 1241 (2021) — Li **염화물** SE 계면 안정성 계산. ref 28 = **Chun, Gong, Kim, Shim & Yu**, *Appl. Surf. Sci.* 616, 156479 (2023) — **Na** 고에너지 ASSB 코팅 계산. ⇒ **교신저자 Yu 의 3부작 중 3편째**이고, 방법(ΔE_D,mutual + MP + 스크리닝)이 그대로 승계됐다. 방법 원전은 ref 25(**Xiao–Miara–Wang–Ceder**, *Joule* 3, 1252 (2019) = 우리 `[Xiao19Coat]` 계보) · ref 33(**Zhu–He–Mo** *JMCA* 4, 3253 (2016)) · ref 35(**Richards–Miara–Wang–Kim–Ceder**, *Chem. Mater.* 28, 266 (2016)) 이다.

---

## 3. 핵심 수치 총정리 ★

### 3a. `Table S2` — Na 할라이드 7종의 전기화학 창 전수 (이 논문의 중심 표)

| SE | 조성 | **환원 전위 (V)** | 환원 가장자리 **아래** 평형 | **산화 전위 (V)** | 산화 산물 | **폭 (우리 산수)** |
|---|---|---|---|---|---|---|
| Zr 염화물 | **`Na₂ZrCl₆`** | **1.69** | `ZrCl₃, NaCl` | **3.75** | `NaCl₃, ZrCl₄` | **2.06** |
| Zr 염화물 | `Na₀.₇La₀.₇Zr₀.₃Cl₄` | **1.68** | `ZrCl₃, LaCl₃, NaCl` | **3.76** | `NaCl₃, ZrCl₄, LaCl₃` | **2.08** |
| Zr 염화물 | `Na₀.₆₂₅Y₀.₂₅Zr₀.₇₅Cl₄.₃₇₅` | **1.69** | `ZrCl₃, Na₃YCl₆, NaCl` | **3.77** | `NaCl₃, ZrCl₄, YCl₃` | **2.08** |
| Ta 염화물 | `NaTaCl₆` | **2.18** ⚠ | `Ta₂Cl₅, NaCl` | **3.76** | `NaCl₃, TaCl₅` | **1.58** |
| 옥시염화물 | `NaAlCl₂.₅O₀.₇₅` | **1.49** | `NaCl, Al₂O₃, Al` | **3.76** | `NaAlCl₄, NaCl₃, Al₂O₃` | **2.27** |
| 옥시염화물 | `NaTaOCl₄` | **2.13** | `Ta₂Cl₅, NaCl, Ta₂O₅` | **3.76** | `TaCl₃O, NaCl₃` | **1.63** |
| **불소화** Zr 염화물 | **`Na₀.₅ZrCl₄F₀.₅`** | **1.69** | `ZrCl₃, NaCl, ZrF₄` | **3.76** | `ZrCl₄, NaCl₃, ZrF₄` | **2.07** |

> ⚠ **`NaTaCl₆` 의 환원 전위가 표마다 다르다**: `Table S2` **2.18 V**, `Table S3` **2.17 V**, 본문 *"near 2.18 V"*. **0.01 V 내부 불일치**(§10-6). 나머지 6종은 두 표가 일치한다.
> 🔑 **산화 전위 7종이 전부 3.75–3.77 V 안에 들어온다.** 저자의 설명이 명쾌하다 — *"their oxidative decomposition **consistently involves the formation of `NaCl₃`**"*. 즉 **산화 가장자리를 정하는 것은 중심금속이 아니라 Cl⁻ 다.**
> ⭐⭐ **이것이 우리 `comp1`/`modelc` 가 둘 다 2.256 V 인 것(= S²⁻-limited)과 *정확히 같은 구조*다** — 한 음이온이 창의 한 변을 독점한다. ⇒ **이온종·음이온종을 바꿔도 살아남는 규칙**이다 (§7-6).
> 🔑 **환원 전위는 중심금속이 정한다**: Zr 계 3종 = **1.68–1.69**(전부 `ZrCl₃` 형성) · Ta 계 2종 = **2.13–2.18** · Al 계 = **1.49**(가장 낮다 = 환원에 가장 강하다).
> 🔴 **불소 치환이 *열역학* 산화 전위를 3.75 → 3.76 = +0.01 V 밖에 못 올린다.** 본문이 자랑하는 *"3.92 → 4.18 V"* 는 **전부 동역학 연장창의 몫**이다 (§3c — 이 digest 에서 제일 날카로운 재구성).

### 3b. `Table S3` — 전 분해 사다리 전수 (ΔE_D 포함) ★★

> 각 행 = **(새 평형이 열리는 임계전위, 그 구간에서의 SE 의 ΔE_D, 그 구간의 평형상)**. **ΔE_D = 0.000 인 두 행이 창의 두 끝**이다.
> ⭐ **아래 볼드 행이 "Na 교환 0" 구간의 아래 가장자리**이고, 그 **바로 윗줄이 우리 버그가 잡는 행**이다.

**`Na₂ZrCl₆`** — 우리 버그의 교과서 사례
| V | ΔE_D (eV/atom) | 평형상 | 비고 |
|---|---|---|---|
| 0.00 | −0.614 | `Zr, NaCl` | 완전환원 |
| 1.04 | −0.153 | `ZrCl, NaCl` | |
| 1.24 | −0.086 | `ZrCl₂, NaCl` | |
| **1.57** | **−0.013** | `ZrCl₃, NaCl` | 🔴 **우리 `max(V\|evo>0)` 이 잡는 행** |
| **1.69** | **0.000** | **`Na₂ZrCl₆`** | ✅ **진짜 환원 전위** |
| **3.75** | **0.000** | `NaCl₃, ZrCl₄` | ✅ **산화 전위** |
| 4.78 | −0.152 | `NaCl₇, ZrCl₄` | |
| 5.68 | −0.324 | `ZrCl₄, Cl₂` | |

**나머지 6종 (환원 쪽 사다리만 — 산화 쪽은 전 계가 3.75/3.76/3.77 → 4.78 → 5.68 로 같은 꼴)**

| SE | 환원 사다리 (V / ΔE_D) | **가장자리** | **우리 버그가 잡을 값** | **어긋남 Δ (우리 산수)** |
|---|---|---|---|---|
| `Na₂ZrCl₆` | 0.00/−0.614 · 1.04/−0.153 · 1.24/−0.086 · **1.57/−0.013** | **1.69** | 1.57 | **0.12 V** |
| `Na₀.₇La₀.₇Zr₀.₃Cl₄` | 0.00/−0.436 · 0.40/−0.207 · 1.04/−0.072 · 1.24/−0.040 · **1.57/−0.006** | **1.68** | 1.57 | **0.11 V** |
| `Na₀.₆₂₅Y₀.₂₅Zr₀.₇₅Cl₄.₃₇₅` | 0.00/−0.761 · 0.52/−0.434 · 0.58/−0.400 · 1.04/−0.172 · 1.24/−0.097 · **1.57/−0.015** | **1.69** | 1.57 | **0.12 V** |
| `NaTaCl₆` | 0.00/−1.244 · **1.81/−0.115** | **2.17** | 1.81 | **0.36 V** |
| `NaAlCl₂.₅O₀.₇₅` | 0.00/−0.447 · 0.30/−0.338 · **0.39/−0.315** | **1.49** | 0.39 | 🔴 **1.10 V** |
| `NaTaOCl₄` | 0.00/−0.908 · 0.01/−0.900 · 0.95/−0.452 · 1.81/−0.072 · **1.86/−0.057** | **2.13** | 1.86 | **0.27 V** |
| `Na₀.₅ZrCl₄F₀.₅` | 0.00/−0.880 · 0.61/−0.473 · 1.04/−0.209 ×2 · 1.24/−0.118 · 1.53/−0.027 · **1.57/−0.018** | **1.69** | 1.57 | **0.12 V** |

> 🔴🔴 **7종 전수에서 어긋남 Δ = 0.11 … 1.10 V, 중앙 0.12 V, 평균 0.31 V** (우리 산수).
> ⭐ **우리 cascade 의 중앙 +0.475 V 는 이 범위 *안*이다** ⇒ **우리 버그의 크기가 이상한 게 아니라, "환원 사다리 한 계단" 의 자연스러운 크기**다. 사다리가 촘촘한 Zr 계는 0.12 V, 사다리가 성긴 Al 계는 1.10 V. **즉 이 버그는 계마다 다른 크기로 틀리므로 계 간 순위까지 흔든다** (§7-4).
> ⚠ **`Na₀.₅ZrCl₄F₀.₅` 의 1.04 V 행이 두 번 인쇄돼 있다** (`Na₂ZrF₆, NaCl, Zr` 와 `Na₂ZrF₆, ZrCl, NaCl`, 둘 다 −0.209). 동시 발생하는 두 평형이거나 인쇄 중복이다 — **구분이 불가능하다**(§10-6).

### 3c. ★★ 동역학 연장창 — **그들이 인쇄하지 않은 레시피를 우리가 복원했다**

본문은 두 가지만 준다: 문턱 *"decomposition energies remain relatively low (**< 25 meV/atom**) up to approximately 4.0 V"* 와 결과 7개.
**우리 산수**: `Table S3` 의 인접 두 행을 **선형보간**해 `ΔE_D = −0.025 eV/atom` 을 지나는 전압을 구한다.

| SE | 열역학 산화 | 다음 행 (V / ΔE_D) | **기울기 (eV/V, 우리 산수)** | **우리 보간값** | **논문 값** | 일치 |
|---|---|---|---|---|---|---|
| `Na₂ZrCl₆` | 3.75 | 4.78 / −0.152 | **−0.148** | **3.92** | **3.92** | ✅ 정확 |
| `Na₀.₇La₀.₇Zr₀.₃Cl₄` | 3.76 | 4.78 / −0.084 | −0.082 | **4.06** | **4.06** | ✅ 정확 |
| `Na₀.₆₂₅Y₀.₂₅Zr₀.₇₅Cl₄.₃₇₅` | 3.77 | 4.78 / −0.070 | −0.069 | **4.13** | 4.12 | ✅ 0.01 |
| `NaTaCl₆` | 3.76 | 4.78 / −0.085 | −0.083 | **4.06** | **4.06** | ✅ 정확 |
| `NaAlCl₂.₅O₀.₇₅` | 3.76 | 4.13 / −0.023 → 4.23 / −0.033 | −0.062 → −0.100 | **4.15** | **4.15** | ✅ 정확 |
| `NaTaOCl₄` | 3.76 | 4.78 / −0.097 | −0.095 | **4.02** | 4.03 | ✅ 0.01 |
| `Na₀.₅ZrCl₄F₀.₅` | 3.76 | 4.78 / −0.056 | **−0.055** | 4.22 | 4.18 | ⚠ 0.04 |

> ✅✅ **7종 중 6종이 ±0.01 V 안에서 재현된다** ⇒ **동역학 연장창의 조작적 정의가 검산됐다: `ΔE_D(V) = −25 meV/atom` 을 지나는 전압.** (`Na₀.₅ZrCl₄F₀.₅` 만 0.04 V 어긋나는데, `Table S3` 이 3.76–4.78 사이의 중간 꺾임을 안 실은 것으로 보인다 — 즉 **`Table S3` 이 모든 breakpoint 를 싣지는 않는다**.)
> 🔴🔴 **그리고 이 검산이 논문의 헤드라인 하나를 무너뜨린다.** 본문: *"**fluorination of `Na₂ZrCl₆` further enhances oxidation stability, increasing the potential from 3.92 to 4.18 V**"*. 그런데 **열역학 산화 전위는 3.75 → 3.76 = +0.01 V** 다. 실제로 바뀐 것은 **onset 이 아니라 onset 이후 ΔE_D 가 자라는 기울기**다 — **−0.148 → −0.055 eV/V, 2.7배 완만**(우리 산수). ⇒ **F 는 "언제 분해가 시작되나" 를 못 바꾸고 "얼마나 빨리 나빠지나" 를 바꾼다.**
> ⭐⭐⭐ **이것이 우리 §B 축 명명 규율의 외부 실증이다.** 우리 `comp1`↔`modelc` 도 **산화 onset 이 2.256 V 로 동일**하고(S²⁻-limited), Cl 은 onset 이 아니라 **분해 양·산물·계면**에 작용한다. **여기서는 Cl→F 가 정확히 같은 방식으로 행동한다.** 음이온을 바꿔도, 이온종을 Li→Na 로 바꿔도 **같은 구조**다 (§7-6).
> ⚠ **25 meV/atom 문턱에 근거 문장이 없다.** *"suggesting that oxidation **can be** kinetically suppressed"* 가 전부다. 장벽 계산 0건, 과전압 실측 대조 0건 (§10-1).
> ⚠ **연장창은 `Fig. 1` 에서 *양쪽* 점선상자로 그려지는데 본문은 산화 쪽 7개만 숫자로 준다.** 환원 쪽 연장값은 **논문 어디에도 없다** (우리가 `Table S3` 로 낼 수는 있으나 **논문 미보고**라 인용 불가).

### 3d. `Fig. 3` — SE‖양극 상호 분해 구동력 전수 (10 SE × 14 양극 = **140 셀**) ★★

> ⚠ **`Table S4` 에는 할라이드 7행(98 셀)만 있다. 황화물 3행(42 셀)은 `Fig. 3` 에만 있다.** 아래 황화물 값은 **그림의 인쇄 숫자를 읽은 것**이고, 할라이드 7행을 `Table S4` 텍스트와 **98/98 전부 대조해 일치를 확인**했으므로 판독 신뢰도는 높다.
> 단위 **meV/atom**, 음수 = 반응 구동력.

**계열별 평균 (우리 산수)**

| | Polyanionic (2종) | **P2 (6종)** | **O3 (6종)** |
|---|---|---|---|
| `Na₂ZrCl₆` | −76.5 | −132.8 | −213.2 |
| `Na₀.₇La₀.₇Zr₀.₃Cl₄` | −61.0 | −140.5 | −214.0 |
| `Na₀.₆₂₅Y₀.₂₅Zr₀.₇₅Cl₄.₃₇₅` | −84.0 | −140.0 | −227.5 |
| `NaTaCl₆` | −80.0 | **−164.3** | 🔴 **−255.0** |
| `NaAlCl₂.₅O₀.₇₅` | −87.0 | **−128.0** | **−194.5** |
| `NaTaOCl₄` | −90.0 | −140.0 | −223.2 |
| `Na₀.₅ZrCl₄F₀.₅` | −85.5 | −146.3 | −236.0 |
| **HSE 7종 평균** | **−80.6** | **−141.7** | **−223.3** |
| `Na₁₁Sn₂PS₁₂` | −70.0 | −189.3 | −209.3 |
| `Na₃SbS₄` | −74.0 | −188.0 | −200.5 |
| 🔴 `Na₃PS₄` | −73.5 | **−300.7** | **−352.2** |
| **황화물 3종 평균** | **−72.5** | **−226.0** | **−254.0** |
| **황화물 2종 평균 (`Na₃PS₄` 제외)** | **−72.0** | **−188.7** | **−204.9** |

> ✅ 위 평균들이 본문 서술(*"approximately −80 … −140 … −220 meV/atom"* / 황화물 *"−230 and −250"*)을 **소수 첫째 자리까지 재현한다** ⇒ 내 판독이 맞다.
> 🔴🔴 **논문이 말하지 않는 것 두 개** (우리 산수 · §10-4 의 근거):
> 1. **Polyanionic 양극 상대로는 황화물이 할라이드보다 *낫다*** (−72.5 vs −80.6). `Na₃PS₄`‖`Na₃V₂(PO₄)₃` = **−47** 로 **140 셀 전체의 최선값**이다.
> 2. **O3 양극 상대로 `Na₃SbS₄`(−200.5) 와 `Na₁₁Sn₂PS₁₂`(−209.3) 가 할라이드 7종 범위(−194.5 … −255.0) *안에* 들어온다.** 즉 *"할라이드가 황화물보다 계면이 낫다"* 는 **`Na₃PS₄` 한 계가 끌고 가는 서술**이다.
> 🔑 **`Na₃PS₄` 만 유별나다**: P2 −300.7 · O3 −352.2 로 나머지 둘의 **1.6–1.8배**. 최악 셀 = `Na₃PS₄`‖`NaNi₀.₅Fe₀.₅O₂` **−405**.
> 🔑 **양극 계열 서열은 전 SE 에서 동일**: Polyanionic ≪ P2 < O3. `NaNi₀.₅Fe₀.₅O₂` 가 14종 중 **거의 항상 최악**(할라이드 7종 중 6종에서 최악).
> 🔑 **분해산물의 문법** (`Table S4`, 우리 요약): 할라이드‖층상산화물은 **거의 항상 `NaCl` + 금속산화물(`ZrO₂`/`Ta₂O₅`/`Al₂O₃`) + `NaClO₄` 또는 `NaCl₃`** 가 나온다. **Cl⁻ 가 양극의 O 를 받아 `NaClO₄` 로 산화되는 경로가 할라이드 계면의 고유 채널**이다(황화물엔 없다). 할라이드‖polyanionic 은 **`NaZr₂(PO₄)₃`·`TaPO₅`·`LaPO₄`·`YPO₄`** 같은 **NASICON/인산염**이 나와 구동력이 작다 — ⭐ **그리고 그 `NaZr₂(PO₄)₃` 가 최종 코팅 추천 목록에 그대로 들어간다**(§3e). 즉 *"어차피 생길 상을 미리 깔아라"* 라는 자기정합적 결론이다.

### 3e. 코팅 스크리닝 — 깔때기와 결과

| 단계 | 기준 (활자) | 남은 수 |
|---|---|---|
| 출발 | MP 의 **Na 함유 화합물** | **12 800** |
| (i) | 원자번호 **> 86** 제외 · **Li/K/Rb/Cs** 함유 제외 · **band gap < 0.5 eV** 제외 | **7 995** |
| (ii) | **`E_hull = 0` 만** 잔류 (*"conservative definition"*, 저자 자인) | (미기재) |
| (iii) | **환원 전위 < 2.5 V** 이고 **산화 전위 > 3.5 V** | **289** |
| (iv-a) 엄격 | ΔE_D,mutual **평균 |·| < 50** 그리고 **최대 |·| < 60 meV/atom** | **11** |
| (iv-b) 실용 | 최대 |·| **< 110 meV/atom** + **원소 ≤ 4** + 산화물·폴리음이온만 + *"Na + 음이온만"* 인 것 제외 | **25** |

**엄격 11종** (`Table S6`, 환원/산화 전위 V): `NaAlH₂CO₅` 1.57/4.03 · `Na₆CdCl₈` 1.97/3.75 · `Na₂Ca(SO₄)₂` 1.63/4.16 · `Na₂Al₂Si₃(HO₃)₄` 1.16/3.69 · **`NaB₃O₅` 1.12/3.54** · `NaAlSi₃O₈` 0.73/3.79 · `NaB₅(H₂O₅)₂` 1.63/3.86 · `Na₂B₈O₁₃` 1.15/4.29 · `BaNa(B₃O₅)₃` 1.33/3.80 · `Na₆Mg(SO₄)₄` 2.20/4.11 · `Na₃B₆PO₁₃` 1.48/3.84

**실용 25종** (`Table S7`, 화학족별): **붕산염** `NaB₃O₅`·`Na₂B₈O₁₃`·`BaNa(B₃O₅)₃`·`Na₃B₆PO₁₃` · **인산염** `Na₃Sc₂(PO₄)₃`·`NaTiPO₅`·**`NaHf₂(PO₄)₃`**·**`NaZr₂(PO₄)₃`**·`NaScP₂O₇`·**`NaTi₂(PO₄)₃`**·`Na₄Mg₃P₄O₁₅`·`NaBePO₄`·`NaSn₂(PO₄)₃`·`Na₃Mg₂P₅O₁₆`·`NaNb₂PO₈` · **알루미노규산염** `NaAlSi₃O₈`·`NaAlSiO₄` · **황산염** `Na₂Ca(SO₄)₂`·`Na₆Mg(SO₄)₄` · **니오브/탄탈산염** `Na₂Ta₄O₁₁`·`NaNb₃O₈`·`NaNb₁₃O₃₃`·`NaTaO₃`·`NaNbO₃` · **기타** `NaBe₄SbO₇`

> ⭐⭐ **우리 코팅 축과 직접 겹치는 것**: **붕산염 계열**(`NaB₃O₅`·`Na₂B₈O₁₃`)이 최종 추천의 **얼굴**이다. 우리 `B₂O₃` 축(`db/properties/anode_interface_b2o3.json` · gap 1.9671 eV)과 **같은 화학족**이다. ⚠ 단 **Na 판이고 값은 못 옮긴다** — 옮길 수 있는 것은 *"붕산염이 SE‖양극 양쪽에 동시에 낮은 구동력을 주는 드문 족"* 이라는 **정성 구조**뿐이다.
> ⭐ **`NaZr₂(PO₄)₃`·`NaTi₂(PO₄)₃`·`NaHf₂(PO₄)₃` = NASICON 이 코팅으로 추천된다.** ⇒ *"전해질로 쓰던 것을 코팅으로 쓴다"* 는 구조. 우리 `LiNbO₃`·`Li₂ZrO₃` 코팅 축과 같은 논리.
> 🔴 **`Na₆CdCl₈` 이 엄격 11종에 들어 있다** — **Cd 는 독성**이고 논문은 실용 25종에서 조용히 뺐지만 **왜 뺐는지 안 적는다**(*"원소 ≤ 4"* 로도 `Na₆CdCl₈`(3원소)은 안 걸린다 — 실제로는 *"산화물·폴리음이온만"* 조건에 걸려 빠진 것이다). ⚠ 인용 시 11종을 그대로 옮기지 말 것.
> 🔴 **`NaAlH₂CO₅`·`Na₂Al₂Si₃(HO₃)₄`·`NaB₅(H₂O₅)₂` = 수화물/수산화물이 세 개**다. 전고체 셀 코팅으로 **H₂O 를 품은 상**을 추천하는 것은 물리적으로 곤란한데 논문은 언급하지 않는다(*"moisture tolerance … will be required"* 는 **HSE 쪽**에 대해서만 적는다).

**대표 코팅 효과 (`Fig. 8`, 본문 인쇄값)**

| 계면 | 코팅 전 | **`NaB₃O₅` 코팅 후 (양극쪽)** | HSE‖코팅 |
|---|---|---|---|
| `Na₂ZrCl₆` ‖ `Na₀.₆₇Mn₀.₆₅Co₀.₂Ni₀.₁₅O₂` | **−131** | **−35** | **−19** |
| `Na₂ZrCl₆` ‖ `NaNi₀.₃₃Fe₀.₃₃Mn₀.₃₃O₂` | **−213** | **−33** | **−19** |
| `Na₂ZrCl₆` ‖ `NaNi₀.₆₁Co₀.₁₂Mn₀.₂₇O₂` | **−224** | **−34** | **−19** |
| `NaTaOCl₄` ‖ `Na₀.₆₇Mn₀.₆₅Co₀.₂Ni₀.₁₅O₂` | **−137** | (본문 미표기, `Fig. 8d` figure-read ≈ **−34**) | **−24** |
| `NaTaOCl₄` ‖ `NaNi₀.₃₃Fe₀.₃₃Mn₀.₃₃O₂` | **−224** | (figure-read ≈ **−33**) | **−24** |
| `NaTaOCl₄` ‖ `NaNi₀.₆₁Co₀.₁₂Mn₀.₂₇O₂` | **−236** | (figure-read ≈ **−34**) | **−24** |

> 🔑 **코팅‖양극 값이 −33 … −35 로 양극 종류에 거의 무관**하다. 즉 **`NaB₃O₅` 가 양극의 산화력을 "평탄화" 한다**. 반면 코팅 없을 때는 −131 … −236 으로 1.8배 벌어진다.
> ⚠ **`NaB₃O₅` 의 산화 전위는 3.54 V** (`Table S6`) 로 **추천 25종 중 가장 낮다**. 즉 **4.4 V 급 P2 양극 작동창을 코팅 자신이 못 버틴다.** 논문은 이 모순을 언급하지 않는다(§10-5).

### 3f. `Table 1` — 7종 HSE 의 보고된 이온전도도 (전부 **문헌 소환값**, 자체 측정 0)

| 계열 | SE | σ (mS/cm) | 원전 |
|---|---|---|---|
| Zr 염화물 | `Na₂ZrCl₆` | **0.018** | ref 17 Kwak 2021 *ESM* 37, 47 |
| Zr 염화물 | `Na₀.₇La₀.₇Zr₀.₃Cl₄` | 0.29 | ref 18 Fu 2024 *Nat. Commun.* 15, 4315 |
| Zr 염화물 | `Na₀.₆₂₅Y₀.₂₅Zr₀.₇₅Cl₄.₃₇₅` | 0.4 | ref 19 Ridley 2024 *Matter* 7, 485 |
| Ta 염화물 | **`NaTaCl₆`** | **3.3** | ref 20 Li 2025 *Nat. Commun.* 16, 6633 (**paddle-wheel**) |
| 옥시염화물 | `NaAlCl₂.₅O₀.₇₅` | 1.33 | ref 21 Dai 2023 *Nat. Energy* 8, 1221 (**유리**) |
| 옥시염화물 | `NaTaOCl₄` | 1.1 | ref 22 Zhou 2024 *ACS EL* 9, 4093 |
| 불소화 | `Na₀.₅ZrCl₄F₀.₅` | 0.11 | ref 23 Wu 2025 *Nat. Commun.* 16, 2808 (**비정질**) |

> ⚠ **σ 는 이 논문의 계산 결과가 아니라 선정 사유**다. 본문은 *"Representative HSEs with high ionic conductivities (~1 mS cm⁻¹)"* 라 쓰는데 **`Na₂ZrCl₆` 는 0.018 mS/cm 로 ~1 의 1/55** 이고 **`Na₀.₅ZrCl₄F₀.₅` 는 0.11** 이다 ⇒ **"~1 mS cm⁻¹" 은 7종 중 3종에만 맞다** (§10-6).
> 🔴 **`NaTaCl₆`(σ 최고 3.3)이 계면 반응성에서는 7종 중 최악**(O3 −255.0) 이다 ⇒ **σ ↔ 계면안정 트레이드오프**가 이 표 안에 이미 들어 있는데 논문이 지적하지 않는다.
> ⚠ **`Na₀.₅ZrCl₄F₀.₅`(비정질)·`NaAlCl₂.₅O₀.₇₅`(유리)를 결정상 MP 엔트리로 계산했다** — 논문 스스로 토론에서 *"halide electrolytes synthesized via non-equilibrium routes may exhibit **amorphous, nanocrystalline, or metastable phases**"* 라며 자인한다 (§10-3).

### 3g. `Table S1` — 양극 14종의 작동창·용량 (전부 문헌 소환값)

| 계열 | 양극 | 작동창 (V) | 용량 (mAh/g)/율속 |
|---|---|---|---|
| Polyanionic | `Na₃V₂(PO₄)₃` | 2.7–3.8 | 66.3 / 0.05 C |
| Polyanionic | `NaFePO₄` | **2.2–4.3** | 125 / (C/20) |
| P2 | `Na₀.₆Mn₀.₈Li₀.₂O₂` | **2.0–4.6** ← 최고 | 190 / (C/20) |
| P2 | `Na₀.₆₇Fe₀.₅Mn₀.₅O₂` | 1.5–4.3 | 190 / 0.05 C |
| P2 | `Na₀.₆₇Ni₀.₃₃Mn₀.₃₃Ti₀.₃₃O₂` | 2.5–4.15 | 88 / 1 C |
| P2 | `Na₀.₆₇Co₀.₅Mn₀.₅O₂` | 1.5–4.3 | 147 / 0.1 C |
| P2 | `Na₀.₆₇Mn₀.₆₅Co₀.₂Ni₀.₁₅O₂` | 2.0–4.4 | 141 / 0.1 C |
| P2 | `Na₀.₆₇Mn₀.₇Ni₀.₂Mg₀.₁O₂` | 2.0–4.5 | 128 / 12 mA g⁻¹ |
| O3 | `NaFe₀.₅Co₀.₅O₂` | 2.5–4.0 | 160 / 12 mA g⁻¹ |
| O3 | `NaNi₀.₅Mn₀.₅O₂` | 2.0–4.0 | 141 / 0.05 C |
| O3 | `NaNi₀.₅Fe₀.₅O₂` | 2.0–3.9 | 129 / 23.8 mA g⁻¹ |
| O3 | `NaNi₀.₃₃Fe₀.₃₃Mn₀.₃₃O₂` | 1.5–4.1 | 100 / 0.5 C |
| O3 | `NaNi₀.₃₃Mn₀.₃₃Co₀.₃₃O₂` | 2.0–3.75 | 120 / 0.1 C |
| O3 | `NaNi₀.₆₁Co₀.₁₂Mn₀.₂₇O₂` | 1.5–4.1 | 153 / 0.5 C |

> 🔑 **`Fig. 1` 의 회색 "Cathodes" 막대(≈1.5–4.6 V)가 이 표의 전 구간 합집합**이다 (우리 산수: min 1.5, max 4.6 ✓).
> 🔴 **그래서 "HSE 창이 양극 작동창을 덮는다" 는 주장이 *산화 쪽에서 성립하지 않는다*** — 열역학 3.76 V < 최고 4.6 V, 동역학 연장 4.18 V < 4.6 V. 본문도 *"the intrinsic oxidation potential **does not fully cover** the operating voltage range of 4 V-class cathodes"* 로 인정한 뒤 *"kinetic overpotentials can effectively extend"* 로 넘어간다 — ⚠ **결론 절에서는 이 단서가 사라지고 *"broadly cover the operating potential range of cathodes"* 로 바뀐다** (§10-2).

---

## 4. ESW 창의 조작적 정의 ★★★ (임무 ①의 심장)

### 4-1. 활자 세 곳 — 전부 옮긴다

**① 창의 정의 (본문 p.2, 축자)**
> *"The decomposition energy profiles in `Figure 2` and `Figure S1` illustrate the thermodynamic driving forces for reduction and oxidation reactions as a function of potential. **Within the electrochemical stability window, the decomposition energy remains zero but increases upon reaching the reduction and oxidation potentials.**"*

**② 계산 절차 (`Methods` p.8, 축자)**
> *"Electrochemical stability windows were evaluated using a **grand-potential phase-diagram** approach.^(26,33,34) For each SE, phase diagrams were constructed, and the **sodium chemical potential (corresponding to the voltage versus Na/Na⁺) was varied to identify the voltage range over which the SE remains thermodynamically stable without decomposition into competing phases**. This voltage range is defined as the electrochemical stability window."*

**③ 계면 쪽은 별도 양 (`Methods` p.8, 식 1–2)**
> Δ*E*_D(A, B, x) = *E*_eq(*C*_bin(*C*_A, *C*_B, x)) − *E*_bin(A, B, x)  … (1)
> Δ*E*_D,mutual(A, B, x) = Δ*E*_D(A, B, x) − x Δ*E*_D(A) − (1−x) Δ*E*_D(B)  … (2)
> *"For each pair, the maximum thermodynamic driving force was determined by **varying the reaction ratio** to identify the most energetically favorable decomposition reaction."*

### 4-2. 정의가 **두 겹으로 중복 선언**돼 있다 — 이게 이 논문의 장점이다

| 겹 | 어디에 | 무엇이 0 이어야 하나 | 우리 데이터의 대응 |
|---|---|---|---|
| **① 에너지 판정** | `Table S3` 의 `ΔE_D` 열 · `Fig. 2a–d`·`Fig. S1a–c` 의 세로축 | **ΔE_D = 0** (두 가장자리 행이 전부 `0.000`) | 🔴 **우리 `esw_*.json` 에 이 열이 없다** (§7-8) |
| **② 교환량 판정** | `Fig. 2e–h`·`Fig. S1d–f` 의 세로축 **`Na uptake per f.u.`** | **uptake = 0** (계단의 평탄 구간) | ✅ **우리 `steps` 의 `evolution` 이 정확히 이것** |

🔑 **두 판정이 그림에서 *같은 구간*을 준다.** `Fig. 2a` 의 음영(`ESW` 라벨)과 `Fig. 2e` 의 uptake=0 평탄이 **픽셀 단위로 겹친다**(실독 확인). ⇒ **중복 선언이라 한쪽이 틀리면 눈에 보인다.** `[Schw21]` 은 이 중복이 없어서 `Table 2` 머리글과 LLZO 문단이 **뒤집힌 채로 인쇄됐다**.

### 4-3. 🔴🔴 **그리고 그 두 겹이 우리 버그를 정확히 재현해 보인다**

`Fig. 2e` (`Na₂ZrCl₆`) 의 계단을 그대로 적으면 (실독 + `Table S3` 대조):

```
V:       0 ──1.04── 1.24 ── 1.57 ── 1.69 ────────── 3.75 ── 4.78 ── 5
uptake:  4     3       2       1       0  (창)        −1.35   −1.75
ΔE_D: −.614  −.153  −.086   −.013    0.000          0.000   −0.152
                              ↑        ↑
                   우리 버그가     진짜 환원 전위
                   잡는 행(1.57)       (1.69)
```

- **`uptake > 0` 인 행의 최대 전압 = 1.57 V** ← `red = max(V | evolution > 0)` 이 주는 값
- **`uptake == 0` 인 행 = 1.69 V** ← 저들이 "reduction potential" 이라 부르는 값
- **차 = 0.12 V**

그리고 **산화 쪽은 우리 규칙이 맞는다**: `ox = min(V | evolution < 0)` → 3.75 V = 저들 산화 전위 ✓.
🔑 **비대칭의 이유**: 사다리의 각 행은 **자기 위쪽 구간의 평형**을 이름표로 달고 있다. 그래서
- **아래 가장자리**(1.69)는 *"창 그 자체"* 를 이름표로 달아 **교환량 0** ⇒ `>0` 필터에서 탈락 ❌
- **위 가장자리**(3.75)는 *"첫 산화평형"* 을 이름표로 달아 **교환량 음수** ⇒ `<0` 필터에 포착 ✅

⇒ **우리 도구의 환원 쪽만 틀리고 산화 쪽은 맞는 것이, 우연이 아니라 이 구조 때문이다.**

### 4-4. ⭐ `Table S2` 와 `Table S3` 이 **일부러 다른 이름표**를 쓴다 (읽을 때 조심)

| SE | `Table S2` 의 *"환원 전위에서의 평형상"* | `Table S3` 에서 그 평형이 실제로 열리는 전위 | `Table S3` 의 가장자리 행 |
|---|---|---|---|
| `Na₂ZrCl₆` | `ZrCl₃, NaCl` | **1.57 V** | 1.69 V → `Na₂ZrCl₆` |
| `Na₀.₇La₀.₇Zr₀.₃Cl₄` | `ZrCl₃, LaCl₃, NaCl` | **1.57 V** | 1.68 V → SE |
| `Na₀.₆₂₅Y₀.₂₅Zr₀.₇₅Cl₄.₃₇₅` | `ZrCl₃, Na₃YCl₆, NaCl` | **1.57 V** | 1.69 V → SE |
| `NaTaCl₆` | `Ta₂Cl₅, NaCl` | **1.81 V** | 2.17 V → SE |
| `NaAlCl₂.₅O₀.₇₅` | `NaCl, Al₂O₃, Al` | **0.39 V** | 1.49 V → SE |
| `NaTaOCl₄` | `Ta₂Cl₅, NaCl, Ta₂O₅` | **1.86 V** | 2.13 V → SE |
| `Na₀.₅ZrCl₄F₀.₅` | `ZrCl₃, NaCl, ZrF₄` | **1.57 V** | 1.69 V → SE |

⇒ **7/7 에서 일관된 관례다** (인쇄 오류가 아니다):
- **`Table S2` 의 "환원 전위" = 숫자**는 **가장자리**(1.69)
- **`Table S2` 의 "환원 전위에서의 평형상" = 이름표**는 **가장자리 아래 계단**(1.57)에서 오는 **"넘어가면 생기는 것"**
- **`Table S3` 은 가장자리 행에 SE 자신**을 적는다

🔴 **두 표를 섞어 읽으면 틀린다** — `Table S3` 만 보고 *"환원 전위에서 SE 가 그대로 있다"* 고 읽으면 산물을 못 얻고, `Table S2` 만 보고 *"1.69 V 에서 ZrCl₃ 가 생긴다"* 고 읽으면 전위를 0.12 V 잘못 잡는다. **이 논문은 그 둘을 다 인쇄해서 독자가 맞출 수 있게 해 놨다.**

⭐⭐ **우리 도구도 정확히 이 두 조각을 이미 갖고 있다** — `ocv_V`(= 가장자리 숫자) 와 `reduction_V` 행의 반응식(= 아래 계단 산물). **라벨만 뒤바뀌어 있다** (§7-2).

### 4-5. 축별 대조 (판정 아님, 나란히만)

| 축 | **이 논문** | `[Schw21]` decomposition | `[Schw21]` intrinsic | **우리 `esw_lis4excluded.json`** |
|---|---|---|---|---|
| 이온종 | **Na** | Li | Li | Li |
| 열린 변수 | **μ_Na** (grand potential) | μ_Li | 조성 x (닫힌계) | **μ_Li** |
| 상공간 | Na–M–Cl(–O/F) **전체** (MP) | 전체 (MP) | 아지로다이트 구조 안 | **전체** (MP2026 + MP2020 보정) |
| 한계의 정의 | **"ΔE_D = 0 인 구간의 양 끝"** (+ uptake=0 중복) | *"SE 조성에 가장 가까운 분해전위"* | 첫 hull 점까지 평균전압 | **Li 교환 0 구간의 양 끝** |
| 방향 표기 | ✅ **그림 축 `Na uptake per f.u.` + Sodiation/Desodiation 화살표** | ❌ **`Table 2` 머리글이 값과 뒤집힘** | (해당 없음) | ✅ `steps[i][1]` = 부호 있는 evolution |
| 균형 반응식 | 🔴 **없다** — `Table S3` 은 **상 목록만**, Na 계수 0개 | 없음 | 없음 | ✅ **완전 균형식** (`Li6PS5Cl + 8 Li -> Li3P + 5 Li2S + LiCl`) |
| ΔE_D(V) 열 | ✅ **있다** (`Table S3`) | ❌ 없음 | ❌ 없음 | 🔴 **없다** |
| 동역학 연장 | ✅ **−25 meV/atom 문턱** (7종 값) | ❌ (가정만) | ❌ | ❌ |
| 층②(골격유지) | ❌ **없다** | (해당) | ✅ | ❌ 없음 |
| pseudo-binary | ❌ 창엔 안 씀 / ✅ **계면엔 씀**(식 1–2) | ❌ | — | ❌ 창엔 안 씀 / ✅ 계면엔 씀(`InterfacialReactivity`) |
| 상도 스냅샷 | 🔴 **MP, 판본 미기재** | 🔴 판본 미기재 | (자체) | ✅ **MP2026** (신 id `mp-aaaceqmj`) |
| `[Xiao20Rev]` 4층 | **층 ①** (+ 문턱 완화판) | **층 ①** | **층 ②** | **층 ①** |

🔑 **각자 잘하는 칸이 다르다.** 저들은 **ΔE_D 열 · 동역학 문턱 · 그림 축 방향표기**가 우리보다 낫고, 우리는 **균형 반응식 · MP 판본 명시**가 저들보다 낫다. ⇒ **§7-8 의 개선 목록이 그대로 나온다.**

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5a. `Fig. 1` — 10종 창 전경 + 양극 작동창 — **실독**

가로 막대 **11행**(맨 위 회색 `Cathodes` + SE 10종), x 축 **Stability window (V vs Na/Na⁺) 0–5**. 색 규약: **파랑 = Chloride**(4종) · **주황 = Oxychloride**(2종) · **초록 = Fluorinated**(1종) · **빨강 = Sulfides**(3종). 각 색 막대 **바깥에 회색 파선 상자**가 하나씩 더 있다 = **동역학 연장창**.

`figure-read ≈` 로 읽은 것 (인쇄값이 있는 것은 §3a 가 정본):
- 회색 `Cathodes` 막대: **≈1.5 → ≈4.6 V** (= `Table S1` 합집합 ✓)
- `Na₂ZrCl₆` 실선 ≈1.7 → ≈3.75, **파선 ≈1.5 → ≈3.95**
- `Na₃SbS₄` 실선이 **거의 선 하나**(≈1.63 → ≈1.68, 폭 `figure-read ≈` 0.05 V), 파선 ≈1.45 → ≈1.9
- `Na₃PS₄` 실선 ≈**1.25** → ≈2.05, 파선 ≈1.1 → ≈2.2
- `Na₁₁Sn₂PS₁₂` 실선 ≈**1.2** → ≈1.92, 파선 ≈1.05 → ≈2.1

> 🔴 **황화물의 *환원* 한계는 이 그림에서만 읽힌다** — 본문은 산화 3개(1.66 / 2.05 / 1.91)만 준다. 위 세 값은 **`figure-read ≈`** 이고 **인용 시 반드시 그렇게 표시**해야 한다.
> 🔑 **`Na₃SbS₄` 의 창이 사실상 0 이다**(`figure-read ≈` 0.05 V). 논문은 이것을 언급하지 않고 *"approximately 2 V"* 라는 산화값만 적는다. ⚠ **창 폭이 0.05 V 인 전해질**은 그 자체로 놀라운 결과인데 서술이 없다.
> 🔑 **파선 상자가 *양쪽*으로 뻗는다** — 즉 동역학 연장은 산화·환원 양쪽에 적용됐는데 **본문은 산화 쪽 7개만 숫자로 준다**(§3c).
> 🔑 **할라이드 7종의 오른쪽 끝이 한 줄로 정렬**된다 = `NaCl₃` 가 정하는 공통 가장자리. **눈으로 보이는 "음이온이 창을 독점한다"** 의 그림 증거다.

### 5b. `Fig. 2` — 분해에너지 프로파일 + **Na uptake 계단** (a–h) — **실독** · 이 digest 에서 가장 중요한 그림

**위줄 (a–d)** = `Decomposition energy (eV/atom)` vs `Voltage (V) vs. Na/Na⁺`, y 범위 **−0.5 … +0.1**, x **0–5**. 네 계: (a) `Na₂ZrCl₆` 파랑 · (b) **"`Na₂TaCl₆`"** 주황 · (c) `NaAlCl₂.₅O₀.₇₅` 보라 · (d) `Na₀.₅ZrCl₄F₀.₅` 올리브.
- **(a) 에만 주석이 있다**: 좌상 **`← Reduction`** 화살표, 우상 **`Oxidation →`** 화살표, 음영 안에 **`ESW`** 라벨.
- 곡선은 **0 에서 정확히 평탄**했다가 양 끝에서 꺾여 내려간다. 음영(연한 색)이 그 평탄 구간을 덮는다.
- **(a) 의 왼쪽 꺾임이 `figure-read ≈` 1.7, 오른쪽 ≈3.75** → `Table S3` 1.69/3.75 와 일치.
- **오른쪽 꺾임 이후 기울기가 계마다 눈에 띄게 다르다**: (a) 가 가장 가파르고 (d) 가 가장 완만하다 — **§3c 의 −0.148 vs −0.055 eV/V 를 눈으로 확인**한 것이다 ✅

**아래줄 (e–h)** = **`Na uptake per f.u.`** vs 같은 x. **이것이 임무 ①의 증거 그림이다.**
- **(e) 에만 주석**: 좌하 **`← Sodiation`**, 우하 **`Desodiation →`**, 그리고 **y=0 에 회색 점선**.
- **(e) `Na₂ZrCl₆`** y 범위 −2…4: 계단이 **4 → 3(≈1.04) → 2(≈1.24) → 1(≈1.57) → 0(1.69–3.75) → ≈−1.35(3.75) → ≈−1.75(≈4.78)**
- **(f) "`Na₂TaCl₆`"** y −1…5: **5 → 2.5(≈1.81) → 0(2.17–3.76) → ≈−0.65 → ≈−0.85**
- **(g) `NaAlCl₂.₅O₀.₇₅`** y −1…2: **1.85 → 1.5(≈0.3) → 0(1.49–3.76) → ≈−0.35 → −0.5 → ≈−0.9** (음의 쪽이 **여러 계단**)
- **(h) `Na₀.₅ZrCl₄F₀.₅`** y −1…4: **4 → 3.6 → 2.7 → 1.75 → 0.85 → 0(1.69–3.76) → ≈−0.3 → ≈−0.5**

> 🔴🔴 **(e)–(h) 네 계 전부에서 uptake=0 평탄이 (a)–(d) 의 ΔE_D=0 평탄과 정확히 겹친다.** 중복 선언이 시각적으로 확인된다 (§4-2).
> 🔴🔴 **그리고 네 계 전부에서, 0 평탄 바로 왼쪽 계단의 uptake 가 *양수*다**(1 / 2.5 / 1.5 / 0.85). ⇒ **`max(V | uptake > 0)` 은 네 계 전부에서 한 계단 아래를 준다.** 이것이 우리 버그의 외부 눈금이다.
> ⚠ **(b)·(f) 의 라벨이 "`Na₂TaCl₆`" 로 인쇄돼 있다.** 캡션·`Table 1`·`Table S2`·`Table S3`·`Fig. 1`·`Fig. 3` 은 전부 **`NaTaCl₆`** 다. **그림 안 라벨만 틀렸다**(§10-6). 값(2.17/3.76)은 `NaTaCl₆` 와 맞는다.
> 🔑 **(g) 의 산화 쪽이 여러 계단**인 것이 `Table S3` 의 `NaAlCl₂.₅O₀.₇₅` 산화 사다리(3.76 → 4.13 → 4.23 → 4.78 → 5.58)와 대응한다 — **유일하게 4 V 근처에 중간 계단이 두 개 있는 계**이고, 그래서 §3c 에서 보간 구간이 달랐다.

### 5c. `Fig. S1` — 나머지 3종의 같은 그림 — **실독**

(a,d) `Na₀.₇La₀.₇Zr₀.₃Cl₄` 초록 · (b,e) `Na₀.₆₂₅Y₀.₂₅Zr₀.₇₅Cl₄.₃₇₅` 분홍 · (c,f) `NaTaOCl₄` 적갈색. 축·범위·음영 규약이 `Fig. 2` 와 동일하고 **주석 화살표는 없다**.

`figure-read ≈` 계단:
- **(d)** `3.3 → 1.2(≈0.4) → 0.85(≈1.04) → 0.55(≈1.24) → 0.3(≈1.57) → 0(1.68–3.76) → ≈−0.45 → ≈−0.6`
- **(e)** `3.75 → 3.1 → 3.0 → 2.25 → 1.5 → 0.7(≈1.57) → 0(1.69–3.77) → ≈−0.45 → ≈−0.6`
- **(f)** `4.0 → 3.3 → 3.1(≈0.95) → 1.85(≈1.81) → 1.5(≈1.86) → 0(2.13–3.76) → ≈−0.65 → ≈−0.85`

> ✅ **3종 모두 같은 구조** — 0 평탄 바로 아래 계단이 양수(0.3 / 0.7 / 1.5). **7종 전수에서 우리 버그가 재현된다.**
> ⚠ **(e) 의 계단 수(6개)가 `Table S3` 의 환원 행 수(6개: 0.00·0.52·0.58·1.04·1.24·1.57)와 맞는다** ✓ — 표와 그림이 정합한다.

### 5d. `Fig. S2` — ΔE_D 와 ΔE_D,mutual 의 차이 도해 — **실독**

`Reaction energy` vs `Mix ratio`, **눈금 없음**. A(왼쪽 끝)·B(오른쪽 끝)에 각각 **검은 점(y=0)** 과 그 위 **회색 점**이 있고, 둘 사이를 **연한 파란 띠**가 채우며 왼쪽에 **`Metastable region`** 화살표가 붙는다. 중앙 아래 한 점(x)에서 두 선이 만난다:
- **파란 선** = 회색 점(A) ↔ 회색 점(B) 를 잇는 직선 → 그 아래 화살표가 **`ΔE_D(A, B, x)`**
- **검은 선** = 검은 점(A, y=0) ↔ 검은 점(B, y=0) → 그 아래 화살표가 **`ΔE_D,mutual(A, B, x)`**
- 오른쪽에 두 화살표가 나란히 그려져 **mutual 이 더 짧다**(= 덜 음수)는 것을 보인다.

> 🔑 **읽는 법**: 회색 점 = 각 물질 *자신의* hull 위 거리(= 준안정성). 파란 띠 = 그 준안정 몫. **mutual 은 그 몫을 빼고 "맞닿아서 새로 생긴 구동력" 만 남긴다.**
> ⭐⭐ **우리 산수로 대수를 풀면 저들 식 (2) 가 pymatgen `InterfacialReactivity(use_hull_energy=True)` 와 *정확히 같다***:
> ΔE_D,mutual = [E_eq(mix) − E_bin] − x[E_hull(A)−E(A)] − (1−x)[E_hull(B)−E(B)] = **E_eq(mix) − [x·E_hull(A) + (1−x)·E_hull(B)]**
> ⇒ **우리 `comp1|LiCoO₂ = −0.3227 eV/atom` 과 *같은 보고량*이다** (§7-7). 이온만 다르다.
> 🔴 **그런데 이 논문에서는 식 (2) 가 식 (1) 과 수치적으로 같아진다** — `Methods` 가 *"The HSEs and sodium cathode materials were **assumed to be thermodynamically stable, corresponding to phases located on the convex hull**"* 라 하고 코팅은 필터 (ii) 로 **`E_hull = 0`** 만 남겼기 때문이다. 세 부류 전부 ΔE_D(A)=ΔE_D(B)=0 ⇒ **뺄 것이 없다** (우리 유도). ⇒ **`Fig. S2` 가 설명하는 보정이 이 논문 안에서는 한 번도 작동하지 않는다** (§10-5).

### 5e. `Fig. 3` — SE‖양극 heatmap — **실독** (§3d 가 전수)

10행 × 14열. 왼쪽에 **파랑 Chloride / 주황 Oxychloride / 초록 Fluorinated / 빨강 Sulfides** 괄호, 아래에 **Polyanionic / P2 / O3** 괄호. 컬러바 **−400 … 0 meV/atom** (빨강 = 반응성 높음, 파랑 = 안정).
할라이드 7행 98 셀을 `Table S4` 텍스트와 **전수 대조 → 98/98 일치** ✅ ⇒ 황화물 3행 42 셀 판독도 신뢰.

> 🔴 **눈으로 먼저 보이는 것이 "할라이드가 낫다" 가 아니다.** 맨 아랫줄 `Na₃PS₄` 만 진한 빨강이고, 그 위 두 황화물(`Na₃SbS₄`·`Na₁₁Sn₂PS₁₂`)은 **할라이드 블록과 색이 섞인다.** 특히 **P2 열에서는 두 황화물이 할라이드보다 붉고, O3 열에서는 오히려 `NaTaCl₆`·`Na₀.₅ZrCl₄F₀.₅` 가 더 붉다.**
> ⇒ **`Fig. 3` 은 본문 주장의 근거이면서 동시에 반례를 품고 있다** (§10-4).

### 5f. `Fig. 8` — 혼합비별 상호반응에너지 곡선 (a–f) — **실독**

6패널, 각 패널에 **세 곡선**: **회색 = 양극‖HSE**(코팅 없음) · **파랑 = 양극‖`NaB₃O₅`** · **빨강 = HSE‖`NaB₃O₅`**. x = `Ratio of B in mixture A-B` 0→1, y = `Mutual reaction E (eV/atom)`.
(a–c) `Na₂ZrCl₆` 계 / (d–f) `NaTaOCl₄` 계. 양극은 각각 `Na₀.₆₇Mn₀.₆₅Co₀.₂Ni₀.₁₅O₂` / `NaNi₀.₃₃Fe₀.₃₃Mn₀.₃₃O₂` / `NaNi₀.₆₁Co₀.₁₂Mn₀.₂₇O₂`.

- **회색 곡선은 깊은 V자**, 최저점이 `figure-read ≈` **x = 0.30–0.40**, 깊이 −0.13 … −0.24.
- **파랑(양극‖코팅)은 얕은 V자**, 최저점 `figure-read ≈` **x = 0.5–0.6**, 깊이 −0.03 … −0.035.
- **빨강(HSE‖코팅)은 거의 직선에 가깝고 최저점이 *끝단 근처*** — `figure-read ≈` **x ≈ 0.06–0.07**, 깊이 −0.019(a–c) / −0.023(d–f).

> 🔴🔴 **이것이 이 그림에서만 읽히는 중요한 것이다**: **보고값은 "x 를 전부 훑어 얻은 최댓값" 이고, 그 x 가 짝마다 전혀 다르다** — HSE‖코팅은 **x ≈ 0.07**(= 코팅이 아주 조금 섞인 지점), 양극‖HSE 는 **x ≈ 0.35**. ⇒ **−19 meV/atom 과 −213 meV/atom 은 *다른 화학량론*에서 온 값**이고, 실제 계면의 조성비와는 아무 관계가 없다.
> ⚠ **그러므로 이 값들을 "계면상 형성에너지" 로 읽으면 안 된다.** 저자도 토론에서 *"should therefore be interpreted as **relative indicators** of thermodynamic compatibility, rather than as direct predictions of interfacial reaction pathways or decomposition products"* 라 적는다 — **정직한 자인**이고 인용 시 반드시 동반해야 한다.
> 🔑 **점의 밀도가 곡선마다 다르다**(회색 ~20점, 빨강 ~8점) — **x 격자가 균일하지 않다.** 최댓값 탐색의 격자 해상도가 미기재다.
> ⭐ **우리 `comp1|LiCoO₂` 의 `min @ x = 0.5302` 와 같은 종류의 수**다. 우리는 x 를 기록하는데 **저들은 본문·표 어디에도 x 를 안 적는다** — `Fig. 8` 에서만 읽힌다 ⇒ **이 칸은 우리가 낫다**.

### 5g. `Fig. 5` — PCA–K-means 군집 + 군집 평균 heatmap — **실독**

**(a)** `Principle component 2` vs `Principle component 1`(원문 철자 그대로 — *Principal* 오기), 범위 x −10…20, y −10…10. 네 색 구름: **분홍 Group A**(x ≈ −6…+2, 가장 조밀) · **주황 Group B**(x ≈ −3…+4, A 아래) · **하늘 Group C**(x ≈ −2…+6, 위쪽) · **초록 Group D**(x ≈ +5…+15, 오른쪽으로 길게 뻗음, 점 수 최소).
**(b)** 4행(Group A–D) × **21열**(HSE 7 + 양극 14), 컬러바 **−200…0 meV/atom**, **셀마다 숫자 인쇄**.

| Group | HSE 7열 (평균, 우리 산수) | 양극 14열 (평균, 우리 산수) | **21열 전체 (우리 산수)** | 논문의 서술 |
|---|---|---|---|---|
| **A** | **−94.8** (−73.45 … −110.83) | **−26.3** (−7.15 … −44.14) | **−49.2** | *"slightly negative … toward SE … low reactivity with cathodes … stable group"* |
| **B** | **−33.5** (−27.8 … −53.6) | **−49.3** (−7.1 … −77.2) | **−44.0** | *"even lower overall … **most stable group**"* |
| **C** | **−86.6** (−68.2 … −116.86) | **−90.1** (−20.24 … −138.58) | **−88.9** | *"intermediate … moderately stable"* |
| **D** | **−11.4** (−8.62 … −17.71) | **−145.7** (−69.47 … −203.06) | **−100.9** | *"stable with SEs but pronounced reactivity toward cathodes … reactive group"* |

> 🔴 **본문의 Group A 서술이 그림과 어긋난다.** *"slightly negative reaction energies **toward solid electrolyte** interfaces"* 라는데 실제 SE 쪽 평균은 **−94.8 meV/atom** 이고, 이는 **코팅 없는 SE‖polyanionic 양극 값(−80.6)보다 더 나쁘다.** Group A 가 낮은 것은 **양극 쪽(−26.3)** 이다 — **두 쪽이 뒤바뀌어 서술됐다** (§10-6).
> 🔴 **"Group B 가 most stable" 은 21열 평균 −44.0 vs A 의 −49.2, 즉 5.2 meV/atom 차**다. 그런데 **두 군집의 구조는 정반대**다(A: SE 나쁨/양극 좋음, B: 균형). **5 meV/atom 으로 "가장 안정" 을 선언하는 것은 근거가 얇다.**
> 🔴🔴 **군집이 최종 선별에 아무 일도 안 한다.** 최종 11종을 `Table S5` 와 대조하면 **10종이 Group B, 1종(`Na₂Al₂Si₃(HO₃)₄`)이 Group A** 다(우리 대조). 그런데 선별 기준은 *"평균 < 50, 최대 < 60 meV/atom"* 이라는 **같은 ΔE_D,mutual 에 건 숫자 문턱**이다. 실용 25종은 **Group A 와 B 를 섞어** 뽑는다(`NaTaO₃`·`Na₃Sc₂(PO₄)₃`·`NaAlSiO₄`·`NaNbO₃`·`NaBePO₄`·`NaSn₂(PO₄)₃`·`NaBe₄SbO₇`·`Na₄Mg₃P₄O₁₅` = Group A). ⇒ **PCA–K-means 는 `Fig. 4` 워크플로에 상자로 그려져 있지만 게이트가 아니다. 서술용이다.**
> ⭐ **`[Park26ML]` §J-22-3 (*"선택 기준이 실제로는 하나뿐이었다"*)과 같은 구조의 두 번째 사례**다.
> 🔑 **Group D 의 정체**(`Table S5`): `Na₃YCl₆`·`Na₃ErCl₆`·`NaAlCl₄`·`NaTaCl₆`·`NaBF₄`·`NaPF₆` … **전부 할로겐화물**이다. ⇒ **"SE 와는 잘 맞고 양극과는 최악" 인 군집이 곧 할라이드 자신**이다 — 이 논문의 주제문을 군집이 독립적으로 재발견한 셈이고, **그건 실제로 의미 있는 결과인데 본문이 그렇게 읽지 않는다.**

### 5h. 본문 서사 (Results 순서대로)

1. **창 (p.2)**: 황화물 산화 ~2 V ⇒ 양극 작동창 안에서 산화분해. 할라이드 산화 ~3.76 V, **`NaCl₃` 공통**. 환원은 중심금속별(Zr 1.69 / Ta 2.18 / Al 1.49). *"the reduction potentials of all HSEs remain below 2.2 V, suggesting sufficient thermodynamic stability against reduction."*
2. **동역학 연장 (p.2–3)**: `<25 meV/atom` 까지는 *"can be kinetically suppressed"* ⇒ 산화 3.92–4.18 V. **Al 계가 가장 높고, F 치환이 3.92→4.18.**
3. **계면 (p.3)**: 창이 넓어도 궁합은 별개. **Polyanionic −80 / P2 −140 / O3 −220.** 황화물은 **−230 / −250**. *"HSEs still demonstrate **considerable** interfacial reactivity"* · *"contradicting the general assumption"*.
4. **스크리닝 (p.4)**: 12 800 → 7 995 → (hull) → **289** → PCA/K-means 4군 → **11종**(엄격) → **25종**(실용).
5. **코팅 효과 (p.6–7)**: −140/−220 → **−20 … −40**. `NaB₃O₅` 대표.
6. **한계 자인 (p.7)**: ⭐ 세 문단이 연속으로 나온다 — ① *"based on **bulk thermodynamic data** and **does not explicitly capture atomic-scale interface structures or kinetic barriers**"* ② *"bulk **crystalline** phases … halide electrolytes synthesized via non-equilibrium routes may exhibit **amorphous, nanocrystalline, or metastable** phases"* ③ *"without accounting for processing-related factors such as the **moisture sensitivity** of HSEs"*. **이 셋이 이 논문에서 제일 정직한 자리다** — 인용할 때 같이 옮긴다.

---

## 6. 기전 — "창이 넓은데 왜 계면이 나쁜가" 를 한 단계씩

### 6-1. 두 양이 묻는 질문이 다르다

| | **전기화학 창 (grand potential)** | **상호 분해에너지 (pseudo-binary)** |
|---|---|---|
| 묻는 것 | *"SE 혼자 전압을 걸면 언제 무너지나"* | *"SE 와 양극을 맞대면 전압 없이도 반응하나"* |
| 열린 변수 | **μ_Na** (Na 저장소와 교환) | **혼합비 x** (Na 교환 없음) |
| 상대 | Na 금속 (전위 기준) | **다른 고체** |
| 이 논문 값 (할라이드) | 1.49–2.18 → 3.75–3.77 V | −54 … −282 meV/atom |
| 0 이면 | 그 전압에서 안정 | **완전 화학적 양립** |

🔑 **둘이 독립이라는 것이 이 논문의 주제문**이다. `NaTaCl₆` 은 창이 **1.58 V 로 7종 중 가장 좁은데** 산화 한계는 남들과 같고(3.76), **계면은 7종 중 가장 나쁘다**(O3 −255.0). 반대로 `NaAlCl₂.₅O₀.₇₅` 는 **창이 가장 넓고**(2.27 V) **계면도 가장 낫다**(O3 −194.5). ⇒ **상관이 있는 듯 없는 듯하다** — 실제로 7종의 창 폭과 O3 계면값의 상관은 눈으로 봐도 약하다(우리 관찰, 정량 안 함).

### 6-2. 왜 할라이드‖층상산화물이 나쁜가 — 산물이 말해 준다

`Table S4` 를 읽으면 경로가 세 갈래로 갈린다 (우리 정리):

| 채널 | 무슨 일 | 대표 산물 | 어느 양극에서 |
|---|---|---|---|
| **① 음이온 교환** | 양극의 **O** 와 SE 의 **Cl** 이 자리를 바꾼다 | **`ZrO₂`/`Ta₂O₅`/`Al₂O₃`** + **`NaCl`** | 전 층상산화물 |
| **② Cl 산화** | Cl⁻ 가 양극의 산화력으로 **더 산화**된다 | **`NaClO₄`** (또는 `NaCl₃`) | 대부분의 O3, 일부 P2 |
| **③ TM 염화** | 전이금속이 **염화물**로 끌려 나온다 | `NiCl₂`·`Na₂CoCl₄`·`NaFeCl₄`·`VCl₃`·`Mn₈Cl₃O₁₀`·`Mn₇FeCl₃O₁₀` | Ni/Co/Fe 가 많은 계 |

🔑 **`NaClO₄` 는 황화물 계면에 없는 종이다** — **할라이드 고유의 산화 채널**이고, 과염소산나트륨은 **산화제**다. 논문은 산물을 표에 적기만 하고 이 함의를 논하지 않는다.
🔑 **폴리음이온 양극에서는 ①–③ 대신 `NaZr₂(PO₄)₃`·`TaPO₅`·`LaPO₄`·`YPO₄`** 가 나온다 — **인산염이 SE 의 금속을 흡수해 안정한 NASICON/인산염을 만든다** ⇒ 구동력이 절반 이하. ⭐ 그리고 **그 `NaZr₂(PO₄)₃` 가 실용 코팅 25종에 들어 있다.** *"반응이 스스로 만드는 상을 미리 깔면 반응이 멈춘다"* 는 자기정합 논리이고, **논문이 명시적으로 이 연결을 짓지 않는다** — 우리가 지을 수 있는 자리다(§12-6).

### 6-3. 왜 코팅이 듣는가 — 세 계면의 산수

`Fig. 8` 의 논리는 단순하다.
- 코팅 없음: **양극‖SE 한 계면**, 구동력 −213.
- 코팅 있음: **양극‖코팅**(−33) + **코팅‖SE**(−19) **두 계면**. 각각이 작으면 전체가 작다.
- 🔑 **코팅이 되려면 *양쪽 다* 작아야 한다** — 이것이 이 논문의 선별 기준(`평균` **그리고** `최대`)이 두 개인 이유다. `Fig. 5b` 의 Group A(SE 쪽 −94.8)와 Group D(양극 쪽 −145.7)가 탈락하는 것이 바로 이 조건 때문이다.
- ⚠ **그런데 "두 계면의 구동력이 작다" 는 것과 "코팅층이 안 자란다" 는 다른 말이다.** 두께·성장속도·자기제한 판정이 **0건**이다 (§10-1, `[Chaney24SEI]` §J-37 과 같은 공백).

### 6-4. 🔴 논증 사슬의 구멍

1. 창이 넓다 (열역학) ✅ 계산됨
2. 4.6 V 양극을 덮지는 못한다 ✅ 본문 자인
3. 그러나 **과전압이 덮어 준다** ⇠ 🔴 **`<25 meV/atom` 이라는 임의 문턱 하나**. 장벽 0건, 과전압 실측 대조 0건, 문턱 근거 문장 0건.
4. 계면 구동력이 크다 ✅ 계산됨
5. 코팅이 구동력을 줄인다 ✅ 계산됨
6. **⇒ 코팅하면 계면이 안정해진다** ⇠ 🔴 **열역학 구동력과 실제 계면 안정성 사이에 슬랩도 동역학도 실험도 없다.** 저자도 자인한다(§5h-6).

⇒ **3 과 6 이 이 논문의 두 구멍**이고, 둘 다 저자가 정직하게 표시해 뒀다는 점은 인정해야 한다 (`[Schw21]` 은 같은 구멍을 더 크게 뚫고 표시를 안 했다).

---

## 7. 우리 DFT 와의 대조 ★★★

> ⚠ 아래 문헌값은 전부 **소환값**이고 **전부 Na 계**다. 우리 db 절대값과 같은 셀에 놓지 않는다. 우리가 뺀 값은 **(우리 유도, 논문 미보고)** 로 표시한다.
> 우리 쪽 원본: `db/properties/esw_lis4excluded.json` · `litdb/our_dft_baseline.md` L19–L20 · `tools/oxidation/constrained_esw.py:80–95` · `tools/oxidation/esw_cascade_batch.py:410–436` · `db/properties/oxidation_stability.json`(`nd2o3_interface_reactivity`) · `db/properties/citation_hazards.json`(`HZ-esw-reduction-limit-label`, **BLOCKED**).

### 7-1. 🔴 먼저 확정 — **이 논문은 `HZ-esw-reduction-limit-label` 의 세 번째 외부 눈금이다**

| 눈금 | 계 | 이온 | 창의 정의가 활자로 | 방향 표기 | 우리 버그가 보이나 |
|---|---|---|---|---|---|
| **① `[Zhu15]`** | LPSCl | Li | (우리 기록: 1.71–2.01 V) | — | ⚠ 값만 있어 간접 |
| **② `[Schw21]`** | LPSC 외 11종 | Li | ✅ *"decomposition potential **closest to the stable SE phase**"* | 🔴 **뒤집혀 인쇄됨** | ⚠ 값 대조로 간접 |
| **③ 이 논문** | Na 할라이드 7종 | **Na** | ✅✅ *"decomposition energy **remains zero**"* + **`Table S3` ΔE_D 열 전수** | ✅✅ **그림 축 `Na uptake per f.u.`** | 🔴🔴 **7/7 에서 직접 보인다** |

⇒ **세 눈금이 같은 정의를 가리킨다.** ①②는 **값**으로, ③은 **구조**로. **③이 가장 강한 증거다** — 값이 아니라 *사다리의 모양*을 인쇄했기 때문에, 우리 필터를 저들 표에 적용해 보고 틀리는 것을 직접 확인할 수 있다 (§3b · §4-3).

### 7-2. ⭐⭐ **우리 도구는 이미 정답을 갖고 있다 — 라벨만 바뀌어 있다**

`db/properties/esw_lis4excluded.json` 의 `comp1.steps` 를 이 논문의 `Table S2`/`Table S3` 양식으로 다시 적으면:

| 그들 양식 | LPSCl (comp1) 의 값 | 우리 json 의 어느 칸 |
|---|---|---|
| **환원 전위 (숫자)** | **1.717 V** | 🔴 **`ocv_V`** ← 이름이 `OCV` 로 붙어 있다 |
| 환원 전위에서의 **평형상** (`Table S3` 관례) | `Li₃PS₄ + Li₂S + LiCl` (교환 0) | `steps[5]` 의 반응식 |
| 환원 전위 **아래 계단의 산물** (`Table S2` 관례) | **`5 Li₂S + LiCl + P`** | `steps[4]` 의 반응식 (= **`reduction_V` = 1.242 V 행**) |
| **산화 전위 (숫자)** | **2.256 V** | ✅ `oxidation_onset_V` |
| 산화 전위에서의 산물 | `Li₃PS₄ + LiCl + S + 2 Li` | `steps[6]` ✓ |
| **창 폭** | **0.539 V** (우리 유도) | 🔴 현재 인쇄값은 **1.014 V** |

🔑 **`ocv_V` 는 OCV 가 아니다. 그것이 환원 전위다.** `esw_cascade_batch.py:419` 의 `ocv = min(V | |evo| ≤ 1e-6)` 이 **정확히 저들 정의를 구현하고 있는데 이름이 `ocv_self_decomposition_V` 로 붙어 있다.**
⇒ ⭐⭐⭐ **그러므로 수정은 *재계산이 아니라 이름 바꾸기 + `window_V` 재유도*다.** cascade 356 행을 다시 돌릴 필요가 없다:
```
window_V  :  ox − red        →   ox − ocv          # 두 값 모두 이미 저장돼 있다
reduction_limit_V            →   first_reduction_products_V   (= Table S2 의 "평형상" 칸)
ocv_self_decomposition_V     →   reduction_limit_V            (= Table S2 의 "환원 전위" 칸)
```
⚠ **적용 전 한 가지 확인**: `min(V | |evo| ≤ 1e-6)` 은 **교환 0 행이 하나일 때만** 가장자리를 준다. 이 논문의 7종은 전부 하나였고(우리 대조), LPSCl 도 하나다(`steps` 9행 중 `evo=0` 은 1개). **cascade 356 행 전체에서 교환-0 행이 2개 이상인 사례가 있는지 세는 것이 fix 의 전제조건**이다. ⛔ **권한 밖이라 제안만 한다.**

### 7-3. 🔑 **우리 버그의 크기가 "이상한 값" 이 아니라는 것**

| | 어긋남 Δ (한 계단의 크기) |
|---|---|
| 이 논문 Zr 염화물 3종 | **0.11–0.12 V** |
| 이 논문 `NaTaOCl₄` | **0.27 V** |
| 이 논문 `NaTaCl₆` | **0.36 V** |
| **우리 LPSCl (comp1·modelc)** | **0.475 V** (1.717 − 1.242) |
| 이 논문 `NaAlCl₂.₅O₀.₇₅` | 🔴 **1.10 V** |

⇒ **우리 +0.475 V 는 이 7종이 만든 범위(0.11–1.10) 안에 들어간다.** 즉 *"우리만 유난히 크게 틀렸다"* 가 아니라 **"이 버그의 크기 = 그 계 환원 사다리의 마지막 계단 폭"** 이고, 계마다 다르다.
🔴🔴 **그래서 이 버그는 절대값만이 아니라 *계 간 순위*도 흔든다.** 사다리가 성긴 계(Al 계 1.10 V)와 촘촘한 계(Zr 계 0.12 V)가 **1 V 가까이 다르게 틀린다** ⇒ ⛔ **정정 전 `window_V` 로 cascade 후보를 서열화한 결과는 전부 무효로 봐야 한다** (원장이 이미 BLOCKED 로 잡아 뒀다 — 이 논문이 그 판정을 **강화**한다).

### 7-4. ⚠ 그리고 이 논문이 **우리 산화 쪽은 건드리지 않는다**

- 우리 `ox = min(V | evolution < 0)` 은 저들 산화 전위 정의와 **일치**한다 (§4-3). ✅
- 그러므로 `[Schw21]` 이 남긴 **산화 쪽 0.246 V 격차**(우리 2.256 ↔ 저들 2.01)는 **이 논문으로는 줄지도 늘지도 않는다.** 이온·계가 달라 대조점이 아니다.
- ⇒ **감사 ①의 남은 한 변은 여전히 열려 있다.** 이 논문의 기여는 **환원 쪽 판정을 세 번째로 못박은 것**이다.

### 7-5. 축별 대조표 (판정 아님 — 나란히만)

| 축 | **이 논문 (Na, 소환값)** | **우리 (Li)** | 쓸 수 있는 말 |
|---|---|---|---|
| **ESW 정의** | ΔE_D = 0 구간 + uptake = 0 중복 선언 | Li 교환 0 구간 (라벨 오류 중) | ✅ **정의가 같다. 이온 무관.** 이게 §7-1–7-3 의 전부 |
| **§B① 산화 onset** | 할라이드 **3.75–3.77 V vs Na/Na⁺** (`NaCl₃`-limited) | comp1·modelc **2.256 V vs Li/Li⁺** (S²⁻-limited) | ⛔⛔ **수치 비교 절대 금지** — 이온·기준전극·음이온·화학계가 전부 다르다. ✅ **구조만**: *"한 음이온이 창의 산화 변을 독점한다"* 가 두 계에서 같다 |
| **§B① 치환 효과** | Cl→F: 열역학 **+0.01 V**, 동역학 **+0.26 V** | Cl 증량(comp1→modelc): 열역학 **±0.000 V** | ⭐⭐ **가장 값진 정합.** *"할로겐 치환은 onset 을 안 움직이고 onset 이후를 바꾼다"* 가 **Li 황화물과 Na 할라이드에서 똑같이** 나온다 ⇒ 우리 §B 축 명명 규율의 **이온종 독립 외부 실증** |
| **§B① 동역학 연장** | **−25 meV/atom 문턱**, 산화 +0.16 … +0.42 V | ❌ **없다** — 우리는 과전압을 `[Du22LMR]`·`[Wei23LNO]` 실측으로만 말한다 | ⭐ **이식 가능한 관례.** ⛔ 단 **문턱 25 meV/atom 에 근거가 없다** — 옮긴다면 **우리가 근거를 대야 한다** (§12-3) |
| **§B③ 계면 반응성** | ΔE_D,mutual, **식 (2) = 우리 `use_hull_energy=True` 와 대수적 동일** (우리 유도) | `comp1\|LiCoO₂` **−0.3227 eV/atom** (min @ x=0.5302, MP2026) | ✅ **보고량이 같다.** ⛔ **값은 못 옮긴다**(Na↔Li, 양극 다름, MP 판본 다름). ⭕ **크기 정합 확인**은 가능: 우리 −323 meV/atom 이 저들 황화물‖O3 범위(−313 … −405) 안에 든다 — **자릿수 점검**까지만 |
| **§B③ 계면 산물** | 할라이드: `NaCl`+`MO_x`+**`NaClO₄`** · 황화물: (표 없음) | comp1\|LCO 5종: `Li₃PO₄`·`Li₂SO₄`·`Li₂S`·`LiCl`·`Co₉S₈` | ⭐ **구조 대응**: 우리 `LiCl` ↔ 저들 `NaCl` (할로겐 배출), 우리 `Li₂SO₄` ↔ 저들 **`NaClO₄`** (음이온의 *추가 산화*). **"음이온이 양극의 O 를 받아 더 산화되는 채널" 이 두 화학계에 공통**이다 |
| **§C 기계** | ⛔ **0건** (`deformability` 는 서론에서 인용만) | E_VRH 22.06/27.66 GPa · B₀ 26.23/21.71 GPa | 대조 불가 |
| **§D 전자구조** | ⛔ **자체 계산 0건.** MP band gap 을 **`< 0.5 eV` 제외 필터로만** 사용 | comp1 2.066 / modelc 2.099 eV (fixed-occ nscf) | ⛔ 대조 불가. ⚠ 다만 **"SE·코팅은 전자절연이어야 한다" 는 조건이 스크리닝의 1단계**라는 점은 우리 `sei_electronic.json` 서사와 같은 방향 |
| **§A 이온전도** | ⛔ **0건** — `Table 1` 은 전부 문헌 소환값 | comp1 D(600K) 3.09e−6 · modelc 7.90e−6 cm²/s | 대조 불가. ⚠ **`NaTaCl₆`(σ 최고)가 계면 최악**이라는 트레이드오프는 정성적으로만 |
| **슬랩/계면 기하** | ⛔⛔ **0건.** 면지수·진공·이완자유도·원자수 **전부 없음** | 우리 v5 계면 기하 (슬랩) | **대조점 없음** (§7-9) |

### 7-6. 임무 ② — **Na 에만 성립하는 것 / 이온종과 무관한 것**

> ⛔ **값 이식 금지.** 아래는 *무엇을 가져오고 무엇을 두고 오나*의 목록이다.

**🟢 이온종과 무관하게 성립한다 (가져온다)**

| # | 무엇 | 왜 무관한가 |
|---|---|---|
| 1 | **창의 조작적 정의** — *"분해에너지가 0 인 구간의 양 끝"* ≡ *"교환량이 0 인 구간의 양 끝"* | grand-potential 형식은 μ_A(A=Li/Na) 에 대해 **동형**이다. 정의에 원소가 안 들어간다 |
| 2 | **가장자리 행이 교환 0 이라 `>0` 필터에서 빠진다는 구조** | 사다리의 이름표 규약 문제이고 **pymatgen 의 동작**이다. 원소 무관 |
| 3 | **`Table S2`/`Table S3` 이중 관례** (숫자는 가장자리, 산물은 아래 계단) | 보고 양식. 원소 무관 |
| 4 | **동역학 연장창 = ΔE_D(V) 가 문턱을 지나는 전압** | 에너지 판정. 원소 무관 (⚠ 문턱값 25 meV/atom 자체는 근거 없음) |
| 5 | **ΔE_D,mutual 식 (2) ≡ `use_hull_energy=True`** | 순수 대수. 원소 무관 |
| 6 | **"최댓값은 혼합비 x 를 훑어 얻는다 → 보고값은 특정 화학량론이 아니다"** | 정의. 원소 무관 |
| 7 | **"한 음이온이 산화 변을 독점한다"는 패턴** (Cl→`NaCl₃` / S→`S⁰`) | 구조적 관찰. ⚠ **패턴이지 정리(theorem)는 아니다** — 우리 계에서 따로 확인됐기 때문에 쓸 수 있는 것 |
| 8 | **"할로겐 치환은 onset 이 아니라 onset 이후를 바꾼다"** | 두 화학계에서 독립 관찰 ⇒ **우리 §B 축 명명 규율 지지** |
| 9 | **"창이 넓다 ≠ 계면이 좋다" 의 분리** | 두 보고량이 묻는 질문이 다르다는 것은 원소 무관 |
| 10 | **비판 항목 전부** (슬랩 없음·동역학 없음·군집이 게이트 아님·문턱 근거 없음) | 방법 비판 |

**🔴 Na 에만 (또는 이 계에만) 성립한다 (두고 온다)**

| # | 무엇 | 왜 못 가져오나 |
|---|---|---|
| 1 | **모든 전압 수치** (1.49–2.18 / 3.75–3.77 / 3.92–4.18 V) | **vs Na/Na⁺** 기준. Li 계와 **상수 오프셋으로 변환되지 않는다**(기준이 각각 그 금속이고 화학계가 다르다) |
| 2 | **모든 계면 에너지** (−47 … −405 meV/atom) | 양극·이온·MP 판본이 다르다 |
| 3 | **코팅 11/25종 목록** | Na 화합물만 스크린했다(필터 (i)이 **Li 를 명시적으로 제외**한다!). Li 판은 **존재하지 않는다** |
| 4 | **`NaCl₃`·`NaCl₇` 같은 산화 산물** | Na–Cl 계 고유. Li–Cl 계엔 `LiCl₃` 가 (MP 에) 없다 |
| 5 | **σ 값** (`Table 1`) | 문헌 소환값이고 Na 계 |
| 6 | **P2/O3 라는 양극 분류** | Na 층상산화물 고유(Li 계엔 P2 가 없다) |
| 7 | **"할라이드가 황화물보다 창이 넓다"의 *크기*** | Na₃PS₄ 2.05 ↔ 할라이드 3.76 = **+1.7 V**. Li 계에서 같은 크기인지 **이 논문은 아무 말도 안 한다** |

⚠ **특히 3번을 조심한다**: 필터 (i) 이 *"alkali metals other than sodium (e.g., **Li**, K, Rb, Cs)"* 를 **제외**한다. 즉 **이 논문의 코팅 후보군에 Li 화합물은 원천적으로 없다.** *"이 논문이 `Li₃BO₃` 를 추천했다"* 같은 문장은 **불가능**하다.

### 7-7. 임무 ③ — **할라이드 vs 황화물: 통설이 수치로 어디까지 버티나**

**축 ① 산화 창 (열역학)** — ✅ **통설이 크게 이긴다**

| | 산화 전위 (V vs Na/Na⁺) | 출처 |
|---|---|---|
| 할라이드 7종 | **3.75 – 3.77** | `Table S2` (인쇄값) |
| `Na₃PS₄` | **2.05** | 본문 p.2 |
| `Na₁₁Sn₂PS₁₂` | **1.91** | 본문 p.2 |
| `Na₃SbS₄` | **1.66** | 본문 p.2 |

⇒ **+1.7 … +2.1 V.** 이건 논쟁의 여지가 없다. 동역학 연장까지 넣으면 할라이드 **4.18** vs 황화물(연장값 미보고, `Fig. 1` `figure-read ≈` **2.2**) = **+2.0 V**.

**축 ③ 양극 계면 (화학)** — 🔴 **통설이 반쯤 깨진다**

| 양극 계열 | 할라이드 7종 | 황화물 3종 | **황화물 2종** (`Na₃PS₄` 제외) | 판정 |
|---|---|---|---|---|
| Polyanionic | **−80.6** | −72.5 | **−72.0** | 🔴 **황화물 우세** |
| **P2** | **−141.7** | −226.0 | −188.7 | ✅ 할라이드 우세 (−47) |
| **O3** | **−223.3** | −254.0 | **−204.9** | 🔴 **황화물 2종이 더 낫다** (+18.4) |

🔴🔴 **그리고 범위가 겹친다**: O3 에서 할라이드 7종은 **−194.5 … −255.0**, `Na₃SbS₄` 는 **−200.5**, `Na₁₁Sn₂PS₁₂` 는 **−209.3** ⇒ **두 황화물이 할라이드 분포 한가운데 있다.**
⇒ **"할라이드가 계면에서 낫다" 는 `Na₃PS₄` 한 계가 끌고 가는 서술**이다. 논문은 3종 평균만 인쇄해 이 사실을 덮는다 (§10-4).

**우리 황화물 값과 나란히 놓을 수 있는 축이 있나?** — ⭕ **하나 있다. 단 "값" 이 아니라 "보고량" 이다.**

| | 보고량 | 값 | 놓을 수 있나 |
|---|---|---|---|
| **우리** | `InterfacialReactivity(use_hull_energy=True)`, x 전 구간 최댓값 | `comp1\|LiCoO₂` **−322.7 meV/atom** (min @ x=0.5302) | — |
| **이 논문** | ΔE_D,mutual (식 2) = **대수적으로 동일**, x 전 구간 최댓값 | `Na₃PS₄\|NaNi₀.₅Fe₀.₅O₂` **−405** · `Na₃PS₄\|O3` 평균 **−352** | ⭕ **자릿수·부호 점검까지** |

⇒ ✅ **쓸 수 있는 문장**: *"우리 `Li₆PS₅Cl`‖`LiCoO₂` 의 −0.32 eV/atom 은, 같은 보고량(hull 기준 상호 분해에너지, 혼합비 전 구간 최댓값)으로 계산된 Na 황화물‖O3 층상산화물의 −0.31 … −0.41 eV/atom 과 같은 크기 범위에 있다."*
⛔ **쓰면 안 되는 문장**: *"우리 값이 저들 할라이드(−0.22)보다 나쁘다"* — 이온·양극·MP 판본이 달라 **우열 판정이 아니다**.

### 7-8. 🔴 우리에게 **불리한 것**을 따로 적는다

1. 🔴🔴 **우리 `esw_*.json` 에 `ΔE_D(V)` 열이 없다.**
   저들은 각 breakpoint 에서 **SE 의 분해에너지(eV/atom)** 를 같이 적어 (a) 창 판정을 **에너지로도** 할 수 있고 (b) **`Fig. 2a` 형 프로파일**을 그릴 수 있고 (c) **동역학 연장창**을 정의할 수 있다. 우리는 **전압과 반응식만** 갖고 있어 셋 다 못 한다.
   ⇒ **§H 신규 항목 제안** (§11). ⚠ pymatgen 에서 값을 얻는 것 자체는 어렵지 않으나(hull 거리 계산), **보고량 카드 없이 던지지 않는다**.
2. 🔴 **우리 라벨 오류가 *세 번째* 문헌에서 확인됐다.** `[Zhu15]`(값) → `[Schw21]`(정의) → 이 논문(**구조 + 7종 전수**). ⛔ **더 이상 "정의가 다를 수도 있다" 는 변호가 불가능하다.**
3. ⚠ **계면 축에서 우리가 나은 게 없다.** 보고량이 **대수적으로 같고**, 저들은 **140 셀 × 14 양극**을 냈으며 **코팅까지 스크린**했다. 우리는 `comp1|LiCoO₂` 등 **소수 짝**뿐이다. ⇒ *"우리가 계면 열역학을 한다"* 는 주장은 **범위에서 밀린다**.
   ⭕ **단 우리가 나은 두 칸**: ① **혼합비 x 를 기록한다**(저들은 `Fig. 8` 에서만 읽힘) ② **MP 판본·상 배제 이력을 명시한다**(저들은 미기재).
4. ⚠ **`NaB₃O₅` 를 우리 B₂O₃ 축의 지지 근거로 쓰고 싶어질 텐데, 쓸 수 없다.** 필터가 Li 를 제외했고(§7-6-3), 게다가 **`NaB₃O₅` 의 산화 전위 3.54 V 가 추천 25종 중 최저**라 저자들 자신의 양극 작동창(최고 4.6 V)을 못 버틴다 (§10-5). ⇒ **"붕산염이 양쪽 계면에 동시에 낮은 구동력을 준다" 는 *정성 구조*까지만.**

### 7-9. 임무 ④ — **양극 계면: 슬랩인가 열역학인가**

> **답: 순수 열역학이다. 슬랩은 한 장도 없다.**

| 항목 | 이 논문 | 우리 v5 |
|---|---|---|
| **슬랩 존재** | ⛔ **0** | ✅ 있음 |
| 면지수 (Miller) | ⛔ **0회** | 선언됨 |
| 진공층 | ⛔ **0회** | 선언됨 |
| 이완 자유도 | ⛔ **0회** | 선언됨 |
| 원자수 | ⛔ **0회** | 선언됨 |
| 계면 접합일 `W_ad` | ⛔ **0회** | — (`[Wang22Res]` §J-36 축) |
| 계면 전하이동/Bader | ⛔ **0회** | — |
| 공간전하층 | ⛔ **0회** (`[Haru14]` 계보 인용조차 없다) | — |
| **대신 있는 것** | **pseudo-binary ΔE_D,mutual, 혼합비 x 전 구간** | 우리도 있음(`interface_reactivity`) |
| 저자 자인 | ✅ *"does not explicitly capture **atomic-scale interface structures** or kinetic barriers"* | — |

**어느 양극인가**: 폴리음이온 2 + P2 6 + O3 6 = **14종**(§3g 전수). 전부 **문헌에서 고른 실험 조성**이고 MP 엔트리로 계산했다. ⚠ `Na₀.₆₇Mn₀.₆₅Co₀.₂Ni₀.₁₅O₂` 같은 **비화학량론 다원계를 "hull 위" 로 가정**한 것(§5d)이 방법의 가장 약한 고리다.
**계면 반응 생성물**: §6-2 의 세 채널 (①음이온 교환 ②Cl → `NaClO₄` 산화 ③TM 염화). `Table S4` 98행 전수가 §3d 주석에 있다.

⇒ ⛔ **우리 v5 기하와 겹치는 축이 없다.** 이 논문은 **§J 의 `🔧 방법 원전` 블록**으로만 들어간다 (§11).

---

## 8. DFT/계산 방법 ★ — 임무 ⑤ 전수

> ⚠ **먼저 못박는다: 이 논문은 자체 DFT 를 한 줄도 돌리지 않았다.** 아래 "값" 칸의 ⛔ 는 **논문의 누락이 아니라 구조**다.

| 항목 | 이 논문 | 우리 |
|---|---|---|
| **코드 (전자구조)** | ⛔ **없음** — MP 의 사전계산값 사용 (refs 30–32) | **Quantum ESPRESSO** |
| **범함수** | ⛔ **명시 없음** (MP 이므로 PBE(+U) 로 **추정**되지만 **논문에 활자 없음**) | PBE |
| **vdW** | ⛔ 없음/미기재 | 없음 |
| **pseudo/PAW** | ⛔ 미기재 | 명시 |
| **ecut** | ⛔ **미기재** | 명시 |
| **k-점** | ⛔ **미기재** | 명시 |
| **슈퍼셀/원자수** | ⛔ **미기재** | 명시 |
| **DFT+U** | ⛔ **미기재** — ⚠ **Ti·V·Mn·Fe·Co·Ni·Nb·Ta 를 잔뜩 다루면서** | — |
| **스핀** | ⛔ **미기재** — ⚠ **층상 TM 산화물 14종이 전부 열린 껍질·산화환원 활성** | — |
| **무질서 처리** | ⛔ **한 줄도 없다** — `Na₀.₆₇Mn₀.₆₅Co₀.₂Ni₀.₁₅O₂` 같은 **다원 무질서 조성**을 어떻게 잡았는지 **0건**. SQS·enumeration·앙상블 **0** | comp1/modelc 배열 선언 |
| **온도/엔트로피** | **0 K**, 포논·진동엔트로피·형상엔트로피 **0건**. ⚠ **`Na₀.₆₇…` 같은 조성은 형상엔트로피가 본질인데 무시** | 동일(0 K) |
| **압력** | **0** (언급 0회) | 동일 |
| **ESW 방법** | **Na grand-potential 상도** (pymatgen), refs 26/33/34 = Nolan 2021 · Zhu–He–Mo 2016 · Nolan–Liu–Mo 2019 | pymatgen `get_element_profile` |
| **ESW 판정** | **ΔE_D = 0 구간** (+ `Na uptake = 0` 중복) | **Li 교환 0 구간** (🔴 라벨 오류 정정 중) |
| **동역학 보정** | ✅ **`ΔE_D > −25 meV/atom` 문턱** (⚠ 근거 0) | ❌ 없음 |
| **계면 방법** | **pseudo-binary** 식 (1)–(2), 혼합비 x 전 구간 최댓값 | `InterfacialReactivity(use_hull_energy=True)`, **같은 양** |
| **상도 출처** | **Materials Project** (refs 30–32) | MP2026 |
| **상도 판본** | 🔴 **미기재.** 스냅샷 날짜 0 · 엔트리 id 는 **코팅 표에만** 있고(`mp-6397` 등) **SE·양극에는 없다** · MP2020Compatibility 여부 0 | ✅ **MP2026**, 신 id 기록 |
| **hull 기준** | **`E_hull = 0` 만** (코팅). SE·양극은 *"assumed to be … on the convex hull"* | 상 배제 이력 명시(`LiS₄`·`SCl₃`·`Li₅PS₄Cl₂`) |
| **ML** | **PCA + K-means** (scikit-learn 추정, **버전·k 선택법·random seed·표준화 여부 전부 미기재**) | — |
| **군집 수 k=4** | 🔴 **선택 근거 0** — elbow·silhouette·BIC **0건**. *"distinctly separated the dataset into four chemically meaningful groups"* 가 전부 | — |
| **AIMD / MLIP / MD** | ⛔ **0건** | UMA-s-1p1 MLIP-MD |
| **NEB / 전이상태 / 장벽** | ⛔ **0건** — 논문의 3번 논거가 *"kinetically suppressed"* 인데 | — |
| **DOS / PDOS / Bader / COHP / ELF / 포논 / 탄성 / BVSE** | ⛔ **전부 0건** | 전부 있음 |
| **밴드갭** | MP 값을 **`< 0.5 eV` 제외 필터로만** 사용. 자체 계산 0 | fixed-occ nscf VBM/CBM |
| **자체 실험** | ⛔ **0건**. `Table 1`(σ)·`Table S1`(양극) 전부 문헌 소환값 | — |
| **실험 대조** | 🔴 **정량 대조 0건.** 토론에 *"Good agreement has been reported between reaction-energy-based interfacial screening and experimental observations … including Na-sulfide and Li-chloride SEs [27, 28]"* 한 문장뿐이고 **자기 결과와 실험을 직접 맞춰 보지 않았다** | — |
| **재현성** | 🔴 리포지터리·코드·중간데이터 **0**. 289종 목록은 이름만(`Table S5`), 수치 없음 | — |
| **계산자원** | KISTI **KSC-2025-CRE-0062** (⚠ DFT 를 안 돌렸는데 슈퍼컴 — 12 800 × 21 pymatgen 상도가 무겁긴 하다) | KISTI/kgy/gabia |

---

## 9. Figure set ★

> **크로핑 17장 = 그림 10장(본문 `Fig. 1`–`8` + SI `Fig. S1`–`S2`) + 표 7장(`Table 1` + `Table S1`–`S7`).** 이 중 **그림 7장 실독**. 표 7장(`tab_*.png`)은 **PDF 텍스트로** 읽었다(그게 정확하다).
> **실독 7장**: `Fig. 1` · `Fig. 2` · `Fig. 3` · `Fig. 5` · `Fig. 8` · `Fig. S1` · `Fig. S2`.
> **미열람 3장**: `Fig. 4`(워크플로 도식 — 내용이 본문 p.4 와 `Methods` p.8 에 **숫자까지 전부 활자로** 있다) · `Fig. 6`(엄격 11종 heatmap) · `Fig. 7`(실용 25종 heatmap). **이유**: `Fig. 6`·`Fig. 7` 의 셀값은 본문이 범위(**−20 … −40 meV/atom**)로 주고 개별 코팅의 전위·산물은 `Table S6`·`Table S7` 텍스트에 전수 있으며, **우리 축(Li 아르지로다이트)에 값이 넘어오지 않는다**. ⚠ 다만 **코팅 개별 셀값은 이 digest 에 없다** — 필요하면 그 두 장을 추가로 읽어야 한다(정직하게 기록).

| Fig | 내용 | 우리 활용 |
|---|---|---|
| **1** | ✅**실독** 10 SE + 양극 작동창 가로막대, x = 0–5 V vs Na/Na⁺. 실선 = 열역학 창, **파선 상자 = 동역학 연장창** | 🔴 **표지 그림.** 할라이드 7종 산화 끝이 **한 줄로 정렬**(= `NaCl₃` 독점)되는 것이 눈으로 보인다. 황화물 환원한계는 **여기서만** 읽힌다(`figure-read ≈` `Na₃PS₄` 1.25 · `Na₁₁Sn₂PS₁₂` 1.2 · `Na₃SbS₄` 1.63). ⚠ **`Na₃SbS₄` 창이 `figure-read ≈` 0.05 V** 인데 본문 서술 없음 |
| **2a–d** | ✅**실독** ΔE_D vs V, 4계. (a) 에 `← Reduction` / `Oxidation →` / **`ESW`** 라벨 | ⭐ **창 = ΔE_D 0 평탄** 의 시각 정본. (a) 가 가장 가파르고 (d) 가 가장 완만 = **§3c 의 −0.148 vs −0.055 eV/V 를 눈으로 확인** |
| **2e–h** | ✅**실독** **`Na uptake per f.u.`** vs V, 계단. (e) 에 `← Sodiation` / `Desodiation →` | 🔴🔴🔴 **이 digest 의 핵심 그림.** **0 평탄 바로 왼쪽 계단이 4계 전부 양수**(1 / 2.5 / 1.5 / 0.85) ⇒ **`max(V\|evo>0)` 이 한 계단 아래를 준다는 직접 증거.** ⚠ **(b),(f) 라벨이 "`Na₂TaCl₆`" 오기** |
| **3** | ✅**실독** 10 SE × 14 양극 ΔE_D,mutual heatmap, **셀마다 숫자 인쇄**, 컬러바 −400…0 | 🔴 **황화물 3행이 `Table S4` 에 없다 — 이 그림이 유일 출처.** 할라이드 98셀을 `Table S4` 와 **전수 대조 98/98 일치** ⇒ 판독 신뢰. 🔴 **`Na₃SbS₄`·`Na₁₁Sn₂PS₁₂` 가 O3 에서 할라이드 범위 안**(§10-4) |
| **4** | ⛔**미열람** 스크리닝 워크플로 도식 | 12 800 → 7 995 → 289 → 11/25 의 숫자가 **본문·Methods 에 전부 활자**로 있다 |
| **5a** | ✅**실독** PCA 산점, 4군 (분홍 A / 주황 B / 하늘 C / 초록 D) | ⚠ 축 라벨 **`Principle component`** 오기. Group D 가 오른쪽으로 길게 뻗음 = **할로겐화물 군** |
| **5b** | ✅**실독** 군집 평균 heatmap 4×21, **셀 숫자 인쇄** | 🔴🔴 **본문의 Group A 서술이 값과 뒤바뀐다**(SE −94.8 을 *"slightly negative"* 라 씀). 🔴 **최종 11종이 Group B 10 + Group A 1 이고, 선별은 숫자 문턱이 한다 ⇒ 군집은 게이트가 아니다**(§10-5) |
| **6** | ⛔**미열람** 엄격 11종 × (HSE·양극) heatmap | 본문이 범위(−20 … −40)로 줌 · 전위/산물은 `Table S6` 텍스트 |
| **7** | ⛔**미열람** 실용 25종 heatmap | 동일. ⚠ **개별 셀값은 이 digest 에 없다** |
| **8** | ✅**실독** ΔE_D,mutual vs **혼합비 x**, 6패널 × 3곡선 | 🔴🔴 **보고값이 "x 최댓값" 이고 그 x 가 짝마다 다르다**(HSE‖코팅 `figure-read ≈` **x 0.07** / 양극‖HSE **x 0.35**) ⇒ ⛔ *"계면상 형성에너지"* 로 읽으면 안 된다. ⭐ 우리는 x 를 기록한다 = **우리가 나은 칸** |
| **S1** | ✅**실독** 나머지 3계의 `Fig. 2` 판 | ✅ **7/7 전수에서 버그 구조 재현.** 0 평탄 왼쪽 계단 = 0.3 / 0.7 / 1.5 |
| **S2** | ✅**실독** ΔE_D ↔ ΔE_D,mutual 도해 (눈금 없음) | ⭐ **식 (2) = `use_hull_energy=True`** 의 그림 설명. 🔴 **그런데 이 논문에선 세 부류가 전부 hull 위라 보정이 항상 0 이다**(우리 유도, §5d) |
| **Table 1** | (PDF 텍스트) 7 HSE 의 σ + 원전 | ⚠ *"~1 mS cm⁻¹"* 은 7종 중 3종만. `Na₂ZrCl₆` = **0.018** |
| **Table S1** | (PDF 텍스트) 양극 14종 작동창·용량 | 🔑 `Fig. 1` 회색막대 = 이 표의 합집합(1.5–4.6 V) |
| **Table S2** | (PDF 텍스트) **7종 창 + 양 끝 평형상** | 🔴🔴 **임무 ①의 정본.** ⚠ *"환원 전위에서의 평형상"* 은 **아래 계단**의 산물이다(§4-4) |
| **Table S3** | (PDF 텍스트) **전 분해 사다리 + ΔE_D 열** | 🔴🔴🔴 **이 digest 에서 가장 값진 표.** 우리 버그를 7/7 에서 재현하게 해 주고, **§3c 동역학 연장창 레시피를 검산**하게 해 준다 |
| **Table S4** | (PDF 텍스트) 할라이드 7 × 양극 14 = **98행** 반응에너지 + 산물 | §3d·§6-2. 🔴 **황화물 42행 없음** |
| **Table S5** | (PDF 텍스트) 289종의 A–D 군집 소속 | 🔴 **수치 없이 이름만.** 최종 11종의 소속 확인용으로만 씀 |
| **Table S6** | (PDF 텍스트) 엄격 11종 전위·산물 + MP-ID | §3e |
| **Table S7** | (PDF 텍스트) 실용 25종 전위·산물 + MP-ID | §3e. 🔴 **`Na₂B₈O₁₃` 행이 `Table S6` 과 어긋난다**(§10-6) |

---

## 10. 비판 — 이 논문의 약한 곳 ★ (임무 ⑥ 포함)

**10-1. 🔴🔴 논문의 두 번째 기둥(동역학)이 문턱 하나로 서 있다.**
*"kinetic overpotentials during oxidation can effectively extend the practical oxidative stability"* 가 **4 V 급 양극을 쓸 수 있다는 결론 전체를 떠받친다**. 그런데 그 동역학의 내용은 **`ΔE_D > −25 meV/atom` 이라는 숫자 하나**다.
- **25 meV/atom 의 근거 문장이 없다.** 문헌 인용도 없다. (참고로 25 meV ≈ **kT at 290 K** 인데, 그렇다면 *atom* 당이 아니라 *반응* 당이어야 말이 되고, 논문은 어느 쪽인지도 안 밝힌다.)
- **장벽 계산 0건** — NEB·전이상태·핵생성 **0**.
- **과전압 실측 대조 0건** — 저들이 인용한 ref 23/24 의 셀 데이터와 맞춰 보지 않았다.
- **환원 쪽 연장값은 `Fig. 1` 에 그려 놓고 숫자를 안 준다.**
⛔ **인용 금지**: *"이 논문이 할라이드의 실효 산화 한계가 4.1 V 임을 보였다"* — **보이지 않았다. 열역학 한계 3.76 V 에 근거 없는 문턱을 얹어 얻은 수**다.

**10-2. 🔴 결론 절이 본문의 단서를 지운다.**
- 본문 p.2: *"the intrinsic oxidation potential **does not fully cover** the operating voltage range of 4 V-class cathodes"*
- 결론 p.8: *"HSEs intrinsically exhibit wide electrochemical stability windows that **broadly cover the operating potential range of cathodes**"*
⇒ **같은 논문 안에서 반대로 쓴다.** `Table S1` 의 최고 컷오프는 **4.6 V**(`Na₀.₆Mn₀.₈Li₀.₂O₂`)이고 열역학 산화 한계는 **3.76 V** 다. ⛔ **결론 문장 쪽을 인용하면 안 된다.**

**10-3. 🔴 비정질·유리 전해질을 결정 MP 엔트리로 계산했다.**
`NaAlCl₂.₅O₀.₇₅`(ref 21 = *Nature Energy* **"Inorganic **glass** electrolytes with polymer-like viscoelasticity"*) 와 `Na₀.₅ZrCl₄F₀.₅`(ref 23 = *"**Fluorinated amorphous** halides"*) 는 **원전 제목에 유리·비정질이 박혀 있다.** 그런데 계산은 결정상 hull 로 했다. 저자도 토론에서 자인하지만 **자인이 `Table S2` 값을 고쳐 주지는 않는다.**
⚠ **그리고 이 논문의 헤드라인 주장(F 치환 3.92 → 4.18 V)이 하필 그 비정질 계**다.

**10-4. 🔴🔴 "할라이드 > 황화물" 이 평균으로 덮였다 — 임무 ⑥의 핵심.**
본문은 황화물을 **3종 평균**(P2 −230 / O3 −250)으로만 제시한다. 그런데 `Fig. 3` 을 풀면 (우리 산수):
- **`Na₃PS₄` 를 빼면 황화물 평균이 P2 −188.7 / O3 −204.9 로 뛴다.**
- **O3 에서 황화물 2종(−200.5, −209.3)이 할라이드 7종 범위(−194.5 … −255.0) 안에 들어온다.**
- **Polyanionic 에서는 황화물(−72.5)이 할라이드(−80.6)보다 낫고, 140 셀 최선값이 `Na₃PS₄`‖`Na₃V₂(PO₄)₃` = −47 이다.**
⇒ ⛔ *"할라이드가 황화물보다 양극 계면에서 안정하다"* 로 옮기면 **안 된다**. 정확히는 **"P2 층상산화물에 대해서만, 그리고 `Na₃PS₄` 대비 가장 크게"** 다.

**10-5. 🔴 PCA–K-means 가 워크플로 상자를 차지하지만 아무것도 거르지 않는다.**
- 최종 11종 = **Group B 10 + Group A 1**, 실용 25종 = **A 와 B 혼합** (우리 `Table S5` 대조).
- 실제 게이트는 *"평균 < 50, 최대 < 60"* / *"최대 < 110"* 이라는 **같은 ΔE_D,mutual 에 건 숫자 문턱**이다.
- **k = 4 의 선택 근거 0건**(elbow·silhouette 없음), **표준화·random seed·PCA 설명분산 전부 미기재**.
- `Fig. 5b` 의 **Group A 서술이 값과 뒤바뀐다**(§5g).
⇒ ⚠ **`[Park26ML]` §J-22-3 과 같은 구조의 2호 사례**: *"선택 기준이 실제로는 하나뿐이었다."*
**같은 절의 두 번째 문제**: `Fig. S2` 가 설명하는 mutual 보정이 **이 논문 안에서 한 번도 작동하지 않는다** — 세 부류(SE·양극·코팅)를 전부 hull 위로 두었기 때문에 식 (2) ≡ 식 (1) 이다(우리 유도, §5d). 특히 **`Na₀.₆₇Mn₀.₆₅Co₀.₂Ni₀.₁₅O₂` 같은 다원 비화학량론 조성을 "hull 위" 로 *가정*한 것**이 결과 전체에 들어 있다.
**세 번째**: 대표 코팅 **`NaB₃O₅` 의 산화 전위가 3.54 V** 로 25종 중 최저라 **4.4–4.6 V 양극 작동창을 코팅 자신이 못 버틴다.** 스크리닝 기준이 *"산화 > 3.5 V"* 라 통과했을 뿐이고, 저자들 자신이 `Methods` 에서 *"enforcing this full window … would eliminate most candidates"* 라며 기준을 낮춘 것을 인정한다. ⇒ ⛔ **`NaB₃O₅` 를 "고전압 코팅" 이라 부르면 안 된다.**

**10-6. ⚠ 내부 불일치·표기 오류 (전수).**
1. **`NaTaCl₆` 환원 전위**: `Table S2` **2.18** vs `Table S3` **2.17** vs 본문 *"near 2.18"*.
2. **`Fig. 2b,f` 의 그림 안 라벨이 "`Na₂TaCl₆`"** — 다른 모든 곳은 `NaTaCl₆`.
3. **`Table S3` 의 `Na₀.₅ZrCl₄F₀.₅` 에 1.04 V 행이 두 번** (`Na₂ZrF₆, NaCl, Zr` / `Na₂ZrF₆, ZrCl, NaCl`, 둘 다 −0.209) — 중복인지 동시평형인지 구분 불가.
4. **`Na₂B₈O₁₃` 이 `Table S6` 과 `Table S7` 에서 다르다**: 환원 산물 `B₆O, **NaB₃O₅**`(S6) ↔ `B₆O, **NaBO₂**`(S7) · 산화 전위 **4.29**(S6) ↔ **4.30**(S7) · 산화 산물 `**B₂O₃, O₂**`(S6) ↔ `**B₆O, Na₃B₇O₁₂**`(S7). 🔴 **S7 의 산화 산물은 `NaB₃O₅` 행의 *환원* 산물과 글자까지 같다 = 복붙 오류**이고, 산화 반응에서 `O₂` 없이 `B₆O`(환원된 붕소 준산화물)가 나오는 것은 **화학적으로 불가능**하다. ⇒ ⛔ **`Table S7` 의 `Na₂B₈O₁₃` 산화 행 인용 금지.**
5. **`Na₆Mg(SO₄)₄` 산화 전위**: `Table S6` **4.11** ↔ `Table S7` **4.12**.
6. **필터 (iii) 의 서술이 세 번 다르다**: 본문 p.4 *"reduction potentials **below** 2.5 V and oxidation potentials **above** 3.5 V"*(= 유지 조건) / Methods (iii) *"reduction potentials **> 2.5 V or** oxidation potentials **lower than** 3.5 V were **discarded**"*(= 같은 뜻) / Methods 뒷 문단 *"Electrochemical stability thresholds of **> 2.5 V (reduction) and < 3.5 V (oxidation)** were **applied as screening criteria**"*(= 읽으면 **반대**). 세 번째 문장이 부호를 흐린다.
7. **완화 문턱의 부호 표현이 틀렸다**: *"relaxing the ΔE_D,mutual threshold to a maximum value **below −110 meV/atom**"* — *"below −110"* 은 더 음수라는 뜻이라 **완화가 아니라 강화**다. 뜻은 `|max| < 110`.
8. **`Fig. 5a` 축이 `Principle component`** (← *Principal*).
9. **`Table 1` 캡션 *"high ionic conductivities"* + 본문 *"~1 mS cm⁻¹"*** 인데 `Na₂ZrCl₆` **0.018** · `Na₀.₅ZrCl₄F₀.₅` **0.11** · `Na₀.₇La₀.₇Zr₀.₃Cl₄` **0.29** = **4종이 1/3 미만**.
10. **본문이 `Fig. 8` 의 `NaTaOCl₄` 쪽 양극‖코팅 값을 안 적는다** — *"substantially lowered"* 로만 쓰고 숫자는 `Fig. 8d–f` 에서만 읽힌다.
11. **Acknowledgements 와 Funding 절이 글자까지 동일한 중복**이다.

**10-7. 🔴 무질서·스핀·U 가 전부 침묵인데 대상이 층상 TM 산화물 14종이다.**
`Na₀.₆₇Mn₀.₆₅Co₀.₂Ni₀.₁₅O₂`·`NaNi₀.₃₃Fe₀.₃₃Mn₀.₃₃O₂` 같은 조성은 **양이온 무질서 + 열린 껍질 + 산화환원 활성** 셋을 동시에 갖는다. 우리 보고량 규율(`kb/templates/estimand_card.md` §2)이 *"admissible state 가 여럿인데 선택·집계 규칙이 없으면 스칼라 보고량은 정의되지 않는다"* 고 하는 **위험신호 3개가 전부 켜져 있다.** 그런데 논문에는 스핀·U·배열·집계 규칙이 **한 줄도 없다**(MP 에 맡겼고 MP 가 무엇을 했는지도 안 적는다).
⇒ ⚠ **−131 과 −144 의 13 meV/atom 차이로 양극 서열을 읽으면 안 된다.**

**10-8. ⚠ 실험 대조가 한 문장뿐이고 그것도 남의 계다.**
*"Good agreement has been reported between reaction-energy-based interfacial screening and experimental observations … including Na-sulfide and Li-chloride SEs [27, 28]"* — **자기 인용 두 편**이고, **이 논문의 7종 할라이드에 대한 실험 대조는 0건**이다. 저자도 *"experimental studies on Na-halide SEs remain limited"* 라 적는다. ⇒ ⛔ *"계산이 실험과 잘 맞았다"* 로 옮기면 안 된다.

**10-9. ⚠ 코팅 후보에 수화물·수산화물·Cd 화합물이 섞여 있다.**
엄격 11종 중 **`NaAlH₂CO₅`·`Na₂Al₂Si₃(HO₃)₄`·`NaB₅(H₂O₅)₂` 3종이 H 함유**, **`Na₆CdCl₈` 은 Cd**. 논문은 HSE 의 흡습성만 걱정하고 **자기 코팅 후보의 수분·독성은 언급하지 않는다.** 실용 25종에서 조용히 빠지는데 **이유를 적지 않는다**.

**10-10. ⚠ 데이터 공개가 사실상 없다.**
*"available in the supplementary material"* 가 Data Availability 전부다. **289종의 ΔE_D,mutual 수치는 어디에도 없고**(`Table S5` 는 이름만), 12 800 → 7 995 의 중간 목록도, 코드도, MP 스냅샷도 없다. ⇒ **이 스크리닝은 재현 불가능하다.**

---

## 11. 우리 원장 매핑 (요약표)

| 우리 원장 | 이 논문이 하는 일 | 조치 |
|---|---|---|
| `db/properties/citation_hazards.json` `HZ-esw-reduction-limit-label` (**BLOCKED**) | ✅✅ **세 번째 외부 눈금.** 7종 전수에서 `max(V\|evo>0)` 이 한 계단 아래를 준다는 것을 **사다리 구조로** 보여 준다 | **판정 유지 + 근거 보강** (재판정 불필요). `evidence` 에 이 digest §3b·§4-3 추가 제안 |
| `tools/oxidation/esw_cascade_batch.py:417–419, 435` | 🔴 `red = max(V\|evo>0)` · `ocv = min(V\|\|evo\|≤1e-6)` · `window_V = ox − red` | ⭐⭐ **`ocv` 가 이미 정답이다** ⇒ **재계산 없이 `window_V = ox − ocv` 로 유도 + 두 필드 rename** 제안 (§7-2). ⚠ 전제: **교환-0 행이 2개 이상인 계가 cascade 에 있는지 먼저 센다** |
| `tools/oxidation/constrained_esw.py:91–93` | 동일 버그 | 동일 제안 |
| `our_dft_baseline.md` L20 *"환원 한계 1.242 V / OCV 1.717 V"* | 🔴 **라벨이 뒤바뀌어 있다** (세 번째 확인) | **`[Schw21]` digest §7-8 의 제안과 동일**. 새 제안 없음 (중복 방지) |
| `db/properties/esw_lis4excluded.json` | 🔴 **`ΔE_D(V)` 열이 없다** — 저들 `Table S3` 의 2번째 열 | **§H 신규 항목 제안** (§12-3). ⛔ 던지기 전 보고량 카드 |
| `db/properties/oxidation_stability.json` `nd2o3_interface_reactivity` | ✅ **보고량이 같다** (식 2 ≡ `use_hull_energy=True`, 우리 유도) | **§J 블록에 방법 대조로만.** ⛔ 값 대조 금지 |
| `comparison_vs_ours.md` §B① 축 명명 규율 (*"Cl 은 onset 이 아니라 분해 양·산물·계면에 작용"*) | ⭐⭐ **이온종 독립 외부 실증** — Na 할라이드에서 **Cl→F 가 onset 을 +0.01 V 밖에 못 움직이고 onset 이후 기울기를 2.7배 바꾼다** | **§J 블록에 넣는다** (§B 4축 표는 **아님** — Na 값이라 행이 전부 n/a) |
| `comparison_vs_ours.md` §H (*"층② 없음"*) | 이 논문도 **층② 없다** — 층①만 + 문턱 완화판 | 변화 없음 |
| `papers/schwietert2021_…md` §12-4 (*"기계가 읽을 수 있는 방향 표지는 부호 있는 교환량뿐"*) | ✅✅ **그 처방을 실제로 구현한 논문이다** (`Na uptake per f.u.` 그림 축) | **§J 블록에 "정례" 로 기록** — `[Schw21]` 은 반례, 이 편은 정례 |
| `db/governance/decisions.json` | *"환원 한계" 보고량 정의가 원장에 없다* | `[Schw21]` digest 가 이미 `estimand_card` 사유를 올림. **중복 제안 안 함** |
| `litdb/properties/` | ⛔ **디렉터리 없음** | 갱신 대상 없음 |
| `litdb/talks/` 인입 대기열 | 이 논문 **없음** (grep 0건) | 역링크 없음 |

---

## 12. 적용 인사이트 ★

1. **🔴🔴 `HZ-esw-reduction-limit-label` 은 이제 세 눈금으로 닫힌다 — 그리고 수정이 싸다.**
   `[Zhu15]`(값) → `[Schw21]`(정의) → **이 논문(구조 + 7종 전수)**. 그리고 §7-2 가 보여 주듯 **우리 도구가 이미 정답(`ocv_V`)을 계산하고 있다.** ⇒ **cascade 356 행 재계산 없이 필드 rename + `window_V` 재유도로 끝난다.** 이게 이 digest 의 실질 산출물 1호다.
2. **⭐⭐ 산화 축 명명 규율의 이온종 독립 실증을 얻었다.**
   우리: `comp1`→`modelc` 에서 **Cl 증량이 onset 을 안 움직인다**(2.256 V 고정, S²⁻-limited).
   저들: `Na₂ZrCl₆`→`Na₀.₅ZrCl₄F₀.₅` 에서 **F 치환이 onset 을 +0.01 V 밖에 안 움직이고**(`NaCl₃`-limited), 대신 **onset 이후 ΔE_D 기울기를 −0.148 → −0.055 eV/V 로 2.7배 완만하게** 만든다(우리 산수).
   ⇒ **"할로겐 치환은 축①을 안 건드리고 축②·③을 건드린다" 가 Li-황화물과 Na-할라이드 양쪽에서 성립한다.** 이건 원고 §B 서론에 쓸 수 있는 외부 문장이다.
3. **⭐ 우리 ESW 출력에 `ΔE_D(V)` 열을 붙일 이유가 생겼다 (§H 신규).**
   붙이면 세 가지가 한꺼번에 열린다: (a) 창 판정을 **에너지로도** 교차확인(라벨 버그 재발 방지) (b) **`Fig. 2a` 형 프로파일 그림** (c) **문턱 기반 동역학 연장창**.
   ⛔ **단 25 meV/atom 을 그대로 베끼지 않는다** — 근거가 없다. 우리가 문턱을 쓰려면 **`[Du22LMR]`·`[Wei23LNO]`·`[Deng26PS]` 의 실측 과전압(0.05–0.45 V)에서 역산**하는 쪽이 정직하다. ⚠ **보고량 카드 먼저**(`kb/templates/estimand_card.md`) — *"동역학 연장 한계 ≡ ΔE_D(V) 가 문턱 τ 를 지나는 전압, τ 는 …로 정한다"* 를 결과 보기 전에 적는다.
4. **⭐ 방향 표기의 *정례*를 확보했다.** `[Schw21]` 은 방향을 손으로 적어 뒤집혔고(반례), 이 논문은 **부호 있는 교환량을 그림의 축으로 박아** 뒤집힐 수가 없다(정례). ⇒ 우리 `tools/oxidation/*.py` 가 그림을 낼 때 **`Li uptake per f.u.` 계단을 ΔE_D 프로파일과 같은 x축으로 나란히** 그리는 것을 표준으로 삼는다. **둘이 어긋나면 눈에 보인다.**
5. **⭐ 계면 보고량이 이미 같다는 것을 확인했다** (식 2 ≡ `use_hull_energy=True`, 우리 대수 유도). ⇒ 원고에서 우리 `interface_reactivity` 를 소개할 때 **"Xiao 2019 / Richards 2016 / Zhu–He–Mo 2016 계보의 표준 보고량"** 이라고 쓸 근거가 하나 더 생겼다. ⛔ **값은 여전히 안 섞는다.**
6. **⭐ "반응이 만들 상을 미리 깔아라" 라는 코팅 원리** — 할라이드‖폴리음이온의 산물이 `NaZr₂(PO₄)₃` 이고, 그 `NaZr₂(PO₄)₃` 가 최종 코팅 추천에 들어 있다(§6-2). **논문이 이 연결을 안 짓는다.** 우리 축으로 옮기면: **`comp1|LiCoO₂` 산물 5종(`Li₃PO₄`·`Li₂SO₄`·`Li₂S`·`LiCl`·`Co₉S₈`) 중 안정한 것을 코팅 후보로 되먹임**하는 검사 — `Li₃PO₄` 는 실제로 우리 코팅 표에 있다. **한 줄 산수로 확인 가능한 가설**이다.
7. **⛔ 쓰지 않을 것**: 저들 전압·계면 에너지 **절대값** · 코팅 11/25종 목록(**Li 가 원천 제외**) · *"할라이드가 황화물보다 계면이 낫다"*(§10-4) · *"실효 산화 4.1 V"*(§10-1) · 결론 절의 *"broadly cover"*(§10-2) · `Table S7` 의 `Na₂B₈O₁₃` 산화 행(§10-6-4) · `NaB₃O₅` 를 *"고전압 코팅"* 으로(§10-5).

---

## 13. 인용 가능 문장 (영문 초안)

> **① 창의 조작적 정의 (안전 · 우리 규율에 직결)** — "Jang et al. define the electrochemical stability window operationally as the potential interval over which the decomposition energy of the electrolyte is identically zero, its two bounds being the reduction and oxidation potentials; equivalently, it is the plateau over which the alkali-ion uptake per formula unit is zero [Jang 2026]."

> **② 우리 정정의 외부 근거 (필수 동반)** — "The same convention is evident in their tabulated decomposition ladders, where the reduction bound carries the electrolyte itself as the equilibrium assemblage and the first reduction products appear one rung below (e.g. 1.69 V vs 1.57 V for `Na₂ZrCl₆`); selecting the highest potential with non-zero ion exchange therefore underestimates the reduction bound by 0.11–1.10 V across their seven electrolytes [Jang 2026]."

> **③ 음이온이 산화 변을 독점한다 (구조만, 값 없음)** — "For all seven sodium halide electrolytes examined the oxidation limit falls within 3.75–3.77 V vs Na/Na⁺ because oxidative decomposition invariably proceeds through `NaCl₃` formation, so the window's anodic bound is set by the halide rather than by the central metal [Jang 2026]."

> **④ 할로겐 치환이 onset 을 안 움직인다 (우리 §B 축 명명과 짝)** — "Fluorine substitution in `Na₂ZrCl₆` shifts the thermodynamic oxidation limit by only 0.01 V (3.75 → 3.76 V vs Na/Na⁺); the reported improvement from 3.92 to 4.18 V arises entirely from the shallower growth of the decomposition energy beyond onset under a −25 meV/atom kinetic criterion [Jang 2026]."

> **⑤ 창이 넓다 ≠ 계면이 좋다 (논문의 주제문)** — "Despite intrinsically wide windows, sodium halide electrolytes show mutual decomposition reaction energies of about −80, −140 and −220 meV/atom against polyanionic, P2-type and O3-type sodium cathodes respectively, i.e. a substantial thermodynamic driving force for interfacial reaction [Jang 2026]."

> **⑥ 한정 (필수 동반 1)** — "These reaction energies are maxima taken over the pseudo-binary mixing ratio and, as the authors state, 'should be interpreted as relative indicators of thermodynamic compatibility, rather than as direct predictions of interfacial reaction pathways or decomposition products' [Jang 2026]."

> **⑦ 한정 (필수 동반 2)** — "The analysis uses bulk crystalline Materials-Project data only; no interface slab, kinetic barrier, amorphous phase or finite-temperature effect is included, as the authors note [Jang 2026]."

> **⑧ 우리 쪽 자리매김 (값 이식 없음)** — "Our interfacial reactivity for `Li₆PS₅Cl`‖`LiCoO₂` (−0.32 eV/atom, hull-referenced pseudo-binary maximum) is computed with the same estimand as Equation (2) of Jang et al.; the two sets of numbers are not interchangeable, since theirs refer to sodium chemistry, different cathodes and an unspecified Materials-Project vintage."

---

## 14. 주의 / 한계 (인용 규율)

1. ⛔⛔ **전압·계면에너지 절대값을 우리 Li 표에 옮기지 않는다.** **vs Na/Na⁺** 기준이고, Li 기준으로 **상수 오프셋 변환되지 않는다**.
2. ⛔ **"실효 산화 한계 4.1 V" 를 이 논문의 계산 결과로 쓰지 않는다** — 근거 없는 25 meV/atom 문턱의 산물이다 (§10-1).
3. ⛔ **결론 절의 *"broadly cover the operating potential range of cathodes"* 를 인용하지 않는다** — 본문이 반대로 적는다 (§10-2).
4. ⛔ **"할라이드가 황화물보다 양극 계면에서 안정하다" 로 옮기지 않는다** — P2 에서만 성립하고 O3·폴리음이온에서는 역전된다 (§10-4).
5. ⛔ **코팅 11/25종 목록을 우리 Li 축에 옮기지 않는다** — 스크리닝 필터가 **Li 를 명시적으로 제외**했다.
6. ⛔ **`NaB₃O₅` 를 "고전압 코팅" 이라 부르지 않는다** — 자기 산화 전위가 3.54 V 다 (§10-5).
7. ⛔ **`Table S7` 의 `Na₂B₈O₁₃` 산화 행(4.30 V / `B₆O, Na₃B₇O₁₂`)을 인용하지 않는다** — `Table S6` 과 어긋나고 화학적으로 불가능하다 (§10-6-4).
8. ⛔ **`Table S3` 의 "평형상" 을 `Table S2` 의 "평형상" 과 같은 것으로 읽지 않는다** — **관례가 다르다** (§4-4).
9. ⛔ **양극 간 10–20 meV/atom 차이로 서열을 읽지 않는다** — 무질서·스핀·U 처리가 전부 미기재다 (§10-7).
10. ⛔ **"계산이 실험과 잘 맞았다" 로 옮기지 않는다** — **이 논문의 7종에 대한 실험 대조는 0건**이다 (§10-8).
11. ⚠ **`figure-read ≈` 표시한 값**(`Fig. 1` 의 황화물 환원 한계·`Na₃SbS₄` 창 폭 · `Fig. 2e–h`·`Fig. S1d–f` 계단 높이 · `Fig. 8` 의 x 위치와 `NaTaOCl₄` 양극‖코팅 값)은 **그림에서 읽은 것**이다. `Table S2`·`Table S3`·`Table S4`·`Fig. 3` 인쇄 숫자와 구분한다.
    ⚠ **`Fig. 3` 의 황화물 42 셀은 "그림에만 있는 인쇄 숫자"** 다 — 좌표 추정이 아니라 **활자 판독**이고, 할라이드 98 셀을 `Table S4` 와 전수 대조해 검증했다. 그래도 **표가 아니라 그림이 출처**라는 점은 밝힌다.
12. ⚠ **"우리 산수" 로 표시한 것**(창 폭 · 계열별 평균 · 어긋남 Δ · ΔE_D 기울기 · 동역학 연장 보간 · 식 (2) ≡ `use_hull_energy=True` 대수 · mutual 보정이 0 이라는 것 · 군집 평균)은 **논문이 인쇄하지 않은 우리 유도값**이다.
13. ⚠ **전부 소환값이고, 그 소환값의 출처는 MP 사전계산값**이다 — 범함수·U·스핀·무질서·판본 전부 미기재. 우리 QE·MP2026 숫자와 **같은 셀에 놓지 않는다**.
14. ⚠ **§7-2 의 "우리 `ocv_V` 가 환원 전위다" 는 *우리 유도*다.** 근거는 강하지만(이 논문 7/7 + `[Schw21]` + `[Zhu15]`) **pymatgen 재실행 검증은 아직 안 됐다** — `[Schw21]` digest §7-8 의 닫는 계산이 그대로 필요하다.

---

## 15. 기법 용어 미니사전

- **HSE (halide solid electrolyte)**: `Li₃YCl₆`·`Na₂ZrCl₆` 류의 **할로겐화물 고체전해질**. 황화물보다 산화에 강하고 산화물보다 무르다(냉간 성형 가능). 약점은 **흡습성**과 **Li/Na 금속에 대한 환원 불안정**.
- **ASSSIB**: all-solid-state sodium-ion battery. 이 논문의 대상.
- **P2 / O3 형 층상산화물**: Na 층상산화물의 적층 표기(Delmas). **P** = Na 가 **프리즘** 자리, **O** = **팔면체** 자리, 숫자 = 단위포 안 전이금속층 수. **P2 는 Na 가 부족(`Na₀.₆₇…`)하고 O3 는 거의 채워져(`NaMO₂`) 있다** — 그래서 O3 가 Na 를 더 많이 내놓고, 계면에서 더 반응적이다(이 논문 −220 vs −140).
- **grand-potential 상도**: Na(Li)를 저장소와 교환하도록 열어 놓고 `μ_Na` 를 독립변수로 만든 상도. `μ_Na = μ⁰_Na − eφ` 로 전압과 이어진다. **SE 혼자의 창**을 잰다.
- **pseudo-binary 계면 반응**: 두 고체 A·B 를 **혼합비 x 로 섞은 가상 조성**의 평형에너지를 x 전 구간에서 훑어 가장 유리한 분해를 찾는 방식. **전압 없이, 접촉만으로** 일어나는 반응을 잰다. 계보 = Richards 2016 · Zhu–He–Mo 2016 · Xiao 2019.
- **ΔE_D vs ΔE_D,mutual**: 앞은 **각 물질 자신의 준안정성까지 포함한** 총 구동력, 뒤는 그것을 빼고 **접촉이 새로 만든 몫**만 남긴 것. **뒤가 pymatgen `use_hull_energy=True`** 와 같다. ⚠ 두 물질이 모두 hull 위면 **둘이 같아진다**.
- **`E_hull` (convex hull 위 거리)**: 그 조성에서 가능한 최저에너지 상 조합보다 얼마나 높은가. **0 = 열역학적으로 안정**. 이 논문은 코팅에 `E_hull = 0` 을 요구했다(*"conservative"*).
- **동역학 연장창 (kinetically extended window)**: 열역학 창 밖이지만 **분해 구동력이 작아서**(여기선 `|ΔE_D| < 25 meV/atom`) 실제로는 안 무너진다고 보는 구간. **문턱은 물리가 아니라 선택**이다.
- **`NaCl₃` / `NaCl₇`**: Na 와 Cl 의 **다염화물**. Cl 이 `Cl₃⁻`·`Cl₇⁻` 형태로 부분 산화된 상으로, **MP hull 위의 가상/고압 상**인 경우가 많다. 이 계열이 **산화 한계를 정하는 상**이라는 것은 곧 **그 상의 MP 에너지가 창 전체를 좌우한다**는 뜻이다 — 판본 미기재가 특히 아픈 자리.
- **paddle-wheel 기전**: 다면체 음이온(여기선 `TaCl₆⁻`)의 회전이 양이온 도약을 돕는 기전. `NaTaCl₆`(σ 3.3 mS/cm)의 원전 ref 20 제목에 박혀 있다.
- **PCA / K-means**: 차원축소(PCA)와 비지도 군집화(K-means). ⚠ **PCA 는 여기서 *시각화용*이고 군집은 전 차원에서 했다**고 본문이 명시한다. `k` 선택 근거는 없다.
- **Na uptake per f.u.**: 화학식 단위당 흡수한 Na 수. **양 = sodiation(환원), 음 = desodiation(산화)**. **부호 있는 교환량의 사람용 표현**이고, 이 논문에서 방향을 기계적으로 검산할 수 있게 해 주는 유일한 양이다 (우리 `evolution` 과 같은 것).

---

## 16. 📌 도구 보고 (`tools/litdb/extract_figures.py`)

**재추출하지 않았다** — 지시대로 `--clean` 금지이고, `litdb/figures/jang2026_halide_se_interfacial_stability_highv_na/` 에 **2026-09-22 06:36 생성분 17장**이 이미 있었다. `figures.json` 의 `sources` 가 **정확히 지정된 두 파일**(`13. Interfacial_stability_halide_SE_highV_Na_ASSB_MAIN.pdf` · `13. Sup) Interfacial_stability_halide_SE_highV_Na_SI.pdf`)이라 **다른 논문 혼입 없음**을 확인했다.

⚠ **폴더 slug 가 digest slug 와 다르다**: 폴더는 `jang2026_halide_se_interfacial_stability_highv_na`(파일명 기반), digest 는 **`jang2026_halide_se_interfacial_stability_highv_na`**(우리 관례 `<firstauthor><year>_<topic>`). ⇒ **webapp 이 `figures/<slug>/` 로 찾는다면 이 digest 의 그림이 안 붙는다.**
**제안(직접 안 고쳤다)**: `litdb/figures/jang2026_halide_se_interfacial_stability_highv_na/` → `litdb/figures/jang2026_halide_se_interfacial_stability_highv_na/` 로 **디렉터리 rename** (또는 심볼릭 링크). 파일 내용은 그대로 두면 된다.

**추출 품질**: 본문 `Fig. 1`–`8` 8장 + SI `Fig. S1`–`S2` 2장 + `Table 1` + `Table S1`–`S7` 7장 = **17장 전부 잡혔고 누락·빈 크롭 0건**. `Table S3`·`Table S4` 처럼 여러 쪽에 걸친 표도 한 장에 들어갔다(`tab_S3.png` 400 KB · `tab_S4.png` 587 KB). 다만 **표는 PDF 텍스트 쪽이 정확해** 이미지는 쓰지 않았다.

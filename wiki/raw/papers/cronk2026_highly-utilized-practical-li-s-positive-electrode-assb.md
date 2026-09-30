---
title: "Cronk et al. 2026 — A highly utilized and practical lithium-sulfur positive electrode enabled in all-solid-state batteries (Nature Communications 17, 3298)"
description: "S(또는 Li2S) : LPSCl : AB = 30:50:20 복합양극을 one-step 고에너지 밀링(500 rpm 1 h, BPR 1:30)으로 만들어 황 표면에 Li3PS4+n interphase 를 형성하고, LPSCl 의 산화환원까지 용량으로 쓴 UCSD·LG ES 논문 — 11 mAh cm⁻²·25 °C·500 사이클, Li2S 반쪽셀 723 mAh g⁻¹(Li2S), anode-free 파우치 10 MPa·60 °C"
source_url: local-upload/0aa1b3d5-A_highly_utilized_and_practical_Li-S_cathode_enabled_in_ASSBs.pdf (본문 15쪽만 — SI 미확보)
doi: 10.1038/s41467-026-69750-0
ingested: 2026-09-30
sha256: c82836c03c00f034e975ebda058d6c5be87fc9d3de92e54128c827dadb0bdb95
tags: [assb, sulfide-electrolyte, composite-cathode, mixing-process, li2s, activation, carbon, anode-free, li-in, units]
compare:
  system: "ASSB Li–S — 본체는 황(S8) 양극, Li2S 양극은 반쪽셀 1문단 + anode-free 파우치"
  electrolyte: "Li6PS5Cl (LPSCl, NEI Corp.) — 분리층 450–500 µm @375 MPa 3 min, 양극 catholyte 50 wt%; 대조로 β-Li3PS4 (0.04 vs 2 mS cm⁻¹). 파우치는 LPSCl 98 wt% + 아크릴레이트 바인더 2 wt% 캐스팅 50 µm 필름"
  cathode: "활물질 : LPSCl : 탄소 = 30 : 50 : 20 wt% (활물질 = S8 또는 Li2S). 탄소는 acetylene black (그 외 VGCF·Ketjen black 시험). 펠릿은 바인더 없음, 건식 필름은 PTFE 1 wt%"
  li2s_source: "상용 Li2S (Sigma-Aldrich 99.98 %), as received — 입자 최대 ≈30 µm. 별도로 400 rpm 10 h / 24 h 밀링 옵션 있으나 723 mAh g⁻¹ 셀은 as-received"
  mixing: "one-step 고에너지 planetary BM (Retsch) 500 rpm · 1 h · 시료:볼 = 1:30 · Ar; LPSCl 은 사전 400 rpm 2 h, 5 mm YSZ. 대조군 = multi-step(S/C 500 rpm 1 h 후 SE 손혼합) · hand-mix(mortar 1 h). 밀링 1 h 초과 시 LPSCl 단독 전도도 1.3×10⁻³ → 4×10⁻⁵ S cm⁻¹"
  loading_mg_cm2: "1.0 / 1.2 / 2.7 / 7.0 / 7.6 (S, 펠릿) · 4.6 (S, 건식 필름) · 2.5 (S, 압력측정) · 3.8 (Li2S, 압력측정) · 4.3 (Li2S, anode-free 파우치)"
  li2s_wt_pct: 30
  anode: "Li1In / Li0.5In (Li 분말 + In 분말 vortex 5 min) · Li2Si (µSi + Li 분말 vortex 3 min) · µSi 슬러리 (N/P 2) · anode-free Ag–C (carbon black : Ag : PVDF = 69.75 : 23.25 : 7.0) / 10 µm 스테인리스 박"
  first_charge: "Li2S 산화 활성화 전위 2.4 V, 촉매 없음 (LPSCl 이 2.3 V 에서 산화되며 매개). anode-free 파우치 첫 충전 1077 mAh g⁻¹(Li2S), ICE 83 %, C/10 (0.1 A g⁻¹), 3.4 V 컷오프, 60 °C"
  first_discharge_mAh_gS: "1500 (bulk) · 1615 (micron) · 1694 (sub-micron) @C/20, 1 mg_S cm⁻² · 1314 @7 mg_S cm⁻² — 전부 SSE redox 기여 포함"
  first_discharge_mAh_gLi2S: "1047 / 1127 / 1182 / 917 [재현] ×0.698 · Li2S 반쪽셀 723 [인쇄] · anode-free 파우치 894 [재현] (1077 × 0.83)"
  cycle_capacity_mAh_gS: "직접 환산 불가 — 사이클 값이 mAh g⁻¹(황+LPSCl) 로 정규화돼 있다. [도표] micron ≈660 · sub-micron ≈535 mAh g⁻¹(active) @500 cyc → [재현] ×0.8 = 528 / 428 mAh g⁻¹(composite)"
  cycle_capacity_mAh_gLi2S: "anode-free 파우치 [도표] ≈810 @50 cyc (Li2S 기준) = [재현] ≈243 mAh g⁻¹(composite)"
  areal_mAh_cm2: "11 → [도표] ≈10.2 (140 cyc, 7 mg_S cm⁻², C/20, 25 °C) · 7.4 → ≈5.7 (147 cyc, C/5, 건식+Li2Si) · 4.7 (파우치, 15 mAh) — 황은 평균 방전, Li2S 는 충전 기준 (정의 다름)"
  cycles: "500 (C/2, micron 81 % · sub-micron 61 %, 2사이클 기준) · 140 (11 mAh cm⁻², 86.8 %) · 147 (7.4 mAh cm⁻², 77.4 %, 3사이클 기준) · 140 (µSi‖Li2S, 83 %, SI) · 47–50 (파우치, 86.6 %, 평균 CE 99.80 %). Methods 는 측정마다 셀 3개라 적지만 오차막대 없음"
  temperature_C: "25 ± 1 (펠릿 전부) · 60 (anode-free 파우치만)"
  mechanism: "one-step 고에너지 밀링이 황 표면에 황 과잉 thiophosphate Li3PS4+n (용량 역산 n≈3) 층을 만들고(Raman 152→149 cm⁻¹, XANES pre-edge, EDS 라인스캔 Cl 50 nm, XRD 비정질화, TGA 6.5 wt%) 동시에 LPSCl 절반을 redox-active LPS 로 바꿔 Li2S 활성화 전위를 2.4 V 로 낮춘다. dQ/dV 4영역 + XANES LCF 로 S / Li3PS4+n / LPSCl 기여를 83 / 7.5 / 9.2 % (방전)로 분해"
  our_axis: "복합양극 조성·SE·탄소·음극·스택압·온도가 우리 reference cell 과 같은 첫 논문 (30:50:20 · LPSCl · AB · Li–In · 75 MPa · 25 °C). 이식 대상: one-step 밀링 레시피와 '세게 짧게' 규율, LPSCl-only 대조셀로 SSE 기여를 빼는 측정법, micron > sub-micron. 이식 불가: 본체가 S8 이고 Li2S 데이터는 본문에 한 문단뿐이며 SI 미확보, 전압 기준 표기가 모호, 파우치는 60 °C"
---

# 수집 목적

A. Cronk, X. Wang, J. A. S. Oh, S.-Y. Ham, S. Bai, P. Ridley, M. Chouchane, C.-J. Huang, D. Cheng,
G. Deysher, H. Yang, B. Sayahpour, M. Vicencio, C. Lee, D. Lee, M.-S. Song, J. Jang, J. B. Lee,
Y. S. Meng, **"A highly utilized and practical lithium-sulfur positive electrode enabled in
all-solid-state batteries"**, *Nature Communications* **17** (2026) 3298,
DOI 10.1038/s41467-026-69750-0 (open access, CC BY) 의 **절별 해체분석**.

이 위키가 이 논문을 흡수하는 이유는 단순하다. **복합양극 조성·고체전해질·음극·스택압·온도가
우리 reference cell 과 사실상 같다.**

| | 이 논문 | 우리 ([[li2s-assb-reference-cell]]) |
|---|---|---|
| 복합양극 | AM : LPSCl : 탄소 = **30 : 50 : 20 wt%** | Li2S : LPSCl : AB = **30 : 50 : 20 wt%** |
| 탄소 | **acetylene black** (주) | **acetylene black** |
| SE | **Li6PS5Cl** | argyrodite LPSCl |
| 음극 | **Li1In / Li0.5In** (+ Li2Si · µSi · anode-free) | **Li–In** (→ anode-free) |
| 운전 스택압 | **75 MPa** (펠릿) | 미기재 |
| 온도 | **25 ± 1 °C** | 상온 |

지금까지 이 위키에 들어온 고체계 논문 두 편은 각각 조성이 달랐다 — Huang 2026 은
S : HES : KB : LPSC = 42 : 6 : 12 : 40, Zhang 2026 은 Li2S-PI3 : LPSCBr : MWCNT = 5 : 4 : 1.
**조성까지 같은 논문은 이것이 처음이다.** 다른 점은 **활물질이 주로 S8 이고 Li2S 는 보조**라는
것과, **혼합 경로가 one-step 고에너지 밀링**이라는 것이다. 그래서 이 논문은
[[one-step-vs-two-step-mixing]] 의 H3(one-step 우세)에 대한 **고체계 직접 근거**이자,
[[reference-cell-500-600-mahg]] 의 H1·H2·H3 을 동시에 건드린다.

**표기 규칙** (이 위키 관례 3구분 + 1):
- `[인쇄]` — 논문 본문/식/캡션/Methods 에 글자로 있는 것
- `[도표]` — 그림에서 눈으로 읽은 근사값 (**원 데이터가 아니다**)
- `[해석]` — 이 문서를 쓰면서 붙인 판단. **논문의 주장이 아니다**
- `[재현]` — 원문 값을 이 세션에서 산술로 옮긴 것 (계산식을 함께 적는다)

- 원본 파일: 로컬 업로드 PDF 15쪽 (본문 + Methods + 참고문헌).
  **Supplementary Information 은 이 세션에 없다** (G1). Nature Communications 는 SI 가 별도
  파일이고, 본문이 인용하는 Fig. S1–S35 · Table S1–S8 을 **하나도 보지 못했다.**
  SI 를 근거로 한 서술은 전부 "본문이 SI 를 이렇게 요약한다" 수준이며, 그 자체를 검증하지 않았다.
- 크로핑 그림: `raw/figures/cronk2026_highly-utilized-practical-li-s-positive-electrode-assb/`
  — 본문 Fig. 1–7 (7장). 자동 크로핑이 Fig. 3·4·7 에서 왼쪽 단만 잡아 **오른쪽 단 패널을
  포함하도록 bbox 를 손으로 넓혀 다시 잘랐다** (`figures.json` 의 `note` 참조). 캡션 문장 중간의
  "Table S4." 를 표 앵커로 오인해 생긴 `tab_S4.png`(7쪽 전면 복사)는 지웠다.
- 페이지 참조는 **PDF 페이지**(1–15) = 저널 조판 페이지.
- 비용량 환산 상수: M(S)/M(Li2S) = 32.065/45.95 = **0.6978** (이 문서에서는 ×0.698 로 쓴다).
  Li2S 이론용량 1166 mAh g⁻¹(Li2S), S 이론용량 1675 mAh g⁻¹(S).

---

# 원문에 없어서 확인이 필요한 것 (읽기 전에 먼저 본다)

이 절이 이 digest 의 가장 중요한 산출물이다.

| # | 공백 | 왜 문제인가 |
|---|---|---|
| **G1** | **SI 전체 미확보.** 본문이 인용하는 **Fig. S1–S35, Table S1–S8 을 하나도 보지 못했다.** 특히: S3(밀링 강도별 이용률) · S9(**Li2S 양극 제조법 비교 — 723 mAh g⁻¹ 의 출처**) · S11(Li2S 셀 사이클) · S23–S27(입도 SEM/XRD) · S28(율속) · S29(탄소 종류) · S33(부피변화 계산) · S35(µSi‖Li2S 140 사이클) · Table S2(용량 분해 계산) · Table S3(이용률 84 % 계산) · Table S5(XANES LCF 전문) · Table S8(에너지밀도 가정). | 이 digest 가 "본문이 SI 를 이렇게 요약한다" 이상으로 말할 수 없는 대목이 **논문의 절반**이다. 특히 우리에게 가장 값진 **Li2S 반쪽셀 데이터가 전부 SI(S9·S10·S11·S13)에 있다.** SI 를 구하면 이 digest 의 `-v2` 를 새로 써야 한다. |
| **G2** | **Li2S 양극의 본문 데이터가 사실상 한 줄이다.** `[인쇄, p.4]` "the one-step method … delivers a high specific capacity of **723 mAh g⁻¹** with a high coulombic efficiency of **99.3 %**" 가 전부고, 첫 충전 곡선·과전압·로딩·전류·컷오프·사이클 수가 본문에 없다. **723 이 충전인지 방전인지도 명시가 없다** (Li2S 계는 CE = 방전/충전이므로 둘의 차이는 0.7 %). | 우리 셀은 **Li2S 양극**이다. 이 논문에서 우리에게 직접 이식되는 숫자가 이 하나인데, 그 조건을 모른다. |
| **G3** | **전압 기준이 전부 "vs Li/Li⁺" 로만 적혀 있다.** Methods `[인쇄]` "cut-off potentials of 1–3 V vs. Li/Li⁺ for Li1In‖Sulfur cells, 0.7–3 V vs. Li/Li⁺ Li2Si‖Sulfur cells, 3.4 V–1 V vs. Li/Li⁺ for Si‖Li2S cells, and 3.4–1 V vs. Li/Li⁺ for anode-free‖Li2S pouch cell." **Li–In → Li/Li⁺ 오프셋 값을 어디에도 적지 않았고**, anode-free 파우치에는 기준 자체가 성립하지 않는다. `[도표]` Fig. 7j 의 축은 실제로 기준 없이 "Voltage (V)" 다. | 우리 위키의 단위 규율([[capacity-normalization-li2s-vs-sulfur]])이 정면으로 걸린다. 이 논문의 "2.4 V 활성화 전위"·"2.3 V LPSCl 산화"를 우리 Li–In 셀에 그대로 옮기려면 **오프셋을 우리가 따로 정해야 한다** (이 위키에는 Li–In 기준전위의 근거 raw 가 아직 없다). |
| **G4** | **셀 3개씩 만들었다면서 오차막대가 없다.** Methods `[인쇄]` "For each electrochemical measurement, **three cells were fabricated and tested.**" 그런데 Fig. 2a·3a·5d·5e·7b·7c·7e·7f·7j·7k 전부 **단일 곡선**이고 분산 표기가 없다. 오차막대는 **XANES LCF 막대그래프(Fig. 4d–f)에만** 있다 (standard error). | n = 3 이 "3개를 만들었다"인지 "3개 평균"인지 알 수 없다. 81 % vs 61 % (micron vs sub-micron, 500 사이클) 같은 결론이 셀 간 분산보다 큰지 판정 불가. |
| **G5** | **"이용률 84 %" 의 계산이 Table S3 에만 있다.** 분모가 1675 인지 1600 인지(설계용량은 1600 을 쓴다), 반응한 황(6.5 wt%)을 분모에 넣었는지 빼는지 본문에 없다. | 초록의 "highly utilized" 가 이 한 숫자에 걸려 있다. |
| **G6** | **interphase Li3PS4+n 의 두께·조성·전도도를 직접 재지 않았다.** n 은 전기화학 용량에서 역산한 값(`[인쇄]` "likely existing in the **Li3PS4+3** phase")이고, 두께는 EDS 라인스캔의 `[인쇄]` "At 50 nm from the particle edge, the Cl signal vanishes" 에서 **간접적으로만** 시사된다. interphase 자체의 이온전도도 측정은 없다 (측정된 것은 S+LPSCl 복합체 전체의 2×10⁻⁵ S cm⁻¹). | 초록의 핵심 주장 — "metastable and **ionically conductive** interphase" — 에서 "ionically conductive" 는 **복합체 전도도가 밀링으로 올라갔다**는 간접 증거뿐이다. 두께도 "50 nm 이내" 라는 상한만 있다. |
| **G7** | **밀링의 "high energy" 가 정량화돼 있지 않다.** 있는 것: 500 rpm · 1 h · 시료:볼 = 1:30 · planetary(Retsch) · Ar · LPSCl 사전분쇄 400 rpm 2 h 5 mm YSZ. 없는 것: **용기 재질·용기 부피·볼 개수·볼 지름(복합체 단계)·밀링 중 온도·on/off 주기·비에너지(J g⁻¹)**. "low milling intensities" 대조군(Fig. S3)의 rpm 도 본문에 없다. | 우리가 [[mixing-equipment-ball-mill-thinky]] 로 재현하려면 **같은 rpm 이 같은 에너지가 아니다** (용기 지름·볼 질량이 다르면 충돌 에너지가 다르다). Kim 2023 G1 과 같은 종류의 공백이되 정도는 훨씬 가볍다. |
| **G8** | **본문 수치 불일치 (a) pre-edge 위치**: `[인쇄, p.4]` "A pre-edge feature at **2470.1 eV**" vs `[도표, Fig. 2d]` 그림의 라벨은 **2471.0**. | 자리수 뒤바뀜으로 보이지만 어느 쪽이 맞는지 본문만으로는 못 정한다. |
| **G9** | **본문 수치 불일치 (b) 고로딩 셀의 전류**: `[인쇄, p.9]` "evaluated at relatively low current densities of **0.52 mA cm⁻²**" vs `[도표, Fig. 7c]` 패널 안 라벨 "**C/20 (0.1 A g⁻¹)**", AM 7 mg_S cm⁻². `[재현]` 0.1 A g⁻¹ × 7 mg cm⁻² = **0.70 mA cm⁻²**. | 0.52 를 쓰려면 0.074 A g⁻¹ 이어야 한다. 셀 면적(0.785 cm²) 문제도 아니다(둘 다 면적당). |
| **G10** | **본문 수치 불일치 (c) 같은 셀의 면적용량이 10 과 11 을 오간다.** `[인쇄, p.9]` "Areal capacities of up to **10 mAh cm⁻²** … sulfur loading of 7 mg cm⁻²" → 두 문장 뒤 "stable cycling at **11 mAh cm⁻²**". Methods 를 읽으면 **정의가 다르다** — `[인쇄]` 황은 "**average** discharge and charge capacity ÷ 면적", Li2S 는 "charge capacity ÷ 면적". `[해석]` Fig. 7b(첫 사이클, 평균) = 10, Fig. 7c(사이클, 충전) = 11 로 읽으면 모순이 아니다. | **초록의 "up to 11 mAh cm⁻²" 는 충전 기준 면적용량**이다. 우리가 인용할 때 정의를 같이 적어야 한다. |
| **G11** | **본문 수치 불일치 (d) XANES 충전 후 황 분율**: `[인쇄, p.6]` "After charging, Li2S is no longer detected, with **32 wt%** assigned to sulfur" vs `[도표, Fig. 4e]` charged 막대 ≈ **27 wt%** (pristine 막대가 ≈32). | 본문이 pristine 값을 charged 로 옮겨 적었을 가능성. Table S5 가 있어야 정한다 (G1). |
| **G12** | **본문 수치 불일치 (e) 사이클 수·단위 오타**: `[인쇄, p.10]` "**77.4 % retention after 150 cycles** at **1.5 mAh cm⁻²** current densities" vs `[도표, Fig. 7f]` "77.4 % (**147 cycles** w.r.t. 3rd cycle)". 전류 단위는 mAh cm⁻² 가 아니라 mA cm⁻² 여야 한다 (`[재현]` 0.32 A g⁻¹ × 4.6 mg cm⁻² = 1.47 mA cm⁻²). 그림 축에도 오타가 있다 — `[도표]` Fig. 5e "0.16 A g⁻²"·"0.8 A g⁻²", Fig. 7k "C/10 (**1** A g⁻¹)" (Fig. 7j 는 같은 C/10 을 0.1 A g⁻¹ 로 적는다). | 유지율의 기준 사이클(2nd / 3rd)도 그림마다 다르다. 그대로 옮기면 틀린다. |
| **G13** | **본문 수치 불일치 (f) SI 표 번호**: 본문 `[인쇄, p.9]` "Parameters and equations used in the simulations can be found in **Tables S6 and S7**" vs Methods `[인쇄, p.14]` "the set of parameters and equations in **Tables S3 and S4**". Table S3 은 본문에서 이미 "이용률 추정" 표로 쓰였다. | SI 없이는 어느 쪽이 맞는지 알 수 없다. |
| **G14** | **"CE" 의 정의가 계마다 뒤집혀 있고 용어도 섞인다.** `[인쇄, Methods]` 황은 CE = 충전/방전, Li2S 는 CE = 방전/충전. 그런데 본문 p.3 은 같은 값을 "**conversion efficiency (CE)** of 17 %" 라고 쓰고 다음 문장부터 "coulombic efficiency" 로 부른다. | **CE 129 % 는 "효율" 이 아니라 SSE 산화가 얹힌 충/방 비**다. 우리가 이 숫자를 인용할 때 반드시 정의를 붙여야 한다. |
| **G15** | **사이클 용량이 mAh g⁻¹(S+LPSCl) 로 정규화돼 있다** (Fig. 5e). 이 위키가 쓰는 세 기준(S / Li2S / composite) 중 어느 것도 아닌 **네 번째 기준**이다. LPSCl 이 실제로 용량을 내므로 `[해석]` 이 값을 ×(80/30) 해서 mAh g⁻¹(S) 로 되돌리면 이론값을 넘는 무의미한 숫자가 된다. | [[capacity-normalization-li2s-vs-sulfur]] 에 **"active mass(AM+SE)" 기준**을 새 열로 추가해야 한다. 복합양극 기준 환산(×0.8)만이 안전하다. |
| **G16** | **anode-free 파우치의 핵심 사양이 없다.** Ag–C 층 두께·Ag 로딩(면적당)·N/P(anode-free 이므로 0)·Li 도금/박리 효율·**10 MPa isostatic 을 어떤 장비로 유지했는지**·60 °C 를 고른 이유·50 사이클 이후. 파우치 조립은 **WIP 500 MPa @80 °C** 인데 이것은 성형압이고 운전압 10 MPa 와 별개다. | [[anode-free-li2s-assb]] 에 그대로 걸리는 대목인데 재현 정보가 부족하다. Zhang 2026(Na 집전체, 1–4 MPa, 25 °C)과의 비교도 온도가 달라 직접 대조가 안 된다. |
| **G17** | **에너지밀도(Fig. 7g·7h)의 분모가 Table S8 에만 있다.** Fig. 7g 는 `[인쇄, 캡션]` "assuming 1600 mAh g⁻¹ discharge capacity, **30 μm SSE layer**, and **Li metal** as the negative electrode" 라는 가정만 밝힌다. 집전체·패키징·탭·음극 과잉분 포함 여부 불명. | 제목의 "practical" 과 "500 Wh kg⁻¹" 은 **모델값**이다. 실제로 만든 파우치는 **15 mAh, 60 °C, 50 사이클**이다. |
| **G18** | **탄소 비교 실험의 수치가 없다.** `[인쇄, p.8]` "Increasing the carbon surface area increased utilization, mainly from the SSE, but showed **no impact on cycling stability**" — VGCF·Ketjen black 의 비표면적·용량·사이클 수가 전부 Fig. S29 에만. | [[carbon-dimensionality-electron-network]] 에 가장 직접적인 고체계 대조 실험인데 숫자를 못 가져온다. |

---

## 0. 서지사항 (직접 확인)

`[인쇄]` PDF 1·15쪽:

| 항목 | 값 |
|---|---|
| 제목 | A highly utilized and practical lithium-sulfur positive electrode enabled in all-solid-state batteries |
| 제1저자 | **Ashley Cronk** (UCSD Materials Science and Engineering Program) |
| 교신 | **Jeong Beom Lee** (LG Energy Solution, jaybilee@lgensol.com) · **Ying Shirley Meng** (Univ. of Chicago, shirleymeng@uchicago.edu) |
| 소속 | 1 UCSD MSE · 2 UCSD NanoEngineering · 3 Univ. of Chicago Pritzker School of Molecular Engineering · 4 **LG Energy Solution, Ltd.** (LG Science Park, Seoul) · 5 현 Argonne National Lab · 6 현 서강대 화학과 |
| 학술지 | *Nature Communications* **17** (2026) 3298 |
| DOI | 10.1038/s41467-026-69750-0 |
| 접수/게재 | Received **25 March 2025** · Accepted **9 February 2026** |
| 저작권 | © The Author(s) 2026 — **CC BY 4.0 (open access)** |
| 지원 | **LG Energy Solution – UC San Diego Frontier Research Laboratory (FRL)** · NSF GRFP · SDNI(ECCS-1542148) · UCSD MRSEC(DMR-201192) |
| 이해충돌 | **있음 (선언)** — Y.S.M., A.C., J.B.L., M.-S.S. 가 이 연구로 **특허 2건**을 UCSD 와 LG Energy Solution 을 통해 출원 |
| 데이터 | figshare 10.6084/m9.figshare.31094524 (전극 모델·FEM 반복 데이터) · "Source data are provided with this paper" |
| 피어리뷰 | Daiwei Wang 외 익명 심사자 (peer review file 공개) |

`[해석]` **기업(LG Energy Solution) 공동연구**라는 점이 논문의 성격을 정한다 — 셀 3개씩 제작,
건식 공정 필름, 파우치, "industry standard formation rates", 에너지밀도 outlook, 특허 2건.
학술적 신규성보다 **양산 경로 확보**가 목적이고, 그래서 공정 조건(rpm·시간·BPR·압력·온도)이
다른 논문보다 훨씬 잘 적혀 있다. 우리에게는 그 점이 가장 쓸모 있다.

---

## 1. 한 문단 요약

`[해석]` 저자들은 **S8(또는 Li2S) : LPSCl : acetylene black = 30 : 50 : 20 wt%** 라는 평범한
조성을, **한 번에 고에너지로 갈아버리는(one-step, planetary 500 rpm, 1 h, 시료:볼 = 1:30)**
것만으로 고성능 양극으로 만들었다고 주장한다. 그 밀링이 황 입자 표면에 **황 과잉
thiophosphate 층(Li3PS4+n, 용량 역산으로 n ≈ 3)** 을 만들고(Raman S–S 굽힘 152 → 149 cm⁻¹,
XANES pre-edge, EDS 라인스캔), 동시에 **LPSCl 의 절반을 redox-active LPS 로 바꿔** 놓는다.
그 결과 (i) 첫 방전이 이론값 근처(1500 mAh g⁻¹(S))에 닿고 충/방 비가 **129 %** 까지 올라가며
(초과분은 SSE 산화환원), (ii) **Li2S 산화 활성화 전위가 촉매 없이 2.4 V 로** 내려가고,
(iii) 입도를 **sub-micron 이 아니라 micron(0.5–5 µm)** 으로 맞추면 C/2 500 사이클에서 81 %
유지(sub-micron 61 %)를 얻는다. 나아가 (iv) 황·Li2S 양극의 큰 부피변화가 **Si·Li 음극의
부피변화를 상쇄**해 셀 압력 변동을 거의 0 으로 만들고(operando 압력), (v) 7 mg_S cm⁻² 에서
**11 mAh cm⁻², 140 사이클 86.8 %** 를, 건식 공정 + Li2Si 에서 7.4 mAh cm⁻², 147 사이클
77.4 % 를, 그리고 **Li2S‖anode-free 파우치(15 mAh, 50 µm 분리층, 10 MPa, 60 °C)** 에서
첫 충전 1077 mAh g⁻¹(Li2S)·ICE 83 %·50 사이클 86.6 % 를 보였다.

---

## 2. p.1–3 — 초록과 서론의 명제

### 2.1 초록 `[인쇄]`

1. "we demonstrate a positive electrode design that employs sulfide solid-state electrolytes,
   where a **high energy synthesis approach forms a metastable and ionically conductive
   interphase on the active material surface**."
2. "This interphase facilitates high active material utilization and **contributes capacity
   with cycling**."
3. "tailoring active material particle sizes to the **micron-scale** improves rate performance
   and cycling stability."
4. "the substantial volume change of sulfur-based positive electrodes during operation can
   **partially offset that of the negative electrodes**, thereby mitigating internal mechanical stress."
5. "enable sulfur areal capacities up to **11 mAh cm⁻²** while maintaining stable cycling at **25 °C**."
6. "a **Li2S anode-free pouch cell** that operates under 'low stack pressure' of **10 MPa**."

`[해석]` 6개 명제 중 **1·2·3 이 우리 축에 정확히 걸린다**. 4·5 는 참고, 6 은 2단계
([[anode-free-li2s-assb]]) 용이다. 주의: 명제 2 "contributes capacity" 는 **장점이자
경고**다 — SSE 가 용량을 내면 mAh g⁻¹(S) 분모가 의미를 잃는다 (G15).

### 2.2 서론의 문제 설정 `[인쇄]`

- S8 → Li2S 전환의 부피변화 **79 %** (ref 9) — "ten times greater than that of conventional
  positive electrodes."
- 기존 방법: 고비표면적 탄소 호스트에 ball-milling / 용액 / 기상증착으로 활물질을 넣는 것 —
  "Nevertheless, these methods have resulted in **inconsistent utilization and cycle life**.
  Given the **large amount of carbon** typically used, inadequate ionic networks and insufficient
  contact to sustain conversion are likely responsible."
- Li–S 전환은 활물질·이온·전자의 **"triple-phase" 접촉**을 요구한다 (refs 8, 24).
- 황화물 SE 의 산화 안정성이 낮은 것은 **Li–S 의 낮은 운전 전위와는 오히려 궁합이 맞고**,
  불완전 redox 는 가역일 수 있다 (refs 29, 30). "Leveraging the redox activity of sulfide SSEs
  can enhance the reaction kinetics of sulfur and Li2S (ref 31)."
- 선행: Lin et al. 이 Li3PS4 + S → 황 과잉 thiophosphate(**Li3PS4+n**)를 보였고(ref 32),
  LPSCl + S 도 있다(ref 15 = Kim, Hwang, Yoon, Sun, ACS Energy Lett. 2023). **다만 선행은
  용매를 썼다.** Tanibata et al. 은 기계화학 밀링으로 S 가 P2S5+n 에 결합함을 보였다(ref 33).
- `[인쇄]` "While mechanochemical synthesis has been widely used, **standards have yet to be
  established**, likely due to the many synthesis permutations that can be employed."

`[해석]` 마지막 문장이 이 논문의 자리다 — **"밀링 조건이 표준화돼 있지 않다"**. 그것이
정확히 [[composite-cathode-mixing-routes]] 와 [[one-step-vs-two-step-mixing]] 이 묻는 것이다.
그리고 서론이 **ref 15 로 Kim–Sun 그룹(우리 위키의 kim2023 digest 와 같은 그룹)** 을 인용한다 —
"용매를 쓴 선행" 이 그쪽이고, 이 논문은 **무용매**를 주장한다.

---

## 3. p.11–14 — Methods 전문 (재현에 필요한 전부)

우리에게 가장 값진 절이다. **원문의 조건을 빠짐없이 옮긴다.**

### 3.1 재료·전처리 `[인쇄]`

| 항목 | 조건 |
|---|---|
| 글러브박스 | Ar, H2O·O2 < 1 ppm. 무수물이 아닌 것은 **80 °C 진공건조**. 보관 22 ± 3 °C, **제조 후 1–4주 내 사용** |
| SE | **Li6PS5Cl (LPSCl), NEI Corp., USA** — 분리층 겸 catholyte |
| catholyte 전처리 | **Ar 분위기, 400 rpm, 2 h, 5 mm 구형 YSZ(이트리아 안정화 지르코니아) 볼, 고에너지 planetary ball mill (Retsch, Germany)** — "to induce more interfacial contact to sulfur" (Fig. S2) |
| LPS | **β-Li3PS4, NEI Corp.** — 같은 절차 |
| 황 | **원소 황 99.98 %, Sigma-Aldrich** — as received 또는 **400 rpm, 10 h(micron) / 24 h(sub-micron), 시료:볼 = 1:10** |
| Li2S | **99.98 %, Sigma-Aldrich** — as received 또는 **황과 같은 절차로 밀링** |
| **복합양극 (최적)** | **500 rpm(별도 언급 없으면), 1 h(별도 언급 없으면), planetary ball mill, 시료:볼 = 1 : 30** |
| 대조군 ① multi-step | **황 + 탄소를 500 rpm 1 h 밀링한 뒤 SE 를 손으로 혼합** |
| 대조군 ② hand-mix | **전 성분을 mortar and pestle 로 1 h** |
| 복합양극 조성 | **활물질 30 wt% : LPSCl 50 wt% : 도전재 20 wt%** (S 계·Li2S 계 동일) |
| SE-only 양극 | **SE 80 wt% : 도전재 20 wt%** (LPSCl 계·LPS 계) |
| 도전재 | **acetylene black (Sigma-Aldrich)** — 사이클·CV 의 주 도전재. 그 외 **vapor grown carbon fiber (Sigma)**, **Ketjen black EC-600JD (MSE Supplies)** |
| LCO 대조 | Nb 코팅 LCO (MSE Supplies), **손혼합**, **LCO 70 : LPSCl 30 wt%** |
| Li–In 음극 | **stabilized Li 금속 분말(99.9 %, FMC) + In 분말(99.99 %, Sigma)** 을 **Li0.5In 또는 Li1In 몰비로 vortex 혼합 5 min** |
| Li2Si 음극 | **µSi(99 %, Sigma) + stabilized Li 분말**을 **Li2Si 몰비로 vortex 혼합 3 min** (ref 64 Ham et al.) |
| µSi 음극 | µSi + NMP(99.5 %) + PVDF 슬러리(**Si 99.9 wt%**)를 Cu 집전체에 닥터블레이드 → 80 °C 진공 하룻밤 → **10 mm 펀칭** (ref 58 Tan et al.) |

`[해석]` **밀링 조건이 이 정도로 적힌 논문은 이 위키에 아직 없었다.** Kim 2023 은 조건이
아예 없었고(G1), Huang 2026 은 rpm·시간만, Zhang 2026 은 상세했지만 장비 계열이 다르다
(3D swing mill 1400 rpm). 여기는 **rpm·시간·BPR·볼 재질·볼 지름(전처리 단계)·분위기·장비
제조사**가 다 있다. 없는 것은 G7 참조.

### 3.2 건식 공정 양극 필름 `[인쇄]`

- 복합양극 분말 + **PTFE 1 wt% (Chemours)** → **가열한 mortar and pestle (50–60 °C)** 에서
  "dough like consistency" 가 될 때까지.
- **60 °C 에서 hot rolling (MTI)**, 두께를 줄여 가며 **300 → 200 µm 필름**.
- 그 필름의 면적 로딩 ≈ **4.5–6 mAh cm⁻²**.

### 3.3 파우치용 SE 필름과 anode-free 층 `[인쇄]`

- SE 필름: **LPSCl 98 wt% + 아크릴레이트 바인더 2 wt%** 를 **p-xylene** 에 혼합 → PET 필름에
  캐스팅 → **40 °C 진공 하룻밤**.
- anode-free 층: **carbon black (Imerys) : 은 나노입자 : PVDF (Solvay) = 69.75 : 23.25 : 7.0 wt%**
  를 NMP 에 혼합(ref 65 Lee et al. — Ag–C anode-free 원전) → **10 µm 스테인리스 강 박**에
  닥터블레이드 → **100 °C 진공 하룻밤**.
- 파우치 조립: **Al 박 / 건식 Li2S 양극 / SE 필름 / anode-free 층** 적층 → 진공 실링 →
  **WIP(warm isostatic press) 500 MPa, 80 °C**.

### 3.4 셀 제작·전기화학 `[인쇄]`

| 항목 | 조건 |
|---|---|
| 펠릿 셀 | **직경 10 mm**, Grade 5 티타늄 플런저 + **PEEK 다이**, 면적 **0.785 cm²** |
| 분리층 성형 | **3 ton = 375 MPa, 3 min** → 두께 **450–500 µm** |
| 양극·µSi 성형 | **3 ton (375 MPa), 5 min** |
| LiIn·Li2Si 성형 | **1 ton = 125 MPa, 30 s** |
| **운전 스택압** | 조립 후 홀더에 넣고 **손으로 75 MPa 까지 조임** ("hand tightened to 75 MPa"). 별도 언급 없으면 전 사이클 **75 MPa** |
| **셀 수** | **"For each electrochemical measurement, three cells were fabricated and tested."** (그러나 G4) |
| EIS | Biologic SP-300, 조립 직후, **진폭 30 mV, 7 MHz–100 mHz, 10 pts/decade**; 등가회로 ZView |
| 이온전도도 | σ = L/RA, **Ti‖SSE‖Ti 또는 Ti‖복합체‖Ti**, A = 0.785 cm² |
| CV | **0.1 mV s⁻¹, 1–3 V vs Li/Li⁺** (황 창) |
| 사이클러 | Neware CT-4008T |
| 컷오프 | **Li1In‖S: 1–3 V** · **Li2Si‖S: 0.7–3 V** · **Si‖Li2S: 3.4–1 V** · **anode-free‖Li2S 파우치: 3.4–1 V** (전부 "vs Li/Li⁺" 로 표기 — G3) |
| 온도 | **25 ± 1 °C** (별도 언급 없으면). **anode-free 파우치만 convection chamber 60 °C** |
| 설계 면적용량 | 활물질 질량 × **1600 mAh g⁻¹(S)** 또는 **1100 mAh g⁻¹(Li2S)** ÷ 면적 (펠릿 0.785 cm², **파우치 3.24 cm²**) |
| 보고 면적용량 | **Li2S 는 충전용량 ÷ 면적, 황은 평균 방전용량 ÷ 면적** (→ G10) |
| 비전류·비용량 | 전류는 **S 또는 Li2S 질량**으로 나눈다. 일부는 **"total active mass (AM + 양극 내 SSE)"** 기준으로 보고 (→ G15) |
| **CE 정의** | **황: 충전/방전. Li2S: 방전/충전** (→ G14) |

### 3.5 분석 `[인쇄]`

| 기법 | 조건 |
|---|---|
| SEM/FIB | FEI Apreo · FEI Scios DualBeam, **5 kV, 0.1 nA**; 단면은 **cryo(−180 °C) Ga FIB, 30 kV 65 nA**, 세정 30 kV 15→7 nA; **air-tight transfer arm** |
| XRD | Bruker ApexII-Ultra CCD **회전 양극, Mo Kα (λ = 0.7107 Å)**, 5–50° 2θ, **0.7 mm 붕소 캐필러리 화염 밀봉** |
| Raman | Renishaw inVia, **785 nm**, 유리 슬라이드 + Kapton 밀봉 |
| TGA | NETZSCH STA 449 F3 Jupiter, **RT → 450 °C, 5 °C min⁻¹, N2**, 알루미늄 팬 크림핑, 분해능 0.1 µg |
| cryo-(S)TEM | ThermoFisher **Talos X200, 200 kV, low dose**, Melbuild 기밀 냉각 홀더, **−180 °C 에서 30 min 안정화 후** 노광, 4× in-column SDD Super-X EDS |
| XAS | **대만 TLS beamline 16A1 (NSRRC)**, Si(111) 2결정, **S K-edge XANES, TFY(Lytle), 0.2 eV step**, 2472 eV 로 보정, **2.5 µm Mylar 파우치**, He 퍼지 45 min 이상; Athena 로 LCF |
| 전극 기하 모델 | MATLAB (ref 67 Duquesnoy), **기공 10 vol% 고정, S 30–60 %, LPSCl:탄소 부피비 5:2 고정**; S 반경 **Bulk 25–50 µm / Micro 0.5–5 µm / Nano 0.25–0.5 µm**; 입방 전극 한 변 **200 / 50 / 15 µm**; 조건마다 **전극 3개 생성**; 토르투오시티는 **TauFactor**(ref 68), 전 방향 평균 |
| FEM | Iso2Mesh 메싱 → **COMSOL Multiphysics 6.1 Solid Mechanics**; **기공 0 가정**, S 입자 균일 리튬화, "Hygroscopic Swelling" 노드로 팽창 부여, 외부 경계 고정; 조건마다 전극 3개 평균 |

---

## 4. p.3–4 — 결과 1: 전도성 계면 만들기 (Fig. 2)

### 4.1 세 가지 혼합 경로의 첫 사이클 (Fig. 2a) ★★

조건 `[인쇄, 캡션 + 도표]`: Li–In 반쪽셀, **80 mA g⁻¹(S) = C/20**, 25 ± 1 °C,
`[도표]` 패널 안 "Loading: **1 mg_S cm⁻²**", 축은 **Voltage vs. Li/Li⁺ (V)** 0.5–3.

| 혼합 경로 | 첫 방전 | 첫 충전 | CE (충전/방전) |
|---|---|---|---|
| **one-step** (전 성분 500 rpm 1 h) | `[인쇄]` **≈1500 mAh g⁻¹(S)** ("near the theoretical (~1500 mAh gS⁻¹ at 25 °C)") = `[재현]` **1047 mAh g⁻¹(Li2S)** | `[도표]` ≈1950 / `[재현]` 1500 × 1.29 = **1935** | `[인쇄]` **129 %** |
| **multi-step** (S/C 밀링 후 SE 손혼합) | `[도표]` ≈**610** mAh g⁻¹(S) = `[재현]` 426 mAh g⁻¹(Li2S) | `[도표]` ≈105 | `[인쇄]` **17 %** |
| **hand-mixed** (전 성분 mortar 1 h) | `[도표]` ≈**200** mAh g⁻¹(S) | `[도표]` 거의 0 | 본문 미기재 |

`[도표]` one-step 의 방전 plateau ≈ **2.05 V**, 충전 plateau ≈ **2.4 V** (vs Li/Li⁺ 표기).
`[재현]` 분극 ≈ 0.35 V.

본문의 해석 `[인쇄]`:
- multi-step 의 낮은 CE 는 "insufficient mass transport to reconvert Li2S back to sulfur,
  usually requiring high activation potentials" 또는 "isolation of sulfur particles and active
  surface areas after volume expansion" 때문.
- one-step 의 CE 129 % 는 "**additional capacity from the SSE** has been obtained."
- Ohno et al.(ref 39)의 hand-mixing vs ball-milling 비교를 인용하며 그쪽은 CE 100 % 였다고 적는다.

`[해석]` **이 표 한 장이 [[one-step-vs-two-step-mixing]] 에 대한 이 논문의 답**이다. 다만
**그들의 "multi-step" 은 우리가 말하는 two-step 이 아니다** — 그들은 SE 를 **손으로** 섞었고,
우리 two-step 후보는 "Li2S–C 를 먼저 만들고 SE 를 **mild BM** 으로 더한다" 이다. 즉
이 실험이 배제한 것은 "**SE 를 저에너지로 붙이는 경로**" 이지 two-step 일반이 아니다.

### 4.2 XRD — 비정질화 (Fig. 2b) `[인쇄 + 도표]`

- 세 방법 모두에서 LPSCl 과 황이 검출된다. **"Only the one-step method facilitated amorphization."**
- `[도표]` hand-mixed·multi-step 은 날카로운 회절선(황 ▽ ≈10.5° 2θ Mo Kα, LPSCl ● 7.2/8.2/11.7/13.7/14.3°),
  one-step 은 **같은 위치의 봉우리가 뭉개지고 넓은 배경**이 된다.
- 탄소의 확산 산란이 가리므로 **탄소 없이 S + LPSCl 만** 밀링한 시료에서 FWHM 증가를 확인(Fig. S4a).
- 기전 설명 `[인쇄]`: 고에너지 밀링이 열을 넣고 **황 고리를 끊으며 PS4³⁻ 단위를 일그러뜨려
  느슨한 P–S 결합을 만든다**(ref 40). "This is advantageous since crystalline sulfur (cyclo-S8)
  requires large activation energies to break covalent bonds between sulfur atoms."

### 4.3 TGA — 6.5 wt% 의 황이 사라졌다 `[인쇄]`

- 황은 350 °C 에서 승화해야 하는데 **"6.5 wt% of sulfur is unaccounted for"** → 황 결합 환경이
  바뀌었고 LPSCl 과 반응했을 가능성 (Fig. S5).

### 4.4 Raman — Li3PS4+n 의 증거 (Fig. 2c) `[인쇄 + 도표]`

- S–S 굽힘(E2 대칭) 기준 **152 cm⁻¹**. `[도표]` 그림의 라벨: 황(S8) 기준선 **≈152**,
  one-step 복합체와 "Milled S and LPSCl" 은 **149 cm⁻¹** 로 적색 이동. "Mixed S and LPSCl"
  (손혼합)은 이동 없음.
- 해석 `[인쇄]`: "The S–S bending at lower wavelengths suggests an **increase in bond lengths from
  P–S stretching**, confirming the formation of **sulfur rich thiophosphates (Li3PS4+n)**, where
  elemental sulfur bonds with the sulfur at the PS4³⁻ terminals of LPSCl (refs 15, 32)."
- 보강: LPSCl 의 PS4³⁻ 대칭 신축 **425 cm⁻¹** 의 세기·파수가 함께 줄어든다(Fig. S4b) →
  "polymerization with bridging S–S bonds" (ref 44).
- **밀링 강도 의존** `[인쇄]`: "Sulfur utilization was found to **decrease when using lower milling
  intensities** (Fig. S3), suggesting incomplete formation of the Li3PS4+n phase." (수치는 SI — G1)

### 4.5 XANES — 사슬형 황의 pre-edge (Fig. 2d) `[인쇄 + 도표]`

- S K-edge: **원소 황 2473.6 eV**, **LPSCl 2472.4 eV**. `[인쇄]` pre-edge **2470.1 eV**
  (`[도표]` 그림 라벨은 **2471.0** — G8), 1차 미분에서 뚜렷.
- 해석 `[인쇄]`: pre-edge 는 황 산화수 감소를 뜻하며 장쇄 폴리설파이드(Li2Sy)에서 관측된다(ref 45).
  "The pre-edge observed here is **likely from chains of sulfur in Li3PS4+n**."

### 4.6 밀링 시간의 양면성 — ★ 가장 실용적인 발견 `[인쇄]`

| 시료 | 밀링 | 이온전도도 |
|---|---|---|
| **S + LPSCl 복합체** (500 rpm) | 0 → **1 h** | **6×10⁻⁶ → 2×10⁻⁵ S cm⁻¹** (증가, Fig. S4c) |
| **LPSCl 단독** | **1 h → 10 h** | **1.3×10⁻³ → 4×10⁻⁵ S cm⁻¹** (감소, Fig. S4d–f) |

- LPSCl 단독의 전도도 감소는 **"formation of insulative Li2S and LPS phases"** 탓.
- 결론 `[인쇄]`: "These results highlight the **importance of limiting milling durations**, where
  **high milling intensities used for short durations** were found to be sufficient to complete
  the interfacial reaction between sulfur and LPSCl **while preserving the ionic conductivity**."

`[해석]` 이것이 이 논문이 우리에게 주는 **가장 값싸게 이식 가능한 규율**이다:
**세게, 짧게 (500 rpm × 1 h), 그리고 SE 를 오래 갈지 마라.** 우리 [[composite-cathode-mixing-routes]]
의 one-step 열에 "시간을 변수로 두고 1 h 부근에서 끊는다" 를 적을 근거가 생겼다.

### 4.7 cryo-TEM 라인스캔 — interphase 의 위치 `[인쇄]`

- low-dose cryo-TEM + HAADF-STEM + 원소 매핑, **여러 입자** (Figs. S6, S7).
- "Hyperspectral mapping shows a **homogenous distribution** of all components."
- 라인스캔: **Cl 은 입자 가장자리에만**. **가장자리에서 50 nm 지점에서 Cl 이 사라지고 황만 남는다.**
  중심으로 갈수록 황 원자분율이 **LPSCl 화학량의 두 배**에서 안정 → 표면의 황 과잉 상 (Table S1).
- 결론 `[인쇄]`: "This sulfur rich interphase **lowers the energy barrier for lithiation**,
  facilitating fast lithium transport from the SSE matrix into the sulfur bulk (Fig. 2e)."

### 4.8 LPS 를 catholyte 로 쓰면 `[인쇄]`

- 황은 LPS 의 thiophosphate 단위에도 결합할 수 있지만 **LPS 의 전도도가 낮다 (0.04 vs 2 mS cm⁻¹,
  Fig. S8a)** → 이용률이 낮다 (Fig. S8b). "Although, reasonable capacity and cell performance
  are still achievable."

### 4.9 ★ Li2S 를 활물질로 쓰면 — 반응 방향이 뒤집힌다 `[인쇄]`

우리에게 가장 중요한 단락인데 **본문에서 한 문단**이다 (G2).

- 같은 제조법 비교를 **Li0.5In 음극 반쪽셀**에서 Li2S 로 수행 (Fig. S9). "Comparable trends seen
  with sulfur are also observed with Li2S."
  - **hand-mixing 은 사이클 자체가 안 된다** ("fails to cycle").
  - **multi-step 은 낮은 이용률 + 큰 분극**.
  - **one-step 은 723 mAh g⁻¹ + CE 99.3 %** ("indicating good reversibility").
- **Li2S 계에서는 밀링이 LPSCl 을 분해·비정질화시킨다** — 회절 봉우리가 사라지고, PS4³⁻ 의
  P–S 신축이 **425 → 418 cm⁻¹** 로 이동 = **Li3PS4 (LPS)** (ref 46) (Fig. S10a–b).
  `[인쇄]` "**This indicates that Li2S reduces LPSCl to LPS.**"
- 복합체 이온전도도가 떨어지는데도(Fig. S10c) Li2S 셀은 안정적으로 순환하고, **1사이클 이후
  전압 곡선에 SSE redox 로 귀속되는 추가 plateau 가 나타난다** (Fig. S11).
  `[인쇄]` "Usually formed electrochemically, **here the redox active products are formed during
  synthesis.**"

**단위 환산 `[재현]`** (Li2S 계는 Li2S 질량 기준으로 정규화한다 — Methods):

| 값 | mAh g⁻¹(Li2S) | mAh g⁻¹(S) | mAh g⁻¹(composite, 30 wt%) | 이론 대비 |
|---|---|---|---|---|
| one-step Li2S 반쪽셀 | **723** `[인쇄]` | **1036** (723 ÷ 0.698) | **217** (723 × 0.30) | 723/1166 = **62.0 %** |
| 우리 목표 대역 | 500–600 | 716–860 | 150–180 | 43–51 % |

`[해석]` **우리 목표(500–600 mAh g⁻¹(Li2S))보다 20–45 % 높다.** 그리고 그 셀은
**as-received 상용 Li2S** 다 — 다음 절 첫 문장이 `[인쇄]` "The previous electrochemical
performances were obtained using **as received sulfur and Li2S**" 이기 때문이다.
**우리와 같은 출발 물질·같은 조성·같은 SE·같은 음극 계열에서 723 이 나왔다면, 병목은 재료가
아니라 공정일 가능성이 크다.** 단 조건(로딩·전류·컷오프)을 모른다 (G2).

---

## 5. p.4–6 — 결과 2: LPSCl 의 산화환원과 용량 분해 (Fig. 3)

### 5.1 왜 분해하나 `[인쇄]`

"Often overlooked in literature, **deconvoluting the capacity contribution between sulfur and the
solid electrolyte is essential in quantifying the effectiveness of the positive electrode
architecture.**"

`[해석]` 이 문장은 이 위키가 그대로 가져가야 할 규율이다. CE 129 %, 1694 mAh g⁻¹(S) 같은 값은
**분해하지 않으면 의미가 없다.**

### 5.2 세 개의 활물질 `[인쇄]`

이 계에는 활물질이 셋이다: **① 벌크 LPSCl, ② 밀링으로 생긴 interphase Li3PS4+n, ③ 미반응 원소 황.**

- TGA: **30 wt% 황 중 23.5 wt% 가 미반응**(즉 **6.5 wt% 가 반응**).
- 1.6 mAh cm⁻² 셀, **복합체 총 질량 2.5 mg**: 미반응 황 23.5 wt% → `[인쇄]` **1 mAh** 기대
  (1675 mAh g⁻¹ 사용). `[재현]` 2.5 mg × 0.235 × 1675 mAh g⁻¹ = **0.984 mAh** ✓
- 방전 중 **미반응 벌크 황이 용량의 83 %**, 나머지는 LPSCl + Li3PS4+n 환원.
  `[재현]` 전체 방전 ≈ 0.984/0.83 = **1.19 mAh** → 면적 0.785 cm² 로 나누면 **1.51 mAh cm⁻²**
  (표기된 1.6 과 부합).

### 5.3 LPSCl 단독 셀 (Fig. 3a) `[인쇄 + 도표]`

- 구성: **LPSCl + 탄소만**, Li–In 음극(리튬 공급원), 황 전압창(1–3 V), `[도표]` **20 mA g⁻¹**.
- `[인쇄]` 환원 **115 mAh g⁻¹**, 산화 **355 mAh g⁻¹**.
  `[도표]` 그림에서 읽으면 환원 ≈105, 산화 ≈368, **2사이클 가역 ≈325 mAh g⁻¹**.
- `[해석]` **산화가 환원의 3배**다. 즉 SSE 는 "충전 때 더 많이 내놓는" 비대칭 기여를 한다.

### 5.4 dQ/dV 4개 영역 (Fig. 3c 1사이클, 3d 3사이클) `[인쇄 + 도표]`

조건 `[인쇄, 캡션]`: 황 10/20/30 wt% 셀. 황 로딩 **0.3 / 0.84 / 1 mg cm⁻²**, 총 활물질
(황 + LPSCl) **2.8 / 2.9 / 2.5 mg cm⁻²**, 전류 **60 / 70 / 80 mA g_S⁻¹**,
**스택압 75 MPa, 25 ± 1 °C**. 용량은 **총 활물질 질량**으로 정규화.

| 영역 | 전위 (vs Li/Li⁺ 표기) | 귀속 |
|---|---|---|
| **I** | `[도표]` **≈1.95 V** (환원 최대) | **황 환원 S⁰ → S²⁻** — 황 wt% 가 높을수록 지배적 |
| **II** | **1.3 V 부터** | **Li3PS4+n 환원 시작** (LPS 처럼 LPSCl 보다 높은 전위에서 환원, Fig. S12). **1.15 V 부터 LPSCl 환원** |
| **III** | `[도표]` **≈2.4 V** (산화 최대, 가장 큰 봉우리) | **Li2S 산화** |
| **IV** | **2.70 V 부터** | **SSE 산화** — "This additional oxidation capacity is **recoverable upon the subsequent discharge**" |

**방전 용량 분해** `[인쇄]` (Table S2):

| 기여 | 방전 용량 비중 | 구간 |
|---|---|---|
| 미반응 벌크 황 | **83 %** | OCV → 1.3 V |
| interphase Li3PS4+n | **7.5 %** | 1.3 → 1.15 V |
| 벌크 LPSCl | **9.2 %** | 1.15 → 1.0 V |

**충전 용량 분해** `[인쇄]`: 반응한 황(Li3PS4+n) **10 %**, LPSCl **27.5 %**.

**반응한 황의 비용량** `[인쇄]` **553 mAh g⁻¹** — "likely existing in the **Li3PS4+3** phase after
synthesis." `[재현]` 반응 황 질량 = 2.5 mg × 0.065 = 0.1625 mg; 방전의 7.5 % = 1.19 × 0.075 =
0.0893 mAh; 0.0893 mAh ÷ 0.1625 mg = **549 mAh g⁻¹** — 원문 553 과 일치(반올림 차).
`[해석]` **논문 내부에서 산술이 맞는다.** 이 계산 사슬은 재현 가능하다.

**이용률** `[인쇄]`: "Positive electrodes with **30 wt% sulfur is 84 % utilized** during the 1st
discharge. Sulfur utilization significantly increases for lower sulfur weight percentages,
increasing to **above 90 % for the positive electrode with 10 wt% sulfur**." (Table S3 — G5)

### 5.5 CV (Fig. 3b) `[도표]`

- Li1In‖Sulfur 와 Li1In‖LPSCl 을 겹쳐 **0.1 mV s⁻¹**, 1–3 V.
- 황 셀: 환원 봉우리 **≈1.68 V**, 산화 봉우리 **≈2.7 V**. 환원 전류가 **1사이클 −0.62 →
  6사이클 −1.03 mA cm⁻²** 로 **커진다** (활성화).
- LPSCl 셀: 산화 봉우리 **≈2.55 V**, 전류는 황 셀의 약 1/3, 역시 사이클마다 커진다.
- `[해석]` CV 의 환원 봉우리(1.68 V)와 dQ/dV 의 영역 I(1.95 V)이 다른 것은 sweep 과
  정전류의 차이다. **둘을 섞어 인용하면 안 된다.**

### 5.6 제안된 LPSCl redox 반응식 `[인쇄]`

```
Li6PS5Cl + 1 Li⁺/e⁻ → Li2S + Li4PS4 + LiCl          Q_red ≈ 100 mAh g⁻¹
Li2S + Li4PS4 → Li2.5PS4 + S + 3.5 Li⁺/e⁻ + LiCl    Q_ox  ≈ 350 mAh g⁻¹
Li2S + Li4PS4 ⇄ Li2.5PS4 + S + 3.5 Li⁺/e⁻           Q_rev ≈ 350 mAh g⁻¹
```

- 부수 조건 `[인쇄]`: **LiCl 생성이 복합체 유효 이온전도도를 낮출 것으로 예상**되지만 이 전압창
  안에서 가역성에는 영향이 없어 보인다. **4 V 아래 컷오프가 LPSCl 의 완전 산화를 막아** 전도도를
  보존한다. LPSCl 분해 정도는 **탄소 접촉·비표면적에 크게 의존**하며 준안정상(Li6±xPS5Cl)과
  안정상이 병존할 것이다 (ref 29).
- ★ `[인쇄]` "the **high oxidative tendency of LPSCl at 2.3 V vs. Li/Li⁺** is also effective at
  **reducing the activation potential of Li2S oxidation**. In this work, the **activation potential
  was found to be 2.4 V, without requiring the use of catalysts or kinetic promoters beyond the
  SSE itself.**"

`[해석]` **이것이 [[li2s-activation-first-charge]] 에 대한 이 논문의 답**이다 — Li2S 활성화
과전압을 낮추는 "매개체" 를 **밀링으로 미리 만들어 둔다**. 액체계의 LiNO3·리독스 매개체,
Zhang 2026 의 LiI, Huang 2026 의 고엔트로피 황화물과 **같은 자리를 SSE 자신의 분해산물로 채운
것**이다. 첨가제 무게 대가가 0 이라는 점에서 셋 중 가장 싸다.

---

## 6. p.6–7 — 결과 3: 가역성 검증 (Fig. 4)

### 6.1 in-situ EIS (Fig. 4a) `[인쇄 + 도표]`

- 첫 형성 사이클의 SoC 마다 측정. **방전 후 임피던스가 85.2 Ω 증가** — Li2S 생성에 따른 전하이동
  저항. **충전 후에는 pristine 근처로 되돌아온다** (Fig. S15).
- `[도표]` Nyquist 축 Z_re 0–400 Ω, 세 상태(OCV / 1 V / 3 V).

### 6.2 XRD (Fig. 4b) `[인쇄 + 도표]`

고로딩 **7.6 mg cm⁻²** 황 양극, pristine / discharged(1 V) / charged(3 V).

- pristine: 비정질 배경 + 약한 LPSCl 봉우리, 황 ▽ ≈10.5°.
- discharged: **나노결정 Li2S** 회절선 출현(▼ ≈12.4°, 20.6°, 23.8° 2θ Mo Kα) `[도표]` +
  **LPSCl 이 결정성을 되찾는다** ("LPSCl regains crystallinity during electrochemical Li2S formation").
- charged: **Li2S 검출 불가**(완전 산화), **황 10.5° 재출현**. 다만 세기가 약하고 배경이
  비정질적 → **재생성된 황도 pristine 처럼 비정질**이고 **황 과잉 interlayer 가 유지됨**을 시사.
- **1사이클 후 15° 2θ 에 새 봉우리** → SE 벌크의 Raman 이 LPSCl+LPS 혼합 PS4³⁻ 를 보여(Fig. S16)
  **LPS 로 귀속**.

### 6.3 TGA (Fig. 4c) `[도표]`

- 잔류질량: pristine **23.4 % 손실**, charged **19.8 %**, discharged **2.11 %**.
- `[인쇄]` "The mass loss differences between the pristine and charged composite originate from the
  sulfur rich interlayer, which **increases the thermal stability of the reacted sulfur**."

### 6.4 XANES LCF 정량 (Fig. 4d–f) `[인쇄 + 도표]`

`[인쇄]` 한계 고백: "XANES quantification of the entire electrode can be challenging due to the
**shallow probe depth when using tender X-rays**" (상세 논의는 SI).

| 패널 | 상태 | `[도표]` 무게 분율 |
|---|---|---|
| **d: LPSCl 양극** | pristine | LPSCl ≈100 % |
| | discharged | LPSCl ≈43, **LPS ≈40** (`[인쇄]` "half of LPSCl … decompose to LPS") |
| | charged | **S 9.7** `[인쇄]`, LPSCl ≈50, **LPS ≈22** `[인쇄]` |
| **e: 황 양극** | pristine | S ≈32, LPSCl ≈51 |
| | discharged | LPSCl ≈45, LPS ≈34, **Li2S 20.2 `[인쇄]`** |
| | charged | S `[인쇄]` **32** / `[도표]` **≈27** (G11), LPSCl ≈37, LPS ≈19, **Li2S 0** |
| **f: Li2S 양극** | pristine | LPSCl ≈27, **LPS ≈26**, Li2S ≈30 (`[인쇄]` "**half of LPSCl decomposes into LPS after synthesis**") |
| | charged | **S ≈38**, LPSCl ≈31, LPS ≈14 |
| | discharged | LPSCl ≈28, LPS ≈28, Li2S ≈27 |

`[해석]` **f 의 pristine 열이 우리에게 가장 중요하다** — Li2S 양극은 **밀링 직후 이미 LPSCl 의
절반이 LPS 다.** 우리가 같은 밀링을 하면 우리 복합양극도 그럴 것이다. 그런데 이 논문은 그것을
**손실이 아니라 기능(리독스 매개 + 활성화 전위 강하)** 으로 읽는다. 다만 오차막대가 커서
(±10 wt% 수준) 이 분율을 정밀값으로 쓰면 안 된다.

---

## 7. p.7–9 — 결과 4: 입자 크기·기하 모델·수명 (Fig. 5) ★

### 7.1 출발 입자 `[인쇄]`

- as-received: **황 일부가 100 µm 급**(Fig. S23), **Li2S 30 µm 급**(Fig. S24).
- 복합체 밀링 후에도 **황 입자는 원래 크기에 가깝게 남는다**(SEM-EDS, Fig. S25).
  `[해석]` 즉 **복합체 one-step 밀링은 황을 잘게 부수는 공정이 아니다** — 표면을 반응시키는
  공정이다. 입도 제어는 **별도의 사전 밀링(400 rpm 10 h / 24 h)** 이 한다.
- 크기 등급: **bulk 25–50 µm · micron 0.5–5 µm · sub-micron 0.25–0.5 µm**. 크기 축소 후
  XRD 로 황의 결정성 보존 확인(Fig. S27).

### 7.2 기하 모델 (Fig. 5a–c) `[인쇄 + 도표]`

`[도표]` 활물질 질량분율 **30 %** 에서:

| 지표 | bulk | micron | sub-micron |
|---|---|---|---|
| **활성 표면적** (SE 와 접촉한 황의 %) | ≈6 % | ≈21 % | **≈87 %** |
| **LPSCl 상의 이온 토르투오시티 τ** | ≈3.0 | **≈2.0 (최저)** | ≈3.4 |

60 % 에서는 τ 가 **sub-micron 15.3 · bulk 5.0 · micron 3.0** 으로 벌어진다 `[도표]`.

`[인쇄]` "**Surprisingly, the micron sulfur electrode exhibits the lowest ionic transport
tortuosity** … sub-micron particles may be the best choice to achieve high utilization, yet high
active wt% may be challenging to implement since the ionic transport tortuosity **increases
drastically after 50 wt%**." 한계도 명시: "the geometrical modeling **does not consider the
chemomechanical effects** from lithiation."

`[해석]` **우리 조성이 정확히 AM 30 wt%** 다. 이 그림은 "30 wt% 에서는 아직 토르투오시티가
문제가 아니다"라고 말한다 — 즉 **우리 조성에서 이온 경로는 병목이 아닐 가능성**을 시사한다
([[reference-cell-500-600-mahg]] H2 에 대한 **모델 기반** 반증 재료). 단 이것은 황 구형 입자
가정의 시뮬레이션이고 Li2S 가 아니다.

### 7.3 입도별 첫 사이클 (Fig. 5d) `[인쇄 + 도표]`

조건: Li–In 반쪽셀, **1 mg_S cm⁻²**, **C/20 (0.08 A g⁻¹)**, 25 °C.

| 입도 | 첫 방전 mAh g⁻¹(S) | `[재현]` mAh g⁻¹(Li2S) | 첫 충전 `[도표]` |
|---|---|---|---|
| bulk | **1500** `[인쇄]` | 1047 | ≈1940 |
| micron | **1615** `[인쇄]` | 1127 | ≈2210 |
| **sub-micron** | **1694** `[인쇄]` (이론 초과) | 1182 | ≈2270 |

`[인쇄]` "This means that **more LPSCl redox activity can be activated with higher surface area
particles.**" 2사이클에서 **분극이 577 → 452 mV 로 감소** (Fig. S28a).

### 7.4 율속 (Fig. S28b) `[인쇄]`

- **1 C = 1.6 A g_S⁻¹ = 1.6 mA cm⁻²** 까지. 이 전류는 **Li–In 의 임계전류(≈1 mA cm⁻², ref 50)를
  넘는다**고 저자들이 명시.
- 총 활물질(황 + LPSCl) 기준으로 micron·sub-micron 모두 **≈700 mAh g_active⁻¹**.
  `[재현]` 활물질 기준 이론 상한 = 0.375 × 1675 + 0.625 × 350 ≈ **847 mAh g_active⁻¹**
  (황이 활물질의 37.5 %, LPSCl 62.5 %, LPSCl 가역용량 350) → 700 은 그 **83 %**.
- `[인쇄]` "This is critical for solid-state, as the **catholyte is usually considered inactive,
  responsible for 'dead weight'** within the cell. In this work, the catholyte contributes
  electrochemically to the overall cell capacity."

### 7.5 500 사이클 (Fig. 5e) ★ `[인쇄 + 도표]`

조건 `[인쇄, 캡션]`: **C/2 (800 mA g⁻¹)**, 방전용량은 **활물질(황 + LPSCl) 질량**으로 정규화,
25 ± 1 °C. `[도표]` 처음 2–3 사이클은 **C/10 (0.16 A g⁻¹)** 형성.

| 입도 | 초기(C/2) `[도표]` | 500 사이클 `[도표]` | 유지율 `[인쇄]` | `[재현]` mAh g⁻¹(composite) = ×0.8 |
|---|---|---|---|---|
| **micron** | ≈750 mAh g_active⁻¹ | ≈660 | **81 % (500 cyc, 2사이클 기준)** | 600 → **528** |
| sub-micron | ≈800 | ≈535 | **61 %** | 640 → 428 |
| bulk | ≈300 (평탄) | — (≈200 사이클에서 중단) | `[인쇄]` "fast decay" | 240 |

CE `[도표]`: 세 셀 모두 **≈100 %** 로 평탄 (우측 축 70–100 %).

`[해석]` **"안정" 은 CE 가 아니라 용량 기준으로도 성립**한다 (CE 100 % + 용량 81 %).
이 위키가 자주 지적하는 "CE 안정 ≠ 용량 안정" 함정에 이 논문은 빠지지 않았다.
다만 **bulk 곡선이 200 사이클에서 끊긴 이유가 본문에 없다.**

**★ 복합양극 기준 대조**: micron 셀의 500 사이클 용량 **≈528 mAh g⁻¹(composite)** 는
우리 목표(500–600 mAh g⁻¹(Li2S) = **150–180 mAh g⁻¹(composite)**)의 **약 3배**다. 단
활물질이 S8 이라 복합양극 기준 이론값 자체가 다르다 (S 30 wt% → 502 vs Li2S 30 wt% → 350
mAh g⁻¹(composite)). **그럼에도 그들은 이론값을 넘는다 — SSE 가 용량을 내기 때문이다.**

### 7.6 왜 sub-micron 이 지는가 `[인쇄 + 도표]`

저자들의 논증 순서:
1. **탄소 탓인가?** 비표면적·형태가 다른 탄소(VGCF·Ketjen black)로 바꿔 봤다 (Fig. S29).
   "Increasing the carbon surface area **increased utilization, mainly from the SSE, but showed
   no impact on cycling stability.**" → 탄소 탓이 아니다. (수치 없음 — G18)
2. **계면 열화인가?** EIS 100/300/500 사이클 (Fig. 5f). `[도표]` CEI 저항:
   micron **260 → 285 → 355 Ω**, sub-micron **420 → 445 → 515 Ω**.
   그런데 `[인쇄]` "these results **differ marginally** (Fig. S30)."
3. **단면 SEM?** `[인쇄]` "both electrodes were found to show **indistinguishable morphology**
   (Fig. S31)."
4. **FEM** (Fig. 5g–h): 1차 리튬화 후 SSE 기지의 von Mises 응력. `[인쇄]` 두 경우 모두 **5 GPa
   초과** 응력 예측. `[도표]` 분포는 **이봉형**이고 **평균은 sub-micro 2.42 GPa vs micro 2.40 GPa**.
   `[인쇄]` "at the sulfur particle and SSE interface, the sub-micron sulfur composite experiences
   a **higher frequency of stress**."
5. 결론 `[인쇄]`: "sub-micron sulfur particles create a microstructure with high electrode
   tortuosity, resulting in higher interfacial stresses and faster capacity decay. … in this work
   we find that **micron-scale particles balance both utilization and stable cycling**."

`[해석]` **이 논증은 이 논문에서 가장 약한 고리다** — 탄소를 배제한 근거는 SI 그림 하나,
EIS 차이는 저자 스스로 "marginal", SEM 은 "indistinguishable", FEM 평균 응력은 **2.42 vs 2.40 GPa
(0.8 % 차)**. 남는 것은 **응력 분포의 고응력 쪽 빈도**뿐이다. "micron 이 최적" 이라는 결론
자체는 500 사이클 실측(81 % vs 61 %)으로 지지되지만, **그 원인이 chemomechanical 이라는 설명은
소거법**이다. 그리고 G4(셀 3개, 오차 없음) 때문에 81 % vs 61 % 가 셀 간 분산을 넘는지도 모른다.

---

## 8. p.9 — 결과 5: 형태 변화와 셀 압력 (Fig. 6)

### 8.1 cryo-FIB 단면 두께 `[인쇄 + 도표]`

| 전극 | pristine | 리튬화(황) / 탈리튬화(Li2S) | 1사이클 후 |
|---|---|---|---|
| **micron 황** | **26 µm** | **32 µm** | **32 µm** (두께 유지, **기공 증가**) |
| **Li2S** | **45 µm** | **26 µm** (`[인쇄]` "~40 %" 감소; `[재현]` (45−26)/45 = **42 %**) | **32 µm** (pristine 근처로 가역) |

- 황 계산 `[인쇄]`: 30 wt% 황에서 완전 리튬화 시 **25.8 vol% 변화** 예상 → 26 → **32.7 µm**
  (관측 32 와 근접). 이 셀의 리튬화 용량 **1.22 mAh** → **4.9 µm mAh⁻¹**.
  `[재현]` (32 − 26)/1.22 = **4.92 µm mAh⁻¹** ✓
  `[인쇄]` "which is also **close to the expected thickness growth of Li metal with cycling**
  (ref 56). Therefore, **lithiating the sulfur positive electrode can compensate the volume
  reduction from stripping Li metal.**"
- 황 전극은 **SSE 기지가 소성변형**해 팽창을 수용하고, 변형된 구조가 분리층과의 밀착을 유지하며
  이후 팽창을 받쳐 준다. `[인쇄]` 시뮬레이션 응력이 **LPSCl 의 전단탄성률 근처**(ref 57)라 소성변형은
  놀랍지 않다.
- **Li2S 는 반대다** `[인쇄]`: 탈리튬화에서 **주상(columnar) 균열**이 단면과 표면 모두에 생긴다
  (Fig. S34). "Surface cracking is likely **strain induced from inhomogeneous lithium removal**."
  실리콘 음극 ASSB 에서 관측된 것과 같은 현상(ref 58)이며 **2D 계면에 구속된 전환형 전극의
  일반 거동**으로 본다. 1사이클을 마치면 형태는 pristine 근처로 **가역**.
- 두 결론 `[인쇄]`: "First, conversion positive electrodes can **alleviate internal pressure from
  negative electrode volume changes.** Second, **Li2S positive electrodes inherently face more
  mechanical challenges compared to sulfur due to strain induced cracking after delithiation.**"

`[해석]` **두 번째 문장이 우리에게 직접 불리한 관측이다** — Li2S 출발은 첫 충전에서 **수축**하고
균열이 생긴다. Li2S 45 → 26 µm 는 42 % 수축이다. 우리 reference cell 의 첫 충전 과전압·용량
손실이 활성화 문제만이 아니라 **수축 균열에 의한 접촉 상실**일 수 있다는 가설을
[[reference-cell-500-600-mahg]] 에 추가할 근거다 (H1 과 H2 사이의 새 경로).

### 8.2 operando 압력 (Fig. 6c–d) `[인쇄 + 도표]`

조건 `[인쇄, 캡션]`: **C/10**, LCO **26 mg cm⁻²**(0.1 A g⁻¹) · 황 **2.5 mg_S cm⁻²**(0.16 A g⁻¹) ·
Li2S **3.8 mg cm⁻²**(0.10 A g⁻¹), 25 ± 1 °C, **N/P 2**.

| 셀 | 초기 압력 `[도표]` | 1사이클 중 변화 `[도표]` |
|---|---|---|
| **LiSi‖Sulfur** (4 mAh cm⁻²) | ≈75.3 MPa | **≈75.3 → 73.9 MPa (−1.4)** — 거의 평탄 |
| LiSi‖LiCoO2 | ≈76.0 | **76.0 → 80.7 → 77.8 (+4.7)** — `[인쇄]` "five times that observed for the sulfur case" |
| **µSi‖Li2S** (3.5 mAh cm⁻²) | ≈76.2 | **거의 0 변동** ("almost zero pressure variation") |
| Si‖LiCoO2 | ≈75.2 | 75.2 → 77.8 → 76.2 |

- µSi‖Li2S 셀은 `[인쇄]` **140 사이클에서 83 % 유지** (Fig. S35 — 미확인).
- `[인쇄]` 결론: "pressure changes from high-capacity negative electrodes **can be compensated
  using conversion positive electrodes that are highly utilized** … mitigates cell 'breathing'."

`[해석]` 압력 그래프의 절대값(≈75–76 MPa)이 Methods 의 **75 MPa 스택압**과 일치한다 —
**운전 스택압이 실제로 유지되고 있다는 독립 확인**이다. Huang 2026 이 운전압을 적지 않은 것과
대비된다.

---

## 9. p.9–11 — 결과 6: 고로딩·에너지밀도·anode-free 파우치 (Fig. 7) ★

### 9.1 Li–In 펠릿 고로딩 (Fig. 7a–c) `[인쇄 + 도표]`

첫 사이클 **C/20 (0.08 A g⁻¹)**:

| 설계 면적용량 | 황 로딩 | 첫 방전 mAh g⁻¹(S) | `[재현]` mAh g⁻¹(Li2S) | `[재현]` 설계 = 로딩×1600 |
|---|---|---|---|---|
| 2 mAh cm⁻² | **1.2 mg_S cm⁻²** | `[도표]` ≈1600 | ≈1117 | 1.92 |
| 5.5 mAh cm⁻² | **2.7 mg_S cm⁻²** | `[도표]` ≈1430 | ≈998 | 4.32 (실측이 설계 초과 — SSE 기여) |
| **10 mAh cm⁻²** | **7 mg_S cm⁻²** | **1314** `[인쇄]` | **917** | 11.2 |

- `[인쇄]` 7 mg cm⁻² 에서 **분극이 약간 증가**.
- 사이클 (Fig. 7c): **11 mAh cm⁻² 수준, 140 사이클 86.8 %** (2사이클 기준), 25 °C,
  `[인쇄]` 전류 **0.52 mA cm⁻²** / `[도표]` 패널 라벨 **C/20 (0.1 A g⁻¹)** (G9).
  `[도표]` 충전 면적용량 ≈11.7 → ≈10.2 mAh cm⁻², CE ≈100 %.
- `[인쇄]` "The ability to achieve stable cycling at **11 mAh cm⁻² at room temperature (25 °C)**
  demonstrates the effectiveness of the positive electrode microstructure."

### 9.2 건식 공정 + Li2Si (Fig. 7d–f) `[인쇄 + 도표]`

- Li–In 의 낮은 임계전류를 피하려고 **자립형 건식 필름 + Li2Si 음극**, **N/P 2**.
- 율속 (5.5 mAh cm⁻² 수준) `[도표]`: 0.05 C ≈1360 → 0.1 C ≈1170 → 0.2 C ≈900 → 0.5 C ≈580 →
  **1 C ≈340 mAh g⁻¹(S)** → 0.05 C 복귀 ≈1340 (`[인쇄]` "full recovery at C/20 (0.3 mA cm⁻²)").
  `[인쇄]` **1 C = 5.5 mA cm⁻²**.
- 사이클 (Fig. 7f): **7.4 mAh cm⁻² 수준**, **C/5 (0.32 A g⁻¹) = `[재현]` 1.47 mA cm⁻²**,
  AM **4.6 mg_S cm⁻²**, **147 사이클 77.4 %** (3사이클 기준; 본문은 "150 cycles" — G12).
  `[도표]` 면적용량 ≈7.0 → ≈5.7 mAh cm⁻², CE ≈100 %.

### 9.3 에너지밀도 전망 (Fig. 7g–h) `[인쇄 + 도표]`

- Fig. 7g 가정 `[인쇄, 캡션]`: **1600 mAh g⁻¹ 방전용량, 30 µm SE 층, Li 금속 음극**.
  `[도표]` "This work"(**황 30 wt%, 10 mAh cm⁻²**) ≈ **525 Wh kg⁻¹**.
- `[인쇄]` "even **lower weight percentages of sulfur at 10 mAh cm⁻² can realize 500 Wh kg⁻¹** and
  is likely a more promising approach than increasing the weight percentage of sulfur. This is
  because after lithiation, the volume of SSE compared to lithiated sulfur will reduce."
- Fig. 7h `[도표]` (Table S8 가정 미확인 — G17):

| 양극 | 음극 | Wh kg⁻¹ |
|---|---|---|
| Sulfur | Li 금속 | **552** |
| Sulfur | lithiated Si | **480** |
| Li2S | Silicon | **403** |
| Li2S | Li 금속 | **457** |
| **Li2S** | **anode-free** | **503** |

- `[인쇄]` "Despite sulfur possessing a higher specific capacity than its Li2S counterpart,
  **negative electrode selection is limited to those with a lithium source** … regardless of their
  high costs and manufacturing challenges. Using the positive electrode composition reported in
  this work, **Li2S can achieve over 400 Wh kg⁻¹ using silicon** … and **go beyond 500 Wh kg⁻¹ if
  combined with an anode-free architecture**."

`[해석]` **이것이 "왜 Li2S 인가" 에 대한 이 논문의 대답**이고, 우리 프로젝트의 2단계
([[anode-free-li2s-assb]])와 정확히 같은 논리다. 황이 더 높은 비용량을 가져도 **리튬 공급원이
있는 음극에 묶이므로**, Li2S + anode-free 가 셀 수준에서 이긴다.

### 9.4 ★ Li2S‖anode-free 파우치 (Fig. 7i–k) `[인쇄 + 도표]`

| 항목 | 값 |
|---|---|
| 형태 | **15 mAh 파우치**, 면적 **3.24 cm²**, `[도표]` 도식은 2 cm × 2 cm |
| 양극 | **건식 공정 Li2S 복합양극** (30:50:20 + PTFE 1 wt%), AM **4.3 mg cm⁻²(Li2S)** |
| 분리층 | **500 µm → 50 µm** 로 축소 (LPSCl 98 % + 아크릴레이트 2 %) |
| 음극 | **없음 (anode-free)** — Ag–C / 10 µm 스테인리스 박 |
| 면적용량 | **4.7 mAh cm⁻²** `[인쇄, 캡션]` · `[재현]` 4.7 × 3.24 = **15.2 mAh** ✓ |
| 조립압 | **WIP 500 MPa, 80 °C** |
| **운전압** | **10 MPa isostatic** (펠릿 75 MPa 대비) |
| 온도 | **60 °C** |
| 첫 사이클 | **C/10 (0.1 A g⁻¹)**, 컷오프 3.4–1 V. **충전 1077 mAh g⁻¹(Li2S)**, **ICE 83 %** → `[재현]` 방전 **894 mAh g⁻¹(Li2S)** (본문 p.3 "reversible capacity of **900 mAh g⁻¹**" ✓) |
| 사이클 | **C/3 (0.34 A g⁻¹ = 1.5 mA cm⁻²)**, `[도표]` **50 사이클** 중 **86.6 % (47 사이클, 3사이클 기준)**, **평균 CE 99.80 %** |
| `[도표]` 용량 추이 | ≈950 → ≈810 mAh g⁻¹(Li2S) |

**단위 환산 `[재현]`**:

| 값 | mAh g⁻¹(Li2S) | mAh g⁻¹(S) | mAh g⁻¹(composite) | 이론(1166) 대비 |
|---|---|---|---|---|
| 첫 충전 | **1077** | 1543 | 323 | **92.4 %** |
| 첫 방전 | 894 | 1281 | 268 | 76.7 % |
| 50사이클 | ≈810 | ≈1160 | ≈243 | 69.5 % |

`[인쇄]` "**Industry standard formation rates and cycling protocols were used**", "delivers high
utilization (1077 mAh g⁻¹) and an initial coulombic efficiency of 83 %."

`[해석]` **이 위키에 들어온 두 번째 anode-free Li2S ASSB 실증**이다 (첫 번째는 Zhang 2026,
Na 집전체·25 °C·1–4 MPa·400 사이클). 비교:
- Cronk: **Ag–C 집전체 · 60 °C · 10 MPa · 50 사이클 · 4.7 mAh cm⁻² · 파우치 15 mAh**
- Zhang: **Na 집전체 · 25 °C · 4 MPa · 400 사이클 · 1.26–2.44 mAh cm⁻² · 펠릿**
→ **Cronk 는 면적용량·형태(파우치)에서 앞서고, Zhang 은 온도·사이클 수에서 앞선다.**
**60 °C 는 큰 단서다** — 상온 anode-free 파우치가 아니다.

---

## 10. SI 대조 — 미확보

**이 세션에는 SI 파일이 없다** (G1). 본문이 인용하는 항목을 목록으로만 남긴다.
SI 를 확보하면 이 digest 를 갱신하지 말고 **`-v2` 를 새로 써서 supersedes 로 잇는다**
(raw 불변, `wiki/SCHEMA.md`).

| 항목 | 본문이 말하는 내용 | 우리 우선순위 |
|---|---|---|
| **Fig. S9** | Li2S 양극 제조법 3종 비교 — **723 mAh g⁻¹·CE 99.3 % 의 출처** | **최우선** |
| **Fig. S11** | Li2S 셀의 사이클 + 1사이클 이후 SSE redox plateau | **최우선** |
| **Fig. S10a–c** | Li2S 계에서 LPSCl → LPS 분해 (XRD·Raman 425→418 cm⁻¹·전도도) | **높음** |
| **Fig. S13** | Li2S 전압창에서의 가역 거동 | 높음 |
| **Table S3** | 이용률 84 % / >90 % 계산 | 높음 |
| **Table S2** | 방전 용량 분해 계산 전문 | 높음 |
| **Fig. S3** | 밀링 강도(rpm)별 황 이용률 | 높음 |
| **Fig. S4a–f** | 탄소 없는 S+LPSCl 의 FWHM·425 cm⁻¹·전도도 vs 밀링 시간 | 높음 |
| **Fig. S29a–e** | 탄소 종류(AB·VGCF·KB)별 이용률·수명 | 높음 |
| Fig. S2 | LPSCl 사전분쇄 입도 | 중간 |
| Fig. S5 | TGA 로 황 정량 | 중간 |
| Fig. S6·S7 | cryo-TEM/HAADF + 라인스캔 (Table S1) | 중간 |
| Fig. S8a–b | LPS vs LPSCl 전도도·성능 | 중간 |
| Fig. S12 | LPS 와 LPSCl 의 환원 전위 비교 | 중간 |
| Fig. S14·S16 | 사이클 후 Raman | 중간 |
| Fig. S15 | 충전 후 임피던스 복귀 | 중간 |
| Fig. S17–S20, Table S5 | XANES 참조 스펙트럼·LCF 전문 | 중간 (G11 판정에 필요) |
| Fig. S21·S22 | XRD/XANES 용 셀의 전기화학 | 낮음 |
| Fig. S23–S27 | 입도 SEM·XRD | 중간 |
| Fig. S28a–b | 2사이클 분극·율속 | 중간 |
| Fig. S30·S31 | EIS 차이·단면 SEM("indistinguishable") | 중간 |
| Fig. S32·S33 | 부피팽창 산정 | 낮음 |
| Fig. S34a–b | Li2S 탈리튬화 균열 | **높음** (우리 첫 충전 문제와 직결) |
| **Fig. S35** | µSi‖Li2S 140 사이클 83 % | **높음** |
| Tables S6·S7 (또는 S3·S4 — G13) | FEM 파라미터 | 낮음 |
| **Table S8** | 에너지밀도 계산 가정 | 높음 (G17) |
| Table S4 | TGA 황 정량 | 낮음 |

---

## 11. 우리 연구와의 접점

| 이 논문 | 우리 ([[li2s-assb-reference-cell]]) | 옮겨 올 수 있는 것 | 옮겨 올 수 없는 것 |
|---|---|---|---|
| **AM : LPSCl : AB = 30 : 50 : 20**, 바인더 없음, Li–In, 75 MPa, 25 °C | **동일** | **조성·셀 구성이 같다 — 직접 비교 대상** | 활물질이 주로 S8 이다 |
| **one-step 500 rpm 1 h BPR 1:30 planetary** | one-step/two-step 비교 중 | **구체적 밀링 레시피 전부**; 대조군 설계(손혼합·multi-step)도 그대로 | 장비 기종별 충돌에너지 차이(G7) |
| **LPSCl 사전분쇄 400 rpm 2 h 5 mm YSZ** | 미정 | **catholyte 전처리를 별도 공정으로 둔다는 발상** | — |
| **"세게, 짧게" — 1 h 넘기면 LPSCl 전도도 1.3e-3 → 4e-5 S cm⁻¹** | 밀링 시간 미정 | **밀링 시간을 변수로 두고 상한을 둔다** | 절대 시간(용기·볼이 다르면 다르다) |
| **Li2S 활성화 전위 2.4 V, 촉매 없음** — LPSCl 이 2.3 V 에서 산화되며 매개 | 첫 충전 활성화가 병목(H1) | **"매개체를 밀링으로 미리 만든다"는 경로** ([[li2s-activation-first-charge]]) | 전압 기준(G3) — Li–In 오프셋을 우리가 정해야 함 |
| **Li2S 계에서 밀링만으로 LPSCl 절반이 LPS 로** (Fig. 4f pristine) | 같은 밀링을 하면 같은 일이 일어난다 | **"SE 분해 = 손실" 이라는 전제를 의심할 근거** | 오차막대가 커서 분율은 정밀값 아님 |
| **micron(0.5–5 µm) > sub-micron** (500 사이클 81 vs 61 %) | 나노화 시도 중(H3) | **"나노가 항상 낫지 않다"** — 이용률과 수명의 트레이드오프 | 황 입자 기준. Li2S 에서 같은지 미검증 |
| **AM 30 wt% 에서 토르투오시티 τ ≈ 2–3.4 로 아직 완만** (Fig. 5c) | 우리도 30 wt% | **우리 조성에서 이온 경로는 1차 병목이 아닐 수 있다**(H2 반증 재료) | 구형 황 가정의 모델. 실측 아님 |
| **Li2S 는 탈리튬화에서 42 % 수축 + 주상 균열** (Fig. 6b) | 첫 충전 문제 | **첫 충전 손실의 새 가설: 수축 균열에 의한 접촉 상실** | — |
| **CE 129 %, 1694 mAh g⁻¹(S) = SSE 기여 포함** | 용량 해석 | **"이론값 초과 = SSE redox" 를 먼저 의심하는 습관** + dQ/dV 분해법 | 우리 셀에서 분해하려면 LPSCl-only 대조셀이 필요 |
| **mAh g⁻¹(active = AM + SE)** 네 번째 기준 | 단위 규율(H4) | **[[capacity-normalization-li2s-vs-sulfur]] 에 열 추가** | ×(80/30) 로 g(S) 환산은 무의미 |
| **anode-free Li2S 파우치 503 Wh kg⁻¹, 10 MPa** | 2단계 | **Ag–C 집전체 레시피(69.75:23.25:7.0)·저압 운전·건식 공정** | **60 °C**, WIP 500 MPa 장비, 50 사이클뿐 |
| **셀 3개씩 제작** | 재현성 | **"n = 3" 을 기본 규율로** | 그들도 오차를 그리지 않았다(G4) |

### 가장 값싼 다음 실험 `[해석]`

1. **밀링 시간 스윕 (30 min / 1 h / 2 h / 4 h), 조성·rpm 고정.** 각 조건에서 (a) 복합체
   Ti‖composite‖Ti 이온전도도, (b) 첫 충전 용량·과전압. 이 논문의 "1 h 부근이 최적" 이
   우리 장비에서도 성립하는지가 **가장 싼 검증**이다.
2. **LPSCl + AB (80:20) 대조셀을 Li–In 으로 한 번 돌린다.** 우리 셀에서 SSE 가 내는 용량을
   빼야 "Li2S 이용률" 을 말할 수 있다. 이 논문의 115 / 355 mAh g⁻¹ 이 우리 LPSCl 에서도
   나오는지 확인 — **분모 논쟁(H4)을 실측으로 끝내는 방법**이다.
3. **첫 충전 후 단면 SEM.** Li2S 수축 균열(42 %)이 우리 펠릿에도 있는지. 있으면 성형압·
   스택압이 새 변수가 된다.

---

## 12. 다른 digest 와의 대조

### 12.1 Huang 2026 (`raw/papers/huang2026_high-entropy-sulfides-kinetic-accelerators-assb.md`)

같은 **LPSCl · Li–In · S8 · 상온** 계.

| | Huang 2026 | Cronk 2026 |
|---|---|---|
| 양극 | S : HES : KB : LPSC = 42 : 6 : 12 : 40 | **S : LPSCl : AB = 30 : 50 : 20** |
| 혼합 | S+KB 그라인딩 → 155 °C 12 h 융합 → LPSC 와 350 rpm 4 h | **one-step 500 rpm 1 h** |
| 탄소만일 때 S 이용률 | `[도표]` **39 %** @0.1 C | **84 %** @C/20 (`[인쇄]`, Table S3) |
| 첨가제 | 고엔트로피 황화물 6 wt% → 76 % | **없음** (SSE 자신의 분해산물) |
| 운전 스택압 | **미기재** | **75 MPa 명시** |

`[해석]` **같은 "탄소만" 조건에서 이용률이 39 % 와 84 % 로 두 배 넘게 갈린다.** 전류(0.1 C vs
C/20)·탄소(KB vs AB)·로딩·SE 함량이 다르므로 직접 비교는 아니지만, **Huang 이 첨가제로 메운
간극을 Cronk 는 혼합 에너지로 메웠다**는 읽기가 가능하다. 이것은
[[reference-cell-500-600-mahg]] H2 에 대한 **중요한 반대 해석**이다 — 삼상 계면 부족이
"탄소의 한계" 가 아니라 "혼합 공정의 한계" 일 수 있다.

### 12.2 Zhang 2026 (`raw/papers/zhang2026_anode-free-assb-nanocrystalline-amorphous-li2s-na-collector.md`)

| | Zhang 2026 | Cronk 2026 |
|---|---|---|
| pristine(상용) Li2S 첫 방전 | `[도표]` **≈270 mAh g⁻¹(Li2S)** (대조군) | **723 mAh g⁻¹(Li2S)** `[인쇄]` (as-received Li2S, one-step) |
| SE | LPSCBr | **LPSCl** (우리와 같다) |
| 탄소 | MWCNT 10 wt% | **AB 20 wt%** (우리와 같다) |
| 혼합 | two-step 고에너지 (3D swing 1400 rpm) | **one-step 고에너지 (planetary 500 rpm 1 h)** |
| 활성화 보조 | **PI3 → LiI** (양극의 43.8 wt% 대가) | **없음** — LPSCl 분해산물 LPS |
| anode-free | Na 박, **25 °C**, 1–4 MPa, 400 사이클 | Ag–C/STS, **60 °C**, 10 MPa, 50 사이클, **파우치** |

`[해석]` **두 논문이 pristine Li2S 에 대해 정반대 값을 준다 (270 vs 723).** 차이의 후보는
(i) 혼합 경로(two-step vs one-step), (ii) SE(LPSCBr vs LPSCl), (iii) 탄소(MWCNT 10 vs AB 20),
(iv) 조건 미상(Cronk 의 723 은 로딩·전류·컷오프 불명 — G2), (v) **정규화 기준**(Cronk 의 다른
값들은 SSE 기여를 포함한다 — 723 도 그럴 수 있다). **Zhang 의 270 을 "pristine Li2S 의 천장"
으로 읽던 이 위키의 잠정 결론은 이 논문으로 흔들린다.** 두 값을 같이 적어 두고
[[reference-cell-500-600-mahg]] 에서 disputed 로 관리해야 한다.

### 12.3 Kim 2023 (액체계)

- Kim 2023 의 ref 15(Kim, Choi, Hwang, Yoon, Sun, *ACS Energy Lett.* 2023, "Tailoring the
  interface between sulfur and sulfide solid electrolyte…")가 **이 논문의 서론에서
  '용매를 쓴 선행 연구'로 인용**된다. 같은 아이디어(S–SE 계면 thiophosphate)를 **용액으로**
  한 것이 그쪽, **무용매 기계화학**으로 한 것이 이쪽이다.
- 공통 결론: **첫 충전/첫 방전의 활성화량이 이후 용량을 정한다**, **압축 성형이 접촉을 만든다**.
- 차이: Kim 2023 은 탄소 차원(2D+1D)으로 풀었고, Cronk 2026 은 **SE 계면 화학**으로 풀었다.

---

## 13. 비판 (이 digest 의 판단)

1. **"highly utilized" 의 근거가 SI 한 칸(Table S3)에 있다.** 본문의 눈에 띄는 숫자
   (1500·1615·1694 mAh g⁻¹(S), CE 129 %)는 **전부 SSE 기여가 섞인 값**이고, 저자들도 그것을
   숨기지 않는다. 그러나 **정작 "84 % 이용률" 이라는 정제된 숫자의 계산은 보이지 않는다** (G5).
   초록의 첫 형용사가 검증 불가능한 자리에 놓여 있다.
2. **sub-micron 이 지는 이유의 논증이 소거법이다** (§7.6). 탄소 배제는 SI 그림 하나, EIS 차이는
   저자 스스로 "marginal", SEM 은 "indistinguishable", FEM 평균 응력은 **2.42 vs 2.40 GPa**.
   남은 것은 응력 분포의 꼬리뿐이다. 결론(micron 이 최적)은 실측으로 서지만 **기전 설명은 약하다**.
3. **셀 3개를 만들었다고 Methods 에 쓰고도 오차를 한 번도 그리지 않았다** (G4). 81 % vs 61 %,
   86.8 %, 77.4 %, 86.6 % — 전부 단일 곡선이다. 기업 공동연구에서 n = 3 을 확보하고도
   분산을 보여주지 않은 것은 아깝다.
4. **전압 기준 관리가 허술하다** (G3). Li–In, Li2Si, µSi, anode-free 넷의 컷오프를 모두
   "vs Li/Li⁺" 로 적었다. anode-free 파우치에는 성립하지 않는 표기이고, 실제 Fig. 7j 축은
   기준 없이 "Voltage (V)" 다. **우리가 2.4 V 활성화 전위를 인용하려면 이 대목을 먼저 정리해야 한다.**
5. **유지율의 기준 사이클이 그림마다 다르고(2nd / 3rd), 본문과 그림의 사이클 수가 어긋난다**
   (150 vs 147 — G12). 단위 오타도 여러 곳(A g⁻², mAh cm⁻² 전류, C/10 = 1 A g⁻¹ — G12).
   **Nature Communications 의 교정이 이 정도 통과한 것은 의외다.**
6. **"practical" 과 "500 Wh kg⁻¹" 은 모델이다** (G17). 실제로 만든 것은 **15 mAh 파우치,
   60 °C, 50 사이클**이다. 초록은 "operates under 'low stack pressure' of 10 MPa" 를 따옴표까지
   붙여 강조하지만, 그 셀은 조립 때 **WIP 500 MPa · 80 °C** 를 거쳤고 **60 °C 에서 운전**한다.
7. **SSE 가 용량을 내는 것을 이점으로만 서술한다.** LPSCl 이 매 사이클 산화되면 LiCl 이 쌓이고
   활물질 질량이 변한다. 본문은 "4 V 아래 컷오프가 완전 산화를 막는다"고만 하고, **500 사이클
   후 SE 조성을 재지 않았다**(XANES 는 1사이클만). 장기적으로 이 기여가 유지된다는 증거는 없다.
8. **Li2S 계가 곁가지로 밀려 있다** (G2). 논문 제목은 "lithium-sulfur positive electrode" 이고
   초록은 anode-free Li2S 파우치를 앞세우지만, **Li2S 에 대한 본문 데이터는 한 문단·한 숫자**다.
   나머지는 전부 SI 로 밀렸다.
9. **좋은 점도 분명하다.** (a) **용량 분해를 시도했고 산술이 맞는다** (§5.4 의 553 mAh g⁻¹ 재현
   확인). (b) 다섯 가지 독립 관측(XRD·Raman·XANES·TGA·EIS)이 같은 방향을 가리킨다.
   (c) **기하 모델 + FEM 을 실험 설계에 먼저 쓰고 실측으로 검증**하는 순서가 정직하다.
   (d) **operando 압력**으로 "양극이 음극 부피변화를 상쇄한다"는 비직관적 주장을 실측했다.
   (e) **밀링 조건을 이 위키의 어떤 논문보다 잘 적었다.** (f) 실패 조건(hand-mix, multi-step,
   LPS catholyte, sub-micron, bulk)을 모두 보여 준다.

---

## 14. 이 저장소가 가져갈 것

- **[[one-step-vs-two-step-mixing]] — H3(one-step 우세)에 대한 고체계 직접 근거.**
  같은 조성·같은 SE·같은 탄소에서 one-step(CE 129 %, ≈1500 mAh g⁻¹(S)) ≫ multi-step
  (CE 17 %, ≈610) ≫ hand-mix (≈200). Li2S 에서도 같은 순서(one-step 723 mAh g⁻¹(Li2S),
  CE 99.3 % / multi-step 저이용률·큰 분극 / hand-mix **사이클 불가**).
  **단서**: 이 논문의 "multi-step" 은 SE 를 **손으로** 붙인 것이라 우리의 two-step(SE 를 mild BM)
  과 다르다. 배제된 것은 "SE 를 저에너지로 붙이는 경로" 이지 two-step 일반이 아니다.
- **[[reference-cell-500-600-mahg]] — 네 가설 전부에 근거가 붙는다.**
  H1: Li2S 활성화 전위 2.4 V 를 촉매 없이 달성, 매개체를 밀링으로 미리 생성.
  H2: AM 30 wt% 에서 τ ≈ 2–3.4 (모델) — 우리 조성에서 이온 경로가 1차 병목이 아닐 수 있다.
  H3: micron > sub-micron (500 사이클 81 vs 61 %) — 나노화가 항상 답이 아니다.
  H4: mAh g⁻¹(active = AM + SE) 라는 네 번째 기준의 등장.
  그리고 **새 경로 H5 후보**: Li2S 탈리튬화 42 % 수축 + 주상 균열에 의한 접촉 상실.
- **[[li2s-activation-first-charge]] 갱신**: "SSE 분해산물(LPS)을 리독스 매개체로 미리 만들어
  활성화 전위를 낮춘다" 를 새 항목으로. Zhang 2026 의 LiI, Huang 2026 의 HES 와 **같은 자리를
  무게 대가 없이 채우는 세 번째 방식**.
- **[[capacity-normalization-li2s-vs-sulfur]] 갱신**: `mAh g⁻¹(active = AM + catholyte)` 열 추가
  + "이론값 초과 = SSE redox 를 먼저 의심" 규율 + 이 논문의 설계용량 관례
  (S 1600 / Li2S **1100** mAh g⁻¹ — 이론 1166 이 아니다).
- **[[composite-cathode-mixing-routes]] 갱신**: one-step 열에 **500 rpm / 1 h / BPR 1:30 /
  planetary / Ar / LPSCl 사전분쇄 400 rpm 2 h 5 mm YSZ** 를 구체 수치로. 그리고 **"밀링 시간
  상한" 이라는 새 축** (LPSCl 단독 10 h 에서 전도도 30배 하락).
- **[[carbon-dimensionality-electron-network]] 갱신 (약한 근거)**: 탄소 비표면적을 올리면
  **이용률은 오르지만(주로 SSE 기여) 수명은 그대로** — AB 20 wt% 를 바꿀 유인이 약하다는
  고체계 관측. 단 수치가 SI 에만 있다 (G18).
- **[[anode-free-li2s-assb]] 갱신**: Ag–C/STS 집전체 레시피, 10 MPa 운전, 50 µm 분리층,
  건식 공정, 503 Wh kg⁻¹ 전망. **60 °C·50 사이클이라는 한계를 같이 적는다.**
- **새 개념 후보**: `sse-redox-capacity-contribution` (황화물 SE 가 내는 용량 — 정의·측정법
  (LPSCl-only 대조셀 + dQ/dV + XANES LCF)·분모 문제). 이 위키의 세 고체계 digest 가 모두
  이론값 초과 용량을 보고했으므로 **3편 이상 기준을 충족**한다.
- **새 개념 후보**: `li2s-delithiation-contraction-cracking` (Li2S 42 % 수축·주상 균열·
  양극이 음극 부피변화를 상쇄) — 아직 이 논문 단독이므로 `single-source` 로 시작.

---

## 15. 그림 판독 기록 (무엇을 보고 무엇을 안 봤는가)

| 그림 | 봤는가 | 어디에 썼는가 |
|---|---|---|
| **Fig. 1** (개념도) | ✓ | §2, §5.6 (반응식·V_p/V_d 도식) |
| **Fig. 2** (a–d) | ✓ | §4.1–4.5 — a 의 곡선 끝점, c 의 149 cm⁻¹, d 의 2471.0 라벨(G8)은 도표 판독 |
| **Fig. 3** (a–d) | ✓ | §5.3–5.5 — **자동 크로핑이 a·c 만 잡아 bbox 를 넓혀 재크로핑**했다 |
| **Fig. 4** (a–f) | ✓ | §6.1–6.4 — **재크로핑**. d–f 의 막대 높이는 전부 도표 판독(G11) |
| **Fig. 5** (a–h) | ✓ | §7.2–7.6 — 가장 오래 봤다. b·c·e·f·h 의 값은 도표 판독 |
| **Fig. 6** (a–d) | ✓ | §8.1–8.2 — 두께 수치는 그림 안 라벨(인쇄) |
| **Fig. 7** (a–k) | ✓ | §9 전체 — **재크로핑**. b·e·f·k 의 곡선 값은 도표 판독 |
| **SI Fig. S1–S35** | **✗ 파일 없음** | **하나도 못 봤다** (G1). 본문의 요약만 옮겼고 그 사실을 §10 에 표로 남겼다 |
| **Table S1–S8** | **✗ 파일 없음** | 위와 같음 |

**본문 서술과 그림이 어긋난 곳**: G8(pre-edge 2470.1 vs 2471.0) · G9(0.52 mA cm⁻² vs
C/20 0.1 A g⁻¹) · G11(충전 후 황 32 vs ≈27 wt%) · G12(150 vs 147 사이클, 축 단위 오타 3곳).
**본문 안에서 서로 어긋난 곳**: G10(10 vs 11 mAh cm⁻² — 정의 차이로 설명 가능) ·
G13(Tables S6·S7 vs S3·S4).
**산술이 맞는 것을 확인한 곳**: §5.2(0.984 mAh) · §5.4(553 mAh g⁻¹) · §8.1(4.92 µm mAh⁻¹) ·
§9.4(15.2 mAh) — 이 논문의 계산 사슬은 재현 가능하다.

<!-- digest 표준 양식 (paper-level STANDALONE). 깊이·양식 기준 = nolan2021_garnet_cathode_coating.md.
     ★ = 1저자가 이 편에 특별히 물은 것 (계산↔실험 맞물림 · 우리 계(황화물/아지로다이트) 취급 분량 · sei_products 대조 · Meng 계보).
     ⚠ 이 파일의 slug 는 의뢰서의 제안(banerjee2020…)과 다르다. 이유는 §0a — **저자가 다르다.** -->
# Understanding interface stability in solid-state batteries — **Xiao**, Wang, Bo, Kim, Miara, **Ceder** (*Nature Reviews Materials* **5**, 105–126, 2020)

> slug `xiao2020_interface_stability_ssb_review` · DOI `10.1038/s41578-019-0157-5` · type `review (계산 0 · 실험 0 — 전편이 문헌 종합. 250 refs · Fig 1–7 + Table 1)` · PDF `litdb/inbox/112. Banerjee2020_Understanding_Interface_Stability_in_Solid_State_Batteries_REVIEW.pdf` (22 pp = 지면 105–126, SI 없음) · digested `2026-09-12` · status ✅
> elements: Li, Na, P, S, Se, O, Cl, Br, I, N, H, B, Al, Si, Ge, Sn, Ti, Zr, Nb, Ta, La, Co, Ni, Mn, Fe, Sb, In
> methods: DFT, AIMD, ESW, XPS, Raman
>
> **저자(PDF 표지 실물)**: **Yihan Xiao**¹'², Yan Wang³, Shou-Hang Bo²'⁴, Jae Chul Kim²'⁵, Lincoln J. Miara³, **Gerbrand Ceder**¹'²\* — ¹UC Berkeley MSE · ²**LBNL Materials Sciences Division** · ³**Advanced Materials Lab, Samsung Research America** (Burlington, MA) · ⁴UMich–SJTU Joint Institute, 상하이교통대 · ⁵Stevens Institute of Technology. 교신 `gceder@berkeley.edu`. *Nat. Rev. Mater.* **5**, 105–126 (2020년 2월호) · **온라인 게재 2019-12-09** · © Springer Nature 2019.
> **저자 기여(원문 그대로)**: *"G.C. conceived the manuscript. Y.X. researched the data. **S.-H.B. and Y.X. wrote the section on sulfides.** Y.X. wrote the sections on garnets and coatings. J.C.K. wrote the sections on LiPON and antiperovskites. Y.W. and Y.X. wrote the sections on perovskites and NASICONs. G.C., Y.X. and L.J.M. wrote the discussion and conclusions."*
> **연구비**: 이온전도도 설계 = **Samsung Advanced Institute of Technology**; **계면 반응성 이론 = Materials Project Program (KC23MP, DOE BES DE-AC02-05CH11231)**; 황화물 일부 = DOE VTO Advanced Battery Materials Research. 이해상충 없음 선언.
> ⚠ 표지 하단에 *"There are amendments to this paper"* 표기 — **이 PDF 에는 정정 내용이 포함돼 있지 않다.** 정정본을 확인하기 전에는 개별 수치를 최종본으로 단정하지 않는다 (§10-1).

---

## 0. 이 digest 를 읽는 법

### 0a. ⛔⛔ 서지 정정 — **이 논문은 Banerjee 도, Meng 그룹도 아니다** (이 건의 첫 작업)

의뢰서와 계보 카드가 이 편을 *"**Banerjee**/Wang/**Meng** — Understanding interface stability in SSB"* 로 적어두었고, 동시에 *"1저자 Yihan Xiao"* 라는 상충 메모가 붙어 있었다. **PDF 표지를 실제로 열어 확인한 결과, 맞는 쪽은 "Xiao" 다.**

| 항목 | 계보 카드·파일명 주장 | **PDF 실물 (p105 표지 + 저자기여 + 감사의 글)** | 판정 |
|---|---|---|---|
| 1저자 | Banerjee (파일명) / Xiao (메모) | **Yihan Xiao** (UC Berkeley MSE + LBNL) | 메모가 맞다 |
| 교신 | Meng | **Gerbrand Ceder** (`gceder@berkeley.edu`) | **카드가 틀렸다** |
| 공저 "Wang" | (Meng 그룹 Wang 으로 암시) | **Yan Wang** — Samsung Research America. Meng 그룹의 Xuefeng Wang 이 **아니다** | **카드가 틀렸다** |
| 저널·연도 | Nat. Rev. Mater. 2020 | **Nat. Rev. Mater. 5, 105–126 (Feb 2020)**, 온라인 2019-12-09 | ✅ 일치 |
| DOI | `10.1038/s41578-019-0157-5` | **동일** | ✅ 일치 |
| 쪽수 | 22 p | **22 p (105–126)** | ✅ 일치 |

**무슨 일이 있었나 (가장 그럴듯한 경위, 단정 아님)**: 2020년에 제목이 비슷한 SSB 계면 리뷰가 **둘** 나왔다. 하나가 이 편(Xiao/Ceder, *Nat. Rev. Mater.*)이고, 다른 하나가 흔히 *"Banerjee, Wang, Meng"* 으로 인용되는 UCSD 리뷰다. 두 편 다 저자 목록에 "Wang" 이 있다. **파일명 `112. Banerjee2020_…` 은 제목·DOI·쪽수가 전부 Xiao 편과 일치하므로, 내용물은 Xiao 편이고 파일명만 다른 리뷰의 이름이 붙은 것**이다. ⚠ 다만 **이 digest 는 Banerjee 편 PDF 를 갖고 있지 않다** — 그 편의 서지(저널·권·쪽)를 여기서 확정하지 않는다. 확인 없이 옮겨 적으면 오기를 하나 더 만든다.

⇒ **조치 3가지**
1. **slug 를 `xiao2020_interface_stability_ssb_review` 로 쓴다** (의뢰서의 `banerjee2020_…` 제안을 기각). 우리 규칙이 `<1저자><연도>_<주제>` 이고 1저자는 Xiao 다. `litdb/figures/` 폴더도 같은 이름으로 만들었다.
2. **계보 카드 #8 행의 저자 칸을 고쳐야 한다** — 완성 문구는 파일 끝 `MERGE-BLOCK` 에 넣었다 (이 digest 는 공유 파일을 직접 안 건드린다).
3. ⛔ **"Cronk 2026 과 같은 Meng 그룹" 이라는 계보 카드의 연결은 무효다.** 이 편은 **Ceder 그룹 + Samsung** 이다. Cronk 2026 두 편과의 관계는 *같은 그룹*이 아니라 **"계산이 깐 전제 ↔ 6년 뒤 실험이 밟은 자리"** 라는 다른 종류의 연결이다 (§7f 에서 다시 세운다).

> 🧭 **역설적 소득**: 이 정정으로 계보가 오히려 **더 깨끗해진다.** #3 `Xiao 2019` (Joule) 과 #8 이 **같은 1저자·같은 교신·같은 Samsung 공저자**다. 즉 #8 은 남의 리뷰가 아니라 **#3 저자들이 자기 방법을 실험 문헌 전체에 대고 채점한 편**이고, 실제로 본문에서 #3 을 `ref.67` 로 **14회** 인용하고 `Fig. 5a` 를 통째로 재수록한다.

### 0b. 본 그림 / 안 본 그림 — **그림 7장 + 표 1장 중 그림 7장 전부 실독**

| | 무엇 | 봤나 |
|---|---|---|
| `Fig. 1` | 양극 복합체 계면 목록 모식도 | ✅ 봤다 (자동 크로핑이 건너뛴 것을 수동 bbox 로 복구) |
| `Fig. 2` | 계면 모델 4종 (grand-potential hull · topotactic · 혼합 · explicit) | ✅ 봤다 |
| `Fig. 3` | 황화물 불안정성 (EIS·CV·XPS·STEM-EDS) | ✅ 봤다 — **자동 크로핑이 a·b 패널을 잘라먹어** 쪽 렌더로 다시 봤고, 저장본 bbox 도 고쳤다 |
| `Fig. 4` | 가넷 불안정성 (CV·Zr 3d XPS·유사이원·전압의존) | ✅ 봤다 |
| `Fig. 5` | **폴리음이온 산화물 = 산화물·황화물 사이 다리** (반응에너지 히트맵 + 3분할 도식) | ✅ 봤다 (크로핑 복구 + **§12a 픽셀 정량화**) |
| `Fig. 6` | **전 SE ESW 지도** (산화한계 × 환원한계 × σ) | ✅ 봤다 (자동 크로핑 실패 → 복구 + **§12b 벡터/픽셀 정량화**) |
| `Fig. 7` | 조성 튜닝의 trade-off 파이차트 5종 | ✅ 봤다 (크로핑 복구) |
| `Table 1` | 음이온별 Li 금속 대비 양이온 분류 (stable / SEI former / MCI former) | 📄 **이미지로 안 봤다 — PDF 텍스트로 전문 읽었다** (관례: 표는 텍스트가 정확) |

**안 본 그림 0장.** 단 `Fig. 3`·`Fig. 4`·`Fig. 5`·`Fig. 7` 은 전부 **남의 논문에서 재수록한 패널**이라, 여기서 읽은 값은 *원출처의 값을 이 리뷰가 재현한 것*이지 이 리뷰가 만든 값이 아니다 (§10-3).

### 0c. 가져올 수 있는 것 / 없는 것

- ✅ **가져온다**: 계면 4분류 문법(type I/II/III + MCI/SEI) · **계산 모델 4층의 위계**(§4) · *"CV 는 창을 넓게 읽는다"* 의 원인 분석과 처방 · 황화물/아지로다이트의 **예측 산물 ↔ 관측 산물 대조표**(§5·§6) · Fig 5a·Fig 6 의 지도.
- ⛔ **안 가져온다**: 이 편 고유의 새 수치는 **하나도 없다** (자체 계산 0). 모든 숫자는 소환값이고 **원출처가 따로 있다** — 원출처 ref 번호를 반드시 달고 쓴다.
- ⛔ **우리 db 절대값과 같은 표에 놓지 않는다**: 이 편이 옮겨 적은 ESW·반응에너지는 2015–2019년 hull 세대(MP/OQMD 구세대)다. 우리 2.256 V·−0.3227 eV/atom 은 MP2026 세대다 (§7e).

---

## 1. 한 줄 요약

SSB 의 병목은 이제 벌크 전도도가 아니라 **계면**이고, 계면 안정성은 **네 층의 계산 모델**(① grand-potential ESW = 최악 시나리오 · ② topotactic = 최선 시나리오 · ③ pseudo-binary 화학혼합 = 최대 구동력 · ④ explicit 계면 슈퍼셀/AIMD = 국소 재배열)로 **상한과 하한을 괄호치는 방식**으로 다뤄야 한다 — 그리고 2015–2019년의 실험(고감도 CV·operando XPS·ToF-SIMS·cryo/STEM-EDS·성분분해 EIS)이 그 예측을 **정성적으로는 거의 전부, 정량적으로도 상당 부분 따라잡았다**. 황화물은 **S²⁻ 산화가 ~2–2.5 V** 에서 켜지고(CV 가 주장해온 0–5 V 는 **전류가 안 보였던 것**이지 안정했던 게 아니다 — 탄소를 섞어 반응면적을 키우면 2.1 V 에서 바로 보인다), 산화물 양극과는 **S↔O 교환 + Li₃PO₄ 형성**이라는 큰 구동력(>300 meV/atom)으로 반응하며, Li 금속 쪽에서는 P⁵⁺·Ge⁴⁺·Sn⁴⁺·Ti⁴⁺ 환원이 **전자전도성 MCI** 를 만든다. 해법은 **코팅 또는 자기부동태화**뿐이고, 조성으로 푸는 다섯 레버 중 **"공유결합성 M–X 혼성(P–O·B–O)" 하나만이 σ·환원·산화 셋을 동시에 개선**한다(`Fig. 7`).

## 2. 메타 — 이 논문이 litdb 에서 차지하는 자리

| 항목 | 내용 |
|---|---|
| 연구유형 | **리뷰**. 자체 DFT 0 · 자체 실험 0 · SI 없음. 250 refs. |
| 다루는 SE | **황화물**(thiophosphate·LGPS 계열·**아지로다이트**) · 가넷 · LiPON · 페로브스카이트(LLT) · 반페로브스카이트(Li₃OCl) · NASICON(LATP/LAGP) · (할라이드는 `Fig. 6` 점 2개 + 본문 한 문단) |
| 핵심 질문 | *"계산이 예측한 계면 분해산물이 실험에서 실제로 보이는가, 안 보이면 왜인가"* |
| 우리 질문(이 카드) | ① 계보 #1–#7 의 계산틀(`E_d`·ESW·hull)이 여기서 **실험 관측과 어떻게 맞물리나** ② **우리 계(Li₆PS₅Cl)가 얼마나·얼마나 구체적으로 다뤄지나** ③ 우리 `sei_products.json`·`interface_reactivity` 산물과 겹치나 |
| ⭐ **우리 무대 등장 여부** | **등장한다.** 「Sulfides」 대절(지면 109–112, 약 3.5쪽)에 **「Argyrodites」 전용 소절**이 있고, `Fig. 5a` 히트맵의 **행·열 라벨에 `LPSCl` 이 직접 찍혀 있다**. ⚠ **다만 "계보 최초" 는 아니다** — 같은 날 나온 형제 digest `nolan2018_computation_accelerated_design_review`(#7) 에 따르면 그 편도 `Li₆PS₅Cl` 을 본문 3회 명시하고 **창 수치(1.7/2.4 V, [Zhu15]·[Rich16] 2차 인용)까지 준다**. 정확히 말하면 **#1–#6 에는 우리 계가 없었고, 두 리뷰(#7·#8)에서 함께 들어온다**. 둘의 성격이 다르다: **#7 은 소절 없이 수치를 주고, #8 은 전용 소절을 두되 고유 수치를 안 준다** (§3d·§10-7). ⚠ #7 쪽 서술은 **형제 digest 를 읽은 것**이지 그 PDF 를 본 것이 아니다 |
| 관련 카드 | `xiao2019_cathode_coating_screening`(= 본문 **ref.67**, 같은 1저자·교신 — `Fig. 5a` 의 원출처) · `richards2016_interface_stability_pseudobinary`(**ref.64**) · `zhu2015_esw_grand_potential_origin`(**ref.66**; ref.65 = Zhu 2016 JMCA) · **`nolan2018_computation_accelerated_design_review`(= 본문 ref.233, 계보 #7, Mo 그룹 교과서 — 같은 날 작성된 형제 digest)** · `nolan2019_…`·`nolan2021_…` · `cronk2026_lis_cathode_interphase_chemistry`·`cronk2026_lis_positive_electrode_geometry_fem`(§7f) · `zuo2022_chlorination_cathode_interface` |
| 🎤 관련 발표 | **없음** — `litdb/talks/*.md` 의 "논문 에이전트 인입 대기열" 을 grep 한 결과 이 논문 행 없음 (2026-09-12 확인) |

---

## 3. 핵심 수치 총정리 — **전부 소환값. 원출처 ref 를 같이 적는다**

> ⚠ 이 표의 모든 값은 **이 리뷰가 옮겨 적은 남의 값**이다. 원고에 쓸 때는 이 리뷰가 아니라 **원출처**를 인용하고, 원출처의 DB 세대·기준전극을 확인한다.

### 3a. 황화물 — 전기화학 창 (우리 축 B①)

| 계 | 값 | 종류 | 원출처(ref) |
|---|---|---|---|
| 황화물 일반 | **S²⁻ 산화 ~2–2.5 V** vs Li | DFT 예측 | 64(Richards 2016) · 65(Zhu 2016 JMCA) · 66(Zhu 2015 ACS AMI) |
| 황화물 일반 | **창 1.5–2.5 V** | DFT 예측 | 64,65,66,95,96 |
| **LGPS** | **1.7–2.1 V** | DFT | 65 |
| **LGPS** | **2.1–2.3 V** | DFT (다른 hull 세대) | 64 |
| **LGPS** | 산화 개시 **≈2.1 V** / 환원 **1.7 V** | **실측 CV (탄소 혼합 복합 WE)** | 97(Han 2016 AEM) · 98(Han 2015 Adv Mater) |
| Li₂S–P₂S₅ | 산화 개시 **≈2.7 V** | **operando XPS** | 99(Wu 2018 PCCP) |
| Li₁₀SnP₂S₁₂ | 예측 **1.78–2.02 V** / CV 실측 **1.5–2.5 V** (3전극, Li 대극 회피) | DFT / CV | 43 / 101 |
| **Li₃PS₄ 환원한계** | **1.69 V** (본문 인쇄값) | DFT | 본문 「Trade-offs」절 |
| Li₃PO₄ 환원한계 | **0.71 V** (P–O 혼성 대조군) | DFT | 동일 |
| Na₃PS₄ / Na₃PSe₄ | 예측 **1.55–2.25 / 1.80–2.15 V**; 실측 **0.9–2.5 / 1.25–2.35 V** | DFT / 액체셀 저속 GITT | 50(Tian 2017 EES) |
| Na₃PSe₄ | **V_topo,ext = 2.75 V** | topotactic DFT (`Fig. 2b`) | 50 |

### 3b. 황화물 — 화학혼합(양극 상대) · 우리 축 B③

| 계면 | 값 | 원출처 |
|---|---|---|
| 황화물 ↔ 산화물 양극 일반 | **>300 meV/atom** (구동력) | 64,65,95,105 |
| `Fig. 5a` 히트맵 (ref.67 재수록) — **LPSCl 행** | **figure-read ≈ −308 (LCO) / −298 (NCM) / −424 (LMO) / −100 (LFPO) meV/atom** | 67 = Xiao 2019 Joule. ⚠ **정본은 Xiao 2019 Table S2 의 −339 / −330 / −421 / −101** — §12a |
| 같은 히트맵 — LGPS·LPS 행 | figure-read ≈ LGPS\|LCO −334 · LPS\|LCO −429 · LPS\|LMO −540 · **LLZO\|LCO ≈ 0** | 67 |
| 같은 히트맵 — **코팅 ↔ LPSCl** | figure-read ≈ LiNbO₃ **−133** · LiTaO₃ **−119** · Li₂ZrO₃ **−85** · LiPO₃ **−56** · LiH₂PO₄ **−54** · **LiBa(B₃O₅)₃ ≈ 0** | 67 |
| 본문 명시 | LiNbO₃·LiTaO₃ 코팅 ↔ 황화물 SE **">100 meV/atom"** | 65,67 |
| Li₃PO₄ 생성엔탈피 | **−2.767 eV/atom** (본문 인쇄, *"deep formation energy"*) | 67 |
| Co 확산 | LiCoO₂/Li₂S–P₂S₅ 1차 충전 후 **>50 nm** | 47(Sakuda 2010 Chem Mater) — `Fig. 3d` |
| 결합에너지 근거 | **P–O 596.6 kJ/mol vs P–S 346 kJ/mol** | 106(Lange's Handbook) |

### 3c. 황화물 — 환원(Li 금속) · 우리 축 E

| 계 | 예측 산물 | 관측 | 원출처 |
|---|---|---|---|
| Li₃PS₄ · Li₇P₃S₁₁ | **Li₃P + Li₂S** | XPS·XRD 로 Li₂S·Li₃P·환원 P 종 검출 (Li₇P₃S₁₁/Li) | 예측 64,84,95 / 관측 109 |
| 개시 산물 | **Li₄P₂S₆** (P₂S₆⁴⁻) | Raman·XPS 로 β-Li₃PS₄/Au 계면 Li 석출 시 PS₄³⁻→P₂S₆⁴⁻ + Li₂S, **부분 가역** | 64 / 108(Sang) |
| LGPS | 위 + **Li₁₅Ge₄** | XPS 로 환원 Ge(Li–Ge 합금 또는 Ge) | 64,96 / 51 |
| Li₁₀SiP₂S₁₂ · Li₁₀Si₀.₃Sn₀.₇P₂S₁₂ | **Li₁₇Sn₄ · Li₂₁Si₅** (전자전도) | 임피던스 연속 증가 | 34 / 111 |
| AIMD | 결정질 Li–P–S·LGPS + Li 금속, **300 K·20 ps 안에** Li_xS·Li_yP·Li_zGe 배위수 변화로 분해가 보인다 | — | 90(Camacho-Forero & Balbuena 2018 JPS) |

### 3d. 아지로다이트 — **우리 조성** (전문 소절이 있다)

| 항목 | 내용 | 원출처 |
|---|---|---|
| 위치 | 지면 111–112, 「Argyrodites」 소절 **한 문단(21줄)** + `Fig. 5a` 의 `LPSCl` 행·열 | — |
| 창·반응성 | *"다른 황화물과 **유사한** 전기화학 창·양극 화학반응성·분해산물을 가질 것으로 예측"* — **아지로다이트 고유 수치는 본문에 하나도 없다** | 64(Richards 2016), 115(Deng/Ong 2017 Chem Mater) |
| **산화 분해산물 (예측↔관측 일치)** | **원소 황 · 리튬 폴리설파이드 · P₂S_x · LiCl** | 예측 64,66,115 / **관측 116,117**(Auvergniot 2017 SSI 300:78 XPS · Auvergniot 2017 Chem Mater 29:3883) |
| **Li 금속 대비 산물** | **Li₂S + Li₃P** (XPS 검출) | 118(Wenzel 2018 SSI 318:102) |
| NCM622 ↔ **Li₆PS₅Cl** | 사이클 시 **PO_x^y⁻ · SO_x^y⁻ 증가** (β-Li₃PS₄/NCM811 과 동일 패턴) | 119(Walther 2019 Chem Mater 31:3745, **XPS + ToF-SIMS**) |
| **할로겐의 역할** | 분해 시 **LiX 이원상 생성 → 계면 부동태화 기여 가능** (Cl-도핑 Na₃PS₄ 의 NaCl 선례 ref.113 에 빗대어) | 113(Wu 2018 ACS AMI) |
| 셀 성능 | LiNi₁ᐟ₃Co₁ᐟ₃Mn₁ᐟ₃O₂\|**Li₆PS₅Cl**\|Li–In **300 사이클 양호한 용량유지** | 117 |
| **O 도핑** | **Li₆PS₅Br 의 O 도핑이 Li 금속·산화물 양극 대비 안정성을 개선** | 64,65,66,**120**(Zhang 2019 JPS 410:162) |

### 3e. 산화물 — 대조군 (우리 계 아님, 맥락용)

| 계 | 값 | 종류 | ref |
|---|---|---|---|
| LLZO ↔ Li | 환원 구동력 **20 meV/atom** (거의 안정) · 산물 Zr, La₂O₃, Li₈ZrO₆, **Zr₃O**, Li₂O | DFT | 64,65,66 |
| LLZO / LLTaO / LLNbO | **topotactic Li 삽입전압 −0.95 / −1.03 / +0.07 V** ⇒ Zr·Ta 계는 반응 개시에 큰 활성화, Nb 계는 쉽게 환원 | DFT | 146 |
| LLZO / LLTaO / LLNbO | 환원한계 (Fig 4d 계열) **… / 0.85 / 1.05 V** ⇒ 환원 용이성 **Zr⁴⁺ < Ta⁵⁺ < Nb⁵⁺** | DFT | 145(Miara 2015 Chem Mater 27:4040) |
| LLZO 산화한계 | **2.9 V 또는 3.2 V** | DFT | 64,66 |
| LLZO ↔ Li 실측 | **~6 nm 두께 tetragonal LLZO 계면상** (in-situ STEM) · Al-LLZO 는 300–350 °C 용융 Li 에서 변색 · Fe³⁺ 도핑 시 **130 µm** tetragonal 층 | 실험 | 154 / 153 / 156 |
| LLZO ↔ 양극 (0 K) | LiCoO₂·NCM **1 meV/atom** · LiMn₂O₄ **63** · LiFePO₄ **94** | DFT | 65,67 |
| LLZTO ↔ 스피넬 (800 °C) | **최소 반응에너지 −60 ~ −30 meV/atom**; 산물 La₂O₃, La₂Zr₂O₇, NiO, Li₂MnO₃, LaMnO₃ (XRD 확인) | DFT+XRD | 80(Miara 2016 ACS AMI 8:26842) — `Fig. 4c` |
| LiPON | 산화: **N 이 2.6 V 위에서 N₂ 가스 + Li₃PO₄/Li₄P₂O₇** · 환원: **P 가 0.68 V 아래에서 Li₃P** · Li 금속 접촉 시 **Li₃P + Li₂O + Li₃N**(in-situ XPS 확인) | DFT / XPS | 64,65,66 / 73 |
| LLT (페로브스카이트) | 환원한계 **1.75 V**(예측) ↔ CV **1.8 V** / GITT **1.5 V**; 산화 **3.71 V**; LiCoO₂ 와 혼합 구동력 **0.5 meV/atom** vs LiNiO₂ **17 meV/atom** | DFT / 실험 | 65,66 / 179,180,181 |
| Li₃OCl | 산화 개시 **3 V** 또는 **2.55 V** → ClO₃·LiClO₃·LiClO₄·Li₂O₂·**LiCl** (전부 절연 ⇒ SEI 기대) · LiCoO₂ 혼합 구동력 **7 meV/atom** | DFT | 64 / 189 |
| LATP / LAGP | 환원 **<2.17 (or 2.7) / <2.7 (or 2.9) V**; **산화 4.21 (or 4.8) / 4.27 (or 4.5) V = 이 리뷰가 다룬 SE 중 최고** | DFT | 64,66 |
| LATP ↔ Li | Li 삽입으로 **130 % 팽창** → 균열; 임피던스 증가의 주범은 계면상 자체가 아니라 **연쇄적 화학-기계 열화** | 실험 | 200,201,202 |
| LATP ↔ LiCoO₂ | **~50 meV/atom** (Li₀.₅CoO₂ 로 탈리튬 + Li₃PO₄·Co₃O₄·LiAl₅O₈·TiO₂) | DFT | 65 |

### 3f. 자기모순으로 유명해진 CV 창들 (리뷰가 직접 기각한다)

| 주장 | 출처 ref | 리뷰의 판정 |
|---|---|---|
| LGPS **0–5 V** | 32 | *"defy basic chemistry"* |
| LLZO **0–9 V** | 26 | 동일 |
| Ba-도핑 Li₃OCl **0–8 V** | 192 | 동일 |
| Li₂(OH)₀.₉F₀.₁Cl · Li₂OHBr **>9 V** | 193 | 동일 |
| LAGP **6 V** | 203 | DFT 4.27–4.5 V 로 하향 |
| LiPON **0–5.5 V** | 9 | 부동태화로 설명 (내재 안정성 아님) |

---

## 4. 계산 방법 ★ — **이 리뷰의 진짜 기여는 "모델 4층의 위계"다**

> 계보 #1–#7 은 각자 하나의 기계를 썼다. **이 편은 그 기계들을 한 축 위에 줄 세우고, 각각이 무엇의 상한/하한인지를 명시한다.** 우리 원고에서 *"우리 onset 은 최악 시나리오다"* 라고 쓸 때 가리킬 활자가 여기 있다.

### 4a. 층 ① 전기화학 안정성 — grand-potential (우리 ESW 의 정의) · **식 (1)–(2) 인쇄됨**

- **식 (1)**: `μ_Li = μ⁰_Li − eV` — μ⁰_Li 는 **Li 금속의 Li 화학퍼텐셜**, e 는 기본전하. 과전압 무시 명시. 출처로 **ref.74 = Aydinol/Ceder 1997 PRB 56:1354** 를 단다.
- **식 (2)**: `Φ[c, μ_Li] = E[c] − n_Li[c]·μ_Li = E[c] − n_Li[c]·(μ⁰_Li + ... )` (인쇄 조판이 깨져 있으나 표준형 grand potential).
- **정의 문장 (★ 계보에서 우리가 찾던 그 문장)**: *"The grand potential convex hull at a given voltage is formed by the grand potentials of a set of phases and their linear combinations that minimize the grand potential at each composition **c − n_Li that excludes Li**. **The electrochemical stability window of a material corresponds to the range of voltages over which it is stable (exactly on the grand potential convex hull).**"*
  ⇒ **[Nolan21] 이 식 (5)(6) 으로 반쯤만 적어놓고 끝낸 것을, 이 편은 "창 = hull 위에 정확히 놓여 있는 전압 구간" 이라고 문장으로 완성한다** (§7c).
- **위상 명시**: *"the stability estimated from this grand potential convex hull method represents the **worst-case scenario (no kinetic stabilization)**"*. 핵절 과전압은 **전환전극 수준(수백 mV 이내)** 일 것이라고 ref.75,76 으로 괄호친다.
- 그림: `Fig. 2a` — Li–P–S 계의 Φ-hull 을 **V = 0 / 2.1 / 3 V** 세 점에서. β-Li₃PS₄ 가 2.1 V 에서만 hull 위(파랑)이고 0 V·3 V 에서는 hull 위로 떠 있다(빨강).

### 4b. 층 ② topotactic 안정성 — **최선 시나리오 (상한)**

- **식 (3)**: `V_topo,ext = (E[c − Na] + μ⁰_Na − E[c]) / e` — 가장 불안정한 알칼리 원자 **1개**를 구조를 유지한 채 빼낸 완화 슈퍼셀의 엔탈피 차. 인터칼레이션 전극 전압 계산과 형식이 같다(ref.74,77).
- 논리: 새 상의 핵생성도, 알칼리 외 원소 확산도 필요 없으므로 **동역학으로 막을 수 없는 분해**다 ⇒ 여기서 나오는 창이 **가장 넓은 창 = 최선 시나리오**.
- 예: **Na₃PSe₄ V_topo,ext = 2.75 V** (`Fig. 2b`).
- ⚠ **우리는 이 층을 갖고 있지 않다.** 우리 `tools/oxidation/` 은 ① 층만 한다 (§8-③).

### 4c. 층 ③ 화학혼합 반응성 — pseudo-binary · **식 (4) 인쇄됨**

- **식 (4)**: `ΔE[c_a, c_b] = E_pd[x·c_a + (1−x)·c_b] − x·E[c_a] − (1−x)·E[c_b]`, **x 에 대해 최소화**. `E_pd` 는 그 조성에서 **반응산물의 최저에너지 조합**.
- **우리 `interface_reactivity` 와 문자 그대로 같은 식이다** (Richards 2016 = ref.64 형식화 → pymatgen `InterfacialReactivity`). 본문도 *"the ability to find the minimum is now an **explicit feature in the Materials Project**"* 라고 적는다 — 즉 **도구까지 같은 것을 가리킨다**.
- **확장 2종을 명시**: ⓐ **알칼리 개방계**(전압 인가 하 화학반응성) ⓑ **산소 개방계**(고온 소결 조건). `Fig. 2c` 가 이 둘을 "Li 저장조 at μ_Li / O₂ 저장조 at μ_O" 로 그린다. ⇒ **우리 `interface_reactivity_v2.py`(GrandPotentialInterfacialReactivity)가 ⓐ 이고, ⓑ 는 우리가 안 하고 있다.**
- 위상: *"capturing the **maximal chemical driving force** that can exist at an interface"* — **최대 구동력**이지 실제 경로가 아니다.

### 4d. 층 ④ explicit 계면 계산 — 국소 재배열 (구조완화 / AIMD)

- **구조완화**: Li₃PS₄/Li(84) · LLZO/Li 및 Li₂CO₃/Li(62,85) · **LiCoO₂/Li₃PS₄ 와 LiNbO₃/Li₃PS₄(86 = Haruyama, Tateyama)** · LiCrS₂·LiMnS₂/Li₃PS₄(87 = Xu, Bo, Zhu) · LiPON/Li(88). `Fig. 2d` 가 LLZO(001)/Li(001) 최저에너지 계면.
- **한계 2가지를 저자가 직접 적는다**: ⓐ **시작 배치에 민감하다** ⓑ **원자확산·핵생성 같은 활성화 과정을 못 담는다** (국소 좌표 최적화일 뿐).
- **AIMD**: LiFePO₄(FePO₄)/Li₃PS₄(89) · Li₇P₃S₁₁/Li, LGPS/Li, β-Li₃PS₄/Li(90) · NaCoO₂/Na₃PS₄(91). *"high computational cost … typically only captures … elevated temperatures and **very small time scales (<1 ns)**. Hence, **it should always be combined with a thermodynamic assessment**."*
- **위상**: 계면에너지는 반응에너지에 비해 작으므로 벌크 반응에너지로 다루는 것이 정당하다 — 는 앞 세 층의 전제를 여기서 명시적으로 정당화한다.

### 4e. 층들의 관계 — 한 줄

```
   ① grand-potential ESW  →  가장 좁은 창 (worst case, 동역학 안정화 0)
   ② topotactic           →  가장 넓은 창 (best case, 동역학 안정화 최대)
   ③ pseudo-binary 혼합    →  최대 화학 구동력 (경로 아님) · 개방계로 전압/산소 확장
   ④ explicit 슈퍼셀/AIMD  →  국소 재배열·결합교환은 보이나 시간·크기 스케일이 갇힘
```
**실험값은 ①과 ② 사이에 떨어져야 한다** — 이것이 이 리뷰가 실험과 계산을 맞물리는 기본 문법이다.

### 4f. ⛔ 이 리뷰가 **안 하는 것**

- 자체 DFT 계산 0건 → **cutoff·k-mesh·PAW·U·supercell·SQS/무질서 처리 정보가 하나도 없다.** (우리 방법표에 옮길 수 있는 항목 0)
- 비정질/유리상을 다루는 열역학이 없다 (본문이 미래과제로 명시).
- 핵생성 속도·확산 속도·계면상 두께 성장 모델 없음.
- **무질서 처리**: 아지로다이트의 S/Cl 자리무질서는 **언급조차 없다**.

---

## 5. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 양극 복합체의 계면 목록 모식도. 무코팅 6종(SE/양극·양극/탄소·집전체/양극·집전체/탄소·집전체/SE·SE/탄소) + 코팅 시 추가 6종(SE/코팅·코팅/양극·코팅/탄소·집전체/코팅·**불완전 코팅 시** SE/양극·양극/탄소) = **12종** | 우리 계면 캠페인이 **SE/양극만 보고 있다**는 사실을 그림 하나로 드러낸다. 특히 **SE/탄소·SE/집전체는 Li 수송 경로가 아니어서 단기 성능엔 안 보이지만 σ 를 갉아먹는다** — 우리 `cascade_interface_carbon.jsonl` 이 정확히 그 자리다 |
| 2a | Li–P–S grand-potential hull @ 0 / 2.1 / 3 V. 0 V hull = **Li₂S–Li₃P 직선**(β-Li₃PS₄ 는 그 위 준안정), 2.1 V = Li₃PS₄ 가 최저점 + Li₄P₂S₆ 가 P 쪽 tie-line, 3 V = **P₂S₅·P₄S₇·P₄S₃** 이 hull 이고 Li₃PS₄ 준안정 | **우리 `esw_lpscl_hull.json` 계단의 교과서 그림.** 0 V 산물이 Li₂S+Li₃P 로 우리 계단(0 V: Li₃P+5Li₂S+LiCl)과 화학이 같다. 발표 슬라이드의 "hull 이 전압에 따라 갈아엎힌다" 도해로 그대로 쓸 수 있다 |
| 2b | Na₃PSe₄ topotactic 추출, **V_topo,ext = 2.75 V**. Na 한 자리를 비우고(빨간 점선 원) 그 원자를 저장조로 보냄 | **우리에게 없는 층 ②의 최소 구현 예제.** comp1 에 그대로 이식 가능 (§8-③) |
| 2c | 화학혼합 모식: A\|B 사이 **혼합층 조성 `x·c_a+(1−x)·c_b`**, 위에 **Li 저장조 at μ_Li** 와 **O₂ 저장조 at μ_O** | 우리 `interface_reactivity`(닫힌계) ↔ `interface_reactivity_v2`(Li-개방) 의 차이를 한 장으로 설명. **O-개방(소결) 축은 우리가 아직 안 연 칸** |
| 2d | LLZO(001)/Li(001) explicit 계면 (ref.85) | 우리 slab/계면 계산의 "층 ④" 위치를 보여주는 참조 이미지 |
| 3a | **성분분해 EIS**: Li-In\|β-Li₃PS₄\|NCM811 셀의 R_SE,bulk / R_SE,gb / R_SE,cathode / R_SE,anode 를 OCV 함수로. figure-read — bulk ≈ 450–490 Ω 평탄, gb ≈ 100 Ω 평탄, **cathode 는 1차 충전에서 ~100 → ~250 Ω 로 비가역 상승(가장 급한 구간 3.2–3.4 V)**, anode 는 방전 말 ~600(1차)/~780 Ω(2차) 로 큰 오차막대와 함께 급등. **x축은 vs Li⁺/Li-In** | 🔑 **"계면저항이 어디서 오르는지"를 성분으로 가른 유일한 실측 그림.** ⚠ **기준전극이 Li-In** 이라 우리 vs Li/Li⁺ 값과 직접 못 붙인다 (+0.6 V 대 오프셋). Zuo 2023 에서 이미 겪은 함정과 같은 것 |
| 3b | **CV, Li\|LGPS\|LGPS+C\|Pt, 1.0–3.5 V**. figure-read — 산화 전류가 **≈2.1–2.2 V** 에서 0 을 떠나 **≈2.75 V 에서 +0.58 mA 피크**, 3.5 V 에서 ~0.2 mA 로 감쇠; 환원쪽은 1.5–1.6 V 부근 −0.34 mA 어깨 후 1.0 V 에서 −0.38 mA | 🔑🔑 **"CV 가 황화물 창을 넓게 읽는 이유 = 반응면적"의 결정적 증거.** 탄소를 섞자 예측 2.1 V 가 그대로 보인다. **우리 2.256 V 를 실험과 붙일 때 인용할 바로 그 그림** — 단 이건 LGPS 다 |
| 3c | **S 2p XPS**, Li₃PS₄ glass+C, before/charge/discharge, 158–166 eV. figure-read — **충전 시 S–S(빨강) 성분이 비-가교 S(파랑)를 압도**(≈162.7 eV 주피크 + ≈163.8 eV 부피크), **방전에서 되돌아온다** | 🔑 **우리 산화 onset 산물 `S`(원소 황/폴리설파이드)의 실험 대응물.** "S²⁻ → S–S 가교" 가 부분가역이라는 점까지 |
| 3d | **HAADF-STEM + EDS 라인프로파일**, LiCoO₂/Li₂S–P₂S₅ 1차 충전 후. figure-read — 계면상 띠가 ~40–50 nm 위치, Co 는 ~98 at% 에서 37–45 nm 구간에 급락하나 **90 nm 까지 5–20 at% 로 꼬리**, S 는 65–70 at%, P 는 30–40 at% 로 상승 | 🔑 **"Co 가 황화물 쪽으로 50 nm 넘게 들어간다" 의 원본 이미지.** 우리 interface_reactivity 산물의 `Co₉S₈`·`CoS₂` 가 왜 나오는지의 실험 근거 |
| 4a | LLZTO+AB / LLZTO+VGCF 복합 WE 의 CV, 2–5 V. figure-read — 인셋(3.5–4.0 V, 0–2 µA)에서 전류가 **≈3.7–3.8 V** 부터 상승, 본 피크 **≈3.5 µA @ ~4.05 V**(AB) / **≈3.8 µA @ ~4.2 V**(VGCF) | **가넷도 "탄소를 섞으면 4 V 부근에서 보인다"** — 3b 와 같은 처방이 산화물에도 통한다는 대조군 |
| 4b | Zr 3d XPS, fresh vs 0 V 방전. 방전본에 **178.2 eV Zr₃O** 성분 추가 | 예측 산물(Zr₃O, ref.66)이 XPS 로 잡힌 사례 — "예측 산물 검증" 의 교과서 예 |
| 4c | **유사이원 반응에너지 vs LLZTO 분율 x** (800 °C), LLZTO/LCMO·LNMO·LFMO. figure-read — 최소가 **x ≈ 0.52–0.58**, 값 **≈ −0.038 / −0.045 / −0.054 eV/atom**(빨간 별) | 🔑🔑 **우리 `all_kinks` 곡선의 그림판.** 우리 comp1\|LiCoO₂ 최소가 x=0.5302 에서 −0.3227 eV/atom — **x 위치는 거의 같고 깊이가 6–8배**다. "황화물 계면이 가넷보다 한 자릿수 반응적" 을 한 그림으로 |
| 4d | **전압 의존 화학혼합 반응에너지** (LLTaO 실선 / LLZO 점선 × LCO·LMO·LFPO), 0–5 V, 하단에 내재 안정구간 막대. figure-read(좌표 캘리브레이션) — **LLZO 0.43–3.41 V · LLTaO 0.88–3.57 V · LCO 1.89–≥5 · LMO 1.44–≥5 · LFPO 2.21–≥5 V** | 🔑 **개방계(전압) pseudo-binary 를 "곡선"으로 그린 유일한 그림** = 우리 `interface_reactivity_v2` 출력의 목표 형태. ⚠ **LLZO 창이 `Fig. 6` 과 어긋난다** (§10-4) |
| 5a | **반응에너지 히트맵** (ref.67 재수록). 행 = 비폴리음이온 산화물 3 + 폴리음이온 산화물 6 + SE 4, 열 = 만충 양극 4(NCM·LCO·LMO·LFPO) + SE 4(**LPSCl**·LGPS·LPS·LLZO). 색 0 → −600 meV/atom | 🔑🔑🔑 **우리 계가 이름으로 찍힌 유일한 정량 그림.** `LPSCl` 행 × `LCO` 열이 **우리 `interface_reactivity` 와 완전히 같은 계·같은 양**이다. §12a 에서 픽셀 정량화해 Xiao 2019 Table S2 와 대조했다 |
| 5b | 산화물·황화물·폴리음이온 3분할 원. 산화물↔황화물만 빨강(*"Anion exchange · Li₃PO₄ formation"*), 폴리음이온은 양쪽과 초록(*"same anion / similar cation + strong hybridization"*) | **"왜 인산염 코팅인가" 한 장 요약.** 우리 O-치환·B₂O₃ 서사의 문법을 그대로 빌려온다 |
| 6 | **전 SE ESW 지도**: x = 환원한계(역방향 5→0), y = 산화한계 0→5, 원 면적 ∝ σ 자릿수(µS/cm), 점선 = 창 폭 등고선 | 🔑🔑 **발표용 "우리가 어디 서 있나" 배경지도.** §12b 에서 9개 계열 전 점을 좌표로 복원했다 |
| 7 | 조성 튜닝 5레버의 **σ/환원/산화 3분할 파이**. ① 분극성 X(Se>S>O): σ↑·환원 불명·**산화↓** ② X=N: σ 불명·환원↑·**산화↓** ③ 높은 Li 함량: σ↑·환원↑·**산화↓** ④ M 없음(Li₃OCl·Li₃N): σ 불명·환원↑·**산화↓** ⑤ **공유결합 M–X 혼성(P–O·B–O): σ↑·환원↑·산화↑ — 셋 다 초록** | 🔑🔑🔑 **우리 O-치환/B₂O₃ 축의 문헌 근거가 이 파이 하나다.** 다섯 중 **넷은 산화를 희생**하고 **혼성만 희생이 없다.** 우리가 "O 를 넣는다"고 할 때 서 있는 자리가 ⑤ |
| Table 1 | 음이온 X(O·S·Cl·Br·N) × 양이온 M 을 **Li 금속 대비 stable / SEI former / MCI former** 로 분류 (Li–M–X 상도 기반, ref.224,233 + MP) | 🔑 **도판트 선정표.** Cl 행: K⁺·Rb⁺·Cs⁺·Sr²⁺·Ba²⁺·Yb²⁺ 안정. O·S 행: **란타나이드 계열이 안정** ⇒ **우리 Nd 도핑의 문헌 자리**. S 행 P⁵⁺ 는 **SEI former**(실험 확인 표시) |

---

## 6. Post-processing ★ — 이 리뷰가 계산과 실험을 **무엇으로** 맞물리는가

자체 후처리는 없다. 대신 **"계산 산물 ↔ 실험 기법" 의 짝짓기 규칙**이 사실상 이 리뷰의 방법론이고, 그게 우리에게 쓸모 있다.

| 계산이 내놓는 것 | 짝지어진 실험 기법 | 리뷰 안의 성공 사례 |
|---|---|---|
| **전압 한계(ESW onset)** | **고감도 CV + 탄소 혼합 복합 WE** (반응면적 확대) | LGPS 2.1 V 산화·1.7 V 환원이 예측과 일치(ref.97,98) |
| 〃 | **operando XPS** | Li₂S–P₂S₅ 산화 2.7 V (ref.99) |
| 〃 | 저속 정전류 충방전 (액체셀) | Na₃PS₄ 0.9–2.5 V, Na₃PSe₄ 1.25–2.35 V (ref.50) |
| **분해산물(고체상)** | **XPS**(결합상태) · **Raman**(음이온 단위) · **XRD/싱크로트론 XRD**(결정상) | PS₄³⁻→P₂S₆⁴⁻+Li₂S (ref.108) · MnS·CoNi₂S₄·Li₃PO₄ (ref.107) |
| **원소 상호확산** | **STEM-EDS 라인프로파일** · **ToF-SIMS** | Co 50 nm (ref.47) · PO_x/SO_x (ref.78,119) |
| **계면상 두께·상** | **in-situ STEM** | LLZO/Li 의 6 nm tetragonal 층 (ref.154) |
| **계면상이 저항을 올리는가** | **성분분해 EIS**(등가회로 피팅) + OCV 스캔 | `Fig. 3a` (ref.60) |
| **가스 생성** | 셀 팽창·가스 검출 | LiPON 5.8 V N₂ (ref.9) |

**리뷰가 명시하는 3대 처방** (우리 실험 협업자에게 그대로 전달 가능):
1. **반응면적을 키워라** — SE+탄소 복합 WE 를 쓰면 산화/환원 전류가 **수 자릿수** 커진다(ref.97,103,144). 계산: 평면전극에 10 nm 층이 1 V 구간·0.1 mV/s 로 생기면 CV 전류는 **~0.3 µA/cm²** 밖에 안 된다 — 보통 조건에선 안 보인다.
2. **cutoff 전류로 한계를 정하지 마라** — 셋업 의존이 너무 크다(ref.238). 대신 **전류가 급격히 꺾이는 전위**를 쓰고, **산화산물의 환원 피크**를 같이 본다.
3. **Li 를 대극/기준극으로 쓰지 마라** — SE 와 반응한다. **In 또는 Au 대극 + In 또는 Ag₃SI/Ag 기준극의 3전극**을 쓴다(ref.101,238,241). 그리고 CV 는 **반드시 TEM·XPS 로 보강**한다.

---

## 7. 우리 DFT 대비 (comp1 / modelc) → `our_dft_baseline.md`

### 7a. 양(quantity) 대조표 — **무엇이 같은 양인가**

| 우리 양 | 이 리뷰의 대응 | 같은 양인가 | 비고 |
|---|---|---|---|
| **산화 onset 2.256 V** (`constrained_esw_cl_scan.json`, LiS₄ 제외) | **층 ① grand-potential ESW 상한** (식 1–2, *"hull 위에 정확히 놓인 전압 구간"*) | ✅ **같은 양·같은 기준(vs Li 금속)·같은 정의** | ⛔ 값은 비교 금지 — 리뷰가 인용한 값은 2015–2016 hull 세대(황화물 1.5–2.5 V, Li₃PS₄ 환원 1.69 V). 우리는 MP2026 |
| **환원한계 1.242 V / OCV 1.717 V** | 동일 층 ①의 하한 | ✅ 같은 양 | 본문 인쇄 **Li₃PS₄ 1.69 V** 가 우리 **1.717 V**(OCV) 와 **0.03 V 차** — [Zhu15] SI 1.71 V 와도 같은 자리 |
| **`interface_reactivity` −0.3227 eV/atom** (comp1\|LiCoO₂, pymatgen `InterfacialReactivity(use_hull_energy=True)`) | **층 ③ 식 (4)**, 그리고 `Fig. 5a` 의 **LPSCl × LCO 칸** | ✅✅ **같은 양 + 같은 계 + 같은 도구** (리뷰가 MP 의 기능이라고 직접 지목) | **계보 8편 중 우리 값과 *완전히 같은 쌍*을 그림으로 인쇄한 첫 편.** 정본 수치는 ref.67 Table S2 = **−339 meV/atom** (§12a) |
| **`interface_reactivity_v2`(전압 분해)** | 층 ③의 **알칼리 개방계 확장** + `Fig. 4d` 곡선 | ✅ 같은 양 | 우리는 곡선을 그려본 적이 없다 — `Fig. 4d` 가 목표 형태 |
| (우리에게 **없음**) | **층 ② topotactic 식 (3)** | ❌ 우리 공백 | §8-③ |
| (우리에게 **없음**) | 층 ③의 **O-개방계**(소결 조건) | ❌ 우리 공백 | 황화물은 소결을 안 하므로 우선순위 낮음 |
| `sei_products.json` 밴드갭 (MP) | 리뷰의 **"SEI former vs MCI former"** 이분법 (Table 1) | 🟡 **같은 물음, 다른 대리변수** | 우리는 **MP 밴드갭 문턱**(≥4 절연 / 2–4 경계 / <2 누설), 리뷰는 **Li-안정 상의 존재 여부 + 전자전도성 정성판단**. 섞지 말고 **두 축을 병기** |

### 7b. ★ 우리 `sei_products.json` · `interface_reactivity` 산물 ↔ 이 리뷰의 산물 대조

> 요청받은 대조다. 좌열은 **우리 원장**(`db/properties/sei_products.json`, `interface_reactivity_results.json`), 우열은 **이 리뷰가 인용한 예측·관측**. ⛔ 값은 섞지 않는다 — **상(phase)의 일치/불일치만** 본다.

| 산물 | 우리 원장에서의 자리 | 이 리뷰에서 | 판정 |
|---|---|---|---|
| **LiCl** | `sei_products` gap 6.65 eV, role **insulator**, side anode+cathode / `interface_reactivity` comp1\|LCO 전 kink 에 등장 | **아지로다이트 산화 산물로 명시**(ref.64,66,115 예측 ↔ **ref.116,117 XPS 관측**) + *"LiX 이원상이 계면 부동태화를 도울 수 있다"* + Li₃OCl 산화산물로도 LiCl | ✅✅ **예측·관측 양쪽에서 일치.** 게다가 리뷰는 **역할까지 우리와 같게 본다**(전자 절연 → 부동태) |
| **Li₃PO₄** | gap 5.73 eV, insulator, "bulk-GB+cathode" / comp1\|LCO 최심 반응의 주산물 | **황화물↔산화물 양극의 대표 산물**, *"formation of Li₃PO₄ is highly favourable because of its deep formation energy (**−2.767 eV/atom**)"* + **300 °C 이상 NMC111/75Li₂S–25P₂S₅ 에서 싱크로트론 XRD·TEM 실측**(ref.107) + LATP\|LCO 에서도 | ✅✅ **완전 일치 + 관측 근거 확보.** 리뷰가 **왜** 나오는지(생성엔탈피가 깊어서)를 숫자로 준다 |
| **Li₂S** | gap 3.90 eV, role **marginal**(반절연), anode+cathode | Li₃PS₄·Li₇P₃S₁₁ 의 **Li 금속 환원 산물**(예측 ref.64,84,95 ↔ **관측 ref.108,109,118**) · 아지로다이트/Li 에서도 XPS 검출 | ✅ 일치. ⚠ 우리는 "marginal", 리뷰는 Li-안정 이원상 = **SEI 후보**로 본다 — **더 낙관적** |
| **Li₃P** | gap 0.70 eV, role **conductor-LEAK** (무도핑 음극 누설 산물) | 동일하게 Li 금속 환원 산물. ⚠ **리뷰는 Li₃P 를 "부동태 산물" 쪽으로 쓴다** — Li₃PO₄/Li 계면에서 *"Li₃P 와 Li₂O … **These reaction products are passivating**"*(ref.222 XPS 확인), LiPON/Li 에서도 *"block electron conduction but … permit Li-ion diffusion"* | 🔴 **충돌한다.** 우리는 Li₃P 를 **전자 누설 경로**로 판정했고(gap 0.70 eV), 리뷰는 **부동태 산물**로 쓴다. §10-5 에 남긴다 |
| **Li₂O** | gap 5.24 eV, insulator, anode (O 도입으로 Li₃P 를 대체) | LiPON/Li 산물 Li₃P+Li₂O+Li₃N · Li₃PO₄/Li 산물 Li₃P+Li₂O · LLZO 환원산물 · **우리와 같은 논리**(전자 차단 + Li 전도) | ✅ 일치 **+ 우리 "O 가 Li₃P 를 Li₂O 로 바꾼다" 서사의 문헌 선례가 LiPON 이다** |
| **Li₂SO₄** | (우리 comp1\|LCO 반응의 주산물, sei_products 에는 미등재) | *"formation of **PO₄³⁻ and SO₄²⁻ polyanions**"*(ref.64,65,95,105) + **ToF-SIMS 로 SO_x^y⁻ 관측**(ref.78,119) | ✅ 일치 — **SO₄²⁻ 는 관측된다** |
| **Co₉S₈ / CoS₂ / Co₃S₄** | comp1\|LCO kink 전 구간 | *"transition-metal sulfides (such as **Co₉S₈**(ref.65), Mn₂S₃, Ni₃S₄, CoNi₂S₄)"* + **MnS·CoNi₂S₄ XRD 관측**(ref.107) + `Fig. 3d` Co 50 nm 확산 | ✅✅ **상 이름까지 일치**(Co₉S₈ 는 ref.65 에서 그대로) |
| **원소 S / 폴리설파이드** | 우리 산화 onset 반응 `Li₆PS₅Cl → Li₃PS₄ + LiCl + S + 2Li⁺ + 2e⁻` 의 S | **아지로다이트 산화산물로 명시**(원소 황·폴리설파이드·P₂S_x·LiCl) + `Fig. 3c` S–S XPS + 5 V 충전 후 원소황 관측(ref.103) | ✅✅ **우리 onset 반응식의 S 가 실험에서 보인다** |
| Nd 계 산물 (NdPO₄·NdOCl·NdCl₃·Nd₂O₃·LiNdO₂·Nd₂S₃·NdS) | `sei_products` 전용 | **없다** — Nd 는 이 리뷰에 안 나온다. 다만 **Table 1 이 "란타나이드 계열 = O·S 화학에서 Li 금속 대비 안정"** 이라고 분류 | 🟡 **직접 대조 불가 / 간접 지지.** Table 1 이 우리 Nd 선택의 **계열 수준 근거**는 된다 (⚠ Nd 개별 검증 아님) |
| Li₃PS₄ (중간체) | 우리 onset 산물 | `Fig. 2a` 의 2.1 V hull 정점 + Cronk 2026 의 "LPS-like" 계면상 | ✅ 일치 |

⇒ **한 줄**: 우리 `interface_reactivity` 산물 5종(**Li₃PO₄·Li₂SO₄·Li₂S·LiCl·Co₉S₈**)은 **전부 이 리뷰 안에 예측으로 있고, 그중 Li₃PO₄·SO₄²⁻·Co₉S₈계·LiCl 은 실험 관측까지 붙어 있다.** 이것이 계보 #1–#7 을 통틀어 우리 산물 목록이 **실험 증거와 연결되는 첫 지점**이다.

### 7c. ★ 계보 물음 — **전압축 정의가 여기서 문장으로 완성된다**

계보 카드가 #4·#5 에 물었던 것: *"anodic limit ≡ E_D^open 이 0 을 벗어나는 φ 라는 문장이 어디 있나."*

- **[Nolan19]**: 정의 없음, 값도 없음(boxplot figure-read 뿐).
- **[Nolan21]**: 식 (5)(6) 은 인쇄됐으나 *"limit ≡ …"* **문장은 없고** φ 는 3 V·5 V 두 점뿐.
- **[Nolan18] = #7** (같은 날 나온 형제 digest `nolan2018_computation_accelerated_design_review` §4c 에 따르면): ✅ **문장이 있다** (p. 2022, §2.2.2) + **Equation 4 로 `μ_Li(φ) = μ⁰_Li − eφ`**. ⛔ 그러나 그 digest 의 판정대로 **`E_d`·`E_D^open`·`ΔH_D`·`E_hull` 에는 번호 붙은 식이 없다 — 전부 산문·캡션**이다.
- **[Xiao20] = 이 편**: ✅ **문장이 있다** — *"The electrochemical stability window of a material corresponds to the range of voltages over which it is stable (exactly on the grand potential convex hull)."* + **번호 붙은 식 (1) `μ_Li = μ⁰_Li − eV` · (2) Φ · (3) V_topo,ext · (4) pseudo-binary ΔE** + **"Li 를 제외한 조성 c − n_Li 에서 최소화"** 라는 구성 규칙 + **worst/best-case 위상 선언**까지.

⇒ **판정 (정정 포함)**: 우리 2.256 V 의 **직계 원전은 여전히 [Zhu15] → Mo/Ong/Ceder 2012** 다 (이 리뷰도 그 값들을 ref.64,65,66 으로 인용할 뿐 자기 값을 만들지 않는다). 그리고 ⚠ **"정의 문장이 있는 유일한 편" 은 아니다 — #7 이 2년 먼저 갖고 있다.** 두 편의 차이는 이렇다:

| | **#7 [Nolan18]** (Mo 그룹) | **#8 [Xiao20]** (Ceder 그룹) |
|---|---|---|
| limit 이 무엇인지 한 문장 | ✅ p. 2022 | ✅ 「Electrochemical stability」 절 |
| `μ_Li = μ⁰_Li − eV` | ✅ Equation 4 | ✅ **식 (1)** |
| 반응에너지 식에 **번호** | ❌ 산문·캡션뿐 | ✅ **식 (4)** (+ topotactic 식 (3)) |
| **worst/best-case 위상 선언** | (해당 서술 없음 — #7 digest 기준) | ✅ 명시 |

⇒ **원고 Methods 에서 정의를 인용한다면 두 편을 같이 단다.** 우리가 하는 것이 *"동역학 안정화 0 인 하한"* 임을 못박으려면 **#8 의 worst-case 문장**이 필요하고, 시간 우선권과 Mo 계보 연결을 보이려면 **#7** 이 필요하다.

### 7d. ★ 계산이 예측한 산물이 실험에서 보이는가 — **이 리뷰의 답 (의뢰 질문 ①)**

리뷰가 자기 결론절에서 직접 채점한다. 정리하면 **세 등급**이다.

| 등급 | 무엇이 맞았나 | 사례 |
|---|---|---|
| 🟢 **정량까지 맞았다** | **전압 한계** — 단, *실험이 제대로 측정됐을 때만*. 초기 CV 의 넓은 창은 **측정의 문제**였고, 고감도·복합 WE 로 다시 재면 DFT 값으로 수렴했다 | LGPS 2.1 / 1.7 V ↔ 예측 1.7–2.3 V · Na₃PS₄·Na₃PSe₄ · LLT 1.75 V ↔ CV 1.8 V |
| 🟢 **상(phase) 수준에서 맞았다** | **분해산물의 이름** | Li₂S·Li₃P(황화물/Li) · P₂S₆⁴⁻ · **LiCl·S·폴리설파이드(아지로다이트)** · MnS·CoNi₂S₄·Li₃PO₄(300 °C) · Zr₃O(LLZO) · Li₃P/Li₂O/Li₃N(LiPON) · Li–Ge 합금(LAGP) · La₂O₃·La₂Zr₂O₇·NiO·Li₂MnO₃·LaMnO₃(LLZTO 소결) |
| 🟡 **정성만 맞았다 / 어긋난다** | **"예측 상이 안 보이는 경우"** 가 남는다 — P₂S₅ 는 XPS 로 직접 관측된 적 없다(대신 S–S 가 보인다). LAGP/Li 에서 **Al³⁺ 는 DFT 예측과 달리 3가를 유지**한다(ref.66,198). LLZO/양극은 **연구마다 산물이 다르다**(La₂CoO₄ / La₂Li₀.₅Co₀.₅O₄ / La₂Zr₂O₇ / tetragonal LLZO) | 본문이 직접 나열 |
| 🔴 **원리적으로 못 맞추는 것** | **비정질 vs 결정질 여부 · 핵생성 속도 · 원소확산 속도 · 계면상 성장 두께 · 실험 시간스케일** | 「Future perspectives」 에 명시 |

> 리뷰의 자기 평가 문장(그대로): *"Even when the predicted interphases are not observed in experiments, the computational results often capture the **qualitative features** of the interfacial reactions, such as the **redox centre** driving the electrochemical decomposition, the **preferred bond formation** upon chemical mixing and the formation of a stable interface, an MCI or an SEI."*

### 7e. ⛔ 우리 db 절대값과 섞으면 안 되는 것

1. **`Fig. 3a` 의 저항값과 전압** — 기준이 **Li⁺/Li-In** 이다. 우리 vs Li/Li⁺ 와 같은 축에 놓지 않는다.
2. **황화물 창 1.5–2.5 V** — 2015–2016 hull 세대. 우리 2.256 V 와 **정의는 같고 세대가 다르다**. 같은 표에 놓을 때 세대를 반드시 병기.
3. **`Fig. 5a` 픽셀 판독값** — §12a 의 −308 은 **figure-read** 다. 인용은 **Xiao 2019 Table S2 의 −339** 로 하고, 우리 −322.7 과의 비교도 그쪽으로 한다.
4. **Li₃PS₄ 환원 1.69 V** 와 우리 `reduction_limit_V` **1.242 V** 를 같은 양으로 놓지 않는다 — 우리 1.717 V(OCV, 자기분해)가 그 자리다 ([Honrao21] 에서 이미 확정된 판정).
5. **아지로다이트 고유 수치는 이 리뷰에 없다.** *"다른 황화물과 유사할 것"* 이라는 문장뿐이다 — **"리뷰가 Li₆PS₅Cl 의 창을 X V 로 준다"고 쓰면 거짓이다.**

### 7f. ★ Meng 그룹 계보 재정립 — Cronk 2026 두 편과 이 편의 **진짜** 관계

계보 카드의 *"Cronk 2026(같은 Meng 그룹)과 이어진다"* 는 저자 오인에서 나온 문장이라 **무효**다(§0a). 그러나 **연결 자체는 있다 — 그룹이 아니라 전제(premise) 수준에서**. 우리 `cronk2026_*` 두 digest 를 다시 읽고 맞춰보면 이 리뷰가 **6년 앞서 깔아둔 전제가 셋**이다.

| Cronk 2026 이 (설명 없이) 전제로 쓰는 것 | 이 리뷰가 미리 깐 자리 |
|---|---|
| ① *"LPSCl 분해산물이 **redox-active** 하고, 그래서 2사이클부터 충전 2.5–2.7 V 숄더가 생긴다 (= SSE redox)"* | 「Oxidation products of sulfides」 절 전체. *"the decomposition of several sulfide SEs may be **partially reversible** or the decomposition products are **redox-active**"* — ref.102(Hakari, S–S 결합 가역) + **ref.103(Swamy/Chiang: β-Li₃PS₄ 5 V 분해는 비가역이나 이후 사이클은 가역, 그 산화환원은 **원소 S 와 P 의 중첩**)**. ⚠ 그리고 리뷰는 곧바로 못을 박는다 — *"**it is unlikely that these processes contribute to the long-term cycling capacity of a battery**"* |
| ② *"양극 복합체 안에서 탄소(AB)가 20 wt% 나 들어가는데 그게 SE 를 분해시킨다"* 를 Cronk 는 **다루지 않는다** | 「Narrow stability windows of sulfides」 절이 **정확히 그 경고**다: *"decomposition of the SE will occur **wherever the SE contacts the electron path** (current collector, conductive additive) … this degradation **may not be immediately visible in the short-term performance** … will ultimately impair the Li-ion conductivity"*(ref.69,70) |
| ③ *"Li₂S 양극이 LPSCl 을 LPS-like 로 환원시킨다"* (합성 중 분해) | 「Reduction stability」 + `Fig. 2a` 의 **0 V hull = Li₂S–Li₃P 직선**. Li₂S 가 풍부한 환경은 Li 화학퍼텐셜이 높은 쪽이고, 거기서 아지로다이트는 hull 위가 아니다 — Cronk 의 XRD 소멸·Raman 425→418 cm⁻¹ 이 그 계단의 실물 |

⇒ **이 리뷰가 Cronk 2026 에 던지는 질문 하나(우리가 물어야 할 것)**: Cronk 는 *"SSE redox 가 용량에 기여한다"* 를 긍정적으로 쓰는데, **이 리뷰는 같은 현상을 "전환반응이라 장기 사이클에 기여할 수 없다"** 고 판정했다. 두 문헌이 **같은 사실을 반대 부호로 읽는다.** 우리 원고에서 SSE-redox 숄더를 언급할 때 이 긴장을 지워서는 안 된다.

---

## 8. 적용 인사이트 — 우리 연구에 어떻게 (추가 계산 0~1건)

1. **원고 Methods 의 ESW 정의를 #7 + #8 두 편으로 고정한다** (추가 계산 0). #3·#4·#5 는 정의를 인용 승계로 넘기고, **#7 이 문장을 주고(p. 2022), #8 이 문장 + 번호 붙은 식 (1)–(4) + worst/best-case 위상을 준다** (§7c 표). 우리가 쓰는 것이 *"동역학 안정화가 0 일 때의 하한"* 이라는 단서는 **#8 에서만** 인용할 수 있다.
2. **우리 산화 onset 을 "worst-case bracket 의 아래쪽" 으로 말한다** (추가 계산 0). 이 리뷰가 명시적으로 층 ①=최악/층 ②=최선이라고 위계를 세워줬다. 지금까지 우리는 2.256 V 를 "그냥 onset" 이라 불러왔는데, **"동역학 안정화가 전혀 없을 때의 하한"** 이라고 쓰면 Zuo 2023 CV 창(2.5–2.7 V)·Cronk dQ/dV(2.70 V) 와의 0.3–0.5 V 차이를 **모순이 아니라 설계된 여유**로 설명할 수 있다.
3. **★ 층 ② topotactic 을 comp1/modelc 에 한 번 돌린다** (추가 계산 **1건, 작다**). 식 (3) 은 *"가장 불안정한 Li 하나를 빼낸 완화 슈퍼셀 − 원본"* 이면 끝이고, 우리는 이미 comp1/modelc 슈퍼셀과 완화 파이프라인이 있다. 나오면 **우리 창이 [2.256, V_topo,ext] 라는 괄호**가 되어 실험값과 붙일 수 있는 유일한 상한이 생긴다. ⚠ 보고량 카드부터: *"가장 불안정한 Li 자리"* 는 **무질서 계에서 여럿**이므로 선택·집계 규칙(최고? 최저? 분포?)을 먼저 선언해야 한다 (CLAUDE.md 계산 규율).
4. **`interface_reactivity_v2` 를 `Fig. 4d` 형태로 그린다** (추가 계산 0~소). 이미 전압분해 도구가 있다. **0–5 V 를 촘촘히 스캔해 comp1\|LiCoO₂ 곡선 + 내재 안정구간 막대**를 그리면, `Fig. 4d`(가넷) 와 나란히 놓아 *"황화물은 같은 그림에서 한 자릿수 깊다"* 를 시각화할 수 있다.
5. **`sei_products.json` 에 열 하나 추가: "리뷰가 뭐라 하는가"** (추가 계산 0). 특히 **Li₃P 의 역할 충돌**(§7b)을 명시적으로 기록한다. 지금 우리 원장은 Li₃P 를 누설원으로 단정하는데, 문헌은 LiPON·Li₃PO₄ 계면에서 부동태로 쓴다. 판정을 뒤집자는 게 아니라 **조건(농도·연속성·이웃 상)을 붙이자**는 것이다.
6. **`Fig. 1` 을 우리 계면 캠페인 범위 그림으로 재사용** (추가 계산 0). 우리가 실제로 계산한 칸(SE/양극, SE/탄소, SE/Li)과 안 한 칸을 12칸 위에 색칠하면 "정직 목록"(comparison §H)이 한 장이 된다.
7. **Table 1 을 도판트 선정 근거로 인용** (추가 계산 0) — **"O·S 화학에서 란타나이드는 Li 금속 대비 안정"** 이 우리 Nd 선택의 계열 수준 문헌 근거다. ⚠ Nd 개별 검증이 아니므로 "계열" 이라고 쓴다.

---

## 9. 인용 가능 문장 (deck/paper 용)

> 아래는 **이 리뷰를 인용**하는 문장이다. 원출처 값을 쓸 때는 원출처를 단다.

- (ESW 정의) "Following the convention laid out by Xiao et al., the electrochemical stability window is the voltage range over which the compound lies exactly on the grand-potential convex hull constructed at μ_Li = μ⁰_Li − eV, and this thermodynamic window represents the **worst case**, i.e. no kinetic stabilization."
- (우리 onset 의 위상) "Our computed oxidation onset of 2.256 V for Li₆PS₅Cl is therefore a **lower bound**; the topotactic limit, which assumes maximal kinetic stabilization, defines the corresponding upper bound."
- (황화물 축 ①) "Sulfide electrolytes are predicted to oxidize at ~2–2.5 V vs Li, and the once-claimed 0–5 V windows from cyclic voltammetry were shown to be an artefact of insufficient reaction area: adding carbon to LGPS reveals the oxidation onset at ~2.1 V, in agreement with the DFT prediction."
- (탄소 경고 — 우리 복합체 설계에 직결) "Decomposition of the sulfide electrolyte occurs **wherever it contacts an electron path**, including the conductive additive and the current collector; because these interfaces are not on the Li-ion transport route to the active material, the resulting degradation is not immediately visible in short-term cycling."
- (아지로다이트 산물) "For Li₆PS₅Cl, elemental sulfur, lithium polysulfides, P₂S_x and **LiCl** have been identified as oxidation decomposition products by XPS, and Li₂S and Li₃P at the Li-metal interface — consistent with the phases predicted from grand-potential decomposition." (원출처: Auvergniot 2017 ×2, Wenzel 2018)
- (S↔O 교환) "The driving force between sulfide electrolytes and oxide cathodes exceeds 300 meV/atom and proceeds by S²⁻/O²⁻ exchange, because the P–O bond (596.6 kJ/mol) is far stronger than P–S (346 kJ/mol) while transition-metal–S and –O bond energies are comparable; Li₃PO₄, whose formation energy is −2.767 eV/atom, is the thermodynamic sink."
- (혼성 = 우리 O/B 축) "Among the composition levers surveyed — polarizable anions, nitride chemistry, high Li content and removal of reducible cations — **only increasing covalent M–X hybridization (P–O, B–O) improves ionic conductivity, reduction stability and oxidation stability simultaneously**; every other lever trades oxidation stability away."
- (실험 처방) "Voltage limits of solid electrolytes should be measured with a carbon-composite working electrode and a non-Li counter/reference electrode, and read from the potential at which the current rises sharply rather than from an arbitrary cut-off current."

---

## 10. 주의 / 한계 (over-claim 방지) — **서지·내부 불일치 한 절로 모음**

1. **⚠ "There are amendments to this paper"** — 표지에 정정 고지가 있으나 **이 PDF 에 정정 내용이 없다.** 어떤 수치가 정정됐는지 모른다. 개별 값을 원고에 옮기기 전에 정정본 확인이 필요하다. (SI 없음은 확인 — 본문에 SI 언급 0.)
2. **⛔ 서지 오기 (§0a)** — 파일명 `Banerjee2020_…` 와 계보 카드의 *"Banerjee/Wang/Meng"* 은 둘 다 틀렸다. 이 편은 **Xiao/Wang(Samsung)/Bo/Kim/Miara/Ceder**. inbox #104 의 `Bai2026`(실제 1저자 Cronk) 에 이어 **두 번째 파일명 오기**다 — inbox 파일명을 서지 근거로 쓰지 않는 관행이 필요하다.
3. **⛔ 리뷰의 요약을 원출처의 주장으로 둔갑시키지 말 것.** 이 편의 수치는 **전부 재인용**이고, 때로 **같은 물질에 두 값을 나란히 적는다**(LGPS 1.7–2.1 ref.65 **vs** 2.1–2.3 ref.64; Li₃OCl 3 V ref.64 **vs** 2.55 V ref.189; LATP 산화 4.21 **or** 4.8 V). *"DFT 가 X V 라고 한다"* 라고 뭉뚱그리면 hull 세대 차이를 지우게 된다.
4. **🔴 내부 불일치: LLZO 의 창이 두 그림에서 다르다.** `Fig. 6`(저자들이 직접 그린 지도) 의 가넷 점은 **figure-read (0.09, 2.97) V**(= [Zhu15] 0.05–2.91 과 정합)인데, `Fig. 4d`(ref.145 Miara 2015 에서 재수록) 의 LLZO 안정막대는 **figure-read 0.43–3.41 V**다. 본문은 또 *"LLZO 산화한계 2.9 **또는** 3.2 V"* 라고 적는다. **세 값이 다 다르다.** 오류라기보다 **출처가 다른 그림을 한 리뷰에 병치한 결과**지만, 인용할 때 어느 그림/어느 ref 인지 반드시 명시해야 한다. LLTaO 도 같다(`Fig. 6` 0.85–3.10 vs `Fig. 4d` 0.88–3.57 — 환원쪽은 맞고 산화쪽이 0.47 V 벌어진다).
5. **🔴 우리 원장과의 판정 충돌: Li₃P.** 우리 `sei_products.json` 은 Li₃P 를 `conductor-LEAK`(MP gap 0.70 eV) 로 두고 "O 가 이것을 Li₂O 로 대체한다" 를 서사의 축으로 쓴다. 이 리뷰는 **Li₃PO₄/Li·LiPON/Li 계면에서 Li₃P 를 부동태 산물로** 쓴다(ref.222 XPS·ref.73). **둘 다 맞을 수 있다** — 부동태 여부는 밴드갭만이 아니라 **연속성·두께·이웃 상**에 달렸다. 그러나 우리 문장 *"Li₃P 는 전자를 샌다"* 를 무조건적으로 쓰면 이 리뷰와 정면으로 부딪힌다. **조건절을 달아야 한다.**
6. **⚠ `Fig. 3a` 의 기준전극이 Li-In 이다.** 그림 축이 *"Open-circuit voltage vs Li⁺/Li-In"* 이다. 3.2–3.4 V 에서 계면저항이 뛴다는 서술을 우리 vs Li/Li⁺ 축으로 옮기려면 **+0.6 V 대의 오프셋**을 더해야 한다(≈3.8–4.0 V vs Li/Li⁺). Zuo 2023 에서 이미 한 번 겪은 함정이다.
7. **⚠ 아지로다이트 절의 실체는 "유사할 것" 한 문장이다.** 소절이 있다는 사실과 **고유 수치가 있다는 것은 다르다.** 이 편에서 Li₆PS₅Cl 에 대해 인용 가능한 것은 (a) **산물 목록**(원소 S·폴리설파이드·P₂S_x·LiCl / Li₂S·Li₃P) (b) **`Fig. 5a` 의 반응에너지 칸**(실은 ref.67 값) (c) **셀 성능 300 사이클**(ref.117) (d) **Li₆PS₅Br 의 O 도핑 효과**(ref.120) 넷뿐이다. 창·Ea·σ 고유값은 **없다**.
8. **⚠ 할라이드가 거의 없다.** 2019년 집필 시점이라 Li₃YCl₆·Li₃YBr₆·Li₃InCl₆ 가 *"recently reported"* 로 한 문단이고, **소절이 없다.** `Fig. 6` 에 점 2개(figure-read 창 3.56 V·2.56 V)뿐이다. 현대 할라이드 SE 비교에는 못 쓴다.
9. **⚠ 기계·덴드라이트·젖음은 범위 밖이라고 명시**(*"beyond the scope"*). 우리 축 C(기계)와는 겹치는 게 없다.
10. **⚠ 온도·압력**: 전부 0 K DFT 기반 인용이고 PV 항 무시. 800 °C 소결 계산(`Fig. 4c`, ref.80)만 예외적으로 온도가 들어간다.
11. **⚠ `Fig. 5a` 를 "이 리뷰의 데이터" 로 인용하면 안 된다** — 캡션이 *"Panel a is reproduced with permission from ref.67, Elsevier"* 라고 명시한다. 정본은 Xiao 2019 Joule 의 SI 다 (§12a).
12. **🔶 형제 digest 와의 표현 충돌 1건 (사람이 정리해야 한다).** 같은 날 작성된 `nolan2018_computation_accelerated_design_review`(#7) 가 자기 카드에 *"`anodic/cathodic limit` 의 **정의 문장**이 실제로 있는 **유일한 편**(p. 2022)"* 이라고 적었다. **본 digest 는 #8 에도 같은 성격의 정의 문장이 있음을 확인했다**(「Electrochemical stability」 절, 식 (1)(2) 와 함께). 두 편이 동시에 돌아서 서로를 못 봤다. ⇒ **#7 카드의 "유일한 편" 표현을 "정의 문장을 가진 두 편 중 하나(다른 하나는 #8)" 로 완화**하는 편집이 필요하다. 우열은 §7c 표 참조 — **#7 은 시간 우선권(2018)·Mo 계보, #8 은 번호 붙은 식 + worst/best-case 위상**이다. ⛔ 이 digest 는 남의 파일을 고치지 않으므로 여기에 기록만 남긴다.

---

## 11. 용어 미니사전 (이 편을 읽는 데 필요한 것만)

- **type I / II / III 계면** — (ref.51,63 의 Janek/Wenzel 분류를 이 리뷰가 채택) **I** = 열역학적으로 안정, 반응 구동력 0. **II** = 반응해서 **MCI** 를 만든다. **III** = 반응하지만 **SEI** 를 만들어 스스로 멈춘다. **장기 안정은 I 과 III 뿐**이고, III 의 성패는 **SEI 의 이온전도도**에 달렸다.
- **MCI (mixed ionic–electronic conducting interphase)** — 전자와 이온을 **둘 다** 통과시키는 계면상. 전자가 계속 공급되니 반응이 안 멈춘다 → **SE 를 계속 먹는다**. 금속·금속간화합물(Li–Ge, Li₁₇Sn₄, Ti⁰)이 나오면 여기.
- **SEI (solid electrolyte interphase)** — 이온은 통과시키되 **전자는 막는** 계면상 → 반응이 자기제한. LiCl·Li₂O·Li₃N·LiF 같은 Li-이원 절연체가 전형.
- **grand potential Φ** — `Φ = E − n_Li·μ_Li`. Li 를 **저장조와 교환 가능**하게 열어둔 열역학 퍼텐셜. 전압을 걸면 μ_Li 가 정해지므로(식 1), **"이 전압에서 이 상이 살아남나"** 를 hull 로 물을 수 있다.
- **topotactic** — 결정 골격을 **그대로 둔 채** 원자만 넣거나 빼는 것. 새 상을 만들 필요가 없어 **동역학 장벽이 거의 없다** ⇒ 이 경로로 일어나는 분해는 못 막는다 ⇒ 여기서 나오는 창이 **상한**.
- **pseudo-binary (유사이원)** — 두 고체 A·B 를 섞는 비율 x 를 0→1 로 훑으며 각 조성에서 **hull 대비 에너지 이득**을 재고 그 **최솟값**을 취하는 것. 계면에서 얼마나 섞일지 모르니 **가능한 모든 비율을 다 보는** 보수적 방법. = 우리 `InterfacialReactivity`.
- **anion exchange (음이온 교환)** — 황화물 SE 의 PS₄³⁻ 안 S²⁻ 와 산화물 양극의 O²⁻ 가 자리를 바꾸는 것. **P–O 결합이 P–S 보다 훨씬 세고(596.6 vs 346 kJ/mol)** TM–S 와 TM–O 는 비슷해서, 알짜로 **PO₄³⁻ + TM 황화물**이 남는 쪽이 이득이다.
- **hybridization (혼성)** — 비금속 M 과 음이온 X 의 궤도가 섞이는 정도. 섞이면 **결합상태가 내려가고 반결합상태가 올라간다** ⇒ 산화(전자 뽑기)도 환원(전자 넣기)도 어려워진다 ⇒ **창이 양쪽으로 넓어진다**. 이 리뷰의 핵심 물리.
- **복합 WE (composite working electrode)** — SE 에 탄소를 섞어 만든 작업전극. **SE↔전자경로 접촉면적**을 키워 CV 신호를 수 자릿수 올린다. 이게 없으면 CV 는 분해를 못 본다.
- **operando / in-situ XPS** — 셀을 돌리면서(또는 Li 를 증착하면서) 계면 화학종을 보는 것. 묻힌 계면을 안 뜯고 보는 몇 안 되는 방법.
- **ToF-SIMS** — 2차이온 질량분석. **PO_x^y⁻·SO_x^y⁻ 같은 분자 단편**을 잡아내 상 이름을 못 주는 XPS 를 보완한다.

---

## 12. ★ 본 digest 의 독립 재분석 — **논문에 인쇄돼 있지 않은 것**

> 이 편은 SI 도 데이터 파일도 없다. 그래서 정량 정보는 **그림 안에만** 있다. PDF 벡터 좌표 + 컬러바 역매핑으로 두 그림을 수치화했다. **모두 `figure-read`** 다.

### 12a. `Fig. 5a` 히트맵 전 셀 복원 — 그리고 **Xiao 2019 Table S2 와의 대조**

방법: 페이지 15 의 컬러바(0 → −600 meV/atom)를 눈금 레이블 좌표로 캘리브레이션(19.0 pt / 100 meV, 눈금선 3개로 교차확인)하고, 각 셀 중심 RGB 를 컬러바 상 최근접점으로 역매핑. 셀 내부는 완전 균일(5×3 표본 편차 0).

| (행) \ (열) | NCM | LCO | LMO | LFPO | LPSCl | LGPS | LPS | LLZO |
|---|---|---|---|---|---|---|---|---|
| Li₂ZrO₃ | ≈0 | ≈0 | −32 | −73 | **−85** | −95 | −119 | ≈0 |
| LiNbO₃ | ≈0 | ≈0 | ≈0 | −25 | **−133** | −138 | −174 | −73 |
| LiTaO₃ | ≈0 | ≈0 | ≈0 | −19 | **−119** | −107 | −150 | −73 |
| LiH₂PO₄ | −63 | −73 | −13 | ≈0 | **−54** | −44 | −19 | −143 |
| LiTi₂(PO₄)₃ | −73 | −63 | ≈0 | ≈0 | **−73** | −73 | −56 | −194 |
| LiBa(B₃O₅)₃ | ≈0 | ≈0 | ≈0 | ≈0 | **≈0** | ≈0 | ≈0 | −80 |
| LiPO₃ | −85 | −73 | −44 | ≈0 | **−56** | −51 | −32 | −206 |
| LiLa(PO₃)₄ | −100 | −80 | −51 | ≈0 | **−63** | −61 | −44 | −221 |
| LiCs(PO₃)₂ | −73 | −56 | ≈0 | ≈0 | **−85** | −80 | −68 | −168 |
| **LPSCl** | **−298** | **−308** | **−424** | **−100** | — | — | — | — |
| LGPS | −325 | −334 | −468 | −100 | — | — | — | — |
| LPS | −424 | −429 | −540 | −82 | — | — | — | — |
| LLZO | ≈0 | ≈0 | −63 | −97 | — | — | — | — |

**대조 (우리 `xiao2019_cathode_coating_screening.md` §4b 가 SI 실물에서 전사한 정본값)**

| 셀 | 본 digest figure-read | Xiao 2019 Table S2 (정본) | 차 |
|---|---|---|---|
| LPSCl\|LMO | −424 | **−421** | **3** ✅ |
| LPSCl\|LFPO | −100 | **−101** | **1** ✅ |
| LPSCl\|NCM | −298 | **−330** | 32 ⚠ |
| LPSCl\|LCO | −308 | **−339** | 31 ⚠ |
| LiNbO₃\|LPS | −174 | **−164** | 10 |
| LiTaO₃\|LPS | −150 | **−139** | 11 |
| Li₂ZrO₃\|LPS | −119 | **−115** | 4 ✅ |

⇒ **판정 3가지**
- ✅ **그림은 SI 표를 재현한다.** 컬러 기울기가 가파른 구간(초록·주황)에서는 **1–4 meV/atom** 이내로 맞는다.
- ⚠ **−300 대의 연노랑 구간은 컬러바 민감도가 절반(0.47 ΔRGB/meV)** 이라 판독 오차가 커진다 — LCO·NCM 두 칸의 ~31 meV 격차는 **판독 한계 + 재조판 가능성**으로 본다(캘리브레이션 오차는 눈금 교차검증으로 배제했다).
- ⛔ **따라서 인용은 figure-read 가 아니라 Xiao 2019 SI 로 한다.** 이 재분석의 쓸모는 *"이 리뷰의 대표 그림이 우리가 이미 가진 표와 같은 데이터임을 독립 확인했다"* 는 것이지, 새 숫자를 만드는 게 아니다.

**🔑 그래도 새로 나오는 것 하나**: `Fig. 5a` 는 **Li₂ZrO₃ ↔ LPSCl 을 −85 meV/atom** 으로 찍는다 — 즉 저자들 자신의 **100 meV/atom 문턱 아래 = "좋음"** 이다. 계보 #5 가 지목한 *"Li₂ZrO₃ 가 편마다 다르게 판정된다"* 목록에 **네 번째 판정**이 추가된다: **[Aykol16] ⛔ 탈락 · [Nolan21] ✅ 생존 · [Lu24] 실험 ✅ · [Xiao20] `Fig. 5a` 🟡 통과하되 비폴리음이온 중 최악**(같은 행의 NCM·LCO·LLZO 칸이 ≈0 인데 LPSCl 칸만 −85). ⚠ 단 **Xiao 2019 SI Table S1 에서 Li₂ZrO₃ 는 filter 4 탈락**이었다(LPS 상대 −115) — **같은 저자·같은 데이터인데 SE 를 LPS 로 재면 탈락, LPSCl 로 재면 통과**다. 문턱을 인용할 때 **어느 SE 상대인지**까지 박아야 한다.

### 12b. `Fig. 6` ESW 지도 전 점 복원 — **9 계열 18점**

방법: 축 눈금 레이블 중심 좌표로 선형 캘리브레이션(x: 5→0 이 172.45→327.75 pt; y: 0→5 가 219.55→68.20 pt), 범례 색 9종으로 픽셀 분류 후 연결성분 중심. **검증 2건이 통과**했다 — ① 본문 인쇄값 **Li₃PS₄ 환원 1.69 V** ↔ 황화물 점 하나가 **정확히 x=1.69** ② 가넷 점 하나가 **(0.09, 2.97)** ↔ [Zhu15] LLZO **0.05–2.91** (0.06 V 이내).

| 계열 | 환원한계 (V) | 산화한계 (V) | 창 폭 (V) | 원 크기(σ 자릿수 대리) |
|---|---|---|---|---|
| Ideal (기준점) | 0.00 | 4.97 | **4.98** | 큼 |
| **황화물** | **1.69** | **2.36** | **0.67** | 중 ← *Li₃PS₄ 로 추정(본문값 일치)* |
| **황화물** | 2.31 | 2.34 | **0.03** | **가장 큼** |
| **황화물** | 1.96 | 2.14 | 0.18 | 큼 |
| **황화물** | 1.69 | 1.91 | 0.22 | 중 |
| **황화물** | 1.57 | 2.18 | 0.60 | 작음 |
| 가넷 | 0.09 | 2.97 | 2.88 | 중 ← *LLZO 로 추정* |
| 가넷 | 0.85 | 3.10 | 2.25 | 중 |
| 가넷 | 1.03 | 3.26 | 2.23 | 중 |
| LiPON | 0.70 | 1.08 | **0.38** | **가장 작음** |
| 페로브스카이트 | 1.95 | 3.74 | 1.79 | 큼 |
| 반페로브스카이트 | −0.04 | 2.75 | 2.79 | 큼 |
| NASICON | 2.06 | 4.50 | 2.44 | 중 |
| NASICON | 2.36 | 4.20 | 1.84 | **가장 큼** |
| NASICON | 2.78 | 4.31 | 1.53 | 큼 |
| 할라이드 | 0.66 | 4.23 | **3.56** | 큼 |
| 할라이드 | 0.58 | 3.14 | 2.56 | 큼 |
| Li₃N | −0.01 | 0.50 | 0.51 | 큼 |

**여기서만 나오는 것 4가지**
1. **황화물 5점의 산화한계가 1.91–2.36 V 안에 다 들어간다** — 폭 0.45 V. **우리 2.256 V 는 이 띠의 위쪽 끝**에 있다. ⚠ **어느 점이 아지로다이트인지는 표기가 없다** — 라벨이 없으므로 "Li₆PS₅Cl 은 여기" 라고 못 쓴다.
2. **창이 가장 넓은 실재 SE 는 할라이드(3.56 V)** 이고, 그 다음이 반페로브스카이트(2.79) · 가넷(2.88) 이다. **NASICON 이 산화한계 최고(4.50 V)** 지만 환원한계도 높아(2.06–2.78) 창은 중간이다.
3. **σ 가 가장 큰 원 두 개는 창이 0.03 V(황화물)와 1.84 V(NASICON)** — 즉 **σ 챔피언이 창 챔피언인 적이 없다.** `Fig. 7` 의 trade-off 주장을 이 지도가 정량으로 받친다.
4. **"이상점"(0, 4.97)에 가까운 점이 하나도 없다.** 가장 가까운 것이 할라이드(0.66, 4.23) — 본문의 *"which has yet to be achieved by any SE"* 가 그림으로 확인된다.

### 12c. `Fig. 4d` 안정구간 막대 좌표 복원

벡터 좌표 직독(x: 0→5 V 가 389.9→542.1 pt): **LLZO 0.43–3.41 · LLTaO 0.88–3.57 · LCO 1.89–≥5 · LMO 1.44–≥5 · LFPO 2.21–≥5 V**(뒤 셋은 화살표 = 5 V 초과). ⚠ §10-4 의 불일치 근거가 이 값이다. 원출처는 ref.145(Miara 2015) 이고 `Fig. 6` 은 저자 재편집판이라 **세대가 다른 두 계산을 한 리뷰가 병치**한 것으로 본다.

### 12d. 그림 크로핑 보정 기록

`tools/litdb/extract_figures.py` 자동 실행은 **6개 추출 / 2개 제외**였고, 제외 2개(`Fig. 1` p2 · `Fig. 6` p16)는 **"영역 없음"** 오탐이었다(둘 다 실제로 그림이 있다). 또 `Fig. 3`·`Fig. 5`·`Fig. 7` 은 **패널 일부만** 잘렸다(`Fig. 3` 은 a·b 가 통째로, `Fig. 5` 는 226 px 높이 띠만). 캡션 앵커 + 그래픽 union 좌표로 **5장을 수동 bbox 로 다시 잘라** `litdb/figures/xiao2020_interface_stability_ssb_review/` 에 덮어쓰고 `figures.json` 에 `note` 로 표시했다. **이 리뷰처럼 그림이 쪽 상단에 있고 캡션이 본문 중간에 오는 조판에서 자동 크로핑이 약하다** — 다음 Nature Reviews 편에서도 확인이 필요하다.

---

## 13. 한 줄 결론

**계보 #8 은 "새 방법" 이 아니라 "채점표" 다** — #1–#7 이 쌓은 grand-potential ESW · pseudo-binary 반응에너지 · hull 분해산물을, 2015–2019년 실험(고감도 CV·operando XPS·ToF-SIMS·STEM-EDS·성분분해 EIS) 앞에 세워 **"상 이름은 거의 다 맞았고, 전압은 실험을 제대로 재면 맞았고, 비정질 여부와 속도는 못 맞춘다"** 로 판정한다. 그리고 **#1–#6 에 없던 우리 무대(황화물·아지로다이트)가 두 리뷰(#7·#8)에서 들어오는데, #8 은 전용 소절 + `Fig. 5a` 의 `LPSCl` 라벨을 주는 대신 아지로다이트 고유 수치를 안 준다**(*"다른 황화물과 유사할 것"* 한 문장). 우리에게 남는 실질 소득은 셋: **① ESW 정의를 "최악 시나리오 하한" 으로 말할 활자 확보(#7 과 함께) ② 우리 `interface_reactivity` 산물 5종 전부가 이 리뷰 안에 예측으로 있고 그중 4종은 실험 관측까지 붙는다 — 계보 전체에서 우리 산물이 실험과 이어지는 첫 지점 ③ `Fig. 7` 이 "공유결합 혼성만이 σ·환원·산화를 동시에 개선한다" 고 못박아, 우리 O-치환/B₂O₃ 축이 문헌에서 서 있는 자리를 지정해준다.**

---

<!-- MERGE-BLOCK — 공유 파일은 이 digest 가 직접 고치지 않는다 (동시 작업 충돌 회피).
     아래 세 덩어리를 그대로 복사해 넣으면 된다. 2026-09-12 작성. -->

<!-- ===== (a) litdb/INDEX.md — 표 행 (Reference key 표에 추가) ===== -->
<!--
| **[Xiao20Rev]** ⭐⭐코팅 계산 계보 #8 = **계보의 채점표** · ★ 우리 ESW 정의를 *"worst-case 하한"* 으로 못박을 활자 · ⭐ **#1–#6 에 없던 우리 무대(황화물·아지로다이트)가 #7 과 함께 들어오는 편** | **Yihan Xiao**¹²/Yan Wang³/Shou-Hang Bo²⁴/Jae Chul Kim²⁵/Lincoln J. Miara³/**Gerbrand Ceder\***¹² (¹UC Berkeley MSE · ²LBNL MSD · ³**Samsung Research America** Advanced Materials Lab · ⁴UMich–SJTU JI · ⁵Stevens Inst.) 2020 *Nature Reviews Materials* **5**, 105–126 (DOI 10.1038/s41578-019-0157-5, 온라인 2019-12-09; inbox #112 본문 22 pp · **SI 없음** · refs 250) — "**Understanding interface stability in solid-state batteries**". ⛔⛔ **서지 정정**: 파일명 `Banerjee2020_…` 과 계보 카드의 *"Banerjee/Wang/Meng"* 은 **오기**다 — 1저자 **Xiao**, 교신 **Ceder**, "Wang" 은 Samsung 의 **Yan** Wang. **Meng 그룹이 아니므로 "Cronk 2026 과 같은 그룹" 연결은 무효**(관계는 그룹이 아니라 *전제↔검증*, digest §7f). **자체 계산 0·실험 0 = 순수 종합**. **핵심 기여 = 계면 모델 4층의 위계**: ① grand-potential ESW(**번호 붙은 식 (1)–(2)** + *"창 = hull 위에 정확히 놓인 전압 구간"* — ⚠ 이 문장 자체는 **[Nolan18](#7) p. 2022 에도 있다**; #8 의 차별점은 **번호 붙은 식 + worst/best-case 위상 선언**) = **최악 시나리오** / ② **topotactic**(식 3, Na₃PSe₄ **V_topo,ext 2.75 V**) = **최선 시나리오** / ③ pseudo-binary 혼합(식 4 = 우리 `InterfacialReactivity` 와 문자 그대로 동일, **Li·O 개방계 확장 명시**) = 최대 구동력 / ④ explicit 슈퍼셀·AIMD(<1 ns, 시작배치 민감 — 저자 자인). **황화물 판정**: S²⁻ 산화 **~2–2.5 V**, 창 1.5–2.5 V(LGPS 1.7–2.1 ref.65 **또는** 2.1–2.3 ref.64); **CV 의 0–5 V 주장은 반응면적 부족의 산물** — 탄소 복합 WE 로 재면 **2.1 V 산화·1.7 V 환원**(ref.97,98, `Fig. 3b`) · operando XPS 2.7 V(ref.99); **SE 는 전자경로에 닿는 모든 곳(집전체·도전재)에서 분해**된다(ref.69,70). **산화물 양극과 >300 meV/atom**, 기전 = **S↔O 교환**(P–O 596.6 vs P–S 346 kJ/mol) + **Li₃PO₄ 싱크**(생성E **−2.767 eV/atom**); Co 가 황화물로 **>50 nm** 확산(ref.47 STEM-EDS). ⭐ **「Argyrodites」 소절 있음(단 21줄 한 문단 — ⚠ #7 도 `Li₆PS₅Cl` 을 3회 명시하므로 "계보 최초" 는 아니다)**: Li₆PS₅Cl 산화산물 **원소 S·폴리설파이드·P₂S_x·LiCl**(예측 64,66,115 ↔ **XPS 관측 116,117**), Li 금속 대비 **Li₂S+Li₃P**(118), NCM622\|LPSCl 에서 **PO_x/SO_x 증가**(119 XPS+ToF-SIMS), **300 사이클 양호**(117), **Li₆PS₅Br 의 O 도핑이 안정성 개선**(120) — ⛔ **아지로다이트 고유 창·Ea·σ 수치는 0**, *"다른 황화물과 유사할 것"* 한 문장. **`Fig. 5a` 에 `LPSCl` 이 행·열 라벨로 직접 등장**(ref.67 재수록) → **본 digest 픽셀 정량화**(§12a): LPSCl\|LCO figure-read −308 ↔ **Xiao2019 Table S2 정본 −339**(LMO −424↔−421·LFPO −100↔−101 은 1–3 meV 일치) ⇒ **인용은 Xiao2019 SI 로**. **`Fig. 6` 18점 좌표 복원**(§12b, 검증 2건 통과: Li₃PS₄ 1.69 V·LLZO (0.09,2.97)↔[Zhu15] 0.05–2.91): 황화물 5점 산화한계 **1.91–2.36 V 띠**, 창 최광 = **할라이드 3.56 V**, σ 챔피언은 창이 0.03 V. **`Fig. 7` = 우리 O/B 축의 문헌 자리**: 조성 레버 5개 중 **공유결합 혼성(P–O·B–O)만 σ·환원·산화 3축 동시 개선**, 나머지 4개는 전부 산화를 희생. **Table 1** = 음이온×양이온 Li-대비 분류(stable/SEI former/MCI former) — **O·S 화학에서 란타나이드 안정 = 우리 Nd 도핑의 계열 수준 근거**. ⚠ **표지에 "There are amendments" 고지가 있으나 PDF 에 정정 내용 없음** · ⚠ **내부 불일치**: LLZO 창이 `Fig. 6`(0.09–2.97) ↔ `Fig. 4d`(0.43–3.41, ref.145 재수록) ↔ 본문(2.9 **또는** 3.2 V) **셋이 다름** · 🔴 **우리 원장과 충돌 1건**: 우리는 Li₃P = `conductor-LEAK`(gap 0.70 eV), 리뷰는 Li₃PO₄/Li·LiPON/Li 에서 **부동태 산물**(ref.222,73) · ⚠ `Fig. 3a` 축이 **vs Li-In** · ⚠ 할라이드 소절 없음(2019 시점) · ⚠ 기계·덴드라이트·젖음은 범위 밖 명시 | ✅ `papers/xiao2020_interface_stability_ssb_review.md` (2026-09-12, **그림 7장 전부 실독 + `Fig. 5a` 52셀·`Fig. 6` 18점·`Fig. 4d` 5막대 좌표 복원**) | **[외부]** 리뷰 (자체 계산 0 · 자체 실험 0) |
-->

<!-- ===== (b) litdb/comparison_vs_ours.md — 축별 추가 행 ===== -->
<!--
[축 B. 산화안정성 — B① (S²⁻-limited onset) 표에 추가]
| **B① 산화 onset — *정의 문장의 인용처*** | comp1/modelc **2.256 V** (grand-potential, LiS₄ 제외, MP2026) | **[Xiao20Rev]** 식 (1) `μ_Li = μ⁰_Li − eV` + 식 (2) `Φ = E − n_Li μ_Li` + **정의 문장**: *"the electrochemical stability window … corresponds to the range of voltages over which it is stable (**exactly on the grand potential convex hull**)"*, Li 제외 조성 `c − n_Li` 에서 최소화. **위상도 명시**: *"represents the **worst-case scenario** (no kinetic stabilization)"*, 핵생성 과전압은 전환전극 수준(수백 mV) | ✅ **같은 양·같은 기준·같은 정의.** ⛔ 값 비교 금지 — 리뷰 인용값은 2015–16 hull 세대(황화물 1.5–2.5 V). 🔑 **우리 2.256 V 를 "최악 시나리오 하한" 으로 기술할 근거가 여기 생겼다** ⇒ Zuo CV 2.5–2.7 V·Cronk dQ/dV 2.70 V 와의 0.3–0.5 V 차가 **모순이 아니라 동역학 여유**로 설명된다. ⛔ **우리에게 층 ②(topotactic, 식 3)가 없다 — 상한이 없다** |

[축 B. B③ (cathode 계면 반응성) 표에 추가]
| **B③ cathode 계면 — *우리 계가 이름으로 찍힌 첫 그림*** | comp1\|LiCoO₂ **−0.3227 eV/atom** (`InterfacialReactivity(use_hull_energy=True)`, MP2026; 산물 Co₉S₈·Li₂SO₄·Li₃PO₄·Li₂S·LiCl, min @ x=0.5302) | **[Xiao20Rev]** `Fig. 5a` 의 **LPSCl 행 × LCO 열** (ref.67 재수록). 본 digest 픽셀 복원 **figure-read −308 meV/atom** (NCM −298 · LMO −424 · LFPO −100) — **정본은 [Xiao19] Table S2 −339 / −330 / −421 / −101**. 본문 일반화: 황화물↔산화물 양극 **>300 meV/atom**, 기전 **S↔O 교환 + Li₃PO₄ 싱크(−2.767 eV/atom)** | ✅✅ **같은 양 + 같은 계 + 같은 도구**(리뷰가 *"explicit feature in the Materials Project"* 로 지목). 우리 **−322.7** vs 정본 **−339** = **16 meV/atom 차, hull 세대(MP2026 vs MP2018) 로 설명 가능한 범위** ⇒ **계보에서 우리 *조성 그대로*(Li₆PS₅Cl\|LiCoO₂) 가 문헌값과 1:1 대조되는 첫 지점** (⚠ [Nolan18](#7) 이 주는 −0.41 eV/atom 은 **Li₃PS₄**\|LCO 이지 아지로다이트가 아니다). ⛔ figure-read −308 은 인용하지 않는다(§12a: 연노랑 구간 판독 민감도 절반) |

[축 B. B② (산물) 표에 추가 — ★ 실험 관측 연결]
| **B② 산화 분해산물 — *예측 ↔ 실험 관측*** | `interface_reactivity` comp1\|LCO 산물 5종 **Li₃PO₄ · Li₂SO₄ · Li₂S · LiCl · Co₉S₈**; onset 반응 `Li₆PS₅Cl → Li₃PS₄ + LiCl + **S** + 2Li⁺ + 2e⁻` | **[Xiao20Rev]** ⓐ **아지로다이트 산화산물 = 원소 S·폴리설파이드·P₂S_x·LiCl** (예측 ref.64,66,115 ↔ **XPS 관측 ref.116,117 Auvergniot 2017 ×2**) ⓑ **PO₄³⁻·SO₄²⁻ 폴리음이온** (ToF-SIMS ref.78,119) ⓒ **TM 황화물 Co₉S₈·MnS·CoNi₂S₄** (XRD·TEM ref.107, 300 °C) ⓓ **Li₃PO₄ 는 XRD 로 직접 관측**(ref.107) ⓔ S–S 가교 XPS 가 충전에 자라고 방전에 줄어든다(`Fig. 3c`, ref.102) | ✅✅ **우리 산물 5종이 전부 리뷰 안에 예측으로 있고, 그중 Li₃PO₄·SO₄²⁻·Co₉S₈계·LiCl 4종은 실험 관측까지 붙는다** ⇒ **계보 전체에서 우리 산물 목록이 실험과 연결되는 첫 지점**. ⚠ **P₂S₅ 는 XPS 로 직접 관측된 적 없다**(대신 S–S) — 우리 산물 서술에서 "관측됨" 을 일괄 적용 금지 |

[축 E. 환원/음극 표에 추가 — 🔴 충돌]
| **E 환원 산물의 *역할* — 🔴 우리 원장과 충돌** | `sei_products.json`: **Li₃P gap 0.70 eV = `conductor-LEAK`** (무도핑 음극 누설 산물, O 도입이 Li₂O 로 대체) · Li₂S 3.90 eV `marginal` · LiCl 6.65 `insulator` | **[Xiao20Rev]** Li₃PO₄/Li → **Li₃P + Li₂O** 이고 *"**These reaction products are passivating** and can enable the stable cycling of Li symmetric cells"*(ref.222 XPS 확인); LiPON/Li → Li₃P+Li₂O+Li₃N 이 *"not only **block electron conduction** but also permit Li-ion diffusion"*(ref.73,174,175). Li₂S 는 **Li-안정 이원상 = SEI 후보**로 분류 | 🔴 **같은 상을 반대로 읽는다.** 둘 다 성립 가능 — 부동태 여부는 밴드갭만이 아니라 **연속성·두께·이웃 상**에 달렸다. ⇒ **우리 문장 "Li₃P 는 전자를 샌다" 에 조건절을 달아야 한다**(단독 상 · 연속층 여부). ⛔ 무조건문으로 쓰면 이 리뷰와 정면 충돌 |

[축 F. 도핑 표에 추가]
| **F 도판트 선택의 계열 근거** | Nd 도핑 (Nd₂O₃ → NdPO₄·NdOCl·NdCl₃ 등 광갭 산물) | **[Xiao20Rev]** `Table 1`: 음이온 X × 양이온 M 을 Li 금속 대비 **stable / SEI former / MCI former** 로 분류(Li–M–X 상도 근거, ref.224,233 + MP). **O 화학·S 화학 모두 "lanthanide series" 가 stable 열**에 있다 | 🟡 **계열 수준 지지**(Nd 개별 검증 아님). ⛔ "Nd 가 안정하다고 문헌이 말한다" 로 쓰지 말고 **"란타나이드 계열이 O·S 화학에서 Li 금속 대비 안정으로 분류된다"** 로 쓴다 |

[🔧 방법 원전 블록 (J-7 / L-5 계열) 에 추가 — 물성값 없는 항목]
| **계면 모델 4층의 위계 + CV 함정의 원인·처방** | **[Xiao20Rev]** | ① ESW=worst / ② topotactic=best / ③ pseudo-binary=최대 구동력(Li·O 개방 확장) / ④ explicit·AIMD=국소 재배열(<1 ns·시작배치 민감). **CV 처방 3**: ⓐ **탄소 복합 WE 로 반응면적 확대**(평면전극 10 nm 층은 0.1 mV/s 에서 **~0.3 µA/cm²** 밖에 안 나온다) ⓑ **cutoff 전류 금지 → 전류 급증 전위 + 산화산물의 환원 피크** ⓒ **Li 대극/기준극 금지 → In·Au 대극 + In·Ag₃SI/Ag 기준극 3전극** + TEM·XPS 보강. **`Fig. 1` = 양극 복합체 계면 12칸 목록**(우리가 안 본 칸을 색칠할 틀) |
-->

<!-- ===== (c) kb/syntheses/cathode_coating_computational_lineage.md — #8 행 전체 교체 ===== -->
<!--
| 8 | **Xiao/Wang/Bo/Kim/Miara/Ceder 2020** *Nat. Rev. Mater.* **5**, 105–126 `10.1038/s41578-019-0157-5` — *Understanding interface stability in solid-state batteries* (UC Berkeley + LBNL + **Samsung Research America**) ⛔ **서지 정정 2026-09-12**: 이 카드가 적어둔 *"Banerjee/Wang/Meng"* 은 **오기**다(파일명 오기가 옮겨온 것). 1저자 **Yihan Xiao** · 교신 **Gerbrand Ceder** · "Wang" 은 Samsung 의 **Yan** Wang. **Meng 그룹이 아니다** | 계보의 **채점표**. #1–#7 이 세운 계산틀을 2015–19 실험 앞에 세워 판정: **상 이름은 거의 다 맞고, 전압은 실험을 제대로 재면 맞고(CV 0–5 V 는 반응면적 부족의 산물 — 탄소 섞으면 2.1 V), 비정질 여부·속도는 못 맞춘다**. 기여 = **모델 4층 위계**(① ESW=worst · ② **topotactic**=best 식 (3) · ③ pseudo-binary 식 (4) + **Li·O 개방계** · ④ explicit/AIMD). ★ **번호 붙은 식 (1)–(4) + "창 = hull 위에 정확히 놓인 전압 구간" 문장 + worst/best-case 위상 선언** (⚠ 문장 자체는 #7 p. 2022 에도 있다 — #8 의 차별점은 번호 붙은 식과 위상 선언) | ⭐⭐ **#1–#6 에 없던 우리 무대가 #7 과 함께 들어온다** — 「Sulfides」 대절 3.5쪽 + **「Argyrodites」 전용 소절**(단 21줄 한 문단; #7 은 소절 없이 창 수치를 주고 #8 은 소절을 주되 수치를 안 준다) + **`Fig. 5a` 행·열에 `LPSCl`**. 🔑 **우리 `interface_reactivity` 산물 5종(Li₃PO₄·Li₂SO₄·Li₂S·LiCl·Co₉S₈)이 전부 예측으로 있고 4종은 XPS·ToF-SIMS·XRD 관측까지 붙는다** = 우리 산물 목록이 실험과 연결되는 첫 지점. 🔑 **`Fig. 5a` LPSCl\|LCO ↔ 우리 −0.3227 eV/atom** (정본 [Xiao19] SI −339; 세대차 16 meV). 🔑 **`Fig. 7`: 조성 레버 5개 중 공유결합 혼성(P–O·B–O)만 σ·환원·산화 3축 동시 개선** = 우리 O/B 축의 문헌 자리. 🔑 **Table 1: 란타나이드 = O·S 화학에서 Li-안정** = Nd 도핑 계열 근거. ⛔ **아지로다이트 고유 창·Ea·σ 는 0건**(*"다른 황화물과 유사할 것"*) · ⛔ 자체 계산 0 = 방법 파라미터 이식 불가 · 🔴 **Li₃P 역할이 우리 원장과 충돌**(우리 `conductor-LEAK` ↔ 리뷰 *"passivating"*) · ⚠ LLZO 창이 `Fig. 6`↔`Fig. 4d`↔본문 셋 다 다름 · ⚠ 표지 "amendments" 고지의 내용 미확인 | ✅ `papers/xiao2020_interface_stability_ssb_review.md` (2026-09-12, **그림 7장 전부 실독 + `Fig. 5a` 52셀·`Fig. 6` 18점·`Fig. 4d` 5막대 좌표 복원**) |
-->

<!-- ⚠ 계보 카드의 "흐름 한 줄" 도 같이 고쳐야 한다:
     현재: "… 분기(6, 음극 + ML …) · 교과서화(7·8)."
     제안: "… 분기(6, 음극 + ML …) · 교과서화(7 = Mo 그룹 방법서) · **채점(8 = Ceder 그룹이 자기 틀을 실험 문헌에 대고 검증)**."
     그리고 #8 행의 "Cronk 2026(같은 Meng 그룹)과 이어진다" 는 삭제하고,
     대신: "Cronk 2026 두 편과는 *그룹*이 아니라 *전제↔검증* 으로 이어진다 (digest §7f: SSE-redox·탄소 경고·Li₂S 환원)." -->

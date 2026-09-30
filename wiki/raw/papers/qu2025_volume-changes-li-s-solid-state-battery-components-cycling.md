---
title: "Qu et al. 2025 — Deciphering volume changes in Li-S solid-state battery components during cycling: Implication for advanced battery design (Nano Energy 138, 110887)"
description: "정압(스프링+LVDT)·정용적(나사+압력변환기) 자작 fixture 로 전고체 Li–S 셀의 수직 변위와 스택 압력을 실시간 측정해 S·Li2S 양극, LixIn 음극, LPSCl 의 부피 기여를 분리한 측정 논문 — 운전 7 MPa, 첫 몇 사이클에 14–20 µm 수축, Li2S 첫 충전 한 번에 절반"
source_url: local-upload/08d276a4-deciphering_volume_changes_in_ASSLSB_components_during_cycling.pdf (SI 미확보)
doi: 10.1016/j.nanoen.2025.110887
ingested: 2026-09-30
sha256: 8513ad8e256c52ed42ee6a9fd4bed27e8708397c638f896dab51357e3336de9d
tags: [assb, sulfide-electrolyte, li2s, composite-cathode, li-in, mixing-process]
compare:
  system: "ASSB Li–S (sulfide) — 성능 논문이 아니라 부피 변화·스택 압력 측정 논문. 운전 스택 압력 7 MPa 정압 vs 정용적(초기 7 MPa) 비교"
  electrolyte: "Li6PS5Cl (LPSCl, NEI Corporation). 건식 필름 = LPSCl + PTFE 0.5 wt%, heat grinding + rolling → 100 µm, 7/16 in 지름으로 300 MPa 3 min 성형 (사이클 전 단면 SEM 83.2 µm). full cell 은 분말 0.1 g 을 500 MPa 펠릿"
  cathode: "Li2S 또는 S : Super C65 : LPSCl = 2 : 1 : 3 (질량) = 33.3 : 16.7 : 50.0 wt%, 바인더 언급 없음. SE 필름 위에 300 MPa 3 min 압착 (사이클 전 단면 SEM 80.5 µm)"
  li2s_source: "상용 Li2S 99.98 % (Sigma-Aldrich) — 입도·전처리 미기재"
  mixing: "one-step — Li2S(또는 S) + Super C65 + LPSCl 을 한 번에 ZrO2 용기, Fritsch Planetary Micro Mill PULVERISETTE 7, 300 rpm, 4 h. 볼 재질·직경·개수·BPR·총 투입량·분위기 미기재. 성형 압력 300 MPa 3 min (양극/SE), 500 MPa (SE 펠릿), 50 MPa 20 s (Li–In)"
  loading_mg_cm2: "미기재"
  li2s_wt_pct: 33.3
  anode: "Li–In (In 박 0.127 mm 99.99 % + Li 박, Li:In 몰비 1.3, 50 MPa 20 s, 3/8 in) · 부피 분리용 대극은 LTO 필름 (LTO : Super C65 : LPSCl = 6:1:3 + PTFE 0.75 wt%, 100 µm, 5/16 in, 0.7 V vs Li–In 까지 전리튬화). 집전체는 스테인리스 로드"
  first_charge: "본문에 컷오프 수치 없음. Li2S 셀 첫 충전은 [도표, Fig. 3c] 0.85 → 2.4 V vs LTO 대극, 약 11 h. full cell 은 formation 3 사이클 0.05 C 후 0.1 C"
  first_discharge_mAh_gS: "해당 없음 — 측정 논문 (절대 용량 미보고)"
  first_discharge_mAh_gLi2S: "해당 없음 — 측정 논문 (절대 용량 미보고)"
  cycle_capacity_mAh_gS: "해당 없음 — 측정 논문 (Fig. 8a 의 y축은 유지율 %)"
  cycle_capacity_mAh_gLi2S: "해당 없음 — 측정 논문 (Fig. 8a 의 y축은 유지율 %)"
  areal_mAh_cm2: "해당 없음 — 측정 논문 (로딩 미기재)"
  cycles: "100 — [도표, Fig. 8a] 유지율 정압 7 MPa ≈63 % · 정용적 ≈50 % (10·20·30·40·50·60 사이클마다 7 MPa 재압축). CE 는 양쪽 모두 ≈100 %"
  temperature_C: 60
  mechanism: "정압 LVDT 변위 + 정용적 압력변환기 + LTO zero-strain 대극으로 성분 분리. [도표] 총 변위: LTO 대조셀 −2 µm / S 양극 −15 µm / Li2S 양극 −19 µm / LixIn 음극 −42 µm; 압력 강하 −0.12 / −0.41 / −0.60 / −1.4 MPa. 사이클 후 단면 SEM 두께: 정압 양극 −9.4 % SE −12.4 %, 정용적 양극 +9.4 % SE −10.9 %. EIS Ohmic 40 → 60 Ω(정용적, +50 %), 재압축하면 오히려 65 Ω. DRT τ≈1 s 어깨가 정용적에서 소멸. 결론 — 균열은 비가역, 공극은 스택 압력으로 가역. 상 동정(EDS·XRD·라만) 없음"
  our_axis: "★ 조성이 우리와 거의 같다 (SE 50 wt% 동일, 활물질 33.3 vs 30). fixture 설계 수치·성형 압력 세트·LTO 대극 성분분리법·'압력은 절대값보다 유지' 명제가 이식 가능. 절대 용량·로딩·anode-free 구성·집전체 데이터는 없음"
---

# 수집 목적

E. Lee, J. Han, J. Jeong, H. Choi, E. Seo, T. J. Shin, K. Y. Chung,
**"Decoupled sulfur redox pathways governed by initial chemical states in all-solid-state
lithium–sulfur batteries"**, *Chemical Engineering Journal* **546** (2026) 179625,
DOI 10.1016/j.cej.2026.179625 (open access, CC BY-NC) 의 **절별 해체분석**.

이 논문을 흡수하는 이유는 하나로 줄일 수 있다. **양극 조성이 우리 reference cell 과 같다.**
이 논문의 복합양극은 활물질 : MWCNT : LPSCl = **3 : 2 : 5 (= 30 : 20 : 50 wt%)** 이고,
우리 1단계는 Li2S : LPSCl : AB = **30 : 50 : 20 wt%** 다 — **같은 30 wt% 활물질 · 50 wt% LPSCl ·
20 wt% 탄소**. 음극도 Li–In, SE 도 LPSCl, 온도도 상온이다. 다른 것은 (i) 탄소가 AB 가 아니라
MWCNT, (ii) 혼합이 **two-step planetary**, (iii) Li2S 를 **cryo-milling** 으로 전처리,
(iv) 충전 컷오프가 **3.0 V vs Li–In (= 3.62 V vs Li/Li⁺)** 로 매우 높다, (v) 운전 중 **외부
스택압을 걸지 않는다** 는 것이다.

그 위에 이 논문이 던지는 명제가 우리 열린 질문의 정면을 친다:

> **"pristine Li2S 로 출발해도, LPSCl 과 볼밀하고 나면 양극은 더 이상 pristine Li2S 가 아니다."**
> 저자들은 혼합 중 Li2S 와 LPSCl 이 반응해 **S–S 결합을 가진 단쇄 황종(S2–4)** 이 생기고,
> 그것이 첫 사이클 거동과 이후 산화환원 경로 전체를 지배한다고 주장한다.

즉 [[reference-cell-500-600-mahg]] 의 H1(활성화 제한)·H3(입자 제한) 옆에 **"혼합 중 계면
화학 변화"** 라는 축을 하나 더 놓아야 하는지가 이 digest 의 핵심 질문이다. 동시에
[[one-step-vs-two-step-mixing]] 의 H2(SE 가 고에너지 단계에 있으면 손상된다)에 대해 이 논문은
**200 rpm 1 h 의 온건한 2단계 혼합에서도 활물질–SE 반응이 일어난다**는 방향의 근거를 준다.

**표기 규칙** (이 위키 관례 4구분):
- `[인쇄]` — 논문 본문/식/표에 글자로 있는 것
- `[도표]` — 그림에서 눈으로 읽은 근사값 (**원 데이터가 아니다**)
- `[해석]` — 이 문서를 쓰면서 붙인 판단. **논문의 주장이 아니다**
- `[재현]` — 원문 값을 이 세션에서 산술로 옮긴 것 (계산식을 함께 적는다)

**단위 변환 상수** (이 digest 전체에서 사용):
- mAh g⁻¹(Li2S) → mAh g⁻¹(S): **× 1.4329** (M(Li2S)/M(S) = 45.947/32.066)
- mAh g⁻¹(S) → mAh g⁻¹(Li2S): **× 0.6979**
- 활물질 기준 → 복합체 기준: **× 0.30** (활물질이 복합양극의 30 wt%)
- 전압: **V vs Li/Li⁺ = V vs Li–In + 0.62** (`[인쇄, §2.1.3]` "0 V vs. Li–In/Li⁺ corresponds to
  ~0.6 V vs. Li/Li⁺", 근거로 Santhosha et al. 의 Li–In 상태도 refs 46,47 를 인용)

- 원본 파일: 로컬 업로드 PDF 11쪽 (본문 10쪽 + 참고문헌). **SI(Fig. S1–S20)는 받지 못했다.**
- 크로핑 그림: `raw/figures/lee2026_decoupled-sulfur-redox-pathways-initial-chemical-states-assb/`
  — 본문 Fig. 1–6, 여섯 장 전부 (§16 에서 전부 직접 판독했다).
- 페이지 참조는 **저널 조판 페이지 = PDF 페이지** (1–11).

---

# 원문에 없어서 확인이 필요한 것 (읽기 전에 먼저 본다)

이 절이 이 digest 의 가장 중요한 산출물이다. G2·G3·G4 는 단순한 공백이 아니라 **논문의 중심
숫자를 흔드는 공백**이다.

| # | 공백 | 왜 문제인가 |
|---|---|---|
| G1 | **SI 를 확보하지 못했다.** 본문이 인용하는 Fig. **S1–S20** (셀 모식도 S1·S2, LPSCl XRD/EIS S3, cryo-mill 후 XRD·SEM S4, EDS 맵 S5, Li–In XRD S6, 0.1 C 곡선 S7, 사이클 후 SEM S8, 광학현미경 S9, EIS S10, 50사이클 CV S11, 고로딩 S12, scan-rate CV S13, EIS S14, charge-first S15, sweep 순서 CV S16, ex situ XRD S17·S18, Cl 2p XPS S19, XANES 2472 eV S20) 는 **본문 서술로만** 옮겼다. | 이 digest 에서 `Fig. S…` 로 인용한 값은 **전부 본문 문장에서 온 `[인쇄]`** 이고, 그림을 본 적이 없다. SI 확보 시 재검증 대상 (§16 표). |
| G2 | **★ Li2S 셀의 용량이 Li2S 이론용량(1167 mAh g⁻¹)을 넘는다.** `[인쇄]` 2nd 방전 **1181**, 1st 충전 **1233.3**, 3rd(0.1 C) **1250** — 각각 이론의 101.2 / 105.7 / **107.1 %** `[재현]`. | 황 원자가 보존되면 칭량한 Li2S 1 g 이 낼 수 있는 최대는 2 F × (32.066/45.947)/32.066 = **1167 mAh** 다. 초기 상태가 어떻게 산화돼 있든 이 상한은 안 바뀐다. 논문은 1233 하나만 언급하며 "잔류 Li2S + 방전 중 새로 생긴 Li2S" 로 설명하는데, 그 설명은 **황 보존을 깨지 않는 설명이 아니다.** 초과분의 출처(LPSCl 산화, MWCNT, SE 로부터의 황 이동)를 분리하지 않았다. `[해석]` 이 digest 의 모든 Li2S 셀 용량은 **"비-황 용량이 섞여 있을 수 있는 값"** 으로 읽어야 한다. |
| G3 | **★ 충전 컷오프 3.0 V vs Li–In = `[재현]` 3.62 V vs Li/Li⁺** 에서 LPSCl 산화 분해의 기여를 분리하지 않았다. 근거는 두 가지뿐 — in situ XRD 의 LPSCl (311) 피크 불변(Fig. 2c,f)과 Cl 2p 에 LiCl 부재(Fig. S19). | 황화물 SE 의 산화 분해 생성물(S, P2Sx)은 **비정질**이라 XRD 에 안 보이고, LiCl 이 아닌 경로로도 분해된다. LPSCl 단독(활물질 없는) 셀의 전류–전압 대조가 없다. G2 의 초과 용량과 같은 방향을 가리킨다. |
| G4 | **"초기 화학 상태" 의 정량이 오직 첫 방전 용량 한 개에서 나온다.** `[인쇄, p.9]` 502.5 / 1672 = 30 % → "oxidized sulfur species 30–35 wt%". | XPS·XAS 로 독립 정량하지 않았다. 게다가 이 계산은 복합양극 활물질의 30 wt% 를 **"Sn"(단체 황 질량)** 으로 잡는데, 그러면 칭량 1 g 당 황 함량이 0.698 g → **0.789 g** 으로 늘어난다 (§11.2). 즉 정량 논증 자체가 **황을 어디선가 빌려온다**. 빌린 곳이 LPSCl 이라면 용량의 분모가 무너진다. |
| G5 | **셀 개수·오차막대가 하나도 없다.** 모든 그림이 단일 곡선이다. | 250 사이클 열화 시점(S8 46사이클 급락, Li2S 34사이클)이 계통인지 셀 하나의 사고인지 모른다. |
| G6 | **"unpressurized" 의 정량값이 없다.** `[인쇄, §2.3]` "without applying external pressure" 이지만 셀은 **2032 코인셀**이고, 코인셀의 스프링·스페이서는 수 MPa 를 가한다. 스페이서 구성·스프링 사양 미기재. | 이 논문의 셀링 포인트가 "무가압" 인데 그 무가압의 실제 값이 없다. 우리 셀(가압 지그)과의 비교가 정성으로만 가능하다. |
| G7 | **온도가 "room temperature" 로만** 적혀 있다. 숫자 없음 (LPSCl 소성 온도만 25 → 550 °C 로 기재). | 상온 ASSLSB 는 수 °C 차이로 동역학이 바뀐다. |
| G8 | **고로딩 시험을 S8 셀에만 했다** (1.4, 2.3 mg cm⁻²(S), 조성 4:1:5). Li2S 셀은 **~1.0 mg cm⁻² 하나뿐**. | 결론의 "Li2S 양극이 스택압 의존을 줄일 수 있다" 가 **로딩 1.0 mg cm⁻² 에서만** 검증됐다. S8 고로딩 셀은 10 사이클 만에 ≈0 이 된다 (§7.3). |
| G9 | **conventional LSB 의 컷오프가 본문과 그림에서 다르다.** `[인쇄, §2.3]` "cut-off voltages were set to 0.1–3.0 V" 인데 `[도표, Fig. 1a]` 액체셀 곡선은 **1.5–3.0 V vs Li/Li⁺** 다. | §2.3 의 0.1–3.0 V 는 ASSLSB(vs Li–In)에만 해당하는 값으로 보인다. 컷오프를 인용할 때 셀마다 나눠 적어야 한다. |
| G10 | **볼밀의 기계적 조건 일부가 없다.** 있는 것: 장비(Fritsch P7), rpm(250 / 200), 시간(6.5 h / 1 h), run–pause(30/10 min), 분위기(Ar). 없는 것: **볼 재질·직경·개수, BPR, 자(jar) 재질·부피, 충전율**. | 우리 [[composite-cathode-mixing-routes]]·[[mixing-equipment-ball-mill-thinky]] 가 요구하는 열의 절반이 빈다. rpm·시간만으로는 투입 에너지가 정해지지 않는다. |
| G11 | **혼합 중 Li2S–LPSCl 반응이 어느 단계에서 생기는지 구분하지 않았다.** 1단계(활물질+MWCNT, 250 rpm 6.5 h)인지 2단계(+LPSCl, 200 rpm 1 h)인지, 시간 의존성이 어떤지 조사 없음. | LPSCl 은 2단계에만 들어가므로 반응은 2단계(또는 그 후 보관 중)여야 하는데 **강도·시간을 바꾼 대조군이 없다.** 우리가 "그 반응을 피할 수 있는가" 를 물으면 답이 없다. |
| G12 | **S2–4 의 정체가 확정되지 않았다.** `[인쇄, §3.6]` "although their exact chemical identity cannot be unambiguously determined". Raman·NMR·적정 없음. | 논문 제목이 "initial chemical states" 인데 그 state 의 화학식이 미확정이다. S 2p ~163 eV 와 XANES ~2472 eV 두 특징에만 의존한다. |
| G13 | **XAS 검출 모드(TEY / TFY / 전도전자)를 적지 않았다.** `[인쇄, §2.4]` 빔라인(TLS 16A1 tender X-ray)만 있다. | XPS(표면 수 nm)에서는 S–S 성분이 **크고**(Fig. 4c 초기 상태), XANES 초기 스펙트럼은 pristine Li2S 와 **거의 겹친다**(Fig. 5b). 두 관측의 차이가 "표면 대 벌크" 인지 "정량 대 정성" 인지 가를 수 없다 → 30–35 wt% 라는 **벌크 분율** 주장이 흔들린다. |
| G14 | **S8 셀의 첫 충전 용량을 글자로 적지 않았다.** | `[재현+도표, Fig. 6a]` 시간축에서 충전 구간 ≈16 h × 0.05 C × 1672 = **≈1340 mAh g⁻¹(S)**. 첫 방전 1084 보다 크다 — 이것이 "혼합 중 생긴 Li2S 가 첫 충전에 활성화된다" 의 직접 숫자인데 본문에 없다. |
| G15 | **Li2S 셀의 첫 사이클 CE 를 적지 않았다.** | `[재현]` 방전선행: Q_dis/Q_ch = 502.5/1233.3 = **40.7 %**. 충전선행: 1095.9/672.3 = **163 %**. 둘 다 통상적 CE 정의로는 뜻이 없고, 이 셀에서 "CE ≈100 %" 는 **3사이클째부터**의 이야기다. |
| G16 | **Li 금속 음극 셀이 "prematurely terminated due to instability"** 라고만 하고 (§3.5), 무엇이 어떻게 끝났는지(단락? 전압 폭주? 몇 시간?) 적지 않았다. | Li2S/Li 셀의 in situ XRD(Fig. 3d–f) 해석이 그 위에 얹혀 있다. |
| G17 | **cryo-milling 후 입도 분포가 숫자로 없다.** `[인쇄]` "particle sizes on the order of several micrometers" (Fig. S4c,d — 미확보). D50 없음. | 우리 H3(입자 제한)에 대응시킬 수가 없다. |
| G18 | **사이클 후 양극의 화학 분석이 없다.** XPS·XAS 는 전부 **1사이클 상태**(initial / discharged / charged)뿐. 250 사이클 열화의 화학적 정체는 EIS·SEM·OM(전부 SI)만으로 "chemo-mechanical" 이라고 귀속된다. | 열화 기전 주장이 **형태학 + 임피던스**에 의존한다. 화학적 열화(SE 분해 축적)를 배제하지 못한다 — G3 과 맞물린다. |
| G19 | **MWCNT 의 제조사·직경·길이·비표면적 미기재.** | 탄소 차원·네트워크 논의([[carbon-dimensionality-electron-network]])로 옮길 때 "MWCNT 20 wt%" 이상은 말할 수 없다. |

---

## 0. 서지사항 (직접 확인)

| 항목 | 값 | 확인 위치 |
|---|---|---|
| 제목 | Decoupled sulfur redox pathways governed by initial chemical states in all-solid-state lithium–sulfur batteries | p.1 표제 |
| 저자 | Eunbyoul Lee ᵃᵇ¹, Jonghyun Han ᵃ¹, Jiwon Jeong ᵃᶜ, Hamin Choi ᵈ, Eunchae Seo ᵃᵉ, Tae Joo Shin ᶠ, **Kyung Yoon Chung** ᵇᵈ (교신, kychung@kist.re.kr). ¹ Lee·Han 동등기여 | p.1 |
| 소속 | a KIST Energy Storage Research Center · b UST KIST School · c 고려대 신소재 · d KIST Sustainable Energy · e 연세대 화공생명 · f UNIST 반도체소재부품대학원 | p.1 |
| **저널** | **Chemical Engineering Journal**, vol. **546** (2026) 179625 | p.1 꼬리글 "Chemical Engineering Journal 546 (2026) 179625" + 머리글 "Contents lists available at ScienceDirect / journal homepage: www.elsevier.com/locate/cej" |
| **DOI** | **10.1016/j.cej.2026.179625** | p.1 꼬리글 "https://doi.org/10.1016/j.cej.2026.179625" |
| 날짜 | Received 10 May 2026 · Revised 6 July 2026 · Accepted 16 July 2026 · Available online 17 July 2026 | p.1 꼬리글 |
| 라이선스 | © 2026 The Authors, Elsevier B.V., **CC BY-NC** | p.1 꼬리글 |
| 지원 | NRF RS-2024-00404414 · NST GTL24013-000 · KIST 2E33940 · 빔타임 PLS-II 6D/9A (POSTECH·UNIST UCRF) | p.10 |
| 키워드 | All-solid-state lithium-sulfur batteries · Sulfur redox pathways · Lithium sulfide · Short-chain sulfur species · Solid-state electrolyte | p.1 |
| 데이터 | "Data will be made available on request" | p.10 |

---

## 1. 한 문단 요약

같은 셀 구조(LPSCl 펠릿 | 복합양극 3:2:5 | Li–In, 2032 코인셀, 상온, 무가압)에서 **출발 활물질만
S8 ↔ Li2S 로 바꾸면 황의 산화환원 경로가 서로 다른 두 갈래로 갈린다**는 것이 이 논문의 주장이다.
S8 셀은 방전에서 LiPS 를 거쳐 Li2S 까지 가지만 **충전에서 결정질 S8 이 재생성되지 않고**
장쇄 LiPS 에서 멈춘다 — 그래서 2사이클 방전이 `[인쇄]` **1443 mAh g⁻¹(S)** 까지 올라가지만
부피변화로 양극에 균열·박리가 생겨 46 사이클 뒤 급락하고 250 사이클에 **409 mAh g⁻¹(S)** 가
된다. Li2S 셀은 **결정질 S8 도 장쇄 LiPS 도 만들지 않고** 단쇄 황종 S2–4 ↔ Li2S 사이만
오가며, 첫 방전은 `[인쇄]` **502.5 mAh g⁻¹(Li2S)** 로 낮지만 2사이클에 **1181**, 0.1 C 에서
**1250** 까지 오르고 250 사이클에 **653 mAh g⁻¹(Li2S)** 를 남긴다 (CE 는 두 셀 다 ≈100 %).
핵심 관측은 **"Li2S 복합양극의 초기 상태가 pristine Li2S 가 아니다"** — 혼합 중 Li2S 와 LPSCl 이
반응해 S–S 결합종(S2–4 로 추정)이 30–35 wt% 생겼고(첫 방전 용량으로 역산), 그것이 첫 방전의
용량원이자 이후 가역 경로의 한쪽 끝이라는 것이다. 근거는 **in situ 방사광 XRD(PLS-II 6D/9A) +
ex situ XRD + S 2p XPS + S K-edge XANES(TLS 16A1)** 의 조합이고, 모두 **1사이클 수준**의
관측이다. 단, `[해석]` **Li2S 셀의 보고 용량이 Li2S 이론용량을 최대 7 % 넘고**(G2), 충전
컷오프가 3.62 V vs Li/Li⁺ 로 LPSCl 산화 영역 깊숙이 들어가 있으며(G3), 30–35 wt% 정량이
질량수지를 맞추지 않는다(G4) — **경로가 갈린다는 정성 주장은 튼튼하지만 숫자는 그대로
인용하면 안 된다.**

---

## 2. 서론이 세운 문제 틀 (p.1–2)

`[인쇄]` 저자들이 명시적으로 겨냥하는 관행은 하나다 — **"ASSLSB 연구가 액체계에서 확립된
S8–Li2S 전환 기전을 그대로 가져다 쓴다"**:

- "their practical implementation is hindered by the limited understanding of sulfur redox
  reactions in solid-state environments, **which are often assumed to follow the conventional
  S8–Li2S conversion mechanism established in liquid electrolytes**" (초록)
- "previous studies on ASSLSBs have primarily focused on improving electrochemical performance
  by **adopting redox mechanisms of S8 established in liquid electrolytes**" (p.2)
- 기존 처방(redox mediator, catalytic additive, conductive carbon framework)은 "often rely on
  **elevated temperature and/or external pressure**" 이고 비활성 성분을 넣어 에너지밀도를
  깎는다 (p.2, refs 33–38).

`[인쇄]` 숫자로 인용된 재료 상수:
- S8 이론용량 **1672 mAh g⁻¹**, 밀도 2.07 g cm⁻³
- Li2S 이론용량 **1167 mAh g⁻¹**, 밀도 1.66 g cm⁻³
- Li 금속 3860 mAh g⁻¹, 0.59 g cm⁻³

`[인쇄]` Li2S 를 다루는 문단이 우리 문제를 정확히 적는다: "Li2S suffers from **high
electrochemical activation barriers, requiring a large initial overpotential that can induce
electrolyte decomposition and destabilize the internal battery environment**" (p.2, refs 29,40).
그리고 Li2S 가 이미 Li 을 갖고 있어 **Li-free 음극 ASSLSB** 를 가능케 한다고 적는다
(refs 28,39,40) → [[anode-free-li2s-assb]]. 최근 Li2S 계 처방으로는 "interfacial redox mediators,
controlled Li2S deposition, **stabilization of short-chain sulfur species**" 를 든다 (refs 38,41–43).

`[해석]` 서론이 스스로 "큰 초기 과전압이 전해질 분해를 일으킨다" 고 써 놓고, 본인들의 컷오프를
3.62 V vs Li/Li⁺ 로 잡은 뒤 그 분해를 정량하지 않는다 (G3). 이 긴장이 논문 전체를 관통한다.

논문이 내세우는 기여 두 줄 `[인쇄]`:
> (i) the redox pathway of S8 in ASSLSBs **deviates from the conventional S8–Li2S conversion
> reaction**; (ii) Li2S undergoes a **distinct reversible conversion involving short-chain sulfur
> species (S2–4)**.

---

## 3. 재료·합성·혼합 — 있는 것을 전부 옮긴다 (§2.1, p.2–3) ★★

### 3.1 LPSCl 고체전해질 (§2.1.1)

| 항목 | `[인쇄]` |
|---|---|
| 출발물 | Li2S (Sigma 99.98 %), LiCl (Sigma ≥99 %), P2S5 (Sigma 99 %) |
| 몰비 | **5 : 2 : 1** (→ Li6PS5Cl) |
| 밀 | **Fritsch Pulverisette 5 planetary**, ZrO2 볼 **직경 10 mm** |
| 조건 | **450 rpm, 60 h** (20 min run / 40 min pause) |
| 소성 | 석영관, 25 °C → **550 °C, 2 °C min⁻¹, 550 °C 5 h**, 자연 냉각 |
| 후처리 | 유발 분쇄 + **125 µm 이하 체거름** |
| 분위기 | 전 공정 Ar |
| 결과 | `[인쇄]` 참조 패턴과 일치하는 결정구조 + 이온전도도 **5.3 × 10⁻³ S cm⁻¹** (Fig. S3a,b — 미확보) |
| 출처 | Wang et al. (ref 14) 의 방법 |

`[해석]` 볼 개수·BPR 미기재(G10). 5.3 mS cm⁻¹ 는 Li6PS5Cl 로서 상단값이다 (측정 온도·가압 미기재).

### 3.2 활물질 전처리 — cryo-milling (§2.1.2) ★

| 항목 | `[인쇄]` |
|---|---|
| 대상 | S8 (Sigma **99.998 %**) 또는 **Li2S (Sigma 99.98 %)** — 둘 다 상용 분말 |
| 장비 | **Retsch CryoMill, −196 °C** |
| 순서 | **5 Hz 5 min → 30 Hz 30 min** |
| 목적 | `[인쇄]` "to obtain uniform particle size distribution" |
| 결과 | `[인쇄]` cryo-mill 후 XRD 로 S8·Li2S 결정구조 확인 (Fig. S4a,b); SEM 상 **둘 다 수 µm**, 단 **S8 이 Li2S 보다 응집이 심하다** (Fig. S4c,d) |
| 이유 | `[인쇄]` "soft molecular nature of S8 promotes **cold welding**, whereas **ionically bonded Li2S undergoes brittle fracture**" (refs 53,54) |

`[해석]` ★ 우리에게 바로 쓸 수 있는 정보다: **Li2S 는 취성 파괴라 밀링으로 잘 깨지고, S8 은
냉간 용접으로 뭉친다.** 그래서 Li2S 계에서는 cryo 가 필수가 아닐 수 있고(상온 밀링으로도
깨진다), 오히려 **새로 생긴 깨끗한 표면이 LPSCl 과 반응할 기회**가 된다 (§10.3 의 S–S 종).

### 3.3 복합양극 혼합 — **two-step** (§2.1.2) ★★

`[인쇄]` "Based on previously reported methods by Gröbmeyer et al. [7] and Wang et al. [14],
the composite cathodes were prepared using **solid-state ball milling**." **S8 양극과 Li2S 양극은
완전히 같은 절차**로 만들었다.

| 단계 | 내용 | 장비·조건 `[인쇄]` |
|---|---|---|
| **1단계** | 활물질(S8 또는 Li2S) + **MWCNT**, 질량비 **3 : 2** | Fritsch **Pulverisette 7** planetary, **250 rpm, 6.5 h** (30 min run / 10 min pause), Ar |
| **2단계** | 1단계 혼합물 + **LPSCl**, 질량비 **1 : 1** | 같은 밀, **200 rpm, 1 h**, Ar |
| 최종 | 활물질 : MWCNT : LPSCl = **3 : 2 : 5** (= 30 : 20 : 50 wt%) | — |
| 고로딩용 | S8 : MWCNT : LPSCl = **4 : 1 : 5** (= 40 : 10 : 50 wt%) | §2.3 에만 언급, 밀링 조건 별도 기재 없음 |
| 확인 | `[인쇄]` EDS 맵에서 S 및 기타 원소가 균일 (Fig. S5) — "active materials were well mixed with MWCNTs and LPSCl" | — |

`[해석]` ★ **[[one-step-vs-two-step-mixing]] 의 two-step 경로의 교과서적 사례**다 —
(활물질+탄소) 고에너지 먼저, (+SE) 저에너지 나중. 그런데 이 논문의 중심 발견이 하필
**"그 2단계에서 Li2S 와 LPSCl 이 화학반응했다"** 는 것이다. 즉 **SE 를 나중에, 약하게 넣어도
(200 rpm 1 h) 활물질–SE 반응은 일어난다.** 그 카드의 H2("SE 를 고에너지 단계에서 빼면 보호된다")
에 대한 **부분 반대 근거**다. 다만 one-step 대조군이 없으므로 **순서 비교는 못 한다**(G11).

### 3.4 Li–In 음극 (§2.1.3)

| 항목 | `[인쇄]` |
|---|---|
| 출발물 | Li (FMC, 98 %) + In (Sigma, 99.99 %) 분말 |
| 비율 | **질량 1 : 32** (≈ 몰 1 : 2, **≈34 at.% Li**) |
| 혼합 | **Thinky NBK-1 planetary mixer, 2000 rpm, 30 s** |
| 분위기 | Ar 글러브박스, H2O < 0.1 ppm, O2 < 0.1 ppm |
| 근거 | `[인쇄]` Santhosha et al. 의 Li–In 상태도(refs 46,47) — 이 조성은 **LiIn/In 이상(二相) 영역**이며 **0.62 V vs Li/Li⁺ 의 안정한 산화환원 전위**를 준다. "0 V vs Li–In/Li⁺ ≈ 0.6 V vs Li/Li⁺" |
| 확인 | `[인쇄]` Li–In 과 In 상의 공존을 XRD 로 확인 (Fig. S6) |
| 채택 이유 | `[인쇄]` Li 금속보다 LPSCl 에 대한 구조적·기계적 안정성이 좋다 (refs 44–46). 일부 실험은 Li 금속도 사용 |

`[해석]` ★ 우리 위키가 "근거 raw 가 없어 인용 금지" 로 묶어둔 **Li–In ≈ +0.62 V vs Li/Li⁺** 에
대해 (2차 인용이지만) 출처와 함께 명시한 첫 digest 다 → [[capacity-normalization-li2s-vs-sulfur]]
옆의 전압 기준 항목에 보탤 것. 단 **이 논문이 측정한 값이 아니다**(refs 46,47 인용).
간접 검증은 있다: `[도표]` 같은 S8 양극이 Li–In 셀에서 방전 plateau ≈1.2 V vs Li–In(Fig. 1d),
Li 금속 셀에서 ≈1.85 V vs Li/Li⁺(Fig. 3a) → 차이 **≈0.65 V** 로 0.62 와 맞는다 `[재현]`.

---

## 4. 셀 조립·운전 조건 (§2.1.4, §2.3) ★★

### 4.1 ASSLSB 셀 구성

| 항목 | `[인쇄]` | `[재현]` |
|---|---|---|
| 셀 | **2032 코인셀**, 3층 펠릿 | — |
| 지름 | **15 mm** | 면적 **1.767 cm²** |
| SE 층 | LPSCl **150 mg**, **4 ton** 가압 | **≈222 MPa** (4 × 9806.65 N ÷ 1.767 cm²) |
| 양극 층 | 복합양극 분말 **6 mg** 을 SE 층 위에, **4 ton** | 복합체 로딩 **3.40 mg cm⁻²**, 활물질 **1.02 mg cm⁻²** (`[인쇄]` "~1.0 mg cm⁻²" 와 일치) |
| 음극 층 | Li–In 분말 **70 mg**, 펠릿을 뒤집어서 **2 ton** | **≈111 MPa** |
| 총 두께 | **≈700 µm** | — |
| 성형 | 전 공정 Ar 글러브박스, **상온 냉간 가압** | — |
| 운전 압력 | `[인쇄]` "**without applying external pressure**" | 코인셀 스프링 압력 미기재 (G6) |

### 4.2 전기화학 프로토콜

| 항목 | `[인쇄]` | `[재현]` / 주의 |
|---|---|---|
| 컷오프 | **0.1 – 3.0 V** (ASSLSB, vs Li–In) | = **0.72 – 3.62 V vs Li/Li⁺** |
| 액체셀 컷오프 | §2.3 은 같은 0.1–3.0 V 로 적었으나 `[도표, Fig. 1a]` 는 **1.5–3.0 V vs Li/Li⁺** (G9) | — |
| 화성 | **0.05 C 2 사이클**, 이후 **0.1 C** | — |
| 방전 | 정전류(CC)로 하한 0.1 V 까지 | — |
| 충전 | **CC–CV**: 3.0 V 도달 후 **전류가 초기값의 50 % 로 떨어질 때까지 정전압** | `[해석]` 충전 용량에 **CV tail 이 포함**된다 — 첫 충전량을 "활성화량" 으로 읽을 때 주의 |
| 1 C 정의 | 이론용량 × 로딩. S8 계 **1672**, Li2S 계 **1167 mAh g⁻¹** | 분모가 **활물질 질량**임이 여기서 확정된다 |
| 1 C 전류밀도 | 액체셀 **2.8**, S8-ASSLSB **1.7**, Li2S-ASSLSB **1.2 mA cm⁻²** | `[재현]` 1.019 × 1672 = 1.70 / 1.019 × 1167 = 1.19 ✓ |
| 실제 전류 | — | `[재현]` Li2S 셀 0.05 C = **0.059 mA cm⁻²**, 0.1 C = **0.119 mA cm⁻²** (매우 낮다) |
| CV | **50 µV s⁻¹** (Fig. 1f,i) | — |
| 동역학 CV | 0.05 mV s⁻¹ 2사이클 화성 후 **0.05 / 0.1 / 0.2 / 0.5 / 1 mV s⁻¹**, 각 측정 후 EIS | — |
| 로딩(활물질) | 액체셀 **~1.7**, ASSLSB **~1.0 mg cm⁻²** | 고로딩 S8 셀: 6 mg → **1.4**, 10 mg → **2.3 mg cm⁻²(S)** (`[재현]` 6 × 0.4 ÷ 1.767 = 1.36 ✓) |
| 온도 | 상온, 숫자 없음 (G7) | — |
| 장비 | Maccor 4000 (충방전), BioLogic VMP3 (CV), Solartron SI 1287/1260 (EIS) | — |

### 4.3 비교용 액체셀 (conventional LSB, §2.2)

`[인쇄]` S8 : MWCNT : PVdF = **6 : 3 : 1**. S8+MWCNT 를 **250 rpm 6.5 h**(Fritsch P7, Ar) 볼밀 →
NMP 에 푼 **5 wt% PVdF** 추가 → **200 rpm 2.5 h** 재볼밀 → Al 박(15 µm) 위에 **습윤두께 150 µm,
20 mm s⁻¹** 캐스팅(Hohsen) → 드라이룸 예비건조 → **50 °C 진공 하룻밤** → **초기 두께의 30 % 로
압연** → **12 mm** 펀칭. 음극 Li 박 14 mm, 분리막 PE 16 mm, 전해질 **1 M LiTFSI in DME:DOL = 1:1 (v/v)**
(`[해석]` **LiNO3 없음**). 2032 코인셀, 드라이룸 조립.

`[해석]` 액체셀에 LiNO3 가 없어 CE 가 80 % 이하로 낮다(§6.1). 이 액체셀은 **최적화된 Li–S 셀이
아니라 "셔틀이 살아 있는 기준선"** 으로 읽어야 한다. [[li2s-activation-first-charge]] 가 기대는
Kim 2023 의 액체셀(LiNO3 0.8 M)과 직접 비교하면 안 된다.

---

## 5. 분석 장비 (§2.4)

| 기법 | `[인쇄]` 세부 |
|---|---|
| **ex situ XRD** | Rigaku R-AXIS IV++, **Mo-Kα (0.7107 Å)** → 식 (1) 로 **Cu-Kα (1.5418 Å) 스케일 환산**해 표시. 양극층을 셀에서 떼어 석영관에 넣고 진공 그리스로 밀봉, 전 과정 Ar |
| **in situ 방사광 XRD** | **PLS-II 6D UNIST-PAL** 및 **9A U-SAXS** 빔라인(포항가속기). 캡에 구멍을 낸 개조 코인셀(Wellcos), 구멍은 **폴리이미드 필름**으로 밀봉 (Fig. S2) |
| **XPS** | PHI 5000 VersaProbe, 단색 **Al-Kα 1486.6 eV**. S 2p 를 **스핀–궤도 이중선**으로 분해: 면적비 **2:1**, 분리 **~1.2 eV** 고정, FWHM 동일 구속 |
| **XAS** | **Taiwan Light Source 16A1** tender X-ray bend-magnet, **S K-edge**. 검출 모드 미기재 (G13) |
| SEM/EDS | FE-SEM Regulus 8230, EDS 10 kV |
| EIS | Solartron SI 1287 + SI 1260 |

`[해석]` 식 (1) 의 파장 환산은 **각도만** 옮긴다 — 강도는 Mo-Kα 조건의 것이다. 상대강도 비교는
같은 측정 안에서만 유효하다.

---

---

## 6. p.4–5 — 결과 ③ Li_xIn 음극 (Fig. 4)

`[인쇄, Fig. 4 캡션]` "The displacement (a) and pressure changes (b) of an **LTO|LPSCl∣Li_xIn**
cell during cycling at **C/20** rate."

`[인쇄, §3]` 셀 배치 주의 — Fig. 3 에서는 LTO 가 **음극**이었지만 Fig. 4 에서는 **LTO 가 양극,
Li_xIn 이 음극**이다. 그래서 "충전/방전" 이 아니라 **산화/환원**으로 불러야 한다. (Fig. 3a 에서
전리튬화 LTO 는 방전 중 **산화**되지만, Fig. 4 에서 LTO 는 방전 중 **환원**된다.)

`[인쇄]` Li_xIn 형성의 기전:
- In 이 **정방정(tetragonal) → 입방정(cubic) Li_xIn** 으로 상전이.
- 이 상전이를 수용하려면 **단위포가 z 방향보다 x–y 면내에서 더 많이 팽창**한다 (이방성).
- 이 이방성 팽창이 **단위포 수준에서 약 100 % 부피 변화**를 만든다.
- 추가로 저자는 **합금화 중 불균일(inhomogeneity)** 을 의심한다 — Li 가 In 전극 전체에
  재분배되는 과정이 사이클 내내 일어날 것이다.
- 면내 비대칭 팽창 + Li 재분배 → **상당한 입자 재배열** → **안정화 전까지 큰 부피 감소**.

`[도표, Fig. 4a]` 전압 **0.8 – 1.6 V** (vs Li–In), 변위 축 **0 ~ −50 µm**, x축 **0–180 h,
≈14 사이클**. 변위는 **0 → 약 −42 µm**. 처음 **60 h(≈5 사이클)에 −35 µm** 가 일어나고 그 뒤는
완만. 데이터가 **점(dot)** 으로 찍혀 있어 Fig. 2·3 의 연속선과 다르다.

`[도표, Fig. 4b]` 압력 축 **0 ~ −1.8 MPa**, x축 **0–210 h, ≈15 사이클**. 압력은
**0 → 약 −1.4 MPa**. 역시 처음 60 h 에 −1.2 MPa 가 집중.

★★ `[해석]` **세 성분 중 Li_xIn 이 압도적으로 크다.**

| 성분 (해당 셀) | 총 변위 `[도표]` | 총 압력 강하 `[도표]` |
|---|---|---|
| LPSCl / LTO 매트릭스 (LTO∣LPSCl∣LTO) | **−2 µm** | **−0.12 MPa** |
| S 양극 (S∣LPSCl∣LTO) | **−15 µm** | **−0.41 MPa** |
| **Li2S 양극** (Li2S∣LPSCl∣LTO) | **−19 µm** | **−0.60 MPa** |
| **Li_xIn 음극** (LTO∣LPSCl∣Li_xIn) | **−42 µm** | **−1.4 MPa** |

`[해석]` 즉 **Li–In 음극이 Li2S 양극보다 2.2배 더 수축한다.** 이 위키의 [[li2s-assb-reference-cell]]
은 1단계에서 **Li–In 을 쓴다** — 그렇다면 **우리 셀에서 첫 사이클 압력 강하의 주범은 양극이
아니라 음극**일 가능성이 크다. 그리고 [[anode-free-li2s-assb]] 로 가면 이 −42 µm 항이 사라지고
**Li 석출/용해의 부피 항**으로 대체된다. 그 교체가 이득인지 손해인지 이 논문은 답하지 않는다
(Li 대칭셀은 Video 1S 로만 언급 — SI 미확보 G18).

`[인쇄, §3]` 중요한 단서: "it's essential to understand that **Li_xIn was never intended to serve
as an anode material in commercial ASSLBs**. Researchers used Li_xIn in an ASSLB cell primarily
due to the instability of the Li/SSE interface."

`[인쇄, §3, Video 1S]` **Li∣SSE∣Li 대칭셀**은 **상보적(reciprocal)** 거동을 보였다 — 한쪽 Li
전극의 부피 증가가 반대쪽의 감소를 상쇄해 **셀 전체의 부피 변화가 무시할 만했다**. 따라서
양극·음극의 부피 변화는 **협조적으로(in a coordinated manner)** 다뤄야 하고, **동기화하면 셀
전체 응력이 줄고**, 어긋나면 SSE 와 계면에 균열·공극이 생긴다. (영상 미확보 — G18)

★ `[해석]` **이것이 이 논문이 주는 설계 원리 중 가장 이식 가능한 것이다**: "양극이 팽창할 때
음극이 수축하도록 짝지어라." Li–S 계는 방전에서 양극이 팽창(+79 %)하고 Li 음극이 소모(수축)되므로
**원리적으로 상보적**이다. Li–In 은 그 상보성을 깬다 — 합금 음극은 방전에서 **탈리튬화되어
수축**하지만 재배열 수축이 그보다 크게 겹친다.

---

## 7. p.5 — 결과 ④ 성분 분해 (Fig. 5) ★ 제목의 "Deciphering" 이 있는 자리

`[인쇄, Fig. 5 캡션]` "Comparison of the displacements of **sulfur cathode (in S8∣LiPSCl∣LTO)**,
**Li_xIn anode (in LTO∣LiPSCl∣Li_xIn)** and **S8∣LiPSCl∣Li_xIn full ASSLB** during the
**1st discharge (a)** and **recharge (b)**, and **2nd discharge (c)** and **recharge (d)**."

### 7.1 저자가 미리 밝힌 한계 `[인쇄, §3]` ★

> "It is important to note that achieving exact reproducibility of the prelithiation for LTO and
> Li_xIn was challenging, and the results presented were based on the data from **three different
> cells**. To facilitate comparison, **all results were normalized to 100 %**, making the
> comparison **more qualitative than quantitative**. For example, **adding the red and blue lines
> might not exactly result in the black curve**, but the trends indicated by the red and blue
> lines combine to produce the black line."

`[해석]` **논문 제목의 동사("Deciphering")가 이 문단 위에 서 있다.** 세 개의 다른 셀에서 잰
곡선을 각각 100 % 로 정규화해 겹친 것이므로, **"양극 몫 3 µm, 음극 몫 11 µm" 같은 수치는 서로
다른 셀의 수치**다. 이 논문의 정량성은 여기서 끝난다 (G7, G9).

### 7.2 본문이 적은 값 `[인쇄, §3]`

**1차 방전** (S 환원):
- 양극 부피 **약 +3 µm 증가**
- Li_xIn 음극 **약 −11 µm 감소**
- 전체 셀 **약 −6 "mm" 감소** ← **단위 오기, µm 여야 함 (G8)**
- `[재현]` +3 + (−11) = **−8 µm** ≠ −6 µm. 차이 **2 µm (25 %)** (G9)

**1차 충전** (S 산화):
- 양극 **약 −4 µm 소폭 감소**
- Li_xIn 음극 **거의 변화 없음** — Li 합금화에 의한 증가가 재배열에 의한 감소로 **상쇄**
- 전체 셀 **거의 변화 없음**

**2차 사이클**: 같은 추세, **변화폭은 더 작다**.

### 7.3 그림에서 읽은 값 `[도표, Fig. 5]`

x축은 **"Properation / %"** (= proportion 의 오기), 0–100 % 로 정규화된 반응 진행도.
**패널마다 변위 축 범위가 다르다** (a: +9~−12 · b: +10~−12 · c: 0~−20 · d: +10~−20 µm) —
**패널 간 절대 비교 금지**.

| 패널 | 빨강 = S 양극 | 파랑 = Li_xIn 음극 | 검정 = full cell |
|---|---|---|---|
| (a) 1차 방전 | 0 → **+3 µm** | 0 → **−11 µm** | 0 → **−6 µm** |
| (b) 1차 충전 | +2 → **−2 µm** (Δ ≈ −4) | −11.5 → −12 (Δ ≈ **−0.5**) | −5.8 → −6.5 (Δ ≈ **−0.7**) |
| (c) 2차 방전 | −1 → 0 (Δ ≈ **+1**) | −13 → −19.5 (Δ ≈ **−6.5**) | −6.5 → −9.5 (Δ ≈ **−3**) |
| (d) 2차 충전 | 0 → **−2 µm** | ≈ −20 (평탄) | ≈ −10 (평탄) |

★ `[해석]` **2차 방전에서도 음극이 −6.5 µm 나 더 줄어든다** (c). 본문은 "2차 사이클은 변화가
더 작다" 고 쓰지만 음극만 보면 1차(−11)와 같은 자릿수다. **Li–In 의 재배열은 2사이클로 끝나지
않는다** — Fig. 4a 가 60 h(≈5 사이클)까지 −35 µm 로 계속 내려간 것과 일치한다.

`[도표, Fig. 5 상단 반응식]` 각 패널 상단에 전압 분해식이 인쇄돼 있다:
- (a),(c) 방전: 빨강 `S8 + Li_x−LTO → Li2S + LTO` (V1) · 파랑 `Li_xIn + LTO → Li_x−LTO + In` (V2)
  · 검정 `S8 + Li_xIn → Li2S + In` (V = V1 + V2)
- (b),(d) 충전: 빨강 `Li2S + LTO → S8 + Li_x−LTO` (V1) · 파랑 `Li_x−LTO + In → Li_xIn + LTO` (V2)
  · 검정 `Li2S + In → S8 + Li_xIn`

`[도표]` (a) 와 (c) 에는 **회색 곡선이 하나 더** 있다 (검정 full-cell 전압 위쪽, ~1.5 → 0.3 V).
캡션·본문 어디에도 설명이 없다. `[해석]` V1+V2 의 계산값으로 보이나 **확인 불가** — 범례가 없다.

`[도표]` 전압 축: (a) 1차 방전 full cell 은 **≈1.35 → 0.15 V** (vs Li–In), (b) 1차 충전은
**≈1.25 → 2.40 V** (vs Li–In). 즉 **S∣LPSCl∣Li–In full cell 의 전압창은 ≈0.15–2.4 V vs Li–In**
`[도표]` 이고, 이것이 Fig. 1b,d 의 전압 범위(0.6–2.4 V)와 대체로 맞는다.

---

## 8. p.5–6 — 기전 가설과 압력 권고 (Fig. 6)

### 8.1 부피 변화가 SSE 셀에 남기는 것 `[인쇄, §3]`

- 무작위 배향 입자가 **이방성 부피 변화** → 양극 내 **미세균열(microcracks)**.
- 큰 부피 변화 → **새 기공·공극** → **활물질–SE–탄소 삼상 계면 파괴** → 미세구조 실패.
- 실시간으로 막지 못하면 **활물질/SSE 계면 불안정의 주원인**.
- **전극–전해질 박리(delamination)** 로 양극/SE 접촉의 기계적 손상.
- 공극에 의한 접촉 부족 → **계면 저항 증가, 전하이동 방해**, SSE 구조 건전성 저하 → 이온 확산
  방해 → **불균일 증가 → 불균일 분극 → Li 덴드라이트 가능성**.

### 8.2 압력 권고 수치 `[인쇄, §3]` ★

| 문장 | 값 |
|---|---|
| SSE 고밀도·저공극·큰 결정립을 위한 **성형 압력** | **"such as 370 MPa"**[11] |
| ASSLB **장기 사이클에 필요한 운전 스택 압력** | **"approximately 7 MPa"** |
| 정용적으로 돌릴 때 **셀 부피 감소** | **"could decrease by 10 %"** |
| 정용적으로 돌릴 때 **스택 압력 강하** | **"could drop by nearly 1 MPa"** |

★ `[재현]` **"10 % 감소"·"1 MPa 강하" 를 이 논문의 자기 데이터로 검산한다.**
- 부피 10 %: `[도표]` Li2S 셀 −19 µm. Fig. 7d 의 사이클 전 **양극 80.5 + SE 83.2 = 163.7 µm**
  → **−11.6 %**. **맞는다** (분모를 양극+SE 로 잡았을 때).
- 압력 1 MPa: `[도표]` Li_xIn 셀 −1.4 MPa, Li2S 양극 셀 −0.6 MPa, S 양극 셀 −0.41 MPa.
  **음극을 포함한 full cell 기준으로 ≈1 MPa 은 타당**하다.
- `[해석]` 따라서 **G6 의 "100 µm" 은 오기이고 실제 분모는 ≈164 µm 로 보인다** — 다만 그렇게
  읽으면 "15–20 %" 가 아니라 **8.6–12.2 %** 가 되어 본문의 두 수치가 서로 맞지 않는다.
  ★ **이 논문에서 인용할 안전한 값은 "정용적 운전 시 스택 압력이 7 → 6 MPa 로 약 1 MPa 떨어진다"
  하나다.**

### 8.3 Fig. 6 만화 — 가설의 그림 `[도표]`

`[인쇄, Fig. 6 캡션]` "Illustration showing the hypothesized morphology changes in an ASSLB
during cycling under constant pressure and constant volume conditions."

`[도표, Fig. 6]` 2행 × 3열. 각 칸은 **위: 복합양극(파란 큰 구 = SE, 노란 구 = 활물질, 검은 점 =
탄소) / 중간: SSE 층 / 아래: Anode(회색)**. 좌 → 우로 **초기 → Discharge → Charge**.

- **1행 정압(Constant Pressure)**: 방전 후 노란 활물질 입자가 **커지고 내부에 균열선**이 생긴다.
  충전 후 입자가 **작아지고 균열은 남지만**, 전극 상단 경계가 **아래로 내려온다**(빨간 "Displacement"
  화살표로 표시) — **압력이 전극 전체를 눌러 입자 재배열로 공극을 메운다**. 매트릭스에 흰 공백이
  거의 없다.
- **2행 정용적(Constant Volume)**: 방전은 같지만, **충전 후 입자 주위에 노란 점선 테두리와 흰
  공극**이 뚜렷하게 남는다. 전극 상단 높이는 그대로다. → **공극이 갇힌다**.

`[인쇄, §3]` 저자의 해설:
- 방전(환원) 시 황 입자가 크게 팽창 → **정압 구속이 없으면 미세균열이 더 잘 생긴다**.
- 충전(산화) 시 황 양극이 수축 → **정용적에서는 그 수축이 공극이 된다**.
- 스택 압력을 걸면 고체 양극이 눌려 **입자 재배열 → 공극 감소 → 삼상 계면 보존**.
- ★ "**it is the stack pressure, rather than the capillary effect, that drives the movement of the
  solid-state electrolyte**" (액체 전해질의 모세관 젖음과 대비).
- 결론 명제: **"while void formation can be mitigated by the external stack pressure, the cracking
  is permanent."**

`[해석]` Fig. 6 은 **가설의 그림이지 데이터가 아니다.** 논문도 "hypothesized" 라고 쓴다. 균열이
정압에서 "덜" 생긴다는 부분(1행 vs 2행의 균열선 개수)은 **SEM 으로 뒷받침되지 않았다** — Fig. 7
상단행은 균열이 아니라 **결정 크기**를 비교한다. 즉 **"압력이 균열을 줄인다" 는 그림에만 있다.**
논문 본문 §3 후반에도 "The fracturing **worsened under unconstrained conditions**" 라고 쓰지만
그 근거는 EIS 의 비가역성(회복 안 됨)이지 균열의 직접 관측이 아니다.

---

## 9. p.6–7 — 사후 단면 SEM (Fig. 7) ★ 유일한 정량 구조 데이터

`[인쇄, Fig. 7 캡션]` "Cross-section SEM images show (a) the sulfur cathode **before cycle**,
(b) after cycling under **7 MPa constant pressure** cycling, (c) after cycling under **constant
volume with an initial pressure of 7 MPa**, (d) the S|SSE interface before cycle, (e) after
constant pressure cycling and (f) after constant volume cycling."

`[인쇄, §3]` 시료: **갓 조립한 셀**과 **10 사이클 후 셀**.

### 9.1 두께 (그림 주석의 숫자 — 이 논문 유일의 구조 정량값) `[인쇄, Fig. 7d–f 주석]`

| 조건 | 양극 두께 | SSE 두께 | `[재현]` 양극 변화 | `[재현]` SSE 변화 | `[재현]` 합 |
|---|---|---|---|---|---|
| **사이클 전** (d) | **~80.5 µm** | **~83.2 µm** | — | — | 163.7 µm |
| **정압 7 MPa, 10 cyc** (e) | **~72.9 µm** | **~72.9 µm** | **−9.4 %** | **−12.4 %** | 145.8 µm (**−10.9 %**) |
| **정용적(초기 7 MPa), 10 cyc** (f) | **~88.1 µm** | **~74.1 µm** | **+9.4 %** | **−10.9 %** | 162.2 µm (**−0.9 %**) |

★★ `[재현]` **이 표가 이 논문에서 가장 깨끗한 결과다** — 그리고 논문은 이 계산을 하지 않았다.
- **정압**: 양극+SE 합계가 **−17.9 µm (−10.9 %)** 줄었다. → LVDT 로 잰 **−14~20 µm** 와 **일치**.
  두 독립 측정(LVDT, 단면 SEM)이 같은 값을 준다.
- **정용적**: 양극+SE 합계는 **−1.5 µm (−0.9 %)** — 거의 변하지 않았다. **당연하다. fixture 가
  높이를 고정했으니까.** 대신 **내부에서 재분배**가 일어났다: **SE 가 −9.1 µm 얇아진 만큼
  양극이 +7.6 µm 두꺼워졌다.**
- `[해석]` **즉 정용적 셀에서는 "양극이 SE 를 밀어내며 부푼다".** 양극은 공극 때문에 부피가
  늘고, 그 팽창이 갈 곳이 없어 **SE 층을 압축해 버린다.** 이것이 본문이 말한 "SSE 가 훨씬
  비정질스러워졌다" 의 기계적 원인일 것이다 `[해석]`.
- 본문은 이 재분배를 "the cathode's thickness increased **slightly** while the SSE's thickness
  **slightly** decreased" 라는 한 줄로 흘려보낸다 (G12). **9–11 % 는 slightly 가 아니다.**

### 9.2 형태 `[인쇄, §3]` + `[도표, Fig. 7a–c]`

`[인쇄]` 정압: SSE·양극 모두 **약 10 % 얇아지고 더 치밀·저공극**. SSE 형태는 사이클 전과
**유사하게 유지**.
`[인쇄]` 정용적: 양극 두께는 **약간 증가**, SSE 두께는 **약간 감소**. 가장 두드러진 관측은
**"the SSE became a lot more amorphous under constant volume cycling"**.

`[도표, Fig. 7a–c]` (×8.00k, 스케일바 5.00 µm, 3.0 kV):
- (a) **사이클 전**: 거칠고 불규칙한 파쇄면. 뚜렷한 결정면 없음. 미세한 요철 다수.
- (b) **정압 후**: **크고 매끈한 판/막대 결정** — 길이 **≈5–10 µm**, 면이 평평하고 모서리가 뚜렷.
  배경 기공은 적다.
- (c) **정용적 후**: **작고 짧은 막대 결정 다수** — 길이 **≈1–2 µm**, 결정 사이에 **어두운 공극이
  촘촘히** 보인다. (a) 보다도 공극이 많아 보인다.

`[인쇄, §3]` 저자의 해석: 크고 매끈한 황 결정은 **끊기지 않은 삼상 계면**의 결과다. 연속된
전하이동 네트워크가 **Li2S 의 산화를 뒷받침**하므로 결정이 크게 자란다. 공극이 생겨 계면이
끊기면 **작은 황 결정**이 된다. 정용적 후 공극률 증가(c)와 정압 후 공극률 감소(b)가 Fig. 6 의
가설과 **일치**.

★ `[해석]` **이 해석은 매력적이지만 원소 증거가 없다** (G15). ×8k 이미지 3장에서 "결정 크기" 를
눈으로 비교했을 뿐, **EDS 도 XRD 도 라만도 없다.** 황화물 SE(LPSCl)의 결정 입자와 S8 결정은
2차전자 상에서 구별되지 않는다. 또 (a) 와 (b),(c) 는 **서로 다른 파단면**이므로 파단 방식의
차이가 형태를 만들었을 수도 있다.

`[도표, Fig. 7d–f]` (×700, 스케일바 50.0 µm): 노란 점선이 **양극/SSE 경계**, 빨간 막대가 두께
측정선. (f) 정용적 시료는 (d),(e) 보다 **경계가 울퉁불퉁**하고 상부(SSE)에 **큰 어두운 공동**이
보인다 — 다만 이 공동이 시료 준비(파단) 인공물인지 구분할 수 없다 `[해석]`.

---

## 10. p.7–8 — 전기화학 검증: 사이클·EIS·DRT (Fig. 8)

`[인쇄, Fig. 8 캡션]` "(a) Comparison of the cyclability of ASSLB cells cycled under **constant
pressure of 7 MPa** versus that cycled at a **constant volume with an initial pressure of 7 MPa**.
(b) AC impedance comparison after **0, 3 and 10 cycles** under constant pressure and constant
volume conditions, with the inset showing an enlarged view of the high-frequency region.
(c) Comparison of the **DRT** derived from the impedance spectra in (b). After 10 cycles of
constant volume conditions, the ASSLB cell was **recompressed to 7 MPa**."

★ **셀의 화학은 캡션에도 본문에도 없다** (G3).

### 10.1 사이클 (Fig. 8a)

`[인쇄, §3]`
- 정압 셀은 **"maintained it capacity well throughout the 100 cycles"**.
- 정용적 셀은 **3번째 사이클부터 감소 시작**, 계속 하락.
- **10번째 사이클 후 7 MPa 로 재압축** → 용량이 **부분 회복**, 정압 셀에 근접.
  그러나 **곧 다시 감소**.
- **20 사이클 후 재압축** → **약간만** 개선, 이후 **급격히** 하락.
- 이후 **10 사이클마다 재압축** → **최소한의 회복만**.
- 정압 셀은 계속 용량을 잘 유지.

`[도표, Fig. 8a]` y축 좌 = **Capacity retention / %** (0–140), y축 우 = **Coulombic Efficiency / %**
(0–120), x축 **Cycle Number 3–100**. 그림 주석: **"Repressed to 7 MPa after 10, 20, 30, 40, 50
and 60 cycles"** (화살표 6개).

| 곡선 | 사이클 3 | 사이클 100 |
|---|---|---|
| **정압 7 MPa** 유지율 (검정) | 100 % | **≈63 %** |
| **정용적** 유지율 (빨강) | 100 % | **≈50 %** |
| **CE** (검정·빨강 모두) | ≈100 % | **≈100 %** (양쪽 모두, 산발적 이상점 제외) |

★★ `[해석]` **G20 의 자리.** 그림이 실제로 말하는 것은:
1. **정압 셀도 100 사이클에 37 % 를 잃는다.** "maintained well" 은 **상대 진술**이다.
2. 두 조건의 차이는 **63 vs 50 %, 13 포인트**다 — 실재하지만 극적이지 않다.
3. **CE 는 양쪽 다 ≈100 %** 다. 즉 **"안정" 을 CE 로 말하면 두 셀이 똑같이 안정**하다.
   이 위키의 규율대로 **"안정" 이 CE 인지 용량인지 갈라야 한다** — 여기서는 **용량**이다.
4. **재압축의 회복은 실재한다** — 10사이클 후 빨강이 **≈63 → 72 %** 로 튀어오르고(그림에서
   화살표가 가리키는 첫 회복), 이후 회복폭이 점점 작아져 50 사이클 이후에는 거의 없다.
   ★ 이것이 논문의 핵심 주장("공극은 압력으로 되살릴 수 있으나 균열은 아니다")의 **가장 강한
   증거**다.
5. `[도표]` 정용적 곡선은 **60 사이클 부근에서 ≈50 % 로 주저앉은 뒤 평탄**해진다. 재압축을
   60 사이클까지만 한 것도 그 때문으로 보인다 `[해석]`.

### 10.2 임피던스 (Fig. 8b)

`[인쇄, §3]`
- 정압 7 MPa 셀의 **Ohmic 저항은 첫 10 사이클 동안 안정**.
- 정용적 셀의 **Ohmic 저항은 거의 50 % 증가**.
- ★ **"the Ohmic resistance increases – rather than decreases as conventional wisdom might
  suggest - when the cell is recompressed to 7 MPa after cycling for 10 cycles under constant
  volume condition."**

`[도표, Fig. 8b]` 주 그림: 6개 곡선이 모두 **거의 직선(≈45°)** — 저주파에서 확산/블로킹 거동.
실축 0–500 Ω. **반원이 사실상 보이지 않는다** (60 °C 에서 만든 셀을 상온에서 쟀는데도).
인셋(실축 25–100 Ω, 허축 0 ~ −50 Ω) 의 고주파 절편 `[도표]`:

| 곡선 | Ohmic 절편 `[도표]` |
|---|---|
| Before cycle (검정) | **≈38–40 Ω** |
| CP-after 3rd (빨강) | **≈40 Ω** |
| CP-after 10th (파랑) | **≈40 Ω** |
| CV-after 3rd (초록) | **≈45 Ω** |
| CV-after 10th (자홍) | **≈55 Ω** |
| **CV-after 10th, back 7 MPa** (갈색) | **≈62–65 Ω** ← **가장 높다** |

`[재현]` 40 → 58–60 Ω 이면 **+45–50 %** — 본문의 "nearly 50 %" 와 맞는다.
인셋에는 **빨간 원(정압 7 MPa 무리)** 과 **파란 화살표 "Increase with cycling"** 이 인쇄돼 있다.

★ `[해석]` **재압축이 Ohmic 저항을 더 올린다는 것이 이 논문에서 가장 반직관적인 관측**이고,
저자의 설명(균열이 이미 났고 7 MPa 로는 못 붙인다)은 그럴듯하지만 **대안 설명을 배제하지
않았다**: 재압축 자체가 이미 균열된 입자를 **더 부수거나** 접촉을 국소적으로 끊었을 수 있다.
같은 데이터가 **"재압축은 해롭다"** 로도 읽힌다 — 그런데 Fig. 8a 에서는 재압축이 **용량을
올린다**. 즉 **Ohmic 은 나빠지고 용량은 좋아진다.** 논문은 이 모순을 다루지 않는다.

### 10.3 DRT (Fig. 8c)

`[인쇄, §3]`
- 주 피크(**시간상수 0.1–1 s**)가 셀 동역학·저항의 병목.
- 정압 셀은 **3사이클 후 시간상수 불변**, 전하이동 저항만 **소폭 증가**.
- 정용적 셀은 **시간상수와 저항이 모두 증가**.
- 갓 조립한 셀의 **작은 어깨 피크**가 정압 3사이클 후에는 **유지**되지만 정용적에서는 **사라진다**.
- 10사이클 후에는 두 조건의 **시간상수가 비슷**해지지만, 정용적 셀의 **저항이 뚜렷이 높다**.
- 재압축 후에도 동역학·저항에 **큰 변화 없음**, **저항만 약간 더 증가**.

`[도표, Fig. 8c]` y = G(τ) / Ω s⁻¹ (0–600), x = τ / s (10⁻³–10). 주 피크와 중간 피크를 읽으면:

| 곡선 | 주 피크 위치 τ | 주 피크 높이 G | τ≈0.02–0.03 s 피크 | τ≈1 s 어깨 |
|---|---|---|---|---|
| Before cycle (검정) | **≈0.27 s** | **≈305** | ≈50 | **있음 (≈105)** |
| CP-after 3rd (초록) | **≈0.30 s** | **≈348** | ≈75 | **있음 (≈110)** |
| CV-after 3rd (빨강) | **≈0.45 s** | **≈310** | ≈65 | **없음** |
| CP-after 10th (파랑) | **≈0.45 s** | **≈372** | ≈70 | 없음 |
| CV-after 10th (자홍) | **≈0.45 s** | **≈525** | ≈105 | 없음 |
| **CV-after 10th, back 7 MPa** (갈색) | **≈0.45 s** | **≈570** | ≈112 | 없음 |

★ `[해석]` **그림은 본문 주장을 대체로 뒷받침하지만 한 군데가 어긋난다**:
- **τ≈1 s 어깨의 존재/소멸은 정확히 맞는다** — 검정·초록에는 있고 빨강에는 없다. 이 관측은
  이 논문에서 가장 미세하고 가장 설득력 있는 증거다.
- **CV-10th(525) ≫ CP-10th(372)** 도 맞는다. **재압축 후 570 으로 더 오른다** 도 맞는다
  (Fig. 8b 와 같은 방향).
- **어긋나는 것**: "정용적은 3사이클 후 저항이 증가" 라는데 **빨강(310)은 검정(305)과 거의
  같고 초록(348)보다 낮다.** 시간상수는 확실히 오른쪽(0.27 → 0.45 s)으로 갔지만, **피크 높이로는
  정압 쪽이 더 높다.** 저항은 G(τ) 의 **면적**이고 빨강이 더 넓으므로 면적으로는 뒤집힐 수
  있으나, **논문은 면적을 계산해 보이지 않았다.**
- DRT 의 **정규화 파라미터(λ)·알고리즘이 미기재**여서 피크 높이 비교의 신뢰구간을 알 수 없다.

---

## 11. p.8 — §4 Conclusion `[인쇄]`

> "Using our custom-made fixture, we successfully monitored the vertical displacement of ASSLBs
> under constant pressure cycling and observed pressure variations during constant volume cycling.
> Additionally, we were able to **decouple the volume changes of the sulfur, Li₂S cathodes, Li_xIn
> anode, and SSE**. Our hypothesis was confirmed through SEM imaging and electrochemical impedance
> analysis, revealing that **at least two types of changes** occur during ASSLB cycling: volume
> expansion and contraction, material fracturing, and the formation of voids. We found that while
> the **structural changes to the primary active material particles are irreversible**, **void
> formation can be mitigated through the application of stack pressure**. Stack pressure reduces
> fracturing and promotes void healing by enabling particle rearrangement. In conclusion, the
> **primary role of stack pressure is to maintain microscale integrity by ensuring continuous
> physical contact between particles, thus preventing the formation of voids.**"

`[해석]` 결론 문장 자체에 **"two types" 라 해놓고 세 가지를 나열**하는 오류가 있다 (팽창/수축,
파단, 공극). 초록은 제대로 둘(균열, 공극)로 쓴다.

---

## 12. SI 대조 — **미확보**

| SI 항목 | 본문에서의 쓰임 | 이 digest 의 처리 |
|---|---|---|
| **Fig. 1S** | `[인쇄, §1]` "The excessive weight of the stack pressure fixture, **accounting for 80–90 % of the cell/battery weight**, as shown in Fig. 1S, necessitates a redesign of the cell for practical use." | **SI 미확보.** 80–90 % 라는 수치의 계산 근거(어느 fixture, 어느 셀 크기)를 확인하지 못했다. 인용 시 "저자 주장" 으로만. |
| **Video 1S** | `[인쇄, §3]` "a symmetric **Li\|SSE\|Li** cell demonstrated **reciprocal behavior** during cycling. The volume increase on one Li electrode compensated for the volume shrinkage of the opposite Li electrode, making the overall volume change of the entire cell **negligible**." | **SI 미확보.** 이 위키에서 **Li 금속 전극의 부피 항을 정량으로 쓸 수 없다.** §6 의 "상보성" 설계 원리는 이 영상에만 근거한다. |

`[인쇄]` 본문의 SI 링크: "Supplementary material related to this article can be found online at
doi:10.1016/j.nanoen.2025.110887." **Table S 는 인용 자체가 없다.**

★ **후속 작업**: SI(특히 Video 1S)를 구하면 anode-free 의 Li 석출 부피 항에 직접 걸린다.
지금은 [[anode-free-li2s-assb]] 에 **"압력" 만 채우고 "Li 부피" 는 비워 둔다.**

---

## 13. 이론 부피 변화 vs 실측 — `[재현]` 대조

이 절은 **원문에 없는 계산**이다. 모두 `[재현]`/`[해석]` 이며, 가정을 명시한다.

**가정**: ρ(Li2S) = 1.66, ρ(S, α-S8) = 2.07 g cm⁻³ (§5.2 표) · 양극 두께 **80.5 µm**
(Fig. 7d 주석) · 두께 변화는 면내 구속 하에서 부피 변화가 **전부 두께로만** 나타난다고 본다
(원통 셀이므로 타당) · 전환은 완전하다고 본다.

| 물음 | 계산 | 값 |
|---|---|---|
| Li2S 1 mol 의 완전 탈리튬화(충전)로 줄어드는 부피 | 27.68 − 15.49 | **12.19 cm³ mol⁻¹ = −44.0 %** |
| 같은 반응의 역방향(방전) 팽창률 | 12.19 / 15.49 | **+78.7 %** |
| 양극 두께 80.5 µm 가 −10 µm 줄려면 필요한 **Li2S 부피분율** | 10 / (0.440 × 80.5) | **f ≈ 0.28 (28 vol%)** |
| 안정화 후 진동 ±1 µm 에 대응하는 **가역 전환 부피분율** | 1 / (0.440 × 80.5) | **f ≈ 0.028 (2.8 vol%)** |

★★ `[해석]` **여기서 이 논문이 말하지 않은 것이 나온다.**
1. **첫 충전의 −10 µm** 는 Li2S 부피분율 ≈28 % 의 **완전 전환**과 같은 크기다. 33.3 wt% 의
   Li2S 가 (SE·탄소보다 가벼우므로) 부피로 30 % 안팎을 차지한다고 보면 **정확히 맞는 자릿수**다
   — 즉 **첫 충전의 셀 수축은 Li2S → S 전환만으로도 거의 전부 설명된다.**
   (저자는 이 몫을 "재배열" 과 나누지 않았다.)
2. 그런데 **안정화 후의 사이클당 진동은 ±1 µm**, 즉 위 값의 **1/10** 이다. 같은 반응이
   같은 양만큼 왕복한다면 매 사이클 ±10 µm 가 나와야 한다.
   → 셋 중 하나다: **(a) 몇 사이클 만에 활물질 이용률이 1/10 로 떨어졌거나, (b) 복합양극 내부
   공극이 활물질의 변형을 흡수해 셀 두께로 나오지 않거나, (c) 둘 다.**
   Fig. 8a 가 100 사이클에 63 % 를 유지한다는 것(정압)을 보면 **(a) 만으로는 설명이 안 된다.**
   → ★ **SE 50 wt% 복합양극은 활물질 변형의 대부분을 내부에서 흡수한다**는 뜻이 된다.
   이것이 사실이라면 **"cell breathing" 의 주범은 반응이 아니라 비가역 치밀화(재배열)** 다.
3. `[해석]` 이 추론이 우리에게 중요한 이유: **우리 조성(SE 50 wt%)이 이 논문과 같으므로**,
   우리 셀에서도 **첫 사이클 이후의 셀 두께 변화는 작을 것**이고, **압력 관리의 초점은
   "첫 충전 + 초기 몇 사이클" 에 놓여야 한다.** 이 논문의 모든 데이터(Fig. 3, 4, 8a 의 초기
   구간)가 같은 방향을 가리킨다.

---

## 14. 우리 연구와의 접점

### 14.1 이식 가능 / 불가 표

| 이 논문 | 우리 ([[li2s-assb-reference-cell]] / [[anode-free-li2s-assb]]) | 옮겨 올 수 있는 것 | 옮겨 올 수 없는 것 |
|---|---|---|---|
| Li2S : C65 : LPSCl = **33.3 : 16.7 : 50 wt%**, 바인더 없음 | Li2S : LPSCl : AB = **30 : 50 : 20** | ★ **거의 그대로** — SE 50 wt% 동일, 활물질 ±3 wt% | 탄소 종류 (Super C65 vs AB) |
| **one-step** planetary BM, ZrO2 용기, **300 rpm 4 h**, Pulverisette 7 | one-step BM (주 경로) | ★ **장비·rpm·시간의 구체적 선례** → [[mixing-equipment-ball-mill-thinky]] | 볼/BPR/분위기 (미기재 G13) |
| **운전 스택 압력 7 MPa** 정압 | (기록 필요) | ★ **우리 셀의 압력을 기록·고정하라**는 규율 | 7 MPa 라는 값의 타당성 (G19, §15) |
| 성형: SE 필름 **300 MPa 3 min** / SE 펠릿 **500 MPa** / 양극 압착 **300 MPa 3 min** / Li–In **50 MPa 20 s** | (기록 필요) | ★ **성형 조건 세트 전부** | — |
| **LVDT + 스프링 4개** 정압 fixture, **압력변환기 + 나사** 정용적 fixture | 없음 | ★ **설계 수치 전부** (§3.1 `[재현]` 표) — 우리가 만들 수 있다 | 논문의 "10⁻² MPa" 환산 (G10 — 틀렸다) |
| **LTO 를 zero-strain 대극**으로 써서 성분 분해 | 없음 | ★ **방법 자체** — 어느 쪽이 움직이는지 가르는 값싼 수단 | LTO 화학식 표기 (G17) |
| Li2S 양극이 S 양극보다 수축 크다 (19 vs 15 µm) | Li2S 가 우리 활물질 | **Li2S 는 첫 단계가 수축**이라는 인식 | 절대값 (로딩 미기재 G2) |
| ★ **Li2S 첫 충전 한 번에 총 수축의 절반(≈10 µm)** `[도표]` | [[li2s-activation-first-charge]] | ★ **활성화의 기계적 얼굴** — 첫 충전에서 압력을 특히 관리 | 첫 충전 컷오프 수치 (G4) |
| **Li_xIn 음극 −42 µm** — 세 성분 중 최대 | 1단계 음극이 Li–In | ★ **우리 셀 부피 변화의 주범은 음극일 수 있다** | Li–In 조성·두께가 다르면 값도 다르다 |
| 정용적에서 **양극 +9.4 %, SE −10.9 %** (SEM) | — | ★ **"양극이 SE 를 밀어낸다"** 는 실측 | 우리 셀 두께로의 환산 |
| 재압축은 용량을 **부분 회복**시키나 **Ohmic 은 오히려 오른다** | — | **공극(가역) vs 균열(비가역) 이분법** | 이 이분법의 직접 증거는 약하다 (§16) |
| Li∣SSE∣Li 대칭셀의 **상보적 부피 거동** | anode-free 의 Li 석출 | 설계 원리("양극 팽창 ↔ 음극 수축을 동기화") | **정량값 없음 (Video 1S 미확보 G18)** |
| 60 °C 운전 | 우리 온도 (기록 필요) | — | **온도가 다르면 SE 소성·크리프가 다르다** |

### 14.2 [[anode-free-li2s-assb]] 의 "스택 압력·집전체" 항목에 넣을 것

그 페이지의 미결 항목 4번("스택 압력·집전체 계면이 침적 형태를 정한다 — 근거 논문 없음")에
대해 이 논문이 **채우는 것**과 **못 채우는 것**:

**채운다 (압력 쪽)**
1. ASSB 에서 **운전 스택 압력의 1차 역할은 "공극 방지" 이지 "접촉 압착" 이 아니다** —
   압력은 **입자 재배열**을 가능하게 해 활물질 수축이 만든 공극을 메운다 (`[인쇄]` 결론).
2. **정용적으로 두면 7 MPa 가 ≈1 MPa 떨어진다** (`[인쇄]`) — 즉 **스프링이나 벨빌 와셔 같은
   compliance 가 없는 구속은 몇 사이클 만에 압력을 잃는다.**
3. 압력 손실의 결과는 **Ohmic +50 %**, **DRT 주피크 +40 %**, **100 사이클 용량 50 vs 63 %**.
4. **되돌릴 수 없다** — 10사이클 후 재압축은 용량을 일부 되살리지만 회복폭이 사이클마다
   줄고, **Ohmic 저항은 오히려 더 오른다**.
5. **작은 셀에서도 fixture 가 무게의 80–90 %** (저자 주장, Fig. 1S 미확보) — anode-free 의
   에너지밀도 논거는 **압력 하드웨어를 포함해** 따져야 한다.

**못 채운다 (집전체 쪽)**
- 이 논문에 **anode-free 구성이 없다.** 음극은 Li–In 또는 LTO 이고, **집전체는 스테인리스 로드**
  뿐이다. Li 석출 형태·집전체 코팅·핵생성에 관한 데이터가 **전혀 없다.**
- Li 금속의 부피 항은 **Video 1S 하나**(미확보)에만 있다.
- → [[anode-free-li2s-assb]] 의 4번 항목은 이 논문으로 **절반만** 채워진다. 나머지 절반
  (집전체·Li 침적)은 여전히 비어 있고, 그 자리는 `raw/papers/zhang2026_…`(Na 박 집전체,
  0/1/4 MPa)가 더 가깝다.

### 14.3 가장 값싼 다음 실험 `[해석]`

1. **지금 당장, 장비 없이**: 우리 셀의 **성형 압력·운전 압력·유지 방식(강체 볼트인가 스프링인가)
   을 실험 노트에 수치로 기록한다.** 이 논문이 보여준 대로 그 값이 없으면 나중에 어떤 비교도
   불가능하다 (Huang 2026 G1 이 그 예다).
2. **볼트 구속이라면**: 우리 셀은 지금 **정용적 조건**일 가능성이 높다. 그렇다면 **첫 10 사이클
   후 한 번 재조임**만 해도 이 논문의 Fig. 8a 대로 용량이 튀어오를 수 있다 — **재조임 전후
   EIS** 로 확인한다 (장비 추가 없음).
3. **스프링 도입**: 이 논문의 §3.1 `[재현]` 표대로 **4개 병렬 254 N mm⁻¹, 초기 압축 3.4 mm**
   면 φ12.6 mm 셀에서 7 MPa 다. 우리 셀 지름에 맞춰 스케일하면 된다.
   (권장: **변위 허용범위를 5 µm 로 잡아야** 압력 변동이 0.01 MPa 이내다 — G10.)
4. **LVDT 없이 하는 근사**: 다이얼 게이지(1 µm 분해능)로도 이 논문의 신호(첫 충전 −10 µm)는
   보인다. **가장 값싼 관측은 "첫 충전 전후 셀 높이 1회 측정"** 이다.
5. **LTO 대극 트릭**: 우리 셀에서 양극/음극 중 누가 움직이는지 가르고 싶다면 **LTO 대극 셀 한
   개**면 된다 (이 논문의 방법 그대로). Li–In 이 주범인지 확인하는 가장 싼 방법.

### 14.4 열린 질문 카드와의 연결 `[해석]`

- [[reference-cell-500-600-mahg]] — 이 논문은 **절대 용량을 주지 않으므로(G1) 목표값 자체에는
  근거를 주지 못한다.** 대신 **"용량이 안 나올 때 의심할 변수" 목록에 스택 압력을 추가**한다.
  특히 **우리 셀이 볼트 고정(정용적)이라면 이 논문이 예측하는 열화 패턴(3사이클부터 감소,
  재조임으로 부분 회복)** 을 확인할 수 있고, 그 패턴이 보이면 원인이 조성이 아니라 **구속
  방식**이라는 뜻이다. → 이 카드에 **압력 가설**을 새로 붙일 자리.
- [[one-step-vs-two-step-mixing]] — 이 논문은 **one-step**(Li2S + C65 + LPSCl 동시 투입,
  planetary 300 rpm 4 h)으로 동작하는 셀을 만들었다는 **약한 for-evidence** 다. 단 **성능
  절대값이 없어(G1) one-step 의 우열을 말하지 못한다.** 조건만 [[composite-cathode-mixing-routes]]
  의 칸에 채워 넣는다.

---

## 15. ★ 압력 축에서 세 논문을 나란히 놓기

이 위키에 지금 있는 세 digest 의 압력 정보를 한 표로 모은다. **성형/운전을 반드시 갈라 읽는다.**

| | **Qu 2025** (이 논문) | `zhang2026_…` | `huang2026_…` |
|---|---|---|---|
| 계 | LPSCl, S 또는 Li2S 양극, Li–In / LTO | LPSCBr, Li2S-PI3 양극, **anode-free(Na 박)** | LPSC, S 양극 + HES |
| **성형 — SE** | 필름 **300 MPa 3 min** / 펠릿 **500 MPa** | **250 MPa 3 min** | **350 MPa** |
| **성형 — 양극** | **300 MPa 3 min** (SE 필름에 압착) | **400 MPa 3 min** | **450 MPa** |
| **성형 — 음극** | Li–In **50 MPa 20 s** | Li **75 MPa 30 s** · Na/Cu **25 MPa 30 s** | 미기재 |
| **운전 스택 압력** | **7 MPa** (정압) · 정용적(초기 7 MPa) | **0 / 1 / 4 MPa** (설정값) | **미기재 (G1)** |
| 온도 | **60 °C** | 25 °C (일부 90 °C) | 상온 |
| 압력이 성능에 미친 영향 | 정압 **63 %** vs 정용적 **50 %** @100 cyc `[도표]` | 4 MPa **92.2 %** · 1 MPa **70.54 %** @300 cyc · **0 MPa 는 60 cyc 에 붕괴** | 측정 없음 |
| 압력의 **기전**을 쟀는가 | ★ **쟀다** (변위 µm, 압력 MPa, 단면 SEM, DRT) | 안 쟀다 (성능 곡선만) | 안 쟀다 |
| 압력을 **낮추는 방법**을 제시했나 | 아니오 (7 MPa 유지를 권한다) | ★ **예** (Na 의 낮은 항복강도로 1 MPa 가능) | 아니오 |

★★ `[해석]` **두 논문을 나란히 놓으면 위키 수준의 충돌이 하나 드러난다.**

- Qu 2025 은 `[인쇄, §1·§3]` **"cycling stack pressure above 7 MPa are crucial"**,
  **"A stack pressure of approximately 7 MPa is necessary for the long-term cycling performance
  of an ASSLB"** 라고 두 번 쓴다. **출처 없음(G19), 다른 압력값을 시험하지 않음.**
- Zhang 2026 은 같은 아지로다이트 계·같은 Li2S 활물질에서 **4 MPa 로 300 사이클 92.2 %**,
  **1 MPa 로도 300 사이클 70.54 %** 를 보였다 (단 0 MPa 는 60 사이클에 붕괴).
- → **"7 MPa 가 필요하다" 는 명제는 이 위키 안에서 이미 반증 쪽으로 기운다.** 실제로 필요한
  것은 **"0 이 아닌, 그리고 사이클 중에 떨어지지 않는" 압력**이다. Qu 2025 자신의 데이터가
  그렇게 말한다 — 정용적 셀이 죽은 이유는 **압력이 낮아서가 아니라 압력이 7 → 6 MPa 로
  *떨어졌기* 때문**이고, Zhang 2026 의 1 MPa 셀은 **1 MPa 를 유지**했다.
- ★ **이 위키가 채택할 명제**: **절대값보다 "유지" 가 중요하다.** 낮은 압력이라도 compliance
  (스프링/벨빌)로 **일정하게** 유지되면 돌아가고, 높은 압력이라도 강체 구속이면 첫 몇
  사이클에 잃는다. 두 논문이 서로 다른 축에서 같은 결론을 가리킨다.
- `[해석]` 온도도 갈린다 — Qu 2025 은 **60 °C**, Zhang 2026 은 **25 °C**. 60 °C 에서는 황화물
  SE 의 크리프가 커서 재배열이 더 쉬울 것이고, 그렇다면 **Qu 의 "압력이 재배열을 유도한다"
  는 60 °C 의 이야기**일 수 있다. 상온에서 같은 효과가 나는지는 두 논문 어느 쪽도 답하지 않는다.

`[해석]` Huang 2026 의 G1(운전 압력 미기재)은 이 논문으로 **메워지지 않는다** — 다른 셀이다.
그러나 **"성형 300–500 MPa / 운전 1–7 MPa" 라는 두 자릿수 분리**가 세 논문 공통이므로,
Huang 2026 의 성능을 읽을 때 **"운전 압력이 7 MPa 근처였을 것" 으로 가정하는 것은 부당하지
않다** — 다만 그것은 가정이고 digest 에는 여전히 "미기재" 로 남긴다.

---

## 16. 비판 (이 digest 의 판단)

1. ★ **"측정 논문" 인데 측정의 정량성이 저자 스스로 부인된다.** Fig. 5(제목의 "Deciphering"
   이 사는 자리)는 **세 개의 다른 셀**을 100 % 로 정규화해 겹친 것이고, 저자도 "more
   qualitative than quantitative", "adding the red and blue lines might not exactly result in
   the black curve" 라고 적는다 (G7). 실제로 **+3 + (−11) = −8 ≠ −6 µm** 로 25 % 가 안 맞고
   (G9), 단위 오기("6 mm")까지 있다 (G8). **성분 분해는 방향성 결론까지만 유효하다.**
2. ★ **절대 용량·로딩이 없다** (G1, G2). 이 때문에 (a) 셀의 품질을 알 수 없고, (b) µm 를
   활물질 몰수로 정규화할 수 없고, (c) 우리 셀로의 환산이 막힌다. **부피 변화 논문이 활물질
   질량을 안 적는 것은 치명적이다** — 부피 변화는 정의상 반응한 물질의 양에 비례한다.
3. ★ **"maintained it capacity well" 이 63 % 다** (G20). 정압 셀도 100 사이클에 37 % 를 잃는다.
   **CE 는 양쪽 다 ≈100 %** 이므로, 이 위키의 규율대로 **"안정" 은 CE 가 아니라 용량으로
   읽어야 하고 그 값은 63 % vs 50 % 다.** 초록의 "enhance battery performance and durability"
   는 13 포인트의 차이다.
4. ★ **자기 데이터를 자기 서술이 가린다** (G12). Fig. 7 의 정용적 결과 — **양극 +9.4 %,
   SE −10.9 %** — 는 이 논문에서 가장 깨끗하고 가장 기계적으로 의미 있는 수치인데,
   본문은 "slightly" 두 번으로 넘어간다. 이 digest 는 그 계산(§9.1)을 복원해 둔다.
5. **"균열은 영구적, 공극은 가역" 이분법의 직접 증거가 없다.** 균열을 **본 적이 없다** —
   Fig. 6 은 만화이고, Fig. 7 상단행은 균열이 아니라 결정 크기를 비교한다. 균열의 근거는
   **EIS 의 비가역성**(재압축해도 Ohmic 이 안 내려감)이라는 **간접 추론 하나**다. 대안 설명
   (재압축이 접촉을 더 망쳤다, SE 층이 이미 비정질화됐다)을 배제하지 않았다.
6. **상 동정이 전혀 없다** (G15). "sulfur crystal 이 커졌다/작아졌다" 는 ×8k SEM 3장의
   형태 판독이고, **EDS·XRD·라만 어느 것도 없다.** 황화물 SE 결정과 S8 결정을 2차전자 상에서
   구별할 근거가 제시되지 않았다.
7. **7 MPa 의 출처가 없고 다른 압력을 시험하지 않았다** (G19). 이 논문은 "압력이 중요하다" 를
   보였지 **"7 MPa 가 필요하다" 를 보이지 않았다.** 비교군은 7 MPa 와 "7 MPa 에서 시작해
   떨어지는 것" 둘뿐이다. 3 MPa 정압, 1 MPa 정압이 없다. → §15 의 충돌.
8. **DRT 의 방법이 미기재**다. 정규화 파라미터·알고리즘 없이 피크 높이를 비교한다. 게다가
   그림에서 읽으면 **"정용적 3사이클 후 저항 증가" 가 피크 높이로는 성립하지 않는다**
   (CV-3rd 310 < CP-3rd 348 — §10.3).
9. **EIS 를 상온에서 쟀는데 사이클은 60 °C 였다** (§3.6). 논문은 이를 언급하지 않는다.
10. **표기 오류가 많다**: LTO 화학식 Li4Ti4O12 (G17), "1166 **MAh** g⁻¹", 캡션의 "LIPSCl"/
    "LiPSCl", x축 "Properation", "6 mm", 결론의 "two types" 뒤 세 가지 나열, "sulfur's113 °C".
    **교정이 거의 안 된 원고다.** 참고문헌도 11개뿐이다.
11. **좋은 점은 분명하다** `[해석]`:
    - **fixture 두 개의 설계가 단순하고 복제 가능**하다 (같은 셀 몸통, 스프링 유무만 차이).
      LVDT 를 쓴 것은 실용적 선택이고 부품번호까지 적어 두었다. **이 논문의 진짜 가치는
      여기 있다.**
    - **LTO zero-strain 대극으로 성분을 가른다**는 착상이 값싸고 명확하다.
    - **재압축 실험**(10·20·30…사이클마다)은 "공극 vs 균열" 가설을 **직접 시험하는 설계**다.
      회복폭이 사이클마다 줄어드는 곡선은 이 논문의 가장 강한 데이터다.
    - **τ≈1 s DRT 어깨의 소멸**은 미세하지만 재현 가능한 관측이고, 기전 주장과 정합한다.
    - **서론의 문제의식**(압력 fixture 가 셀 무게의 80–90 %)은 이 분야가 잘 안 적는 정직한
      지적이다.

---

## 17. 이 저장소가 가져갈 것

- **개념 신설 후보**: `stack-pressure-volume-change-assb` — "ASSB 의 운전 스택 압력: 무엇을
  하는가, 얼마가 필요한가, 어떻게 유지하는가". 뼈대는 (1) 성형 압력 ≠ 운전 압력(두 자릿수
  차이), (2) 압력의 1차 역할은 **공극 방지 = 입자 재배열 허용**, (3) **절대값보다 유지**
  (정압 vs 정용적, compliance 의 필요), (4) 가역(공극) vs 비가역(균열) 이분법과 그 증거의
  한계, (5) 실측 자릿수 표(이 digest §6 의 성분별 변위·압력 표), (6) 미해결 — 최소 필요
  압력은 계·온도·음극에 따라 다르며 1–7 MPa 사이 어딘가.
  `sources:` 는 이 digest + `raw/papers/zhang2026_…` → **multi-source-primary** 가 된다.
- **[[li2s-activation-first-charge]] 갱신**: "Li2S 첫 충전은 **기계적 사건이기도 하다** —
  Qu 2025 `[도표, Fig. 3c]` 에서 첫 충전 한 번에 셀이 ≈10 µm 줄고 이는 전체 수축의 절반이다"
  한 줄. `sources:` 에 이 digest 추가.
- **[[li2s-assb-composite-cathode]] 갱신**: 우리와 같은 **SE 50 wt%** 복합양극의 실측 두께
  (≈80 µm), 성형 조건(300 MPa 3 min), 사이클 후 두께 변화(정압 −9.4 %, 정용적 +9.4 %).
- **[[mixing-equipment-ball-mill-thinky]] 갱신**: "Fritsch **Pulverisette 7** planetary,
  **ZrO2 용기, 300 rpm, 4 h**, Li2S+C65+LPSCl **one-step**" 한 줄 (볼·BPR 미기재).
- **[[composite-cathode-mixing-routes]] 갱신**: one-step 열에 위 조건과 조성(2:1:3) 추가.
- **[[anode-free-li2s-assb]] 갱신**: 미결 항목 4번의 **"스택 압력" 절반**을 §14.2 의 5개
  항목으로 채우고, **"집전체·Li 침적" 절반은 여전히 공백**임을 명시.
- **[[li2s-assb-reference-cell]] 갱신**: "구속 방식(볼트=정용적 / 스프링=정압)을 기록한다"
  를 미결 항목으로 추가. §14.3 의 값싼 실험 5개.
- **[[reference-cell-500-600-mahg]] 에 가설 추가**: "용량 미달의 원인 후보에 **구속 방식**이
  있다 — 정용적(강체 볼트) 구속이면 3사이클부터 감소하고 재조임으로 부분 회복한다는 서명이
  있다 (Qu 2025 Fig. 8a)." Evidence 는 **간접**(절대 용량 없음 G1)임을 명시.
- **[[one-step-vs-two-step-mixing]]**: 약한 for-evidence(one-step 으로 동작하는 셀) + 성능
  절대값 부재로 **우열 판단 불가**라고 명시.
- **`comparisons/` 후보**: §15 의 "압력 축 3논문 표" 를 `comparisons/` 한 페이지로 승격.
- **주의**: 이 digest 의 `compare:` 성능 키는 비어 있다 (측정 논문). `/compare` 화면에서
  이 행은 **조성·혼합·압력 열만** 채워진다 — 정상이다.

---

## 18. 그림 판독 기록 (무엇을 보고 무엇을 안 봤는가)

| 그림 | 봤는가 | 어디에 썼는가 |
|---|---|---|
| **Fig. 1** (a–d) | ✓ | §3.1, §3.2 — fixture 도면. 가장 오래 봤다. LVDT/스프링/압력변환기 배치 확인 |
| **Fig. 2** (a,b) | ✓ | §4 — LTO 대조셀. **본문이 "변화 없음" 이라 한 곳에서 −2 µm / −0.12 MPa 를 읽었다** (G11) |
| **Fig. 3** (a–d) | ✓ (+ 패널 c 확대) | §5.3 — 이 논문의 본체. **Li2S 첫 충전 −10 µm** 를 여기서 읽었다 |
| **Fig. 4** (a,b) | ✓ | §6 — Li_xIn −42 µm / −1.4 MPa |
| **Fig. 5** (a–d) | ✓ | §7.3 — 성분 분해. **패널마다 축 범위가 달라** 표에 명시 |
| **Fig. 6** | ✓ | §8.3 — 가설 만화 (데이터 아님) |
| **Fig. 7** (a–f) | ✓ | §9 — **두께 6개 값**과 결정 형태. 이 논문 유일의 구조 정량값 |
| **Fig. 8** (a–c) | ✓ (+ a·b·c 각각 확대) | §10 — 유지율 63/50 %, Ohmic 40→65 Ω, DRT 피크 6개 |
| **Fig. 1S** | **✗ SI 미확보** | §2.1·§12 에 "저자 주장" 으로만 인용 (fixture 무게 80–90 %) |
| **Video 1S** | **✗ SI 미확보** | §6·§12 에 "저자 주장" 으로만 인용 (Li 대칭셀 상보성) |

**본문 서술과 어긋난 그림**: 세 군데.
1. Fig. 2 — "LPSCl 부피 변화 없음" vs 실제 −2 µm / −0.12 MPa (G11).
2. Fig. 7 — "slightly" vs 실제 ±9–11 % (G12).
3. Fig. 8c — "정용적은 3사이클 후 저항 증가" vs DRT 피크 높이로는 정압 쪽이 더 높다 (§10.3).

**본문 안에서 서로 어긋난 수치**: G5(0.05 C vs C/10), G6(100 µm 분모), G8(6 mm),
G9(3 − 11 ≠ −6), G10(20 µm = 10⁻² MPa), G20(maintained well = 63 %).

**크로핑 파일**: `raw/figures/qu2025_volume-changes-li-s-solid-state-battery-components-cycling/`
— `fig_1.png` … `fig_8.png` + `figures.json` (8장, 전부 본문 그림. SI 그림 없음).

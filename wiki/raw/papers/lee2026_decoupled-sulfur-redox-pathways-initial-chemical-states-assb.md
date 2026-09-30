---
title: "Lee et al. 2026 — Decoupled sulfur redox pathways governed by initial chemical states in all-solid-state lithium–sulfur batteries (Chem. Eng. J. 546, 179625)"
description: "같은 LPSCl·MWCNT·Li–In 셀에서 출발 활물질만 S8 ↔ Li2S 로 바꾸면 산화환원 경로가 갈린다 — S8 은 충전에서 결정질 S8 을 되찾지 못하고, Li2S 는 혼합 중 생긴 단쇄 S2–4 와 가역 순환한다. 상온·무가압. 양극 비율(30:20:50)이 우리 reference cell 과 같지만 보고 용량이 Li2S 이론용량을 넘는다"
source_url: local-upload/0eafdb13-decoupled_sulfur_redox_pathways.pdf
doi: 10.1016/j.cej.2026.179625
ingested: 2026-09-30
sha256: 2695f3bc564e9a93248c03a9925a7c99be11430c4d8fb5ddef9600bd6893639f
tags: [li2s, assb, sulfide-electrolyte, composite-cathode, activation, mixing-process, li-in, carbon, units]
compare:
  system: "ASSB Li–S — S8 양극 셀과 Li2S 양극 셀을 같은 구조로 나란히 비교 (+ 비교용 액체 LSB 1종)"
  electrolyte: "Li6PS5Cl 자체 합성 (Li2S:LiCl:P2S5 = 5:2:1, 450 rpm 60 h → 550 °C 5 h), 5.3 × 10⁻³ S cm⁻¹"
  cathode: "활물질 : MWCNT : LPSCl = 3 : 2 : 5 (= 30 : 20 : 50 wt%), 바인더 없음, 4 ton 냉간 성형 펠릿"
  li2s_source: "상용 Li2S (Sigma 99.98 %) 를 CryoMill −196 °C 로 전처리 (5 Hz 5 min + 30 Hz 30 min), 수 µm. S8 셀은 상용 S8 (Sigma 99.998 %) 동일 처리"
  mixing: "two-step planetary (Fritsch P7) — ① 활물질+MWCNT 3:2, 250 rpm 6.5 h (30/10 min) ② +LPSCl 1:1, 200 rpm 1 h. 볼 제원·BPR 미기재"
  loading_mg_cm2: "1.0 (활물질 기준; 복합체 3.4) · 고로딩은 S8 셀만 1.4 / 2.3 mg cm⁻²(S), 조성 4:1:5"
  li2s_wt_pct: 30
  anode: "Li–In (질량 1:32 = 몰 1:2, ≈34 at.% Li, LiIn/In 이상영역, Thinky 2000 rpm 30 s). in situ XRD 용으로 Li 금속 셀도 별도 제작"
  first_charge: "Li2S 셀 1233.3 mAh g⁻¹(Li2S) — 방전 선행의 2번째 스텝. 충전 선행이면 672.3. 0.05 C, CC–CV, 컷오프 3.0 V vs Li–In = 3.62 V vs Li/Li⁺"
  first_discharge_mAh_gS: "1084 (S8 셀, 인쇄) · 720 (Li2S 셀, 재현 — 인쇄 502.5 mAh g⁻¹(Li2S))"
  first_discharge_mAh_gLi2S: "502.5 (Li2S 셀, 방전 선행) · 1095.9 (충전 선행의 첫 방전) · 757 (S8 셀, 재현)"
  cycle_capacity_mAh_gS: "1443 @2nd (S8 셀 최대) → 409 @250 cyc"
  cycle_capacity_mAh_gLi2S: "1250 @3rd 0.1 C → 653 @250 cyc (1250 은 Li2S 이론용량 1167 의 107 % — 인용 시 주의)"
  areal_mAh_cm2: "Li2S 셀 1.25 최대 → 0.65 @250 · S8 셀 1.44 @2nd → 0.41 @250"
  cycles: "250 (두 ASSLSB 모두). 재현 유지율 Li2S 52 % · S8 28 % (각 최대 대비)"
  temperature_C: "상온 (숫자 미기재), 외부 스택압 없음 (2032 코인셀)"
  mechanism: "초기 화학 상태가 경로를 가른다 — S8 셀: S8 → LiPS → Li2S 이나 충전에서 결정질 S8 재생성 실패(장쇄 LiPS 에서 정지). Li2S 셀: 혼합 중 Li2S–LPSCl 반응으로 생긴 단쇄 S2–4 ↔ Li2S 가역 순환, 결정질 S8·장쇄 LiPS 없음. 근거는 in situ 방사광 XRD + ex situ XRD + S 2p XPS + S K-edge XANES"
  our_axis: "활물질:SE:탄소 비율·SE·음극·온도가 우리 reference cell 과 같은 유일한 digest. 이식 대상은 '혼합 후 양극은 더 이상 pristine Li2S 가 아니다'(S 2p XPS 로 확인 가능)와 two-step 혼합 레시피, 충전 선행의 부피 수축 이점. 용량 숫자는 Li2S 이론용량 초과로 인용 불가, 3.62 V vs Li/Li⁺ 컷오프도 이식 불가"
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
## 6. §3.1 전기화학 성능 — 세 셀 비교 (Fig. 1, p.3–5) ★★

### 6.1 기준선: 액체 Li–S 셀 (Fig. 1a–c)

`[인쇄]` 방전 plateau **≈2.25 V** 와 **≈2.05 V vs Li/Li⁺** (S8 의 2단계 환원: 고전압 plateau =
가용성 장쇄 LiPS 생성, 저전압 plateau = 불용성 단쇄 LiPS → Li2S). 충전에서는 Li2S 가 LiPS 를
거쳐 S8 로 되돌아간다 (refs 48–51). 첫 방전 **711 mAh g⁻¹(S)**, 100사이클에 **~500 mAh g⁻¹(S)
이상** 유지. 그러나 **충전 용량이 방전 용량을 넘어 CE < ~80 %** — 셔틀 때문(ref 52).

`[재현]` 711 mAh g⁻¹(S) = **496 mAh g⁻¹(Li2S)** = **427 mAh g⁻¹(composite)** (S8 60 wt%)
= 면적용량 **1.21 mAh cm⁻²** (1.7 mg cm⁻²(S)).
`[도표, Fig. 1b]` 250사이클까지 방전 0.60 → 0.43 Ah g⁻¹, 충전 0.85 → 0.55 Ah g⁻¹, CE 는 70 %
언저리에서 시작해 80 % 아래에 머문다. `[도표, Fig. 1a]` 전압창 **1.5–3.0 V vs Li/Li⁺** (G9).

`[해석]` 이 셀의 역할은 "셔틀이 있는 액체계" 를 보여주는 것뿐이다. LiNO3 가 없어 CE 가 낮고,
따라서 "고체계가 셔틀을 억제한다" 는 대비는 **과장되기 쉬운 대비**다.

### 6.2 S8-ASSLSB (Fig. 1d–f)

| 항목 | `[인쇄]` mAh g⁻¹(S) | `[재현]` (Li2S) | `[재현]` (composite) | `[재현]` 이용률 /1672 | `[재현]` mAh cm⁻² |
|---|---|---|---|---|---|
| 1st 방전 (0.05 C) | **1084** | 757 | 325 | 64.8 % | 1.08 |
| 1st 충전 (0.05 C) | `[도표+재현, Fig. 6a]` **≈1340** | ≈935 | ≈402 | ≈80 % | ≈1.34 |
| 2nd 방전 (0.05 C) | **1443** | 1007 | 433 | 86.3 % | 1.44 |
| 3rd 방전 (0.1 C) | **1371** (Fig. S7a) | 957 | 411 | 82.0 % | 1.37 |
| 46사이클까지 | **>~1100** | >767 | >330 | >66 % | >1.10 |
| 250th | **409** | 285 | 123 | 24.5 % | 0.41 |
| CE | `[인쇄]` "**close to 100 % for 250 cycles**" | — | — | — | — |

`[인쇄]` 1사이클 → 2사이클 용량 증가(1084 → 1443)는 **"activation of pre-existing Li2S formed
during composite cathode preparation"** 때문이라고 명시하고, 그 근거를 §3.5 의 XPS 로 돌린다.
`[인쇄]` 방전 plateau 가 **≈1.2 V vs Li–In** (= `[재현]` 1.82 V vs Li/Li⁺) 로 낮아 "its sulfur
redox pathway differs from conventional LSBs" 라고 적는다.
`[인쇄]` 0.1 C 로 올린 직후 **충전 곡선 말단에 작은 전압 진동** — "likely associated with
interfacial instability under increased current density".
`[인쇄]` CV(Fig. 1f)의 **음극 피크가 사이클과 함께 넓어지고 이동** → 분극 증가 → 계면 열화.

`[도표, Fig. 1d]` 1st 방전은 ≈1.35 V 에서 시작해 **평탄부 없이 계속 기울어지며** 0.1 V 까지
내려간다. 충전은 ≈1.9 V 부근에 완만한 구간을 지나 3.0 V 로 치솟는다.
`[도표, Fig. 1e]` 45사이클 근처까지 ≈1.2 Ah g⁻¹ 을 유지하다가 **50–80사이클 사이에 급락**,
이후 완만히 0.4 까지. CE 점은 시종 100 % 선에 붙어 있다.
`[도표, Fig. 1f]` 1st CV 음극 피크 **≈1.05 V vs Li–In, −0.8 mA** → 2nd −0.55 mA → 3rd −0.4 mA
로 **급격히 줄고 저전위로 끌린다**. 양극 피크는 ≈2.3 V(1st) → ≈2.6 V(2,3rd), +0.45 mA 수준.

`[해석]` ★ **"CE ≈100 % 인데 용량은 3분의 1 로 준다"** 가 이 셀의 요약이다. 고체계에서 CE 는
**셔틀의 부재를 보여줄 뿐 수명을 보증하지 않는다** — 우리 셀 평가에서도 CE 를 "안정" 의 증거로
쓰면 안 된다는 직접 사례.

### 6.3 Li2S-ASSLSB (Fig. 1g–i) ★★

| 항목 | `[인쇄]` mAh g⁻¹(Li2S) | `[재현]` (S)* | `[재현]` (composite) | `[재현]` /1167 | `[재현]` mAh cm⁻² |
|---|---|---|---|---|---|
| **1st 방전** (0.05 C) | **502.5** | 720 | 151 | 43.1 % | 0.50 |
| **1st 충전** (0.05 C) | **1233.3** | 1767 | 370 | **105.7 %** | 1.23 |
| 2nd 방전 (0.05 C) | **1181** | 1692 | 354 | **101.2 %** | 1.18 |
| 3rd 방전 (0.1 C) | **1250** (Fig. S7b) | 1791 | 375 | **107.1 %** | 1.25 |
| 34사이클까지 | **>~1100** | >1576 | >330 | >94 % | >1.10 |
| 250th | **653** | 936 | 196 | 56.0 % | 0.65 |
| CE | `[인쇄]` "**close to 100 %**" | — | — | — | — |
| 유지율 | `[재현]` 653/1250 = **52.2 %** (250사이클, 0.1 C 3rd 기준) | — | — | — | — |

\* `[해석]` (S) 환산은 **"보고 용량이 전부 Li2S 로부터 왔다"** 고 가정했을 때의 값이다. G2 때문에
그 가정이 이미 깨져 있으므로 **이 열은 상한 비교용**으로만 쓴다. (S) 기준 1692·1791 은 S8 의
이론용량 1672 마저 넘는다 — 물리적으로 불가능하다는 뜻이고, 그 자체가 G2 의 재확인이다.

`[인쇄]` 저자들의 서술: 첫 방전은 낮지만(502) 2사이클에 크게 오르고(1181), 0.1 C 로 올려도
**오히려 조금 더 올라** 1250 이 되며, 250사이클 653 은 **액체셀과 S8 셀 둘 다를 같은 조건에서
능가**한다. CV(Fig. 1i)의 음극 피크 **≈0.4 V 와 ≈1.0 V vs Li–In 이 사이클 동안 변하지 않는다**
→ "stable electrochemical behavior and limited interfacial degradation".

`[도표, Fig. 1g]` ★ 1st 방전 곡선은 **≈0.55 V vs Li–In 에서 시작**해(= `[재현]` ≈1.17 V vs Li/Li⁺)
완만히 0.1 V 로 내려간다 — 짧고 낮다. 1st 충전은 0.1 V 에서 바로 솟아 **≈1.9 V 에서 어깨**를
만든 뒤 2.0 → 3.0 V 까지 **계속 기울어지며 오른다** (평탄한 plateau 가 아니다).
2nd 방전(빨강)은 ≈1.5 V 에서 시작해 ≈1.2 V 를 지나 **≈0.9 V 부근에서 꺾이고** 0.1 V 까지 간다.
`[도표, Fig. 1h]` 20사이클 근처 ≈1.25 Ah g⁻¹ 최고점 → 이후 **단조 감소**, 100사이클 ≈0.8,
250사이클 ≈0.65. **S8 셀 같은 절벽은 없다.**
`[도표, Fig. 1i]` 음극 피크 ≈1.0 V(−0.3 mA)와 ≈0.4 V(−0.2 mA), 양극 피크 ≈1.95 V 와 ≈2.3 V
(+0.15 mA). **1–3사이클이 거의 겹친다.** 전류 크기는 S8 셀의 **약 3분의 1**(세로축 −0.4~0.2 mA
vs −1.0~0.5 mA).

`[해석]` ★★ 두 가지가 우리에게 중요하다.
1. **첫 방전이 0.55 V 에서 시작한다.** 30–35 wt% 의 S2–4 가 Li2S 와 전기적·이온적으로 접촉한 채
   공존한다면 개회로 전위는 그 두 상의 평형 전위(CV 환원 피크가 있는 ≈1.0 V vs Li–In) 근처여야
   한다. 관측된 0.55 V 는 **그보다 낮다** — S–S 종이 소수이거나, 전기적으로 고립돼 있거나,
   조립 직후 이미 일부 환원됐을 가능성. **논문은 OCV 를 한 번도 논하지 않는다.**
2. **첫 방전(502)과 첫 충전(1233)의 비대칭이 극단적**이다. `[재현]` 첫 사이클 Q_dis/Q_ch =
   40.7 %. 이 셀에서 "Li 재고" 를 따지려면 **첫 충전 1233 이 어디서 왔는가**가 전부인데, 그
   값이 Li2S 이론용량을 5.7 % 넘는다 (G2) → [[anode-free-li2s-assb]] 에 그대로 옮기면 재고를
   과대평가한다.

### 6.4 세 셀 나란히 (같은 그림, 같은 조건)

| | 액체 LSB | S8-ASSLSB | Li2S-ASSLSB |
|---|---|---|---|
| 전해질 | 1 M LiTFSI DME:DOL | LPSCl | LPSCl |
| 음극 | Li 금속 | Li–In | Li–In |
| 활물질 로딩 | 1.7 mg cm⁻²(S) | 1.0 mg cm⁻²(S) | 1.0 mg cm⁻²(Li2S) |
| 1st 방전 | 711 (S) | 1084 (S) | 502.5 (Li2S) |
| 250사이클 | `[도표]` ≈430 (S) | 409 (S) | 653 (Li2S) |
| CE | **< 80 %** | ≈100 % | ≈100 % |
| 열화 형태 | 점진 + 셔틀 | **46사이클 후 절벽** | 완만한 단조 감소 |

---

## 7. §3.2 열화 기전·계면 안정성·고로딩 (p.5, 전부 SI 그림 — 본문 서술만)

### 7.1 형태 변화 (Fig. S8 SEM, Fig. S9 OM — **미확보**)

`[인쇄]` S8 복합양극: **1사이클 후 뚜렷한 균열 + 고체전해질 층으로부터의 부분 박리**. 원인은
"large volume changes associated with the S8 conversion reaction" → 입자 간 접촉과 전해질 계면
악화. Li2S 복합양극: 1사이클 후 변화가 작고 **사이클과 함께 더 치밀해진다**(denser morphology).
OM 에서도 S8 은 첫 방전 후 균열, Li2S 는 **10번째 방전 후에도 식별 가능한 변화 없음**.

### 7.2 임피던스·CV 추이 (Fig. S10, S11 — 미확보)

`[인쇄]` S8-ASSLSB 가 Li2S-ASSLSB 보다 **계면 임피던스 증가가 현저히 크다**. 50사이클 CV 에서
S8 의 ≈1 V 음극 피크는 저전위로 이동·확장(분극 증가), Li2S 는 위치·모양 변화 최소.
`[인쇄]` 결론: ASSLSB 의 용량 감소는 셔틀이 아니라 **"chemo-mechanical degradation at the
cathode–electrolyte interface"** 가 지배한다.

### 7.3 고로딩 (Fig. S12 — 미확보) ★

| 로딩 `[인쇄]` | 조성 | 1st 방전 `[인쇄]` mAh g⁻¹(S) | `[재현]` (Li2S) | `[재현]` mAh cm⁻² | 수명 `[인쇄]` |
|---|---|---|---|---|---|
| 1.0 mg cm⁻²(S) | 3:2:5 | 1084 | 757 | 1.08 | 46사이클 후 급락 |
| **1.4** mg cm⁻²(S) | 4:1:5 | **607** | 424 | 0.85 | **10사이클 내 ≈0** |
| **2.3** mg cm⁻²(S) | 4:1:5 | **505** | 352 | 1.16 | **10사이클 내 ≈0** |

`[인쇄]` "unstable discharge/charge profiles" + "reaching nearly 0 mAh g⁻¹ within 10 cycles".
결론: 로딩이 오르면 chemo-mechanical 열화·계면 불안정이 **더 심해진다**.

`[해석]` ★ 이 표가 논문의 실용성 주장을 거의 다 깎는다. **면적용량이 1 mAh cm⁻² 대에서 이미
10사이클 만에 죽는다.** 그리고 **Li2S 양극의 고로딩은 시험하지 않았다**(G8) — 즉 "Li2S 가
무가압에서 낫다" 는 결론은 **1.0 mg cm⁻², 0.12 mA cm⁻² 이라는 매우 온순한 조건에 한정**된다.
탄소가 20 → 10 wt% 로 준 것(4:1:5)도 동시에 바뀐 변수라 **로딩만의 효과가 아니다**.

---

## 8. §3.3 산화환원 동역학 — scan-rate CV (p.5–6, Fig. S13/S14 — 본문 서술만)

| 지표 `[인쇄]` | S8-복합양극 | Li2S-복합양극 |
|---|---|---|
| 피크 전류 | 전 구간에서 **더 크다** | 더 작다 |
| b 값 (ip = a·v^b) 음극/양극 | **0.521 / 0.516** | **0.546 / 0.453** |
| 해석 `[인쇄]` | 0.5 근처 또는 약간 아래 → **확산 지배**(용량성 아님) | 같음 |
| Epc 이동 (0.05 → 1 mV s⁻¹) | **−374 mV** | **−684 mV** |
| Epa 이동 | +180 mV | **+18 mV** |
| Qa/Qc | **0.92–1.01** (평행하게 감소) | 0.05 → 0.1 mV s⁻¹ 에서 Qc 2.77 → 1.70 C (**−38.6 %**), Qa 2.85 → 2.40 C (−15.8 %) → **Qa/Qc ≈1.41**; 0.2–1 mV s⁻¹ 에서는 **0.79–0.75** |
| 계면 저항 (각 scan 후 EIS) | 더 **높다** | 일관되게 **더 낮다** |

`[인쇄]` 종합: "sulfur conversion kinetics and long-term interfacial stability are governed by
**different factors**" — scan-rate CV 는 **본질적 동역학 장벽**을, 임피던스 변화는 **계면의
구조적 건전성**을 본다. Li2S 양극은 **환원이 느리지만**(더 큰 Epc 이동) 부피변화가 작아 계면을
지켜 저항이 낮다.

`[해석]` ★ 우리 축으로 옮기면: **Li2S 출발은 "동역학은 느리고 기계적으로는 착한" 쪽**이다.
전류를 올릴 때 먼저 깨지는 것은 **환원(방전)** 이지 산화(충전)가 아니다 — Li2S 셀의 Epa 이동이
18 mV 뿐이라는 것은 **충전(활성화 방향)은 오히려 전류에 둔감**하다는 뜻이다. 우리 reference
cell 에서 rate 를 올릴 때 무엇이 먼저 죽는지 예측하는 데 쓸 수 있다. 단 **b 값 0.45–0.55 는
고체계에서 "확산 지배" 로 읽기 애매하다** — 고체 내 상전환 반응에 Randles–Ševčík 류의
용액 확산 모형을 적용한 것이고, 논문은 그 전제를 논하지 않는다 `[해석]`.

---

## 9. §3.4 Li2S 양극의 첫 사이클 거동 — 이 논문의 핵심 논증 (p.5–6) ★★

`[인쇄]` 문제 제기: 액체계에서 Li2S 는 **최종 방전 생성물**이므로 더 환원될 것이 없다. 그런데
Li2S-ASSLSB 는 **첫 방전에서 502.5 mAh g⁻¹ 를 낸다.** → "the composite cathode **may not consist
solely of pristine Li2S**, but may also contain **oxidized sulfur species formed during composite
cathode preparation**."

`[인쇄]` 보조 논거 둘:
1. **첫 충전 용량 1233 mAh g⁻¹ 가 Li2S 이론용량 1167 을 넘는다** — "may result from the combined
   contribution of residual Li2S and newly formed Li2S during discharge".
2. Li2S-ASSLSB 의 전압 곡선이 **액체계에서 단쇄 황종(S2–4)을 활물질로 쓴 셀의 곡선과 닮았다**
   (refs 48,55) — 거기서는 S2–4 가 단쇄 LiPS 를 거쳐 Li2S 로 환원된다. → **작업가설**:
   "oxidized sulfur species containing **S–S bonds, analogous to S2–4**, may be present".

`[해석]` ★ 논거 1은 **논거가 아니라 문제**다 (G2). 황 보존 하에서 칭량 Li2S 1 g 의 상한은
1167 mAh 이고 "잔류 Li2S + 새로 생긴 Li2S" 를 더해도 그 상한은 안 움직인다. 이 문장은
**모순을 설명한 것이 아니라 재서술한 것**이다.

### 9.1 charge-first 프로토콜 (Fig. S15, S16 — 미확보, 본문 서술) ★

| 프로토콜 | 1st 충전 | 1st 방전 | `[재현]` 환산 |
|---|---|---|---|
| **방전 선행** (Fig. 1g) | 1233.3 (2번째 스텝) | **502.5** (1번째 스텝) | 충전 1767 mAh g⁻¹(S) 상당 |
| **충전 선행** (Fig. S15a) | **672.3** (1번째 스텝) | **1095.9** (2번째 스텝) | 충전 963 / 방전 1570 mAh g⁻¹(S) 상당 |

`[인쇄]` 해석: 충전 선행에서 첫 충전이 작은 것(672)은 **"초기 충전은 잔류 Li2S 의 산화가
지배하고, 이미 고도로 산화된 황종은 충전 용량에 거의 기여하지 않기" 때문**. 이어지는 방전에서
그 산화종까지 함께 환원되므로 **방전이 충전보다 크다**. 첫 사이클 이후에는 **출발 프로토콜과
무관하게 같은 산화환원 상태로 수렴**한다 (Fig. S15b,c 의 사이클·CV).

`[인쇄]` **충전 선행이 사이클 수명에 더 좋다** (Fig. S15b > Fig. 1h). 이유: "initial **volume
contraction** during charge... mitigate subsequent interfacial stress", 반대로 방전 선행은
즉각적인 부피 팽창으로 비가역 계면 열화를 부른다. CV 로도 확인 — **양극 sweep 선행**이면 음극
피크가 **1.01 V 에서 35사이클 동안 불변**, **음극 sweep 선행**이면 **1.07 → 0.97 V 로 이동하며
피크 전류가 크게 감소** (Fig. S16a,b).

`[해석]` ★★ **우리에게 가장 값싼 이식 후보다.** 우리 셀은 pristine Li2S 이므로 자연히
**충전 선행**이다 — 즉 이 논문 기준으로 "좋은 쪽" 프로토콜을 이미 쓰고 있다. 뒤집어 말하면
**"첫 스텝이 충전이라 부피가 수축하며 시작한다" 는 것이 Li2S 양극의 구조적 이점**이라는
주장이 하나 생긴 것이고, 이것은 [[li2s-activation-first-charge]] 에 새로 붙일 항목이다
(현재 그 개념 페이지는 활성화를 **전자/이온 접촉** 문제로만 다룬다).
단 근거는 **SI 그림 두 장(미확보)** 이고 셀 1개씩이다 (G1, G5).

---

## 10. §3.5 X선 분석 — 무엇이 무엇을 받치는가 (p.6–8) ★★

이 절이 논문의 증거 본체다. **어느 관측이 어느 주장을 받치는지 하나씩 갈라 적는다.**

### 10.1 in situ 방사광 XRD, Li–In 음극 (Fig. 2)

`[인쇄]` S8 셀에서 **S8 회절을 직접 보기 어렵다**: (i) S8 (222) 가 **Li–In (111) 과 ~23° 에서
겹치고**, (ii) S8 의 결정성이 낮아 약한 데다 **양극·전해질 양쪽에 있는 LPSCl 의 강한 신호에
묻힌다**. 그래서 **Li2S 관련 특징으로만** 추적했다.

| 관측 `[인쇄]` | 셀 | 주장 |
|---|---|---|
| **26.3°–27.7° 의 넓은 특징**이 첫 방전 plateau(~1.3 V) 이후 출현 | S8 | Li2S + 장쇄 LiPS (refs 56,57) |
| 그 강도가 **이어지는 충전에서 거의 변하지 않는다** | S8 | **"crystalline S8 is not fully re-formed once converted"** |
| 26.3°–27.7° 의 뚜렷한 넓은 특징이 **전혀 없다** | Li2S | **장쇄 LiPS 가 생기지 않는다** |
| 초기 상태의 **Li2S (111) 이 상대적으로 약하다** | Li2S | 혼합 중 **Li2S 의 부분 산화** |
| 방전에서 Li2S 피크가 **강해지고** 충전에서 **약해진다** | Li2S | 가역적 산화환원 |
| **LPSCl (311) @ 30.1° 가 강도·위치 모두 거의 불변** | 둘 다 | 전해질이 구조적으로 안정 |

`[도표, Fig. 2]` (a) S8 셀 방전 ≈11.7 h → 충전 ≈21 h. (b) 26.5–27.7° 맵은 **신호가 약하고
점묘(speckle)처럼 흩어져** 있다 — 강도 변화를 눈으로 단정하기 어렵다. (d) Li2S 셀 방전 ≈4.2 h
→ 충전 ≈13.3 h. (e) 27.05° 피크가 **처음부터 끝까지 뚜렷하게 존재**하고, 강도는 중간 구간에서
가장 진하며 충전 말기(위쪽)로 갈수록 옅어진다. (c),(f) LPSCl (311) 은 **완벽히 수직인 띠**.

`[해석]` (b)의 "broad feature" 는 `[도표]` 상 **노이즈와 구분이 어렵다**. 반면 (e)의 Li2S 피크
존재는 명백하다. 즉 **"S8 셀에 장쇄 LiPS 가 있다"** 쪽이 **"Li2S 셀에 없다"** 쪽보다 약한 근거다
(부재의 증명이 오히려 더 쉬운 역설적 상황).

### 10.2 in situ XRD, **Li 금속 음극** — 겹침을 피한 결정적 실험 (Fig. 3) ★

`[인쇄]` Li–In 이 S8 과 겹치므로 **Li 금속 음극 셀(S8/Li-ASSLSB, Li2S/Li-ASSLSB)** 을 따로 만들어
S8 (222) 를 직접 봤다.

| 관측 `[인쇄]` | 주장 |
|---|---|
| S8/Li: **S8 (222) 강도가 방전 중 점차 감소하고 충전에서 회복되지 않는다** | **비가역 전환** |
| 동시에 26.3°–27.7° 에 넓은 특징 출현 | Li2S + LiPS 생성 |
| Li2S/Li: **결정질 S8 (23.1°) 도 LiPS (26.3–27.7°) 도 나타나지 않는다** | Li2S 는 **결정질 S8 과 장쇄 LiPS 없이** 산화환원한다 |
| Li2S/Li: Li2S (111) 강도가 1st 충전 말 → 2nd 방전 초에 **감소했다가 2nd 방전에서 다시 증가** | 가역성 |
| `[인쇄]` 주의 | **1사이클이 Li 금속/LPSCl 불안정으로 조기 종료**되어 2번째 방전까지 연장 측정 (G16) |

`[도표, Fig. 3]` x축이 **0.5–3.5 V vs Li/Li⁺** 다. (a) S8/Li 방전 plateau **≈1.85 V vs Li/Li⁺**,
방전 5.8 h 후 충전이 3.5 V 까지. (b) 23.1° 띠는 **아래쪽(초기)이 가장 붉고 위로 갈수록 옅어져**
끝까지 회복되지 않는다 — 본문 주장과 일치한다. (c) 26.3–27.7° 는 넓고 얼룩덜룩하며 **왼쪽
(26.3–26.7°)에 붉은 얼룩**이 보인다. (e) **완전히 파랗다** = Li2S/Li 셀에 결정질 S8 이 한 번도
없다. (f) 27.05° 에 **매우 강한 붉은 띠**가 처음부터 끝까지.

`[해석]` ★ **(e)가 이 논문에서 가장 깨끗한 그림**이다. "Li2S 양극은 충전해도 결정질 S8 을 만들지
않는다" 는 결론이 **한 장으로 보인다** (3.62 V vs Li/Li⁺ 까지 충전했는데도). 우리 위키에서
Kim 2023 이 액체계에서 주장한 **"직접 전환 Li2S → S8"** 과 **정면으로 다르다**: 같은 "LiPS 없음"
이지만 **도착지가 S8 이 아니라 S2–4** 다. §13.3 에서 대조한다.

### 10.3 S 2p XPS (Fig. 4) ★★

`[인쇄]` 기준 결합에너지 (S 2p3/2, Fig. 4a): **S²⁻(Li2S) ≈160 eV · PS4³⁻(LPSCl) ≈161 eV ·
S⁰(S8) ≈164 eV**.

**S8 복합양극 (Fig. 4b)**
- `[인쇄]` 초기 상태에 **작은 Li2S 피크가 이미 있다** → "a small fraction of S8 is already reduced
  to Li2S **during composite cathode preparation**". 이 Li2S 는 **전기화학적으로 비활성**이며
  **첫 충전에서 활성화**되어 2사이클 용량 증가에 기여한다.
- `[인쇄]` 방전 후 Li2S 면적 증가·S8 면적 감소 + S8 피크의 **저에너지 쪽 소폭 이동**(LiPS 생성).
- `[인쇄]` 충전 후 Li2S 면적 감소, **LiPS 관련 성분 증가**. Fig. 3b 의 S8 무회복과 합치면
  **"방전: S8 → (LiPS) → Li2S / 충전: Li2S → LiPS (S8 재생성 없음)"**.

**Li2S 복합양극 (Fig. 4c)** ★
- `[인쇄]` 초기 상태에 Li2S·LPSCl 외에 **더 높은 결합에너지의 추가 피크**가 있다. 그중 **~163 eV**
  는 S8 의 S 2p3/2 와 거의 겹친다. 그러나 **XRD 에 S8 피크가 없으므로**(Fig. 3e, S18),
  이것은 결정질 S8 이 아니라 **"Li2S 와 LPSCl 이 복합양극 제조 중 반응해 생긴 S–S 결합 황종"**
  이고, 전기화학 작업가설에 따라 **S2–4** 로 귀속한다.
- `[인쇄]` 방전 후 S2–4 면적 **감소**(+저에너지 이동), Li2S 면적 **증가**. 충전 후 **반대**.
  → "S2–4 formed during composite cathode preparation is reduced to Li2S during discharge and
  oxidized back to S2–4 during charge."

**"initial chemical state" 의 정의** `[인쇄, p.8]` — 논문이 직접 정의한다:
> 전기화학 이전에 복합양극에 존재하는 **황 화학종 전체**. pristine 활물질(S8 또는 Li2S)뿐 아니라
> **제조 중 활물질–고체전해질 반응으로 생긴 계면 황종**(S8 양극의 Li2S, Li2S 양극의 S2–4)을 포함.
> 단순한 산화수가 아니라 **계면 speciation** 을 뜻한다.

**LPSCl 분해가 아니라는 반증** `[인쇄]` — Cl 2p XPS (Fig. S19): 합성된 LPSCl 에도, 두 복합양극
에도 **LiCl(LPSCl 의 주 분해생성물, refs 4,59) 신호가 없다.** 복합양극의 Cl 2p 는 pristine 대비
**고에너지 쪽으로 약간 이동** → 국소 화학환경 변화. XRD(Fig. S3a)에도 분해생성물 없음.
→ "the formation of Li2S and S2–4 is **not associated with LPSCl decomposition** but is more likely
due to **interfacial reactions between active materials and LPSCl**".

`[도표, Fig. 4]` ★ 중요한 눈 관측: **Li2S 복합양극의 초기 상태(c 아래)에서 주황색(S–S) 성분의
면적이 파란색(Li2S) 성분보다 훨씬 크다.** S8 복합양극 초기(b 아래)와 비슷한 정도로 크다.
방전 상태(c 중간)에서 파란색이 커지고 주황이 줄며, 충전 상태(c 위)에서 되돌아간다 — 본문의
정성 서술과 일치한다.

`[해석]` ★★ 두 가지를 갈라야 한다.
1. **정성 결론("혼합 중 S–S 종이 생겼고 그것이 가역적으로 오간다")은 XPS 가 잘 받친다.** 세
   상태의 면적 변화 방향이 전기화학과 맞고, Cl 2p 반증까지 붙였다.
2. **정량("30–35 wt%")은 XPS 가 전혀 받치지 않는다.** XPS 는 **표면 수 nm** 이고, 면적비를
   벌크 분율로 환산하지 않았다. 오히려 `[도표]` 로 보이는 표면의 S–S 우세는 **30 %보다 훨씬
   많아 보인다** — 즉 "표면에 몰려 있다" 는 그림과 더 어울린다. 논문은 이 긴장을 다루지 않는다
   (G4, G13).
3. **"LPSCl 분해가 아니다" 는 논증에는 구멍이 있다.** LiCl 부재는 **염소 경로 분해**만 배제한다.
   Li2S + LPSCl → S–S 종이 생기려면 **황이 산화**돼야 하고 그 전자는 어디론가 가야 한다
   (PS4³⁻ → P2Sx 등). P 2p 스펙트럼이 **없다** — 이 논문에서 가장 아쉬운 누락이다 `[해석]`.

### 10.4 S K-edge XANES (Fig. 5)

`[인쇄]` 기준 피크 (ref 60): **pristine S8 = 2474.5, 2481.5 eV**; **pristine Li2S = 2475, 2477.8,
2485.5 eV**. LPSCl 이 사이클 동안 구조적으로 안정하므로(Fig. 2c,f) 변화는 **황 활물질에만**
귀속된다는 전제를 깐다.

`[인쇄]` **초기 복합양극의 XANES 가 pristine 물질의 것과 다르다** → LPSCl 과의 계면 상호작용으로
황 환경이 바뀌었다.

**S8 복합양극 (Fig. 5a)** — 방전 후 스펙트럼이 pristine Li2S 를 닮는다(환원). **2477.8 eV 의
Li2S 특징이 특히 0.4 V 위에서 커진다** — 방전 용량 대부분이 0.4 V 위에서 나온다는 Fig. 1d 와
일치. 충전에서 그 특징이 줄고 **새 황종 특징이 전압과 함께 커진다**. Li2S → S8 산화가 불완전
하므로 그 특징은 **결정질 S8 이 아니라 LiPS** 로 귀속 (S–S 를 가진 LiPS 의 XANES 는 S8 과
닮았다는 선행연구 refs 61,62 인용).

**Li2S 복합양극 (Fig. 5b)** — 방전에서 Li2S 특징이 **뚜렷해지고**(선존 S2–4 의 환원), 충전에서
사라지며 황종 특징이 나타난다. 결정질 S8·장쇄 LiPS 의 뚜렷한 서명이 없으므로 그 황종은
**S–S 를 가진 S2–4** 로 본다. `[인쇄]` **~2472 eV 의 XANES 특징은 단쇄 Li2S2 및 S2–4 에 귀속**
(refs 63,64) 되는데, 그 피크가 **방전에서 줄고 충전에서 다시 나타난다** (Fig. S20 — 미확보).
3.0 V 의 스펙트럼은 Li2S 의 것과 다르고 **S2–4 의 S–S 와 맞는 특징**을 보인다.

`[도표, Fig. 5]` (a) **초기 상태(검정)와 pristine S8(노랑 점선)이 확연히 다르다** — pristine S8
에 있는 2478 eV 부근의 깊은 골과 2481.5 eV 의 뚜렷한 봉우리가 초기 복합양극에는 **뭉개져
있다**. (b) **초기 상태(검정)는 pristine Li2S(하늘색 점선)와 상당히 닮았다** — 2475·2477.8·
2485.5 세 특징이 다 있고, 다른 점은 2473 eV 부근 어깨가 조금 더 뚜렷한 정도다. 충전(3.0 V,
주황)에서는 2473–2475 에 **새 이중 구조**가 생긴다.

`[해석]` ★ (b)의 초기 상태가 pristine Li2S 와 그렇게 닮았다는 것은 **XPS 가 보여준 표면의 큰
S–S 몫과 어울리지 않는다.** 두 관측을 동시에 만족하는 가장 단순한 그림은 **"S–S 종이 Li2S
입자의 표면 껍질에 있고 벌크 분율은 작다"** 이다 — 그러면 **30–35 wt% 라는 벌크 분율 주장이
약해진다**. XAS 검출 모드를 적지 않아(G13) 이 판정을 논문 안에서 할 수 없다.

---

## 11. §3.6 제안된 기전과 그 정량 논증의 검산 (p.8–9, Fig. 6) ★★

### 11.1 논문이 그린 두 경로 (Fig. 6)

**S8-ASSLSB (Fig. 6a)** `[인쇄]`
- 방전: S8 → (LiPS) → Li2S
- 충전: Li2S → **장쇄 LiPS 에서 멈춤** (결정질 S8 로 돌아가지 않음)
- 혼합 중 이미 일부 S8 이 Li2S 로 환원돼 있고, 그 **비활성 Li2S 가 첫 방전 용량을 낮춘다**.
  첫 충전에서 그 선존 Li2S + 방전으로 생긴 Li2S 가 **함께 장쇄 LiPS 로 산화**되어 2사이클
  방전 용량이 커진다.

**Li2S-ASSLSB (Fig. 6b)** `[인쇄]`
- 초기 양극 = **잔류 Li2S + 제조 중 생긴 산화 황종(S2–4 로 추정)**
- 방전: S2–4 → Li2S (첫 사이클의 측정 가능한 방전 용량의 정체)
- 충전: Li2S → S2–4. **결정질 S8 을 거치지 않는 가역 순환**
- `[인쇄]` 단서: "although their exact chemical identity cannot be unambiguously determined"

`[도표, Fig. 6]` x축이 **용량이 아니라 시간(h)** 이다. (a) S8: 방전 ≈13 h, 충전 ≈16 h(총 ≈29 h).
(b) Li2S: 방전 ≈8.7 h, 충전 ≈21.3 h(총 ≈30 h). 라벨은 (a) S8 → LiPSs → Li2S → **Long-chain
LiPSs**, (b) **S2–4** → Li2S → **Short-chain LiPSs** → **S2–4**.
`[재현]` 시간 → 용량: (a) 방전 13 h × 0.05 × 1672 = **1087** ≈ 인쇄값 1084 ✓; 충전 16 h × 83.6 =
**≈1340**(G14). (b) 방전 8.7 h × 0.05 × 1167 = **508** ≈ 502.5 ✓; 충전 21.3 h × 58.35 = **1243**
≈ 1233 ✓. **시간축과 인쇄된 용량이 서로 맞는다** — 좋은 내부 일관성이다.

### 11.2 논문의 정량 논증 — 그대로 옮기고, 검산한다 ★★

`[인쇄, p.9]` 방전 선행:
1. 첫 방전 **502.5 mAh g⁻¹**. 황종의 이론용량을 **1672 mAh g⁻¹ (Sn 기준)** 으로 보면
   → 복합양극 중 **약 30–35 wt% 의 산화 황종**의 환원에 해당.
2. 따라서 초기 양극 = **잔류 Li2S ~65–70 wt% + S2–4**.
3. 첫 충전 **1233.3 mAh g⁻¹**. 잔류 Li2S 65–70 wt% 의 산화분은 **~760–820 mAh g⁻¹**
   (1167 기준). 나머지 **~410–470 mAh g⁻¹** 는 **첫 방전에서 새로 생긴 Li2S 의 산화**.
   그 값이 첫 방전 502.5 보다 **작으므로** 정량적으로 일관된다.

`[인쇄, p.9]` 충전 선행:
4. 첫 충전 **672.3 mAh g⁻¹** < 잔류 Li2S 완전 산화 기대치 760–820 → **잔류 Li2S 의 일부만** 참여.
5. 이어진 방전 **1095.9 mAh g⁻¹**. S2–4 분(30–35 wt%)의 환원 기대치 **~500–585** + 첫 충전에서
   생성된 S2–4 분(672.3) = **~1170–1250** 으로, 관측치 1095.9 와 "합리적으로 일치".

**`[재현]` 검산 — 세 군데가 어긋난다.**

| # | 논문의 수 | 이 세션의 검산 | 문제 |
|---|---|---|---|
| A | 502.5 / 1672 = 30.0 % | 산술은 맞다 | 그러나 **1672 는 "단체 황 1 g" 의 용량**이다. 이 30 wt% 를 **칭량한 Li2S 질량의 30 %** 에 적용하면, 1 g 당 황 함량이 0.30 + 0.70 × 0.698 = **0.789 g** 이 된다. pristine Li2S 1 g 의 황은 **0.698 g** 이다. **황이 0.09 g 늘었다** — 혼합 중 LPSCl 에서 황이 넘어오지 않는 한 불가능하다. |
| B | 0.65–0.70 × 1167 = 758.6–816.9 | 산술 맞다 (760–820 ✓) | — |
| C | 이 모형의 총 이론용량 | `[재현]` 0.30 × 1672 + 0.70 × 1167 = **1319 mAh g⁻¹** | 논문은 이 숫자를 적지 않는다. 적었다면 **관측된 1250(0.1 C)이 이론의 95 %** 라는 비정상적으로 높은 이용률이 드러난다. 황 보존을 지키는 올바른 상한은 **1167** 이고, 그 기준으로는 **1250 이 107 %** 다 (G2). |
| D | 충전 선행 합계 1170–1250 vs 관측 1095.9 | 산술 맞다 | 단 **계산이 자기 참조적**이다 — S2–4 분율 자체가 방전 선행의 첫 방전 용량에서 나왔으므로, 이 "검증" 은 **같은 가정을 두 번 쓴 것**에 가깝다. |

`[해석]` ★★ 정리하면: **"초기 상태에 S–S 종이 있다" 는 정성 주장은 XPS·XANES·XRD 가
독립적으로 받친다. 그러나 "30–35 wt%" 라는 수, 그리고 1181·1233·1250 이라는 용량은
질량수지를 맞추지 않는다.** 가장 그럴듯한 설명 후보는 셋이고, 논문은 셋 다 검토하지 않는다:
(i) 황이 LPSCl 에서 양극 활물질 쪽으로 넘어왔다(그러면 SE 가 소모되고 있다),
(ii) 3.62 V vs Li/Li⁺ 충전에서 **LPSCl 자체가 산화되어 전하를 낸다**(G3),
(iii) 0.72 V vs Li/Li⁺ 까지의 깊은 방전에서 **MWCNT·LPSCl 의 비-황 환원**이 섞인다.
(ii)와 (iii)은 둘 다 **컷오프를 좁히면 사라지는지**로 반증 가능한데, 그 실험이 없다.

---

## 12. 결론 절이 스스로 적은 것 (p.10)

`[인쇄]` 핵심 문장들:
- "redox reactions of S8 and Li2S in the LPSCl solid-state electrolyte, particularly under
  **unpressurized conditions at room temperature**, deviate significantly from the conventional
  S8–Li2S conversion observed in liquid systems **and in ASSLSBs operated under external pressure
  and/or elevated temperature**."
- S8: "S8 is reduced to Li2S via LiPSs; however, **the reverse regeneration of S8 is kinetically
  hindered**."
- Li2S: "operates through a **reversible conversion between Li2S and short-chain sulfur species
  (S2–4)**, without involving long-chain LiPSs or S8."
- 설계 지침: "**controlling the initial chemical state of sulfur to favor the formation of
  short-chain sulfur species can facilitate Li2S oxidation**", 장쇄 LiPS 를 억제하고 단쇄를
  안정화하는 양극 설계가 부피 변형을 줄이고 계면을 안정화한다.
- 한계 자인: "**achieving higher sulfur loadings and ensuring compatibility with other
  solid-state electrolytes remain important challenges**."

`[해석]` ★ 설계 지침 한 줄이 우리에게 직접적이다 — **"단쇄 황종이 생기게 초기 상태를 조절하면
Li2S 산화(= 첫 충전 활성화)가 쉬워진다."** 이 논문 안에서 그 지침을 **의도적으로 실행한 실험은
없다**(S2–4 는 의도가 아니라 부산물이었다). 즉 **검증되지 않은 처방**이다. 그러나 우리
[[composite-cathode-mixing-routes]] 의 언어로 번역하면 **"혼합 조건으로 Li2S 표면의 부분 산화
정도를 조절한다"** 는 새로운 조작 변수가 된다.

---

## 13. 우리 연구와의 접점 ★★

### 13.1 이식 가능 / 불가

| 이 논문의 것 | 우리에게 | 이유 |
|---|---|---|
| **활물질 : 탄소 : LPSCl = 30 : 20 : 50 wt%** | **○ 직접 대조군** | 우리 1단계 비율과 **같다**. 탄소 종류(MWCNT vs AB)와 혼합 경로만 다르다 → **탄소 종류 하나만 바꾼 비교가 성립**한다 |
| **two-step 혼합**: (활물질+C) 250 rpm 6.5 h → (+SE) 200 rpm 1 h, Fritsch P7 | **○ 레시피로** | 단 볼·BPR·자 미기재(G10). rpm·시간은 그대로 쓸 수 있는 출발점 |
| **Li2S cryo-milling** (−196 °C, 5 Hz 5 min + 30 Hz 30 min) | **△** | Li2S 는 취성이라 상온에서도 깨진다는 것이 이 논문 자신의 설명이다. cryo 의 이득이 분리돼 있지 않다 |
| **Li–In 0.62 V vs Li/Li⁺ 기준** + 조성(질량 1:32, 몰 1:2, 34 at.% Li, LiIn/In 이상영역) | **○** | 우리 전압 기준 표기의 근거로 인용 가능 (단 2차 인용). Thinky 2000 rpm 30 s 제조법도 |
| **초기 상태가 pristine 이 아니다** (혼합 중 Li2S–LPSCl 반응 → S–S 종) | **○○ 가장 중요** | 우리 pristine Li2S 양극에도 같은 일이 일어나고 있을 수 있다. 확인은 **혼합 직후 분말의 S 2p XPS** 하나면 된다 |
| **첫 스텝이 충전인 편이 수명에 낫다** (부피 수축 선행) | **○ 가설로** | 우리는 이미 충전 선행이다. "그것이 이점" 이라는 새 해석을 얻는다. 근거는 SI 미확보 |
| **충전 컷오프 3.0 V vs Li–In (3.62 V vs Li/Li⁺)** | **✗ 그대로 쓰면 안 된다** | G2·G3. 이 컷오프에서 나온 용량은 비-황 기여를 포함할 수 있다. 우리 컷오프 선택의 근거로 쓸 수 없다 |
| **보고된 용량 숫자(1181/1233/1250)** | **✗ 인용 금지** | Li2S 이론용량 초과 (G2) |
| **무가압 운전** | **△ 참조만** | 코인셀 스프링 압력 미기재(G6), 로딩 1.0 mg cm⁻² 한정(G8) |
| **고로딩 결과** | **✗ Li2S 계에는 없다** | S8 계만, 그리고 10사이클 내 사망 |
| **"S2–4 를 만들면 Li2S 산화가 쉬워진다"** | **△ 가설로만** | 논문 안에 그것을 **의도적으로 조절한 실험이 없다** |

### 13.2 열린 질문 카드에 붙는 자리

**[[reference-cell-500-600-mahg]]**
- **H1(활성화 제한)에 정밀화 근거.** 이 논문은 **3.62 V vs Li/Li⁺ 까지 충전하면 pristine Li2S
  출발 양극에서 1233 mAh g⁻¹(Li2S) 의 첫 충전이 나온다**고 보고한다. 우리 위키의 다른 digest
  (`raw/papers/zhang2026_…`)에서 **같은 pristine Li2S 가 3.0 V vs Li 컷오프에서 첫 충전 ≈350,
  첫 방전 ≈270 mAh g⁻¹(Li2S)** 에 그친 것과 **정면 대비**된다 → §13.3.
- **H3(입자 제한)에는 근거가 약하다** — 입도 숫자가 없다(G17).
- **새 가설 후보 H5(혼합 중 계면 화학 변화)**: 첫 사이클 거동을 정하는 것은 입자 크기나 탄소
  접촉만이 아니라 **혼합 중 활물질–SE 반응으로 생긴 계면 황종**이라는 축. 이 논문이 그 축의
  첫 직접 근거다. `[해석]` 카드에 H5 를 추가할지는 컴파일 단계의 판단.
- **H4(단위 착시)에 경고 사례.** 이 논문은 분모를 본문에 글자로 안 쓰고(축 라벨 `Ah g⁻¹`),
  1 C 계산식으로만 역산 가능하며, 그 결과가 **이론용량을 넘는다**. 남의 500–600 을 인용할 때
  **분모와 이론용량 대비 비율을 같이 봐야 한다**는 것을 보여준다.

**[[one-step-vs-two-step-mixing]]**
- **H2(SE 보호)에 부분 반대 근거**: two-step 으로 SE 를 **저에너지 2단계(200 rpm, 1 h)** 에만
  넣었는데도 **Li2S–LPSCl 반응이 일어났다**. "SE 를 나중에 약하게 넣으면 보호된다" 는 전제가
  **화학 반응까지 막지는 못한다**. 단 one-step 대조군이 없어 **순서의 우열은 말할 수 없다**(G11).
- 동시에 **H1(two-step 우세, 계면 이유)에 약한 찬성**: 탄소를 먼저 6.5 h 갈아 활물질에 입힌
  이 경로에서 1.0 mg cm⁻² · 상온 · 무가압으로 1000 mAh g⁻¹ 대가 나왔다 (숫자 자체는 G2 유의).

### 13.3 ★ 세 digest 나란히 놓기 — pristine Li2S 는 어느 경로에 있는가

| | **Lee 2026** (이 논문) | **Zhang 2026** (`raw/papers/zhang2026_…`) | **Kim 2023** (`raw/papers/kim2023_…`) |
|---|---|---|---|
| 계 | ASSB, LPSCl, Li–In, 상온, 무가압 | ASSB, LPSCBr, **anode-free Na 집전체**, 1–4 MPa | **액체** 에테르 + LiNO3, Li 금속 |
| 활물질 | **pristine 상용 Li2S**(cryo-mill) | **pristine 상용 Li2S** vs Li2S–PI3 처리 | 상용 micro Li2S |
| 탄소 | MWCNT **20 wt%** | C **10 wt%** | Gr/CNT **25 wt%** |
| 충전 컷오프 | **3.0 V vs Li–In = 3.62 V vs Li/Li⁺** | **3.0 V vs Li**(Na 위 석출 Li 기준) | 3.6 V vs Li/Li⁺ |
| pristine Li2S 첫 충전 | `[인쇄]` **1233 mAh g⁻¹(Li2S)** (방전 선행) / **672** (충전 선행) | `[도표]` **≈350** | `[도표]` 활성화 완료 |
| pristine Li2S 첫 방전 | 502.5(방전 선행, 활성화 **전**) / **1095.9**(충전 선행, 활성화 **후**) | **≈270** | 1150 mAh g⁻¹(S) = 800 (Li2S) |
| 기전 주장 | Li2S ↔ **S2–4**, S8 없음 | LiI·비정질 골격이 과전압을 낮춘다 | **직접 전환 Li2S → S8**, LiPS 없음 |

`[해석]` ★★ **이 표가 이 digest 의 가장 값진 산출물이다.**
- **같은 pristine 상용 Li2S 인데 활성화 후 첫 방전이 ≈270 (Zhang) vs 1095.9 (Lee) 로 4배 차이**
  난다. 비교 가능한 쌍은 **"활성화(충전) 후의 방전"** 끼리다: Zhang 의 충전선행 ≈270,
  Lee 의 충전선행 **1095.9**.
- 가장 크게 다른 변수 셋: (a) **충전 컷오프 3.0 vs 3.62 V vs Li/Li⁺ — 0.62 V 차이**,
  (b) **탄소 10 vs 20 wt%**, (c) **혼합 경로**(Zhang 은 Li2S+PI3 고에너지 1400 rpm, pristine
  대조군은 같은 조건 / Lee 는 two-step 250 → 200 rpm).
- **가장 유력한 한 줄** `[해석]`: **pristine Li2S 의 첫 충전 활성화는 컷오프 전위에서 잘린다.**
  Zhang 의 pristine LSV 산화 피크가 **3.05 V** 인데 컷오프가 **3.0 V** 라 활성화를 끝내지 못하고,
  Lee 는 **3.62 V** 까지 밀어 활성화를 끝낸다 — **그 대가로 SE 산화가 섞여 이론용량을 넘는
  용량이 나온다**(G2, G3). 즉 두 논문은 **같은 벽의 양쪽 면**을 보여준다:
  *컷오프를 낮추면 활성화가 안 되고, 높이면 SE 가 탄다.*
- **우리에게 가장 중요한 한 줄**: 우리 reference cell 이 500–600 mAh g⁻¹ 에서 막힌다면,
  그 값은 **Zhang 의 270 과 Lee 의 1096 사이**에 있다 — **컷오프–SE 안정성 창이 우리 용량을
  직접 정하고 있을 가능성**이 크다. 이것은 H1 을 **"활성화가 덜 된다"** 에서 **"활성화를 끝낼
  전위가 SE 산화 전위보다 높다"** 로 날카롭게 만든다.
- **Kim 2023 과의 대조**: 액체계에서 "LiPS 없이 Li2S → S8 직접 전환" 이 관측됐다면, 고체계
  이 논문에서는 **"LiPS 도 S8 도 없이 Li2S → S2–4"** 다. **둘 다 LiPS 를 건너뛰지만 도착지가
  다르다.** [[li2s-activation-first-charge]] 가 지금 "고체계에서는 직접 전환이 유일 경로" 라고
  적은 문장은 **도착지를 S8 로 단정해서는 안 된다**는 수정이 필요하다 (컴파일 단계 과제).

### 13.4 가장 값싼 다음 실험 (우리 셀에서)

1. **혼합 직후 복합양극 분말의 S 2p XPS 한 장.** ~163 eV 의 S–S 성분이 보이면 우리 양극도
   pristine 이 아니다. 비용: 시료 하나. **이 논문의 중심 주장을 우리 계에서 바로 확인**한다.
2. **컷오프 사다리**: 3.0 / 3.2 / 3.4 / 3.6 V vs Li/Li⁺ 로 첫 충전만 바꾼 4셀. 첫 충전 용량과
   2사이클 방전을 본다. `[해석]` Lee↔Zhang 대비가 예측하는 것: **첫 충전 용량이 컷오프에 거의
   선형으로 붙고, 어느 지점부터 2사이클 방전이 따라 오르지 않는다**(= SE 산화 구간 진입).
3. **혼합 2단계의 강도·시간 변주**(200 rpm 1 h vs 더 약하게/짧게) 후 XPS + 첫 사이클. G11 이
   비워둔 자리를 우리가 채운다.

---

## 14. 비판

1. **★ 보고 용량이 이론용량을 넘는데 논문이 그것을 문제로 다루지 않는다** (G2). 1233 만
   언급하고 "잔류 + 새로 생긴 Li2S" 로 넘어가는데, 그것은 황 보존을 복구하는 설명이 아니다.
   2nd 방전 1181(101 %)과 0.1 C 1250(107 %)은 **아예 언급이 없다**.
2. **★ 3.62 V vs Li/Li⁺ 충전에서 LPSCl 산화 기여를 분리하지 않았다** (G3). "LPSCl (311) 불변 +
   LiCl 부재" 로 안정성을 주장하는데, 둘 다 **비정질 산화생성물에 눈이 없다**. 서론이 스스로
   "큰 과전압이 전해질 분해를 유발한다" 고 써 놓고 그 분해를 재지 않는다.
3. **★ 정량 논증이 질량수지를 맞추지 않는다** (G4, §11.2 A·C). 30 wt% 를 "Sn" 으로 잡아 칭량
   1 g 의 황 함량을 0.698 → 0.789 g 으로 늘린다. 이 모형의 총 이론용량 1319 를 논문은 적지 않고,
   적었다면 이용률 95 % 라는 비현실적 수가 드러난다.
4. **관측의 깊이가 갈라진다** (G13). 표면 민감한 XPS 는 S–S 가 크고, 벌크 쪽 XANES 초기
   스펙트럼은 pristine Li2S 와 거의 겹친다. 검출 모드를 안 적어 "표면 껍질인가 벌크 분율인가" 를
   논문 안에서 판정할 수 없다 — 그런데 결론은 **벌크 분율(wt%)** 로 쓴다.
5. **P 2p XPS 가 없다.** Li2S + LPSCl → S–S 종이 생기려면 인 쪽 산화수가 움직여야 한다.
   Cl 2p 만 보고 "LPSCl 분해가 아니다" 라고 한 것은 **염소 경로만 배제**한 것이다.
6. **셀이 전부 1개**로 보인다 (G5). 46사이클/34사이클이라는 열화 전환점이 계통인지 알 수 없다.
7. **"안정" 의 정체**: 두 ASSLSB 다 CE ≈100 % 지만 **S8 은 250사이클에 28 %, Li2S 는 52 %** 만
   남는다 `[재현]`. 초록의 "stable cycling with a capacity of ~1200 mAh g⁻¹ and near-unity
   Coulombic efficiency" 는 **~1200 이 34사이클짜리**라는 사실을 가린다.
8. **초록의 S8 수치가 2사이클 값**이다. "delivers a high discharge capacity of ~1400" 의 1443 은
   **2사이클**이고 첫 방전은 1084 다.
9. **고로딩은 S8 만, 그것도 10사이클 내 사망**(G8). "무가압·상온 실용성" 이라는 틀과
   1.0 mg cm⁻² · 0.12 mA cm⁻² 라는 실제 조건 사이의 거리가 크다.
10. **액체셀 기준선이 약하다**. LiNO3 없는 1 M LiTFSI DME:DOL 셀의 CE < 80 % 를 상대로
    "고체계가 셔틀을 억제한다" 를 보이는 것은 **쉬운 비교**다.
11. **좋은 점도 분명히 적는다**: (i) **Fig. 3e** — Li 금속 음극으로 바꿔 겹침을 피하고 "결정질
    S8 이 한 번도 안 생긴다" 를 한 장으로 보인 설계는 깔끔하다. (ii) **charge-first / discharge-
    first 대조**는 초기 상태 가설을 검증하는 영리한 전기화학 실험이다. (iii) **Cl 2p 반증**을
    스스로 붙인 태도. (iv) in situ XRD·XPS·XANES 세 관측이 **같은 방향**을 가리킨다.
    (v) 혼합·성형 조건을 (볼 제원 빼고) **꽤 상세히** 적었다 — 우리가 재현을 시도할 수 있다.

---

## 15. 이 저장소가 가져갈 것

1. **"pristine 은 혼합 후에도 pristine 인가" 라는 질문 자체.** 우리 [[composite-cathode-mixing-routes]]
   표에 **"혼합 후 활물질–SE 계면 반응 여부(XPS S 2p)"** 열을 추가할 근거.
2. **Lee ↔ Zhang 의 컷오프 대비**(§13.3): pristine Li2S 활성화가 **컷오프와 SE 산화 전위 사이에
   끼어 있다**는 가설. [[reference-cell-500-600-mahg]] 의 H1 을 날카롭게 만든다.
3. **고체계의 도착지가 S8 이 아닐 수 있다**: [[li2s-activation-first-charge]] 의 "직접 전환"
   서술을 **S8 / S2–4 두 가능성**으로 나눠 적어야 한다.
4. **CE ≈100 % 가 수명을 보증하지 않는다**는 고체계 직접 사례 (S8 셀: CE 100 %, 용량 28 % 잔존).
5. **Li–In 0.62 V vs Li/Li⁺ 의 출처 있는 기재** (2차 인용이지만 조성·상영역과 함께).
6. **동역학의 비대칭**: Li2S 양극은 전류를 올릴 때 **환원(방전)이 먼저 깨진다**(Epc −684 mV vs
   Epa +18 mV). rate 시험 설계에 쓸 것.
7. **주의 문구**: 이 digest 의 Li2S 셀 용량은 **이론용량을 넘으므로 비교표에 넣을 때 반드시
   "이론 대비 %" 를 함께** 적는다.

---
## 16. 그림 판독 기록

### 16.1 본문 그림 — **여섯 장 전부 직접 판독했다**

| 그림 | 봤나 | 어디에 썼나 | 그림에서만 읽은 것 `[도표]` |
|---|---|---|---|
| **Fig. 1** (전기화학 9패널) | **✓ 본다** | §6.1–6.4 | 액체셀 전압창 1.5–3.0 V vs Li/Li⁺ (본문과 불일치, G9) · S8 CV 음극 피크 1.05 V, −0.8 → −0.4 mA · Li2S CV 음극 0.4/1.0 V, 양극 1.95/2.3 V, 1–3사이클 중첩 · **Li2S 셀 방전 시작 전압 ≈0.55 V vs Li–In** · S8 사이클의 50–80사이클 절벽 · Li2S 사이클의 단조 감소 · CV 전류 크기 비 ≈3:1 |
| **Fig. 2** (in situ XRD, Li–In) | **✓ 본다** | §10.1 | S8 셀 방전 11.7 h/충전 21 h, Li2S 셀 4.2 h/13.3 h · (b) 맵이 **점묘처럼 흩어져 판정이 어렵다** · (e) 27.05° 피크가 **전 구간 존재** · (c),(f) LPSCl 띠는 완전히 수직 |
| **Fig. 3** (in situ XRD, Li 금속) | **✓ 본다** | §10.2 | x축 0.5–3.5 V **vs Li/Li⁺** · S8/Li 방전 plateau **≈1.85 V vs Li/Li⁺** (Li–In 셀의 1.2 V + 0.62 와 일치, §3.4 검증) · (b) 23.1° 강도 단조 감소·무회복 · **(e) 전면 파랑 = 결정질 S8 전무** · (f) 27.05° 강한 띠 지속 |
| **Fig. 4** (S 2p XPS) | **✓ 본다** | §10.3 | **Li2S 복합양극 초기 상태에서 S–S(주황) 면적이 Li2S(파랑)보다 훨씬 크다** — 벌크 30 wt% 와 어울리지 않는다 · 방전/충전에서 두 성분이 반대로 움직인다 |
| **Fig. 5** (S K-edge XANES) | **✓ 본다** | §10.4 | (a) 초기 S8 복합양극이 pristine S8 과 **확연히 다르다**(2478 골·2481.5 봉우리가 뭉개짐) · **(b) 초기 Li2S 복합양극은 pristine Li2S 와 상당히 닮았다** — XPS 와 어긋나는 지점 · 충전 3.0 V 에서 2473–2475 새 이중 구조 |
| **Fig. 6** (제안 기전) | **✓ 본다** | §11.1 | **x축이 시간(h)** · S8 13/16 h, Li2S 8.7/21.3 h · `[재현]` 시간×C-rate×이론용량이 인쇄된 용량과 일치 · 라벨 "Long-chain LiPSs"(S8) vs "Short-chain LiPSs → S2–4"(Li2S) |

### 16.2 SI — **한 장도 보지 못했다** (G1)

SI PDF 를 받지 못했다. 아래는 본문이 인용한 SI 그림과, 이 digest 가 그 그림에 **의존하는 서술**이다.
**전부 본문 문장에서 온 `[인쇄]` 이며, 그림을 확인한 적이 없다.** SI 확보 시 최우선 재검증 대상에
★ 를 붙였다.

| SI 그림 | 본문이 말하는 내용 | 이 digest 의 위치 | 재검증 |
|---|---|---|---|
| Fig. S1 | 세 셀(액체·S8·Li2S)의 단면 모식도 | §4.1 | |
| Fig. S2 | in situ XRD 용 개조 코인셀 구성 | §5 | |
| Fig. S3a,b | LPSCl XRD + 이온전도도 5.3 mS cm⁻¹ | §3.1 | |
| Fig. S4a–d | cryo-mill 후 S8·Li2S XRD·SEM (수 µm, S8 응집) | §3.2 | ★ 입도(G17) |
| Fig. S5 | 복합양극 EDS 맵 (균일 분산) | §3.3 | |
| Fig. S6 | Li–In 분말 XRD (Li–In + In 공존) | §3.4 | |
| Fig. S7a,b | 0.1 C 3사이클 곡선 (S8 1371 / Li2S 1250) | §6.2, §6.3 | ★ 분모·곡선 모양 |
| Fig. S8 | 사이클 후 양극 SEM (S8 균열·박리 / Li2S 치밀화) | §7.1 | ★ |
| Fig. S9 | 광학현미경 (S8 첫 방전 후 균열 / Li2S 10사이클 무변화) | §7.1 | |
| Fig. S10 | EIS 추이 (S8 계면 임피던스 급증) | §7.2 | |
| Fig. S11a,b | 50사이클 CV (S8 피크 이동·확장 / Li2S 불변) | §7.2 | |
| Fig. S12a–d | 고로딩 1.4·2.3 mg cm⁻² 곡선·사이클 | §7.3 | ★ |
| Fig. S13a–h | scan-rate CV, b 값, Epc/Epa/ΔEp, Qa/Qc | §8 | ★ |
| Fig. S14 | scan 후 EIS (Li2S 가 낮은 계면 저항) | §8 | |
| Fig. S15a–c | **charge-first 프로토콜** 곡선·사이클·CV | §9.1 | ★★ 우리 축 |
| Fig. S16a,b | sweep 순서별 CV 35사이클 (1.01 V 불변 vs 1.07→0.97 V) | §9.1 | ★★ |
| Fig. S17 | S8 복합양극 ex situ XRD (방전 후 27° Li2S 출현, 23.1° 감소) | §10.1 | |
| Fig. S18 | Li2S 복합양극 ex situ XRD (27° 가역, S8 (222) 부재) | §10.1, §10.3 | ★ |
| Fig. S19 | **Cl 2p XPS** (LiCl 부재, 고에너지 이동) | §10.3 | ★★ "SE 분해 아님" 의 유일 근거 |
| Fig. S20 | XANES ~2472 eV 특징의 방전/충전 가역 변화 | §10.4 | ★ S2–4 귀속의 핵심 |

### 16.3 이 digest 가 **원문에 없는 수를 만든 곳** (전부 `[재현]`)

| 수 | 식 | 위치 |
|---|---|---|
| 펠릿 성형압 222 / 111 MPa | 4(2) ton × 9806.65 N ÷ (π × 0.75² cm²) | §4.1 |
| 활물질 로딩 1.02 mg cm⁻² | 6 mg × 0.30 ÷ 1.767 cm² | §4.1 |
| 전압 환산 +0.62 V | 논문이 인용한 Li–In 기준전위 | 전역 |
| S8 셀 첫 충전 ≈1340 mAh g⁻¹(S) | Fig. 6a 충전 16 h × 0.05 C × 1672 | §6.2, G14 |
| Li2S 셀 첫 사이클 CE 40.7 % | 502.5 ÷ 1233.3 | §6.3, G15 |
| 이론 대비 % (101.2 / 105.7 / 107.1) | 인쇄값 ÷ 1167 | §6.3, G2 |
| 250사이클 유지율 52.2 % / 28.3 % | 653÷1250 · 409÷1443 | §6.3, §14-7 |
| 모형 총 이론용량 1319 mAh g⁻¹ | 0.30 × 1672 + 0.70 × 1167 | §11.2 C |
| 황 함량 0.789 vs 0.698 g g⁻¹ | 0.30 + 0.70 × (32.066/45.947) | §11.2 A |
| 모든 (S)↔(Li2S)↔(composite) 환산 | × 1.4329 / × 0.6979 / × 0.30 | 전역 |

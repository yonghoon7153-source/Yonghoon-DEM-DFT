---
title: 복합양극 혼합 경로 비교 — one-step · two-step · 탄화 · 용액
description: "복합양극 혼합 경로 비교 — one-step·two-step·탄화·용액·고상 소결 코팅·반응성 밀링(첨가제형/SE 분해형) 경로의 제어 변수와 위험, 그리고 digest 24편의 ball milling 조건 전수 대조표(장비·rpm·시간·BPR·볼·분위기)"
created: 2026-09-11
updated: 2026-10-06
type: comparison
tags: [mixing-process, composite-cathode, li2s, sulfide-electrolyte]
sources: [raw/transcripts/2026-09-11-li2s-wiki-kickoff-session.md, raw/papers/kim2023_reinforced-electrical-networking-high-loading-li2s-cathode.md, raw/papers/cronk2026_highly-utilized-practical-li-s-positive-electrode-assb.md, raw/papers/kim2025_high-areal-capacity-sulfur-cathode-dual-phase-electrolyte-assb.md, raw/papers/jeong2026_reconciling-triple-phase-boundaries-tortuosity-assb.md, raw/papers/qu2025_volume-changes-li-s-solid-state-battery-components-cycling.md, raw/papers/lee2026_decoupled-sulfur-redox-pathways-initial-chemical-states-assb.md, raw/papers/huang2026_high-entropy-sulfides-kinetic-accelerators-assb.md, raw/papers/zhang2026_anode-free-assb-nanocrystalline-amorphous-li2s-na-collector.md, raw/papers/wang2023_high-capacity-assb-li-s-low-density-solid-electrolyte.md, raw/papers/wang2026_molecular-coordination-triple-synergy-cathode-assb.md, raw/papers/yu2024_nanocrystallite-cus-n-doped-carbon-host-all-solid-state-li2s.md, raw/papers/wan2021_lii-libr-catalyst-solid-state-li2s-s-reactions.md, raw/papers/liu2026_li4sns4-molecular-mediator-low-barrier-li2s-chemistry.md, raw/papers/zhangj2026_strain-coordination-long-cycling-assb.md, raw/papers/wangd2025_overcoming-conversion-limitation-tpb-mixed-conductors.md, raw/papers/kwok2023_interfacial-redox-mediator-high-performance-asslsb.md, raw/papers/gao2024_cu-i-codoping-activating-li2s-redox-kinetics-assb.md, raw/papers/park2026_low-pressure-operation-carbon-coated-current-collector-asslsb.md, raw/papers/kimjt2023_mixed-discharge-products-li2s2-li2s-asslsb.md, raw/papers/hong2026_high-valence-cation-lattice-expansion-activating-li2s.md, raw/papers/wangx2026_dual-conductivity-optimization-high-rate-ultralong-life-asslsb.md, raw/papers/hao2025_nanosized-li2s-amorphous-matrix-asslsb.md, raw/papers/feng2026_anode-free-asslsb-fe-stabilized-polysulfides.md, raw/papers/leej2025_halide-segregation-assb-lithium-chalcogen.md]
confidence: medium
explored: false
verificationStatus: unverified
claimType: mixed
evidenceScope: multi-source-primary
---

# 복합양극 혼합 경로 비교

## 비교 이유

[[li2s-assb-composite-cathode]] 의 세 네트워크(e⁻·Li⁺·활물질)는 **혼합 순서와 에너지**가
만든다. 사용자가 고려 중인 경로는 넷이고, 문헌 선례로 Kim 2023 의 액체계 절차를 다섯째 열에
둔다. 이 표가 [[one-step-vs-two-step-mixing]] 카드의 가설 목록이다.

## 비교표

| 기준 | ① One-step BM | ② Two-step (Li2S–C 선제작 → +LPSCl) | ③ Li2SO4–PVP 탄화 | ④ 에탄올 용액 | ⑤ Kim 2023 (액체계 선례) |
|---|---|---|---|---|---|
| 절차 (사용자 진술 / 원문) | Li2S·LPSCl·AB 일괄 ball milling | Li2S–C 나노복합체를 여러 방법으로 만든 뒤 LPSCl 을 **mild mixing 또는 BM** 으로 추가 | Li2SO4 를 PVP 용액에 용해 → 600–700 °C 탄화 → 900 °C 승온 → Li2S–C → LPSCl 혼합 | Li2S·C·LPSCl 각각 anhydrous ethanol 에 용해/분산 → stirring → Li2S–LPSCl–C | Gr·CNT 를 NMP 초음파 분산 → 여과·건조 → Li2S 와 BM(75:25, 조건 미기재) → 1 GPa 펠릿 |
| 무엇을 제어하나 | 한 번에 세 상을 나노 스케일로 섞음; 공정 최단 | **Li2S/C 계면을 먼저 확보**하고 SE 는 나중에 — SE 를 고에너지에서 보호 | Li2S 입자를 **탄소 안에서 생성** — 입자 크기·분산이 합성으로 정해짐 | 분자/콜로이드 수준 혼합 — 가장 균일한 삼상 접촉을 노림 | 탄소 골격을 먼저 얽고 활물질을 뒤에 — ②의 액체계 판 |
| 기대 미세구조 | Li2S·SE 모두 미세화·비정질화 가능; 세 상 무작위 분포 | Li2S–C 도메인 + 그 사이 SE; C 가 Li2S 를 감싼 채 SE 와 접함 | 탄소 매트릭스에 박힌 nano-Li2S; SE 는 도메인 밖 | 이론상 가장 균일; 실제는 용해도·재석출에 좌우 | micro-Li2S(1–5 µm)가 Gr 시트에 캡슐화 + CNT 네트워크 |
| 주요 위험 (가설) | 고에너지 BM 이 **LPSCl 을 손상**(비정질화·전도도 저하·탄소와 부반응)할 수 있음 | 2단계 mild mixing 이 SE–Li2S 접촉을 충분히 못 만들 수 있음; BM 이면 ①의 위험 재발 | 900 °C 공정·잔류 Li2SO4/황화물 부산물·탄소 함량 제어; 수율 | **LPSCl 이 극성 용매에서 분해될 위험** — 이 위키에 근거 없음(확인 필요); Li2S 의 에탄올 용해도·재석출 형태 | 액체 전해질 전용 — SE 없음. 이온 경로 문제가 애초에 없다 |
| 장비 | planetary/high-energy BM | BM 또는 Thinky(mild) | 관로·튜브 퍼니스 + BM/Thinky | 교반·건조 + Thinky | 초음파·여과·BM·프레스 |
| 위키의 근거 | 사용자 진술 | 사용자 진술 + Kim 2023 (구조적 유사) | 사용자 진술 | 사용자 진술 | `raw/papers/kim2023_…` §3 |
| 상태 | 사용 중 (주요) | 고려 중 | 고려 중 | 고려 중 | 문헌 |

장비별 성격은 [[mixing-equipment-ball-mill-thinky]].

## ★ ball milling 조건 전수 대조 (digest 24편, 2026-10-05 / 2026-10-06 갱신)

사용자 요청으로 봉인된 digest 전부의 **복합양극 제작 ball milling 조건만** 뽑았다.
수치의 정본은 각 digest 의 `compare:` 블록 → 원문이다. 이 표는 사본이다.

| 논문 | 경로 | 장비 | rpm | 시간 | BPR | 볼 · 용기 | 분위기 |
|---|---|---|---|---|---|---|---|
| **cronk2026** (Nat. Commun.) | **one-step** | Retsch planetary | **500** | **1 h** | **1 : 30** | (LPSCl 사전분쇄 5 mm YSZ) | **Ar** |
| **kim2025** (AEM, 선양국) | two-step ① | Fritsch P7, 80 mL 밀폐 포트 | **200/400/600/800 스캔 — 600 최적** | **6 h** | 미확정 (투입량 "5 mg" 오기 추정) | ZrO2 ⌀5 mm, **1 ball/mL ≈80개** | 미기재 |
| 〃 ② | 손혼합 | **agate mortar** | — | 15 min | — | — | 미기재 |
| **jeong2026** (Joule, PNNL) | two-step ② | Retsch **PM 100** | **450** | **순 4 h** (5 min on / 10 min off × 48, 벽시계 12 h) | **50 : 1** | **3 mm ZrO2 50 g** / 50 mL ZrO2 jar | 미기재 |
| **qu2025** (Nano Energy, PNNL) | **one-step** | Fritsch P7 | **300** | **4 h** | 미기재 | ZrO2 용기 (볼 미기재) | 미기재 |
| **lee2026** (CEJ, KIST) | two-step ① | Fritsch P7 | **250** | **6.5 h** (30/10 min) | 미기재 | 미기재 | **Ar** |
| 〃 ② | two-step ② | Fritsch P7 | **200** | **1 h** | 미기재 | 미기재 | **Ar** |
| **zhang2026** (AEM, anode-free) | two-step — **두 단계 모두 고에너지** | **QM-3B 3D 스윙밀** | **1400** | **유효 2 h** (15 on / 5 off, 1 h 마다 벽면 스크래핑) | **≈30 : 1** | ZrO2 jar | **Ar** |
| **huang2026** (J. Energy Chem.) | two-step ② | planetary | **350** | **4 h** | 미기재 | 미기재 | 불활성 |
| **wang2023** (Nat. Commun., 저밀도 SE) | two-step ② | Fritsch P7 premium | **350** | **10 h** | 미기재 | 45 mL ZrO2 jar (볼 미기재) | **Ar** |
| **kim2023** (Carbon Energy, **액체계**) | — | 미기재 | 미기재 | 미기재 | 미기재 | 미기재 | 미기재 |
| **wan2021** (Nano Lett., MoS2 계) | 2단계 | 미기재 | 미기재 | 미기재 | 미기재 | 미기재 | 미기재 |
| **wang2026** (ESM) | 미기재 | **미기재** — Experimental 절 자체가 없다 | — | — | — | — | — |
| **yu2024** (AEM, Nazar) | 미기재 | **미기재** — Methods 가 SI 에만 있고 SI 미확보 | — | — | — | — | — |
| **liu2026** (AFM, Li4SnS4) | **밀링이 아니다 — 고상 소결 코팅** | **미기재** — 본문 전부가 "prepared by mixing the ionic conductor, electronic conductor, and active materials" 한 문장. Experimental 절이 통째로 SI | — | 활물질 전처리 **"Sintering for 6 h"** (Fig. 2a 안의 글자, 온도 미기재) | — | — | 미기재 |
| **zhangj2026** (Nat. Commun., strain) | **one-step** (활물질 FeS2) | planetary ball mill | **300** | **2 h** | 미기재 | ZrO2 볼 · ZrO2 jar (지름·부피 미기재) | 미기재 — 밀링만 글로브박스 밖으로 읽히고 밀봉 여부 불명 |
| **wangd2025** (Nat. Mater., MIEC) | two-step ① | **유발 수동(mortar)** + 멜트 함침 160 °C 6 h | — | 10 min | — | — | 밀폐 플라스크 |
| 〃 ② | two-step ② | FRITSCH P7, 45 mL ZrO2 jar | **350** | **6 / 10 / 20 h 스캔 — 20 h 까지 단조 개선** | 미기재 | ZrO2 jar (볼 재질·지름·개수 미기재) | **Ar** |
| **gao2024** (Small, CuI) ① 도핑 | **공밀링** (소결 아님) | **Changsha Tianchuang XQM-2** planetary | **510** | **20 h** | **20 : 1 (w/w)** | **ZrO2 ⌀4 mm** (개수·용기 미기재) | **Ar** |
| 〃 ② 복합양극 | **one-step 삼상** (50:40:10 w/ VGCF) | planetary (모델 미기재) | **510** | **10 h** | 미기재 | 미기재 | **Ar** |
| **kwok2023** (EES, Nazar) | **밀링이 아니다 — `[인쇄]` "physical blending"** (저에너지 혼합) | **ESI 미확보** | **본문에 아예 없음** | 〃 | 〃 | 〃 | 〃 |
| **park2026** (AEM, Meng) ① | **two-step** ① | planetary | **600** | **1 h** (Li2S + AB **만**) | 미기재 | 미기재 | 미기재 |
| 〃 ② | two-step ② | **막자사발 손혼합** — **LPSCl 은 고에너지 단계를 겪지 않는다** | — | — | — | — | 미기재 |
| **kimjt2023** (Nat. Commun., UWO) | **one-step** (S8 계) | "high-speed ball-milling machine" — **모델 미기재**이고 "high-speed" 와 200 rpm 이 본문 내부 모순 | **200** | **4 h** | ★ **계산 불가** — 볼 40 g·⌀5 mm·50 mL 마노 jar 까지 적고 **시료 질량만 빠뜨렸다** | **ZrO2 ⌀5 mm 40 g** `[재현]` ≈102개 / **마노 jar 50 mL** | **Ar** (<0.1 ppm) |
| **hong2026** (Adv. Mater., ZrS2) ① 도핑 | **공밀링** | 미기재 | **550** | **6 h** | 미기재 | 미기재 | **Ar** |
| 〃 ② 복합양극 | two-step ② (40:40:20 또는 65:25:10) | 미기재 | **550** | **10 h** | 미기재 | 미기재 | **미기재** (①에는 Ar 이라 적었는데 ②에는 없다) |
| **wangx2026** (Adv. Mater., Li2SexS1−x) | ★ **혼합 기술 자체가 없다** — Experimental 절이 통째로 부재(SI 미확보). 활물질 합성은 `[인쇄]` "Se, S, LiH 의 ball milling + subsequent heat treatment" 다섯 단어가 전부 | **미기재 — rpm 조차 없다** | 〃 | 〃 | 〃 | 〃 |
| **hao2025** (JACS, 반응성 밀링) ① | ★ **반응성 밀링(in-situ 치환)** — Li2S + FeCl3 **85:15 wt%** | **전량 SI 미확보** — 본문 10쪽에 `rpm`·`MPa`·`°C` 가 **한 번도 없다** | 〃 | 〃 | 〃 | 〃 |
| 〃 ② 복합양극 | **6:3:1 wt%**(Li2S:LPSCl:AB) — ★ **방식 자체가 미기재**(볼밀인지 손혼합인지 모른다) | 〃 | 〃 | 〃 | 〃 | 〃 |
| **feng2026** (ACS EL, FeCl3) ① | ★ **반응성 밀링** — Li2S + FeCl3 **몰비 0.1** | **전량 SI 미확보** — 본문의 합성 서술은 `[인쇄]` "A mixture of Li2S and 5 or 10 mol % FeCl3 was ball-milled under Ar protection (details in the SI)" **한 문장**이 전부 | 〃 | 〃 | 〃 | **Ar** `[인쇄]` |
| 〃 ② 복합양극 | **40:40:20 wt%**(FLS:LPS:VGCF) — ★ 방법이 **"mixing" 이라는 단어 하나**뿐 | 〃 | 〃 | 〃 | 〃 | **SI 미확보** |
| **leej2025** (*Science*, 할로겐 분리) | **one-step 삼상** (S8/Se/SeS2/Te + LPSCl + 탄소) | ★ **미기재 — 본문에 `ball`·`mill` 이라는 단어가 한 번도 없다.** "ultrahigh-speed (UHS) mixing" 만 47회 | **2000** (대조 **400**) ★ 이 위키 최고속 | **5 h** (스캔 **1 / 5 / 10 h**) | 미기재 | 미기재 | **미기재** — Ar·글로브박스·밀폐 한 글자도 없다 |

### 이 표에서 읽히는 것 `[해석]`

1. **★ BPR 을 적은 논문이 24편 중 **4편**뿐이다** (cronk 1:30 · jeong 50:1 · zhang ≈30:1 · **gao 20:1**).
   BPR 은 밀링 에너지를 정하는 1차 변수인데 대부분이 안 적는다 → **논문 간 "밀링 강도" 비교가
   원리적으로 불가능하다.** 우리는 반드시 적는다 ([[mixing-equipment-ball-mill-thinky]] 양식).
2. **볼 재질·지름을 적은 논문은 2편**(jeong 3 mm ZrO2 50 g · kim2025 ⌀5 mm 1 ball/mL).
   **분위기는 8편**(Ar 7 · 불활성 1). **rpm·시간은 11편**이 적는다. **볼 재질·지름은 3편**(jeong · kim2025 · **gao ⌀4 mm**).
3. **10편은 ball milling 조건을 한 글자도 안 적는다** — kim2023(액체계) · wan2021 · wang2026 ·
   yu2024 · liu2026 · **kwok2023** · **wangx2026** · **hao2025** · **feng2026** · **leej2025**.
   ★★★ **그 열 번째가 가장 아프다 — `leej2025` 는 자기 초록에서 `[인쇄]` "mixing 은 가장 많이 쓰지만
   가장 이해되지 않은 공정" 이라고 선언한 논문인데, 그 공정을 숫자 두 개(2000 rpm · 5 h)로 기술한다.**
   본문에 **`ball`·`mill` 이라는 단어 자체가 없고** 장비 종류조차 알 수 없다 — **2000 rpm 은 유성
   볼밀·고속전단믹서·비드밀에서 전혀 다른 에너지밀도**다. `[해석]` Methods 가 통째로 SI 인 것은
   *Science* 형식이고 SI 미확보가 1차 원인이므로 단정하지 않는다. 다만 **"UHS" 를 47회 쓰면서
   그 rpm 이 무엇의 rpm 인지 한 번도 말하지 않는다** → 본문만으로 재현 불가.
   ★★ **그중 셋은 "미기재" 가 아니라 "SI 미확보" 다** — hao2025 · feng2026 · wangx2026 은 본문에
   Experimental 절이 통째로 없다. `[해석]` **진단이 다르면 처방도 다르다**: "미기재" 는 저자가 안
   적은 것이라 영원히 알 수 없고, **"SI 미확보" 는 우리가 PDF 한 건을 구하면 닫힌다.** 이쪽이
   실험보다 훨씬 싸다 — 이 셋의 SI 를 확보하는 것이 ball milling 표의 가장 값싼 다음 수다. 그중 **wang2026 은 Experimental 절 자체가 없고**, yu2024·liu2026 은 Methods 가
   SI 에만 있다. **혼합 조건 미기재가 이 분야의 예외가 아니라 다수 관행에 가깝다** — 17편 중 6편이면,
   우리가 "문헌 조건을 따라 한다" 는 말을 할 수 있는 대상이 애초에 좁다.
   ★ **wangx2026 은 rpm 조차 없다** — 복합양극 혼합은 **기술 자체가 없고**(Fig. 1 범례로 3성분인
   것만 안다) **조성비·탄소 종류도 미기재**이며, 간접 상한은 `[인쇄]` "48 wt% 로 늘려" 한 줄뿐이다.
   ⚠ 그리고 그 논문은 **도입부에서 "과도한 압력은 내부 응력과 SE 내 Li 석출을 유발한다" 며 압력을
   비판하면서 자기 셀의 성형압·구속압을 둘 다 안 적는다** — 공백의 새 유형이다.
   ★ **그중 kwok2023 이 가장 심하다**: 이 위키에서 **가장 긴 상온 수명(1 mA cm⁻² 1,000 사이클, 77 %)**
   을 낸 논문인데 **혼합 방식이 `[인쇄]` "physical blending" 두 단어이고 성형압·운전 구속압·셀 형식이
   본문에 아예 없다** (Methods 전량 ESI). `[해석]` 그래도 하나는 읽힌다 — **core–shell 껍질이 깨지면
   안 되므로 고에너지 밀링일 수 없다.** 즉 "physical blending" 은 저에너지 혼합이고, 이것은
   [[one-step-vs-two-step-mixing]] H4(밀링 에너지 상한)의 간접 근거다.
4. **"세고 짧게" vs "약하고 길게" 가 갈린다.** 같은 Fritsch P7 안에서도
   **qu2025 300 rpm 4 h (one-step)** · lee2026 250 rpm 6.5 h · huang2026 350 rpm 4 h ·
   **wang2023 350 rpm 10 h** · **kim2025 600 rpm 6 h** 가 제각각이고, cronk2026 은 **Retsch
   500 rpm 1 h** 로 가장 짧고 세다. zhang2026 의 **1400 rpm** 은 장비 계열이 달라(3D 스윙밀)
   직접 비교가 안 된다.
   → **밀링 조건이 성능과 어떻게 대응하는지는 이 표로는 안 나온다** (조성·활물질·SE 가 전부
   다르다). 대응을 보려면 **한 논문 안에서 밀링만 바꾼 스캔**이 필요하고, 그것을 한 논문은
   **kim2025**(200/400/600/800 rpm, 600 최적 — [[one-step-vs-two-step-mixing]] H4)와
   **wangd2025**(350 rpm 에서 **6/10/20 h** 스캔, 20 h 까지 단조 개선) **둘**이다.
   ★ 둘이 스캔한 축이 다르다 — kim2025 는 **세기(rpm)**, wangd2025 는 **시간**. 그리고 결과가
   반대 모양이다: 세기에는 **최적점이 있고**(600 에서 꺾인다), 시간은 **단조**다(20 h 까지).
   `[해석]` 우리 밀링 설계에서 **먼저 고정할 변수는 rpm** 이고, 시간은 뒤에 늘려 가며 본다.
5. **간헐 밀링(on/off)을 쓰는 논문이 셋**이다 — jeong 5/10 min · zhang 15/5 min · lee 30/10 min.
   `[해석]` 황의 녹는점 115 °C 를 의식한 설계로 보인다 (jeong 의 5 min 은 특히 짧다).
   **연속 밀링(cronk 1 h)과 간헐 밀링은 같은 "시간" 이어도 열 이력이 다르다** — 이것이
   Cronk↔Jeong 이 밀링의 효과를 정반대로 보고하는 이유의 후보다 (digest jeong2026 §13.2).
6-a. ★ **BPR 에 "거의 다 왔는데 한 숫자" 범주를 신설한다 (kimjt2023).** 그 논문은 **볼 질량 40 g ·
   볼 지름 5 mm · 용기 부피 50 mL · 용기 재질(마노)** 까지 적고 **시료 질량만 빠뜨려** BPR 이 계산되지
   않는다. `[재현]` 볼 개수는 ≈102개까지 복원된다. `[해석]` **BPR 미기재의 절반은 의도가 아니라 누락**
   이라는 뜻이고, **우리 기록 양식에서 빠지기 쉬운 칸이 바로 "총 투입량"** 임을 알려준다.

6. **S8 계는 밀링 전에 멜트 함침(155–160 °C, 10–12 h)을 넣는다** — huang · jeong · kim2025 ·
   wang2023 넷 모두. **우리 Li2S 계에는 해당하지 않는다** (Li2S 는 m.p. 938 °C).
7. **우리 셀과 조성이 겹치는 둘의 밀링이 반대다**: **qu2025(Li2S:C65:LPSCl = 33:17:50) one-step
   300 rpm 4 h** vs **lee2026(30:20:50) two-step 250 rpm 6.5 h + 200 rpm 1 h**.
   둘 다 작동하고, **절대 용량을 적은 쪽은 lee2026 뿐**이다(qu2025 는 측정 논문이라 G1).

8. **★ 밀링을 아예 피하는 다섯 번째 경로가 있다 — liu2026 의 고상 소결 코팅.**
   Li2S 에 SnS2 를 섞어 **6 h 소결**하면 ≈30 nm Li4SnS4 껍질이 in-situ 로 자란다
   (반응식 `x Li2S + SnS2 = (x−2) Li2S + Li4SnS4`, ΔH −27.1 kJ mol⁻¹ [인쇄]).
   **목적은 cronk2026 과 같다** — 활물질 표면에 thiophosphate 계열 계면상을 미리 깔아 두는 것.
   **수단만 다르다**: cronk 는 밀링의 기계적 에너지로, liu 는 열로 만든다.
   `[해석]` 이것이 우리에게 중요한 이유는 [[one-step-vs-two-step-mixing]] 의 H2b
   (밀링을 겪은 LPSCl 이 아직 superionic 인가)를 **원리적으로 우회**하기 때문이다 — SE 를
   밀링에 넣지 않고 활물질 쪽만 처리한다. **단 소결 온도·분위기가 논문에 없어 지금은 시도 불가**
   (G: liu2026 공백표). SI 가 확보되면 가장 먼저 꺼내 볼 조건이다.

9-a. ★★ **같은 그룹이 같은 조성을 one-step 과 two-step 으로 둘 다 했다 — 그런데 통제 비교가 아니다.**
   **cronk2026**(one-step, Retsch 500 rpm 1 h, **BPR 1:30**)과 **park2026**(two-step, 600 rpm 1 h 로
   Li2S+AB 만 밀고 **LPSCl 은 손혼합**)은 조성(**30:50:20**)·SE(NEI LPSCl)·탄소(AB)·대극(Li–In)이 같다.
   이 표에서 **가장 통제에 가까운 한 쌍**이다. ⚠ **그래도 승패 판정에 쓰면 안 된다** — 로딩·전극 형태
   (건식 PTFE 필름 vs 펠릿)·집전체·운전 압력이 다르다.
   ★ 그리고 park2026 이 **H2(SE 보호) 의 인과를 넓힌다**: **LPSCl 을 고에너지 밀링에 넣지 않았는데도**
   Raman `[인쇄]` **425 → 418 cm⁻¹** 로 PS₄³⁻ 가 움직인다(Li2S 가 LPSCl 을 LPS 로 환원). →
   가설을 **"밀링이 SE 를 죽인다" 에서 "접촉만으로도 SE 가 환원된다" 로 넓혀야 한다.**

9. **펠릿셀과 파우치셀이 사실상 다른 경로인데 비교한 논문이 없다.** zhangj2026 의 파우치 양극은
   볼밀이 아니라 **Hummer 음향 혼합기(HAM100) + 반복 섬유화 롤프레스**로 만든 자립 필름이다.
   같은 논문 안에서 **0.05 C · 55 °C 펠릿 868.4 vs 파우치 615.8** `[재현]` **29 % 낮다** — 다만
   로딩도 다르므로 혼합 경로 단독에 귀속할 수 없다. kim2025 도 유발 손혼합 단계를 쓰지만
   **밀링 ↔ 비밀링 혼합의 직접 대조는 24편 중 1편**(아래 소견 11 — `leej2025` 가 처음 했다)이다. `[해석]` 스케일업하면 밀링을 못 쓰는데,
   **그때 성능이 어떻게 변하는지 아무도 측정하지 않았다.**

10. ★★ **여섯째 경로 — "반응성 밀링(in-situ 치환)" (2026-10-06, Hao 2025).**
   지금까지 다섯 갈래였다: one-step BM · two-step BM · 탄화 · 용액 · **고상 소결 코팅**(Liu 2026).
   Hao 2025 는 어디에도 안 들어간다 — **활물질과 반응성 전구체를 함께 밀링해 밀링 중 고상 치환
   반응을 일으킨다**: `2 Li2S + FeCl3 → LiFeS2 + 3 LiCl`. 한 공정이 **(i) 활물질을 ≈4 nm 로 쪼개고
   (ii) 비정질 혼합전도 매트릭스를 새로 만든다.** 보편성도 보였다 — M = Al·Ga·Zn·Cu·Fe·V·Zr·Hf·Y
   아홉 가지에서 같은 반응이 XRD 로 확인된다.

   ★ **이 경로가 앞의 다섯과 근본적으로 다른 점**: **밀링이 분산 공정이 아니라 합성 반응기**다.
   그래서 **투입 조성 ≠ 생성 조성**이고 **활물질 질량 자체가 반응으로 줄어든다**
   (`[재현]` 투입 Li2S 85 wt% → 잔존 **76.5 wt%**, 생성 LiFeS2 11.7 + **LiCl 11.8 wt%**).
   `[해석]` 우리에게 두 가지를 뜻한다 —
   **(a) 밀링 조건을 기록하는 양식에 "반응이 일어났는가" 칸이 필요하다.** 우리 one-step 셀에서
   Li2S·LPSCl·AB 를 함께 밀 때 **LPSCl 이 반응물로 참여할 수 있다**(Park 2026 은 밀링 없이
   접촉만으로도 Raman 425 → 418 cm⁻¹ 의 PS₄³⁻ 변화를 보였다 — 소견 9-a).
   **(b) 조성을 "투입 기준" 으로만 적으면 틀린다.** 이름 `92Li2S@8LiFeS2` 는 **LiCl 11.8 wt% 를
   통째로 숨기고**, 그 논문의 "활물질 함량 48 %" 는 `[재현]` **mol% 를 wt% 로 쓴 값**이다
   (화학량론 wt% 로는 45.9 %, 저자 자신의 XRD 모델로는 41.0 %).
   → **우리는 투입 조성과 "밀링 후 XRD 로 확인한 상" 을 따로 적는다.**
   ⚠ 밀링 조건은 **전량 SI 미확보**라 이 경로를 지금 시도할 수는 없다.
   ★ **그리고 이 경로가 둘이 됐다** — `feng2026_…` 도 `Li2S + FeCl3`(몰비 0.1)를 Ar 하에서 밀어
   저결정 FeSx·LiCl·S–S 모티프를 만든다. **같은 전구체족(MClx)에서 독립 두 그룹**(EIT/UWO ·
   UCSD/Brookhaven)이 같은 해에 나왔다는 것은 **경로가 재현된다는 뜻**이다.
   ⚠ 다만 둘 다 **"갈지 않은 물리 혼합" 음성대조**가 없다(Hong 2026 은 σ 축에서 그것을 했다) →
   전도도 상승이 **반응 산물 때문인지 그냥 섞여서인지** 아직 분리되지 않았다.

11. ★★★ **혼합 축의 완전 대조군 집합이 처음 나왔다 (2026-10-02, Lee J 2025).** 이 표의 23편은
   모두 "자기 레시피 하나" 만 보고했다. `leej2025` 는 **속도 · 시간 · 기계력 유무 · 열 단독 · 활물질
   유무**를 모두 갈라 돌렸고, 그것이 이 논문의 진짜 기여다.

   | 대조 | 조건 | 표면 Cl:P `[도표]` | 결과 |
   |---|---|---|---|
   | pristine LPSCl | — | 0.96–1.00 | 분리 없음 |
   | **손혼합 (무밀링, 상온)** | — | **1.00** | ★ **분리 없음** |
   | **손혼합 + 열만** | **145 °C 3 h** | **1.38** | ★★ **기계력 없이 열만으로 부분 분리** |
   | 저속 | **400 rpm** | `[인쇄]` "no Cl segregation" | 없음 |
   | 단시간 | 2000 rpm **1 h** | `[인쇄]` "no Cl segregation" | 없음 |
   | **표준** | **2000 rpm 5 h** | **3.55 · 2.45** (벌크 0.92) | `[인쇄]` "two to three times" |
   | 과혼합 | 2000 rpm **10 h** | 분리는 유지 | ★ `[인쇄]` **"notable crystal structure collapse of LPSCl"** |
   | **활물질 없는 대조** | LPSCl + 탄소만 가열 | — | ★★ `[인쇄]` LiCl 분리는 **"not driven by the reaction with sulfur"** |

   `[해석]` 우리에게 세 가지를 준다.
   **(a) 임계 에너지가 있다** — 400 rpm 과 1 h 에서는 **아무 일도 일어나지 않는다.** 즉 "밀링은 늘
   SE 를 바꾼다" 가 아니라 **문턱을 넘어야 바뀐다.**
   **(b) 열만으로도 일어난다** — 손혼합 + 145 °C 3 h 에서 Cl:P 가 1.00 → 1.38 이다. **기계력이
   필수가 아니다.** 그래서 밀링 중 국부 발열이 기전 후보인데 ⚠ **그 논문은 혼합 중 온도를 재지 않았다.**
   **(c) 과혼합에 대가가 있다** — 10 h 에서 **LPSCl 결정구조가 붕괴**하고 성능이 무너진다.
   → **최적점이 존재한다**(1 / 5 / 10 h 세 점으로 보였다).

12. ★★ **경로 ⑥ "반응성 밀링" 을 두 갈래로 나눈다.**
   - **⑥-a 첨가제 치환형** — `hao2025`(Li2S + FeCl3 → LiFeS2 + 3 LiCl) · `feng2026`(Li2S + FeCl3).
     **밖에서 넣은 전구체**가 활물질과 반응한다.
   - **⑥-b SE 분해·재증착형** — `leej2025`. **첨가제가 없고 SE 자신의 할로겐이 분리**되어 활물질
     표면에 Li halide 층으로 쌓인다.

   ★ **그래서 "우리 one-step 셀에서도 이미 일어나고 있을 가능성" 이 생긴다** — 우리 LPSCl 은 전량이
   밀링을 겪는다. ⚠ 다만 **"반응성 밀링이 기본값이다" 로 단정하지 않는다**: 근거가 이 한 편이고,
   같은 논문의 400 rpm·1 h 대조가 **문턱 아래에서는 아무 일도 없다**는 것을 함께 보인다.
   ⚠ 그리고 **`park2026` 의 "접촉만으로도 SE 가 환원된다"(Raman 425 → 418 cm⁻¹)와는 다른 현상**이다 —
   그쪽은 **Li2S(환원제)** 계이고 이쪽은 **S8/Se/Te(산화제)** 계다. **기전이 다르므로 같은 줄에 두지 않는다.**

   → **가장 값싼 확인은 셀을 안 쓴다**: **우리 one-step 복합분말을 그대로 XRD 에 걸어 LiCl(200) /
   LPSCl 피크비를 본다.** 하루면 되고, 나오면 우리 "밀링이 SE 를 망가뜨린다" 서사의 일부는
   **"이미 일어난 계면 설계"** 가 된다 ([[reference-cell-experiment-plan]] 0-c).

### 우리가 기록해야 할 항목 (이 표의 빈칸이 곧 체크리스트다)

장비·용기 부피·**볼 재질·지름·개수** · **총 투입량** · **BPR** · rpm · **순 밀링 시간과 on/off 주기** ·
**밀링 후 XRD 로 확인한 상(= 반응이 일어났는가)** ·
분위기 · 단계 수와 각 단계의 조성 · (S8 계면) 멜트 함침 온도·시간 · 성형 압력과 시간.

## 결론

지금 말할 수 있는 것은 **구조**뿐이다: ①은 SE 를 활물질·탄소와 같은 에너지에 노출시키고,
②③④ 는 모두 **Li2S–C 계면을 먼저 만들고 SE 를 나중에 붙이는** 전략이다. Kim 2023 은 액체계
이지만 ②의 논리(탄소 골격 선제작)로 micro-Li2S 를 활성화했고 소량의 1D 탄소가 네트워크를
유지했다([[carbon-dimensionality-electron-network]]). 어느 경로가 우리 셀에서 이기는지는
**위키에 데이터가 없다** — 다음 ingest 와 실험이 채운다.

**★ 2026-10-02 — 이 표의 밀링 좌표를 읽는 법이 하나 추가됐다.** 위 전수표는 **투입 조건**
(rpm·시간·BPR)을 모으지만, **그 조건이 SE 에 실제로 무엇을 했는지**를 잰 행은 따로 모아야
한다 — [[what-milling-does-to-the-electrolyte]] 가 그 22행이다. 거기서 나온 두 결론이 이 표의
해석을 바꾼다: ① **"고에너지" 라는 말은 분모를 정하지 않으면 뜻이 없다** — 같은 밀링이 벌크
SE 전도도는 내리고 복합체 유효 수송은 올린다. ② **문턱과 상한이 둘 다 보고됐다** — 400 rpm·
1 h 에서는 아무 일도 안 일어나고(Lee J 2025), 10 h 에서는 SE 결정구조가 붕괴한다.
→ 그래서 이 표의 "기록해야 할 항목" 에 **밀링 중 온도**가 들어가야 한다(아래 체크리스트는
아직 그 칸이 없고, 24편 중 온도를 잰 논문도 0편이다).

## 불확실성

- 위 표의 "주요 위험" 열은 전부 가설이다. 특히 ④ 의 용매–SE 상용성과 ① 의 SE 손상은 근거
  논문을 ingest 하기 전에는 인용하지 않는다.
- 사용자의 실제 BM 조건(rpm·시간·BPR·볼 재질·분위기)이 위키에 없다 — 기록 양식은
  [[mixing-equipment-ball-mill-thinky]] 에 두었다.

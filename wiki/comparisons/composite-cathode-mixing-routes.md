---
title: 복합양극 혼합 경로 비교 — one-step · two-step · 탄화 · 용액
description: "복합양극 혼합 경로 비교 — one-step·two-step·탄화·용액 네 경로의 제어 변수와 위험, 그리고 digest 15편의 ball milling 조건 전수 대조표(장비·rpm·시간·BPR·볼·분위기)"
created: 2026-09-11
updated: 2026-10-06
type: comparison
tags: [mixing-process, composite-cathode, li2s, sulfide-electrolyte]
sources: [raw/transcripts/2026-09-11-li2s-wiki-kickoff-session.md, raw/papers/kim2023_reinforced-electrical-networking-high-loading-li2s-cathode.md, raw/papers/cronk2026_highly-utilized-practical-li-s-positive-electrode-assb.md, raw/papers/kim2025_high-areal-capacity-sulfur-cathode-dual-phase-electrolyte-assb.md, raw/papers/jeong2026_reconciling-triple-phase-boundaries-tortuosity-assb.md, raw/papers/qu2025_volume-changes-li-s-solid-state-battery-components-cycling.md, raw/papers/lee2026_decoupled-sulfur-redox-pathways-initial-chemical-states-assb.md, raw/papers/huang2026_high-entropy-sulfides-kinetic-accelerators-assb.md, raw/papers/zhang2026_anode-free-assb-nanocrystalline-amorphous-li2s-na-collector.md, raw/papers/wang2023_high-capacity-assb-li-s-low-density-solid-electrolyte.md, raw/papers/wang2026_molecular-coordination-triple-synergy-cathode-assb.md, raw/papers/yu2024_nanocrystallite-cus-n-doped-carbon-host-all-solid-state-li2s.md, raw/papers/wan2021_lii-libr-catalyst-solid-state-li2s-s-reactions.md, raw/papers/liu2026_li4sns4-molecular-mediator-low-barrier-li2s-chemistry.md, raw/papers/zhangj2026_strain-coordination-long-cycling-assb.md, raw/papers/wangd2025_overcoming-conversion-limitation-tpb-mixed-conductors.md]
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

## ★ ball milling 조건 전수 대조 (digest 15편, 2026-10-05 / 2026-10-06 갱신)

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

### 이 표에서 읽히는 것 `[해석]`

1. **★ BPR 을 적은 논문이 15편 중 3편뿐이다** (cronk 1:30 · jeong 50:1 · zhang ≈30:1).
   BPR 은 밀링 에너지를 정하는 1차 변수인데 대부분이 안 적는다 → **논문 간 "밀링 강도" 비교가
   원리적으로 불가능하다.** 우리는 반드시 적는다 ([[mixing-equipment-ball-mill-thinky]] 양식).
2. **볼 재질·지름을 적은 논문은 2편**(jeong 3 mm ZrO2 50 g · kim2025 ⌀5 mm 1 ball/mL).
   **분위기는 6편**(Ar 5 · 불활성 1). **rpm·시간은 10편**이 적는다.
3. **5편은 ball milling 조건을 한 글자도 안 적는다** — kim2023(액체계) · wan2021 · wang2026 ·
   yu2024 · liu2026. 그중 **wang2026 은 Experimental 절 자체가 없고**, yu2024·liu2026 은 Methods 가
   SI 에만 있다. **혼합 조건 미기재가 이 분야의 예외가 아니라 다수 관행에 가깝다** — 3편을 넘어
   5편이면, 우리가 "문헌 조건을 따라 한다" 는 말을 할 수 있는 대상이 애초에 좁다.
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

9. **펠릿셀과 파우치셀이 사실상 다른 경로인데 비교한 논문이 없다.** zhangj2026 의 파우치 양극은
   볼밀이 아니라 **Hummer 음향 혼합기(HAM100) + 반복 섬유화 롤프레스**로 만든 자립 필름이다.
   같은 논문 안에서 **0.05 C · 55 °C 펠릿 868.4 vs 파우치 615.8** `[재현]` **29 % 낮다** — 다만
   로딩도 다르므로 혼합 경로 단독에 귀속할 수 없다. kim2025 도 유발 손혼합 단계를 쓰지만
   **밀링 ↔ 비밀링 혼합의 직접 대조는 15편 중 0편**이다. `[해석]` 스케일업하면 밀링을 못 쓰는데,
   **그때 성능이 어떻게 변하는지 아무도 측정하지 않았다.**

### 우리가 기록해야 할 항목 (이 표의 빈칸이 곧 체크리스트다)

장비·용기 부피·**볼 재질·지름·개수** · **총 투입량** · **BPR** · rpm · **순 밀링 시간과 on/off 주기** ·
분위기 · 단계 수와 각 단계의 조성 · (S8 계면) 멜트 함침 온도·시간 · 성형 압력과 시간.

## 결론

지금 말할 수 있는 것은 **구조**뿐이다: ①은 SE 를 활물질·탄소와 같은 에너지에 노출시키고,
②③④ 는 모두 **Li2S–C 계면을 먼저 만들고 SE 를 나중에 붙이는** 전략이다. Kim 2023 은 액체계
이지만 ②의 논리(탄소 골격 선제작)로 micro-Li2S 를 활성화했고 소량의 1D 탄소가 네트워크를
유지했다([[carbon-dimensionality-electron-network]]). 어느 경로가 우리 셀에서 이기는지는
**위키에 데이터가 없다** — 다음 ingest 와 실험이 채운다.

## 불확실성

- 위 표의 "주요 위험" 열은 전부 가설이다. 특히 ④ 의 용매–SE 상용성과 ① 의 SE 손상은 근거
  논문을 ingest 하기 전에는 인용하지 않는다.
- 사용자의 실제 BM 조건(rpm·시간·BPR·볼 재질·분위기)이 위키에 없다 — 기록 양식은
  [[mixing-equipment-ball-mill-thinky]] 에 두었다.

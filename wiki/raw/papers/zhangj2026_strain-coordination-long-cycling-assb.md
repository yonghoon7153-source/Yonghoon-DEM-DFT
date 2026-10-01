---
title: "Zhang (Jiaxu) et al. 2026 — Strain-coordination strategy enabling long-cycling all-solid-state lithium-sulfur batteries (Nat. Commun. 17, 7858)"
description: "FeS2 양극의 팽창과 prelithiated Si(Li2Si) 음극의 수축을 부호로 맞춰 셀 수준 몰부피 변화를 −17.2 %에서 +2.6 %로 줄이고, LTO zero-strain 대극으로 전극별 용량당 응력(σc)을 분해 측정해 15 MPa 저압 운전을 주장한 논문 — 주의, 산둥대 Qi Zhang 의 anode-free 논문과 다른 Zhang 이다"
source_url: local-upload/13e1c1a6-2._strain_coordination_strategy_enabling_long_cycling_ASSLSBs.pdf
doi: 10.1038/s41467-026-74625-5
ingested: 2026-10-01
sha256: 972dbd871c98caba3a217209af4042d4d374efd80eac3795e88e4643e33fff76
tags: [assb, sulfide-electrolyte, composite-cathode, li2s, mixing-process, li-free-anode]
compare:
  system: "ASSB Li–S 계열(저자 표기 ASSLSB). 활물질은 Li2S 도 S8 도 아닌 **FeS2** — Li2S 는 방전 생성물(FeS2 + 4Li → Fe⁰ + 2Li2S). 전략 논문이지 Li2S 양극 논문이 아니다"
  electrolyte: "Li5.5PS4.5Cl1.5 (LPSC, >6 mS cm⁻¹, GLABAT). 산화물 대조전극(NCM·LCO)에는 Li3InCl6 별도 사용"
  cathode: "FeS2 : LPSC : VGCF = 20:40:4 (합 64 — 정규화 31.3:62.5:6.3) 또는 50:42:8 wt%. 바인더 없음(펠릿). 파우치만 PTFE 0.5 추가"
  li2s_source: "해당 없음 — Li2S 는 in-situ 방전 생성물이고 Fe⁰ 나노입자와 함께 생긴다. 출발 활물질은 상용 micro FeS2 D50 14–18 µm (Macklin 99.5 %)"
  mixing: "planetary ball mill, zirconia jar + zirconia balls, 300 rpm 2 h, 1단계. BPR·볼 지름·용기 부피·휴지 주기 전부 미기재. 밀링만 Ar 글로브박스 밖으로 읽히고 밀봉 여부 미기재 (G1·G2). 파우치 양극은 볼밀이 아니라 Hummer Acoustic Mixer HAM100 + 섬유화 롤프레스"
  loading_mg_cm2: "1.6 mg cm⁻²(FeS2, 펠릿 표준) · 2.2(파우치) · 30.5(고로딩, 총 복합체 60.96 중 FeS2 50 wt%) · 광학현미경 셀만 ~20"
  anode: "prelithiated Si = LixSi, in-situ 합금화. Si(97):PTFE(3) 롤링 필름 ~30 µm, ~3 mg cm⁻², ⌀10 mm + Li 박 ⌀8 mm 22/45/65 µm(0.6/1.2/1.8 mg) → LiSi/Li2Si/Li3Si. 대조군은 Li 금속, 별도 Li–In 셀도 있음. N/P 표기 불일치 (Fig.1 캡션 1 · Methods ~1.5 · 재구성 ≈4)"
  first_charge: "해당 없음 — 셀은 충전상태(FeS2)에서 시작해 첫 스텝이 방전이다. 충전 컷오프 2.65 V vs LixSi = 3.0 V vs Li/Li⁺. 충전 말기 2.6–2.9 V 구간이 Li2S → S (Fig. 7e 귀속)"
  first_discharge_mAh_gS: "1384 — [재현] 인쇄값 740.0 mAh g⁻¹(FeS2) × 1.871. 단 [도표, Fig. 5a] 1사이클은 ≈650 (= 1216 S 기준) 으로 본문과 어긋난다 (G3). 55 °C 0.05 C 는 868.4(FeS2) = 1625(S)"
  first_discharge_mAh_gLi2S: "966 — [재현] 740.0 × 1.3054 (생성 Li2S 질량 기준). [도표] 기준이면 ≈849. 55 °C 값은 1134"
  cycle_capacity_mAh_gS: "15 MPa·25 °C·0.1 C 50사이클 [도표] ≈450 mAh g⁻¹(FeS2) = ≈842(S). 100 MPa·1 C 4500사이클 411(FeS2) = 769(S). 4 C 30000사이클 339.5 = 635(S). 15 C 140000사이클 243.6 = 456(S)"
  cycle_capacity_mAh_gLi2S: "50사이클 [도표] ≈587 · 4500사이클 537 · 30000사이클 443 · 140000사이클 318 (모두 ×1.3054 환산)"
  areal_mAh_cm2: "1.18 (첫 방전, 1.6 mg cm⁻² 인쇄값 기준) · 1.39 (55 °C) · 0.66 (1 C 4500사이클) · 0.54 (4 C) · 0.39 (15 C) · **21.7 @ 30.5 mg cm⁻²(FeS2), 100 MPa, 100사이클 19.3 로 89 %** (C-rate 가 본문 0.1 C vs 그림 1C 로 충돌 — G12)"
  cycles: "15 MPa 25 °C: [도표] 50사이클 유지 ≈69 % (본문은 30사이클까지만 말한다, G4) · 30 MPa 25 °C: 50사이클 94.3 % · 100 MPa: 1 C 4500사이클 85 %(분모가 첫 사이클이 아니라 활성화 후 ≈483, 첫 사이클 기준이면 71 % — G11) · 4 C 30000 · 15 C 140000(그림은 SI 미확보) · 파우치 15 MPa 55 °C 1 C 500사이클 [도표] ≈67 %"
  temperature_C: "25 (표준·상온 사이클·율속·응력·두께·100 MPa 장수명) · 55 (고용량·파우치)"
  mechanism: "strain-coordination = 전극 쌍(pairing) 설계. 몰부피 회계로 Li‖FeS2 −17.2 % → Li2Si‖FeS2 +2.6 %(셀 수준). LTO zero-strain 대극을 기준자로 용량당 응력 σc 측정: FeS2 0.80 · Li2Si 0.88 · Li 1.03 · LiSi 0.71 · Li3Si 0.94 · NCM 0.213 · LCO −0.1558 MPa mAh⁻¹, 실셀 0.16 (−80 %). Lagrange 보간합이 실측과 겹침. XCT: 양극 56 → 68 µm(+21.4 %), 음극 28 → 13 µm(−53.6 %), 셀 총 두께 변화 ~1.4 µm(레이저 변위, 정압). 압력-EIS: 0 MPa 356 Ω, 15 MPa 이상 포화. in-situ EIS/DRT 4영역 귀속, GITT D_Li 4.1 vs 4.7 ×10⁻¹² cm² s⁻¹. AC-STEM: 100사이클 후 Fe⁰ 나노입자가 Li2S + LPSC 기지에 분산. 계면 반응에너지 Li −0.59 / Li2Si −0.41 / Si −0.155 eV/atom. 55 °C 용량 증가를 LPSC 환원 → Li2S 로 귀속하면서 대조셀 없음"
  our_axis: "H5(기계적 제한)의 도구를 준다 — LTO zero-strain 기준자 · 용량당 응력 σc · 압력별 EIS(0 MPa 356 Ω, 15 MPa 포화). 이식 가능: 압력-EIS 스윕, LTO 기준자 반쪽셀, 셀 수준 ΔV 와 양극 수준 ΔV 의 구분. 이식 불가: FeS2 활물질, 100 MPa 체제, Li 재고를 늘리는 음극 설계(우리는 anode-free 방향), 619.2 Wh kg⁻¹(분모가 FeS2 뿐)"
---

# 수집 목적

Jiaxu Zhang, Shengjie Xia, Pushun Lu, Suzhe Liang, Jiamin Fu, Zhimin Zhou, Wenlin Yan,
Guantai Hu, Kaiyong Tuo, Jian Hong, Shutao Zhang, Ziqing Wang, Xueliang Sun, Changhong Wang,
**"Strain-coordination strategy enabling long-cycling all-solid-state lithium-sulfur batteries"**,
*Nature Communications* **17** (2026) 7858, DOI **10.1038/s41467-026-74625-5**
(received 2025-08-28 / accepted 2026-06-09) 의 **절별 해체분석**.

> [!warning] ⚠ 동명이인 구분 — 이 위키에는 Zhang 논문이 둘이다
> - **이 파일 (`zhangj2026_…`)** = **Jiaxu Zhang** 제1저자, Eastern Institute of Technology(닝보)
>   + USTC, 교신 **Xueliang Sun · Changhong Wang**. 활물질 **FeS2**, 음극 **prelithiated Si(LixSi)**,
>   SE **Li5.5PS4.5Cl1.5**. 주제는 **스택 압력·변형(strain) 상쇄**.
> - **`zhang2026_anode-free-assb-nanocrystalline-amorphous-li2s-na-collector.md`** = **Qi Zhang**,
>   산둥대, **anode-free + Na 집전체 + 나노결정–비정질 Li2S**, SE **LPSCBr**.
> - 둘은 **서로 다른 논문**이고 인용할 때 slug 로 구분한다. "Zhang 2026" 이라고만 쓰면 안 된다.

## 왜 이 논문을 흡수하는가

[[reference-cell-500-600-mahg]] 의 **H5(기계적 제한)** 가설 — *"첫 충전에서 Li2S 가 크게 수축하면서
균열이 생겨 접촉을 잃는다. 그리고 셀의 구속 방식(정압 vs 정용적)이 그 손실을 좌우한다"* — 의
**정면에 있는 논문**이다. 제목 자체가 "strain-coordination" 이고, 이 위키의 H5 근거 4편
(Cronk 2026 · Qu 2025 · Jeong 2026 · Kim 2025) 중 어느 것도 하지 않은 일을 한다:
**응력(stress)을 전극별로 분해해 측정하고, 그 분해를 설계 변수로 되돌려 쓴다.**

단, **활물질이 Li2S 도 S8 도 아닌 FeS2** 다. Li2S 는 **방전 생성물**로 in-situ 생성된다
(FeS2 + 4 Li → Fe⁰ + 2 Li2S). 그러므로 우리 Li2S 양극과 **방향이 반대**다 — 우리는 Li2S 에서
출발해 충전에서 수축하고, 이 논문은 방전에서 Li2S 를 만들며 팽창한다. 같은 물리의 반대 부호다.

## 표기 규칙

`[인쇄]` 원문 글자 그대로 · `[도표]` 그림에서 읽은 근사값 · `[해석]` 우리 판단 ·
`[재현]` 원문 값의 산술 환산(식 병기).

**이 논문의 비용량 기준은 전부 `mAh g⁻¹(FeS2)`** 다 (원문은 그냥 `mAh/g` 로 쓰고 Fig. 5·6 의
`AM: 1.6 mg/cm²`, `1C: 800 mA/g` 로만 간접 확정된다 — G5). 이 위키 규율에 맞추기 위해
digest 전체에서 **양단위 환산을 `[재현]` 으로 병기**한다:

| 환산 | 계수 | 유도 |
|---|---|---|
| `mAh g⁻¹(FeS2)` → `mAh g⁻¹(S)` (FeS2 안의 황 질량 기준) | **× 1.871** | M(FeS2)/M(S₂) = 119.97/64.12 |
| `mAh g⁻¹(FeS2)` → `mAh g⁻¹(Li2S)` (방전 생성 Li2S 질량 기준) | **× 1.3054** | M(FeS2)/(2 M(Li2S)) = 119.97/91.90 |
| FeS2 이론용량 (4 e⁻) | **893.6 mAh g⁻¹(FeS2)** | 4 × 26801 / 119.97 |
| 같은 값의 다른 분모 | **1672 mAh g⁻¹(S)** · **1166 mAh g⁻¹(Li2S)** | 위 두 계수 적용 — Li2S 이론용량 1166 과 일치한다 |

전압은 원문이 두 기준을 섞어 쓴다. Methods 의 전압창은 **셀 전압(vs LixSi)** 이고 Fig. 5b·5e·7e 의
축은 **`V vs Li⁺/Li`** 다. 차이 **0.35 V** 가 LixSi 의 기준전위다 (G7).

---

# 원문에 없어서 확인이 필요한 것 (공백표)

**이 논문에서 가장 중요한 산출물이다.** SI(Supplementary Information)를 확보하지 못했으므로
`Figure S1–S22`, `Table S1–S6`, `Supplementary Movie 1` 에 걸린 항목은 전부 **"SI 미확보"** 로
적는다 — 추측하지 않는다.

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | **볼밀 조건이 절반만 적혀 있다.** `[인쇄]` "placed in a **zirconia jar** containing **zirconia balls** and milled at **300 rpm for 2 h** using a **planetary** ball milling apparatus." **BPR(ball-to-powder ratio)·볼 지름·볼 개수·용기 부피·분말 투입량·휴지(rest) 주기·정회전/역회전·단계 수가 전부 없다.** | 우리 [[composite-cathode-mixing-routes]] 표의 열이 통째로 빈다. Kim 2025 가 **같은 조성·같은 부피분율에서 밀링 이력만으로 σ_Li⁺ 를 6배** 바꿨으므로, 300 rpm 2 h 라는 숫자만으로는 재현이 불가능하다. |
| **G2** | **볼밀을 글로브박스 밖에서 했는지 불명.** `[인쇄]` "**Except for ball milling**, all sample preparation procedures were carried out in an Ar-filled glovebox (O₂ <0.1 ppm, H₂O < 0.1 ppm)." | 문장 그대로 읽으면 **밀링만 Ar 글로브박스 밖**이다. 용기를 밀봉해 꺼냈다는 말이 없다. 황화물 SE + FeS2 를 대기에서 밀면 H2S 가 난다. **밀봉 여부가 안전·재현의 핵심인데 한 글자도 없다.** |
| **G3** | **첫 방전 740.0 mAh g⁻¹ 이 자기 그림과 맞지 않는다.** `[인쇄]` "a high initial discharge capacity of **740.0 mAh g⁻¹**". 그런데 `[도표, Fig. 5a]` 같은 조건(15 MPa · 25 °C · 0.1 C · AM 1.6 mg cm⁻²)의 **1사이클 빨간 점은 ≈650** 이다. 같은 패널의 Li‖FeS2 1사이클 ≈603 은 본문의 599.9 와 맞는다. | **대조군 숫자는 그림과 맞는데 주장군 숫자만 90 mAh g⁻¹(FeS2) 높다** (`[재현]` 740/650 = 1.14). 740.0 의 출처(다른 셀? 다른 그림?)가 본문에 없다. 우리가 인용해야 하는 값은 **≈650** 쪽이다. |
| **G4** | **"maintains high capacity retention after 30 cycles" 에 숫자가 없고, 50 사이클에서는 명백히 꺾인다.** `[도표, Fig. 5a]` 빨간 점 궤적 = 1사이클 **≈650** → 12–22사이클 **최대 ≈665** → 50사이클 **≈450**. `[재현]` 50사이클/최대 = **68 %**, 50사이클/1사이클 = **69 %**. | **저압(15 MPa) 상온 셀의 진짜 수명은 50사이클에 ≈69 %** 다. 본문은 그 구간을 "30 cycles" 로 끊어 말한다. 이 논문의 "long-cycling" 은 **100 MPa 에서만** 성립한다 (§7). |
| **G5** | **비용량의 분모를 글자로 명시한 문장이 없다.** 본문·Methods 어디에도 "based on FeS2" 가 없다. | `[재현]` Fig. 5d `AM: 1.6 mg/cm²` + Fig. 6b `1C: 800 mA/g` → 1 C 전류 = 0.8 A g⁻¹ × 1.6 mg cm⁻² = **1.28 mA cm⁻²**, 그리고 본문의 4 C = 5.3, 15 C = 19.7, 40 C = 52.58 mA cm⁻² 가 각각 **5.12 / 19.2 / 51.2** 와 맞는다 → **분모는 FeS2 질량**으로 확정. 다만 이것은 우리가 한 재구성이고 논문은 말하지 않는다. |
| **G6** | **N/P 비가 논문 안에서 세 가지로 다르다.** `[인쇄, Fig. 1a·1b 캡션]` "**N/P = 1**" · `[인쇄, Methods]` "The N/P ratio of the full cell is **~1.5**" · `[재현]` Si 3 mg cm⁻²(Li2Si → Si + 2Li = 1908 mAh g⁻¹(Si)) = **5.72 mAh cm⁻²** vs FeS2 1.6 mg cm⁻² × 893.6 = **1.43 mAh cm⁻²** → **N/P ≈ 4.0**. | **strain-coordination 은 N/P 에 직접 의존한다** — 양극 팽창과 음극 수축의 크기를 맞추는 것이 전략의 전부인데, 그 비가 1 / 1.5 / 4 중 무엇인지 모른다. 전략의 정량적 근거가 흔들린다. |
| **G7** | **전압 기준이 두 개인데 환산 근거가 없다.** `[인쇄, Methods]` LixSi‖FeS2 **0.65–2.65 V**, Li‖FeS2 **1–3 V**. `[도표, Fig. 5b·5e]` 축은 **`V vs Li⁺/Li`, 1.0–3.0 V**. `[재현]` 차 = **0.35 V** = LixSi 기준전위. | 그 0.35 V 의 출처(실측인지 문헌인지)가 없다. 우리 Li–In(≈0.62 V vs Li/Li⁺) 과 다른 기준이므로 활성화 전위 사다리에 올릴 때 반드시 밝혀야 한다. |
| **G8** | **양극 조성 `20:40:4` 가 100 이 아니다.** `[인쇄]` "FeS2 … LPSC … VGCF in a **20:40:4 or 50:42:8 (wt%)** ratio". 두 번째는 합이 100 이고 첫 번째는 **합이 64** 다. | `[재현]` 정규화하면 **FeS2 31.3 : LPSC 62.5 : VGCF 6.3 wt%**. 어느 셀에 어느 조성을 썼는지도 안 적혀 있다 — Fig. 5·6 의 `AM 1.6 / 2.2 / 30.5 mg cm⁻²` 중 고로딩 셀만 `[인쇄]` "50 wt% FeS2" 로 확인된다. |
| **G9** | **운전 압력을 "유지" 하는지 "초기값" 인지 안 적혀 있다.** `[인쇄]` 셀은 "homemade mold cells consisting of **stainless-steel clamping fixtures**, a **PEEK** outer sleeve, and an **alumina ceramic** inner liner (⌀10 mm)". 스프링도 로드셀 피드백도 언급이 없다. | **Qu 2025 의 핵심 발견이 "정압 63 % vs 정용적 50 %" 였다.** 이 논문은 응력을 **측정**하므로(§3) 적어도 응력 측정 셀은 **정용적**이다. 그렇다면 4,500·140,000 사이클 셀의 15/100 MPa 는 **초기 체결값**일 가능성이 높고, 사이클 중 압력 추이는 **보고되지 않는다**. |
| **G10** | **140,000 사이클(15 C) 그림이 SI 에 있다.** `[인쇄]` "243.6 mAh g⁻¹ ( ~ 0.39 mAh cm⁻²) after 140,000 cycles at 15 C (19.7 mA cm⁻²) (Fig. 6a and **Figure S15**)". Fig. 6a 의 x축 최대는 **30,000** 이다. | **초록의 헤드라인 숫자를 본문 PDF 만으로는 검증할 수 없다.** SI 미확보. |
| **G11** | **"After activation" 의 정의가 없다 — 85 % 의 분모가 불명.** `[인쇄]` "**After activation**, the Li2Si‖FeS2 cell delivers a capacity of **411 mAh g⁻¹ after ~4500 cycles at 1 C, corresponding to 85 % capacity retention**." `[재현]` 411/0.85 = **483.5** 가 분모다. `[도표, Fig. 6a 상단]` **1사이클 방전 ≈580**, 2사이클 이후 밴드 **≈440–520(중심 ≈480)**, 2,000사이클 부근 최대 **≈510**, 4,500사이클 **≈415**. | 분모 483.5 는 **첫 사이클(≈580)이 아니라 활성화 후 어느 초기 사이클**이다. `[재현]` **1사이클 기준이면 71 %**, **최대값(≈510) 기준이면 81 %**, 저자 기준이면 85 %. **이 위키가 Yu 2024·Kim 2025 에서 지적한 "분모 바꿔치기" 와 같은 유형**이다. |
| **G12** | **고로딩 셀의 C-rate 가 본문과 그림에서 10배 다르다.** `[인쇄]` "achieves an high areal capacity of **21.7 mAh cm⁻² at 0.1 C** over 100 cycles (Fig. 6c)". `[도표, Fig. 6c]` 패널 안의 조건 라벨은 "**1C**" 이고 좌상단에 "1C: 800 mA/g" 이 따로 있다. | 30.5 mg cm⁻²(FeS2) × 800 mA g⁻¹ = `[재현]` **24.4 mA cm⁻²** 다. 그 전류로 21.7 mAh cm⁻² 를 뽑았다면 이 분야의 기록을 한 자릿수 갈아치우는 주장이고, 0.1 C 라면 평범하게 훌륭한 결과다. **본문과 그림 중 하나가 틀렸고 주장 크기가 10배 달라진다.** |
| **G13** | **파우치셀 619.2 Wh kg⁻¹ 의 분모가 FeS2 56 mg 뿐이다.** `[인쇄]` "442.3 mAh g⁻¹ in the second cycle, corresponding to **619.2 Wh/kg (based on active material, Table S6)**" + Methods 의 파우치 질량표: 양극 복합체 **112 mg**(FeS2 56 · LPSC 47.04 · VGCF 8.96), SE 분리막 **253 mg**(~90 µm), Li2Si 음극 **~60 mg**. | `[재현]` 평균전압 = 619.2/442.3 = **1.40 V**; 에너지 = 0.056 g × 0.6192 Wh g⁻¹ = **34.7 mWh**; 적층 질량 112+253+60 = **425 mg** → **81.6 Wh kg⁻¹**. 집전체·탭·파우치를 더하면 더 낮다. **619.2 와 81.6 은 7.6배 차이**이고 Table S6 는 미확보다. |
| **G14** | **Li‖FeS2 대조셀의 성형 압력이 다르다.** `[인쇄]` "For Li\|LPSC\|FeS₂ cells, the LiₓSi alloy layer were replaced by fresh Li foil and **the final pressing pressure is 15 MPa**" — Li2Si 셀은 **500 MPa**. | **대조 실험이 변수 하나만 다르지 않다.** 음극 종류와 **최종 성형 압력이 33배** 함께 바뀌었다. Li‖FeS2 가 10사이클에 25 % 로 죽은 것(§6)에 성형 압력 차이가 얼마나 기여했는지 **분리 불가능**하다. 이 논문의 가장 큰 설계 결함이다. |
| **G15** | **두께 변화 ~1.4 µm 와 XCT 수치가 맞지 않는다.** `[인쇄]` "the total thickness change of the FeS2-based cell was only **~1.4 μm**" vs `[인쇄]` XCT 양극 **56 → ~68 µm (+12)**, 음극 **28 → ~13 µm (−15)**. `[재현]` 순변화 = **−3 µm**. 게다가 `[인쇄]` XCT 해상도는 **~4 µm** 다. | −3 µm(XCT)과 −1.4 µm(레이저 변위) 가 2배 다르고, **XCT 의 ±4 µm 해상도로는 둘을 구분할 수 없다.** 두 측정은 **서로 다른 셀**(XCT는 양극 56 µm, 광학현미경 셀은 양극 ~20 mg cm⁻²)이기도 하다. |
| **G16** | **"charge 때 수축" 인지 "discharge 때 수축" 인지 본문이 자기모순이다.** `[인쇄, §응력]` "cell stress initially **decreases during discharge**, suggesting Li2Si shrinkage exceeds FeS2 expansion" · `[인쇄, §변형]` "the Li2Si‖FeS2 cell **first contracts during charge** and then expands during discharge, **aligning with the stress behavior in Fig. 2e**". | `[도표, Fig. 3f]` 전압이 2.6 → 0.7 V 로 **먼저 내려가고(방전)** 그때 두께가 0 → **−1.5 µm** 로 줄어든다. 즉 **수축은 방전에서 일어난다** — 응력 절(Fig. 2e)이 맞고 변형 절 문장이 틀렸다. |
| **G17** | **σc 의 정의식이 없다.** `[인쇄]` "we normalized the maximum stress change by capacity. The stress change per capacity (σc)…". 분모가 **최대 응력이 나타난 용량**인지 **총 용량**인지 적지 않았다. | `[재현]` Fig. 2b 최대 0.72 MPa @ ≈0.9 mAh → 0.80 ✓ (최대점 용량 기준). 그런데 셀마다 총 용량(1.8 / 1.9 / 1.87 mAh)이 다르므로 **σc 의 화학 간 비교는 용량 차이와 섞여 있다.** NCM 0.213 · LCO **−0.1558** 의 부호가 다른 이유도 설명이 없다. |
| **G18** | **DRT 귀속의 근거가 그림에 보이지 않는다.** `[인쇄]` τ 10⁻⁵~10⁻⁶ s = 입자 접촉, 10⁻³~10⁻² s = 공극에 의한 접촉 상실, 10⁻²~1 s = 음극/SSE 계면 확산, ~10 s = 셀 분극. | `[도표, Fig. 4b·4c]` 두 패널 모두 **τ ≈ 10 s 의 큰 봉우리 하나가 신호를 지배**하고, 화살표가 가리키는 10⁻⁵·10⁻³ 영역은 배경(청록)과 거의 구분되지 않는다. 컬러바는 0–380 Ω. **"fewer peaks" 는 정성 진술이고 피크 면적·저항값이 표로 주어지지 않는다.** |
| **G19** | **사이클 데이터의 셀 개수와 선택 기준.** `[인쇄]` "**At least three** independent pellet cells were tested… The representative data shown in the manuscript were **selected from cells exhibiting consistent electrochemical behavior**. For mechanistic characterizations, operando/in situ measurements, and pouch-cell tests, **one or two** representative cells were assembled." | **이 위키 digest 13편 중 셀 개수를 밝힌 몇 안 되는 논문**이라는 점은 평가한다. 그러나 "consistent 한 셀에서 골랐다" 는 **선택 편향을 스스로 적은 문장**이고, 오차막대·분포는 어디에도 없다. operando·파우치는 **n = 1–2**. |
| **G20** | **SE 자신의 용량 기여를 분리한 대조셀이 없는데, 본문은 SE 환원을 용량 증가의 원인으로 지목한다.** `[인쇄]` 55 °C 50사이클에 용량이 **807 mAh g⁻¹ 로 증가**하는 것을 "attributed to **LPSC reduction to Li2S by VGCF and Fe particles**, enhancing the Li2S/S conversion reaction" 으로 설명한다. | **자기 손으로 "SE 가 Li2S 가 되어 용량에 섞인다" 고 적어 놓고 `LPSC + VGCF` 대조셀을 돌리지 않았다.** 이 위키의 **0번 실험**(`LPSCl + AB 80:20` 대조셀)이 또 필요해진 열세 번째 사례다. 4 C 에서 30,000 사이클에 걸쳐 용량이 `[도표]` **≈250 → ≈340** 으로 오르는 것도 같은 의심을 받는다. |
| **G21** | **LixSi 조성 확정의 근거가 SI 에 있다.** `[인쇄]` Li 박 **22 / 45 / 65 µm (⌀8 mm) = 0.6 / 1.2 / 1.8 mg**, Si 필름 **~3 mg cm⁻² (⌀10 mm)**, "LiₓSi … **in situ formed by brief contact**". 상 동정은 `Figure S11–S14`(미확보). | `[재현]` ⌀10 mm Si 전체가 리튬화된다고 가정하면 Si 2.36 mg = 0.0839 mmol, Li 1.2 mg = 0.173 mmol → **x = 2.06** ✓. 그러나 **Li 박은 ⌀8 mm 로 Si 보다 작다** — 접촉 면적 밖의 Si 까지 리튬화됐다는 가정이 필요하고 그 근거가 없다. 겹친 면적만 반응하면 **x ≈ 3.2** 다. |
| **G22** | **SI 전반 미확보.** `Figure S1`(응력 재분배 모식도) · `S2`(압력별 EIS, 356 Ω 의 출처) · `S3–S5`(NCM·LCO·LixSi σc) · `S6`(광학현미경 보조) · `S7–S9`(XCT 단면) · `S10`(파우치 LED) · `S11–S14`(상·형상) · `S15`(140,000 사이클) · `S16`(방전 STEM) · `S17`(30 MPa, 94.3 %) · `S18–S19`(FeS2 55·60 wt%) · `S20`(율속별 응력) · `S21–S22`(DRT 보조) · `Table S1–S6` · `Supplementary Movie 1`. | 위 G 항목 다수가 SI 를 받으면 해소된다. **재요청 시 우선순위: Figure S2(압력-EIS) → Figure S15(140,000) → Table S6(에너지밀도 분모) → Figure S17(30 MPa).** |

---

## 0. 서지사항

| 항목 | 값 |
|---|---|
| 제목 | `[인쇄]` Strain-coordination strategy enabling long-cycling all-solid-state lithium-sulfur batteries |
| 저자 | Jiaxu Zhang¹²⁴, Shengjie Xia¹⁴, Pushun Lu¹², Suzhe Liang¹², Jiamin Fu³, Zhimin Zhou¹, Wenlin Yan¹, Guantai Hu¹², Kaiyong Tuo¹², Jian Hong¹, Shutao Zhang¹, Ziqing Wang¹, **Xueliang Sun**¹, **Changhong Wang**¹ |
| 소속 | ¹ Eastern Institute for Advanced Study / Eastern Institute of Technology, Ningbo (Ningbo Key Laboratory of All-Solid-State Battery; Ningbo Institute of Digital Twin) · ² USTC 화학재료과학원(허페이) · ³ University of Western Ontario 기계·재료공학과 · ⁴ 공동 제1저자 |
| 교신 | xsun@eitech.edu.cn · cwang@eitech.edu.cn |
| 저널 | *Nature Communications* **17** (2026) 7858 |
| DOI | 10.1038/s41467-026-74625-5 |
| 투고/수리 | `[인쇄]` Received 28 August 2025 · Accepted 9 June 2026 |
| 참고문헌 | 60편 |
| 본문 그림 | 7개 (Fig. 1–7). SI 는 **미확보** |

---

## 1. 한 문단 요약

전고체 Li–S 셀이 **수백 MPa 의 운전 스택 압력**을 요구하는 이유는 양극의 큰 부피변화와 음극의
부피변화가 **같은 방향으로 어긋나** 계면 접촉을 잃기 때문이다. 이 논문은 그 둘을 **반대 부호로
맞춰 상쇄**시키는 전략을 제안한다: 방전에서 **팽창하는 FeS2 양극**과 방전에서 **수축하는 Li2Si
(prelithiated Si) 음극**을 짝지어, 셀 전체의 몰부피 변화를 **Li 음극의 −17.2 % 에서 +2.6 %** 로
줄인다. 저자들은 **LTO(zero-strain) 대극**을 기준자로 써서 각 전극의 **용량당 응력 변화 σc** 를
따로 측정하고(FeS2 0.80 · Li2Si 0.88 · Li 금속 1.03 MPa mAh⁻¹), 둘을 합친 실제 셀에서
**0.16 MPa mAh⁻¹ (−80 %)** 를 얻었으며, Lagrange 보간으로 두 곡선의 합이 실측과 겹침을 보였다.
In-situ 광학현미경·ex-situ XCT·레이저 변위계로 **셀 총 두께 변화 ~1.4 µm** 를 보고하고, 그 결과
**15 MPa** 라는 낮은 운전 압력에서 상온 0.1 C 첫 방전 `[인쇄]` **740.0** (대조 Li 음극 599.9),
55 °C 0.05 C **868.4 mAh g⁻¹(FeS2)**, 파우치셀 500사이클을 보고한다. **100 MPa** 에서는 1 C
4,500사이클(85 % 유지), 4 C 30,000사이클, 15 C 140,000사이클, 그리고 **30.5 mg cm⁻²(FeS2) 고로딩
셀에서 21.7 mAh cm⁻²** 를 보고한다. **우리에게 중요한 것은 성능 숫자가 아니라 측정 체계**다 —
LTO 기준자 + 용량 정규화 응력 + 레이저 변위라는 **3종 세트**가 H5 를 판정하는 도구다.

---

## 2. ★ "strain-coordination" 의 실체 — 무엇을 무엇과 조율하는가 (Fig. 1)

**한 문장으로**: *양극 활물질의 **팽창**과 음극 활물질의 **수축**이 같은 전기화학 스텝에서
일어나도록 음극 재고(Li-to-Si 비)를 조절해, **셀 적층 전체의 몰부피 변화 합을 0 근처로 만드는
것**.* 입자 수준의 응력 분산도, SE 의 연성을 쓰는 것도 아니다 — **전극 쌍(pairing) 설계**다.

### 2.1 몰부피 회계 `[인쇄, §Design Principles]`

| 물질 | 몰부피 (cm³ mol⁻¹) |
|---|---|
| FeS2 | **24.1** |
| Li | **12.9** |
| Fe | **7.1** |
| Li2S | **27.8** |
| Li2Si | **30.3** |
| Si | **12.1** |

**(a) Li 음극 셀** — `FeS2 + 4 Li → Fe + 2 Li2S`
`[재현]` 좌변 24.1 + 4×12.9 = **75.7** → 우변 7.1 + 2×27.8 = **62.7** cm³ mol⁻¹
→ **ΔV = −17.2 %** (`[인쇄]` 와 일치: (62.7−75.7)/75.7 = −17.17 %).

**(b) Li2Si 음극 셀** — `[인쇄]` 반응식 두 개:
```
FeS2 + Li2Si → FeS + Li2S + Si
FeS  + Li2Si → Fe  + Li2S + Si
```
`[재현]` 좌변 24.1 + 2×30.3 = **84.7** → 우변 7.1 + 2×27.8 + 2×12.1 = **86.9** cm³ mol⁻¹
→ **ΔV = +2.6 %** (`[인쇄]` 와 일치: +2.60 %).

### 2.2 ★ 중요 — **−17.2 %(셀 수준)와 +259 %(양극 수준)는 다른 숫자다**

`[인쇄, Fig. 7e]` "Initial: FeS2, **V = 100 %**" → "Discharge State: Li2S + Fe⁰, **V = 259 %**",
그리고 본문 `[인쇄]` "the large volume change (**259 %**) of FeS2 compared to NCM (~7 %) and
LCO (~4 %)".

`[재현]` 양극 **고체 생성물만** 세면 24.1 → 7.1 + 55.6 = 62.7 cm³ mol⁻¹ = **260 %** ✓.
즉 **259 % 는 "리튬을 빼고 센 양극 부피"** 이고, **−17.2 % 는 "리튬까지 넣어 센 셀 부피"** 다.

`[해석]` **이 구분이 우리 H5 를 읽는 핵심이다.** Cronk 2026 의 Li2S 전극 **45 → 26 µm (−42 %)**,
Qu 2025 의 Li2S 양극 **−19 µm**, Jeong 2026 의 **+46.6 %** 는 전부 **양극 수준**이고,
이 논문의 **−17.2 % / +2.6 %** 는 **셀 수준**이다. 같은 표에 나란히 두면 안 된다.
이 논문에서 우리 양극 수치와 직접 비교 가능한 것은 **XCT 의 양극 56 → 68 µm (+21.4 %)** 뿐이다 (§4.2).

### 2.3 설계 변수 — 무엇을 돌렸나

`[인쇄]` Li-to-Si 몰비를 **1:1, 2:1, 3:1** 로 바꿔 **LiSi / Li2Si / Li3Si** 를 만들고,
σc 가 FeS2 와 가장 가까운 **Li2Si** 를 골랐다 ("Given the **similar σc values** of FeS2 and Li2Si,
we paired FeS2 positive electrode with a Li2Si negative electrode").

구현은 **Li 박 두께**다 `[인쇄, Methods]`: Si 필름(⌀10 mm, ~3 mg cm⁻², ~30 µm) 위에
**22 / 45 / 65 µm (⌀8 mm) Li 박 = 0.6 / 1.2 / 1.8 mg** 을 셀 조립 중 접촉시켜 **in situ** 합금화.
→ **설계 변수는 "Li 박 두께 45 µm" 라는 한 숫자**다. (근거의 공백은 G21.)

`[해석]` **값싼 전략이다.** 새 물질·새 첨가제·새 코팅이 아니라 **음극 리튬 재고의 양**만 돌렸다.
우리 [[anode-free-li2s-assb]] 축과 정확히 같은 변수(Li 재고)를 **반대 목적**으로 쓴다 —
우리는 Li 를 줄이려 하고 이들은 **부피 상쇄를 위해 Li 를 정확히 맞춘다.**

---

## 3. 응력 분석 — LTO 기준자 (Fig. 2) `[인쇄 + 도표]`

### 3.1 방법

`[인쇄]` **Li4Ti5O12(LTO)** 를 대극으로 쓴다 — 충·방전 부피변화가 **~0.2 %** 라서
"observed stress changes primarily originate from the **working electrode**".
측정은 `[인쇄, Methods]` "custom-built **pressure-measuring device integrated with a force sensor**"
(CHUANGLI Ningbo), **25 °C, 운전 압력 15 MPa, ~0.1 mA cm⁻²**.

`[해석]` **Qu 2025 와 같은 트릭이다** — Qu 도 LTO∣LPSCl∣LTO 대조셀로 SE 의 부피 기여를 뺐다.
두 논문이 독립적으로 같은 기준자를 골랐다는 사실 자체가 이 방법의 신뢰도를 올린다.
다만 **Qu 는 변위(LVDT)를 재고 이 논문은 응력(force sensor)을 잰다** — 전자는 정압, 후자는 정용적이다.

### 3.2 용량당 응력 변화 σc

| 전극 (셀 구성) | σc (MPa mAh⁻¹) | `[도표]` 최대 응력 / 그때의 용량 | 부호 |
|---|---|---|---|
| **FeS2** (LTO‖FeS2, Fig. 2b) | **0.80** | **+0.72 MPa** @ ≈0.9 mAh (총 1.8 mAh) | **+** (리튬화 = 팽창) |
| **Li2Si** (LTO‖Li2Si, Fig. 2c) | **0.88** | **−0.85 MPa** @ ≈0.95 mAh (총 1.9 mAh) | **−** (탈리튬화 = 수축) |
| **Li 금속** (LTO‖Li, Fig. 2d) | **1.03** | **−0.97 MPa** @ ≈0.95 mAh (총 1.87 mAh) | **−** |
| **LiSi** (SI) | **0.71** | SI 미확보 | — |
| **Li3Si** (SI) | **0.94** | SI 미확보 | — |
| **NCM** (LTO‖NCM, SI) | **0.213** | SI 미확보 | + |
| **LCO** (LTO‖LCO, SI) | **−0.1558** | SI 미확보 | − |
| **★ Li2Si‖FeS2 실셀** (Fig. 2e) | **0.16** | `[도표]` **−0.17 / −0.19 MPa** 두 번의 얕은 골 | 거의 평탄 |

`[인쇄]` "the total stress … of the Li2Si‖FeS2 cell is **reduced by 80 %**, with a σc of 0.16".
`[재현]` 0.16/0.80 = 0.20 → 확실히 **FeS2 단독 대비 −80 %** 다.

`[재현]` **이상적 상쇄라면 |0.80 − 0.88| = 0.08 이어야 하는데 실측은 0.16, 즉 2배다.**
논문은 이 차이를 언급하지 않는다.

`[인쇄]` 검증 — "the σc of NCM is 0.213, and the σc of LCO is −0.1558. These results are
**consistent with the large volume change (259 %) of FeS2 compared to NCM (~7 %) and LCO (~4 %)**,
confirming the **reliability of this measurement**."
`[해석]` 7 %/4 % 대 259 % 는 **37–65배**인데 σc 는 0.80 대 0.213/0.156 으로 **4–5배**다.
"consistent" 는 **순서가 맞는다**는 뜻 이상으로 읽으면 안 된다 (G17).

### 3.3 ★ 응력 궤적의 모양 — 이게 진짜 결과다 `[도표, Fig. 2e]`

Li2Si‖FeS2 셀 응력은 단조롭지 않다. **0 → −0.17 (≈0.6 mAh) → −0.07 (≈0.95 mAh) →
−0.19 (≈1.3 mAh) → 0 (1.85 mAh)** 의 **W 자**다.

`[인쇄]` "cell stress **initially decreases** during discharge, suggesting **Li2Si shrinkage
exceeds FeS2 expansion**. As discharge continues, **stress increases**, indicating FeS2 expansion
dominates."

`[해석]` 즉 **상쇄는 매 순간 완전하지 않다** — 전체 행정에서 "누가 이기는가" 가 두 번 바뀐다.
전략의 올바른 표현은 "zero-strain" 이 아니라 **"peak strain 을 80 % 깎는다"** 다.
논문 자신도 `[인쇄]` "**quasi** zero-strain" 이라고 쓴다.

### 3.4 Lagrange 보간 검증 `[도표, Fig. 2f]`

x축 **normalized capacity (%)**, y축 **normalized pressure (MPa)**.
`[도표]` FeS2 (검정) 최대 **+0.72** @ 50 % · Li2Si (빨강) 최소 **−0.87** @ 50 % ·
FeS2+Li2Si 실측(파랑) **−0.05 ~ −0.20 사이 평탄** · 보간합 `y1fit+y2fit`(연파랑 원)이 그 위에 겹침.
`[재현]` 0.72 + (−0.87) = **−0.15** — 실측 평탄선의 높이와 맞는다. **산술이 자기 그림과 맞는 드문 사례다.**

---

## 4. 변형 분석 — 두께를 세 가지로 쟀다 (Fig. 3) `[인쇄 + 도표]`

### 4.1 In-situ 광학현미경 (Fig. 3a–c)

`[인쇄, Methods]` YUESCOPE **YD650**, Ar 글로브박스 안. **성형 압력 250 MPa**, 관측을 쉽게 하려
**두꺼운 전극**(양극 **~20 mg cm⁻²**, 음극 **~12 mg cm⁻²**) 사용. 펠릿을 **탈형(demolding)** 해
셀 홀더로 옮겨 단면을 본다.

`[도표, Fig. 3a–c]` 3장 모두 scale bar **200 µm**, 위에서부터 `FeS2 / LPSC / Li2Si` 3층에 흰 점선
경계. 충전상태 → 방전상태 → 재충전상태로 가면서 **빨간 ΔV 화살표**가 양극 경계는 아래로(두꺼워짐),
음극 경계는 위로(얇아짐) 이동함을 표시한다. **두께 수치 자체는 그림에 없다.**

`[해석]` ⚠ **탈형한 펠릿을 보는 것이므로 운전 압력이 걸린 상태가 아니다.** 그리고 이 셀은
성능 셀(1.6 mg cm⁻²)보다 **양극이 12배 두껍다.** 정성 관측으로만 쓸 수 있다.
`Supplementary Movie 1`, `Figure S6` 미확보.

### 4.2 ★ Ex-situ XCT — 우리 축에 직접 걸리는 유일한 수치 (Fig. 3d–e)

`[인쇄, Methods]` Carl Zeiss **Xradia 610 & 620 Versa**, 사이클 후 Ar 글로브박스에서 분해 →
플라스틱 필름 밀봉, 중앙 **2 × 2 mm** 영역 스캔, **해상도 ~4 µm**.

| 층 | pristine `[인쇄]` | 방전 후 `[인쇄]` | `[재현]` 변화 |
|---|---|---|---|
| **FeS2 양극** | **~56 µm** | **~68 µm** | **+12 µm = +21.4 %** |
| **LPSC 분리막** | **~268 µm** | (수치 없음) | — |
| **Li2Si 음극** | **~28 µm** | **~13 µm** | **−15 µm = −53.6 %** |
| **합(양극+음극)** | 84 µm | 81 µm | `[재현]` **−3 µm** |

`[해석]` **우리 Li2S 양극과 부호만 반대인 같은 사건이다.** Li2S 가 생기면서 양극이 **+21 %**
두꺼워진다. Cronk 2026 은 Li2S 가 없어지면서 **−42 %** 얇아졌다. 두 값의 차이는 (i) Li2S 가
복합체의 **일부**인가 **전부**인가, (ii) 기공이 팽창을 흡수하는가에서 온다.

`[재현]` **일관성 검산** — 20:40:4 조성(`[재현]` FeS2 31.3 wt%)에서 밀도 FeS2 4.9 ·
LPSC ≈1.86 · VGCF ≈2.0 g cm⁻³ 로 보면 FeS2 **≈14.8 vol%**. 활물질 부피가 **+159 %**(100→259 %)
늘고 기공이 전혀 흡수하지 않으면 두께는 0.148 × 1.59 = **+23.5 %** → 실측 **+21.4 %** 와
2 %p 안에서 맞는다. **즉 이 복합양극의 기공은 팽창을 거의 흡수하지 못한다.**
(이 검산은 우리 계산이고 논문에 없다.)

### 4.3 In-situ 두께 (정압 조건) (Fig. 3f)

`[인쇄, Methods]` **SPFT2000 IESTTECH**, 캡션 `[인쇄]` "measured using **laser displacement sensors
combined with a force sensor**", 본문 `[인쇄]` "thickness variations were in situ recorded
**under constant pressure**".

`[도표, Fig. 3f]` 상단 전압 2.6 → **0.7 V** (≈7.5 h, 방전) → 2.6 V (15 h, 충전).
하단 두께 **0 → −1.5 µm** (≈5 h에 도달, 10.5 h까지 평탄) → **−0.1 µm** (15 h).
`[인쇄]` "the total thickness change of the FeS2-based cell was only **~1.4 μm**, even smaller than
reported values for cells with NCM positive electrodes".

`[해석]` ★ **이 셀은 정압(constant pressure)이고 §3 의 응력 셀은 정용적이다.**
두 모드를 **같은 논문에서 둘 다 운용한 것은 Qu 2025 이후 두 번째**다. 그러나
**Qu 와 달리 두 모드의 성능(용량 유지)을 비교하지 않았다.** 이 논문이 가장 쉽게 할 수 있었던
실험 하나가 빠져 있다.

⚠ 수축 방향에 대한 본문 자기모순은 **G16** 참조 — 그림은 **방전에서 수축**을 보인다.

---

## 5. 동역학 — in-situ EIS/DRT 와 GITT (Fig. 4) `[인쇄 + 도표]`

### 5.1 측정 조건

`[인쇄]` 운전 압력 **15 MPa**, **첫 1.5 사이클**. 이유 `[인쇄]` "considering the **allotropic
transformation of FeS2 from cubic to orthorhombic** during the initial lithiation/delithiation".
EIS `[인쇄, Methods]` BioLogic **VSP-300**, **7 MHz – 20 mHz**, decade 당 10점, AC **10 mV**.
`[도표, Fig. 4a]` 전압축 3 → 1 V, 데이터점 1–24, 순서는 **방전(1–9) → 충전(10–16) → 방전(17–24)**.

### 5.2 DRT 귀속 `[인쇄]`

| τ | 귀속 | Li‖FeS2 | Li2Si‖FeS2 |
|---|---|---|---|
| 10⁻⁵ ~ 10⁻⁶ s | **입자 접촉·집전체** | 더 강함 | `[인쇄]` "weaker peak … indicating **improved particle contact**" |
| 10⁻³ ~ 10⁻² s | **Li 금속의 공극 형성에 의한 접촉 상실** (충·방전 끝에서 출현) | 출현 | `[인쇄]` "**fewer peaks**" |
| 10⁻² ~ 1 s | **음극/SSE 계면 Li 확산** | `[인쇄]` 큰 피크 — **Li/LPSC 부동태층** | 첫 방전에서 약함 = 빠른 계면 동역학 |
| ~10 s | **셀 전체 분극** | 강함 | 약함 |

`[도표, Fig. 4b·4c]` 컬러바 **0–380 Ω**. **두 패널 모두 τ ≈ 10 s 의 주황색 띠 하나가 신호를
지배**하고, Li‖FeS2 의 데이터점 1–4 에 **짙은 갈색(포화) 블롭**이 있다.
화살표가 가리키는 10⁻⁵·10⁻¹ 영역은 배경과 거의 구분되지 않는다 (G18).

### 5.3 GITT `[인쇄 + 도표]`

`[인쇄, Methods]` **0.1 C (~0.13 mA cm⁻²)**, **10 min 펄스 + 2 h 이완**, 10 s 마다 1점.

| | Li‖FeS2 | Li2Si‖FeS2 |
|---|---|---|
| 첫 방전 초기 D_Li `[인쇄]` | **4.1 × 10⁻¹² cm² s⁻¹** | **4.7 × 10⁻¹² cm² s⁻¹** |
| `[도표]` 전체 시간축 | ~250 h | ~380 h |
| `[도표]` logD 거동 | 초기 "**high slope**" 급락 → 사이클마다 상단선에 못 미침 (**"Irreversible loss"** 표시) | "**low slope**" → 매 사이클 상단선 회복 |

`[인쇄]` 방전 중 D_Li 의 비단조 거동 설명: ① (S–S)₂²⁻ 퍼설파이드 환원이 확산경로를 짧게 하고 구조를
크게 바꿔 D 가 내려가고, ② 층상 **γ-LixFeS2** 가 생기면 D 가 올라가며, ③ **Li₂FeS2** 로 완전 전환
후 Fe²⁺ → Fe⁰ 환원과 **저항성 Li2S 생성**으로 다시 내려간다.
`[인쇄]` "the Li2Si‖FeS2 cell exhibits **minimal irreversible D_Li loss**, unlike Li‖FeS2".

`[해석]` ★ **"저항성 Li2S" 라는 표현이 우리 H5 와 맞물린다.** 같은 셀에서 D_Li 를 떨어뜨리는 것이
Li2S 의 **생성**이고, 우리 셀에서는 Li2S 의 **분해(첫 충전)** 가 접촉을 끊는다. 방향만 반대다.
단, **4.1 vs 4.7 × 10⁻¹²** 의 차이는 **15 %** 로 측정 산포 안일 수 있다 — 논문은 오차를 주지 않는다.
(이 위키의 측정 규율: 고체셀 D_Li 는 CV 가 아니라 **GITT 또는 EIS–DRT** 로 — Wang 2026 교훈.
이 논문은 그 규율을 지켰다.)

---

## 6. 저압(15 MPa) 전기화학 성능 (Fig. 5) `[인쇄 + 도표]`

### 6.0 ★ 운전 압력 15 MPa 를 고른 근거 `[인쇄, §Stress Analysis]`

`[인쇄]` **성형 압력 500 MPa** 적용 후 운전 압력을 바꿔 가며 EIS (`Figure S2`, 미확보):

| 운전 압력 | 총 저항 |
|---|---|
| **0 MPa (무압)** | `[인쇄]` **356 Ω** — "due to **inadequate solid-solid contact**" |
| 1 / 3 / 5 / 10 MPa | `[인쇄]` "decreases **significantly**" (수치 없음) |
| **15 ~ 100 MPa** | `[인쇄]` "remains **nearly constant**" |

→ `[인쇄]` "**15 MPa is chosen as the optimal operating pressure**".

`[해석]` ★ **[[anode-free-li2s-assb]] 의 "무압 운전 불가" 항목에 세 번째 독립 근거가 생긴다.**
Qu 2025 의 "0 MPa 60사이클 붕괴" 와 같은 결론을 **EIS 한 장**으로 보인다.
다만 **1–10 MPa 구간의 수치가 없어** "최소 몇 MPa 인가" 는 여전히 못 정한다.
그리고 **이 EIS 는 FeS2/Li2Si 셀**이지 Li2S 양극이 아니다.

### 6.1 상온 사이클 (Fig. 5a) — 15 MPa · 25 °C · 0.1 C · AM 1.6 mg cm⁻²

| | `[인쇄]` 첫 방전 | `[도표]` 궤적 |
|---|---|---|
| **Li2Si‖FeS2** | **740.0 mAh g⁻¹(FeS2)** (⚠ G3) | 1사이클 **≈650** → 12–22사이클 최대 **≈665** → 50사이클 **≈450** |
| **Li‖FeS2** | **599.9 mAh g⁻¹(FeS2)** | 1사이클 **≈603** → 10사이클 **≈148** (`[인쇄]` "retains only **25 %** after 10 cycles"; `[재현]` 148/603 = 24.5 % ✓) |

`[재현]` 양단위 환산 (×1.871 / ×1.3054):

| 값 | mAh g⁻¹(FeS2) | mAh g⁻¹(S) | mAh g⁻¹(Li2S) | 면적용량 @1.6 mg cm⁻² | 이론 대비 |
|---|---|---|---|---|---|
| Li2Si 첫 방전 `[인쇄]` | 740.0 | **1384** | **966** | **1.18 mAh cm⁻²** | 82.8 % |
| Li2Si 첫 방전 `[도표]` | ≈650 | ≈1216 | ≈849 | ≈1.04 | 72.7 % |
| Li 첫 방전 `[인쇄]` | 599.9 | 1122 | 783 | 0.96 | 67.1 % |
| Li2Si 50사이클 `[도표]` | ≈450 | ≈842 | ≈587 | ≈0.72 | 50.4 % |

`[도표]` CE — Li2Si 셀의 빨간 빈 원은 초기부터 **≈99–100 %** 로 평탄. Li 셀의 파란 빈 원은
**100–105 % 사이에서 산포**한다. `[해석]` CE > 100 % (충전 > 방전)는 **SE 산화 또는 음극 Li 재고의
추가 공급**을 뜻한다 — 분리되지 않았다 (G20).

### 6.2 3사이클 전압곡선 (Fig. 5b)

`[도표]` 축 **`Potential (V vs. Li⁺/Li)` 1.0–3.0**, x축 0–800 mAh g⁻¹.
Li2Si 셀(빨강) 방전은 **≈2.0 V 의 넓은 경사** → **≈1.5 V 어깨** → 1.0 V 에서 **≈640** 종료.
Li 셀(파랑)은 **≈430** 에서 끝나고 `[인쇄]` "voltage **fluctuations** at the end of discharge …
caused by **void formation at the Li/SSE interface**" (Fig. 5b 의 빨간 점선 박스 + 확대 삽입도).
충전은 둘 다 **≈2.5 V 평탄부**를 지나 3.0 V 로 급상승한다.

`[해석]` ★ **충전 말기 2.6–3.0 V 구간이 `Li2S → S` 다** (Fig. 7e 의 귀속). 즉 이 셀에서
**in-situ 생성된 Li2S 는 2.6 V vs Li/Li⁺ 부근부터 산화된다** — 우리 상용 Li2S 의 활성화 전위
(Zhang(Qi) 2026 의 LSV 피크 3.05 V, Lee 2026 의 컷오프 3.62 V)보다 **훨씬 낮다**.
단 그 Li2S 는 **Fe⁰ 나노입자와 원자 수준으로 섞여 있고**(Fig. 7d) 밀링으로 만든 것이 아니다.
[[li2s-activation-first-charge]] 의 전위 사다리에 **"Fe⁰ 공존 in-situ Li2S ≈2.6 V"** 로 올릴 수 있다.

### 6.3 율속 (Fig. 5c) — 15 MPa · 25 °C

`[인쇄]` Li2Si‖FeS2: **697.0 / 617.3 / 564.7 / 528.4 / 498.9** mAh g⁻¹(FeS2) @ 0.1/0.2/0.3/0.4/0.5 C,
0.1 C 복귀 **632.0**. Li‖FeS2 는 0.1 C 복귀 **127.8**.
`[도표]` 그림의 "0.1C: 80 mA/g" 라벨 → `[재현]` 0.1 C = 80 mA g⁻¹ ⇒ **1 C = 800 mA g⁻¹** ✓ (G5 의 근거).
`[재현]` 복귀율 Li2Si **632.0/697.0 = 90.7 %** vs Li **127.8/≈300 = 43 %**.

`[인쇄]` `Figure S20` (미확보) — 율속이 높을수록 응력 응답이 약간 작아지며, 그 이유는
"the **lower delivered capacity** and thus reduced lithium transport".
`[해석]` **응력이 용량에 비례한다는 자기 주장의 자기 검증**이라 깔끔하다.

### 6.4 55 °C (Fig. 5d·5e) — 15 MPa · AM 1.6 mg cm⁻²

`[인쇄]` 0.05 C 에서 **868.4 mAh g⁻¹(FeS2)** (`[재현]` = **1625 (S)** = **1134 (Li2S)** =
**1.39 mAh cm⁻²** = 이론의 **97.2 %**).
`[인쇄]` 0.1 C 에서 50사이클 안정, **50사이클에 807 mAh g⁻¹ 로 오히려 증가**.
`[도표, Fig. 5d]` 1사이클 **≈870** → 2–8사이클 **≈765** 로 떨어졌다가 → 50사이클 **≈805** 로 단조 상승.
CE 빈 원은 **≈99–100 %** 평탄.
`[도표, Fig. 5e]` 3사이클(빨강)과 50사이클(파랑) 곡선이 거의 겹치고, 방전 종료가 **≈780 → ≈810** 으로
**50사이클 쪽이 더 길다.**

★ `[인쇄]` 용량 증가의 귀속: "This capacity increase is attributed to **LPSC reduction to Li2S by
VGCF and Fe particles**, enhancing the Li2S/S conversion reaction."

`[해석]` ★★ **이 위키가 13편째 만나는 "SE 가 용량을 낸다" 의 사례이고, 저자가 자발적으로 인정한
두 번째 사례다** (첫 번째는 Kim 2025 의 S–S bridging 귀속). 그런데 **Kim 2025 와 달리 이 논문은
그 몫을 정량하지 않았고 `LPSC + VGCF` 대조셀도 없다** (G20). `[재현]` 증가분 807 − 765 = **42
mAh g⁻¹(FeS2)** = 첫 방전의 **4.8 %** — 작지만 **부호가 "증가" 라는 점이 중요**하다. 열화가
아니라 **성장**이고, 그 성장을 SE 소모로 설명하면 **수명의 대가**가 어딘가에 있어야 한다.

### 6.5 파우치셀 (Fig. 5f) — 15 MPa · 55 °C · AM 2.2 mg cm⁻²

`[인쇄]` 0.05 C **615.8 mAh g⁻¹(FeS2)** (`Figure S10`, LED 점등), 1 C 2사이클 **442.3 mAh g⁻¹**
= `[인쇄]` **619.2 Wh kg⁻¹ (based on active material, Table S6)**, **500사이클 이상**.
`[도표, Fig. 5f]` 1사이클 **≈520** → 2사이클 **≈440** → 20사이클 **≈355** → 500사이클 **≈295**.
`[재현]` 500/2사이클 = **67 %**. **본문은 유지율 숫자를 주지 않는다.**
`[재현]` 1 C = **44.8 mA** `[인쇄]` ÷ 800 mA g⁻¹ = **56 mg FeS2** ✓ (Methods 와 일치).
에너지밀도 분모 문제는 **G13** (`[재현]` 적층 기준 **81.6 Wh kg⁻¹**).

### 6.6 30 MPa 중간 압력 `[인쇄]`

`Figure S17` (미확보): 25 °C 에서 **50사이클 용량 유지 94.3 %**. 파우치도 30 MPa 에서 개선.
`[해석]` **15 MPa 50사이클 ≈69 %(G4) vs 30 MPa 50사이클 94.3 %** — 같은 논문 안에서
**압력을 2배 올리면 50사이클 유지가 25 %p 좋아진다.** 저자들은 이 대비를 강조하지 않는다.
**strain-coordination 이 압력 의존을 없앤 것이 아니라 완화한 것**임을 보여주는 가장 날카로운 숫자다.

---

## 7. 100 MPa 장수명·고율·고로딩 (Fig. 6) `[인쇄 + 도표]`

`[인쇄]` 서두에 솔직한 단서가 있다 — "Although such elevated pressures are **impractical for
real-world applications**, they enable an assessment of the **intrinsic potential** of FeS₂".

| 조건 | `[인쇄]` 결과 | `[재현]` 양단위 | `[도표]` 비고 |
|---|---|---|---|
| **1 C, 4,500사이클** (Fig. 6a 상) | **411 mAh g⁻¹**, "**85 % 유지**" (After activation) | 769 (S) / 537 (Li2S) / **0.66 mAh cm⁻²** | 1사이클 **≈580**, 밴드 중심 **≈480**, 2,000사이클 최대 **≈510**, 끝 **≈415**. 분모는 **≈483** (G11) |
| **4 C (5.3 mA cm⁻²), 30,000사이클** (Fig. 6a 하) | **339.5 mAh g⁻¹ (~0.54 mAh cm⁻²)** | 635 (S) / 443 (Li2S) | **≈250 → ≈340 으로 증가**. 1사이클 방전 ≈480·충전 ≈600 |
| **15 C (19.7 mA cm⁻²), 140,000사이클** | **243.6 mAh g⁻¹ (~0.39 mAh cm⁻²)** | 456 (S) / 318 (Li2S) | 그림은 **`Figure S15`, 미확보** (G10) |
| **율속** (Fig. 6b) | 0.1 C **674.2** → 40 C (52.58 mA cm⁻²) **73.8** | 1261/880 → 138/96 | 0.1C 복귀 `[도표]` **≈700** |
| **고로딩** (Fig. 6c) | **21.7 mAh cm⁻²**, 100사이클, 총 로딩 **60.96 mg cm⁻²**, **FeS2 50 wt%** (= 30.48 mg cm⁻²), CCCV 충전 | `[재현]` **712 mAh g⁻¹(FeS2)** = 1332 (S) = 929 (Li2S) = 이론의 **79.7 %** | `[도표]` 1사이클 **≈21.5** → 최대 **≈22** → 100사이클 **≈19.3** (`[재현]` **89 %**). CE 1사이클 **≈102 %**, 이후 **≈99.5 %**. C-rate 표기 충돌은 **G12** |

`[재현]` **C-rate 와 전류의 내적 일관성** — 1 C = 800 mA g⁻¹ × 1.6 mg cm⁻² = **1.28 mA cm⁻²**.
4 C = 5.12 (본문 5.3) · 15 C = 19.2 (본문 19.7) · 40 C = 51.2 (본문 52.58) → **모두 ±4 % 안에서 맞는다.**

`[재현]` ★ **140,000 사이클의 소요 시간 검산** — 초록은 `[인쇄]` "140,000 cycles at **15 C (4 min)**"
라고 쓴다. 액면대로면 반사이클 4분 × 2 × 140,000 = **778일 = 2.13년**이고, 2025-08-28 투고와
양립하기 어렵다. 실제로는 **전달 용량이 공칭의 ~30 %** 이므로 `[재현]` 0.39 mAh cm⁻² ÷
19.7 mA cm⁻² = **1.19 분/반사이클** → 2.4 분/사이클 → **≈231일 = 7.6개월**. 이쪽이면 가능하다.
**즉 "15 C (4 min)" 이라는 괄호는 공칭 C-rate 의 정의이지 실제 사이클 시간이 아니다.**
같은 식으로 4 C 30,000사이클 = `[재현]` **≈255일**.

`[해석]` ★ **100 MPa 는 우리 셀에서 재현 불가능한 조건**이다. 이 논문의 "long-cycling" 헤드라인
(4,500 / 30,000 / 140,000)은 **전부 100 MPa** 이고, **저압(15 MPa) 상온 셀은 50사이클에 ≈69 %**
로 끝난다 (G4). **초록이 두 체제를 한 문장에 붙여 놓아 섞이기 쉽다.**

`[인쇄]` 비교 그림들 — Fig. 5g(운전 압력 vs 비용량, 본문 ref.4·28·32–38) · Fig. 6d(수명·율속) ·
Fig. 6e(원료비: FeS2 **0.18 US$/kWh** vs NCM ~74 / LCO ~72 / LFP ~39; 음극 US$/Ah 는
Si < Graphite < **Li2Si** < Li metal) · Fig. 6f(로딩 vs 면적용량). 출처는 **Table S1–S5, 미확보**.

---

## 8. 기전 — AC-STEM 과 계면 반응에너지 (Fig. 7) `[인쇄 + 도표]`

`[인쇄, Methods]` CEOS probe-corrected **FEI Themis**, 가속전압 **300 kV**.

- `[인쇄 + 도표, Fig. 7a·7b]` 초기 FeS2 복합양극 명시야상: 격자무늬 간격 **d₁₁₁ = 0.31 nm**
  (pyrite FeS2 (111)), "indicating **high crystallinity**". 50 nm / 5 nm scale bar.
  `[도표]` 노란 점선이 LPSC, 빨간 점선이 FeS2 — **밀링 후에도 FeS2 가 결정질로 남아 있다.**
- `[인쇄 + 도표, Fig. 7c]` **100사이클 후 방전 상태** 암시야상: **Fe⁰ 와 Li2S** 형성
  (`Figure S16` 미확보). `[도표]` 입자가 **≈200 nm 크기의 다공성 응집체**로 보이고 내부에
  밝은 점(Fe⁰, 빨간 점선)과 어두운 기지(LPSC+Li2S, 노란 점선)가 섞여 있다.
- `[인쇄 + 도표, Fig. 7d]` 원자분해능 STEM(2 nm / 500 pm) + EDS 맵: **Fe 신호는 격자와 일치하고
  S 신호는 어긋난다** → `[인쇄]` "**pure phase Fe⁰ nanoparticles** … uniformly embedded within the
  **Li2S and LPSC matrix**, facilitating a highly reversible and efficient redox process
  **despite the insulating nature of Li₂S**".
- `[도표, Fig. 7e]` 모식 전압곡선 (x = 전자 수 0–8, y = 1.0–3.0 V):
  방전 `FeS2 → Li2S + FeS` (0–2 e⁻, ≈2.0 V) → `FeS → Li2S + Fe⁰` (2–4 e⁻, ≈1.5 V);
  충전 `Li2S + Fe⁰ → FeS` (4–6.5 e⁻, ≈2.0–2.5 V) → **`Li2S → S` (6.5–8 e⁻, ≈2.65–2.9 V)**.
  상태 라벨: Initial FeS2 **V = 100 %** · Discharge Li2S + Fe⁰ **V = 259 %** ·
  Charge **FeSx + (2−x)S**.
- `[인쇄 + 도표, Fig. 7f]` 음극/LPSC **계면 반응에너지** (Materials Project + **Interface Reactions
  Calculator**): `[도표]` **Li −0.59 · Li2Si −0.41 · Si −0.155 eV/atom** (0 에 가까울수록 안정).
  `[인쇄]` Li2Si 가 "**significantly improved interfacial stability** compared to the Li metal-LPSC
  interface".

`[해석]` ★ **Fe⁰ 나노입자가 절연성 Li2S 안에 박혀 전자 경로를 만든다 — 이것이 우리
[[carbon-dimensionality-electron-network]] 의 금속판(版)이다.** 우리는 AB 를 외부에서 넣어
Li2S 입자에 **붙이려** 하고, 이 셀은 **Li2S 가 생길 때 전자도체가 함께 태어난다**. 그래서
"도전재가 활물질 표면 어디에 있는가" 문제가 원천적으로 없다.
단 ⚠ (i) **계산은 열역학적 반응에너지일 뿐 속도론이 아니고**, (ii) Fig. 7f 는 **Si 가 Li2Si 보다
안정**하다고 말하는데 그렇다면 **리튬 재고가 없는 쪽이 계면에 더 좋다**는 뜻이어서, 전략의
전제(Li2Si 가 필요하다)와 긴장 관계다. 논문은 이 긴장을 언급하지 않는다.

---

## 9. 실험 방법 전문 — 표로 옮긴 것 `[인쇄, Methods]`

### 9.1 ★ 복합양극 제조 (우리 [[composite-cathode-mixing-routes]] 열)

| 항목 | 값 |
|---|---|
| 활물질 | **상용 micro-sized FeS2**, **D50 = 14–18 µm**, Macklin, **99.5 %** |
| 고체전해질 | **Li5.5PS4.5Cl1.5 (LPSC)**, **> 6 mS cm⁻¹**, GLABAT |
| 도전재 | **VGCF (vapor-grown carbon fibers)**, GLABAT — **1D 섬유, 단일 탄소** |
| 조성 | **20 : 40 : 4** 또는 **50 : 42 : 8 (wt%)** (앞의 것은 합이 64 — G8; `[재현]` 정규화 **31.3 : 62.5 : 6.3**) |
| 바인더 | **없음** (펠릿셀). 파우치셀만 PTFE **0.5** 추가 |
| 혼합 장비 | **planetary ball mill** (제조사·모델 **미기재**) |
| 용기 | **zirconia jar** (부피 **미기재**) |
| 볼 | **zirconia balls** (지름·개수·질량 **미기재**) |
| **BPR** | **미기재** |
| 회전수 | **300 rpm** |
| 시간 | **2 h** (휴지 주기·정역회전 **미기재**, 단계 수 **1단계로 읽힘**) |
| 분위기 | `[인쇄]` "**Except for ball milling**, all sample preparation procedures were carried out in an Ar-filled glovebox (O₂ <0.1 ppm, H₂O < 0.1 ppm)" — **밀링 분위기/밀봉 여부 미기재** (G2) |

**대조 전극들** (같은 논문, 조건 비교용):

| 전극 | 조성 (wt%) | SE | 혼합 |
|---|---|---|---|
| **LTO** (zero-strain 대극) | **50 : 42 : 8** | LPSC | **planetary, 400 rpm, 2 h**, zirconia jar + balls |
| **NCM811 / LCO** | **70 : 26 : 4** | **Li3InCl6** (>1.5 mS cm⁻¹, D50 1–3 µm, GLABAT) | **mortar & pestle, 30 min** (밀링 아님) |
| **Li7Ti5O12** (prelithiated LTO) | — | — | `Li4Ti5O12∣LPSC∣Li-In` 셀을 방전 후 **분해해 긁어냄** |

`[해석]` ★ **같은 논문이 활물질에 따라 혼합 에너지를 3단계로 나눠 쓴다** — FeS2 300 rpm,
LTO 400 rpm, 산화물(NCM·LCO) **막자사발**. 산화물에 할라이드 SE 를 쓰고 손혼합한 것은
황화물–산화물 계면 반응을 피하기 위한 통상 선택이지만, **혼합 에너지 자체가 변수라는 인식**이
이 논문에는 없다 (Cronk 2026·Kim 2025 의 핵심 발견과 대비된다).

### 9.2 음극

| 음극 | 제조 |
|---|---|
| **LixSi** | Si (Macklin **99.9 %**) + **PTFE 97 : 3 wt** 를 **반복 롤링** → 균일 필름 **두께 ~30 µm**, 로딩 **~3 mg cm⁻²**, **⌀10 mm** 펀칭. Li 박(China Energy Lithium, >99.9 %)을 **⌀8 mm**, **22 / 45 / 65 µm (= 0.6 / 1.2 / 1.8 mg)** 로 펀칭. **셀 조립 중 짧은 접촉(brief contact)으로 in situ 합금화** |
| **Li–In** | In 박 ⌀10 mm · 30 µm · **99.999 %** (Wanda) + Li 박 ⌀8 mm · ~20 µm 를 **기계적으로 압착** |
| **Li 금속** | fresh Li foil |

### 9.3 셀 조립 — ★ 성형 압력과 운전 압력의 분리

| 단계 | 값 |
|---|---|
| 셀 하우징 | `[인쇄]` **stainless-steel clamping fixtures + PEEK outer sleeve + alumina ceramic inner liner**, **⌀10 mm** (homemade mold cell) |
| ① SE 펠릿 | **~80 mg** 황화물 SE 를 **125 MPa (1 ton), 1 min** |
| ② 양극 압착 | 복합양극을 한쪽 면에 펼치고 **125 MPa, 1 min** |
| ③ 음극 적층 | 반대쪽에 Si 필름 → 그 위에 Li 박 |
| ④ **최종 성형** | **500 MPa (4 tons), 1 min** |
| ④′ **Li‖FeS2 대조셀만** | **최종 성형 15 MPa** ⚠ **G14 — 대조군의 성형 압력이 33배 낮다** |
| **운전 압력** | **15 MPa** (저압 실험) 또는 **30 / 100 MPa**. **유지 방식 미기재** (G9) |
| N/P | `[인쇄]` "~1.5" (Fig. 1 캡션은 "N/P = 1", `[재현]` 재구성은 ≈4 — **G6**) |
| 전 공정 | Ar 글로브박스 (O₂ <0.1 ppm, H₂O < 0.1 ppm) |

### 9.4 파우치셀 — **무용매(solvent-free) 건식 공정**

| 항목 | 값 |
|---|---|
| 혼합 | FeS2 : LPSC : VGCF : **PTFE = 50 : 42 : 8 : 0.5 (wt)**, **Hummer Acoustic Mixer (HAM100)** — **음향 혼합기, 볼밀 아님** |
| 성형 | 반복 **fiberization + roll pressing** → **자립 필름** → **carbon-coated Al 호일**로 전사 |
| 치수 | 음극·SE **50 × 60 mm**, 양극 **45 × 56 mm**, 펀칭은 공압 펀칭기, 탭은 **초음파 용접** |
| 적층 후 가압 | **300 MPa, 90 s** (BTKF 고압 프레스) — 진공 실링 후 |
| 질량 | 양극 복합체 **~112 mg** (FeS2 **56** · LPSC **47.04** · VGCF **8.96**) · SE 분리막 **~253 mg (~90 µm)** · Li2Si 음극 **~60 mg** |
| 운전 | **15 MPa**, 55 °C |

`[해석]` ★ **파우치 양극은 볼밀이 아니라 음향 혼합기 + 섬유화 롤프레스**다. 즉 **펠릿셀과 파우치셀의
혼합 경로가 다르다** — 그런데 논문은 두 결과를 같은 선상에 놓고 말한다. 우리 one-step/two-step
질문([[one-step-vs-two-step-mixing]])의 관점에서는 **같은 조성·다른 경로의 비교 기회**였는데
비교가 이루어지지 않았다 (펠릿 0.05 C 868.4 @55 °C vs 파우치 0.05 C 615.8 @55 °C — `[재현]`
**29 % 낮다**. 로딩도 1.6 → 2.2 mg cm⁻² 로 다르므로 단독 귀속 불가).

### 9.5 측정

| 측정 | 장비·조건 |
|---|---|
| 충방전 | **LAND CT2001A**, 25 ± 1 °C, **CC** (고로딩만 **CCCV** 충전) |
| 전압창 | LixSi‖FeS2 **0.65–2.65 V** · Li‖FeS2 **1–3 V** · LTO‖FeS2 **−0.55–1.45 V** · LTO‖NCM **1.15–2.8 V** · LTO‖LCO **1.25–2.7 V** · Li‖LTO **1–2.5 V** · LixSi‖LTO **0.65–2.15 V** |
| EIS | **BioLogic VSP-300**, 7 MHz – 20 mHz, 10 pts/decade, **10 mV** AC |
| GITT | **0.1 C (~0.13 mA cm⁻²)**, 10 min 펄스 + **2 h** 이완, 10 s 마다 기록 |
| **응력** | custom-built pressure-measuring device + **force sensor** (**CHUANGLI Ningbo**), 25 °C, **15 MPa** |
| **두께** | **SPFT2000 IESTTECH** (**laser displacement sensor + force sensor**), **정압 조건** |
| **XCT** | **Zeiss Xradia 610 & 620 Versa**, 중앙 **2 × 2 mm**, 해상도 **~4 µm**, Ar 박스 분해 + 플라스틱 필름 밀봉 |
| 광학현미경 | **YUESCOPE YD650**, Ar 박스 내, 성형 250 MPa, 두꺼운 전극(양극 ~20 / 음극 ~12 mg cm⁻²), **탈형 후 관측** |
| XRD / SEM / STEM | Rigaku / Hitachi FESEM / **FEI Themis** probe-corrected, 300 kV |
| 계산 | **Materials Project + Interface Reactions Calculator** (계면 반응에너지) |
| **셀 개수** | `[인쇄]` 펠릿 **"at least three"**, 대표 데이터는 **"consistent 한 셀에서 선택"**; operando·파우치 **1–2개** (G19) |

---

## 10. ★ H5(기계적 제한) 5논문 대조표 — 무엇을 쟀고 무엇을 안 쟀나

[[reference-cell-500-600-mahg]] H5 의 근거를 한 표에 모은다. **이 논문이 비로소 "응력" 축을 채운다.**

| 축 | **Zhang(J) 2026** (이 논문) | **Qu 2025** | **Cronk 2026** | **Jeong 2026** | **Kim 2025** |
|---|---|---|---|---|---|
| 활물질 | **FeS2** (Li2S 는 방전 생성물) | **S8 · Li2S 각각** | **Li2S · S8** | **S8** (멜트 함침) | **S8** |
| **무엇을 쟀나** | **응력(force sensor)** + **두께(레이저 변위)** + **XCT 단면** + in-situ 광학 | **수직 변위(LVDT)** + **스택 압력(압력변환기)** | **cryo-FIB 단면 두께** | **단면 SEM 두께** | **AFM Young's modulus** |
| **기준자(zero-strain)** | **LTO 대극** ✔ | **LTO 대극** ✔ | 없음 | 없음 | 없음 |
| **정압/정용적** | **둘 다 운용** (응력=정용적, 두께=정압) — **성능 비교는 없음** | **둘 다 + 성능 비교** ✔ (100사이클 **63 % vs 50 %**) | 미기재 | **정용적(constant-gap) 단일** | 미기재 |
| **운전 스택 압력** | **15 / 30 / 100 MPa** (무압 EIS **356 Ω**) | **7 MPa** | 미확인 | **50 MPa** | 미기재 |
| **성형 압력** | **125 MPa(층) → 500 MPa(최종)**; 파우치 300 MPa; 광학셀 250 MPa | 500 MPa | — | 700 MPa | — |
| **양극 두께 변화** | **56 → 68 µm (+21.4 %)**, 방전 (Li2S 생성) | **Li2S 양극 −19 µm**, 첫 충전에 **−10 µm = 53 %** | **Li2S 45 → 26 µm (−42 %)** + **주상 균열** | **첫 방전 후 +46.6 %(Mic-S) / +36.8 %(Mic-L)** | — |
| **셀 전체 두께 변화** | **~1.4 µm** (정압, G15) | 성분별 분해 | — | — | 펠릿 **8.8 % 얇아짐**(밀링 SE) |
| **응력·탄성계수** | **σc: FeS2 0.80 · Li2Si 0.88 · Li 1.03 · 셀 0.16 MPa mAh⁻¹** | 압력 강하 −0.12 ~ −1.4 MPa | — | — | **LPSCl E 21.98 → 4.63 GPa**; 양극 13.64/8.98/14.03 GPa |
| **균열 관측** | **없음** (STEM 입자 단위만) | **SEM — 균열은 비가역, 공극은 가역** | **cryo-FIB 주상 균열** ✔ | crack/void 분율 **수치 없음** | — |
| **압력-성능 민감도** | **15 vs 30 MPa: 50사이클 ≈69 % vs 94.3 %** (저자는 강조 안 함) | **정압 vs 정용적 63 vs 50 %** | — | 없음 (50 MPa 고정) | — |
| **우리 Li2S 축에의 직결성** | **간접** (부호 반대, 활물질 다름) | **직접** (Li2S 양극 단독 측정) | **직접** (Li2S 전극 단면) | 간접 (S8) | 간접 (SE 기계물성) |

### 10.1 이 논문이 **새로 채우는 칸**

1. **"응력을 전극별로 나눠 재고, 그 수를 설계에 되먹인다"** — Qu 는 변위를 성분별로 나눴지만
   **설계 변수로 되돌리지 않았다.** 이 논문은 σc 라는 한 숫자로 전극 쌍을 고른다.
2. **무압 운전의 정량** — `[인쇄]` 0 MPa 에서 **356 Ω**. [[anode-free-li2s-assb]] 의 "무압 불가"
   근거가 **Qu 2025 + 이 논문** 둘이 된다.
3. **압력 포화점** — `[인쇄]` **15 MPa 이상에서는 저항이 거의 변하지 않는다.**
   Qu 의 7 MPa, Jeong 의 50 MPa 사이에 **세 번째 좌표**가 생겼다.
   `[해석]` 세 논문의 운전 압력이 **7 / 15 / 50 MPa** 로 7배 흩어져 있고, **각자 자기 근거를 댄다.**
   → **"ASSB 의 표준 운전 압력" 같은 것은 문헌에 없다.** 우리 셀의 압력은 우리가 측정해 정해야 한다.

### 10.2 이 논문이 **채우지 못하는 칸**

- **균열을 보지 않았다.** `[인쇄]` 100사이클 후 STEM 은 **입자 하나**를 본다. 전극 단면 균열
  (Cronk 의 주상 균열, Qu 의 비가역 균열)에 해당하는 관측이 없다.
- **정압/정용적 성능 비교가 없다.** 장비는 둘 다 있는데 Qu 의 핵심 실험을 하지 않았다.
- **Li2S 가 아니다.** 우리 첫 충전 수축에 직접 쓸 수 없다.

---

## 11. 우리 연구와의 접점 — 이식 가능/불가

| 이 논문의 것 | 우리 [[li2s-assb-reference-cell]] 로 | 판정 |
|---|---|---|
| **LTO(zero-strain) 대극을 기준자로 쓰기** | `Li2S∣LPSCl∣LTO` 반쪽 셀로 **우리 양극만의 응력/변위**를 뽑는다 | ★ **즉시 이식 가능.** Qu 2025 와 중복 확인됐다 |
| **용량 정규화 응력 σc (MPa mAh⁻¹)** | 우리 양극의 첫 충전 응력을 **용량으로 나눠** 보고한다 | ★ **이식 가능.** 단 정의식을 **우리가 명시**해야 한다 (G17) |
| **레이저 변위계 + force sensor 동시 운용** | 정압 모드에서 두께, 정용적 모드에서 응력 | **이식 가능하나 장비 필요.** Qu 의 LVDT 가 더 싸다 (Qu digest §3.1) |
| **15 MPa 포화 판정 (압력별 EIS)** | 우리 셀에서 **0/1/3/5/10/15/30 MPa 의 EIS 한 세트** | ★★ **가장 값싼 이식.** 셀 1개·반나절. 우리 운전 압력의 근거가 생긴다 |
| **음극 Li 재고로 부피를 상쇄한다 (Li2Si)** | 우리는 **Li–In → anode-free** 방향이라 **Li 재고를 늘리는 설계는 반대 방향** | ⚠ **직접 이식 불가.** 단 **"음극 쪽 부피 거동이 양극 수명을 바꾼다"** 는 명제는 가져온다 |
| **FeS2 양극 자체** | 우리 활물질이 아니다 | **불가** |
| **VGCF 단일 1D 탄소로 6–8 wt%** | 우리 AB 20 wt% 와 비교 가능한 조건 | ⚠ **참고만.** 조성·로딩·활물질이 전부 다르다 |
| **Fe⁰ 나노입자가 Li2S 안에서 전자 경로를 만든다** | "절연 Li2S 안에 금속 상을 분산시킨다" 는 **설계 모티프** | `[해석]` **개념으로만 이식.** 우리는 in-situ 생성 수단이 없다 (CuS·CoS 도핑 경로가 그 대안 — 이 위키 inbox 의 Gao 2024 참조) |
| **in-situ 생성 Li2S 가 ≈2.6 V vs Li/Li⁺ 에서 산화된다** | [[li2s-activation-first-charge]] 전위 사다리에 한 칸 | **데이터로 이식.** 단 Fe⁰ 공존 조건임을 반드시 병기 |
| **100 MPa 장수명 숫자들** | 우리 셀 압력(수십 MPa 수준)과 체제가 다르다 | **불가.** 인용하면 오도된다 |
| **619.2 Wh kg⁻¹** | 분모가 FeS2 뿐 | **불가** (G13) |

### 11.1 질문 카드 라우팅

- **H5 (기계적 제한) — 지지 방향의 새 근거이자 도구 제공.** 전극 수준 부피변화가 **셀 수준 접촉
  상실의 직접 원인**임을 응력·두께·XCT 세 측정으로 보였고, **15 → 30 MPa 로 압력을 올리면
  50사이클 유지가 ≈69 % → 94.3 %** 로 바뀐다. 다만 **활물질이 Li2S 가 아니므로 "우리 첫 충전
  손실" 에 대한 직접 근거는 아니다.** 또 하나: `[인쇄]` "SSEs may **share mechanical load** via
  local amorphization, grain-boundary sliding, and time-dependent plasticity" — **Kim 2025 의
  밀링된 LPSCl(E 4.63 GPa)이 오히려 응력을 흡수할 수 있다**는 가능성을 저자가 명시한다.
  → H5 안에 **"무른 SE 는 손해인가 이득인가"** 라는 하위 질문이 선다.
- **H2b (밀링을 겪은 SE 가 아직 superionic 인가) — 간접 반증 방향.** 전량이 **300 rpm 2 h 밀링**을
  겪은 LPSC 로 **40 C (52.58 mA cm⁻²)** 까지 작동했다. `[해석]` 밀링이 이온 경로를 **치명적으로**
  망가뜨리지는 않는다. 단 rpm·시간이 Kim 2025(600 rpm 6 h)·Cronk(500 rpm 1 h)와 달라
  **강도 비교는 불가**하고, **활물질이 다르다.**
- **H4 (분모·SE 기여) — 지지.** `[인쇄]` 55 °C 용량 증가를 **LPSC 환원 → Li2S** 로 귀속하면서
  대조셀이 없다 (G20). **"이론 초과 용량" 은 없지만**(최대 97.2 %) **용량이 사이클과 함께
  증가**하는 두 사례(55 °C 50사이클, 4 C 30,000사이클)가 같은 의심을 받는다.
  → **0번 실험(`LPSCl + AB` 대조셀)의 필요성이 한 번 더 확인됐다.**
- **H1 (활성화 전위) — 부분 근거.** `Li2S → S` 가 **≈2.6–2.9 V vs Li/Li⁺** 에서 일어난다
  (Fig. 7e 귀속 + Fig. 5b·5e 의 충전 말기 상승). **Fe⁰ 공존 + in-situ 생성**이라는 두 특수조건이
  붙는다.
- **H2a (전자 네트워크) — 근거 없음.** σ_e⁻·σ_Li⁺ 를 **측정하지 않았다.**
- **H3 (입자) — 근거 없음.** FeS2 D50 14–18 µm 하나뿐, 입도 스윕이 없다.
- **[[one-step-vs-two-step-mixing]]** — **단계 구분이 없다** (1단계 300 rpm 2 h). 다만 §9.4 의
  **파우치(음향 혼합) vs 펠릿(볼밀)** 이 사실상 다른 경로이고, 비교는 되어 있지 않다.

### 11.2 가장 값싼 다음 실험 (이 논문에서 나온 것)

1. **압력-EIS 스윕 (셀 1개, 반나절).** 우리 `Li2S:LPSCl:AB = 30:50:20` 셀을
   **0 / 1 / 3 / 5 / 10 / 15 / 30 MPa** 에서 EIS. 저항이 포화하는 압력을 찾는다.
   문헌값이 7(Qu) / 15(이 논문) / 50(Jeong) MPa 로 7배 흩어져 있으므로 **우리 값을 우리가 정해야 한다.**
2. **구속 방식 기록 + 첫 충전 전후 높이 (비용 ≈0).** H5 설계 6번 그대로. 이 논문이 **정압/정용적
   둘 다 쓰면서도 비교하지 않았다**는 사실이 그 실험의 가치를 올린다.
3. **`Li2S∣LPSCl∣LTO` 기준자 셀.** Qu 2025 와 이 논문이 **독립적으로** 같은 기준자를 골랐다.
   우리 양극만의 변위/응력을 분리하는 표준 수단으로 채택한다.

---

## 12. 비판

1. **★ 대조실험이 변수 하나만 다르지 않다 (G14).** Li‖FeS2 는 **최종 성형 15 MPa**, Li2Si‖FeS2 는
   **500 MPa** 로 만들어졌다. 33배다. 이 논문의 모든 "Li2Si 가 Li 보다 좋다" 비교 — Fig. 5a(용량·수명),
   Fig. 5b(전압 요동), Fig. 5c(율속), Fig. 4b·4c(DRT), Fig. 4d·4e(GITT) — 가 **음극 종류와 성형
   압력의 교락(confounding)** 위에 서 있다. 논문은 이 사실을 결과 어디에서도 언급하지 않는다.
   (Methods 한 문장에만 적혀 있다.) **이 논문에서 가장 큰 결함이고, 고치려면 Li 셀을 500 MPa 로
   한 번 더 만들면 된다.**
2. **"long-cycling" 의 체제가 초록에서 뒤섞인다.** 4,500 / 30,000 / 140,000 사이클은 **전부
   100 MPa** 이고, 저자 스스로 `[인쇄]` "**impractical for real-world applications**" 라고 쓴다.
   반면 전략의 목적인 **저압(15 MPa) 상온 셀은 50사이클에 ≈69 %** 로 끝난다 (G4).
   초록 문장 — "868.4 mAh g⁻¹ at 15 MPa. **Under 100 MPa**, … cycle life 4,500 … and 140,000" —
   은 형식적으로는 정확하지만, **"strain-coordination 이 장수명을 가능하게 했다"** 는 제목의
   주장은 **저압에서 입증되지 않았다.** 입증된 것은 "저압에서 **죽지는 않는다**" 까지다.
3. **유지율의 분모를 밝히지 않는다 (G11).** 85 % 의 분모는 **첫 사이클(≈580)이 아니라 "활성화 후"
   어느 값(≈483)** 이다. 첫 사이클 기준이면 **71 %**. 이 위키가 Yu 2024·Kim 2025 에서 같은 유형을
   지적했고, 이번에는 **"After activation" 이라는 단어가 분모를 숨긴다.**
4. **SE 가 용량을 내는 것을 인정하면서 분리하지 않는다 (G20).** 55 °C 에서 용량이 **늘어나는**
   현상을 `[인쇄]` "LPSC reduction to Li2S by VGCF and Fe particles" 로 설명해 놓고
   `LPSC + VGCF` 대조셀을 돌리지 않았다. 4 C 30,000사이클의 `[도표]` **≈250 → ≈340 증가**도
   같은 설명을 요구하는데 아예 언급이 없다. **"용량이 오르는 전지" 는 좋은 소식이 아니라
   미분리 변수의 신호다.**
5. **기전 논증이 그림 한 장에 의존한다.** 100사이클 후 STEM **입자 하나**(Fig. 7c·7d)로
   "Fe⁰ 가 Li2S 안에 균일 분산" 을 주장한다. 통계도, 다른 위치도, 사이클 전후 비교(Fig. 7a 는
   **사이클 전 ≠ 충전 상태**)도 없다. 그리고 Fig. 7e 는 **모식도**이지 측정 곡선이 아니다.
6. **DRT 귀속의 강도가 그림과 맞지 않는다 (G18).** 네 개의 τ 영역에 이름을 붙였지만,
   실제 지도는 **τ ≈ 10 s 봉우리 하나가 지배**하고 나머지 세 영역은 배경과 구분이 어렵다.
   "fewer peaks" 라는 표현에 **피크 면적·저항값이 따라붙지 않는다.**
7. **두께 측정 셋이 서로 다른 셀이고 서로 안 맞는다 (G15).** 광학현미경 셀(양극 ~20 mg cm⁻²,
   250 MPa, 탈형), XCT 셀(양극 56 µm), 변위 셀(정압). **~1.4 µm(변위) vs −3 µm(XCT)** 이고
   XCT 해상도는 **~4 µm** 다. "quasi zero-strain" 의 정량적 근거가 생각보다 약하다.
8. **본문이 자기 그림과 어긋나는 곳이 최소 넷.** 첫 방전 740.0 vs ≈650 (G3) · 수축이 충전인가
   방전인가 (G16) · 고로딩 0.1 C vs "1C" (G12) · N/P 1 vs 1.5 vs ≈4 (G6).
9. **Fig. 7f 가 전략의 전제와 긴장한다.** 계면 반응에너지가 **Si(−0.155) < Li2Si(−0.41) < Li(−0.59)**
   이면 **리튬이 적을수록 LPSC 계면에 안정**하다. 그렇다면 Li2Si 의 이점은 계면 화학이 아니라
   **부피 상쇄 하나**여야 하는데, 본문은 두 효과를 같이 묶어 설명한다 (§8 끝 "Taken together").
10. **긍정할 점도 적는다.** (i) `[인쇄]` **셀 개수를 밝혔다** ("at least three" / operando 1–2) —
    이 위키 digest 13편 중 드문 일이다. (ii) **성형 압력과 운전 압력을 분리해 적었다.**
    (iii) **율속별 응력(Figure S20)으로 자기 가설을 교차검증**했다. (iv) **100 MPa 가 비현실적임을
    스스로 밝혔다.** (v) **SE 가 용량에 섞인다는 것을 숨기지 않았다.**

---

## 13. 이 저장소가 가져갈 것

1. **★ 압력-EIS 스윕을 우리 셀의 표준 전처리로 만든다.** 0 MPa 에서 356 Ω 이라는 숫자 하나가
   "무압은 안 된다" 를 끝낸다. 우리도 같은 한 장을 가져야 한다.
2. **★ LTO zero-strain 기준자**를 [[li2s-assb-reference-cell]] 의 표준 반쪽셀로 채택 검토.
   Qu 2025 와 이 논문이 독립적으로 같은 선택을 했다.
3. **★ "셀 수준 ΔV" 와 "양극 수준 ΔV" 를 섞지 않는다** (§2.2). 이 위키의 H5 표에 단위 열을 추가해야
   한다 — Cronk −42 %, Jeong +46.6 %, Qu −19 µm 는 **양극**, 이 논문의 −17.2 %/+2.6 % 는 **셀**.
4. **운전 스택 압력에는 문헌 표준이 없다** — 7 / 15 / 50 MPa. [[anode-free-li2s-assb]] 의 압력 절에
   세 번째 좌표(15 MPa, 그리고 "15 MPa 이상은 포화")를 추가한다.
5. **"용량이 오르는 전지" 를 의심 목록에 넣는다.** 지금까지 이 위키의 규율은 "이론 초과 용량을
   보면 SE redox 를 의심한다" 였다. 여기에 **"사이클과 함께 용량이 증가하면 SE 소모를 의심한다"**
   를 더한다 (이 논문이 그 귀속을 자기 입으로 했다).
6. **활성화 전위 사다리에 한 칸**: **Fe⁰ 공존 in-situ Li2S ≈2.6 V vs Li/Li⁺**
   (Cronk 2.4 V/무게 0 · Wan 2.80 V/39.9 wt% · Zhang(Qi) 2.87 V/43.8 wt% · Lee 컷오프 3.62 V 와 나란히).
7. **"대조군의 성형 압력을 맞춰라" 를 우리 실험 체크리스트에 넣는다** (G14 의 교훈).
8. **새 개념 후보**: `strain-coordination-electrode-pairing` — 양극 팽창과 음극 수축을 부호로 맞춰
   셀 수준 ΔV 를 0 근처로 만드는 설계. 근거는 현재 **이 논문 하나**(single-source)이므로
   `confidence: low ~ medium`.

---

## 14. 그림 판독 기록 — 무엇을 보고 무엇을 안 봤나

크로핑 결과는 `wiki/raw/figures/zhangj2026_strain-coordination-long-cycling-assb/`.
초기 캡션 앵커 bbox 가 **오른쪽 열을 잘라서**(Fig. 2 의 c·f, Fig. 5 의 f·g, Fig. 6 의 c·f)
**페이지 전폭(x 30–566 pt)으로 재크롭**했고, Fig. 5·6 은 위쪽 패널 상단도 잘려 y0 를 40 pt 로
올렸다. 사유는 `figures.json` 의 `note` 에 기록했다.

| 그림 | 파일 | 봤나 | 무엇을 읽었나 |
|---|---|---|---|
| **Fig. 1** | `fig_1.png` | **✔ 봤다** | 모식도. 범례 **FeS2 / LPSC / VGCF / Fe⁰ / Li2S**. 하단 수식 **Σ_ΔV = −17.2 %** (Li) · **+2.6 %** (Li2Si). 캡션의 **N/P = 1** 확인 (G6) |
| **Fig. 2** | `fig_2.png` (재크롭) | **✔ 봤다** | σc 4종(0.80 / 0.88 / 1.03 / 0.16) · 응력 최대값과 그 용량 · **2e 의 W 자 궤적** · 2f 의 **보간합 −0.15 겹침** |
| **Fig. 3** | `fig_3.png` | **✔ 봤다** | 3a–c 광학 단면(200 µm bar, 3층 + ΔV 화살표) · 3d·3e XCT(100 µm bar, 라벨 `Pristine/Lithiated FeS2 Electrode`, `LPSC`, `Li2Si/LixSi`) · **3f 두께 0 → −1.5 µm 가 방전에서 일어남** (G16 의 근거) |
| **Fig. 4** | `fig_4.png` (재크롭) | **✔ 봤다** | 4a 순서 **방전→충전→방전** · DRT 컬러바 **0–380 Ω**, **τ≈10 s 단일 지배** · 화살표 3개 위치 · 4d·4e logD −10 ~ −25, "high/low slope", "Irreversible loss" |
| **Fig. 5** | `fig_5.png` (재크롭 + 1200 dpi 확대 판독) | **✔ 봤다** | **5a 의 Li2Si 1사이클 ≈650 (본문 740.0 과 불일치, G3)**, 최대 ≈665, 50사이클 ≈450 · Li 1사이클 ≈603 → 10사이클 ≈148 · CE 곡선 · 5b 전압곡선과 삽입도 · 5c 율속 · 5d 55 °C 궤적(870→765→805) · 5e 3rd vs 50th · 5f 파우치(520→440→295) · 5g 압력-용량 산점도 |
| **Fig. 6** | `fig_6.png` (재크롭 + 확대 판독) | **✔ 봤다** | **6a 상단 1사이클 방전 ≈580·충전 ≈605, 밴드 ≈480, 최대 ≈510, 4500 ≈415 (G11 의 근거)** · 6a 하단 4C **≈250 → ≈340 증가** · 6b 율속 라벨 전부 · **6c 의 "1C" 라벨 (G12)**, 21.5 → 19.3, CE 1사이클 ≈102 % · 6d·6e·6f 비교 막대 |
| **Fig. 7** | `fig_7.png` (재크롭) | **✔ 봤다** | 7a·7b d₁₁₁ = 0.31 nm · 7c 방전 입자(≈200 nm 다공 응집체) · 7d Fe/S 맵 불일치 · **7e 전 구간 반응 귀속과 V = 100 % / 259 %** · **7f 막대 Li −0.59 / Li2Si −0.41 / Si −0.155 eV/atom** |
| **SI 전체** | — | **✘ 못 봤다** | `Figure S1–S22` · `Table S1–S6` · `Supplementary Movie 1` **전부 미확보** (G22). 특히 **S2(압력-EIS) · S15(140,000사이클) · Table S6(에너지밀도 분모) · S17(30 MPa)** 가 아쉽다 |

`[해석]` **digest 의 모든 `[도표]` 값은 위 7장을 실제로 띄워 읽은 것**이고, 눈금 간 보간이므로
오차는 축 한 눈금의 **±5 % 내외**로 본다. 본문과 그림이 어긋나는 네 곳(G3·G6·G12·G16)은
**둘 다 적어 두었다** — 어느 쪽이 맞는지는 SI 없이 판정할 수 없다.

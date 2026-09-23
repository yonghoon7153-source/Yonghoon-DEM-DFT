---
title: "Strauss, Bartsch, de Biasi, Kim, Janek, Hartmann, Brezesinski 2018 — Impact of Cathode Material Particle Size on the Capacity of Bulk-Type All-Solid-State Batteries (ACS Energy Lett. 3, 992-996)"
source_url: local-upload/21._Impact_of_Cathode_Material_Particle_Size_on_the_Capacity_of_Bulk-Type_All-Solid-State_Batteries.pdf + 21._sup_Impact_of_Cathode_Material_Particle_Size_on_the_Capacity_of_Bulk-Type_All-Solid-State_Batteries.pdf (SI)
source_url_note: "본문 5쪽(Letter, 참고문헌 26편) + SI 8쪽(그림 S1-S7, 표 S1, 참고문헌 5편). 크로퍼가 본문 그림 4 + SI 그림 7 + SI 표 1 을 전부 잡았다. **그림 11장 전부 직접 봤다 — 안 본 그림 0장.** 표 S1 은 이미지 대신 PDF 텍스트로 읽었다. PDF 는 커밋하지 않는다."
source_doi: 10.1021/acsenergylett.8b00275
source_license: "(c) 2018 American Chemical Society — 오픈액세스 아님"
pdf_sha256: d3fa26699f0e158b5da757a802e85553c0947a6a3e02f7ca347e1f0840156dd3
si_sha256: 5b23a700e4b26e298b877cac673fa68776bcc31826a3d19072cfd0d9d19cff01
ingested: 2026-09-23
sha256: 9f56acaae391813dbfa4c1cd3731cc35c4999d707fd75f27489573da00bb874d
---

# 수집 목적

`assb` 섹션 **22호**. 큐 **21번** (21호 = 큐 20 Sedlmeier 2023, 20호 = 큐 19 Chang 2020,
19호 = 큐 18 Yoshida 2024, 18호 = 큐 17 Fukunishi 2023, 17호 = 큐 16 Yanev 2024).
닻은 `questions/assb-contact-loss-vs-lampe.md`. 큐 문서(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md`)의
등록 축은 **★★ Q2 의 measured 라벨 — 01 의 ref 13. ex situ XRD 의 inactive AM 분율 = `1 − θ_AM`**.

> ★★★★ **이 편이 계보에서 차지하는 자리를 먼저 적는다.**
> 1. **기준극 계보(16~21호)가 아니라 1호(Bielefeld 2019)의 `θ_AM` 축으로 돌아가는 편이다.**
>    1호가 자기 모델의 **유일한 실험 대조**로 인용한 논문이 이것(1호 ref 13)이고, 1호 digest 가
>    "후속 후보 1 순위 — 거기에 `1 − θ_AM` 의 measured 값이 있다" 로 적어 둔 자리다.
> 2. **계보에서 처음으로 "전기화학적으로 불활성인 양극 활물질의 분율" 이 전기화학이 아닌 채널
>    (회절 상 분율)로 측정된다.** 용량에서 역산한 이름표가 아니다 — §5-1 에서 식 단위로 가른다.
> 3. **계보에서 처음으로 양극 상태를 상대극 전위와 무관하게 읽는다** — 격자상수로 `x(Li)` 를,
>    상 분율로 불활성 분율을 잰다. 17호 함정의 **주 주장 쪽은 구조적으로 면제**된다(§5-4).
> 4. 시간상으로는 계보에서 **가장 이르다** (2018-02-16 접수 · 2018-03-21 게재; 20호 Chang 은 2019 접수).
>    큐 22번 **Koerver 2017** 이 이 편의 **ref 9** 로 **4 번** 인용된다(저 CE 의 기구 근거).

⚠ **표기 규약** (사용자 지정): `[인쇄]` = 원문이 실제로 쓴 것 ·
`[도표]` = 그림에서 읽은 값(figure-read ≈) · `[재현]` = 원문 수치로 우리가 다시 계산한 것 ·
`[추론]` = 우리의 해석. **`[인쇄]` 표시가 없는 서술문 중 원문의 주장은 인용부호로만 둔다.**

---

# 판정 한 줄

> **이 편은 무탄소 NCM622/β-Li₃PS₄ 복합양극에서 2차 입자 크기(d₅₀ 4.0 / 8.3 / 15.6 µm)만 바꿔
> 첫 충전 용량이 162 → 95 → 84 mAh g⁻¹ 로 떨어지는 것을 보이고, 그 원인을 ex situ XRD 의
> 2상 Rietveld 로 "충전된 상 ↔ 손대지 않은 상" 으로 갈라 불활성 분율 2 / 27 / 31 % 를 잰
> 2018 년 Letter** 다.
>
> ★★★★ **Q1 — `θ` 형의 양이 처음으로 "측정된 양" 이 된다.** 측정 원리는 **회절 상 분율**
> (Rietveld scale factor → 무게 분율)이고, 용량은 **나중에 독립 대조**로만 쓰인다
> (`[인쇄]` 90 / 92 / 153 ↔ 전기화학 84 / 95 / 162 mAh g⁻¹). ⇒ **역산이 아니다.**
> ⚠ 그러나 잰 것은 **"첫 C/10 충전에서 한 번도 탈리튬되지 않은 활물질 분율"** 이고,
> 이것은 1호의 `1 − θ_AM`(**전자** 퍼콜레이션에서 떨어진 부피)보다 **넓은 합집합**이다
> (전자 고립 ∪ 이온 고립 ∪ SE 접촉 없음 ∪ 2차 입자 내부 미반응 영역 ∪ C/10 에서 못 닿은 것).
> 그리고 `[재현]` **반사 기하에서 Cu Kα 의 정보 깊이는 ≈3–15 µm (1/e)** 라 **90 µm 전극의
> 집전체 면 쪽 표층**을 본다 — 전자 고립이 **가장 덜 일어나는 자리**다(§5-1-c).
>
> ★★★★ **1호 대질 — 인용은 맞게 옮겼고, "correlate well" 이 정량 모순을 가린다.**
> 1호가 가져간 네 가지(큰 입자에서 불활성 분율 큼 · XRD 로 잼 · 낮은 전자 전도도로 귀속 ·
> 공극률 안 잼)는 **원문과 맞는다**(`poros*` 본문·SI **0 회**). 그런데 `[재현]` **공극률을 몰라도
> 비교는 된다** — 공극률은 AM 부피 분율을 **낮추기만** 하므로 7:3 wt 의 **무공극 상한(≈48–50 vol%)**
> 에서 1호 모델을 읽으면 된다. 그 상한에서 1호는 **불활성 ≈23–40 / ≈95 / ≈95–97 %** 를 예측하고,
> 측정은 **2 / 27 / 31 %** 다. **XRD 없이 용량만으로도** 전극 평균 불활성은 **≤3 % (S, C/30) ·
> ≤39 % (M, C/30) · ≤44 % (L, C/50)** 로 묶인다 ⇒ **순위는 맞고 크기는 3–15 배 어긋난다** (§5-2).
>
> ★★★ **3항 분해의 첫 실측 분리**: 불활성 분율(`θ`)과 활성 상의 `x(Li)`(`η`)가 **따로** 나온다.
> `[재현]` NCM-L 은 **θ ≈ 0.69 · η ≈ 0.69** — 논문 제목의 "불활성" 은 **결손의 절반**이고
> 나머지 절반은 **활성 입자가 반만 충전된 것**이다. NCM-M 은 η 쪽이 더 크다(ln −0.43 ↔ −0.31).
>
> ⚠⚠ **원인 배정("due to a lack of electronic contact")은 자기 전도도 그림이 지지하지 않는다.**
> `[도표]` Fig. 4 는 **두 y 축의 자릿수 간격이 다르다**(좌 5 자릿수 ↔ 우 3 자릿수). 값으로 읽으면
> NCM-L 의 σ_e ≈1.4×10⁻⁶ ≥ σ_ion ≈9×10⁻⁷ S cm⁻¹ — **그림 인상과 반대로 전자가 이온보다 낮지 않다.**
> NCM-M 은 σ_e/σ_ion ≈ **50** 으로 저자가 "이온 제한" 이라 판정한 NCM-S(≈550)와 **같은 체제**인데
> "전자 비연결" 로 배정된다. 불활성 분율은 M ≈ L(27 ↔ 31 %)인데 σ_e 는 **≈26 배** 다르다.

---

# 0. 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | **공극률·밀도를 재지 않았다** (`poros*` 0 회, 충전밀도 0). 1호의 불평 그대로다. ⚠ `[재현]` 인쇄된 근사값(면적 용량 **1.9 mAh cm⁻²** · 두께 **≈90 µm** · 7:3 wt · 1C = 180 mA g⁻¹)을 합치면 겉보기 밀도 **≈1.68 g cm⁻³** = 무공극 밀도(ρ_NCM 4.75 · ρ_LPS 1.87 가정, **≈3.25**)의 **≈52 %**, 즉 **공극률 ≈48 %** — 375 MPa 냉간 압착 황화물 복합체로는 **믿기 어렵다**(14호 XRM 4.5–9.8 vol% 와 대조). 근사값끼리 **맞지 않는다** | 1호가 x 축(AM vol%)을 맞출 수 없었던 이유이자, 이 편의 셀 기하가 **자기 인쇄값으로 재구성되지 않는다**는 신호 |
| **G2** | **XRD 가 전극의 어느 부분을 보는지 논의가 없다.** `[인쇄]` "disassembled ASSB pellets (with the **cathode composite side up**)" — 드러난 면은 **집전체(스테인리스 plunger) 쪽 면**이다. `[재현]` §5-1-c: 1/e 정보 깊이 **003(2θ≈18.7°) ≈3 µm · 104(≈44°) ≈8 µm · 2θ = 90° ≈15 µm** (공극률 20 % 가정; 0–48 % 범위에서 2.8–23.7 µm) | 측정값이 **전극 평균이 아니라 집전체 면 가중 평균**이다. NCM-L(d₅₀ 15.6 µm)에서 003 은 **첫 입자 층의 윗머리**만 본다 |
| **G3** | **셀 수 n 이 한 번도 적히지 않는다** (`n =` 0 회). XRD 는 크기당 **몇 셀**인지, 전기화학 곡선은 **대표**인지 불명 | Q3. `[인쇄]` ± 는 Rietveld 추정오차 `(1)` 뿐 |
| **G4** | **XRD 는 C/10 첫 충전 직후 한 점뿐.** C/30·C/50 셀도, 방전 후 셀도 XRD 하지 않았다 | `θ` 가 **율 불변**인지(3항 분해의 핵심 전제) 시험되지 않는다. 방전 쪽 비가역(CE 50–70 %)의 소재도 모른다 |
| **G5** | **양극 면적/지름이 인쇄되지 않는다** ("setup described elsewhere", ref 18). `[재현]` 면적 용량에서 역산하면 **0.66–0.80 cm² (∅9.2–10.1 mm)** 인데 In 음극은 **∅8 mm (0.503 cm²)** ⇒ **음극이 양극보다 작다(0.63–0.76 배)** | 양극 가장자리 고리가 음극 투영 밖이다. `[추론]` 복합체 σ_ion 이 세 크기에 **같으므로**(Fig. 4) 크기 대비를 만들지는 않지만, 불활성 분율의 **절대값**에는 들어갈 수 있다 |
| **G6** | **비표면적(BET)·밀링 후 입도를 재지 않았다.** 복합체는 ZrO₂ 볼(∅10 mm ×10) 유성 밀 140 rpm 30 분 — 2차 입자가 깨졌는지 모른다 | 곱 축퇴의 "면적" 인자를 대조군으로 쓸 수 없다(처방 2단계) |
| **G7** | **NCM-S 만 다른 로트다.** `[인쇄]` "Both NCM-S and NCM-M were supplied by BASF SE. **NCM-L was obtained by sieving NCM-M**" ⇒ **M ↔ L 은 같은 로트(순수 크기 대조), S ↔ M/L 은 로트까지 다르다** | 큰 효과(S ↔ M: 불활성 2 → 27 %)가 **교락된 쪽**에 있고, 깨끗한 쪽(M ↔ L)의 효과는 **작다**(27 → 31 %, 95 → 84 mAh g⁻¹) |
| **G8** | **기준극 없음.** In/InLi 전위는 `[인쇄]` "(corresponding to 4.4−2.9 V vs Li⁺/Li)" · SI "(0.6 V difference)" 로 **0.6 V 가정** | Q5. 용량·CE 축은 17호 함정에 노출(§5-4) |
| **G9** | **상 분율 오차의 정의가 모호하다** — `[인쇄]` "errors in the calculation of the phase fraction of **–3%** for both NCM-L and NCM-M and **–11%** for NCM-S". NCM-S 불활성이 **2(1) %** 이므로 −11 %p(절대)일 수 없고, 상대(−11 % × 2 % = −0.2 %p)라면 "relatively large error" 라 부를 이유가 없다 | Q3 — 오차 예산을 **인쇄한 계보 첫 편**인데 그 단위가 안 읽힌다 |
| **G10** | **전도도는 셀이 아니라 별도 100 mg 펠릿에서, 미충전 상태로** 쟀다. 전자: 375 MPa 2 분 · 이온: 250 MPa 후 375 MPa 적층. 셀 양극은 375 MPa 로 SE 에 붙이고 55 MPa 로 운전 | 불활성 분율(충전 후, 셀 안, 표층)과 σ(미충전, 별도 시편, 벌크)를 **같은 대상의 두 관측으로 볼 근거가 없다** — 원인 배정이 **병치**다 |
| **G11** | **열화 축 0.** 첫 사이클만 보인다(`degrad*` 1 회 = 탄소 첨가제가 SE 를 분해한다는 서론) | `θ(N)` 은 여전히 **0 편** |

---

# 1. 서지·셀 사양

- **Strauss, F.; Bartsch, T.; de Biasi, L.; Kim, A-Y.; Janek, J.; Hartmann, P.; Brezesinski, T.**
  "Impact of Cathode Material Particle Size on the Capacity of Bulk-Type All-Solid-State Batteries."
  *ACS Energy Lett.* **2018**, 3, 992−996. DOI 10.1021/acsenergylett.8b00275. Letter, 본문 5 쪽
  (참고문헌 26 편) + SI 8 쪽(그림 S1–S7 · 표 S1 · 참고문헌 5 편).
  접수 2018-02-16 · 수락/게재 2018-03-21. KIT BELLA + JLU Giessen(Janek) + **BASF SE**(Hartmann).
  `[인쇄]` "BASF International Network for Batteries and Electrochemistry" 과제.
- ⚠ **1호(Bielefeld·Weber·Janek 2019)와 교신 연구망이 겹친다** — Janek 이 두 편 공저자다.
  "외부 실측 대조" 가 아니라 **같은 연구망 안의 대조**다.

| 항목 | 값 | 출처 |
|---|---|---|
| CAM | NCM622 (60 % Ni), 코팅 없음. **NCM-S** d₅₀ **4.0** / d₉₀ 4.8 µm · **NCM-M** d₅₀ **8.3** / d₉₀ 13.0 µm · **NCM-L** d₅₀ **15.6** / d₉₀ 26.1 (단위 누락) | `[인쇄]` |
| NCM-L 제조 | NCM-M 을 **20 µm 체로 치고 "the remaining fraction" 수집** | `[인쇄]` SI. ⚠ D2 |
| 전처리 | 300 °C 진공 하룻밤 건조 → Ar 글로브박스 | `[인쇄]` SI |
| SE | β-Li₃PS₄, THF 습식 합성(Li₂S 459.3 mg + P₂S₅ 740.6 mg), 140 °C ≥12 h; 순수도 Rietveld(Fig. S1, 불순물 Li₂S 상 포함 정련). 벌크 σ_ion **≈0.2 mS cm⁻¹** | `[인쇄]` |
| 복합양극 | CAM : SE = **7 : 3 w/w**, 1 g 을 ZrO₂ 볼 ×10(∅10 mm) 유성 밀 **140 rpm 30 분** · Ar. **무탄소 · 무바인더** | `[인쇄]` SI |
| 셀 | SE **60 mg** 을 **≈125 MPa** → ≈400 µm; 양극 복합체 **10–12 mg**(≈90 µm, **1.9 mAh cm⁻²**)을 **375 MPa** 로 부착; In 박 **100 µm · ∅8 mm** 을 **125 MPa** 로 반대면에. 운전 중 **55 MPa** 유지 | `[인쇄]` SI |
| 전기화학 | MACCOR, **25 °C**, **C/10 (1C = 180 mA g⁻¹)**, **3.8–2.3 V vs In/InLi** (`[인쇄]` "corresponding to 4.4−2.9 V vs Li⁺/Li"); 1 h OCV 휴지 후 시작. 추가로 C/30 (세 크기) · C/50 (NCM-L) | `[인쇄]` |
| LIB 대조 | 94 wt% CAM · 4 wt% Super C · 2 wt% PVDF, Al 박, ∅14 mm, CR2032, Li 600 µm, **LP57 100 µL**, 4.4–2.9 V vs Li⁺/Li, 같은 C/10 | `[인쇄]` SI |
| ex situ XRD 셀 | 같은 방식 조립, Specac Mini-Pellet Press 안 **≈55 MPa**, VMP3 로 **C/10 · 3.8 V vs In/InLi 까지 충전**, "disassembled **without breaking the pellet apart**" | `[인쇄]` SI |
| ex situ XRD | Bruker D8 ADVANCE, **θ-θ 반사**, Cu Kα₁/₂, Ni-Kβ 필터, LynxEye 1D; 기밀 돔 셀; **Si 분말을 펠릿 위에 얹어 내부 표준(시편 변위 보정)**; 10–90° 2θ, 0.01° 스텝, 2.3 s | `[인쇄]` SI |
| Rietveld (NCM) | FullProf; 시편 변위 정련, 배경 Chebyshev **24 항**, 고정 등방 ADP(문헌), **두 NCM 상(active · inactive) 동시 정련**, 점유율 **공칭 고정** | `[인쇄]` SI |
| operando XRD (교정) | **LIB** NCM-M/Li 파우치(20×40 mm², Celgard 2500, LP57 250 µL), Mo Kα 회전 음극 + Pilatus 300K-W, 75 s 간격, C/10 · 4.4–2.9 V; TOPAS 5 | `[인쇄]` SI |
| 부분 전도도 | **DC 분극 300 mV**, 정상 상태 전류 선형 적합 → `R = U/I`. 전자: 복합체 ≈100 mg 을 **스테인리스(이온 차단)** 사이 375 MPa 2 분, 1 h 휴지. 이온: 복합체 250 MPa + 양쪽에 1.5Li₂S·0.5P₂S₅·LiI 유리(1.3 mS cm⁻¹) 100 mg 씩 250 MPa + **In ∅9 mm · Li ∅6 mm** 저장조, 375 MPa 2 분, **6 h 휴지**. 측정 중 55 MPa | `[인쇄]` SI. ⚠ D1 (식 오기) |
| SEM/EDX | LEO-1530, 10 keV; **미사이클** 복합체 단면 + S 맵 (Fig. S7) | `[인쇄]` SI |

---

# 2. 절별 해체분석

## 2-1. 초록 · 서론

- `[인쇄]` 초록의 핵심 문장: "We show the benefits of using small particles (**d ≪10 μm**), allowing
  **virtually full charge capacity**." 그리고 "Our results indicate the importance of considering and
  avoiding **electrochemically inactive electrode material** in bulk-type ASSBs, which we show using
  charge transport measurements is due to **poor electronic contact** (in carbon-free cathode composites)."
- `[인쇄]` 무탄소 이유: 탄소 첨가제가 "cause severe degradation of sulfidic SEs upon cycling"
  (refs 10–12) ⇒ "electronic transport pathways are provided **only through interconnected CAM particles**".
- `[인쇄]` 발상의 출처는 **SOFC**: "electronic percolation through the cathode composite can be
  tailored via microstructural and/or interfacial engineering" (refs 13–15, 전부 SOFC).
- `[인쇄]` "to our knowledge for the **first time**, the effect of CAM particle size on the capacity
  of ASSB cells using NCM and β-Li₃PS₄".

## 2-2. 전기화학 — 크기가 용량을 가른다 (Fig. 1, S2)

- `[인쇄]` **LIB**: 충전 ≈200 mAh g⁻¹, 첫 사이클 손실 ≈10 %, 크기 간 "negligible differences".
  `[도표]` Fig. 1d: 방전 끝 **≈188–194** 로 셋이 거의 겹치지만, **충전은 NCM-L ≈233 ↔ M ≈210 ↔ S ≈213**
  — L 이 **≈10 % 더 충전되고 첫 손실이 ≈17 %** 다(D4). "negligible" 은 방전 쪽에만 참이다.
- `[인쇄]` **ASSB C/10**: 첫 충전 **162 (S) · 95 (M) · 84 (L) mAh g⁻¹**; 분극이 LIB 대비
  **"100 to 200 mV"** 증가; 첫 CE **70 (S) · 55 (M) · 50 % (L)**.
  `[도표]` Fig. 1e 방전 끝 ≈110 / ≈56 / ≈42 mAh g⁻¹.
- `[도표]` Fig. S2 (dQ/dU, 전부 V vs In/InLi; LIB 곡선은 `[인쇄]` "0.6 V difference" 로 옮김):
  충전 주 봉우리 **LIB ≈3.10 · S ≈3.18 · M ≈3.23 · L ≈3.29 V** ⇒ LIB 대비 **+80 / +130 / +190 mV**;
  봉우리 높이 ≈1230 / ≈550 / ≈460 / ≈240 mAh g⁻¹ V⁻¹. 방전 봉우리 ≈3.12(LIB) · ≈3.00 · ≈2.98 · ≈2.96 V.
- `[인쇄]` 저 CE 의 원인 서술: "not yet fully understood but is **most likely** associated with different
  chemo-mechanical effects … (note that the **volume contraction during charging leads to a reduced
  electrical contact between the CAM particles and the SE**)" (refs 9, 18) + 코팅 없는 NCM 에서 SE 산화
  분해 → 절연층 → "increases the kinetic barrier … causing low Coulombic efficiency" (ref 9).
  ⇒ **접촉 손실과 계면층을 한 문단에 나란히 놓고 둘 다 "kinetics" 로 묶는다** — 가르지 않는다.

## 2-3. 율 스윕 — 저율로도 안 채워진다 (Fig. 2)

- `[인쇄]` "Using very low current densities should allow mitigating limitations imposed by kinetics."
  C/30: **S ≈190** ("almost full") · **M 120** · **L 100** mAh g⁻¹; L 은 C/50 에서 **100 → 110** 뿐.
- `[도표]` Fig. 2: C/30 방전 끝 S ≈152 · M ≈80 · L ≈60; L C/50 충전 ≈113 · 방전 ≈65.
  충전 개시 평탄 **C/10 ≈3.15 → C/30 ≈3.05 V vs In/InLi** (S).
- `[인쇄]` 결론: "poor kinetics is **not the only issue** … it seems likely that some of the CAM particles
  are inactive or, in other words, **cannot be addressed electrochemically**."
- ★ **이것이 우리 3항 분해의 "율 연산자"(`i → 0` 이면 `η → 1`)를 실험으로 쓴 형태다** — 그리고
  §5-3 에서 보듯 **C/50 에서도 `η → 1` 이 안 된다.**

## 2-4. ★ ex situ XRD — 두 상이 보인다 (Fig. 3, S3–S5, Table S1)

- `[인쇄]` 목적: "determine the **actual SOC** of the ASSB cells (i.e., lithium content of CAM)".
- `[인쇄]` 교정: LIB operando XRD 의 a·c 가 `x(Li)` 와 함께 "unequivocally change" — a 는 거의 선형 수축,
  c 는 **x ≈ 0.5 까지 증가 후 급감**(Ni–O 전하이동, refs 20, 21), 단위포 부피 단조 감소(Fig. S4).
- `[인쇄]` "The **splitting of reflections** … especially noticeable for the **003** reflection, provides clear
  evidence of the presence of **two NCM species with a different lithium content** after charging."
  → 두 상 동시 정련 + operando 대조 → "one as being partially delithiated (SOC > 0, **active**), while the
  other remains in a **pristine state (SOC = 0, inactive)**."
- `[인쇄]` **"The fraction of inactive CAM is found to increase with increasing particle size from 2% for
  NCM-S to 31% for NCM-L (27% for NCM-M)."**
- `[인쇄]` 용량 재구성: "From the SOC and the fraction of active CAM … capacities of **90, 92, and 153**
  mAh/g are obtained for NCM-L, NCM-M, and NCM-S … **close to those obtained from the electrochemical data**.
  This finding demonstrates that **the method is viable for estimating the SOC of ASSB cells**."
- `[인쇄]` SI 오차: 점유율 사후 보정(활성 상 `x(Li)` = **0.53 · 0.56 · 0.46** for L · M · S)으로 상 분율 오차
  **−3 % (L, M) · −11 % (S)**, S 의 큰 오차는 "the **detection limit** of inactive cathode active material by
  XRD"; `x(Li)` 추정 오차 **≈±0.02**; 그리고 "**irreversible capacities from side reactions such as solid
  electrolyte degradation are not taken into account** in the XRD data analysis."
- Table S1 `[인쇄]` (a / c / V / 분율 / z):

| | 상 | a (Å) | c (Å) | V (Å³) | 분율 (%) |
|---|---|---|---|---|---|
| NCM-S | charged | 2.817(1) | 14.501(1) | 99.68(1) | **98(1)** |
| | inactive | 2.869(1) | 14.227(4) | 101.43(5) | **2(1)** |
| | pristine | 2.869(1) | 14.221(1) | 101.38(1) | — |
| NCM-M | charged | 2.823(1) | 14.486(1) | 100.00(1) | **73(1)** |
| | inactive | 2.868(1) | 14.229(1) | 101.34(1) | **27(1)** |
| | pristine | 2.868(1) | 14.225(1) | 101.36(1) | — |
| NCM-L | charged | 2.823(1) | 14.509(1) | 100.10(1) | **69(1)** |
| | inactive | 2.872(1) | 14.240(1) | 101.73(1) | **31(1)** |
| | pristine | 2.870(1) | 14.220(1) | 101.44(1) | — |

## 2-5. 부분 전도도 — 전자가 3 자릿수 떨어진다 (Fig. 4, S6)

- `[인쇄]` "the ionic conductivity is **not affected** by the NCM622 particle size, being around **10⁻⁶ S/cm**
  … roughly 2 orders of magnitude lower than for bare β-Li₃PS₄ (approximately 0.2 mS/cm)."
- `[인쇄]` "the electronic conductivity … decreases by **3 orders of magnitude from about 10⁻³ for NCM-S
  to 10⁻⁶ S/cm for NCM-L**."
- `[인쇄]` 결론: "**slow ionic transport** through the electrode composite is the major issue when NCM-S is
  used … In contrast … in the case of medium and large NCM622, **not all of the particles are electronically
  connected**, which is why they cannot be addressed electrochemically. This is in agreement with
  **percolation theory**" (ref 26, SOFC).
- `[인쇄]` 분리(segregation) 가능성: 건식 혼합이 크기에 따라 분리를 낳을 수 있으나 "cross-sectional SEM
  images and corresponding sulfur EDX maps … **do not reveal major inhomogeneities** (Figure S7). Accordingly,
  it seems reasonable to **assume** that the drastic changes in mean electronic conductivity mainly result from
  the different average particle size."

## 2-6. 결론

`[인쇄]` "Using complementary XRD measurements allowed us to correlate the low specific capacities … to
**apparently inactive material**. Additional charge transport measurements revealed that the presence of
NCM622 that cannot be addressed electrochemically is **due to a lack of electronic contact**."
⇒ 결론 안에서 XRD 쪽은 "**apparently** inactive" 로 조심스럽고, **원인 쪽은 단정**이다.

---

# 3. 그림 — 전부 직접 봤다

크로퍼(`wiki/tools/extract_figures.py`)가 **본문 그림 4 + SI 그림 7 + SI 표 1** 을 전부 잡았다.
**그림 11장 전부 이미지로 봤다 — 안 본 그림 0장.** Table S1 은 이미지 대신 PDF 텍스트로 읽었다(규약).

## Fig. 1 — 분말 SEM · LIB · ASSB 첫 사이클 `[도표]`
(a–c) 상면 SEM: L 은 **구형 2차 입자 ≈15–25 µm + 작은 입자 섞임**, M 은 **≈5–15 µm 혼재**,
S 는 **≈3–5 µm 가 균질**. S 는 **1차 입자 형상이 더 거칠게** 보인다(로트 차이 G7 의 시각적 단서, `[추론]`).
(d) LIB: 방전 셋 겹침, 충전 L 만 오른쪽(≈233). (e) ASSB: 충전 ≈83 / ≈94 / ≈161, 방전 ≈42 / ≈56 / ≈110.

## Fig. 2 — 율 스윕 `[도표]`
§2-3. **저율에서 방전도 같이 는다**(S 110 → 152) — `η` 성분이 방전에도 있다.

## Fig. 3 — ★ 핵심 그림 `[도표]`
(a) 003 영역 17–20°: **활성 봉우리 ≈18.35° · 불활성 ≈18.70°**, L·M 은 **뚜렷이 둘로 갈리고 사이에 중간
위치 봉우리가 없다**; S 는 18.7° 에 **어깨만**(2 %). 별표(≈17.5°)는 β-Li₃PS₄ 210.
⇒ `[추론]` **이봉(bimodal)** — 활성 상의 `x` 가 연속 분포가 아니라 한 값 근처에 모인다 ⇒ **"전부 아니면 전무"
가 결정 영역 수준에서 성립한다.** ⚠ 그러나 이것은 **2차 입자 전체 고립**과 **2차 입자 내부 코어 미반응**을
가르지 못한다 — 둘 다 이봉을 낸다(§5-1-b).
(b) operando 교정 곡선: a 2.869 → 2.816 Å (x 1.02 → 0.31), c 14.20 → **최대 ≈14.51 (x ≈ 0.5)** → 14.29.
교차(+)는 **c 곡선의 최대점 바로 위**에 앉는다 — **L ≈0.51–0.54 · M ≈0.555–0.575 · S ≈0.445–0.47** (음영 폭).

## Fig. 4 — ★ 부분 전도도 `[도표]`
좌축 σ_ionic **10⁻⁸–10⁻³ (5 자릿수)**, 우축 σ_electronic **10⁻⁶–10⁻³ (3 자릿수)** — **같은 높이에 다른 자릿수**.
읽은 값(figure-read ≈):

| | σ_ion (S cm⁻¹) | σ_e (S cm⁻¹) | σ_e / σ_ion `[재현]` | 불활성 `[인쇄]` |
|---|---|---|---|---|
| NCM-S | ≈1.4×10⁻⁶ | ≈7.7×10⁻⁴ | **≈550** | 2 % |
| NCM-M | ≈7×10⁻⁷ | ≈3.5×10⁻⁵ | **≈50** | 27 % |
| NCM-L | ≈9×10⁻⁷ | ≈1.4×10⁻⁶ | **≈1.5** | 31 % |

⚠ 그림에서 L 의 σ_e(빈 원)는 **σ_ion(찬 원)보다 아래**에 그려져 있지만 값은 **위**다 — 축 인상(D8).

## Fig. S1 — β-Li₃PS₄ Rietveld `[도표]`
R_wp 6.4 %, χ² 1.1; 틱 두 줄(β-Li₃PS₄ · Li₂S). 차분 곡선 ≈15–30° 에서 요동. 순수도 확인용 — 우리 축 무관.

## Fig. S2 — dQ/dU `[도표]`
§2-2. **LIB 곡선을 0.6 V 옮겨 겹친 그림** — 가정이 그림의 축 변환으로 들어간다(20·21호와 같은 형태).

## Fig. S3 — operando 등고선 `[도표]`
LIB NCM-M/Li, 충전 ≈12.5 h 에 4.4 V → 방전. 003 이 충전 끝 근처에서 **급히 고각으로 꺾인다**(c 붕괴),
Li·Al 반사 표시. 교정의 원자료.

## Fig. S4 — 단위포 부피 `[도표]`
V: x = 1.02 에서 ≈101.35 Å³ → x ≈ 0.5 에서 ≈99.95 → x = 0.31 에서 ≈98.05; **x ≲ 0.45 에서 급감**. 단조.

## Fig. S5 — 전체 패턴 Rietveld `[도표]`
(a) 분말 R_wp 2.1 / 2.0 / 1.6 % · χ² 1.4 / 1.4 / 1.7. (b) 충전 복합체 R_wp **3.8 / 3.0 / 3.2 %** ·
χ² 1.5 / 1.6 / 1.5; **저각 ≈10–15° 에 돔 셀 배경의 큰 언덕**, Si 반사 영역(≈28.5, 47, 56, 69.5, 76.5, 88°)
제외. 틱 두 줄(충전 상 · 불활성 상). 차분 곡선에 ≈18° · ≈37° 부근 잔차.

## Fig. S6 — DC 분극 전류 `[도표]`
(a) 이온 차단: 스파이크 후 **0.127 → 0.1215 mA 로 ≈1.5 h 안에 정상**. (b) 전자 차단: 0.3 mA 스파이크 후
**수 h 에 걸쳐 감쇠, 60 h 에서 ≈0.005 mA 이고 아직 내려가는 중**. **어느 크기 시편인지 캡션에 없다**
("Representative"). `[재현]` (a) 의 감쇠분 ≈0.0055 mA ≈ (b) 의 정상 전류 ≈0.005 mA — 같은 시편류라면
σ_ion/σ_e ≈ 0.045 로 **NCM-M 의 비(≈1/50)와 자릿수가 맞는다**(`[추론]` 대표 = M 일 가능성).

## Fig. S7 — ★ 미사이클 단면 SEM + S 맵 `[도표]`
(a, d) L: 둥근 입자/구멍이 전 두께에 흩어짐. (b, e) **M: 위쪽 ≈25–30 µm 에 큰 구형 입자가 몰린 띠 +
그 아래 수평 틈(어두운 공동)**, S 맵에서도 **위쪽 띠가 S 빈약(어두움)** ⇒ `[도표]` **CAM 풍부·SE 빈약
층**이 보인다. (c, f) S: 균질해 보이는 층, 아래에 SE 분리막(밝은 S).
⚠ 저자는 "do not reveal major inhomogeneities" — **(b, e) 는 그렇게 읽히지 않는다**(D7). 그리고
**어느 면이 위(집전체 면인가 자유면인가)인지 캡션에 없다** — (b) 의 위 띠가 집전체 면이라면
**XRD 가 보는 바로 그 층이 SE 빈약층**이다(`[추론]`, §5-1-c).

---

# 4. 검산과 새 계산

## 4-1. 원문 수치 검산

| 항목 | 원문 | `[재현]` | 판정 |
|---|---|---|---|
| NCM622 이론 용량 | (인쇄 없음) | M = 96.93 g mol⁻¹ → **276.5 mAh g⁻¹** | 기준 |
| XRD 용량 L | 90 | Δx = 1 − 0.53: **89.7** · Δx = 1.02 − 0.53: 93.5 | ✅ (1−x 규약) |
| XRD 용량 M | 92 | 88.8 · **92.9** | ✅ (1.02−x 규약) |
| XRD 용량 S | 153 | 146.3 · **151.7** | ≈ (1.02−x 규약, −1.3) |
| ⇒ | | **셋을 동시에 재현하는 한 규약은 없다**; 어긋남 ≤ 4 mAh g⁻¹ < `x` ±0.02 의 ≈±5.5 mAh g⁻¹ | 오차 안 |
| σ 식 | SI "σ = (R×A)/l" | 차원상 **σ = l/(R·A)** | ❌ 오기 (D1) |
| 벌크 대비 | "roughly 2 orders" | 2×10⁻⁴ / 10⁻⁶ = 200 | ✅ |
| σ_e 범위 | "3 orders … 10⁻³ … 10⁻⁶" | `[도표]` 7.7×10⁻⁴ → 1.4×10⁻⁶ = **2.7 자릿수** | ✅ |
| 분극 | "100 to 200 mV" | `[도표]` S2 +80 / +130 / +190 mV | ≈ (S 는 100 미만) |
| Table S1 V | — | V = (√3/2)a²c: L 100.14 · M 99.98 (인쇄 100.10 · 100.00) | ✅ |

## 4-2. ★ 이 편에서 새로 계산한 것

**(a) 3항 분해** — `Q = θ · η · Q_full`, `θ = 1 − f_inactive`, `η = (1.02 − x_active)/(1.02 − 0.31)`
(분모 = LIB 4.4 V 까지의 Δx, Fig. 3b 끝점; `Q_full` ≈196 mAh g⁻¹):

| | θ | η(활성 상) | θ·η | ln θ | ln η |
|---|---|---|---|---|---|
| NCM-S | 0.98 | 0.79 | 0.77 | −0.02 | **−0.24** |
| NCM-M | 0.73 | 0.65 | 0.47 | −0.31 | **−0.43** |
| NCM-L | 0.69 | 0.69 | 0.48 | **−0.37** | **−0.37** |

⇒ **L 에서도 결손의 절반, M 에서는 과반이 "활성 입자가 덜 충전된 것"** 이다. 제목과 초록은 불활성만 말한다.

**(b) 용량만으로 본 전극 평균 불활성 상한** — 활성 상이 **완전히** 충전됐다고 쳐도
`f_inactive ≤ 1 − Q/Q_full`: **L ≤ 57 % (C/10) · ≤ 44 % (C/50) · M ≤ 39 % (C/30) · S ≤ 3 % (C/30)**.
(XRD 불필요. §5-2 에서 1호 예측을 기각하는 데 쓴다.)

**(c) X 선 정보 깊이** — Cu Kα 질량감쇠계수(NIST 근사: Ni 48.8 · Co 320 · Mn 285 · O 11.5 · P 77.3 ·
S 91.3 cm² g⁻¹; Ni 는 K 흡수단 아래) → NCM622 ≈92.8 · β-Li₃PS₄ ≈78.4 · 7:3 복합체 **≈88.5 cm² g⁻¹**.
대칭 반사에서 1/e 깊이 `t = sin θ / (2μ)`:

| 공극률 | 003 (18.7°) | 104 (44.4°) | 2θ = 90° |
|---|---|---|---|
| 0 | 2.8 µm | 6.6 µm | 12.3 µm |
| 0.20 | **3.5 µm** | **8.2 µm** | **15.4 µm** |
| 0.48 (G1 의 인쇄값 조합) | 5.4 µm | 12.6 µm | 23.7 µm |

⇒ **95 % 깊이(3t)로 잡아도 003 은 ≈10–16 µm, 전체 패턴은 ≈25–70 µm** — **90 µm 전극의 집전체 면 쪽**이다.

**(d) 셀 기하** — 면적 용량 → 양극 **0.66–0.80 cm²**; In 음극 0.503 cm²; In 36.7 mg → LiIn 까지 **8.58 mAh**;
첫 충전 뒤 **Li/In ≈0.07–0.19** (평균, 균일 가정) ⇒ In + LiIn 2상 영역 안(`[추론]` 20호가 본 표층 구배라면 표층은 더 높다).
SE 펠릿 60 mg · 400 µm 를 ∅10 mm 로 두면 **상대밀도 ≈1.02** — ∅10 mm 가정 또는 두께 근사가 맞지 않는다(G1·G5).

**(e) 1호 모델을 이 편의 조성에 놓기** — §5-2.

---

# 5. 우리 축에서의 판정

## 5-1. ★★★★ Q1 — "XRD 로 본 비활성 AM 분율" 은 `1 − θ_AM` 의 측정인가, 역산인가

### (a) 측정 원리를 식 단위로

1. 충전 복합체의 회절 패턴 `I(2θ)` 를 **두 NCM 상**(같은 구조 R3̄m, 다른 격자)으로 Rietveld 정련한다.
   각 상의 적분 세기는 `I_j ∝ s_j · (구조인자, LP, 흡수)` 이고, 정련된 scale factor `s_j` 로 **무게 분율**
   `w_j = s_j Z_j M_j V_j / Σ_k s_k Z_k M_k V_k` (Hill–Howard) 를 얻는다.
2. 상의 정체는 **격자상수**로 정한다: 한 상은 operando 교정 곡선 `a(x), c(x)` 위의 `x ≈ 0.46–0.56`
   (**active**), 다른 상은 미충전 분말과 같은 a, c (**inactive, SOC = 0**).
3. ⇒ `f_inactive = w_inactive / (w_active + w_inactive)` — **용량이 한 번도 입력되지 않는다.**
4. 그 다음에 **독립 대조**로 `Q_XRD = (1 − f_inactive) · (x₀ − x_active) · Q_th` 를 계산해 셀 용량과 비교한다.

⇒ **판정: 역산이 아니다. 측정이다.** 두 상이 같은 물질이라 흡수·미세흡수 보정이 상쇄되고(두 상의 μ 가
사실상 같다), 이름표(active/inactive)는 **격자상수라는 두 번째 독립 관측**이 붙인다.
**계보 22 편에서 "전기화학적으로 쓰이지 않은 양극 활물질의 분율" 이 전기화학 밖의 채널로 측정된 첫 편이다.**

### (b) 그러나 잰 것은 `1 − θ_AM` 보다 넓다

| 1호 `1 − θ_AM` | 이 편 `f_inactive` |
|---|---|
| **전자** 퍼콜레이팅 클러스터 밖 AM 부피 (기하, 이진) | **첫 C/10 충전에서 x 가 1 에서 움직이지 않은** 결정 영역의 무게 분율 |
| 이온 경로 무관 (별도 `θ_SE`) | 전자 고립 ∪ **이온 고립** ∪ **SE 접촉 없음** ∪ **2차 입자 내부 미반응 코어** ∪ **C/10 에서 못 닿음** |
| 율 무관 | **C/10 한 점** — 율 의존 여부 미시험(G4) |
| 전극 평균 | **집전체 면 표층 가중**(§4-2c) |

- 이봉(Fig. 3a)은 **결정 영역 단위의 전부/전무**만 말한다. 2차 입자(L d₅₀ 15.6 µm) 안에서 **SE 가 닿는 바깥
  1차 입자만 반응하고 코어가 남는** 경우도 이봉이다 — LIB 대조에서 크기 효과가 없는 것은 **액체가 2차 입자
  기공으로 스며들기 때문**일 수 있어 이 대안을 지우지 못한다(`[추론]`).
- ⇒ **`f_inactive` 는 `1 − θ_AM^{elec}` 의 상한**(같은 자리에서)이다. 저자의 "전자" 배정은 **§5-1-d 의 병치**다.

### (c) 측정 위치 — 집전체 면

`[인쇄]` 셀을 "without breaking the pellet apart" 분해하고 "cathode composite side up" 으로 놓는다 —
드러난 면은 **plunger(집전체)에 닿아 있던 면**이다. `[재현]` 그 면에서 003 의 1/e 깊이는 ≈3 µm,
Rietveld 전체로 ≈8–15 µm. ⇒ `[추론]` **XRD 가 보는 입자는 집전체에서 한두 입자 거리 안에 있다.**
- **전자 고립은 여기서 가장 드물다** — 집전체에 닿았거나 한 입자 건너인 입자는 퍼콜레이션과 무관하게
  전자가 닿는다(1호 모델도 집전체 경계에서 출발한다).
- **이온 고립은 여기서 가장 흔하다** — 분리막에서 가장 멀다(≈90 µm, σ_ion ≈10⁻⁶ S cm⁻¹).
- ⇒ **NCM-L 의 31 % 가 이 층에서 나왔다면, 그것은 저자 배정(전자)보다 이온·SE 접촉 쪽과 더 잘 맞는다.**
  ⚠ 첫 층 입자 중 SE 막에 덮여 plunger 에 직접 안 닿는 것은 전자 고립될 수 있다 — 방향성만 주장한다.
- 그리고 **용량 대조가 ±7 % 안에서 닫힌다** — 표층 가중 값이 전극 평균과 크게 다르지 않다는 뜻이고,
  `[추론]` **두께 방향 구배가 약하다** ⇒ 집전체 거리(전자)도 분리막 거리(이온)도 지배적이지 않고
  **입자 국소 원인(입자–SE 접촉·계면층·입자 내부)** 쪽을 가리킨다. 이것이 우리 카드의 `θ` —
  **"입자가 SE 와 닿아 있는가"** — 에 더 가깝다.
- ⚠ Fig. S7(b, e) 의 **SE 빈약 윗띠**가 집전체 면이라면(방향 미기재) XRD 가 **분리된(segregated) 층**을
  보는 것이고, 저자의 "no major inhomogeneities" 가정이 측정값을 직접 오염시킨다.

### (d) 원인 배정 — 병치(juxtaposition)

`[인쇄]` 원인 = "lack of **electronic** contact", 근거 = Fig. 4. `[재현]` §3 Fig. 4 표:
- NCM-L: σ_e ≈ σ_ion (비 ≈1.5) — **벌크 전도도로는 전자와 이온이 같은 자리에 있다.**
- NCM-M: σ_e/σ_ion ≈ 50 — S(≈550)와 **같은 쪽**(전자 ≫ 이온). 저자의 S 판정 논리("이온 제한")를 그대로 쓰면
  M 도 이온 제한이다. 그런데 불활성 27 %.
- 불활성 **M ≈ L** 인데 σ_e 는 **≈26 배** 차이 — **불활성 분율이 σ_e 를 따라가지 않는다.**
- 시편도 다르다(G10): 미충전 · 별도 펠릿 · 벌크 평균 ↔ 충전 후 · 셀 안 · 표층.
⇒ **배정은 시험되지 않았다.** "전자 비연결" 은 **가능한 설명 중 하나**이고, 이 편의 데이터가 그중 하나를
고르지 않는다.

### (e) Q1 판정

**+0.5 — 계보 22 편 만에 처음으로 `θ` 형 양(무차원 비활성 분율)이 전기화학 밖 채널로 측정됐다.**
**반 칸인 이유 넷**: (1) 잰 것이 `1 − θ_AM` 의 **합집합 상한**이다(접촉 손실만이 아니다) (2) **신품 첫 충전
한 점** — `θ(N)` 은 **여전히 0 편** (3) **표층 가중**, 전극 평균이 아니다 (4) **n 미기재**, ± 는 Rietveld esd.
18호의 Q1 반 칸(접촉 **면적 비**, Image-J)과 **다른 층위**다 — 18호는 기하, 22호는 **전기화학적 결과(쓰였나)
의 구조 측정**이다.

## 5-2. ★★★★ 1호 대질 — 인용 문장과 원문

### (a) 1호가 이 편에서 가져간 것 (1호 digest §1·§4.1·§6.6·§7.1·§9 에서)

| # | 1호의 문장 (`[인쇄]`, 1호) | 이 편 원문 | 판정 |
|---|---|---|---|
| 1 | 서론: AM 입자 크기 ↑(최대 20 µm) → 전자 전도도 급락, 무탄소 NCM-622 + LPS | "approximately **20 to 5 μm**" (서론의 표현), σ_e **10⁻³ → 10⁻⁶** | ✅ ("20" 은 저자 자신의 어림; 실측 d₅₀ 최대 15.6) |
| 2 | "high fractions of **inactive NCM-622 for large AM particle sizes, measured via ex situ X-ray diffraction** and with their **attributed low effective electronic conductivity**" | 27 · 31 % (M, L), ex situ XRD, 전자 전도도로 귀속 | ✅ ("attributed" 가 정확하다 — 귀속이지 증명이 아니다) |
| 3 | "the total packing density of AM used by Strauss et al. is **not known, as the porosity was not measured**" | `poros*` 본문·SI **0 회** | ✅ |
| 4 | 무탄소 AM + SE 2성분 구성이 Strauss 와 같다 / 실험적으로 뒷받침 | 7:3 w/w, 탄소·바인더 없음 | ✅ |
| 5 | "5 µm 가 NCM 입자로 현실적 (Strauss 에 따르면)" | NCM-S d₅₀ **4.0 µm**, "d ≪10 μm" | ≈ (4.0 을 5 로 둥글림) |

⇒ **8호식 "숫자를 틀리게 옮김" 은 없다.** 1호는 **정직하게** 옮겼다.

### (b) 그러나 "correlate well" 이 가리는 것 — 공극률 없이도 비교된다 `[재현]`

- 7:3 wt 의 AM 부피 분율(고체 중): 1호 자신의 밀도비(1호 G4 역산 `ρ_AM/ρ_SE ≈ 2.35–2.45`)로 **48.8–49.8 vol%**,
  문헌형 밀도(4.75/1.87)로 47.9 vol%. **공극률은 이 값을 낮추기만 한다** ⇒ **무공극이 1호에게 가장 유리한 상한.**
- 1호 식 (8) `p_c = 7.83 ln d + 36.67`: **p_c(4.0) = 47.5 · p_c(8.3) = 53.2 · p_c(15.6) = 58.2 vol%**.
- 1호 Fig. 3(5 µm) 곡선을 `[인쇄]` "steepness … similar for all particle sizes" 에 기대 p_c 차만큼 옮기면
  (1호 digest 의 figure-read 표: 48 → ≈16 · 49 → ≈25 · 50 → ≈48 · 51 → ≈71 · 52 → ≈81 %):

| | AM − p_c (무공극 상한) | 1호 예측 불활성 | **측정 불활성 (XRD)** | **용량만의 상한 (§4-2b)** |
|---|---|---|---|---|
| NCM-S | +1.3 ~ +2.3 vol% | **≈23–40 %** | **2 %** | **≤ 3 %** |
| NCM-M | −3.4 ~ −4.4 | **≈95 %** | **27 %** | **≤ 39 %** |
| NCM-L | −8.4 ~ −9.4 | **≈95–97 %** | **31 %** | **≤ 44 %** |

⇒ **1호 모델은 이 편의 조성에서, 가장 유리한 가정으로도, 불활성을 3–15 배 과대 예측한다** — 그리고 이것은
**XRD 없이 용량만으로** 기각된다. 공극률이 몇 %만 있어도 S 까지 p_c 아래로 내려가 격차는 커진다.
1호가 이 계산을 할 수 없었던 것이 아니다 — **공극률이 부호를 정하는 방향이 알려져 있었다.**
- ⚠ 1호 쪽 변명의 여지(`[추론]`): SE 입자 크기 **3 µm 고정**(1호 G3) ↔ 이 편 β-Li₃PS₄ 는 습식 합성 나노다공체 ·
  밀링이 입자 형상을 바꿈 · 1호는 **구형 무겹침**. 즉 **실재 복합체의 AM–AM 접촉망이 모델보다 훨씬 잘 이어진다.**
  그러나 그 경우에도 결론은 같다 — **1호의 `p_c(d)` 는 이 재료계의 불활성 분율을 예측하지 못한다.**
- ⇒ **우리 계획에 대한 함의**: DEM 이 주는 `θ` 를 `1 − f_inactive` 와 **곧바로 등치하면 안 된다**. 최소한
  (i) 정보 깊이 가중 (ii) 이온 쪽 `θ_SE` (iii) 입자 내부 항을 붙인 **관측 연산자**가 필요하다.

## 5-3. ★★★ 곱 축퇴 처방 — 여섯 번째 적용

| 처방 단계 | 필요한 입력 | 22호 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | `impedan*` **본문·SI 0 회**, `capacitan*` 0 | ❌ **주파수 영역 없음** |
| **2단계** (18호) | + 면적을 아는 대조군 | ① **LIB 대조**(같은 CAM, 액체 = 완전 적심): 크기 효과 "negligible" ⇒ **재료·고유 고체확산은 크기 효과의 원인이 아니다** ② **M ↔ L 같은 로트 체 분리 쌍**(d₅₀ 1.9 배) ⚠ 그러나 **면적 자체는 미측정**(BET 0, 밀링 후 입도 0), 액체는 2차 입자 기공을 적셔 **SE 접촉 면적의 대조가 아니다** | ⚠ **부분** |
| **3단계-a** (19호) | `Ea` | 25 °C 한 점 | ❌ |
| **3단계-b** (19호) | `C` 물리 상한 | `C` 없음 | ❌ |
| **4단계** (20호) | 시간 영역에도 같은 검사 | Fig. S6(b) 전자 차단 DC 분극: `[도표]` τ ≈ 5–10 h, `[재현]` R_ss = 0.3 V / 5 µA = **60 kΩ** ⇒ **C = τ/R ≈ 0.3–0.6 F ≈ 0.4–0.8 F cm⁻²** (0.785 cm² 가정) = 이중층(10 µF cm⁻²)의 **≈10⁴–10⁵ 배** | ✅ **적용 — 계면이 아니다** |

- **4단계의 뜻**: 이 과도는 혼합전도체(NCM 이 섞인 복합체)의 **화학량 분극(Li 저장)** 이다 — 계면 이중층이 아니다.
  `[재현]` 과도의 초과 전하 ≈0.36 mAh ≈ 시편 NCM 용량(70 mg × 180 = 12.6 mAh)의 **≈3 %**. 그리고 `[도표]`
  **60 h 에서도 전류가 아직 내려간다** ⇒ `[추론]` **σ_ion 은 상한**이다(정상 상태 미도달). 원인 배정(§5-1-d)의
  한 축이 **상한값 위에** 서 있다.
- ★★★ **처방 목록에 없는 채널이 들어왔다 — "SOC 를 따라가는 상 분율"**: 곱 `A_eff · ε_p / R_s` 의 **`ε_p` 쪽
  (쓰이는 부피)을 구조 채널이 직접 뗀다.** 남는 것은 `A_eff · j₀`(활성 입자당 접촉 면적 × 동역학)이다.
  `[도표]` 분극 +80 / +130 / +190 mV (S2) ↔ `[재현]` 활성 CAM 면적당 전류 비(∝ d / θ) **1 / 2.2 / 5.5** —
  선형 동역학이면 면적 설명이 **과잉**, Butler–Volmer/Tafel 영역이면 **부족하지 않다** ⇒ **면적 ↔ j₀ 는 이 자료로
  못 가른다.** 저자는 `[인쇄]` "deterioration of kinetics" + "insulating layer increases the kinetic barrier" 로
  **j₀ 쪽**에 놓는다 — **16호 · 20호와 같은 "한쪽 끝 선택"**, 다만 이 편은 식이 없다.
- ⇒ **개념 페이지 처방 표에 한 줄**: *"SOC 추종 상 분율 (ex situ/operando XRD) — `θ·ε_p` 를 떼어 낸다;
  열화 판에서는 **두 SOC 에서** 찍어 **SOC 를 따라가지 않는 상**의 분율을 잰다(고립 당시 SOC 에 얼어붙은 상은
  pristine 이 아닐 수 있다)."*

## 5-4. 17호 함정 — 이 편은 어디에 서나

- **상대극**: 순수 In 박 100 µm · ∅8 mm, **사전 리튬화 없음**. 기준극 **없음**.
- **전위 처리**: `[인쇄]` "3.8 and 2.3 V with respect to In/InLi (**corresponding to** 4.4−2.9 V vs Li⁺/Li)" ·
  SI Fig. S2 "(**0.6 V difference**)". `assum*` 1 회(분리 문단, 전위 무관) · `0.62` **0 회** · `0.6 V` **1 회**.
  ⇒ **Q5 일곱 번째 형태 = "가정이 대조군의 전압창을 정한다"** — LIB 대조를 4.4–2.9 V 로 돌린 것 자체가
  0.6 V 가정의 산물이다. 가정은 **괄호 속 환산**과 **SI 그림의 축 이동**으로 들어간다(20·21호 맹점).
- `[도표]` **자체 정합 검사 하나는 된다**: C/30 NCM-S 충전 개시 평탄 **≈3.05 V vs In/InLi** ↔ LIB 충전 개시
  **≈3.63–3.65 V vs Li** ⇒ 차 **≈0.58–0.60 V** (C/30 분극 포함이므로 실제 오프셋은 이보다 작거나 같다).
  **±30 mV 수준에서 0.6 V 와 모순 없다.**
- **주 주장은 함정에서 구조적으로 면제된다**: 불활성 분율과 활성 상 `x(Li)` 는 **양극 결정에서 직접** 읽는다 —
  상대극 전위가 한 번도 들어가지 않는다. **계보 22 편 중 양극 상태를 전위 없이 읽은 첫 편이다.**
  (단, `x_active ≈ 0.5` 가 LIB 평형 4.4 V 의 x ≈ 0.31 보다 높다는 것 — 즉 **컷오프에서 활성 상이 덜 충전됐다**는
  것 — 은 컷오프 전위에 의존한다. 오프셋이 +20 mV 어긋나도 `x` 차 0.19 를 설명하지 못한다: `[추론]`.)
- **용량·CE 축은 면제되지 않는다** `[추론]`: Li 가 양극에서만 오는 순수 In 셀에서 **방전 끝은 음극이 다시
  Li-빈약 쪽으로 돌아가는 구간**이다. `[재현]` 첫 충전 뒤 Li/In ≈0.07–0.19(평균)이고 20호가 본 것처럼 표층에
  몰려 있다면, 방전 끝의 음극 전위 상승(17호 ③ 국소 고갈)이 **2.3 V 컷오프를 먼저 칠 수 있다.** 저자는
  CE 50–70 % 를 **양극 쪽**(화학-기계 · 계면층)에만 배정한다 — **3전극 없이 가를 수 없다.**
- ⇒ **판정: 주 주장은 피했다(설계상), 부수 주장(CE)은 밟았다.** 20호("3전극으로 명시적으로 피함")와 대칭이다.

## 5-5. Q4 — 22/22 연속 0, 그리고 0 의 성질

`identif*` 1 회("allowed us to **identify** one as being partially delithiated" — 상 동정) · `unique*`·`degenera*`·
`error bar` 0 · `uncertaint*` 1 회("A detailed discussion of the **uncertainty** is provided in the SI") · `fit*` 1 회(SI,
선형 적합).
**열다섯 번째 성질 = "측정이 분할을 대신했고, 남은 자리(원인)는 다른 시편의 값과 병치됐다."**
- 역문제가 없다 — `θ` 와 `η` 를 **적합하지 않고 따로 잰다**. 그래서 **분할의 유일성 문제가 생기지 않는다**
  (14호 "역문제가 없다" 와 가깝다). 용량 대조의 닫힘은 **값(분할)의 검증**이고 정당하다.
- 그러나 **원인 배정("전자")은 별도 펠릿의 벌크 σ 와 나란히 놓였을 뿐**이고, 그 σ 가 불활성 분율의 M ≈ L 을
  따라가지 않는다는 것을 저자는 검토하지 않는다. 대안(이온 고립 · SE 접촉 · 입자 내부 · 분리층)은 인쇄조차 안 된다
  — 18호("갈림을 인쇄하고 가르지 않음")보다 **한 단계 앞**, 갈림을 **인쇄하지도 않았다**.
- ★ **방법 자체에 작은 비유일성이 있고 밟고 지나간다**: 교정 곡선 **c(x) 는 x ≈ 0.5 에서 최대라 두 가지(branch)**
  를 갖는데, 활성 상 교차가 **정확히 그 최대점 위**에 앉는다(Fig. 3b). `[인쇄]` Table S1 에서 **L 과 M 의 a 가 같다
  (2.823(1))** ⇒ 단조 채널(a)로는 **x_L = x_M**, 인쇄된 0.53 ↔ 0.56 의 차는 **c 의 가지 선택**에서 온다.
  단조인 V(x)(Fig. S4)로 읽으면 `[도표]` **L ≈0.55 · M ≈0.52 — 순서가 뒤집힌다.** 저자의 유일한 인정은
  "shaded areas represent the deviation in x(Li) between a and c". ⇒ **"비단조 교정 → 가지 선택" 은 우리
  degeneracy 물음의 소형판이다**(크기는 ±0.02–0.03, 저자 오차 예산 안).
- 계보 비교: 12호 "낱말 없음" · 14호 "역문제 없음" · 15호 "추정기 없음" · 16호 "밟고 지나감" · 17호 "인쇄로 사양" ·
  18호 "갈림을 인쇄하고 안 가름" · 19호 "어휘 없이 기하로 물음" · 20호 "작도" · 21호 "값의 정확도를 배정의 유일성으로
  읽음" · **22호 "측정이 분할을 대신했고 원인은 병치"**.

## 5-6. Q2·Q3·Q5·Q6·Q7·Q8

- **Q2 +0.5** — ★ **"물질은 그대로인데 쓰이지 않는" 양극 활물질을 구조 채널로 보고, 그것을 "쓰였지만 덜 충전된"
  활물질(η)과 같은 측정에서 가른 첫 편.** 그리고 **불활성 상의 격자가 pristine 과 같다** ⇒ 진짜 `LAM_PE`(구조 변화)와
  접촉형 손실을 **원리적으로 가를 수 있는 서명**이다. 보조 채널 둘(율 스윕 · LIB 대조)도 있다.
  **반 칸인 이유**: 신품이라 **가를 `LAM_PE` 가 없다** — 서명의 존재를 보였지 분리를 실행하지 않았다(21호 Q2 반 칸과
  같은 논리). ⚠ `[인쇄]` Table S1 의 불활성 L 은 c = 14.240(1) ↔ pristine 14.220(1), V 101.73 ↔ 101.44 로 **esd 의
  ≈20–30 배** 다르다 — "SOC = 0" 은 교정 분해능 안에서만 참이다(D9).
- **Q3 층 추가(칸 이동 없음)** — **measured-crystallographic + 방법 오차 예산을 인쇄한 계보 첫 편**(상 분율 −3/−11 %,
  x ±0.02, 부반응 미반영 명시, 검출 한계 명시). ⚠ 단위 모호(G9) · n 미기재(G3) · ± 는 esd.
- **Q5 칸 이동 없음** — 일곱 번째 형태(§5-4). 기준극 0, 0.6 V(0.62 아님).
- **Q6 칸 이동 없음** — **보고·통제**: 제조 125 / 375 / 125 MPa, 운전 **55 MPa**, 전도도 시편 375 · 250 MPa,
  XRD 셀 "approx. 55 MPa". 스윕 0. ⚠ `[인쇄]` "volume contraction during charging leads to a reduced electrical
  contact" 를 **ref 18(압력 변화 감시 논문)** 로 뒷받침 — 압력 축의 기구는 **인용**으로만 온다.
- **Q7 해당 없음** — In 음극. `dead`·`plating` 0.
- **Q8 칸 이동 없음** — NCM622 는 새 화학이 아니다(1호 모델 대상). 대신 **`x(Li)` ↔ 격자(a, c, V) 교정**이 들어왔다 —
  OCP 가 아니라 **구조 축의 SOC 눈금**이다. OCP 기울기는 LIB 곡선(Fig. 1d)뿐.

---

# 6. Q1~Q8 판정 (채움표 22호 행의 근거)

| Q | 판정 | 요지 |
|---|---|---|
| **Q1 정량** | **+0.5** | **`θ` 형 양의 첫 측정** — 2상 Rietveld 상 분율, 용량 비입력, 용량은 독립 대조(±7 %). ⚠ 합집합 상한 · 신품 1 점 · 집전체 면 표층 · n 미기재 |
| **Q2 독립관측** | **+0.5** | 구조 채널이 "불활성(pristine 격자)" ↔ "활성·덜 충전(`x ≈ 0.5`)" 을 한 측정에서 가른다 = `θ` ↔ `η` 분리 + `LAM_PE` 판별 서명. 신품이라 `LAM_PE` 분리는 미실행 |
| **Q3 라벨층위** | 층 추가 | measured-crystallographic + 방법 오차 예산 인쇄(첫 편). 단위 모호 · n 0 |
| **Q4 유일성** | **0 / 22** | 열다섯 번째 성질 — "측정이 분할을 대신했고 원인은 병치". c(x) 가지 선택을 밟고 지나감 |
| **Q5 Li-In 기준** | 칸 이동 없음 | 0.6 V 가정, 일곱 번째 형태 = "가정이 대조군 전압창을 정한다"; 저율 개시 전위로 ±30 mV 정합 |
| **Q6 압력** | 칸 이동 없음 | 보고·통제(55 MPa 운전), 스윕 0 |
| **Q7 dead Li** | 해당 없음 | In 음극 |
| **Q8 화학·OCP** | 칸 이동 없음 | NCM622; 구조 SOC 눈금(a, c, V vs x) 추가 |

---

# 7. 우리 프로젝트와의 접점

1. ★★★★ **`θ` 의 measured 라벨이 존재한다 — 그러나 관측 연산자가 필요하다.** DEM 의 `θ_AM` 과 XRD 의
   `1 − f_inactive` 를 잇는 사상은 **항등이 아니다**: (i) 정보 깊이 가중(집전체 면 3–15 µm) (ii) 이온 쪽 고립
   (iii) 입자 내부 코어 (iv) 율. 이 넷을 모델 쪽에 붙여야 **같은 양을 비교**한다. 1호 식 (8) 을 그대로 대면
   **3–15 배** 어긋난다(§5-2).
2. ★★★ **3항 분해의 첫 실측 분리** — `θ` 와 `η` 가 따로 나오고, **C/50 에서도 `η → 1` 이 안 된다**(`θ` 가 율 불변이라면
   L 의 C/50 η ≈ 110/(0.69·196) ≈ 0.81). 우리 개념 페이지의 "율 연산자" 는 **극저율에서도 불완전**하다 — 또는 `θ` 가
   율 의존이다. **이 편은 둘을 못 가른다**(XRD 가 C/10 한 점뿐, G4).
3. ★★★ **OCV 적합이 이 셀에서 무엇을 보고했을까** (`[추론]`, 사고 실험): 두 상 복합체의 OCV 는 활성 상의 곡선
   하나를 **용량 축으로 줄인 것**이다(불활성 상은 전위에 기여하지 않는다). 적합은 `a_PE ≈ θ·(…)` 로 **31 % 의
   `LAM_PE`** 를 보고한다 — **물질은 전부 그대로다**(격자 pristine). **닻 물음의 정확한 사례**이고, 이 편은 그것을
   **구조 채널로 깬다.** ⇒ Evidence **Against**(독립 관측이 존재한다) 쪽 — 다만 **ex situ · 파괴 분석**이다.
4. ★★ **열화 판 설계 제안**: 두 SOC 에서 XRD → **SOC 를 따라가지 않는 상의 분율**이 `1 − θ(N)`. 고립 당시 SOC 에
   얼어붙은 상은 pristine 이 아니므로 "pristine = 불활성" 규칙은 **신품에서만** 쓸 수 있다.
5. **degradation-degeneracy 수치와 비교하지 않는다** — 이 편에는 적합·열화가 없다.

---

# 8. 후속 후보

| 순위 | 문헌 (이 편의 ref) | 왜 | 축 |
|---|---|---|---|
| ★★★★ 1 | **Koerver, Aygün, Leichtweiß, Dietrich, Zhang, Binder, Hartmann, Zeier, Janek, *Chem. Mater.* 29, 5574−5582 (2017)** (ref **9**, 본문 **4 회** 인용) | **큐 22번.** 이 편의 저 CE·"volume contraction → reduced contact"·절연 계면층 서술의 **기구 원전**. 이 편이 가르지 않은 "접촉 손실 ↔ 계면층" 을 원전이 가르는지 | Q1·Q2 |
| ★★★ 2 | **Zhang, Schröder, Arlt, Manke, Koerver, Pinedo, Weber, Sann, Zeier, Janek, *J. Mater. Chem. A* 5, 9929−9936 (2017)** (ref **18** + SI ref 2) | 이 편 **셀 장치의 원전**(양극 면적·지름, G5) + "충전 중 부피 수축 → 접촉 감소" 의 **압력 감시** 근거 | Q1·Q6 |
| ★★★ 3 | **Zhang, Weber, Weigand, Arlt, Manke, Schröder, Koerver, Leichtweiss, Hartmann, Zeier, Janek, *ACS Appl. Mater. Interfaces* 9, 17835−17845 (2017)** (ref **16**) | 7:3 조성의 근거 + 저자에 토모그래피(Arlt·Manke) — **같은 연구망 복합체의 공극률 실측**이 있을 가능성(1호 G2·이 편 G1 을 메울 후보) | Q1 |
| ★★ 4 | **Nam, Oh, Jung, Jung, *J. Power Sources* 375, 93−101 (2018)** (ref **17**) | 건식 ↔ 슬러리 혼합 복합전극 — **분리(segregation)·미세구조**(Fig. S7 D7). ⚠ 원장의 "Nam 2018 *JMCA* 6, 14867"(In 음극)과 **다른 논문** | Q1 |
| ★★ 5 | **Koerver, Walther, Aygün, Sann, Dietrich, Zeier, Janek, *J. Mater. Chem. A* 5, 22750−22760 (2017)** (ref **12**) | 탄소 첨가제·산화 계면층 — 계면층(j₀) 쪽 원전 | Q2 |
| ★ 6 | **Chen, He, Zhang, Wang, Ni, *Energies* 6, 1632−1656 (2013)** (ref **26**) | 저자가 기댄 "percolation theory" — **SOFC** 원전. 1호 모델과의 관계 | Q1 |
| ★ 7 | **de Biasi et al., *J. Phys. Chem. C* 121, 26163 (2017)** (ref 20 / SI ref 4) · **Kondrakov et al., *J. Phys. Chem. C* 121, 24381 (2017)** (ref 21) | a·c–x 교정의 원전(c 최대의 기구) | Q8 |

원장에 이미 있는 것 중 이 편이 가리키는 것: **Koerver 2017 *Chem. Mater.* (큐 22) — ref 9.**
**Ikezawa 2020 · Nam 2018 *JMCA* · Santhosha 2019 · Sedlmeier 2023 은 이 편에 없다**(2018 년 3 월 게재라 뒤 셋은
시간상 불가능; Nam 2018 *JMCA* 도 이 편 뒤다).

---

# 9. 주장하지 않는 것

- **`f_inactive` 가 `1 − θ_AM` 과 같다고 주장하지 않는다.** 상한(합집합)이라는 것까지다.
- **XRD 가 전극의 몇 %를 봤는지 정확한 값을 주장하지 않는다.** §4-2c 는 NIST 근사 감쇠계수 · 가정 공극률 ·
  대칭 반사의 1/e 깊이다. **"집전체 면 표층" 이라는 방향**이 주장이다.
- **원인이 이온이라고 주장하지 않는다.** 저자의 "전자" 배정이 **자기 데이터로 시험되지 않았다**는 것까지다.
- **1호 모델이 틀렸다고 단정하지 않는다** — 1호의 SE 크기·구형 가정이 이 복합체와 다르다. 주장은
  **"1호 식 (8) 은 이 재료계의 불활성 분율을 예측하지 못하고, 그것은 공극률 없이도 보인다"** 이다.
- **§4-2a 의 θ·η 표는 `Q_full` = LIB 4.4 V 기준**이다. ASSB 컷오프의 실제 양극 전위는 0.6 V 가정 위에 있다.
- **Fig. S7(b, e) 가 분리층이라고 단정하지 않는다** — 단면 방향이 캡션에 없고, 파단면 아티팩트일 수 있다.
- **이 편의 수치는 전부 신품 첫 사이클이다.** `θ(N)` 은 0 이다.

---

# 10. 어긋남 (지면 내부 정합)

| # | 어긋남 | 크기 |
|---|---|---|
| **D1** | SI 전도도 식 "σ = (R×A)/l" | 차원 역전 — σ = l/(R·A) |
| **D2** | NCM-L = NCM-M 을 **20 µm 체**로 거른 "remaining fraction" ↔ NCM-L **d₅₀ 15.6 µm**(< 20), NCM-M **d₉₀ 13.0 µm** | 체 위에 남은 분획이면 d₅₀ > 20 이어야 한다; M 의 90 % 가 13 µm 이하인데 L 이 나올 양도 적다 (`[추론]` 응집체이거나 "remaining" 이 체 통과분) |
| **D3** | NCM-L "d90 = 26.1" 단위 누락 | 사소 |
| **D4** | LIB "approximately 10% capacity loss", "negligible differences" ↔ `[도표]` Fig. 1d NCM-L 충전 ≈233 · 방전 ≈193 | L 은 ≈17 % 손실, 충전 ≈10 % 더 |
| **D5** | CE M **55 %** ↔ `[도표]` Fig. 1e ≈56/≈94 | ≈60 % (판독 오차 ≈3 %p) |
| **D6** | SI "side reactions … not taken into account in the XRD" ⇒ Q_XRD ≤ Q_echem 이어야 ↔ **L: 90 > 84** | 부호 반대 +6 mAh g⁻¹ (다른 셀이라 셀 간 산포일 수 있다) |
| **D7** | "do **not reveal major inhomogeneities** (Figure S7)" ↔ `[도표]` S7(b, e) M 의 CAM 풍부·S 빈약 윗띠 + 수평 틈 | 정성 |
| **D8** | Fig. 4 두 y 축 자릿수 간격 불일치(5 ↔ 3) — L 의 σ_e 가 σ_ion 아래로 **보이는데** 값은 위 | 인상 반전 |
| **D9** | "remains in a **pristine state (SOC = 0)**" ↔ Table S1 불활성 L c **14.240(1)** vs pristine 14.220(1), V 101.73 vs 101.44 | esd 의 ≈20–30 배 (Rietveld esd 과소 추정일 수 있다) |
| **D10** | 상 분율 오차 "−11% for NCM-S" ↔ 분율 2(1) % | 절대·상대 불명 (G9) |
| **D11** | 결론 "due to a lack of electronic contact" (단정) ↔ 같은 결론 문단 "apparently inactive" | 확신 수준이 XRD 쪽보다 원인 쪽이 높다 — 증거 강도와 반대 |
| **D12** | 초록 "d ≪10 μm" ↔ NCM-S d₅₀ 4.0 · d₉₀ 4.8 | 2.5 배를 "≪" |

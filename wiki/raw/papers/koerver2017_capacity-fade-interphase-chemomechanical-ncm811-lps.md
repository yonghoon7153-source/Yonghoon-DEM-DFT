---
title: "Koerver, Aygün, Leichtweiß, Dietrich, Zhang, Binder, Hartmann, Zeier, Janek 2017 — Capacity Fade in Solid-State Batteries: Interphase Formation and Chemomechanical Processes in Nickel-Rich Layered Oxide Cathodes and Lithium Thiophosphate Solid Electrolytes (Chem. Mater. 29, 5574-5582)"
source_url: local-upload/22._Capacity_Fade_in_Solid-State_Batteries_Interphase_Formation_and_Chemomechanical_Processes_in_Nickel-Rich_Layered_Oxide_Cathodes_and_Lithium_Thiophosphate_Solid_Electrolytes.pdf + 22._Sup_Capacity_Fade_in_Solid-State_Batteries_Interphase_Formation_and_Chemomechanical_Processes_in_Nickel-Rich_Layered_Oxide_Cathodes_and_Lithium_Thiophosphate_Solid_Electrolytes.pdf (SI)
source_url_note: "본문 9쪽(Article, 참고문헌 48편) + SI 7쪽(그림 S1-S8, 표 0). 크로퍼가 본문 그림 6 + SI 그림 8 을 전부 잡았다. Fig. 6 은 PDF 원본 SEM 이미지(2000x2095 px)를 따로 뽑아 틈 폭을 픽셀로 쟀다. **그림 14장 전부 직접 봤다 — 안 본 그림 0장.** PDF 는 커밋하지 않는다."
source_doi: 10.1021/acs.chemmater.7b00931
source_license: "(c) 2017 American Chemical Society — 오픈액세스 아님"
pdf_sha256: 5be652c4d8383b901ae475344dda27a5e873685019f85d04925c9f5b6bee6779
si_sha256: 96534ee472de42057cbb7c8cbdbf0dbcad3403a60137f1b987f8393ae5422624
ingested: 2026-09-23
sha256: a2c0ebfc817f83af7c959fd0e114d3d270fc86e3badb85fc84ae496ce81abe72
---

# 수집 목적

`assb` 섹션 **23호**. 큐 **22번** (22호 = 큐 21 Strauss 2018, 21호 = 큐 20 Sedlmeier 2023, 20호 = 큐 19 Chang 2020,
18호 = 큐 17 Fukunishi 2023). 닻은 `questions/assb-contact-loss-vs-lampe.md`. 큐 문서
(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md`)의 등록 축은 **★★ 접촉 손실의 실험 원전 + 전압·용량축 — 01 의 ref 7**.

> ★★★★ **이 편이 계보에서 차지하는 자리를 먼저 적는다.**
> 1. **이 위키의 `assb` digest 가운데 여덟 편이 이 논문을 인용했다** — 1호(ref 7) · 3호(ref 7) · 4호(ref 8) · 9호([17]) ·
>    18호([23]) · 21호(ref 29) · 22호(ref 9, 본문 4 회). "접촉 손실의 실험 원전" 이라는 이름표는 그 인용들이 붙였다.
>    §5-6 에서 **그들이 가져간 문장이 원문과 맞는지** 하나씩 대조한다.
> 2. 시간상 **계보에서 가장 이르다** (2017-03-07 접수 · 2017-06-09 게재; 22호 Strauss 는 2018-02).
>    Giessen(Janek·Zeier) + KIT BELLA + **BASF** — 1호·22호와 **같은 연구망**이다.
> 3. **두 기구(계면층 CEI · 화학-기계적 접촉 손실)를 둘 다 처음 이름 붙인 편**이고, 22호가 "안 가른" 두 기구의 **원전**이다.
>    그런데 ★ **원전도 가르지 않는다** — 각 기구에 **전용 채널**(XPS ↔ SEM)을 하나씩 붙여 **존재**를 보이고,
>    **몫은 시간 구간으로 배정**한다(§5-1). 그리고 ★★ **SI 에 원전 자신이 쓰지 않은 가르는 입력이 있다**:
>    `R_SE/Cathode(OCV)` 와 `C_SE/Cathode(OCV)` 가 **두 셀 × 네 구간**으로 인쇄돼 있다 — 곱 축퇴 처방 1단계의 입력이 완비된
>    계보 첫 **상태축 위 연속 곡선**이다(§5-3).

⚠ **표기 규약** (사용자 지정): `[인쇄]` = 원문이 실제로 쓴 것 ·
`[도표]` = 그림에서 읽은 값(figure-read ≈) · `[재현]` = 원문 수치로 우리가 다시 계산한 것 ·
`[추론]` = 우리의 해석. **`[인쇄]` 표시가 없는 서술문 중 원문의 주장은 인용부호로만 둔다.**
⚠ 이 편의 `η` 는 **쿨롱 효율**이다(`[인쇄]` "Coulombic efficiency of η = 70.5%"). 우리 3항 분해의 `η(i)`(이용률)와 **다른 양**이다.

---

# 판정 한 줄

> **이 편은 NCM811/β-Li₃PS₄ 무탄소 복합양극 | β-Li₃PS₄ | In 박 셀의 첫 사이클 손실(충전 176 → 방전 124 mAh g⁻¹,
> CE 70.5 %)을 in situ EIS(OCV 별 4-RQ 적합) · XPS(S 2p·P 2p 산화종) · 사후 SEM(입자 둘레 틈)으로 조사해,
> "전위로 구동되는 CEI 형성" 과 "탈리튬 수축에 의한 접촉 손실" 의 **조합**이라고 결론짓는 2017 년 Article** 이다.
>
> ★★★★ **접촉 손실 vs 계면층 — 이 편은 가르지 않는다. 세 관측은 각각 한 기구의 *존재*만 보고, 몫은 *배정*이다.**
> XPS 는 산화종(계면층)만, SEM 은 틈(접촉)만 본다. 둘 다 원인이 될 수 있는 **`R_SE/Cathode` 의 +140 Ω** 은 본문에서 CEI 로,
> **초록에서는 접촉 손실에도** 배정된다(`[인쇄]` "contact loss … further increasing the interfacial resistance" ↔ 결론
> "This resistance was found to originate from a highly resistive interphase"). 첫 사이클 손실 52 mAh g⁻¹ 은 `[인쇄]`
> "combination" 이고 **분할 숫자는 0** 이다. 이후 감쇠는 **소거법**으로 CEI 에 배정된다(SEM 1 회 ↔ 50 회 "similar").
>
> ★★★★ **그런데 가를 입력은 SI 에 있다 — 우리가 가른다.** `[도표]` SI Fig. S2: 첫 충전 3.25 → 3.53 V 에서
> `R_SE/Cathode` 가 **≈105 → ≈257 Ω(×2.4)** 오르는 동안 `C_SE/Cathode` 는 **≈1.8 → ≈1.9 µF(×≈1.0)**. 면적(접촉) 설명은
> `C` 를 **×0.41** 로 떨어뜨려야 한다. 둘째 충전(`R` ×1.5, `C` ×1.0)과 **LTO 대조 셀**(Fig. S6·S7: 첫 방전 `R` ×1.8, `C` ×0.96)도 같다.
> ⇒ **EIS 창(7 MHz–1 Hz) 안에서 자란 양극 저항은 화학(계면층) 형이고, 접촉 면적 형이 아니다** — 원전의 본문 배정은 지지되고,
> **초록의 "접촉 손실이 저항을 올린다" 는 원전 자신의 SI 가 지지하지 않는다**(⚠ 전제 `C ∝ 면적` 위; 같은 SI Fig. S3 의 무전류
> 기계 이완에서 `R₂·C₂` 가 ±5 % 로 보존되는 **부분 양성 대조**가 있다 — §5-3).
>
> ★★★ **첫 사이클 손실 예산 — 원전 숫자로는 CEI 의 두 정량 경로가 합쳐도 작다** (`[재현]`, §4-2):
> CEI 의 **패러데이 전하**(`[인쇄]` "≈1 % of the solid electrolyte") ≈0.016 mAh = 손실 0.437 mAh 의 **≈4 %**(양극 SE 기준) ·
> CEI 의 **옴 이동**(EIS 25 mV · DC 100 mV)이 방전 컷오프를 당기는 몫 `[도표]` **≲1–2 mAh g⁻¹(≲3 %)**.
> ⇒ **≳90 % 가 미배정**이고, 거기에 접촉 고립(`θ`) · 동역학(`η(i)`, `[인쇄]` 0.25 C 에서 66 · 0.5 C 에서 4 mAh g⁻¹) ·
> **상대극 고갈**이 함께 들어 있다.
>
> ★★★★ **17호 함정을 밟았고, 대조군이 같은 함정을 공유한다.** `[인쇄]` "Upon further discharge, **In is fully delithiated**" ·
> `R_SE/Anode` **2000 %** — 그리고 `[도표]` S2 에서 `C_SE/Anode` 가 방전 끝에 **≈1.8 mF → ≈20 µF(≈90 배) 붕괴** = 상대극이
> **2상 평탄을 떠난 전기화학 서명**. LTO 대조(Fig. S7)도 **≈10 mF → ≈0.1 mF** 로 똑같이 무너진다 — 두 상대극 모두
> **Li 없이 조립**돼 방전 끝 재고비가 `[재현]` **≈Q_ch/Q_dis ≈1.4** 로 구조적으로 바닥이다. LTO 대조는 **저항 배정**을 검사했지
> **용량 배정**을 검사하지 않았다.

---

# 0. 원문에 없어서 확인이 필요한 것 (공백)

| # | 공백 | 왜 중요한가 |
|---|---|---|
| **G1** | **부피 변화 % 가 없다.** `[인쇄]` "the unit cell volume of NCM shrinks" (refs 41, 48) · "especially high for nickel-rich" — 숫자 0. **틈의 폭도 재지 않았다** (`gap` 1 회, 치수 0) | "부피 수축 → 접촉 손실" 이 **식 단위로 한 번도 닫히지 않는다.** §4-2(e) 에서 `[도표]` 틈 폭으로 역산한 요구 `ΔV/V` 를 적는다 |
| **G2** | **NCM811 입자 크기·BET 가 없다** (BASF 공급, "characteristic spherical morphology" 뿐) | 곱 축퇴의 면적 인자, `C` 의 실면적 환산을 못 한다. `[도표]` Fig. 6a·e 단면 ≈6–9 µm |
| **G3** | **양극 지름이 인쇄되지 않는다** ("previously described procedure", ref 29). `[재현]` 35 kN ↔ 445 MPa ⇒ **0.787 cm² (∅10.0 mm)**, 0.1 C = 214 µA cm⁻² ↔ 8.4 mg AM ⇒ **0.785 cm²** — 두 경로가 맞는다 | 이것으로 D2(Ω·cm⁻²) 를 판정한다. **In 박은 ∅6 mm = 0.283 cm²** — 양극의 **0.36 배** |
| **G4** | **LTO 대조 셀의 용량·CE 가 인쇄되지 않는다.** EIS 만 있다 (SI Fig. 5·S6·S7) | 17호 함정 판정의 유일한 대조군인데 용량 축이 없다. `[도표]` 시간축으로 충전 ≈7.8 h · 방전 ≈4.5 h ⇒ **≈58 %** (In 셀 Fig. 2a ≈7.4 / ≈4.4 h ⇒ ≈59 %) — ⚠ EIS 휴지 제외 가정 |
| **G5** | **EIS 하한 1 Hz** — 방전 끝 저주파 호가 닫히지 않는다(Fig. 2b `[도표]` Z_Re 1100+ Ω 에서 끊김). `[인쇄]` DC 과전압 증가 ~100 mV ↔ EIS 추정 ~25 mV 차이를 "formation effects" 로 돌린다 | `[재현]` DC 100 mV / 0.168 mA = **595 Ω** ↔ EIS ΔR 140 Ω — **455 Ω 는 창 밖**(또는 D6 처럼 IR 이 아니다) |
| **G6** | **CPE(Q) → C 환산식이 없다** (S8 에서 α = 0.71 인쇄). Fig. 4·S2·S3·S6·S7 의 **오차 막대 정의가 없다** (`error` 0 회, `±` 0 회) | §5-3 의 `C` 비 판정이 환산식에 걸린다. 오차 막대는 적합 불확도로 추정되나 확인 불가 |
| **G7** | **SEM 은 "첫 충전 후(충전 상태)" 와 "50 사이클 후(방전 상태)" 뿐** — **첫 방전 후** 시편이 없다 | 틈이 **재리튬화에서 닫히는가**(가역 수축) **안 닫히는가**(비가역 접촉 손실)를 가르는 **바로 그 시편**이 빠졌다. `[인쇄]` "contact loss should only occur during the initial charge" 는 시험되지 않은 문장이다 |
| **G8** | `[인쇄]` "A total of **four cells** were used, and the shown data are **representative**" — **어느 그림이 어느 셀인지, 산포 0** | Fig. 1(176/124)과 Fig. 2a(`[도표]` ≈148/≈88 mAh g⁻¹ 상당)는 **다른 셀로 보인다**(§4-2(g)) |
| **G9** | **0.1 C 아래 율이 없다** (율 스윕 0.1/0.25/0.5/1 C, 전부 첫 사이클 뒤) | 3항 분해의 `η(i)` 를 `i → 0` 쪽에서 못 지운다 |
| **G10** | **XPS "≈1 % of the solid electrolyte" 의 기준(어느 시편 · 어느 SE · 정보 깊이)이 없다** | 계면층의 **전하량**으로 옮길 때 기준에 따라 손실의 ≈4 % ↔ ≈65 % 로 16 배 흔들린다(§4-2(c)) |
| **G11** | **S3 기계 이완 실험의 압력·전극 재질·시편 두께가 없다** ("house made press cell") | 이 편 유일한 무전류 대조가 운전 셀과 같은 조건인지 모른다 |
| **G12** | 0.6 V(In) · 1.55 V(LTO) 가정의 근거는 **리뷰(ref 16)와 1999 년 LTO 논문(ref 44)** | Q5 — 이 편 안에서 기준 전위를 잰 적은 없다 |

---

# 1. 서지·셀 사양

- **Koerver, R.; Aygün, I.; Leichtweiß, T.; Dietrich, C.; Zhang, W.; Binder, J. O.; Hartmann, P.; Zeier, W. G.; Janek, J.**
  "Capacity Fade in Solid-State Batteries: Interphase Formation and Chemomechanical Processes in Nickel-Rich Layered Oxide
  Cathodes and Lithium Thiophosphate Solid Electrolytes." *Chem. Mater.* **2017**, 29, 5574−5582.
  DOI 10.1021/acs.chemmater.7b00931. Article 9 쪽(참고문헌 48 편) + SI 7 쪽(그림 S1–S8, 표 0).
  접수 2017-03-07 · 수정 2017-06-08 · 게재 2017-06-09. JLU Giessen + KIT BELLA + **BASF SE** (`[인쇄]` BASF International
  Network for Electrochemistry and Batteries 재정 지원; "no competing financial interest").
- ⚠ SI 저자명은 **"Isabel Dursun"**(본문 "Aygün"), SI 제목은 "…oxide cathodes **in contact with** lithium thiophosphate…" 로 본문 제목과 다르다.

| 항목 | 값 | 출처 |
|---|---|---|
| CAM | **NCM811** (LiNi₀.₈Co₀.₁Mn₀.₁O₂), BASF, **코팅 없음**, 250 °C 진공 건조 | `[인쇄]` |
| SE | **β-Li₃PS₄** (Pmna), BASF. XPS 로 S 의 ≈96 at% 가 PS₄³⁻ | `[인쇄]` |
| 복합양극 | NCM:SE = **70:30 wt (47:53 vol)**, 마노 유발 15 분, **12 mg**, **무탄소** (`[인쇄]` "to purely focus on decomposition behavior of the solid electrolyte and avoid side reactions of carbon") | `[인쇄]` |
| 면적 적재 | **10.7 mg cm⁻²** (`[재현]` = AM 8.4 mg / 0.785 cm² ✓) | `[인쇄]` |
| 분리막 | β-Li₃PS₄ **60 mg ≈ 400 µm**; 단독 `R_SE,bulk` **463 Ω** (α = 0.71, SI Fig. S8) | `[인쇄]` |
| 음극 | **In 박 0.125 mm · ∅6 mm**, `[인쇄]` "approximately capacity = 7.7 mAh/cm²" — **Li 없이** 조립 | `[인쇄]` ⚠ D17 |
| 대조 음극 | **LTO 복합체** 30 mg (LTO:SE = 35:65 wt, 23:77 vol), 양극 대비 **5 % 용량 여유** | `[인쇄]` |
| 압력 | 제작 **35 kN ≈ 445 MPa** (다른 쪽 "446 MPa") · 운전 "approximately **70 MPa**" (다른 쪽 "**5 kN (64 MPa)**") | `[인쇄]` ⚠ D3 |
| 전기화학 | MACCOR, **25 °C**, 1C = 200 mAh g⁻¹; In 셀 **3.70–2.00 V**, LTO 셀 **1.00–2.75 V**; `[인쇄]` "The potential of the negative anode was **assumed** to be **0.6 V** vs Li/Li⁺ … for indium foil and **1.55 V** … for lithium titanate" | `[인쇄]` |
| 프로토콜 | 0.1 / 0.25 / 0.5 / 1 C 각 5 사이클 → 0.1 C 로 ≥30 사이클 (총 ≈50) | `[인쇄]` |
| EIS | SP300, **7 MHz – 1 Hz**, 10 mV, **1 h 충·방전마다 개방회로에서**, RelaxIS 적합; `(RQ)(RQ)(RQ)(RQ)` | `[인쇄]` |
| XPS | PHI5000 VersaProbe II, Al Kα, **−80 °C**, Ar 이송, 식각 없음, 스폿 100 × 1400 µm | `[인쇄]` |
| SEM | Zeiss Merlin, **사후 파편**, 미사이클 셀을 **같은 방식으로 분해**한 대조 포함 | `[인쇄]` |
| LIB 대조 | 90:5:5 (NCM:Super P:PVdF), ∅12 mm, CR2032, LP-type EC/EMC 1 M LiPF₆ 15 µL | `[인쇄]` |
| 셀 수 | **4 개**, "representative" | `[인쇄]` |

---

# 2. 절별 해체분석

## 2-1. 초록 · 서론

- `[인쇄]` 초록의 두 기구: "A **passivating cathode/electrolyte interphase layer** forms upon charging and leads to an
  irreversible first cycle capacity loss, corresponding to a decomposition of the sulfide electrolyte" · "**most of the
  interphase formation takes place in the first cycle, when charging to potentials above 3.8 V vs Li⁺/Li**" ·
  "In addition … the chemomechanical contraction of the active material upon delithiation causes **contact loss** between
  the solid electrolyte and active material particles, **further increasing the interfacial resistance and capacity loss**."
- `[인쇄]` 서론의 문제 설정: NCM 을 쓴 황화물 ASSB 는 "losing roughly **30%** of their initial capacity during discharge"
  (refs 30–32) — **"the origin … has not been elucidated yet"**.
- `[인쇄]` 접촉 손실 가설의 서론 판: "scanning electron microscopy reveals severe morphological changes … **suggesting**
  contact loss" · "mechanical contact loss due to irreversible shape changes of the NCM material is **expected** to have a
  significant contribution to the observed interfacial resistance." — **"expected"** 이다.

## 2-2. 전기화학 (Fig. 1, S1)

- `[인쇄]` 첫 사이클 **176 / 124 mAh g⁻¹, CE 70.5 %**; 0.25 C **66**, 0.5 C **4**, 1 C **0** mAh g⁻¹; 고율 뒤 0.1 C 로 돌아오면 회복;
  0.1 C 평균 CE **99.1 %**; "constant capacity loss of **1−2%** per charging cycle"; 50 사이클(율 시험 포함) 뒤 **81 mAh g⁻¹**.
- `[도표]` Fig. 1a: LIB 첫 사이클 CE **85.9 %**(그림에만 인쇄) — 충전 ≈211 · 방전 ≈181 mAh g⁻¹.
- `[도표]` **SSB 방전 곡선은 2.6 V 에서 끝난다**(Fig. 1a · S1a). 본문의 "2.7−4.3 V vs Li/Li⁺" 는 **LIB 창**이다(D1).
  `[재현]` 3.70 / 2.00 V vs In + 0.6 V = **4.30 / 2.60 V**.
- `[인쇄]` 1·2 사이클 사이 "increase in the overpotential (**∼100 mV**, Figure S1a) … indicating an increase in the **IR drop**".
  `[도표]` 그러나 S1a(정규화 곡선)에서 **충전만 ≈+100 mV 오르고 1·2 차 방전 곡선은 겹친다** — IR 증가라면 충전 ↑·방전 ↓ 가
  대칭이어야 한다(D6). 2 → 50 차는 충전 ≈+130 · 방전 ≈−150 mV 로 대칭이다.
- `[도표]` Fig. 1b: 사이클 21 에서 **방전 ≈112 > 충전 ≈99** mAh g⁻¹ — 고율 구간에서 못 꺼낸 Li 가 돌아온다.

## 2-3. in situ EIS (Fig. 2–4, S2, S5–S8)

- `[인쇄]` 개방회로 1 h 충·방전마다 측정. "The impedance response recorded between the **initial low OCV and OCV < 2.90 V
  could not be evaluated** properly due to strong scattering … and are therefore **omitted**" · "the applied potential differs
  significantly from the measured OCV, indicating formation effects … **We assume this activation process** to be the cause".
  `[도표]` Fig. 2a: 첫 충전 0 · 1 · 2 h 의 휴지에서 셀 OCV 가 **≈0.9 · ≈1.35 · ≈2.1 V** 로 떨어진다(통전 중 ≈3.05 V).
  LTO 셀(SI Fig. 5a)도 **≈0.4 · ≈0.75 · ≈1.4 V** 로 같은 모양이다.
- `[인쇄]` 네 호의 배정 (Fig. 3, OCV = 3.00 V): `R_SE,bulk` (C ≈ **40 pF**, "unequivocally") · `R_SE,gb` (C = **161 nF**) ·
  `R_SE,cathode` (C ≈ **1.1 µF**) · `R_SE,anode` (C ≈ **0.4 mF**). `[재현]` `f = 1/(2πRC)` 로 **1.9 kHz · 18 kHz · 11 Hz** —
  그림의 주파수 표지(1.6 kHz · 26.5 kHz · 9.7 Hz)와 맞는다.
- `[도표]` Fig. 3a: 중·저주파의 **위상은 최대 ≈−4°** — 435 Ω 이후의 ≈170 Ω 를 **세 RQ(9 파라미터)** 로 나누는 적합이다.
  `[인쇄]` 색 반원은 "guide-to-the-eye".
- `[인쇄]` `R_SE,bulk` 는 "virtually independent of the SOC"; `R_SE,gb` 는 첫 사이클에 **≈50 Ω** 증가 → "mechanical relaxation
  … consolidated at 35 kN (446 MPa) … **5 kN (64 MPa)**" 로 배정.
- `[인쇄]` **음극**: "Below an OCV of 3.2 V, corresponding to approximately 80% SOC … strong increase of the anode resistance of
  **up to 2000%** … recently been attributed to a **kinetic hindrance** using indium alloys (ref 29). **Upon further discharge, In is
  fully delithiated.** At low Li concentrations in the alloy, the interfacial resistance increases significantly" · 다음 충전에
  "≈40 Ω (**≈50 Ω·cm⁻²**)" 로 복귀.
- `[인쇄]` **양극**: 첫 충전 `R_SE,cathode` +**≈140 Ω (≈180 Ω·cm⁻²)** ⇒ "IR drop of **∼25 mV**"; "almost fully **irreversible**";
  둘째 충전은 "increases further, but … smaller … and is not fully translated to the subsequent charge"; LTO 셀도 "Similar
  impedance results … these irreversible interfacial impedance changes are indeed effects at the **cathode** side".
- `[인쇄]` ★ **배정 논거**: "the observed buildup of the resistance is in fact **not a function of the SOC** of the battery but
  rather a **function of the applied potential**. The strongest increase takes place between the OCV of **3.2 and 3.4 V**.
  Exceeding a certain potential appears to lead to irreversible changes … by oxidation of the solid electrolyte."
- `[인쇄]` 용량 연결: "The theoretical capacity … is not fully achieved as the **cutoff voltage is reached earlier due to the
  developed overpotential**. Additionally, the solid cathode composites are **not 100% dense**, and thus, not every NCM particle
  is ionically and electronically well addressed" — `θ` 형 문장, **값 0**.
- `[인쇄]` 방전 중 `R_SE,cathode` 변화: "may originate from lithium intercalation … **It is difficult to interpret** … This may be due
  to the simultaneous steep resistance increase of the low frequency semicircle" — **호가 겹친다는 것을 인쇄**.

## 2-4. XPS (Fig. 5, S4)

- `[인쇄]` 순수 SE ≈ 혼합물(48 h 접촉) ≈ 175 h 이완 혼합물 — **화학 반응 없음**. 첫 충전 후와 50 사이클 후: S 2p·P 2p 가
  높은 결합에너지 쪽으로 넓어진다 — 산화 S(**163.7 eV**, 그림 표지는 **163.5 eV** — D8, −S−S−/폴리설파이드) · 산화 P(P−Oₓ,
  그림 133.5 eV). S−Oₓ 는 없다.
- `[인쇄]` "quantification of the P 2p signal yields **7.2 atom %** of the species with the highest binding energy, which corresponds
  to **approximately 1% of the solid electrolyte** to have reacted" — **어느 시편인지, 무엇의 1 % 인지 없다**(G10).
- `[인쇄]` "**no steady decomposition** takes place. **Most of the interphase has formed after the first charging cycle**" ↔ 같은 절
  "The amount of oxidized sulfur and phosphorus species **increases** between one and 50 cycles" (D12).
- `[인쇄]` "The growing interfacial resistance … suggests a decreased lithium ion conductivity in the newly formed CEI, which
  **possibly** results in **partial insulation of NCM particles** due to the forming elemental sulfur species" — 계면층이 `θ`
  (고립) 쪽으로도 작용할 수 있다는 문장. **두 기구가 같은 결과(입자 고립)를 낼 수 있음을 원전이 인쇄한다.**

## 2-5. SEM (Fig. 6)

- `[인쇄]` 미사이클 셀(같은 방식으로 분해): "close and intimate contact" · 첫 충전(4.3 V) 후: "particles … are surrounded by a
  **spherical gap**" · 50 사이클(방전 상태) 후: "a **similar** morphology" · SE 면에 NCM 표면의 **음각 자국**.
- `[인쇄]` ★ 소거법: "After 50 charge and discharge cycles, a similar morphology was found (Figure 6e). **Thus, the observed capacity
  fading is likely originating from the ongoing decomposition of the SE.**"
- `[인쇄]` 분해 인공물 반론: "While mechanically induced contact loss is possible after disassembling, the **symmetrical shape** of
  electrolyte shells as well as the good contact of the particles in the uncycled cells **suggests otherwise**."
- `[인쇄]` 기구: "During delithiation, the unit cell volume of NCM shrinks (41, 48) … **We suspect** that the cathode interface
  formation **in combination with** the mechanical deflation provokes a contact loss … at the first charge" · "no additional solid
  electrolytes can fill the emerging voids" · "**While the contact loss should only occur during the initial charge**, corresponding
  well to the initial capacity drop, **the ongoing capacity fade can be attributed to the propagating interphase formation**."

## 2-6. 결론

- `[인쇄]` "an additional resistance is formed irreversibly at the positive electrode interface … **suspected** to be responsible
  for the low capacity retention in the first cycle. This resistance was found to originate from a highly resistive **interphase**"
  · "particles … lose contact … which suggests that those are **no longer fully electrochemically addressed**" · "the observed
  capacity loss during the first cycle is **a combination** of changes in the chemical composition at the interface (oxidation)
  **as well as** contraction of the NCM particles".

---

# 3. 그림 — 14 장 전부 직접 봤다 (본문 6 + SI 8)

크로퍼(`wiki/tools/extract_figures.py`)가 본문 그림 6 장 + SI 그림 8 장을 **전부** 잡았다. Fig. 6 은 추가로 PDF 원본 이미지
(2000×2095 px)를 뽑아 틈 폭을 픽셀로 쟀다. **안 본 그림 0 장.**

## Fig. 1 — 첫·둘째·50 차 곡선 + 율·수명 `[도표]`
(a) 축은 **"V vs Li/Li⁺"(환산 축)**. SSB 1/2/50 차 방전 끝 ≈124 / ≈120 / ≈80, **끝 전압 2.6 V**; LIB 첫 충전 ≈211, 방전 ≈181,
CE 85.9 %(그림에만). ★ `[도표]` 픽셀 판독: **SSB 첫 충전은 Q ≈10 mAh g⁻¹ 에서 ≈3.72 V 로 LIB 충전(≈3.78 V)보다 ≈60 mV
낮고**, Q ≈40–60 에서 교차해 Q = 150 에서 ≈+100 mV 위로 간다(§5-4). 방전 무릎: Q = 100 → 3.50 · 110 → 3.36 · 116 → 3.16 ·
120 → 2.90 · 123 → 2.65 V. (b) 1–5 사이클 방전 ≈124 → ≈114, 0.25 C ≈66, 0.5 C ≈3, 1 C ≈0, 사이클 21 방전 ≈112, 50 차 ≈80.

## Fig. 2 — 첫 사이클 곡선과 휴지별 Nyquist `[도표]`
(a) **축 "OCV vs Li⁺/InLi"(원 축)** — 같은 편 안에서 Fig. 1 과 **다른 기준의 축**이다. 첫 충전 0–2 h 휴지 OCV ≈0.9 / ≈1.35 / ≈2.1 V;
충전 ≈7.4 h · 방전 ≈4.4 h. (b) 방전: OCV 3.6 → 2.9 V 로 저주파(3.4 Hz) 호가 **Z_Re ≈800 → ≈1150 Ω** 으로 커지고 닫히지 않는다.
(c) 충전: 1.6 kHz 호가 자란다. 40 Ω 오프셋 적층.

## Fig. 3 — 대표 적합 (OCV 3.00 V, 충전) `[도표]`
|Z| 1 Hz ≈610 Ω, 위상 **최대 ≈−4°**(1 kHz–100 kHz), 고주파에서만 −32°. Nyquist 분할 `[도표]`: bulk ≈435 · gb ≈55 · cathode ≈75 ·
anode ≈37 Ω. bulk 반원은 데이터가 ≈300 Ω 부터라 **외삽**이다(inset).

## Fig. 4 — 네 저항 vs OCV, 1·2 사이클 ★ `[도표]`
`R_SE/Cathode`: 첫 충전 3.00 → 3.16 → 3.25 → 3.35 → 3.46 → 3.53 V 에서 **≈86 → 72 → 105 → 207 → 253 → 257 Ω**; 첫 방전 **≈227 →
223 → 242 → 268 → ≈340–375**; 둘째 충전 **≈207 → 205 → 205 → 233 → 302 → ≈310**; 둘째 방전 **≈240 → 245 → 272 → 328 → 385 → ≈410–455**.
`R_SE/Anode`: 방전 끝마다 ≈25–35 → **≈590**(1 차) · **≈780**(2 차). `R_SE,bulk` 첫 충전 **≈448 → ≈485**(+8 %). `R_SE,gb` 첫 충전
**≈37 → ≈85**. 그림의 "ΔR = 140 Ω" 막대, "a) irreversible · b) reversible" 화살표. 오차 막대는 방전 끝 점에만 크다(정의 없음, G6).
★ **둘째 충전에도 같은 전위창(3.25–3.45 V)에서 `R` 이 ≈+100 Ω 오른다** — 첫 충전과 같은 자리의 반복이다.

## Fig. 5 — XPS S 2p · P 2p `[도표]`
산화 S 성분(적색) 면적이 첫 충전 ↔ 50 사이클에서 **눈으로 ≈2 배** 커진다; 산화 P(녹색) 도 커진다.

## Fig. 6 — SEM ★ `[도표]`
(a,b) 미사이클 — 입자 ∅ ≈8 µm 단면, SE 와 맞붙음. (c,d) 첫 충전 후 — 입자 둘레 어두운 띠. **원본 픽셀 계측**: 0.5 µm 막대 =
120 px(1 px ≈ 4.2 nm), 틈 띠의 반치폭 **≈11–50 px(중앙 30 px) ≈ 0.05–0.2 µm (중앙 ≈0.12 µm)** — ⚠ 경사 파단면·그림자 포함,
투영 폭이다. (e,f) 50 사이클 방전 상태 — 입자 ∅ ≈6–7 µm 단면, 둘레 틈이 선명.

## Fig. S1 — 정규화 곡선 · 평균 전압 `[도표]`
(a) 정규화 0.5 에서 충전 1/2/50 차 **≈3.77 / ≈3.87 / ≈4.0 V**, 방전 1/2 차 **≈3.65 (겹침)**, 50 차 ≈3.5 V — **1 → 2 차는 충전만
이동**(D6). (b) 평균 충전/방전 전압: 0.5 C ≈4.28 / ≈2.78, **1 C ≈4.42 / ≈2.3 V — 컷오프 창(4.3/2.6) 밖**(용량 ≈0 이라 평균이
무의미; 인쇄된 곡선 그대로). 21 → 50 사이클 충전 ≈4.03 → 4.09, 방전 ≈3.58 → 3.50 V. 캡션 "2.14 A/cm²"(D4).

## Fig. S2 — 네 정전용량 vs OCV (In 셀) ★★ `[도표]`
`C_SE/Cathode`: 첫 충전 **≈1.1 (3.0 V) → ≈1.9 → 1.8 → 1.7 → 1.8 → 1.9 µF**; 첫 방전 **≈1.8 → 1.9 → 2.3 → 3.4 → 4.3 → ≈5.5 µF**;
둘째 충전 **≈2.4 → 2.1 (평탄)**; 둘째 방전 **≈2.2 → 2.5 µF**. `C_SE/Anode`: 첫 충전 **≈0.15 → 0.18 → 0.26 → 1.1 → 1.3 → 1.1 mF**;
첫 방전 **≈1.8 → 1.8 → 0.95 mF → 0.11 → 0.06 → 0.04 → ≈0.02 mF** (≈90 배 붕괴); 둘째 충전 ≈0.38 → ≈2 mF; 둘째 방전 ≈2 → ≈0.38 mF.
`C_SE,grain` ≈0.16–0.4 µF, `C_SE,bulk` ≈35 pF (평탄).

## Fig. S3 — 무전류 혼합물 EIS 이완 (≈165 h) `[도표]`
(a) Nyquist: as prepared **Z_Re ≈35 → ≈130 Ω**, 128 h **≈45 → ≈275 Ω**. (c) `R_total` **≈950 → ≈2250 Ω**, `R₃` ≈730 → ≈1750,
`R₂` ≈220 → ≈450, `R₁` ≈50. ⚠ **(a) 와 (c) 의 크기가 ≈8 배 다르다**(D10). (d) `C₂` ≈2.6 → ≈1.5 ×10⁻⁷ F, `C₃` ≈0.7 → ≈0.95 ×10⁻⁹ F.
시간축 단위 표지 잘림(h 로 추정).

## Fig. S4 — 혼합물 XPS, 0 ↔ 175 h — 변화 없음 `[도표]`

## Fig. S5 (캡션 "Figure 5") — LTO 셀 첫 사이클 + Nyquist `[도표]`
충전 ≈7.8 h · 방전 ≈4.5 h. 첫 충전 휴지 OCV ≈0.4 / ≈0.75 / ≈1.4 V (In 셀과 같은 모양). 방전 끝 저주파(2.1 Hz) 호 Z_Re ≈950 Ω 까지.

## Fig. S6 — LTO 셀 네 저항 ★ `[도표]`
`R_SE/Cathode`: 첫 충전 **≈65 → 60 → 64 → 83 → 98 → 104 → 110**; 첫 방전 **≈136 → 150 → 180 → 212 → 250 → ≈250**; 둘째 충전
**≈183 → 145 → 137 → 137 → 152 → 158 → 163**; 둘째 방전 **≈154 → 168 → 197 → 248 → 320 → ≈337 Ω**. `R_SE/Anode`(LTO) 방전 끝
**≈14 → ≈325 Ω** — ★ **In 셀의 "In 동역학 장애" 와 같은 모양이 LTO 에서도**. `R_SE,bulk` **≈310–375 Ω 로 SOC 따라 ±10 %** 움직인다(D14).

## Fig. S7 — LTO 셀 네 정전용량 ★ `[도표]`
`C_SE/Cathode` **≈2.2–2.8 µF 로 첫 충전·첫 방전·둘째 충전 내내 평탄**, 둘째 방전 끝만 ≈6 µF. `C_SE/Anode` 첫 방전
**≈10 mF → ≈0.1 mF**(≈100 배 붕괴), 둘째 방전 ≈8 → ≈0.18 mF.

## Fig. S8 — 분리막 단독 EIS `[인쇄]` R = 463 Ω, α = 0.71.

---

# 4. 검산과 새 계산

## 4-1. 원문 수치 검산

| 인쇄값 | 검산 `[재현]` | 판정 |
|---|---|---|
| 10.7 mg cm⁻² ↔ 12 mg × 70 % | 8.4 mg / 0.785 cm² = **10.70** | ✓ (양극 ∅10 mm 전제) |
| 214 µA cm⁻² = 0.1 C | 0.1 × 200 × 8.4 mg = 0.168 mA / 0.785 = **0.214** | ✓ |
| 35 kN ≈ 445 MPa | 35 kN / 0.785 cm² = **446 MPa** | ✓ (445 ↔ 446 표기차) |
| 5 kN = 64 MPa | **63.7 MPa** | ✓ — 그러나 방법 절 "approximately **70 MPa**" 와 다르다(D3) |
| ΔR 140 Ω ⇒ IR ∼25 mV | 140 × 0.168 mA = **23.5 mV** | ✓ |
| 40 Ω ≈ 50 Ω·cm⁻² · 140 Ω ≈ 180 Ω·cm⁻² | **R/A** = 51 · 178 ✓ — 그러나 면적 비저항은 **R·A = 31 · 110 Ω cm²** | ❌ **차원 역전(D2)** — 인쇄값이 **1.62 배 과대** |
| CE 70.5 % | 124/176 = **70.45 %** | ✓ |
| "1−2 % per cycle" ↔ CE 99.1 % · 81 mAh g⁻¹ | `[도표]` 사이클 21 → 50: (80/111)^(1/29) ⇒ **1.1 %/cycle**; 1 → 5: **≈2.1 %/cycle**; CE 99.1 % ⇒ 0.9 % | ⚠ 21–50 구간은 "1 %" 끝에만 걸린다(D5) |
| 분리막 σ (S8) | 0.04 cm / (463 Ω × 0.785 cm²) = **1.1 × 10⁻⁴ S cm⁻¹** | 인쇄 안 됨 — β-Li₃PS₄ 로 합당 |
| 호 주파수 | `f = 1/(2πRC)`: cathode 75 Ω·1.1 µF → **1.9 kHz**, gb 55 Ω·161 nF → **18 kHz**, anode 37 Ω·0.4 mF → **11 Hz**, bulk 435 Ω·40 pF → **9 MHz** | ✓ 그림 표지와 맞음; bulk 는 **측정 상한(7 MHz) 밖** — 외삽 |
| In 용량 7.7 mAh cm⁻² | In 0.0125 cm × 7.31 g cm⁻³ ⇒ In→LiIn **21.3 mAh cm⁻²** | ⚠ 인쇄값은 그 **36 %** — 기준 불명(D17) |

## 4-2. ★ 이 편에서 새로 계산한 것

**(a) 음극 기하와 재고.** In ∅6 mm = **0.283 cm² = 양극의 0.36 배** ⇒ 음극 면 전류밀도 **0.59 mA cm⁻²**(양극 면 0.214 의 2.8 배).
In 25.8 mg = 0.225 mmol, 첫 충전 1.478 mAh ⇒ **평균 Li/In ≈0.25**. 조립 때 Li 0 ⇒ **방전 끝 재고비 ≈ Q_ch/Q_dis = 176/124 ≈ 1.4**.
[[assb-li-in-reference-potential-window]] 의 평탄 조건 (5) "재고 / 이동 전하 ≥ 한 자릿수" 와 (6) "≲0.1 mA cm⁻²" 를 **둘 다
구조적으로 깬다**.

**(b) Ω·cm⁻² 정정.** 면적 비저항은 **31 Ω cm²(음극 기준 호, 양극 면적으로 환산)** · **110 Ω cm²(양극 계면 증분)**. 인쇄값은 R/A 다.

**(c) 계면층의 패러데이 몫.** β-Li₃PS₄ → ½P₂S₅ + 3/2 S + 3 Li⁺ + 3 e⁻ 를 완전 산화의 상한으로 두면(`[추론]` 식), "≈1 % of the SE" 가
- 양극 복합체 SE(3.6 mg) 기준: 2.0 × 10⁻⁷ mol × 3 e⁻ ⇒ **0.016 mAh = 첫 사이클 손실(52 × 8.4 mg = 0.437 mAh)의 3.7 %**;
- 셀 전체 SE(63.6 mg) 기준이라도: **0.28 mAh = 65 %**.
XPS 가 **양극 파편 표면(수 nm)** 을 본 것이므로 전자가 자연스러운 기준이다(G10). ⇒ **계면층이 전하를 먹어서 잃은 용량은 작다**;
계면층이 용량을 줄인다면 **분극(옴) 또는 고립(`θ`)** 을 통해서여야 한다.

**(d) 계면층의 옴 몫.** `[도표]` Fig. 1a 방전 무릎의 기울기: 컷오프(2.6 V) 부근 **Q 120 → 123 에서 2.90 → 2.65 V ⇒ ≈12 mAh g⁻¹ V⁻¹**.
방전 곡선을 ΔV 만큼 내리면 컷오프 교차가 **ΔV × 12** 만큼 당겨진다 ⇒ EIS 25 mV → **≈0.3 mAh g⁻¹**, DC 100 mV → **≈1.2 mAh g⁻¹**
(무릎 위쪽 기울기 ≈47 mAh g⁻¹ V⁻¹ 로 잡아도 **≤5 mAh g⁻¹**). ⇒ 52 의 **≲3 %(최대 ≲10 %)**.
**(c)+(d) ⇒ 원전이 정량한 CEI 경로 둘을 합쳐도 첫 사이클 손실의 ≲15 % 다.** 나머지 **≳85 %** 가 `θ`(접촉·절연 고립) ·
`η(i)`(`[인쇄]` 0.25 C 에서 이미 66 mAh g⁻¹) · 상대극 고갈 사이에 **미배정**으로 남는다.

**(e) 틈 폭 ↔ 부피 수축.** 구형 입자가 반경 `r` 에서 등방 수축하면 틈 `δ = r[1 − (1 − ΔV/V)^{1/3}] ≈ r·ΔV/(3V)`.
`[도표]` δ ≈ 0.05–0.2 µm (중앙 ≈0.12), r ≈ 3–4.5 µm ⇒ **요구 ΔV/V ≈ 3δ/r ≈ 3–20 % (중앙 ≈8–10 %)**.
**이 편은 NCM811 의 ΔV/V 를 인쇄하지 않으므로(G1) 이 식을 닫을 수 없다** — 닫으려면 ref 41·48 의 값이 필요하다. ⚠ δ 는 경사
파단면의 투영이고 그림자를 포함한다. 그리고 **방전 상태(50 사이클)에서도 틈이 있다는 것**은 두 해석과 다 맞는다:
비가역 접촉 손실 ∨ **첫 사이클 손실로 양극이 완전히 재리튬화되지 못해(Δx ≈ 52/275 ≈0.19) 수축된 채 남은 것**(`[추론]`).
후자라면 **틈은 용량 손실의 원인이 아니라 결과**다 — G7(첫 방전 후 SEM 부재)이 이것을 가를 시편이다.

**(f) 곱 축퇴 처방 1단계 — 연속 곡선** (§5-3 표의 근거). 면적 가설 `R ∝ 1/A, C ∝ A` 이면 `C` 비 = `R` 비의 역수, 동역학
가설이면 `C` 비 = 1.

| 셀 · 구간 | `R_SE/Cathode` 비 | 면적 예측 `C` 비 | 관측 `C` 비 `[도표]` | 판정 |
|---|---|---|---|---|
| In · 첫 충전 3.25 → 3.53 V | 105 → 257 = **×2.45** | ×0.41 | 1.8 → 1.9 = **×1.05** | 동역학 끝 |
| In · 첫 충전 전체 3.00 → 3.53 V | 86 → 257 = ×3.0 | ×0.33 | 1.1 → 1.9 = ×1.7 | 면적과 **반대 방향** |
| In · 둘째 충전 | 205 → 310 = **×1.5** | ×0.66 | 2.1 → 2.1 = **×1.0** | 동역학 끝 |
| In · 첫 방전 끝 | 227 → ≈375 = ×1.65 | ×0.61 | 1.8 → 5.5 = ×3.0 | ⚠ **호 혼합** — 같은 구간 `C_anode` 가 ≈20 µF 까지 떨어져 두 호의 주파수 비가 ≈6 배로 좁혀진다 (`[재현]` 590 Ω·20 µF → 13 Hz ↔ 375 Ω·5.5 µF → 77 Hz) |
| LTO · 첫 충전 | 65 → 110 = **×1.7** | ×0.59 | ≈2.5 → 2.6 = **×1.0** | 동역학 끝 |
| LTO · 첫 방전 | 136 → 250 = **×1.8** | ×0.54 | 2.3 → 2.2 = **×0.96** | 동역학 끝 |
| **양성 대조** — S3 무전류 기계 이완, (`R₂`,`C₂`) | ≈280 → ≈450 = ×1.6 (t ≈5 h → 끝) | ×0.62 | ≈2.3 → 1.5 ×10⁻⁷ = **×0.65** | **면적 끝** (`R₂·C₂` 6.4 → 6.8 ×10⁻⁵ s, +5 %) |
| 〃 (`R₃`,`C₃`) | 730 → 1750 = ×2.4 | ×0.42 | 0.7 → 0.95 ×10⁻⁹ = ×1.35 | 동역학 끝 |

**(g) Fig. 1 셀 ≠ Fig. 2 셀.** `[도표]` Fig. 2a 충전 ≈7.4 h · 방전 ≈4.4 h × 0.1 C(20 mAh g⁻¹ h⁻¹) ⇒ **≈148 / ≈88 mAh g⁻¹**
(⚠ EIS 휴지가 시간축에서 빠졌다는 가정). Fig. 1 의 176 / 124 와 **충전 −16 %, 방전 −29 %**. "representative" 의 폭이다(G8).

**(h) 3-b 물리 상한** (§5-3). `C_SE/Cathode` ≈1.8–2.6 µF ⇒ 기하 면적당 **2.3–3.3 µF cm⁻²**; `[도표]` 입자 ∅6–9 µm 와 ρ ≈4.75 g cm⁻³
(`[추론]` 가정)로 실면적 **≈12–18 cm²** ⇒ **≈0.10–0.15 µF cm⁻² = 이중층(10 µF cm⁻²)의 ≈1–2 %** — **상한 안(통과)**.
`C_SE/Anode` ≈0.15–1.8 mF / 0.283 cm² ⇒ **0.5–6.4 mF cm⁻² = 이중층의 50–640 배** — **상한 밖(실패)**. LTO 는 ≈0.7–10 mF.

---

# 5. 우리 축에서의 판정

## 5-1. ★★★★ 접촉 손실 vs 계면층 — 가르는 관측과 배정만 한 자리

### (a) 관측 — 무엇을 재서 어느 쪽을 지지하는가

| # | 관측 | 무엇을 보나 | 지지 | 가르는가 |
|---|---|---|---|---|
| O1 | XPS S 2p·P 2p 산화종 (첫 충전 · 50 사이클), 무전류 대조 2 개 | **화학** | 계면층 **존재** | ❌ 접촉에 대해 말이 없다 |
| O2 | 사후 SEM 틈·음각 (첫 충전 · 50 사이클), 미사이클 분해 대조 | **형태** | 접촉 손실 **존재** | ❌ 계면층에 대해 말이 없다; 틈이 원인인지 결과인지(§4-2e) 모른다 |
| O3 | `R_SE/Cathode(OCV)` 첫 충전 +140 Ω, 3.2–3.4 V 에 집중 | 양극 호 크기 | **둘 다** 예측한다 | ❌ "SOC 가 아니라 전위의 함수" 논거는 **첫 충전에서 SOC 와 전위가 단조 동행**해 구별 불가 `[추론]` |
| O4 | LTO 상대극 교체 | 음극 ↔ 양극 배정 | 증가가 **양극 쪽** | ❌ 기구는 안 가른다 (전극만 가른다) |
| **O5** | ★ `C_SE/Cathode(OCV)` (SI S2 · S7) — **원전은 이 조합을 만들지 않는다** | 면적 대리 | **계면층(동역학) 형** — `C` 평탄 | ✅ **EIS 창 안의 `R` 증가에 한해** (전제 `C ∝ 면적`) |
| **O6** | ★ S3 무전류 기계 이완의 `R₂·C₂` 보존 | 전제의 양성 대조 | 기계적 과정에서 **면적 서명이 실제로 나온다** | ⚠ **부분** — `R₃·C₃` 는 안 나오고, 호의 배정·셀 조건 미상 |

### (b) 배정 — 가르는 관측 없이 한쪽으로 놓은 자리

| # | 배정 | 근거 | 우리 판정 |
|---|---|---|---|
| A1 | 첫 사이클 손실 52 mAh g⁻¹ = **"combination"** | O1 + O2 + O3 병치 | **분할 0**. `[재현]` 원전이 정량한 CEI 경로는 ≲15 % (§4-2c·d) |
| A2 | 이후 감쇠(124 → 81) = **계면층 성장** | SEM 1 ↔ 50 "similar" (소거법) | ⚠ 같은 편이 "no steady decomposition · most formed after first charge" 라 적는다 — **느린 성장으로 30 % 추가 감쇠를 돌리면서 수량 0** (D12) |
| A3 | 접촉 손실은 **첫 충전에서만** | 서술 | 시험 0 — 첫 방전 후 SEM 없음(G7). ★ 둘째 충전에서도 **같은 전위창에서 `R` 이 +100 Ω 오른다**(Fig. 4) |
| A4 | **초록**: 접촉 손실이 계면 저항을 **더 올린다** | 없음 (본문은 CEI) | ❌ **본문·결론과 모순**(D11), O5 와도 모순 |
| A5 | 저주파 호 = **음극(In)**, 증가 = **In 동역학 장애**(ref 29) | 선행 문헌 | ⚠ **LTO 셀에서도 같은 모양**(S6: ≈14 → ≈325 Ω) — "In 고유" 가 아니다. 두 상대극 모두 방전 끝에 **평탄 이탈**(§5-4) |
| A6 | 과전압 → 이른 컷오프 → 저 CE | 서술 | `[재현]` ≲1–2 mAh g⁻¹ (§4-2d) — **크기가 안 맞는다** |
| A7 | `R_SE,gb` +50 Ω = 기계 이완(446 → 64 MPa) | 서술 | ⚠ 첫 충전에서 `R_gb` 증가가 **`R_cathode` 급등과 같은 전위창(3.25–3.5 V)** 에 있다 `[도표]`. S3 이완은 첫 ≈8 h 에 `R₂` 를 ≈+30–40 % 올리므로 **양립은 한다** — 그러나 가르지는 않는다 |

### (c) 식 단위 요약

- **부피 변화**: 원전 0 % 표기. 우리: `δ ≈ r·ΔV/(3V)` ⇒ `[도표]` δ 로 역산한 요구 ΔV/V ≈3–20 % (G1 로 대조 불가).
- **계면층 두께**: 원전 0 nm 표기. 대신 `[인쇄]` "≈1 % of SE" ⇒ 전하 ≈0.016 mAh(양극 SE 기준).
- **임피던스 성분**: `ΔR_cathode` = +140 Ω(`[재현]` 110 Ω cm², 23.5 mV) · `C_cathode` 불변(×1.0–1.05) ⇒ `τ = RC` ×2.4–2.6.

⇒ **판정**: **원전은 두 기구를 가르지 않는다.** 두 채널이 **존재**를 각각 보이고, 몫은 **시간 구간(첫 사이클 ↔ 이후)** 으로 배정된다.
**가르는 입력(`R` 과 `C` 의 동시 궤적)은 SI 에 있고 원전은 조합하지 않는다** — 16호 · 18호와 같은 모양("두 값을 인쇄하고 조합을
안 만든다"), 다만 **이번에는 상태축 위 연속 곡선**이다.

## 5-2. Q1 — 접촉 손실은 측정량인가, 이름표인가 · `θ(N)`

- **이름표 + 정성 영상**이다. `contact loss` 본문 7 회, 치수·분율·면적 **0**. SEM 은 **N = 0(미사이클) · 1(충전) · 50(방전)** 세 상태의
  **존재/부재**이고, **다른 셀**의 **파편**이다.
- `[인쇄]` "not 100% dense … not every NCM particle is ionically and electronically well addressed" — `θ` 의 **문장**, 값 0.
- ★ **`θ(N)` 을 측정량으로 준 편: 여전히 0 / 23.** 그러나 **대리량으로는 첫 입력이 있다** — `C_SE/Cathode` 를 면적 대리로 읽으면
  (전제부) `[도표]` **N = 1 → 2 동안 In 셀 ×1.0–1.3(1.8 → 2.1–2.4 µF), LTO 셀 ×0.9–1.0(2.5 → 2.2 µF)** ⇒ **EIS 창이 보는 접촉 면적은
  두 사이클 동안 줄지 않았다**. 이것은 **우리 조합**이고 원전 문장이 아니다. 그리고 SEM 의 "틈" 과 **긴장 관계**다 — (i) 전제
  `C ∝ 면적` 이 이 복합체에서 안 선다(18·19호 선례), (ii) 틈이 **분해·감압 뒤** 생겼다(원전은 "symmetrical shape" 로 반박, 정량 0),
  (iii) 틈이 난 면이 원래 전류를 나르지 않았다 — 셋 중 무엇인지 이 편은 못 가른다.
- **칸 이동 없음.** 반 칸을 주지 않은 이유: 측정량 0, 대리량은 전제 위, 원전이 만든 양이 아니다.

## 5-3. ★★★ 곱 축퇴 처방 — 일곱 번째 적용

| 처방 단계 | 필요한 입력 | 23호 | 판정 |
|---|---|---|---|
| **1단계** (16호) | `R` 과 `C` 를 같이 | ★ **Fig. 4 + S2 (In) · S6 + S7 (LTO)** — **두 셀 × 네 구간의 연속 곡선** | ✅ **계보 첫 상태축 위 완전 적용** — 여섯 비교 중 다섯이 **동역학 끝**(§4-2f), 하나는 호 혼합으로 판정 불가 |
| **2단계** (18호) | + 면적을 아는 대조군 | 면적 대조 없음. 대신 ★ **S3 무전류 기계 이완**(XPS 로 화학 변화 0 확인 — S4) = **"면적만 변하는 과정" 의 대조** | ⚠ **부분 — 계보 첫 전제 양성 대조**: `R₂·C₂` 보존(+5 %) = 면적 서명이 **실제로 나온다**. 단 `R₃·C₃` 는 아니고, 호의 정체·셀 조건 미상(G11), 판 a↔c 크기 불일치(D10) |
| **3단계-a** (19호) | `Ea` | 25 °C 한 점 | ❌ |
| **3단계-b** (19호) | `C` 물리 상한 | 양극 호 **≈1–2 % of DL(실면적)** · 기하 2.3–3.3 µF cm⁻² | ✅ **양극 호 통과** — 19·20·21호의 연속 실패와 다르다. ⚠ 실면적은 입자 크기 가정 위 |
| 〃 | 〃 | **음극 호 0.5–6.4 mF cm⁻² = DL 의 50–640 배** | ❌ **"R_SE/Anode" 는 이중층·전하이동 호가 아니다** — 합금의 화학 용량(`[추론]`). 음극 호가 상한을 넘은 **네 번째 편** |
| **4단계** (20호) | 시간 영역에도 같은 검사 | DC 과전압 ~100 mV ↔ EIS 25 mV | ⚠ **불일치 4 배** — 그리고 S1a 에서 **충전만** 오른다(D6) ⇒ DC 쪽 100 mV 는 옴이 아니라 **창 이동**(`[추론]`: 첫 사이클 손실로 양극이 덜 리튬화된 채 둘째 충전을 시작) |

- ★★★ **결과**: **EIS 창 안의 양극 저항 증가는 화학 형**이다 — 원전의 **본문 배정(CEI)이 원전의 SI 로 지지된다**. 동시에
  **초록의 "접촉 손실이 저항을 올린다" 는 지지되지 않는다.** 16호(한쪽 끝을 **골랐다**)·18호(`or` 를 **남겼다**)와 달리 23호는
  **두 기구를 다 주장했고 SI 가 한쪽만 남긴다.**
- ★★ **처방 표에 붙는 것 둘** (개념 페이지 [[assb-lampe-contact-product-degeneracy]]):
  1. **"같은 셀의 무전류 이완 = 전제 양성 대조"** — 화학 변화 0 을 XPS 로 확인한 기계 이완에서 `R·C` 가 보존되는지를 **먼저** 본다.
     보존되면 그 호에 대해서는 `C ∝ 면적` 이 이 복합체에서 작동한다는 뜻이다. 23호는 **한 호에서 통과, 한 호에서 실패**다.
  2. **"상대극 교체 대조는 두 상대극이 같은 결함(무 Li 조립)을 공유하지 않을 때만 대조다"** (§5-4).
- ⚠ **이 결론이 곱 축퇴를 푼 것은 아니다.** 푼 것은 **`R_cathode` 의 변화분**이고, **용량**의 분할(`θ` ↔ `η` ↔ `Q_material` ↔
  상대극)은 **여전히 0** 이다. `R_cathode` 가 동역학 형이라는 것은 **"접촉 손실이 EIS 에 안 보인다"** 이지 **"접촉 손실이 용량에
  없다"** 가 아니다 — 완전히 고립된 입자는 호에서 **빠질** 뿐 `R`·`C` 를 더 바꾸지 않을 수 있다(`[추론]`: 고립 분율 `f` 면
  `R/(1−f)`, `C(1−f)` 로 면적 서명을 내야 하므로, `C` 평탄은 **첫 충전 중 새 고립이 ≲10–20 %** 라는 약한 상한이다).

## 5-4. 17호 함정 · Q5 기준 전위

### (a) 17호 함정 — 겉보기 양극 손실이 사실은 상대극인가

- **상대극**: 순수 In 박 **∅6 mm**(양극의 0.36 배), **Li 없이** 조립. 기준극 **없음**. 대조: LTO 복합체, **역시 Li 없이**, 여유 **5 %**.
- `[인쇄]` "Upon further discharge, **In is fully delithiated**" · `R_SE/Anode` "**up to 2000%**". `[도표]` S2 `C_SE/Anode` 첫 방전 끝
  **≈1.8 mF → ≈20 µF**, S7(LTO) **≈10 → ≈0.1 mF**. `[추론]` **2상 평탄(In+LiIn · Li₄/Li₇Ti₅O₁₂)의 화학 용량은 크고, 단상역으로
  나가면 두 자릿수 떨어진다** — 이 붕괴는 **상대극이 평탄을 떠났다는 2전극 EIS 서명**이다. 그 순간부터 셀 전압의 하강은
  **상대극 전위의 상승**을 포함한다 ⇒ **방전 컷오프(2.00 V)의 일부를 상대극이 끊는다.**
- `[재현]` 이것은 설계에서 필연이다: Li 없는 상대극의 방전 끝 재고비는 **≈Q_ch/Q_dis ≈1.4**(평탄 조건 (5) 가 요구하는 ≥10 의 1/7).
  21호가 인쇄한 문장 — *"the potential of the indium CE cannot be assumed to stay invariant … would depend on the overall loss of
  cyclable lithium"* — 의 **원인 쪽 사례**다.
- **LTO 대조의 한계**: `[인쇄]` 저자는 LTO 로 **"irreversible interfacial impedance changes are indeed effects at the cathode side"** 를
  보였다 — **저항**의 전극 배정이다. **용량**은 LTO 셀에서도 `[도표]` ≈58 % 로 비슷하지만, **두 상대극이 같은 결함(무 Li · 방전 끝
  평탄 이탈)을 공유**하므로 이 일치는 "In 이 아니라 양극" 의 증거가 아니라 **"무 Li 상대극 두 종" 의 일치**다.
- ⇒ **판정: 주 주장(첫 사이클 손실 = 양극의 CEI + 접촉)은 17호 함정에 노출됐고, 대조군이 함정을 공유한다.** 22호("주 주장은
  면제, CE 는 노출")보다 **나쁘고**, 20호("3전극으로 명시적으로 피함")의 반대편이다. ⚠ 몫은 모른다 — 상대극이 끊은 방전 용량이
  몇 mAh g⁻¹ 인지는 3전극 없이 안 나온다.

### (b) Q5 — 기준 전위를 재는가, 가정하는가: 여덟 번째 형태

- **낱말**: `assum*` 본문 **4 회**, 그중 기준 전위 **1 회**(`[인쇄]` "was **assumed** to be **0.6 V** … and **1.55 V** vs Li/Li⁺ for
  lithium titanate", refs 16·44) — **계보에서 가정을 가장 또렷이 적은 편 중 하나**. `0.62` **0 회** · `0.6 V` **2 회**(그중 하나는
  "initial OCV (approximately 0.6 V)" = **셀 개방 전압** — 같은 숫자 두 뜻, D15) · `1.55` **1 회**.
- **그림 축**: Fig. 1a · S1 = **"V vs Li/Li⁺"(환산 축)**, Fig. 2a · 4 · S2 = **"OCV vs Li⁺/InLi"(원 축)**, S5–S7 = "vs Li⁺/Li₄Ti₅O₁₂".
  한 편 안에 **두 기준의 축**이 섞이고, 원 축의 이름이 **"InLi"** — 조립 직후의 **순수 In** 에도 같은 이름이 붙는다.
- ★★★ **가정이 깨지는 곳이 셋이고, 셋 다 데이터에 남아 있다.**
  1. **첫 충전 앞 ≈3 h**: `[도표]` 휴지 OCV **≈0.9 → ≈1.35 → ≈2.1 V**(In) · **≈0.4 → 0.75 → 1.4 V**(LTO). `[인쇄]` "initial OCV ≈0.6 V" 가
     In/InLi 0.6 V 와 양립하려면 양극이 **≈1.2 V vs Li** 여야 한다 — 층상 산화물로 불가능한 값(`[추론]`) ⇒ **조립 직후 상대극은
     0.6 V 짝이 아니다**(20호의 비리튬화 In 1.77–1.93 V 와 같은 현상). 저자는 이 구간을 `[인쇄]` "activation" 이라 부르고
     **EIS 를 잘라 냈다**.
  2. **첫 충전 앞 ≈10–30 mAh g⁻¹**: `[도표]` 환산 축의 SSB 충전 곡선이 **LIB 충전보다 ≈60 mV(Q ≈10) · ≈16 mV(Q ≈30) 낮다**.
     `[재현]` 분리막만의 옴 강하가 463 Ω × 0.168 mA = **78 mV** 이므로, 두 셀의 양극 OCP 가 같다면 SSB 곡선은 **≥ +78 mV 위**여야 한다
     ⇒ 그 구간에서 **상대극은 가정보다 ≥ ≈0.1 V 높다**(`[재현]` LIB 분극 ≤30 mV 가정 시 **E_In ≥ ≈0.71 V**). Q ≈150 에서는 SSB 가
     ≈+100 mV 위 — **평탄에 들어간 뒤에만 가정이 맞는다.**
  3. **방전 끝**: `C_SE/Anode` 두 자릿수 붕괴(§5-4a) — 저자는 `[인쇄]` "kinetic hindrance" 로 **음극 동역학에 배정**한다.
- ⇒ **Q5 여덟 번째 형태 = "가정을 낱말로 명시하고, 가정이 깨지는 구간을 '활성화' · '음극 동역학 장애' 로 이름 붙여 잘라 내거나
  음극 저항에 배정했다."** 계보: 안 쟀다(4호) → 설치·미검증(16호) → 실측(17호) → 제3물질로 가정(18호) → 차분으로 소거(19호) →
  가정하되 깨지는 모습을 남김(20호) → 교정 이식(21호) → 가정이 대조군 전압창을 정함(22호) → **명시하고 깨지는 곳을 이름표로
  덮음(23호)**.
- ★ **계보 사실 하나**: 18호가 `[인쇄]` "**Assuming** 1.55 V" 로 쓴 R-LTO 기준값은 **이 편(2017)이 이미 가정한 값**이다 — 근거는 ref 44
  (Zaghib 1999, 액체 전해질 LTO). 즉 1.55 V 가정은 Ikezawa 2020 보다 **최소 3 년 앞서** 황화물 ASSB 에 들어와 있었다.
- **칸 이동 없음** — 기준 전위를 잰 값이 없다. 다만 **새 진단 하나**가 생겼다: **2전극 EIS 의 저주파 `C` 두 자릿수 붕괴 = 상대극
  평탄 이탈 서명** (기준극 없이 쓸 수 있다) → [[assb-li-in-reference-potential-window]] P13.

## 5-5. Q4 — 23/23 연속 0, 그리고 0 의 성질

`identif*` 본문 3 회(전부 XPS 상 동정·SEM 형태 식별) · `unique*` 0 · `uncertain*` 0 · `error` 0 · `±` 0 · `fit*` 본문 11 / SI 7.
**열여섯 번째 성질 = "채널 분담 + 시간 분할 배정"** — 두 기구에 **전용 채널**(XPS ↔ SEM)을 하나씩 주어 **공존**을 보이고,
**몫은 시간 구간**(첫 사이클은 "combination", 이후는 CEI)으로 나눈다. 두 기구를 **동시에** 볼 수 있는 유일한 채널(양극 호)은
"전위의 함수" 라는 논거로 한쪽에 배정되는데, 그 논거는 **첫 충전에서 SOC 와 전위가 단조 동행**해 판별력이 없다.
- 부수: **4-RQ 적합이 위상 ≤4° 의 스펙트럼 위에 있다**(Fig. 3) — 9 파라미터로 ≈170 Ω 을 나눈다. `[인쇄]` "to the best of our knowledge,
  assigned" · "guide-to-the-eye" · 방전 쪽 "It is difficult to interpret" — **비유일성을 문장 셋으로 인정하고 수치화하지 않는다.**
- 부수: **초록 ↔ 결론의 배정이 다르다**(A4, D11) — 같은 `ΔR` 이 초록에서는 두 기구, 결론에서는 한 기구다.
- 계보: 16호 "밟고 지나감" · 17호 "인쇄로 사양" · 18호 "갈림을 인쇄하고 안 가름" · 19호 "어휘 없이 기하로 물음" · 20호 "작도" ·
  21호 "값의 정확도를 배정의 유일성으로 읽음" · 22호 "측정이 분할을 대신했고 원인은 병치" · **23호 "채널 분담 + 시간 분할 배정"**.

## 5-6. ★★★★ 인용 대질 — 후속 편들이 이 편에서 가져간 것

| 인용한 편 (ref) | 가져간 문장 | 원문 대조 | 판정 |
|---|---|---|---|
| **22호 Strauss 2018** (ref 9, 본문 **4 회** — 확인함) | ① "ASSB cathode composites consist of a mixture of CAM and SE" (8,9) ② "volume contraction during charging leads to a reduced electrical contact between the CAM particles and the SE" (9,18) ③ 코팅 없는 NCM → SE 산화 분해 → "insulating layer" (9) ④ "This layer increases the kinetic barrier … leading to overvoltage and causing low Coulombic efficiency" (9) | ① ✓ ② ✓ 원전 결론 문장과 같다(단 원전에서도 **SEM + 서술**뿐) ③ ✓ ④ ✓ 문장은 맞다 — 그러나 `[재현]` 원전 숫자로는 과전압 경로가 손실의 **≲3 %**(§4-2d) | **인용은 맞다.** 원전의 **약한 고리(④ 의 크기)를 그대로 물려받았다.** 그리고 NCM811 → **NCM622** 로 옮기면서 수축 크기 차이는 논하지 않는다 |
| **21호 Sedlmeier 2023** (ref 29, 2 회 — 확인함) | ① "a pure indium foil with a capacity high enough to accommodate the entire lithium from a cathode" (29, 30) ② "high-frequency feature, which represents the **separator resistance**" (29, 36) | ① ✓ 인쇄된 7.7 mAh cm⁻² 기준 In 0.283 cm² = 2.18 mAh ≥ 양극 1.48 mAh (`[재현]` 1.47 배) ② ✓ `R_SE,bulk` + S8 분리막 단독 463 Ω | **맞다.** ⚠ ① 의 "high enough" 는 **용량** 얘기이고, 이 편은 **면적**이 양극의 0.36 배다 |
| **18호 Fukunishi 2023** ([23], 1 회 — 확인함) | "resistances related to the **space charge layer** formed at SE\|AM interface [23] can be significant" | ❌ **이 편에 `space charge` 0 회.** 이 편이 보인 것은 **산화 분해 계면층(CEI)** 이지 공간전하층이 아니다 | **기구 치환** — 화학 계면층을 공간전하층으로 옮겼다. 1호는 둘을 다른 ref(7 ↔ 8)로 **정확히 가른다** |
| **1호 Bielefeld 2019** (ref 7, 위키 digest 경유) | ① "contact loss **throughout the composite cathode** occurs because of volume change … as was exemplarily shown for NCM-811 and LPS" ② "vulnerable for chemical degradation and formation of passivating … interfacial layers upon charging" ③ 탄소 첨가제가 티오포스페이트와 **분해 반응을 보인다** (7, 23, 24) | ① ⚠ **"throughout" 은 과장** — 원전은 파편 SEM 몇 장 ② ✓ ③ ⚠ **원전은 탄소를 "피했다"**(`[인쇄]` "avoid side reactions of carbon") — 분해를 **보이지 않았다** | ① 강도 과장 · ③ **회피를 증명으로 인용** |
| **9호 Huo 2025** ([17], 위키 digest 경유) | "contact loss between NCM811 particles and sulfide SSE … led to **increased resistance** and decreased capacity" | 원전 **초록**과 같다 | ⚠ **원전에서 가장 덜 지지되는 문장**(A4)을 가져갔다 — 원전 본문·결론은 저항을 CEI 에 두고, SI `C` 궤적은 면적 형이 아니다 |
| 3호 Liu 2024 (ref 7) · 4호 Shi 2020 (ref 8) | 우리 digest 는 **후속 후보로만** 기록 — 인용 문장 미확인 | — | 확인 안 함 |

- ★ **숫자를 옮긴 편은 없다** — 가져간 것은 **전부 기구 문장**이다(8호식 숫자 오기는 없다). 문제는 다른 모양이다:
  **(i) 강도 과장**(1호 "throughout") · **(ii) 회피의 증명화**(1호 탄소) · **(iii) 기구 치환**(18호 공간전하) ·
  **(iv) 초록 채택**(9호 — 본문이 지지하지 않는 문장). 이 편 자체가 **"expected" · "suspect" · "suggests"** 로 쓴 접촉 손실이
  후속 편들에서 **평서문**이 된다.
- ⇒ **"접촉 손실의 실험 원전" 이라는 이름표는 반만 맞다**: **실험 원전은 맞다**(계보 최초의 SEM 틈 영상 + 미사이클 분해 대조).
  **정량 원전은 아니다** — 치수 0 · 분율 0 · 용량 몫 0 이고, 원전의 SI 는 **EIS 창 안에서 접촉 면적 변화를 보지 못한다.**

## 5-7. Q2 · Q3 · Q6 · Q7 · Q8

- **Q2 +0.5** — ★ **두 비-LAM 기구(계면층 ↔ 접촉)에 전용 독립 채널이 붙은 계보 첫 편**(XPS · SEM, 각각 무전류·미사이클 대조 포함)이고,
  **같은 지면이 양극 호의 `R`·`C` 를 두 셀 × 네 구간으로 인쇄해 `R` 변화분을 화학 형으로 가를 수 있게 한다**(§5-3, 전제 양성 대조 부분
  포함). **반 칸인 이유**: 가른 것은 **저항의 변화분**이지 **용량**이 아니고, 가른 주체는 **우리**(원전은 조합하지 않았다)이며, 전제 `C ∝ 면적`
  은 한 호에서만 양성 대조를 얻었다. 그리고 `LAM_PE`(구조 손실)를 가르는 채널은 **0**(XRD 없음).
- **Q3 칸 이동 없음(층 하나)** — fitted(4-RQ, 적합 불확도로 보이는 막대, 정의 없음) + measured-chemical(XPS 정량 한 줄) + measured-
  morphological 정성. **n = 4 를 인쇄하고 산포 0**("representative") — n 을 적은 계보 두 번째 편(21호 n = 3 ± 다음), 그러나 ± 없음.
  `[도표]` Fig. 1 ↔ Fig. 2 셀은 방전 용량이 **≈29 % 다르다**(§4-2g) — "representative" 의 폭.
- **Q6 칸 이동 없음** — 보고·통제: 제작 **445/446 MPa**, 운전 **70 ↔ 64 MPa**(D3). 스윕 0. ★ 기여 하나: `[인쇄]` "no additional solid
  electrolytes can fill the emerging voids" + S3 **무전류에서 복합체 저항이 ≈165 h 에 ≈2.2 배** — **압력이 일정해도 시간에 따라
  접촉이 변한다**(압력 미상, G11). 압력 축의 `θ(t)` 가 **무전류로** 존재한다는 첫 표본이다(정량은 판 불일치 D10 에 걸린다).
- **Q7 해당 없음** — In · LTO 음극. `plating` · `dead` 0.
- **Q8 칸 이동 없음** — NCM811 은 3호(Liu)·9호(Huo)에 이미 있다. 기여: **같은 CAM 의 LIB ↔ SSB 첫 사이클 곡선 쌍**(Fig. 1a) —
  §5-4b 의 기준 전위 검산이 이 쌍에서 나왔다.

---

# 6. Q1~Q8 판정 (채움표 23호 행의 근거)

| Q | 판정 | 요지 |
|---|---|---|
| **Q1 정량** | **칸 이동 없음** | 이름표 + 정성 SEM(N = 0/1/50, 다른 셀). 치수·분율 0. `θ(N)` 측정량 **0/23**; `C_SE/Cathode` 대리량으로 N = 1–2 불변(우리 조합, 전제부) |
| **Q2 독립관측** | **+0.5** | 두 기구에 전용 채널(XPS ↔ SEM) + 양극 호 `R`·`C` 연속 궤적(두 셀) ⇒ `R` 변화분 = 화학 형. 용량은 미분할 |
| **Q3 라벨층위** | 층 추가 | n = 4 인쇄, 산포 0; 오차 막대 정의 없음 |
| **Q4 유일성** | **0 / 23** | 열여섯 번째 성질 — "채널 분담 + 시간 분할 배정"; 위상 ≤4° 위 4-RQ, 비유일성을 문장 셋으로 인정 |
| **Q5 Li-In 기준** | 칸 이동 없음 | `assumed` 0.6 V · 1.55 V 명시; 여덟 번째 형태 = "깨지는 곳을 '활성화' · '음극 동역학' 으로 덮음"; `[재현]` 첫 충전 앞 ≥ ≈0.1 V 어긋남; 2전극 `C_anode` 붕괴 서명 |
| **Q6 압력** | 칸 이동 없음 | 보고·통제(445/446 · 70/64 MPa), 스윕 0; 무전류 시간 이완 ×2.2 |
| **Q7 dead Li** | 해당 없음 | In/LTO |
| **Q8 화학·OCP** | 칸 이동 없음 | NCM811(기존), LIB ↔ SSB 곡선 쌍 |

---

# 7. 우리 프로젝트와의 접점

1. ★★★★ **"접촉 손실 → 겉보기 `LAM_PE`" 의 실험 원전에 용량 몫이 없다.** 우리 닻 물음의 전제(접촉 손실이 용량을 줄여 `LAM_PE` 처럼
   보인다)는 이 편에서 **서술**로 태어났고 정량된 적이 없다. 우리가 이식판에서 접촉 손실을 모델에 넣을 때 **크기의 문헌 근거로 이 편을
   쓰면 안 된다** — 크기 근거는 22호(XRD 불활성 분율, 신품)가 유일하다.
2. ★★★ **`R`·`C` 동시 궤적은 우리가 바로 쓸 수 있는 분류기다.** 우리 합성 쪽(PyBaMM)에서 **접촉 면적 노브 ↔ 교환전류 노브**를 따로 돌려
   2전극 EIS 의 `(R, C)` 궤적을 만들면, 이 편의 S2/S7 모양(`C` 평탄)이 어느 쪽인지 **forward 로** 확인할 수 있다 — 전제 `C ∝ 면적` 의
   검증을 실험 대신 모델에서 먼저 한다.
3. ★★★ **무 Li 상대극 셀의 방전 끝은 상대극이 끊는다** — Li-In 을 "평탄 상대극" 으로 가정한 우리 §1 합성(5 → 3 파라미터 붕괴)은 **방전
   끝 구간에서 이 편의 셀에 맞지 않는다.** 이식판에서 **방전 끝 수 %** 를 적합 창에서 빼거나, 상대극 재고비를 입력으로 받아야 한다.
4. ★★ **2전극에서 상대극 평탄 이탈을 잡는 싼 진단**: 저주파 `C` 의 두 자릿수 붕괴(§5-4a). 기준극 없이 RPT EIS 로 된다.
5. **degradation-degeneracy 수치와 비교하지 않는다** — 이 편에는 OCV 적합이 없다.

---

# 8. 후속 후보

| 순위 | 문헌 (이 편의 ref) | 왜 | 축 |
|---|---|---|---|
| ★★★★ 1 | **Zhang, Weber, Weigand, Arlt, Manke, Schröder, Koerver, Leichtweiß, Hartmann, Zeier, Janek, *ACS Appl. Mater. Interfaces* 9, 17835−17845 (2017)** (ref **29**, 본문 **8 회**(범위 인용 포함) — 그중 핵심 넷: 셀 조립 절차 · 70:30 최적 조성 · EIS 배정 모델 · In "kinetic hindrance") | **이 편의 방법 원전** — 셀 기하(G3)·등가회로 배정·"In 동역학 장애"(A5)의 근거가 전부 여기로 간다. 22호 digest 가 이미 3순위로 지목 | Q1·Q2·Q5 |
| ★★★★ 2 | **Kondrakov, Schmidt, Xu, Geßwein, Mönig, Hartmann, Sommer, Brezesinski, Janek, *J. Phys. Chem. C* 121, 3286−3294 (2017)** (ref **41**) | **G1 — NCM811 부피 수축 % 의 원전.** §4-2(e) 의 `δ = r·ΔV/3V` 를 닫을 값. ⚠ 22호 digest 가 적은 Kondrakov *JPCC* 121, **24381** 과 **다른 논문**(같은 해·같은 권) | Q1 |
| ★★★ 3 | **Ishidzu, Oka, Nakamura, *Solid State Ionics* 288, 176−179 (2016)** (ref **48**) | 조성별 격자 부피 변화 ↔ 사이클 성능 — "Ni 많을수록 수축 큼" 의 근거 | Q1·Q8 |
| ★★★ 4 | **Zhang, Schröder, Arlt, Manke, Koerver, Pinedo, Weber, Sann, Zeier, Janek, *J. Mater. Chem. A* 5, 9929−9936 (2017)** (ref **40**, 본문 2 회: 서론 범위 인용 · "LiCoO₂ undergoes an overall expansion of the unit cell") | 운전 중 **압력 변화 감시** — 부피 변화를 셀 단위로 잰 같은 연구망 편. 22호 digest 2순위 | Q1·Q6 |
| ★★ 5 | **Jung, Oh, Nam, Park, *Isr. J. Chem.* 55, 472−485 (2015)** (ref **16**) | **In 0.6 V 가정의 인용 근거**(리뷰) — Q5 계보의 뿌리 한 가닥 | Q5 |
| ★★ 6 | **Zaghib, Simoneau, Armand, Gauthier, *J. Power Sources* 81−82, 300−305 (1999)** (ref **44**) | **LTO 1.55 V 가정의 근거** — 18호 R-LTO "Assuming 1.55 V" 의 더 이른 뿌리 | Q5 |
| ★ 7 | **Auvergniot, Cassel, Foix, Viallet, Seznec, Dedryvère, *Solid State Ionics* 300, 78−85 (2017)** (ref **45**) | XPS 산화종 배정(P₂S₅ 배제, S−Oₓ) 의 참조 | Q2 |

원장에 이미 있는 것 중 이 편이 가리키는 것: **Zhang 2017 *ACS AMI* 9, 17835 (ref 29)** · **Zhang 2017 *JMCA* 5, 9929 (ref 40)**.
이 편이 **가리키지 않는 것**: Koerver 2017 *JMCA* 5, 22750 (같은 해 후속 — 시점상 불가) · Nam 2018 *JPS* · Nam 2018 *JMCA* ·
Ikezawa 2020 · Santhosha 2019 · Sedlmeier 2023 (전부 시점상 불가).

---

# 9. 주장하지 않는 것

- **접촉 손실이 없었다고 주장하지 않는다.** 주장은 **"EIS 창(7 MHz–1 Hz) 안에서 자란 양극 저항은 `C` 가 따라가지 않아 면적 형이 아니다
  (전제 `C ∝ 면적` 위)"** 까지다. 완전 고립된 입자, 창 밖(< 1 Hz) 과정, 분해 뒤 생긴 틈은 이 판정 밖이다.
- **`C` 비를 측정값처럼 쓰지 않는다** — 로그 축 판독 · CPE → C 환산식 미상(G6) · 적합 호가 위상 ≤4° 에서 겹친다.
- **S3 양성 대조를 강한 근거로 쓰지 않는다** — 호 정체 미상, 판 a ↔ c 크기 ≈8 배 불일치(D10), 셀 조건 미상(G11), 두 호 중 하나만 통과.
- **틈 폭(0.05–0.2 µm)을 측정값으로 쓰지 않는다** — 경사 파단면 투영 + 그림자. `ΔV/V ≈3–20 %` 는 **요구치의 범위**이지 추정치가 아니다.
- **상대극이 첫 사이클 손실의 몇 %를 만들었다고 주장하지 않는다** — 평탄 이탈의 **서명**과 **구조적 필연**(재고비 ≈1.4)까지다.
- **§4-2(c) 의 3.7 % 를 확정하지 않는다** — "1 % of SE" 의 기준이 인쇄되지 않았다(G10). 셀 전체 SE 기준이면 65 % 다.
- **E_In ≥ ≈0.71 V 를 측정값으로 쓰지 않는다** — LIB 분극 ≤30 mV 와 두 셀의 양극 OCP 동일을 가정한 **하한**이다.
- **3호 Liu · 4호 Shi 가 이 편을 잘못 인용했다고 하지 않는다** — 그 두 편의 인용 문장은 이번에 대조하지 않았다.

---

# 10. 어긋남 (지면 내부 정합)

| # | 어긋남 | 크기 |
|---|---|---|
| **D1** | "cycled between **2.7**−4.3 V vs Li⁺/Li" (본문·S1 캡션) ↔ 3.70–**2.00 V** vs In + 0.6 = 4.3–**2.6** ↔ `[도표]` Fig. 1a·S1a 방전 끝 **2.6 V** | 0.1 V — "2.7" 은 LIB 창 |
| **D2** | "≈50 Ω·cm⁻²" · "≈180 Ω·cm⁻²" | **R/A 로 계산된 차원 역전** — R·A = 31 · 110 Ω cm² (1.62 배 과대) |
| **D3** | 운전 "approximately **70 MPa**" ↔ "5 kN (**64 MPa**)"; 제작 445 ↔ 446 MPa | 9 % |
| **D4** | SI "current density of **2.14 A/cm²** (0.1 C)" ↔ 214 µA cm⁻² | 10⁴ 배 |
| **D5** | "constant capacity loss of **1−2%** per charging cycle" ↔ `[도표]` 21–50 사이클 ≈1.1 %, CE 99.1 % ⇒ 0.9 % | "2 %" 쪽은 1–5 사이클에만 |
| **D6** | "~100 mV … indicating an increase in the **IR drop**" ↔ `[도표]` S1a 1·2 차 **방전 곡선 겹침, 충전만 이동** | IR 이면 대칭이어야 한다 |
| **D7** | EIS ΔR ⇒ **~25 mV** ↔ DC **~100 mV** | 4 배 ("formation effects") |
| **D8** | 산화 S "**163.7 eV**"(본문) ↔ Fig. 5 표지 "**163.5 eV**" | 0.2 eV |
| **D9** | 무전류 이완 "at least **180 h**"(본문) ↔ S4 "**175 h**" ↔ S3 마지막 점 ≈165 h | 표기 |
| **D10** | S3(a) Nyquist 전체 **≤ ≈275 Ω** ↔ S3(c) `R_total` **≈950–2250 Ω** | ≈8 배 — 같은 실험의 두 판 |
| **D11** | 초록 "contact loss … **further increasing the interfacial resistance**" ↔ 결론 "This resistance was found to originate from a highly resistive **interphase**" | 배정 모순 |
| **D12** | "**no steady decomposition** … most of the interphase has formed after the first charging cycle" ↔ "amount … **increases** between one and 50 cycles" · `[도표]` Fig. 5 산화 S ≈2 배 · "ongoing capacity fade … attributed to the **propagating** interphase formation" | 서술 방향이 절마다 다르다 |
| **D13** | 공저자 "Aygün"(본문) ↔ "Dursun"(SI); 본문 SI 목록 "**Li₄Ti₅O₁₀**" | 표기 |
| **D14** | `R_SE,bulk` "virtually independent of the SOC" ↔ `[도표]` 첫 충전 448 → 485 Ω(+8 %) · LTO 셀 310–375 Ω(±10 %, SOC 추종) | "bulk" 호에 SOC 의존 성분이 섞였다 (`[추론]` LTO 는 리튬화로 전자 전도가 바뀐다) |
| **D15** | "initial OCV (**approximately 0.6 V**)" ↔ "assumed to be **0.6 V** vs Li/Li⁺" | 같은 숫자 두 뜻 — 둘이 동시에 참이면 양극 ≈1.2 V vs Li |
| **D16** | "Below an OCV of 3.2 V, corresponding to approximately **80% SOC**" ↔ `[도표]` Fig. 4 첫 방전 7 점 중 3.2 V 는 **세 번째** 점 | SOC 기준 미정의 |
| **D17** | In 박 "approximately capacity = **7.7 mAh/cm²**" ↔ `[재현]` 0.125 mm In → LiIn **21.3 mAh cm⁻²** | 기준 불명 (36 %) |
| **D18** | "**7.2 atom %** … ≈1 % of the SE" — 시편·기준 미기재 | G10 |

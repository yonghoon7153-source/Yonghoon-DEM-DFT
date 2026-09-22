---
title: "Yanev, Heubner, Nikolowski, Partsch, Auer, Michaelis 2024 — Editors' Choice: Alleviating the Kinetic Limitations of the Li-In Alloy Anode in All-Solid-State Batteries (J. Electrochem. Soc. 171, 020512)"
source_url: local-upload/16._Editors__Choice_Alleviating_the_Kinetic_Limitations_of_the_Li-In_Alloy_Anode_in_All-Solid-State_Batteries.pdf + 16._Sup_Editors__Choice_Alleviating_the_Kinetic_Limitations_of_the_Li-In_Alloy_Anode_in_All-Solid-State_Batteries.pdf (SI)
source_url_note: "본문 8쪽 (IOP 표지 1 + 본문 pp.1-7, 참고문헌 35편) + SI 2쪽 (Figure S1-S2 + Table S1). 크로핑 6장(본문 Fig. 1/3/4/5 + SI Fig. S1/S2) 중 **6장 전부 열람** + Figure 2(캡션 크로퍼가 놓친 사진 2장)를 `get_image_rects` 로 직접 렌더해 열람 + Fig. 1 g-i / d-f / a-c, Fig. 4 a/c/d, Fig. 5 a/b 를 500-1100 dpi 로 재크롭해 수치 판독. **안 본 것 0.** 1차 측정 있음 — 셀 12개(2전극 10 + 3전극 2), 조건당 n=1, 최대 5 사이클, 신품. `[인쇄]`/`[도표]`/`[재현]`/`[해석]` 4구분."
source_doi: 10.1149/1945-7111/ad2594
source_license: "CC BY 4.0, (c) 2024 The Author(s). Published on behalf of The Electrochemical Society by IOP Publishing Limited — Open Access, Editors' Choice"
pdf_sha256: 8fb10ec47e6136144b6334816cd6fb30b1bd7e53de1356f39fa70e3b5051163e
si_sha256: 5e3fdd576b865b2de1cabf23cf7f7e0a107a7df1c77426d13ceb5bb4ed324734
ingested: 2026-09-22
sha256: fed98b4bcf17cd748a8b555afd225a06e88087930fc6449a921175e744de7d37
---

# Yanev, Heubner, Nikolowski, Partsch, Auer, Michaelis 2024 — Editors' Choice: Alleviating the Kinetic Limitations of the Li-In Alloy Anode in All-Solid-State Batteries

> `assb` 섹션 **17호**. 닻은 `wiki/questions/assb-contact-loss-vs-lampe.md`.
> *J. Electrochem. Soc.* **171** (2024) 020512, doi `10.1149/1945-7111/ad2594`.
> Fraunhofer IKTS Dresden + TU Dresden. **Open Access (CC BY 4.0)**, Editors' Choice.
> 접수 2023-11-29 → 수정본 2024-01-15 → 게재 2024-02-12.
> 본문 **8쪽**(표지 1 + 본문 6 + 참고문헌) + **SI 2쪽**. 둘 다 sha256 봉인.
>
> ★★★★ **이 편은 이 계보에서 `Q5`(Li-In 기준 전위)를 본체로 삼은 첫 논문이다.**
> 16호(Ramanayagam 2026)가 μ-RE 를 설치해 놓고 기준 전위의 **안정성을 재지 않은**
> 바로 그 자리를, 17호는 **Li 금속 기준극으로 시간축 위에서 직접 잰다.**

## 0. 원문에 없어서 확인이 필요한 것 (먼저 읽는다)

이 절은 **이 논문이 주지 않는 것**의 목록이다. 아래 본문에서 `G*` 로 다시 가리킨다.

| # | 없는 것 | 왜 중요한가 |
|---|---|---|
| **G1** | ★★★ **개방회로에서 잰 `E_CE` 값이 한 번도 인쇄되지 않는다.** 셀 안에 Li 금속 RE 가 있고 프로토콜에 `[인쇄]` "initial **4 h relaxation**" 과 EIS 전 `[인쇄]` "relaxed for **5 h**" 이 있는데, **그 시점의 `E_CE` 숫자가 없다** | **0.62 V 가 끝까지 인용값**(ref 26 Santhosha)이다. 이 편은 그것을 자기 셀에서 검증할 수 있었고 하지 않았다. 16호가 두 셀에서 In–Li 평탄을 **0.58 ↔ 0.47 V** 로 본 직후라 더 아프다 |
| **G2** | ★★★ **CA 방전 종료 후 이완 중 `E_CE`** — Fig. 4d 는 foil 셀이 **1.33 V 인 채로** 끝난다 | **"과전압" 인지 "기준 전위가 옮겨 갔는지" 를 가르는 유일한 측정**이고, 그것이 이 카드의 Q5 그 자체다 |
| **G3** | **반복 0 · `n =` 0 회 · 오차막대 0.** 조건 12 개(2E 10 + 3E 2) × 셀 **1 개** | 아래 D11 — 논문이 "추세" 라 부른 것이 산포 대용보다 **작다** |
| **G4** | ★★ **적합이 0 이다.** `[인쇄]` "Detailed quantitative analyses and **modelling of the impedance spectra are beyond the scope of this study**". `fit*`·`equivalent circuit`·`ECM`·`CPE`·`capacitance`·`DRT`·`R_ct`(기호) **전수 0 회** | 16호에서 세운 **`R_CT·C_dl` 곱 축퇴 검사**의 첫 적용 대상인데 **입력이 없다** (§12) |
| **G5** | ★★ **접촉 면적의 값이 0 이다.** `contact surface` 1 회 · `contact area` 1 회 — **둘 다 인과 변수로 지목**되고 **단위·측정법·숫자 0** | Q1. 16호는 이름 붙이고 기하로 계산했고(θ≡1), 9호는 적합했고, **17호는 이름만 붙인다** |
| **G6** | **SE 20 wt% ↔ 40 wt% 의 차이를 전극 분해로 확인하지 않았다** — 3전극은 **40 % 쪽만** | §12 — 논문은 그 차이를 `[인쇄]` "effective ionic conductivity of the Li-In anode" 에 귀속한다 |
| **G7** | ★★ **화학·단면 분석이 0.** XRD·EDS·XPS·ToF-SIMS·**단면 SEM·post-mortem 전수 0** | 이 논문의 중심 기구(In-rich 고갈층)가 **직접 관찰된 적이 없다.** Li₅In₄·Li₃In₂ 도 전위로만 추정(ref 26,27) |
| **G8** | **스택 압력 스윕 0 · 이력 0 · 계측 0.** 운전 **50 MPa 한 점**, `hysteres*` 0 회 | Q6. 그리고 Wang et al. 과의 불일치를 `[인쇄]` "lower stack and assembly pressure" 로 설명하면서 **Wang 의 압력값을 적지 않는다** |
| **G9** | **사이클 수명 0.** 최대 **5 사이클**(형성 2 + CA 3). `LLI`·`LAM`·`SOH`·`aging` 전수 0 회 | `θ(N)` 도 `LLI(N)` 도 없다 — 이 편은 **신품 상태의 제조 변수** 논문이다 |
| **G10** | **`110 µA cm⁻²` 의 기준 면적이 명시되지 않았다** (셀 ∅12 mm? Cu 선 표면?) | D15 — RE 도금 전하가 **음극 조성을 얼마나 바꾸는가**가 8 배 달라진다 |
| **G11** | **"experimental capacity" 의 정의가 없다** (어느 사이클의 방전 용량인가) | EIS 의 "ca. 50 % SOC" 가 셀 간에 정렬됐는지 판정 불가 (D8) |
| **G12** | **데이터 가용성 문장 0** (JES 필수 아님). 원자료 없음 | 재적합 불가 — 16호와 같은 상태 |

## 1. 서지와 모집단

| 항목 | 값 |
|---|---|
| 저자 | S. Yanev¹, C. Heubner¹, K. Nikolowski¹, M. Partsch¹, H. Auer¹(교신), A. Michaelis^{1,2} |
| 소속 | ¹ Fraunhofer IKTS, Dresden · ² TU Dresden, Chair of Inorganic Non-Metallic Materials |
| 지면 | *J. Electrochem. Soc.* 171 (2024) 020512 · **Editors' Choice** · CC BY 4.0 |
| 과제 | "MaLiFest"(Lower Saxony MWK, 11–76251–99–2/17 (ZN3402)) · "FB2-Oxid"(BMBF, 03XP0434B) |
| 참고문헌 | **35 편** |
| 그림 | 본문 **5**(Fig. 1 9 패널 · Fig. 2 사진 2 장 · Fig. 3 모식도 · Fig. 4 4 패널 · Fig. 5 2 패널) + SI **2**(S1 SEM 4 패널 · S2 셀 모식도) + **Table S1** |
| 셀 수 | **12** — 2전극 10(foil 4 · powder 4 · composite 2) + 3전극 2(foil 1 · composite 1). **조건당 1** |
| 사이클 | **최대 5** (형성 CCCV 2 + 크로노암페로메트리 율시험 3) |
| 열화 | **없다** — `degrad*` 4 회는 전부 **율시험 3 회 사이의 성능 저하**를 가리킨다 |

**모집단 경고**: 이 편의 결론을 **`assb` 열화 문헌**으로 옮길 수 없다. 사이클 5 회,
신품, 압력 한 점, 셀당 1 개다. 이 편이 주는 것은 **열화 라벨이 아니라 "라벨을 읽는
자(기준극)가 얼마나 흔들리는가" 의 1차 측정**이다.

## 2. §서론 — 이 논문이 세운 물음

논문은 ASSB 양극 연구의 **표준 실험 설계**를 먼저 해부한다.

> `[인쇄]` "In a typical experiment, a two-electrode setup is employed, where the
> cathode (working electrode, WE) parameters … are varied. The sulfide separator,
> and the anode (counter electrode, CE) are kept constant. **Any recorded
> differences in the cell performance are then correlated with the varied cathode
> parameters.** The WE potential of the cell is controlled against the CE potential."

그 다음이 이 논문의 물음이다.

> `[인쇄]` "Due to the CE potential control, it is desirable that the anode has a
> **defined reference potential** and does not generate significant overpotentials
> during electrochemical characterization. … **However, this assumption is rarely
> confirmed experimentally.**"

`[해석]` **이 두 문단은 우리 닻 카드의 Q5 를 그대로 쓴 것이다.** 우리가 "완전지 OCV 는
평탄 음극 위에 얹힌 양극 곡선 하나" 라고 가정할 때 딛는 바로 그 가정을, 이 논문은
**실험 설계의 가정**으로 부르고 검증 대상으로 세운다.

**0.62 V 의 출처**(중요 — 이 숫자는 이 논문이 잰 것이 아니다):

> `[인쇄]` "a **stable reference potential of 0.62 V vs Li⁺/Li in a broad
> stoichiometric region**.²⁶"
> `[인쇄]` "Santhosha et al. conducted **coulometric titration** of Li-In electrodes
> and concluded that indeed the **In+LiIn two-phase region** is responsible for the
> well-known reference potential of 0.62 V vs Li⁺/Li.²⁶ **The Li-richer phases show
> lower potentials, which are strongly dependent on small lithiation changes.**²⁶"

⇒ ref **26 = Santhosha, Medenbach, Buchheim, Adelhelm, *Batteries & Supercaps* 2019**.
**후속 후보 상위권**이다 (§17).

그리고 **선행 반례 넷**을 논문이 직접 나열한다 — 이 계보의 지도로 그대로 쓸 수 있다.

| ref | 누가 | 무엇을 보였나 (`[인쇄]` 요약) |
|---|---|---|
| **14** | Krauskopf 2019 (*AEM* 9, 1902568) | 합금 음극의 **확산 한계** |
| **16** | Ikezawa 2020 (*Electrochem. Commun.* 116, 106743) | 3전극 Li-In/LCO — **1 C 이상에서 Li-In 이 병목** |
| **20** | Nam 2018 (*JMCA* 6, 14867) | Sn WE 대조 3전극 — **제조법이 동역학을 결정** · **Li-In-SE 복합 음극 제안** |
| **21** | Sedlmeier 2023 (*JES* 170, 030536) | 3전극 임피던스 — **분리막 근처 Li 농도가 결정적** |

`[해석]` **이 편은 "새 현상 발견" 이 아니라 "네 편이 따로 말한 것을 한 셀 계열에서
계통적으로 재현하고 처방까지 붙인 편" 이다.** 그 점은 논문도 감추지 않는다
(`[인쇄]` "These results are **consistent with** the results of Ikezawa et al.").

## 3. §실험 — 셀 제원과 프로토콜 (전수 채록)

### 3.1 재료
- SE: **Li₆PS₅Cl (LPSCl)**, NEI Corp.
- CAM: **단결정 LiNi₀.₈Co₀.₁Mn₀.₁O₂ (NCM811)**, MSE Supplies
- 도전재: **VGCF**(기상성장 탄소나노섬유), Merck
- Li: Tobmachine · In 박: ChemPur · In 분말: Merck
- 전부 Ar 글러브박스(`[인쇄]` "<1 ppm O₂, <1 ppm H₂O")

### 3.2 복합양극
`[인쇄]` CAM : SE : VGCF = **73.2 : 24.0 : 2.8 wt%**, 볼밀(Pulverisette 23, Fritsch).

`[재현]` **면적 하중과 공칭 비용량의 정합 검사** — 논문이 하지 않은 계산:
- 2전극: 양극 **15 mg** / A = π(0.5 cm)² = 0.7854 cm² ⇒ **19.1 mg cm⁻²**
- 3전극: 양극 **21.6 mg** / A = π(0.6 cm)² = 1.1310 cm² ⇒ **19.1 mg cm⁻²** (동일 ✔)
- CAM 분율 73.2 % ⇒ **13.98 mg cm⁻²**
- 공칭 **2.80 mAh cm⁻²** ÷ 13.98 mg cm⁻² = **200 mAh g⁻¹**
⇒ **내부 정합 ✔**. 공칭 비용량 200 mAh g⁻¹(NCM811 통상치)이 명시되지 않았지만
**역산으로 확인된다.** 그리고 **1 C = 2.80 mA cm⁻²** 도 이로써 확인된다
(결론절 `[인쇄]` "already ≥ 1 C = 2.80 mA cm⁻²" 와 일치).

### 3.3 음극 세 종류

| 종류 | 제조 | 조성 스윕 |
|---|---|---|
| **(a) foil** | In 박 + Li 박을 **셀 안에서** 500 MPa/1 min 로 압착 (in situ 기계화학 합금화) | **45 · 47 · 49 · 50 at% Li** (2E) |
| **(b) powder** | LiIn(1:1)을 강관/강판 사이에서 **손으로 압연·접기 반복** → 어두워지고 부서질 때까지 → 마노유발에서 **과잉 In 분말과 혼합** | **36 · 40 · 44 · 47 at% Li** (2E) |
| **(c) composite** | Li-In 분말(40 at% 고정) + **SE 분말 20 또는 40 wt%** 를 유발에서 혼합 | **40 at% + 20 % SE · 40 at% + 40 % SE** (2E) |

`[인쇄]` 복합 음극은 **Nam et al.²⁰ 의 제안**이고 이 편이 `[인쇄]` "verified in our study".

### 3.4 셀 조립

| | **2전극** | **3전극** |
|---|---|---|
| 몰드 | PET, **∅10 mm**, SS 피스톤 (Hohsen KP) | **PEEK, ∅12 mm**, **WC 피스톤** (rhd CompreCell 12PEEK-DP) |
| 분리막 | LPSCl **150 mg @ 500 MPa** | LPSCl **216 mg @ 375 MPa** (Cu 선을 품고) |
| 음극 | (a) In **75 mg**(125 µm) + Li **3.6–4.4 mg**(80–100 µm) / (b) LiIn 분말 **80 mg** / (c) 복합 **80 mg** — 전부 500 MPa/1 min | (a) In **108 mg** + Li **4.4 mg** / (b) 복합 **120 mg** — 500 MPa/1 min |
| 양극 | **15 mg**, 500 MPa/1 min | **21.6 mg**, 500 MPa/1 min |
| RE | 없음 | **∅400 µm Cu 선**을 분리막 **한가운데 근처**에 매립 → `[인쇄]` **110 µA cm⁻² × 15 h** 로 **in situ Li 도금** |
| 온도 | **30 °C** | **room temperature** ← ⚠ D4 |
| 스택 압력 | `[인쇄]` **ca. 50 MPa** | `[인쇄]` **50 MPa** (rhd CompreDrive) |
| 포텐시오스탯 | Biologic VMP-3e | Biologic VSP |

`[재현]` **질량 정합**: 3E/2E 면적비 = 1.1310/0.7854 = **1.440**.
분리막 216/150 = 1.440 ✔ · 양극 21.6/15 = 1.440 ✔ · In 108/75 = 1.440 ✔.
⇒ **3전극 셀은 2전극 셀을 면적만 1.44 배 키운 것**이다 — 딱 두 가지를 빼고:
**분리막 압착압(375 ↔ 500 MPa)** 과 **온도(실온 ↔ 30 °C)**. 둘 다 무언급 (D4·D5).

### 3.5 전기화학 프로토콜 (순서가 결과 해석을 좌우한다)

`[인쇄]` 전압창 **2.38–3.68 V vs Li⁺/LiIn = 3.00–4.30 V vs Li⁺/Li**
(변환은 **0.62 V 오프셋 가정**, ref 26).

1. 초기 **4 h 이완**
2. **형성 2 사이클** — 0.1 C **CCCV 충전**(CV 종료 전류 0.02 C) + **CC 방전**, 충·방전 뒤 각 **10 min 이완**
3. **율시험 3 사이클** — 같은 CCCV 충전 + **정전위 방전(CA)** at `[인쇄]` **3.0 V vs Li⁺/Li**, 종료 기준 **0.02 C**
   (방법 원전: ref 29 = **Yanev 2022 *JES* 169, 090519**, ref 30 = Heubner 2018)
4. 0.1 C 로 **실험 용량의 절반**까지 충전 → 셀 전압 `[인쇄]` "∼3.2 V"
5. **5 h 이완** → **EIS**: 2전극 **1 MHz–10 mHz**, 3전극 **1 MHz–100 mHz**, 진폭 **25 mV**

★ **율시험 곡선은 오른쪽(고율) → 왼쪽(저율) 으로 읽는다**:
> `[인쇄]` "the rate performance curves are recorded **from high (right) to low
> (left) C-rates** i.e., the cell initially experiences its highest possible
> discharge rate, and then discharges to completion with a steadily decreasing rate."

`[해석]` 이것이 중요하다 — **CA 한 번이 곡선 한 줄을 만든다.** 따라서 Fig. 1d–f·4b 의
"세 사이클" 은 **세 번의 CA**이고, 곡선이 서로 어긋나면 그것은 율 효과가 아니라
**사이클 간 변화**다.

## 4. §결과 — Fig. 1 (2전극, 음극 3 종 × 조성 스윕) 【그림 본 것】

캡션 `[인쇄]`: "(a)–(c): Charge and discharge curves of the initial two CCCV cycles …
(d)–(f): Discharge rate performance … recorded via chronoamperometry (three cycles).
(g)–(i): Impedance spectra … at 3.2 V vs Li-In, corresponding to ca. 50% SOC."

열: **foil(초록) | powder(빨강) | composite(파랑)**.

### 4.1 (a)–(c) 전압 곡선 — 축과 실제 값

`[도표]` y = **E vs LiIn (V)**, 2.4–3.8 · x = **Spec. capacity (mAh g⁻¹)**, 0–250.

| 패널 | 읽은 것 |
|---|---|
| **a (foil)** | 45 · 47 · 49 at% 세 곡선이 **겹친다** (방전 ≈190, 충전 CV 끝 ≈225). **50 at%(검정)만 다르다** — 충전 ≈140 에서 3.68 V 도달, 방전 ≈140 |
| **b (powder)** | 36 · 40 at% 정상(방전 ≈195–200) · **44 at% ≈172** · **47 at%(가장 진함) ≈140** |
| **c (composite)** | **두 곡선이 사실상 겹친다** (방전 ≈190, 충전 CV 끝 ≈225) |

`[인쇄]` foil 의 50 at% 에 대한 논문의 해석 — **이 편에서 우리 Q5 에 가장 직접적인 문단**:

> "At 50% Li a significant change in the voltage profile as well as much lower charge
> and discharge capacities are observed. … the charging curves initially overlap and
> then deviate as soon as **ca. 50 mAh g⁻¹** are charged. **In the two-electrode
> configuration, the potential is referenced to the Li-In CE, only.** Overlithiation
> of Li-In likely occurs … This leads to the generation of **Li-rich phases such as
> Li₅In₄ or Li₃In₂**, which **lower the anode and reference potential below the
> target 0.62 V**. **A potential shift of roughly 0.2 V** is observed at comparable
> charging capacities. … Consequently, the upper charging limit of the cell is
> achieved before the CAM is completely delithiated. In other words, the ASSB is
> effectively cycled to a lower cut-off potential of **roughly 4.1 V relative to
> Li/Li⁺** and thus significantly lower than the **4.3 V** as intended."

★★★★ `[해석]` **이것이 우리 축퇴의 순수 표본이다.** 2전극 데이터만 보면 이 셀은
**"용량이 40 mAh g⁻¹ 작다"** — 즉 **`LAM_PE` 의 서명**이다. 실제로는 **활물질이 그대로
있고 기준극이 0.2 V 내려간 것**이다. 그리고 논문은 이것을 **3전극 없이** 전압 곡선의
모양 변화만으로 잡아냈다 — 하지만 그것이 가능했던 이유는 **Li 함량을 의도적으로 스윕**
했기 때문이다. **스윕 없이 셀 하나만 있었다면 구별할 수 없다.**

### 4.2 (d)–(f) 율 특성 (CA)

`[도표]` y = 방전 비용량 0–220 · x = **C-rate (nom.) 로그축 0.01–30**.

| 패널 | 읽은 것 (`[도표]`, ≈) |
|---|---|
| **d (foil)** | **49 at%** 0.02 C 에서 **≈202**, ~0.5 C 까지 평탄, 1 C **≈175**, 0 도달 ≈9 C · **50 at%** 시작 **≈152**, 완만, 1 C ≈120 · **47 at%** 시작 ≈200, **세 사이클이 벌어진다** · **45 at%** 0.2 C 에서 이미 ≈150, 가장 빨리 붕괴 |
| **e (powder)** | 36 · 40 · 44 at% 시작 **≈205–210** 인데 **0.1–0.5 C 에서 급락** · **47 at%** 시작 **≈148**, 완만하고 고율에서 최선 |
| **f (composite)** | 두 조성 모두 시작 **≈196–202**, **무릎이 ≈1 C**, 0 도달 ≈9 C. **세 사이클이 촘촘히 겹친다**(가장 재현성이 높다). 40 % SE 가 20 % SE 보다 **근소하게 오른쪽** |

★ `[재현]` **1 C 에서의 값 비교** (그림 판독, ±10 mAh g⁻¹): composite **≈185** ·
foil-49 **≈175** · foil-50 **≈120** · powder-47 **≈115** · foil-45 **≈65** ·
powder-40 **≈45**. ⇒ **최선과 최악이 4 배**이고 **모두 같은 양극**이다.

`[인쇄]` 논문의 해석: "The shape of the chronoamperometry profiles shows a low-rate
plateau and a **steep rate performance drop, which is typical for cathode-limited
cells**" — 즉 composite 과 foil-49/50 의 곡선 모양이 **양극 제한**의 모양이고,
나머지의 완만한 붕괴는 **음극 제한**의 모양이다. 형태 기준이다.

⚠ `[해석]` **형태 기준은 정량 기준이 아니다.** "steep" 의 문턱이 정의되지 않았고
(`G4`), 전 그림에서 **곡선을 적합한 곳이 한 군데도 없다.** 이 분류가 3전극(§6)에서
**독립으로 확인되는 것은 foil-40 at% 와 composite-40 %SE 두 셀뿐**이다.

### 4.3 (g)–(i) 임피던스 — 값 판독

`[도표]` 축 **Re(Z) 0–120 Ω · −Im(Z) 0–120 Ω** (⚠ **데이터 최대가 ≈15 Ω** 이라
패널의 **87 % 가 비어 있다.** 두 번째 반원이 눈으로 거의 안 보인다).
`[도표]` **보라색 마름모 = 2 Hz** 표식 (유일한 주파수 앵커).

`[재현]` 고주파 절편(≈ 분리막+접촉) **→** 2 Hz 지점의 실축값:

| 셀 | HF 절편 (Ω) | 2 Hz Re (Ω) | 저주파 반원 | 총 (≈) |
|---|---:|---:|---|---:|
| foil **45 at%** | ≈34.5 | ≈76.5 (−Im ≈13) | ★ **크다**, 정점 −Im ≈13.5 @ Re ≈84, 끝 **≈104** | **≈70** |
| foil **47 at%** | ≈36 | ≈75.5 (−Im ≈6.5) | 있다, 끝 ≈90 | ≈54 |
| foil **49 at%** | ≈40 | ≈72 (−Im ≈0.6) | 작다, 끝 ≈77 | ≈37 |
| foil **50 at%** | ≈41 | ≈66 (−Im ≈0.5) | 거의 없다, 끝 ≈72 | ≈31 |
| powder **36/40/44** | ≈35 | ≈84–86 | ★ 크다, 끝 **≈96** | ≈61 |
| powder **47 at%** | ≈35 | ≈60 | 없다, 끝 ≈62 | **≈27** |
| composite **20 % SE** | ≈39 | ≈75 | 없다(단일 호), 끝 ≈80 | ≈36 |
| composite **40 % SE** | ≈37.5 | ≈64.5 | 없다(단일 호), 끝 ≈70 | **≈27** |

`[인쇄]` 논문의 읽기: "anodes with **higher lithium content show a single semicircle
in the high frequency region (ca. 1 kHz)**, whereas anodes with **lower Li content
show a high frequency contribution and an additional semicircle in the low frequency
region (1–10 Hz)** … **Prior impedance studies on sulfide ASSBs have established that
higher frequencies are associated with cathode effects and lower frequencies are
associated with anode effects.**³²,³³" (→ **D12**, ref 32 = 우리 10호)

`[인쇄]` 그리고 **고주파 산포는 지나간다**:
> "**The variation in the high frequency impedance is most likely not related to the
> anode and is within the typical error of the measurement**, considering that the
> charge transfer resistance of composite cathodes is very sensitive to the state of
> charge.³⁴ Detailed quantitative analyses and modelling of the impedance spectra
> are **beyond the scope of this study**."

⚠⚠ `[재현]` **그 "typical error" 는 34.5 → 41 Ω, 즉 ≈19 %** 다(foil 4 셀). 그리고
**반복이 0 이므로 "typical error" 의 근거가 이 논문 안에 없다**(G3). 게다가 그 설명
자체가 **D8 의 자기 모순**으로 이어진다.

★★ `[재현]` **powder-47 at%(≈27 Ω)와 composite-40 %SE(≈27 Ω)의 총 임피던스가 같다.**
그런데 방전 용량은 **≈140 ↔ ≈190 mAh g⁻¹** 다. ⇒ **임피던스가 같아도 용량이 26 % 다르고,
그 차이는 과리튬화에 의한 기준 전위 이동에서 온다.** `[해석]` **임피던스 채널과 전위
채널은 서로 다른 것을 본다** — 우리 3항 분해(`Q_apparent = θ_AM · Q_material · η(i)`)에
**네 번째 인자(기준 전위 이동)** 가 있고 그것은 **η 에도 θ 에도 들어가지 않는다.**

## 5. Fig. 2(사진) + Fig. 3(모식도) — 기구 주장의 근거 【그림 본 것】

### 5.1 Fig. 2 — 이 논문의 중심 기구를 떠받치는 유일한 형태학 증거

`[인쇄]` 캡션: "Photographs of a un**a**xially pressed Li-In foil-type anode.
Left: Indium side. Right: Lithium side." (원문 오타 "unaxially")

`[도표]` **본 것**: 왼쪽(In 쪽) = **거의 전면이 밝은 금속 광택**, 아래 가장자리에
어두운 반점 몇 개. 오른쪽(Li 쪽) = **중앙 ≈60 % 가 짙은 회흑색**, 바깥에 밝은 테.
핀셋이 우측 상단을 가린다. **스케일바 없음 · 배율 미상 · 시편 1 개.**

`[인쇄]` 본문: "manufactured by uniaxially pressing Li and In foil with **40 at% Li**
at a high pressure of 500 MPa. … the **dark colored Li-In phases are found mostly on
the Li side** of the disc, while the In side … consists mostly of metallic In with
only minor Li-In regions, implying an **incomplete intermetallic reaction**. **In an
ASSB stack the In side is in contact to the separator** while the Li side is directed
to the current collector piston."

그리고 결정적인 기하 문장:
> `[인쇄]` "we pressed discs of **10 mm diameter in a 13 mm die**, and it appears that
> the Li-In phases remained at roughly the initial 10 mm, while the **In phase was
> flattened to 13 mm**."
> `[인쇄]` "**Li-In does not flow plastically** and does not distribute evenly in the
> soft indium matrix with uniaxial pressing alone, even at high fabrication pressures
> of 500 MPa.²¹ Effectively, **most of the generated Li-In phases remain embedded on
> the current collector side of the In foil and do not reach the separator side**."

⚠⚠ **D7**: **이 시편은 이 연구의 어떤 셀도 아니다.** 실제 셀은 **∅10 mm PET 몰드(2E)**
또는 **∅12 mm PEEK 몰드(3E)** 안에서 압착돼 **측면 구속**이 있다. Fig. 2 의 관측
(In 이 13 mm 로 퍼지고 Li-In 은 10 mm 에 남는다)은 **측면 유동이 허용된 기하**의
산물이다. 논문은 이 차이를 언급하지 않는다. ⇒ **두께 방향 편석 주장은 살아남을 수
있지만, 그 주장을 "보여 주는" 사진은 다른 실험에서 왔다.**

⚠ 부수: Fig. 2 는 **광학 사진에서 어두운 것 = Li-In** 이고 Fig. S1 은 `[인쇄]`
**BSE-SEM 에서 밝은 것 = In-rich** 다. 모순은 아니지만(모달리티가 다르다) 독자가
**두 대비 규약을 오가야** 하고, 둘 중 어느 쪽도 **면적 분율로 정량되지 않았다**(D10).

### 5.2 Fig. 3 — 모식도

`[인쇄]` 캡션: "Schematic of ASSBs with differing Li-In anode types and **Li depletion
during fast discharge conditions**. The target LiIn phase is shown in **purple**."

`[도표]` **본 것**: 3 열. 각 열 위 = 원료, 아래 = "Fast discharge" 화살표 뒤의 상태.
- **foil**: 아래 그림이 **위(집전체) 보라 → 아래(분리막) 회색**의 **연속 구배**.
  캡션 `[도표]` "Li depletion at discharge."
- **powder**: 보라·회색 입자가 섞여 있으나 **분리막 접촉면에 옅은 띠**.
  캡션 `[도표]` "Li depletion at discharge. **Poor contacts.**"
- **composite**: 보라 + **노랑(SE)** 이 전 두께에 고르게. 캡션 `[도표]` "Li accessible.
  Good kinetics."

⚠ **D13**: **Fig. 2 + 본문은 In-rich 층을 제조 기원**(불완전 합금화)으로 놓고,
**Fig. 3 은 같은 층을 "Fast discharge" 화살표 뒤**에 그린다. 본문이 `[인쇄]` "expect the
existence of an In-rich layer … to **aggravate** the Li transport limitations" 로 둘을
겹치기는 하지만, **둘을 가르는 실험이 없다**(G7 — 신품 단면 0 · 방전 후 단면 0).
`[해석]` **"제조 결함" 인지 "매 사이클 재발하는 내재 현상" 인지가 정해지지 않는다** —
그리고 그 분기가 이 논문의 처방(제조법을 바꿔라)이 딛는 바로 그 자리다.

## 6. §3전극 — Fig. 4 【그림 본 것 · 이 편의 심장】

캡션 `[인쇄]`: "(a) Charge and discharge curves of the initial two CCCV cycles of
Li-In/NCM811 **three-electrode** ASSBs with **Li reference electrode** and foil- and
composite-type anode. (b): Discharge rate performance … (c): Time dependence of the
WE, CE and cell potential and current density during the **second CCCV cycle**.
(d): … during the **first chronoamperometric discharge**."

⚠⚠ **D6 — 비교 대상 고르기**: `[인쇄]` "In both cases, the **Li content of the Li-In
phase is fixed at 40 at%**." 즉 **3전극의 foil 셀은 40 at%** 인데, 2전극 foil 계열은
**45/47/49/50 at%** 였고 논문이 스스로 찾은 sweet spot 은 **49 at%** 다.
⇒ **논문이 권장하는 foil 음극(49 at%)은 전극 분해로 한 번도 검증되지 않았다.**
(저자 의도는 복합과 Li 함량을 맞추는 것이고 그렇게 적혀 있다. 문제는 결론절의
`[인쇄]` "Li-In **foil-type anodes, which are used in the vast majority of sulfide
ASSB works**, showed severe kinetic limitations" 가 3전극 근거를 끌어다 쓴다는 것이다.)

### 6.1 Fig. 4a — 0.1 C 정전류에서는 차이가 작다 ★★★★

`[도표]` 축 E_cell 2.4–3.8 V · Q 0–250 mAh g⁻¹.
- **복합**: 방전 **≈198**, CCCV 충전 CV 끝 **≈247**
- **foil**: 방전 **≈185**, CV 끝 **≈232**
- 두 셀의 **방전 곡선 모양이 Q ≈ 170 까지 구별되지 않는다.** 갈라지는 것은
  **마지막 ≈15 mAh g⁻¹ 의 무릎 위치**뿐(foil ≈178, 복합 ≈192 에서 급락 시작)

★★★★ `[재현]` **0.1 C 에서 foil 의 손실은 (198−185)/198 = 6.6 %.**
같은 두 셀의 CA 율시험(Fig. 4b)에서는 **최대 용량이 ≈135 ↔ ≈207, 손실 ≈35 %.**
⇒ **같은 결함이 율에 따라 6.6 % 에서 35 % 로 5 배 커진다.**

`[해석]` ★★★ **이것이 이 편이 우리에게 주는 가장 직접적인 것이다.**
**0.1 C 에서 이 셀을 2전극으로만 보면, 관측되는 것은 "용량이 6.6 % 작다 + 방전 곡선의
끝이 잘렸다" 이고 그것은 `LAM_PE`(또는 컷오프 이동)의 서명과 같다.** 3전극이 말해 주는
것은 **양극 활물질이 전혀 줄지 않았다**는 것이다 (§6.3). **RPT 가 저율일수록 이 오독이
작아 보이지만 사라지지는 않는다.**

### 6.2 Fig. 4b — 율 특성

`[도표]` **복합**: 0.02 C **≈207**, 세 사이클 겹침, 0 도달 ≈4–5 C.
**foil**: 세 사이클이 **≈135 → ≈110 → ≈95** 로 **단조 감소**(최저율에서), 0 도달 ≈1–5 C.
`[인쇄]` "The cell with Li-In metal **loses capacity between the first and second
galvanostatic cycle** and shows severely limited performance during the rate
capability test."

`[해석]` foil 의 세 CA 곡선이 회복하지 않고 계속 내려간다 ⇒ **In-rich 고갈층이 한
사이클 안에 완전히 되돌려지지 않는다.** (논문은 2전극 Fig. 1d 의 47 at% 에서도
`[인쇄]` "a notable shift … between the first and second measurement, indicating
**rapid degradation**" 이라고 적는다.) ⚠ **그 비가역분을 정량한 곳은 없다.**

### 6.3 Fig. 4c — 정전류 사이클 중의 세 전위 ★★★ (Q5 의 본체)

`[도표]` 축: 왼쪽 **E vs Li (V) 0.5–4.5** · 오른쪽 **I (µA cm⁻²) −400 … +400** · x = t 0–24 h.
10 개 트레이스(복합 실선 4 · foil 파선 4): E_cell(검정) · E_we(빨강) · E_ce(**파랑**) · I(초록).

`[도표]` **읽은 것**:
- **전류(초록)**: 충전 **+280 µA cm⁻²** 평탄(= 0.1 C ✔) → t ≈9.7 h 에서 CV 로 꺾임 →
  t ≈10.3 h 에 **−280 µA cm⁻²** 로 방전 → 복합 t ≈20.3 h, foil t ≈19.6 h 종료
- **E_we(빨강)**: 복합 충전 끝 정점 **≈4.28–4.30 V** ✔(= 3.68 + 0.62), 방전 끝 **≈3.02 V**
- **E_we(빨강, foil)**: t ≈18 h 부터 실선에서 갈라져 **≈3.45 V 에서 종료**
- **E_ce(파랑)**: ★ 두 셀 모두 **0.61–0.63 V 에서 t ≈17 h 까지 겹친다.**
  **foil 만** t ≈17 h 부터 서서히 오르고 **t ≈19.5 h 에 ≈1.0 V 로 급상승**한 뒤 종료.
  **복합은 끝까지 평탄**하다.

`[인쇄]` 논문의 수치:
> "During charging (anode lithiation), **E_CE remains constant at 0.61 V for both
> anode types**, which translates to a **minor anodic overpotential of about 10 mV**
> considering the expected potential of 0.62 V. During discharge (delithiation)
> **E_CE of both anode types are initially constant at ca. 0.63 V**. However, **at the
> end of discharging, E_CE of the Li-In metal cell significantly increases**, whereas
> E_CE of the Li-In-SE composite cell **remains constant**. The increase of E_CE
> lowers E_cell, which leads to an **early termination of the discharge**, and an
> overall reduced discharge capacity for the Li-In metal cell."

★★★ **논문은 그 "significantly increases" 에 숫자를 붙이지 않는다. 우리가 붙인다**:
`[도표]` **≈1.0 V**, 즉 **0.62 V 기준에서 +≈0.4 V**.
`[재현]` 정합 검사: E_cell 하한 2.38 V + E_CE ≈1.0 V = **E_we ≈3.4 V** — `[도표]` 로 읽은
foil 의 방전 종료 E_we **≈3.45 V** 와 맞는다 ✔.
⇒ **양극은 의도한 3.00 V 가 아니라 ≈3.4 V 에서 방전이 끝난다.** 그 0.4 V 구간이
Fig. 4a 의 **잃어버린 13 mAh g⁻¹** 이다.

### 6.4 Fig. 4d — CA 방전 중의 전위 ★★★★ (이 편 최고의 숫자)

`[도표]` 축: **E vs Li 0.5–4.5 V** · 오른쪽 **I (mA cm⁻²) +2 … −16** · x = t 0–12 h.
**인셋**: x = 0–0.4 h, 같은 y.

`[도표]` **읽은 것**:
- **전류(초록)**: t = 0 에서 **축 하단(−16 mA cm⁻²) 아래**에서 시작 → t ≈1 h 에 **≈0**
  (두 셀 모두). ⇒ **초기 전류 ≥ 16 mA cm⁻² ≈ 5.7 C**
- **복합(실선)**: E_ce 가 인셋에서 **≈0.95 V 로 시작 → t ≈0.03 h 에 ≈0.62 로 떨어져 평탄**,
  t = 2.3 h 종료까지 **0.61–0.63**. E_we **3.02 → 2.99 V**. E_cell **2.38 고정**
- **foil(파선)**: E_ce 가 인셋에서 **≈0.75 ↔ ≈1.30 V 사이를 t ≈0.15 h 까지 요동** →
  **t ≈1.5 h 에 ≈1.40 V 정점** → t = 7.3 h 종료까지 **≈1.33 V 로 완만히 하강**.
  E_we **≈3.78 → ≈3.72 V**

`[인쇄]` 논문의 수치 (그림과 일치):
> "At the beginning of discharge, which corresponds to the highest current densities,
> the Li-In metal E_CE is **very unstable and oscillates rapidly between 1.3 V and
> 0.7 V**. After about 0.2 h, **E_CE stabilizes between 1.4 V and 1.3 V vs Li⁺/Li**
> until low-rate discharge completion, which corresponds to a **very high anodic
> overpotential of over 0.7 V**. Since the WE is referenced against the CE, **E_WE is
> between 3.7 V and 3.8 V vs Li⁺/Li at discharge completion, instead of the ideal
> 3.0 V**, explaining the uncomplete discharge. In contrast, **E_CE of the Li-In-SE
> composite cell shows a much lower potential of ca. 0.9 V at the beginning of
> discharge and relaxes rapidly to 0.64 V at 0.2 h**, which corresponds to an
> **overpotential of just ca. 20 mV**."

`[재현]` **내부 정합 ✔**: E_we − E_ce = 3.78 − 1.40 = **2.38 = E_cell** ✔ ·
2.99 − 0.61 = **2.38** ✔. 논문의 수치는 자기 정합적이다.

### 6.5 ★★★★ 우리가 한 계산 — "과전압" 의 몇 %가 옴인가 `[재현]`

논문은 E_CE 의 편차를 전부 **"anodic overpotential"** 이라고 부른다. 그런데 3전극에서
측정되는 E_CE 에는 **CE–RE 사이 분리막 구간의 미보상 옴 강하**가 그대로 들어간다.
그 저항은 **Fig. 5 의 CE/RE 고주파 절편**으로 읽을 수 있다 — **논문이 하지 않은 연결**이다.

`[도표]` Fig. 5 CE/RE HF 절편: **foil ≈28.7 Ω · composite ≈13 Ω** (§7).
셀 면적 **1.1310 cm²**, 공칭 용량 **3.167 mAh**.

| 구간 | 전류 | `I·R(CE–RE)` foil | 관측 ΔE_CE foil | 옴 몫 |
|---|---:|---:|---:|---:|
| 0.1 C 정전류 | 0.317 mA | **9.1 mV** | `[인쇄]` ±10 mV | **≈100 %** |
| CA 초기 (≈16 mA cm⁻²) | 18.1 mA | **0.52 V** | `[인쇄]` +0.68 V (→1.3) | **≈76 %** |
| **CA 정상 (전류 → 종료기준 0.02 C)** | **≤0.063 mA** | **≈1.8 mV** | `[인쇄]` **+0.73 V** (→1.35) | **≈0.2 %** |

★★★★ `[해석]` **세 줄이 각각 다른 것을 말한다**:

1. **0.1 C 의 "≈10 mV 음극 과전압" 은 옴 강하와 구별되지 않는다.** 게다가 논문은 **두
   셀 모두 0.61/0.63** 이라고 적는데, `R(CE–RE)` 가 **2.2 배 다르므로**(28.7 ↔ 13 Ω)
   순수 옴이라면 **9.1 ↔ 4.1 mV** 로 갈렸어야 한다. ⇒ **두 기여가 섞여 있고 논문은
   나누지 않는다.** (충전 −10 mV / 방전 +10 mV 의 **대칭**은 옴 또는 대칭 동역학 둘 다와
   양립한다.)
2. **CA 초기의 거대한 돌출은 대부분 옴이다** (foil 76 % · composite `[재현]` 0.235 V /
   0.33 V ≈ **71 %**). ⇒ `[인쇄]` "oscillates between 1.3 V and 0.7 V" 의 진폭은
   **전류 요동의 그림자일 수 있다.** 논문은 이것을 검토하지 않는다.
3. ★★★★ **그러나 정상 구간은 옴이 아니다.** 전류가 **종료 기준(0.02 C)** 까지 떨어진
   뒤에도 foil 의 E_CE 는 **≈1.35 V 에 6 시간 이상 머문다.** 그 전류에서 옴은
   **≈2 mV**, 관측은 **+730 mV** — **0.2 %** 다. 넉넉히 0.5 C 를 가정해도 45 mV 다.
   ⇒ **이것은 과전압이 아니라, Li 가 거의 빠진 In 표면의 (준)평형 전위다.**

★★★★★ **그래서 이 편의 결론적 숫자는 이렇게 적어야 한다**:
> **같은 프로토콜 · 같은 전류(≈0) · 같은 공칭 조성(40 at% Li) 의 두 Li-In 음극이
> `E_CE` = 0.61 V ↔ 1.35 V, 즉 ≈0.74 V 갈린다. 차이는 제조법뿐이다.**

⚠ 그리고 **이것을 "기준 전위 이동" 이라고 못 박으려면 G2 가 필요하다** — CA 종료 후
이완 곡선. 논문은 그것을 재지 않았다. **우리 판정은 "옴이 아니다" 까지가 확실하고,
"평형 전위다" 는 `[해석]` 이다.**

## 7. Fig. 5 — 전극 분해 EIS 【그림 본 것】

캡션 `[인쇄]`: "Impedance spectra at a cell voltage of **3.2 V** of the three-electrode
Li-In/NCM811 cells with (a) foil and (b) composite-type anode."
각 패널 3 곡선: **WE/CE(검정, 완전지) · WE/RE(빨강, 양극) · CE/RE(파랑, 음극)** + **2 Hz**.

`[재현]` 판독표 (축 0–140 Ω × 0–60 Ω, ±1–2 Ω):

| | **(a) foil 40 at%** | **(b) composite 40 at% + 40 % SE** |
|---|---|---|
| WE/RE **HF 절편** | **≈12.6 Ω** | **≈29.5 Ω** |
| CE/RE **HF 절편** | **≈28.7 Ω** | **≈13 Ω** |
| WE/CE **HF 절편** | ≈44.3 Ω | ≈43 Ω |
| **양극**(HF → 2 Hz) | ≈43.2 − 12.6 = **≈31 Ω**, 정점 −Im ≈7.2 @ Re ≈31 | ≈62 − 29.5 = **≈32.5 Ω**, 정점 −Im ≈8.5 @ Re ≈48 |
| **음극**(HF → 2 Hz) | ≈38.2 − 28.7 = **≈9.5 Ω** 인데 **−Im 이 이미 13 Ω 이고 상승 중** | ≈16.5 − 13 = **≈3.5 Ω**, 정점 −Im ≈2 |
| **음극 100 mHz** | Re **≈87**, −Im **≈45.5** ⇒ 실축 확장 **≥58 Ω**, **반원이 닫히지 않는다** | Re **≈19**, −Im ≈1 ⇒ **≈6 Ω, 닫힌다** |

`[인쇄]` 논문의 읽기:
> "(a) … shows a semicircle-like contribution of the cathode WE … **The Li-In CE
> contributes a very large impedance in the low frequency region. Between 10 Hz and
> 0.3 Hz predominantly blocking behavior is observed** as the imaginary component of
> the impedance increases, and **at very low frequencies >0.3 Hz additional resistance
> is observed.** These impedance contributions likely describe the **formation of an
> In-rich depletion layer and the sluggish Li⁺-ion transport through it** …
> In contrast, the cell with Li-In-SE composite (Fig. 5b) shows **purely resistive and
> overall insignificant CE contribution**."

⚠ **D2**: "at **very low frequencies >0.3 Hz**" — 앞 문장이 "Between 10 Hz and 0.3 Hz"
이므로 여기는 **<0.3 Hz** 여야 한다. **부등호가 뒤집혀 있다.**

### 7.1 ★★★ 우리가 한 합산 검사 (논문이 하지 않은 자기 검증) `[재현]`

3전극이 옳게 배선됐다면 `Z_WE/CE = Z_WE/RE + Z_CE/RE` 여야 한다.

| 검사 지점 | (a) foil | (b) composite |
|---|---|---|
| **HF 절편** | 12.6 + 28.7 = **41.3** vs **44.3** → **Δ ≈3.0 Ω (7 %)** | 13 + 29.5 = **42.5** vs **43** → **Δ ≈0.5 Ω (1 %)** |
| **2 Hz (Re)** | 43.2 + 38.2 = **81.4** vs **82.1** → **Δ ≈0.7 Ω (0.9 %)** | 16.5 + 62 = **78.5** vs **79** → **Δ ≈0.5 Ω (0.6 %)** |

★ **2 Hz 에서는 두 셀 다 1 % 안에서 합이 맞는다** — 16호가 `[인쇄]` "2E = 3E 합
(10 kHz 아래)" 으로 한 자기 검증과 **같은 성질의 확인**이고, **17호는 그것을 하지 않는다.**
우리가 대신 한다. ⚠ foil 의 **고주파 절편만 7 % 어긋나는데**, 이 셀은 음극 임피던스가
거대해서 3전극 고주파 아티팩트가 가장 크게 생길 조건이다 (10호가 경고한 축).

### 7.2 ★★★ 이 그림이 닫아 주는 것과 열어 놓는 것

★ **닫아 주는 것**: **양극 임피던스가 두 셀에서 같다** — ≈31 ↔ ≈32.5 Ω, **차이 5 %**.
⇒ **음극을 바꿔도 양극은 안 변했다.** Fig. 4a 의 **6.6 % 용량 차이와 Fig. 4b 의 35 %
율 차이는 전부 음극에서 온다.** `[해석]` 이것이 **우리 닻의 물음에 대한 가장 깨끗한
전극 분해 근거**다 — "겉보기 `LAM_PE` 처럼 보이는 것이 사실은 상대극" 인 경우가
**한 셀 안에서 실증**됐다.

⚠ **열어 놓는 것 두 개**:
1. **D14 — EIS 를 찍은 시점은 "충전 상태" 다.** 프로토콜(§3.5)상 EIS 직전에 셀은
   0.1 C 로 실험 용량의 **절반까지 충전**됐고(= 음극 **리튬화**) **5 h 이완**했다.
   그런데도 foil 의 음극은 **100 mHz 에서 닫히지 않는다.**
   `[해석]` **In-rich 고갈층이 다음 충전 + 5 h 이완으로 되돌려지지 않는다.**
   ⚠ 대안: 5 사이클 동안 쌓인 계면 열화. **둘을 가르는 관측이 없다**(G7).
   **논문은 이 순서를 적어 놓고 이 함의를 말하지 않는다.**
2. ★★ **RE 위치가 두 셀에서 뒤집혀 있다** `[재현]`: 분리막 저항의 배분이
   foil **12.6 : 28.7 = 30.5 : 69.5** · composite **29.5 : 13 = 69.4 : 30.6**.
   **총합은 41–43 Ω 로 5 % 안에서 같은데 배분이 정확히 뒤집힌다.**
   `[인쇄]` 제작은 "a copper wire **roughly through the middle**" 다.
   ⇒ **"roughly" 의 실측값이 30 % ↔ 70 % 다.** 직류 전위 측정에는 (RE 에 전류가 흐르지
   않으므로) 1차적으로 무해하지만, **§6.5 의 옴 보정이 셀마다 2.2 배 달라지는 이유**가
   바로 이것이고, **EIS 의 전극 귀속에도 들어간다.** 논문 무언급.

### 7.3 `[재현]` 면적 정규화 — 2전극과 3전극이 같은 셀이 아니다

- 2전극 HF 절편 ≈37 Ω × 0.7854 cm² = **≈29 Ω cm²**
- 3전극 HF 절편 ≈42 Ω × 1.1310 cm² = **≈47 Ω cm²**
⇒ **3전극 쪽이 ≈1.6 배 높다.** 후보 원인 셋 (전부 논문 무언급):
① **온도**(30 °C ↔ 실온) — LPSCl `E_a ≈ 0.35 eV` 를 가정하면 22 → 30 °C 만으로
   **≈1.4 배** (⚠ `E_a` 는 **우리 가정**, "room temperature" 는 **정의되지 않음**)
② **분리막 압착압**(500 ↔ 375 MPa)
③ Cu 선이 분리막을 가로지르는 것 · 하드웨어(PET/SS ↔ PEEK/WC)
`[해석]` 그런데 논문은 `[인쇄]` "the WE potential was controlled against the CE potential
**to reproduce the two-electrode cell experiments**" 라고 쓴다 — **reproduce 가 아니다.**
(**D4 · D5**)

## 8. §결론 — 논문이 스스로 말하는 것

> `[인쇄]` "Li-In **foil-type anodes, which are used in the vast majority of sulfide
> ASSB works**, showed **severe kinetic limitations** during rate performance testing.
> The collected data at high rates (in our case **already ≥ 1 C = 2.80 mA cm⁻²**) is
> **strongly dominated by the anode, making it impossible to observe the cathode
> behavior.**"
> `[인쇄]` "improper balancing can lead to the generation of undesirable Li-rich
> Li_xIn_y phases during charging, which **effectively reduce the cut-off voltage
> relative to Li/Li⁺ by at least 0.2 V**."
> `[인쇄]` "there is only a **narrow sweet spot at around 49 at% Li** content of the
> metal foil anode … This sweet spot furthermore will be **very susceptible to the
> preparation process**."
> `[인쇄]` "**Insufficient reproducibility, which is hardly reported in ASSB half-cell
> studies, at moderate C-rates can be easily explained by anode dominated data.**"
> `[인쇄]` "Likewise, **the deconvolution of half-cell impedance spectra e.g., when
> characterizing cathodic charge transfer phenomena, could be severely complicated by
> overlapping anode impedance.**"
> `[인쇄]` "We **strongly recommend the preparation of Li-In-SE composite anodes** …
> and prevent the possibility of **misinterpretation of anodic effects as cathodic
> effects** in typical half cells."

★★★ **마지막 두 인용은 이 위키의 두 페이지에 그대로 꽂힌다**:
- "**deconvolution … severely complicated by overlapping anode impedance**"
  → [[drt-peak-count-nonidentifiability]] 와 [[assb-lampe-contact-product-degeneracy]]
  (16호의 `j₀ · ε_CAM / r_CAM` 배정 문제에 **음극 오염**이라는 항이 하나 더 붙는다)
- "**misinterpretation of anodic effects as cathodic effects**"
  → 닻 [[assb-contact-loss-vs-lampe]] 의 물음을 **JES 지면이 한 문장으로 인쇄한 것**이다.
  8호(Li 2026)가 `[인쇄]` "distinguishing contact loss from ordinary electrochemical
  aging" 을 요구로 적은 것에 이은 **두 번째 인쇄 요구**이고, 이쪽은 **1차 측정을 동반한다.**

⚠ 그리고 **논문 스스로 붙인 한계**:
> `[인쇄]` "This result is **contrary to the findings of Wang et al.**, who identified
> Li content as low as **14.3 at%** as optimal … We **suspect** that methodic
> differences could explain the differing findings, since our study was done with
> **considerably higher rates and lower stack and assembly pressure**."

⚠ **G8**: 압력을 불일치의 설명으로 꺼내면서 **Wang 의 압력값을 적지 않고**, 자기 압력은
**한 점(50 MPa)** 이다. **압력 스윕 0.** 이 문장은 **측정 없는 압력 귀속**이다.

## 9. SI (2쪽) 전수

### 9.1 Fig. S1 — LiIn 분말 BSE-SEM 4 패널 【그림 본 것】
`[인쇄]` 캡션: "Field-emission scanning electron microscopy images of the LiIn alloy.
… **Carl Zeiss Crossbeam 550** … **backscatter electron detector**. The **lighter
colors are associated with a higher backscatter intensity i.e. In-rich phases**."

`[도표]` 스케일바 **100 µm · 20 µm · 5 µm · 1 µm**. 입자는 **20–100 µm**의 거친 파편
(본문 `[인쇄]` 와 일치). 5 µm·1 µm 패널에서 **밝은 In-rich 영역이 0.3–2 µm 크기로
조밀하게 흩어져 있고** `[재현]` 눈대중 면적 분율 **≈10–20 %** (⚠ 논문은 정량하지 않는다).
`[인쇄]` "ca. **1 μm** large In-rich domains … due to the **incomplete mechanic alloying
via low-energy manual mixing**."

⚠ **D10**: 그 뒤 문장이 `[인쇄]` "However, the **homogeniety is still considered
significantly higher than the Li-In foil**" 인데 — **foil 의 근거는 광학 사진(Fig. 2),
powder 의 근거는 BSE-SEM(Fig. S1)** 이다. 배율이 10²–10⁴ 배 다르고 대비 원리가 다르며
**양쪽 다 정량값이 0** 이다. `[해석]` **비교 가능한 척도가 없는 비교다.**

### 9.2 Fig. S2 — 셀 배선 모식도 【그림 본 것】
`[도표]` (a) **2E**: CE 와 RE 단자를 **둘 다 Li-In 음극에** 물린다(표준 2전극 결선),
WE = 복합양극.
`[도표]` (b) **3E, 두 단계**:
- **왼쪽(도금 전)**: **Cu 선이 WE(빨강)**, **Li-In 음극이 CE + RE**
  ⇒ ★★ **RE 용 Li 는 Li-In 음극에서 꺼내 온다.**
- **오른쪽(본실험)**: WE = 복합양극, CE = Li-In 음극, **RE = Li 도금된 Cu 선**

★★ `[해석]` **RE 는 LPSCl 안에 박힌 Li 금속**이다. 그런데 같은 논문 서론이
`[인쇄]` Li 금속은 "**high reactivity towards sulfide SEs**²²" 때문에 CE 로 거의 안
쓰인다고 적는다. ⇒ **이 논문이 불안정하다고 말한 재료가 기준극이다.**
⚠ **그 안정성을 재지 않는다** — RE 표류 검사 0 · 재도금 0 · 대칭 검사 0.
**16호의 문제(기준극 안정성을 인용으로 가정)가 다른 형태로 반복된다.**

★★★ **다만 이 편에는 16호에 없던 암묵적 상한이 있다** `[재현]`:
**복합 셀의 `E_CE` 가 Fig. 4c 의 20 h 전 구간에서 0.61–0.63 V 밖으로 나가지 않는다.**
⇒ **(RE 표류 + 음극 과전압 + 옴) 의 합이 20 h 동안 ≈20 mV 를 넘지 않는다.**
**이 계보 최초의 기준극 표류 상한**이다. ⚠ 세 항이 **상쇄될 수도** 있으므로 엄밀히는
**합의 상한**이지 RE 단독의 상한이 아니다.

### 9.3 Table S1 — 첫 사이클 쿨롱 효율 (전수)

| 음극 | 첫 사이클 CE (%) |
|---|---:|
| Foil – 45 at% | **85.3** |
| Foil – 47 at% | **85.0** |
| Foil – 49 at% | **84.8** |
| Foil – 50 at% | **81.8** |
| Powder – 36 at% | **85.0** |
| Powder – 40 at% | **84.9** |
| Powder – 44 at% | **84.4** |
| Powder – 47 at% | **82.0** |
| Composite – 40 at% + 20 % SE | **82.7** |
| Composite – 40 at% + 40 % SE | **84.9** |

**오차 0 · 반복 0 · 유효숫자 3.**

`[인쇄]` 논문의 읽기: foil·powder 모두 "**decreasing trend with increasing Li content**",
그리고 `[인쇄]` "**might be an indication of increased SE degradation at the interface
of Li rich anodes and the SE**".

⚠⚠ **D11 — 이 "추세" 는 산포 대용보다 작다** `[재현]`:
- foil 45 → 49 at% 의 전 구간 변화 = **85.3 → 84.8 = 0.5 %p**
- **같은 Li 함량(40 at%)** 의 복합 두 셀 = **82.7 ↔ 84.9 = 2.2 %p**
  (논문 스스로 이 둘의 율 성능 차이를 `[인쇄]` "**slight**" 라고 부른다)
⇒ **가장 가까운 산포 대용이 "추세" 의 4.4 배다.** 반복이 0(G3)이므로 **0.5 %p 추세에
대조할 오차 바닥이 논문 안에 없다.** 살아남는 것은 **50 at%(81.8)와 powder-47(82.0)의
≈3 %p 낙차**뿐이고 그것도 2.2 %p 바닥의 1.4 배다.
`[해석]` **"Li 가 많을수록 SE 분해가 는다" 는 이 데이터로 주장될 수 없다.** (그리고 그
주장은 XPS·XRD 같은 독립 관측이 0 이라(G7) 다른 채널로도 받쳐지지 않는다.)

## 10. 어휘 전수 계수 (NFKC 정규화 · 대소문자 구분 · 표지 1쪽 제외 · 본문 p.2–8 + SI)

### 10.1 ★ Q4 — 유일성·식별성 어휘: **전부 0**

`identifiab*` **0** · `uniqu*` **0** · `ill-posed` **0** · `regulari[sz]*` **0** ·
`uncertaint*` **0** · `confidence` **0** · `error bar` **0** · `standard deviation` **0** ·
`condition number` **0** · `Fisher` **0** · `bootstrap` **0** · `Bayes*` **0** ·
`posterior` **0** · `degenerac*` **0** · `overfit*` **0** · `Kramers` **0** · `Kronig` **0** ·
`cross-valid*` **0** · `objective function` **0** · `initial guess` **0** · `multi-start` **0** ·
**`n =` 0** · `sensitiv*` **1**(양극 `R_ct` 의 SOC 민감도, 고주파 산포를 넘기는 문장).

### 10.2 ★★ 그리고 **적합 어휘 자체가 0 이다** — 이것이 17호의 성질이다

`fit`/`fitted`/`fitting` **0** · `equivalent circuit` **0** · `ECM` **0** · `CPE` **0** ·
`capacitance` **0** · `double layer` **0** · `DRT` **0** · `distribution of relaxation` **0** ·
`simulat*` **0** · `machine learning` **0**. `model*` **4 회**(전부 "model cell"/"model
half-cells" — **계산 모델이 아니다**). `charge-transfer` **2**(정성).

★★★★ `[해석]` **Q4 의 열 번째 성질 — "인쇄로 사양했다".**
계보: 안 쟀다(1–7) → 이름만(8) → 지문이 자기 표에(9) → 분야가 명제로(10) → 재료만(11)
→ 0(12·13) → 역문제가 없어 자리가 없음(14) → 추정기가 없어 대상이 없음(15) →
**밟고 지나갔다(16)** → **17호: 역문제가 눈앞에 있는데 `[인쇄]` "beyond the scope of
this study" 로 명시적으로 사양했다.**
★ 그리고 **그 사양이 이 편의 결론을 오히려 방어한다** — 결론("음극이 율 제한")은
**적합의 출력이 아니라 전압계 판독**이다. **축퇴할 자리가 없다.**
14호도 적합이 없었지만 14호는 **귀속이 가정**이었고(ΔS 변화 → "비균질"),
**17호는 귀속이 배선**이다(세 번째 전극이 직접 읽는다). ⚠ 단 그 배선에도 오염원이
둘 있고(§6.5 옴 · §9.2 RE 안정성) **논문은 둘 다 다루지 않는다.** **여전히 0/17.**

### 10.3 우리 축 어휘

`contact` **6**(전부 정성) — `contact loss` **1**(서론의 문헌 열거) · `contact area` **1** ·
`contact surface` **1** · `percolat*` **1**("well-**percolated** composite anode") ·
`tortuos*` **0** · `poros*` **0** · `void` **0** · `θ` **0**.
`LAM` **0** · `LLI` **0** · `SOH` **0** · `aging/ageing` **0** · `cycle life` **0** ·
`degrad*` **4**(율시험 3 회 사이 + SE 분해 추정).
`pressure` **7** · `MPa` **13** · `stack pressure` **2** · `hysteres*` **0**.
`indium/Indium` **7** · `Li-In` **95**(본문 92 + SI 3) · `reference potential` **4**.
`OCV` **0** · `open circuit` **0** · `GITT` **0** · `half-cell` **12**.
`dead li`/`isolated`/`plating(고립)` **0** · `dendrit*` **2**(서론, Li 금속 회피 사유).
⚠ 오검출 방지 확인: `flam*` 0 · `Soh` 0 (LAM→flammable, SOH→Sohn 오검출 없음).

## 11. 우리 축 Q1~Q8 — 이 편의 판정

| 축 | 판정 |
|---|---|
| **Q1 접촉 손실 정량** | **없다 (17/17).** 그런데 형태가 새롭다 — `[인쇄]` "the Li depletion is primarily a function of the **contact surface between the SE and LiIn**" 로 **인과 변수로 지목**하고, `[인쇄]` "high **effective contact area** to the separator" 로 **처방의 근거**로 삼으면서 **값·단위·측정법이 0** 이다. 16호는 이름 붙이고 기하로 계산해 **1 로 못 박았고**(θ≡1), 9호는 **적합했고**(0.4938), **17호는 이름만 붙인다.** 그리고 이것은 **양극이 아니라 음극/분리막 계면**의 접촉이다 — 축이 다르다 |
| **Q2 독립 관측** | ★★★ **있다 — 계보 두 번째 전극 분해, 그리고 첫 "전위" 채널.** 16호가 임피던스를 전극별로 갈랐다면 **17호는 전위를 전극별로 가른다**(`E_WE`·`E_CE`·`E_cell` 시계열). ★ 결정적 대조: **양극 임피던스가 두 음극에서 ≈31 ↔ ≈32.5 Ω 로 같다** ⇒ 용량·율 차이가 **전부 음극**. ⚠ **형태학·화학 관측은 0**(G7) — Fig. 2 의 광학 사진 2 장이 전부다 |
| **Q3 라벨 층위** | ★★ **새 층위: `measured-potentiometric`.** 이 계보의 라벨 층위 계보에 없던 것 — 적합(9·16호)도, 형태학(4·14호)도, 열역학 도함수(14호)도, 역변환(11호)도 아니고 **기준극 대비 전압계 판독**이다. ⚠ 오차막대 0 · 반복 0 · 조건당 셀 1 · `n =` 0 회 · 데이터 가용성 문장 0. 그리고 **기준극 자체가 검증되지 않았다**(G1·§9.2) |
| **Q4 유일성** | **0 / 17.** 열 번째 성질 = **"인쇄로 사양했다"**(§10.2) |
| **Q5 Li-In 기준 전위** | ★★★★ **이 계보에서 가장 크게 채워진 칸이고, 이 편의 본체다.** §13 전체 |
| **Q6 압력** | **한 점.** 운전 `[인쇄]` **ca. 50 MPa**(2E) / **50 MPa**(3E). 제작 **500 MPa**(3E 분리막만 375). **스윕 0 · 이력 0(`hysteres*` 0) · 계측 0 · 압력→용량 0.** ★ 유일한 개념 기여는 **부정적**이다 — 타 논문과의 불일치를 `[인쇄]` "lower stack and assembly pressure" 로 설명하면서 **상대 압력값도 자기 스윕도 없다**(G8) |
| **Q7 dead Li** | **해당 없음** (Li-In 음극). `dead`·`isolated` 0. `dendrit*` 2 는 Li 금속을 **피하는 사유**로만 |
| **Q8 화학·OCP** | ★ **있다.** **단결정 NCM811** : LPSCl : VGCF = **73.2:24.0:2.8 wt%**, `[재현]` **19.1 mg cm⁻² · 2.80 mAh cm⁻² · 공칭 200 mAh g⁻¹**. 창 **3.00–4.30 V vs Li⁺/Li (2.38–3.68 vs LiIn)**, `[도표]` **전 구간 기울기 있음**. ★ **V–Q 곡선 11 장**(Fig. 1a–c 10 + Fig. 4a) — 10·11호가 0 장이었던 칸. ⚠ **OCV·GITT 0** — 곡선은 전부 0.1 C **pseudo-OCV** 다. 접촉 손실 = LAM 안/밖: **미언급** |

**채움표 누적: 16편 ≈9.5 → 17편 ≈10.0** (**Q5 +0.5** — 이 칸이 처음으로 논문의 본체가
됐다). **Q1·Q4 는 그대로 0.**

## 12. ★★★ 곱 축퇴 검사 — 16호 처방의 첫 적용

16호 digest 와 [[assb-lampe-contact-product-degeneracy]] 가 세운 처방은 이것이었다:

> `R_CT·C_dl` 은 접촉 면적이 소거된 고유 시상수이고 `C_dl` 단독은 면적에 비례한다.
> **둘을 같이 보고하면 `θ` 와 `j₀` 가 갈린다.**

### 12.1 판정: **적용 불가 — 그리고 그 이유가 정보다**

| 처방 입력 | 17호에 있나 |
|---|---|
| `R_CT` | **없다** (`fit*` 0 회) |
| `C_dl` / `Q_DL` / `CPE` | **없다** (`capacitance`·`CPE` 0 회) |
| 등가회로 | **없다** (`equivalent circuit`·`ECM` 0 회) |
| 면적 인자 `a_V`/`θ` | **없다** (기하 계산 0) |

`[인쇄]` "Detailed quantitative analyses and **modelling of the impedance spectra are
beyond the scope of this study**."

⇒ **처방의 첫 적용은 "입력이 없다" 로 끝난다.** 세 편의 실패 양식이 전부 다르다:
**9호** = 곱을 적합했다 · **16호** = 곱 위에 서서 한쪽 끝을 골랐다(`θ≡1`) ·
**17호** = **곱을 만들지 않았다**.
`[해석]` **역설적으로 17호가 가장 안전하다** — 배정하지 않았으므로 잘못 배정할 수 없다.
대신 **정량이 0 이라 우리가 가져갈 숫자도 없다.**

### 12.2 ★★ 그래도 이 편에 곱 축퇴가 **있다** — 다른 자리에서, 문장으로

논문의 인과 주장은 **같은 조작을 두 이름으로 부른다**:

> ① `[인쇄]` "the Li depletion is primarily a function of the **contact surface between
>    the SE and LiIn**"
> ② `[인쇄]` "the major advantage of Li-In powder is that it can be mixed with the soft
>    sulfide powder to produce a … **well-percolated composite anode with high
>    effective contact area to the separator**"
> ③ `[인쇄]` "By increasing the sulfide content from 20 wt% to 40 wt% a further slight
>    performance increase is observed, which confirms that the **effective ionic
>    conductivity of the Li-In anode** plays an important role"

★★ **SE 분말을 넣는 조작 하나가 (i) LiIn↔SE 접촉 면적과 (ii) 음극 유효 이온전도도를
동시에 올린다.** 둘을 따로 움직인 실험이 **없다.** ⇒ **곱은 아니지만 공변(co-varying)
두 인자이고, 데이터는 그 둘의 어떤 조합만 본다** — 우리 곱 축퇴와 **같은 구조**다.

★★★ **그리고 그 배정이 숫자로도 안 받쳐진다** `[재현]`:
- 2전극 총 임피던스: composite **20 % SE ≈36 Ω → 40 % SE ≈27 Ω**, **Δ ≈9 Ω (−25 %)**
- 그런데 `[도표]` Fig. 5b 에서 **40 % SE 복합 음극의 임피던스 전체가 ≈6 Ω** 이다
⇒ **Δ 9 Ω 을 음극에 다 줄 수 없다.** (20 % SE 의 음극이 15 Ω 이었다면 가능하지만
**3전극은 40 % 쪽만 쟀다** — G6.) 남는 통로는 **양극/분리막의 셀 간 산포**이고,
§7.2 에서 본 대로 **이 실험의 셀 간 기하는 분리막 저항 배분이 30 % ↔ 70 % 로 뒤집힐
만큼 흔들린다.**
⇒ ③의 "confirms" 는 **전극 분해 근거가 0 이다.**

⚠ **단서 — 이 축퇴는 이 편의 주 결론을 흔들지 않는다.** 주 결론(음극이 율 제한이고
`E_CE` 가 0.7 V 움직인다)은 **면적/전도도 배정과 무관하게** 전압계 판독에서 나온다.
흔들리는 것은 **"왜 복합이 더 좋은가" 의 기구 설명**뿐이다.

## 13. ★★★★ Q5 — "평탄 전위" 의 실제 폭 (이 편의 최대 수확)

### 13.1 실측 표

| 상태 | `E_CE` vs Li⁺/Li | 0.62 V 로부터 | 출처 |
|---|---:|---:|---|
| 문헌 인용 (쿨로메트릭 적정, ref 26) | **0.62** | — | `[인쇄]` |
| **개방회로 실측** | **없다** | — | **G1** |
| 0.1 C 충전 (두 음극 모두) | **0.61** | **−10 mV** | `[인쇄]` |
| 0.1 C 방전 초기 (두 음극 모두) | **0.63** | **+10 mV** | `[인쇄]` |
| 0.1 C 방전 종료, **복합** | **0.63** | +10 mV | `[도표]` Fig. 4c |
| 0.1 C 방전 종료, **foil** | **≈1.0** | **+≈0.4 V** | `[도표]` Fig. 4c (논문은 수치 없음) |
| CA 초기(≈16 mA cm⁻²), **복합** | **≈0.9** | +0.28 V | `[인쇄]` |
| CA 초기, **foil** | **0.7 ↔ 1.3 요동** | +0.08 … +0.68 V | `[인쇄]` |
| CA 정상(전류 → 0.02 C), **복합** | **0.64** | **+20 mV** | `[인쇄]` |
| **CA 정상, foil** | **1.30–1.40** | **+0.68 … +0.78 V** | `[인쇄]` + `[도표]` |
| **과리튬화** (foil 50 at% · powder 44/47 at%) | **≈0.42** | **−0.2 V** | `[인쇄]` |

★★★★ **전체 폭: 0.42 → 1.40 V, 즉 ≈0.98 V.** 그리고 **양쪽 끝이 모두 "정상적인
Li-In 음극" 이라고 이름 붙은 셀에서 나온다.**

### 13.2 ★★★ 세 가지를 갈라서 읽어야 한다

1. **2상역 안, 저율, 좋은 음극** → **±10–20 mV.** 그리고 §6.5 에서 본 대로
   **그 ±10 mV 는 CE–RE 옴 강하(≈9 mV)와 구별되지 않는다** ⇒ **진짜 열역학 평탄은
   적어도 ±10 mV 안이고, 이 실험은 그보다 좁게 재지 못한다.**
   `[해석]` **우리 닻의 "ASSB 음극은 평탄" 전제는 이 조건에서 성립한다 — 그리고 이 편이
   그것을 처음으로 Li 금속 기준극으로 확인했다.**
2. **Li-rich 쪽으로 나가면 −0.2 V** (Li₅In₄ / Li₃In₂). 이 이동은 **충전 중에 생긴다** —
   양극이 넘겨준 Li 를 음극이 받으면서. `[인쇄]` "ca. **50 mAh g⁻¹**" 부터 곡선이 갈라진다.
   ⇒ **2전극에서 이것은 "용량이 40 mAh g⁻¹ 작다" 로 보인다** (§4.1).
3. ★★★★ **In-rich 쪽으로 나가면 +0.7 V 이상이고, 전류가 0 이어도 안 돌아온다.**
   §6.5 의 계산이 이것의 근거다 — 종료 기준 전류에서 옴은 **≈2 mV**, 관측은 **+730 mV**.
   ⇒ **과전압이 아니다.**

### 13.3 ★★★★ 그래서 우리 계획에 무엇이 붙는가

★ **닻 카드의 "아직 모르는 것 2"("Li-In 기준 전위가 얼마나 안정한가")에 대한 답**:

> **평탄한 것은 조성이 2상역 안에 있고 *동시에* 분리막 접촉면의 LiIn 이 고갈되지 않은
> 동안뿐이다. 두 조건 중 하나가 깨지면 기준이 −0.2 V ~ +0.7 V 움직이고, 그 이동은
> 완전지 OCV 를 통째로 미는 것이라 `LLI` 와 모양이 같다.**

★★ **그리고 이 편이 주는 새 경고 두 개**:

**(가) 이동의 방향이 충전과 방전에서 반대다.**
- 충전 중 과리튬화 → 기준 **내려감**(−0.2 V) → 양극이 **덜 충전**된다(4.3 → 4.1 V)
- 방전 중 고갈 → 기준 **올라감**(+0.4 ~ +0.7 V) → 양극이 **덜 방전**된다(3.0 → 3.4 V)
⇒ `[해석]` **둘이 같이 있으면 충전 용량과 방전 용량이 서로 다른 이유로 줄고, 그 둘의
비(= 쿨롱 효율)는 두 이동의 차로 오염된다.** Table S1 의 CE 를 `LLI` 대리로 읽으면
안 되는 이유가 여기 있다 — **6호(Lee 2020)에서 "CE 로 `LLI` 를 센다" 가 10 배 어긋났던
것**([[anode-free-li-inventory-accounting]])에 **기준 전위라는 오염원이 하나 더 붙는다.**

**(나) 저율 RPT 는 이것을 줄이지만 지우지 못한다.**
`[재현]` 0.1 C 에서 **6.6 %** · CA(초기 ≈5.7 C)에서 **≈35 %**. 5 배 차이지만 **0 이 아니다.**
⇒ **율을 낮춰 `η(i) → 1` 로 보내는 우리 분리 시험**([[assb-apparent-capacity-decomposition]])
**이 기준 전위 이동은 지우지 못한다** — 그것은 `η` 가 아니라 **축의 원점**이기 때문이다.
`[해석]` **3항 분해에 네 번째 항이 필요하다**: `Q_apparent = θ_AM · Q_material(ΔE_cut) · η(i)`
에서 **컷오프 자체가 `E_CE(i, x_Li, 제조법)` 의 함수**다.

### 13.4 ★★★ 16호와의 대질 — 같은 결론의 두 축

| | **16호 Ramanayagam 2026** | **17호 Yanev 2024** |
|---|---|---|
| 기준극 | 리튬화 **Au/W μ-RE** ∅25 µm | **Li 금속** 도금 Cu 선 ∅400 µm |
| 기준극 안정성 | **안 쟀다**(인용 2 건) | **안 쟀다** — 단 `[재현]` **합의 상한 ≈20 mV/20 h** |
| In–Li 평탄값 | `[도표]` **0.58 ↔ 0.47 V** (두 셀, Δ110 mV) | `[인쇄]` **0.61/0.63** (한 셀) · **0.42–1.40 V** (조건 전체) |
| 평탄 구간 안에서 움직이는 것 | ★ **음극 DRT 봉우리 18.6 → 1.2 (≈15 배)** | ★ **`E_CE` 자체가 0.61 → 1.35 V** |
| 운전 압력 | **97 / 389 MPa** | **50 MPa** |
| 음극 임피던스 | `[인쇄]` **4 ↔ 9 Ω cm²** (389 ↔ 97 MPa) | `[재현]` **≈6.8 Ω cm²**(복합) · **≥66 Ω cm²**(foil, 미폐) |

★★★★ `[해석]` **두 편을 겹치면 하나의 설명이 나온다 — 그리고 어느 편도 그것을 쓰지 않는다.**
16호의 음극은 **순수 In 박**이고 Li 가 **분리막 쪽에서 전기화학적으로** 들어온다 ⇒
**LiIn 상이 필요한 바로 그 자리(분리막 계면)에 생긴다.** 17호의 foil 음극은 **Li 박을
집전체 쪽에서 기계적으로** 눌러 붙인 것이다 ⇒ `[인쇄]` "most of the generated Li-In
phases remain embedded on the **current collector side**".
⇒ **같은 "In 박 음극" 인데 LiIn 이 생기는 위치가 반대다.**
그러면 16호가 `x_Li` **0.05–0.28**(17호가 "치명적" 이라 한 것보다 훨씬 Li-poor)인데도
음극 임피던스가 **4–9 Ω cm²** 로 작은 것이 설명된다.
⚠⚠ **다만 압력이 2–8 배 다르고**(50 ↔ 97/389 MPa) **SE·조성·전류·SOC 가 전부 다르다.**
⇒ **이것은 두 편을 가로지르는 가설이지 어느 편의 결론도 아니다.** 검증 실험은 명백하다:
**같은 셀에서 Li 박을 분리막 쪽/집전체 쪽으로 뒤집어 3전극으로 재는 것** — 그리고
17호가 `[인쇄]` Sedlmeier 가 그것을 시도했다고 적는다(ref 21, Li 쪽을 분리막으로 돌리면
**저장고는 커지지만 SE 와의 계면 안정성이 나빠진다**). **후속 2순위.**

## 14. 어긋남·의심 원장 (15 건)

| # | 무엇 | 좌표 |
|---|---|---|
| **D1** | ★★ **그림 번호 오기** — 분말 음극 임피던스를 `[인쇄]` "(**Fig. 1f**)" 라 부른다. 캡션상 임피던스는 **(g)–(i)**, 분말 임피던스는 **Fig. 1h** 다. 같은 쪽에서 `1f` 가 두 번 나오고 한 번은 틀렸다(복합 쪽 `1f` 는 맞다) | p.5 |
| **D2** | ★ **부등호 반전** — `[인쇄]` "at very low frequencies **>0.3 Hz**" 는 **<0.3 Hz** 여야 한다 (앞 문장이 "Between 10 Hz and 0.3 Hz") | p.7 |
| **D3** | ★★ **Li 질량 범위가 자기 조성 라벨과 안 맞는다** `[재현]` — `[인쇄]` In **75 mg** + Li **3.6–4.4 mg** ⇒ (M_Li 6.94 · M_In 114.82) **44.3–49.3 at%**. 보고 라벨은 **45–50 at%**. 50 at% 에는 **4.53 mg** 이 필요하다. ★ 논문 스스로 `[인쇄]` "steps of about **2 at%** … had a significant impact" 라고 쓰므로 **0.7 at% 장부 오차 = 그 단차의 35 %** | p.3 ↔ p.3–4 |
| **D4** | ★★ **2전극 30 °C ↔ 3전극 "room temperature"** 인데 3전극의 목적이 `[인쇄]` "to **reproduce** the two-electrode cell experiments" 다. `[재현]` 면적 정규화 HF 저항 **≈29 ↔ ≈47 Ω cm² (1.6 배)**, LPSCl `E_a ≈0.35 eV` 가정 시 22→30 °C 만으로 **1.4 배**. 무언급 | p.3 |
| **D5** | ★ **3전극 분리막은 375 MPa, 2전극은 500 MPa** 로 눌렀다 — 역시 "reproduce" 주장과 어긋난다. 무언급 | p.3 |
| **D6** | ★★★ **3전극의 foil 셀(40 at%)은 2전극에서 시험한 어떤 foil 셀(45/47/49/50 at%)도 아니다.** 논문이 찾은 sweet spot 은 **49 at%** 인데 **권장 조성은 전극 분해로 검증된 적이 없다.** (의도는 명시돼 있다 — 문제는 결론이 3전극 근거를 foil 일반으로 확장한다는 것) | p.6 ↔ p.3–4 |
| **D7** | ★★ **Fig. 2 의 시편은 어느 셀의 것도 아니다** — `[인쇄]` "**10 mm diameter in a 13 mm die**"(측면 유동 허용) ↔ 실제 셀은 ∅10/∅12 mm 몰드(**측면 구속**). In 이 13 mm 로 퍼졌다는 관측 자체가 그 기하의 산물인데 실제 셀의 In-rich 층 논거로 쓰인다. 무언급 | p.5 |
| **D8** | ★★ **"ca. 50 % SOC" 의 자기 모순** — 충전은 `[인쇄]` "up to **half of the experimental capacity**"(셀마다 140–200 mAh g⁻¹ 로 다르다) 인데 캡션은 `[인쇄]` 공통 "ca. 50% SOC". 그리고 고주파 산포를 `[인쇄]` "charge transfer resistance … very sensitive to the **state of charge**" 로 넘긴다. ⇒ **그 설명이 참이면 SOC 가 안 맞춰졌다는 뜻이고, 맞춰졌다면 그 설명이 안 된다** | p.4 ↔ p.3 |
| **D9** | ★ **50 at% 셀의 EIS 만 기준축이 다르다** — 그 셀의 기준극은 `[인쇄]` 0.62 → ≈0.42 V 다. "3.2 V vs Li-In" 은 **≈3.62 V vs Li** 이고 다른 셀의 3.82 V 와 **0.2 V 다르다.** 논문은 **Fig. 1a 에서는 이 계산을 하고(4.3→4.1 V) Fig. 1g 에서는 하지 않는다** | p.4 |
| **D10** | ★ **균질성 비교에 공통 척도가 없다** — foil = **광학 사진**(Fig. 2), powder = **BSE-SEM**(Fig. S1), 배율 10²–10⁴ 배 차이, 양쪽 정량 0. 그런데 `[인쇄]` "significantly higher" | p.5 ↔ SI p.1 |
| **D11** | ★★ **Table S1 의 "추세" 가 산포 대용의 1/4.4** `[재현]` — foil 45→49 at% **0.5 %p** ↔ 같은 40 at% 복합 두 셀 **2.2 %p**. 반복 0 이라 오차 바닥이 없다. 그 위에 `[인쇄]` "increased SE degradation at the interface of Li rich anodes" 라는 **기구 주장**이 얹힌다(독립 관측 0) | SI p.2 ↔ p.4–5 |
| **D12** | ★★ **인용의 일반화** — `[인쇄]` "Prior impedance studies … have **established** that higher frequencies are associated with cathode effects and lower frequencies with anode effects.³²" 인데 **ref 32 = 우리 10호 Vadhva 2021** 이 실제로 인쇄한 것은 `[인쇄]` "full devices using a **LMA** … assign the SE\|cathode interface as the **lowest** frequency arc, while those utilising an **In–Li** anode assign this to the SE\|anode interface" + `[인쇄]` "highlights the need for thorough EIS studies on a **system-by-system basis**". ⇒ **원전은 "보편 규칙이 없다"고 쓰고 17호는 "확립됐다"고 옮긴다.** ⚠ **17호의 셀이 In–Li 이므로 결론 자체는 원전과 정합**이고 Fig. 5 가 자기 셀에서 실증한다. **우리 위키의 원전 대조 두 번째 사례**(15호 이후) | p.4 ↔ `raw/papers/vadhva2021_eis-for-assb-theory-methods.md` |
| **D13** | ⚠ **Fig. 3 이 두 기원을 합친다** — In-rich 층이 **제조 기원**(Fig. 2, 불완전 합금화)인지 **방전 기원**(Fig. 3 "Fast discharge")인지 가르는 실험이 없다(G7). 본문은 `[인쇄]` "aggravate" 로 겹치지만, **그 분기가 이 논문의 처방이 딛는 자리다** | Fig. 2 ↔ Fig. 3 |
| **D14** | ★★ **EIS 는 "충전 상태 + 5 h 이완" 에서 쟀는데 foil 음극이 여전히 막혀 있다** — `[도표]` Fig. 5a 의 CE/RE 가 100 mHz 에서 닫히지 않는다(실축 ≥58 Ω). `[해석]` 고갈층이 다음 충전과 5 h 이완으로 안 돌아온다(또는 5 사이클 계면 열화). **논문은 순서를 적어 놓고 함의를 말하지 않는다** | p.3 ↔ Fig. 5a |
| **D15** | ★★ **RE 도금 전하가 음극에서 나오는데 조성은 "40 at% 고정" 이라고 쓴다** `[재현]` — `[인쇄]` "110 μA cm⁻² for **15 h**" (Fig. S2b: 도금 중 **Li-In 이 CE**). 셀 면적 기준이면 **1.87 mAh**, foil 음극 Li 재고(4.4 mg = **17.0 mAh**)의 **11 %** ⇒ **40.3 → 37.5 at%**. 복합 셀은 Li-In **72 mg** ⇒ Li 재고 **10.8 mAh**, 같은 전하가 **17 %** ⇒ **40 → 35.5 at%**. **두 셀이 서로 다른 만큼 줄어드는데 둘 다 "40 at% 고정"** 이다. ⚠ **기준 면적 미명시**(G10) — Cu 선 표면(≈0.15 cm²)이면 효과가 8 배 작다 | p.3 ↔ SI Fig. S2b |

## 15. 이웃 — 이 위키의 다른 편들과의 관계

- **10호 Vadhva 2021 = 이 편 ref 32.** D12 (인용 일반화). ★ **그리고 반대 방향의
  선물이 있다**: 10호가 재인용으로 적었던 `[인쇄]` "during discharge the **anode
  interface resistance increases** … ascribed to the **degree of lithiation of the
  In–Li alloy anode, which becomes more In-rich during discharge**" 를,
  **17호가 자기 셀에서 전위 채널로 1차 측정한다.** ⇒ 우리 Q5 경고(#2, "`R_anode(N)`
  에서 노화분과 SoC 분이 안 갈린다")에 **1차 근거가 붙었다.**
- **16호 Ramanayagam 2026.** §13.4 전체. **같은 In 계 음극, 다른 기준극, 다른 압력,
  같은 결론의 두 축**(동역학 / 전위).
- **4호 Shi 2020.** 4호가 `[인쇄]` "1.4–3.7 V vs In (2–4.3 V vs Li/Li⁺)" 로 **오프셋
  0.6 V 를 고정 가정**하고, 음극 `R_LF` 가 50 사이클에 `[도표]` ≈157 배로 자란 것을
  **열화**로 읽었다. ⇒ **17호는 그 오프셋이 신품 상태에서도 제조법만으로 0.74 V
  움직인다는 것을 보인다.** 4호의 노화 귀속에 대한 **두 번째 경고**(10호에 이어).
- **6호 Lee 2020.** CE 로 `LLI` 를 세는 통로에 **기준 전위 오염**이 추가된다(§13.3 가).
- **9호 Huo 2025.** `A_eff·ε_p/R_s` 곱 축퇴. 17호는 **적합을 안 해서 그 자리에 서지
  않는다**(§12.1) — 대신 **면적 ↔ 전도도 공변**이라는 다른 형태를 문장으로 갖는다.
- **8호 Li 2026.** `[인쇄]` "distinguishing **contact loss** from ordinary
  electrochemical aging" 요구 ↔ 17호 `[인쇄]` "misinterpretation of **anodic effects as
  cathodic effects**". **두 번째 인쇄 요구이고 이쪽은 1차 측정을 동반한다.**
- **ref 8 = Koerver 2017 (*JMCA* 5, 22750).** 우리 위키에서 여러 번 후속 후보로 올랐던
  논문인데, 17호는 그것을 **interphase formation** 으로만 인용한다(접촉 손실 아님).

## 16. 이 digest 가 주장하지 않는 것

- **논문의 결론이 틀렸다고 주장하지 않는다.** 주 결론(foil Li-In 음극이 율 제한이고
  Li-In-SE 복합이 그것을 완화한다)은 **전극 분해 전위 측정**이 떠받치고, 그 측정은
  이 계보에서 가장 직접적인 종류다. 비판은 **n=1 · 옴 분리 · 기준극 검증 · 배정**에 있다.
- **"기준 전위가 1.35 V 로 옮겨 갔다" 고 단정하지 않는다.** 확실한 것은 **"옴이 아니다"**
  (§6.5, 옴 몫 0.2 %)까지다. **평형 전위라는 해석에는 G2(이완 곡선)가 필요하고 없다.**
- **0.98 V 라는 "폭" 을 Li-In 물질의 성질로 옮기지 않는다.** 그것은 **조성 ×
  제조법 × 율** 의 폭이지 2상역의 열역학 폭이 아니다. **열역학 폭은 이 편에서 ±10 mV
  안이고 그보다 좁게 재지 못했다.**
- **압력을 결론에 넣지 않는다.** 이 편은 **50 MPa 한 점**이고, 16호와의 비교(§13.4)는
  **가설**이다.
- **Table S1 의 CE 를 `LLI` 대리로 쓰지 않는다** (D11 + §13.3 가).
- **Q4 는 여전히 0/17 이다.**

## 17. 후속 후보

| 순위 | 논문 | 왜 |
|---|---|---|
| ★★★ **1** | **Santhosha, Medenbach, Buchheim, Adelhelm, *Batteries & Supercaps* 2019** (ref 26) | **0.62 V 가 태어난 자리.** 쿨로메트릭 적정으로 In+LiIn 2상역을 동정한 원전이고, `[인쇄]` "Li-richer phases … **strongly dependent on small lithiation changes**" 의 출처. **우리 Q5 의 열역학 바닥**이고, 16호(0.58↔0.47 V)·17호(±10 mV)의 산포를 대조할 유일한 기준. ⚠ 서지 표기가 `[인쇄]` "414, 359 (2019)" 로 **권호가 이상하다** — 확인 필요 |
| ★★★ **2** | **Nam, Park, Oh, An, Jung, *J. Mater. Chem. A* 2018, 6, 14867** (ref 20) | **Li-In-SE 복합 음극의 원전**이자 `[인쇄]` "Li-depleted **In-rich layers** with low Li conductivity are formed during delithiation" 의 원전. 17호의 처방과 기구 설명이 **전부 여기서 온다.** 3전극(Li-In/Sn)도 있다 |
| ★★★ **3** | **Sedlmeier, Schuster, Schramm, Gasteiger, *JES* 2023, 170, 030536** (ref 21) | 3전극 임피던스로 **분리막 근처 Li 농도**의 중요성 + `[인쇄]` **Li 쪽을 분리막으로 돌리는 실험**(§13.4 의 검증 실험이 이미 여기 있다). Gasteiger 그룹 |
| ★★ **4** | **Ikezawa, Fukunishi, …, Kanno, Arai, *Electrochem. Commun.* 2020, 116, 106743** (ref 16) | Li-In/LCO 3전극, `[인쇄]` **1 C 이상에서 Li-In 이 병목**. ⚠ **큐 17번(Fukunishi, *J. Power Sources* 564 (2023) 232864)과 같은 그룹**이고 16호의 유일한 외부 실측 대조군이었다 — **큐 17번을 먼저 읽는 것이 경제적일 수 있다** |
| ★★ **5** | **Yanev, Auer, Heubner, Höhn, Nikolowski, Partsch, Michaelis, *JES* 2022, 169, 090519** (ref 29) | 이 편의 **CA 율시험 방법 원전.** "저율 평탄 + 급락 = 양극 제한" 형태 기준의 근거가 여기 있어야 한다 — §4.2 의 `[해석]`(형태 기준에 문턱이 없다)을 확인하거나 반박할 자리 |
| ★ **6** | **Wang, Zhao, …, Huang, *eScience* 2023, 3, 100087** (ref 28) | 17호와 **정면 충돌하는 편** — `[인쇄]` **14.3 at% Li 가 최적**이라고 주장. 17호는 그것을 압력·율 차이로 넘기지만 **수치를 대지 않는다**(G8). Q5·Q6 양쪽 |
| ★ **7** | **Krauskopf, Mogwitz, Rosenbach, Zeier, Janek, *AEM* 2019, 9, 1902568** (ref 14) | 합금 음극의 확산 한계 원전. `D_Li(In)` 의 값이 여기 있으면 §13.2 의 "6 h 에 안 돌아온다" 를 **시간 척도로 검증**할 수 있다 |

⚠ **큐 대조**: 큐 **17**(Fukunishi 2023)·**19**(embedded indium RE)·**20**(μ-RE,
Indium-Lithium anodes) 세 편이 **전부 이 축**이다. **위 후속 후보 1·2·3 은 큐에 없다.**

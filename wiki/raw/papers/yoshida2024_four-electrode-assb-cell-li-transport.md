---
title: "Yoshida, Ikezawa, Okajima, Arai 2024 — An all-solid-state electrochemical four-electrode cell: application to Li-ion transport between two sulfide solid electrolytes (Electrochimica Acta 497, 144523)"
source_url: local-upload/18._An_all-solid-state_electrochemical_four-electrode_cell_Application_to_Li-ion_transport_between_two_sulfide_solid_electrolytes.pdf + 18._Sup_An_all-solid-state_electrochemical_four-electrode_cell_Application_to_Li-ion_transport_between_two_sulfide_solid_electrolytes.pdf (SI)
source_url_note: "본문 9쪽 (pp. 1-8 + 참고문헌 27편) + SI 9쪽 (Fig. S1-S8, 표 없음). 크로핑 17장(본문 그림 8 + SI 그림 7 + 표 2) 중 **그림 9장을 직접 봤다** — Fig. 1/2/3/4/5/6/7/8 + Fig. S1 + Fig. S4 + Fig. S6, 그리고 **캡션이 'Figure S 5' 로 띄어져 크로퍼가 놓친 Fig. S5 를 SI p.6 직접 렌더로 열람**. 표는 PDF 텍스트를 쓰되 **Table 2 는 지수 부호 오타 확인을 위해 크롭도 직접 봤다**. 안 본 것: Fig. S2(전도도 셀 도식) · S3(XRD) · S7 · S8 — 본문/SI 텍스트로 충분. 누락은 get_images()/get_drawings() 페이지별 계수로 기계 확인. 1차 측정 있음(4전극 셀 3종 + 단일/적층 LPSCl 대조 + 압력 2점 + 온도 4점), n 미상(`n =` 실질 0회). `[인쇄]`/`[도표]`/`[재현]`/`[해석]` 4구분."
source_doi: 10.1016/j.electacta.2024.144523
source_license: "(c) 2024 The Author(s), Elsevier Ltd — CC BY 4.0 오픈액세스"
pdf_sha256: a991f5351cb61a20ea0a94f1185d065d27c2147f698643d32d4fa8a7a04e975e
si_sha256: 774a121241a8d2dc67e77d8845bf1fe3e0e55a506cd65a6c29dbc580cd1b49b0
ingested: 2026-09-22
sha256: 1864228cc4979bf50849e4838f51b6c133f384cc00276ff707955663f7a747e7
---

# 수집 목적

`assb` 섹션 **19호**. 큐 **18번** (18호 = 큐 17 Fukunishi 2023 NCM523 3전극 열화,
17호 = 큐 16 Yanev 2024 Li-In, 16호 = 큐 15 Ramanayagam 2026 압력×3전극).
닻은 `questions/assb-contact-loss-vs-lampe.md`. 큐 문서
(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md`)의 등록 축은 **Q5**이고 메모는
*"상대극 전위 변화가 선형이 아니다"* 였다 — **그 메모는 맞다**(§3.2, 아래 확정).

★★★★ **그리고 이 편은 18호와 같은 연구실의 같은 계보다** — Ikezawa·Okajima·Arai
셋이 겹치고, 18호가 방법 원본으로 든 **Ikezawa 2020 (*Electrochem. Commun.* 116,
106743)** 이 여기서도 **ref [18]** 로 인용된다(§자기 계보). 18호 자신도 **ref [20]**
으로 인용된다. **기준극 계보의 네 번째 편이고, 그 계보의 방법 본체 쪽에 가장 가깝다.**

> **판정 한 줄 (먼저)**: 이 편은 `assb` 계보에서 **전극이 하나도 없는 첫 편**이다 —
> 복합양극도, 활물질도, 용량도, 사이클도 없다. 잰 것은 **두 황화물 고체전해질
> 펠릿을 포개서 만든 계면 하나의 Li⁺ 수송 저항**뿐이다. 그래서 Q1·Q2·Q3(라벨)·
> Q7·Q8 에는 **구조적으로 기여할 수 없다.**
> ★★★★ **대신 Q5 에 이 계보가 지금까지 못 준 것을 준다: 기준극의 절대 전위를
> 가정하지 않는 측정 구조.** 4전극에서는 측정량이 **RE₁ 대 RE₂ 의 전위차**이므로
> R-LTO 의 절대 전위가 **소거된다** — 실제로 이 편에는 `assum*` 이 **0 회**이고
> "**1.55**" 라는 숫자가 **한 번도 나오지 않는다**(18호의 G4 가 여기서는 생기지
> 않는다). 남는 것은 **기준극 쌍의 재현성**이고, 그것이 처음으로 인쇄된다:
> `[인쇄]` **ca. ±30 mV**.
> ★★★★ **그리고 Li-In 상대극이 처음으로 "평탄하지 않은 모습"으로 4전극에 찍힌다**:
> `[인쇄]` "The potential change in the counter electrode is **not linear**, and the
> voltammogram of the counter electrode is **asymmetric**" — `[도표]` 200 초·≤0.7 mA
> 의 CV 한 번에 `E_CE` 가 **42 / 126 / 75 mV** 움직인다(세 셀).
> ★★★★ **비분리가 자기 데이터로 증명된다**: `[인쇄]` Li-In 전극 자신의 반원이
> **P1(>1 kHz)과 P2(1 kHz–0.1 Hz) 둘 다와 겹치고**, 그래서 "**P1 and P2 are
> difficult to extract from the impedance measured with the two-electrode system**".
> 이것이 Q2(분해 비유일성) 계보에 들어오는 **네 번째 층**이다.
> ⚠⚠ **그런데 이 편의 중심 배정(P2 = 계면)이 걸린 그림은 4 점짜리이고 그중 하나가
> 4.5 배 이상치다** — `[도표]` Fig. 4(d): `R₂/d` = **17.0 / 3.3 / 3.0 / 3.2 Ω mm⁻¹**.
> **이상치를 빼면 R₂ 는 R₁ 만큼 깨끗하게 `d` 에 비례한다**(산포 1.10× ↔ R₁ 1.12×),
> 즉 논문의 결론과 **반대**가 된다. 같은 결론을 훨씬 강하게 떠받치는 그림(Fig. 7,
> 계면 유무 대조)이 같은 지면에 있는데 **1차 근거의 자리에 놓이지 않았다.**
> **Q4**: `identifiab*`·`uniqu*`·`uncertaint*`·`degenerac*`·`condition number`·
> `error bar`·`n =` **전수 0 회** ⇒ **0 / 19**. 다만 **성질이 열두 번째로 바뀐다**:
> **어휘 없이 귀속을 실험으로 물은 첫 편**(단면적 스윕 + RE 간격 스윕 + 계면 유무
> 대조)이고, **그 설계의 절반이 판별력이 없다**(단면적 축은 벌크도 계면도 똑같이
> `1/S` 로 스케일한다).
> **Q6**: `pressure` 4 회 · `kPa` **5 회** · `MPa` 3 회. **운전 압력을 보고하고 스윕한다
> — 단 2 점(560 · 840 kPa)이고, 조립 압력은 ca. 420 kPa.** ★ **계보 최저 압력대**이고
> 8호가 인쇄한 산업 요구치(<≈1 MPa) **안에 들어오는 첫 편**이다.
> ★★★ **그리고 압력이 `Ea` 를 안 움직인다**(`[인쇄]` "the physical state of the
> interface does **not affect the Ea** but the resistance values") ⇒ **`Ea` 가
> 접촉 면적에 불변인 관측량**이라는, 우리 곱 축퇴 처방의 **새 채널**이 생긴다.

> 표기: `[인쇄]` 본문·SI 명시 · `[도표]` 그림에서만 읽은 값 (`figure-read ≈`, 판독 오차 붙음) ·
> `[재현]` 우리가 지면의 숫자로 계산한 값 · `[해석]` 우리 해석.
> **`[해석]` 표시 없는 문장은 원문이 실제로 말한 것이다.**

# 원문에 없어서 확인이 필요한 것 (공백 원장)

| # | 공백 | 왜 걸리나 |
|---|---|---|
| **G1** | **셀 개수가 어디에도 없다.** `n =`·`error bar`·`standard deviation`·`replicate` **전수 0 회**. 모든 ± 는 **4 점 Arrhenius 회귀의 표준오차**이고 셀 간 반복이 아니다 | 16·17·18호와 같은 층위. 조건당 n=1 로 읽을 수밖에 없다 |
| **G2** | **단면적 `S` 의 정의가 없다.** Fig. 4(a)(b)의 `S` 가 펠릿 단면인지, R-LTO 복합체(φ5 mm)인지, Li-In 박(φ9 mm)인지 적혀 있지 않다. `[재현]` 값은 **12.2 / 25.0 / 48.8 mm²** 인데 펠릿 몰드는 **φ10 mm = 78.5 mm²** 라 **셋 다 그보다 작다** | 배정 논증의 x 축이다. 그리고 `S` 를 **어떻게 바꿨는지** Experimental 에 한 줄도 없다 |
| **G3** | **RE 간격 `d` 를 어떻게 바꿨는지도 없다.** `[도표]` 값은 **0.88 / 1.0 / 1.4 / 1.95 mm**. 표준 제작은 100 mg + RE + 100 mg 한 장이므로 `d` = 펠릿 한 장 두께인데, 그 두께가 인쇄되지 않았다(전도도용 펠릿만 "1.0 mm") | 위와 같다 |
| **G4** | **R-LTO 기준극의 전위가 이 편에는 아예 없다.** 절대값을 쓰지 않으므로 필요가 없다 — 대신 `[인쇄]` "the **reproducibility of the reference electrode potentials (ca. ±30 mV)**" 가 **근거 없이** 등장한다(데이터도 인용도 없다) | ★ 18호의 "Assuming 1.55 V" 가 **사라진 자리**에 **±30 mV** 가 들어왔다. 그런데 그 숫자의 출처가 없다. ref [18](Ikezawa 2020)에 있을 가능성이 높다 — **확인해야 한다** |
| **G5** | **등가회로(Fig. 3d)에 `P3` 가 없다.** 그림은 `R₁/CPE1` + `R₂/CPE2` **두 개뿐**인데 Table 2(c)는 **P3 파라미터 3 열**을 인쇄한다. 직렬 저항(`R_s`)도 없다 | (c) 셀이 실제로 어떤 회로로 적합됐는지 지면에 없다 |
| **G6** | **`P3` 의 정체에 독립 근거가 0.** `[인쇄]` "we **deduce** that P3 is derived from the ion transport at the **crack** formed in the solid electrolyte pellet" — 근거는 **시상수가 P1 과 P2 사이라는 것**과 **셀마다 크기가 다르다는 것** 둘뿐. `crack` 은 본문 **1 회**, 단면 관찰·토모·균열 정량 **0** | ⚠⚠ `[도표]` Fig. 7(a)의 P3 는 **≈35 Ω** 로 같은 논문의 계면 저항(8–29 Ω)보다 **크다**. "정체 미상이고 셀마다 다르며 관심 성분보다 큰 항" 이 회로 안에 있다 |
| **G7** | **CV 와 EIS 가 같은 셀인지 안 적는다.** `[재현]` (a)(b)는 CV 기울기와 Nyquist 총 저항이 맞는데(106↔105 Ω · 210↔218 Ω) **(c)는 114 ↔ 184 Ω 로 1.6 배 어긋난다** | DC↔AC 정합 검사를 논문이 하지 않는다 |
| **G8** | **`P1` 원호의 꼭짓점이 측정 대역 밖이다.** Table 2 의 특성 주파수가 `[재현]` **2.4×10⁷ Hz**(b)·**9.1×10⁶ Hz**(c) 인데 상한은 **7 MHz** 다. `[도표]` 세 Nyquist 모두 고주파 쪽이 **닫히지 않는다** | `R₁` 은 **외삽값**이다. 특히 (b)는 원호 208 Ω 중 측정된 구간이 `[도표]` ≈55 Ω(26 %) |
| **G9** | **압력 점이 둘뿐이다** (560 · 840 kPa). 조립 기본값 ca. **420 kPa** 에서의 `R₁`·`R₂` 는 따로 인쇄되지 않는다 | "dependence of pressure" 를 2 점으로 말한다. 그리고 `[재현]` Table 2(b)의 `R₂` 21.5 Ω(≈420 kPa)가 Fig. 8 의 560 kPa 값 ≈24.7 Ω 보다 **작다** — 압력 추세와 **반대 방향** |
| **G10** | **`Ea` 의 자기 불일치를 다루지 않는다.** `[도표]` Fig. 7(c): LPSCl\|LPSCl 셀의 **`Ea(R₁)` = 45.5 ± 0.1** kJ mol⁻¹ 인데 같은 물질의 Table 1 벌크값은 **40.5 ± 0.3** 이다. `R₁` 은 정의상 LPSCl 벌크뿐이므로 **같아야 한다** | ★★★★ **5.0 kJ mol⁻¹ 차이 = 인쇄된 ± 의 12 배 이상.** 이 편이 주는 **산포 하한**이다 |
| **G11** | **`C` 의 절대 크기를 검토하지 않는다.** `[재현]` `P2` 의 용량 1.6–3.8 mF 를 φ10 mm 기하 면적으로 나누면 **2.0–4.8 mF cm⁻²** = 전형적 이중층(10 µF cm⁻²)의 **200–480 배** | 접촉 면적은 기하 면적을 **넘을 수 없다** ⇒ `P2` 의 `C` 는 이중층이 아니다. 우리 곱 축퇴 처방의 전제가 여기서 2–3 자릿수로 깨진다 |
| **G12** | **`P1`·`P2` 를 "RE artifact 가 아니다" 라고 말한 근거가 진폭 비의존성뿐이다.** `[인쇄]` "These semicircles do not show the **AC amplitude dependence** (Fig. 3(a)), suggesting that the semicircles are **not derived from artifacts related to the RE**" | ★ **범주 오류**다 — 진폭 비의존성은 **선형성**을 보지 **기원**을 보지 않는다. 기하학적 수축·프로브 결합 같은 **선형 artifact 는 정의상 진폭 무관**이다. 18호의 "K–K 잔차 → 기준극 안정성" 과 **같은 구조의 추론, 같은 그룹** |
| **G13** | **Fig. 4 의 캡션에 셀 종류·온도·나머지 변수가 없다.** 어느 전해질 쌍인지, (a)(b)의 `d` 가 얼마인지, (c)(d)의 `S` 가 얼마인지 없다 | 두 스윕이 **직교했는지** 확인 불가 |
| **G14** | **`P2` 의 물리 모형이 없다.** 3 과정 그림(Fig. 6)은 **정성 도식**이고 `interphase` 의 두께·조성·존재 증거(회절·분광)는 **0** (`interphase` 5 회 전부 본문 서술) | `[인쇄]` "interphase between two SEs" 가 실재한다는 독립 관측이 없다 |
| **G15** | **데이터 비공개** — `[인쇄]` "Data will be made available **on request**" | 16·18호와 같다. 원시 스펙트럼 재적합 불가 |
| **G16** | **Fig. S5 의 패널 배정이 본문과 SI 캡션에서 다르다** (아래 D1) | 어느 셀의 Li-In 임피던스가 어느 것인지 지면만으로는 정할 수 없다 |

# 서지

**Kotaro Yoshida, Atsunori Ikezawa\*, Takeyoshi Okajima, Hajime Arai** — "An all-solid-state
electrochemical four-electrode cell – Application to Li-ion transport between two sulfide
solid electrolytes", ***Electrochimica Acta* 497 (2024) 144523**,
doi `10.1016/j.electacta.2024.144523`.

- 소속: **Tokyo Institute of Technology** — School of Materials and Chemical Technology +
  **All-Solid-State Battery Center, Institute of Innovative Research**, Yokohama.
  교신 **Atsunori Ikezawa** (`ikezawa.a.aa@m.titech.ac.jp`). ★ **18호의 교신은 Hajime
  Arai 였고 여기서는 Ikezawa 가 교신·Funding acquisition·Conceptualization 이다.**
- 접수 **2024-02-23** → 개정 **2024-04-25** → 승인 **2024-05-30** → 온라인 **2024-05-31**.
- `[인쇄]` © 2024 The Author(s), Elsevier Ltd, **CC BY 오픈액세스**.
  ⇒ ★ **이 계보에서 16호(CC BY)에 이은 두 번째 오픈액세스**이고 18호(All rights reserved)와
  다르다.
- 자금: **JSPS KAKENHI JP22H04608** (Grant-in-Aid for Scientific Research on Innovative
  Areas "**Interface IONICS**"). 이해충돌 신고: Ikezawa 가 JSPS 지원을 받았다고 기재.
- 감사: **Ryoji Kanno · Masaaki Hirayama · Kota Suzuki**(합성 장비) + ★ **Dr. Goro
  Fukunishi**(실험 기술 자문) — **18호의 제1저자**다.
- 분량: **본문 9 쪽**(pp. 1–8 본문 + 참고문헌 **27 편** pp. 8–9) + **SI 9 쪽**
  (Fig. S1–S8; 표 없음).
- 키워드 `[인쇄]`: Four-electrode cell | Interface ionics | Electrochemical impedance
  spectroscopy | Solid \| Solid interface | Solid-state ionics.
- PDF: 본문 sha256 `a991f5351cb61a20…`, SI `774a121241a8d2dc…` (frontmatter 에 전문).

## 이 논문의 자기 계보 — 그리고 우리 위키와의 접점

| ref | 문헌 | 역할 |
|---|---|---|
| **[18]** | **Ikezawa, Fukunishi, Okajima, Kitamura, Suzuki, Hirayama, Kanno, Arai**, *Electrochem. Commun.* **116** (2020) 106743 — "Performance of Li₄Ti₅O₁₂-based reference electrode for the electrochemical analysis of all-solid-state lithium-ion batteries" | ★★★★ **큐 문서가 확인하라고 한 바로 그 편이고, 여기서도 인용된다.** R-LTO 기준극·3전극 셀·Ni 메시 집전체 제작법이 전부 여기서 온다(Methods 가 이것을 직접 가리킨다). **16·17·18·19호 네 편이 전부 이것을 가리키는데 큐에 없다** |
| **[19]** | **Fukunishi, Ikezawa, Okajima, Kitamura, Suzuki, Hirayama, Kanno, Arai**, *ACS Appl. Energy Mater.* **6** (2023) 10908 — "Impedance analysis and **cyclability** evaluation of **graphite** composite electrodes with all-solid-state three-electrode cells" | ★★★ **새로 보이는 자매편.** 18호(NCM523 양극)의 **흑연 음극 판**이다. 11호(Yu 2024)가 `assb` 최초의 흑연 음극 완전지였던 것과 걸린다 — **큐에 없다** |
| **[20]** | **Fukunishi, Tabuchi, Ikezawa, …, Arai**, *J. Power Sources* **564** (2023) 232864 | **= 우리 18호.** 이 편이 자기 3전극 계보의 세 번째 항으로 인용한다 |
| **[14]** | **Abe, Sagane, Ohtsuka, Iriyama, Ogumi**, *JES* **152** (2005) A2151 | ★★ **방법의 개념 원전** — 고체\|액체 계면의 Li⁺ 이동을 4전극으로 재고 `Ea` 로 율결정 단계(용매화/탈용매화)를 정한 편. **이 논문의 논증 구조 전체가 여기서 왔다** |
| **[10]–[13]** | Kakutani 1983 · Senda 1991 · Samec 1977 · Samec 2009 | 액체\|액체 계면(ITIES)의 4전극 전기화학 원전들 |
| **[17]** | **Rosenkranz, Janek**, *Solid State Ionics* **82** (1995) 95 | 혼합전도체의 국소 전위 측정 — 금속 기준극이 황화물에 안 되는 이유의 근거 |
| **[27]** | **Brug, van den Eeden, Sluyters-Rehbach, Sluyters**, *J. Electroanal. Chem.* **176** (1984) 275 | **식 (1)(유효 용량)의 원전.** ★ 18호 검사 A 에서 우리가 쓴 바로 그 변환이고, **여기서는 저자가 직접 써서 `C` 열을 인쇄한다** |
| **[21]** | **Rosenbach, Walther, …, Janek, Zeier**, *Adv. Energy Mater.* **13** (2022) 2203673 | 할라이드↔황화물 전해질의 **화학적 비양립성** — "황화물\|황화물은 상대적으로 안정·단순하다" 의 근거 |
| **[8]** | **Lewis, …, McDowell**, *Nat. Mater.* **20** (2021) 503 — operando X-ray tomography 로 void ↔ interphase | ⚠ **5호(Doux 2020)와 같은 계열**의 원전. 이 편은 "contact loss" 의 근거로만 인용 |
| **[4]** | **Shi, Tu, Tian, …, Ceder**, *Adv. Energy Mater.* **10** (2020) 1902881 — "High active material loading … via **particle size optimization**" | ⚠ **큐 21번과 같은 주제**이고 18호 검사 A(입자 크기 ↔ 접촉 면적)의 배경 |

`[해석]` **이 편은 16호가 지목한 "외부 실측 대조군"(18호)의 형제이지 독립 검증이
아니다.** Tokyo Tech / Arai–Kanno 그룹의 R-LTO 기준극 방법이 **2전극(전도도) → 3전극
(18호·[19]) → 4전극(이 편)** 으로 확장된 세 번째 단계다. 그리고 **그 확장의 방향이
우리에게 중요하다**: 3전극은 상대극 분극을 **일부** 남기고, 4전극은 **전부 제거한다.**

# 어휘 집계 (NFKC 정규화 · 대소문자 구분 · 본문 pp.1–8 참고문헌 제외 / SI 전문)

| 낱말 | 본문 | SI | 메모 |
|---|---:|---:|---|
| `interface` | **55** | 0 | 이 편의 주인공 |
| `reference electrode` | **19** | 2 | |
| `four-electrode` | **17** | 2 | |
| `R-LTO` | **13** | 2 | |
| `Li-In` | 11 | 7 | + `InLi` 2 (본문에서 표기가 섞인다) |
| `LTO` | 15 | 2 | |
| `CPE` | 8 | 0 | |
| `rate-determining` | **7** | 0 | |
| `interphase` | **5** | 0 | ★ 전부 서술 — 독립 관측 0 (G14) |
| `SE1` / `SE2` | 5 / 5 | 0 | Fig. 6 |
| `fit*` | 5 | 0 | |
| `activation energy` | 4 | 0 | + `Ea` 다수 |
| `pressure` | **4** | 0 | ★ 18호는 **0 회**였다 |
| `kPa` | **5** | 0 | 420 · 560 · 840 |
| `MPa` | 3 | 0 | 140(전도도 펠릿) · 280(Au / 4전극 펠릿) |
| `contact` | 3 | 0 | 아래 전수 |
| `contact area` | **2** | 0 | 서론 1 + 압력 논의 1 — **값 0** |
| `two-electrode` | 2 | 2 | |
| `equivalent circuit` | 2 | 0 | |
| `reproducib*` | **2** | 0 | ★ 둘 다 결정적 — 기준극 ±30 mV · Li-In 임피던스 "poor" |
| `symmetr*` | 2 | 0 | `[인쇄]` "symmetric linear current response" |
| `asymmetr*` | **1** | 0 | ★ `[인쇄]` 상대극 볼타모그램이 비대칭 |
| `not linear` | **1** | 0 | ★★★★ **큐 메모의 출처** |
| `polarization` | 2 | 3 | |
| `artifact` | 1 | 0 | G12 |
| `crack` | **1** | 0 | ⚠ P3 의 유일한 정체 서술 (G6) |
| `capacitance` | 1 | 0 | 식 (1) |
| `open circuit` | 1 | 0 | 4전극 셀의 RE–RE OCV |
| `cycle` | 3 | 0 | 전부 밀링 사이클·수명 일반론 |
| `three-electrode` | **1** | 1 | 본문은 배경(18호 인용), SI 는 Fig. S5(d) |
| `void` · `porosit*` · `tortuos*` · `percolat*` · `contact loss` · `θ` | **0** | **0** | ⚠ **`contact loss` 0 회** — 서론의 "significant contact loss" 는 `contact loss` 로 붙어 있어 1 회로도 셀 수 있으나 **정량은 0** |
| `degrad*` · `aging` / `ageing` · `capacity` · `cycle life` | **0** | **0** | ★ **열화·용량 어휘가 전무하다** — 전극이 없다 |
| `LAM` · `LLI` · `SOH` · `state of health` | **0** | **0** | |
| `OCV` · `GITT` | **0** | **0** | |
| `dendrit*` · `dead` · `isolat*` | **0** | **0** | |
| `DRT` · `Kramers` · `Kronig` · `residual*` · `regulariz*` | **0** | **0** | ⚠ **18호가 쓴 검증 도구(K–K·DRT)를 이 편은 하나도 안 쓴다** |
| `assum*` / `Assum*` | **0** | **0** | ★★★★ **가정이라는 낱말이 없다.** 그리고 "**1.55**" 도 0 회 |
| `identifiab*` · `uniqu*` · `ill-posed` · `uncertaint*` · `confidence` · `error bar` · `standard deviation` · `condition number` · `Fisher` · `bootstrap` · `Bayes*` · `degenerac*` · `overfit*` · `cross-valid*` · `sensitiv*` · `initial guess` · `multi-start` · `n =` | **0** | **0** | **Q4 = 0 (19/19 편)** |
| 오검출 확인 | — | — | `[Ll]am[a-z]+` **0 건** · `Soh\w*` **0 건** ⇒ `LAM`→flammable, `SOH`→Sohn 오검출 **없음**. ⚠ 정규식 `n =` 는 "Li: **In =** 25: 75 at%" 를 1 건 오검출했다 — **실질 0 회** |

## `contact` 3 회 전수 — 이 편에서 "접촉" 이 놓이는 자리

1. 서론 — "the **contact area** between the solid electrolyte and solid electrode materials
   … a relatively large amount of solid electrolyte must be mixed in the electrodes"
2. 서론 — "the solid \| solid interface is hardly deformed to result in significant
   **contact loss** [8,9]" ⇒ **우리 닻 물음의 낱말이 서론에 있다. 값은 없다.**
3. §3.7(압력) — "Both R1 and R2 values decrease with the increase in pressure, **possibly
   due to the increases in the contact areas of SE particles and SE pellets**, respectively"
   ⇒ ★★★ **접촉 면적이 이 편에서 유일하게 인과로 불려 나오는 자리이고, 여전히 값이 없다.**
   `[해석]` **`R(P)` 는 있고 `θ(P)` 는 없다** — 18호에서 `R(N)` 은 있고 `θ(N)` 이 없던 것과
   같은 모양이다. ⇒ **`assb` 19/19 편이 `θ` 를 노화·압력 축 위에서 주지 않았다.**

# §1 서론 — 이 편이 자기를 놓는 자리

- `[인쇄]` ASS-LIB 의 문제(저수명 · 전해질 질량비)는 **"solid \| solid 계면 면적을
  만들기 어렵다"** 에서 온다. 액체셀은 다공 전극에 용액을 적시면 경로가 생기지만
  고체셀은 전극 안에 **많은 양의 SE 를 섞어야** 한다.
- `[인쇄]` 그리고 solid \| liquid 계면은 전극 부피 변화를 **유연하게 받아내지만**
  solid \| solid 계면은 **거의 변형되지 않아 significant contact loss** 가 된다 [8,9].
- `[인쇄]` 그래서 필요한 것은 **충분한 접촉 면적**뿐 아니라 **계면 고유 Li⁺ 전도도의 개선**이다.
  ⇒ ★★ `[해석]` **이 편이 겨눈 것이 정확히 우리 곱 축퇴의 두 인자다**: `면적 θ` 와
  `고유 전도도 j₀`. 그리고 이 편은 **후자를 재려고 전자를 통제하려 한다** —
  우리와 반대 방향이지만 **같은 곱을 본다.**
- 4전극 셀의 정의 `[인쇄]`: "comprises **two reference electrodes for charge
  compensation** and **two counter electrodes for potential measurement or control**"
  ⚠ **역할이 뒤집혀 적혀 있다** — 뒤 문장과 Fig. S1 을 보면 **RE 쌍이 전위 측정용**이고
  **CE 쌍이 전류(전하 보상)용**이다. (아래 D2)
- 선행: 액체\|액체(ITIES)는 CV·CA 로 **이온 이동의 Gibbs 자유에너지·전위창**까지
  정량됐고 [10–13], 고체\|액체는 AC 임피던스로 이동 저항을 쟀다 [14–16].
  `[인쇄]` **Abe 등[14]은 `Ea` 로 율결정 단계를 용매화/탈용매화로 동정했다** —
  ★ **이 편의 논증 틀(=`Ea` 로 율결정 단계를 지목)의 원본**이다.
- `[인쇄]` **"there is no report on AC impedance analysis of the solid \| solid interface
  resistance."** 4단자 측정은 벌크 전도도용으로 흔하지만 계면에는 거의 안 쓰였고[17],
  **Pt·Au 같은 금속 기준극은 전자에만 가역이라 전자전도가 나쁜 황화물에 못 쓴다.**
  ⇒ `[인쇄]` 그래서 **Li⁺ 에 가역인 R-LTO(Li₇Ti₅O₁₂ \| Li₄Ti₅O₁₂) 메시 기준극** [18–20].
- 황화물\|황화물을 고른 이유 둘 `[인쇄]`: ① R-LTO 의 안정 작동을 이미 확인했다 [18–20]
  ② 황화물\|황화물 계면은 **상대적으로 안정·단순**할 것이다 [21].
  ⚠ ①의 "확인" 은 **자기 그룹 세 편의 자기 인용**이다.

# §2.1 재료 — 전해질 3종 + R-LTO + Li-In

| 재료 | 조성·출처 | 값 |
|---|---|---|
| **LPSCl** | argyrodite **Li₆PS₅Cl**, **Sigma-Aldrich 상용** | σ = **1.8 mS cm⁻¹**, `Ea` = **40.5 ± 0.3** kJ mol⁻¹ |
| **LPSI** | glass-ceramic **Li₂S:P₂S₅:LiI = 60:20:20 mol%**, 자체 합성 (ZrO₂ 볼 φ10 mm × 10, 370 rpm, 60 min × 38 사이클 + 10 min 간격 → 진공 석영관 **433 K, 3 h**) [22] | σ = **2.1 mS cm⁻¹**, `Ea` = **29.8 ± 0.3** kJ mol⁻¹ |
| **LGPS** | **Li₁₀.₃₅Ge₁.₃₅P₁.₆₅S₁₂**, GeS₂:Li₂S:P₂S₅ = **70:11:19 mol%**, 같은 밀링 + **823 K, 8 h** [23] | σ = **7.1 mS cm⁻¹**, `Ea` = **37 ± 2** kJ mol⁻¹ |
| **R-LTO** | **Li₇Ti₅O₁₂ : Li₄Ti₅O₁₂ = 67 : 33 mol%**, 상용 Li₄Ti₅O₁₂(Ishihara Sangyo)를 **리튬 나프탈레나이드 THF 용액**(0.2 mol dm⁻³, 30 cm³, Li 3 mmol 투입)으로 화학 환원 [24] | ★★ **조성이 처음 인쇄된다** — 18호는 "partially reduced" 라고만 했다 |
| **Li-In** | **Li : In = 25 : 75 at%**, In 박(**φ9 mm × 50 µm**, Nilaco) 20 mmol 을 같은 용액에 1 일 교반 | ★★★ **`x_Li` = 25 at%** — 17호 40 at%, 18호 37.7→40.0 at% 와 **다른 세 번째 조성** |

★★ **R-LTO 조성 67:33 mol% 는 18호의 공백(G4)을 절반 메운다**: 2 상 혼합이 **한복판**에
있으므로 **평탄 전위가 성립할 구조적 근거**가 생긴다. ⚠ **절대 전위(1.55 V)의 근거는
여전히 이 편에 없다** — 다만 **이 편은 그것을 필요로 하지 않는다**(§3.2).

- XRD `[인쇄]`: SmartLab(Rigaku), **Cu Kα₁**, Ar 밀봉, 4°/min · 0.01° step · 2θ = 10–60°.
- 이온전도도: **Au 분말 대칭 2전극 셀**(Fig. S2). 펠릿 **φ10 mm × 1.0 mm**, 140 MPa 1 min
  성형 → 양면에 Au 분말 캐스팅 후 **280 MPa**(토크 렌치) → VSP-300(BioLogic) + 항온조
  (IW223, Yamato). **10 mV, 50 mHz–7 MHz.**

# §2.2 4전극 셀 제작 (Fig. 1 — 도식 수준으로 기록)

**적층(위→아래)**: 단자 / **Cu 박** / **Li-In 박 (CE₁)** / 〔 **SE1 펠릿**(안에 **RE₁**) +
**SE2 펠릿**(안에 **RE₂**) 을 PET 관 안에 포갠 것 〕 / **Li-In 박 (CE₂)** / **Cu 박** /
부틸 고무 링 / 단자. 전체를 **Ar 채운 플라스틱 용기**에 밀봉(Fig. 1d).

- **R-LTO 기준극**: **R-LTO : PVdF = 86.5 : 13.5 wt%** 슬러리(NMP)를 **Ni 메시**
  (3Ni7-3/0, Taiyo Wire Cloth, **개구율 90–91 %**, 두께 **0.08 mm**)에 캐스팅 [18].
  `[인쇄]` **셀 중앙 근처의 전위를 잡으려고 복합체를 집전체 중앙 φ5 mm 에만** 마스킹
  테이프로 한정(Fig. 1c).
- **펠릿**: 스테인리스 몰드에 **SE 분말 100 mg** → 그 위에 **R-LTO 기준극** → 다시
  **SE 분말 100 mg** → **280 MPa, 1 min**(유압 프레스).
  ⇒ ★ **RE 가 각 펠릿의 중앙면에 매립된다.** 두 펠릿을 포개면 **계면이 두 RE 의 한가운데**다.
- **계면**: 두 펠릿을 **PET 관 안에서 포개는 것**으로 형성(별도 가압·열처리 없음).
- **운전 압력**: `[인쇄]` **ca. 420 kPa**, 토크 렌치.

★★★★ **배선과 측정량**(Fig. S1a + §2.3):
- 전류는 **CE₁ → SE1 → 계면 → SE2 → CE₂** 로 흐른다.
- 측정·제어되는 전위는 **RE₂(오른쪽) − RE₁(왼쪽)** 이고, `[인쇄]` 양의 전류는
  **오른쪽 → 왼쪽**으로 정의된다.
- ⇒ **측정량에 CE 의 분극이 전혀 들어오지 않는다.** `[인쇄]` Fig. S1 캡션:
  "The electrochemical four-electrode cell can measure or control the potential between
  two reference electrodes **without the polarization of the two counter electrodes**.
  In contrast, the potential measured or controlled with the electrochemical two- and
  three-electrode cells contains **the polarization of the counter and working
  electrodes** and **the polarization of the working electrode**, respectively."
- ⇒ ★★★★ `[해석]` **이것이 Q5 에 대한 구조적 답이다.** 3전극은 기준극의 **절대 전위**를
  알아야 작업전극 전위를 말할 수 있다(18호의 1.55 V 가정). 4전극은 **두 기준극의 차**만
  쓰므로 **같은 재료의 RE 를 두 개 쓰면 절대값이 소거된다.** 남는 오차는 **RE 쌍의
  불일치**뿐이고, 그 크기가 `[인쇄]` **ca. ±30 mV** 다.

# §2.3 전기화학 측정

| 측정 | 조건 |
|---|---|
| **CV** | **−50 → +50 mV**(RE₂ vs RE₁), **1.0 mV s⁻¹** ⇒ 1 사이클 **200 s** |
| **AC 임피던스** | **개방회로 전위에서**, **50 mHz – 7 MHz**, 진폭 **10 또는 50 mV** |
| 온도 | 항온조, **25 / 15 / 5 / −5 °C**(Arrhenius 4 점; SI Fig. S6–S8) |
| 장비 | VSP-300(BioLogic) 다채널 + IW223 항온조 |

⚠ **진폭 50 mV 는 열전압(25.7 mV)의 약 2 배다.** 비선형 응답을 부를 수 있는 크기인데,
그것을 검사한 것이 **Fig. 3(a)의 10 mV ↔ 50 mV 중첩** 하나이고 **한 셀에서만** 했다.

# §3.1 재료 특성 (Table 1 · Fig. S3)

- `[인쇄]` LGPS·LPSCl 은 불순물상 없는 특성 XRD; LPSI 는 20°·30° 부근 **넓은 회절**
  (glass-ceramic, [22]와 같다).
- 문헌 대비 `[인쇄]`: LPSI **1.35 mS cm⁻¹ · 28.8 kJ mol⁻¹** [22] ↔ 이 편 2.1 · 29.8 —
  비슷. LPSCl **0.74–4.73 mS cm⁻¹ · 11–34 kJ mol⁻¹** [25,26] ↔ 이 편 1.8 · **40.5**
  — ⚠ **`Ea` 가 문헌 범위(11–34)의 위로 6.5 kJ mol⁻¹ 벗어나는데 본문은 "similar" 라고
  한다**(D4). LGPS **6.1 mS cm⁻¹ · 26 kJ mol⁻¹** [23] ↔ 7.1 · **37**.
- `[인쇄]` LGPS `Ea` 가 높은 이유: **펠릿 제작이 냉간 프레스**(문헌은 **673 K 열간 프레스**).
  ⇒ ★★ `[해석]` **저자 스스로 "같은 물질의 `Ea` 가 성형법으로 11 kJ mol⁻¹ 움직인다"고
  적는다.** 그렇다면 **`Ea` 는 순수 물질 상수가 아니라 미세구조의 함수**이고, 이것이
  뒤의 §3.5 논증(계면 `Ea` ≈ 낮은 σ 쪽 벌크 `Ea`)의 **허용 오차를 결정한다** — 그런데
  논문은 그 연결을 하지 않는다.

# §3.2 순환전압전류법 — ★★★★ Q5 의 1 차 증거

## (가) 4전극이 본 것 (Fig. 2)

- `[인쇄]` 세 셀 모두 **"symmetric linear current response"** ⇒ **RE 사이의 이온 수송은
  옴 법칙 지배**.
- `[인쇄]` **개방회로 전압**: LPSI\|LPSCl **−4 mV** · LGPS\|LPSI **−5 mV** ·
  LGPS\|LPSCl **+25 mV**.
- ★★★★ `[인쇄]` "These potentials are **within the reproducibility of the reference
  electrode potentials (ca. ±30 mV)**, indicating **no difference in the activity of
  Li-ion in these solid electrolytes that this measurement system can detect**."
  ⇒ **세 가지가 한 문장에 있다**:
  ① **R-LTO 기준극 쌍의 재현성 = ca. ±30 mV** (계보 최초의 인쇄된 기준극 재현성 숫자)
  ② **그것이 이 측정계의 검출 하한이다**
  ③ **황화물\|황화물 계면에 검출 가능한 열역학적 접합 전위가 없다** (≤25 mV)
  ⚠ ①의 **근거가 지면에 없다**(G4) — 데이터도 인용도 없다.

`[재현]` **CV 기울기로 읽은 직류 전 저항**(±5 % 판독):

| 셀 | `[도표]` CV 기울기 | `[재현]` `R_DC` | Table 2 의 `ΣR` | 정합 |
|---|---|---:|---:|---|
| LPSI \| LPSCl | +0.49 mA @ +50 mV, −0.45 @ −50 | **≈106 Ω** | 84.5 + 21.5 = **106** | ✅ |
| LGPS \| LPSI | +0.26 / −0.215 | **≈210 Ω** | 208 + 12 = **220** | ✅ (5 %) |
| **LGPS \| LPSCl** | +0.20 / −0.68 | **≈114 Ω** | 149 + 29.3 + 4.8 = **183** | ❌ **1.6 배** |

⇒ ★★ `[해석]` **셋 중 하나가 DC↔AC 정합을 깬다.** 같은 셀이라면 이 차이는 설명되지
않고, 다른 셀이라면 **같은 전해질 쌍의 셀 간 산포가 1.6 배**라는 뜻이다. **논문은 이
검사를 하지 않는다**(G7). ⚠ 그리고 **이 한 셀이 P3 를 가진 셀이자 OCV 가 +25 mV 로
튀는 셀이자 상대극 볼타모그램이 가장 비대칭인 셀이다** — 넷이 같은 셀에 몰려 있다.

## (나) ★★★★ 상대극이 한 일 (Fig. S4) — 큐 메모의 출처 확정

> `[인쇄]` **"The potential change in the counter electrode is *not linear*, and the
> voltammogram of the counter electrode is *asymmetric*, especially in the case of the
> LGPS | LPSCl cell. This result shows that the polarization of the counter electrode
> affects the voltammogram of the LGPS | LPSCl cell measured with the **two-electrode
> system** using the Li-In counter electrode due to the difficulty in the linear sweep
> of the potential applied to the interface."**

⇒ ★★★★ **큐 문서의 메모 "상대극 전위 변화가 선형이 아니다" 는 정확하다. 출처는
§3.2 마지막 문단이고 근거 그림은 Fig. S4 다.** 우리 메모가 맞았다.

`[도표]` **Fig. S4 판독** (`E_CE` = 왼쪽 Li-In 상대극 vs 왼쪽 R-LTO 기준극):

| 셀 | `E_CE` 시작 | 최저 (시각) | 최고 (시각) | **전체 진폭** | 전류 범위 | `[재현]` `ΔE/ΔI` |
|---|---:|---:|---:|---:|---:|---:|
| (a,b) LPSI \| LPSCl | −965 mV | **−988** (t ≈ 53 s) | **−946** (t ≈ 153 s) | **≈42 mV** | +0.49 … −0.46 mA | **≈44 Ω** |
| (c,d) LGPS \| LPSI | −952 | **−1021** (t ≈ 54 s) | **−895** (t ≈ 155 s) | **≈126 mV** | +0.26 … −0.215 | **≈221 Ω** |
| (e,f) LGPS \| LPSCl | −952 | **−968** (t ≈ 23 s) | **−893** (t ≈ 124 s) | **≈75 mV** | +0.20 … −0.70 | **≈83 Ω** |

★★★★ **세 가지가 여기서 나온다.**

**1. 비선형·비대칭의 실체.** (e)에서 **꼭짓점이 t ≈ 23 s 와 124 s** 다 — CV 의 반전
시각은 **50 s 와 150 s** 인데 상대극 전위의 극값이 **27 초 앞선다.** 그리고 하강 구간
(0→23 s)이 상승 구간(23→124 s)보다 **4 배 짧다**. ⇒ **삼각파 입력에 대해 상대극
전위는 삼각파가 아니다.** (a)(c)는 훨씬 삼각에 가깝다 — `[인쇄]` "especially in the
case of the LGPS \| LPSCl cell" 과 일치.

**2. `[재현]` 상대극 가지가 관심 신호보다 크다.**
`ΔE_CE/ΔI` = **44 / 221 / 83 Ω** 이고, 같은 셀의 **계면 저항 `R₂` 는 21.5 / 12 / 29.3 Ω**
이다. ⇒ **상대극(+그 쪽 벌크)이 2–18 배 크다.** 2전극으로 재면 관심 신호가 그 안에
묻힌다. ★★ **이것이 "4전극이 3전극보다 무엇을 더 재는가" 의 정량 답이다.**

**3. `[재현]` 이것은 재고 고갈이 아니라 분극이다.**
Li-In 박: In φ9 mm × 50 µm ⇒ 0.636 cm² × 50 µm × 7.31 g cm⁻³ = **23.2 mg = 0.202 mmol In**.
Li : In = 25 : 75 at% ⇒ **n_Li = 0.0674 mmol = 6.50 C = 1.81 mAh**.
CV 반주기(100 s, 평균 \|I\| ≈ 0.25 mA)의 통과 전하 ≈ **0.025 C = 재고의 0.39 %**.
그리고 `[도표]` **`E_CE` 가 200 s 뒤 출발값(−965 → −965 mV)으로 돌아온다.**
⇒ **가역 분극이다.** 17호의 +0.68…+0.78 V(재고 고갈)와 **기구가 다르다.**

★★★★ **4. Q5 의 경계 조건에서 (ㄷ)만 깬 첫 표본이다.**
18호 digest 가 세운 세 조건: **(ㄱ) 조성이 2 상역 안 · (ㄴ) Li 재고 / 이동 전하 ≥ 한
자릿수 · (ㄷ) 전류밀도 ≲ 0.1 mA cm⁻².**

| | 17호 (foil, CA) | 18호 | **19호 (이 편)** |
|---|---|---|---|
| (ㄱ) `x_Li` | 40 at% (foil 은 49–50 에서 깨짐) | 37.7 → 40.0 at% | **25 at% — 여유 있게 안** ✅ |
| (ㄴ) 재고 / 이동 전하 | ≈5 배 (CA 에서 깨짐) ❌ | 9.5 배 ✅ | **≈260 배** ✅✅ |
| (ㄷ) 전류밀도 | ≈16 mA cm⁻² ❌ | 0.054 mA cm⁻² ✅ | **0.41 – 1.07 mA cm⁻²** ❌ |
| **관측된 `E_CE` 이동** | **+680 … +780 mV** | **≈0**(평탄) | **42 – 126 mV** |

⇒ ★★★★ `[해석]` **(ㄷ)을 한 자릿수 깨면 이동은 10⁻¹ V 대가 아니라 10⁻²–10⁻¹ V 대에
머문다. 17호의 0.7 V 를 만들려면 (ㄴ)이 같이 깨져야 한다.**
**이것은 세 편을 가로지르는 첫 분리 추론이고, 어느 편의 결론도 아니다.**
⚠ 단서 둘: ① 19호의 이동은 **가역 분극**이고 17호의 것은 **지속 이동**이다 —
**같은 축의 같은 양이 아니다.** ② `ΔE_CE` 에는 **CE–RE 벌크 옴 강하가 포함**된다
(보상 없음). `[재현]` LPSI\|LPSCl 에서 CE–RE 구간은 대략 펠릿 반 장이므로
`R₁/2 ≈ 42 Ω` — **관측 44 Ω 의 거의 전부**다. ⇒ **(a)의 42 mV 는 옴과 구별되지 않는다.**
(c)의 221 Ω 은 `R₁/2 ≈ 104 Ω` 의 **2 배**라 **절반은 옴이 아니다.**

★★ `[재현]` **절대 전위 교차 확인**(가정 위): 18호의 R-LTO = 1.55 V vs Li/Li⁺ 를
빌려오면 `E_CE` ≈ −0.95 V ⇒ **Li-In ≈ 0.60 V vs Li/Li⁺**. **17호 0.61 V · 18호 ≈0.60 V
와 일치**하고, **여기 조성은 25 at%, 저기는 40 at%** 다.
⇒ **25–40 at% 에서 같은 평탄값** — 2 상 평탄의 **교차 조성 확인**이다.
⚠⚠ **1.55 V 는 이 편에 없는 값이다.** 이 줄은 **우리가 18호에서 빌려온 가정 위**에 있고,
**채움표에 올리지 않는다.**

# §3.3 AC 임피던스 — 성분 분해와 귀속

## (가) 관측 (Fig. 3 · Table 2)

`[인쇄]` 세 셀 모두 **비슷한 주파수대에 반원 둘**. **P1 의 특성 주파수 > 1 MHz**,
**P2 는 ca. 5 Hz**. `[인쇄]` 진폭 의존성 없음(Fig. 3a) ⇒ "RE 관련 artifact 가 아니다"
(⚠ G12 — 범주 오류).

**Table 2 전수** (등가회로 = `R₁/CPE1` + `R₂/CPE2`, 식 (1) `C = (Q·R)^{1/p}/R` [27]):

| 셀 | 성분 | `R`/Ω | `Q`/F s^{p−1} | `p` | `C`/F | `f_0`/Hz | `τ`/s |
|---|---|---:|---:|---:|---:|---:|---:|
| **LGPS \| LPSI** | P1 | **208** | 3.1×10⁻⁸ | 0.71 | 2.3×10⁻¹⁰ | 3.3×10⁶ | 4.8×10⁻⁸ |
| | P2 | **12** | 1.4×10⁻² | 0.57 | **3.8×10⁻³** | 3.4×10⁰ | 4.6×10⁻² |
| **LPSI \| LPSCl** | P1 | **84.5** | 1.8×10⁻⁷ | 0.59 | 7.8×10⁻¹¹ | **2.4×10⁻⁷** ⚠ | 6.6×10⁻⁹ |
| | P2 | **21.5** | 6.0×10⁻³ | 0.61 | **1.7×10⁻³** | 4.5×10⁰ | 3.6×10⁻² |
| **LGPS \| LPSCl** | P1 | **149** | 2.5×10⁻⁸ | 0.70 | 1.2×10⁻¹⁰ | **9.1×10⁻⁶** ⚠ | 1.7×10⁻⁸ |
| | P2 | **29.3** | 6.3×10⁻³ | 0.55 | **1.6×10⁻³** | 3.4×10⁰ | 4.6×10⁻² |
| | P3 | **4.8** | 1.8×10⁻⁶ | 0.96 | 1.0×10⁻⁶ | **3.2×10⁻⁴** ⚠ | 4.9×10⁻⁶ |

⚠ **`f_0` 세 칸의 지수 부호가 틀렸다**(D3). `[재현]` `f_0 = 1/(2πτ)` 로 검산하면
**2.4×10⁷ · 9.4×10⁶ · 3.2×10⁴ Hz** 여야 한다. (그림 크롭 `tab_2.png` 를 직접 봐서
추출 오류가 아니라 **인쇄된 오타**임을 확인했다. 2.4×10⁻⁷ Hz = **48 일에 한 주기**이고
측정 하한은 50 mHz 다.)
★ `[재현]` **그리고 정정하면 (b)(c)의 `P1` 꼭짓점이 측정 상한 7 MHz 위에 있다**(G8).

`[재현]` **식 (1) 검산**: (a) P1 → (3.1e-8×208)^{1/0.71}/208 = **2.35×10⁻¹⁰** ✓ ·
(a) P2 → (1.4e-2×12)^{1/0.57}/12 = **3.6×10⁻³** ✓. **저자의 `C` 열은 재현된다.**

`[인쇄]` "Both P1 and P2 show **similar fitting parameters among the three cells,
including the time constant**, which strongly suggests that the Li-ion transport
processes attributed to both P1 and P2 are **not different among the three cells**."

## (나) P3 — 정체 미상이고 관심 성분보다 클 수 있다

`[인쇄]` LGPS\|LPSCl 만 P1 과 P2 사이에 작은 반원(P3). `[인쇄]` "We **deduce** that P3 is
derived from the ion transport at the **crack** formed in the solid electrolyte pellet,
considering that the time constant of P3 is between those of P1 and P2 and that the
**magnitude of P3 varies from cell to cell** even when the same solid electrolytes are used."

⇒ ⚠⚠ **근거가 ① 시상수의 위치와 ② 셀마다 다르다는 것뿐이다.** 균열의 직접 관찰은 없다
(`crack` 1 회, 단면 SEM·토모 0).
`[도표]` **Fig. 7(a)** 에서 같은 P3 가 **Z′ ≈ 125 → 160 Ω, 즉 ≈35 Ω** 로 나타난다 —
**Table 2 의 4.8 Ω 의 7 배**이고 **이 편의 계면 저항(8–29 Ω)보다 크다.**
⇒ ★★★ `[해석]` **"셀마다 크기가 다르다" 는 성질은 귀속의 근거가 아니라 산포의 측정이다.**
같은 문장이 **P3 의 셀 간 산포 ≥ 7 배**를 말하고 있고, 그 성분이 **P2 바로 옆 주파수**에
있다. **P2 의 적합이 P3 의 존재·크기에 얼마나 민감한지 검사한 것이 0 이다.**

## (다) ★★★★ Fig. S5 — 상대극이 P1·P2 와 같은 대역을 차지한다 (Q2 직격)

**구성**(Fig. S5d, 3전극): **WE = 왼쪽 Li-In** · **RE = 왼쪽 R-LTO** · **CE = 오른쪽 Li-In**.
`[인쇄]` 그래서 **"The interfacial Li-ion transport resistances between two solid
electrolytes are not included in these impedances"**(WE 와 RE 가 같은 전해질 안에 있다).

`[도표]` **판독**(SI 캡션 배정 기준):

| 패널 | 셀 | Z′ 범위 | **Li-In 전극 총 저항** | 모양 |
|---|---|---|---:|---|
| (a) | LPSI \| LPSCl | 81 → 120 | **≈39 Ω** | 넓은 반원 1 (정점 −Z″ ≈ 6 Ω, Z′ ≈ 103) |
| (b) | LGPS \| LPSI | 100 → 272 | **≈172 Ω** | 반원 2 (1 kHz ≈ 205) |
| (c) | LGPS \| LPSCl | 43 → 97 | **≈54 Ω** | 겹친 혹 2 |

★★★★ **두 문장이 이 편에서 우리 Q2 에 가장 직접적이다:**
> `[인쇄]` "the Li-In electrode showed semicircles in the frequency ranges **overlapping
> with P1 (above ca. 1 kHz) and P2 (ca. 1 kHz to 0.1 Hz)**."
> `[인쇄]` "the impedance spectra of the Li-In electrodes in the … cells **does not match
> well, showing poor reproducibility of the InLi impedance**."
> `[인쇄]` "These results show that **P1 and P2 are difficult to extract from the
> impedance measured with the two-electrode system with InLi counter electrodes**."

⇒ ★★★★ **비분리가 저자의 결론으로 인쇄되고, 자기 측정으로 증명된다.**
`[재현]` **그리고 산포가 숫자로 나온다: 같은 공칭 Li-In 박(25 at%)의 전극 임피던스가
39 ↔ 172 Ω, 4.4 배 갈린다**(n = 3).
⇒ 17호가 `E_CE` 축에서 준 **0.61 ↔ 1.35 V(제조법 차)** 의 **임피던스 축 대응물**이다.

# §3.4 성분 귀속 — 단면적 `S` 와 RE 간격 `d` 스윕 (Fig. 4) ★ 이 편의 가장 약한 자리

논리 `[인쇄]`: RE 사이의 수송은 **① 펠릿 내부**와 **② 펠릿 사이 계면** 둘로 나뉜다.
- Fig. 4(a)(b) — `R` vs `1/S`: `[인쇄]` "R1 and R2 increase **roughly** in proportion to
  the inverse of the cross-sectional area" ⇒ 둘 다 **셀 내부의 이온 수송**이다.
- Fig. 4(c)(d) — `R` vs `d`: `[인쇄]` "**R1 shows a linear increase** with the RE distance,
  while **R2 does not show clear dependence** on the RE distance" ⇒ **R1 = 벌크, R2 = 계면**.

`[도표]` **우리 판독 전수**(±5 %):

| 패널 | 데이터 점 | `[재현]` 규격화 | **산포** |
|---|---|---|---:|
| (a) `R₁` vs `1/S` | (20.5, 56) (40, 170) (82, 320) ×10⁻³ mm⁻² | `R₁·S` = 2733 / 4250 / 3904 Ω mm² | **1.56 ×** |
| (b) `R₂` vs `1/S` | (20.5, 2.3) (40, 4.2) (82, 20.0) | `R₂·S` = 112 / 105 / 244 Ω mm² | **2.3 ×** |
| (c) `R₁` vs `d` | (0.88, 120) (1.0, 128) (1.4, 170) (1.95, 235) mm, Ω | `R₁/d` = 136 / 128 / 121 / 121 Ω mm⁻¹ | **1.12 ×** |
| (d) `R₂` vs `d` | (0.88, **15.0**) (1.0, 3.3) (1.4, 4.2) (1.95, 6.2) | `R₂/d` = **17.0** / 3.3 / 3.0 / 3.2 | **5.7 ×** (이상치 제외 **1.10 ×**) |

★★★★ **세 가지 비판이 나온다.**

**1. `S` 축은 판별력이 없다.** 벌크 저항도 계면 저항도 **둘 다 `1/S` 로 스케일한다.**
Fig. 4(a)(b)는 "펠릿 밖의 무언가(접촉 불량·배선)가 아니다" 만 말하고 **벌크↔계면은
전혀 못 가른다.** 논문도 그렇게 적는다(`[인쇄]` "reasonable to assign P1 and P2 as the
Li-ion transport **within solid electrolyte pellets or at the interface**"). ⇒ **배정 전체가
Fig. 4(d) 하나에 걸려 있다.**

**2. ★★★★ Fig. 4(d)의 "의존성 없음" 은 점 하나가 만든다.**
`[재현]` **0.88 mm 의 15.0 Ω 를 빼면 남은 3 점은 `R₂ = 3.2 Ω mm⁻¹ × d` 로 `R₁` 만큼
깨끗하게 `d` 에 비례한다** (산포 **1.10 ×** ↔ `R₁` 의 **1.12 ×**).
⇒ **같은 4 점이 정반대의 두 읽기를 허용한다**:
- (읽기 A, 논문) 산포가 커서 추세가 없다 ⇒ **P2 = 계면**.
- (읽기 B, 우리) 한 점이 이상치이고 나머지는 `d` 에 비례한다 ⇒ **P2 도 벌크형**.
**4 점 · n = 1 · 오차막대 0 으로는 둘을 가를 수 없다.** 그리고 **논문은 이상치를
언급하지 않는다.**

**3. ★★★ 그런데 같은 논문에 훨씬 강한 근거가 있고, 뒤에 배치돼 있다.**
§3.6 의 **LPSCl 단일 펠릿 ↔ LPSCl\|LPSCl 적층** 대조(Fig. 7)는 **같은 재료에서 계면
하나만 추가**했을 때 **P2 가 생긴다**는 것을 보인다. 이것은 **읽기 B 를 직접 반증**한다.
⇒ `[해석]` **결론은 살아남지만 논증 순서가 거꾸로다.** 논문은 Fig. 4(d)를 1 차 근거로
쓰고 Fig. 7 을 "consistent with the assignment" 로 뒤에 놓는다.

# §3.5 활성화에너지 — 이 편의 논지 (Fig. 5 · SI Fig. S6–S8)

`[도표]` **Fig. 5 · Fig. 7(c) · Fig. 8(c)(d) 전수** (모두 **4 점**: 25/15/5/−5 °C):

| 셀 | `Ea(R₁)` / kJ mol⁻¹ | `Ea(R₂)` / kJ mol⁻¹ | 낮은 σ 쪽 SE 의 벌크 `Ea` |
|---|---:|---:|---:|
| LPSI \| LPSCl (Fig. 5a) | **36.4 ± 0.4** | **41 ± 3** | LPSCl **40.5 ± 0.3** ✅ |
| LGPS \| LPSI (Fig. 5b) | **33.4 ± 0.2** | **27 ± 3** | LPSI **29.8 ± 0.3** ✅ |
| LGPS \| LPSCl (Fig. 5c) | **40.8 ± 0.2** | **42 ± 1** | LPSCl **40.5 ± 0.3** ✅ |
| **LPSCl \| LPSCl** (Fig. 7c) | **45.5 ± 0.1** ⚠ | **39 ± 2** | LPSCl **40.5 ± 0.3** ✅ |
| LPSI \| LPSCl @560 kPa (8c) | 37 ± 2 | 41.5 ± 0.3 | |
| LPSI \| LPSCl @840 kPa (8d) | 37.0 ± 0.6 | 42 ± 3 | |

`[인쇄]` 결론: **"the Ea of R2 … is to the same extent as that of the Li-ion transport in
the solid electrolyte having lower ionic conductivity."** ⇒ 3 과정 도식(Fig. 6) 중
**한쪽 SE\|interphase 계면**이 율결정 단계다.

★★★★ **비판 1 — 자기 벌크값과 5.0 kJ mol⁻¹ 어긋난다(G10).**
LPSCl\|LPSCl 셀의 `R₁` 은 **정의상 LPSCl 벌크뿐**이다. 그 `Ea` 가 **45.5 ± 0.1** 인데
같은 물질의 Table 1 값은 **40.5 ± 0.3** 이다. **인쇄된 ± 로는 12σ 이상 떨어져 있고
논문은 언급하지 않는다.**
⇒ ★★★★ `[해석]` **이 편이 우리에게 주는 가장 값진 숫자는 여기다**: **"같은 물질, 같은
그룹, 두 측정계" 의 `Ea` 불일치 ≥ 5 kJ mol⁻¹ = 인쇄된 회귀 표준오차의 12–50 배.**
⇒ **모든 `Ea` 비교의 실질 허용오차는 ±0.1–3 이 아니라 ≥ ±5 kJ mol⁻¹ 다.**
그 눈금으로 다시 보면 **논지의 네 비교(41↔40.5 · 27↔29.8 · 42↔40.5 · 39↔40.5)는 여전히
통과하지만, "다르다" 를 말할 해상도가 없어진다** — 예컨대 `Ea(R₂)` 27 과 LGPS 벌크 37 의
차(10)는 유의하고, 41 과 36.4 의 차(4.6)는 **유의하지 않다.**

★★ **비판 2 — 저자 자신이 `Ea` 가 성형법으로 11 kJ mol⁻¹ 움직인다고 적었다**(§3.1,
LGPS 냉간 ↔ 열간). 그 진술과 위 논증은 **같은 지면에서 충돌한다.**

★★ **비판 3 — 자유도.** `Ea(R₂)` 후보가 **세 개**(SE1 벌크 · SE2 벌크 · 계면 고유)이고
관측이 **네 조합**이다. 네 조합 중 **세 개가 LPSCl 을 포함**하므로 사실상 독립 점은
**LGPS\|LPSI 하나**뿐이다. ⇒ **"낮은 σ 쪽" 규칙을 반증할 수 있었던 유일한 표본이 1 개다.**

★★★ **비판 4 — Fig. 6 의 지표가 본문과 다르다**(D5). 본문은 `[인쇄]` "**(ii)** is the
rate-determining step when the ion conductivity of **SE1 is higher than** that of SE2"
라고 쓰는데, **(ii) 는 캡션상 `SE1 | interphase` 계면**이다. SE1 이 **더 좋은** 쪽이면
느린 곳은 **SE2 쪽 = (iii)** 이어야 한다. `[도표]` **Fig. 6 자신이 "Slow" 를 (iii) 위치
(SE2 쪽)에 그린다.** ⇒ **본문 지표가 자기 그림·자기 논리와 어긋난다.**
(결론 절은 `[인쇄]` "at the interface of **one side of the SE**" 로 지표를 피한다.)

# §3.6 같은 전해질끼리 — 계면 유무 대조 (Fig. 7) ★★★ 이 편의 가장 강한 근거

- **LPSCl 셀**: 한 장의 LPSCl 펠릿 **안에 RE 두 개**를 함께 성형 ⇒ **적층 계면 없음**.
- **LPSCl \| LPSCl 셀**: LPSCl 펠릿 **두 장을 포갠 것** ⇒ **적층 계면 하나만 추가**.

`[도표]` 판독:
- (a) 단일 펠릿: Z′ **72 → 162 Ω**. **P1** 뒤에 **넓은 P3 혹(≈125 → 160, ≈35 Ω)**.
  **P2 없음.**
- (b) 적층: Z′ **225 → 300 Ω**. P1(가파른 선) → P3 → **작은 P2(≈291 → 299, `R₂` ≈ 8 Ω)**.
- (c) 적층 셀의 Arrhenius: **`Ea(R₁)` = 45.5 ± 0.1**, **`Ea(R₂)` = 39 ± 2**.

`[인쇄]` "which is **consistent with the assignment of P2** as Li-ion transport between
two solid electrolyte pellets."

⇒ ★★★ `[해석]` **이것이 `assb` 계보에서 우리가 본 가장 깨끗한 대조군 형태다**:
**같은 재료 · 같은 공정 · 계면 하나만 추가 → 임피던스 성분 하나만 생김.**
접촉 손실 연구가 원하는 **"면적/계면을 아는 대조군"** 의 교과서적 모양이고,
**18호 검사 A(입자 크기 축)가 실패했던 자리의 대안**이다.
⚠ 단서 셋: ① 두 셀의 `R₁` 이 **162 ↔ 291 Ω** 로 1.8 배 다르다 ⇒ **`d` 나 `S` 가 다르다**
(값 미인쇄) ⇒ 완전한 동일 조건이 아니다. ② **P3 가 양쪽에 다 있고 크기가 다르다.**
③ **n = 1.**

# §3.7 압력 (Fig. 8) — Q6

`[인쇄]` "we examined the **dependence of pressure** applied to the cell to evaluate the
influence of the **physical state of the interface**."

`[도표]` **Fig. 8(b) — 점 두 개**:

| 압력 | `R₁` | `R₂` |
|---:|---:|---:|
| **560 kPa** | **≈79.5 Ω** | **≈24.7 Ω** |
| **840 kPa** | **≈74.3 Ω** | **≈18.2 Ω** |
| **변화** | **−6.5 %** | **−26 %** |

`[인쇄]` "Both R1 and R2 values decrease with the increase in pressure, **possibly due to
the increases in the contact areas of SE particles and SE pellets**, respectively."
`[인쇄]` "the Ea values of both R1 and R2 **do not show pressure dependence**" ⇒
`[인쇄]` "**the physical state of the interface does not affect the Ea but the resistance
values. It is thus proposed Ea as the essential parameter to describe the nature of the
ion transport in this measurement system.**"

★★★★ **우리에게 이것이 이 편의 두 번째 수확이다.** 다시 쓰면:
> **압력(= 접촉 면적)은 `R` 을 움직이고 `Ea` 를 움직이지 않는다.**
> ⇒ **`Ea` 는 접촉 면적에 불변인 관측량이고, `R` 은 (면적) × (장벽 인자) 의 곱이다.**

⇒ **우리 곱 축퇴 처방에 `C_dl` 과 독립인 두 번째 채널이 생긴다**(아래 §곱 축퇴 검사).

⚠⚠ **그러나 근거는 약하다**:
1. **점이 둘뿐이다.** "dependence" 를 2 점으로 말한다.
2. `[재현]` **조립 기본값(ca. 420 kPa)의 Table 2(b) `R₂` = 21.5 Ω 가 560 kPa 의 24.7 Ω
   보다 작다** — **압력 추세와 반대**다(G9). ⇒ **셀 간 산포가 압력 효과보다 크다**는 뜻이
   거나 같은 셀이 아니라는 뜻인데, **논문은 둘 다 확인하지 않는다.**
3. `Ea` 불변의 판정 근거는 **37 ± 2 ↔ 37.0 ± 0.6**(R₁)과 **41.5 ± 0.3 ↔ 42 ± 3**(R₂)이다.
   `[재현]` **위 G10 의 실질 허용오차 ≥ ±5 kJ mol⁻¹ 을 쓰면, 이 데이터는 `Ea` 가 압력에
   불변이라는 것도 변한다는 것도 구별하지 못한다** — 압력이 `Ea` 를 **3 kJ mol⁻¹ 움직여도
   못 본다.**
4. **압력 범위가 1.5 배뿐이다** (560 → 840 kPa). 5호(Doux)는 1 → 25 MPa 에서 임피던스를
   >15 배 움직였다.

★ **그래도 Q6 에서 새로운 것**: `[재현]` 운전 압력 **0.42 / 0.56 / 0.84 MPa** 는
**이 계보 최저 대역**이고, **8호가 인쇄한 산업 요구치(<≈1 MPa) 안에 들어오는 첫 편**이다.
(비교: 16호 97 / 389 MPa · 17호 50 MPa · 18호 미보고 · 5호 1–75 MPa · 6호 2–4 MPa.)

# §4 결론 (인쇄된 것)

`[인쇄]` ① 황화물 SE 사이 계면의 Li⁺ 수송 저항을 **AC 임피던스로 성공적으로 평가**.
② 그 `Ea` 가 **낮은 이온전도도 쪽 SE 의 벌크 `Ea` 와 비슷**. ③ 그래서 **율결정 단계는
한쪽 SE 의 계면에서의 Li⁺ 수송**. ④ 이 셀은 다른 solid\|solid 계면에도 쓸 수 있다 —
`[인쇄]` "**as long as the Li-In counter and R-LTO reference electrodes function stably**",
안 되면 **전극 재료를 바꾸면 된다**.
⚠ ④의 단서가 이 편의 **미검증 전제를 한 줄로 요약한다** — "안정적으로 작동한다면".

# SI 전수

| Fig. | 무엇 | 우리 메모 |
|---|---|---|
| **S1** | **4 / 3 / 2 전극의 전위 프로파일 도식** | ★★★★ **이 편의 개념 핵심.** 빨간 선 = 셀을 가로지르는 전위. (a) 4전극은 **두 RE 팁 사이의 계단만** 잰다 — CE 두 개의 분극과 대부분의 벌크 강하가 빠진다. (b) 3전극은 **WE 분극을 포함**. (c) 2전극은 **전부 포함**. ⇒ **"4전극이 3전극보다 무엇을 더 재는가" 의 그림 답** |
| **S2** | 이온전도도용 2전극 셀 도식 (Au 분말, φ10 mm × 1.0 mm, 부틸 고무 링) | Table 1 의 출처. **직접 보지 않음 — 본문 서술로 충분** |
| **S3** | LGPS · LPSCl · LPSI 의 XRD (ICSD #193947 · #11900 대조) | **직접 보지 않음 — 본문 서술과 SI 텍스트로 충분**. LPSI 는 참조 패턴 없음(glass-ceramic) |
| **S4** | **Li-In 상대극의 `E_CE`(t) + `I`–`E_CE`, 세 셀** | ★★★★ **Q5 의 1 차 증거.** 위 §3.2(나) 전수 |
| **S5** | **Li-In 전극의 Nyquist(3전극) + 구성 도식** | ★★★★ 위 §3.3(다). ⚠ **캡션이 "Figure S **5**" 로 띄어져 있어 캡션 크로퍼가 놓쳤다** — SI p.6 을 직접 렌더해서 봤다 |
| **S6** | LPSI\|LPSCl 의 Nyquist 4 온도 | `[도표]` 25/15/5/−5 °C: `R₁` ≈ **84.5 / 139 / 241 / 437 Ω**, `R₂` ≈ **20.5 / 41 / 72 / 128 Ω**. `[재현]` 거기서 계산한 `Ea` = **36.4 / 40.6 kJ mol⁻¹** — **인쇄값 36.4 ± 0.4 / 41 ± 3 과 1 % 안에서 일치**(우리 판독의 자기 검증) |
| **S7** | LGPS\|LPSI 의 Nyquist 4 온도 | **직접 보지 않음** — SI 텍스트의 축 범위만 확인(Z′ 최대 ≈200 / 350 / 600 / 1000 Ω) |
| **S8** | LGPS\|LPSCl 의 Nyquist 4 온도 | **직접 보지 않음** — 축 범위 ≈180 / 300 / 600 / 1200 Ω |

# 어긋남 원장 (본문 ↔ 그림 ↔ SI ↔ 계산)

| # | 어긋남 | 근거 |
|---|---|---|
| **D1** | ★★ **Fig. S5 패널 배정이 본문과 SI 캡션에서 다르다.** 본문: "(a) LGPS \| LPSCl, (b) LGPS \| LPSI, (c) LPSI \| LPSCl". SI 캡션: "(a) LPSI \| LPSCl, (b) LGPS \| LPSI, (c) LGPS \| LPSCl". **(b)만 일치** | 본문 §3.3 ↔ SI p.6 |
| **D2** | ★ **4전극의 역할이 서론에서 뒤집혀 있다**: `[인쇄]` "two **reference** electrodes for **charge compensation** and two **counter** electrodes for **potential measurement or control**". Fig. S1·§2.3 은 반대(RE 가 전위, CE 가 전류) | 본문 p.1 ↔ Fig. S1 |
| **D3** | ★★ **Table 2 의 특성 주파수 세 칸의 지수 부호가 틀렸다**: **2.4×10⁻⁷**(b P1) · **9.1×10⁻⁶**(c P1) · **3.2×10⁻⁴**(c P3). `[재현]` `1/(2πτ)` 로는 **2.4×10⁷ · 9.4×10⁶ · 3.2×10⁴ Hz**. 표 이미지를 직접 확인 — 추출 오류가 아니다 | Table 2 |
| **D4** | ⚠ **LPSCl 의 `Ea` 40.5 를 문헌 "11–34 kJ mol⁻¹" 과 "similar" 라고 한다** — 범위 밖으로 6.5 벗어난다 | §3.1 ↔ Table 1 |
| **D5** | ★★★ **율결정 단계의 지표가 본문과 Fig. 6 에서 다르다.** 본문 "(ii) … when SE1 is **higher**"; Fig. 6 은 **"Slow" 를 SE2 쪽 = (iii)** 에 그린다 | §3.5 ↔ Fig. 6 |
| **D6** | ★★★ **`R₂` vs `d` 의 "의존성 없음" 이 이상치 한 점에 달려 있다.** `[도표]` `R₂/d` = 17.0 / 3.3 / 3.0 / 3.2 Ω mm⁻¹ | Fig. 4(d) |
| **D7** | ★★ **`R₁` vs `d` 에 원점 아닌 절편이 있다.** `[재현]` 최소자승 기울기 107 Ω mm⁻¹, **절편 ≈ +26 Ω**(d = 1 mm 에서 `R₁` 의 20 %). 논문은 **원점 통과 점선**을 그린다 | Fig. 4(c) |
| **D8** | ★★ **`R₂·S` 가 2.3 배 흩어지는데 "roughly in proportion" 이라 한다.** `[도표]` 112 / 105 / 244 Ω mm² — 세 번째 점만 2.2 배 | Fig. 4(b) |
| **D9** | ★★★ **LGPS\|LPSCl 의 CV 기울기(≈114 Ω)와 Nyquist 총합(183 Ω)이 1.6 배 어긋난다.** 다른 두 셀은 5 % 안에서 맞는다 | Fig. 2(c) ↔ Fig. 3(c)/Table 2(c) |
| **D10** | ★★★★ **LPSCl\|LPSCl 셀의 `Ea(R₁)` = 45.5 ± 0.1 ↔ Table 1 의 LPSCl 벌크 40.5 ± 0.3.** `R₁` 은 정의상 LPSCl 벌크뿐이다. 논문 무언급 | Fig. 7(c) ↔ Table 1 |
| **D11** | ★★ **등가회로(Fig. 3d)에 P3 와 직렬저항이 없는데 Table 2(c)는 P3 를 인쇄한다** | Fig. 3(d) ↔ Table 2(c) |
| **D12** | ★★ **"symmetric linear" 이라 하는데 Fig. 2(c)는 OCV 가 +25 mV 여서 ±50 mV 스윕이 전류축에서 비대칭이고**(+0.20 ↔ −0.68 mA) **음의 끝에 이력 고리가 보인다** | §3.2 ↔ Fig. 2(c) |
| **D13** | ★ **`P1` 의 꼭짓점이 측정 상한(7 MHz) 밖인데 `R₁` 을 3 유효숫자로 인쇄한다**(208 · 84.5 · 149). `[도표]` 세 Nyquist 모두 고주파 쪽이 닫히지 않고, (b)는 원호 208 Ω 중 **≈55 Ω(26 %)** 만 측정됐다 | Fig. 3 · Table 2 |
| **D14** | ★ **진폭 비의존성으로 "RE artifact 아님" 을 주장한다**(G12) — 선형 artifact 는 정의상 진폭 무관이다. **18호의 "K–K 잔차 → 기준극 안정성" 과 같은 구조** | §3.3 |
| **D15** | ⚠ **`Li-In` 과 `InLi` 표기가 같은 문단에서 섞인다**(본문 11 ↔ 2 회). 조성 표기도 "Li: In = 25: 75 at%" 와 "In-Li alloy film" 이 섞임 | §2.1 · §3.3 |
| **D16** | ⚠ **서론에 문장 중복**: "and the reference electrodes were placed on both sides of the electrolyte solution" 이 **같은 문장 안에서 두 번** 나온다 | p.1 우단 |

# ★★★ 곱 축퇴 검사 — 16호 처방의 **세 번째 적용**

처방(16호에서 세우고 18호에서 정련):
> **`R_CT·C_dl` 은 접촉 면적이 소거된 고유 시상수이고 `C_dl` 단독은 면적에 비례한다.
> 둘을 같이 보고하고, 여기에 *면적을 아는 대조군* 을 붙이면 `θ` 와 `j₀` 가 갈린다.**

## 입력 점검

| 처방 입력 | 9호 | 16호 | 17호 | 18호 | **19호 (이 편)** |
|---|---|---|---|---|---|
| `R` | 적합 | Table 2 | 없다 | Table S1 + Fig. 5 | ✅ **Table 2 (3 셀 × 2–3 성분)** |
| `C` / CPE `Q` | 없다 | Table 2 | 없다 | Table S1 (± 없음) | ✅ **Table 2 — 저자가 Brug 식으로 직접 계산해 인쇄** |
| CPE 지수 `p` | — | 0.89/0.81 | — | Table S1 | ✅ **0.55 – 0.96** |
| 면적을 바꾼 조작 | 없다 | 압력 2 점 | 없다 | 입자 크기 2 점 + 노화 | ✅ **압력 2 점 · 단면적 3 점 · 계면 유무 대조** |
| **면적을 아는 대조군** | 없다 | 없다 | 없다 | ⚠ **실패**(신품 입자크기) | ⚠ **있다(단면적 `S` 3 점) — 그러나 그 축에 `C` 가 인쇄되지 않았다** |
| **판정** | 곱을 적합 | 곱 위에서 한쪽을 골랐다 | 곱을 안 만들었다 | ★ 갈랐다(전제는 흔들림) | ★ **부분 적용 + 전제 반증 + 대체 채널 획득** |

## 검사 A — 절대 크기 (전제의 직접 검사) ⇒ **반증**

`[재현]` `P2` 의 용량 **1.6 – 3.8 mF**. 기하 단면(φ10 mm = 0.785 cm²)으로 나누면
**2.0 – 4.8 mF cm⁻² = 2000 – 4800 µF cm⁻²**.
이중층 비용량을 **10 µF cm⁻²** 로 놓으면 실면적/기하면적 = **200 – 480 배**.

★★★★ **접촉 면적은 기하 면적을 넘을 수 없다.**
⇒ **`P2` 의 `C` 는 접촉 면적의 대리가 될 수 없다.** 남는 해석은 (ㄱ) 화학용량/공간전하
(ㄴ) 계면의 거칠기가 아니라 **분포형 요소**(`p` = 0.55–0.61 은 극단적으로 눌린 CPE)
(ㄷ) Brug 변환이 이 `p` 에서 물리 용량을 주지 않는다 — **셋 다 검토되지 않았다.**

⇒ ★★★ **18호 검사 A 가 "예측보다 2–3 배 빗나감" 이었다면, 19호는 "물리 상한을
2–3 자릿수 초과" 다.** 전제가 **같은 방향으로 두 번 연속 깨졌다.**

## 검사 B — 셀 간 축 (`C` 채널 ↔ `Ea` 채널의 정면 충돌)

`[재현]` `P2` 세 셀:

| 셀 | `R₂`/Ω | `C₂`/mF | `τ₂`/ms | `Ea(R₂)` |
|---|---:|---:|---:|---:|
| LGPS \| LPSI | **12** | **3.8** | 46 | **27 ± 3** |
| LPSI \| LPSCl | **21.5** | **1.7** | 36 | **41 ± 3** |
| LGPS \| LPSCl | **29.3** | **1.6** | 46 | **42 ± 1** |

- **`C` 채널**: `τ = R·C` 가 **36 – 46 ms, ±13 % 안**. `R` 비 (LGPS\|LPSCl)/(LGPS\|LPSI)
  = **2.44**, `C` 비(역방향) = **2.375** — **3 % 안에서 일치**.
  ⇒ **"세 계면은 유효 면적만 다르다"**(= 순수 `θ` 변동). 논문 자신도 같은 관찰을
  `[인쇄]` "similar fitting parameters … including the time constant … **not different
  among the three cells**" 로 적는다.
- **`Ea` 채널**: **27 ↔ 42 kJ mol⁻¹, 15 kJ mol⁻¹ 차이.**
  `[재현]` 298 K 에서 `A = R·exp(−Ea/RT)` 로 환산한 **전지수 인자**:
  **2.21×10⁻⁴ / 1.40×10⁻⁶ / 1.27×10⁻⁶** ⇒ **A 비가 158 – 174 배.**
  ⇒ **"세 계면은 장벽이 다르고, 전지수 인자(≈면적)가 158–174 배 반대로 보상한다"**
  (= 순수 `j₀` 변동 + 거대한 보상 효과).

★★★★ **두 채널이 70 배 어긋난다**: `C` 는 면적 차 **2.4 배**를 말하고, `Ea` 를 믿으면
면적 차 **158–174 배**가 필요하다.
⇒ `[해석]` **이 편에서 `C_dl` 과 `Ea` 는 같은 곱의 두 인자를 서로 다르게 나눈다.
둘 다 맞을 수는 없고, 검사 A 가 `C` 쪽을 의심할 이유를 준다.**
⚠ 단서: 이것은 **노화 축이 아니라 재료 축**의 비교다(세 계면이 물리적으로 다른 계면).
**동일 계면의 두 상태**를 비교한 18호 검사 B 와 성질이 다르다 — 여기서는 "면적만 다르다"가
애초에 성립할 이유가 없다.

## 검사 C — 압력 축 ⇒ **적용 불가, 그러나 대체 채널 획득**

`[도표]` 560 → 840 kPa 에서 `R₂` −26 %. **`C₂`·`Q`·`p` 는 두 압력에서 인쇄되지 않는다.**
⇒ **면적을 바꾼 조작이 있는데 `C` 가 그 축에 없다** — 18호와 정확히 반대의 결손
(18호는 `C` 는 있고 면적을 아는 조작이 실패했다).

★★★★ **대신 논문이 다른 채널을 준다**: `[인쇄]` **압력이 `R` 을 바꾸고 `Ea` 는 안 바꾼다.**
⇒ **처방에 줄이 하나 추가된다**:

> **`Ea` 는 접촉 면적에 불변인 관측량이다.**
> `R(T) = A(θ) · exp(Ea/RT)` 에서 **`Ea` 는 `θ` 와 직교하고 `A` 만 `θ` 를 탄다.**
> ⇒ **노화 전후의 `Ea` 를 같이 재면, `C_dl ∝ θ` 라는 (두 번 깨진) 전제 없이도
> "면적이 줄었나 화학이 나빠졌나" 의 필요조건 검사를 할 수 있다.**
> - `Ea` 불변 + `R` 증가 ⇒ **면적/기하 쪽**과 양립
> - `Ea` 증가 ⇒ **화학/장벽 쪽** (면적만으로는 설명 불가)
> ⚠ **충분조건은 아니다** — `A` 에는 면적 외에 시도 빈도·엔트로피가 들어간다
> (검사 B 의 보상 효과가 그 증거다).

★★★ **그리고 이것이 18호로 되돌아간다**: 18호는 `Ea` 를 **신품 축에서만** 쟀다
(Table 1 의 입자 크기 × SoC). **노화 전후 `Ea` 가 없다.**
⇒ **18호가 `Ea(before/after)` 를 쟀다면 검사 B 의 결론(LPSI = 면적 + 화학, LPSCl = 화학만)이
`C` 없이도 독립으로 확인됐을 것이다.** ⇒ **처방 P 목록에 올린다.**

## 세 번째 적용의 요약

| | 16호 | 17호 | 18호 | **19호** |
|---|---|---|---|---|
| 처방 적용 | 입력 절반 | **불가** | **성공(갈랐다)** | **부분** |
| 전제 `C ∝ θ` | 미검증 | — | ⚠ **신품 축에서 2–3 배 빗나감** | ❌ **절대 크기가 200–480 배 초과** |
| 면적을 아는 대조군 | 없다 | 없다 | 실패 | ⚠ **있다(S 3 점 · 계면 유무) — `C` 가 안 붙어 있다** |
| **새로 얻은 것** | 처방 | "왜 불가" | "두 값 + 대조군" | ★ **면적-불변 채널 `Ea`** |

# Q1~Q8 판정 (채움표 19호 행의 근거)

| | 판정 |
|---|---|
| **Q1 접촉 손실 정량** | **없다.** `contact area` 2 회 · `contact loss` 1 회(서론, 인용) · `θ`·`percolat*`·`porosit*`·`tortuos*` **0 회**. ★ 유일한 인과 사용은 `[인쇄]` 압력 효과를 "possibly due to the **increases in the contact areas**" 로 설명하는 한 줄이고 **값이 없다**. ⇒ `R(P)` 는 있고 `θ(P)` 는 없다 — **`assb` 19/19 편이 `θ` 를 상태축 위에서 주지 않았다** |
| **Q2 독립 관측** | **해당 없음에 가깝다 — 활물질이 없다.** 채널은 많지만(4전극 구성 · `S` 3 점 · `d` 4 점 · 계면 유무 대조 · Li-In 3전극 임피던스 · 압력 2 점 · 온도 4 점) **`LAM_PE` ↔ 접촉 손실을 가르는 데 쓰인 조합은 0** 이다. ★ 다만 **설계 형태를 하나 준다**: **"같은 재료 · 계면 하나만 추가" 대조군**(Fig. 7) — 접촉 손실 연구가 원하는 대조군의 교과서적 모양. ⇒ **칸은 안 올린다** |
| **Q3 라벨 층위** | **fitted(등가회로) + measured(Nyquist 절편·기울기).** ± 는 **Arrhenius 4 점 회귀의 표준오차**뿐이고 셀 간 반복이 **0**(`n =` 실질 0 회). ★★★★ **그런데 이 편이 스스로 산포 하한을 드러낸다**: **같은 물질 LPSCl 의 `Ea` 가 두 측정계에서 40.5 ± 0.3 ↔ 45.5 ± 0.1** (D10) ⇒ **실질 허용오차 ≥ 5 kJ mol⁻¹ = 인쇄된 ± 의 12–50 배.** 그리고 **Li-In 전극 임피던스 39 ↔ 172 Ω (4.4 배, n = 3)**, **`P3` 가 셀마다 7 배** |
| **Q4 유일성** | **0 / 19.** 어휘 **전수 0 회**(NFKC · 대소문자 구분, 오검출 0 확인). ★★★ **열두 번째 성질 = "어휘 없이 귀속을 실험으로 물은 첫 편"** — 성분의 정체를 적합 통계가 아니라 **기하 섭동**(단면적·간격)과 **대조군**(계면 유무)으로 묻는다. **그러나 ① 설계의 절반이 판별력이 없고**(`1/S` 축은 벌크·계면을 못 가른다) **② 결정적 축의 점이 4 개이고 그중 하나가 4.5 배 이상치이며**(D6) **③ 적합 자체의 유일성(조건수·근최적 폭·λ·다중 출발)은 전혀 안 쟀다.** ★ 그리고 **비분리를 자기 데이터로 증명한 첫 편**이다 — `[인쇄]` "P1 and P2 are **difficult to extract** from the … two-electrode system" |
| **Q5 Li-In / 기준극** | ★★★★ **있다 — 그리고 성질이 네 편 중 가장 다르다.** ① **기준극의 절대 전위를 가정하지 않는다** — 측정량이 RE₂ − RE₁ 이라 소거된다. `assum*` **0 회**, "1.55" **0 회**(18호의 G4 가 여기서는 생기지 않는다). ② **대신 기준극 쌍의 재현성이 인쇄된다**: `[인쇄]` **ca. ±30 mV**(⚠ 근거 미제시, G4). ③ **R-LTO 의 조성이 처음 인쇄된다**: `[인쇄]` **Li₇Ti₅O₁₂ : Li₄Ti₅O₁₂ = 67 : 33 mol%** — 2 상 한복판. ④ ★★★★ **Li-In 상대극의 비평탄이 4전극으로 직접 찍힌다**: `[인쇄]` "not linear" · "asymmetric", `[도표]` **42 / 126 / 75 mV** 이동, `[재현]` **0.41–1.07 mA cm⁻²**, **가역**(재고의 0.39 %만 통과). ⑤ `[재현]` **(ㄱ)(ㄴ)은 만족하고 (ㄷ)만 깬 첫 표본** ⇒ **(ㄷ) 단독으로는 10⁻²–10⁻¹ V 대에 머문다.** ⑥ `[재현]` 18호의 1.55 V 를 빌리면 **Li-In ≈ 0.60 V @ 25 at%** — 17·18호(40 at%)와 일치 |
| **Q6 압력** | **★★ 있다 — 계보 최저 대역.** 조립 **ca. 420 kPa**, 스윕 **560 / 840 kPa**(2 점). 성형은 **280 MPa**(4전극 펠릿) · 140 + 280 MPa(전도도 셀). ★ **8호가 인쇄한 산업 요구치 <≈1 MPa 안에 들어오는 첫 편.** ★★★ **`R` 은 움직이고 `Ea` 는 안 움직인다**(`[인쇄]`) ⇒ **면적-불변 관측량**. ⚠ 2 점 · n = 1 · 범위 1.5 배 · `[재현]` **420 kPa 의 `R₂`(21.5 Ω)가 560 kPa(24.7 Ω)보다 작아 추세와 반대**(G9) |
| **Q7 dead Li** | **해당 없음.** `dendrit*`·`dead`·`isolat*` **0 회**. Li-In 상대극이고 도금/스트리핑 실험이 없다 |
| **Q8 화학·OCP** | **해당 없음 — 전극이 없다.** 활물질·용량·V–Q 곡선 **0**. `OCV`·`GITT` 0 회. ★ 유일한 "개방회로" 는 **RE–RE 전위차**이고 값이 **−4 / −5 / +25 mV** ⇒ `[인쇄]` **황화물 세 종 사이에 검출 가능한 Li⁺ 활동도 차가 없다**(검출 하한 ±30 mV). ★ 이 편이 주는 물성: **σ 와 `Ea` 3 종**(Table 1) + **계면 저항 4 종**(LPSI\|LPSCl 21.5 · LGPS\|LPSI 12 · LGPS\|LPSCl 29.3 · LPSCl\|LPSCl `[도표]` ≈8 Ω) |

**채움표 누적: 18편 ≈10.5 → 19편 ≈11.0** (**Q5 +0.5** — 기준극의 절대 전위를 **측정
구조로 제거한 첫 편**이고, **기준극 쌍 재현성 ±30 mV 를 인쇄한 첫 편**이며, **Li-In
상대극의 비평탄을 4전극으로 직접 잰 첫 편**이다. 반 칸인 이유 둘: **±30 mV 의 근거가
지면에 없고**, 이동 폭이 **가역 분극**이라 17호의 지속 이동과 같은 양이 아니다).
**Q1 은 그대로 ≈0.5 · Q4 는 그대로 0.**
⚠ **Q2 +0.5 를 검토했다가 접었다** — 이 편에는 **활물질이 없어** `LAM_PE` ↔ 접촉 손실을
가를 대상 자체가 없다. 준 것은 **값이 아니라 대조군의 형태**다.

# ★★★ 18호와의 대질 — 같은 그룹, 한 칸 더 간 자리와 그대로인 자리

| | **18호 (Fukunishi 2023, 3전극)** | **19호 (이 편, 4전극)** |
|---|---|---|
| 측정 대상 | NCM523 복합양극 + Li-In 음극 | **SE \| SE 계면 하나** |
| 기준극 | R-LTO 메시 | **R-LTO 메시 2 개** |
| 기준 전위 | `[인쇄]` "**Assuming** … **1.55 V**" | ★★★★ **가정 없음 — 차분으로 소거.** `assum*` 0 회 |
| R-LTO 조성 | "partially reduced"(미상) | ★ **Li₇Ti₅O₁₂ : Li₄Ti₅O₁₂ = 67 : 33 mol%** |
| 기준극 검증 주장 | **K–K 잔차 ±0.4** (범주 오류) | **진폭 비의존성** (범주 오류) — **같은 구조** |
| 기준극 재현성 | 없다 | ★★★ **ca. ±30 mV**(근거 미제시) |
| Li-In 의 역할 | 상대극, `[도표]` **평탄 ≈0.60 V** | 상대극, `[인쇄]` **"not linear" · "asymmetric"**, `[도표]` **42–126 mV** |
| 전류밀도 | 0.054 mA cm⁻² | **0.41 – 1.07 mA cm⁻²** (8–20 배) |
| 압력 | `pressure` **0 회** | `pressure` 4 · `kPa` 5 · **스윕 2 점** |
| `Ea` | Table 1(입자 크기 × SoC, 신품만) | **계면 4 종 + 압력 2 점** — **노화 축은 둘 다 없다** |
| `C` / CPE | Table S1(± 일부) | **Table 2 전수** |
| **곱 축퇴** | ★ **갈랐다**(C 비 0.37 ↔ 1.07) | ⚠ **`C` 와 `Ea` 가 70 배 충돌 · 전제 절대 크기 반증** |
| DRT · K–K | 쓴다 | **안 쓴다**(0 회) |
| 열화 | **있다**(50 사이클, 333 K) | **없다** |

★★★ `[해석]` **두 편을 겹치면 이 그룹의 방법이 무엇을 해결하고 무엇을 남겼는지가 보인다.**
- **해결**: 상대극 분극 제거(4전극) · 기준 전위의 절대값 제거(차분) · 기준극 쌍의
  재현성 숫자화.
- **남음**: **기준극이 스펙트럼에 미치는 영향을 검증하는 방법**이 두 편 다 **범주 오류**다
  (K–K ↔ 진폭). 올바른 검사는 **기준극 위치·개수·재료를 바꾸고 스펙트럼이 불변인지**
  보는 것이고, 두 편 다 안 한다.
- **그리고 노화 축의 `θ` 와 `Ea` 가 여전히 둘 다 0 이다.**

# ★★ 17호·16호와의 대질 — Q5 의 네 번째 점

| | 16호 (Ramanayagam) | 17호 (Yanev) | 18호 (Fukunishi) | **19호 (Yoshida)** |
|---|---|---|---|---|
| 기준극 | 리튬화 Au/W μ-RE | **Li 금속** | R-LTO(가정 1.55 V) | **R-LTO × 2 (차분)** |
| 기준 전위의 처리 | 설치하고 **미검증** | `E_CE` **실측**(RE 자체 미검증) | **가정** | ★ **소거** |
| Li-In `x_Li` | 5 – 28 at% | 40 at% | 37.7 → 40.0 at% | **25 at%** |
| Li-In 전위 관측 | `[도표]` 0.47 ↔ 0.58 V (두 셀) | `[인쇄]` 0.61 ↔ 1.35 V | `[도표]` ≈0.60 V 평탄 | `[재현]` **≈0.60 V**(가정 위) |
| 전위 **변동** 관측 | Δ0.11 V 셀 간 | **+0.68…+0.78 V**(지속) | ≈0 | **42–126 mV**(가역 분극) |
| 전류밀도 | 미보고 | 0.28 … 16 mA cm⁻² | 0.054 | **0.41 – 1.07** |
| 압력 | 97 / 389 MPa | 50 MPa | 미보고 | **0.42 – 0.84 MPa** |
| Li-In 임피던스 산포 | — | — | — | ★ **39 ↔ 172 Ω, 4.4 배 (n = 3)** |

★★★★ **`E_CE(j)` 의 점이 네 개가 됐다** (`[재현]`, 어느 편의 결론도 아니다):

| 전류밀도 | 관측 `ΔE_CE` | 출처 | 재고 여유 |
|---:|---:|---|---:|
| **0.054 mA cm⁻²** | **≈0** | 18호 | 9.5 배 |
| **0.41 – 1.07** | **42 – 126 mV**(가역) | **19호** | ≈260 배 |
| 0.28 | ±10 mV | 17호 0.1 C | ≈5 배 |
| ≈16 (CA) | **+680 – 780 mV**(지속) | 17호 | ≈5 배, **고갈** |

⇒ `[해석]` **재고 여유가 충분하면 전류밀도를 20 배 올려도 이동은 10⁻¹ V 에 못 미친다.
17호의 0.7 V 는 전류밀도가 아니라 고갈의 산물이다.**
⚠⚠ **이것은 네 편을 가로지르는 추론이고, 네 편은 SE·압력·조성·제조법이 전부 다른
관측이다. 통제 실험이 아니다.** (처방 **P7**: 재고비와 전류밀도를 독립 스윕.)

# ★★ Q2 — "EIS 분해 비유일성" 계보의 네 번째 층

- **10호(Vadhva)**: `[인쇄]` 유일해가 없다 + 전극↔주파수 귀속이 **화학의 함수**.
- **11호(Yu)**: 봉우리 **이름표가 상태·배선·조작으로 흔들린다**(−15 … +69 %).
- **16호**: 전극별 DRT 의 **합이 완전지 DRT 가 아니다**.
- **18호**: 같은 화학에서도 **양극의 미세구조**(단결정 ↔ 다결정)가 "저주파 = 음극" 을 깬다.
- **19호(새로 들어오는 것)**: ★★★★ **상대극이 관심 성분의 주파수대를 통째로 덮는다 —
  그리고 그것이 저자의 결론으로 인쇄된다.** `[인쇄]` Li-In 전극의 반원이
  **P1(>1 kHz)과 P2(1 kHz–0.1 Hz)** 둘 다와 겹치고, 그래서 2전극에서는 **"difficult to
  extract"**. **해법은 분해 알고리즘이 아니라 배선이다**(4전극).

★★★ **18호와의 관계 — 보강인가 충돌인가**: **보강이다, 그리고 한 층 아래로 내려간다.**
18호는 **"저주파 = 음극" 이 양극 미세구조의 함수**라고 했다(다결정 `R4` 가 같은 대역에
들어온다). 19호는 **"음극 자체가 1 MHz–0.1 Hz 전 대역에 걸쳐 있다"** 고 말한다.
⇒ **주파수 → 전극 규칙이 흔들리는 이유가 둘 다 "같은 대역의 중첩" 이고,
19호 쪽이 더 근본적이다 — 양극을 바꿔도 음극은 그대로 거기 있다.**
⇒ `[해석]` **두 편을 합치면: 주파수만으로 성분을 전극에 배정하는 모든 절차는
같은 셀 안에서 배선으로 검증되기 전까지 가설이다.**
그리고 **19호는 그 검증을 실제로 하는 배선을 보여 준다** — `assb` 에서 처음이다.

# 무엇이 우리 프로젝트로 넘어오는가

1. ★★★★ **면적-불변 관측량으로서의 `Ea`.** [[assb-lampe-contact-product-degeneracy]] 의
   처방에 `C_dl` 과 독립인 줄이 하나 생긴다. **노화 전후 `Ea`** 는 어느 편도 안 쟀다.
2. ★★★★ **"계면 하나만 추가" 대조군.** 접촉 손실을 재려면 **접촉을 아는 대조군**이
   필요한데(18호 교훈), 이 편이 그 형태를 보여 준다. 복합양극 판으로 옮기면:
   **같은 활물질 · 같은 SE · 같은 공정에서 계면 수/면적만 바꾼 전극 쌍.**
3. ★★★ **산포 하한의 실측**: 같은 물질 `Ea` 두 측정계 **≥5 kJ mol⁻¹** ·
   Li-In 전극 임피던스 **4.4 배** · `P3` **7 배**. ⇒ **등가회로 파라미터를 점추정으로
   보고하는 모든 `assb` 편에 대한 우리 비판의 야생 눈금.**
4. ★★★ **Q5 의 구조적 해법**: 기준 전위를 **재거나 가정하는** 대신 **소거하는** 설계가
   존재한다. 단 **RE 쌍의 불일치(±30 mV)가 새 바닥**이 된다.
5. ⚠ **가져오지 않는 것**: 이 편에는 용량도 열화도 활물질도 없다. **`θ(N)`·`LAM_PE`·
   `LLI` 에 대해 아무것도 주지 않는다.**

# 이 digest 가 주장하지 않는 것

- **논문의 결론(계면 `Ea` ≈ 낮은 σ 쪽 벌크 `Ea`)이 틀렸다고 주장하지 않는다.**
  네 조합이 전부 그 규칙을 만족한다. 비판은 **독립 표본이 사실상 1 개**라는 것,
  **허용오차가 인쇄된 ± 보다 한 자릿수 크다**는 것(D10), **율결정 단계의 지표가
  본문과 그림에서 다르다**는 것(D5)에 있다.
- **`P2` = 계면 이라는 배정이 틀렸다고 주장하지 않는다.** Fig. 7(계면 유무 대조)이
  그것을 강하게 지지한다. 비판은 **논문이 그것을 1 차 근거로 쓰지 않았다**는 것과
  **실제로 1 차 근거로 쓴 Fig. 4(d)가 4 점 · 이상치 1 개**라는 것이다.
- **`R₂/d` 의 비례(읽기 B)를 사실로 주장하지 않는다.** 그것은 **그림에서 읽은 4 점 중
  3 점**이고, 이상치를 배제할 독립 근거가 없다. 주장하는 것은 **같은 4 점이 정반대의
  두 읽기를 허용한다**는 것까지다.
- **`C` 와 `Ea` 의 70 배 충돌을 "면적이 안 변했다" 로 옮기지 않는다.** 세 계면은
  **물리적으로 다른 계면**이라 "면적만 다르다" 가 애초에 성립할 이유가 없다.
  주장하는 것은 **두 진단 채널이 같은 표에서 양립하지 않는다**는 것이다.
- **`Li-In ≈ 0.60 V` 를 이 편의 측정으로 쓰지 않는다.** 1.55 V 는 **18호에서 빌려온
  가정**이고 이 편에는 없다.
- **±30 mV 를 검증된 값으로 쓰지 않는다.** 근거가 지면에 없다 — ref [18] 에 있을
  가능성이 있고, 그것이 후속 1 순위인 이유다.
- **압력 결과를 다른 셀로 옮기지 않는다.** **0.56 – 0.84 MPa, 1.5 배 범위, 2 점, n = 1**,
  그리고 **SE\|SE 계면**이지 전극 계면이 아니다.
- **Q4 는 0 / 19 다.** **귀속을 실험으로 물었다**는 것이 **유일성을 쟀다**는 뜻은 아니다.
- 수치는 전부 **사본**이다. 정본은 원문 PDF 이고, `[도표]` 에는 판독 오차가,
  `[재현]` 에는 명시한 가정이 붙는다.

# 후속 후보

| 순위 | 논문 | 왜 |
|---|---|---|
| ★★★★ **1** | **Ikezawa, Fukunishi, Okajima, Kitamura, Suzuki, Hirayama, Kanno, Arai, *Electrochem. Commun.* 116 (2020) 106743** (ref [18]) | ★★★★ **이제 네 편(16·17·18·19호)이 전부 이것을 가리킨다.** 이 편의 **±30 mV 의 근거**(G4)와 18호의 **1.55 V 의 근거**(G4)가 **둘 다 여기 있어야 한다**. 그것이 없으면 이 계보 전체의 기준 축이 미검증이다. **큐에 없다 — 순위가 더 올라갔다** |
| ★★★ **2** | **Fukunishi, Ikezawa, …, Arai, *ACS Appl. Energy Mater.* 6 (2023) 10908** (ref [19]) — "Impedance analysis and **cyclability** evaluation of **graphite** composite electrodes with all-solid-state three-electrode cells" | ★★ **새로 보인 자매편.** 18호의 **흑연 음극 판**이고 **cyclability(= 열화)를 제목에 단다** ⇒ `θ(N)`·`Ea(N)` 이 있을 가능성이 이 계보에서 가장 높다. 11호(Yu 2024, 흑연 음극 완전지)와 직접 대질된다. **큐에 없다** |
| ★★★ **3** | **Abe, Sagane, Ohtsuka, Iriyama, Ogumi, *JES* 152 (2005) A2151** (ref [14]) | **이 편의 논증 틀(=`Ea` 로 율결정 단계를 정한다)의 원전.** 우리가 새로 채택하려는 **"`Ea` = 면적-불변 채널"** 의 타당 범위가 거기서 정해진다 (액체\|고체 계면). **큐에 없다** |
| ★★ **4** | **Brug, van den Eeden, Sluyters-Rehbach, Sluyters, *J. Electroanal. Chem.* 176 (1984) 275** (ref [27]) | **식 (1)의 원전.** 우리가 18호 검사 A 와 19호 검사 A 에서 두 번 쓴 변환이고, **`p` = 0.55–0.61 에서 이 변환이 물리 용량을 주는지**(G11)가 곱 축퇴 처방의 전제를 결정한다. **큐에 없다** |
| ★★ **5** | **Lewis, …, McDowell, *Nat. Mater.* 20 (2021) 503** (ref [8]) — operando X-ray tomography 로 **void ↔ interphase ↔ 전기화학** 연결 | 이 편이 "contact loss" 의 근거로 든 편이고, **5호(Doux 2020)의 형제**다. `θ(N)` 을 영상으로 준 몇 안 되는 후보. **큐에 없다** |
| ★ **6** | **Rosenbach, Walther, …, Janek, Zeier, *Adv. Energy Mater.* 13 (2022) 2203673** (ref [21]) | "황화물\|황화물은 안정·단순" 이라는 **이 편의 전제의 출처**. 반대로 할라이드\|황화물에서는 이 편의 방법이 무엇을 볼지 알려준다. **큐에 없다** |
| ★ **7** | **Shi, Tu, Tian, …, Ceder, *Adv. Energy Mater.* 10 (2020) 1902881** (ref [4]) | ⚠ **큐 21번**("Impact of Cathode Material Particle Size on the Capacity of Bulk-Type ASSB" 과 같은 주제축). 18호 검사 A(입자 크기 ↔ 접촉 면적)의 배경이고 **큐에 이미 있으니 순서만 당기면 된다** |

⚠ **큐 대조**: 위 **1–6 은 큐에 없다**. **7 은 큐 21번 계열**이다.
★ 그리고 **1 번(Ikezawa 2020)은 17·18호 digest 에서 각각 4 순위·1 순위였고 이번이
세 번째 지목**이다 — 이 계보의 기준 축이 **단 한 편에 걸려 있는데 그 편을 아직
안 읽었다.**

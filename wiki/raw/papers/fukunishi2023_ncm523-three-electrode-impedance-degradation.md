---
title: "Fukunishi, Tabuchi, Ikezawa, Okajima, Kitamura, Suzuki, Hirayama, Kanno, Arai 2023 — AC impedance analysis of NCM523 composite electrodes in all-solid-state three electrode cells and their degradation behavior (J. Power Sources 564, 232864)"
source_url: local-upload/17._AC_impedance_analysis_of_NCM523_composite_electrodes_in_all-solid-state_three_electrode_cells_and_their_degradation_behavior.pdf + 17._Sup_AC_impedance_analysis_of_NCM523_composite_electrodes_in_all-solid-state_three_electrode_cells_and_their_degradation_behavior.pdf (SI)
source_url_note: "본문 10쪽 (pp. 1-9 + 참고문헌 44편) + SI 6쪽 (Fig. S1-S4 + Table S1). 크로핑 13장(본문 그림 7 + SI 그림 4 + 표 2) 중 **11개 그림 파일을 전부 봄** — 본문 Fig. 1-7 + SI Fig. S1/S2/S3/S4. 여기에 캡션이 없어 크로퍼가 놓친 **1쪽 Graphical Abstract** 를 직접 렌더해 열람. 안 본 것: 표 크롭 2장(PDF 텍스트 사용). 누락은 `get_images()`/`get_drawings()` 페이지별 계수로 기계 확인. 1차 측정 있음 — 3전극 셀(LPSI/LPSCl 2계) + 대칭셀 2점 + 입자크기 2종, n 미상(`n =` 0회). `[인쇄]`/`[도표]`/`[재현]`/`[해석]` 4구분."
source_doi: 10.1016/j.jpowsour.2023.232864
source_license: "(c) 2023 Elsevier B.V. All rights reserved — 오픈액세스 아님"
pdf_sha256: c0798ee51006342906af994458fcf23aa89b1f676d95b7c3674a145cecb7abbb
si_sha256: 773e6fbca1d7b938b658aed52192ad671f72e784670dea9f23ae8c8428746588
ingested: 2026-09-22
sha256: b0cea42eff980b1b5918e9606e58b93500409dc46d0ebfccbcf5651afbd71657
---

# 수집 목적

`assb` 섹션 **18호**. 큐 **17번** (17호 = 큐 16 Yanev 2024 Li-In 음극, 16호 = 큐 15
Ramanayagam 2026 3전극×압력). 닻은 `questions/assb-contact-loss-vs-lampe.md`.
큐 문서(`bms-balancing/docs/ASSB_TRANSFER_NOTE.md`)의 등록 축은 **Q2 + 양극 열화**이고,
이 편은 **16호가 자기 ref [39] 로 든 유일한 외부 실측 대조군**이다 — 그래서 이번 흡수의
1순위는 새 지식이 아니라 **대질**이었다.

> **판정 한 줄 (먼저)**: 이 편은 `assb` 계보에서 **전극 분해(3전극)와 열화를 같은 셀에서
> 동시에 한 첫 편**이고, **컷오프를 완전지 전압이 아니라 작업전극 전위에 걸어
> 17호가 연 오염 경로(상대극이 겉보기 양극 용량을 민다)를 설계상 닫은 첫 편**이다.
> 그리고 **우리 닻 물음을 저자들이 문장으로 인쇄하고 가르지 않은 채 남긴다**:
> `[인쇄]` "the **chemical composition at the interface or the contact area** between the
> NCM523 and electrolyte particles changed". **또 하나**: `[인쇄]` "if insulative layers
> completely cover the active material to make the particle inactive, such **dead particles**
> probably have no contribution to the charge transfer process. This could explain the
> **large capacity decrease**" — 즉 **`θ_AM`(덮여서 죽은 입자)을 용량 손실의 기구로
> 명시하면서 값을 재지 않는다.**
> ★★★★ **그런데 이 편은 그 갈림을 가를 입력을 자기 지면에 갖고 있다** — Table S1 이
> `R3` 와 **CPE 용량**을 같이 인쇄하고, Fig. 5 가 **노화 전후의 `R`과 `τ` 를 둘 다**
> 인쇄한다. 16호에서 세운 처방(`R_CT·C_dl` 은 면적이 소거되고 `C_dl` 단독은 면적에
> 비례한다)을 **이 계보에서 처음으로 실제로 계산할 수 있었다**. 결과는 §곱 축퇴 검사:
> **LPSCl 의 `R3` 7.4 배 증가에는 면적 손실이 없고(`[재현]` C 비 1.07), LPSI 의 6.5 배
> 증가에는 있다(`[재현]` C 비 0.37 ⇒ 유효 면적 ≈2.7 배 감소 + 고유 `R_ct` ≈2.4 배 증가).**
> 그리고 **그 분해가 같은 논문의 SEM/EDX(LPSI 에만 입자를 덮는 O·P 층)와 독립으로
> 일치한다.** Q4(유일성 어휘) **0/18** — 다만 성질이 또 바뀐다: **축퇴를 "A 또는 B" 로
> 인쇄하고 가르지 않는다.**
> **Q6**: `pressure` **본문 0 회**. 제작 110 MPa(3전극)·150 MPa(대칭셀) 두 값뿐이고
> **운전 압력은 보고도 제어도 없다** — 주 열화 기구로 지목한 것이 **void 형성**인데도.

> 표기: `[인쇄]` 본문·SI 명시 · `[도표]` 그림에서만 읽은 값 (`figure-read ≈`, 판독 오차 붙음) ·
> `[재현]` 우리가 지면의 숫자로 계산한 값 · `[해석]` 우리 해석.
> **`[해석]` 표시 없는 문장은 원문이 실제로 말한 것이다.**

# 원문에 없어서 확인이 필요한 것 (공백 원장)

| # | 공백 | 왜 걸리나 |
|---|---|---|
| **G1** | **셀 개수가 어디에도 없다.** `n =` **0 회**, "cells" 는 늘 복수형인데 몇 개인지 안 적는다. 반복 측정·평균·표준편차 **0** | 조건당 n=1 로 읽을 수밖에 없다 (16·17호와 같은 층위) |
| **G2** | **운전 압력이 없다.** `pressure` **본문 0 회**. 셀은 PET 관에 110 MPa 로 압착한 뒤 `[인쇄]` "Ar-filled polystyrene container" 에 넣고 단자로만 측정한다 — **압착 상태가 유지되는지, 얼마로 유지되는지 한 줄도 없다** | 이 편의 결론이 **void 형성**이다. void 는 압력의 직접 함수다 |
| **G3** | **두 전해질계의 복합양극 조성이 다르다.** LPSI 계 `[인쇄]` **49 : 43 : 8.0**, LPSCl 계 **69 : 26 : 5.0 wt%**. 근거는 `[인쇄]` "optimized mixing ratios were determined with the **preliminary tests**" 뿐이고 그 데이터가 없다 | **LPSI ↔ LPSCl 비교 전체가 "전해질 종류" 와 "조성" 의 교락**이다. 활물질 40 % 더 많고 SE 40 % 적고 VGCF 38 % 적은 전극을 비교한다 |
| **G4** | **R-LTO 기준극의 전위를 재지 않았다.** `[인쇄]` "**Assuming** that the potential of the R-LTO reference electrode is **1.55 V** vs. Li/Li⁺ [32,33]" | 4호(Shi)의 "0.6 V 고정 가정" 과 같은 층위. 컷오프 환산(0.85–2.65 → 2.40–4.20 V)이 **전부 이 가정 위**에 있다 |
| **G5** | **기준극 안정성 주장의 근거가 K–K 잔차다.** `[인쇄]` "The **Kramers-Kronig residuals within ±0.4** (Figs. S1 and S2) **suggest the stability of the reference electrodes** during the durability tests" | ★ **범주 오류**다 — K–K 는 측정 스펙트럼의 선형·인과·정상성을 보는 검사이고 **기준극의 DC 전위**를 보지 않는다. 그리고 ±0.4 라는 문턱 자체가 느슨하다(아래 D7) |
| **G6** | **접촉 면적의 절대값이 없다.** Image-J 로 잰 것은 **비(比) 2.0** 하나뿐이고 단위·면적·분율이 없다. **노화 전후 접촉 면적은 재지 않았다** — 도구(Image-J)와 시편(Figs. 6·7)이 둘 다 지면에 있는데도 | `θ(N)` 이 또 0 이다. 이번에는 **장비가 방 안에 있었다** |
| **G7** | **CPE 용량(`CPE2-C`)에만 ± 가 없다.** Table S1 에서 `R3` 와 `CPE2-p` 는 ± 를 달고, `CPE2-C` 와 `τ3` 는 안 단다 | **우리 곱 축퇴 검사가 필요로 하는 바로 그 파라미터**의 불확실성이 비어 있다 |
| **G8** | **노화 후 적합 파라미터의 표가 없다.** Fig. 5 는 **막대그래프(로그축)**이고 숫자 표가 없다. `p`(CPE 지수)의 노화 전후 값은 **어디에도 없다** | 우리가 Fig. 5 에서 읽은 값은 전부 `[도표]` 이고, `τ = (R·Q)^{1/p}` 의 `p` 를 모른다 |
| **G9** | **`Wo`(Warburg) 의 값이 한 번도 인쇄되지 않는다.** 회로도(Fig. 2b)에 `Wo1` 이 있고 본문이 `[인쇄]` "diffusion-related resistance" 가 늘었다고 말하는데 **값·파라미터 0** | 저주파가 이 편에서 가장 크게 움직이는 구간이고(Fig. 4c: −Z″ 660 Ω), 그 구간의 정량이 없다 |
| **G10** | **DRT 의 λ 선택 규칙이 없다.** 값은 둘 다 인쇄됐다(LPSI **6.0×10⁻²**, LPSCl **8.5×10⁻⁴**, **70 배 차이**). 근거는 `[인쇄]` "by applying **adequate** regularization parameters" · "the independent components of R2 to R4 are **confirmed** by using λ = …" | ★★ **λ 가 봉우리 개수를 확인하는 데 쓰였다 — 즉 개수가 λ 의 출력이 아니라 λ 선택의 목표다**. λ 민감도·L-curve·GCV **0** |
| **G11** | **Young 계수 22.1 / 30 에 단위가 없다** (`[인쇄]` "The Young's modulus of LPSCl (22.1) lower than that of LPSI (30) [42]"). 그리고 ref [42] 는 **제일원리 계산**(Deng 2016) 인데 LPSI 는 **glass-ceramic** 이다 | 이 값이 LPSCl 의 R1′ 반원(= void) 서사 전체를 떠받친다 |
| **G12** | **SoC 정의가 충전 용량 기준이다** (`[인쇄]` "defined with the **charge** capacity at 0.10C"). 초회 효율이 `[도표]` **80 %(LPSI)** 인데 SoC=100 % 가 무엇인지 — 충전 종료 상태인지 — 만 말한다 | SoC 축이 두 계에서 같은 뜻이 아닐 수 있다(효율이 다르다) |
| **G13** | **대칭셀의 질량 점이 2 개뿐이다** (50.0 / 93.5 mg). 그 두 점으로 그은 직선의 **외삽 절편**을 `[인쇄]` **8.011 Ω** 로 4 유효숫자로 인쇄하고, 본문은 같은 값을 **7.9 Ω** 라 부른다 | `R2` 귀속의 유일한 독립 근거다. 그리고 대칭셀은 **150 MPa**, 3전극 셀은 **110 MPa** 로 눌렸다 |
| **G14** | **Fig. 5 가 어느 온도·어느 SoC 인지 캡션에 없다** (본문 맥락상 298 K·SoC 100 %) | 절대값을 다른 그림과 비교할 때 걸린다 (아래 D9) |
| **G15** | **데이터 비공개** — `[인쇄]` "Data will be made available **on request**" | 원시 스펙트럼 재적합 불가. 16호와 같다 |
| **G16** | **`LAM`·`LLI`·`SOH` 어휘가 0 이고**, 대신 `[인쇄]` "the amount of **effective active material** decreased only in the LPSI system" 라는 문장이 한 번 나온다. 정량은 없다 | 이 계보에서 **양극 활물질 손실을 문장으로 말한 몇 안 되는 실측 편**인데 값이 없다 |

# 서지

**Goro Fukunishi, Mayu Tabuchi, Atsunori Ikezawa, Takeyoshi Okajima, Fusao Kitamura,
Kota Suzuki, Masaaki Hirayama, Ryoji Kanno, Hajime Arai\*** — "AC impedance analysis of
NCM523 composite electrodes in all-solid-state three electrode cells and their degradation
behavior", ***Journal of Power Sources* 564 (2023) 232864**,
doi `10.1016/j.jpowsour.2023.232864`.

- 소속: **Tokyo Institute of Technology** — School of Materials and Chemical Technology +
  **All-Solid-State Battery Center, Institute of Innovative Research**.
  교신 **Hajime Arai** (`arai.h.af@m.titech.ac.jp`).
- 접수 **2022-11-07** → 개정 **2023-01-30** → 승인 **2023-02-20** → 온라인 **2023-03-03**.
- `[인쇄]` © 2023 **Elsevier B.V. All rights reserved** (오픈액세스 아님).
- 자금: **NEDO SOLiD-EV 프로젝트** (Grant P18003). NCM523 분말은 **Sumitomo Metal Mining** 제공.
  이해충돌 없음.
- 분량: **본문 10 쪽** (본문 pp. 1–9 + 참고문헌 **44 편** pp. 9–10) + **SI 6 쪽**
  (Fig. S1–S4 + Table S1).
- 키워드 `[인쇄]`: All-solid-state lithium-ion batteries | Three-electrode cells |
  LiNi₀.₅Co₀.₂Mn₀.₃O₂ | Reference electrodes | Electrochemical impedance spectroscopy.
- PDF: 본문 sha256 `c0798ee510063429…`, SI `773e6fbca1d7b938…` (frontmatter 에 전문).

## 이 논문의 자기 계보 — 그리고 우리 위키와의 접점

| ref | 문헌 | 역할 |
|---|---|---|
| **[27]** | **Ikezawa, Fukunishi, Okajima, Kitamura, Suzuki, Hirayama, Kanno, Arai**, *Electrochem. Commun.* **116** (2020) 106743 — "Performance of Li₄Ti₅O₁₂-based reference electrode …" | **이 편의 방법 원본.** R-LTO 메시 기준극·3전극 셀 제작·LiCoO₂ 비교가 전부 여기서 온다. **저자 8 명 중 8 명이 겹친다.** 17호 digest 의 후속 후보 **4 순위**이자 **큐에 없는 편** |
| **[23]** | **Koerver, Aygün, …, Zeier, Janek**, *Chem. Mater.* **29** (2017) 5574 — 공간전하층·계면 | ⚠ **큐 22 번과 같은 논문**이다 (Capacity Fade in Solid-State Batteries). 이 편은 그것을 **공간전하층 한 줄**로만 인용한다 |
| **[19]** | **Ruess, …, Janek**, *JES* **167** (2022) 100532 — NCM 입자 균열이 액체/고체 동역학에 주는 영향 | 입자 균열 → 저항 계보의 원전 |
| **[30]** | **Schönleber, Klotz, Ivers-Tiffée**, *Electrochim. Acta* **131** (2014) 20 — **Lin-KK** | ★ **이 계보에서 K–K 도구를 실제로 돌린 첫 편**의 근거 |
| **[28][29]** | **Schichlein 2002** · **Illig 2012** (LiFePO₄ 에서 **전하이동과 접촉 저항의 분리**) | DRT 의 방법 원전. ⚠ [29] 의 제목이 곧 **우리 물음**("Separation of charge transfer and **contact resistance**")인데, 이 편은 그것을 **DRT 참고문헌으로만** 쓴다 |
| **[35]** | **Zuo, Rueß, …, Kanno, Janek**, *Nat. Commun.* **12** (2021) 6669 | 용량 140–150 mAh g⁻¹ 이 "2전극 문헌과 비슷하다" 의 비교 대상 |
| **[34]** | **Santhosha, Medenbach, Buchheim, Adelhelm**, *Batteries & Supercaps* **2** (2019) 524 | ★★ **17호 digest 의 후속 후보 1 순위(0.62 V 가 태어난 자리)가 여기서도 Li-In 전위의 근거로 인용된다.** ⚠ 이 편의 서지는 **"2 (2019) 524–529"** 로 정상이다 — 17호가 `[인쇄]` "414, 359 (2019)" 로 적은 것이 **오기임이 확인된다** |

`[해석]` **이 편은 16호의 "유일한 외부 실측 대조군" 이지만, 독립 그룹의 재현이 아니라
자기 그룹(Tokyo Tech / Arai–Kanno) 방법의 열화 확장판**이다 — 16호(Marburg/Roling)가
자기 그룹 방법의 3전극 확장판이었던 것과 같은 구조다.

# 어휘 집계 (NFKC 정규화 · 대소문자 구분 · 본문 pp.1–9 / SI 전문 · 참고문헌 제외)

| 낱말 | 본문 | SI | 메모 |
|---|---:|---:|---|
| `durability` | **16** | 0 | 이 편의 열화 어휘 |
| `three-electrode` | **12** | 1 | |
| `reference electrode` | **10** | 0 | |
| `Li-In` / `Li–In` | 13 | 13 | |
| `contact` | **9** | 0 | 아래 전수 |
| `contacting area` | **4** | 0 | ★ 전부 한 문단 (입자 크기 논증) |
| `contact area` | 2 | 0 | 서론 1 + Methods 1 |
| `void` | **7** | 0 | ★ 이 계보 실측 편 중 최다 |
| `degrad*` | 8 | 1 | |
| `capacity` | 8 | 0 | |
| `fit*` | 9 | 1 | |
| `DRT` | 8 | 8 | |
| `equivalent circuit` | 6 | 0 | |
| `crack` | 4 | 0 | |
| `Kramers` / `Kronig` | **2 / 2** | **2 / 2** | ★★ **계보 최초의 K–K 검증** |
| `λ` | **3** | 2 | ★ 두 값이 **70 배 다르다** |
| `regulariz*` | 1 | 0 | |
| `residual*` | 2 | 32 | |
| `cycle life` | 2 | 0 | |
| `space charge` | 1 | 0 | |
| `dead` | **1** | 0 | ★ `[인쇄]` "such **dead particles**" — 아래 §3.3 |
| `isolat*` | 2 | 0 | 하나는 "R4 has not been **isolated**", 하나는 1차 입자의 "**isolation**" |
| `half-cell` | 1 | 0 | |
| `MPa` | **2** | 0 | 110(셀) · 150(대칭셀) |
| `pressure` · `stack pressure` · `hysteres*` | **0** | **0** | ★★ **압력이라는 낱말이 없다** |
| `porosity` · `tortuos*` · `percolat*` · `contact loss` · `θ` | **0** | **0** | |
| `identifiab*` · `uniqu*` · `ill-posed` · `uncertaint*` · `confidence` · `error bar` · `standard deviation` · `condition number` · `Fisher` · `bootstrap` · `Bayes*` · `degenerac*` · `overfit*` · `cross-valid*` · `sensitiv*` · `initial guess` · `multi-start` · `n =` | **0** | **0** | **Q4 = 0 (18/18 편)** |
| `LAM` · `LLI` · `SOH` · `aging` / `ageing` | **0** | **0** | (⚠ `state of health` 는 **1 회** — Methods) |
| `OCV` · `open circuit` · `GITT` | **0** | **0** | 곡선은 전부 0.1 C pseudo-OCV |
| `dendrit*` · `dead li` (음극 의미) | **0** | **0** | Li-In 음극 |
| 오검출 확인 | — | — | `flam*` 0 · `Soh` 0 · `[Ll]am[a-z]` 0 ⇒ `LAM`→flammable, `SOH`→Sohn 오검출 **없음** |

## `contact` 9 회 전수 — 이 편에서 "접촉" 이 놓이는 자리

1. 서론 — "the **contact area** between the solid electrolyte and solid electrode materials
   **is limited** in ASS-LIBs, and thus a large amount of solid electrolyte is used"
2. 서론 — "The **cycle life** is also affected by the **insufficient contact** between the
   solid electrolyte and solid electrode materials" ← ★ **접촉 손실 ↔ 수명을 서론에서 연결한다**
3. Methods §2.4 — "Image processing software **Image-J** was used to estimate the
   **contact area** between the solid electrolyte and active material particles [31]"
4–7. §3.2 입자 크기 논증 — "If these particles are **completely immersed** in the electrolyte,
   the **contacting area** should also be inversely proportional to the radius r … the
   **contacting area ratio** S(5.0)/S(11.2) is calculated to be **2.4** … Image-J shows that
   the ratio of **contacting area** is **2.0** … the reciprocal of the estimated
   **contacting area** ratio, **0.42 or 0.50**"
8. §3.2 결론 — "The result also suggests the **uniform physical contact** between the active
   electrode and solid electrolyte particles"
9. **§3.3 — "These results suggest that the chemical composition at the interface **or the
   contact area** between the NCM523 and electrolyte particles changed"** ← ★★★★ **이 digest 의 축**

★★★ `[해석]` **8 과 9 를 나란히 놓으면 이 편의 성질이 보인다.** 신품에서는 **비(比)가
맞으니 접촉이 균일하다**고 단정하고(8), 노화에서는 **화학 아니면 면적이라고 인쇄한 뒤
가르지 않는다**(9). 두 문장 사이에 있는 것은 **같은 관측량(`R3`) 하나**다.

# §Abstract (전수 요지)

`[인쇄]`:
- LPSI(glass-ceramic Li₂S-P₂S₅-LiI) 또는 LPSCl(결정질 Li₆PS₅Cl) 전해질의 **전고체 3전극 셀**에서
  NCM523 복합양극의 AC 임피던스를 분석해 **율 제한 과정**과 **충방전 사이클 뒤의 변화**를 본다.
- 성분 다섯: **(i)** 전해질층의 Li⁺ 이동 저항 · **(ii)** 복합양극–집전체 간 전자이동 저항 ·
  **(iii)** NCM523–고체전해질 간 전하이동 저항 · **(iv)** **정체가 밝혀지지 않은 성분** ·
  **(v)** NCM523 입자 내 Li⁺ 확산(Warburg).
- (iii)의 활성화에너지는 **액체계보다 낮다**.
- 사이클 시험 뒤 **두 계 모두 (iii)이 크게 증가**. 다만 **LPSI 계가 (iv)의 증가와
  2차 입자 내 미세 void 가 더 크다** ⇒ (iv)는 **NCM523 1차 입자 사이의 전하이동 저항**으로 귀속.

# §1 Introduction

- LIB → NCM523 이 양극 주류. EIS 가 율 제한 과정을 정량한다 [7–14].
- 액체계에서 **지배 저항은 전해질|활물질 계면의 전하이동**이고 [10], 거기에는
  **용매화/탈용매화**가 들어간다 [11]. 그 밖에 **집전체|NCM 전자 저항** [12],
  **NCM 입자 내 Li 확산** [13,14]. **사이클 중 전하이동 저항이 증가**한다 [14,15].
  원인 후보 `[인쇄]`: **표면층 형성** [11] · **전이금속 용출** [16,17] · **입자 균열** [18,19].
- ASS-LIB 에서 다른 점 `[인쇄]`: **용매화/탈용매화가 없다**, **전이금속 crosstalk 이 억제된다**,
  대신 **공간전하층** [23] 이 커질 수 있어 **LiNbO₃ 코팅** [24–26] 을 쓴다.
- ★ `[인쇄]` "the **contact area** between the solid electrolyte and solid electrode materials
  **is limited** … **The cycle life is also affected by the insufficient contact**".
- `[인쇄]` 3전극 셀이 **critical** 하다 — "the influence of the **Li-In counter electrode** on the
  impedance is **significant**, showing the necessity to use three-electrode cells" [27].
- 이 연구: 3전극 셀 제작 → NCM523 임피던스 성분 정량 → 활성화에너지 → **충방전 사이클 시험
  전후 비교** → **두 전해질(LPSI/LPSCl)의 열화 차이**.

`[해석]` **서론이 "접촉 부족 → 수명" 을 명제로 적고, 본론에서 그 접촉을 노화 축으로는
한 번도 재지 않는다** (G6).

# §2 Experimental (전수)

## 2.1 재료

- **활물질**: **LiNbO₃ 코팅 NCM523**, `[인쇄]` "basically **D50 = 5.0** and **occasionally 11.2 μm**"
  (Sumitomo Metal Mining).
- **고체전해질 2 종**:
  - **LPSI** glass-ceramic Li₂S-P₂S₅-LiI — **D50 = 5.0 µm**, **σ_ion = 2.6 mS cm⁻¹** (Idemitsu Kosan)
  - **LPSCl** argyrodite Li₆PS₅Cl — **D50 = 0.66 µm**, **σ_ion = 1.8 mS cm⁻¹** (Mitsui Metal & Mining)
- **복합양극 조성** `[인쇄]`:
  - LPSI 계: **NCM523 : LPSI : VGCF = 49 : 43 : 8.0 wt%**
  - LPSCl 계: **NCM523 : LPSCl : VGCF = 69 : 26 : 5.0 wt%**
  - 근거는 `[인쇄]` "optimized mixing ratios … determined with the **preliminary tests**" (G3).
  - 혼합은 milling pot (ANZ-10S0, Nitto Kagaku). **분리막층의 SE 는 복합양극의 SE 와 같은 종류.**
- **기준극**: `[인쇄]` "**partially reduced** lithium titanate Li₄Ti₅O₁₂ (**R-LTO**)" **검은 분말**,
  합성법은 [27]. 슬러리를 **니켈 메시**(3Ni7-3/0, Taiyo Wire Cloth, **개구율 90–91 %**,
  **두께 0.08 mm**, **φ 9.0 mm**)에 도포한 **메시형**.
  ★ `[인쇄]` "universal design **without solid electrolytes** so that it can be applied to
  **both LPSI and LPSCl systems** without modification".
- **상대극**: **Li-In** — **인듐박 φ10.0 mm × 0.05 mm** (Niraco) + **리튬박 φ5.0 mm × 0.1 mm**
  (Honjo Metal) 를 압착.

★★ `[재현]` **상대극의 조성을 우리가 계산했다** (지면에 없다):
In 부피 π·(0.5 cm)²·0.005 cm = 3.93×10⁻³ cm³ × 7.31 g cm⁻³ = **28.7 mg = 0.250 mmol**;
Li 부피 π·(0.25 cm)²·0.01 cm = 1.96×10⁻³ cm³ × 0.534 = **1.05 mg = 0.151 mmol**
⇒ **Li 몰분율 = 0.151/(0.151+0.250) = 37.7 at%** — **In + LiIn 2 상 공존역 한복판**이다.

## 2.2 셀 조립

`[인쇄]` 순서:
1. **R-LTO 메시 기준극을 두 장의 고체전해질층 사이에 끼운다 — 위쪽 1.3 mm, 아래쪽 1.0 mm**.
   PET 관(**φ 10.0 mm**)에 넣는다.
2. **Li-In 상대극(위)** 과 **NCM523 복합양극(아래, 6.0 mg, ca. 7.6 mg cm⁻²)** 을 각각 얹는다.
3. **전체를 110 MPa 로 압착**.
4. 셀 전체를 **Ar 채운 폴리스티렌 용기**에 넣고 단자로 측정. 전 과정 Ar 글러브박스
   (이슬점 < **−80 °C**, O₂ < **5 ppm**).
- **대칭셀**: NCM523 복합체를 **알루미늄 집전체 두 장 사이**에 끼우고 **150 MPa** 로
  중공 원통 용기에서 압착.

`[재현]` 셀 면적 = 6.0 mg ÷ 7.6 mg cm⁻² = **0.79 cm²** = π·(0.5 cm)² ✔ (φ10 mm 와 정합).
`[재현]` **활물질 면적 로딩**: LPSI 계 **3.72 mg cm⁻²**(0.54 mAh cm⁻² @145 mAh g⁻¹),
LPSCl 계 **5.24 mg cm⁻²**(0.76 mAh cm⁻²).
★ `[해석]` **이 계보에서 가장 얇은 전극에 속한다** — 17호가 **19.1 mg cm⁻² · 2.80 mAh cm⁻²**,
16호가 26–219 µm 였다. **율·확산 제한이 거의 없는 조건**이고, 그것이 이 편의 결론
(계면 저항이 지배)을 유리하게 만든다.

## 2.3 전기화학 시험

- **VSP-300 (BioLogic)**, 항온조 SH-222 (Espec).
- **C-rate 는 공칭 160 mAh g⁻¹ 기준.**
- ★★★ **컷오프는 작업전극 전위에 건다**: `[인쇄]` "The **cutoff potential of the working
  electrode** was set at **0.85–2.65 V (2.40–4.20 V vs. Li/Li⁺)**".
  `[재현]` 0.85 + 1.55 = 2.40 ✔ / 2.65 + 1.55 = 4.20 ✔ — **환산이 G4 의 가정 위에 있다.**
- 초기 **0.10 C 3 사이클** → 그 뒤 EIS.
- EIS: **10 mV**, **7.0 MHz – 5.0 mHz**.
- **SoC 는 0.10 C 충전 용량으로 정의.**
- 적합: **Z-View (Scribner)**. **DRT** [28,29] 를 `[인쇄]` "occasionally" 수행.
  `[인쇄]` 고주파 **유도 성분은 DRT 전에 곡선적합으로 뺀다**.
  `[인쇄]` **Lin-KK tools (KIT [30])** 로 K–K 만족을 확인, **residuals < 0.40** (Fig. S1·S2).
  DRT 소프트웨어는 **Z-assist (TOYO)**.
- ★ **적합 절차** `[인쇄]`: "First, the **time constants obtained from the DRT analysis were
  fixed** and the other parameters were refined. Then, **all the valuable parameters** in the
  equivalent circuit were refined."
  `[해석]` **DRT → 시상수 고정 → 등가회로 적합** 은 **DRT 의 봉우리 개수·위치가 회로의 차수를
  정한다**는 뜻이다. 그리고 그 개수는 λ 로 조정됐다(G10) ⇒
  **λ → 봉우리 개수 → 회로 차수 → `R3`/`R4` 의 값** 이라는 사슬이 지면에 그대로 있다.
  [[drt-peak-count-nonidentifiability]] 가 예측한 하류 전파의 **가장 명시적인 사례**다.
- **내구(durability) 시험**: **1.0 C, 50 사이클, 333 K**.
  `[인쇄]` 추가로 "the **state of health** of the cell was evaluated by **0.10C** charging and
  discharging at **298 K** before and after the durability test" ⇒ **RPT 설계가 있다.**

`[재현]` **전류밀도**: 0.1 C = **0.054 mA cm⁻²**(LPSI 계), 1.0 C = **0.54 mA cm⁻²**.
17호의 1 C(**2.80 mA cm⁻²**)의 **1/5**, 17호 CA 초기(≈16 mA cm⁻²)의 **1/300** 이다 (§Q5 대질).

## 2.4 SEM-EDX

`[인쇄]` **완전충전 상태의 전극 펠릿**을 3전극 셀에서 분해 → 가변각 슬라이서
(SliceMaster HW-1S, JASCO) → **이온 밀링**(IM-4000, Hitachi High-Tech) →
**FE-SEM (Regulus 8230)** + **EDX (FlatQUAD, Bruker)** 동시 관찰.
`[인쇄]` "**Image-J** was used to estimate the **contact area** between the solid electrolyte
and active material particles [31]".

# §3.1 3전극으로 단극 성분 분리

- Fig. 1: NCM523 과 Li-In 의 충방전 곡선(LPSI (a)(b) · LPSCl (c)(d)).
- ★ `[인쇄]` "**Assuming** that the potential of the R-LTO reference electrode is **1.55 V** vs.
  Li/Li⁺ [32,33], the **plateau potentials of the NCM523 and Li-In electrodes are ca. 3.7 and
  0.6 V vs. Li/Li⁺**, which agree with those in the liquid electrolyte systems [5,6,34].
  This result **confirms that the R-LTO reference electrode works as a Li₇Ti₅O₁₂/Li₄Ti₅O₁₂
  redox couple**."
  ⚠ `[해석]` **순환이다** — 1.55 V 를 가정해서 얻은 두 평탄값이 문헌과 맞는다는 것으로
  1.55 V 가 맞다고 결론한다. 독립 측정(예: Li 금속 대비)은 없다.
- `[인쇄]` 충방전 용량 **140–150 mAh g⁻¹** 이 2전극 문헌 [35] 과 비슷 ⇒
  "**no negative effect of the reference electrode** on the intrinsic charge-discharge
  characteristics".
- Fig. S3: `[인쇄]` **"The combined impedances of NCM523 and Li-In … agree well with the cell
  impedances measured in the two electrode configurations … in the frequency ranges
  below 1 MHz"** ⇒ 3전극 분해의 **자기 검증**.
- ★★ `[인쇄]` "the **cell impedance** (in the two-cell configuration) is **significantly
  different from the impedance of NCM523**, indicating that the three-electrode
  configuration … **is crucial**".

# §3.2 NCM523 전극 과정의 동정 (LPSI)

## 다섯 성분 (Fig. 2a, 298 K, SoC 0/25/50/75/100 %)

| 성분 | 주파수 | SoC 의존 | 귀속 |
|---|---|---|---|
| **R1** (절편) | ~1 MHz | **없음** | 기준극–작업전극 사이 **고체전해질층의 Li⁺ 이동** |
| **R2** (작은 반원) | ~1 MHz | **없음** | **Al 집전체\|NCM523 전자 이동** |
| **R3** (큰 반원) | ~1 kHz | **있음** | **NCM523\|고체전해질 전하이동** |
| **R4** (반원) | ~1 Hz | 상대적으로 작음 | **NCM523 2차 입자 내 1차 입자 사이의 전하이동** |
| **Wo** (직선) | < 1 Hz | 있음 | NCM523 입자 내 Li 확산 |

`[인쇄]` R4 의 SoC 의존이 작은 것은 "(iii), (iv), (v) 의 **중첩** 때문일 수 있다".
`[인쇄]` 스펙트럼 모양이 **LiCoO₂ 와 비슷하되 LiCoO₂ 에는 R4 가 없다** [27].

**활성화에너지** (283/293/303 K 3 점, Fig. 2d):
`[인쇄]` **R1 24 ± 1 · R2 70 ± 20 · R3 49 ± 6 · R4 42 ± 1 kJ mol⁻¹**.
★ `[해석]` **이 계보에서 적합 파라미터에 ± 를 붙인 첫 편이다** (16·17·9호 전부 0). 다만
그 ± 는 **3 점 회귀의 표준오차**이고 **셀 간 반복이 아니다**(G1).

## 각 귀속의 근거 (전수)

**R1** — `[인쇄]` Ea 24 kJ mol⁻¹ 이 LPSI 이온저항 [36] 과 대략 일치.
`[인쇄]` **절대값 55 Ω** 이 **기하 추정 49 Ω** 과 가깝다 (σ 2.6 mS cm⁻¹, 면적 0.79 cm²,
기준극–작업전극 간 두께 1.0 mm).
`[재현]` L/(σA) = 0.1 cm / (2.6×10⁻³ S cm⁻¹ × 0.79 cm²) = **48.7 Ω** ✔ **재현된다.**
`[재현]` 그리고 **상대극 쪽은 1.3 mm 이므로 ≈63 Ω** — 지면에 없다.

**R2** — 대칭셀(Al\|복합체\|Al, Fig. S4)로 검증. `[인쇄]` 복합체 내부 전자저항 `R_bulk` 는
질량에 비례하고 계면 저항 `R_interface` 는 일정하다 → 질량 대 DC 저항 직선의
**절편이 `R_interface` = 7.9 Ω**, `[인쇄]` "one side of R_interface is **ca. 4 Ω** and this is
**the same order as R2**". Ea 비교: 액체계 문헌의 같은 성분은 **ca. 4 kJ mol⁻¹** [37,38] 인데
여기서는 **ca. 70** ⇒ `[인쇄]` **LiNbO₃ 코팅** 때문으로 추정.

**R3** — `[인쇄]` SoC 의존이 액체계 보고 [15] 와 매우 유사. Ea **49** < 액체계 **59–71** [39]
⇒ `[인쇄]` 용매화/탈용매화가 없어서.
★★★ **그리고 입자 크기 실험** (이 편의 Q1 에 해당하는 유일한 정량):
- `[인쇄]` D50 = 5.0 / 11.2 µm 두 시료. Table S1: `R3(5.0)/R3(11.2) ≈ 0.5`,
  그리고 `[인쇄]` "the **time constants are nearly unchanged**" (⚠ D3).
- 식 (1)–(4) `[인쇄]`: 구 가정, `V_i = 4πr³/3`, `V_w = M/d`, `N = 3M/(4πdr³)`,
  **`S_w = 4πr²N = 3M/(dr)`** ⇒ **총 표면적은 반경에 반비례**.
- `[인쇄]` "**If these particles are completely immersed in the electrolyte**, the contacting
  area should **also** be inversely proportional to r" ⇒ **접촉 분율을 입경에 무관한 상수로
  가정**한다(= `θ` 를 소거한다).
- `[인쇄]` 계산값 **S(5.0)/S(11.2) = 2.4**, **Image-J 실측 2.0**, 역수 **0.42 또는 0.50**
  ≈ 실측 `R3` 비 **0.5** ⇒ `[인쇄]` "we conclude that R3 is the resistance associated with
  charge transfer at the interface of NCM523\|solid electrolyte. **The result also suggests
  the uniform physical contact** between the active electrode and solid electrolyte particles."
- ⚠ `[재현]` **반경비는 11.2/5.0 = 2.24 이지 2.4 가 아니다.** 2.4 가 어떻게 나왔는지 안 적혀
  있다 (D4).

**R4** — `[인쇄]` 선행 연구에서 **분리된 적이 없는 성분**이고, `[인쇄]` "The existence of R4 is
apparent **when the three-electrode cell is applied to separate the Li-In component, which
significantly affects the low-frequency behavior**." ⇒ ★★ **3전극이 없으면 R4 는 음극에
가려진다.** `[인쇄]` D50 = 11.2 µm 의 R4 가 5.0 µm 의 **2–3 배**. Fig. 3(d)(e) ×50,000 에서
2차 입자 내부에 **입계와 void** 가 보이고 **11.2 µm 쪽이 더 뚜렷** ⇒ **2차 입자 내부의
전하이동**으로 귀속.

## LPSCl 계의 차이

`[인쇄]`:
- **R1 에 반원이 붙는다**(`R1′//CPE`, ~1 MHz). **같은 반원이 Li-In 쪽에도 보인다**
  ⇒ **LPSCl 자체의 성질**.
- `Ea(R1 + R1′) = 40 kJ mol⁻¹` 이 LPSCl 이온전도 문헌 [41] 과 일치.
- 이유 `[인쇄]`: "The **Young's modulus of LPSCl (22.1) lower than that of LPSI (30)** [42]
  implies that the **adhesions between LPSCl particles are less sufficient** …
  leading to **void formation** to generate **capacitive components** in the impedance."
  ⚠ 단위 없음, 계산값(제일원리) vs glass-ceramic 실물 (G11).
- **R2 는 LPSCl 계에서 거의 검출 불가** — 1 MHz 반원과 1 kHz 반원 사이에 끼여서.
- **R3 과 R4 의 경계가 불명확** ⇒ **DRT** 로 분리, `[인쇄]` "the independent components of
  R2 to R4 are **confirmed by using λ = 8.5 × 10⁻⁴**".
- 두 계의 Ea 가 `Ea(R1)` 빼고 일치. **`Ea(R3) ≈ 50` 둘 다** ⇒ 용매화 없는 성질.

# §3.3 반복 충방전에 의한 열화 (이 편의 본체)

## 용량 축 (Fig. 4a·4b — 0.1 C RPT, 298 K)

`[인쇄]`:
- **두 계 모두 방전 전위 강하**가 관측됐다.
- **LPSCl 은 용량이 거의 유지**, **LPSI 는 크게 감소**.
- ★★★★ `[인쇄]` "These results suggest that the **overpotential increased in both systems**,
  possibly due to **reaction inhomogeneity caused by the resistance increase**, whereas the
  **amount of effective active material decreased only in the LPSI system**."

`[도표]` 우리 판독 (Fig. 4a·4b, ±5 mAh g⁻¹):

| 계 | 전 방전 | 후 방전 | 변화 |
|---|---:|---:|---|
| **LPSI** | ≈143 | ≈103 | **−28 %** |
| **LPSCl** | ≈148 | ≈147 | **≈−1 %** |

★★ `[해석]` **이것이 이 계보에서 드문 조합이다** — **같은 셀 안에서 전극 분해된 용량 축과
전극 분해된 임피던스 축이 동시에 있고**, 컷오프가 **작업전극 전위**에 걸려 있어
**상대극이 겉보기 용량을 밀 수 없다**. 17호가 연 오염 경로가 **설계상 닫혀 있다**(§Q5 대질).

## 임피던스 축 (Fig. 4c·4d, Fig. 5)

`[인쇄]`:
- K–K 잔차 ±0.4 ⇒ (저자들 주장) 기준극 안정 (G5).
- 노화 뒤 **R3–R4 경계가 다시 불명확**해져 DRT 로 분리:
  **LPSI λ = 6.0 × 10⁻²**, **LPSCl λ = 8.5 × 10⁻⁴**.
- **LPSI**: R1·R2 **변화 미미**, **R3 6 배**, **R4 9 배**.
  `[인쇄]` "These results suggest that the **chemical composition at the interface or the
  contact area** between the NCM523 and electrolyte particles **changed**."
- **LPSCl**: **R3 증가는 LPSI 와 같다**, **R4 증가는 훨씬 억제**.

`[도표]` 우리가 Fig. 5 의 로그 막대에서 읽은 값 (판독 오차 ±0.04 in log ⇒ ±10 %):

| 계 | 항 | 신품 R / Ω | 노화 R / Ω | 배율 | 신품 τ / s | 노화 τ / s | 배율 |
|---|---|---:|---:|---:|---:|---:|---:|
| **LPSI** | R1 | ≈76 | ≈105 | **×1.4** | — | — | — |
| | R2 | ≈7.9 | ≈12.6 | **×1.6** | 8.3×10⁻⁷ | 1.5×10⁻⁷ | ×0.18 |
| | **R3** | **≈79** | **≈513** | **×6.5** | 2.0×10⁻⁴ | 4.8×10⁻⁴ | **×2.4** |
| | **R4** | **≈21** | **≈195** | **×9.3** | 1.0×10⁻² | 5.3×10⁻² | **×5.3** |
| **LPSCl** | R1′+R2′ | ≈63 | ≈89 | ×1.4 | 2.1×10⁻⁷ | 1.3×10⁻⁷ | ×0.6 |
| | R2 | ≈1.4 | ≈9.6 | **×6.9** | 2.0×10⁻⁶ | 1.1×10⁻⁶ | ×0.5 |
| | **R3** | **≈18** | **≈135** | **×7.4** | 5.6×10⁻⁵ | 4.5×10⁻⁴ | **×7.9** |
| | **R4** | **≈2.8** | **≈9.5** | **×3.4** | 2.8×10⁻³ | 6.0×10⁻² | **×21** |

⚠ **본문이 말하지 않는 것 둘**: ① **LPSCl 의 R2 가 6.9 배 자란다** — `R2` 는
**Al 집전체\|복합양극 전자 접촉**이다. 본문은 LPSI 의 R2 만 "미미" 하다고 적고 **LPSCl 의
R2 는 언급하지 않는다**(D6). ② **LPSI 의 R1·R2 도 40–60 % 자란다** — "insignificant" 는
6–9 배에 비해 작다는 뜻이지 0 이 아니다.

## 활성화에너지 축 (Table 1 — 전수)

| 항 | LPSI 전 | LPSI 후 | LPSCl 전 | LPSCl 후 |
|---|---:|---:|---:|---:|
| `Ea(R1 또는 R1+R1′)` | **24 ± 1** | 26 ± 4 | **40 ± 2** | 36 ± 5 |
| `Ea(R2)` | **70 ± 20** | **41 ± 8** | **60 ± 10** | **43 ± 6** |
| `Ea(R3)` | **49 ± 6** | 54 ± 1 | **50 ± 2** | **63 ± 5** |
| `Ea(R4)` | **42 ± 1** | **64 ± 4** | **50 ± 3** | **56 ± 1** |

(단위 kJ mol⁻¹)

`[인쇄]` 본문의 요약: "Ea(R1) and Ea(R2) **remained almost unchanged**, while **Ea(R3)
increased** after the cycle test … **Ea(R4) increased in the LPSI system more than** in LPSCl."

⚠⚠ `[재현]` **자기 표와 두 군데 어긋난다** (D5):
- `Ea(R2)` LPSI **70 ± 20 → 41 ± 8**: 구간 [50, 90] 과 [33, 49] 가 **겹치지 않는다**.
  "almost unchanged" 가 아니다.
- `Ea(R3)` LPSI **49 ± 6 → 54 ± 1**: 구간 [43, 55] 와 [53, 55] 가 **거의 포개진다**.
  "increased" 는 **LPSCl(50±2 → 63±5)에서만 구간이 갈린다**.
★ `[해석]` **이 편은 ± 를 인쇄한 첫 편인데, 자기 ± 를 결론에 쓰지 않는다.**

## 형태·조성 축 (Fig. 6 LPSI · Fig. 7 LPSCl)

`[인쇄]`:
- **두 계 모두 활물질 → 고체전해질로 O 원자 이동**이 관측됨 [43,44].
- **LPSI 에서만** 2차 입자 둘레에 **O 와 P 를 포함하는 두께 2 µm 의 퇴적층**.
  LPSCl 에서는 `[인쇄]` "such layers were **not apparent**".
- ★★★ 두 갈래의 추론이 나란히 인쇄된다:
  > `[인쇄]` "**If** these layers are chemically formed **resistive compounds**, the increase in
  > R3 **would be more significant in the LPSI system than in the LPSCl system**.
  > **On the other hand, if insulative layers completely cover the active material to make the
  > particle inactive, such dead particles probably have no contribution to the charge transfer
  > process. This could explain the large capacity decrease in the LPSI system.**"
  ⚠⚠ `[재현]` **첫 번째 조건문의 귀결이 자기 데이터에서 성립하지 않는다** — 같은 절이
  `[인쇄]` "The increase in R3 in the LPSCl system **was the same as** that in the LPSI system"
  이라고 적는다 (우리 판독으로는 LPSCl 쪽이 오히려 크다: ×7.4 vs ×6.5). ⇒ **저자 자신의
  논리대로라면 퇴적층은 "저항성 화합물" 이 아니다.** 논문은 이 귀결을 적지 않는다 (D8).
  ⇒ 남는 것은 **두 번째 가지 = `θ_AM`(덮여서 죽은 입자)** 인데, **그 분율을 재지 않는다.**
- **LPSI 에서 2차 입자 내부에 미세 void 가 더 많다** — `[인쇄]` "probably caused by
  **particle cracking** during the repeated cycling" ⇒ R4 증가와 연결.
- `[인쇄]` 1차 입자의 **산소 분포 변화 + 고립(isolation)** ⇒ **R4 와 Ea(R4) 증가** ⇒ 용량 감소.
- `[인쇄]` "It is **unclear at the moment why the kind of the electrolyte affects the physical
  characteristics of the active material**, and further study is needed … as well as to
  **reinforce the R4 assignment**." ← ★ **저자들이 스스로 R4 귀속이 덜 굳었다고 적는다.**

## §3.3 의 요약 (인쇄된 2 기구)

`[인쇄]` "two degradation processes. **One is the oxygen migration** to cause chemical
composition change in the active material and sulfide solid electrolyte, which seems to be
responsible for the **increases of R3**. The other one is the **void formation** seen in the
LPSI system that causes the increase in **R4 and the diffusion-related resistance**."

# §4 Conclusion (전수)

`[인쇄]`:
1. 전고체 3전극 셀로 **NCM523 과 Li-In 의 임피던스 성분을 두 전해질계에서 분리**했다.
2. **다섯 성분** (R1 이온수송 · R2 Al 집전체\|NCM 전자 · R3 NCM\|전해질 전하이동 ·
   R4 2차 입자 내 1차 입자 간 전하이동 · Wo Warburg).
3. `[인쇄]` "The **DRT analysis is effective to separate these components to design
   appropriate equivalent circuits**."
4. `[인쇄]` "During repeated cycling, **the main cause of the degradation is the increase in
   R3**" — SEM/EDX 상 **활물질\|고체전해질 계면의 부반응**에서 온다.
5. `[인쇄]` "**Void formation by particle cracking** also affects the increase in R4, that leads
   to the **capacity loss** particularly seen in the LPSI electrolyte systems."
6. `[인쇄]` "Such quantitative analysis … using the three-electrode cell is **essential for
   degradation diagnosis** for ASS-LIBs."

⚠ `[재현]` **4 와 5 가 서로 당긴다**: `R3` 는 **두 계에서 똑같이** 자라는데 **용량 손실은
LPSI 에만** 있다. 따라서 **"주 원인이 R3" 은 "임피던스 상승의 주 원인" 이지 "용량 손실의
주 원인" 이 아니다.** 논문은 두 뜻의 "degradation" 을 한 문장에서 바꿔 쓴다 (D9).

# SI (6 쪽 전수)

## Fig. S1 — LPSI 의 DRT (λ = 6.0×10⁻²) + K–K 잔차

`[도표]` (a)(b)(c) DRT: 세로 **DRT / Ω s**, 가로 **Frequency / Hz** (10⁻¹ – 10⁶),
**before(밝은 빨강) / after(진한 갈색)**, 봉우리 라벨 **P_R2 · P_R3 · P_R4**.

| | 283 K (a) | 293 K (b) | 303 K (c) |
|---|---|---|---|
| **before** P_R4 / P_R3 | ≈20 / ≈30 | ≈10 / ≈15 | ≈6 / ≈8 |
| **after** P_R4 / P_R3 | **≈118 / ≈205** | ≈52 / ≈92 | ≈21 / ≈43 |
| P_R2 (after) | ≈8 (10⁵ Hz) | ≈8 | ≈4 |
| 최저 주파수 끝 | before ≈50 → after ≈175 (0.1 Hz) | — | — |

★★ `[도표]` **"before" 곡선에서는 P_R3 와 P_R4 가 봉우리라기보다 완만한 혹이다** —
283 K 에서 골(≈18)과 마루(≈30)의 비가 **1.7**, 293 K 에서 **1.5**, 303 K 에서 **1.3**.
`[해석]` `[인쇄]` "the **independent** components … are **confirmed**" 는 **육안 판정**이고,
λ 를 키우면 두 혹은 하나로 합쳐진다. **개수를 정한 것은 데이터가 아니라 λ 다**(G10).

`[도표]` (d)(e)(f) **Lin-KK 잔차**: 세로 **Residuals / −** (**무차원 표기**, ±0.6), 가로 10⁻³–10⁶ Hz.
거의 전 대역에서 |잔차| < 0.05 이고, **10⁻³ – 10⁻¹ Hz 에서만 ±0.2 … ±0.4** 로 커진다.
⚠⚠ `[해석]` **축 라벨이 무차원이면 0.4 = 40 %** 다 — Lin-KK 관례(보통 % 단위, |Δ| < 1 %)와
자릿수가 다르다. **둘 중 하나다**: (ㄱ) 라벨이 실제로는 % 이고 0.4 % 라면 정상적인 검증이다,
(ㄴ) 무차원이라면 **저주파에서 스펙트럼이 K–K 를 크게 벗어난다**. **어느 쪽이든 G5 의
"기준극이 안정하다" 는 따라오지 않는다.**

## Fig. S2 — LPSCl 의 DRT (λ = 8.5×10⁻⁴) + K–K 잔차

`[도표]` 봉우리 라벨이 **넷**이다: **P_R1′ · P_R2 · P_R3 · P_R4**.
- (a) 283 K: after 의 **P_R1′ 가 ≈10⁶ Hz 에서 높이 ≈190 의 뾰족한 첨봉**, P_R3 ≈125 (넓음),
  P_R4 ≈65, P_R2 ≈20. before 는 P_R3 ≈40 · P_R1′ ≈180.
- (b) 293 K: after P_R1′ **≈100(첨봉, 축 상단을 친다)**, P_R3 ≈55, P_R4 ≈25.
- (c) 303 K: after P_R1′ ≈33, P_R3 ≈27, P_R4 ≈13.
- 최저 주파수(0.2–0.3 Hz)에서 **축 밖으로 치솟는 스파이크**(Warburg).

★★★ `[해석]` **이것이 이 위키가 찾던 λ 대조 실측이다.** **같은 연구실 · 같은 소프트웨어 ·
같은 셀 구조 · 같은 측정기**인데 **λ 가 70 배 다르고, 분해된 봉우리 개수가 3 ↔ 4 로 다르다.**
논문은 그 차이를 **재료 탓**(LPSCl 의 낮은 Young 계수 → void → 용량성 성분)으로 돌리지만,
**λ 를 같게 두고 비교한 그림이 없다.** ⇒ **"봉우리가 하나 더 있다" 와 "정규화가 70 배 약하다"
가 이 지면에서 구별되지 않는다.** [[drt-peak-count-nonidentifiability]] 의 C1 을 통과하면서
동시에 그 페이지의 논지를 **가장 선명하게 예시하는** 편이다.

⚠ `[도표]` **(d) 패널만 가로축이 10⁻²–10⁶ 이고 (e)(f) 는 10⁻³–10⁶ 이다** — 즉 **283 K 의
잔차 그림은 잔차가 가장 큰 최저주파 구간을 잘라내고 보여 준다**(그래서 완벽해 보인다).
그리고 **S1·S2 캡션이 둘 다 "(d-e)" 라고 쓰는데 패널은 (d)(e)(f) 셋이다**(D11).

## Fig. S3 — 3전극 분해의 자기 검증 (7 패널)

`[도표]` 각 패널에 **NCM523(빨강) · Li-In(파랑) · combined = 둘의 합(노랑 원) ·
cell impedance = 2전극 실측(보라 사각)** 네 곡선. (a)(b)(c) = LPSI 283/293/303 K,
(d)(e)(f) = LPSCl 283/293/303 K, (g) = **LPSI ↔ LPSCl 의 NCM523 비교 (293 K)**.

주요 판독:
- **(b) LPSI 293 K**: NCM523 절편 ≈60 Ω, 중주파 호 꼭대기 −Z″ ≈17 at Z′ ≈95(1 kHz 마커),
  골 ≈130, **1 Hz 마커 ≈150**, 이후 Warburg 가 Z′ ≈205 / −Z″ ≈62 까지. **Li-In 은 작다**
  (Z′ ≈60–100 구간, −Z″ ≲ 10). combined 와 cell 은 Z′ ≈300 까지 포개진다.
- ★★ **(a)(d) 에서 combined(노랑)가 cell(보라)보다 눈에 띄게 위에 있다.**
  (d) LPSCl 283 K 에서 노랑 꼭대기 **≈130 at Z′ ≈270**, 보라 꼭대기 **≈115 at Z′ ≈330**
  — **크기 ≈13 %, 위치 ≈60 Ω 어긋난다.** 두 곡선은 Z′ ≳450 에서 다시 만난다.
  `[해석]` **본문의 "agree well below 1 MHz" 는 저주파에서만 참이다.** 중주파(≈1 MHz–1 kHz)
  에서 3전극 합이 2전극과 갈리고, **논문은 이 구간을 정량하지 않는다** (D10).
- **(g)**: 두 전해질계의 NCM523 스펙트럼이 **거의 겹친다**(둘 다 절편 ≈60, 호 꼭대기 ≈14).
  LPSCl 쪽이 먼저 Warburg 로 꺾인다(Z′ ≈130 vs ≈135).
  `[재현]` **Fig. 5 의 `R3` 절대값(LPSI 79 Ω ↔ LPSCl 18 Ω, 4.3 배)과 겉보기가 다르다** —
  LPSCl 은 `R1′` 반원이 따로 있어 **총합이 비슷해지기 때문**이고, 논문은 이 대비를
  한 번도 논하지 않는다.

## Fig. S4 — 대칭셀 (R2 귀속의 유일한 독립 근거)

`[도표]` (a) 모식도 **Al-plane \| NCM523 composite \| Al-plane**, Li⁺ 차단(×) · e⁻ 통과(↑).
(b) Nyquist, **50.0 mg(빨강) / 93.5 mg(파랑)**, 축 Z′ 6–16 Ω, −Z″ −2…8.
- 빨강: 절편 ≈6.7 → **호 하나**(꼭대기 ≈1.0 at Z′ ≈9) → 닫힘 ≈11.4. **1 kHz·1 Hz 마커가
  끝에 뭉쳐 있다.**
- 파랑: 절편 ≈7.8 → 첫 호(꼭대기 ≈1.45 at Z′ ≈11) → 골 ≈12.2 → **둘째 호**(≈0.75 at ≈13.8)
  → 닫힘 ≈14.8.
⚠⚠ `[도표]` **"두 개의 반원이 나타난다" 는 93.5 mg 에서만 보인다** — 50.0 mg 곡선에는
반원이 **하나**다. 본문은 `[인쇄]` "There appear **two semicircles** … and **only the latter
increased**" 라고 두 시료 공통인 것처럼 적는다 (D12).
(c) DC 저항 vs 질량 **2 점**, 직선 `[인쇄]` **R = 0.059M + 8.011**.
⚠ `[재현]` 절편 8.011 Ω 은 **2 점 외삽**이고, 본문은 같은 값을 **7.9 Ω** 라 부른다 (G13).
⚠ `[재현]` 그리고 **고주파 절편 자체가 질량에 따라 6.7 → 7.8 로 움직인다** — 즉 "절편 =
계면" 과 "고주파 반원 = 계면" 이라는 **두 정의가 같은 문단에서 섞여 있다.**

## Table S1 — 입자 크기별 `R3` 적합 파라미터 (SoC 100 %) — 전수

| | 283 K 5.0 µm | 283 K 11.2 µm | 293 K 5.0 µm | 293 K 11.2 µm | 303 K 5.0 µm | 303 K 11.2 µm |
|---|---:|---:|---:|---:|---:|---:|
| **R3 / Ω** | **184.6 ± 0.4** | **347 ± 2** | **76.6 ± 2** | **161 ± 1** | **45.9 ± 0.3** | **93.9 ± 0.9** |
| `R3_11.2/R3_5.0` | **1.88** | | **2.10** | | **2.04** | |
| **CPE2-C / F** | 1.1×10⁻⁴ | 1.39×10⁻⁵ | 1.2×10⁻⁵ | 1.34×10⁻⁵ | 2.4×10⁻⁵ | 1.82×10⁻⁵ |
| **CPE2-p / −** | 0.57 ± 0.02 | 0.76 ± 0.03 | 0.76 ± 0.09 | 0.76 ± 0.02 | 0.71 ± 0.07 | 0.71 ± 0.03 |
| **τ3 / s** | 1.1×10⁻⁴ | 9.0×10⁻⁴ | 1.1×10⁻⁴ | 3.2×10⁻⁴ | 6.5×10⁻⁴ | 1.2×10⁻⁵ |

★★★ **이 표가 이 흡수의 핵심 입력이다** — `R`, `Q`(CPE-C), `p`(CPE-p) 가 **같은 계면에
대해 한 표에** 있다. 16호의 처방을 처음으로 **계산할 수 있다**(§곱 축퇴 검사).

⚠ `[재현]` **인쇄된 τ3 중 셋이 `(R·Q)^{1/p}` 와 10 배 어긋난다**:

| 조건 | `(R·Q)^{1/p}` 계산 | 인쇄된 τ3 | 비 |
|---|---:|---:|---:|
| 283 K 5.0 | **1.07×10⁻³** | 1.1×10⁻⁴ | **9.8** |
| 283 K 11.2 | 8.95×10⁻⁴ | 9.0×10⁻⁴ | 0.99 ✔ |
| 293 K 5.0 | 1.01×10⁻⁴ | 1.1×10⁻⁴ | 0.92 ✔ |
| 293 K 11.2 | 3.10×10⁻⁴ | 3.2×10⁻⁴ | 0.97 ✔ |
| 303 K 5.0 | **6.82×10⁻⁵** | 6.5×10⁻⁴ | **0.10** |
| 303 K 11.2 | **1.27×10⁻⁴** | 1.2×10⁻⁵ | **10.6** |

⇒ **10 의 지수 오타 3 건**(D2). 그리고 **303 K 의 두 오타는 방향이 반대**라, 인쇄된 표만
보면 τ3 비가 **0.018**(54 배 차이)로 읽힌다.

⚠⚠ `[재현]` **그래서 본문의 `[인쇄]` "the time constants are nearly unchanged" 는 어느 쪽으로도
성립하지 않는다** (D3):
- 인쇄된 표대로면 비 = **8.2 / 2.9 / 0.018**
- 우리 재계산대로면 비 = **1.20 / 0.33 / 0.54** (즉 293 K 에서 **3.0 배**)

# 그림 판독 — 실제로 본 것 (크롭 13 장 중 **11 장** + 크로퍼가 놓친 1 장)

> **본 것**: 본문 **Fig. 1 · 2 · 3 · 4 · 5**(+ (c) 확대) **· 6 · 7**, SI **Fig. S1 · S2 · S3 · S4**
> = **11 개 파일**. 여기에 **캡션이 없어 크로퍼가 놓친 1 쪽의 Graphical Abstract** 를
> `page.get_pixmap(clip=…)` 로 직접 렌더해 열람했다.
> **안 본 것**: 표 크롭 2 장(`tab_1.png` · `tab_S1.png`) — PDF 텍스트가 정확해 이미지로
> 읽지 않는 것이 이 도구의 규칙이다. **그림 중 안 본 것은 0.**
>
> **누락 기계 확인** (17호에서 Figure 2 를 놓친 전례 때문에): `get_images()` /
> `get_drawings()` 를 페이지별로 세었다 — p1 **4 img**(= Graphical Abstract + 저널 로고
> 2 + Check-for-updates) · p2 0 img/359 draw(본문) · **p3 2 img**(Fig. 1·2) ·
> **p4 1 img**(Fig. 3) · p5 0 · **p6 2 img**(Fig. 4·5) · **p7 1 img**(Fig. 6) ·
> **p8 1 img**(Fig. 7) · p9·p10 0(결론·참고문헌).
> ⇒ **캡션 앵커가 본문 그림 7 장을 전부 잡았고, 놓친 그래픽은 1 쪽의 무캡션 도판뿐**이다.

## Graphical Abstract (1 쪽, 무캡션 — 크로퍼 밖)

`[도표]` **Fig. 5(a) 와 같은 막대그래프**(Log(R/Ω), R1–R4, fresh 파랑 / aged 분홍) +
셀 모식도 삽입: **Current collector(검정) ↔ e⁻–R2**, **LiNi₀.₅Co₀.₂Mn₀.₃O₂(분홍 입자) ↔
Solid electrolyte(노랑 입자)**, 화살표 **R3**(입자–전해질 계면), **R4**(2차 입자 내부, Li⁺),
**R1**(전해질 내부, 파랑).
`[해석]` **표지 그림이 곧 이 편의 귀속 지도**이고, **R4 를 2차 입자 안쪽에 그린다** —
본문이 "reinforce 가 필요하다" 고 유보한 바로 그 귀속을 표지가 확정형으로 그린다.

## Fig. 1 — 충방전 곡선 4 패널 (★ Q5 의 1 차 증거)

`[도표]` 좌축 **Potential / V vs. Li₇Ti₅O₁₂/Li₄Ti₅O₁₂** (0.85–2.85), 우축 **V vs. Li/Li⁺**
(2.40–4.40), 가로 **Capacity / mA h g⁻¹** (0–200). 1st/2nd × charge/discharge 4 곡선.
- **(a) LPSI NCM523**: 1st 충전 ≈175, 1st 방전 ≈143; 2nd 충전 ≈143. 평탄부 ≈3.65–3.70 V
  뒤 4.20 V 까지 상승, 방전 말에 급락. `[재현]` **초회 효율 ≈82 %**.
- **(c) LPSCl NCM523**: 1st 충전 ≈165, 방전 ≈150. `[재현]` **초회 효율 ≈91 %**.
- ★★★ **(b)(d) Li-In 상대극**: **두 계 모두 전 구간(0 → 175 mAh g⁻¹, 충·방전 4 곡선 전부)
  에서 완전히 평탄**, `[도표]` **≈−0.95 V vs R-LTO = ≈0.60 V vs Li/Li⁺**.
  축 분해능상 우리가 읽을 수 있는 한계는 **≈±0.03 V** 다.

★★ `[재현]` **왜 평탄한지가 계산된다** (§2.1 의 `x_Li` = 37.7 at% 와 함께):
옮겨 가는 전하가 **0.0159 mmol(LPSI) / 0.0224 mmol(LPSCl)** 이고 음극 Li 재고가
**0.151 mmol** 이므로 **재고비 9.5 배 / 6.7 배**, **`x_Li` 는 37.7 → 40.0 / 41.0 at%** 로만
움직인다. **In + LiIn 2 상역 안에서 거의 제자리다.** ⇒ **17호가 본 고갈(In-rich → +0.7 V)이
일어날 수 없는 설계**다 (§Q5 대질).

## Fig. 2 — SoC 스윕 Nyquist + 등가회로 + R(SoC) + Arrhenius

`[도표]` (a) Nyquist 298 K: x **Z′/Ω 50–230**, y **−Z″/Ω 0–180**. SoC 0/25/50/75/100 %,
마커 **◆ 1 MHz(청록) · 1 kHz(연두) · 1 Hz(자홍)**. 절편 ≈57–60. 삽입도(x 55–75, y 0–20)가
**R2** 를 보여 준다. **SoC = 0 %(검정)만 완전히 다르다** — 반원이 닫히지 않고 Z′ ≈145 에서
−Z″ ≈75 까지 치솟는다. 나머지 SoC 는 Z′ ≈120–130 에 골, Z′ ≈140–170 에 둘째 혹,
이후 Warburg 가 Z′ ≈210 / −Z″ ≈60 까지.
`[도표]` (b) **등가회로**: **L1 — R1 — (R2‖CPE2) — (R3‖CPE3) — (R4‖CPE4) — Wo1**.
`[도표]` (c) **R vs SoC**: R3 **180 → 80 → 60 → 57 → 60 Ω**(SoC 0/25/50/75/100),
R4 **73 → 35 → 25 → 23 → 23**, R1 **≈55 평탄**, R2 **≈0 에 붙어 있음**.
`[도표]` (d) Arrhenius `ln(R⁻¹)` vs `10³/T`: 초록(**R2**)이 가장 가파르다(−1.0 → −3.05),
빨강(**R3**) −3.9 → −5.2, 황토(**R4**) −3.35 → −4.5, 파랑(**R1**) −3.9 → −4.5. **각 3 점.**

★ `[재현]` (d)의 빨강을 저항으로 되돌리면 **R3 ≈49 Ω(303 K) / ≈181 Ω(283 K)** —
**Table S1 의 45.9 / 184.6 Ω 과 정합**한다 ✔.
⚠ `[재현]` 그러나 **(c)의 SoC 100 % R3 ≈60 Ω(298 K)** 과 **Fig. 5(a)의 신품 R3 ≈79 Ω(298 K)**,
그리고 **Table S1 을 Ea = 49 kJ mol⁻¹ 로 298 K 에 외삽한 ≈55 Ω** — **셋이 55 / 60 / 79 Ω
로 1.45 배 벌어진다**. 전부 "LPSI · D50 5.0 µm · SoC 100 %" 라는 같은 이름표를 달고 있다.
★★ `[해석]` **이것이 이 편에서 우리가 만들 수 있는 유일한 셀 간 산포 추정이다: ≈±20 %.**
그리고 **입자 크기 효과(2.0 배)는 그 산포의 ≈2 배**, **노화 효과(6.5 배)는 ≈5 배**다.
⇒ 노화 결론은 산포 위에 안전하게 서 있고, **입자 크기 결론은 여유가 훨씬 적다.**

## Fig. 3 — 입자 크기 (a) + 단면 SEM/EDX (b)–(e)

`[도표]` (a) Nyquist 293 K: x **50–400 Ω**, y **0–350**. 절편 **둘 다 ≈75 Ω**.
- **D50 = 5.0 µm(검정)**: 1 kHz 마커 ≈112, 호 꼭대기 ≈25, 1 Hz 마커 ≈175, Warburg 가
  Z′ ≈300 / −Z″ ≈110 까지.
- **D50 = 11.2 µm(빨강)**: 1 kHz 마커 ≈148(호 꼭대기 부근), 호 꼭대기 **≈55**, 골 ≈250,
  1 Hz 마커 ≈270, Warburg 가 Z′ ≈400 / −Z″ ≈122 까지.
⇒ 본문의 `R3` 76.6 ↔ 161 Ω 과 정합.

`[도표]` (b)(c) 단면 SEM + EDX 중첩 (Image-J 접촉 면적의 원자료):
- **(b) 5.0 µm**: 스탬프 **MAG 2500x · HV 15 kV · WD 8.0 mm**, 스케일바 **10 µm**,
  채널 **Ni Co Mn P S C O Nb I Al (10 종)**. 분홍 입자 + 청록 SE 기질, **검은 균열/공극이
  기질을 가로지른다**.
- **(c) 11.2 µm**: 스탬프 **MAG 1000x · HV 10 kV · WD 14.0 mm**, 스케일바 **20 µm**,
  채널 **Ni Mn P S C O I (7 종 — Co·Nb·Al 없음)**. 배경이 연보라, 입자는 붉은 얼룩.
⚠⚠⚠ `[도표]` **캡션은 (b)(c)를 둘 다 "× 2500" 이라고 쓰는데 (c)의 스탬프는 1000x 이고
스케일바도 2 배다. 가속전압(15 ↔ 10 kV)·WD(8.0 ↔ 14.0 mm)·EDX 채널 수(10 ↔ 7)도 다르다.**
⇒ **이 편의 유일한 접촉 면적 측정(비 2.0)이 배율·대비 조건이 다른 두 이미지에서 나왔다**
(D1). 임계값·분할 방법·오차도 없다.

`[도표]` (d)(e) ×50,000 (스탬프 **50.0kx** ✔ 캡션 일치): 둘 다 2차 입자 내부의 1차 입자와
입계가 보인다. **(e) 11.2 µm 쪽이 쐐기 모양 검은 void 가 더 많고 날카롭다.**
**(d) 5.0 µm 에도 큰 검은 영역이 있다.** **정량 0.**

## Fig. 4 — 열화 전후 (충방전 + Nyquist)

`[도표]` (a) LPSI: before(빨강) 충전 ≈145 · 방전 ≈143; after(진갈색) 충전 ≈105 ·
방전 ≈103. after 의 충전 곡선이 **위로**, 방전 곡선이 **아래로** 이동(과전압 증가).
`[도표]` (b) LPSCl: before(연두) ≈148, after(진녹) ≈147. **용량이 거의 그대로**이고
**곡선 모양만 기울어진다**(방전 초기 전위 강하).
`[도표]` (c) LPSI Nyquist: 축이 **0–1000 Ω** 으로 커진다. after 는 호 꼭대기 ≈75 at Z′ ≈230,
골 ≈390, 1 Hz 마커 ≈430, 그 뒤 **Warburg 가 Z′ ≈960 / −Z″ ≈660 까지** 치솟는다.
`[도표]` (d) LPSCl Nyquist: 축 **0–350 Ω**. after 호 꼭대기 ≈35 at Z′ ≈150, 골 ≈250,
1 Hz ≈270, Z′ ≈345 / −Z″ ≈75 까지.
★★ `[도표]` **가장 크게 자라는 것은 저주파 Warburg 다** — LPSI 의 −Z″ 가 660 Ω 에 이른다.
**그런데 `Wo` 의 값은 지면 어디에도 없다**(G9). `[인쇄]` 본문은 "diffusion-related
resistance" 가 늘었다고 한 줄 적을 뿐이다.

## Fig. 5 — 적합 파라미터 비교 (로그 막대) — 위 §3.3 표의 원자료

`[도표]` (a)(c) **Log(R/Ω)**, (b)(d) **−Log(τ/s)**, fresh 파랑 / aged 분홍.
(a)(b) = LPSI (R1·R2·R3·R4 / T2·T3·T4), (c)(d) = LPSCl.
⚠ `[도표]` **(c)의 첫 막대 라벨이 "R1′+R2′" 다** — 본문·회로도 어디에도 **R2′ 라는 기호가
없다**(본문은 `R1 + R1′`). 500 % 확대해 재확인했다 (D13).
⚠ **캡션에 온도·SoC 가 없다**(G14).

## Fig. 6 — LPSI 단면 SEM/EDX (before / after)

`[도표]` (a) **before** ×10,000(스탬프 10000x, 15 kV, WD 8.0): 분홍 2차 입자 + 회색 SE,
**기질과 입자 주변에 검은 균열**. 채널 **Ni Co Mn O (4 종)**. O·Ni 맵은 입자 위치에 밝고
P 맵은 입자 위치에 어둡다(= 입자에는 P 가 없다).
`[도표]` (b) **after** ×10,000(15 kV, WD 8.1): 대비가 낮고 흐리다. 채널 **Ni Co Mn O Nb (5 종)**.
★ **O 맵에서 입자를 두르는 밝은 띠**가 보인다 — 본문이 말하는 **두께 2 µm 퇴적층**.
스케일바가 2 µm 이므로 `[도표]` **띠 폭 ≈1–2 µm** 로 읽힌다.
⚠ `[도표]` **P 맵에서는 대응하는 밝은 띠를 확인하기 어렵다** — 전체적으로 균일한 파랑에
입자 자리만 어둡다. 본문은 `[인쇄]` "layers … that contain **O and P**" 라고 쓰지만
**선 스캔·정량·원소비가 없다**.
`[도표]` (c) **after** ×25,000: 2차 입자 하나의 내부에 **미세한 검은 void 가 다수**.

## Fig. 7 — LPSCl 단면 SEM/EDX (before / after)

`[도표]` (a) **before** ×10,000 — 스탬프 **HV 5 kV · WD 13.9 mm**, 채널 **Ni Co Mn P O Nb**.
입자 윤곽이 또렷하고 **이미 사이클 전에도 2차 입자 안에 쐐기형 void 와 균열이 보인다**.
`[도표]` (b) **after** ×10,000 — **HV 15 kV · WD 8.1 mm**, 채널 **Co P S O Nb Ti Cl Ni Mn (9 종)**.
입자 둘레에 뚜렷한 띠가 없다(본문 주장과 일치). P 맵은 입자 자리만 어둡다.
`[도표]` (c) **after** ×50,000 — 입자/SE 경계와 오른쪽의 검은 void.
⚠⚠ `[도표]` **(a)와 (b)의 가속전압이 5 kV ↔ 15 kV 로 다르다.** EDX 상호작용 부피와 검출
깊이가 달라진다. **"LPSCl 에는 퇴적층이 안 보인다" 는 이 비교 위에 서 있다** (D14).
⚠ 채널 목록에 **Ti** 가 있다 — R-LTO 기준극의 원소다. 검출됐다는 뜻인지 채널만 켠 것인지
지면이 말하지 않는다.

# 어긋남 원장 (Discrepancies)

| # | 내용 | 층위 |
|---|---|---|
| **D1** | ★★★ **Fig. 3 캡션 "(b), (c) … (× 2500)" ↔ 스탬프 (b) 2500x / (c) 1000x**, 스케일바 10 ↔ 20 µm, HV 15 ↔ 10 kV, WD 8.0 ↔ 14.0 mm, EDX 채널 10 ↔ 7 종. **유일한 접촉 면적 측정(비 2.0)의 원자료다** | 캡션 ↔ `[도표]` |
| **D2** | ★★ **Table S1 의 τ3 6 개 중 3 개가 `(R·Q)^{1/p}` 와 정확히 10 배 어긋난다** (283 K 5.0 · 303 K 5.0 · 303 K 11.2). 303 K 의 둘은 **방향이 반대** | SI 내부 (`[재현]`) |
| **D3** | ★★★ **본문 "the time constants are nearly unchanged" ↔ 인쇄된 표(비 8.2/2.9/0.018) 도, 우리 재계산(1.20/0.33/0.54) 도 그렇지 않다.** 293 K 에서 **3.0 배** | 본문 ↔ SI |
| **D4** | **"contacting area ratio … calculated to be 2.4" ↔ 반경비는 11.2/5.0 = 2.24** (식 (4)가 1/r 이므로 2.24 여야 한다) | 본문 ↔ 자기 식 (`[재현]`) |
| **D5** | ★★ **"Ea(R1) and Ea(R2) remained almost unchanged" ↔ Table 1 의 LPSI Ea(R2) 70±20 → 41±8 (구간이 안 겹친다).** 반대로 **"Ea(R3) increased" 는 LPSI 에서 49±6 → 54±1 로 구간이 거의 포개진다** | 본문 ↔ 자기 표 |
| **D6** | ★★ **LPSCl 의 R2 가 `[도표]` 6.9 배 자라는데 본문이 한 번도 언급하지 않는다** (LPSI 의 R2 만 "insignificant" 로 처리). `R2` = **집전체 전자 접촉** | 선택적 보고 |
| **D7** | ★★ **K–K 잔차 축이 "Residuals / −"(무차원)인데 값이 0.2–0.4 까지 간다.** Lin-KK 관례와 자릿수가 다르다. 그리고 그 잔차로 **기준극 안정성**을 주장한다 | SI 축 ↔ 본문 주장 |
| **D8** | ★★★ **자기 조건문의 귀결이 자기 데이터와 반대다** — "만약 퇴적층이 저항성 화합물이면 R3 증가가 LPSI 에서 더 클 것" ↔ 같은 절이 "R3 증가는 두 계가 같다" | 본문 내부 |
| **D9** | ★★ **결론 "the main cause of the degradation is the increase in R3" ↔ R3 는 두 계에서 같이 자라는데 용량 손실은 LPSI 에만 있다** (= R3 는 용량 손실의 원인이 아니다) | 결론 ↔ 결과 |
| **D10** | ★★ **Fig. S3(a)(d) 에서 combined(3전극 합) 와 cell(2전극)이 중주파에서 ≈13 % · ≈60 Ω 어긋난다** ↔ 본문 "agree well … below 1 MHz" | `[도표]` ↔ 본문 |
| **D11** | **SI 캡션 S1·S2 가 둘 다 "(d-e)" 인데 패널은 (d)(e)(f) 셋.** 그리고 **S2(d) 만 가로축이 10⁻²부터**라 잔차가 가장 큰 구간이 잘려 있다 | SI 캡션·축 |
| **D12** | ★ **Fig. S4(b) 에서 반원이 둘인 것은 93.5 mg 뿐이고 50.0 mg 은 하나다** ↔ 본문 "There appear two semicircles … only the latter increased" | `[도표]` ↔ 본문 |
| **D13** | ★ **Fig. 5(c) x축 라벨 "R1′+R2′" — 본문·회로도에 `R2′` 가 없다**(본문은 `R1 + R1′`) | 그림 라벨 ↔ 본문 |
| **D14** | ★★ **Fig. 7(a) before 는 5 kV, (b) after 는 15 kV 로 찍혔다.** "LPSCl 에는 퇴적층이 없다" 가 이 비교 위에 있다 | `[도표]` |
| **D15** | **대칭셀 절편을 "7.9 Ω"(본문) 과 "8.011"(SI 적합식) 두 값으로 부른다.** 그리고 "절편 = 계면" 과 "고주파 반원 = 계면" 두 정의가 같은 문단에 섞인다 | 본문 ↔ SI |
| **D16** | **Ohzuku, Ueda, Yamamoto, *JES* 142 의 연도를 "(2022)" 로 적는다**(실제 1995). ref [33] | 참고문헌 |
| **D17** | ⚠ **Fig. 2(c) SoC100 R3 ≈60 Ω · Fig. 5(a) 신품 R3 ≈79 Ω · Table S1 외삽 ≈55 Ω** — 같은 이름표의 세 값이 **1.45 배** 벌어진다 (논문 무언급; 우리는 이것을 셀 간 산포 추정으로 쓴다) | `[도표]`·`[재현]` |

# 우리 축 판정 (Q1–Q8) — 닻 채움표 18호 행의 근거

| 축 | 판정 |
|---|---|
| **Q1 접촉 손실 정량** | **부분 — 그리고 계보에서 가장 가까이 갔다가 돌아선다.** ① `[인쇄]` **Image-J 로 SE\|활물질 접촉 면적을 실제로 쟀다**(계보 최초의 **이미지 기반 접촉 면적 측정**) — 그러나 나온 값은 **입자 크기 두 시료의 비 2.0** 하나이고 **절대 면적·분율·오차·임계값이 없다**(G6), 원자료 두 장은 **배율이 다르다**(D1). ② `[인쇄]` 식 (4) `S_w = 3M/(dr)` 는 **완전구 기하 면적**이고, `[인쇄]` "**completely immersed**" 가정으로 **접촉 분율을 소거**한다 — 16호의 `a_V = 3ε/r` 과 **같은 자리, 같은 수법**. ③ ★★★ **노화 축의 `θ` 는 0 이다** — 그런데 이번에는 **도구(Image-J)와 시편(Fig. 6·7)이 둘 다 지면에 있다.** ④ ★★★★ 대신 **말로는 가장 멀리 간다**: `[인쇄]` "insulative layers **completely cover** the active material to make the particle **inactive**, such **dead particles** … no contribution … **could explain the large capacity decrease**" = **`θ_AM` 의 기구 서술**. **값 0.** |
| **Q2 독립 관측** | **★★★ 있다 — 계보 세 번째 전극 분해이고, 열화를 동반한 첫 편.** ① **R-LTO 메시 3전극**(전극별 임피던스 + 전극별 충방전 곡선) ② **입자 크기 스윕 2 점**(면적 여기) ③ **온도 스윕 3 점**(Ea) ④ **SoC 스윕 5 점** ⑤ **Al\|복합체\|Al 전자 차단 대칭셀**(R2 귀속) ⑥ **단면 FE-SEM + EDX 원소 맵**(노화 전후) ⑦ **전해질 2 종 대조**. ★ `[인쇄]` **2전극 = 3전극 합** 자기 검증도 있다(⚠ 중주파에서 어긋난다, D10). ⚠ 그러나 **`LAM_PE` ↔ 접촉 손실을 가르는 데 쓰인 조합은 0** — 접촉 면적은 **신품 입자 크기 축에서만** 쟀다 |
| **Q3 라벨 층위** | **fitted — 그리고 층이 하나 더 깊다.** 열화 라벨 = `R1..R4` 의 **등가회로 적합값**이고, 그 회로의 **차수와 시상수가 DRT 에서 왔으며 DRT 는 λ 가 정했다**(§2.3 의 인쇄된 절차). ★ **단, 이 계보 최초로 ± 를 인쇄한다** (Table 1 의 Ea, Table S1 의 `R3`·`p`) — ⚠ **그 ± 는 3 점 회귀·단일 적합의 표준오차이고 셀 간 반복이 아니다**(G1). ⚠ `CPE2-C` 와 `τ3` 에만 ± 가 없다(G7) — **우리 검사가 쓰는 바로 그 값**. ★★ 그리고 **용량 축은 fitted 가 아니다** — `[인쇄]` 0.1 C RPT 의 실측 용량이고, **컷오프가 작업전극 전위**라 상대극 오염이 없다 |
| **Q4 유일성** | **0 / 18. ★ 그러나 열한 번째 성질이 새롭다 — "축퇴를 'A 또는 B' 로 인쇄하고 가르지 않는다".** `identifiab*`·`uniqu*`·`uncertaint*`·`degenerac*`·`condition number`·`error bar`·`n =` **전수 0 회**. 그런데 `[인쇄]` "the **chemical composition at the interface or the contact area** … changed" 는 **우리 닻 물음의 두 가지를 이름으로 나란히 적은 문장**이다. 계보: 안 쟀다(1–7) → 이름만(8) → 지문이 자기 표에(9) → 분야가 명제로(10) → 재료만(11) → 0(12·13) → 역문제 없음(14) → 추정기 없음(15) → 밟고 지나갔다(16) → 인쇄로 사양(17) → **18호: 갈림을 인쇄하고 갈리지 않은 채 다음 문단으로 간다.** ★★ 그리고 **가를 입력을 자기 지면에 갖고 있다**(§곱 축퇴 검사) — 9호가 "지문이 자기 표에" 였다면 **18호는 "해답이 자기 표에"** 다 |
| **Q5 Li-In 기준** | **★★★ 있다 — 그리고 성질이 세 편 중 가장 다르다.** ① **기준극이 Li-In 이 아니다**: **R-LTO 메시**(부분환원 Li₄Ti₅O₁₂, `[인쇄]` 전위 **1.55 V vs Li/Li⁺ 를 가정**). ⇒ **Li-In 이 처음으로 "기준" 이 아니라 "피측정 전극" 이 된다.** ② `[도표]` **Fig. 1(b)(d): 두 전해질계 모두 0.1 C 전 사이클에서 Li-In 이 완전 평탄, ≈0.60 V vs Li/Li⁺** (판독 분해능 ≈±30 mV — **17호의 ±10 mV 보다 좁게는 못 잰다**). ③ ★★ `[재현]` **평탄한 이유가 설계에 있다**: `x_Li` = **37.7 → 40.0 at%**(재고비 **9.5 배**), 전류밀도 **0.054 mA cm⁻²** = 17호 0.1 C 의 **1/5**, 17호 CA 의 **1/300**. ⇒ **17호와 모순이 아니라 반대편 끝의 표본**이다. ④ ⚠ 기준 축이 **R-LTO 의 가정된 1.55 V** 로 옮겨갔고 **자기 셀에서 검증 0**(G4), 검증 주장은 **K–K 잔차**라는 **범주 오류**(G5). ⑤ ★ `[인쇄]` Li-In 전위의 근거로 **Santhosha 2019** 를 인용하며 **서지가 정상**이다 — 17호의 권호 오기가 확인된다 |
| **Q6 압력** | **★ 거의 없다 — 그리고 "없음" 의 형태가 가장 날카롭다.** `pressure`·`stack pressure`·`hysteres*` **본문 0 회**, `MPa` **2 회**(제작 **110 MPa** · 대칭셀 **150 MPa**). **운전 압력은 값도 장치도 문장도 없다**(G2). ⚠⚠ **그런데 이 편의 두 열화 기구 중 하나가 `void formation` 이고**(`void` 7 회), LPSCl 의 R1′ 반원도 `[인쇄]` "**void formation**" 으로 설명된다. ⇒ **압력에 가장 민감한 양을 주인공으로 삼으면서 압력을 통제하지 않은 첫 실측 편.** ★ 비교: 16호 `pressure` 49 회 · 17호 7 회 · **18호 0 회** |
| **Q7 dead Li** | **해당 없음** (Li-In 음극). `dendrit*` 0. ⚠ **`dead` 1 회는 음극이 아니라 양극이다** — `[인쇄]` "such **dead particles**"(절연층에 덮인 NCM 2차 입자). **낱말은 같고 대상이 다르다** |
| **Q8 화학·OCP** | **★★ 있다 — 그리고 계보 최초의 조합이다.** **LiNbO₃ 코팅 NCM523**(D50 **5.0** / **11.2 µm**) + **LPSI(2.6 mS cm⁻¹, D50 5.0 µm)** 또는 **LPSCl(1.8 mS cm⁻¹, D50 0.66 µm)** + **Li-In**. `[인쇄]` 창 **2.40–4.20 V vs Li/Li⁺**, 평탄 ≈3.7 V 뒤 **전 구간 기울기 있음**, 0.1 C 용량 **140–150 mAh g⁻¹**(공칭 160). ★ **V–Q 곡선 6 장**(양극 4 + **음극 2**) — 그리고 **음극 곡선이 전극 분해로 따로 그려진 것이 17호에 이어 두 번째**다. ⚠ `OCV`·`GITT` **0 회** — 전부 0.1 C pseudo-OCV. ★★ **SoC 축 위의 `R3(SoC)` 5 점**(Fig. 2c)은 이 계보에서 **가장 조밀한 양극 전하이동 저항의 SOC 곡선**이다 |

**채움표 누적: 17편 ≈10.0 → 18편 ≈10.5** (**Q1 +0.5** — 접촉 면적이 처음으로 **측정된 양**이
됐다; 비뿐이고 노화 축은 여전히 0 이라 반 칸). **Q4 는 그대로 0.**

# ★★★ 곱 축퇴 검사 — 16호 처방의 **두 번째 적용, 그리고 첫 성공**

16호 digest 와 [[assb-lampe-contact-product-degeneracy]] 가 세운 처방:

> **`R_CT·C_dl` 은 접촉 면적이 소거된 고유 시상수이고, `C_dl` 단독은 면적에 비례한다.
> 둘을 같이 보고하면 `θ` 와 `j₀` 가 갈린다.**

| 처방 입력 | 9호 | 16호 | 17호 | **18호 (이 편)** |
|---|---|---|---|---|
| `R_CT` | 적합 | Table 2 | 없다 | ✅ **Table S1 + Fig. 5** |
| `C_dl`/`Q`/CPE | 없다 | Table 2 | 없다 | ✅ **Table S1 (`CPE2-C`) + Fig. 5 의 τ** |
| CPE 지수 `p` | — | β 0.89/0.81 | — | ✅ **Table S1** (⚠ 노화 후는 없다, G8) |
| 면적을 바꾼 조작 | 없다 | 압력 2 점 | 없다 | ✅ **입자 크기 2 점** + ✅ **노화 전후** |
| **판정** | 곱을 적합했다 | 곱 위에서 한쪽을 골랐다 | 곱을 만들지 않았다 | ★ **우리가 곱을 만들 수 있다** |

## 검사 A — 입자 크기 축 (신품, Table S1)

논문의 주장: `R3` 비 0.5 = **접촉 면적 비 2.0–2.4 의 역수** ⇒ `R3` 는 계면 저항이고
**접촉은 균일**하다.
**검사**: 면적이 유일한 차이라면 `C_dl` 은 **면적에 비례**해야 하고(즉 5.0 µm 쪽이
**2.0–2.4 배 커야** 하고) `R·C` 는 **불변**이어야 한다.

`[재현]` (`C_eff = Q^{1/p}·R^{(1-p)/p}` — Hsu–Mansfeld/Brug 류 유효용량):

| T | `R3(11.2)/R3(5.0)` | `Q(5.0)/Q(11.2)` | **`C_eff(5.0)/C_eff(11.2)`** | `τ(5.0)/τ(11.2)` | `p` 가 같나 |
|---|---:|---:|---:|---:|---|
| **283 K** | 1.88 | 7.91 | **2.26** | 1.20 | ❌ 0.57 ↔ 0.76 |
| **293 K** | 2.10 | 0.90 | **0.68** | 0.33 | ✅ 0.76 ↔ 0.76 |
| **303 K** | 2.05 | 1.32 | **1.10** | 0.54 | ✅ 0.71 ↔ 0.71 |
| **면적 설명의 예측** | 2.0–2.4 | **2.0–2.4** | **2.0–2.4** | **1.0** | |

★★★ **판정: `p` 가 같은 두 온도(293·303 K)에서 용량은 면적처럼 스케일하지 않는다.**
`C_eff` 비가 **0.68 / 1.10** 인데 면적 설명은 **2.0–2.4** 를 요구한다 — **2–3 배 어긋난다.**
면적 설명이 맞는 유일한 온도(283 K, 2.26)는 **`p` 가 0.57 ↔ 0.76 으로 달라 두 `Q` 의 차원이
애초에 다른** 온도다.
⇒ `[해석]` **`R3` 비 ≈2 는 면적 비 ≈2 와 수치가 맞지만, 같은 표의 용량은 그 배정을
지지하지 않는다.** 남는 가능성은 셋이고 **논문은 셋 다 검토하지 않는다**: (ㄱ) 두 시료의
**고유 전하이동 속도가 다르다**(코팅 두께·표면 상태·입도 분포), (ㄴ) `C_dl` 이 접촉 면적의
대리가 아니다(LiNbO₃ 유전층이 지배), (ㄷ) **적합이 `R`–`Q` 를 교환한다**.

⚠⚠ `[재현]` **(ㄷ)을 의심할 근거가 같은 표에 있다**: **같은 계면의 `C_eff` 가 283/293/303 K
에서 5.82 / 1.32 / 1.49 µF 로 4.4 배 움직인다.** 이중층 용량이 20 K 에 4 배 변하는 물리는
없다. ⇒ **`Q` 는 이 적합에서 잘 정해지지 않는 파라미터이고, 그것이 ± 가 빠진 유일한
열이다**(G7). **그래서 우리는 검사 A 를 "반증" 이 아니라 "지지되지 않음" 으로 적는다.**

★ `[재현]` **부수적으로 얻어지는 절대 스케일** (⚠ 가정 위): 이중층 비용량을
**10 µF cm⁻²** 로 놓으면 293/303 K 의 `C_eff` 는 **실면적 0.13–0.15 cm²** 에 해당한다.
같은 전극의 **NCM 기하 표면적은 식 (4) 로 7.5 cm²**(D50 5.0 µm, 2.94 mg, d = 4.7 g cm⁻³)
이다 ⇒ **전기화학적으로 활성인 접촉은 입자 표면의 ≈2 %.**
⚠⚠ **이 숫자를 채움표에 올리지 않는다** — 비용량 10 µF cm⁻² 는 **우리 가정**이고(LiNbO₃
코팅 유전층이면 같은 자릿수이나 확인 불가), `C_eff` 자체가 위에서 본 대로 4 배 흔들린다.
다만 **방향은 분명하다: `[인쇄]` "completely immersed" · "uniform physical contact" 와
자기 용량 데이터가 맞지 않는다.**

## 검사 B — 열화 축 (Fig. 5, `[도표]`) ★★★★ 이 흡수의 최대 수확

**면적만 잃으면** `R ∝ 1/θ`, `C ∝ θ` 이므로 **`C` 비 = 1/(R 비)**.
**고유 동역학만 나빠지면** `C` 비 = **1.00**.

`[재현]` (`C ≡ τ/R`, Fig. 5 의 로그 막대 판독 ±0.04 ⇒ `C` 비 상대오차 ≈±18 %):

| 계 · 항 | `R` 비 | `τ` 비 | **`C` 비 (= τ/R)** | 순수 면적 예측 | 순수 동역학 예측 | **판정** |
|---|---:|---:|---:|---:|---:|---|
| **LPSI · R3** | **6.5** | 2.4 | **0.37 ± 0.07** | 0.15 | 1.00 | **둘 다** — 유효 면적 **≈2.7 배 감소** + 고유 `R_ct` **≈2.4 배 증가** |
| **LPSCl · R3** | **7.4** | 7.9 | **1.07 ± 0.19** | 0.13 | 1.00 | ★ **면적 손실 없음 — 전부 고유 동역학** |
| LPSI · R4 | 9.3 | 5.3 | 0.56 ± 0.10 | 0.11 | 1.00 | 둘 다 |
| LPSCl · R4 | 3.4 | 21 | **6.3** | 0.30 | 1.00 | ⚠ **비물리**(면적이 6 배 늘 수 없다) — `R4` 가 2.8 Ω 로 작아 잘 안 정해진다 |

★★★★ **그리고 이 분해가 같은 논문의 두 번째 관측과 독립으로 일치한다**:
`[인쇄]` **LPSI 에만** 2차 입자를 **두르는 O·P 퇴적층(2 µm)**이 생겼고 LPSCl 에는
`[인쇄]` "**not apparent**" 다. **덮으면 면적이 준다** ⇒ LPSI 의 `C` 비 0.37 ✔,
LPSCl 의 `C` 비 1.07 ✔.

★★★★ **그래서 이 검사는 저자가 남긴 "or" 를 실제로 가른다**:

> `[인쇄]` "the **chemical composition at the interface or the contact area** … changed"
> → `[재현]` **LPSCl 에서는 화학(면적 불변), LPSI 에서는 둘 다(면적 ≈1/2.7 + 화학 ≈2.4 배).**

⚠⚠ **단서 넷 — 이것은 재적합이 아니라 지면 숫자의 조합이다**:
(ㄱ) `R`·`τ` 가 **로그 막대 판독값**이다(수치 표 없음, G8). (ㄴ) `τ` 의 정의가 `(R·Q)^{1/p}`
라면 **노화 후 `p` 를 모른다**(G8) — `p` 가 함께 변하면 `C ≡ τ/R` 는 유효용량이 아니다.
(ㄷ) **`C_dl ∝ 접촉 면적`** 은 가정이다(검사 A 가 그 가정을 신품 축에서 흔든다).
(ㄹ) **조건당 셀 1 개**(G1)이고 우리가 추정한 셀 간 산포는 **±20 %**(D17) — `C` 비
0.37 과 1.07 의 차이는 그 산포보다 훨씬 크지만, **셀이 다르면 이 검사 전체가 무효**다
(같은 셀의 before/after 라는 보장은 `[인쇄]` "before and after the durability test" 뿐이다).

★★ `[해석]` **이 위키가 처방을 세운 지 두 편 만에, 처방이 실제로 무언가를 가른다.**
그리고 **처방의 입력이 이미 출판된 논문 안에 있다**는 것이 요점이다 — 새 실험이 아니라
**같은 표의 두 열을 곱하는 일**이었다.

# ★★★ 16호와의 대질 — 3전극 배정은 재현되는가

큐 문서가 이 흡수의 1순위로 지정한 물음이다. 16호(Ramanayagam 2026)의 결론 2 는
`[인쇄]` **"고·중주파 = 주로 양극, 저주파 = 주로 음극"** 이었다.

| | **16호 (Marburg, 2026)** | **18호 (Tokyo Tech, 2023 — 이 편)** |
|---|---|---|
| 기준극 | 리튬화 **Au/W μ-RE** ∅25 µm | **R-LTO 메시** (φ9 mm, Ni 메시) |
| 양극 | **단결정 NMC 83\|6\|11** | **다결정 NCM523**(2차 입자) |
| 전해질 | Li₅.₃PS₄.₃ClBr₀.₇ | **LPSI** 또는 **LPSCl** |
| 운전 압력 | **97 / 389 MPa** | **보고 없음** |
| 주파수 범위 | 10⁵ – 10⁻³ Hz | **7×10⁶ – 5×10⁻³ Hz** |
| **양극이 차지하는 대역** | ≈10⁴ – 10¹ Hz (+ 더 낮은 쪽 일부) | **1 MHz – 5 mHz 전체** (R1·R2 ~1 MHz · R3 ~1 kHz · **R4 ~1 Hz** · Wo < 1 Hz) |
| **음극(Li-In)이 차지하는 대역** | 10¹ – 10⁻¹ Hz (**저압에서 거의 전부**) | **저주파** — `[인쇄]` "the Li-In component, which **significantly affects the low-frequency behavior**" |
| 고주파 반원의 귀속 | `[인쇄]` **양극–집전체 계면**(저압에서만 보임) | ★ **양극–집전체 계면(`R2`)** — **대칭셀로 독립 검증** |
| 저주파 반원의 귀속 | **없다**(단결정이라 안 나타난다) | ★ **`R4` = 2차 입자 내부 1차 입자 간 전하이동** |

**판정 — 배정은 절반만 재현되고, 어긋나는 절반이 더 중요하다:**

1. ★ **고주파(≈1 MHz) = 양극–집전체 전자 접촉**: **두 편이 같다**. 그리고 **18호 쪽에
   독립 근거가 있다**(Al\|복합체\|Al 대칭셀, Fig. S4) — 16호는 문헌 인용이었다.
   ⇒ **이 한 칸은 두 편이 서로를 보강한다.**
2. ★ **중주파(10²–10³ Hz) = 양극 전하이동**: **같다**. 16호 `[도표]` ≈30–50 Hz,
   18호 `[인쇄]` ≈1 kHz — **1.5 자릿수 차이**지만 둘 다 "중주파 = 양극" 이다.
   ⚠ 두 편의 셀 기하·온도·SoC 가 달라 절대 주파수는 비교할 수 없다.
3. ★★★★ **저주파는 두 편이 다르다 — 그리고 16호가 그 사실을 알고 있다.**
   16호는 `[인쇄]` "Fukunishi 도 같은 중주파 반원을 봤다. 다만 Fukunishi 는 **저주파
   반원을 하나 더** 봤고 그것을 **2차 입자 NMC532 의 전하이동**으로 돌렸다. 이 논문은
   **단결정**을 써서 그 저주파 반원이 없다" 고 적는다. **18호를 읽으니 그것이 맞다** —
   `R4` 는 **2차 입자 안쪽**의 성분이고 **단결정에는 있을 수 없다**.
   ⇒ ★★★ **"저주파 = 음극" 은 재료의 함수다.** 다결정 양극을 쓰면 **양극이 저주파에
   반원을 하나 더 놓고, 그것이 음극 기여와 같은 대역에서 겹친다.**
   `[인쇄]` 18호 자신이 그렇게 말한다: "The existence of R4 is **apparent when the
   three-electrode cell is applied to separate the Li-In component**".
4. ★★ **Warburg(< 1 Hz)는 양극이다** — 18호에서 가장 크게 자라는 성분이고(Fig. 4c,
   −Z″ 660 Ω), **주파수만으로는 음극과 구별되지 않는다.**

★★★★ `[해석]` **이것이 10·11호가 세운 "분해의 비유일성" 계보의 세 번째 층이다.**
- **10호(Vadhva)**: `[인쇄]` **In–Li 셀과 Li 금속 셀은 전극↔주파수 귀속이 반대**이고
  "**system-by-system basis**" 가 필요하다 — **화학이 바꾼다**.
- **11호(Yu)**: 같은 봉우리의 **이름표가 상태·배선·조작으로 흔들린다**.
- **16호**: 전극별 DRT 의 **합이 완전지 DRT 가 아니다**.
- **18호(새로 들어오는 것)**: ★ **같은 화학(둘 다 In-Li 음극 + 황화물 + 층상 양극)에서도
  양극 활물질의 형태(단결정 ↔ 다결정)가 "저주파 = 음극" 규칙을 깬다.**
  ⇒ **주파수 → 전극 규칙은 화학뿐 아니라 미세구조의 함수다.** 그리고 **이것은 두 편이
  서로를 인용하며 동의하는 내용**이라 `[해석]` 이 아니라 **문헌이 이미 말한 것**이다.
  ⚠ 다만 **두 편 다 이 함의를 "규칙이 없다" 로 일반화하지 않는다** — 16호는 자기 셀에
  저주파 반원이 없다는 관찰로, 18호는 자기 셀에 있다는 관찰로 끝낸다.

# ★★ 17호(Yanev 2024)와의 대질 — Q5 와 "상대극이 미는 겉보기 용량"

## (가) 17호가 연 오염 경로가 18호에서는 **설계상 닫혀 있다**

17호의 최대 수확은 **"같은 양극인데 상대극 때문에 용량이 줄어 보인다"** 였다 —
2전극 셀에서 **완전지 전압**에 컷오프를 걸면, 음극 `E_CE` 가 방전 말에 0.62 → ≈1.0 V 로
오르면서 양극이 **3.0 V 대신 ≈3.4 V 에서 멈춘다**.

★★★★ **18호는 컷오프를 작업전극 전위에 건다**: `[인쇄]` "The **cutoff potential of the
working electrode** was set at 0.85–2.65 V". ⇒ **상대극 전위가 무엇을 하든 양극은 항상
같은 전위 구간을 돈다.** 게다가 `[도표]` Fig. 1(b)(d) 가 **상대극이 실제로 평탄함을 보인다.**

⇒ **`[인쇄]` "the amount of effective active material decreased only in the LPSI system" 은
17호가 지적한 오염원이 제거된 상태의 진술**이다. **이 계보에서 양극 활물질 손실을
상대극 오염 없이 말한 첫 문장**이다. ⚠ **값은 없다**(G16) — 그래서 반 칸이다.

## (나) Q5 — 두 편은 모순이 아니라 **같은 축의 반대편 끝**이다

| | **17호 (Yanev)** | **18호 (이 편)** |
|---|---|---|
| Li-In 의 역할 | **상대극**(그리고 기준극은 Li 금속) | **상대극**(기준극은 R-LTO) |
| 조성 `x_Li` | `[인쇄]` 40 at%(3전극 셀) | `[재현]` **37.7 → 40.0 at%** |
| Li 재고 / 이동 전하 | `[재현]` ≈5 배(foil) | `[재현]` **9.5 배(LPSI) / 6.7 배(LPSCl)** |
| 0.1 C 전류밀도 | `[재현]` **0.28 mA cm⁻²** | `[재현]` **0.054 mA cm⁻²** (1/5) |
| 최대 전류밀도 | `[인쇄]` CA 초기 ≈16 mA cm⁻² | **0.54 mA cm⁻²**(1.0 C) — **1/30** |
| 관측된 `E_CE` | `[인쇄]` 0.61 → **1.35 V** (foil, CA) | `[도표]` **≈0.60 V 평탄, 전 구간** |

★★★ `[해석]` **두 편을 겹치면 Q5 의 경계 조건이 처음으로 윤곽을 갖는다**:
**Li-In 상대극은 (ㄱ) 조성이 2 상역 안에 있고 (ㄴ) Li 재고가 이동 전하의 한 자릿수
이상이며 (ㄷ) 전류밀도가 0.1 mA cm⁻² 이하일 때 평탄하다.** 18호는 **세 조건을 전부
만족하는 표본**이고 17호의 foil/CA 는 **(ㄴ)(ㄷ)을 깬 표본**이다.
⚠ **이것은 두 편을 가로지르는 정리이지 어느 편의 결론도 아니다** — 셋 중 무엇이
지배적인지 가른 실험은 **아직 0 편**이다.

## (다) 그러나 기준 축의 가정은 **옮겨갔을 뿐 사라지지 않았다**

18호는 Li-In 을 측정 대상으로 내리는 대신 **R-LTO 의 1.55 V 를 가정**한다(G4).
- 계보: **4호(Shi)** = In 오프셋 **0.6 V 고정 가정** → **16호** = μ-RE 를 넣고 **안정성 미측정**
  → **17호** = Li 금속 RE 로 **`E_CE` 를 실측**(단 RE 자체는 미검증) →
  **18호** = **제 3 물질(R-LTO) 기준극 + 그 전위의 문헌 가정**.
- ★ 18호의 가정이 **덜 위험한 이유**: R-LTO 는 **Li₇Ti₅O₁₂/Li₄Ti₅O₁₂ 2상 평탄**이고
  기준극에 **전류가 흐르지 않는다**(3전극 전위 측정). Li-In 기준극이 위험한 이유(상대극
  역할을 겸하며 리튬화도가 변한다)가 **구조적으로 제거된다.**
- ⚠ 18호의 가정이 **여전히 위험한 이유**: ① 값 검증 0, ② `[인쇄]` 1.55 V 인데
  16호가 인용한 Zhang 2025 의 LTO-RE 는 `[인쇄]` **1.57 V**, ③ 안정성 근거가
  **K–K 잔차**라는 범주 오류(G5), ④ **`R-LTO`(부분환원)는 화학량론이 불명확**하다.
⇒ **[[assb-li-in-reference-potential-window]] 에 "기준을 Li-In 에서 빼는 길" 이라는 항이
하나 생긴다** — 그리고 **그 길에도 자기 가정이 따라붙는다.**

# 이 digest 가 주장하지 않는 것

- **논문의 결론(R3 증가가 주 원인, R4 는 2차 입자 내부)이 틀렸다고 주장하지 않는다.**
  비판은 **교락(G3)·산포(G1·D17)·배정 근거(D1·D8)·λ 선택(G10)** 에 있다.
- **검사 B 의 분해(LPSI = 면적 2.7 배 감소 + 동역학 2.4 배)를 측정값으로 쓰지 않는다.**
  그것은 **로그 막대에서 읽은 두 수의 비**이고, `p` 미공개(G8)·`C∝θ` 가정·n=1 위에 있다.
  주장하는 것은 **"같은 지면의 두 열을 곱하면 저자가 남긴 'or' 가 갈린다"** 까지다.
- **"활성 접촉이 입자 표면의 2 %" 를 수치로 인용하지 않는다** — 비용량 10 µF cm⁻² 는
  우리 가정이고 `C_eff` 자체가 온도에 따라 4.4 배 흔들린다.
- **LPSI ↔ LPSCl 의 차이를 전해질의 성질로 옮기지 않는다** — **복합양극 조성이 다르다**(G3).
- **이 편의 열화 값을 다른 셀로 옮기지 않는다** — **3.7–5.2 mg cm⁻²** 의 초박형 전극,
  **0.54 mA cm⁻²**, **333 K, 50 사이클**, **운전 압력 미상**이다.
- **압력에 대해 아무것도 주장하지 않는다** — 이 논문에 압력이 없다.
- **Q4 는 0/18 이다.** 저자들이 갈림을 **인쇄했다**는 것이 갈랐다는 뜻은 아니다.
- 수치는 전부 **사본**이다. 정본은 원문 PDF 이고, `[도표]` 에는 판독 오차가,
  `[재현]` 에는 명시한 가정이 붙는다.

# 후속 후보

| 순위 | 논문 | 왜 |
|---|---|---|
| ★★★★ **1** | **Ikezawa, Fukunishi, Okajima, Kitamura, Suzuki, Hirayama, Kanno, Arai, *Electrochem. Commun.* 116 (2020) 106743** (ref [27]) | **이 편의 방법 원본이자 R-LTO 기준극의 원전.** Q5 의 새 갈래(기준을 Li-In 에서 빼는 길)가 검증되려면 **1.55 V 의 근거와 안정성 데이터가 거기 있어야 한다**. 그리고 `[인쇄]` "Li-In 상대극의 영향이 유의하다" 는 이 계보의 **3전극 필요성 원전**이다. ⚠ 17호 digest 의 후속 후보 4 순위와 같은 편이고 **큐에 없다** — 세 편(16·17·18호)이 전부 이것을 가리킨다 |
| ★★★ **2** | **Illig, Ender, Chrobak, Schmidt, Klotz, Ivers-Tiffée, *JES* 159 (2012) A952** (ref [29]) | 제목이 곧 우리 물음이다 — "**Separation of charge transfer and contact resistance** in LiFePO₄-cathodes by impedance modeling". **액체셀이지만 분리 절차의 원전**이고, 18호는 이것을 **DRT 참고문헌으로만** 쓴다 |
| ★★★ **3** | **Koerver, …, Zeier, Janek, *Chem. Mater.* 29 (2017) 5574** (ref [23]) | ⚠ **큐 22 번과 같은 편**(Capacity Fade in Solid-State Batteries). 18호는 공간전하층으로만 인용하지만, **NCM\|thiophosphate 의 chemo-mechanical 용량 손실 원전**이고 우리 닻의 중심에 있다. **큐에 이미 있으니 순서만 당기면 된다** |
| ★★ **4** | **Ruess, Schweidler, …, Janek, *JES* 167 (2022) 100532** (ref [19]) | `[인쇄]` "Influence of **NCM particle cracking** on kinetics … with **liquid or solid** electrolyte" — **18호의 `R4` 귀속(입자 내부 균열 → 저항)의 원전**이고, **같은 균열이 액체/고체에서 다르게 보이는지**를 직접 다룬다 |
| ★★ **5** | **Schönleber, Klotz, Ivers-Tiffée, *Electrochim. Acta* 131 (2014) 20** (ref [30]) | **Lin-KK 의 원전.** D7(잔차가 무차원 0.4 인지 0.4 % 인지)을 푸는 유일한 길이고, 우리 [[drt-peak-count-nonidentifiability]] 체크리스트 **C2** 의 정본이다 |
| ★ **6** | **Deng, Wang, Chu, Luo, Ong, *JES* 163 (2016) A67** (ref [42]) | LPSI/LPSCl 의 **Young 계수 22.1 / 30 의 출처**(제일원리). G11(단위 없음 · 계산값 ↔ glass-ceramic)을 푸는 자리이고, 우리 Q6(압력)·DEM 갈래와 직접 닿는다 |

⚠ **큐 대조**: 위 1·2·4·5·6 은 **큐에 없다**. 3 은 **큐 22 번**이다.

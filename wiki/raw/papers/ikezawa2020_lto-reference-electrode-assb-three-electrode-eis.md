---
title: "Ikezawa, Fukunishi, Okajima, Kitamura, Suzuki, Hirayama, Kanno, Arai 2020 — Performance of Li4Ti5O12-based reference electrode for the electrochemical analysis of all-solid-state lithium-ion batteries (Electrochem. Commun. 116, 106743)"
source_url: local-upload/2._Performance_of_Li4Ti5O12-based_reference_electrode_for_the_electrochemical_analysis_of_all-solid-state_lithium-ion_batteries.pdf
source_url_note: "본문 5 쪽(짧은 통신, 참고문헌 29 편), 그림 3 장, 표 0, SI 없음. 크로퍼가 3 장(Fig. 1-3)을 잡았고 3 장 다 봤다 — 판정 수치는 화소 좌표 판독(Fig. 1c·1d·2a·2d·3b·3d). 원자료는 커밋하지 않는다. 16·17·18·19·21호가 지목한 R-LTO 기준극 원전."
source_doi: 10.1016/j.elecom.2020.106743
source_license: "CC BY 4.0 (지면 표기 'open access article under the CC BY license')"
pdf_sha256: abb22ae2bdd51d79286315e0c4e72f51a2920c150aeba05a89f1cd9065ab6e80
ingested: 2026-09-23
sha256: 182057355a5b3762a7f6357da86007a872c29f4def24273fe7682e7a5eb0e514
---

# 수집 목적

`assb` 섹션 **40호**. 큐 **41번** — 2차 묶음(큐 40~59, 원장 §1 상단 순서)의 **둘째 편** (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g).
닻은 `questions/assb-contact-loss-vs-lampe.md`. 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md` §1) ★★★★ · **지목 5 회**(16 · 17 · 18 · 19 · 21호) —
"R-LTO 기준극의 원전. 18호의 'Assuming 1.55 V', 19호의 기준극 쌍 ±30 mV 의 근거, 21호가 InLi-(In) 조립의 예로 인용, **두 Q5 가지(R-LTO · In)가 만나는 자리**".
이 편에 걸린 물음은 하나로 모인다: **이 원전이 R-LTO 기준 전위의 안정성 · 누설 · 드리프트를 실제로 쟀는가.**

Atsunori **Ikezawa**(교신), Goro Fukunishi, Takeyoshi Okajima, Fusao Kitamura, Kota Suzuki, Masaaki Hirayama, Ryoji Kanno, Hajime Arai —
**"Performance of Li₄Ti₅O₁₂-based reference electrode for the electrochemical analysis of all-solid-state lithium-ion batteries"**,
*Electrochemistry Communications* **116** (2020) 106743, doi `10.1016/j.elecom.2020.106743`.
`[인쇄]` 접수 2020-03-18 · 수정 2020-05-08 · 수리 2020-05-08 · 온라인 2020-05-11. **CC BY 4.0**(Elsevier OA).
소속: Tokyo Institute of Technology, School of Materials and Chemical Technology (전원). 자금: NEDO **SOLiD-EV** 프로젝트(18호와 같은 사업).
본문 **5 쪽**(짧은 통신, 참고문헌 29 편), 그림 3 장, 표 0, **SI 없음**. PDF sha256 은 frontmatter `pdf_sha256`. 원자료는 커밋하지 않는다.

> ⚠ **표기**: `[인쇄]` = 지면에 문자 그대로 있는 것 · `[도표]` = 그림을 열어 읽은 값(figure-read ≈; 이 편은 **화소 좌표 판독**, 축 틀 기준 보정 — Fig. 1d 는 1 화소 ≈0.76 mV) ·
> `[재현]` = 지면의 수치로 이 위키가 다시 계산한 것 · `[해석]`/`[추론]` = 이 위키의 해석. 표시가 없는 서술은 원문이 실제로 말한 것이다.

---

# 판정 (먼저)

> ★★★★ **Q5 — 이 원전은 R-LTO 전위의 안정성 · 누설 · 드리프트를 재지 않았다.** 한 것은 **문헌 증인 두 명과의 일치 검사**다.
>
> **(a) 1.55 V 는 측정이 아니라 수입이다.** `[인쇄]` "With reported redox potential of Li₇Ti₅O₁₂|Li₄Ti₅O₁₂ (**1.55 V vs. Li|Li⁺**) **[11]**, these potentials can be calculated to be 3.90 and −0.60 V vs. Li|Li⁺, which are **coincident with reported values [5,17]**. This result clearly shows that the R-LTO electrode successfully worked as a Li₇Ti₅O₁₂|Li₄Ti₅O₁₂ reference electrode."
> ref [11] = **Costard, Ender, Weiss, Ivers-Tiffée, *J. Electrochem. Soc.* 164 (2017) A80 — 액체셀 3전극 논문**(미열람). 셀 안에 Li 금속이 없다 — `[인쇄]` "lithium metal is not stable in most of the sulfide-base solid electrolytes, including Li₁₀GeP₂S₁₂ [7]" 가 **Li 대비 교정을 설계상 막는 이유**로 서론에 있다.
> ⇒ **이 편의 "검증" = (가정한 1.55 V 로 환산한 두 평탄) ≈ (문헌값 두 개)** — 18호 digest 가 원전 없이 추정했던 처방 **P6 의 "인용 + 순환 논증" 구조가 원전에서 그대로 확인된다.**
>
> **(b) 누설 — 0.** `leak` **0 회**, 기준극 전류 · 입력 임피던스 · 재고 예산 **인쇄 0**. ⇒ 계보의 **누설 직접 측정은 0/40 그대로**.
>
> **(c) 드리프트 — 명시 측정 0.** `drift` **0 회** · `stab*` 3 회는 전부 **기대 서술**(서론: "These features **can contribute to** good stability and reproducibility of the reference electrode potential") 또는 **다른 재료의 성질**(Li 금속 불안정 · LTO 가 황화물에 안정). 시간 축 전위 기록 · 개방회로 반복 · 셀 간 산포 **0**.
> `[재현]` **암묵적 상한은 있다**: Fig. 1d 의 Li-In 대 R-LTO 충·방전 평탄 중점이 0.1 · 0.2 · 0.5 · 1 C 에서 **−0.9545 / −0.9524 / −0.9530 / −0.9515 V**(`[도표]` 화소 판독) — **≈3 mV 안**, 2 C 에서만 −0.9452(+9 mV). ⚠ 이것은 **(R-LTO − Li-In) 차**의 안정이라 두 전극의 표류를 **공통 모드로 가르지 못하고**(20호 ⑤), 측정 순서 · 휴지 · 총 시간이 미인쇄다(순서대로라면 `[재현]` 충·방전 시간만 ≈31 h).
> ⇒ **원장 구조적 공백 3("기준극 누설 · 드리프트를 잰 ASSB 3전극 논문")을 채우지 않는다.**
>
> **(d) 19호의 "ca. ±30 mV" 의 근거도 여기 없다.** `30 mV` **0 회** · `reproducib*` 1 회(위 기대 서술) · `mV` 1 회(EIS 진폭 10 mV). 19호 digest 가 "ref [18] 에 있어야 한다" 고 남긴 사슬이 **원전에서 빈 채로 끝난다.**
>
> ★★★★ **두 Q5 가지는 여기서 만난다 — 세 겹으로, 그리고 서로를 증언한다.**
> ① **인용**: 서론 "few examples in which three-electrode cells were applied to ASS-LIB systems **[5,6]**" — [5] = **Nam 2018 *JMCA***(큐 42), [6] = **Chang … Lim, *Ionics* (2019)** = **우리 20호**(In 가지의 매립 In 기준극). ⇒ 20호 digest 의 "R-LTO 가지와 In 가지는 뿌리가 둘" 은 **R-LTO 원전이 In 가지의 두 뿌리를 인용한다**로 고쳐 읽는다 — 두 가지는 독립이 아니다.
> ② **기각**: `[인쇄]` "The mechanical strength of the reference electrode was also important … since relatively high pressures are applied … From these points of view, **lithium metal and Li-In alloy seem not suitable**." — R-LTO 가지는 **In 가지를 기준극 재료로 기각하면서** 태어났다(근거는 기계 강도 서술뿐, 데이터 0).
> ③ **한 셀**: Li-In 은 **상대극**으로 남고, 그 평탄(`[인쇄]` "around −0.95 V vs. R-LTO")이 R-LTO 를 검증하는 **증인 둘 중 하나**다(ref [5] Nam 2018 의 Li-In 값).
> ⇒ `[해석]` **Q5 열여섯 번째 형태 — "상호 증언"**: 한 가지의 **가정값**(Li-In ≈0.6 V)이 다른 가지의 **검증 증인**이 되고, 그렇게 "검증된" 기준(R-LTO 1.55 V)이 뒤에 오는 편(18호)에서 다시 Li-In 을 ≈0.6 V 로 **보고**한다. 측정된 것은 **두 전극의 전위 차 하나**뿐이다(21호 ③ 의 "측정된 것은 둘의 차 0.31 V 하나" 와 같은 모양, 여기가 더 이르다).
>
> **(e) 그 증언의 분해능.** `[재현]` 증인이 0.62 V(Santhosha — 21호 `[인쇄]` 값)라면 Fig. 1d 의 0.1 C 중점 −0.9545 V 는 R-LTO = **1.5745 V** 를 뜻한다 — 16호가 인용한 **Zhang 의 LTO-RE 1.57 V** 와 같고, 이 편의 1.55 V 와 **≈25 mV** 다르다. 인쇄된 두 평탄이 "around 2.35 / −0.95"(소수 둘째 자리)이므로 **이 검증은 1.55 와 1.57 을 가르지 못한다.** 17호의 열역학 평탄 폭 ①(±10 mV)보다 두 배 이상 굵다.
>
> **(f) 부호 오기.** `[인쇄]` "these potentials can be calculated to be 3.90 and **−0.60** V vs. Li|Li⁺" ↔ `[도표]` Fig. 1d 오른쪽 축("Potential / V vs. Li/Li⁺")은 평탄을 **+0.60 V** 에 둔다. −0.95 + 1.55 = **+0.60** — 지면의 음부호는 오기다(D1).
>
> **채움표 — ≈17.5 → ≈17.5 (움직이지 않음).** Q5 는 **반 칸 검토 후 접는다**: 원전의 "검증" 이 문헌 증인 일치이고(Li 대비 0 · 시간 0 · 누설 0 · 산포 0), 새 측정 층이 아니라 **이미 P6 가 예상한 순환의 원전 확인**이다. Q2 도 검토 후 접는다(아래 Q2). Q1 · Q4 · Q6 · Q8 이동 없음, Q7 해당 없음.
>
> ★★★ **Q4 — 0/40, 서른두 번째 성질 "통과가 보장된 검사로 분리를 검증했다"**: 전극 분해의 근거가 (i) **2전극 임피던스 = 양 전극 임피던스 합**(키르히호프 항등 — 기준극 위치 artifact 는 합을 보존하며 임피던스를 **재분배**한다) 과 (ii) **문헌값 두 개와의 일치**(오프셋 하나를 두 증인에 맞춤 — 증인이 같은 쪽으로 틀리면 통과). 둘 다 **틀린 분해 · 틀린 오프셋에서도 통과한다.** 이 계보의 기준극 검증 범주 오류(18호 K–K · 19호 진폭 · 20호 · 21호 키르히호프)의 **R-LTO 가지 원형**이 여기 있다.
>
> ★★★ **같은 지면의 R3 가 세 값이다.** 명목상 같은 상태(LCO, 만충/0.1 C 충전 뒤, 298 K)의 전하이동 저항이 `[도표]` **30.6 Ω**(Fig. 2d) · **37.7 Ω**(Fig. 3b, SOC 100 %) · **45.5 Ω**(Fig. 3d, 298 K 점 — `[재현]` ln R⁻¹ = −3.817) — **×1.49**. Nyquist 호 끝도 ≈50 · ≈65 · ≈70 Ω 로 달라 **회로 선택 차가 아니라 스펙트럼 자체가 다르다.** 설명 0(셀 · 시점 · 순서 미기재). ⇒ **SOC 의존성(25 → 100 %: 40.5 → 37.7, −7 %)은 이 미설명 산포보다 작다** — R3 = 전하이동 귀속의 SOC 축 근거가 약해진다(D3). Ea 축(37 kJ mol⁻¹)은 한 셀 안의 3 온도라 영향이 작다.

---

# 0. 원문에 없어서 확인이 필요한 것

| # | 공백 | 왜 중요한가 |
|---|---|---|
| G1 | **R-LTO 전위를 Li 대비로 잰 값 0** — 셀 안(Li 금속이 LGPS 에 불안정)도, 별도 교정 셀도 없다 | 1.55 V 가 전부 ref [11](액체셀) 수입. P6 미충족 |
| G2 | **기준극 누설 전류 · 계측기 입력 임피던스 · 기준극 재고** 인쇄 0 | 누설 공백(0/40) · 조건 (5′) |
| G3 | **시간 축 안정성 0** — 개방회로 반복 · 장시간 기록 · 사이클 전후 대조 0 | 드리프트 공백 |
| G4 | **셀 수(n) · 셀 간 산포 0** — `n =` 0 회, 오차 막대는 Ea 의 ± 두 개뿐 | 19호 ±30 mV 의 근거가 여기 없는 이유 |
| G5 | **측정 순서 · 휴지 · Fig. 1/2/3 이 같은 셀인가** 미기재 | R3 세 값(D3)을 설명 못 함 |
| G6 | **210 MPa 가 제조 압력인가 운전 중 유지 압력인가** — `[인쇄]` "pressed between chrome-plated SUS pins at 210 MPa" 하나뿐 | Q6 · 21호의 "3배 제조 압력" 비교 |
| G7 | **Li 박 · In 박의 지름** 미인쇄(두께만 0.1 mm 씩) | Li-In 조성 판정 — 같은 φ10 mm 면 `[재현]` **≈55 at% Li**(2상역 밖) |
| G8 | **R-LTO 메시의 셀 안 면적** · 코팅이 개구를 막는가 | 전류 경로 방해 · 재고 예산 |
| G9 | **2전극 EIS 와 3전극 EIS 를 같은 측정에서 얻었나** (VSP-300 은 두 전극 전위를 동시에 잰다고만 인쇄) | 합 검사가 항등인지 정상성 검사인지 |
| G10 | **충방전 · Fig. 2 측정 온도** 미기재(항온조 사용만 인쇄) | Fig. 3d 298 K 점과의 대조 |
| G11 | LCO 입도 · BET · 복합체 두께 · LGPS 밀도 | `C` 의 면적 정규화 · 분리막 두께 |

---

# 1. 서지 · 낱말 지문

| | |
|---|---|
| 종류 | 짧은 통신(*Electrochem. Commun.*), 실험, 신품만(열화 0) |
| 쪽 | 5 (본문 4 + 참고문헌) · 그림 3 · 표 0 · SI 없음 |
| 셀 | **LiNbO₃ 코팅 LiCoO₂ + LGPS 복합양극 \| LGPS \| R-LTO 메시 \| LGPS \| Li-In**, φ10 mm PET 관, 210 MPa |
| 기준극 | **화학 환원 Li₄Ti₅O₁₂(R-LTO) + PVDF, Ni 메시에 딥코팅**, SE · 도전재 없음, Ni 선을 PET 관 핀홀로 인출 |

**★ 낱말 지문** (규칙: NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문(참고문헌 전); SI 없음):

| `identifiab` | `uncertaint` | `conf.interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM` | `degradation mode` | `contact loss` | `MPa` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **0** | **0** | **0** | 0 | 0 | **0** | 0 | 0 | 0 | **0** | **1** |

NFKC 변경 **0 자**(합자 · 전각 없음) · 소프트 하이픈 0 · 줄끝 하이픈 47 곳 — 이으면 `reference electrode` 22 → 24, **지문 열 변화 0**.
**Q5 보조 열**: `leak` **0** · `drift` **0** · `assum*`/`Assum*` **0** · `stab*` 3(전부 기대 · 타 재료) · `reproducib*` 1(기대) · `1.55` 1 · `1.57` 0 · `30 mV` 0 · `mV` 1(AC 10 mV) · `polariz*` 1 · `overpotential` 2 · `artifact` 3 · `Kramers` 0 · `degrad*` 0 · `aging` 0 · `contact` 2(입자 간 접촉 서론 · 기준극 전기 접속) · `time` 2("first time" · "time constants").
`[해석]` **`assum*` 0 회인데 가정이 있다** — 가정이 "With **reported** redox potential … can be **calculated**" 로 적힌다. 21호의 "calculated/converted based on" 과 같은 낱말 부류(P11 지문 확장 대상).

---

# 2. 셀 · 실험 (`[인쇄]`, 괄호 안 `[재현]`)

- **R-LTO 합성**: Li 금속 6 mmol + 나프탈렌 6 mmol, THF 30 cm³, 1 일 교반 → 리튬 나프탈레나이드. 시판 Li₄Ti₅O₁₂ 3 mmol 투입 1 h → "the mixture of **2 mmol Li₇Ti₅O₁₂ and 1 mmol Li₄Ti₅O₁₂**"(청색 분말, XRD 로 불순물 없음 확인 — XRD 그림은 지면에 없다). 방법 원전 ref [15] Tabuchi 2006. (조성 67 : 33 mol% — 19호 `[인쇄]` 와 같다.)
- **기준극**: R-LTO : PVDF = 6.4 : 1 (wt), NMP, 마노 유발 → Ni 메시(3Ni7-3/0, Taiyo Wire Cloth, 개구율 90–91 %, 두께 0.08 mm)를 슬러리에 담갔다 올려 353 K 건조. 적재 ≈**35 mg cm⁻²**. `[인쇄]` "To ensure the wide application to ASS-LIB systems, we did not use any solid electrolytes and conductive materials in the R-LTO reference electrode."
  (`[재현]` 메시 1 cm² 당 R-LTO 30.3 mg · 이론 175 mAh g⁻¹ · 2/3 환원 ⇒ **탈리튬 가능 ≈3.4 mAh · 리튬화 가능 ≈1.7 mAh**. 메시가 1 mm² 만 들어가도 **17–34 µAh** — 21호 GWRE 3 µAh 의 5–10 배, 20호 매립 In 20 µAh 와 같거나 크다. ⚠ 셀 안 면적 미인쇄 G8.)
- **배치**: 메시형 기준극을 **양극과 음극 사이 LGPS 층 안**에 둔다 — `[인쇄]` "to weaken the artifacts in the EIS data [10,11] though this configuration has the disadvantages of difficulty in the application to the cells with thin solid electrolyte layers and possibility of hindering ion current." LGPS 질량 **양극 쪽 50 mg · Li-In 쪽 160 mg**(비대칭).
  (`[재현]` LGPS 밀도 ≈2.0 g cm⁻³ 가정 시 ≈0.32 mm · ≈1.0 mm — 기준극은 양극에서 전체 분리막의 ≈24 % 지점.)
- **양극**: LiNbO₃ 코팅 LiCoO₂(시판) **4.2 mg** + LGPS **1.8 mg**(70 : 30 wt). 율 기준 137 mAh g⁻¹.
  (`[재현]` 0.575 mAh · 0.733 mAh cm⁻² · 1 C = 0.733 mA cm⁻² · C/2 = **0.366 mA cm⁻²** — 21호 `[인쇄]` "0.37 mA cm⁻² (corresponding to their C/2 cycle)" ✓.)
- **음극**: Li 박(0.1 mm) + In 박(0.1 mm) 냉간 압착. `[도표]` Fig. 1a 적층도: 위에서 Cu 메시 · **Li film · In film** · LGPS — **In 박이 분리막 쪽**(= 21호 분류의 InLi-(In) 조립; 본문은 방향을 적지 않는다).
  (`[재현]` 두 박이 φ10 mm 로 같다면 Li 0.604 mmol · In 0.500 mmol ⇒ **x_Li ≈ 54.7 at%**, Li 재고 16.2 mAh = 셀의 **×28**. ⚠ 지름 미인쇄 G7 — 모식도는 같은 크기로 그린다.)
- **셀**: PET 관 φ10 mm, 크롬 도금 SUS 핀 사이 **210 MPa** 압착(Fig. 1a). 양극 쪽 Al 메시 + Al 박, 음극 쪽 Cu 메시.
- **계측**: VSP-300(BioLogic) — `[인쇄]` "which can measure potential of both the positive and the negative electrodes". 컷오프 **셀 전압 1.9–3.6 V**. EIS 10 mV · **7 MHz–10 mHz** · 개방회로. Ar 글러브박스 조립, Ar 밀폐 용기 · 항온조(SH-222, Espec).

---

# 3. 절별 해체

## 3.1 서론 (p1–2)

- ASSB 에서 3전극 선례가 적다 — `[인쇄]` "there are few examples in which three-electrode cells were applied to ASS-LIB systems **[5,6]**. In addition, **electrochemical impedance spectroscopy (EIS) with a three-electrode cell has never successfully performed in ASS-LIB systems.**"
  ([6] = 20호 Chang — EIS 가 없는 3전극이라 이 "최초" 주장과 양립한다. 16호 표의 "Ikezawa 2020 (최초)" 도 이 인쇄에서 온다.)
- 기준극 재료 선택 제약 둘: Li 금속은 대부분의 황화물(LGPS 포함 [7])에 불안정 · 높은 압력 때문에 기계 강도가 필요 ⇒ "lithium metal and Li-In alloy seem not suitable". **Li-In 을 기각하는 이유는 기계 강도 서술뿐**(데이터 · 인용 0).
- 형상 · 위치: `[인쇄]` "Inappropriate shapes and positions of reference electrodes are known to cause artifacts in impedance spectra [8–11]."
- LTO 선택 이유: `[인쇄]` "Li₄Ti₅O₁₂ was known to be stable in many sulfide-base solid electrolytes **[3,4,6]** and show quite flat charge–discharge potential profiles [12]. These features **can contribute to** good stability and reproducibility of the reference electrode potential. In fact, Li₄Ti₅O₁₂ electrodes that are electrochemically-reduced … are known as reliable reference electrodes for **liquid** LIB systems [13,14]."
  ⚠ **[6](20호 Chang)은 LTO 를 쓰지 않는다** — 20호 셀은 Li₂S–P₂S₅ 유리 · Li₄.₄Si · TiS₂ · In 기준극이고 원문 검색 `Ti5` **0 회**(D2). **안정성의 근거는 전부 기대이고, 액체셀 근거는 [13,14]다.**

## 3.2 충방전 — Fig. 1(b)–(d)

- `[인쇄]` "Charge-discharge profiles of the LiCoO₂ electrode (Fig. 1(c)) and the Li-In electrode (Fig. 1(d)) showed plateaus at **around 2.35 and −0.95 V vs. R-LTO**" → 1.55 V [11] 로 환산해 3.90 · "−0.60" V vs Li → 문헌 [5,17] 과 일치 ⇒ 기준극이 작동했다.
- `[도표]` Fig. 1c · 1d 는 **왼쪽 축 vs R-LTO · 오른쪽 축 vs Li/Li⁺** 두 축이다(오른쪽 = 왼쪽 + 1.55). **측정 축이 같이 인쇄된다** — 21호 Fig. 6 · 8(환산 축만)과 달리 P11 의 "측정 축 병기" 는 만족.
- `[도표]` **Li-In 평탄(화소 판독, 용량 10–30 mAh g⁻¹ 구간)**:

| 율 | 충전(Li-In 리튬화) | 방전(탈리튬) | 중점 | 폭(충–방) |
|---|---:|---:|---:|---:|
| 0.1 C | −0.9585 | −0.9505 | **−0.9545** | 8.0 mV |
| 0.2 C | −0.9638 | −0.9410 | −0.9524 | 22.8 mV |
| 0.5 C | −0.9744 | −0.9316 | −0.9530 | **42.8 mV** |
| 1 C | −0.9877 | −0.9153 | −0.9515 | 72.4 mV |
| 2 C | −1.0116 | −0.8788 | −0.9452 | 132.8 mV |

  (V vs R-LTO. 판독 분해능 ≈±1 mV.)
- `[인쇄]` "At higher discharge rates than 1C, Li-In shows **relatively large overpotential at the end of the discharges**, in agreement with a previous report [5]." `[도표]` 1 C · 2 C 방전 끝에서 Li-In 이 **≈+10–15 mV 위로 꺾인다**. 2 C 방전 용량(`[도표]` ≈25–30 mAh g⁻¹)의 끝은 **LCO 전위의 붕괴**(Fig. 1c, 2.3 → 2.1 V)가 정한다 — Li-In 은 ≈−0.88 에 머문다.
  ⇒ ⚠ 17호 digest 표의 요약 "**1 C 이상에서 Li-In 이 병목**" 은 이 인쇄보다 세다(원문은 "끝에서 비교적 큰 과전압"). 용량을 끊는 것은 이 그림에서 LCO 다(§8 원전 대조 표).
- `[인쇄]` "the monotonous increase in the LiCoO₂ potential at the early state of charge (ca. 0–5 mAh g⁻¹) was **not correctly captured in the cell voltage** at higher rate than 1C due to the relatively steep decrease in the Li-In overpotential, which shows the limitation of the conventional two-electrode cell with the Li-In negative electrode". `[도표]` 2 C 충전: Li-In 이 −1.035 → −1.01 V 로 풀리는 동안 셀 전압은 3.47 → 3.46 V 로 **내려간다**(Fig. 1b) — 양극은 오르는데 셀은 내려가는 구간. **2전극에서 상대극 분극이 양극 곡선의 모양을 뒤집는 첫 인쇄 사례**(Q5 "왜 중요한가 1" 의 모양 오염, 크기 ≈10–25 mV).
- `[도표]` 0.1 C 충전 ≈125 · 방전 ≈117 mAh g⁻¹(첫 사이클 여부 미기재).

## 3.3 EIS 전극 분해 — Fig. 2

- `[인쇄]` "Good agreement between cell impedance measured with two-electrode configuration and the sum of LiCoO₂ impedance and Li-In impedance measured with the reference electrode showed that the impedances … were **successfully separated**." `[인쇄]` "Some deviation observed above 1 MHz may be derived from the artifact caused by limited conductance of the reference electrode [18]."
  `[추론]` **합의 일치는 분리의 검증이 아니다** — 기준극 위치 artifact(이 편이 인용한 [8–11])는 WE 와 CE 사이에서 임피던스를 **재분배하되 합을 보존**한다. 3전극 두 성분을 한 측정에서 얻었다면 합은 항등이고, 2전극을 따로 쟀다면 이 검사가 보는 것은 **두 측정 사이의 정상성**이다(G9). 21호 digest 가 "범주 오류 네 번째" 로 적은 검사의 **R-LTO 가지 원형**이다.
- `[도표]` **고주파 끝**(화소 판독): LCO 스펙트럼 ≈**12–13 Ω** · Li-In 스펙트럼 ≈**33–35 Ω**(7 MHz 쪽 첫 점, Z″ ≈5) · 합 ≈45–47 ↔ `[도표]` Fig. 2b 결합 임피던스 시작 ≈45 · 셀 ≈51 Ω.
  `[재현]` **LCO : Li-In 옴 몫 ≈1 : 2.7 ↔ LGPS 질량 50 : 160 = 1 : 3.2** — **기준극 위치가 분리막 옴을 질량비 가까이 나눈다.** ⇒ 이 편의 "Li-In 임피던스" 에는 **분리막의 ≈3/4** 이 들어 있다(Q2 · 아래 §5.2).
- `[인쇄]` "The Nyquist plot of the cell impedance shows three semicircles and Warburg impedance … The semicircles observed above 1 kHz were usually identified as … mainly derived from the LiCoO₂ electrode [19–21]. However, **two relatively large semicircles were also observed in the Nyquist plot of the Li-In impedance above 1 kHz.** … the number of semicircles observed in the cell impedance (three) was smaller than that of the sum … (five). This means that the semicircles derived from the LiCoO₂ impedance are **coupled** with those derived from the Li-In impedance probably due to the similar time constants."
- 1 kHz 이상을 R1–(R2‖CPE2)–(R3‖CPE3) 로 Z-view 적합. `[도표]` Fig. 2d(화소 판독): **R2 LCO 7.0 ↔ 셀 18.8 Ω (×2.7) · R3 LCO 30.6 ↔ 셀 51.2 Ω (×1.67)**. `[인쇄]` "Larger values of R2 and R3 in the cell impedance indicated that the LiCoO₂ impedance was **overestimated** with the combination of the conventional two-electrode cells using Li-In negative electrodes and the conventional equivalent circuit disregarding the Li-In impedance above 1 kHz."
  `[재현]` 셀 (R2+R3) − LCO (R2+R3) = 70.0 − 37.6 = **32.4 Ω** ↔ `[도표]` Li-In 스펙트럼의 1 kHz 이상 호 ≈33 → ≈70 Ω(≈37 Ω) — 같은 자릿수 ✓. **2전극 "양극 호" 의 거의 절반이 상대극이다** (신품 LCO|Li-In, 210 MPa).
- CPE 값 · 적합 잔차 · 적합 표 **인쇄 0**. Fig. 2 는 **Ω(면적 정규화 없음)**.

## 3.4 LCO 임피던스 성분 동정 — Fig. 3

- **SOC 의존**(Fig. 3a · b, 회로에 Warburg 추가): `[인쇄]` "The SOC dependence observed in the semicircle at **around 10 kHz** suggested that this semicircle is related to the charge transfer reaction … The semicircle at **around 1 MHz** was independent of SOC". `[도표]` 범례 SOC 0 / 25 / 50 / 75 / 100 % = **3.86 / 3.90 / 3.97 / 4.12 / 4.17 V vs Li/Li⁺**(1.55 V 환산값). `[도표]` Fig. 3b R3 = **48.2 / 40.5 / 37.2 / 36.5 / 37.7 Ω**(화소 판독). 액체계 LCO 의 `R_ct`(SOC) [22–24] 와 모양이 닮았다는 것이 근거.
- **온도 의존**(Fig. 3c · d, SOC 100 %, 298 · 288 · 273 K): `[인쇄]` **Ea(R3) = 37 ± 2 kJ mol⁻¹**(고체계 LCO 30–60 [25,26], 액체 ≈60 [27]) ⇒ "R3 was mainly derived from the charge transfer reaction of the LiCoO₂" · **Ea(R2) = 55 ± 1 kJ mol⁻¹** — LGPS 이온 저항 Ea 24 kJ mol⁻¹ [16] 보다 크고 LCO 전자 저항은 온도에 반대로 움직인다 [29] ⇒ "we could identify R2 as **some interface or interphase resistance** … such as ion transfer resistance between LiNbO₃|Li₁₀GeP₂S₁₂ interface and electron/ion transfer resistance in LiNbO₃ layer. **Further research is needed**".
  `[재현]` Fig. 3d 점 화소 판독 → R2 = 7.1 / 15.9 / 54.4 Ω, R3 = 45.5 / 72.9 / 178.6 Ω(298 / ≈288 / 273 K) · 직선 적합 **Ea 55.4 · 37.2 kJ mol⁻¹** — 인쇄와 일치 ✓. 잔차 ≤0.026(ln 단위, 3 점, 자유도 1).
  `[인쇄]` "The non-optimal fittings observed in Fig. 3(a), (c) and **the deviation from the straight line observed in Fig. 3(d)** may be due to the effect of the ionic transport resistance in the composite electrode … coupled [28]." ⚠ 3 점 · 잔차 ≤0.026 이라 "직선에서 벗어남" 은 판독으로는 보이지 않는다(D6).
- ⚠ **R3 세 값 (D3)**: Fig. 2d 30.6 · Fig. 3b(100 %) 37.7 · Fig. 3d(298 K) 45.5 Ω. Fig. 2 는 Warburg 없는 회로라 30.6 ↔ 37.7 의 일부는 회로 차일 수 있으나, **Fig. 3b ↔ 3d 는 같은 회로 · 같은 SOC · 같은 온도**에서 ×1.21 이고, Nyquist 호 끝이 Fig. 2a ≈50 · Fig. 3a(100 %) ≈65 · Fig. 3c(298 K) ≈70 Ω 로 **스펙트럼이 다르다**.

## 3.5 결론 (p5)

`[인쇄]` "In charge–discharge measurement, the potential of the LiCoO₂ electrode was measured **without the polarization of the Li-In electrode**. In electrochemical impedance spectroscopy, we separated the LiCoO₂ and the Li-In electrode impedances and identified two impedance components … To our best knowledge, this is **the first time** that electrochemical impedance was successfully measured using three-electrode cells in ASS-LIB systems."
안정성 · 재현성 · 수명에 관한 결론 문장 **0**.

---

# 4. ★★★★ Q5 — 계보에서 이 편의 자리

## 4.1 1.55 V 의 수입 경로가 셋이다 (지금까지 읽은 편 기준)

| 편 | 1.55 V 의 근거로 인쇄된 문헌 | 성격 |
|---|---|---|
| 23호 Koerver 2017 | ref 44 **Zaghib 1999** *JPS* 81–82 | 액체 LTO |
| **40호 Ikezawa 2020 (이 편)** | ref [11] **Costard 2017** *JES* 164 A80 | 액체셀 3전극(Ivers-Tiffée 그룹) |
| 18호 Fukunishi 2023 | [32] **Colbow 1989** *JPS* 26 · [33] **Ohzuku 1995** *JES* 142 | 액체 LTO |
| 19호 Yoshida 2024 | — (소거, 1.55 0 회) | — |

`[해석]` **같은 연구실의 원전(40호)과 후속(18호)이 1.55 V 에 다른 문헌을 단다** — 18호는 방법 원전(이 편, 18호 ref [27])을 1.55 V 의 근거로 쓰지 않았다. 이 편이 1.55 V 를 재지 않았으니 일관된 선택이다. ⇒ **읽은 범위에서 1.55 V 가 ASSB 안에서 Li 대비로 측정된 적은 0 번**이고, 매번 다른 액체 원전에서 들어온다. (Costard 2017 · Zaghib 1999 · Colbow 1989 는 미열람 — 그 안에 1.55 V 가 실제로 있는지는 확인 안 됨.)

## 4.2 두 가지가 만나는 방식 — "상호 증언" (열여섯 번째 형태)

계보(개념 페이지 [[assb-li-in-reference-potential-window]]): 안 쟀다(4호) → 설치 · 미검증(16호) → 실측(17호) → 제3물질로 가정(18호) → 차분으로 소거(19호) → 깨지는 모습을 남김(20호) → 교정 이식(21호) → … → 고정 전위가 게이지 영점(38호) → 상대극 계면을 양극 접촉 면적에 흡수(39호) → **상호 증언(40호, 시점으로는 18호보다 앞 — 18호 "제3물질로 가정" 의 원전)**.

- **무엇이 측정되었나**: `E_LCO − E_RLTO` 와 `E_LiIn − E_RLTO` 두 개 — 그러나 둘의 **절대값**을 Li 척도로 붙이는 데는 미지수(R-LTO vs Li) 하나가 더 필요하고, 이 편은 그것을 **문헌 두 값에 동시에 맞춰** 정했다. 자유도 1 에 증인 2 — 과잉결정이므로 **원리적으로는 검사가 된다.** 문제는 분해능: 인쇄 "around" 두 자리, 증인 자체의 산포(Li-In 0.60 ↔ 0.62, 17호 ①, 21호 교정), LCO 평탄의 모양(`[도표]` 0.1 C 충전 2.344 → 2.362 V 로 경사).
- `[재현]` **증인 0.62 V 를 쓰면 R-LTO = 1.5745 V** · 그러면 LCO 0.1 C 평탄 중점(≈2.345)은 ≈3.92 V vs Li — LCO 쪽 증인과도 모순이 없다. **1.55 와 1.575 가 둘 다 이 검사를 통과한다.**
- ⇒ 18호의 "Assuming 1.55 V" 는 이 편에서 **검증된 값이 아니라 25 mV 폭의 증인 합의**를 물려받았다. 17호 ① ±10 mV · 38호 "기준 ±10 mV ≈ 활성 질량 ±4 %" 척도로 보면 **이 원전의 분해능 자체가 38호 SC 신호의 절반 크기를 넘는다**(`[해석]`, 화학 다름).

## 4.3 평탄 조건 (1)–(8) 대조 — 상대극 Li-In

| 조건 | 이 편 | 판정 |
|---|---|---|
| (1) 2상역 안 | `[재현]` 박 지름이 같으면 **≈55 at%** — 17호 "50 at% 에서 깨진다" 밖 | ⚠ **판정 불가**(G7). 관측 평탄 −0.9545 는 0.62 V 증인과 25 mV 차 — **조성 이탈(②, 아래쪽)과 R-LTO 오프셋(1.575)이 같은 방향 · 같은 크기**라 이 셀에서 갈리지 않는다 |
| (2) 분리막 면 LiIn | `[도표]` In 박이 분리막 쪽(InLi-(In)) — 21호에서 **9 초**에 끊긴 조립 | `[해석]` 그런데 이 편은 **먼저 충전**(분리막 면에 전기화학적 LiIn 형성 = 21호 ③-a) → 방전은 넣은 것만 뺀다(21호 98 % 가역). 1 · 2 C 방전 끝 +10–15 mV 꺾임이 그 고갈의 초기 형태와 양립. 210 MPa creep 가능성(21호 `[인쇄]`)도 열려 있다 |
| (3) 저율 | 0.1–2 C | 1 C 이상에서 분극 ≥72 mV(폭) |
| (4) CE–RE 옴 | `[재현]` Li-In 쪽 옴 ≈33–35 Ω — 0.5 C 에서 ≈10 mV | ⚠ 보상 0 — "Li-In 과전압" 의 ≈절반이 분리막 |
| (5) 재고비 | `[재현]` 같은 지름이면 ×28 | ✓ |
| (6) 전류밀도 | 0.1 C = 0.073 mA cm⁻² · 2 C = 1.47 | 0.1 C 만 만족 |
| (5′) 기준극 재고 | `[재현]` 메시 1 mm² 당 17–34 µAh | **설계상 크다**(21호 GWRE 의 5–10 배 이상) — 단 누설 자체는 0 측정 |

---

# 5. `[재현]` 검산

## 5.1 21호가 인용한 "≈40 mV ≈110 Ω cm²" 의 정체

21호(Sedlmeier 2023) `[인쇄]`: "consistent with the study by Ikezawa et al., who for a 3-fold higher fabrication pressure **report** a delithiation overpotential at 0.37 mA cm⁻² (corresponding to their C/2 cycle) of only ∼40 mV, which equates to a much lower areal resistance of ∼110 Ω cm²."

- 이 편은 그런 수를 **인쇄하지 않았다**(`mV` 1 회 = EIS 진폭). 그림에서 읽은 값이다.
- `[도표]` C/2 의 **충·방전 폭 = 42.8 mV**(위 표). 탈리튬만의 과전압은 0.5 C 중점 대비 **21.4 mV**, 0.1 C 중점 대비 **22.9 mV**.
- ⇒ `[재현]` **"≈40 mV" 는 탈리튬 과전압이 아니라 충–방 폭(= 리튬화 + 탈리튬)이다.** 탈리튬만이면 21–23 mV ÷ 0.366 mA cm⁻² = **≈58–63 Ω cm²**. 그중 `[재현]` 분리막 옴 몫(Li-In 쪽 ≈33–35 Ω × 0.785 cm²) **≈26–27 Ω cm²** ⇒ Li-In 전극만 **≈30–35 Ω cm²**.
- 독립 대조(시간 ↔ 주파수): `[도표]` Fig. 2a Li-In 의 1 Hz 실수부 ≈**82.6 Ω** × 0.2877 mA = **23.8 mV** ↔ DC 21.4–22.9 mV ✓(≈10 % 안).
- ⇒ 21호의 비교 방향("Ikezawa 가 훨씬 낮다")은 **더 강하게** 선다(110 → ≈60, 전극만 ≈30–35 Ω cm² ↔ 21호 750). 수치는 ×≈2 과대. 그리고 "3-fold higher **fabrication** pressure" 는 이 편의 "pressed … at 210 MPa" 를 제조 압력으로 읽은 것이다(G6 — 원문은 구분하지 않는다).

## 5.2 분리막 옴의 위치 분할

`[도표]` 고주파 끝 LCO ≈12–13 · Li-In ≈33–35 Ω ⇒ 1 : 2.6–2.9 ↔ LGPS 질량 1 : 3.2. `[재현]` LGPS 밀도 ≈2.0 g cm⁻³(가정)이면 210 mg → ≈1.34 mm, 셀 고주파 ≈45–51 Ω 는 σ ≈3.4–3.8 mS cm⁻¹ 에 해당(분말 압분체로 그럴듯한 자릿수). **메시가 전류를 크게 막는 흔적은 이 자릿수에서 안 보인다**(`[추론]` — 막는 양의 상한은 못 준다).

## 5.3 `C` 자릿수 (1단계 τ 형)

- R3(≈10 kHz): `C₃ = 1/(2π·10⁴·R₃)` = **0.35–0.52 µF**(R3 30.6–45.5 Ω) ⇒ 기하 면적당 **0.45–0.66 µF cm⁻²**.
- R2(≈1 MHz, 7.0–7.1 Ω): `C₂` ≈ **22–23 nF** ⇒ 기하 면적당 **≈0.029 µF cm⁻²**.
- `[추론]` R2 = "LiNbO₃ 층 · LiNbO₃|LGPS 계면" 귀속과 자릿수 긴장: CAM 표면 전체를 덮는 nm 급 산화물 층이면 `ε₀ε_r/d` 가 (실면적 ≥ 기하 면적 위에서) **µF cm⁻² 급**이어야 한다(`ε_r`, `d` 는 이 편에 없다 — 가정). 관측 `C₂` 는 기하 면적당으로도 **두 자릿수 작다.** 그리고 R2 꼭짓점(≈1 MHz)은 **저자 스스로 기준극 artifact 를 의심한 대역**("deviation observed above 1 MHz")의 문턱에 있다. 판별은 못 한다 — Ea 55 kJ mol⁻¹ 은 LGPS 벌크와 다르다는 것까지만 준다.

---

# 6. 우리 축 (Q1–Q8)

| 축 | 이 편 | 판정 |
|---|---|---|
| **Q1** 접촉 정량 | `contact` 2 회(입자 간 접촉을 위한 고압 서론 · 기준극 전기 접속). 양극 `θ`/`φ` 0 | **없다. `θ(N)` 0/40** |
| **Q2** 독립 관측 | 3전극 EIS 전극 분해 + 2전극 대조: `[도표]` 2전극이 LCO R2 ×2.7 · R3 ×1.67 과대 | **이동 없음 — 반 칸 검토 후 접음.** 신품이라 가를 `LAM_PE` 가 없고, 분리의 근거로 쓴 합 검사는 항등(범주 오류). 16호 이후 이미 있는 층. 기여는 **"2전극 양극 호의 ≈절반이 상대극" 의 크기** |
| **Q3** 라벨 층위 | ECM 적합(CPE 값 · 잔차 0) · Ea ± 는 회귀 SE(3 점) · 기준 오프셋 = 문헌 증인 | 층 하나 — **literature-witness offset + sum-identity validation**; 같은 상태 R3 세 값(×1.49, 미설명) |
| **Q4** 유일성 | `identifiab` · `uncertaint` · `calibrat` 0 | **0/40 — 서른두 번째 성질 "통과가 보장된 검사로 분리를 검증했다"** |
| **Q5** 기준 전위 | 1.55 V 수입([11] 액체) · 증인 2 · 누설 0 · 드리프트 0 · ±30 mV 없음 · 부호 오기 | **이동 없음(반 칸 검토 후 접음) — 열여섯 번째 형태 "상호 증언"** |
| **Q6** 압력 | "pressed … at 210 MPa" 한 값, 제조/운전 미구분 | 이동 없음 |
| **Q7** dead Li | Li-In 음극 | 해당 없음 |
| **Q8** 화학 · OCP | LiNbO₃-LCO, SOC 5 점 전위(3.86–4.17 V, 환산) — 개방회로 조건 · 휴지 미기재 | 이동 없음 |

---

# 7. ★★★ 곱 축퇴 처방 — 스물세 번째 적용

LCO(LiNbO₃) | LGPS | Li-In, 신품, 210 MPa, R-LTO 3전극 EIS.

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | CPE 값 인쇄 0 · 꼭짓점 **"around 10 kHz"(R3) · "around 1 MHz"(R2)** 인쇄 + 그림 주파수 표지(1 MHz · 1 kHz · 1 Hz) | ⚠ τ 형만 — `C₃` ≈0.45–0.66 · `C₂` ≈0.03 µF cm⁻²(기하). SOC 축 5 점의 `R3` 는 있으나 `C` 가 없어 **`R·C` 궤적 불가** |
| **2단계** 면적 대조군 | 없음 | ❌ |
| **3단계-a** `Ea` | ✅ R2 · R3 둘 다, 3 온도(298–273 K), SOC 100 %, `[재현]` 55.4 · 37.2 kJ mol⁻¹ | ✅ **재료만** — 노화 전후가 없어 "`Ea` 불변 + `R` 증가" 검사는 못 한다 |
| **3단계-b** `C` 물리 상한 | `C₂` ≈23 nF | ⚠ **R2 = 표면 산화물 층 귀속과 두 자릿수 긴장**(§5.3, 가정 위) |
| **4단계** 시간 영역 | Li-In 쪽 DC(Fig. 1d) ↔ EIS(Fig. 2a) | ✅ **통과** — 0.5 C 탈리튬 21–23 mV ↔ `Z′(1 Hz)·I` ≈24 mV |

**⇒ 이 적용이 처방에 더하는 것 (새 줄 후보 "3전극 옴 몫은 기준극 위치가 정한다")**: 3전극으로 나눈 전극 저항 · 과전압에는 **기준극 위치가 정한 분리막 몫**이 들어 있다 — 이 편에서 LCO : Li-In 고주파 끝 ≈1 : 2.7 ≈ LGPS 질량비 1 : 3.2. `R·C` · `Ea` 는 R1 을 뗀 호에 걸어야 하고(이 편은 뗐다), **DC 과전압 비교(21호가 이 편을 인용한 방식)는 그 몫을 먼저 빼야 한다.** 그리고 **2전극 "양극 호" 에 붙는 상대극 몫의 첫 직접 크기**: 1 kHz 이상 호 합 ×1.86(신품).

**⚠ 이것이 곱을 푼 것은 아니다**: 신품 · 열화 0 · 면적 대조 0 · CPE 미인쇄 · R3 세 값의 미설명 산포(×1.49)가 SOC 효과(−7 %)보다 크다.

---

# 8. 어긋남 (실제로 어긋난 것만)

| # | 어디 | 무엇 |
|---|---|---|
| **D1** | p3 본문 ↔ Fig. 1d 오른쪽 축 | "**−0.60** V vs. Li\|Li⁺" ↔ 축은 **+0.60**. −0.95 + 1.55 = +0.60 — 부호 오기 |
| **D2** | 서론 ref [6] | "Li₄Ti₅O₁₂ was known to be stable in many sulfide-base solid electrolytes [3,4,**6**]" — [6](20호 Chang)은 LTO 를 쓰지 않는다(Li₄.₄Si · TiS₂ · In; 원문 `Ti5` 0 회) |
| **D3** | Fig. 2d ↔ 3b ↔ 3d | 명목상 같은 상태의 R3 = 30.6 / 37.7 / 45.5 Ω(×1.49), Nyquist 호 끝 ≈50 / ≈65 / ≈70 Ω — 설명 0 |
| D4 | Fig. 1a 라벨 | SE 를 "Li₁₀GeP₂**S₅**" 로 적는다(본문 Li₁₀GeP₂S₁₂). Fig. 2b 범례 "LiCO₂" |
| D5 | 참고문헌 | [5] "J. Mat. **Cham.** A" · [25] "Solid State Ion. **276 (2005)**"(권 · 연도 불일치 의심) · [26] "J. Power Sources **15** (2012)"(권 불일치 의심) · [18] 저자명에 소속 첨자가 붙음("Chechirliana, P. Eichnera…"). 서지 확인 안 함 |
| D6 | p5 ↔ Fig. 3d | "the deviation from the straight line observed in Fig. 3(d)" ↔ `[재현]` 3 점 잔차 ≤0.026(ln) — 판독으로 안 보인다 |

**다른 digest 가 이 편에 대해 한 말 — 원전 대조**

| 출처 | 그 편의 말 | 원전 |
|---|---|---|
| 21호 Sedlmeier `[인쇄]` | "report a delithiation overpotential … ∼40 mV … ∼110 Ω cm²" | **인쇄 0**, 그림의 40 mV 는 **충–방 폭**; 탈리튬만 ≈21–23 mV ≈58–63 Ω cm²(§5.1) |
| 21호 Sedlmeier `[인쇄]` | InLi-(In) 조립("In 박을 SE 에, Li 를 뒤에")의 예(ref 18) | `[도표]` ✓ Fig. 1a 적층 순서. 본문은 방향 무기재 |
| 19호 Yoshida | ±30 mV 재현성(근거 없음 — ref [18] 에 있어야) | **없다** |
| 18호 Fukunishi | 1.55 V 는 [32,33] · 방법 원전 [27] = 이 편 | 이 편의 1.55 V 는 [11] — 원전과 후속이 다른 문헌 |
| 17호 digest 요약 | "1 C 이상에서 Li-In 이 병목" | 원문 "relatively large overpotential at the end of the discharges"; 2 C 용량 끝은 LCO 붕괴 |
| 16호 Ramanayagam 표 | "Ikezawa 2020 (최초) … 임피던스 분해 가능" | ✓ 인쇄된 "first time" 주장 |
| 원장 Ikezawa 행 | "3배 압착에서 110 Ω cm²" | 21호의 판독 — 원전에 없음, ×≈2 과대 |

---

# 9. 그림 — 무엇을 봤나

크로퍼가 **3 장**(Fig. 1–3, 이 편의 그림 전부)을 잡았고 **3 장 다 봤다**. 이 편은 판정이 전부 그림 판독에 걸려 있어 **화소 좌표 판독**을 따로 했다 — Fig. 1c · 1d(충방전 평탄) · 2a(고주파 끝 · 1 Hz 실수부) · 2d(막대) · 3b(R3–SOC) · 3d(Arrhenius 점 · Ea 재적합).

| 그림 | 본 것 | 본문과 어긋남 |
|---|---|---|
| Fig. 1 (a) 모식도 · 사진 (b)–(d) 충방전 | 적층 순서(In 박이 SE 쪽) · 메시 사진(개구 열림) · 두 축(vs R-LTO / vs Li) · Li-In 평탄 5 율 | **D1**(부호) · D4(라벨) |
| Fig. 2 (a)–(d) Nyquist · 적합 · R2/R3 막대 | 고주파 끝 분할 · 1 MHz 이상 편차 · R2/R3 비 | D3 의 첫 값(30.6) |
| Fig. 3 (a)–(d) SOC · 온도 의존 | 범례 SOC 전위 5 점 · R3(SOC) · Arrhenius 3 점 | **D3** · D6 |

안 본 것: 없다(XRD 는 "confirmed" 로만 서술되고 그림이 지면에 없다).

---

# 10. 참고문헌 중 후속 후보 (29 편 중 — 미열람, 서지는 지면 그대로)

| 서지 | ref | 왜 | 축 |
|---|---|---|---|
| **Nam, Park, Oh, An, Jung, *J. Mater. Chem. A* 6 (2018) 14867** | [5] | In 가지의 뿌리 · 이 편의 Li-In 증인 · "1 C 이상 Li-In 과전압" 선례 — **큐 42** | Q5 |
| **Costard, Ender, Weiss, Ivers-Tiffée, *J. Electrochem. Soc.* 164 (2017) A80** | [11] | ★★★★ **이 편 1.55 V 의 유일한 근거** + 메시형 위치 선택의 근거. 1.55 V 가 거기서 측정인가 인용인가 | Q5 · Q2 |
| Ender, Illig, Ivers-Tiffée, *J. Electrochem. Soc.* 164 (2017) A71 | [10] | 메시형 기준극 위치 artifact 이론 — 합 보존 재분배의 원전 후보 | Q2 |
| Ender, Weber, Ivers-Tiffée, *J. Electrochem. Soc.* 159 (2012) A128 | [9] | 같은 계열 | Q2 |
| Hoshi … Itagaki, *J. Power Sources* 288 (2015) 168 | [8] | 기준극 형상 artifact | Q2 |
| Chechirlian … Mazille, *Electrochim. Acta* 35 (1990) 1125 | [18] | >1 MHz 편차 = 기준극 유한 전도 artifact 의 근거 | Q2 |
| Braun, Uhlmann, Weiss, Weber, Ivers-Tiffée, *J. Power Sources* 393 (2018) 119 | [28] | 복합전극에서 이온 수송 ↔ 전하이동 결합(TLM) — R3 "비최적 적합" 의 설명 | Q2 · 곱 |
| Zhang, Weber, … Zeier, Janek, *ACS Appl. Mater. Interfaces* 9 (2017) 17835 | [19] | "세 반원 + Warburg" 의 선례 — 원장의 Zhang 2017 *ACS AMI*(22호 지목)와 같은 편 | Q1 · Q2 |
| Tabuchi, Yasuda, Yamachi, *J. Power Sources* 162 (2006) 813 | [15] | 화학 환원 방법 원전 | Q5 |
| La Mantia … Cui, *Electrochem. Commun.* 31 (2013) 141 · Ohzuku 1995 *JES* 142 | [13] · [14] | 액체셀 LTO 기준극 신뢰성 | Q5 |

큐 42–59 중 이 편이 인용하는 것: **42 Nam 2018 하나.** (큐 52 Illig 2012 *JES* 159 A952 는 인용하지 않는다 — [10] 은 Ender · Illig 2017 A71 로 다른 논문.)

---

# 11. 이 digest 가 주장하지 않는 것

- **R-LTO 의 전위가 1.55 V 가 아니라고 주장하지 않는다.** 주장은 **"이 원전의 검증이 1.55 와 1.575 를 가르지 못한다"** 까지이고, 1.575 는 증인 0.62 V 를 넣은 우리 계산이다.
- **R-LTO 가 표류하거나 누설한다고 주장하지 않는다.** 재지 않았다는 것이다. 재고 예산이 크다는 것(메시 1 mm² 당 17–34 µAh)은 **설계상 여유**의 `[재현]` 이고, 셀 안 메시 면적은 미인쇄다.
- **≈3 mV 중점 안정을 기준극 드리프트 상한으로 쓰지 않는다** — R-LTO 와 Li-In 의 차이며, 측정 순서 · 시간 미기재다.
- **Li-In 이 55 at% 라고 주장하지 않는다** — 두 박의 지름이 같다는 모식도 가정 위의 계산이다.
- **R2 가 기준극 artifact 라고 주장하지 않는다.** `C` 자릿수가 표면 산화물 층 귀속과 긴장한다는 것(가정 `ε_r`, `d` 위)과, 저자가 artifact 를 의심한 대역에 걸친다는 것까지다.
- **R3 세 값의 원인을 안다고 주장하지 않는다** — 다른 셀 · 다른 시점 · 회로 차 어느 것인지 지면이 말하지 않는다.
- **21호의 결론이 틀렸다고 주장하지 않는다** — 21호가 인용한 수가 ×≈2 크고, 방향은 오히려 강해진다.

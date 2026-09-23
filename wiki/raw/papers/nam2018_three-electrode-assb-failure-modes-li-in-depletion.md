---
title: "Nam, Park, Oh, An, Jung 2018 — Diagnosis of failure modes for all-solid-state Li-ion batteries enabled by three-electrode cells (J. Mater. Chem. A 6, 14867-14875)"
source_url: local-upload/3._Diagnosis_of_failure_modes_for_all-solid-state_Li-ion_batteries_enabled_by_three-electrode_cells.pdf + 3._Sup_Diagnosis_of_failure_modes_for_all-solid-state_Li-ion_batteries_enabled_by_three-electrode_cells.pdf (SI)
source_url_note: "본문 9 쪽(참고문헌 50 편, 그림 6 · 표 1) + SI 16 쪽(그림 S1-S14). 크로퍼가 20 장을 잡았고(S8 누락) 8 장 봤다(Fig. 2-6 · S2 · S4 · S10) — 판정 수치는 화소 좌표 판독(S2 인셋은 원본 래스터). 추출 텍스트에서 µ · fi 글리프 일부 소실, 단위는 렌더링으로 확인. 원자료는 커밋하지 않는다. 17 · 20 · 21 · 40호가 지목한 In 가지 원전."
source_doi: 10.1039/c8ta03450h
source_license: "CC 표기 없음 (지면 '© The Royal Society of Chemistry 2018' · 'Licence and permissions' 링크)"
pdf_sha256: 81b517d8ce87c7361e2b8dbdfbbe26ec2834dba56353d13c1382c44f36609e75
si_sha256: a5fd5d3ecf9c4e356402030c140e6daeb3a7a29cf6764065cd10d6fe192fb02c
ingested: 2026-09-23
sha256: 76dc86240358d54ba13a1a914cf7746ba8de065e890651566a5347f450d7c594
---

# 수집 목적

`assb` 섹션 **41호**. 큐 **42번** — 2차 묶음(큐 40~59, 원장 §1 상단 순서)의 **셋째 편** (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g).
닻은 `questions/assb-contact-loss-vs-lampe.md`. 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md`) ★★★★ · **지목 4 회**(17 · 20 · 21 · 40호) —
"**In-rich depletion layer 원전.** 17호의 국소 고갈(+680~780 mV)과 20호의 Li 도금 전위 도달을 잇는 자리. 21호는 '탈리튬 후 계면 Li 고갈을 실험으로 봤다' 로 인용 — 21호 조립 방향 판정의 원전".
40호(Ikezawa 2020)는 이 편을 ref [5] 로 들어 **In 가지의 뿌리 · Li-In 증인 · "1 C 이상 Li-In 과전압" 선례**로 썼다.
이 편에 걸린 물음은 셋이다: **(1) 0.62 V 를 쟀는가, (2) 고갈층을 봤는가(무엇으로 · 얼마나), (3) "failure modes" 를 무엇으로 가르고 그것이 곱 축퇴(접촉 ↔ `LAM_PE`)에 닿는가.**

Young Jin **Nam**, Kern Ho Park, Dae Yang Oh, Woo Hyun An, Yoon Seok **Jung**(교신) —
**"Diagnosis of failure modes for all-solid-state Li-ion batteries enabled by three-electrode cells"**,
*J. Mater. Chem. A* **2018**, **6**, 14867–14875, doi `10.1039/c8ta03450h`.
`[인쇄]` 접수 2018-04-16 · 수리 2018-07-03 · 게재 2018-07-03. 라이선스 표기: "This journal is © The Royal Society of Chemistry 2018" · "Licence and permissions" 링크뿐 — **CC 표기 없음**.
소속: Hanyang Univ. 에너지공학과(전원) + UNIST(Nam · Oh). 자금: **Hyundai Motor group** · NRF(2017M1A2A2044501 · 2018R1A2B6004996) · MOTIE/KEIT(10076731).
본문 **9 쪽**(참고문헌 50 편), 그림 6 · 표 1 + **SI 16 쪽**(그림 S1–S14, 표 0). PDF sha256 은 frontmatter `pdf_sha256` · `si_sha256`. 원자료는 커밋하지 않는다.
⚠ 같은 해 **Nam · Oh · Jung · Jung 2018 *J. Power Sources* 375, 93** 은 **다른 논문**이다(이 편 ref 39 로 인용된다 — 슬러리 복합전극).

> ⚠ **표기**: `[인쇄]` = 지면에 문자 그대로 있는 것 · `[도표]` = 그림을 열어 읽은 값(figure-read ≈; 판정 수치는 **화소 좌표 판독**, 축 눈금 기준 보정 — Fig. S2 인셋은 원본 래스터 827 × 774 에서 1 화소 ≈1.0 mV · Fig. 5b 하단 1 화소 ≈12 mV · Fig. S10b 하단 1 화소 ≈6.8 mV) ·
> `[재현]` = 지면의 수치로 이 위키가 다시 계산한 것 · `[해석]`/`[추론]` = 이 위키의 해석. 표시가 없는 서술은 원문이 실제로 말한 것이다.
> 추출 텍스트에서 **`µ` 가 빠지고**("730 mm" = 730 µm, "50–60 mm" = 50–60 µm) **`fi` 합자가 일부 글리프째 빠진다**("rst" = first) — 단위는 페이지 렌더링으로 확인했다.

---

# 판정 (먼저)

> ★★★★ **Q5 — 0.62 V 를 쟀는가: 본문 값은 수입이고, SI 그림 한 장이 Li 금속 기준극으로 쟀다 — 수는 인쇄하지 않았다.**
>
> **(a) 본문의 0.62 V 는 인용이다.** `[인쇄]` "Since the reaction of In with Li⁺ ions proceeds via a two-phase reaction (In + Li⁺ + e⁻ → LiIn) with a flat voltage plateau at 0.62 V (vs. Li/Li⁺),**33** it serves as a good RE." — ref 33 = **Jung, Lee, Kim, Kwon, Oh, *Adv. Funct. Mater.* 2008, 18, 3010**(교신저자 Jung 자신의 선행 연구, 제목 미인쇄 · 미열람). ⇒ **0.62 V 의 수입 경로가 하나 더 있다**: 20 · 17 · 21호가 댄 **Santhosha 2019**(이 편보다 늦다) · 20호의 Takada 1996 · **이 편의 Jung 2008 *AFM***. 23호(Koerver 2017)의 "0.6 V" 근거 ref 16 = **Jung · Oh · Nam · Park 2015 *Isr. J. Chem.*** 도 같은 연구실(이 편 ref 9 와 같은 논문)이다 ⇒ **In 가지의 0.6/0.62 V 는 두 경로로 Jung 연구실에 닿는다**(`[해석]`, 원전 둘 다 미열람).
>
> **(b) ★★★★ 그러나 이 편은 셀 안에서 Li 금속 대비로 대조했다 — 계보에서 가장 이르다(2018).** `[인쇄]` "It is confirmed that, when using the Li–In RE, **calibration** of voltages for the WE and CE in the scale of vs. Li/Li⁺ by adding 0.62 V shows **a marginal difference**, compared with the case when using the **Li metal RE** (Fig. S2, ESI)." 같은 설계(cell-2, Sn | Li₆PS₅Cl | Li₀.₅In)의 셀을 **기준극 재료만 바꿔**(Li₀.₅In 분말 74 MPa ↔ Li 박 15 MPa 가압) 전극별 곡선을 겹쳤다.
> `[도표]` Fig. S2 CE/RE 인셋(화소 판독, 1 화소 ≈1.0 mV): **Li 금속 기준극 셀의 CE(Li₀.₅In) = 방전(CE 탈리튬) 중앙값 0.6267 V · 충전(CE 리튬화) 0.6144 V** ⇒ `[재현]` **중점 ≈0.621 V, 반폭 ≈6 mV**(CE 분극 + CE–RE 옴 포함). Li₀.₅In 기준극 셀(+0.62 V 환산) 방전 0.6246 V — 두 셀 차 **≈2 mV**. 충전 인셋은 두 곡선이 겹쳐 빨강이 거의 안 보인다(Li 금속 쪽 위에 그려짐).
> ⇒ **"0.62 V 를 재지 않았다" 가 아니다.** 측정은 있고, **본문은 수를 싣지 않고 "marginal difference" 로 닫았다.** 계보 처방 **P8(기준극의 재료를 바꿔 불변을 본다)의 재료 축 · 전위 판을 2018 원전이 이미 했다** — 단 **셀 간**(한 셀 안 교체 아님) · 전류 중(개방회로 아님) · 전류밀도 미인쇄 · 셀당 n = 1 · 시간 축 없음.
>
> **(c) 40호 "상호 증언" 순환의 다른 쪽 끝이 이 편이다 — 그리고 그 끝은 반쯤 열려 있다.** 40호는 Li-In 문헌값 [5](= 이 편)을 R-LTO 1.55 V 의 증인으로 썼다. 이 편의 값은 **본문으로는 수입(ref 33), SI 로는 Li 금속 대조(Fig. S2)** — 순환 밖의 측정 고리가 **하나** 있다. 그러나 ① 수가 지면에 없고(40호가 가져갈 수 있는 것은 "0.62" 라는 인용 값뿐) ② SE 가 **Li₆PS₅Cl**(40호는 LGPS — Li 가 불안정해 같은 대조를 못 한다고 40호 서론이 적는다) ③ 40호는 이 값을 "**−0.60**"(부호 오기) · "reported values" 로 옮겼다(이 편은 0.62). `[재현]` 이 편의 판독 중점 ≈0.621 V 를 40호 Fig. 1d 중점(−0.9545 V vs R-LTO)에 넣으면 R-LTO ≈**1.575 V** — 40호의 1.55 V 보다 ≈25 mV 높다(40호 digest 의 0.62 V 계산과 같은 결론; **다른 셀 · 다른 SE · 다른 Li-In** 이라 판정 아님).
>
> **(d) Q5 열일곱 번째 형태 — "기준극 교체 대조"**: 가정값(0.62 V, 인용)으로 환산한 곡선을 **다른 재료의 기준극(Li 금속)으로 잰 곡선과 겹쳐 보이고, 차이를 수 없이 "marginal" 로 닫는다.** 18호(제3물질) · 21호(교정 이식) · 40호(상호 증언)보다 **이르고, 셋 중 유일하게 Li 금속을 같은 설계의 셀 안에 넣었다.**
> 그리고 **가정이 컷오프를 정한다**(일곱 번째 형태의 재등장): `[인쇄]` "the discharge cut-off voltage for Sn/Li–In cells was set to be 0 V vs. Li/Li⁺ (or 0.62 V for the WE with respect to the CE)" — 컷오프가 WE/CE 에 걸리므로 **CE 가 0.62 V 에 있다는 가정이 WE 의 종단 전위를 정한다.** (부호: Fig. 2c · 2d 의 WE/CE 는 −0.62 V 로 끝난다 — D2.)

> ★★★★ **고갈층 — 봤다. 단 Li⁺ 이온 계수의 정성 단면 지도 한 쌍이고, "절연" 과 "In-rich" 는 측정이 아니다.**
>
> **(a) 무엇으로 봤나**: 방전 끝(WE/CE 컷오프)까지 간 Sn/Li–In · Sn/Li–In-SE(20 wt%) 반쪽전지를 분해해 CE 단면(Ar 이온 연마)을 **TOF-SIMS(Bi⁺ 25 keV) Li⁺ 지도**로 찍었다(Fig. 4a · b, 영역 300 × 300 · 450 × 450 µm²). `[인쇄]` "The thickness of the Li-depleted layer is **estimated to be 50 µm** for the Li–In CE (Fig. 4a). In stark contrast, for the Li–In-SE CE, the Li-depleted or deficient signals are distributed in much deeper regions."
> `[도표]` Fig. 4a 행 평균 프로파일(색상 → 0–1 환산, 눈금 막대 50 µm = 86 화소): 외표면(점선)에서 **≈33 µm 거의 0**, **반값 깊이 ≈49 µm**(인쇄 "50 µm" ✓), 벌크 평탄 도달 ≈69 µm. CE 전체 두께 ≈215 µm.
> **(b) 무엇이 없나**: **방전 전 대조 지도 0**(고갈이 방전 기원인지 제조 · 연마 기원인지 가르는 짝이 없다) · **Li 정량 0**(계수 척도 "a.u. 0–300" 뿐 — 조성으로 환산 0, TOF-SIMS 매트릭스 효과 보정 0) · **In 지도 0** · 조건당 **시편 1 개** · **분석한 셀의 Sn 적재 · 전류밀도 미인쇄**. EDXS(Fig. S4)는 Li 를 못 보고 **In 이 균일**하게 나온다 — 고갈층은 SEM/EDXS 에 안 보인다.
> **(c) "In-rich" 는 이 편의 낱말이 아니다** — `In-rich` **0 회**. 본문은 "**Li-depleted indium layer**" · 결론은 "**Li-depleted insulating In layers**". "insulating" 은 결론 한 번뿐이고 **전도도 · 임피던스 측정 0**(이 편에 EIS 가 없다). 17호가 인용한 "Li-depleted **In-rich** layers with **low Li conductivity**" 는 뜻은 맞되 두 낱말이 **17호의 것**이다.
> **(d) `[재현]` 전하 수지는 자릿수가 맞는다**: 분석 셀이 Fig. 3 계열(Sn 10 mg cm⁻², SE 무첨가, 307 mAh g⁻¹)이면 통과 전하 ≈**2.15 mAh cm⁻²**. CE 재고는 `[인쇄]` "more than two times higher full capacity for WEs" 로 읽으면 ≈13.4 mAh cm⁻²(치밀 두께 ≈157 µm, 관측 ≈215 µm 와 양립 — "1 배" 로 읽으면 ≈79 µm 라 관측과 안 맞는다). ⇒ 완전 고갈 등가 두께 ≈**25 µm(치밀) … 34 µm(관측 두께 비례)** ↔ 지도의 거의-0 띠 ≈33 µm · 반값 ≈49 µm. **같은 자릿수다 — 지도가 전하 수지와 모순되지 않는다**(가정 넷: 분석 셀 정체 · "2 배" 해석 · 신호 ∝ Li · Li 원천이 합금뿐).
> **(e) ⚠ Fig. 4b 의 "더 깊은 결손" 은 SE 상과 교락된다**(`[해석]`): Li–In-SE 복합체에서 Li⁺ 계수가 낮은 망상 영역은 **Li₆PS₅Cl 입자 자리와 형태가 겹친다**(Fig. S4b 의 S 지도). 황화물과 금속의 Li⁺ 2차 이온 수율이 다를 수 있어, 대조 지도 없이 "결손이 깊게 분포" 와 "SE 상이 깊게 분포" 를 가를 수 없다. `[도표]` 행 평균으로는 (b) 도 벌크 도달 깊이가 (a) 와 비슷하다(≈y 165–180 화소) — 다른 것은 **표층 수준**(a ≈0 · b ≈0.33)이다.
> ⇒ **21호 인용("탈리튬 후 계면 Li 고갈을 실험으로 봤다")은 선다** — 봤다. **단 강도는 "정성 지도 1 쌍 + 전위 거동" 이다.** 그리고 이 편의 CE 는 **Li 금속 + In 분말을 Thinky 믹서로 섞은 분말 전극**이지 박이 아니다 ⇒ 21호의 **조립 방향(박의 어느 면이 분리막에 닿나)** 은 이 편이 시험하지 않았다. 이 편이 지지하는 것은 **③ 의 방전 기원 가지**뿐이다(분말이 처음에 균질했다는 확인도 없다).

> ★★★ **고장 모드 — 셋을 가르고, 셋 다 양극 `LAM`·접촉 손실이 아니다.** ① **반쪽전지의 상대극 병목**(Sn/Li–In: 겉보기 WE 용량 손실이 CE) · ② **얇은 SE 완전지의 Li 관통 연성 단락**(NCM622/Gr, 50–60 µm SE, ≥0.5 C 충전) · ③ **0 V 과방전 내성**(NCM 이 1.8 V 에서 과리튬화되지만 이후 열화 없음). 양극 쪽은 `[인쇄]` "no significant changes in mechanical integrity for the composite NCM and Gr electrodes were observed after cycling (Fig. S11)"(단면 SEM, 0.2 C 10 사이클) 한 문장으로 닫힌다 — **접촉 손실은 정성 부정 한 줄, `θ(N)` 0/41.**
> **3전극이 곱 축퇴에 닿는가: 닿지 않는다 — 양극 전위 채널은 있으나 양극 용량 손실을 분석하지 않았고 EIS 가 없다.** 대신 이 편은 3전극의 **옴 배정 문제**를 가장 날카롭게 보여 준다(아래 ★★★).

> ★★★ **`[재현]` 배면형 기준극은 분리막 옴 전부를 상대극 채널에 싣는다 — 그리고 "Gr < 0 V" 판정은 그 안에 있다.** 기준극은 **WE 뒷면**에 추가 SE 층으로 붙는다(Fig. 2b; NCM 은 Al 박의 1 mm² 구멍으로 연결). 측정은 `[인쇄]` "applying the current between the WE and CE while the open-circuit voltage of the WE/RE was measured" — CE 전위는 **WE/RE − WE/CE 로 얻는 파생 채널**이다. ⇒ WE/RE 에는 분리막 옴이 **안 들어가고**(20호 `[인쇄]` "ohmic resistances were not incorporated" 는 WE 쪽에서만 맞다), **CE/RE 에 분리막 전부 + WE 층 이온 경로가 들어간다.**
> 전류 반전 순간의 계단(옴 + 빠른 분극의 상한)을 같은 그림에서 읽으면: `[도표]` Fig. 5b(50–60 µm SE, **1 C**) Gr 최저 ≈**−0.02 V**, 반전 계단 ≈0.19 V → **절반 ≈0.10 V** · Fig. S10b(730 µm SE, **2 C**) Gr 최저 ≈**−0.15 V**, 계단 ≈0.41 V → **절반 ≈0.20 V**. ⇒ **관측된 "0 V 아래" 가 계단 절반보다 작다** — 3전극 궤적만으로는 Gr 이 Li 도금 전위를 넘었는지 **판정되지 않는다.** 도금의 증거는 따로 선다: `[인쇄]` ⁷Li MAS-NMR 264 ppm 금속 Li(2 C 20 분 · 0.1 C 8 시간 대조, **두꺼운 SE 의 Gr/Li–In 반쪽전지**) · Ni 부직포 감지극의 전위 급락(연성 단락). 저자도 두꺼운 SE 셀의 0 V 아래 구간은 "possible deposition" 으로만 적는다.

---

# 0. 원문에 없어서 확인이 필요한 것

| # | 공백 | 왜 중요한가 |
|---|---|---|
| G1 | **Fig. S2 의 조건** — 전류밀도 · Sn 적재 · 두 셀인가 한 셀의 순차 교체인가 · 측정 순서 · 온도 미인쇄 | 기준극 교체 대조(열일곱 번째 형태)가 **셀 간 산포를 포함한 비교**인지 판정 |
| G2 | **기준극 누설 · 드리프트 · 시간 안정성 · 재고 0**. Li 금속 기준극의 Li₆PS₅Cl 계면 안정성(서론이 "deteriorating chemical reaction of SEs with Li metal" 을 적는다)도 검사 0 | 누설 직접 측정 **0/41** |
| G3 | **TOF-SIMS 대조군(방전 전) 0 · Li 정량 0 · In 지도 0 · 분석 셀의 적재 · 전류 미인쇄 · 시편 1 개** | 고갈층의 **방전 기원 · 두께 · 조성** |
| G4 | **NCM/Gr 완전지의 기준극이 Li₀.₅In 인가 Li 박인가** 미기재(실험절은 둘 다 적는다) | "vs Li/Li⁺" 축의 0.62 V 가정 여부 |
| G5 | **옴 보상 0 · 전류 반전 계단 · 휴지 전위 0** — `ohmic` 0 회 · `overpotential` 0 회 | "Gr < 0 V" · CE 종단 전위의 옴 몫 |
| G6 | **n(조건당 셀 수) · 오차 막대 0** | 전 수치 |
| G7 | **1 C 의 정의(mA g⁻¹)** 미인쇄 | 율 비교 · 40호 "1 C" 선례 대조 |
| G8 | **슬러리 SE 층(NBR 함유)의 이온 전도도** 미인쇄 — 분말 3.0 × 10⁻³ S cm⁻¹(30 °C)만 | 분리막 옴 크기 |
| G9 | **NMR 정량(금속 Li 양) 0** — 조건당 스펙트럼 1 개 | 도금 양 |
| G10 | **CE 양의 규칙이 두 가지로 읽힌다** — "more than two times higher full capacity" ↔ "set to accommodate a capacity of 959 mAh g_Sn⁻¹" | 재고비(조건 (5)) |
| G11 | **Fig. S4 시편이 방전 후인가 방전 전인가** 미기재 · **Mo 박**(실험절은 Ti 집전체) | EDXS 해석 · D3 |

---

# 1. 서지 · 낱말 지문

| | |
|---|---|
| 종류 | 실험 논문(*J. Mater. Chem. A*, PAPER), 신품 + 단기 사이클(≤ 수십 사이클), 열화 모드 분석 0 |
| 쪽 | 본문 9(참고문헌 50) · 그림 6 · 표 1 · SI 16 쪽(그림 S1–S14) |
| 셀 | 반쪽: **Sn(SE 30 wt%) \| Li₆PS₅Cl(150 mg) \| Li₀.₅In(± SE 10/20 wt%)** · 완전지: **NCM622 \| Li₆PS₅Cl(50–60 µm 슬러리 또는 730 µm 펠릿) \| Gr 또는 Si–C** · PEEK 몰드 ∅1.3 cm, Ti 집전 |
| 3전극 | **cell-1**: RE 가 SE 층 옆면(≥1 mm SE 필요) · **cell-2**: RE/SE/WE/SE/CE — RE 를 **WE 뒷면**에 추가 SE 층(120 mg)으로. 완전지는 Al 박을 1 mm² 제거해 연결 |
| 기준극 | **Li₀.₅In 분말(74 MPa 가압) 또는 Li 박(15 MPa)** |
| 압력 | 조립 **370 MPa** → RE 층 74 / 15 MPa → **운전 74 MPa**(`[인쇄]` "All the all-solid-state cells were cycled under 74 MPa") |
| 온도 | 30 °C |

**★ 낱말 지문** (규칙: NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문(참고문헌 전); SI 는 괄호):

| `identifiab` | `uncertaint` | `conf.interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM` | `degradation mode` | `contact loss` | `MPa` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **0** | **0** | **0** | 0 | 0 | **1** | 0 | 0 | 0 | **0** | **6** (SI 0) |

NFKC 변경 본문 **57 자**(`ﬀ` 29 · `ﬁ` 14 · `ﬃ` 10 · `ﬂ` 2 · `¨` 1 · `¼` 1) — **열 변화 0**. ⚠ RSC 조판이라 `fi` 가 **합자로 남는 곳과 글리프째 빠지는 곳이 섞인다**("veriﬁcation" ↔ "rst") — `identiab` 따로 검사: 0. `µ` 도 빠진다. 소프트 하이픈 0 · 줄끝 하이픈 **53 곳** — 이으면 `Li-depleted` 3 → 4 · `reference electrode` 1 → 2 · `Li metal` 29 → 34, **지문 열 변화 0**.
**`calibrat` 1 은 Q5 문장 자체다** — "calibration of voltages … by adding 0.62 V". **`MPa` 6** = "hundreds of MPa"(서론) · 74 ×3 · 15 · 370.
**Q5 보조 열**: `leak` 1(**연성 단락 누설 전류** — 기준극 아님) · `drift` **0** · `assum*` **0** · `stab*` 1(Na 음극 안정성) · `reproducib*` 0 · `0.62` **4** · `marginal` 1 · `open-circuit` 1(측정 방식) · `ohmic` **0** · `IR` 0 · `overpotential` **0** · `polariz*` 1 · `In-rich` **0** · `deplet*` 4 · `insulat*` 1(결론) · `contact` 8(전부 접속 · 접촉 형성, 손실 0) · `failure mode` 2(제목 · 결론) · `degrad*` 1("no noticeable degradation") · `plating` 1.
`[해석]` **`assum*` 0 회인데 가정이 있다** — 가정이 "**calibration** … by adding 0.62 V" 로 적힌다. 21호의 "calculated/converted based on" · 40호의 "reported … can be calculated" 와 같은 부류이고, **이번에는 지문 열(`calibrat`)에 걸린다** — 지문 표에서 `calibrat` 가 0 이 아닌 편은 35 · 36호도 있으나(불확실성 보정 · 확산계수 보정) **기준 전위 환산 자체를 가리키는 것은 이 편이 처음이다**(표 40 · 41 행과 35 · 36 행 대조, 01–34 행 전수 확인은 안 함).

---

# 2. 셀 · 실험 (`[인쇄]`, 괄호 안 `[재현]`)

- **SE**: Li₆PS₅Cl, 볼밀 600 rpm 10 h → 550 °C 5 h, **3.0 × 10⁻³ S cm⁻¹(30 °C)**.
- **Sn 전극**: Sn(10 µm) : SE = 70 : 30 wt, 손 혼합. 적재 **4 · 10 mg_electrode cm⁻²** (`[재현]` Sn 2.8 · 7.0 mg cm⁻²).
- **슬러리 전극**(자일렌, NBR): NCM : SE : NBR : 도전재 = 68.1 : 29.2 : 1.4 : 1.3 · Gr 58.6 : 39.1 : 2.3 : 0 · Si–C 59.4 : 39.6 : 1.0 : 0. 적재 NCM **23** · Gr **14 mg cm⁻²**. 얇은 SE 층은 **Gr 전극 위에 직접 닥터블레이드**(자일렌–NBR 슬러리) → 50–60 µm. np ≈1.1.
- **CE**: Li 금속 + In 분말(± SE)을 **Thinky 믹서 2000 rpm 1 분**. 공칭 **Li₀.₅In**(`[재현]` 33 at% Li, In+LiIn 2상역 안). SE 10 · 20 wt% ≈ 26 · 44 vol%. 양: "more than two times higher full capacity for WEs by full lithiation of Li₀.₅In to LiIn … set to accommodate a capacity of 959 mAh g_Sn⁻¹" (G10).
- **조립**: WE/SE/CE 370 MPa → 추가 SE 120 mg → RE(Li₀.₅In 분말 74 MPa 또는 Li 박 15 MPa). 운전 74 MPa. 전압창: Sn 반쪽 0.0–2.0 V(vs Li 환산) · NCM/Gr 2.50–4.25 V · NCM/Si–C 1.20–4.25 V.
- **Ni 부직포 감지 셀**: Gr / SE / **Ni-NW**(Ni 스퍼터 부직포, SE 함침) / SE / Li–In — 2 C 로 Gr 을 리튬화하며 Ni-NW 전위(vs Li–In)를 잰다.
- **분석**: TOF-SIMS(ION-TOF 5, Bi⁺ 25 keV) · FESEM/EDXS(Hitachi S-4800, Ar 이온 연마 1.5 kV 4 h) · ⁷Li MAS-NMR(233.12 MHz, 25 kHz, LiCl 기준, 공기 노출 없이).

---

# 3. 절별 해체

## 3.1 서론 (p1–2)

- 액체셀처럼 Li 금속을 상대극 겸 기준극으로 쓰기 어려운 이유: `[인쇄]` "not only a deteriorating chemical reaction of SEs with Li metal … but also the penetrating growth of Li metal into the defects of SE structures" ⇒ "This must be the reason why In or Li–In, not Li metal, has been mostly used as the counter and reference electrode".
- `[인쇄]` "However, its significant contribution to the kinetic behavior of all-solid-state half-cells has **not been evaluated yet**, deterring reliable interpretation of WEs." — ref 34(Zhang … Janek 2017 *ACS AMI*: LCO/In 셀의 저주파 In–SE 계면 저항이 방전 끝에 커진다)를 선행으로 든다. **10호(Vadhva) 가 인쇄한 경고의 원전 쪽과 같은 관측**이다.
- 박막 ASSB 3전극 선례 1 건(ref 37 Yu 1997, Li 금속 RE). 벌크형은 `[인쇄]` "cold-pressing under high pressures (hundreds of MPa) … makes the design … extremely challenging", 그리고 실용 SE 두께가 수십 µm 라 액체셀 설계를 못 옮긴다.

## 3.2 Sn/Li–In 반쪽전지 — Fig. 1 · 2 · 3 · S1–S3

- `[인쇄]` 첫 방전 용량 **534 (4 mg) → 307 mAh g_Sn⁻¹ (10 mg)** — 액체 Sn/Li 반쪽전지 **958**(Fig. S1). 차이는 **0.5 V(vs Li) 아래 구간**에서 나오고, 0.5 V 위 두 평탄(180–220 mAh g⁻¹)은 액체셀과 비슷하다 ⇒ 상대극을 의심.
- **cell-1 ↔ cell-2**: cell-1 은 SE **2.2 mm**, cell-2 는 **730 µm** — cell-1 의 낮은 용량 · 율 특성을 두꺼운 SE 저항으로 돌린다.
- ★★★ `[인쇄]` "As suspected, the overall discharge is ended by termination of Li–In CEs, not Sn WEs." 방전 끝 Sn 전위 **0.43 (cell-1) · 0.36 V (cell-2)** vs Li — 0 V 에 못 간다.
  `[도표]` Fig. 2d CE/RE: 방전 내내 ≈0.6 V(환산) → 끝에서 **≈1.05 (cell-1) · ≈0.95–1.0 V (cell-2)** 로 치솟고, **충전(CE 리튬화)으로 바뀌는 즉시 ≈0.6 V 로 돌아온다**(휴지 없음 — 이완이 아니라 전류 반전).
  `[재현]` **항등식**: 컷오프가 WE/CE = −0.62 V 이므로 종단 순간 **E_CE = E_WE + 0.62 V** — 0.36 + 0.62 = 0.98 · 0.43 + 0.62 = 1.05, 그림과 맞다.
- **Li–In-SE 복합 CE**(Fig. 3): 0.11 mA cm⁻² 에서 **652 (10 wt%) · 689 mAh g_Sn⁻¹ (20 wt%)**. CE 종단 전위 `[인쇄]` **1.07 → 0.72 · 0.71 V**. `[도표]` Fig. 3c(0.11 · 0.57 · 1.1 · 2.3 mA cm⁻²): SE 0 % ≈1.07 · 1.135 · 1.17 · 1.185 V · 10 % ≈0.72 · 0.79 · 1.035 · 1.06 V · 20 % ≈0.71 · 0.71 · 0.76 · 0.86 V.
  ★★★ `[재현]` **Fig. 3c 는 CE 의 성능 곡선이 아니다** — 위 항등식 때문에 "종단 전위" = **WE 종단 전위 + 0.62 V** 다. 20 wt% 의 0.71 V 는 "CE 가 90 mV 만 올랐을 때 WE 가 ≈0.09 V 에 닿아 컷오프" 를, 0 % 의 1.07 V 는 "WE 가 ≈0.45 V 에 있을 때 CE 가 +0.45 V 튀어 컷오프" 를 뜻한다. **어느 전극이 끝을 냈는가의 지표로는 쓸 수 있으나, CE 과전압의 크기 곡선으로는 못 쓴다**(컷오프가 자른 값이고, 전류 의존성에는 CE–RE 사이 분리막 옴이 들어 있다 — `[재현]` 730 µm × 3.0 mS cm⁻¹ ⇒ ≈24 Ω cm², 2.3 mA cm⁻² 에서 ≈56 mV).
  ⇒ 40호의 "At higher discharge rates than 1C, Li-In shows relatively large overpotential at the end of the discharges, **in agreement with a previous report [5]**" 가 가리키는 것이 이 그림이다. 이 편은 **C 율이 아니라 전류밀도**로 적었고(`[재현]` 40호 1 C = 0.733 mA cm⁻² 는 이 편 0.57–1.1 mA cm⁻² 사이), 값은 컷오프 항등식의 산물이다 — **"선례" 는 방향(끝에서 CE 가 오른다)만 선다.**
- Fig. S2: 기준극 교체 대조 — 판정 (b) 참조.

## 3.3 고갈층 — Fig. 4 · S4

판정 "고갈층" 절 참조. 추가로:
- `[인쇄]` 해석: "the Li-depleted indium layer is formed at the top of the CE, **impeding further movement of Li⁺ ions from the inner regions** of Li–In to the SE layer, which results in early termination" · 복합 CE 는 "utilization of Li⁺ ions from much deeper regions … facilitated by the aid of percolated SEs".
- `[도표]` Fig. 4c · d 는 **모식도**다 — 색 범례 "Li₀.₀In ↔ Li₀.₅In" 은 측정 조성이 아니다.
- `[도표]` Fig. S4a(Li₀.₅In, ×350): CE 두께 ≈200 µm(눈금 막대 판독), EDXS In **균일**, O 가 국소 반점. **위쪽에 "Mo foil"** 표지(D3). Fig. S4b(Li₀.₅In-SE, ×250): In 섬 · S 망상 · **O 가 길쭉한 줄 모양으로 강하게** — 설명 0. `[해석]` 시편 산화(이송 · 연마) 가능성이 있고, 그렇다면 TOF-SIMS Li⁺ 계수의 매트릭스도 바뀐다.
- `[도표]` Fig. 4a 의 **바닥 쪽(집전체 쪽) 가장자리도 Li⁺ 가 약하다**(행 평균이 마지막 ≈25 µm 에서 0.82 → 0.55 로 하강) — 설명 0. 가장자리 효과가 외표면 띠에도 섞였을 수 있다(`[해석]`, 대조군 없이 못 가른다).

## 3.4 NCM/Gr 완전지 — Fig. 5 · Table 1 · S5–S10

- 첫 사이클 반쪽전지: `[인쇄]` NCM/Li–In **149** · Gr/Li–In-SE **310 mAh g⁻¹**(0.1 C). 완전지 0.1 C 방전 **137 mAh g_NCM⁻¹** → 1 C **82**.
- **이상 거동**: 0.5 C 부터 충전 곡선 **4.1 V 부근 평탄**(dQ/dV 날카로운 봉우리) · 쿨롱 효율 **99.0 %(0.2 C) → 88.7 · 80.3 · 82.5 %(0.5 · 1 · 2 C)**. 730 µm SE 셀은 99.5–99.8 % · 평탄 없음(Table 1).
- `[인쇄]` "Starting at 1C, charging of the Gr electrode proceeds below 0 V (vs. Li/Li⁺). This would inevitably lead to deposition of Li metal" — `[재현]` 판정 ★★★ 참조: **1 C 최저 ≈−0.02 V ↔ 반전 계단 절반 ≈0.10 V.**
- ⁷Li MAS-NMR(Fig. 5c): **2 C 20 분 → 264 ppm 금속 Li 봉우리**, 0.1 C 8 시간 → 없음. `[인쇄]` 시편은 "Gr/Li–In all-solid-state cells" 의 Gr + 접한 SE, SE 는 **150 mg 펠릿(730 µm)** — **완전지 · 얇은 SE 셀이 아니다.**
- **Ni-NW 감지극**(Fig. 5d · e): `[인쇄]` Ni-NW 전위 **1.8 V 로 0.17 h 유지 → 급락해 Gr 전위에 붙는다** ⇒ "electrical connection (or ISC) between Ni-NW and Gr electrodes, which must be attributed to the penetrating growth of Li metal through the SE layers." `[도표]` 그 구간 Gr 은 ≈**−0.4 V**(vs Li 환산) — 이 셀은 **Li–In 이 상대극 겸 기준극**이라 분리막 옴 전부 + Li–In 분극이 들어간다(저자도 이 값으로 도금을 주장하지 않는다).
  `[해석]` **이 설계는 단락을 "전위 급락" 이라는 이진 사건으로 잡는다 — 계보에서 드문, 옴 배정에 안 걸리는 검출 채널이다**(전위가 1.8 V ↔ Gr 전위로 두 자릿수 크게 움직인다).
- Fig. 5f 기구: 관통 Li 가 NCM 에 닿으면 `[인쇄]` "NCM … will be chemically lithiated by consuming the as-contacted Li metal, which is the opposite direction to charge and causes **leakage of current**" ⇒ 충전 전하 과잉 · 쿨롱 효율 저하.
- 두꺼운 SE(730 µm) 셀도 Gr 0 V 아래가 보인다(S10) — `[인쇄]` "indicating the **possible** deposition of Li metal on Gr", 단락은 `[인쇄]` "approx. ten times longer distances" 로 없다.
- 양극 기계 건전성: `[인쇄]` Fig. S11 단면 SEM(0.2 C 10 사이클) "no significant changes" · "the applied pressure (74 MPa) … would deform the SEs having low Young's modulus of 20–30 GPa(ref 47 Koerver 2018), maintaining the integrity" · "severer test conditions, such as extended cycling and **less applied pressure**, may cause mechanical failure … future work."

## 3.5 0 V 방전 — Fig. 6 · S12–S14

- `[인쇄]` 첫 사이클 쿨롱 효율 **NCM 79.1 %**(SE 접촉) < **Gr 92.5 %** ⇒ "The overall first-cycle discharge is ended by **full lithiation of NCM**, not by full delithiation of Gr, which is opposite to the case for conventional LIBs." 대조로 **Si–C 66.7 %** → NCM/Si–C 는 Si–C 가 끝을 낸다(`*` 표시, Si–C 종단 전위가 Gr 보다 높다).
- 0 V 정전류 → 0 V 정전압 24 h → 정상 사이클. `[인쇄]` NCM/Gr 에서 NCM 이 **1.8 V(vs Li)** 에서 과리튬화(화살표), NCM/Si–C 의 NCM 은 **>3 V** 유지. 둘 다 이후 `[인쇄]` "no noticeable degradation"(Fig. 6 · S12–S14).
- `[도표]` Fig. 6a 0 V 유지 구간에서 **Gr 전위가 ≈3.4 V(vs Li)** 까지, Fig. 6b 에서 **Si–C 가 ≈3.6 V** 까지 오른다 — 본문은 NCM 과리튬화만 말하고 **음극(SE 39–40 wt% 포함)이 3 V 이상에 24 h 머문 것**은 논하지 않는다. `[해석]` 황화물 SE 의 산화 쪽 안정창과 부딪치는 조건일 수 있으나 이 편 지면에는 판단 재료가 없다.
- `[인쇄]` 과방전 1.75 V 평탄의 가역성은 ref 49(LiNi₀.₇₅Co₀.₂₅O₂, in situ XRD)를 빌려 설명하고 "clear elucidation … remains".

## 3.6 결론

`[인쇄]` "a novel all-solid-state three-electrode cell that enabled **diagnosis of failure modes for positive and negative electrodes separately**" · "overall capacity was limited by the Li–In CEs, not by the Sn WEs, which was attributed to the formation of **Li-depleted insulating In layers**" · "The Li–In-SE CEs … serve as a reliable test protocol for all-solid-state half-cells."

---

# 4. ★★★★ Q5 — 계보에서 이 편의 자리

## 4.1 시간 순서가 뒤집힌다

이 편(2018-07)은 In 가지에서 **가장 이르다** — 20호(Chang, 2019-08 접수)보다, Santhosha 2019 보다, 40호(Ikezawa 2020)보다 앞선다. 20호 · 21호 · 40호 · 17호가 다 이 편을 인용한다(각각 ref [10] · 13 · [5] · 20).
⇒ **"0.62 V 의 출생지 = Santhosha 2019"**(20호 digest ①)는 **"Santhosha 경로의 출생지"** 로 좁혀 읽어야 한다 — 0.62 V 는 그 전에 이미 ASSB 에서 **Jung 2008 *AFM* 을 근거로** 쓰이고 있었다.

## 4.2 열일곱 번째 형태 — 기준극 교체 대조

| | 이 편(41호, 2018) | 21호(2023) | 40호(2020) |
|---|---|---|---|
| 기준 값 | 0.62 V (ref 33 수입) | GWRE 0.31 V | R-LTO 1.55 V (ref [11] 수입) |
| 대조 대상 | **Li 금속 기준극** (같은 설계 셀, SE 같음) | Li \| Li 교정 셀(3 MPa) | 문헌 증인 둘 |
| 셀 안? | 같은 **설계**의 다른 셀 | 다른 셀 · 다른 압력 | 대조 없음(셀 안 Li 설계상 불가) |
| 수 인쇄 | **없다** ("marginal difference") | 있다 (0.31 V) | 있다 (3.90 · −0.60) |
| `[재현]` 분해능 | **≈2 mV**(인셋 1 화소 ≈1 mV) | — | ≈25 mV 를 못 가른다 |

`[해석]` **이 표의 역설**: 계보에서 **가장 분해능이 높고 가장 이른 대조가, 수를 싣지 않아 인용 사슬에 안 들어갔다.** 40호는 이 편에서 "0.62"(인용 값)만 가져갔고, 17호는 Santhosha 를, 21호는 교정 이식을 썼다. **처방 P11("측정 축을 같이 인쇄") 이 왜 필요한지의 원전 표본이다.**

## 4.3 평탄 조건 (1)–(8) 대조 — CE Li₀.₅In

- (1) 2상역: 공칭 Li₀.₅In(33 at%) ✓. `[재현]` SE 무첨가 CE 가 끝날 때 평균 **≈Li₀.₄₂In**(재고의 ≈16 % 사용, "2 배" 해석) — 전체 조성은 2상역 안.
- (2) 분리막 면 LiIn: **방전이 깬다** — 이 편이 (2) 의 붕괴를 **TOF-SIMS 로 본 첫 편**(정성). 분말 전극이라 제조 기원 여부는 시험 안 됨.
- (5) 재고비: `[재현]` ≈6.2(SE 0 %, 307) · ≈2.8(SE 20 %, 689) — **재고가 6 배 남은 쪽이 먼저 끊겼다** ⇒ 21호의 "17호를 깬 것은 (5) 가 아니라 (2)" 와 **같은 방향의 이른 표본**(`[추론]`, 두 해석 G10 중 "2 배" 쪽 위).
- (6) 전류밀도: 0.045–2.3 mA cm⁻² — (6) ≲0.1 mA cm⁻² 는 0.045 한 점만. 그 0.045 에서도 SE 무첨가 CE 가 끊긴다(Fig. 2d) ⇒ **(6) 을 지켜도 (2) 가 깨지면 끊긴다.**
- (4) CE–RE 옴: 보상 0, 이 배치에서는 분리막 전부가 CE 채널로 — 위 ★★★.
- (8) 개방회로 0.62 V ≠ (2) 검사: 이 편에 개방회로 측정 0 — 해당 없음.

---

# 5. `[재현]` 검산

## 5.1 Fig. S2 인셋 화소 판독

원본 래스터(827 × 774, JPEG) 추출. 방전 인셋 축 눈금 0.64 V = y 585 · 0.63 = 595 · 0.62 = 604.5(≈1.03 mV/화소). 충전 인셋 같은 눈금 행.
빨강(Li₀.₅In RE) · 보라(Li 금속 RE) 화소를 열마다 평균:

| 구간 | Li 금속 RE (보라) | Li₀.₅In RE (빨강, +0.62 환산) | 차 |
|---|---:|---:|---:|
| 방전 인셋(정규 용량 0.1–0.5) | 중앙 **0.6267** (0.6256–0.6287) | 중앙 **0.6246** (0.6236–0.6267) | ≈2 mV |
| 충전 인셋(0.3–0.8) | 중앙 **0.6144** (0.6138–0.6174) | 보라 밑에 가림(보이는 6 열 0.616) | ≲2 mV |

⇒ Li 금속 대비 **CE Li₀.₅In 중점 ≈0.621 V · 반폭 ≈6 mV**. 반폭에는 CE 분극과 CE–RE 사이 분리막 옴(이 배치에서는 분리막 전부)이 들어 있어 **열역학 평탄 폭 ① 의 상한으로만** 쓴다(17호 ±10 mV 와 같은 층).

## 5.2 반전 계단 — "Gr < 0 V" 의 분해능

| 그림 | SE | 율 | Gr 최저 | 반전 직후 | 계단 | 절반 |
|---|---|---|---:|---:|---:|---:|
| Fig. 5b | 50–60 µm | 1 C | ≈−0.02 V | ≈+0.17 V | ≈0.19 V | **≈0.10 V** |
| Fig. S10b | 730 µm | 2 C | ≈−0.15 V | ≈+0.26 V | ≈0.41 V | **≈0.20 V** |

(y 눈금: Fig. 5b 0 V = 806.5 · 1 V = 723 화소, Fig. S10b 0 V = 2270 · 1 V = 2123 화소.) 계단 절반은 옴 + 빠른 계면 분극의 **상한**이라, 보상 후 Gr 전위가 0 V 위인지 아래인지는 **이 궤적만으로 정해지지 않는다.** 두꺼운 SE 쪽 계단이 두 배인 것은 분리막 옴이 CE 채널에 들어간다는 배치 해석과 같은 방향이다(율도 두 배라 가르지 못함).

## 5.3 CE 재고와 고갈 두께

판정 "고갈층 (d)" 참조. 식: In 몰 = Q / (0.5 F) · 두께 = m_In / ρ_In(7.31 g cm⁻³, Li 부피 무시). `[도표]` Fig. 4a 반값 깊이 ≈49 µm · 거의-0 띠 ≈33 µm · CE ≈215 µm(눈금 50 µm = 86 화소).

## 5.4 Table 1 의 행 라벨

"Discharge capacity" 행 = 177 · 141 · 124 · 115 · 102 · 61, "Charge capacity" 행 = 137 · 137 · 123 · 102 · 82 · 50 인데 본문은 방전 **137**(0.1 C) · **82**(1 C) — **두 행 이름이 뒤바뀌었다**(D1). 쿨롱 효율 = 두 번째 행 / 첫 번째 행(`[재현]` 137/177 = 77.4 % ↔ 인쇄 77.3 ✓).

---

# 6. 우리 축 (Q1–Q8)

| Q | 이 편 |
|---|---|
| Q1 정량 | **없다.** `contact` 8 회 전부 접속 · 접촉 형성. 양극 건전성은 SEM 정성 부정 한 줄(10 사이클). **`θ(N)` 0/41** |
| Q2 독립관측 | 이동 없음(**반 칸 검토 후 접음**). 전극 분해로 **겉보기 WE 용량 손실을 CE 로 귀속**(20 · 17호와 같은 층, 시점만 이르다) + CE 고갈을 **TOF-SIMS 로 독립 관측** — 대상이 상대극이고 양극 `LAM` ↔ 접촉이 아니다 |
| Q3 라벨층위 | 층 하나 — **cutoff-identity terminal value**(CE "종단 전위" 곡선 = WE 종단 + 0.62 V, 컷오프가 만든 값) · 셀 간 기준극 교체 대조는 **수 미인쇄**. n 0 · 오차 막대 0 |
| Q4 유일성 | **0/41 — 서른세 번째 성질 "전극 분해를 '진단' 으로 인쇄했다 — 분해가 분리막 옴을 어느 전극 채널에 싣는지 묻지 않고"**. `identifiab` · `uncertaint` 0 |
| **Q5 Li-In** | **+0.5 — 열일곱 번째 형태 "기준극 교체 대조"**: Li 금속 기준극 셀 ↔ Li₀.₅In 기준극 셀, `[도표]` 차 ≈2 mV · Li 대비 중점 ≈0.621 V. P8(재료 축 · 전위)의 첫 실행이자 계보 최초(2018). 반 칸인 이유: 셀 간 · 전류 중 · 수 미인쇄 · n = 1 · 시간 0. 그리고 **(2) 의 붕괴를 본 첫 편**(TOF-SIMS, 정성) |
| Q6 압력 | 이동 없음 — **제조 370 · 운전 74 MPa 를 명시적으로 가른다**(RE 층 74 / 15). 스윕 0. "less applied pressure" 는 미래 과제 |
| Q7 dead Li | 해당 없음(무음극 아님). ⚠ 단 **Gr 위 도금 Li 의 관통**은 이 편의 주제 — 무음극 계보(6 · 7호)의 단락 경로와 같은 현상 쪽 |
| Q8 화학·OCP | 이동 없음 — NCM622(첫 사이클 쿨롱 효율 79.1 %) · Gr · Si–C. OCP 곡선 기울기 0 |

★ **카드에 주는 것 — 칸 밖 셋**
1. **쿨롱 효율 → `LLI` 대리 통로의 세 번째 오염 경로 "연성 단락 누설"**(`[해석]`): 이 편의 쿨롱 효율 80–89 %(≥0.5 C)는 Li 손실이 아니라 **관통 Li 가 NCM 을 화학적으로 되리튬화하는 누설**이다(`[인쇄]` 기구). 2전극 노화 해석은 이것을 `LLI` 로 적는다. [[assb-li-in-reference-potential-window]] "왜 중요한가 3" 의 경로(상대극 전위 · 무음극 재고)에 하나를 더한다.
2. **첫 사이클 끝을 양극이 낸다**(NCM 79.1 % < Gr 92.5 %): 액체셀과 반대로 **방전 끝이 양극 벽**이면 음극 쪽 여유 Li 가 남아 **작은 `LLI` 가 용량에 안 보인다**(38호 "재고 과잉이면 `LLI` 가 용량에 안 보인다" 와 같은 구조, `[해석]`). 균등화(α · β) 이식에서 **어느 전극이 끝을 내는가**가 ASSB 에서 뒤집힐 수 있다는 첫 인쇄다.
3. **Ni-NW 감지극 = 옴 배정에 안 걸리는 이진 채널** — 부호 판정(Gr < 0 V)이 계단 안에 있을 때 쓸 수 있는 대안 설계.

---

# 7. ★★★ 곱 축퇴 처방 — 스물네 번째 적용

| 단계 | 입력 | 판정 |
|---|---|---|
| 1단계 `R`·`C` | **EIS 0** | ❌ 적용 불가 |
| 2단계 면적 대조군 | 없음 | ❌ |
| 3-a `Ea` | 없음(30 °C 한 점) | ❌ |
| 3-b `C` 물리 상한 | 없음 | ❌ |
| 4단계 시간 영역 | 3전극 DC 곡선 — **전류 반전 계단**(Fig. 5b · S10b) · 컷오프 항등식(Fig. 2d · 3c) | ⚠ 옴 몫의 **상한**만 — 보상 0 |

**⇒ 이 적용이 처방에 더하는 것**: 새 줄 **"배면형 기준극은 분리막 옴 전부를 상대극 채널에 싣는다 — 파생 채널의 부호 판정은 반전 계단 절반과 먼저 비교한다."** 40호의 "3전극 옴 몫은 기준극 위치가 정한다" 의 **극단 표본**이다(40호는 1 : 3.2 로 나눴고, 이 편은 0 : 1). 그리고 **컷오프가 WE/CE 에 걸리면 CE 종단 전위는 WE 종단 + 오프셋의 항등식**이라 "상대극 성능 곡선" 으로 쓰지 않는다.
**⚠ 이것이 곱을 푼 것은 아니다** — 양극 용량 손실 분석 0 · EIS 0 · 면적 0. 기여는 곱 앞의 **배정 오염 크기 둘**(≈0.10 · ≈0.20 V 계단 절반)이다.

---

# 8. 어긋남 (실제로 어긋난 것만)

| # | 무엇 | 어디 |
|---|---|---|
| **D1** | **Table 1 의 "Discharge" · "Charge" 행 이름이 뒤바뀜** — 본문 방전 137 · 82 는 표의 "Charge" 행 | Table 1 ↔ p4 본문 |
| **D2** | **컷오프 부호** — "0.62 V for the WE with respect to the CE" · "fully discharged down to 0.62 V" ↔ Fig. 2c · 2d · 3a · S2 WE/CE 는 **−0.62 V** 로 끝남 | p2 · p3 ↔ 그림 |
| **D3** | **Fig. S4a 에 "Mo foil"** ↔ 실험절 "Ti metal current collectors" — 설명 0 | S4 ↔ p8 |
| **D4** | **Fig. 3c "Terminal voltage" 는 컷오프 항등식**(WE 종단 + 0.62) — 본문은 CE 이용률의 지표로 읽는다 | Fig. 3c ↔ p3 |
| **D5** | **"Gr below 0 V" 가 반전 계단 절반 안** — 1 C ≈−0.02 ↔ ≈0.10 V | Fig. 5b ↔ p4 |
| **D6** | **CE 양 규칙 두 문장** — "more than two times higher full capacity" ↔ "accommodate a capacity of 959 mAh g_Sn⁻¹" | p8 |
| **D7** | ref 35(Jung 2013 *AEM*)가 **액체 3전극 배치 · Ni-NW 스퍼터 방법 · LIB 전극 균형** 셋에, ref 36(Bhide 2014 *PCCP*)이 **Swagelok 3전극 · SE 전도도** 둘에 달린다 — 번호 밀림 가능성(`[추론]`, 원전 미열람) | p2 · p7 · p8 |
| D8 | **교차 편**: 40호가 이 편 값을 "−0.60 V vs Li" · "reported values" 로 인용 — 이 편은 **0.62**(부호 +) | 40호 ↔ p1 |
| D9 | **교차 편**: 17호 "Li-depleted **In-rich** layers with **low Li conductivity**" — 이 편 `In-rich` 0 회 · 전도도 측정 0("insulating" 결론 1 회) | 17호 ↔ p3 · p7 |
| D10 | **교차 편**: 40호 "1C 이상 … previous report [5]" — 이 편은 C 율이 아니라 mA cm⁻², 값은 컷오프 항등식(D4) | 40호 ↔ Fig. 3c |

---

# 9. 그림 — 무엇을 봤나

크로퍼가 **20 장**(본문 Fig. 1–6 · Table 1 + SI S1–S7 · S9–S14)을 잡았다. **Fig. S8 은 크로퍼가 놓쳤다**(SI p10 — NCM/Li 전고체 셀의 이상 평탄 · 쿨롱 효율).

- **본 것 8 장**: **Fig. 2**(cell-1/2 설계 · WE/CE · WE/RE · CE/RE) · **Fig. 3**(복합 CE · 종단 전위) · **Fig. 4**(TOF-SIMS — 행 평균 프로파일 화소 판독) · **Fig. 5**(완전지 3전극 · NMR · Ni-NW — 1 C Gr 궤적 화소 판독) · **Fig. 6**(0 V 방전) · **Fig. S2**(기준극 교체 — **원본 래스터 인셋 화소 판독**) · **Fig. S4**(단면 EDXS) · **Fig. S10**(두꺼운 SE 완전지 — 2 C Gr 궤적 화소 판독).
- **안 본 것 12 장**: Fig. 1 · S1 · S3 · S5 · S6 · S7 · S9 · S11 · S12 · S13 · S14 · Table 1 이미지(텍스트로 읽음). S8 은 크롭 없음.
- **본문과 어긋난 그림**: Fig. 2c · 2d · S2(D2 컷오프 부호) · Fig. 3c(D4) · Fig. 5b(D5) · Fig. S4a(D3 Mo 박) · Fig. 6(본문이 말하지 않는 음극 ≈3.4–3.6 V).

---

# 10. 참고문헌 중 후속 후보 (50 편 중 — 미열람, 서지는 지면 그대로)

| 서지 | ref | 왜 | 축 |
|---|---|---|---|
| **Jung, Lee, Kim, Kwon, Oh, *Adv. Funct. Mater.* 2008, 18, 3010** | 33 | **이 편 0.62 V 의 유일한 근거** — Santhosha 2019 이전 경로, 교신저자 자신의 선행 | Q5 |
| **Jung, Oh, Nam, Park, *Isr. J. Chem.* 2015, 55, 472** | 9 | 23호(Koerver) "0.6 V" 근거(ref 16)와 같은 논문 — In 가지 가정의 두 번째 Jung 연구실 경로 | Q5 |
| Zhang, Weber, Weigand, … Zeier, Janek, *ACS Appl. Mater. Interfaces* 2017, 9, 17835 | 34 | LCO/In 셀의 In–SE 저주파 저항이 방전 끝에 커진다 — 10호(Vadhva) 인용 경고의 원전 후보 | Q5 · Q2 |
| Yu, Bates, Jellison, Hart, *J. Electrochem. Soc.* 1997, 144, 524 | 37 | 박막 ASSB Li 금속 RE 3전극 — 20호도 [11] 로 인용 | Q5 |
| Koerver, Zhang, de Biasi, … Janek, *Energy Environ. Sci.* 2018 (DOI 10.1039/C8EE00907D) | 47 | SE 영률 20–30 GPa · 74 MPa 에서 건전성 유지 논거 | Q6 · Q1 |
| Nam, Jo, Oh, … Jung, *Nano Lett.* 2015, 15, 3317 | 38 | 얇은 SE 층 · Ni-NW 계열 선행 | Q6 |
| Nam, Oh, Jung, Jung, *J. Power Sources* 2018, 375, 93 | 39 | ⚠ 원장의 별도 행(슬러리 복합전극) — 이 편과 다른 논문 | Q1 |

큐 43–59 중 이 편이 인용하는 것: **0 편**(시점상 대부분 불가 — 이 편이 2018-07 로 큐 편들보다 이르다. Solchenbach 2016 · Illig 2012 · Jin 2015 는 시점상 가능하나 인용 0). ⚠ ref 44 **Uhlmann, Illig, Ender, Schuster, Ivers-Tiffée 2015 *J. Power Sources* 279, 428**(Li 도금 인용)은 큐 52 **Illig 2012 *JES* 159 A952 와 다른 논문**이다.

---

# 11. 이 digest 가 주장하지 않는 것

- **"이 편이 0.62 V 를 측정해 확정했다" 고 하지 않는다** — 본문 값은 인용이고, Fig. S2 의 ≈0.621 V 는 **우리 화소 판독**(전류 중 · 셀 간 · 조건 미인쇄)이다. 주장은 "Li 금속 기준극 대조가 지면(SI)에 있고, 수는 인쇄되지 않았다" 까지다.
- **R-LTO 가 1.575 V 라고 하지 않는다** — 다른 셀 · 다른 SE(LGPS ↔ Li₆PS₅Cl) · 다른 Li-In 조성 위의 산술이다.
- **Li 도금이 없었다고 하지 않는다** — NMR · Ni-NW 가 2 C 에서 선다. 주장은 "3전극 Gr 궤적의 0 V 아래는 **그 자체로는** 계단 절반 안이라 판정 근거가 못 된다" 까지다. 계단 절반은 옴의 **상한**이지 옴이 아니다.
- **고갈층이 없다고 하지 않는다** — TOF-SIMS 가 있다. 주장은 대조군 · 정량 · 반복이 없어 **두께 "50 µm" 와 "insulating" 이 측정 강도로 서지 않는다**는 것까지다. 전하 수지 대조는 가정 넷 위다.
- **Fig. 4b 의 결손이 SE 상이라고 하지 않는다** — 교락 가능성이다.
- **Fig. 6 의 음극 3.4–3.6 V 가 SE 를 분해했다고 하지 않는다** — 지면에 판단 재료가 없다.

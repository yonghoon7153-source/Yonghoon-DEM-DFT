---
title: "Ren, Danner, Moy, Finsterbusch, Hamann, Dippell, Fuchs, Müller, Hoft, Weber … Latz, Srinivasan, Janek, Sakamoto, Wachsman, Fattakhova-Rohlfing 2023 — Oxide-Based Solid-State Batteries: A Perspective on Composite Cathode Architecture (Adv. Energy Mater. 13, 2201939)"
source_url: local-upload/15._Oxide_based_solid_state_batteries_a_perspective_on_composite_cathode_architecture.pdf + 15._Sup_Oxide_based_solid_state_batteries_a_perspective_on_composite_cathode_architecture.pdf (SI)
source_url_note: "Perspective 본문 34 쪽(참고문헌 222 번호) + SI 15 쪽(P2D 식 (1)-(10) · Figure SI-1 · SI-2). 크로퍼 13 장(그림 9 + 표 4) + 수동 크롭 2 장(SI-1 · SI-2). Read 7 장(Fig. 1 · 4 · 5 · 7 · 9 · SI-1 · SI-2), 안 본 것 Fig. 2 · 3 · 6 · 8, 표는 텍스트로. 종설 — 인용 원전은 미열람. 원자료는 커밋하지 않는다."
source_doi: 10.1002/aenm.202201939
source_license: "© 2022 The Authors — CC BY-NC (open access)"
pdf_sha256: fd9943e8635f2d944897695e91e7a7ee394740bc1cec96d0a0b1b6b72176717c
si_sha256: bbd08b42ca4e3f2b82a1355fe28c1ce54104f6a045a1861eefc44a31835f1581
ingested: 2026-09-23
sha256: af2ccf84688b29094aef96ce15f506af5656a8d40ec1885575409ba7a34a7117
---

# 수집 목적

`assb` 섹션 **53호**. 큐 **54번** — 2차 묶음(큐 40~59, 원장 §1 상단 순서)의 **열다섯째 편** (`bms-balancing/docs/ASSB_TRANSFER_NOTE.md` §6-3-g).
닻은 `questions/assb-contact-loss-vs-lampe.md`. 원장(`bms-balancing/docs/ASSB_WANTED_PAPERS.md`) 행 ★★: "**`θ(N)` 시간축의 입구** — 1·2호가 동역학을 안 줬다", ⚠ "Perspective(종설형)·LLZO 산화물계 — 1차 `θ(N)` 측정 기대는 낮고, 그 안의 1차 원전을 찾는 입구로 본다". 지목 1 회 — **02호 Clausnitzer 2023 ref 17** (02호가 "pore formation and contact loss … mechanical degradation due to volume changes of the CAM during operation" · "electrochemical and mechanical degradation" · "single-crystal NMC, conducting additives" 를 전부 이 편에 매달았다).
이 digest 의 1순위 물음: **(1) 복합양극 접촉 손실의 시간 진화 `θ(N)` 을 이 편 자신이 재거나 모델링하는가, 아니면 그것을 준 1차 원전을 가리키는가 — 가리킨다면 무엇을, 정량으로? (2) 산화물(LLZO) 공소결 복합양극에서 접촉 손실은 언제 생긴다고 쓰나 — 제조(소결 · 냉각)인가 운전(사이클)인가, 황화물과 무엇이 다른가. (3) 모델 쪽(Danner · Latz)은 접촉 손실을 어느 자리에 넣는가 — 37호(Li 2024)의 두 자리(`ε_p` = `LAM_PE` 동어반복 · `A_eff·k_p` 곱)와 대조.**

Y. Ren(공동 1저자), **T. Danner**(공동 1저자), A. Moy, M. Finsterbusch, T. Hamann, J. Dippell, T. Fuchs, M. Müller, R. Hoft, **A. Weber**, L. A. Curtiss, P. Zapol, M. Klenk, A. T. Ngo, **P. Barai**, B. C. Wood, R. Shi, L. F. Wan, T. W. Heo, M. Engels, J. Nanda, F. H. Richter, **A. Latz**, V. Srinivasan*, **J. Janek***, J. Sakamoto*, E. D. Wachsman*, D. Fattakhova-Rohlfing* (28 인, * 교신 5) —
**"Oxide-Based Solid-State Batteries: A Perspective on Composite Cathode Architecture"**,
*Adv. Energy Mater.* **2023**, **13**(1), 2201939, doi `10.1002/aenm.202201939` · 표제 "**Perspective**" · "Editor's Choice".
`[인쇄]` Received 2022-06-08 · Revised 2022-09-09 · Published online 2022-11-20 · "© 2022 The Authors … open access … Creative Commons Attribution-NonCommercial License". `[인쇄]` "Y.R. and T.D. contributed equally to this work."
소속 9 곳: UMD(MEI2) · **DLR–HIU Ulm**(Danner · Dippell · Latz) · U. Michigan · **FZJ IEK-1**(Finsterbusch · Engels · Fattakhova-Rohlfing) · **JLU Giessen**(Fuchs · Richter · Janek) · **KIT IAM-ET**(Müller · A. Weber) · **ANL**(Curtiss · Zapol · Klenk · Ngo · Barai · Srinivasan) · LLNL · ORNL. 자금: 미·독 공동 "CatSE / CatSE2"(DOE + BMBF). `[인쇄]` "The authors declare no conflict of interest."
**계보 겹침**: 02호(Clausnitzer 2023)와 **같은 DLR · Latz 계열**(Danner · Latz) · 49호(Barai 2018)의 제1저자 **Barai** · 51호(Illig 2012)의 KIT IAM-ET(**A. Weber**) · 23호(Koerver 2017) · 1호(Bielefeld 2019)의 **Janek** 연구실이 저자다.

본문 PDF **34 쪽**(Perspective 29 쪽 + 참고문헌 **222 번호**, 하위 a–h 포함) · SI PDF **15 쪽**(§1 열역학 에너지 밀도 계산 절차 · §2 P2D 모델 식 (1)–(10) · Figure SI-1 · SI-2 · 참고문헌 14). sha256 은 frontmatter(본문 `pdf_sha256` · SI `si_sha256`). 원자료는 커밋하지 않는다.

> ⚠ **표기**: `[인쇄]` = 지면에 문자 그대로 있는 것 · `[도표]` = 그림을 열어 읽은 값(figure-read ≈) ·
> `[재현]` = 지면의 수치로 이 위키가 다시 계산한 것 · `[해석]`/`[추론]` = 이 위키의 해석. 표시가 없는 서술은 원문이 실제로 말한 것이다.
> ⚠ **종설이다.** 이 편의 1차 기여는 §7.4 의 **P2D 사례 계산**(자기 모델, 문헌 파라미터)과 §7.4.1 의 **열역학 에너지 밀도 계산**뿐이다. 나머지 서술은 전부 인용이고, **인용 문장만으로 채움표 칸을 올리지 않는다**(32 · 33 · 36호 선례). 인용된 1차 원전은 **이 digest 에서 열람하지 않았다** — 서지와 이 편이 매단 문장만 적는다.

---

# 판정 (먼저)

> ★★★★ **Q1 — 이 편은 `θ(N)` 을 재지도 모델링하지도 않는다(`θ(N)` 0/53). 그리고 "측정은 없다" 를 스스로 인쇄한다.** `[인쇄]` "**There is yet no experimental study that incorporates percolation theory and its influence on mechanical degradation.**" · "**no experimental technique has successfully estimated the fracture strength between the CAM and SE particles.**" 자기 P2D 사례 계산은 접촉을 **1 로 못 박는다** — `[인쇄]` SI "the CAM and LLZO form a percolating network … allowing **full utilization** of the active material. We assume a **completely dense composite after sintering without any porosity**" · "**Electrochemical and mechanical degradation processes are also neglected** in the simulations"; 본문 "assuming percolating transport pathways in both CAM and SE when neglecting electrochemical and mechanical degradation phenomena". ⇒ **02호가 기대한 "`θ(N)` 시간축의 입구" 는 이 편 안에서 닫힌 문으로 확인된다** — 문 뒤에 있는 것은 **정량 1차 측정 0 · 사이클 축을 가진 모델 1 편(Barai 2021, ref [127]) · 사이클 용량 곡선을 준 산화물 실험 셋(refs [83] · [104] · [105]/[11])** 이다(아래 목록).
>
> **(a) 이 편이 가리키는 `θ(N)` 쪽 1차 원전 — 이 편이 매단 문장 그대로(원전 미열람)**:
> - ★★★★ **[127] Barai, Rojas, Narayanan, Ngo, Curtiss, Srinivasan, *Chem. Mater.* 2021, 33, 5527** — `[인쇄]` "Computational modeling of the interfacial delamination between the CAM and LLZO during charge/discharge reveals that the **capacity fade cause[d] by mechanical detachment persists for ten cycles without showing saturation**" · "LLZO with smaller grains, softer electrolytes (e.g., sulfides), or better interfacial adhesion … may help to minimize interfacial de-bonding". **계보에서 처음 나오는 "사이클 축 위의 박리 모델"** — 10 사이클 · 포화 없음. 저자 Barai · Ngo · Curtiss · Srinivasan 이 **이 편의 공저자**(자기 인용).
> - ★★★ **[83] Tsai … Guillon, *Sustainable Energy Fuels* 2019, 3, 280** (LCO/LLZO 스크린 인쇄 + 통상 소결) — `[인쇄]` §4.2 "loss of most of the initial capacity (**1.8 to 0.4 mAh cm⁻²**) within **100 cycles** at 50 µA cm⁻²" · §3.3 "twice the areal capacity (**1.62 mAh cm⁻²**) at 50 °C … a high cycling degradation of about **50–60 % after 50 cycles** … mechanical failure due to the chemomechanical stresses during cycling was identified as origin" · §4.2.2 "Such a degradation was shown for LLZO/LCO based cells and **unambiguously pinpointed the increase in ASR stemming from the electrodes, with the mixed cathode being the most likely origin**" · "microcracks appeared in the mixed LLZO/LCO cathode as both trans-granular cracks in LCO and LLZO particles, especially close to macropores, and as cracks between LCO and LLZO particles". ⇒ **사이클 용량 곡선 + 사후 균열 관측**이지 접촉 분율이 아니다(이 편이 옮긴 문장 기준).
> - ★★★ **[105] Ihrig … Guillon, *J. Power Sources* 2021, 482, 228905** (FAST/SPS 치밀 LCO–LLZO, ≈95 % 이론밀도) — `[인쇄]` "high density and **no sign of mechanical degradation, excluding this failure mechanism**, but also exhibited rather large capacity losses within the first 5 cycles, dropping from **1.2 to 0.8 mAh cm⁻²**" · §3.3 "often losing up to **10 % capacity per cycle** … Since cracking of the cathode, as observed for free sintered cathodes with 80 % density, **was ruled out** as cause for the degradation, the results provided the first evidence of an **electrochemical** degradation". ⇒ **기계 기구를 뺀 대조군**(공정으로 `θ` 경로를 끈 셀)이 여전히 빠르게 감쇠한다 — 카드 물음에 가장 쓸모 있는 원전 후보. ⚠ "ruled out" 의 근거 채널은 이 편에 없다.
> - ★★★ **[11] Ihrig … Guillon, *ACS Appl. Mater. Interfaces* 2022, 14, 11288** — Fig. 4a–d 원전(TEM/EDX 사이클 전후, Al → LCO · Co → LLZO 확산, LLZO 비정질화 → "highly resistive interfacial layers").
> - ★★ **[104] Rosen … Fattakhova-Rohlfing, *J. Mater. Chem. A* 2022, 10, 2320** (테이프 캐스팅 공소결 · 조성 구배) — `[인쇄]` "initial discharge capacities of **2.75 mAh cm⁻²**, which drop to **1.3 mAh cm⁻² after only 10 cycles** (see Figure 7d)". ⚠ `[도표]` Fig. 7d 는 **첫 방전 곡선 셋**(이론 용량 대비 %)뿐, 사이클 데이터 0(D4).
> - ★★ **[12] Finsterbusch, Danner, Tsai, Uhlenbruck, Latz, Guillon, *ACS Appl. Mater. Interfaces* 2018, 10, 22329** — 1050 °C 30 분 소결 ≈80 % 밀도 LCO–LLZO, 첫 방전 0.84 mAh cm⁻² · 이용률 ≈81 % · 100 °C 운전, **3D 미세구조 분해 연속체 모델**(DLR). 50–60 %/50 사이클 감쇠 문장이 [83] 과 묶여 있다.
> - ★★ **[126] Bucci, Talamini, Renuka Balakrishna, Chiang, Carter, *Phys. Rev. Mater.* 2018, 2, 105407** — `[인쇄]` cohesive zone 으로 "LLZO should delaminate from the CAM particles if the active materials **shrink by more than 7.5 %** during operation". **문턱**이지 `N` 축이 아니다.
> - ★★ **[108] Mücke … Guillon, *J. Power Sources* 2021, 489, 229430** — 3D 미세구조 응력(LLZO 인장 → "microcracking and **ionic isolation of regions**"). 응력 분포이지 `N` 축 아님. SI 참고문헌 [4] 로도 쓰였다.
> - ★★ **[32] Neumann, Randau, Becker-Steinberger, Danner, Hein, Ning, Marrow, Richter, Janek, Latz, *ACS Appl. Mater. Interfaces* 2020, 12, 9277** — `[인쇄]` "**Loss of contact between CAM and SE leads to a decrease in electrochemically active surface area, which can substantially increase the charge transfer resistance and cause voltage and capacity fade.**" — DLR 계열(Danner · Latz)의 **접촉 손실 → 활성 면적** 모델 문장. 계면 면적 자리(`A_eff`)에 넣는 쪽의 원전 후보.
> - ★ [122] Besli … Doeff 2019 *Chem. Mater.* 31, 491("isolation of particles") · [121a] Ruess … Janek 2020 *JES* 167, 100532(균열 → 확산 저하, `D` 2.5 × 10⁻¹² 의 출처) · [107] Koerver … Janek 2018 *EES* 11, 2142(부피 변화 곡선 Fig. 4e) · [95] Han … Wang 2018 *Joule* 2, 497(LCBO 소결조제 — 100 °C 40 사이클 ≈50 % ↔ 25 °C 100 사이클 15 %, "strong electrochemo-mechanical effect").
>
> **(b) 큐 55–59 대조**: **55 Neumann 2021 = ref [27]** ✅(본문 5 곳 + SI [10] — `σ_LLZO` 8 × 10⁻⁴ · `β_GB` 1.39 · `β_tort` 2.31 의 출처) · **56 Hlushkou 2018 ❌ 인용 0** · **57 Bielefeld 2022 = ref [203]** ✅(한 문장 — 입도 분포 · 농도 의존 동역학) · **58 Bielefeld · Weber · Janek 2020 = ref [151b]** ✅(한 문장 — 도전 바인더 분포 → 활성 면적) · 59 Asheri 2023 ❌(이 편보다 늦다). **1호 Bielefeld 2019 = ref [151a]** · **23호 Koerver 2017 = ref [103]**.
>
> ★★★★ **산화물 특유 — 접촉 손실의 시점은 둘이다: 제조(냉각)와 운전(사이클). 제조 쪽은 모델 예측뿐, 운전 쪽은 사후 균열 서술뿐.**
> - **제조**: `[인쇄]` §3.2 "upon cooling interfacial stresses can arise … either remain as residual stresses … or dissipate through the formation of interfacial cracks … **Such cracks at the interface between the CAM and LLZO can lead to a reduction in electrochemically active surface area** and increased interfacial resistance" · Yu 2019 [82] 연속체 모의 "stresses **approaching 1 GPa**" ↔ LLZO 파괴강도 "approximately **100–150 MPa**" ⇒ "fracture of LLZO composite electrodes is **possible** during the cooling". CTE: LLZO ≈1.5 × 10⁻⁵ · LCO 1.25 × 10⁻⁵ · NMC 1.3 × 10⁻⁵ K⁻¹ — "≈0.2 × 10⁻⁵ K⁻¹ difference". `[재현]` 0.2–0.25 × 10⁻⁵ K⁻¹ × ≈1000 K ≈ 0.2–0.25 % 변형 × 150–185 GPa ≈ **300–460 MPa**(1축 · 푸아송 무시) — 1 GPa 모의와 같은 자릿수, 파괴강도의 ×2–4. 소결 중 기공 영역이 응력 집중점([204] Fathiannasab 2021) · 반응 생성물 몰부피 불일치([89] · [90]). ⇒ `[해석]` **산화물에서 `θ` 의 초기값은 공정 변수다** — 소결 경로(자유 소결 ≈80 % ↔ FAST/SPS ≈95 %) · 냉각 이력 · 소결조제가 `θ₀` 를 정하고, 그 값은 이 편 어디에도 측정으로 없다.
> - **운전**: `[인쇄]` §4.2 두 영역 — "1) the first charge/discharge cycle shows a large capacity fade in combination with a low Coulombic efficiency and 2) the subsequent cycles show a capacity fade at a slower, but substantial rate, while the Coulombic efficiency is rather high"([83,103]) · "The majority of reports indicate that the rapid capacity fade during the first charge/discharge step can be attributed to the **electrochemical oxidation of the interface** … whereas the slower subsequent decay is due to **fatigue failure of the CAM/SE interface and loss of electrochemically active surface area**." — **"fatigue" 문장에는 인용 번호가 없다.**
> - ★★★★ **황화물과의 차이를 지면이 둘로 인쇄한다 — 그리고 시간 배정이 계에 따라 뒤집힌다.** §5.2(황화물): `[인쇄]` "contact loss can be induced by volume changes of CAM" · "**Koerver et al. link this phenomenon to an irreversible resistance increase in the first cycle**, lowering the Coulombic efficiency to 70.5 %" · 해결책 "substantial pressure (**>10 MPa**) during operation … considered to be impractical" · "Since there are few cycling studies using oxide SEs, **it is not understood yet if the aforementioned effects are also present in sintered oxide-oxide cathodes**." ↔ §4.2(산화물): 접촉(피로)은 **이후 사이클**, 첫 사이클은 **산화**. ⚠ 두 영역 문장이 인용한 [103] 은 **황화물 논문(23호)** 이고, 23호 원문은 `[인쇄]` "While the contact loss should **only occur during the initial charge** … the ongoing capacity fade can be attributed to the propagating **interphase** formation" — **이 편 §4.2 의 배정과 정반대**다(D2). 33호(Zhang 2025)가 같은 역전을 했다("decrease in electrochemical activity **in subsequent cycles**") — **종설에서 두 번째 표본**, 발행은 이 편이 먼저다.
> - `[해석]` **소결 결합의 파단은 압력으로 되돌릴 수 없다** — 황화물의 재가압 채널([[assb-pressure-reapplication-separation-test]], 4호 300 MPa)은 산화물 공소결 복합양극에서 같은 뜻을 갖지 않는다. 이 편은 산화물 셀의 **운전 압력을 한 번도 적지 않는다**(`MPa` 7 중 6 이 응력 · 강도, 1 이 황화물 >10 MPa).
>
> ★★★★ **모델 쪽(Danner · Latz) — 자기 모델에는 접촉 손실의 자리가 없고, 서술은 두 자리를 가리킨다.**
> - **자기 P2D**(SI Table 1, 식 (1)–(10)): `a·i_se` 로 전하 보존에 들어가는 **`a` 는 SI 어디에도 정의되지 않는다**(D5) · `ε_CAM` 75 vol% **고정**(노화 없음 → 37호 ① `ε_p(N)` 자리 없음) · 계면 = BV `i_se = 2·i₀₀·√c_s·sinh(Fη/2RT)` + **직렬 옴** `η = Φ_s − Φ_e − U₀ − i_se·R_SP` · `i₀₀ = (1/R_CT)(RT/F)(1/c_max^0.5)`(임피던스 선형화로 매개변수화). ⇒ 접촉 면적이 들어갈 수 있는 곳은 `a` 하나이고, 거기서 **`a·i₀₀`(= 37호 ② `A_eff·k` 곱)** 와 **`a/R_SP`(직렬 옴 — 37호에 없는 세 번째 곱)** 두 조합으로만 보인다(`[해석]`, 식에서).
> - **서술이 가리키는 두 자리**: ① "decrease in electrochemically active surface area … increase the charge transfer resistance and cause voltage **and capacity** fade"([32]) — **면적 자리**(`A_eff`, 37호 ② 형) ② "isolation of particles, with subsequent capacity fade"([122]) · "ionic isolation of regions of the mixed cathode"([108]) — **고립 자리**(`u` · 1 · 2호 `θ` 연결 분율 형). 이 편은 두 낱말을 **구분 없이** 쓴다. `[해석]` P2D 의 면적 자리에서 용량 손실은 과전압을 통해서만(율 의존) 나온다 — ①의 "capacity fade" 는 모델 안에서는 ②와 다른 서명이다.
> - **제안**: `[인쇄]` "An appropriate computational model needs to be developed that takes into account the ionic and electronic transport through these SE/CAM composites and study the influence of mechanical degradation within the cathode particles on the overall capacity fade" · 결론 "By using reconstructed microstructures of real cells as input parameters for continuum modeling, electrochemical performance and electro-chemomechanical stress evolution can be assessed" — **미세구조 분해(1 · 2호 형) + 역학 결합** 쪽이다. `ε_p` 로 넣자는 제안(37호 ①)은 없다.
>
> **채움표: 새 칸 0** (≈20.0 그대로). Q1 0/53(인쇄된 공백 두 문장 — 층 하나) · Q2 반 칸 검토 후 접음(FAST/SPS "기계 기구 배제" 대조는 원전 [105] 서술의 재인용) · **Q4 0/53 마흔다섯 번째 성질**(아래) · Q3 층 하나 · Q5 · Q6 · Q7 없음/해당 없음 · Q8 부분(NMC811 OCV = 액체 18650 원전 곡선). **곱 축퇴 처방 서른여섯 번째 적용**(1–4단계 ❌ · 새 줄 "전류 진폭 — 직렬 `R_SP` ↔ `R_CT`").

---

# 0. 원문에 없어서 확인이 필요한 것

| # | 없는 것 | 왜 필요한가 |
|---|---|---|
| G1 | **P2D 식의 `a`(비계면 면적) 정의** — SI Table 1 식 (1)·(2) 에 `a·i_se` 로만 등장 | 접촉 면적이 들어갈 유일한 자리. 구 기하(`3ε/r`, 50호 형)라면 `d50` 손잡이가 확산 길이와 면적을 같이 움직인다(§6 · D6) |
| G2 | **[127] Barai 2021 의 박리 모델 형태** — `θ` 를 무엇으로(면적 · 연결 분율 · 균열 길이), 10 사이클 곡선의 수치 | 이 편이 가리킨 유일한 `N` 축 모델. 이 편은 한 문장만 옮긴다 |
| G3 | **[105] "no sign of mechanical degradation" 의 근거 채널**(SEM 단면? CT? 셀 수?) | 기계 기구를 뺀 대조군의 성립 여부 — 카드의 가장 쓸모 있는 조작 |
| G4 | **[83] 두 수치의 관계**(1.62 mAh cm⁻² @50 °C ↔ 1.8 → 0.4 mAh cm⁻² @50 µA cm⁻²) | 같은 원전을 두 절이 다른 초기값으로 인용(D7) |
| G5 | **산화물 셀의 운전 스택 압력** | Q6. `MPa` 7 중 산화물 운전 압력 0; "no applied pressures" 는 Li\|LLZO 음극 반쪽 [4,5] 에만 |
| G6 | **§4.2 "fatigue failure" 의 인용** | 산화물 접촉 손실을 "이후 사이클" 에 배정한 문장에 번호 0 |
| G7 | **`R_CT` = `R_SP` = 2600 Ω cm² 두 칸의 합 근거** | 본문 "about 2600 … reported" 한 값 + "most … attributed to resistive secondary phases" ↔ 표 두 칸 다 2600(D3) |
| G8 | **Fig. 4a 셀의 상대극** | 캡션 "Li metal anode" ↔ `[도표]` 축 "Voltage (V vs **In-Li**)" (D8) |
| G9 | **상태 · 조건당 셀 수 · 오차** | 사례 계산은 결정론 모델(± 무의미), 인용 실험의 n 은 전부 0 |

---

# 1. 서지 · 낱말 지문

규칙: NFKC 뒤 · 대소문자 구분 · 낱말 경계 · 본문은 참고문헌 전까지(Wiley 내려받기 바닥글 줄 제외, "Received" 앞에서 자름). SI 는 괄호(§3 References 전). 줄끝 하이픈은 이은 판을 병기.

| `identifiab` | `uncertaint` | `confidence interval` | `Bayes` | `posterior` | `calibrat` | `LLI` | `LAM` | `degradation mode` | `contact loss` | `MPa` |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | **0** (0) | **0** (0) | **0** (0) | 0 (0) | **5** (0) | **7** (0) |

- NFKC 변경: 본문 **375 자**(NBSP 297 · U+2002 41 · U+2005 13 · `µ` 22 · `Ω` 옴 기호 2) · SI **244 자**(수학 이탤릭 U+1D4xx — 식 (1)–(10) 전부 · `µ` 4) — **열 변화 0**. 소프트 하이픈 본문 **6**(`­Creative` 등) · SI 0. 줄끝 하이픈 본문 **436 곳** · SI 4 곳 — 이으면 `contact` 21 → 23 · `pressure` 29 → 31 · `sensitiv*` 13 → 15 · `active surface` 11 → 13 · `identif*` 11 → 13 — **열 변화 0**.
- ⚠ Wiley 조판 추출에서 본문 식(σ_Li,eff · κ_eff)이 **글자 조각으로 흩어진다**("8 10 LLZO 0 4 σ = × −") — 쪽 렌더로 읽었다. 그림 안 글자(Fig. 4a 축 "V vs In-Li" 등)는 래스터라 세지 않는다.
- **`contact loss` 5 = 황화물 4**(§5.2 세 번 + Fig. 5 캡션 — 전부 β-Li₃PS₄/NCM811, 23호 · Walther 2020) **+ 일반 1**(§7.1.1 "the volume changes cause mechanical damage to CAM particles as well as delamination and contact loss with SE" — 인용 번호 없음, §4.2.2 를 가리킴). 산화물에 쓴 동의어: `[Ll]oss of contact` 2(§4.2.2 [32] 문장 · §7.4.2 "loss of contact and active surface area") · `delaminat*` 8 · `detach*` 2 · `isolat*` 2 · `fatigue` 1(인용 0) · `saturation` 1([127]).
- **`MPa` 7 = 응력 · 강도 6**(LLZO 파괴강도 100–150 · >100 · 입계 파열 "hundreds of" · CAM 파괴강도 "hundreds of" · 공간전하층 응력 "hundreds" · 계면 인장 "hundreds of MPa to a few GPa") **+ 운전 압력 1(황화물 ">10 MPa", "impractical")**. 산화물 셀의 운전 압력 값 0. `GPa` 7(탄성률 · 응력 1 GPa).
- 보조(이은 판, 본문 / SI): `crack*` 17 / 0 · `CTE` 19 / 0 · `percolat*` 7 / 2 · `cycles?` 23 / 0 · `capacity fad*` 14 / 0 · `impedance` 15 / 1 · `assum*` 12 / 6 · **`Deconvol*` 1**("Deconvolution of the contributions in impedance data is challenging") · `sensitiv*` 15 / 0 · `indium` 3 / 0(Fig. 2 캡션 "lithium indium" · "lithium (or indium metal) anodes" · 산화인듐주석) · **`reference electrode` · `three-electrode` · `OCV` · `error` 0 / 0** · `reproduc*` 1(라이선스 문구 "reproduction in any medium" — 재현성 뜻 0; 대문자 `Reproduced` 20 은 그림 재수록 표기) · `exchange current` 0 / 2 · `Butler` 1 / 1 · `kΩ` 1(§4.1 "1–5 kΩ cm²", 인용 0).
- `[해석]` **식별성 · 불확실성의 낱말은 0 이고, 그 자리를 "sensitivity analysis"(OAT 스파이더, §7.4.2)가 차지한다** — 36 · 37 · 42호 계열의 "민감도 = 설계 KPI 스윕" 이다([[assb-sensitivity-sweep-vs-identifiability]]).

---

# 2. 이 편의 1차 기여 — P2D 사례 계산 (§7.4.2 + SI §2)

**셀**(Fig. 8a · SI §1.1): Li 금속 \| LLZO 치밀층 **10 µm** \| LLZO 다공층에 CAM 공소결/함침 = 복합양극 **50 · 100 µm**, **CAM 75 vol%**, 도전재 0 · 공극 0 · 액체 0. 전류 **1 · 10 mA cm⁻²**, 실온.

**식**(SI Table 1, `[인쇄]`): CAM 전자 `a·i_se = ∂x(κ_eff ∂xΦ_s)` (1) · LLZO 이온 `−a·i_se = ∂x(σ_Li,eff ∂xΦ_e)` (2) · 입자 확산 Fick 구 (3) · 계면 `i_se = 2·i₀₀^CAM·√c_S·sinh(F η/2RT)` (4) · `η = Φ_S − Φ_E − U₀^CAM(c_S) − i_se·R_SP` (5) · Li 음극 `i_Li = 2·i₀₀^Li·sinh(F(Φ_Li − Φ_E)/2RT)` (6) · `κ_eff = ε_CAM^βs·κ_CAM(c_s)`, `β_s` = 2.3 고정 (7) · `σ_Li,eff = ε_LLZO^βe·σ⁰_LLZO`, `β_e = β_GB + β_tort` (8) · `i₀₀^CAM = (1/R_CT,CAM)(RT/F)(1/c_max^0.5)` (9) · `i₀₀^Li = (1/R_CT,Li)(RT/F)` (10). `[인쇄]` "The linearization step is only done for the parametrization of `i₀₀` by impedance data. If passivating layers of degradation products limit the ion transport towards the interface the resistance determined by `R_SP` (Eq. (5)) governs the interface kinetics at high currents." · "LLZO is a single-ion conductor".

**파라미터**(Table 3, `[인쇄]` — 왼쪽 state-of-the-art / 오른쪽 improved):

| 파라미터 | state-of-the-art | improved | 출처 |
|---|---|---|---|
| NMC811 `d50` | **10 µm** ("Design parameter") | **0.1 µm** ("Desired parameter") | — |
| `D` (cm² s⁻¹) | 2.54 × 10⁻¹² | 2.54 × 10⁻¹¹ | [121a] Ruess 2020(SE 로 잰 다결정 NMC811) / [219] 단결정 |
| `κ` (S cm⁻¹) | 4.54 × 10⁻² | 3.15 | [220] / [209](LCO) |
| **`R_CT`** (Ω cm²) | **2600** | 150 | **[183] Kato 2014**(LCO/LLZO, Nb 코팅 전후) |
| **`R_SP`** (Ω cm²) | **2600** | 0 | [183] |
| `σ⁰_LLZO` (S cm⁻¹) | 8 × 10⁻⁴ | 1.0 × 10⁻² | [27] Neumann 2021 = 큐 55 |
| `β_GB` | 1.39 | 0 | [27] |
| `β_tort` | 2.31 | 1.5 | [27] |

OCV · `D(x)` · `κ(x)`: Figure SI-1 — `[인쇄]` OCV = **Sturm 2019 *JPS* 412, 204(액체 18650 NMC811/SiC 셀 모델)** · `D` = Ruess 2020 · `κ` = Amin 2016 · Noh 2013. `[도표]` SI-1a OCV ≈4.2 → ≈3.5 V(0 → ≈215 mAh g⁻¹), 끝에서 급강하.

**`[재현]` 유효 이온전도도 네 값 — 전부 인쇄와 일치**: `0.25^3.7 × 8e-4` = **4.7 × 10⁻⁶**(인쇄 "5 × 10⁻⁶") · `0.25^2.31 × 8e-4` = **3.3 × 10⁻⁵** ✓ · `0.25^1.5 × 8e-4` = **1.0 × 10⁻⁴** ✓ · `0.25^1.5 × 2e-3` = **2.5 × 10⁻⁴** ✓.
**`[재현]` 유효 전자전도도 — 한 자릿수 어긋남**: `0.75^2.3 × 4.52e-2` = **2.3 × 10⁻²** ↔ `[인쇄]` "κ_eff = **2.3 × 10⁻³** S cm⁻¹"; 같은 문장의 "ohmic loss is only around **50 mV** at 10 mA cm⁻²" 는 2.3 × 10⁻³ 과 맞는다(`[재현]` `I·L/κ` = 0.01 × 0.01/2.3e-3 ≈ 43 mV; 2.3 × 10⁻² 이면 ≈4 mV) — D9.

**결과**(Fig. 9, `[도표]` — 막대 윗변, ±≈10 Wh kg⁻¹; 괄호 안 % 는 그림에 인쇄된 값):

| | 50 µm · 1 mA | 50 µm · 10 mA | 100 µm · 1 mA | 100 µm · 10 mA |
|---|---|---|---|---|
| 이론 | 519 | 519 | 567 | 567 |
| state-of-the-art (회색) | **≈120 (23 %)** | 0 | **≈115 (20 %)** | 0 |
| + LLZO 2차상 `β_SP` 제거 | ≈210 (41 %) | ≈0 | ≈310 (55 %) | ≈0 |
| + CAM\|LLZO 계면(`R_IP`, `R_CT`) | ≈215 | ≈25 (5 %) | ≈315 | ≈15 (3 %) |
| + 복합 굴곡도 `β_tort` 1.5 | ≈220 | ≈50 | ≈330 | ≈62 |
| + NMC811 `D_Li` ×10 | ≈385 | ≈175 | ≈440 | ≈235 |
| + `d50` 0.1 µm | ≈515 (99 %) | ≈485 (93 %) | ≈550 (97 %) | ≈455 (80 %) |
| + 전자 · 이온(σ⁰ 2e-3) | (99 %) | ≈508 (98 %) | (99 %) | ≈555 (98 %) |

⚠ **D1 — 본문의 state-of-the-art 값이 그림과 다르다.** `[인쇄]` "The predicted state-of-the-art specific energy for a cell operated at a current density of **1 mA cm⁻²** is about **24 Wh kg⁻¹ and 15 Wh kg⁻¹** for a composite cathode thicknesses of 50 and 100 µm … about **5 % and 3 %**" ↔ `[도표]` Fig. 9D 1 mA 회색 막대 **≈120 · ≈115 (그림 인쇄 23 % · 20 %)**, 그리고 SI-2 `[인쇄]` "optimum … around 65 vol-% reaching up to **2 times** the specific energy of the configuration presented in the main manuscript" + 최적점 **224 Wh kg⁻¹** ⇒ `[재현]` 본문 구성 ≈112 — **그림 · SI 가 서로 맞고 본문이 ×5–8 작다.** 본문의 5 % · 3 % 는 그림에서 **10 mA 의 계면 개선 막대** 라벨이다.

**스파이더(Fig. 9A · B, `[도표]`)**: 한 번에 한 묶음씩 state-of-the-art 로 되돌린 OAT. **"LLZO\|CAM Charge Transfer (`R_CT`)" 가지는 두 두께 · 두 전류 모두 바깥 테(≈520–580) 근처** — 손실 ≈0; **"Resistive Interphases (`R_IP`, `R_CT`)" 가지는 50 µm · 10 mA 에서 뚜렷이 안쪽**(100 µm 에서는 두 전류 모두 바깥 테 근처 — 원근 그림이라 수치 판독은 하지 않는다). 본문 "Interface processes, namely … resistive interphases … and charge transfer kinetics … also have a prominent effect, though primarily at high current densities" 는 **`R_CT` 단독 가지와 맞지 않는다**(D10). `[재현]` 왜 그런가 — `a` 를 구 기하(`3ε/r`, 미인쇄 가정)로 두면 `a·L` = 3 × 0.75/5 µm × 50 µm ≈ **22.5**(거칠기 인자), 10 mA 에서 국소 전류 ≈4.4 × 10⁻⁴ A cm⁻²: 옴 `R_SP` 2600 → **≈1.2 V**, BV `R_CT` 2600(`i₀` ≈9.9 × 10⁻⁶) → `sinh⁻¹(22)` ≈3.8 → **≈0.20 V**(√c 인자 무시). 즉 **선형(옴) 칸이 결과를 지배하고 BV 칸은 로그로 눌린다** — 본문 `[인쇄]` "close to linear dependence of the overpotential on the current density is expected … Note that in this case the overpotential depends logarithmically on the current" 가 스스로 말한 구조.

**`[인쇄]` 비가법성**: "Note that in this procedure, in addition to the absolute improvements of the individual material properties, **the order of the improvements is also crucial** and has a significant influence on the practical achievable specific energy" — 누적 막대가 순서 의존이라고 저자가 적는다(OAT 의 교호작용 인정, 정량 0).

---

# 3. 절별 해체

## 3.1 서론 (p. 1–2, Fig. 1)
- LLZO 네 장점(전도도 ≤2 mS cm⁻¹ · 공기 가공 · Li 대비 높은 전단 탄성률 · 넓은 창) · 이론 >400 Wh kg⁻¹ · >1000 Wh L⁻¹([2]) "practically achieved energy densities fall short".
- 음극 쪽 진척: Li/LLZO 반쪽 10 mA cm⁻² 실온 "**with no applied pressures**"(Wachsman [4] · Sakamoto [5]) → "the SSB cathode is becoming the next frontier".
- 황화물과의 격차 원인: `[인쇄]` "the ease in composite cathode manufacturing using sulfides (**essentially compaction of mixed powders**) compared to **sintering LLZO and CAM** in a composite cathode 3D structure".
- 목표 저항: `[인쇄]` 10 mA cm⁻² + 에너지 효율 ⇒ "internal cell resistance of less than **30 Ω cm²**"([7] Randau 2020).
- Fig. 1(`[도표]` 봤다): 세 계면(석류석\|석류석 · 양극\|양극 · 석류석\|양극) 아이콘 — 이종 계면에 "Differential Expansion" · "Mechanical Stability" · "Ion Interdiffusion" · "Secondary Phases" · "Charge Transfer Resistance" · "Electrochemical Stability". 공정 ↔ 운전 시점 구분 **없음**, 흰 원 = 기공. 모식도.

## 3.2 §2 전해질 내부 계면 (p. 2–6, Fig. 2)
입계 구조(TEM 두께 ≈1.5 nm ↔ 2차상 보고) · 가압 소결은 2차상 적다 · 방위차 평균 ≈39° · 공간전하층 연속체 모델 · 미세구조 5 인자(입경 · 부피분율 · 퍼콜레이션 · 협착 · 굴곡도, [26]) · 계산 5 부류(영상 재구성 · 구 무작위 배치 [32] · DEM [33] · 상장 [34] · MC [35]) · 도펀트(Ta · Nb ↔ Al · Ga 액상 소결 · 이상 입성장) · Li 손실(Li₂O 증발 → La₂Zr₂O₇). **카드와 무관 — 세지 않는다.** Fig. 2 는 안 봤다.

## 3.3 §3 공정 중 SE/CAM 계면 (p. 7–12, Table 1, Fig. 3)
- `[인쇄]` "Due to their rigid nature, **sintering is generally required to establish intimate contact** between the garnet-type SEs and CAMs."
- Table 1(텍스트로 읽음): CAM × 석류석 조합 22 행 — 반응 개시 온도 **<300 °C**(스퍼터 LCO 박막 [64]) ~ **900 °C 안정**([59]) · 생성물 La₂Zr₂O₇ · LaCoO₃ · 정방정 LLZO 등. LCO 가 가장 안정, LMO · LFP 는 500 °C 위에서 분해.
- §3.2 냉각 응력 → 계면 균열 → "reduction in electrochemically active surface area"(판정 참조).
- §3.3 공정 처방: 소결조제(Li₃BO₃ · LiBO₂ · Li₂SiO₃ · Li₃PO₄) · LCBO(Han [95], 20 µm · 0.1 mAh cm⁻² · 100 °C, 온도 의존 감쇠) · 자유 소결 LCO–LLZO(Finsterbusch & Danner [12], 1050 °C 30 분 ≈80 % 밀도, 0.84 mAh cm⁻², 100 °C) → Tsai [83] 1.62 mAh cm⁻² @50 °C, **둘 다 50–60 %/50 사이클, "mechanical failure … identified as origin"** · FAST/SPS [11,96](650–700 °C 10 분 · ≈95 %, TEM 상 2차상 없음, 1.2 mAh cm⁻² @80 °C) — "fast degradation … often losing up to 10 % capacity per cycle … cracking … ruled out … first evidence of an electrochemical degradation".
- `[인쇄]` "There does not exist any continuum level model that captures the interdiffusion of ions and formation of the passivation layers between CAM and LLZO at higher voltages."

## 3.4 §4 운전 중 SE/CAM 계면 (p. 12–15, Fig. 4)
- §4.1: LCO/LLZO 전하이동 저항 "**1–5 kΩ cm²**"(인용 0), "very likely includes contributions of processing-induced secondary phases". LiPON 박막전지 "up to 10000 cycles … only 10 % capacity loss"([102]).
- §4.2 두 영역 · 두 범주(전기화학 = 산화 + 상호확산 · 기계 = CAM 수축/팽창) — 판정 참조.
- §4.2.1: LLZO 산화 3.5 V vs Li(Wagemaker [111] — LLZO-C 복합체) · Ihrig [11] 치밀 셀에서 "cation diffusion … and a loss of crystallinity for LLZO close to the interface" · `[인쇄]` "Presently, continuum level modeling cannot capture the formation of the passivation layers during operation at high voltages."
- §4.2.2 기계: 균열 세 자리(LLZO 입계 · CAM 입계 · LLZO/CAM 이종 계면) · `[인쇄]` "The resulting cracks can hinder the transport of Li ions in the bulk of LLZO by detaching one grain from the other, **or reduce the electrochemically active surface area by delaminating the electrode from the LLZO electrolyte**." · SE 는 균열을 채우지 못한다 → "isolation of particles"([122]) · "There is yet no experimental study that incorporates percolation theory …" · Bucci [126] 7.5 % · Tsai [83] 균열 · Mücke [108] · Barai [127] 10 사이클.
- **Fig. 4(`[도표]` 봤다)**:
  - (a) 원전 [11] — 60 사이클 충 · 방 곡선, **축 "Voltage (V vs In-Li)" 2.8–3.6 V**(캡션 "Li metal anode" 와 어긋남 — D8), 첫 충전(빨강) ≈1.15 mAh cm⁻², 방전 끝 ≈0.9 → 마지막 ≈0.25 mAh cm⁻²(60 사이클). 본문 "1.2 to 0.8 within the first 5 cycles" 는 **[105]** 를 인용하면서 **Figure 4a([11])** 를 가리킨다(D11).
  - (e) 원전 [107] — `ΔV/V₀` vs `x(Li)`: **NCM-811 ≈−6.5 % @x≈0.15** · NCA ≈−5.7 % · NCM-622 ≈−4.8 % · NCM-111 ≈−2.5 % @x≈0.25 · **LCO +2 % @x≈0.6 뒤 감소**(≈+0.6 % @x≈0.47).
  - (f) 원전 [108] — 정렬 이방 LCO 복합체 최대주응력: **cath. LLZO +1.06 ± 0.54 GPa(인장)** · cath. LCO −0.48 ± 0.26 · separator −0.41 ± 0.08 GPa.
  - `[해석]` **Bucci 문턱 7.5 % 를 (e) 에 대면 그려진 CAM 어느 것도 문턱에 닿지 않는다**(최대 NCM811 ≈6.5 %, LCO 는 최대 +2 % 팽창) — 그런데 박리 · 균열 보고는 **LCO**/LLZO 에서 온다([83]). 이 편은 문턱 · 곡선 · 관측을 나란히 두고 맞추지 않는다(D12). (f) 의 LLZO 인장 ≈1 GPa 는 파괴강도 100–150 MPa 의 ≈7–10 배 — 문턱을 쓰지 않아도 균열이 예측되는 쪽은 **응력 쪽 서술**이다.

## 3.5 §5 황화물 · 폴리머와의 대조 (p. 15–17, Fig. 5, Table 2)
- Table 2: 영률 NCM111 199 · **LLZO:Al 163** · Li₆PS₅Cl **22** · LiPON 77 GPa.
- §5.2 판정 참조(첫 사이클 · >10 MPa · "not understood yet … sintered oxide-oxide cathodes").
- **Fig. 5(`[도표]` 봤다)**: (a,b) β-Li₃PS₄/NCM811 입자 둘레 틈(캡션 "after 50 cycles", 원전 [103] = 23호) · (c) ToF-SIMS 0 ↔ 100 사이클, VGCF 유무(원전 [142b] Walther 2020) — PO₂⁻·PO₃⁻ 가 입자 둘레에 증가. ⚠ 본문은 매핑을 "(Figure 5b)" 로, 캡션은 "(c)" 로 적는다(D13, 사소).
- `[인쇄]` "While it is a priori difficult to separate chemical and electrochemical degradation due to the similar nature and difficult interface accessibility in composite electrodes …" — 분리 불가의 서술(황화물).

## 3.6 §6 혼성(액체 · 겔 · 폴리머) (p. 17–20, Fig. 6) — 카드와 무관. Fig. 6 안 봤다.

## 3.7 §7.1–7.3 전고체 구조 (p. 20–23, Fig. 7)
- 3층 · 2층 LLZO(Hitz [4]) · 역전 2층 · 공소결 테이프(Rosen [104], 구배 LCO:LLZO 2:1 → 1:2) · 이용률 "improved by a factor of 2, reaching almost 100 % … (3 mAh cm⁻²)".
- §7.1.1 `[인쇄]` "the volume changes cause mechanical damage to CAM particles as well as **delamination and contact loss with SE**" · FIB-SEM 재구성 모의가 실온 실험보다 좋다 → "unaccounted secondary reactions at the CAM/SE interface"([12]).
- §7.2 이상 계면층 9 조건 — "(6) High fracture energy … to minimize interfacial delamination and loss of electrochemically active surface".
- **Fig. 7(`[도표]` 봤다)**: (a–c) 3층 · 2층 모식도 · (d) **공소결 LCO 첫 방전 곡선 셋**(200 µm 균일 ≈11 % · 70 µm 균일 ≈72 % · 70 µm 구배 ≈100 % 이론 용량) vs V vs Li/Li⁺ 3.2–4.0 V · SEM 단면. **사이클 데이터 없음** — §4.2 "drop to 1.3 mAh cm⁻² after only 10 cycles (see Figure 7d)" 와 어긋남(D4).

## 3.8 §7.4 에너지 밀도 (p. 23–28, Fig. 8, 9, Table 3; SI §1 · §2)
§2 참조. Fig. 8 안 봤다(캡션 · SI §1 절차로 대체). SI-2(`[도표]` 봤다, 수동 크롭): 이론 최적 567 Wh kg⁻¹(75 vol% · 100 µm) ↔ state-of-the-art 1 mA 최적 **224 Wh kg⁻¹ @65 vol% · 100 µm**, 75 vol% 쪽은 급락(색 띠 ≈100–118).

## 3.9 §8 결론 (p. 28–29)
- `[인쇄]` "the evolution of the SE/CAM interface during operation needs to be studied in terms of electro-chemo-mechanically induced degradation" · 운용 처방 "by limiting it to upper or lower cutoff potentials" · operando 필요 · "reconstructed microstructures of real cells as input parameters for continuum modeling".
- `[인쇄]` "our modeling shows that the Li-ion diffusion length in intercalation cathodes is more critical in SSBs than in cells with LE, **because the SE will not flow to fill the cracks formed in the CAM particles**" — ⚠ 자기 P2D 에는 균열이 없다(`D` 를 문헌값으로 낮췄을 뿐, "mechanical degradation processes are … neglected") — 결론 문장의 "because" 는 모델의 출력이 아니다(D14).

---

# 4. Q1 판정 표 — 이 편 안의 `N` 축

| 항목 | 이 편 | 출처 층위 |
|---|---|---|
| 자기 측정 | 0 | — |
| 자기 모델의 `θ` | **≡ 1**(퍼콜레이션 · 치밀 가정) · 열화 무시 | `[인쇄]` SI §2.1 |
| 사이클 축 모델 | [127] "ten cycles without showing saturation" | 재인용 한 문장 |
| 사이클 용량 곡선(산화물) | [83] 1.8 → 0.4 / 100 · [104] 2.75 → 1.3 / 10 · [105] 1.2 → 0.8 / 5 · [12]/[83] 50–60 % / 50 · Fig. 4a([11]) `[도표]` ≈0.9 → ≈0.25 / 60 | 재인용 · 그림 1 |
| 원인 배정 | 첫 사이클 = 산화 · 이후 = 피로 + 활성 면적 손실(인용 0) · [105] 치밀 셀 = 전기화학("cracking … ruled out") | 서술 |
| 접촉 분율 · 면적 수치 | **0** | — |
| 공백의 인쇄 | "no experimental study that incorporates percolation theory" · "no experimental technique … fracture strength between CAM and SE" | `[인쇄]` |

⇒ **Q1 칸 이동 없음 — 층 하나: "`θ(N)` 측정이 없다는 것을 종설이 인쇄했다(2022)".** 02호가 이 편에서 기대한 동역학은 **이 편 안에 없고**, 이 편은 그것이 **당시 문헌에도 없다**고 적는다.

---

# 5. 계보 대조 — 02호가 ref 17 로 매단 것

| 02호 문장(ref 17) | 이 편에 있나 |
|---|---|
| "the cathode is prone to electrochemical and mechanical degradation during cell manufacturing and operation … secondary phases and voids"(ref 17, 21) | ✅ §3 · §4.2 두 범주 — 그대로 선다 |
| "pore formation and contact loss between individual particles can also result from mechanical degradation due to volume changes of the CAM during operation"(ref 17) | ✅ **서술로** §4.2.2 · §7.1.1 — 단 이 편 자신의 근거도 재인용(Tsai [83] 균열 · Barai [127] 모의)이고 **접촉 분율 0**. "pore formation" 은 이 편에서 **냉각 · 소결 단계**(§3.2 · [204])에 더 많이 붙는다 |
| "large surface area and short transport paths"(ref 17) | ✅ §7.1 "the electrochemically active surface area between the CAM and LLZO should be maximized" |
| "single-crystal NMC, conducting additives"(ref 17, 71) | ✅ §7.4.2 단결정 `D` ×10([219]) · §7.3 MIEC/도전재 — 단 이 편 결론은 도전재를 **없애는 쪽**("the preferred solution … is to remove the conductive additives completely")이다. 02호가 "adding conducting additives" 로 옮긴 것은 ⚠ **약한 판**(이 편은 도전재를 에너지 밀도 손실로 보고 MIEC 대체를 선호, "Even small amounts of this critical additive significantly reduce cell energy density") |

⇒ `[해석]` 02호는 이 편을 **동역학(시간축) 근거가 아니라 "그런 일이 있다" 는 서술 근거**로 썼고, 그 쓰임은 선다. 원장이 붙인 "`θ(N)` 시간축의 입구" 라는 기대는 02호 문장이 아니라 **우리가 붙인 기대**였다.

---

# 6. 곱 축퇴 처방 — 서른여섯 번째 적용

| 단계 | 입력 | 판정 |
|---|---|---|
| **1단계** `R`·`C` | `R_CT` · `R_SP` 문헌값(2600 · 2600 / 150 · 0), `C` 0 | ❌ |
| **2단계** 면적 대조군 | `d50` 10 → 0.1 µm(`a` 정의 미인쇄 — 구 기하면 면적 ×100 과 확산 길이 ×1/100 이 **한 손잡이**) | ❌(교락) |
| **3단계-a** `Ea` | 실온 한 온도(인용 [95] 25 ↔ 100 °C 감쇠 차는 서술) | ❌ |
| **3단계-b** `C` 상한 | 없음 | ❌ |
| **4단계** 시간 영역 | 없음 | ❌ |

**곱이 선 자리**: 계면 과전압 `η_int = f_BV(i/(a·i₀₀)) + (i/a)·R_SP`. 면적 `a` 는 **두 계면 항 모두에 나눗셈으로** 들어간다 — `a·i₀₀`(37호 `A_eff·k` 항등)과 `a/R_SP`(직렬 옴). 두 항은 **전류 의존이 다르다**(로그 ↔ 선형) — 저자가 `[인쇄]` 그 차이를 적고("close to linear dependence … depends logarithmically") 곧바로 "**Deconvolution of the contributions in impedance data is challenging** … we assume that most of the interfacial impedance can be attributed to resistive secondary phases" 로 **가정해 버린다**.

⇒ **이 적용이 처방에 더하는 것**:
1. **새 줄 "전류 진폭(선형 ↔ 로그) — 직렬 `R_SP` ↔ `R_CT` 를 가르고, 면적은 둘 다에 남는다"**. 소신호 EIS 는 두 저항을 합으로만 본다(선형화 영역에서 둘 다 옴). 진폭 스윕(또는 펄스 전류 여러 개)이 두 칸을 가른다 — 49호 `[재현]` 진폭 의존(10 s 창 ×1.46)의 **계면 판**. 면적(접촉)은 여전히 두 칸 모두의 공통 인자라 `a` 는 따로 필요하다(1 · 2단계).
2. **"입경" 손잡이는 곱이다** — 50호 `a_v = 3ε/r` 규약을 쓰는 모델에서 `d50` 스윕은 확산 길이와 계면 면적을 같이 움직인다. 이 편 Fig. 9 의 "Reduce NMC811 Particle Size (`d50`)" 이득(`[도표]` 10 mA 50 µm ≈175 → ≈485)은 **"확산 길이" 라는 이름표가 붙은 곱**이다(`a` 정의가 인쇄되지 않아 판정은 조건부).
3. `[재현]` **면적형 접촉 손실의 가시성은 계면 체제가 정한다** — 이 편 state-of-the-art(`R_SP` 2600, `a·L` ≈22.5 가정)에서 `a` 를 반으로 줄이면 10 mA 옴 몫이 ≈1.2 → ≈2.3 V 로 뛰지만, improved(`R_CT` 150 · `R_SP` 0 · `d50` 0.1 µm → `a·L` ≈2250)에서는 10 mA 국소 전류 ≈4.4 × 10⁻⁶ A cm⁻² ↔ `i₀` ≈1.7 × 10⁻⁴ ⇒ `η` ≈0.7 mV — **`a` 가 반이 돼도 전압에 안 보인다.** 그 체제의 접촉 손실은 **고립(`u`, 용량 쪽)** 으로만 보인다. `[해석]` 합성 truth 를 이 편의 "improved" 파라미터로 만들면 면적형 접촉 손실은 정의상 비가시다 — truth 설계 때 계면 체제를 먼저 정한다.

⚠ **이것이 곱을 푼 것은 아니다**: 식에서 읽은 구조 + 우리 계산(`a` 구 기하 가정). 저자는 진폭 채널을 쓰지 않았다.

---

# 7. 37호(Li 2024) 대조 — 두 자리

| | 37호 Li 2024 | 이 편(Ren · Danner 2022) |
|---|---|---|
| ① `ε_p` = `LAM_PE` 동어반복 | 노화를 `ε_p(N)` 로 — 정의상 `LAM_PE` | **없음** — `ε_CAM` 75 vol% 고정, 열화 무시 |
| ② `A_eff·k_p` 곱 | BV 분모에 `A_eff`, 균일 표면 전류 가정 | **`a·i₀₀`**(`a` 미정의) — 같은 곱. 그리고 **③ `a/R_SP` 직렬 옴** 이 더 있다 |
| 서술이 가리키는 자리 | — | ① 대신 **고립**(`u` — [122] · [108]) · ② **활성 면적**([32]) — 두 낱말 구분 없음 |
| 제안 | — | 미세구조 분해 + 역학 결합(1 · 2호 형), `ε_p` 경로 제안 0 |

⇒ `[해석]` DLR 계열은 **접촉을 기하(연결 · 면적)로 다루는 쪽**이고 `ε_p` 동어반복 경로를 안 쓴다 — 우리 truth 생성기에 옮길 때 가장 가까운 자리는 **1 · 2호 `θ` 연결 분율(용량)** 과 **`a` 면적(동역학)** 두 칸을 따로 두는 것이다. 이 편이 두 낱말을 섞어 쓰는 것은 그 두 칸이 **서명이 다르다는 것**(용량 ↔ 율 의존 과전압)을 지면에서 가르지 않았다는 뜻이다.

---

# 8. Q2 · Q3 · Q4 · Q5 · Q6 · Q7 · Q8

- **Q2 반 칸 검토 후 접음.** 산화물에는 **공정으로 기계 기구를 끄는 조작**(FAST/SPS 치밀 ≈95 % ↔ 자유 소결 ≈80 %)이 있고, 이 편은 그 대조의 결과("cracking … ruled out … electrochemical degradation")를 옮긴다 — 황화물 재가압(4호)과 **반대 방향의 조작**(접촉 손실을 되돌리는 대신 애초에 막는다). 그러나 근거 채널 · n · 수치가 이 편에 없다(G3) → 원전 [105] 열람 대상.
- **Q3 층 하나: "계 간 이식 파라미터(cross-system transplant)"** — `[인쇄]` "An interface impedance of about 2600 Ω cm² between LCO and LLZO has been reported … Ruess et al. measured a similar interfacial resistance for their NMC811-containing cells with an **agyrodite**-type SE. **In the absence of data on NMC811/LLZO interfaces, we define this resistance as the state of the art**" — NMC811/LLZO 셀의 계면 저항 = LCO/LLZO 값 + 황화물 NMC811 값의 "similar". OCV 는 액체 18650 모델 곡선.
- **Q4 0/53 — 마흔다섯 번째 성질 "분해 불가를 인쇄하고 가정으로 한쪽에 몰았는데, 표는 두 칸에 같은 값을 넣었다"**: `[인쇄]` "Deconvolution of the contributions in impedance data is challenging. In the state-of-the-art case, we assume that most of the interfacial impedance can be attributed to resistive secondary phases" ↔ Table 3 `R_CT` 2600 = `R_SP` 2600(D3). 그리고 OAT 스파이더를 "sensitivity analysis" 로 부르며 순서 의존("the order of the improvements is also crucial")을 인쇄한다 — 교호작용을 인정하고 재지 않는다. 식별성 낱말 0.
- **Q5 해당 없음 + 어긋남 하나**: 산화물 셀은 Li 금속 음극 설계. ⚠ 재수록 Fig. 4a 축 "V vs In-Li" ↔ 캡션 "Li metal anode"(D8) — 영점이 두 개로 적혀 있다. 반 칸 검토 대상 아님(측정 · 명제 0, 래스터 판독).
- **Q6 없음**: 산화물 셀 운전 압력 0. 황화물 ">10 MPa … impractical" 한 줄 · 음극 반쪽 "no applied pressures".
- **Q7 해당 없음**(Li 금속 · 무음극 0).
- **Q8 부분**: NMC811 OCV(SI-1a, 액체 원전) · LCO · NMC622 · NMC811 평균 방전 전압(SI §1.3, 3.96 · 3.82 · 3.86 V, 3–4.3 V 창). ASSB 에서 잰 OCP 0.

---

# 9. 채움표 행 (Q1–Q8)

| Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 |
|---|---|---|---|---|---|---|---|
| **없다 — `θ(N)` 0/53** · 자기 P2D `θ ≡ 1`(퍼콜레이션 · 치밀 · 열화 무시 인쇄) · **공백을 인쇄**("no experimental study that incorporates percolation theory") · `N` 축 모델 1([127], 한 문장) · 산화물 용량 곡선 재인용 4 | 반 칸 검토 후 접음 — FAST/SPS 치밀 셀 "cracking … ruled out"(공정으로 기계 기구를 끈 대조, 재인용) | 층 하나: **계 간 이식 파라미터**(LCO/LLZO + 황화물 NMC811 → NMC811/LLZO) · 결정론 사례 계산 | **0/53 — 마흔다섯 번째 성질** | 해당 없음(⚠ Fig. 4a 축 In-Li ↔ 캡션 Li) | 없음(산화물 운전 압력 0) | 해당 없음 | 부분 — NMC811 OCV = 액체 원전 곡선 |

---

# 10. 어긋남 (실제로 어긋난 것만)

| # | 어긋남 | 무게 |
|---|---|---|
| **D1** | 본문 state-of-the-art 1 mA "≈24 · 15 Wh kg⁻¹ (5 % · 3 %)" ↔ Fig. 9D 회색 `[도표]` ≈120 · ≈115(인쇄 23 % · 20 %) ↔ SI-2 "2 times … 224" ⇒ `[재현]` ≈112 — 그림 · SI 일치, 본문 ×5–8 | ★★★ |
| **D2** | §4.2 첫 사이클 = 산화 · 이후 = 접촉 피로([83,103] · 피로 문장 인용 0) ↔ [103] = 23호 원문 "contact loss should only occur during the initial charge … ongoing … interphase" ↔ 같은 편 §5.2 "Koerver … link this phenomenon to an irreversible resistance increase in the first cycle" | ★★★ |
| **D3** | "most of the interfacial impedance … resistive secondary phases"(총 ≈2600) ↔ Table 3 `R_CT` 2600 **+** `R_SP` 2600 | ★★ |
| **D4** | §4.2 "2.75 → 1.3 mAh cm⁻² after only 10 cycles (see Figure 7d)" ↔ `[도표]` Fig. 7d 첫 방전 곡선 셋, 사이클 0 | ★★ |
| **D5** | SI 식 (1)·(2) 의 `a` 정의 없음 | ★★ |
| **D6** | `d50` 한 손잡이가 확산 길이와 (구 기하라면) 계면 면적을 같이 움직이는데 이름은 "CAM Li Diffusion Length" | ★★ `[해석]` |
| **D7** | [83] 초기 용량 §3.3 1.62 mAh cm⁻² ↔ §4.2 1.8 mAh cm⁻² | ★ |
| **D8** | Fig. 4a 캡션 "Li metal anode" ↔ `[도표]` 축 "V vs In-Li" | ★★ |
| **D9** | κ_eff `[재현]` 0.75^2.3 × 4.52 × 10⁻² = 2.3 × 10⁻² ↔ 인쇄 2.3 × 10⁻³(50 mV 는 후자와 맞음) · Table 3 4.54 ↔ 본문 4.52 × 10⁻² | ★★ |
| **D10** | "charge transfer kinetics … prominent effect" ↔ `[도표]` 스파이더 `R_CT` 단독 가지 손실 ≈0(두 두께 · 두 전류) | ★★ |
| **D11** | "1.2 to 0.8 mAh cm⁻² within the first 5 cycles (Figure 4a).[105]" ↔ Fig. 4a 원전 [11] · `[도표]` 첫 방전 ≈0.9 | ★ |
| **D12** | Bucci 문턱 7.5 % ↔ Fig. 4e 최대 수축 NCM811 ≈6.5 % · LCO 는 팽창 — 그런데 균열 보고는 LCO/LLZO([83]) | ★★ `[해석]` |
| **D13** | ToF-SIMS 매핑 본문 "(Figure 5b)" ↔ 캡션 "(c)" | · |
| **D14** | 결론 "our modeling shows … because the SE will not flow to fill the cracks" ↔ 모델에 균열 없음(`D` 문헌값 · 기계 열화 무시) | ★★ |
| D15 | 기호: Fig. 9 `R_IP` · `β_SP` ↔ Table 3 · SI `R_SP` · `β_GB`; SI "Figure 7.3d" = 본문 Fig. 9D; §4.2 [56a,103] 을 "oxidation of LLZO by the CAMs" 에 — [103] 은 황화물 | · |

---

# 11. 그림 — 무엇을 봤나

크로퍼 13 장(본문 그림 9 + 표 3 + SI 표 1) + **수동 크롭 2 장**(SI-1 · SI-2 — 크로퍼가 SI p12 를 "그래픽 없음" 으로 제외). **Read 7 장**: Fig. 1 · 4 · 5 · 7 · 9 · SI-1(쪽 렌더) · SI-2(크롭). 표 1 · 2 · 3 · SI 표 1 은 PDF 텍스트로 읽었다(이미지로 안 봄). **안 본 것**: Fig. 2(입계 실험 · 이론 모식) · Fig. 3(LCO/LLZO 공정 반응 TEM · 광학 · XAS) · Fig. 6(혼성 계면) · Fig. 8(셀 설계 · 이론 에너지 밀도 곡선). 그림 판독 ±≈10 Wh kg⁻¹(Fig. 9D) · ±≈0.05 mAh cm⁻²(Fig. 4a) · ±≈0.3 %(Fig. 4e).

---

# 12. 참고문헌 중 후속 후보 (222 번호, 서지 기준 — 미열람)

| 서지 | ref | 왜 | 축 |
|---|---|---|---|
| **Barai, Rojas, Narayanan, Ngo, Curtiss, Srinivasan 2021 *Chem. Mater.* 33, 5527** | [127] | **사이클 축 박리 모델** — "ten cycles without showing saturation" · `θ(N)` 모델 원전 후보 | Q1 ★★★★ |
| **Ihrig … Guillon 2021 *J. Power Sources* 482, 228905** | [105] | 치밀 FAST/SPS — 기계 기구 배제 대조 · 1.2 → 0.8 / 5 사이클 | Q2 · Q1 ★★★ |
| **Tsai … Guillon 2019 *Sustain. Energy Fuels* 3, 280** | [83] | LCO/LLZO 사이클 감쇠 + 사후 균열 · "ASR from electrodes" | Q1 ★★★ |
| **Neumann, Randau, …, Danner, …, Janek, Latz 2020 *ACS AMI* 12, 9277** | [32] | "loss of contact → decrease in electrochemically active surface area → R_ct ↑, voltage and capacity fade" — DLR 면적 자리 원전 | Q1 · 곱 ★★★ |
| **Finsterbusch, Danner, Tsai, Uhlenbruck, Latz, Guillon 2018 *ACS AMI* 10, 22329** | [12] | LCO–LLZO 실험 + 3D 미세구조 모델, 50–60 % / 50 사이클 | Q1 · Q3 ★★ |
| Ihrig … Guillon 2022 *ACS AMI* 14, 11288 | [11] | Fig. 4a–d 원전 — TEM 전후 · 전기화학 열화(축 In-Li?) | Q2 · Q5 ★★ |
| Bucci … Carter 2018 *Phys. Rev. Mater.* 2, 105407 | [126] | 박리 문턱 7.5 % (cohesive zone) | Q1 ★★ |
| Mücke … Guillon 2021 *J. Power Sources* 489, 229430 | [108] | 3D 응력 · "ionic isolation of regions" | Q1 ★★ |
| Rosen … Fattakhova-Rohlfing 2022 *J. Mater. Chem. A* 10, 2320 | [104] | 테이프 공소결 · 2.75 → 1.3 / 10 사이클 | Q1 ★★ |
| Yu … Sakamoto, Thornton 2019 *J. Power Sources* 440, 227116 | [82] | 냉각 열응력 ≈1 GPa — 제조 단계 `θ₀` | Q1 ★ |
| Kato … Iriyama 2014 *J. Power Sources* 260, 292 | [183] | `R_CT` 2600 / 150 Ω cm² 의 출처 | Q3 ★ |
| Koerver … Janek 2018 *EES* 11, 2142 | [107] | CAM 부피 변화 곡선(Fig. 4e) | Q1 ★ |
| Randau … Janek 2020 *Nat. Energy* 5, 259 | [7] | 30 Ω cm² 목표 | · |

**큐 55–59**: 55 Neumann 2021 = [27] ✅ · 56 Hlushkou 2018 ❌ · 57 Bielefeld 2022 = [203] ✅ · 58 Bielefeld 2020 = [151b] ✅ · 59 Asheri 2023 ❌.

---

# 13. 이 digest 가 주장하지 않는 것

- **인용된 원전의 내용을 확인하지 않았다.** §판정 (a) 목록은 이 편이 원전에 매단 문장이다 — [127] 이 `θ(N)` 을 무엇으로 정의하는지, [105] 의 "ruled out" 근거가 무엇인지는 원전 열람 전까지 모른다.
- **산화물에서 접촉 손실이 제조 단계에 실제로 생긴다고 주장하지 않는다** — 이 편은 "possible"(모의 응력 ↔ 파괴강도)까지이고, `[재현]` 열응력 추정도 1축 근사다.
- **§4.2 의 시간 배정이 산화물에서 틀렸다고 주장하지 않는다.** 산화물(소결 결합 · 강체)과 황화물(압착 · 연성)은 물리가 달라 배정이 다를 수 있다. 주장은 "인용 [103] 이 반대 배정을 가진 황화물 원전이고, 산화물 피로 문장에는 인용이 없다" 까지다.
- **Fig. 9 값의 D1 에서 어느 쪽이 맞는지 판정하지 않는다** — 그림 · SI 가 서로 맞는다는 것까지다.
- `[재현]` 계면 체제 계산(§2 · §6)은 **`a` = 구 기하 가정** 위에 있다. 원문은 `a` 를 정의하지 않았다.

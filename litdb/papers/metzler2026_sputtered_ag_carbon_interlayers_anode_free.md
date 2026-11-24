<!-- digest 표준 양식 (paper-level STANDALONE) · 깊이 본 = zuo2022_chlorination_cathode_interface.md · 같은 계열 꼴 = spencerjolly2023_ag_graphite_interlayer_operando_xrd.md · kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode.md
     작성 2026-11-24 — 병렬 세션 (이 파일과 litdb/figures/<slug>/ 만 쓴다 · INDEX · comparison 은 메인 세션이 합친다 · git 안 씀).
     원문 = 본문 11 쪽 (ACS Appl. Energy Mater. 9, 9817–9827 · CC-BY 4.0) + SI 18 쪽 (그림 S1–S12 · 표 S1) — 글자 층 전부 읽음 + 그림 17 장 전부 Read 로 렌더해 실독 (표 S1 은 PDF 글자로 옮김).
     쪽 표기 = "p.N" 본문 PDF N 쪽 (인쇄 쪽 = 9816 + N) · "SI S-N" = SI PDF N 쪽 (인쇄 S-N 과 같다).  figures.json 의 page 는 PDF 쪽.
     값 표지: [인쇄] = 본문 · SI · 표 · 그림 안 글자로 적힌 값 · figure-read ≈ = 그림에서 읽은 값 (축 눈금 · 축척 막대 · 픽셀) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산 (식 병기) ·
     [가정] = 원문에 없는 상수를 카드가 넣음 · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = litdb 다른 카드의 값 (slug 병기) · [미확인] = 본문 + SI 전수에 없음.
     우리 점착 (W) 값은 이 카드에 싣지 않는다 — 위치만 (병렬 규칙 4).  이 논문에 DFT · MD · 연속체 모델은 없다 (실험 전용). -->

# 얇은 스퍼터 Ag (≈100 nm) + 상용 탄소 (≈1 µm) 2 층이 무음극 Li₆PS₅Cl 전지의 Li 석출을 돕는다 — Li 는 **Cu | C 사이**에 쌓여 C 를 SE 쪽으로 밀어내고, Ag 는 Li 속으로 흩어졌다가 방전 뒤 **C 위**에 남는다 · 핵생성 과전압 16.1 → 3.9 mV · 첫 방전 163 → 203 mAh g⁻¹ — Metzler · Doerrer · Matthews · Sun · Liotti · Grant (*ACS Appl. Energy Mater.* 9, 9817 (2026))

> slug `metzler2026_sputtered_ag_carbon_interlayers_anode_free` · DOI `10.1021/acsaem.6c01118` · type `exp (스퍼터 Ag 박막 on 상용 탄소 코팅 Cu 집전체 · Li₆PS₅Cl 펠릿 무음극 풀 셀 + 3 전극 반쪽 셀 · P-FIB 단면 SEM/EDS · SIMS · Raman · 광학 조도 · EIS) — 원자단위 계산 · 모델 0` · PDF `litdb/inbox/sputag2026_ag_c_sputtered_main.pdf` (본문 11 pp) + SI `litdb/inbox/sputag2026_ag_c_sputtered_SI.pdf` (18 pp · 그림 S1–S12 · 표 S1) · digested `2026-11-24` · status ✅
> elements: Li, Ag, C, Cu, P, S, Cl
> methods: Raman

> **저자**: **Michael Metzler** (1저자) · Christopher Doerrer · Guillaume Matthews · Yige Sun · Enzo Liotti · **Patrick S. Grant\*** (교신 · patrick.grant@materials.ox.ac.uk) — Department of Materials, University of Oxford · The Faraday Institution (Harwell Campus) · Doerrer 는 Department of Mechanical and Industrial Engineering, University of Toronto 겸 · *ACS Appl. Energy Mater.* **2026**, **9**, **9817–9827** (Article · 9 권 15 호) · 받음 2026-03-31 · 고침 2026-06-27 · 승인 2026-07-02 · 출판 2026-07-21 · **CC-BY 4.0** · 연구비 Faraday Institution NEXTRODE (FIRG066/090) · SOLBAT (FIRG022) · Henry Royce Institute (EPSRC EP/R010145, 장비) · 이해 상충 없음 · 키워드 *sputtering, anode-free, silver-carbon layer, secondary-ion mass spectrometry, solid-state battery manufacturing*
> **기여 (원문 p.9)**: M.M. 전 과정 · 원고 / C.D. 실험 설계 · 해석 / G.M. + M.M. 단면 식각 · SEM/EDX / Y.S. + M.M. PFIB/SIMS / 구상 M.M. + P.S.G. · 공동 지도 E.L. + P.S.G.
> **이웃 카드 (링크만)**: [`spencerjolly2023_ag_graphite_interlayer_operando_xrd`](spencerjolly2023_ag_graphite_interlayer_operando_xrd.md) (이 논문 ref 23 · 같은 Oxford 라인 · Ag–흑연 층의 상 변화를 operando XRD 로 — 이 논문이 기전 설명을 거기에 기댄다) · `metzler2025_ag_particle_distribution_carbon_interlayer_anode_free` (ref 30 · SI ref S16 · 같은 1저자 전작 — 셀 꼴 · SIMS 기준 이중층 · Li 두께 산식의 원전 · 다른 세션이 정리 중이라 링크 대신 slug 만) · [`doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density`](doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density.md) (ref 36 · 같은 랩 셀 장치 · 같은 단결정 NMC83 · 같은 140 rpm 30 min 혼합 · 같은 PEEK Ø 5 mm 500 MPa) · [`kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode`](kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode.md) (Ag–C + CNF 2 층 · 탄소 결정성 Raman 대조) · [`liao2025_interfacial_adhesion_li_plating_carbon_interlayer`](liao2025_interfacial_adhesion_li_plating_carbon_interlayer.md) (탄소 인터레이어 점착 ↔ Li 석출 위치) · [`ahn2026_cej_agno3_pvp_li3n_anodefree`](ahn2026_cej_agno3_pvp_li3n_anodefree.md) (Ag 전구체 무음극).

> **실제로 본 그림 (2026-11-24 · Read 로 렌더)**: `Fig. 1` `Fig. 2` `Fig. 3` `Fig. 4` `Fig. 5` + `Fig. S1`–`Fig. S12` = **17 장 전부**.  확대해서 다시 본 것 (scratchpad 사본 · 저장소에 안 남김): `Fig. 1d` · `Fig. 3h` · `Fig. S2a`.
> 안 본 것: `Table S1` 이미지 (표는 PDF 글자로 옮겼다 — 글자가 정확하다).  크롭 = 도구 18 개 (그림 17 + 표 1) · `missing_labels` 없음 · 손 크롭 0.
> 그림에서만 읽은 값은 **`figure-read ≈`** 로 표시했다.  그림 판독이 본문 서술과 어긋난 곳은 §10 에 모았다.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: MTI 상용 탄소 코팅 Cu 박 (Cu 9 µm + *"fine particulate C"* ∼1 µm) 위에 Ag 를 ≈100 nm (BSE 실측 89.32 nm) 스퍼터해 Li₆PS₅Cl (≈1 mm) 펠릿 무음극 셀의 음극 집전체로 쓰면 (500 MPa 조립 · 4 MPa · 60 °C), 3 전극 셀의 **핵생성 과전압이 16.1 ± 1.1 → 3.9 ± 1.1 mV** (2 mA cm⁻² · 각 5 셀 · std err) 로 줄고, 단결정 NMC83 풀 셀의 **첫 방전이 163 → 203 mAh g⁻¹** (+25 % · 첫 효율 71 → 86 %) 로 오른다 (1 mA cm⁻² · 각 3 셀) (p.4–5).  P-FIB 단면 + EDS 에서 Li 는 **Cu 집전체와 C 층 사이**에 쌓여 C 층을 SE 쪽으로 밀어내고, 처음 C 위에 있던 Ag 는 충전 뒤 **Li 속에 희미하게 흩어지며**, 방전 뒤에는 **C 위에 덩어리로 다시 남고** Cu 와 C 사이에 큰 공극과 Li 잔여 실이 생긴다 (p.5–7 · `Fig. 3` · `Fig. 4`).  10 사이클 유지율은 Ag C-Cu **59.3 %** · C-Cu 38.5 % · Ag Cu 47.3 % · Ag 500 nm 37 % — 이 '유지율' 은 **10 번째 충전 용량 ÷ 첫 충전 용량**이다 (`Fig. S9` 로 역산 · §3-3).

| 우리 질문 | 이 논문의 답 | 근거 · 표지 |
|---|---|---|
| ★ 스퍼터 Ag 두께 | 목표 **100 nm** (BSE 단면 실측 **89.32 nm**, `Fig. S2b`) · 비교군 **500 nm** · C 없는 Cu 위에도 100 nm ("Ag Cu") · Leica EM ACE600 · **35 mA** · Ar · **4.0 × 10⁻² mbar** · 거리 50 mm · 기울기 0° · 스퍼터 시간 · 속도 · 두께 감시 방법 [미확인] | [인쇄] p.2 · SI S-1 · S-5 |
| ★ 탄소 층 종류 | **MTI Corporation 상용 '전도성 탄소 코팅 Cu 박'** — Cu 9 µm + *"1 µm thick fine particulate C layer"* · 공급사 말로 *"carbon ink … coated onto the Cu foil via a form of slot die coating"* · Raman D **1359** · G **1588** · 2D **2689 cm⁻¹** → 저자 판정 *"composed principally of graphitic carbon"* · 높이비 I_D/I_G figure-read ≈ **1.3** (바탕 ≈40 을 빼면 ≈ **1.4**) = 결함이 많은 흑연질 [카드 해석] · 위에서 본 형상 = figure-read ≈0.1 µm 입자 응집 (카본블랙꼴) · **결합제 · 1차 입경 · 제품 번호 [미확인]** | [인쇄] SI S-1–S-2 · S-7–S-8 · `Fig. S1a` · `Fig. S4` |
| ★ 층 순서 (Ag 위치) | 조립 때: **Cu \| C \| Ag \| LPSCl** — Ag 는 C 의 **윗면 (SE 쪽)** 에만 (*"deposition was almost exclusively restricted to the upper surface … no widespread Ag penetration directly to the Cu foil surface"*) · 충전 뒤: Ag 가 **Cu 쪽에 쌓인 Li 속**으로 흩어짐 · 방전 뒤: Ag 가 **C 위** (SE 쪽) 로 다시 석출 | [인쇄] SI S-5 · p.5 · p.7 · `Fig. 1a` · `Fig. 5` · `Fig. S2` |
| ★ 전해질 (황화물?) | **예 — Li₆PS₅Cl (argyrodite, 본문 약칭 "LPS")** · ≈1 mm × Ø 5 mm · 분말 ≈30 mg · PEEK 몰드에서 **250 MPa** 선성형 → 양극 + 집전체와 **500 MPa** 공압착 (상온 · 일축) · 공급처 · 입경 [미확인] · σ ≈1.6 mS cm⁻¹ (풀 셀 EIS — §3-6 주의) | [인쇄] SI S-2 · p.3 · p.5 |
| ★ 전류 | 풀 셀 **1 mA cm⁻²** (≈0.3C [카드 산술 §3-7]) · 속도 시험 1 / 2 / 3 mA cm⁻² · 활성화 0.1 mA cm⁻² · 3 전극 첫 도금 **1 mA cm⁻² × 1 h** · **2 mA cm⁻² × 2.5 h (= 5 mAh cm⁻²)** · 탈리 1 mA cm⁻² | [인쇄] p.3 · p.5 · SI S-10–S-11 |
| ★ 압력 | 제조: SE 250 MPa → 전체 **500 MPa** (상온 · 일축) · 운전: **4 MPa** 일축 적층압 · **60 °C** · Ar · 자체 장치 (ref 36) | [인쇄] p.3 · SI S-2 |
| ★ 과전압 판독 | **3 전극** (WE = 집전체 Ø 2 mm · CE = Li Ø 3 mm · RE = Li Ø 1 mm · CE · RE 는 WE 반대면) · 정의 · iR 보정 **본문 미기재** → `Fig. 3a,b` 를 **'꼭지 전압 − 뒤 평탄 전압'** 으로 읽으면 본문 값이 재현된다 [카드 해석] · 2 mA cm⁻²: **C-Cu 16.1 ± 1.1 · Ag C-Cu 3.9 ± 1.1 mV** (각 5 셀 · std err · 그림은 3 셀씩) · 1 mA cm⁻² (각 1 셀): 꼭지 − 평탄 figure-read ≈ steel 17 · Cu 7.5 · C-Cu 2 · Ag C-Cu ≈0 mV | [인쇄] p.3 · p.5 · figure-read `Fig. 3a,b` · §3-4 |
| ★ Li 가 쌓인 위치 | **Cu 집전체 \| C 층 사이** — C 층은 *"remained largely adjacent to the LPS separator"* (일부 자리는 C 가 Cu 에 붙은 채 남고 Li 는 그 C 와 SE 쪽 C 사이에) · Li 두께 본문 ∼20 µm (figure-read 자리마다 ≈4–28 µm) · Ag 는 Li 속 · 방전 뒤 **Cu 와 C 사이 큰 공극** + Li 잔여 '실' · C-Cu (Ag 없음) 도 Cu 쪽에 쌓이되 덜 고르다 | [인쇄] p.5 · p.7 · SI S-14 · `Fig. 3c–j` · `Fig. 4c–i` · `Fig. S11` · `Fig. S12` |

⛔ **한정어 (떼지 말 것)**: ① **셀 수가 작다** — 풀 셀 n = 3 · 핵생성 n = 5 · 왕복 효율 n = 2 · 단면 (충전 · 방전) 각 2 셀 · 오차는 **std err (= sd/√n)** 다 ② 핵생성 과전압의 **정의 · iR 보정이 없다** — 평탄 전압 절대값은 같은 구성에서도 셀마다 ±5–10 mV 흔들린다 (`Fig. 3b` · `Fig. 4b`) ③ **Li–Ag 상 · LiC₆ 는 재지 않았다** (XRD · XPS 없음) — 'Ag 가 Li 에 녹았다' 는 EDS 의 희미한 신호에서 나온 해석이다 ④ 탄소는 '흑연질' 로 불렀지만 Raman 높이비로는 결함이 많다 · 결합제 · 입경 미기재 ⑤ **60 °C · 4 MPa · Ø 5 mm 펠릿 셀** 조건이다.
⇒ **절대값 전이: 0 건** (우리 DFT 로).  전이되는 것은 **단계별 접촉 쌍 · Ag 위치 변화 · 핵생성 과전압의 순서 (실험 앵커)** 셋이다 — §0-1.

---

## 0-1. ★ 표면 모형 고르기용 표 — 탄소 종류 · Ag 위치 · 단계별 접촉 쌍

> 용도: 우리 Li 친화성 계산 (W_ad 보고서 `docs/collab/wad_dem_interface_adhesion_report_2026_11_24.html` **§7 · §7-1** — 값은 그 보고서에서만) 에서 **어느 표면 · 계면 모형을 고를지** 정하는 근거.  '대응 모형' 칸은 그 보고서 §7-1 표의 행 이름을 따랐다.  이 논문은 표면 방위 · 결함 밀도 · 작용기를 **재지 않았다** — 모형 칸은 전부 [카드 해석] 이다.

| 단계 | 층 순서 (SE → 집전체) | Ag 위치 · 형태 | 탄소 종류 · 형태 | 이 단계의 접촉 쌍 (Li 가 만나는 면) | W_ad 보고서 §7-1 대응 모형 (후보) | 근거 · 주의 |
|---|---|---|---|---|---|---|
| ① 스퍼터 직후 (압축 전 · 셀 밖) | (공기) / **Ag 89–100 nm** / C (공급사 "∼1 µm" · 단면 figure-read ≈**2–3 µm**) / Cu 9 µm | C 입자 **윗면**을 따라 덮은 막 (BSE 밝은 띠 · Ag EDS 가 위쪽에 몰림) · 위에서 보면 둥근 알갱이 figure-read ≈0.15–0.25 µm · 결정 방위 [미확인] | MTI 상용 "fine particulate C" · 위에서 본 1차 입자 figure-read ≈0.1 µm 응집 · 단면은 스펀지꼴 다공 · Raman I_D/I_G ≈1.3–1.4 (figure-read · 532 nm) + 2D 2689 cm⁻¹ | — | — | `Fig. S1a,b` · `Fig. S2` · `Fig. S4` · SI S-4–S-8 — ⚠ 두께가 공급사 값과 어긋난다 (§10-①) |
| ② 셀 조립 뒤 (500 MPa · 첫 충전 전) | **LPSCl** (≈1 mm) / **Ag** / C (**<1 µm** · figure-read ≈0.5–0.75 µm · 2D 기공률 18.5 %) / Cu | *"a coherent, now smoother Ag layer"* — 위쪽 C 입자를 감싼 밝은 띠 (BSE) · 조도 Sa 0.283 µm (압축 뒤) | 같은 탄소 (눌림) | **LPSCl\|Ag** (SE 와 처음 닿는 면 = 첫 Li⁺ 환원 자리 후보) · Ag\|C · C\|Cu · (Ag 틈이 있으면 LPSCl\|C) | **Ag(111) 위 Li — 합금 전 날카로운 계면** · SE 쪽 쌍 = 보고서 §2-3 (LPSCl\|Ag(111)) | `Fig. 1d–g` · `Table S1` — ⚠ Ag 방위 미측정 → (111) 은 fcc 최저 에너지 면이라 고른 **가정** |
| ③ 첫 충전 끝 (5 mAh cm⁻² @ 2 mA cm⁻²) | LPSCl / **C (밀려남)** / **Li** (본문 ∼20 µm · 희박 Ag) / **Cu** | **Li 속에 흩어짐** (EDS 희미 · 선 스캔에서는 Li 의 C 쪽 절반 3.2–4.9 µm 에만 ≈3,000 cps) · 100 nm 가 전부 녹으면 Ag ≈**0.5–0.6 at%** [카드 산술 §3-7] = Li 쪽 **희박 고용** 끝 (LiAg 금속간 화합물이 아니다) | C 층은 SE 쪽에 붙어 남는다 (일부 조각은 Cu 쪽에) · 리튬화 (LiC₆) 여부 [미확인] | **Li\|Cu** (새 집전체 계면 = 석출 자리) · **Li(Ag)\|C** · **C\|LPSCl** (Ag 가 빠져나간 SE 쪽 면) · C 가 끊긴 곳은 Li\|LPSCl | **Cu 면 (§7-1 표에 없음 — Cu(111) · Cu(100) 추가 후보)** · 탄소 = **결함 · 작용기가 많은 탄소 (카본블랙 류) 행 → 빈자리 결함 기저면** + **흑연 기저면 LiC₆** · Li–Ag = §7 '합금 구동력' 중 **희박 Ag-in-Li 용해 에너지** · SE 쪽 쌍 = 보고서 §2-4 (LPSCl\|흑연) | `Fig. 3c–j` · `Fig. S10` · SI S-13 — ⚠ Li 두께가 자리마다 figure-read ≈4–28 µm (§10-③) |
| ④ 방전 끝 (1 mA cm⁻² 탈리) | LPSCl / **C + Ag 덩어리** / **공극** (+ Li 잔여 '실') / Cu | **C 위로 다시 석출** — 덩어리 (EDS 밝은 점 · 선 스캔 Ag 혹이 C 혹과 겹침) · *"rather than onto the current collector"* | 같은 탄소 · SE 곁 | 다음 충전의 핵생성 면 = **C 위 Ag 덩어리** · C · 공극 너머 Cu (그 Cu 면에 **S 신호** — figure-read · 저자 언급 없음) | 작은 Ag 덩어리 (계단 · 가장자리 많은 Ag) · Cu 위 황화물 막 (Cu–S · Li₂S) [가설 — 확인 안 됨] | `Fig. 4c–i` · `Fig. S12` — ⚠ 공극은 분해 · 하중 해제로 넓어졌을 수 있다 (저자 p.7) |
| 대조 — C-Cu (Ag 없음) 충전 끝 | LPSCl / C (밀려남) / Li (≈10–20 µm · *"somewhat less uniform"*) / Cu | — | 같은 탄소 | Li\|Cu · Li\|C · C\|LPSCl | 탄소 모형 단독 | `Fig. S11` — Cu\|Li 경계에 가는 S 줄 (figure-read) |
| 대조 — Ag Cu (탄소 없음) | LPSCl / Ag 100 nm (압축 뒤 Sa **0.029 µm** · 매끈) / Cu | Cu 위에 바로 · 매끈한 막 | 없음 | LPSCl\|Ag · Ag\|Cu | Ag(111) · Ag\|Cu | 단면 없음 · 풀 셀만 (유지율 47.3 %) |

**핵생성 과전압 순서 — 실험 앵커 (DFT 친화성 순서와 맞대 볼 값)**

| 조건 | 순서 (꼭지 − 평탄) | 값 | 표지 |
|---|---|---|---|
| 1 mA cm⁻² · 1 h · 각 1 셀 (`Fig. 3a`) | stainless steel > Cu > C-Cu ≳ Ag C-Cu | figure-read ≈ **16.7 / 7.5 / 2 / ≈0 mV** (꼭지 ≈ −26 / −18 / −17.5 / −18 mV · 평탄 ≈ −9.3 / −10.5 / −15.5 / −18 mV) | figure-read · 본문 *"C-Cu required approximately 6 mV less overpotential compared with Cu"* 와 맞는다 (7.5 − 2 ≈ 5.5) |
| 2 mA cm⁻² · 2.5 h · 각 5 셀 (`Fig. 3b` 는 3 셀씩) | C-Cu > Ag C-Cu | **16.1 ± 1.1 vs 3.9 ± 1.1 mV** (std err) | [인쇄] p.5 |

⚠ 이 값은 **복합 층 전체의 응답**이다 — Li 가 실제로 핵을 만든 자리는 단면상 **Cu \| C 계면**인데 (`Fig. 3c`), 과전압을 낮춘 Ag 는 처음에 **SE 쪽 윗면**에 있었다.  그래서 'Ag(111) 위 Li 원자 하나의 흡착 세기' 하나로 이 차이를 설명하지 않는다 [카드 해석] — Li⁺ 가 Ag 에서 환원 → Ag/C 를 지나 → Cu 쪽에서 금속으로 자라는 **경로 전체**의 값이다.  절대 평탄 전압은 iR 이 섞여 있어 친화성 비교에 쓰지 않는다 (§3-4).

**우리 W 쌍 목록에 주는 뜻 (요약 · 상세 §8)**
- 이 구조에서 **운전 중 처음 벌어지는 계면은 C \| Cu** 다 (Li 가 그 사이로 들어가 C 를 밀어낸다) — 보고서 §2 의 네 쌍 (C–C · Ag–C · LPSCl\|Ag(111) · LPSCl\|흑연) 에 **C\|Cu · Li\|Cu · Li\|C (리튬화)** 가 없다.
- **LPSCl\|Ag 는 첫 충전 전까지만** 맞는 쌍이다 — 첫 충전 뒤 SE 쪽 면은 **LPSCl\|C** (+ 방전 뒤 C 위 Ag 덩어리) 로 바뀐다.
- '합금 구동력' 은 LiAg · Li₉Ag₄ · Li₁₀Ag₃ (Spencer-Jolly 경로) 만이 아니라 **Li 속 희박 Ag (≈0.5 at%) 의 용해 에너지**가 이 구조의 끝 상태다.
- 탄소 모형은 **CNF 헤링본 가장자리 행이 아니라 '결함 많은 탄소' 행** (I_D/I_G > 1) + **흑연 기저면 (LiC₆)** 쪽이다 — 작용기 (O · N) 는 XPS 가 없어 정할 수 없다.

---

## 1. 한 줄 요약

상용 탄소 코팅 Cu 박에 Ag 100 nm 를 스퍼터한 **두께 1 µm 미만의 Ag/C 2 층**이 황화물 (Li₆PS₅Cl) 무음극 셀에서 Li 핵생성 과전압을 낮추고 (16.1 → 3.9 mV) 첫 용량 · 효율을 올린다 (163 → 203 mAh g⁻¹ · 71 → 86 %).  단면으로 본 기전은 *"Ag 가 Li 석출을 돕고, Li 는 Cu | C 사이에 쌓여 C 를 밀어내며, Ag 는 Li 에 녹아 흩어졌다가 방전 뒤 C 위에 남는다"* 이다.
저자 스스로 꼽는 기여는 성능보다 **만들기 쉬움 · 확장성 · 재현성** (상용 박 + 실험실 표준 스퍼터 코터) 이고 (p.8 결론), 공극 · 불완전 탈리 때문에 10 사이클 유지율은 59 % 에 그친다.

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 던지는 질문 | Ag/C 인터레이어가 Li 석출 · 탈리를 돕는 **기전이 아직 불분명**하다 (p.2).  슬러리 Ag/C (보통 수십 µm · ≈35 nm 탄소 + ≈60 nm Ag) 는 Ag 가 탄소 속에 무작위로 흩어져 Ag · C · 집전체 계면이 겹치므로 **Ag 의 역할만 떼어 보기 어렵다**.  그래서 Ag 를 **스퍼터로 C 표면에 한 겹 몰아 놓은** 얇은 층으로 Ag 의 처음 위치를 분명히 하고, 충전 · 방전 뒤 Ag · C · Li 가 어디 있는지를 단면 (P-FIB · EDS · SIMS) 으로 본다 |
| 선행 기전 (ref 23 = `spencerjolly2023_…`) | Ag/흑연 층: 충전 시 Li 가 흑연에 먼저 **전기화학 삽입** → 리튬화 흑연이 Ag 와 **화학 반응**해 점점 Li-rich 한 Li–Ag 합금 → 인터레이어와 집전체 사이에 석출 · Ag 는 CCD 를 올리지 않고 집전체 쪽 Li 층을 균일하게 · 2 mA cm⁻² 를 넘으면 흑연 삽입이 화학 반응을 앞질러 Li 금속이 바로 집전체에 · 방전은 점점 Li-poor 한 Li–Ag 상을 거쳐 C 와 Ag 만 남는다 (p.2 요약).  저자 표현: Ag 는 Li 와 합금 · 용해해 *"a solid–solution that presents a positive attraction potential to Li"* (refs 24–26) |
| 다른 금속 | Zn · Sn · Al · Ni + 탄소 층은 Ag/C 만 못했다 (refs 27, 28) |
| 스퍼터 Ag 선행 | 대부분 **저전류**: ≈0.25 mA cm⁻² · 30 µA cm⁻² · 25 µA cm⁻² (refs 32–34).  예외 1 건 = 1.6 mA cm⁻² · LLZTO 위 200 nm 스퍼터 Ag + ≈7 µm Ag/C + Li (ref 35) — 거기서 스퍼터 Ag 는 촉매가 아니라 **LLZTO 와 Ag/C 의 점착을 높인 것**으로 해석 · Li\|Ag/C\|Ag\|LLZTO\|이온 액체\|NCM333 파우치 800 사이클 ≈85 % (상온 · 무가압) |
| 이 논문의 설계 | 상용 C-Cu 박 (C ∼1 µm) + 스퍼터 Ag 100 nm — *"5–10 μm (and 5–10 times) thinner than previous Ag/C arrangements operating at comparable current densities"* (p.2) · p.4 에서는 *"∼20 times thinner than those explored in the literature"* (ref 17) · 스퍼터는 Ag 를 *"localization and concentration at the C surface"* 로 둔다 (슬러리는 Ag · 응집이 두꺼운 C 층 전체에 무작위) |
| 계보 | Lee 2020 *Nat. Energy* (Samsung Ag–C 원조 · ref 17) → Spencer-Jolly 2023 *Joule* (ref 23) → Doerrer 2024 *Device* (분무 LPSCl + Ag–C 다층 · ref 29) → Metzler 2025 *ACS AMI* (탄소 나노복합 층 속 Ag 입자 분포 · ref 30) → **본 논문** — 같은 Oxford 재료과 Grant 그룹 라인 |
| 글의 꼴 | 1 서론 → 2 방법 → 3.1 층 형상 → 3.2 풀 셀 → 3.3 충전 뒤 층 → 3.4 방전 뒤 층 → 3.5 기전 → 4 결론 · 그림 5 · 표 0 · 식 1 (이온전도도) · 참고문헌 61 / SI: 방법 (스퍼터 · 레이저 절단 · 조립 · 조도 · Raman · SEM/EDX · PFIB/SIMS) · 그림 S1–S12 · 표 S1 · 참고문헌 S1–S16 |

---

## 3. 핵심 수치 총정리 ★

### 3-1. 제작 · 셀 (p.2–3 · SI S-1–S-4)

| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| 집전체 원판 | MTI Corporation (미국) *"conductive carbon-coated Cu foil with a 9 µm Cu foil thickness and a 1 µm thick fine particulate C layer"* · 공급사 말로 *"formed from a carbon ink that was coated onto the Cu foil via a form of slot die coating"* · 결합제 · 탄소 원료 · 제품 번호 [미확인] | [인쇄] SI S-1–S-2 |
| 스퍼터 | Leica EM ACE600 박막 코터 · **35 mA** · Ar · 운전 압력 **4.0 × 10⁻² mbar** · 타깃–기판 **50 mm** · 기울기 **0°** · 목표 **100 nm** (비교 **500 nm**) · 대조 "Ag Cu" = 맨 Cu 위 ≈100 nm · 시간 · 속도 · 두께 감시 [미확인] | [인쇄] p.2 · SI S-1 |
| 이름 규약 | "C-Cu" = 탄소 코팅 Cu (Ag 없음) · "Ag Cu" = 맨 Cu + Ag · "Ag C-Cu" = 탄소 코팅 Cu + Ag (100 / 500 nm) | [인쇄] p.2 |
| 원판 자르기 | 레이저 절단 — Needham NLase Desktop Pro · Q-switched 고체 MOPA · **1064 ± 4 nm** · 첨두 출력 > 10 kW · 빔 지름 ≈7 mm (원문 그대로) · 발산 < 2 mrad · Al 받침판에 고정 | [인쇄] SI S-2 |
| SE 분리막 | **Li₆PS₅Cl** (argyrodite · 본문 약칭 "LPS") · 분말 ≈**30 mg** · PEEK 몰드 **Ø 5 mm** · **250 MPa** 상온 일축 → **≈1 mm** · 공급처 · 입경 [미확인].  30 mg 이 진밀도 1.64 g cm⁻³ 로 꽉 차면 0.93 mm [카드 산술 · 진밀도는 litdb 진밀도 묶음 값 대입] → "≈1 mm" 와 맞는다 | [인쇄] SI S-2 |
| 양극 | **단결정 LiNi₀.₈₃Mn₀.₀₆Co₀.₁₁O₂** (1–2 µm · MSE Supplies) : LPS : **CNF** = **75 : 22 : 3** wt% · 유성 볼밀 Fritsch Pulverisette 7 · ZrO₂ 40 mL 통 · Ø 5 mm 볼 55 g · **140 rpm 30 min** · 셀당 **4 mg** → NMC 면 적재 **15.3 mg cm⁻²** [카드 산술 = 3.0 mg ÷ 0.196 cm²] · 양극 집전체 Al 15 µm | [인쇄] p.3 · SI S-2 |
| 조립 | SE 펠릿 위에 양극 분말 4 mg → Ag/C 집전체를 얹고 전체를 **500 MPa** 상온 일축 (기공 줄이기 · 층간 접촉) | [인쇄] p.3 · SI S-2 |
| 3 전극 반쪽 셀 | WE = 집전체 원판 **Ø 2 mm** (0.0314 cm²) · CE = Li **Ø 3 mm** · RE = Li **Ø 1 mm** · Li 박 (Sigma-Aldrich) 을 파우치 안에서 ≈150 µm 로 밀어 손 펀치로 · Li 쪽 집전체 Cu 30 µm · `Fig. 1c` 그림상 **CE · RE 는 SE 윗면, WE 는 아랫면** · 사후 관찰용 셀은 **500 MPa** 로 조립 | [인쇄] p.3 · SI S-2 · `Fig. 1c` |
| 운전 | **적층압 4 MPa (일축) · 60 °C** (*"to facilitate Li⁺ ion mobility"*) · Ar 안의 자체 장치 (ref 36) · 풀 셀 **2.5–4.3 V** · 용량은 **NMC 질량** 기준 | [인쇄] p.3 |
| 3 전극 시험 | 첫 도금 **1 mA cm⁻² × 1 h** · **2 mA cm⁻² × 2.5 h** · 사후 관찰 셀 = **2 mA cm⁻² 로 5 mAh cm⁻² 충전 → 1 mA cm⁻² 방전** (60 °C · 4 MPa) → 글러브박스에서 분해 | [인쇄] p.3 |
| 셀 수 | 풀 셀 (유지율 · 임피던스) 구성마다 **3** · 핵생성 과전압 3 전극 **5** · 왕복 효율 3 전극 **2** · 단면 충전 · 방전 각 **2** (분해 뒤 온전히 꺼낸 것) | [인쇄] p.3 |
| 통계 | 평균 ± **std err = sd/√n** (n = 측정 수) | [인쇄] p.3 |
| 자료 처리 | Batalyse "Data Analysis" (충방전) · EC-Lab (BioLogic · 등가회로 맞춤) · ImageJ (기공 문턱) · Aztec 4.1 SP1 (EDS) · Hiden SIMS MAPPER 2.0.0.5 | [인쇄] SI S-2 · S-4 · S-6 · p.3 |

### 3-2. 층 형상 — 두께 · 기공 · 조도 · 탄소 결정성 (p.3 · SI S-4–S-9 · `Fig. 1d–g` · `Fig. S1`–`Fig. S4` · `Table S1`)

**두께**

| 대상 | 값 | 표지 |
|---|---|---|
| C 층 (공급사) | **∼1 µm** — *"significantly thinner than common previously reported Ag/C interlayer thicknesses in SSBs of 10–20 µm"* | [인쇄] SI S-5 |
| C 층 (스퍼터 직후 · 압축 전 단면 `Fig. S2a` · Ar 광폭 이온 밀링) | figure-read ≈ **2.1–3.2 µm** (1 µm 막대 = 70 px · 자리마다) — ⚠ 공급사 값의 2–3 배 | figure-read |
| Ag/C 층 (500 MPa 압축 뒤 `Fig. 1d`) | 본문 **"<1 μm"** · figure-read ≈ **0.5–0.75 µm** (1 µm 막대 = 85 px) | [인쇄] p.3 · figure-read |
| Ag 막 | **89.32 nm** (BSE 단면 `Fig. S2b` 그림 글자 · *"close to the target thickness of 100 nm"*) | [인쇄] p.3 · SI S-5 |
| Ag 분포 (압축 전) | *"deposition was almost exclusively restricted to the upper surface, and there was no widespread Ag penetration directly to the Cu foil surface"* · BSE: 밝은 Ag 가 위쪽 C 입자를 덮는 껍질 + 위쪽 ≈0.3 µm 안의 작은 밝은 점 몇 개 · EDS Ag 가 위쪽 ≈1 µm 에 몰리고 아래로 갈수록 약해짐 (EDS 10 kV 의 흐림 포함) | [인쇄] SI S-5 · figure-read `Fig. S2b,d` |
| Ag 분포 (압축 뒤) | *"the presence of a coherent, now smoother Ag layer. There was no delamination of the Ag or C."* · BSE 밝은 띠가 층 위쪽 절반에서 C 입자 윤곽을 따라감 | [인쇄] p.3 · figure-read `Fig. 1d` |
| 표면 (위에서) | C-Cu: 미세 입자 응집 (figure-read 1차 ≈0.1 µm · 사슬꼴 · 사진 검정) · Ag 100 nm: 둥근 알갱이 figure-read ≈0.15–0.25 µm + 평평한 틈 · 사진 은빛 · *"no obvious patches of uncovered C"* · Ag 500 nm: 솟은 C 입자 위 Ag 마디 figure-read ≈0.3–0.4 µm · 입자 사이 틈이 메워져 *"somewhat smoother"* | [인쇄] SI S-4 · figure-read `Fig. S1` |

**기공률** (SI S-6 · `Fig. S3` · ImageJ 회색조 문턱 · 단면 3 곳)

| 상태 | 평균 | sd | std err | 비고 |
|---|---|---|---|---|
| 압축 전 | **26.7 %** | 1.8 % | 0.8 % | ROI figure-read ≈1.5 × 11.4 µm |
| 500 MPa 압축 뒤 | **18.5 %** | 1.4 % | 0.6 % | ROI figure-read ≈0.5 × 5.7 µm · 본문 *"(std err 0.6%)"* |

- 저자: *"It was however challenging to reliably quantify such thin coatings and fine-scale porosity."* · 흔한 Ag/C 층은 ≈29 % (ref S5) · *"a certain degree of porosity is likely beneficial to accommodate volume changes during plating/stripping (such as Ag-Li alloying, any Li intercalation into C, etc)"*.
- ⚠ (sd/se)² = 5.1 · 5.4 [카드 산술] → std err 는 n ≈ 5 로 계산된 값이다 (본문은 '세 단면').  압축 전후 두께 (figure-read 2.1–3.2 → 0.47–0.74 µm) 를 질량 보존으로 풀면 압축 전 기공률 ≈70–90 % 가 나와 26.7 % 와 안 맞는다 (§3-7 · §10-②).

**조도** (`Table S1` · SI S-7–S-8 · µSurf Nanofocus 공초점 광학 · 320-S 50× · dR max ±0.5 · n = 40 · cutoff 800 µm · Gauss 회귀 필터 · 수평 차수 1 · 값 = 같은 박에서 3 번 잰 평균 · 단위 µm)

| 집전체 | Sa | sd | se | Sq | sd | se |
|---|---|---|---|---|---|---|
| stainless steel | 0.047 | 0.007 | 0.004 | 0.060 | 0.009 | 0.005 |
| Cu | 0.167 | 0.019 | 0.011 | 0.217 | 0.026 | 0.015 |
| Ag-Cu (100 nm) | 0.272 | 0.110 | 0.064 | 0.340 | 0.137 | 0.079 |
| Ag-Cu (100 nm · 500 MPa) | **0.029** | 0.005 | 0.003 | 0.046 | 0.002 | 0.001 |
| C-Cu | 0.370 | 0.029 | 0.017 | 0.513 | 0.046 | 0.026 |
| C-Cu (500 MPa) | **0.245** | 0.062 | 0.036 | 0.332 | 0.092 | 0.053 |
| Ag C-Cu (100 nm) | 0.790 | 0.143 | 0.082 | 1.055 | 0.196 | 0.113 |
| Ag C-Cu (100 nm · 500 MPa) | **0.283** | 0.167 | 0.097 | 0.377 | 0.204 | 0.118 |
| Ag C-Cu (500 nm) | 0.427 | 0.013 | 0.008 | 0.632 | 0.071 | 0.041 |
| Ag C-Cu (500 nm · 500 MPa) | **0.075** | 0.001 | 0.000 | 0.097 | 0.001 | 0.001 |

- 저자 해석 (SI S-7): C-Cu 가 steel · Cu 보다 거칠고 500 MPa 뒤에도 그렇다 · 압축 뒤 Ag C-Cu (0.283) 는 C-Cu (0.245) 와 비슷 → *"the feedstock C-Cu foil roughness was largely unaltered by the addition of 100 nm of Ag"* · 500 nm 는 *"reduced"* (0.427 · 기공 메움) · 압축 뒤 0.075 (두꺼운 Ag 의 쉬운 변형).  본문 (p.3) 은 Ag Cu 압축 뒤 0.029 를 *"even smoother than uncoated Cu (Sa = 0.167 μm)"* 라 쓰고, 매끈 · 연속 Au 층이 덩어리 Au 보다 덜 도왔다는 선행 (ref 39) · 거친 촉매면 = 활성 자리 많음 (refs 40, 41) 을 근거로 든다.  ⚠ 비교 기준이 섞여 있다 (§10-⑨).

**탄소 결정성 — Raman** (SI S-3 · S-7–S-8 · `Fig. S4` · Horiba JY LabRam Aramis · **532 nm** · 출력 1 % · 30 s × 16 평균 · ×50 ELWD · 후방 산란 · 100–3000 cm⁻¹)

| 항목 | 값 | 표지 |
|---|---|---|
| 띠 위치 | **D 1359 · G 1588 · 2D 2689 cm⁻¹** (그림 글자) | [인쇄] |
| 저자 판정 | *"relatively well-defined D (1359 cm⁻¹) and G (1588 cm⁻¹) bands"* · *"The peaks in Figure S4 also indicated graphene-like regions"* · 2D 는 *"related to the number of graphene layers stacked in graphitic AB ordering"* · *"the C-coating on the C-Cu current collector was composed principally of graphitic carbon"* · 비정질 탄소는 넓은 띠만 보인다 (ref S9) | [인쇄] SI S-7–S-8 |
| 세기 (figure-read) | 바탕 ≈40 · D 꼭지 ≈185 · G ≈142 · 2D ≈72 (그 둘레 바탕 ≈45) · D–G 사이 골 ≈75 · ≈1100–1250 cm⁻¹ 어깨 | figure-read ≈ |
| 비 (카드) | I_D/I_G (원 높이) ≈ **1.30** · 바탕 뺀 높이 ≈145/102 ≈ **1.42** · I_2D/I_G (바탕 뺀) ≈ **0.26** | [카드 산술 · figure-read 값으로] |
| 읽는 법 | I_D/I_G > 1 + 높은 D–G 골 + 1100–1250 어깨 = **결함 · 무질서가 많은 나노결정 흑연질** (카본블랙 · 덜 흑연화된 탄소꼴) · 2D 가 보이므로 쌓인 흑연 영역도 일부 있다 — 저자의 '흑연질' 과 '비정질 아님' 은 맞지만, **결함 없는 흑연 기저면은 아니다** | [카드 해석] |
| 대조 | `kang2026_…` CNF: LC (PR-25-XT-PS) I_D/I_G **0.99** · HC (PR-25-XT-LHT · 1500 °C) **0.19** — 이 논문의 C 는 LC CNF 보다도 무질서하다 (레이저 파장 등 측정 조건은 대조 안 했다) | [다른 카드] |

### 3-3. 풀 셀 전기화학 (p.3–5 · `Fig. S6`–`Fig. S9` · 1 mA cm⁻² · 2.5–4.3 V · 60 °C · 4 MPa)

> 그림: `Fig. 2` (한 셀씩 · 세 셀 · 100 사이클) · `Fig. S6`–`Fig. S9`.

**구성별 평균 (`Fig. S9` = 셀 3 개 평균 ± std err) — 모든 용량은 mAh g⁻¹_NMC**

| 구성 | C1 (첫 충전) | DC1 (첫 방전) | C10 | DC10 | 본문 유지율 (std err) | C10/C1 [카드 산술] | DC10/DC1 [카드 산술] | 첫 효율 DC1/C1 [카드 산술] |
|---|---|---|---|---|---|---|---|---|
| C-Cu | ≈231 | ≈163 (본문 **163**) | ≈88 | ≈85 | **38.5 %** (4.6 mAh g⁻¹) | 0.38 | 0.52 | 0.71 (본문 **71 %**) |
| Ag Cu | ≈216 | ≈172 | ≈102 | ≈96 | **47.3 %** (18.5) | 0.47 | 0.56 | 0.80 |
| **Ag C-Cu 100 nm** | ≈233 | ≈203 (본문 **203**) | ≈139 | ≈135 | **59.3 %** (11.5) | 0.60 | 0.67 | 0.87 (본문 **86 %**) |
| Ag C-Cu 500 nm | ≈207 | ≈163 | ≈77 | ≈74 | **37 %** (13.4) | 0.37 | 0.45 | 0.79 |
| Ag C-Cu 100 nm + 활성화 | ≈161 | ≈129 | ≈51 | ≈47 | **31.3 %** (6.9) | 0.32 | 0.36 | 0.80 |

C1 · DC1 · C10 · DC10 은 figure-read ≈ (눈금 840 px = 250 mAh g⁻¹) · std err 막대도 본문 값과 맞는다 (예: Ag C-Cu C10 막대 ≈127–151 = ±11.6).
⇒ **본문 '유지율' = C10/C1 (충전 용량)** 이다 — 다섯 구성 모두 0.01 안에서 맞는다.  첫 사이클 비가역 손실 (첫 효율 71 vs 87 %) 이 유지율에 섞여 있고, 방전 기준 (DC10/DC1) 으로 보면 Ag C-Cu 의 C-Cu 대비 우위가 **21 → 15 %p** 로 줄어든다 [카드 산술].

**그림의 개별 셀 (figure-read ≈)**
- `Fig. 2a` C-Cu (1 셀): 1 · 2 · 5 · 10 번째 방전 ≈160 / 138 / 103 / 67–72 · 충전 ≈225 / 162 / 112 / 78 · 10 번째 방전 끝의 꺾임에 "Polarisation" 표지 (본문 *"slight deviations in the expected shape … after one or two cycles"* — 불균일 석출 · 부반응 · 저항 불연속 가능성) · 화살표 **−62 %** = 세 셀 평균 38.5 % 와 같은 숫자.
- `Fig. 2b` Ag Cu (1 셀): 방전 ≈164 / 134 / 92 / 57 · 충전 ≈235 / 170 / 107 / 72 · 화살표 **−53 %** (평균) — 이 셀 자체는 평균보다 나쁘다.
- `Fig. 2c` 첫 사이클 세 셀씩: Ag C-Cu 셀 1 / 2 / 3 방전 ≈202 / 193 / 212 · C-Cu ≈160 / 161 / 167 · 충전 곡선은 둘이 거의 겹친다 (≈228–243 · 평탄 ≈3.55 V) · 화살표 **+25 %** (203/163 = 1.245).
- `Fig. 2d` Ag C-Cu (1 셀): 방전 ≈202 / 198 / 181 / 160 · 충전 ≈233 / 205 / 187 / 168 · 화살표 **−41 %** (평균) — 이 셀의 C10/C1 ≈0.72 · 10 번째 충전 ≈168 은 평균 139 ± 11.5 보다 높아 **세 셀 중 가장 좋은 셀**로 보인다 [카드 해석].
- `Fig. 2e` 100 사이클 충전 용량 (셀 2 개): 셀 1 ≈232 → 205 (2) → 150 (20) → 115 (40) → 107 (60) → 98 (80) → **93 (100)** · 셀 2 ≈228 → 170 → 110 → 82 → 73 → 70 → **64** · 100 번째 ÷ 첫 = ≈0.40 · 0.28 [카드 산술].  셀 1 의 2 · 10 번째 충전이 `Fig. 2d` 와 같아 `Fig. 2d` = `Fig. 2e` 의 셀 1 로 보인다 [카드 해석].
- `Fig. 2f` 쿨롱 효율: 첫 사이클 셀 1 ≈87 % · 셀 2 ≈75 % → 2 번째 ≈95–97 % → ≈10 사이클 ≈98–99 % → 40 사이클 뒤 ≈99.3–99.7 % · 본문 *"an average Coulombic efficiency >95% over 100 cycles"*.  무음극은 Li 저장고가 없어 CE 99 % 도 100 사이클이면 0.99¹⁰⁰ ≈ 0.37 [카드 산술] — 셀 1 의 0.40 과 같은 자릿수다.

**다른 문장 · 비교값**
- C-Cu 첫 방전 163 은 *"comparable to 166 mAh/g for an Ag-containing Ag/C interlayer"* (ref 27) — ⚠ ref 27 의 제목은 *"… Based on Thin Carbon Black Layer"* 라 'Ag 를 품은' 층인지 이 카드는 확인 못 했다 [미확인].
- 첫 효율 86 % 는 Lee 2020 의 89 % (ref 17) *"under similar cycling conditions"* 와 비슷 · 결론에서 첫 방전 >200 은 다른 무음극 풀 셀의 166 · 192 · 215 mAh g⁻¹ (refs 17, 27, 30) 와 견준다 (어느 값이 어느 ref 인지 원문 미대응).
- 효과의 해석 (p.4): *"the plating homogenizing effect of Ag when combined with a high areal density of active reaction sites provided by the fine-scale C particulate coating"* · Ag Cu 는 C 보호막이 없어 Li 를 뺄 때마다 Cu–LPS 부반응 (Cu–S) 이 쉬웠을 것 (p.3).
- Cu 대 스테인리스 (p.4): 전기전도 5.97 × 10⁷ vs 1.45 × 10⁶ S m⁻¹ (20 °C) 이지만 무음극에는 부동태가 강한 스테인리스가 보통 낫다 · LPS + Cu 무음극은 Cu 부식 · Cu–S 화합물이 보고됨 (refs 42, 52) · 이 논문은 부반응을 *"could not be ruled out"* 하면서 100 사이클 안정성을 C 코팅의 보호 효과 근거로 든다 (p.5).

**속도 · Ag 두께 · 활성화**
- `Fig. S7` 첫 사이클 (figure-read ≈): C-Cu 1 mA cm⁻² 충전 ≈230 · 방전 ≈160 / **2 mA cm⁻² 충전 ≈450 = "Charging failure"** · 방전 ≈135 · Ag C-Cu 1 → ≈232 / 202 · **2 → 충전 ≈157 · 방전 ≈95** (기운 곡선) · **3 → 충전 ≈500 = "Charging failure"** · 방전 ≈107.  SI: *"For 3 mA/cm², first cycle charging failure was exhibited by significantly (and impossibly) exceeding the theoretical capacity of NMC811 of approximately 230 mAh/g"*.  ⇒ *"extended functionality from 1 mA/cm² up to 2 mA/cm²"* 는 **2 mA cm⁻² 첫 충전이 단락 없이 끝났다**는 뜻이고, 그 방전 용량은 1 mA cm⁻² 의 ≈절반이다 · 2 mA cm⁻² **여러 사이클 자료는 없다**.
- `Fig. S6` Ag 500 nm (1 셀): 충전 ≈190 · 방전 ≈148 → 10 번째 ≈88 / 80 · 화살표 −63 % (평균 37 %) · 첫 충전 평탄 시작 ≈3.65–3.7 V (100 nm 셀 ≈3.55 V · `Fig. 2d`) · 방전이 3.6 → 2.5 V 로 길게 기운다 (분극 큼) [figure-read].  저자 해석: 치밀한 500 nm Ag 가 *"diffusion barrier"* 가 되어 Li 확산 길이를 늘리고 (ref 54), 압축 뒤 평평한 면 (Sa 0.075) 이 반응 자리를 줄였을 것 — Zn 은 두께를 1 µm 로 늘렸을 때 좋아졌다는 선행 (ref 53) 과 반대 결과.
- `Fig. S8` 활성화: SI 서술 = 0.1 mA cm⁻² 로 *"50 % SOC (3.78 V) and 10 % SOC (4.16 V)"* 사이 한 번 → 1 mA cm⁻² 로 *"10 % SOC and 90 % SOC (3.53 V)"* · 그림의 활성화 곡선은 **3.53–3.78 V** (충전 ≈112 · 방전 ≈80) · 그 뒤 3.53–4.15 V 에서 첫 ≈160 / 131 → 10 번째 ≈50 / 46 · 화살표 −69 % (평균 31.3 %) — 활성화가 안정성을 늘리지 못했다 (§10-⑫ SOC 표기).

### 3-4. ★ 핵생성 과전압 — 3 전극 (p.5)

> 그림: `Fig. 3a,b` · `Fig. 4a,b` · 장치 `Fig. 1c`.

- **장치**: WE (집전체) Ø 2 mm 아랫면 · CE (Li Ø 3 mm) · RE (Li Ø 1 mm) 윗면 (`Fig. 1c`) · 목적 = *"to separate the contribution of working and counter electrodes to the Li plating nucleation overpotential"* (ref 37) · 본문은 축을 *"the voltage versus Li⁺/Li at the counter electrode"* 라고 부른다 — 전작 (ref 30) 의 같은 그림은 *"voltage versus Li⁺/Li counter electrode"* 라 적었으므로 'Li 전극 대비 WE 전압' 의 뜻이고, 3 전극의 목적으로 보아 **WE − RE 전압**으로 읽는다 [카드 해석].
- **시간 축**: 도금은 figure-read ≈2.42–2.46 h 에 시작 — 그 앞 ≈2.4 h 는 휴지 (OCV) 로 보인다 (본문 미기재 · `Fig. 4a` 에 "OCV" 표지 ≈1.9–2.0 V).
- **본문 값 (2 mA cm⁻² · 2.5 h · 각 5 셀)**: *"five cells with C-Cu interlayers had an average nucleation overpotential of 16.1 mV (std err 1.1 mV), and five cells with Ag C-Cu interlayers had a much reduced average nucleation overpotential of 3.9 mV (std err 1.1 mV)"* · 해석 = *"a higher density of Li nucleation sites and a lower Li nucleation energy barrier"* (ref 55).
- **1 mA cm⁻² 문장**: *"plain stainless steel and Cu required the highest overpotential magnitude to initiate Li plating, while C-Cu required approximately 6 mV less overpotential compared with Cu. Ag C-Cu exhibited a more stable (flatter, less erratic) subsequent charging profile than C-Cu."*
- **정의는 본문에 없다** → 그림으로 역산:

| 셀 (`Fig. 3a` 1 mA cm⁻² · `Fig. 3b` 2 mA cm⁻²) | 꼭지 (mV) | 뒤 평탄 (mV) | 꼭지 − 평탄 (mV) |
|---|---|---|---|
| 3a stainless steel | ≈ −26 | ≈ −9.3 (3.4 h) | ≈ 16.7 |
| 3a Cu | ≈ −18 (2.6 h 시작) | ≈ −10.5 (3.25 h — 그 뒤 "Charging failure" 로 ≈ −4 mV 로 뜀) | ≈ 7.5 |
| 3a C-Cu | ≈ −17.5 | ≈ −15.5 | ≈ 2 |
| 3a Ag C-Cu | ≈ −18 | ≈ −18 ("Stabilised charging") | ≈ 0 |
| 3b C-Cu 셀 1 / 2 / 3 | ≈ −33 / −39 / −31 | ≈ −14.5 / −22 / −15 (≈4.9 h) | ≈ 18.5 / 17 / 16 → 평균 ≈17 |
| 3b Ag C-Cu 셀 1 / 2 / 3 | ≈ −15.5 / −25 / −16 | ≈ −12 / −21.5 / −12 | ≈ 3.5 / 3.5 / 4 → 평균 ≈3.7 |

전부 figure-read ≈.  ⇒ **'꼭지 − 도금 끝 무렵 평탄'** 으로 읽으면 본문 값 (16.1 · 3.9 · "6 mV less") 이 재현된다 [카드 해석].  꼭지 절대값만 보면 1 mA cm⁻² 에서 Cu · C-Cu · Ag C-Cu 가 모두 ≈ −18 mV 로 같다 (steel 만 크다).
- **평탄 (성장) 전압은 갈리지 않는다**: 2 mA cm⁻² 도금 끝 C-Cu −14.5…−22 · Ag C-Cu −12…−21.5 mV 로 겹치고, 1 mA cm⁻² 에서는 오히려 Ag C-Cu (−18) 가 C-Cu (−15.5) 보다 크다 — Ag 가 낮춘 것은 **핵생성 꼭지**뿐이다.  C-Cu 는 꼭지 뒤 2.5 h 내내 천천히 풀려서 (−33 → −15) '평탄' 을 언제 읽느냐에 값이 걸린다.
- **iR**: RE 가 CE 쪽 면에 있어 WE–RE 사이 SE 의 iR 이 일부 섞인다.  1 mm 를 다 지나는 iR 은 2 mA cm⁻² 에서 j·t/σ = 125 mV (σ 1.6) · 49 mV (σ 4.1 mS cm⁻¹) [카드 산술] 인데 측정 평탄이 그보다 작으므로 RE 가 보는 몫은 일부이고 크기를 모른다 — **평탄 절대값을 계면 과전압으로 읽지 않는다**.  iR 보정 언급 없음 [미확인].
- **왕복 효율 (`Fig. 4a,b` · 2 셀)**: 2 mA cm⁻² 2.5 h 도금 (셀 1 ≈ −33 → −26 · 셀 2 ≈ −20 → −15 mV) → 1 mA cm⁻² 탈리 (셀 1 ≈ +12 → +17 · 셀 2 ≈ +8 → +13 mV) → 끝에 급상승해 5 V (셀 2 ≈8.6 h · 셀 1 ≈8.85 h) [figure-read].  본문: *"A peak in voltage after approximately 4 h was attributed to the depletion of Li and indicated a round-trip efficiency of approximately 80%, which was comparable to the initial CE of Ag C-Cu full cells."* · figure-read 탈리 ≈3.7–3.9 h → **74–78 %** [카드 산술 = 1 mA cm⁻² × t ÷ 5 mAh cm⁻²].

### 3-5. ★ 단면 — Li 가 쌓인 위치 · 두께 · Ag 분포 (p.5–7 · `Fig. 4c–i` · `Fig. S10`–`Fig. S12` · SI S-13–S-15)

> 그림: `Fig. 3c–j` (충전 뒤) · `Fig. 4c–i` (방전 뒤) · `Fig. S10`–`Fig. S12`.

**충전 뒤 — Ag C-Cu (100 nm) · 2 mA cm⁻² × 2.5 h (= 5 mAh cm⁻²)**
- `Fig. 3c` (SE · 10 µm 막대): 위 = 집전체 (Cu) · 가운데 = **Li** · 아래 = 주황 점선의 C 띠 → LPSCl · 본문 *"a Li layer formed (∼20 μm) between the Cu current collector (top of image), and the C coating, which remained largely adjacent to the LPS separator (bottom of image)"* · 그림 화살표 자리의 Li figure-read ≈ **14 µm** (그림 축척 그대로 · 기울기 보정 여부 미기재).  왼쪽 위에 C 조각 하나가 Cu 바로 아래 붙어 있고 왼쪽 가운데에 다른 C 조각이 있어 Li 는 그 둘 사이에 있다 [figure-read] — 본문 *"there were some regions where the C coating remained attached to the Cu (e.g., on the LHS of Figure 3c), but the Li nonetheless plated towards the current collector, in this case, over the C"*.
- `Fig. 3d–g` (EDS): Cu = 위 · S = 아래 (LPSCl) · C = 왼쪽 위 조각 + 아래 띠 · Ag = Li 자리 전체에 희미 (LPSCl 자리보다 조금 밝다) — 본문 *"a faint Ag signal distributed throughout the newly plated layer i.e., the initial, distinct ∼100 nm Ag layer on the C had become distributed into the plated Li, regardless of the final position of the C coating"* · *"Even though a demanding current density of 2 mA/cm² was used, Li plating was reasonably uniform."*
- `Fig. 3h` (다른 셀 · 저배율 · 100 µm 막대): 단면 폭 figure-read ≈850 µm (본문 *"milled to a width of almost 1 mm"*) · Li 화살표 자리 figure-read ≈25–28 µm (층 경계 판독 거칢).
- `Fig. 3i,j` (확대 · 5 µm 막대 · EDS 선): Cu ≈53,000 cps (0–1.3 µm) → **Li (1.6–5.4 µm · EDS 0)** → C 두 꼭지 ≈40,000 cps (5.4–6.9 µm) → S ≈10,000 cps (> 7 µm · LPSCl) · **Ag ≈3,000 cps 는 3.2–4.9 µm 에만** ("Ag in Li" 표지 = Li 의 C 쪽 절반) [figure-read].  ⇒ 이 자리의 Li 는 ≈4–5.5 µm — 같은 셀 저배율 (≈25–28 µm) 과 4–5 배 다르다 (§10-③).
- 이론 두께: SI *"(applied charge of 2.5 mA/cm² for 2 hours)/(theoretical capacity of Li: 3482 mAh/g) … ≈27 µm"* — 실험은 2 mA cm⁻² × 2.5 h 로 곱은 같다 · 서론의 3860 mAh g⁻¹ 를 쓰면 **24.3 µm** [카드 산술] · 결론은 *"a 20–25 μm plated layer"*.
- **SIMS** (`Fig. S10` · ⁷Li⁺ · 113 nm 분해능 · 시야 45.2 × 45.2 µm² · 400 × 400 px · Xe⁺ 30 keV 1 nA · Hiden EQS): 기준 = 고순도 Li 를 치밀 LPS 펠릿에 500 MPa 상온 압착한 Li/LPS 이중층 → Li 영역 **38 : 100** (LPS = 100) · 도금 층 평균 **42 : 100** → *"overall consistent with plated Li"* · 차이는 밀링 면의 고르기 탓 · 도금 층 단면 프로파일은 ≈20–70 사이로 출렁인다 [figure-read].  본문 p.5 는 *"SIMS analysis for Li6+"* 라 적었다 (⁷Li⁺ 의 오기).
- **Ag 희박**: SI *"If the sputtered 100 nm thick Ag layer dissolved in the 20 µm plated Li layer … it would correspond to 0.5 vol.% and 8.9 wt.% Ag in Li, which explains the low intensity Ag EDS signal"* → **0.63 at%** [카드 산술] · 5 mAh cm⁻² 전량에 녹으면 **0.52 at%** [카드 산술].

**충전 뒤 — C-Cu (Ag 없음) · 같은 조건** (`Fig. S11` · SI S-14)
- 본문: *"the displacement of the C interlayer and the plating of an approximately 10-20 µm thick Li layer onto the current collector, i.e. somewhat less uniform"* · *"While the C-Cu interlayer arrangement (i.e. no Ag) also facilitated plating of metallic Li on charging, full-cell cycling, rate capability, and single-charge investigations all showed the positive effect of adding the sputtered Ag layer."*
- figure-read: 화살표 자리 Li ≈10 µm · Li 자리에 기둥 · 섬유꼴 + 왼쪽 위에 신호 없는 빈 곳 (C 지도 검정) · **S 지도에 Cu\|Li 경계를 따라 가는 S 줄 + Li 자리 섬유에 S** (저자 언급 없음).

**방전 뒤 — Ag C-Cu (100 nm) · 2 mA cm⁻² 2.5 h → 1 mA cm⁻²** (`Fig. 4c–i` · `Fig. S12`)
- `Fig. 4c`: Cu (위) 와 Ag/C (아래 · LPSCl 위) 사이 **큰 공극** — figure-read ≈15 µm (이 자리) · "Li after stripping" = 밝은 실 · 조각 · 본문 *"There was a large void between the current collector (top of image) and the C interlayer/LPS separator (bottom of image)"* · 공극은 **모든 탈리 셀**에 있었고 시료 준비 · 평평한 밀링 · EDS 를 어렵게 했다 · *"Stripping voids were also likely widened after releasing the stack pressure during cell disassembly"*.
- `Fig. 4d–g`: C = LPSCl 곁 띠 · **Ag 밝은 점이 C 띠 가까이** · S 지도 위끝 (Cu 아래 경계) 에 가는 밝은 S 줄 [figure-read].
- `Fig. 4h,i` (EDS 선 · 10 µm 막대): Cu ≈21,000 → 15,000 cps (0–4 µm) → 4.3 µm 에서 Cu 끝 + **S 작은 혹 ≈1,500 cps** → "Stripped Li" (4.5–10 µm · 신호 0) → Ag/C (10–11.8 µm · C ≈5,500 · **Ag ≈700 cps 혹이 C 혹과 겹침**) → LPSCl S ≈5,000 cps (> 12.5 µm) [figure-read].
- 본문: *"The Ag signal suggested that Ag, "left behind" when the Li was stripped away, reprecipitated onto the C particulate rather than onto the current collector"* · *"The Li "filaments" shown in Figure 4c,i were attributed to incomplete Li stripping at the anodic current collector/SE interface during discharge, potentially due to partial interfacial contact loss."*
- `Fig. S12` (같은 조건 다른 셀): Cu 바로 아래 남은 층 figure-read ≈1.5 µm (본문 *"some non-stripped Li remained next to the current collector"*) → 공극 ≈2 µm → Ag/C → LPSCl · Ag 점은 C 띠와 남은 층 아래 경계 둘 다 · **S 지도에서 그 '남은 Li' 층이 LPSCl 만큼 밝다** [figure-read] — Li 는 EDS 로 안 보이므로 그 층이 Li 금속만은 아니라는 뜻이다 (해석 §10-⑥).

### 3-6. EIS (p.5 · SI S-9–S-10 · `Fig. S5`)
- 풀 셀 C-Cu · Ag C-Cu · 1 · 5 · 10 사이클 뒤 · 60 °C · 4 MPa · **10 mHz–10 kHz** · 10 mV · 맞춤 (Ag C-Cu 1 사이클) = **R1 – (Q2 ‖ R2) – W3** · **R1 123.9 Ω · R2 175.5 Ω · Q2 0.4896 × 10⁻³ F s^(α−1)** (α 미기재).
- 본문: *"a typical ionic conductivity for LPS of ∼1.6 mS/cm and a stable response up to 10 cycles. The Ag nanolayer on the 1 μm C did not produce a resolvable change in impedance over the first 10 cycles despite the reduction in Li nucleation overpotential"* → *"the primary benefit is the easy processing and scalability of the thin Ag/C interlayer, rather than inducing a lower interfacial impedance"*.
- figure-read: 고주파 첫 점 C-Cu ≈240 Ω · Ag C-Cu ≈200 Ω (맞춤 그림 ≈195 Ω) · 작은 호 끝 ≈305 / ≈255 Ω (Ag C-Cu 10 사이클 ≈285 Ω) · 그 뒤 확산 꼬리.
- [카드 산술] 식 (1) σ = t/(A R_t) · t 0.1 cm · A 0.196 cm²: **R1 + R2 (299.4 Ω) → 1.70** · R1 만 → 4.11 · 고주파 첫 점 (≈200 Ω) → ≈2.6 mS cm⁻¹ — 본문 1.6 은 **R1 + R2** 로 푼 값과 맞는다 (t = 0.94 mm 면 정확히 1.60).  Q2 가 mF 급이라 R2 는 SE 벌크 · 입계가 아니라 **계면형 저항**일 가능성이 크다 [카드 해석] · 10 kHz 상한으로는 SE 벌크 반원이 안 보인다.

### 3-7. 카드 산술 모음 (원문에 없는 값 — 식 · 가정 병기)

| 양 | 값 | 식 · 가정 |
|---|---|---|
| 치밀 Li 두께 per 면적 용량 | **4.85 µm per mAh cm⁻²** | 3.6 Q M_Li / (F ρ_Li) · M 6.941 g mol⁻¹ · ρ 0.534 g cm⁻³ |
| 5 mAh cm⁻² (3 전극 사후 셀) | **24.3 µm** | 위 × 5 · SI 27 µm 는 3482 mAh g⁻¹ 를 써서 11 % 크다 |
| NMC 면 적재 | 15.3 mg cm⁻² | 4 mg × 0.75 ÷ 0.19635 cm² |
| 풀 셀 면적 용량 | 첫 충전 ≈3.56 · 첫 방전 ≈3.10 mAh cm⁻² | 233 · 203 mAh g⁻¹ (`Fig. S9` figure-read) × 15.3 mg cm⁻² |
| 1 mA cm⁻² 의 C-율 | ≈0.32C (2 → 0.65C · 3 → 0.97C) | j ÷ 3.10 mAh cm⁻² (방전 용량 기준) |
| 풀 셀 한 번 충전의 치밀 Li | ≈17 µm | 3.56 × 4.85 |
| Ag 면 질량 | 0.105 mg cm⁻² (100 nm) · 0.093 (89 nm) | × ρ_Ag 10.49 g cm⁻³ [가정 = 벌크 밀도] |
| Li 속 Ag 농도 | 0.52 at% (5 mAh cm⁻² 전량) · 0.63 at% (20 µm 층) · 0.73 at% (풀 셀 3.56 mAh cm⁻²) | Ag 9.7 × 10⁻⁷ mol cm⁻² ÷ Li 몰 |
| Ag 가 담을 수 있는 Li (Li₁₀Ag₃ 까지) | ≈0.087 mAh cm⁻² = 5 mAh cm⁻² 의 **1.7 %** | Li/Ag 3.33 × 9.7 × 10⁻⁷ mol × 96485 ÷ 3600 |
| C 가 담을 수 있는 Li (LiC₆) | ≈0.03–0.05 mAh cm⁻² = **0.5–1 %** | 두께 0.5–0.75 µm × (1 − 0.185) × 1.8–2.2 g cm⁻³ [가정 · 결합제 무시] × 372 mAh g⁻¹ |
| ⇒ 층이 '호스트' 로 담는 몫 | **≲ 3 %** | 나머지 ≳ 97 % 는 Li 금속 — 실제로 Cu \| C 사이 Li 층으로 보인다 |
| Ag 양 비교 | `kang2026_…` Ag–C ≈0.22 mg cm⁻² (7.8 µm × 1.25 g cm⁻³ × Ag 0.23) · `spencerjolly2023_…` Ag–흑연 ≈0.30 mg cm⁻² (5 µm × 5.7 vol% × 10.49 g cm⁻³) | [다른 카드 값으로 카드 산술] — 층은 5–10 배 얇아도 Ag 양은 그 1/2–1/3 이다 |
| 압축 전 기공률 (질량 보존 역산) | ≈70–90 % | φ₀ = 1 − (1 − 0.185) t₁/t₀ · t₀ 2.1–3.2 µm (`Fig. S2a`) · t₁ 0.47–0.74 µm (`Fig. 1d`) · 다른 시료 · 다른 자리라 참고값 (§10-②) |
| CE 누적 | 0.99¹⁰⁰ ≈ 0.37 · 0.98¹⁰⁰ ≈ 0.13 | 무음극 = Li 저장고 없음 |
| SE 분리막 상대밀도 | ≈0.93 (두께가 정확히 1 mm 라면) | 30 mg ÷ (1.64 g cm⁻³ × 0.19635 cm² × 0.1 cm) · 1.64 는 [가정] |
| 하중 | 500 MPa → ≈9.8 kN · 250 MPa → ≈4.9 kN · 4 MPa → ≈79 N (Ø 5 mm) | P × 0.19635 cm² |
| 3 전극 iR (SE 1 mm 전부) | 2 mA cm⁻² 에서 125 mV (σ 1.6) · 49 mV (σ 4.1) | j t / σ — RE 가 보는 몫은 그 일부 (§3-4) |

---

## 4. 계산 방법 ★ — 이 논문에는 없다 (실험 방법을 대신 적는다)

- **code / functional / pseudo / k-points / ecut / supercell**: n/a — DFT · AIMD · MLIP · 연속체 · DEM **없음**.
- **무질서 처리**: n/a.
- **실험 장비 · 설정 (SI S-2–S-4 · 원문 그대로)**:
  - **단면 SEM/EDX**: 시료를 Ti 날에 붙여 **Ar 광폭 이온 밀링** (Gatan PECS II · 8 kV) → Zeiss Merlin FEG-SEM + Oxford Instruments X-max EDX · **10 kV** (`Fig. 1d–g` · `Fig. S1`–`Fig. S3`).
  - **P-FIB**: Thermo Fisher Helios G4 PFIB CXe DualBeam (**Xe⁺** 플라스마) · 단면 · 연마 · 전자 SE 상 5 · 10 kV · 1.6 nA · 이온 유도 SE (iSE) 30 kV · 0.1 nA · EDS = Oxford Ultim Max 170 SDD (Ag · C · Cu · S · Li 제외) · Aztec 4.1 SP1 · 시야 **52.1 × 35.8 µm²** · 1024 × 704 px (`Fig. 3` · `Fig. 4` · `Fig. S11` · `Fig. S12`).
  - **SIMS**: Hiden Analytical EQS · **⁷Li⁺** · 공간 분해능 **113 nm** · 시야 45.2 × 45.2 µm² · 400 × 400 px · Xe⁺ 30 keV · 1 nA · Hiden SIMS MAPPER 2.0.0.5 (`Fig. S10`).
  - **Raman**: Horiba JY LabRam Aramis 공초점 · 532 nm · 1 % · 30 s × 16 · ×50 ELWD · 100–3000 cm⁻¹ (`Fig. S4`).
  - **광학 조도**: µSurf Nanofocus 백색광 공초점 · 320-S (50×) · dR max ±0.5 · n = 40 · cutoff 800 µm · Gauss 회귀 필터 · 수평 차수 1 (`Table S1`).
  - **EIS**: 10 mHz–10 kHz · 10 mV · EC-Lab 등가회로 (`Fig. S5`).
  - **셀 장치**: 4 MPa 일축 · 60 °C · Ar 안 자체 장치 (ref 36 = `doerrer2021_…`).
- **이 논문이 하지 않은 것**: 상 동정 (XRD · operando) · 계면 화학 (XPS · ToF-SIMS) · 점착 · 박리 측정 · 압력 측정 (적층압 고정값뿐) · 속도론 (교환 전류) · 모델링 — 그래서 '합금' · 'LiC₆' · '촉매' 는 모두 **해석**이다 (§10-⑦ · ⑪).

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나 — 실독) | 우리 활용 |
|---|---|---|
| 1a–c | 스퍼터 모식 (Ag 타깃 · Ar⁺ · 떨어지는 Ag 원자 · 시편대 위 Cu 박 9 µm + C 코팅 1 µm) · 펠릿 풀 셀 (PEEK 몰드 · Ø 5 mm LPS · 양극 위 · Ag C-Cu 아래) · 3 전극 (Ø 2 mm WE 아랫면 · Ø 3 mm CE · Ø 1 mm RE 윗면) | 층 순서 (Cu → C → Ag → SE) 의 원문 그림 · RE 가 CE 쪽 면 → WE–RE 전압에 SE iR 일부가 섞임 (§3-4) |
| 1d–g | 500 MPa 압축 뒤 단면 BSE + Cu · C · Ag EDS — 층 figure-read ≈0.5–0.75 µm · Ag 가 위쪽 C 입자를 감싼 밝은 띠 · 박리 없음 | 조립 직후 접촉 쌍 = LPSCl–Ag · Ag–C · C–Cu (§0-1 ②) |
| 2a,b | C-Cu · Ag Cu 풀 셀 1 · 2 · 5 · 10 사이클 (한 셀씩) — 화살표 −62 · −53 % = 세 셀 평균 유지율 · "Polarisation" 꺾임 | 유지율 = C10/C1 (충전) 정의 확인 (§3-3) |
| 2c,d | (c) 첫 사이클 세 셀씩: Ag C-Cu 방전 ≈193–212 vs C-Cu ≈160–167 mAh g⁻¹ · 충전 곡선은 겹침 · +25 % · (d) Ag C-Cu 한 셀 1 · 2 · 5 · 10 사이클 — 방전 ≈202 → 160 · 화살표 −41 % (평균) | 첫 효율 차 (86 vs 71 %) 가 Ag 효과의 대부분 · (d) 의 셀은 세 셀 중 가장 좋은 셀로 보인다 (대표 셀 편향) |
| 2e,f | Ag C-Cu 두 셀 100 사이클: 충전 ≈232 / 228 → ≈93 / 64 mAh g⁻¹ · CE 첫 ≈87 / 75 % → ≈99 % | 무음극 = CE 99 % 도 100 사이클에 ≈37 % 남는다 |
| 3a,b | (a) 1 mA cm⁻² × 1 h 첫 도금 (steel · Cu · C-Cu · Ag C-Cu · 1 셀씩) — 꼭지 ≈ −26 / −18 / −17.5 / −18 mV · 꼭지 − 평탄 ≈16.7 / 7.5 / 2 / 0 mV · Cu 는 3.25 h 에 "Charging failure" · (b) 2 mA cm⁻² × 2.5 h (C-Cu 3 · Ag C-Cu 3 셀 — 본문 평균은 5 셀) — 꼭지 − 평탄 ≈17 vs ≈3.7 mV · 평탄은 겹침 | ★ 핵생성 과전압 순서 앵커 · 판독법 = 꼭지 − 평탄 (§3-4) · 16.1 vs 3.9 mV (n 5 · std err) 의 그림 근거 |
| 3c–g | 5 mAh cm⁻² 충전 뒤 단면 SE + Cu · S · C · Ag EDS — 위에서부터 Cu / Li (화살표 자리 figure-read ≈14 µm) / 밀려난 C / LPSCl · 왼쪽에 Cu 에 붙은 C 조각 · Ag 희미 | ★ Li 위치 = Cu–C 사이 · C 는 SE 쪽 |
| 3h–j | 다른 셀 저배율 (폭 ≈850 µm · Li ≈25–28 µm) + 확대 + EDS 선 (Cu 0–1.3 · Li 1.6–5.4 · C 5.4–6.9 · LPSCl > 7 µm · Ag ≈3,000 cps 는 3.2–4.9 µm) | 같은 셀 안에서 Li 두께가 4–5 배 다르다 · Ag 는 Li 의 C 쪽 절반 |
| 4a,b | 2 mA cm⁻² 2.5 h 충전 → 1 mA cm⁻² 방전 (2 셀) — OCV ≈1.9–2.0 V · 도금 −15…−33 · 탈리 +8…+17 mV · 끝 ≈8.6–8.9 h 에 5 V | 왕복 효율 ≈80 % (figure-read 74–78 %) |
| 4c–i | 방전 뒤 단면 — 위에서부터 Cu / 공극 (+ Li 잔여 실) / C + Ag 덩어리 / LPSCl · S 지도 위끝 가는 S 줄 · 선 스캔 4.3 µm 의 S 혹 · Ag 혹 = C 혹 | 다음 사이클 핵생성 면 = C 위 Ag 덩어리 · Cu 쪽 S (§10-⑥) |
| 5 | 작동 모형 모식 (스퍼터 → 충전 시작 (Ag/C 위 · Cu–C 사이 얇은 Li) → 충전 끝 (Ag 가 퍼진 Li 층 · C 는 SE 쪽) → 방전 끝 (공동 · C 위 Ag · Cu 위 Li 잔여)) | 단계별 접촉 쌍 표 (§0-1) 의 원문 그림 |
| S1 | 위에서 본 SE 상 + 사진: C-Cu (≈0.1 µm 입자 응집 · 검정) · Ag 100 nm (둥근 알갱이 ≈0.15–0.25 µm · 은빛) · Ag 500 nm (마디 ≈0.3–0.4 µm · 틈 메움) | 탄소 형상 = 카본블랙꼴 응집체 · Ag 막 형태 |
| S2 | 스퍼터 직후 (압축 전) 단면 SE · BSE + Ag · C · Cu EDS — 층 figure-read ≈2.1–3.2 µm · Ag **89.32 nm** · Ag 는 위쪽에 몰림 | ★ Ag 위치 = C 윗면 · 두께가 '∼1 µm' 와 어긋남 (§10-①) |
| S3 | 압축 전 · 뒤 단면 SE 와 기공 문턱 지도 (ROI ≈1.5 × 11.4 / 0.5 × 5.7 µm) — 26.7 → 18.5 % | 2D 문턱 기공률의 한계 (§10-②) · DEM 입력으로 안 씀 |
| S4 | Raman: D 1359 · G 1588 · 2D 2689 cm⁻¹ · 높이비 I_D/I_G figure-read ≈1.3 (바탕 빼면 ≈1.4) · D–G 골 높음 · 1100–1250 어깨 | ★ 탄소 모형 = 결함 많은 흑연질 (§0-1 · §8-③) |
| S5 | Nyquist C-Cu · Ag C-Cu (1 · 5 · 10 사이클) + R1–(Q2‖R2)–W3 맞춤 (R1 123.9 · R2 175.5 Ω · Q2 0.49 mF s^(α−1)) · 고주파 첫 점 ≈240 / ≈200 Ω | σ ≈1.6 = R1 + R2 로 푼 값 — σ 로 인용 안 함 (§10-⑤) |
| S6 | Ag 500 nm 풀 셀 한 셀 — 첫 충전 ≈190 · 방전 ≈148 → 10 번째 ≈88 / 80 · −63 % · 첫 충전 평탄 ≈3.65–3.7 V | 두꺼운 Ag = 분극 ↑ (원인 미분리) |
| S7 | 속도 첫 사이클: C-Cu 1 / 2 · Ag C-Cu 1 / 2 / 3 mA cm⁻² — "Charging failure" = 충전 ≈450 / ≈500 mAh g⁻¹ | Ag 가 2 mA cm⁻² 첫 충전 단락을 막음 — 첫 사이클만 |
| S8 | 0.1 mA cm⁻² 활성화 (3.53–3.78 V) 뒤 1 mA cm⁻² (3.53–4.15 V) — ≈160 → ≈50 · −69 % | 활성화 효과 없음 · SOC 표기 뒤바뀜 (§10-⑫) |
| S9 | 다섯 구성 C1 / DC1 / C10 / DC10 평균 ± std err | ★ 유지율 정의 역산의 근거 (§3-3) |
| S10 | SIMS ⁷Li 단면: 기준 Li/LPS 이중층 Li 38 : LPS 100 · 도금 층 평균 42 : 100 (프로파일 ≈20–70 출렁) | Li 함유 확인일 뿐 — 금속 Li 판정은 약하다 |
| S11 | C-Cu (Ag 없음) 충전 뒤 단면 + C · Cu · S — Li ≈10 µm · 기둥 · 섬유꼴 + 빈 곳 · Cu–Li 경계 S 줄 | Ag 없을 때 Li 형태 대조 · Cu 쪽 S (§10-⑥) |
| S12 | 다른 Ag C-Cu 셀 방전 뒤 + Cu · C · Ag · S — Cu 곁 남은 층 ≈1.5 µm + 공극 ≈2 µm + C/Ag · 남은 층이 S 지도에서 밝다 | '남은 Li' 에 S — 정체 미확인 (§10-⑥) |
| Table S1 | 조도 Sa · Sq — 10 구성 (steel · Cu · Ag-Cu · C-Cu · Ag C-Cu 100 / 500 nm · 압축 전 · 뒤) | DEM · 접촉 모델의 표면 거칠기 입력 (§3-2) |

---

## 6. Post-processing ★

- **무엇**: EIS 등가회로 맞춤 → 식 (1) σ = t/(A R_t) (*"Rt = total Ohmic resistance"*) · SEM 단면 회색조 문턱 → 면적 기공률 · 광학 공초점 → Sa · Sq · Raman → 띠 위치만 (I_D/I_G 숫자 안 냄) · EDS 지도 · 선 스캔 (cps) · SIMS 상대 세기 (**LPS 영역 = 100** 으로 정규화) · 충방전 곡선 → 용량 · CE · 유지율 · 3 전극 꼭지 → 핵생성 과전압 · 탈리 시간 → 왕복 효율.
- **도구**: EC-Lab (BioLogic) · ImageJ · Batalyse "Data Analysis" · Aztec 4.1 SP1 · Hiden SIMS MAPPER 2.0.0.5 · µSurf 소프트웨어 (Gauss 회귀 · 수평 1 차).
- **수치화 · 기록 방식**: 평균 ± **std err** · 용량 = NMC 질량 기준 · '유지율' = C10/C1 (충전 — 본문에 정의 없음 · `Fig. S9` 로 역산) · 핵생성 과전압 정의 없음 · 자료 공개 문장 [미확인].
- **우리가 가져올 꼴**: ① 유지율 · 효율의 **정의를 숫자 옆에 적는다** (이 논문은 안 적어서 역산해야 했다) ② 핵생성 과전압은 **꼭지 · 평탄을 어느 시점에서 읽었는지** 같이 적는다 ③ 3 전극은 RE 위치와 iR 처리를 적는다 ④ SIMS 는 기준 시료 (Li/LPS 이중층) 로 정규화한 상대 세기 — 금속 판정이 아니라 'Li 함유' 판정으로만.

---

## 7. 우리 DFT 대비 (comp1 / modelc · DEM 점착 트랙)  →  `our_dft_baseline.md`

| 항목 | 이 논문 | 우리 | 같다 / 다르다 / 왜 |
|---|---|---|---|
| A 이온전도 (LPSCl) | ≈1.6 mS cm⁻¹ (풀 셀 EIS · 10 kHz 상한 · R1 + R2 로 풀린 값으로 보임 · 60 °C 운전 셀) | MLIP-MD (UMA) D · σ — 절대값은 인용하지 않는다 (계 간 상대차만) | **비교 안 함** — ① 측정 정의 (계면형 R2 가 섞였을 가능성) ② 우리 인용 정책 ③ 온도 (60 °C) |
| B 환원 쪽 (Li 금속 전위) | SEI 화학 미측정 · Cu 쪽 S 신호 (figure-read · 저자 언급 없음) · Ag C-Cu WE 의 OCV ≈1.9–2.0 V (figure-read `Fig. 4a`) | grand-potential 환원 쪽 가장자리 (`our_dft_baseline.md` · 라벨은 원장 `HZ-esw-reduction-limit-label` CONDITIONAL) — Li 금속 전위 (0 V) 는 그보다 한참 아래 | **정성 일치** — Li 와 닿는 LPSCl (C 가 끊긴 곳 · SE 파편) 은 열역학적으로 환원된다.  값 비교 없음 · OCV 는 혼합 전위라 안정창과 견주지 않는다 |
| C 기계 | 없음 (조도 · 2D 기공률만) | E_VRH · B₀ (DFT 탄성 · EOS) | 해당 없음 |
| D 전자구조 | 없음 | band gap (fixed-occ nscf) | 해당 없음 |
| ★ Li 친화성 · 점착 (DEM 트랙) | 핵생성 과전압 순서 · 단계별 접촉 쌍 · Ag 위치 변화 · 탄소 Raman | W_ad 보고서 §2 (C–C · Ag–C · LPSCl\|Ag(111) · LPSCl\|흑연 — **값은 그 보고서에서만**) · §7 Li 친화성 (제안 · 미계산) | 이 논문은 **'어느 쌍이 언제 중요한가'** 와 **탄소 모형 행**을 준다 — 맞출 값은 없다 (§0-1 · §8) |
| (곁) 같은 Ag–C 계열 · 우리 그룹 실험 | 층 < 1 µm · Ag 0.105 mg cm⁻² · 4 MPa · 60 °C · Ø 5 mm | `kang2026_…`: Ag–C 7.8 µm · Ag ≈0.22 mg cm⁻² [카드 산술] · 20 MPa · 45 °C · Ø 13 mm | 조건이 다 달라 값을 같은 줄에 두지 않는다 — Ag 양 기준 차이는 ≈2 배뿐이라는 것만 |

⚠ 이 논문은 DFT 를 하지 않았으므로 **'방법 의존성 (functional · 이온 이완 · k-점) 때문에 다르다' 라는 판정이 없다** — 대신 실험 쪽 방법 의존성 (유지율 정의 · η 정의 · iR · 2D 기공률 · EDS 분해능) 을 §10 에 적었다.

---

## 8. 적용 인사이트 (우리 연구에 어떻게)

- ① **W 쌍 목록에 C\|Cu · Li\|Cu · Li\|C (리튬화) 가 빠져 있다** — 이 구조에서 Li 는 Cu \| C 사이로 들어가 C 를 SE 쪽으로 밀어낸다 (`Fig. 3c–j` · `Fig. S11` · `Fig. 5`).  즉 **운전 중 처음 벌어지는 계면은 C\|Cu** 이고, 그 뒤 Li 가 만나는 면은 Cu (아래) 와 C (위) 다.  W_ad 보고서 §2 의 네 쌍 (C–C · Ag–C · LPSCl\|Ag(111) · LPSCl\|흑연) 만으로는 이 구조의 '어디가 먼저 갈라지나' 를 못 묻는다.  `liao2025_…` 의 구도 (탄소/SE 점착이 크면 Li 가 집전체 쪽으로) 와 같은 그림이지만, 이 논문은 점착을 **재지 않았다** — 순서 관찰이지 G_c 나 W 의 대조 값이 아니다.
- ② **LPSCl\|Ag(111) 쌍의 쓰임새는 '첫 충전 전' 으로 한정된다** — 조립 (500 MPa) 직후 SE 와 닿는 면은 Ag 지만, 첫 충전 뒤 Ag 는 Li 속으로 흩어지고 SE 쪽 면은 **LPSCl\|C** 가 된다 (+ 방전 뒤 C 위 Ag 덩어리).  DEM 박리 입력을 '운전 중' 계면에 쓰려면 LPSCl\|C (보고서 §2-4) 쪽이 대표다 [카드 해석].
- ③ **탄소 모형은 '결함 많은 탄소' 행** — Raman I_D/I_G figure-read ≈1.3–1.4 (532 nm) 는 결함 없는 흑연 기저면과 거리가 멀다 (`kang2026_…` 의 고결정 CNF 0.19 · 저결정 CNF 0.99 보다도 크다 [다른 카드]).  W_ad 보고서 §7-1 표로는 **빈자리 결함이 있는 기저면** + **흑연 기저면 LiC₆** (2D 띠가 있어 쌓인 영역도 있다) 가 후보이고, CNF 헤링본 가장자리 행은 아니다.  작용기 (O · N) 는 XPS 가 없어 정할 수 없다 — 결함 · 작용기 밀도는 계산 입력이 아니라 실험값을 받아야 한다 (보고서 §7-1 의 단서 그대로).
- ④ **'합금 구동력' 의 끝 상태는 희박 Li(Ag)** — 100 nm Ag 가 5 mAh cm⁻² Li 에 다 녹으면 ≈0.5 at% [카드 산술] 이라, 이 구조에서 계산할 것은 LiAg · Li₉Ag₄ · Li₁₀Ag₃ (`spencerjolly2023_…` 경로) 만이 아니라 **bcc Li 속 Ag 치환 용해 에너지**와 **Ag 의 Li 표면 · 계면 편석 경향**이다.  ⚠ 방전 뒤 Ag 가 C 위에 남는 것을 'Ag\|C 친화성 > Ag\|Cu' 의 증거로 쓰지 않는다 — 탈리가 C 쪽 (SE 쪽) 에서 시작해 Ag 가 거기 남는 **기하** 로도 설명되고, 원문은 둘을 가르지 않는다 [카드 해석].
- ⑤ **핵생성 과전압은 '순서' 앵커로만** — steel > Cu > C-Cu ≳ Ag C-Cu (1 mA cm⁻² · 1 셀씩 · figure-read) · C-Cu 16.1 > Ag C-Cu 3.9 mV (2 mA cm⁻² · n 5).  DFT 친화성 순서와 맞대 보되 **크기는 견주지 않는다** — 복합 층 전체의 경로 값이고 (Ag 는 SE 쪽 · 핵은 Cu 쪽), 평탄 전압에는 iR 이 섞여 있다 (§3-4).  보고서 §7 '할 수 없는 것' 에 적힌 '핵이 생길 때의 과전압' 을 실험 쪽에서 채우는 값이지, 계산 결과의 검증 표적은 아니다.
- ⑥ **연속체 · DEM 에 바로 쓸 형상** — 층 < 1 µm (figure-read ≈0.5–0.75 µm) · Ag 89–100 nm · 조도 Sa (`Table S1`) · 조립 500 MPa · 운전 4 MPa · Li ≈20 µm (자리마다 4–28 µm) 가 **1 µm 탄소 '껍질'** 을 밀어낸다 · 탈리 뒤 Cu \| C 사이 공극 (하중 해제로 넓어졌을 수 있다 — 저자).  ⇒ DEM 에서 이 탄소 층은 '두꺼운 다공 호스트' 가 아니라 **SE 에 붙은 얇은 막 + Cu 와의 약한 계면**으로 두는 것이 이 관찰과 맞다 [카드 해석].  2D 기공률 18.5 % 는 입력 · 보정 표적으로 쓰지 않는다 (§10-②).
- ⑦′ **같은 1저자 전작과 합치면** — 전작 (ref 30 · `metzler2025_…` · 분무 Ag/카본블랙 층) 은 Ag 의 **위치** (집전체 쪽 몰기 vs 고르게) 만 바꿨을 때 *"there was no resolvable nucleation potential difference between unstructured and structured interlayers"* 였고 (스테인리스 대비 둘 다 *"∼13 mV less"*), 첫 방전 172 → 198 mAh g⁻¹ · ICE 72 → 83 % 는 위치에서 갈렸다 [전작 원문 PDF 에서 확인 · 2026-11-24].  이 논문은 Ag 의 **유무**를 바꿔 핵생성 과전압이 16.1 → 3.9 mV 로 갈렸다.  ⇒ 두 편을 같이 읽으면 **'Ag 가 있느냐' 가 핵생성 꼭지를, 'Ag 가 어디 있느냐 · 층 구조' 가 첫 효율 · 석출 위치를 정한다** 는 가설이 된다 [카드 해석 — 두 편의 탄소 · 셀이 달라 같은 실험 계열의 결론은 아니다].  DFT 로 옮기면: Li 친화성 (흡착 · W) 은 핵생성 쪽, 층 순서 · 계면 쌍은 석출 위치 쪽 질문이다.
- ⑦ **호스트 몫 ≲ 3 %** [카드 산술 §3-7] — Ag (Li₁₀Ag₃ 까지 1.7 %) + C (LiC₆ 0.5–1 %) 가 담는 Li 는 충전량의 몇 % 뿐이라, 이 층은 Li 를 '담는' 층이 아니라 **핵생성 · 수송을 거드는 층**이다.  `kang2026_…` 의 CNF 층 (Li 를 기공에 담아 압력 요동을 줄이는 설계) 과 역할이 다르다.

---

## 9. 인용 가능 문장 (deck/paper 용 — 조건을 떼지 않는다)

- "A ≈100 nm sputtered Ag film on a commercial ≈1 µm carbon-coated Cu foil reduced the Li nucleation overpotential in Li₆PS₅Cl three-electrode cells from 16.1 ± 1.1 mV (carbon only) to 3.9 ± 1.1 mV (2 mA cm⁻², 60 °C, 4 MPa; mean ± standard error, n = 5)." — *ACS Appl. Energy Mater.*, 9, 9817 (2026).
- "In this bilayer, Li plated between the Cu current collector and the carbon layer, which was displaced toward the separator; Ag was dispersed in the plated Li after charge and was found on the carbon after discharge (PFIB-SEM/EDS)." — 같은 출처.
- "Anode-free NMC83 | Li₆PS₅Cl cells with the sputtered Ag/C bilayer delivered 203 mAh g⁻¹ initial discharge capacity and 86 % initial Coulombic efficiency at 1 mA cm⁻², versus 163 mAh g⁻¹ and 71 % without Ag (n = 3, 60 °C, 4 MPa)." — 같은 출처.
- "Stripping left large voids between the Cu current collector and the carbon layer and residual Li filaments." — 같은 출처.
- ⛔ 쓰지 말 것: 'Ag is catalytic' (속도론 측정 없음) · 'comparable to 10–20 µm Ag/C layers' (저자 스스로 조건이 달라 *"definitive comparisons difficult"*) · '10-cycle retention 59 %' 를 방전 기준 유지율처럼 (정의 = C10/C1 충전) · 'σ = 1.6 mS cm⁻¹' 를 LPSCl 물성값으로.

---

## 10. 주의 / 한계 (over-claim 방지)

- ① **C 층 두께** — "∼1 µm" 는 공급사 값이다.  스퍼터 직후 (압축 전) 단면 `Fig. S2a` 는 figure-read ≈2.1–3.2 µm (1 µm 막대 70 px 로 자리마다 잼) · 500 MPa 압축 뒤 `Fig. 1d` 는 ≈0.5–0.75 µm.  본문의 '1 µm' 는 압축 전 실측과 맞지 않고, 셀 안의 층은 '<1 µm' 가 맞다.
- ② **기공률** — 26.7 → 18.5 % (ImageJ 2D 문턱 · 저자도 *"challenging to reliably quantify"*).  압축 전후 두께가 2–3 배 줄었는데 기공률은 8 %p 만 줄었다 — 질량 보존으로 풀면 압축 전 ≈70–90 % [카드 산술] 이어야 한다.  두 그림은 다른 시료 · 다른 자리이고 가로 흐름도 있을 수 있어 결론은 아니지만, **18.5 % 를 DEM 입력 · 보정 표적으로 쓰지 않는다**.  또 std err 은 n ≈5 로 계산된 값이다 ((sd/se)² = 5.1 · 5.4) — 본문은 '세 단면'.
- ③ **Li 두께 · 균일성** — 같은 셀 안에서 저배율 (`Fig. 3h`) figure-read ≈25–28 µm vs 확대 · 선 스캔 (`Fig. 3i,j`) ≈4–5.5 µm · 다른 셀 `Fig. 3c` ≈14 µm (그림 축척 그대로) · 본문 "∼20 µm" · 결론 "20–25 μm".  *"reasonably uniform"* 은 정성 판정이다.  SI 이론 두께 27 µm 는 Li 용량 **3482 mAh g⁻¹** 를 썼다 (서론은 3860 · 맞는 값은 24.3 µm [카드 산술]) · SI 산식에 *"2.5 mA/cm² for 2 hours"* · *"Ag/CB working electrode"* 같은 전작 (ref S16) 표현이 남아 있다 (곱 5 mAh cm⁻² 는 같다).
- ④ **유지율 정의 · 대표 셀** — '유지율' 은 C10/C1 (충전) 이다 (`Fig. S9` 역산 · 본문 정의 없음) — 첫 사이클 비가역 (71 vs 87 %) 이 섞여 Ag 효과가 커 보인다 (방전 기준이면 우위 21 → 15 %p).  `Fig. 2d` 는 세 셀 중 가장 좋은 셀로 보이고 (10 번째 충전 ≈168 vs 평균 139 ± 11.5), 100 사이클은 **2 셀** · 그중 셀 2 는 첫 CE ≈75 % (본문 평균 86 % 보다 낮다 — 같은 세 셀인지 [미확인]).
- ⑤ **EIS 의 σ ≈1.6 mS cm⁻¹** — R1 + R2 (299.4 Ω) 로 식 (1) 을 풀면 1.70 이 나와 본문과 맞고, R1 만이면 4.11 · 고주파 첫 점이면 ≈2.6 [카드 산술].  Q2 ≈0.5 mF 급이라 R2 는 계면형일 가능성이 크고 10 kHz 상한으로는 SE 벌크가 안 보인다 → **σ 로 인용하지 않는다**.  '두 구성의 임피던스 차이 없음' 도 고주파 첫 점이 ≈240 vs ≈200 Ω 으로 셀마다 다른 흩어짐 안에서의 판정이다.
- ⑥ **Cu 쪽 S 신호 (그림 판독 · 저자 언급 없음)** — `Fig. S11d` (C-Cu 충전 뒤 · Cu\|Li 경계의 가는 S 줄 + Li 자리 섬유의 S) · `Fig. 4e,h` (Ag C-Cu 방전 뒤 · Cu 아래 경계 S 줄 · 선 스캔 4.3 µm 의 S 혹) · `Fig. S12e` (방전 뒤 'non-stripped Li' 층이 LPSCl 만큼 밝다).  충전 뒤 Ag C-Cu (`Fig. 3e`) 에는 Cu 쪽 S 가 안 보인다.  가능성: Cu–S 부식 생성물 · Li₂S 를 품은 SEI · SE 파편 · Xe⁺ 밀링 재증착 — **그림만으로 못 가른다**.  저자가 p.4–5 에서 걱정한 Cu–LPS 부반응을 직접 확인할 수 있었던 자료이고, '남은 Li' 의 정체와 다음 사이클 핵생성 면 (Cu 냐 Cu 위 황화물 막이냐) 에 걸린다.
- ⑦ **Li–Ag 상 · LiC₆ · SEI 를 재지 않았다** (XRD · XPS · 사후 Raman 없음) — 'Ag 가 Li 에 녹았다' 는 희미한 EDS (≈0.5 at% 면 검출 한계 근처) + 선 스캔 한 줄 (Ag 는 Li 의 C 쪽 절반에만) 에서 나온 해석이다.  SIMS 는 Li 를 가진 상 전부를 보고, 42 vs 38 의 일치는 matrix 효과에 기댄 약한 '금속 Li' 판정이다.
- ⑧ **핵생성 과전압** — 정의 · iR 처리 미기재 · 그림은 5 셀 중 3 셀 · C-Cu 는 꼭지 뒤 2.5 h 내내 풀려 '평탄' 을 언제 읽느냐에 값이 걸린다 · 1 mA cm⁻² 비교는 셀 1 개씩 · *"stainless steel and Cu required the highest overpotential"* 은 꼭지 − 평탄 정의에서만 성립한다 (꼭지 절대값은 Cu · C-Cu · Ag C-Cu 모두 ≈ −18 mV) · 축 이름 *"voltage versus Li⁺/Li at the counter electrode"* 는 전작 (ref 30) 의 *"voltage versus Li⁺/Li counter electrode"* 와 같은 뜻 (Li 전극 대비 WE 전압) 으로 읽힌다 — 오기라기보다 어색한 표현이다 · 전작은 꼭지를 *"The sharp minima indicated the instant of Li plating"* 로만 정의했다.
- ⑨ **조도 비교의 기준이 섞였다** — *"Ag Cu 0.029 (압축 뒤) < 맨 Cu 0.167"* 은 압축 뒤 대 압축 전 (steel · Cu 는 압축 뒤 값이 없다) · *"100 nm Ag 가 거칠기를 거의 안 바꿨다"* 는 압축 뒤에만 맞다 (압축 전은 0.370 → 0.790 으로 2 배) · *"500 nm 가 거칠기를 줄였다"* 는 100 nm (0.790) 대비이고 원래 C-Cu (0.370) 보다는 거칠다 (0.427).
- ⑩ **"Cycling at up to 2 mA/cm²"** (p.4) — 2 mA cm⁻² 자료는 풀 셀 첫 사이클 (`Fig. S7`) 과 3 전극 한 번 충전뿐이다 · 그 첫 방전 ≈95 mAh g⁻¹ 은 1 mA cm⁻² 의 ≈절반.
- ⑪ **'catalytic'** (초록 · 결론) — 교환 전류 · 속도 상수를 재지 않았다 · 근거는 핵생성 꼭지 하나와 첫 용량 · 효율이다.
- ⑫ **`Fig. S8` SOC 표기** — SI 의 *"10 % SOC (4.16 V)"* · *"90 % SOC (3.53 V)"* 는 높낮이가 뒤바뀐 꼴이고, 그림의 활성화 곡선은 3.53–3.78 V 다 (서술의 '3.78–4.16 V' 와 다르다).
- ⑬ **서술 · 서지 불일치** — p.3 *"The use of pouch cells for the FIB microscopy post-cycle studies"* ↔ 셀은 PEEK 몰드 펠릿이다 (Li 박을 파우치 안에서 민 것을 가리키는지 [미확인]) · ref 27 의 제목 (*"… Thin Carbon Black Layer"*) ↔ 본문 *"an Ag-containing Ag/C interlayer"* [미확인] · ref 48 *"ACS Appl. Mater. Interfaces 2007, 16"* (16 권은 2024) · ref 58 *"Nat Mater. 2022, 9"* (권 표기 오기로 보임) · SI ref S14 *"Heliyon 2019, 9"* (9 권은 2023) · 본문 p.5 *"Li6+"* (⁷Li⁺ 의 오기).
- ⑭ **표본 · 오차** — 셀 3 · 5 · 2 · 2 개 · 오차는 std err 이라 sd 로 바꾸면 √n 배 (n 3 → 1.7 배 · n 5 → 2.2 배) 커진다.
- ⑮ **조건 한정** — 60 °C · 4 MPa · Ø 5 mm 펠릿 · 양극 4 mg · Li₆PS₅Cl ≈1 mm.  저자 스스로 두꺼운 Ag/C 층과의 비교는 전해질 · 셀 기하 · 적층압 · 적재 차이로 *"definitive comparisons difficult"* 라 하고 표준 실험실 셀 · 절차를 제안한다 (p.8) — 이 카드도 같은 이유로 `kang2026_…` · `spencerjolly2023_…` 값과 같은 줄에 두지 않는다.

---

## 11. 용어 미니 사전

- **스퍼터링 (sputtering)** — Ar⁺ 이온이 타깃 (여기선 Ag) 을 때려 튀어나온 원자가 기판에 쌓이는 물리 증착.  막 두께는 전류 · 시간 · 거리로 조절한다 (이 논문은 시간 · 속도를 안 적었다).
- **무음극 (anode-free)** — 처음에 Li 금속을 넣지 않고 양극의 Li 를 첫 충전 때 음극 집전체 위에 석출시켜 음극을 만드는 셀.  Li 저장고가 없어서 쿨롱 효율 손실이 그대로 용량 손실이 된다 (CE 99 % × 100 사이클 ≈ 37 %).
- **핵생성 과전압 (nucleation overpotential)** — 석출이 시작될 때 전압이 한 번 크게 내려갔다 (꼭지) 올라오는데, 그 꼭지와 뒤 평탄 (성장) 전압의 차.  새 상 (Li 핵) 을 만드는 에너지 장벽의 신호다.
- **3 전극 셀** — 작업 (WE) · 상대 (CE) · 기준 (RE) 전극.  WE − RE 전압을 보면 CE (Li 탈리) 쪽 과전압이 빠진다.  WE–RE 사이 전해질의 iR 은 RE 위치에 따라 일부 남는다.
- **BSE (후방산란 전자) 상** — 원자번호가 큰 원소 (Ag) 가 밝게 보인다.  **SE (2 차 전자) 상** — 표면 형상이 보인다.
- **P-FIB (plasma focused ion beam)** — Xe⁺ 플라스마 이온 빔으로 단면을 깎는다.  Ga FIB 보다 빨라 mm 폭 단면을 만든다.
- **EDS (EDX)** — 전자빔이 낸 X 선으로 원소 지도를 그린다.  Li 는 못 본다.  10 kV 에서는 공간 분해능이 수백 nm–1 µm 라 100 nm 막의 위치를 잘라 말하기 어렵다.
- **SIMS** — 이온빔으로 튀어나온 2 차 이온의 질량을 분석한다 — Li 를 본다.  세기가 주변 물질 (matrix) 에 따라 달라 절대 정량이 어렵다.
- **Raman D · G · 2D 띠** — G (≈1580 cm⁻¹) = 흑연 면 안 진동 · D (≈1350) = 결함 · 가장자리가 있어야 켜지는 띠 · 2D (≈2700) = D 의 2 차 (층 쌓임 정보).  I_D/I_G 가 클수록 결함이 많고 결정이 작다 · 비는 레이저 파장에 따라 달라진다.
- **Sa · Sq** — 표면 높이 편차의 산술 평균 · 제곱 평균 제곱근 (면 조도).
- **CPE (Q) · Warburg (W)** — 이상적이지 않은 축전기 · 확산 임피던스.  α 는 CPE 의 이상성 (1 이면 순수 축전기).  용량이 mF 급이면 보통 계면 (전극 · 전하 이동) 요소다.
- **쿨롱 효율 (CE) · 왕복 효율** — 방전 용량 ÷ 충전 용량 · 3 전극에서 석출한 Li 가운데 다시 뺀 몫.
- **std err (표준 오차)** — sd/√n — 평균의 불확실성.  셀 사이 흩어짐은 sd 로 본다.
- **희박 고용 (dilute solid solution)** — 한 원소가 다른 금속 결정 속에 소량 녹아 있는 상태 — 여기서는 Li 결정 속 Ag ≈0.5 at% [카드 산술].

---

## 12. 다음에 먹일 논문 (이 논문 참고문헌에서 · 최근 것 먼저 · 2026-11-24 litdb 대조)

| # | 논문 (이 논문의 ref 번호) | 왜 (우리 축) | litdb |
|---|---|---|---|
| 1 | Park, Naik, Vishnugopi, Mukherjee, Hatzell, "Lithium Kinetics in Ag–C Porous Interlayer in Reservoir-Free Solid-State Batteries", *Adv. Energy Mater.* 15, 2405129 (2025) (ref 54 · SI S5) | Ag–C 다공 층 안의 Li 수송 · 석출 위치 (기공률 ≈29 % 기준값의 출처) · 연속체 모델 축 | 카드 없음 (`kang2026_…` 등이 인용만) |
| 2 | Ko et al., "Mechanism of stable lithium plating and stripping in a metal-interlayer-inserted anode-less solid-state lithium metal battery", *Nat. Commun.* 16, 1066 (2025) (ref 51) | 금속 층의 위치 (집전체 쪽) 와 Li 석출 위치 — 층 순서 축 | 없음 |
| 3 | Xie, Diallo, Kim, Tu, Ceder, "The Microscopic Mechanism of Lithiation and Delithiation in the Ag/C Buffer Layer for Anode-Free Solid-State Batteries", *Adv. Energy Mater.* 14, 2302960 (2024) (ref 28) | Ag/C 층의 리튬화 · 탈리튬화 미시 기전 · Li–Ag 합금 구동력 | 없음 |
| 4 | Wang, Xia, Ji, Liu, Zhang, He, Zhang, Wan, Wang, "Lithium Anode Interlayer Design for All-Solid-State Lithium-Metal Batteries", *Nat. Energy* 9, 251–262 (2024) (ref 19) | 인터레이어 설계 원리 — 친Li · 소Li · 계면 에너지 · 젖음 | 카드 없음 (`kang2026_…` 가 인용만) |
| 5 | Doerrer, Metzler, Matthews, Bu, Spencer-Jolly, Bruce, Pasta, Grant, "Spraying Li₆PS₅Cl and Silver-Carbon Multilayers to Facilitate Large-scale Fabrication of All-Solid-State Batteries", *Device* 2, 100468 (2024) (ref 29) | 같은 랩 · Ag 위치를 층으로 나눈 '구조화' Ag/C · DEM 제조 축 | 없음 |
| 6 | Müller, Paravicini, Morzy, Krause, Casella, Osenciat, Futscher, Romanyuk, "Influence of Au, Pt, and C Seed Layers on Lithium Nucleation Dynamics for Anode-Free Solid-State Batteries", *ACS Appl. Mater. Interfaces* 16, 695–703 (2024) (ref 48 — 이 논문은 연도를 2007 로 오기) | 금속 · 탄소 씨앗층별 핵생성 과전압 — 핵생성 축 · 탄소 대 금속 | 없음 |
| 7 | Fuchs, Ortmann, Becker, Haslam, Ziegler, Singh, Rohnke, Mogwitz, Peppler, Nazar, Sakamoto, Janek, "Imaging the microstructure of lithium and sodium metal in anode-free solid-state batteries using electron backscatter diffraction", *Nat. Mater.* 23, 1678–1685 (2024) (ref 61) | 집전체 위 석출 Li 의 결정 조직 (EBSD) — Li\|기판 계면 · Li 면 선택 | 없음 · 공저자 'Sakamoto, J.' (참고문헌 표기) |
| 8 | Haslam, Sakamoto, "Stable Lithium Plating in 'Lithium Metal-Free' Solid-State Batteries Enabled by Seeded Lithium Nucleation", *J. Electrochem. Soc.* 170, 040524 (2023) (ref 39) | 매끈 · 연속 vs 덩어리 Au 씨앗 — 이 논문의 '거친 Ag 가 낫다' 근거 · Li\|기판 핵생성 | 없음 · 공저자 'Sakamoto, J.' (참고문헌 표기) |

차순위 (8 편 밖): Kwon et al., *Adv. Funct. Mater.* 35, 2420474 (2025) (ref 43 · LPSCl 셀의 Cu 부식 — §10-⑥ 의 S 신호) · Futscher et al., *J. Mater. Chem. A* 10, 15535 (2022) (ref 59 · 비정질 탄소 층과 핵생성) · Sandoval et al., *Joule* 7, 2054 (2023) (ref 32 · 무음극 합금 층의 진화) · Kim J.-S. et al., *Nat. Commun.* 14, 782 (2023) (ref 35 · LLZTO 위 스퍼터 Ag + Ag/C).

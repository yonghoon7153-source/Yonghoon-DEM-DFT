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

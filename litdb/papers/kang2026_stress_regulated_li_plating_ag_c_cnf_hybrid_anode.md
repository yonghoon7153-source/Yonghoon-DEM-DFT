<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 편에서 꼭 뽑으라고 한 항목 (후보 표 밖 · 1저자 11-16 직접 요청 · 정독 NN 125 · 1저자 말 없음 → 메인 세션 추정 의도 여섯 = §0-1).
     본 = jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표 꼴).
     원문 = 출판본 (Adv. Energy Mater. 2026, 0:e71816 · 18 쪽 · Research Article · CC BY-NC) + Supporting Information (42 쪽 PDF · Word 문서를 PDF 로 바꾼 판 · 쪽마다 머리 로고).
     쪽 표기 = 본문 "p.n" = 인쇄 "n of 18" = PDF 쪽 n · SI "SI p.n" = SI PDF 쪽 n (SI 인쇄 쪽 번호 = PDF 쪽 · SI p.1 = 표지).  크롭 파일 이름의 pN 과 figures.json 의 page 는 PDF 쪽이다.
     값 표지: [인쇄] = 본문 · SI · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 55 행 — 축 눈금 위치 · 표지 / 막대 윗변 · 색 판별, 방법은 note 열) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본의 다른 카드에 적힌 값 (그 카드 slug 병기) ·
     [우리] = 우리 쪽 값 (CLAUDE.md 출처) · [미확인] = 본문 18 쪽 + SI 42 쪽 전수에 없음.
     원문 60 쪽은 글자 층 추출 (본문 · SI 전부) + 그림 쪽 렌더로 읽었다 (본문 식 (1)–(21) · SI 식 (S1)–(S10) 은 크롭으로 눈 대조).  DEM · 입자 계산은 없다 — 실험 (operando 하중 셀 압력 · SEM · XRD · ToF-SIMS · 전기화학) + 2D 선형 탄성 FE + 2D phase-field (Li = 점성 유체). -->
# Ag–C 층 + 다공 탄소나노섬유 (CNF) 층 2 층 음극 — operando 하중 셀 ΔP 가 양극 면적 용량에 비례 (2.3 / 3.5 / 4.9 mAh cm⁻² → 1.1 / 1.8 / 2.4 MPa · 몰드 스택 20 MPa) · CNF 20 µm 로 2.3 → 1.6 MPa · 2D 선형 탄성 FE (경계 변위 β·h_Li·f(x)) · 2D phase-field (Stokes + 대류 Cahn–Hilliard + Coble 크리프 점도) · 파우치 1 · 2 MPa — Kang · Lee · Park · Shin · Kim · Lee · Jung · Choi · Lee (Adv. Energy Mater. 2026) — [우리 그룹]

> slug `kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode` · DOI `10.1002/aenm.71816` · type `experiment + 2D FEM (선형 탄성 · 평면 변형 · 경계 변위 처방) + 2D phase-field (비압축 Stokes 2 상 흐름 + 대류 Cahn–Hilliard · Coble 크리프 점도) — DEM · 입자 계산 없음` · PDF `0a342b1c-Stress-Regulated_Li_Plating_in_Hybrid_Ag_CarbonCarbon_Nanofiber_Anodes_for_Durable_All-Solid-State_Batteries.pdf` · SI `1dbda7de-Sup_Stress-Regulated_Li_Plating_in_Hybrid_Ag_CarbonCarbon_Nanofiber_Anodes_for_Durable_All-Solid-State_Batteries.pdf` · digested `2026-11-16` · status ✅
>
> **저자**: **Junhee Kang** ¹ · **Tae Young Lee** ¹ (공동 1 저자 — *"Junhee Kang and Tae Young Lee contributed equally to this work"*) · Jeongvin Park ¹ · Hong Rim Shin ¹ · Dong Seok Kim ¹ · Jieun Lee ¹ · **Hun-Gi Jung\*** ²·³·⁴ · **Jeong-Hee Choi\*** ⁵·⁶·⁷ · **Jong-Won Lee\*** ¹·⁸ — ¹ Division of Materials Science and Engineering, Hanyang University · ² Energy Storage Research Center, KIST · ³ Division of Energy & Environment Technology, KIST School, UST · ⁴ Department of Energy Science and KIST-SKKU Carbon-Neutral Research Center, Sungkyunkwan University · ⁵ Battery Research Division, KERI · ⁶ Department of Electro-Functionality Materials Engineering, UST · ⁷ Glocal University Project Group, Changwon National University · ⁸ Department of Battery Engineering, Hanyang University — \* 교신 3 인 · *Adv. Energy Mater.* **2026**, **0**:**e71816** (권 · 쪽이 아직 0 = [미확인 — 조판 전] · 18 쪽 · Research Article) · 받음 2026-07-29 · 고침 2026-10-25 · 승인 2026-10-31 · **CC BY-NC** · 키워드 *Ag–C interlayer · all-solid-state battery · high energy density · hybrid anode · Li metal* · 연구비 NRF RS-2025-25441254 · RS-2025-25418010 · 자료 = 교신 저자에게 요청.
> **[우리 그룹]** = 한양대 Jong-Won Lee 연구실 (교신 3 인 중 1).  우리 계산 담당은 저자가 **아니다** — 선례 `kang2026_site_specific_customized_se_dendrite_tolerant_li_metal` · `kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review` 와 같은 표지.
> **이웃 카드 (링크만)**: [`kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review`](kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review.md) (같은 1 저자 · 같은 해 · 이 논문 ref [9]) · [`ahn2026_cej_agno3_pvp_li3n_anodefree`](ahn2026_cej_agno3_pvp_li3n_anodefree.md) (같은 랩 · **같은 장치 · 같은 조건** — §0-1 ⑥) · [`liao2025_interfacial_adhesion_li_plating_carbon_interlayer`](liao2025_interfacial_adhesion_li_plating_carbon_interlayer.md) (탄소 인터레이어 접착 ↔ Li 석출 위치) · [`spencerjolly2023_ag_graphite_interlayer_operando_xrd`](spencerjolly2023_ag_graphite_interlayer_operando_xrd.md) (Ag–C 의 Li–Ag 상) · [`lawrence2008_single_vgcnf_elastic_modulus_morphology`](lawrence2008_single_vgcnf_elastic_modulus_morphology.md) (같은 Pyrograf III 계열 단섬유 탄성률).
> **판독 원자료**: `litdb/figures/kang2026_stress_regulated_li_plating_ag_c_cnf_hybrid_anode/digitized.csv` (55 행 — SI 그림 S3 · S16 막대 · S6 표지 (β 5 × 용량 3) · S12 표지 · 그림 4e 막대 · 그림 7e 표지 · S26 고원 · 그림 8c 표지 · S8 눈금 막대) · 그림 크롭 **150 장** (도구 44 = 본문 그림 8 · SI 그림 32 · SI 표 4 — 그중 **SI 그림 32 · 표 4 다시 자름** + 손 크롭 106 = 본문 패널 42 · SI 패널 12 · 식 32 · 근거 문단 20 · 손 크롭 1 장 다시 자름) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: NCM811 ‖ LPSCl ‖ Li 반쪽 셀 (Ø 13 mm PEEK 몰드 · **스택 20 MPa** · 45 °C · 0.2C) 에서 양극 면적 용량을 2.3 → 3.5 → 4.9 mAh cm⁻² 로 올리면 하중 셀로 잰 **압력 요동 ΔP 가 1.1 → 1.8 → 2.4 MPa** 로 거의 비례해 커지고 (p.2), 4.9 셀만 **128–129 번째 사이클에 단락**한다 (p.3 · 그림 1c · 1e) — 저자들은 이것을 "Li 석출 · 탈리의 부피 변화가 쌓는 기계 부담" 으로 읽고, 반대쪽 판 (Ag–C 층 위에 18.5 µm · 기공 71 % 의 CNF 층) 을 두어 ΔP 를 **2.3 → 1.6 MPa** 로 줄이고 (p.6) 몰드 셀 **250 사이클** (Ag–C 만 = 213 번째 단락, p.10) · 파우치 (3 × 3 cm² · **2 MPa**) **92.0 % vs 80.8 %** (250 사이클, 그림 8b) 를 보인다.  역학 계산은 둘이다: **① 2D 평면 변형 선형 탄성 FE** — LPSCl 한 상 (E 22.1 GPa · ν 0.33) 의 Li 쪽 경계에 **u_y = β · h_Li(Q) · f(x)** (β = 0.003 · f = 영평균 가우스 셋) 를 처방하고 위 경계에 **−20 MPa** 를 건다 → 첨두 σ_yy 4.6 / 43.3 / 110.8 MPa (p.4 · 식 (1)–(10)) · **② 2D phase-field** — Li 를 **Coble 크리프에서 유도한 점도의 뉴턴 유체**로 두고 비압축 Stokes + 대류 Cahn–Hilliard 로 곧은 기공 (인터레이어 50 nm · 호스트 200 nm) 을 채운다 → SOC 14 % 에 인터레이어 포화 · 58 % 에 호스트 포화 · 계면 압력 33.2 MPa (식 (11)–(21) · 표 S3 · 그림 6 · S24).  **두 모델 모두 실측 ΔP 와 숫자로 맞춰 보지 않았다.**

| 우리 질문 (추정 의도) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 실측 압력 (장치 · 처음 압력 · 면적 용량별 ΔP · 시간 · 충방전) | 장치 = 하중 셀 (Bongshin · **분해능 0.01 MPa**) 을 몰드와 직렬로 묶은 볼트 틀 (SI 그림 S2) · 셀 = **Ø 13 mm** PEEK 몰드 · SUS 막대 · 운전 스택 **20 MPa** (모든 몰드 셀) · 45 °C · 2.5–4.25 V · 0.1C CC–CV 한 번 뒤 0.2C · ΔP (상대) **1.1 / 1.8 / 2.4 MPa** (2.3 / 3.5 / 4.9 mAh cm⁻²) — 충전 때 오르고 방전 때 내린다 (그림 1a · 0–40 h · 한 사이클 ≈8 h [판독 — 꼭대기 5 개 ≈4.5 · 13 · 21 · 29 · 37 h]) · 최대 dP/dt **0.27 / 0.43 / 0.72 MPa h⁻¹** [판독 SI 그림 S3] · CNF 0 / 10 / 20 µm: ΔP **2.3 / 2.0 / 1.6 MPa** · 최대 dP/dt **0.88 / 0.61 / 0.46** [판독 S16] · CNF 만: **2.3 MPa** (S20) · **절대 압력 곡선 · 파우치 operando 압력 없음** | [인쇄] p.2 · p.6 · p.7 · p.14 · [판독] |
| ② ★ "mechanical modeling" 의 정체 | **2D 평면 변형 선형 탄성 FE · 자체 구현 여부 · 도구 [미확인]** · LPSCl 한 상 (E 22.1 GPa · ν 0.33 · Ref. S1) · 120 × 100 µm · 81 × 51 절점 · 80 × 50 Q4 · 경계 = 아래 u_y = β h_Li f(x) · 위 σ_yy = −20 MPa · 옆면 [미확인] · Li · Ag · Ag–Li · 탄소 · CNF · 집전체 물성 **없음** (Li 는 고체로 계산하지 않는다) · 결과 = 첨두 σ_yy **4.6 / 43.3 / 110.8 MPa** · 95 백분위 von Mises **22.8 / 35.4 / 65.7 MPa** · β 민감도 (S6) · f(x) 밀도 (S7) · 실측 ΔP 와 대조 **없음** | [인쇄] p.4 · p.14–15 · SI p.7–9 |
| ③ ★ phase-field 모델 | 식 (11)–(21) + SI 식 (S1)–(S10) · 표 S3 (매개변수 16) · 2D 곧은 기공 기하 (S21: 인터레이어 8 µm · 50 nm · 기공률 0.4 / 호스트 20 µm · 200 nm · 0.7 · 옆 2 µm) · 경계 = 위 기공 입구 같은 적분 유입 · 아래 0 Pa · 고체 벽 젖음 + Navier 미끄럼 200 nm · 접촉각 75° (가정) · 계면 두께 20 nm · 이동도 2 × 10⁻⁸ · **도구 · 격자 · 초기 조건 [미확인]** · 맞춘 값 없음 (SOC 10 / 50 / 75 % 단면과 정성 대조) | [인쇄] p.8–10 · p.15–16 · SI p.24–33 |
| ④ ★ CNF 망 · Ag–C 층 숫자 | CNF = **Pyrograf-III 기상성장 CNF** (Sigma 719811 PR-25-XT-PS = LC · 719803 PR-25-XT-LHT = HC · 1500 °C 열처리) · 층 두께 **19.6 / 18.5 µm** · 기공률 **70.1 / 71.0 %** · 면 질량 **0.76 / 0.70 mg cm⁻²** · CNF : SBR = **2 : 1** · 비표면적 54 / 39 m² g⁻¹ · 세공 부피 0.12 cm³ g⁻¹ · 밀도 1.8 / 1.9 g cm⁻³ (공급사) · I_D/I_G **0.99 / 0.19** · **섬유 지름 · 길이 [미확인]** ([판독 거칢] SEM ≈0.2–0.5 µm) · 전자 전도 = 모델 입력 κ_e **1000 S m⁻¹** (실측 없음) · 압축: ≈35 µm 층 **5 MPa 4 h** P_avg 4.75 → 4.72 MPa · 5 회 누름 두께 ≈35.1 → 33.2 µm (≈5.6 %) · 회복 ≈34.7–35.0 µm [판독 S12] / Ag–C: Ag (D50 60 nm) : 카본블랙 (D50 35 nm) = 1 : 3 · PVDF 8 wt% · 7.7–7.9 µm · 겉보기 밀도 1.25 g cm⁻³ · **≈450 MPa** 치밀화 | [인쇄] p.6 · p.13 · SI p.18 · p.40–41 · [판독] |
| ⑤ ★ SE · 셀 조건 | SE = Li₆PS₅Cl (공급처 · 입경 [미확인]) · 분리막 0.15 g · 양극 NCM : LPSCl : Super P = **72 : 27 : 1** (볼밀) · 양극 + Ag–C **450 MPa** 공압착 · CNF 넣고 **150 MPa** · 스택 **20 MPa** · 파우치 = 건식 양극 NCM811 77 / LPSCl 19.5 / CNF 3 / PTFE 0.5 wt% · LPSCl 막 (NBR 2 wt%) · **WIP 30 → 500 MPa** · 3 × 3 cm² · 조임 토크 틀 · **1 · 2 MPa** · 45 °C · 0.2C = 0.46 / 0.70 / 0.98 mA cm⁻² [카드 산술] · 같은 전류 대조 **0.98 mA cm⁻²** · 파우치 0.3C ≈1.3 mA cm⁻² [판독 그림 8c · 카드 산술] | [인쇄] p.3 · p.13–14 · [판독] |
| ⑥ 같은 랩 다른 카드 | `ahn2026_cej_agno3_pvp_li3n_anodefree` = **같은 몰드 (Ø 13 mm PEEK) · 같은 0.15 g LPSCl · 같은 하중 셀 분해능 0.01 MPa · 같은 20 MPa · 45 °C · 2.5–4.25 V · 0.1C CC–CV (차단 = CC 전류의 절반)** [다른 카드 L114–L127] — 다른 점: 그 논문은 SE 층 50 MPa 선성형 · 전체 400 MPa (이 논문 450 MPa · 분리막 성형압 [미확인]) · NCA 건식 필름 양극 · `kang2026_site_specific_…` (같은 1 저자 Junhee Kang · Tae Young Lee 공저) = Ø 10 mm 몰드 · 스택 20 MPa [다른 카드 L12 · L45] · `kang2026_intertwined_…` = Li–In 셀 압력 요동 ≈3.8 MPa vs LTO ≈0.2 MPa (리뷰 ref 120 = 같은 랩) [다른 카드 L172 · L263] | [다른 카드] |

⛔ **한정어 (떼지 말 것)**: ① ΔP 는 **상대값** (각 그림의 0 기준) 이고 그 셀의 스택 (20 MPa) 위에 얹힌 요동이다 — 절대 압력 곡선 · 하중 셀 온도 보정 · 틀 강성은 원문에 없다 ② ΔP 크기는 **셀 + 틀의 순응**이 정한다 — 재료 강성으로 읽지 않는다 (ΔP ÷ 치밀 Li 두께 ≈0.1 MPa µm⁻¹ 는 이 틀 한정 [카드 산술 · §3-2]) ③ FE 는 **한 상 선형 탄성 · 효과 매개변수 β (측정 아님)** — 응력 크기는 β 에 비례해 움직이고 (S6), 저자 스스로 "비교 틀" 이라 부른다 ④ phase-field 는 **곧은 기공 2D · Li = 점성 유체 (탄성 · 항복 없음)** · 기공 크기 · 접촉각 · 간극은 가정 ⑤ 재료: 음극 쪽 계 (Li · Ag–C · CNF) 가 주인공이고 SE 는 쓰기만 했다 — 우리 양극 압밀 계와 **축이 다르다**.
⇒ **절대값 전이: 0 건** (우리 양극 DEM · MPM 으로).  전이되는 것은 **측정 · 보고 꼴** (스택 위 상대 ΔP · dP/dt · 같은 전류 대조 · 효과 매개변수의 민감도 보고) 과 **반대쪽 판의 부피 변화가 스택 압력을 흔든다는 크기 감각** 이다.

---

## 0-1. ★ 고른 의도 대조 (추정 의도 — 1저자 말 아님 · 메인 세션 지시서의 여섯 항목)

후보 표 행 · 가리킨 카드 없음 (1저자가 PDF 둘을 직접 줌 · *"논문 에이전트 부탁해용"* · *"litdb로 잘 크롭핑해서 보내줘"*).  아래 의도 문장은 메인 세션이 적은 **추정 의도**다.

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| ① "실측 (operando) 압력 — 측정 장치 · 셀 꼴" | **채움** | SI 그림 S2: 볼트 4 개로 죄는 두 판 사이에 셀 스택 + 하중 셀 · 표시기 kgf (그림 글자 "100.0 kgf" · "000.0–999.9") · p.14 *"pressure sensors with a resolution of 0.01 MPa (load cell, Bongshin) were assembled with the cells"* · 몰드 = PEEK · SUS 막대 **Ø 13 mm** (p.13–14) · 0.1 kgf 표시 = Ø 13 mm 에서 0.0074 MPa [카드 산술] → 분해능 0.01 MPa 와 같은 자릿수 |
| ① "처음 스택 압력" | **채움 (그림 밖)** | p.14 *"Electrochemical tests were conducted under a stack pressure of 20 MPa for all cell configurations"* — ΔP 그림 축은 상대값 (0 에서 시작) · 시작 때 실측 절대 압력 · 휴지 이완 곡선 [미확인] |
| ① "면적 용량 (mAh cm⁻²) 별 압력 요동 크기" | **채움** | p.2 · 그림 1a: **1.1 · 1.8 · 2.4 MPa** (2.3 · 3.5 · 4.9) — 저자 *"increases nearly proportionally"* · ΔP ÷ Q = 0.48 / 0.51 / 0.49 MPa per mAh cm⁻² [카드 산술] · 최대 dP/dt 0.27 / 0.43 / 0.72 MPa h⁻¹ [판독 S3] · CNF: 2.3 / 2.0 / 1.6 MPa (p.6 · 그림 4c) · CNF 만 2.3 MPa (p.7 · S20) |
| ① "시간 축 · 충전 / 방전 어디서 오르내리나" | **채움** | 그림 1a: 0–40 h · ≈5 사이클 [판독] · ΔP 는 충전 (Li 석출 · 전압 4.25 V 까지) 동안 오르고 방전 동안 내린다 · dP/dt (그림 1b): 충전 ≈+0.25 (2.3)…+0.75 (4.9) · 방전 ≈−0.3 (2.3)…−0.75 (4.9) MPa h⁻¹ [판독] · 단락 셀 = 128 번째부터 불규칙 → dP/dt ≈0 구간 (p.3 · 그림 1e) · Ag–C 만 셀 213–214 번째도 같은 꼴 (S30) · ⚠ 바닥 · 꼭대기가 사이클마다 조금 내려가는 표류가 보이나 원문 언급 없음 [판독 거칢] |
| ① "우리 DEM 압축 · 탈압 · 스택 압력과 견줄 숫자" | **일부** | 제조압 450 (양극 + Ag–C) · 150 (CNF) MPa · 파우치 WIP 30 → 500 MPa · 운전 20 MPa (몰드) · 1 · 2 MPa (파우치) [인쇄] · ΔP / 스택 = 5.5 / 9 / 12 % [카드 산술] — **누른 채 기공 · 탈압 곡선 · SE 의 회복량은 없다** (탈압 쪽 실측은 CNF 층 5 MPa 누름–회복뿐 · §3-5) |
| ② "mechanical modeling 이 무엇인가 (해석식 / FEM · 도구)" | **채움 (도구만 [미확인])** | p.4 · p.14–15: **2D FE · 평면 변형 · 선형 탄성** · Gauss 점 4 개 평균 · 도구 이름 없음 |
| ② "지배식" | **채움** | 식 (1) h_Li = 3.6 Q M_Li / (F ρ_Li) · (2) u_y = β h_Li f(x) · (3) ∇·σ = 0 · (4) 작은 변형률 · (5) σ = Cε · (6)–(8) 평면 변형 성분 · (9) σ_zz = ν(σ_xx + σ_yy) · (10) 3D von Mises — 식 크롭 10 장 |
| ② "입력 물성 (Li · Ag · Ag–Li · 탄소 · CNF · SE · 집전체의 E · ν · 항복과 출처)" | **일부 — SE 둘뿐** | 표 S1: LPSCl **E 22.1 GPa · ν 0.33 (Ref. S1 = Pustorino 2025 *Chem. Mater.* 37, 313)** — Li · Ag · Ag–Li · 탄소 · CNF · 집전체 물성 **없음** (Li 는 계산 영역 밖 · 그 효과는 β 로 대체).  ⚠ 정본 `pustorino2025_…` 카드 표 3 에 **22.1 GPa 가 없다** (48H 29.0 GPa · ν 0.33 · 전체 범위 21.7–37.9) [다른 카드 L72–L80] — §3-7 ⑧ |
| ② "경계 조건" | **일부** | 아래 (Li 쪽) = 영평균 법선 변위 처방 · 위 = 고른 압축 견인 −20 MPa (= 몰드 스택) · **옆면 · 아래 접선 경계 · f(x) 의 가우스 폭 · 위치 [미확인]** (그림 2a: 아래 경계에 압축 띠 3 개 (x ≈30 · 62 · 95 µm) + 그 사이 · 바깥 인장 띠 4 개 [판독] = "three principal Gaussian features" + 영평균 보상으로 읽힘 [카드 해석]) |
| ② "결과 (응력 · 압력 · 변형) 와 실측의 대조" | **일부** | 결과 = σ_yy · von Mises (그림 2 · S6 · S7) · 실측과의 대조 = 4.9 셀의 단락 · SEM 박리와 **정성 일치**만 — 실측 ΔP · 응력 · 변형과 수치 대조 **없음** |
| ③ "phase-field — 지배식 (식 번호마다 식 크롭)" | **채움** | 본문 식 (11)–(21) + SI Note 1 식 (S1)–(S10) · 크롭 21 장 (eq_11–eq_21 · eq_S01–eq_S10) |
| ③ "매개변수 표" | **채움** | 표 S3 (16 행 · 출처 칸 — 실험 2 · 문헌 6 · 가정 4 · 계산 1 · 출처 칸 "-" 3 (R · M_Li · ρ_Li)) · SI Note 1 의 덧붙임 (α_a 0.5 · κ_ion · κ_e · b_nuc 0.30 · i0,grow 1.0 × 10⁻³ A m⁻² · τ_creep,host 1.84) |
| ③ "경계 · 초기 조건 · 격자 · 차원 · 도구" | **일부** | 경계 = 채움 (p.15–16) · 차원 = 2D · 시간 영역 · **초기 조건 (SOC 0 % = 빈 기공으로 읽힘 [카드 해석]) · 격자 · 풀이기 · 도구 [미확인]** (용어 "Fluid 2" · "wetted wall" · "Navier slip" 은 상용 2 상 흐름 phase-field 인터페이스 용어와 같다 [카드 해석 — 원문에 도구 이름 없음]) |
| ③ "무엇을 실측과 맞췄고 무엇은 가정인지" | **채움 (맞춘 것 없음)** | 맞춘 값 **0** · 실험 값 2 (T 318.15 K · j 0.49 mA cm⁻²) · 가정 4 (인터레이어 기공 50 nm · 호스트 기공 200 nm · 접촉각 75° · 간극 80 nm) · 계산 1 (호스트 기공률 0.7) · 문헌 (D · δ · ε_interlayer · ρ_dep · γ_s) · 예측 순서 (SOC 14 % → 58 %) 를 SOC 10 / 50 / 75 % 단면과 **정성 대조** (p.9 · S22) |
| ④ "다공 CNF 망 · Ag–C 층 — 섬유 지름 · 길이 · 기공률 · 두께 · 면 질량 · 전도도 · 압축" | **일부** | 기공률 · 두께 · 면 질량 · 비표면적 · 밀도 · 열처리 = **채움** (표 S2 · Note S2) · **지름 · 길이 = 없음** ([판독 거칢] S8 ≈0.2–0.5 µm · 길이는 시야 5 µm 넘음) · **전도도 실측 없음** (모델 κ_e 1000 S m⁻¹ · Ref. S3) · 압축 = **채움** (S10–S13: 5 MPa · 4 h · 5 회) |
| ⑤ "SE 종류 · 펠릿 두께 · 성형 압력 · 양극 조성 · 면적 용량 · 파우치 스택 (1 · 2 MPa) · 온도 · 전류 밀도" | **일부** | SE = Li₆PS₅Cl (XRD S1) · 펠릿 = 0.15 g (두께 [미확인] — 진밀도 1.64 g cm⁻³ · 기공 0 이면 0.69 mm [카드 산술 · 랩 표준 값 대입]) · 분리막 성형압 [미확인] · 양극 450 MPa · 72 : 27 : 1 · 2.3 / 3.5 / 4.9 mAh cm⁻² (NCM mg cm⁻² [미확인]) · 파우치 1 · 2 MPa · 45 °C · 0.2C · 0.98 mA cm⁻² — 채움 |
| ⑥ "같은 랩 다른 카드와의 관계 — 같은 장치 · 같은 조건이면 그 사실만" | **채움** | 위 표 ⑥ 행 그대로 — ahn2026 = 같은 장치 · 같은 조건 (그 카드의 ΔP = 3.0 / 2.8 / 2.5 MPa 는 **NCA 양극 · 다른 인터레이어** — 이 논문 값과 같은 표에 넣지 않는다) |

**2 차 인용 대조**: 정본 카드 가운데 이 논문 (DOI `aenm.71816` · 제목 낱말) 을 인용한 카드 **0 건** (2026-11-16 `git grep`).  거꾸로 이 논문이 정본 카드의 원문을 인용한 자리 하나가 맞지 않는다 — 표 S1 *"Young's modulus 22.1 GPa · Ref. S1"* ↔ `pustorino2025_lpscl_bulk_surface_mechanical_electronic_li_filament` 표 3 (E 27.8 · 29.0 · 21.7 · 29.9 · 37.9 GPa · 22.1 없음) [다른 카드 · Pustorino 원문 PDF 는 이 작업에서 열지 않았다 → 최종 판정은 원문 대조 뒤].  22.1 GPa 는 정본 비교 문서 `litdb/comparison_vs_ours.md` 의 `[Deng16]` 행 (L115 · Deng 2016 JES PBEsol DFT · Li₆PS₅Cl **E 22.1 · ν 0.37**) 과 같은 숫자이고, ν 0.33 은 Pustorino 48H 와 같다 — 두 출처가 섞였을 가능성 [카드 해석].

⇒ **의도 대조 결과: 일부** — 실측 압력 (장치 · 20 MPa · ΔP 1.1 / 1.8 / 2.4 · 충전 상승 / 방전 하강) · phase-field 지배식 · 매개변수 · CNF 기공률 · 두께 · 면 질량 · 압축 · 셀 조건은 **채움**; FE 는 **SE 한 상 선형 탄성** (Li · Ag · CNF 물성 없음 · 도구 · 옆면 경계 미기재 · 실측 대조 없음) 이라 **일부**; phase-field 의 도구 · 격자 · 초기 조건, CNF 섬유 지름 · 길이 · 전도도 실측은 **없음**.

---

## 1. 한 줄 요약
고적재 (≈5 mAh cm⁻²) 황화물 전고체 전지의 Li 음극 쪽에서 **석출 · 탈리 부피 변화가 스택 압력을 흔들고** (하중 셀 실측 ΔP ∝ 면적 용량), 그 요동이 계면 박리 · 단락으로 이어진다고 보고, **치밀 Ag–C 층 (핵생성 · 전기화학 조절) + 다공 CNF 층 (부피 흡수 · 기계 완충)** 을 따로 만들어 붙인 2 층 음극으로 ΔP 를 30 % 줄이고 수명을 늘린다; 2D 선형 탄성 FE 는 "용량이 크면 SE 경계 응력이 커진다" 를, 2D phase-field 는 "Ag–C 합금화 → CNF 기공 채움 (SOC ≈58 % 에서 끝) → 계면 Li 층" 순서를 보인다.
저자의 결론: *"the results establish partial Li accommodation as a more practical strategy than complete zero-strain hosting"* (p.13) — Li 전부를 담으려면 CNF 가 ≈35.4 µm 필요하고 비활성 부피가 9.5 → 13.9 mm³ 로 는다 (p.13 · 그림 8d · 8e).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM · 음극) | 연구유형 |
|---|---|---|---|---|
| J. Kang · T. Y. Lee (공동 1 저자) · J. Park · H. R. Shin · D. S. Kim · J. Lee · **H.-G. Jung\*** · **J.-H. Choi\*** · **J.-W. Lee\*** (한양대 · KIST · KERI · UST · 성균관대 · 창원대) | Adv. Energy Mater. 2026, 0:e71816 · CC BY-NC | 10.1002/aenm.71816 | **Li₆PS₅Cl** (공급처 · 입경 미기재) + **NCM811** (공급처 미기재) · 음극 = Li 포일 (200 µm) / **Ag–C** (Ag 60 nm : 카본블랙 35 nm = 1 : 3 · PVDF 8 wt%) / **Ag–C + CNF** (Pyrograf-III PR-25 · SBR 1/3) | 실험 (operando 하중 셀 압력 · 압력 지도 · SEM · EDS · FIB · XRD · ToF-SIMS · Raman · EIS-DRT · 전기화학) + 2D 선형 탄성 FE + 2D phase-field |

- **1저자 메모와의 대조**: 제목 · 학술지 · 권 0 / e71816 · DOI · 저자 첫 줄 · 교신 셋 · 소속 · 받음 · 고침 · 승인 날짜 · 쪽 수 (18 · 42) · CC BY-NC — **같다**.  덧붙임: ① SI 제목은 문장체 (*"Stress-regulated Li plating in hybrid Ag–carbon/carbon nanofiber anodes for durable all-solid-state batteries"*) ② 본문 끝 *"Supporting File: aenm71816-sup-0001-SuppMat.docx"* — 받은 SI PDF 는 그 Word 문서를 PDF 로 바꾼 판 (쪽마다 출판사 머리 로고).
- **글의 꼴**: 서론 → 결과 (그림 1 압력 · 수명 / 그림 2 FE / 그림 3 제작 / 그림 4 CNF 결정성 · 두께 / 그림 5 단면 · XRD · ToF-SIMS / 그림 6 phase-field / 그림 7 반쪽 · 풀 셀 / 그림 8 파우치 · 저장량 추정 · 기전) → 결론 → 실험 (4.1 CNF · Ag–C · 4.2 몰드 셀 · 4.3 파우치 · 4.4 전기화학 · 4.5 분석 · 4.6 FE · 4.7 phase-field) → 참고문헌 61.  그림 8 · 표 0 · 번호 식 21 (본문) / SI: 그림 S1–S32 · 표 S1–S4 · 식 (S1)–(S10) + 표 S2 아래 번호 없는 기공률 식 · Note S1 (수송 경로 분해) · Note S2 (CNF 출처 · 결정성) · 참고문헌 S1–S10.
- 그룹 맥락: 같은 랩의 고변형 음극 → 양극 열화 (ref [5] = 정본 `kim2023_chemomech_failure_highstrain_anode`, 그 카드 H1 은 Kang & Shin) · 무음극 달력 노화 (ref [8]) · 리뷰 (ref [9] = `kang2026_intertwined_…`) · 무음극 전구체 (같은 랩 `ahn2026_…` — 이 논문은 인용하지 않음).

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 재료 · 셀 · 조건 (p.13–14 · SI p.18 · p.40–41 · `txt_p13_experimental_fab.png` · `txt_p14_pellet_pouch_fab.png` · `txt_p14_electrochem_load_cell.png`)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| CNF | LC = Sigma-Aldrich PR-25-XT-PS (719811 · 열분해 세척 · ≈700 °C 후처리) · HC = PR-25-XT-LHT (719803 · **1500 °C** 열처리 · 흑연화) — 둘 다 Pyrograf Products 의 **floating-catalyst 기상성장 CNF** (CVD ≈1100 °C) · 속 빈 stacked-cup / herringbone (섬유 축에 기운 흑연 면 · 가장자리 면 노출) | [인쇄] p.13 · SI p.41 (Note S2) |
| CNF 층 (EPD) | CNF 10 mg / 아세톤 20 mL · 초음파 10 min · SBR (10 wt% 용액) 50 µL → *"binder content of 33 wt.% with respect to the CNF mass"* · 초음파 40 s 더 · 30 V **3 min 30 s** + 초음파 10 s + 30 s 더 · SUS 기판 · 그림 3a 모식 = *"Acid-treated CNF"* (산 처리는 실험 절에 없음) | [인쇄] p.13 · 그림 3a |
| Ag–C 층 | Ag (D50 **60 nm**) : 카본블랙 (D50 **35 nm**) = **1 : 3** (질량) · NMP + PVDF 8 wt% · 10 µm SUS 박 위 주조 · 80 °C 20 min → 100 °C 진공 12 h · 표 S4: C 0.69 · Ag 0.23 · 결합제 0.08 · 두께 7.8 µm · 겉보기 밀도 1.25 g cm⁻³ | [인쇄] p.13 · SI p.40 |
| 몰드 셀 | PEEK 몰드 · SUS 막대 **Ø 13 mm** (면적 1.327 cm² [카드 산술] · 표 S2 "Electrode area 1.33") · LPSCl **0.15 g** 펠릿 (분리막 · 성형압 [미확인]) · 양극 NCM : LPSCl : Super P = **72 : 27 : 1** (볼밀) · Ag–C 셀 = 양극과 Ag–C 를 차례로 넣고 **450 MPa** 공압착 · 반쪽 셀 = 양극 450 MPa + Li 포일 200 µm · CNF = 넣은 뒤 **150 MPa** · 운전 **20 MPa** (모든 몰드 셀) | [인쇄] p.13–14 |
| 파우치 | 건식 양극 NCM811 **77** / LPSCl **19.5** / CNF **3** / PTFE **0.5** wt% (막자 · 반복 캘린더 · 자립막) · SE 막 = LPSCl 98 wt% + NBR 2 wt% (벤질 아세테이트 · PE 필름 위 주조) · **WIP 30 MPa** (양극 + SE 막) → Ag–C 얹고 **WIP 500 MPa** → CNF 음극 얹고 재봉합 · **3 × 3 cm²** · 조임 토크 틀 · 스택 **1 · 2 MPa** (S31) | [인쇄] p.10 · p.14 |
| 전기화학 | **2.5–4.25 V vs Li/Li⁺ · 45 °C** · 첫 사이클 0.1C CC–CV (CV 차단 = CC 전류의 절반) → 0.2C (몰드) · 0.3C (파우치) · 1C = 면적 용량 (4.9 셀 0.2C = 0.98 mA cm⁻², p.3) · EIS Biologic SP-300 7 MHz–10 mHz · 5 mV | [인쇄] p.3 · p.14 |
| 압력 측정 | operando = 하중 셀 (Bongshin) · **분해능 0.01 MPa** · 압력 지도 = KITRONYX Baikal II (MA2032) | [인쇄] p.14 |
| 분석 | SEM-EDS FEI Verios G4UC · FIB Helios · Raman DXR3xi · ToF-SIMS ION-TOF M6 · XRD Bruker D8 (Cu Kα 1.541 Å · 2° min⁻¹) | [인쇄] p.14 |
| ⚠ 서로 다른 셀 | **0.1C 첫 충전**의 FE · phase-field 기준 전류 0.49 mA cm⁻² (= 4.9 × 0.1) ↔ 그림 1 의 운전 0.2C (0.98) — 모델 조건과 그림 1 의 ΔP 사이클은 C-율이 다르다 | [인쇄] p.15 · SI p.25 |

### 3-2. ★ operando 압력 — ΔP · dP/dt (p.2–3 · p.6–7 · 그림 1 · 4c–d · S2–S5 · S16–S17 · S20 · S30 · `fig_1a.png` · `fig_1b.png` · `fig_1e.png` · `fig_4c.png` · `fig_4d.png` · `fig_S2.png` · `fig_S3.png` · `fig_S16.png` · `fig_S17.png` · `fig_S20.png` · `txt_p2_operando_pressure_dP.png` · `txt_p3_same_current_control.png` · `txt_p6_cnf_thickness_dP.png`)
- **장치** (SI 그림 S2 · p.14): 두 판을 볼트 4 개로 묶은 틀 안에 셀 스택과 하중 셀을 직렬로 · 표시기 kgf (그림 글자 "100.0 kgf" · 범위 "000.0–999.9") · 0.1 kgf ÷ 1.327 cm² = **0.0074 MPa** [카드 산술] ≈ 분해능 0.01 MPa · 999.9 kgf = 73.9 MPa (Ø 13 mm) [카드 산술].  틀 강성 · 온도 (45 °C) 보정 · 예압 절차 [미확인].
- **NCM ‖ Li 반쪽 셀, 0.2C, 20 MPa, 45 °C** (p.2 · 그림 1a):

| 면적 용량 (mAh cm⁻²) | 인가 전류 (그림 글자) | 전류 밀도 [카드 산술] | ΔP (인쇄) | ΔP ÷ Q [카드 산술] | 치밀 Li 두께 h_Li [카드 산술 · 식 (1)] | ΔP ÷ h_Li [카드 산술] | 최대 dP/dt [판독 S3] |
|---|---|---|---|---|---|---|---|
| 2.3 | 0.61 mA | 0.46 mA cm⁻² | **1.1 MPa** | 0.48 | 11.2 µm | 0.099 MPa µm⁻¹ | 0.27 MPa h⁻¹ |
| 3.5 | 0.93 mA | 0.70 | **1.8** | 0.51 | 17.0 | 0.106 | 0.43 |
| 4.9 | 1.30 mA | 0.98 | **2.4** | 0.49 | 23.8 | 0.101 | 0.72 |

  [카드 산술]: h_Li = 3.6 Q M_Li/(F ρ_Li) = **4.85 µm per mAh cm⁻²** (M 6.94 · ρ 0.534 g cm⁻³) · ΔP / 스택 = 5.5 / 9.0 / 12 % · ΔF (4.9) = 2.4 MPa × 1.327 cm² = 318 N.  ⇒ 이 틀 · 셀에서 **ΔP ≈ 0.1 MPa per µm 치밀 Li** — 셀 + 틀의 겉보기 순응이다 (양극 NCM 의 충전 수축이 반대 부호로 섞여 있고 원문은 둘을 가르지 않는다 [카드 해석]).
- **시간 축** (그림 1a · 1b): 0–40 h · ≈5 사이클 (한 사이클 ≈8 h [판독 — 꼭대기 5 개 ≈4.5 · 13 · 21 · 29 · 37 h]) · ΔP 는 충전 동안 0 → 꼭대기, 방전 동안 → 바닥 (음수) · dP/dt 충전 ≈+0.25 (2.3)…+0.75 (4.9) · 방전 ≈−0.3 (2.3)…−0.75 (4.9) MPa h⁻¹ [판독] · 바닥 · 꼭대기가 사이클마다 조금씩 내려간다 [판독 거칢 · 원문 언급 없음].
- **고장 신호** (p.3 · 그림 1c · 1e): 4.9 셀만 *"highly irregular and dynamic pressure fluctuations beginning from the 128th cycle"* → 단락 구간에서 dP/dt → 0 · 그림 1c 표지 **"129th"** · 2.3 · 3.5 셀은 200 사이클 안정 · 100 사이클 유지율 **76.8 / 73.5 / 68.3 %** · 첫 효율 **87.5 / 87.6 / 88.8 %** (그림 1d) · SEM (그림 1f): 4.9 셀 LPSCl/Li 계면에 빈틈 · 박리 (붉은 점선 타원).
- **같은 전류 대조** (p.3 · S5): *"the contributions from electrochemical polarization and mechanically driven degradation cannot be fully distinguished from these results alone"* → 2.3 · 3.5 셀도 **0.98 mA cm⁻²** (= 0.43C · 0.28C [카드 산술]) 로 → 80 사이클 유지율 **75.0 / 73.3 / 70.2 %** (2.3 / 3.5 / 4.9) — 저적재 셀이 더 높은 C-율에서도 더 안정.
- **CNF 효과** (p.6 · 그림 4c–d · S16–S17): Ag–C/CNF (CNF **0 / 10 / 20 µm**) ‖ NCM (≈4.9–5.2 mAh cm⁻² — 그림 4e [판독]): ΔP **2.3 / 2.0 / 1.6 MPa** (−13 · −30 % [카드 산술]) · 최대 dP/dt **0.88 / 0.61 / 0.46 MPa h⁻¹** [판독 S16] · 20 µm 셀의 1.6 MPa 은 3.5 mAh cm⁻² 반쪽 셀 (1.8) 보다 낮다 (p.6) · 충전 첫 ≈1 h 의 dP/dt 상승이 CNF 가 두꺼울수록 늦고 완만 (S17).
- **대조**: Ag–C 만 ΔP **2.3 MPa** = Li 금속 4.9 셀 2.4 와 거의 같다 → *"the Ag–C interlayer homogenizes Li deposition but does not sufficiently suppress mechanically driven degradation"* (p.5) · **CNF 만** (Ag–C 없음) **≈2.3 MPa** (p.7 · S20) — 이때 Li 는 SE/CNF 계면에 ≈26 µm 층으로 모인다 (S19 그림 글자).
- 하중 셀 ΔP ↔ 모델: FE · phase-field 어느 쪽도 이 ΔP 를 계산하지 않는다 (§4-2).

### 3-3. ★ 역학 모델 = 2D 선형 탄성 FE (p.4 · p.14–15 · 표 S1 · 그림 2 · S6 · S7 · `eq_01`–`eq_10` · `tab_S1.png` · `fig_2a.png` · `fig_2b.png` · `fig_S6.png` · `fig_S7.png` · `txt_p4_fe_model_beta.png` · `txt_p4_fe_results_limits.png` · `txt_p14_fe_methods.png` · `txt_p15_fe_bc_traction.png`)
- **목적** (p.4): *"The model was intentionally simplified to isolate the mechanical consequence of increasing interfacial deformation with plated Li capacity, rather than to reproduce the full electrochemo-mechanical evolution of the interface."*
- **지배식** (p.14–15 · 크롭 eq_01–eq_10):
  - (1) h_Li(Q) = 3.6 Q M_Li / (F ρ_Li) — 석출 면적 용량 → 치밀 Li 두께
  - (2) **u_y(x, Q) = β h_Li(Q) f(x)** — f = *"normalized zero-mean spatial profile"* · β = *"dimensionless effective transfer factor"* (*"the combined contribution of the relative heterogeneity of the deposited Li morphology and the fraction of this heterogeneous deformation mechanically transferred to the LPSCl interface"*)
  - (3) ∇·σ = 0 · (4) ε = ½(∇u + ∇uᵀ) · (5) σ = Cε (평면 변형) · (6) σ_xx · (7) σ_yy · (8) τ_xy (등방 Hooke 성분) · (9) σ_zz = ν(σ_xx + σ_yy) · (10) 3D von Mises
- **입력 · 이산화 · 경계** (표 S1 · p.14–15):

| 항목 | 값 | 출처 |
|---|---|---|
| 영역 | 폭 W **120 µm** (계면 따라) × 높이 H **100 µm** (LPSCl 만) | 표 S1 |
| 격자 | 81 × 51 = **4 131 절점** · 80 × 50 = **4 000 Q4** (쌍선형 4 절점) · 요소 넓이 3 µm² (= 1.5 × 2.0 µm [카드 산술]) · 요소마다 Gauss 점 4 개 응력 평균 | 표 S1 · p.14–15 |
| 물성 | LPSCl **E 22.1 GPa · ν 0.33** (등방 · 균질 · 선형 탄성) → K = 21.7 · G = 8.31 GPa [카드 산술] | Ref. S1 (⚠ §3-7 ⑧) |
| 아래 경계 (Li 쪽) | 식 (2) 의 법선 변위 · **β = 0.003** (세 용량 모두) · f = *"three principal Gaussian features"* (S7 에서 여섯으로) · 진폭 β h_Li = **33.5 / 50.9 / 71.3 nm** (2.3 / 3.5 / 4.9) [카드 산술] · 접선 경계 [미확인] | p.4 · p.14 |
| 위 경계 | 고른 압축 견인 **σ_yy = −20 MPa** (= 몰드 스택) | p.15 |
| 옆면 | [미확인] | — |
| 기타 | 45 °C · 0.1C (4.9 기준 0.49 mA cm⁻²) 를 적었지만 정적 선형 탄성이라 계산에 들어가지 않는다 [카드 해석] · 고른 Li 성장은 *"accommodated primarily by Li plastic flow, creep, and compliance of the cell stack and therefore was not imposed directly on the elastic LPSCl domain"* | p.15 |

- **결과** (p.4 · 그림 2): 첨두 σ_yy **4.6 / 43.3 / 110.8 MPa** · 95 백분위 σ_vM **22.8 / 35.4 / 65.7 MPa** (2.3 / 3.5 / 4.9) · 4.9 에서 *"pronounced σyy hotspots extending across the interface"* · 그림 2 색 막대 σ_yy ≈−165…+165 · σ_vM 0…≈105 MPa [판독] · 응력이 Li 쪽 경계에서 ≈20–40 µm 안에 몰린다 [판독].
- **β 민감도** (SI 그림 S6 · *"bulk 95th-percentile von Mises"*) [판독 · digitized.csv]:

| β | 2.3 | 3.5 | 4.9 mAh cm⁻² |
|---|---|---|---|
| 0 | 5.5 | 5.5 | 5.5 MPa |
| 0.001 | 11.1 | 14.9 | 19.7 |
| 0.002 | 18.8 | 28.7 | 41.9 |
| 0.003 | 28.0 | 45.8 | 70.7 |
| 0.005 | 51.2 | 87.4 | 131.1 |

  저자: *"Although the absolute stress magnitude varied with β, the increase in stress with plated Li capacity was consistently maintained for all nonzero β values"* · [카드 산술] 값은 β · Q 곱의 함수로 겹친다 (β·Q ≈0.007 → 28.0 · 28.7 · ≈0.0115 → 51.2 / 0.0105 → 45.8) — 식 (2) 의 꼴과 맞다.
- **f(x) 민감도** (S7): 가우스 셋 → 여섯 (같은 명목 진폭 · 4.9) → *"a correspondingly denser distribution of localized stress variations"* (색 막대 0–100 MPa).
- **[카드 산술] 원문 숫자 대조 둘** (해석은 원문에 없음 — 보류):
  ① **같은 β = 0.003 인데** 본문 95 백분위 (22.8 / 35.4 / 65.7) 와 S6 의 "bulk 95 백분위" [판독 28.0 / 45.8 / 70.7] 가 **5–10 MPa 다르다** — 두 통계의 영역 정의 [미확인].
  ② 첨두 σ_yy 는 Q 의 아핀 함수가 아니다: (σ_yy,peak + 20) = 24.6 / 63.3 / 130.8 MPa 가 진폭 비 1 : 1.52 : 2.13 에 대해 **1 : 2.57 : 5.32** (≈ Q^2.2).  선형 탄성 · 같은 f(x) · 고른 −20 MPa 면 한 점의 σ_yy 는 Q 의 1 차식이고, 첨두 자리가 바뀌는 경우에도 3.5 → 4.9 직선의 Q = 0 절편이 **−125 MPa** (경계 압축 −20 의 6 배) 가 되어야 한다.  β = 0 의 S6 값 5.5 MPa [판독] 도 −20 MPa 일축 (평면 변형 · 옆면 자유 17.6 · 옆면 구속 10.2 MPa [카드 산술]) 로 재현되지 않는다 — 옆면 경계 · 통계 정의 [미확인].
- **저자 한계** (p.4): *"Although the model does not explicitly account for Li creep, interfacial separation, or fracture, it provides a comparative framework for evaluating the increasing mechanical burden associated with larger plated-Li inventories."* · *"Since β is an effective model parameter rather than a directly measured material property, its influence was evaluated over a range of values (Figure S6)."* · 결론 쪽 해석 (p.5): *"the modeling suggests that complete strain elimination is unnecessary"*.
- ⚠ 영역 높이 100 µm ↔ 실제 분리막 0.15 g (Ø 13 mm · 진밀도 1.64 · 기공 0 이면 0.69 mm [카드 산술 · 랩 표준 값 대입]) — 위 경계를 계면 가까이 둔 단순화 [카드 해석].

### 3-4. ★ phase-field 모델 (p.8–10 · p.15–16 · 표 S3 · SI Note 1 · 그림 6 · S21 · S24–S26 · `eq_11`–`eq_21` · `eq_S01`–`eq_S10` · `tab_S3.png` · `fig_6a`–`fig_6d.png` · `fig_S21_*` · `fig_S24_*` · `fig_S25_*` · `fig_S26_*` · `txt_p8_phasefield_setup.png` · `txt_p9_soc_resolved.png` · `txt_p9_sensitivity.png` · `txt_p16_phasefield_bc.png`)
- **틀** (p.8 · p.15): *"A 2D, time-dependent model was developed to simulate Li penetration through the interconnected pores of the interlayer and porous host"* · Li = "Fluid 2" · 밀려나는 상 = 다른 유체 · Li/밀려나는 상 계면 = ϕ_Li 0.5 등고선 · *"Li was treated as a highly viscous Newtonian phase whose local viscosity was derived from a pore-scale Coble-type diffusion-creep relation"*.
- **지배식** (크롭 eq_11–eq_21):
  - (11) 0 = −∇p + ∇·[μ(∇v + ∇vᵀ)] + f_st (관성 무시 · 비압축 Stokes · 확산 계면 표면장력 힘) · (12) σ_f = −pI + 2μD_f · (13) D_f = ½(∇v + ∇vᵀ)
  - (14) **∂ϕ_Li/∂t + v·∇ϕ_Li = ∇·(M_ϕ ∇G)** (대류 Cahn–Hilliard) · (15) G = ∂f_mix/∂ϕ_Li − λ_pf ∇²ϕ_Li
  - (16) Δp = γ_s K_c (Young–Laplace · γ_s **0.5 N m⁻¹** · 젖은 벽 접촉각 **75°**)
  - (17) **B_Coble,i = D_i δ V_m / (R T d_p,i³)** · (18) ε̇_cr = B_Coble,i σ_eq · (19) η_Coble,i = 1/B_Coble,i · (20) **μ_Coble,i = η_Coble,i / χ_map** (χ_map = 3 · 일축 → 전단 점도) · i = 인터레이어 / 호스트 · 특성 확산 길이 = 국소 기공 폭
  - (21) v_dep = j_app M_Li / (F ρ_Li) (치밀 Li 석출 법선 속도)
- **매개변수** (표 S3 · 인쇄):

| 기호 | 값 | 출처 (표 그대로) |
|---|---|---|
| R | 8.314 J mol⁻¹ K⁻¹ | - |
| T | 318.15 K | Experimental value |
| j_app | 0.49 mA cm⁻² | Experimental value |
| D_interlayer | 3.15 × 10⁻¹⁰ m² s⁻¹ | Ref. S3, S4 |
| δ (확산층 두께) | 5 × 10⁻¹⁰ m | Ref. S5 |
| d_p,interlayer | 50 nm | **Assumed** |
| ε_p,interlayer | 0.4 | Ref. 39 (Xie 2024) |
| M_Li · ρ_Li | 6.94 g mol⁻¹ · 0.534 g cm⁻³ | — |
| ρ_dep (석출 밀도 인자) | 0.8 | Ref. S2 |
| d_p,host | 200 nm | **Assumed** |
| ε_p,host | 0.7 | Calculated |
| D_host | 3.15 × 10⁻¹¹ m² s⁻¹ | Ref. S2, S3 |
| γ_s | 0.5 N m⁻¹ | Ref. S6 |
| θ (Li 쪽 접촉각) | 75° | **Assumed** |
| h_gap (고정 간극) | 80 nm | **Assumed** |

- **기하 · 경계** (S21 · p.15–16): 인터레이어 **8 µm** (기공 50 nm) 위 호스트 **20 µm** (기공 200 nm) · 옆 **2 µm** · 곧은 세로 기공 (그림 6 에서 인터레이어 기공 ≈16 · 호스트 7 [판독] = 2 µm × 0.4 / 50 nm = 16 · 2 µm × 0.7 / 200 nm = 7 [카드 산술] — 기공 수로 기공률을 맞춘 그림) · ⚠ 그림 6 · S21 은 가로 · 세로 비율이 다르게 그려졌다 (2 µm × 28 µm 영역이 가로로 넓게 보인다) [판독] · 위 기공 입구 = 같은 적분 Li 유입 · 아래 호스트 경계 = 게이지 압력 **0 Pa** (*"without backflow suppression"*) · 고체 벽 = 젖은 벽 + **Navier 미끄럼 (미끄럼 길이 200 nm)** · 계면 두께 매개변수 **20 nm** (기공 크기 사례 10 nm) · 이동도 조정 매개변수 **2 × 10⁻⁸ m s kg⁻¹** (단위 원문 그대로) · 평균 계면 압력 = 고정 80 nm 간극의 부호 있는 게이지 압력 평균 (음수는 평균 뒤 0 이상만 표시) · **격자 · 풀이기 · 시간 간격 · 초기 조건 [미확인]**.
- **결과** (p.8–9 · 그림 6): ϕ_Li — SOC **14 %** 에 인터레이어 거의 포화 · **58 %** 까지 호스트 기공 채움 · 크리프 속도 0–21 nm s⁻¹ (인터레이어 작은 기공에서 빠른 아래 방향 수송) · 계면 압력 0–40 MPa 띠 (호스트 채움 동안 계속 오름) · **CNF 만**: SOC 19 % · 44 % · 계면 압력 0–400 MPa 띠 (*"develops a much larger pressure before appreciable host infiltration"*).
- **민감도** (p.9–10 · S24 · S25 · SOC 58 % · 기준 **33.2 MPa**):

| 바꾼 것 | 계면 압력 P_interface (MPa) | 같이 보인 값 |
|---|---|---|
| 호스트 기공 100 / 200 / 400 nm | **10.5 / 33.2 / 118.5** | μ_Coble,host 0.04 / 0.34 / 2.75 × 10⁸ Pa s · B 7.75 / 0.97 / 0.12 × 10⁻⁸ Pa⁻¹ s⁻¹ |
| 인터레이어 D × 0.1 / 1 / 10 | 33.2 / 33.2 / 33.2 | μ_Coble,interlayer 5.37 / 0.54 / 0.05 × 10⁵ Pa s · B 0.06 / 0.62 / 6.20 × 10⁻⁵ |
| 호스트 D × 0.1 / 1 / 10 | **346.5 / 33.2 / 2.3** | 점도 3.44 / 0.34 / 0.03 × 10⁸ Pa s · B 0.10 / 0.97 / 9.69 × 10⁻⁸ (⚠ 세로축 이름이 "interlayer" 로 인쇄 — 값은 호스트 쪽) |
| γ_s 0.125 / 0.5 / 2 N m⁻¹ | 33.8 / 33.2 / 29.3 | P_capillary 0.3 / 1.3 / 5.2 MPa |
| 접촉각 30 / 75 / 120° | 29.2 / 33.2 / 36.2 | P_capillary 4.3 / 1.3 / −2.5 MPa |

  저자: *"These results identify host-side transport resistance as the dominant parameter controlling the pressure required for Li redistribution under the present model conditions."*
- **전기화학 수송 분해** (SI Note 1 · 식 (S1)–(S10) · S26): j_app (0.49) = j_lith + j_nuc + j_grow · 탄소 리튬화 = 대칭 Butler–Volmer (α_a 0.5 · η = φ_e − φ_ion − U) · 이온 전류 κ_ion = **0.01 mS cm⁻¹** (인터레이어) · **0.001 또는 0.01** (호스트) — *"relatively favorable ionic transport conditions compared with reported values for lithiated amorphous carbon (10⁻⁶–10⁻⁴ mS cm⁻¹) and vapor-grown carbon fibers (1.91 × 10⁻³ mS cm⁻¹)"* [S7 · S8] · 전자 κ_e **1000 S m⁻¹** [S3] · 핵생성 (S5) · 성장 (S6) Tafel 꼴 (α_c = 1 · b_nuc 0.30 · i0,grow 1.0 × 10⁻³ A m⁻²) · j_electrochem = −∫ a_host (i_nuc + i_grow) dx (a_host = 2ε/d) · 크리프 한계 (S8 · S9): **N_creep = 4 ε_p D σ_stack δ / (R T τ_creep L d_p)** (τ_creep,interlayer = 1 · τ_creep,host = **1.84** [S9]) · j_creep = F N_creep (S10) · S26 [판독]: 크리프 등가 전류가 ≈0.6–0.7 (κ 0.001) · ≈1.0 mAh cm⁻² (κ 0.01) 에서 출발해 ≈3 mAh cm⁻² 부터 **≈0.44 mA cm⁻²** 고원 · 전기화학 수송 ≈0.02–0.03 mA cm⁻² → *"pressure-driven creep transport plays a dominant role"* (p.10).
- **[카드 산술] 원문 숫자 재현** (식 · 표만으로):
  - 식 (17)–(20) 기준값: B_host = 3.15 × 10⁻¹¹ × 5 × 10⁻¹⁰ × 1.30 × 10⁻⁵ / (8.314 × 318.15 × (2 × 10⁻⁷)³) = **0.967 × 10⁻⁸** · μ_host = 1/(3B) = **0.345 × 10⁸ Pa s** · B_interlayer = **0.619 × 10⁻⁵** · μ = **0.538 × 10⁵** · 기공 100 · 400 nm → 7.74 · 0.121 × 10⁻⁸ — S24 인쇄값과 같다.
  - 모세관: P_cap = 2 γ_s cos θ / d_p,host → 1.29 (기준) · 4.33 (30°) · −2.50 (120°) · 0.32 · 5.18 MPa (γ 0.125 · 2) — S25 와 같다.
  - **SOC 58 % = 기공 다 찬 때**: (0.4 × 8 + 0.7 × 20) µm × Li 2062 mAh cm⁻³ × ρ_dep 0.8 = 2.84 mAh cm⁻² = 4.9 의 **57.9 %** · 인터레이어만 = 0.53 mAh cm⁻² = 10.8 % (본문 "SOC 14 %") — SOC 기준 = 4.9 mAh cm⁻² · 석출 밀도 인자 0.8 로 읽힌다 [카드 해석].
  - **크리프 한계 ↔ 스택 압력**: 식 (S9) 에 표 S3 값 · τ_creep,host 1.84 · **σ_stack 20 MPa** 를 넣으면 F N_creep,host = **0.437 mA cm⁻²** = S26 고원 0.44 [판독] — 모델의 σ_stack 은 표 S3 에 없지만 20 MPa 로 읽힌다 [카드 해석] · 같은 식으로 인터레이어 한계 ≈46 mA cm⁻² (호스트가 병목) · 파우치 **1 · 2 MPa** 면 호스트 한계 **0.022 · 0.044 mA cm⁻²** (식이 σ_stack 에 비례 — p.11 저자 문장과 같은 방향).
  - v_dep (식 21) = 0.66 nm s⁻¹ (0.49 mA cm⁻²) — 크리프 속도 띠 0–21 nm s⁻¹ 와 견줄 크기.
- **실측 대조** (p.9 · S22–S23): SOC **10 %**: Ag 든 영역이 **7.9 µm** Ag–C 안에만 · XRD LiAg + Li₉Ag₄ · SOC **50 %**: CNF 대부분에 Li (뚜렷한 계면 Li 층 없음 · 그림 글자 Ag–C 8.2 µm) · SOC **75 %**: 계면 Li **10.7 µm** (그림 글자 Ag–C 8.3 µm) → 충전 끝 **16.3 µm** (그림 5b) — *"broadly consistent with the phase-field prediction that host filling approaches completion near SOC = 58%"*.

### 3-5. ★ CNF 망 · Ag–C 층 (p.6 · p.8 · p.10 · 표 S2 · S4 · 그림 3–5 · S8–S15 · S27 · `tab_S2.png` · `tab_S4.png` · `eq_ST2_cnf_layer_porosity.png` · `fig_S8.png` · `fig_S11.png` · `fig_S12.png` · `fig_S13.png` · `fig_5a.png` · `fig_5b.png` · `fig_S27.png` · `txt_p6_cnf_compression.png` · `txt_p12_storage_agc.png` · `txt_p13_storage_estimate.png`)
- **표 S2** (인쇄 · *"The average pore volume, pore diameter, and density were taken from the material specifications provided by the supplier"*):

| | LC CNF | HC CNF |
|---|---|---|
| 비표면적 | 54 m² g⁻¹ | 39 |
| 평균 세공 부피 | 0.12 cm³ g⁻¹ | 0.12 |
| 세공 지름 | 89.3 Å | 126.1 Å |
| 밀도 (공급사) | 1.8 g cm⁻³ | 1.9 |
| 전극 넓이 · CNF : SBR · CNF 밀도 · SBR 밀도 | 1.33 cm² · 2 : 1 · **1.6** · 0.94 (Ref. S2) | 같음 |
| 면 질량 | 0.76 mg cm⁻² | 0.70 |
| 층 두께 | 19.6 µm | 18.5 µm |
| 층 기공률 | **70.1 %** | **71.0 %** |

  기공률 식 (번호 없음 · `eq_ST2`): ε_p,host = 1 − (면 질량)(CNF 비/CNF 밀도 + SBR 비/SBR 밀도)/두께 · [카드 산술] 재현 70.8 · 70.1 % ✓ · 공급사 밀도 (1.9 · 1.8) 를 넣으면 **73.3 · 71.9 %** — 표가 쓴 "CNF density 1.6" 을 고르면서 2 %p 남짓 바뀐다.
- **결정성** (p.6 · 그림 4a–b): I_D/I_G **0.99 (LC) · 0.19 (HC)** (그림 글자 · 왼쪽 패널에는 "LC CNF" 이름표가 원 그림에도 없다 — LC 는 본문 *"low-crystallinity (LC) CNF exhibits comparable D- and G-band intensities"* 로 판별 · 0.19 는 본문에도) · LC 셀은 큰 비가역 · 감쇠 (그림 4b) → HC 선택 · *"the observed electrochemical difference is primarily associated with carbon crystallinity"*.
- **형상** (S8 · S9 · 그림 3f): 엉킨 섬유 · 섬유 지름 [판독 거칢] ≈0.2–0.5 µm (S8 눈금 5 µm = 237 px · 2 배 확대에서 섬유 폭 20–50 px · SEM 가장자리 번짐으로 클 수 있음) · 길이 = 시야 (5 µm) 를 넘는 마디가 많다 · **원문 숫자 없음**.
- **압축** (p.6 · S10–S13 · *"A thicker CNF layer (∼35 µm) was used for this measurement to more clearly observe its elastic and compliant behavior"*):
  - 압력 지도 (S11 그림 글자): 5 MPa 로 누른 직후 P_avg **4.75** → 1 h 4.71 → 2 h 4.72 → 4 h **4.72 MPa** (−0.6 % [카드 산술]) — *"stable load transmission without pronounced time-dependent collapse"*.
  - 5 회 누름–회복 (S12) [판독]: 누른 뒤 **33.15 → 32.92 µm** · 회복 뒤 **35.11 → 34.65 µm** → 누름 변형 ≈**5.6 %** (5 MPa) · 할선 겉보기 탄성률 ≈**90 MPa** (5 MPa ÷ 0.056) [카드 산술 · 판독 · 1 축 · 옆 구속 [미확인]] · 5 회 동안 회복 두께 −1.3 % (영구 변형).
  - SEM (S13): 5 회 뒤에도 다공 골격 유지 (정성).
- **충방전 중 두께** (그림 5 · S27 그림 글자): 제작 뒤 Ag–C **7.7** · CNF **18.5 µm** → 첫 충전 뒤 Ag–C **8.3** · 계면 Li **16.3** · CNF **21.0 µm** (+13.5 %) → 방전 뒤 Ag–C **8.0** · CNF **18.7 µm** (*"nearly recovers its initial morphology … no evident pore collapse, delamination, or permanent structural damage"*, p.10).
  - [카드 산술 · 가정 명시] 계면 Li 층 16.3 µm 를 석출 밀도 인자 0.8 · 1.0 으로 환산하면 2.69 · 3.36 mAh cm⁻² → CNF 안 Li = 4.9 − 0.61 (Ag–C) − 그것 = **1.6 · 0.9 mAh cm⁻²** — 원문 추정 1.71–2.51 (아래) 과 같은 자릿수 또는 아래 (충전량을 4.9 로 둔 경우 · 실제 첫 충전량은 그림 S18 에서 ≈5.7 mAh cm⁻² [판독 거칢]).
- **저장량 추정** (p.12–13 · 표 S4 · 그림 8d–e): Ag–C = 탄소 리튬화 **0.12** + 기공 채움 **0.49** = **0.61 mAh cm⁻²** → 나머지 **4.29** · CNF 수용 (석출 밀도 인자 0.6–0.9) **1.71–2.51 mAh cm⁻²** — *"This range represents an estimate of the capacity that the CNF can accommodate, rather than a direct measurement of its actual Li inventory"* · 4.29 를 다 담으려면 CNF **≈35.4 µm** (인자 0.8) · 비활성 부피 (3 × 3 cm²) **Ag–C 만 4.6 · 이 논문 9.5 · 영변형 13.9 mm³**.
  - [카드 산술] 재현: CNF 18.5 µm · 기공 0.71 · Li 2062 mAh cm⁻³ · 탄소 200 mAh g⁻¹ → **1.72 / 2.53** (인자 0.6 / 0.9) · 4.29 → **35.1 µm** ✓ · Ag–C: 겉보기 1.25 g cm⁻³ ↔ 성분 밀도 (표 S4) 로 이론 1.99 → 기공 0.37 → 탄소 0.135 + 기공 0.477 = **0.61** ✓ (나눔은 0.13 / 0.48 로 조금 다르다).
  - ⚠ [카드 산술] 비활성 부피 4.6 / 9.5 / 13.9 mm³ 는 본문이 말한 *"geometric inactive-anode volume, calculated from the total thickness of the non-Li anode layers"* (= 7.8 · 26.3 · 43.2 µm × 9 cm² = **7.0 · 23.7 · 38.9 mm³**) 와 맞지 않고, **기공을 뺀 고체 부피** (Ag–C 4.4 · + CNF 고체 4.9 = 9.3 · + 35.4 µm CNF 고체 9.2 = 13.6 mm³) 와 맞는다 — 정의 문장과 숫자가 어긋난다.
- **Ag–C 층**: 표면 · 단면에 Ag 나노 입자가 비정질 탄소 기질에 고르게 (그림 3c · S14) · XRD 금속 Ag 38.1° · 44.3° 부근 (S15 [판독]) · ≈450 MPa 로 치밀화하면 SUS 박이 저절로 떨어진다 (*"owing to the stronger adhesion between Ag–C and the SE layer"*, p.6 · 그림 3e) · CNF 만 셀은 Li 가 SE/CNF 계면에 모임 — *"This behavior originates primarily from the insufficient interfacial contact between the sulfide SE and the porous CNF layer"* (p.7 · S19).
- **충전 CNF 층 XRD** (그림 5c · p.8): Li–Ag 합금 반사 ≈23° · 27–28.3° · Li 많은 Li–Ag ≈36.4° · 금속 Ag 38.2° · 44.3° 거의 없음 · LiC₆ · LiC₁₂ 표지 · ToF-SIMS Li⁻ 가 CNF 영역 전체에 (그림 5d).

### 3-6. 전기화학 · 구조 (p.6–7 · p.10–11 · 그림 4b · 4e · 7 · 8 · S18 · S28–S32 · `fig_4e.png` · `fig_7a`–`fig_7g.png` · `fig_8a`–`fig_8e.png` · `txt_p10_pouch_20mpa_condition.png` · `txt_p11_creep_flux_stack_pressure.png`)
- **CNF 두께 vs 첫 사이클** (그림 4e [판독]): 면적 용량 **5.17 / 5.04 / 4.96 mAh cm⁻²** · 첫 효율 **89.6 / 88.6 / 87.3 %** (0 / 10 / 20 µm) — 탄소 비가역 리튬화 때문 (p.6).
- **반쪽 셀 Anode ‖ Li** (그림 7a–b · 0.1C · 45 °C): 핵생성 과전압 **12.1 / 7.5 / 7.8 mV** · 리튬화 용량 **0.16 / 0.53 / 0.72 mAh cm⁻²** (CNF 만 / Ag–C 만 / Ag–C/CNF · 그림 글자) · DRT (그림 7c): 시간 상수 순서대로 R_SE · R_int · R_ct,Li (ref [49]) — Ag–C/CNF 의 R_ct,Li 봉우리가 조금 낮고 빠르다 [판독].
- **풀 몰드 셀** (그림 7d–e · 0.2C · 45 °C · 20 MPa): Ag–C 만 = **213 번째 단락** · Ag–C/CNF = **250 사이클 이상** · [판독 · digitized.csv] 면적 용량 Ag–C 만 4.82 (1) → 4.68 (5) → 3.16 (200) · Ag–C/CNF 4.57 (1) → 4.43 (5) → 2.88 (200) → 2.67 (249) mAh cm⁻² → 200 번째 유지율 (5 번째 기준) **67.5 vs 65.0 %** [카드 산술] — ⚠ 단락 전까지는 Ag–C/CNF 의 용량 · 유지율이 **높지 않다**; 차이는 단락 없음 (본문 *"significantly improved capacity retention"* 은 Ag–C 만 셀의 단락 뒤를 포함한 말 [카드 해석]) · 사이클 뒤 SEM: Ag–C 만 = 변형된 Ag–C · 불규칙 Li (그림 7f) · Ag–C/CNF = 층 구조 유지 (그림 7g).
- **파우치** (그림 8 · S31–S32 · 3 × 3 cm² · 0.3C): **2 MPa** 250 사이클 유지율 **92.0 % (Ag–C/CNF) vs 80.8 % (Ag–C 만)** · 첫 방전 **141.8 (1 MPa) vs 158.3 mAh g⁻¹ (2 MPa)** · 1 MPa 도 35 사이클 안정 (S32) · 그림 8c 의 이 논문 표지 = 순환 전류 **≈11.7 mA** · 92.0 % [판독] → 9 cm² 에서 1.30 mA cm⁻² → 0.3C 면 ≈**4.3 mAh cm⁻²** [카드 산술 · 1C = 공칭 용량 가정 · 파우치 적재 원문 미기재].
- **스택 압력 해석** (p.10–11): *"Accordingly, the 20 MPa condition should be regarded as the selected operating condition required for stable cycling of the present powder-assembled mold-cell configuration, rather than as an intrinsic pressure requirement of the Ag–C/CNF architecture."* · *"the diffusional-creep relation (Equation S9) indicates that the creep molar flux into the CNF host is proportional to the applied stack pressure when other model parameters are held constant"*.

### 3-7. ★ 원문 안 어긋남 · 확인할 것 (고치지 않고 적는다)
1. **단락 사이클**: 본문 "128th" (불규칙 시작) ↔ 그림 1c 표지 "129th" ↔ 그림 1e 128–130 번째 — 같은 사건의 다른 표기일 수 있다.
2. **95 백분위 von Mises**: 본문 22.8 / 35.4 / 65.7 ↔ S6 β = 0.003 [판독] 28.0 / 45.8 / 70.7 MPa (§3-3).
3. **첨두 σ_yy 의 Q 의존** 이 진술된 선형 모델로 재현되지 않는다 (§3-3 ②).
4. **비활성 부피**: "geometric … total thickness" 정의 ↔ 숫자는 고체 부피 (§3-5).
5. **SBR 함량 표현**: *"33 wt.% with respect to the CNF mass"* (p.13) ↔ CNF : SBR = 2 : 1 (표 S2 = SBR 이 CNF 질량의 50 % · 전체의 33 %) [카드 산술].
6. **S24 셋째 열** 세로축 이름 "μ_Coble,interlayer" · "B_Coble,interlayer" ↔ 값은 호스트 (0.34 × 10⁸ · 0.97 × 10⁻⁸ = 호스트 기준값).
7. **Ag–C 두께**: 7.7 (그림 5a 제작 뒤) · 7.8 (표 S4) · 7.9 (S22 SOC 10 %) · 8.2 (S22 SOC 50 %) · 8.3 (S22 SOC 75 % · 그림 5b 충전 뒤) · 8.0 µm (S27 방전 뒤) · 모델 8 µm — 측정 상태가 다른 값들 (리튬화로 7.7 → 8.3 µm = +8 % [카드 산술]).
8. **E = 22.1 GPa 의 출처 (Ref. S1 = Pustorino 2025)** ↔ 정본 그 카드의 표 3 · 인용 비교에 22.1 이 없다 (48H 29.0 · ν 0.33) [다른 카드] — Pustorino 원문 PDF 로 최종 확인 필요.
9. **"Acid-treated CNF"** (그림 3a) ↔ 실험 절에 산 처리 없음.
10. 그림 8f 의 철자 *"Unifrom deposition"* (그림 글자 그대로).
11. **모델 전류 0.1C (0.49 mA cm⁻²)** ↔ ΔP 사이클 0.2C (0.98) — §3-1 마지막 행.

---

## 4. ★ 방법 — 측정 사슬 · 모델 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 측정 사슬
분말 (볼밀 양극 · LPSCl) → 몰드에서 450 MPa (양극 + Ag–C) → 150 MPa (CNF) → 하중 셀 틀에 20 MPa 로 묶음 → 45 °C 충방전 + 하중 셀 ΔP · dP/dt (미분) → 사후 FIB-SEM · EDS · XRD · ToF-SIMS (충전 상태 · SOC 10 / 50 / 75 % · 방전 뒤) · DRT.  파우치는 따로 (WIP 30 → 500 MPa · 1 · 2 MPa) · 압력 측정 없음.  CNF 층 압축은 별도 시편 (≈35 µm) · 압력 지도 센서.

### 4-2. 모델 사슬 (두 모델은 서로 이어지지 않는다)
- FE: Q → h_Li (식 1) → u_y = β h f(x) (식 2) → 정적 선형 탄성 (식 3–9) → σ_yy · von Mises (식 10) · 결과는 세 Q 의 상대 비교 · 실측 ΔP 는 입력도 출력도 아니다.
- phase-field: 곧은 기공 2D → Stokes + 대류 Cahn–Hilliard + Coble 점도 (식 11–21) → ϕ_Li(t) · 크리프 속도 · 계면 압력 → Note S1 의 전류 분해 (S1–S10).  호스트 · 인터레이어의 **탄성 · 변형 (CNF 의 21.0 µm 팽창) 은 계산하지 않는다** (고정 기공 벽) [카드 해석].

### 4-3. 입자 처리 ★
- 실험: CNF = 엉킨 섬유 망 (그림 3f · S9) · Ag–C = 나노 입자 복합 · SE · 양극 = 분말 압분체 — 입자 단위 정량 없음.
- FE: **SE 연속체 한 상** · Li · 섬유 · 입자 없음.
- phase-field: **곧은 기공 벽 (고정 고체)** + 두 유체 · 섬유 형상 · 접촉 · 미끄럼 · 박리 없음 (벽 젖음 · Navier 미끄럼은 유체 경계 조건).
- 그림 3d · 3g 의 구 입자 그림은 모식이다 (DEM 아님).

### 4-4. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말한 문장** — **말 없음** (본문 · SI 에 DEM · discrete element 낱말 0 회).
2. **소성 · 큰 변형을 넣기 어려운 이유 · 우회 · 비용** — FE 는 Li 소성 · 크리프 · 셀 순응을 계산하지 않고 **효과 매개변수 β 하나로 대체**: *"only a fraction of the deposition-induced deformation is transferred to the SE because deformation can be partially relaxed through Li plasticity and creep, occupation of interfacial free volume, and compliance of the surrounding cell stack"* (p.4) · *"Uniform Li growth was assumed to be accommodated primarily by Li plastic flow, creep, and compliance of the cell stack and therefore was not imposed directly on the elastic LPSCl domain"* (p.15) · *"Since β is an effective model parameter rather than a directly measured material property …"* (p.4).  phase-field 는 Li 소성을 **Coble 크리프 점도의 뉴턴 유체**로 바꿨다 (탄성 · 항복 없음, p.15).  계산 비용 [미확인] (FE 4 000 요소 · phase-field 격자 미기재).
3. **2D / 3D** — 두 모델 다 **2D** (FE 평면 변형 · phase-field 곧은 기공) · 2D → 3D 전이에 대한 말 **없음**.
4. **압력을 뺄 때의 거동** — 셀: ΔP 가 방전 (Li 탈리) 동안 내려간다 (그림 1a) · CNF 층: 5 MPa 누름–회복 5 회 (≈5.6 % · 회복 −1.3 %/5 회 [판독]) · 방전 뒤 CNF 18.7 µm (제작 18.5) · SE 의 탈압 · 회복 [미확인].

### 4-5. 기법 미니 용어집
| 용어 | 뜻 (이 논문 안에서) |
|---|---|
| ΔP | 하중 셀 압력의 한 사이클 안 꼭대기 − 바닥 (상대값 · 스택 20 MPa 위) |
| dP/dt | ΔP 곡선의 시간 미분 — 기계 변화 속도 (단락 때 0 으로 수렴) |
| 효과 전달 인자 β | 석출 Li 두께 가운데 SE 경계에 **불균일 변위로 전달되는 몫** (측정 아님 · 0.003) |
| f(x) | 영평균 정규화 공간 분포 (가우스 셋 → 여섯) |
| Coble 크리프 점도 | 확산 크리프 계수 B = Dδ V_m/(R T d³) 의 역수를 일축 → 전단 (÷3) 으로 바꾼 뉴턴 점도 · 기공 폭 d³ 에 비례 |
| 석출 밀도 인자 ρ_dep | 겉보기 Li 밀도 ÷ 이론 0.534 (0.6–0.9 · 기준 0.8) |
| 크리프 등가 전류 j_creep | 이미 석출된 Li 가 크리프로 호스트에 들어가는 몰 유속 × F (전자 이동 없음) |
| SOC (phase-field) | 4.9 mAh cm⁻² 충전 중 진행 몫 (58 % = 기공 다 참 [카드 해석]) |
| LC / HC CNF | 낮은 · 높은 결정성 (PR-25-XT-PS · PR-25-XT-LHT) |
| EPD | 전기영동 증착 (대전 CNF 를 전기장으로 SUS 에 쌓음) |
| WIP | 온간 등방압 (파우치 30 → 500 MPa) |
| DRT | 이완 시간 분포 — R_SE · R_int · R_ct,Li 봉우리 |

---

## 5. Figure set ★
| 그림 | 보이는 것 | 우리가 쓸 것 |
|---|---|---|
| **Fig. 1** (`fig_1.png` · 패널 `fig_1a`–`fig_1f`) | (a) 전압 + ΔP vs 시간 (2.3 · 3.5 · 4.9 · 인가 전류 0.61 · 0.93 · 1.30 mA) · (b) dP/dt · (c) 200 사이클 · (d) 첫 효율 · 100 번째 유지율 · (e) 128–130 번째 dP/dt · (f) 사이클 뒤 단면 SEM | ★ 스택 위 상대 ΔP 의 면적 용량 비례 (≈0.1 MPa per µm 치밀 Li [카드 산술]) · 고장 신호 (dP/dt → 0) |
| **Fig. 2** (`fig_2.png` · `fig_2a` · `2b`) | FE σ_yy · von Mises 지도 (120 × 100 µm · 세 용량) | 효과 매개변수 하나 (β) 의 경계 처방 FE 꼴 — 우리 연화 E_eff 보고와 같은 지위 |
| **Fig. 3** (`fig_3.png` · `fig_3a`–`3g`) | EPD 모식 · CNF 사진 · Ag–C 단면 · 제작 순서 (450 → SUS 박리 → CNF 150 MPa) · 기능 모식 | 층마다 다른 압력으로 굳히는 제작 순서 |
| **Fig. 4** (`fig_4.png` · `fig_4a`–`4f`) | Raman (I_D/I_G 0.99 · 0.19) · LC/HC 전압 · CNF 0/10/20 µm ΔP (2.3/2.0/1.6) · dP/dt · 첫 용량 · 효율 · 충전 CNF 면 SEM | ★ CNF 두께 → ΔP 감소 |
| **Fig. 5** (`fig_5.png` · `fig_5a`–`5d`) | 제작 · 충전 단면 (7.7/18.5 → 8.3/16.3/21.0 µm) + C · Ag · P 지도 · XRD · ToF-SIMS | 두께 변화 (CNF +13.5 %) · Li 침투 |
| **Fig. 6** (`fig_6.png` · `fig_6a`–`6d`) | phase-field ϕ_Li (SOC 0/14/58 %) · 크리프 속도 · 계면 압력 (0–40 MPa) · CNF 만 (0–400 MPa) | ★ Li 를 점성 유체로 둔 기공 채움 계산의 꼴 |
| **Fig. 7** (`fig_7.png` · `fig_7a`–`7g`) | 반쪽 셀 핵생성 · 리튬화 용량 · DRT · 풀 셀 (213 번째 단락 vs 250+) · 사이클 뒤 SEM | 전기화학 결과 (흐름 밖) |
| **Fig. 8** (`fig_8.png` · `fig_8a`–`8f`) | 파우치 (2 MPa · 92.0 vs 80.8 %) · 문헌 비교 · Li 저장 vs CNF 두께 · 비활성 부피 · 기전 모식 | 부분 수용 설계 · ⚠ 비활성 부피 정의 어긋남 |
| **SI Fig. S1–S5** (`fig_S1`–`S5`) | NCM · LPSCl XRD · 하중 셀 틀 사진 · 모식 · 최대 dP/dt · 반쪽 셀 전압 · 같은 전류 0.98 mA cm⁻² 수명 | ★ 장치 · 같은 전류 대조 |
| **SI Fig. S6–S7** (`fig_S6` · `S7`) | β 민감도 (0–0.005) · f(x) 여섯 혹 | ★ 효과 매개변수 민감도 보고 꼴 |
| **SI Fig. S8–S15** (`fig_S8`–`S15`) | CNF SEM · EPD 층 위 SEM · 압력 지도 장치 · 5 MPa 4 h · 5 회 누름–회복 두께 · 단면 · Ag–C SEM/EDS · XRD | ★ CNF 망 압축–회복 |
| **SI Fig. S16–S20** (`fig_S16`–`S20`) | 최대 dP/dt (CNF 두께) · 확대 dP/dt · 첫 전압 · CNF 만 단면 (Li ≈26 µm) · CNF 만 ΔP 2.3 MPa | CNF 단독은 ΔP 를 못 줄인다 |
| **SI Fig. S21–S26** (`fig_S21`–`S26` + 패널 `fig_S21_*` · `fig_S22_soc*` · `fig_S24_*` · `fig_S25_*` · `fig_S26_*`) | phase-field 기하 · SOC 단면 · Ag–C XRD (SOC 10 %) · 민감도 (기공 · D · γ · θ) · 전류 분해 | ★ 매개변수 민감도 · 크리프 고원 0.44 mA cm⁻² |
| **SI Fig. S27–S32** (`fig_S27`–`S32`) | 방전 뒤 단면 (8.0 · 18.7 µm) · Nyquist · 사이클 전 Ag–C 단면 · 213–214 번째 dP/dt · 파우치 사진 · 1 vs 2 MPa | 회복 · 저압 운전 |
| **표 S1–S4** (`tab_S1`–`S4`) | FE 매개변수 · CNF 물성 + 기공률 식 · phase-field 매개변수 · 저장량 매개변수 | 입력 원장 |
| 식 크롭 32 (`eq_01`–`eq_21` · `eq_S01`–`eq_S10` · `eq_ST2`) · 근거 문단 20 (`txt_p*`) | 본문 · SI 식 전부 · 인용 문장 | 보고서 붙임 |

## 6. Post-processing ★
- **ΔP**: 하중 셀 원 신호에서 한 사이클의 꼭대기 − 바닥 (그림 위 점선 화살표) · 기준선 처리 · 거름 [미확인].
- **dP/dt**: ΔP 곡선의 시간 미분 (평활 여부 [미확인]) · 최대값 막대 (S3 · S16).
- **FE**: Gauss 점 4 개 평균 → 요소 응력 · 첨두 σ_yy · 95 백분위 σ_vM (영역 정의 [미확인]).
- **phase-field**: ϕ_Li 0.5 등고선 · 80 nm 간극 게이지 압력 평균 (음수 = 0 으로 표시) · 크리프 등가 전류 (S10).
- **기공률 (CNF 층)**: 질량 · 두께 · 성분 밀도 식 (표 S2 아래).
- **Li 저장량**: 기공 부피 × Li 밀도 × 석출 밀도 인자 + 탄소 200 mAh g⁻¹ (표 S4).
- **판독 (이 카드)**: 크롭 300 dpi · 축 눈금 위치 · 막대 윗변 (25 행 연속) · 표지 색 판별 — digitized.csv note 열.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처를 병기해 적는다)

### 7-1. 비교표 (모든 행에서 **계 · 축 · 측정 상태가 다르다**)
| 양 | 이 논문 | 우리 | 같은 / 다른 · 이유 |
|---|---|---|---|
| 제조압 | 양극 + Ag–C **450 MPa** · CNF **150 MPa** · 파우치 WIP 30 → 500 MPa | DEM · MPM 압밀 **300 MPa** [우리] | 같은 "제조압" 부류 (비교 문서 머리 "3 종 압력 구분") · 계 다름 (음극 층 ↔ 양극 복합체) |
| 운전 스택압 | 몰드 **20 MPa** · 파우치 **1 · 2 MPa** | 압밀 뒤 판 고정 이완 · 스택 단계 · 언로딩 = 진행 중 (언로딩 키트) [우리] | 우리 계산에 **스택 압력 단계가 아직 없다** — 20 MPa 는 300 MPa 의 ≈7 % [카드 산술] |
| 압력 요동 | ΔP **1.1–2.4 MPa** (스택의 5.5–12 %) · ≈0.1 MPa per µm 치밀 Li (이 틀) | 없음 (A10 사이클 원장 = 접촉 후처리 · 압력 없음) [우리] | 흐름 밖 — 반대쪽 판 부피 변화 ↔ 스택 순응 |
| SE 탄성 입력 | FE **E 22.1 GPa · ν 0.33** (K 21.7 · G 8.31 [카드 산술]) · 출처 의심 (§3-7 ⑧) | DFT E_VRH 22.06 · B₀ 26.23 · ν 0.360 · G 8.11 · DEM E_eff **1.35** (18 배 연화) · MPM **1.53** (ν 0.49 · K 25.5) [우리] | E 는 우리 DFT 와 거의 같다 (출처 다름) · ν · K 다름 · 그들 FE 는 압밀이 없어 연화가 필요 없다 |
| Li 거동 | FE 미포함 (β 대체) · phase-field = Coble 점도 뉴턴 유체 (μ 호스트 3.4 × 10⁷ · 인터레이어 5.4 × 10⁴ Pa s [카드 산술 = S24]) | Li 금속 음극 모델 없음 [우리] | 흐름 밖 |
| 탄소 섬유 망 | Pyrograf-III PR-25 **기상성장 CNF** 층 · 18.5–19.6 µm · 기공 70–71 % · 0.70–0.76 mg cm⁻² · SBR 1/3 · 모델 κ_e **1000 S m⁻¹ (= 10 S cm⁻¹ · 층 유효 · Ref. S3)** · 5 MPa 에서 ≈5.6 % (할선 ≈90 MPa [카드 산술 · 판독]) | VGCF (Showa Denko VGCF-H Ø 150 nm · CL-47) 를 양극 복합체에 · STEP3 유효 σ_VGCF **100 S cm⁻¹** · MPM 섬유 E **100 GPa** (CL-93) [우리] | **다른 양** — 층 유효 (망 · 결합제 · 기공) ↔ 복셀 유효 / 단섬유 · 같은 표에 넣지 않는다 |
| 기공 연산자 | CNF 층 = 질량 · 두께 · 성분 밀도 (고른 밀도에 2 %p 민감) · 비활성 부피 = 고체 부피 (정의 문장과 어긋남) | ε_sphere · 합집합 · 질량 보존 (명시 등록) [우리] | 정의 기록 꼴 대조만 |
| 계면 압력 (모델) | phase-field SOC 58 % **33.2 MPa** (스택 20 MPa 보다 큼 · 국소 80 nm 간극) | — | 흐름 밖 |

### 7-2. ★ "스택 압력" 을 우리 계획에 들일 때
- 쓸 수 있는 것: **운전 스택 (20 MPa) 위에서 반대쪽 판의 부피 변화가 만드는 압력 요동의 크기 감각** (ΔP ≈1–2.4 MPa · ≈0.1 MPa per µm · 이 틀 한정) — 우리 언로딩 · 스택 단계 계산에서 *"판을 고정 압력에 두느냐 고정 간극에 두느냐"* 를 정할 때의 실측 사례 (이 논문 = 볼트로 죈 틀 → 간극 고정에 가까움 · 압력이 출력 [카드 해석 · 정본 `zhang2026_anode_free_asslsb_li2s_pi3_na_current_collector` 와 같은 부류]).
- 붙일 꼬리표: 상대 ΔP · 하중 셀 틀 강성 미기재 · 45 °C · 양극 수축 섞임 · Ø 13 mm 몰드.
- 쓰지 말 것: ΔP 를 SE · 양극 재료 강성으로 읽는 것 · 몰드 20 MPa 결과를 파우치 1–2 MPa 로 옮기는 것 (저자 자신이 금지 — §3-6).

### 7-3. frame[5] — 어느 반쪽을 가졌나
- 이 논문 = **실험 (스택 압력 요동 · 단면 · 수명)** + **선형 탄성 SE 응력 (경계 처방)** + **Li 크리프 유동 (phase-field)**.  우리 분업으로는 MPM 쪽 (유동 · 응력장) 의 **음극 · 연속체 판**이고 DEM 쪽 (접촉망 · 수송) 은 없다.
- 없는 반쪽: 압밀 과정 · SE 입자 · 양극 · 접촉 · 박리의 정량 · 3D.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문은 **음극 (Li · Ag–C · CNF) 축**이고 순수 SE 기공 · 진밀도 · 복합 양극 기공 값이 **없다** — 랩 표준과 나란히 놓을 숫자 0.  §3-3 의 0.69 mm 는 랩 표준 진밀도를 대입한 카드 산술이지 문헌 값이 아니다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ 반면교사 둘 — ① **기공률이 고른 밀도에 2 %p 넘게 움직인다** (CNF 1.6 ↔ 공급사 1.9 → 71.0 ↔ 73.3 %) → 우리 질량 보존 기공에 쓰는 진밀도 (1.64) 의 출처 · 값을 등록 칸에 ② **정의 문장과 숫자가 다른 부피** ("geometric total thickness" ↔ 고체 부피) → 연산자 이름 (ε_sphere · 합집합 · 질량) 을 숫자 옆에 | SE · 복합 양극 기공 없음 |
| **단계 1** (3D 메모리 · 장 수) | 없음 (두 모델 2D · FE 4 000 요소) | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 닫힌 꼴 검산의 예 — Coble 점도 (식 17–20) · 모세관 압력 · SOC 58 % 가 표 값만으로 재현된다 [카드 산술] → 우리 2D 코드 단위 시험도 "표 값 → 닫힌 꼴 → 그림 값" 으로 | MPM · 입자 없음 |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 를 실험 기공에 맞춤) | 없음 — SE 는 탄성 (E 22.1 · ν 0.33) 만 · 항복 · 경도 없음 · 출처 의심 | 맞춤 표적 아님 |
| **단계 5** (3D 복합 압밀) | 없음 (양극 압밀 정량 없음) · 제작 순서 (450 MPa 치밀 층 → 150 MPa 다공 층) 는 "층마다 다른 압력" 의 실례 | — |
| **단계 6** (탈압 · 되돌아옴) | ★ 탄소 섬유 망의 누름–회복 실측: 5 MPa · ≈5.6 % · 회복 −1.3 %/5 회 · 4 h 유지 P_avg −0.6 % [판독 · 인쇄] · 셀 스택 ΔP 가 충전 (부피 증가) 에 오르고 방전에 내린다 (20 MPa · 45 °C) → **조건 R4 의 흐름 밖 표적** (SE 아님 · 섬유 망 · 셀 스택) | SE 의 탈압 회복 · 탈압 곡선 없음 |
| **단계 7** (형상 · 피복 · 수송) | 흐름 밖: 층 유효 κ_e 1000 S m⁻¹ (모델 입력 · Ref. S3) · 호스트 κ_ion 0.001–0.01 mS cm⁻¹ (가정 · 기상성장 탄소 섬유 문헌값 1.91 × 10⁻³ 인용) · DRT 봉우리 배정 (R_SE · R_int · R_ct,Li) | 접촉 단위 피복 · 접촉망 σ 없음 |
| **후보 D0** (지금 DEM) | 없음 — 이 논문은 DEM 을 쓰지 않는다 | — |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 개념 대조만 — 고체 벽에 **Navier 미끄럼 (200 nm) + 젖은 벽 접촉각** 을 둔 연속체 경계 (유체) | 고체 접촉 규칙 아님 |
| **후보 A · A′** (MPM 강체 AM · 입자별 속도장) | 없음 | — |
| **후보 B** (입자별 FE + 접촉) | 없음 — FE 는 한 상 연속체 (입자 · 접촉 없음) | — |
| **후보 C · C′** (큰 변형 · 탄소성 접촉 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀) | 없음 (Coble 크리프는 Li 의 균질 크리프 법칙 · SE 압밀 아님) | — |
| **U0–U6** | **U1** (해상도) 쪽 수치 — phase-field 계면 두께 20 nm 를 기공 50 · 200 nm 에 (기공 100 nm 사례에서 10 nm 로 줄임) = 계면 두께 ÷ 기공 ≤ 0.4 · FE 요소 1.5 × 2 µm (수렴 시험 없음) | U2–U6 없음 |
| **R1–R7** | **R4** (탈압 · 되돌아옴) — 섬유 망 · 셀 스택 (위 단계 6) · **R2** (미끄럼 · 분리) — FE 는 *"interfacial separation"* 을 넣지 않았다고 스스로 적음 · phase-field 의 "계면 열림" 은 해석 문장뿐 · **R7** (AM 파괴) — 없음 (SE · Li 계면 박리 SEM 만) | R1 · R3 · R5 · R6 없음 |
| **결과 전 대조 항목** | ① 스택 20 MPa · Ø 13 mm 몰드에서 **ΔP ≈0.1 MPa per µm 치밀 Li** (= 0.48–0.51 MPa per mAh cm⁻²) — 이 틀의 순응 · 스택 압력 모델이 생기면 견줄 값 ② 탄소 섬유 망 (기공 ≈70 % · SBR 1/3) **5 MPa 에서 ≈5.6 % · 할선 ≈90 MPa** [판독 · 카드 산술] — 우리 VGCF 망 압축 (생기면) 과 견줄 자릿수 ③ phase-field 의 **SOC 58 % = 기공 다 참** (기공 부피 × 0.8) — 맞추는 데 쓰지 않음 | 순수 SE 랩 표준 (10–13 % · 1.64) 과 같은 표에 넣지 않는다 |

- **재료 · 차원 · 조건 차이**: 계 = 황화물 전고체지만 **음극 쪽** (Li 금속 · Ag–C · 기상성장 CNF) · SE 는 LPSCl (입경 · 공급처 미기재) · 양극 72 : 27 : 1 (탄소 1 wt%) · 45 °C · 몰드 Ø 13 mm 20 MPa / 파우치 1–2 MPa · 모델 2D.  우리 = 양극 (NCM + LPSCl · 300 MPa · 3D DEM / MPM) — **겹치는 것은 LPSCl 이름 · 스택 압력 개념 · 탄소 섬유라는 부류**뿐이다.

## 9. 적용 인사이트 (행동)
1. **스택 압력 단계의 경계 조건 결정 근거 (흐름 밖 → 언로딩 키트 · 단계 6)**: 실전 셀은 볼트 틀 (간극 고정에 가까움) 이고 압력이 출력이다 — 우리 언로딩 · 스택 계산에서 "고정 압력 / 고정 간극" 을 등록할 때 이 논문 (20 MPa · ΔP 1–2.4 MPa) 과 `zhang2026_anode_free_asslsb_li2s_pi3_na_current_collector` (0–4 MPa · ΔP/P 11–13 %) 를 실측 사례로 함께 적는다.
2. **효과 매개변수 보고 꼴 (단계 0 · 보고서)**: 측정되지 않은 손잡이 (그들 β · 우리 E_eff 18 배 연화 · MPM σ_y) 는 *"값 하나 + 범위 스윕 + 결론이 범위 전체에서 같은지"* 로 보고한다 — 이 논문 S6 (β 0–0.005 에서 Q 증가 → 응력 증가가 유지) 이 그 꼴.
3. **같은 전류 대조로 엉킨 원인 가르기 (설계 규칙)**: 적재를 올리면 전류도 같이 오르는 교란을 0.98 mA cm⁻² 고정으로 갈랐다 — 우리 "노브 하나만" 원칙의 실험판 예.  우리 비교 (조성 · 입경 · 압력) 에서 같이 움직이는 둘째 변수를 등록 때 적는다.
4. **E 22.1 GPa 인용 주의**: 이 논문의 표 S1 을 근거로 "Pustorino 2025 = 22.1 GPa" 라고 쓰지 않는다 (정본 카드 = 48H 29.0) — 22.1 은 우리 DFT (22.06) · `[Deng16]` · Bazzoun DEM 입력과 같은 숫자라 출처가 섞이기 쉽다.
5. **탄소 섬유 망 압축 (흐름 밖 · VGCF)**: 우리 VGCF 를 넣은 건식 양극의 섬유 망 순응을 다룰 때 *"섬유 단일 E (100 GPa) ↔ 망 할선 (≈90 MPa · 기공 70 % · 결합제 1/3)"* 의 3 자릿수 차이를 먼저 적는다 (`lawrence2008_…` = 같은 Pyrograf III 계열 단섬유 6–207 GPa).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In NCM811‖Li₆PS₅Cl‖Li cells held at a 20 MPa stack pressure (13 mm mold, 45 °C, 0.2C), the load-cell pressure fluctuation increased from 1.1 to 1.8 to 2.4 MPa as the cathode areal capacity increased from 2.3 to 3.5 to 4.9 mAh cm⁻², and only the 4.9 mAh cm⁻² cell short-circuited (~128th cycle) (Kang et al., *Adv. Energy Mater.* 2026, e71816)."
- "Adding an 18.5–20 µm porous carbon-nanofiber layer (≈71 % porosity) beneath a dense Ag–C interlayer lowered the pressure fluctuation from 2.3 to 1.6 MPa (Kang et al., 2026)."
- 국문 (한정어와 함께): *"20 MPa 스택 몰드 셀에서 반대쪽 Li 석출 부피가 스택 압력을 흔드는 크기는 치밀 Li 1 µm 당 ≈0.1 MPa 였다 (Kang 2026 · 하중 셀 상대 ΔP · 이 틀 한정 · 양극 수축 섞임) — 그 논문의 FE 응력은 측정되지 않은 전달 인자 β 에 비례하는 상대값이다."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**: FE 는 Li 크리프 · 계면 분리 · 파괴를 넣지 않은 비교 틀 (p.4) · β 는 측정 물성이 아님 (p.4) · 전류와 기계 몫을 적재만으로는 못 가름 (p.3) · CNF Li 저장량은 추정이지 측정이 아님 (p.13) · 20 MPa 는 몰드 셀의 선택 조건 (p.10) · 석출 밀도 인자는 측정 어려움 (p.12–13).
**카드가 본 한계**
1. **ΔP 는 상대값 · 틀 의존** — 절대 압력 · 틀 강성 · 온도 보정 없음 · 양극 수축과 음극 팽창이 섞인 합.
2. **FE 응력의 크기는 β 에 비례** — 본문 · S6 의 95 백분위가 다르고 첨두 σ_yy 의 Q 의존이 선형 모델로 재현되지 않는다 (§3-3) · 옆면 경계 · f(x) 미기재.
3. **phase-field 는 곧은 기공 · 고정 벽** — CNF 의 실제 팽창 (18.5 → 21.0 µm) 과 섬유 형상은 계산 밖 · 도구 · 격자 미기재 · σ_stack 미기재 (20 MPa 로 읽힘 [카드 해석]).
4. **n = 1** — 반복 셀 · 오차 막대 없음 (그림 1 · 4 · 7 · 8).
5. **풀 몰드 셀 수명 이득 = 단락 회피** — 단락 전 용량 · 유지율은 Ag–C 만 셀이 같거나 높다 [판독].
6. **E 22.1 GPa 출처 의심** (§3-7 ⑧).
7. **전이 한계**: 음극 축 · 2D 모델 · 몰드 / 파우치 압력 다름 — 우리 양극 압밀 값으로 옮길 숫자 없음.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| [47] | C. Lin, H. Ruan, and M. Wang, "Comprehensive Study of Li Deposition and Solid Electrolyte Cracking by Integrating Simulation and Experimental Data," Advanced Science 12 (2025): 2501434, https://doi.org/10.1002/advs.202501434 | ★ Li 를 크리프 점도 유체로 다루는 phase-field 의 인용처 [21, 47, 48] — 카드 없음 |
| [33] | M. Dixit, N. Muralidharan, A. Parejiya, et al., "Differences in the Interfacial Mechanical Properties of Thiophosphate and Argyrodite Solid Electrolytes and Their Composites," ACS Applied Materials & Interfaces 14 (2022): 44292–44302, https://doi.org/10.1021/acsami.2c10589 | ★ FE 경계 처방의 인용 [31–33] · argyrodite 계면 역학 물성 — 카드 없음 (정본 `dixit2022_isostatic_…` 은 다른 논문) |
| [31] | S. H. Park, K. G. Naik, Z. Li, et al., "Pressure Heterogeneity and Material Utilization in Thin-Film Solid-State Cathodes," ACS Energy Letters 11 (2026): 5086–5094, https://doi.org/10.1021/acsenergylett.6c01154 | ★ 불균일 경계 변위 FE 의 인용처 · 압력 불균일 — 카드 없음 |
| [59] | C. Fang, B. Lu, G. Pawar, et al., "Pressure-Tailored Lithium Deposition And Dissolution In Lithium Metal Batteries," Nature Energy 6 (2021): 987–994, https://doi.org/10.1038/s41560-021-00917-3 | 석출 밀도 인자 0.6–0.9 의 인용처 · 스택 압력 ↔ Li 밀도 — 카드 없음 |
| SI [S3] | S. H. Park, K. G. Naik, B. S. Vishnugopi, P. P. Mukherjee, K. B. Hatzell, Adv. Energy Mater. 2025, 15, 2405129. | D_interlayer · D_host · κ_e 1000 S m⁻¹ 의 출처 (제목 미인쇄 = 서지 일부만) — 카드 없음 |
| SI [S1] | G. Pustorino, H. Jagad, W. Li, M. Feng, M. Poma, J. Ko, P. Johari, Y. Qi, Chem. Mater. 2025, 37, 313–321. | E 22.1 · ν 0.33 의 출처로 인용 — 정본 카드 있음 (`pustorino2025_…`) · 22.1 대조 필요 |
| [19] | Y. G. Lee, S. Fujiki, C. Jung, et al., "High-Energy Long-Cycling All-Solid-State Lithium Metal Batteries Enabled By Silver–Carbon Composite Anodes," Nature Energy 5 (2020): 299–308 | Ag–C 음극 원전 — 카드 없음 (I 축 배경) |
| [21] | Z. Wang, J. Xia, X. Ji, et al., "Lithium Anode Interlayer Design For All-Solid-State Lithium-Metal Batteries," Nature Energy 9 (2024): 251–262 | 크리프 수송 모델 인용 · 인터레이어 설계 — 카드 없음 |
| [5] · [9] · [11] · [2] · [17] · [22] · [50] · [51] · [54] | Kang 2023 ESM · Kang 2026 Chem. Commun. · Kang 2025 ACS AMI · Yun 2023 ESM · Lei 2026 EER · Kim 2021 AEM · Lee 2025 Nat. Commun. · Doux 2020 JMCA · Doux 2020 AEM | 정본 카드 있음 (`kim2023_chemomech_failure_highstrain_anode` · `kang2026_intertwined_…` · `kang2025_toughened_bimodal_nca_lzo` · `yun2023_deciphering_degradation_halide_vs_sulfide` · `lei2026_se_particle_size_effects_review` · `kim2021_review_oxide_sulfide_se_interfaces` · `lee2025_corolling_dryprocess_lpscl_ptfe` · `doux2020_pressure_effects_sulfide_se_jmca` · `doux2020_stack_pressure_assb`) |

## 13. [미확인] 목록 (본문 18 쪽 + SI 42 쪽 전수에 없음)
1. 하중 셀 틀의 강성 · 예압 절차 · 온도 (45 °C) 보정 · ΔP 의 절대 기준 · 휴지 이완.
2. FE 도구 · 옆면 · 아래 접선 경계 · f(x) 의 가우스 폭 · 위치 · 95 백분위의 영역 정의 · 수렴 시험.
3. phase-field 도구 · 격자 · 시간 간격 · 초기 조건 · σ_stack 값 (20 MPa 로 읽힘) · 혼합 자유에너지 꼴 f_mix · λ_pf 값.
4. CNF 섬유 지름 · 길이 · 단섬유 · 층 전도도 실측.
5. LPSCl 공급처 · 입경 · 분리막 성형압 · 두께 · NCM 공급처 · 적재 (mg cm⁻²) · 파우치 적재 · 파우치 전류 밀도.
6. 단면 SEM 이 압력을 뺀 뒤인지 (FIB 시편) — 두께 값 (16.3 · 21.0 · 18.7 µm) 의 측정 상태.
7. 반복 셀 수 · 오차.
8. E 22.1 GPa 의 원 출처 (Ref. S1 표기 ↔ 정본 Pustorino 카드).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-16)
- 본문 18 쪽 + SI 42 쪽을 글자 층 추출로 전부 읽음 · 그림 쪽은 도구 크롭 (본문 8 장 원 크기) + 패널 · SI · 표 · 식 · 글 조각 모음 그림으로 봄.  서지 = 본문 첫 쪽 (제목 · 저자 9 명 · 소속 8 · 교신 3 · 받음 · 고침 · 승인 · 키워드 · CC BY-NC · DOI) · 쪽 꼬리 "Advanced Energy Materials, 2026; 0:e71816" · PDF 메타 "Advanced Energy Materials 0.0:e71816" · SI 첫 쪽 = 같은 제목 (문장체) · 저자.  원문 낱말 셈: DEM · discrete = 0 · "linear-elastic" 1 (p.14) · "creep" 다수 · "unload" = 0.
- 그림 크롭 **150 장** = 도구 44 (본문 그림 1–8 그대로 · **SI 그림 S1–S32 전부 다시 자름** — 쪽 머리 로고 (35.4–68.0 pt) 가 도구 크롭 안에 → 래스터 ±4 pt · y ≥ 68.6 pt · **SI 표 S1–S4 다시 자름** — S1 · S4 아래 테두리 줄 잘림 · S2 식 분모 잘림 · S3 왼쪽 · 오른쪽 열 글자 잘림) + 손 크롭 106 (본문 패널 42 · SI 패널 12 · 식 32 · 근거 문단 20) · 본 뒤 다시 자른 손 크롭 1 (`fig_S24_interlayer_D` — 열 제목 끝 글자 잘림 → 1286 px 까지).  다시 자른 수 **37** (도구 36 + 손 1).  모음 그림 = 세션 scratchpad `litcards/<slug>_sheet_1–4.png`.
- 판독: digitized.csv 55 행 — 각 판독의 축 보정 · 판별 방법을 note 열에.  S3 · S16 · 4e 막대 윗변은 "25 행 연속 채움" 규칙 (처음 느슨한 규칙은 4e 에서 0.1 mAh cm⁻² 높게 읽혀 버림 · 화면 대조로 확인).
- 카드 산술 재현: Coble B · μ (S24) · 모세관 (S25) · SOC 58 % · 크리프 고원 0.437 ↔ 0.44 [판독] · CNF 기공률 (표 S2) · Fig. 8d 1.72 / 2.53 · 35.1 µm · Ag–C 0.61 — §3-4 · §3-5.
- 2 차 인용 대조: 이 논문을 인용한 정본 카드 0 건 · 이 논문이 인용한 Pustorino 2025 (E 22.1) ↔ 정본 카드 표 3 불일치 (§3-7 ⑧).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 + DOI (`aenm.71816`) · 제목 낱말 (Stress-Regulated · Carbon Nanofiber Anode) · 저자 (Junhee Kang) grep — 같은 논문 카드 없음 · 같은 1 저자 같은 해 = `kang2026_intertwined_…` (리뷰 · 다른 논문) (2026-11-16).

## 🔗 관련 카드
- 같은 1 저자 · 같은 해 (다른 논문): [`kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review`](kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review.md) — 이 논문 ref [9] · 리뷰의 Li–In 셀 압력 요동 ≈3.8 MPa vs LTO ≈0.2 MPa (같은 랩 ref 120).
- 같은 랩 · 같은 장치 · 같은 조건: [`ahn2026_cej_agno3_pvp_li3n_anodefree`](ahn2026_cej_agno3_pvp_li3n_anodefree.md) (Ø 13 mm PEEK · 0.15 g LPSCl · 하중 셀 0.01 MPa · 20 MPa · 45 °C · 2.5–4.25 V — 그 카드의 ΔP 3.0 / 2.8 / 2.5 MPa 는 NCA 양극 · 다른 인터레이어) · [`kang2026_site_specific_customized_se_dendrite_tolerant_li_metal`](kang2026_site_specific_customized_se_dendrite_tolerant_li_metal.md) (같은 1 저자 · Tae Young Lee 공저 · Ø 10 mm · 20 MPa) · [`kim2023_chemomech_failure_highstrain_anode`](kim2023_chemomech_failure_highstrain_anode.md) (이 논문 ref [5] · 고변형 음극 → 양극 열화 · 그 카드 H1 = Kang & Shin).
- 탄소 인터레이어 · Ag–C: [`liao2025_interfacial_adhesion_li_plating_carbon_interlayer`](liao2025_interfacial_adhesion_li_plating_carbon_interlayer.md) (적층압 100–400 MPa ↔ 박리 인성 · Li 석출 위치 — 이 논문의 "450 MPa 치밀 Ag–C · CNF 만은 계면에 Li" 와 같은 구도) · [`spencerjolly2023_ag_graphite_interlayer_operando_xrd`](spencerjolly2023_ag_graphite_interlayer_operando_xrd.md) (Li–Ag 상 LiAg · Li₉Ag₄ — 이 논문 SOC 10 % XRD 와 같은 상).
- 탄소 섬유: [`lawrence2008_single_vgcnf_elastic_modulus_morphology`](lawrence2008_single_vgcnf_elastic_modulus_morphology.md) (같은 Pyrograf III 계열 단섬유 E 6–207 GPa ↔ 이 논문 망 할선 ≈90 MPa) · ⚠ [`kim2026_charge_engineered_cnf_binder`](kim2026_charge_engineered_cnf_binder.md) 의 CNF = **셀룰로오스 나노피브릴** (이름만 같다).
- SE 탄성 입력 · 출처: [`pustorino2025_lpscl_bulk_surface_mechanical_electronic_li_filament`](pustorino2025_lpscl_bulk_surface_mechanical_electronic_li_filament.md) (Ref. S1 · 표 3 에 22.1 없음) · [`jeong2024_operando_densification_chemomechanics_se_size_composite_cathode`](jeong2024_operando_densification_chemomechanics_se_size_composite_cathode.md) (같은 부류의 SE 선형 탄성 입력 E 22 · ν 0.27 ↔ 이 논문 22.1 · 0.33 · FE 경계 처방 인용 [31] · SI [S3] 가 같은 Hatzell–Mukherjee 계열).
- 저압 운전 실측: [`zhang2026_anode_free_asslsb_li2s_pi3_na_current_collector`](zhang2026_anode_free_asslsb_li2s_pi3_na_current_collector.md) (0 / 1 / 4 MPa 하중 셀 · 정간극 틀 · ΔP/P 11–13 %) · [`doux2020_stack_pressure_assb`](doux2020_stack_pressure_assb.md) (이 논문 ref [54]).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

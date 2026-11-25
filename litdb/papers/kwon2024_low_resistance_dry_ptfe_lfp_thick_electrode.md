<!-- 표준 양식 확장 (paper-level STANDALONE — 이 카드만 읽어도 논문을 읽은 것과 같게). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     본 카드 = kollenda2024_time_sensitivity_calendered_electrode_springback_storage.md (절 번호 체계 · 머리 상자 · 서지 표 · 그림 표 꼴) ·
     형식 이웃 = lee2025_pvp_ptfe_binary_binder_dry_thick_graphite_anode.md · han2024_fec_mitigates_ptfe_decomposition_dry_thick_graphite_anode.md (같은 랩 · 같은 '세 단계' 건식 공정 서술 · 같은 SAICAS · 같은 1.15 M LiPF₆ 계열 전해질 — 이 논문은 그 묶음의 **양극 (LFP)** 판).
     쪽 표기 = 학술지 인쇄 쪽 = PDF 쪽 ("2300302 (n of 10)" · p.1–10) · SI = 받은 보충 PDF 17 쪽 ("SI p.N" — p.1 저자 · p.2–14 그림 S1–S12 · 표 S1 (p.4 · 이미지) · 식 (1) (p.5) · 표 S2 (p.15) · 표 S3 (p.16) · p.17 SI 참고 [1]–[10]).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 — 본문 그림은 래스터 한 장씩 (원 해상도 ≈300 dpi) 이라 그 화소에서,
     SI 그림은 래스터에 soft mask 가 붙어 있어 300 dpi 쪽 렌더에서 읽었다 (축 틀 직선 · 눈금으로 화소를 선형 대응 · 계열 색 마스크 (파랑 · 보라 = 습식 · 주황 · 빨강 = 건식) ·
     재현 = litdb/figures/<slug>/digitized.csv 225 행 · 행마다 방법 칸) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 추론] = 이 카드의 해석 ·
     [미확인] = 원문 (본문 10 쪽 + SI 17 쪽 전수) 에 없음.  본문은 텍스트 층 (PyMuPDF) 과 렌더 이미지로 다 읽었다 (텍스트 층이 지수의 '−' 를 잃는 곳은 렌더로 확인) · SI 표 S1 은 이미지라 렌더로 읽었다. -->
# PTFE 섬유화 건식 공정 LFP 후막 양극 (LFP : Super P : PTFE = 97 : 1 : 2 · 행성 혼합기 + 막자 · 60 °C 압착 · 라미네이트 · 2.3 g/cc) ↔ 같은 조성 습식 PVDF (2.1 g/cc) — 5.5 mAh/cm² 에서 대칭 셀 R_ion 35.01 → 6.19 Ω · N_M ≈22.3 → ≈4.3 · τ (= ε·N_M = 우리 tau2) ≈8.8 → ≈1.7 [판독] · CV 봉우리 간격 0.83 → 0.61 V (차 0.22 V = 카드 산술 · 원문에 '0.22' 인쇄 없음) · 7.8 mAh/cm² 흑연 전셀 300 사이클 (≈7.84 → ≈4.80 mAh/cm² [판독] · 유지율 숫자 미인쇄) — 본문 1C 유지율 '습식 89 · 건식 80 %' 는 그림 4d 와 순서 반대 · 액체 LIB · 압력 · 압연 조건 없음 — Kwon · Kim · Han · Lee · Lee · Kwon · Lee · Seo · Kim\* · Song\* · Choi\* (Small Sci. 4, 2024)

> slug `kwon2024_low_resistance_dry_ptfe_lfp_thick_electrode` · DOI `10.1002/smsc.202300302` · type `experiment (dry process 건식 전극 · PTFE binder 섬유화 · LFP 후막 양극 · slurry 습식 PVDF 대조 · 액체 전해질 LIB 반쪽 · 흑연 전셀 · impedance (대칭 셀 R_ion · R_ct) · MacMullin · tortuosity (그림 막대) · Hg porosity · SAICAS adhesive · BET powder · morphology SEM/TEM · XPS · XRD · GITT · CV — DEM · MPM · 모델 없음 · 압력 없음)` · PDF `6abf5bb7-93._Low_Resistance_LiFePO4_Thick_Film_Electrode_Processed_with_Dry_Electrode_Technology_for_High_Energy_Density_Lithium_Ion_Batteries.pdf` · digested `2026-11-22` · status ✅
> **[팔로우 랩: 가천대 최준현 교수 (건식 전극)]** — 태그 문구는 같은 태그를 단 이웃 카드 (`lee2025_pvp_*` · `kim2026_*` · `kang2026_*` · `lee2026_li_*`) 와 같게 둔다 (한글 이름 한정 = 아래 '팔로우 랩 표지 근거')
>
> **저자 (p.1 · SI p.1, 인쇄 순서 그대로)**: Kihwan Kwon (a, b, ‡) · Jiwoon Kim (c, ‡) · Seungmin Han (a, c) · Joohyun Lee (a, d) · Hyungjun Lee (c) · Jiseok Kwon (c) · Jungwoo Lee (d) · Jihoon Seo (e) · **Patrick Joohyun Kim\*** (b) · **Taeseup Song\*** (c) · **Junghyun Choi\*** (a, f) — **11 명** (‡ = 동등 기여 · 본문 *"K.K. and J.K. contributed equally"* · \* 교신 셋) · a 한국세라믹기술원 (KICET) Energy Storage Materials Center, Jinju · b 경북대 응용화학과 · c 한양대 에너지공학과 · d 부산대 재료공학과 · e Clarkson University 화공 · 생명공학과 (Potsdam, NY) · f 가천대 배터리공학과 · 교신 전자우편 jchoi@kicet.re.kr (p.1) · junghchoi@gachon.ac.kr (SI p.1) · pjkim@knu.ac.kr · tssong@hanyang.ac.kr [인쇄 p.1 · SI p.1].
> **팔로우 랩 표지 근거**: 인쇄 로마자 **"Junghyun Choi"** — 소속 KICET + 가천대 배터리공학과 · **교신저자** (p.1 · SI p.1).  한글 이름은 PDF 어디에도 인쇄되지 않았다 (다른 팔로우 랩 카드와 같은 한정 — 같은 분인지는 인쇄 로마자 · 소속 · 교신까지만 확인) · 연구비 번호는 `kim2026_*` (NRF RS-2024-00408156 · RS-2024-00449682) 와 **다르고** `han2024_fec_*` 와 **같다** (산업부 20024261 · 그 카드 L13) · SI p.1 전자우편 junghchoi@gachon.ac.kr 은 `kim2026_*` L21 의 J. Choi 전자우편과 같은 글자다.
> *Small Science* **4** (5) (2024) **2300302** (10 쪽) · 접수 2023-11-21 · 수정 2024-01-21 · 온라인 2024-02-09 · © 2024 저자 · Wiley-VCH · **오픈 액세스 CC BY** · 연구비 산업통상자원부 산업기술혁신사업 **20024261** (*"Development of thick film electrode and cell manufacturing technology for high-performance lithium iron phosphate battery with energy density of over 200 Wh kg⁻¹"*) · 이해상충 없음 · 데이터 = *"available from the corresponding author upon reasonable request"* · 키워드 dry process · lithium ion batteries · lithium iron phosphate · polytetrafluoroethylene [인쇄 p.1 · p.9 · 호 (5) = 쪽 꼬리글 '26884046, 2024, 5'].
> **보충 PDF**: `46d65a9a-93._Sup_Low_Resistance_LiFePO4_Thick_Film_Electrode_Processed_with_Dry_Electrode_Technology_for_High_Energy_Density_Lithium_Ion_Batteries.pdf` (17 쪽 · Word 원고를 PDF 로 바꾼 사본 · 문서 정보 작성자 '권기환' — 그림 S1–S12 · 표 S1 (이미지) · S2 · S3 · 식 (1) · SI 참고 [1]–[10]).
> **이웃 카드 (링크만)**: [`kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode`](kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode.md) (이 논문을 참고 [40] 으로 인용 · 'ΔV 0.22 V' 2 차 인용 — §0-1) · [`kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation`](kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation.md) (참고 [23] 으로 인용) · [`han2024_fec_mitigates_ptfe_decomposition_dry_thick_graphite_anode`](han2024_fec_mitigates_ptfe_decomposition_dry_thick_graphite_anode.md) (★ 같은 해 · 같은 랩 · 공저자 겹침 (K. Kwon · S. Han · P.J. Kim · T. Song · J. Choi) — 건식 **음극** 판 · 이 논문을 참고 [15] 로 인용) · [`lee2025_pvp_ptfe_binary_binder_dry_thick_graphite_anode`](lee2025_pvp_ptfe_binary_binder_dry_thick_graphite_anode.md) (참고 [35] 로 인용 — '건식 공정 세 단계' 서술) · [`morasch2018_binder_gradient_impedance_tortuosity`](morasch2018_binder_gradient_impedance_tortuosity.md) (이 논문의 참고 [43] · 바인더 구배 ↔ 차단 EIS τ).
> **판독 원자료**: `litdb/figures/kwon2024_low_resistance_dry_ptfe_lfp_thick_electrode/digitized.csv` (225 행 — 그림 2f · 4a · 4d · 5b · 5c · 5d · 6a · 6d · S1 · S2 · S3 · S6 · S7 · S9 · S12) · 크롭 75 장 (도구 20 = 본문 그림 2–8 · SI 그림 S1–S4 · S6–S12 · SI 표 S2 · S3 — **전부 다시 자름** (래스터 사각 / 벡터 상자 + 6 pt 를 비지 않은 내용 + 20 px 로 고르게 · S2 는 아래 괘선 · S3 은 오른쪽 절반이 잘리고 표 글자가 캡션에 섞였음) + 손 55 = 본문 그림 1 (도구가 놓침) · SI 그림 S5 (벡터 막대 · 도구가 '그래픽 없음' 으로 버림) · SI 표 S1 (이미지 · 캡션이 표 아래) · 패널 33 · **식 1** (SI 식 (1) · GITT D_Li) · 근거 문단 18) — `figures.json`.  **본문에는 번호 붙은 식이 없다** — 식 크롭은 SI 식 (1) 하나 (`eq_S1_gitt_diffusion_coefficient.png`).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 같은 LFP (LFP-NCO) · Super P · 바인더 **97 : 1 : 2 wt%** 를 (i) 습식 (PVDF Solef 5130 · NMP 슬러리 · 20 µm Al 에 테이프 캐스팅 · 100 °C 진공 건조 · **2.1 g/cc · 190 µm**) 과 (ii) 건식 (PTFE F-104 · 행성 혼합기 ARE-310 + 막자 → 60 °C 에서 눌러 20 µm Al 에 라미네이트 · **2.3 g/cc · 175 µm**) 로 만들어 **5.5 mAh/cm² (35 mg/cm²)** Li 반쪽 셀 · 흑연 전셀 (N/P 1.1) 로 견주면, 건식이 대칭 셀 **R_ion 35.01 → 6.19 Ω** [인쇄 그림 5a] · Hg 기공 39.5 → **38.2 %** [인쇄] · **N_M ≈22.3 → ≈4.34 · τ ≈8.80 → ≈1.66** [판독 그림 5c — 막대만 · 숫자 미인쇄] · CV 봉우리 간격 **0.83 → 0.61 V** [인쇄 그림 4b 글자] · D_Li (GITT) **1.06 → 1.35 × 10⁻¹¹ cm²/s** [인쇄] · 사이클 뒤 R_ct ≈360 → ≈15 Ω [판독] 이고, **7.8 mAh/cm² · 2.3 g/cc 건식 LFP 후막**이 흑연 전셀로 300 사이클 돌았다 (같은 조건 습식은 균열로 못 만듦 · 그림 S11) — 저자 해석 = *"PTFE 섬유의 점 접촉 (spot contact) 이 LFP 표면을 덮지 않고 (BET 11.9 ≈ 11.6 m²/g ↔ PVDF 9.5) · 용매 증발이 없어 바인더가 고르게 남는다 (SAICAS 습식만 깊이 따라 ≈12 % ↓)"*.  ⚠ 그러나 **'ΔV 0.22 V' 라는 숫자는 원문 · SI 어디에도 인쇄되어 있지 않다** — 나오는 길은 CV 봉우리 간격의 **차 (0.83 − 0.61 = 0.22 V)** 하나뿐 [카드 산술] 이고 로딩을 늘린 습식 계열은 없다 (§0-1) · 본문 1C 유지율 *"wet- and dry- … 89% and 80%, respectively"* 는 그림 4d 판독 (습식 ≈80.0 · 건식 ≈89.4 %) 과 **순서가 반대** · 300 사이클 유지율 숫자 없음 (판독 ≈61 % — 첫 점 기준).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 무엇을 (조성 · 공정 · 전극) | LFP **LFP-NCO** (Advanced Lithium Electrochemistry) · Super P · 바인더 = **97 : 1 : 2 wt%** (두 공정 같음) · 습식 = PVDF Solef 5130 (Mw 1 100 000 g/mol) + NMP (DAEJUNG > 99.7 %) → 20 µm Al 테이프 캐스팅 → 100 °C 진공 하룻밤 · 건식 = PTFE **F-104 (DAIKIN)** · **행성 혼합기 ARE-310 (THINKY) + 막자** → *"pressed and laminated onto a 20 μm thick Al current collector at 60 °C"* · 캘린더로 **2.1 / 2.3 g/cc** · 두께 **190 / 175 µm** (Al 포함으로 읽힘 [카드 산술 §3-1]) · LFP 입경 · rpm · 시간 · 압착 하중 · 캘린더 하중 · 간극 · 통과 횟수 = 없음 | [인쇄] p.8–9 · [미확인] |
| ② 바인더 형태 · 분포 | 단면 SEM: 건식에 PTFE 섬유 (*"bridge-like connection"*) · Cs-TEM: 습식은 PVDF 가 LFP 표면을 덮음 · BET (N₂) **LFP 분말 11.6 · LFP/PTFE 혼합 분말 11.9 · LFP/PVDF 슬러리 분말 9.5 m²/g** · 기공 크기 봉우리 ≈2.6 (PTFE 혼합) · ≈4.4 (LFP) · ≈5.9 nm (PVDF) [판독] · SAICAS 깊이 30 µm 마다: 건식 거의 같음 · 습식 **≈12 % ↓** (위 → 가운데 · 바닥) | [인쇄] p.2–3 · 그림 2 · 3 · [판독] 그림 2f |
| ③ ★ 기공 쪽 이온 수송 (액체 전해질) | 대칭 파우치 셀 EIS **R_ion 35.01 (습식) → 6.19 Ω (건식)** (= −82.3 % [카드 산술] · 본문 '83 %') · **N_M 22.3 → 4.34 · τ 8.80 → 1.66** [판독] — 막대는 **τ = ε·N_M** 을 만족 (22.29 × 0.395 = 8.80 · 4.34 × 0.382 = 1.66 [카드 산술]) = **우리 tau2 (수송 tortuosity) 꼴** · 식은 미인쇄 (참고 [35] [36]) · Hg 기공 **39.5 → 38.2 %** (SI 39.46 · 38.23 %) · 기공 지름 봉우리 ≈0.079 → ≈0.052 µm [판독] · 분포 0.02–0.3 → 0.02–0.1 µm [인쇄] | [인쇄] 그림 5a · 5b · p.4–5 · SI 그림 S5 · [판독] 그림 5c |
| ④ 반쪽 셀 전기화학 (5.5 mAh/cm²) | 첫 사이클 정전류 ΔV **≈0.26 (습식) · ≈0.10 V (건식)** [판독 그림 4a · 평탄 중앙값] (본문은 '낮다' 만) · CV 봉우리 **3.87 / 3.04 V (습식) · 3.75 / 3.14 V (건식)** [인쇄 그림 글자] → 간격 0.83 / 0.61 V · *"26% lower"* · D_Li **1.06 / 1.35 × 10⁻¹¹ cm²/s** (+27.3 %) · 율속 0.05 → 1C **5.40 → 4.32 (습식) · 5.47 → 4.88 mAh/cm² (건식)** [판독] · 40 사이클 (1.08 mA/cm²) 유지 **85.9–91.4 % (습식 5 셀) · 96.5–98.2 % (건식 5 셀)** [인쇄 표 S1] · GITT IR 강하 ≈44–50 · ≈24–34 mV [판독 그림 S1] | [인쇄] p.3–4 · 그림 4 · 표 S1 · [판독] |
| ⑤ 계면 (사이클 전 · 뒤) | R_ct 사이클 전 두 전극 비슷 (반원 ≈945 Ω 에서 닫힘 [판독 그림 S6]) → 사이클 뒤 **≈360 (습식) · ≈15 Ω (건식)** [판독 그림 5d] · F 1s XPS 사이클 뒤 **LiF 56.5 % (습식) · 54.1 % (건식)** · 바인더 43.5 · 45.9 % [인쇄 그림 S7 글자] · PTFE · PVDF 미반응 (CF₂ · XRD 별표) · 사이클 뒤 **습식 LFP 입자만 균열** (그림 S10) | [인쇄] p.5–6 · 그림 5d · S6–S10 · [판독] |
| ⑥ ★ 건식 후막 · 전셀 | 흑연 (96 : 1 : 3 · N/P 1.1) 전셀 5.5 mAh/cm²: 1C 에서 습식 ≈0 · 건식 **4 mAh/cm²** (*"approximately 75%"* of 0.05C — 판독 ≈71 %) · **7.8 mAh/cm² · 2.3 g/cc · 2.4 mA/cm² 300 사이클** (첫 점 ≈7.84 → 299 번째 ≈4.80 mAh/cm² [판독] · 원문 유지율 숫자 없음 · *"excellent cycle stability"*) · 부하 **52 mg/cm²** (표 S3) · 부피 용량 **376.8 mAh/cm³** (표 S2 · 본문 'over 370') · 같은 부하 · 밀도 습식 = 균열 (그림 S11) · 습식은 > 2.2 g/cc · > 5 mAh/cm² 에서 박리 | [인쇄] p.4 · p.7 · 그림 6 · 8 · S11 · S12 · 표 S2 · S3 · [판독] |
| ⑦ 에너지 밀도 추정 (각형 셀) | 습식 최대 **153 Wh/kg · 390 Wh/L** (5 mAh/cm²) · 건식 **185 Wh/kg · 470 Wh/L** (7.8 mAh/cm² — **470 은 표 S3 의 '+ High Density LFP' 칸** · 초후막만이면 400 Wh/L) · CTP 적용 **213 Wh/kg · 705 Wh/L** (= 185 × 1.15 · 470 × 1.5 [카드 산술] · 참고 [44] 의 '+10–15 % · +50 %') · 계산 근거 = *"based upon the previous reports"* (식 · 셀 설계값 미인쇄) | [인쇄] p.7–8 · 표 S3 · [미확인] |
| ⑧ 저자 한계 (원문 'limitation' 절 없음) | 원문이 하지 않은 것: 압착 · 라미네이트 · 캘린더 조건 · LFP 입경 · 셀 수 · 오차 막대 (표 S1 만 5 + 5 셀) · 측정 온도 · 대칭 셀 전해질 · N_M · τ 식 · R_ct 숫자 · 300 사이클 유지율 · 에너지 밀도 계산식 | [미확인] |
| ⑨ 모델 | **없음** — DEM · 연속체 · 접촉 모델 0 · 본문 식 0 (SI 식 (1) = GITT D 식 하나) | §4-4 |

⛔ **한정어 (떼지 말 것)**: ① **액체 전해질 LIB 의 LFP 양극** — 고체전해질 없음 · 기공은 **액체가 찬 기공** (우리 ASSB 는 SE 상이 이온 길) ② **압력 숫자 없음** — 건식 압착 · 라미네이트 (60 °C) · 캘린더 하중 · 간극 · 통과 횟수 [미확인] → MPa 대응 불가 ③ 그림 4–6 의 비교는 **셀 하나씩** (표 S1 = 같은 조건 5 + 5 셀의 첫 · 40 번째 사이클 숫자뿐 · 오차 막대 0) ④ **N_M · τ · R_ct · 정전류 ΔV · 300 사이클 유지율은 판독값** (원문 숫자 없음) ⑤ 기전 (점 접촉 · PVDF 덮임 · 균일 CEI · b 축 확산) 은 **정성 영상 · 인용** — 측정이 기전을 가르지 않는다 (예: XPS LiF 몫 차는 56.5 ↔ 54.1 % = 2.4 %p) ⑥ 인쇄값끼리 어긋남 여럿 (§3-8 — 1C 유지율 순서 · CV 주사 속도 1 ↔ 0.1 mV/s · GITT 휴지 30 분 ↔ 그림 ≈10 분 · PTFE XPS 689.9 eV ↔ 그림 ≈687.5 eV · XRD 18° ↔ 별표 ≈17.0° · SI 식 (1) 의 m_B · M_B 정의 뒤바뀜).
⇒ **절대값 전이**: 하지 않는다 (액체 LIB · LFP · 압력 없음 · 기공 30–40 % 대).  **전이 가능한 것** = (i) **같은 조성 · 같은 활물질에서 바인더 형태 · 분포만으로 기공 쪽 tau2 가 ≈5.3 배** (8.80 ↔ 1.66 [판독]) 달라질 수 있다 — 수송 tortuosity 는 조성 · 기공률만의 함수가 아니다 (우리 모델의 바인더 · 첨가제 표현이 수송 결과를 바꿀 수 있다는 크기 감각) (ii) **섬유화 PTFE 는 AM 표면을 막처럼 덮지 않는다** (BET · TEM 정성) — 우리 STEP3 의 PTFE `centerline` 스탬프 (CL-60) 가 '막' 이 아니라 '선' 으로 그리는 것과 같은 방향 (iii) 측정 규약: 같은 이름 'ΔV' 가 CV 봉우리 간격 (0.61–0.83 V) 과 정전류 평탄 차 (0.10–0.26 V) 로 쓰인다 — 인용할 때 어느 양인지 붙인다.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-93 의 '왜' 칸)

의도 원문: *"건식 공정 — 건식 LFP 후막 (ΔV 0.22 V 비교의 출처)"* · 가리킨 카드 = `kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode` (L386 · 참고 [40] — 같은 카드 §3-6 **L170** 이 *"문헌 슬러리 로딩 증가 시 ΔV 최대 0.22 V, ref 40"* 이라 적음) · `kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation` (L414 · 참고 [23]).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "건식 공정" | **채움** | PTFE 섬유화 건식: *"The dry-processed LFP mixture was produced by mixing LFP, carbon black (Super P), and the PTFE binder (F-104, DAIKIN) using a planetary mixer (ARE-310, THINKY) and a pestle. The resultant mixture was then pressed and laminated onto a 20 μm thick Al current collector at 60 °C."* [인쇄 p.9] · 세 단계 서술 *"1) shear mixing … without solvent; 2) rolling and calendaring of the resulting mixture; and 3) laminating the electrode composites onto the current collector"* [인쇄 p.2 · 그림 1 모식] · 97 : 1 : 2 · 캘린더로 2.3 g/cc · rpm · 시간 · 막자 반죽 시간 · 압착 하중 · 캘린더 하중 · 간극 · 통과 횟수 [미확인] · 압력 (MPa) 없음 |
| "건식 LFP 후막" | **채움** | **7.8 mAh/cm² · 2.3 g/cc** 건식 LFP / 흑연 전셀 *"was successfully fabricated"* · *"excellent cycle stability over 300 cycles"* [인쇄 p.7 · 그림 6d · S12] · 부하 **52 mg/cm²** [인쇄 표 S3] · 기본 비교 전극 5.5 mAh/cm² (35 mg/cm²) · 175 µm [인쇄 p.3 · p.9] · 같은 부하 · 밀도의 습식 = 균열 (그림 S11 사진) · ⚠ 7.8 mAh/cm² 전극의 **두께는 인쇄 안 됨** (52 mg/cm² · 2.3 g/cc 면 코팅 ≈226 µm [카드 산술 · 가정] · 그림 7 모식 글자 '140µm ≥') |
| "ΔV 0.22 V 비교의 출처" | **일부** | **0.22 V 는 원문 · SI 어디에도 인쇄되어 있지 않다** (본문 · SI 텍스트 층 전수 검색 + 그림 안 글자 전수).  원문의 ΔV 비교 = **같은 5.5 mAh/cm² 에서 습식 ↔ 건식**: ⓐ CV 봉우리 간격 — 본문 *"which shows a 26% lower voltage hysteresis than the wet-processed one (0.83)"* [인쇄 p.3] · 그림 4b 글자 **습식 3.87 / 3.04 V (간격 0.83) · 건식 3.75 / 3.14 V (간격 0.61)** → 0.61 / 0.83 = 0.735 = '26 % lower' · **0.83 − 0.61 = 0.22 V** [카드 산술] ← 0.22 가 나오는 유일한 길 ⓑ 첫 사이클 정전류 곡선 (그림 4a · C-rate 미기재) 평탄 차 **≈0.26 (습식) · ≈0.10 V (건식)** [판독 · 1–4 mAh/cm² 중앙값 · 1 화소 = 2.4 mV] — 본문은 숫자 없이 *"low-voltage hysteresis (ΔV)"* 만.  ⚠ **로딩을 늘린 습식 계열은 없다** (습식은 5.5 mAh/cm² 한 부하 · > 5 mAh/cm² · > 2.2 g/cc 는 박리로 못 만듦 p.4) · ⚠ CV 주사 속도 본문 · 캡션 **1 mV/s** ↔ 방법 **0.1 mV/s** (p.9) |
| (가리킨 카드 · 2 차 인용) `kang2026_*` **L170** *"(p.8; 문헌 슬러리 로딩 증가 시 ΔV 최대 0.22 V, ref 40)"* | **원문과 다름** | 이 원문 (= Kang 의 ref 40) 에는 ⓐ '슬러리 로딩 증가' 계열이 없고 ⓑ 0.22 V 라는 인쇄값이 없다 — 0.22 V 는 **같은 부하에서 습식 CV 간격 0.83 V 와 건식 0.61 V 의 차** [카드 산술] 로만 재현된다 · 그 카드가 같은 줄에서 견준 Kang 의 판독 ΔV ≈0.14 V 는 **정전류 충 · 방전 평탄 차** 라서 CV 봉우리 간격 (0.61–0.83 V) 과는 다른 양이다 [카드 추론].  ⚠ 그 줄이 Kang 원문 p.8 문장을 옮긴 것인지 카드가 풀어 쓴 것인지는 **Kang 원문 확인 전 [미확인]** — 어느 쪽이든 'Kwon 2024 가 슬러리 로딩 증가로 ΔV 0.22 V' 로 인용하면 안 된다 |
| (가리킨 카드 · 서지) `kang2026_*` L386 *"Kwon, K. et al. Low‐resistance LiFePO4 thick film electrode processed with dry electrode technology for high‐energy‐density lithium‐ion batteries. Small Sci. 4, 2300302 (2024)."* | **원문과 같음** | p.1 제목 · 학술지 · 권 · 논문 번호 · 연도 일치 · 그 줄의 *"`kim2026_…` §12 ref 23 의 전체 저자 목록에 J. Choi 인쇄"* 도 맞음 (11 번째 저자 Junghyun Choi · 교신) |
| (가리킨 카드 · 서지) `kim2026_*` L414 저자 11 명 · 제목 · *"Small Sci. 4 (5) (2024) 2300302"* | **원문과 같음** | 머리글자 · 순서 모두 원문 p.1 과 일치 · 호 (5) = 쪽 꼬리글 *"26884046, 2024, 5"* · 그 카드 L405 표 머리 *"'J. Choi' 가 Junghyun Choi 인지는 머리글자만이라 [미확인]"* 은 이 논문 (그 표의 ref 23) 에 대해서는 원문으로 풀린다 (인쇄 'Junghyun Choi' · KICET + 가천대 · 교신 · SI 전자우편 junghchoi@gachon.ac.kr) |
| (후보 표 메모) '서지 상태: 온전' · 'litdb 확인: 카드 없음 (인용만)' | **맞음** | papers/ 목록 · DOI `smsc.202300302` · '2300302' · 'Low-resistance LiFePO4' grep = `kang2026_*` · `kim2026_*` 에 더해 `han2024_fec_*` (L343) · `lee2025_pvp_*` (L348) 의 **인용 줄뿐** (이 카드가 첫 카드) |

**2 차 인용 대조 (카드 문제 — 고치지 않음)**:
- `kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode` **L170**: *"nominal capacity plateau near 3.43 V and low hysteresis ΔV"* (p.8; **문헌 슬러리 로딩 증가 시 ΔV 최대 0.22 V, ref 40**) — 원문 (Kwon 2024) 에는 로딩 증가 계열도 0.22 V 인쇄값도 없다 · 0.22 V = 습식 · 건식 CV 봉우리 간격의 차 (0.83 − 0.61) [카드 산술] · 같은 줄이 나란히 둔 Kang 의 ΔV ≈0.14 V (정전류) 와 다른 양.
- `kang2026_*` **L386** (§12 표 · '왜 · 카드' 칸) *"건식 LFP 후막 (ΔV 0.22 V 비교의 출처 …)"* — '출처' 라는 말은 맞을 수 있으나 (0.22 V 는 이 논문의 CV 숫자로만 만들어진다) 비교의 내용 (로딩 증가) 은 원문과 다르다.
- 참고 (문제 아님): `han2024_fec_*` L343 이 이 논문을 *"전셀 양극 공정 (§11-15) 을 채울 후보"* 로 적었는데, Han 2024 전셀 LFP 는 **94 : 3 : 3** (그 카드 §3) · 이 논문은 **97 : 1 : 2** — 같은 공급사 (LFP-NCO) · 같은 랩이지만 조성이 달라 그 공정을 그대로 채우지는 않는다 [카드 추론].

⇒ **의도 대조 결과: 일부** — '건식 공정' · '건식 LFP 후막 (7.8 mAh/cm² · 2.3 g/cc · 300 사이클)' 은 채움; **'ΔV 0.22 V' 는 원문에 인쇄된 값이 아니고 같은 부하의 습식 ↔ 건식 CV 봉우리 간격 (0.83 ↔ 0.61 V) 의 차로만 나오며, kang2026 카드의 '슬러리 로딩 증가 시' 계열은 원문에 없다.**

---

## 1. 한 줄 요약
LFP 는 값싸고 안정하지만 전자전도도 (10⁻⁶–10⁻¹⁰ S/cm) · Li 확산이 낮고 전압 (3.2 V) · 이론 용량 (≈170 mAh/g) 이 낮아, 에너지 밀도를 올리려면 **후막** (높은 부하) 이 필요한데 습식 슬러리 후막은 건조 중 균열 · 바인더 · 도전재 이동이 문제다 — 저자들은 **PTFE 섬유화 건식 공정**으로 LFP 후막을 처음 만들었다고 주장하고 (p.1 · p.2), 같은 97 : 1 : 2 조성의 습식 (PVDF) 전극과 5.5 mAh/cm² 에서 견준다: 건식은 SAICAS 깊이별 접착이 고르고 (습식 ≈12 % ↓), BET 비표면적이 LFP 분말과 같으며 (점 접촉), 대칭 셀 R_ion 이 83 % 낮고 (35.01 → 6.19 Ω), N_M · τ 가 작고, CV 간격 · D_Li · 율속 · 40 사이클 · 사이클 뒤 R_ct · LiF 몫이 모두 건식 쪽이 좋다 — 그 결과 **7.8 mAh/cm² · 2.3 g/cc 건식 LFP / 흑연 전셀이 300 사이클** 돌았고 (습식은 같은 조건에서 균열), 각형 셀 추정 에너지 밀도는 185 Wh/kg · 470 Wh/L (CTP 면 213 · 705) 로 NMC 계와 견줄 만하다고 맺는다.

## 2. 메타
| 저자 | 저널 / 년 | DOI | 소재 | 연구 유형 |
|---|---|---|---|---|
| K. Kwon‡ · J. Kim‡ · S. Han · J. Lee · H. Lee · J. Kwon · J. Lee · J. Seo · P.J. Kim\* · T. Song\* · J. Choi\* (KICET · 경북대 · 한양대 · 부산대 · Clarkson · 가천대) | Small Sci. 4 (5) (2024) 2300302 · 10 쪽 · CC BY · SI 17 쪽 | 10.1002/smsc.202300302 | **액체 전해질 LIB LFP 양극** — LFP-NCO + Super P + PVDF (습식) / PTFE F-104 (건식) · 1.15 M LiPF₆ EC : EMC : DMC 2 : 4 : 4 + LiPO₂F₂ 1 wt% + VC 1 wt% · 상대 = Li 금속 / 흑연 (96 : 1 : 3) · **고체전해질 없음** | 실험 (제조 + 분석 + 전기화학) — **모델 · 시뮬레이션 없음** |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 · 조성 · 제조 (p.8–9 §4 · 그림 1)
| 항목 | 습식 | 건식 | 표지 · 쪽 |
|---|---|---|---|
| 활물질 | **LFP-NCO** (Advanced Lithium Electrochemistry Co. Ltd.) — 입경 · 분포 · 탄소 코팅 여부 [미확인] · TEM 상 수십–수백 nm 1 차 입자 (정성 · 그림 2b · 2d 눈금 200 nm) | 같음 | [인쇄] p.8 · [미확인] |
| 도전재 | Super P | Super P | [인쇄] |
| 바인더 · 용매 | **PVDF Solef 5130** (Mw 1 100 000 g/mol) · NMP (DAEJUNG > 99.7 %) | **PTFE F-104 (DAIKIN)** · 용매 없음 | [인쇄] p.8–9 |
| 조성 (wt%) | **97 : 1 : 2** | **97 : 1 : 2** | [인쇄] p.9 |
| 성형 | 슬러리 → 20 µm Al 테이프 캐스팅 → 100 °C 진공 하룻밤 | 행성 혼합기 ARE-310 + **막자** → *"pressed and laminated onto a 20 μm thick Al current collector at 60 °C"* | [인쇄] p.9 |
| 캘린더 | *"Through the calendaring process to increase the electrode density and tailor the microstructure"* → **2.1 g/cc** | → **2.3 g/cc** | [인쇄] p.9 · 하중 · 간극 · 온도 · 횟수 [미확인] |
| 두께 | **190 µm** | **175 µm** | [인쇄] p.9 |
| 표 S1 실측 (셀 5 개씩) | 부하 33.23–34.69 mg/cm² (평균 33.79) · 밀도 2.08–2.15 g/cc (평균 2.102) | 32.86–33.6 mg/cm² (평균 33.27) · 2.29–2.32 g/cc (평균 2.304) | [인쇄] SI 표 S1 · 평균 = [카드 산술] |

- [카드 산술] **두께는 Al 박을 포함한 값으로 읽힌다**: 35 mg/cm² ÷ 2.3 g/cm³ = 152.2 µm (+ Al 20 = 172.2 ≈ 인쇄 175) · 35 ÷ 2.1 = 166.7 µm (+ 20 = 186.7 ≈ 인쇄 190) — 단면 코팅 가정.
- 공정 세 단계 (서론 · 그림 1 모식 *Mixing → Fibrillation → Calendering and lamination*): *"1) shear mixing electroactive particles, conductive additives, and the PTFE binder without solvent; 2) rolling and calendaring of the resulting mixture; and 3) laminating the electrode composites onto the current collector"* [인쇄 p.2 · 참고 [18]] — ⚠ 실제 방법 절은 '막자' 와 '60 °C 압착 · 라미네이트' 만 적고 **섬유화 (반죽) 단계의 조건** 은 적지 않는다.
- 비용 동기: NMP 증발 · 회수가 *"approximately 78% of the overall electrode production cost"* [인쇄 p.2 · 참고 [16] [17]].

### 3-2. 셀 · 측정 조건 (p.9 §4)
- **CR2032** (Wellcos) · 건조실 이슬점 **−50 °C 아래** · 분리막 Celgard 3501 (PP) · 전해질 **1.15 M LiPF₆ in EC : EMC : DMC = 2 : 4 : 4 (v/v/v) + LiPO₂F₂ 1 wt% + VC 1 wt%** · 상대 전극 Li 금속 박 "1.0 T" (인쇄 그대로) · 양극 **5.5 mAh/cm² (35 mg/cm²)** · 충방전기 WBCS3000L32 (WonATech) · CC–CV [인쇄 p.9].
- 형성: 0.05 C · 0.1 C 두 번 (**1 C = 5.5 mAh/cm²**) · 율속: 0.1 C 충전 뒤 방전 0.1 · 0.2 · 0.3 · 0.5 · 1 C (0.05 C 충방전 제외) [인쇄].
- **CV**: *"constant scan rate of 0.1 mV s⁻¹"* · 2.8–4.0 V (VSP, Biologic) [인쇄 p.9] ⚠ 본문 p.3 · 그림 4 캡션은 **1 mV s⁻¹**.
- **EIS**: *"frequency range from 250 kHZ to 10 MHz"* · 5 mV (인쇄 그대로 — 10 MHz 는 10 mHz 의 오기로 보이나 [카드 추론] · 확정 [미확인]).
- **GITT**: *"pulse current of 0.1 mA cm⁻² for a duration of 10 min, followed by pause times of 30 min"* · 2.0–4.2 V [인쇄] ⚠ 그림 S3 판독 = 펄스 ≈597 s · 휴지 ≈604 s (≈10 분) · 전 구간 시간과도 안 맞음 (§3-8).
- **전셀**: 흑연 : Super P : 바인더 = **96 : 1 : 3** (바인더 종류 미기재) · **N/P 1.1** · 2.5–4.0 V · 0.05 · 0.1 C 형성 뒤 **0.2 C** 수명 (⚠ 그림 6d 캡션 = **2.4 mA cm⁻²** → 7.8 mAh/cm² 기준 0.31 C [카드 산술]).
- **대칭 셀**: *"Symmetric pouch cells were assembled to measure the Li-ion transfer resistance (R_ion)"* · *"calculated in the frequency range of 1–1 MHz with an amplitude of 10 mV"* (인쇄 그대로) · 대칭 셀 전해질 · 면적 · 추출 모형 (TLM 등) [미확인].
- 분석 장비: FE-SEM MIRA II LMH (TESCAN) · Cs-TEM Titan Themis Z + FIB (Thermo Scientific) · XRD D8 Advance · BET Quadrasorb evo (Quantachrome) · **SAICAS EN-EX (Daipla Wintes) — 다이아몬드 날 폭 1 mm · shear angle 45° · rake angle 20° · clearance angle 10°** · XPS NEXSA (ThermoFisher) · Hg 압입 Autopore v (인쇄 그대로 · Micromeritics) [인쇄 p.9].
- 측정 온도 [미확인] (전 구간 미기재).

### 3-3. 바인더 형태 · 비표면적 · 깊이별 접착 (그림 2 · 3 · p.2–3)
- 단면 SEM (눈금 1 µm): 건식에 섬유화 PTFE · *"The bridge-like connection of fibrous PTFE enables efficient Li-ion diffusion into the LFP crystal"* [인쇄 p.2 — 주장] · Cs-TEM (FIB · 200 nm): 습식은 *"PVDF, covers the surfaces of the LFP particles"* · 근거 문장 *"the diffusion of Li ions in LFP occurs unidirectionally along the b-axis"* (참고 [3] [21]) [인쇄 p.2].
- **BET (N₂ 흡착 · 그림 2e 표)**: LFP particle **11.6** · LFP/PVDF slurry powder **9.5** · LFP/PTFE mixed powder **11.9 m²/g** [인쇄] — 해석 *"attributed to the spot contact between the fiberized PTFE and LFP particles"* · PVDF 는 *"relatively lower number of micropores"* [인쇄 p.2].  ⚠ 캡션은 'LFP electrodes' 인데 범례 · 본문은 '분말' (mixed / slurry powder) — 측정 시료가 성형 전극인지 분말인지 [미확인].
- 기공 크기 분포 (그림 2f) 봉우리: LFP/PTFE 혼합 ≈**2.6 nm** (dV ≈3.9) · LFP 분말 ≈4.4 nm (≈2.3) · LFP/PVDF ≈5.9 nm (≈1.0 cc nm⁻¹ g⁻¹) [판독 · 맨 위 화소].  원문이 'micropores' 라 부른 것은 이 2–6 nm 대 [카드 추론 — 이름의 국제 기준은 이 카드에서 판단하지 않는다].
- **SAICAS (그림 3 · p.2–3)**: 접착 세기 *"proportional to the binder ratio"* · 깊이 **30 µm 마다** (30 · 60 · 90 · 120 µm) · 박리 시험 (peel) 은 약한 계면에서만 떨어져 깊이별 분포를 못 본다는 이유로 SAICAS 를 씀 · F_H · F_V 동시 측정 · F_H 로 평가 · 결과 = 건식 *"nearly similar adhesion strengths"* · 습식 *"decreases (by approximately 12%) as the depth increases from the top to the middle and bottom points"* [인쇄 p.3] · 판독: 습식 30 µm ≈1.0 (400 s 쯤 ≈1.05) · 60 · 90 · 120 µm ≈0.88–0.90 · 건식 네 깊이 모두 ≈1.0 (흔들림 ≈0.9–1.3) (축 이름 'Normalized horizontal force (N)' · 'Normalized F_H (N)' — 정규화인데 'N' 단위 표기 그대로) [판독 · 그림 3b · 3c 눈대중 (축 눈금 0.3 간격 · 화소 계측 아님 · 계열 색 겹침 · digitized.csv 에 없음)] · 가로축은 깊이가 아니라 **시간 (s)** — 깊이마다 곡선 시작이 ≈0 · 65 · 125 · 185 s 로 밀려 있다 [판독].  ⚠ 120 µm 는 전극 두께 (175–190 µm · Al 포함) 의 2/3 쯤 — '바닥' 이 어디인지 [미확인] · 정규화 기준 [미확인].
- 저자 해석: 습식의 깊이 의존 = *"binder migration near the surface of the electrode during solvent evaporation"* (참고 [34]) [인쇄 p.3 — 측정은 깊이별 F_H 뿐].

### 3-4. ★ 반쪽 셀 전기화학 — 5.5 mAh/cm² (그림 4 · S1–S4 · 표 S1 · p.3–4)
**(a) 첫 사이클 · ΔV (그림 4a · C-rate 미기재)** — 평탄 중앙값 (면적 용량 1–4 mAh/cm²) [판독 · 원 래스터 · 1 화소 = 2.4 mV]:

| 전극 | 충전 평탄 (V vs Li/Li⁺) | 방전 평탄 | 차 ΔV [카드 산술] |
|---|---|---|---|
| 습식 | 3.562 | 3.302 | **0.26** |
| 건식 | 3.481 | 3.376 | **0.10** |

- 본문: *"the dry-processed electrode exhibits a low-voltage hysteresis (ΔV) between the lithiation and delithiation … associated with low overpotential"* (참고 [23] [24]) — **숫자 없음** [인쇄 p.3] · 두 전극 모두 첫 방전 끝 ≈5.4 mAh/cm² [판독].

**(b) CV (그림 4b · 5.5 mAh/cm²)** — 그림 안 글자 [인쇄]:

| 전극 | 산화 봉우리 | 환원 봉우리 | 간격 [카드 산술] |
|---|---|---|---|
| 습식 | **3.87 V** | **3.04 V** | **0.83 V** (본문 '(0.83)') |
| 건식 | **3.75 V** | **3.14 V** | **0.61 V** |

- 본문 *"which shows a 26% lower voltage hysteresis than the wet-processed one (0.83)"* — 0.61 / 0.83 = 0.735 → 26.5 % 낮음 [카드 산술] · **두 간격의 차 = 0.22 V** [카드 산술 — 원문에 인쇄 없음] · 봉우리 전류 ≈6.5 / ≈8.0 mA (산화) · ≈−5.9 / ≈−6.9 mA (환원) [판독 · 눈대중 (축 3 mA 간격) · digitized.csv 에 없음] · ⚠ 주사 속도 1 mV/s (본문 · 캡션) ↔ 0.1 mV/s (방법) · 전극 면적 미기재 → 전류 밀도 [미확인].

**(c) GITT (그림 4c · S1 · S3 · SI 식 (1))**
- **D_Li⁺ 1.06 × 10⁻¹¹ (습식) · 1.35 × 10⁻¹¹ cm²/s (건식)** — *"27.3% higher"* [인쇄 p.4 · 그림 4c 표] (1.35 / 1.06 = 1.274 → 27.4 % [카드 산술]) · 계산식 = SI 식 (1) **D = (4/πτ)·(m_B V_M / (M_B S))²·(ΔE_s/ΔE_t)²** (Weppner–Huggins 꼴 · SI 참고 [1] Nickol 2020) — 'S' 를 *"specific active surface area of the electrode"* 로 · *"m_B and M_B are the molecular weight and mass of the active material, respectively"* 로 적음 [인쇄 SI p.5] ⚠ 이 정의대로 넣으면 괄호 안 차원이 cm 가 아니다 (뒤바뀐 정의 [카드 산술 — 차원]) · 넣은 S · m_B · V_M 값 미인쇄 → D 재계산 불가.
- 그림 S3 (펄스 한 쌍): 펄스 ≈597 s (τ = 10 분) · 휴지 ≈604 s [판독 — 방법 '30 분' 과 다름] · 점선 표시 ΔE_t **≈34 mV (습식 · 3.485 → 3.518 V) · ≈27 mV (건식 · 3.463 → 3.489 V)** · ΔE_s = E₁ − E₀ ≈ −0.6 / −0.3 mV [판독 — 그림 분해능 ≈0.2 mV/화소 근처] → 2 상 평탄 구간에서 ΔE_s 가 판독 분해능 근처라 (ΔE_s/ΔE_t)² 를 그림에서 다시 셀 수 없다 · 원문은 2 상 (LFP) 에서 이 식의 적용성을 논하지 않는다 [카드 추론].
- 그림 S1 (GITT IR 강하 · 세로축 'Δ Voltage (mV)' · 가로축 'Points on GITT' ≈33 점): 습식 **≈44–50 mV** (점 1–29) → 점 30 뒤 오르며 ≈60 mV 축 위로 벗어남 · 건식 **≈24–34 mV** [판독 · 표본 점 = digitized.csv (습식 7 · 건식 8 점 · 44.1–49.1 · 24.3–32.7 mV) · 범위 = 곡선 눈대중] — 본문 *"a large internal resistance drop is observed in the wet-processed electrode during the initial charging phase"* (참고 [25]) [인쇄 p.3].

**(d) 율속 (그림 4d · S4 · 0.1 C 충전 뒤 방전)** [판독 · 사이클마다 표지 중심]:

| 율 | 습식 (mAh/cm²) | 건식 (mAh/cm²) |
|---|---|---|
| 0.05 C (1–3) | 5.40 · 5.40 · 5.39 | 5.47 · 5.47 · 5.46 |
| 0.1 C (4–6) | 5.37 · 5.37 · 5.36 | 5.43 · 5.42 · 5.42 |
| 0.2 C (7–9) | 5.29 · 5.29 · 5.28 | 5.38 · 5.37 · 5.37 |
| 0.3 C (10–12) | 5.17 · 5.16 · 5.15 | 5.32 · 5.31 · 5.31 |
| 0.5 C (13–15) | 4.89 · 4.88 · 4.87 | 5.20 · 5.19 · 5.18 |
| 1 C (16–18) | **4.33 · 4.31 · 4.32** | **4.89 · 4.89 · 4.87** |
| 0.1 C (19–20) | (건식 표지에 가림) | 5.37 · 5.34 |

- 1 C / 0.05 C [카드 산술 · 세 점 평균]: **습식 4.318 / 5.396 = 80.0 % · 건식 4.884 / 5.464 = 89.4 %**.  ⚠ 본문 *"At 1C, the retention of the discharge capacity for the wet- and dry-processed electrodes is 89% and 80%, respectively"* [인쇄 p.4] = **순서가 그림과 반대** (같은 문단 첫 문장 *"The dry-processed electrode shows a larger discharge capacity than the wet-processed electrode"* 와도 반대).

**(e) 반쪽 셀 수명 (그림 S2 · 1.08 mA/cm² ≈0.2 C · 표 S1)**
- 그림 S2 (셀 하나씩): 습식 5.37 (1) · 5.42 (2) · 5.38 (3) → **4.82** (40) · 건식 5.44 · 5.53 · 5.50 → **5.37 mAh/cm²** (40) [판독] · 본문 *"the wet-processed electrode experiences severe discharge capacity degradation after only five cycles"* [인쇄 p.3].
- **표 S1 (같은 조건 5 + 5 셀)** [인쇄 SI p.4]:

| 셀 | 부하 (mg/cm²) | 'Cathode Current Density' (mAh/cm²) | 밀도 (g/cc) | 1 번째 충 / 방 (mAh/g) | ICE | 40 번째 충 / 방 | C.E. | 40 사이클 유지 |
|---|---|---|---|---|---|---|---|---|
| Wet 1 | 34.69 | 5.48 | 2.09 | 161.4 / 160.5 | 99.4 % | 140.7 / 139.9 | 99.4 % | 85.9 % |
| Wet 2 | 34.26 | 5.42 | 2.08 | 160.7 / 158.7 | 98.8 % | 146.0 / 145.5 | 99.6 % | 91.4 % |
| Wet 3 | 33.42 | 5.28 | 2.09 | 160.6 / 158.0 | 98.4 % | 138.5 / 137.7 | 99.4 % | 87.2 % |
| Wet 4 | 33.23 | 5.25 | 2.15 | 160.8 / 158.5 | 98.6 % | 143.8 / 143.2 | 99.6 % | 90.3 % |
| Wet 5 | 33.34 | 5.27 | 2.10 | 161.1 / 160.5 | 99.6 % | 142.2 / 141.6 | 99.6 % | 88.2 % |
| Dry 1 | 32.94 | 5.21 | 2.3 | 161.3 / 159.6 | 98.9 % | 157.9 / 156.8 | 99.3 % | 98.2 % |
| Dry 2 | 32.86 | 5.20 | 2.31 | 161.4 / 160.2 | 99.3 % | 158.2 / 157.3 | 99.4 % | 98.0 % |
| Dry 3 | 33.6 | 5.31 | 2.29 | 160.6 / 159.2 | 99.1 % | 154.6 / 153.7 | 99.4 % | 96.5 % |
| Dry 4 | 33.47 | 5.29 | 2.32 | 162.2 / 161.6 | 99.6 % | 159.6 / 158.4 | 99.2 % | 98.0 % |
| Dry 5 | 33.46 | 5.29 | 2.3 | 161.3 / 160.4 | 99.4 % | 157.8 / 156.5 | 99.2 % | 97.6 % |

- [카드 산술] 평균: 습식 첫 방전 159.2 · ICE 98.96 % · 40 번째 방전 141.6 · 유지 **88.6 %** / 건식 160.2 · 99.26 % · 156.5 · **97.7 %**.
- [카드 산술] '유지율' = 40 번째 방전 ÷ 첫 방전 으로 7 셀이 ±0.05 %p 안에서 재현 · **Wet 1 = 87.2 (인쇄 85.9 · −1.3 %p)** · Wet 2 = 91.7 (91.4) · Dry 2 = 98.2 (98.0).
- [카드 산술] **'Cathode Current Density' 칸 ÷ 부하 = 0.1580–0.1583 mAh/mg (10 셀 모두)** → 이 칸은 측정값이 아니라 **부하 × 158 mAh/g (전극) = 162.9 mAh/g (LFP)** 로 매긴 설계 면적 용량이고 이름 ('current density') 도 단위 (mAh/cm²) 와 안 맞는다.  본문의 '35 mg/cm²' 는 실측 32.86–34.69 의 반올림 위쪽 값.

### 3-5. ★ 기공 쪽 이온 수송 — 대칭 셀 R_ion · Hg 기공 · N_M · τ (그림 5a–c · S5 · p.4–5)
- **R_ion (그림 5a 글자)**: **습식 35.01 Ω · 건식 6.19 Ω** [인쇄] → −82.3 % [카드 산술] (본문 *"an 83% reduction in the R_ion value"* p.4) · 정의 문장 *"R_ion is directly related to the Li-ion transport through the pore channels within the electrode"* (참고 [32]) · 면적 정규화 없음 · 대칭 셀 전해질 · 면적 · 추출 모형 미기재 [미확인] · 그림 5a 습식 스펙트럼 = ≈5 → ≈44 Ω 반원 + 비스듬한 직선 · 건식 = ≈5 Ω 에서 시작하는 비스듬한 직선 (≈25 Ω 까지) [판독 · 눈대중 · 축 20 Ω 간격] (어느 구간 · 어떤 모형으로 R_ion 을 맞췄는지 미기재 — 차단 조건 TLM 이면 보통 45° 구간의 투영 × 3 이지만 이 논문은 그 식을 적지 않는다 [카드 추론]).
- **Hg 압입 (그림 5b 표 · SI 그림 S5)**: 기공률 **습식 39.5 % · 건식 38.2 %** (S5 막대 글자 **39.46 · 38.23 %**) [인쇄] · 해석 *"owing to the low density of the wet-processed electrode"* · 기공 지름 분포: 건식 **0.02–0.1 µm** 좁은 봉우리 · 습식 **0.02–0.3 µm** 넓은 봉우리 [인쇄 p.4] · 봉우리 ≈0.052 µm (건식 · 0.63 mL/g) · ≈0.079 µm (습식 · 0.41 mL/g) [판독 · 표지 윗변].
- **습식 고밀도 한계**: *"A high-density wet-processed electrode could not be fabricated at high areal capacity (>2.2 g cc⁻¹, >5 mA h cm⁻²) because of delamination between electrode layer and current collector"* [인쇄 p.4].
- **N_M · τ (그림 5c 막대 — 숫자 미인쇄)** [판독 · 막대 윗변 · 왼축 N_M 0–30 · 오른축 τ 0–10]:

| 전극 | N_M (MacMullin) | τ ('Tortuosity') | ε (Hg) | ε·N_M [카드 산술] | f = 1/N_M [카드 산술] |
|---|---|---|---|---|---|
| 습식 | **22.3** | **8.80** | 0.395 | 8.80 | 0.045 |
| 건식 | **4.34** | **1.66** | 0.382 | 1.66 | 0.230 |

- [카드 산술] **막대 τ = ε·N_M 이 두 전극 모두 판독 정밀도 안에서 맞는다** → 원문 τ 는 **Landesfeind 꼴 'tortuosity' (N_M = τ/ε)** = 우리 규약의 **tau2 (수송 tortuosity · tortuosity factor)** 이지 √ 값 (tau) 이 아니다 [카드 추론 · 식 미인쇄 — 본문 *"MacMullin number (N_m) and tortuosity (τ); these parameters represent Li ions transport through the pore channels, regardless of the thickness and porosity of the electrode (Figure 5c).[35,36]"* p.5].
- [카드 산술] N_M 판독 비 22.29 / 4.34 = **5.14** ↔ R_ion 비 × 두께 비 = 5.656 × 175/190 = **5.21** (Al 뺀 코팅 155/170 이면 **5.16**) → 같은 면적 · 같은 전해질 κ 에서 N_M ∝ R_ion/d 로 계산했다는 것과 맞는다 (식 · A · κ 미인쇄).
- 원문 문장의 논리 주의: *"Both the N_m and τ values of the dry-processed electrode were lower … despite its low thickness and porosity"* — N_M 은 두께를 이미 나눈 양이다 [카드 추론].
- [카드 산술] **같은 조성인데 다른 골격 밀도**: 2.3 / (1 − 0.382) = **3.72 g/cm³** (건식) ↔ 2.1 / (1 − 0.395) = **3.47 g/cm³** (습식) (표 S1 평균 밀도로도 3.73 ↔ 3.47) — 같은 97 : 1 : 2 고체면 같은 골격 밀도여야 한다 → Hg 기공과 명목 밀도가 한 골격 밀도로 함께 맞지 않는다 (3.72 면 습식 2.1 g/cc 는 43.6 % · 3.47 이면 건식 2.3 g/cc 는 33.7 % [카드 산술]) · 원인 [미확인] (Hg 시료 · 측정 범위 · 명목 밀도 정의).

### 3-6. 계면 — R_ct · XPS · XRD · 사이클 뒤 SEM (그림 5d · S6–S10 · p.5–6)
- **R_ct**: 사이클 전 *"similar"* (그림 S6 — 두 반원 모두 ≈945 Ω 에서 닫힘 · 꼭대기 −Z_im ≈335–341 Ω [판독]) → 사이클 뒤 (그림 5d · 회로 R_b–(R_ct–W)∥CPE): **습식 반원 ≈2.7 → ≈366 Ω (오른쪽 끝 = 표지 바깥 가장자리 · 꼭대기 ≈185 / 114 Ω) · 건식 ≈2.1 → ≈17.5 Ω (삽도 극소 · 꼭대기 ≈8.8 / 3.3 Ω)** [판독 · digitized.csv] → R_ct ≈360 ↔ ≈15 Ω (≈24 배) [카드 산술 · 판독] · 본문 *"After cycling, the reduction in the R_ct value is unexpectedly large"* [인쇄 p.5 — 숫자 없음] · 몇 사이클 뒤인지 [미확인].
- **F 1s XPS (그림 S7)**: 사이클 전 *"only peaks corresponding to PVDF (687.8 eV) and PTFE (689.9 eV) were detected (Figure S7a,b …)"* [인쇄 p.5] · 사이클 뒤 **습식 PVDF 43.5 % · LiF 56.5 % / 건식 PTFE 45.9 % · LiF 54.1 %** [인쇄 그림 글자] · 저자 결론 = 습식이 LiF 많음 → 건식 *"homogeneous CEI"* → 사이클 뒤 R_ct ↓ [인쇄 p.5–6].  ⚠ 판독 봉우리 위치: 습식 전 ≈687.6 · 습식 뒤 PVDF ≈687.7 · LiF ≈685.7 · **건식 전 PTFE ≈687.5 eV** · 건식 뒤 PTFE ≈688.9 · LiF ≈685.4 eV [판독 · 눈금 글자 중심 ±0.2 eV] → 본문의 PTFE **689.9 eV 는 그림의 '사이클 전' 봉우리 (≈687.5) 와 맞지 않는다** · 본문의 패널 글자 (a,b = 전 · c,d = 뒤) 는 그림 · SI 캡션 배치 (a,b = 습식 전 · 뒤 · c,d = 건식 전 · 뒤) 와 다르다.  LiF 몫 차 = 2.4 %p [카드 산술].
- **바인더 안정**: PVDF · PTFE 미반응 — CF₂ 봉우리 (그림 S8 = 사이클 뒤 PTFE 섬유 SEM) · *"XRD results indicate a persistent presence of the PTFE peak at 18° both before and after cycling"* [인쇄 p.6] ⚠ 그림 S9 별표 = **≈17.0°** 봉우리 위 [판독] · 바로 옆 ≈17.9° 작은 봉우리 · **LFP 분말 곡선에도 ≈17.1° 작은 봉우리** [판독] → 그림만으로 별표 봉우리를 PTFE 몫으로 가를 근거가 없다 [카드 추론].
- **사이클 뒤 단면 SEM (그림 S10 · 500 nm)**: 습식 LFP 입자 *"cracks … were observed"* (화살표 'Crack formation') · 건식 없음 · 이유 = *"the high stress of inserting and extracting Li ions in the particles of the wet-processed LFP electrode"* (참고 [42]) [인쇄 p.6 — 기전은 인용 · 응력 측정 없음].

### 3-7. 전셀 · 후막 · 에너지 밀도 (그림 6 · 8 · S11 · S12 · 표 S2 · S3 · p.6–8)
- **전셀 율속 (그림 6a · 5.5 mAh/cm² · N/P 1.1)** [판독]: 건식 0.05 C **5.55 · 5.53 · 5.51** · 0.1 C 5.44 · 5.43 · 5.43 · 0.2 C 5.36 · 5.34 · 5.33 · 0.3 C 5.25 · 5.23 · 5.21 · 0.5 C 5.04 · 5.03 · 5.00 · **1 C 3.97 · 3.92 · 3.90** · 0.1 C 회복 5.27 · 5.30 / 습식 (1–4 번째는 건식 표지와 겹쳐 판독 안 함) 0.1 C 5.28 · 5.27 (5 · 6 번째) · 0.2 C 4.98 · 4.95 · 4.92 · 0.3 C 4.47 · 4.43 · 4.39 · 0.5 C 2.88 · 2.80 · 2.75 · **1 C ≈0** (축 위 표지) · 회복 5.11 mAh/cm².  본문 *"It almost reaches near-zero capacity when it was tested at 1C"* (습식) · *"the dry-processed LFP/graphite cell shows a discharge capacity of 4 mAh cm⁻² at 1C; this value was approximately 75% of its discharge capacity at 0.05C"* [인쇄 p.6–7] ↔ 판독 3.93 / 5.53 = **71.1 %** [카드 산술].
- **7.8 mAh/cm² 전셀 (그림 6d · 2.4 mA/cm²)**: 첫 표지 ≈**7.84** · 5 번째 ≈7.16 · 10 ≈6.91 · 25 ≈6.41 · 50 ≈6.04 · 100 ≈5.71 · 150 ≈5.45 · 200 ≈5.20 · 250 ≈4.98 · 290 ≈4.83 · **299 ≈4.80 mAh/cm²** [판독 · 표지 띠 가운데 · 띠 두께 ≈0.34 mAh/cm² · digitized.csv] → 첫 점 기준 **≈61 %** (4.795 / 7.844) · 5 번째 기준 ≈67 % (4.795 / 7.156) [카드 산술] · CE ≈99–100 % (첫 몇 점 ≈93–97 % [판독 · 눈대중 · digitized.csv 에 없음]) · 원문 = *"achieved excellent cycle stability over 300 cycles"* (유지율 숫자 없음) [인쇄 p.7].  첫 사이클 곡선 (그림 S12): 충전 ≈7.95 · 방전 ≈7.84 [판독] — ⚠ 축 이름 'Capacity (mAh/g)' · 'Voltage (V vs Li/Li⁺)' 은 값 (면적 용량 · 전셀 전압) 과 맞지 않는다 [카드 추론].
- **후막 제조성**: *"it is technically difficult to fabricate a wet-processed electrode with the same areal capacity and electrode density because of issues related to crack formation (Figure S11)"* · 균열 = PVDF 불균일 → 약한 접착 [인쇄 p.7] · 그림 S11 = 7.8 mAh/cm² 습식 (표면 균열) ↔ 건식 (매끈) 사진.
- 기존 문헌 수준: *"Most of the previous studies with regard to LFP full cells have evaluated LFP electrodes with low areal capacity (≈3 mAh cm⁻²) and low density (≈2.1 g cc⁻¹)"* [인쇄 p.7].
- **표 S2 (그림 8) 문헌 비교** [인쇄 SI p.15]: 이 연구 **7.8 mAh/cm² · 376.8 mAh/cm³ · LFP 97 % · 2.3 g/cc · 건식** ↔ [2] 4.56 · 141.9 · 80 · 0.91 · 습식 / [3] 0.83 · 118.57 · 70 · 1 · 습식 / [4] 3.2 · 248 · 80 · 1.55 · 습식 / **[5] 3.1 · 256.2 · 90 · 2.0 · 건식** / [6] 3.14 · 129.2 · 37.43 · 2.2 · 습식 / [7] 2.53 · 314 · 80.8 · 1.965 · 습식 / [8] 2.76 · 168 · 80 · – · 습식 / [9] 2.42 · 234.35 · 80 · 1.38 · 습식 / [10] 1.5 · 68.18 · 76 · 1.9 · cold plasma coating.  ⚠ [5] = Zhang 2023 *"Solvent-free lithium iron phosphate cathode fabrication with fibrillation of polytetrafluoroethylene"* (SI 참고 [5]) — **PTFE 섬유화 건식 LFP 가 이미 보고**되어 있다 (3.1 mAh/cm²) → 서론 · 초록의 *"reported for the first time"* · *"has not been reported yet"* 은 '후막 (높은 부하)' 에 한정해 읽어야 한다 [카드 추론].
- [카드 산술] **부피 용량 376.8 의 기준**: 376.8 ÷ 2.3 = 163.8 mAh/g (전극) = 168.9 mAh/g (LFP) ↔ 표 S3 의 7.8 mAh/cm² · 52 mg/cm² = 150 mAh/g (전극) — 같은 52 mg/cm² · 2.3 g/cc 면 코팅 ≈226 µm · 7.8 / 0.0226 = **≈345 mAh/cm³** → 376.8 은 표 S3 과 다른 비용량 기준으로 계산된 값.
- **표 S3 (각형 셀 추정)** [인쇄 SI p.16]: 습식 (thin) 3 mAh/cm² · 20 mg/cm² · 118 Wh/kg · 375 Wh/L / 습식 (thick) 5 · 33 · 153 · 390 / 건식 (super thick) 7.8 · 52 · 185 · **400 Wh/L** / 건식 + **high density LFP** 7.8 · 52 · 185 · **470 Wh/L** — 본문 *"the gravimetric/volumetric energy density of the dry-processed LFP electrode can be maximized to 185 Wh kg⁻¹/470 Wh L⁻¹"* 의 470 은 '고밀도 LFP' 칸 · 셀 설계값 (분리막 · 집전체 · 케이스) · 계산식 미인쇄 [미확인] · CTP: *"increase the gravimetric and volumetric energy densities by 10–15% and 50%, respectively"* (참고 [44]) → **213 Wh/kg · 705 Wh/L** [인쇄 p.8] = 185 × 1.15 = 212.75 · 470 × 1.5 = 705 [카드 산술].

### 3-8. 인쇄값끼리 어긋남 (원문 비판 — §11 에 다시)
1. **1 C 유지율 순서**: 본문 '습식 89 · 건식 80 %' ↔ 그림 4d 판독 습식 80.0 · 건식 89.4 %.
2. **CV 주사 속도**: 본문 p.3 · 그림 4 캡션 **1 mV s⁻¹** ↔ 방법 p.9 **0.1 mV s⁻¹**.
3. **GITT**: 방법 '0.1 mA cm⁻² · 10 분 펄스 · 30 분 휴지' ↔ 그림 S3 휴지 ≈604 s [판독] · 그림 4c 충전 구간 ≈35 000 s 에 0.1 mA/cm² · 듀티 ½ 면 0.1 × 35 000 / 3600 × ½ = **0.49 mAh/cm²** (휴지 30 분이면 0.24) ≪ 5.5 mAh/cm² [카드 산술] — 그림의 전 충전 (4.2 V 도달) 과 맞으려면 ≈1.1 mA/cm² (≈0.2 C) 가 필요 [카드 산술] · 독립 대조: 그림 S1 의 GITT 점 ≈33 개 × 10 분 펄스로 5.5 mAh/cm² 를 채우려면 5.5 × 3600 / (33 × 600) ≈ **1.0 mA/cm²** [카드 산술] → 인쇄된 펄스 전류 (0.1 mA/cm²) · 휴지 (30 분) 중 적어도 하나는 그림과 안 맞는다.
4. **SI 식 (1) 기호**: m_B · M_B 정의가 뒤바뀜 (차원) · S 를 'specific' 면적으로 표기.
5. **XPS**: PTFE 689.9 eV (본문) ↔ 그림 S7c 사이클 전 봉우리 ≈687.5 eV [판독] · 패널 글자 (본문 S7a,b / c,d ↔ 그림 배치).
6. **XRD**: PTFE 18° (본문) ↔ 별표 ≈17.0° [판독] · LFP 분말에도 같은 자리 봉우리.
7. **전셀 수명 율**: 방법 0.2 C ↔ 그림 6d 캡션 2.4 mA/cm² (7.8 mAh/cm² 의 0.31 C · 5.5 mAh/cm² 기준이면 0.44 C [카드 산술]).
8. **전셀 1 C**: '≈75 %' ↔ 판독 71.1 %.
9. **R_ion**: '83 %' ↔ 그림 글자로 82.3 %.
10. **골격 밀도**: Hg 기공 ↔ 명목 밀도가 같은 조성에 다른 골격 밀도 (3.72 ↔ 3.47 g/cm³) 를 함축.
11. **표 S1**: 'Cathode Current Density' (mAh/cm²) = 부하 × 0.158 (설계값 · 이름 단위 어긋남) · Wet 1 유지율 85.9 ↔ 재계산 87.2 % · 'L.oading Level' 오타.
12. **부피 용량** 376.8 ↔ 표 S3 기준 ≈345 mAh/cm³ [카드 산술].
13. **EIS 범위** '250 kHZ to 10 MHz' · R_ion '1–1 MHz' (인쇄 그대로).
14. **그림 S12** 축 이름 (mAh/g · V vs Li/Li⁺) ↔ 값 (≈7.8 · 전셀).
15. **그림 7** 모식 '140µm ≥' ↔ 175 µm (방법) · ≈226 µm (7.8 mAh/cm² 산술).
16. **BET** 캡션 'electrodes' ↔ 범례 · 본문 'powder'.
17. **'처음 보고'** ↔ 표 S2 의 [5] (건식 PTFE 섬유화 LFP 3.1 mAh/cm²).
18. 본문 오타: *"outperforms the that with"* (p.2) · 'Tortusity' (그림 5c 범례).

---

## 4. ★ 방법 — 장치 · 측정 사슬 · 해석

### 4-1. 장치
행성 혼합기 ARE-310 (THINKY) · 막자 · 열 압착 · 라미네이트 (60 °C · 장비 미기재) · 캘린더 (장비 미기재) · 진공 오븐 (100 °C · 습식) · FE-SEM MIRA II LMH (TESCAN) · Cs-TEM Titan Themis Z + FIB (Thermo Scientific) · XRD D8 Advance · BET Quadrasorb evo (Quantachrome) · SAICAS EN-EX (Daipla Wintes · 다이아몬드 날 1 mm · 45° · 20° · 10°) · XPS NEXSA (ThermoFisher) · Hg Autopore v (Micromeritics) · 충방전기 WBCS3000L32 (WonATech) · 전위기 VSP (Biologic) · CR2032 (Wellcos) · 대칭 파우치 셀 [인쇄 p.9].

### 4-2. 측정 사슬 (재구성)
LFP + Super P + PVDF (NMP 슬러리) → 20 µm Al 캐스팅 → 100 °C 진공 → 캘린더 2.1 g/cc (190 µm) / LFP + Super P + PTFE → 행성 혼합기 + 막자 → 60 °C 압착 · Al 라미네이트 → 캘린더 2.3 g/cc (175 µm) → (i) 단면 SEM · FIB-TEM · BET (분말) · SAICAS 깊이 30–120 µm (ii) Hg 압입 · 대칭 파우치 셀 EIS (R_ion → N_M · τ) (iii) Li 반쪽 셀 (5.5 mAh/cm²): 형성 0.05 · 0.1 C → 첫 사이클 · CV · GITT (D_Li · IR 강하) · 율속 0.05–1 C · 0.2 C 40 사이클 (표 S1 5 + 5 셀) · 사이클 전 · 뒤 EIS (R_ct) · XPS · XRD · 단면 SEM (iv) 흑연 전셀 (N/P 1.1): 율속 · 7.8 mAh/cm² · 2.3 g/cc 300 사이클 (v) 문헌 비교 (표 S2 · 그림 8) · 각형 셀 에너지 밀도 추정 (표 S3) · CTP 배수.

### 4-3. 해석 (저자 기전 — 이 논문 안의 측정과 연결 정도)
| 저자 주장 | 이 논문 안의 근거 | 연결 정도 [카드 추론] |
|---|---|---|
| PTFE 섬유 = 점 접촉 → LFP 표면 노출 → Li 출입 쉬움 | BET 11.9 ≈ 11.6 ↔ PVDF 9.5 m²/g · TEM 정성 | 비표면적 차는 측정 · '점 접촉' 과 '확산 쉬움' 의 연결은 해석 |
| PVDF 가 표면을 덮어 b 축 Li 확산을 막음 | TEM 정성 · 참고 [3] [21] | 덮임 정량 0 |
| 용매 증발이 없어 바인더가 고름 → 기공 균일 → R_ion ↓ · N_M · τ ↓ | SAICAS (습식 ≈12 % ↓) · Hg 분포 폭 · R_ion | 깊이 의존 F_H 는 측정 · 바인더 '비율' 로 읽는 것은 가정 (*"proportional to the binder ratio"*) |
| 균일 CEI (LiF 적음) → 사이클 뒤 R_ct ↓ | XPS LiF 56.5 ↔ 54.1 % · R_ct ≈360 ↔ ≈15 Ω [판독] | LiF 차 2.4 %p 에 R_ct 24 배 — 크기 연결 근거 없음 |
| 습식 LFP 입자 균열 = 삽입 응력 | 사이클 뒤 SEM 정성 · 참고 [42] | 응력 · 기계 측정 없음 |
| 건식 = 높은 D_Li (+27 %) | GITT (그림 4c) | 2 상 평탄에서 ΔE_s 가 판독 분해능 근처 · 식 기호 오기 — D 값의 신뢰 범위 미제시 |

### 4-4. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM 한계 진술 = 말 없음** — 이 논문은 계산을 하지 않는다 (DEM · FEM · 연속체 0).
- **(ii) 소성 · 큰 변형을 계산에 넣는 어려움 = 논의 없음** — 기계 쪽 문장은 *"a dry process, which uses polytetrafluoroethylene (PTFE) as a deformable binder"* (p.2) 와 섬유화 · 압착 서술뿐 · PTFE 섬유화의 하중 · 변형 · 온도 조건은 [미확인] · LFP 입자 변형 · 파쇄는 사이클 뒤 SEM 정성 (습식만 균열) 하나.
- **(iii) 차원**: 측정은 단면 SEM · TEM (2D 영상) · Hg · BET (부피 평균) · 전기화학 (1D 두께 방향) · 2D → 3D 전이 진술 없음.
- **(iv) 탈압**: **다루지 않는다** — 압착 · 캘린더 하중도, 하중을 뺀 뒤 두께 회복도 없음 (두께는 최종값 190 / 175 µm 만).

### 4-5. 기법 미니 용어집
- **건식 전극 공정 (dry electrode process)** = 용매 없이 활물질 · 도전재 · PTFE 를 전단으로 섞어 PTFE 를 섬유로 늘리고 (섬유화) 압연해 막을 만든 뒤 집전체에 붙이는 공정.
- **섬유화 (fibrillation)** = 전단을 받은 PTFE 입자가 가는 섬유로 늘어나 입자들을 그물처럼 묶는 현상.
- **SAICAS** = 기울인 날로 전극을 정해진 깊이까지 비스듬히 깎으며 수평 · 수직 힘을 재는 장비 — 깊이별 접착 (바인더 분포) 을 본다.
- **대칭 셀 R_ion** = 같은 전극 두 장을 마주 놓은 셀의 임피던스에서 기공 전해질의 이온 저항만 뽑은 값 (Li 출입이 없는 조건에서).
- **MacMullin 수 (N_M)** = 전해질 자체 전도도 ÷ 전극 기공 안 유효 전도도 = 1/f · 'tortuosity' τ = ε·N_M (이 논문의 막대가 맞는 꼴) = 우리 tau2.
- **GITT** = 짧은 전류 펄스와 휴지를 번갈아 주며 전압 변화 (ΔE_t · ΔE_s) 로 고상 확산 계수를 구하는 법 (SI 식 (1)).
- **BET 비표면적** = 질소 흡착량으로 잰 g 당 표면적.
- **Hg 압입 (mercury porosimetry)** = 수은을 압력으로 밀어 넣어 기공 부피 · 지름 분포를 재는 법.
- **N/P 비** = 음극 용량 ÷ 양극 용량.
- **CTP (cell-to-pack)** = 모듈 없이 셀을 팩에 바로 넣는 설계 — 팩 에너지 밀도를 올린다.

---

## 5. Figure set ★
| 그림 · 표 | 내용 | 크롭 | 우리 활용 |
|---|---|---|---|
| 그림 1 | 건식 공정 모식 (혼합 → 섬유화 → 압연 · 라미네이트) | `fig_1.png` (손 · 도구가 놓침) | 공정 단계 이름 (흐름 밖: 건식) |
| 그림 2a–d | 단면 SEM (1 µm) · Cs-TEM (200 nm) 습식 / 건식 | `fig_2.png` · `fig_2a`–`fig_2d.png` | PTFE 섬유 vs PVDF 덮임 (정성) — STEP3 PTFE 표현 |
| 그림 2e | N₂ 등온선 + 비표면적 표 (11.6 / 9.5 / 11.9) | `fig_2e.png` | '덮지 않는 바인더' 의 숫자 근거 |
| 그림 2f | 기공 크기 분포 (≈2.6 / 4.4 / 5.9 nm [판독]) | `fig_2f.png` | — |
| 그림 3 | SAICAS 모식 + 깊이 30–120 µm F_H (습식 ≈12 % ↓) | `fig_3.png` · `fig_3a`–`fig_3c.png` | 바인더 깊이 분포 관측량 |
| 그림 4a | ★ 첫 사이클 곡선 (평탄 차 ≈0.26 / ≈0.10 V [판독]) | `fig_4a.png` | 'ΔV' 의 정전류 쪽 정의 |
| 그림 4b | ★ CV (3.87/3.04 · 3.75/3.14 V 글자 → 0.83 · 0.61 V) | `fig_4b.png` | ★ 0.22 V 의 유일한 출처 (차 · 카드 산술) |
| 그림 4c | GITT 전 구간 + D_Li 표 (1.06 / 1.35 × 10⁻¹¹) | `fig_4c.png` | GITT D 인용 주의 (§3-4c) |
| 그림 4d | 반쪽 셀 율속 (1 C 유지 80.0 / 89.4 % [판독]) | `fig_4d.png` | 본문 89 / 80 % 순서 오류의 근거 |
| 그림 5a | ★ 대칭 셀 EIS — R_ion 35.01 / 6.19 Ω | `fig_5a.png` | 기공 쪽 이온 저항 (액체) |
| 그림 5b | Hg 분포 + 기공률 표 39.5 / 38.2 % | `fig_5b.png` | 단계 0 (기공 연산자 · 측정법) |
| 그림 5c | ★ N_M · τ 막대 (22.3 / 4.34 · 8.80 / 1.66 [판독]) | `fig_5c.png` | 수송 tortuosity (tau2) 꼴 · 바인더만으로 ×5.3 |
| 그림 5d | 사이클 뒤 EIS · 회로 (R_ct ≈360 / ≈15 Ω [판독]) | `fig_5d.png` | — |
| 그림 6a–c | 전셀 율속 · 전압 곡선 (1 C 건식 ≈3.93 · 습식 ≈0) | `fig_6.png` · `fig_6a`–`fig_6c.png` | — |
| 그림 6d | ★ 7.8 mAh/cm² 전셀 300 사이클 (≈7.84 → ≈4.80 [판독]) | `fig_6d.png` | 건식 후막 기준점 (액체 LIB) |
| 그림 7 | 기전 모식 (습식 = 덮임 · 박리 · 고 R_ion / 건식 = 섬유 · '140µm ≥') | `fig_7.png` | — |
| 그림 8 | 부피 용량 vs 면적 용량 (표 S2) | `fig_8.png` | — |
| 그림 S1 | GITT IR 강하 (≈44–50 / ≈24–34 mV [판독]) | `fig_S1.png` | — |
| 그림 S2 | 반쪽 셀 40 사이클 (1.08 mA/cm²) | `fig_S2.png` | — |
| 그림 S3 | GITT 펄스 · ΔE_s · ΔE_t 정의 (휴지 ≈604 s [판독]) | `fig_S3.png` · `fig_S3a` · `fig_S3b.png` | GITT 방법 대조 |
| 그림 S4 | 반쪽 셀 율속 전압 곡선 | `fig_S4.png` · `fig_S4a` · `fig_S4b.png` | — |
| 그림 S5 | Hg 기공률 막대 39.46 / 38.23 % | `fig_S5.png` (손 · 벡터) | 단계 0 |
| 그림 S6 | 사이클 전 EIS (반원 ≈945 Ω) | `fig_S6.png` | — |
| 그림 S7 | F 1s XPS 전 · 뒤 (LiF 56.5 / 54.1 %) | `fig_S7.png` · `fig_S7a`–`fig_S7d.png` | PTFE 689.9 ↔ ≈687.5 eV 어긋남 |
| 그림 S8 | 사이클 뒤 PTFE 섬유 SEM | `fig_S8.png` | 섬유 형태 (정성) |
| 그림 S9 | XRD (별표 ≈17.0° [판독] · 본문 18°) | `fig_S9.png` | — |
| 그림 S10 | 사이클 뒤 단면 SEM (습식 입자 균열) | `fig_S10.png` · `fig_S10a` · `fig_S10b.png` | R7 (사이클 균열 · 압밀 균열 아님) |
| 그림 S11 | 7.8 mAh/cm² 전극 사진 (습식 균열) | `fig_S11.png` · `fig_S11a` · `fig_S11b.png` | 후막 제조성 (정성) |
| 그림 S12 | 건식 전셀 첫 사이클 (축 이름 어긋남) | `fig_S12.png` | — |
| 표 S1 | ★ 반쪽 셀 5 + 5 셀 (부하 · 밀도 · 첫 · 40 번째 · 유지) | `tab_S1.png` (손 · 캡션 아래) | 셀 간 산포 (실현 수 5) |
| 표 S2 | 문헌 LFP 비교 (9 편 + 이 연구) | `tab_S2.png` | — |
| 표 S3 | 각형 셀 에너지 밀도 추정 | `tab_S3.png` | — |
| SI 식 (1) | GITT D_Li 식 | `eq_S1_gitt_diffusion_coefficient.png` | 식 기호 정의 오류 근거 |
| 근거 문단 18 | 초록 · 공정 세 단계 · BET · SAICAS · ΔV · CV · D · 율속 · R_ion · Hg · N_M · XPS · XRD · 전셀 · 후막 · 에너지 밀도 · 제조 · 셀 조건 · SI 기호 | `txt_p*.png` · `txt_sip5_*.png` | 원문 인용용 |
- 그림 크롭은 도구 관례대로 **캡션 제외** (캡션은 `figures.json` · 지수 · 합자 · 하이픈 고침) · 표는 캡션 포함 · 패널 둘 (`fig_5b` · `fig_5d` · `fig_6a` · `fig_6d`) 은 상자 안에 걸린 **이웃 패널의 라벨 · 축 제목 조각만** 흰색으로 지웠다 (패널 내용 무변경 · `figures.json` 에 화소 범위).

## 6. Post-processing ★
- **무엇을 (원문)**: SAICAS F_H 곡선 · BET 다점 비표면적 · Hg 분포 · 대칭 셀 EIS 맞춤 (R_ion · 모형 미기재) · N_M · τ (식 미인쇄) · GITT D (SI 식 (1)) · 등가 회로 R_b–(R_ct–W)∥CPE · XPS 봉우리 분리 (면적 % 글자) · 문헌 표 · 에너지 밀도 추정 (계산식 미인쇄).
- **안 한 것**: 오차 막대 · 셀 반복 통계 (표 S1 만) · 면적 정규화 R · 측정 온도 · 기공률 측정의 반복 · R_ct 숫자 · 300 사이클 유지율 · 섬유 굵기 · 길이 통계 · 바인더 덮임 정량 · 기계 (압착 · 캘린더 하중 · 두께 회복) · 입경.
- **이 카드의 후처리**: 화소 판독 225 행 (`digitized.csv`) · ΔV 두 정의 분리 · 1 C 유지율 재계산 · τ = ε·N_M 확인 · N_M ∝ R_ion/d 대조 · 골격 밀도 산술 · 두께 ↔ 부하 대조 · 표 S1 재계산 · GITT 전류 · 시간 산술 · 에너지 밀도 · CTP 산술 · 부피 용량 기준 대조.  스크립트 = 작업 스크래치 (`make_crops.py` · `make_csv.py`) — 값은 csv 와 이 카드에 있다.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · `docs/` 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 계 | 액체 LIB **LFP 양극** (LFP 97 · Super P 1 · 바인더 2 wt%) · 기공 38–40 % 에 **액체 전해질** | ASSB 복합 양극 NCM811 + LPSCl (+ VGCF · PTFE · SDCP) · 300 MPa 일축 · 순수 SE 10–13 % (랩 표준) · 복합 ≈15–16 % (real_14 15.6 % · CLAUDE.md) | **이온 길이 다르다** (액체가 찬 기공 ↔ 고체 SE 접촉망) · 압력 경로 다름 |
| 압력 | 미기재 (60 °C 압착 · 캘린더) | 300 MPa | 대응시킬 숫자 없음 |
| 바인더 | PTFE 섬유 (점 접촉 · BET 로 표면 노출) ↔ PVDF 막 (표면 덮음) | STEP3 PTFE = `centerline` 절연 스탬프 (CL-60 · 본문 규약) · PVDF 같은 막 표현 없음 | **섬유 쪽은 우리 규약과 같은 방향** (선 · 막 아님) [카드 추론] · 막 (덮임) 항은 우리에게 없다 |
| 수송 지표 | 기공 쪽 **tau2 8.80 (습식) · 1.66 (건식)** [판독] · N_M 22.3 · 4.34 | 우리 수송 tortuosity (tau2 · SE 상) ps45 Hertz 7.24–5.03 · Tabor 4.12–2.78 (CLAUDE.md 10-07 · 10-13) | **같은 이름 · 다른 상** — 수치 비교 금지 (τ 규약 표 · 'tortuosity factor' = τ² 만) |
| 구조 → 수송 | 같은 조성에서 바인더 형태 · 분포만으로 tau2 ×5.3 [판독 · 카드 산술] | STEP3 · 접촉망은 첨가제 표현 (PTFE 스탬프 · 격자) 에 σ 가 민감 (CL-49 PTFE 스탬프 σ_e −25 % · CL-60) | 방향 같음 (표현이 결과를 바꾼다) · 크기 전이 안 함 |
| 기계 | 없음 | DEM 18 배 연화 (E_eff 1.35 GPa · Heckel P_y 138 MPa) · MPM E 1.53 · σ_y 0.30 · ν 0.49 | 견줄 자리 없음 |

### 7-2. ★ 랩 기준과 나란히 (판정 없이 · **랩 표준과 다른 문헌 값 = 다른 재료 · 다른 공정**)
| 출처 | 재료 | 상태 | 진밀도 분모 | 기공 |
|---|---|---|---|---|
| **랩 표준** | 순수 LPSCl | 300 MPa | **1.64 g/cm³** (고정) | **10–13 %** |
| 이 논문 건식 (인쇄) | LFP 97 · Super P 1 · PTFE 2 wt% · 액체 LIB | 캘린더 뒤 2.3 g/cc · 하중 없음 | Hg 직접 (함의 골격 3.72 g/cm³ [카드 산술]) | **38.2 %** (S5 38.23) |
| 이 논문 습식 (인쇄) | LFP 97 · Super P 1 · PVDF 2 wt% | 캘린더 뒤 2.1 g/cc | Hg 직접 (함의 골격 3.47 g/cm³ [카드 산술]) | **39.5 %** (S5 39.46) |
- 이 표는 **"랩 표준과 다른 문헌 값"** 의 자리다 — 고체전해질이 없는 전극이고 압력 대응도 없다.  뜻을 가질 수 있는 것은 **기공 숫자와 명목 밀도가 같은 골격 밀도로 함께 맞지 않을 수 있다** 는 측정 규약 감각 (같은 조성인데 3.72 ↔ 3.47 g/cm³) 뿐이다.

### 7-3. ★ 18 배 연화 · 수송 tortuosity 해석과 견줄 자리 (frame [2])
- 우리 DEM 의 18 배 연화 (E_SE 24 → E_eff 1.35 GPa) · MPM 연화 (E 1.53 · ν 0.49) 는 **가압 기공**을 맞추는 대리다 — 이 논문은 기계 숫자를 주지 않아 그 연화를 검증 · 반증할 자리가 없다.
- 수송 쪽: 원문 τ (= ε·N_M) 는 우리 tau2 와 **같은 정의** 지만 **액체 기공 상** 이다.  우리 ps45 의 수송 tortuosity 73–75 % 가 SE–SE 접촉 협착이라는 결과 (CLAUDE.md 10-13) 와 달리, 액체 기공에는 접촉 협착이 없다 → 이 논문의 ×5.3 은 **기공 연결 · 막힘 (바인더 분포)** 의 몫이다 [카드 추론].  우리 SE 망에서 PTFE 가 SE–SE · AM–SE 접촉을 끊는 효과 (STEP3 PTFE 스탬프) 와 '바인더 분포 → tau2' 라는 축은 같지만 기전 (접촉 ↔ 기공 막힘) 이 다르다.

### 7-4. PTFE 규약 (STEP3) · 바인더 형태 — 이 논문이 더하는 한 줄
- 섬유화 PTFE 는 AM 표면을 **막처럼 덮지 않는다** (BET 11.9 ≈ LFP 11.6 · PVDF 9.5 m²/g · TEM) — 우리 STEP3 가 PTFE 를 `centerline` (선) 으로 찍고 '표면 코팅' 효과를 담지 않는 것 (CLAUDE.md §SR-01 · CL-49 의 '문헌 3,000 배 붕괴는 표면 코팅 효과') 과 같은 방향의 정성 근거 (액체 LIB LFP · 2 wt% · 측정은 분말).
- ⚠ 거꾸로, **PVDF 같은 막 바인더** (습식 · 표면 덮음) 가 들어간 계를 우리 모델로 그리면 덮임 항이 빠진다 — 우리 계 (건식 PTFE · 복합 양극) 에서는 해당 없음.
- 전위: PTFE 는 양극 전위 (LFP 2.0–4.2 V) 에서 미반응 (XPS CF₂ · XRD) — `han2024_fec_*` · `lee2025_pvp_*` 의 '음극 전위에서는 환원' 과 짝을 이룬다 (우리 CL-60 '불활성 절연' 은 양극 쪽에서 맞음).

### 7-5. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 같은 조성 · 같은 활물질에서 **공정 (바인더 형태 · 분포) → 기공 쪽 수송 (R_ion · N_M · τ) → 율속 · 후막 제조성** 의 실험 사슬 · 바인더 깊이 분포 관측량 (SAICAS) · 셀 5 + 5 산포 (표 S1).
- **없는 것**: 압력 · 응력 · 기계 · 입자 거동 · 계산 · 고체전해질.  ⇒ DEM · MPM 어느 반쪽의 **입력**도 아니고, 우리 STEP3 · 접촉망의 **첨가제 표현 규약** (PTFE = 선) 과 **수송 tortuosity 명명 · 비교 규약** 에 정성 근거를 하나 더한다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ (1) **기공 숫자와 명목 밀도가 같은 골격 밀도로 함께 맞지 않을 수 있다** — 같은 97 : 1 : 2 인데 Hg 38.2 % @ 2.3 g/cc ↔ 39.5 % @ 2.1 g/cc 가 골격 3.72 ↔ 3.47 g/cm³ 를 함축 [카드 산술] → 실험 기공을 판정 기준으로 등록할 때 **측정법 (Hg · 질량 · 단면) · 분모 (진밀도) · 시료** 를 같이 적는다 (2) 'ΔV' · 'τ' 처럼 **같은 이름 다른 양** — 결과 전 대조 항목에 정의 (CV 간격 ↔ 정전류 평탄 · tau2 ↔ tau) 를 박아 둔다 | SE · 압력별 기공 · 진밀도 (SE) |
| **단계 1 · 2 · 3** | 없음 (계산 없음) | — |
| **단계 4** (3D 순수 SE · σ_y 맞춤) | 없음 (SE 없음 · 기계 숫자 없음) | 값 · 재료 |
| **단계 5** (3D 복합 압밀) | 없음 — 액체 LIB 압연 전극 · 압력 미기재 (습식은 > 2.2 g/cc · > 5 mAh/cm² 에서 박리 = 정성) | — |
| **단계 6** (탈압 · 되돌아옴) | 없음 — 하중 · 두께 회복 미측정 | — |
| **단계 7** (형상 · 피복 · 수송) | ★ (1) **같은 조성에서 바인더 형태 · 분포만으로 기공 쪽 tau2 가 8.80 ↔ 1.66 (×5.3)** [판독] · R_ion 35.01 ↔ 6.19 Ω — '수송 tortuosity 는 기공률 · 조성만의 함수가 아니다' 의 실험 사례 (2) 원문 τ = ε·N_M = 우리 tau2 · N_M = 1/f (f 0.045 ↔ 0.230 [카드 산술]) — 수송 tortuosity 규약 표 (CLAUDE.md τ 명명) 의 Landesfeind 꼴 사례 하나 더 (3) BET · TEM: PTFE 섬유는 AM 표면 노출 (STEP3 `centerline` 규약과 같은 방향) | 액체 기공 상 (우리 = SE 상) · 그림 판독 · 식 미인쇄 · 셀 하나씩 |
| **후보 D0** (지금 DEM) | 없음 | DEM 언급 0 |
| **후보 A′-0 · A · A′** (MPM 접촉 · 강체 AM · 입자별 속도장) | 없음 | — |
| **후보 B** (입자별 FE) | 없음 | — |
| **후보 C · C′** (MDR · 항복 캡 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀) | 없음 (압력 없음) | — |
| **U0–U6** | 없음 | — |
| **R1–R6** | 없음 | — |
| **R7** (AM 파괴) | 사이클 뒤 습식 LFP 입자 균열 · 건식 없음 (그림 S10 · 정성 · 기전 = 인용 [42]) — **전기화학 사이클 균열** 이지 압밀 균열이 아니다 | 응력 · 하중 · 크기 없음 |
| **결과 전 대조 항목** | (흐름 밖 표지로만) 같은 조성 액체 LIB LFP 전극의 기공 쪽 tau2 8.80 / 1.66 · N_M 22.3 / 4.34 [판독] · R_ion 35.01 / 6.19 Ω · Hg 39.5 / 38.2 % — '액체 · LFP · 대칭 셀 · 판독' 표지 필수 | ASSB 절대값 비교 금지 |
| **흐름 밖: 믹서 (Ⓒ 코팅 활물질 믹싱)** | 건식 혼합 = 행성 혼합기 ARE-310 + 막자 (rpm · 시간 · 에너지 0 건) → 믹서 V2 앵커 불가 (`lee2026_li_*` · `han2024_*` 와 같은 꼴) | 공정 에너지 · 시간 |
| **흐름 밖: 첨가제 · 바인더 분포 (STEP3)** | SAICAS 깊이별 F_H = 바인더 깊이 분포 관측량 (습식 ≈12 % ↓ · 건식 균일) — 우리 침대는 바인더 깊이 분포를 균일로 두므로 건식 계와 맞는 가정 [카드 추론] | 깊이별 정량 · 정규화 기준 미기재 |

- **재료 · 차원 · 조건 차이**: 액체 LIB LFP ↔ 우리 ASSB NCM811 + LPSCl · 이온 길 = 액체가 찬 기공 ↔ SE 접촉망 · 기공 38–40 % ↔ 10–16 % · 압력 미상 ↔ 300 MPa · 1D 두께 방향 전기화학 ↔ 우리 3D 계산 · 측정 온도 미상.

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **'ΔV 0.22 V' 를 Kwon 2024 의 값으로 인용하지 않는다** — 원문에 인쇄된 0.22 V 는 없고, 같은 부하에서 습식 · 건식 CV 봉우리 간격 (0.83 ↔ 0.61 V) 의 차로만 나온다.  인용하려면 *"CV peak separation 0.83 V (wet) vs 0.61 V (dry) at 5.5 mAh cm⁻²"* 로 원값을 쓴다.
2. **수송 tortuosity 를 옮길 때는 τ = ε·N_M 꼴인지 막대 · 식으로 확인** — 이 논문은 식 없이 막대만 주지만 두 막대가 ε·N_M 을 정확히 만족해 tau2 꼴로 판정된다 (§3-5).  우리 tau2 와 '같은 정의 · 다른 상' 으로 표지한다.
3. **같은 조성 · 다른 공정 → tau2 ×5** — 우리 침대의 첨가제 (PTFE · 탄소) 표현 규약이 수송 결과를 바꿀 수 있다는 것을 문헌 쪽에서도 보인 사례.  STEP3 PTFE `centerline` 은 섬유화 PTFE 의 '표면을 덮지 않는' 형태와 같은 방향이다.
4. **본문 숫자는 그림과 대조한 뒤 인용** — 이 논문은 1 C 유지율 순서 · CV 주사 속도 · GITT 휴지 · XPS · XRD 위치가 본문과 그림 · 방법 사이에서 어긋난다 (§3-8).  인용 문장은 그림 판독과 맞는 쪽 + 어긋남 표지를 함께.
5. **GITT D 를 STEP4 D_s 앵커로 쓰지 않는다** — 2 상 LFP 평탄에서 ΔE_s 가 판독 분해능 근처 · 식 기호 오기 · 펄스 조건 불일치 (흐름 밖: STEP4 확산 계수).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "At the same composition (LFP : Super P : binder = 97 : 1 : 2 wt%) and areal capacity (5.5 mAh cm⁻²), a PTFE dry-processed LFP electrode (2.3 g cm⁻³) showed a symmetric-cell ionic resistance of 6.19 Ω versus 35.01 Ω for the PVDF slurry electrode (2.1 g cm⁻³) (Kwon et al., Small Sci. 4 (2024) 2300302, Fig. 5a)."
- "The CV peak separations were 0.83 V (wet) and 0.61 V (dry) — '26% lower' (Kwon et al. 2024, Fig. 4b); the often-quoted 0.22 V is their difference (our arithmetic), not a printed value."
- "Their MacMullin-number and tortuosity bars (Fig. 5c; ≈22.3 / 4.3 and ≈8.8 / 1.7, read from the figure) satisfy τ = ε·N_M, i.e. the tortuosity factor (our tau2) of the electrolyte-filled pores."
- 국문: *"같은 97 : 1 : 2 LFP 전극에서 PTFE 건식 공정이 PVDF 습식보다 기공 쪽 수송 tortuosity (tau2) 를 ≈8.8 → ≈1.7 [판독] 로 낮췄다 — 액체 LIB · 대칭 셀 · 그림 판독 (Kwon 2024)."*
- 국문 (금지 표지): *"Kwon 2024 를 '슬러리 로딩 증가 시 ΔV 최대 0.22 V' 의 근거로 인용하지 않는다 — 원문에 로딩 계열도 0.22 V 인쇄값도 없다."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **압력 · 공정 조건 미기재** — 막자 반죽 · 60 °C 압착 · 라미네이트 · 캘린더 하중 · 간극 · 통과 횟수 · 섬유화 조건 [미확인] → MPa 대응 불가.
2. **셀 하나씩 비교** — 그림 4–6 · S1–S12 는 셀 하나 (표 S1 만 5 + 5 셀) · 오차 막대 0.
3. **판독값이 핵심** — N_M · τ · R_ct · 정전류 ΔV · 율속 · 300 사이클 값은 원문 숫자 없음 (판독).
4. **1 C 유지율 순서 오류** (본문 89 / 80 % ↔ 그림 80.0 / 89.4 %).
5. **CV 주사 속도** 1 ↔ 0.1 mV/s · **GITT** 전류 · 휴지 ↔ 그림 · 전 구간 시간 불일치 · **SI 식 (1)** 기호 정의 뒤바뀜 · 2 상 평탄 GITT 적용성 미논의.
6. **XPS 689.9 eV ↔ 그림 ≈687.5 eV** · 패널 글자 · **XRD 18° ↔ ≈17.0°** · LFP 분말에도 같은 자리 봉우리.
7. **'ΔV 0.22 V' 는 원문에 없음** (CV 간격 차 = 카드 산술).
8. **골격 밀도 불일치** (Hg 기공 ↔ 명목 밀도 · 3.72 ↔ 3.47 g/cm³).
9. **부피 용량 376.8 mAh/cm³** 의 기준 ↔ 표 S3 (≈345 [카드 산술]) · **470 Wh/L 은 '고밀도 LFP' 가정 칸** · 에너지 밀도 계산식 · 셀 설계 미인쇄.
10. **'처음 보고'** ↔ 표 S2 [5] 건식 PTFE LFP (3.1 mAh/cm²).
11. **BET 시료** (전극 ↔ 분말) · SAICAS 정규화 기준 · '바닥' 깊이 미기재.
12. **기전은 정성 · 인용** — 점 접촉 · PVDF 덮임 · b 축 확산 · 균일 CEI · 삽입 응력 균열 모두 측정으로 가르지 않음 (LiF 몫 차 2.4 %p 로 R_ct 24 배를 설명).
13. **전셀 300 사이클 유지율 숫자 없음** — 판독 ≈61 % (첫 점) · ≈67 % (5 번째 점) · 2.4 mA/cm² (0.31 C) ↔ 방법 0.2 C.
14. 측정 온도 · 대칭 셀 전해질 · 면적 · R_ion 추출 모형 미기재.
15. ⚠ 이 카드의 판독은 원 래스터 (본문) · 300 dpi 렌더 (SI) 화소라 **[판독]** 표지로만 인용 · 골격 밀도 · 유지율 · 비용량은 **[카드 산술]** (식 병기).

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 32 | Y. Itou, N. Ogihara, S. Kawauchi, J. Phys. Chem. C 2020, 124, 5559. | R_ion 대칭 셀 방법의 출처 (서지 일부만 — 제목 미인쇄) | 없음 |
| 35 | P. Zhu, P. R. Slater, E. Kendrick, Mater. Des. 2022, 223, 111208. | N_M · τ 정의 출처 (τ 명명 규약 · J 축) | 없음 |
| 36 | M. S. Hossain, L. I. Stephens, M. Hatami, M. Ghavidel, D. Chhin, J. I. G. Dawkins, L. Savignac, J. Mauzeroll, S. B. Schougaard, ACS Appl. Energy Mater. 2020, 3, 440. | N_M · τ 정의 출처 | 없음 |
| 25 (= SI [1]) | A. Nickol, T. Schied, C. Heubner, M. Schneider, A. Michaelis, M. Bobeth, G. Cuniberti, J. Electrochem. Soc. 2020, 167, 090546. (SI [1] 은 제목까지 인쇄: *GITT analysis of lithium insertion cathodes for determining the lithium diffusion coefficient at low temperature: challenges and pitfalls*, Journal of The Electrochemical Society, 167 (2020) 090546.) | GITT 식 (1) 의 출처 · 적용 함정 (STEP4 D_s 인용 주의) | 없음 |
| 15 | W. Yao, M. Chouchane, W. Li, S. Bai, Z. Liu, L. Li, A. X. Chen, B. Sayahpour, R. Shimizu, G. Raghavendran, Energy Environ. Sci. 2023, 16, 1620. | 습식 후막 문제 · 건식 후막 (서지 일부만 — 제목 미인쇄) | 없음 |
| 43 | R. Morasch, J. Landesfeind, B. Suthar, H. A. Gasteiger, J. Electrochem. Soc. 2018, 165, A3459. | 바인더 구배 ↔ 차단 EIS τ (습식 바인더 이동의 결과) | `morasch2018_binder_gradient_impedance_tortuosity` |
| 22 | B. Son, M.-H. Ryou, J. Choi, T. Lee, H. K. Yu, J. H. Kim, Y. M. Lee, ACS Appl. Mater. Interfaces 2014, 6, 526. | SAICAS 깊이별 접착 방법 | 없음 (`bak2024_binder_distribution_multilayer` 가 SAICAS 사용) |
| 34 | S. Jaiser, M. Müller, M. Baunach, W. Bauer, P. Scharfer, W. Schabel, J. Power Sources 2016, 318, 210. | 건조 중 바인더 이동 (습식 기전의 출처) | 없음 (`lyu2025_3d_dem_drying_calendering_lib` · `morasch2018_binder_gradient_impedance_tortuosity` 가 인용) |
| 18 | J. Shin, J.-H. Lee, J. K. Seo, W. T. A. Ran, S. M. Hwang, Y.-J. Kim, Int. J. Energy Res. 2022, 46, 16061. | 건식 공정 세 단계 서술의 출처 | 없음 |
| 44 | M. Fichtner, Batteries Supercaps 2022, 5, e202100224. | CTP '+10–15 % · +50 %' 배수의 출처 | 없음 |
| SI [5] | Y. Zhang, S. Lu, F. Lou, Z. Yu, Solvent-free lithium iron phosphate cathode fabrication with fibrillation of polytetrafluoroethylene, Electrochimica Acta, 456 (2023) 142469. | 앞선 건식 PTFE LFP (3.1 mAh/cm²) — '처음 보고' 주장과 견줄 자료 | 없음 |

---

## [미확인] 목록
- LFP-NCO 입경 · 분포 · 탄소 코팅 · 형상.
- 혼합 rpm · 시간 · 막자 반죽 시간 · 섬유화 조건 · 60 °C 압착 하중 · 라미네이트 · 캘린더 하중 · 간극 · 온도 · 통과 횟수 → 압력.
- 7.8 mAh/cm² 전극의 두께 (부하 52 mg/cm² 는 표 S3).
- 대칭 셀 전해질 · 면적 · R_ion 추출 모형 · N_M · τ 의 식 (참고 [35] [36]).
- CV 주사 속도 (1 ↔ 0.1 mV/s) · GITT 펄스 전류 · 휴지 (인쇄 ↔ 그림) · EIS 주파수 범위 (인쇄 그대로).
- 첫 사이클 곡선 (그림 4a) 의 C-rate · 그림 4 · 5 · 6 의 셀이 표 S1 의 어느 셀인지.
- R_ct 숫자 · 측정 사이클 수 · 300 사이클 유지율.
- 전셀 흑연 음극의 부하 · 바인더 종류.
- 측정 온도.
- Hg 시료 상태 · 측정 범위 · 골격 밀도 불일치의 원인.
- BET 시료 (전극 ↔ 분말) · SAICAS 정규화 기준 · '바닥' 깊이.
- 에너지 밀도 계산식 · 셀 설계값 · '고밀도 LFP' 가정의 내용.
- `kang2026_*` L170 의 'ΔV 최대 0.22 V · 슬러리 로딩 증가' 가 Kang 원문 문장인지 카드의 풀어 쓰기인지 (Kang PDF 대조 필요).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-22)
- 서지: 1저자 메모 (K. Kwon … J. Choi · 제목 · Small Sci. 4 (5) (2024) 2300302) = 원문 첫 쪽 · 머리글 · 꼬리글 ('Small Sci. 2024, 4, 2300302' · '26884046, 2024, 5') 과 같음 · DOI `10.1002/smsc.202300302` = 첫 쪽 인쇄 · PDF 문서 정보 (Title · Subject 'Small Science 2024.4:2300302' · Author 11 명) 와도 같음 · **다른 점 없음**.
- 숫자: 텍스트 층 + 렌더 이미지로 대조 (지수의 '−' 는 렌더로 확인) — 97 : 1 : 2 · 2.1 · 2.3 g/cc · 190 · 175 µm · 20 µm · 60 · 100 °C · Mw 1 100 000 · > 99.7 % · 5.5 mAh/cm² · 35 mg/cm² · −50 °C · 1.15 M · 2 : 4 : 4 · 1 wt% · 1.0 T · 0.05 · 0.1 C · 1 C = 5.5 mAh/cm² · 0.1–1 C · 0.1 mV/s · 2.8–4.0 V · 250 kHZ–10 MHz · 5 mV · 0.1 mA/cm² · 10 · 30 min · 2.0–4.2 V · 96 : 1 : 3 · N/P 1.1 · 2.5–4.0 V · 0.2 C · 1–1 MHz · 10 mV · 1 mm · 45° · 20° · 10° · 11.6 · 9.5 · 11.9 m²/g · 30 µm · 12 % · 1 mV/s · 26 % · 0.83 · 1.35 · 1.06 × 10⁻¹¹ · 27.3 % · 89 · 80 % · 83 % · 38.2 · 39.5 % (S5 38.23 · 39.46) · > 2.2 g/cc · > 5 mAh/cm² · 0.02–0.1 · 0.02–0.3 µm · 687.8 · 689.9 eV · 18° · 4 mAh/cm² · 75 % · 7.8 mAh/cm² · 2.4 mA/cm² · 300 사이클 · ≈3 mAh/cm² · ≈2.1 g/cc · 370 mAh/cm³ · 5.0 mAh/cm² · 153 · 390 · 185 · 470 · 213 · 705 · 10–15 % · 50 % · 78 % · 10⁻⁶–10⁻¹⁰ S/cm · 3.2 V · ≈170 mAh/g · 270 °C · 17 000 · 7.2 million · 30 % · 140 million · 그림 안 글자 (3.87 · 3.04 · 3.75 · 3.14 V · 35.01 · 6.19 Ω · 표 39.5 · 38.2 · 43.5 · 56.5 · 45.9 · 54.1 % · 1.06 · 1.35 × 10⁻¹¹) · 표 S1 100 값 · 표 S2 50 값 · 표 S3 13 값 — 전부 위치 확인.
- 판독: 본문 그림 = 원 래스터 (xref 64 · 94 · 110 · 124) 화소 · SI 그림 = 300 dpi 렌더 · 축 = 틀 직선 · 눈금 · 판독 검산 = 그림 4b 글자로 계산한 26.5 % ↔ 본문 26 % · τ = ε·N_M (두 막대) · N_M 비 ↔ R_ion·d 비 · 그림 S2 · 표 S1 평균 수준 일치.
- 원문 전수 검색 ('0.22' · 'loading' 계열): 본문 · SI 텍스트 층에 '0.22' 없음 (표 S2 의 '0.83' 은 참고 [3] 의 면적 용량) · 습식 전극의 부하 계열 없음.
- 정본 중복 확인: papers/ 목록 · DOI · '2300302' · 'Low-resistance LiFePO4' · 'kwon' grep — 카드 없음 (kang2026 · kim2026 · han2024 · lee2025_pvp 가 인용만).

## 🔗 관련 카드
- 이 논문을 인용한 카드: `kang2026_multiscale_inverse_design_ptfe_fibrillation_dry_electrode` (참고 [40] · L386 · ★ L170 'ΔV 0.22 V' — §0-1 대조) · `kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation` (참고 [23] · L414) · `han2024_fec_mitigates_ptfe_decomposition_dry_thick_graphite_anode` (참고 [15] · L343) · `lee2025_pvp_ptfe_binary_binder_dry_thick_graphite_anode` (참고 [35] · L348).
- 이 논문이 인용한 정본 카드: `morasch2018_binder_gradient_impedance_tortuosity` ([43]).
- ★ 같은 랩 · 같은 해 (공저자 겹침): `han2024_fec_mitigates_ptfe_decomposition_dry_thick_graphite_anode` (건식 흑연 음극 · K. Kwon · S. Han 공저 · 같은 과제 20024261 · 전셀 LFP = 94 : 3 : 3 — 이 논문 97 : 1 : 2 와 다른 조성) · 같은 랩: `lee2025_pvp_*` · `lee2026_li_underlayer_primer_free_dry_prelithiated_thick_anode` · `kim2026_pregranulation_*` · `kang2026_multiscale_*`.
- 건식 PTFE 공정: `hippauf2019_dry_film_ptfe_sulfide_cathode_sheet` · `lee2025_dual_fibrous_ptfe_dry_electrode` · `lee2025_corolling_dryprocess_lpscl_ptfe` · `lee2026_unveiling_ptfe_dry_electrode_digital_twin` · `kang2025_bollard_anchored_binder_dry_electrode` · `lee2024_shear_force_dry_process_cathode_coverage` · `liu2025_dry_processing_high_energy_li_batteries_review` · `mun2025_dry_electrode_technology_assb_review`.
- PTFE 섬유 형태 · 전기화학 안정성 (이 논문 = 양극 전위에서 PTFE 미반응 · 사이클 뒤 섬유 남음): `matthews2024_ptfe_nanofibril_network` (PTFE 나노 섬유 망 SEM) · `schmitt2026_chemomech_stability_dry_cathode_separator_sheets` (황화물 ASSB · 양극 시트) · `han2024_fec_*` (음극 전위에서는 PTFE 환원 분해).
- 기공 쪽 수송 tortuosity (대칭 셀 · τ 규약): `landesfeind2016_tortuosity_eis_electrodes_separators` · `malifarge2017_tortuosity_symmetric_cell_impedance_tlm` · `nguyen2020_electrode_tortuosity_factor` · `morasch2018_*`.
- LFP 후막 · 입경: `noh2026_pedotpss_peg_swcnt_binder_ultrahigh_loading_lfp` · `eizenhammer2026_lfp_psd_halfcell_many_particle_fullcell`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     꼴 = kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md (같은 그룹 · 같은 해 · 이 논문 ref [17] · 이온 수송 계산의 원판) ·
     곁 = sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps.md (이 논문을 ref 24 로 인용 · 고른 의도의 출처) ·
     heck2026_densification_sulfide_se_binder_scalable.md (ref 61 · CL-90 '같은 권' 표지).
     쪽 표기 = 학술지 논문 번호 228437 의 쪽 p.1–10 (PDF 쪽 = 인쇄 쪽).  보충 자료 (SI) 는 원문에 안내가 없다 (본문 10 쪽 텍스트 층 전수에 'supplementary' 0 회).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 146 행 · 300 dpi 원 래스터의
     눈금 선 픽셀 위치로 환산 — 방법은 그 파일의 note 칸) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 추론] · [카드 해석] = 이 카드의
     해석 · [다른 카드] = 정본의 다른 카드에 적힌 값 (slug · 줄 병기) · [우리] = 우리 쪽 값 (CLAUDE.md 출처) · [미확인] = 원문 (본문 10 쪽 전수) 에 없음.
     원문 10 쪽은 전부 렌더 이미지로 읽었고 숫자는 텍스트 층 (PyMuPDF) 과 대조했다. -->
# 복합 전극 안 응력 분포가 황화물 SE 이온 수송을 정한다 — LGPS (Li₁₀GeP₂S₁₂) + ZrO₂ (활물질 대리 · E 200 GPa) 복합체를 100 MPa 누른 채 X 선 CT (복셀 4 × 4 × 5 µm) → GPU 복셀 FEM (선형 탄성 · 추가 100 MPa · 빈틈 0) → 복셀마다 최소 주응력 (MPS) 으로 순수 LGPS σ(P) 곡선을 읽어 넣은 전도 계산 · SE 평균 MPS 87.7 → 48.9 MPa (ZrO₂ 19 → 67 vol% [판독]) · 42 vol% 에서 SE 평균 66 · 최빈 69 MPa [인쇄] ↔ ZrO₂ 평균 ≈153 MPa [판독] · 응력 무시 (Case 1) 계산 ÷ 실측 1.72–4.71 → 응력 반영 (Case 2 · 3) 0.67–1.66 (오차 막대 = E_SE 0.3 ↔ 21.7 GPa) — Ohashi · Kodama · Sun · Hori · Suzuki · Kanno · Hirai (J. Power Sources 2020)

> slug `ohashi2020_stress_distribution_composite_electrode_sulfide_assb` · DOI `10.1016/j.jpowsour.2020.228437` · type `experiment + image-based voxel FEM (linear-elastic stress, VOXELCON GPU, bonded continuum, void-free) + stress-mapped voxel conduction (pure-SE sigma(P) curve per voxel) — LGPS + ZrO2 (AM stand-in) composite under 100 MPa · no DEM / MPM / contact law / compaction history / unloading` · PDF `Stress_distribution_in_the_composite_electrodes_of_sulfide_all-solid-state_lithium-ion_batteries.pdf` · digested `2026-11-17` · status ✅
>
> **저자**: Akinari Ohashi ᵃ · **Manabu Kodama\*** ᵃ (교신) · Sun Xueying ᵇ · Satoshi Hori ᶜ · Kota Suzuki ᵇ · Ryoji Kanno ᶜ · Shuichiro Hirai ᵃ — ᵃ School of Engineering, Tokyo Institute of Technology (Meguro, Tokyo) · ᵇ School of Materials and Chemical Technology, Tokyo Tech (Nagatsuta, Yokohama) · ᶜ Institute of Innovative Research, Tokyo Tech (Nagatsuta, Yokohama) · *J. Power Sources* **470** (2020) **228437** (본문 10 쪽 · SI 안내 없음) · 접수 2020-03-24 · 수정 05-08 · 승인 06-03 · 온라인 06-14 · 연구비 Japan Keirin Autorace Foundation (일부) · R.K. 는 Grant-in-Aid for Scientific Research (S, no. 17H06145) · *"We thank Quint Corporation for support with voxel-FEM stress analysis"* (p.9) · 기여: Ohashi = 방법 · 소프트웨어 · 초고 / Kodama = 개념 · 소프트웨어 · 검토 · 검증 / Sun = 자원 · 검토 / Hori = 자원 · 검토 · 과제 관리 / Suzuki · Kanno = 검토 / Hirai = 과제 관리 (p.9).  ⚠ 공저자 이름 표기: 머리글은 **"Sun Xueying"** — sakka2022 는 "X. Y. Sun", heck2026 은 "S. Xueying" 로 옮겼다 (둘 다 그 논문들의 원문 그대로 · 카드 문제 아님).
> **이웃 카드 (링크만)**: [`kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation`](kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation.md) (이 논문 ref [17] = 같은 그룹 · 기밀 셀 · 이온 수송 계산 절차의 원판 · *"reduction of voids … already discussed in the previous study [17]"*) · [`sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps`](sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps.md) (이 논문을 ref 24 로 · §0-1) · [`heck2026_densification_sulfide_se_binder_scalable`](heck2026_densification_sulfide_se_binder_scalable.md) (ref 61 · CL-90 표지 · §3-6) · [`deng2016_elastic_superionic_electrolytes_dft`](deng2016_elastic_superionic_electrolytes_dft.md) (이 논문 [23] — LGPS 21.7 GPa · ν 0.37) · [`kamaya2011_lgps_lithium_superionic_conductor`](kamaya2011_lgps_lithium_superionic_conductor.md) ([5]) · [`sakuda2013_sulfide_mechanical_property`](sakuda2013_sulfide_mechanical_property.md) ([16]) · [`koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb`](koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb.md) ([14]) · [`hlushkou2018_void_space_ion_transport_assb_cathode`](hlushkou2018_void_space_ion_transport_assb_cathode.md) ([9]) · [`froboese2019_microstructure_ionic_conductivity_assb_electrode`](froboese2019_microstructure_ionic_conductivity_assb_electrode.md) ([10]) · [`bielefeld2020_effective_ionic_conductivity_binder`](bielefeld2020_effective_ionic_conductivity_binder.md) ([28]) · [`kato2018_thick_electrode_assb_cycle_tortuosity`](kato2018_thick_electrode_assb_cycle_tortuosity.md) ([6]) · [`yano2024_eepa_binary_mixture_plasticity_compression_dem`](yano2024_eepa_binary_mixture_plasticity_compression_dem.md) (강성이 다른 두 성분 압축 — 하중 몫은 안 잼 · 이 논문이 그 빈칸의 연속체 값).
> **판독 원자료**: `litdb/figures/ohashi2020_stress_distribution_composite_electrode_sulfide_assb/digitized.csv` (146 행 — Fig 5 본 곡선 26 · 삽도 27 · Fig 6a 두 히스토그램 67 + 통계 10 · Fig 6b 4 · Fig 7 막대 12) · 크롭 **45 장** (도구 9 중 그대로 5 · 다시 자름 4 = Fig 2 · 7 · 8 · 표 1 / 손 크롭 36 = 패널 15 · 식 2 · 근거 문단 19) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 활물질 대신 영률이 비슷하다는 **ZrO₂ (200 GPa · 전기화학 반응 없음)** 를 LGPS 분말 (< 40 µm) 에 19 · 42 · 55 · 67 vol% 섞어 지름 1 mm 셀에서 **100 MPa 로 누른 채** DC 로 σ 를 재고, 같은 상태의 X 선 CT (복셀 4 × 4 × 5 µm) 를 그대로 격자로 삼아 **선형 탄성 복셀 FEM** (VOXELCON · GPU · ≈300 × 300 × 400 복셀 · SE 를 빈틈 없는 연속체로 · E_SE 21.7 GPa (DFT) 와 0.3 GPa (압분체) 두 극단) 으로 응력을 푼 뒤, SE 복셀마다 그 자리 응력으로 **순수 LGPS 의 σ(P) 곡선**을 읽어 넣어 전도를 풀면 — 응력을 무시한 계산 (Case 1) 이 실측을 **1.72–4.71 배** 넘던 것이 **0.67–1.66 배** 로 줄어든다 [판독 Fig 7].  **단단한 상이 하중을 더 진다** 는 것은 연속체 계산값으로 있다 (SE 평균 MPS 가 인가 100 MPa 의 0.88 → 0.49 · ZrO₂ 는 인가압 위) — **NCM · AM–SE 접촉 · 기공 · 압밀 · 탈압은 없다**.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 단단한 입자 (AM) 의 하중 몫 (R1) | ★ **SE 평균 MPS 87.7 · 66.0 · 60.9 · 48.9 MPa** (ZrO₂ 19 · 42 · 55 · 67 vol% · 인가 100 MPa · E_SE 21.7 GPa) · 42 vol%: SE *"average and mode … approximately 66 and 69 MPa"* · ZrO₂ 최빈 ≈128 · 평균 ≈153 MPa · 67 vol%: SE *"approximately 50 MPa"* → 평균 응력 정리로 ZrO₂ 축하중 몫 **≥ 0.29 · 0.62 · 0.73 · 0.84** | [판독] Fig 6b · 6a · [인쇄] p.6 · [카드 산술] §3-3 |
| ② 그 계산의 정체 | **선형 탄성 · 완전 결합 (접촉 없음) · 빈틈 0 · 등방** 복셀 FEM — Hooke 법칙 Galerkin · 한쪽 고정 / 반대쪽 100 MPa / 옆면 미끄럼 (roller) + 양쪽 가상 강판 · CT (이미 100 MPa 로 눌린 형상) 에 **추가 100 MPa** 를 선형으로 건다 · 소성 · 압밀 이력 · 잔류 응력 · 탈압 없음 | [인쇄] p.3 · 그림 3 |
| ③ 순수 SE 의 압력별 σ · 기공 | 순수 LGPS σ(P) **0.02 (0.6) → 0.43 (8.4) → 1.17 (100) → 1.40 mS/cm (≈129 MPa)** — 가압 가지만 · 기공률 · 상대밀도 · 진밀도 **없음** | [판독] Fig 5 · [미확인] |
| ④ 복합체 기공 · 접촉 | **없음** — CT 에서 빈틈은 보이지 않아 고체로 셌고 (*"treated as void-free"*), 'volume fraction' = ZrO₂ 부피만 · AM–SE 접촉 면적 · 개구 계산 없음 | [인쇄] p.3 · p.6 |
| ⑤ 복합체 σ (실측) | 숫자 없음 — 그림 7 은 **계산 ÷ 실측** 만 · 실측 복합체 ÷ 순수 SE 비는 Wiener 상한으로 **≤ 0.47 · 0.33 · 0.096 · 0.079** [카드 산술] | [미확인] · §3-4 |
| ⑥ 하중을 뺀 뒤 | **없음** (가압 · 100 MPa 측정만) | [미확인] |
| ⑦ DEM 한계 · 소성의 어려움 | DEM 을 쓰지 않음 (말 없음) · 소성 대신 **E 두 극단** 으로 오차 막대 · *"Non-linear stress analysis is necessary to minimize the margin of error"* · *"it is impossible to determine whether the isotropic (Case 2) or anisotropic (Case 3) model is more accurate because of the large margin of error"* | [인쇄] p.3 · p.9 |
| ⑧ CL-90 ('Wang 2020, JPS 470' 의 NCM 경도 · NCM 140 GPa · LPSCl 24 GPa) | **이 논문에 셋 다 없다** — 입력은 LGPS 21.7 / 0.3 GPa · ν 0.37 · ZrO₂ 200.0 GPa · ν 0.30 (표 1) 뿐 · NCM 은 *"LCO, Si, and NMC [18]"* 한 문장 · 참고문헌의 'Wang' = [23] 2 저자 · [26] Z.Q. Wang 2014 (LGPS DFT) | [인쇄] p.2 · 표 1 · p.10 · §3-6 |

⛔ **한정어 (떼지 말 것)**: ① 재료 = **LGPS + ZrO₂** (NCM · LPSCl 없음 · ZrO₂ 는 활물질 *대리*) ② 압력 = **100 MPa 한 점** (계산 · 복합체 측정 둘 다) — 순수 SE σ(P) 만 0–≈129 MPa ③ 응력 = **선형 탄성 · 결합 연속체 · 빈틈 0** (응력 비가 인가압에 무관하다는 꼴 — 실제 압밀은 비선형) ④ ZrO₂ 입경 < 150 µm · LGPS < 40 µm · 복셀 4 × 4 × 5 µm (LGPS 입자 · 빈틈은 안 풀린다) ⑤ 그림 7 은 **비 (계산 ÷ 실측)** — 복합체 σ 실측값 [미확인] ⑥ 오차 막대 = E_SE 0.3 ↔ 21.7 GPa 두 계산 (반복 측정이 아니다) · 막대 폭 (위 끝 ÷ 아래 끝) ×1.3–11.6 ⑦ 원문 안 어긋남 셋 (§3-7): 그림 6a 히스토그램 넓이 비 (ZrO₂ 0.69) ↔ 42 vol% · 본문 '최빈 69 MPa' ↔ 그림 봉우리 61–63 MPa · 그림 5 삽도로 낸 σ (≈0.6) ↔ 본 곡선 (1.17 mS/cm @100 MPa).
⇒ **절대값 전이**: 하지 않는다 (재료 · 상 · 압력 · 모델 모두 다르다).  옮길 수 있는 것 = **꼴과 방법** — (i) 강성이 다른 두 상을 결합 연속체로 누르면 SE 평균 응력이 인가압 아래로 (ZrO₂ 42 vol% 에서 0.66 배) 내려가고 그 몫은 단단한 상 부피 분율과 함께 커진다 (ii) 기하만 넣은 복셀 σ (= 우리 STEP3 의 꼴) 가 단단한 상이 많은 복합체에서 실측을 1.7–4.7 배 넘을 수 있다 (iii) 국소 응력 → σ 를 순수 SE σ(P) 로 잇는 방법 · 그 불확도는 E_SE 선택이 지배한다.

---

## 0-1. ★ 고른 의도 대조 (위시 11-17 · sakka2022 n 줄 + 본 세션 의도 넷)

의도 원문 (wishlist 원문 그대로): *"[n] A. Ohashi, M. Kodama, X. Y. Sun, S. Hori, K. Suzuki, R. Kanno and S. Hirai, J. Power Sources, 2020, 470, 228437. | d · i — "the NCM particles are pressurised preferentially" · "strain caused by the pressure reduces the contact between the AM and SE" 의 근거 · 카드 §12 ref 24"*.  본 세션이 덧붙인 의도 = ① AM 하중 몫 (AM · SE 응력 평균 · 분포 · 비 · 모델 · 경계 조건 · 해상도 · 입력 물성) ② CL-90 단서 ③ [DEM 우선 (수영)] 재설계 (가압 → 탈압 한 모델) ④ 기공 · 접촉 감소의 정량과 측정 조건.

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| (d) *"the NCM particles are pressurised preferentially"* (Sakka 2022 의 문장 · ref 24 = 이 논문) | **일부** | 단단한 상이 더 눌린다는 것은 **계산값으로 있다**: 42 vol% 에서 ZrO₂ MPS 가 인가압 위 (*"zirconia will experience stress higher than what was applied"* p.6) · 판독 최빈 ≈128 · 평균 ≈153 MPa ↔ SE 평균 66 · 최빈 69 MPa [인쇄] (Fig 6a · p.6) · 조건 = 선형 탄성 복셀 FEM · 인가 100 MPa · **누른 채** CT 형상 · 온도 무관 (탄성).  **그러나 NCM 은 없다** — 계산 · 실험 재료는 ZrO₂ (활물질 대리) 이고 NCM 은 저자의 외삽 문장뿐: *"If this phenomenon is extended to an actual electrode of SASLIB, when active materials with high Young's modulus such as LCO, NMC, Si is present, stress experienced by SSE decreases and stress experienced by active material increases"* (p.6) · 결론 1) 의 *"(such as LCO, Si, NMC)"* (p.9).  ZrO₂ ≈ AM 영률의 근거 [18] 은 **LCO** 논문 하나 (Cheng 2017, J. Asian Ceram. Soc.) |
| (i) *"strain caused by the pressure reduces the contact between the AM and SE"* (Sakka 2022 서론 · refs 18 · 24 를 함께 단 문장) | **없음** | 이 논문은 AM (ZrO₂)–SE 접촉 면적 · 개구 · 변형률을 재지도 계산하지도 않는다 — FEM 은 **결합 연속체** (상 경계가 붙어 있음 · 접촉 · 분리 없음) [카드 추론 · 복셀 FEM 이 절점을 공유] · 원문의 기전은 **SE 안** 의 빈틈 · 입계: *"The decrease in stress/pressure leads to an increase in voids and thereby grain-boundary resistance"* (p.9).  'particle contact area' 는 가릴 수 없는 나노 특징 후보로만 나온다: *"Currently it is not possible to discuss which nanoscale features, such as void content, tortuosity, or particle contact area, is the dominant factor affecting ion transport in local regions"* (p.9).  ⇒ Sakka 문장의 이 부분은 ref 18 (Fathiannasab 2021) 쪽 근거일 수 있다 [카드 추론 · Fathiannasab 원문 미확인] |
| sakka2022 카드 L363 (ref 24 행 · 서지 + 두 문장) | **서지 채움 · 귀속 일부** | 서지 "A. Ohashi, M. Kodama, X. Y. Sun, S. Hori, K. Suzuki, R. Kanno and S. Hirai, J. Power Sources, 2020, 470, 228437." = 원문 머리글 (저자 7 · 순서 · 권 · 번호 같음).  두 문장 가운데 둘째는 Sakka 원문이 **refs 18 · 24** 를 함께 단 문장이다 (`sakka2022_…/txt_p1_p2_fabrication_vs_stack_pressure.png`) — L363 은 24 만 적었지만 L365 (ref 18 행) 에 같은 내용이 있어 두 행을 같이 읽으면 원문 그대로 → **카드 문제 아님** · Sakka 원문의 인용 범위 문제 (Ohashi 원문에 AM–SE 접촉 감소 내용이 없다) |
| sakka2022 카드 L136 (Sakka p.4 해석 *"… pressurised preferentially (ref 24), and so contact with the surrounding LGPS is not increased"*) | **일부** | 앞 절반 ('단단한 입자가 먼저 눌린다') = 이 논문의 ZrO₂ 계산과 같은 방향 · 뒤 절반 ('그래서 둘레 LGPS 와 접촉이 늘지 않는다') = **이 논문에 없음**.  카드는 Sakka 원문을 그대로 옮겼다 (카드 문제 아님) |
| heck2026 카드 L305 (ref 61 · "복합 전극 응력 분포 (강성 높은 상으로 응력 집중)") | **채움** | 서지 (S. Xueying 표기 포함) = 원문과 같음 · 'stress concentrates on a high Young's modulus material' (Highlights · p.1).  L305 의 *"CL-90 … 그 인용이 이 논문을 잘못 기억한 것인지는 [미확인]"* → 아래 ② 줄로 답한다 |
| 가리킨 카드의 **2 차 인용 값** | **해당 없음** | sakka2022 · heck2026 · kodama2020 세 카드 모두 이 논문에서 **숫자를 옮기지 않았다** (서지 · 문장 · 주제 표기뿐) |
| ① AM 하중 몫 — AM · SE 응력 (평균 · 분포 · 비) · 압력별 | **채움 (한 압력 · 연속체 · 대리 재료)** | 압력 = 100 MPa 한 점 (선형이라 비는 압력 무관) · SE 평균 MPS 87.7 / 66.0 / 60.9 / 48.9 MPa (Fig 6b · E_SE 21.7 GPa [판독]) · 42 vol% 분포 = Fig 6a (SE 봉우리 61.6 · 평균 68.4 · 중앙 65.6 MPa · ZrO₂ 봉우리 127.9 · 평균 153.0 · 중앙 145.6 MPa [판독 · 카드 산술]) · 비 ZrO₂ / SE 평균 ≈2.2–2.3 [카드 산술] · E_SE 0.3 GPa 계산의 응력 분포는 **그림이 없다** (그림 7 오차 막대 끝으로만) |
| ① 모델 · 경계 조건 · 해상도 · 입력 물성 (출처) | **채움** | 복셀 FEM VOXELCON [22] (감사의 글에 Quint Corporation — 제작사 표기는 원문에 없음) · Galerkin · 선형 탄성 · GPU · ≈300 × 300 × 400 복셀 · 4 × 4 × 5 µm (≈1.2 × 1.2 × 2.0 mm [카드 산술]) · 빈틈 0 · BC = 고정 / 100 MPa / roller + 가상 강판 (그림 3) · 표 1: LGPS E 21.7 GPa (*"first-principle calculation [23]"* = Deng 2016) · 0.3 GPa (*"obtained experimentally for a compressed powder by considering total strain and applied stress"* — 출처 인용 없음) · ν 0.37 · ZrO₂ E 200.0 · ν 0.30 (**출처 없음**) · 요소 종류 · 풀이기 · 수렴 · 시간 · 메모리 [미확인] |
| ② CL-90 — NCM 경도 · NCM E 140 GPa · LPSCl E 24 GPa 가 입력인가 | **없음 (셋 다)** | 본문 · 표 · 그림 · 참고문헌 10 쪽 전수: 'hardness' 0 회 · 'NCM' 0 회 · 'NMC' 3 회 (모두 '고영률 활물질의 예' 문장 · 값 없음) · 'LPSCl' · 'Li6PS5' · 'argyrodite' 0 회 · '140' 은 참고문헌 [2] 의 논문 번호 '1401408' 안에만 · '24 GPa' 0 회.  가까운 값 = LGPS **21.7 GPa** (← [23] Z. Deng, **Z. Wang**, I.-H. Chu, J. Luo, S.P. Ong, J. Electrochem. Soc. 163 (2016) A67 — 정본 deng2016 Table III 의 LGPS 21.7 · ν 0.37 과 같다 [다른 카드]).  참고문헌에서 'Wang' 이 든 것은 [23] (2 저자) 과 [26] (Z.Q. Wang … C.Y. Ouyang, Int. J. electrochem. Sci. 9 (2014) 562–568 · LGPS 탄성 DFT) 둘 — **둘 다 2020 · J. Power Sources 가 아니다**.  ⇒ CL-90 의 'Wang 2020, J. Power Sources 470' (작업 지시의 논문 번호 228413) 을 이 논문으로 메울 근거가 **없다** — 같은 권이라는 것만 같다 (추측으로 잇지 않는다) |
| ③ [DEM 우선 (수영)] — 가압부터 탈압까지 한 모델 | **일부 (보여 주는 것) · 없음 (요구)** | 보여 주는 것: 실측 CT 를 격자로 한 **3D 미시 응력장** 을 GPU 로 한 번에 푼다 · 그 응력을 국소 σ 로 바꿔 수송까지 잇는다 (기계 → 수송 한 방향 결합).  요구 (한 모델로 가압 → 탈압) 는 **없다**: 압밀 이력 · 형상 변화 · 빈틈 닫힘 · AM 이동 · 접촉 미끄럼 · 분리 · 탈압 · 되돌아옴 모두 없음 (선형 증분 한 번) |
| ④ 기공 · 접촉 감소의 정량 · 측정 조건 | **없음** | 복합체 · 순수 SE 모두 기공 숫자 없음 · 접촉 면적 숫자 없음 · 가정만: *"We initially assume that the void ratio of the SSE is solely dependent on stress"* (p.6–7) · 조건 = 복합체 σ 는 **누른 채 100 MPa DC** (≈0.1 mA/cm²) · 순수 SE σ(P) 는 **누른 채 가압 가지** · 뺀 뒤 값 0 |

⇒ **의도 대조 결과: 일부** — 단단한 상 (ZrO₂ 대리) 이 더 눌리고 SE 응력이 인가압 아래로 내려간다는 **연속체 계산값** 과 모델 · 입력 · 경계 조건은 **있다**; NCM · AM–SE 접촉 감소 · 기공 · 탈압은 **없다**; CL-90 의 세 값은 **없다**.

---

## 1. 한 줄 요약
복합 전극을 누르면 영률이 다른 상 사이에 응력이 고르지 않게 퍼진다는 가설 (p.2) 을, 활물질을 전기화학적으로 안정한 ZrO₂ 로 바꾼 'zirconia composite' 로 시험한다 — 100 MPa 에서 잰 복합체 σ (DC) 는 ZrO₂ 부피 분율과 굴곡 (기하) 만으로 예상한 것보다 크게 떨어지는데 (Case 1 계산 ÷ 실측 1.7–4.7 [판독]), CT 형상 위 선형 탄성 복셀 FEM 으로 구한 국소 응력 (ZrO₂ 가 하중을 받쳐 SE 응력이 인가압보다 낮다) 을 순수 SE 의 σ(P) 곡선으로 국소 σ 에 넣으면 그 차이가 '오차 범위 안' 으로 줄어든다 (0.67–1.66 · 막대 = E_SE 0.3 ↔ 21.7 GPa) — 저자 결론: 응력 분포를 넣는 것은 보이지 않는 나노 특징 (빈틈 · 입계 · 굴곡) 을 넣는 것과 같다 (p.7 · p.9).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| A. Ohashi · M. Kodama\* · Sun Xueying · S. Hori · K. Suzuki · R. Kanno · S. Hirai (Tokyo Tech) | J. Power Sources 470 (2020) 228437 · 10 쪽 | 10.1016/j.jpowsour.2020.228437 | SE = **LGPS** (Li₁₀GeP₂S₁₂ · 이전 보고 [5] 대로 합성 · < 40 µm) · '활물질' = **ZrO₂** (Toray · < 150 µm · 19 · 42 (41) · 55 · 67 vol%) · 전극 = Li 금속 0.3 mm 양쪽 · **CAM · 탄소 · 바인더 없음** | 실험 (100 MPa DC · CT · 순수 SE σ(P)) + 영상 기반 계산 (선형 탄성 복셀 FEM + 응력 → σ 복셀 전도) — DEM · MPM · 압밀 계산 없음 |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 재료 · 셀 · 측정 상수 (p.2–3)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| SE | LGPS — *"prepared as explained in the previous study"* ([5] Kamaya 2011) · 입경 **< 40 µm** (SEM 그림 1 · 40 µm 막대) | [인쇄] p.2 · 그림 1 |
| 활물질 대리 | ZrO₂ (Toray) · **< 150 µm** (그림 1 · 1 mm 막대) · *"the Young's modulus of zirconia is almost the same as that of common active materials such as LCO, Si, and NMC [18]"* | [인쇄] p.2 |
| 조성 | ZrO₂ **19 · 42 · 55 · 67 vol%** (그림 7 · 6b) · 그림 2b · 본문 p.3 은 같은 시료를 **41 vol%** 로 · 부피 분율 = ZrO₂ 부피만 (*"The voids present in the SSE are not included in the volume fraction"* p.6) · 분율을 낸 방법 (CT 셈? 무게?) | [인쇄] · [미확인] |
| 셀 | 안지름 **1 mm** · 복합체 *"about 1~2 mm thickness"* · 양 끝 Li 금속 **0.3 mm** · 스테인리스 봉 (그림 2a) · 기밀 + 제습 · 원통 재료 · 하중 장치 · 하중 측정 | [인쇄] p.2 · [미확인] |
| 복합체 σ 측정 | **DC** · **100 MPa** · 전류 밀도 *"approximately 0.1 mA/cm2"* · 조립 직후 짧게 (LGPS/Li 불안정 계면 [19]) · 두께 = 셀 안 CT · 식 (1) σ = (1/R)(t/A) | [인쇄] p.2 |
| 순수 SE 기준 시료 | 같은 측정 · 두께 다른 둘 (그림 5 삽도 **t = 2.7 mm · 0.8 mm**) 의 저항 차로 Li/SE 계면 저항을 빼 *"the pressure dependence of LGPS/SE interface was negligible"* (p.3) | [인쇄] p.2–3 · 그림 5 |
| CT | 실험실 · **160 kV 텅스텐 표적** · **복셀 4 × 4 × 5 µm** [20, 21] · CT 압력 = 100 MPa (*"Stress was analyzed for the visualized composite under a pressure of 100 MPa"* p.3 = 누른 채) · 투영 수 · 재구성 · 분할 문턱 | [인쇄] p.3 · [미확인] |
| 온도 | 측정 온도 숫자 없음 | [미확인] |

### 3-2. ★ 순수 LGPS 의 σ(P) — 그림 5 (계산 입력 곡선)
원문: *"Fig. 5 shows the experimentally measured ionic conductivities after eliminating interfacial resistance. When under sufficient pressure, the measured ionic conductivities roughly correspond with the known value for sulfide solid electrolyte [16]"* (p.5) · 계산은 *"the fitted pressure–ionic conductivity curve"* (p.3) 를 쓴다 — 맞춤 식 [미확인] (그림의 선은 매끈한 곡선 하나 · 측정점 표시 없음).

| P (MPa) | σ (mS/cm) [판독] | | P (MPa) | σ (mS/cm) [판독] |
|---|---|---|---|---|
| 0.63 (곡선 시작) | 0.0205 | | 20 | 0.523 |
| 1.05 | 0.058 | | 40 | 0.682 |
| 2.42 | 0.137 | | 60 | 0.845 |
| 4.41 | 0.242 | | 80 | 1.008 |
| 5.88 | 0.322 | | **100** | **1.168** |
| **8.4 (꺾임)** | **0.428** | | 120 | 1.329 |
| 10 | 0.444 | | 128.6 (곡선 끝) | 1.40 |

- 모양 [카드 산술]: 0.63 → 8.4 MPa 에서 **×21** (거의 지수꼴 급경사) · 10 → 125 MPa 는 거의 **직선** (기울기 0.0080 mS/cm/MPa · 0.444 → 1.367).  ⇒ 응력이 ≈ 8 MPa 아래인 SE 복셀은 σ 가 급히 떨어진다 (§7-4 의 읽는 법).
- **그림 5 삽도 (순수 SE 저항 · 판독)**: t = 2.7 mm — 132.3 (1 MPa) · 104.0 (5) · 90.6 (10) · 78.3 (20) · 68.3 (40) · 62.9 (60) · 59.1 (80) · **56.9 kΩ (99 MPa)** / t = 0.8 mm — 66.0 (1) · 46.0 (5) · 32.0 (15) · 26.3 (30) · 21.7 (50) · 20.6 (61.5) · 18.3 (90) · **17.7 kΩ (99 MPa)**.
- 단위 길이 저항 [카드 산술]: 99 MPa 에서 56.9/2.7 = **21.1** ↔ 17.7/0.8 = **22.1 kΩ/mm** (원문 *"The unit length resistances of SSE samples with different thicknesses eventually converged to a similar value as the applied pressure increased"* p.2 와 같은 그림) · 5 MPa 에서는 38.5 ↔ 57.5 kΩ/mm.
- 두 두께 직선의 절편 (= 두 Li/SE 계면 + 직렬 저항) [카드 산술 · 두 점]: ≈37–38 kΩ (1–2 MPa) → 10.5 (15) → 6.9 (30) → 3.3 (50) → 1.2–1.7 kΩ (90–99 MPa) — 100 MPa 에서는 R 의 ≈2 % (원문 '계면 압력 의존 무시' 는 고압 쪽에서 맞는 꼴) · 저압에서는 두 시료의 밀도 차를 가를 수 없어 [카드 해석].
- ⚠ **삽도 ↔ 본 곡선 어긋남** [카드 산술]: 두 두께의 차 (Δt 1.9 mm · ΔR 39.2 kΩ · 단면 = 안지름 1 mm 원 0.785 mm²) 로 낸 σ = Δt/(ΔR·A) = **0.62 mS/cm (99 MPa)** · 시료 하나씩 0.60 · 0.58 ↔ 본 곡선 **1.17 mS/cm (100 MPa)** — **≈1.9 배**.  순수 SE 시료의 단면 · 본 곡선을 낸 시료 · 맞춤 식이 원문에 없어 어느 쪽이 맞는지 [미확인] (가정 = 셀 안지름 1 mm 를 시료 단면으로).
- 다른 카드와 [다른 카드]: LGPS 소결 펠릿 12 mS/cm (27 °C · `kamaya2011_…` L29 · L97 · 이 논문 [5]) 의 ≈1/10 · [16] Sakuda 2013 은 75Li₂S·25P₂S₅ **유리** (냉간 360 MPa 0.31 mS/cm · `sakuda2013_…` L61) — 원문의 *"roughly correspond with the known value … [16]"* 는 다른 재료와의 비교다.

### 3-3. ★ 응력 분포 — 그림 6 · 8 (선형 탄성 복셀 FEM · 인가 100 MPa)
| ZrO₂ (vol%) | SE 평균 MPS (MPa) | SE 평균 ÷ 인가 | ZrO₂ 축하중 몫 하한 [카드 산술] | Voigt (등변형) 몫 (E 200 / 21.7) [카드 산술] | Reuss (등응력) 몫 = f |
|---|---|---|---|---|---|
| 19 (판독 19.06) | **87.7** [판독] | 0.877 | ≥ **0.29** | 0.684 | 0.19 |
| 42 (판독 41.4) | **66.0** [판독] · *"approximately 66"* [인쇄] | 0.660 | ≥ **0.62** | 0.870 | 0.42 |
| 55 (판독 54.9) | **60.9** [판독] | 0.609 | ≥ **0.73** | 0.918 | 0.55 |
| 67 (판독 66.8) | **48.9** [판독] · *"approximately 50 MPa"* [인쇄] | 0.489 | ≥ **0.84** | 0.949 | 0.67 |

- 그림 6b 는 *"obtained from voxel-FEM stress analysis with a Young's modulus of 21.7 GPa"* (p.6) — E_SE 0.3 GPa 계산의 SE 평균 응력은 그림 · 본문에 없다 [미확인] (대비 667 이면 SE 몫이 더 작아질 쪽 [카드 추론]).
- **하한의 근거** [카드 산술]: 평균 응력 정리 — 경계 견인력만으로 정해지므로 복합체 전체의 부피 평균 σzz = 인가 100 MPa (옆면 roller = z 방향 견인 0) → f·⟨σzz⟩_ZrO₂ + (1 − f)·⟨σzz⟩_SE = 100.  압축을 양으로 MPS ≥ σzz (모든 점) → (1 − f)·⟨σzz⟩_SE ≤ (1 − f)·⟨MPS⟩_SE → **ZrO₂ 몫 ≥ 1 − (1 − f)·⟨MPS⟩_SE / 100**.  (가정: 그림의 '평균' = 부피 평균 · f = 표시 분율)
- **42 vol% 분포 (그림 6a · 판독 · 카드 산술)**: SE 봉우리 **61.6 MPa** (2.14 × 10⁶) · 평균 **68.4** · 중앙 65.6 · 범위 ≈11–159 MPa · ZrO₂ 봉우리 **127.9 MPa** (1.61 × 10⁶) · 평균 **153.0** · 중앙 145.6 · 범위 ≈43–400 MPa (꼬리: > 200 MPa 16.5 % · > 300 MPa 1.7 % — 곡선 아래 넓이 몫) · 겹침 대략 40–160 MPa.  본문: *"zirconia will experience stress higher than what was applied. On the other hand, the applied stress is not transferred to SSE"* (p.6).
- 비 [카드 산술]: ZrO₂ / SE 평균 **2.24** (판독끼리) · 2.32 (판독 ZrO₂ ÷ 인쇄 SE 66) · 봉우리끼리 2.08 ↔ 영률 비 9.2.
- 일관 점검 [카드 산술]: 0.42 × 153.0 + 0.58 × 68.4 = **103.9 MPa** (인쇄 66 을 쓰면 102.5) — 정리 (σzz 평균 = 100) 보다 2–4 % 크다 = MPS ≥ σzz 와 맞는 방향 → 그림 6a 의 두 평균은 42 vol% 와 **맞는다**.  ⚠ 그러나 두 곡선 아래 **넓이 비** 는 ZrO₂ **0.69** : SE 0.31 — 42 vol% 와 안 맞는다 (§3-7 ①).
- **지도 (그림 8 · 19 · 55 vol%)**: 물질 (1 · 검정 = ZrO₂) · MPS (2 · 0–100 MPa 띠 · ZrO₂ 자리는 흰색 = 100 MPa 이상으로 포화) · 전류 밀도 (3 · 0–80 A/m²).  원문: *"the higher stress regions corresponds with zirconia"* · *"zirconia acts as a stress support, decreasing the stress propagating through the SSE. As the volume fraction of zirconia increases, the rigidity of the stress support increases"* (p.7–9) · *"current runs through the narrow regions of the SSE"* · *"Steep potential gradient (drop) formed at narrow pathways and regions with decreased stress"* (p.9).  단면 위치 · 어느 Case · 어느 E 인지 [미확인].

### 3-4. ★ 계산 ÷ 실측 — 그림 7 (100 MPa · 판독)
| ZrO₂ | Case 1 (응력 없음 · σ(100) 고르게) | Case 2 (MPS · 등방) [막대 끝] | Case 3 (NS · 방향별) [막대 끝] | 실측 복합체 ÷ 순수 SE 상한 (1 − f)/Case1 [카드 산술] |
|---|---|---|---|---|
| 19 vol% | **1.72** | 1.29 [1.14–1.49] | 1.18 [0.99–1.42] | ≤ 0.47 |
| 42 vol% | **1.78** | 0.77 [0.32–1.27] | 0.67 [0.22–1.17] | ≤ 0.33 |
| 55 vol% | **4.71** | 1.66 [0.40–2.97] | 1.48 [0.31–2.71] | ≤ 0.096 |
| 67 vol% | **4.17** | 1.24 [0.22–2.30] | 1.09 [0.18–2.05] | ≤ 0.079 |

- 정의 (p.5): 계산 상대 σ = 복합체 전류 ÷ 순수 SSE 전류 (계산) · 실측 상대 σ = 복합체 σ ÷ 순수 SSE σ (측정) · 그림 값 = 계산 ÷ 실측 (*"normalized by experimental data … the value approaches unity"* p.6).
- 오차 막대 = *"the extremes of the error bars were set by these two Young's moduli"* (p.3) — E_SE 0.3 · 21.7 GPa 두 계산.  어느 끝이 어느 E 인지 원문에 없다 [미확인] — 대비가 큰 0.3 GPa 쪽이 SE 응력을 더 낮춰 아래 끝일 것 [카드 추론].  막대 높이 = 두 끝의 산술 중간과 0.03 안에서 같다 (1.29 ↔ 1.32 · 0.77 ↔ 0.80 · 1.66 ↔ 1.69 · 1.24 ↔ 1.26 …) [판독 · 카드 추론].  Case 1 은 막대 없음.
- 상한 열의 근거 [카드 산술]: Case 1 계산 상대 σ = 같은 기하의 유효 σ 비 ≤ 1 − f (부도체 함유물의 Wiener 병렬 상한 · 기하 무관) → 실측 상대 σ = (Case 1 계산) / (그림 값) ≤ (1 − f)/그림 값.  **실측 복합체 σ 는 순수 SE 의 많아야 47 · 33 · 9.6 · 7.9 %** (100 MPa) — 원문의 *"decreases drastically"* (초록) 의 하한 쪽 크기.
- 원문 읽기: *"discrepancy increases with the zirconia volume fraction … the zirconia composite with 67% had a slightly smaller discrepancy in Case-1. This due to the difference in tortuosity … However, these structural differences of zirconia are negligible compared to the magnitude of effect stress has on ionic conductivity"* (p.6).
- ⚠ 판별력 [카드 산술]: Case 2 · 3 의 막대 폭 = 1.31 · 1.43 (19) · 4.0 · 5.3 (42) · 7.4 · 8.7 (55) · 10.6 · 11.6 배 (67 vol% · 위 끝 ÷ 아래 끝) — 42–67 vol% 에서 막대가 1 을 포함하는 것은 **거의 어떤 결과도 '일치'** 로 받아들이는 폭이다.  저자 자신: *"it is impossible to determine whether the isotropic (Case 2) or anisotropic (Case 3) model is more accurate because of the large margin of error"* (p.9).  19 vol% 에서는 Case 2 막대 [1.14, 1.49] 가 1 을 넘는다 (응력 반영 뒤에도 과대).

### 3-5. 응력 → σ 가 얼마나 '셀' 수 있나 — Case 1 → 2 의 크기 [카드 산술 · 카드 추론]
- 42 vol% 에서 Case 1 → Case 2 = 1.78 → 0.77 (**× 0.43**).  만약 SE 가 평균 66 MPa 로 **고르게** 눌렸다면 σ_SE(66)/σ_SE(100) = 0.891/1.168 = **× 0.76** (그림 5 판독) 뿐이다 → 실제 감소의 나머지는 **응력의 퍼짐** — σ(P) 의 저압 급경사 (≈8 MPa 아래 ×21) 때문에 저응력 SE 와 좁은 목이 거의 막힘 요소가 되는 효과 [카드 추론 · 그림 8 의 '좁은 길에 전류 · 저응력에 급한 전위 강하' 와 같은 방향].

### 3-6. 입력 물성 (표 1) · 정본 카드 · CL-90 대조
| 원문 값 (표 1 · p.3–4) | 원문의 근거 | 대조 |
|---|---|---|
| LGPS E **Max 21.7 GPa** | *"obtained by a first-principle calculation [23] and is considered the maximum for an SSE at true density"* | [23] = Deng 2016 · `deng2016_…` L102 Table III: LGPS E **21.7** · ν **0.37** · G/B 0.29 [다른 카드] → 값 · ν 둘 다 같다 |
| LGPS E **Min 0.3 GPa** | *"obtained experimentally for a compressed powder by considering total strain and applied stress … the minimum limit for the Young's modulus of LGPS"* | 인용 없음 · 시험 조건 (압력 · 변형률) [미확인] · = 압분체 **할선** (총변형률 기준) — 같은 그룹 kodama2020 의 Li₆PS₅Br 분말 할선 *"25 MPa to 250 MPa"* 와 같은 꼴의 양 [다른 카드 `kodama2020_…` §3-4] |
| LGPS ν **0.37** | 출처 표시 없음 | = Deng 2016 Table III 의 LGPS 값 [다른 카드] |
| ZrO₂ E **200.0 GPa** · ν **0.30** | 출처 표시 없음 · 본문은 *"almost the same as … LCO, Si, and NMC [18]"* | [18] = Cheng · Taylor · Wolfenstine · Sakamoto, J. Asian Ceram. Soc. 5 (2017) 113 (**LCO** 탄성) — `koerver2018_…` L187 이 옮긴 LCO **191.0 GPa** · ν 0.24 · NCM111 199.0 GPa (Cheng 2017 J. Eur. Ceram. Soc. — 이 논문은 인용 안 함) [다른 카드] · NMC811 이차입자 압입 138 ± 24 GPa (`sedlatschek2026_…`) [다른 카드] → ZrO₂ 200 은 LCO · NCM111 과 비슷 · NMC811 의 ≈1.4 배 |
| **CL-90 세 값** (NCM 경도 · NCM E 140 GPa · LPSCl E 24 GPa) | — | **없음** (§0-1 ② 줄 · 전수 낱말 검색) — heck2026 L305 의 '[미확인]' 에 대한 답 = 이 논문이 아니다 (값으로 확인) |

### 3-7. 원문 안 어긋남 (그림 판독으로 드러난 것 · 고치지 않고 적는다)
1. **그림 6a 넓이 비** [카드 산술]: 곡선 아래 넓이 ZrO₂ 1.945 × 10⁸ : SE 0.892 × 10⁸ (count·MPa) = **0.69 : 0.31** ↔ 캡션 42 vol% — 세는 단위 (복셀 · 절점 · 구간 폭) · 정규화 [미확인].  두 평균은 42 vol% 와 맞는다 (§3-3) — 넓이로 부피를 읽지 않는다.
2. **SE 최빈 · 평균** : 본문 *"average and mode … approximately 66 and 69 MPa"* ↔ 그림 6a 봉우리 **61–63 MPa** (판독 61.6) · 판독 평균 68.4 · 중앙 65.6 — 그림은 오른쪽 꼬리 (최빈 < 중앙 < 평균) 인데 본문 두 값은 그 반대 순서 · 구간 폭 [미확인].
3. **그림 5 삽도 ↔ 본 곡선** σ 1.9 배 (§3-2).
4. **ZrO₂ 분율 41 ↔ 42 vol%** (본문 p.3 · 그림 2b ↔ 그림 6a · 7b 캡션) — 판독 x 41.4 (그림 6b).
5. 계면 이름 섞임: 'LGPS/Li interfacial resistance' · 'LGPS/SE interface' · 'Li/SE interfacial resistance' (p.2–3) 가 같은 것을 가리킨다 [카드 해석] · 'the SEE' (p.7) · 'As general a general trend' (p.6) · 'quantitively' (p.6) · 'The SE constraints' (p.2) 오타.
6. 참고문헌: [7] 학술지 이름 'Electrochem. Soc.' (J. 빠짐) · [22] 학술지 이름 없음 ("52, 2004, https://doi.org/10.11396/jjsndi.53.701, 701-701") · [21] 'T. li' · [26] DOI 없음.

---

## 4. ★ 방법 — 실험 · CT · 복셀 FEM · 이온 수송 계산

### 4-1. 측정 사슬 (재구성)
LGPS 분말 (< 40 µm) + ZrO₂ (< 150 µm) 섞음 (혼합 방법 · 시간 [미확인]) → 지름 1 mm 셀 · 양 끝 Li 0.3 mm → **100 MPa** (가압 방법 [미확인]) → DC ≈0.1 mA/cm² · 짧게 → R → 두께 t (셀 안 CT) → 식 (1) σ → 순수 SSE (두께 둘) 로 같은 측정 → 상대 σ (복합체 ÷ 순수).  CT (160 kV · 4 × 4 × 5 µm) → 분할 (SE · ZrO₂ 두 상 · 문턱 [미확인]) → 계산 둘.

### 4-2. ★ 복셀 FEM 응력 해석 (§2.2.1 · p.3 · 그림 3)
| 항목 | 내용 | 표지 |
|---|---|---|
| 도구 | **VOXELCON** [22] (제작사 표기 없음 · 감사의 글 *"We thank Quint Corporation for support with voxel-FEM stress analysis"* p.9) · *"Unlike the regular FEM, voxel-FEM operates on a cubic mesh, which allows one-to-one processing of structural data and prevents errors associated with meshing"* · *"large-scale graphics processing unit (GPU)-based voxel-FEM stress analyses"* | [인쇄] p.3 · p.9 |
| 격자 | *"approximately 300 × 300 × 400 voxels"* = 3.6 × 10⁷ 복셀 · 절점 ≈3.63 × 10⁷ → 변위 자유도 ≈1.09 × 10⁸ [카드 산술] · 복셀 4 × 4 × 5 µm → 영역 ≈1.2 × 1.2 × 2.0 mm [카드 산술] (지름 1 mm · 두께 1–2 mm 시료 전체 — RVE 가 아니라 **시료 통째**) | [인쇄] · [카드 산술] |
| 구성식 | **Hooke 법칙 (선형 탄성 · 등방)** · Galerkin FEM · 요소 강성 행렬의 1 차 연립 → 복셀 꼭짓점의 응력 · 변형률 | [인쇄] p.3 |
| 상 | SE (LGPS) · ZrO₂ 두 상 — 빈틈은 고체 SE 로: *"treated as void-free in the stress calculation, because micro/nanoscale voids smaller than voxel size could not be distinguished from the SSE"* | [인쇄] p.3 |
| 상 경계 | 접촉 · 미끄럼 · 분리 조건 언급 없음 → 복셀 FEM 의 절점 공유 = **완전 결합** [카드 추론] | [미확인] · [카드 추론] |
| 물성 | 표 1 (§3-6) · E_SE 는 21.7 / 0.3 GPa 두 계산 — *"the actual Young's modulus, which is equivalent to accounting for local variations, was between these two extreme cases"* | [인쇄] p.3 |
| 경계 조건 | *"While one side of the composite was fixed, a pressure of 100 MPa was applied to the opposite surface and the lateral surface was allowed to slide along the thickness direction"* · *"a stiff plate was virtually placed on both sides … pressure and fixation constraints were placed over the plates"* (표면 변형이 인가압을 흐리지 않게) — 그림 3: 위 고정 · 아래 100 MPa · 옆 roller | [인쇄] p.3 · 그림 3 |
| 하중 이력 | CT 형상은 이미 100 MPa — *"the virtual pressurization with VOXELCON corresponded to applying an additional pressure of 100 MPa. Nevertheless, analytical results were approximately equal to the actual stress distribution … because the stress calculation relied on the assumption that no large-scale deformation occurred under linear stress analysis. In fact, no large-scale deformation was observed in experiments near 100 MPa"* | [인쇄] p.3 |
| 출력 | 복셀마다 **MPS** (*"a scalar value representing the magnitude of compression and include the effects of shearing"*) · **NS** (*"the magnitude of a stress vector perpendicular to a particular voxel"* = 복셀 면 방향별 수직 응력 [카드 해석]) | [인쇄] p.3 |
| 맞춘 값 | **0** (E 는 DFT · 압분체 실험 · ZrO₂ 표 값) | [인쇄] |
| 비용 · 수렴 · 요소 | 요소 종류 · 풀이기 · 수렴 기준 · 시간 · 메모리 · GPU 종류 | [미확인] |

### 4-3. ★ 이온 수송 계산 (§2.2.2 · p.3–5 · 그림 4)
| 항목 | 내용 | 표지 |
|---|---|---|
| 형상 | 같은 CT 복셀 (SE · ZrO₂) | [인쇄] p.3 |
| 국소 σ (결합 규칙) | SE 복셀 = 순수 LGPS σ(P) 곡선 (그림 5 · 맞춤) 에서 읽은 값 · ZrO₂ = 0 · Case 1: 모든 SE = σ(100 MPa) · **Case 2 (그림 4a)**: σ_x = σ_y = σ_z = σ(MPS) · **Case 3 (그림 4b)**: σ_i = σ(NS_i) (i = x, y, z) | [인쇄] p.3–5 |
| 가정 | *"Since experimental ionic conductivity values reflect the effects of nanoscale features, we assumed that assigning ionic conductivities to each voxel from the pressure-ionic conductivity curve will allow us to reflect the effects of nanoscale features without visualizing them"* (p.3) · *"We initially assume that the void ratio of the SSE is solely dependent on stress"* (p.6–7) | [인쇄] |
| 지배식 · 풀이 | *"the applied voltage, which can be an arbitrary value, was set to unity, and the resistance was obtained by calculating the current flowing through a given voxel based on the Maxwell equations [27]"* · 절차 = [17] (Kodama 2020 — 그 카드: 유한체적 + SOR · ∇·j = 0 · 옴 법칙 [다른 카드 `kodama2020_…` §4-3]) · 이 논문 본문엔 식 · 이산화 이름이 없다 | [인쇄] p.3–4 · [다른 카드] |
| 수렴 | *"Calculations were regarded as converged to a solution when the current values through the composite in the z-direction were uniformly distributed"* (p.4) — 문턱 숫자 [미확인] | [인쇄] · [미확인] |
| 산출 | 상대 σ (계산 · 실측) · 그림 7 의 비 · 그림 8 의 전류 밀도 지도 | [인쇄] p.5 |
| ★ 결합의 꼴 | **기계 → 수송 한 방향** (응력장 → 국소 σ) — 수송이 기계에 되먹지 않음 · 나노 특징 (빈틈 · 입계 · 굴곡 · 접촉) 은 순수 SE σ(P) 안에 '평균' 으로 들어 있다고 본다 | [카드 해석] |

### 4-4. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **입자 처리**: 입자 단위 모델이 **아니다** — CT 로 분할한 두 상의 **결합 연속체** (SE 입자 · 빈틈 · 입계는 4–5 µm 복셀보다 작아 하나의 매질로) · ZrO₂ (≤ 150 µm ≈ 30–37 복셀 [카드 산술]) 는 형상대로 들어가지만 SE 입자 (< 40 µm · ≤ 8–10 복셀) 는 경계가 풀리지 않는다 · 강체 · 접촉 · 형상 소성 없음.
- **(i) DEM 한계 진술 = 말 없음** — DEM 을 쓰지 않는다.  가까운 문장: *"because the SSE is a powder, its Young's modulus may vary with pressure depending on the resultant non-linear stress–strain relationship [24–26]"* (p.3).
- **(ii) 소성 · 큰 변형을 넣기 어려운 이유와 우회**: 논문은 **넣지 않는다** — 선형 탄성 한 번 · 소성 대신 SE 영률 두 극단 (참밀도 DFT 21.7 ↔ 압분체 할선 0.3 GPa) 으로 **오차 막대** 를 세운다.  저자 진술: *"This margin of error is attributed to the non-linearity of the stress–strain relationship of the SSE powder. The nanoscale voids and particle size of the SSE are examples of factors that introduce non-linearity. Non-linear stress analysis is necessary to minimize the margin of error"* (p.9).  비용 = 3.6 × 10⁷ 복셀 선형 풀이 한 번 (GPU) · 시간 [미확인].
- **(iii) 차원**: 측정 · 계산 모두 **3D** (CT 부피 · 복셀 FEM · 3D 전도) · 그림 8 은 3D 결과의 2D 단면 · 2D → 3D 진술 없음.
- **(iv) 탈압**: **없음** — 복합체는 100 MPa 측정 · 계산 하나 · 순수 SE σ(P) 도 가압 가지뿐.

### 4-5. 기법 미니 용어집
- **복셀 FEM (voxel finite element method)** = CT 의 정육면체 복셀을 그대로 8 절점 육면체 요소로 쓰는 FEM — 망 만들기 오류가 없고 거대 계산에 GPU 가 맞지만, 상 경계가 계단 모양이고 기본은 절점 공유 (결합) 라 접촉 · 미끄럼을 따로 넣지 않으면 없다 [카드 해석 · 요소 종류는 원문 미기재].
- **최소 주응력 (MPS)** = 응력 텐서의 가장 작은 고유값 — 인장 양수 규약에서 가장 압축인 값 · 원문은 압축 크기를 양수로 그린다.
- **수직 응력 (NS)** = 한 면에 수직인 응력 성분 (여기서는 x · y · z 면) — Case 3 의 방향별 σ.
- **평균 응력 정리** = 정적 평형 물체의 부피 평균 응력 = (1/V)∮ t ⊗ x dA — 경계 견인력만으로 정해진다 → 상별 평균 응력과 부피 분율로 상별 하중 몫을 맞춰 볼 수 있다.
- **Voigt · Reuss 경계** = 등변형 (병렬) · 등응력 (직렬) 가정의 두 극단 — 단단한 상의 응력 몫은 그 사이.
- **Wiener 경계** = 혼합물 유효 σ 의 병렬 (위) · 직렬 (아래) 경계 — 부도체 함유물이면 σ_eff/σ_SE ≤ 1 − f.
- **할선 영률** = 응력 ÷ 총변형률 (원점에서 그은 기울기) — 분말 압밀처럼 비선형이면 압력마다 다르다.

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | SEM — LGPS (40 µm 막대) · ZrO₂ (1 mm 막대) | 입경 감각 (< 40 · < 150 µm) |
| 2 (a · b) | 실험 셀 그림 (X 선 원 · 검출기 · 스테인리스 봉 · Li · 복합체 · 아래에서 가압 · 회전) · 41 vol% 복합체 CT 3D (밝은 회색 SE · 어두운 회색 ZrO₂) | 시료 통째 CT · 단단한 상 덩어리 모양 |
| 3 | ★ 응력 해석 경계 조건 — 위 고정 · 옆 roller · 아래 100 MPa · 좌표 | 우리 MPM 플래튼 + 미끄럼 벽과 같은 꼴의 BC |
| 4 (a · b · c) | Case 2 (σ(MPS) 등방) · Case 3 (σ(NS_i) 방향별) 그림 · 흐름도 (실험 → CT → 복셀 FEM → MPS · NS → 수송) | 응력 → σ 결합 규칙 (식 대신 그림) |
| 5 (+ 삽도) | ★ 순수 LGPS σ(P) (로그 축 · 0–≈129 MPa) · 삽도 = 두 두께 (2.7 · 0.8 mm) 저항 vs P | 국소 σ 법칙의 입력 · 저압 급경사 · 삽도 ↔ 본 곡선 어긋남 (§3-2) |
| 6a | ★ 42 vol% MPS 분포 (ZrO₂ 실선 · SE 점선) | 상별 응력 분포의 꼴 (평균 · 꼬리) |
| 6b | ★ SE 평균 MPS vs ZrO₂ vol% (E_SE 21.7) | R1 의 연속체 기준 (§7-3) |
| 7 (a–d) | ★ Case 1 · 2 · 3 계산 ÷ 실측 (19 · 42 · 55 · 67 vol%) | 기하만 넣은 복셀 σ 의 과대 · 응력 반영 · 막대 폭 |
| 8 (a · b · c) | 19 · 55 vol% 단면의 물질 · MPS · 전류 밀도 지도 · 나노 특징 그림 (응력 → 빈틈 우회) | 좁은 길 · 저응력 자리의 흐름 집중 그림 |
| 표 1 | LGPS E 21.7 / 0.3 GPa · ν 0.37 · ZrO₂ 200.0 GPa · 0.30 | CL-90 대조 (§3-6) |
| 식 (1) | σ = (1/R)(t/A) + 기호 줄 | 측정 정의 (유일한 번호 식) |
| 근거 문단 19 장 | `txt_p1_*` (하이라이트 · 초록) · `txt_p2_*` (재료 · 셀 · DC · 순수 SE) · `txt_p3_*` (CT · 복셀 FEM · BC · 수송) · `txt_p4_p5_*` (Case · 상대 σ) · `txt_p5_*` · `txt_p6_*` (결과) · `txt_p6_p7_*` · `txt_p7_*` · `txt_p7_p9_*` (기전) · `txt_p9_*` (한계 · 결론) | 원문 인용용 |

## 6. Post-processing ★
- **무엇을**: DC → R → σ (식 1) · CT → 두 상 → 복셀 FEM → MPS · NS (복셀) → 분포 (그림 6a · 히스토그램) · SE 평균 (그림 6b) · 지도 (그림 8) · 국소 σ → 전류 → 상대 σ → 계산 ÷ 실측 (그림 7) · E 두 극단 → 막대.
- **안 한 것**: 기공률 · 상대밀도 · 접촉 면적 · 접촉 수 · 굴곡 숫자 (본문은 'tortuosity' 말만) · 상별 하중 몫 숫자 · ZrO₂ 평균 응력 숫자 · 응력 성분별 (σzz) 평균 · 격자 · 복셀 수렴 · 반복 측정 · 복합체 σ 절대값 · 탈압.
- **이 카드의 후처리**: 원 래스터 판독 (그림 5 본 곡선 · 삽도 · 6a 두 곡선 (열마다 무리 나눔 · 점선 틈 보간) · 6b 원 중심 · 7 막대 · 오차 끝 — 146 행) · 평균 응력 정리로 ZrO₂ 몫 하한 · Voigt · Reuss 몫 · 그림 6a 평균 · 중앙 · 넓이 비 · Wiener 상한 · 두 두께 저항의 단위 길이 · 절편 · 삽도 σ.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · `comparison_vs_ours_DEM.md` 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 재료 | LGPS + **ZrO₂** (대리 · 200 GPa) · Li 전극 · 탄소 없음 | LPSCl + NCM811 (DEM E_AM 140 GPa · 출처 [미확인] · CL-90) | 재료 둘 다 다름 · 'AM' 이 전기화학 없는 세라믹 |
| 압력 | 100 MPa 한 점 (계산 · 복합체) | 300 MPa (가압 중 · 판 고정 이완) | ⅓ · 선형이라 비만 옮겨질 수 있는 꼴 (실제는 비선형) |
| 역학 모델 | 선형 탄성 결합 연속체 (복셀 FEM · 빈틈 0) | DEM = 강구 · hooke/hysteresis · E_eff 1.35 GPa (18 배 연화) / MPM = J2 · E 1.53 · σ_y 0.30 · ν 0.49 · AM 얼림 | 셋 다 다름 — 이 논문은 소성 · 접촉 · 재배열이 모두 없는 '탄성 기준선' |
| E 대비 (단단한 상 ÷ SE) | 9.2 (21.7 GPa) · 667 (0.3 GPa) [카드 산술] | DEM 140/1.35 = 104 [카드 산술] · MPM = ∞ (AM 얼림) | 우리 DEM 대비가 그들 두 극단 사이 |
| 하중 몫 | SE 평균 MPS ÷ 인가 0.88 → 0.49 · ZrO₂ 몫 ≥ 0.29 → 0.84 (19 → 67 vol%) | DEM f_AM (AM–AM 규약) 0.52–0.68 · 상별 virial 0.73–0.79 (100–600 MPa · CLAUDE.md) · 300 MPa 끝 f_AM 0.675–0.794 · φ_AM ≈0.62 (`comparison_vs_ours_DEM.md` [StallardJES22] 줄) | 같은 양이 아니다 (§7-3) |
| 수송 | 복셀 FV 류 전도 · 국소 σ = σ_pure(응력) | STEP3 복셀 FV (SE σ 고르게 · CONTACT_FREE · CL-81) · 접촉망 Holm (DEM) | 이 논문의 Case 1 = 우리 STEP3 의 꼴 (§7-4) |
| 해상도 | 복셀 4 × 4 × 5 µm · SE 입자 안 풀림 · ZrO₂ ≈30–37 복셀 | STEP3 vox 0.15–0.4 µm · SE ⌀1 µm (2.5–7 복셀) | 그들은 SE 를 매질로 · 우리는 SE 입자를 (거칠게) 푼다 |
| 탈압 | 없음 | DEM 언로딩 키트 (진행) · MPM 제하 없음 | 표적 없음 |

### 7-2. ★ 랩 기준과 나란히 (판정 없이)
| 출처 | 재료 | 압력 · 상태 | 진밀도 분모 | 기공 |
|---|---|---|---|---|
| **랩 표준** | LPSCl | 300 MPa | **1.64** (고정) | **10–13 %** |
| 이 논문 | LGPS (순수 · 복합) | 0–≈129 MPa (순수) · 100 MPa (복합) · 누른 채 | **없음** | **없음** (CT 빈틈 안 보임 · 고체로 셈) |
- 이 논문은 "랩 표준과 다른 문헌 값" 자리에 놓을 기공 숫자를 **주지 않는다**.  나란히 놓을 수 있는 것은 순수 LGPS σ(P) (§3-2) 뿐 — 우리 쪽 짝은 σ₀ (보고 1.5 mS/cm · 솔버 3.0 · CL-91) 이지 기공이 아니다.

### 7-3. ★ AM 하중 몫 (MPM DO-NOT ② · R1) — 연속체 탄성 기준선
- **이 논문이 주는 것**: '단단한 상이 하중을 더 진다' 의 **결합 연속체 · 선형 탄성** 값 — 인가 100 MPa 에서 SE 평균 MPS 87.7 → 48.9 MPa (ZrO₂ 19 → 67 vol%) · ZrO₂ 몫 ≥ 0.29 · 0.62 · 0.73 · 0.84 [판독 · 카드 산술].  우리 MPM 의 문제 (AM 을 얼려 판 반력 읽기에서 AM 몫 0 → SE 가 100 % 를 져 과압축 · CLAUDE.md MPM DO-NOT) 에 대해 **'SE 는 인가압의 얼마를 지는가'** (상별 **평균 응력**) 의 문헌 계산값 — 정본 비교 문서 [Du25FC] 줄의 *"MPM DO-NOT ② (AM 하중 분담) 의 문헌 값은 여기 없다 (상별 · 쌍 종류별 하중 몫 0)"* 자리에 놓이는 한 점 (DEM 접촉력 비는 `martinbouvard2003_dem_composite_cold_compaction` 의 N₂₂/N₁₁ ≈3.5 (경질 40 % · 마찰) [다른 카드] 가 따로 있다 — 다른 양).
- 우리 DEM 과 숫자 [카드 산술 · 같은 양 아님]: 우리 침대 φ_AM ≈0.62 자리를 그들 55–67 vol% 사이로 직선 보간하면 ZrO₂ 몫 하한 ≈ **0.79** ↔ 우리 DEM 300 MPa 상별 virial 0.794 · AM–AM 0.675 — **숫자가 가깝다는 것 이상을 말하지 않는다**: 양 (MPS 기반 σzz 몫 하한 ↔ 접촉망 · 상별 virial) · 모델 (결합 탄성 연속체 ↔ 연화 강구 접촉망) · 재료 · E 대비 (9.2 ↔ 104) · 압력 (100 ↔ 300) · 기공 (0 ↔ ≈15 %) 이 다 다르다.  frame [4] — 서로 맞춘 것이 아니고 같은 관측량도 아니다 → 교차검증으로 인용하지 않는다.
- 쓸 자리: MPM 에서 AM 이 하중을 지게 한 뒤 (후보 A · A′ · B) **결과 전 대조 항목** 으로 'SE 평균 축응력 ÷ 인가압 vs 단단한 상 분율' 네 점 (선형 탄성 · E 21.7 · 표지 필수) · 우리 f_AM v1 (target·(1 − f_AM)) 규약을 고를 때 '탄성 연속체면 어디쯤' 의 참고 한 줄.
- ⚠ 선형이라 그들의 비는 압력과 무관하고 E 대비에만 달린다 — 실제 압밀은 SE 의 비선형 (0.3 ↔ 21.7) 이 지배한다 (막대 폭 ×1.3–11.6) · 대비가 클수록 (E_SE 0.3) SE 몫이 더 작아질 것 [카드 추론 · 그 계산의 분포는 원문에 없음].

### 7-4. ★ 복셀 σ (STEP3) ↔ Case 1 — 기하만 넣은 복셀 σ 의 과대
- 이 논문의 **Case 1** (SE 를 σ(100 MPa) 로 고르게 · ZrO₂ 0 · 접촉 저항 0) 은 우리 STEP3 (SE σ_grain 고르게 · 계면 저항 0 = CONTACT_FREE · CL-81) 과 **같은 꼴** — 계산 ÷ 실측 **1.72 · 1.78 · 4.71 · 4.17** (19 · 42 · 55 · 67 vol%) [판독].  같은 그룹 kodama2020 (순수 Li₆PS₅Br) 의 복셀 ÷ EIS 1.07 (104 MPa) [다른 카드] 보다 훨씬 크다 → **단단한 상이 많을수록 기하만 넣은 복셀 σ 의 과대가 커진다** (같은 그룹 · 같은 계산 계열 · 다른 재료 · 다른 시료) [카드 추론].
- 저자의 원인 = SE 응력 차폐 → 빈틈 · 입계 (순수 SE σ(P) 로 대리).  CL-81 의 '복셀 σ = CONTACT_FREE 상한' 과 **방향이 같다** (계산 > 실측).
- ⛔ 배수를 우리에게 옮기지 않는다: (i) LGPS + ZrO₂ (전극 없는 대리) ↔ 우리 LPSCl + NCM (ii) 복셀 4–5 µm (SE 를 매질로) ↔ 우리 SE 입자 (iii) 그들 σ(100) 는 그들 순수 SE 의 값 · 우리 σ_grain 3.0 은 펠릿값 (CL-91) (iv) 실측 복합체 σ 절대값이 원문에 없다.
- 가져올 수 있는 방법: MPM 응력장 (또는 DEM 입자 응력) → SE 국소 σ = σ_pure(국소 압력) — 우리 순수 LPSCl σ(P) 가 있을 때만 · 검증은 같은 침대 복합체 σ 실측으로 (§9 ③).

### 7-5. E 축 (frame [2]) — 두 극단과 우리 연화값
- 그들의 E_SE 두 극단 = 참밀도 DFT **21.7 GPa** (Deng [23]) ↔ 압분체 할선 **0.3 GPa** — 우리 DEM E_eff 1.35 GPa · MPM E 1.53 GPa 는 그 사이에 있다.  '분말 상태의 유효 영률은 참밀도 값과 다르고 압력에 따라 변한다' (p.3) 는 frame [2] (연화 = 재배열 · 미끄럼 · 파쇄의 대리) 와 **말이 비슷할 뿐** 숫자를 옮기지 않는다 (그들의 0.3 GPa = 총변형률 할선 · 시험 조건 미인쇄 · 우리 1.35 = 기공에 맞춘 접촉 강성 매개변수).
- 그들은 E 를 **맞추지 않고 묶는다** (오차 막대) — R5 ('맞추는 값은 모델마다 하나') 의 반대쪽 극: 맞춘 값 0 · 불확도를 그대로 보고.

### 7-6. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 실측 3D 형상 위 **기계 (응력장)** 와 **수송 (전도)** 을 한 방향으로 잇는 사슬 — 우리 '기계 = MPM · 수송 = DEM / STEP3' 분업의 좁은 접점 (응력 → σ) 을 실제로 계산한 선례.
- **없는 것**: 압밀 (형상 변화 · 재배열 · 빈틈 닫힘) · 접촉망 (협착 · 접촉 수) · 소성 · 파괴 · 탈압 — 역학 쪽은 '탄성 기준선' 하나 · 수송 쪽은 '응력 → 순수 SE σ' 경험 법칙 하나.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | (1) **상별 평균 응력 ↔ 인가압 항등식** (평균 응력 정리) 을 판정 전 점검으로 — 그들 그림 6a 평균은 0.42·153 + 0.58·68 = 104 MPa 로 맞고 (MPS ≥ σzz) · 넓이 비 (0.69) 는 안 맞는다 → 우리 상별 응력 출력도 같은 항등식으로 먼저 거른다 (2) 'volume fraction' 정의 (빈틈 뺀 단단한 상 부피 ÷ 전체) 를 숫자 옆에 | 기공 숫자 · 진밀도 · 문턱 규칙 |
| **단계 1** (3D 메모리 · 장 수) | 3.6 × 10⁷ 복셀 · ≈1.09 × 10⁸ 자유도 선형 탄성 한 번을 GPU 로 (2020 · 상용 VOXELCON) [카드 산술] — 크기 감각 | 시간 · 메모리 · GPU [미확인] · 입자별 장 아님 |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 | — |
| **단계 3** (2D 접촉 표현 비교) | 간접: '결합 (접촉 없음)' 연속체가 단단한 상에 응력을 모으는 크기 (탄성 기준) — 한 속도장 모델 (후보 A) 이 접촉 없이도 내는 몫의 참고 | 2D 아님 · 접촉 있는 쪽 비교 없음 |
| **단계 4** (3D 순수 SE · σ_y 하나 맞춤) | 순수 LGPS σ(P) 곡선 (§3-2) — 저압 급경사 (≈8 MPa 아래 ×21) · 그 위 직선 | 기공 곡선 없음 → 맞춤 표적 아님 (랩 표준이 표적) · LGPS ≠ LPSCl |
| **단계 5** (3D 복합 압밀) | ★ **결과 전 대조 항목 후보**: SE 평균 MPS ÷ 인가 = 0.877 · 0.660 · 0.609 · 0.489 (19 · 42 · 55 · 67 vol% · 선형 탄성 · E_SE 21.7 · ZrO₂ 200) · 42 vol% 상별 분포 (SE 봉우리 ≈62 · ZrO₂ 봉우리 ≈128 MPa) — AM 이 하중을 지는 모델에서 같은 분율 · 같은 정의 (MPS) 로 읽어 견준다 | 탄성 · 결합 · 빈틈 0 · 100 MPa · 대리 재료 — 우리 모델이 소성 · 재배열로 다른 값을 내면 그것은 '모델 한계' 가 아니라 '탄성 기준선과의 차' (정보) |
| **단계 6** (탈압 · 되돌아옴) | 없음 | 탈압 계산 · 측정 0 |
| **단계 7** (형상 · 피복 · 수송) | ★ (1) 기하만 넣은 복셀 σ (Case 1 = STEP3 꼴) 가 단단한 상 19–67 vol% 에서 실측을 1.72–4.71 배 넘는다 (2) 국소 응력 → 국소 σ (순수 SE σ(P)) 로 0.67–1.66 (불확도 = E_SE 선택 · 막대 폭 ×1.3–11.6) (3) 저응력 꼬리 · 좁은 목이 복합체 σ 를 정한다 (Case 1 → 2 감소 ×0.43 ↔ 평균 응력만이면 ×0.76 [카드 산술]) | 배수 전이 금지 (§7-4) · 접촉 저항 · 피복 숫자 없음 |
| **후보 D0** (지금 DEM) | 정성: DEM 입자 응력 (Love–Weber) 으로 같은 'SE 상 평균 응력 ÷ 인가' 를 낼 수 있다 — 우리 쪽에 상별 Love–Weber 열 (`stress_ratio_<상>_lw` · CLAUDE.md ④b) 이 있다 → 정의 (분모 · 벽 접촉 입자 포함 여부) 를 맞춘 뒤 이 논문 6b 와 결과 전 대조 [카드 추론] | DEM 없음 · 값 대조 전 정의 대조 필수 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | BC 의 꼴: 양쪽 가상 강판 + 한쪽 고정 / 반대쪽 압력 + 옆면 미끄럼 (그림 3) — 우리 MPM 플래튼 + 미끄럼 벽과 같은 선택 (표면 변형이 인가압을 흐리지 않게) | AM 자리 접촉 규칙 없음 |
| **후보 A** (MPM 강체 AM + SE 한 속도장) | 결합 연속체 (AM 이 SE 에 붙어 함께 변형) 의 탄성 몫 — A 에서 AM 이 '움직이는 강체' 면 이 논문의 E_ZrO₂ → ∞ 극한 쪽 [카드 추론] | 분리 · 미끄럼 · 소성 없음 |
| **후보 A′** (입자별 속도장) | 없음 | — |
| **후보 B** (입자별 FE + 접촉) | '접촉 없는 FE' 의 극한값 — B 가 접촉 · 미끄럼을 넣었을 때 하중 몫이 얼마나 바뀌는지의 기준 | 입자별 망 아님 |
| **후보 C · C′** (MDR · 항복 캡 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀) | E_SE 두 극단 (참밀도 ↔ 압분체 할선) 을 국소 밀도에 따라 고른다는 생각 — 저자가 비선형 해석이 필요하다고 적은 자리 (p.9) | 캡 · Heckel 없음 |
| **U0–U6** | U6 (해상도) 쪽 관찰: SE 를 복셀보다 작은 매질로 두면 '빈틈 0' 이 된다 (그들 4–5 µm ↔ LGPS < 40 µm) · 수렴 시험 0 | 단위 시험 없음 |
| **R1–R7** | ★ **R1** (AM 이 하중을 나눠 짐) 의 연속체 근거 · R2 (미끄럼 · 분리) 는 없음 (결합) · R5 의 반대 예 (맞춘 값 0 · 묶음으로 보고) | R3 · R4 · R6 · R7 없음 |
| **결과 전 대조 항목** | 그림 6b 네 점 · 그림 6a 두 분포 · 그림 7 Case 1 배수 · 순수 LGPS σ(P) — 전부 [판독] · 'LGPS + ZrO₂ · 100 MPa · 선형 탄성 · 결합 · 빈틈 0' 표지와 함께 | 맞추는 데 쓰지 않는다 |

- **재료 · 차원 · 조건 차이**: LGPS ↔ LPSCl · ZrO₂ (200 GPa · 전기화학 없음) ↔ NCM811 · 100 ↔ 300 MPa · 누른 채 = 같음 · 3D = 같음 · 시료 통째 (⌀1 mm × 1–2 mm) ↔ 우리 RVE · 탄성 연속체 ↔ 우리 DEM 접촉망 / MPM 소성.

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **'SE 는 인가압의 얼마를 지는가' 의 탄성 기준선** — 단단한 상 42 vol% 에서 0.66 · 67 vol% 에서 0.49 (평균 MPS) → MPM 에서 AM 하중 분담 ② 를 풀 때 결과 전 대조 항목 (단계 5 · R1) · 우리 DEM f_AM 과 같은 표에 둘 때는 '양 · 모델 · 재료 다름' 표지.
2. **평균 응력 정리로 상별 응력 출력을 거른다** — f·⟨σ⟩_hard + (1 − f)·⟨σ⟩_soft = P 는 모델과 무관한 항등식 → 우리 MPM · DEM 의 상별 응력 · f_AM 출력이 이것을 맞추는지부터 (단계 0) · 이 논문 그림 6a 도 평균은 맞고 넓이는 안 맞았다.
3. **기하만 넣은 복셀 σ 는 단단한 상이 많을수록 더 과대** (1.7 → 4.7) — STEP3 σ_ion 을 실험 옆에 둘 때 CL-81 한정어 ('협착 미포함 = 상한') 에 'AM 분율이 클수록 커질 수 있다' 를 붙인다 (단계 7).  응력 → σ 국소 법칙은 우리 순수 LPSCl σ(P) 와 복합체 σ 실측이 같은 침대에 있을 때만 시도한다.
4. **σ(P) 저압 급경사가 '저응력 목' 을 막힘 요소로 만든다** — 복합체 σ 는 SE 평균 응력보다 응력의 아래 꼬리 · 직렬 목이 정한다 (×0.43 ↔ ×0.76) → 응력장을 σ 로 바꿀 때 평균만 넘기지 않는다 (흐름 밖: Rint ② SE–SE 계면 · 협착).
5. **함정 · 보고 방식** — (i) E 한 값으로 맞추지 않고 두 극단으로 묶은 것은 정직하지만, 막대가 ×4–12 (42–67 vol%) 이면 '일치' 는 판별력이 없다 (ii) 히스토그램 넓이 · 최빈 · 평균 서술이 서로 안 맞을 수 있다 → 분포를 내면 정규화 · 구간 폭 · 평균을 같이 적는다 (iii) '추가 100 MPa' 선형 중첩 = 압밀 이력 · 잔류 응력 무시 — 우리가 눌린 구조에 다른 계산을 이어 붙일 때 (DEM → MPM · 단계 6) 같은 가정을 쓰면 적어 둔다.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In a linear-elastic voxel-FEM analysis of X-ray CT images of Li₁₀GeP₂S₁₂ composites containing ZrO₂ (a stiff, electrochemically inert stand-in for the active material, E = 200 GPa) under 100 MPa, the mean minimum principal stress in the solid electrolyte drops from ≈88 to ≈49 MPa as the ZrO₂ fraction increases from 19 to 67 vol% (digitized from Ohashi et al., J. Power Sources 470 (2020) 228437, Fig. 6b; 66 MPa at 42 vol% stated in the text)."
- "Assigning each electrolyte voxel the conductivity of the pure electrolyte at its local stress reduced the ratio of computed to measured composite conductivity from 1.7–4.7 (geometry only) to 0.7–1.7, with an uncertainty band set by the electrolyte modulus (0.3 vs 21.7 GPa) that spans a factor of up to ≈12 at 42–67 vol% (Ohashi et al. 2020, Fig. 7, digitized)."
- 국문: *"단단한 상 (ZrO₂ 대리) 이 많을수록 SE 가 지는 응력이 인가압 아래로 내려간다 — 선형 탄성 복셀 FEM 계산 (Ohashi 2020) · NCM · 접촉 · 기공은 다루지 않았다."*
- 국문: *"Ohashi 2020 에는 NCM 경도 · NCM 영률 · LPSCl 영률이 없다 (CL-90 대조)."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **NCM 없음** — 'NCM 이 먼저 눌린다' 는 ZrO₂ 계산의 저자 외삽 · ZrO₂ ≈ AM 의 근거 [18] 은 LCO 한 편 · Si 근거 없음.
2. **선형 탄성 · 결합 · 빈틈 0** — 소성 · 접촉 · 재배열 · 파쇄 없음 · CT 형상 (이미 100 MPa) 에 추가 100 MPa (잔류 응력 · 이력 무시) · 저자 스스로 비선형 해석이 필요하다고 적음.
3. **판별력 약한 검증** — Case 2 · 3 막대가 42–67 vol% 에서 ×4.0–11.6 · Case 2 ↔ 3 구분 불가 (저자) · 19 vol% 는 응력 반영 뒤에도 Case 2 > 1.
4. **복합체 σ 절대값 · 기공 · 접촉 · 굴곡 숫자 없음** — 그림 7 은 비뿐.
5. **그림 6a 넓이 비 0.69 ↔ 42 vol%** · **본문 최빈 69 ↔ 그림 봉우리 61–63 MPa** · **삽도 σ ≈0.6 ↔ 본 곡선 1.17 mS/cm** [판독 · 카드 산술].
6. **E_SE 0.3 GPa** — 시험 조건 · 인용 없음 · 그 계산의 응력 분포 그림 없음.
7. **ZrO₂ 물성 출처 없음** (표 1) · ν 0.37 출처 표시 없음 (Deng 과 같음).
8. **수송 계산 세부 미기재** — 식 · 이산화 · 풀이기 · 수렴 문턱 (본문은 [17] · [27] 에 맡김 · [27] 은 플라스마 MHD 발전기 논문).
9. **해상도 · RVE 시험 없음** — 복셀 바꾸기 · 영역 바꾸기 0 · 그림 8 단면 위치 · Case · E [미확인].
10. **CT 조건 · 분할 문턱 · 부피 분율을 낸 방법** [미확인] · 41 ↔ 42 vol%.
11. **이름 · 오타** — 계면 이름 섞임 · 'SEE' · 참고문헌 [7] · [22] 학술지 이름 빠짐 (§3-7).
12. ⚠ 판독 값은 원 래스터 눈금 환산 (그림 6b 의 42 · 67 vol% 점이 본문 66 · ≈50 과 0.1 · 1.1 MPa 안) — 그래도 [판독] 표지로만 인용.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 17 | M. Kodama, S. Komiyama, A. Ohashi, N. Horikawa, K. Kawamura, S. Hirai, High-pressure in situ X-ray computed tomography and numerical simulation of sulfide solid electrolyte, J. Power Sources 462 (2020) 228160. | 기밀 셀 · 수송 계산 절차 · '빈틈 감소' 의 앞 논문 | `kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation` |
| 23 | Z. Deng, Z. Wang, I.-H. Chu, J. Luo, S.P. Ong, Elastic properties of alkali superionic conductor electrolytes from first principles calculations, J. Electrochem. Soc. 163 (2016) A67. | LGPS 21.7 GPa (표 1 최대) | `deng2016_elastic_superionic_electrolytes_dft` |
| 18 | E.J. Cheng, N.J. Taylor, J. Wolfenstine, J. Sakamoto, Elastic properties of lithium cobalt oxide (LiCoO2), J. Asian Ceram. Soc. 5 (2017) 113–117. | 'ZrO₂ ≈ 활물질 영률' 의 유일한 근거 (LCO) — 질문 c | 없음 (stallard2022 · koerver2018 · sharma2023 이 인용만) |
| 26 | Z.Q. Wang, M.S. Wu, G. Liu, X.L. Lei, B. Xu, C.Y. Ouyang, Elastic properties of new solid state electrolyte material Li10GeP2S12: a study from first-principles calculations, Int. J. electrochem. Sci. 9 (2014) 562–568. | LGPS 탄성 DFT · 비선형 응력–변형 근거 [24–26] 의 하나 · CL-90 'Wang' 대조 (2014 · 다른 학술지) | 없음 |
| 24 | A. Kato, M. Nose, M. Yamamoto, A. Sakuda, A. Hayashi, M. Tatsumisago, Mechanical properties of sulfide glasses in all-solid-state batteries, J. Ceram. Soc. Jpn. 126 (2018) 719–727. | 황화물 분말의 비선형 응력–변형 근거 [24–26] — 질문 c | 없음 (var2026 이 인용만) |
| 25 | A. Sakuda, A. Hayashi, Y. Takigawa, K. Higashi, M. Tatsumisago, Evaluation of elastic modulus of Li2S–P2S5 glassy solid electrolyte by ultrasonic sound velocity measurement and compression test, J. Ceram. Soc. Jpn. 121 (2013) 946–949. | 같은 근거 (wishlist batch_45 줄에 이미 있음) | 없음 |
| 22 | Y. Nagano, Y. Ikeda, H. Kawamoto, N. Takano, Image-based modeling by 3-D CT for homogenization stress analysis - application to porous ceramics -, 52, 2004, https://doi.org/10.11396/jjsndi.53.701, 701-701. | VOXELCON · 영상 기반 균질화 응력 해석의 원 방법 (학술지 이름 빠진 서지) — 질문 f · h | 없음 |
| 15 | G. Bucci, T. Swamy, S. Bishop, B.W. Sheldon, Y.-M. Chiang, W.C. Carter, The effect of stress on battery-electrode capacity, J. Electrochem. Soc. 164 (2017) A645. | 활물질 응력 · 용량 (서론 근거) — 질문 d · j | 없음 (`bucci2017_chemomech_failure_assb_cycling_czm` 은 다른 Bucci 2017 · JMCA) |
| 14 | R. Koerver, W. Zhang, L. Biasi, S. Schweidler, A.O. Kondrakov, S. Kolling, T. Brezesinski, P. Hartmann, W.G. Zeier, J. Janek, Chemo-mechanical expansion of lithium electrode materials – on the route to mechanically optimized all-solid-state batteries, Energy Environ. Sci. 11 (2018) 2142–2158. | 활물질 부피 변화 · 응력 | `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` |
| 16 | A. Sakuda, A. Hayashi, M. Tatsumisago, Sulfide solid electrolyte with favorable mechanical property for all-solid-state lithium battery, Sci. Rep. 3 (2013) 2261. | 'known value' 비교 · 가압 → 빈틈 · 입계 감소 | `sakuda2013_sulfide_mechanical_property` |
| 5 | N. Kamaya, K. Homma, Y. Yamakawa, M. Hirayama, R. Kanno, M. Yonemura, T. Kamiyama, Y. Kato, S. Hama, K. Kawamoto, A. Mitsui, A lithium superionic conductor, Nat. Mater. 10 (2011) 682–686. | LGPS 합성 · σ | `kamaya2011_lgps_lithium_superionic_conductor` |
| 7 | H.-K. Tian, Y. Qi, Simulation of the effect of contact area loss in all-solid-state Li-ion batteries, Electrochem. Soc. 164 (2017) E3512. | 접촉 면적 감소 계산 (서론 근거) | 없음 (위시 W-1117-3 차례) |
| 9 · 10 · 28 | Hlushkou 2018 · Froboese 2019 · Bielefeld 2020 (원문 [9] · [10] · [28]) | 빈틈 · 미세구조 · 굴곡 → σ | `hlushkou2018_…` · `froboese2019_…` · `bielefeld2020_…` |
| 27 | M. Tanaka, Y. Okuno, Plasma behavior in a high-temperature noble gas plasma disk-shaped MHD power generator, Electr. Eng. Jpn. 197 (2016) 33–40. | 'Maxwell equations' 계산 절차의 출처 (kodama2020 의 [15] 와 같은 논문 — 방법 추적만) | 없음 |

---

## [미확인] 목록
- 복합체 σ 절대값 (네 분율) · 순수 SE 시료의 단면 · 그림 5 본 곡선을 낸 시료 · 맞춤 식 · 측정 온도.
- 혼합 방법 · ZrO₂ 부피 분율을 낸 방법 · 가압 방법 · 셀 원통 재료 · 하중 측정.
- CT 투영 수 · 재구성 · 분할 문턱 · 기공 (CT 로 안 보임).
- 복셀 FEM 요소 종류 · 풀이기 · 수렴 · 시간 · 메모리 · GPU · 상 경계 조건 (결합 가정 [카드 추론]).
- E_SE 0.3 GPa 의 시험 조건 · 그 계산의 응력 분포 · 그림 6a 의 E · 그림 8 의 단면 · Case · E.
- 그림 6a 의 세는 단위 · 구간 폭 (넓이 비 0.69 의 원인) · 본문 '최빈 69 MPa' 의 정의.
- 오차 막대의 어느 끝이 어느 E 인지 · 막대 높이 (중간값) 의 정의.
- 수송 계산의 식 · 이산화 · 수렴 문턱 (본문 미기재 · [17] 참조).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-17)
- 서지: 1저자 메모 (Ohashi · Kodama · Sun · Hori · Suzuki · Kanno · Hirai, J. Power Sources 470 (2020) 228437) = 원문 첫 쪽과 같음 · DOI 10.1016/j.jpowsour.2020.228437 = 첫 쪽 · PDF 메타데이터 ('subject' 칸) 와 같음 · 10 쪽 · SI · 부록 안내 없음 ('supplementary' 0 회).
- 숫자: 텍스트 층 + 10 쪽 렌더로 대조 — 470 · 228437 · 1 mm · 0.3 mm · 1~2 mm · 100 MPa · 0.1 mA/cm2 · < 40 · < 150 µm · 4 × 4 × 5 µm · 160 kV · 41 vol% · 300 × 300 × 400 · 21.7 · 0.3 GPa · 200.0 GPa · 0.37 · 0.30 · 66 · 69 MPa · 67 vol% · ≈50 MPa · 19 · 42 · 55 · 67 vol% · t = 2.7 · 0.8 mm (삽도) · 그림 8 색 막대 0–100 MPa · 0–80 A/m² — 전부 위치 확인.
- 낱말 전수 (텍스트 층): 'hardness' 0 · 'NCM' 0 · 'NMC' 3 · 'LPSCl' · 'Li6PS5' · 'argyrodite' 0 · 'porosity' 0 · 'void' 20 (전부 정성) · 'contact' 4 (서론 둘 · 'intimate contact' · 'particle contact area') · 'plastic' 0 · 'unload' · 'decompress' · 'release' 0 · '140' = 참고문헌 [2] 번호 안 · 'Wang' 2 ([23] · [26]).
- 판독 보정: 그림 5 (로그 10 진 간격 241.8 px · 작은 눈금 log 간격과 맞음) · 6a · 6b · 7 의 큰 눈금 선 위치로 직선 환산 · 그림 6b 의 42 · 67 vol% 점 (66.05 · 48.89) 이 본문 66 · ≈50 과 맞음 · 그림 7 막대 = 오차 중간과 0.03 안.
- 정본 중복 확인: papers/ 목록 (596) · 'ohashi' · 'kodama' · 'hirai' 파일 이름 · DOI · '228437' · 'Stress distribution in the composite' grep — 카드 없음 (sakka2022 L363 · heck2026 L305 · kodama2020 L363 의 인용만).

## 🔗 관련 카드
- 이 논문을 인용한 카드: `sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps` (ref 24 · §0-1) · `heck2026_densification_sulfide_se_binder_scalable` (ref 61 · CL-90 표지) · `kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation` (§12 끝 '같은 그룹 · 이 논문이 인용하지 않은 후속' 줄).
- 같은 그룹 앞 논문 (이 논문 [17]): `kodama2020_high_pressure_insitu_xct_sulfide_se_voxel_simulation` (순수 황화물 누른 채 CT · 복셀 FV ↔ EIS).  같은 그룹 후속 Ohashi · Kodama · Horikawa · Hirai, J. Power Sources 483 (2021) 229212 (sakka2022 ref 25) = 정본 카드 없음 (11-17 기준).
- 강성이 다른 두 성분 압축 (DEM · 하중 몫 안 잼): `yano2024_eepa_binary_mixture_plasticity_compression_dem`.
- 탄성 상수: `deng2016_elastic_superionic_electrolytes_dft` · AM 영률: `koerver2018_chemomechanical_expansion_partial_molar_volume_operando_stress_ssb` (표 1 · LCO · NCM111) · `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` (NMC811 · CL-90 교체 출처).
- 미세구조 → σ: `hlushkou2018_void_space_ion_transport_assb_cathode` · `froboese2019_microstructure_ionic_conductivity_assb_electrode` · `bielefeld2020_effective_ionic_conductivity_binder`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

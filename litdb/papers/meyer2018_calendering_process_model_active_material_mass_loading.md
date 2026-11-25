<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md ·
     본 카드 = kollenda2024_time_sensitivity_calendered_electrode_springback_storage.md (절 번호 · 머리 상자 · 표 꼴) ·
     형식 이웃 = meyer2017_calendering_compaction_resistance_line_load_exponential_model.md (같은 그룹의 앞 논문 = 이 논문 참고 [22] · 같은 캘린더 · 같은 식의 밀도 꼴 · 전극 No.13 · 15 의 출처).
     쪽 표기 = 학술지 인쇄 쪽 p.371–379 (PDF 쪽 n = 인쇄 370 + n).  SI 없음.
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 — 이 논문의 그림 1–10 은 전부 PDF 에 박힌 **300 dpi 래스터** 라 벡터 좌표가 없다 →
     박힌 원본 래스터를 그대로 꺼내 (다시 표본화하지 않음) 축 눈금 · 격자선의 픽셀 위치로 좌표를 맞추고 (눈금 맞춤 잔차 ≤ 0.6 px = Fig 2 기공률 0.0005 · Fig 6 0.3 N/mm · Fig 10 0.4 N/mm) 표지를 읽었다:
     네모 = 외곽 상자 중심 (= 오차 막대 두 끝 (cap) 의 가운데) · 세모 = **무게중심** (밑변에서 높이의 1/3 — 상자 중심으로 읽으면 0.0036 어긋난다 · cap 가운데와 대조해 확인) · 빈 표지 = 속 구멍의 무게중심 · 막대 = 윗변 줄 ·
     겹친 표지는 6–8 배 확대 (±0.003–0.004) · Fig 9 의 계열 6 · 7 · 9 · 10 · 11 은 일부 점만 (겹침) · Fig 5 의 두 점은 낮은 신뢰 (digitized.csv 에 표지).
     검증 일곱 = (가) Fig 2 의 압연 전 기공률 = 표 2 의 1 − Σ vol% (15 중 13 이 ≤ 0.001) (나) 빨간 원 = 0.4 × 네모 (다) 본문 인쇄 계수 0.33 · 0.60 · 0.29 = 판독 비 0.338 · 0.605 · 0.295 (라) Fig 6 막대 = 표 3 의 μ × 223 g/m² (≤ 3 N/mm)
     (마) Fig 10 일곱 점의 원점 통과 재맞춤 μ = 1.310 (인쇄 1.31 ± 0.03) (바) Fig 5 · 9 곡선의 마지막 두 점 평균 = Fig 2 의 달성 최소 (11 중 10 이 ≤ 0.001) (사) 판독점에 식 (4) 를 한 수로 재맞춤한 γ_C 가 전부 인쇄 오차 막대 안.
     재현 = litdb/figures/<slug>/digitized.csv 168 행 · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 추정] = **원문에 없는 식 · 가정**을 이 카드가 넣어 만든 어림 (코팅 두께 · 접촉 길이 · 평균 압력 — 원문 값이 아니다 · 인용 금지) ·
     [카드 추론] = 이 카드의 해석 · [미확인] = 원문 (본문 9 쪽 전수) 에 없음.  본문은 텍스트 층과 쪽 렌더 이미지로 다 읽었고 크롭 57 장을 전부 열어 봤다. -->
# 압연 공정 모형 — 선하중 → 압연 뒤 코팅 기공률을 Heckel 꼴 지수 식 ε_C = ε_C,0·(p + (1 − p)·exp(−q_L/γ_C)) 한 줄로: 끝값 (최소 기공률) 을 압연 전 값의 0.4 배로 미리 정해 (같은 크기 구의 단순 입방 47.64 % ↔ 입방 조밀 25.95 % 충전의 비 0.54 에서 출발 · 실측에 맞춰 낮춤) 맞춤 수를 'compaction resistance' γ_C 하나로 줄임 — 활물질별 γ_C: NCA · NCM622 · NCM111 ≈ 297–310 ↔ NCM811 · NCA-80/20 ≈ 220–230 N/mm (223 g/m²) · 면적 부하에 비례 γ_C = μ·M_C (μ 1.31 ± 0.03 kN·m/g · 80–284 g/m²) — ⛔ 압력 (MPa) 이 아니라 선하중 (환산 없음) · 압연 뒤 값 · 구형 활물질 · 첨가제 ≤ 10 wt% 한정 · 되돌아옴 측정 · 입자 계산 없음 — Meyer · Kosfeld · Haselrieder · Kwade (J. Energy Storage 18, 2018)

> slug `meyer2018_calendering_process_model_active_material_mass_loading` · DOI `10.1016/j.est.2018.05.018` · type `experiment + empirical process model (파일럿 2 롤 캘린더 GKL 400 · 롤 힘 → 선하중 · 질량 + 두께 + He 피크노미터 밀도 → 압연 뒤 코팅 기공률 · Heckel 꼴 지수 식 + 최소 기공률 예측 p = 0.4 · 맞춤 수 γ_C 하나 · 활물질 입자 미세압축 파괴 세기 — 입자 계산 없음 (DEM · FEM · MPM 없음) · 액체 전해질 LIB 양극 · 압력 환산 없음)` · PDF `345d91e1-61._Process_modeling_of_the_electrode_calendering_of_lithium-ion_batteries_regarding_variation_of_cathode_active_materials_and_mass_loadings.pdf` · digested `2026-11-12` · status ✅
>
> **저자**: **Chris Meyer\*** (a, b) · Malte Kosfeld (a, b) · Wolfgang Haselrieder (a, b) · Arno Kwade (a, b) — a Institute of Particle Technology, Technische Universität Braunschweig (Volkmaroder Straße 5, 38104 Braunschweig) · b Battery LabFactory Braunschweig, TU Braunschweig (Langer Kamp 8, 38106 Braunschweig) · *Journal of Energy Storage* **18** (2018) 371–379 · 접수 2018-04-11 · 수정 2018-05-25 · 승인 2018-05-26 · 온라인 2018-06-19 · © 2018 Elsevier Ltd. All rights reserved (공개 접근 표지 없음 · 2352-152X) · 키워드 Calendering · Compaction model · Lithium-ion battery electrodes · Porosity · Ni-rich cathode materials · Mass loading · 연구비 S-ProTrak (01MX13003B · Federal Ministry of Economic Affairs and Energy) + ProKal (03XP0077A · Federal Ministry of Education and Research) [인쇄 p.371 · p.378].
> **이웃 카드 (링크만)**: [`meyer2017_calendering_compaction_resistance_line_load_exponential_model`](meyer2017_calendering_compaction_resistance_line_load_exponential_model.md) (같은 그룹의 **앞 논문** = 참고 [22] — 식 (2) 의 밀도 꼴 · 같은 캘린더 · 전극 No.13 · 15 의 출처) · [`kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation`](kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation.md) (이 논문을 가리킨 카드 · 참고 27) · [`kollenda2024_time_sensitivity_calendered_electrode_springback_storage`](kollenda2024_time_sensitivity_calendered_electrode_springback_storage.md) (참고 [39] 로 인용 — 2 차 서술 대조 §0-1) · [`diener2022_roll_gap_springback_calendering`](diener2022_roll_gap_springback_calendering.md) (같은 그룹 · 같은 캘린더 · 이 논문에 없는 **롤 간극 · 순간 회복**) · [`lu2020_insitu_nanoct_calendering_microstructural_evolution`](lu2020_insitu_nanoct_calendering_microstructural_evolution.md) (참고 12 로 인용) · [`heck2026_densification_sulfide_se_binder_scalable`](heck2026_densification_sulfide_se_binder_scalable.md) (같은 계열 식을 **압력** 축으로 β-Li₃PS₄ 에) · [`song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage`](song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage.md) (입자 하나의 파괴 = 명목 응력 f_max/d²) · [`onoda1990_random_loose_packing_uniform_spheres_dilatancy_onset`](onoda1990_random_loose_packing_uniform_spheres_dilatancy_onset.md) (같은 크기 구의 느슨한 무작위 충전) · [`lee2025_heckel_argyrodite_powder_densification_nanoindentation`](lee2025_heckel_argyrodite_powder_densification_nanoindentation.md) (LPSCl 가루의 압력 축 Heckel).
> **판독 원자료**: `litdb/figures/meyer2018_calendering_process_model_active_material_mass_loading/digitized.csv` (168 행 — Fig 2 압연 전 · 달성 최소 · 외삽 최소 · 예측 최소 60 행 · Fig 5 선하중 ↔ 기공률 44 행 · Fig 9 선하중 ↔ 기공률 46 행 · Fig 10 부하 ↔ γ_C 7 행 · Fig 6 막대 5 행 · Fig 7 파괴 세기 6 행) · 그림 크롭 57 장 (그림 10 + 패널 10 · 표 3 · **식 14** (식 (1)–(5) 를 식만 / 앞뒤 문장과 함께 두 장씩 + 번호 없는 정의식 셋 + Fig 10 의 맞춤 상자) · 근거 문단 20 — 도구가 자른 그림 10 · 표 3 은 여백 · 범위가 틀려 **13 장 전부 다시 잘랐다**) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 파일럿 2 롤 캘린더 (GKL 400 · 롤 Ø430 mm · 최대 1500 N/mm · 최소 설정 간극 25 µm · 상온) 에서 **액체 LIB 양극 12 종** — 활물질만 바꾼 다섯 (NCA-80/20 · NCA · NCM811 · NCM622 · NCM111 · 활물질 94 wt% · 223 g/m²) 과 면적 부하만 바꾼 일곱 (NCM111 90 wt% · 80–284 g/m²) — 을 간극을 바꿔 가며 누르고, 롤 힘 ÷ 코팅 폭 = **선하중 q_L (N/mm)** 과 **압연 뒤** 질량 · 두께 · He 피크노미터 밀도로 셈한 코팅 기공률 ε_C 를 견주면 **ε_C = ε_C,0·(p + (1 − p)·exp(−q_L/γ_C))** (식 (4) · p = 0.4) 로 적힌다 — 앞 논문 (Meyer 2017) 에서 외삽 맞춤값이던 끝값 (최소 기공률) 을 **압연 전 기공률의 0.4 배**로 미리 정해 맞춤 수를 **'compaction resistance' γ_C 하나**로 줄였고, 그 γ_C 는 면적 부하에 비례한다 (**γ_C = μ·M_C** · μ = 1.31 ± 0.03 kN·m/g · 식 (5)).  ⛔ '같은 크기 구의 이론 충전' 이 0.4 를 **주지는 않는다** — 단순 입방 47.64 % → 입방 조밀 25.95 % 의 비 0.54 를 출발점으로 삼았다가 실측에 맞춰 0.4 로 낮춘 *"an appropriate estimation of practical use"* 다 (p.374).  원문은 **선하중을 압력으로 바꾸지 않았고**, 모든 기공률은 **롤을 빠져나온 뒤** 값이며, **되돌아옴 측정 · 입자 계산 (DEM · FEM) · 고체전해질은 없다**.

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 모델 식 (번호별) | 식 (1) Heckel [인쇄 그대로] **ε = ε0 + exp(−K·P)** (⚠ 덧셈표 = 인쇄 오류 — P = 0 에서 ε0 + 1 · Heckel 의 꼴은 ε = ε0·exp(−K·P)) · 식 (2) **ε_C = ε_C,min + (ε_C,0 − ε_C,min)·exp(−q_L/γ_C)** (앞 논문 식의 기공률 꼴 · 맞춤 수 둘 = ε_C,min · γ_C) · 식 (3) **ε_C = 1 − ρ_C/ρ_ph = 1 − (m_E − m_C)/((h_E − h_C)·ρ_ph)** (기공률 연산자) · 식 (4) **ε_C = ε_C,0·(p + (1 − p)·exp(−q_L/γ_C))** (끝값 = p·ε_C,0 을 넣은 꼴 · 맞춤 수 하나) · 식 (5) **ε_C = ε_C,0·(p + (1 − p)·exp(−q_L/(μ·M_C)))** (⚠ 인쇄는 나눗셈표가 빠진 exp(−q_L(μ·M_C)) — 바로 위 문장 γ_C = μ·M_C 로 뜻이 정해진다) · 번호 없는 정의: q_L = F_N/w_C · ε_C,min_p = p·ε_C,0 (p = 0.4) · γ_C = μ·M_C | [인쇄] p.372 · p.373 · p.374 · p.375 · p.378 · 크롭 `eq_01_*` – `eq_05_*` · `eq_p37*_inline` |
| ② 매개변수의 뜻 | **ε_C,0** = 압연 전 기공률 (실측 입력 · 맞추지 않음) · **p = 0.4** (전 전극 공통 · 고정) · **γ_C [N/mm]** = 유일한 맞춤 수 — *"functions as a reciprocal equivalent to Heckels constant K"* · **μ [kN·m_length/g = (N/mm)/(g/m²)]** = γ_C ÷ 면적 부하 (부하 의존을 뺀 수) · q_L = 롤 힘 ÷ 코팅 폭 | [인쇄] p.372 · p.373 · p.378 |
| ③ ★ 활물질별 (부하 223 ± 1 g/m² · 94 / 3 / 3 wt%) | γ_C [판독 Fig 6]: NCA-80/20 **220 ± 29** · NCA **310 ± 25** · NCM811 **230 ± 22** · NCM622 **305 ± 21** · NCM111 **297 ± 36** N/mm — μ [인쇄 표 3]: **0.99 ± 0.13 · 1.40 ± 0.11 · 1.04 ± 0.10 · 1.36 ± 0.09 · 1.33 ± 0.16** kN·m/g (μ × 223 = 221 · 312 · 232 · 303 · 297 ✓) · 압연 전 기공률 [판독 Fig 2] 0.450 · 0.457 · **0.479** · 0.461 · 0.443 · 달성 최소 0.201 · 0.204 · 0.215 · 0.213 · 0.202 (선하중 ≈720–796 N/mm) | [인쇄] 표 3 p.378 · [판독] Fig 2 · 5 · 6 · §3-5 |
| ④ ★ 부하별 (NCM111 · 90 / 5 / 5 wt%) | M_C **80 ± 2 · 120 ± 3 · 161 ± 3 · 179 ± 3 · 198 ± 3 · 242 ± 2 · 284 ± 4** g/m² [인쇄 표 2] ↔ γ_C **98 ± 11 · 164 ± 11 · 168 ± 11 · 254 ± 12 · 249 ± 16 · 340 ± 14 · 371 ± 5** N/mm [판독 Fig 10] · 직선 γ_C = μ·M_C · **μ = 1.31 ± 0.03** (N/mm)/(g/m²) · **R² = 0.996** [인쇄 — 원점 통과 맞춤의 비중심 R²: 평균 기준으로는 0.948 · 161 g/m² 점이 직선보다 21 % 낮다 · 카드 산술 §3-6] · 압연 전 기공률 0.548 · 0.484 · 0.441 · 0.437 · 0.436 · 0.424 · 0.425 · 달성 최소 0.238 · 0.214 · 0.188 · 0.197 · 0.192 · 0.199 · 0.190 (마지막 선하중 ≈300 · 424 · 479 · ≈570 (겹쳐 불확실) · 659 · 751 · 867 N/mm) | [인쇄] 표 2 · 표 3 · Fig 10 상자 · [판독] Fig 2 · 9 · 10 · §3-6 |
| ⑤ ★ 최소 기공률 예측이 맞는가 | 원문: No.1–12 에서 *"the prediction approach works quite well"* · No.13–15 에서는 *"significantly worse"* (맞는 계수 = NCM + 도전 흑연 양극 **0.33** · LMO **0.60** · 흑연 음극 **0.29**) → *"No. 13–15 are not further discussed"*.  [판독 + 카드 산술] No.1–12: **달성 최소 ÷ 압연 전 = 0.427–0.471 (평균 0.447)** · **외삽 최소 ÷ 압연 전 = 0.354–0.444 (평균 0.398)** ⇒ p = 0.4 는 **앞 논문 식으로 외삽한 끝값의 평균**과 같고, 기계가 실제로 닿은 최소는 그보다 기공률 0.012–0.030 (rms 0.022) 높다 | [인쇄] p.374–375 · [판독] Fig 2 · §3-4 |
| ⑥ ★ 맞춤 품질 | 그림 범례의 reduced χ²: 활물질 다섯 **2.24–4.00** (Fig 5) · 부하 일곱 **0.19–5.83** (Fig 9) — 캡션은 *"the approximations describe the data courses visually sufficiently well for practical purposes"* · γ_C 표준오차 1.4–13 % (결론: *"The maximum is 12 %"*) · [카드 산술] 판독점과 인쇄 매개변수 곡선의 차 = rms 0.004–0.021 · 최대 0.037 (기공률) · 잔차 무늬 (활물질 다섯) = 낮은 선하중 (≤ 55 N/mm) 에서 모델이 0.02–0.04 높고 중간 (≈270–480 N/mm) 에서 0.01–0.02 낮다 | [인쇄] Fig 5 · 9 범례 · 캡션 · p.378 · [카드 산술] §3-5 · §3-6 |
| ⑦ ★ 적용 범위 | *"limited to the application of spherical active materials and additive contents up to 10 wt.-%"* · *"valid by all means for relevant mass loadings MC > 80 g/m2"* (≈ 입자 세 층 · 45 µm · 1.1 mAh/cm² 이상) · 기계 한계 = 선하중 ≤ 1500 N/mm · 최소 간극 25 µm · 상온 · 활물질은 공급사가 서로 달라 Ni 함량 효과는 *"no general validity"* | [인쇄] p.376 · p.378 |
| ⑧ ★ 선하중은 압력이 아니다 | q_L = F_N/w_C (롤 힘 ÷ 코팅 **폭**) — 접촉 **길이** 로 나누지 않은 값.  원문에 압력 환산 · 접촉 길이 · 하중 아래 간극 · 롤 속도 · 코팅 폭 수치가 **없다** (텍스트 층에 'MPa' 0 회 — Fig 7 축의 입자 파괴 세기에만) | [인쇄] p.373 · [미확인] · §3-9 |
| ⑨ ★ 기공률 정의 | **기하 한 가지** — 질량 부하 (초음파 감쇠 · 건조 직후) + 두께 (다이얼 게이지 1 µm · 24 점) + 성분 He 피크노미터 밀도의 평균 ρ_ph → 식 (3).  **수은 압입 기공률은 싣지 않았다** — 수은 압입에서 온 값은 인용 둘 ([22] 활물질 사이 기공 지름 2 µm · [11] LMO 의 기공 부피비 3.27) 과 No.8 의 기공 부피비 ≈1.34 (방법 서술 없음) 뿐이고, 두 방법의 일치는 *"in well corresponce with the porosities measured by mercury porosimetry [22,23]"* 한 문장 | [인쇄] p.372 · p.374 |
| ⑩ ★ 누른 채인가 뺀 뒤인가 | **압연 뒤 (하중 0)** — 되돌아옴은 *"The coating relaxes elastically when it leaves the gap."* 한 문장 (크기 · 시간 · 측정 없음) · 압연 뒤 두께 측정까지의 시간 [미확인] | [인쇄] p.371 |
| ⑪ 활물질 입자의 세기 | 미세압축 (지름 100 µm 원기둥 압자 · 2.8 mN/s · 입자 ≥ 24 개 · 첫 파괴 힘 ÷ 투영 면적) 파괴 세기 중앙값 [판독 Fig 7]: 흑연 ≈30 · **NCM811 ≈63** · NCAI ≈117 · NCM622 ≈139 · NCM111 ≈274 · NCAII ≈347 MPa — Ni 함량이 높을수록 약하다 (공급사가 달라 일반화 불가) · 저자 결론 = 파괴 세기는 γ_C 의 **지배 인자가 아니고** 입도 분포 · 표면이 정하는 **마찰** 이 지배 (초기 재배열 단계) | [판독] Fig 7 · [인쇄] p.375–376 · §3-8 |
| ⑫ 앞 논문 (2017) 과의 관계 | 2017 의 3 수 식 (시작 · 외삽 끝 · γ_C) → 끝값을 p·ε_C,0 로 고정한 1 수 식 · 2017 의 두 전극이 No.13 · 15 로 다시 나오는데 **양극 No.13 의 기공률이 달라졌다** (압연 전 0.57 → 0.521 · 최소 0.26 → 0.176 / 0.169) — [카드 산술] 분모 밀도를 4.3 → 3.84 g/cm³ 로 바꾼 것과 같고 그러면 2017 의 '수은 압입보다 ≈8 %p 높다' 가 사라진다 | [인쇄] 표 2 · [판독] Fig 2 · [카드 산술] §3-11 |
| ⑬ 가리킨 카드 · wishlist 서술과 같은가 | **일부만** — '캘린더링 공정 모형' = 맞음 · 'DEM 압밀 대조' = 원문에 DEM 없음 · '압력 축' = 없음 (선하중) · **'두께가 되돌아옴을 줄이는 근거' = 원문에 없음** (§0-1) | §0-1 |
| ⑭ 입자 계산 | **없음** — DEM · 'simulation' · 'discrete' 0 회 (인용 = 저항망 유효 전도 [8] · 다입자 유한요소 [27] 한 문장) | §4-4 |

⛔ **한정어 (떼지 말 것)**: ① **액체 전해질 LIB 압연 양극** (고체전해질 없음 · 바인더 3–5 wt% + 도전 탄소 3–5 wt% · 압연 전 기공 42–55 %) ② **선하중 (N/mm) 이지 압력이 아니다 — 원문에 환산 없음** ③ **압연 뒤 (하중을 뺀 뒤) 값** ④ **p = 0.4 는 경험 계수** (충전 이론 값 0.54 가 아니다 · 구형 활물질 · 첨가제 ≤ 10 wt% · M_C > 80 g/m² 안에서만 · 다른 세 전극은 0.29 · 0.33 · 0.60) 이고 **끝값은 기계가 닿은 값이 아니라 점근값** (닿은 최소는 0.447 × 압연 전) ⑤ γ_C 는 **재료 상수가 아니다** — 면적 부하에 비례하고 (μ 가 그 몫을 뺀 수) 활물질 다섯의 μ 는 부하 한 수준 (223 g/m²) 에서 선형 가정으로 옮긴 값 ⑥ 활물질 다섯은 입도 · 표면 · 세기 · 공급사가 함께 다르다 (원인 분리 안 됨) ⑦ 롤 속도 · 통과 횟수 · 코팅 폭 · 집전체 두께 [미확인] · 온도 한 수준.
⇒ **절대값 전이**: 하지 않는다 (재료 · 하중 단위 · 상태가 다 다르다).  **전이 가능한 것** = (i) 압밀 곡선을 '시작점 × (끝값 비 + 지수 감쇠)' 로 적고 끝값을 따로 정해 맞춤 수를 하나로 줄이는 꼴과 그 함정 (끝값 비는 재료 · 조성 · 분모 밀도에 따라 0.29–0.60 · 점근값 ≠ 닿은 값 · 한 지수로는 초기의 빠른 감소를 못 따른다) (ii) 선하중 기준 저항이 코팅 질량에 비례한다는 사실 = 압연 문헌의 N/mm 는 두께가 다르면 서로도 견줄 수 없다 (iii) 혼합물 고체 밀도를 어떻게 평균하느냐가 기공률을 5–9 %p 움직인 실례 (No.13) (iv) 얇은 코팅 (입자 ≈3 층) 은 압연 전 기공률이 ≈0.12 높다 (0.548 ↔ 0.42–0.44 · 벽 · 표면 효과).

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-61 의 '왜' 칸 + 지시서 덧붙임)

의도 원문: *"후보 M0 · 단계 5 (결과 전 대조) — "캘린더링 공정 모형 (DEM 압밀 대조)" · LIB 전극"* (후보 표 N-61 · 근거 = `kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation` L421) · 지시서 덧붙임: *"'Heckel 기반 모델 식 + 같은 크기 구의 이론 충전 구조로 최소 기공률을 예측'. 모델 식 · 매개변수 · 활물질별 (Ni-rich 포함) · 질량 부하별 값 · 맞춤 품질 · 적용 범위를 표로. 식은 번호별로 따로 자른다. 선하중 ↔ 압력 환산이 원문에 있는지 · 기공률 정의 (기하 / 수은 압입) · 압연 뒤 (뺀 뒤) 값인지. wishlist 의 batch_64 줄 ('두께가 되돌아옴을 줄이는 근거' · kollenda2024 §3-3 · §12 [39]) 이 원문과 같은지"*.

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "캘린더링 공정 모형" | **채움** | 식 (2) → (4) → (5) (p.372 · p.375 · p.378) — 선하중 ↔ **압연 뒤** 코팅 기공률 · 맞춤 수 γ_C 하나 (p = 0.4 고정 · ε_C,0 실측) · 서론: *"there are to date no approaches to develop a process model for the calendering of battery electrodes"* (p.372) |
| "(DEM 압밀 대조)" | **없음** (논문 안에 DEM 없음) | 입자 계산이 없다 — 'DEM' · 'discrete' · 'simulation' 0 회 (본문).  우리 DEM 압밀의 **대조 값**으로도 못 쓴다: 축이 N/mm (압력 환산 없음) · 고체전해질 없음 · 뺀 뒤 값.  (압연 DEM 카드 `sangros2019_*` · `schreiner2020_*` · `ngandjong2021_*` 가 표적으로 삼는 종류의 자료이기는 하다) |
| "LIB 전극" | **채움** | 액체 전해질 LIB 양극 12 종 (NCA · NCM111 · 622 · 811) + 다른 연구의 세 전극 (NCM + 도전 흑연 양극 · LMO 양극 · 흑연 음극) — 표 1 · 표 2 (p.373) |
| "Heckel 기반 모델 식" | **채움** (한정 둘) | 초록 *"a Heckel-based model equation"* · 식 (1) → (2): *"This exponential relation was transferred to Eq. (2) … The compaction resistance γC functions as a reciprocal equivalent to Heckels constant K [22]"* (p.372).  한정 ① 하중 변수가 압력 P 가 아니라 **선하중 q_L** (환산 없음) ② 인쇄된 식 (1) 은 덧셈표 오류 (ε = ε0 + exp(−K·P)) · 식 (2) 는 Heckel 에 **끝값 ε_C,min 을 더한 꼴** (Heckel 은 끝값 0) — 앞 논문에서는 *"reminds of"* 였다 (meyer2017 카드 §3-10) |
| "같은 크기 구의 이론 충전 구조로 최소 기공률을 예측" | **일부** | 초록: *"a predictive model for the lowest achievable coating porosity based on the theoretical packing structures of equally sized spheres"*.  본문 (p.374): 끝값 = p × 압연 전 값 이라는 **가정**을 단순 입방 (47.64 %) ↔ 입방 조밀 (25.95 %) 의 비 **0.54** 로 세운 뒤, 전극의 최소가 그보다 낮아 *"Therefore p has to be much smaller for the electrodes. The proposed p = 0.4 turns out to be an appropriate estimation of practical use."* — **0.4 는 충전 구조에서 나온 값이 아니라 실측에 맞춘 값**이다.  조건: 구형 활물질 · 첨가제 ≤ 10 wt% · No.1–12 (압연 전 0.42–0.55 → 예측 0.17–0.22 ↔ 달성 0.19–0.24 [판독]) · 기하 기공률 · 압연 뒤 · 상온 |
| "후보 M0" (입자를 풀지 않는 압밀 식) | **채움** (꼴 · 함정) | 1 수 현상 곡선 + 그 한계 (끝값 비의 재료 의존 0.29–0.60 · 점근값 ≠ 닿은 값 · 한 지수의 잔차 무늬 · γ_C ∝ 부하) — §3-4 – §3-7 · §8 |
| "단계 5 (결과 전 대조)" (3D 복합 가압) | **없음** | 고체전해질 없는 액체 LIB 코팅 · 압력 없음 · 뺀 뒤 값 → 복합 (AM + SE) 가압의 대조 값이 못 된다.  정성 방향만: 작은 활물질 20 wt% 를 섞으면 γ_C 가 29 % 낮다 (310 → 220 N/mm) · 얇은 코팅은 덜 조밀하다 |
| ★ 모델 식 · 매개변수를 표로 | **채움** | §0 ① ② · §3-3 |
| ★ 활물질별 (Ni-rich 포함) | **채움** | NCM811 γ_C 230 ± 22 N/mm (μ 1.04 ± 0.10) · NCM622 305 ± 21 (1.36 ± 0.09) · NCA 310 ± 25 (1.40 ± 0.11) · NCA-80/20 220 ± 29 (0.99 ± 0.13) · NCM111 297 ± 36 (1.33 ± 0.16) — 223 g/m² · 94 wt% · §3-5 |
| ★ 질량 부하별 | **채움** | 80–284 g/m² 일곱 수준 · γ_C 98 → 371 N/mm · μ 1.31 ± 0.03 — §3-6 |
| ★ 맞춤 품질 | **채움** (원문 지표 + 카드 재검) | reduced χ² 0.19–5.83 (범례) · R² 0.996 (Fig 10) · 표준오차 ≤ 12–13 % · [카드 산술] 잔차 rms 0.004–0.021 |
| ★ 적용 범위 | **채움** | 구형 활물질 · 첨가제 ≤ 10 wt% · M_C > 80 g/m² (p.376 · p.378) |
| ★ 식 크롭 (번호별) | **채움** | 식 (1)–(5) 를 식만 / 앞뒤 문장과 함께 각 2 장 + 번호 없는 정의식 3 + Fig 10 맞춤 상자 = 14 장 |
| ★ 선하중 ↔ 압력 환산이 원문에 있는가 | **채움** (= 원문에 **없다** 는 확인) | q_L = F_N/w_C (p.373) 뿐 — §3-9 (카드 추정은 원문 값이 아님) |
| ★ 기공률 정의 (기하 / 수은 압입) | **채움** | 기하 한 가지 (식 (3) · 질량 + 두께 + 성분 He 밀도의 평균) · 수은 압입 기공률 값은 없음 (인용 + No.8 의 기공 부피비 한 값) — §0 ⑨ |
| ★ 압연 뒤 (뺀 뒤) 값인가 | **채움** | **압연 뒤** — §0 ⑩ · §4-4 (iv) |
| wishlist batch_64 줄 "i — 활물질 · 부하별 압연 압축 곡선" | **채움** | Fig 5 (활물질 다섯) · Fig 9 (부하 일곱) — 단 고체전해질 없는 코팅 · 선하중 축 |
| wishlist batch_64 줄 "b — 두께가 되돌아옴을 줄이는 근거" | **없음** | 이 논문은 되돌아옴을 **재지 않았다** ('spring' 0 회 · 'relax' 1 회 = 위 한 문장).  두께 (부하) 에 대해 원문이 말하는 것은 ① 부하가 클수록 γ_C 가 크다 — *"the more friction between the particles has to be overcome as the friction area increases"* (p.376) ② 얇은 코팅은 압연 전 기공률이 높다 ③ 입자 한 층은 파괴 없이 못 누른다 — 셋 다 '두꺼운 층은 재배열 · 코팅의 소성 변형 기회가 많다' 나 '덜 되돌아온다' 가 아니다.  'plastic' 은 Heckel 의 K 설명에 한 번 (*"plastic deformability of the particular bulk"*) |

**가리킨 카드의 2 차 서술 대조** (고치지 않고 '카드 문제' 로 보고):
- `kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation` L421 — 서지 (저자 · 제목 · J. Energy Storage 18 (2018) 371–379) = 원문과 같다.  메모 *"캘린더링 공정 모형 (DEM 압밀 대조)"* 는 값을 싣지 않는다 — 앞 절반은 맞고, 괄호 안은 '우리 DEM 과 견줄 자리' 라는 기대이지 원문 내용이 아니다 (원문에 DEM 없음 · 견줄 압력 축도 없음).
- `kollenda2024_time_sensitivity_calendered_electrode_springback_storage` L122 · L171 (Kollenda 원문 인용 *"the higher coating thicknesses of higher mass loadings provide more opportunities for rearrangement of the particles and, therefore, plastic deformation of the coating [39, 40]"*) · L334 (§12 [39] 줄 *"활물질 · 부하별 압연 압축 곡선 · 두께 효과 (i · b)"*) — 그 카드는 Kollenda 의 문장을 옳게 옮겼다.  그러나 **[39] (= 이 논문) 에는 그 문장을 받칠 내용이 없다**: 부하가 클수록 압밀 저항이 **커진다** (마찰 면적) 는 것이 이 논문의 결과이고, 재배열은 *"in the early state of compaction"* 의 지배 기전이라는 문장 (p.376 · 금속 가루 문헌 [26] 인용) 과 결론의 *"interparticular friction during the rearrangement"* 뿐이다 — 두께와 재배열 기회 · 소성 변형 · 되돌아옴을 잇지 않는다.  ⇒ Kollenda 의 기전 문장 가운데 [39] 몫은 **원문 근거 없음** ([40] = Meyer 2020 Energy Technol. 은 이 작업에서 못 봄 [미확인]).  §12 [39] 줄의 "(i · b)" 가운데 b 는 채워지지 않는다.
- `lu2020_insitu_nanoct_calendering_microstructural_evolution` L423 (참고 12 · 왜 = *"압연의 압력 축 (이 논문에 없는 것)"*) — 서지는 같다.  기대와 달리 이 논문도 **압력 축을 주지 않는다** (선하중 N/mm · 환산 없음).
- `diener2022_roll_gap_springback_calendering` L79 (*"Meyer 압축 저항 γ_C 가 질량에 선형 증가 — 접점 수 · 마찰"*) · L217 (참고 17–19 · *J. Energy Storage* 2018, 18, 371) — 원문과 맞다 (γ_C = μ·M_C · 이유 = 마찰 면적).  같은 카드 L57 의 캘린더 치수 *"롤 Ø465 mm · 폭 430 mm"* 는 이 논문의 *"rolls of 430 mm in diameter and 465 mm in width"* (같은 GKL 400) 와 **지름 · 폭이 뒤바뀌어 있다** — 어느 쪽이 옳은지는 이 논문만으로 모른다 (앞 논문 2017 은 Ø450 × 470 mm · meyer2017 카드 §3-2) → §3-12.
- `meyer2017_calendering_compaction_resistance_line_load_exponential_model` — [미확인] 목록의 *"Froboese 외 (Mater. Charact.) 의 권 · 쪽"* 은 이 논문 참고 [23] 으로 풀린다: **Mater. Charact. 133 (2017) 102–111**.  §3-5 '약점 3' (분모 밀도) 은 이 논문의 No.13 값으로 뒷받침된다 (§3-11) · [미확인] 'NCM 조성' 도 NCM111 로 좁혀진다 (§3-1).  그 카드의 '예고' 줄 아래에 이 카드를 가리키는 한 줄만 더했다.

⇒ **의도 대조 결과: 일부** — 모델 식 · 매개변수 · 활물질별 (NCM811 · NCM622 · NCA 포함) · 부하별 값 · 맞춤 품질 · 적용 범위는 원문에 다 있다 (채움).  그러나 ① 'DEM 압밀 대조' 는 원문에 없고 (입자 계산 없음 · 선하중 축 · 고체전해질 없음 · 뺀 뒤 값이라 우리 가압 계산의 대조 값도 못 된다) ② '같은 크기 구의 충전 구조로 예측' 은 출발 가정일 뿐 쓰인 계수 0.4 는 경험값이며 ③ wishlist 가 기대한 '두께가 되돌아옴을 줄이는 근거' 는 원문에 없다.

---

## 1. 한 줄 요약
같은 파일럿 캘린더로 **활물질 다섯 · 면적 부하 일곱** 의 LIB 양극을 눌러, 앞 논문의 3 수 지수 식에서 끝값을 **압연 전 기공률 × 0.4** 로 고정하고 **'compaction resistance' γ_C 하나**만 맞추는 공정 식으로 줄인 논문 — γ_C 는 작은 입자를 섞거나 (NCA-80/20) 굵어서 처음에 성긴 (NCM811) 코팅에서 ≈25–30 % 낮고, 면적 부하에 비례하며 (μ = 1.31 kN·m/g), 입자 파괴 세기 (NCM811 ≈63 ↔ NCM111 ≈274 MPa) 와는 나란히 가지 않는다.  **압력 · 누른 채 상태 · 되돌아옴 · 입자 계산 · 고체전해질은 없다.**

## 2. 메타
| 항목 | 값 |
|---|---|
| 저자 · 소속 | Chris Meyer\* · Malte Kosfeld · Wolfgang Haselrieder · Arno Kwade — TU Braunschweig Institute of Particle Technology (iPAT) · Battery LabFactory Braunschweig (BLB) |
| 학술지 | *Journal of Energy Storage* 18 (2018) 371–379 · DOI 10.1016/j.est.2018.05.018 · 2352-152X |
| 날짜 | 접수 2018-04-11 · 수정 2018-05-25 · 승인 2018-05-26 · 온라인 2018-06-19 |
| 종류 | 실험 (공정 특성화 + 입자 미세압축) + 현상 맞춤 식 — 계산 · 모사 없음 |
| 분량 | 본문 9 쪽 · 그림 10 · 표 3 · 번호 식 5 (+ 번호 없는 정의식 3) · 참고문헌 27 · **SI 없음** · 자료 공개 문구 없음 |
| 재료 | 양극 활물질 NCAI · NCAII · NCM811 · NCM622 · NCM111 (공급사 서로 다름 · 이름 미인쇄) + 도전 탄소 + 바인더 (종류 [미확인]) · 비교용 = 다른 연구의 NCM + 도전 흑연 양극 (참고 [22]) · LMO 양극 (참고 [11]) · 흑연 음극 (참고 [22]) |
| 장치 | Saueressig GKL 400 파일럿 2 롤 캘린더 (Ø430 × 465 mm · 최대 1500 N/mm) · Mesys USM200 (초음파 질량 부하) · Mitutoyo ID-C 다이얼 게이지 (1 µm) · He 가스 피크노미터 (기종 [미확인]) · ASMEC UNAT (미세압축) · BET · SEM (기종 [미확인]) |
| 쪽 표기 | 인쇄 p.371–379 = PDF 1–9 쪽 |

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 전극 · 활물질 입자 (표 1 · 표 2 · p.373)
| No. | 이름표 | 활물질 · 입도 x10 / x50 / x90 (µm · 공급사 자료) | 모양 | 질량 분율 AM / CC / CG / B (wt%) | 부피 분율 AM / CC / CG / B (vol% · 압연 전 코팅) | 1 − Σ vol% [카드 산술] | 면적 부하 (g/m²) |
|---|---|---|---|---|---|---|---|
| 1 | NCA-80/20 | 80 wt% NCAI (7.2 / 15.2 / 29.1) + 20 wt% NCAII (3.1 / 5.8 / 9.1) | spheres | 94 / 3 / 0 / 3 | 45.9 / 4.3 / 0 / 4.2 | 0.456 | 223 ± 1 |
| 2 | NCA | NCAI 7.2 / 15.2 / 29.1 | 〃 | 〃 | 46.5 / 4.3 / 0 / 4.2 | 0.450 | 〃 |
| 3 | NCM811 | 8.1 / 14.3 / 24.7 | 〃 | 〃 | 44.0 / 4.1 / 0 / 4.0 | 0.479 | 〃 |
| 4 | NCM622 | 6.5 / 11.7 / 20.7 | 〃 | 〃 | 45.6 / 4.2 / 0 / 4.1 | 0.461 | 〃 |
| 5 | NCM111 | 6.4 / 12.0 / 21.6 | 〃 | 〃 | 47.4 / 4.2 / 0 / 4.1 | 0.443 | 〃 |
| 6 | 80 | (칸 비어 있음 = 위 줄 NCM111 과 같음으로 읽힘) | 〃 | 90 / 5 / 0 / 5 | 34.6 / 5.3 / 0 / 5.2 | 0.549 | 80 ± 2 |
| 7 | 120 | 〃 | 〃 | 〃 | 39.6 / 6.1 / 0 / 6.0 | 0.483 | 120 ± 3 |
| 8 | 160 | 〃 | 〃 | 〃 | 42.9 / 6.6 / 0 / 6.5 | 0.440 | 161 ± 3 |
| 9 | 180 | 〃 | 〃 | 〃 | 43.2 / 6.7 / 0 / 6.5 | 0.436 | 179 ± 3 |
| 10 | 200 | 〃 | 〃 | 〃 | 43.3 / 6.7 / 0 / 6.5 | 0.435 | 198 ± 3 |
| 11 | 240 | 〃 | 〃 | 〃 | 44.2 / 6.8 / 0 / 6.7 | 0.423 | 242 ± 2 |
| 12 | 280 | 〃 | 〃 | 〃 | 44.1 / 6.8 / 0 / 6.7 | 0.424 | 284 ± 4 |
| 13 | NCM cathode | (칸 비어 있음 · 본문은 'NCM111-451' 로 부름) | 〃 | 86 / 4 / 4 / 6 | 34.0 / 4.4 / 3.1 / 6.4 | 0.521 | 451 ± 14 (양면 코팅) |
| 14 | LMO | 5.5 / 9.1 / 14.6 | undefined polygones | 90 / 6 / 0 / 4 | 32.6 / 5.6 / 0 / 3.6 | 0.582 | 133 (표준편차 ≤ 3 %) |
| 15 | graphite anode | 14.3 / 20.4 / 27.7 (측정값) | flakes | 85 / 5 / 0 / 10 | 32.2 / 2.6 / 0 / 5.0 | 0.602 | 197 ± 3 (양면 코팅) |
- AM = active material · CC = conductive carbon · CG = conductive graphite · B = binder (표 2 캡션).  바인더 · 도전 탄소의 종류 · 공급사 · 용매 = [미확인].  도전 흑연 (No.13) x50 = 2.4 µm · x90 = 4.1 µm (p.374).
- *"The electrodes No. 1–5 vary in the active material used while the formulation and applied mass loading was kept constant.  No. 6–12 are produced in one mixing batch but coated with different mass loadings.  The last three electrodes (No. 13–15) are further examples from other studies (No. 14 [11], No. 13 and 15 [22]) to demonstrate the limits of the … prediction model"* (p.373) · 코팅 = doctor blade 연속 코팅 + 온도가 올라가는 건조 구간 셋 (조건 수치 없음).
- 표 1 에서 No.6–13 의 활물질 · 입도 칸은 비어 있다 — 위 줄 (NCM111 · spheres) 과 같다는 뜻으로 읽었다 [카드 추론]: 본문이 No.13 의 계수를 *"pNCM111-451"* 로 적고 (p.374), 앞 논문의 NCM 입도 x50,3 = 12 µm (meyer2017 카드 §3-1) 과 맞는다 ⇒ **앞 논문의 'NCM 양극' 은 NCM111** (그 카드의 [미확인] 'NCM 조성' 이 이 논문으로 좁혀진다).
- 표 2 의 부피 분율은 합이 40–58 % 라 **기공을 포함한 압연 전 코팅 부피** 기준이다 → [카드 산술] 1 − Σ vol% = 압연 전 기공률 · Fig 2 의 판독값과 15 중 13 이 ≤ 0.001 로 같다 (No.1 · No.2 만 0.006–0.007 어긋남 — 두 줄이 서로 바뀐 것으로 보인다 · §3-12).
- 각주 'two-side coated' 는 No.13 · 15 에만 붙어 있다 → 나머지 13 종은 **단면 코팅**으로 읽힌다 [카드 추론] · 집전체 종류 · 두께 [미확인] (No.13 · 15 는 앞 논문에 Al 20.0 · Cu 17.3 µm).
- 첨가제 (CC + CG + B) 부피 분율 [카드 산술 · 표 2]: No.1–5 8.1–8.5 vol% · No.6–12 10.5–13.5 · No.13 13.9 · No.14 9.2 · No.15 7.6 — 본문 *"about 7.6 vol.-% is rather small compared to the range of the other electrodes of 8.1–13.9 vol.-%"* (p.375) 와 같다.

### 3-2. 압연 · 측정 조건 (p.372–374 · p.376)
- 캘린더: *"a pilot scale two roll compactor GKL 400 (Saueressig GmbH Co. KG, Germany) with rolls of 430 mm in diameter and 465 mm in width"* · *"Different line loads were applied by varying the gap size between the rolls (maximal line load of the machine: 1500 N/mm)"* · 롤 힘 F_N 의 측정 · 해석은 *"explained in [22]"* (= 앞 논문: 주 실린더의 하중 덜림) · **최소 롤 간극 25 µm** (p.374 · p.376) · *"The process was performed at ambient temperature"* (수치 없음).
- 시료: No.13 · 15 는 연속 압연 · **나머지는 ≈300 mm 길이 시트로 잘라 불연속 압연** · *"For every adjusted state of compaction two sheets were calendered"* → 압밀 상태마다 시트 2 장 (Fig 5 · 9 에서 같은 간극의 두 점이 붙어 보이는 이유 [카드 추론]).
- **선하중 q_L = F_N / w_C** (롤 힘 ÷ 코팅 폭 · p.373) — 코팅 폭의 수치 · 롤 속도 · 통과 횟수 · 간극 값 · 하중 아래 두께 = [미확인].
- 질량 부하: *"measured by ultrasonic attenuation with a traversing sensor immediately after drying (USM200, Mesys, Germany)"* (전극 m_E · 집전체 m_C) — 압연 **전** 한 번 잰 값을 쓴다 (압연으로 늘어난 면적의 보정 언급 없음 [카드 추론]).
- 두께: *"a tactile dial gauge (ID-C, Mitutoyo, Japan) with a resolution of 1 μm … following a fixed pattern with 24 single measurements"* (전극 h_E · 집전체 h_C) · 높은 압축에서 활물질이 집전체에 1–2 µm 박히는 오차는 *"can be disregarded in relation to the measurement error"*.
- 고체 밀도: 성분별 **He 가스 피크노미터** · *"The mean value ρph of a coating is calculated by taking the mass fractions of each component into account"* — 평균하는 식 (부피 가산 = 조화 평균인지 산술 평균인지) 은 인쇄돼 있지 않다 (§3-11 에서 표 2 로 되짚음).
- 입자 미세압축 (UNAT, ASMEC): 활물질마다 *"at least 24 separate particles"* · 지름 100 µm 원기둥 압자 · 힘 증가 2.8 mN/s · 힘–변위 곡선에서 **첫 파괴가 나는 힘** ÷ **입자 투영 면적** (현미경으로 잰 지름) = 파괴 세기 · 고른 입자 크기는 x10–x90 사이 (p.372).

### 3-3. ★ 식 (1)–(5) — 인쇄 그대로 + 뜻 + 무엇을 맞추는가
| 식 | 인쇄된 꼴 | 뜻 · 맞춤 수 | 쪽 · 크롭 |
|---|---|---|---|
| (1) | ε = ε0 + exp(−K·P) | Heckel [21] 의 *"exponential relation between the applied load and the resulting density of metal powders by assuming a similarity to a first-order chemical reaction, substituting the time by the pressure P and the concentration by the density or porosity ε"* · ε0 = 느슨한 충전의 처음 기공률 · K = *"the plastic deformability of the particular bulk"*.  ⚠ **덧셈표는 인쇄 오류** (P = 0 에서 ε0 + 1) — 1 차 반응 꼴은 ε = ε0·exp(−K·P) [카드 산술] | p.372 · `eq_01_heckel_porosity_form.png` |
| (2) | ε_C = ε_C,min + (ε_C,0 − ε_C,min)·exp(−q_L/γ_C) | 앞 논문 식 (4) (밀도 꼴) 의 **기공률 꼴** — ε = 1 − ρ/ρ_ph 를 넣으면 같은 식 · 같은 γ_C [카드 산술] · 맞춤 수 둘 (ε_C,min · γ_C) · *"The minimum porosity of the coating εC,min is used as a second fitting parameter, the possibility to determine it independently would be beneficial to reduce the charactization of the compaction behavior to γC"* | p.372 · `eq_02_compaction_model_coating_porosity.png` |
| (3) | ε_C = 1 − ρ_C/ρ_ph = 1 − (m_E − m_C)/((h_E − h_C)·ρ_ph) | 기공률 연산자 (기하) — ρ_C = 코팅 밀도 · ρ_ph = 성분의 평균 고체 밀도 · m = 질량 부하 · h = 두께 (E = 전극 · C = 집전체) | p.372 · `eq_03_coating_porosity_definition.png` |
| 인라인 | q_L = F_N/w_C | 선하중 정의 | p.373 · `eq_p373_line_load_definition_inline.png` |
| 인라인 | ε_C,min_p = p·ε_C,0 with p = 0.4 | 끝값 예측 (가정) | p.374 · `eq_p374_min_porosity_prediction_p04_inline.png` |
| (4) | ε_C = ε_C,0(p + (1 − p)·exp(−q_L/γ_C)) | 식 (2) 에 ε_C,min = p·ε_C,0 을 넣은 것 — **맞춤 수 하나 (γ_C)** · ε_C,0 은 실측 · p = 0.4 고정 · Fig 5 · 9 의 곡선 | p.375 · `eq_04_model_with_predicted_minimum_p.png` |
| 인라인 | γ_C = μ·M_C | 부하 의존 (직선 · 원점 통과) | p.378 · `eq_p378_gamma_mu_mass_loading_inline.png` · `eq_fig10_inset_linear_fit_gamma_mu.png` |
| (5) | ε_C = ε_C,0(p + (1 − p)·exp(−q_L(μ·M_C))) | 식 (4) 에 γ_C = μ·M_C 를 넣은 것 — ⚠ **나눗셈표가 빠졌다** (뜻은 exp(−q_L/(μ·M_C))) · 맞춤 수 하나 (μ) 로 여러 부하를 한꺼번에 | p.378 · `eq_05_model_with_mass_loading_mu.png` |
- 각 번호 식은 식만 자른 것과 앞뒤 문장을 함께 자른 것 (`*_with_text.png`) 두 장씩 있다.
- **무엇이 달라졌나 (앞 논문 ↔ 이 논문)**: 2017 = 시작 · 끝 · γ_C 세 수를 곡선마다 맞춤 (끝은 외삽) → 2018 = 시작은 실측 · 끝은 0.4 × 시작 · γ_C 만 맞춤 → 여기에 γ_C = μ·M_C 를 더해 **한 활물질 · 한 조성에 μ 하나**.  동기 [인쇄 p.373]: *"The minimum coating porosity in the model equation proposed in [22] is an extrapolation of the curve.  It is favorable to determine the final porosity in a separate way to make the compaction resistance independant from this value.  Thus, the compaction resistance is the sole fitting parameter of the compaction behavior."*
- **Heckel 을 쓸 수 있다는 논거** [인쇄 p.372]: Heckel 식은 금속 가루의 일축 압축용이고 *"Heckel showed that it is less suitable for brittle materials as alumina.  However, the brittle active materials in the coatings investigated in this work are embedded in the additive matrix increasing the deformability of the coating drastically."* — 측정으로 받친 문장이 아니다 (첨가제 기지의 변형 물성 값 없음).

### 3-4. ★ 최소 기공률 예측 — Fig 2 (p.374) [판독 · ± = 오차 막대 반폭]
| No. | 전극 | 압연 전 ε_C,0 | 달성 최소 ε_min_a (최소 간극 25 µm 에서) | 외삽 최소 ε_min_e (식 (2) 맞춤) | 예측 0.4·ε_C,0 | 달성 ÷ 압연 전 | 외삽 ÷ 압연 전 | 달성 − 예측 |
|---|---|---|---|---|---|---|---|---|
| 1 | NCA-80/20 | 0.450 ± 0.010 | 0.201 ± 0.004 | 0.200 | 0.180 | 0.447 | 0.444 | +0.021 |
| 2 | NCA | 0.457 | 0.204 ± 0.005 | 0.180 ± 0.003 | 0.183 | 0.446 | 0.393 | +0.021 |
| 3 | NCM811 | 0.479 | 0.215 ± 0.003 | 0.201 ± 0.002 | 0.192 | 0.448 | 0.419 | +0.023 |
| 4 | NCM622 | 0.461 | 0.213 ± 0.005 | 0.203 ± 0.003 | 0.184 | 0.463 | 0.442 | +0.029 |
| 5 | NCM111 | 0.443 | 0.202 ± 0.004 | 0.189 ± 0.005 | 0.177 | 0.457 | 0.427 | +0.025 |
| 6 | 80 g/m² | 0.548 | 0.238 ± 0.009 | 0.227 ± 0.018 | 0.219 | 0.433 | 0.414 | +0.018 |
| 7 | 120 | 0.484 ± 0.006 | 0.214 ± 0.006 | 0.180 ± 0.004 | 0.193 | 0.442 | 0.372 | +0.020 |
| 8 | 161 | 0.441 ± 0.006 | 0.188 ± 0.003 | 0.159 ± 0.003 | 0.176 | 0.427 | 0.360 | +0.012 |
| 9 | 179 | 0.437 ± 0.011 | 0.197 ± 0.005 | 0.181 ± 0.003 | 0.175 | 0.450 | 0.414 | +0.022 |
| 10 | 198 | 0.436 ± 0.004 | 0.192 ± 0.002 | 0.154 ± 0.004 | 0.174 | 0.440 | 0.354 | +0.017 |
| 11 | 242 | 0.424 | 0.199 ± 0.003 | 0.162 ± 0.003 | 0.169 | 0.471 | 0.383 | +0.030 |
| 12 | 284 | 0.425 | 0.190 ± 0.003 | 0.153 ± 0.002 | 0.170 | 0.446 | 0.361 | +0.020 |
| 13 | NCM + 도전 흑연 (양면 451) | 0.521 ± 0.015 | 0.176 ± 0.006 | 0.169 ± 0.004 | 0.209 | **0.338** | 0.324 | −0.032 |
| 14 | LMO | 0.582 | 0.352 ± 0.005 | 0.332 ± 0.007 | 0.233 | **0.605** | 0.571 | +0.119 |
| 15 | 흑연 음극 (양면 197) | 0.603 | 0.178 ± 0.004 | 0.159 ± 0.002 | 0.241 | **0.295** | 0.264 | −0.064 |
- 압연 전 값의 오차 막대가 표지 안에 묻힌 것은 ± 를 비웠다 (≤ 0.009).  판독 불확도 ≈ ±0.002 (1 px = 기공률 0.0012).
- **가정의 세움** [인쇄 p.373–374]: 압연 전 기공률 (No.1–5 · 7–12) *"between 42 and 48% are generally speaking somewhat lower than the theoretical porosity of 47.64% of a simple cubic packing (scp) of hard, incompressible spheres of identical size"* · 입자는 크기가 같지도 완전한 구도 아니지만 *"the particles can be assumed as hard and incompressible"* · 첨가제는 활물질 사이 공간 (interparticle space **IS**) 에 끼어 입자를 벌리면서 (기공률 ↑) 활물질이 차지할 수 없는 공간 (unoccupiable space **US**) 을 채운다 (기공률 ↓) — *"possibly a partially self-balancing factor"* (Fig 3).  끝값은 *"the assumption that the compaction factor p between the initial and the minimum coating porosity is similar to the factor between the simple cubic packing (scp, 47.64%.) and the cubic close packing (ccp, 25.95%), which is 0.54"* 에서 출발 — [카드 산술] 1 − π/6 = 0.4764 · 1 − π/(3√2) = 0.2595 · 비 0.545.
- **0.54 → 0.4 로 낮춘 이유** [인쇄 p.374]: 달성 최소 (No.1–5 · 7–12) *"between 19 and 21 % deviate especially in relative terms significantly more from the ccp-porosity (up to 7 % or in relative terms 37 %) than the initial porosities from the scp-porosity (up to 6 % or in relative terms 13 %).  The additives in the studied particle coatings plausibly get pushed out of the IS, stay in the US and hence decrease the porosity (see Fig. 3).  Therefore p has to be much smaller for the electrodes.  The proposed p = 0.4 turns out to be an appropriate estimation of practical use."*  ([카드 산술] 상대 % 는 전극 값 기준이다: (25.95 − 19)/19 = 37 % · (47.64 − 42)/42 = 13 %.)
- ★ **[카드 산술] p = 0.4 는 무엇과 맞는가 (No.1–12)**: 달성 최소 ÷ 압연 전 = 0.427–0.471 (평균 **0.447** · 원점 통과 맞춤 0.447 · rms 잔차 0.005) ↔ 외삽 최소 ÷ 압연 전 = 0.354–0.444 (평균 **0.398** · 원점 통과 맞춤 0.400 · rms 0.014).  ⇒ **0.4 는 앞 논문 식 (2 수 맞춤) 으로 외삽한 끝값들의 평균**이고, 기계가 닿은 최소는 전부 예측보다 0.012–0.030 높다 (rms 0.022).  그래도 곡선이 끝점을 지나는 것은 마지막 선하중이 γ_C 의 2.2–3.3 배뿐이라 식 (4) 의 값이 아직 0.42–0.47 × ε_C,0 이기 때문이다 (지수 항이 남아 있다) — **0.4·ε_C,0 은 닿은 값이 아니라 점근값**이고, 거기서 기공률 0.005 안으로 들어가려면 q_L ≈ 4 γ_C (NCM111 223 g/m² 에서 ≈1180 N/mm · 기계 한계 1500 N/mm 안이지만 최소 간극에 먼저 걸린다) 가 든다.
- [카드 산술] 달성 최소를 '상수' 로 보면 평균 0.204 (rms 0.013 · No.6 을 빼면 0.201 · rms 0.009), '압연 전에 비례' 로 보면 rms 0.005 — 비례 꼴이 더 낫다 (자유 절편 직선: 기울기 0.38 · 절편 0.03 · R² 0.88 · No.6 을 빼면 R² 0.72).  12 점 · 압연 전 값의 폭이 0.42–0.48 (No.6 만 0.55) 이라 **비례 가정의 시험으로는 약하다**.
- 원문: *"In case of increasing mass loadings (No. 10–12) the deviation between the predicted εC,min and the achieved εC,min_a increases significantly, probably because the applied line load is not sufficient"* (p.374) — [판독] 달성 − 예측 은 No.10–12 에서 +0.017 · +0.030 · +0.020 으로 No.1–5 (+0.021 – +0.029) 와 다르지 않다.  커지는 것은 달성 − **외삽** (No.7 · 8 · 10 · 11 · 12 에서 0.030–0.038 ↔ No.1 · 3 · 4 · 5 · 6 에서 0.001–0.014 · No.2 · 9 는 0.016–0.025) 이다.
- **벗어난 세 전극** [인쇄 p.374–375]: (No.13) *"favors a slightly varied factor of pNCM111-451 = 0.33"* — 도전 흑연 (x50 2.4 µm · x90 4.1 µm) 이 US 에 잘 들어맞는다 (앞 논문의 수은 압입에서 압연 전 활물질 사이 기공 지름 2 µm) · (No.14) *"pLMO = 0.60"* — 다각형 입자는 부피가 커서 조밀 충전에 맞지 않는다 (수은 압입: 활물질 사이 기공 (0.3–9 µm) 부피가 탄소 기공 (0.02–0.3 µm) 부피의 3.27 배 [11] ↔ 부하 · 조성이 가장 비슷한 No.8 은 ≈1.34 배 — 이 논문의 전극인데 측정 방법 서술은 없다) · (No.15) *"pgraphiteanode = 0.29"* — 판상 입자가 처음에 매우 성기고 (0.60) 눕혀 쌓이면 구 · 다각형보다 틈이 적고, 파괴 세기가 매우 낮아 (Fig 7) *"fragments resulting from the calendering can fill the US"* · 첨가제 양은 원인이 아니다 (7.6 vol% 로 오히려 적다).  [판독 + 카드 산술] 달성 ÷ 압연 전 = 0.338 · 0.605 · 0.295 = 인쇄 0.33 · 0.60 · 0.29 ✓ (인쇄값은 달성 최소 기준).
- **얇은 코팅의 높은 압연 전 기공률** [인쇄 p.373–374 · Fig 4]: No.6 (80 g/m²) 0.548 ↔ No.8–12 0.42–0.44 (*"stays roughly constant (No. 8–12)"*) — 이유 ① 위에서 누르는 입자가 없어 느슨하다 (160 g/m² 부터는 건조 중 위 현탁액의 무게로 침강 충전) ② 집전체 면에 닿은 구 충전은 덜 조밀하다 [24] — *"Considering the low coating thickness in absolute scale, the second reason, namely the decreasing proportions of the interface porosity at the coating surface and substrate interface from the total coating volume, is the dominant one."*  No.6 은 *"about three layers of active material particles … a coating thickness of about 45 μm and a capacity loading of 1.1 mAh/cm2"* (p.378).
- [카드 산술] 표 2 의 활물질 부피 분율 × (1 − ε_min)/(1 − ε_0) = **달성 최소에서의 활물질 부피 분율**: 94 wt% 전극 (No.1–5) 0.66–0.68 · 90 wt% 전극 (No.6–12) 0.58–0.62 (외삽 끝값이면 0.59–0.65) · 그때 고체 전체 = 1 − ε_min = 0.76–0.81.  같은 크기 구의 무작위 조밀 충전 (≈0.63–0.64 — 이 논문 값이 아니라 `onoda1990_*` 카드가 옮긴 Scott 의 조밀 끝 0.63 · 0.635 ± 0.005) 근처다 — 원문이 견준 입방 조밀 (0.74) 에는 못 미친다 [카드 추론: 끝값은 '활물질 골격이 무작위 조밀 충전에 이르고 첨가제가 남은 틈의 일부를 채운 상태' 로 읽는 편이 0.54 → 0.4 의 보정보다 자료에 가깝다 — 원문의 말은 아니다].

### 3-5. ★ 활물질별 압밀 곡선 · γ_C — Fig 5 (p.375) · Fig 6 (p.376) · 표 3 (p.378)
| No. · 활물질 | γ_C (N/mm) [판독 Fig 6] | μ (kN·m/g) [인쇄 표 3] | reduced χ² [인쇄 Fig 5 범례] | 판독점에 식 (4) 한 수 재맞춤 γ_C (χ²_red) [카드 산술] | 판독점 (q_L N/mm → ε_C) [판독 Fig 5] |
|---|---|---|---|---|---|
| 1 NCA-80/20 | **220 ± 29** | 0.99 ± 0.13 | 3.57 | 229 +14/−13 (5.7) | ≈0 → 0.454 (가려짐) · 0.444 ± 0.010 · 2.5 → 0.420 ± 0.014 · 9.9 → 0.418 ± 0.005 · 48 → 0.361 ± 0.012 · 55 → 0.362 ± 0.009 · 266 → 0.281 ± 0.013 · 0.278 ± 0.007 · 715 → 0.197 ± 0.017 · 721 → 0.204 ± 0.016 |
| 2 NCA | **310 ± 25** | 1.40 ± 0.11 | 3.02 | 312 ± 15 (2.3) | ≈0 → 0.455 ± 0.007 · 0.460 ± 0.006 · 9.7 → 0.431 ± 0.007 · 128 → 0.345 ± 0.007 · 147 → 0.352 ± 0.009 · 346 → 0.284 ± 0.010 · 369 → 0.281 ± 0.009 · 748 → 0.216 ± 0.020 · 760 → 0.208 ± 0.018 |
| 3 NCM811 | **230 ± 22** | 1.04 ± 0.10 | 4.00 | 247 ± 10 (4.2) | 0 → 0.480 ± 0.010 · 23 → 0.431 ± 0.005 · 123 → 0.360 · 127 → 0.360 · 297 → 0.288 · 316 → 0.283 · 718 → 0.219 ± 0.010 · 741 → 0.210 ± 0.011 |
| 4 NCM622 | **305 ± 21** | 1.36 ± 0.09 | 2.24 | 321 ± 16 (1.9) | 0 → 0.463 · 0.456 · 27 → 0.418 ± 0.006 · 142 → 0.357 ± 0.009 · 146 → 0.356 · 325 → 0.295 · 0.289 · 782 → 0.214 ± 0.015 · 796 → 0.211 ± 0.014 |
| 5 NCM111 (두 패널의 기준) | **297 ± 36** | 1.33 ± 0.16 | 3.45 | 306 ± 21 (2.7) | 0 → 0.444 · 20 → 0.401 ± 0.007 · 141 → 0.331 ± 0.011 · 154 → 0.331 ± 0.012 · 477 → 0.247 ± 0.012 · 480 → 0.250 ± 0.012 · 771 → 0.198 ± 0.018 · 777 → 0.206 ± 0.017 |
- 표 3 의 μ = γ_C ÷ 223 g/m² ([카드 산술] μ × 223 = 221 · 312 · 232 · 303 · 297 N/mm = Fig 6 막대 ±3 N/mm) — *"the data of No. 1–5 are projected from the standard errors of the compaction resistance from Fig. 6"* · **활물질 다섯의 μ 는 부하 한 수준에서 γ_C = μ·M_C 를 가정해 옮긴 값**이다 (각 활물질에서 부하를 바꿔 본 것이 아니다).
- 오차 = *"The standard errors result from the error propagation of the approximations"* (Fig 6 캡션) — 맞춤 매개변수의 표준오차.  상대 크기 [카드 산술] 13 · 8 · 10 · 7 · 12 %.  Fig 5 의 점마다 붙은 오차 막대의 정의 (24 점 두께의 산포인지 등) 는 [미확인].
- **저자 해석** [인쇄 p.375–376]: NCA · NCM622 · NCM111 은 γ_C 가 비슷하다 (*"The electrodes No. 2, 4 and 5 show very similar values"*) · **NCA-80/20** 은 낮은 선하중에서 더 가파르다 — 작은 입자 몫이 *"get easily pushed into the US of the larger AM-particles at low applied line loads up to about 100 N/mm2"* (단위는 N/mm 의 오기) · **NCM811** 은 입자가 굵어 (x10 8.1 µm) *"the highest initial porosity and a 20 % lower specific surface"* → 탄소-바인더 기지와 닿는 면이 작아 마찰 면적이 줄고 낮은 선하중에서 쉽게 눌린다 · *"the low compaction resistance of No. 3 does not result from particular low porosities at high possibly particle breaking line loads, but from the strong porosity drop due to the high initial porosity"*.
- ★ **[카드 산술] 맞춤의 잔차 무늬** (판독점 − 인쇄 매개변수 곡선): 다섯 활물질 모두 **낮은 선하중 (2.5–55 N/mm) 에서 자료가 곡선보다 0.017–0.037 낮고** (NCA-80/20 −0.027 · −0.020 · −0.037 · −0.028 / NCA −0.017 / NCM811 −0.021 / NCM622 −0.020 / NCM111 −0.025) **중간 (266–480 N/mm) 에서 0.010–0.020 높고**, 끝 (715–796 N/mm) 에서 0.001–0.014 높다 — rms 0.010–0.021 · 최대 0.037.  오차 막대 (±0.005–0.014) 보다 크다 → 범례의 reduced χ² 2.2–4.0 과 같은 말이다.  ⇒ **한 지수로는 초기의 빠른 감소 (저자가 말한 재배열 단계) 와 뒤의 느린 꼬리를 함께 못 따른다** — γ_C 는 그 둘을 가로지르는 평균 빠르기이고, 저자도 *"the impact of the data of this state has a large influence on the compaction resistance γC"* (p.376) 라고 적는다.
- 캡션은 *"Even though the values for χν2 are very near to 1, the approximations describe the data courses visually sufficiently well for practical purposes"* 인데 범례 값은 2.24–4.00 이다 (Fig 9 캡션은 *"not for every fit near to 1"* — §3-12).
- 같은 기공률에 드는 선하중 (인쇄 매개변수로 셈 · §3-7): ε_C = 0.30 에 NCA-80/20 178 · NCM811 226 · NCM111 229 · NCM622 264 · NCA 265 N/mm.

### 3-6. ★ 부하별 압밀 곡선 · γ_C = μ·M_C — Fig 9 (p.377) · Fig 10 · 표 3 (p.378)
| No. | M_C (g/m²) [판독 Fig 10 · ± 가로 막대] | γ_C (N/mm) [판독 Fig 10] | γ_C/M_C [카드 산술] | 직선 1.31·M_C 와의 차 | reduced χ² [인쇄 Fig 9 범례] | 판독점 (q_L N/mm → ε_C) [판독 Fig 9 · 일부 계열은 겹쳐 일부 점만] |
|---|---|---|---|---|---|---|
| 6 | 79.6 ± 2.2 | 98 ± 11 | 1.23 | −6 % | 5.83 | 0 → 0.548 · 7 → 0.520 ± 0.008 · 0.519 · 58 → 0.417 · 71 → 0.408 · 271 → 0.237 ± 0.025 · 301 → 0.238 ± 0.029 |
| 7 | 120.1 ± 2.6 | 164 ± 11 | 1.36 | +4 % | 1.72 | 0 → 0.483 ± 0.016 · 65 → 0.386 ± 0.015 · 209 → 0.290 ± 0.013 · 291 → 0.248 ± 0.013 · 296 → 0.255 · 400 → 0.206 ± 0.021 · 424 → 0.221 ± 0.024 |
| 8 | 161.4 ± 3.3 | 168 ± 11 | **1.04** | **−21 %** | 1.47 | 0 → 0.440 · 19 → 0.395 · 76 → 0.341 · 148 → 0.293 · 318 → 0.232 ± 0.023 · 457 → 0.186 ± 0.014 · 479 → 0.189 ± 0.012 |
| 9 | 179.5 ± 3.1 | 254 ± 12 | 1.42 | +8 % | 1.09 | 203 → 0.290 ± 0.011 · 417 → 0.238 ± 0.011 (끝점 ≈566–575 N/mm 는 겹쳐 미판독) |
| 10 | 198.1 ± 3.5 | 249 ± 16 | 1.26 | −4 % | 3.89 | 0 → 0.438 · 17 → 0.384 · 106 → 0.338 · 122 → 0.328 · 390 → 0.228 ± 0.014 · 409 → 0.234 ± 0.010 · 621 → 0.187 ± 0.006 · 659 → 0.194 ± 0.008 |
| 11 | 241.5 ± 1.9 | 340 ± 14 | 1.41 | +8 % | 1.18 | 19 → 0.395 ± 0.007 · 242 → 0.302 · 428 → 0.239 ± 0.013 · 747 → 0.199 ± 0.010 · 751 → 0.200 ± 0.015 |
| 12 | 283.9 ± 3.7 | 371 ± 5 | 1.31 | −0.3 % | 0.19 | 0 → 0.425 ± 0.009 · 68 → 0.380 · 149 → 0.343 · 157 → 0.338 · 256 → 0.291 · 269 → 0.296 · 447 → 0.247 ± 0.013 · 455 → 0.246 ± 0.010 · 860 → 0.188 ± 0.014 · 867 → 0.191 ± 0.015 |
- [인쇄 Fig 10 상자] **γ_C = μ·M_C · R² = 0.996 · μ = 1.31 ± 0.03 (N/mm)/(g/m²) = 1.31 ± 0.03 kN·m_length/g** · 캡션 *"linearly fitted with γC(MC = 0) = 0.  The first fitting proposed an ordinate intercept near zero."* · 표 3 의 No.6–12 줄 = 1.31 ± 0.03 (맞춤의 표준오차).  단위 [카드 산술]: (N/mm)/(g/m²) = 10³ N·m/g ✓.
- [카드 산술] 일곱 점의 재맞춤: 원점 통과 μ = **1.310** (비가중) · 1.306 ± 0.016 (오차 가중 · χ²_red 3.6) · 절편을 풀면 기울기 1.39 · 절편 −16 N/mm · 멱 꼴 γ_C ∝ M_C^n 이면 n = 1.06 ± 0.11 (가중 1.02 ± 0.05) — **직선 비례와 맞고 √M_C (n = 0.5 · rms 49 ↔ 직선 21 N/mm) 는 아니다**.  인쇄 R² 0.996 은 원점 통과 맞춤의 **비중심** 값으로 읽힌다 (재계산 0.993 비가중 · 0.997 가중) — 평균 기준 (보통의) R² 는 **0.948** 이다.  No.8 (161 g/m²) 한 점이 직선보다 44 N/mm (21 %) 낮다 (오차 막대 ±11 의 4 배).
- **저자 해석** [인쇄 p.376]: 얇은 No.6 · 7 은 시작 기공률이 높고 급히 줄어 끝 기공률이 더 높다 — *"As the minimum roll gap width of 25 μm is relatively high compared to the thin electrode thicknesses of No. 6 and 7, the geometrically limited applicable line load is smaller than for thicker electrodes"* · No.8–12 는 시작이 거의 같고 부하가 클수록 느리게 준다 — *"Higher line loads have to be applied to decrease the porosity to the same level"* · 이유 = *"The higher the amount of particles that have to be compacted, the more friction between the particles has to be overcome as the friction area increases"* (측정으로 받친 문장이 아니다) · 아주 낮은 부하에서는 직선에서 벗어나야 한다 — *"As it is not possible to compact a monolayer of particles without particle breakage, the compaction resistance must increase at very low mass loadings"*.
- **표 3 아래 문장** [인쇄 p.378]: *"The mass dependency of No. 5 is not so pronounced in comparison to No. 6–12.  This can be explained by the lower content of carbon conductive additives, which have a very high specific surface area"* — 표 3 의 값은 No.5 1.33 ± 0.16 ↔ No.6–12 1.31 ± 0.03 으로 **차이가 오차 안**이다 (§3-12).
- 식 (5) (μ 하나) 로 일곱 곡선을 그리면 [카드 산술] No.8 에서 자료가 곡선보다 최대 0.023 낮다 (압연한 여섯 점 중 다섯이 0.015–0.023 · 그 전극의 γ_C 가 직선보다 21 % 낮으므로) · No.12 는 rms 0.004.  개별 γ_C 를 쓴 식 (4) 의 잔차 rms = 0.013 · 0.010 · 0.010 · (0.009) · 0.014 · 0.008 · 0.004 (No.6–12).
- 마지막 선하중 [판독]: ≈300 · 424 · 479 · (566–575) · 659 · 751 · 867 N/mm (No.6–12) — 부하가 클수록 큰 선하중까지 눌렀다 (최소 간극 25 µm 가 한계) · γ_C 의 2.2–3.1 배.

### 3-7. 식 (4) · (5) 가 주는 곡선 값 [카드 산술 — 인쇄 μ (표 3) × 인쇄 M_C (표 2) · 판독 ε_C,0 (Fig 2) · p = 0.4]
| No. | γ_C = μ·M_C (N/mm) | ε_C @ 100 | @ 200 | @ 400 | @ 800 N/mm | ε_C = 0.30 에 드는 q_L | ε_C = 0.25 에 드는 q_L | 끝값 0.4·ε_C,0 |
|---|---|---|---|---|---|---|---|---|
| 1 NCA-80/20 | 221 | 0.351 | 0.289 | 0.224 | 0.187 | 178 | 297 | 0.180 |
| 2 NCA | 312 | 0.382 | 0.327 | 0.259 | 0.204 | 265 | 439 | 0.183 |
| 3 NCM811 | 232 | 0.378 | 0.313 | 0.243 | 0.201 | 226 | 370 | 0.192 |
| 4 NCM622 | 303 | 0.383 | 0.327 | 0.258 | 0.204 | 264 | 435 | 0.184 |
| 5 NCM111 | 297 | 0.367 | 0.312 | 0.246 | 0.195 | 229 | 383 | 0.177 |
| 6 (80) | 105 | 0.346 | 0.268 | (0.227) | (0.220) | 147 | 249 | 0.219 |
| 7 (120) | 157 | 0.347 | 0.275 | 0.216 | (0.195) | 157 | 257 | 0.193 |
| 8 (161) | 211 | 0.341 | 0.279 | 0.216 | (0.182) | 160 | 270 | 0.176 |
| 9 (179) | 234 | 0.346 | 0.287 | 0.222 | (0.183) | 173 | 293 | 0.175 |
| 10 (198) | 259 | 0.352 | 0.295 | 0.230 | (0.186) | 190 | 322 | 0.174 |
| 11 (242) | 317 | 0.355 | 0.305 | 0.241 | (0.190) | 211 | 364 | 0.169 |
| 12 (284) | 372 | 0.365 | 0.319 | 0.257 | 0.200 | 250 | 430 | 0.170 |
- 괄호 = 그 전극에 실제로 건 최대 선하중 (§3-6) 을 넘는 외삽.  이 표는 **모델 값**이다 (실측점은 §3-5 · §3-6) — 낮은 선하중 쪽은 실제보다 0.02–0.04 높게, 중간은 0.01–0.02 낮게 나온다 (§3-5 잔차 무늬).
- 읽는 법: 같은 기공률 0.30 에 드는 선하중이 부하 80 → 284 g/m² 에서 147 → 250 N/mm (1.7 배) · 활물질에 따라 178–265 N/mm (1.5 배).

### 3-8. 활물질 입자의 파괴 세기 · 표면 · 밀도 — Fig 7 (p.376) · Fig 8 (p.377) · 본문 p.375–376
| 재료 | 파괴 세기 σ_b 중앙값 (누적 0.5) [판독 Fig 7 · MPa] | 그려진 점 수 · 범위 [판독] | 중앙값 입자 (x50) 의 첫 파괴 힘 [카드 산술 σ_b·π·x50²/4] |
|---|---|---|---|
| 흑연 | ≈30 | 31 · 5–111 | ≈10 mN (20.4 µm) |
| NCM811 | **≈63** | 35 · ≤ 180 | ≈10 mN (14.3 µm) |
| NCAI | ≈117 | 31 · ≈76–350 | ≈21 mN (15.2 µm) |
| NCM622 | ≈139 | 23 · ≤ 343 | ≈15 mN (11.7 µm) |
| NCM111 | **≈274** | 36 · 80–545 | ≈31 mN (12.0 µm) |
| NCAII | ≈347 (±15 — 표지 일부만 가려 읽음) | 미계수 · ≤ 678 (0.90) | ≈9 mN (5.8 µm) |
- 정의 [인쇄 p.372]: 첫 파괴 힘 ÷ 입자 투영 면적 · 누적 분포로 그림 (*"At 0.5 the median value for the breaking strength is readable"*).  [카드 산술] 투영 면적이 πd²/4 이므로 d² 로 나누는 명목 응력 (`song2025_insitu_ct_dem_*` 카드의 σm = f_max/d²) 으로는 π/4 배 = NCM811 ≈49 · NCM622 ≈109 · NCM111 ≈215 MPa — 그 카드의 문턱 ≈200 MPa (NCM9055 · 5.5 µm · 6 mN 인용) 와 **정의를 맞춘 뒤에만** 나란히 놓는다 (재료 · 입경 · 공급사가 다르다).
- [인쇄 p.376] *"the breaking strength decreases with increasing Ni-content and slightly decreases with particle size for the two NCA fractions.  The NCM811 shows the lowest values, followed by NCAI and NCM622.  NCM111 turns out to be the mechanically most stable material at similar particle sizes."* · Fig 8 (SEM): Ni 함량이 높을수록 2 차 입자가 느슨하게 뭉쳐 *"less area for solid bridges within the aggregates"* · BET **0.22 (NCM111) · 0.30 (NCM622) · 0.27 m²/g (NCM811)** · 가스 피크노미터 밀도 **NCAII 4.892 ± 0.003 ↔ NCAI 4.829 ± 0.003 g/cm³** (작은 NCAII 가 더 치밀).
- ⚠ [인쇄] *"the different active materials were obtained by different producers using probably different manufacturing processes.  Thus, the shown results have no general validity about the effect of the Ni-content on the mechanical integrity, but surely on the materials investigated in this work."*
- ★ **파괴 세기 ↔ γ_C** [인쇄 p.376]: *"low breaking strengths are one factor leading to a low compaction resistance, but not the only one as the comparable compaction resistance of the NCM111 electrode No. 5 shows"* — 파괴 세기가 지배 인자라면 NCM111 (≈274 MPa) 의 γ_C 가 NCA (≈117) · NCM622 (≈139) 보다 뚜렷이 커야 하는데 셋이 같다 (297 · 310 · 305 N/mm) · *"Ultimately, the friction, hence the particle size distribution and surface, appears to be the most important particulate characteristic determining the line load necessary for the compaction of the electrodes with different spherical active materials.  The differences discussed above occur in the early state of compaction … At this stage, rearrangement is the dominant densification mechanism for composites of metallic nano- and microparticles [26] and the interparticular friction affects the compaction pressure significantly [27]."*
- 압연 뒤 입자가 실제로 깨졌는지는 이 논문에 **없다** — *"The properties of the calendered cathodes will be discussed in a future publication"* (p.376) · 결론: 더 센 기계로 더 낮은 기공률이 가능하겠지만 *"then ion diffusion limitations and particle breakage are expected"* (p.378).

### 3-9. ★ 선하중은 압력이 아니다 — 원문에 환산 없음 + [카드 추정] 크기 감각
- **원문**: q_L = F_N/w_C — 롤 힘을 코팅 **폭** (롤 축 방향) 으로 나눈 값 (N/mm).  압력이 되려면 롤 진행 방향의 **접촉 길이**로 한 번 더 나눠야 하는데, 원문에는 접촉 길이 · 하중 아래 간극 · 롤 탄성 변형 · 압력 분포 · 코팅 폭 · 롤 속도가 없다.  텍스트 층에 'MPa' 는 0 회 (Fig 7 의 축 = 입자 파괴 세기에만) · 'pressure' 는 두 번 (Heckel 의 P · 참고 [27] 을 인용한 *"compaction pressure"*) · 'stress' 는 한 번 (미세압축의 *"applied stress"*).  본문의 *"100 N/mm2"* (p.375) 는 N/mm 의 오기다.  ⇒ **γ_C (N/mm) · μ (kN·m/g) 를 압력 단위 값 (우리 Heckel P_y · σ_y) 과 나란히 놓을 수 없다.**
- ★ **γ_C 는 재료 상수가 아니라 부하에 비례하는 양**이다 (γ_C = μ·M_C) — 같은 재료 · 같은 조성인데 80 → 284 g/m² 에서 98 → 371 N/mm.  압연 문헌의 N/mm 값은 **부하 (두께) 가 다르면 서로도 견줄 수 없다**.
- **[카드 추정 — 원문 값 아님 · 인용 금지]** 코팅 두께 h = M_C/(ρ_ph·(1 − ε_C)) · 접촉 길이 = 강체 롤의 기하 호 L = √(R·Δh) (R = 215 mm [인쇄 Ø430] · Δh = 압연 전 − 압연 뒤 코팅 두께) · 평균 압력 = q_L/L.  고체 밀도는 원문에 없어서 ① No.6–12 는 *"about 45 μm"* (No.6 · 80 g/m² · p.378) 와 판독 ε_C,0 0.548 에서 ρ_ph ≈ 3.94 g/cm³ (45 ± 1 µm 이면 3.85–4.03) ② No.2 는 인쇄 NCAI 밀도 4.829 와 표 2 에서 ρ_ph ≈ 4.34 ③ No.5 는 ①에서 나온 NCM111 밀도 ≈4.62 와 표 2 에서 ρ_ph ≈ 4.18 로 두었다 [카드 산술]:

| 전극 | 압연 전 → 뒤 코팅 두께 (µm) | Δh (µm) | L (mm) | 마지막 선하중 (N/mm) | 평균 압력 q_L/L (MPa) | q_L = γ_C 일 때 평균 압력 (MPa) |
|---|---|---|---|---|---|---|
| No.6 (80 g/m²) | 45 → 27 | 18 | 2.0 | ≈300 | ≈150 | ≈56 |
| No.8 (161) | 73 → 50 | 23 | 2.2 | ≈479 | ≈220 | ≈88 |
| No.10 (198) | 89 → 62 | 27 | 2.4 | ≈659 | ≈270 | ≈120 |
| No.12 (284) | 125 → 89 | 36 | 2.8 | ≈867 | ≈310 | ≈153 |
| No.5 NCM111 (223 · 94 wt%) | 96 → 67 | 29 | 2.5 | ≈777 | ≈310 | ≈136 |
| No.2 NCA (223 · 94 wt%) | 95 → 65 | 30 | 2.5 | ≈760 | ≈300 | ≈140 |
- 가정과 방향: 하중 아래 간극은 압연 뒤 두께보다 좁다 (탄성 회복) → Δh · L 과소 → 압력 과대 쪽 · 롤의 탄성 납작해짐 무시 (같은 방향 · 높은 선하중일수록 크다) · 압력 분포 균일 가정 (최대는 평균보다 크다) · 집전체 변형 무시 · 고체 밀도는 'about 45 µm' 한 값에 기댄다.  ⇒ **'압연 양극의 마지막 점은 평균 수백 MPa 자릿수' 라는 크기 감각**만 뜻이 있다 (앞 논문의 양면 코팅 어림 ≈220 MPa @ 1065 N/mm 보다 큰 것은 단면 코팅이 얇아 접촉 길이가 짧기 때문 · meyer2017 카드 §3-9).
- [카드 산술 · 카드 추론] **설정 간극 ≠ 압연 뒤 두께**: 최소 간극 25 µm 에서 나온 전극의 **코팅만** 해도 27 µm (No.6) – 89 µm (No.12) 다 (집전체 두께는 더해야 한다) → 인쇄된 '간극' 은 하중이 없을 때의 설정값이고, 하중 아래에서 롤 · 기계가 벌어진 양 + 전극의 되돌아옴이 그 차이다.  이 둘을 가르는 측정은 이 논문에 없다 (`diener2022_roll_gap_springback_calendering` 이 같은 기계에서 간극을 직접 쟀다).
- [카드 추론 — 원문에 없는 검토] **γ_C ∝ M_C 의 일부는 기하일 수 있다**: 선하중 = 평균 압력 × 접촉 길이이고 접촉 길이는 두께 감소와 함께 는다 (강체 롤이면 L ∝ √Δh ∝ √M_C).  같은 기공률에 같은 평균 압력이 든다면 γ_C ∝ √M_C 여야 하는데 자료는 M_C^1.0 이다 → 위 어림으로는 같은 압밀 상태 (q_L = γ_C) 의 평균 압력이 56 → 153 MPa 로 부하와 함께 커진다.  롤의 납작해짐을 넣으면 이 차이는 줄어든다 (방향만 · 크기 [미확인]).  ⇒ 저자의 '마찰 면적' 설명과 접촉 길이 기하를 이 자료로는 가를 수 없다.

### 3-10. ★ Heckel 식과의 관계
- [인쇄 p.372] 초록 *"a Heckel-based model equation"* · 본문 (§3-3 의 인용) — Heckel 식을 1 차 반응에 빗대 소개하고, 금속 가루용이며 알루미나 같은 취성 재료에는 덜 맞지만 활물질이 첨가제 기지에 묻혀 있어 쓸 수 있다고 하고, γ_C 를 *"a reciprocal equivalent to Heckels constant K"* 라 부른다.  Heckel 좌표 그림 · K · 항복 압력 P_y · 항복 세기 환산은 **없다**.
- [카드 산술] Heckel: ln(1/ε) = K·P + ln(1/ε_0) ⇔ ε = ε_0·exp(−K·P) (끝값 0).  식 (2) 는 **끝값 위에 남는 기공률** 에 같은 꼴을 쓴 것: (ε_C − ε_C,min) = (ε_C,0 − ε_C,min)·exp(−q_L/γ_C) — 대응 = P → q_L (선하중) · K → 1/γ_C · 끝값 0 → ε_C,min (= 0.4·ε_C,0).  다른 점 = ① 끝값이 0 이 아니다 ② 하중 변수가 압력이 아니다 ③ 하중을 뺀 뒤 상태 ④ 처음 기공률이 실측 압연 전 값.
- [카드 산술] 식 (4) 를 고전 Heckel 좌표 ln(1/ε_C) ↔ q_L 에 놓으면 **직선이 아니다** — 국소 기울기 K(q) = (1 − p)·e^(−q/γ)/(γ·[p + (1 − p)·e^(−q/γ)]) 의 역수가 q_L = 0 · γ_C · 2γ_C · 3γ_C 에서 **1.67 · 2.81 · 5.93 · 14.4 × γ_C** (8.6 배) 로 커진다.  시작점의 1/K = γ_C/0.6: NCA-80/20 367 · NCM811 383 · NCM111 495 · NCM622 508 · NCA 516 N/mm.  ⇒ 끝값이 있는 자료를 Heckel 직선에 맞추면 '항복 압력' 이 맞춤 창에 따라 변한다 (앞 논문 카드 §3-10 과 같은 결론 · 여기서는 끝값을 고정했을 뿐).
- [카드 추론] 이 논문의 진전은 Heckel 과의 관계가 아니라 **끝값을 맞춤에서 뺀 것**이다 — 앞 논문에서 맞춤 범위에 따라 변하던 끝값 (meyer2017 카드 §3-4) 을 압연 전 값의 비로 묶어 γ_C 를 전극끼리 견줄 수 있는 한 수로 만들었다.  값은 그 묶는 비 (0.4) 가 맞는 범위에서만 뜻이 있다 (§3-4).

### 3-11. ★ 앞 논문 (Meyer 2017) 의 두 전극이 여기서 달라진 값 — No.13 · No.15
| 양 | 앞 논문 (meyer2017 카드의 인쇄 · 판독값) | 이 논문 (표 2 · Fig 2 판독) | [카드 산술] |
|---|---|---|---|
| No.13 활물질 부피 분율 (압연 전) | 31 vol% | **34.0 vol%** | 34.0 % × 4.65 g/cm³ (앞 논문의 NCM 입자 밀도) ÷ 0.86 = **1.838 g/cm³** = 앞 논문 ρ_C,0 1.83–1.84 ✓ — **코팅 밀도는 같다** |
| No.13 압연 전 기공률 | 0.570 (57.0 ± 1.2 %) · 분모 ρ_ph 4.3 g/cm³ | **0.521 ± 0.015** | 1.838/(1 − 0.521) = **3.84 g/cm³** — 분모 밀도가 4.3 → 3.84 로 바뀐 것과 같다 |
| No.13 최소 기공률 | 기하 0.260 (판독 · 1065 N/mm · 3.14 g/cm³) · 외삽 0.26 / 수은 압입 0.183 · 외삽 0.16 | **달성 0.176 ± 0.006 · 외삽 0.169 ± 0.004** | 1 − 3.14/3.84 = 0.182 ✓ · 외삽 밀도 3.16–3.21 → 0.164–0.177 ✓ |
| No.15 압연 전 기공률 | 0.608 · 분모 2.2 (판독 2.187) | 0.603 (표 2: 0.602) | 0.856/(1 − 0.602) = 2.15 g/cm³ |
| No.15 최소 기공률 | 기하 0.191 (판독 · 728 N/mm · 1.77 g/cm³) | 달성 0.178 ± 0.004 · 외삽 0.159 ± 0.002 | 1 − 1.769/2.151 = **0.1776** ✓ (소수 넷째 자리까지) |
- [카드 산술] 표 2 의 부피 분율 비에서 No.13 성분 밀도를 되짚으면 (NCM 4.65 기준) 도전 탄소 1.67 · 도전 흑연 2.37 · 바인더 1.72 g/cm³ → **부피 가산 (조화) 평균 3.84** · **질량 가중 산술 평균 4.26 ≈ 앞 논문의 4.3** (그 카드가 Fig 6 에서 되짚은 값 4.245).  ⇒ 앞 논문의 혼합물 밀도 4.3 g/cm³ 은 질량 분율로 **산술 평균**한 값으로 보이고, 이 논문의 표 2 는 부피가 더해지는 옳은 평균과 맞는다 [카드 추론 — 두 논문 어디에도 평균 식은 인쇄돼 있지 않고, 값이 바뀌었다는 말도 없다].  흑연 음극도 같은 무늬다: 표 2 에서 되짚은 성분 밀도 (흑연 2.26 · 도전 탄소 1.65 · 바인더 1.71 g/cm³) 의 산술 평균 2.17 (앞 논문 판독 2.187) ↔ 조화 평균 **2.151** (이 논문) — 성분 밀도가 서로 비슷해 영향이 작을 뿐이다 (0.608 → 0.603).
- ⇒ **이 논문의 No.13 기공률 (0.521 → 0.176) 은 앞 논문의 수은 압입 값 (0.49–0.52 → 0.16–0.18) 과 겹친다.**  앞 논문이 *"εC,Hg is approximately 8% lower than εC,ph … Probably this offset arises from closed pores like inner voids of the NCM particles"* 라고 설명한 차이는 **분모 밀도의 평균 방식에서 온 것으로 설명된다** [카드 추론] — meyer2017 카드 §3-5 '약점 3' (성분 합산 밀도 3.90 이면 기하 값이 수은 값과 겹친다) 이 이 논문의 표 2 로 뒷받침된다.  이 논문의 *"This method delivers porosities which are in well corresponce with the porosities measured by mercury porosimetry [22,23]"* (p.372) 도 고친 밀도일 때만 [22] 의 양극 자료와 맞는다.
- [카드 산술] **끝값 비 p 는 분모 밀도에 민감하다**: 같은 No.13 이 앞 논문 값으로는 0.26/0.57 = 0.46 (No.1–12 의 달성 비 0.447 과 같다), 이 논문 값으로는 0.176/0.521 = 0.34.  분모 밀도 −2 % 에 ε 0.20 은 0.016 · ε 0.45 는 0.011 내려가 p 가 ≈6 % 줄어든다.
- [카드 산술] **앞 논문의 양면 전극은 '한 면의 부하' 로 나눠야 이 논문의 μ 와 맞는다** (한 쌍뿐이라 우연일 수 있다): 앞 논문의 No.13 (NCM111 · 양면 합 451 g/m² = 한 면 225.5) γ_C 292 ± 9 · 309 ± 45 N/mm ÷ 225.5 = **1.29 · 1.37 kN·m/g** = 이 논문 NCM111 의 μ (1.31 ± 0.03 · 1.33 ± 0.16) — 양면 합으로 나누면 0.65 · 0.69 로 절반이다.  저자 설명 ('눌러야 할 입자가 많을수록 마찰 면적이 크다') 이라면 간극에 든 전체 질량 (양면 합) 을 따라야 한다 → 맞다면 한 층의 두께가 정하는 무엇 (롤 면과 집전체 면 사이 한 층 안의 응력 전달) 쪽을 가리킨다 [카드 추론 — 두 전극은 조성 (86 ↔ 90–94 wt%) · 맞춤식 (3 수 ↔ 1 수) 이 달라 엄밀한 대조가 아니고, 원문은 No.13–15 를 더 다루지 않는다 · 접촉 길이 기하만으로는 양면 전극의 γ_C 가 √2 배 (≈420 N/mm) 여야 한다 · §3-9].

### 3-12. 인쇄값끼리 어긋남 (원문 비판 — §11 에 다시)
1. 식 (1) 의 덧셈표 (ε = ε0 + exp(−K·P)) — 곱셈이어야 한다 (§3-3).
2. 식 (5) 의 나눗셈표 누락 (exp(−q_L(μ·M_C))) — 위 문장 γ_C = μ·M_C 와 식 (4) 로 뜻이 정해진다.
3. 단위 오기: Fig 4 캡션 *"80 g/cm2 … 160 g/cm2"* (g/m²) · 본문 *"up to about 100 N/mm2"* (N/mm).
4. Fig 5 캡션 *"Even though the values for χν2 are very near to 1"* ↔ 범례 2.24–4.00 (Fig 9 캡션은 *"not for every fit near to 1"* — Fig 5 캡션에서 'not' 이 빠진 것으로 보인다) · 같은 캡션의 기호가 한 번은 χn² 로 찍혔다.
5. 표 2 의 No.1 (45.9) · No.2 (46.5) 활물질 부피 분율 → 압연 전 기공률 0.456 · 0.450 ↔ Fig 2 · Fig 5 판독 0.450 · 0.457 — **두 줄이 서로 바뀐 것으로 보인다** [카드 산술: 인쇄 NCA 밀도 4.829 · 4.892 로 두 전극의 혼합물 밀도를 셈하면 그대로는 비가 0.976, 바꾸면 1.002 (조성에서 기대되는 값 1.002)].
6. 가장 큰 부하: 표 1 · Fig 2 이름표 '280' · 표 2 '284 ± 4' ↔ Fig 9 범례 · 표 3 · 본문 '285' (*"between 80 and 285 g/m2"*) · 초록은 *"from 80 to 280 g/m2"*.
7. *"The NCM811 particles are coarse … This leads to the highest initial porosity and a 20 % lower specific surface"* (p.375) ↔ BET 0.27 (NCM811) · 0.22 (NCM111) · 0.30 m²/g (NCM622) (p.376) — NCM811 은 NCM622 보다 10 % 낮고 NCM111 보다는 23 % **높다**.  '20 %' 가 무엇 대비인지 인쇄돼 있지 않다 (NCA 의 BET 는 없음).
8. *"The mass dependency of No. 5 is not so pronounced in comparison to No. 6–12"* (p.378) ↔ 표 3 의 1.33 ± 0.16 ↔ 1.31 ± 0.03 (같다 · 오히려 No.5 가 조금 크다).
9. 결론 *"The maximum is 12 %, converted into relative errors"* ↔ 표 3 의 0.13/0.99 = 13 % (No.1) · Fig 6 판독 29/220 = 13 % (12 % 는 No.5 의 값).
10. No.13 의 기공률이 참고 [22] 의 인쇄값과 다르다 (§3-11) — 본문에 설명 없음.
11. 참고 [9] (제약 가루 압축 모델 총설 · Chin. J. New Drugs) 가 *"the increasing tortuosity possibly impedes the wetting step of the electrode [9]"* (p.371) 의 근거로 달려 있다 — 내용이 맞지 않는다 (앞 논문에서도 같은 문헌이 같은 문장에 달렸다 · meyer2017 카드 §3-11 14 번).
12. *"the compaction behavior of the mixed NCA and the NCM111 cathode are very similar, while the NCA cathode exhibits slightly higher porosities.  In contrast, the NCA‐80/20 cathode has a more distinct porosity decrease"* (p.375) — 'mixed NCA' 가 가리킬 전극은 NCA-80/20 뿐인데 바로 다음 문장이 그 전극을 '대조' 로 든다 · Fig 5 에서 NCM111 과 닮은 것은 NCA (No.2) 다.
13. Fig 10 의 *"R2 = 0,996"* 은 원점 통과 맞춤의 비중심 값 (평균 기준 0.948 · §3-6) · 본문은 소수점을 쉼표로 적는다.
14. *"the deviation between the predicted εC,min and the achieved εC,min_a increases significantly"* (No.10–12 · p.374) ↔ 판독에서는 달성 − 예측이 다른 전극과 같고 달성 − 외삽이 크다 (§3-4).
15. 같은 캘린더 (GKL 400) 의 롤 치수가 논문마다 다르다: 이 논문 Ø430 × 폭 465 mm · 앞 논문 Ø450 × 470 mm (meyer2017 카드) · Diener 2022 Ø465 × 폭 430 mm (diener2022 카드) — 이 카드의 접촉 길이 어림은 ±4 % 안에서만 달라진다.
16. 기호가 섞여 쓰인다: 압연 전 기공률 ε0 ↔ ε_C,0 · 면적 부하 M_C (본문 · Fig 10) ↔ 식 (3) 의 m_E · m_C (질량 부하) · 식 (3) 아래 설명의 h_C (집전체 두께) 와 ε_C · ρ_C 의 C (코팅) 가 같은 첨자다.

---

## 4. ★ 방법 — 장치 · 측정 사슬 · 해석

### 4-1. 장치
- Saueressig GKL 400 파일럿 2 롤 캘린더 (롤 Ø430 × 폭 465 mm [이 논문 인쇄] · 최대 1500 N/mm · 최소 간극 25 µm · 롤 힘 = 주 실린더의 하중 덜림 — 세부는 참고 [22]) · Mesys USM200 (초음파 감쇠 · 이동식 센서 · 건조 직후 질량 부하) · Mitutoyo ID-C 다이얼 게이지 (1 µm) · He 가스 피크노미터 (기종 [미확인]) · ASMEC UNAT 미세압축기 (지름 100 µm 원기둥 압자 · 2.8 mN/s) · BET · SEM (기종 · 조건 [미확인]).

### 4-2. 측정 사슬 (재구성)
- 슬러리 → doctor blade 연속 코팅 → 건조 구간 셋 → (건조 직후) 초음파로 질량 부하 m_E · m_C → 시트 (≈300 mm) 로 자름 → 롤 간극을 정하고 통과 (압밀 상태마다 시트 2 장 · 상온) → 통과 중 롤 힘 F_N → q_L = F_N/w_C → **롤을 지난 전극**에서 두께 h_E (24 점 무늬) → 식 (3) ε_C = 1 − (m_E − m_C)/((h_E − h_C)·ρ_ph) → 전극마다 (q_L, ε_C) 점 ≈7–10 개 [판독] → 식 (2) 맞춤 (ε_C,min · γ_C · Fig 2 의 '외삽 최소') · 식 (4) 맞춤 (γ_C 하나 · Fig 5 · 9 · 6 · 10) → γ_C ↔ M_C 직선 (Fig 10 · μ) → 표 3.
- 따로: 활물질 입자 ≥ 24 개씩 미세압축 → 파괴 세기 누적 분포 (Fig 7) · BET · 입자 밀도 · 코팅 속 입자 SEM (Fig 8) · 단면 SEM (Fig 4).
- 간극 → 선하중 → 기공률의 순서지만 **간극 값은 '최소 25 µm' 말고는 보고되지 않는다** (독립 변수로 쓰인 것은 잰 선하중).

### 4-3. 해석
- 식 (4) 의 **오차 가중 최소제곱** [카드 추론 — 범례에 reduced χ² 를 적었고 이 카드의 가중 재맞춤이 같은 크기의 χ² 를 낸다] · 맞춤 수 = γ_C 하나 (ε_C,0 은 실측값으로 고정 · p = 0.4) · γ_C 의 ± = *"standard errors result from the error propagation of the approximations"* · 소프트웨어 · 잔차 그림 없음.
- Fig 10: γ_C ↔ M_C 를 원점 통과 직선으로 (*"linearly fitted with γC(MC = 0) = 0.  The first fitting proposed an ordinate intercept near zero"*) · R² 0.996 (비중심 · §3-6).
- 표 3 의 활물질별 μ = γ_C ÷ 223 g/m² (직선 가정으로 **옮긴** 값 · 오차도 γ_C 오차를 나눈 것).
- 기전 해석 (US 채움 · 마찰 면적 · 재배열 단계) 은 **정성 논증**이다 — 마찰 · 재배열을 잰 측정은 없고 문헌 둘 ([26] 금속-나노 알루미나 복합 가루 · [27] 다입자 유한요소) 을 든다.

### 4-4. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) 입자 · DEM**: 입자 계산이 **없다** — 'DEM' · 'discrete' · 'simulation' (본문) 0 회.  계산 문헌 인용은 둘: 저항망 유효 전도 모델 [8] (서론) 과 *"the interparticular friction affects the compaction pressure significantly [27]"* (다입자 유한요소 · 제목은 참고문헌 목록에만).  ⇒ DEM 의 한계에 대한 문장 = **말 없음**.  다만 저자의 머릿속 그림은 단단한 구 모형과 같다: *"the particles can be assumed as hard and incompressible"* (p.373) · Fig 3 은 압연 전 ↔ 최대 압밀에서 **활물질 원의 모양이 그대로**이고 탄소 · 바인더만 IS 에서 US 로 옮겨 간 2D 그림이다.
- **(ii) 소성 · 변형 기전**: 재지 않았다.  저자의 말 = ① Heckel 의 K 는 *"the plastic deformability of the particular bulk"* · Heckel 식은 취성 재료 (알루미나) 에 덜 맞지만 활물질이 첨가제 기지에 묻혀 *"increasing the deformability of the coating drastically"* ② 압밀은 초기의 **재배열** (입자 간 마찰이 저항) → 첨가제가 IS 에서 밀려나 US 를 채움 → (흑연) 파편이 US 를 채움 → 그 너머는 **입자 파괴** (*"particle breakage are expected"*) ③ 입자 한 층은 파괴 없이 못 누른다.  활물질 입자 자체의 소성 변형은 말하지 않는다 (단단하고 비압축이라는 가정).  항복 · 경도 값 없음 — 있는 것은 2 차 입자의 **파괴 세기** (Fig 7).  택한 우회 = 입자를 풀지 않는 현상 식 (맞춤 수 1) · 계산 비용 없음.
- **(iii) 차원**: 두께 방향 평균 (1D · 24 점 면 평균) + 2D 단면 SEM 두 장 (정량 없음) + 2D 개념 그림.  충전 기준 구조 (단순 입방 · 입방 조밀) 는 3D 같은 크기 구.  두께 방향 기울기 · 폭 방향 분포 · 2D ↔ 3D 에 대한 말 없음.
- **(iv) 탈압**: *"The coating relaxes elastically when it leaves the gap"* (p.371) 한 문장 — 크기 · 시간 · 측정 없음.  **이 논문의 모든 기공률은 회복이 끝난 (또는 진행 중인) 뒤의 값**이고 하중 아래 간극 · 기공률은 없다.  설정 간극 25 µm 에서 나온 코팅이 27–89 µm 라는 것 (§3-9 · 카드 산술) 이 '간극 ≠ 압연 뒤 두께' 를 보여 줄 뿐, 롤 벌어짐과 되돌아옴을 가르지 못한다.  압연 뒤 측정까지의 시간 [미확인] (순간 회복 = `diener2022_*` · 보관 중 두께 = `kollenda2024_*`).

### 4-5. 기법 미니 용어집
- **캘린더링 (calendering · 압연)** = 서로 반대로 도는 두 롤 사이로 전극을 통과시켜 코팅을 누르는 공정.
- **선하중 (line load) q_L** = 롤 힘 ÷ 코팅 폭 (N/mm) — 압력이 아니다 (접촉 길이로 나누지 않음).
- **면적 부하 (mass loading) M_C** = 단위 면적당 코팅 질량 (g/m²).
- **코팅 기공률 ε_C (기하)** = 1 − 코팅 밀도/성분 평균 고체 밀도 — 질량 · 두께 · 피크노미터 밀도로 셈.
- **compaction resistance γ_C** = 지수 식에서 기공률이 끝값으로 다가가는 빠르기를 정하는 수 (N/mm) — 끝값까지 거리의 63 % 를 가는 선하중 · 클수록 같은 압밀에 큰 선하중이 든다.
- **mass dependency factor μ** = γ_C ÷ M_C (kN·m/g) — 부하에 비례하는 몫을 뺀 수.
- **끝값 비 p** = 최소 기공률 ÷ 압연 전 기공률 (이 논문 0.4 · 가정).
- **단순 입방 (scp) · 입방 조밀 (ccp) 충전** = 같은 크기 구의 규칙 배열 — 기공률 47.64 % · 25.95 %.
- **IS (interparticle space) · US (unoccupiable space)** = 저자 용어 — 활물질 입자 사이에 끼어 입자를 벌리는 자리 · 활물질이 어차피 못 들어가는 틈.
- **파괴 세기 (breaking strength) σ_b** = 입자 하나를 평판으로 눌러 첫 파괴가 나는 힘 ÷ 투영 면적.
- **reduced χ² (χ_ν²)** = 오차로 나눈 잔차 제곱합 ÷ 자유도 — 1 근처면 오차 막대만큼 맞는다는 뜻.
- **Heckel 식** = ln[1/(1 − D)] = K·P + A — 가루 압축에서 기공률이 압력에 대해 1 차 반응처럼 준다는 식 (1/K 를 항복 압력으로 읽는다).

---

## 5. Figure set ★
| 그림 · 표 · 식 | 내용 | 크롭 | 우리 활용 |
|---|---|---|---|
| Fig 1 (p.372) | 압연 개념도 — 바꾼 것 (활물질 AM · 면적 부하 M_C · 압연 전 기공률 ε_C,0) · 결과 (코팅 기공률 ε_C) · 선하중 q_L | `fig_1.png` | 기호 정의 |
| ★ Fig 2 (p.374) | 전극 15 종의 압연 전 · 달성 최소 · 외삽 최소 · 예측 최소 (0.4 ×) 기공률 | `fig_2.png` | 판독 60 행 (§3-4) — p = 0.4 의 근거와 한계 |
| Fig 3 (p.374) | 충전 차이 그림 (uncompacted ↔ maximal compaction) — 구형 활물질 · 도전 탄소 · 바인더 · US · IS | `fig_3.png` | 저자의 기전 그림 — 2D · 입자 모양 불변 (§4-4) |
| Fig 4 (p.375) | 단면 SEM — No.6 (80 g/m²) ↔ No.8 (160 g/m²) | `fig_4.png` · `fig_4_left.png` · `fig_4_right.png` | 얇은 코팅 (입자 ≈3 층) 이 더 성기다 (정성) |
| ★ Fig 5 (p.375) | 선하중 ↔ 코팅 기공률 + 식 (4) 곡선 — 왼쪽 NCA-80/20 · NCA · NCM111 / 오른쪽 NCM811 · NCM622 · NCM111 · 범례에 reduced χ² | `fig_5.png` · `fig_5_left.png` · `fig_5_right.png` | 판독 44 행 (§3-5) · 잔차 무늬 |
| ★ Fig 6 (p.376) | γ_C 막대 (활물질 다섯) | `fig_6.png` | 판독 5 행 (§3-5) = 표 3 × 223 g/m² |
| ★ Fig 7 (p.376) | 활물질 입자 파괴 세기의 누적 분포 (흑연 · NCM811 · NCM622 · NCM111 · NCAI · NCAII · 축 MPa) | `fig_7.png` | 판독 6 행 (§3-8) — 조건 R7 · 단위 시험 U1 의 실험 쪽 |
| Fig 8 (p.377) | 코팅 속 활물질 입자 SEM 넷 | `fig_8.png` · `fig_8_ncm111.png` · `fig_8_ncai.png` · `fig_8_ncm622.png` · `fig_8_ncm811.png` | Ni 함량 ↑ → 2 차 입자가 느슨 (정성) |
| ★ Fig 9 (p.377) | 선하중 ↔ 코팅 기공률 + 식 (4) 곡선 — 왼쪽 No.6 · 7 · 8 / 오른쪽 No.8–12 · 범례에 reduced χ² | `fig_9.png` · `fig_9_left.png` · `fig_9_right.png` | 판독 46 행 (§3-6) |
| ★ Fig 10 (p.378) | 면적 부하 ↔ γ_C + 원점 통과 직선 · 맞춤 상자 (μ · R²) | `fig_10.png` · `eq_fig10_inset_linear_fit_gamma_mu.png` | 판독 7 행 (§3-6) — γ_C 는 부하에 비례 |
| 표 1 (p.373) | 활물질 입자 (종류 · 입도 · 모양) | `tab_1.png` | §3-1 |
| 표 2 (p.373) | 전극 조성 (질량 · 부피 분율) · 면적 부하 | `tab_2.png` | §3-1 · 압연 전 기공률 · 고체 밀도 되짚기 (§3-11) |
| ★ 표 3 (p.378) | μ (활물질 다섯 + 부하 계열) | `tab_3.png` | §3-5 · §3-6 |
| 식 (1) (p.372) | ε = ε0 + exp(−K·P) (인쇄 그대로 · 덧셈표 오류) | `eq_01_heckel_porosity_form.png` · `eq_01_heckel_porosity_form_with_text.png` | Heckel 꼴 (인용할 때 오류 표지) |
| ★ 식 (2) (p.372) | ε_C = ε_C,min + (ε_C,0 − ε_C,min)·exp(−q_L/γ_C) | `eq_02_compaction_model_coating_porosity.png` · `eq_02_compaction_model_coating_porosity_with_text.png` | 후보 M0 의 2 수 꼴 |
| 식 (3) (p.372) | ε_C = 1 − ρ_C/ρ_ph = 1 − (m_E − m_C)/((h_E − h_C)·ρ_ph) | `eq_03_coating_porosity_definition.png` · `eq_03_coating_porosity_definition_with_text.png` | 기공률 연산자 (단계 0) |
| ★ 식 (4) (p.375) | ε_C = ε_C,0(p + (1 − p)·exp(−q_L/γ_C)) | `eq_04_model_with_predicted_minimum_p.png` · `eq_04_model_with_predicted_minimum_p_with_text.png` | 후보 M0 의 1 수 꼴 |
| ★ 식 (5) (p.378) | ε_C = ε_C,0(p + (1 − p)·exp(−q_L(μ·M_C))) (인쇄 그대로 · 나눗셈표 누락) | `eq_05_model_with_mass_loading_mu.png` · `eq_05_model_with_mass_loading_mu_with_text.png` | 부하까지 넣은 꼴 |
| 인라인 (p.373) | q_L = F_N/w_C | `eq_p373_line_load_definition_inline.png` | 선하중 ≠ 압력의 근거 |
| 인라인 (p.374) | ε_C,min_p = p·ε_C,0 with p = 0.4 | `eq_p374_min_porosity_prediction_p04_inline.png` | 끝값 가정 |
| 인라인 (p.378) | γ_C = μ·M_C | `eq_p378_gamma_mu_mass_loading_inline.png` | 부하 비례 |
| 근거 문단 20 장 | 서지 · 초록 · 날짜 · 되돌아옴 한 문장 · '공정 모형이 아직 없다' · 미세압축 · 전극 구성 · 캘린더 · 맞춤 수 하나 · 얇은 코팅 · 형상 · p = 0.4 · 맞음 / 안 맞음 · LMO · 흑연 · 활물질 해석 · 파괴 세기 · 마찰 결론 · 부하 해석 · 표 3 논의 · 결론 | 아래 목록 | §0 – §3 · §10 인용문의 원문 대조 |

- 근거 문단 크롭 (쪽 순 · 카드가 숫자 · 정의 · 단정의 근거로 인용한 문단만): `txt_p371_title_authors_journal.png` (서지) · `txt_p371_abstract_keywords.png` (초록 · 키워드 — *Heckel-based* · *equally sized spheres* · 80–280 g/m²) · `txt_p371_doi_received_accepted.png` (DOI · 날짜 · 저작권) · `txt_p371_intro_roll_compaction_coating_relaxes_elastically.png` (*"The coating relaxes elastically when it leaves the gap"*) · `txt_p372_intro_optimum_no_process_model_to_date.png` (*"no approaches to develop a process model"*) · `txt_p372_methods_microcompression_breaking_strength.png` (미세압축 절차 · 파괴 세기 정의) · `txt_p372_p373_electrodes_overview_no13_15_from_other_studies.png` (전극 구성 · No.13–15 의 출처) · `txt_p373_calendering_gkl400_roll_430mm_sheets_ambient.png` (캘린더 · 시트 · q_L = F_N/w_C · 상온) · `txt_p373_min_porosity_sole_fitting_parameter_scp_is_us.png` (*"sole fitting parameter"* · 단순 입방 47.64 % · IS · US) · `txt_p373_p374_initial_porosity_low_mass_loading_interface.png` (얇은 코팅의 높은 기공률 · 계면 기공) · `txt_p374_additives_graphite_lmo_flake_morphology_loose_packing.png` (No.13–15 의 첨가제 · 형상) · `txt_p374_min_gap_25um_factor_p04_scp_ccp_054.png` (최소 간극 25 µm · 0.54 → p = 0.4) · `txt_p374_prediction_works_no1_12_fails_no13_15_p033.png` (맞음 / 안 맞음 · 0.33) · `txt_p374_p375_lmo_p060_graphite_p029_reasons.png` (0.60 · 0.29 의 이유) · `txt_p375_active_material_gamma_small_particles_friction.png` (활물질별 γ_C 해석) · `txt_p375_p376_breaking_strength_ni_content_bet_density.png` (파괴 세기 · BET · 입자 밀도 · *no general validity*) · `txt_p376_breaking_strength_not_dominant_friction_rearrangement.png` (파괴 세기는 지배 인자 아님 · 마찰 · 재배열) · `txt_p376_mass_loading_gap_limit_linear_gamma_monolayer.png` (간극 한계 · 직선 · 입자 한 층) · `txt_p378_mu_table3_discussion_additive_surface.png` (표 3 논의 — *"The mass dependency of No. 5 is not so pronounced"* · 첨가제 표면) · `txt_p378_conclusions_validity_spherical_10wt_outlook.png` (적용 범위 · 12 % · 전망).
- 앞뒤 문장과 함께 자른 식 크롭이 받치는 인용문: `eq_01_heckel_porosity_form_with_text.png` (Heckel 소개 · *"less suitable for brittle materials as alumina … embedded in the additive matrix"*) · `eq_02_compaction_model_coating_porosity_with_text.png` (*"reciprocal equivalent to Heckels constant K"* · *"second fitting parameter"*) · `eq_03_coating_porosity_definition_with_text.png` (기공률 측정 사슬 전체 — 초음파 질량 부하 · 다이얼 게이지 24 점 · He 피크노미터 · *"in well corresponce with … mercury porosimetry [22,23]"* · *"taking the mass fractions of each component into account"*) · `eq_04_model_with_predicted_minimum_p_with_text.png` (*"No. 13–15 are not further discussed"*) · `eq_05_model_with_mass_loading_mu_with_text.png` (*"about three layers … about 45 μm … 1.1 mAh/cm2 … valid by all means for relevant mass loadings MC > 80 g/m2"*).

---

## 6. Post-processing ★
- **저자가 한 것**: 롤 힘 → 선하중 · 질량 + 두께 + 피크노미터 밀도 → 기하 기공률 · 식 (2) 2 수 맞춤 (외삽 최소) · 식 (4) 1 수 오차 가중 맞춤 (reduced χ² 표기) → γ_C 막대 · γ_C ↔ M_C 원점 통과 직선 → μ · 입자 파괴 세기의 누적 분포 · 충전 구조 비 (0.54) 와의 비교.
- **이 카드가 한 것**: (1) 박힌 300 dpi 래스터에서 눈금 맞춤 판독 (머리 주석) — 검증 일곱 가지 (2) 표 2 로 압연 전 기공률 · 성분 밀도 · 혼합물 밀도 되짚기 (No.1 ↔ 2 줄 바뀜 · No.13 의 분모 밀도) (3) p 의 재검 (달성 ↔ 외삽 · 상수 ↔ 비례) (4) 인쇄 매개변수 곡선의 잔차 무늬 · 1 수 재맞춤 (5) Fig 10 재맞춤 (가중 · 절편 · 멱 꼴 · 중심 R²) (6) 식 (4) ↔ Heckel 대수 · 국소 기울기 (7) 최소 기공률에서의 활물질 부피 분율 (8) 코팅 두께 · 접촉 길이 · 평균 압력 어림 [카드 추정] (9) 앞 논문 γ_C ÷ 한 면 부하.  도구 = numpy + PIL (스크립트는 작업 scratchpad · 판독 결과는 `digitized.csv`).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · `docs/` 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 계 | 액체 LIB **압연** 양극: 구형 NCA / NCM (x50 5.8–15.2 µm) 90–94 wt% + 도전 탄소 + 바인더 6–10 wt% · 압연 전 기공 42–55 % | ASSB 복합 양극 NCM811 + LPSCl · 일축 300 MPa · 순수 SE 10–13 % (랩 표준) · 복합 ≈15–16 % (real_14 15.6 % · CLAUDE.md) | **무른 상이 다르다** (다공 탄소-바인더 기지 6–10 wt% ↔ 부피의 절반쯤을 차지하는 소성 LPSCl) · 기공이 이온 통로인 계 ↔ 기공이 결함인 계 |
| 하중 변수 | 선하중 q_L = F_N/w_C · ≤ 867 N/mm · 압력 환산 없음 | 압력 300 MPa (일축 · 판 반력) | 단위가 다르다 — 접촉 길이 없이는 대응 불가 ([카드 추정] 마지막 점 평균 ≈150–310 MPa) |
| 상태 | **압연 뒤** (하중 0 · 회복 포함) | DEM 기공 = 목표 압력 도달 뒤 판 고정 상태 · MPM `hold` (CLAUDE.md) | 우리 값은 '누른 채 (판 고정)' · 이 논문은 '뺀 뒤' — 같은 표에 넣지 않는다 |
| 압밀 곡선 꼴 | ε = ε_0·(0.4 + 0.6·exp(−q/γ)) — 끝값 = 0.4 × 처음 (고정) · 맞춤 수 1 | DEM 순수 SE Heckel ln(1/(1−D)) = K·P + A · R² 0.965 · P_y 138 MPa · σ_y_eff 46 MPa (4 압력 · CLAUDE.md) | 같은 지수 감쇠 계열 — 끝값이 0 (우리 Heckel 직선) ↔ 처음 값의 0.4 배 (이 논문) |
| 맞춘 값 수 | 전극마다 1 (γ_C) · 부하 계열 전체에 1 (μ) · p 는 전 전극 공통 경험값 | DEM: E_eff 하나 (18 배 연화 · 1.35 GPa) · MPM: σ_y 하나 (0.30 GPa · E 1.53 · ν 0.49) | 이 논문 = 현상 곡선 맞춤 · 우리 = 입자 모델의 재료 값 |
| 기공 바닥 | 닿은 최소 0.19–0.24 = 0.447 × 압연 전 · 그때 활물질 부피 분율 0.58–0.68 [카드 산술] · 더 내리면 *"particle breakage are expected"* | DEM: 구가 영원히 구라 연화 없이는 ≈20 % 바닥 (CLAUDE.md) · MPM: 얼린 AM + J2 SE 는 정직하게 누르면 ε_sphere 1.13 % 까지 간다 (R1 · CLAUDE.md) | 실험의 바닥은 단단한 활물질 골격이 조밀 충전에 이른 데서 온다 [카드 추론] — 우리 MPM 에 그 바닥이 없는 것이 AM 하중분담 ② 문제와 같은 자리 |
| 작은 활물질을 섞으면 | NCAI 에 NCAII (x50 5.8 ↔ 15.2 µm) 20 wt% → γ_C 310 → 220 N/mm (−29 %) · 압연 전 기공률은 거의 같다 (0.457 → 0.450) | DEM 코퍼스의 이봉 AM (P:S) 은 더 조밀 (Furnas 충전 · CLAUDE.md) · MPM 스캐폴드에서는 작은 AM 이 많을수록 SE 통로가 좁아 **SE 응력이 높다** (d_h 접힘 · CLAUDE.md) | **같은 양이 아니다** — 이 논문 = 코팅 전체를 누르는 선하중 · 우리 d_h 결과 = 얼린 AM 골격 사이 SE 상의 응력 |
| 얇은 층 | 입자 ≈3 층 (45 µm) 의 압연 전 기공률이 +0.12 · 닿은 최소도 높다 (0.238 ↔ 0.19–0.20) · ≈6 층 (73 µm) 부터 일정 [카드 산술] | 얇은 (1–2 mAh) 단일 대립 침대에서 DEM ↔ MPM 이 갈린다 · σ_e 식의 얇은 층 문턱 T/d_AM = 8 (CLAUDE.md) | 벽 · 표면 효과가 실험에서도 수 층 두께까지 간다 (방향만 — 습식 코팅의 건조 구조 ↔ 우리 건식 가압) |
| 두께와 저항 | γ_C ∝ M_C (선하중 기준) | 판 반력 = 압력 (면적으로 나눈 값) · 주기 경계 (벽 마찰 없음) | 선하중이 두께에 비례해 드는 것은 압력 기준으로는 절반쯤 기하일 수 있다 [카드 추론 §3-9] |
| 기공률 연산자 | 기하 (질량 · 두께 · 성분 He 밀도의 평균) — 평균 방식이 No.13 을 5–9 %p 움직임 | ε_sphere (구 부피 합) · ε_union (정확 합집합) · MPM 관례 — 관례 오프셋 1.251 %p (CLAUDE.md) | 실험 쪽 분모 밀도의 차이가 우리 모델 쪽 관례 차이보다 크다 |
| 활물질 파괴 | 입자 하나의 파괴 세기 분포 (NCM811 중앙 ≈63 MPa · 투영 면적 기준) — 압연 뒤 파괴 관찰은 없음 | DEM 파괴 판정 (Auerbach · 힘 기준 · CLAUDE.md) | 정의 (첫 파괴 힘 ÷ 투영 면적) 를 맞춘 뒤 입자 하나 수준에서만 견줄 수 있다 |
| 입자 계산 | 없음 | DEM + MPM | — |

### 7-2. ★ 랩 기준과 나란히 (판정 없이 · **랩 표준과 다른 문헌 값 = 다른 재료 · 다른 공정**)
| 출처 | 재료 | 상태 | 고체 밀도 분모 | 기공 |
|---|---|---|---|---|
| **랩 표준** | 순수 LPSCl | 300 MPa | **1.64 g/cm³** (고정) | **10–13 %** |
| 이 논문 No.1–5 (판독 · 닿은 최소 · ≈720–796 N/mm) | NCA / NCM 94 · 도전 탄소 3 · 바인더 3 wt% · 액체 LIB · 223 g/m² | 압연 뒤 | 성분 He 밀도의 평균 (값 미인쇄 · [카드 산술] ≈4.2–4.3 g/cm³) | **20.1–21.5 %** |
| 이 논문 No.7–12 (판독 · 닿은 최소 · ≈424–867 N/mm) | NCM111 90 · 5 · 5 wt% · 120–284 g/m² | 압연 뒤 | 〃 ([카드 산술] ≈3.9 g/cm³) | **18.8–21.4 %** |
| 이 논문 No.6 (판독 · 닿은 최소 · ≈300 N/mm) | 〃 · 80 g/m² (입자 ≈3 층) | 압연 뒤 | 〃 | **23.8 %** |
| 이 논문 모델의 끝값 (0.4 × 압연 전 · No.1–12) | 〃 | 압연 뒤 · 선하중 → ∞ (점근) | 〃 | **16.9–21.9 %** |
- 이 표는 **"랩 표준과 다른 문헌 값"** 의 자리다 — 고체전해질이 없는 코팅이고 압력 대응도 없다 (랩 표준의 분모 1.64 g/cm³ 는 고정 — 판정하지 않는다).  뜻을 가질 수 있는 것은 **단단한 구형 활물질이 90–94 wt% 인 코팅은 기계 한계까지 눌러도 압연 뒤 기공률이 ≈19–21 % 에서 멈춘다**는 크기 감각뿐이다.

### 7-3. ★ 18 배 연화 · Heckel P_y 138 MPa 와 견줄 자리 (frame [2] · [3])
- 우리 DEM 은 E_SE 24 → E_eff 1.35 GPa (18 배 연화) 로 순수 SE 의 **가압 기공**을 맞추고, 4 압력 Heckel 직선에서 P_y 138 MPa (R² 0.965) 를 읽는다 (CLAUDE.md).  이 논문은 그 값을 보정 · 반증할 숫자를 **주지 않는다** (SE 없음 · N/mm · 압연 뒤).
- 주는 것은 **식의 꼴에 대한 것 둘**이다: ① 끝값이 0 이 아닌 자료 (이 논문 0.4 × 처음) 는 Heckel 좌표에서 휜다 — 국소 1/K 가 1.67 γ_C → 14.4 γ_C (§3-10) · 우리 DEM 은 구가 영원히 구라 바닥이 있는 모델이므로 넓은 압력 창에서는 같은 휨이 나올 수 있다 [카드 추론] ② 한 지수는 **초기의 빠른 감소**를 못 따른다 (다섯 활물질 모두 낮은 선하중에서 자료가 0.02–0.04 낮다 · reduced χ² 2.2–4.0) — 저자 말로는 재배열 단계.  4 점 · R² 0.965 는 이 둘을 가를 점 수가 아니다.
- MPM (σ_y 0.30 GPa 를 순수 SE 한 점에 맞춤) 쪽: 한 점 보정 뒤의 다압력 곡선을 '처음 × (끝값 비 + 지수 감쇠)' 로 줄여 적을 수 있다 — 견줄 실측 짝은 이 논문이 아니라 **압력 축 · 황화물** 자료다 (`heck2026_*` β-Li₃PS₄ 가루 in-die γ_c 0.32 ± 0.02 GPa · `lee2025_heckel_*` LPSCl Heckel P_y 294–344 MPa — 값은 그 카드들의 것 · 재료 · 상태 표지 필수).

### 7-4. 같은 계열 식을 쓴 정본 카드와 나란히 (값은 그 카드의 것)
| 출처 | 재료 | 하중 변수 · 상태 | γ | 끝값 |
|---|---|---|---|---|
| 이 논문 | LIB NCM111 양극 (단면 80–284 g/m²) | 선하중 · 압연 뒤 | 98–371 N/mm (= 1.31 kN·m/g × 부하) | 0.4 × 압연 전 (고정) |
| 이 논문 | LIB NCA · NCM622 · NCM811 양극 (단면 223 g/m²) | 선하중 · 압연 뒤 | 220–310 N/mm | 〃 |
| `meyer2017_*` | LIB NCM111 양극 (양면 451 g/m²) | 선하중 · 압연 뒤 | 292–309 N/mm | 맞춤 (외삽) 3.16–3.21 g/cm³ |
| `meyer2017_*` | LIB 흑연 음극 (양면 197 g/m²) | 선하중 · 압연 뒤 | 126–161 N/mm | 맞춤 (외삽) 1.71–1.80 g/cm³ |
| `heck2026_*` (표 S7) | β-Li₃PS₄ 가루 · HNBR 3 · 4.3 wt% 시트 | **압력 · 다이 안 (누른 채)** | 0.32 · 0.42 · 0.45 GPa | 1.99 · 1.68 · 1.69 g/cm³ |
| `heck2026_*` (표 S6) | β-Li₃PS₄ + HNBR 3 wt% 시트 | **압력 · 다이 밖 (뺀 뒤)** | 26–61 MPa | 1.12–1.33 g/cm³ |
- 선하중 기준 γ 는 **부하에 비례**하므로 (이 논문) 위 표의 N/mm 값끼리도 부하를 맞춰야 견줄 수 있다 — 앞 논문 양극 (한 면 225.5 g/m²) 의 292–309 N/mm 은 이 논문 NCM111 223 g/m² 의 297 ± 36 N/mm 과 같다 (§3-11).  압력 기준 값 (`heck2026_*`) 과는 단위가 맞지 않는다.

### 7-5. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 공정 규모의 하중 (선하중) ↔ 결과 구조 (압연 뒤 기공률) 실측을 한 수 (γ_C · μ) 로 줄인 현상 식 + 입자 하나의 파괴 세기 분포.
- **없는 것**: 압력 · 응력 · 하중 아래 상태 · 탈압량 · 입자 거동의 측정 · 계산 · 고체전해질 · 수송.  ⇒ DEM (접촉망 · 충전) 과 MPM (소성 형상 변화) **어느 반쪽의 입력도 아니고**, 입자를 풀지 않는 균질화 쪽 (후보 M0) 의 **식의 꼴 · 끝값을 정하는 법 · 보고 규약**에 닿는다.  저자의 그림 (단단하고 비압축인 구 + 재배열 + 마찰 + 틈을 채우는 무른 첨가제) 은 DEM 쪽 물리와 같지만 계산으로 시험하지 않았다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ (1) **혼합물 고체 밀도의 평균 식을 등록**: 성분 밀도를 질량 분율로 산술 평균하면 (4.26) 부피가 더해지는 옳은 평균 (3.84) 보다 11 % 크고, 같은 전극 (No.13) 의 기공률이 0.57 → 0.52 (압연 전) · 0.26 → 0.18 (최소) 로 5–9 %p 달라진다 (§3-11 · 카드 산술) — 복합 양극 실측과 견줄 때 **ρ = (Σ w_i/ρ_i)⁻¹ 인지** 와 성분 밀도 값을 칸으로 둔다 (LPSCl 1.64 g/cm³ 는 랩 고정) (2) **끝값 비 같은 '기공률의 비' 는 분모 밀도에 민감**하다 (같은 전극 0.46 ↔ 0.34) → 비로 적는 판정 기준은 분모를 함께 등록 (3) **누른 채 ↔ 뺀 뒤** 표지 · 설정 간극은 두께가 아니다 (4) 질량 부하를 **압연 전** 값으로 쓰는 실험 관행 (늘어난 면적 미보정) | 값 전이 안 함 (액체 LIB) · 밀도 평균 방식은 원문에 인쇄돼 있지 않다 (카드가 표 2 에서 되짚음) |
| **단계 1 · 2 · 3** | 없음 (계산 없음) | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 맞춤 표적 아님 (SE 없음).  참고 하나: 한 압력의 기공 한 점에 맞춘 재료 값은 곡선의 **모양** 을 검증하지 못한다 — 이 논문의 1 수 곡선도 끝점은 지나지만 낮은 선하중에서 0.02–0.04 어긋난다 (§3-5) → 맞춘 뒤 다압력 곡선의 **초기 구간**을 따로 본다 (결과 전 등록) | 값 · 재료 |
| **단계 5** (3D 복합 압밀) | 대조 값 없음.  정성 방향 셋: ① 작은 활물질 20 wt% 를 섞으면 (크기비 2.6) 선하중 기준 저항이 29 % 낮다 ② 굵고 처음에 성긴 활물질 (NCM811 · 압연 전 0.479) 도 저항이 낮다 — 저항 수 γ_C 는 '얼마나 단단한가' 보다 **'처음에 얼마나 성긴가 · 초기에 얼마나 빨리 주는가'** 를 잰다 ③ 닿은 최소에서 활물질 부피 분율 0.58–0.68 (무작위 조밀 충전 근처 · 카드 산술) | 고체전해질 없음 · 선하중 · 뺀 뒤 · 활물질 다섯은 입도 · 표면 · 세기 · 공급사가 함께 다르다 |
| **단계 6** (탈압 · 되돌아옴) | 없음 — *"relaxes elastically"* 한 문장.  주의로만: **압연 문헌의 기공률은 뺀 뒤 값**이고 **'두꺼울수록 덜 되돌아온다' 의 근거는 이 논문에 없다** (Kollenda 2024 가 이 논문을 그 근거로 인용 — §0-1) | 회복 크기 · 시간 [미확인] |
| **단계 7** (형상 · 피복 · 수송) | 없음 (서론의 수송 문헌 인용뿐) | — |
| **후보 D0** (지금 DEM) | DEM 언급 없음.  저자의 물리 그림 (단단한 구 · 재배열 · 입자 간 마찰이 선하중을 정함 · 첨가제가 틈을 채움) 은 구 DEM 이 담는 기전과 같다 — 선하중 ↔ 기공률 실측점 (§3-5 · §3-6) 은 압연 DEM 카드들 (`sangros2019_*` · `schreiner2020_*` · `ngandjong2021_*`) 이 표적으로 삼는 종류의 자료 | DEM 한계 진술 없음 · 마찰이 지배라는 결론은 추론 (마찰 측정 없음) |
| **후보 A′-0 · A · A′** (MPM 접촉 · 강체 AM · 입자별 속도장) | 없음 | — |
| **후보 B** (입자별 FE) | 인용 한 줄 — 다입자 유한요소 [27] 가 '입자 간 마찰이 압축 압력에 크게 영향' 의 근거 (그 논문은 정본에 카드 없음 → 정독 출력 n) | 이 논문 자체에는 없음 |
| **후보 C · C′** (MDR · 항복 캡 DEM) | 없음 — 접촉 · 항복 값 없음 | — |
| **후보 M0** (균질화 압밀 · Heckel · 캡) | ★★ (1) **끝값을 맞춤에서 빼는 법**: ε = ε_0·(p + (1 − p)·e^(−q/γ)) — 끝값을 처음 값의 비로 묶어 맞춤 수를 하나로 (앞 논문의 '끝값이 맞춤 범위에 따라 변한다' 를 푸는 한 길) (2) **그 대가 넷**: p 는 이론 값 (0.54) 이 아니라 경험값 (0.4) 이고 재료 · 조성에 따라 0.29–0.60 · 분모 밀도에 민감 · 닿은 값 (0.447 ×) 이 아니라 점근값 · 한 지수의 잔차 무늬 (χ² 2–4) (3) **저항 수가 재료 상수가 아닐 수 있다**: 선하중 기준 γ_C 는 부하에 비례 (μ 로 정규화) — 우리 압력 축에서도 P_y 가 침대 두께 · 벽 마찰에 무관한지를 한 번 확인할 일 [카드 추론] (4) 맞춤 품질은 R² 가 아니라 **오차 대비 잔차 (reduced χ²) 와 잔차의 무늬**로 보고 (이 논문은 χ² 를 범례에 적었다 — 값이 2–6 인데도 '실용에 충분' 이라 한 것은 본받지 않는다) | N/mm 이라 우리 MPa 값과 수치 비교 불가 · 식은 유도가 아니라 가정 + 맞춤 · 물리 수 (마찰 · 세기) 와의 연결은 정성 |
| **U0–U6** (단위 시험) | U1 (입자 하나 압축) 의 **실험 쪽 본**: 2 차 입자를 평판 (지름 100 µm) 으로 눌러 첫 파괴 힘 ÷ 투영 면적 · 입자 ≥ 24 개 · 누적 분포로 보고 — NCM811 중앙 ≈63 MPa (≈10 mN @ 14.3 µm · 카드 산술) | 힘–변위 곡선 자체는 실리지 않았다 · 활물질 공급사 미상 · 우리 SE 입자 자료 아님 |
| **R1** (AM 이 움직이고 하중을 나눠 짐) | 정성 — 활물질은 *"hard and incompressible"* · 변형은 첨가제 기지가 맡는다 · 초기는 재배열.  닿은 최소에서 활물질 부피 분율 0.58–0.68 [카드 산술] = 골격이 조밀 충전에 이른 뒤에는 더 안 눌린다 (파괴 없이는) | 하중 몫 숫자 없음 |
| **R2 · R3** | 없음 | — |
| **R4** (탈압 · 되돌아옴) | 단계 6 과 같음 (한 문장) | — |
| **R5** (맞추는 값은 모델마다 하나) | ★ 같은 방향의 사례: 맞춤 수를 3 (앞 논문) → 1 로 줄이자 값이 전극끼리 견줄 수 있게 됐다 (γ_C ↔ 부하의 직선이 드러남).  대가 = 고정한 수 (p) 가 틀리는 범위 (No.13–15) 에서는 쓸 수 없다 | 현상 식의 이야기 — 입자 모델의 재료 값과는 층이 다르다 |
| **R6** (SE 입자 형상 변형) | 없음 (SE 없음 · 활물질은 모양 불변으로 가정) | — |
| **R7** (AM 파괴) | ★ 입자 파괴 세기 분포 (§3-8 · 판독): NCM811 ≈63 · NCM622 ≈139 · NCM111 ≈274 MPa (투영 면적 기준 · Ni 가 많을수록 약함 — 공급사가 달라 일반화 불가) · **파괴 세기는 압밀 저항을 정하지 않는다** (저자 결론) · 기계 한계 너머에서는 파괴 예상 | 압연 뒤 파괴의 관찰 · 정량 없음 (속편 예고) · 평판 사이 한 입자의 값이라 침대 속 접촉 힘과 바로 견주지 못한다 |
| **결과 전 대조 항목** | 넣지 않는다 (N/mm · 액체 LIB · 뺀 뒤).  흐름 밖 표지로만: '구형 활물질 90–94 wt% 압연 양극의 닿은 최소 기공률 0.19–0.24 = 0.447 × 압연 전 · 선하중 축 · Meyer 2018' | ASSB 절대값 비교 금지 |

- **재료 · 차원 · 조건 차이**: 액체 LIB 압연 코팅 (첨가제 6–10 wt% · 기공 42–55 % → 19–24 %) ↔ 우리 ASSB 냉간 일축 가압 복합 양극 · 무른 상 = 다공 탄소-바인더 ↔ LPSCl · 하중 = 선하중 (롤 통과) ↔ 300 MPa (유지) · 상태 = 뺀 뒤 ↔ 누른 채 · 1D 두께 평균 ↔ 우리 3D 계산.

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **끝값을 맞춤에서 뺄 수 있으면 빼되, 무엇으로 정했는지를 결과 전에 등록한다** — 이 논문은 끝값을 '처음 × 0.4' 로 묶어 맞춤 수를 하나로 줄였고 그래서 γ_C ↔ 부하의 직선이 드러났다.  대가는 그 비가 경험값이고 (충전 이론의 0.54 가 아님) 재료 · 조성 · 분모 밀도에 따라 0.29–0.60 으로 변하며, 점근값이지 닿은 값이 아니라는 것 (후보 M0 · 단계 0).
2. **혼합물 고체 밀도는 부피가 더해지게 평균한다 (ρ = (Σ w_i/ρ_i)⁻¹) — 그리고 그 식을 값 옆에 적는다.**  같은 전극이 평균 방식 하나로 기공률 5–9 %p 달라진 실례 (No.13: 0.57 → 0.52 · 0.26 → 0.18) 가 같은 그룹의 연속 두 논문 사이에 있다 (단계 0).
3. **한 지수 (Heckel 류) 맞춤은 잔차의 무늬까지 본다** — 끝점을 지나도 초기 구간에서 0.02–0.04 어긋날 수 있다 (재배열 단계).  R² 대신 오차 대비 잔차 (reduced χ²) 와 구간별 부호를 보고한다 (후보 M0).
4. **압연 문헌의 N/mm 는 MPa 옆에도, 부하가 다른 다른 N/mm 옆에도 놓지 않는다** — γ_C 는 부하에 비례한다 (μ = γ_C/M_C 로 정규화 · 한 면 부하 기준인지 양면 합인지 표기).  놓으려면 접촉 길이 가정을 밝힌 어림임을 적는다 (이 카드의 ≈150–310 MPa 는 카드 추정이고 인용 금지).
5. **입자 파괴 세기는 정의를 맞춘 뒤 견준다** — 이 논문 = 첫 파괴 힘 ÷ 투영 면적 (πd²/4) · 다른 카드 (`song2025_insitu_ct_dem_*`) = 힘 ÷ d² → π/4 배 차이.  그리고 '약한 입자 = 잘 눌리는 전극' 이 아니다 (NCM111 ≈274 MPa 와 NCA ≈117 MPa 의 γ_C 가 같다) (조건 R7).
6. **얇은 침대의 벽 · 표면 효과는 실험에도 있다** — 입자 ≈3 층에서 압연 전 기공률 +0.12 · ≈6 층부터 일정.  우리 얇은 (1–2 mAh) 침대의 높은 기공률을 모델 결함으로만 읽지 않는다 (흐름 밖: 얇은 침대 해석 — 방향만 · 습식 코팅의 건조 구조와 건식 가압은 출발 구조가 다르다).
7. **'두꺼울수록 덜 되돌아온다' 의 근거로 이 논문을 쓰지 않는다** — 이 논문은 되돌아옴을 재지 않았고 그런 문장도 없다 (Kollenda 2024 의 인용 [39] 는 원문 근거 없음 · §0-1).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Meyer et al. reduced their exponential calendering model to a single fitting parameter by fixing the minimum coating porosity at a constant fraction of the initial porosity, ε_C = ε_C,0·(p + (1 − p)·exp(−q_L/γ_C)) with p = 0.4; the compaction resistance γ_C was 220–310 N/mm for NCA, NCM111, NCM622 and NCM811 cathodes at 223 g/m² and increased in proportion to the mass loading, γ_C = μ·M_C with μ = 1.31 ± 0.03 kN·m/g between 80 and 285 g/m² (J. Energy Storage 18 (2018) 371–379)."
- "The factor p = 0.4 is an empirical estimate: the authors started from the ratio of the porosities of a cubic close packing and a simple cubic packing of equal spheres (0.54) and lowered it because the achieved minimum porosities were smaller; the model is stated to be limited to spherical active materials and additive contents up to 10 wt% (Meyer et al. 2018, pp. 374, 378)."
- "The line load (rolling force per coating width, N/mm) is not converted into a pressure in that work, and all porosities were determined after calendering from mass loading, thickness and the pycnometric density of the components (Meyer et al. 2018)."
- "Single-particle micro-compression showed breaking strengths decreasing with nickel content for the materials studied, but the authors concluded that the breaking strength is not the dominant factor for the compaction resistance and attributed the differences to interparticle friction during the early rearrangement stage (Meyer et al. 2018, p. 376)."
- 국문: *"압연 선하중 ↔ 압연 뒤 코팅 기공률은 끝값을 압연 전 값의 0.4 배로 둔 지수 식 하나로 적히고 (Meyer 2018 식 (4)), 그 매개변수 'compaction resistance' γ_C 는 면적 부하에 비례한다 (μ = 1.31 ± 0.03 kN·m/g · NCM111 · 80–285 g/m²) — 선하중 축 · 액체 LIB · 압연 뒤 값 · 구형 활물질 · 첨가제 ≤ 10 wt% 한정."*
- 국문 (금지 표지): *"Meyer 2018 을 '충전 이론으로 최소 기공률을 예측했다' 고 쓰지 않는다 (0.4 는 경험값) · '두꺼운 코팅이 덜 되돌아온다' 의 근거로 쓰지 않는다 (되돌아옴 측정 없음) · γ_C (N/mm) · μ (kN·m/g) 를 MPa 값과 나란히 놓지 않는다 · 식 (1) · (5) 는 인쇄 오류 (덧셈표 · 나눗셈표 누락) 를 고쳐 적었음을 밝힌다."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **선하중 ≠ 압력** — 환산 · 접촉 길이 · 하중 아래 간극 · 롤 속도 · 코팅 폭 값 없음 (§3-9).
2. **압연 뒤 값** — 하중 아래 기공률 · 회복 크기 · 측정 시각 없음 · 되돌아옴은 한 문장.
3. **p = 0.4 의 지위** — 충전 구조에서 유도된 값이 아니라 12 전극에 맞춘 경험값 · 그 12 전극은 한 그룹 · 한 코팅 라인 · 구형 NCA / NCM · 압연 전 기공률 0.42–0.48 (하나만 0.55) 이라 '비례' 가정의 시험 폭이 좁다 · 달성 최소 기준으로는 0.447 (§3-4) · 벗어나는 세 전극 (0.29 · 0.33 · 0.60) 은 *"not further discussed"*.
4. **맞춤 품질** — reduced χ² 가 대부분 1 을 넘고 (활물질 다섯 2.2–4.0) 잔차에 무늬가 있다 (§3-5) · 저자는 *"visually sufficiently well for practical purposes"* 로 넘어간다.
5. **γ_C = μ·M_C** — 일곱 점 · 한 활물질 (NCM111) · 한 조성 (90/5/5) · 평균 기준 R² 0.948 · 161 g/m² 점이 21 % 벗어남 · 인쇄 R² 0.996 은 원점 통과 맞춤의 비중심 값 · 활물질 다섯의 μ 는 부하 한 수준에서 **가정으로 옮긴** 값.
6. **기전 설명은 측정이 아니다** — '마찰 면적' · 'US 채움' · '재배열' 은 문헌 인용과 추론 (마찰 · 구조 측정 없음) · 활물질 다섯은 입도 · 표면 · 세기 · 공급사 · 입자 밀도가 함께 다르다 (저자: *"no general validity"*).
7. **기공률 분모** — ρ_ph 값과 평균 식 미인쇄 · 앞 논문의 같은 전극과 값이 달라진 것을 밝히지 않았다 (§3-11) · 수은 압입 기공률 값은 이 논문에 없다 (*"in well corresponce"* 는 인용에 기댄 문장).
8. **재료 정보 부족** — 공급사 · 등급 · 바인더 · 탄소 종류 · 집전체 · 건조 조건 [미확인] → 다른 전극으로 옮길 근거가 약하다.
9. **입자 파괴** — 세기 분포만 있고 압연 뒤 파괴 여부는 속편으로 미룸 · 파괴 세기는 평판 사이 한 입자의 명목 값.
10. **인쇄 어긋남 16 건** (§3-12) — 특히 식 (1) 덧셈표 · 식 (5) 나눗셈표 누락 · 표 2 의 No.1 ↔ 2 · Fig 5 캡션의 'very near to 1' · '20 % lower specific surface' · '12 %'.
11. ⚠ 이 카드의 판독은 래스터라 **[판독]** 표지로만 인용 (불확도 = 머리 주석 · Fig 9 일부 계열은 일부 점) · 코팅 두께 · 접촉 길이 · 평균 압력은 **[카드 추정]** (원문 값 아님) · p 재검 · 잔차 · 재맞춤 · 밀도 되짚기는 **[카드 산술]** · 그 해석은 **[카드 추론]**.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 27 | J. Zhang, A study of compaction of composite particles by multi-particle finite element method, Compos. Sci. Technol. 69 (2009) 2048–2053. | 입자마다 유한요소로 복합 입자 가루를 누른 계산 — '입자 간 마찰이 압축 압력에 크게 영향' 의 출처 (후보 B · k · l) | 없음 |
| 26 | Z.R. Hesabi, H.R. Hafizpour, A. Simchi, An investigation on the compressibility of aluminum/nano-alumina composite powder prepared by blending and mechanical milling, Mater. Sci. Eng. A 454–455 (454–455) (2007) 89–98. | 무른 금속 + 단단한 나노 입자 복합 가루의 압축성 — '초기 치밀화는 재배열이 지배' 의 출처 (d · l · 후보 M0) | 없음 |
| 23 | L. Froboese, P. Titscher, B.G. Westphal, W. Haselrieder, A. Kwade, Mercury intrusion for ion- and conversion-based battery electrodes – structure and diffusion coefficient determination, Mater. Charact. 133 (2017) 102–111. | 기하 ↔ 수은 압입 기공률이 '잘 맞는다' 는 근거 · 수은 압입 절차 (단계 0) — meyer2017 카드의 [미확인] (권 · 쪽) 을 푸는 서지 | 없음 (`froboese2019_*` 은 다른 논문) |
| 24 | G.D. Scott, Radial distribution of the random close packing of equal spheres, Nature 194 (1962) 956–957. | 평평한 면에 닿은 구 충전이 덜 조밀하다는 근거 (얇은 코팅의 높은 기공률 · d) | 없음 (`onoda1990_*` 이 인용한 Scott 1960 Nature 188, 908 과는 다른 논문) |
| 13 | H. Kang, C. Lim, T. Li, Y. Fu, B. Yan, N. Houston, V. De Andrade, F. De Carlo, L. Zhu, Geometric and electrochemical characteristics of LiNi1/3Mn1/3Co1/3O2 electrode with different calendering conditions, Electrochim. Acta 232 (2017) 431–438. | 압연 조건 ↔ NCM111 전극의 기하 · NCM 파쇄 보고 · 최적 코팅 밀도 3.0 g/cm³ (≈35 % · 이 논문의 환산) (조건 R7 · i 근처) | 없음 |
| 12 | H. Bockholt, M. Indrikova, A. Netz, F. Golks, A. Kwade, The interaction of consecutive process steps in the manufacturing of lithium-ion battery electrodes with regard to structural and electrochemical properties, J. Power Sources 325 (2016) 140–151. | 분산 ↔ 압연의 상호작용 · NCM 파쇄 (조건 R7) | 없음 |
| 16 | W.A. Appiah, J. Park, S. Song, S. Byun, M.-H. Ryou, Y.M. Lee, Design optimization of LiNi0.6Co0.2Mn0.2O2/graphite lithium-ion cells based on simulation and experimental data, J. Power Sour. 319 (2016) 147–158. | NCM622 양극의 부하별 최적 기공률 (얇으면 ≈20 % · ≈170 g/m² 에서 ≈30 %) — 이 논문이 닿은 최소 (19–21 %) 의 쓰임새 쪽 기준 | 없음 |
| 15 | W. Haselrieder, S. Ivanov, D.K. Christen, H. Bockholt, A. Kwade, Impact of the calendering process on the interfacial structure and the elated electrochemical performance of secondary lithium-ion batteries, ECS Trans. 50 (2013) 59–70. | 같은 그룹의 앞선 압연 논문 | 없음 |
| 21 | R.W. Heckel, Density-pressure relationships in powder compaction, Trans. Metall. Soc. AIME 221 (1961) 671–675. | Heckel 식 원전 (c · m) — 식 (1) 의 인쇄 오류를 바로잡을 곳 | 없음 (wishlist 에 이미 있음 · batch_104) |
| 11 | C. Schilcher, C. Meyer, A. Kwade, Structural and electrochemical properties of calendered LMO cathodes, Energy Technol. 4 (2016) 1–8. | 전극 No.14 (LMO) 의 출처 · 기공 부피비 3.27 · LMO 파쇄 (조건 R7) | 없음 (wishlist 에 이미 있음 · batch_104) |
| 8 | J. Ott, B. Völker, Y. Gan, R.M. McMeeking, M. Kamlah, A micromechanical model for effective conductivity in granular electrode structures, Acta Mech. Sin. 29 (2013) 682–698. | 입자 구조 저항망 유효 전도 모델 (흐름 밖: 접촉망 σ) | 없음 (wishlist 에 이미 있음 · batch_104) |
| 22 | C. Meyer, H. Bockholt, W. Haselrieder, A. Kwade, Characterization of the calendering process for compaction of electrodes for lithium-ion batteries, J. Mater. Process. Technol. 249 (2017) 172–178. | 앞 논문 — 식 (2) 의 밀도 꼴 · 롤 힘 측정 · 전극 No.13 · 15 | **있음** `meyer2017_calendering_compaction_resistance_line_load_exponential_model` |
- 뒤 논문 (이 논문 밖 · 다른 정본 카드의 참고문헌에서): Meyer C, Weyhe M, Haselrieder W, Kwade A. Heated Calendering of Cathodes for Lithium‐Ion Batteries with Varied Carbon Black and Binder Contents. Energy Tech 2020;8. (`kollenda2024_*` [40] 의 표기 그대로 · `diener2022_*` 참고 17–19 가운데 하나) — 이 논문 전망 (조성 · 롤 온도) 의 후속으로 보인다 [카드 추론 · 원문 미확인].  본문이 예고한 *"The properties of the calendered cathodes will be discussed in a future publication"* (p.376) 의 서지는 [미확인].

---

## [미확인] 목록
- 롤 속도 · 통과 횟수 · 코팅 폭 · 간극 값 (최소 25 µm 말고) · 하중 아래 두께 · 접촉 길이 · 압력 · 온도 수치.
- 탄성 회복의 크기 · 압연 뒤 두께 측정까지의 시간 · 보관 조건.
- 활물질 공급사 · 등급 · 바인더 · 도전 탄소 종류 · 슬러리 · 건조 조건 · 집전체 종류 · 두께 (No.1–12 · 14).
- 성분 고체 밀도 (NCAI · NCAII 말고) · 혼합물 밀도 ρ_ph 의 값과 평균 식 · 앞 논문과 No.13 값이 달라진 이유 (원문에 말 없음).
- Fig 5 · 9 의 점마다 붙은 오차 막대의 정의 · 맞춤 소프트웨어 · 가중 방식 (reduced χ² 에서 미루어 본 것뿐).
- NCA 의 BET · *"20 % lower specific surface"* 의 기준.
- 압연 뒤 입자 파괴 여부 · 속편의 서지.
- Fig 9 의 계열 6 · 7 · 9 · 10 · 11 가운데 겹쳐서 못 읽은 점 · Fig 5 의 낮은 신뢰 두 점.
- GKL 400 의 실제 롤 치수 (이 논문 Ø430 × 465 · 앞 논문 Ø450 × 470 · Diener 2022 카드 Ø465 × 430 mm).
- Kollenda 2024 가 같은 문장에 함께 단 [40] (Meyer 2020 · Energy Technol.) 의 내용 — '두께 ↔ 재배열 · 소성 변형' 이 거기 있는지.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 서지: 지시서 (C. Meyer, M. Kosfeld, W. Haselrieder, A. Kwade · 제목 · Journal of Energy Storage 18 (2018) 371–379 · doi:10.1016/j.est.2018.05.018 · 9 쪽) = 원문 첫 쪽과 같음 · **다른 점 없음**.
- 식 (1)–(5) · 표 1–3: 텍스트 층 + 400 dpi 렌더로 글자 대조 — 식 (1) 의 덧셈표 · 식 (5) 의 나눗셈표 누락 · 표 1 의 빈 칸 (No.6–13) 은 렌더에서 확인한 인쇄 그대로.
- 낱말 전수 검색 (텍스트 층 · 줄 끝 붙임표를 잇고 셈): 'compaction resistance' 28 회 (캡션 포함) · 'Heckel' 6 회 + 참고문헌 1 · 'spring' 0 · 'relax' 1 (*relaxes elastically*) · 'plastic' 1 (*plastic deformability* — Heckel 의 K) · 'pressure' 본문 2 (Heckel 의 P · *compaction pressure* [27]) · 'MPa' 0 (Fig 7 축에만 — 래스터) · 'stress' 1 (*applied stress* — 미세압축) · 'displacement' 1 (*Force-displacement curves* — 미세압축) · 'DEM' · 'discrete' 0 · 'simulation' 본문 0 (참고 [16] 제목 1) · 'finite element' 본문 0 (참고 [27] 제목 1) · 'speed' · 'm/min' 0 · 'rearrangement' 2 · 'friction' 8 · 'breakage' 4 · 'thick' 11 (전부 두께 측정 · 얇은 코팅 · 간극 대비 — 되돌아옴과 이어진 문장 없음).
- 판독 검증: 머리 주석의 일곱 가지 (표 2 ↔ Fig 2 · 0.4 × · 인쇄 계수 0.33 · 0.60 · 0.29 · 표 3 × 223 ↔ Fig 6 · μ 1.310 ↔ 1.31 · 곡선 끝점 ↔ Fig 2 · 1 수 재맞춤 ↔ 인쇄 오차 막대) + 앞 논문 밀도로 되짚은 No.13 · 15 의 최소 기공률 (0.182 · 0.1776 ↔ 판독 0.176 ± 0.006 · 0.178).
- 가리킨 카드 · wishlist: `kim2026_pregranulation_*` L421 (서지 같음) · `kollenda2024_*` L122 · L171 · L334 ([39] 의 문장 근거 없음) · `lu2020_*` L423 (압력 축 없음) · `diener2022_*` L79 · L217 (맞음) · L57 (롤 치수 뒤바뀜) · wishlist L54 (batch_64 줄: i 채움 · b 없음) — 어느 카드 · wishlist 도 고치지 않았다 (`meyer2017_*` 의 관련 카드 절에 한 줄만 더함).
- 정본 중복 확인: papers/ 목록 (528 장) · DOI · 'Kosfeld' · 제목 낱말 grep — 카드 없음 (kim2026 · kollenda2024 · lu2020 · diener2022 · meyer2017 이 인용만) · 끝낼 때 다시 확인.

## 🔗 관련 카드
- **같은 그룹의 앞 논문**: `meyer2017_calendering_compaction_resistance_line_load_exponential_model` (참고 [22] — 3 수 지수 식 (밀도 꼴) · 'compaction resistance' 의 이름 · 롤 힘 측정법 · 전극 No.13 · 15 의 원자료 — 이 논문에서 No.13 의 기공률이 달라졌다 §3-11 · 그 카드의 [미확인] 둘 (Froboese 서지 · NCM 조성) 이 이 논문으로 좁혀진다).
- 이 논문을 가리킨 카드: `kim2026_pregranulation_ptfe_dry_nca_cathode_crack_delithiation` (L421 참고 27 — 후보 표 N-61 의 근거) · `kollenda2024_time_sensitivity_calendered_electrode_springback_storage` (참고 [39] — 원문에 없는 내용의 근거로 인용 · §0-1) · `lu2020_insitu_nanoct_calendering_microstructural_evolution` (참고 12) · `diener2022_roll_gap_springback_calendering` (참고 17–19 · 같은 캘린더 · 롤 간극 직접 측정 · 순간 회복).
- 같은 계열 식 (압력 축 · 황화물): `heck2026_densification_sulfide_se_binder_scalable` (β-Li₃PS₄ · 누른 채 / 뺀 뒤 γ) · `lee2025_heckel_argyrodite_powder_densification_nanoindentation` · `faka2026_particle_size_consolidation_strain_lpscl` · `miss2026_insitu_conductivity_porosity_pressure_compaction`.
- 입자 하나의 파괴 · 압연 중 파괴: `song2025_insitu_ct_dem_cathode_calendering_nominal_stress_breakage` (명목 응력 f_max/d² — 이 논문의 투영 면적 기준과 π/4 배 차이) · `he2026_dem_calendering_inhomogeneity_areal_density`.
- 같은 크기 구의 충전 기준: `onoda1990_random_loose_packing_uniform_spheres_dilatancy_onset` (무작위 느슨 충전 0.555 = 기공률 0.445 — 이 논문이 견준 단순 입방 0.476 대신 놓을 수 있는 기준 · 단 이 논문의 압연 전 고체 분율 0.52–0.58 은 첨가제 포함이고 활물질만은 0.44–0.47) · `mcgeary1961_bimodal_sphere_packing` (크기가 다른 구를 섞은 충전 — NCA-80/20 의 배경).
- 압연 DEM (이런 선하중 ↔ 기공률 자료를 표적으로 삼는 쪽): `sangros2019_dem_calendering_lib_electrode` · `sangros2020_lib_electrode_dem_mech_elec_ionic` · `schreiner2020_dem_calendering_lib` · `ngandjong2021_dem_calendering_digital_twin` · `lyu2025_3d_dem_drying_calendering_lib` · `zhang2026_xct_dem_cathode_calendering_peel_calibration`.
- 입자마다 유한요소 (참고 [27] 과 같은 방법 계열): `demirtas2021_mpfem_hollow_sphere_die_compaction` · `pycompact2025_dem_mpfem_workflow`.
- 같은 그룹의 수은 압입 · 미세구조: `froboese2019_microstructure_ionic_conductivity_assb_electrode` (이 논문 참고 [23] 과는 다른 논문).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

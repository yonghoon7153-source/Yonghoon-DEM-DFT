<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 이 묶음 (후보 표 3 순위 · N-87 · 믹싱 · 정독 136) 에서 꼭 뽑으라고 한 항목.
     본 = kollenda2024_time_sensitivity_calendered_electrode_springback_storage.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표 꼴).
     같은 그룹 · 같은 재료 이웃 = hayakawa2023_dry_coated_composite_particles_conductive_additives_ab_vgcf.md (같은 NCM523 + LiNbO₃ 1 wt% · 같은 Li₆PS₅Cl 0.7 µm · 2.02 mS cm⁻¹ · 같은 360 MPa 이온 차단 셀 — 그 논문 ref [10] = 이 논문) ·
     형식 이웃 = kim2013_mixing_method_dry_wet_ball_mixer_lco_li2s_p2s5_composite_cathode.md (같은 날 · 혼합 방법 비교 · 이 논문의 ref [21]).
     두 필수 절 (§0-1 고른 의도 대조 · §8 자세한 분석) 은 같은 묶음 카드들과 같은 꼴.
     원문 = 출판본 10 쪽 (Advanced Powder Technology 33 (2022) 103705 · 논문 번호 하나 · 쪽 = PDF 쪽 = 인쇄 쪽 1–10) · SI 없음 (본문에 보충 자료 언급 없음).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 — 그림 3 · 5 · 7 · 9 · 11 · 12 · 13 은 **벡터**라서 래스터 눈대중이 아니라
     **PDF 경로 좌표** (막대 사각형 윗변 · 오차 막대 캡 · 표지 원 중심 · 곡선 꼭짓점 → 틀 + 눈금선으로 맞춘 축, 눈금 잔차 ≤ 0.003 단위) 에서 읽었다 (재현 = litdb/figures/<slug>/digitized.csv 162 행) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 추론] = 원문에 말이 없어 카드가 읽은 뜻 · [다른 카드] = 정본의 다른 카드에 적힌 값 (slug 병기) ·
     [우리] = CLAUDE.md 출처 우리 값 · [미확인] = 본문 10 쪽 전수에 없음.  본문은 글자 층 (pdftotext · PyMuPDF) 과 렌더 영상으로 전부 읽었다.
     DEM · MPM · FEM · 입자 계산 · 압밀 모델은 없다 — 실험만 (건식 고전단 혼합 · SEM/EDX · 순 조성 · 레이저 회절 · 이온 차단 셀 EIS · Li–In 반쪽셀). -->
# 수평 고전단 믹서 (칼날 5000 → 25,000 rpm · 팔 100 rpm · 30 min · 30 g) 로 LiNbO₃ 1 wt% 코팅 NCM523 (4.3 µm) 와 Li₆PS₅Cl (0.7 µm) 84 : 16 wt% 를 건식 혼합 — 칼날이 빠를수록 SE 덩어리가 풀려 AM 위에 붙지만 SE 가 장치 벽에 붙어 순 SE 가 12.2 wt% 까지 준다 (SE 의 최대 27 % [카드 산술]) · 360 MPa 압분체 σ_e 6.8 → 3.9 · σ_ion 4.3 → 4.2 × 10⁻⁵ S cm⁻¹ (그대로) · 같은 87.8 : 12.2 에서 막자 · 습식보다 σ_ion 1.9 · 2.4 배 · 2 C 방전 95 vs 38 · 40 mAh g⁻¹ · 1 C 20 사이클 유지 97 · 69 · 92 % — 혼합 지수 · 기공 · 응력 측정 없음 — Hayakawa · Nakamura · Ohsaki · Watano (Adv. Powder Technol. 33, 2022)

> slug `hayakawa2022_high_shear_mixer_dry_mixing_ncm523_lpscl_composite_cathode` · DOI `10.1016/j.apt.2022.103705` · type `experiment (수평 고전단 mixer 건식 혼합 dry process · powder 응집 해쇄 · 칼날 회전수 5000 / 12,500 / 25,000 rpm · 막자 · 습식 대조 · SEM/EDX morphology · 이온빔 단면 microstructure · UV–vis 순 조성 · 레이저 회절 PSD · 360 MPa 이온 차단 셀 EIS impedance σ_e · σ_ion · Li–In 반쪽셀 율속 · Rs/Rct · dQ/dV · 20 사이클 — DEM · MPM · 모델 계산 없음)` · PDF `577427f8-87._Dry_mixing_of_cathode_composite_powder_for_all-solid-state_batteries_using_a_high-shear_mixer.pdf` · digested `2026-11-22` · status ✅
>
> **원제**: *Dry mixing of cathode composite powder for all-solid-state batteries using a high-shear mixer* (p.1 · 제목 끝 별표 각주 = *"This article was submitted for Virtual Special Issue of APT2021: the 8th Asian Particle Technology Symposium"*)
> **저자 · 소속 (p.1)**: Eiji Hayakawa · **Hideya Nakamura\*** · Shuji Ohsaki · Satoru Watano — Department of Chemical Engineering, **Osaka Metropolitan University**, Sakai, Osaka 599-8531, Japan (\* 교신) · *Advanced Powder Technology* **33** (2022) **103705** (Original Research Paper · 10 쪽) · 접수 2022-03-24 · 수정 2022-06-17 · 승인 2022-06-23 · 온라인 2022-07-12 · © 2022 The Society of Powder Technology Japan (Elsevier) · 연구비 NEDO **SOLiD-EV (JPNP18003)** (p.9) · 이해상충 없음 (p.9) · 키워드 *All-solid-state battery · High-shear mixer · Composite cathode · Dry mixing* (p.1).
> **같은 그룹 · 같은 재료 이웃 (링크만)**: [`hayakawa2023_dry_coated_composite_particles_conductive_additives_ab_vgcf`](hayakawa2023_dry_coated_composite_particles_conductive_additives_ab_vgcf.md) (같은 저자 넷 · **같은 AM · SE 로트 규격** · 같은 360 MPa 이온 차단 셀 · 이 논문을 ref [10] 으로 인용 · 충격 블렌딩 코어–셸) · [`nakamura2020_dry_coating_ncm_li3ps4_core_shell`](nakamura2020_dry_coating_ncm_li3ps4_core_shell.md) · [`kawaguchi2017_dry_coating_parametric_na2so4_model_se`](kawaguchi2017_dry_coating_parametric_na2so4_model_se.md) · [`kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps`](kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps.md) (같은 그룹의 건식 코팅 계열 — **이 논문은 이 셋을 인용하지 않는다** · §0-1) · [`kim2013_mixing_method_dry_wet_ball_mixer_lco_li2s_p2s5_composite_cathode`](kim2013_mixing_method_dry_wet_ball_mixer_lco_li2s_p2s5_composite_cathode.md) (이 논문의 ref [21] · 혼합 방법 비교) · [`siroma2016_ac_impedance_tlm_electron_electron_connection_effective_conductivity_assb`](siroma2016_ac_impedance_tlm_electron_electron_connection_effective_conductivity_assb.md) · [`asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity`](asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity.md) (refs [30] · [31] = 이온 차단 셀 두 반원 방법의 원전).
> **판독 원자료**: `litdb/figures/hayakawa2022_high_shear_mixer_dry_mixing_ncm523_lpscl_composite_cathode/digitized.csv` (162 행 — 그림 3 PSD 봉우리 6 · 그림 5 · 9 막대 + 오차 막대 12 · 그림 7a · 11a 곡선 끝 12 · 7c · 7d · 12b · 12c 율속 표지 60 · 11b dQ/dV 봉우리 6 · 13 사이클 60 · 7b · 12a 나이키스트 끝점 6) · 그림 크롭 **57 장** (도구 14 = 그림 13 + 표 1 — **전부 다시 자름** · 손 43 = 패널 23 + 근거 문단 20) — `figures.json`.  **번호 붙은 식 · 인라인 식 없음** (σ 계산식도 인쇄 안 됨) — 식 크롭 0.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: Osaka Metropolitan Univ. (Nakamura 그룹) 가 **수평 고전단 믹서** (DALTON SPMH-02C · 용기 ≈100 ml · 칼날 (chopper) 3500–25,000 rpm · 혼합 팔 (mixing arm) 30–600 rpm · 반대 방향 회전) 에 **LiNbO₃ 1 wt% 코팅 NCM523 (개수 중앙 4.3 µm) + Li₆PS₅Cl (개수 중앙 0.7 µm · 2.02 mS cm⁻¹) 30.0 g (84.0 : 16.0 wt%)** 을 넣고 팔 100 rpm · 30 min 으로 섞으며 **칼날만 5000 → 12,500 → 25,000 rpm** 으로 올리면, AM 크기의 SE 덩어리가 풀리고 (≥ 12,500 rpm) 25,000 rpm 에서는 SE 가 대부분 AM 위에 붙는다 (SEM/EDX 정성) — AM 입도는 그대로다 (깨지지 않음 · 그림 3).  그러나 SE 가 **장치 안벽에 붙어** 순 조성이 86.0 : 14.0 → 86.5 : 13.5 → **87.8 : 12.2 wt%** 로 바뀌고 (투입 SE 의 14.5 · 18.1 · **27.1 %** 손실 [카드 산술 · AM 을 추적자로]), 360 MPa 압분체의 **σ_e 는 6.77 → 4.54 → 3.94 × 10⁻⁵ S cm⁻¹ 로 떨어지고 σ_ion 은 4.28 · 4.90 · 4.25 × 10⁻⁵ 로 그대로** (오차 막대 안) 다 [판독 그림 5].  같은 순 조성 87.8 : 12.2 에서 **막자 혼합 (원문 약어 'MPM' — 우리 MPM 과 다른 뜻) · 습식 혼합 (WM)** 과 비교하면 HSM 의 σ_ion 이 **1.93 · 2.42 배**, σ_e 는 0.71 · 0.76 배 [판독 그림 9 · 카드 산술] · 반쪽셀 **Rs + Rct = 84 vs 126 · 150 Ω** [인쇄 그림 12a 표] · **2 C 방전 94.9 vs 37.8 · 40.4 mAh g⁻¹** [판독] · **1 C 20 사이클 유지 96.8 · 69.0 · 91.4 %** [판독] (본문 97 · 69 · 92 % [인쇄 p.8]).  저자 해석 = '고르게 퍼진 SE → 이온 경로 · AM–SE 계면 ↑ · SE 끼리 합체 ↑' — **혼합 지수 · 기공 · 응력 · 혼합 뒤 SE 입도 · 셀 반복 수는 없다**.

| 우리 질문 (이 묶음 · 믹싱) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 무엇을 (재료 · 조성 · 장치 · 조건) | AM = **NCM523** (Sumitomo Metal Mining) · **LiNbO₃ 1 wt%** 코팅 · 이론 ca. 160 mAh g⁻¹ [28] · 개수 중앙 **4.3 µm** · 소결된 일차 입자의 2 차 입자 (다결정) · SE = **Li₂S–P₂S₅–LiCl (Li₆PS₅Cl argyrodite type · Mitsui Mining & Smelting)** · 이온 **2.02 mS cm⁻¹** · 전자 **< 10⁻¹⁰ S cm⁻¹** (298 K) · 개수 중앙 **0.7 µm** · 받은 그대로 · 탄소 · 바인더 **없음** · 믹서 = **수평 HSM SPMH-02C (DALTON)** · 칼날 3500–25,000 rpm 조절 · 팔 30–600 rpm · 반대 방향 회전 · 유효 용적 ≈100 ml · **30.0 g · 84.0 : 16.0 wt% [29] · 팔 100 rpm · 30 min** · 칼날 **5000 · 12,500 · 25,000 rpm** (rsc-5000 · rsc-12500 · rsc-25000) · Ar 글러브박스 이슬점 **< 193 K** · 혼합 중 온도 · 칼날 지름 · 선속도 · 에너지 [미확인] | [인쇄] p.2 · 표 1 · 그림 2 |
| ② ★ 혼합 정도를 무엇으로 쟀나 | **숫자 지표 없음** — ⓐ SEM/EDX 입자 영상 (×2.00k · ×10.0k · Ni = AM · S = SE · 시야 하나씩) ⓑ 이온빔 단면 SEM (밝은 회색 AM · 어두운 회색 SE · 검정 공극) ⓒ 순 조성 (에탄올에 SE 녹여 원심 13,000 rpm 60 min · 윗물 UV–vis 235 nm) ⓓ SE 제거 뒤 AM 레이저 회절 PSD (SALD2100) · 판정 = 영상 서술 ("almost identical" · "more uniformly dispersed in the order of HSM, MPM, WM") | [인쇄] p.2 · p.4 · p.7 |
| ③ ★ 칼날 회전수 → 구조 | 5000 rpm = AM 만 한 SE 덩어리 · 12,500 rpm = 큰 SE 덩어리 줄고 일부 SE 가 AM 에 붙음 · 25,000 rpm = **SE 대부분이 AM 에 붙음** (p.4 · 그림 4) · AM 덩어리 (소결 2 차 입자) 는 풀리지 않음 · AM PSD 그대로 (봉우리 4.45 µm 칸 · 폭 2.9–7.5 µm [판독 그림 3]) · 단면: rsc-5000 = 공극 훨씬 많음 · ≥ 12,500 rpm = 공극 적고 *"well-percolated ionic path"* (p.4 · 그림 6 · **정량 없음**) | [인쇄] p.4 · [판독] 그림 3 |
| ④ ★ 칼날 회전수 → σ · 셀 | σ_e (10⁻⁵ S cm⁻¹ · ± SD N = 3) **6.77 ± 1.66 → 4.54 ± 0.26 → 3.94 ± 0.60** · σ_ion **4.28 ± 1.03 · 4.90 ± 0.90 · 4.25 ± 0.69** [판독 그림 5] · Rs / Rct (Ω) **101 / 32.0 → 79.3 / 19.6 → 71.0 / 13.0** [인쇄 그림 7b 표] · 0.1 C 방전 129.3 · 143.1 · 141.1 mAh g⁻¹ [판독 그림 7a] · 2 C 방전 71.8 · 87.5 · 94.8 · 2 C 충전 30.3 · 74.2 · 66.4 [판독 그림 7c · d] · 저자 = 25,000 rpm 최적 (내부 저항 최저 · 용량은 12,500 rpm 이 조금 높음) | [판독] 그림 5 · 7 · [인쇄] p.4–6 |
| ⑤ ★ HSM ↔ 막자 ↔ 습식 (같은 87.8 : 12.2) | σ_e / σ_ion (10⁻⁵ S cm⁻¹): **HSM 3.94 / 4.25 · MPM 5.58 / 2.20 · WM 5.15 / 1.76** [판독 그림 9] · Rs / Rct: **71.0 / 13.0 · 105 / 21.0 · 101 / 49.0 Ω** [인쇄 그림 12a 표] · dQ/dV 봉우리 차 **0.059 (HSM) vs 0.077 V (MPM)** · 쿨롱 효율 **99.01 vs 97.35 %** [인쇄 p.7] · 2 C 방전 94.9 · 37.8 · 40.4 · 2 C 충전 66.6 · 11.0 · 5.0 mAh g⁻¹ [판독 그림 12] · 1.0 C 1 → 20 사이클 109.8 → 106.3 · 97.3 → 67.1 · 71.3 → 65.2 [판독 그림 13] | [판독] 그림 9 · 11–13 · [인쇄] p.7–8 |
| ⑥ ★ SE 손실 · AM 손상 · LiNbO₃ 코팅 | 순 SE 16 → 14.0 · 13.5 · 12.2 wt% = *"adhesion of the SE particles to the inner wall of the HSM"* · 회전이 빠를수록 더 (p.4) → 투입 SE 의 **14.5 · 18.1 · 27.1 %** 손실 (30 g 배치에서 SE 4.80 g 가운데 0.70 · 0.87 · 1.30 g [카드 산술 · AM 손실 0 가정]) · AM: 깨지지 않음 (PSD) · LiNbO₃: *"not worn out by mixing of HSM"* — **성능에서 거꾸로 읽은 추정** (p.9 · 표면 분석 없음) | [인쇄] p.4 · p.9 · [카드 산술] |
| ⑦ 압력 · 두께 · 기공 | 이온 차단 셀 = 혼합물 **80 mg · 360 MPa** (가압 시간 [미확인]) · 집전 SUS 막대 Ø10 mm · 반쪽셀 = 혼합물 10 mg + SE 80 mg 을 **360 MPa · 5 min** 일축 성형 → 양극 **ca. 50 µm** · 분리막 **400–500 µm** → Li–In **90 MPa · 5 min** · Ø10 mm · **기공 · 밀도 · 진밀도 숫자 없음** · 어림 (두께 45–55 µm · ρ_NCM523 4.72 [다른 카드] · ρ_LPSCl 1.64 [랩 표준]) **26–40 %** [카드 산술 · §3-5] · ⚠ 분리막 SE 80 mg · Ø10 mm · 400–500 µm 은 겉보기 2.04–2.55 g cm⁻³ 로 진밀도 1.64 [랩 표준] 를 넘는다 = 인쇄값끼리 안 맞음 [카드 산술 · §3-5] · 시험 중 적층압 [미확인] | [인쇄] p.2–3 · [카드 산술] |
| ⑧ 저자 한계 | 한계 절 없음 · 원문이 스스로 적은 혼선 하나: σ_ion 이 회전수와 무관했던 것은 *"the difference in the net SE fraction"* 때문 (p.4 — 분산 ↑ 과 SE 몫 ↓ 가 겹쳤다) | [인쇄] p.4 |
| ⑨ 모델 · DEM | **없음** — 본문에 DEM · simulation · model 0 회 (DEM 인용도 없음) | 원문 낱말 셈 |

⛔ **한정어 (떼지 말 것)**: ① 재료 = **NCM523 + LiNbO₃ 1 wt%** (우리 NCM811 아님) · Li₆PS₅Cl (Mitsui · 0.7 µm · 2.02 mS cm⁻¹) · **탄소 · 바인더 없음** ② 칼날 회전수를 바꾸면 **순 SE 몫도 같이 바뀐다** (14.0 → 12.2 wt%) — 회전수 효과는 'SE 분산 + SE 손실' 의 겹침이다 (σ_ion 이 그 예) ③ 혼합 상태 = **영상 서술뿐** (혼합 지수 · 덩어리 크기 · 피복 · 기공 정량 0 건 · 시야 하나씩) ④ σ = **360 MPa 로 누른 80 mg 압분체의 EIS 두 반원 맞춤** (두께 값 · 맞춤 회로 · 측정 때 압력 [미확인] · N = 3 = 같은 시료 세 번인지 시료 셋인지 [미확인]) ⑤ 반쪽셀 **Rs 는 분리막 (400–500 µm SE) 을 포함** — 차이를 양극 구조로 읽은 것은 저자 해석 ⑥ 셀 = 조건마다 곡선 하나 (반복 · 오차 없음) ⑦ **3.2 절의 HSM = 3.1 절의 rsc-25000 과 같은 자료** (막대 · 곡선 · 표 같음 · 그림 8a = 그림 4c 3 행 영상) ⑧ 압력을 뺀 뒤 두께 · 기공 · 되돌아옴 측정 없음.
⇒ **절대값 전이: 0 건.**  전이되는 것은 **방향 · 비** (같은 조성에서 건식 고전단 혼합이 막자 · 습식보다 σ_ion ×1.9–2.4 · σ_e ×0.7 · 2 C 방전 용량 ×2.3–2.5 · SE 벽 부착 손실이 회전수와 함께 커진다) 와 **실험 꼴** (한 인자 세 수준 + 대조 공정 둘 + 순 조성 측정 + AM PSD + 압분체 σ 쌍 + 반쪽셀) 뿐이다.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-87 의 '왜' 칸)

의도 원문: *"믹싱 — '★ 고전단 믹서 건식 혼합 (오사카 그룹 · Nakamura 계보) — 믹서 실험 설계 직접 선례 후보' (wolf2026) · '고강도 혼합 코팅' (frankenberg2025)"* · 가리킨 카드 = `wolf2026_extruder_vs_batch_mixing_core_shell_dry_sulfide_cathode` **L335** (목록 15) · `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` **L363** (목록 63 · 64).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 측정 조건 |
|---|---|---|
| "고전단 믹서 건식 혼합" | **채움** | p.2 §2.2: *"A horizontal high-shear mixer (HSM, SPMH-02C, DALTON Co.) was employed for the dry mixing of AM and SE"* · 칼날 3500–25,000 rpm · 팔 30–600 rpm · 반대 방향 · ≈100 ml · 30.0 g · 84.0 : 16.0 wt% · 팔 100 rpm · 30 min · 칼날 5000 · 12,500 · 25,000 rpm (표 1) · Ar 이슬점 < 193 K · 용매 없음 · 온도 [미확인] |
| "오사카 그룹" | **채움** | p.1 소속 = Department of Chemical Engineering, Osaka Metropolitan University · 교신 = Hideya Nakamura · 연구비 NEDO SOLiD-EV (p.9 — 같은 그룹 hayakawa2023 · kawaguchi2023 와 같은 과제 [다른 카드]) |
| "Nakamura 계보" | **일부** | 저자 · 재료는 같은 줄기 (hayakawa2023 와 같은 저자 넷 · 같은 NCM523 + LiNbO₃ 1 wt% · 같은 Li₆PS₅Cl 0.7 µm · 2.02 mS cm⁻¹ · 같은 360 MPa 이온 차단 셀 [다른 카드]).  그러나 **원문 참고문헌 35 개에 그룹의 건식 코팅 줄기 (Kawaguchi 2017 · 2018 · Nakamura 2020) 가 없다** — 그룹 논문 인용은 [32] Hayakawa 2022 (*Adv. Powder Technol.* 33, 103470) 하나 (p.10).  서론은 '코어–셸 복합 입자' 와 '고른 혼합물' 을 두 길로 나란히 적고 (p.1) 이 논문을 뒤쪽 (혼합) 에 둔다 — 코팅 계열의 후속으로 자기를 위치시키지 않는다 · 시간 순서: 온라인 2022-07-12 → hayakawa2023 (접수 2022-09-16) 가 이 논문을 ref [10] 으로 인용 [다른 카드] |
| "믹서 실험 설계 직접 선례 후보" | **일부** | 주는 것 = **한 인자 세 수준** (칼날 회전수 5000 · 12,500 · 25,000 rpm · 다른 조건 고정) + **대조 공정 둘** (건식 막자 30 min · 헵테인 초음파 습식) + **평가 사슬** (순 조성 UV–vis → SE 제거 뒤 AM PSD → 입자 SEM/EDX → 이온빔 단면 → 360 MPa 이온 차단 셀 σ_e · σ_ion → 반쪽셀 0.1 C · 율속 · EIS · 20 사이클) · 못 주는 것 = **혼합 지수 (Lacey 류 · 분산 · 덩어리 크기) 0 건** · 칼날 지름 · 선속도 · 투입 에너지 · 분체 온도 · 채움률 (30 g / ≈100 ml = 0.30 g ml⁻¹ 뿐 [카드 산술]) · 시간 계열 · 배치 반복 · 혼합 뒤 SE 입도 · 벽 손실 질량 수지 · **회전수 ↔ 순 SE 몫 교락** (14.0 → 12.2 wt%) |
| "고강도 혼합 코팅" (frankenberg2025) | **일부** | 장치는 고전단 (칼날 25,000 rpm) 건식 혼합이 맞다 · '코팅' 은 원문 주장이 아니다 — 25,000 rpm 에서 *"most of the SE particles adhere to the AM particles"* (p.4 · SEM/EDX ×10k · 정성) · HSM · 막자에서 *"the SE particles are likely to adhere to the AM particles by applying a strong shear force"* (p.7) = **부착** 서술 · 피복률 · 껍질 두께 · 연속성 측정 없음 · 원문에서 'coating' 은 LiNbO₃ 에만 쓰인다 (p.2 · p.9) · 'intensive' 는 참고문헌 [16] 제목에만 |

**가리킨 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `wolf2026_…` **L335** (목록 15) | 서지 *"E. Hayakawa, H. Nakamura, S. Ohsaki, and S. Watano, "Dry Mixing of Cathode Composite Powder for All-Solid-State Batteries Using a High-Shear Mixer," Advanced Powder Technology 33 (2022): 103705."* · *"★ 고전단 믹서 건식 혼합 (오사카 그룹 · Nakamura 계보) — 믹서 실험 설계 직접 선례 후보"* | 서지 ✓ (원제는 문장형 대소문자 · 'a high-shear mixer' · 쪽 = 논문 번호 103705) · 설명 = 위 표 (그룹 ✓ · 계보 일부 · 설계 선례 일부) | **채움** (서지) |
| `frankenberg2025_…` **L363** (목록 63 · 64) | *"E. Hayakawa, H. Nakamura, S. Ohsaki, S. Watano, Adv. Powder Technol. 2022, 33, 103705."* · *"카드 없음 — 고강도 혼합 코팅 (오사카 그룹)"* | [64] 서지 ✓ · '코팅' 은 [63] (= hayakawa2023 · 충격 블렌딩 코어–셸) 과 한 줄로 묶은 설명 — 이 논문은 혼합 (SE 부착 · 정성) | **일부** (설명 · 값 없음) |
| (참고) `hayakawa2023_…` **L313** (ref [10]) | *"Dry mixing of cathode composite powder for all-solid-state batteries using high shear mixer, Adv. Powder Tech. 33 (2022), 103705"* · *"후보 표 N-87 · 카드 없음"* | 서지 ✓ ('a high-shear' ↔ 'high shear' = 인용한 쪽 목록의 표기) · '카드 없음' 은 이 카드가 생기기 전 상태 | — (값 없음) |

⇒ **의도 대조 결과: 일부** — 고전단 믹서 건식 혼합 · 오사카 그룹은 **채움**; 'Nakamura 계보' 는 저자 · 재료로만 이어지고 원문은 그룹 코팅 계열을 인용하지 않는다 (**일부**); '믹서 실험 설계 선례' 는 한 인자 세 수준 + 대조 공정 + 평가 사슬을 주지만 **혼합 지수 · 에너지 · 반복이 없고 회전수 ↔ 순 SE 몫이 교락** (**일부**); '고강도 혼합 코팅' 의 '코팅' 은 원문 주장이 아니다 (SE 부착 · 정성 · **일부**).

---

## 1. 한 줄 요약
황화물 전고체 양극 분말 (AM + SE) 은 대부분 10 µm 아래의 응집성 가루라 고르게 섞기 어렵고, 손 · 막자 혼합은 키울 수 없고 볼 밀링은 너무 세다 — 그래서 제약 · 식품 산업의 **수평 고전단 믹서** (팔이 분체를 들어 올려 가운데로 떨어뜨리고, 가운데의 빠른 칼날이 큰 전단으로 덩어리를 깬다) 를 처음으로 써 본다.  칼날을 빠르게 할수록 SE 덩어리가 풀리고 SE 가 AM 에 붙어 단면의 공극이 줄고 반쪽셀 저항이 내려가며 율속이 좋아진다 (대신 SE 가 벽에 붙어 순 SE 몫이 준다).  25,000 rpm 을 최적으로 골라 같은 순 조성의 막자 · 습식 혼합과 견주면 이온 전도도 · 내부 저항 · 2 C 용량 · 20 사이클 유지가 모두 HSM 쪽이 낫고 전자 전도도만 조금 낮다 (AM 이 부피의 70 % 넘게 차지해 그 손해가 작다는 해석).  결론: HSM 은 **키울 수 있는 건식 혼합이면서 고른 혼합을 주는 방법**이고 *"process-homogeneity-performance"* 관계를 보였다 (p.1 · p.9).

## 2. 메타
| 저자 | 저널 / 년 | DOI | 소재 (SE/CAM) | 연구 유형 |
|---|---|---|---|---|
| E. Hayakawa · **H. Nakamura\*** · S. Ohsaki · S. Watano (Osaka Metropolitan Univ. 화공) | *Advanced Powder Technology* 33 (2022) 103705 · 10 쪽 · APT2021 (8th Asian Particle Technology Symposium) 가상 특집호 투고 | 10.1016/j.apt.2022.103705 | **Li₆PS₅Cl** (Mitsui · 0.7 µm · 2.02 mS cm⁻¹) + **NCM523** (Sumitomo · LiNbO₃ 1 wt% · 4.3 µm) · 탄소 · 바인더 없음 · Li–In 대극 | 실험 (건식 고전단 혼합 + 막자 · 습식 대조 · SEM/EDX · 순 조성 · PSD · 이온 차단 셀 EIS · 반쪽셀 전기화학) — **계산 없음** |

- **1저자 메모 (후보 표) 와의 대조**: 저자 넷 · 학술지 · 권 33 · 논문 번호 103705 · 2022 · DOI — **같다** (PDF 첫 쪽 · 쪽 머리).  다른 점: 원제는 문장형 대소문자 (*"Dry mixing of cathode composite powder for all-solid-state batteries using a high-shear mixer"*) — 후보 표 (wolf2026 목록에서 옮김) 는 낱말마다 대문자 · 덧붙임: 가상 특집호 각주 · 온라인 2022-07-12 · 교신 Nakamura.
- **글의 꼴**: 1 서론 → 2 실험 (2.1 재료 · 2.2 혼합 · 2.3 분석 · 2.4 이온 차단 셀 σ · 2.5 반쪽셀) → 3.1 칼날 회전수 효과 (3.1.1 분말 · 양극 · 3.1.2 반쪽셀) → 3.2 혼합 공정 비교 (3.2.1 · 3.2.2) → 4 결론 → 참고문헌 35.  그림 13 · 표 1 · **번호 식 0** · SI 없음.

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 재료 · 장치 · 혼합 조건 (p.2 · 그림 1 · 2 · `fig_1.png` · `fig_1a.png` · `fig_1b.png` · `fig_2.png` · `txt_p2_materials_lpscl_ncm523_linbo3.png` · `txt_p2_hsm_operation_mortar_wet.png`)
| 항목 | 값 | 표지 · 쪽 |
|---|---|---|
| SE | Li₂S–P₂S₅–LiCl (**Li₆PS₅Cl** argyrodite type) · Mitsui Mining & Smelting · 이온 **2.02 mS cm⁻¹** · 전자 **< 10⁻¹⁰ S cm⁻¹** (298 K · 측정법 [미확인]) · 개수 중앙 **0.7 µm** · 그림 1b = 모난 판 · 덩어리 (눈금 1 µm) | [인쇄] p.2 · [판독 정성] 그림 1b |
| AM | LiNi₀.₅Co₀.₂Mn₀.₃O₂ (**NCM523**) · Sumitomo Metal Mining · **LiNbO₃ 1 wt%** 코팅 · 이론 ca. **160 mAh g⁻¹** [28] · 개수 중앙 **4.3 µm** · *"aggregate in which the primary particles bonded by sintering"* (p.4) · 그림 1a = 수백 nm 일차 입자의 둥근 2 차 입자 (눈금 5 µm) | [인쇄] p.2 · p.4 · [판독 정성] 그림 1a |
| 믹서 | **수평 고전단 믹서 SPMH-02C (DALTON)** · 칼날 (chopper) **3500–25,000 rpm** · 혼합 팔 (mixing arm) **30–600 rpm** · 두 회전자 반대 방향 (칼날 쪽에서 보면 칼날 시계 · 팔 반시계) · 유효 용적 **≈100 ml** · 동작: *"The powder was lifted by the rotating mixing arm and dropped in the center of the vessel. The fallen powder was then highly agitated by the high-speed rotating chopper at the center, resulting in the disintegration of the agglomerates and a uniform powder mixture"* · 그림 2 = 옆모습 (용기 · 팔 · 칼날 축) + 칼날 쪽 앞모습 (삼각 팔 · 네 날 칼날) | [인쇄] p.2 · 그림 2 |
| HSM 조건 | **30.0 g** · AM : SE = **84.0 : 16.0 wt%** [29] · 팔 **100 rpm** · **30 min** · 칼날 **5000 · 12,500 · 25,000 rpm** (rsc-5000 · rsc-12500 · rsc-25000) · 채움 = 30 g / ≈100 ml = **0.30 g ml⁻¹** [카드 산술] · 칼날 지름 · 선속도 · 동력 · 분체 온도 [미확인] | [인쇄] p.2 · 표 1 |
| 막자 (MPM) | 건식 막자 **30 min** · 투입 **87.8 : 12.2 wt%** (= HSM 25,000 rpm 의 순 조성 · p.7) · 손 · 막자 · 사람 수 [미확인] | [인쇄] p.2 · p.7 |
| 습식 (WM) | **헵테인** 에 분산 → 초음파 균질기 (UH-50) → 증발기 (smart evaporator C1) **373 K** → 감압 (*"gauge pressure = −0.9 Pa"* · 인쇄 그대로) **393 K 하룻밤** · 투입 87.8 : 12.2 wt% · 시간 · 초음파 출력 [미확인] | [인쇄] p.2 · p.7 |
| 분위기 | 모든 혼합 = Ar 글러브박스 · 이슬점 **< 193 K** | [인쇄] p.2 |
| 서론의 문제 설정 | *"AMs and sulfide SEs are mostly fine particles smaller than 10 µm, and are classified as cohesive particles with poor flowability [14]"* (p.1) · 볼 밀링 = *"the mechanical energy externally applied by ball milling is too high, causing severe damage to the raw materials"* (p.2) · 칼날 = *"can impose a much higher shear stress on the particles. This leads to powder mixing with the de-agglomeration of fine and cohesive particles [27]"* · 처리 시간 *"within a few minutes"* [26] (p.2 — 그러나 이 실험은 30 min) | [인쇄] p.1–2 · `txt_p1_deformable_se_fine_cohesive_powders.png` · `txt_p2_ball_milling_damage_hsm_chopper.png` |

### 3-2. ★ 순 조성 (표 1) · 벽 부착 손실 (p.4 · `tab_1.png` · `txt_p4_se_wall_adhesion_net_fraction.png`)
| 시료 | 칼날 (rpm) | 순 AM : SE (wt%) [인쇄] | 남은 SE = (SE/AM)_순 ÷ (SE/AM)_투입 [카드 산술] | 30 g 배치 SE 손실 [카드 산술 · AM 손실 0 가정] | 고체 중 SE vol% [카드 산술 · ρ_LPSCl 1.64 · ρ_NCM523 4.72] |
|---|---|---|---|---|---|
| 투입 | — | 84.0 : 16.0 | 100 % | — (SE 4.80 g) | 35.4 % |
| rsc-5000 | 5000 | **86.0 : 14.0** | **85.5 %** | 0.70 g | 31.9 % |
| rsc-12500 | 12,500 | **86.5 : 13.5** | **81.9 %** | 0.87 g | 31.0 % |
| rsc-25000 (= HSM) | 25,000 | **87.8 : 12.2** | **72.9 %** | 1.30 g | **28.6 %** |
- 원인 (저자): *"This was due to the adhesion of the SE particles to the inner wall of the HSM, and the adhesion of the SE particles was more pronounced at higher rotating speeds of the chopper"* (p.4) · 벽에 붙은 양 · AM 손실 · 회수율 측정 없음 [미확인].
- 밀도: ρ_NCM523 **4.72** = [다른 카드: `siroma2016_…` L96–97 · 그 원문의 가정 진밀도] · ρ_LPSCl **1.64** = [랩 표준] — 이 논문에는 진밀도가 없다.
- 견줄 값: 같은 그룹 · 같은 재료의 충격 블렌딩 코팅 (Nara · 13,000 rpm · 5 min) 은 남은 SE **54–63 %** [다른 카드: `hayakawa2023_…` §3-1] — 이 고전단 믹서 (30 min) 쪽이 덜 잃는다 (73–86 %).

### 3-3. AM 입도 · 혼합 상태 (p.4 · p.7 · 그림 3 · 4 · 8 · `fig_3.png` · `fig_4.png` · `fig_4a–c.png` · `fig_8.png` · `fig_8a–c.png` · `txt_p4_am_unbroken_se_deagglomeration_adhesion.png` · `txt_p7_mpm_wm_same_net_fraction_sem_edx.png`)
- **그림 3 (SE 제거 뒤 AM 의 개수 기준 PSD · 0.1–100 µm 로그 축)** [판독 벡터]: 원 NCM 봉우리 **4.45 µm** 칸 19.8 % · rsc-5000 4.45 µm 22.9 % · rsc-12500 **4.00 µm** 칸 19.0 % · rsc-25000 4.45 µm 19.2 % · 빈도 > 0.5 % 구간 2.9–7.5 µm (셋 다 같음) → *"the AM particles were not broken after mixing using the HSM"* (p.4).  ⚠ 혼합 뒤 **SE** 의 입도는 재지 않았다 (SE 는 녹여 없앴다).
- **그림 4 (입자 SEM ×2.00k · EDX S + Ni · SEM ×10.0k · EDX S)**: rsc-5000 = *"agglomerates of SE particles with size equivalent to that of the AM particles"* · rsc-12500 = 큰 SE 덩어리 감소 · 일부 SE 가 AM 에 붙음 · rsc-25000 = *"most of the SE particles adhere to the AM particles"* · *"the higher shear mixing led to deagglomerating the SE particles, whereas the AM aggregates were maintained without their disaggregation"* (p.4).  결론: 탈응집 = **≥ 12,500 rpm** · 부착 = **25,000 rpm** 에서 두드러짐 (p.4).
- **그림 8 (같은 87.8 : 12.2 · 입자 SEM ×10.0k + Ni · S)**: HSM · 막자 = Ni 와 S 위치가 거의 같다 · 습식 = *"the AM and SE particles exist separately"* · *"the SE particles are likely to adhere to the AM particles by applying a strong shear force in the case of HSM and MPM"* (p.7).  ⚠ 그림 8a (HSM) 는 그림 4c 3 행과 **같은 영상**이다 [카드 산술 · 원 래스터 정규 상관 0.93 · 대조 (그림 8b) 0.54].
- 모든 판단은 **시야 하나** · 숫자화 없음.

### 3-4. ★ 360 MPa 압분체 σ_e · σ_ion (p.3–4 · p.7 · 그림 5 · 9 · `fig_5.png` · `fig_9.png` · `txt_p3_ion_blocking_cell_360mpa.png` · `txt_p4_sigma_e_am_contact_sigma_ion_net_se.png` · `txt_p7_conductivity_balance_am_70vol.png`)
- **방법** [인쇄 p.2–3]: 이온 차단 셀 [30,31] = *"only the composite cathode, which was prepared by uniaxial compression of the AM-SE mixture (80 mg) at 360 MPa"* · 스테인리스 막대 두 개 (Ø10 mm) = 집전체 · SP-200 · 10 mV · **1 MHz–10 mHz** · **298 K** · 나이키스트의 **두 반원을 맞춰** 전자 · 이온 저항 [30–32] → *"the thickness of the composite cathode, and the electrode area"* 로 σ · 시료마다 세 번 (평균 ± SD).  두께 값 · 가압 시간 · 측정 때 압력 · 맞춤 회로 [미확인] (같은 밀도라면 80 mg Ø10 mm 는 ≈400 µm [카드 산술 · §3-5 의 2.55 g cm⁻³ 가정]).
- **판독 (벡터 · 막대 윗변 · 오차 막대 캡 · ± = SD · N = 3)**:

| 시료 | 순 조성 | σ_e (10⁻⁵ S cm⁻¹) | σ_ion (10⁻⁵ S cm⁻¹) | σ_e / σ_ion [카드 산술] | f_ion = σ_ion / 2.02 mS cm⁻¹ [카드 산술] |
|---|---|---|---|---|---|
| rsc-5000 | 86.0 : 14.0 | **6.77 ± 1.66** | **4.28 ± 1.03** | 1.58 | 0.021 |
| rsc-12500 | 86.5 : 13.5 | **4.54 ± 0.26** | **4.90 ± 0.90** | 0.93 | 0.024 |
| rsc-25000 = HSM | 87.8 : 12.2 | **3.94 ± 0.60** | **4.25 ± 0.69** | 0.93 | 0.021 |
| MPM (막자) | 87.8 : 12.2 (투입) | **5.58 ± 0.57** | **2.20 ± 0.70** | 2.53 | 0.011 |
| WM (습식) | 87.8 : 12.2 (투입) | **5.15 ± 0.44** | **1.76 ± 0.40** | 2.93 | 0.009 |
- 그림 9 의 HSM 막대 = 그림 5 의 rsc-25000 막대 (값 차 ≤ 0.004 · 같은 자료) [판독].
- 비 [카드 산술]: σ_ion HSM / MPM = **1.93** · HSM / WM = **2.42** · σ_e MPM / HSM = 1.42 · WM / HSM = 1.31 · rsc-5000 / rsc-25000 σ_e = 1.72.
- **저자 해석** [인쇄]: σ_e — *"electrons passed through AM. Thus, electrical conductivity was determined by the contact state between the AM particles"* · 분산된 SE 가 AM 둘레에 놓여 AM–AM 접촉을 줄인다 (p.4) · σ_ion — 분산은 늘었지만 *"the SE fraction of cathode decreased (Table 1). As a result, the ionic conductivity of cathode was unchanged"* (p.4 · 인쇄 문장은 *"was not unchanged"* = 오식) · HSM 의 σ_e 손해가 작은 이유 = *"because the AM particles occupied more than 70% of the volume in cathode in this study"* (p.7).
- ⚠ **'70 % 부피' 검산** [카드 산술 · 같은 두 밀도]: 87.8 : 12.2 의 **고체 중** AM 부피 = **71.4 %** (84 : 16 이면 64.6 %) → 원문의 '70 % 넘게' 는 고체 부피로만 성립한다 · 공극 ≈30 % 를 넣으면 전체 부피 중 AM ≈ 47–50 % [카드 추론 · §3-5].
- 같은 재료 · 같은 셀의 다른 카드 값 [다른 카드: `hayakawa2023_…` §3-3]: 막자 84.0 : 16.0 (SE 더 많음) = σ_ion **3.52** · σ_e **2.84** × 10⁻⁵ S cm⁻¹ → 이 논문의 막자 87.8 : 12.2 = 2.20 · 5.58 — **SE 가 많을수록 σ_ion ↑ · σ_e ↓** 로 방향이 맞다 (두 논문 · 다른 시료).

### 3-5. 단면 미세구조 · 두께 · 기공 어림 (p.3–4 · p.7 · 그림 6 · 10 · `fig_6.png` · `fig_6a–c.png` · `fig_10.png` · `fig_10a–c.png` · `txt_p4_voids_percolated_summary_12500.png`)
- **그림 6 (이온빔 단면 · 눈금 20 µm)**: 밝은 회색 AM · 어두운 회색 SE · 검정 공극 · rsc-5000 = AM–AM 접촉 많고 *"many more voids"* · rsc-12500 · rsc-25000 = SE 가 AM 사이를 채우고 공극 적음 · *"a relatively well-percolated ionic path"* (p.4) — **공극률 · 접촉 수 · 경로 정량 없음**.
- **그림 10 (단면 SEM + EDX S)**: S 신호의 고르기 HSM > 막자 > 습식 (p.7 · 정성) · 막자 · 습식 단면에서 S 가 덩어리로 모인 자리가 보인다 [판독 정성].
- **반쪽셀 양극 두께** *"ca. 50 µm"* (p.3 · 10 mg · Ø10 mm · 360 MPa 5 min 뒤 · 잰 방법 [미확인]) → 면적 하중 **12.73 mg cm⁻²** · 겉보기 밀도 **2.55 g cm⁻³** [카드 산술].
- **기공 어림** [카드 산술 · 가정 셋 = ρ_NCM523 4.72 [다른 카드] · ρ_LPSCl 1.64 [랩 표준] · LiNbO₃ 무시]: 87.8 : 12.2 의 진밀도 3.84 g cm⁻³ → 두께 45 · 50 · 55 µm 에서 기공 **26.3 · 33.7 · 39.7 %** (84 : 16 이면 22.0 · 29.8 · 36.2 %) — 'ca. 50 µm' 의 ±5 µm 가 ±6–7 %p 를 낳는다 ⇒ **기공 값으로 인용하지 않는다** (자릿수 감각만).
- ⚠ **분리막 검산** [카드 산술 · 가정 = ρ_LPSCl 1.64 [랩 표준] · 이 논문 진밀도 없음]: SE **80 mg** / Ø**10 mm** = 101.9 mg cm⁻² · 인쇄 두께 **400–500 µm** (p.3 · *"The thickness of the cathode and separator after compression were ca. 50 and 400–500 µm"* · `txt_p3_halfcell_360mpa_thickness_cycling.png`) → 겉보기 밀도 **2.04–2.55 g cm⁻³** = 진밀도 1.64 보다 크다 (1.64 로 꽉 찬 두께 = 621 µm) ⇒ 인쇄된 **80 mg · Ø10 mm · 400–500 µm 가 서로 맞지 않는다** (SE 진밀도가 2.04 g cm⁻³ 를 넘지 않는 한 · 어느 값이 틀렸는지 [미확인]).  §3-7 의 분리막 저항 검산 (25–32 Ω) 도 이 인쇄 두께를 썼다 — 질량 · 지름이 맞다면 두께 ≥ 621 µm · 분리막 저항 ≥ 39 Ω (σ 2.02 mS cm⁻¹ 상한) [카드 산술].

### 3-6. ★ 반쪽셀 전기화학 (p.3 · p.4–9 · 그림 7 · 11 · 12 · 13 · `fig_7.png` · `fig_7a–d.png` · `fig_11.png` · `fig_11a–b.png` · `fig_12.png` · `fig_12a–c.png` · `fig_13.png` · `txt_p3_halfcell_360mpa_thickness_cycling.png` · `txt_p7_dqdv_peaks_coulomb_efficiency.png` · `txt_p8_rs_compressive_force_coalescence_rate.png` · `txt_p9_cycle_retention_linbo3_not_worn.png`)
- **셀 · 시험** [인쇄 p.3]: AM-SE 혼합물 양극 / SE 분리막 / Li–In · 혼합물 10 mg + SE 80 mg → **360 MPa · 5 min** → 양극 ca. 50 µm · 분리막 400–500 µm → Li–In **90 MPa · 5 min** · Ø10 mm · SUS 막대 집전 · BTS-2004H · CC · 298 K · **0.1 C (1 C = 1.6 mA cm⁻²)** 세 사이클 → 율속 (0.1 · 0.2 · 0.5 · 1.0 · 2.0 C · 다른 쪽은 0.1 C) → EIS (SOC 50 % · 10 mV · **7 MHz–10 mHz**) → **1.0 C 방전 / 0.1 C 충전 20 사이클** · 차단 전압 2.38–3.63 V vs Li–In (**3.0–4.25 V vs Li⁺/Li** · 차 0.62 V [카드 산술]) · 시험 중 적층압 · 셀 수 [미확인].
- ⚠ **1 C 정의** [카드 산술]: 10 mg × 87.8 % × 160 mAh g⁻¹ ÷ 0.785 cm² = **1.79 mA cm⁻²** (84 % 면 1.71) — 인쇄 1.6 mA cm⁻² 은 AM 143–150 mAh g⁻¹ 기준에 해당 · 원문은 1 C 의 기준 용량을 적지 않는다.
- **그림 7a · 11a (0.1 C 충방전 · 끝 용량 [판독 벡터 · 곡선 꼭짓점])**:

| 셀 | 충전 끝 (4.25 V) | 방전 끝 (3.0 V) | 쿨롱 효율 [카드 산술] |
|---|---|---|---|
| rsc-5000 | 130.1 | **129.3** | 99.4 % |
| rsc-12500 | 144.2 | **143.1** | 99.3 % |
| rsc-25000 = HSM | 142.5 | **141.1** | 99.0 % (본문 HSM **99.01 %** [인쇄 p.7]) |
| MPM | 145.5 | **141.8** | 97.5 % (본문 **97.35 %**) |
| WM | 134.5 | **130.9** | 97.3 % (본문 없음) |
- 쿨롱 효율 97–99 % → 그려진 곡선은 **첫 사이클로 보기 어렵다** (같은 재료 · 같은 그룹 hayakawa2023 의 첫 사이클 효율 71–83 % [다른 카드]) · 사이클 번호 [미확인].  본문: HSM · 막자 *"ca. 140 mAh g⁻¹"* · 습식 *"significantly lower"* (p.7).
- **그림 11b (dQ/dV · 0.1 C)**: 본문 충전 봉우리 **MPM 3.760 · HSM 3.772 V** · 방전 봉우리 **HSM 3.713 · MPM 3.683 V** · 봉우리 차 **0.059 (HSM) · 0.077 V (MPM)** [인쇄 p.7].  [판독 벡터]: 방전 봉우리 극값 HSM 3.7131 · MPM 3.6833 · WM 3.6932 V (본문과 같다) · **충전 봉우리는 꼭대기가 평평하고 잡음** — 최대에서 4 % 안의 꼭짓점이 HSM 3.756–3.777 · MPM 3.742–3.760 (3.742 와 3.760 이 같은 최댓값) · WM 3.754–3.778 V ⇒ 본문 값은 그 안에 있지만 **두 봉우리 차의 차 (18 mV) 가 꼭대기 폭 (≈20 mV) 과 같은 크기** [카드 산술].
- **율속 (그림 7c · d · 12b · c)** [판독 벡터 · mAh g⁻¹]:

| 셀 | 방전 0.1 · 0.2 · 0.5 · 1 · 2 C | 충전 0.1 · 0.2 · 0.5 · 1 · 2 C | 2 C / 0.1 C 방전 · 충전 [카드 산술] |
|---|---|---|---|
| rsc-5000 | 129.1 · 120.5 · 106.3 · 92.1 · **71.8** | 128.2 · 123.2 · 109.1 · 87.4 · **30.3** | 55.6 · 23.6 % |
| rsc-12500 | 151.8 · 143.9 · 130.2 · 114.5 · **87.5** | 153.7 · 148.9 · 138.3 · 120.1 · **74.2** | 57.6 · 48.3 % |
| rsc-25000 = HSM | 140.8 · 134.4 · 123.0 · 110.8 · **94.9** | 140.4 · 136.1 · 125.6 · 106.8 · **66.6** | 67.4 · 47.4 % |
| MPM | 138.9 · 132.2 · 119.7 · 96.5 · **37.8** | 143.7 · 134.1 · 117.1 · 78.5 · **11.0** | 27.2 · 7.7 % |
| WM | 128.8 · 117.6 · 100.0 · 77.8 · **40.4** | 128.0 · 119.0 · 92.9 · 49.6 · **5.0** | 31.4 · 3.9 % |
- rsc-25000 (그림 7) 과 HSM (그림 12) 은 같은 셀 자료 (차 ≤ 0.2 mAh g⁻¹) [판독].  ⚠ rsc-12500 의 0.1 C 방전: 그림 7a 143.1 ↔ 그림 7c 151.8 (8.7 차) — 다른 사이클로 보이나 원문 설명 없음 (다른 둘은 0.4 안에서 같다).
- **사이클 (그림 13 · 1.0 C 방전)** [판독 벡터]: HSM 109.8 → 106.3 (**96.8 %**) · MPM 97.3 → 67.1 (**69.0 %**) · WM 71.3 → 65.2 (**91.4 %**) · 본문 MPM *"97 mAh g⁻¹ … 67 mAh g⁻¹ … 69%"* · HSM · WM *"97% and 92%"* [인쇄 p.8] (WM 판독 91.4 ↔ 인쇄 92 %) · MPM 은 14 사이클 뒤 급히 떨어진다.  저자: 용량 감소 = *"a change in the contact state between particles due to the volume change of AM particles during charge/discharge"* · 습식의 높은 유지 = AM 이용률이 낮아 부피 변화가 작아서 (p.8–9) · HSM 은 최고 용량 · 유지 → *"the LiNbO₃ coating layer on AM particle was not worn out by mixing of HSM"* (p.9 · 추정).

### 3-7. EIS — Rs · Rct (p.5–6 · p.8 · 그림 7b · 12a · `txt_p5_eis_assignment_rs_rct.png` · `txt_p6_rs_rct_decrease_optimal_25000.png`)
- **배정** [인쇄 p.5 · 인용 [33,34]]: > 100 kHz = SE 저항 **Rs (양극층 + 분리막)** · 100 kHz–100 Hz 반원 = 양극의 전하 이동 **Rct** · 100 Hz–0.2 Hz = Li–In 의 리튬 확산 (SOC 의존) · 그림에서 Rs = 100 kHz 표지까지의 Z′ · Rct = 100 kHz → 100 Hz 표지 사이 (그림 7b · 12a 화살표) · 맞춤 회로 없음 (그림 위 표지로 읽은 값).
- **값** [인쇄 그림 안 표 · Ω]: rsc-5000 **101 / 32.0** · rsc-12500 **79.3 / 19.6** · rsc-25000 = HSM **71.0 / 13.0** · MPM **105 / 21.0** · WM **101 / 49.0** → Rs + Rct 133 · 98.9 · **84.0** · 126 · 150 Ω [카드 산술] · 면적 곱 (0.785 cm²) Rct 25.1 · 15.4 · 10.2 · 16.5 · 38.5 Ω cm² [카드 산술].
- 나이키스트 첫 점 (가장 높은 주파수) Z′ [판독 벡터]: rsc-5000 73.6 · rsc-12500 64.0 · rsc-25000 58.4 · MPM 83.9 · WM 75.9 Ω — **Rs (71.0) 는 첫 점 (58.4) 이 아니라 100 kHz 표지의 Z′** 다.
- 저자 해석 [인쇄]: Rct ↓ = 고른 SE 분산 · AM 위 SE 부착 → AM–SE 계면 ↑ [35] (p.5) · Rs ↓ = 공극 감소 (p.5) · 공정 비교의 Rs = *"more uniformly dispersed SE particles, which can result in application of more uniform compressive force during electrode preparation and promote coalescence between the SE particles, leading to lower interfacial resistance between SEs"* (p.8 · **응력 · 합체 측정 없음 · 가설**) · Rct 순서 HSM < MPM < WM = 분산 순서 (p.8).
- ⚠ **검산** [카드 산술]: 분리막 SE 400–500 µm 를 σ 2.02 mS cm⁻¹ 로 보면 **25–32 Ω** (Rs 의 ⅓ 안팎) · 이온 차단 셀 σ_ion 으로 50 µm 양극층의 이온 저항을 세면 HSM 150 · MPM 290 · WM 362 Ω — Rs 순서 (HSM 71 < WM 101 < MPM 105) 와 σ_ion 순서 (HSM > MPM > WM) 가 막자 ↔ 습식에서 **어긋난다** · 원문은 두 측정을 잇지 않는다.

### 3-8. 인쇄값끼리 어긋남 · 같은 자료 재사용 (원문 비판 — §11 에 다시)
*"the ionic conductivity was not unchanged"* (p.4 · 뜻은 unchanged) · *"Rct1"* (p.5) · *"gauge pressure = −0.9 Pa"* (p.2) · *"Technolvogy"* (p.9) · 그림 7a ↔ 7c rsc-12500 0.1 C (143.1 ↔ 151.8) · 그림 13 습식 유지 91.4 ↔ 92 % · 막자 효율 97.46 (판독) ↔ 97.35 % (인쇄) · 3.2 절 HSM = 3.1 절 rsc-25000 (그림 5 ↔ 9 · 7 ↔ 11 · 12 · 그림 4c ↔ 8a 영상) · 1 C = 1.6 mA cm⁻² ↔ 160 mAh g⁻¹ 기준 1.79 · 서론 *"within a few minutes"* ↔ 실험 30 min · 분리막 SE 80 mg · Ø10 mm · 400–500 µm ↔ 진밀도 (겉보기 2.04–2.55 > 1.64 [랩 표준] · §3-5).

---

## 4. ★ 방법 — 장치 · 측정 사슬 · 해석

### 4-1. 장치
수평 고전단 믹서 SPMH-02C (DALTON) · 막자 · 초음파 균질기 UH-50 (SMT) · 증발기 smart evaporator C1 (BioChromato) · SEM/EDX SU3500 (Hitachi) · 이온빔 단면 연마기 IM4000 (Hitachi) · 원심 (13,000 rpm) · UV–vis UV-1800 (Shimadzu · 235 nm) · 레이저 회절 SALD2100 (Shimadzu) · 임피던스 SP-200 (Bio-Logic) · 충방전 BTS-2004H (Nagano) · 일축 다이 (지름 10 mm) · Ar 글러브박스 (이슬점 < 193 K) [인쇄 p.2–3].

### 4-2. 측정 사슬 (재구성)
AM + SE 30.0 g (84 : 16) → HSM (팔 100 rpm · 30 min · 칼날 5000 / 12,500 / 25,000) ⟶ ⓐ 일부 → 에탄올 · 원심 → 윗물 UV–vis (순 SE) · 침전 333 K 건조 → 물 분산 → PSD ⓑ 일부 → SEM/EDX 입자 ⓒ 80 mg → 360 MPa → 이온 차단 셀 EIS ×3 → σ_e · σ_ion ⓓ 10 mg + SE 80 mg → 360 MPa 5 min → Li–In 90 MPa 5 min → 0.1 C ×3 → 율속 → EIS (SOC 50 %) → 1.0 C 20 사이클 ⓔ 양극층 단면 (이온빔) → SEM (/EDX) / 25,000 rpm 순 조성 87.8 : 12.2 로 막자 · 습식 혼합물을 만들어 ⓑ–ⓔ 반복.

### 4-3. 해석 (저자 논리)
고전단 (칼날) → SE 탈응집 + SE 의 AM 부착 → ① 양극층의 공극 ↓ · 이온 경로 퍼콜레이션 ↑ (σ_ion 은 SE 손실과 상쇄) ② AM–AM 접촉 ↓ (σ_e ↓) ③ AM–SE 계면 ↑ (Rct ↓) ④ 고른 압축력 → SE 끼리 합체 ↑ (Rs ↓ · 가설) → 율속 · 수명 ↑.  통계 = 평균 ± SD (σ 만) · 유의성 검정 없음 · 맞춘 모델 없음.

### 4-4. ★ 입자 처리 · DEM 한계 · 소성 · 차원 · 탈압
- **(i) DEM 한계 진술 = 말 없음** — 계산을 하지 않고 DEM 을 인용하지도 않는다 (참고문헌 35 개에 입자 모사 0).
- **(ii) 소성 · 큰 변형** = 측정 · 모델 없음.  정성 진술 셋: *"Sulfide SEs are also advantageous over other SEs in terms of the construction of the AM-SE contact interface because of the higher deformability of the SEs even at room temperature [13]"* (p.1) · 강한 전단에서 SE 가 AM 에 붙는다 (p.7) · 고른 분산 → *"more uniform compressive force during electrode preparation and promote coalescence between the SE particles"* (p.8).  단면 SEM (그림 6 · 10) 에서 SE 가 AM 사이를 메운 모습이 보이지만 (정성) 변형량 · 압력 의존 · 경도 · 항복은 없다.  우회 · 맞춘 값 · 계산 비용 = 해당 없음.
- **(iii) 차원**: 2D 영상 (입자 SEM/EDX · 단면 SEM/EDX · 시야 하나씩) 뿐 · 3D 재구성 · 2D → 3D 전이 진술 없음.
- **(iv) 탈압**: 360 MPa (5 min) 로 성형한 뒤 셀로 시험 · 성형 뒤 두께 'ca. 50 µm' 하나 · 되돌아옴 · 탈압 전후 비교 · 시험 중 적층압 없음 [미확인].

### 4-5. 기법 미니 용어집
- **고전단 믹서 (high-shear mixer · HSM)** = 고정 용기 + 느린 혼합 날개 (대류 혼합) + 빠른 칼날 (chopper · 큰 전단 · 덩어리 해쇄) — 제약 습식 과립에 흔한 장치.
- **칼날 (chopper)** = 용기 가운데의 고속 회전자 (여기 최대 25,000 rpm) · **혼합 팔 (mixing arm)** = 분체를 들어 올려 떨어뜨리는 느린 회전자 (30–600 rpm).
- **탈응집 (deagglomeration)** = 입자 덩어리를 낱알로 푸는 것 · **부착 (adhesion)** = SE 낱알이 AM 표면에 붙는 것 (여기선 SEM/EDX 로 본 정성).
- **순 조성 (net weight fraction)** = 혼합 뒤 실제 남은 AM : SE (벽 부착 손실을 뺀 값) · 투입 조성과 다르다.
- **이온 차단 셀 (ion-blocking cell)** = 양극 혼합물만 금속 집전체 사이에 누른 셀 — EIS 의 두 반원에서 전자 · 이온 저항을 함께 얻는다 [30,31].
- **Rs · Rct** = 반쪽셀 EIS 의 고주파 저항 (SE · 양극층 + 분리막) · 중간 주파 반원 (전하 이동).
- **dQ/dV 봉우리 차** = 충전 (산화) · 방전 (환원) 봉우리 전위의 차 — 분극의 지표로 쓰였다.

---

## 5. Figure set ★
| 그림 · 표 | 내용 | 크롭 | 우리 활용 |
|---|---|---|---|
| Fig 1a · b | AM (NCM523 2 차 입자 · 5 µm 눈금) · SE (Li₆PS₅Cl 판 · 덩어리 · 1 µm) SEM | `fig_1.png` · `fig_1a.png` · `fig_1b.png` | 입경 · 형상 출발점 (믹서 · 압밀 초기 침대 크기비 ≈6 : 1 [카드 산술 4.3 / 0.7]) |
| Fig 2 | 수평 HSM 도식 (용기 · 팔 30–600 rpm · 칼날 3500–25,000 rpm · 반대 회전) | `fig_2.png` | 믹서 축 장치 형상 (우리 드럼과 다름) |
| Fig 3 | SE 제거 뒤 AM PSD (원 NCM ↔ 세 회전수) | `fig_3.png` | R7 (AM 파괴 없음 · 25,000 rpm 까지) |
| Fig 4 | 회전수별 입자 SEM/EDX 네 줄 (×2.00k · S+Ni · ×10.0k · S) | `fig_4.png` · `fig_4a.png` · `fig_4b.png` · `fig_4c.png` | ★ 믹서 Ⓒ — SE 덩어리 → AM 부착 (정성) |
| Fig 5 | σ_e · σ_ion 막대 (회전수) | `fig_5.png` | ★ 단계 7 · 결과 전 대조 (분산 ↔ σ 의 방향) |
| Fig 6 | 회전수별 양극층 단면 SEM | `fig_6.png` · `fig_6a.png` · `fig_6b.png` · `fig_6c.png` | 단계 5 · 7 (공극 · 퍼콜레이션 정성) |
| Fig 7 | 회전수별 0.1 C 곡선 · 나이키스트 (+ Rs/Rct 표) · 방전 · 충전 율속 | `fig_7.png` · `fig_7a.png` · `fig_7b.png` · `fig_7c.png` · `fig_7d.png` | 흐름 밖: Rint (Rs/Rct) · 수송 |
| Fig 8 | 공정별 (HSM · 막자 · 습식) 입자 SEM + Ni · S | `fig_8.png` · `fig_8a.png` · `fig_8b.png` · `fig_8c.png` | ★ 믹서 Ⓒ (건식 전단 = 부착 · 습식 = 분리) |
| Fig 9 | 공정별 σ_e · σ_ion 막대 | `fig_9.png` | ★ 결과 전 대조 (같은 조성 · 공정만 다름) |
| Fig 10 | 공정별 단면 SEM + S 지도 | `fig_10.png` · `fig_10a.png` · `fig_10b.png` · `fig_10c.png` | 단계 7 (SE 분포 정성) |
| Fig 11 | 공정별 0.1 C 곡선 · dQ/dV | `fig_11.png` · `fig_11a.png` · `fig_11b.png` | 분극 지표 (잡음 한정) |
| Fig 12 | 공정별 나이키스트 (+ Rs/Rct 표) · 율속 | `fig_12.png` · `fig_12a.png` · `fig_12b.png` · `fig_12c.png` | ★ 2 C 방전 용량 ×2.3–2.5 · Rct ×1.6–3.8 |
| Fig 13 | 공정별 1.0 C 20 사이클 | `fig_13.png` | 수명 (정성 · 셀 하나) |
| 표 1 | 회전수별 순 조성 (투입 84 : 16) | `tab_1.png` | ★ SE 벽 부착 손실 (믹서 DEM 의 상별 보존과 견줄 값) |
| 근거 문단 20 | 초록 · 이력 · 서론 (변형성 · 응집성 · 볼 밀링 · 칼날) · 재료 · 믹서 조건 · 순 조성법 · 이온 차단 셀 · 반쪽셀 · 벽 부착 · AM 무파쇄 · σ 해석 · 공극 · EIS 배정 · 최적 회전수 · 공정 비교 조성 · 70 % 부피 · dQ/dV · 합체 가설 · 수명 · LiNbO₃ | `txt_p1_*` · `txt_p2_*` · `txt_p3_*` · `txt_p4_*` · `txt_p5_*` · `txt_p6_*` · `txt_p7_*` · `txt_p8_*` · `txt_p9_*` | 원문 인용용 |
- 그림 크롭은 도구 관례대로 **캡션 제외** (캡션은 `figures.json`) · 표는 캡션 포함 · 식 크롭 0 (원문에 식 없음) · 전체 쪽 그림 없음.

## 6. Post-processing ★
- **무엇을 (원문)**: σ = 두 반원 맞춤 저항 + 두께 + 면적 (평균 ± SD · N = 3) · Rs · Rct = 주파수 표지 사이 Z′ · dQ/dV 봉우리 전위 · 쿨롱 효율 · 용량 유지 % · 순 조성 = UV–vis 235 nm · PSD = 레이저 회절.
- **안 한 것**: 혼합 지수 · SE 덩어리 크기 분포 · 피복률 · 단면 공극률 · 접촉 수 · 퍼콜레이션 정량 · 두께 측정법 · 등가 회로 맞춤 · 셀 반복 · 유의성 검정 · 혼합 에너지 · 온도.
- **이 카드의 후처리**: 벡터 경로 판독 162 행 (`digitized.csv`) · AM 추적자로 남은 SE · 고체 부피 분율 · 겉보기 밀도와 기공 어림 · 1 C 정의 검산 · 쿨롱 효율 · 2 C / 0.1 C 비 · dQ/dV 꼭대기 폭 · 분리막 · 양극층 이온 저항 어림 · 원 래스터 정규 상관 (그림 4c ↔ 8a).  재현 스크립트 = 작업 스크래치 (`fig7.py` · `curves_rates.py` · `bars_csv.py` · `fig3.py` · `dqdv_detail.py` · `crop.py`) — 값은 csv 와 이 카드에 있다.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md 출처를 병기해 적는다)

### 7-1. 비교표
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 계 | NCM523 + LiNbO₃ 1 wt% (4.3 µm) + Li₆PS₅Cl (0.7 µm) · 87.8 : 12.2 wt% (고체 중 SE 28.6 vol% [카드 산술]) · 탄소 없음 | NCM811 바이모달 (AM_P 다결정 · AM_S 단결정) + LPSCl · real_14 SE / 고체 ≈ 26–27 % [우리 · CLAUDE.md] | SE 부피 몫은 비슷 · AM 종류 · 크기비 (≈6 : 1 ↔ 우리 12 : 4 : 1) · 첨가제가 다르다 |
| 압력 | 360 MPa (성형) · 시험 중 [미확인] | 300 MPa (DEM · MPM 압밀) | 비슷한 자릿수 · 압력별 자료 없음 |
| 혼합 | 수평 고전단 (칼날 5000–25,000 rpm · 30 min) · 막자 · 습식 | 드럼 믹서 DEM (회전 벽 · 층상 캠페인 · Lacey M) [우리] · 압밀 DEM 의 초기 침대 = 무작위 비중첩 삽입 (잘 섞인 쪽 가정) | 장치 · 지표가 다르다 — 이 논문은 지표가 없다 |
| 혼합 → 구조 | SE 덩어리 → 부착 (정성) · 공극 ↓ (정성) | 접촉망 (SE–SE · AM–SE 접촉 · 피복 · 퍼콜레이션) 을 수치로 낸다 | 이 논문은 우리 구조 지표와 숫자로 견줄 칸이 없다 |
| σ_ion · σ_e | 4.25 · 3.94 × 10⁻⁵ S cm⁻¹ (HSM) · f_ion ≈ 0.021 (σ_SE 2.02 mS cm⁻¹ 기준) | DEM 접촉망 Kirchhoff/Holm · STEP3 복셀 FV (CONTACT_FREE 가지) [우리] | 비 (HSM ÷ 막자 1.93 · ÷ 습식 2.42) 만 방향 대조에 쓸 수 있다 |
| 기공 | 숫자 없음 · 어림 26–40 % [카드 산술] | 랩 표준 순수 SE 10–13 % · real_14 DEM 15.6 % [우리] | 대조 불가 (두께 'ca.') |

### 7-2. ★ 랩 기준과 나란히 (판정 없이 · **랩 표준과 다른 문헌 값 = 다른 재료 · 다른 조성**)
| 출처 | 재료 | 상태 | 진밀도 분모 | 기공 |
|---|---|---|---|---|
| **랩 표준** | 순수 LPSCl | 300 MPa | **1.64 g/cm³** (고정) | **10–13 %** |
| 이 논문 반쪽셀 양극 (어림) | NCM523 + LiNbO₃ : Li₆PS₅Cl = 87.8 : 12.2 wt% | 360 MPa 5 min 성형 뒤 (두께 ca. 50 µm) | 3.84 (= 4.72 [다른 카드] · 1.64 [랩 표준] 혼합) [카드 산술] | **26–40 %** (두께 45–55 µm) [카드 산술] — 인용 금지 · 자릿수만 |
| 이 논문 순수 SE | — | — | — | **없음** |
- 이 표는 **"랩 표준과 다른 문헌 값"** 의 자리다 — 이 논문은 기공을 재지 않았고 순수 SE 자료가 없다.

### 7-3. ★ 18 배 연화 · 접촉망 해석과 견줄 자리 (frame [2] · [5])
- 우리 DEM 은 E_SE 24 → E_eff **1.35 GPa** (18 배 연화) · 순수 SE Heckel **P_y 138 MPa** 로 가압 기공을 맞춘 단단한 구 모델 · MPM 은 **E 1.53 GPa · σ_y 0.30 GPa · ν 0.49** [우리] — 이 논문은 어느 값도 검증 · 반증하지 않는다 (기계 측정 0).
- 이 논문이 우리에게 주는 해석 하나 [카드 추론]: **같은 조성 · 같은 압력에서 혼합 상태만으로 σ_ion 이 ×1.9–2.4 · σ_e 가 ×0.7 로 갈린다** → 우리 압밀 DEM 의 초기 침대 (무작위 삽입 = 고른 혼합 가정) 는 '막자 · 습식' 쪽 (SE 덩어리 · 분리) 상태를 원리적으로 못 낸다 · 혼합 이력을 등록하지 않은 σ 대조는 이 배수만큼 흔들릴 수 있다.
- 저자의 *"uniform compressive force … coalescence between the SE particles"* (p.8) 는 우리 접촉망의 **SE–SE 접촉 면적 · Holm 협착** 과 같은 자리의 가설이다 — 그러나 응력 · 합체를 잰 자료가 없다 → 가설로만.

### 7-4. ★ 믹서 축 (우리 드럼 DEM · Lacey M · 논지) 과 견줄 자리
- **SE 벽 부착 손실**: 칼날이 빠를수록 투입 SE 의 14.5 → 27.1 % 가 벽에 붙었다 [카드 산술] — 우리 믹서 DEM 은 상별 유지 부피 · 벽 점착 (CED) 을 따로 다룬다 [우리 · CLAUDE.md 믹서 행] → '벽에 붙어 빠지는 SE 몫' 을 결과 전 대조 항목 (방향 · 자릿수) 으로 둘 수 있다 (장치 · 재료가 달라 값 전이 없음).
- **혼합 지수 부재**: 우리 판정 지표 (Lacey M · 3D 칸) 와 수치 대조 불가 — 이 논문의 '고른 정도' 는 SEM/EDX 시야 하나의 서술.
- **논지 (SE–SE 응집 ↔ SE→AM 부착 · `docs/hetero_thesis.md` §2)** [카드 추론]: 받은 그대로의 SE 는 AM 크기의 덩어리로 있고 (rsc-5000) 큰 전단에서 풀린 뒤 AM 에 붙는다 (rsc-25000 · 막자) · 습식에서는 따로 있다 — **방향은 'SE 응집은 에너지로 깨지고, 깨진 SE 는 AM 에 붙는다'** 와 어긋나지 않지만, AM 이 **LiNbO₃ 코팅** NCM523 이고 비코팅 대조가 없으며 γ · 부착력이 0 건이라 **판가름 수 (γ_A/γ_S < 0.31) 를 주지 않는다**.
- **코팅 활물질 (Ⓒ)**: 이 논문의 AM 은 코팅 (LiNbO₃) 된 활물질이다 — 25,000 rpm 에서도 코팅이 닳지 않았다는 말은 **성능에서 거꾸로 읽은 추정** (표면 분석 · XPS 없음) · 코팅 유무 대조 없음.
- 견줄 다른 정본 카드 (같은 축): `frankenberg2024_dem_high_intensity_mixer_assb` (고강도 믹서 DEM · 응력 모델) · `wolf2026_extruder_vs_batch_mixing_core_shell_dry_sulfide_cathode` (배치 메카노퓨전 ↔ 압출 · 크기별 피복) · `kissel2025_cathode_mixing_quality_cam_utilization_reproducibility_press_cells` (혼합 질 = 셀 간 흩어짐) · `otani2025_dem_se_dispersion_aggregation_compression` (SE 분산 · 응집 DEM) · `kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage` (기계 혼합 · 피복) · `lee2024_shear_force_dry_process_cathode_coverage` (건식 전단 · 피복).

### 7-5. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 공정 (회전수 · 장치) → 분말 상태 (정성) → 같은 압력 압분체 σ_e · σ_ion 쌍 → 셀 성능의 **한 사슬** · SE 벽 손실의 실측 · AM 무파쇄의 실측 (PSD).
- **없는 것**: 미세구조 정량 · 압력 축 · 기계 물성 · 계산.  ⇒ DEM (수송) 쪽에는 '혼합 상태가 σ 를 ×2 흔든다' 는 **방향 대조 표적**, MPM (역학) 쪽에는 줄 것이 없다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ 반면교사 둘 — ① σ 를 두께로 냈다면서 이온 차단 셀 두께를 적지 않았고 반쪽셀 두께는 'ca. 50 µm' 하나 → 우리 결과 전 대조 항목에 **두께 · 진밀도 · 기공을 같이 적지 않은 문헌 σ 는 기공 축에 놓지 않는다** ② '투입' ↔ '순' 조성이 다르다 (SE 최대 27 % 손실) → 대조 문헌의 조성 칸은 **순 조성 (측정법 병기)** 으로 | 순수 SE · 압력별 기공 · 진밀도 |
| **단계 1 · 2 · 3** | 없음 (계산 없음) | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 없음 — 순수 SE 자료 없음 · 서론의 *"higher deformability … even at room temperature [13]"* 는 정성 | 값 0 |
| **단계 5** (3D 복합 압밀) | 출발 상태 경고: 같은 조성에서 SE 가 **AM 크기 덩어리** (rsc-5000) ↔ **AM 위에 붙은 낱알** (25,000 rpm) 로 다르면 360 MPa 뒤 단면 공극이 달랐다 (정성 · 그림 6) → 초기 침대 (무작위 삽입) 의 '혼합 상태' 를 등록 항목으로 · 크기비 출발점 4.3 / 0.7 µm (≈6 : 1) | 기공 숫자 · 압력 축 없음 |
| **단계 6** (탈압 · 되돌아옴) | 없음 — 성형 뒤 두께 하나 · 되돌아옴 측정 없음 | — |
| **단계 7** (형상 · 피복 · 수송) | ★ **같은 조성 · 같은 360 MPa 에서 혼합만으로 σ_ion ×1.93 (HSM ÷ 막자) · ×2.42 (÷ 습식) · σ_e ×0.71 · ×0.76** [판독 · 카드 산술] · 회전수 축에서는 σ_e 6.77 → 3.94 (AM–AM 접촉 감소 해석) · σ_ion 그대로 (SE 손실 상쇄) → 접촉망 수송 계산의 **방향 대조 표적** (분산 ↑ → SE 경로 ↑ · AM–AM 경로 ↓) | 미세구조 정량 · 피복률 없음 · N = 3 의 정체 [미확인] |
| **후보 D0** (지금 DEM) | 직접 없음 — 초기 침대가 '고른 혼합' 하나라는 정성 경고 (§7-3) | DEM 한계 진술 없음 |
| **후보 A′-0 · A · A′** (MPM 접촉 · 강체 AM · 입자별 속도장) | 없음 | — |
| **후보 B** (입자별 FE) | 없음 | — |
| **후보 C · C′** (MDR · 항복 캡 DEM) | 없음 | 접촉 · 항복 값 없음 |
| **후보 M0** (균질화 압밀 · Heckel · 캡) | 없음 (압력 한 값) | P_y 를 정할 수 없다 |
| **U0–U6** | 없음 | — |
| **R1** (AM 이 움직이고 하중을 나눔) | 없음 | — |
| **R3** (SE 입자 경계 기억) | 저자 가설 *"coalescence between the SE particles"* (p.8) = SE–SE 경계가 압축에서 사라지면 Rs ↓ — 가설 · 측정 없음 | 정량 없음 |
| **R6** (SE 형상 변형) | 정성 — 단면에서 SE 가 AM 사이를 메움 (그림 6 · 10) · 서론의 변형성 문장 [13] | 변형량 · 압력 의존 없음 |
| **R7** (AM 파괴) | ★ 25,000 rpm 혼합에서도 **AM PSD 그대로** (봉우리 4.45 µm 칸 · 폭 2.9–7.5 µm [판독 그림 3]) · 볼 밀링은 *"severe damage"* (서론 · 인용) | 압밀 (360 MPa) 뒤 파괴는 보지 않았다 · 소결 2 차 입자 |
| **R2 · R4 · R5** | 없음 | — |
| **결과 전 대조 항목** | (흐름 밖 표지로만) 같은 조성 · 같은 압력에서 공정만 다른 σ 쌍 (HSM ↔ 막자 ↔ 습식) · Rs/Rct 표 · 2 C 용량 · SE 벽 손실 % — '고전단 건식 · NCM523 + LiNbO₃ · 탄소 없음 · 360 MPa' 표지 필수 | 절대값 대조 금지 |
| **흐름 밖: 믹서 Ⓒ** | ★ 한 인자 (칼날 회전수) 세 수준 + 대조 공정 둘 + 순 조성 측정 + AM PSD + σ 쌍 + 셀의 **실험 꼴** · SE 벽 부착 손실 (14.5–27.1 %) · 탈응집 문턱 (≥ 12,500 rpm) · 부착 (25,000 rpm) — 정성 · 이 장치 · 이 재료 | 혼합 지수 · 에너지 · 반복 · 칼날 지름 없음 · 회전수 ↔ 순 SE 교락 |
| **흐름 밖: Rint · EIS** | Rs (분리막 포함) · Rct 의 공정 의존 (Rct ×1.6 · ×3.8 · HSM 기준) · 배정은 인용 [33,34] | 맞춤 회로 없음 · Rs 의 분리막 몫 미분리 |

- **재료 · 차원 · 조건 차이**: NCM523 + LiNbO₃ ↔ 우리 NCM811 · 탄소 없음 ↔ 우리 VGCF · PTFE (SDCP 계) · 360 ↔ 300 MPa · 2D 영상 ↔ 우리 3D 계산 · 고전단 믹서 ↔ 우리 드럼 DEM · 셀 하나 ↔ 우리 시드 앙상블.

## 9. 적용 인사이트 (내 연구에 어떻게)
1. **혼합 이력을 σ 대조의 칸으로 둔다** — 같은 조성 · 같은 압력에서 공정만으로 σ_ion 이 ×1.9–2.4 갈렸다 (그림 9).  문헌 σ 를 우리 접촉망 결과 옆에 놓을 때 장치 · 시간 · 회전수 · 용매를 결과 전에 적고, 혼합이 다른 값을 한 선에 놓지 않는다 (같은 날 `kim2013_…` 의 ×1.86 용량 차와 같은 방향).
2. **'투입' 이 아니라 '순' 조성** — 고전단일수록 SE 가 벽에 붙어 최대 27 % 가 빠졌다 (표 1 · 카드 산술).  우리 믹서 DEM 결과를 압밀 · 수송으로 넘길 때 상별 유지 부피를 함께 넘기고, 문헌 조성은 측정된 순 조성인지 확인한다.
3. **회전수 효과는 교락을 품는다** — 칼날을 올리면 분산 ↑ 와 SE 몫 ↓ 가 같이 와서 σ_ion 이 평평했다 (p.4).  우리 믹서 · 압밀 사슬의 공정 비교 등록은 SE 몫을 고정한 쌍 (이 논문의 3.2 절 꼴) 을 따로 둔다.
4. **dQ/dV 봉우리 차로 공정을 가를 때는 꼭대기 폭을 같이 적는다** — 충전 봉우리 꼭대기가 ≈20 mV 로 평평해 HSM ↔ 막자 봉우리 차의 차 (18 mV) 와 같은 크기였다 [카드 산술].
5. **같은 자료 재사용을 확인한다** — 3.2 절 HSM = 3.1 절 rsc-25000 (막대 · 곡선 · 표 · 영상) → 이 논문의 HSM 대 rsc 비교는 독립 반복이 아니다.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Dry mixing of LiNbO₃-coated NCM523 (4.3 µm) with Li₆PS₅Cl (0.7 µm) in a horizontal high-shear mixer at chopper speeds of 5000–25,000 rpm deagglomerated the electrolyte and made it adhere to the cathode particles without breaking them, but electrolyte adhesion to the mixer wall lowered the net electrolyte fraction from 16 to 12.2 wt% (Hayakawa et al., *Adv. Powder Technol.* 33 (2022) 103705)."
- "At the same net composition (87.8 : 12.2 wt%) and compaction pressure (360 MPa), high-shear mixing gave an ionic conductivity of ≈4.2 × 10⁻⁵ S cm⁻¹, about twice that of dry mortar–pestle and wet mixing (≈2.2 and 1.8 × 10⁻⁵ S cm⁻¹, values read from Fig. 9), with a slightly lower electronic conductivity (Hayakawa et al. 2022)."
- 국문: *"건식 고전단 혼합은 같은 조성 · 같은 압력에서 막자 · 습식보다 압분체 이온 전도도를 약 2 배로 올렸고 (그림 9 판독), 칼날을 빠르게 할수록 SE 가 벽에 붙어 순 SE 몫이 16 → 12.2 wt% 로 줄었다 (Hayakawa 2022 · NCM523 + LiNbO₃ · 탄소 없음 · 360 MPa)."*
- 국문 (금지 표지): *"Hayakawa 2022 를 '고전단 혼합으로 SE 코팅 (껍질) 을 만들었다' 의 근거로 인용하지 않는다 — 원문은 SEM/EDX 로 본 부착 (정성) 이고 피복 · 껍질 정량이 없다."*

## 11. 주의/한계 (over-claim 방지 · 원문 비판)
1. **혼합 지수 · 미세구조 정량 0 건** — '고르다' 는 SEM/EDX 시야 하나의 서술.
2. **회전수 ↔ 순 SE 몫 교락** — 14.0 → 12.2 wt% (원문도 σ_ion 해석에서 인정 · p.4).
3. **벽 부착 손실의 질량 수지 없음** — '남은 SE 72.9 %' 는 AM 손실 0 가정의 [카드 산술].
4. **σ 측정 조건 일부 미기재** — 이온 차단 셀 두께 · 가압 시간 · 측정 때 압력 · 맞춤 회로 · N = 3 의 정체.
5. **Rs 는 분리막 포함** — 공정 차이를 양극 구조로 읽은 것은 저자 해석 · Rs 순서 (막자 105 > 습식 101) ↔ σ_ion 순서 (막자 > 습식) 어긋남 [카드 산술 · §3-7].
6. **셀 반복 없음** — 조건마다 곡선 하나 · 3.2 절 HSM 은 3.1 절 rsc-25000 과 같은 자료 (§3-8).
7. **기공 · 밀도 · 진밀도 없음** — 두께 'ca. 50 µm' 하나 → 기공 어림 26–40 % 는 인용 금지 · 분리막 인쇄값 (SE 80 mg · Ø10 mm · 400–500 µm) 은 겉보기 2.04–2.55 g cm⁻³ 로 진밀도 1.64 [랩 표준] 를 넘는다 → 두께 · 질량 · 지름 가운데 하나가 틀렸다 [카드 산술 · §3-5] · 이 두께를 쓴 분리막 저항 검산 (§3-7) 도 그만큼 흔들린다.
8. **'70 % 부피'** — 고체 부피 기준일 때만 성립 [카드 산술 · 71.4 %].
9. **1 C = 1.6 mA cm⁻²** — 160 mAh g⁻¹ × 10 mg × 87.8 % 면 1.79 · 기준 미기재.
10. **0.1 C 곡선의 사이클 번호 미기재** — 쿨롱 효율 97–99 % 라 첫 사이클로 보기 어렵다.
11. **dQ/dV 충전 봉우리 꼭대기 평평 · 잡음** — 봉우리 차의 차 18 mV ≈ 꼭대기 폭.
12. **그림 7a ↔ 7c** rsc-12500 0.1 C 방전 143.1 ↔ 151.8 (설명 없음) · 그림 13 습식 91.4 ↔ 본문 92 %.
13. **LiNbO₃ '닳지 않음'** — 성능에서 거꾸로 읽은 추정 · 표면 분석 없음 · 비코팅 대조 없음.
14. **합체 가설** (*"uniform compressive force … coalescence"*) — 응력 · 합체 측정 없음.
15. 표기: *"was not unchanged"* · *"Rct1"* · *"−0.9 Pa"* (게이지) · *"Technolvogy"* · 서론 *"within a few minutes"* ↔ 실험 30 min.
16. ⚠ 이 카드의 판독은 벡터 좌표라 정확하지만 그래도 **[판독]** 표지로만 인용 · 부피 분율 · 기공 · 손실은 **[카드 산술] (가정 병기)**.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| # | 서지 (원문 그대로) | 왜 | 정본 카드 |
|---|---|---|---|
| 32 | E. Hayakawa, H. Nakamura, S. Ohsaki, S. Watano, Characterization of solid-electrolyte/active-material composite particles with different surface morphologies for all-solid-state batteries, Adv. Powder Technol. 33 (2022) 103470. | 같은 그룹 · 같은 해 · 같은 재료 — 방전 성능이 AM–SE 계면에 주로 달렸다는 근거 · σ 방법 [30–32] 의 하나 | 없음 (wishlist 에 이미 있음 · batch_130) |
| 27 | T.M. Chitu, D. Oulahna, M. Hemati, Wet granulation in laboratory-scale high shear mixers: Effect of chopper presence, design and impeller speed, Powder Technol. 206 (2011) 34–43. | 칼날 (chopper) 이 전단 · 탈응집을 맡는다는 근거 — 믹서 실험 설계 | 없음 |
| 13 | A. Sakuda, A. Hayashi, M. Tatsumisago, Recent progress on interface formation in all-solid-state batteries, Curr. Opin. Electrochem. 6 (1) (2017) 108–114. | "황화물 SE 는 상온에서도 변형성이 높다" 의 출처 (c · l) | 없음 (`ohashi2021_…` 가 인용만) |
| 14 | D. Geldart, types of gas fluidization, Powder Technol. 7 (5) (1973) 285–292. | < 10 µm 응집성 분체 분류 (유동성 · Bond 수 축) | 없음 (`geldart2006_…` 은 다른 논문) |
| 16 | H. Bockholt, W. Haselrieder, A. Kwade, Intensive Dry and Wet Mixing Influencing the Structural and Electrochemical Properties of Secondary Lithium-Ion Battery Cathodes, ECS Trans. 50 (26) (2013) 25–35. | 건식 ↔ 습식 고강도 혼합 (액체 LIB) — 믹서 축 | 없음 |
| 21 | J. Kim, M. Eom, S. Noh, D. Shin, Effect of mixing method on the properties of composite cathodes for all-solid-state lithium batteries using Li2S–P2S5 solid electrolytes, J. Power Sources 244 (2013) 476–481. | 혼합 방법 비교 선례 | `kim2013_mixing_method_dry_wet_ball_mixer_lco_li2s_p2s5_composite_cathode` |
| 19 | Y.J. Nam, D.Y. Oh, S.H. Jung, Y.S. Jung, Toward practical all-solid-state lithium-ion batteries with high energy density and safety: comparative study for electrodes fabricated by dry- and slurry-mixing processes, J. Power Sources 375 (2018) 93–101. | 건식 ↔ 슬러리 혼합 | `nam2018_dry_vs_slurry_mixed_electrode_binder_coverage_premixing_pouch` |
| 30 · 31 | Z. Siroma … J. Power Sources 316 (2016) 215–223 · T. Asano … J. Electrochem. Soc. 164 (14) (2017) A3960–A3963. | 이온 차단 셀 두 반원 방법 | `siroma2016_…` · `asano2017_…` |
| 33 | A. Sakuda, H. Kitaura, A. Hayashi, K. Tadanaga, M. Tatsumisago, Modification of Interface Between LiCoO2 Electrode and Li2S – P2S5 Solid Electrolyte Using Li2O – SiO2 Glassy Layers, J. Electrochem. Soc. 156 (2009) A27–A32. | EIS 배정 (Rs · Rct · Li–In) 의 출처 | 없음 (wishlist 에 이미 있음) |
| 35 | A. Sakuda, A. Hayashi, T. Ohtomo, S. Hama, M. Tatsumisago, All-solid-state lithium secondary batteries using LiCoO2 particles with pulsed laser deposition coatings of Li2S–P2S5 solid electrolytes, J. Power Sources 196 (16) (2011) 6735–6741. | 계면 ↑ → Rct ↓ 의 근거 | `sakuda2011_pld_sulfide_se_coated_licoo2_composite_cathode` |
| 8 · 11 | Kamaya 2011 (Nat. Mater. 10) · Kato 2016 (Nat. Energy 1) | 서론 배경 (SE 전도도) | `kamaya2011_…` · `kato2016_…` |

---

## [미확인] 목록
- 칼날 지름 · 선속도 (끝 속도) · 혼합 동력 · 투입 에너지 · 분체 온도 · 채움률 (부피) · 혼합 중 분위기 압력.
- 혼합 뒤 SE 입도 · SE 덩어리 크기 분포 · 혼합 지수 · 피복률.
- 벽에 붙은 SE 질량 · AM 손실 · 회수율 · 막자 · 습식 혼합물의 순 조성 (투입 87.8 : 12.2 만).
- 이온 차단 셀 두께 · 가압 시간 · 측정 때 압력 · 맞춤 회로 · N = 3 이 시료 셋인지 측정 셋인지.
- 반쪽셀 두께 측정법 · 기공 · 밀도 · 진밀도 · 시험 중 적층압 · 셀 수 · 분리막 SE 80 mg · Ø10 mm · 400–500 µm 가운데 어느 값이 틀렸는지 (겉보기 2.04–2.55 > 진밀도 1.64 [랩 표준] · §3-5).
- 0.1 C 곡선 (그림 7a · 11a) 의 사이클 번호 · 1 C 기준 용량.
- LiNbO₃ 코팅의 혼합 뒤 상태 (표면 분석 없음).
- 막자 혼합의 손 · 사람 · 막자 크기 · 습식의 초음파 출력 · 시간.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-22)
- 서지: 후보 표 메모 (E. Hayakawa, H. Nakamura, S. Ohsaki, S. Watano · Advanced Powder Technology 33 (2022): 103705) = 원문 첫 쪽 · 쪽 머리와 같음 · DOI `10.1016/j.apt.2022.103705` = 첫 쪽 아래 인쇄 · 다른 점 = 제목 대소문자 (원문 문장형) · 특집호 각주 · 날짜 (접수 2022-03-24 · 수정 06-17 · 승인 06-23 · 온라인 07-12).
- 숫자: 글자 층 + 렌더 영상으로 대조 — 2.02 mS cm⁻¹ · 10⁻¹⁰ S cm⁻¹ · 298 K · 1 wt% · 160 mAh g⁻¹ · 4.3 · 0.7 µm · 3500–25,000 · 30–600 rpm · 100 ml · 30.0 g · 84.0 : 16.0 · 100 rpm · 30 min · 373 · 393 K · −0.9 Pa · < 193 K · 13,000 rpm · 60 min · 235 nm · 333 K · 80 mg · 360 MPa · 10 mm · 10 mV · 1 MHz · 10 mHz · 10 · 80 mg · 5 min · 50 · 400–500 µm · 90 MPa · 0.1 C · 1.6 mA cm⁻² · 0.1–2.0 C · 2.38–3.63 · 3.0–4.25 V · 50 % · 7 MHz · 20 사이클 · 1.0 C · 표 1 (5000 · 12,500 · 25,000 · 86.0 : 14.0 · 86.5 : 13.5 · 87.8 : 12.2) · > 100 kHz · 100 kHz–100 Hz · 100 Hz–0.2 Hz · 그림 7b 표 (101 / 32.0 · 79.3 / 19.6 · 71.0 / 13.0) · 87.8 : 12.2 · 70 % · ca. 140 · 3.760 · 3.772 · 3.713 · 3.683 · 0.059 · 0.077 V · 99.01 · 97.35 % · 그림 12a 표 (71.0 / 13.0 · 105 / 21.0 · 101 / 49.0) · 97 · 67 mAh g⁻¹ · 69 · 97 · 92 % · JPNP18003 — 전부 위치 확인.
- 판독: 그림 3 · 5 · 7 · 9 · 11 · 12 · 13 의 경로 좌표를 틀 + 눈금선 (값 = 눈금 글자) 으로 맞춤 — 막대 그림 눈금 잔차 ≤ 0.002 단위 · 인쇄 끝값과 대조: 그림 11a 쿨롱 효율 99.02 % (인쇄 99.01) · 97.46 (인쇄 97.35) · 방전 봉우리 3.7131 · 3.6833 V (인쇄 3.713 · 3.683) · 그림 13 MPM 97.3 → 67.1 (인쇄 97 → 67 · 69 %) · 그림 5 ↔ 9 HSM 막대 · 그림 7 ↔ 11 · 12 HSM 곡선 같음.
- 원 래스터 상관 (같은 영상 확인): 그림 4c 3 행 ↔ 그림 8a = 0.93 (대조 0.54) · 그림 6c ↔ 그림 10a = 같은 영상 아님 (−0.20).
- 원문 전수 검색: DEM · simulation · model 0 회 · 'coating' = LiNbO₃ 만 · 'intensive' = 참고문헌 [16] 제목만 · Kawaguchi · Nakamura 2020 인용 0.
- 정본 중복 확인: `git ls-tree` 로 `litdb/papers/` 전수 + DOI (`apt.2022.103705` · `103705`) · 'hayakawa' · 'high-shear' · 'Dry mixing of cathode composite' grep — 카드 없음 (wolf2026 · frankenberg2025 · hayakawa2023 이 인용만) · 같은 저자 같은 해의 다른 논문 (103470) 카드 없음.

## 🔗 관련 카드
- 이 논문을 인용한 카드: `wolf2026_extruder_vs_batch_mixing_core_shell_dry_sulfide_cathode` (목록 15 · L335) · `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` (목록 64 · L363) · `hayakawa2023_dry_coated_composite_particles_conductive_additives_ab_vgcf` (ref [10] · L313).
- 이 논문이 인용한 정본 카드: `kim2013_mixing_method_dry_wet_ball_mixer_lco_li2s_p2s5_composite_cathode` ([21]) · `nam2018_dry_vs_slurry_mixed_electrode_binder_coverage_premixing_pouch` ([19]) · `siroma2016_ac_impedance_tlm_electron_electron_connection_effective_conductivity_assb` ([30]) · `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity` ([31]) · `sakuda2011_pld_sulfide_se_coated_licoo2_composite_cathode` ([35]) · `kamaya2011_lgps_lithium_superionic_conductor` ([8]) · `kato2016_high_power_assb_lsipscl_superionic` ([11]).
- 같은 그룹 (오사카 공립대 · Nakamura): `hayakawa2023_dry_coated_composite_particles_conductive_additives_ab_vgcf` (같은 재료 · 같은 σ 셀) · `nakamura2020_dry_coating_ncm_li3ps4_core_shell` · `kawaguchi2017_dry_coating_parametric_na2so4_model_se` · `kawaguchi2018_dry_coating_model_se_particle_powtec` · `kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps`.
- 혼합 공정 · 믹서 (정본): `frankenberg2024_dem_high_intensity_mixer_assb` · `kissel2025_cathode_mixing_quality_cam_utilization_reproducibility_press_cells` · `kissel2026_mechanofusion_derived_cathode_composite_microstructures_scalable` · `otani2025_dem_se_dispersion_aggregation_compression` · `lischka2025_dem_eirich_intensive_mixer_dry_mixing` · `hare2026_dem_pept_dry_mixing_nmc622_eirich` · `kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage` · `lee2024_shear_force_dry_process_cathode_coverage` · `kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact`.
- LiNbO₃ 코팅 NCM523: `bong2023_linbo3_thickness_uniformity_ncm523`.
- 수송 대조 (정본): `bazzoun2026_dem_fem_rnm_ionic` · `minnmann2021_jes_charge_transport_bottlenecks`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

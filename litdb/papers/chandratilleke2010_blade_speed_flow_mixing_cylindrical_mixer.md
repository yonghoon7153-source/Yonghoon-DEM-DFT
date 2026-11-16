<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목. 형식 = chandratilleke2012_particle_scale_mixing_index.md (같은 제1 저자 · 같은 믹서 계열 — 절 번호 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표 꼴 그대로).
     쪽 표기 = 학술지 쪽 "p.5467"–"p.5478" (Ind. Eng. Chem. Res. 49(11) · PDF 쪽 = 학술지 쪽 − 5466 · figures.json 의 page 와 크롭 이름 txt_p<NN> 은 PDF 쪽).
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv · 박힌 래스터의 프레임 선 · 눈금으로 보정) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 대조] = 다른 정본 카드 · 일반 식과 꼴을 맞춰 본 것 · [카드 추론] · [추정] = 이 카드의 해석 · [미확인] = 원문 (12 쪽 전수 · SI 없음) 에 없음 · [정본 카드 표기] = 우리 쪽 값을 다른 정본 카드에서 옮긴 것 (리포 코드 대조는 이 카드에서 하지 않았다) · [지시서] = 논문 에이전트 지시서가 준 우리 쪽 값.
     원문 = 본문 12 쪽 (SI 없음) — 텍스트 층 전수 + Table 1 · 식 (1)–(4) 를 300 dpi 렌더로 글자 대조 (텍스트 층이 '=' 를 ')' 로 · 분수 · 지수를 깨뜨림) · 그림 14 · 표 1 = 크롭 45 장 전부 열람. -->

# 날개 속도 2–100 rpm 수직 원통 2 날개 믹서 DEM — 단분산 5 mm 유리 유사 구 16,000 개 · 수평 · 원통 단면 속도장 · 배위수 · Lacey 지수 · 힘 망 · 날개 토크 · **Table 1 = Yu 그룹 DEM 의 힘 · 토크 식 한 벌** (법선 δ_n^{3/2} 탄성 · μ_s 한도 3/2 승 접선 · 비선형 점성 감쇠 · 방향 일정 구름 토크 μ_r = 5 × 10⁻⁵ m) · 영률 10⁹ → 2.16 × 10⁶ Pa (계산 시간 때문 · ≈ 1/463) — 회전수로 보면 느린 날개가 더 빨리 섞는다 (2 rpm 4 회전 ↔ 100 rpm 6 회전 · 에너지 27.6 ↔ 65.5 J) — Chandratilleke · Zhou · Yu · Bridgwater (Ind. Eng. Chem. Res. 2010)

> slug `chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer` · DOI `10.1021/ie901581t` · type `DEM (vertical bladed mixer · in-house soft-sphere DEM: Hertz-form normal + Mindlin–Deresiewicz-form tangential + nonlinear viscous damping + directional constant rolling torque · E softened 10⁹ → 2.16 × 10⁶ Pa · monosized 5 mm · non-cohesive · 2–100 rpm)` · PDF `c37e391c-32._Effect_of_blade_speed_on_granular_flow_and_mixing_in_a_cylindrical_mixer.pdf` (본문 12 쪽 · SI 없음) · digested `2026-11-12` · status ✅
>
> **원제**: *Effect of Blade Speed on Granular Flow and Mixing in a Cylindrical Mixer* (p.5467)
> **저자**: G. R. Chandratilleke · Y. C. Zhou · A. B. Yu (교신, a.yu@unsw.edu.au) — Laboratory for Simulation and Modeling of Particulate Systems, School of Materials Science and Engineering, University of New South Wales, Sydney · J. Bridgwater — Department of Chemical Engineering, University of Cambridge (p.5467)
> *Ind. Eng. Chem. Res.* **49**(11), 5467–5478 (2010) · 접수 2009-10-09 · 수정 2010-04-16 · 채택 2010-04-21 · 웹 게재 2010-05-06 (p.5467 · p.5478) · 연구비 Australian Research Council (p.5477).
> **판독 원자료**: `litdb/figures/chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer/digitized.csv` (241 행 — Fig 4 · 6 · 7 · 8 · 9 · 12 · 13 · 14) · 크롭 **45 장** = 그림 14 · 표 1 · 식 10 (식 1–4 번호마다 + Table 1 여섯 행) · 근거 문단 20 — `figures.json`.
> **이 카드가 서랍에 들어온 이유**: 후보 표 N-32 (`litdb/_curation/S8_candidates.md`) — 정본 카드 [`chandratilleke2012_particle_scale_mixing_index`](chandratilleke2012_particle_scale_mixing_index.md) 가 DEM 을 *"선행 ref 18 의 방법"* 으로만 적고 힘 법칙을 [미확인] 으로 남겼다 (그 카드 L187 · L291 · L307) — 그 ref 18 이 이 논문이다.

> ★★ **한 줄로 왜 중요한가**: 2012 PSMI 카드가 남긴 빈칸 — *"연화 영률이 어느 점접촉 법칙에 들어갔나"* — 의 답이 Table 1 에 있다: **법선 = 같은 크기 두 구의 Hertz 꼴** (E/(3(1−ν²))·(2R_i)^{1/2}·δ_n^{3/2} = (4/3)E*√R*·δ_n^{3/2} [카드 산술]) · **법선 감쇠 = (m·E·√(Rδ_n))^{1/2} 꼴 (∝ δ_n^{1/4})** — E 는 이 둘에 **직접** 들어가고, 접선 (Mindlin–Deresiewicz 꼴 · μ_s F_n 상한) · 접선 감쇠 · 구름 토크 (μ_r F_n) 에는 **법선력을 거쳐** 들어간다.  ÷463 연화는 **시간 간격을 위한 것** 이라 같은 힘에서 겹침 ×59.9 · 충돌 시간 ×11.6 · 반발계수는 그대로 [카드 산술].
> ★ 혼합 쪽 메시지: **시간으로는 빠른 날개 · 회전수로는 느린 날개** (2 rpm 4 회전 ↔ 100 rpm 6 회전에 M ≈ 1 · p.5471) — 저자는 팽창 (공극 0.54 → 0.63 [판독]) · 충돌 에너지 손실 · 원심력이 **확산 혼합** 을 늦춘다고 설명하고, 2 rpm 이 에너지 58 % 를 아낀다 (27.6 ↔ 65.5 J · 시간 33 배).
> ⚠ 저자 스스로 접촉 지표 하나를 **연화 탓** 으로 돌린다: *"the observed slight increase in the steady-state value should have resulted from the use of the softer particles in this work"* (p.5473) — 우리 연화 (압축 DEM 18 배 · 믹서 SE 1 × 10⁷ Pa) 아래 **접촉 기반 지표** (s1 · s2 · 배위수) 의 E 민감도를 결과 전에 등록할 근거.
> ⚠ **절대값 전이**: 유리 유사 mm 구 · 비점착 · 무압축 흐름이라 **LPSCl · NCM 값으로 옮길 숫자가 없다** — 옮길 수 있는 것은 식 꼴 · 지표 정의 · 보고 방식뿐.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: UNSW Yu 그룹의 2 날개 수직 원통 믹서 (안지름 249 mm · 날 높이 40 × 두께 10 mm · 벽 · 바닥 틈 없음) 에 단분산 5 mm 유리 유사 구 16,000 개를 넣고 날 속도를 2 → 100 rpm 으로 바꾼 3D DEM 에서, 시간으로는 빠를수록 빨리 섞이지만 (Fig 6a) **회전수로는 느릴수록 빨리 섞이고** (*"at 2 rpm, M = 1 is reached in four revolutions compared to six revolutions at 100 rpm"* · p.5471), 그 차이를 저자는 팽창 · 충돌 에너지 손실 · 원심력이 늦춘 확산 혼합으로 설명하며 (47.75 → 100 rpm 의 약간의 회복은 Fr 0.32 → 1.4 의 토로이드 운동), B–W 배위수가 거시 Lacey 지수와 같은 회전수에 정상에 닿는다 — 그리고 **Table 1 이 이 계열 DEM 의 힘 · 토크 식 여섯을 지면에 싣는다** (법선 = 같은 크기 두 구의 Hertz 꼴 · 접선 = Mindlin–Deresiewicz 꼴 · 비선형 점성 감쇠 · 방향 일정 구름 토크 · E 는 법선 힘과 법선 감쇠에 직접).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① 2012 PSMI 논문 DEM 의 **힘 법칙** 은? | Table 1 여섯 행 = 법선 탄성 F_cn = −E/(3(1−ν²))·(2R_i)^{1/2}·δ_n^{3/2}·n̂ (같은 크기 두 구의 Hertz 꼴) · 법선 감쇠 (∝ δ_n^{1/4}) · 접선 = μ_s F_cn [1 − (1 − δ_t/δ_t,max)^{3/2}] (Mindlin–Deresiewicz 꼴 · δ_t,max = μ_s(2−ν)/(2(1−ν))·δ_n) · 접선 감쇠 · 회전 토크 R_i × (F_ct + F_dt) · 구름 토크 −μ_r F_cn ω̂_i.  'Hertz' · 'Mindlin' 낱말은 원문에 없다 | [인쇄] Table 1 p.5468 · [카드 대조] §3-2 |
| ② **연화 영률이 어디에** 들어갔나? | 법선 탄성 계수 E/(3(1−ν²)) 와 법선 감쇠 계수 (3m_iE/(√2(1−ν²)))^{1/2} 두 곳에 직접 · 나머지는 F_cn 을 거쳐.  10⁹ → 2.16 × 10⁶ Pa (÷463) *"to reduce computational time"* | [인쇄] p.5468 · [카드 산술] 겹침 ×59.9 · 충돌 시간 ×11.6 · 반발계수 그대로 (§3-9 ②) |
| ③ 이 논문이 2012 DEM 의 **원전** 인가? | **식의 지면 출처** 다 (2012 ref 18).  모델 자체는 *"developed previously,9,12"* = Zhou 2004 (*Chem. Eng. Sci.*) · Zhou 1999 (*Physica A*) · 식 표는 *"commonly used as discussed in the recent review ... 13"* (Zhu 2007) | [인쇄] p.5468 |
| ④ **혼합 지수** 정의 · 칸? | Lacey M = (S₀² − S²)/(S₀² − S_R²) · S₀² = pq (이론) · S_R² = pq/N (이항) · S² = Σ(N_i/N)(n_i/N_i − p)² (칸 입자 수 가중 · 편차는 기대 분율 p 기준) · 칸 = 고리 5 개 (폭 21.7 mm) × 6/11/16/21/26 등분 (층당 80 칸) × 높이 20 mm | [인쇄] 식 3–4 p.5471 · 칸당 ≈ 67–101 개 [카드 산술] |
| ⑤ **날 속도 효과** (값)? | M ≥ 0.95 첫 도달 = 2 rpm 3.70 · 9.55 rpm 4.06 · 47.75 rpm 5.00 · 100 rpm 4.58 회전 · 배위수 (5 % 간격) 6.34 → 5.45 · 공극 (바닥 – 날 윗변) ≈ 0.45 (0 rpm) → 0.54 (2) → 0.63 (100) · 평균 법선력 0.0137 → 0.0222 N · 토크 Γ = 1.086 e^{0.0047ω} N m | [판독] Fig 4 · 6b · 12b · [인쇄] p.5475–5476 |
| ⑥ 우리 믹서 **Lacey (16×16×4)** 와 같은 연산자? | **이름만 같다** — 분리 기준 (이론 pq ↔ 우리 런 t₀ 실측) · 칸 가중 (입자 수 ↔ 같은 무게) · 무작위 기준 (이항 pq/N ↔ 균일 삽입 런 실측) · 칸당 입자 (≈ 67–101 ↔ n_eff ≈ 3.6–3.7) 가 다 다르다 | [인쇄] p.5471 · [정본 카드 표기] 2012 카드 §7 · 비교 문서 §H |
| ⑦ **DEM 한계 · 소성** (질문 k · l)? | 구 · 점접촉 한계 문장 없음 · 소성 · 탈압 · 2D 없음 (3D DEM).  가장 가까운 둘: 연화 E 가 접촉 지표 (B–W 배위수 비) 를 바꾼다 (p.5473) · 5 % 간격 허용 때문에 배위수 > 12 가 가능 (p.5472) | [인쇄] p.5472–5473 |
| ⑧ **힘 · 파괴** 자리? | 날 앞 · 바닥 모서리에 큰 법선력 (0.1–0.3 N) · 100 rpm 에서 벽 쪽으로 · *"these forces can be reduced if the blade is lifted above the bottom of the mixer"* — 파괴 모델은 없다 | [인쇄] p.5474–5475 · Fig 10 · 11 |

⛔ **한정어 (떼지 말 것)**: ① **단분산 5 mm · 비점착 · 유리 유사 물성 (재료 이름 없음) · 공기 무시** ② 날 속도마다 **런 1 회** (시드 산포 없음) · 계산 비용 [미확인] ③ **실험 값이 이 논문 안에 없다** — 검증은 Stewart 2001 PEPT (ref 10) 로 넘긴다 ④ E ÷463 은 **시간 간격용** (보정값 · 물성 아님) ⑤ 40 rpm 이하 *"회전수 한 곡선"* (선행 refs 19 · 20) 과의 대조는 **dt 50 → 5 µs 와 속도 범위가 함께 바뀐** 비교다.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-32 의 '왜' 칸)

의도 원문: *"e · k — chandratilleke2012 DEM 의 방법 원전: 힘 법칙 (Hertz · Mindlin 여부) · 감쇠 · 구름마찰 식이 2012 논문에 없어 카드가 '이 논문만으로 DEM 을 재현할 수 없다 (ref 18 필요)' 로 남김 → 연화 영률이 어느 점접촉 법칙에 들어갔는지"* — 가리킨 카드 = `chandratilleke2012_particle_scale_mixing_index` (L187 · L291 · L307).  측정 조건 공통: 흐름 (혼합) 중 · 압축 · 탈압 없음 · 상온 개념 없음 · 단분산 5 mm · 진밀도 = 입자 밀도 2500 kg m⁻³ (인쇄).

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "chandratilleke2012 DEM 의 방법 원전" | **일부** | 2012 의 ref 18 = 이 논문 (서지 같음).  그러나 이 논문은 모델을 *"The DEM model used here was developed previously,9,12 extending the original DEM model proposed by Cundall and Strack8 by accounting for the rolling friction of particles."* 로 적는다 (p.5468 · `txt_p02_dem_developed_previously_refs9_12_table1_review13.png`) → 모델 원전 = ref 9 (Zhou, Yu, Stewart, Bridgwater 2004 · *Chem. Eng. Sci.* 59, 1343–1364) · ref 12 (Zhou, Wright, Yang, Xu, Yu 1999 · *Physica A* 269, 536–553).  식 표 = *"They are commonly used as discussed in the recent review of various force models for DEM simulations.13"* (ref 13 = Zhu, Zhou, Yang, Yu 2007 · *Chem. Eng. Sci.* 62, 3378–3396).  ⇒ **식이 지면에 실린 출처** 로는 채움 · '처음 만든 논문' 으로는 아님 |
| "힘 법칙 (Hertz · Mindlin 여부)" | **채움 (식) · 일부 (이름)** | 법선 F_cn,ij = −E/(3(1−ν²))·(2R_i)^{1/2}·δ_n^{3/2}·n̂ (Table 1 1 행) — 같은 크기 두 구에서 Hertz (4/3)E*√R*·δ_n^{3/2} (E* = E/(2(1−ν²)) · R* = R_i/2) 와 같다 [카드 산술: 두 식 다 계수 55,947 N m^{−3/2}].  접선 F_ct,ij = −(μ_s F_cn,ij/\|δ_i\|)·[1 − {1 − min(\|δ_t\|, δ_t,max)/δ_t,max}^{3/2}]·δ_t · δ_t,max = μ_s(2−ν)/(2(1−ν))·δ_n (3 행) — Mindlin–Deresiewicz 꼴 (μ_s F_n 에서 미끄럼) [카드 대조].  'Hertz' · 'Mindlin' 낱말 = 원문 12 쪽 0 회.  조건: 단분산 · 벽 · 날 = 입자 물성 · 크기 다른 쌍 · 벽 접촉의 R = [미확인] |
| "감쇠" | **채움** | 법선 F_dn,ij = −c_n·(3m_iE/(√2(1−ν²))·(Rδ_n)^{1/2})^{1/2}·(V_ij·n̂)n̂ (2 행) · 접선 F_dt,ij = −c_t·(6m_iμ_sF_cn,ij·√(1 − δ_t/δ_t,max)/δ_t,max)^{1/2}·V_t,ij (4 행) · c_n = c_t = 0.3 (p.5468 · `txt_p02_glass_like_mu_r_5e-5m_mu_s_0p3_e_1e9_to_2p16e6_dt_5us.png`).  ⚠ 법선 감쇠의 부호 · R 정의 · 접선 식의 \|δ_i\| (§3-9 ⑥ · §10) |
| "구름마찰 식" | **채움** | M_ij = −μ_r·F_cn,ij·ω̂_i · ω̂_i = ω_i/\|ω_i\| · μ_r = 5 × 10⁻⁵ m (6 행 · p.5468) — 크기 일정 · 방향만 자기 회전 반대 = [`ai2011_rolling_resistance_contact_models_dem`](ai2011_rolling_resistance_contact_models_dem.md) 의 **A 부류 (방향 일정 토크 · 대표 = Zhou 1999)** 꼴 [카드 대조] · 단 방향 기준이 **자기 ω_i** (ai2011 식 8a 는 상대 회전 ω_i − ω_j) · μ_r 이 길이 (m) |
| "2012 논문에 없어 카드가 '이 논문만으로 DEM 을 재현할 수 없다 (ref 18 필요)' 로 남김" | **일부 해소** | 식은 이 카드 §3-2 로 채워진다.  남는 빈칸: ① 벽 · 날 접촉의 R (식은 같은 크기 두 구 꼴만) ② 크기 다른 두 구의 R 규약 (2012 는 크기비 0.5–1) ③ 법선 감쇠의 R · 부호 ④ 2012 믹서는 틈이 있다 (벽 2.5 mm · 바닥 7.5 / 0 mm · 날 106 mm — 2012 카드 §3-1 L58) ↔ 이 논문 *"the blades have no clearance either at the cylindrical wall or at the bottom of the vessel"* (p.5468) ⑤ dt 2–5 µs (2012) ↔ 5 µs ⑥ 적분법 · 이웃 탐색 · 계산 비용 [미확인] |
| "연화 영률이 어느 점접촉 법칙에 들어갔는지" | **채움** | E 는 법선 탄성 계수 E/(3(1−ν²)) 와 법선 감쇠 계수 (3m_iE/(√2(1−ν²)))^{1/2} 에 **직접**, 접선력 · 접선 감쇠 · 구름 토크에는 F_cn (곧 δ_n) 을 거쳐 **간접** 으로 들어간다.  값 · 이유 · 근거: *"Young's modulus E, however, was reduced from 10^9 of real glass beads to 2.16 × 10^6 to reduce computational time; this approach has been found to be able to produce reliable results.9,12"* (p.5468 · 단위 = Pa, Nomenclature p.5477).  [카드 산술] ÷463 → 같은 힘에서 겹침 ×463^{2/3} = 59.9 · 접촉 반지름 ×7.7 · 충돌 시간 ×463^{2/5} = 11.6 · 반발계수 그대로 |
| (질문 e) 점접촉 법칙이 깨지는 범위 · 대안 | **없음** | 큰 변형 · 고밀도 압밀을 다루지 않는다 · 대안 법칙 (multi-contact · MDR · Thornton–Ning) 없음 · 맞춘 값 0 (모두 지정값 · 선행 연구 인용) |
| (질문 k) DEM 한계 문장 | **일부** | 구 · 점접촉 자체의 한계 문장은 없다.  가장 가까운 둘 = *"Therefore, the observed slight increase in the steady-state value should have resulted from the use of the softer particles in this work. Use of a larger Young's modulus will have resulted in fewer particle deformations and thus fewer particle contacts, possibly reducing the B-W CN ratio at the steady state."* (p.5473 · `txt_p07_cn_ratio_100rpm_softer_particles_larger_e_fewer_contacts.png`) · *"(N.B.: coordination number >12 is possible because of the (5%)d gap allowance used here)"* (p.5472 · `txt_p06_initial_cn_6_and_2_eight_vs_six_max14_gap_5pct.png`) |

**가리킨 카드의 2 차 인용 대조** (`chandratilleke2012_particle_scale_mixing_index` — 고치지 않는다):

| 가리킨 카드 줄 | 이 논문 원문 | 판정 |
|---|---|---|
| L187 *"자체 DEM (선행 ref 18 의 방법 — 이 논문에서는 반복하지 않음) · 병진 · 회전 운동량 보존 · 접촉 = 법선 · 접선 탄성 + 감쇠 · 접선력 토크 + 구름마찰 (변형 에너지 소산) · 벽 · 날개 = 입자 물성.  ⚠ 힘 법칙의 식 (Hertz · Mindlin 여부) 은 이 논문에 없다 [미확인 — ref 18 · 29 참조]"* | 식 (1) · (2) = 병진 · 회전 운동량 식 · Fc = 법선 + 접선 탄성 · Fd = 법선 + 접선 감쇠 · T_ij + M_ij (구름) · 벽 · 날 = 입자 물성 (p.5468) | **같은 뜻** — [미확인] 은 이 카드 §3-2 로 해소 ('변형 에너지 소산' 이라는 구름마찰 풀이는 이 논문에 없음 · 2012 원문의 말로 보임 [추정]) |
| L291 *"힘 법칙 미기재 — 이 논문만으로 DEM 을 재현할 수 없다 (ref 18 필요)."* | ref 18 (이 논문) Table 1 에 식 여섯이 있다 | **맞음** — 단 ref 18 로도 2012 의 크기 다른 쌍 · 벽 접촉 · 틈 있는 믹서는 다 정해지지 않는다 (위 표 다섯째 줄) |
| L307 *"18 \| Chandratilleke GR, Zhou YC, Yu AB, Bridgwater J. Ind Eng Chem Res. 2010;49:5467–5478 \| 이 논문 DEM 의 방법 원전 — 카드 없음"* | 서지 같음 (호 11 · 제목 · DOI 10.1021/ie901581t 는 그 줄에 없음).  이 논문 자신은 *"developed previously,9,12"* | ⚠ **카드 문제 (경미)** — '방법 원전' 은 반만 맞다: 모델 원전 = Zhou 2004 · Zhou 1999 · 이 논문 = 식의 지면 출처.  '카드 없음' 은 이 카드로 낡음 |
| (참고) L61 *"★ 영률 … 2.16 × 10⁶ N m⁻² 로 낮춤 (시간 간격 때문) · '실험과 잘 맞음' (ref 12 · 17)"* | 이 논문의 같은 문장은 근거를 refs 9 · 12 (Zhou 2004 · Zhou 1999) 로 단다 | 문제 아님 — 2012 논문 자기 번호 (그 카드 §11: 12 = Stewart 2001) |

⇒ **의도 대조 결과: 일부** — 힘 · 감쇠 · 구름 토크 식과 연화 E 가 들어간 자리는 **채움** (Table 1 · p.5468) · '방법 원전' 은 **일부** (모델 원전 = refs 9 · 12 · 식 표 = review ref 13 · 이 논문은 식의 지면 출처) · 'Hertz · Mindlin' 은 **꼴로만** (낱말 없음) · 2012 재현의 빈칸 (벽 · 크기 다른 쌍 · 감쇠의 R · 틈) 은 남음 · 질문 e (깨지는 범위 · 대안) 는 **없음** · 질문 k 는 연화 고백 한 문장으로 **일부**.

---

## 1. 한 줄 요약

**같은 그룹의 2 날개 수직 믹서 DEM (단분산 5 mm 구 16,000 개) 에서 날 속도를 2 → 100 rpm 으로 바꿔 흐름 (날 상대 속도장) · 구조 (배위수 · 공극) · 혼합 (Lacey M · 부분 배위수) · 힘 (힘 망 · 접촉력 분포 · 날 토크) 을 본 논문.**  ① 날 앞에 더미가 서고 일부는 날을 넘거나 더미 면을 굴러 다시 날 쪽 흐름에 합류 — 속도 ↑ 면 벽 쪽 재순환은 사라지고 축 쪽에 복잡한 재순환 · 축–날 모서리 소용돌이 · 날 뒤 빈 공간 · 더미 높이 (100 rpm 날 높이의 2 배) 가 커진다 ② 속도 ↑ 면 배위수 ↓ · 공극 ↑ (팽창) ③ 시간으로는 빨라도 **회전수로는 느린 날이 낫다** (2 rpm 4 회전 · 100 rpm 6 회전에 M ≈ 1) — 40 rpm 이하에서 보였던 '회전수 한 곡선' 은 넓은 범위에서 깨진다 ④ B–W 배위수가 거시 지수와 같은 회전수에 정상에 닿는다 ⑤ 날 앞 · 바닥 모서리에 큰 힘 (0.1–0.3 N) · 속도 ↑ 면 벽 쪽으로 · 평균 법선력 0.014 → 0.022 N ⑥ 토크 Γ = 1.086 e^{0.0047ω} · 혼합 에너지 2 rpm 27.6 J ↔ 100 rpm 65.5 J (58 % 절감 · 시간 33 배).

## 2. 메타

| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| G. R. Chandratilleke · Y. C. Zhou · A. B. Yu (교신, UNSW) · J. Bridgwater (Cambridge) | *Ind. Eng. Chem. Res.* 49(11) 5467–5478 (2010) · 웹 2010-05-06 | 10.1021/ie901581t | **유리구 유사 구** (재료 이름 없음 · ρ 2500 kg m⁻³ · μ_s 0.3 · μ_r 5 × 10⁻⁵ m · ν 0.3 · c_n = c_t 0.3 · E 2.16 × 10⁶ Pa 연화) · 단분산 지름 5 mm · 벽 · 날 = 입자 물성 | **DEM** (자체 코드 · Cundall–Strack + 구름마찰 · 선행 refs 9 · 12 의 모델) — 흐름 · 구조 · 혼합 · 힘 · 토크 |

> ★ **계보 (이 논문 참고문헌만으로)**: Zhou 1999 (*Physica A* — 구름마찰 · 모래더미 · ref 12) → Stewart 2001 (*Chem. Eng. Sci.* — 같은 믹서 DEM ↔ PEPT · ref 10) → Zhou 2002 WCPT4 학회 (날 속도 · ref 20) · Zhou 2003 (*J. Chem. Technol. Biotechnol.* — 이원 분리 · ref 19) → Zhou 2004 (*Chem. Eng. Sci.* — 미시 동역학 · ref 9) → **이 논문 (2010)** → Chandratilleke 2012 (*AIChE J.* — PSMI · 이 논문을 ref 18 로 DEM 방법 인용 · [`chandratilleke2012_particle_scale_mixing_index`](chandratilleke2012_particle_scale_mixing_index.md)).
> ★ **이 논문 안의 '선행 연구'**: refs 19 · 20 = 40 rpm 이하 날 속도 · dt 50 µs · *"the mixing index M of eq 3 collapses into a single curve when expressed as a function of the number of blade revolutions"* (p.5471) · ref 9 = 10 rpm 토크 1.1 N m (*"for the simulation conditions identical to those of this work"*, p.5475) · 배위수 · 공극 · 힘 망 분석법 (p.5470 · 5474).

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 믹서 · DEM 설정 (Simulation Conditions · p.5468–5469 · Fig 1)

| 항목 | 값 | 출처 |
|---|---|---|
| 믹서 | 수직 원통 **안지름 0.249 m** · 축 지름 0.032 m · 평판 날 2 개 (지름 방향 · **높이 0.04 m × 두께 0.010 m**) · **벽 · 바닥 틈 없음** · 용기 높이 100 mm (Fig 1a 라벨) | [인쇄] p.5468 · Fig 1a |
| 설계 근거 | *"The mixer geometry and simulation conditions are very similar to those in a PEPT study by Stewart et al.10"* | [인쇄] p.5468 |
| 입자 | 단분산 구 **지름 5 mm × 16,000 개** · *"properties close to those of glass beads"* · 벽 · 날 = 입자와 같은 물성 | [인쇄] p.5468 |
| 물성 | μ_r **5 × 10⁻⁵ m** · μ_s **0.3** · ρ **2500 kg m⁻³** · ν **0.3** · c_n = c_t = **0.3** | [인쇄] p.5468 |
| ★ 영률 | **10⁹** (실제 유리구 · 본문에 단위 없음 — Nomenclature E = Pa) → **2.16 × 10⁶** · *"to reduce computational time"* · *"reliable results"* (refs 9 · 12) | [인쇄] p.5468 · p.5477 · 배수 ≈ **463** [카드 산술] |
| 시간 간격 | **5 × 10⁻⁶ s** (선행 refs 19 · 20 = 50 µs) · 허용 최대 **54 µs** (*"based on the known relationships for the particle properties considered.21,22"* · 식 없음) · *"A smaller time step can generate more reliable results."* | [인쇄] p.5468 · p.5471 |
| 생성 · 정착 | 겹침 없는 무작위 배치 → 중력 정착 **≈ 0.95 s** → 윗면 ≈ 날 윗변 (**바닥에서 ≈ 40 mm**) → 정착 직후 일정 각속도로 회전 · *"A few blade rotations produce a macroscopically stable flow"* 뒤 미시 분석 | [인쇄] p.5468–5469 |
| 날 속도 | **2–100 rpm** — 보고 값 2 · 9.55 · 23.87 (23.8) · 47.75 (47.7 · 47.5) · 100 · Fig 7a = 10 · 100 rpm = 끝 속도 **1.3 m/s** (*"about 1/10 the blade tip speed required for a so-called high-speed mixer"*) | [인쇄] p.5469 · 그림 캡션 |
| 공기 | 항력 무시 (*"the blade tip speed is still low, the inertia of particles is large, and the drag force is small"*) | [인쇄] p.5469 |
| 검증 | *"the proposed DEM approach has been validated against the PEPT measurements as detailed by Stewart et al.10"* — 이 논문 안에 실험 값 없음 | [인쇄] p.5469 |
| 계산 비용 · 하드웨어 · 적분법 · 이웃 탐색 | 없음 | [미확인] |
| 혼합 장입 | 좌우 반씩 색칠 (밝은 회색 = W · 어두운 회색 = B) — 같은 입자, 색만 다르다 | [인쇄] p.5470 · 5472 |
| 기준틀 | **날 상대 속도** = 입자 속도 − ω × r (r = 수평면에 투영한 위치) · 끝 속도로 정규화 · 정규화 값 ≈ 1 = 거의 정지 | [인쇄] p.5469 |

[카드 산술] (§3-9 에 식):
- rpm → rad/s: 9.55 = **1.000** · 23.87 = **2.500** · 47.75 = **5.000** · 100 = 10.47 · 2 = 0.209 → 중간 세 속도는 rad/s 로 둥근 값.
- 끝 속도 v_tip = ωD/2: 2 → 0.026 · 9.55 → 0.125 · 23.87 → 0.311 · 47.75 → 0.623 (인쇄 0.62) · 100 → 1.304 m/s (인쇄 1.3 · 1.31).
- 날 길이 (틈 없음) = (249 − 32)/2 = **108.5 mm** (2012 믹서 = 106 mm + 벽 틈 2.5 mm — 2012 카드 §3-1).
- 입자 질량 1.636 × 10⁻⁴ kg · 무게 1.61 mN · 침대 무게 25.7 N.
- 정지 침대: 축–벽 고리 (r 16–124.5 mm) × 높이 40 mm 에 16,000 개가 다 있으면 고체분율 0.547 (날 부피 빼지 않음) · 0.573 (날 2 × 108.5 × 10 × 40 mm 뺌) → 공극 **0.453 · 0.427** — Fig 4 의 0 rpm 표지 ≈ 0.45 (축 아래 끝) 와 같은 크기.

### 3-2. ★ 운동 식 (1)–(2) · 힘 · 토크 식 (Table 1 · p.5468 · 렌더 대조)

**식 (1)–(2)** (크롭 `eq_01_translational_motion_newton.png` · `eq_02_rotational_motion_torques.png`):
- (1) m_i dV_i/dt = m_i **g** + Σ_{j=1}^{k_i} (**F**_c,ij + **F**_d,ij)
- (2) I_i dω_i/dt = Σ_{j=1}^{k_i} (**T**_ij + **M**_ij)
- k_i = 입자 i 와 닿은 입자 수 · 앞 문장 = *"subjected to the gravity and interactions with the neighboring particles, blade, and walls"* · F_c = 법선 + 접선 **탄성력** · F_d = 법선 + 접선 **감쇠력** · T = 토크 · M = 구름 마찰 토크 [인쇄].

**Table 1 — Formulas for Contact Forces and Torques** (크롭 `tab_1.png` + 행마다 `eq_t1a` … `eq_t1f`):

| 힘 · 토크 | 식 (렌더 대조 · 인쇄 그대로) | 딸린 정의 | 크롭 |
|---|---|---|---|
| 법선 탄성력 | **F**_cn,ij = −E/(3(1 − ν²)) · (2R_i)^{1/2} · δ_n^{3/2} · n̂ | n̂ = **R**_i/R_i | `eq_t1a_normal_contact_force_delta_n_3_2.png` |
| 법선 감쇠력 | **F**_dn,ij = −c_n · ( 3m_iE/(√2(1 − ν²)) · (Rδ_n)^{1/2} )^{1/2} · (**V**_ij·n̂) n̂ | **V**_ij = **V**_j − **V**_i + ω_j × **R**_j − ω_i × **R**_i | `eq_t1b_normal_damping_force.png` |
| 접선 탄성력 | **F**_ct,ij = −(μ_s F_cn,ij / \|δ_i\|) · [1 − {1 − min(\|δ_t\|, δ_t,max)/δ_t,max}^{3/2}] · δ_t | δ_t,max = μ_s · (2 − ν)/(2(1 − ν)) · δ_n | `eq_t1c_tangential_contact_force_delta_t_max.png` |
| 접선 감쇠력 | **F**_dt,ij = −c_t · ( 6m_iμ_sF_cn,ij · √(1 − δ_t/δ_t,max) / δ_t,max )^{1/2} · **V**_t,ij | **V**_t,ij = (**V**_ij × n̂) × n̂ | `eq_t1d_tangential_damping_force.png` |
| 회전 토크 | **T**_ij = **R**_i × (**F**_ct,ij + **F**_dt,ij) | — | `eq_t1e_rotational_torque.png` |
| 구름 마찰 토크 | **M**_ij = −μ_r F_cn,ij ω̂_i | ω̂_i = ω_i/ω_i (단위 벡터) | `eq_t1f_rolling_friction_torque_mu_r_fcn.png` |

- 기호 (Nomenclature p.5477 · `txt_p11_nomenclature_e_pa_mi_ri_delta_t_max_mu_r_m.png`): δ_n = 법선 변형 (겹침) · δ_t = 누적 접선 변형 벡터 · δ_t,max = *"maximum tangential deformation … under nonslip condition"* · **R_i = 입자 i 중심에서 접촉점까지의 위치 벡터** · m_i = 입자 i 질량 · μ_r = 구름마찰 계수 (**단위 m**) · μ_s = 미끄럼 마찰 계수 · c_n · c_t = 감쇠 계수 · E = 영률 (Pa).  법선 감쇠의 **R (첨자 없음)** 은 Nomenclature 에 없다 [미확인].
- 접선 식 · 구름 식 · 접선 감쇠 안의 F_cn,ij 는 이탤릭 (크기) · 그 밖은 굵은 글씨 (벡터) [인쇄 · 렌더 대조].
- [카드 대조 · 산술] **법선 = 같은 크기 두 구의 Hertz 꼴**: E* = E/(2(1−ν²)) · R* = R_i/2 이면 (4/3)E*√R* = (√2/3)E√R_i/(1−ν²) = E(2R_i)^{1/2}/(3(1−ν²)) — 이 논문 값으로 둘 다 **55,947 N m^{−3/2}** (E 2.16 × 10⁶ · ν 0.3 · R_i 2.5 mm).  벽 (평면) 과의 접촉이면 R* = R_i 라 같은 꼴에서 √2 배가 달라진다 — 벽 · 날 접촉에 어떤 꼴을 썼는지 [미확인].
- [카드 대조] **접선 = Mindlin–Deresiewicz 꼴**: 힘이 μ_s F_n 에서 멈추고 (1 − (1 − δ_t/δ_t,max)^{3/2}) 로 부드럽게 다가간다 · δ_t,max/δ_n = μ_s(2−ν)/(2(1−ν)) = **0.364** [카드 산술].
- [카드 산술] **법선 감쇠 ∝ δ_n^{1/4} · ∝ √(m E)** — 비선형 점성 감쇠 (이 꼴의 원전 · 이름은 원문에 없다).  같은 크기 두 구의 정면 충돌을 인쇄 식 그대로 (m_i = 입자 질량 · R = R_i · 감쇠는 소산 방향으로) 적분하면 반발계수 **e ≈ 0.251** — 충돌 속도 0.1–1.3 m/s · E 2.16 × 10⁶ ↔ 10⁹ 에 무관 (이 꼴의 성질) · m_i → 환산 질량 m/2 · R → R/2 · E → E* 로 읽으면 감쇠 ×0.707 → e ≈ **0.393**.  원문은 반발계수를 적지 않는다 [미확인].
- [카드 대조] **구름 = 방향 일정 토크** (크기 μ_r F_cn · 방향 = 자기 회전 반대) — ai2011 A 부류 꼴.  무차원으로 바꾸면 μ_r/R = **0.02** · μ_r/R* = **0.04** [카드 산술].

### 3-3. ★ Lacey 지수 · 칸 (식 3–4 · p.5471 · `eq_03_lacey_mixing_index.png` · `eq_04_weighted_sample_variance_cells.png`)

- (3) **M = (S₀² − S²)/(S₀² − S_R²)** — *"The Lacey index M defined by eq 3 makes a comparison of the sample variance of the mixture S2 with the variances S0 2 and SR 2 of the two reference states of the binary mixture, fully segregated and fully random states, respectively.17"* · **S₀² = pq** (p = 종류 1 의 입자 분율 · q = 1 − p) · *"p is roughly 0.5 for the case in Figure 5a"* · **S_R² = pq/N** (크기 N 의 표본) [인쇄].
- ★ 무작위 기준의 한계 (저자 문장): *"Note that the equation for SR2 is based on the assumption that the particles are different only in color and have a binomial probability distribution for position.16 The latter equation is not applicable to a binary mixture consisting of different sized particles, as implied by Kristensen's results on sampling by fixed volumes.18"* (p.5471 · `txt_p05_s0_pq_sr_pq_over_n_binomial_not_for_sized_kristensen.png`).
- (4) **S² = Σ_{i=1}^{m} [ (N_i/N)(n_i/N_i − p)² ]** — *"the weighted average variance of the particle fraction ni/Ni of type 1 particles ni in the sample i of size Ni"* · p = 기대 분율 · m = 표본 수 · N = 혼합물 전체 입자 수 (Σ N_i = N) [인쇄].  ⚠ 기호 N 두 뜻 (S_R² 의 표본 크기 ↔ 식 4 의 전체 입자 수).
- 칸 (p.5471 · `txt_p05_eq4_weighted_cells_5_annuli_21p7mm_80_segments_20mm.png`): (a) 축–벽 사이 **고리 5 개 (폭 21.7 mm)** (b) 원주 **6 · 11 · 16 · 21 · 26 등분** (안 → 밖) (c) 바닥부터 **높이 20 mm** 씩 · *"The samples produced according to the present segmenting method are different in size. However, this variation has been taken into account in eq 4; the resulting mixing index is reliable. This has been tested in our calculation of M under different conditions."* (검사 결과는 없음).
- [카드 산술] 고리 경계 r = 16 · 37.7 · 59.4 · 81.1 · 102.8 · 124.5 mm → 칸 바닥 넓이 610 · 602 · 599 · 597 · 596 mm² (**거의 같은 넓이** — 등분 수의 이유로 보임 [추정]) · 칸 부피 ≈ 1.2 × 10⁴ mm³ · 층당 80 칸 · 공극 0.45 / 0.54 / 0.632 면 칸당 입자 ≈ **101 / 84 / 68** · 정지 침대 40 mm = 2 층 · 100 rpm 더미 80 mm = 4 층 (빈 칸 · 반쯤 찬 칸 처리 [미확인]).
- [카드 산술] 무작위 이항이면 E[S²] = Σ(N_i/N)·pq/N_i = m·pq/N = pq/N̄ (N̄ = 칸 평균 입자 수) → **식 (4) 와 짝이 맞는 S_R² 의 N 은 N̄** 이다.  원문은 S_R² 에 어떤 N 을 썼는지 적지 않는다 [미확인].

### 3-4. 흐름 (Fig 1b · 2 · 3 · 9 · p.5469–5474)

- **일반 모습** (Fig 1b · p.5469): *"particles rise in front of the blade to form a heap; some particles flow downward on the heap surface in front of the blade and some flow over the blade; the particles that roll down to the front of the blade can rejoin the particle flow toward the blade"* — Stewart 2001 · Remy 2009 (4 날개) 와 같은 모습 [인쇄].
- **수평 단면** (Fig 2 · 중심 높이 ± 2.5 mm): (i) Z = 10 · (ii) 35 · (iii) 60 mm [그림 라벨] · 2 rpm 130 s · 23.8 rpm 55.3 s · 47.75 rpm 27.5 s · 100 rpm 13.3 s [인쇄] = **4.33 · 21.9 · 21.9 · 22.2 회전** [카드 산술 — 2 rpm 만 적은 회전].  2 rpm 에서 날 작용은 날 근처뿐 · 벽 근처는 정지 · 속도 ↑ 면 더 많은 입자가 날에 끌려간다 · 47.75 · 100 rpm 에 축과 앞 날 면의 모서리에 **소용돌이** · 속도 ↑ 면 앞 날 뒤 빈 공간 ↑ · 단면 ii 에서 날을 넘는 입자 ↑ · 단면 iii 입자 수 ↑ = 침대 부피 증가 [인쇄 p.5469–5470].
- **원통 단면** (Fig 3 · r = 50 · 100 mm ± 2.5 mm · 한 날 중앙면 → 다른 날 중앙면): 축 근처 = 날을 넘는 무리 + 자유 표면 근처 재순환 · 벽 근처 = 대체로 한 방향 (저속에서만 재순환) · 속도 ↑ 면 벽 근처 재순환은 줄고 축 근처에는 복잡한 재순환 · 더미 높이 ↑ · 날 뒤 빈 공간 ↑ (끝 속도 1.4 m/s 실험에서 관찰 · ref 15 Kuo 2004 · 이 논문 100 rpm = 1.3 m/s) [인쇄 p.5470].
- **바깥 원통 (r > 80 mm) 의 속도 비** (Fig 9 · θ 0–π 를 15 칸 · 정상 상태): V_z/V_θ 모양은 속도에 크게 안 바뀜 · **V_r/V_θ 는 100 rpm 에서 최소 · 최대가 뚜렷** — [판독] 100 rpm 최소 ≈ −0.11 (θ ≈ 66°) · 최대 ≈ +0.15 (θ ≈ 138°) · 9.55 · 47.75 rpm 은 θ ≈ 30° 의 봉우리 (0.30 · 0.21) 뒤 θ 54–162° 에서 −0.18 – +0.04 로 작고 θ 174° 에서 −0.51 · −0.70 로 떨어진다 · V_z/V_θ 100 rpm 은 θ 138–162° 에서 0.26 → 0.96 [판독].
- **토로이드 운동 판단** (p.5473–5474 · `txt_p08_vr_vtheta_100rpm_froude_15p5_1p4_0p32_toroidal.png`): Nilpawar 2006 (ref 25) = 312 rpm · 지름 285 mm · 끝 속도 4.65 m/s · **Fr = Dω²/(2g) = 15.5** · 사인 모양 속도 비 = 토로이드 운동 (벽 근처에서 오르고 가운데로 떨어짐) · 이 논문 **Fr 1.4 (100 rpm) · 0.32 (47.75 rpm)** → *"at a rotational speed of 100 rpm, the centrifugal acceleration starts to become dominant overcoming gravity, resulting in a toroidal motion in particles"* [인쇄].  [카드 산술] Fr: 2 → 0.0006 · 9.55 → 0.013 · 23.87 → 0.079 · 47.75 → 0.317 · 100 → 1.392 · Nilpawar → 15.5 (인쇄값 셋 재현).

### 3-5. 구조 — 배위수 · 공극 (Fig 4 · 7 · p.5470–5473)

- **정의** (p.5470 · `txt_p04_cn_gap_1_5pct_walls_included_porosity_0_to_blade_top.png`): 두 입자의 간극이 **d 의 1 % 또는 5 %** 보다 작으면 접촉 · 배위수 = 빈도 분포의 평균 · *"In counting the number of contacts, those with the blade surfaces and container surfaces have also been included."* · 침대 전체 평균 · 공극 = 두 수평 단면 사이 (Fig 4 = **바닥 – 날 윗변**) · *"both quantities are difficult to produce experimentally"* [인쇄].

| 날 속도 (rpm) | 배위수 5 % 간격 (△) | 배위수 1 % 간격 (○) | 공극 0–40 mm (□) |
|---|---|---|---|
| 0 | — | — | ≈ 0.45 (축 아래 끝 · 그 이하일 수도) |
| 2 | 6.34 | 5.43 | 0.539 |
| 9.55 | 6.25 | 5.30 | 0.555 |
| 23.87 | 6.18 | 5.19 | — (표지 없음) |
| 47.75 | 5.93 | 4.87 | 0.587 |
| 100 | 5.45 | 4.34 | 0.632 |

[판독 Fig 4 · digitized.csv · 표지 상자 중심 · 오차 ≈ ±0.02 (배위수) · ±0.002 (공극) · 1 % · 5 % 는 그림 안 라벨]
- 원문: 배위수는 속도와 함께 서서히 ↓ · 공극은 ↑ — *"The increase in the average bed porosity is drastic at low blade speeds, after which the increase is gradual"* · 배위수는 *"not a local value, but an average over the entire bed"* 라 급변하지 않는다 [인쇄 p.5470].
- [카드 산술] 5 % − 1 % = 0.91 · 0.95 · 0.99 · 1.06 · 1.10 — 간격 창 하나가 접촉 ≈ 1 개를 더한다 · 2 → 100 rpm 감소 = −14 % (5 %) · −20 % (1 %).
- **부분 배위수** (Fig 7 · 5 % 간격 · 10 · 100 rpm): [판독] 시작 W–W = B–B ≈ 6.0 · B–W = W–B ≈ 2.1 · 전체 ≈ 6.1 (10 rpm) · 정상 (10–20 회전) 10 rpm 전체 **6.11** · 넷 다 ≈ **3.14** · 100 rpm 전체 **5.29** · 넷 다 ≈ **2.80** · 100 rpm 은 시작 6.22 → ≈ 0.5 회전에 최소 5.16 (시동 팽창).  원문: *"Initially, B-B and W-W contact numbers are both about 6. On the other hand, B-W and W-B contacts are both about 2."* · *"Therefore, a particle will have about eight contacts under loose-packing condition at the beginning. The average of the total number of contacts … for a particle is however only slightly more than six; solid angle analysis shows that a single particle can have a maximum of 14 contacts with uniform-sized spheres in three dimensional space (N.B.: coordination number >12 is possible because of the (5%)d gap allowance used here)."* · 정상까지 *"about seven to eight blade rotations"* (p.5472).
- [카드 추론 · 산술] **부분 배위수는 조건부 평균** 이어야 숫자가 맞는다 — 모든 입자 평균이면 W 의 W–W + W–B = 전체 ≈ 6.1 이라 W–W ≈ 6.0 일 때 W–B 는 ≈ 0.1 이어야 하는데 그림은 ≈ 2.1 · 정상에서도 W–W + W–B ≈ 6.28 > 전체 6.11.  ⇒ 그 종류 접촉을 하나 이상 가진 입자만의 평균 (2012 원문은 이것을 명시 — 2012 카드 §4-3) · *"about eight contacts"* = 두 조건부 평균의 합 = 어떤 전형적 입자의 접촉 수가 아니다.
- ⚠ [판독 차이] Fig 4 (9.55 · 100 rpm) 5 % 배위수 6.25 · 5.45 ↔ Fig 7 (10 · 100 rpm) 정상 전체 6.11 · 5.29 — 둘 다 ≈ 0.15 낮다 · 벽 · 날 접촉 포함 여부 · 시간 창 차이일 수 있음 [추정 · 원문에 없음].

### 3-6. 혼합 (Fig 5 · 6 · 8 · p.5470–5474)

- **Fig 5** (높이 37.5 mm 단면 · 위에서 봄): (i) 2 rpm 0 · 20 · 50 · 100 s (ii) 47.7 rpm 0 · 5 · 10 · 15 s (iii) 100 rpm 0 · 2.5 · 5 · 6 s [인쇄] = 0 · 0.67 · 1.67 · 3.33 / 0 · 3.98 · 7.96 · 11.9 / 0 · 4.17 · 8.33 · 10 회전 [카드 산술] · 100 rpm 앞 날 뒤 빈 공간 (*"a result of the particles moving upward in front of the leading blade, causing the particle bed to increase in height"*) [인쇄 p.5471].
- **Fig 6** — 원문: *"Figure 6a shows that the mixture reaches the fully mixed state, M = 1, in shorter times when blade speed is increased"* · *"at 2 rpm, M = 1 is reached in four revolutions compared to six revolutions at 100 rpm. M does not collapse into a single curve as previously observed, but rather it shows a speed dependence in the transition region of mixing. The results suggest that while the mixing due to convection is dominant, the mixing due to diffusion also plays a role"* (p.5471 · `txt_p05_m1_four_rev_2rpm_six_rev_100rpm_no_collapse_diffusion.png`).

| M 수준 (처음 닿는 회전수) | 2 rpm | 9.55 rpm | 47.75 rpm | 100 rpm |
|---|---|---|---|---|
| 0.5 | 1.16 | 1.26 | 1.38 | 1.58 |
| 0.8 | 2.18 | 2.44 | 3.00 | 2.92 |
| 0.9 | 2.90 | 3.30 | 3.98 | 3.74 |
| 0.95 | 3.70 | 4.06 | 5.00 | 4.58 |
| 0.97 | 4.18 | 4.70 | 6.10 | 5.00 |

[판독 Fig 6b · 색 마스크 열 추적 · 오차 ≈ ±0.05 회전] · 시간 (Fig 6a): 2 rpm 34.8 · 64.3 · 86.1 · 108.6 · 129.0 s · 9.55 rpm 7.8 · 15.2 · 20.6 · 25.7 · 30.0 s (같은 M 수준) [판독 · 47.75 · 100 rpm 은 5 s 아래라 못 가름] · 시작 M ≈ **0.10** (좌우 장입) · 평탄값 ≈ **0.98–0.99** (1.00 아님) [판독] · 2 rpm 런은 ≈ 157 s (= 5.2 회전) 에서 끝남 [판독 Fig 6a].
- [카드 산술] 6a ↔ 6b 정합: 2 rpm M 0.95 = 108.6 s → 3.62 회전 (6b 3.70) · 9.55 rpm 25.7 s → 4.09 회전 (6b 4.06).
- **속도 의존의 설명 (저자)** (p.5471–5472 · `txt_p06_porosity_fewer_per_cell_s2_up_centrifugal_blades.png`): ① *"The increased porosity will cause the total particle number in cells to decrease, which in turn will cause S2 to increase as seen from eq 4. The increase in S2 will result in a decrease in M as seen from eq 3."* ② 충돌 에너지 손실 · 원심력 증가 (칸 입자 수 분석 = 벽 근처 입자 ↑) → *"diffusive mixing becomes slower at higher blade speeds"* ③ *"increasing the blade speed is not a good practice for improving the mixing performance. Instead a better choice would be to increase the number of blades"* · *"there may be an optimum number of blades"* ④ 47.75 → 100 rpm 에서 전이 구간 M 이 약간 좋아짐 = 흐름 양상 변화 (토로이드) [인쇄].
- [카드 산술 · 추론] 설명 ① 은 **S_R² 를 고정했을 때** 의 이야기다 — 칸 입자 수가 줄면 무작위 몫 pq/N̄ 도 같이 커지므로, S_R² 를 같은 칸 점유로 다시 세면 그 부분은 상쇄된다 (§3-3 끝).  S_R² 의 N 을 무엇으로 두었는지 [미확인].
- **Fig 8** — 원문: B–W 배위수의 정상 상태는 속도 ↑ 면 **더 많은 회전수** 에 닿는다 (*"consistent with the fact that diffusive mixing can be hampered by the increased centrifugal forces"*) · 정상값은 팽창 때문에 ↓ · *"The fact that B-W CN has reached a constant value shows that mixing has reached the steady state at each blade speed, but it does not reveal the mixing state or the quality of the mixture"* → B–W / 전체 비 (8b) 를 쓴다 · 전이 구간의 비는 2 → 47.75 rpm 에서 ↓ · 47.75 → 100 rpm 에서 다시 ↑ (끝 속도 1.31 ↔ 0.62 m/s · 토로이드) (p.5473).
- [판독 Fig 8] 정상 (8–9.9 회전) B–W 배위수 3.17 (2) · 3.15 (9.55) · 2.99 (47.75) · 2.83 (100 rpm) · B–W / 전체 0.504 (2) · 0.504 (47.75) · **0.518 (100)** · 9.55 rpm 0.489 (4.5–5.5 회전 · 그 뒤 다른 선에 가림) · 시작 0.33–0.38 · 100 rpm 시동 B–W 최저 1.84 (0.67 회전).
- ★ 원문 (연화 고백 · p.5473): *"The CN ratio of Figure 8b shows an increase in the steady-state value at 100 rpm. However, this increase does not imply that mixing has improved at that speed because the state of mixing at the steady state needs to be independent of the blade speed as seen from Figure 6. In other words, the mixer is only capable of fully randomizing the particles and cannot engage in increasing the quality of the mixture any further. Therefore, the observed slight increase in the steady-state value should have resulted from the use of the softer particles in this work."* · 결론: *"the use of the slow blade speeds produces a better mixing rate per blade revolution"* [인쇄].
- [카드 산술] 50 : 50 무작위 침대의 이종 접촉 몫 기대값 = 0.5 → 정상 0.504 는 무작위와 같음 · 100 rpm 0.518 = +2.8 %.

### 3-7. 힘 (Fig 10–13 · p.5474–5475)

- **힘 망** = 두 입자 중심을 잇는 선의 굵기 ∝ 법선 접촉력 (ref 9 방법) · 색 4 구간: 검정 F < 0.03 N · 파랑 0.03–0.1 · 초록 0.1–0.2 · 빨강 > 0.2 N [인쇄 캡션].
- **Fig 10** (수평 단면 Z 0–10 mm · 반쪽 Y ≥ 0): 법선력이 앞 날에서 뒤 날 쪽으로 원주 방향으로 퍼지며 작아진다 · 저속은 그 방향으로 잘 이어짐 · 속도 ↑ 면 뒤 날 뒤에서 끊기고 (빈 공간) 성긴 구조 (침대 부피 ↑ · Stewart PEPT 와 같은 방향) · 앞 날 앞은 약간 더 촘촘 · *"at all blade speeds, the normal contact forces are larger in the quarter of the mixer in front of the blade"* · 100 rpm 은 큰 법선력 (0.1–0.2 N) 이 벽 쪽으로 (원심력) [인쇄 p.5474].
- **Fig 11** (앞 날 면을 지나는 수직 단면 Y 5–55 mm): 큰 법선력이 앞 날과 벽의 모서리 · 특히 바닥에 모인다 → *"these forces can be reduced if the blade is lifted above the bottom of the mixer. Such a provision will help reduce particle breakage during mixing."* · 앞 더미 ↑ · 뒤 더미 ↓ · 날을 넘는 입자 ↑ · *"At 100 rpm, the particles build up twice as high as the blade height, which is 40 mm."* [인쇄 p.5475].
- 스냅숏 회전: 2 rpm **5.24** · 23.87 rpm 20.09 · 47.75 rpm 21.88 · 100 rpm 21.66 회전 [인쇄 캡션] — 2 rpm 은 회전이 적다 (5.24 회전 = 157 s = 그 런의 끝 [카드 산술]).
- **분포 범위** (p.5475 · `txt_p09_normal_1e-4_0p3N_shear_1e-4_0p1N_breakage.png`): 법선 **10⁻⁴–0.3 N** · 접선 **10⁻⁴–0.1 N** (2–100 rpm) · 속도 ↑ 면 누적 분포가 큰 힘 쪽으로 · *"By definition, the tangential force is proportional to the normal force between particles. It is therefore not surprising that Figures 12 and 13 are similar."* · 큰 힘 지역 = *"These are the regions where stress concentration occurs, possibly leading to particle breakage and severe attrition."* [인쇄].

| 누적 확률 | 법선 2 rpm | 법선 47.75 | 법선 100 | 접선 2 rpm | 접선 47.75 | 접선 100 |
|---|---|---|---|---|---|---|
| 0.5 (중앙) | 6.0 × 10⁻³ | 7.9 × 10⁻³ | 1.04 × 10⁻² | 1.27 × 10⁻³ | 1.71 × 10⁻³ | 2.33 × 10⁻³ |
| 0.9 | 3.4 × 10⁻² | 4.2 × 10⁻² | 5.5 × 10⁻² | 6.7 × 10⁻³ | 8.3 × 10⁻³ | 1.16 × 10⁻² |
| 0.99 | 0.101 | 0.131 | 0.159 | 2.1 × 10⁻² | 2.7 × 10⁻² | 3.7 × 10⁻² |

[판독 Fig 12a · 13a · 로그 축 행 추적 · 단위 N] · 세 곡선은 누적 0.1 (≈ 9 × 10⁻⁴ N) 근처에서 엇갈린다 [판독].
- **평균** (Fig 12b · 13b · 선만 있고 표지 없음): 법선 0.0137 (2) · 0.0139 (10) · 0.0147 (20) · 0.0176 (50) · **0.0222 N (100 rpm)** (+62 %) · 접선 0.00279 → **0.00490 N** (+76 %) [판독] · 그 선 밑의 런 수 [미확인].
- [카드 산술] 평균 접선/법선 = 0.204 (2 rpm) · 0.221 (100 rpm) < μ_s 0.3 · 2 rpm 평균 법선력 0.0137 N ≈ 입자 무게의 8.5 배 ≈ 깊이 40 mm 고체 기둥 (고체분율 0.55) 의 무게를 d² 에 나눈 0.0135 N — **저속 힘은 중력 (누르는 무게) 크기** [어림].

### 3-8. 토크 · 에너지 (Fig 14 · p.5475–5476)

- 원문 (`txt_p10_torque_fit_1p086_exp_0p0047w_zhou_1p1nm.png`): 정상 날 토크 vs 속도 · *"Zhou et al.9 have reported a torque of 1.1 N m at 10 rpm for the simulation conditions identical to those of this work."* · 저속에서 점근 · 100 rpm 까지 지수 증가 (100–600 rpm 에서는 선형일 수 있음 · Sato 2008) · **Γ = 1.086 e^{0.0047ω}** (Γ in N m · ω in rpm) · *"This relationship predicts a torque of 1.086 N m at zero blade speed, which can be thought as the threshold torque required for the blade to move the particles in the mixer overcoming various frictional forces present."* · Knight 2001 반해석 모델은 *"not directly applicable here because it does not account for the particle size and empirical constants of the model are not known for this mixer configuration"* [인쇄].
- [판독 Fig 14 · 표지 중심 · 로그 x] 1.120 (2) · 1.135 (9.55) · 1.197 (23.87) · 1.333 (47.75) · 1.762 N m (100 rpm) · 맞춤 대비 +2.2 · −0.1 · −1.5 · −1.9 · +1.4 % [카드 산술] · 9.55 rpm 1.135 ≈ Zhou 의 10 rpm 1.1 N m.
- **에너지** (`txt_p10_energy_27p6_vs_65p5J_58pct_33x_time.png`): 토크는 평균 둘레로 흔들림 (*"Although not shown here"*) → 에너지 = 토크 × 날이 쓸고 간 각 · *"the energy consumed in four and six revolutions at 2 and 100 rpm respectively is 27.6 and 65.5 J, respectively; an energy saving of 58% can be achieved by choosing 2 rpm over 100 rpm, though the mixing time increases by 33 times"* · 고속에서는 열 발생도 손실 [인쇄 p.5476].
- [카드 산술 · 재현] Γ(2)·8π = **27.55 J** · Γ(100)·12π = **65.51 J** (맞춤식 값 — 인쇄 27.6 · 65.5 를 정확히 재현 = 맞춤식으로 계산했다) · 판독 표지값이면 28.15 · 66.43 J (57.6 %) · 시간 비 (4/2)/(6/100) = 33.3.

### 3-9. 카드 산술 묶음 (이 논문 숫자만으로 · 식 병기)

① **Hertz 동치** — E(2R_i)^{1/2}/(3(1−ν²)) = (4/3)·[E/(2(1−ν²))]·(R_i/2)^{1/2} = 55,947 N m^{−3/2} (E 2.16 × 10⁶ Pa · R_i 2.5 mm · ν 0.3).
② **E 를 ÷463 했을 때** — 같은 힘에서 겹침 δ = (F/K)^{2/3} ∝ E^{−2/3} → ×**59.9** · 접촉 반지름 a = √(R*δ) ∝ E^{−1/3} → ×7.7 · Hertz 충돌 시간 t_c = 2.87(m*²/(R*E*²v))^{1/5} ∝ E^{−2/5} → ×**11.6** · 반발계수 = 0.251 그대로 (§3-2) · 겹침 (인쇄 법선 식 · 연화 E): 평균력 0.0137 N → 39 µm (**0.78 % d**) · 0.0222 N → 54 µm (1.08 % d) · 99 % 분위 0.101–0.159 N → 148–201 µm (3.0–4.0 % d) · 최대 0.3 N → 306 µm (**6.1 % d** — 5 % 간격 기준보다 크다) · E = 10⁹ 이면 0.0137 N → 0.65 µm (0.013 % d).
③ **시간 간격** — Rayleigh 간격 πR√(ρ/G)/(0.1631ν + 0.8766) = 466 µs (연화) · 21.6 µs (10⁹) → 인쇄 54 µs 는 Rayleigh 가 아니다 · Hertz 충돌 시간 (v 0.5–1.3 m/s) = 1.08–0.89 ms (연화) · 93–77 µs (10⁹) · t_c/20 = 54.1 µs at v = 0.5 m/s (우연일 수 있음 · 원문 식 [미확인] — refs 21 · 22) · dt 5 µs = 충돌 하나에 179–216 걸음 (50 µs 면 18–22) · 54 µs 를 E = 10⁹ 로 옮기면 ×(2.16 × 10⁶/10⁹)^{0.4} = **4.6 µs** (t_c 축척) 또는 ^{0.5} = 2.5 µs (Rayleigh 축척) → **실제로 쓴 5 µs 는 연화하지 않은 E 가 요구할 간격과 비슷하다** (연화의 '시간 절약' 은 dt 50 → 5 µs 로 다시 쓰였다 [카드 추론]).
④ **구름 계수** — μ_r/R = 5 × 10⁻⁵/2.5 × 10⁻³ = 0.02 · μ_r/R* = 0.04.
⑤ **접선 한계 변위** — δ_t,max/δ_n = 0.3 × 1.7/1.4 = 0.364.
⑥ **법선 감쇠의 부호** — n̂ = **R**_i/R_i 는 i 중심에서 접촉점 (j 쪽) 을 향한다 · **V**_ij = **V**_j − **V**_i (+ 회전 항) · 다가올 때 (**V**_ij·n̂) < 0 → 인쇄 식 −c_n(…)(**V**_ij·n̂)n̂ 은 **+n̂ (j 쪽)** 을 향해 다가옴을 돕는다 (에너지를 넣는 방향).  접선은 (**V**_ij × n̂) × n̂ = −(**V**_ij)_t 라 −c_t(…)**V**_t,ij = +c_t(…)(**V**_ij)_t → 소산 방향.  ⇒ 같은 표 안 두 감쇠 식의 부호 규약이 서로 다르다 — 하나는 지면 오식 [카드 산술 · 부호 검사] · 반발계수는 소산 방향으로 계산했다.
⑦ **칸** — §3-3 (칸 넓이 · 칸당 입자 · E[S²] = pq/N̄).
⑧ **Froude · 끝 속도** — §3-4 · §3-1 (인쇄값 0.32 · 1.4 · 15.5 · 0.62 · 1.3 · 1.31 · 4.65 m/s 재현).
⑨ **에너지** — §3-8 (인쇄 27.6 · 65.5 J = 맞춤식 값).
⑩ **회전수** — Fig 2 · 3 스냅숏 4.33 · 21.9 · 21.9 · 22.2 · Fig 10 · 11 의 2 rpm 5.24 회전 = 157 s = 2 rpm 런의 끝 (Fig 6a) · M ≥ 0.95 시간 = 2 rpm 108.6 s ↔ 100 rpm 4.58 회전 = 2.75 s.
⑪ **우리 드럼과의 Froude** — 우리 믹서 드럼 Fr 0.0827 [정본 카드 표기 — 2012 카드 §7] 을 같은 Dω²/(2g) 로 이 믹서 (D 0.249 m) 에 옮기면 ≈ 24 rpm.  ⚠ 축 방향이 다르다 (수직축 날 믹서 = 원심 ↔ 중력이 직교 · 수평 드럼 = 같은 면) → 같은 수라도 흐름 체제 문턱의 뜻이 다르다 [카드 추론] · 우리 드럼 Fr 의 정의식 [미확인 · 정본 카드에 없음].
⑫ **연화 크기 비교** — 이 논문 2.16 MPa 는 우리 믹서 SE 1 × 10⁷ Pa 보다 4.6 배 무르고 (2012 카드 §3-9 ⑦ 과 같은 비) 우리 압축 DEM SE E_eff 1.35 GPa 보다 625 배 무르다 [지시서 · 정본 카드 표기].

---

## 4. ★ 방법 — DEM · 지수 · 배위수 · 힘 · 입자 처리

### 4-1. DEM (p.5468)
자체 DEM · *"developed previously,9,12, extending the original DEM model proposed by Cundall and Strack8 by accounting for the rolling friction of particles"* · 병진 · 회전 운동량 식 (1)–(2) · 힘 · 토크 = Table 1 (§3-2) · 벽 · 날 = 입자 물성 · 공기 무시 · dt 5 µs · 일정 각속도 회전 (가속 구간 없음).  적분법 · 이웃 탐색 · 병렬 · 비용 [미확인].

### 4-2. 지수 · 칸 (p.5471)
Lacey (식 3) + 칸 입자 수 가중 분산 (식 4 · 편차는 기대 분율 p 기준 — 칸 평균 기준이 아니다) · 칸 = 고리 × 부채꼴 × 20 mm 층 (§3-3) · 장입 = 좌우 반 · 입자 분율 = **개수** 분율 (단분산이라 부피 분율과 같음).  무작위 기준 = 이항 (색만 다른 입자) · 크기 다른 혼합물에는 부적용 (저자).

### 4-3. 배위수 · 공극 (p.5470 · 5472)
간격 1 % · 5 % d · 벽 · 날 접촉 포함 · 빈도 분포 평균 · 부분 배위수 W–W · B–B · B–W · W–B (중심 종 – 이웃 종) · B–W / 전체 비 (순간 평균끼리) · 공극 = 두 수평 단면 사이 (Fig 4 = 0–40 mm 고정 슬랩 — 날 뒤 빈 곳 · 더미가 날 윗변을 넘은 몫이 섞인다 [카드 추론]).

### 4-4. 힘 망 · 분포 · 토크 (p.5474–5476)
법선력 = 선 굵기 · 색 4 구간 · 수평 (Z 0–10 mm) · 수직 (Y 5–55 mm) 단면 · 법선 · 접선 접촉력 누적 분포와 평균 · 정상 날 토크 (평균) · 에너지 = 토크 × 쓸고 간 각.  속도 셀 (Fig 9) = r > 80 mm · θ 0–π 15 칸 · 정상 상태 날 상대 속도 평균.

### 4-5. ★ 입자 처리 (우리 축 언어로)
- **강체 구 · 점접촉 (겹침 허용 soft-sphere)** · 비점착 · 탄성 (Hertz 꼴) + 점성 감쇠 + 방향 일정 구름 토크 · **소성 없음 · 형상 불변 · 파괴 없음** (파괴 '가능 지역' 을 힘으로 지목만).
- 단분산 5 mm · 색만 다른 두 무리 (분리 구동력 0) · 같은 물성의 벽 · 날.
- 날 속도마다 **런 1 회** — 시드 · 장입 무작위성 산포 없음.

### 4-6. ★ 네 항목 (CURATOR_BRIEF 5 의 (i)–(iv))
- **(i) DEM (단단한 구 · 점접촉) 의 한계를 말한 문장**: 구 · 점접촉 자체에 대해서는 **말 없음**.  닿는 문장 = ① 연화 E 고백 (p.5473 · §0-1 · §3-6) ② *"coordination number >12 is possible because of the (5%)d gap allowance used here"* (p.5472) ③ 배위수 · 공극은 *"difficult to produce experimentally"* (p.5470) ④ 입자 크기 효과를 못 담는 토크 모델 (Knight) 은 적용 불가 (p.5476) ⑤ 결론 (f) *"Many of the effects due to particle size and cohesive force will also become equally accessible"* (p.5477 · `txt_p11_conclusion_f_size_cohesive_future.png`) — 크기 · 점착은 **앞으로** 의 일.
- **(ii) 입자의 소성 · 큰 변형이 어려운 이유와 우회 · 비용**: **말 없음** — 소성을 넣으려 하지 않았다.  쓴 우회 = E 연화 (÷463 · **시간 간격 목적** · 소성 대리 아님) · 맞춘 값 0 (E 는 선행 연구의 *"reliable results"* 로 정당화) · 검증 = 선행 PEPT (ref 10) · 비용 [미확인].
- **(iii) 2D / 3D**: **3D DEM** (원통 · 16,000 구) · 2D → 3D 전이에 대한 말 없음 · 'three dimensional' 은 입체각 최대 이웃 수 (14) 문장과 결론 (b) *"three-dimensional vortex"* 에만.
- **(iv) 압력을 뺄 때의 거동**: **없음** — 압축 · 하중 제거가 없다 (날 회전 혼합만).

### 4-7. 기법 미니 용어집
- **날 상대 속도 (blade relative velocity)** — 날과 함께 도는 틀에서 본 속도 (ω × r 을 뺌) · 끝 속도로 나눔.
- **토로이드 운동 (toroidal motion)** — 벽 근처에서 오르고 가운데로 떨어지는 도넛 모양 순환 (Nilpawar).
- **Froude 수 Fr = Dω²/(2g)** — 원심 가속 / 중력 (이 논문 정의).
- **전이 구간 (transition region of mixing)** — 혼합 곡선 가운데 부분 (정의 없음 · 그림 6b 의 M ≈ 0.4–0.9 쯤으로 쓰임 [카드 추론]).
- **부분 배위수** — 중심 종 × 이웃 종 접촉 수 (W–B 와 B–W 는 다름) · 조건부 평균 (§3-5).
- **문턱 토크 (threshold torque)** — 맞춤식의 0 rpm 값 1.086 N m.
- **힘 망 (force network)** — 법선력을 선 굵기로 그린 접촉 그래프.

---

## 5. Figure set ★ (크롭 45 장 = `litdb/figures/chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer/`)

| Fig | 내용 | 크롭 | 우리 활용 |
|---|---|---|---|
| 1 | (a) 믹서 기하 (지름 249 · 높이 100 · 축 32 · 날 40 × 10 mm · α) (b) 20 rpm 침대 모양 · 흐름 화살표 | `fig_1.png` | 기하 · 날 앞 더미 |
| 2 | 수평 단면 (Z 10 · 35 · 60 mm) 날 상대 속도장 · 2 / 23.8 / 47.75 / 100 rpm | `fig_2.png` | 끝 속도 정규화 · 날 상대 틀 (드럼 판독에도 같은 꼴 가능) |
| 3 | 원통 단면 r = 50 · 100 mm 속도장 | `fig_3.png` | 축 근처 재순환 ↔ 벽 근처 한 방향 |
| 4 | 배위수 (5 % · 1 % 간격) · 공극 (0–40 mm) vs 날 속도 | `fig_4.png` | ★ 간격 기준이 배위수를 ≈ 1 바꾼다 · 고정 슬랩 공극 |
| 5 | 37.5 mm 단면 좌우 장입 혼합 (2 · 47.7 · 100 rpm) | `fig_5.png` | 100 rpm 날 뒤 빈 공간 |
| 6 | Lacey M vs 시간 (a) · 회전수 (b) — 2 · 9.55 · 47.75 · 100 rpm | `fig_6.png` | ★ 시간 ↔ 회전수 축 · 평탄값 ≈ 0.98–0.99 |
| 7 | 부분 배위수 vs 회전수 — 10 · 100 rpm | `fig_7.png` | 조건부 평균 함정 (6 + 2 = '8') · 시동 팽창 |
| 8 | B–W 배위수 (a) · B–W / 전체 (b) vs 회전수 | `fig_8.png` | ★ 연화 고백이 걸린 그림 |
| 9 | r > 80 mm 15 칸 V_z/V_θ · V_r/V_θ vs θ — 9.55 · 47.75 · 100 rpm | `fig_9.png` | 토로이드 판별 (Fr 1.4) · (a) 에 정의 없는 곡선 번호 '4' |
| 10 | 수평 단면 Z 0–10 mm 법선력 망 (색 4 구간) | `fig_10.png` | R7 '위치' 보고 꼴 |
| 11 | 앞 날 면을 지나는 수직 단면 법선력 망 | `fig_11.png` | 날 · 벽 · 바닥 모서리 집중 · 100 rpm 더미 80 mm |
| 12 | 법선 접촉력 누적 분포 (2 · 47.75 · 100 rpm) · 평균 vs 속도 | `fig_12.png` | 힘 분위 보고 꼴 |
| 13 | 접선 접촉력 누적 분포 · 평균 vs 속도 | `fig_13.png` | — |
| 14 | 정상 날 토크 vs 속도 (로그 x) | `fig_14.png` | 토크 → 혼합 에너지 계산 꼴 |
| Table 1 | 힘 · 토크 식 여섯 + 딸린 정의 | `tab_1.png` + `eq_t1a` … `eq_t1f` | ★★ 이 카드의 의도 (§3-2) |
| 식 1–4 | 운동 식 둘 · Lacey · 칸 가중 분산 | `eq_01` … `eq_04` | §3-2 · §3-3 |
| 본문 근거 20 | 카드가 인용한 문장 (`txt_p01` … `txt_p11` · 아홉은 두 단 · 두 쪽을 이음) | `txt_p<NN>_<뜻>.png` | §0-1 · §3 · §9 |

## 6. Post-processing ★
- **무엇을**: 수평 · 원통 단면 날 상대 속도 · 배위수 (간격 둘) · 공극 (슬랩) · Lacey M (칸 80 × 층) · 부분 배위수 · B–W / 전체 · 바깥 원통 15 칸 속도 비 · 힘 망 · 접촉력 누적 분포 · 평균 · 정상 토크 · 에너지.
- **도구**: 자체 DEM 후처리 (이름 없음).
- **안 한 것**: 런 반복 · 시드 산포 · 칸 크기 사다리 · 간격 기준을 Lacey 쪽과 함께 바꾸기 · S_R² 의 N 선택 공개 · 실험 대조 (이 논문 안) · E 민감도 (연화 고백만 있고 실험하지 않음) · 점착 · 크기 · 밀도 차.
- **우리 후처리 (이 카드)**: §3-9 ①–⑫ · 판독 Fig 4 · 6 · 7 · 8 · 9 · 12 · 13 · 14 (digitized.csv 241 행 · 표지 상자 중심 · 화소 열 · 행 추적 · 색 마스크 · 프레임 선과 눈금 보정 · 12a · 13a · 14 는 로그 축).

---

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md` (⚠ 정본 가지에서는 값 자리표시 상태 — 우리 수치는 지시서 · 다른 정본 카드 · CLAUDE.md (메인 리포) 출처를 병기)

| 항목 | 이 논문 (Chandratilleke 2010) | 우리 | 차이 / 판정 |
|---|---|---|---|
| 혼합 장치 | 2 날개 **수직축** 원통 · 2–100 rpm · Fr 0.0006–1.4 | **회전 드럼** · CGF 151.4 · Fr 0.0827 [정본 카드 표기 — 2012 카드 §7] | 흐름 기전이 다르다 (날 대류 ↔ 드럼 굴림) · 같은 Fr 꼴의 뜻도 다름 (§3-9 ⑪) |
| 점착 | 없음 | 쌍별 CED (SJKR) [2012 카드 §7] | 우리 질문 (코팅 · 응집) 은 범위 밖 |
| 입자 | 단분산 5 mm · 색만 다름 | SE · AM_S · AM_P (크기비 1 : 4 : 9) | 분리 구동력 0 ↔ 크기 · 밀도 차 큼 |
| 강성 | E 10⁹ → 2.16 × 10⁶ Pa (÷463 · 시간 간격) | 믹서 SE 1 × 10⁷ · AM 1.037 × 10⁹ Pa (÷135) [2012 카드 §7] · 압축 DEM SE 24 → 1.35 GPa (÷18 · 기공 보정) [지시서 · CLAUDE.md frame [2]] | 같은 '연화' 라도 목적이 다르다 (시간 간격 ↔ 기공 보정) — 배수 전이 금지 |
| 접촉 법칙 | Hertz 꼴 법선 · Mindlin–Deresiewicz 꼴 접선 · δ^{1/4} 감쇠 · 방향 일정 구름 토크 (자기 ω_i) | 압축 = hooke/hysteresis [지시서] · 구름 = cdt (A 부류 꼴 [ai2011 카드]) · 믹서 접촉 법칙 [미확인 · 이 카드에서 대조 안 함] | 법선 · 감쇠 꼴 차이는 겹침 · 반발에 걸린다 |
| 혼합 지수 | Lacey · S₀² = pq (이론) · S_R² = pq/N (이항) · S² 는 입자 수 가중 · p 기준 편차 · 칸 ≈ 600 mm² × 20 mm (≈ 67–101 개) | Lacey · S₀² = 런 자신의 t₀ · S_R² = 균일 삽입 런 실측 · 칸 16×16×4 (n_eff ≈ 3.6–3.7) · AM 부피분율 · 같은 무게 [2012 카드 §7 · 비교 문서 §H] | ★ 네 칸이 다 다르다 — 같은 이름 · 다른 연산자 (§8-2 ①) |
| 혼합 끝 | M 평탄 ≈ 0.98–0.99 · 4–6 회전 [판독 · 인쇄] | 층상 L 10 런 = 8 바퀴 뒤 M 0.96–1.00 · '이 칸 규모에서 가를 해상도 없음' (CLAUDE.md 현재 상태 표 · 믹서 층상 09-30) | 둘 다 1 근처 차이를 다룬다 — 이 논문은 산포 없이 '4 ↔ 6 회전' 을 말한다 |
| 접촉 지표 | 배위수 (간격 1 · 5 %) · 부분 배위수 · B–W / 전체 | s1 (SE–SE 군집) · s2 (AM–SE 부착) [2012 카드 §7] | 저자 스스로 접촉 비가 연화 E 에 민감하다고 적음 → 우리 s1 · s2 도 같은 위험 |
| 압축 · 탈압 | 없음 | 혼합 → 압축 DEM (300 MPa) → 망 σ | frame[5]: 이 논문은 **혼합 흐름 · 힘 지표** 반쪽만 |
| 반복 | 속도마다 1 런 | 시드 3 (본 캠페인) [2012 카드 §7] | — |

### 7-1. frame[5] — 어느 반쪽을 가졌나
DEM **흐름 · 혼합 통계 · 접촉력 분포** 만.  점착 · 압축 · 전달 · 형상 소성은 없다 → 우리 파이프라인 첫 단계 (혼합 → 압축 초기 배치) 의 **관측량 정의 · 보고 방식** 과 **연화의 쓰임새 대조** 에 쓴다.

### 7-2. ★ 랩 기준과 나란히 (판정 없이 · **랩 표준과 다른 문헌 값 = 다른 재료 · 다른 상태**)

| 양 | 랩 기준 (고정 · 판정 안 함) [지시서] | 이 논문 | 차이 |
|---|---|---|---|
| 순수 SE 기공률 | 10–13 % (눌린 상태) | 흐르는 단분산 mm 구 침대의 고정 슬랩 공극 0.45 (정지) · 0.54–0.63 (2–100 rpm) [판독] | 재료 (유리 유사) · 상태 (무압축 흐름 · 날 뒤 빈 곳 포함) · 정의 (슬랩) 가 다 다르다 — 견줄 수 없다 |
| 진밀도 | LPSCl 1.64 g/cm³ | 입자 밀도 2.50 g/cm³ (2500 kg m⁻³ · 유리 유사) | 랩 표준과 다른 문헌 값 (다른 재료) |

### 7-3. ★ 18 배 연화와 견줄 자리 (frame [2])
- **우리**: 압축 DEM SE E 24 → E_eff 1.35 GPa (÷18) — 단단한 구 DEM 이 못 담는 재배열 · 입계 미끄럼 · 미세 파괴를 탄성률 하나에 묶어 300 MPa 에서 기공을 실험에 맞춘다 (보정값 · Heckel P_y 138 MPa) [지시서 · 'SE 24' 와 묶음 해석 = CLAUDE.md frame [2]].  MPM 은 E 1.53 · σ_y 0.30 · ν 0.49 [지시서].
- **이 논문**: ÷463 은 **계산 시간 (dt)** 을 위해서이고 맞춘 대상이 없다 — 흐름 · 혼합 결과가 PEPT 와 맞는다는 선행 연구로 정당화 (refs 9 · 12).  흐르는 침대에서 접촉력은 중력 · 운동량이 정하므로 (§3-7 끝 어림) 연화가 바꾸는 것은 주로 **겹침 (×59.9) · 충돌 시간 (×11.6) · 접촉으로 세는 수** 다 — 그래서 저자도 접촉 비 하나를 연화 탓으로 돌린다 [카드 추론].
- ⇒ 같은 '연화' 라는 말 아래 **보정 (우리 압축) ↔ 속도 (이 논문 · 우리 믹서)** 두 목적이 있다.  압축에서는 겹침이 곧 기공 (보정 대상) · 흐름에서는 겹침이 인공물 (≈ 1 % d) — 연화 배수를 서로 옮기지 않는다.

---

## 8. ★★ 자세한 분석 — 우리 계획에 무엇을 주나

### 8-1. 계획의 이름별 (정독 지시서 3 절 · 주는 것 / 못 주는 것)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 차이 |
|---|---|---|
| 단계 0 (기공 연산자 · 판정 기준 결과 전) | ★ 정의 함정 둘: ① 고정 슬랩 (0–40 mm) 공극에 날 뒤 빈 곳 · 넘친 더미가 섞인다 → 제어 부피를 명시해야 ② 배위수가 간격 기준 (1 ↔ 5 % d) 에 ≈ 1 · 벽 · 날 접촉 포함 여부에 걸린다 → 간격 · 벽 포함을 결과 전에 | 압축 기공 값 없음 |
| 단계 1 (입자별 속도장 3D 메모리) | 없음 | — |
| 단계 2 (2D MPM 코드 · 단위 시험) | 없음 | — |
| 단계 3 (2D 접촉 표현만 바꿔 누르는 힘 비교) | 없음 | — |
| 단계 4 (3D 순수 SE 붓기 · 누르기 · σ_y 맞춤) | 붓기 절차 하나 (겹침 없는 무작위 배치 → 중력 정착 0.95 s → 정지 침대 공극 ≈ 0.45) | 단분산 mm 유리 유사 구 · 압축 없음 — 순수 SE 기준 (10–13 %) 과 상태가 다르다 |
| 단계 5 (3D 복합 압축) | 없음 | — |
| 단계 6 (탈압 · 되돌아옴) | 없음 | — |
| 단계 7 (눌린 구조의 형상 · 피복 · 수송) | 접촉력 분포 (누적 분위) · 힘 망 그림의 보고 꼴 · 부분 배위수 (조건부 평균) 함정 | 눌린 구조 아님 · 수송 없음 |
| 후보 D0 (지금의 DEM) | ★ 같은 계열 (soft-sphere · Hertz 꼴 · 구름 A 부류) 의 연화 선례 (÷463 · 시간 간격) · 연화가 접촉 기반 지표를 바꾼다는 저자 고백 (p.5473) | 압축 · 점착 · 다분산 없음 · 맞춘 값 없음 |
| 후보 A′-0 · A · A′ · B | 없음 (MPM · FE 없음) | — |
| 후보 C (큰 변형 접촉 MDR) | 없음 — 겹침 ≤ 6 % d (최대 힘 · 연화) 의 흐름 영역 | — |
| 후보 C′ (항복 캡 탄소성 접촉) | 없음 (탄성 + 점성) | — |
| 후보 M0 (균질화 압밀) | 없음 | — |
| U2 (경사면 마찰 회귀) | 구름 토크 꼴 = 방향 일정 (A 부류) · 자기 ω_i 기준 → ai2011 이 보인 정지 상태 2Δt 토크 진동이 같은 꼴에서 생길 수 있다 [카드 대조] — cdt 정지 시험의 기준 문헌 짝 | 이 논문은 정지 · 경사 시험을 하지 않았다 |
| U5 (비슷한 강성 입자끼리 충돌) | Table 1 법선 식 + 감쇠 식이면 두 구 정면 충돌의 접촉 시간 · 최대 겹침 · 반발계수 (e ≈ 0.25 · 속도 · E 무관) 를 해석 · 수치로 낼 수 있다 (§3-2 · §3-9 ②–③) — 탄성 충돌 비교 기준 | 작은 변형 · 탄성 · 단분산만 · 원문은 반발계수를 적지 않음 |
| U0 · U1 · U3 · U4 · U6 | 없음 | — |
| R1 (AM 이 움직이며 하중 분담) | 없음 | — |
| R2 (미끄럼 · 분리) | 접선 = μ_s F_n 상한 · δ_t,max = 0.364 δ_n 의 미끄럼 규약 | DEM 쪽 규약 — MPM 접촉과 직접 대응 없음 |
| R3 · R4 · R5 · R6 | 없음 (R5: 맞춘 값 0 · R6: 형상 불변) | — |
| R7 (AM 파괴) | 큰 힘 지역의 **위치** (날 앞 · 바닥 · 벽 모서리) · 분포 분위 · 날을 띄우면 줄어든다는 설계 문장 | 파괴 모델 없음 · 힘이 연화 E 로 계산됨 (충돌 최대 힘은 E 에 걸린다 — §10 ⑰) |
| 결과 전 대조 항목 | 없음 (우리 재료 · 상태의 외부 값이 없다) | — |

### 8-2. 받아들일 통찰 (번호마다: 논문이 보인 것 → 우리에게 뜻 → 할 일)

1. **Lacey 연산자의 네 칸을 결과 전에 적는다.**  이 논문 = 분리 기준 이론 pq · 칸 입자 수 가중 · 편차 기준 = 기대 분율 p · 무작위 기준 이항 pq/N (칸 ≈ 70–100 개).  우리 = 런 t₀ 실측 · 같은 무게 · 칸 평균 · 균일 삽입 런 실측 (n_eff ≈ 3.6–3.7).  → [DEM 우선] Ⓒ 확인 블록의 등록 · 보고에 이 네 칸을 문헌 값 옆에 같이 적는다 (같은 'Lacey' 라도 숫자를 나란히 놓지 않는다).
2. **팽창은 칸 지수를 흔든다 — 무작위 기준을 같은 흐름 상태에서 재야 하는 이유.**  저자의 설명 (공극 ↑ → 칸 입자 ↓ → S² ↑ → M ↓) 은 S_R² 를 고정했을 때의 이야기 (§3-3 · §3-6) · 우리 S_R² = 같은 흐름의 균일 삽입 런 실측은 이 효과를 기준 쪽에 넣는다.  → 속도 · 회전수가 다른 팔을 견줄 때 **칸 점유 (입자 수 / 칸) 를 지수와 함께 보고** 한다.
3. **시간 · 회전수 · 에너지 세 축으로 보고한다.**  같은 결과가 시간으로는 '빠른 날', 회전수로는 '느린 날', 에너지로는 '느린 날 (58 % 절감 · 시간 33 배)' 이 된다.  → 믹서 팔 (V2 시간 · 에너지) 보고 축을 셋으로 고정한다.
4. **연화 E 는 접촉 기반 지표를 바꾼다 (저자 고백).**  100 rpm 정상 B–W 비 +2.8 % 를 저자 스스로 *"softer particles"* 탓으로 돌린다 (p.5473).  → 우리 s1 · s2 · 배위수 같은 접촉 지표는 **E 사다리 또는 간격 (판정 거리) 사다리** 를 결과 전 등록에 넣는다 (2012 카드 Fig 7 의 간격 민감도와 함께 인용).
5. **배위수 정의 = 간격 + 벽 포함 + 조건부 여부.**  1 ↔ 5 % d 에 배위수 ≈ 1 차이 · 5 % 허용이면 > 12 가능 · 부분 배위수의 조건부 평균은 '6 + 2 = 8' 같은 합을 만든다.  → 단계 0 · 7 의 접촉 수 보고에 셋을 표지로 단다.
6. **E 와 dt 를 같이 바꾼 비교는 교락이다.**  선행 (dt 50 µs · < 40 rpm) 의 '한 곡선' 과 이 논문 (dt 5 µs · 2–100 rpm) 의 '한 곡선 아님' 은 두 가지가 같이 바뀐 비교 · 실제로 쓴 5 µs 는 연화 안 한 E 가 요구할 간격과 비슷하다 (§3-9 ③).  → 우리 Phase A 재현의 'E + dt 세대 전환 효과' (CLAUDE.md 현재 상태 표 · 09-30) 와 같은 구조 — 한 번에 하나만 바꾼다.
7. **흐르는 침대의 접촉력은 중력 · 운동량 크기, 연화는 겹침을 바꾼다.**  2 rpm 평균 법선력 ≈ 깊이 40 mm 고체 기둥 무게 / d² (§3-7) · 연화 E 의 겹침 0.8–1.1 % d (최대 6 % d).  → 우리 믹서 DEM (SE 1 × 10⁷ Pa) 에서도 접촉 판정 거리 · 덤프 반올림과 겹침 크기를 같은 표에 두고 판정한다 (흐름 밖: 믹서 판독).
8. **힘 지도의 '위치' 보고 꼴 (R7 쪽).**  색 4 구간 힘 망 + 분위표 + 큰 힘 지역의 기하 (날 · 벽 · 바닥 모서리) · 설계 처방 (날을 띄움).  → 우리 R7 판정 보고에 AM 입자별 최대 접촉력 분위 + 위치 지도를 같이 (단 연화 모델의 충돌 힘은 하한 쪽 — §10 ⑰).

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In a two-bladed vertical cylindrical mixer DEM (16,000 monosized 5 mm spheres), the Young's modulus was reduced from 10⁹ to 2.16 × 10⁶ Pa to reduce computational time, and the contact law used a δ_n^{3/2} normal force, a μ_s-capped tangential force, nonlinear viscous damping and a constant-magnitude rolling-friction torque (Chandratilleke et al., Ind. Eng. Chem. Res. 2010, Table 1)." [인쇄 p.5468]
- "At 2 rpm the Lacey index reached the fully mixed state in four blade revolutions compared with six at 100 rpm, while 2 rpm required about 58 % less energy but 33 times longer mixing time." [인쇄 p.5471 · p.5476]
- "The authors attributed a slight rise of the steady-state B–W contact ratio at 100 rpm to the softened particles: a larger Young's modulus would give fewer particle deformations and fewer contacts." [인쇄 p.5473]
- "Normal contact forces ranged from 10⁻⁴ to 0.3 N and tangential forces from 10⁻⁴ to 0.1 N over 2–100 rpm, with the largest forces in front of the leading blade near the bed bottom, moving toward the wall at higher speed." [인쇄 p.5474–5475]
- ⚠ "M = 1" 은 판독 평탄값 ≈ 0.98–0.99 · "4 ↔ 6 회전" 은 속도마다 런 1 회 — 산포 없는 차이로 인용.  e ≈ 0.25 · 54 µs = t_c/20 · 연화 안 한 E 의 간격 4.6 µs 는 카드 산술 (원문 값 아님).

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **단분산 · 비점착 · 유리 유사 mm 구 · 공기 무시** — 점착 응집 · 크기 · 밀도 차 · µm 분말 · 회전 드럼으로 결과 전이 금지.
2. **실험 값이 이 논문 안에 없다** — *"validated against the PEPT measurements as detailed by Stewart et al."* 는 선행 논문 (ref 10) 의 검증이다.
3. **속도마다 런 1 회** — '4 ↔ 6 회전' (판독 M 0.95 에서 3.70 ↔ 4.58 · 0.97 에서 4.18 ↔ 5.00) 의 산포 없음 · 평탄값 ≈ 0.98–0.99 근처의 차이.
4. **법선 감쇠 부호** — 인쇄 그대로면 다가올 때 에너지를 넣는 방향 · 접선 감쇠와 규약이 반대 (§3-9 ⑥) — 지면 오식 하나 [카드 산술].
5. **접선 식의 \|δ_i\|** — 정의 안 된 기호 · \|δ_t\| 의 오식으로 읽힌다 [카드 추론].
6. **법선 감쇠의 R (첨자 없음) 미정의** · m_i 가 입자 질량인지 환산 질량인지 표에 없음 → 반발계수 0.25 ↔ 0.39 (해석 둘 · §3-2).
7. **법선 식은 같은 크기 두 구 꼴** (2R_i)^{1/2} — 벽 · 날 (평면) 접촉의 꼴 [미확인] (같은 꼴이면 Hertz 대비 √2 배 차이).
8. **54 µs 의 식 없음** (refs 21 · 22) — Rayleigh (466 µs) 는 아니다 · t_c/20 at 0.5 m/s 와 같은 값 (우연일 수 있음).
9. **'실제 유리구 10⁹'** — 인쇄값 그대로 · 통상 유리 영률보다 낮아 보인다 (2012 카드 §3-9 ⑦ 의 [추정] 과 같은 의문 · 이 카드도 수치를 덧붙이지 않는다).
10. **속도 표기 불일치** — 47.75 · 47.7 (Fig 5) · 47.5 (p.5473 본문) · 23.87 · 23.8 (Fig 2 · 3) · Fig 7a '10 rpm' 이 9.55 rpm 런인지 [미확인].
11. **스냅숏 회전수가 다르다** — Fig 2 · 3 의 2 rpm = 4.33 회전 ↔ 다른 속도 ≈ 22 회전 · Fig 10 · 11 의 2 rpm = 5.24 ↔ 20–22 회전 (2 rpm 런 끝) — 흐름 · 힘 비교에 정상 도달 정도가 섞인다.
12. **'한 곡선' 주장의 교락** — 선행 (dt 50 µs · < 40 rpm) ↔ 이 논문 (dt 5 µs · 2–100 rpm).
13. **'about eight contacts'** — 조건부 평균 둘의 합 (§3-5).
14. **Fig 4 ↔ Fig 7 전체 배위수 ≈ 0.15 차이** [판독 · 원인 미확인].
15. **공극 = 고정 슬랩 (0–40 mm)** — 날 뒤 빈 곳 · 날 위로 넘친 더미가 섞인다 · 충전 공극으로 읽지 않는다 [카드 추론].
16. **기호 N 두 뜻 · S_R² 의 N 선택 미공개** — 저자의 'S² ↑ → M ↓' 설명은 S_R² 고정을 전제 (§3-3 · §3-6).
17. **힘은 연화 E 로 계산** — 중력 · 느린 흐름 힘은 E 에 거의 무관하지만, Hertz 충돌의 최대 힘은 E*^{2/5} 에 걸려 ÷463 이면 ≈ 1/11.6 [카드 추론 · Hertz 충돌 축척 — 원문 밖 일반 식] → '파괴 가능 지역' 판단의 힘 크기는 고속 충돌 쪽에서 하한일 수 있다.
18. **토크 흔들림 미제시** (*"Although not shown here"*) · 에너지는 맞춤식 값 (판독 표지값이면 57.6 %).
19. **Fig 9a 의 곡선 번호 '4'** — 캡션은 1–3 만 정의 (θ ≈ 90° 근처 남은 라벨) [판독] · θ = 6° 칸 표지 없음 [판독].
20. **Fig 8 캡션 'instaneous' · Fig 11 캡션 'verticle' · Nomenclature 'Poison's ratio'** — 철자 그대로 (크롭 대조).
21. **계산 비용 · 하드웨어 · 적분법 · 이웃 탐색 없음** [미확인] — 비용 근거로 인용 불가.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄 · 정본 확인 = `papers/` 파일 목록 + 제목 · 쪽 grep)

| 번호 | 서지 (원문 목록 그대로) | 왜 · 카드 |
|---|---|---|
| 8 | Cundall, P. A.; Strack, O. D. L. A Discrete Numerical Model for Granular Assemblies. Geotechnique 1979, 29 (1), 47–65. | DEM 원전 — 카드 없음 (이름만 여러 카드) |
| 9 | Zhou, Y.; Yu, A. B.; Stewart, R. L.; Bridgwater, J. Microdynamic Analysis of the Particle Flow in a Cylindrical Bladed Mixer. Chem. Eng. Sci. 2004, 59, 1343–1364. | ★ **이 모델의 원전 (첫째)** · 연화 E 정당화 · 10 rpm 토크 1.1 N m · 배위수 · 힘 망 방법 — 카드 없음 |
| 10 | Stewart, R. L.; Bridgwater, J.; Zhou, Y. C.; Yu, A. B. Simulated and Measured Flow of Granules in a Bladed Mixer. Chem. Eng. Sci. 2001, 56 (19), 5457–5471. | 같은 믹서 DEM ↔ PEPT 검증 — 카드 없음 (후보 표 N-45) |
| 11 | Knight, P. C.; Seville, J. P. K.; Wellm, A. B.; Instone, T. Prediction of Impeller Torque in High Shear Powder Mixers. Chem. Eng. Sci. 2001, 56, 4457–4471. | 토크 – Fr 축척 · 고속 믹서 끝 속도 — 카드 없음 |
| 12 | Zhou, Y. C.; Wright, B. D.; Yang, R. Y.; Xu, B. H.; Yu, A. B. Rolling Friction in the Dynamic Simulation of Sandpile Formation. Physica A 1999, 269, 536–553. | ★ **이 모델의 원전 (둘째)** · 구름 마찰 (A 부류 대표 — ai2011 카드) · 연화 E 정당화 — 카드 없음 (`wishlist.md` 에 이미 있음) |
| 13 | Zhu, H. P.; Zhou, Z. Y.; Yang, R. Y.; Yu, A. B. Discrete Particle Simulation of Particulate Systems: Theoretical Developments. Chem. Eng. Sci. 2007, 62, 3378–3396. | ★ Table 1 의 *"commonly used"* 근거 (힘 모델 리뷰) — 카드 없음 |
| 14 | Remy, B.; Khinast, J. G.; Glasser, B. J. Discrete Element Simulation of Free Flowing Grains in a Four-Bladed Mixer. AIChE J. 2009, 55 (8), 2035–2048. | 4 날개 믹서 DEM — 카드 없음 (jadidi2023 이 이름 언급) |
| 15 | Kuo, H. P.; Knight, P. C.; Parker, D. J.; Adams, M. J.; Seville, J. P. K. Discrete Element Simulations of a High-Shear Mixer. Adv. Powder Technol. 2004, 15 (3), 297–309. | 날 뒤 빈 공간 실험 (끝 속도 1.4 m/s) — 카드 없음 |
| 16 | Fan, L. T.; Chen, S. J.; Watson, C. A. Solids Mixing. Ind. Eng. Chem. 1970, 62 (7), 53–69. | S₀² = pq · S_R² = pq/N 의 인용처 — 카드 없음 |
| 17 | Lacey, P. M. C. Developments in the Theory of Particle Mixing. J. Appl. Chem. 1954, 4, 257. | ✅ [`lacey1954_particle_mixing_theory_index`](lacey1954_particle_mixing_theory_index.md) |
| 18 | Kristensen, H. G. Statistical Properties of Random and Non-Random Mixture of Dry Solids. Powder Technol. 1973, 7 (5), 249–257. | ★ 크기 다른 혼합물의 무작위 분산 (고정 부피 표본) — 우리 1 : 9 크기비 S_R² · 카드 없음 |
| 19 | Zhou, Y. C.; Yu, A. B.; Bridgwater, J. Segregation of Binary Mixture of Particles in a Bladed Mixer. J. Chem. Technol. Biotechnol. 2003, 78, 187–193. | 40 rpm 이하 날 속도 · dt 50 µs · 한 곡선 — 카드 없음 |
| 20 | Zhou, Y.; Yu, A. B.; Bridgwater, J. The Effect of Blade Speed on Granular Flow in a Cylindrical Mixer. Presented at The 4th World Congress of Particle Technology, Sydney, Australia, 2002. | 같은 질문의 학회 판 — 카드 없음 |
| 21 | Asmar, B. N.; Langston, P. A.; Matchett, A. J.; Walters, J. K. Validation Tests on a Distinct Element Model of Vibrating Cohesive Particle Systems. Comput. Chem. Eng. 2002, 26 (6), 785–802. | ★ 54 µs 시간 간격 기준의 근거 (둘 중 하나) · nadeem2023 이 MGMMI 원전으로 이름 언급 — 카드 없음 |
| 22 | Tsuji, Y.; Kawaguchi, T.; Tanaka, T. Discrete Particle Simulation of Two-Dimensional Fluidized Bed. Powder Technol. 1993, 77 (1), 79–87. | 54 µs 근거 (둘째) — 카드 없음 |
| 23 | Massol-Chaudeur, S.; Berthiaux, H.; Dodds, J. A. Experimental Study of the Mixing Kinetics of Binary Pharmaceutical Powder Mixtures in a Laboratory Hoop Mixer. Chem. Eng. Sci. 2002, 57 (19), 4053–4065. | '확산이 혼합 곡선 가운데부터 지배' 의 근거 — 카드 없음 |
| 24 | Muzzio, F. J.; Llusa, M.; Goodridge, C. L.; Duong, N. H.; Shen, E. Evaluating the Mixing Performance of a Ribbon Blender. Powder Technol. 2008, 186 (3), 247–254. | 고속에서 나쁜 혼합 (리본 블렌더) — 카드 없음 |
| 25 | Nilpawar, A. M.; Reynolds, G. K.; Salman, A. D.; Hounslow, M. J. Surface Velocity Measurement in a High Shear Mixer. Chem. Eng. Sci. 2006, 61 (13), 4172–4178. | 토로이드 운동 · Fr 15.5 — 카드 없음 |
| 26 | Sato, Y.; Nakamura, H.; Watano, S. Numerical Analysis of Agitation Torque and Particle Motion in a High Shear Mixer. Powder Technol. 2008, 186 (2), 130–136. | 100–600 rpm 선형 토크 — 카드 없음 |
| 1–7 | Bridgwater 1976 · Bates 1997 · McCarthy 1996 · Bagster & Bridgwater 1969 · Malhotra 1988 · Parker 1993 · Broadbent 1993 (서론 배경 · PEPT 원전) | 우선순위 낮음 — 카드 없음 |

## 12. [미확인] 목록 (원문 12 쪽 전수에 없음)
- 계산 비용 · 하드웨어 · 적분법 · 이웃 탐색 · 병렬.
- 54 µs 허용 간격의 식 (refs 21 · 22 를 봐야 함).
- 벽 · 날 접촉의 법선 식 (반지름 규약) · 크기 다른 두 구의 R 규약 (이 논문은 단분산이라 필요 없었음).
- 법선 감쇠 식의 R · m_i 의 뜻 (입자 질량 ↔ 환산 질량) · 인쇄 부호가 맞는지.
- 반발계수 (원문 값 없음 · 카드 산술 0.25 / 0.39 만).
- S_R² 에 쓴 N (칸 평균 · 최소 · 전체) · 빈 칸 · 반쯤 찬 칸 처리 · 칸 층 수.
- Fig 7a '10 rpm' 이 9.55 rpm 런인지 · Fig 12b · 13b 선의 런 수.
- Fig 4 ↔ Fig 7 전체 배위수 차이 (≈ 0.15) 의 원인.
- 'real glass beads 10⁹' 의 출처.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- 본문 12 쪽 텍스트 층 전수 (PyMuPDF · 쪽마다) · Table 1 · 식 (1)–(4) · 영률 문장 · Nomenclature = 300 dpi 렌더로 글자 대조 (텍스트 층: '=' → ')' · 위첨자 · 분수 깨짐 · 'ﬁ' 합자).
- 'Hertz' · 'Mindlin' · 'plastic' · 'unload' · '2D' · '3D' = 0 회 · 'three dimension(al)' 2 회 (입체각 · 소용돌이) · 'soft' 1 회 (p.5473) · 'deform' 4 회 (p.5473 1 + Nomenclature 3) [텍스트 층 grep].
- 그림 14 · 표 1 = 박힌 래스터 (그림) · 벡터 (표) — 도구 크롭 15 장은 캡션이 빠졌거나 (그림 14) 쪽 전체 (표 1) 라 전부 손으로 다시 자름 · 식 10 · 근거 문단 20 손 크롭 — 45 장 전부 열람.
- 수치 재현 (scratch 스크립트 · 저장 안 함): Hertz 계수 · 겹침 · 충돌 시간 · 반발계수 (적분) · Rayleigh 간격 · 끝 속도 · Fr · 회전수 · 칸 넓이 · 칸당 입자 · 정지 침대 공극 · 토크 맞춤 · 에너지 · 시간 비 → §3.
- 정본 litdb 중복 확인: `papers/` 파일 목록 (chandratilleke* = 2012 한 장) · DOI `ie901581t` · '5467' · 'Effect of blade speed' grep = 2012 카드 인용 줄뿐 · 제목 · 쪽 grep 으로 참고문헌 카드 유무 (§11).
- PDF 는 기관 구독 다운로드본 (쪽마다 다운로드 표기) — 내용 판독에 영향 없음.

## 🔗 관련 카드
- 같은 제1 저자 · 같은 믹서 계열: [`chandratilleke2012_particle_scale_mixing_index`](chandratilleke2012_particle_scale_mixing_index.md) (이 논문을 ref 18 로 DEM 방법 인용 · PSMI · 크기 · 밀도 이원계).
- 구름 저항 꼴: [`ai2011_rolling_resistance_contact_models_dem`](ai2011_rolling_resistance_contact_models_dem.md) (A 부류 = 방향 일정 토크 · 대표 Zhou 1999 = 이 논문 ref 12).
- 혼합 지수: [`lacey1954_particle_mixing_theory_index`](lacey1954_particle_mixing_theory_index.md) (ref 17 · 원 정의) · [`nadeem2023_gnn_mixing_index`](nadeem2023_gnn_mixing_index.md) (Asmar 2002 = ref 21 의 MGMMI) · [`chibwe2020_nnsi_segregation_index`](chibwe2020_nnsi_segregation_index.md) · [`jadidi2023_dem_batch_solid_mixers_review`](jadidi2023_dem_batch_solid_mixers_review.md) (Lacey · 힘 망 계열에 'Chandratilleke 2010' 언급 — 이 논문과 맞음).
- 건식 혼합 DEM: [`hare2026_dem_pept_dry_mixing_nmc622_eirich`](hare2026_dem_pept_dry_mixing_nmc622_eirich.md) · [`lischka2025_dem_eirich_intensive_mixer_dry_mixing`](lischka2025_dem_eirich_intensive_mixer_dry_mixing.md).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

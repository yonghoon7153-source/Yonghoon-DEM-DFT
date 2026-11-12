<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 ([DEM 우선 (수영)] 문헌 보강 · 후보 표 N-47 · 정독 87) 에서 꼭 뽑으라고 한 항목.
     본 = mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표) · stewart2001_dem_pept_bladed_mixer_detailed_comparison.md (DEM 계산 논문의 3 · 4 절 꼴).
     원문 = 출판본 PDF (Particuology 12 (2014) 107–112 · 6 쪽).  쪽 표기 = 인쇄 쪽 p.107–112.  크롭 파일 이름의 pN 과 figures.json 의 page 는 PDF 쪽 (PDF p.N = 인쇄 p.106 + N).
     보충 자료 (SI) 없음 · 그림 10 · 표 2 · 번호 붙은 식 5 · 참고문헌 11.
     값 표지: [인쇄] = 본문 · 표 · 그림 안 글자로 적힌 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 182 행 — 그림 10 장이 모두 내장 래스터라 원본 래스터 화소에서 ·
     축 = 화소에서 찾은 눈금 표시로 선형 / 로그 맞춤 · 방법은 csv 의 note 칸) · [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 ·
     [우리 산술] = 우리 쪽 값과 견주는 계산 (원문에 없다) · [미확인] = 원문 6 쪽 전수에 없음.
     원문 6 쪽은 글자 층 추출 (블록 좌표) + 전 쪽 렌더로 전부 읽었다 (식 · 그리스 문자 · 위첨자는 글자 층이 깨져 렌더에서 옮겼다).  계산 = 상용 EDEM DEM · 실험 없음. -->
# DEM 계산 속도를 위해 입자 강성 (전단탄성률 G) 을 낮추면 벌크 거동이 어디서부터 바뀌나 — EDEM Hertz–Mindlin 3D 구 · G 10⁴–10¹¹ Pa 스윕: 구–벽 충돌 힘 ∝ G^0.40 · 접촉 시간 ∝ G^−0.40 [판독] · 50 kg 블록 낙하 벌크 강성 'linear correlation' = log–log 기울기 0.59 [판독] · 벌크 반발은 무를수록 커짐 (≤ 0.9 · 입자 C_R 0.01 로도 0.7) · 안식각은 G ≥ 10⁷ Pa (평균 겹침 < 반지름의 0.3–0.34 %) 에서 무영향 · 쐐기 관입 저항은 G ≥ 10⁸ Pa (겹침 ≤ 0.3 %) 에서 큰 차 없음 — "강성이 아니라 겹침으로 판정하라 · 조심하고 검증하라" — Lommen · Schott · Lodewijks (Particuology 2014)

> slug `lommen2014_dem_speedup_contact_stiffness_reduction_bulk_behavior` · DOI `10.1016/j.partic.2013.03.006` · type `DEM (EDEM commercial · built-in Hertz–Mindlin with Tsuji-type delta^1/4 damping · 3D spheres · particle shear-modulus sweep G = 1e4–1e11 Pa; single particle–wall impact (d 4/8/16 mm, 1 m/s) · bulk compression = 50 kg block dropped on a laterally periodic bed of 18,000 spheres (bulk stiffness from eigenfrequency, bulk restitution from six rebounds) · angle of repose (glass-bead parameters, d 4 mm, two-chamber rig) · wedge penetration (iron-ore-pellet parameters, d 15 mm, 5,000 spheres, 10 repeats) — no experiments)` · PDF `a7be108b-47._DEM_speedup_Stiffness_effects_on_behavior_of_bulk_material.pdf` · SI 없음 · digested `2026-11-12` · status ✅
>
> **저자**: **Stef Lommen\*** · Dingena Schott · Gabriel Lodewijks — Department of Maritime and Transport Technology, Delft University of Technology (2628CD Delft, The Netherlands) — \* 교신 · *Particuology* **12** (2014) **107–112** · 접수 2012-12-21 · 수정본 2013-03-20 · 수락 2013-03-26 · © 2013 Chinese Society of Particuology and Institute of Process Engineering, Chinese Academy of Sciences (Elsevier B.V.) · 키워드 *Discrete element method · Speedup · Stiffness reduction · Limit · Overlap* · 지원 = 그랩 (grab) 제조사 **NEMAG** (네덜란드) [인쇄 p.112 감사].
> **이웃 카드 (링크만)**: [`roessler2019_dem_cohesive_aor_cylinder_lift_calibration`](roessler2019_dem_cohesive_aor_cylinder_lift_calibration.md) (참고문헌 L236 = 이 논문 · 가리킨 카드) · [`coetzee2017_dem_calibration_review`](coetzee2017_dem_calibration_review.md) (ref [81] = 이 논문 · §7 강성 감소 표 L230) · [`paulick2015_elastic_particle_properties_dem_review`](paulick2015_elastic_particle_properties_dem_review.md) (ref [23] 'Lommen 2013' = 이 논문 · 선형 증거 표 L170 · 안식각 L569 · 관입 L591) · [`paulick2015_particle_contact_stiffness_two_particle_method`](paulick2015_particle_contact_stiffness_two_particle_method.md) (접촉 강성 실측) · [`morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis`](morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis.md) (같은 EDEM · 철광석 · G 타협) · [`chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer`](chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer.md) (연화 E "to reduce computational time") · [`stewart2001_dem_pept_bladed_mixer_detailed_comparison`](stewart2001_dem_pept_bladed_mixer_detailed_comparison.md) (연화 E 고정 유동 검증) · [`hare2026_dem_pept_dry_mixing_nmc622_eirich`](hare2026_dem_pept_dry_mixing_nmc622_eirich.md) (연화 정당화 실험 선례).
> **판독 원자료**: `litdb/figures/lommen2014_dem_speedup_contact_stiffness_reduction_bulk_behavior/digitized.csv` (182 행 — Fig. 1 · 2 표지 48 · Fig. 6 극값 18 · Fig. 7 표지 7 · Fig. 8 표지 48 · Fig. 9a 안식각 8 + 겹침 6 (+ 화면 밖 외삽 1) · Fig. 9b 8 · Fig. 10 곡선 36 + 오차 막대 2) · 크롭 **40 장** (그림 · 표 14 = 도구 10 (표 1 다시 자름 · 캡션 고침 4) + 손 4 (그림 7 · 표 2 · 패널 9a · 9b) · 식 6 · 근거 문단 20) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 상용 EDEM 의 Hertz–Mindlin 접촉으로 mm 크기 구를 계산하면서 **입자 전단탄성률 G 를 10¹¹ 에서 10⁴ Pa 까지 (7 자릿수) 낮춰** 네 시험 (구–벽 충돌 · 50 kg 블록 낙하 · 안식각 · 쐐기 관입) 의 응답을 본 결과, **안식각은 G ≥ 10⁷ Pa (평균 법선 겹침 < 반지름의 0.34 %) 에서, 관입 저항은 G ≥ 10⁸ Pa (겹침 ≤ 0.3 %) 에서 크게 변하지 않았지만, 벌크 강성 · 벌크 반발은 G 전 구간에서 강성을 따라 움직였다** — 저자 권고 = *"compare the normal overlaps and not the stiffness or shear modulus"* (p.108) · *"users should be cautious and verify their approach"* (p.111).
**소성 · 큰 변형 · 압밀 (수백 MPa) · 탈압 · 2D 는 이 논문에 없다.**  연화의 목적은 오직 **계산 시간** (시간 간격 ↑) 이다.

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 무엇을 계산했나 | **EDEM® (DEM-Solutions)** 내장 **Hertz–Mindlin** (법선 = Tsuji 1992 꼴 k δ^{3/2} + c v δ^{1/4} · 식 1–5) · **3D 구** · 강성은 **G (전단탄성률) 입력으로만** 바꿈 (E = 2G(1 + ν) · 식 5) · 네 시험: 단일 구–벽 충돌 (d 4 · 8 · 16 mm · 1 m/s · 중력 무시) / 벌크 압축 = **옆 주기 경계 바닥 (0.3 m 정사각) 위 18,000 구에 50 kg 블록을 0.2 m 에서 떨어뜨림** / 안식각 (유리구 값 · d 4 mm · 160 mm 두 칸 장치) / 쐐기 관입 (철광석 펠릿 값 · d 15 mm · 5,000 구 · 쐐기 밑변 40 mm · 30° · 8 mm/s · 10 회 반복) | [인쇄] p.107–110 · 표 1 · 2 |
| ② ★ 연화의 크기 효과 | 단일 충돌: 힘 0.0163 → 10.3 N (d 4 mm) · 접촉 시간 4.59 × 10⁻³ → 7.36 × 10⁻⁶ s (G 10⁴ → 10¹¹) — 최소제곱 log–log 기울기 **+0.400 / −0.399** (Hertz 의 ±2/5 와 같다 [카드 산술]) · 벌크 강성 7.51 × 10³ (G 10⁵) → 2.76 × 10⁷ N/m (G 10¹¹) — **6 자릿수 G 에 3,669 배** · 첫 충돌 벌크 반발 0.28–0.39 (G ≥ 10⁹) ↔ 0.62–0.72 (G ≤ 10⁷) · 관입 일 (≈64.7 mm) 14.2 (10¹⁰) · 11.2 (10⁸) · 6.0 (10⁷) · 1.5 J (10⁵) | [판독] Fig. 1 · 2 · 7 · 8 · 10 · [카드 산술] |
| ③ ★ "바꾸지 않는 범위" (문턱) | 안식각: *"Shear modulus between 10⁷ and 10¹¹ Pa appears to have no influence"* · 바뀌는 순간 평균 겹침 **0.34 % of the particle radius** (p.111) — 결론에서는 **0.3 %** · 관입: G ≥ 1 × 10⁸ Pa · 겹침 ≤ 0.3 % 에서 *"did not exhibit large differences"* (그래도 64.7 mm 에서 10⁸ 은 10¹⁰ 의 0.79 [판독 · 카드 산술]) · **벌크 압축에는 안전 범위가 없다** (*"Properties such as the bulk stiffness and bulk restitution changed as a result of the stiffness reduction"* p.111) | [인쇄] p.110–111 · [판독] |
| ④ ★ 'linear correlation' 의 실체 | 본문 *"Fig. 7 shows a linear correlation between the shear modulus of the particles and the bulk stiffness"* — 그림 7 은 **log–log 축** 이고 점 7 개 · 그려진 직선 모두 **기울기 0.591** [판독 · 카드 산술] ⇒ **비례가 아니라 멱법칙 K ∝ G^0.59** | [인쇄] p.110 · [판독] Fig. 7 |
| ⑤ ★ 연화 → 되튐 (반발) | 무른 침대일수록 감쇠가 적다: G 10⁵ 의 벌크 반발 0.72 (첫 충돌) · 0.88–0.91 (2–6 번째) [판독] · 입자 C_R 을 0.5 → **0.01** 로 낮춰도 G 10⁶ 침대 벌크 반발 **≈0.7** (판독 0.62–0.74) — 저자 추정 원인 *"the large number of parallel springs and dampers, as well as the size of the normal overlaps (10%) at this low stiffness"* | [인쇄] p.110 · [판독] Fig. 8 |
| ⑥ ★ DEM 한계 문장 (k) | 여러 곳 (§4-3) — 연화의 *"limits and drawbacks … may lead to invalid results"* (p.107) · G 10⁴ 침대는 *"impossible"* (p.110) · 구 모양 효과를 줄이려 **구름을 막음** (p.109) · 단단한 입자에서 **한 입자가 관입 힘의 30 %** (p.111) | [인쇄] |
| ⑦ ★ 소성 · 큰 변형 (l) | **없음** — 본문에 plastic · yield · deform 0 회 (plastic 은 참고문헌 제목에 1 회) · 접촉은 탄성 + 점성 감쇠 · 비용 서술 = *"changing the stiffness from 10¹¹ to 10⁷ Pa can decrease the computation time by up to a factor of 100"* (p.111) 뿐 | [인쇄] |
| ⑧ ★ 2D / 3D | **3D 만** (EDEM 3D 구) — 2D · 2D → 3D 언급 없음 | 원문 전수 |
| ⑨ ★ 탈압 | **다루지 않음** — 있는 것은 50 kg 블록의 되튐 (동적 · 블록 정하중 ≈5.45 kPa [카드 산술]) 과 관입 (누르기만) | Fig. 6 · 8 · 10 |
| ⑩ 절대값 전이 | **안 된다** — 재료 (유리 · 철광석 펠릿 값 · ρ 1500–3500 kg/m³) · 크기 (mm) · 하중 (중력 · 충돌 · kPa) · 접촉 법칙 (Hertz–Mindlin ↔ 우리 hooke/hysteresis) 이 모두 다르다 · 옮길 것은 **판정 규칙 (겹침으로 판정) 과 경고 (벌크 강성 · 반발 · 힘 꼬리가 강성에 묶인다)** 뿐 | §7 |

⛔ **한정어 (떼지 말 것)**: ① 연화 목적 = **계산 시간** (실측에 맞추는 보정이 아니다) ② 문턱 0.3–0.34 % 는 **평균** 법선 겹침 ÷ **반지름** · **mm 구 · 중력 · 충돌 · 관입** 의 값 (안식각 0.34 % = 유리구 값 + ρ 7800 확인 (안 보임) · 관입 0.3 % = 철광석 펠릿 값) ③ 'linear correlation' 은 **log–log 직선 (기울기 0.59)** — 비례 아님 ④ 벌크 압축 시험 = **블록 낙하 동적 시험** (정적 압밀 · 압력 곡선 아님) ⑤ 그림 9 의 표지 x 위치는 인쇄 눈금으로 **10^(n + 0.445)** 이라 본문 G 값과 반 자릿수 어긋난다 (§3-4) ⑥ 시간 간격 규칙 · 계산 시간 · 벽 물성 · 벌크 압축 시험의 입자 지름 · 안식각 시험의 입자 수는 [미확인].

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-47 의 '왜' 칸)

의도 원문: *"k · l — "강성 연화가 벌크 거동에 주는 영향 — 카드 없음" → 무르게 맞춘 강성 (우회) 이 거동을 바꾸는 범위의 인용처 후보"* (가리킨 카드 = `roessler2019_dem_cohesive_aor_cylinder_lift_calibration` L236)

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "강성 연화가 벌크 거동에 주는 영향" | **채움** | 네 시험 (§3-1 – §3-5) · G 10⁴ → 10¹¹ Pa (7 자릿수) · 결과: 단일 충돌 힘 · 시간 ∝ G^{±0.40} [판독] · 벌크 강성 ∝ G^0.59 [판독] · 벌크 반발 ↑ (무를수록) · 안식각 G ≥ 10⁷ 불변 · 관입 G ≥ 10⁸ 큰 차 없음 (p.110–111 · Fig. 1 · 2 · 7 · 8 · 9 · 10) · 조건 = 3D mm 구 · 중력 / 충돌 1 m/s / 블록 정하중 ≈5.45 kPa [카드 산술] / 쐐기 8 mm/s · 온도 개념 없음 (DEM) · 누른 채 / 뺀 뒤 구분 해당 없음 |
| "무르게 맞춘 강성 … 이 거동을 바꾸는 **범위**" | **채움** (범위) · **일부** (조건) | 범위는 **겹침 (반지름 비)** 으로 주어진다 — 안식각: 바뀌는 순간 평균 겹침 **0.34 %** (p.111 결과) · 결론 *"below 0.3% of the particle radius"* (p.111) · 관입 **≤ 0.3 %** (G ≥ 10⁸ · p.111) · 단일 충돌: 강성은 *"an important parameter during impact collisions"* (p.108 · 문턱 없음) · 벌크 강성 · 반발: **문턱 없음 (전 구간에서 바뀜)**.  조건 한정 = mm 구 · 저응력 · Hertz–Mindlin · 평균 겹침 |
| "(우회)" = 다른 이유로 무르게 **맞춘** 강성 | **일부** | 이 논문의 연화는 **속도 (시간 간격) 목적** 뿐이다 — *"By making particles less stiff or softer, a larger time step can be used"* (p.107).  실측 벌크에 맞추려 낮춘 연화 (우리 frame [2] 의 소성 · 재배열 대리 · `coetzee2017` 카드의 '(a) 보정' ↔ '(b) 계산속도용 강성 감소' 구분에서 (a)) 는 다루지 않는다 — 이 논문은 (b) 의 전형.  '맞춘' 값은 표 2 (철광석 펠릿 G 1 × 10⁸ Pa · ν 0.2 · ρ 3500 · d 15 mm · Lommen 2011 관입 보정) 하나이고 그 보정 대상 · 방법은 이 논문에 없다 [미확인] |
| "인용처 후보" (k — DEM 한계를 문헌으로 말하기) | **채움** | 인용 가능 문장 §4-3 (p.107 · 108 · 109 · 110 · 111) — 연화의 한계 · 겹침 판정 규칙 · G 10⁴ 계산 불가 · 병렬 스프링 · 댐퍼 · 구 모양 (구름 금지) · 한 입자 30 % · 마찰로 보상하면 다른 곳이 바뀜 |
| "(l) 소성변형이 왜 어려운가" | **없음** | 소성 · 항복 · 입자 모양 변화 · 부피 보존 유동 · 가공 경화 · 이웃 접촉 상호 영향 — 본문 **0 회** (plastic 은 참고문헌 제목 1 회뿐).  접촉 = 탄성 Hertz–Mindlin + 감쇠 (식 1).  우회 · 비용 서술은 **시간 간격 (최대 100 배)** 하나 (p.111) |
| (가리킨 카드의 서지) roessler2019 L236 | **채움** | *"Lommen, S., Schott, D., & Lodewijks, G. (2014). DEM speedup: Stiffness effects on behavior of bulk material. Particuology, 12, 107–112."* = 원문 첫 쪽 (저자 셋 · 제목 · 권 · 쪽 · 연도) 과 같다 · 그 카드의 '카드 없음' 은 이 카드로 낡았다 (고치지 않음) |

**같은 원문을 2 차로 옮긴 카드 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `roessler2019_…` L236 | 서지 + "강성 연화가 벌크 거동에 주는 영향" | 같은 서지 · 같은 주제 | **채움** |
| `coetzee2017_…` L230 ① | "①구속압축 … **벌크강성 = 접촉강성의 선형함수**" | 본문 낱말 *"linear correlation"* (p.110) 은 맞다 · 그러나 Fig. 7 은 log–log · 기울기 **0.59** [판독] = 비례 아님 · 시험 = 주기 경계 침대 위 **블록 낙하 (고유진동수로 강성)** | **일부** |
| `coetzee2017_…` L230 ② | "G **>** 1×10⁸ Pa(오버랩 ≤0.3 %) 이면 저항 **포화**" | *"a shear modulus of 1 × 10⁸ Pa **or higher** … did not exhibit large differences in average penetration resistance"* (p.111) — '≥' · '포화' 아님 (64.7 mm 에서 10⁸ 은 10¹⁰ 의 0.79 · 10⁹ 는 0.94 [판독]) | **일부** |
| `coetzee2017_…` L230 ③ | "G ≥ 1×10⁷ Pa 또는 오버랩 <0.3 % 면 안식각 무영향" | 결론 *"kept above 10⁷ Pa or … below 0.3%"* (p.111) ✓ · 결과 절의 값은 0.34 % | **채움** |
| `coetzee2017_…` L230 따옴표 | *"users should be cautious **when reducing the contact stiffness and should** verify their approach"* | 원문 (p.111): *"…when applying a particle stiffness reduction in models related to the bulk stiffness and bulk restitution, shearing behavior, and the interaction between material and equipment, users should be cautious and verify their approach."* — 따옴표 안 문장은 원문 그대로가 아니다 (리뷰의 바꿔 쓰기로 보임 [카드 해석]) | **일부** |
| `coetzee2017_…` L689 | 'Bulk density ✅[81]' | Fig. 9b 안식각 더미의 bulk density ✓ | **채움** |
| `paulick2015_elastic_…` L170 | "G **∝** 벌크강성 · 단축 벌크압축 · 18,000 입자 · 수평 주기경계 · G 10⁴ → 10¹¹ Pa (10⁷×) · EDEM H–M · [23] Lommen **2013**" | 18,000 ✓ · 주기 경계 (X · Y) ✓ · EDEM Hertz–Mindlin ✓ · 범위는 방법 절 그대로이지만 **10⁴ 은 계산 불가** · Fig. 7 점 = 10⁵–10¹¹ (6 자릿수) · **'∝' 아님 (기울기 0.59)** · '단축 압축' = 블록 낙하 동적 · 연도 = 2014 권 (© 2013) | **일부** |
| `paulick2015_elastic_…` L464 | "[23] Lommen (스윕 폭) 10¹¹ → 10⁴ Pa ÷10⁷" | *"a stiffness reduction factor of 10⁷"* (p.108) ✓ | **채움** |
| `paulick2015_elastic_…` L569–572 | 안식각 "G < 10 MPa 에서 **28° → 26° → 23° → 12°** 급락 · G > 10 MPa 무영향" | 판독 평탄 28.0–28.7° → **27.5 → 23.9 → 13.0°** [판독 Fig. 9a] · '26' 은 같은 x 의 겹침 원을 왼쪽 축으로 읽은 높이 (26.2°) 와 같다 [판독] · 문턱 방향 ✓ | **일부** (숫자 둘 다름) |
| `paulick2015_elastic_…` L585–588 | "선형 · 하한: *'**Below** 10⁴ Pa the contacts could not generate enough force…'*" | 원문 (p.110): *"A simulation using a shear modulus **of 1 × 10⁴ Pa** turned out to be impossible, as the contacts could not generate enough force to reverse the direction of the mass motion."* — 'Below' 아님 · 선형 → 기울기 0.59 | **일부** (따옴표 문장 다름) |
| `paulick2015_elastic_…` L591–592 | "**콘** 관입(쐐기, base 40 mm, 30°, 8 mm/s): G 10⁸–10⁹ → 11–14 J, **G 10⁴–10⁶ → 1–6 J** = 저항을 **절반으로** 과소평가" | 쐐기 · 40 mm · 30° · 8 mm/s ✓ ('콘' 낱말 없음) · 64.7 mm 판독 10⁸ 11.2 · 10⁹ 13.4 J ✓ · **G 10⁴ 곡선은 없다** (Fig. 10 = 10⁵–10¹⁰) · 1.5 J (10⁵) · 3.2 (10⁶) · **6.0 (10⁷)** → '1–6 J' 은 **10⁵–10⁷** · '절반' 은 10⁷ (0.42) 에만 맞음 (10⁶ 0.22 · 10⁵ 0.11 [카드 산술]) | **일부** |
| `paulick2015_elastic_…` L656 · L909 | 단일 입자 절에 [23] · "선형 강성↔벌크계수" 요약 | 단일 접촉 시험 ✓ · 선형 → 기울기 0.59 | **채움** / **일부** |

⇒ **의도 대조 결과: 일부** — k (연화가 벌크를 바꾸는 범위 · 문턱 · 인용 문장) 는 **채움**; l (소성이 왜 어려운가) 는 **없음**; '무르게 맞춘 우회' 는 이 논문에서 **속도 목적 연화** 라 일부.  다른 카드 두 장 (coetzee2017 · paulick2015) 이 이 원문을 옮기며 **'선형 (∝)' · 숫자 (26° · 12° · 10⁴–10⁶ → 1–6 J) · 따옴표 문장 둘** 을 바꿨다.

---

## 1. 한 줄 요약
DEM 계산 시간을 줄이는 흔한 방법인 입자 강성 낮추기가 "어디까지 안전한가" 를 재려고, EDEM Hertz–Mindlin 으로 G 를 10¹¹ (강철 80 GPa 기준) → 10⁴ Pa 까지 낮추며 구–벽 충돌 · 블록 낙하 (벌크 강성 · 반발) · 안식각 · 쐐기 관입을 계산했다.
안식각 · 관입 평균 저항은 평균 법선 겹침이 반지름의 0.3 % 안팎을 넘기 전까지 거의 그대로 (G 10¹¹ → 10⁷ 이면 시간 최대 100 배 절약) 였지만, 벌크 강성 · 반발 (되튐) 은 강성을 따라 계속 바뀌었고, 무른 입자는 관입 힘의 요동 (한 입자 몫 최대 30 %) 을 깎아 평균 저항까지 낮췄다.
저자 권고: 강성 감소량은 G 가 아니라 **겹침** 으로 판정하고, 벌크 강성 · 반발 · 전단 · 장비–재료 상호작용 모델에서는 조심하고 검증하라 — 대안으로 입자 크기 키우기 (particle scaling) 를 든다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| S. Lommen\* · D. Schott · G. Lodewijks (TU Delft, Maritime and Transport Technology) | Particuology 12 (2014) 107–112 · © 2013 · 키워드 *Discrete element method · Speedup · Stiffness reduction · Limit · Overlap* | 10.1016/j.partic.2013.03.006 | 모의 입자 (값만): 단일 접촉 ρ 1500 kg/m³ · 안식각 = 유리구 값 (ρ 2470) · 관입 = 철광석 펠릿 값 (ρ 3500) — 배터리 재료 없음 | DEM (EDEM · Hertz–Mindlin) · 파라미터 스윕 · 실험 없음 |

- **1저자 메모 · 후보 표와의 대조**: 후보 표 N-47 · roessler2019 L236 의 서지 (Lommen, S., Schott, D., & Lodewijks, G. (2014) · 제목 · Particuology, 12, 107–112) — **같다**.  덧붙임 ① DOI = `10.1016/j.partic.2013.03.006` (p.107 바닥 · 후보 표에는 없음) ② 호 번호는 원문 머리글에 없다 (*"Particuology 12 (2014) 107–112"*) ③ PDF 문서 정보 (Title · Author) 는 비어 있다 ④ `paulick2015_elastic_…` 카드는 이 논문을 **'Lommen 2013'** 으로 적는다 — 원문 권 연도는 2014 · 저작권 표기 · 수락일은 2013.
- **글의 꼴**: 서론 (p.107) → 2 단일 접촉 (p.107–108 · 식 1–5 · Fig. 1–2) → 3 방법 (3.1 벌크 압축 · 3.2 안식각 · 3.3 관입 · p.108–110 · Fig. 3–5 · 표 1–2) → 4 결과 (4.1–4.3 · p.110–111 · Fig. 6–10) → 5 결론 (p.111) → 감사 · 참고문헌 11 (p.112).  그림 10 · 표 2 · 식 5 · SI 0.
- 같은 저자 앞 연구: Lommen, Schott, Rahman, Lodewijks (2011) 철광석 펠릿 관입 보정 (학회 논문 · 이 논문 표 2 의 출처 · 카드 없음).

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. 접촉 모델 — EDEM 내장 Hertz–Mindlin (p.107–108 · 식 1–5 · `eq_01…` – `eq_05…` · `eq_02_05_stiffness_definitions_set.png` · `txt_p1_single_contact_edem_hertz_mindlin.png`)
| 식 | 원문 (렌더에서 옮김) | 뜻 |
|---|---|---|
| (1) | **F⃗_n = F⃗_n,k + F⃗_n,d = (k_HM δ_n^{3/2} + c_HM v⃗_n δ_n^{1/4} n⃗) n⃗** | 법선 힘 = 탄성 + 점성 감쇠 · *"in a similar manner to Tsuji, Tanaka, and Ishida (1992)"* · c_HM = *"a function of the coefficient of restitution C_R"* (식은 인쇄 안 됨 [미확인]) · ⚠ 인쇄 꼴은 괄호 안에 v⃗_n 과 n⃗ 가 같이 있다 — 차원상 감쇠 항은 (v⃗_n · n⃗) 스칼라 × n⃗ 로 읽힌다 [카드 해석] |
| (2) | **k_HM = (4/3) E_eff √R_eff** | Hertz 강성 계수 (δ^{3/2} 에 곱함) |
| (3) | **1/R_eff = 1/R_i + 1/R_j** | 유효 반지름 (본문은 *"R_eff is the particle radius"* 라고도 적는다) |
| (4) | **1/E_eff = (1 − ν_i²)/E_i + (1 − ν_j²)/E_j** | 유효 영률 |
| (5) | **E = 2G(1 + ν)** | *"EDEM uses the shear modulus G and Poisson's ratio ν to compute the Young's modulus"* — 입력 = G · ν |

- **강성 = 물성에서 유도**: *"The stiffness of contact is sometimes directly adjustable in DEM codes, but most codes derive the stiffness from the properties of the material and colliding particles."* (p.108) · *"By lowering the shear modulus G, the effective Young's modulus will decrease, resulting in a reduced stiffness constant k_HM."* (p.108)
- **접선 (Mindlin) 힘 · 구름 마찰 모델 식은 실리지 않았다** [미확인] — 매개변수만 (μ_s · μ_r).
- [카드 산술] 같은 두 구 (ν 같음) 이면 E_eff = E/(2(1 − ν²)) = G/(1 − ν) → k_HM ∝ G (ν · R 고정) — 그래서 이 논문의 'G 스윕' = '접촉 강성 계수 스윕'.

### 3-2. ★ 단일 접촉 — 구–벽 충돌 (p.108 · Fig. 1 · 2 · `txt_p2_single_contact_setup_results.png`)
**조건 [인쇄]**: G **10⁴–10¹¹ Pa** (*"The upper value of 10¹¹ Pa was based on the 80 GPa shear modulus of steel. The lower limit was set to 10⁴ Pa to investigate a stiffness reduction factor of 10⁷."*) · 구 **d = 4, 8, 16 mm** · ν 0.25 · ρ 1500 kg/m³ · C_R 0.5 · 벽으로 **1 m/s** · 중력 무시 (*"because of the short simulation time"*).  벽 물성 · 시간 간격 [미확인].

**판독 (digitized.csv fig1 · fig2 · 8 G × 3 d)**:
| G (Pa) | F̄ d 4 / 8 / 16 mm (N) | t_c d 4 / 8 / 16 mm (s) |
|---|---|---|
| 10⁴ | 0.0163 / 0.0649 / 0.259 | 4.59 × 10⁻³ / 9.03 × 10⁻³ / 1.83 × 10⁻² |
| 10⁶ | 0.102 / 0.412 / 1.64 | 7.30 × 10⁻⁴ / 1.45 × 10⁻³ / 2.91 × 10⁻³ |
| 10⁸ | 0.649 / 2.61 / 10.3 | 1.16 × 10⁻⁴ / 2.34 × 10⁻⁴ / 4.67 × 10⁻⁴ |
| 10¹¹ | 10.3 / 41.2 / 165 | 7.36 × 10⁻⁶ / 1.47 × 10⁻⁵ / 2.91 × 10⁻⁵ |

- [카드 산술] 최소제곱 log–log 기울기 (점 8 · 7 자릿수 · d 4 / 8 / 16 mm): 힘 **+0.400 · +0.400 · +0.401** · 시간 **−0.399 · −0.399 · −0.399** = Hertz 충돌의 **E^{2/5} · E^{−2/5}** 와 같다.  크기: 힘 ∝ d² (16 배 = 4 → 16 mm) · 시간 ∝ d (4 배).
- [카드 산술 · Hertz 충돌 해 — 원문에 식 없음] t_c = 2.868 (m²/(R E*² v))^{1/5} · E = 2G(1 + ν) · **벽 = 같은 재료** (E* = E/(2(1 − ν²))) 이면 G 10⁸ 에서 d 4 · 8 · 16 mm = 1.066 · 2.133 · 4.266 × 10⁻⁴ s → 판독 / 이론 = **1.089 · 1.097 · 1.094** (감쇠 C_R 0.5 가 시간을 늘린 몫으로 읽힌다 [카드 해석]) · **벽 = 강체** 면 비 1.44 — 벽 물성이 원문에 없어 [미확인].  같은 조건의 최대 겹침 δ_max/R = **1.81 %** (같은 재료 벽) · 1.37 % (강체 벽).
- [카드 산술] F̄ = (1 + C_R) m v / t_c(판독) = 0.649 · 2.579 · 10.34 N ↔ 판독 0.649 · 2.606 · 10.33 N (≤ 1 %) — 그림의 *"Average normal elastic force"* 는 운동량 변화 ÷ 접촉 시간과 같은 값으로 움직인다.
- 원문 해석: *"when the stiffness of the particle is reduced, the average contact force decreases. At the same time, the contact time increases to conserve the collision energy"* · *"This implies that stiffness is an important parameter during impact collisions, and will thus affect the simulation results if a substantial number of collisions with large relative velocities are present in the system."* (p.108)

### 3-3. ★ 벌크 압축 = 50 kg 블록 낙하 (p.108–110 · Fig. 3 · 6 · 7 · 8 · `txt_p2_bulk_compression_rig.png` · `txt_p3_bulk_compression_protocol.png` · `txt_p4_bulk_compression_results.png` · `txt_p4_soft_restitution_overlaps.png`)
**조건 [인쇄]**: 정사각 바닥판 **0.3 m** (판–입자 접촉 = 입자–입자 값) · **X · Y 주기 경계** · **18,000 구** · ν 0.25 · C_R 0.5 · μ_s 0.5 · μ_r 0.04 (*"chosen to match the properties used during the single contact tests"*) · G 10⁴–10¹¹ Pa · 동적 생성기 **20,000 개/s** 로 채우고 가라앉힘 → **50 kg 블록을 윗면 0.2 m 위에서** 놓음 (*"the vertical velocity is limited to 1 m/s"*) · 블록 궤적에서 **고유진동수 + 블록 질량 → 벌크 강성** · 충돌마다 **들어오고 나가는 속도 → 벌크 반발** · 처음 **여섯** 충돌.  ⚠ 이 시험의 입자 지름 · 밀도 숫자는 없다 (단일 접촉 시험과 '맞췄다' 고만 · 그 시험은 d 셋) [미확인].
- [카드 산술] 블록 정하중 = 50 × 9.81 / 0.3² = **5.45 kPa** (우리 300 MPa 의 1/5.5 × 10⁴).

**결과 [인쇄]**
- *"Fig. 7 shows a linear correlation between the shear modulus of the particles and the bulk stiffness. A simulation using a shear modulus of 1 × 10⁴ Pa turned out to be impossible, as the contacts could not generate enough force to reverse the direction of the mass motion."* (p.110)
- *"most bulk restitution coefficients are higher than the particle restitution coefficient of 0.5. On the first collision, however, simulations with a high stiffness (… G ≥ 1 × 10⁹ Pa) showed a much lower bulk restitution coefficient than those with a low stiffness (G ≤ 1 × 10⁷ Pa)"* — 원인 추정 = 단단한 입자에서는 첫 충돌에 큰 빈틈이 줄어 둘째 충돌이 효율적 (p.110).
- *"Softer bulk materials showed significantly less damping than the stiff materials, with coefficients of restitution of up to 0.9"* · 입자 C_R **0.01** → 벌크 C_R **0.7** · *"It is possible that this was caused by the large number of parallel springs and dampers, as well as the size of the normal overlaps (10%) at this low stiffness (G = 1 × 10⁶ Pa)."* · 첫 충돌 평균 겹침 = 반지름의 **1 % (G 10⁸)** · **0.33 % (G 10⁹)** (p.110).

**Fig. 7 판독 (점 7 · 원본 래스터 xref 58 · 9 × 9 열림 연산으로 맞춤 선 제거)**
| G (Pa) | 10⁵ | 10⁶ | 10⁷ | 10⁸ | 10⁹ | 10¹⁰ | 10¹¹ |
|---|---|---|---|---|---|---|---|
| 벌크 강성 (N/m) | 7.51 × 10³ | 2.12 × 10⁴ | 7.98 × 10⁴ | 3.00 × 10⁵ | 1.25 × 10⁶ | 4.52 × 10⁶ | 2.76 × 10⁷ |
- [카드 산술] 최소제곱 log–log 기울기 **0.591** (점 7) · 10⁵–10¹⁰ 만 0.565 · 이웃 구간 기울기 0.45 · 0.58 · 0.58 · 0.62 · 0.56 · 0.79 · **그림에 그려진 직선의 기울기도 0.591** (선 위 13 점) · 10⁶ 배 G 에 **3,669 배** 강성.
- [카드 해석 — 원문은 지수를 다루지 않는다] Hertz 접촉 하나의 같은 힘에서의 접선 강성은 E*^{2/3} 를 따른다 (지수 0.667) — 판독 0.59 는 그보다 조금 낮다.  어느 쪽이든 **비례 (지수 1) 가 아니다**.
- 10⁴ Pa 는 점이 없다 (계산 불가).

**Fig. 6 판독 (G 10⁸ · 블록 속도)** — 0.24 s 까지 −1 m/s (떨어짐) → **+0.453 (0.285 s) → −0.448 (0.377 s) → +0.259 → −0.240 → +0.167 → −0.143 → +0.097 …** → ≈1.5 s 에 0.
- [카드 산술] 첫 되튐 뒤 내려오는 구간 기울기 **−9.98 m/s²** ≈ −g → 블록이 첫 두 충돌 사이 **침대를 떠나 날았다** (*"mass-damper system"* 이라는 본문 표현과 달리) · 뒤 구간 기울기 −9.1 · −6.2 · −4.4 m/s² (점점 붙어 있음).
- [카드 산술] 양의 봉우리 사이 시간 0.077–0.099 s (첫 간격 0.144 s) → k = m (2π/T)² ≈ **2.6 × 10⁵ N/m** (T 0.086–0.088 s · m 50 kg) ↔ Fig. 7 의 10⁸ 값 3.00 × 10⁵ (−11 ~ −14 %) — 원문은 고유진동수를 어느 구간 · 어떤 질량으로 냈는지 적지 않았다 [미확인].

**Fig. 8 판독 (8 계열 × 6 충돌 · 겹친 표지는 ± 0.01)**
| 계열 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| G 10⁵ | 0.72 | 0.88 | 0.89 | 0.90 | 0.90 | 0.91 |
| G 10⁶ | 0.66 | 0.75 | 0.81 | 0.83 | 0.84 | 0.85 |
| G 10⁷ | 0.62 | 0.58 | 0.63 | 0.69 | 0.73 | 0.74 |
| G 10⁸ | 0.57 | 0.64 | 0.57 | 0.62 | 0.66 | 0.62 |
| G 10⁹ | 0.39 | 0.69 | 0.67 | 0.50 | 0.67 | 0.62 |
| G 10¹⁰ | 0.28 | 0.86 | 0.74 | 0.64 | 0.57 | 0.56 |
| G 10¹¹ | 0.31 | 0.85 | 0.70 | 0.63 | 0.56 | 0.56 |
| G 10⁶ + C_R 0.01 | 0.62 | 0.70 | 0.73 | 0.74 | 0.74 | 0.74 |
- [카드 산술] 입자 C_R 0.5 → 0.01 (50 배) 이 G 10⁶ 침대의 벌크 반발을 **0.66–0.85 → 0.62–0.74** 로만 낮춘다.
- [카드 해석 · 판독 대조] Fig. 6 의 연속한 양의 봉우리 비 (v⁺_{k+1}/v⁺_k) = 0.571 · 0.646 · 0.580 · 0.640 · 0.652 · 0.667 ↔ Fig. 8 G 10⁸ = 0.572 · 0.643 · 0.572 · 0.618 · 0.655 · 0.620 — Fig. 8 의 '충돌 k' 는 Fig. 6 의 처음 −1 m/s 충돌 (+0.453 ÷ 1.0 = 0.45) 을 세지 않은 번호로 읽힌다 · 원문은 *"entry and exit velocities"* 라고만 적었다 [미확인].

### 3-4. ★ 안식각 (p.109–111 · Fig. 4 · 9 · 표 1 · `txt_p3_aor_setup_chamber_glass_beads.png` · `txt_p3_aor_opening_angle_fit.png` · `txt_p4_aor_results_start.png` · `txt_p5_aor_results_overlap_034.png`)
**조건 [인쇄]**: 칸 폭 **160 mm** · 표 1 = **유리구** 값 — d **4 mm** · ν **0.22** · ρ **2470** kg/m³ · C_R **0.9** · μ_s **0.5** · μ_r **0.01** · 위 칸을 채운 뒤 옆 판을 **10 mm/s** 로 내려 *"five times the particle size"* 만큼 열고 → 아래 칸으로 빠지고 위에 남은 더미의 경사 = 입자 위치에 직선 맞춤 (경사 위 · 아래 끝 · 벽 근처 제외).  입자 수 · 시간 간격 · 계산한 G 값 목록 [미확인].
- ⚠ 그림 4 의 여는 틈 표시는 **"24"** (단위 없음) ↔ 본문 '입자 크기의 다섯 배' = 4 × 5 = **20 mm** [카드 산술] · 본문 '칸 폭 160 mm' ↔ 그림 4 의 **가운데 판** 너비 "160" — 같은 치수인지 [미확인].

**결과 [인쇄]**: *"The stiffness effect on the angle of repose became apparent when the shear modulus dropped to 10⁷ Pa"* (p.110) · *"Shear modulus between 10⁷ and 10¹¹ Pa appears to have no influence on the angle of repose. An increase in the bulk density was detected at the same moment the angle of repose began to decrease. This means that changing the stiffness from 10¹¹ to 10⁷ Pa can decrease the computation time by up to a factor of 100 without significantly altering the results. At the moment at which the angle of repose and bulk density changed, the average of the normal overlaps of the contacts was 0.34% of the particle radius. This value could be used as a limit for the maximum particle softness. We have confirmed this value in a second series of angle of repose tests using a particle density of 7800 kg/m³ instead of 2470 kg/m³ (not shown)."* (p.111)

**Fig. 9 판독 (원본 래스터 xref 75 · 2150 × 807 px · 표지 8 개 · 왼쪽 → 오른쪽)**
| 표지 (왼쪽부터) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| 인쇄 눈금으로 읽은 log₁₀ G | 3.445 | 4.443 | 5.442 | 6.450 | 7.448 | 8.447 | 9.445 | 10.443 |
| 안식각 (°) · (오차 막대) | 13.04 (12.29–13.80) | 23.89 (22.53–25.25) | 27.50 (27.22–27.78) | 28.63 (27.68–29.59) | 28.38 (27.93–28.84) | 28.73 (28.03–29.44) | 28.03 (27.02–29.04) | 28.08 (27.42–28.73) |
| 평균 법선 겹침 (반지름 %) | 화면 밖 (외삽 ≈5.3) | 화면 밖 | 1.495 | 0.342 | 0.076 | 0.016 | 0.003 | 0.0002 |
| bulk density (kg/m³) | 2653 | 1837 | 1473 | 1421 | 1408 | 1379 | 1409 | 1407 |

- ⚠ **x 위치가 반 자릿수 어긋난다** [판독]: 표지는 인쇄 눈금으로 **10^(n + 0.445)** (n = 3–10) 에 있다 (두 패널 모두 · 눈금은 10² 와 10¹¹ 가 틀과 정확히 맞는다).  본문 (10⁷–10¹¹ 무영향 · 10⁷ 에서 겹침 0.34 % · 계산 G 범위의 끝 10¹¹) 은 **표지 8 개가 G = 10⁴ … 10¹¹ Pa 일 때** 와 맞는다 (오른쪽 다섯 = 평탄 · 넷째 표지의 겹침 0.342 % = 본문 0.34 %) — 원인 · 어느 쪽이 맞는지 원문으로 가릴 수 없다 [카드 해석 · 미확인].  **겹침 문턱 (0.34 %) · 평탄값은 이 어긋남과 무관하다** (오른쪽 축 값 · 본문 숫자).
- [카드 산술 · 본문 대응을 따를 때] 평탄 (10⁷–10¹¹ 다섯 점) 평균 **28.37°** · 10⁶ → 27.50 (−0.87°) · 10⁵ → 23.89 (−4.5°) · 10⁴ → 13.04 (−15.3°).
- [카드 산술] 겹침의 자릿수당 비 4.38 · 4.50 · 4.63 → 지수 −0.64 · −0.65 · −0.67 ≈ **−2/3** (같은 힘에서 Hertz 겹침 ∝ (F/E*)^{2/3}) — 더미는 중력 하중이라 정적 Hertz 꼴.
- [카드 산술] 고체 분율 = bulk density ÷ 2470: 평탄 (오른쪽 다섯) **0.558–0.575** (평균 0.569 · 기공 ≈ 43 %) → 셋째 표지 0.596 → 둘째 0.744 → 첫째 **1.074** — **1 을 넘는다** = 겹친 구들의 부피 합이 그 부피보다 크다 (겹침 인공물) · bulk density 를 어떻게 셌는지는 원문에 없다 [미확인].
- [판독] 왼쪽 겹침 점선은 1.495 % 원에서 화면 위로 나간다 — 그 직선 조각을 둘째 표지 x 까지 늘이면 ≈5.3 % [외삽 · 표지 아님].
- 두 패널의 'Trendline' 식 · 오차 막대의 뜻 [미확인] (추세선은 안식각 0 · 밀도 3500 까지 늘어진 맞춤선이다).

### 3-5. ★ 쐐기 관입 (p.109–111 · Fig. 5 · 10 · 표 2 · `txt_p3_penetration_setup.png` · `txt_p4_penetration_wedge_protocol.png` · `txt_p5_penetration_results_overlap.png` · `txt_p5_penetration_results_ci_single_particle.png`)
**조건 [인쇄]**: Lommen et al. 2011 관입 시험 · 표 2 = **철광석 펠릿** 값 — G **1 × 10⁸ Pa** · ν **0.2** · ρ **3500** · 구 · d **15 mm** · C_R **0.6** · 입자–입자 정지 마찰 **0.5–1.5** · 경계–입자 정지 마찰 **0.5–1.5** · 입자 **5000** · *"Particles are prohibited from rolling to reduce the effect of their spherical shape."* · 상자 **300 mm × 400 mm** · 쐐기 **8 mm/s** · 밑변 **40 mm** · 각 **30°** · 0.5 N 이 잡히는 순간 깊이 0 · 강성마다 **10 회 반복**.  Fig. 10 에 쓴 마찰 값 (0.5–1.5 가운데) [미확인].

**결과 [인쇄]**: *"the use of a lower stiffness resulted in a lower penetration resistance … The normal overlap increased from 0.013% for 1 × 10¹⁰ Pa to 8% for 1 × 10⁵ Pa."* · *"Simulations using a shear modulus of 1 × 10⁸ Pa or higher, resulting in a normal overlap of 0.3% or less, did not exhibit large differences in average penetration resistance. Moreover, the confidence interval of the mean turned out to be much smaller for softer particles … In the case of stiff particles, a few particles make a large contribution to the penetration resistance, with up to 30% of the total force due to a single particle. When softer particles were used, the maximum contact force was much closer to the average contact force … The decrease in penetration resistance can, however, be compensated by increasing the coulomb friction (Lommen et al., 2011), although this might affect other aspects of the simulation."* (p.111)

**Fig. 10 판독 (관입 일 J · 곡선 추적 · 2 J 아래는 ± 0.15 J)**
| G (Pa) | 20 mm | 40 mm | 60 mm | 끝 (≈64.7 mm) | 10¹⁰ 대비 (끝) [카드 산술] |
|---|---|---|---|---|---|
| 10¹⁰ | 0.88 | 3.85 | 11.14 | **14.16** | 1.00 |
| 10⁹ | 1.05 | 3.60 | 10.58 | **13.36** | 0.94 |
| 10⁸ | 0.73 | 3.47 | 9.31 | **11.23** | 0.79 |
| 10⁷ | 0.38 | 1.80 | 4.89 | **5.98** | 0.42 |
| 10⁶ | 0.21 | 1.03 | 2.71 | **3.18** | 0.22 |
| 10⁵ | 0.08 | 0.54 | 1.31 | **1.50** (64.0 mm) | 0.11 |
- y 축 이름은 *"Penetration resistance (J)"* 이지만 캡션은 *"The work done to penetrate a wedge"* — 누적 일이다.
- [카드 산술] 겹침 0.013 % → 8 % (5 자릿수) = 자릿수당 지수 **−0.56**.
- [판독] 63.2 mm 의 오차 막대: 10¹⁰ **11.75–13.94 J** · 10⁸ **9.49–11.73 J** — 막대가 겹친다 (저자의 '큰 차 없음' 의 근거로 읽힌다 · 막대 = 10 회 반복 평균의 신뢰 구간으로 읽힌다 — 캡션은 막대를 정의하지 않는다 [카드 해석]).

### 3-6. 계산 비용 (p.107 · p.111)
- *"One such method is a reduction of particle stiffness, which allows for bigger time steps and therefore fewer iterations in a simulation."* (p.107) · *"changing the stiffness from 10¹¹ to 10⁷ Pa can decrease the computation time by up to a factor of 100"* (p.111).
- [카드 산술] √(10¹¹/10⁷) = **100** = Δt ∝ G^{−1/2} (Rayleigh 꼴) 의 비 · 같은 범위의 Hertz 충돌 시간 비 (Fig. 2 기울기 −0.4) 는 10^{1.6} ≈ **40** — 원문은 시간 간격 규칙 · 실제 계산 시간 · 장비를 적지 않았다 [미확인].
- 입자 수: 단일 접촉 1 · 벌크 압축 18,000 · 관입 5,000 · 안식각 [미확인].
- 대안: *"Particle scaling could be an alternative to particle stiffness reduction for speeding up simulations."* (p.111).

### 3-7. 원문 안 어긋남 (카드가 본 것)
1. 서론은 시험을 *"angle of repose tests, a separation process, and a tri-axial compression test"* 라고 예고 (p.107) ↔ 실제 = 벌크 압축 (블록 낙하) · 안식각 · 관입 (p.108).
2. 방법은 벌크 압축이 *"the effects of stiffness on the packing of particles and the bulk modulus"* 를 본다고 적었으나 (p.108) 그 시험의 충전 (밀도) 결과는 실리지 않았다.
3. *"became apparent when the shear modulus dropped to 10⁷ Pa"* (p.110) ↔ 바로 다음 *"between 10⁷ and 10¹¹ Pa appears to have no influence"* (p.111) — 10⁷ 이 양쪽에.
4. 그림 9 의 표지 x 위치 = 10^(n + 0.445) (§3-4).
5. 그림 4 의 '24' ↔ 본문 '입자 크기 다섯 배' (20 mm) · '칸 폭 160' ↔ 그림의 가운데 판 160.
6. 문턱이 시험마다 다르다 — 안식각 0.34 % (결과) · 관입 0.3 % · 결론은 둘을 0.3 % 로 묶음 · 벌크 압축의 첫 충돌 평균 겹침은 1 % (10⁸) · 0.33 % (10⁹).
7. 식 (1) 인쇄 꼴 (괄호 안 v⃗_n · n⃗) — §3-1.
8. 벌크 압축을 *"mass-damper system"* 이라 불렀으나 Fig. 6 의 첫 되튐은 자유 비행 (−g) [카드 산술].

---

## 4. ★ 방법 — 계산 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 계산 사슬
G 하나를 고름 (나머지 매개변수 고정) → EDEM Hertz–Mindlin (식 1–5) → (a) 구 하나를 1 m/s 로 벽에 → 평균 힘 · 접촉 시간 / (b) 주기 경계 바닥에 18,000 구 생성 · 가라앉힘 → 50 kg 블록 낙하 → 블록 속도 궤적 → 고유진동수 + 질량 = 벌크 강성 · 충돌마다 들어오고 나가는 속도 = 벌크 반발 (여섯 충돌) / (c) 두 칸 장치에서 옆 판을 내려 더미 → 경사 직선 맞춤 → 안식각 · bulk density · 평균 겹침 / (d) 상자에 5,000 구 → 쐐기 8 mm/s → 깊이별 힘 · 일 · 10 회 반복 → G 를 바꿔 되풀이 (10⁴ … 10¹¹).
- **맞춘 값과 맞춘 대상**: 없음 (스윕).  고정한 값 = 표 1 (유리구) · 표 2 (철광석 펠릿 · Lommen 2011 의 관입 보정에서 옴) · 단일 접촉 · 벌크 압축 매개변수 (출처 없음).
- **검증**: 실험 대조 없음 · 수치 수렴 (시간 간격 · 입자 수) 시험 없음 · 안식각 문턱을 ρ 7800 으로 한 번 더 확인 (그림 없음) · 관입 10 회 반복의 신뢰 구간.

### 4-2. 입자 처리
- **단단한 구 + 겹침** (DEM 표준) — 입자 모양 · 소성 없음 · 접촉마다 독립 (식 1 은 쌍마다 계산).  큰 겹침 (8–10 %) 에서 *"parallel springs and dampers"* 의 집단 효과를 저자가 의심 (p.110).
- 구 모양 효과를 줄이려 **구름을 막음** (관입 · p.109) · 다른 시험은 구름 마찰 계수 μ_r (0.04 · 0.01) — 모델 식 [미확인].
- 우리 대응: DEM = 구 + hooke/hysteresis (CLAUDE.md frame [2]) · 연화 E_eff 1.35 GPa 는 **보정형** (소성 · 재배열 대리) — 이 논문의 **속도형** 연화와 목적이 다르다.

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말했나** — **말했다 (연화 쪽 한계)**:
   - *"However, the limits and drawbacks of this approach are still unclear, and may lead to invalid results."* (p.107 초록)
   - *"However, the pitfalls of a large reduction are still unclear, possibly influencing the simulation results and invalidating the predictions made by DEM."* (p.107)
   - *"When users want to determine a feasible amount of stiffness reduction for their model, they should compare the normal overlaps and not the stiffness or shear modulus, as the latter two do not take differences in the process and particle properties into account."* (p.108)
   - *"Particles are prohibited from rolling to reduce the effect of their spherical shape."* (p.109 — 구 모양 한계의 우회)
   - *"A simulation using a shear modulus of 1 × 10⁴ Pa turned out to be impossible, as the contacts could not generate enough force to reverse the direction of the mass motion."* (p.110)
   - *"It is possible that this was caused by the large number of parallel springs and dampers, as well as the size of the normal overlaps (10%) at this low stiffness (G = 1 × 10⁶ Pa)."* (p.110)
   - *"In the case of stiff particles, a few particles make a large contribution to the penetration resistance, with up to 30% of the total force due to a single particle."* · *"…compensated by increasing the coulomb friction …, although this might affect other aspects of the simulation."* (p.111)
   - *"This research has shown that a reduction in particle stiffness can lead to undesirable effects … Properties such as the bulk stiffness and bulk restitution changed as a result of the stiffness reduction."* · *"…users should be cautious and verify their approach."* (p.111)
   - 수치: 믿을 수 있는 평균 겹침 상한 = 반지름의 **0.3–0.34 %** (안식각 · 관입) · G 하한 10⁴ Pa (계산 불가) · Cleary (2010) 인용 *"average overlaps of 0.1–0.5% are required to ensure that the flow behavior is not dependent on the spring stiffness"* (p.107).
   - ⚠ **'보정값이 물성이 아니다' 는 말은 없다** — 속도용 연화만 다룬다.
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — **말 없음** (소성 0 회).  이 논문의 '우회' = 연화 그 자체 · 비용 = 시간 간격 (최대 100 배 절약 · p.111) · 대안 = 입자 크기 키우기 (p.111).
3. **2D 인가 3D 인가** — **3D** (EDEM 구 · Fig. 3 · 5).  2D · 2D → 3D 전이에 대한 말 없음.
4. **압력을 뺄 때의 거동** — **다루지 않음**.  있는 것 = 블록 되튐 (벌크 반발 · Fig. 6 · 8 · 동적 · 정하중 5.45 kPa [카드 산술]) — 무른 침대가 더 많이 되돌려 준다 (≤ 0.9) · 입자 C_R 로 못 낮춤 (≈0.7).

### 4-4. 기법 미니 용어집
- **Hertz–Mindlin (EDEM)**: 법선 = Hertz (k δ^{3/2}) + 점성 감쇠 (Tsuji 꼴 δ^{1/4}) · 접선 = Mindlin (식 없음) · 강성은 E · ν · R 에서 유도 (식 2–5).
- **강성 감소 (stiffness reduction)**: 계산 시간 간격 (입자 접촉 시간 · Rayleigh 시간에 비례) 을 키우려 E (또는 G) 를 낮추는 것 — 이 논문의 대상.
- **평균 법선 겹침 (÷ 반지름)**: 접촉마다의 δ_n 을 입자 반지름으로 나눠 평균한 것 — 저자의 판정량.
- **벌크 강성 · 벌크 반발**: 블록–침대 계의 고유진동수 (k = m ω²) 와 충돌마다 나가는 / 들어오는 속도의 비.
- **안식각 시험 (두 칸)**: 옆 판을 내려 아래 칸으로 빠지게 하고 위 칸에 남은 더미 경사를 잼.
- **particle scaling**: 입자를 실제보다 크게 그려 입자 수를 줄이는 속도 기법 (이 논문은 이름만 · 미래 과제).

---

## 5. Figure set ★
| 그림 (크롭 파일) | 내용 | 우리 활용 |
|---|---|---|
| Fig. 1 (`fig_1.png`) · Fig. 2 (`fig_2.png`) | 단일 충돌 평균 힘 · 접촉 시간 vs G (10⁴–10¹¹ · d 4 / 8 / 16 mm · log–log) | U5 단위 시험의 Hertz 꼴 기준 (기울기 ±0.40) |
| Fig. 3 (`fig_3.png`) | 벌크 압축 장치 — 블록 + 구 기둥 (Time 0 s) | 시험 꼴 (정적 압밀 아님) |
| Fig. 4 (`fig_4.png`) | 안식각 장치 — 위 칸 · 가운데 판 160 · 틈 24 · 옆 판 · 아래 칸 · α | 장치 치수 (§3-4 어긋남) |
| Fig. 5 (`fig_5.png`) | 관입 — 상자 단면 + 쐐기 | 장비–재료 상호작용 시험 꼴 |
| Fig. 6 (`fig_6.png`) | G 10⁸ 블록 속도 vs 시간 | 되튐 · 자유 비행 (−g) · 고유진동수 [카드 산술] |
| Fig. 7 (`fig_7.png` · 손 크롭) | ★ 벌크 강성 vs G (log–log · 점 7 + 직선) | ★ 'linear correlation' = 기울기 0.59 [판독] |
| Fig. 8 (`fig_8.png`) | 벌크 반발 vs 충돌 1–6 (G 10⁵–10¹¹ + 10⁶ & C_R 0.01) | ★ 연화 → 되튐 ↑ · 입자 C_R 로 못 낮춤 |
| Fig. 9 (`fig_9.png`) · 9a (`fig_9a.png`) · 9b (`fig_9b.png`) | (a) 안식각 + 평균 겹침 (오른쪽 축 %) vs G (b) bulk density vs G | ★ 0.34 % 문턱 · 고체 분율 > 1 인공물 · ⚠ x 위치 반 자릿수 |
| Fig. 10 (`fig_10.png`) | 관입 일 vs 깊이 (G 10⁵–10¹⁰ · 오차 막대) | 장비 힘의 강성 의존 · 힘 꼬리 |
| 표 1 (`tab_1.png` · 다시 자름) · 표 2 (`tab_2.png` · 손 크롭) | 안식각 (유리구) · 관입 (철광석 펠릿) 매개변수 | 재료 · 크기 꼬리표 |
| 식 (1)–(5) (`eq_01_hertz_mindlin_normal_force.png` · `eq_02_hertz_mindlin_stiffness.png` · `eq_03_effective_radius.png` · `eq_04_effective_youngs_modulus.png` · `eq_05_youngs_from_shear_modulus.png`) + 정의 묶음 (`eq_02_05_stiffness_definitions_set.png`) | Hertz–Mindlin 법선 힘 · 강성 · 유효 반지름 · 유효 영률 · E = 2G(1 + ν) | 보고서 DEM 절의 식 그대로 |
| 근거 문단 20 장 (`txt_p1_abstract.png` · `txt_p1_intro_stiffness_reduction_context.png` · `txt_p1_intro_goal_tests_coordination.png` · `txt_p1_single_contact_edem_hertz_mindlin.png` · `txt_p2_overlap_not_stiffness_criterion.png` · `txt_p2_single_contact_setup_results.png` · `txt_p2_methods_three_tests.png` · `txt_p2_bulk_compression_rig.png` · `txt_p3_bulk_compression_protocol.png` · `txt_p3_aor_setup_chamber_glass_beads.png` · `txt_p3_aor_opening_angle_fit.png` · `txt_p3_penetration_setup.png` · `txt_p4_penetration_wedge_protocol.png` · `txt_p4_bulk_compression_results.png` · `txt_p4_soft_restitution_overlaps.png` · `txt_p4_aor_results_start.png` · `txt_p5_aor_results_overlap_034.png` · `txt_p5_penetration_results_overlap.png` · `txt_p5_penetration_results_ci_single_particle.png` · `txt_p5_conclusion.png`) | 초록 · 서론 (Cleary 0.1–0.5 % · 예고한 시험) · 단일 접촉 · 겹침 판정 규칙 · 방법 셋 · 결과 셋 · 결론 | 인쇄 숫자 · 인용 문장의 근거 (파일 이름의 pN = PDF 쪽) |

## 6. Post-processing ★
- **원문이 한 것**: 단일 충돌 평균 힘 · 접촉 시간 · 블록 궤적의 고유진동수 → 벌크 강성 · 충돌마다 속도 비 → 벌크 반발 · 더미 경사 직선 맞춤 · 평균 법선 겹침 ÷ 반지름 · bulk density · 관입 힘 → 일 · 10 회 반복 평균 · 신뢰 구간 · 그림 7 의 직선 · 그림 9 의 추세선 (식 없음).
- **이 카드의 후처리**: 그림 10 장 모두 내장 래스터 (xref 17 · 18 · 41–43 · 58–60 · 75 · 76) → 판독 7 장을 원본 화소에서 (눈금 표시를 화소로 찾아 축 맞춤 · 표지 = 열 단면 / 열림 연산 / 이진 틀 맞춤 / 원 맞춤 · 곡선 = 색 마스크 추적) → digitized.csv 182 행 · Fig. 7 기울기 · Fig. 9 x 어긋남 · 겹침 지수 · 고체 분율 · Fig. 6 자유 비행 · 고유진동수 → 강성 · Fig. 6 ↔ 8 대응 · Hertz 충돌 해 대조 · 비용 비 · 2 차 인용 카드 대조 (coetzee2017 · paulick2015 · roessler2019).  스크립트 = 이 묶음 scratchpad (`dig_fig7.py` · `dig_fig8b.py` · `dig_fig9.py` · `dig_fig12b.py` · `dig_fig6*.py` · `dig_fig10b.py` · `write_digitized.py` · `arith.py`) — 결과는 `digitized.csv` 에 남겼다.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · 정본 비교 문서 출처를 병기해 적는다)

### 7-1. 비교표 (모든 행에서 **재료 · 크기 · 응력 영역이 다르다**)
| 항목 | 이 논문 | 우리 | 같음 / 다름 · 왜 |
|---|---|---|---|
| 연화의 목적 | **계산 시간** (Δt ↑) | DEM E_SE 24 → **E_eff 1.35 GPa (÷17.8)** = 소성 · 재배열 · 입계 미끄럼의 **대리** · 실측 기공 · Cronau 겹침에 맞춤 (CLAUDE.md frame [2] · E_SE 보정 절) | **다름** — 이 논문의 '안전 범위' 로 우리 연화를 방어하거나 재지 않는다 (`coetzee2017` 카드의 (a) 보정 / (b) 계산속도용 구분 — "우리 18× 연화는 (a)다" · 비교 문서 A 절 Coetzee 블록 ④) |
| 판정 자 | 평균 법선 겹침 ÷ 반지름 **0.3–0.34 %** | 순수 SE ⟨δ⟩ ≈ 지름의 11–12 % = **반지름의 22–24 %** (CLAUDE.md E_SE 보정 절 · 비교 문서 A 절 Coetzee 블록 ④ · `coetzee2017` 카드 "우리 오버랩은 그 창 밖 20–100×") | [우리 산술] 65–80 배 — 그러나 응력 영역이 다르다 (아래 7-3) |
| G | 스윕 10⁴–10¹¹ · 표 2 철광석 1 × 10⁸ Pa | E_eff 1.35 GPa · ν 0.3 (DEM 설정 · CLAUDE.md) → **G ≈ 0.52 GPa** [우리 산술] | G 로만 보면 저자의 '안전' (≥ 10⁷) 안이지만 저자 자신이 **G 가 아니라 겹침으로** 판정하라고 한다 |
| 접촉 법칙 | Hertz–Mindlin (δ^{3/2}) + δ^{1/4} 감쇠 | LIGGGHTS hooke/hysteresis | 지수 (K ∝ G^0.59 · F ∝ G^0.40) 를 옮기지 않는다 [카드 해석] |
| 벌크 강성 | ∝ G^0.59 [판독] · 동적 · 5.45 kPa | E_eff 가 300 MPa 도달 기공을 정한다 (비교 문서 A 절 제목 · MPM E-sweep 24 → 33–38 % · 1.35 → 8 %) | **방향 같음** (입자 강성이 벌크 순응을 정한다) · 꼴 · 크기 · 응력 다름 |
| 되튐 | 무를수록 벌크 반발 ↑ (G 10⁵: 0.72–0.91) · 입자 C_R 0.01 로 0.62–0.74 [판독] | 언로딩 (탈압 · 되돌아옴) 시험 = 등록 단계 | 경고로만 — 동적 블록 되튐 ≠ 정적 탈압 |
| 밀도 · 기공 | 안식각 더미 고체 분율 0.558–0.575 (평탄 · 평균 0.569) → **1.074** (가장 무른 점) [카드 산술] · 유리구 · 중력 | 순수 SE 랩 표준 기공 **10–13 %** · LPSCl 진밀도 **1.64 g/cm³** (CLAUDE.md 1저자 11-10 Q5 · 고정) · 조밀 순수 SE 의 ε_sphere 음수 = 겹침 인공물 (CLAUDE.md E_SE 보정 절) | **랩 표준과 다른 문헌 값** (유리구 더미 · 기공 ≈43 %) — 값 비교 아님 · 같은 부류의 인공물 (구 부피 합 > 공간) 만 같다 |
| 소성 · 모양 | 없음 | DEM 없음 (연화로 대리) · MPM J2 (E 1.53 · σ_y 0.30 · ν 0.49) | 이 논문은 MPM 쪽 대조점이 없다 |
| 차원 | 3D | DEM 3D · MPM 2D / 3D | — |
| 응력 | 중력 · 1 m/s 충돌 · 블록 5.45 kPa · 쐐기 | 300 MPa 냉간 압축 | 5.5 × 10⁴ 배 |

### 7-2. ★ 'linear correlation' — 우리 문서의 선형 표현과 나란히 (판정 없이 · 남의 줄은 고치지 않는다)
- 원문 문장 = *"linear correlation"* (p.110) · 그림 = log–log 직선 · 기울기 **0.591** (점 · 그린 선 모두) [판독].
- `paulick2015_elastic_…` 카드 L170 (G **∝** 벌크강성) · `coetzee2017_…` 카드 L230 (선형함수) · 비교 문서 A 절 (Paulick 블록 ① 표 · Coetzee 블록 ⑤) 의 '선형' 은 **비례로 읽으면 원문 그림과 다르다** — 6 자릿수 G 에 강성은 3,669 배 (비례면 10⁶ 배).
- ⚠ 그래도 **단조** 라는 점은 맞다 → "원하는 벌크 강성을 주는 G 를 고를 수 있다" 는 역함수 논리 (`paulick2015_elastic_…` 카드 L163–165 · 비교 문서 A 절 Paulick 블록 ②) 는 단조성만으로 선다 [카드 해석].

### 7-3. ★ [우리 산술] 0.3 % 문턱을 압밀 (300 MPa) 로 옮길 수 없는 이유
- 같은 E 에서 Hertz 겹침 ∝ (σ/E)^{2/3} (이 논문 안식각 겹침의 지수 −0.64 ~ −0.67 도 같은 꼴 [카드 산술]).  응력이 블록 정하중 5.45 kPa → 300 MPa (**5.5 × 10⁴ 배**) 가 되면 같은 E 에서 겹침은 **≈1.4 × 10³ 배** (기준 응력 = 블록 정하중 · 안식각 더미 · 관입 상자의 응력은 원문에 없음 [미확인]) — 저응력에서 0.3 % 였던 계는 압밀 응력에서 구 모형 자체가 깨지는 겹침이 된다.
- ⇒ 이 논문의 문턱은 **저응력 유동 · 장비 상호작용** 의 판정선이지 **압밀 (수백 MPa)** 판정선이 아니다.  우리 순수 SE ⟨δ⟩ (반지름의 22–24 %) 가 문턱을 넘는 것은 연화 탓만이 아니라 응력 영역 탓이다 — 그 영역의 겹침 처리 (Stage-E 면적 상한 · ε_sphere 규약) 는 우리 쪽 규약이 맡는다 (CLAUDE.md E_SE 보정 절).

### 7-4. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: DEM (구 · 탄성 접촉) 에서 **입자 강성 선택이 벌크 응답에 들어가는 꼴** — 충돌 (±2/5) · 벌크 강성 (0.59) · 반발 (연화 ↑) · 유동 (문턱 0.3 %) · 장비 힘 (꼬리 · 평균).  ⇒ 우리 DEM 의 E_eff 가 **물성이 아니라 벌크를 정하는 보정 손잡이** 라는 frame [2] 서술의 **문헌 쪽 근거** (방향만).
- **없는 것**: 압밀 · 소성 · 모양 · 복합체 · 수송 · 탈압 · MPM · 실험.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa · σ_y_eff 46 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 (K 25.5 GPa) / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  이 논문 재료 = mm 구 (유리 · 철광석 펠릿 값) — 모든 행에 "재료 · 응력 다름".)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ 두 가지 — ① **겹침 분포 (÷ 반지름) 를 결과와 함께 보고할 칸으로 등록**: 저자 판정 규칙 *"compare the normal overlaps and not the stiffness or shear modulus"* (p.108) ② **겹침이 크면 '구 부피 합' 밀도가 공간을 넘는다** — 안식각 더미 고체 분율 1.074 (Fig. 9b · 가장 무른 점 [카드 산술]) = 우리 ε_sphere 음수와 같은 부류 → 기공 연산자 (ε_sphere / ε_union) 규약을 결과 전에 적는다 · bulk density 를 어떻게 셌는지 원문에 없어 [미확인] 이라는 것도 반면교사 | 압밀 기공 숫자 · LPSCl 값 |
| **단계 1** (3D 메모리 · 장 수) | 없음 | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 없음 (충돌 단위 시험의 Hertz 기준값은 U5 칸) | — |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 간접 — DEM 에서는 **강성 하나가 도달 밀도 · 벌크 강성을 같이 바꾼다** (Fig. 7 · 9b) → MPM 에서 σ_y 하나를 기공에 맞출 때 E (1.53) 를 같이 고정해 등록해야 '맞춘 값 하나' 가 성립 [카드 해석] | MPM · 소성 없음 |
| **단계 5** (3D 복합 압밀) | 관입: **단단한 입자에서 한 입자가 힘의 30 %** · 연화가 힘 꼬리를 깎고 평균까지 낮춤 (p.111) → AM (140 GPa) : SE (1.35 GPa) 강성 비 ≈104 [우리 산술] 인 우리 DEM 의 AM 하중 몫 · 힘 사슬 꼬리는 강성 선택에 묶인다 [카드 해석] | AM · SE 혼합 계산 없음 · 하중 몫 숫자 없음 |
| **단계 6** (탈압 · 되돌아옴) | ★ 경고 — 연화 DEM 의 **되튐 (반발) 은 강성 선택에 묶이고 입자 C_R 로 못 낮춘다** (G 10⁶: C_R 0.5 → 0.01 이 벌크 반발 0.66–0.85 → 0.62–0.74 [판독]) · 저자 추정 원인 = 많은 병렬 스프링 · 댐퍼 + 10 % 겹침 → DEM 탈압 되돌아옴을 결과 전 대조에 쓸 때 연화의 몫을 분리해 등록 | 정적 탈압 · springback 숫자 없음 (동적 블록 · 5.45 kPa) |
| **단계 7** (형상 · 피복 · 수송) | 겹침 = 접촉 면적의 원천 (Hertz a ∝ √(Rδ)) 이라 연화가 면적 · 힘 분포를 바꾼다는 정성 · 힘 꼬리 30 % → Holm 망 (면적 분포) 에 같은 경고 (`paulick2015` 카드 ③ Xu 와 같은 결론) [카드 해석] | 면적 · 수송 숫자 없음 |
| **후보 D0** (지금 DEM) | ★★ 핵심 — ① 이 논문의 연화 = **속도형 (b)** · 우리 18× = **보정형 (a)** → **Lommen 의 '바꾸지 않는 범위' 로 우리 연화를 방어하지 않는다** ② 우리 G ≈ 0.52 GPa 는 G 기준 '안전' 이지만 저자는 **겹침으로** 판정하라 했고 우리 겹침 (반지름의 22–24 %) 은 문턱의 65–80 배 [우리 산술] — 단, 응력 영역 차 (7-3) 때문에 이것은 '연화가 결과를 바꾼다' 의 증거가 아니라 '이 문턱이 해당 없음' 의 증거 ③ 벌크 강성 · 반발이 입자 강성을 따른다 = **E_eff 는 벌크를 정하는 손잡이 (물성 아님)** 라는 frame [2] 서술의 문헌 근거 (방향) | 압밀 영역 검증 · 우리 접촉 법칙 (hooke) 의 지수 |
| **후보 A′-0** (판 · 벽 · AM 자리 접촉 규칙) | 경계 마찰을 따로 둔 예 (관입: 입자–입자 · 경계–입자 정지 마찰 각 0.5–1.5) · 판–입자 = 입자–입자 값 (벌크 압축) · **마찰로 강성 손실을 보상하면 다른 것이 바뀐다** (p.111) → 경계 규칙 매개변수를 다른 매개변수의 보상에 쓰지 않는다 [카드 해석] | 미끄럼 · 분리 규칙 식 · 값의 근거 |
| **후보 A · A′** (MPM 강체 AM · 입자별 속도장) | 없음 (MPM 아님) | — |
| **후보 B** (입자별 FE + 접촉) | 없음 | — |
| **후보 C** (큰 변형 접촉 DEM · MDR 류) | 동기 — Hertz 점접촉 DEM 이 **겹침 8–10 %** 에서 '병렬 스프링 · 댐퍼' 문제를 낸다는 저자 관찰 (p.110) · 평균 겹침 0.3 % 를 넘으면 장비 힘이 줄고 매끄러워진다 (p.111) [카드 해석: 큰 겹침에서 점접촉 법칙의 대안이 필요한 이유의 한 예] | 큰 변형 법칙 · 대안 비교 없음 |
| **후보 C′** (항복 캡 탄소성 접촉 DEM) | 없음 (탄성 + 점성만) | — |
| **후보 M0** (균질화 압밀) | 없음 | — |
| **U0–U6** | **U5** (비슷한 강성 입자 충돌) — 구–벽 1 m/s 충돌의 Hertz 꼴 기준: 힘 ∝ G^{0.40} · 시간 ∝ G^{−0.40} · d 4 mm · G 10⁸ · ρ 1500 · ν 0.25 에서 t_c 판독 **1.16 × 10⁻⁴ s** ↔ Hertz 해 1.07 × 10⁻⁴ s (같은 재료 벽 · 감쇠 없음 [카드 산술]) — 우리 충돌 해 점검의 외부 대조값 (벽 물성 [미확인] 꼬리표와 함께) · **U6** (작은 조밀 충전 압축의 수렴) — 블록 낙하 벌크 강성처럼 **동적 시험의 '강성' 은 정의 (고유진동수 · 질량) 를 같이 적어야 한다** (원문은 구간 · 질량을 안 적음 [미확인]) | U1 · U2 · U3 · U4 없음 |
| **R1–R7** | **R4** (탈압 · 되돌아옴) — 위 단계 6 경고 · **R5** (맞추는 값은 모델마다 하나) — 강성을 낮춰 잃은 관입 저항을 **마찰로 보상** 하면 *"might affect other aspects of the simulation"* (p.111) = 두 값이 서로를 보상하는 함정의 예 · **R6** (SE 형상 변형) 반대편 — 구 모양 효과를 **구름 금지** 로 누름 (p.109) | R1 · R2 · R3 · R7 없음 |
| **결과 전 대조 항목** | (흐름 밖 포함) ① U5 충돌 기준 (위) ② 연화 DEM 의 겹침 분포를 결과와 함께 보고 (문턱 0.3 % 는 **저응력 유동** 값이라는 꼬리표) ③ 'K ∝ G^0.59' 는 Hertz–Mindlin · mm 구 · 블록 낙하의 값 — 우리 hooke DEM 으로 옮기지 않는다 | LPSCl · 압밀 · 탈압 값 없음 |

- **재료 · 차원 · 조건 차이**: mm 구 (d 4 · 8 · 15 · 16 mm) ↔ µm (SE ⌀1–3 · AM 수–십 µm) · 유리 · 철광석 펠릿 값 ↔ LPSCl · NCM · 3D ↔ 3D · 중력 · 충돌 · kPa ↔ 300 MPa · Hertz–Mindlin ↔ hooke/hysteresis · 실험 대조 없음.

## 9. 적용 인사이트 (행동)
1. **연화를 말할 때 배수가 아니라 겹침 분포를 함께 적는다 (단계 0 · D0)** — 이 논문의 판정 규칙 (p.108).  우리 DEM 보고서 · 원장에 "E_eff 1.35 GPa (÷17.8)" 옆에 "⟨δ⟩/R (순수 SE 22–24 %) · 응력 300 MPa" 를 같이 둔다 (`paulick2015_elastic_…` 카드의 "배수는 옳은 자가 아니다 — 옳은 자는 결과 오버랩" 과 같은 결론).
2. **이 논문을 '우리 연화가 안전하다' 의 근거로 쓰지 않는다** — 속도형 연화의 문턱이고 응력 영역이 5.5 × 10⁴ 배 다르다 (7-3).  쓸 수 있는 문장은 "DEM 에서 입자 강성은 벌크 강성 · 반발 · 장비 힘을 바꾼다 (Lommen 2014)" — 즉 E_eff 는 보정 손잡이다.
3. **'linear correlation' 을 옮길 때 기울기 0.59 를 같이 적는다** — "벌크 강성 ∝ 입자 강성" 이라 쓰지 않는다 (coetzee · paulick 카드 · 비교 문서 A 절의 선형 표현에 대한 원문 쪽 근거 · 남의 줄은 고치지 않음).
4. **연화 DEM 의 되돌아옴 (단계 6 · R4) 은 강성 선택에 묶인다** — 입자 C_R 로는 못 낮춘다 (Fig. 8) · 탈압 계산을 등록할 때 'E_eff 를 바꾸면 되돌아옴이 어떻게 바뀌나' 팔을 결과 전에 둘지 정한다.
5. **보상 매개변수의 함정 (R5)** — 강성 손실을 마찰로 메우면 다른 응답이 바뀐다 (p.111) · 우리 보정에서 E_eff 와 마찰 · 점착 (CED) 을 서로의 보상에 쓰지 않는다.
6. **흐름 밖: 믹서 Ⓒ** — 믹서 DEM 의 시간 간격용 연화 (Bo · 충돌 많은 계) 는 이 논문의 '충돌이 많으면 강성이 중요' (p.108) · 반발 (Fig. 8) 경고에 바로 걸린다 → 믹서 팔의 E 배수를 바꿀 때는 겹침 · 반발을 같이 보고 (`stewart2001` · `chandratilleke2010` 카드의 연화 E 와 같은 묶음).

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "In EDEM Hertz–Mindlin simulations of millimetre-sized spheres, reducing the particle shear modulus from 10¹¹ to 10⁷ Pa left the angle of repose unchanged and the average penetration resistance changed little for G ≥ 10⁸ Pa, as long as the average normal overlap stayed below about 0.3 % of the particle radius; bulk stiffness and bulk restitution, however, followed the particle stiffness over the whole range (Lommen et al., *Particuology* 12 (2014) 107–112)."
- "Lommen et al. (2014) recommend judging a stiffness reduction by the resulting normal overlap rather than by the modulus: 'they should compare the normal overlaps and not the stiffness or shear modulus'."
- ⚠ 쓰지 말 것: "bulk stiffness is proportional to particle stiffness (Lommen 2014)" — 원문 그림은 log–log 기울기 ≈0.59 [판독].
- 국문 (조건과 함께): *"mm 구의 Hertz–Mindlin DEM 에서 G 를 10¹¹ → 10⁷ Pa 로 낮춰도 안식각은 그대로였지만 (평균 겹침 < 반지름의 0.3 %), 벌크 강성과 반발은 강성을 따라 바뀌었다 (Lommen 2014) — 저응력 유동의 결과이고 압밀 (수백 MPa) 의 판정선이 아니다."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**
1. 연화의 한계 · 단점이 아직 불분명하고 잘못된 결과를 낼 수 있다 (p.107).
2. 충돌이 많은 계에서는 강성이 결과를 바꾼다 (p.108).
3. 무른 침대의 반발을 입자 C_R 로 못 낮춤 — 병렬 스프링 · 댐퍼 · 10 % 겹침 추정 (p.110).
4. 관입 저항을 마찰로 보상하면 다른 것이 바뀔 수 있다 (p.111).
5. 벌크 강성 · 반발 · 전단 · 장비 상호작용 모델에서는 조심하고 검증하라 (p.111).

**카드가 본 한계 · 원문 안 어긋남**
6. **실험 대조 · 수치 수렴 시험이 없다** — '바뀌지 않는다' 는 강성끼리의 비교일 뿐 참값 대조가 아니다.
7. **문턱은 평균 겹침** — 분포 · 최대 겹침은 보고되지 않았다 · 시험마다 0.34 / 0.3 / 1 (첫 충돌 10⁸) / 0.33 % (10⁹) 로 다르다.
8. **그림 9 의 x 위치 반 자릿수 어긋남** (§3-4) · 그림 4 치수 (§3-4) · 서론의 시험 예고 (§3-7).
9. **벌크 압축 = 블록 낙하 동적 시험** — 첫 되튐은 자유 비행 (−g) 이라 '질량–스프링' 고유진동수의 정의가 구간에 따라 달라진다 [카드 산술] · 추출 구간 [미확인].
10. 시간 간격 · 계산 시간 · 벽 물성 · 벌크 압축 입자 지름 · 안식각 입자 수 · 관입에 쓴 마찰 값 · 추세선 식 · 오차 막대의 뜻 — [미확인].
11. **'linear correlation' = log–log 직선** (기울기 0.59) — 낱말만 옮기면 비례로 읽힌다 (실제 2 차 인용 두 카드).
12. **전이 한계**: mm 구 · 유리 / 철광석 값 · 중력 · 충돌 · kPa · Hertz–Mindlin — LPSCl · NCM · 300 MPa · hooke DEM 에 숫자를 옮기지 않는다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 서지 (원문 목록 그대로) | 왜 |
|---|---|
| Malone, K. F., & Xu, B. H. (2008). Determination of contact parameters for discrete element method simulations of granular systems. Particuology, 6(6), 521–528. | ★ 겹침으로 강성 감소량을 정하는 규칙의 출처 (이 논문 p.108) · 연화 이득 (*"lower stiffness values can benefit users without significantly altering results"*) — 카드 없음 |
| Cleary, P. W. (2010). DEM prediction of industrial and geophysical particle flows. Particuology, 8(2), 106–118. | ★ "평균 겹침 0.1–0.5 %" 관행의 원전 (p.107 · p.111) — 카드 없음 (coetzee 카드가 [233] 로 인용) |
| Kruggel-Emden, H., Simsek, E., Rickelt, S., Wirtz, S., & Scherer, V. (2007). Review and extension of normal force models for the discrete element method. Powder Technology, 171(3), 157–173. | 법선 힘 모델 비교 (탄성 · 탄소성 포함) — 접촉 법칙 후보 (C · C′) 표 · 카드 없음 (여러 카드가 인용만) |
| Kruggel-Emden, H., Wirtz, S., & Scherer, V. (2008). A study on tangential force laws applicable to the discrete element method (DEM) for materials with viscoelastic or plastic behavior. Chemical Engineering Science, 63(6), 1523–1541. | 점탄성 · 소성 재료의 접선 법칙 — 카드 없음 |
| Härtl, J., & Ooi, J. (2008). Experiments and simulations of direct shear tests: Porosity, contact friction and bulk friction. Granular Matter, 10(4), 263–271. | '강성 감소가 결과에 영향 없음' 쪽 근거 (p.107 · 직접 전단 · 기공) — 카드 없음 (coetzee · morrissey 카드가 인용) |
| Lommen, S. W., Schott, D. L., Rahman, M., & Lodewijks, G. (2011). The penetration of iron ore pellets: Calibrating discrete element parameters using penetration tests. In Proceedings of the 11th Particulate System Analysis Conference Edinburgh, UK, (p. 5). | 표 2 매개변수 (G 1 × 10⁸ 포함) 와 마찰 보상의 출처 — 학회 논문 · 카드 없음 |
| Tsuji, Y., Tanaka, T., & Ishida, T. (1992). Lagrangian numerical simulation of plug flow of cohesionless particles in a horizontal pipe. Powder Technology, 71(3), 239–250. | 식 (1) 감쇠 꼴 (δ^{1/4}) 의 원전 — 카드 없음 |
| Huang, H., Tutumluer, E., Hashash, Y. M. A., & Ghaboussi, J. (2008). Contact stiffness affecting discrete element modelling of unbound aggregate granular assemblies. In Advances in transportation geotechnics. CRC Press. | '강성은 중요' 쪽 근거 — 책 장 |
| Masson, S., & Martinez, J. (2000). Effect of particle mechanical properties on silo flow and stresses from distinct element simulations. Powder Technology, 109(1-3), 164–178. | 사일로 응력의 강성 의존 — 카드 없음 |
| Zhang, X., & Vu-Quoc, L. (2000). Simulation of chute flow of soybeans using an improved tangential force–displacement model. Mechanics of Materials, 32(2), 115–129. · Zhu, H. P., Zhou, Z. Y., Yang, R. Y., & Yu, A. B. (2007). Discrete particle simulation of particulate systems: Theoretical developments. Chemical Engineering Science, 62(13), 3378–3396. | 접촉 모델 배경 (서론) |

## 13. [미확인] 목록 (원문 6 쪽 전수에 없음)
1. 시간 간격 규칙 · 실제 계산 시간 · 장비 (속도 '최대 100 배' 의 근거 계산).
2. 단일 접촉 시험의 벽 물성 (Hertz 해 비 1.09 ↔ 1.44 를 가르는 값).
3. 벌크 압축 시험의 입자 지름 · 밀도 숫자 · 침대 높이 · 고유진동수 추출 구간 · 질량.
4. 안식각 시험의 입자 수 · 계산한 G 목록 · bulk density 를 센 방법 · 오차 막대의 뜻 · 추세선 식 · 그림 9 x 위치가 반 자릿수 어긋난 이유.
5. 관입 시험 (Fig. 10) 에 쓴 마찰 값 (표 2 의 0.5–1.5 가운데) · 표 2 의 G 1 × 10⁸ 를 맞춘 대상 (Lommen 2011).
6. 접선 (Mindlin) 힘 · 구름 마찰 모델 · c_HM(C_R) 식.
7. 겹침의 분포 · 최대값 (평균만 보고).
8. 그림 4 의 '24' 단위 · '칸 폭 160 mm' 가 그림의 어느 치수인지.

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-12)
- PDF 6 쪽을 글자 층 추출 (블록 좌표 · 그리스 문자 · 위첨자 깨짐 → 렌더로 확인) + 전 쪽 130 dpi 렌더 + 크롭 300 dpi 렌더로 읽음.  서지 = p.107 머리글 · 제목 · 저자 · 소속 · 접수 / 수정 / 수락 · 키워드 · 초록 · 바닥 (ISSN 1674-2001 · © 2013 · DOI) · p.112 감사 (NEMAG) · 참고문헌 11.  SI 없음.  원문 낱말 셈 (글자 층): plastic = 본문 0 (참고문헌 제목 1 = Kruggel-Emden 2008 *"viscoelastic or plastic behavior"*) · yield · 2D · two-dimensional · unload · deform · Rayleigh = 0 · porosity = 본문 0 (참고문헌 제목 1 = Härtl & Ooi) · overlap 15 · *"linear"* 2 (Fig. 7 의 *"linear correlation"* · 안식각의 *"linear curve fitting"*) · coordination 1 · periodic 1 · time step 2.
- 그림 크롭 **40 장** = 도구 10 (Fig. 1–6 · 8 · 9 · 10 그대로 · **표 1 다시 자름** (도구가 쪽 아래 2/3 를 통째로 잡음) · 캡션 고침 4 = Fig. 6 위첨자 · Fig. 8 둘째 줄 · Fig. 10 하이픈 · 표 1 제목) + 손 크롭 30 (그림 7 · 표 2 (도구가 놓침 — 캡션이 쪼개진 글 덩어리) · 패널 9a · 9b (첫 시도 321 pt 경계는 (b) 의 y 축 제목이 섞이고 잘려 두 패널 사이 빈 열 308.5 pt 로 다시 렌더) · 식 6 · 근거 문단 20).  40 장 전부 Read 로 열어 확인 · `figures.json` 의 `recrop` · `manual_crop` · `caption_fix` · `note_manual`.  `--audit` 경고 없음.
- 판독: 그림 10 장 모두 내장 래스터 → Fig. 1 · 2 · 6 · 7 · 8 · 9 · 10 을 원본 화소에서 (digitized.csv 182 행 · 방법은 note 칸).
- 2 차 인용 대조: `roessler2019` L236 (가리킨 카드) · `coetzee2017` L230 · L689 · `paulick2015_elastic_…` L170 · L464 · L569–572 · L585–588 · L591–592 · L656 · L909 — 고치지 않았다 (카드 문제 = 정독 출력 batch_87 의 "카드 문제" 절).
- 정본 litdb 중복 확인: `git ls-tree` (papers/ 562 장) + `git grep` (DOI `partic.2013.03.006` · 'DEM speedup' · 'Stiffness effects on behavior' · 'Lodewijks' · 'Lommen' · 'Particuology, 12' · '107–112') — 카드 없음 (인용만: roessler2019 · coetzee2017 · paulick2015_elastic) (2026-11-12).

## 🔗 관련 카드
- 이 논문을 인용한 카드: `roessler2019_dem_cohesive_aor_cylinder_lift_calibration` (참고문헌 L236) · `coetzee2017_dem_calibration_review` (ref [81] · §7 강성 감소) · `paulick2015_elastic_particle_properties_dem_review` (ref [23] 'Lommen 2013').
- 연화 영률 · 시간 간격 묶음: `chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer` (연화 E 2.16 × 10⁶ · 시간용) · `stewart2001_dem_pept_bladed_mixer_detailed_comparison` (연화 E 고정 · 유동 검증) · `hare2026_dem_pept_dry_mixing_nmc622_eirich` (보정형 연화의 실험 검증 선례) · `morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis` (EDEM · 철광석 · 벌크 강성 ↔ G 타협).
- 접촉 강성 실측 · 보정: `paulick2015_particle_contact_stiffness_two_particle_method` · `roessler2019_dem_cohesive_aor_cylinder_lift_calibration` (CED · E · R 봉인).
- 큰 겹침 · 다접촉 쪽: `brodu2015_multiple_contact_dem_dense_granular` · `harthong2009_high_density_compaction_dem_voronoi_contact_law`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

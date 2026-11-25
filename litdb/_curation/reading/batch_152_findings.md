# batch 152 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-23 · 후보 표 N-150 · 새 카드)

대상: `chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed` — Bodhisattwa Chaudhuri · Amit Mehrotra · Fernando J. Muzzio · M. Silvina Tomassone\*, "Cohesive effects in powder mixing in a tumbling blender", *Powder Technology* 165 (2006) 105–114 · DOI 10.1016/j.powtec.2006.04.001.
Walton–Braun 이력 스프링 + Walton 증분 미끄럼 DEM 에 '정사각 우물' (접촉 중 상수 인력 · K = F_cohes/mg) 점착을 넣어, 부분 충전 회전 드럼 (본문 지름 9 cm · 길이 1 cm) 의 같은 크기 (2 mm) · 크기 1 : 1.5 이원계 혼합을 분리 세기 I = σ²/σ0² 로 5 바퀴까지 본 계산 + Avicel PH101 영상 정성 대조.
쪽 = PDF 쪽 p.1–10 (인쇄 105–114) · p.5 = 가로 쪽 (그림 3) · SI 없음 · 고른 의도 대조 = **일부** ('점착 ↑ → 혼합 속도 증가 → 감소' · '쌍 힘 대비로 무늬가 달라짐' · '점착 혼합은 빠른 회전이 낫다' 채움 (단 증가는 K 0.1 의 끝 값 하나 · 회전은 K 120 하나) / '점착 × rpm 지도' 는 두 자름뿐 / G1 일부 · G4 없음 / 코팅 DEM · 측정 점착 입력 없음 · 카드 §0-1).
인용 서지 (질문 k · l 용): B. Chaudhuri, A. Mehrotra, F.J. Muzzio, M.S. Tomassone, *Powder Technology* 165 (2006) 105–114, DOI 10.1016/j.powtec.2006.04.001.
⚠ 이 PDF 의 글자 층은 '=' → '¼' · '+' → 'þ' · '( )' → 'ð Þ' · '×' → 제어 문자로 깨진다 — 식 · 기호 · 숫자는 렌더 (300–400 dpi) 에서 확인 · 곡선 값은 벡터 경로 꼭짓점 ([판독 · 벡터] · `digitized.csv`).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (압밀 · 기공 숫자 0 — 혼합 단계 DEM).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
- [b] chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed | **접촉 하나 수준만** — Walton–Braun latching spring 의 되돌림 가지 F_N = K2(α1 − α0) (누름 F_N = K1α1 · 잔류 겹침 α0) · e = (K1/K2)^½ = 0.7 (입자) · 0.5 (벽) · 표 1 강성은 하나 (6000 N/m) 라 K2 는 [미확인] (6000 = K1 이면 K2 12,245 · 24,000 N/m [카드 산술]) · 덩어리 탈압 · 되돌아옴 없음 | 카드 §3-1 · p.2 · 표 1 · `eq_inline_a` · `eq_inline_b` | 인쇄 · 카드 산술 · 미확인 | 2 mm 가상 구 · 혼합 충돌의 소산 모델 (압밀 탈압 아님)

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 (항복 판정 없는 선형 이력 스프링 · 재료 항복 · 경도 값 0).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음.

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed | 큰 변형 한계 진술 없음 — 쓴 법칙 = **가장 단순한 점착 소산 조합**: Walton–Braun 선형 이력 (K1 · K2) + Walton 증분 미끄럼 (T_{t+1} = T_t + k_TΔs · F_t ≤ μ_sF_n · F_n = 점착 + 전달 무게) + 정사각 우물 상수 점착 (겹침 · R\* 무관 · 작용 거리 [미확인]) · 강성 조건은 *"large enough to ensure that the overlaps α1 and α0 remain small compared to the particles sizes"* 뿐 (p.2) · 맞춘 값 = K 하나 (K 60 ↔ Avicel 영상 · 절차 없음) · 강성 · 마찰 · 반발 = 고른 값 (표 1) · 검증 = 영상 정성 | 카드 §3-1 · §4-2 · p.2–4 · 표 1 | 인쇄 · 미확인 | 압밀 밀도 영역 · 다접촉 · 항복 없음

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음.

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed | **말 없음** — 3D DEM (*"second order scalar equations in three dimensions"* p.3) 이지만 드럼 길이 1 cm (작은 입자 지름 5 개 · 끝판 마찰 0) 의 얇은 슬랩 · 스냅숏 = *"two-dimensional viewing plane"* (p.8) · 실험은 길이 42 cm 원통을 끝에서 찍은 사진 · 슬랩 ↔ 긴 원통 · 2D ↔ 3D 진술 없음 · I 의 칸이 3D 인지 단면인지 [미확인] | 카드 §4-3 (iii) · p.3 · p.8 | 인쇄 · 미확인 | —

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed | 가압 · 탈압과 닿는 것 없음 — 원문이 적은 한계는 혼합 쪽: 정전기 미포함 (각주 2 *"Improvement of this model can be achieved by including electrostatic forces explicitly"*) · *"All the values reported here are for the system as described in Table 2, and are strongly scale dependent"* (p.9) · *"the optimum values of bond numbers are scale dependent"* · *"The existence of an optimal mixing state is still an open question"* (p.10) · 크기 다른 계의 점착 효과는 *"more complex than originally thought"* (p.10) | 카드 §3-10 · p.2 · p.9–10 | 인쇄 | 압밀 전 혼합 상태 (압밀 DEM 출발 배치의 정성 근거로만)

## k — DEM 의 한계
- [k] chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed (B. Chaudhuri · A. Mehrotra · F.J. Muzzio · M.S. Tomassone, *Powder Technol.* 165, 105–114, 2006) | **말 있음 (일부 · 큰 변형 · 점접촉 한계는 아님)** — ① 점착 세기를 '무게의 몇 배' 로 정의한 편의 척도: *"Notice that we are not claiming that cohesive forces depend on the particle weight. This is just a convenient way of defining how strong cohesion is, as compared to the particle weight"* (각주 1 · p.2) ② 정전기 없음 (각주 2) ③ 최적값의 규모 의존: *"All the values reported here are for the system as described in Table 2, and are strongly scale dependent"* (p.9) · *"the optimum values of bond numbers are scale dependent"* (p.10) — [카드 추론] K 를 *"independent of particle size"* (p.2) 로 정의한 상수 힘이라 실제 반데르발스 (F ∝ R) 의 크기 의존이 빠진 결과 ④ 강성은 '겹침이 작게' 라는 조건뿐 (6000 N/m · 근거 · 민감도 없음) · 입자 모양 불변 (말 없음) | 카드 §4-3 (i) · §3-1 · p.2 · p.9–10 | 인쇄 · 카드 추론 | 혼합 DEM 의 정의 · 척도 한계 — 압밀 · 큰 변형 상한 수치 없음

## l — 소성변형이 왜 어려운가 · 우회 · 값 · 비용
- [l] chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed (B. Chaudhuri · A. Mehrotra · F.J. Muzzio · M.S. Tomassone, *Powder Technol.* 165, 105–114, 2006) | **논의 없음** — 소성은 이력 스프링의 잔류 겹침 α0 (접촉 소산) 수준뿐 · 입자 형상 · 부피 보존 유동 없음 · 우회 = 실제 분말 (≈50 µm Avicel) 을 **2 mm 가상 구 + 무차원 점착 K** 로 키워 흉내 (우리 믹서 덱 parcel + Bo_code 와 같은 관행) · 맞춘 값 = K 하나 (영상 정성) · 비용 [미확인] ([카드 산술] 20 rpm 5 바퀴 = 6.0×10⁶ 걸음 · 입자 1.04–2.0 만 개 · 충돌당 ≈24 걸음) | 카드 §4-2 · §4-3 (ii) · §3-1 · p.2–3 | 인쇄 · 카드 산술 · 미확인 | 소성 · 큰 변형 문헌이 아니다

## m — 받아들일 통찰
- [m] chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed | **비교 기준 짝을 결과 전에 고정한다** — 원문 결론 '다른 종 점착은 늘 혼합을 돕는다' 는 비점착 (NC) 대비로만 서고, 같은 처음 상태의 K_rb = 0 짝 (그림 5B K_bb 50 · 4.5 바퀴 ln I −2.40) 과 견주면 K_rb 5 · 25 · 50 (−1.90 · −2.02 · −2.21) 이 더 나쁘고 100 (−2.38) 이 겨우 같다 · 'K_rr 중간 최적 5' 도 K_rr 0 짝과 구분 불가 [판독 · 벡터 · 카드 판정] | 흐름 밖: Ⓒ 믹서 판독 · 단계 0 (결과 전 등록) — 왜: B2-U · B2-C 의 '돕는다 / 해친다' 문장은 기준 (E0 · B1 · 상대 팔) 에 따라 뒤집힐 수 있다 (카드 §3-6 · §3-7 · §9-1)
- [m] chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed | **쌍 Bond 수 정규화 규약을 맞춘다** — 이 논문 K = 모든 쌍 ÷ 작은 입자 무게 (식 4) · Li–McCarthy = 쌍의 가벼운 쪽 · 우리 Bo_code — 우리 덱을 이 K 로 옮기면 AM_P–AM_P 19.1 이 SE–SE 21.2 와 비슷해 보이지만 자기 무게 대비는 0.011 (정규화 배수 1,750 ↔ 그들 3.4) [카드 산술] | 흐름 밖: Ⓒ 믹서 문헌 대조 · 후보 D0 — 왜: 문헌 K 와 우리 Bo 를 그대로 견주면 큰 입자 쌍의 점착을 크게 잘못 읽는다 (카드 §3-9 · §7-2)
- [m] chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed | **회전 효과는 회전당 · 시간당을 나눠 보고** — K 120 에서 30 rpm 은 12.5 rpm 보다 시간으로 2.7 배 빨리 ln I −0.5 에 닿지만 그중 2.4 배가 회전 수 · 회전당 이득은 11 % (3.83 → 3.39 바퀴) [판독 · 벡터 · 카드 산술] · 비점착 회전 무관은 인용 (Sudah [10]) 이지 시뮬레이션이 아니다 | 흐름 밖: Ⓒ 믹서 rpm 축 — 왜: 우리 rpm 사다리도 비점착 대조 팔 (E0) 을 같은 사다리로 돌려야 '점착 때문' 이 선다 (카드 §3-4 · §7-3)
- [m] chaudhuri2006_cohesive_mixing_tumbling_blender_bond_number_rotation_speed | **'세 쌍 모두 켬 + 결합 규칙' 은 비어 있는 칸** — 비균일 런마다 K_rr 이나 K_rb 가 0 · JKR · 기하평균이면 K_rb² = 0.96·K_bb·K_rr (그 크기) 라 기하평균과 맞는 런은 그림 5 (K_rb = K_rr = 0) 뿐 [카드 산술] · 벽 점착 = 같은 종 쌍과 같은 크기로 묶여 강한 점착 침대가 '고체 회전' (p.7) | 흐름 밖: Ⓒ 믹서 novelty · 판독 칸 — 왜: 우리 B 덱 (기하평균 · 세 쌍 모두 켬 · γ_W/γ_SE 0.00256) 이 그 칸이고 판독에 '벽에 붙은 SE 몫' 을 따로 둔다 (카드 §3-9 · §7-2 · §9-5 · §9-6)

## n — 논문 에이전트 후보
- [n] O.S. Sudah, D. Coffin-Beach, F.J. Muzzio, Effects of blender rotational speed and discharge on the homogeneity of cohesive and free flowing mixtures, Int. J. Pharm. 247 (2002) 57–68. (원문 참고 [10]) | m (G3 · G4) — '비점착 = 회전 무관 · 점착 = 회전 의존' 의 실험 근거 · 이 논문이 비점착 회전 런 대신 쓴 인용 (카드 §3-4 · §7-3 · §12) | litdb 확인: papers/ 620 목록 (이 카드 포함) 'sudah' ls 0 · 'Effects of blender rotational' · '247 (2002)' grep 0 · wishlist 0 → 카드 없음
- [n] T. Shinbrot, A. Alexander, F.J. Muzzio, Spontaneous chaotic granular mixing, Lett. Nat. 397 (1999) 675–678. (원문 참고 [8] · 'Lett. Nat.' = Nature) | m (G1) — 약한 점착이 혼합을 크게 빠르게 한다는 실험 (같은 크기 · ≤ 300 µm) · 이 논문 'K 0.1 이 빠름' 의 근거 (카드 §3-3 · §12) | litdb 확인: 'shinbrot' ls 0 · 'Spontaneous chaotic' · '675–678' grep 0 → 카드 없음
- [n] J.J. McCarthy, Micro-modelling of cohesive mixing processes, Powder Technol. 138 (2003) 63–67. (원문 참고 [21]) | m — 젖은 계에서 '중간 점착이 혼합을 조금 빠르게' 의 선례 (최적의 존재 · 이 논문 p.1) (카드 §12) | litdb 확인: 'mccarthy' ls 0 · 'Micro-modelling of cohesive' · '138 (2003) 63' grep 0 → 카드 없음
- [n] N. Duong, et al., Segregation in granular materials and the direct measurement of surface forces using atomic force microscopy, Powder Technol. 145 (2004) 69–72. (원문 참고 [22] · 서지 일부만 — 저자 'et al.') | m (G2) — AFM 으로 잰 표면력과 분리를 잇는 선례 후보 · 우리 '같은 SE 탐침 AFM → 결과 예측' 의 앞선 시도인지 확인 (카드 §0-2 G2 · §12) | litdb 확인: 'duong' ls 0 · 'direct measurement of surface forces' grep 0 → 카드 없음
- [n] A. Alexandar, et al., Avalanching flow of cohesive powders, Powder Technol. 164 (2006) 13–21. (원문 참고 [35] · 서지 일부만 · 원문 철자 'Alexandar') | m — 점착 분말 무너짐 · 팽창 실험 (이 논문의 영상 검증 근거 [34, 35]) · 우리 SE 분말 안식각 · 흐름 실측 설계 (카드 §3-3 · §12) | litdb 확인: 'alexander' ls 0 · 'Avalanching flow of cohesive' grep 0 → 카드 없음

## 카드 문제
- `jadidi2023_dem_batch_solid_mixers_review` **L187** — **경미 (식 귀속)**: 혼합 지수 표의 Intensity of segregation 식을 *"I_s = (σ² − σ_r²) / (σ₀² − σ_r²)"* 로 적고 사용처에 'Chaudhuri 2006' 을 넣었다 ↔ 원문 식은 **I = σ²/σ0²** (p.3 · σ_r² 항 없음 · 범위 1 → 0 은 같음) — 카드는 리뷰 표의 식을 그대로 옮긴 것으로 보인다 (리뷰 원문 대조 [미확인]) · 고치지 않음.
- `jadidi2023_dem_batch_solid_mixers_review` **L483** — **경미 (해석 칸)**: 인용 두 문장 (점착 ↑ → 무너짐 · 팽창 증가 · K 0.1 이 더 잘 섞임) 은 원문과 같다 · 그러나 '우리에게' 칸의 *"약한 점착은 bed dilation 을 통해 재배열을 돕는다"* 는 원문에 없는 기전 연결이다 (원문은 K 0.1 의 차가 *"not large"* 라고만 하고 Shinbrot [8] · Bocquet [18] 와 맞는다고 함 · 4.3 바퀴까지는 비점착이 앞섬 [판독 · 벡터]) · 고치지 않음.
- `jadidi2023_…` L55 · L139 · L381 · `jarray2019_cohesion_driven_mixing_segregation_drum` L48 · L325 — **문제 아님 (기록)**: 값 (F_cohesion/W_p 0.1) · 모델 (Walton–Braun + square-well) · 서지 · 'DEM 결과 정성 인용' 모두 원문과 같다.
- `li2003_cohesive_mixing_segregation_pairwise_bond_hierarchy` — **문제 아님 (원문 쪽 인용 단순화 · 기록)**: 이 논문이 Li & McCarthy 2003 을 *"segregation would be limited at equilibrium whenever the materials are adhesive, and more cohesion will lead to more segregation than would be achieved in the dry case"* 로 요약하며 '같은 종 쌍 Bo 가 더 클 때' 라는 조건절을 뺐다 (li2003 카드 G1 칸의 원문 인용과 대조) — 카드는 고치지 않았고 🔗 관련 카드에 이 slug 한 줄만 더했다 (li2003 · li2005 · figueroa2009 · jarray2019 각 한 줄).
- 그 밖: 정본에서 이 논문을 인용한 카드 = jadidi2023 · jarray2019 (+ li2003 §8 의 'N-150' 언급) — papers/ 620 목록 (이 카드 포함) + DOI 'powtec.2006.04.001' · 'Cohesive effects in powder mixing' · 'Chaudhuri' grep.

## 공백 검사 G1–G4 (★ 이 카드의 핵심 산출 · 카드 §0-2 와 같은 판정)
- **G1 — 점착 대비를 설계 변수로 혼합 결과 (덮임 ↔ 뭉침 · 섞임 ↔ 분리) 를 예측** → **일부** (쌍 대비를 설계 변수로 바꿔 본 DEM 은 있다 · 예측 규칙 · 문턱 · 결합 규칙 · 덮임 정량은 없다) | 근거: p.2 *"we specify independently the normal contact forces between like and unlike particles"* (식 4 · 모두 작은 입자 무게로) · p.8 *"Kbb=150 displays a different pattern, the "blue" particles stay together, leading to the formation of agglomerated "islands", thus hampering mixing"* · p.9 *"it appears that adhesion between the components always favors the mixing process; but the final mixed state of the blend relative to non-cohesive/free-flowing material depends strongly on the intrinsic cohesiveness of the components being mixed"* — 사후 관찰 · 관측량 I 하나 · ⚠ '늘 돕는다' 는 같은 K_bb 50 의 K_rb 0 짝 (4.5 바퀴 ln I −2.40) 대비로는 서지 않는다 (K_rb 5–50 이 더 나쁨 [판독 · 벡터 · 카드 판정]) | 좁힐 문장: "같은 · 다른 쌍 점착력을 따로 둔 DEM 에서 혼합 결과가 쌍 힘 대비에 달린다는 관찰 = Chaudhuri 2006 (건식 · 정사각 우물 상수 힘 · 크기비 0.667 · 5 바퀴)" 을 먼저 적고, 우리 몫 = **결합 규칙 (기하평균) 으로 묶인 세 쌍 점착 · 측정 γ 비 (같은 SE 탐침 AFM) 에서 시작한 문턱 예측 (0.31 · 0.39 = Figueroa 2009 식 32) · 덮임 정량 (AM–SE 접촉 분율 · 무작위 대비 SE 군집) · 3 상 µm · 압밀 뒤 수송** — "쌍별 점착 대비가 혼합 ↔ 뭉침을 가른다는 것을 DEM 으로 처음 보였다" 는 쓸 수 없다.
- **G2 — 점착 입력을 따로 재고 (AFM · IGC · 접촉각 등) 혼합 결과를 미리 예측** → **없음** | 근거: 각주 1 *"This is just a convenient way of defining how strong cohesion is, as compared to the particle weight (i.e. 20 times the weight, 30 times the weight, etc.)"* (p.2) · K 60 ↔ *"moderately cohesive Avicel-101"* 영상 대조 (그림 1 · 고른 절차 없음) · 정전기 미포함 (각주 2) · AFM 표면력 문헌 Duong [22] 은 서론 인용뿐 · 측정 0 · 사전 등록 없음 | 좁힐 필요 없음 (이 논문 기준) — 가까운 선례는 접촉각 입력의 Li & McCarthy 2005 (`li2005_…` G2) · 약학 쪽 AFM 점착 · 응집 비 예측은 후보 표 N-152.
- **G3 — 회전 속도 최적을 입자 수준 맞교환 (덩어리 풀림 ↔ 벽 부착 손실 등) 으로 설명** → **일부** (풀림 쪽 한 면 · 말로만 · 최적 없음) | 근거: p.8 *"At 30rpm, higher shear helps in stretching and breaking striations of similar particles, promoting faster homogenization of the mixture"* · *"Higher tumbler speeds transmit more shear to the system, breaking up the coherent particle bonds, resulting in better mixing"* · K 120 하나 · 12.5 · 20 · 30 rpm 단조 (5 바퀴 ln I −0.70 · −0.76 · −0.85 [판독 · 벡터]) · 벽 부착 · 다시 뭉침 · 끊긴 결합 수 없음 · 비점착 회전 무관은 Sudah [10] 인용 · [카드 추론] K 120 침대의 '고체 회전' (p.7) 에는 같은 종 쌍과 같은 벽 점착 (μ_w 0.7) 이 거들었을 수 있으나 원문 논의 없음 | 좁힐 문장: "점착 혼합에서 빠른 회전이 회전당 혼합을 돕는다는 DEM 관찰과 '전단이 같은 종 줄무늬 · 결합을 끊는다' 는 말 설명 = Chaudhuri 2006" → 우리 몫 = **최적이 생기는 맞교환 (덩어리 풀림 ↔ 벽 부착 · 다시 뭉침) 을 끊긴 SE–SE 결합 수 · 벽에 붙은 SE 몫으로 세어 보이기 · 여러 점착 수준 · 무차원 회전 세기 (Fr · 충돌 수 Co)**.
- **G4 — 공정 × 재료 상태도 (회전 세기 × 점착 · Bond 수 등) 가 다른 재료로 옮겨 감** → **없음** | 근거: 상태도 없음 (회전은 K 120 에서만) · p.9 *"All the values reported here are for the system as described in Table 2, and are strongly scale dependent"* · p.10 *"the optimum values of bond numbers are scale dependent"* · *"The existence of an optimal mixing state is still an open question"* · 옮기는 것은 모델뿐 *"This model could easily be used for blenders of other geometries like tote, v-blender or double cone"* (p.10) | 좁힐 필요 없음 — 오히려 '최적 Bond 수는 규모 의존' 이라는 저자 문장이 우리 G4 (회전 세기 · 충돌 수까지 넣은 무차원 지도) 의 필요를 받친다.

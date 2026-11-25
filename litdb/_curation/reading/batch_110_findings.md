# batch 110 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 표 N-71 · 대피 세션)

대상: `silbert2001_chute_flow_bagnold_spring_dashpot_hertz_dem` — L. E. Silbert · D. Ertaş · G. S. Grest · T. C. Halsey · D. Levine · S. J. Plimpton, "Granular flow down an inclined plane: Bagnold scaling and rheology", *Phys. Rev. E* **64**, 051302 (2001) · DOI 10.1103/PhysRevE.64.051302.
단분산 구 (3D) · 원판 (2D) 의 중력 경사면 정상 흐름 DEM (Model L 스프링–감쇠 · Model H Hertz + 저장 접선 변위의 Coulomb 절단) — 압밀 · 탈압 · 소성 없음 · 무재료 · 무차원.
쪽 = 논문 번호 쪽 051302-N (PDF 14 쪽) · 판독 원자료 = `litdb/figures/silbert2001_chute_flow_bagnold_spring_dashpot_hertz_dem/digitized.csv` (94 행) · 고른 의도 = 후보 D0 (접촉 법칙 원전) · 'gran/hertz/history 꼴 원전' (benhadjali2026 L445) → 의도 대조 결과 **일부** (카드 §0-1).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 무재료 단분산 구 · 중력 흐름.  가장 가까운 숫자 = 단분산 마찰 구 (μ 0.5) 의 무압력 정지 충전 0.595 (기공 40.5 % [카드 산술]) — 랩 표준 (300 MPa 순수 SE 10–13 %) 과 다른 상태 · 다른 재료 (카드 §9 표).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 하중을 빼는 계산이 없다.  접촉 법칙에서 법선 재하 / 제하 이력을 일부러 뺐으므로 (*"We ignore hysteretic effects between loading or unloading normal contacts"* p.4) 잔류 겹침 · 되돌아옴 비대칭이 원리적으로 생기지 않는다 (카드 §4-11).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 재료 항복 · 경도 · 크리프 값이 없다.  원문의 'yield' 는 (i) 접촉 마찰의 정적 항복 기준 μ (0.50 · 시험 0.15–1.0 · p.5 · p.8) 와 (ii) 연속체 Coulomb 항복과의 비교 (Mohr 원 응력 각 2φ · IYE · p.10–11) 뿐 — 일축 항복 세기 환산 없음.

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 한 종류 단분산 입자 · 혼합 · 하중 분담 없음.

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] silbert2001_chute_flow_bagnold_spring_dashpot_hertz_dem | 이 논문의 법칙 = 선형 스프링–감쇠 (f = 1) · Hertz (f = √(δ/d)) × (k_n δ n − γ_n m_eff v_n) + 저장 접선 변위 u_t 의 Coulomb 절단 ('proportional loading') · 맞춘 값 0 개 (매개변수는 '실제 입자를 닮게' 고른 값) · 깨지는 범위는 원문이 말하지 않음 (겹침 미보고) | 카드 §4-2 · p.4–5 · 식 (2)–(7) · 표 I | 인쇄 | 작은 겹침 (~10⁻⁴–10⁻³ d [카드 산술]) 의 중력 흐름에서만 쓰였다
- [e] silbert2001_… | 원문이 든 '더 실제적인' 접촉: 법선 재하/제하 이력 (Walton–Braun [22] · 원문은 뺌) · 실제 접촉의 접선 이력 (Mindlin–Deresiewicz [36] — *"proportional loading … is a simplification of the much more complicated and hysteretic behavior of real contacts"*) · 마찰 방향 기억 (Walton [23]) · *"More recent versions of these models now exist [31–33]"* (Vu-Quoc & Zhang 탄소성 · Moreau) | p.4–5 | 인쇄 | 대안을 계산해 견주지 않았다 (이름만)
- [e] silbert2001_… | 접선 꼴 대안 시험: u_t 를 자르지 않음 → 결과 비슷 · KE 차 18 % (L2) (*"we do not believe this to be a physically reasonable choice"*) · 동마찰만 (u_t = 0 · 접선 속도 감쇠만) → *"we never observed a steady state flow"* · k_t/k_n 2/3 ↔ 2/7 → KE +≈10 % · 밀도 · 응력 그대로 | p.5 · ref [34] p.13–14 | 인쇄 | 정마찰 (저장 변위) 이 정상 흐름에 필요하다는 것까지 · 압밀 범위 아님

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 — MPM 없음.

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] silbert2001_… | 같은 꼴은 옮겨진다: 일정 밀도 구간 · Bagnold 단면 · α = 1.52 ± 0.05 (2D μ 0.5 · 0.25 와 3D H3 같은 기울기) · 응력의 99 % 가 지속 접촉 · 얇은 더미 (H ≲ 20) 비-Bagnold | p.7 · p.12 · p.13 · Fig. 19 | 인쇄 | 단분산 · 중력 흐름
- [g] silbert2001_… | 옮겨지지 않는 것: 2D 단분산 원판은 멈출 때 다결정 삼각 격자로 결정화 (φ ≃ 0.9) → *"Crystallization of the 2D monodisperse pile upon the arrest of flow was primarily responsible for the large hysteresis observed in that case"* · 재시작에 훨씬 큰 각 · A_Bag 이 2D 에서 안식각에 유한 도약 (3D 는 0 으로 연속) · 흐름 정지가 3D 는 표면 (표면 층이 IYE 에 접근) · 2D 는 바닥 근처 | p.3 · p.6 · p.10–12 · Fig. 14 · 18 | 인쇄 | 원문은 '2D → 3D 전이' 를 따로 논하지 않는다 — 나란히 놓은 결과
- [g] silbert2001_… | 숫자 비교 불가 예: φ_max 2D 0.815 (면적 분율) ↔ 3D 0.590 (부피 분율) · θ_r 17.8° ↔ 19.4° · Z_c 2D 0.3–0.9 ↔ 3D 0.5–3.2 [판독] · 3D 만 σ_yy 가 15–20 % 작다 · ε 민감도 2D 만 (3D *"little effect"*) | p.8 · p.11 · Fig. 10 · 12 · 20 | 인쇄 + 판독 | 정규화 · 차원이 달라 값 전이 금지

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] silbert2001_… | 법선 이력 없음 → 탈압 잔류 겹침 · 되돌아옴을 이 꼴로는 셀 수 없다 · 우리 압축 덱 법선 법칙 (Luding 2008 계보) 의 원전으로 인용 금지 | 카드 §0-1 · §4-9 · §4-11 · §10-1 | 카드 관찰 | —
- [j] silbert2001_… | '강성을 낮춰도 밀도 둔감' 은 중력 흐름 (겹침 ~10⁻⁴ d) 영역의 결과 — 우리 압밀 (⟨δ⟩/d ≈ 0.11) 은 25–400 배 겹친 영역이라 옮길 수 없다 | 카드 §8-3 · §8-4 · §12-A | 카드 산술 (자릿수) | 겹침은 원문 미보고 · 카드 어림
- [j] silbert2001_… | 원문 내부 불일치: 식 (21) σ_xz = A_Bag² γ̇² ↔ Fig. 18 정의 A_Bag = γ̇/√σ_xz · 식 (22) (A_Bag⁻² 이어야 함) · Z_c 정규화 (삼각 격자 3 ↔ 3D '4–6') · Fig. 7b 캡션 ↔ 범례 H 값 · Fig. 19 캡션 (a)(b) ↔ 한 패널 | 카드 §12-B | 카드 산술 · 판독 | —

## k — DEM 의 한계 (원문 문장 · 인용 서지 = Silbert 외 2001, Phys. Rev. E 64, 051302)
- [k] silbert2001_… (Silbert · Ertaş · Grest · Halsey · Levine · Plimpton 2001 · Phys. Rev. E 64, 051302) | 강성은 물성이 아니라 계산 시간에 맞춘 값: *"For a realistic simulation of glass spheres with diameter d=100 μm, the appropriate elastic constant k_n^glass=O(10^10) necessitates a very small time step for accurate simulation, prohibiting any large-scale study. In our simulations, we typically use a value for k_n=O(10^5) which we believe captures the general behavior of intermediate-to-high-k systems, thus offering a reasonable representation of realistic granular materials"* — 무른 배수 ≈5 × 10⁴ [카드 산술] | p.4 · `txt_p4_units_kn_glass_softening` | 인쇄 | 중력 흐름
- [k] silbert2001_… (Silbert 외 2001) | 작은 겹침 · 시간 간격의 맞바꿈: *"The value of the spring constant should be large enough to avoid grain interpenetration, yet not so large as to require an unreasonably small simulation time step δt, since an accurate simulation typically requires δt ~ t_col/50."* · *"increasing k_n by a factor of 100 requires a reduction in the time step by a factor of 10"* | p.4 · p.8 | 인쇄 | 겹침 상한 숫자는 원문에 없다
- [k] silbert2001_… (Silbert 외 2001) | 접촉 법칙의 단순화를 스스로 적음: *"We ignore hysteretic effects between loading or unloading normal contacts and we do not differentiate between frictional directions at the same contact point at different time steps as does Walton [23]."* · *"This ‘‘proportional loading’’ approximation [35] is a simplification of the much more complicated and hysteretic behavior of real contacts [36]."* | p.4 · p.5 | 인쇄 | —
- [k] silbert2001_… (Silbert 외 2001) | 매개변수 둔감의 해석 (= 단단한 구 · 기하 지배): *"for a densely packed pile of stiff objects in motion, the overall time evolution of the system in the configurational phase space is primarily constrained and controlled by aspects of geometrical packing, rather than the specific form of the stiff force laws between particles or dissipation functions"* · *"the effect of variations in k_n is minimal, provided k_n is sufficiently large"* (Fig. 11: 10 배 무른 쪽 φ −≈0.01 · 표면 속도 +≈20 % [판독]) | p.12 · p.8 | 인쇄 + 판독 | 중력 흐름 · '충분히 큰 k_n' 의 기준 숫자 없음

## l — 소성변형이 왜 어려운가 · 우회 · 비용 (인용 서지 = Silbert 외 2001, Phys. Rev. E 64, 051302)
- [l] silbert2001_… (Silbert 외 2001) | 소성을 다루지 않는다 — 입자는 단단한 구 · 법선 이력 (잔류 겹침) 도 뺐다 · 원문의 '소성' 은 연속체 비교뿐: *"the normal stress anomalies … are quite small compared to what one would have attributed to a plastic material at incipient yield"* | p.4 · p.11 | 인쇄 | 소성이 어려운 이유의 설명은 없다
- [l] silbert2001_… (Silbert 외 2001) | 택한 우회 = 강성 낮추기 (계산 시간 · 맞춘 값 0 · 검증 = k_n 100 배 범위 · μ · ε · k_t/k_n · γ_t 민감도 시험 · 실험 대조 α 하나) · 비용 = 500-MHz DEC Alpha 에서 3D 8000 입자 10⁷ 걸음 ≈5 일 · MPI 8 프로세서 1.5 × 10⁷ 걸음/일 (병렬 효율 ≈0.94 [카드 산술]) · 정상 상태까지 1–2 × 10⁷ δt (N < 10,000) · 2–5 × 10⁸ δt (2D H 200) | p.4–5 · p.8 | 인쇄 + 카드 산술 | 소성 비용과 직접 대응되지 않음 (흐름 계산 비용)

## m — 받아들일 통찰
- [m] silbert2001_… | 무엇을: **U5 두 입자 충돌 기대값** — Model L 의 ε = exp(−γ_n t_col/2) · t_col = π(2k_n/m − γ_n²/4)^(−1/2) 가 표 I 의 ε 0.92 · 0.88 을 재현 (0.920 · 0.883 [카드 산술]) · 우리 쪽 어디에: U5 · 후보 D0 (덱 COR ↔ 강성 · 감쇠 정합 — comparison F-P5 미감사와 같은 할 일) · 왜: 닫힌 꼴이라 단일 충돌 시험의 판정선을 결과 전에 쓸 수 있다 (p.4 식 10–11)
- [m] silbert2001_… | 무엇을: **시간 간격 규칙 δt ≤ t_col/50 을 가장 단단한 가지로** — 이력 법칙이면 k̂₂ 로 t_col 를 센다 · 우리 쪽 어디에: 후보 D0 (덱 감사 한 줄) · 왜: 원문 규칙 (p.4) + `luding2008` 카드의 k̂₂ = 시간 간격 안정 상한
- [m] silbert2001_… | 무엇을: **2D 단분산 벤치마크 금지** — 단분산 원판은 정지 때 결정화해 이력 · 재시작 · 정지 위치가 3D 와 달라진다 · 우리 쪽 어디에: 단계 3 (2D 접촉 표현 비교 침대는 다분산 · 결정화 점검을 결과 전에) · 왜: p.3 · p.6 · p.10–12
- [m] silbert2001_… | 무엇을: **인용 규칙 둘** — ① 우리 압축 덱 법선 이력의 원전은 이 논문이 아니다 (Luding 2008 ← Walton–Braun 1986) — 이 논문은 접선 이력 · Coulomb 절단 · Hertz 배율의 원문 ② '강성 낮춰도 밀도 둔감' 은 '중력 흐름 · 작은 겹침' 한정어와 함께 · 우리 쪽 어디에: 후보 D0 · 보고서 방법 절 · 18 배 연화 방어 문장 · 왜: p.4 원문 진술 · 카드 §8-4 겹침 자릿수

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드 없음 · papers/ ls + grep 확인)
- [n] P. A. Cundall and O. D. L. Strack, Geotechnique 29, 47 (1979). (원문 목록 [28] 그대로 · 제목 미인쇄 — 서지 일부만) | DEM 과 접선 스프링 (tangential history) 의 원전 — e · k · 후보 D0 (원문 p.4 *"developed earlier by Cundall and Strack [28]"*) | litdb 확인: papers/ 에 cundall* 없음 · 'Geotechnique 29' grep 0 (다른 카드는 이름만 언급)
- [n] R. D. Mindlin and H. Deresiewicz, L. Appl. Mech. 20, 327 (1953). (원문 목록 [36] 그대로 — 'L.' 은 인쇄 그대로 · 서지 일부만) | 실제 접촉의 접선 이력 — 'proportional loading' 이 단순화한 대상 · e · k | litdb 확인: papers/ 에 mindlin* 없음 (다른 카드는 Hertz–Mindlin 이름만)
- [n] J. Schafer, S. Dippel, and D. E. Wolf, J. Phys. I 6, 5 (1996). (원문 목록 [38] — 제목 미인쇄) | k_t/k_n = 2/7 의 근거 · DEM 접촉력 꼴 비교 — 후보 D0 · U5 · e | litdb 확인: papers/ 에 schafer* · dippel* 없음 · 'J. Phys. I 6' grep 0
- [n] L. Vu-Quoc and X. Zhang, Mech. Mater. 31, 235 (1999). (원문 목록 [31] — ⚠ [32] (Vemuri 외) 와 권 · 쪽이 같다 · 서지 일부만) | 탄소성 접촉 법칙 — 후보 C′ · e (원문 *"More recent versions of these models now exist [31–33]"*) | litdb 확인: papers/ 에 vuquoc* · vu-quoc* 없음 (harthong2009 · lommen2014 · demirtas2021 · morrissey2013 카드는 언급만)
- [n] H. A. Makse, D. L. Johnson, and L. M. Schwartz, Phys. Rev. Lett. 84, 4160 (2000). (원문 목록 [48] — 제목 미인쇄) | 3D 정지 충전 배위수 '4–6' 의 근거 — d · k (원문 p.12) · Z 정규화 확인 | litdb 확인: papers/ 에 makse* 없음 (cantor2020 · shi2019 카드는 다른 Makse 논문 · 언급)
- (참고 · 후보 아님) O. R. Walton and R. L. Braun, J. Rheol. 30, 949 (1986) [22] — 우리 hooke/hysteresis 계보의 원판이지만 **후보 표 제외 (N-72 첫째 · 1저자 내려받기 불가)** · 공개 대체판 = `luding2008_cohesive_frictional_contact_models`.

## 카드 문제
- 없음 (고칠 줄 없음).  확인한 2 차 인용 넷:
  - `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` L445 서지 = 원문과 같다 · L222 의 F^{GH} = √δ·√(R_iR_j/(R_i+R_j))·[…] 는 원문 식 (6)·(7) 과 같은 꼴 (같은 크기 구에서 상수배 K_n = 2k_n/d [카드 산술]) — 다분산 R_eff 배율은 원문에 없지만 그 카드는 benhadjali 논문의 식을 옮겼다 (귀속은 그 논문 몫).
  - `shi2019_high_am_loading_particle_size_assb` L169–173: [22] 서지 · 귀속은 원문과 같다 · 그 카드가 옮긴 SI 식은 원문과 세 곳 다르다 (감쇠에 m_eff 없음 · 접선 스프링이 저장 변위 u_t 가 아닌 'δ t_ij' · 접선 스프링 부호 +) — 카드가 *"인쇄 그대로"* 라 적었으므로 그 논문 SI 의 표기.
  - `haervig2017_jkr_adhesion_rolling_reduced_stiffness_dem` L141 · L298 *"Δt_col/δt ≈ 50"* = 원문 p.4 *"δt ~ t_col/50"* · ⚠ 확인 필요 한 건: L298 서지 *"Phys. Rev. (2001) 051302"* 에 'E 64' 가 없다 — 그 카드는 haervig 원문 목록을 옮긴 것이라 적혀 있고 이 정독은 haervig PDF 를 대조하지 않았다 (카드 문제로 단정하지 않음).
  - `clemmer2024_bpm_elastic_grain_compaction_beyond_jamming` L135 *"Silbert · Santos 의 φ_c(μ)"* = 그 논문 refs 5 · 24 (Santos 외) 로 이 논문이 아니다 · `brodu2015_multiple_contact_dem_dense_granular` L476 = Silbert 2002 (PRE 65, 031304) — 이 논문 아님 (혼동 없음).

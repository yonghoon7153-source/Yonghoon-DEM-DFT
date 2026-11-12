# batch 85 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `stewart2001_dem_pept_bladed_mixer_detailed_comparison` — R. L. Stewart, J. Bridgwater, Y. C. Zhou, A. B. Yu, "Simulated and measured flow of granules in a bladed mixer—a detailed comparison", *Chem. Eng. Sci.* 56 (2001) 5457–5471 (DOI 인쇄 없음 · PII S0009-2509(01)00190-7) (후보 표 N-45 · 가리킨 카드 = `chandratilleke2012_particle_scale_mixing_index` L61 · L49 · L305 · 11-12 대피 세션이 본 세션에서 넘겨받은 1 순위 후보).
지름 249 mm 2 날개 수직 믹서의 유리구 유동을 PEPT 로 재고 같은 계 DEM (16,000 구 · E 2.16 × 10⁶ N/m² 고정) 의 마찰 다섯 경우를 셀마다 견준 논문 — 압밀 · 탈압 · 소성 · 수송 없음.
쪽 = 인쇄 p.5457–5471 (PDF 쪽 N = 인쇄 5456 + N) · SI 없음 · 판독 없음 (정량 값 = 표 2 [인쇄]).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (유리구 · 중력 유동 · 압밀 · 기공 · 진밀도 0 — 카드 §7-2).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 (하중 · 탈압 단계가 없다 — 카드 §4-3 · §4-4 (iv)).

## c — 항복 · 경도 · 크리프 값과 정의
- [c] stewart2001_dem_pept_bladed_mixer_detailed_comparison | 항복 · 경도 · 크리프 **없음** — 탄성 · 마찰 상수만: E 2.16 × 10⁶ N/m² (연화 · 출처 = Zhou 1999 더미 쌓기 계산) · ν 0.3 · ρ 2500 kg/m³ · c 0.3 · μ_s 0.2–0.5 · μ_r 0–0.05 mm (기호표는 '무차원') · 구름 저항 = *"elastic hysteresis loss and time-dependent deformation (Tabor, 1955)"* | 카드 §3-2 · p.5459–5460 · 표 1 | [인쇄] | 유리구 · 일축 항복 세기 환산 없음 · 실제 유리 E 없음

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (한 재료 · 하중 분담 · 재밍 · 힘 분석 없음 — 힘은 *"cannot be measured experimentally"* 라는 DEM 장점 언급뿐 p.5469).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] stewart2001_dem_pept_bladed_mixer_detailed_comparison | 쓴 법칙 = Hertz 꼴 법선 (f_cn = −√2E/(3(1 − ν²)√|R_p|) δ_n^{3/2} R_p) + Mindlin–Deresiewicz 꼴 접선 (δ_s,max 정의 없음) + 점성 감쇠 + 방향 일정 구름 토크 τ_r = −μ_r|f_cn|ω̂_p · 깨지는 범위 · 대안 (multi-contact · MDR · EEPA · Thornton–Ning · Storåkers) **언급 없음** · 이 계의 겹침 = 0.2–0.9 % d (무게 1–10 배 · [카드 산술 — δ = (F/K)^{2/3} · K = 55,947 N m^−3/2]) = 작은 겹침 영역 · 맞춘 값 0 (마찰 두 개의 민감도 다섯 경우) | 카드 §3-2 · §3-6 · p.5459 · 식 크롭 `eq_f_cn_*` … `eq_tau_r_*` | [인쇄] · [카드 산술] | 큰 변형 · 압밀과 무관 (저속 유동)

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 아님).  DEM ↔ 측정 쪽 오차 추정 꼴만 있다: 셀 (15 mm) 평균 속도 정확도 ±15 % (PEPT) · ±7 % (DEM) · 셀당 값 ≥ 5 · PEPT 크기의 무작위 오차를 모의 위치에 더하면 분산 지수 +5 % 이하 (p.5461 · p.5466 · 카드 §3-4) — 격자 · 시간 간격 수렴 시험은 없다.

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] stewart2001_dem_pept_bladed_mixer_detailed_comparison | 실험 쪽 경고 한 문단: 투명 벽 너머 혼합 실험은 *"unable to capture the full three-dimensional motion of particles that occurs in process equipment, and most have focused on two-dimensional flows. Furthermore, the effect of the wall on particle motion raises questions about the reliability of quantitative flow data from these experiments."* (p.5457) · 이 논문은 PEPT · DEM 모두 3D (그림 = 3D 장의 2D 단면 셋) | 카드 §4-4 (iii) · `txt_p1_intro_transparent_wall_2d_flows_unreliable.png` | [인쇄] | 계산의 2D → 3D 정량 대조 없음 · 측정 (벽 관찰) 의 한계 문장

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 (DEM ↔ 측정 비교만 · 연속체 넘김 없음).

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] stewart2001_dem_pept_bladed_mixer_detailed_comparison | 가압 · 탈압과 직접 닿는 한계 없음 · 가까운 것: 저자 *"DEM is based on simple models about inter-particle interactions which may not fully represent the physics, and some of required parameters are not readily available … although focused on friction coefficients only, the results … highlight the effects of material properties and hence the need for their proper selection"* (p.5469) · 카드: E · 감쇠 · 속도 민감도 · 반복 · δ_s,max 식 · 계산 비용 [미확인] | 카드 §4-4 (i) · §11 · [미확인] 목록 | [인쇄] · [미확인] | 유동 계 · 영률은 고정값이라 '물성 선택' 의 근거는 마찰 쪽뿐

## k — DEM 의 한계
- [k] stewart2001_dem_pept_bladed_mixer_detailed_comparison — Stewart, Bridgwater, Zhou & Yu 2001 (Chem. Eng. Sci. 56, 5457–5471) | 단순 모델 · 매개변수 · 모양 · 비용: *"DEM is based on simple models about inter-particle interactions which may not fully represent the physics, and some of required parameters are not readily available."* · *"While PEPT can be readily employed with particles of any shape this is difficult or more often impossible when using DEM, which is limited currently by computing power."* · *"none was able to accurately predict the velocity of every part of the bed"* (p.5469) | 카드 §4-4 (i) · `txt_p13_dem_simple_models_parameters_shape_single_criterion.png` · `txt_p13_conclusions_friction_geometry_best_cases.png` | [인쇄] | 저속 유동 · 유리구 — 압밀 · 큰 겹침에 관한 한계는 아님
- [k] stewart2001_dem_pept_bladed_mixer_detailed_comparison — Stewart, Bridgwater, Zhou & Yu 2001 (Chem. Eng. Sci. 56, 5457–5471) | 비용 · 검증 필요: *"As even a small granular system can contain millions of particles it can take an impracticably long time to solve real problems. Furthermore, without accurate flow data from real systems it is impossible to validate these models"* (p.5458) · 16,000 구 25 s 도 *"demanding computationally"* (p.5460) | 카드 §4-4 (i) · `txt_p1_p2_methods_review_dem_cost_validation.png` · `txt_p3_p5_dem_tracks_to_pept_format_25s_resampling.png` | [인쇄] | 2001 년 계산 기준 · 하드웨어 · 시간 [미확인]
- [k] stewart2001_dem_pept_bladed_mixer_detailed_comparison — Stewart, Bridgwater, Zhou & Yu 2001 (Chem. Eng. Sci. 56, 5457–5471) | 경계 접촉 가정: 날 근처 큰 차를 *"the simplifying assumption that the particle–blade friction coefficient is the same as the particle–particle friction coefficient"* 탓으로 · 날 옆 셀을 빼면 r² 0.57–0.91 → 0.80–0.95 (p.5464 · 표 2) | 카드 §3-5 · `txt_p7_p8_velocity_r2_blade_friction_assumption_case_a_third.png` | [인쇄] | 가정을 바꾼 계산은 없다 (크기 미상)
- [k] stewart2001_dem_pept_bladed_mixer_detailed_comparison — Stewart, Bridgwater, Zhou & Yu 2001 (Chem. Eng. Sci. 56, 5457–5471) | ★ **보정값이 물성이 아니라는 말은 없다 — 대신 말 없이 고정**: E = 2.16 × 10⁶ N/m² 를 *"Table 1 lists the parameters used in the present simulation, which have been used to simulate the piling process of glass beads (Zhou et al., 1999)"* 로만 둔다 (실제 유리 E · 낮춘 이유 · E 민감도 0) · 같은 그룹 2010 의 *"reduced from 10⁹ of real glass beads to 2.16 × 10⁶ to reduce computational time"* 는 그 논문 문장 [다른 카드 `chandratilleke2010_…`] | 카드 §0-1 · §3-2 · §7-3 · `txt_p3_dem_model_parameters_zhou1999_setup_five_cases.png` | [인쇄] · [다른 카드] | '말 없음' 의 확인 — 연화의 검증 근거로 이 논문을 인용하지 않는다

## l — 소성변형이 왜 어려운가
- [l] stewart2001_dem_pept_bladed_mixer_detailed_comparison — Stewart, Bridgwater, Zhou & Yu 2001 (Chem. Eng. Sci. 56, 5457–5471) | **소성 논의 없음** (유리구 · 무게 하중 · 겹침 0.2–0.9 % d [카드 산술]) · 우회 = **연화 E 하나 (2.16 × 10⁶ N/m²) — 이유 · 맞춘 대상 없음 · 출처 = Zhou 1999 더미 쌓기** · 맞춘 값 0 · 이 논문이 바꾼 것 = μ_s · μ_r (다섯 경우) · 검증 = 1 rad/s 한 속도 · 셀 속도장 r² (날 영역 뺌) 0.80–0.95 · 기준 충족 셀 25–61 % · 비용 = 16,000 구 · dt 5 × 10⁻⁵ s · 25 s (500,000 걸음 [카드 산술]) · *"demanding computationally"* · [카드 산술] 이 dt 는 연화 E 에서 충돌 시간의 1/30 (0.1 m/s) · E = 10⁹ 이면 1/2.6 | 카드 §0 · §3-6 · §4-4 (ii) · §7-3 | [인쇄] · [카드 산술] | 연화의 목적 (시간 간격 · 계산 시간 — 2010 의 말) 이 우리 압밀 DEM 의 연화 (소성 · 재배열 대리 · 기공 보정) 와 다르다 — 배수 전이 금지

## m — 받아들일 통찰
- [m] stewart2001_dem_pept_bladed_mixer_detailed_comparison | 무엇: **계산을 측정과 같은 연산자로 바꿔 비교** — DEM 이 속도를 직접 알아도 PEPT 와 같은 사슬 (0.05 s 재표본 · 6 점 속도 · 15 mm 셀 · 값 ≥ 5) 로 만든 값만 썼다 · 어디에: 단계 0 · 결과 전 대조 항목 (기공 · 두께 · 피복을 CT · SEM 과 견줄 때 해상도 · 문턱 · 단면 규칙을 계산 쪽에도) · 왜: *"only the velocities calculated using the method above have been used"* (p.5461 · 카드 §3-4)
- [m] stewart2001_dem_pept_bladed_mixer_detailed_comparison | 무엇: **영역별 다지표 + 통계 검정이 아닌 오차 기준** — r² · 기울기 · Δv 세 꼴 (셀 속력 · 속력 중앙값 · 표준오차로 나눔) · 셀 기준 0.2 · 0.2 · 2.5 · 계산과 실험은 다른 모집단이라 통계 검정은 자료 양만 가린다 · 히스토그램은 B–D 를 낫게 보였지만 E 가 더 가까웠다 · 어디에: 단계 0 · R5 (맞춘 지표 하나 + 점검 지표 여럿 · 영역별 보고) · 왜: p.5466 · p.5468 · *"a single global criterion could prove to be dangerously misleading"* (p.5469 · 카드 §3-4 · §3-5)
- [m] stewart2001_dem_pept_bladed_mixer_detailed_comparison | 무엇: **'검증된 연화' 는 무엇을 바꿨는지까지 따라간다** — 2010 · 2012 가 연화 E 의 근거로 드는 이 논문은 E 를 고정하고 마찰만 바꿨다 · 뒤 논문의 마찰 한 벌 = case D (기준 충족 셀 49 % · 다섯 가운데 넷째) · 어디에: 후보 D0 (frame [2] 연화 서술의 인용 근거) · 흐름 밖: 믹서 Ⓒ (시간 간격용 연화 E 는 E 를 바꾼 팔로 검증) · 왜: p.5459 · 표 1 · 표 2 · 카드 §0-1 · §7-3
- [m] stewart2001_dem_pept_bladed_mixer_detailed_comparison | 무엇: **경계 마찰을 입자끼리 값과 따로 둔다** — 큰 차가 날 근처에 몰렸고 저자는 '입자–날 = 입자–입자 마찰' 가정을 원인으로 든다 · 어디에: 후보 A′-0 (판 · 벽 · 다이 접촉 규칙) · R2 · 왜: p.5464 · 카드 §3-5

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
litdb 확인 = 정본 `litdb/papers/` 파일 목록 (`ls` · `git ls-tree`) + `git grep` (제1 저자 성 · 제목 낱말 · 권쪽) — 아래 셋 모두 자기 카드 없음 · `_curation/wishlist.md` 에도 없음.
- [n] Stewart, R. L., & Bridgwater, J. (2001). Granular flow over a flat-bladed stirrer, Chemical Engineering Science, in press. (원문 참고문헌 · 인쇄 그대로 · 권 · 쪽 없음 = 서지 일부만) | m · k — 이 논문의 속도 보정 근거 (*"the velocity field scales linearly with blade speed"* p.5461) · 2 mm 구 더미 소용돌이 · 100 s 재순환 (p.5462 · 5463) — 날 속도 축의 실측 · 카드 §2 계보 · §12 | litdb 확인: 'flat-bladed' · 'Granular flow over' grep 0 · ls stewart* = 이 카드뿐 → 카드 없음
- [n] Cundall, P. A., & Stack, O. D. L. (1979). A discrete numerical model for granular assemblies. Géotechnique, 29, 47–65. (원문 참고문헌 · 인쇄 그대로 — 'Stack' 은 원문 표기 · 정본 `chandratilleke2010_…` 은 'Strack') | k — DEM 원전 (단단한 구 · 연성 접촉 · 겹침 가정의 출발점 · 그 원전이 적은 한계) · 카드 §3-2 · §12 | litdb 확인: ls cundall* 없음 · 'Geotechnique, 29' · 'discrete numerical model for granular' grep = 인용 카드뿐 → 카드 없음
- [n] Tabor, D. (1955). Mechanics of rolling friction II. Proceedings of the Royal Society A, 229, 198–220. (원문 참고문헌 · 인쇄 그대로) | e · c — 구름 저항 = 탄성 이력 손실 (τ_r 의 물리 근거 · 우리 `cdt` 구름 토크 꼴의 정당화 원전) · 카드 §3-2 · §12 | litdb 확인: ls tabor* 없음 · 'Mechanics of rolling friction' grep 0 → 카드 없음
- (참고 · 후보로 세지 않음 · 이미 `wishlist.md` 에 있음) Zhou, Y. C., Wright, B. D., Yang, R. Y., Xu, B. H., & Yu, A. B. (1999). Rolling friction in the dynamic simulation of sandpile formation. Physica A, 269, p 536. (L208 · ★ 이 논문 표 1 매개변수 — E 2.16 × 10⁶ N/m² 포함 — 의 출처: 그 값을 무엇에 맞췄는지가 의도 (k · l) 의 남은 빈칸) · Zhou, Yu, Stewart, Bridgwater 2004 Chem. Eng. Sci. 59, 1343–1364 (L260 · 이 원문 뒤 논문 · 2010 카드 ref 9) · Parker 1993 (PEPT 방법) · Jones & Bridgwater 1997 · Laurent 2000 · McCarthy 1996 · Novosad 1964 · 1968 — 카드 없음 · a–m 몫이 작다.

## 카드 문제
- 가리킨 카드 `chandratilleke2012_particle_scale_mixing_index` **L32 · L305** (경미 · 표현): *"PEPT 비교로 정당화 (선행 연구 ref 12 · 17)"* · *"같은 믹서 DEM ↔ PEPT 대조 (연화 정당화의 근거)"* — 원문 (ref 12 = 이 논문) 은 **E 를 다섯 경우 모두 2.16 × 10⁶ N/m² 로 고정하고 마찰만 바꿨으며** 실제 유리 E · 연화 · 그 이유를 한 번도 말하지 않는다 (매개변수 출처 = Zhou 1999 더미 쌓기) → '연화 정당화의 근거' 가 아니라 'E 고정 유동 검증 (마찰 민감도)' 이 원문에 맞다.  2012 원문이 ref 12 · 17 을 어떤 문장으로 붙였는지는 2012 PDF 가 없어 대조 못 함 [미확인].
- 같은 카드 **L305 '같은 믹서'** ↔ 같은 카드 **L58 '(Stewart 2001 실험 믹서와 유사)'**: 원문 실험 믹서 = 날 102 mm · 축–날 6.5 mm · 벽 · 바닥 틈 0 / 2012 모의 = 날 106 mm · 벽 틈 2.5 mm · 바닥 틈 7.5 또는 0 mm (그 카드 L58) → '유사' 가 맞다 (카드 안의 어긋남).
- 같은 카드 **L61 '(시간 간격 때문)'**: 이 원문에는 없는 이유 · 2012 원문 문장 [미확인] · 같은 그룹 2010 원문은 *"to reduce computational time"* [다른 카드 크롭] · 참고: 이 원문 dt = 5 × 10⁻⁵ s ↔ 2012 dt = 2–5 × 10⁻⁶ s (같은 E) — 고치지 않음.
- 같은 카드 **L274** *"E ÷ 463 + 선행 PEPT 대조로 '유동은 맞다'"* (한정어 빠짐): 큰 특징은 다섯 경우 모두 맞다 (원문 결론) · 2012 가 쓴 마찰 한 벌 (L60 μ_s 0.3 · μ_r 5 × 10⁻⁵ m) = 원문 case D — 기준 충족 셀 49 % · *"only met the criteria near the blades and in the slow moving parts of the heaps"* (p.5468–5469).
- 참고 (카드 문제 아님): `chandratilleke2010_blade_speed_flow_mixing_cylindrical_mixer` L409 의 서지 (제목에 부제 '—a detailed comparison' 없음 · '56 (19)') 는 2010 논문 목록 표기로 보인다 — 이 PDF 첫 쪽에는 호 (19) 가 없다.  그 카드가 옮긴 2010 원문 *"validated against the PEPT measurements as detailed by Stewart et al."* 는 이 원문의 검증 범위 (1 rad/s · dt 50 µs) 를 넘어 2–100 rpm · dt 5 µs 에 쓰였다 [카드 관찰].
- 참고: 2012 · 2010 · chibwe2020 카드의 이 논문 줄 '카드 없음' 은 이 카드로 낡았다 (고치지 않음).

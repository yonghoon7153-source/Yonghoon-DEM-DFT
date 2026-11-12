# batch 52 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `dang2019_nmc111_secondary_particle_flat_punch_fracture_strength` — Dingying Dang, Yikai Wang, Yang-Tse Cheng, "Communication—Fracture Behavior of Single LiNi0.33Mn0.33Co0.33O2 Particles Studied by Flat Punch Indentation", J. Electrochem. Soc. 166 (13) A2749–A2751 (2019), DOI 10.1149/2.0331913jes (본문 3 쪽 + SI 3 쪽).
NMC111 (Umicore) 다결정 2차입자 하나씩을 다이아몬드 평판 (명목 Ø40 µm) 으로 아르곤 글러브박스 안에서 눌러 (하중 제어 1 mN/s) 변위가 튀는 하중 F_c 를 재고, S_t ≈ 2.8F_c/(πd²) (Hiramatsu–Oka) 로 강도를 낸 실험 Communication — pristine · 전해액 48 h 침지 · 첫 탈리튬화 · 첫 리튬화 네 상태 129 입자의 원 자료 (SI 표 S2) 와 Weibull (표 S1) 을 준다.  후보 표 N-10 (조건 R7) · Wheatcroft 2023 이 2차 인용한 "NMC111 평판 188 MPa" 의 1 차 자료.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (SE 를 다루지 않는다 — 재료는 NMC111 활물질만).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
- [b] dang2019_nmc111_secondary_particle_flat_punch_fracture_strength | 되돌아옴 **없음**.  하중 제어의 *"loading/unloading rate of 1 mN s⁻¹"* 만 있고, 제하는 **입자가 부서진 뒤의 조각 덩어리** 에서만 했다 (Fig. 2a · S3 — 거의 수직 제하, 분석 없음) · 파괴 전 제하 · 반복 하중 없음 | 카드 §4-6 (iv) · §3-2 · p. A2749 · Fig. 2a | [인쇄] · [판독] | 조건 R4 의 값이 아니다

## c — 항복 · 경도 · 크리프 값과 정의
- [c] dang2019_nmc111_secondary_particle_flat_punch_fracture_strength | 항복 · 경도 · 영률 · 크리프 **없음** (본문 + SI: modulus · hardness · yield · elastic · plastic 0 회).  준 것은 **파괴 강도** 하나: S_t ≈ 2.8F_c/(πd²) (식 [1], Hiramatsu & Oka 1966 — 두 점 압축된 불규칙 취성 조각의 인장 강도 근사 · 계수 2.8/π ≈ 0.891 [카드 산술]) · pristine Weibull S_m **188 MPa** (S₀ 205 · m 4.8 · n 33) | 카드 §0 · §3-1 · §4-4 · 식 [1] p. A2750 · SI 표 S1 · S2 | [인쇄] · [SI] · [카드 산술] | NMC111 · 명목 강도 (진응력 아님) · 일축 항복 환산 없음
- [c] dang2019_nmc111_secondary_particle_flat_punch_fracture_strength | **규약 표** — 같은 입자 · 같은 하중이 2.8F/(πd²) = 188 · F/d² = 210.9 · F/(πd²/4) = 268.6 MPa (최대 43 % 차) [카드 산술].  정본 카드의 R7 강도가 세 규약에 흩어져 있다: 이 카드 · `stallard2022_…` (2.8/π) / `wheatcroft2023_…` · `song2025_insitu_ct_dem_…` (계수 1) / `meyer2018_calendering_process_model_…` (투영 면적) | 카드 §3-4 | [카드 산술] | 규약을 맞추지 않고 문헌 강도를 나란히 놓지 않는다
- [c] dang2019_nmc111_secondary_particle_flat_punch_fracture_strength | (참고 · 인용 금지) Fig. 2a 부하 곡선 (d 16.2 µm · 10–70 mN) 의 겉보기 Hertz (두 강체 평판 사이 구) E\* ≈ 97.5 GPa → E ≈ 91 GPa (ν 0.25) · 파괴 순간 δ/d ≈ 0.046 · 20→60 mN 기울기 ≈134 mN/µm | 카드 §3-2 · §13 D8–D9 | [판독] · [카드 산술] | 프레임 순응 · 비구형 · 한 입자 — 원문은 E 를 내지 않았다

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
- [d] dang2019_nmc111_secondary_particle_flat_punch_fracture_strength | 하중 몫 값 **없음** (입자 하나 시험).  카드가 낸 연결 하나: AM 입자 하나가 버티는 하중의 상한 — d 10–12 µm pristine 중앙 F_c ≈21–30 mN (Weibull 중앙 S 189.9 MPa 를 식 [1] 로 되돌림) · 5 % 분위 ≈12 mN (d 10 µm) → AM 골격의 하중 분담이 입자 분할로 끊길 수 있는 크기 (조건 R1 · R7) | 카드 §3-3c · §8 (R1–R7 행) · §13 D14 | [카드 산술] · [카드 해석] | 두 점 하중 · 고립 입자 · NMC111

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 (계산 · 접촉 법칙 없음).  카드 §8 후보 C′ 행: AM 에는 "항복 캡" 보다 **파쇄 문턱** 이 맞다는 정성 (취성 · 입계 분할) 뿐.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 (MPM 없음).  카드 §8 후보 A 행 (제안): 강체 AM MPM 에서 R7 을 사후 판정 — AM 마다 받은 맞은편 접촉 반력을 F_c(d) = S·πd²/2.8 (d 10 µm: pristine 중앙 21 mN · 5 % 12 mN) 과 비교 [카드 산술].

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] dang2019_nmc111_secondary_particle_flat_punch_fracture_strength | 실험은 3D 입자지만 **d = 누르기 전 현미경 2D 투영 면적에서 계산한 지름 (ImageJ)** — 구가 아니면 d 오차가 S_t 에 제곱으로 들어간다 · 식 [1] 은 *"without knowing the precise shape of the brittle blocks"* 라고 정당화 (p. A2750) · 2D ↔ 3D 전이에 대한 말 없음 | 카드 §4-3 · §4-6 (iii) · p. A2749–A2750 | [인쇄] | 우리 DEM 의 d = 구 지름 (정의가 다르다)

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 (압밀 · 기공 없음 · 전극은 액체계 무압연 92 : 4 : 4 wt% · 7.3 mg cm⁻²).

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] dang2019_nmc111_secondary_particle_flat_punch_fracture_strength | 고립 입자 · 두 점 하중만 — 다접촉 · 전극 속 · 캘린더링된 입자 · 압밀 중 파괴는 없다 · 파괴 전 제하 없음 · E · K_IC · 경도 없음 · 순환 값은 액체 전해질 + NMP 80 °C 추출 이력 (충 / 방전 입자의 추출 영향 대조 없음) · 온도 · 1차입자 크기 · 분말 PSD · 입자 선정 기준 · 장비 보정 미기재 | 카드 §11 · §14 | [미확인] | —
- [j] dang2019_nmc111_secondary_particle_flat_punch_fracture_strength | 저자 결론 *"the fracture strength of NMC secondary particles at all states is, statistically, independent of the particle size"* (p. A2750) 은 Fig. 3b 의 d 를 표 S2 원 자료 126/129 개에 짝지어 재분석하면 **pristine 에서만** 선다: ln S ~ ln d 기울기 pristine −0.16 [−0.40, +0.09] (p 0.20) · 침지 −0.29 [−0.50, −0.09] (p 0.007) · 첫 리튬화 −0.62 [−0.81, −0.42] (p < 0.001) · 첫 탈리튬화 −0.30 (p 0.078; Spearman 0.023) | 카드 §3-3a · §13 D10–D12 | [판독 d] · [SI] · [카드 산술] | 순위 짝짓기 (가린 3 점 제외) — 판독 d 오차 ±0.03 µm 수준
- [j] dang2019_nmc111_secondary_particle_flat_punch_fracture_strength | SI 는 Weibull 모수를 *"P_f(S_i) = i/N"* 로 추정했다고 쓰지만 표 S1 (m 4.8 · S₀ 205 …) 은 **최대가능도 (MLE)** 값과 반올림까지 같다 (i/N 회귀면 pristine m 5.56) — 추정법 서술과 값이 다르다 | 카드 §3-3b · §13 D2–D3 | [카드 산술] | 결과 전 등록 때 Weibull 추정법을 적는다

## k — DEM 의 한계
- [k] dang2019_nmc111_secondary_particle_flat_punch_fracture_strength (Dang · Wang · Cheng 2019, J. Electrochem. Soc. 166 (13) A2749–A2751) | **말 없음** — DEM · 입자 계산을 쓰지도 언급하지도 않는다 (simulat · discrete element · finite element · numerical 0 회 · DEM 캘린더링 논문 [2,3] 은 "캘린더링이 입자를 깰 수 있다" 의 근거로만 인용).  DEM 한계의 근거 문헌으로 인용할 수 없다.  쓸 수 있는 것은 계산 쪽에 대한 **요청** 한 문장: *"We expected that the measured fracture strength of the NMC particles can be incorporated in computational models of electrodes made of NMC particles under battery operating conditions."* (p. A2751) | 카드 §4-6 (i) · `txt_p2751_other_factors_strength_for_computational_models.png` | [인쇄] | 실험 Communication

## l — 소성변형이 왜 어려운가
- [l] dang2019_nmc111_secondary_particle_flat_punch_fracture_strength (Dang · Wang · Cheng 2019, J. Electrochem. Soc. 166 (13) A2749–A2751) | **말 없음** (계산 없음 · 맞춘 값 0 개 · 비용 해당 없음).  입자를 **취성** 으로 본다: *"Both the secondary and primary particles are brittle and, therefore, vulnerable to fracture."* (p. A2749) · *"Because of the brittle nature of the NMC particles, the fracture of the NMC secondary particles should be similar to the uniaxial compression induced fracture of rock and alumina particles."* (p. A2749) — plastic · yield 0 회 · 파괴 전 부하 곡선의 곡률은 분석하지 않았다.  우리 쪽 의미 = AM 은 소성 캡이 아니라 **분할 문턱** 으로 다루는 것이 맞는 부류 (조건 R7 · R6 은 SE 몫) | 카드 §4-6 (ii) · `txt_p2749_intro_…` · `txt_p2749_2750_hiramatsu_oka_…` | [인쇄] | NMC111 · 실험

## m — 받아들일 통찰
- [m] dang2019_nmc111_secondary_particle_flat_punch_fracture_strength | **R7 평판 끝의 독립 앵커 + 산포** — pristine NMC111 Weibull S₀ 205 · m 4.8 (n 33 · 원 자료 공개) 을 F/D² 로 맞추면 평균 211 MPa = Wheatcroft NMC811 평판 207 (n 15) 과 2 % 안 → 강도 기준 팔 (wheatcroft 카드 §8 ①) 의 평판 끝을 이 분포로 · 확률적 문턱이면 m ≈5 | 후보 D0 · 조건 R7 · 단계 5 | 카드 §7-2 · §9-1 · SI 표 S1–S2 | 재료 NMC111 · 두 점 하중 · 등록 뒤에만 (결과 보고 고르면 순환)
- [m] dang2019_nmc111_secondary_particle_flat_punch_fracture_strength | **규약 열 강제** — 문헌 입자 강도는 2.8F/(πd²) · F/d² · F/(πd²/4) 세 규약이 섞여 있고 같은 입자가 188 · 211 · 269 MPa 로 적힌다 → R7 판정 기준을 결과 전에 적을 때 규약 열 · d 정의 (2D 투영 ↔ 구 지름) · Weibull 추정법 (MLE ↔ i/N 회귀: m 4.8 ↔ 5.6) 을 같이 적는다 | 단계 0 · 결과 전 대조 항목 | 카드 §3-4 · §3-3b | 함정의 크기 = 최대 43 % (규약) · 16 % (m 추정법)
- [m] dang2019_nmc111_secondary_particle_flat_punch_fracture_strength | **Auerbach 크기 스케일 점검** — 평판 pristine 강도는 입경과 무관 (원 자료 기울기 −0.16 n.s. · Wheatcroft 평판 −0.49 n.s.) 인데 Auerbach (P_c ∝ R) 는 F/D² ∝ D^−1 → 넓은 AM 입도 (bimodal · 큰 AM_P) 로 갈 때 두 기준의 판정이 갈린다 (지금 R_min 5/6 µm 폭에서는 ≤ 20 %) | 후보 D0 · 조건 R7 | 카드 §7-1 · §9-4 · §13 D12 | 순환 입자는 크기 의존이 생긴다 (첫 리튬화 −0.62)
- [m] dang2019_nmc111_secondary_particle_flat_punch_fracture_strength | **사후 SEM 대조의 함정** — 같은 전극을 코인셀로 조립 · 분해하면 일부 2차입자가 깨지고 전극이 변형된다 (Swagelok 은 그대로 · SI §6 · Fig. S5) → 실험 압밀체의 AM 파괴 분율과 우리 R7 결과를 견줄 때 시료 회수 경로 (분해 · 절단 · 연마) 를 같이 적는다 | 흐름 밖: 실험과의 대조 (조건 R7 검증) | 카드 §4-2 · §9-5 · `txt_S2_S3_swagelok_vs_coin_cell_…` | 액체 LIB 셀 · 정성 (화살표)

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
- [n] M. Yoshida, H. Ogiso, S. Nakano, and J. Akedo, Review of Scientific Instruments, 76(9), 093905 (2005) (원문 참고 [18] · SI 참고 1 · 인쇄 그대로) | c · m — 서브마이크로 취성 입자의 단일 입자 압축 장치 + Weibull 정리 (이 논문 식 [1] 적용 · Weibull 방법의 출처) · `paulick2015_particle_contact_stiffness_two_particle_method` [35] · `stallard2022_…` [111] 도 인용 | papers/ 파일 목록 + "093905" · "Yoshida" grep — 카드 없음 (paulick2015 · stallard2022 · matsusaka2010 은 인용만)
- [n] E. J. Cheng, K. Hong, N. J. Taylor, H. Choe, J. Wolfenstine, and J. Sakamoto, Journal of the European Ceramic Society, 37(9), 3213 (2017) (원문 참고 [14] · 인쇄 그대로 · 제목은 이 논문 목록에 없음) | c — NMC111 (열간 가압) 의 E · 경도 · 파괴 인성 — `sharma2023_…` · `sakka2022_…` · `stallard2022_…` [76] · `so2022_…` 가 가리키는 NMC111 기계 물성의 1 차 자료 | papers/ 목록 + "3213" · "Wolfenstine" grep — 카드 없음 (인용만) · 후보 표 · wishlist 에 없음
- [n] Y. Wang and Y.-T. Cheng, Scripta Materialia, 130, 191 (2017) (원문 참고 [15] · 인쇄 그대로) | c · m — 글러브박스 평판 압입 방법 (장치 · 보정 — 이 논문이 프레임 순응 · 열 표류 보정을 적지 않아 방법 원전에서 확인) | papers/ 목록 + "Scripta" grep — 카드 없음
- [n] Y. Wang, Q. Zhang, D. Li, J. Hu, J. Xu, D. Dang, X. Xiao, and Y. T. Cheng, Advanced Energy Materials, 8(10), 1702578 (2018) (원문 참고 [16] · 인쇄 그대로) | c · m — 액체 전해질 속 · 순환 중 압입 (이 논문 결론이 후속으로 가리킴: *"in the liquid electrolyte and during electrochemical cycling"*) | papers/ 목록 + "1702578" grep — 카드 없음
- (참고 · 후보로 세지 않음) 원문 참고 [17] Hiramatsu & Oka 1966 (식 [1] 의 원전) = **후보 표 N-11 에 이미 있다** · [2] · [3] Sangrós Giménez 2019 = 정본 카드 있음 (`sangros2019_…` · `sangros2020_lib_electrode_…`) · [8] · [13] = 정본 카드 있음 (`xu2017_…` · `devasconcelos2016_…`).

## 카드 문제
- `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem` L34 · L91 — *"NMC111 평판 평균 188 MPa [21] (p. 4) — 2차 인용 · 원문 미확인"*: 값 · 재료 · 기하는 원문 (SI 표 S1 · Fig. 3c) 과 **같다**.  다만 그 188 은 **2.8F_c/(πd²) 규약의 Weibull 평균** 이라 같은 카드의 207 (계수 1) 과 규약이 다르다 (같은 규약으로 210.9 ↔ 207) → 카드 오류 아님 · "미확인" 이 풀리는 **갱신 거리** (고치지 않음).
- 같은 카드 L535 (D24) — *"(Dang NMC333 비교 188 은 규약 미확인)"*: 이제 규약 = Hiramatsu–Oka 2.8/π (식 [1]) 로 확인됨 → 갱신 거리.
- `stallard2022_cathode_mechanical_properties_review` L115 · L158 (+ 그 값을 쓰는 L27 · L181 · L375 · L526) — NMC333 pristine **중앙 185.6** (리뷰 Fig. 10C vector-read): 원 자료 (SI 표 S2 · n 33) 의 중앙은 **182.6** (17 번째) · 수염 128.3 / 289.2 와 상자 156.3 / 216.0 (중앙 뺀 반쪽 중앙) 은 원 자료와 같다.  185.6 = (182.6 + 188.5)/2 = 17 · 18 번째 값의 평균 → 리뷰 그림 쪽 차이로 보인다 (리뷰 원 그림으로만 판정 · 3.0 MPa · 1.6 %).  L181 의 *"건조 pristine 분모면 0.379"* 는 원 자료 중앙으로 0.385.
- 같은 카드 L176 — 13A 세 상자 (침지 · 첫 탈리튬화+재리튬화 · 첫 탈리튬화) 의 15 값은 원 자료와 **같다** (±0.05) · 상태 표지 x ≈ 0.92 · 0.33 은 Dang 원문에 없다 (리뷰의 덧붙임 — 용량 곡선 Fig. 1c 만 있음) — 기록만.
- 같은 카드 L115 — *"NMC333, 결정립 0.5–1 µm"*: Dang 원문은 *"submicron primary particles"* 뿐 (숫자 없음) → 리뷰의 귀속 (Dang 원문으로 확인 불가 · 기록만).
- 같은 카드 L89 — 침지 조건 *"1 M LiPF₆/EC 48 h"*: 원문 전해액은 **1 M LiPF₆ in EC : EMC = 3 : 7 (v/v) + VC 2 wt%** — "EC" 만은 줄임 (리뷰 문장인지 카드 요약인지는 리뷰 원문으로만 · 기록만).
- `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` L142 · L268 · L327 · L386 — *"188 MPa (평균 파괴 인장강도) · NMC111 · flat punch"* = 원문과 같다 · 규약 (2.8/π) 표기만 없다 (오류 아님).
- **낡은 "카드 없음" 표기**: 후보 표 N-10 행과 가리킨 카드 셋 (wheatcroft · stallard · sedlatschek) 이 이 논문을 "인용만 · 카드 없음" 으로 적는다 — 이 카드가 생겨 낡음 (고치지 않음).
- 후보 표 (`litdb/_curation/S8_candidates.md`) N-10 행 — 서지 (저자 · 제목 · J. Electrochem. Soc. 166 · A2749–A2751 · 2019 · DOI) 는 원문과 같다 (원문에는 호 13 · 이름 전체가 더 있다).

# batch 62 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `ai2011_rolling_resistance_contact_models_dem` — Jun Ai, Jian-Fei Chen, J. Michael Rotter, Jin Y. Ooi, "Assessment of rolling resistance models in discrete element simulations", *Powder Technology* **206** (2011) 269–282 · DOI 10.1016/j.powtec.2010.09.030 (호 번호는 원문 PDF 에 인쇄 안 됨).
DEM 구름저항 모델을 네 부류 (A 방향 일정 토크 · B 점성 · C 탄소성 스프링–대시포트 · D 접촉 무관 = 평형 위반으로 제외) 로 나누고, 되굴림 가지 · 감쇠 스위치 f 를 넣은 일반 Model C 를 제안해 2D PFC2D 기준 시험 셋 (평면 굴림 · 10° 경사 · 원판 25 개 정착) 과 2D 광탄성 원판 모래더미 (Zuriguel 2007 실험 · 안식각 27°) 로 견준 리뷰 겸 모델 논문.  재료 = 고무 같은 원판 · 2D · 중력만 · 압밀 · 기공 · 탈압 0 → 값 전이 0 건 · 문장 · 시험 꼴 · 규칙만.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (기공 · 밀도 · 압력 계열 0 — 'porosity' · 'compaction' 0 회 · 카드 §7-3).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 압력을 다루지 않는다.  곁 정보: '되돌림' 은 **회전 방향** 에만 있다 — Model C 의 되굴림 가지 (Fig 4 · *"when the contact rolling torque should reduce back to zero, the rolling angle is required to reduce by the angle θ_r^m"* p.274) · 10° 경사에서 *"rolls back very slightly before becoming stationary"* (p.277 · μ_r 0.2 에서 꼭지 ≈0.102 → 0.096 m ≈ 6 mm [판독 · Fig 12a]) — 압력 탈압 · 스프링백과 다른 양 (카드 §4-2 (iv)).

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 재료 항복 · 경도 · 크리프 값 0.  곁 정보: Model C 의 토크 상한 M_r^m = μ_r R_r F_n (식 13) 과 *"similar to the loading-unloading stress-strain curve of an elastic perfectly plastic material (Fig. 4)"* (p.274) 의 '탄–완전소성' 은 **회전 방향 토크–각 관계의 비유** 이지 재료 항복이 아니다 (카드 §3-4 · §8 후보 C · C′ 줄).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (한 종류 원판 · 이원 크기 모래더미 · 하중 몫 0).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 직접 해당 없음 — 구름 토크 모델은 법선 점접촉의 큰 변형 대안이 아니라 **회전 자유도에 보태는 항** 이다 (법선 · 접선 = PFC2D 내장 Hertz–Mindlin · p.275).
- [e] ai2011_rolling_resistance_contact_models_dem | 곁 정보 — 구름 모델별 매개변수 수: A = μ_r 하나 (식 8a) · B = μ_r 하나 (식 9 · 속도에 곱함) · C = μ_r · k_r (J_n 또는 θ_r^m · 식 7c · 15 · 16) · η_r (식 18) · f (식 17 스위치) · MDEM (Iwashita & Oda) = *"four artificial parameters, with three of them chosen separately by trial and error and the fourth related to particle overlap"* (Jiang [20] 의 비판을 옮김 · p.271) · 맞춘 값 0 (시험 = 표 1 · 모래더미 = *"were chosen"* p.280) | 카드 §3-2 · §3-4 · §8 후보 C · C′ · p.271 · 273–275 · 280 | [인쇄] | 2D · 회전 자유도 · 법선 소성 (Thornton–Ning · EEPA · MDR) 과 다른 축 — '맞춘 값 수' 비교에 섞지 않는다

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 (MPM · 연속체 0 — 2D 원판 DEM).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] ai2011_rolling_resistance_contact_models_dem | 식 (2–20) · 시험 전부 2D 원판 · 3D 에 대한 말 = *"For simplicity, all formulations and examples are presented in 2D form, though the general conclusions are also applicable to 3D systems"* (초록 · 서론 두 번) — 근거 · 3D 시험 없음 · *"As only 2D circular disks and clumps of them are considered here"* (p.272) · 일반 모양 2D · 3D 운동학은 Kuhn & Bagi [73–77] 로 넘김 · 3D 에만 있는 비틀림 (twisting · spin · torsion) 0 회 | 카드 §0 ⑤ · §4-2 (iii) · p.269 · 272 | [인쇄] · [카드 관찰] (낱말 셈) | 주장 한 문장 — 3D 전이의 증거로 쓰지 않는다 · 3D 구름 토크는 축 둘 (구름 · 비틀림) 이라 2D 식을 그대로 못 옮김 [카드 추론 · 원문 말 없음]

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 (DEM 만 · FE · MPM 넘김 0).

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] ai2011_rolling_resistance_contact_models_dem | 저자 한계: 매개변수 선택이 *"often empirical and consequently very problem dependent"* (p.271) · J_n 의 이론 범위 0.25–0.5 를 일부러 무시 (모양 · 점착을 담으려고 · p.273) · f = 0 고정 (모델을 가르려는 선택 · p.274) · 모래더미는 겉모양 · 안식각만 (응력 · 접촉력 · 충전 구조 = Ai 박사논문 [84] · p.279) · 구름 기전 규명은 범위 밖 (p.271) · 공기 저항 등 제외 (p.270) | 카드 §0 ⑨ · §11 | [인쇄] | 가압 · 탈압과 닿는 것: A 부류의 정지 토크 진동 (주기 2Δt) 이 잔류 KE · 기어내림을 남기고 *"reduced, but not eliminated, by adopting smaller time steps"* (p.280) → 우리 cdt 덱의 정착 · 판 고정 이완 · 언로딩 판정이 Δt 에 걸릴 수 있다 [카드 추론 · 크기 미측정]
- [j] ai2011_rolling_resistance_contact_models_dem | 카드가 찾은 원문 어긋남: 표 1 E 40 MPa 로는 Δt 5 × 10⁻⁵ s = Δt_crit 의 **34 %** (원문 *"about 10%"*) · E 4 MPa 이면 10.9 % · 모래더미 (E 4 MPa · r_min 3.45 mm · ν 0.49 가정) 6.3 % (원문 *"about 6%"*) — 표 1 의 '40' 이 '4' 의 오식일 가능성 [추정] · 식 (9) 는 무차원 μ_r 이면 토크 차원이 아님 (N·m²/s) | 카드 §3-10 | [카드 산술] · [추정] | 원문 오류인지 [미확인] — 이 논문의 Δt 비율을 그대로 옮기지 않는다

## k — DEM 의 한계
인용 서지: **Ai, Chen, Rotter, Ooi (2011), Powder Technology 206, 269–282 (2D PFC2D · 원판).**
- [k] ai2011_rolling_resistance_contact_models_dem (Ai · Chen · Rotter · Ooi · 2011 · Powder Technol. 206, 269–282) | 입자 표현: *"In a DEM model, a granular medium is usually treated as an assembly of 2D disks or 3D spheres [3,4], or else as clumps of these shapes made by rigidly connecting and overlapping multiple disks or spheres [5–7]."* | p.269 (서론 첫 쪽 왼 단) · 카드 §4-2 (i) · 글 크롭 없음 (20 장 한도 · 텍스트 층으로 대조) | [인쇄] | 일반 진술 (한계 단정은 아님)
- [k] ai2011_… (Ai et al. 2011 · Powder Technol. 206) | ★ 모양 대리: *"In modelling a pseudo-static system, rolling resistance is often introduced to represent the effects on rolling of particle shape (non-sphericity in 3D or non-circularity in 2D) and inter-particle bonds."* | p.270 · 크롭 `txt_p1_p2_pseudostatic_*` | [인쇄] | 2D 논문 · 대리의 정량 근거 없음
- [k] ai2011_… (Ai et al. 2011 · Powder Technol. 206) | ★ 이상화한 원 · 구: *"This lack of circularity is present in all real particles, but it can also arise from large deformations of spheres or disks. … It is of special importance in DEM modelling, when idealized circular or spherical particles are used."* | p.270 §2 e) · 크롭 `txt_p2_source_e_*` | [인쇄] | '모양이 하중에서 안 변한다' 는 직접 문장은 없다 — 큰 변형이 비원형을 만든다는 진술까지
- [k] ai2011_… (Ai et al. 2011 · Powder Technol. 206) | 보통 DEM 은 구름 저항이 0: *"… in conventional DEM analyses, rolling takes place without any resistance at the contacts."* (Iwashita & Oda [11] 의 인식을 옮김) · Sakaguchi [18]: 원판 아치가 보통 DEM 에서 *"not stable and could easily be broken"* · 시험 3 = 구름저항 없으면 *"almost all the disks have rolled away"* (더미 없음) | p.270 · 278 · 크롭 `txt_p2_iwashita_oda_*` | [인쇄] | 원판 · 중력 쌓기
- [k] ai2011_… (Ai et al. 2011 · Powder Technol. 206) | 임의 처리 · 경험 매개변수: *"In early studies using conventional DEM, special treatments or assumptions are required in a simulation to form a stable heap of particles with a finite angle of repose [17]. … Such arbitrary treatments can only have a weak basis, and may significantly distort the outcome, resulting in predictions of uncertain accuracy [17]."* · *"the selection of parameters in some models is often empirical and consequently very problem dependent"* | p.271 · 크롭 `txt_p3_early_dem_*` · `txt_p3_mdem_*` | [인쇄] | —
- [k] ai2011_… (Ai et al. 2011 · Powder Technol. 206) | 보정값 ≠ 물성 (고백에 가까운 것): J_n 의 이론 범위 0.25–0.5 를 무시해 *"permitting consideration of rolling resistance arising from other sources such as out-of-roundness and adhesion"* — 한 매개변수가 근원 여럿을 담는다 · 모래더미 θ_r^m 0.05 ⇒ J_n 3.0 [카드 산술] (이론 범위 밖) | p.273 · 280 · 크롭 `txt_p5_kr_units_*` | [인쇄] · [카드 산술] | —
- [k] ai2011_… (Ai et al. 2011 · Powder Technol. 206) | 모델 쪽 한계 (A 부류 = 우리 cdt 꼴 [카드 대조]): *"Model A has an inherent shortcoming of producing a final oscillating torque on each particle with a period of twice the time step adopted in the simulation. This oscillating torque produces residual kinetic energy and destabilises the system leading to an unintended creeping collapse response. Both effects can be reduced, but not eliminated, by adopting smaller time steps."* | p.280 · 크롭 `txt_p12_conclusions_*` | [인쇄] | 2D 시험 · 한 실험
- [k] ai2011_… | 겹침 · 상대밀도 · 변형률의 믿을 수 있는 상한 · 접촉 독립 가정 · 조밀 영역의 과강성 = **말 없음** | 카드 §4-2 (i) | [카드 관찰] | —

## l — 소성변형이 왜 어려운가
- [l] ai2011_rolling_resistance_contact_models_dem (Ai · Chen · Rotter · Ooi · 2011 · Powder Technol. 206, 269–282) | 원인 진술: *"Plastic deformation is a major source of energy dissipation during particle rolling contact, and is thus an important cause of rolling friction. Here the energy is not usually dissipated at the interface, but within the solid at the location of the maximum shear stress caused by the contact."* + 큰 변형은 비원형을 만든다 (p.270) — 강체 원판 · 구는 둘 다 기하로 못 낸다 [카드 추론] | p.270 §2 b) · e) · 크롭 `txt_p2_source_b_*` | [인쇄] · [카드 추론] | 소성 계산 자체는 없음
- [l] ai2011_… (Ai et al. 2011 · Powder Technol. 206) | 우회 = 접촉마다 **회전 토크 한 쌍**: A · B = μ_r 하나 · C = 회전 스프링 k_r + 상한 μ_r R_r F_n + 감쇠 η_r (+ f) · 맞춘 값 0 (고른 값) · 검증 = 2D 시험 셋 (기대 거동 · 해석해 없음) + 2D 실험 하나 (안식각 27° · 겉모양) · 비용 = 원판 1 · 25 · 3000 개 · 모래더미 50 s ÷ 2 × 10⁻⁵ s = 2.5 × 10⁶ 걸음 [카드 산술] · 계산 시간 [미확인] | 카드 §4-1 · §4-2 (ii) · p.274–275 · 280 | [인쇄] · [카드 산술] | 'elastic-plastic' 은 회전 방향 이름 — 입자 형상 소성 (우리 MPM · R6) · 법선 접촉 소성 (C′) 의 근거로 쓰지 않는다

## m — 받아들일 통찰
- [m] ai2011_rolling_resistance_contact_models_dem | **U2 단위 시험 꼴 (구름 정지)** — 10° 경사에 원판을 올려 보내 정지하는지: 정지 조건 μ_r ≥ tan α (= 식 1 의 β ≥ α) · 정지 토크 m g R sin α (원판 4.71 × 10⁻⁶ N·m [카드 산술] ↔ −4.7 [판독 Fig 12b]) · A 는 평균 각속도 ≈0.05 rad/s 로 기어내림 (p.276) · B 는 되굴러 내려옴 (p.277) → 우리 LIGGGHTS 단일 구로 `rolling_friction cdt` ↔ `epsd2` 를 결과 전 등록 뒤 잰다 | U2 · 후보 D0 | 카드 §3-7 · §9-1 · p.276–277 | [인쇄] · [카드 산술] | 2D 원판 → 3D 구는 관성 · 회전 반지름 규약을 다시 셈
- [m] ai2011_… | **시간 간격 수렴 칸** — A 부류는 잔류 KE 가 Δt 에 걸린다 (25 원판 ~10³ → ~10 정규화 단위 · Δt 5 → 1 × 10⁻⁵ s · p.278 · C 는 차이 *"well within numerical rounding errors"* p.279) → 압축 정착 · 판 고정 이완 · 언로딩 판정과 이완 KE 문턱에 '같은 런 Δt × ½' 한 번을 결과 전에 등록 | 단계 0; 단계 6; 후보 D0 | 카드 §3-8 · §9-2 | [인쇄] | 조밀 300 MPa 침대에서의 크기 미측정
- [m] ai2011_… | **μ_r 옮김 규칙** — 같은 이름 '구름 마찰 계수' 가 μ_r = tan β (무차원 · 이 논문) ↔ 편심 e (길이 · 관례 [71,72]) 로 단위가 다르고 회전 반지름도 R_r = r_i r_j/(r_i + r_j) ↔ Jiang 2 r_i r_j/(r_i + r_j) 로 두 배 다르다 → μ_r 숫자는 정의 · 반지름 규약 · 코드 (cdt ↔ epsd) 를 같이 적을 때만 옮긴다 | 후보 D0; 흐름 밖: 믹서 덱 보정값 (μ_r 0.075 · hare2026 세트) 대조 | 카드 §3-3 · §9-3 · p.272 | [인쇄] | 우리 덱 μ_r 값은 정본 카드 표기 (리포 미대조)
- [m] ai2011_… | **함정 — 이름** — *"elastic-plastic spring-dashpot"* 은 회전 방향 토크–각 고리 (Fig 4) 의 이름이다 → 후보 C′ (Thornton–Ning 류 법선 소성) · 조건 R6 (SE 형상 변형) 의 근거로 세지 않는다 · 또 A 부류는 동적 흐름 (*"rotating drum"*) 의 소산에는 쓸 만하나 준정적 계에서 *"non-stop oscillating torque"* (p.279) → 믹서 덱의 cdt 는 '쓸 만한 자리', 압축 덱의 cdt 는 '주의 자리' 로 나눠 적는다 | 후보 C′; R6; 흐름 밖: 믹서 덱 | 카드 §8 · §9-5 · p.274 · 279 | [인쇄] · [카드 추론] | —

## n — 논문 에이전트 후보
- [n] Y.C. Zhou, B.D. Wright, R.Y. Yang, B.H. Xu, A.B. Yu, Rolling friction in the dynamic simulation of sandpile formation, Physica A 269 (1999) 536–553. | k — **A 부류 (방향 일정 토크 = 우리 cdt 꼴) 와 B (각속도 비례) 의 원전** · 구름 마찰 없이는 유한 안식각 더미를 못 세운다는 근거 (카드 §3-2 · §0-1 '원전' 줄 · §12 [17]) | litdb 확인: papers/ ls `zhou1999*` 없음 · git grep "Physica A 269" · 제목 낱말 0 건 → 카드 없음
- [n] K. Iwashita, M. Oda, Rolling resistance at contacts in simulation of shear band development by DEM, J. Eng. Mech. Asce 124 (1998) 285–292. | k — MDEM 원전 · *"in conventional DEM analyses, rolling takes place without any resistance at the contacts"* 의 출처 · 회전 스프링 + 대시포트 + 비인장 결합 + 슬라이더 (카드 §3-2 · §12 [11]) | litdb 확인: `iwashita*` 없음 · grep "Iwashita" · 제목 낱말 0 건 → 카드 없음
- [n] M.J. Jiang, H.S. Yu, D. Harris, A novel discrete model for granular material incorporating rolling resistance, Comput. Geotech. 32 (2005) 340–357. | k · e — 접촉 폭을 나타내는 '모양 매개변수' · k_r = 3k_nμ_r²R_r² (식 7b) · MDEM 매개변수 넷 (셋은 시행착오) 비판 (카드 §3-2 · §3-3 · §12 [20]) | litdb 확인: `jiang2005*` 없음 (`jiang2022_*` 는 다른 DFT 논문) · 제목 낱말 0 건 → 카드 없음
- [n] M. Oda, K. Iwashita, Study on couple stress and shear band development in granular media based on numerical simulation analyses, Int. J. Eng. Sci. 38 (2000) 1713–1740. | k — 회전 저항 = 입상체 강도를 정하는 주된 성분의 하나이며 *입자 모양* 에서도 온다 (카드 §3-2 · §12 [48]) | litdb 확인: `oda*` 없음 · 제목 낱말 0 건 → 카드 없음
- [n] I. Zuriguel, T. Mullin, J.M. Rotter, Effect of particle shape on the stress dip under a sandpile, Phys. Rev. Lett. 98 (2007) 028001. | k · m — 이 논문 모래더미 실험 (2D 광탄성 원판 · 안식각 27°) 의 원전 · 입자 모양 효과 (카드 §3-9 · §12 [83]) | litdb 확인: `zuriguel*` 없음 · grep "Zuriguel" · 제목 낱말 0 건 → 카드 없음

## 카드 문제
- `chibwe2020_nnsi_segregation_index` L273–274 (가리킨 카드): *"비구형성 대리로 CDT(constant directional torque) 모델 [43, Ai 2011] T_r,ij = (ω_rel/|ω_rel|)·μ_r·r*·|F^N_ij|, μ_r = 0.5"* ↔ 원문 — (1) 이름: 원문은 *"directional constant torque models"* · 'CDT' · 'constant directional torque' 낱말 0 회 (2) 부호: 원문 식 (8a) M_r = **−**(ω_rel/|ω_rel|) μ_r R_r F_n (회전 반대) · 카드 식에 − 없음 (chibwe2020 원문 표기인지 카드 옮김인지 [미확인]) (3) 귀속: 이 꼴의 원전 = Zhou et al. 1999 [17] (*"The model proposed in Zhou et al. [17] is typical"* p.273) · Ai 2011 = 분류 · 평가 · 일반 C 의 원전.  고치지 않음.
- `chibwe2020_nnsi_segregation_index` L790 (가리킨 카드): *"구로 비구형성을 흉내 내는 표준 수법"* — 방향은 원문 p.270 과 같으나 원문은 A 부류를 준정적 계에서 *"should be used with care"* (p.279) 로 적는다 ('표준 수법' 은 카드의 말).  고치지 않음.
- `jadidi2023_dem_batch_solid_mixers_review` L99 (가리킨 카드): *"세 모델 — Model A 일정토크 / Model B 점성 / Model C 탄소성 spring-dashpot. [원저 Ai 2011] 'Model C 가 가장 적합'"* — 원문은 **네 부류** (D = 접촉 무관 · 평형 위반으로 처음부터 제외) · 시험한 대표가 셋 · '가장 적합' 은 이 논문의 2D 시험 · 한 실험 범위 (*"appears to work well in all the critical aspects examined in this paper"* p.280) — 뜻은 같고 범위 한정어가 빠짐.  L544 는 같음.  고치지 않음.
- `jadidi2023_dem_batch_solid_mixers_review` L101 ↔ 다른 정본 카드: *"우리 덱은 rolling resistance 를 이 축에서 논의한 적이 없다 … 비구형 대리(rolling friction) 라는 이 분야의 표준 우회로를 쓰지 않는다"* ↔ `luding2008_cohesive_frictional_contact_models` L185 (`fix m5 coefficientRollingFriction` AM 0.2 / 0.1 · SE–SE 0.1 = *"우리 real_14/thin9 값"*) · `shenouda2020_dem_metal_powder_am_liggghts_tutorial` L233 (`thin9:61` `… rolling_friction cdt`) · `otani2025_dem_se_dispersion_aggregation_compression` L367 · `nase2001_granular_bond_collision_number_wet_cohesion` L158 · `roessler2019_dem_cohesive_aor_cylinder_lift_calibration` L191 (믹서 덱 `rolling_friction cdt` · μ_r 0.075) — 정본 카드끼리 어긋남 (리포 덱 대조 전 · 이 배치는 리포를 열지 않았다).  고치지 않음.
- (참고 · 가리킨 카드 아님) `morrissey2013_eepa_elastoplastic_adhesion_dem_iron_ore_fines_thesis` L264 *"EDEM 기본 = Ai et al. 2011 의 Model A"* — 'EDEM 기본' 이라는 말은 이 논문에 없다 (EDEM v.2.1 [19] 은 'rolling friction' 용어 쓰임의 예 *"[e.g., 17–19]"* 로만 · p.269) · L456 서지 *"Powder Technology, 206(3)"* — 호 번호 원문 미인쇄 · 같은 줄 '정본 카드' 칸 "없음" 은 이 카드가 생겨 이제 낡음.
- (참고 · 카드 아님) 후보 표 `litdb/_curation/S8_candidates.md` N-19 처리 기록의 *"Powder Technology 206 (3) (2011)"* — 원문 PDF 에 호 번호가 없다 (출판 기록에서 온 값) · 나머지 서지 (저자 · 제목 · 권 · 쪽 · 연도 · DOI) 는 원문과 같음 · PDF 메타데이터 Subject 는 *"206 (2010) 269-282"* (인쇄 머리 = 2011).
- (참고 · 카드 아님) `litdb/figures/_sources.json` 의 choi2018 줄: 이 배치의 `extract_figures.py` 가 `figures` 를 8 → 32 로 바꿨으나 지시대로 HEAD 값 (8) 으로 되돌렸다 (다른 카드의 줄 · batch_58 과 같은 현상).
- (참고 · 원문 자체 · 카드 §3-10) 표 1 E 40 MPa ↔ *"about 10% of the critical time step"* (식 21–22 로 34 %) · 식 (9) 의 μ_r 차원 — 원문의 문제이지 정본 카드의 문제가 아니다.

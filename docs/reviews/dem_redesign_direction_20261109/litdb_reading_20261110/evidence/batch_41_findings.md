# 배치 41 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-11)

읽은 카드 = 1/1: `bardenhagen2005_mpm_foam_densification_simulation` (590 줄 · 논문 에이전트가 원문 PDF 21 쪽을 읽고 만든 카드 · 그림 11 + 식 그림 6 장을 전부 열어 봄 · 판독 원자료 = 정본 litdb/figures/bardenhagen2005_mpm_foam_densification_simulation/digitized.csv 2,173 행).  형식 = `- [글자] slug | 내용 (값 · 단위) | 위치 | 표지 | 한계`.
서지 (k · l 인용용) = Bardenhagen S.G., Brydon A.D., Guilkey J.E., *Insight into the physics of foam densification via numerical simulation*, Journal of the Mechanics and Physics of Solids 53 (2005) 597–617, DOI 10.1016/j.jmps.2004.09.003.  쪽 = 논문 쪽 (PDF 쪽 + 596).
카드의 성격: **발포체 단위 셀** (탄성 neo-Hookean 뼈대 한 물체 · 상대밀도 7.9 · 9.6 % · 3D) 을 입자 기법 (GIMP · MPM 계열) 으로 공칭 변형률 90 % 까지 누른 시연 논문.  **분말 · 입자 층 · 소성 · 마찰 · 하중 제거 · DEM 이 없다** → a · b · c · d · e · h · i 는 없음.  쓸 것은 f (MPM 수치 장치) · g · j · l · m 이다.  표지는 카드에 적힌 그대로 (`인쇄` · `[판독]` = 그림의 벡터 경로 좌표 (Fig. 2 · 7 은 화소) 에서 읽은 값 · `[카드 산술]` · `[카드 판독]` · `[카드 추론]` · `[우리 코드 판독]` · `[우리 기록]` · `[미확인]`).

---

## a — 순수 SE 압력별 기공 곡선

이 배치에 없음 (황화물 · 분말이 논문에 없음).  관련만 (재료가 다르다):
- [a] bardenhagen2005_mpm_foam_densification_simulation | 발포체의 기공 대 공칭 변형률 곡선 (압력 축이 아니라 변형률 축): lattice 0.9218 → 0.3452 · random 0.9029 → 0.3844 (ε 0 → 0.9) · 그때의 반력 3,896 · 6,673 MPa | 카드 §3-6 · §3-5 · 논문 Fig. 8 · Fig. 3 · p.610–611 | [판독] | 탄성 발포체 뼈대 — LPSCl 아님 · 진밀도 · 질량 기준 개념 없음 · 전부 누른 채의 계산값

## b — 탈압 때 되돌아오는 양 · 잰 방법

이 배치에 없음 — 하중 제거를 다루지 않는다 ('unload' · 'recover' · 'rebound' 0 회 · 카드 §0-2 (iv) · [카드 전문 검색]).

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

이 배치에 없음 (탄성만 · 항복 없음).  관련만:
- [c] bardenhagen2005_mpm_foam_densification_simulation | 뼈대 재료 = 압축성 neo-Hookean 탄성 · K 10.2 GPa · G 7.2 GPa · ρ 1900 kg/m³ → E 17.49 GPa · ν 0.214 · 종파속 3,228 m/s; Gibson–Ashby 의 '항복' 응력은 소성 항복이 아니라 발포체가 고원으로 넘어가는 (탄성 붕괴) 응력 — 그림의 선 5.53 · 8.13 MPa | 카드 §3-1 · §3-5 · 논문 p.602 · p.607–608 · Fig. 6 | K · G · ρ = 인쇄 (출처 미인쇄) · E · ν · 파속 = [카드 산술] · 선의 값 = [판독] | 발포체 뼈대 값 — LPSCl · NCM 값으로 쓰지 않는다 · 경도 · 크리프 없음

## d — 단단한 입자의 하중 몫 · 재밍

이 배치에 없음 (입자 혼합이 없음).  관련만:
- [d] bardenhagen2005_mpm_foam_densification_simulation | 뼈대가 서로 걸려 (pinned) 기공이 갇힌다 (*"the microstructure becomes pinned near full densification and porosity is "locked in""*) — ε 0.88 → 0.90 에서 random 기공 0.4036 → 0.3844 (느려짐) | 카드 §3-6 · 논문 p.610 · Fig. 8 | 문장 = 인쇄 · 값 = [판독] | 입자 재밍이 아니라 접힌 탄성 뼈대의 걸림 · 붙는 접촉

## e — 점접촉 법칙이 깨지는 범위 · 대안 · 맞춘 값 수

이 배치에 없음 (접촉 법칙 · DEM 이 논문에 없음).  'Hertzian contact mechanics' 는 "거시 응답이 뼈대 계수에 비례한다" 는 문장의 근거로 한 번 나올 뿐이다 (p.612 · 카드 §3-7).

## f — MPM 접촉 · 다물체 · 강체 결합 · 해상도 규칙 · 수치 오차

- [f] bardenhagen2005_mpm_foam_densification_simulation | **접촉 = no-slip** (*"elastic material models and no-slip contact are used in these simulations"*) · 알고리즘 이름 · 접촉 거리 · 분리 판정 미기재 · 한 물체 (뼈대) 의 자기 접촉이라 격자 한 벌의 속도장이 주는 붙는 접촉으로 읽힘 · 마찰 미끄럼은 *"will be studied later"* · 같은 제1 저자의 다물체 마찰 접촉 (2000 · 2001) 은 인용만 | 카드 머리 ③ · §4-3 · 논문 p.600–601 | 인용문 = 인쇄 · "한 속도장" 은 [카드 판독] | 다물체 · 마찰 · 강체 결합의 방법을 주지 않음
- [f] bardenhagen2005_mpm_foam_densification_simulation | 기법 = GIMP (MPM 을 특수한 경우로 포함) · *"the contiguous particle GIMP method used here"* · 명시적 적분 · 격자는 매 걸음 처음 배치로 되돌림 (*"eliminating mesh tangling problems"*) · 형상 이산화 = 규칙 격자의 후보점 가운데 물체 안의 점에 물질점 (*"similar to using pixels to represent an image"*) | 카드 §4-1 · 논문 p.600–603 | 인쇄 | 보간 함수 · 갱신식은 논문에 없음 (Bardenhagen and Kober 2004 로 넘김)
- [f] bardenhagen2005_mpm_foam_densification_simulation | 해상도: 꽉 찬 블록 1 mm³ 에 셀 0.01 mm (한 변 100 셀) · 발포체도 "같은 이산화" · **단위 셀 변 길이 · 셀당 물질점 수 · 물질점 수 미인쇄** · strut 지름 ÷ 셀 변 ≈ 0.10–0.14 (셀 변이 1 mm 라면 지름당 10–14 셀) · **격자 수렴 시험 없음** | 카드 §3-2 · §3-10 · 논문 p.603 · p.605 · Fig. 2 | 셀 크기 = 인쇄 · 지름비 = [판독] · 괄호는 [카드 산술 · 가정] | 지름당 셀 수 같은 해상도 규칙을 주지 않음
- [f] bardenhagen2005_mpm_foam_densification_simulation | 수치 오차 추정 = 꽉 찬 블록의 일축 변형 압축 ↔ 해석해 한 건: 끝 (ε 0.9) 오차 *"approximately 5%"* — 수치 286,061 ↔ 해석 271,063 MPa (+5.5 %) · 구간 평균 (수치 ÷ 해석 − 1) +6.6 % (ε 0.1–0.3) · +6.0 % (0.3–0.5) · +5.7 % (0.5–0.7) · +5.8 % (0.7–0.8) · +5.5 % (0.8–0.9) · 큰 변형률의 튐 = 물질점이 셀 경계를 넘을 때의 오차 · ε 0.9 에서 응력 5 % = 판 위치 0.32 셀 | 카드 §3-3 · 논문 p.603 · Fig. 1 | "5 %" · 튐의 원인 = 인쇄 · 값 · 구간 평균 = [판독] · 0.32 셀 = [카드 산술] | 접촉 없는 균질 블록뿐 — 발포체 계산의 오차 추정은 없음 · 구간 평균이 한쪽으로 치우친 원인 미기재
- [f] bardenhagen2005_mpm_foam_densification_simulation | **준정적 설정**: 판 속도 = 종파속의 3 % (96.8 m/s) · 90 % 압축에 파 통과 시간의 30 배 · 인공 점성 (계수 미인쇄) · 절반 속도 런 1 건과 *"similar"* → 빠른 속도 채택.  구간 평균 반력의 비 (빠름 ÷ 느림) 1.02 (ε 0.05–0.3) · 1.35 (0.3–0.55) · 1.09 (0.55–0.7) · ε 0.7 에서 361 ↔ 289 MPa · 구조의 겉보기 파속 기준으로는 판 속도 0.05–0.12 | 카드 §3-2 · §3-4 · 논문 p.603 · p.606 · Fig. 4 | 설정 · 판정문 = 인쇄 · m/s = [카드 산술] · 비 · 값 = [판독 · 카드 산술] | 판정이 눈 대조 (에너지 · 수치 기준 없음) · 탄성 발포체 · 재하율 효과의 방향이 우리 MPM 과 반대 (카드 §9 ⑥)
- [f] bardenhagen2005_mpm_foam_densification_simulation | 붙는 접촉의 틈: 한 속도장의 접촉은 셀 크기 급 거리에서 걸리므로 strut 지름 10–14 셀 · 틈 0.5–1 셀이면 틈이 뼈대 부피의 7–21 % = ε 0.9 에서 기공 5–20 %p 급 — 그 논문은 재지 않음 | 카드 §9 ⑩ | [카드 추론 · 카드 산술 · 가정: 단위 셀 1 mm] | 논문 주장 아님

## g — 2D → 3D 경고 · 증거

- [g] bardenhagen2005_mpm_foam_densification_simulation | 계산은 **3D** (본문에 '3D simulation' 낱말은 없고 *1 mm³ block* · *spherical nodes* · 원근 그림 · *viewed from below* 로 알 수 있음) · 2D ↔ 3D 를 견준 문장 없음 ('two-dimensional' 은 참고문헌 제목 한 번) | 카드 §0-2 (iii) · 논문 p.603–604 · Fig. 2 · 7 | [카드 판독] | 2D → 3D 전이의 증거를 주지 않음
- [g] bardenhagen2005_mpm_foam_densification_simulation | 차원 대신 **크기** 경고: *"Although it is tempting to suggest the results in Fig. 6 are representative of bulk foams with similar microstructures, it is unlikely to be the case.  Much bigger unit cells need to be considered …  Accurate determination of bulk foam response requires finding the necessary size of a representative volume element (RVE) of material."* · 필요한 규모 100–1000 기공 | 카드 §0-2 (iii) · §3-9 · 논문 p.610 · p.615 | 인쇄 | 발포체 — 작은 단위 셀의 값을 거시 값으로 옮기지 말라는 일반 경고로만

## h — DEM 에서 FE · MPM 으로 넘긴 선례

이 배치에 없음 (DEM 이 논문에 없음 · 출발 형상은 손으로 만든 뼈대).  관련만:
- [h] bardenhagen2005_mpm_foam_densification_simulation | 영상 → 물질점: *"for a particle method, an array of pixel intensities representing an image can be easily discretized"* · X 선 단층 영상은 *"a data format which should be easily discretized via particle methods"* — 전망으로만 (이 논문의 계산은 이상화 단위 셀) | 카드 §12 D · 논문 p.602 · p.615 | 인쇄 | 실제로 영상에서 넘긴 계산은 이 논문에 없음 (`devaucorbeil2020…` 카드의 *image-based* 표기는 이 논문으로는 받쳐지지 않음)

## i — 복합 양극 (AM + SE) 의 압력별 기공

이 배치에 없음.

## j — 카드가 스스로 적은 한계 (가압 · 탈압과 닿는 것)

- [j] bardenhagen2005_mpm_foam_densification_simulation | 탄성 재료 · 붙는 접촉뿐: *"Effects due to including more realistic models, such as viscoelasticity for polymeric foams, plasticity for metallic foams, and frictional sliding contact, will be studied later."* | 카드 §11 #1 · 논문 p.601 | 인쇄 | 소성 · 미끄럼 · 분리가 드는 가압 · 탈압 계산의 근거가 못 됨
- [j] bardenhagen2005_mpm_foam_densification_simulation | 준정적을 명시적 풀이로 흉내 (*"less elegant"*) · 암시적 풀이는 *"expensive, and remain an area of algorithm research"* | 카드 §11 #4 · 논문 p.602 | 인쇄 | 판정은 절반 속도 런과의 눈 대조
- [j] bardenhagen2005_mpm_foam_densification_simulation | 반력의 잡음은 작은 단위 셀의 산물 (*"divided by a larger measurement area"*) · 불안정 (snap-through) 구간은 관성이 지배할 수 있음 | 카드 §11 #5 · #7 · 논문 p.606 · p.612 | 인쇄 | 작은 RVE 의 판 반력을 읽을 때 같은 주의
- [j] bardenhagen2005_mpm_foam_densification_simulation | 단위 셀이 대표 부피가 아님 · '두 배 규칙' 은 두 사례 (*"not conclusive"*) · 직렬 계산 | 카드 §11 #2 · #8 · #10 · 논문 p.610 · p.612 · p.614–615 | 인쇄 | —
- [j] bardenhagen2005_mpm_foam_densification_simulation | 물질점이 셀 경계를 넘을 때의 오차 (큰 변형률의 반력 튐) | 카드 §11 #6 · 논문 p.603 | 인쇄 | 조밀 끝의 반력 판독에 잡음

## k — DEM 의 한계 (서지 병기)

- [k] bardenhagen2005_mpm_foam_densification_simulation (Bardenhagen · Brydon · Guilkey · J. Mech. Phys. Solids 53, 597–617, 2005) | **말 없음** — DEM 을 쓰지도 언급하지도 않는다 ('DEM' · 'discrete element' 0 회 · 참고문헌 34 건에도 없음).  한계를 적은 대상은 유한요소법이다 (질문 l).  다른 입자 기법에 대한 말은 한 구절: *"The method uses a grid to interact particles, as opposed to pairwise interactions as used in Smooth Particle Hydrodynamics."* | 카드 §0-2 (i) · 논문 p.601 | 인쇄 + [카드 전문 검색] | DEM 한계의 인용처로 쓸 수 없음

## l — 소성변형이 왜 어려운가 (서지 병기)

- [l] bardenhagen2005_mpm_foam_densification_simulation (Bardenhagen · Brydon · Guilkey · J. Mech. Phys. Solids 53, 597–617, 2005) | 큰 변형이 격자 기법에 어려운 까닭: *"Even at moderate bulk deformations, e.g. within the stress plateau, localized bending at the microscale results in large deformations and rotations of the individual structural components (struts, membranes).  Hence finite deformation continuum mechanics formulations must be implemented, including appropriate kinematics and constitutive models.  Large strains result in numerical inaccuracies as Lagrangian meshes become too distorted or Eulerian meshes require extensive material advection."* | 카드 §0 (1) · 논문 §1 p.599 | 인쇄 | 발포체 뼈대에 대한 문장 · 2005 년 시점 · 소성 자체는 이 논문에 없음
- [l] bardenhagen2005_mpm_foam_densification_simulation (같은 서지) | 자기 접촉이 어려운 까닭: *"Contact algorithms themselves are an area of ongoing research Zhong and Mackerie (1994).  Simulation results are often found to be strongly dependent on the specific values of the algorithm's parameters, which are generally only loosely tied to material properties.  Common algorithms, such as master and slave, require the identification a priori of candidate contact surfaces, which is only possible early in the deformation for foam microstructures, if at all."* → *"Consequently, foam micromechanics simulations with FEM have been forced to focus on modest deformation foam behavior"* | 카드 §0 (1) · 논문 §1 p.599 | 인쇄 | 후보 B (입자별 유한요소) 를 견줄 때의 인용처 — 이후의 FEM 접촉 기법 발전은 반영 안 됨
- [l] bardenhagen2005_mpm_foam_densification_simulation (같은 서지) | 택한 우회 = 입자 기법 (GIMP): 물질점이 상태 · 계면을 싣고 격자는 매 걸음 새로 (*"eliminating mesh tangling problems"*) · 준정적은 명시적 풀이를 천천히 (*"While less elegant, it is also possible to obtain quasi-static results with an explicit code provided the loading is applied slowly enough."*).  **소성은 넣지 않음** (*"plasticity for metallic foams … will be studied later"*).  **맞춘 값 = 0 개** (재료 상수를 정해 놓고 계산).  **검증** = 꽉 찬 블록 해석해 1 건 (≈ 5 %) + Gibson–Ashby 선의 1.5–3.9 배 + 남의 실험과 정성.  **비용** = *"(serial) calculations"* 뿐 — 물질점 수 · 걸음 수 · 시간 미인쇄 | 카드 §0-2 (ii) · §3-8 · §3-9 · 논문 p.601–603 · p.615 | 인쇄 · 배수 = [판독 · 카드 산술] | 무르게 맞춘 영률 같은 우회는 없음 (실제 계수 그대로 · 물체 하나라 재배열이 없음)

## m — 받아들일 통찰 (무엇을 · 우리 쪽 어디에 · 근거)

- [m] bardenhagen2005_mpm_foam_densification_simulation | **기공 연산자를 두 꼴로 적고 서로 점검한다** — p_fix = 1 − (씨앗 때 고체 부피)/V_bulk (지금 우리 MPM · 논문 식 2 꼴) 과 p_trk = 1 − (물질점으로 추적한 고체 부피)/V_bulk (논문 식 1 꼴).  항등식 p_trk − p_fix = (고체 분율) × (1 − J) · 순수 SE 300 MPa 에서 ≈ 1.1 %p (누른 채) · 점검 = 추적한 부피 변화가 평균 압력 ÷ K 와 같은 부호 · 자릿수인가 (그 논문의 lattice 곡선은 고체 부피 +11 % 로 읽혀 이 점검을 통과하지 못한다) | 단계 0 | 카드 §3-6 · §8-2 · §9 ③ ④ ⑤ · 논문 식 (1)(2) p.610 · Fig. 8 (인쇄 + [판독 · 카드 산술] + [우리 코드 판독 · `scripts/mpm3d_compaction.py` 2794 · 3261 행])
- [m] bardenhagen2005_mpm_foam_densification_simulation | **준정적 판정을 수로 적는다** — 절반 속도 쌍에서 구간 평균 반력의 비와 차의 rms 를 통과 기준으로 · 판 반력과 바닥 반력의 차 (관성) 를 함께 기록 · 접촉망이 막 생기는 느슨한 구간에는 침대의 겉보기 파속 기준 Mach 를 병기.  그 논문은 고체 종파속 기준 0.03 ↔ 0.015 를 눈으로 "similar" 라 했는데 구조가 무너지는 구간의 평균 반력은 35 % 달랐다 | 단계 2 ; 단계 4 ; 단계 5 | 카드 §3-4 · §9 ⑥ · §10 행동 3 · 논문 p.603 · p.606 · Fig. 4 ([판독 · 카드 산술])
- [m] bardenhagen2005_mpm_foam_densification_simulation | **접촉 없는 꽉 찬 블록 ↔ 해석해** 를 단위 시험으로 — 옆이 막힌 (일축 변형) 블록을 판 Mach 두 단으로 누르고 오차를 변형률 구간별로 기록 (그 논문은 끝 값 5 % 만 적었고 구간 평균은 +5.5–6.6 % 한쪽으로 치우쳐 있었다 · 조밀 끝에서는 응력 5 % 가 판 위치 0.32 셀) | 단계 2 (단위 시험) | 카드 §3-3 · §10 행동 2 · 논문 p.602–603 · Fig. 1 (인쇄 + [판독 · 카드 산술])
- [m] bardenhagen2005_mpm_foam_densification_simulation | **조밀 충전 압축의 해상도 수렴에서 기공 자체를 관측량으로** (반력만 보지 않는다) — 붙는 접촉은 셀 크기 급 거리에서 걸려 틈이 기공으로 남을 수 있고, 그 논문은 남은 기공 35–38 % 의 해상도 의존을 재지 않았다.  덧붙여 반력 곡선을 매끈하게 만들 때 창 · 차수 · 맞춘 런을 적는다 (그 논문의 5차 맞춤선은 느린 런 쪽인데 빠른 런의 원자료와 한 그림에 놓였다) | U6 ; 단계 4 ; 후보 A | 카드 §9 ⑦ ⑩ · §10 행동 4 · 5 · 논문 Fig. 4 · 6 · 10 ([카드 추론] · [판독 · 카드 산술])

## n — 논문 에이전트 후보 (litdb 에 카드 없음 · 많아야 다섯)

(서지는 이 논문 참고문헌 목록에 적힌 그대로 · litdb 확인 = 정본 `papers/` 파일 목록에서 제1 저자 성 · 제목 낱말을 찾음 — 파일 없음.  괄호 안은 그 논문을 언급만 하는 기존 카드.)

- [n] Bardenhagen, S.G., Kober, E.M., 2004. The generalized interpolation material point method. Comp. Model. Eng. Sci. 5, 477–496. | f — 이 논문이 쓴 기법 (GIMP · contiguous-particle 변종) 의 원전 · 물질점이 셀 경계를 넘을 때의 오차 (Fig. 1 의 반력 튐을 이 논문이 넘긴 자리 · 카드 §3-3 · §4-1) → 우리 B-spline 가중과의 비교 기준 | 카드 없음 (언급만: devaucorbeil2020 · gritton2017 — 배치 40 에서도 후보로 올림)
- [n] Guilkey, J.E., Weiss, J.A., 2003. Implicit time integration for the material point method: quantitative and algorithmic comparisons with the finite element method. Int. J. Numer Meth. Eng. 57, 1323–1338. | f · l — 준정적을 암시적 MPM 으로 풀고 FEM 과 정량 비교한 논문 (이 논문이 *"expensive … area of algorithm research"* 로 가리킨 자리 · 카드 §3-9 · §4-4) → 명시적 풀이를 천천히 돌리는 것의 대안과 그 비용 | 카드 없음
- [n] Cummins, S.J., Brackbill, J.U., 2002. An implicit particle-in-cell method for granular materials. J. Comp. Phys. 180, 506–548. | f · l · d — **입자 재료**의 암시적 PIC (같은 자리 · 카드 §3-9) → 가루 침대의 준정적 압축을 MPM 계열로 푼 선례 후보 | 카드 없음
- [n] Sulsky, D., Chen, Z., Schreyer, H.L., 1994. A particle method for history-dependent materials. Comp. Methods Appl. Mech. Eng. 118, 179–196. | f · l — MPM 원전: 이력 의존 (소성) 재료의 상태를 물질점에 싣는 까닭 (카드 §4-1 의 계보) → "소성을 입자 기법에 넣는 방법" 의 1 차 인용처 | 카드 없음 (언급만: devaucorbeil2020 · stomakhin2013 등)
- [n] Smith, R.A., Paulus, M.J., Branning, J.M., Phillips, P.J., 2001. X-ray computed tomography on a cellular polysiloxane under compression. J. Cell. Plastics 37, 231–248. | m (단계 0) — 누른 채 X 선 단층으로 기공을 잰 실험 (처음 48 % → ε 0.5 에서 13 % → 0.6 에서 6 % · 카드 §3-6 · §3-8) → 계산 기공 (식 1 꼴) 과 영상 기공을 견주는 방법의 선례 · 재료는 고분자 발포체 | 카드 없음

## 카드 문제

- 새 카드 자체의 모순은 찾지 못함.  읽을 때의 주의 넷:
  1. `[판독]` 값은 논문에 인쇄된 수가 아니다 — 벡터 그림의 경로 좌표 (Fig. 2 · 7 은 200 dpi 내장 래스터의 화소) 에서 읽었다.  추세 · 자릿수용.
  2. 카드가 그림에서 **역산한 것** (논문의 주장이 아님 · 카드 §12 B): neo-Hookean 저장 에너지의 꼴 · Gibson–Ashby 선 = 0.05 E_s φ² · 5차 맞춤선이 느린 런 쪽이라는 것 · stiffened 런의 판 속도 · J = (1 − p)/(1 − p_inc).
  3. "lattice 의 기공이 비압축선 아래 = 부피 측도의 오차" · "붙는 접촉의 틈이 기공 5–20 %p 급" 은 [카드 추론] 이다 — 원자료 · 코드로 확인한 것이 아니다.
  4. 단위 셀 변 길이가 미인쇄라 "strut 지름당 10–14 셀" 은 가정 (셀 변 = 1 mm) 위의 산술이다.
- 정본의 다른 카드: `devaucorbeil2020_mpm_after_25_years_review` 56–59 · 76 행이 이 논문을 *image-based (voxel → 입자) 치밀화 · multi-contact* 의 선례 · *"우리 scaffold 접근의 직접 선례"* 로 적었으나, 이 논문의 계산은 손으로 만든 이상화 단위 셀 · 붙는 접촉이다 (영상 기반 이산화는 전망으로만 · p.602 · p.615).  그 카드에 2026-11-11 정오 줄을 붙였다 (리뷰 원문이 가리킨 논문은 [미확인]).
- 논문 쪽 인쇄 어긋남 · 걸리는 곳 (카드 §12 C): 상대밀도 7.9 · 9.6 % ↔ Fig. 8 출발점 7.82 · 9.71 % · Fig. 6 범례 *plateau stress* ↔ 캡션 *yield stress* · Fig. 6 · 10 에 속도가 다른 런의 선이 섞임 · *"about 35%"* 는 0.345 · 0.384 를 뭉뚱그린 값 (lattice 는 비압축 추정으로도 0.218 이 남는 지점) · *"two orders of magnitude lower"* ↔ 1/43 · 1/70 · Fig. 7 의 큰 구멍 (lattice) ↔ Fig. 8 의 부피 기공 (lattice 가 더 작음) · Fig. 4 축 이름이 원본에서 잘림 · σ_eq 식의 근호가 이웃 줄과 겹쳐 인쇄.

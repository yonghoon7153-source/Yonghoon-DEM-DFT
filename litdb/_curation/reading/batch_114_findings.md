# batch 114 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 표 N-75 · 대피 세션)

대상: `mullikin1993_surface_area_estimation_digitized_planes` — J. C. Mullikin · P. W. Verbeek, "Surface area estimation of digitized planes", *Bioimaging* **1** (1993) 6–16 (1 호 · 접수 1992-10-21 · IOP Publishing) · DOI 10.1002/1361-6374(199303)1:1<6::AID-BIO3>3.0.CO;2-3 (내려받기 표지에만)
이진 3D 영상의 넓이를 6-연결 표면 복셀의 노출 배치 9 부류 (S1–S9) 가중합으로 재는 국소 추정기 — 평면 세 부류의 가중을 무작위 방향 · 위치 평면에서 치우침 0 + 평균 제곱 오차 최소로 해석적으로 풀고 (식 7–8 · W₁ 0.8940 · W₂ 1.3409 · W₃ 1.5879 · 평면 CV 2.33 %), 평면 · 이진 구 · 침식 구조 원소로 시험 — DEM · MPM · 역학 · 재료 · 압력 없음.
쪽 = 학술지 쪽 p.6–16 (PDF 쪽 = 학술지 쪽 − 5) · 판독 원자료 = `litdb/figures/mullikin1993_surface_area_estimation_digitized_planes/digitized.csv` (280 행 · Fig. 5–7) · 고른 의도 = '단계 7 (형상 · 피복 넓이 진단) — 복셀 면 면적 S1–S6 가중치의 도출 · 구 · 원기둥 성능 · 물체/배경 평균 처방의 원전' → 의도 대조 결과 **일부** (S1–S3 도출 · 구 성능 · 평균 처방 = 채움 · S4–S6 도출 = 없음 (공간 격자 값 차용) · 원기둥 성능 = 없음 (원기둥 = 평면 시험의 넓이 1 창)).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 재료 · 압력 · 기공 없음 (넓이 추정 이론).  랩 표준 (순수 SE 기공 10–13 % · 진밀도 1.64 g/cm³) 과 나란히 놓을 숫자 없음 (카드 §8 단계 0).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음.

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음.

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음.

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙이 없다.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 MPM 없음.  해상도 · 수치 오차 추정 쪽 근거만 (넓이 측정의 규칙 — MPM 역학 규칙 아님):
- [f] mullikin1993_surface_area_estimation_digitized_planes | 평판 조각의 넓이 σ 가 방향 바닥 (최적 가중 0.0233) 의 +10 % 안에 드는 것은 지름 방향 표본 ≈18.5 개부터 (10.1 개 0.033 · 5.4 개 0.062 · 3.3 개 0.122) · 공간 격자 (바닥 0.102) 는 ≈10 개에서 +3 % 안 · 위치 성분 (σ² 에서 바닥을 뺀 것) 은 두 가중이 같고 ∝ 표본^−1.4 | 카드 §3-4 · Fig. 5(b) | [판독 + 카드 산술 · 두 성분 독립 가정] | 넓이 1 원기둥 창 안의 평면 · 무작위 방향 · 위치
- [f] mullikin1993_… | 수치 오차 추정 방법: 원점을 가운데 복셀 안 균일 무작위로 N 회 (평면 10⁴ · 구 100) → 평균 · 표준편차 · 95 % 신뢰 한계 (*"95% confidence limits for the mean of 10000 trials assuming a standard deviation of 0.0233"*) · 판독: Fig. 5(a) 50 점의 표준편차 2.33 × 10⁻⁴ = 0.0233/√10⁴ 그대로 | 카드 §3-4 · p.11 · Fig. 5(a) | [인쇄 · 판독 + 카드 산술] | —
- [f] mullikin1993_… | 표본 간격 조건: *"the volumetric data must be properly sampled. The sample spacing must satisfy the Nyquist criterion with respect to the resolution of the imaging device"* | 카드 §3-8 · p.7 | [인쇄] | 영상 해상도 기준 (모의 격자의 지름당 셀 수 규칙 아님)

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] mullikin1993_surface_area_estimation_digitized_planes | ★ 곡률 편향의 차원 의존: *"A similar underestimation occurs when calculating the perimeter length of disks using corner-count chain-code weights optimized for straight lines of infinite length. In that case, however, a constant can be added (Young 1988) because underestimation is independent of disk radius. For spheres, surface area underestimation is proportional to sphere radius in addition to an overall offset"* — 2D 원판 = 상수 · 3D 구 = 반지름 비례 + 상수 (구 물체만 −4.116 r + 2.610 Δ²) | 카드 §4-3 ③ · p.11 · Fig. 6 | [인쇄] | 넓이 · 둘레 추정기의 이야기 (역학 아님) — 2D 단위 시험이 3D 곡률 편향을 못 보여 준다는 근거
- [g] mullikin1993_… | 2D → 3D 일반화 문장: *"If one considers the contribution as a function of the number of exposed sides rather than step direction, as in the Freeman approach, then the perimeter length can be generalized to hyper-surface area in any dimension"* | 카드 §4-3 ③ · p.8 | [인쇄] | —

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] mullikin1993_… | 원문 한계: 평면 CV 는 해상도를 올려도 바닥으로 수렴 (*"the CV of the estimate asymptotically approaches a given lower bound. This is a result of the anisotropy of the surface normal"*) · 구는 과소 → 물체 · 배경 평균 + 상수 보정 (p.15–16) · S4–S6 는 *"of lesser significance"* 라 공간 격자 값 (p.11) | 카드 §3-8 · §11 | [인쇄] | 가압 · 탈압 언급 없음 — 압밀 뒤 계면 넓이를 복셀로 잴 때만 닿는다
- [j] mullikin1993_… | 카드가 적은 범위 밖: 세 상 (AM · SE · 기공) 계면 나누기 · 오목 · 닿은 두 물체 · 원기둥 · 비등방 격자 · 방향이 몰린 계면 (압축축 모자 · 근축면 원판) 의 불편 | 카드 §7-3 · §13 | [카드 해석 · 미확인] | 압밀 침대의 AM \| SE 계면은 원문 조건 (두 상 · 볼록 · 방향 무작위) 을 어긴다

## k — DEM 의 한계 (원문 문장 · 인용 서지 = Mullikin & Verbeek 1993, Bioimaging 1, 6–16)
- [k] mullikin1993_surface_area_estimation_digitized_planes (Mullikin & Verbeek 1993 · Bioimaging 1, 6–16) | **말 없음** — 입자 · 접촉 · DEM · 역학 · 압력 0 회 (11 쪽 전수) | 카드 §4-3 ① | [인쇄 전수] | DEM 한계 진술로 인용하지 않는다

## l — 소성변형이 왜 어려운가 · 우회 · 비용 (인용 서지 = Mullikin & Verbeek 1993, Bioimaging 1, 6–16)
- [l] mullikin1993_… (Mullikin & Verbeek 1993) | 해당 없음 — 역학이 없다.  비용 문장만: 이 추정기는 *"only requires the determination of surface voxel configurations from the six nearest neighbours of the cubic lattice"* (국소 · 선형 시간) ↔ 14 면체 침식은 *"its large size, the requirement of converting typical cubic lattice data to the FCC lattice and the condition that the object measured must be somewhat thicker than the structuring element size"* | 카드 §4-3 ② · p.16 | [인쇄] | 소성 · 형상 변화의 어려움은 다루지 않는다

## m — 받아들일 통찰
- [m] mullikin1993_… | 무엇을: **면 세기 "~1.5×" 의 두 번째 원문 근거** — 식 (8a) 의 계수로 노출 면 수 / 넓이 = 1·0.372249 + 2·0.249072 + 3·0.209869 = **1.500** (등방 평면) · 공간 격자 (노출 면 × 2/3) 가 불편 (β = 0 · p.11) · 구는 공간 격자 상수 −1.06Δ² (p.12) 로 **면 세기 = 1.5 × (1 − 1.06Δ²/4πr²)** (`lindblad2005_…` pilot 1.453–1.4997 과 같은 크기) · 방향별 1–1.732 · 우리 쪽 어디에: 단계 7 · 흐름 밖: STEP4 `A_face` · r1 면 막 · `am_surface_patches` 넓이 기준 한정어 · 왜: 카드 §3-3 · §7-1 · §9 ①
- [m] mullikin1993_… | 무엇을: **방향이 정해진 계면에 MV "불편" 을 쓰지 않는다** — 식 (7c) 로 한 방향 평면 = −10.6 % (축 정렬) … +3.0 % · 면 세기 1–1.732 · 해상도로 안 줄어든다 (p.15) · 우리 쪽 어디에: 단계 7 · U6 (넓이 수렴 시험은 위치 잡음 성분만 줄어드는지 본다) · 왜: 카드 §3-7 · §7-3 ① (①′ 근축면 원판 · 압축축 모자는 해석 법선 가중)
- [m] mullikin1993_… | 무엇을: **닫힌 곡면 넓이 = 물체 · 배경 평균 + 상수 보정** — 물체만 세면 구에서 −0.33 Δ/r (상대 · 우리 SE r/h 1.7–10 이면 −12 … −3 %) · 평균 뒤 +0.527Δ² (r/h 3.3 이면 +0.38 %) · 우리 쪽 어디에: 단계 7 (AM 구 표면 · 피복 분모를 복셀로 잴 때) · U1 (입자 하나 넓이 판독의 오차 바닥) · 왜: p.11 · Fig. 6 · Fig. 7(a) · 카드 §7-2 표
- [m] mullikin1993_… | 무엇을: **진단 자기시험의 원문 기대값** — 평면 β 0 · σ 0.0233 / 0.10163 / 0.12037 (최적 · 공간 격자 · 불편 표본 세기) · 축 정렬 평면 0.8940 · 구 Fig. 6 직선 · 평균 뒤 0.527 ± ~0.1 Δ² · CV 식 (9) Table 2 · Table 1 부류 몫 — 계획된 넓이 편향 진단 (`lindblad2005_…` §적용 후보 가-1) 의 MV 구현이 이 값을 재현하는지 (맞추는 데 쓰지 않음) · 우리 쪽 어디에: 결과 전 대조 항목 · 왜: 카드 §8 마지막 행 · §9 ②

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드 없음 · papers/ ls + grep 확인)
- [n] Verwer B J H 1991 Local distances for distance transformation in two and three dimensions *Pattern Recognition Lett.* **12** 671–82 (원문 목록 그대로) | 이 논문의 식 (7) 과 **같은 식** · 같은 값이 *"table 6"* 에 · Mathematica 스크립트 제공 — 단계 7 (복셀 걸음 경로 길이 · τ_geo 류 격자 거리의 최적 국소 거리) · f (해상도) · 카드 §3-2 ⑧ · §12 | litdb 확인: papers/ 에 verwer* 없음 · 'Verwer' grep 0 · 'chamfer' grep 0
- [n] Hahn U and Sandau K 1989 Precision of surface area estimation using spatial grids *Acta Stereol.* **8** 425–30 (원문 목록 그대로) | 공간 격자 = S4–S6 가중값의 출처 · 평면 σ 상한 식 (6) → ≅ 0.102 — 단계 7 · 카드 §3-6 | litdb 확인: papers/ 에 hahn* · sandau* 없음 · 'Sandau' grep = `windreich2003_…` (인용만)
- [n] Eberly D, Lancaster J et al 1991 On gray scale image measurements: II. Surface area and volume *CVGIP: Graphical Models and Image Process.* **53** 550–62 (원문 목록 그대로) | 표본 세기 · 표본 법선 방법 · 구에서의 표본 세기 비 (*"table 3"*) — 16.8 % 과소를 구로 본 원전 · 결과 전 대조 항목 · 카드 §3-3 | litdb 확인: papers/ 에 eberly* 없음 · 'Eberly' grep 0
- [n] Meyer F 1992 Mathematical morphology: from two dimensions to three dimensions *J. Microsc.* **156** 5–28 (원문 목록 그대로) | 팽창 / 침식 넓이 · CC · FCC 시험선 — Table 3 의 비교 대상 · 단계 7 대안 추정기 | litdb 확인: papers/ 의 meyer* = meyer2017 · meyer2018 (캘린더링 · 다른 Meyer) · 'Mathematical morphology' grep 0
- [n] Young I T 1988 Sampling density and quantitative microscopy *Anal. Quant. Cytol. Histol* **10** 269–75 (원문 목록 그대로) | 원판 둘레의 상수 보정 (2D 짝) · 표본 밀도 (Nyquist) — f · g · U1 (해상도 규칙) | litdb 확인: papers/ 에 young1988* 없음 · 'Sampling density and quantitative' grep 0 · 'Quant. Cytol' grep 0

## 카드 문제
- `windreich2003_voxel_based_surface_area_estimation` **L191** (n/a 목록) *"Mullikin & Verbeek 1993 원문 (S1–S6 가중치 도출 · 구·원기둥 성능)"* — 원문에 **S4–S6 도출이 없고** (공간 격자 값 차용 · p.11) **원기둥 물체 성능도 없다** (원기둥 = 평면 시험의 넓이 1 창 · p.10–11) → 기대한 두 항목이 원문과 다르다 (경미 · 고치지 않음).  후보 표 N-75 의 '왜' 칸 ("구 · 원기둥 성능") 도 같은 기대에서 왔다.
- `windreich2003_…` **L174** *"S1–S6 가중치는 원저자 [9] … 의 값을 이 논문이 인용한 것 — 원전 PDF 미확인"* — 값은 원문과 같다 (0.894 = 0.8940 · 1.3409 · 1.5879 · 2 · 8/3 · 10/3).  "원전 미확인" 은 이 카드로 풀렸고, S4–S6 은 원저자가 **도출한** 값이 아니라 시뮬레이션에 쓴 공간 격자 값이라는 한정이 빠져 있다 (경미).
- 비교 문서 `comparison_vs_ours_DEM.md` [Windreich03] 블록의 *"S1–S6 가중은 원전 미확인 (MV 1993 카드 없음)"* — 낡은 줄 (같은 절에 [MullikinVerbeek93] 블록을 더했고 그 줄은 고치지 않음).
- 그 밖에 확인한 2 차 인용 — 같음: `windreich2003_…` L34 (서지 · 출처 배분) · L42–50 (가중 · S7–S9 의 지위 · S8 = 마주 보는 두 쌍 (원문 Fig. 2 '선') 은 그 카드가 적은 캡션 쪽과 같음) · L52 · L53 (축 정렬 −10.6 %) · L56 (Table 1) · L101 (평균 처방) · L169 · L62–L65 (그 논문의 판독 = 이 논문 상수 · 식 (9) 와 같은 크기) / `lindblad2005_…` L30 · L39 · L40 · §7-3 표 A (pilot "MV 물체" 열 = 원문 Fig. 6 직선과 r/h ≥ 5 에서 0.0005 안 · "면 세기" 열 = 1.5 × (1 − 1.06Δ²/4πr²) 와 sd 안).  (줄 번호 = 이 카드가 두 카드 머리에 '관련 카드' 한 줄을 더하기 전 기준 · 지금은 +1.)

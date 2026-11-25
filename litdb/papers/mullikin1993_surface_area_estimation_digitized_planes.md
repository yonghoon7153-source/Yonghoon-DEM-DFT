<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 이 묶음 (후보 표 N-75 · 우선순위 2 · 정독 114 · 대피 세션) 에서 꼭 뽑으라고 한 항목.
     본 = mcgrogan2017_compliant_brittle_li2s_p2s5_glass_nanoindentation.md (절 번호 체계 · 머리 요약 상자 · 메타 줄 · 서지 표 · 그림 표) · 같은 축 = windreich2003_voxel_based_surface_area_estimation.md · lindblad2005_surface_area_weighted_local_configurations.md (서로 가리킴).
     원문 = 스캔본 11 쪽 (쪽마다 8 비트 회색 래스터 한 장 ≈ 300 dpi + 숨은 OCR 글자 층 — 낱말이 벌어지고 'Yerbeek' · 'IOO' 처럼 깨진다 → 숫자 · 식 · 인용 문장은 전부 쪽 그림을 보고 옮겼다).
     쪽 표기 = 학술지 쪽 p.6–16 (쪽 아래 번호).  PDF 쪽 = 학술지 쪽 − 5.  크롭 txt 이름의 pN = 학술지 쪽 · figures.json 의 page = PDF 쪽.
     오른쪽 여백의 세로 글 = 내려받기 표지 (출판사 사이트가 붙인 벡터 글) — 1993 인쇄면이 아니다.  DOI 는 이 표지에만 있다.
     보충 자료 (SI) 없음 · 그림 8 · 표 3 · 번호 붙은 식 9 묶음 (26 줄: 1a–c · 2a–d · 3a–b · 4a–c · 5a–b · 6a–f · 7a–c · 8a–b · 9) + 번호 없는 식 3 · 참고문헌 23.
     값 표지: [인쇄] = 본문 · 그림 · 표에 인쇄된 값 · [판독] = 그림에서 읽은 값 (재현 = litdb/figures/<slug>/digitized.csv 280 행 — 쪽을 300 dpi 로 렌더 (= 원 래스터) · 축 = 틀 선 + 틀 끝 눈금 글자 · 표지 = 이진 열림 연산 뒤 무게중심) ·
     [카드 산술] = 인쇄 · 판독 값으로 이 카드가 계산한 값 (식 병기 · 식 (7)(8) 재현 = 가우스–르장드르 400 × 400 적분) · [카드 해석] = 원문에 말이 없어 카드가 읽은 뜻 · [우리 산술] = 우리 쪽 값과 견주는 계산 · [미확인] = 11 쪽 전수에 없음.
     계산 모델 (DEM · MPM · FEM) · 재료 · 실험 없음 — 이진 3D 영상의 넓이 추정 이론 + 몬테카를로 시험. -->
# Surface area estimation of digitized planes — Mullikin & Verbeek (Bioimaging 1993) · 6-연결 표면 복셀 9 부류 넓이 가중의 원전: 무작위 방향 · 위치 평면에서 치우침 0 + 평균 제곱 오차 최소 (W₁ 0.8940 · W₂ 1.3409 · W₃ 1.5879 · 평면 CV 2.33 %) · S4–S6 = 공간 격자 값 차용 (도출 아님) · 이진 구는 물체 · 배경 평균 뒤 상수 +0.527Δ²

> slug `mullikin1993_surface_area_estimation_digitized_planes` · DOI `10.1002/1361-6374(199303)1:1<6::AID-BIO3>3.0.CO;2-3` · type `method (digital geometry — six-connected surface-voxel area weights · analytic bias and mean-square-error integrals over randomly oriented and positioned planes, solved numerically · planar-window and binary-sphere Monte-Carlo checks · erosion structuring-element comparison) · 전지·DEM·MPM 없음` · PDF `d24c923d-75._Surface_area_estimation_of_digitized_planes.pdf` · digested `2026-11-16` · status ✅
>
> **저자**: **James C Mullikin** · **Piet W Verbeek** — Pattern Recognition Group, Delft University of Technology, Lorentzweg 1, 2628 CJ Delft, The Netherlands (교신 표시 없음) · *Bioimaging* **1** (1993) **6–16** · *"Printed in the UK"* · *"Received 21 October 1992"* · 쪽 아래 *"0964-1726/93/010006+11$07.50 © 1993 IOP Publishing Ltd"* · 키워드 *surface area, estimator, digitized planes, unbiased, minimum mean-square-error, three-dimensional, optimal weights, numerical integration, simulations* · 지원 = *"the Netherlands' Project Team for Computer Science Research, SPIN (project three-dimensional analysis)"* · 감사 = Dr Verwer (3D chamfer 거리 변환의 치우침 · MSE 를 계산하는 Mathematica 스크립트를 줌).
> ⚠ DOI 는 **내려받기 표지** (쪽 오른쪽 여백 세로 글 · 둘째 쪽부터) 의 주소 *"…/doi/10.1002/1361-6374(199303)1:1<6::AID-BIO3>3.0.CO;2-3"* 에서 옮겼다 — 1993 인쇄면에는 DOI 가 없다.  같은 표지의 *"13616374, 1993, 1"* = ISSN · 해 · 호 (1 호).
> **짝 카드 (서로 가리킴)**: [`windreich2003_voxel_based_surface_area_estimation`](windreich2003_voxel_based_surface_area_estimation.md) (이 논문 = 그 논문의 [9] · S7–S9 가중을 새로 정함) · [`lindblad2005_surface_area_weighted_local_configurations`](lindblad2005_surface_area_weighted_local_configurations.md) (이 논문 = 그 논문의 [8] · 2×2×2 로 개선) · [`ziegel2010_surface_area_measure_digitizations`](ziegel2010_surface_area_measure_digitizations.md) (2×2×2 점근 최악 3.98 %) · [`neumann2021_garnet_3d_structure_grain_boundaries_li_transport`](neumann2021_garnet_3d_structure_grain_boundaries_li_transport.md) (복셀 면에 입계 조건) · [`chouchane2019_innov_voxelization_multiphase_meshing`](chouchane2019_innov_voxelization_multiphase_meshing.md) (복셀 → 사면체 · 피복 % 는 분리면 삼각형).
> **판독 원자료**: `litdb/figures/mullikin1993_surface_area_estimation_digitized_planes/digitized.csv` (280 행 — Fig. 5(a) 표지 50 · Fig. 5(b) 표지 36 (두 계열) · Fig. 6 사슬 양 끝 · Fig. 7(a) 표지 117 덩어리 (겹친 둘 3 · 반쯤 가린 1 포함) · Fig. 7(b) 표지 72 덩어리 · 요약 3) · 크롭 **52 장** (그림 8 + 패널 6 · 표 3 · 식 15 · 근거 문단 20 — 전부 손 크롭 · 다시 자름 6) — `figures.json`.

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 이진 3D 영상에서 물체의 넓이를 재려고, 배경과 **6-연결** 인 물체 복셀 (= 표면 복셀) 을 노출 면의 개수 · 배치로 9 부류 (S1–S9) 로 나누고, 평면에 나타나는 세 부류 (노출 면 1 개 · 이웃한 2 개 · 이웃한 3 개) 의 가중을 **무작위 방향 · 위치 평면에서 치우침 0 (식 7a) 이 되게 하면서 평균 제곱 오차 (식 7b) 를 최소** 로 풀어 **W₁ ≈ 0.8940 · W₂ ≈ 1.3409 · W₃ ≈ 1.5879** (격자 단위², 평면 CV **2.33 %**) 를 얻었다 — 같은 식이 3×3×3 chamfer 거리 변환의 최적 국소 거리 식과 **똑같다** (Verwer 1991).
곡면에만 나오는 S4–S6 은 **최적화하지 않고 공간 격자 (spatial grid) 의 같은 값 (2 · 8/3 · 10/3) 을 썼고**, 판 · 선 · 점 (S7–S9) 은 가중이 없다.  이진 구에서는 물체만 세면 **반지름에 비례해 과소** (Fig. 6: Error = −4.116 r + 2.610 Δ²) 라, **물체에 6-연결된 배경 복셀의 넓이와 평균** 하면 선형 부분이 사라지고 **상수 +0.527Δ²** 만 남는다 (Fig. 7(a)).

| 우리 질문 (이 묶음) | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ① ★ 표면 복셀 정의 · 유형 | *"Surface voxels are defined as object voxels which are six-connected to one or more background voxels"* (초록) · S1 · S2 · S3 = 노출 면 1 · 2 · 3 개, 서로 **이웃한** (adjacent = 마주 보는 두 면이 함께 노출되지 않음) · 평면에는 이 셋만 (세 점이 한 줄에 있으면 가운데 점이 평면 양쪽일 수 없다) · 곡면 S4–S6 · 병적 (판 · 선 · 점) S7–S9 (Fig. 2) · 6-연결 배치 63 개가 9 부류의 회전으로 다 덮인다 (각주) | [인쇄] p.6 · p.8 · Fig. 1–2 |
| ② ★ 가중의 도출 | 법선을 대칭이 없는 구면 조각 (구의 1/48 · 식 1a–1b) 으로 줄이고 · 법선은 그 조각 넓이에 균일 · 평면과 선분 PA 의 교점은 PA 위 균일 (p.9) → 부류 확률 (식 4) → 넓이 1 의 평면 조각의 추정 Â = W₁(n_x − n_y) + W₂(n_y − n_z) + W₃ n_z (식 7c) → 치우침 β = 0 (식 7a) 아래 σ² (식 7b) 최소 → 수치 적분 (Mathematica) 의 결과 식 (8a) · (8b) → **W₁ ≈ 0.8940 · W₂ ≈ 1.3409 · W₃ ≈ 1.5879 · CV = σ/µ = 2.33 %** · *"These values can also be found in the account of Verwer (1991, table 6)"* | [인쇄] p.9–10 · 식 (1)–(8) · [카드 산술] 계수 6 자리 · 최적값 재현 (§3-3) |
| ③ ★ S4–S6 · S7–S9 의 지위 | S4–S6: 구에서 드물어 (Table 1: r 5 에서 5.64 % · r 15 에서 0.82 %) *"of lesser significance"* → *"we set weights for surface voxel types S4–6 to W4 = 2, W5 = 8/3 and W6 = 10/3, which are the equivalent spatial grid weights"* — **최적화한 값이 아니다** · S7–S9: 가중 없음 (*"pathological situations"*) | [인쇄] p.8 · p.11 · Table 1 |
| ④ ★ 평면 성능 | 넓이 1 단위인 평면 조각 (반지름 r = π^−0.5 원기둥 창) 을 무작위 위치 10⁴ 회: 평균 오차가 95 % 한계 안 (가장 성긴 두 점만 밖) · σ 가 해상도와 함께 이론 바닥 **0.0233** (최적) · **≈0.102** (공간 격자, Hahn–Sandau 식의 상한 √((4/9)(1 + 4/π) − 1)) 로 간다 (Fig. 5) · [판독 Fig. 5(b)] 최적 가중은 지름 방향 표본 ≈**18.5 개** 에서 바닥 +10 % 안 (0.0251) · 10 개면 0.033 · 5.4 개면 0.062 | [인쇄] p.11 · p.13 · Fig. 5 · [판독] |
| ⑤ ★ 구 성능 + 물체 · 배경 평균 | 이진 구 = 중심이 반지름 안인 복셀 전부 · 중심은 가운데 복셀 안 균일 · 반지름마다 100 개 · 물체만: Error = −4.116(Radius) + 2.610 Δ² (r² 0.99980 · Fig. 6) · 평균 뒤: **상수 0.527Δ²** (Fig. 7(a)) · 다른 두 가중 (공간 격자 · 불편 표본 세기) 은 상수 **−1.06Δ²** · **−0.457Δ²** · *"the percentage error decreases with (radius)^−2"* · CV = 12.539(Radius)^−1.578 % (r² 0.933 · Fig. 7(b) · Table 2) · [판독] 반지름 ≈3–40 Δ · 간격 ≈0.31 Δ | [인쇄] p.11–13 · Fig. 6–7 · Table 1–2 · [판독] |
| ⑥ 다른 방법과의 비교 | **표본 세기** (모든 표면 복셀 = 1): 넓이 **16.8 % 과소** → 불편이려면 복셀마다 **≈1.2031** · **공간 격자** (W 2/3 · 4/3 · 2): β = 0 · σ ≈ **0.10163** · 팽창 / 침식 구조 원소 (Table 3): 14 면체 σ 0.04372 · 육팔면체 0.06202 · 마름모 12 면체 0.07527 · 8 면체 (= 표본 세기) 0.12037 · 결론 *"The accuracy is over four times better than that of the spatial grid method"* (0.10163/0.0233 = 4.36 [카드 산술]) | [인쇄] p.11 · p.13–16 · Table 3 |
| ⑦ ★ 한 방향 평면의 오차 | **원문에 숫자 없음** — 원문은 무작위 방향 평균만 낸다.  [카드 산술] 식 (7c) 로: 격자축에 맞춘 평면 **−10.6 %** (전부 S1 → 0.8940) · 면 대각 −5.2 % · 몸 대각 −8.3 % · 최대 **+2.95 %** (n ≈ (0.868, 0.434, 0.240)) · 노출 면을 그대로 세면 **1 (축) … √3 = 1.732 (몸 대각) · 등방 평균 1.500** (식 8a 의 계수로 1·0.372249 + 2·0.249072 + 3·0.209869 = 1.500000) | [카드 산술] §3-7 |
| ⑧ ★ 원기둥 (의도의 '원기둥 성능') | **없음** — 원기둥 물체의 넓이 시험은 하지 않았다.  이 논문의 원기둥은 평면 시험의 **잣대 창** (반지름 π^−0.5 → 평면과 만나는 넓이 1 단위) 이다 (p.10 · p.11) | [인쇄] p.10–11 |
| ⑨ ★ DEM 한계 · 소성 · 2D / 3D · 탈압 | **말 없음** (입자 · 접촉 · 역학 · 압력 0 회).  2D → 3D 에 대한 말은 넓이 추정기의 것뿐: 2D 원판 둘레의 과소는 반지름과 무관해 상수를 더하면 되지만 (Young 1988) *"For spheres, surface area underestimation is proportional to sphere radius in addition to an overall offset"* (p.11) | [인쇄] p.11 · §4-3 |
| ⑩ 절대값 전이 | 재료와 무관한 **기하 상수** 라 그대로 옮는다 — 단 조건이 붙는다: 이진 (두 상) · 입방 격자 · 6-연결 표면 · 복셀 중심 판정 (구) · **무작위 방향 · 위치** 평균 · 평면 조각은 지름에 표본 ≳20 개 · 구 결과는 반지름 ≈3–40 Δ 범위 | §7-3 |

⛔ **한정어 (떼지 말 것)**: ① 가중은 **무작위 방향 평균에서만 불편** — 방향이 정해진 평면 한 장은 −10.6 … +3.0 % [카드 산술] ② **S4–S6 = 공간 격자 값 차용 (도출 아님) · S7–S9 가중 없음** ③ 닫힌 곡면 (구) 은 **물체 · 배경 평균이 필요** 하고 그래도 **+0.527Δ²** 가 남는다 (빼려면 상수를 뺀다) ④ 평면 CV 는 해상도를 올려도 **2.33 % 아래로 안 간다** (국소 추정기 · 법선 이방성 · p.15) ⑤ 구 시험 범위 r ≈ 3–40 Δ [판독] — 그 밖의 식 (9) · Fig. 6 직선은 외삽 ⑥ 이진 두 상 · 입방 격자 — 세 상 계면 (AM \| SE ↔ AM \| 기공) 나누기 · 비등방 격자 · 오목 · 닿은 두 물체 시험 없음 ⑦ "원기둥 성능" 은 이 논문에 없다.

---

## 0-1. ★ 고른 의도 대조 (후보 표 N-75 의 '왜' 칸)

의도 원문: *"단계 7 (형상 · 피복 넓이 진단) — 복셀 면 면적 S1–S6 가중치 (0.894 · 1.3409 · 1.5879 …) 의 도출 · 구 · 원기둥 성능 · 물체/배경 평균 처방의 원전 · windreich2003 "원문 카드 없음 → 그 값들은 이 논문이 인용한 내용" · "원전 PDF 미확인""* (가리킨 카드 = windreich2003 L34 · L174 · L191) · 덧붙임 지시: *"가중치 값이 원문 어디에 · 어떤 최적화 (치우침 0 · 평균 제곱 오차 최소) 로 나오는지"* · *"표면 복셀 정의 (6-연결) · 노출 면 1 · 2 · 3 개 유형 · 치우침 / 평균 제곱 오차 식"* · *"적용 조건 (평면 · 무작위 방향) 과 한계"*.

| 의도의 문장 | 판정 | 원문 위치 · 값 · 조건 |
|---|---|---|
| "단계 7 (형상 · 피복 넓이 진단)" | **채움** (측정 도구로서) | 이진 영상 넓이 추정기의 정의 · 치우침 · 정밀도 · 다른 추정기 대비 (p.6–16).  조건 = 압력 · 온도 해당 없음 (기하 시험) · 재료 없음 |
| "복셀 면 면적 S1 … 가중치 (0.894 · 1.3409 · 1.5879) 의 도출" | **채움** | **식 (7a)** β = (12/π)∬ sin θ (Â − 1) dθ dφ = 0 (치우침 0 제약) · **식 (7b)** σ² = (12/π)∬ sin θ (Â − 1)² dθ dφ (최소화) · **식 (7c)** Â(n) · 수치 해 **식 (8a)** β = 0.372249 W₁ + 0.249072 W₂ + 0.209869 W₃ − 1 · **식 (8b)** σ² 의 이차식 (계수 9 개) → 값 **p.10** *"W₁ ≈ 0.8940, W₂ ≈ 1.3409 and W₃ ≈ 1.5879 in sample-grid units squared with a coefficient of variation (CV = σ/µ) of 2.33%"* (초록 p.6 에도) · 표에는 없다 (본문 · 초록) · 원 표 = Verwer (1991) table 6 (이 논문 밖) · [카드 산술] 식 (7) 을 다시 적분해 (8a)(8b) 계수 15 개를 인쇄 자리수까지 재현 · 제약 최소의 닫힌 해 W = M⁻¹μ/(μᵀM⁻¹μ) = (0.8940, 1.3409, 1.5879) · σ = 0.023252 |
| "… S4–S6 가중치 … 의 도출" | **없음** | S4–S6 은 도출하지 않았다 — *"For the simulations using the optimal weights, we set weights for surface voxel types S4–6 to W4 = 2, W5 = 8/3 and W6 = 10/3, which are the equivalent spatial grid weights"* (p.11) · 근거 = 구에서 드묾 (Table 1) |
| "구 … 성능" | **채움** | Table 1 (r 5 · 7 · 15 · 25 · 50 의 부류 몫 · 100 개) · Fig. 6 (물체만 · −4.116 r + 2.610 Δ² · 100 개) · Fig. 7(a) (평균 뒤 상수 0.527Δ²) · Fig. 7(b) · Table 2 (CV = b r^a) · 디지털화 = *"the set of all voxels whose centres are within a given radius to a point"* · 중심 = 가운데 복셀 안 균일 (p.11) · [판독] 반지름 ≈3.1–40 Δ · 간격 ≈0.31 Δ (Fig. 7(a) 표지 ≈120 개) |
| "… 원기둥 성능" | **없음** | 원기둥 물체 시험이 없다.  원기둥 = 평면 시험의 창: *"A solid cylinder of radius r = π^−0.5 (units) is oriented axially parallel to the plane normal … The surface area of the plane–cylinder intersection is one square unit"* (p.10) · 그 성능 = **평면** 성능 (Fig. 5 · x 축 *"Samples Across Cylinder Diameter"*) |
| "물체/배경 평균 처방의 원전" | **채움** | p.11: *"To counteract this underestimation in curved regions, the surface area of the object is averaged with the surface area of the background voxels which are 6-connected to the object. This operation does not influence the optimal weights determined for S1–3 due to the symmetry of object and background voxels with respect to a planar boundary."* · 효과: *"removes the linear part of the underestimation and leaves only a constant bias"* · 상수 **0.527Δ²** · 이유: *"the actual boundary lies somewhere between the object and the background"* · 처방 반복 p.15–16: *"We suggest that the averaging procedure be followed when estimating the area of curved surfaces. If the object boundary is closed a constant should be added"* (Fig. 7 캡션: *"could be removed by subtracting the measured bias"*) |
| windreich2003 "원문 카드 없음 → 그 값들은 이 논문이 인용한 내용" · "원전 PDF 미확인" | **채움** (이번에 확인) | 아래 2 차 인용 표 — 값은 같고, S4–S6 이 도출이 아닌 점과 원기둥 시험이 없는 점만 다르다 |
| (덧붙임) "표면 복셀 정의 (6-연결) · 노출 면 1 · 2 · 3 개 유형" | **채움** | 초록 p.6 · p.8 (*"Let us define border voxels as the set of object voxels which are six-connected to non-object voxels"* · S1 · S2 · S3 · *"By 'adjacent' we mean that opposite sides of a surface voxel are not exposed to background voxels"*) · Fig. 1(b) (1 · 2 · 3 표시) · Fig. 2 |
| (덧붙임) "적용 조건 (평면 · 무작위 방향) 과 한계" | **채움** (조건) · **일부** (한계) | 조건: 입방 격자 · Nyquist 를 만족하는 표본 간격 (p.7) · 법선 균일 · 교점 균일 (p.9) · 평면 = 최악 대상 (p.8) · 평면 CV 바닥 (p.15) · 구는 평균 필요 (p.11) / 한계 중 방향별 오차 크기 · 세 상 · 오목 · 닿은 물체는 원문에 없다 ([카드 산술] §3-7 · §7-3) |

**가리킨 카드 · 같은 값을 쓴 카드의 2 차 인용 대조** (카드 줄은 고치지 않는다 — 다른 점은 카드 문제로 보고 · 줄 번호 = 이 카드가 두 카드 머리에 '관련 카드' 한 줄을 더하기 **전** 기준 (후보 표의 L34 · L174 · L191 과 같은 기준 · 지금은 +1)):

| 카드 (줄) | 옮긴 값 · 표기 | 원문 | 판정 |
|---|---|---|---|
| `windreich2003_…` L34 | *"[9] Mullikin & Verbeek 1993 (Bioimaging 1, 6–16) — S1–S3 가중치 · [19] Hahn & Sandau 1989 (spatial grid) — S4–S6 가중치"* · "원문 카드 없음" | Bioimaging 1 (1993) 6–16 ✓ · S1–S3 = 이 논문 도출 ✓ · S4–S6 = *"equivalent spatial grid weights"* (p.11) — 공간 격자 = Hahn and Sandau (1989) · Howard and Sandau (1992) 의 방법 (p.6–7) ✓ | **채움** |
| `windreich2003_…` L42–44 | S1 **0.894** · S2 **1.3409** · S3 **1.5879** | 0.8940 · 1.3409 · 1.5879 (p.6 · p.10) | **채움** (W₁ 끝자리 0 생략) |
| `windreich2003_…` L45–47 | S4 2 · S5 8/3 · S6 10/3 *"spatial grid [19] 를 [9] 가 채택"* · S4 *"(곡면 · 3 면 — 본문은 배치를 말로 적지 않음)"* | W4 = 2 · W5 = 8/3 · W6 = 10/3 (p.11) · S4–6 *"occur in curved border regions"* (p.8) · 배치는 Fig. 2 그림뿐 | **채움** · [카드 산술] S4 = 노출 3 면 (마주 보는 한 쌍 포함) — 6 면 조합 셈 (§3-1) + 공간 격자 가중 = 노출 면 수 × 2/3 |
| `windreich2003_…` L48–50 | S7–S9 = 그 논문 제안 (1.79 · 2.68 · 4.08) · S8 본문 *"adjacent"* ↔ 캡션 *"opposite"* | 이 논문: S7–9 = *"pathological situations where the object is a plane, line or point"* (p.8) · 가중 없음 · S8 = 선 (Fig. 2: 위 · 아래 이웃만) → 노출 4 면 = **마주 보는 두 쌍** [카드 산술] | **채움** — 이 논문은 Windreich 캡션 (*"opposite"*) 쪽과 같다 (그 카드가 적은 Windreich 본문의 어긋남은 그대로) |
| `windreich2003_…` L52 | *"무작위 방향 평면에 대해 불편 · MSE 최소 · 평면 CV 2.33 %"* · *"평면 = 최악 경우"* | 식 (7a)(7b) · CV 2.33 % (p.10) · *"worst-case objects"* (p.8) · *"a difficult object class"* (p.15) | **채움** |
| `windreich2003_…` L53 | [derived] 축 정렬 평면 **−10.6 %** · 방향별 최대 오차는 논문에 없음 | 이 논문에도 숫자 없음 · 식 (7c) [카드 산술] −10.6 % (축) … **+2.95 %** | **같은 값** (방향 범위를 이 카드가 채움) |
| `windreich2003_…` L56 | 반경 5–50 의 디지털 구: S4 없음 · S6 매우 드묾 · S5 **5.5 % (r 5) → 0.82 % (r 15)** · 물체 · 배경 평균으로 크게 줄어든다 | Table 1: S4 = 0 (다섯 반지름 모두) · S6 0.14 · 0.088 · 0 · 0 · 0 · S5 5.50 · 1.68 · 0.820 · 0.285 · 0.107 % · 평균 = 선형 부분 제거 + 상수 0.527Δ² 남음 | **채움** ("크게 줄어든다" = 원문은 "선형 부분이 없어지고 상수가 남는다") |
| `windreich2003_…` L101 | 물체 · 배경 평균 = 물체와 **여집합** 의 추정 넓이 평균 · 전경/배경 비대칭 반경 의존 편향을 줄임 | 원문 = 물체에 **6-연결된 배경 복셀** 의 넓이 (= 여집합의 표면 복셀) 와 평균 (p.11 · Fig. 7 캡션) · 이유 = 실제 경계가 물체와 배경 사이에 있음 | **채움** |
| `windreich2003_…` L169 | 인용 문장 *"Mullikin–Verbeek weights 0.894 / 1.3409 / 1.5879"* | ✓ | **채움** |
| `windreich2003_…` L174 | *"S1–S6 가중치는 원저자 [9] … 의 값을 이 논문이 인용한 것 — 원전 PDF 미확인"* | S1–S3 = 이 논문 도출 · S4–S6 = 이 논문이 **시뮬레이션에 쓴** 공간 격자 값 (도출 아님) | **일부** — "원전 미확인" 은 이제 풀림 · S4–S6 의 지위는 '원저자의 값' 이되 '도출된 값' 은 아님 |
| `windreich2003_…` L191 | n/a 목록 *"Mullikin & Verbeek 1993 원문 (S1–S6 가중치 도출 · 구·원기둥 성능)"* | S4–S6 도출 없음 · **원기둥 성능 없음** (원기둥 = 평면 시험 창) | **카드 문제 (경미)** — 기대한 내용 둘이 원문에 없다 |
| `windreich2003_…` L62–L65 (그 논문 Fig. 6 · 7 판독 — MV 가중 + 평균 적용 결과) | 구 평균 상대오차 r 2 **+0.97 %** · r 3 +0.46 % · r 4 +0.25 % · r 5 +0.13 % · CV ≈4 % (r 2) → 0.5 % (r 5) | 이 논문 상수 0.527Δ² 로 +0.527/(4πr²) = **+1.05 · +0.47 · +0.26 · +0.17 %** · 식 (9) CV = **4.20 % (r 2) · 0.99 % (r 5)** [카드 산술 · r 2 는 이 논문 그림 범위 밖] | 편향은 **같은 크기** · CV 는 r 2 같고 r 5 에서 Windreich 가 절반 (그쪽 50 개 · 이쪽 100 개 · 식 (9) r² 0.933) |
| `lindblad2005_…` L30 · L40 | *"[8] Mullikin & Verbeek 1993 (6-이웃 9 부류)"* · W₁ 0.8940 · W₂ 1.3409 · W₃ 1.5879 · 평면 CV 2.33 % · 전경/배경 비대칭 → 여집합과 평균 권고 | ✓ (Fig. 2 · p.10 · p.11 · p.15–16) | **채움** |
| `lindblad2005_…` L39 | 배경 이웃 전경 voxel 세기 *"quite severe underestimation"* · voxel 당 **1.2031** 이면 등방 평면 불편 [8] · 분산 큼 | 표본 세기 **16.8 % 과소** · *"each surface voxel should be assigned ≈1.2031 square units"* (p.11) · 불편 표본 세기의 평면 σ = **0.12037** (= Table 3 의 8 면체 행 · *"The sample-count method is analysed similarly using the octahedron"* p.15) | **채움** ("quite severe" 는 Lindblad 의 말) |
| `lindblad2005_…` §7-3 표 A "MV 물체" 열 (pilot · scratch) | r/h 2.5 · 3.33 · 5 · 6.67 · 10 · 13.3 · 20 · 40 → 0.906 · 0.924 · 0.943 · 0.956 · 0.969 · 0.977 · 0.984 · 0.992 | 이 논문 Fig. 6 직선 1 + (−4.116 r + 2.610)/(4πr²) = 0.902 · 0.920 · 0.943 · 0.956 · 0.969 · 0.977 · 0.984 · 0.992 [카드 산술] | **같다** (r/h ≥ 5 에서 0.0005 안) — 그 pilot 의 MV 구현이 원문 직선을 재현한다 (그 카드는 pilot 을 "인용 전 재현" 으로 묶어 두었다 — 그 한정은 그대로) |
| `lindblad2005_…` §7-3 표 A "면 세기" 열 (pilot) | 1.453 (1.67) · 1.484 (2.5) · 1.497 (3.33) · 1.494 (5) · 1.500 (10) · 1.4997 (40) | 이 논문 공간 격자 상수 −1.06Δ² + 공간 격자 = 노출 면 수 × 2/3 → 면 세기 / 참 = **1.5 × (1 − 1.06/(4πr²))** = 1.455 · 1.480 · 1.489 · 1.495 · 1.499 · 1.4999 [카드 산술] | **같은 크기** (pilot sd 안) — "구 면 세기 → 1.5" 에 원문 근거가 하나 더 생겼다 (그 카드는 식 18 + 우리 산수로만 세웠다) |
| 비교 문서 `comparison_vs_ours_DEM.md` [Windreich03] 블록 | *"⚠ … S1–S6 가중은 원전 미확인 (MV 1993 카드 없음)"* | 이 카드로 확인 (위) | **낡은 줄** — 같은 절에 이 카드 블록을 더했다 (그 줄은 고치지 않음) |

⇒ **의도 대조 결과: 일부** — S1–S3 가중의 도출 (식 7–8 · 치우침 0 + MSE 최소) · 구 성능 (Table 1 · Fig. 6–7 · Table 2) · 물체 / 배경 평균 처방 (p.11 · p.15–16) · 2 차 인용 값은 **채움**; **S4–S6 의 도출은 없음** (공간 격자 값 차용) · **원기둥 성능은 없음** (원기둥 = 평면 시험 창).

---

## 1. 한 줄 요약
2D 에서 곧은 선의 길이를 사슬 부호 가중으로 재듯, 3D 이진 영상의 넓이를 **표면 복셀 하나하나의 6-이웃 노출 배치** 에 가중을 주어 더해서 재는 방법을 세웠다.
평면에 나타나는 세 부류의 가중을 **무작위 방향 · 위치의 평면에서 불편 + 최소 MSE** 로 해석적으로 정하니 (0.8940 · 1.3409 · 1.5879) 평면 CV 가 2.33 % 로, 공간 격자 (0.10163) 보다 4 배 넘게 정밀하고 팽창 / 침식 구조 원소 넷보다도 낫다 (Table 3) — 표본 세기 (복셀 하나 = 1) 는 16.8 % 과소다.
곡면 (이진 구) 에서는 물체만 세면 반지름에 비례해 과소이므로 배경 표면 넓이와 평균해 선형 부분을 없애고 상수 0.527Δ² 를 남긴다 (닫힌 경계는 상수를 보정).

## 2. 메타
| 저자 | 저널/년 | DOI | 대상 | 연구유형 |
|---|---|---|---|---|
| James C **Mullikin** · Piet W **Verbeek** (Pattern Recognition Group, TU Delft) | *Bioimaging* 1 (1993) 6–16 (1 호 · IOP Publishing · 접수 1992-10-21) | 10.1002/1361-6374(199303)1:1<6::AID-BIO3>3.0.CO;2-3 (내려받기 표지) | 이진 3D 영상 (CT · MRI · 광학 절편 · 공초점 현미경 — p.7) · 합성 평면 · 이진 구 | 이론 (해석 적분 + 수치 해) + 몬테카를로 시험 · 계산 · 재료 실험 없음 |

- **1저자 메모 (지시서) 와의 대조**: 저자 (J. C. Mullikin · P. W. Verbeek) · 제목 · 학술지 · 권 1 · 쪽 6–16 · 1993 · 접수일 · 11 쪽 — **같다**.  덧붙임 ① 이름 = James C · Piet W (첫 쪽) ② 호 = 1 (내려받기 표지 *"1993, 1"* · DOI 의 *"(199303)1:1"*) ③ DOI 는 1993 인쇄면에 없고 내려받기 표지에만 ④ 출판 = IOP Publishing Ltd (쪽 아래 저작권 줄).  후보 표 행의 *"Bioimaging 1, 6–16"* 과도 같다.
- **글의 꼴**: 1 Introduction (p.6–7) → 2 Surface description (p.7–8) → 3 Surface area estimation (p.8–11) → 4 Simulation methods and results (p.11–13) → 5 Discussion (p.13–16) → 6 Conclusions (p.16) → 감사 → 참고문헌 23 (p.16).  그림 8 · 표 3 · 번호 식 9 묶음 + 번호 없는 식 3 · SI 없음.
- **같은 그룹의 줄기**: 2D 직선 길이 추정 (Groen and Verbeek 1978 · Vossepoel and Smeulders 1982 · Dorst and Smeulders 1987 · Beckers and Smeulders 1989, 1992) · 3D chamfer 거리 (Verwer 1991 — 같은 식 · Mathematica 스크립트 제공).

---

## 3. 핵심 수치 (★ 전부 쪽 · 표지 병기)

### 3-1. ★ 표면 복셀 정의와 9 부류 (p.6 · p.8 · Fig. 1–2 · `txt_p6_title_abstract_definition_weights.png` · `txt_p8_border_voxel_definition_s1_s3.png` · `txt_p8_nine_types_63_configurations.png`)
- 정의: *"Let us define border voxels as the set of object voxels which are six-connected to non-object voxels"* (p.8) — 초록은 같은 집합을 *"surface voxels"* 라 부른다 (원문이 두 이름을 섞어 쓴다).  2D 짝 = Freeman 사슬 부호의 경계 (*"object pixels which are four-connected to non-object pixels"*, 8-연결 경로 · p.7).
- S1 · S2 · S3 = 노출 면 1 · 2 · 3 개 · *"By 'adjacent' we mean that opposite sides of a surface voxel are not exposed to background voxels"* · 평면에는 이 셋만 — 마주 보는 두 면이 노출되면 *"the middle point of three collinear points are on opposite sides of a plane"* 이라 모순 (p.8).
- 그 밖의 여섯: *"six other unique surface voxel types which occur in curved regions or in pathological situations"* · Fig. 2 = 가운데 복셀 (검은 점) + 이웃 정육면체 · 27-이웃의 6-연결 아닌 이웃은 *"'don't-care' voxels"* · 둘째 줄 S4–6 = 곡면 · 셋째 줄 S7–9 = 물체가 판 · 선 · 점 (p.8).
- 각주: *"Given six-connectedness, one could think of 63 surface voxel configurations. Through rotation of the nine types shown, all 63 configurations are accounted for."* (p.8).

[카드 산술] 노출 면 조합 (6 면 중 k 개 · 그중 마주 보는 쌍 m 개) 으로 63 = 2⁶ − 1 을 나누면 아홉 부류가 정확히 나온다 (Fig. 2 와 공간 격자 가중 = 노출 면 × 2/3 에 맞춤):

| 부류 | 노출 면 | 배치 | 배치 수 | 원문 가중 | 공간 격자 가중 |
|---|---|---|---|---|---|
| S1 | 1 | — | 6 | **0.8940** (최적) | 2/3 |
| S2 | 2 | 이웃한 두 면 | 12 | **1.3409** (최적) | 4/3 |
| S3 | 3 | 서로 이웃한 세 면 (모서리) | 8 | **1.5879** (최적) | 2 |
| S4 | 3 | 마주 보는 한 쌍 + 한 면 (홈 · 등) | 12 | 2 (= 공간 격자) | 2 |
| S5 | 4 | 마주 보는 한 쌍 + 이웃 둘 | 12 | 8/3 (= 공간 격자) | 8/3 |
| S6 | 5 | 이웃 하나만 | 6 | 10/3 (= 공간 격자) | 10/3 |
| S7 | 2 | 마주 보는 두 면 (판) | 3 | 없음 | (4/3) |
| S8 | 4 | 마주 보는 두 쌍 (선) | 3 | 없음 | (8/3) |
| S9 | 6 | 고립 (점) | 1 | 없음 | (4) |

(마지막 열의 괄호 = 같은 규칙을 S7–S9 에 연장한 값 [카드 산술] — 원문에 없다.  배치 수 합 6 + 12 + 8 + 12 + 12 + 6 + 3 + 3 + 1 = 63.)

### 3-2. ★ 최적화 문제 — 식 (1)–(7) (p.9–10 · Fig. 3–4 · `eq_01…` – `eq_07c…` · `txt_p9_restricted_normals_uniform_assumptions.png` · `txt_p10_cylinder_unit_area_type_counts.png`)
1. **법선 영역 줄이기** (식 1): *"restrict the analysis to the set of planar objects with unique normals containing no symmetrical duplicates"* (축 바꾸기 · 뒤집기) → 0 ≤ φ ≤ π/4 (1a) · π/2 − cos⁻¹(1/√(1 + sin²φ)) ≤ θ(φ) ≤ π/2 (1b) · n = (cos φ sin θ, sin φ sin θ, cos θ) (1c).  Fig. 3 캡션: *"Forty-eight of these patches completely cover the sphere through rotation and mirroring"* → 조각 넓이 π/12 (식 7 의 12/π) [카드 산술: 4π/48].  이 영역은 n_x ≥ n_y ≥ n_z ≥ 0 과 같다 [카드 산술].
2. **가정** (p.9): P (원점) 는 표면 복셀 · *"the probability of the boundary plane normal is uniformly distributed over the restricted area"* · *"the probability of the line-plane intersection point is uniformly distributed over the line segment PA"* · A (1,0,0) · B (0,1,0) · C (0,0,1).
3. **노출 조건** (식 2): A ∉ O if PA·n ≥ d ⇒ cos φ sin θ ≥ d (2b) · B ∉ O … sin φ sin θ ≥ d (2c) · C ∉ O … cos θ ≥ d (2d) · d = 평면에서 P 까지 거리 · O = 물체 복셀 집합.
4. **노출 확률** (식 3, Fig. 4): Pr(F_A) = 1 · Pr(F_B) = sin φ sin θ / cos φ sin θ = tan φ (3a) · Pr(F_C) = cos θ / (cos φ sin θ) (3b) — d 가 (0, cos φ sin θ] 에 균일.  원문 문장 *"some planes will fall within both hatches regions, H1 and H1"* = 둘째 H1 은 H2 의 오식 [카드 해석].
5. **부류 확률** (식 4): *"C ∈ O if B ∈ O and B ∈ O if A ∈ O"* 이라 Pr(S1) = 1 − tan φ (4a) · Pr(S2) = tan φ − cos θ/(cos φ sin θ) (4b) · Pr(S3) = cos θ/(cos φ sin θ) (4c).
6. **넓이 1 단위 평면 조각** (식 5–6): 반공간 V_i ∈ O ⇔ V_i·n ≤ 0 (5a · 5b) · 반지름 r = π^−0.5 의 원기둥 (축 ∥ 법선) · 간격 Δ ≪ 1 → 0 · Â = Σ_{i=1}^{3} Δ² W_i N_i (6a) · N_B = Δ⁻²(n·(1,0,0)) = Δ⁻² cos φ sin θ (6b · Y–Z 평면 사영) · N_i = N_B Pr(S_i) (6c) · N1 = Δ⁻²(cos φ sin θ − sin φ sin θ) (6d) · N2 = Δ⁻²(sin φ sin θ − cos θ) (6e) · N3 = Δ⁻² cos θ (6f) · *"The projection and normalization to the number of border voxels is valid because of the restricted set of surface normals"* (p.10).
7. **치우침 · MSE** (식 7): β = (12/π) ∬ sin θ (Â − 1) dθ dφ = 0 (7a) · σ² = (12/π) ∬ sin θ (Â − 1)² dθ dφ (7b) · Â = W₁(cos φ sin θ − sin φ sin θ) + W₂(sin φ sin θ − cos θ) + W₃ cos θ (7c).
8. **chamfer 거리와 같은 식**: *"These equations turn out to be identical to those previously derived for basis vector lengths of the 3 × 3 × 3 three-dimensional chamfer-distance transform (Verwer 1991). These expressions were computed numerically (Wolfram 1988) to find the vector lengths which minimize (7b). The optimal, i.e. unbiased and minimum MSE based, real-valued distances are the same values for the surface area weights."* (p.10).

[카드 해석] 식 (6b) 의 N_B 는 n 의 **가장 큰 성분** (= L∞ 노름) — 한 표면 복셀이 축 하나의 기둥에 하나씩 있다는 뜻 · N1 + 2N2 + 3N3 = Δ⁻²(n_x + n_y + n_z) = **노출 면 수 = L1 노름** (`lindblad2005_…` §3-3 의 식 18 관계와 같은 양).

### 3-3. ★ 결과 — 식 (8a)(8b) 와 가중 (p.10 · `eq_08a…` · `eq_08b…` · `txt_p10_chamfer_identity_numerical_solution.png` · `txt_p10_optimal_weights_cv_233.png`)
- **식 (8a)**: β = 0.372249 W₁ + 0.249072 W₂ + 0.209869 W₃ − 1 [인쇄].
- **식 (8b)**: σ² = [1 − 0.744497 W₁ + 0.200629 W₁² − 0.498144 W₂ + 0.142699 W₁W₂ + 0.0914020 W₂² − 0.419739 W₃ + 0.122710 W₁W₃ + 0.0791798 W₂W₃ + 0.0642662 W₃²] [인쇄].
- **가중**: *"If (7a) is satisfied, surface area estimation of planar regions is unbiased. If (7b) is minimized with the constraint of (7a), optimal weights are found which, in addition to being unbiased, also give minimum MSE. Performing these operations, the optimal weights are: W₁ ≈ 0.8940, W₂ ≈ 1.3409 and W₃ ≈ 1.5879 in sample-grid units squared with a coefficient of variation (CV = σ/µ) of 2.33%."* (p.10).
- [카드 산술 · 재현] 식 (7a)(7b) 를 영역 (1a)(1b) 위에서 가우스–르장드르 400 × 400 으로 다시 적분: 조각 넓이 π/12 (4π / 0.2618 = 48.000) · (8a) 계수 0.372249 · 0.249072 · 0.209869 · (8b) 계수 0.744497 · 0.498144 · 0.419739 · 0.2006286 · 0.1426992 · 0.0914020 · 0.1227101 · 0.0791798 · 0.0642662 — **인쇄 자리수까지 같다**.  Â 가 W 에 선형이라 β = 0 아래 최소 σ² 의 닫힌 해 W = M⁻¹μ/(μᵀM⁻¹μ) → **(0.8940, 1.3409, 1.5879)** · σ = **0.023252** (CV 2.33 %) ✓ · 인쇄 반올림 W 를 넣으면 β = +2.2 × 10⁻⁵.
- [카드 산술] 계수의 뜻: μ₁ + μ₂ + μ₃ = **0.831190** = 등방 평면에서 넓이당 **표면 복셀 수** (L∞ 평균) · μ₁ + 2μ₂ + 3μ₃ = **1.500000** = 넓이당 **노출 면 수** (L1 평균).

**가중 묶음별 비교 (평면 · 무작위 방향 · 위치)**:

| 가중 (S1 · S2 · S3) | 뜻 | β (평균 치우침) | σ (= CV) | 표지 |
|---|---|---|---|---|
| **최적 (0.8940 · 1.3409 · 1.5879)** | 이 논문 | 0 | **0.0233** | [인쇄] p.10 |
| 공간 격자 (2/3 · 4/3 · 2) | 노출 면 수 × 2/3 | 0 | **0.10163** (≅ 0.102) | [인쇄] p.11 · p.13 |
| 표본 세기 (1 · 1 · 1) | 표면 복셀 하나 = 1 | **−0.1688** (16.8 % 과소) | 0.1962 (치우친 채) | [인쇄] p.11 · [카드 산술] σ |
| 불편 표본 세기 (1.2031 · 1.2031 · 1.2031) | 위를 1/0.83119 로 | 0 | **0.12037** | [인쇄] p.11 (1.2031) · Table 3 8 면체 · [카드 산술] 재현 |
| 노출 면 그대로 (1 · 2 · 3) | 면 하나 = Δ² | **+0.500** (평균 1.5 배) | 0.5227 (치우친 채) / 0.10163 (1.5 로 나누면) | [카드 산술] 식 (8a)(8b) |

- [카드 산술] 공간 격자의 σ 는 원문 Hahn–Sandau 상한 √((4/9)(1 + 4/π) − 1) = **0.101630** 과 같고 (p.13 *"The upper bound of this equation is the analytic result of (7b)"*), 그 식의 (1 + 4/π) = 2.2732 = 등방 법선의 E[(L1)²] 이다.  ⇒ **"면 세기는 등방 평균 1.5 배 · 방향에 따라 ±10 %대 흩어짐"** 이 이 논문 식 (8a)(8b) 와 공간 격자 문장에서 바로 나온다.

### 3-4. ★ 평면 시뮬레이션 (p.11 · p.13 · Fig. 5 · `fig_5.png` · `fig_5a.png` · `fig_5b.png` · `txt_p11_planar_simulation_spatial_grid.png` · `txt_p13_discussion_planar_simulation_confirms.png`)
- 방법: 식 (5a)(5b) 로 평면을 디지털화 · 원기둥 (r = π^−0.5) 안의 표면 복셀을 세어 (6a) · *"translating the object-space origin to some uniformly distributed point within a centrally located voxel of the sample space"* · 간격마다 N 회 (그림: **N = 10⁴**) · x 축 = *"samples across the diameter of the cylinder"* (지름 2/√π = 1.128 단위 [카드 산술]) · 점선 = *"95% confidence limits for the mean of 10000 trials assuming a standard deviation of 0.0233"* (p.11).
- 결과 (원문): *"nearly all data plotted in figure 5(a) fall within the 95% confidence limits … The two data points at the lowest sample densities fall outside the 95% confidence limits because the actual σ is much greater due to the low sample densities"* · σ 는 해상도와 함께 이론 바닥 (최적 0.0233) 으로 · 공간 격자 시험값 = Hahn and Sandau (1989) 식 (6) 과 맞음 (p.13).
- [판독 Fig. 5(a) · 50 점] 표본 0.79–99.5 · 점선 ±0.000457 (= 1.96 × 0.0233/100 [카드 산술]) 밖 = 4 점: **0.79 (−0.00109) · 3.42 (−0.00260)** (원문이 말한 둘) + 21.3 (−0.00052) · 92.6 (+0.00052) (50 점 중 둘 = 95 % 한계에서 기대되는 수 [카드 해석]) · 표본 > 5 의 평균 +2.4 × 10⁻⁵ · 표준편차 **2.33 × 10⁻⁴** = 0.0233/√10⁴ 그대로 [판독 + 카드 산술] → 불편 확인.
- [판독 Fig. 5(b) · 로그 축 · 네모 = 공간 격자 · 세모 = 최적] 표본 0.78: 1.33 · 1.19 / 3.3: 0.171 · 0.122 / 5.4: 0.120 · **0.0615** / 6.9: 0.1105 · 0.0504 / 9.1: 0.105 · 0.0373 / 10.1: 0.104 · **0.0329** / 13.2: 0.103 · 0.0281 / 16.8: 0.103 (점선 위) · 0.0261 / **18.5: 0.098 (점선 위) · 0.0251** / 21.4: — · 0.0244 / 25–56: — · 0.0237–0.0239 (점선 위) · 공간 격자는 ≈10 표본에서 바닥 +3 % 안.
- [카드 산술 · 두 성분이 독립이라고 보고] σ² = σ_방향² + σ_위치² 로 나누면 위치 성분은 두 가중에서 **거의 같다**: 5.4 표본 0.057 · 0.063 / 9.1 0.029 · 0.026 / 13.2 0.016 · 0.016 · 감소 ≈ (표본)^−1.4 — 최적 가중은 바닥이 낮아서 **바닥에 닿는 데 표본이 더 필요할 뿐** 이다.

### 3-5. ★ 이진 구 — Table 1 · Fig. 6 · Fig. 7 · Table 2 (p.11–13 · `tab_1.png` · `fig_6.png` · `fig_7*.png` · `tab_2.png` · `eq_09_cv_power_law.png` · `txt_p11_binary_sphere_definition_random_centre.png` · `txt_p11_s4_s6_spatial_grid_weights.png` · `txt_p11_p12_object_background_averaging_offsets.png`)
- 디지털화 · 표본: *"A binary sphere is the set of all voxels whose centres are within a given radius to a point in three-space"* · 중심 = *"uniformly distributed within a centrally located voxel in the simulation space"* · 반지름마다 N 개 (그림 N = 100 · Table 1 은 100 개) · 간격 Δ 고정 (p.11).
- **Table 1** (부류 몫 %, 100 개 평균) [인쇄]:

| 반지름 (Δ) | S1–3 | S4 | S5 | S6 | [카드 산술] S4–6 합 |
|---|---|---|---|---|---|
| 5 | 94.36 | 0 | 5.50 | 0.14 | 5.64 |
| 7 | 98.23 | 0 | 1.68 | 0.088 | 1.77 |
| 15 | 99.18 | 0 | 0.820 | 0 | 0.82 |
| 25 | 99.715 | 0 | 0.285 | 0 | 0.285 |
| 50 | 99.893 | 0 | 0.107 | 0 | 0.107 |

  (행 합 100 · 7 행만 99.998 — 반올림.  S4 는 볼록한 구에 한 번도 안 나온다.)
- **물체만 (Fig. 6)**: *"surface area is underestimated. This occurs because the actual boundary lies somewhere between the object and the background"* · *"For spheres, surface area underestimation is proportional to sphere radius in addition to an overall offset"* · 그림 글자 **Error = −4.116(Radius) + 2.610 · r² = 0.99980** (Δ² · N = 100) [인쇄] · [판독] 원 표지 사슬 ≈3.0 (−9.9) … 39.8 (−160) Δ — 직선과 맞음.
  - [카드 산술] 상대 오차 = (−4.116 r + 2.610)/(4πr²): r 3.33 −7.96 % · 5 −5.72 % · 6.67 −4.44 % · 10 −3.07 % · 20 −1.59 % · 40 −0.81 % · 선형 계수의 뜻 = 표면이 안쪽으로 δ = 4.116/(8π) = **0.164 Δ** 물러난 구의 넓이 (d(4πr²)/dr = 8πr) [카드 해석].
- **물체 · 배경 평균 (Fig. 7(a))**: 평균 뒤 *"leaving an offset of 0.527Δ²"* [인쇄 p.11] · 다른 두 가중: *"spatial-grid weights and unbiased sample-count weights, give similar results as those shown in figure 7(a) with different offsets, −1.06Δ² and −0.457Δ² respectively. Keep in mind that the percentage error decreases with (radius)^−2"* (p.12) · 공간 격자는 평균이 필요 없다: *"because the number of object voxel surfaces exposed to background voxels is the same as the number of background voxel surfaces exposed to object voxels"* (p.11–12).
  - [판독 Fig. 7(a) · 표지 ≈120] 반지름 3.1–40 Δ · 간격 ≈0.31 Δ · 오차 −1.11 … +2.46 Δ² · 가중 평균 **0.536** · 표준편차 0.58 · 중앙 0.534 · 그려진 직선 0.507 (r 0.5) → 0.532 (r 20) → 0.548 (r 39.5) Δ² (거의 수평 · 인쇄 0.527 과 같은 크기).
  - [카드 산술] 흩어짐 0.58 Δ² = N = 100 의 표본 평균 잡음 (r 20: CV 0.111 % × 5,027 Δ² / √100 = 0.56) · 상수의 불확도 ≈ ±0.1 Δ² (2 × 0.58/√120).
  - [카드 산술] 평균 뒤 상대 오차 +0.527/(4πr²): r 2 **+1.05 %** · 3.33 +0.38 % · 5 +0.17 % · 10 +0.042 % · 40 +0.003 %.
- **CV (Fig. 7(b) · 식 9 · Table 2)**: CV = b(radius)^a · 최적 **b 12.539 · a −1.578 · r² 0.933** · 공간 격자 14.916 · −1.513 · 0.910 · 표본 세기 12.119 · −1.555 · 0.935 [인쇄] · [판독] 72 덩어리를 다시 맞추면 b 11.85 · a −1.589 · r² 0.94.
  - [카드 산술] 최적 CV: r 2 4.20 % · 3.33 1.88 % · 5 0.99 % · 6.67 0.63 % · 10 0.33 % · 20 0.11 % · 40 0.037 % · r 10 에서 공간 격자 0.46 % · 표본 세기 0.34 % → **등방인 구에서는 최적 가중과 (불편) 표본 세기의 정밀도가 거의 같다** — 최적 가중의 이점은 평면 (방향 오차) 쪽이다 [카드 해석].

### 3-6. 다른 추정기 — 공간 격자 · 팽창 / 침식 (p.13–15 · Table 3 · Fig. 8 · `tab_3.png` · `fig_8.png` · `eq_u1…` · `eq_u2…` · `eq_u3…` · `txt_p13_p14_dilation_erosion_effective_radius.png`)
- 공간 격자: 세 직교 시험선 · 하나만 등방 균일 무작위 (IUR) → 불편 (p.7) · 이 논문 식으로 분석 가능 (가중을 주면) · 평면 σ 상한 √((4/9)(1 + 4/π) − 1) ≅ 0.102 (Hahn and Sandau 1989 식 6 을 넓이 1 로 고친 것 · p.13) · FCC · CC 격자 시험선의 분산 상한은 *"not to be found in Gesbert et al (1990) or Meyer (1992)"*.
- 팽창 / 침식 (Meyer 1992): 구조 원소 = CC 의 마름모 12 면체 · FCC 의 육팔면체 · 14 면체 (*"Presumably"*) · 저자가 합성 평면을 침식해 유효 반지름 ΔR 을 냄 · 대칭 원소 · 평면이면 Â = Δ³N/(ΔR) · 10⁴ 회 · 지름 방향 표본 > 50 · R̂ 의 표준편차 = σ/100 (p.14–15).
- **Table 3** [인쇄]:

| 구조 원소 | 시험 R̂ | 시험 σ̂ | 같은 W_i | 적분 R | 적분 σ |
|---|---|---|---|---|---|
| 14 면체 (tetracaidecahedron) | 2.12 | 0.044 | [2, 3, 3] | 2.121 32 | 0.043 72 |
| 육팔면체 (cuboctahedron) | 1.29 | 0.062 | [1, 2, 2] | 1.290 13 (표에는 *"1.290.13"*) | 0.062 02 |
| 마름모 12 면체 (rhombododecahedron) | 1.73 | 0.075 | † | 1.732 00 | 0.075 27 |
| 8 면체 (octahedron = 표본 세기) | 0.83 | 0.121 | [1, 1, 1] | 0.831 19 | 0.120 37 |

  † *"Cannot be expressed as a set of weights for equations (8a) and (8b). The integration region was divided into three sub-regions, with one limit linearly approximated. The accuracy of the numerical results for the rhombododecahedron may be less than the accuracy indicated."*
  - [카드 산술] 식 (8a)(8b) 에 [2,3,3] · [1,2,2] · [1,1,1] 을 넣고 R 로 나누면 R = 2.121320 · 1.290131 · 0.831190 · σ = 0.043721 · 0.062018 · 0.120368 — 표 · 본문 (단계 C *"σ = 0.062018"*) 과 같다.  마름모 12 면체 R = 1.73200 ≈ √3.
- **연속 영역의 해석 (단계 A–C · Fig. 8)**: 유효 반지름 = *"the average height of the polyhedron centre when rolled over a plane"* · 육팔면체: [(1, 1, 0) − r n]·n = 0 ⇒ r = cos φ sin θ + sin φ sin θ → (7a) 꼴 적분 · (7c) 로 W₁ = 1 · W₂ = 2 · W₃ = 2 → **1.290 13** · (8b) → **σ = 0.062018** · *"The analytical results are in excellent agreement with the simulation results"* (p.15).
- 순위 [카드 산술]: 평면 σ 를 최적 0.0233 에 견주면 14 면체 1.88 배 · 육팔면체 2.66 · 마름모 12 면체 3.23 · 공간 격자 4.36 · 불편 표본 세기 5.17 배.

### 3-7. ★ 한 방향 평면의 오차 — 원문에 없는 범위 (식 7c 로 [카드 산술])
식 (7c) 는 Â(n) = 0.8940 n_x + 0.4469 n_y + 0.2470 n_z (n_x ≥ n_y ≥ n_z ≥ 0) 로 n 에 선형이다 → 구면 조각 위 최댓값 = |c| (n ∥ c) · 최솟값 = 꼭짓점.

| 법선 | 최적 (MV) | 노출 면 그대로 (L1) | 공간 격자 (2/3 · L1) | 표면 복셀 수 (L∞) | 불편 표본 세기 |
|---|---|---|---|---|---|
| 축 (1,0,0) | **0.8940 (−10.6 %)** | 1.000 | 0.667 (−33.3 %) | 1.000 | 1.203 (+20.3 %) |
| (2,1,0)/√5 | 0.9995 (−0.1 %) | 1.342 | 0.894 | 0.894 | 1.076 |
| 면 대각 (1,1,0)/√2 | 0.948 (−5.2 %) | 1.414 | 0.943 (−5.7 %) | 0.707 | 0.851 (−14.9 %) |
| 몸 대각 (1,1,1)/√3 | 0.917 (−8.3 %) | **1.732** | 1.155 (+15.5 %) | 0.577 | 0.695 (−30.5 %) |
| MV 최대 (0.868, 0.434, 0.240) | **1.0295 (+3.0 %)** | 1.542 | 1.028 | 0.868 | 1.045 |
| **등방 평균** | **1.000** | **1.500** | 1.000 | **0.831** | 1.000 |

- ⇒ 원문의 "불편" 은 **방향 평균** 의 성질이다.  방향이 몰린 계면 (축에 맞춘 평판 · 압축축 쪽 모자) 에서는 MV 도 −10.6 … +3.0 %, 면 세기는 1–1.732 배로 **결정론적으로** 틀린다 — 해상도를 올려도 줄지 않는다 (p.15 *"the CV of the estimate asymptotically approaches a given lower bound … a result of the anisotropy of the surface normal"*).

### 3-8. ★ 저자가 적은 한계 · 원문 안 어긋남
1. 표본 간격 조건: *"the volumetric data must be properly sampled. The sample spacing must satisfy the Nyquist criterion with respect to the resolution of the imaging device. Physical sectioning does not necessarily meet this requirement … In this situation, the techniques of stereology must be used."* (p.7)
2. 평면 = 최악: *"optimizing surface area weights for planar objects in 3D presents the estimation method with worst-case objects. The CV of the estimated surface area of any other non-planar, reasonably shaped object should be lower that that of planar objects."* (p.8 · 'that' = 'than' 오식)
3. 평면 CV 바닥 · 구 과소: *"The planar boundary is a difficult object class for the surface area estimator developed in this paper as well as other estimators that start from a binary voxel representation. The estimate of the surface area is unbiased; however, the CV of the estimate asymptotically approaches a given lower bound."* · *"The CV of estimated surface area applied to digital spheres is not lower-bounded for increasing radius, but surface area is underestimated."* (p.15)
4. 성긴 해상도: Fig. 5(a) 의 가장 성긴 두 점은 σ 가 훨씬 커서 95 % 한계 밖 (p.13).
5. 14 면체의 약점: *"its large size, the requirement of converting typical cubic lattice data to the FCC lattice and the condition that the object measured must be somewhat thicker than the structuring element size"* (p.16).
6. **원문 안 어긋남 (카드가 본 것)**: ① *"border voxels"* (p.8 정의) ↔ *"surface voxels"* (초록 · 이후) — 같은 집합 ② *"H1 and H1"* (p.9 · H2 오식) ③ *"this stimulation"* (p.11 · simulation) ④ Table 3 육팔면체 R *"1.290.13"* ↔ 본문 *"1.290 13"* ⑤ Fig. 5(b) 의 *"0.102"* ↔ 본문 σ ≈ 0.10163 (반올림 · Hahn–Sandau 상한 ≅ 0.102) ⑥ 단계 (A) 문장이 *"…a plane touching the structuring"* 에서 끊김 (element 빠짐 · p.15) ⑦ 본문 *"Proffitt and Rosen 1979"* (p.8) ↔ 목록 *"Profitt D and Rosen D 1979"* ⑧ *"should be lower that that"* (p.8).

---

## 4. ★ 방법 — 계산 사슬 · 입자 처리 · 이 묶음의 네 질문

### 4-1. 계산 사슬
2D 사슬 부호 길이 가중 (곧은 선에 맞춤) 의 3D 판을 세운다 → 표면 복셀 = 6-연결 · 노출 배치 9 부류 (63 배치) → 평면에는 S1–S3 만 → 법선을 1/48 조각으로 줄이고 · 법선 · 교점 균일 가정 → 부류 확률 (식 3–4) → 넓이 1 조각의 부류 수 (식 6) → Â(n) (식 7c) → β = 0 아래 σ² 최소 (식 7a · 7b · Mathematica 수치 적분 · Verwer 의 스크립트) → (8a)(8b) → W₁–W₃ → 시험: 평면 (창 원기둥 · 무작위 위치 10⁴ 회 · Fig. 5) · 구 (S4–S6 = 공간 격자 값 · 100 개 · Fig. 6–7 · Table 1–2) · 다른 추정기 (표본 세기 · 공간 격자 · 팽창 / 침식 4 원소 · Table 3 · 해석 단계 A–C).
- **맞춘 값과 맞춘 대상**: 가중 3 개 (W₁–W₃) = 무작위 방향 · 위치 **평면** 에 대한 β = 0 + 최소 σ² · 상수 (0.527Δ² 등) 는 구 시험에서 **잰 값** (평균 뒤 남는 치우침 — 원문은 빼라고 권할 뿐 값을 가중에 넣지 않는다).
- **검증**: 평면 시뮬레이션 ↔ 해석 (Fig. 5 · σ 바닥 · 95 % 한계) · 공간 격자 ↔ Hahn–Sandau 식 · 해석 R · σ ↔ 침식 시뮬레이션 (Table 3).  구 · 다른 물체의 참값 대조는 구뿐 (4πr²).

### 4-2. 입자 처리
- 입자 · 전지 논문이 아니다.  대상은 **연속 곡면 하나를 디지털화한 이진 물체** (평면 · 구) — 생의학 3D 영상 (CT · MRI · 광학 절편 · 공초점) 을 염두 (p.7).
- 디지털화 = **복셀 중심 판정** (평면: V_i·n ≤ 0 · 구: 중심이 반지름 안) — `lindblad2005_…` §7-3 이 읽은 우리 `_ball_cells` 의 `≤` 판정 (Gauss 디지털화) 과 같은 꼴 [카드 해석 · 그 카드의 코드 줄 읽기 (stoic @57f1b2baf 11-03) 경유].
- 우리 대응물: STEP3 래스터의 상 경계 (AM 구 표면 · AM \| SE · ①′ AM–AM 근축면 · 다음 트랙의 SE–SE 입계) · MPM 피복 (면 걷기 쪽).  역학 · 수송은 없다.

### 4-3. ★ 이 묶음의 네 질문 (원문 문장과 위치)
1. **DEM (단단한 구 · 점접촉) 의 한계를 말했나** — **말 없음** (입자 · 접촉 · 역학 · 압력 0 회 · 11 쪽 전수).
2. **소성 · 큰 변형을 계산에 넣기 어려운 이유 · 우회 · 비용** — 해당 없음 (역학이 없다).  비용 문장 하나: 이 방법은 *"only requires the determination of surface voxel configurations from the six nearest neighbours of the cubic lattice"* (p.16) — 14 면체 침식은 FCC 변환 · 원소보다 두꺼운 물체가 필요.
3. **2D 인가 3D 인가 · 2D → 3D** — 3D.  2D → 3D 문장 둘: ① *"In three dimensions the boundary of a binary object does not have a Freeman chain-code equivalent; the boundary is a two-dimensional surface, not a one-dimensional path. The voxels of a 2D surface cannot be ordered in an unambiguous way. However, even when determining perimeter length, the order of the boundary pixels is not essential as long as their contribution to perimeter length is well defined. If one considers the contribution as a function of the number of exposed sides rather than step direction, as in the Freeman approach, then the perimeter length can be generalized to hyper-surface area in any dimension."* (p.7–8) ② 곡률 편향이 차원에 따라 달라진다: *"A similar underestimation occurs when calculating the perimeter length of disks using corner-count chain-code weights optimized for straight lines of infinite length. In that case, however, a constant can be added (Young 1988) because underestimation is independent of disk radius. For spheres, surface area underestimation is proportional to sphere radius in addition to an overall offset"* (p.11) — 2D 원판 = 상수 · 3D 구 = 반지름 비례 + 상수.
4. **압력을 뺄 때의 거동** — 해당 없음.

### 4-4. 기법 미니 용어집
- **표면 (경계) 복셀**: 배경 복셀과 면을 맞댄 (6-연결) 물체 복셀.
- **S1 … S9**: 노출 면의 수 · 배치 (회전 · 거울 동치) 로 나눈 부류 — S1–S3 평면 · S4–S6 곡면 · S7–S9 판 · 선 · 점 (§3-1 표).
- **치우침 β · MSE σ²**: 무작위 방향 (1/48 조각 위 균일) · 위치 평균의 Â − 1 과 (Â − 1)² (식 7a · 7b).  CV = σ/µ (µ = 1 이면 σ).
- **표본 세기 (sample-count)**: 표면 복셀 하나를 넓이 1 로 — Eberly et al (1991).  등방 평균 0.831 배 (16.8 % 과소).
- **공간 격자 (spatial grid)**: 세 직교 시험선 (하나는 IUR) 과 표면의 교차 수 — Hahn and Sandau (1989) · Howard and Sandau (1992).  이 논문 가중으로 쓰면 노출 면 하나 = 2/3.
- **chamfer 거리 변환**: 격자 이웃 걸음에 국소 거리 (면 · 모서리 · 꼭짓점 이웃) 를 주어 거리를 근사 — 최적 국소 거리 식이 이 논문의 넓이 가중 식과 같다 (Verwer 1991).
- **유효 반지름 (구조 원소)**: 다면체를 평면 위에 굴렸을 때 중심 높이의 평균 — 침식된 부피 Δ³N 을 이것으로 나누면 넓이.
- **물체 · 배경 평균**: 물체의 추정 넓이와, 물체에 6-연결된 배경 복셀 (배경의 표면 복셀) 의 추정 넓이를 평균.
- **IUR**: isotropic uniform random — 방향이 구면 위 균일한 무작위.

---

## 5. Figure set ★
| 그림 (크롭 파일) | 내용 | 우리 활용 |
|---|---|---|
| Fig. 1 (`fig_1.png` · `fig_1a.png` · `fig_1b.png`) | (a) 곧은 모서리의 2D 사슬 부호 걸음 (b) 디지털화한 평면 경계 — 노출 면 1 · 2 · 3 개 복셀에 1 · 2 · 3 표시 | 계단 표면의 그림 근거 — 우리 STEP3 계면이 면 1 · 2 · 3 개 노출 복셀로 이뤄진다는 설명 |
| Fig. 2 (`fig_2.png`) | ★ 9 부류 S1–S9 (검은 점 = 대상 복셀 · 정육면체 = 이웃) | 진단에서 부류 빈도를 셀 때의 분류표 (§3-1 표) · S7–S9 = 1 복셀 판 · 선 · 점 = 미해상 표지 |
| Fig. 3 (`fig_3.png`) | 1/48 법선 조각 + P · A · B · C | 최적화 정의역 (식 1) |
| Fig. 4 (`fig_4.png`) | H1 · H2 빗금 — PA 를 균일하게 자르는 평면이 PB 는 tan φ 확률로 | 식 (3) 의 기하 |
| Fig. 5 (`fig_5.png` · `fig_5a.png` · `fig_5b.png`) | ★ (a) 평면 평균 오차 vs 지름 방향 표본 (최적 · 95 % 한계) (b) σ vs 표본 (공간 격자 → 0.102 · 최적 → 0.0233 · 로그) | ★ 해상도 규칙 — 평판 계면은 지름에 표본 ≳20 개라야 방향 바닥 (§3-4 [판독]) |
| Fig. 6 (`fig_6.png`) | ★ 구 · 물체만 오차 vs 반지름 — −4.116 r + 2.610 Δ² | 물체만 세는 넓이의 곡률 편향 기대값 (진단 자기시험) |
| Fig. 7 (`fig_7.png` · `fig_7a.png` · `fig_7b.png`) | ★ (a) 물체 · 배경 평균 뒤 상수 ≈0.53 Δ² (b) CV = 12.539 r^−1.578 % | 진단 기대값 · 우리 r/h (1.7–40) 의 넓이 잡음 (§7-2) |
| Fig. 8 (`fig_8.png`) | 꼭짓점으로 평면에 닿은 육팔면체 · 중심–평면 거리 r | 유효 반지름의 정의 |
| Table 1 (`tab_1.png`) | 구 반지름별 S1–3 · S4 · S5 · S6 몫 | 곡면 부류의 몫 = 해상도 표지 (r 5 에서 5.6 %) |
| Table 2 (`tab_2.png`) | CV = b r^a 계수 (최적 · 공간 격자 · 표본 세기) | 가중별 구 정밀도 |
| Table 3 (`tab_3.png`) | 구조 원소 4 개의 R · σ (시험 · 적분) | 다른 추정기의 크기 |
| 식 (1)–(9) (`eq_01…` … `eq_09…` · 15 장) | 영역 · 노출 조건 · 확률 · 반공간 · 부류 수 · ★ 치우침 (7a) · ★ MSE (7b) · Â(n) (7c) · ★ (8a)(8b) · CV 멱함수 | 보고서 붙임용 · (7c) 로 방향별 오차 계산 |
| 번호 없는 식 3 장 (`eq_u1_hahn_sandau_spatial_grid_sigma_bound.png` · `eq_u2_dilation_erosion_area_estimate.png` · `eq_u3_cuboctahedron_effective_radius_steps.png`) | 공간 격자 σ 상한 ≅ 0.102 · Â = Δ³N/(ΔR) · 육팔면체 단계 A–C | 공간 격자 = 면 세기 × 2/3 의 σ 근거 |
| 근거 문단 20 장 (`txt_p6_…` … `txt_p16_…`) | 서지 + 초록 · 시험선 관점 · 입방 격자 · Nyquist · 정의 · 9 부류 · 평면 = 최악 · 가정 · 창 원기둥 · chamfer · 가중 값 · 표본 세기 · 평면 시뮬 · 구 정의 · S4–S6 · 평균 처방 · 토의 · 침식 · 평면 바닥 · 결론 · 감사 | 인쇄 숫자 · 인용 문장의 근거 (파일 이름의 pN = 학술지 쪽) |

## 6. Post-processing ★
- **원문이 한 것**: 해석 적분 (식 7) → Mathematica 수치 해 (8a)(8b) → 제약 최소 (W₁–W₃) · 몬테카를로 (평면 10⁴ · 구 100 · 무작위 위치) → 평균 · 표준편차 · 95 % 신뢰 한계 · 멱함수 맞춤 CV = b r^a (r²) · 직선 맞춤 (Fig. 6) · 해석 R · σ ↔ 시험 대조 (Table 3).  도구 = Mathematica (Wolfram 1988) · Verwer 의 스크립트 · 시뮬레이션 코드 [미확인].
- **이 카드의 후처리**: ① 식 (7) 재적분 → (8a)(8b) 계수 15 개 · W · σ 재현 · 다른 가중 묶음의 β · σ (§3-3) ② 식 (7c) 로 방향별 오차 (§3-7) ③ Table 3 의 R · σ 재현 ④ 6 면 조합 63 = 9 부류 분해 ⑤ Fig. 5 · 6 · 7 판독 (`digitized.csv` 280 행 — 쪽 300 dpi 렌더 = 원 래스터 · 틀 선 = 눈으로 고른 틀 둘레 ±14 px 안에서 가장 어두운 행 / 열 · 축 끝 = 틀 끝 눈금 글자 · 표지 = 이진 열림 (5×5 · 5(b) 는 3×3) 뒤 무게중심 · 겹친 두 세모는 둘로 셈 · 5(b) 계열 = 표지 모양 (채움 비) + 높이) ⑥ 우리 r/h 에서 원문 식의 값 (§7-2) ⑦ 2 차 인용 카드 줄 대조 (§0-1).  스크립트 = 이 세션 scratchpad (`verify_mv.py` · `digitize2.py` · `write_digitized.py` · `card_numbers.py`) — 결과는 이 카드와 `digitized.csv` 에 남겼다.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 CLAUDE.md · 같은 축 정본 카드의 코드 줄 읽기를 출처와 함께 적는다)

### 7-1. 우리가 넓이를 세는 자리 — 이 논문 기준의 편향 (코드 자리 = `lindblad2005_…` §7-1 이 읽은 stoic @57f1b2baf (2026-11-03) · 이 카드는 리포 코드를 다시 읽지 않았다)
| 자리 (그 카드가 읽은 코드) | 넓이 규약 | 이 논문 기준의 편향 | 표지 |
|---|---|---|---|
| STEP4 BV 반응면 `A_face = vox_m*vox_m` (`scripts/step4_dyn.py:1134`) | 노출 AM\|SE · AM\|SDCP 면 하나 = h² = **노출 면 그대로** | 등방 평면 평균 **1.500 배** (식 8a) · 방향별 1–1.732 · 구 1.5 × (1 − 1.06/(4π(r/h)²)) | [카드 산술] |
| r1 면 막 `face_rint` (`scripts/step3_sigma.py:362`) | 다른 sid 면마다 같은 r | 막 총 컨덕턴스 = (면 수 · h²)/r → 참 넓이당 유효 값은 위 배수만큼 [카드 해석 · lindblad 카드와 같은 결론] | [카드 해석] |
| 면 걷기 피복 `am_surface_patches` (`:4832` · docstring *"계단으로 ~1.5× 과대"*) | 면 개수 비 | **"~1.5×" 의 원문 근거 = 이 논문 식 (8a) + 공간 격자 문장** (p.11) · 비율 상쇄는 피복 영역 방향이 무작위일 때만 (§3-7: 축 쪽 1.0 · 몸 대각 1.73) | [카드 산술] |
| ①′ AM–AM 막 CNC `iface_rface_ohm_cm2` (`:1751-1756`) | 접점마다 해석 원판 넓이로 총량 정규화 | 추정기가 아니다 — 이 논문의 대상 밖 (참값을 아는 정규화) | [카드 해석] |
| MPM 피복 (CLAUDE.md "MPM coverage PLASTIC vs RIGID" 절) | 강체 = 해석 (구면 표본) · 소성 = 변형 SE 점 구름 · ⛔ 복셀 인접 `coverage_AM_*_mpm_pct` (~26 %) 는 보고 금지 | 해석 · 점 구름 측정은 이 편향과 무관 · 복셀 인접 측정은 표면 칸 세기 꼴이라 비율의 상쇄가 피복 영역의 방향 분포에 기댄다 (§3-7) [카드 해석 — 그 측정이 보고 금지인 이유 (점 밀도 · 비수렴) 는 다른 기전] | [카드 해석] |

### 7-2. ★ 우리 해상도 (r/h) 에서 이 논문 식의 값 (구 · 물체만 · 물체 · 배경 평균 · CV · 면 세기) — [카드 산술] · "우리 예" = `lindblad2005_…` §7-3 표 A 의 크기 대응
| r/h | 우리 예 (r µm @ h µm) | 물체만 (Fig. 6 직선) | 평균 뒤 (+0.527Δ²) | CV (식 9 · 최적) | 면 세기 / 참 (1.5(1 − 1.06Δ²/A)) |
|---|---|---|---|---|---|
| 1.67 | SE 0.25 @ 0.15 | −12.2 % ⚠외삽 | +1.50 % ⚠외삽 | 5.6 % ⚠외삽 | 1.455 |
| 2.5 | AM 1 @ 0.4 | −9.8 % ⚠외삽 | +0.67 % | 2.95 % | 1.480 |
| 3.33 | SE 0.5 @ 0.15 | −8.0 % | +0.38 % | 1.88 % | 1.489 |
| 5 | SE 0.75 @ 0.15 | −5.7 % | +0.17 % | 0.99 % | 1.495 |
| 6.67 | AM 1 @ 0.15 | −4.4 % | +0.094 % | 0.63 % | 1.497 |
| 10 | SE 1.5 @ 0.15 | −3.1 % | +0.042 % | 0.33 % | 1.499 |
| 13.3 | AM 2 @ 0.15 | −2.3 % | +0.024 % | 0.21 % | 1.4993 |
| 20 | AM 3 @ 0.15 | −1.6 % | +0.010 % | 0.11 % | 1.4997 |
| 40 | AM 6 @ 0.15 | −0.8 % | +0.003 % | 0.037 % | 1.4999 |

- ⚠ 외삽 = 이 논문 구 시험 범위 (r ≈ 3–40 Δ [판독]) 밖.  r/h < 3 에서는 S7–S9 (원문 가중 없음) 와 S4–S6 (원문 미최적) 몫이 커진다 (Table 1: r 5 에서 이미 5.6 %).
- 해석 (값은 위 표 · 판정 아님): ① 면 세기의 **1.5 배** 는 해상된 구에서 반지름과 거의 무관 (r/h ≥ 3.3 에서 1.489–1.4999) — STEP4 반응면 · r1 막의 넓이 기준이 "면 넓이당" 이라는 한정어의 크기 ② MV 가중은 평균만 하면 r/h ≥ 3 에서 넓이 오차 < 0.5 % · 잡음 < 2 % ③ **물체만** 세면 우리 SE (r/h 1.7–10) 에서 −12 … −3 % — 평균을 빼먹으면 생기는 크기.

### 7-3. ★ 이 가중을 AM–SE 계면 · 피복에 쓸 때의 적용 조건과 한계 (의도 덧붙임)
1. **방향 무작위 · 위치 무작위** — 불편은 이 평균에서만 (p.9 가정 · §3-7).  우리 쪽에서 방향이 몰리는 곳: ①′ AM–AM 근축면 (평판 원판 · 법선 = 접점 방향 하나 → 원판 하나는 −10.6 … +3.0 %) · 압축축 쪽 피복 모자 (일축 압밀) — 이런 곳은 법선을 아는 해석 가중 (`lindblad2005_…` §7-4 의 1/L1(n) · \|n_k\|) 이 맞다.
2. **해상도** — 평판 계면의 지름에 표본 ≳20 개 (Fig. 5(b) 판독: 18.5 개에서 바닥 +10 % · 5.4 개면 σ 0.062) · 우리 AM–AM 접점 원판 a/h 1–9 (지름 표본 2–17) 은 이 규칙에 못 미치거나 겨우 닿는다 [우리 산술 · a/h 범위 = `lindblad2005_…` §7-3 표 B].  구는 r ≳ 3 Δ (이 논문 시험 범위).
3. **닫힌 곡면은 물체 · 배경 평균** — AM 구 표면처럼 닫힌 경계는 물체 쪽만 세면 −0.33 Δ/r (상대) 과소 · 평균 뒤 +0.527Δ² 를 빼야 한다.  두 상 계면 (AM \| SE) 에서는 AM 쪽 표면 복셀과 SE 쪽 표면 복셀의 두 추정을 평균하는 꼴이 같은 처방의 대응 [카드 해석 · 원문은 두 상 (물체 · 배경) 만].
4. **세 상 (AM · SE · 기공)** — 이 논문은 이진 영상뿐.  AM 표면 복셀의 노출 면이 SE 와 기공에 나뉠 때 가중을 나누는 규칙은 **원문에 없다** (Windreich 2003 의 W_i^p = (p/P)·W_i 가 후속 규칙 — `windreich2003_…` §3-1).
5. **S4–S6 · S7–S9** — 곡면 부류는 미최적 (공간 격자 값) · 판 · 선 · 점은 가중 없음 → 1–2 복셀 두께의 SE 막 · 섬유 (VGCF 선분 스탬프) · 1 복셀 섬은 이 추정기의 정의역 밖 (그 몫 = 미해상 표지).
6. **오목 · 닿은 두 물체** — 시험은 평면 · 볼록 구뿐 (Table 1 의 S4 = 0 이 그 증거) · 압밀 뒤 SE 의 오목 면 · 접점 둘레의 곡률은 이 논문 밖.
7. **다중격자 수렴 없음** — 평면 CV 바닥 2.33 % 는 해상도로 안 사라진다 (p.15) · 수렴 시험 (U6) 에서 넓이 오차가 0 으로 가지 않는 것이 결함이 아니다.

### 7-4. frame[5] · frame[4]
- **frame[5]**: 이 논문은 수송도 역학도 아닌 **측정 (기하) 도구** — 우리 쪽 소유자는 STEP3/STEP4 의 면 넓이 (복셀 FV · 수송 쪽 이산화) 와 MPM 피복 측정 (역학 산출의 후처리) 둘 다.  DEM 접촉망의 Holm · Tabor 넓이는 접촉마다 해석식이라 이 편향과 무관하다.
- **frame[4]**: 대조 대상이 우리 다른 모델이 아니라 **해석해 (평면 넓이 1 · 4πr²)** 라 순환 위험이 없다.

---

## 8. ★ 자세한 분석 — 우리 계획에 무엇을 주나
(이름 = 정독 지시서 3 절.  우리 값 = CLAUDE.md: DEM 18 배 연화 · E_eff 1.35 GPa · 순수 SE Heckel P_y 138 MPa / MPM E 1.53 GPa · σ_y 0.30 GPa · ν 0.49 / 랩 표준 = 순수 SE 300 MPa 기공 10–13 % · LPSCl 진밀도 1.64 g/cm³ — 고정 · 판정 대상 아님.  **이 논문은 기하 측정 이론이라 역학 · 기공 숫자를 나란히 놓을 자리가 없다** — 행마다 그 사실을 적는다.)

| 이름 | 이 논문이 주는 것 | 못 주는 것 · 한정어 |
|---|---|---|
| **단계 0** (기공 연산자 · 판정 기준 결과 전 등록) | ★ **"넓이 연산자도 정의를 먼저 적는다"** 의 근거 — 같은 영상에서 표본 세기 0.831 배 · 면 세기 1.500 배 · MV 1.000 배 (등방 평균) · 방향별로는 셋 다 다르게 틀린다 (§3-7).  피복 · 계면 넓이를 판정 기준에 쓸 때 (추정기 · 해상도 (지름 표본 수) · 방향 가정 · 물체 / 배경 평균 여부) 를 결과 전에 적는다 · 무작위 위치 표본 (가운데 복셀 안 균일 · N 회) = 연산자 시험 설계 | 기공 (부피) 연산자에 대한 말은 없다 — 부피 세기는 이 넓이 편향을 받지 않는다 [카드 해석] · 랩 표준 (10–13 % · 1.64) 과 나란히 놓을 숫자 없음 |
| **단계 1** (3D 메모리 · 장 수) | 없음 (6-이웃 배치만 보는 국소 · 선형 시간 연산 — p.16) | — |
| **단계 2** (2D MPM 코드 · 단위 시험) | 2D 단위 시험의 함정 하나: 2D 원판 둘레 과소는 반지름과 무관 (상수) 이지만 3D 구 넓이 과소는 반지름 비례 (p.11) → 2D 에서 맞춘 넓이 · 둘레 연산자가 3D 곡률 편향을 보여 주지 않는다 [카드 해석] | MPM 구성식 · 시험 해 없음 |
| **단계 3** (2D 접촉 표현 비교) | 없음 | — |
| **단계 4** (3D 순수 SE · σ_y 하나를 실험 기공에 맞춤) | 없음 (넓이 · 부피 아님 · 맞춤 표적 아님) | — |
| **단계 5** (3D 복합 압밀) | 없음 (압밀 뒤 AM–SE 계면 넓이를 복셀로 잴 때만 §7-3 의 조건이 걸린다) | 하중 몫 · 기공 숫자 없음 |
| **단계 6** (탈압 · 되돌아옴) | 없음 | — |
| **단계 7** (형상 · 피복 · 수송) | ★ 주 자리 — ① 면 세기 편향 **1.5 배 (등방) · 1–1.732 (방향) · 구 1.5 × (1 − 1.06Δ²/4πr²)** 의 원문 근거 ② MV 가중 (0.8940 · 1.3409 · 1.5879 + S4–S6 공간 격자 값) 과 성능: 평면 CV 2.33 % (바닥) · 구 CV 12.539 r^−1.578 % · 평균 뒤 +0.527Δ² ③ 닫힌 곡면 = 물체 · 배경 평균 필수 ④ 해상도: 평판 지름 표본 ≳20 · 구 r ≳ 3 Δ ⑤ 우리 r/h 표 (§7-2) | 세 상 계면 나누기 · 오목 · 닿은 물체 · 방향이 몰린 계면 (압축) 의 불편은 보장 안 됨 · 이온 / 전자 수송 숫자 없음 |
| **후보 D0** (지금 DEM) | 없음 — DEM 접촉 넓이 (Hertz · Tabor · Stage-E) 는 접촉마다 해석식 | DEM 침대를 복셀화해 STEP3 로 넘길 때의 계면 넓이에만 §7 이 걸린다 |
| **후보 A′-0 · A · A′** (MPM 판 · 벽 접촉 · 강체 AM · 입자별 속도장) | MPM 침대의 피복을 **측정 격자 면 걷기** 로 잴 때 (피복 설계 메모 C(b) 주 추정기 · `lindblad2005_…` §7-4) 이 편향 · 조건이 그대로 걸린다 · 변형된 SE 표면은 해석 법선이 없어 MV · 2×2×2 같은 국소 가중이 유일한 길 | 다물체 접촉 · 강체 결합 · 해상도 규칙 (지름당 셀) 의 역학 쪽 근거 없음 |
| **후보 B** (입자별 FE + 접촉) | 없음 (표면 메시 = 삼각형 넓이 · 복셀 아님) | — |
| **후보 C · C′** (큰 변형 · 항복 캡 접촉 DEM) | 없음 | — |
| **후보 M0** (균질화 압밀) | 없음 | — |
| **U0–U6** | **U1** (입자 하나 압축과 해상도): 접촉 · 피복 넓이 판독의 측정 오차 바닥 = 구 r(셀) 별 원문 값 (§7-2 · 물체만 −0.33Δ/r · 평균 +0.527Δ² · CV 식 9) · **U6** (조밀 충전 압축의 해상도 수렴): 방향 오차는 해상도로 안 줄어든다 (평면 CV 바닥 · p.15) → 넓이 수렴 시험은 위치 잡음 성분만 줄어드는지 본다 (Fig. 5(b) 의 위치 성분 ∝ 표본^−1.4 [카드 산술]) | U0 · U2 · U3 · U4 · U5 없음 |
| **R1–R7** | **R6** (SE 형상 변형): 변형된 SE 표면 · SE–SE 계면의 넓이는 해석 법선이 없어 이 꼴의 국소 가중으로만 잴 수 있다 — 그 정밀도 바닥 (평면 2.33 %) 과 조건 | R1–R5 · R7 없음 |
| **결과 전 대조 항목** | ★ 진단 (`lindblad2005_…` §적용 후보 가-1 · `scripts/diag_voxel_area_bias.py` 제안) 의 **원문 기대값**: 평면 β = 0 · σ 0.0233 (최적) · 0.10163 (공간 격자) · 0.12037 (불편 표본 세기) · 표본 세기 0.83119 · 면 세기 1.5 · 축 정렬 평면 0.8940 · 구 물체만 −4.116 r + 2.610 Δ² · 평균 뒤 0.527 ± ~0.1 Δ² · 공간 격자 −1.06Δ² · 불편 표본 세기 −0.457Δ² · CV 식 (9) Table 2 · Table 1 부류 몫 — 우리 MV 구현이 이 값들을 재현하는지 (맞추는 데 쓰지 않음) | 재료 · 압력 · 진밀도 무관 |

- **재료 · 차원 · 조건 차이**: 재료 없음 (이진 영상) · 3D · 입방 격자 · 두 상 · 볼록 구와 평면 · 디지털화 = 복셀 중심 판정 · 압력 · 온도 해당 없음 → 우리 침대 (세 상 · 압밀 뒤 오목 · 접촉 · 방향 몰림) 와의 차이는 §7-3 이 전부다.

## 9. 적용 인사이트 (행동)
1. **"면 세기 ~1.5×" 한정어에 원문 출처를 붙인다 (단계 7)** — STEP4 `A_face` · r1 면 막 · `am_surface_patches` (VX1) 의 넓이 기준: *"노출 면 하나 = h² 는 등방 평면에서 참 넓이의 1.500 배 (방향별 1–√3) · 해상 구에서 1.5 × (1 − 1.06Δ²/4πr²) — Mullikin & Verbeek 1993 식 (8a) · p.11–12 (공간 격자 = 노출 면 × 2/3 · 상수 −1.06Δ²)"*.  Lindblad 식 18 (같은 L1 관계) 과 두 출처가 된다.
2. **진단 자기시험에 원문 숫자를 넣는다 (결과 전 대조 항목)** — 계획된 넓이 편향 진단에서 우리 MV 구현이 ① 평면 무작위 β ≈ 0 · σ ≈ 0.0233 ② 축 정렬 평면 0.8940 ③ 구 물체만 Fig. 6 직선 (r/h ≥ 5 에서 0.1 % 안 — `lindblad2005_…` pilot 이 이미 0.0005 안) ④ 평균 뒤 0.527 ± 0.1 Δ² 를 재현하는지 본다 (변이 시험: 가중 하나를 바꾸면 ①–② 가 깨져야).
3. **방향이 정해진 계면에는 MV "불편" 을 쓰지 않는다** — 원판 하나 · 압축축 모자는 −10.6 … +3.0 % (MV) · 1–1.732 (면 세기) 의 결정론 오차 (§3-7) → 법선을 아는 곳 (AM 구 · 근축면) 은 해석 법선 가중 · 모르는 곳 (변형 SE) 만 국소 가중.
4. **해상도 규칙을 판독 조건으로 적는다** — 평판 계면 · 피복 패치는 지름 표본 ≳20 개에서만 방향 바닥 (2.33 %) · 5–10 개면 위치 잡음 2–6 % 가 더해진다 (Fig. 5(b) [판독 · 카드 산술]) — 접점 원판 (a/h 1–9) 의 넓이를 개별로 인용하지 않는 근거.
5. **닫힌 곡면 넓이는 물체 · 배경 평균** — AM 구의 표면 넓이 · 피복 분모를 복셀로 잴 때 AM 쪽만 세면 r/h 6.7 에서 −4.4 % (Fig. 6 직선 [카드 산술]) — 양쪽 평균 + 상수 보정이 원문 처방.
6. **흐름 밖: SR-01 섬유 계단 인자 k 의 크기 읽기** — CLAUDE.md 가 적은 계단 인자 k = 1.4855 (vox 0.4) · 1.4917 (0.3) · 1.4461 (0.25) (그 뒤 경로 순서를 지키는 L1 걸음으로 estimator 를 고쳤다고 적힘 — 이 값이 어느 판인지 이 카드는 가리지 않는다) 은 **등방 방향의 L1 평균 1.500** (식 8a 의 μ₁ + 2μ₂ + 3μ₃) 과 같은 크기다 — 같은 항등식 (직선 단위 길이당 6-연결 걸음 수 = \|u_x\| + \|u_y\| + \|u_z\|) [카드 해석 · 섬유 방향 분포가 등방인지는 확인 안 됨 · CLAUDE.md 대로 k 로 σ_e 에 상 · 하한을 붙이지 않는다].  같은 식이 3×3×3 chamfer 거리의 최적 국소 거리 (0.8940 · 1.3409 · 1.5879) 이기도 해 (p.10), 복셀 걸음 경로 길이의 등방 보정 계수가 필요하면 그 값이 출처다.

## 10. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Surface voxels — object voxels six-connected to the background — fall into nine configuration types; weighting the three planar types (one, two or three adjacent exposed faces) by W₁ ≈ 0.8940, W₂ ≈ 1.3409 and W₃ ≈ 1.5879 (grid units²) makes the area estimate unbiased with minimum mean-square error for randomly oriented and positioned planes, with a coefficient of variation of 2.33 % (Mullikin and Verbeek, *Bioimaging* 1 (1993) 6–16)."
- "Counting surface voxels with unit weight underestimates the area of digitized planes by 16.8 %; counting exposed voxel faces overestimates it by a factor of 1.5 on average (spatial-grid weights of 2/3 per exposed face are unbiased) (Mullikin and Verbeek 1993; factor 1.5 derived from their Eq. 8a)."
- "For digitized spheres the object-only estimate is low by an amount proportional to the radius (−4.116 r + 2.610 Δ²); averaging the object and background surface areas leaves a constant bias of 0.527 Δ² (Mullikin and Verbeek 1993)."
- 국문: *"복셀 면을 그대로 세면 무작위 방향 평면의 넓이를 평균 1.5 배로 센다 (방향에 따라 1–1.73 배) — 노출 배치별 가중 (0.894 · 1.341 · 1.588) 은 그 평균 치우침을 없애지만 방향이 정해진 평면 한 장에는 −10.6 … +3.0 % 가 남는다 (Mullikin & Verbeek 1993 · 방향 범위는 식 (7c) 로 계산)."*

## 11. 주의/한계 (over-claim 방지)
**원문이 스스로 적은 한계**
1. 표본 간격이 영상 해상도의 Nyquist 조건을 만족해야 한다 — 물리 절편은 안 될 수 있다 (p.7).
2. 평면은 최악 대상 · 평면 CV 는 바닥 (2.33 %) 으로 수렴 — 법선 이방성 (p.8 · p.15).
3. 구는 넓이가 과소 → 물체 · 배경 평균 + 상수 보정 필요 (p.11 · p.15–16).
4. 성긴 해상도 (가장 성긴 두 점) 에서는 σ 가 커서 95 % 한계를 벗어난다 (p.13).

**카드가 본 한계 · 원문 안 어긋남**
5. **불편은 무작위 방향 평균에서만** — 방향별 오차는 원문에 없다 (−10.6 … +3.0 % 는 [카드 산술]).
6. **S4–S6 은 도출하지 않았다** (공간 격자 값) · **S7–S9 가중 없음** · 원기둥 물체 시험 없음 (의도의 '원기둥 성능' 은 없다).
7. **이진 두 상 · 볼록 · 입방 격자 · 복셀 중심 판정** — 세 상 계면 · 오목 · 닿은 두 물체 · 비등방 격자 · 부피 문턱 디지털화는 범위 밖.
8. 구 결과의 범위는 r ≈ 3–40 Δ [판독] · 식 (9) · Fig. 6 직선을 r < 3 Δ 로 외삽하면 [카드 산술] 표지를 달아야 한다.
9. 상수 0.527Δ² 는 반지름 ≈120 개 · 각 100 개의 평균에서 낸 값 — 그 자체의 불확도 ≈ ±0.1 Δ² [카드 산술] 는 원문에 없다.
10. 원문 안 어긋남 여덟 (§3-8 ⑥) — 값에 닿는 것은 Table 3 의 *"1.290.13"* (본문 1.290 13) 하나.
11. 시뮬레이션 코드 · 난수 · 구 반지름 목록은 실리지 않았다 [미확인].
12. **전이 한계**: 기하 상수라 재료와 무관하게 옮지만 위 7 의 조건이 붙는다 — 우리 압밀 침대의 AM \| SE 계면은 그 조건 (두 상 · 볼록 · 방향 무작위) 을 어긴다.

## 12. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 원문 목록 | 서지 (원문 그대로) | 왜 |
|---|---|---|
| Verwer 1991 | Verwer B J H 1991 Local distances for distance transformation in two and three dimensions *Pattern Recognition Lett.* **12** 671–82 | ★ 같은 식 · 같은 값 (*"table 6"*) · Mathematica 스크립트의 출처 — 복셀 걸음 경로 길이의 최적 국소 거리 · 카드 없음 |
| Hahn and Sandau 1989 | Hahn U and Sandau K 1989 Precision of surface area estimation using spatial grids *Acta Stereol.* **8** 425–30 | ★ 공간 격자 (S4–S6 값의 출처) · σ 상한 식 (6) → 0.102 · 카드 없음 (`windreich2003_…` 이 인용만) |
| Eberly et al 1991 | Eberly D, Lancaster J et al 1991 On gray scale image measurements: II. Surface area and volume *CVGIP: Graphical Models and Image Process.* **53** 550–62 | 표본 세기 · 표본 법선 방법 · 구에서의 표본 세기 비 (*"table 3"*) — 16.8 % 를 구로 확인한 원전 · 카드 없음 |
| Meyer 1992 | Meyer F 1992 Mathematical morphology: from two dimensions to three dimensions *J. Microsc.* **156** 5–28 | 팽창 / 침식 넓이 · CC · FCC 시험선 — Table 3 의 대상 · 카드 없음 (`meyer2017` · `meyer2018` 은 다른 Meyer) |
| Young 1988 | Young I T 1988 Sampling density and quantitative microscopy *Anal. Quant. Cytol. Histol* **10** 269–75 | 원판 둘레에 상수를 더하는 처방 · 표본 밀도 (Nyquist) — 해상도 규칙 · 카드 없음 |
| Howard and Sandau 1992 | Howard V C and Sandau K 1992 Measuring the surface area of a cell by the method of the spatial grid with a CSLM—a demonstration *J. Microsc.* **165** 183–8 | 공간 격자의 실영상 적용 |
| Mattfeldt et al 1985 | Mattfeldt T, Möbius H-J et al 1985 Orthogonal triplet probes: an efficient method for unbiased estimation of length and surface of objects with unknown orientation in space *J. Microsc.* **139** 279–89 | 직교 세 시험선의 *"antithetic effect"* (p.7) |
| Beckers and Smeulders 1992 | Beckers A L D and Smeulders A W M 1992 Optimization of length measurements for isotropic distance transformations in three dimensions *CVGIP: Image Understanding* **55** 296–306 | 3D 길이 측정 최적화 — 같은 방법의 길이 판 |

## 13. [미확인] 목록 (11 쪽 전수에 없음)
1. 방향별 (한 방향 평면의) 오차 — 원문 숫자 없음 (§3-7 은 카드 산술).
2. S4–S6 의 최적 가중 · S7–S9 의 가중.
3. 원기둥 · 타원체 · 오목 물체의 시험.
4. 구 시험의 반지름 목록 · 간격 (판독 ≈0.31 Δ) · Fig. 7 의 직선 맞춤 방법 (판독상 거의 수평) · Fig. 5(a) 점들의 표본 값.
5. 시뮬레이션 코드 · 난수 생성 · 계산 시간.
6. 원판 (2D) 처방의 상수 값 (Young 1988 에 맡김).
7. 세 상 · 다중 라벨 영상에서의 쓰임.
8. 1993 인쇄면의 DOI (내려받기 표지에만 있음).

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-11-16)
- PDF 11 쪽 (학술지 p.6–16 · 쪽마다 회색 래스터 + 숨은 OCR 층) 을 쪽 그림 (130–300 dpi) 으로 전부 읽음 · OCR 글자 층은 위치 · 문장 찾기에만 썼다 (식 줄의 OCR 상자는 실제 잉크와 4–10 pt 어긋나 식 크롭은 눈금 자 렌더로 다시 잡음).  서지 = 첫 쪽 (머리 줄 · 제목 · 저자 · 소속 · 접수일 · 초록 · 키워드 · 쪽 아래 저작권 줄) + 내려받기 표지 (DOI · 호).  SI 없음 · 그림 8 · 표 3 · 식 9 묶음 + 3 · 참고문헌 23.
- 그림 도구 (`extract_figures.py --dry`) 는 9 개를 냈으나 모두 쪽 폭 전체 · 표는 쪽 전체 (두 단이 섞임) · Fig. 5 는 '영역 없음' 으로 빠짐 → **52 장 전부 손 크롭** (300 dpi = 원 래스터 · 흰 여백 잘라 사방 15 px · 글 · 식은 가장자리 이웃 줄 조각 띠 제거 · 두 조각 이상이면 위아래로 이어 붙임 (사이 24 px)).  **다시 자름 6**: `fig_8.png` (윗줄 본문 꼬리 섞임) · `tab_3.png` (σ 끝자리 잘림) · `eq_07a` · `eq_07b` · `eq_07c` (적분 아래 첨자가 옆 식으로 넘어감) · `eq_u2` (문장 중간에서 시작).  52 장 전부 열어 봄 (모음 판 6 장 + 글 · 식 위아래 띠 모음 2 장).  `figures.json` 의 `manual_crop` · `recrop` · `viewed_how`.
- 판독: Fig. 5(a) · 5(b) · 6 · 7(a) · 7(b) — 겹쳐 그린 확인 그림 (`overlay2_*`) 으로 표지 · 오탐을 눈으로 확인 (5(b) 의 글자 조각 1 · 7(a) 의 직선 조각을 걸러냄 · 5(b) x 3.3 의 세모를 네모로 잘못 붙인 것을 표지 모양으로 고침).
- 재현: 식 (8a)(8b) 계수 15 개 · 최적 가중 · σ · 표본 세기 −16.8 % · 1.2031 · 공간 격자 σ 0.10163 = Hahn–Sandau 상한 · Table 3 의 R · σ 6 개 — 모두 인쇄값과 같다 (§3-3 · §3-6).
- 2 차 인용 대조: `windreich2003_…` (L34 · L42–56 · L63–65 · L101 · L169 · L174 · L191) · `lindblad2005_…` (L30 · L39 · L40 · §7-3 표 A) · 비교 문서 [Windreich03] 블록 — 고치지 않았다 (카드 문제 = 정독 출력 batch_114 의 "카드 문제" 절).
- 정본 litdb 중복 확인: `litdb/papers/` 파일 목록 (mullikin* · verbeek* 없음) + 제목 · 'Mullikin' · 'Verbeek' · 'Bioimaging' grep — 카드 없음 (인용만: windreich2003 · lindblad2005) (2026-11-16).

## 🔗 관련 카드
- 같은 축 (복셀 넓이 추정): `windreich2003_voxel_based_surface_area_estimation` (이 논문 [9] → S7–S9 · 고곡률 · ROI) · `lindblad2005_surface_area_weighted_local_configurations` (이 논문 [8] → 2×2×2) · `ziegel2010_surface_area_measure_digitizations` (점근 최악 3.98 %).
- 복셀 면에 계면 조건 · 복셀 → 메시: `neumann2021_garnet_3d_structure_grain_boundaries_li_transport` · `chouchane2019_innov_voxelization_multiphase_meshing` · `chouchane2021_innov_webapp_stochastic_generation_meshing`.
- 계단이 계면 넓이를 부풀린다는 경고: `ketter2025_resistor_network_models_predict_transport_properties` (§7-6 · `lindblad2005_…` 머리의 짝 카드 목록 경유).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

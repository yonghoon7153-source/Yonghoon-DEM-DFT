# batch 74 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-12)

대상: `nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions` — John A. Nairn, James E. Guilkey, "Axisymmetric form of the generalized interpolation material point method", *Int. J. Numer. Meth. Engng* 101 (2015) 127–147 · DOI 10.1002/nme.4792 (후보 표 N-35 · 가리킨 카드 = `gritton2017_mpm_chemomechanical_coupling_silicon_anode` §9 ⑩ · §10 행동 4 · L597 · L624 · L58).
GIMP 를 원통 좌표로 다시 유도해 회전체 + 축대칭 하중 문제를 r–z 단면 하나로 푸는 MPM (r 가중 형상 함수 · 후프 함수 T_ip · 라디안당 질량 · 축 r = 0 영역 자르기 · uGIMP / CPDI 닫힌 꼴) + 확장 넷 (견인 경계 · 명시 균열 · 다물질 접촉 법선 · 열 / 확산) + 시험 셋 (Neo-Hookean 원판 균일 반지름 압축 · 원기둥 끝 견인 · 텅스텐 봉 관통 실험 대조) + 코드 체크리스트 9 항.
쪽 = 학술지 쪽 = PDF 쪽 + 126 · SI 없음 · 그림 판독 = PDF 벡터 경로 좌표 (`figures/<slug>/digitized.csv`).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 (SE · 분말 · 기공 보고 0).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 'unload' 0 회 · 원판은 끝까지 압축 · 견인은 선형 증가 · 관통은 한 번의 충돌 (카드 §0-2 (iv)).

## c — 항복 · 경도 · 크리프 값과 정의
- [c] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions | 금속 Johnson–Cook 상수만 — 텅스텐 A 1.50696 GPa · B 0.17664 GPa · C 0.016 · n 0.12 · m 1.0 · T_m 1723 K / 강 A 1.50 · B 0.569 · C 0.003 · n 0.22 · m 1.17 · T_m 1777 K (+ Mie–Grüneisen C₀ · S · γ₀ · 밀도 · 전단 계수) | Table I · p.143 | 인쇄 (*"as reported by Anderson et al. [21]"*) | JC 식 자체는 인쇄 안 함 (ref. [19] 로 넘김) · 일축 항복 환산 없음 · 금속 — LPSCl 값 아님 · 맞춘 값 아님

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 (한 물체 · 입자 층 없음).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 (DEM · 점접촉 법칙 0 회).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
- [f] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions | 축대칭 다물질 접촉: 물질마다 속도장 (multimaterial mode) · 축대칭으로 바꿀 곳은 법선뿐 (*"Most planar 2D contact tasks can be applied directly to axisymmetric MPM.  The only exception is determination of the normal vector"*) → 부피 기울기 (식 54) 는 V_p ∝ r 라 틀림 → **r–z 면적 기울기** ‖n‖n = Σ A_p G_ip (식 55) · 축 노드에서 n 의 r 성분 = 0 · 접촉 판정의 노드 부피 → 노드 면적 · 축 노드 면적 두 배 (평면 대칭면에도 같은 수정) · 불완전 계면은 총 계면 넓이 보정 ([17] 에 유도) | §3.3 · p.138–139 · 체크리스트 4 (p.145) | 인쇄 | **정식화만 · 접촉 계산 예 0** · 관통 (§4.3) 의 두 물체 처리 [미확인]
- [f] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions | 법선 정확도: *"experience has shown that accurate determination of the normal is crucial to accurate contact simulations [6]"* · 밀도가 다른 물질끼리는 질량 대신 부피 기울기 (p.138) | p.138 | 인쇄 | 근거는 ref. [6] (Lemiale 외 2010 · 정본 카드 없음)
- [f] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions | 강체: 원판 압축을 *"rigid particles"* 일정 속도로 (강체 결합 식 없음) · 해상도: 셀 2.5 × 2.5 (원판) · 2 × 2 (원기둥) · 0.25 × 0.25 mm (관통) · 셀당 입자 = 관통 *"four particles/cell"* (인쇄) · 원판 · 원기둥은 방향당 2 ([판독] — 입자 간격 = 셀 절반) · 수치 오차 = 정확해 (식 66–67) · 지정 응력 · 실험 대조 · 격자 수렴은 *"not shown"* | §4.1–4.3 · p.141–145 | 인쇄 · [판독] | 노름 · 수렴 차수 · '지름당 셀 수' 규칙 없음
- [f] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions | 축 처리 규칙: 영역이 축을 넘으면 (n_i < 1 + l_p/2 · r_p < l_pΔr/2) 형상 함수 특이 → uGIMP 는 r = 0 에서 자름 · 격자는 r = 0 에 노드 (특수 꼴 n_i = −1 · 0 · 1 뿐) · CPDI 는 평행사변형을 s = r_p/\|d_1r + d_2r\| 로 줄임 · 입자가 r = 0 을 넘으면 계산 정지 | p.131 · p.135–136 · p.145 | 인쇄 | —

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions | 축대칭 = 3D 회전체를 r–z 2D 로 (*"The key changes were to replace volume integration by cylindrical volume integration and to account for cylindrical coordinates in gradient evaluations"* p.128) — 질량 · 힘 · 부피 · 열 유속은 라디안당 | §2 · p.128–130 | 인쇄 | 기하 · 하중 · 경계 · 접촉이 다 축대칭일 때만 [카드 추론]
- [g] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions | 평면 2D 형상 함수를 축대칭 계산에 그대로 쓰면 축 근처 큰 오차: 원판 J 16 % 에서 축 첫 입자 J 23.33 % (축 바깥 노드 처리 없음) · 17.48 % (BC 0) · 16.02 % (거울 — *"meant to mimic the value that node would have in a full three-dimensional simulation"*) ↔ 축대칭 자름 16.31 % | Fig. 6 · p.142 | [판독] · 인쇄 | Neo-Hookean · ν 0.33 · 원판 균일 압축만
- [g] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions | 평면 ↔ 축대칭 차이 목록: 형상 함수 = 평면 + 1/(2n_i + ξ_p) 항 (축에서 멀면 평면 · 카드 수치 n = 100 차 2 × 10⁻⁴) · 후프 항 · 견인 두께 B ↔ 반지름 가중 (3D = 여섯 면 *"straightforward"*) · 입자 힘 라디안당 + r 의존 · 접촉 법선 · 열 유속 | §2–§3 · p.131 · p.137–140 | 인쇄 · [카드 산술] | **3D 계산 · 3D 와의 같은 문제 대조 · 계산 비용 0**

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 (DEM 0 회).

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions | 큰 변형 한계: uGIMP 인장 약 50 % (*"large-deformation tension tests are limited to about 50% strain when using uGIMP"* p.134 · p.144 *"not stable for the simulated 50% tensile strain"*) · 압축 uGIMP 88 % · CPDI 약 93 % 에서 붕괴 (p.143) | p.134 · p.143 · p.144 | 인쇄 | 원판 균일 압축 · 원기둥 인장 · Neo-Hookean
- [j] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions | 축대칭 J 적분 미개발 (*"is in need of additional development"*) · 입자가 r = 0 을 넘으면 계산을 멈춤 (체크리스트 9) · CPDI 모서리가 반올림으로 축을 넘음 (*"and they do in some sample calculations"*) · 평면 형상 함수는 *"only if great care is used in setting boundary conditions"* | p.138 · p.135 · p.143 · p.145 | 인쇄 | —
- [j] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions | 카드가 남긴 미확인: 3D 대조 · 비용 · Δt · 압축 속도 · 입자 수 (인쇄) · 관통의 두 물체 처리 · 격자 수렴 수치 · ν 0.33 밖 (거의 비압축) 의 축 근처 거동 · Fig. 7 의 선이 84 % 를 넘어 V/V0 ≈ 9.3 % 까지 그려진 까닭 · Fig. 5 ↔ 6 의 같은 이름 계열 끝 두 점 차 | 카드 §3-6 · §12 | [미확인] | —

## k — DEM 의 한계
- [k] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions — Nairn & Guilkey 2015 (Int. J. Numer. Meth. Engng 101, 127–147) | DEM (단단한 구 · 점접촉) 의 한계 = **말 없음** (DEM · 'discrete' 0 회 · 'granular' 는 참고문헌 제목 둘) | 카드 §0-2 (i) | — | —
- [k] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions — Nairn & Guilkey 2015 | 대신 옛 MPM 의 한계: *"It has long been recognized that this original MPM (i.e., particles represented spatially as Dirac delta functions) has serious element crossing artifacts and should not be used."* (p.127) · *"No results for classic axisymmetric MPM shape functions are given, because they became unstable as many particles crossed element boundaries."* (p.141) · *"classic axisymmetric MPM methods are not robust"* (p.143) | p.127 · p.141 · p.143 | 인쇄 | MPM 쪽 한계 (k 의 DEM 한계 아님)

## l — 소성변형이 왜 어려운가
- [l] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions — Nairn & Guilkey 2015 (Int. J. Numer. Meth. Engng 101, 127–147) | 큰 변형의 어려움 = 변형한 입자 영역 위 적분: *"Although uGIMP explicitly evaluates S_ip, G_ip, and T_ip, it will lose accuracy as the actual particle domain deforms.  For example, large-deformation tension tests are limited to about 50% strain when using uGIMP.  The solution is to evaluate the integrals over the deformed particle domain.  Although this task is easy in 1D [11], it is very difficult in 2D or 3D."* | §2.2 · p.134 | 인쇄 | 연속체 MPM 의 수치 이유 (입자 = 물질점 · 알갱이 아님)
- [l] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions — Nairn & Guilkey 2015 | 우회 = CPDI (격자 함수를 평행사변형 네 모서리 값으로 보간 · 닫힌 꼴 식 35–39) · 축을 넘으면 자름 (uGIMP) / 줄임 (CPDI) · 회전이 크면 dF 의 k ≥ 2 항 (*"in problems involving rotation (less common in axisymmetry, but possible in penetration), the k = 2 or higher terms are needed"* p.129) | §2 · §2.2 · p.129 · p.134–136 | 인쇄 | 한계 = uGIMP 88 % · CPDI 약 93 % 압축 붕괴
- [l] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions — Nairn & Guilkey 2015 | 소성 계산 = 관통 하나 (텅스텐 · 강 둘 다 elastic-plastic · Johnson–Cook + Mie–Grüneisen) · **맞춘 값 0** (상수 = Anderson 외 [21] 의 값) · 검증 = 코 · 꼬리 위치 *"good agreement"* (차 코 −0.08…+0.05 · 꼬리 −0.11…+0.13 cm [판독] · 거의 같은 시각 두 실험점끼리 0.03–0.10 cm) · 격자 셀 0.25 mm · 셀당 4 입자 · 입자 ≈ 7 만 [카드 산술] · **계산 시간 · 비용 미인쇄** | §4.3 · Table I · Fig. 10 · p.144–145 | 인쇄 · [판독] · [카드 산술] | 동적 충돌 (1.70 km/s) · 금속

## m — 받아들일 통찰
- [m] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions | 무엇: **축대칭 판의 고칠 곳 목록 = 체크리스트 9 항** (질량 라디안당 · 축 노드 r 속도 0 · 자른 축대칭 형상 함수 + T_ip · 면적 기울기 접촉 법선 + 축 성분 0 + 노드 면적 두 배 · 후프 변형률 du_r/r · 구성식 후프 성분 · 견인 축대칭 꼴 / 입자 힘 라디안당 · 내부력 후프 항 · 축 넘김 정지) · 어디에: 단계 2 (U1 · U3 를 3D 회전체로 푸는 2D 판) · 왜: p.145 — 우리 MLS-MPM 부품마다 대응시켜 '바꿀 곳' 을 결과 전에 적는 틀 (MLS-MPM 의 축대칭 꼴은 이 논문에 없음)
- [m] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions | 무엇: **정확해 단위 시험 = 균일 반지름 압축** (z 구속 · F = diag(1 + ε, 1, 1 + ε) · Neo-Hookean 식 64–67 · J 16 % 에서 σ_rr = σ_θθ −12.0 · σ_zz +3.40 GPa [카드 산술]) + **축 근처 입자 J 균일성** (첫 입자가 평균선에서 벗어나는가 — 축 처리 오류는 여기서만 보인다) · 어디에: 단계 2 · U1 · 결과 전 대조 항목 (코드 검증) · 왜: Fig. 5 · 6 · 7 (축 첫 입자 6.52–23.33 % 로 갈림)
- [m] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions | 무엇: **하중을 어디에 거느냐의 함정** — 같은 1000 MPa 를 입자 힘으로 걸면 가장자리 입자 574.5 (≈ 안쪽의 0.48) · 안쪽 +15–20 % (처음 치수로 정한 힘 + Poisson 수축) ↔ 견인 (변 적분) 은 991.8–1004.1 MPa [판독] · 어디에: 후보 A′-0 (판 하중 · 판 근처 입자 응력 판독) · 왜: Fig. 8 · p.138 · p.144
- [m] nairn2015_mpm_axisymmetric_gimp_cpdi_shape_functions | 무엇: **스칼라 장은 노드 외삽이 아니라 비율로 갱신** (T_p += Δt Σ (dT_i/dt) S_ip · 외삽 = 수치 전도) · 구성식에는 노드에서 외삽한 값 (입자 값은 셀 안에서 요동) · 자리: 흐름 밖: 같은 MPM 위에서 열 · 농도 · 손상 같은 장을 함께 풀 때 · 왜: p.140

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드가 없는 것)
- [n] 12. Sulsky D, Schreyer HK. Axisymnmetric form of the material point method with applications to upsetting and Taylor impact problems. Computer Methods in Applied Mechanics and Engineering 1996; 139:409–429. (원문 참고문헌 12 · 인쇄 그대로) | g · l · f — 점 질량 축대칭 MPM 원전 · 원기둥 업세팅 (압축 큰 소성 변형) · 이 논문이 *"the first, and thus far, only"* 라 한 판 · 카드 §2 · §15 | litdb 확인: 파일 목록에 sulsky* 없음 · "Taylor impact" 는 인용 카드뿐 → 카드 없음 — ⚠ `wishlist.md` L196 에 이미 있음 (bardenhagen2004 카드에서 · 중복 표시)
- [n] 6. Lemiale V, Hurmane A, Nairn JA. Material point method simulation of equal channel angular pressing involving large plastic strain and contact through sharp corners. Computer Modeling in Engineering & Sciences 2010; 70(1):41–66. (원문 참고문헌 6 · 인쇄 그대로) | l · f — MPM 큰 소성 변형 + 날카로운 모서리 접촉 · 이 논문의 *"accurate determination of the normal is crucial to accurate contact simulations [6]"* 근거 (후보 A′ 법선) · 카드 §4-6 · §15 | litdb 확인: grep "Lemiale" · "equal channel angular" 0 건 → 카드 없음
- [n] 17. Nairn JA. Modeling of imperfect interfaces in the material point method using multimaterial methods. Computer Modeling in Engineering & Sciences 2013; 92(3):271–299. (원문 참고문헌 17 · 인쇄 그대로) | f · 흐름 밖 (계면 저항) — 다물질 MPM 의 불완전 계면 견인 법칙 · 축대칭 계면 넓이 유도가 여기 있다 (이 논문은 *"The development of these axisymmetric methods is given in [17]"*) · 카드 §4-6 · §15 | litdb 확인: grep "imperfect interface" 0 건 → 카드 없음
- [n] 4. Bardenhagen SG, Brackbill JU. Dynamic stress bridging in granular material. Journal of Applied Physics 1998; 83:5732–5740. (원문 참고문헌 4 · 인쇄 그대로) | d · f — 입상체 MPM 의 마찰 접촉 원전 하나 ([4–6]) · 응력 다리 · 카드 §15 | litdb 확인: grep "Dynamic stress bridging" 0 건 · bardenhagen 카드 넷 (2000 · 2001 · 2004 · 2005) 은 다른 논문 → 카드 없음
- [n] 9. Nairn JA. Material point method calculations with explicit cracks. Computer Modeling in Engineering & Sciences 2003; 4:649–664. (원문 참고문헌 9 · 인쇄 그대로) | R7 (AM 파괴) · f — CRAMP 원전 · 축대칭에서 그대로 쓰인다 (p.138) · `homel2017_…` 이 견준 명시 균열 MPM 계열 · 카드 §4-5 · §15 | litdb 확인: 파일 목록에 nairn* 은 이 카드뿐 · "explicit cracks" 는 homel2017 카드의 언급뿐 → 카드 없음
- (참고 · 후보로 세지 않음) [3] Sadeghirad 2011 = 정본 `sadeghirad2011_…` · [5] Bardenhagen 외 2001 = 정본 `bardenhagen2001_…` · [11] Bardenhagen–Kober 2004 = 정본 `bardenhagen2004_…` · [1] Sulsky 1994 = 후보 표 N-40 · [2] Sulsky 1995 = `wishlist.md` L195 · [21] Anderson 외 1995 (관통 실험 · 우리 질문 밖).

## 카드 문제
- `gritton2017_mpm_chemomechanical_coupling_silicon_anode` **L597** (§9 ⑩) · **L624** (§10 행동 4) — 값 · 서지 어긋남은 없다 ([41] = 이 논문 · '축대칭 MPM' 맞음).  다만 두 줄의 [카드 추론] (*"축대칭 MPM … 을 쓰면 2D 값을 3D 로 옮기는 문제의 일부가 사라진다"* · *"축대칭이면 구 하나 · 구–블록 문제가 그대로 3D 문제다"*) 에는 **한정어가 필요**하다: 기하 · 하중 · 경계 · 접촉이 모두 축대칭일 때만 · 축 r = 0 처리 (영역 자름 · 축 노드 · r 속도 0 · 축 넘김 정지) 를 전제로 · 이 논문은 구 · 구–블록 예제 · 3D 대조 · 비용을 싣지 않았다 (평면 형상 함수를 그대로 쓰면 축 첫 입자 J 23.33 % ↔ 16 % · Fig. 6).  고치지 않음.
- (참고 · 문제 아님) `gritton2017_…` L254 *"modeling heat diffusion [41–43]"* — 이 논문 §3.4 (식 56–62) 에 축대칭 GIMP 열 전도 · 확산 알고리즘이 있다 (계산 예는 없음) → 맞음.  L58 은 gritton 원문 문장 (이 논문과 무관) → 맞음.
- (참고 · 카드 아님) 후보 표 N-35 서지 *"Int. J. Numer. Methods Eng. 101 127–47"* (2015) = 원문과 같음 · 원문 안에서 연도 표기가 둘 (첫 쪽 머리글 2015 · 쪽마다 바닥글 2014 · 온라인 2014-10-01).
- (참고 · 문제 아님) `devaucorbeil2020_…` L46 · L56 · L61 · `homel2017_…` L267 · L458 · L617 의 'Nairn' 은 다른 Nairn 문헌 · 코드 이름 (NairnMPM) — 이 논문을 가리키지 않는다 (이 논문은 코드 이름을 인쇄하지 않는다).
- (관찰 · 원문 자체의 어긋남 — 카드 §12-C 에 기록) 식 (25) 적분 아래 끝 · p.132 윗첨자 (0) · 식 (28) x_p · 식 (31) Δr ↔ Δz · 식 (54)/(55) 부호 · 식 (57) 부호 · 식 (66)/(67) G₁ · 식 (A.2) 조건 · Fig. 1 '−2' · Fig. 2 · 3 캡션 'red' · Fig. 7 범위 (≈ 90.7 %) ↔ 본문 84 % · Fig. 5 ↔ 6 의 같은 이름 계열 끝 두 점 · 참고문헌 [12] 철자 · [1] 쪽 179–186 (bardenhagen2004 카드는 179–196) · [11] 쪽 477–496 (그 논문 머리글 495).
- (참고 · 카드 아님) `litdb/figures/_sources.json`: 이 배치의 `extract_figures.py` 가 다른 카드 줄 셋 (choi2018 · devasconcelos2019 · heenan2020) 을 바꿨으나 HEAD 값으로 되돌리고 이 카드 줄만 더했다 (batch 69 · 71 · 72 · 73 과 같은 현상).
- (참고) `bardenhagen2004_mpm_gimp_generalized_interpolation_cell_crossing` 의 §16 관련 카드에 이 카드를 가리키는 한 줄만 더했다 (다른 곳은 고치지 않음).

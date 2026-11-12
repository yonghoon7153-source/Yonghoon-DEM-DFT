# 배치 76 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-12)

카드 = `sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps` (원문 = 출판본 8 쪽 + ESI 16 쪽 · 그림 크롭 58 장 = 도구 23 (다시 자름 13) +
손 크롭 35 (패널 17 · 근거 문단 18 · 식 0 — 원문에 번호 식 · 인라인 식 없음) · 판독 원자료 `litdb/figures/<slug>/digitized.csv` 538 행).
서지 (k · l 인용용) = Sakka Y., Yamashige H., Watanabe A., Takeuchi A., Uesugi M., Uesugi K., Orikasa Y.,
*Pressure dependence on the three-dimensional structure of a composite electrode in an all-solid-state battery*, J. Mater. Chem. A 10 (2022) 16602–16609,
DOI 10.1039/D2TA02378D (CC BY 4.0).
⚠ 재료 = LiNbO₃ 코팅 NCM111 + **Li₁₀GeP₂S₁₂ (LGPS)** + 아세틸렌 블랙 (1 : 1 : 0.1 wt) — LPSCl · NCM811 아님 · DEM · MPM · 계산 없음.  쪽 = PDF 쪽 p.1–8 (인쇄 16601 + n) · ESI 는 "SI p.n".

---

## a — 순수 SE 압력별 기공 곡선 · 진밀도 · 상태

- [a] sakka2022_operando_xct_pressure_porosity_tortuosity_anisotropy_ncm111_lgps | 같은 셀의 **LGPS 층** (순수 황화물 SE · LPSCl 아님) 누른 채 CT 기공: 53.0 (0) · 40.9 (6) · 39.0 (12) · 15.0 (50) · 4.3 % (≈101 MPa) · 본문 *"5% at a pressure of 100 MPa"* | 카드 §3-3 표 · 그림 3a · p.4 | [판독] (본문 5 % = [인쇄]) | 기공 = CT 세 상 분할 (화소 ≈0.5 µm · 문턱 미기재) · **진밀도 · 질량 분모 없음** · 0.5 µm 아래 기공 미검출 (하한일 수 있음) · ≤ 100 MPa · 랩 표준 (10–13 % · 1.64) 과 다른 재료
- [a] sakka2022_… | 카드 산술 Heckel 꼴 (판독 기공 · 세 점 12 · 50 · 101 MPa): LGPS 층 K 0.0248 MPa⁻¹ · **P_y ≈ 40 MPa** (R² 1.000 · 다섯 점 41 · 본문 5 % 쓰면 43) | 카드 §3-3 | [카드 산술] | 원문은 Heckel 을 쓰지 않음 · LGPS · CT 분할 기공
- [a] sakka2022_… | 두께 자기 일관: SI S6 단면 두께 (500 µm 막대 환산) 의 LGPS 층 t₁₀₀/t₆ = 0.628 ↔ CT 기공이 주는 0.617 (2 % 안) · 그러나 절대 고체량은 진술 1.0 mg 의 ≈33 % 상당 | 카드 §3-3 | [카드 판독 · 카드 산술 · 가정 밀도 2.05] | 질량으로 기공을 다시 셀 수 없음

## b — 압력을 뺄 때 되돌아오는 양 · 잰 방법

- [b] sakka2022_… | 50 → 0 MPa (복합 양극 · 같은 셀로 읽힘): *"No clear changes were detected with respect to the void in the pressure-released condition"* — XY 단면 두 장 비교 (SI S14) · **숫자 (기공 · 두께 · 되돌아옴) 없음** · 100 MPa 탈압 없음 | 카드 §3-4 · p.4 · SI S14 | [인쇄] (정성) | 되돌아옴 측정 [미확인] · 단계 6 의 값 대조점 아님 (방향만)

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- [c] sakka2022_… | 항복 · 경도 · 크리프 값 없음 — 저자는 **영률** 로 설명 (*"NCM particles, which exhibits a high Young's modulus (ref 37)"* · *"LGPS with a smaller grain size and Young's modulus can fill the voids"* p.4) · 카드 산술 겉보기 Heckel P_y: LGPS 층 ≈40 MPa · 복합 양극 ≈168 MPa (×4) | 카드 §3-3 · p.4 | [인쇄] · [카드 산술] | 일축 항복 환산 없음 · 분말층 겉보기 값 (재료 항복 아님) · LGPS

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

- [d] sakka2022_… | 하중 몫 값 없음 · 정성 기전: *"uniaxial pressing preferentially pushes the NCM particles, owing to their large Young's modulus, the pressure of the flat current collector is not sufficiently applied to the space between the AM particles when the AMs are dense. Therefore, low-pressure spots are created in the gaps in the AM, and thus the SE does not fill these gaps"* · *"Since no force is applied from the horizontal direction, the gap cannot be fully filled"* | 카드 §4-2 · p.6 · 그림 7 | [인쇄] | 하중 분담 측정 · 계산 없음 (R1 의 실험 쪽 정성 진술)
- [d] sakka2022_… | 같은 셀 · 같은 압력의 대조: ≤ 12 MPa 에선 복합 ≈ SE 층 (39 ↔ 39 %) · 100 MPa 에서 **22.9 ↔ 4.3 %** · ≤ 12 MPa 에서 NCM 부피 몫 18 → 30 % (재배열) · > 12 MPa 에서 LGPS 몫 31 → 44 % (두 단계) · 접촉 분율 50 MPa 에서 멈춤 | 카드 §3-3 · §3-4 · 그림 3 | [인쇄 3b] · [판독 3a · 3c] | LGPS · NCM111 · SE ≈65 vol% (카드 산술) — 우리 SE ≈26 vol% 와 조성이 다름 · ⚠ 분할 LGPS/NCM 부피비가 2.11 → 1.03–1.41 로 흔들림 (명목 2.29)

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안

이 배치에 없음 (접촉 법칙 · DEM 없음).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙

이 배치에 없음 (MPM 없음).  (해상도 쪽 측정 교훈은 m 의 넷째 · 카드 §8 U1 · U6.)

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거

- [g] sakka2022_… | 2D → 3D 진술 없음 · 이방성은 2D 단면 (XY · YZ · XZ) 과 3D 렌더를 눈으로 본 판단 · 카드 판독 (SI S13 XZ 단면 한 장) 의 녹색 몫 0.80–0.91 은 3D 값 (그림 3c 74.9–84.3 %) 보다 3–7 %p 높지만 압력 순서 (50 > 100 > 0 ≈ 12 > 6) 가 같다 | 카드 §3-5 | [카드 판독] · [판독] | 한 단면 · 그림 화소 — 원문의 양이 아님

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공

- [i] sakka2022_… | NCM111-LiNbO₃ + LGPS + AB (1 : 1 : 0.1 wt) · **누른 채** · 0 · 6 · 12 · 50 · 100 MPa → **44 · 42 · 39 · 31 · 23 %** (표지 판독 44.2 · 42.3 · ≈39 · 30.6 · 22.9) · 부피 NCM / LGPS 18/38 · 25/33 · 30/31 · 29/41 · 33/44 % | 카드 §3-3 · 그림 3a · 3b · p.4 | [인쇄 3b] · [판독 3a] | CT 분할 (512 × 512 × 50 µm³ 하나 · 분모 = 영상 부피 · AB 분류 미기재) · LGPS · ≤ 100 MPa · 정본에서 **누른 채 CT 복합 양극 압력별 곡선** 의 첫 카드
- [i] sakka2022_… | 두께 자기 일관: SI S6 양극 두께 388 · 345 · 298 · 291 µm (6 · 12 · 50 · 100 MPa · ±10 %) → t₁₀₀/t₆ 0.750 ↔ CT 기공이 주는 0.748 · 절대 고체량 = 진술 1.0 mg 의 ≈47 % 상당 · 층 경계 그릇 모양 (가운데 ≈1.4–1.5 × 가장자리) | 카드 §3-3 | [카드 판독 · 카드 산술 · 가정 밀도] | 진술 질량이 CT 셀에 그대로 들어갔다고 볼 수 없음 · 지름 1 mm 벽 효과

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것

- [j] sakka2022_… | 저자 한계: 적재 60 mg cm⁻² (1 mm 지름 · 저울 한계) · 두꺼운 전극 불균일 반응 · LGPS 첫 충전 분해 · tortuosity 는 상대 비교만 (문헌 1–10) · LFP 나노 공극은 CT 해상도로 못 셈 · τ 증가 영향은 작을 것 | 카드 §3-9 1–4 · p.2–6 | [인쇄] | 탈압 · 유지 시간 · 반복 · 분할 문턱 없음
- [j] sakka2022_… | 카드가 본 원문 안 어긋남: 분할 조성비 · 질량 ↔ 두께 · R_ct (그림 6b) ↔ S15 보이는 반원 (50 · 100 MPa ≈3 배) · S3b 계산 규칙 재현 안 됨 · 그림 번호 둘 (*"Fig. 3b"* → 3c · *"(Fig. 1)"* → 그림 2) · 결론의 "vertical" 낱말 | 카드 §3-9 5–13 | [카드 산술] · [카드 해석] | 기공 · R_ct 절대값 인용 시 한정어 필수

## k — DEM 의 한계 (원문 문장 · 위치)

- [k] sakka2022_… (Sakka et al., J. Mater. Chem. A 10 (2022) 16602) | **말 없음** — DEM · 입자 계산 · discrete element 낱말 0 회.  가까운 문장 (모델 아님): *"The volume ratio of NCM and LGPS does not follow the relative modulus because the direction of pressure is in one direction, and the particle size and shape are also different between NCM and LGPS."* (p.4) | 카드 §4-3 1 | [인쇄] | 단단한 구 · 점접촉의 한계에 대한 진술 아님

## l — 소성변형이 왜 어려운가 · 우회 · 값

- [l] sakka2022_… (Sakka et al., J. Mater. Chem. A 10 (2022) 16602) | 계산 없음 → 어려운 이유 · 우회 · 비용 말 없음.  재료 쪽 문장: *"During electrode fabrication, high pressure is applied to improve solid-to-solid contact between powders, which involves plastic deformation within composite electrodes."* (p.1) · *"Hard NCM particles are slightly deformed by applied pressure"* (p.4) · *"Since no force is applied from the horizontal direction, the gap cannot be fully filled. In addition, even where the AMs overlap, the SEs cannot be filled and the voids remain."* (p.6) | 카드 §4-3 2 · p.1 · p.4 · p.6 | [인쇄] | 맞춘 값 0 개 · 일축 가압 + 단단한 AM 에서 소성 SE 가 AM 옆 틈에 못 들어간다는 정성 기전 (R1 · R6)

## m — 받아들일 통찰

- [m] sakka2022_… | **누른 채 단계 CT + 같은 셀 EIS + 두께로 자기 일관 확인** — 같은 셀을 0 → 100 MPa 로 누르며 CT 기공 · 접촉 분율 · R_ct 를 같은 자리에서 잼 (그림 1) · 카드가 단면 두께 비로 CT 기공 변화를 2 % 안에서 확인 · 절대 질량은 안 맞음 → 문헌 기공 인용 칸에 "두께 자기 일관 확인 여부" 를 더함 | 단계 0 · 단계 6 (실험 대조 설계) | 카드 §3-3 · §9 3 · p.2
- [m] sakka2022_… | **방향별 접촉 관측량** — AM 표면 법선 |n_z| 칸별 SE 피복 (Z 면 ↔ 옆면) 을 DEM · MPM 공통으로 정의 · 결과 전에 "Z 면 > 옆면" (카드 S13 판독 0.89–0.96 ↔ 0.65–0.85 · 원문 정성) 을 적고 본다 | 후보 D0 · 단계 3 · 단계 5 | 카드 §3-5 · §8 · §9 2
- [m] sakka2022_… | **같은 압력에서 복합 ↔ SE 단독층 기공 비교** 가 AM 하중 차폐 (R1) 의 실험 쪽 방향 지표 — LGPS 계 100 MPa 22.9 ↔ 4.3 % · 겉보기 P_y ≈168 ↔ 40 MPa (카드 산술) | 결과 전 대조 항목 · 후보 A · A′ · 후보 M0 | 카드 §3-3 · §8
- [m] sakka2022_… | **함정 · 보고 방식**: tortuosity 를 분포 (N = 100 경로) 로 내고 최소 · 최빈 · 평균 · 퍼짐을 따로 보면 100 MPa 에서 최소는 그대로 (2.45 → 2.75) 인데 평균 · 퍼짐이 오른다 · 단 영역 하나 (36 × 36 × 50 µm³ = NCM 3–4 개 폭) 라 표본 차이를 배제 못 함 · 기하 τ 를 τ_Laplace 와 섞지 말 것 (비교 문서 2 차 인용의 함정) | 단계 7 · 흐름 밖: 우리 τ_geo 보고 꼴 | 카드 §3-6 · §0-1

## n — 논문 에이전트 후보

- [n] A. Ohashi, M. Kodama, N. Horikawa and S. Hirai, J. Power Sources, 2021, 483, 229212. | d · i — *"In composites with different Young's moduli, large pressures can be applied to materials that have larger Young's moduli"* 의 근거 (단단한 AM 하중 몫) · 카드 §12 ref 25 | litdb 확인: papers/ ls · grep "Ohashi" · "229212" → 카드 없음 (heck2026 · kodama2020 카드에 같은 그룹 다른 논문 언급만)
- [n] A. Ohashi, M. Kodama, X. Y. Sun, S. Hori, K. Suzuki, R. Kanno and S. Hirai, J. Power Sources, 2020, 470, 228437. | d · i — *"the NCM particles are pressurised preferentially"* · *"strain caused by the pressure reduces the contact between the AM and SE"* 의 근거 · 카드 §12 ref 24 | litdb 확인: grep "228437" → heck2026 참고문헌 표에 서지만 (카드 없음)
- [n] E. J. Cheng, K. Hong, N. J. Taylor, H. Choe, J. Wolfenstine and J. Sakamoto, J. Eur. Ceram. Soc., 2017, 37, 3213–3217. | c — NCM 의 *"high Young's modulus"* 근거 (NCM111 기계 물성) · 카드 §12 ref 37 | litdb 확인: grep "3213" · "J. Eur. Ceram" · "Wolfenstine" → 이 논문 카드 없음
- [n] H. Fathiannasab, L. K. Zhu and Z. W. Chen, J. Power Sources, 2021, 483, 229028. | i · d — 가압 변형 ↔ AM–SE 접촉 · AM/SE CT 구조 분석 · 카드 §12 ref 18 | litdb 확인: grep "Fathiannasab" · "229028" → so2021_dem_fabrication_degradation_ductile_particles 가 "Fathiannasab synchrotron [14]" 로 언급만 (어느 Fathiannasab 논문인지 그 카드 줄로는 모름) · 카드 없음
- [n] A. Neumann, S. Randau, K. Becker-Steinberger, T. Danner, S. Hein, Z. Y. Ning, J. Marrow, F. H. Richter, J. Janek and A. Latz, ACS Appl. Mater. Interfaces, 2020, 12, 9277–9291. | h · m — CT 구조 + 시뮬레이션 (불균일 충방전) · tortuosity 1–10 문헌 · 카드 §12 ref 34 | litdb 확인: ls "neumann*" = neumann2021 (garnet · 다른 논문) 뿐 · grep "9277" → 카드 없음

## 카드 문제

- `tailored_cathode_microstructure_low_pressure_assb` L78: 저자 표기 *"Sakka(Sakuda) et al."* — 1저자는 Yuya Sakka (교신 Orikasa · Ritsumeikan) · Sakuda 는 다른 연구자.  같은 줄 *"모델 연구는 25 MPa면 안정 계면접촉에 충분(ref 12 모델)"* — Sakka 2022 에 모델 · 25 MPa 진술 없음 (다른 문헌이 섞인 것으로 보임).  고치지 않음 · 그 카드에 관련 카드 한 줄만 더함.
- comparison_vs_ours_DEM.md L456–458: *"R_ct+R_bulk 동시↓"* 의 R_bulk 는 원문 양이 아님 (겉보기 전도도 +24 %) · *"실접촉면적"* 은 분율 · *"τ_Laplace 이방성 검증거리"* — 원문 τ 는 Z 방향 기하 경로 하나 (옆 방향 · Laplace τ 없음).  옛 줄은 그대로 두고 [151] 을 1 차 카드로 잇고 원문 대조 한 줄을 보탬.
- comparison_vs_ours_DEM.md L450: 리뷰 카드 경로 papers/li2026_sulfide_stability_review_ecer.md — 정본 papers/ 에 그 파일 없음 (정본 = `fan2026_sulfide_assb_stability_review_ECERD2600097`) · 고치지 않음.
- (원문 문제 · 이 카드 §3-9 에 기록) Sakka 2022 본문의 그림 번호 둘 (p.5 *"Fig. 3b"* = 3c · *"(Fig. 1)"* = 그림 2) · 분할 조성비 흔들림 · 진술 질량 ↔ 단면 두께 · R_ct ↔ S15 반원 폭 · S3b 계산 규칙 재현 안 됨.

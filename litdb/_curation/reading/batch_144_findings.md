# batch 144 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-23 · U-1123-1)

대상: `sun2026_fff_printing_extruded_filament_sph_dry_electrode_preprint` — P. Sun · F. Fernandez · P. Vigneaux\* · A. A. Franco\*, "Microstructure-resolved modeling of fused filament fabrication of lithium-ion battery electrodes", ChemRxiv (2026) · **동료 심사 전 원고** · DOI 10.26434/chemrxiv.15012329/v1 (43 쪽 = ChemRxiv 표지 2 + 원고 41 · SI 미포함).
같은 그룹의 압출 DEM 필라멘트 (마지막 6 프레임 · 990 µm · ≈30,000 입자) 를 LAMMPS RHEO 입자 모델 (SPH 점성 유체 BC + 고체 구 AM + 가정 냉각 상태 · BC 결합) 의 공급 원료로 써서 FFF 노즐 흐름 · 퇴적 · 고화를 3D 로 모사 (한 가닥 17 · 한 층 9 · 두 층 18) 하고, 두 층 전극을 0.5 µm 복셀 FVM 으로 확산 · 전자 전도까지 본 방법 원고 — 실험 대조 · 압력 없음.
쪽 = 받은 PDF 쪽 (p.1–2 ChemRxiv 표지 · p.3–43 원고 · 원고 자체 쪽 번호 없음) · 판독 원자료 = `litdb/figures/sun2026_fff_printing_extruded_filament_sph_dry_electrode_preprint/digitized.csv` (90 행 · 원 래스터 화소 · 인쇄 범위로 검산) · 고른 의도 대조 = **일부** (카드 §0-1 — 앞 압출 DEM 의 다음 단계 = 채움 · 같은 필라멘트 = 일부 · 같은 DEM 설정 = 없음).
인용 서지 (질문 k · l 용): Sun, Fernandez, Vigneaux, Franco, ChemRxiv (2026) preprint, doi:10.26434/chemrxiv.15012329/v1.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 고체전해질 없음 (액체 LIB LFP 양극 FFF 인쇄 · 압력 없음).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 가압 · 탈압 없음. 가장 가까운 것 = 공급 중단 → 노즐 25 µm 후퇴 (1500 µs) → 잔여 물질 기하 제거 → 균일 냉각 이완 (카드 §4-5 (iv) · p.13 · p.17) — 되돌아옴 숫자 없음.

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 항복 · 경도 · 크리프 없음 (BC 는 점성 유체 · η = η₀(1 + 9s) · η₀ = 0.01 Pa s 가정 (p.14) · AM 은 고체 구 · 일축 항복 환산 없음).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 압력 · 하중 몫 없음 (AM 은 유체 BC 안에서 재배열 · 뭉침 · 분리 — A12 위 모습 정성 · p.23).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] sun2026_fff_… | 점접촉 법칙 대안이 아니라 **무른 상 (BC) 을 SPH 점성 유체로** 바꿔 큰 변형을 피한다 — 유체 상호작용은 쌍의 하나라도 유체일 때 · 고체 접촉 (AM–AM · AM–기판 = 짧은 거리 탄성 반발 + 법선 감쇠 · 계수 SI 표 S2 [미확인]) 과 결합은 따로 더함 (p.10–11) · 고화 = 상태 점도 (최대 10 배) + 결합 (k 2 pg µs⁻² · γ 10 pg µs⁻¹ · 끊김 변형률 0.25) · 맞춘 값 0 | 카드 §3-1 · §4-2 · §4-3 | 인쇄 | 압력 · 고체 소성 없음 · 접촉 계수 SI

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
- [f] sun2026_fff_… | (MPM 아님 · SPH 혼성) 해상도 꼴: 차단 거리 11.775 µm = 5 r_BC · AM 반지름 5 µm = 2.12 r_BC [카드 산술] · Δt 0.005 µs · c_s 8 µm µs⁻¹ (V_p/c_s 0.010–0.015 [카드 산술]) · BC 밀도 편차 5 % 넘으면 런 중단 (p.16) · 수송 복셀 0.5 µm = AM 지름당 20 · BC 지름당 9.4 복셀 [카드 산술] · **해상도 · 커널 · 복셀 수렴 시험 0 · 반복 런 0** (오차 막대 = 단면 사이 공간 SD) | 카드 §3-1 · §4-4 · §6 | 인쇄 + 카드 산술 | 수치 오차 추정 없음

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 인쇄 · 분석 모두 3D · 2D 는 관련 연구 한 줄 (Yang 등 [28] *"two-dimensional, isothermal model"* · p.7) · 전이 진술 없음.

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
- [h] sun2026_fff_… | **DEM (압출) → SPH 입자 모델 (RHEO)** 넘김 — 넘긴 시점 = 압출 DEM 출구의 마지막 6 프레임 (각 165 µm · 합 990 µm · ≈30,000 물질 입자) · 이음매만 국소 이완해 *"preserving particle number, phase, radius, and source identity"* (p.9) · 압출 축 → 공급 축 Y · 경로가 길면 처음으로 돌아가 다시 공급 (입자마다 바퀴 번호) · 넘기면서 BC 표현을 DEM 구 (반지름 2.5 µm · sun2026_dem_extrusion 카드 §3 (나)) → SPH 유체 (외피 2.355 µm) 로 바꿈 · 출처 모델이 원문 안에서 어긋남 (방법 절 [36] Paredes-Goyes 2024 ↔ 초록 *"our previously developed twin-screw extrusion model"* = [37]) · 넘김 식 · 수리 규칙 · 허용치 = SI 절 S1 [미확인] | 카드 §0-1 · §4-1 · `txt_p9_feedstock_six_segments_990um_30000_particles.png` | 인쇄 | 압력 · 소성 없는 공정 · 연속체 쪽은 FE/MPM 이 아니라 SPH

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — 압력 없음 · SE 없음 (FFF 두 층 빈 곳 ε_v 38.59–40.15 % · ε_tot 42.83–44.29 % = 무압 · 분모 = 탐침 외피 + 틈 채움 영역 V_Ω · 랩 표준과 다른 문헌 값으로도 견줄 수 없음 · 카드 §7-2).

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압 계산과 닿는 것)
- [j] sun2026_fff_… | 원문 한계: *"Experimental validation remains necessary before these predictions can be quantitatively applied to printed electrode structures and their transport properties."* (p.27) · BC 나노 공극 10 % *"without experimental calibration"* (p.35) · *"The quantitative rankings remain conditional on the reconstructed envelope, voxel resolution, assigned phase properties and ideal surface-following contacts."* (p.35) · 결과 = *"candidates for further evaluation rather than battery-level performance rankings"* (p.35) · 수치 중단 = *"a numerical limitation, without establishing physical unprintability"* (p.16) | 카드 §0 ⑩ · §11 | 인쇄 | 가압 · 탈압과 직접 닿는 것은 없음 (압력 없는 공정)
- [j] sun2026_fff_… | 카드가 적은 원문 공백: SI 미포함 (접촉 계수 · 경우별 설정 표 S1(a–c) · 두 층 경로 S4 · 넘김 식 S1 · 추가 결과 S5 · 동영상) · 해상도 · 반복 0 · 서론이 약속한 기술자 (입자 분포 · 가닥 안 공극 · 연결성) 일부 결과 없음 · 식 14 · 16 · 19 · 20 인쇄 깨짐 · 그림 4g 가 쪽 clip 밖 · 노즐 간격 30 (p.16) ↔ 35 µm (p.17 · p.25 · p.28) | 카드 §11 · [미확인] 목록 | 카드 서술 | —

## k — DEM 의 한계 (서지: Sun, Fernandez, Vigneaux, Franco, ChemRxiv (2026) preprint)
- [k] sun2026_fff_… (Sun 2026 · ChemRxiv 원고) | **말 없음** — 인쇄 단계는 DEM 이 아니다 (SPH + 고체 구 · 'LIGGGHTS' · 'Hertz' 낱말 0 회) · 앞 DEM 연구에 대해서는 범위만 말한다: *"these existing extrusion studies have not yet investigated the processes of particle rearrangement and structural reconstruction resulting from the following 3D printing"* (p.8 · 단 인용 번호는 압출이 아닌 [34,35] = Lombardo 2021 건조 · Ngandjong 2021 캘린더링) · 연속체 쪽 한계 문장은 있다: *"When the deposited composite is represented as an effective continuum medium, however, the redistribution of its individual constituents is not explicitly resolved."* (p.7) · DEM 구 → SPH 유체로 바꾼 이유 진술 없음 | 카드 §4-5 (i) | 인쇄 | DEM 한계 진술 아님 (연속체 · 범위 진술)

## l — 소성변형이 왜 어려운가 · 우회 (서지: Sun, Fernandez, Vigneaux, Franco, ChemRxiv (2026) preprint)
- [l] sun2026_fff_… (Sun 2026 · ChemRxiv 원고) | **어려운 이유는 말하지 않는다 · 우회 = 무른 상을 SPH 점성 유체로 · 단단한 상은 고체 구 (모양 변화 · 파쇄 없음)** · 고화 = 가정 냉각 상태 θ (*"an assumed cooling rule rather than a temperature calculated from the energy conservation"* p.13) → 점도 최대 10 배 + BC–BC / BC–AM 결합 (*"not calibrated against electrical contact resistance or macroscopic mechanical strength"* p.15) · *"The model omitted explicit surface tension, a prescribed contact angle and a calibrated shear-rate-dependent rheological law."* (p.12) · 맞춘 값 0 · 비용 64 CPU 코어 · 한 가닥 16–24 h · 두 층 인쇄 + 냉각 1–2 일 (p.17) · 공급 원료 ≈30,000 입자 (p.9) | 카드 §3-1 · §4-3 · §4-5 (ii) | 인쇄 | 압력 · 고체 소성 없음

## m — 받아들일 통찰
- [m] sun2026_fff_… | **DEM 출력을 다음 모델로 넘길 때 보존 항목을 이름으로 적는다** — 입자 수 · 상 · 반지름 · 출처 번호 (*"preserving particle number, phase, radius, and source identity"* p.9) + 이음매만 국소 이완 + 순환 공급이면 바퀴 번호 → 우리 DEM → MPM scaffold 넘김 (흐름 밖: Ⓑ 연계 · 입자 번호 승계 · 피복 설계 메모 §4 의 '번호 하나') 등록 문서에 같은 칸 | 자리: 흐름 밖 (Ⓑ 연계) · 단계 0 | 카드 §9-1
- [m] sun2026_fff_… | **부피 규약 둘을 목적별로** — 기준 부피 합 = 공급 · 유량 회계 / 외피 합집합 = 기하 (겹침 한 번) 를 원문이 처음부터 나눈다 (p.10) · 빈 곳도 분해 몫 ε_v 와 가정 몫 (ε_tot − ε_v = 0.1 φ_BC) 을 다른 열로 (p.20) → 우리 ε_sphere ↔ ε_union (관례 오프셋 1.251 %p 사건) 을 단계 0 연산자 등록에 함께 적는 근거 | 자리: 단계 0 | 카드 §7-1 · §8
- [m] sun2026_fff_… | **이완 끝 판정에 접촉 집합 변화율** — 최대 θ ≤ 0.01 · rms 속도 ≤ 10⁻⁴ · 최대 속도 ≤ 10⁻³ µm µs⁻¹ · 구간 최대 변위 ≤ 0.1 µm · 결합 집합 대칭차 비 f_E ≤ 10⁻³ (식 16 · 0 ≤ f_E ≤ 2) 를 연속 3 구간 (500 µs) 만족할 때 끝 (p.17) → 우리 고정 이완 · 언로딩 런의 '언제 끝인가' 판정 후보 (U3 · U4 의 끝 조건) | 자리: 단계 6 | 카드 §8 · §9-3
- [m] sun2026_fff_… | **σ 순위와 R 순위가 갈린다 — σ 옆에 정규화 기하를 적는다** — σ_Y,app = G·L_Y/A_Y (상자 높이 · 투영 면적) · R_Y = 1/G (p.21–22) 에서 X04-75 가 σ 최고 (0.1912 S/m) 인데 R 최저는 U07-85 (4.30 kΩ) · λ ↑ 에서 R 은 아홉 짝 모두 줄지만 σ 는 넷만 오른다 (p.35) · L/A 668–1603 m⁻¹ (2.4 배) · '같은 ε · τ 인데 σ 1.92 배' 의 1.21 배가 L/A [그림 8b 판독 · 카드 산술] → 망 σ · STEP3 σ 인계에 σ basis (판 간격 ↔ L_mc · 면적) 표지 | 자리: 단계 7 · 흐름 밖 (LHS · 망 σ 인계) | 카드 §3-5 · §7-3

## n — 논문 에이전트 후보 (카드가 인용 · 언급했지만 litdb 에 카드가 없는 것)
- [n] B. Paredes‐Goyes, F.M. Zanotto, V. Boudeville, S. Grugeon, L. Dupont, A.A. Franco, Mesoscopic Model of Extrusion during Solvent‐Free Lithium‐ion Battery Electrode Manufacturing, Batteries & Supercaps (2024) e202300441. https://doi.org/10.1002/batt.202300441. (원문 참고 [36] 그대로) | h · m — 이 원고 방법 절이 필라멘트 출처로 단 DEM (카드 §0-1 '일부') · 두 압출 DEM 의 입자 크기 · 밀도 (sun2026_dem_extrusion 카드 §2 '전작 그대로 계승' ↔ 이 원고 ρ_AM 2.71) 를 원문으로 가른다 — 카드 §0-1 · §12 | papers/ 목록 (paredes* 없음) · '202300441' grep = sun2026_dem_extrusion (인용만) · 'Paredes' grep = 인용 카드 셋
- [n] E.T. Palermo, K.T. Wolf, J.T. Clemmer, T.C. O'Connor, Reproducing hydrodynamics and elastic objects: A hybrid mesh-free model framework for dynamic multi-phase flows, Physics of Fluids 36 (2024) 113337. https://doi.org/10.1063/5.0228823. (원문 참고 [31] 그대로) | f · 후보 A (meshfree 판) — RHEO 원전 (재생 커널 SPH + 결합 입자 · 냉각 · 고화 시연) · 이 원고의 상태식 · 커널 · 밀도 확산 · 결합의 원 정의와 검증 — 카드 §4-2 · §12 | papers/ 목록 (palermo* 없음) · '113337' · 'Palermo' grep 0
- [n] M.F. Lagadec, R. Zahn, S. Müller, V. Wood, Topological and network analysis of lithium ion battery components: the importance of pore space connectivity for cell operation, Energy Environ. Sci. 11 (2018) 3194–3200. https://doi.org/10.1039/c8ee00875b. (원문 참고 [43] 그대로) | m · 단계 7 — 기공률 · 두께 방향 tortuosity factor 로 안 잡히는 기공 연결 (이 원고 p.33 근거) · 정본 다섯 카드가 인용만 — 카드 §3-4 | papers/ 목록 (lagadec* 없음) · 'Lagadec' grep = 인용 카드 다섯
- [n] S. Pinilla, F.M. Zanotto, D.Z. Dominguez, T. García, A.A. Franco, Carbon-binder-domain porosity extraction through lithium-ion battery electrode impedance data, Energy Storage Materials 74 (2025) 103818. https://doi.org/10.1016/j.ensm.2024.103818. (원문 참고 [46] 그대로) | m · 흐름 밖 (J 축 · B 축) — 이 원고가 가정한 BC 나노 공극 10 % 를 EIS 로 정하는 방법 · 해상 안 되는 상 안 공극이 tau2 를 바꾸는 크기 (p.35) — 카드 §11 · §12 | papers/ 목록 (pinilla* 없음) · '103818' grep 0
- [n] P. Sun, F. Fernandez, D.E. Galvez-Aranda, J.-P. Chehab, P. Vigneaux, A.A. Franco, Machine learning surrogate modeling of materials extrusion for lithium-ion battery electrode dry manufacturing, Energy Storage Materials 91 (2026) 105437. https://doi.org/10.1016/j.ensm.2026.105437. (원문 참고 [38] 그대로) | 흐름 밖 (LHS → ML 인계) — 압출 DEM 기술자의 대리 모델 · 역설계 (같은 그룹 · *"enabling rapid exploration and inverse design of extrusion-induced microstructural descriptors"* p.8) — 우리 LHS 기술자 → ML 인계와 같은 꼴 — 카드 §12 | papers/ 목록 (sun2026_* 셋 = 이 논문 아님) · '105437' grep 0

## 카드 문제
- 없음 — 후보 표 행이 아니라 가리킨 카드 (근거 칸) 가 없다 · 정본에 이 원고를 인용한 카드 없음 (DOI '15012329' · 'fused filament' grep 0).
- 서지 대조: 지시서의 서지 (저자 넷 · 제목 · ChemRxiv · 17 November 2026 · DOI · 43 쪽) = 원문 p.1 · p.3 과 같다 · **43 쪽에 SI 는 없다** (표지 2 + 원고 41 · 본문이 가리키는 SI 절 S1 · S4 · S5 · 표 S1 · S2 · S4 · 동영상 미포함).
- 이웃 카드 서지 차이 (카드 문제 아님): `sun2026_dem_extrusion_recirculation_dry_electrode` 의 서지 *"Batteries & Supercaps 2026, 9, e202500211"* ↔ 이 원고 ref [37] *"Batteries & Supercaps (2025) 2500211"* = 조기 공개 연도 ↔ 권호 연도.
- 보탤 정보 (그 카드는 고치지 않음): `sun2026_dem_extrusion_…` L41 *"입자 크기·밀도·복원계수·마찰·구름마찰은 전작 그대로 계승"* + L118 역산 ρ_AM ≈3.51 g cm⁻³ [DERIVED] ↔ 이 원고 (같은 그룹 · 방법 절 필라멘트 출처 = 그 '전작' [36]) 인쇄 ρ₀,AM 2.71 · ρ₀,BC 1.1 pg µm⁻³ (p.10) — AM 밀도 23 % 차 [카드 산술: 2.71/3.51 = 0.772] · 넘어온 것은 배치 · 상 · 반지름 · 출처 번호뿐이라 어느 쪽이 DEM 의 값인지 이 원고로 못 가린다 (질문 n 의 Paredes-Goyes 원문으로 가른다).
- 보탤 정보: `benhadjali2026_fully_coupled_chemomech_stress_3d_assb_cathode` L9 은 출판본 서지 (ESM 90 (2026) 105304 · 10.1016/j.ensm.2026.105304) 를 '이 PDF 로 확인 안 됨' (후보 표 · 그 카드 L443 의 2 차 서지) 으로 적는다 — 이 원고 ref [50] 이 같은 제목 · 저자 일곱 · *"Energy Storage Materials 90 (2026) 105304. https://doi.org/10.1016/j.ensm.2026.105304."* 로 적는다 (독립 2 차 서지 하나 더 · 원문 확인은 아님).
- 원문 자체 어긋남 (카드 문제 아님 · 카드 §11 에 적음): 필라멘트 출처 [36] (방법 절) ↔ 초록 'twin-screw' (= [37]) · 노즐 간격 30 (p.16) ↔ 35 µm · *"the four conditions are mentioned above"* ↔ 다섯 조건 (p.17) · 그림 4g 가 쪽 clip 밖 (캡션 (a)–(f)) · 식 14 · 16 · 19 · 20 · 4 · 22 인쇄 깨짐 · 그림 1 'Effective ionic conductivity' 미계산 · 서론 약속 기술자 일부 결과 없음 · 문장 반복 두 곳 (p.30 · p.34) · 그림 3c 제목 *"Mean heigh measurementst"*.

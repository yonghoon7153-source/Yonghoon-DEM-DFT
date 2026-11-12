# 배치 50 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-12)

카드 = `park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics` (원문 = 출판본 8 쪽 + SI 5 쪽 · 그림 크롭 56 장 = 도구 10 (전부 그대로 · 캡션 5 고침) +
손 크롭 46 (그래픽 초록 1 · 패널 19 · 식 2 · 근거 문단 24 · 본 뒤 다시 렌더 24) · 판독 원자료 `litdb/figures/<slug>/digitized.csv` 584 행 — 그림 1 · 2d–e · 3g–h · 5g · SI S1 은 벡터 경로 판독).
서지 (k · l 인용용) = Park S. H., Naik K. G., Vishnugopi B. S., Xiao X., Drakopoulos M., Vo N. T., Zhong Z., Mukherjee P. P., Hatzell K. B.,
*Chemo-Mechanical Behavior and Stability of High-Loading Cathodes in Solid-State Batteries*, ACS Nano 19 (24), 22262–22269 (2025), DOI 10.1021/acsnano.5c04431.
⚠ 재료 = LiNbO₃ 코팅 NCM811 + Li₆PS₅Cl (NEI) + Super C65 (100 : 3) · NCM : LPSCl 질량비 70:30 · 80:20 · 85:15 — 계는 우리와 같지만 **연산자 (XCT 분할 · 기공망) · 조성 표 · 상태 (300 MPa 조립 뒤 · 촬영 압력 미인쇄)** 가 다르다 · DEM · 압밀 시뮬레이션 없음 · 응력은 2D 선형 탄성.
쪽 = PDF 쪽 (인쇄 쪽 = 22261 + n) · SI 는 SI PDF 쪽 (SI p.1 = 표지).

---

## a — 순수 SE 압력별 기공 곡선 · 진밀도 · 상태

- [a] park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics | **없음** — 순수 SE 기공 · 밀도 없음 (SE 층 = LPSCl 80 mg · 지름 10 mm · 80 MPa 펠릿, 밀도 미기재) · 진밀도 (NCM811 · LPSCl · C65) 미인쇄 | 카드 §3-1 · §13 · 원문 p.7 | [인쇄] · [미확인] | 복합 양극만

## b — 압력을 뺄 때 되돌아오는 양 · 잰 방법

- [b] park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics | **없음** — 셀 전체 300 MPa 2 분 조립 → 운전 적층압 50 MPa 사이의 탈압 · 되돌아옴 · 기공 · 접촉 변화를 재지도 계산하지도 않았다 · 모델은 방전 0 % 를 무응력으로 두고 압밀 이력이 없다 (SI 그림 S2) | 카드 §4-4 · §3-4 · 원문 p.7 · SI p.3 | [인쇄] | 탈압은 [미확인]

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- [c] park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics | **항복 · 경도 · 크리프 없음** — 모델 탄성 입력만 (표 1): E_SE **22 GPa** (표 1 = ref 30 Singh 2022 · 서론 p.1 = ref 16 Deng 2016 — 같은 값 출처 둘) · ν_SE **0.27** (출처 없음 · Deng 2016 의 LPSCl ν 0.37 [다른 카드 `deng2016_…` 표 III]) · E_AM **200 GPa** (ref 17) · ν_AM 0.3 · Ω 2 × 10⁻⁶ m³ mol⁻¹ · c_max 52 500 mol m⁻³ (ref 3) · K_SE 15.9 · G_SE 8.7 GPa [카드 산술] | 카드 §3-4 · 표 1 (p.4) · 원문 p.1 | [인쇄] · [카드 산술] | 탄성 인용값 (측정 아님) · 우리 DFT ν 0.360 · B₀ 26.23 과 ν · K 다름 · 소성 없음

## d — 단단한 입자 + 무른 입자 혼합 압축의 하중 몫 · 재밍

- [d] park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics | 하중 몫 · 압축 계산 **없음** — 대신 단단한 NCM 망의 구조 지표: NCM–NCM 배위수 평균 **4.8 · 6.5 · 7.4** (NCM 질량비 70 · 80 · 85 % · p.3) · 분포 sd 2.43 · 2.63 · 3.08 · P(CN ≤ 2) 16.0 · 4.1 · 3.0 % · P(CN ≥ 10) 4.6 · 13.2 · 23.7 % (그림 2e 벡터 판독 · 합 1.00 · 평균 4.88 · 6.55 · 7.40 재현) · 저자: 높은 CN 이 *"enhances interparticle contact and restricts the freedom for individual particles to expand"* (p.4 — 사이클 중 구속이지 압밀 재밍이 아님) | 카드 §3-2 · §3-4 · 그림 2e | [인쇄] · [판독 · 벡터] · [카드 산술] | 연결 판정 기준 (거리 문턱 · 분리 · 경계 입자) 미인쇄 · XCT 복셀 0.65 µm

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위 · 대안

- 이 배치에 없음 (접촉 법칙 · DEM 없음 — 모델은 상 연속체 선형 탄성, 맞닿은 NCM 은 한 상 영역으로 붙어 있다 [카드 해석])

## f — MPM 접촉 · 다물체 · 강체 결합 · 해상도 규칙

- 이 배치에 없음 (MPM 없음).  해상도 쪽 참고: XCT 복셀 0.65 µm 에서 NCM 단면 ≈2–15 µm [판독] → 지름당 ≈3–23 복셀 · 두 NCM 사이 틈이 복셀 하나보다 좁으면 붙어 보일 수 있어 '연결' 이 근접 문턱 ≈ 1 복셀일 수 있다 — 원문은 해상도 영향을 말하지 않는다 (카드 §3-2 [카드 해석])

## g — 2D 결과를 3D 로 옮길 때의 경고 · 증거

- [g] park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics | **말 없음** — 응력은 *"a 2D computational domain"* (p.7) · *"two-dimensional (2D) tomography slices"* (p.3) 인데, 응력이 커지는 셋째 이유로 **3D** 망의 CN (그림 2e) 을 든다 (p.4) — 2D 단면의 이웃 수는 3D CN 과 다르다 [카드 해석] · 단면 ≈260 µm 가 양극 두께 ≈37–48 µm [카드 산술] 보다 커서 면과 나란한 단면일 수밖에 없고, 그 위에 '위아래 = 적층압' 을 걸었다 [카드 해석] | 카드 §3-4 · §4-4 | [인쇄] · [카드 산술 · 해석] | 2D → 3D 전이 진술 없음

## h — DEM 에서 FE · MPM 으로 넘긴 선례 · 시점

- 이 배치에 없음 (DEM 없음).  인접 (영상 → 연속체): XCT 분할 단면 (≈260 µm · 세 상) 을 그대로 2D 연속체 영역으로 써서 방전 응력을 풀었다 — 넘긴 시점 = 300 MPa 조립 뒤 (촬영 상태 미인쇄) · 압밀 이력 · 잔류 응력 · 접촉 상태는 넘기지 않음 (방전 0 % 무응력) (카드 §3-4 · §4-2)

## i — 복합 양극 (AM + SE) 의 압력별 기공

- [i] park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics | **조성별 · 한 압력**: 셀 전체 300 MPa 2 분 조립 뒤 XCT 공극 + 탄소 **14.7 · 18.1 · 23.3 %** · NCM 부피분율 0.391 · 0.506 · 0.500 · LPSCl 0.462 · 0.310 · 0.267 (NCM : LPSCl 질량비 70:30 · 80:20 · 85:15 · C65 3 phr) — *"Due to the low density of carbon, distinguishing empty spaces from carbon particles is challenging"* (p.3) | 카드 §3-2 · 그림 2d · 원문 p.3 · p.7 | [인쇄] | 공극에 탄소 포함 (공극의 상한) · 진밀도 기공 아님 · 촬영 때 압력 (50 MPa 유지 여부) 미인쇄 · 압력별 아님
- [i] park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics | XCT 의 NCM 몫 (NCM/(NCM+SE)) 0.458 · 0.620 · 0.652 ↔ 질량비 + 진밀도 (NCM811 4.77 [다른 카드] · LPSCl 1.64 랩 표준 / 1.87 랩 표준과 다른 문헌 값 [다른 카드]) 0.445–0.478 · 0.579–0.611 · 0.661–0.690 → ±0.04 안 (저자 *"aligns well"* 은 그 범위에서 성립 · 원문 진밀도 미인쇄) · 양극 두께 ≈48 · 37 · 38 µm [카드 산술 · 가정 NCM 9 mg cm⁻²] | 카드 §3-1 · §3-2 | [카드 산술 · 다른 카드 밀도] | 탄소 무시
- [i] park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics | 저자 해석: SE 가 적으면 *"less effective filling of the interstitial voids between NCM particles during electrode densification, resulting in higher residual porosity"* · 85:15 의 NCM 부피 (0.500) 가 80:20 (0.506) 보다 작다 (공극 + 탄소가 0.233 으로 큼) | 원문 p.3 · 그림 2d | [인쇄] | 해석 · 측정 아님

## j — 카드가 스스로 적은 한계 (가압 · 탈압 계산과 닿는 것)

- [j] park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics | 저자: *"Distinguishing and quantifying the individual contributions of interparticle and intraparticle stresses are challenging, as these phenomena are highly coupled and amplify each other"* (p.6) · 60:40 이면 응력은 줄어도 *"can limit effective electronic conduction and material utilization"* (p.6) · 탄소 · 공극 분할 어려움 (p.3) | 카드 §3-7 | [인쇄] |
- [j] park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics | 카드: 응력 모델 = 2D · 선형 탄성 · 소성 · 파괴 · 접촉 · 박리 · 압밀 이력 없음 · 공극/탄소 물성 (*"Table S1"* — SI 에 표 없음) · 적층압 값 · c(x) · 무응력 기준 · 격자 · 풀이기 · 단면 방향 미인쇄 · 확산 변형 식 c_max(1 − c/c_max)Ω/3 은 리튬화 때 수축 ↔ 본문 '리튬화 때 팽창' · 원문 수치 어긋남 셋 (그림 1a–c 곡선 끝 ↔ 인쇄 · 그림 1e ↔ 1d · 그림 5g ↔ 인쇄 XANES 통계) | 카드 §3-4 · §3-7 · §11 · §13 | [카드 해석] · [판독 · 벡터] |

## k — DEM 의 한계 (원문 문장 · 위치)

- [k] park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics (Park 외 2025 · ACS Nano 19, 22262) | **말 없음** — 본문 · SI 에 DEM · discrete · particle simulation 낱말 0 회 · DEM 을 쓰지 않음 | 카드 §4-4 · 원문 대조 기록 | [인쇄 전수] |

## l — 소성변형이 왜 어려운가 · 우회 · 비용

- [l] park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics (Park 외 2025 · ACS Nano 19, 22262) | **말 없음** — *"plastic"* 0 회 · *"The mechanical strain component is obtained based on the linear elasticity formulation, whereas the diffusion-induced component is a function of the Li concentration, c, within the active material, and the partial molar volume of Li, Ω"* (p.7) — 소성 · 파괴를 넣지 않았고 이유 · 우회 · 비용 없음 · 그 결과 응력이 색 막대 ±5 GPa · σy > 2 GPa 면적 (인장 0.25 → 2.42 · 압축 1.73 → 3.98 %) 까지 탄성으로 남는다 (LPSCl 이 그만큼 버틴다는 뜻 아님 [카드 해석]) · 맞춘 값 0 개 (전부 인용 물성) · 검증 = FIB-SEM 균열 · XANES 불균일의 방향 일치뿐 | 카드 §3-4 · §4-4 · 그림 3h | [인쇄] · [판독 · 벡터] | 2D · 사이클 고유 변형 (압밀 아님)

## m — 받아들일 통찰

- [m] park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics | **CN 연산자를 결과 전에 두 판으로**: AM–AM CN 을 겹침 (δ > 0) 과 '틈 ≤ 0.65 µm' (XCT 복셀 하나) 로 함께 내고 벽 · 판 접촉 입자 제외 값을 따로 둔다 → XCT 값 (4.8 · 6.5 · 7.4) 이 그 띠에 오는지로 연산자 차이를 잰다 | 단계 0 · 후보 D0 · 결과 전 대조 항목 | 근거 = 판정 기준 미인쇄 · 복셀 0.65 µm (카드 §3-2 · §7-2)
- [m] park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics | **CN 보고 꼴**: 평균만이 아니라 정수 빈도 분포 (합 1) · sd · P(CN ≤ 2) · P(CN ≥ 10) — 조성이 바뀔 때 평균보다 꼬리 (16 → 3 % · 4.6 → 23.7 %) 가 더 크게 움직인다 | 단계 7 · 후보 D0 (`am_am_cn` 열에 분포 열) | 근거 = 그림 2e 벡터 판독 (카드 §3-2)
- [m] park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics | **응력 지표 보고 규율**: 여러 단면 평균 ± sd 로 내고, 탄성 상한 응력 (±5 GPa) 은 소성 모델 응력 · 항복 값과 같은 표에 두지 않는다 | 단계 5 (MPM) | 근거 = 그림 3h · p.7 (카드 §3-4 · §9-4)
- [m] park2025_high_loading_cathode_cam_ratio_coordination_chemomechanics | **흐름 밖: A10 사이클 원장의 AM–AM 재폐합 가정 재검토** — 우리 생산 조성 (ps45 NCM 81.6 wt% [다른 카드 gandla2026 L335]) 은 이 논문에서 균열 · 유지율이 크게 나빠지는 80:20–85:15 사이이고 저자는 그 열화를 입자 사이 (AM–AM) 응력 탓으로 본다 (p.6 · 추론) | 흐름 밖: A10 · 조건 R7 | 근거 = p.6 · 그림 4 · 1e (카드 §7-3)

## n — 논문 에이전트 후보

- [n] Choi, S.; Jeon, M.; Ahn, J.; Jung, W. D.; Choi, S. M.; Kim, J.-S.; Lim, J.; Jang, Y.-J.; Jung, H.-G.; Lee, J.-H.; et al. Quantitative analysis of microstructures and reaction interfaces on composite cathodes in all-solid-state batteries using a three-dimensional reconstruction technique. ACS Appl. Mater. Interfaces 2018, 10, 23740−23747 | i · 단계 5 — 14.7 % 공극/탄소가 *"similar to prior studies"* 의 근거 (ref 23) · 3D 재구성 복합 양극 정량 (상 분율 · 계면) | litdb 확인: `ls litdb/papers/choi2018*` 없음 · "23740" grep = shi2019 · nakamura2020 (인용만) → 카드 없음 (PDF 가 inbox 에 이미 있다: `3dad4b72-14._Quantitative_Analysis_of_Microstructures_and_Reaction_Interfac…`)
- [n] Naik, K. G.; Jangid, M. K.; Vishnugopi, B. S.; Dasgupta, N. P.; Mukherjee, P. P. Interrogating the Role of Stack Pressure in Transport-Reaction Interaction in the Solid-State Battery Cathode. Adv. Energy Mater. 2024, No. 2403360 | j · 단계 5 · 6 — 같은 모델 그룹의 적층압 의존 양극 모델 (경계 적층압 값 · 구성식 · 압력 → 수송 결합의 단서) (ref 9) | litdb 확인: `ls naik2024*` 없음 · "2403360" grep 0 건 → 카드 없음
- [n] Kim, S. Y.; Cha, H.; Kostecki, R.; Chen, G. Composite cathode design for high-energy all-solid-state lithium batteries with long cycle life. ACS Energy Lett. 2023, 8, 521−528 | i · 흐름 밖 (고 CAM 비율 설계 · 기계 열화) (ref 14) | litdb 확인: `ls kim2023*` 에 해당 없음 · 제목 낱말 grep = luo2026 · schmitt2026 · tailored_cathode · wolf2026 (인용만 · tailored_cathode 는 Zhou 2025 다른 논문) → 카드 없음
- [n] Singh, D. K.; Henss, A.; Mogwitz, B.; Gautam, A.; Horn, J.; Krauskopf, T.; Burkhardt, S.; Sann, J.; Richter, F. H.; Janek, J. Li6PS5Cl microstructure and influence on dendrite growth in solid-state batteries with lithium metal anode. Cell Rep. Phys. Sci. 2022, 3, No. 101043 | c — 표 1 의 E_SE 22 GPa 출처 (서론은 Deng 2016) · 그 논문에 22 GPa 가 있는지 확인 | litdb 확인: `ls singh2022*` 없음 · "101043" grep = tron2023_lpscl_ccd (인용만) → 카드 없음
- [n] Woodcox, M.; Shepard, R.; Smeu, M. First principles investigation into the interwoven nature of voltage and mechanical properties of the LixNMC-811 cathode. J. Power Sources 2021, 516, No. 230620 | c — E_AM 200 GPa 출처 (Li 함량 의존 NMC811 탄성 · 우리 DEM NCM 140 GPa 와 대조) | litdb 확인: `ls woodcox*` 없음 · "230620" grep 0 건 → 카드 없음

## 카드 문제

1. `gandla2026_layered_cathode_degradation_diagnostics_review` L121 — *"NCM 입자 사이 배위수 (직접 접촉 수)"*: 원문은 *"connected"* · *"physical connections"* (p.3) 만 쓰고 판정 기준이 없다 → '직접 접촉' 은 원문보다 강한 표현.  같은 줄의 꼬리 끝 *"≈12 (70:30)"* 는 재수록 래스터 판독 — 원 그림 벡터로는 빈도 > 0.001 인 마지막 CN 이 14 (CN 13–15 = 0.0035 · 0.0017 · 0.0007).
2. `gandla2026_…` L337 의 [미확인] ① (질량/부피 기준) · ② 중 분해능 · ④ (원 논문 카드) 는 이 카드로 해소 — ② 의 판정 기준 · ③ 입경은 원 논문에도 없다.  그 카드 줄은 고치지 않았다.
3. `li2026_electrochemomechanical_coupling_asslmb_review` L66 — *"미세구조 기반 모의에서 방전 중 NCM 부피변화 ≈10 %"*: 원문의 ≈10 % 는 서론의 문헌값 (*"CAM experiences volume changes of up to ∼10%,11−13"* p.1) 이지 모의 결과가 아니다 (모델 입력 Ω c_max/3 = 선 3.5 % [카드 산술]).
4. `li2026_…` L98 · L104 — *"로딩 의존"* · *"(로딩)"*: 이 논문의 'high-loading' 은 **CAM 질량비** — 면 로딩은 세 조성 모두 NCM 9 mg cm⁻² 로 같다 (p.7).
5. comparison_vs_ours_DEM.md L3032 (§E) — *"DEM AM–AM CN 과 같은 양"*: 원 논문 기준 = **같은 이름 · 다른 연산자** (기공망 연결 · 복셀 0.65 µm · 판정 기준 미인쇄).  옛 줄은 두고 바로 아래 원전 줄을 보탰다 (이 커밋).
6. 원문 안 어긋남 (논문 문제 · 카드 §3-7): *"Table S1"* 없음 · E_SE 출처 둘 (ref 16 · 30) · ν 0.27 출처 없음 · 확산 변형 식 부호 ↔ 본문 · 그림 1a–c 곡선 끝 (70:30 0.1C 158.6 vs 156.7 · 80:20 0.5C 114.1 vs 117.4) · 그림 1e 사이클 2 ↔ 그림 1d 0.2C · 그림 5g 통계 (평균 8353.24 · 8353.54 · 8353.70 · sd 0.26 · 0.28 · 0.33) ↔ 인쇄 (8353.4 · 8353.8 · 8353.9 · 0.31 · 0.36 · 0.41).

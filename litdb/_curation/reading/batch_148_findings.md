# batch 148 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-23 · U-1123-5 · 새 카드)

대상: `vanpeene2026_4d_nano_holotomography_dvc_graphite_silicon_chemomechanics` — V. Vanpeene\* · O. Stamati · F. Cadiou · Q. Jacquet · J. Villanova · S. Lyonnard\*, "Four-dimensional X-ray nano-holotomography reveals multiscale chemomechanics in composite graphite–silicon battery electrodes", *Nature Nanotechnology* (2026 · 권 · 쪽 없음 · 출판 전 판 · DOI 10.1038/s41565-026-02327-6).
흑연–Si 액체 LIB 음극 (흑연 74 · nano Si@C 11 · SBR:CMC 14 · Super C45 1 wt%) 의 첫 화성 사이클을 중단-operando 나노 홀로토모그래피 (복셀 50 nm · 한 장 9 분 · 13 상태) + 국소 / 이산 DVC + TauFactor 로 잰 측정 논문 — 고체전해질 · 압밀 · 계산 모델 없음 · 적층압 ≈ 23 kPa (추정).
쪽 = 본문 PDF 쪽 p.1–16 · SI 는 `SI p.N` (보충 PDF 쪽) · 원자료 = 보충 엑셀 MOESM9–14 · 고른 의도 대조 = **일부 (거의 채움)** (후보 표 행 아님 · 의도 = 1저자 11-23 업로드 + 지시서 '꼭 뽑을 것' · 카드 §0-1 — 변위 정확도 (µm) · 균열 정량은 원문에 없음).
인용 서지 (질문 k · l 용): V. Vanpeene, O. Stamati, F. Cadiou, Q. Jacquet, J. Villanova, S. Lyonnard, *Nature Nanotechnology* (2026), DOI 10.1038/s41565-026-02327-6.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 고체전해질 · 압밀 없음 (액체 LIB 흑연–Si 음극 · 압연 선하중 5 MPa 사양 기공 30–35 % · 영상 OCP '기공 + 바인더/Si' 35.3 %v · 카드 §3-1 · §3-4 · §7-2).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
- [b] vanpeene2026_4d_nano_holotomography_dvc_graphite_silicon_chemomechanics | 기계 탈압 없음 (적층압 ≈ 23 kPa 그대로) — 대신 **화학 하중 (리튬화 팽창) 이 빠진 뒤 남는 변형**: 전극 ε_V 12.42 → 7.35 % (끝/최대 0.59) · ε_D 7.23 → 5.38 % (0.743 = 본문 '74 %') · ε_zz 9.32 → 5.87 (0.63) · ε_yy 2.08 → 1.21 (0.58) · ε_xx 0.98 → 0.23 % (0.23) · 입자 평균 ε_V 11.63 → 7.45 % · 두께 60 → 75 → 64 µm | 카드 §3-5 · §3-6 · §3-8 · 그림 1e · 3b–c · 5c · p.5 | 원자료 MOESM11 · 13 (변형률) · 인쇄 (두께) · 카드 산술 (비) | 잰 방법 = 국소 DVC (4 µm 창 · OCP 기준 total · 질량 중심 강체 운동 뺌 · 식 7–8) · 압력 제거가 아니다 · 액체 LIB · 두께 (+25 %) ↔ DVC 평균 ε_zz (9.3 %) 2.7 배 차는 해명 없음 · 본문 'ε_zz 8.8 · ε_xx 1.24 · ε_yy 2.43 %' 는 원자료와 안 맞음

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 항복 · 경도 · 크리프 값 0.  가장 가까운 것 (2 차 인용 · 바인더): *"a local maximum tensile strain of 7% or higher could lead to binder failure"* — CMC 거시 물성 문헌 [14] Li · Lewis · Dahn (Electrochem. Solid State Lett. · SI 참고문헌) 인용 (SI p.42 · 카드 §0 ⑪) — 우리 SE 항복과 무관.

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
- [d] vanpeene2026_4d_nano_holotomography_dvc_graphite_silicon_chemomechanics | 하중 몫 숫자 없음 · 정성 둘: *"dominated by graphite particle deformation rather than silicon, demonstrating graphite's role as the structural backbone, with localized particle movements driving microstructural rearrangements"* (p.10) · 이웃 흑연 > 10 개면 비가역 ↓ — *"probably due to constraining effects in locally compacted areas with numerous contact points"* (p.10 · 영향 인자 +0.714 · corr 0.828) | 카드 §3-9 · §4-7 (ii) · p.10 · 그림 6i | 인쇄 · 원자료 MOESM14 | 압밀 아님 (팽창하는 Si 와 흑연 골격) · 하중 · 접촉력 측정 없음 · '이웃 수' 는 배위수 꼴이지만 정의식 · 문턱 근거 미인쇄

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음 — 접촉 법칙 · 계산 없음.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
- [f] vanpeene2026_4d_nano_holotomography_dvc_graphite_silicon_chemomechanics | **MPM 아님 — 측정 쪽의 같은 꼴 (해상도 · 오차 추정)**: DVC 창 크기 사다리 2–16 µm 를 충방전 없는 두 스캔으로 재 오차가 창이 작을수록 커짐 (2 µm ε_D ≈ 2.0 · ε_V ≈ 1.6 % [판독] → 4 µm ε_V 0.36 · ε_D 0.53 %) → 4 µm 택함 · 이산 DVC 오차 ≈ 0.26 % (20 입자) · 경계 해상도 (회색값 미분 반치폭) 140 nm = 복셀 50 nm 의 2.8 배 · Si (공칭 200 nm) 는 해상도 1.4 배라 해상 Si 4.1 %v ↔ 이론 18 %v (75 % 미해상) · REV = 무작위 부분 부피 10 개 · 95 % · 5 % → 90³ µm³ | 카드 §3-2 · §3-6 · §4-4 · §7-4 · SI 그림 1 · 21 · 23 · SI 주석 1 · 10 · 11 · p.2 | 인쇄 · 판독 (SI 그림 21) · 원자료 오차 칸 | 시뮬레이션 격자 규칙 아님 — U6 (해상도 수렴) · 단계 0 (REV) 의 측정판 · 우리 MPM dx ≈ 141 nm (real_14 · n_grid 384) 가 이 측정의 해상 한계와 같은 급

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 측정 · 분석 모두 3D (2D 단면은 표시용) · 2D → 3D 전이 진술 없음 (카드 §4-7 (iii)).

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 — 계산 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — 음극 · 액체 전해질 · 압력 축 없음.

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] vanpeene2026_4d_nano_holotomography_dvc_graphite_silicon_chemomechanics | 원문 스스로 적은 측정 한계: (i) Si 의 75 % 미해상 (p.2) (ii) 집전체 근처 단면은 위상 인공물로 정량 제외 (p.14) (iii) 창마다 아핀 변형 가정 · 비선형은 잔차로만 (*"no nonlinear changes … were identified in the DVC residual fields"* p.16) (iv) 반응–확산 결합 무시 (C/6 · SI 주석 5) (v) 박리 *"no delamination was qualitatively observed"* (p.5 · 정성) | 카드 §3-2 · §4-4 · §4-5 · §11 | 인쇄 | 가압 · 탈압 계산과 직접 닿는 한계는 없다 — 기계 하중이 없다 (≈ 23 kPa 추정 · 시간 변화 미측정) 는 것이 이 측정의 범위 한계 · 카드 쪽 한계: 본문 수 여럿이 원자료와 어긋남 (카드 §11 · 19 항)

## k — DEM 의 한계
- [k] vanpeene2026_4d_nano_holotomography_dvc_graphite_silicon_chemomechanics (V. Vanpeene et al., *Nature Nanotechnology* 2026) | **말 없음** — DEM 을 쓰지 않는다.  가까운 일반 문장 둘 (평균 기술자 모델 비판): *"Empirical tuning of averaged parameters (particle size distribution and porosity) often fails to capture the three-dimensional (3D) multiscale complexity that governs electrochemical performance2–4."* (p.1 · [4] = Ngandjong 2021 DEM 압연 디지털 트윈 = `ngandjong2021_dem_calendering_digital_twin`) · *"While current approaches rely on ensemble and space-averaged descriptors,[17, 18] few works incorporate actual microstructures as simulation inputs.[19–21] To our knowledge, no detailed modeling has been attempted using operando nano-CT data on battery materials."* (SI p.46 · [18] = 같은 Ngandjong 2021) | 카드 §4-7 (i) · p.1 · SI 주석 9 | 인쇄 | 강구 · 점접촉 · 접촉 독립 가정의 한계를 말한 문장이 아니다 — '평균 기술자로 맞춘 모델' 일반에 대한 동기 문장으로만 인용 가능

## l — 소성변형이 왜 어려운가 · 우회 · 값 · 비용
- [l] vanpeene2026_4d_nano_holotomography_dvc_graphite_silicon_chemomechanics (V. Vanpeene et al., *Nature Nanotechnology* 2026) | **논의 없음** (계산 없음 · 측정) — 측정 해석 문장: *"Transient and irreversible phenomena relate directly to particle rearrangements and sliding within the binder matrix, involving changes in ionic diffusion pathways, pore clogging and particle–binder debonding."* (p.9–10) · *"This dilatant shearing behavior, typical of dense granular and/or cohesive materials, develops heterogeneously in the electrode microstructure."* (SI p.42) · 측정 쪽 가정 = 창마다 아핀 (선형 · 균일) 변형 Φ (12 미지수) — 입자 안 비선형 · 불연속은 잔차로만 본다 (p.15–16) | 카드 §4-4 · §4-7 (ii) | 인쇄 | 우회 · 맞춘 값 · 비용 없음 — '미끄럼 · 재배열 · 탈착이 비가역을 만든다' 는 측정 쪽 정성 근거로만 (액체 LIB · 화학 하중 · 흑연)

## m — 받아들일 통찰
- [m] vanpeene2026_4d_nano_holotomography_dvc_graphite_silicon_chemomechanics | **변형률 장 보고 규약** — 첫 상태 기준 (total) · 질량 중심 강체 운동 뺌 · 창 평균 F → 극분해 → ε_V = det F − 1 · ε_D = ‖det(F)^(−1/3)U − I‖ (식 7–8) · 끝/최대 비 (ε_V 0.59 · ε_D 0.743) 를 '남는 몫' 으로 | 단계 6 (언로딩) · 후보 A′ — 왜: MPM 장을 같은 정의로 줄여야 측정 · 문헌과 같은 이름 · 같은 양으로 견준다 (카드 §4-4 · §9-1 · p.15–16)
- [m] vanpeene2026_4d_nano_holotomography_dvc_graphite_silicon_chemomechanics | **입자 번호별 아핀 F (이산 DVC)** — 입자 바운딩 박스 = 창 하나 · 질량 중심 Φ → F → 입자 ε_V · ε_D · 전극 평균 ↔ 입자 평균 대조 (12.44 ↔ 11.63 % · 끝 7.50 ↔ 7.45 %) | Ⓑ DEM → MPM 입자 번호 승계 · R3 · R6 — 왜: 번호 무리마다 최소제곱 아핀 F 하나 = '입자 형태 변형' 의 한 수 (측정과 같은 꼴) (카드 §3-8 · §4-4 · §9-2 · p.7 · p.16)
- [m] vanpeene2026_4d_nano_holotomography_dvc_graphite_silicon_chemomechanics | **함정: 고정 상자 상분율 두 곡선은 한 측정 · 해상도 밑 상의 귀속** — 흑연 상대 변화 = −0.627 × 기공 상대 변화 (13 상태 소수 셋째 자리까지) · 해상도 밑 CBD–Si 를 '기공' 으로 셈 · 입자 안 · 사이 가름이 그림 2b–c 원자료 (몫 ≈ 20 %) 와 SI 그림 8a (≈ 46 % [판독 · 카드 산술]) 에서 다름 | 단계 0 (기공 연산자 · 상 규약 칸 · STEP3 표현 부피 장부 CL-25 와 같은 부류) — 왜: 두 곡선을 독립 증거로 세면 같은 것을 두 번 센다 · '기공' 에 어느 상이 들어갔는지 적어야 비교가 된다 (카드 §3-4 · §11-3 · §11-4 · SI 주석 4)
- [m] vanpeene2026_4d_nano_holotomography_dvc_graphite_silicon_chemomechanics | **흐름 밖: 배위수 ↔ 비가역 · 빠른 경로 ↔ 활성** — 이웃 흑연 > 10 → 비가역 ↓ (IF 0.71) · 빠른 기하 경로 (τ_geo = L_geodesic/L_E < 1.2 인 기공 복셀 다발 · 9 → 3 → 13 개) 근접 IF 1.0 | 흐름 밖: A10 사이클 접촉 원장 결과를 입자 배위수로 쪼개 보기 · SE 망 τ_geo 지도 (`tau_geo_SE_dij`) 위 빠른 경로 기술자 — 왜: DEM · 망이 바로 내는 양의 측정 쪽 상관 꼴 (카드 §3-7 · §3-9 · §9-4 · p.6 · p.10 · 그림 6)

## n — 논문 에이전트 후보
- [n] Vanpeene, V. et al. Comparative study of the quantitative analysis of battery materials with X-ray nano-tomography: from ex situ toward operando measurements. ACS Nano 19, 9994–10012 (2025). | 같은 셀 · 같은 측정 흐름의 방법 논문 — 선량 · ex situ ↔ operando 정량 차이 (f 의 측정판 · m 의 상 규약) (카드 §12 · 참고 25) | litdb 확인: papers/ 목록 (616) · 'Comparative study of the quantitative' · '9994' grep — 카드 없음 ('Vanpeene' = korjus2025 공저자 이름뿐)
- [n] Pietsch, P. et al. Quantifying microstructural dynamics and electrochemical activity of graphite and silicon–graphite lithium ion battery anodes. Nat. Commun. 7, 12909 (2016). | 흑연 · Si–흑연 전극 DVC 의 선행 (b · m 의 창 크기 · 변형률 값 대조) (카드 §12 · 참고 30) | litdb 확인: '12909' · 'Quantifying microstructural dynamics' grep 0 · pietsch* 카드 없음
- [n] Lu, X. et al. Unravelling electro-chemo-mechanical processes in graphite/silicon composites for designing nanoporous and microstructured battery electrodes. Nat. Nanotechnol. 20, 1656–1666 (2025). | 같은 계 (흑연/Si) 화학기계 · ε_zz 비등방의 '이전 보고' (b) (카드 §12 · 참고 43) | litdb 확인: 'Unravelling electro-chemo-mechanical' grep 0 · `lu2025_tailoring_cl_rich_anode_licl` = 다른 논문
- [n] Valisammagari, A. et al. Study of microstructural evolution and strain analysis in SiOx/C negative electrodes using in-situ X-ray tomography and digital volume correlation. Batteries Supercaps 8, 202400416(2025). | Si 계 음극 DVC · 집전체 박리 사례 (이 논문 p.5 의 박리 근거 · b · j) (카드 §12 · 참고 31) | litdb 확인: '202400416' · 'Study of microstructural evolution and strain' grep 0 · 'Valisammagari' = 다른 카드 세 곳의 공저자 이름 · 인용만
- [n] Nelson, D.L., Sandoval, S.E., Pyo, J., Bistri, D., Thomas, T.A., Cavallaro, K.A., Lewis, J.A., Iyer, A.S., Shevchenko, P., Di Leo, C.V., McDowell, M.T.: Fracture dynamics in silicon anode solid-state batteries. ACS Energy Lett. 9(12), 6085– 6095 (2024) | **고체** Si 음극의 파괴 역학 — R7 · j (우리 고체 쪽 사이클 화학기계 · A10) (카드 §12 · SI 참고 [28]) | litdb 확인: 'Fracture dynamics in silicon' grep 0 · '6085' = 무관 카드 1

## 카드 문제
없음 — 가리킨 카드가 없고 (후보 표 행 아님), 정본의 'Vanpeene' 는 `korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens` (L13 · L76 · L389) · INDEX.md L228 · reading/batch_61 에 나오는 Korjus 2025 (Energy Storage Mater. 82, 104589) 의 **공저자 이름**뿐 — 이 논문의 2 차 인용이 아니다.  참고 (이 논문 쪽 · 고치지 않음): 이 논문은 tortuosity factor 의 *"standard definition"* 근거로 참고 63 = `nguyen2020_electrode_tortuosity_factor` (제목부터 그 관습 정의가 다공 전극 수송에 맞지 않는다고 하는 논문) 를 인용한다.

# batch 138 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-22 · 후보 N-89)

대상: `bielefeld2022_li_kinetics_morphology_voids_fem_composite_cathode` — A. Bielefeld\* · D. A. Weber · R. Rueß · V. Glavas · J. Janek\*, "Influence of Lithium Ion Kinetics, Particle Morphology and Voids on the Electrochemical Performance of Composite Cathodes for All-Solid-State Batteries", *J. Electrochem. Soc.* **169** (2) (2022) 020539 · DOI 10.1149/1945-7111/ac50df (13 쪽 + SI 14 쪽).
다결정 NCM811 / Li₆PS₅Cl 복합 양극의 정전류 충전을 3D FEM (COMSOL 5.4) 으로 — 입자형 (GeoDict 구 · CAM 42 vol% · SE = 이상 접촉 연속체) · 1-입자 반구 공극 · 원뿔 구조 세 기하 · 입력 = 같은 재료 측정 (Rueß 2020 GITT · EIS · OCV · σ_SE 0.7 mS cm⁻¹) · 맞춘 값 0 · 역학 · 압력 · DEM 없음.
쪽 = PDF 쪽 (p.1 = IOP 표지 · 논문 첫 쪽 = p.2) · SI p.N = SI PDF 쪽 N (인쇄 S-(N−1)) · 판독 원자료 = `litdb/figures/bielefeld2022_…/digitized.csv` (319 행) · 고른 의도 대조 = **일부** (카드 §0-1 — 수송 · 반응 · 공극 · 형태의 3D 모델 = 채움 (한정) · "i₀,ref 0.05 A/m² 출처" = **없음** · lee2024 의 3D 판 = 일부 (범위 겹치지 않음) · 2019 · 2020 카드 있음 = 채움).
인용 서지 (질문 k · l 용): Bielefeld, Weber, Rueß, Glavas, Janek, J. Electrochem. Soc. 169 (2022) 020539.

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 순수 SE 기공 · 밀도 · 압력 자료가 원문에 없다.
- [a] bielefeld2022_li_kinetics_… | (참고 · 곡선 아님) σ_SE **0.7 mS cm⁻¹** = 모델 입력 (Li₆PS₅Cl · 출처 표기 Rueß 2020) — 펠릿 기공 · 압력 · 온도 [미확인] | 카드 §3-2 · SI 표 S2 (`tab_S2.png`) | [인쇄] | 랩 표준 (10–13 % · 1.64) 옆에 둘 숫자 아님

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 가압 · 탈압 · 역학 계산이 없다.

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음.

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 하중이 없다 (CAM = 고정 구 · SE = 연속체 · 이상 접촉).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
이 배치에 없음.

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차 추정
이 배치에 없음 (MPM 아님).
- [f] bielefeld2022_li_kinetics_… | (참고 · FE 격자) 1-입자 7 µm 의 요소 0.0162–0.378 µm (사면체 0.41–1.74 M) · 입자형 0.0765–1.79 µm (8 625 685) · 원뿔 0.0102–1.02 µm (523 859) · 계면 · 좁은 틈 세분 · **격자 수렴 시험 보고 없음** | 카드 §3-3 · SI Fig. S5 (`fig_S5.png`) · SI p.10 | [인쇄] | 전기화학 FE · 수치 오차 추정 없음

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 (3D 만 · 2D 와 견주지 않음).
- [g] bielefeld2022_li_kinetics_… | (참고) 같은 질문 (계면 덮임 → 성능) 의 2D 단일 입자 (lee2024 · 피복 10–100 % · ≤ 5 C) 와 이 3D 단일 입자 (남은 계면 ≥ 53 % · ≤ 0.5 C) 는 **범위가 겹치지 않아** 2D ↔ 3D 대조가 안 된다 | 카드 §0-1 · §3-7 · Fig. 8 · 9 | [판독] · [다른 카드] | 출력도 다름 (공극 과전압 ↔ 이용률)

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음 (DEM 없음).
- [h] bielefeld2022_li_kinetics_… | (참고 · DEM 아님 · 기하 넘김 선례) GeoDict 구 목록 (.gad · 지름 · 위치) → Matlab (GeoLab · LiveLink) → COMSOL .mph 로 같은 구를 다시 만들고 · 주기 배치를 (3 × 3 × 2) 복제 뒤 SE 상자로 잘라 x · y 주기 · 첫 충전 계산으로 고립 입자를 찾아 **손으로 옮김** · 주기 경계용 모서리 · 면 격자 복사 | 카드 §3-3 · SI p.6 · p.10 (`txt_pS6_placeholder_percolation_trick.png`) | [인쇄] | 압밀 · 접촉 정보 없는 생성기 → FE

## i — 복합 양극 (AM + SE) 의 압력별 기공
- [i] bielefeld2022_li_kinetics_… | (2 차 인용 · 압력 없음) ASSB 양극 공극 **6–40 %** · 슬러리 미압연 NCM622/β-Li₃PS₄ **20–40 %** (Ates 2019) · LiCoO₂ 에 Li₆PS₅Cl 침투 **6–8 %** (Kim 2017) · 실험실 프레스 셀 다결정 NCM/Li₆PS₅Cl **≈14 %** (refs 10 · 27) · LiCoO₂/Li₂S-P₂S₅-LiI **13 %** (Hlushkou 2018) | 카드 §3-7 · p.10 (`txt_p10_void_fraction_range.png`) | [인쇄 · 2 차] | 압력 · 기공 정의 · 진밀도 기준 [미확인]
- [i] bielefeld2022_li_kinetics_… | 모델 쪽: 70 : 30 wt% + 공극 14 % → **CAM 42 vol%** · 그러나 SE 가 남은 부피를 다 채워 **모델 기공 0 %** (모델 SE 58 vol% ↔ 실물 SE ≈44 % + 공극 14 % [카드 산술]) · 42 % 는 ρ_SE ≈1.95 g cm⁻³ 일 때 재현 (원문 ρ_SE 없음 · 랩 표준 1.64 면 38.3 vol% [카드 산술]) | 카드 §3-3 · SI p.6 | [인쇄] · [카드 산술] | 문헌 시뮬 기공 = 0 % 조건 · 밀도 기준 표기 필요

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 (가압 · 탈압 계산과 닿는 것)
- [j] bielefeld2022_li_kinetics_… | *"this model approach is not capable to quantify the influence of voids in the cathode composite on ionic percolation, as we are focusing on the role of the active surface area and one CAM particle only"* | p.10 (`txt_p10_void_model_limits.png`) | [인쇄] | 공극 = 고정 반구 · 복합체 퍼콜레이션 없음
- [j] bielefeld2022_li_kinetics_… | *"Moreover, assuming that the SE becomes more compact upon cycling due to external pressure, the influence of the smaller voids is expected to decrease."* (계산 없음) | p.10 | [인쇄] | 압력 효과는 가정 문장뿐
- [j] bielefeld2022_li_kinetics_… | *"the model also does not feature voids that, in practice, would occur between CAM particles, between SE particles and at the SE/CAM interface and would lower the performance"* (원뿔 모델) | p.12 (`txt_p12_cone_size_guideline.png`) | [인쇄] | —
- [j] bielefeld2022_li_kinetics_… | *"coupled (chemo-)mechanical and electrochemical simulations of the cathode composite are required on the microstructure level, as these can enlighten the mechanical behavior, the formation and evolution of voids and inter-particle cracks during cycling"* | p.13 | [인쇄] | 후속 과제로만
- [j] bielefeld2022_li_kinetics_… | 단순화 (계면 열화 · 공극 · 공간 전하 무시 · SE Ohm) 는 과전압을 **과소평가** 쪽 · 구 2 차 입자 (거칠기 없음) 만 반대 쪽 | p.8 (`txt_p8_simplifications_underestimate.png`) | [인쇄] | 방향만 · 크기 없음

## k — DEM 의 한계 (서지: Bielefeld, Weber, Rueß, Glavas, Janek, J. Electrochem. Soc. 169 (2022) 020539)
- [k] bielefeld2022_li_kinetics_… (Bielefeld 2022 · J. Electrochem. Soc.) | **말 없음** — DEM 을 쓰지 않는다 (본문 DEM 0 회).  관련 (DEM 아님 · 구 형상 가정의 대가): *"We explain this by the surface roughness of the NCM visible in the SEM-images in Fig. 2 (right) that is not part of the microstructure model, because solely spherical secondary CAM particles are modeled"* (모델 0.17 ↔ BET 0.2 m² g⁻¹ · p.4) · *"The only influence that would act contrariwise is the modeling of NCM particles as spherical secondary particles, neglecting their primary particle structure and surface roughness that increases the active surface area and would lower the overpotential"* (p.8) | 카드 §3-4 · §3-6 · `txt_p4_validation_surface_area.png` · `txt_p8_simplifications_underestimate.png` | [인쇄] | 구 입자 모델 일반의 면적 과소 — 크기 ≈15 % (0.17/0.2)

## l — 소성변형이 왜 어려운가 · 우회 (서지: Bielefeld, Weber, Rueß, Glavas, Janek, J. Electrochem. Soc. 169 (2022) 020539)
- [l] bielefeld2022_li_kinetics_… (Bielefeld 2022 · J. Electrochem. Soc.) | **논의 없음 (역학 없음)** — 관련 문장: 초록 *"the rigid solid electrolyte entails its own morphology and does not wet residual voids in composite electrodes"* · *"Possibly, SE particles are only partly disconnected, depending on their mechanical rigidity"* (p.10) · SE 미세구조를 풀지 않은 이유 = 격자 비용 *"not resolving the actual SE-microstructure for technical reasons: The finite element method (FEM) in COMSOL Multiphysics requires a computation mesh on the geometry whose element size would drastically increase when modeling the SE as e.g. convex polyhedra"* (SI p.7) · 우회 = SE 를 이상 접촉 연속체로 · 공극을 고정 반구로 · 맞춘 값 0 · 비용 = 입자형 8 625 685 사면체 · 128 GB RAM 워크스테이션 (계산 시간 [미확인]) | 카드 §3-3 · §4-2 · `txt_pS7_1particle_no_se_microstructure.png` · `txt_p10_void_size_ratio_types.png` | [인쇄] | 소성 · 압밀은 다루지 않음 — '어려움' 의 직접 진술은 FEM 격자 비용뿐

## m — 받아들일 통찰
- [m] bielefeld2022_li_kinetics_… | **맞춤 0 검증 규약 — 입력은 같은 재료 측정 곡선 그대로**: SOC 의존 D̃_Li · j₀ · OCV (Rueß 2020) 를 맞추지 않고 넣어 0.02–0.5 C 곡선을 따라갔고, 상수 입력은 첫 전압 상승을 못 냈다 · *"the often performed fitting of j₀ or the reaction rate constant to the simulation should be rethought"* → 우리 STEP4 에 같은 계 곡선 (digitized.csv Fig. 7a · S2) 으로 맞춤 없는 한 팔을 결과 전에 등록 (우리 다결정 D 기본값 3 × 10⁻¹⁴ m² s⁻¹ 은 이 곡선 최대 6.9 × 10⁻¹⁶ 의 ≈44 배 [카드 산술 · 우리 CLAUDE.md]) | 자리: 흐름 밖: STEP4 전기화학 · R1–R7 (R5) | 왜: 카드 §3-4 · §3-6 · §9-1 · p.5 · p.10 · Fig. 7
- [m] bielefeld2022_li_kinetics_… | **R_CT → j₀ 는 면적 A 를 품는다 (식 [12])** — 모델 0.17 ↔ BET 0.2 m² g⁻¹ 면 j₀ 가 ×1.18 갈린다 · 출처 없는 상수 j₀ (예: kim2024 의 'i₀,ref 0.05 A/m²' — 원문에 없음) 를 옮기지 말고 면적 기준과 함께 곡선을 옮긴다 | 자리: 흐름 밖: Rint ② · STEP4 | 왜: 카드 §3-1 · §4-3 · §9-2 · 식 [12] (`eq_12_rct_j0.png`)
- [m] bielefeld2022_li_kinetics_… | **피복 출력에 분포 척도를 함께** — 같은 남은 계면 70 % 에서 공극 크기 비 1.2 ↔ 10 의 0.2 C 공극 과전압 65.9 ↔ 14.4 mV (@100 mAh g⁻¹) [판독] (큰 공극 둘 ↔ 작은 공극 160) → 우리 Hertz · Tabor 피복 몫 옆에 '가장 큰 덮이지 않은 조각 · 조각 수' 를 결과 전에 등록 | 자리: 단계 7 · 흐름 밖: 피복 정의 | 왜: 카드 §3-7 · §9-3 · Fig. 9 (`fig_9_right.png`)
- [m] bielefeld2022_li_kinetics_… | **PSD 는 부피 가중 꼬리와 함께 보고** — 수 6–7 % 의 큰 입자가 CAM 부피 42–62 % · 표면적 0.173 → 0.113 m² g⁻¹ (−35 %) · 큰 입자 속은 충전 끝에도 리튬화 [카드 산술 Fig. 5a · 인쇄 Table I · Fig. 6] → DEM 침대 · 실험 PSD 에 d > d₉₀ 부피 몫을 적는다 | 자리: 단계 5 · 흐름 밖: 입도 설계 | 왜: 카드 §3-5 · §9-4 · `fig_5a.png` · `tab_1.png`

## n — 논문 에이전트 후보 (카드가 인용 · 언급했지만 litdb 에 카드가 없는 것)
- [n] R. Ruess, S. Schweidler, H. Hemmelmann, G. Conforto, A. Bielefeld, D. A. Weber, J. Sann, M. T. Elm, and J. Janek, J. Electrochem. Soc., 167, 100532 (2020). (원문 ref 10 · SI [1]) | m · i — 이 논문의 모든 SOC 의존 입력 (GITT D̃ · EIS R_CT → j₀ · OCV · σ_SE 0.7 · 200 mAh g⁻¹) 과 검증 셀 (70 : 30 · 공극 14 %) 의 **원 측정** — 측정 조건 (압력 · 온도) 이 이 논문에 없다 · 카드 §3-2 · §12 | papers/ 목록 (ruess* 없음) · '100532' grep = benhadjali2025 · benhadjali2026 · doerrer2021 · stallard2022 · taghikhani2025 인용만 → 카드 없음 · **wishlist 에 이미 있음** (L88)
- [n] T. Ates, M. Keller, J. Kulisch, T. Adermann, and S. Passerini, Energy Storage Mater, 17, 204 (2019). (원문 ref 57) | i — 슬러리 · 미압연 NCM622/β-Li₃PS₄ 양극 공극 20–40 % 의 출처 (p.10) — 복합 양극 기공의 상한 쪽 실측 · 카드 §3-7 · §12 | papers/ 목록 (ates* 없음) · 'Kulisch' · '17, 204' grep = 다른 논문만 → 카드 없음 · wishlist 없음
- [n] M. Weiss et al., Adv. Energy Mater, 11, 2101126 (2021). (원문 ref 43 · 서지 일부만 — 원문 목록이 'et al.' 로 줄임) | m — R_CT = RT/(zFAj₀) (식 [12]) 와 j₀ 꼴 [11] 의 출처 · j₀ 를 옮길 때 면적 기준의 근거 · 카드 §3-1 · §12 | papers/ 목록 · '2101126' grep = 0 → 카드 없음 · wishlist 없음
- [n] M. Finsterbusch, T. Danner, C. L. Tsai, S. Uhlenbruck, A. Latz, and O. Guillon, ACS Appl. Mater. Interfaces, 10, 22329 (2018). (원문 ref 37) | m · h — 이 모델 꼴 (3D 미세구조 전기화학) 의 원형 · 카드 §3-1 · §12 | papers/ 목록 (finsterbusch* 없음) · '22329' grep = clausnitzer2024 · park2019 · park2020_dimension · pranami2015 인용만 → 카드 없음 · wishlist 없음
- (참고 · 후보로 세지 않음 — wishlist 에 이미 있음) ref 47 Conforto 2021 J. Electrochem. Soc. 168, 070546 (L132 · L519) · ref 8 Koerver 2017 Chem. Mater. 29, 5574 (L73 · L218 · L490) · ref 38 Neumann 2020 ACS AMI 12, 9277 (L121) · ref 58 Kim 2017 Nano Lett. 17, 3013 (L499) · ref 48 Märker 2019 Chem. Mater. 31, 2545 (L239).

## 카드 문제
- **`kim2024_optimal_cathode_composite_mechanical_mixing_se_coverage` L279** (가리킨 카드): S8 = 이 논문을 *"i₀,ref 0.05 A/m² 출처"* 로 적었으나 **원문에 0.05 A m⁻² 는 인쇄되지 않았다** — j₀ 는 SOC 의존 곡선 (Fig. 7a · 판독 0.017–0.155 A m⁻²) · 비교 상수 j₀,₁ 0.155 · j₀,₂ 0.090 A m⁻² (p.8) · 곡선이 0.05 를 지나는 곳은 ≈3.65 · ≈4.17 V 뿐 [판독].  같은 카드 L115 (표 S2 물성 줄) 의 i₀,ref 0.05 A/m² · D_s 5.5 × 10⁻¹⁴ m²/s 도 이 논문 값이 아니다 (이 논문 D̃ 최대 6.9 × 10⁻¹⁶ m² s⁻¹).  Kim 2024 논문 표 S2 의 인용 자체인지 카드의 귀속인지는 [미확인] — 고치지 않음.
- `lee2024_shear_force_dry_process_cathode_coverage` L390 (가리킨 카드): *"같은 질문의 3D 판"* — 3D 단일 입자 ✓ 이나 범위가 겹치지 않는다 (이 논문 남은 계면 ≥ 53 % · ≤ 0.5 C ↔ lee2024 2D 10–100 % · ≤ 5 C) · 설명 수준 · 값 문제 없음 — 고치지 않음.
- `taghikhani2025_electrochemomechanical_phase_field_fracture_assb_composite_cathode` L108: x₀ 0.9729 *"(Bielefeld et al., 2022)"* — 원문에 x₀ 인쇄 없음 (SI Fig. S2 OCV 표지 x 0.970 ↔ 3.601 V [판독]) · 그 논문 표를 옮긴 줄 — 고치지 않음.
- `benhadjali2026_oneway_chemomech_stress_stack_pressure_3d_assb_cathode` L405: δ_ion · i₀ · OCV · D 의 출처 = Bielefeld 2022 — 원문 표 S2 는 이 넷의 출처를 **Rueß 2020 [1]** 로 적는다 (Bielefeld 2022 = 2 차 출처) · 값 문제 없음 — 고치지 않음.
- `reisacher2023_percolation_sulfide_carbon_matrix` L60: 논문 번호 *"20539"* (원문 020539 · 앞 0 빠짐) — 서지 표기만 — 고치지 않음.

# 배치 28 — 정독 근거 (질문 a–m)

읽은 카드 7/7 (전부 끝까지): bucci2018 368 줄 · dem_mechanical 372 · gandla2026 455 · interfacial 408 · intergranular 410 · kang2025 333 · kim2023 379.
"줄" = 카드 사본 (`litdb_read/litdb/papers/<slug>.md`) 의 줄 번호. 표지는 카드에 적힌 그대로. [내 산술] = 카드 문제를 가리려고 이 조수가 한 한 줄 산술 (값으로 쓰지 말 것).
이 배치 7 장에 "인용 금지" 표지 없음 (전수 검색 0 건).
m 절의 줄인 이름: bucci2018 · dem_mechanical · gandla2026 · interfacial · intergranular · kang2025 · kim2023 (= 위 7 slug 의 앞부분).

## a. 순수 SE 압력별 기공 곡선 · 진밀도

이 배치에 없음 (순수 SE 압력별 기공 곡선 · 진밀도 값 0 건 — 7 장 전수 검색).
- (가까운 것) [a] interfacial_impedance_formulation_assb_cathode | 순수 SE 펠릿 (300 MPa) 은 이온 저항만: r_i,bulk 178 · r_i,gb 631 Ω·cm · E_a 0.33 eV (기공 값 없음) | §3 줄 83–86 (Fig 2a–d) | stated | Cl-rich Li₅.₇₅PS₄.₇₅Cl₁.₂₅ · 압력 한 점
- (가까운 것) [a] interfacial_impedance_formulation_assb_cathode | SE 부피분율 ε_i = 1.0 셀의 eps_pore 0.16 · 정의 = (펠릿 부피 − 성분 부피)/펠릿 부피 (FIB 단면 · 뺀 뒤) — 카드는 '복합셀' 로 표기 · 그 스윕의 성형 압력 카드에 없음 · 진밀도 값 없음 · 순수 SE 라면 랩 표준 (10–13 %) 과 다른 문헌 값 | §3 줄 94 · §5.2 줄 205 · §7 줄 281 | stated | 순수 SE 인지 카드에서 분명하지 않음 · 같은 ε_i 의 r_i 가 카드 안에서 두 값 (카드 문제)

## b. 압력을 뺄 때 되돌아오는 양과 잰 방법

- [b] dem_mechanical_stresses_ssb_electrode_cycling | 일축 375 MPa → 1 atm 점감 (relaxation): z 두께 84 → 95 µm (카드: "영구변형 + 탄성 회복") · 같은 단계 σ_el/σ_AM 0.072 → 0.032 ("significant decrease upon relaxation" · 접촉 끊김); 잰 방법 = DEM 상자 z 두께 (xy 150 µm 주기 고정) | §3.1 줄 66 · §4.4 줄 155 · §3.5 줄 109–110 (Fig 2 · Fig 6a) | digitized | 강체 구 Hertz DEM (실험 아님) · NMC532 + LPSCl · 기공률 미보고 · 다음 등방 단계는 xy 150 → 130 µm 로 바뀌어 두께로 견줄 수 없음 (줄 68)
- [b] gandla2026_layered_cathode_degradation_diagnostics_review | 측정법 경고: ex situ 분해 중 *"contact recovery under pressure, lithium redistribution, and stress relaxation can partially reverse"* → 실제 고장 상태를 가림 · 논쟁 5.2.5 의 결정 실험 = 같은 입자 operando → 완화 → 재측정 짝 비교 | §3-1 줄 64 (p.2–3) · §3-10 표 줄 198 (p.27) | [인쇄] | 회복 양 수치 없음 · 총설 (2 차)
- [b] intergranular_cracking_nmc811_jmca2023 | 측정법 경고: FIB-SEM 처럼 입자를 잘라 보면 잔류응력이 풀림 → 같은 입자를 비파괴 CT 로 충전 전 · 후 두 번 (탭 형상으로 같은 RoI 재추적) | 머리 줄 65–67 · §A-1 줄 289 | 카드 서술 | 탈압 회복 값 없음 · 액체계 LIB
- (가까운 것) [b] kim2023_chemomech_failure_highstrain_anode | 150 사이클 뒤 250 MPa 재가압 → 방전용량 25.2 → 38.3 mAh/g 만 회복 (불완전 = 비가역 손상 해석) · R_int 약간 ↓ | §5 줄 231–232 · §7 줄 275 (Fig S13–S14) | 그림 / 본문 근사 (줄 365) | 재가압 (제하 아님) · NCA · 사이클 뒤

## c. 항복 · 경도 · 크리프 값과 정의 (일축 항복 환산 여부)

- [c] bucci2018_mechanical_instability_interface_delamination | 항복 정의: 구대칭에서 von Mises ≡ Tresca → σ_θθ − σ_RR = σ_yield · 개시 변형 (αc)_plastic = −(f³−1)νσ_yield/[3f³λ(2ν−1)] (Eq 13) · 기준 σ_yield < 0.5·F_c (Eq 14 · F_c = 2–20 GPa @ ‖u‖_R 1 nm) — σ_yield 값 자체는 없음 (σ_yield/F_c 비 스윕) | §4.4 줄 163–174 · §3.2 줄 48–49 (Fig 7) | stated | 소재 무관 · 1D 구대칭 · 일축 시험 값으로 환산하는 별도 식 없음 (같은 σ_yield 를 씀)
- [c] kang2025_toughened_bimodal_nca_lzo | 항복 · 경도 없음; FEM 탄성 입력 E_NCA 175 · E_LPSCl 22.1 GPa · cohesive 계면 강도 100 MPa · G_c 1 J/m² · 손상 개시 = 2 차 nominal stress 기준 (압축은 Macaulay 로 제외) | §3 줄 60–61 · Table S4 줄 130–131 · §4 줄 168–169 | stated (SI verbatim) | 2D FEM 입력값 (측정 아님) · NCA
- [c] kim2023_chemomech_failure_highstrain_anode | 항복 · 경도 없음; FEM 입력 E NCA 175 / LPSCl 22.1 GPa (ref [39]) · σ_Mises 값 미명시 ("입계에서 더 빠르게 증가 → 소성/균열") | §3 줄 77 · 91 | stated · 정성 | 카드 안 E 표기 충돌 (카드 문제)
- [c] intergranular_cracking_nmc811_jmca2023 | 항복 없음 (1 차입자 = 등방 선형탄성); FEM 입력 E_p 150 GPa · CBD E_c 0.3 GPa · ν 0.3 · 입계 / 입내 파괴 인성은 보조장 γ 로 나눔 (값 카드에 없음); 카드가 다른 논문 값으로 Jung2023 다결정 경도 113 MPa 인용 | §3 줄 90–91 · §4-B 줄 139 · 153–155 · §A-4 줄 320 | stated · (113 MPa = 다른 카드 값) | NMC811 · 액체계
- [c] dem_mechanical_stresses_ssb_electrode_cycling | σ_y · 소성 · 균열 = n/a (강체 구 + Hertz) · GFF 물성 (E · ν · 마찰 · COR) 은 refs [30,31] · SI 에만 (카드에 값 없음) | §3.6 줄 127 · §4.0 줄 139 · §6 줄 234 | 카드 서술 | —
- [c] interfacial_impedance_formulation_assb_cathode | 항복 값 없음 — 저자 정성 "낮은 모듈러스 SE (LPSC)" 만 | §4.5 줄 186 | 저자 명시 (카드 옮김) | 값 없음
- [c] gandla2026_layered_cathode_degradation_diagnostics_review | 항복 값 없음 — AFM DMT 탄성률 (1.0 GPa · 100 MPa 등) 은 고분자 전해질 셀 CEI 값 | §3-6 줄 136 (그림 6f–g) | [인쇄] | 다른 계 · 역학 항복 아님

## d. 단단한 + 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

- [d] dem_mechanical_stresses_ssb_electrode_cycling | 일축 375 MPa: 평균 AM 응력 ≈ 2 × SE (*"stress on SE reduced by factor of two w.r.t. AM, due to deformability + lower mechanical stiffness of SE"*) · AM z 응력 ~500–700 MPa 로 경계압 375 MPa 를 넘음 (카드: bulk 가 위 · 아래 판 압력을 같이 받음) · 바닥 · 윗면 층 응력 낮음 · 작은 AM 일수록 응력 큼 (2 µm ~390 → 6 µm ~250 MPa, x/y) | §3.2 줄 76–80 · §5.3 줄 198 (Fig 4) | stated (2×) · digitized | NMC532 26.7 wt% · SE 가 AM 보다 큼 · 강체 Hertz (카드: 소성 캡이 없어 응력 과대 가능 · 줄 322)
- [d] dem_mechanical_stresses_ssb_electrode_cycling | 등방 5 MPa · 사이클: 방전 (AM 팽창) 때 AM–SE 응력 차 벌어짐 → 충전 (AM 수축) 때 응력이 SE 로 이전 · 더 고르게 | §3.4 줄 98–104 (Fig 5a) | stated | 응력 수치 = 6–16 MPa 범위만
- [d] interfacial_impedance_formulation_assb_cathode | 일축 (UP-C · SUS 판) 은 단단한 CAM 에 응력이 몰려 SE 변형이 등방 (IP-P) 보다 적음 (대신 CAM 전자 접촉 ↑ · r_e UP-C/IP-C < IP-P) · SE 분율 ↓ → 공극 ↑ (단단한 NCM 이 SE 치밀화 방해) | §4.5 줄 187 · §5.3 줄 217 · §5.2 줄 205 | 카드 해석 · stated | Cl-rich LPSC · 하중 몫 수치 없음
- [d] gandla2026_layered_cathode_degradation_diagnostics_review | [104]: NCM 비율 ↑ → NCM–NCM 배위수 ↑ → 부피 변화 때 이웃이 입자를 붙잡아 전달 하중 ↑ · 단층촬영 형상 메조 모델 고응력 영역 비선형 증가 | §3-5 줄 121 (p.14 · 그림 5g–h) | [인쇄] · [판독] | 사이클 부피 변화 하중 (가압 아님) · 2 차 인용 · 원 논문 카드 없음
- (가까운 것) [d] kang2025_toughened_bimodal_nca_lzo · kim2023_chemomech_failure_highstrain_anode | 제조압 400 MPa (kang2025 Fig S9) · 433 MPa (kim2023 Fig S15) 직후 단면 SEM 에 NCA 균열 없음 · 사이클 균열에서 stack pressure (수백 MPa) ≪ 확산 유발 응력 (GPa) | kang2025 §5 줄 221 · §4 줄 182–183 · kim2023 §5 줄 233 · §3 줄 92 | stated | NCA (≠ NMC811) · 하중 몫 수치 없음

## e. 점접촉 법칙이 깨지는 범위와 대안 · 맞춘 값 수

multi-contact · MDR · EEPA · Thornton-Ning · Storåkers: 이 배치에 없음.
- [e] dem_mechanical_stresses_ssb_electrode_cycling | 점접촉 = Hertz (GFF) 만 · 대안 없음 · 이 논문 안 맞춘 값 0 (E · ν · 마찰 · COR 는 refs [30,31]) · 큰 변형 범위 논의 없음; 카드 해석: 소성 캡이 없어 일축 응력 과대 가능 | §4.0 줄 139 · §B.5 줄 322 · §9 줄 366 | 카드 서술 · 카드 해석 | —
- (가까운 것) [e] bucci2018_mechanical_instability_interface_delamination | 연속 계면의 cohesive 법칙 (입자 점접촉 아님): G(‖u‖) = F_c(‖u‖ − F_c‖u‖²/(4γ)) · 선형 traction-separation · ‖u‖_R = 2γ/F_c · 맞춘 값 0 (F_c · γ · ‖u‖_R 스윕) | §4.2 줄 126–136 (Eq 8–9) | stated | 입자 접촉 법칙 아님
- (가까운 것) [e] kang2025_toughened_bimodal_nca_lzo | 입계 cohesive zone (두께 0 요소 · bilinear TSL · 혼합모드 d_m · damage D 0 → 1) · 입력 2 개 (강도 100 MPa · G_c 1 J/m² · refs S3 · S4) | §4 줄 166–176 · Table S4 줄 130–131 | stated | 입계 법칙 · 2D

## f. MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙 · 수치 오차

이 배치에 없음 (MPM 을 쓴 카드 없음).
- (가까운 것 · MPM 아님) [f] dem_mechanical_stresses_ssb_electrode_cycling | DEM → 복셀 0.5 µm (AM 3–10 µm · SE 6–13 µm) · AM–SE 겹침 복셀은 영률 높은 쪽 (AM) 에 배정 · z 1 V / Δc · 측방 주기 · 해상도 수렴 시험 카드에 없음 | §4.7 줄 168–169 | stated | 수송 후처리
- (가까운 것 · MPM 아님) [f] intergranular_cracking_nmc811_jmca2023 | phase-field FEM ~4 M 요소 · 13 M DOF · MUMPS · 2 차 backward Euler + time-step sensitivity · CT 화소 ~124 nm 아래 균열은 해상 못 해 부분 부피로 간접 보정 | §4-B 줄 134–135 · §3 줄 93 · §6 줄 189–190 | stated | 오차 크기 카드에 없음
- (가까운 것 · MPM 아님) [f] bucci2018_mechanical_instability_interface_delamination | FPT: 입자 표면 2160 삼각형 · walker 1000 · step = 반경의 1 % | §4.5 줄 178 | stated | 이산화 오차 추정 카드에 없음

## g. 2D 결과를 3D 로 옮길 때의 경고 · 증거

- [g] dem_mechanical_stresses_ssb_electrode_cycling | 서론: *"lack of comprehensive 3D models that address material interfaces and mechanics remains a gap"* · 3D 모델이 계면 진화 · 공극 형성 이해에 필요 (refs [11,21]) · 이 논문은 3D (카드: So 2021 · Bucci 는 2D) | §5.1 줄 191–192 · §4.9 줄 182 | stated · 카드 서술 | 2D ↔ 3D 정량 비교 없음
- [g] kang2025_toughened_bimodal_nca_lzo · kim2023_chemomech_failure_highstrain_anode | FEM 이 2D (Voronoi · 12.5 µm 도메인) — 3D 로 옮기는 경고 · 근거 카드에 없음 | kang2025 §2 줄 49 · §4 줄 152–153 · kim2023 §2 줄 66 · §4 줄 167–168 | stated | —
- (가까운 것) [g] gandla2026_layered_cathode_degradation_diagnostics_review | 척도 이전 경고: 얇은 모델 전극에서 얻은 감소 원인 배분을 후막으로 그대로 옮길 수 없다 · 원자 척도 결론 = 입자 몇 개 ↔ 파우치 수십억 | §3-10 줄 187 · 189 (p.26–27) | [인쇄] | 2D/3D 이전 아님
- (가까운 것) [g] intergranular_cracking_nmc811_jmca2023 | 단면 (잘라 보기) 관찰은 잔류응력을 풀어 균열을 바꿀 수 있음 → 3D 비파괴 CT | 머리 줄 65–67 | 카드 서술 | —

## h. DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

이 배치에 DEM → FE · MPM 기계 넘김 선례 없음.
- (가까운 것) [h] dem_mechanical_stresses_ssb_electrode_cycling | 단계마다 (일축 · relax · 등방 · D1–C5) DEM 입자 → 복셀 (0.5 µm) → GeoDict 수송 (σ_el · τ) | §4.7 줄 168–169 · §7 줄 243 | stated | 수송만
- (가까운 것) [h] intergranular_cracking_nmc811_jmca2023 | X-ray CT 실입자 형상 → Rhino Voronoi 400 1 차입자 (+ 20 µm CBD 껍질) → COMSOL phase-field (영상 → FE) | §4-B 줄 136–138 | stated | DEM 아님
- (가까운 것) [h] gandla2026_layered_cathode_degradation_diagnostics_review | 단층촬영 미세구조 → 메조 화학-기계 모델 [104] · 전망 3 단계 (MLIP → FIB-SEM/XCT 또는 GAN 형상 위 메조 모델 → 셀 트윈) · 카드 [추정]: 공정 모의 (DEM 압축) 가 형상을 만드는 길은 목록에 없음 | §3-5 줄 121 · §3-11 줄 209 · §7-1 줄 315 | [인쇄] · [추정] | DEM 아님

## i. 복합 양극 (AM + SE) 의 압력별 기공

- [i] interfacial_impedance_formulation_assb_cathode | Cl-rich LPSC + NCM90 (ε_i 0.58): IP-P 500 MPa eps_pore 0.046 · UP-C 가 가장 높음 (값 카드에 없음) · bimodal NCA-b-12 (500 MPa 풀셀) 0.11 · SE 분율 스윕 eps_pore 0.16 → 0.23 (압력 카드에 없음) | §3 줄 94 · 99 · 107 · §5.3 줄 215 (Fig 4d · 3b · 6e) | stated | 뺀 뒤 펠릿 · 정의 = (펠릿 − 성분)/펠릿 · 압력 축 수치는 점 하나 · 조성 다름
- [i] kang2025_toughened_bimodal_nca_lzo | NCA : LPSCl : SP 72:27:1 · 0.15 g · 10 mm · 400 MPa 펠릿 두께 U 0.74 · B 0.68 · LZO-B 0.67 mm · 부피 로딩 ~1.87 vs ~2.02 (1.1×) — 기공률 미보고 | §3 줄 63–64 · Fig S2 줄 214 | stated (표지 충돌 — 카드 문제) | 기공 아님 · 단위 표기 둘
- [i] dem_mechanical_stresses_ssb_electrode_cycling | NMC532 + LPSCl DEM 두께만: 84 (375 MPa) → 95 (1 atm) → 125 µm (등방 · xy 130 µm) · 기공 미보고 | §3.1 줄 65–67 · §3.6 줄 122 | digitized | 시뮬 · 두께 ≠ 기공
- (가까운 것) [i] gandla2026_layered_cathode_degradation_diagnostics_review | NMC/LPS 복합 공극 < 3 → 9.5 % (50 사이클 · FIB-SEM [60]) · 표 5 의 압력 범주 (제작 수십–수백 · operando 수십 · 실용 ≤ 2 MPa) | §3-5 줄 118 · §3-10 표 줄 183 | [인쇄] | 압력 축 아님 · 2 차 인용

## j. 카드가 스스로 적은 "아직 못 한다 · 한계" 중 가압 · 탈압과 닿는 것

- [j] dem_mechanical_stresses_ssb_electrode_cycling | AM 크기 변화를 균일하게 둠 (저자: 실제는 불균일 · 대칭 충방전 가정) · lithiated/delithiated AM 전도도 변화 미보정 → 값은 기하만 · full electro-mechanical coupling = 계산비용으로 보류 · 등방 1 MPa 아래 σ_el ↓ · 최적 등방압은 더 다듬어야 · τ 비단조 원인 "further investigation needed" | §4.6 줄 163 · §3.5 줄 116 · §5.1 줄 192 · §5.4 줄 204–205 | stated | —
- [j] gandla2026_layered_cathode_degradation_diagnostics_review | ≤ 2 MPa · > 4 mAh/cm² 에서 장기 검증된 코팅 없음 · operando 셀 = 작은 나사로 조여 정부피 → 내부 압력 계속 변함 · 필요한 셀 = *"one that can impose a low target pressure precisely and hold it constant during operation"* · 적층압을 고정 · 균일 조건으로 읽지 말 것 · 변형 문턱 ~2.5 % 일반화 미검증 | §3-11 줄 208 (p.29) · §3-10 줄 188 (p.26) · §3-5 줄 123 · 118 (p.14 · p.12) | [인쇄] | 총설
- [j] intergranular_cracking_nmc811_jmca2023 | 단일입자 FEM 이 중심 큰 공극 · 13–25 % 부피팽창을 재현 못 함 → 제조 (고온 소결) 잔류응력 탓으로 추정 (future work) · 외부 압력 항 없음 · CBD/입자 박리 미포함 · SC · SSE 확장 = 향후 | §4-B 줄 162–168 · §10 줄 260–262 · 268–269 | stated · 카드 서술 | —
- [j] kang2025_toughened_bimodal_nca_lzo | 계산부담 때문에 Li 확산 · 삽입 변형 등방 가정 · 입자 완전 방전 균일 출발 · AM 반경 5 µm 대표값 · 사이클 균열에서 stack pressure 기여 미미 (본문) | §4 줄 157–158 · 182–183 · §10 줄 327–328 | stated | —
- [j] kim2023_chemomech_failure_highstrain_anode | FEM 주결과 = 응력장 (균열은 입계 von Mises 증가로 추론) · 재가압이 접촉을 일부만 회복 (비가역 손상) · 작동 100 MPa 가 300 사이클 안정 (250 MPa 대비) | §10 줄 353–355 · §7 줄 275–276 · §5 줄 235 | stated · 그림 | —
- [j] bucci2018_mechanical_instability_interface_delamination | rate-independent (충전율 의존 = 향후) · 벌크 / SE 분해 경쟁 = 향후 · Vegard 선형 등방 가정 | §5.1 줄 199 · §5.2 줄 202 · §10 줄 361 · 364 | stated | —
- [j] interfacial_impedance_formulation_assb_cathode | 저자 한계 서술 카드에 없음 · 카드 주의 = 제조 300–500 MPa ≠ 작동 4 MPa · r_i,gb 는 압밀된 구조를 잰 값 | §12 줄 385 | 카드 서술 | —

## k. DEM 의 한계 (인용 서지 병기)

- [k] dem_mechanical_stresses_ssb_electrode_cycling (M. Alabdali, F.M. Zanotto, M. Chouchane, A.C. Ngandjong, V. Viallet, V. Seznec, Y.S. Meng, A.A. Franco, *Energy Storage Materials* 70 (2024) 103527, doi 10.1016/j.ensm.2024.103527) | 입자 모양 · 겹침 · 접촉 독립 가정의 한계를 논문이 말한 문장 = 카드에 없음 (말 없음); 논문이 적은 한계는 사이클 쪽: *"In real systems, the size change of AM does not occur uniformly because of the heterogeneity in interfaces and AM active surface → heterogeneous (de)lithiation kinetics. ... we assume the DEM model captures the effects ... symmetrical charge/discharge profiles anticipated, without difference in potential values since AM revert to original size after each step (homogeneous AM size change)."* (카드 인용 · 화살표 · 줄임은 카드 것) · *"we are not accounting for the change of electronic conductivity of AM in lithiated/delithiated states → resulting values attributed to changes in geometry only"* · τ 비단조: *"May be attributed to lower pressure allowing easier particle rearrangement; further investigation needed."* | §4.6 줄 163 · §3.5 줄 116 · §5.4 줄 204 | stated (카드 인용) | 원문 쪽 번호 카드에 없음 → 인용 전 원문 대조
- [k] dem_mechanical_stresses_ssb_electrode_cycling (같은 서지) | 카드 해석 (논문 문장 아님): 강체 구 + Hertz → 소성 · 항복 · 균열 없음 · 사이클 '팽창' = 구 반경 키움 (형상 흐름 아님) · 소성 캡이 없어 일축 응력 과대 가능 | §4.8 줄 173 · §B.5 줄 322 · §9 줄 366 | 카드 해석 | 인용용 아님
- [k] bucci2018_mechanical_instability_interface_delamination (G. Bucci, B. Talamini, A. Renuka Balakrishna, Y.-M. Chiang, W.C. Carter, *Phys. Rev. Materials* 2 (2018) 105407) · gandla2026_layered_cathode_degradation_diagnostics_review (D. Gandla et al., *Adv. Energy Mater.* 2026, e71528) · interfacial_impedance_formulation_assb_cathode (W. Choi et al., *ACS Appl. Mater. Interfaces* 16 (2024) 26066–26078) · intergranular_cracking_nmc811_jmca2023 (H.C.W. Parks et al., *J. Mater. Chem. A* 11 (2023) 21322–21332) · kang2025_toughened_bimodal_nca_lzo (J. Kang, H.R. Shin et al., *ACS Appl. Mater. Interfaces* 17 (2025) 60558−60567) · kim2023_chemomech_failure_highstrain_anode (J. Kang, H.R. Shin et al., *Energy Storage Mater.* 63 (2023) 103049) | DEM 미사용 — 해당 없음 (gandla2026 = DEM · MPM 언급 0 건) | gandla2026 §4-2 줄 257 | — | bucci2018 줄 190 의 "계면 박리 = 우리 DEM · MPM 둘 다에 없는 메커니즘" 은 카드 해석

## l. 소성변형이 왜 어려운가 · 택한 우회와 그 값 (인용 서지 병기)

- [l] dem_mechanical_stresses_ssb_electrode_cycling (Alabdali et al., *Energy Storage Materials* 70 (2024) 103527) | 어려운 이유를 논문이 설명한 문장 = 카드에 없음; 우회 = 소성 자체를 두지 않음 (강체 구 + Hertz · 사이클 = AM 반경 ±6 % 부피 swing — 카드: "재료가 흐르는 게 아니라 구가 커짐"); 맞춘 값 = 이 논문 안 보정 없음 (GFF E · ν · 마찰 · COR 는 refs [30,31] · SI); 검증 = 실험 없음 (ref [28] 프로토콜 모사) · 2 seed; 비용 = 11,002 입자 · 40 코어 1 노드 · 375 GB RAM · 일축 ~400 µs (800 µs 와 차이 없음) · 벽시계 시간 카드에 없음 | §4.8 줄 173 · §4.0 줄 139–140 · §4.3 줄 151 · §2 줄 52 | stated · 카드 서술 | —
- [l] bucci2018_mechanical_instability_interface_delamination (Bucci et al., *Phys. Rev. Materials* 2 (2018) 105407) | 입자 계산의 소성 난점 = 말 없음; 우회 = 1D 구대칭 연속체 — AM 을 풀지 않고 반경 변화를 부과 변위로 · SE 껍질 J2/Tresca 탄소성 (소성 흐름이 계면 응력을 풀어 박리 방지) · 형상 · PSD · 접촉망 없음; 맞춘 값 = 0 (E · ν · γ · F_c · σ_yield/F_c 스윕); 검증 없음; 비용 = 닫힌 해 + walker 1000 | §4 줄 90 · §4.4 줄 164–174 · §4.6 줄 187–188 · §10 줄 358 | stated · 카드 서술 | —
- [l] intergranular_cracking_nmc811_jmca2023 (Parks et al., *J. Mater. Chem. A* 11 (2023) 21322–21332) | 말 없음; 우회 = 1 차입자 고정 형상 등방 선형탄성 + 입계 phase-field AT2 취성 손상 (γ 로 입계 인성 낮춤) · 소성 없음; 값 = 입력 E_p 150 · E_c 0.3 GPa · ν 0.3 (맞춤 서술 없음); 검증 = 모델 · 실험 전압곡선 일치 (Fig 5c) · 중심 큰 공극 · 13–25 % 팽창은 재현 못 함; 비용 = ~4 M 요소 · 13 M DOF · 시간 카드에 없음 | §4-B 줄 134–166 · §5 줄 177 | stated | 액체계 · 단일입자
- [l] kang2025_toughened_bimodal_nca_lzo (Kang, Shin et al., *ACS Appl. Mater. Interfaces* 17 (2025) 60558−60567) | 말 없음 — 단, 계산부담 절감 위해 Li 확산 · 삽입 변형을 등방으로 가정 (카드 옮김); 우회 = 2D 선형탄성 + 확산 유발 변형 ε_d = (Ω/3)Δc + 입계 cohesive zone · 입자 형상 고정 · 소성 없음; 값 = 입력 (Table S4 · refs) · 맞춤 서술 없음; 검증 = 100 cyc 큰 입자 균열 SEM (정성); 비용 카드에 없음 | §4 줄 154–158 · 163–176 | stated | NCA · 2D
- [l] kim2023_chemomech_failure_highstrain_anode (Kang, Shin et al., *Energy Storage Mater.* 63 (2023) 103049) | 말 없음; 우회 = 2D 선형탄성 + ε_d · 음극 부피 변화를 윗면 견인력 (n·σ_yy = −P_app) 으로 · 계면 불균일 = 비활성 경계의 i₀ 낮춤 · 균열 모델 없음 (응력장에서 추론); 값 = 입력 (Table S1 · refs S3–S5); 비용 카드에 없음 | §4 줄 164–192 · Table S2 줄 153–157 | stated | NCA · 2D
- [l] gandla2026_layered_cathode_degradation_diagnostics_review (Gandla et al., *Adv. Energy Mater.* 2026, e71528) | 입자 계산 없음; 모델 쪽 문장: *"DFT/MD cannot reach the time and length scales of interphase growth, while finite-element models rest on assumed rather than measured constitutive inputs."* · 실물 쪽: 고체 SE 는 단단하고 흐르지 않아 활물질 표면 모양 변화를 따라가지 못함 → 접촉 불완전 · 불균일 (카드 옮김) | §3-11 줄 209 (p.29) · §3-1 줄 63 (p.2) | [인쇄] | 총설 · 우리 frame (LPSCl 연성) 과 결이 다른 일반 서술
- [l] interfacial_impedance_formulation_assb_cathode (Choi et al., *ACS Appl. Mater. Interfaces* 16 (2024) 26066–26078) | 입자 계산 없음 (회로 · 측정); 소성 관련 실험 관찰: "낮은 모듈러스 SE (LPSC) 가 fluidic-media (등방) 가압으로 pristine 펠릿 수준까지 치밀화" (저자 명시 · 카드 옮김) · IP-P 500 MPa 85 °C τ_eff² 1.46 | §4.5 줄 186 · §3 줄 101 | stated | Cl-rich LPSC

## m. 받아들일 통찰

(bucci2018)
- [m] bucci2018 | 해석해 단위 시험: 중공 구 (내경 부과 변위 u(R_A) = αcR_A · 외경 u = 0) 의 탄성 Lamé 해 (Eq 3–6) 와 J2/Tresca 항복 개시 (αc)_plastic (Eq 13) → U3 인접 (단단한 심 + 무른 SE 껍질) 3D 탄소성 검증 기준 · 근거 §4.1 줄 92–118 · §4.4 줄 163–168 | stated | 3D 구대칭 전용 (2D 판은 원통 해가 따로 필요 — 카드에 없음)
- [m] bucci2018 | 관측량: 같은 50 % 박리라도 연속 patch → FPT 평균 ×2.75 · std ×5 · 흩어진 patch → 훨씬 작음 = 수송은 면적뿐 아니라 연결성에 달림 → 단계 7 (피복 정의): 피복률과 함께 피복 patch 연결성 (patch 수 · 최대 patch 몫) 을 결과 전에 관측량으로 등록 · 근거 §4.5 줄 179–183 (Fig 8a,b) | stated | 상대 비 · 확산 random walk
- [m] bucci2018 | 규칙: 박리 개시식 (Eq 10) 에 입자 크기가 없음 (*"fracture cannot be alleviated by simply choosing a smaller particle size"*) · 크기는 전파 안정성 (A_crit/‖u‖_R, Eq 12) 에만 → 흐름 밖: 사이클 박리 원장 (A10) 에서 입경별로 개시 기준을 바꾸지 말고 전파 양식 (급격 / 점진) 만 가른다 · 근거 §4.2 줄 142 · §5.3 줄 208 · §4.3 줄 150–161 | stated | F_c · ‖u‖_R 미지

(dem_mechanical)
- [m] dem_mechanical | 유지 시간 수렴 규칙: 판 위치 · 판 힘 · 입자 위치가 일정해질 때까지 · 400 µs vs 800 µs 차이 없음 → 400 채택 (= 유지 시간을 두 배로 늘려 같음을 확인) → 단계 4 · 단계 5: 가압 끝 판정에 '유지 2 배 대조' 를 결과 전 등록 · 근거 §4.3 줄 151 | stated | 차이 크기 카드에 없음
- [m] dem_mechanical | 함정 (기공 연산자): 등방 단계에서 xy 150 → 130 µm 로 줄며 z 두께는 95 → 125 µm 로 '늘어남' — 카드: "porosity 절대값을 thickness 단독으로 읽지 말 것" → 단계 0: 기공은 상자 부피 (횡 치수 포함) 로 정의 · 횡 경계가 바뀌는 단계에서 두께 지표 금지 · 근거 §3.1 줄 67–68 · §3.6 줄 122 | digitized · 카드 서술 | —
- [m] dem_mechanical | 응력 판독 규칙: 판 근처 (바닥 · 윗면) 층은 응력이 낮고 bulk 가 높음 · AM z 응력 (500–700 MPa) 이 경계압 375 MPa 를 넘음 → 조건 R1 · 단계 5: 하중 몫 · 응력 통계를 벽 접촉층과 bulk 로 나눠 보고하고 경계압과 입자 평균 응력을 같은 양으로 두지 않는다 · 근거 §3.2 줄 76–79 (Fig 4) | stated · digitized | 강체 Hertz · SE > AM 크기
- [m] dem_mechanical | 실험 대조 산포: 같은 시료 σ_ion 의 실험실 간 측정 1.3–5.8 mS/cm (RSD 35–50 %, ref [39]) → 흐름 밖: 실험과의 대조 — 단일 실험 σ 값과의 차이를 판정할 때 이 산포를 띠로 둔다 · 근거 §5.4 줄 205 | stated (2 차 인용) | ref [39] 원문 · 시료 조건 카드에 없음

(gandla2026)
- [m] gandla2026 | 경계 조건: 운전 셀은 작은 나사로 조여 사실상 정부피 → 충방전 부피 변화가 내부 압력을 계속 바꿈 · 적층압을 고정 · 균일 조건으로 읽지 말 것 → 단계 6: 탈압 뒤 (운전) 상태의 경계를 '정부피 (변위 고정)' 인지 '정응력 (servo)' 인지 결과 전에 적는다 (카드 §7-3 도 같은 지적) · 근거 §3-10 줄 188 (p.26) · §3-5 줄 123 (p.14) · §7-3 줄 332 | [인쇄] · [추정] | 총설
- [m] gandla2026 | 표지 규칙: ex situ (분해 뒤) 측정은 압력 아래 접촉 회복 · Li 재분포 · 응력 완화가 일부 되돌아가 고장 상태를 가림 → 결과 전 대조 항목: 실험값마다 '누른 채 (operando) / 뺀 뒤 (ex situ)' 표지를 붙여 같은 쪽끼리만 견준다 · 근거 §3-1 줄 64 (p.2–3) · 5.2.5 줄 198 | [인쇄] | —
- [m] gandla2026 | 대조 관측량: XCT NCM–NCM 배위수 분포 (빈도 vs CN · NCM811/LPSCl 70:30 · 80:20 · 85:15 → 최빈 ≈4.5 · ≈5.3–5.5 · ≈5–6.5 · 꼬리 ≈12 → ≈17–18) → 단계 5 · 결과 전 대조 항목 (모양 · 이동 방향만 · 질량/부피 기준 · 분해능 · 접촉 판정 [미확인] 을 같이 적음) · 근거 §3-5 줄 121 · §7-4 줄 334–338 (그림 5h) | [판독] ±0.5 CN | 원 논문 [104] 카드 없음
- [m] gandla2026 | 함정 (용어): 총설이 'tortuosity' 를 정의 없이 씀 (기하 τ 인지 수송 tortuosity τ² 인지 불명) → 단계 7: 문헌 tortuosity 를 견주기 전에 정의 (최단 경로 · 확산 √ · τ²) 를 확인하고 우리 τ 명명 규약으로 다시 붙인다 · 근거 §6 줄 306 | [미확인] | —

(interfacial)
- [m] interfacial | 진단법: 이온 차단 대칭셀 (SUS | 복합 | SUS) EIS 로 r_i,bulk · r_i,gb 를 가르고 SE 분율 의존을 τ² = ε^(−α) 로 맞춰 α_bulk 0.52 (≈ 이상 0.5) vs α_gb 4.3 → '경로 신장' 과 '입계 성장' 을 판별 → 흐름 밖: 접촉망 수송 — 우리 망의 bulk 항 (CF) · 협착 항 (FULL 대비) 의 SE 분율 의존을 같은 꼴로 내 실험 지수와 방향만 견줌 · 근거 §4.3 줄 165–174 · §5.2 줄 207 (Fig 3d) | stated | Cl-rich · 경험 지수
- [m] interfacial | 결과 전 대조 문장: 같은 압력이면 등방 (IP-P) 이 일축 (UP-C) 보다 기공 · 입계 저항이 작음 (r_i,gb UP-C 300 8 700 → IP-P 500 2 650 Ω·cm · IP-P 500 eps_pore 0.046) · 일축 SUS 판은 단단한 CAM 에 응력 집중 → 단계 4 · 단계 5: 실험 기공 기준을 고를 때 가압 방식 (일축 · 등방 · 온도) 을 같이 적는다 · 근거 §4.5 줄 183–187 · §5.3 줄 212–218 | stated · digitized | 우리 계산 = 일축 판
- [m] interfacial | 방향 대조: SE 분율 ↓ → 공극 ↑ (0.16 → 0.23) · 작은 CAM → 공극 ↑ (Roller · 비균질 응집) · bimodal 이 공극 최저 (0.11) → 단계 5 결과 전 대조 항목 (방향만) · 근거 §5.2 줄 205 · §5.4 줄 225–228 | stated | 절대값 전이 금지 (조성)
- [m] interfacial | R_ct 스케일링: r_i/e ∝ 1/A_CAM (NCA · 0.082 Ω·cm⁵) → 흐름 밖: R_int ② — 전하 이동 항을 피복 면적 위에 k/A 로 얹는 형식 (k 는 NCM811/LPSCl 값 따로 · NCA 기울기 전이 금지 · 카드 줄 384) · 근거 §4.4 줄 178 · §9 ③ 줄 333 | stated | —

(intergranular)
- [m] intergranular | 함정 (기공 연산자): 화소 ~124 nm 아래 균열은 분할 못 함 → 분할 균열은 부피 증가의 일부 (best ~70 %) 만 설명 · 나머지는 부분 부피 (두 상 섞인 복셀의 강도 저하) 로 간접 → 단계 0: 복셀 · 분할 기공률은 복셀 이하 공극을 놓치므로 하한 표지 또는 부분 부피 보정 규칙을 결과 전에 정함 · 근거 §3 줄 88 · 93 · §6 줄 189–190 | stated | 액체계 CT
- [m] intergranular | 관측법: 같은 입자를 비파괴 CT 로 전 · 후 두 번 (탭 형상 · 같은 RoI) — 잘라 보는 FIB-SEM 은 잔류응력을 풀어 균열을 바꿈 → 결과 전 대조 항목 (탈압 뒤 구조 · 균열의 실험 대조는 비파괴 · 같은 시료 전후 꼴을 우선) · 근거 머리 줄 65–67 · §4-A 줄 119–127 | stated · 카드 서술 | —
- [m] intergranular | 부호 함정: 다결정 2 차입자 겉보기 부피 +19 % (균열 공극) ↔ 단위격자 −5 % → 흐름 밖: A10 사이클 원장 (AM 반경 swing 의 부호 · 크기를 격자값으로 정하지 않음 · 다결정은 공극이 지배) · 근거 §1 줄 34–38 · §3 줄 83–85 | stated | 제조 잔류응력 몫 미분리 (줄 260–262)
- [m] intergranular | 방법: phase-field 에 보조장 γ (γ = 1 입계 · 0 입내) + h = (1−γ)² 로 입계 · 입내 파괴 에너지를 나눠 균열이 입계를 따르게 함 · 손상 비가역 (history field) → 조건 R7 (AM 파괴 표현 후보) · 근거 §4-B 줄 150–156 | stated | 값 카드에 없음

(kang2025)
- [m] kang2025 | 결과 전 대조 항목 (조건 R7): 400 MPa 제조 직후 단면 SEM 에 NCA 균열 없음 (Fig S9) — 300 MPa 압밀 파괴 예측 (카드 줄 268 의 '우리 DEM 8 mAh 37–40 % cracked' 류) 과 견줄 기준 · 근거 §5 줄 221 | stated | NCA 3/10 µm (≠ NMC811)
- [m] kang2025 | CZM 규칙: 손상 개시 2 차 기준 (⟨σ_t⟩/σ_t^c)² + (σ_s/σ_s^c)² = 1 에서 Macaulay 괄호로 압축 법선응력은 손상에 기여 안 함 → 조건 R2 · R7: 가압 중 계면 · 입계 분리를 다룰 때 압축이 손상을 만들지 않게 · 근거 §4 줄 168–169 (S5) | stated | —
- [m] kang2025 | 경계 표기: 윗면 견인력 n·σ_yy = −P_app · 나머지 n·u = 0 (Table S5) → 단계 6: 탈압을 '견인력 P → 0' 으로 적는 선례 (판 분리 U4 와 따로) · 근거 §3 줄 133–142 | stated | 2D FEM
- [m] kang2025 | EIS 서명: R_ion 거의 불변 (5.7 → 6.7) · R_int 113.5 → 501.8 · R_w 70.7 → 353.4 Ω·cm² (B-NCA 1 → 100 cyc) · U-NCA 는 완만 (R_int 1.5× · R_w 2.1×) → 흐름 밖: R_int ② · 사이클 열화 — 계산 결과를 이온망 (기하) 항과 계면 · 확산 항으로 나눠 실험 시계열과 같은 이름으로 견줌 · 근거 Table S2 줄 87–97 · S3 줄 99–106 | SI verbatim | NCA · 200 MPa 작동

(kim2023)
- [m] kim2023 | 결과 전 대조 항목 (조건 R7): 433 MPa 제조 직후 양극 단면 NCA 균열 없음 (Fig S15) — kang2025 Fig S9 (400 MPa) 와 같은 랩 두 번째 관찰 · 근거 §5 줄 233 | stated | NCA ~10 µm
- [m] kim2023 | 관측량 (조건 R4 · 단계 6): 150 cyc 뒤 250 MPa 재가압 → 방전용량 25.2 → 38.3 mAh/g 만 회복 = 재가압으로 돌아오는 몫 (가역 접촉) 과 남는 몫 (비가역 손상) 을 가르는 시험 꼴 · 근거 §5 줄 231–232 · §7 줄 275 | 그림 / 근사 (줄 365) | 사이클 뒤 · 제조 탈압 아님
- [m] kim2023 | 측정법: in-situ 압력 (로드셀 분해능 0.01 MPa) 으로 음극 · 양극 부피 변화 위상 분리 · 3-전극 (lithiated Ag) 으로 음극 · 양극 임피던스 분리 → 흐름 밖: R_int ② 실험 대조 설계 (원장 항목을 양극 · 음극 따로 견줌) · 근거 §6 줄 240–243 · §3 줄 122–125 | stated | —
- [m] kim2023 | 운전압 의존: 작동 100 MPa → 300 cyc 안정 vs 250 MPa (Fig S17) — 낮은 운전압이 음극 strain 전달을 줄여 덜 깨짐 → 흐름 밖: 운전압 설계 (우리 모델에 운전 적층압 축 없음) · 근거 §5 줄 235 · §10 줄 358–359 | 그림 | 메커니즘 = 음극 strain (가압 압밀 아님)

## 카드 문제

34 건 (고치지 않음). "카드 밖 근거" = 프로젝트 원장 · CLAUDE.md 기준으로 표시한 것.

공통 (여러 카드)
- intergranular 줄 45 "우리 압밀/전달 앵커 (Minnmann 10/14 %, ...)" — 출처가 철회된 Minnmann 순수 SE 10 % 를 압밀 앵커로 적음 (프로젝트 원장 CL-94). 다른 Minnmann 표기 (bucci2018 줄 269 · dem_mechanical 줄 59 · 264 · 279 · 312 · interfacial 줄 25 · 120 · 382 · 385 · kang2025 줄 55 · 314 · kim2023 줄 71 · 344) 는 14 % (복합) · 380 MPa · 측정압 40 MPa · σ 1.6 · 이름만이라 철회된 순수 SE 서술 자체는 아님 (참고).
- "Cronau 단결정 3.0" 라벨: dem_mechanical 줄 339 ("σ_grain = 3.0 mS/cm (Cronau 2022 단결정)") · interfacial 줄 120 ("Cronau 단결정 3.0") — 프로젝트 원장 CL-91 · SELF-51 (3.0 = 펠릿값 · '단결정' 라벨 · Cronau 2022 출처 철회) 과 다름 (카드 밖 근거).
- 문헌 E_LPSCl 22.1 GPa 와 '우리 real-bulk 24' 를 '일치' 로 적음 (두 값이 다름): kang2025 줄 30 · 61 · 247 · 305 · kim2023 줄 77 · 267 · 297.
- 우리 피복 값이 카드마다 다름: bucci2018 줄 279 · 333 "우리 Stage-E (Tabor) real_14 AM_P/AM_S 49.6/48.2 % vs Hertz 18 % (CLAUDE.md DEM↔MPM scaffold cross-validation)" ↔ dem_mechanical 줄 336 "Hertz/Tabor coverage (real_14 16/52 %)" — CLAUDE.md 기준 49.6/48.2 는 MPM scaffold 의 Tabor 피복 (DEM Physics = 48.3/51.8) · 16/49 는 기하 대조 · 그 '교차검증' 지위는 CLAUDE.md 에서 철회 (같은 기하 공유 · CDX-16) (카드 밖 근거).
- Bucci 임계 귀속: dem_mechanical 줄 10 · 283 · 305 는 '7.5 % · G_c 4 J/m²' 를 Bucci 2017 (FEM-CZM) 로 적음 ↔ bucci2018 카드는 7.5 % 를 Bucci 2018 (PRM · 1D 해석) 대표값으로 적고 G_c 4 J/m² 는 그 카드에 없음 — 어느 논문 값인지 카드끼리 다름.

bucci2018
- 줄 57 · 184 "셀 시간 2t_P → 3t_P (+150 % 의 t_P 기여)" — 2t_P → 3t_P 는 ×1.5 (셀 시간 +50 %) 라 '+150 %' 와 맞지 않음 [내 산술].
- 줄 225 결론 요약 "nanostructured AM (<~100 nm 계열)" ↔ 줄 45 · 160 · 212 · 240 "임계반경 ~50–500 nm" — 크기 표기 두 값.
- 줄 65 · 241 von Mises σ "~−4 → −2 GPa (스칼라 음부호 표기)" — 등가응력은 음수가 아님 (카드가 스스로 표기 방식이라 적음 · 원 그림 확인 필요).

dem_mechanical
- 줄 263 "우리 real_14 AM-shielding (SE overlap 1.75 % ...)" — CLAUDE.md E_SE 보정 절 기준 1.75 % 는 input_2mAh_real_9 의 값 (카드 밖 근거).
- 줄 86 표 칸 "~400 MPa? → 아니, 6–16 MPa": 논문의 'isostatic' 평균 응력 문장 (400 / 380 / 700 MPa) 을 카드가 일축 재서술로 재해석 — 원문 확인 필요.
- 줄 88 · 223 Fig 5a 컬러바 0–10 MPa ↔ 같은 그림 응력 6–16 MPa — 범위 불일치 (확인 필요).
- 줄 78 "입경 2 µm ~390 → 6 µm ~250 MPa" ↔ 같은 행 조건 "particle radius 2–6 µm" — 지름 / 반경 혼용.
- 같은 원문 인용 "nearly twice the order of magnitude" 에 카드가 끼운 말이 줄 92 [lower stress] ↔ 줄 203 [pressure] 로 다름.
- 줄 117 · 170 · 242 · 317: DiffuDict 확산 τ = √(η/D_eff) 를 '기하 tortuosity' 로 부름 — 프로젝트 τ 명명 규약 (10-03) 상 확산 (flux) τ (√ 형) 이고 기하 τ (최단 경로) 와 다른 양 (카드 밖 근거).

gandla2026
- 카드 §10 · §12 가 스스로 기록한 원문 · 다른 카드 충돌 (보고만): '~20 %' 분모 셋 (줄 110 · 399) · 실용 하중 문턱 셋 (줄 404) · 중성자 영상 하중 33 vs 30 mg/cm² (줄 405) · [127] / [135] 권 7 vs 6 (줄 407) · 그림 11 P3 이름표 (줄 403) · 인용 번호 [20] · [88] · [123] (줄 406) · 그림 4g mT 단위 의심 (줄 409).
- 줄 437: li2026 카드와 Shi 2020 [60] 2 차 인용 값이 다름 (접촉 손실 부피 2.87 → 10.4 vol % · 129 → 102 mAh/g ↔ 공극 < 3 → 9.5 % · ~100 → < 20 mAh/g) — 카드가 스스로 적음.
- 80:20 최빈 배위수 "≈5.5" (줄 32 · 336 · 379) ↔ "≈5.3–5.5" (줄 121) — 작은 차.

interfacial
- 줄 87 · 120 · 249 · 297 "r_i (composite, ε_i = 1.0) 12 800 Ω·cm" ↔ 줄 89–90 · 206 ε_i 1.0 의 r_i,bulk 170 + r_i,gb 630 = 800 Ω·cm — 같은 ε_i 에서 두 값 (16 배 차) · 줄 120 의 σ ≈ 0.078 mS/cm 환산도 12 800 에 기댐.
- 줄 94 · 205 · 251 "ε_i 0.26" ↔ 줄 67 · 203 스윕 범위 "ε_i 0.49–1.0" — 범위 밖 값.
- 줄 101 · 186 · 218 · 262 "τ_eff² 1.46 ≈ 이상 Bruggeman 1.41 (α 0.5)" — 그 셀 ε_i 0.58 이면 0.58^(−0.5) ≈ 1.31 [내 산술] · 1.41 은 ε_i 0.5 에 해당 — 원문 확인 필요.
- 줄 45 · 173 · 299 τ_eff² (= φσ₀/σ_eff · 제곱 양) 를 '우리 τ_Laplace,eff 와 정의 동일' 로 적음 — 프로젝트 τ 명명 규약상 그 양은 tau2 (수송 tortuosity) 이고 τ_Lap,eff 는 그 √ (카드 밖 근거).
- 줄 385 "separator 433" — 이 카드 다른 곳에 근거 없음 (kim2023 카드의 제조압 433 MPa 와 같은 수 — 다른 논문 값이 섞인 것으로 보임).

intergranular
- 균열이 설명하는 부피 증가 몫이 세 값: "best-case ~70 % (분할가능)" · "평균 92.0 % (Fig 3k · 15 입자)" · 8 입자 표 30–72 % (모두 72 % 이하) — 같은 양인지 정의가 다른지 카드에서 갈리지 않음 (줄 38 · 88 · 99–108 · 189).
- 줄 165 · 260 "모델이 재현 못 하는 13–25 % 부피팽창" ↔ 측정 표 +13.3 – +28.3 % (줄 99–106) — 범위 표기 다름.
- 줄 11–15 · 216 · 284 '사이클 (중) 입계 균열' ↔ 시험 = C/50 4.5 V 1 회 충전 (줄 61 "사이클링 반복 아님") — 용어 불일치.

kang2025
- 본문 "R_ele B-NCA 33.9 Ω·cm² lower" (줄 74 · 193) ↔ Table S1 89.9 − 20.0 = 69.9 (카드가 줄 84–85 에 스스로 적음).
- 부피 로딩 단위: 줄 64 "mg cm⁻³" ↔ 줄 214 "g cm⁻³" (같은 ~1.87 / ~2.02).
- 표지 충돌: 줄 64 (Fig S2 값 'stated') · 줄 70–71 (Fig 3d/3e 컬러바 'stated') ↔ 줄 329 (같은 값들 = '그림에서 읽은 값').
- 줄 199 Fig 2f "R_w 급등 (70 → 210+)" ↔ Table S2 100 사이클 353.4 (75 사이클 212.0) — 끝값 다름.

kim2023
- 줄 76 "E_NCA n/a (본문 미명시)" ↔ 줄 77 "NCA 175 / LPSCl 22.1 GPa · stated (본문 §2.5)" — 같은 표 안 충돌.
- 줄 77 · 267 · 296 · 339 "이 논문이 175/22.1 의 원조 · 최초 출처" ↔ 같은 줄 "FEM 입력 (ref [39])" · kang2025 카드 줄 60 은 E_NCA 175 의 출처를 ref [42] Koerver 2018 로 적음 — '원조' 주장과 인용 출처가 맞지 않음.
- in-situ ΔP Li-In "±3.8 MPa" (줄 79 · 199 · 323) ↔ 본문 "≈4.0" (줄 80 · 365) — 두 값.
- 줄 62 "PEEK 몰드 0.5 mm dia" ↔ SUS rod 10 mm · In 10 mm dia (줄 61–62) — 몰드 지름 표기 의심.
- slug 'kim2023' ↔ 제 1 저자 Junhee Kang (카드가 스스로 정정 · 줄 10–13 · 360–361) — 인용 시 'Kang et al. 2023'.

### 인용 금지 표지 위치

이 배치 7 장에 없음 (전수 검색 0 건).

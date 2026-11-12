# batch_21 정독 근거 (카드 7 장 · 전문 읽음 · 2026-11-10)

읽은 카드: `zhou2026_gyroid_structural_electrolyte_stiffness_ionic_tradeoff` (340 줄) · `asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing` (862) · `bak2024_binder_distribution_multilayer` (472) · `bzox_dry_zro2x_nmc_shell_coating_sulfide_assb` (3 줄 안내문) · `cho2024_conflicting_roles_conductive_additive` (551) · `duquesnoy2023_ml_multiobjective_manufacturing_optimization` (365) · `frankenberg2024_dem_high_intensity_mixer_assb` (285). 끝까지 못 읽은 카드 없음 (zhou 3 번 · asylbekov 6 번 · bak 3 번 · cho 4 번 · duquesnoy 3 번 · frankenberg 5 번에 나눠 마지막 줄까지 읽음).

배치의 성격: 연속체 FEM 1 (자이로이드 구조 전해질 · 액체 + 고분자) · 혼합 DEM 2 (Kwade 계열 — CB 분쇄 PBE / ASSB heteroaggregate force-scaling) · 액체 LIB 실험 + 복셀 전자 전도 1 (바인더 z 분포) · ML 역설계 + 압연 DEM 1 (액체 LIB) · **NCM811 + LPSCl 실전극 실험 1 (cho2024 — 이 배치에서 우리 소재와 같은 유일한 카드)** · 안내문 1. **MPM 카드 · 순수 SE 압력별 기공 곡선 · 되돌아옴 실측 · SE 항복 / 경도 · 큰 변형 접촉 법칙 대안을 준 카드는 없다.** 가압 · 탈압 계획에 쓸 것은 복합 양극 433 MPa 기공 한 점 (cho2024) · 복셀 σ 해법 검증 기준 (zhou2026) · DEM 한계 문장 (asylbekov · frankenberg · duquesnoy) · 보정 · 검증 분리 형식 (frankenberg · asylbekov) 이다.

적는 법: 위치의 `L숫자` = 카드 줄 번호 · 표지는 카드에 적힌 그대로 (`stated` · `digitized` · `digitize TREND` · `[인쇄]` · `[우리 산술]` · `[추정]` · `[제안]`) · 없으면 "표지 없음". "카드 풀이" = 논문 문장이 아니라 카드 작성자의 서술. "내 검산 / 내 대조" = 카드에 적힌 숫자끼리만 대조한 것 (새 계산 아님 · 카드 문제 절에만 씀). 큰따옴표 안 영어 = 카드가 옮겨 둔 원문 · 한국어 따옴표 = 카드의 옮김. **"인용 금지" 표지가 붙은 값 (숫자로 옮기지 않음 · 위치만)**: asylbekov2023 L801 (σ_crit 을 CB 파괴 강도로) · L127–131 (Γ_SJKR 을 재료 표면에너지로) · L181 (§3.8 digitized 표 '추세 전용, 정밀 인용 금지') · L484 ("분쇄가 유동거동을 바꾼다" 를 데이터로). 랩 표준 (순수 SE 기공률 10–13 % · LPSCl 진밀도 1.64 g/cm³) 은 고정.

---

## a. 순수 SE (LPSCl · 황화물) 압력별 기공 곡선 · 진밀도

이 배치에 없음 (순수 SE 의 압력별 기공 곡선을 가진 카드 없음). 관련만:
- [a] zhou2026_gyroid_structural_electrolyte_stiffness_ionic_tradeoff | (다른 카드 값의 포인터) 냉간압착 LPSCl 펠릿 공극 13 ± 2 % · E 4.7 GPa = 조밀 결정 22.1 GPa 의 ≈21 % — `song2025_porous_argyrodite_modulus_fracture_toughness` 에서 가져옴 | §7-5 L244 | [우리 산술 · 추정] | 이 카드의 측정 아님 · 압력 · 진밀도 · 질량 기준 · 누른 채 여부 이 카드에 없음 · 랩 표준과 다른 문헌 값 (범위 일부 겹침)
- [a] cho2024_conflicting_roles_conductive_additive | wt% → vol% 환산용 LPSCl 밀도 ~1.64 g/cm³ (NCM ~4.77) | §12 L497 | 표지 없음 (논문 값인지 카드 가정인지 표시 없음) | 랩 표준 진밀도 1.64 와 같은 값 · 이 카드에 기공 곡선 없음
- [a] cho2024_conflicting_roles_conductive_additive | LPSCl σ_ion 4.8 mS/cm (RT) — 기공이 아닌 전도도 | §3 L109 · Fig S1 | stated | 같은 랩 Kim 2025 는 1.6 (L138–140) · 카드: 절대 직접대조 금지, 범위로만

## b. 압력을 뺄 때 되돌아오는 양 · 잰 방법

이 배치에 없음 (되돌아옴을 잰 카드 없음). 관련만:
- [b] zhou2026_gyroid_structural_electrolyte_stiffness_ionic_tradeoff | 압밀이 끝난 MPM 상 격자에 선형 탄성 주기 균질화 (단위 변형 6 경우) 를 걸면 이방 탄성 텐서 (E_x · E_z · ν) 를 낼 수 있다는 카드 제안 — 접촉이 완전 결합으로 들어가 실제보다 뻣뻣하고, 언로딩 · 스프링백은 접촉이 열려 비선형 | §7-5 L243 | [제안] · [추정] | 값 없음 · 방법 제안만
- [b] frankenberg2024_dem_high_intensity_mixer_assb | 압축 보정 시험은 하중 쪽만 (1 g · 상부 stamp 4.17 mm/s 로 6 mm 까지 · force–displacement) — 되돌림 구간 기록 없음 | §4.6 L116 · Fig 5b | stated | heteroaggregate 분체 · 되돌아옴 값 없음
- [b] duquesnoy2023_ml_multiobjective_manufacturing_optimization | 되돌아옴을 다루지 않음 — Table 4 의 두께 68 ± 4 → 48 ± 4 µm (압연 30 %) 만 있음 | §3.5 L91 | stated | 액체 LIB · 두께 감소율 축 · 카드에 되돌아옴 해석 없음

## c. 항복 · 경도 · 크리프 값과 정의 · 일축 항복 환산

항복 · 경도 · 크리프를 잰 카드 없음. 관련 정의 · 값만:
- [c] asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing | σ₅₀ = 50 % 확률로 파괴를 일으키는 비(比)파괴응력 (eq 11 · Tavares 계열) · x_p = 그 아래에서 소성변형이 지배해 더는 안 깨지는 크기 0.199 µm | §4.5 L327–333 · §3.3 L102 | stated | CB 응집체 **파괴** 강도 (항복 아님) · 적합값 σ_crit(x) = '인용 금지' 표지 (L801 · 숫자 안 옮김 · Fig 7 right) · 미보고 λ 와 축퇴 (§A-4) · eq 16 은 σ_crit 를 hard threshold 로 써 "50 % 확률" 이 실제로 구현되지 않음 (§10 L831) · 일축 항복 환산 없음
- [c] asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing | NCM622 E 230 GPa = 실물 재료값 · DEM 에 넣은 E 는 논문이 밝히지 않음 (Table 1 에 E 없음 → 접촉 강성 축 재현 불가) | §3.4 L123–124 | stated | AM 탄성 · 항복 아님
- [c] frankenberg2024_dem_high_intensity_mixer_assb | 보정 E 25 MPa · ν 0.3 = heteroaggregate 분체 (다공) 의 압축 거동 모듈러스 · 재료 E 아님 (저자 명시) · 항복 캡 (p_y) 없음 | Table 3 · §3 L44 · §4.2 L77 · §10 L278 | stated | 분체 강성 · 일축 항복 환산 없음
- [c] zhou2026_gyroid_structural_electrolyte_stiffness_ionic_tradeoff | 고체 E_s 3 GPa · ν_s 0.3 = 인쇄 PLA 대표값 ("dimensional reference") · 선형 탄성뿐 | §3-1 L69 · p.5 | [인쇄] | 고분자 · 항복 · 경도 없음
- [c] cho2024_conflicting_roles_conductive_additive | E_SE · σ_y · ν = n/a (역학 미모델) | §3 L133 | — | —
- [c] bak2024_binder_distribution_multilayer · duquesnoy2023_ml_multiobjective_manufacturing_optimization | 항복 · 경도 · 크리프 값 없음 (bak = SAICAS 접착 강도 N/m · M 층 100 % 정규화뿐 · §2.4 L128–131 · §4.1) | — | — | —

## d. 단단한 + 무른 입자 혼합 압축의 하중 몫 · 재밍

이 배치에 없음 (하중 몫 · 재밍을 잰 카드 없음). 관련만:
- [d] asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing | 가정 — 크고 단단한 AM 이 날 · 내벽에서 눌리며 그 사이에 낀 CB 응집체의 분쇄 매체가 된다: "The much larger and tougher active material particles are compressed at the blades and the inner wall of the mixer and serve as a grinding media for the CB agglomerates which are caught in between." | §4.7 L374–377 | 원문 따옴표 (카드 옮김) | 혼합 · 저응력 · CB 가 DEM 에 없어 하중 몫 계산 아님
- [d] frankenberg2024_dem_high_intensity_mixer_assb | coarse-grain 입자를 너무 크게 (> 0.5 mm) 하면 gap (1.532–1.895 mm) 에 jam → 비현실적 고응력 · 0.5 mm = gap 의 ~1/3 절충 | §4.4 L103 · §10 L279 | stated (저자) | 입자–틈 기하 재밍 = 수치 인공물 · 단단 / 무른 혼합의 하중 몫 아님
- [d] cho2024_conflicting_roles_conductive_additive | AM 88 wt% 전극이 72 wt% 보다 기공이 큼 (0.18–0.19 ↔ 0.14–0.15) · 카드 해석 "SE 적어 충전율↓" | §3 L121–122 · Table S2 | stated (해석 = 카드 풀이) | 하중 몫 측정 아님 · 433 MPa 한 점

## e. 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안 · 맞춘 값 수

대안 (multi-contact · MDR · EEPA · Thornton–Ning · Storåkers) 을 쓴 카드 없음. 각 카드의 접촉 표현과 맞춘 값:
- [e] asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing | Hertz 법선 + Mindlin–Deresiewicz 접선 + SJKR 점착 · 항복 캡 · 소성 접촉 · 입자 파쇄 없음 · CG 100 에서도 자기닮음 때문에 마찰 모델 수정 불필요 (논문 주장) | §4.6 L351–355 · §3.5 L140 · §4.8 L382–383 | stated / 카드 풀이 | 맞춘 값 = μ_static · μ_dynamic · e · Γ_SJKR 네 종을 확대 입자 위에서 보정 (§4.8 L384 · Γ 값은 인용 금지 표지 L130) · Table 1 벽 · 입자 두 열 중 무엇을 맞췄는지 카드에 없음 · 보정에 CNN 사용 · 방법은 "향후 논문" (§6 L499–500)
- [e] frankenberg2024_dem_high_intensity_mixer_assb | Hertz–Mindlin + JKR · 항복 캡 없음 · 비구형성은 rolling friction (linear spring · μ_r 0.2) 으로 대리 · 점착 분말이라 JKR 필수 (저자 강조) | §4.2 L76–78 · §4.5 L107 | stated | 맞춘 값 7 = DAOR 로 μ_r · μ_s · μ_d · Γ_pp (pyDOE 16 시뮬 민감도) + 압축 시험으로 E · ν · e_pp · 그 밖에 충진율 맞춤 ρ_b 750 (실측 701.83) · 보정점 10 min⁻¹ · 검증 5/15/60 min⁻¹ + SAOR 54.21 ↔ 55.58° (§4.6 L114–116)
- [e] duquesnoy2023_ml_multiobjective_manufacturing_optimization | 압연 DEM 접촉 법칙 카드에 없음 ("rigid-ish 강체구 압축" · "CONTACT도 명시 약함") | §4.5 L178 · §7.1 L239 | 카드 풀이 | 맞춘 값 개수 카드에 없음
- [e] zhou2026 · bak2024 · cho2024 | 점접촉 법칙 없음 (연속체 FEM · 복셀 전도 · 실험) | — | — | —

## f. MPM 의 접촉 · 다물체 · 강체 결합 · 해상도 규칙 · 수치 오차 추정

이 배치에 MPM 카드 없음. 해상도 · 수치 오차 관련만 (모두 MPM 아님):
- [f] zhou2026_gyroid_structural_electrolyte_stiffness_ionic_tradeoff | (복셀 FV 수송) 조화평균 면 복셀 FV 는 매끈한 기하에서 1 차 수렴 (오차 ∝ 1/N) · 덜 풀린 쪽이 늘 낮게 나옴 · 원문 대비 오차 ≈ −0.28/(d_h/dx) (시트 28 점 · d_h/dx 1.6–18.8 · 최대 잔차 1.3 %p) · d_h = V_liq/S · N 64 · 128 + 1 차 Richardson 외삽 | §7-3 L221–224 · §6 L178 | [우리 산술] | 카드의 독립 재현 (논문 값 아님) · 입자 목이 없어 '가짜 상호연결' 인공물은 이 규칙 밖 (L224) · 원문 FEM 은 메시 · 요소 · 수렴 정보 없음 (§3-1 L71)
- [f] bak2024_binder_distribution_multilayer | (GeoDict 복셀) CBD voxel 1 nm · 입경 20 nm / 전극 voxel 100 nm · NCM 입경 10 µm | §2.6 L160–164 (SI Table S1 · S2) | 표지 없음 | 수치 오차 추정 카드에 없음
- [f] asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing | (DEM · PBE) CG 100 = Feng et al. [55] 에 따르면 방법의 상한 부근 · PBE RK4 Δt ≤ 0.1 s 면 시간간격 무관 · 크기 클래스 수 N 은 "결과 품질이 클래스 수에 크게 의존" 하는데 값 미보고 · Kumar 보정으로 질량보존이 격자 무관 | §3.5 L137–138 · L146–147 · §4.3 L288–296 | stated | DEM 응력 절대값은 독립 검증 없음 (§4.8 L395)
- [f] frankenberg2024_dem_high_intensity_mixer_assb | (DEM) Δt_sim = 0.2·πR*√(ρ/G*)/(0.8766 + 0.1631ν) ∝ R* · force-scaling 검증 = 같은 크기 두 입자 충돌 (ρ 1,250 kg/m³ · v 0.1 m/s · 거리 10 mm · friction 0.001) 의 force–time 곡선이 f² 를 따르는지 확인 | §3 L60 · §4.3 L97 | stated | —
- [f] duquesnoy2023_ml_multiobjective_manufacturing_optimization | 복셀 물성 추출 (GeoDict · TauFactor) 의 격자 수렴 미시험 (2020 → 2023 "바뀌지 않은 것") | §선행 논문 L363 | 표지 없음 (카드 비교표) | —

## g. 2D 결과를 3D 로 옮길 때의 경고 · 증거

이 배치에 없음 (2D → 3D 경고 · 증거를 준 카드 없음 — zhou2026 은 3D 단위셀이고 2D 결과가 없다).

## h. DEM 에서 FE · MPM 으로 넘긴 선례 · 넘긴 시점

- [h] duquesnoy2023_ml_multiobjective_manufacturing_optimization | DEM 압연이 끝난 구조 → MATLAB 메싱 → GeoDict (σ_e · 복셀 연속체) · TauFactor (τ · Laplace FV) · Python (active surface · density · porosity) — 넘긴 시점 = 압연 DEM 끝 (과정 결합 없음) | §4.6 L183–188 · §4.1 L120 | stated | 넘긴 곳 = 복셀 연속체 수송 (역학 FE · MPM 아님) · 액체 LIB
- [h] asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing | DEM → PBE 단방향 · 1 회 — DEM 은 최적화 루프 밖에서 한 번만 돌아 응력 분포 σ̄ 와 비빈도 ṅ(σ̄) 두 통계만 넘김 · CB 분쇄가 분체 거동을 바꾸는 되먹임 없음 (저자도 결론에서 문제로 지적) | §4.0 L231–233 · §4.1 L237–253 | stated | FE · MPM 아님 · 크기 공간 0D
- [h] bak2024_binder_distribution_multilayer | (DEM 아님) GeoDict GrainGeo 로 설계한 구형 NCM 골격 + stochastic CBD → ConductoDict | §2.6 L151–157 | 표지 없음 | 넘김 선례 아님 (설계 구조 입력)

## i. 복합 양극 (AM + SE) 의 압력별 기공

- [i] cho2024_conflicting_roles_conductive_additive | NCM811 + LPSCl (+ VGCF 2 wt%) · 433 MPa 적층: 기공 0.14 (f_AM 72 wt% · CA 없음) · 0.15 (CA 있음) · 0.18 (88 wt% · 없음) · 0.19 (있음) | Table S2 · §3 L121–122 · §6.4 L329–332 | stated | 압력 한 점 · 측정법 · 누른 채인지 (작동 stack 250 MPa) 카드에 없음 · 카드 환산 72 wt% ≈ φ_SE 0.45 · 88 wt% ≈ 0.15–0.20 (§12 L497–498 · 카드 어림)
- [i] duquesnoy2023_ml_multiobjective_manufacturing_optimization | (AM + SE 아님 · LIB NMC111 + CBD) 실험 기공 60 ± 3 % (비압연) → 29 ± 0.7 % (압연 30 %) · Liu 2023 3×3 예: AM 90 % · CD 0 / 10 / 20 % → 53.03 / 49.835 / 42.145 % | Table 4 L94 · SI Table S3 L105–107 | stated | 압력 아닌 두께 감소율 축 · 액체 LIB
- [i] bak2024_binder_distribution_multilayer | (AM + SE 아님 · LIB NCM622 + 탄소 + PVDF) 비캘린더 모델 전극 기공 34–37 vol% · Ref 39 vol% (표면 쪽 ↑) · 깊이 표준편차 3.1 | SI Fig S6 · §7(d) L414 | 표지 없음 | 압력 축 없음 · 캘린더 (3.0 g/cm³) 뒤 기공은 카드에 없음
- [i] frankenberg2024_dem_high_intensity_mixer_assb | 셀을 380 MPa 로 조립했으나 기공 미산출 | §3 L58 · L62 | stated | —

## j. 카드가 스스로 적은 한계 가운데 가압 · 탈압 계산과 닿는 것

- [j] zhou2026_gyroid_structural_electrolyte_stiffness_ionic_tradeoff | 소성 · 압밀 · 접촉 · 파괴 없음 · 작은 변형 선형 탄성 · 역학 ↔ 수송 비결합 (p.3) · 실험 검증 = 향후 (방향별 기계 시험 + 차단 전극 임피던스 · p.8) | §0 L35–36 · §10 L299 | [인쇄] / [우리 산술] | 연속체 · 설계 기하
- [j] asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing | DEM 입자는 영원한 강체 구 (항복 캡 · 소성 접촉 · 파쇄 없음) · 응력 체제가 300 MPa 보다 3–6 자릿수 아래라 σ_crit 곡선을 압밀에 그대로 넣으면 "모든 CB 가 첫 접촉에서 하한까지 분쇄" (카드) · 재응집 모델 없음 — 바인더를 넣으면 필수 (저자 결론) · 0D 공간 무시 | §4.6 L355 · §10 L792–795 · L818–820 · §A-5 L610–615 | stated / 카드 풀이 | 혼합 공정
- [j] bak2024_binder_distribution_multilayer | 캘린더링이 이차입자 활물질을 파괴해 접착 강도를 왜곡 → 분포 측정은 비캘린더 상태 (Fig S5) · 디지털 트윈 = 전자 전도만 · 입자 스케일 압축 역학 예측 없음 (구조는 측정 · 설계로 입력) · 저자: 중로딩 3.5 mAh/cm² 라 분포 차이가 미묘 | §2.4 L135–136 · §2.6 L158–159 · §7(e) L421–423 · §4.6 L279–280 | 표지 없음 | 액체 LIB
- [j] cho2024_conflicting_roles_conductive_additive | 압밀 곡선 · Heckel · coordination · coverage · E_SE n/a · τ 산출법 미명시 · PSD 미보고 | §12 L500–505 · §3 L133–136 | 카드 풀이 | 실험
- [j] duquesnoy2023_ml_multiobjective_manufacturing_optimization | 고밀도 극단 (CD 36.36 %) 의 AM 입자 파쇄 위험 (CEI/TM 용해 · 비활성화) 은 현 모델 미반영 · 모델 ↔ 실험 차이 원인 (그들 명시) = 구형 입자 + clustered CBD 단순화 · σ_e 실험 미측정 | §3.4 L84 · §3.5 L96 · §10 L339 | stated | 액체 LIB
- [j] frankenberg2024_dem_high_intensity_mixer_assb | 항복 캡 없음 · 입자 파쇄 미모델 (고속 분쇄는 정성 언급) · 응집체 형성 자체를 시뮬하지 않음 (응력만 추출) · 압축 보정 곡선 초반 편차 (coarse-grain 입자망 ε_total 0.75) — 고압축에서만 일치 · 기공 미산출 | §4.2 L77 · §4.5 L110 · §B-3 L214 · §4.6 L116 · §3 L62 | stated / 카드 풀이 | 혼합 공정 · 분체

## k. DEM 의 한계 (인용할 서지와 함께)

이 배치에 믿을 수 있는 겹침 · 상대밀도 상한이나 접촉 독립 가정이 깨지는 밀도를 수치로 준 카드는 없다. DEM 을 쓴 세 편이 직접 적은 한계:
- [k] asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing (Asylbekov et al., Energy Technology 11, 2200867, 2023) | 나노 도전제는 DEM 에서 풀 수 없다 — "Due to the small size of the CB, it is not possible to completely resolve the particles in the DEM, even with low mass fractions." → CB 를 DEM 에서 빼고 PBE 로 | §A-2 L554 · §9 L760–761 | 원문 따옴표 | 해상도 · 비용 한계 (소성 이야기 아님)
- [k] asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing (Asylbekov et al., Energy Technology 11, 2200867, 2023) | 보정값은 재료값이 아니다 — μ · e · Γ_SJKR 은 "calibrated directly on scaled-up particles, so that they are already adapted to the coarse grain factor" | §3.4 L128–129 | 원문 따옴표 | 값은 인용 금지 표지 (L130) — 숫자 안 옮김
- [k] asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing (Asylbekov et al., Energy Technology 11, 2200867, 2023) | CG 100 은 Feng et al. [55] 에 따르면 방법의 상한 부근 · 입자 수 정규화는 CG 오차를 '부분적으로 (partially)' 만 보상 · 입자가 작아질수록 시간간격이 작아져 비용 폭증 | §3.5 L138 · §4.8 L386–388 · §4.6 L357 | stated (카드의 한국어 옮김) | 카드: 응력 절대값은 어떤 독립 검증도 없음 (§4.8 L395)
- [k] asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing (Asylbekov et al., Energy Technology 11, 2200867, 2023) | DEM 입자 = 영원한 강체 구 · 형상 · 소성 · 파쇄 없음 | §4.6 L355 · §4.7 L364–367 | 카드 풀이 | 논문이 스스로 적은 문장은 카드에 없음 — 인용 시 카드의 분류로만
- [k] frankenberg2024_dem_high_intensity_mixer_assb (Frankenberg et al., Powder Technology 435, 119403, 2024) | 비구형 형상은 계산 비용 때문에 구로 처리 (Rocky 비구형 입자는 훨씬 느림 — 저자 명시) · 비구형성은 rolling friction 으로 대리 | §4.1 L72 · §4.5 L107 | stated | 원문 따옴표 없음 (카드의 한국어 풀이)
- [k] frankenberg2024_dem_high_intensity_mixer_assb (Frankenberg et al., Powder Technology 435, 119403, 2024) | Δt ∝ R* (eq 1) — 0.5 µm 미만 입자는 CPU · GPU 모두 비현실적 (SI) · 입자를 너무 키우면 gap jam → 0.5 mm 절충 · force-scaling 이 응력은 보존해도 국소 충돌 통계 · gap jam 은 입자 크기에 의존 | §4.4 L102–103 · §10 L279 | stated | —
- [k] frankenberg2024_dem_high_intensity_mixer_assb (Frankenberg et al., Powder Technology 435, 119403, 2024) | 보정 E 25 MPa 는 재료 E 가 아니라 분체 (다공) 의 압축 거동 E (저자 명시) — 보정값 ≠ 물성 | §3 L44 · §10 L278 | stated | —
- [k] frankenberg2024_dem_high_intensity_mixer_assb (Frankenberg et al., Powder Technology 435, 119403, 2024) | coarse-grain 압축 곡선 초반 편차 — 입자망 (ε_total 0.75) 이 처음엔 거의 저항이 없다가 점착을 넘으면 급증 · 고압축에서만 sim = exp | §4.6 L116 · Fig 5b | 카드 풀이 ("coarse-grain 탓" 이 논문 문장인지 표시 없음) | —
- [k] duquesnoy2023_ml_multiobjective_manufacturing_optimization (Duquesnoy et al., Energy Storage Materials 56, 50–61, 2023) | 모델 ↔ 실험 차이 원인 (그들 명시) = 구형 입자 + clustered CBD 단순화 · 비구형 입자는 향후 과제 (ref 79) · NMC111 은 구형 coarse-grained 입자로 충분 (그들 선행연구) | §3.5 L96 · §4.5 L180–181 · §4.1 L121 | stated | 원문 따옴표 없음
- [k] duquesnoy2023_ml_multiobjective_manufacturing_optimization (Duquesnoy et al., Energy Storage Materials 56, 50–61, 2023) | 고밀도 극단에서 AM 입자 파쇄 위험 · 현 모델 미반영 | §3.4 L84 | 표지 없음 (Fig 6 설명 표 — 논문 문장인지 카드 풀이인지 표시 없음) | —
- [k] zhou2026_gyroid_structural_electrolyte_stiffness_ionic_tradeoff (Zhou et al., J. Appl. Phys. 140, 154901, 2026) | 논문: 말 없음 (DEM 을 쓰지 않음) · 카드 풀이: 압밀로 판처럼 눌린 SE 영역의 기하 몫 (z tau2 증가) 을 DEM 구 (강체) 는 못 그리고 MPM-STEP3 는 그릴 수 있다 | §7-4 L239 | [추정] (카드) | Zhou 2026 의 주장으로 인용하지 말 것
- [k] bak2024_binder_distribution_multilayer (Bak et al., Chemical Engineering Journal 483, 148913, 2024) · cho2024_conflicting_roles_conductive_additive (Cho et al., Electrochimica Acta 481, 143990, 2024) | 말 없음 (DEM 을 쓰지 않음) | — | — | —

## l. 소성변형이 왜 어려운가 · 택한 우회와 그 값 (인용할 서지와 함께)

이 배치에서 입자 계산에 소성을 넣기 어려운 이유를 직접 설명한 논문은 없다. 우회 · 맞춘 값 · 검증 · 비용만:
- [l] asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing (Asylbekov et al., Energy Technology 11, 2200867, 2023) | 우회 = 나노 CB 를 DEM 에서 빼고 크기 공간 PBE 로 (DEM 은 응력 · 빈도 통계만) + CG 오차를 확대 입자 보정 · 입자 수 정규화로 흡수 (카드: 우리 18× 연화와 같은 '보상' 쪽) · 맞춘 값 = DEM 네 종 (μ_s · μ_d · e · Γ — CNN 보정 · 방법 미공개) + PBE σ_crit (power-law 2 · σ₅₀ 4 개) + θ(z) 의 (q · ν) × 2 집단 + 자유 스칼라 λ (값 미보고) · 9.5 m/s 실험 PSD 하나에 맞춤 · 검증 = 6.25 m/s 전이 (Case III) 실패 → breakage function 재보정 (Case IV) 으로 회복 · 비용 = 입자 수 · Δt · 물리시간 미보고 · GPU V100 · PBE 는 ODE 수준 (카드) | §1 L42–45 · §4.1 · §4.5 L317–332 · §4.8 L390–392 · §4.11 · §A-4 L585–591 | stated / 카드 풀이 | 혼합 · 저응력 · 데이터 비공개 · 13 m/s 전이 서술은 카드 안에서 갈림 (카드 문제)
- [l] asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing (Asylbekov et al., Energy Technology 11, 2200867, 2023) | 아주 작은 입자에서는 투입 에너지가 전부 소성 · 탄성 변형으로 가서 파괴가 일어나지 않는다 (Tavares) → x_p 0.199 µm 아래 분쇄 없음 | §4.5 L331–333 | stated (카드의 한국어 옮김) | 파괴 하한의 근거이지 입자 계산에 소성을 넣는 어려움의 설명은 아님
- [l] frankenberg2024_dem_high_intensity_mixer_assb (Frankenberg et al., Powder Technology 435, 119403, 2024) | 소성 없음 — 카드 풀이: 혼합 응력이라 탄성-점착 접촉으로 충분 · mechanofusion 의 표면 융합 · 코팅 · 합체는 미모델 (응력 추출로 경향만 추론) · 응집체를 입자 하나로 coarse-grain · 우회 = force-scaling (F × f² · δ × f · τ × f · E* · G* 상수) + rolling friction · 맞춘 값 7 (μ_r 0.2 · μ_s = μ_d 0.44 · Γ_pp 0.0045 J/m² · E 25 MPa · ν 0.3 · e_pp 0.3) + ρ_b 조정 · 보정 = DAOR 10 min⁻¹ · 검증 = DAOR 5/15/60 + SAOR + 압축 곡선 (고압축에서만 일치) · 비용 = 36,670 입자 (3 g · 도메인 1/5) · 물리시간 1 s (주입 0.1 s) · 계산 시간 카드에 없음 | §4.2 L77 · §4.5 L107 · Table 3 L44–50 · §4.6 L112–116 · §3 L43 · §4.5 L109 | stated / 카드 풀이 | 할라이드 + LFP · 분체
- [l] duquesnoy2023_ml_multiobjective_manufacturing_optimization (Duquesnoy et al., Energy Storage Materials 56, 50–61, 2023) | 소성 설명 없음 · 우회 = 건조를 CBD 균일 수축 (부피 연산 · 소성 아님) · 압연 DEM 강체 구 (형상 소성 없음) · AM–CBD force-field 를 top-down 으로 맞춤 · 실험 파일럿 라인 · Liu 2023 실험으로 보정 (맞춘 값 개수 카드에 없음) · 검증 = 최적 전극 제작 (모델 density 2.45 · τ 1.47 · porosity ~24 % ↔ 실측 2.6 · 1.8 · 29 %) · 비용 = 슬러리 1 건 ~150 h · 압연 1 건 ~8 h · 174 조건 2 개월 · 8 노드 (384 GB · Xeon Gold 6148 20 core) · 총질량 0.1 µg (바닥 400–900 µm²) · 입자 수 카드에 없음 | §4.1 L121–128 · §4.5 L178 · §2 L27–28 · §3.6 · §3.5 L95 | stated / 카드 풀이 | 액체 LIB · 모델 기공 서술이 두 가지 (카드 문제)
- [l] zhou2026_gyroid_structural_electrolyte_stiffness_ionic_tradeoff (Zhou et al., J. Appl. Phys. 140, 154901, 2026) | 논문: 말 없음 (선형 탄성만) · 카드 풀이: 매끈한 시트 자이로이드는 공극 20 % 에서 강성 60 % (Ē 0.599) 를 지키는데 냉간압착 LPSCl 펠릿은 조밀 결정의 ≈21 % → 펠릿의 약함은 공극 부피가 아니라 입자 사이 목 (접촉) 에 있다 — 연화 (E_eff) 정당화와 같은 방향 | §7-5 L244 · §8-6 L281–283 | [우리 산술 · 추정] | 기하 · 재료 다름 · 방향만 (카드) · 논문 주장 아님
- [l] bak2024_binder_distribution_multilayer (Bak et al., Chemical Engineering Journal 483, 148913, 2024) · cho2024_conflicting_roles_conductive_additive (Cho et al., Electrochimica Acta 481, 143990, 2024) | 말 없음 (입자 소성 계산 없음) | — | — | —

## m. 받아들일 통찰 (무엇 → 어디 · 왜)

- [m] zhou2026_gyroid_structural_electrolyte_stiffness_ionic_tradeoff | 자이로이드 시트 κ̄ (표 I 8 점 · 표 II 18 점) 를 복셀 σ 코드의 회귀 시험으로 상주 (N 64 · 128 + 1 차 Richardson · 판정 ±1.5 % · 눌린 방향 ±2.5 %) → 단계 7 · 함정: 원문은 고체 정의를 안 적어 네트워크형 (F ≥ t) 으로 하면 +15 … +45 % 어긋남 — 시트형 (−s ≤ F ≤ s) 으로 | §7-3 L220–221 · §8-2 L261–264 · §10 L296 | [우리 산술] · [제안] | 해법 검증 (verification) 이지 물리 검증 아님 (카드)
- [m] zhou2026_gyroid_structural_electrolyte_stiffness_ionic_tradeoff | 격자를 고르기 전에 스캐폴드에서 SE 상 d_h = V/S 를 재 d_h/dx 로 계단 인공물 크기를 어림 (오차 ≈ −0.28/(d_h/dx)) → 단계 7 (STEP3 격자 선택) | §7-3 L222 · §8-3 L266–269 | [우리 산술] | 입자 목 · 가짜 상호연결 (σ↑) 은 이 규칙 밖 (L224 · L268)
- [m] zhou2026_gyroid_structural_electrolyte_stiffness_ionic_tradeoff | 등방 연속체 하한 tau2 ≥ (3−φ)/2 (Hashin–Shtrikman) 를 접촉망 CF 값의 점검선으로 — ps45 CF 7:3 (1.282) · 10:0 (1.247) 이 이 하한 (1.350 · 1.352) 아래 → CF 를 '경로 몫' 그대로 읽지 않는다 · 원문 τ = ε/κ̄ = tau2 (√ 아님) 로 표기 → 흐름 밖: 접촉망 수송 (CF 가지 해석 · τ 규약) | §7-4 L238 · §7-2 L199–202 · §8-1 L256–259 | [우리 산술 · 추정] | 기하 다름 · CF 원기둥 과전도와 압밀 이방성 중 무엇 몫인지 못 가름 (카드)
- [m] asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing | 한 공정 조건 (9.5 m/s) 에 맞춘 유효 파라미터를 다른 조건 (6.25 m/s) 으로 옮기면 실패했다 (Case III = 사실상 hold-out 실패) → 단계 4 에서 항복 세기를 한 조건에 맞출 때 다른 압력 · 조건의 hold-out 을 결과 전에 정함; 결과 전 대조 항목 | §4.11 · Fig 9 · §B-5 L679–681 | stated / digitized | 13 m/s 전이 성패는 카드 안에서 서술이 갈림 (카드 문제)
- [m] asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing | 자유 스칼라 둘 (λ · σ_crit) 이 축퇴하면 절대값이 식별되지 않는다 — 무작위 다중 시작 ≥ 15 · 로그 전처리 · 정규화 · 물리 제약 (ν ≥ 2) 으로 비유일성을 드러냄 (Fig A1 = 국소최소 실재) → 단계 4 (맞추는 값이 둘 이상이 될 때); 흐름 밖: 스케일링 · 역보정 | §A-4 L585–591 · §4.10 L418–423 · §5 L479–480 | stated / 카드 풀이 | —
- [m] asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing | 셀별 질량가중 응력 텐서 → 주응력 → 평균 σ̄ 와 τ_max 를 같이 내는 응력 집계 (좌표계 무관 · 전단 정보 보존) → 단계 5 (관측량 정의) | §4.9 L400–406 · §B-4 L660–671 | stated | 믹서에서는 두 분포가 거의 같았으나 구속 압밀에서는 성립할 이유가 없다 — 우리 침대에서 직접 확인 (카드)
- [m] asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing | Super P 0.20 µm 에 '완전 분산 극한의 분쇄 하한' 이라는 출처를 붙임 (건식 · 습식 [63] · 마이크로 DEM [64] 세 경로가 같은 0.2 µm) · 하한 ≠ 평균 (6.25 m/s 에선 조대 모드가 남음) → 흐름 밖: 첨가제 기하 (`scripts/additives.py` 의 SP_D) | §3.3 L99–108 · §B-1 L621–633 | stated | Super C65 ≠ Super P (같은 계열 · grade 다름 · 카드)
- [m] bak2024_binder_distribution_multilayer | 압연이 이차입자 활물질을 깨 측정을 왜곡하므로 분포 측정은 비캘린더 상태에서 → 조건 R7 (AM 파괴) 의 정성 근거 한 줄; 흐름 밖: 실험 대조 | §2.4 L135–136 · Fig S5 | 표지 없음 | 액체 LIB NCM622 · 압력 미기재
- [m] bak2024_binder_distribution_multilayer | 집전체 쪽 계면 저항과 bulk 저항을 따로 잰다 — 바인더가 집전체 쪽에 몰리면 계면 저항이 폭증 (LMH ~1600 mΩ·cm²) → 단계 7 (판 · 집전체 경계 항); 흐름 밖: 접촉망 수송 경계 조건 | §4.3 L225–233 · Fig 4a | digitize TREND | 액체 LIB · 계면 최저 모델 서술이 갈림 (카드 문제)
- [m] bak2024_binder_distribution_multilayer | 함정 — 전극 유효 σ_e 가 가장 높은 HML (6.94 S/m) 이 성능 최적이 아니다 (MMM 2.46 이 고율 · 사이클 최적) → 흐름 밖: 보고 · 설계 대조 (수송 한 지표로 성능을 말하지 않음) | §4.3 L238–242 · §4.4 | 표지 없음 | —
- [m] bak2024_binder_distribution_multilayer | 단면 EDX (좁은 80–100 µm 선) 대신 10 µm 씩 절삭한 노출면 EDX (60×100 µm² 넓은 면) 로 깊이 분포를 잰다 — F 원자비 ↔ SAICAS 접착 강도 두 측정 교차 → 흐름 밖: 실험 대조 (성분 z 분포 측정법) | §2.4 L132–136 · §4.2 L219 · Fig S4 | 표지 없음 | —
- [m] cho2024_conflicting_roles_conductive_additive | 전자 (이온 차단 SUS 셀 DC 분극 → r_ele) 와 이온 · 계면 (AC TLM → R_ion · R_int) 을 따로 잰 실험 꼴 — CA 가 r_ele 를 2.4–3.3 배 낮추면서 88 wt% 에서 R_ion 을 +26 % 올린다 (반대 부호) → 흐름 밖: 접촉망 · 복셀 수송 (첨가제 효과) 의 결과 전 대조 항목 | §4.1 L155–157 · §4.2 L161–165 · §3 L111–118 · Table S1 | stated | TLM 은 전자 레일 생략 (전자전도 충분 가정)
- [m] cho2024_conflicting_roles_conductive_additive | 함정 — CA 추가로 기공은 +0.01 만 변하는데 tortuosity 는 +17 % (72 wt%) → 단계 7 관측량은 기공과 수송 tortuosity 를 함께 (기공 하나로 연결성을 판정하지 않음) | §6.4 L333–334 · Table S2 | stated | τ 산출법 미명시
- [m] cho2024_conflicting_roles_conductive_additive | 제조 433 MPa ≠ 작동 stack 250 MPa → 실험 기공 · σ 와 견줄 때 어느 압력 상태의 값인지 적는다 → 단계 6; 결과 전 대조 항목 | §4.4 L174 · §2 L94 | stated | 기공을 어느 상태에서 쟀는지는 카드에 없음
- [m] cho2024_conflicting_roles_conductive_additive | 같은 랩에서 LPSCl σ_ion 이 1.6 ↔ 4.8 mS/cm 로 갈린다 (측정 셀 · 압력 · 로트) → σ₀ 절대 비교는 범위로만 → 흐름 밖: σ₀ 기준 상태 | §3 L138–140 · §12 L509–510 | stated / 카드 풀이 | —
- [m] duquesnoy2023_ml_multiobjective_manufacturing_optimization | 비싼 앞 단계 (슬러리 ~150 h) 는 적게 · 싼 뒤 단계 (압연 ~8 h) 조건을 무작위로 많이 붙이는 짧은 quasi-random DOE (Sobol + Saltelli) → 흐름 밖: 계산 배치 설계 (예: DEM 침대 몇 개 × MPM · STEP3 조건 여럿) | §4.2 L135–137 · Fig S1 | stated | —
- [m] duquesnoy2023_ml_multiobjective_manufacturing_optimization | 대리모델이 고른 최적점을 물리 모델로 다시 돌려 대조 (tortuosity −3.8 · σ_e −1.5 · active surface −3.0 · density +0.01 %) 한 뒤 실험 제작 → 흐름 밖: ML 설계 루프 (대리모델 최적점 재계산 규칙) | Table 3 · §3.2 L54–61 | stated | —
- [m] duquesnoy2023_ml_multiobjective_manufacturing_optimization | 압연 축을 두께 감소율 (변위 제어) 로 둔 문헌과 견주려면 우리 압력 기준 결과에 두께 감소율도 함께 적는다 → 단계 5 | §3.0 L41 · §8.C Q4 L305–306 | 카드 풀이 | —
- [m] frankenberg2024_dem_high_intensity_mixer_assb | force-scaling 처방 (δ × f · τ × f · F × f² · E* · G* 상수 → σ_CG = σ₀ · E_m,CG = E_m,0) 과 그 검증 시험 (같은 크기 두 입자 충돌 force–time · 마찰 0.001) → 흐름 밖: 믹서 · 큰 RVE 의 DEM coarse-graining | §4.3 L83–97 | stated | 응력 보존이지 국소 충돌 통계 보존은 아님 (§10 L279)
- [m] frankenberg2024_dem_high_intensity_mixer_assb | 3 단계 분체 보정 (DAOR 회전드럼 → SAOR 실린더 들어올림 → 압축 시험) · 민감도 DoE 16 시뮬로 DAOR 지배 파라미터 (μ_r · μ_s · μ_d · Γ) 를 고름 · 한 속도 보정 · 나머지 검증 · 역학 값은 마지막 (안식각에 영향 작음) → 흐름 밖: 믹서 D3 (SE–SE 점착 유동성 실측 앵커 설계); 단계 4 (보정 · 검증 분리 형식) | §4.6 L112–116 · Fig 2 | stated | 할라이드 + LFP 분체
- [m] frankenberg2024_dem_high_intensity_mixer_assb | 함정 — coarse-grain 압축 곡선은 초반이 실험과 어긋나고 고압축에서만 맞는다 → 단계 4 에서 압축 곡선으로 값을 맞출 때 어느 구간을 썼는지 적는다 | §4.6 L116 · Fig 5b | 카드 풀이 | —
- [m] frankenberg2024_dem_high_intensity_mixer_assb | 회전 속도는 응력 강도 (SI ∝ n^2.1) 와 빈도 (SN ∝ n^0.62) 를 다르게 바꾸고, 같은 SN 에서 SI 가 용량을 가른다 → 흐름 밖: 믹서 판독 (강도 · 빈도를 따로 보고) | §4.8 L129 · §3 L29–33 · Fig 9 | stated | —
- [m] bzox_dry_zro2x_nmc_shell_coating_sulfide_assb | 없음 (안내문 카드) | L1–3 | — | —

## 카드 문제

1. **asylbekov2023** — §3.7 Table 3 (L170) 에서 145.8 은 soft · 13 m/s 의 σ₅₀ **q** 칸인데, L175 와 §10 L809 는 "ν = 158.2 · 145.8 · 60.0" 로 ν (파편 개수) 라 적는다 (자기 표와 어긋남).
2. **asylbekov2023** — Table 2 soft σ₅₀ z₅₀ = 9.86 × 10⁻⁴ (L159) ↔ Table 3 같은 칸 9.8 × 10⁻⁴ (L169). 다른 칸은 반올림으로 맞는데 (3.08 → 3.1 · 4.59 → 4.6 · 1.68 → 1.7) 이 칸만 맞지 않는다 (원문 차이인지 전사인지 카드 표시 없음 · 내 검산).
3. **asylbekov2023** — 13 m/s 전이의 성패가 두 가지: §1 L50–52 · §10 L805 "9.5 → 13 전이는 괜찮다" ↔ §3.8 L197 (Case III 13 m/s 오차가 보정점의 한 자릿수대 · digitized · 숫자 안 옮김) · §5 Fig 9 행 L477 · §9 L778–779 ("6.25 와 13 모두 한 자릿수 큼"). L52 의 "Case IV 로 오차가 한 자릿수 준다" 도 같은 L197 판독으로는 13 m/s 에만 해당.
4. **asylbekov2023** — 철회된 앵커 서술: §7 표 L528 "Minnmann porosity" 를 우리 검증 앵커로 · §A-4 표 L599 "porosity(Minnmann)" 를 18× 연화의 실험 앵커로 · L600 · L603–604 · §9 L781–783 ("세 독립 앵커") — 순수 SE 기공 앵커의 Minnmann 출처는 철회됨 (원장 CL-94).
5. **frankenberg2024** — 같은 부류: §A-2 표 L187 (연화 bed 가 "실험 ~10 % porosity 재현") · L190 ("Minnmann 실험 앵커") · §7 표 L170 · §C (6) L245 · Fig 2 행 L136 · L254 ("우리 단일 Minnmann 앵커").
6. **frankenberg2024 · cho2024** — §C (5) L241 "σ_grain = 3.0 mS/cm × Cronau(r_SE) — LPSCl **단결정** 문헌값 + sub-µm amorphization 인자" · cho2024 §3 L109 · L138 "Cronau 단결정 3.0" — 프로젝트 원장 기준으로 '단결정' 라벨 (3.0 = Cronau 2021 SI 의 µC 펠릿값 · CL-91) 과 Cronau(r_SE) 의 문헌 출처 (모델 가정 · SELF-51) 는 철회됐다.
7. **frankenberg2024** — Δt_out 이 두 값: §4.8 L123 "Δt_out(=0.005 s)" ↔ §6 L149 "Δt_out=5 µs 로 축소".
8. **bak2024** — 계면 전자저항이 가장 낮은 모델이 두 가지: §3 (1) L178 · §4.3 L226–227 "MMM ≈ 최저 ≪ Ref < HML" ↔ 같은 줄 판독값 "Ref ~280 · HML ~10 · MMM ~150" (L227–228) · L230–231 "HML … 계면저항 최저".
9. **bak2024** — 머리 표지 type `MPM` (L3) · `methods: dft` (L12) — 본문은 실험 + GeoDict 복셀 전자 전도이고 MPM · DFT 가 없다 (§2.6 · §7(e) L421–423).
10. **cho2024** — tortuosity 의 지위가 두 가지: §0.2 L44 · §6.4 머리 L326 · §9 L398 · L413 "우리 τ-항 **직접 앵커**" ↔ §12 L504–505 "산출법 미명시 · 절대값보다 추세만 유효 · 정의가 다를 수 있음".
11. **cho2024** — §6.3 읽기 L321 "High-f_AM 이 **모든 R 이 ~5×** 큼" ↔ 같은 표 R_int 241.1 ↔ 145.0 (≈1.7 배) · 같은 문단 (3) L322–323 "R₁ ~2×" (내 검산).
12. **duquesnoy2023** — 모델 최적 기공이 두 가지: §3.0 L46 "~24–29" ↔ §3.5 L95 "~24 %" (Table 3 에는 기공 행이 없다). 또 실측 density 2.6 (> 모델 2.45) 인데 실측 기공 29 % (> 모델 ~24 %) — 같은 조성이면 방향이 맞지 않는데 카드는 "reasonable 일치" 로만 적는다 (§3.5 L95 · 내 대조 · density 는 ± 0.3 오차).
13. **duquesnoy2023** — 압연과 tortuosity 의 방향이 두 가지: §7.2 L243–244 · §10 L327 "CD↑ → τ↑" (Table S3 Liu 값과 같은 방향) ↔ 같은 카드 Table 4 L93 의 이 논문 실험 tortuosity factor 3.5 ± 0.5 (비압연) → 1.8 ± 0.4 (압연 30 %) = 감소. 카드에 설명 없음.
14. **duquesnoy2023** — §3.0 L42 가 'tortuosity factor' 를 "우리 τ_Laplace" 에 대응시킨다 ↔ 카드 §4.6 L187 의 정의 τ = porosity / effective-diffusivity 는 τ 명명 규약상 tau2 (수송 tortuosity · √ 아님) — √ 값 (τ_Lap,eff) 과 다른 양.
15. **duquesnoy2023** — §7.0 L226 "실험 앵커는 문헌 차용(Minnmann/Bazzoun/Doux)" — 무엇의 앵커인지 적혀 있지 않아 철회된 순수 SE 기공 앵커인지 가를 수 없다 (확인 필요).
16. **bzox_dry_zro2x_nmc_shell_coating_sulfide_assb** — 3 줄 안내문 (정독할 내용 없음). 가리키는 정본 `choi2026_bzox_dry_zro2x_nmc_shell_coating` 은 litdb 사본에 있으나 batch_01–38 목록 어디에도 없다 — 정독에서 빠질 수 있음 (내 대조).
17. (소소) 머리 `elements` 줄: duquesnoy2023 L7 "C I" · frankenberg2024 L10 "Cl I In Li O P S" — 본문 소재에 I (요오드) 가 없다 (frankenberg 는 Fe · C 도 빠짐) · cho2024 L21 에 P (LPSCl) 빠짐 · bak2024 L11 "F Li P" (NCM 원소 없음).

참고 (카드 잘못 아님 — 카드가 이미 표시해 둔 원문 문제): asylbekov2023 = ρ 단위 kg m⁻² 오타 (§2 L60) · 본문 §3.5 ↔ Table 3 의 폭 서술 반대 · 중복 문장 (L177–179) · Fig A1 상호참조 오류 (L482–485) · eq 10 에 없는 x₀ 서술 (L322); duquesnoy2023 = Table 1 R² 0.933 두 번 (자기 CI95 밖) · train/test RMSE 스왑 의심 (L70–74) · mass loading 15–40 ↔ 6.7 mg/cm² (L338); bak2024 = SAICAS 2 m/s 단위 (L130) · mg m⁻² (L96) · "9.3:5:2" 오타 (L105) · "L 대비 ~8.4 %" 상대 기준 모호 (L236).

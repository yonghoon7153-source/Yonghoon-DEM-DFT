# 배치 35 정독 근거 (카드 7 장 · 2026-11-11)

읽은 카드 = 7/7 (전문 · 긴 카드 (pan2026 493 줄 · park2019 475 줄 · song2025 523 줄 · oh2026 552 줄) 는 나눠 끝까지).  형식 = `- [글자] slug | 내용 (값 · 단위) | 위치 | 표지 | 한계`.
카드 줄 번호 = 정본 사본 (sha c8faad2d7) 의 줄.  "[우리 산술]" 등 표지는 카드에 적힌 그대로다 (카드 작성자의 계산이지 이 조수의 계산이 아니다).

## a — 순수 SE 압력별 기공 곡선

- [a] otani2023_ionic_conductivity_path_resistance_separation_model | 순수 LPSCl 층 공극–σ 곡선 (공극 3.0–41 % · 예 3.0 % 1.71 · 19.1 % 0.92 · 29.0 % 0.46 · 40.8–41.0 % 0.24–0.28 ×10⁻³ S/cm) — 같은 층을 0.4 → 6.0 tf/cm² (≈39–588 MPa) 로 재가압한 열이지만 **압력 ↔ 공극 짝은 카드에 없음**.  진밀도 = 공급처 재료 밀도 1.8 g/cm³ (랩 표준과 다른 문헌 값) · 공극률 = 두께 + 재료 밀도 (질량 언급은 카드에 없음) · 두께 = 구속 상태 (누른 채) | §3-1 (줄 58 · 60 · 61) · §3-3 (줄 80) · p.2 · p.4 · Fig 4 | [인쇄] (방법 · 밀도) · [판독] (점) · [우리 산술] (MPa 환산) | Mitsui LPSCl x≈1 · D50 0.7 µm · 측정 압력 · 온도 [미확인] · 압력 열과 공극이 함께 변함 · 데이터 기밀
- 그 밖 여섯 장: 이 배치에 없음 (oh2026 의 500 MPa·90 s 펠릿은 SiOx 분말 접촉각용 · 기공 미보고).

## b — 탈압 때 되돌아오는 양 · 잰 방법

이 배치에 직접 값 없음.  참고:

- [b] otani2023 | 되돌아오는 양 없음.  순수 층 공극은 "구속 상태 두께" 로 냈고, SEM 단면 시료는 "구속 못 해 측정 공극률과 다름" (이진화 공극으로 대신) — 누른 채 ↔ 뺀 뒤 차를 보고하지 않음 | §3-1 (줄 60 · 64) · §10-3 (줄 246) · p.2–3 | [인쇄] | 차이 크기 미보고
- [b] pan2026_thesis_rate_capable_energy_dense_cathode_composites | 되돌아옴 측정 없음.  압축률 대 기공 비선형 (40 % 두께 감소에 CT 기공 38 → 29 %) 을 저자는 표면 돌기로 설명 · 카드는 스프링백 (`diener2022_roll_gap_springback_calendering`) 을 같은 방향의 다른 후보로 적음 (압축률 측정 방식 [미확인]) | §3-1-3 (줄 104) · §12 보강 2 (줄 475) · p.43–44 | [인쇄] (저자 해석) · 카드 추정 | 액체 LIB 습식 롤 프레스 · 압력 미기재
- [b] song2025_electrochemo_mechanical_microelectrode_ees | 이 논문 자신의 탈압 측정 없음.  카드가 다른 카드 (`hong2026_cbd_viscoelasticity_springback`, #285) 의 시간 의존 되돌아옴 "RT 3주 +4µm vs HT +1µm" 을 가리키고 이 논문의 Perzyna 점소성을 그 정식 후보로 연결 | §6.3 (줄 427 · 431–438) | 카드 해석 | 액체 LIB CBD · 수치는 다른 카드 몫

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- [c] song2025 | NMC711: E_AM 2.611 GPa · σ_y,AM 0.1534 GPa · 등방 접선 1.3055 GPa · ν 0.25 — 단일입자를 수십 µm 평면 압자로 압축 (카드는 nanoindentation 이라 부름) | Table 2 (줄 148–151) · §2.1 (줄 110–111) | 표지 없음 (표 값) · 카드 해석: 2.611 은 균열 · 기공 포함 유효값 (줄 153–156) | oxide AM · 압입 → 일축 환산 방법 카드에 없음 · 식 22 는 AM 비탄성 변형을 뺌 (σ_y,AM 이 쓰이는지 카드에 없음 → 카드 문제 18)
- [c] song2025 | CBM (PVDF + Super P 통합상): E 1.05 GPa · σ_y 19.36 MPa · 접선 284.90 MPa · ν 0.326 · Perzyna b 1 · A 0 → 3×10⁻³ s⁻¹ · Ludwick n 2 · k ≈1100 → 1200 MPa (변형률 속도 함수) · PVDF 파괴 강도 45 MPa (0.00003 s⁻¹).  항복 함수 = von Mises (f = σ̄ − σ_y · σ̄ = √(3/2 s:s), 식 26–27) — 인장 시험값을 일축 등가 σ_y 로 그대로 씀 | Table 3 (줄 158–173) · §3.2(3) (줄 236–244) · §4.5 (줄 332–344) · Fig 6A | 표지 없음 · Fig 6A 곡선 판독 | 건조 필름 (전해질 swelling 미반영 · 논문 명시) · 바인더이지 SE 아님
- [c] shenouda2020_dem_metal_powder_am_liggghts_tutorial | 항복 · 경화 없음 (Hertz 무한탄성) · 예제 E 강철 200 GPa · 분말 5e7 barye (≈5 GPa) · ν 0.3 | §3 (줄 44) · §4 (줄 67–70) | stated | 소재 무관 예시값
- 나머지 (oh2026 · otani2023 · pan2026 · park2019 · park2026): 값 없음.  oh2026 SAICAS 응집 · 접착 강도 (N/m · Fig 5f,g) 는 항복이 아님.

## d — 단단한 입자의 하중 몫 · 재밍

이 배치에 하중 몫 값 없음.  참고:

- [d] otani2023 | SE 21 vol% 복합의 저공극 영역에서 실측 < 모형 → 저자 해석 "AM 이 가압 충돌로 변형돼 거시 β > 1.5" (재맞춤 없음) · 카드 비판: 모형은 AM 이 하중을 지는 차폐를 반영하지 않음 | §3-4 표 (줄 94) · §4-2 (줄 119) · §10-5 (줄 248) · p.4 | [인쇄] (저자 해석) · 카드 비판 | 하중 몫 정량 없음
- [d] song2025 | 압밀 아님 — 충전 말기 집전체 근처 활물질 최대 von Mises 314 MPa 가 CBM 으로 전달돼 CBM 소성 (Fig 5) | §4.4 (줄 320–323) | 표지 없음 | 사이클 Li 변형 하중 · 액체 LIB

## e — 점접촉 법칙이 깨지는 범위 · 대안 · 맞춘 값 수

- [e] shenouda2020 | Hertz 접촉 면적 A₀ = πa² = 2πRδ 는 a² = 2Rδ − δ² 에서 δ² 를 버린 근사 (작은 겹침 가정) · 원문은 접촉면 변형을 무시한다고 적음 · Hooke 는 characteristicVelocity 입력 필요 (실험 · 수치 · Hertz 시뮬에서 추정) · SJKR (CED) · JKR · DMT (*"작고 약한 점착 입자의 허용 근사"*) 는 교육용 · 소성 분기 (Thornton–Ning · EEPA) 는 데모에 안 씀.  맞춘 값 = 없음 (안식각 데모는 CED 하나를 4.0–9.5×10⁵ erg/cc 로 훑기만 · 실험 맞춤 아님) | §4 (줄 59–63 · 68) · §5 표 (줄 160–169) · 슬라이드 DEM Contact Models | stated | 금속 분말 흐름 · 큰 변형 범위 수치 없음
- 나머지: 이 배치에 없음.

## f — MPM 접촉 · 다물체 · 강체 결합 · 해상도 규칙 · 수치 오차

MPM 카드는 이 배치에 없음.  복셀 · 영상 계산의 해상도 규칙만:

- [f] park2019_electrode_design_methodology_assb_3d | 복셀 0.1 µm = *"approximately a third of the smallest LSTP particle"* (p.125) → LSTP 지름 2.5–5 voxel · **격자 수렴 시험 없음** · RVE 시험 = 도메인 25–200 µm 에서 a_s CV 2.0 · 1.4 % · σ_ion (3 도메인만) 40 % CV 0.85 % · 20 % CV 53 % · 실현 반복 없음 | §3-B (줄 81 · 90) · §4-6 (줄 226–231) · SI Fig. S2–S3 | stated · 우리 산술 (voxel 수 · CV) | 산화물 · 복셀 FVM (접촉 저항 0)
- [f] song2025 | FIB-SEM 43.78 nm 화소 → 계산비용 때문에 600 nm/voxel 로 낮춰 8 절점 고체 요소 · CBM (sub-µm 탄소) 은 개별 입자화 불가 → 목표 부피분율 연속상 · 도메인 30×70.8×30 µm³ (Table 1) ↔ Fig 1E 90×90×90 µm³ · 방전 곡선 하나 ≈2 주 (64 코어) · 격자 수렴 시험 카드에 없음 | §2.2 (줄 115–126) · §3 (줄 191–193) | 표지 없음 | 1차입자 0.5–1.5 µm 대비 해상도 비는 카드에 없음
- [f] pan2026 | μCT 0.5 µm voxel · 평균 공극 지름 3.1–4.2 µm (6–8 voxel) · 목 둘레 9–15 µm (18–30 voxel) > Nyquist 2–4 voxel 을 해상도 근거로 · CBD (100–300 nm) 미해상 → 고체 쪽에 합침 · PNM 편향 *"uniform across all configurations"* (주장 · 검증 없음) | §3-1-2 (줄 80–83) · §10-1-8 (줄 421) · p.38–42 | [인쇄] | 영상 해상도 규칙 (계산 격자 아님)
- [f] otani2023 | 2D 무작위 행보 (행보자 200 개) · 그림 크기 · 화소 · 시료 수 · 반복 [미확인] · 오차 추정 없음 | §3-1 (줄 64–65) | [인쇄] · [미확인] | —

## g — 2D → 3D 경고 · 증거

- [g] otani2023 | 2D SEM 단면 무작위 행보로 낸 경로 저항 계수가 3D 펠릿 실측 σ–공극 곡선을 재현 (순수 층 · p.4) = 증거 한 건.  카드 경고: 2D 단면은 3D 연결을 과소 · 과대평가할 수 있다 (2D 퍼콜레이션 문턱이 다름) · SEM 시료는 무구속이라 공극이 다름 | §3-3 (줄 79–81) · §10-3 (줄 246) · Fig 4 · 5 | [인쇄] (재현) · 카드 비판 (경고) | 복합 (AM 있음) 은 2D 계수를 안 냄
- [g] pan2026 | η = 2D FIB 단면 호 길이 ÷ 둘레 = "3D 접촉 면적 분율의 2D 대리" · Holm 산술에 2D 호 길이의 절반을 3D 반지름으로 씀 (입체해석 보정 없음) · 카드: 2D 호 길이 ≠ 3D 접촉 지름 | §3-2-9 (줄 212) · §4-2 (줄 289) · §10-2-3 (줄 430) | [인쇄] · 카드 비판 | 10–11 입자 · 불확도 없음

## h — DEM 에서 FE · MPM 으로 넘긴 선례

이 배치에 없음.  참고: song2025 = FIB-SEM 재구성 → 복셀 FEM (DEM 아님 · §2.2) · park2019 = 확률 배치 복셀 → σ_eff · a_s → COMSOL P2D 에 직접 투입 (DEM 아님 · §4-4 줄 205–206).

## i — 복합 양극 (AM + SE) 의 압력별 기공

- [i] otani2023 | NCM523 + LPSCl 막자 혼합 · SE 54 / 35 / 21 / 10 vol% (고체 기준) · 같은 압력 열 (0.4 → 6.0 tf/cm²) 재측정 → 공극 범위 54 %: 8.1–33.5 % · 35 %: 7.2–31.0 % · 21 %: 8.9–36.3 % · 10 %: 11.8–12.4 % (σ 와 짝 · **압력 ↔ 공극 짝은 카드에 없음**) · 공극 = 두께 + 두 재료 밀도 (전체 부피 기준) | §3-1 (줄 62–63) · §3-4 표 (줄 92–95) · Fig 6 | [인쇄] (조성 · 방법) · [판독] (점) | 복합의 구속 여부 명시 없음 · 바이모달 아님 · 데이터 기밀
- [i] pan2026 (참고 · SE 없음) | 액체 LIB NCM811 롤 프레스 압축률 0/20/40 % → CT 거대 기공 38/35/30 % · 같은 두께 질량 수지로는 6.5 % → CT 기공 ≠ 총 기공 | §3-1-3 (줄 89–91) · §10-1-1 (줄 414) | [인쇄] · [우리 산술] | 압력 미기재 · ASSB 아님

## j — 카드가 적은 한계 가운데 가압 · 탈압과 닿는 것

- [j] otani2023 | 모형 가정 셋 (SE ≪ AM · 퍼콜레이션 무시 · 전극 안 분포 무시) · SE 21 % 저공극 = AM 변형 (거시 β > 1.5) 로 어긋남 (재맞춤 없음) · SE 10 % = 퍼콜레이션 붕괴 · 높은 공극에서는 Nyquist 반원이 안 보여 σ 못 얻음 · 흑연은 눌리면 납작해져 거시 β 증가 예상 (시험 안 함) | §3-2 (줄 74) · §3-4 표 (줄 94–95) · §3-5 (줄 109) · p.4–5 | [인쇄] | —
- [j] park2019 | *"Although the reliability is not confirmed by experimental data, we believe that this modeling and simulation approach is quite meaningful"* (p.128) · 압밀 · 기계 없음 (확률 배치 + 열처리 접촉 가정 p.125) | §2 (줄 56) · §4-5 (줄 213–223) | stated | —
- [j] song2025 | 소성 기반 기계 열화만 예측 — 입자 균열 · 집전체 분리 · SEI · Li 도금 · 가스 미반영 (계산비용 + 파괴 모델 부재 · 논문 명시) · 바인더 인장 = 건조 필름 (swelling 미반영 · 논문 명시) · AM 은 취성 탄성 (식 22) | §4.5 (줄 334–335 · 345–346) · §3.2(2) (줄 228–230) | 표지 없음 (논문 명시) | 사이클 하중이지 압밀 · 탈압 아님
- [j] pan2026 | *"most tests presented here were only repeated once or twice"* (p.60) · CT 는 CBD · 하위 복셀 기공을 못 봄 · PNM 편향 균일 주장 검증 없음 · 압축률 정의가 표마다 반대 (줄어든 % ↔ 남은 %) | §3-2-1 (줄 159) · §3-1-2 (줄 82–83) · §10-1-2 (줄 415) | [인쇄] | 액체 LIB
- [j] shenouda2020 | 구만 (multisphere · superquadratic 은 언급만) · Hertz 는 접촉 변형 무시 · 운동에너지가 *"wildly varying"* 이면 불안정 → 입자를 적게 · 천천히 넣거나 강성 낮춤 | §4 (줄 79 · 94) · 줄 264 | stated | 흐름 응용

## k — DEM 의 한계 (인용 가능 서지)

- [k] shenouda2020_dem_metal_powder_am_liggghts_tutorial (S. Shenouda & A. Hoff, LLNL-TR-813736, Lawrence Livermore National Laboratory 기술보고서, 2020 · DOI 없음) | (1) 접촉 면적 A₀ = 2πRδ 는 a² = 2Rδ − δ² ≈ 2Rδ (δ² 무시) 근사이고, 원문은 Hertz 가 *"neglects the deformation at the contact area"* 라 적음 (2) 입자는 구만 (`atom_style granular` · `fix nve/sphere`; multisphere · superquadratic 은 "다른 옵션" 언급만) → 모양 안 변함 (3) 안정 시간 간격 = Rayleigh 시간 간격의 ~20 % · Hertz 시간 간격은 V_max 를 미리 알아야 함 · KE 가 *"wildly varying"* 이면 불안정 (4) 소성 · 항복 없음 (Hertz 무한탄성).  믿을 수 있는 겹침 · 밀도 상한 수치는 없음 | 줄 59 · 264 (원문 따옴표) · §4 (줄 70 · 79–81 · 89 · 94) · §4.5(a) (줄 106–109) · 튜토리얼 §2.4.1 | stated | 흐름/안식각 응용 · 압밀 범위는 말 없음 · 카드 해석: 'soft' = 겹침 허용이지 입자 변형 아님 (줄 303)
- [k] otani2023_ionic_conductivity_path_resistance_separation_model (K. Otani et al., J. Energy Storage 58 (2023) 106279) | 말 없음 (DEM 안 씀).  서론에 시뮬레이션 소프트웨어 관련 문단 (*"Nevertheless, such simulation software may be difficult …"*, p.1 · p.2 두 번) 이 있으나 카드엔 첫 낱말만 — 원문 확인 필요 | §10-6 (줄 249) | [인쇄] (첫 낱말) | 내용 [미확인]
- [k] oh2026 · pan2026 · park2019 · park2026 · song2025 | 말 없음 (DEM 안 씀) — park2019 는 DEM 대신 GeoDict 확률 배치 (§4-5 줄 217) · pan2026 은 시뮬레이션 입자 없음 (§4-2 줄 288) | — | — | —

## l — 소성변형이 왜 어려운가 · 택한 우회

- [l] song2025_electrochemo_mechanical_microelectrode_ees (J. Song, R.C. Ihuaenyi, J. Lim, …, Y.M. Lee, J. Zhu, Energy Environ. Sci. 18 (2025) 3129–3147 · DOI 10.1039/d4ee04856c) | **이유**: 기존 입자 수준 모델은 대부분 작은 변형 · 탄성만 가정해 활물질의 큰 수축/팽창과 CBM 소성을 무시 — 원문 *"these models only consider elastic deformation when analyzing CBM … neglecting the plastic deformation"* · 계산비용 때문에 43.78 nm → 600 nm/voxel 로 낮추고 sub-µm 탄소는 연속상으로.  **우회**: 균질화 없이 성분마다 지배식 (*"directly defining the governing equations on each component … avoiding homogenization and approximations"*) + CBM 만 Perzyna 점소성 + Ludwick 경화 (식 24–31) · AM 은 취성이라 *"strain tensor formulation excludes viscoplastic strains"* (식 22) · 작은 변형 가산분해 (식 20) + deformed geometry.  **맞춘 값** = CBM E · σ_y · 접선 · Perzyna A(속도) · b · Ludwick k(속도) · n — 건조 필름 인장 3 속도 (0.00003/0.0003/0.003 s⁻¹ · 정확도 89.21/93.75/97.11 %).  **검증** = 코인셀 전압 >98 %.  **비용** = 방전 곡선 하나 ≈2 주 (Threadripper PRO 64 코어) | §1 (줄 98–99) · 줄 67–68 (원문) · §2.2 (줄 123–126) · §3 (줄 191–193 · 228–244) · §4.5 (줄 332–337) · §6.4 (줄 467) | 표지 없음 (본문 · 표) | NMC711 + PVDF · 액체 · 소성 주체 = 바인더 (입자 형상 고정 · AM 탄성) · 압밀 아님
- [l] park2019_electrode_design_methodology_assb_3d (J. Park et al., Energy Storage Mater. 19 (2019) 124–129 · DOI 10.1016/j.ensm.2019.03.012) | 소성 · 압밀을 계산하지 않고 접촉을 가정으로 대신 — *"we assumed that 1D or 2D contacts in the ASSEs could be formed by the heat treatment process"* (p.125) + LSTP 를 NG 에 −0.1 µm 겹쳐 놓기 (*"which allows LSTP particles to be located around NG and leads to real contact between the NG and LSTP particles while minimizing the deformation of NG particles"*, p.126) · 맞춘 값 0 (σ₀ = 문헌 입력) · 검증 없음 (p.128) · 계산 비용 카드에 없음 | §3-B (줄 86 · 88) · §4-1 (줄 168) · §4-5 (줄 213–223) | stated | 산화물 · 흑연 음극 · 압력 축 자체 없음
- [l] otani2023 (K. Otani et al., J. Energy Storage 58 (2023) 106279) | 입자 계산 없이 실측으로 우회 — 실험에는 SE 소성 · 치밀화가 압력 열에 들어 있고 (공극 41 → 3 %), 모형은 접촉 면적 (목) 효과를 β = 4 하나에 뭉뚱그림 (따로 매개변수 없음 · 순수 층 실측 맞춤 1 개 · 복합에 그대로 옮김) | §4-2 (줄 119–120) · §3-2 (줄 73) | [인쇄] · 카드 정리 | 수송 모형 (역학 없음)
- [l] shenouda2020 (LLNL-TR-813736, 2020) | 말 없음 — 소성 · 항복을 다루지 않음 (Hertz + SJKR) · 카드 해석: 흐름 · 안식각은 압밀 고압이 아니라 탄성으로 충분 | 줄 82 | 카드 해석 | —
- [l] oh2026 · pan2026 · park2026 | 말 없음 — pan2026 은 압축을 실험 변수로만 다루고 입자 소성 · 형상 변화는 SEM 정성 관찰뿐 (§4-2 줄 290) | — | — | —

## m — 받아들일 통찰 (무엇 → 자리 | 왜 · 위치 | 표지 | 한계)

oh2026
- [m] oh2026_carbon_coating_siox_ion_electron_balance | 눌러 만든 분말 펠릿 (500 MPa·90 s) 위 극성 (DIW) · 비극성 (DIM) 접촉각 → OWRK 로 γᵈ · γᵖ 분리 → W_adh = 2(√(γ₁ᵈγ₂ᵈ) + √(γ₁ᵖγ₂ᵖ)) 로 두 고체상 부착을 숫자로 → 흐름 밖: 믹싱 (이종기술 논지의 γ_A/γ_S 판가름 수 측정 방법 후보) | SiOx↔CBD W_adh 99.9 → 108.6 mN/m 가 SSRM · 유변학 분산 개선과 같은 방향 · §2.5 (줄 138–143) · §4.2 (줄 245–257) · Table S1 | 표지 없음 | 황화물 분말에 같은 액체 · 같은 법을 쓸 수 있는지 카드에 없음
- [m] oh2026 | 분산 균일도 스칼라 = 복셀 탄소 점유율의 공간 변동계수 · 최근접 탄소 거리 분포 → 흐름 밖: CBD 분산 (STEP3 셀맵 후처리 · SSRM 추세와 대조) | 우리에게는 근접도 지표만 있고 균일도 스칼라가 없다는 카드 진단 · §7(b) (줄 461–465) · §8-3 (줄 524–530) | 카드 제안 | 원 논문 방법이 아니라 카드 설계
- [m] oh2026 | 탄소량을 0.5 → 4 wt% 로 훑으며 σ_e 이득 · σ_ion 손실을 한 그림에 → 흐름 밖: CBD 탄소량 균형점 | 실험: 전자는 moderate ↔ thick 에서 포화 (0.013 ↔ 0.012 Ω·cm) · thick 은 Rct · DCIR ↑ → "중간 (2.91 wt%) 이 균형" · §4.1 (줄 215–216) · §4.3 (줄 273–274) · §8-2 (줄 517–522) | 디지타이즈 TREND only · 카드 제안 | 액체 계 · 기전 (CCL 이 Li⁺ 경로를 막음) 이 우리 (SE 망 교란) 와 다름
- [m] oh2026 | 함정: SSRM 그림 색 범례가 본문 서술과 반대로 읽힐 수 있음 → 흐름 밖: 실험 맵 판독 (범례 ↔ 본문 먼저 대조) | §4.2 (줄 237–239) | 카드 경고 | 카드 안에서도 CBD 저항 고저가 갈림 (카드 문제 3)

otani2023
- [m] otani2023 | 분포를 모르는 귀무 모형 f = ε_SE⁴(ε_SE + ε_void)^−2.5 (τ_all = τ_macro β 1.5 × τ_micro β 4) → 단계 7 결과 전 대조 항목; 흐름 밖: 믹싱 (같은 SE 량 · 공극에서 벗어나는 만큼 = 분산 · 코팅 효과 후보) | ps45 다섯 침대에서 우리 Hertz tau2 의 0.94–1.02 배 (union 공극이면 1.01–1.09) · Nakamura 2020 혼합 8.52 ↔ 측정 8.86 · 코팅 9.74 ↔ 5.49 · §3-2 (줄 75) · §7-2 (줄 170–180) · §7-3 (줄 183–191) | [우리 산술] · [추정] | β 4 = Mitsui LPSCl 순수 층 맞춤 · 우리 tau2 시드 1 개 침대
- [m] otani2023 | 순수 층이 σ = σ₀(1−p)⁴ 이면 펠릿 σ₀ 는 펠릿 공극의 함수 (공극 10 % → 재료값 × 0.66) → 기준 펠릿의 두께 · 질량 · 압력을 반드시 기록 → 흐름 밖: σ₀ 기준 상태 (CL-91 재해석 참고값) | §7-4 3 (줄 198) · §8-4 (줄 223–226) | [우리 산술] · [추정] | Cronau 펠릿 공극 미상
- [m] otani2023 | 같은 조성에서 공극 7 → 31 % 사이 σ 가 한 자릿수 바뀜 (SE 35 %: 1.7×10⁻⁴ → 1.4×10⁻⁵ S/cm) → 실험 σ 는 공극을 공변량으로 함께 잰다 → 흐름 밖: 대칭셀 실험 대조 | §7-4 2 (줄 197) · Fig 6 | [판독] | 다른 재료 · 입경 · 혼합
- [m] otani2023 | 함정: 원문이 기하 τ = l/L (식 1) 을 σ = σ₀ε/τ (식 2) 의 tortuosity factor 자리에 넣음 — "경로 ≈1.2" (기하) 와 "경로 저항 계수 ≈3" (수송) 을 섞어 옮기지 않는다 → 단계 7 관측량 정의 (τ 명명 규약) | §8-6 (줄 233–236) · p.1–2 | [인쇄] | —

pan2026
- [m] pan2026_thesis_rate_capable_energy_dense_cathode_composites | 영상 (CT) 기공은 총 기공이 아니다 — 같은 두께에서 질량 수지 6.5 % ↔ CT 30 % (CBD · 하위 복셀 기공 · 표면 돌기) → 영상 기공은 질량 수지 기공과 나란히 적는다 → 단계 0 (기공률 연산자 정의 · 결과 전) | §10-1-1 (줄 414) · 표 4.4 | [우리 산술] | 액체 LIB 습식 전극
- [m] pan2026 | 2D 단면 접촉 분율 η = L_contact/P (FIB 단면 10–11 입자 · 접촉 수 · 점당 길이 따로) → 우리 침대의 합성 단면 η 를 같은 정의로 (입체해석 보정 포함) → 단계 7 (피복) · 결과 전 대조 항목 | CB 는 압축에 접촉 수 ↓ · 패치 ↑, 혼성은 둘 다 ↑ (반응이 갈림) · §3-2-9 (줄 211–222) · §8-2 (줄 389–392) | [인쇄] · 카드 제안 | 2D 호 길이 ≠ 3D 지름 · 탄소–LMR
- [m] pan2026 | 함정: Holm 기하 산술 1.9× ↔ EIS R2 비 ≈20–27× (같은 쌍은 19.6×) — 전자 협착과 전하 전달은 다른 양 → 접촉망 σ 를 EIS R2 로 검증하지 않는다 → 흐름 밖: 접촉망 수송 검증 | §3-2-9 (줄 223–224) · §7-4 (줄 377) · §10-2-3 (줄 430) | [인쇄] · [우리 산술] | —
- [m] pan2026 | 같은 조성 · 통합 방식만 다른 MF ↔ MIX 비교는 C/20 에서 차이가 거의 없고 율 · 깊은 점검 사이클 뒤에 드러남 → 코팅 비교는 율 3 수준 이상 + 점검 사이클 전후 + 탄소 배치 같게 (MF 에만 Super-P 1 % 예비 혼합 · MIX [미확인]) → 흐름 밖: 코팅 활물질 믹싱 실험 · 계산 설계 | §3-3-5 (줄 254–258) · §7-3 1 (줄 370) · §8-1 (줄 384–387) | [인쇄] · [추정] | 액체 LMO/LFP

park2019
- [m] park2019_electrode_design_methodology_assb_3d | RVE (도메인 크기) 시험은 문턱 근처 조성에서 — 40 % σ CV 0.85 % 인데 20 % 는 CV 53 % (σ 는 3 도메인만) → 단계 7 (대표성 시험 조성 고르기 · 결과 전 등록) | §4-6 (줄 226–229) · §8-3 ① (b) (줄 417) | 그림 안 stated · 우리 산술 (CV) | 복셀 · 산화물
- [m] park2019 | τ 계열 값을 낼 때 σ₀ 를 숫자와 같은 줄에 (원문 이온 N_m × σ_eff = Table S3 σ₀ 의 0.80 배 → 재구성 불가) · 복셀 σ 에 격자 수렴 · 실현 수를 붙인다 → 단계 7 보고 방식 | §τ(4) (줄 357–368) · §8-3 ① (a)(c) (줄 417) | 우리 산술 | —
- [m] park2019 | 접촉 면적 a_s 의 분모 (AM 부피 ↔ 전극 부피) 가 ε_s 배 (0.40–0.46) 를 가름 → 면적 열마다 분모를 명기 → 단계 7 (피복 · 면적 정의) | §4-2 (줄 174–176) · §8-2 결정 9 (줄 411) | stated · 우리 산술 | 원문 Fig. 2b 두 축이 그 정의로도 재현 안 됨
- [m] park2019 | P2D 에 τ 대신 3D σ_eff (+ σ₀ 짝) 를 바로 넣은 선례 → τ ↔ √τ 모호성 회피 → 흐름 밖: COMSOL/P2D 인계 | §4-4 (줄 205–206) · §8-2 결정 5 (줄 410) | stated | a_s 분모 환산 미기술

park2026
- [m] park2026_ceramic_pp_separator | 없음 (카드도 §8 줄 315 "정직하게 없음").

shenouda2020
- [m] shenouda2020_dem_metal_powder_am_liggghts_tutorial | `fix ts_check all check/timestep/gran 1000 0.2 0.2` (1000 step 마다 Rayleigh · Hertz 시간 간격 20 % 초과 경고) + dt_R = πR√(ρ/G)/(0.1631ν + 0.8766) → 강성 · 겹침이 바뀌는 압밀 중 시간 간격 자동 점검 → 후보 D0 · 후보 C′ | 카드 대조: 우리 덱은 dt 고정 · §4.5(a) (줄 106–109) · §8 ② (줄 216) | stated | 카드가 적은 우리 SE 입력값 (ρ=2000 등) 은 확인 필요 (카드 문제 11)
- [m] shenouda2020 | 새 접촉 모델 조합은 `src/style_contact_model.whitelist` 에 있어야 함 (없으면 "ERROR: Contact model not found in any whitelist") → 후보 C′ · 후보 C (항복 캡 · 큰 변형 접촉 조합을 넣을 때 실무 점검) | §4 (줄 64) · Fig 2 · §8 ⑤ (줄 219) | stated | PUBLIC 판 기준
- [m] shenouda2020 | 자유낙하 공 반발을 MATLAB ode45 해석해와 시계열로 대조 (국소 극값 오차 ~0.3 %) → 접촉 법칙을 바꿀 때 첫 단위 시험 (입자–벽 반발 · U5 앞단) → 후보 C · C′ 단위 시험 | 슬라이드 p.17–20 · Fig 17–20 (줄 48 · 148) · §6 (줄 176) | stated | 탄성 반발 (CoR 0.9) 만 · 소성 분기 시험 아님

song2025
- [m] song2025_electrochemo_mechanical_microelectrode_ees | 구조를 격자로 옮긴 뒤 상 부피분율을 원본과 대조 (AM 0.68355 ↔ 0.68335 · CBD 0.08067 ↔ 0.08062 · 공극 0.23582 ↔ 0.23583) → 단계 7 (DEM/MPM → 복셀 변환 뒤 상 부피 보존 검사) | Table 1 · §2.2 (줄 120–122) | 표지 없음 | 다운샘플 600 nm 뒤 값인지 카드에 없음
- [m] song2025 | 유효 반응 면적 = 입자 비표면적에서 비반응 계면 (AM–CBM 의 88 % · AM–집전체 · 측면) 을 빼서 = 61.76 % → 피복 · 반응 면적을 "가린 면적 차감" 으로 정의 → 단계 7 (피복 정의); 흐름 밖: STEP4 반응 면적 | §4.2 (줄 276–286) | 표지 없음 | CBM 전해질 함유 12 % 가정 (Table 3 0.16 과 다름 — 카드 문제 15)
- [m] song2025 | 속도 의존 재료는 변형률 속도 셋 (0.00003/0.0003/0.003 s⁻¹) 에서 맞추고 속도별 정확도 (89.21/93.75/97.11 %) 를 따로 보고 · Perzyna λ̇ = A⟨f/σ_y⟩ᵇ + Ludwick σ_y = σ_y0 + k ε̄_vpⁿ → 단계 6 · 조건 R4 (시간 의존 되돌아옴 정식 후보 · 맞춤 방법) | §3.2(3) (줄 236–244) · §4.5 (줄 332–337) · §6.3 (줄 431–438) | 표지 없음 | PVDF 건조 필름 값은 옮기지 않음 · SE 크리프 자료 아님
- [m] song2025 | 함정: 건조 중 바인더가 끓어 생긴 기공이 전극 표면 근처 CBM 연결을 끊고 전류 분포를 좌우 (CBM 전류밀도가 AM 의 10 배 넘음) → 흐름 밖: 탄소망 연결성 (공정 결함이 σ_e 를 바꾸는 경로) | §4.3 (줄 309–315) | 표지 없음 | 습식 공정 · 건조 온도 표기 둘 (카드 문제 16)

## n — 논문 에이전트 후보 (litdb 에 카드 없음 · 많아야 다섯)

litdb 확인 방법 = `litdb/papers/` 목록 (488 개) 을 제1 저자 성으로 `ls` 걸러 보고, 권쪽 · 제목 낱말 · DOI 조각을 내용 grep (INDEX 미사용).  So 2021 JES 168 030538 (otani ref 8 · `so2021_dem_fabrication_degradation_ductile_particles`) · Park 2020 Chem. Eng. J. 391 123528 (park2019 [12b] · `park2020_dimension_controlled_se_percolation_contact_area`) · Hong 2026 #285 (`hong2026_cbd_viscoelasticity_springback`) 는 카드가 있어 뺐다.  Siroma 2016 은 배치 33 에 이미 올라 뺐다.

- [n] M. Kodama, S. Komiyama, A. Ohashi, et al., J. Power Sources 462 (2020) 228160 (서지 일부만 — 제목 · DOI 가 이 카드에 없음) | a (순수 황화물 SE 를 고압에서 in situ XCT — 누른 채 구조 · 공극) · m (otani2023 이 "③ 격자 부정합 저항 무시" 를 refs 7 · 22 와 같은 방향이라 할 때의 근거 22) — otani2023 카드 줄 265 "카드 없음 — 고압 in situ XCT · 황화물 입계 저항 무시 근거" · 줄 30 · 81 | papers/ 에 kodama 파일 없음 · "228160" grep = faka2026 · otani2023 · yadav2021 (인용만) · 제목 낱말 "High-pressure in situ X-ray" = yadav2021 인용뿐 → 카드 없음
- [n] J.A. Greenwood, Constriction resistance and the real area of contact, Br. J. Appl. Phys. 17 (1966) 1621–1632 (DOI 카드에 없음) | m · k (수송 쪽 "접촉끼리 독립" 가정 — 다접촉 협착의 상호작용 항 · 우리 Holm 망은 접촉마다 독립 직렬) — pan2026 카드 줄 465 "카드 없음 — 다접촉 협착 (우리 Holm 망의 상호작용 항)" | papers/ 에 greenwood 파일 없음 · 제목 · "Br. J. Appl. Phys" grep = pan2026 뿐 (bielefeld2020 · lee2024_multiphysics 는 "Greenwood 1966" 이름만) → 카드 없음
- [n] G. Inoue, M. Kawase, J. Power Sources 342 (2017) 476–488 (서지 일부만 — 제목 · DOI 가 이 카드에 없음) | m (흐름 밖: 재구성 다공 전극 구조 ↔ 유효 전도도의 수치 · 실험 평가 — otani2023 · So 계보 (같은 교신) 의 수송 방법 원전) — otani2023 카드 줄 262 "카드 없음 — 다공 전극 구조 ↔ 유효 전도도 (같은 교신)" | papers/ 에 inoue 파일 없음 · "Kawase" grep = hlushkou2018 · kaiser2018 · otani2023 · so2021 (인용만) → 카드 없음
- [n] M. Klingele, R. Zengerle, S. Thiele, Quantification of artifacts in scanning electron microscopy tomography: improving the reliability of calculated transport parameters in energy applications such as fuel cell and battery electrodes, J. Power Sources 275 (2015) 852–859 (DOI 카드에 없음) | f · m (영상 기반 구조에서 계산한 수송 매개변수의 인공물 · 오차 정량 — 단계 7 복셀 σ 의 영상 · 격자 오차 추정 근거 후보 · ConductoDict 경계 · 솔버 관행 확인 후보) — park2019 카드 줄 469 | papers/ 에 klingele 파일 없음 · 제목 · 이름 grep = park2019 뿐 → 카드 없음
- [n] D. Hou, J. Han, C. Geng, Z. Xu, M.M. AlMarzooqi, J. Zhang, Z. Yang, J. Min, X. Xiao, O. Borkiewicz, K. Wiaderek, Y. Liu, K. Zhao, F. Lin, Surface coating by mechanofusion modulates bulk charging pathways and battery performance of Ni-rich layered cathodes, Proc. Natl. Acad. Sci. U.S.A. 119 (2022) e2212802119 (DOI 카드에 없음) | m (흐름 밖: 코팅 활물질 믹싱 — 메카노퓨전 코팅이 벌크 충전 경로를 바꾼다는 근거 · pan2026 MF↔MIX 설계와 대조) — pan2026 카드 줄 466 | papers/ 에 hou 파일 없음 · "e2212802119" · 제목 grep = pan2026 뿐 → 카드 없음

## 카드 문제

1. oh2026 | 머리 메타 type `FEM·digital-twin` (줄 3) · methods `adhesion, dft` (줄 12) ↔ 본문 = 실험만 (§2 · §7(d) 줄 486–488 "입자스케일 압축역학 예측 없음") — 계산 없음.
2. oh2026 | Minnmann 을 "LPSCl cold-press" σ/porosity 절대 앵커로 적음 (줄 40 · 421 · 548–549) — 철회된 출처 (CL-94).
3. oh2026 | SSRM 색 · 저항 해석이 카드 안에서 갈림: 줄 135 "저항이 낮은 (파랑) = 활물질, 높은 (빨강) = CBD" · 줄 237–238 "빨강 = 도전재 + 탄소코팅층 (고저항?)" ↔ 줄 240–241 "bare: 국소 응집된 저저항 영역 (CBD aggregation)" (카드도 줄 238–239 에서 주의 표시).
4. oh2026 | 음극 조성 "80:9:1:5:1.5:5 wt%" (줄 109) 여섯 수의 합 101.5 · SiOx-only 음극 조성 "80:9:1:5.5…" ↔ "본문 80:9:1:5:5" (줄 114–115) 두 표기.
5. park2026 | 머리 메타 type `DEM` (줄 3) · methods `dft` (줄 12) ↔ 본문 = 분리막 실험 (DEM · DFT 없음 · §7 줄 296–298).
6. park2026 | Minnmann (LPSCl cold-press) 를 σ/porosity 절대 앵커로 (줄 63–64 · 285 · 311 · 340) — 철회된 출처.
7. shenouda2020 | 줄 269 "real_14 16.7↔DEM 15.6↔Minnmann 10 % 교차검증" · 줄 281 "DEM(Minnmann porosity + Cronau overlap) ⟂ MPM(SEM + Minnmann pure-SE) 각각 실험에 독립 보정" · 줄 199 · 277 · 305 (Minnmann 앵커) — Minnmann 10 % 를 실험 근거로 적음 (철회된 출처) · 16.7↔15.6 을 독립 교차검증으로 적음 (프로젝트 CLAUDE.md 2026-09-09 정정 = 같은 기하 일관성이지 독립 확인 아님).
8. shenouda2020 | CED 스윕 범위: 줄 24 "0→9.5×10⁵ erg/cc" ↔ 줄 68 · §5 표 (줄 161–168) "4×10⁵–9.5×10⁵".
9. shenouda2020 | 유량 단위: 줄 47 "~36 → ~29 g/cc" ↔ 줄 130 · 175 "g/s".
10. shenouda2020 | 회귀식 "θ=0.0079·CED²−0.209·CED+20 (CED 단위 ×10⁵)" (줄 46) — 표의 CED 를 ×10⁵ 단위 (4–9.5) 로 넣으면 θ ≈ 18.7–19.3° 로 표 (24.7–73°) 와 안 맞고, ×10⁴ 단위 (40–95) 면 ≈24–71° 로 맞음 (조수의 단순 대입 확인 · 카드 산술 아님).
11. shenouda2020 | 줄 248 우리 SE 입력을 "r=0.5µm·ρ=2000·E_eff=1.35 GPa" 로 적음 (단위 없음) — 랩 표준 LPSCl 진밀도 1.64 g/cm³ 와 다른 값 (DEM 입력값인지 확인 필요).
12. song2025 | Minnmann "(pure-SE 10%@300MPa)" 를 절대 앵커로 (줄 523) · 줄 28 · 81 · 482 · 508 — 철회된 출처.
13. song2025 | D_s,init: Table 2 행 "3×10⁻¹¹ cm²/s (=3×10⁻¹⁵ m²/s)" (줄 144) ↔ 식 3 · 요약 "3×10⁻¹⁴ m²/s" (줄 201 · 376 · 402) — 10 배 차.
14. song2025 | t₊: "≈0.38 (1 M 기준)" (줄 41 · 79 · 181 · 473) ↔ Table 4 곡선 "t₊ ~0.10–0.30 (c_e 400–1600)" (줄 181) — 1 M 는 그 범위 안인데 값이 다름.
15. song2025 | CBM 전해질 분율: Table 3 "0.16" · 식 6 "ε_e=0.16" (줄 169 · 207) ↔ 반응 면적 계산 "CBM 12% 전해질 함유 가정" (줄 281).
16. song2025 | 건조 온도: "160°C 1 h 건조" (줄 44) ↔ "슬러리 건조 (130°C) 중 바인더 boiling" (줄 313).
17. song2025 | 도메인 30×70.8×30 µm³ (Table 1) ↔ Fig 1E 90×90×90 µm³ (줄 124–125 · 카드가 표시) · Al 집전체 E_CC "6.88 GPa (또는 2.611 표기)" (줄 185) 두 값.
18. song2025 | Table 2 에 σ_y,AM 0.1534 GPa · 접선 1.3055 GPa (줄 149–150) 가 있으나 식 22 는 AM 의 비탄성 변형을 뺌 (줄 228–230) — 이 값이 계산에 쓰이는지 카드에 없음.
19. pan2026 | 출처 표지: 1저자 전달 메모 "가천대 최준현 교수 연구실 (건식 전극)" ↔ 인쇄본 = CMU · Bonian Pan · 습식 전극 (줄 12 · 카드가 1저자 확인 대기로 표시).
- (참고 · 카드 내부 모순 아님) pan2026 줄 359 의 우리 σ_e 실험 앵커 "SBE 4.47 · DBE 12.4 mS/cm" 는 카드 작성 (10-13) 뒤 바뀐 값일 수 있음 — 프로젝트 CLAUDE.md 10-19 줄은 SBE 1.63 · DBE 4.68 mS/cm 로 대체.
- (참고 · 이 배치 밖 카드) otani2023 §10-1 (줄 244) 이 `lee2024_multiphysics_dem_fem_initial_pressure_assb` 카드의 선형식 τ = −11.7·ε_SE + 8.54 "Otani 2023 ref46" 귀속이 이 논문 본문 · 그림에 없다고 적음 — 그 카드 쪽 문제 (Lee 2024 원문 ref 46 · 식 38 대조 필요).
- otani2023 · park2019 | 카드 자체 문제 없음 (park2019 가 표시한 ×0.80 등은 원문 내부 불일치).

# batch 109 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 표 N-70 · 대피 세션)

대상: `xu2023_dem_bonded_particle_fracture_calendering` — J. Xu · B. Paredes-Goyes · Z. Su · M. Scheel · T. Weitkamp · A. Demortière · A. A. Franco, "Computational Model for Predicting Particle Fracture During Electrode Calendering", *Batteries & Supercaps* **6** (2023) e202300371 · DOI 10.1002/batt.202300371
액체 LIB NMC111 양극 (SE 없음) 의 2 차 입자를 1.59 µm 1 차 구 응집체 + 끊어지는 결합 (BPM) 으로 만든 3D LIGGGHTS 압연 DEM (평판 0–157.7 MPa · 압축 + 같은 속도 되돌림) + 롤 압연 실험 (나노 XCT 41 nm 균열 관찰 · 마이크로 XCT).
쪽 = 학술지 쪽 'e202300371 (n of 10)' 의 n · SI 쪽 = SI PDF 쪽 · 판독 원자료 = `litdb/figures/xu2023_dem_bonded_particle_fracture_calendering/digitized.csv` (112 행) · 고른 의도 = 조건 R7 'bonded-particle 입자파괴 모델 (>120 MPa → bond 파단 >10 %) · 우리 Auerbach / f_intact 의 문헌 대응물' (he2026 L690) → 의도 대조 결과 **일부** (모델은 있다 · '120 MPa · 10 %' 는 고른 입자 하나의 추측 기준 · f_intact (파괴 → 전도) 대응은 없다 · 카드 §0-1).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — SE 가 없는 액체 LIB 양극 (NMC111 : C65 : PVdF 96 : 2 : 2).  전극 기공 값 (표 1 · 그림 4a · S2f) 은 '랩 표준과 다른 문헌 값' 으로 카드 §7-2 에만 둔다 (같은 줄에 두지 않음).

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
- [b] xu2023_dem_bonded_particle_fracture_calendering | 모의: 위판을 압축과 같은 속도 (0.01 m/s) 로 처음 자리까지 되돌림 · 되돌아옴 정도 = h₂/h₁ × 100 % (h₁ = 압축 변위 · h₂ = 되돌아온 높이 · 그림 S4a 안 글자 *"h₁: compressed thickness"* · *"h₂: spring back thickness"*) · 최대 압력 12.5 · 40.0 · 80.0 · 120.0 · 157.7 MPa → 31.2 · 37.7 · 36.3 · 33.0 · 32.6 % | 카드 §3-9 · 원문 p.5–7 · SI 그림 S4b | 판독 (눈금 직선 맞춤) | 액체 LIB · 탄성 헤르츠 접촉 (되돌아옴 = 탄성 회복 — 원문 *"fast elastic recovery of the electrode as reported in the literature."*[58]) · 실험 되돌아옴 측정 없음
- [b] xu2023_… | 40 % 런 (그림 4b): 판 하중이 0 이 되는 압축도 ≈26–27 % → 되돌아옴 ≈13 %p = 변위의 ≈33 % · 기공률 최대 압력 26.72 % ↔ 이완 뒤 29.12 % (p.7) · 이완 중 결합 끊김 = 전체 끊김의 3 % (p.7) | 카드 §3-7 · §3-9 | 판독 · 인쇄 | ⚠ 같은 런의 압축도 · 기공률 · 되돌아옴이 고체 부피 보존으로 서로 맞지 않는다 (40 % 압축이면 16.7 % 여야 할 최대 압력 기공이 26.72 % · 이완 두께 증가 +3.4 % ↔ 되돌아옴이 뜻하는 +21.7 % [카드 산술 · 처음 기공 50.0 % 판독]) — 기준 높이 · 부피 정의 [미확인]
- [b] xu2023_… | 원문 추세 *"In general, the higher the maximum applied pressure, the lower the spring back degree"* · 첫 점 (10 %) 예외 = *"the pressure applied to the electrode is not high enough to reach the elastic conditions, and the microstructure evolution is mostly governed by particle rearrangement"* | p.7 | 인쇄 | 모델 값 · 다섯 런뿐

## c — 항복 · 경도 · 크리프 값과 정의
이 배치에 없음 — 재료 항복 · 경도 · 크리프 값이 없다.  가장 가까운 것: 결합 강도 σ_B^n 0.1 · σ_B^t 0.038 GPa (SI 표 3 · 모델 매개변수 · 보정 안 됨 · 매개변수 연구 그림 S3 의 'Sigma value' 0.1–1.0 ×10⁶ 은 단위 · 조건 미인쇄) · 결합 최대 응력 = 보 이론 식 (6)–(7) — 일축 항복 세기와의 환산 없음 (카드 §0-2 · §3-10).

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — AM (E_p 5 GPa) + CBD 구 (E 2 GPa · 1.16 µm) 를 함께 누르지만 상별 하중 몫 · 재밍은 보고하지 않는다.  위치별 손상 (집전체 쪽 입자가 10 MPa 아래부터 끊김 · 원문 해석 *"This could be attributed to its proximity to the current collector, which limited its ability to undergo corresponding displacement and rotation in the electrode’s self-organization process in response to pressure."* p.8 · 그림 S6) 은 하중 몫이 아니라 위치 효과다.

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] xu2023_… | 이 논문의 법칙 = 헤르츠 탄성 법선 + 누적 접선 변위의 쿨롱 상한 + 점성 감쇠 (식 1–2) · SJKR 점착 F_C = −c_CED A_COH n (식 3) · 큰 변형 대안으로 소성 접촉 법칙 (MDR · EEPA · Thornton–Ning) 을 쓰지 않고 **입자를 1 차 구 응집체 + 끊어지는 결합 (BPM)** 으로 바꿔 입자 변형 · 파단을 대리 · 맞춘 값 = 입자 E_p (+ Po_p) 하나 (*"straightforwardly calibrated by fitting the maximum pressure"* p.4 → NMC E 5 GPa · ν 0.3) · 결합 강도는 맞추지 않음 | 카드 §0-2 · §4-2 · 원문 p.4–5 · SI 표 1–3 | 인쇄 | 깨지는 범위 (겹침 · 상대밀도 상한) 수치 없음 · 고압 기공이 실험보다 높다는 결과로만 한계를 말함 (k 첫 줄)
- [e] xu2023_… | 결합 법칙: 법선 / 접선 힘 증분 ΔF = (E_b A_b / l_b) v_r Δt · ((E_b/2(1 + Po_b)) A_b / l_b) v_r Δt (식 4–5) · 최대 응력 σ_B^n = −\|F_B^n\|/A_b + \|M_B^t\| R_min/I · σ_B^t = \|F_B^t\|/A_b + \|M_B^n\| R_min/J (식 6–7 · 첫 항 음수 부호 인쇄 그대로) · 끊김 = σ_B^n ≥ σ_B^cn 또는 σ_B^t ≥ σ_B^ct · 결합 감쇠 없음 · 처음 맞닿은 쌍에만 생성 | 카드 §0-2 · §4-3 | 인쇄 | ⚠ 원문 안 어긋남: 본문 '결합 E · Po = 입자 값' ↔ SI 표 3 결합 E 10 GPa (입자 5) · 본문 'σ_cn = σ_ct' ↔ 0.1 ≠ 0.038 GPa · A_b · l_b · 모멘트 증분식 [미확인]

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 없음 — MPM 없음.

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
이 배치에 없음 — 계산 · 측정 모두 3D (2D 는 단면 표시뿐) · 2D → 3D 전이 진술 없음.

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
- [h] xu2023_… | 넘김 없음 — *"In the future, the microstructures obtained from the model will be used in a finite element method simulator"* (p.8) · 앞 단계 넘김 = LAMMPS CGMD 건조 결과 → LIGGGHTS 압연 (*"The initial electrode microstructure for calendering was derived from the simulation result of drying in our previous work[44]"* p.4 · 같은 1 차 구 응집체 · 처음 맞닿은 쌍에 결합) | 카드 §0-2 · §4-2 | 인쇄 | DEM → FE · MPM 넘김이 아니라 CGMD → DEM

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 — SE 없는 액체 LIB 양극 (참고: 표 1 0 · 80 · 150 MPa → 47.97 · 27.75 · 25.17 % · 압연 뒤 · 두께는 집전체 포함으로 읽어야 세 열이 맞는다 [카드 추론 · 카드 §3-2] — 랩 표준과 다른 문헌 값).

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] xu2023_… | 같은 런의 기공률 · 압축도 · 되돌아옴이 고체 부피 보존 하나로 맞지 않는다 → 이 논문의 세 숫자를 섞어 인용하지 않는다 · 우리 보고 표에 항등식 검사 줄 | 카드 §3-9 · §11-7 | 카드 산술 | 기준 높이 · 부피 정의 · h₂ 측정법 [미확인]
- [j] xu2023_… | 압력 세 벌: 본문 14.2 · 50.3 · 98.7 · 157.7 MPa (10–40 %) ↔ 그림 3 캡션 9.2 · 20.1 · 50.9 · 146.8 MPa · 그림 4a 실험 점 (80 MPa 28.6 % · 120 MPa 27.8 % [판독]) ↔ 표 1 (80 MPa 27.75 % · 120 MPa 줄 없음) | 카드 §3-5 · §3-6 · §3-11 | 인쇄 · 판독 | —
- [j] xu2023_… | 실험 압력 = 롤 간격 · 두께 공식 (계산값 · 공식 미인쇄) · 실험 기공 = 압연 뒤만 (*"it is difficult to obtain in operando the mechanical behavior of particles under each pressure"* p.4) · 롤 (실험) ↔ 평판 (모의) | 카드 §3-1 · §4-1 | 인쇄 | —
- [j] xu2023_… | 결합 강도 미보정 · '10 %' 기준 = 입자 하나 추측 · *"These observations are qualitative"* (p.8) | 카드 §0-1 · §3-10 · §11-1 · 11-2 | 인쇄 | —

## k — DEM 의 한계 (원문 문장 · 인용 서지 = Xu · Paredes-Goyes · Su · Scheel · Weitkamp · Demortière · Franco 2023, Batteries & Supercaps 6, e202300371)
- [k] xu2023_… (Xu 외 2023 · Batteries & Supercaps 6, e202300371) | 탄성 접촉이 소성을 못 잡아 고압 기공률이 실험보다 높다: *"This may be due to the inability of the simulation to capture the plastic behavior exhibited by the electrode during this process since we use an elastic contact model."* (p.7 · 157.7 MPa 런 29.12 % ↔ 실험 25.16 %) · 80 MPa 에서는 +9.5 %p [판독] | 카드 §0 · §3-6 · §4-4 | 인쇄 · 판독 | 액체 LIB · 우리 SE 와 다른 상
- [k] xu2023_… (Xu 외 2023) | 1 차 입자 구 = 조대화 (모양 · 크기가 실제와 다름): *"Although the real primary particle crystal shape is not spherical and the size is smaller than the primary particle size within the model, here, we perform a coarse-grained simulation with primary spherical particles of 1.59 μm diameter to simulate the AM mechanical behavior against the strain."* (p.5) | 카드 §4-4 | 인쇄 | —
- [k] xu2023_… (Xu 외 2023) | 구 겹침이 기공 연산자 오차를 키운다: *"The difference comes from the overlapping appearing after the calendering between the primary particles of AM, resulting in a higher simulation error under high calendering pressures."* (p.5–6 · 이론 부피 ↔ 메시 기공 차 0.1 → 2.7 %p [판독]) | 카드 §3-6 | 인쇄 · 판독 | —
- [k] xu2023_… (Xu 외 2023) | 모델 해상도 아래의 파괴는 못 본다: *"Since the nano-fracture we observe is smaller than the scale of our model, we are not able to observe the fracture of the secondary particle from the simulation results."* (p.7) · *"due to the scale limitation, we cannot observe the fracture and the reintegration of the material due to the binder after the fracture generation"* (p.8) | 카드 §4-4 | 인쇄 | 1 차 구 1.59 µm = 나노 XCT 복셀 41 nm 의 39 배 [카드 산술]
- [k] xu2023_… (Xu 외 2023) | 결합만으로 응집체가 서지 않는다: *"the addition of cohesion (SJKR) between primary particles in our simulations was required to ensure the stability of the secondary particle. This limitation will be further investigated in future work."* (p.4) | 카드 §0-2 · §11-10 | 인쇄 | —
- [k] xu2023_… (Xu 외 2023) | 보정값이 물성이 아니라는 고백: **말 없음** — E_p 5 GPa 를 최대 압력에 맞췄다고만 적고 (p.4) 같은 그룹 앞 논문의 NMC E 135 GPa (`xu2023_realistic_am_shape_cgmd_calendering`) · 200 GPa (`ngandjong2021_dem_calendering_digital_twin`) 와의 차 (1/27–1/40 [카드 산술]) 는 말하지 않는다 | 카드 §3-4 · §7-4 | 카드 산술 | —

## l — 소성변형이 왜 어려운가 · 우회 · 비용 (인용 서지 = Xu 외 2023, Batteries & Supercaps 6, e202300371)
- [l] xu2023_… (Xu 외 2023) | 어려운 이유의 설명: **말 없음** — 소성을 넣지 않았다는 사실과 그 결과 (기공률이 높다 · k 첫 줄) 만 적는다 · 입자 '변형' 은 결합으로 묶인 1 차 구의 재배열 · 결합 끊김으로 대리 (*"a slight deformation of the particle"* p.7) · 결론의 관찰 *"With the increase of the pressure and the decrease of the electrode porosity, the source of the microstructural change in the electrode changes from the movement of particles to the deformation and fracture of particles."* (p.8) | 카드 §4-4 (ii) | 인쇄 | 모델 안의 '변형' = 응집체 모양 변화 (입자 소성 아님)
- [l] xu2023_… (Xu 외 2023) | 우회와 값: 입자 E_p 를 최대 압력 하나에 맞춤 (5 GPa · ν 0.3 · SI 표 1) · 결합 강도 = 매개변수 연구 (그림 S3) 만 · 검증 = 압력–기공률 (실험 3–4 점) + 나노 XCT 정성 (80 MPa 온전 · 150 MPa 균열) · 비용 = 런당 2–9 일 × 28 코어 (Xeon E5-2680 v4 · 1 노드 · 128 GB · p.5) · Δt 0.01 ns (*"around 1.5% of Rayleigh time"* — 가정 밀도 4.65 g/cm³ 로는 0.24 % [카드 산술]) · 입자 수 미기재 (결합 ≈38,470 [판독 그림 S8]) | 카드 §0-2 · §3-4 · §4-2 | 인쇄 · 판독 · 카드 산술 | 맞춘 값 하나지만 결합 강도 · A_b 는 정해지지 않은 채

## m — 받아들일 통찰
- [m] xu2023_… | 무엇을: **R7 보고에 위치 · 크기별 손상 나눔** — Auerbach 등급 수를 z 세 겹 (집전체 쪽 · 가운데 · 위) 과 입자 크기 계급으로 나눠 싣는다 · 우리 쪽 어디에: R7 · 결과 전 대조 항목 (방향 · 꼴만: 이 모델은 집전체 쪽 −17.3 % > 위 −9.8 % > 가운데 −7.5 % [판독 · 카드 산술]) · 왜: 그림 S8 · S5 · S6 · S7 (같은 40 % 압축에서 입자 위치로 9 ↔ 46 % 끊김)
- [m] xu2023_… | 무엇을: **탈압 보고 꼴 + 항등식 검사** — 최대 압력 기공 · 이완 뒤 기공 · 변위 대비 되돌아옴 (h₂/h₁) · 이완 중 손상 몫을 따로 싣고 고체 부피 보존 t/t₀ = (1 − ε₀)/(1 − ε) 로 서로 대조하는 줄을 결과 표에 · 우리 쪽 어디에: 단계 6 · 단계 0 · R4 · 왜: 이 논문은 넷을 다 냈지만 서로 맞지 않는다 (카드 §3-9)
- [m] xu2023_… | 함정: **'파괴 기준' 을 입자 하나 + 정성 영상으로 정하지 않는다** — 같은 '끊긴 결합 10 %' 가 입자 하나 ≈122 MPa · 전극 전체 ≈144 MPa [판독] · 우리 쪽 어디에: R7 (Auerbach K_IC 0.3 도 옛 출처 실재 미확인 — `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem` §0 · 같은 함정) · 왜: 원문 p.8 *"we can speculate"* · 카드 §0-1
- [m] xu2023_… | 함정: **두 기공 연산자를 함께 보고** (겹침으로 차가 압력과 함께 0.1 → 2.7 %p) · 우리 쪽 어디에: 단계 0 (ε_sphere ↔ ε_union 등록에 압력별 차 칸) · 왜: 그림 4a · p.5–6

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드 없음 · papers/ ls + grep 확인)
- [n] D. O. Potyondy, P. A. Cundall, Int. J. Rock Mech. Min. Sci. 2004, 41, 1329. (원문 목록 [51] 그대로 · 제목 미인쇄 — 서지 일부만) | 결합 입자 모델 (BPM) 의 원전 — 식 (6)–(7) · 파단 기준 · 'σ_cn = σ_ct' 조건의 출처 · e · l · R7 (원문 p.4 *"[51]"*) | litdb 확인: papers/ 에 potyondy* 없음 · 'Potyondy' grep = 다른 카드 9 장에서 인용만 · '1329' grep 4 장 (다른 문맥)
- [n] M. Schramm, M. Z. Tekeste, C. Plouffe, D. Harby, Biosyst. Eng. 2019, 186, 349. (원문 목록 [56] — 제목 미인쇄) | 이 논문이 쓴 LIGGGHTS BPM 수정판 — 우리 LIGGGHTS 덱에 결합 (R7 · 응집체 AM) 을 넣는 경로 · e · l | litdb 확인: papers/ 에 schramm* 없음 · 'Schramm' · 'Biosyst' grep 0
- [n] Y. Guo, J. Curtis, C. Wassgren, W. Ketterhagen, B. Hancock, AIP Conf. Proc. 2013, 1542, 491. (원문 목록 [52] — 제목 미인쇄) | 결합 힘 · 모멘트 증분식 (모멘트 식은 이 논문에 인쇄 없음 · *"Similar expressions can be found in Ref. [52]"* p.4) · e | litdb 확인: papers/ 에 guo2013* 없음 · '1542, 491' · 'Wassgren' grep 0
- [n] A. Lundkvist, P.-L. Larsson, E. Olsson, Powder Technol. 2023, 425, 118574. (원문 목록 [36] — 제목 미인쇄) | 원문 서론: *"developed a method to simulate the electrode creation and calendering with DEM, which is able to capture the unloaded stiffness behavior induced by the viscoelastic binder"* (p.2) — 하중 뺀 뒤 강성 · b · e · 단계 6 | litdb 확인: papers/ 에 lundkvist* 없음 · '118574' grep 0 · ⚠ wishlist L106 의 Lundkvist 2024 (Powder Technol. 443, 119873) 와 다른 논문
- [n] R. Sim, S. Lee, W. Li, A. Manthiram, ACS Appl. Mater. Interfaces 2021, 13, 42898. (원문 목록 [13] — 제목 미인쇄) | 원문 서론: *"reported the cracking and fusion in high-nickel cathode materials during calendering by using scanning electron microscopy"* (p.1) · 파괴 뒤 바인더에 의한 재결합 (p.8) — R7 실험 쪽 · j | litdb 확인: papers/ 에 sim2021* 없음 · '42898' grep 0
- (참고 · 후보로 세지 않음 · 이미 `wishlist.md` 에 있음) [15] Huttner 외 2021 (J. Electrochem. Soc. 168, 090539 · L57) · [31] Ge 외 2022 (Powder Technol. 403, 117366 · L242) · [32] Ge 외 2023 (Chem. Eng. J. 465, 142749 · L326).
- (참고 · 카드 있음) [11] `lu2020_insitu_nanoct_calendering_microstructural_evolution` · [27] `sangros2019_dem_calendering_lib_electrode` · [41] `ngandjong2021_dem_calendering_digital_twin` · [44] `xu2023_realistic_am_shape_cgmd_calendering` · [58] `diener2022_roll_gap_springback_calendering`.

## 카드 문제
- `he2026_dem_calendering_inhomogeneity_areal_density` **L690**: 서지 *"Xu 2023 (*Batteries & Supercaps* 6, e202300525)"* ↔ 원문 첫 쪽 · 모든 쪽 머리글 · PDF 메타 = **e202300371** (DOI 10.1002/batt.202300371).  he2026 카드에 참고문헌 목록이 없어 오기가 he2026 원문의 것인지 카드의 것인지 [미확인] — he2026 원문 목록과 대조 필요 (그 카드는 고치지 않고 관련 카드 한 줄만 더했다).  후보 표 `S8_candidates.md` N-70 행도 같은 번호를 옮겼다.
- `he2026_dem_calendering_inhomogeneity_areal_density` **L499 · L690**: *"(bonded-particle, >120 MPa 에서 bond 파단 >10 %)"* · *"(>120 MPa → bond 파단 >10 %)"* — 숫자 120 · 10 은 원문과 같지만 정의가 빠졌다: 원문은 **고른 2 차 입자 하나** (11.96 µm · 결합 1748) 에 대한 **추측 기준** (*"we can speculate … approximately above 10%, i.e., … approximately above 120 MPa"* p.8) 이고, 전극 전체로는 50 · 100 · 150 MPa 에서 1.8 · 4.5 · 11.1 % 끊겨 10 % 를 ≈144 MPa 에서 넘는다 [판독] → '압력 문턱 규칙' 으로 인용하지 않는다.
- (지시서 메모) "2 차 입자 형상의 출처 (나노 단층 촬영)" — 원문 = **마이크로** XCT (PETRA III P05 · 화소 0.64 µm · p.4) · 나노 XCT (SOLEIL ANATOMIX · 41 nm) 는 압연 전 · 80 · 150 MPa 전극의 균열 관찰에만.
- (갱신 후보 · 오류 아님) `xu2023_realistic_am_shape_cgmd_calendering` 🔗 자매 논문 (a): *"계보 5 편 … 중 MPa 축을 가진 것은 Ngandjong 2021 하나뿐이고, 그것으로 확정이다"* — 그 5 편 안에서는 맞지만, 이 논문 (같은 BPN250 · 0.54 m/min · 60 °C) 이 실험 80 · 150 MPa · 모의 0–157.7 MPa 를 보고한다 (그 카드에는 관련 카드 한 줄만 더했다 · 문장은 고치지 않음).
- 확인한 다른 2 차 인용: `wet_processing_resolved_am_ssb_cathode_manufacturing` L45 · L239 · L477 (ref [38] Xu, Paredes-Goyes 2023 = 압연 중 입자 fracture 예측 모델 · LIB) = 원문과 같다 (숫자 없음).

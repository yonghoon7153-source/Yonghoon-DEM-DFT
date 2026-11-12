# 배치 46 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-12)

카드 = `jeong2024_operando_densification_chemomechanics_se_size_composite_cathode` (원문 = 출판본 8 쪽 + SI 9 쪽 · 그림 크롭 54 장 = 도구 13 (다시 자름 3) +
손 크롭 41 (SI 표 1 · 패널 17 · 식 10 · 근거 문단 13) · 판독 원자료 `litdb/figures/<slug>/digitized.csv` 383 행).
서지 (k · l 인용용) = Jeong M.-G., Naik K. G., Zheng Y., Suk W. J., Vishnugopi B. S., Lin L., Puthusseri D., Chuang A. C., Okasinski J. S., Sakamoto J.,
Mukherjee P. P., Hatzell K. B., *Operando Investigation on the Role of Densification and Chemo-Mechanics on Solid-State Cathodes*, Adv. Energy Mater. 14 (23) 2304544 (2024),
DOI 10.1002/aenm.202304544.
⚠ 재료 = NCM811 + Li₆PS₅Cl (NEI) + Super P 70 : 27.5 : 2.5 wt% — 계는 우리와 같지만 **상태 (무하중 분할) · 조성 · 입경**이 다르다 · DEM · 압밀 시뮬레이션 없음.
쪽 = 본문 인쇄 쪽 "(n of 8)" = PDF 쪽 · SI 는 SI PDF 쪽.

---

## a — 순수 SE 압력별 기공 곡선 · 진밀도 · 상태

- [a] jeong2024_operando_densification_chemomechanics_se_size_composite_cathode | **없음** — 순수 SE 펠릿의 기공 · 밀도가 없다 (SE 층 125 mg cm⁻² · EDXRD 분리막 40 mg 손 가압은 밀도 미기재) · 진밀도 (LPSCl · NCM811) 미인쇄 | 카드 §3-1 · §13 · 원문 p.7 | [미확인] | 복합 양극만

## b — 압력을 뺄 때 되돌아오는 양 · 잰 방법

- [b] jeong2024_operando_densification_chemomechanics_se_size_composite_cathode | **없음** — 재압축 시험은 올리는 가지 (5→500 MPa) 만 · 내리는 곡선 · 회복량 · 시편 두께 없음.  XCT 는 "(without pressure)" 한 상태이고 그 무하중 기공 차가 400 MPa 아래 적층압에서 *"is expected to remain effective"* 라는 가정만 있다 | 카드 §3-3 · §4-4 · 원문 p.3–4 · p.7 | [인쇄] (가정 문장) | 탈압 회복은 [미확인]

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- [c] jeong2024_operando_densification_chemomechanics_se_size_composite_cathode | **항복 · 경도 · 크리프 없음** — 모델 입력 탄성만: E_SE 22 GPa · ν_SE 0.27 (K 15.9 · G 8.7 GPa [카드 산술]) · E_AM 200 GPa · ν_AM 0.3 (출처 Naik 2023 ESM 55, 312) · 압축 곡선은 *"we did not use or interpret the data to calculate the intrinsic mechanical properties … (e.g. Young's modulus)"* | 카드 §3-3 · §3-7 · SI p.8 표 S3 · 원문 p.3 | [인쇄] | 탄성 입력 · 인용값 (측정 아님) · 우리 DFT ν 0.360 · B₀ 26.23 과 ν · K 다름

## d — 단단한 입자 + 무른 입자 혼합 압축의 하중 몫 · 재밍

- [d] jeong2024_operando_densification_chemomechanics_se_size_composite_cathode | 하중 몫 자료 **없음** — 대신 복합 (NCM811 70 wt%) 재압축 순응: 370 MPa 선가압 뒤 5→400 MPa 변위 **L ≈103 · S ≈34 µm (≈3.0 배)** · 400→≈495 MPa ≈14 · ≈12 µm · S 기울기 ≤370 MPa ≈41–61 → 370–400 ≈17 → 400–435 ≈10 MPa µm⁻¹ (물러짐) · L ≈6.5–8.6 (뚜렷한 꺾임 없음) · 저자 해석 "기공 = 강성 0" | 카드 §3-3 · Fig. 2c | [판독] + [카드 산술] | S 곡선은 저자가 끝점을 L 에 맞춰 옮김 · 시편 높이 미인쇄 (h ≈1 mm 는 변형률 속도에서 역산 [카드 산술 · 가정])

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위 · 대안

- 이 배치에 없음 (접촉 법칙 · DEM 없음 — 모델은 상 연속체 선형 탄성)

## f — MPM 접촉 · 다물체 · 강체 결합 · 해상도 규칙

- 이 배치에 없음 (MPM 없음).  해상도 쪽 참고 한 줄: XCT 복셀 0.92 µm ≈ SE 1 µm (지름당 ≈1 칸) 이라 작은 SE 사이 기공 · 접촉은 풀리지 않는다 — 원문은 해상도 한계를 말하지 않음 (카드 §3-2 · §11-2 [카드 해석])

## g — 2D 결과를 3D 로 옮길 때의 경고 · 증거

- 이 배치에 없음 (XCT 3D · 모델은 3D 장의 z 단면 세 장으로 읽힘 [카드 해석] · 2D↔3D 말 없음)

## h — DEM 에서 FE · MPM 으로 넘긴 선례 · 시점

- 이 배치에 없음 (DEM 없음).  인접: XCT 대표 부피 100³ µm³ → 모의 (*"selected … for subsequent visualization and simulation"* p.7) 지만 모델 영역 (≈60 / ≈65 µm · 두 상만) 과의 관계 · 넘김 규칙 [미확인] (카드 §3-7)

## i — 복합 양극 (AM + SE) 의 압력별 기공

- [i] jeong2024_operando_densification_chemomechanics_se_size_composite_cathode | **무하중 XCT 분할 기공 (한 압력 상태): SE ≈1 µm 0.11 · 3–5 µm 0.16** (NCM811 : LPSCl : Super P = 70 : 27.5 : 2.5 wt% · 복셀 0.92 µm · 임계 + top-hat + watershed) — 같은 논문에 L **0.18** (결론) · p.4 뒤바뀐 문장 (S 16 · L 11) · 모델 대표 부피 0.0926 / 0.1588 · Fig. 2b 두께 방향 10 점 평균 0.109 / 0.163 | 카드 §3-2 · 원문 p.3 · p.4 · p.6 · p.7 · SI p.7 | [인쇄] · [판독] | **압력별 아님** (XCT 시편 성형압 미인쇄 · 같은 조성 전기화학 셀 370 MPa) · 진밀도 분모 없음 · 1 µm SE = 복셀 1 개
- [i] jeong2024_operando_densification_chemomechanics_se_size_composite_cathode | **'임계압 ≈400 MPa'** = 재압축 곡선 수렴점 · *"It is likely that when the applied pressure is greater than the 'critical pressure' of 400 MPa, where the porosity is minimized, the pressure-induced elastic and plastic deformation can mechanically close the pores … to reach nearly 100% relative density"* | 카드 §3-3 · 원문 p.3 | [인쇄] (가설) | 400 MPa 위 기공 측정 없음 · 선가압 370 MPa 바로 위 [카드 해석] · 다른 카드 (lee2025 순수 LPSCl 97 % TD 에 650 MPa · miss2026 NMC622 400 MPa ε ≈0.14) 와 맞지 않을 수 있음
- [i] jeong2024_operando_densification_chemomechanics_se_size_composite_cathode | 기공 크기: L 은 r < 2 µm (≥19 900 / 14 000) · 6–12 µm 기공이 많고 S 는 2–6 µm 가 많다 · Σ n r³ 비 L/S 1.50 = 기공 비 1.50 · r ≥ 6 µm 가 부피의 ≈82 % (L) · ≈61 % (S) → L 의 추가 기공은 큰 빈 곳 | 카드 §3-2 · SI Fig. 2a | [판독] + [카드 산술 · 가정: 구 · 같은 분석 부피] | 분석 부피 [미확인]
- [i] jeong2024_operando_densification_chemomechanics_se_size_composite_cathode | 이론 부피비 0.58 : 0.42 (기공 제외) 는 70 : 27.5 wt% 와 정본 카드 진밀도 (NCM811 4.74–4.80 · LPSCl 1.64 랩 표준 / 1.87) 로 재현 안 됨 — 필요 ρ_SE/ρ_NCM = 0.54 (ρ_SE ≈2.6) · 1.64 · 4.77 이면 ≈0.47 : 0.53 | 카드 §3-1 · 원문 p.7 | [카드 산술 · 다른 카드 밀도] | 원문 진밀도 미인쇄 → 분할비 검증 문장 확인 불가

## j — 카드가 스스로 적은 한계 (가압 · 탈압 계산과 닿는 것)

- [j] jeong2024_operando_densification_chemomechanics_se_size_composite_cathode | 저자: 압축 곡선 = *"only represents the compliance of the densified pellet"* (다이가 옆 팽창을 막아 영률 계산 안 함) · *"The impact of variable volume change on the mechanical and electrochemical properties … is not well understood"* · 리튬화 기울기가 *"does not fully explain the stable capacity retention in LPSC-S"* | 카드 §3-8 · 원문 p.3 · p.5 | [인쇄] |
- [j] jeong2024_operando_densification_chemomechanics_se_size_composite_cathode | 카드: 압력별 기공 · 탈압 없음 · 모델 = 선형 탄성 (압밀 · 소성 · 접촉 · 박리 · 공극 처리 없음 / 미기재) · 영역 60–65 µm (실측 두께 ≈110–140 µm 의 절반) · 격자 · 경계조건 · Ω [미확인] · 세 시편 (XCT · 6 mm 압축 · 10 mm 셀 · 6 mm EDXRD 28 mg cm⁻²) 조건이 다름 | 카드 §11 · §13 | [카드 해석] |

## k — DEM 의 한계 (원문 문장 · 위치)

- [k] jeong2024_operando_densification_chemomechanics_se_size_composite_cathode (Jeong 외 2024 · Adv. Energy Mater. 14, 2304544) | **말 없음** — 본문 · SI 에 DEM · discrete · particle simulation 낱말 0 회 · DEM 을 쓰지 않음 | 카드 §4-4 · 원문 대조 기록 | [인쇄 전수] |

## l — 소성변형이 왜 어려운가 · 우회 · 값

- [l] jeong2024_operando_densification_chemomechanics_se_size_composite_cathode (Jeong 외 2024 · Adv. Energy Mater. 14, 2304544) | 실험 해석에서만 소성을 부름: *"the pressure-induced elastic and plastic deformation can mechanically close the pores in composite structures to reach nearly 100% relative density"* (p.3 · 가설) · 모델은 *"mechanics is modeled based on linear elasticity"* (SI p.5) + 등방 확산 변형 ĉΩ/3 · 무응력 기준 = 완전 탈리튬 — **소성 · 압밀 단계를 넣지 않았고 이유도 적지 않음** · 계산 비용 · 격자 [미확인] | 카드 §4-4 · §3-7 · SI 식 (8) · (9) | [인쇄] | 우회 = 압밀을 빼고 정해진 미세구조 위 탄성 응력만 (맞춘 값 0 · 물성은 Naik 2023 인용)

## m — 받아들일 통찰

- [m] **선가압 이력 검사** — 무엇을: 370 MPa 선가압 → 재압축 곡선의 꺾임 (작은 SE 370–400 MPa) 이 선행 압밀압에서 나는지 우리 MPM / DEM 침대 (같은 이력: 370 → 내림 → 500 MPa) 로 시험 · 어디: 단계 6 · 조건 R3 · R4 · 후보 A · A′ · M0 · 왜: 문헌 "임계압 ≈400 MPa" 가 재료값인지 이력 표지인지 원문이 가르지 않음 (카드 §3-3 · Fig. 2c [판독])
- [m] **기공 인용 꼬리표 규칙** — 무엇을: 문헌 기공을 받을 때 연산자 (분할 / 질량 / 구 부피) · 상태 (가압 중 / 무하중) · 해상도 (복셀 ↔ 입경) · 같은 논문 안 판본 (11 · 16 · 18 % · 뒤바뀜) 을 함께 등록 · 어디: 단계 0 · 결과 전 대조 항목 · 왜: 이 한 편 안에서 같은 시료 기공이 다섯 값으로 흩어지고 2 차 인용 (li2026 · lei2026) 이 꼬리표 없이 옮김 (카드 §0-1 · §3-2)
- [m] **SE 입경 방향 대조 점** — 무엇을: 70 wt% NCM811 에서 SE ≈1 vs 3–5 µm → 무하중 기공 11 vs 16 % 를 우리 DEM 입경 뒤집힘 (AM 62 ↔ 82 wt%) 구간 안의 **방향** 대조 점으로 · 어디: 단계 5 · 후보 D0 · 결과 전 대조 항목 · 왜: 우리 DEM 의 AM 많은 쪽 방향 (큰 SE → 기공 ↑) 과 같음 · 절대값은 상태 · 연산자 차로 대조 불가 (카드 §7-1 · §7-2)
- [m] **τ 이름 (흐름 밖: J 절 · 수송 보고)** — 무엇을: 식 (6) k_eff = k ε/τ 의 τ 는 우리 tau2 (수송 tortuosity) 자리 · 같은 SI 의 "Tortuosity Measurements" 는 다른 숫자 · 방법 미상 → 한 표에 섞지 않음 · 어디: 흐름 밖: 수송 tortuosity 보고 · 왜: 같은 이름 두 벌 (카드 §3-7 · §7-4)

## n — 논문 에이전트 후보 (이 카드가 인용 · 언급했지만 litdb 에 카드가 없는 것)

- [n] A. Bielefeld, D. A. Weber, R. Rueß, V. Glavas, J. Janek, J. Electrochem. Soc. 2022, 169, 020539. (서지 일부만 — 제목 원문 목록에 없음) | i · j — "기공의 크기 · 분포가 복합 양극 가역 운전에 주는 영향 (void overpotential)" 의 이론 인용처 (원문 p.2 [12]) · 카드 §12 | litdb 확인: `ls bielefeld*` = bielefeld2019 · bielefeld2020 (다른 논문) · "020539" grep = kim2024_optimal · lee2024_shear (인용만) → 카드 없음
- [n] P. Perrenot, P. Bayle-Guillemaud, C. Villevieille, ACS Energy Lett. 2023, 8, 4531 (서지 일부만 — 제목 없음) | i · l — 입경 → 치밀화 기전 · 사이클 중 기공 증가의 인용처 (원문 p.2 [17]) · 카드 §12 | litdb 확인: `ls perrenot*` 없음 · "4531" grep = stavola2023 (인용만) → 카드 없음
- [n] P. Perrenot, A. Fauchier-Magnan, M. Mirolo, L. Lecarme, P.-H. Jouneau, A. Boulineau, P. Bayle-Guillemaud, C. Villevieille, Adv. Funct. Mater. 2023, 34, 2310739. (서지 일부만 — 제목 없음) | i · l — "densification mechanisms[17,20]" (원문 p.2 [20]) · 카드 §12 | litdb 확인: "2310739" grep = thompson2026 (인용만) → 카드 없음
- [n] Naik, K. G.; Vishnugopi, B. S.; Mukherjee, P. P. Kinetics or transport: whither goes the solid-state battery cathode? ACS Applied Materials & Interfaces 2022, 14, 29754–29765. | m · 수송 (J 절) — 모델 식 (6) τ · 활성 면적의 직접 수치 모사 방법 (SI ref 1) = 이 τ 가 tau2 꼴인지 확정할 원전 · 카드 §12 | litdb 확인: `ls naik*` 없음 · "29754" grep = stavola2023 (인용만) → 카드 없음
- [n] Naik, K. G.; Vishnugopi, B. S.; Mukherjee, P. P. Heterogeneities affect solid-state battery cathode dynamics. Energy Storage Materials 2023, 55, 312–321. | c — 모델 물성 (E_SE 22 GPa · ν_SE 0.27 · E_AM 200 GPa · k₀ 0.04 S m⁻¹ · D_s · k_r) 의 출처 (SI ref 3 · 표 S3) · 카드 §12 | litdb 확인: `ls naik*` 없음 · 제목 grep 0 건 → 카드 없음

## 카드 문제

1. `li2026_electrochemomechanical_coupling_asslmb_review` L72 — *"임계압 ≈400 MPa 위에서 두 전극 응답 비슷 (공극 붕괴)"* 의 "(공극 붕괴)" 는 원문의 가설 (*"It is likely … can mechanically close the pores"*) 을 사실로 옮긴 것.  L153 · L72 는 기공 11 · 16 % 를 측정 상태 (무하중 · 분할 · 복셀 0.92 µm) · 같은 논문의 18 % 판본 없이 옮김.
2. `lei2026_se_particle_size_effects_review` L128 · L251 — SE 입경 "LPSC-S (< 1 µm)" · "SE < 1 vs 3–5 µm" ↔ 원문 "≈1 μm" (p.2) · "1 μm" (p.6 · p.7).  L128 의 *"큰 SE = 낮은 압력에서 불균일 부피 변화 · 변위 ↑"* 는 두 결과 (압축 순응 = Fig. 2c · 사이클 리튬화 기울기 = Fig. 4 · 5) 를 한 문장에 섞음.
3. `lei2026_se_particle_size_effects_review` L173 · L214 — "두께 0–60 µm × 시간 SOC 지도" 는 **모델 영역** (작은 SE 60 µm · 큰 SE ≈65 µm) · 실측 EDXRD 두께는 ≈110–140 µm — 카드에 모델 / 실측 구분 표지 없음.
4. 프롬프트가 가리킨 `lei2026_…` "L279" 는 그 카드의 정본 확인 줄 · Jeong 서지 줄은 L262 (줄 번호 차이 · 내용 문제 아님).
5. (원문 문제 — 카드 §3-8 에 기록) 기공 16 / 18 % · p.4 뒤바뀜 · tortuosity 두 벌 · 율속 % 정의 · SI 그림 번호 겹침 ("Figure S1" 두 그림) · SI 그림 4 "midpoint of discharge" ↔ 충전 중간 판독 · "red dashed line" 없음 · SI 그림 3 제목 4.75 Å ↔ 4.774 / 4.785 · 이론 부피비 재현 안 됨 · 캡션 결손 (Fig. 1 (e) · Fig. 3 (c) · Fig. 4 끊김).

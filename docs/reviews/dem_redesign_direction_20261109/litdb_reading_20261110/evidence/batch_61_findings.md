# 배치 61 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-12)

카드 = `korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens` (원문 = 출판본 10 쪽 + SI 14 쪽 · 그림 크롭 64 장 = 도구 20 (다시 자름 19) +
손 크롭 44 (패널 18 · 인라인 식 3 · 근거 문단 22 · 표 S1) · 판독 원자료 `litdb/figures/<slug>/digitized.csv` 56 행).
서지 (k · l 인용용) = Korjus O., Mitra S., Berrod Q., Vanpeene V., Appel M., Broche L., Lyonnard S., Villevieille C.,
*Investigating the densification of Li6PS5Cl solid electrolyte through multi-scale characterization techniques*, Energy Storage Mater. 82 (2025) 104589,
DOI 10.1016/j.ensm.2025.104589.
⚠ 재료 = 순수 Li₆PS₅Cl (NEI · 결정 ≈50 nm 의 응집체) — 복합 양극 없음 · DEM · MPM · 압밀 계산 없음.  쪽 = 인쇄 쪽 p.1–10 = PDF 쪽 · SI 는 SI PDF 쪽.

---

## a — 순수 SE 압력별 기공 곡선 · 진밀도 · 상태

- [a] korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens | 누른 채 (in situ) 기공 곡선 하나 — Fig S11: 12.12 (76.2) · 11.58 (127) · 10.21 (255) · 9.50 (382) · 8.61 % (510 MPa) · 300 MPa 보간 9.96 % · 방법 = ex situ 나노 CT 기공 9.5 vol % (382 MPa · 30 분 · 뺀 뒤 · 다른 펠릿) 앵커 + 두께 '선형' 환산 · 진밀도 분모 미사용 (원문 "crystallographic density remain constant" — 값 미인쇄) | 카드 §3-3 · Fig S11 · 원문 p.6 | [판독] (S11) · [인쇄] (9.5 %) | ⚠ 같은 논문 두께 (480 → 331 µm) + 저자 가정 (질량 · 결정밀도 · 면적 일정) 이면 34.9 → 5.7 % [카드 산술] · 앵커와 무관하게 ε₇₆ ≥ 31 % → S11 재현 안 됨 · 300 MPa: 10.0 (S11) ↔ 15.2 % (재계산 · 앵커 5–15 % 면 11.0–20.3 %)
- [a] korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens | 진밀도 분모: Table S1 격자 9.84369 (표기 'nm' · 실제 Å) · Z = 4 가정 → 결정밀도 1.869 g/cm³ — 원문이 쓰거나 인쇄한 값이 아니다 (랩 표준 1.64 와 다른 값) | 카드 §3-3 · §3-9 · SI p.9 | [카드 산술] | 이 논문의 기공은 밀도가 아니라 영상 분할
- [a] korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens | 나노 CT (382 MPa · 뺀 뒤): 기공 9.5 vol % · 중앙 기공 지름 479 nm · 기공 부피의 10 % 만 > 1 µm → *"if we were only estimating porosity from in situ μ-tomography, we would have biased results"* | 카드 §3-3 · §3-9 · 원문 p.6 | [인쇄] | ≈150 nm 미만 기공 제외 (복셀 50 nm · 분해능 ≈3 배)

## b — 압력을 뺄 때 되돌아오는 양 · 잰 방법

- [b] korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens | 510 → 76.2 MPa (기밀 유지 최소압 · 0 아님): σ *"mainly remained unchanged"* · 미세구조 '이완' — 큰 입자 분포 (30–55 µm) 넓어짐 · P2 · P3 감소 *"the “cold sintering” … is not a fixed state"* · **두께 · 되돌아옴 · 감압 기공 숫자 없음** | 카드 §3-6 · 원문 p.4–5 · Fig 2b · 3f · 3g | [인쇄] (정성) | 되돌아옴 측정 [미확인] · 언로딩 대조점 아님

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- [c] korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens | 항복 · 경도 · 크리프 없음.  카드가 두께로 낸 겉보기 다이 접선 dP/dε 0.81 → 0.84 → 1.35 → 3.15 GPa (76 → 510 MPa) · Heckel 꼴 P_y ≈ 232 MPa (앵커 9.5 % 재계산) · 128–340 MPa (앵커 5–15 %) · S11 그대로면 ≈1280 MPa | 카드 §3-3 · §7-1 | [카드 산술] (판독 두께) | 재료 E · 항복이 아니다 (분말층 전체 · 파쇄 포함) · 앵커 없이는 P_y 를 정하지 못한다 · 일축 항복 환산 없음

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

이 배치에 없음 (순수 SE).

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안

이 배치에 없음 (접촉 법칙 · DEM 없음).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙

이 배치에 없음 (MPM 없음).  (해상도 교훈은 m 의 첫 항목 — 측정 쪽.)

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거

- [g] korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens | 2D → 3D 진술 없음 · SEM (2D · 가루 한 장 · ≈450 입자) ↔ μ-CT (3D) PSD 는 *"corresponds well"* · < 10 µm 은 SEM 이 더 많다 — 원인을 해상도 (202 ↔ 600 nm 화소) 로 설명 | 카드 §4-4 (iii) · 원문 p.4 | [인쇄] | 차원보다 해상도 문제로 다룸

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공

이 배치에 없음 (순수 SE).

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것

- [j] korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens | 저자 한계: μ-CT 는 1.8 µm 미만 기공 · 입자를 못 봄 (→ 나노 CT 로 보완) · 분석 영역 1.77 mm² / 전체 38.5 mm² (압력이 오르면 ROI 로 더 많은 입자가 들어옴) · 회전 177° (프레스 기둥) · 나노 CT 50 nm 복셀 (빔 손상) · 가루에서 시작 못 함 (76.2 MPa 최소) · σ 는 *"just an averaged metric"* (유지 중 국소 변화 못 잡음) | 카드 §0 ⑧ · 원문 p.3 · p.4 · p.5 · p.6 | [인쇄] | 감압 두께 · 기공 · 0 MPa · 파쇄 시작 압력 · 반복 수 미측정 (카드 [미확인] 목록)
- [j] korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens | 카드가 적은 원문 문제: S11 ↔ 두께 모순 · NE 5.3 재현 안 됨 · '≈50 mg' ↔ 기하 · 초록 1.66 ↔ 1.62 · P1/P2/P3 이름 뒤바뀜 · Table S1 단위 | 카드 §3-10 · §11 | [카드 산술] | 기공 절대값 인용 금지

## k — DEM 의 한계 (원문 문장 · 위치)

- [k] korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens (Korjus et al., Energy Storage Mater. 82 (2025) 104589) | **말 없음** — DEM · 입자 계산을 쓰지 않는다.  가까운 문장 둘: *"For the sake of investigation, the particles are ascribed as ideal spheres."* (p.4 — PSD 를 위한 등가 구 가정) · *"the ionic conductivity is just an averaged metric that does not necessarily capture local morphological modifications or chemomechanical dynamics while being pressed for a longer time."* (p.5) | 카드 §4-4 (i) | [인쇄] | 단단한 구 · 점접촉의 한계 진술이 아니다

## l — 소성변형이 왜 어려운가 · 우회 · 값

- [l] korjus2025_lpscl_densification_multiscale_insitu_xct_eis_qens (Korjus et al., Energy Storage Mater. 82 (2025) 104589) | 소성을 계산에 넣는 어려움 = 논의 없음 (계산 없음).  측정으로 본 '냉간 소결' 기전 (≤ 510 MPa · 누른 채) = **큰 2 차 입자 파쇄** — *"the larger particles fracture under the pressure applied, resulting in smaller particles"* (p.4) · 개수 >30 µm 4424 → 2865 · <10 µm 3555 → 10,241 (p.6) — + **재배열** (30 분 유지 중 PSD 이동 · σ 그대로, p.5) + **입계 접촉 개선** (Ea_GB 0.42 → 0.33 eV) · 큰 입자 형상 (Sneed–Folk) · 회색값 밀도 불변 → *"“cold sintering” the solid electrolyte with pressures up to 510 MPa only reorganizes the particles, leading to improved contact and decreased porosity, while the bulk itself does not sinter"* (p.9) · 우회 · 맞춘 값 · 계산 비용 = 해당 없음 (실험) | 카드 §4-4 (ii) · §3-4 · §7-3 | [인쇄] | '입자' = 결정 ≈50 nm 의 응집체 (*"“particles” mean secondary particles or aggregates"*, p.6) → 응집체 해체 (단결정 파괴 아님) · 18 배 연화가 뭉친 기전 (재배열 · 미세 파괴) 의 실측 사례로만 인용

## m — 받아들일 통찰

- [m] **기공 연산자의 '해상도 아래 상' 칸** — 무엇을: CT 이진 분할의 '기공' 등급에 해상도 아래 작은 입자가 섞인다 (76.2 MPa 단면 ≈54 % · 문턱 따라 48–61 % [판독]) · 같은 펠릿 기공 부피의 90 % 가 < 1 µm → 우리 기공 연산자 등록에 '해상도 · 문턱 · 해상도 아래 상의 배정' 칸을 결과 전에 · 어디: 단계 0 · U6 · 왜: 카드 §3-3 · §8 (원문 p.6 · SI Note 2 · Fig S3a)
- [m] **두께 → 기공은 고체 부피 보존 식으로** — 무엇을: (1 − ε)·t = 일정 (질량 · 단면적 일정) 을 식으로 명시하고 앵커의 상태 (뺀 뒤 ↔ 누른 채 · 다른 펠릿) 를 같이 등록 · 어디: 단계 0 · 결과 전 대조 항목 · 왜: S11 이 자기 두께와 모순 (ε₇₆ ≥ 31 % 여야 하는데 12.1 %) — 카드 §3-3
- [m] **σ₀ = 펠릿 값 관례의 실측 정합** — 무엇을: 가압은 입계만 바꾸고 벌크 (Ea 0.44 → 0.40 · QENS 가루 = 펠릿) 는 둔하다 (≤ 510 MPa) → 우리 σ_grain (펠릿 · CL-91) 을 압력 무관 상수로 두는 것의 근거 쪽 · 'GB 없는 σ' 숫자 (5.3) 는 재현 안 되므로 σ₀ 자리에 쓰지 않음 · 어디: 단계 7 · 흐름 밖: σ₀ 해석 · 왜: 카드 §3-7 · §3-8 · §7-4
- [m] **인용 사슬 · 단위 함정** — 무엇을: 문헌 표의 단위 (Table S1 'nm' = Å) 와 남이 다시 낸 값 (ou2026 '31.01 mS/cm @ d ≈ 491 nm' ↔ 원문 5.3 mS/cm · ≈50 nm) 을 원문 값과 구분 표지 · 어디: 흐름 밖: 확산 계수 · σ · 입도 인용 검사 · 왜: 카드 §0-1 · §3-8 · §3-9

## n — 논문 에이전트 후보 (이 카드가 인용 · 언급했지만 litdb 에 카드가 없는 것)

- [n] P. Perrenot, A. Fauchier-Magnan, M. Mirolo, L. Lecarme, P.-H. Jouneau, A. Boulineau, P. Bayle-Guillemaud, C. Villevieille, Room-temperature sintering of amorphous thiophosphate solid electrolyte (Li3PS4): coupling morphological evolution to electrochemical properties, Adv. Funct. Mater. n/a (n.d.) 2310739. https://doi.org/10.1002/adfm.202310739. | a · b · j · m — 같은 그룹 · 같은 σ 에서 다른 잔류 기공 분포 (3D 기공 퍼콜레이션 → 덴드라이트) · 유지 중 입자 재배열의 선례 (원문 p.2 · p.5 [18]) · 카드 §12 | litdb 확인: `ls perrenot*` 없음 · "2310739" grep = jeong2024 · thompson2026 (인용만) → 카드 없음
- [n] Z. Chen, Y. Zhao, Tortuosity estimation and microstructure optimization of non-uniform porous heterogeneous electrodes, J. Power Sourc. 596 (2024) 234095. | m · 흐름 밖 (J 절 τ_geo) — 이 논문 τ_geo 계산법 (Dijkstra · quasi-Euclidean + city-block) 의 원전 ([26] · SI Note 1) · 카드 §12 | litdb 확인: "234095" · "jpowsour.2024.234095" grep 0 건 → 카드 없음
- [n] P. Braun, C. Uhlmann, A. Weber, H. Störmer, D. Gerthsen, E. Ivers-Tiffée, Separation of the bulk and grain boundary contributions to the total conductivity of solid lithium-ion conducting electrolytes, J. Electroceram. 38 (2017) 157–167. | m — 벌크 / 입계 분리 (DRT 고주파 위성 봉우리 경고 [19]) · 우리 σ₀ = 펠릿 값 해석의 방법 근거 · 카드 §12 | litdb 확인: "s10832-016-0061-y" grep 0 건 → 카드 없음
- [n] I. Hanghofer, M. Brinek, S.L. Eisbacher, B. Bitschnau, M. Volck, V. Hennige, I. Hanzu, D. Rettenwander, H.M.R. Wilkening, Substitutional disorder: structure and ion dynamics of the argyrodites Li6PS5Cl, Li6PS5Br and Li6 PS5I, Phys. Chem. Chem. Phys. 21 (2019) 8489–8507. | m — 용량 크기 (≈10⁻¹⁰ ↔ ≈10⁻⁹ F) 로 벌크 / 입계를 배정한 근거 ([34, 35]) · 음이온 무질서 (ou2026 캡션의 '∼60 % anion disorder' 확인처 후보) · 카드 §12 | litdb 확인: "C9CP00664H" grep 0 건 → 카드 없음

## 카드 문제

1. `ou2026_microstructural_multiscale_fast_ion_transport` L139 · L451 — *"exp QENS [Korjus] (d ≈ 491 nm) **31.01 mS/cm**"* · *"QENS 31.01 mS/cm ⇒ 1.07×"*: 이 논문이 인쇄한 QENS σ 는 **5.3 mS/cm** (p.8) — 31.01 은 Ou 가 이 논문의 D (2.28×10⁻¹¹ m²/s) 에 자기 Λ_Cl (2.181×10⁻² Å⁻³) 를 곱해 다시 낸 값 (298 K 에서 31.0 으로 재현 [카드 산술]) 인데 카드에 '재계산' 표지 · 원문 5.3 병기가 없다.  'd ≈ 491 nm' 은 Table S1 의 단위 오기 ('491.38 [nm]' = Å · 원문 본문 · SI Note 3 는 ≈50 nm) 를 그대로 읽은 크기.
2. `thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography` L124 — *"LPSCl 은 큰 입자가 깨지고 (Korjus 2025 인용) 입내 공극까지 닫히며"* — 파쇄는 이 논문과 같다; '입내 공극 닫힘' 은 Thompson 자신 (L109 · 1155 MPa) 의 관찰이고 이 논문 (≤ 510 MPa) 은 반대로 382 MPa 에서도 입내 공극이 상당 · 큰 입자 밀도 불변이라 적는다 — 문장 귀속이 모호 (값 문제 아님).
3. `thompson2026_…` L44 — NEI LPSCl *"추정 입경 5 µm"* ↔ 이 논문 SEM PSD (같은 공급사 · 가루 KDE 봉우리 ≈3.4 µm · 집단 ≈20 · ≈40 µm 응집체) — 다른 로트일 수 있어 카드 오류로 단정하지 않음 (정보).
4. (원문 문제 — 카드 §3-10 · §11 에 기록) S11 기공 ↔ Fig 2a 두께 모순 · NE 5.3 재현 안 됨 · 초록 '1.66' ↔ 1.62 · P1/P2/P3 이름 뒤바뀜 · '10 – 33 μm' ↔ '10–30 µm' · τ_geo '1.24' ↔ 1.20 bin · Table S1 단위 · '≈50 mg' ↔ ⌀7.0 mm 기하 · Fig 5 캡션 76.2 MPa ↔ 패널 · SI 교차 참조 오기 셋 · ref [14] 쪽 '755–788' (원 논문 755–758).

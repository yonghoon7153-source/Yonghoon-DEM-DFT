# 배치 93 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-17 · 위시 W-1117-2)

카드 = `ohashi2021_am_youngs_modulus_ion_transport_voxel_fem_ct` (원문 = 출판본 7 쪽 · SI 안내 없음 · 그림 크롭 36 장 = 도구 9 (그림 8 + 표 1 — 9 장 모두 다시 자름) +
손 크롭 27 (패널 8 · 근거 문단 19 · 식 0 — 원문에 번호 매긴 식 없음) · 판독 원자료 `litdb/figures/<slug>/digitized.csv` 133 행).
서지 (k · l 인용용) = Ohashi A., Kodama M., Horikawa N., Hirai S., *Effect of Young's modulus of active materials on ion transport through solid electrolyte in all-solid-state lithium-ion battery*,
J. Power Sources 483 (2021) 229212, DOI 10.1016/j.jpowsour.2020.229212.
⚠ 재료 = **Li₅.₅PS₄.₅Br₁.₅** (LPSCl 아님) + **지르코니아 (≈200 GPa) · 나일론 (≈2 GPa)** 활물질 대리 (NCM 아님) — 계산 = 선형 탄성 복셀 FEM (응력만 · 이온 수송 계산 없음 · DEM · MPM · 압밀 계산 없음).  쪽 = PDF 쪽 p.1–7 (= 인쇄 쪽).

---

## a — 순수 SE 압력별 기공 곡선 · 진밀도 · 상태

- [a] ohashi2021_… | 순수 Li₅.₅PS₄.₅Br₁.₅ 의 **σ(P) 만** — 0.10 (12 MPa) · 0.87 (100) · 1.73 (200) · 2.40 (300) · 2.75 mS/cm (400 MPa) · 포화 ≈300 MPa | 카드 §3-2 · p.4 · Fig 4 | [판독 · 벡터 경로] · 포화 [인쇄] | 누른 채 · 25 °C · 가압만 · **기공률 · 상대밀도 · 진밀도 없음** ('porosity' 0 회) · 선만 있고 측정 표지 없음 (측정인지 맞춤인지 [미확인]) · 재료 Li₅.₅PS₄.₅Br₁.₅

## b — 압력을 뺄 때 되돌아오는 양 · 잰 방법

이 배치에 없음 (가압 가지 · 400 MPa 한 상태만 · 'unload' · 'decompress' · 'release' 0 회 — 카드 §4-1).

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

- [c] ohashi2021_… | 항복 · 경도 · 크리프 값 **없음** · 탄성 입력만: Li₅.₅PS₄.₅Br₁.₅ 자리에 Li₆PS₅Br **E 25.3 GPa · ν 0.35** (Deng 2016 [21] · *"have not been measured"*) · 지르코니아 200.0 · 0.30 · 나일론 2.0 · 0.30 (출처 없음) · 문헌 활물질 LCO · Si · Sn · 흑연 ≈190 · 185 · 50 · 20 GPa ([7] = LCO 논문 하나) | 카드 §3-9 · 표 1 · p.2–3 | [인쇄] | 일축 항복 환산 없음 · SE 25.3 은 치밀 결정 DFT (압분체 아님) · CL-90 세 값 (NCM 경도 · NCM 140 · LPSCl 24 GPa) 없음
- [c] ohashi2021_… | 소성 언급은 하나: *"SE particles must undergo plastic deformation (crushing) to be densified"* | 카드 §3-2 · p.4 | [인쇄] | 값 없음 · 정성

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍

- [d] ohashi2021_… | ★ 400 MPa 결합 선형 탄성 복셀 FEM: 지르코니아 22 / 39 / 52 vol% — SE 평균 MPS **291 / 234 / 196** · 지르코니아 **815 / 692 / 598 MPa** → 지르코니아 축하중 몫 **[0.43, 0.45] · [0.64, 0.68] · [0.77, 0.78]** (평균 응력 정리 아래 · 위 한계) · SE ÷ 인가 0.73 / 0.585 / 0.49 | 카드 §3-6 · Fig 8b · p.5 | [판독 ±3 MPa] · [카드 산술] | 계산값 (측정 아님) · E_SE 25.3 한 값 · E 대비 7.9 · Li₅.₅PS₄.₅Br₁.₅ + 지르코니아 대리 · Σ φ·MPS ÷ 400 = 1.01–1.03 (일관)
- [d] ohashi2021_… | 무른 대리 (나일론 2 GPa · E 대비 0.079) 29 / 61 / 75 %: SE 546 / 856 / 918 · 나일론 118 / 165 / 289 MPa → 나일론 몫 [0.03, 0.09] · [0.17, 0.25] · [0.43, 0.54] · 원문 *"Stress concentrates in a material with higher Young's modulus"* (Highlights) · *"This material will act as a stress support and decrease the stress experienced by the neighboring materials"* (p.5) | 카드 §3-6 · Fig 8a | [판독] · [카드 산술] · [인쇄] | 결합 가정이 무른 상 응력을 올리는 사슬을 원문이 스스로 씀 (p.6) · E_SE 를 압분체 강성 (0.3 GPa · 같은 그룹 2020) 으로 두면 나일론이 더 단단해진다 [카드 추론]
- [d] ohashi2021_… | 실측 쪽 (응력 아님): 포화 압력 나일론 ≈250 < 순수 SE ≈300 < 지르코니아 22 % ≈350 · 39 / 52 % > 400 MPa · 200 MPa 에서 분율이 7–22 %p 더 큰 나일론 복합체가 지르코니아와 같거나 높다 (1.22 · 1.06 배) → 400 MPa 에서 0.98 배 | 카드 §3-4 · §3-5 · Fig 5 · 6 · p.4 | [인쇄] · [판독] · [카드 산술] | 두 대리는 모양 (구 ↔ 불규칙) · 소성도 다르다 · 같은 분율 짝 없음

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안

이 배치에 없음 (DEM · 접촉 법칙 없음 — 결합 연속체 FEM).

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙

- [f] ohashi2021_… | MPM 아님 — 영상 기반 **복셀 FEM** (CT 복셀 = 요소 · *"used as a mesh one-to-one"* · ≈300³ · GPU) · 상 경계 **결합** (*"nylon and SE are continuous in a FEM"*) · 접촉 · 미끄럼 · 분리 없음 · 해상도: 복셀 5 × 5 × 6 µm · 대리 50 µm = 10 복셀 (6 µm 축 8.3) [카드 산술] · SE 입자 · 나노 빈틈은 SE 상에 묻힘 · 수치 오차 추정 · 격자 수렴 시험 없음 | 카드 §4-2 · p.3 · p.6 | [인쇄] · [카드 산술] | 지름당 셀 수 규칙의 근거 문장은 없다 (원문은 해상도 부족을 '이온 수송 계산을 못 하는 이유' 로만 씀)

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거

이 배치에 없음 (측정 · 계산 모두 3D · '2D' 0 회).

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점

- [h] ohashi2021_… | DEM 넘김은 없음 — **CT → FEM** 넘김 (400 MPa 누른 채 찍은 형상을 그대로 · 압밀이 끝난 시점에 한 번 · 응력 무상태에서 400 MPa 다시) | 카드 §4-2 | [인쇄] · [카드 추론 — 하중 이력 해석] | 압밀 이력 · 잔류 응력이 넘어가지 않는다 (선형 · 한 상태)

## i — 복합 양극 (AM + SE) 의 압력별 기공

이 배치에 없음 — 복합체 기공 숫자 없음 (CT 는 대리 부피 분율만 · 압력별 **σ** 는 있다 = Fig 5 표지 51 점 · 카드 §3-3).

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것

- [j] ohashi2021_… | 원문: *"X-ray CT measurement in high resolution was difficult to perform … calculation in this study was limited to FEM stress calculation, which is applicable for low resolution dataset"* (p.3) · *"the difference in the saturation pressure between a high and low volumetric fraction of nylon is indistinguishable from the experimental results"* (p.6) · *"the saturation pressures plotted are approximated values within the scope of our definition"* (p.4) · 나노 특징 *"were not visualized in this study"* (p.2) | 카드 §3-4 · §4-2 · §11 | [인쇄] | 카드가 덧붙인 한계: 선형 탄성 · 결합 · E_SE 한 값 · 탈압 · 기공 · 같은 분율 짝 없음 · 대리 모양 · 소성 차이 (§11)

## k — DEM 의 한계 (원문 문장 · 위치)

- [k] ohashi2021_… (Ohashi et al. 2021, J. Power Sources 483, 229212) | **말 없음** — DEM 을 쓰지 않는다.  가까운 문장 (연속체 가정이 결론의 이유): *"From the viewpoint of a continuous model, because the stress concentration occurs in a greater magnitude on the SE as the volumetric fraction of nylon increases, the strain of the SE increases. Because nylon and SE are continuous in a FEM, the increase in the strain of the SE induces an increase in the strain of an adjacent nylon."* (p.6) | 카드 §4-3 (i) | [인쇄] | DEM 한계의 근거로 인용하지 않는다 (결합 연속체의 성질을 적은 문장)

## l — 소성변형이 왜 어려운가 · 우회 · 값

- [l] ohashi2021_… (Ohashi et al. 2021, J. Power Sources 483, 229212) | 어려움 논의 **없음** · 원문이 소성을 스스로 요구: *"as the larger voids disappear as the pressure is increased, SE particles must undergo plastic deformation (crushing) to be densified"* (p.4) · 그런데 계산 = **선형 탄성** (*"linear stress analysis"* · *"linear voxel-based finite-element method"*, p.3) · 우회 = 압밀은 실험이 하고 마지막 형상의 탄성 응답만 계산 · 맞춘 값 0 (물성 = 빌린 DFT · '대략' 값) · 비용 = ≈300³ 복셀 한 번 · GPU · 시간 [미확인] · 모형 선택 이유 = 해상도뿐 (*"applicable for low resolution dataset"*, p.3) | 카드 §4-3 (ii) · §4-2 | [인쇄] · [카드 산술] | 소성을 넣지 않은 까닭을 말하지 않는다 — '소성이 왜 어려운가' 의 인용 근거로는 약하다 (요구 문장 + 탄성 계산의 대비로만)

## m — 받아들일 통찰

- [m] ohashi2021_… | **하중 몫을 두 한계로 보고하는 관측량** — 상별 평균 최소 주응력만 있어도 평균 응력 정리로 [1 − (1 − φ)⟨MPS⟩_SE / P, φ⟨MPS⟩_AM / P] (이 논문 지르코니아 22 % 폭 0.02) · Σ φ·MPS ÷ P ≥ 1 이 출력 일관 점검 → 자리: 단계 0 · 단계 5 · 조건 R1 (우리 DEM AM–AM · 상별 virial 과 MPM 결과를 같은 축에) | 카드 §3-6 · §9-1
- [m] ohashi2021_… | **영률 민감도 시험은 모양 · 크기 · 소성을 묶어 둔다** — 이 논문의 두 대리는 구 ↔ 불규칙 · 세라믹 ↔ 고분자라 '영률 효과' 를 가르지 못했다 → 자리: 단계 3 · 단계 5 (같은 침대 · 같은 PSD 에서 AM E 하나만 바꾼다) | 카드 §0 한정어 ② · §11-2 · Fig 1
- [m] ohashi2021_… | **'어느 상이 단단한가' 는 E_SE 선택이 정한다** — 치밀 결정 25.3 GPa 면 나일론 2 GPa 가 무르고, 압분체 할선 (같은 그룹 25–250 MPa · 0.3 GPa) 이면 단단하다 → 문헌 연속체 하중 몫과 견줄 때 E 대비부터 병기 (우리 DEM ≈104 ↔ 실제 NCM811/LPSCl ≈6.3 ↔ 이 논문 7.9) → 자리: 후보 D0 · 후보 A · frame [2] | 카드 §7-4 · §9-3
- [m] ohashi2021_… | **포화 압력 이동을 방향 표적으로** — 단단한 AM 분율 ↑ → 포화 압력 ↑ (≈350 → > 400 MPa) · 무른 대리 ↓ (≈250) → 자리: 흐름 밖: 접촉망 σ_ionic(P) 사다리 (100–600 MPa) 에서 'AM 많을수록 포화가 늦어지는가' (크기 대조 금지) · 후보 M0 (유효 SE 압력 κ: FEM 0.73 ↔ 포화 압력 비 0.86) | 카드 §3-4 · §8 M0 · §9-4

## n — 논문 에이전트 후보

- [n] M. Kodama, A. Ohashi, S. Hirai, In situ X-ray computational tomography measurement of single particle behavior of sulfide solid electrolyte under high- pressure compression, J. Power Sources Adv. 4 (2020) 100019, https://doi.org/10.1016/j.powera.2020.100019. | a · c · l — '입자 **안** 빈틈 감소' 근거 [19,24] (p.4) · 단일 황화물 입자의 고압 거동 (파쇄 · 소성) — 카드 §3-2 · §12 | litdb 확인: `git ls-tree` papers/ 에 kodama* = kodama2020 (다른 논문) 뿐 · "100019" grep = faka2026 · kodama2020 · taghikhani2025 (인용 · 언급만) → 카드 없음 (`wishlist.md` L37 에 'n 밖' 참고 줄로만 있음)
- [n] C. Yu, Y. Li, W. Li, K.R. Adair, F. Zhao, M. Willans, J. Liang, Y. Zhao, C. Wang, S. Deng, R. Li, H. Huang, S. Lu, T.-K. Sham, Y. Huang, X. Sun, Enabling ultrafast ionic conductivity in Br-based lithium argyrodite electrolytes for solid-state batteries with different anodes, Energy Storage Mater 30 (2020) 238–249. | a · c — 이 논문 SE (Li₅.₅PS₄.₅Br₁.₅) 의 처방 · 400 MPa σ 가 *"roughly corresponds"* 한 문헌 값 (원문에 값 없음) — 카드 §3-1 · §3-2 · §12 | litdb 확인: 'Enabling ultrafast' · 'Br-based lithium argyrodite' grep 0 → 카드 없음
- [n] A. Sakuda, Favorable composite electrodes for all-solid-state batteries, J. Ceram. Soc. Japan. 126 (2018) 675–683, https://doi.org/10.2109/jcersj2.18114. | a · i — 복합 전극 σ–압력 곡선의 선례 (*"similar to that of many of reported curves from previous studies [19,22,23]"*, p.4) — 카드 §12 | litdb 확인: 'jcersj2.18114' · 'Favorable composite electrodes' grep 0 → 카드 없음
- [n] A. Sakuda, A. Hayashi, M. Tatsumisago, Recent progress on interface formation in all-solid-state batteries, Curr. Opin. Electrochem. 6 (2017) 108–114, https://doi.org/10.1016/j.coelec.2017.10.008. | a · l — 상온 가압 소결 · 포화 압력 상승을 제조에서 고려해야 한다는 근거 [26] (p.6) — 카드 §12 | litdb 확인: 'coelec.2017.10.008' · 'interface formation in all' grep 0 → 카드 없음
- (참고 · 셈에 넣지 않음 · batch_92 (본 세션 · `ohashi2020_…`) n 줄에 이미 있음) [7] E.J. Cheng 외 2017 J. Asian Ceram. Soc. 5, 113 (LCO 탄성 — 이 논문은 LCO · Si · Sn · 흑연 넷의 근거로 씀) · [20] Y. Nagano 외 2004 (VOXELCON 방법 원전 — 이 논문은 *"2004, 53, 701-708"* · batch_92 는 *"52 … 701-701"*) · [25] G. Bucci 외 2017 J. Electrochem. Soc. 164, A645 (활물질 응력 → 용량) · [10] 같은 제목을 이 논문은 *"A. Hayashi, M. Tatsumisago … J. Ceram. Soc. Japan. (2018) 719–727"* (저자 잘림 · 권 없음) 로 적는다 — batch_92 의 Kato 외 판.

## 카드 문제

없음 — 가리킨 카드 `sakka2022_…` (L126 · L362) 는 이 논문에서 숫자를 옮기지 않았고 서지가 원문과 같다.  (원문끼리의 어긋남은 카드 §3-11 에 적었다: 이 논문이 [19] 의 셀을 '450 MPa 까지' 라 쓰는데 `kodama2020_…` §3-1 은 그 셀을 '최대 ≈100 MPa (PEEK 내구)' 로 적는다 — 카드 문제가 아니라 두 원문의 차이 · 같은 셀인지 [미확인].)

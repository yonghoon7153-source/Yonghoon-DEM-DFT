# 배치 43 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-12)

카드 = `doux2020_pressure_effects_sulfide_se_jmca` (새 카드 · 원문 본문 7 쪽 + ESI 5 쪽 전부 렌더 정독 · 그림 크롭 36 장 (그림 12 + 패널 14 · 표 1 · 근거 문단 9) ·
판독 원자료 litdb/figures/doux2020_pressure_effects_sulfide_se_jmca/digitized.csv 129 행 — 인쇄값으로 보정 확인).
서지 (k · l 인용용) = Doux J.-M., Yang Y., Tan D. H. S., Nguyen H., Wu E. A., Wang X., Banerjee A., Meng Y. S., *Pressure effects on sulfide electrolytes for
all solid-state batteries*, J. Mater. Chem. A 8 (2020) 5049–5055, DOI 10.1039/c9ta12889a.
⚠ 같은 1저자 · 같은 해의 다른 논문 = `doux2020_stack_pressure_assb` (Adv. Energy Mater. 10, 1903253) — 섞지 않는다.  재료 = Li₆PS₅Cl (NEI 상용) — 우리와 같은 조성이지만 분말 · 입경 미상.

---

## a — 순수 SE 압력별 기공 곡선

- [a] doux2020_pressure_effects_sulfide_se_jmca | 순수 Li₆PS₅Cl (NEI) 펠릿 70 mg · ⌀10 mm · 성형압 3 분 → 상대밀도 68.3 / 70.3 / 75.4 / ≈77 % (50 / 150 / 250 / 370 MPa) → 기공 31.7 / 29.7 / 24.6 / ≈23 % (자기 분모) | 카드 §3-2 · 논문 p.5051 (68.3 · 75.4) · Fig 4 그림 글자 (68 % · 77 %) · Fig 3a (70.3 · 77.2) | [인쇄] · [판독] · 기공 [카드 산술] | **성형압을 뺀 뒤** · "physical measurements" (방법 · 측정 시점 압력 미인쇄) · 300 MPa 점 없음 · 시료 4 개 표준편차
- [a] doux2020_pressure_effects_sulfide_se_jmca | 진밀도 분모 = **원문에 없음** (1.64 · 1.860 둘 다 본문 · ESI 에 없음) · 역산 (m 70 mg · ⌀10 mm · σ · Fig 3b 저항) 1.77–1.98 g/cm³ (평균 1.88) · 분모가 1.860 이었다면 랩 표준 1.64 기준 기공 14.5 / 12.4 % (250 / 370 MPa) · 1.64 였다면 24.6 / ≈23 % | 카드 §3-3 · §7-2 | [미확인] · [카드 산술 · 추정] | 가정 넷 (질량 손실 없음 · 면적 ⌀10.0 mm · R = 수직선 시작 Z′ (한 스펙트럼) · 두께 = SE 만) — 분모를 정하지 못한다
- [a] doux2020_pressure_effects_sulfide_se_jmca | 같은 압력의 σ_ion 0.99 / 1.43 / 2.06 / 2.28 mS/cm (적층압 25 MPa · 4 시료 평균) | 카드 §3-2 · p.5052 · Fig 3a | [인쇄] (1.43 [판독]) | Fig 3 의 전극 종류 미기재 (탄소 쪽 [추정])

## b — 탈압 때 되돌아오는 양 · 잰 방법

- [b] doux2020_pressure_effects_sulfide_se_jmca | **성형압 탈압**: 치수 회복 · 가압 중 두께를 **재지 않았다** — 모든 밀도 · σ 가 뺀 뒤 값 | 카드 §4-2 | 원문에 없음 | 언로딩 트랙의 대조점 아님
- [b] doux2020_pressure_effects_sulfide_se_jmca | **적층압 탈압** (370 MPa 펠릿 · 70 → 2 MPa): σ 이력 — 같은 압력에서 감압 가지 ÷ 가압 가지 = Ti 2.47 (2) · 2.01 (10) · 1.16 (50) · 1.08 (60 MPa) · 탄소 1.20 (2) · 1.22 (5) · 1.06 (50) · 1.03 (60 MPa); 잰 방법 = EIS (1 MHz – 1 Hz) 만 | 카드 §3-4 · Fig 2a · p.5050 (*"after releasing the stack pressure from 70 MPa, the conductivity at lower pressures is significantly higher than before"*) | [판독] · [카드 산술] | 치수가 아니라 전극–SE 계면 접촉의 이력 (저자: 접촉이 적층압에 강하게 의존 · 소성 평탄화로 읽는 것은 [카드 추론])

## c — 항복 · 경도 · 크리프 값과 정의 · 일축 환산

이 배치에 없음 (원문에 E · H · 항복 · 크리프 측정 없음 — 카드 §3 · §11).

## d — 단단한 입자의 하중 몫 · 재밍

이 배치에 없음 (복합체 하중 · 재밍 자료 없음).

## e — 점접촉 법칙이 깨지는 범위와 대안 · 맞춘 값 수

이 배치에 없음 (모델 없음).

## f — MPM 접촉 · 다물체 · 강체 결합 · 해상도 규칙 · 수치 오차

이 배치에 없음.

## g — 2D → 3D 경고 · 증거

- [g] doux2020_pressure_effects_sulfide_se_jmca | 실험 영상 쪽 경고: *"As a cross-sectional view is not representative of the volume distribution of the porosity, FIB 3D reconstruction was performed."* — 재구성 10 × 8 × 4 µm · 100 nm × 40 장 · 기공 숫자는 내지 않음 | 카드 §3-6 · 논문 p.5053 · SI p.2 | [인쇄] | 계산 2D → 3D 전이가 아니라 **2D 단면 ↔ 3D 부피** 영상 대표성 진술

## h — DEM 에서 FE · MPM 으로 넘긴 선례

이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공

- [i] doux2020_pressure_effects_sulfide_se_jmca | 셀 양극 = LNO-NCA / Li₆PS₅Cl / 아세틸렌 블랙 11 : 16 : 1 (NCA ≈39 wt% [카드 산술]) 12 mg 을 SE 와 같은 성형압 (50–370 MPa) 으로 — **기공 숫자 없음** · 음극 Li–In 은 150 MPa (50 MPa 셀만 50 MPa) | 카드 §3-7 · SI p.2 | [인쇄] | 조성 · 압력 이력만 · 우리 AM 70–80 wt% 와 다름

## j — 카드가 스스로 적은 한계 (가압 · 탈압과 닿는 것)

- [j] doux2020_pressure_effects_sulfide_se_jmca | 저자: 50 MPa 는 *"densification is not complete"* (p.5053) · 250 MPa 위는 *"progressively smaller impact on the relative density"* (p.5052) · *"necessary to focus on reducing the porosity … hot pressing or spark plasma sintering"* (p.5053) · 문헌은 적층압을 보고하지 않는다 (p.5050) | 카드 §0-1 · §3-2 | [인쇄] | 모델 한계 진술 없음
- [j] doux2020_pressure_effects_sulfide_se_jmca | 카드가 적은 한계: 진밀도 분모 · 상대밀도 측정법 미인쇄 · Fig 2 캡션 "decreased to 5 MPa" ↔ 그림 2 MPa 점 · 탄소 "almost independent" ↔ ×1.75 · "one order of magnitude" 는 2 MPa 에서만 (×7.8) · 50 MPa 셀은 음극도 50 MPa · Fig S5 캡션 "350 MPa" ↔ 370 | 카드 §11 | [미확인] · [판독] · [카드 산술] | —

## k — DEM 의 한계 (서지 병기)

- [k] doux2020_pressure_effects_sulfide_se_jmca (Doux · Yang · Tan · Nguyen · Wu · Wang · Banerjee · Meng 2020, J. Mater. Chem. A 8, 5049–5055) | **말 없음** — DEM · 모델이 없는 실험 논문 | 카드 §4-3 (i) | — | —

## l — 소성변형이 왜 어려운가 (서지 병기)

- [l] doux2020_pressure_effects_sulfide_se_jmca (Doux 외 2020, J. Mater. Chem. A 8, 5049–5055) | **말 없음** (계산이 없다).  재료 무름에 대한 원문만: *"the contact interface between the soft sulfide electrolyte and the hard titanium plunger depends strongly on the stack pressure"* (p.5050) · *"As expected, due to the softer electrode materials, the stack pressure does not have a distinguishable effect on the cycling stability of the cell"* (p.5051) · 370 MPa 단면이 *"denser and made of larger grains"* (p.5053 — 냉간 압착의 입자 합체로 읽는 것은 [카드 추론]) | 카드 §4-3 · §3-6 | [인쇄] | 소성의 계산 우회 · 비용 없음

## m — 받아들일 통찰 (무엇을 · 우리 쪽 어디에 · 근거)

- [m] doux2020_pressure_effects_sulfide_se_jmca | **계산 σ 와 견줄 실험 σ 는 탄소 전극 · 충분한 적층압 측정** — 같은 펠릿 · 같은 적층압에서 Ti ↔ 탄소가 ×7.8 (2 MPa) · ×1.8 (25) · ×1.3 (70 MPa) 갈린다; 우리 망 · 복셀 σ 는 판 면 전체 Dirichlet (이상 접촉) | 흐름 밖: 수송 계산 경계조건 · 실험 σ 앵커 선택 (단계 7 · Rint ②) | 카드 §3-4 · §7-4 · Fig 2a | [판독] · [카드 산술]
- [m] doux2020_pressure_effects_sulfide_se_jmca | **기공 연산자 등록에 분모 · 상태 칸을 필수로** — 이 논문의 상대밀도는 분모 미인쇄라 랩 표준 1.64 로 옮기면 분모 선택만으로 ≈10 %p (24.6 ↔ 14.5 % @ 250 MPa) | 단계 0 · 결과 전 대조 항목 | 카드 §3-3 · §7-2 | [카드 산술]
- [m] doux2020_pressure_effects_sulfide_se_jmca | **"Doux 2020" 인용은 권 · 쪽으로 가른다** — Tron 2023 의 1.64 근거 (ref 22) 는 AEM 1903253 이고 이 JMCA 논문에는 진밀도가 인쇄돼 있지 않다 | 흐름 밖: 진밀도 1.64 인용 사슬 · 서지 규율 | 카드 머리 · §7-3 · `tron2023` §3-2 | [인쇄]
- [m] doux2020_pressure_effects_sulfide_se_jmca | **기공이 클수록 계면 몫** — MWBH ÷ 측정 비 0.52 (ε 0.32) → 0.93 (ε 0.25) · 고주파 입계 호는 50 MPa 에만 (전체 저항의 ≥ 8 %) | 흐름 밖: Rint ② SE–SE 계면 저항의 기공 의존 (방향만) | 카드 §3-5 · §7-4 | [판독] · [카드 산술]

## n — 논문 에이전트 후보 (litdb 에 카드 없음 · 많아야 다섯)

litdb 확인 = 정본 `litdb/papers/` 파일 목록 509 장 (`git ls-tree`) + `git grep` (권 · 쪽 · 제1 저자 성) — 다섯 모두 자기 카드 없음 (ref 12 Sakuda 2013 은 카드 있음 → 뺐다).

- [n] A. Hayashi, A. Sakuda and M. Tatsumisago, Front. Energy Res., 2016, 4, 25. | a — 이 논문이 "성형압 ↓ → 기공 ↑ → σ ↓" 의 두 근거로 [12, 13] 을 든다 (p.5049) · 12 (Sakuda 2013) 는 카드가 있고 13 은 없다 — 황화물 성형성 · 압력별 밀도 자료가 있는지 원문 확인 | papers/ 에 hayashi* 없음 · "Front. Energy Res" grep = 다른 논문 인용만
- [n] F. Wu, W. Fitzhugh, L. Ye, J. Ning and X. Li, Nat. Commun., 2018, 9, 4037. | a · j — *"the effect of operating stack pressure on this ionic conductivity also needs to be characterized"* 의 근거 [14] (p.5049) | papers/ 에 wu2018* 없음 · "4037" grep = 인용만 (fitzhugh2021 · wang2022)
- [n] N. Riphaus, B. Stiaszny, H. Beyer, S. Indris, H. A. Gasteiger and S. J. Sedlmaier, J. Electrochem. Soc., 2019, 166, A975–A983. | a · j — 같은 문장의 둘째 근거 [15] | papers/ 에 riphaus* 없음 · "A975" grep 0
- [n] J. A. Dawson, P. Canepa, M. J. Clarke, T. Famprikis, D. Ghosh and M. S. Islam, Chem. Mater., 2019, 31, 5296–5304. | m (흐름 밖: Rint ② SE–SE 계면) — *"In the case of sulfide electrolytes, the grain boundaries nevertheless have a high ionic conductivity compared to oxides"* 의 근거 [31] (p.5053) | papers/ 에 dawson2019* 없음 · "5296" grep 0
- [n] D. Pérez-Coll, E. Sánchez-López and G. C. Mather, Solid State Ionics, 2010, 181, 1033–1042. | m (흐름 밖: 밀도별 입계 저항) — *"larger contributions from the grain boundaries are expected at a lower fabrication pressure"* 의 근거 [28] (p.5050) | papers/ 에 perezcoll* 없음

## 카드 문제

- `doerrer2021_single_crystal_nmc_lpscl_cathode_high_energy_density` L150 — Fig 5d 판독 "NCA (ref 32) **139.5 @ 5 MPa**" ↔ 이 논문 (= doerrer ref 32) 의 5 MPa 셀 첫 방전 **136.1** · 25 MPa 대조 **139.3** mAh/g [판독 Fig S6 · S4 와 같음] — 139.5 는 25 MPa 대조 값 높이.  doerrer 원문 그림의 문제인지 그 카드 판독의 문제인지 [미확인] (고치지 않음).
- `heck2026_densification_sulfide_se_binder_scalable` L294 — ref 21 (J. Mater. Chem. A 8 (2020) 5049–5055) 을 "정본 카드 있음 (`doux2020_stack_pressure_assb`)" 으로 적었다 — 그 카드는 AEM 1903253 (다른 논문) · 이제 맞는 카드 = `doux2020_pressure_effects_sulfide_se_jmca` (고치지 않음).
- `beutl2024_round_robin_coin_cell_sulfide_assb` L363 — 저자 "A. **Banerjeea**" = 원문 첫 쪽의 소속 위첨자 a 가 이름에 붙은 꼴 (원문 Abhik Banerjee^a) · beutl 원문 참고문헌의 오기를 옮긴 것인지 [미확인] (고치지 않음).
- `kim2023_mechanofusion_ncm811_lpscl_core_shell_intimate_contact` L281 — "D. H. Tan" ↔ 원문 "D. H. S. Tan" (머리글자 하나 빠짐 · kim2023 원문 표기일 수 있음 [미확인]).
- (원문 자체의 어긋남 — 카드 §11 에 기록) Fig 2 캡션 "decreased to 5 MPa" ↔ 그림의 2 MPa 감압 점 · Table 1 적층압 "5–70" ↔ 그림 2 MPa · Fig S5 캡션 "350 MPa" ↔ 범례 370 MPa · 탄소 전극 "almost independent" ↔ 판독 ×1.75 · 결론 "approximately one order of magnitude" ↔ 25 MPa ×1.8.

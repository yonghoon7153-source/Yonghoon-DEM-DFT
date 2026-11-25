# batch 117 — 정독 질문 a–n 의 근거 (한 편 · 2026-11-16 · 후보 표 N-65 · 대피 세션)

대상: `swinkels1983_hip_densification_plastic_yield_creep_mechanisms` — F. B. Swinkels · D. S. Wilkinson · E. Arzt · M. F. Ashby, "Mechanisms of hot-isostatic pressing", *Acta metall.* **31** (11) 1829–1840 (1983) · Pergamon · 접수 1983-04-17 · 수정 1983-05-27 · DOI 인쇄면 없음 (후보 표 10.1016/0001-6160(83)90129-3 = 2 차 기록)
납 · 주석 (100–200 µm) · PMMA 분말을 실리콘 기름 등방 가압기에서 누르며 밀도를 연속으로 재고 (납 3.52–10.35 · 주석 1.38–13.79 MPa · 27–150 °C · 24 h), 첫 30 s = 소성 항복 · 그 뒤 = 멱법칙 크리프 (압력 지수 6.5) 로 보고, 옛 모델 (배위수 일정 · 둥근 기공) 을 Arzt 1982 의 배위수 n_f(Δ) · 접촉 면적 A_c(Δ) · 뾰족한 기공으로 고친 새 모델 (식 21–24 · 속도 5 배 · 밀도 1 % 안).
쪽 = 학술지 쪽 p.1829–1840 (PDF 쪽 = 학술지 쪽 − 1828) · 판독 원자료 = `litdb/figures/swinkels1983_hip_densification_plastic_yield_creep_mechanisms/digitized.csv` (86 행 · Figs 11 · 12 · 16 · 17 · 20 · 21) · 고른 의도 = '후보 M0 (균질화 압밀 계보) — HIP 기전 지도 (Arzt 계열 · 정본 arzt1982 와 이웃)' → 의도 대조 결과 **일부** (M0 · 기전 · Arzt 계열 · 식 번호별 · 단계 · 기호 · 가정 · 납 · 주석 값 · 장치 · 모델 ↔ 실험 = 채움 / **기전 지도 그림 = 없음** · PMMA 물성 · 확산 속도 식 · 정규화 회귀값 = 없음).

## a — 순수 SE (LPSCl · 황화물) 의 압력별 기공 곡선
이 배치에 없음 — 황화물 없음.  다른 재료 (참고용 · 랩 표준 옆에 놓지 않음):
- [a] swinkels1983_hip_densification_plastic_yield_creep_mechanisms | 납 · 주석 분말의 열간 등방 압력별 영시 (≈30 s) / 최종 (24 h) 상대 밀도 41 시험 — 납 영시 0.698–0.857 · 최종 0.877–0.961 · 주석 영시 0.644–0.864 · 최종 0.820–0.967 (24 h 증가 평균 납 0.129 · 주석 0.158) · 분모 = 재료 밀도 (납 1.14 × 10⁴ · 주석 7.3 × 10³ kg/m³ · 표 3) · 영시 = 누른 채 · 최종 = 시험 끝 침지 (뺀 뒤) 에 맞춘 값 | 카드 §3-3 · p.1832 표 1 · 2 | [인쇄] · 범위 [카드 산술] | 금속 · 27–150 °C · 등방 1.38–13.79 MPa · 랩 표준 (순수 SE 10–13 % · 1.64 g/cm³) 과 다른 재료의 값

## b — 압력을 뺄 때 되돌아오는 양과 잰 방법
이 배치에 없음 — 회복을 재지 않았다.  반면교사 하나:
- [b] swinkels1983_… | 누른 채 연속 밀도는 식 (1) Δ/Δ₀ = (Δ_f/Δ₀)(V_f/V) 로 **시험 끝 침지 밀도 (뺀 뒤)** 에 맞춰 환산된다 — 압분체 부피가 챔버 부피를 그대로 따르고 탈압 회복이 0 이라는 가정이 들어 있다 | 카드 §3-1 · p.1829–1832 · 식 (1) | [인쇄] + [카드 해석] | 열간 금속 (회복이 작을 것이라 짐작할 수는 있어도 원문은 말하지 않는다)

## c — 항복 · 경도 · 크리프 값과 정의
- [c] swinkels1983_… | 항복 응력 σ_y (300 K) 납 **18.5** · 주석 **21.8 MN/m²** ([50] Metals Handbook) · 정의 = *"the tensile flow strength of the material of the particle"* · 온도 식 (19) σ_y = σ_y0[1 − (T − 300)C_T] · C_T 납 4.8 × 10⁻³ · 주석 3.7 × 10⁻³ K⁻¹ (→ 150 °C 에서 7.6 · 11.9 MN/m² [카드 산술]) | 카드 §3-2 · p.1835 · 1837 · 표 3 | [인쇄] | 금속 문헌값 · 이 논문 측정 아님
- [c] swinkels1983_… | ★ 일축 ↔ 접촉 압력 환산: 목이 자라 *"until the local indentation pressure, p₁, is p₁ ≈ 3σ_y"* (평판 압자 미끄럼선 해 [18]) · 크리프 쪽 구속 계수 1/3 (식 24) | 카드 §4-2 식 (4) · §4-6 · p.1835 · 1839 | [인쇄] | 완전 소성 · 속도 무관 가정 (경화 없음)
- [c] swinkels1983_… | 크리프: 치밀화 속도의 압력 지수 **6.5** (100 °C · 납 · 주석 · *"agreeing well with that for steady-state creep of cast samples"*) · 표 3 n 납 5 [48] · 주석 6.6 [49] · [판독] 칠캐스트 100 °C 기울기 납 ≈6.1 (4 점) · 주석 ≈7.3 (3 점) · 소결 시편은 칠캐스트보다 크리프 저항이 크다 (산화막으로 추정) | 카드 §3-4 · §3-6 · p.1832–1833 · Figs 11 · 12 · 16 · 17 | [인쇄] · [판독] | 금속 · T/T_M 0.6–0.8 — LPSCl 실온 압입 크리프 (n ≈21 · papakyriakou2021) 와 다른 구간
- [c] swinkels1983_… | ★ Heckel 상수의 뜻: ln[1/(1 − Δ/Δ₀)] = K₁p_e/σ_y + K₂ (식 10) · *"if K₁ is set equal to 3/2, equation (10) is almost identical with equation (7)"* → [우리 산술] DEM P_y 138 MPa ↔ σ_y = K₁·P_y = 207 MPa (K₁ 3/2) · 새 모델 할선 K₁ 0.72 → 99 MPa · CLAUDE.md P_y/3 = 46 MPa (4.5 배 퍼짐) | 카드 §4-4 · §7-3 · p.1835–1836 | [인쇄] + [우리 산술] | 등방 · 단분산 모델의 K₁ — 일축 금형 Heckel 에 그대로 옮기지 않는다

## d — 단단한 입자와 무른 입자를 섞어 누를 때 단단한 입자의 하중 몫 · 재밍
이 배치에 없음 — 단상 분말.  기하 정성만:
- [d] swinkels1983_… | *"During densification, the average number of contacts per particle (the co-ordination number n_f) increases steadily [3]. At the same time existing contacts grow in area (Fig. 24). Both processes cause the effective pressure on a particle contact to decrease during densification."* — p_eff/p_e = 6.1 (D 0.75) → 2.5 (0.85) → 1.3 (0.95) [카드 산술 식 23] | 카드 §3-5 · §4-3 · p.1838 | [인쇄] + [카드 산술] | 단분산 · 단상 — 이종 하중 분담 아님

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안
- [e] swinkels1983_… | 옛 모델 (배위수 일정 · 둥근 기공 · Wilkinson & Ashby [8]) 은 30 s 밀도와 *"Agreement is poor"* · 크리프 속도를 약 두 자릿수 크게 → 대안 = Arzt 1982 무작위 조밀 충전 기하 n_f = 7.3 + 9.5(Δ − Δ_i)/Δ₀ … (Δ/Δ₀ = 1 에서 13.70 [카드 산술]) · A_c = 3(Δ − Δ_i)a²/Δ₀ · p_eff (식 21–23) · **맞춘 값 0 개** (σ_y 문헌 · A · n 별도 크리프 시험 · Z₀ 7.3 · D₀ 0.64 고정) · 결과 = 저압 ±0.02 ln · 고압 과소 · 크리프 속도 5 배 · 밀도 1 % · 초기 → 최종 전환 Δ/Δ₀ ≈ 0.95 | 카드 §3-7 · §4-3 · p.1837–1840 | [인쇄] + [판독] | 접촉 법칙 (힘–변위) 이 아니라 평균장 기하 · 등방 · 단분산 · 열간 금속

## f — MPM 의 접촉 · 다물체 · 강체 결합 방법과 해상도 규칙
이 배치에 MPM 없음 (J2 단위 시험 해석해 후보는 m 에).

## g — 2D 결과를 3D 로 옮길 때의 경고나 증거
- [g] swinkels1983_… | 말 없음 (2D ↔ 3D 비교 문장 없음) · 모델은 3D (구각 · 무작위 조밀 충전) · 중간 단계의 원통각 (축 구속) 이 2D 꼴 — [카드 산술] 같은 Δ/Δ₀ 에서 원통 붕괴 압력 (식 8 · σ_y/√3) ÷ 구각 (식 7 · (2/3)σ_y) = **0.87** · ln(b/ρ) 기준으로는 (2/√3)σ_y ↔ 2σ_y | 카드 §4-2 · §8 단계 2 · p.1835 | [인쇄] + [카드 산술] | 원문은 이것을 2D/3D 경고로 쓰지 않았다 (단계 구분일 뿐)

## h — DEM 에서 FE · MPM 으로 넘긴 선례와 넘긴 시점
이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공
이 배치에 없음 (단상 분말).

## j — 카드가 스스로 "아직 못 한다 · 한계" 라고 적은 것 가운데 가압 · 탈압 계산과 닿는 것
- [j] swinkels1983_… | 원문: 새 모델도 *"still approximate"* (초록) · 고압 30 s 밀도 과소 (30 s 가압 중 크리프 · 20 s 크리프를 더한 일점쇄선) · 크리프 자료 선택의 불확실성 (소결 ↔ 칠캐스트) · 확산 기전 제외 · 세부는 학위논문 [13, 14] | 카드 §11 1–4 · p.1829 · 1834 · 1839 · 1840 | [인쇄] | —
- [j] swinkels1983_… | 카드가 본 것: 기전 지도 그림 없음 · Figs 20–21 정규화 회귀값 (K₁ · K₂ · C_T) 미인쇄 → 표 3 값으로 재현 안 됨 (rms 0.08–0.09 · 두 상수를 풀면 0.02) · 새 크리프 모델 그림은 주석 한 시험 · 칠캐스트 A · n 숫자 없음 · 식 (18) 응력에 n_f 없음 · Fig. 14 캡션 2.52 ↔ 표 3.52 MPa · 탈압 · 일축 금형 없음 | 카드 §11 5–12 · §3-7 · §13 | [판독] · [카드 해석] | —

## k — DEM 의 한계 (원문 문장 · 인용 서지 = Swinkels, Wilkinson, Arzt & Ashby 1983, Acta metall. 31, 1829–1840)
- [k] swinkels1983_… (Swinkels et al. 1983, Acta metall.) | **말 없음** — 입자 계산 (DEM) 이 없다.  평균장 압밀 모델의 한계로 읽을 문장: *"The models are deficient in at least two regards: they assume a constant co-ordination number for a particle, whereas in reality, it increases with density; and they assume a rounded pore shape, whereas in reality it is sharply cusped."* (p.1839 결론) · *"First, the number of contacts per particle n_f, is assumed constant; in reality it increases with density. Second, the pore is assumed to be rounded; our observations and those of Matthews [34] show that it remains cuspy."* (p.1836) | 카드 §4-6 · §4-8 ① · p.1836 · 1839 | [인쇄] | DEM 의 단단한 구 · 점접촉 한계 문장이 아니다 (단위 셀 모델의 기하 가정)

## l — 소성변형이 왜 어려운가 · 우회 · 비용 (인용 서지 = Swinkels, Wilkinson, Arzt & Ashby 1983, Acta metall. 31, 1829–1840)
- [l] swinkels1983_… (Swinkels et al. 1983, Acta metall.) | 원문 문장: *"Approximate solutions exist for the contact area which results when spheres of a perfectly plastic solid are passed together (Fig. 18)"* (p.1835 · 'passed' = 인쇄 그대로) · *"An exact solution for the constrained creep indentation at the contact faces is difficult, but a dimensional argument [37] leads to the following approximate solution"* (p.1839) · *"We present improved models, which, while still approximate, include new physical ideas"* (초록) | 카드 §4-8 ② · p.1829 · 1835 · 1839 | [인쇄] | —
- [l] swinkels1983_… | 우회 = 평균 입자 하나의 기하 (Arzt 무작위 조밀 충전 n_f(Δ) · A_c(Δ)) + 구속 계수 (소성 3 · 크리프 1/3 · 차원 논증 상수 5.3) · **새 모델에 맞춘 값 0 개** (σ_y = 문헌 [50] · A · n = 칠캐스트 크리프 시험 · Z₀ · D₀ 고정) · 비교 그림의 정규화에만 회귀 상수 3 (K₁ · K₂ · C_T · 값 미인쇄) · 검증 = 30 s 밀도 납 20 · 주석 20 점 (Figs 20–21) + 주석 한 시험의 24 h 곡선 (Fig. 25) · 비용 = 해석식 (계산 없음) | 카드 §3-7 · §4-3 · §4-8 ② · p.1837–1840 | [인쇄] + [판독] | 입자 형상 계산 없음 · 등방 · 단분산 · 금속

## m — 받아들일 통찰
- [m] swinkels1983_… | **P_y ↔ σ_y 환산 규칙을 결과 전에 등록** — 같은 DEM P_y 138 MPa 가 P_y/3 46 · 새 모델 할선 99 · 식 (7) K₁ 3/2 207 MPa 로 4.5 배 갈린다 | 단계 4 (+ CLAUDE.md `SELF-160`) | 카드 §7-3 · p.1836 (K₁ 3/2) · §4-3 할선 [카드 산술]
- [m] swinkels1983_… | **J2 MPM 의 '기공 하나' 해석해 단위 시험** — 구각 붕괴 p = −(2/3)σ_y ln(1 − Δ/Δ₀) = 2σ_y ln(b/ρ) (식 7 + 15) · 평면 변형 원통각 p = −(σ_y/√3) ln(1 − Δ/Δ₀) (식 8) — 다입자 압밀 전에 구성식 · 해상도를 가른다 | 단계 2 · U (새 후보 · U1/U3 옆) | 카드 §4-2 · §8 · p.1835–1836 [카드 산술]
- [m] swinkels1983_… | **실험 밀도를 받을 때 측정 시점 칸** (압력 도달 시간 · 유지 시간 · 누른 채 / 뺀 뒤 · 보정 연산자) — 이 논문의 '30 s 밀도' 에는 크리프가 섞였고 누른 채 곡선은 침지 밀도로 맞춰져 있다 | 단계 0 · 결과 전 대조 항목 | 카드 §3-1 · §3-7 · p.1830–1832 · 1839
- [m] swinkels1983_… | **문헌 그림의 정규화 축을 옮겨 쓰지 않는다** — Figs 20–21 의 p_e/σ_y 는 인쇄되지 않은 회귀 상수로 만들어져 표 3 값으로 재현되지 않는다 ([판독] rms 0.08–0.09) → 표 1 · 2 원 밀도에서 다시 계산 | 결과 전 대조 항목 · 흐름 밖: 문헌 대조 규율 일반 | 카드 §3-7 · digitized.csv

## n — 논문 에이전트 후보 (이 논문이 인용했지만 정본에 카드 없음 · papers/ ls + grep 확인)
- [n] [37] E. Arzt, M. F. Ashby and K. E. Easterling, *Metall. Trans.* **14A**, 211 (1983). (원문 목록 그대로) | 식 (24) 의 차원 논증 · 압입 처리의 원전 · `arzt1982_…` L460 이 *"기구 지도"* 로 적은 그 카드 [15] — 후보 표 N-65 가 기대한 'HIP 기전 지도' 가 있을 자리 · M0 · c · l | litdb 확인: papers/ 에 arzt1983* · easterling* 없음 · 'Easterling' grep = `arzt1982_…` (인용만)
- [n] [8] D. S. Wilkinson and M. F. Ashby, *Proc. 4th Int. Conf. on Sintering and Catalysis*, p. 473. Plenum Press, New York (1975). (원문 목록 그대로) | 옛 크리프 모델 (16)–(18) · 가압 소결 지도의 원전 (서론 *"pressure sintering diagrams [8, 14]"*) — M0 · e | litdb 확인: papers/ 에 wilkinson* 없음 · 'Wilkinson and M. F. Ashby' · 'Wilkinson–Ashby' grep 0
- [n] [35] H. F. Fischmeister and E. Arzt, *Powder Metall.* In press. (서지 일부만 — 권 · 쪽 없음) | 새 모델 식 (21)–(22) 의 원전 쌍둥이 ([35, 36]) · impingement 이후 — e · M0 | litdb 확인: papers/ 에 fischmeister* 없음 · 'Fischmeister' grep = `arzt1982_…` · `german2014_…` · `kakar1967_…` (인용만 · `german2014_…` 가 출판판 후보 Powder Metall. 26 (1983) 82–88 을 적음)
- [n] [19] R. W. Heckel, *Trans. Am. Inst. Min. Engrs.* **221**, 671 (1961). · [20] R. W. Heckel, *Trans. Am. Inst. Min. Engrs.* **221**, 1001 (1961). (원문 목록 그대로) | Heckel 식 (9)–(10) 의 원전 — P_y ↔ σ_y 환산 (c · m 첫째) | litdb 확인: papers/ 에 heckel1961* 없음 · 'R. W. Heckel' grep = `lee2025_heckel_…` · `faka2026_…` · `meyer2017_…` (인용만) · wishlist L81 에 이미 있음
- [n] [3] H. F. Fischmeister, E. Arzt and R. L. Olsson, *Powder Metall.* **21**, 179 (1978). (원문 목록 그대로) | 압분 배위수 · 접촉 면적 실측 (*"increases steadily [3]"* p.1838) — e · d | litdb 확인: papers/ 에 fischmeister* 없음 · 'Olsson' grep = `arzt1982_…` · `german2014_…` 등 (인용만)

## 카드 문제
- `benhadjali2026_wip_vs_cup_pressing_assb_cathode_dem` **L436** (설명 칸) *"카드 없음 — HIP 기전 지도 (Arzt 계열 · 정본 arzt1982_… 와 이웃)"* — 이 논문에 **기전 지도 그림은 없다** (서론이 앞선 *"pressure sintering diagrams [8, 14]"* 를 인용할 뿐 · p.1829).  같은 줄의 서지는 원문과 같다 (호 11 은 그 줄에 없음 · DOI 는 인쇄면에 없는 2 차 기록).  경미 · 고치지 않음.  후보 표 N-65 의 '왜' 칸도 같은 기대에서 왔다.
- `dixit2022_isostatic_pressing_ssb_large_scale_manufacturing_review` **L215** *"등방 = 벽 마찰 없음 → 같은 압력에서 평균 밀도 · 균일성 ↑ | [29] Radomir 2012 · [30] Swinkels 1983 · [31] du Plessis 2020 | p.3938"* — 이 논문 ([30]) 에 벽 마찰 · 밀도 균일성 · 같은 압력의 등방 ↔ 금형 대조 문장이 없다 (서론의 *"most models apply to isostatic pressing while most of the data are collected in die-pressing experiments"* 한 줄뿐).  리뷰의 귀속이고 그 카드는 리뷰를 그대로 옮겼다 — **카드 오류 아님 · 기록만**.
- `arzt1982_particle_coordination_densification_spheres` **L460** (그 원문 참고 [15] *"Metall. Trans. To be published."*) · **L453** ([8] *"Powder Metall. To be published."*) — 이 논문 참고 [37] = *Metall. Trans.* **14A**, 211 (1983) · [35] = *Powder Metall.* In press (정보 · 그 카드의 [미확인] 하나에 서지 실마리 · 고치지 않음).
- 그 밖에 확인한 2 차 인용 — 같음: `benhadjali2026_wip_vs_cup_…` L436 (서지) · `dixit2022_…` L459 (서지 · 호 11 포함) · L60 ([23] = [30]) · `arzt1982_…` L111 (HIP 크리프 축척 √a/(aZ)ⁿ = 이 논문 식 (24) 의 x^(1−2n)·n_f^(−n) [카드 산술]).

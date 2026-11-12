# 배치 55 정독 근거 (새 카드 1 장 · 원문에서 직접 · 2026-11-12)

카드 = `koenig2023_wet_milling_se_ion_tortuosity_composite_cathode` (원문 = 출판본 7 쪽 + SI 9 쪽 · 그림 크롭 53 장 = 도구 15 (다시 자름 2 · 그대로 13) +
손 크롭 38 (식 10 · 그림 5 패널 8 · 근거 문단 20) · 본 뒤 다시 렌더 2 · 판독 원자료 `litdb/figures/<slug>/digitized.csv` 82 행 — 본문 그림은 ≈300 dpi · SI 는 ≈220 dpi 원본 래스터 눈금 보정).
서지 (k · l 인용용) = König C., Miß V., Janin L., Roling B., *Mitigating the Ion Transport Tortuosity in Composite Cathodes of All-Solid-State Batteries by Wet Milling of the Solid Electrolyte Particles*,
ACS Appl. Energy Mater. 6 (18), 9356–9362 (2023), DOI 10.1021/acsaem.3c01242.
⚠ 재료 = SE **Li₅.₃PS₄.₃ClBr₀.₇ 유리-세라믹** (HDM · 열처리 없음 · ± LWM) — LPSCl 아님 · CAM 다결정 NCM85/10/5 (LiNbO₃) · **탄소 · 바인더 없음** · SOC50 · DEM · MPM · 압밀 시뮬레이션 없음 (실험만).
쪽 = PDF 쪽 (p.1 = 인쇄 9356 … p.7 = 9362) · SI p.n = S-n.

---

## a — 순수 SE 압력별 기공 곡선 · 진밀도 · 상태

- [a] koenig2023_wet_milling_se_ion_tortuosity_composite_cathode | **순수 SE 기공 · 압력 곡선 없음** — 펠릿 (100 mg · CompreCell · 392 MPa 90 s 제조 · 측정 중 98 MPa) 의 σ 만: σ₂₅°C **HDM 4.43 · LWM 1.09 mS/cm** (85 → 30 °C 측정 · 25 °C 는 외삽 — 카드 ln σ 맞춤이 같은 값을 다시 냄) · 30 °C 측정 ≈4.90 · ≈1.54 · 85 °C ≈18.1 · ≈16.2 | 카드 §3-2 · 원문 p.2–3 · SI 그림 S2 | [인쇄] · [판독] · [카드 산술] | Br 치환 유리-세라믹 · 펠릿 밀도 · 공극 [미확인]
- [a] koenig2023_… | 진밀도 표 (SI 표 S1): Li₆PS₅Cl **1.86** · Li₆PS₅Cl₀.₇₅Br₀.₂₅ 1.92 · Cl₀.₅Br₀.₅ 1.96 · Cl₀.₂₅Br₀.₇₅ 2.03 · Li₆PS₅Br 2.09 g/cm³ (출처: Cl = SI ref 1 Dewald 2019 · 혼합 = ref 2 Kraft 2017 · Br = ref 3 Yu 2019 — 그림 S4 캡션 위첨자 렌더 확인) · Li₅.₃PS₄.₃ClBr₀.₇ ≈**2.01** = 음이온 몰부피 규칙 ρ = 0.648·M/V_m (그림 S4 별 [판독] · 표 S2 역산 2.0095–2.0105 [카드 산술]) | 카드 §3-1 · SI p.3–4 | [인쇄] · [판독] · [카드 산술] | Li₆PS₅Cl 1.86 = **랩 표준 1.64 와 다른 문헌 값** (판정 아님)

## b — 압력을 뺄 때 되돌아오는 양 · 잰 방법

- [b] koenig2023_… | **없음** — 공극 펠릿 두께는 392 MPa 뒤 마이크로미터 캘리퍼 (하중 뺀 뒤로 읽힘 · 원문 명시 없음) · 되돌아옴 몫을 따로 재지 않음 · 대칭셀은 98 ↔ 392 MPa 를 오가지만 그 사이 두께 · 공극 측정 없음 | 카드 §3-3 · §3-5 · §4-4 | [인쇄] · [카드 해석] | —

## c — 항복 · 경도 · 크리프 값과 정의

- [c] koenig2023_… | **없음** (기계 물성 0 · 일축 항복 환산 없음) | 카드 §4-3 | — | —

## d — 단단한 + 무른 입자 혼합의 하중 몫 · 재밍

- [d] koenig2023_… | 하중 분담 값 없음 — 방향만: AM 몫이 클수록 392 MPa 공극이 크다 (70:30 9.4–11.1 → 85:15 20.2–21.3 % · 고체 중 SE 50.6 → 29.7 % [카드 산술]) · HDM 80:20 (22.7 %) > 85:15 (21.3 %) 비단조 (n = 1) | 카드 §3-3 · 원문 표 1 | [인쇄] · [카드 산술] | 한 압력 · 뺀 뒤

## e — 점접촉 법칙이 큰 변형에서 깨지는 범위와 대안

- 이 배치에 없음 (원문에 접촉 법칙 · 모델 없음).

## f — MPM 접촉 · 다물체 · 강체 결합 · 해상도

- 이 배치에 없음.

## g — 2D 결과를 3D 로 옮길 때의 경고 · 증거

- [g] koenig2023_… | 미세구조 근거가 **2D** — FIB-SEM/EDX 단면 (80:20 · 2 µm 막대) 과 SEM 분말 영상에서 낸 입도 누적 분포 (D50 · D95 · 입자 수 · 크기 정의 [미확인]) · 측정 (EIS · 두께) 은 3D 덩어리 · 2D → 3D 전이 말 없음 | 카드 §3-9 · §4-4 · 원문 p.5 · SI p.3 | [인쇄] · [카드 해석] | 2D 영상 입도 ≠ 3D 부피 분포

## h — DEM 에서 FE · MPM 으로 넘긴 선례 · 시점

- 이 배치에 없음.

## i — 복합 양극 (AM + SE) 의 압력별 기공

- [i] koenig2023_… | **한 압력 (392 MPa) · 조성별**: HDM SE 11.1 · 22.7 · 21.3 % ↔ LWM SE 9.4 · 13.5 · 20.2 % (70:30 · 80:20 · 85:15 wt% · NCM85 + Li₅.₃PS₄.₃ClBr₀.₇ · 탄소 없음) · 20 mg · ⌀10 mm PEEK · 스테인리스 피스톤 · **캘리퍼 두께 (뺀 뒤로 읽힘)** · 분모 = **추정 진밀도** (NCM 4.81 = NCM80/15/5 문헌값 · SE 2.01 = 규칙) · n = 1 · 두께 1 µm 반올림 → ±0.5 %p [카드 산술] — lei2026 의 "13.5 vs 22.7 %" = **80:20 한 쌍** (세 쌍 중 가장 큰 차이) | 카드 §3-3 · 원문 p.3 표 1 | [인쇄] · [카드 산술] | 압력 곡선 · Heckel 없음
- [i] koenig2023_… | ⚠ **같은 측정의 두 정의** — 식 (6) d = (V_solid/A)(1 + ε) · (8) ε = d·A/V_solid − 1 (인쇄 꼴) 과 SI 표 S2 'ε_void' (0.125 · 0.294 · 0.271 · 0.103 · 0.156 · 0.253) 는 **공극비 V_void/V_solid** · 본문 표 1 = 참 기공률 1 − V_solid/(d·A) (6/6 재현) | 카드 §3-4 · 원문 p.4 · SI p.5 | [카드 산술] | SI 표 S2 를 옮기면 공극 1.1–1.3 배 과대

## j — 카드가 스스로 적은 한계 (가압 · 탈압 계산과 닿는 것)

- [j] koenig2023_… | 공극 · 두께 · ε_SE 는 **따로 한 번 누른 20 mg 펠릿** (392 MPa) 의 값 — 대칭셀 속 양극은 392 MPa 두 번 + 98 MPa 단계 셋을 거침 → 같은 상태라는 근거 [미확인] · 대칭셀 EIS 때 적층압 · 온도 [미확인] · 진밀도 추정 | 카드 §3-5 · §13 | [인쇄] · [미확인] | —

## k — DEM 의 한계 (인용 서지 = König, Miß, Janin, Roling, ACS Appl. Energy Mater. 6 (2023) 9356–9362)

- [k] koenig2023_… (König 외 2023 · ACS Appl. Energy Mater.) | **DEM 에 대해 말 없음** (DEM · discrete element 낱말 0 회) · 계산 미세구조 일반에 대한 문장: *"Thus, the results of theoretical studies on computer-generated microstructures appear to underestimate the ion transport tortuosities in real composite electrodes of ASSBs."* (근거 = Bielefeld 2020 τ 5.0 @ ε_SE 0.3 · Yamakawa 2020 위상장 τ 11 @ 0.25) · LIB: *"this result has to be taken with caution since it was demonstrated that diffusion simulations can underestimate ion transport tortuosity as compared to values obtained from impedance spectroscopy"* (Ebner 2014 재구성 확산 모사 · 근거 ref 20) | 카드 §4-4 · 원문 p.2 | [인쇄] | Bielefeld 2020 = GeoDict 확률 배치 복셀 (DEM 아님 [다른 카드 `bielefeld2020_effective_ionic_conductivity_binder`]) · 실험 τ ↔ 계산 τ 의 정규화 · 정의 차를 원문이 따지지 않음

## l — 소성변형이 왜 어려운가 (인용 서지 = 위와 같음)

- [l] koenig2023_… (König 외 2023) | **말 없음** (계산 없음) — 재료 쪽 진술만: *"an inhomogeneous distribution of CAM and SE particles in the composite cathode as well as gaps between the particles can lead to bottlenecks or constrictivities for the ion transport as well as to barriers for the charge transfer at the interface between CAM and SE particles"* (p.1) · *"poor particle contacts can give rise to high values for ion transport tortuosity"* (초록) · 우회 · 맞춘 값 0 · 계산 비용 0 | 카드 §4-4 · 원문 p.1 | [인쇄] | —

## m — 받아들일 통찰

- [m] koenig2023_… | 무엇: **τ 정규화 함정** — 처리 (밀링) 가 SE 고유 σ 를 바꾸면 '자기 펠릿 기준 τ' 의 하락은 기하 이득이 아니다: ε_SE ≈0.235 에서 τ 35.4 → 8.0 (4.4 배) 중 로그로 ≈94 % 가 펠릿 σ₀ 4.43 → 1.09 (4.1 배) · 절대 σ_eff ≈0.029 → ≈0.032 mS/cm (+10 %) · ε_SE ≈0.45 에서는 ≈0.32 → ≈0.16 (−49 %) · 어디: 단계 7 · 흐름 밖: 수송 보고 규칙 (tau2 와 f · 절대 σ_ion · σ₀ 기준을 같은 줄에) · 왜: 카드 §3-8a · SI 그림 S2 | [카드 산술] | LWM 쪽 σ₀ 선택은 원문 [미확인] · 그림 S6 호 높이 근사로 1.09 (카드 §3-8b)
- [m] koenig2023_… | 무엇: **문헌 공극 정의 확인 규칙** — 표가 m · d · V_solid 를 주면 다시 계산해 참 기공률 ↔ 공극비를 가린다 · 어디: 단계 0 · 왜: 같은 논문 표 1 (참 기공률) ↔ 식 (6) · (8) · 표 S2 (공극비) (카드 §3-4) | [카드 산술] | —
- [m] koenig2023_… | 무엇: **우리 단분산 SE (⌀1.0 µm) 의 실험 짝은 LWM 분포** (D50 0.79 · D95 1.25 µm) — HDM 의 굵은 꼬리 (D95 3.17 · 최대 ≈7 µm ≈ CAM 3–6 µm) 는 우리 침대에 없다 → SE 입도 팔을 등록할 때 '굵은 꼬리' 팔을 따로 두고, 고유 σ 변화 (밀링 손상) 는 모형 밖 입력으로 분리 (Cronau(r_SE) 는 이 하락의 근거 아님) · 어디: 후보 D0 · 흐름 밖: 입도 설계 · 왜: SI 그림 S3 · 카드 §4-3 · §7-1 | [인쇄] · [판독] · [카드 해석] | 2D 입도
- [m] koenig2023_… | 무엇: **임피던스 R_ion 외삽 표지** — 문헌 R_ion 을 쓸 때 호가 실수축에 닿았는지 본다 (이 논문은 ε_SE ≲ 0.3 의 호가 10⁻⁴ Hz 에서도 열려 Warburg-short 외삽 · 꼭대기/R ≈0.32–0.33 → α ≈0.41) · 어디: 흐름 밖: 문헌 수송값 인용 · 왜: 그림 3 · S6 (카드 §3-7) | [판독] · [카드 산술] | —

## n — 논문 에이전트 후보 (원문 참고문헌 목록 서지 그대로)

- [n] Kroll, M.; Duchardt, M.; Karstens, S. L.; Schlabach, S.; Lange, F.; Hochstrasser, J.; Roling, B.; Tallarek, U. Sheet-type All-Solid-State Batteries with Sulfidic Electrolytes: Analysis of Kinetic Limitations based on a Cathode Morphology Study. J. Power Sources 2021, 505, No. 230064. | i · m — 같은 그룹 양극 형태 (SE 입경) ↔ 수송 한계 · König p.2 *"This observation is well in line with the works by Shi et al. and Kroll et al."* · 카드 §12 | litdb 확인: papers/ 에 kroll* 없음 · "Kroll" grep = 인용만 (cronau2022 · miss2026_pressure · pouraghajan2018 · yadav2021)
- [n] Yamakawa, S.; Ohta, S.; Kobayashi, T. Effect of Positive Electrode Microstructure in All-Solid-State Lithium-Ion Battery on High-Rate Discharge Capability. Solid State Ionics 2020, 344, No. 115079. | k · m — 위상장 계산 미세구조 τ_eff 11 @ ε_SE 0.25 = "계산 미세구조가 τ 를 과소평가" 진술의 근거 (König p.2) · 카드 §4-4 | litdb 확인: yamakawa* 없음 · "Yamakawa" grep = 다른 논문 공저자 줄뿐 (kamaya2011 · kato2018 · park2020 · sakka2022)
- [n] Cronau, M.; Paulus, A.; Pescara, L. P.; Kroll, M.; Renz, D.; Mekontso, J. A.; Marx, A.; Roling, B. What Limits the Rate Capability of Ultrathick Composite Electrodes in Lithium-Ion Batteries? A Case Study on the Thickness-Dependent Impedance of LiCoO2 Cathodes. Batteries Supercaps 2022, 5, No. e202200194. | k · m — *"diffusion simulations can underestimate ion transport tortuosity as compared to values obtained from impedance spectroscopy"* 의 근거 + 그림 4 LIB 띠 (König p.2 · p.5) | litdb 확인: cronau* = cronau2021_stack_pressure · cronau2022_wet_milling (다른 논문) · "e202200194" · "Ultrathick" grep 없음
- [n] Dewald, G. F.; Ohno, S.; Kraft, M. A.; Koerver, R.; Till, P.; Vargas-Barbosa, N. M.; Janek, J.; Zeier, W. G. Experimental Assessment of the Practical Oxidative Stability of Lithium Thiophosphate Solid Electrolytes. Chem. Mater. 2019, 31, 8328–8337. | a — SI 표 S1 Li₆PS₅Cl 진밀도 **1.86 g/cm³** 의 출처 (랩 표준 1.64 와 다른 문헌 값의 원전 확인) | litdb 확인: dewald* 없음 · "Dewald" grep = 인용만 (banik2022 · korjus2025 · minnmann2021 · taklu2021 · wu2026 · yang2025)
- [n] Miß, V.; Ramanayagam, A.; Roling, B. Which Exchange Current Densities Can Be Achieved in Composite Cathodes of Bulk-Type All-Solid-State Batteries? A Comparative Case Study. ACS Appl. Mater. Interfaces 2022, 14, 38246−38254. | m (흐름 밖) — 같은 그룹 복합 양극 교환 전류 · SOC0 NCM 전자 σ > 1 mS/cm 근거 (König ref 33) | litdb 확인: miss2022* 없음 · "38246" grep 없음

## 카드 문제

1. (원문 · 카드 §3-4) 식 (6) · (8) 의 인쇄 꼴과 SI 표 S2 'ε_void' = **공극비** · 본문 표 1 = **참 기공률** (6/6 [카드 산술]) — 같은 측정에 두 정의.
2. (원문 · 카드 §3-8c) 본문 R_ion (22.6 · 347 Ω cm²) · 두께 (87 · 83 µm) · ε_SE (0.450 · 0.234) 와 τ (6.3 · 35.4) 가 식 (5) · (9) 로 맞지 않음 — σ₀ · 단위 무관 비 8.37 ↔ 인쇄 5.62 [카드 산술].
3. (원문 · 카드 §3-8) LWM 순수 펠릿 σ 하락 (×0.25) 을 본문에서 다루지 않음 · 식 (9) 에 넣은 σ₀ 값 · 대칭셀 EIS 온도 · 압력 미기재.
4. (원문 · 카드 §3-10) *"see Figure S4"* (LWM 스펙트럼) = 실제 그림 S6 · NCM 밀도 문장 방향이 바뀜 (NCM80/15/5 ↔ NCM85/10/5) · 인라인 Warburg 식 (iωβ) ↔ 식 (4) (iωτ) · 그림 4 범례 'HDM: Park' (Park LPSCl = 볼밀 + 550 °C 어닐 [다른 카드]) · Kaiser 인용 'from 0.63' (정본 카드 0.665).
5. (다른 카드) `wolf2026_extruder_vs_batch_mixing_core_shell_dry_sulfide_cathode` L348 *"복합 양극 이온 tortuosity 를 SE 습식 분쇄로 낮춤"* — 방향 맞음 · σ₀ 정규화 한정어 없음 (절대 σ_eff 는 ε_SE 0.235 에서 거의 같음 [카드 산술]) — 고치지 않음 · 보고만.
6. (다른 카드) `lei2026_se_particle_size_effects_review` L267 *"LWM 공극 13.5 vs 22.7 %"* — 값 맞음 · 80:20 · 392 MPa · 캘리퍼 + 추정 진밀도 조건과 '세 쌍 중 가장 큰 차이' 한정이 없음 — 보고만.
7. (후보 표 S8 · N-13 '왜' 칸) *"lei2026 L238 = König 가 ε_SE 0.237 을 tortuosity 처럼 적었다는 표기 문제"* — 주어가 틀림: König 원문은 τ_eff 8.0 과 ε_SE 0.237 을 언제나 따로 적었고, lei2026 L238 은 **리뷰 (Lei 2026) 의 옮김 결함**을 옳게 적은 줄이다.

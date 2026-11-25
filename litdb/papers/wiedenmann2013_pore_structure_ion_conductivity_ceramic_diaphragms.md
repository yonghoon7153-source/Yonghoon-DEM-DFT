<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · τ 묶음 형식 기준 = tjaden2018_… · landesfeind2016_… · taufactor_… · 같은 날 앞 묶음 10 장
     (특히 자매 논문 holzer2013_… — 이 논문의 격막 8 시료를 β–δ 관점에서 다시 쓴 후속, 이 논문 ref 24).
     이 논문은 시뮬레이션이 아니라 *3D 영상 서술자 (SRµCT) + EIS + 매개변수 모형* 논문이다 → §4 = 정의식 · 측정 사슬, §8 = "M-factor 식과 지수의 원전".
     쪽 표기 = 학술지 인쇄 쪽 (AIChE J. 59(5)).  PDF n 쪽 = 인쇄 (1445 + n) 쪽 → PDF 1 = p.1446 … PDF 12 = p.1457.  식 · 표 · 그림 번호 = 원문 번호.
     SI 없음 (본문이 SI 를 인용하지도 않는다).
     수식 · 표 · 그림이 든 쪽 (p.1447–1449 · p.1451–1456) 은 원문을 렌더해 읽었다 (텍스트 추출은 τ→s · ε→e · β→b · σ→r · δ→d 로 깨뜨린다).
     Table 1 · 2 는 렌더와 텍스트 추출이 글자 단위로 일치한다.
     값 표지: stated = 본문 · 표 · 캡션 원문 / 판독 = 그림에서 눈으로 읽은 값 (≈ · 추세 전용) / 우리 산술 = 원문 표값으로 카드 작성자가 계산한 값 (식 명시 · 원문 값 아님). -->
# Three-Dimensional Pore Structure and Ion Conductivity of Porous Ceramic Diaphragms — 단층촬영 기하 τ_geo · constriction factor β 와 EIS σ_eff 를 맞대는 "확장 기공 구조 모형" σ_eff/σ₀ = ε·β/τ_geo (지수 전부 1 · 맞춤 0) = Landesfeind Eq 4 N_M 의 원식 — Wiedenmann (AIChE J. 2013)
> slug `wiedenmann2013_pore_structure_ion_conductivity_ceramic_diaphragms` · DOI `10.1002/aic.14094` · type `exp + 3D image analysis (tortuosity · constriction · porosity microstructure — SRµCT 740 nm · skeleton Dijkstra τ_geo · c-PSD / MIP 모사 β · 4-전극 impedance (EIS) σ_eff — 25 wt% KOH 함침 소결 세라믹 격막)` · PDF `21. Three‐dimensional pore structure and ion conductivity of porous ceramic diaphragms.pdf` · digested `2026-10-03` · status ✅
>
> ★ **판정 요약 (이 카드의 목적 = M-factor 식과 지수의 원전)** — 원문에 **"M-factor" 라는 이름은 없다**.  있는 것은 **Eq. 11 σ_eff/σ₀ = ε·β/τ_geo** (p.1448) — 저자가 "extended pore structure model" 이라 부르는 식 (초록 p.1446 · 결론 p.1456) — 이고 **ε · β · τ_geo 의 지수가 전부 1, 맞춘 매개변수 0** (*"… tortuosity (τ) and constriction factor (β), but no fitting parameters"*, p.1446).  τ_geo 1 승은 경험 지수가 아니라 **균일 관 모형의 유도 (Eq. 4–7) 를 그대로 옮긴 것**이다 (Eq. 5 가 관 단면 합을 시료 단면의 기공 면적 εA 로 둔다).
> ⇒ Landesfeind 2016 Eq. 4 `N_M ≡ τ̄_geo/(ε·β)` 는 Eq. 11 의 **정확한 역수** → 메모 v2 §8-2 의 **"τ_geo 지수 [미확인]" 은 닫힌다: 1 승**.  원문의 'm-factor' 는 Archie 지수 m (Eq. 8: olivine **2.31** · wollastonite **2.95**, 계열당 4 시료) — M-factor 와 다른 양.  경험 지수가 붙은 ε^a·β^b/τ^c 꼴은 **이 논문에도 없다** (자매 논문 Holzer 2013 카드도 "없다").
> τ 는 셋이다: **τ_elc = ε_tot·σ₀/σ_eff** (Eq. 6, 'electric tortuosity') = **우리 tau2** · **τ_geo** = 기공 skeleton 선 그래프의 Dijkstra 최단 경로 ÷ **시료 입방체 길이 L**, **모든 source–sink 쌍의 평균** (p.1452) = **우리 τ_geo** · Eq. 3 τ = l_eff/L 은 원문이 Carman 을 따라 **'tortuosity factor'** 라 부른다 (p.1447) — 우리 규칙 ('tortuosity factor' = tau2 전용) 과 **이름이 정반대**다.
> 협착도 둘이다: **β_geo = (r_min/r_max)²** (Eq. 9–10, 'constriction factor', 영상 직접 — r_min = MIP 모사 PSD 의 r50, r_max = c-PSD 의 r50) ↔ **δ_elc = σ_eff·τ_geo/(σ₀·ε_tot)** (Eq. 12, 'electric constrictivity', EIS 역산).  Table 1: β_geo 0.42–0.67 ≠ δ_elc 0.32–0.91.
> EIS 대조 (Table 1 · 그림 7): 측정 σ 0.031–0.254 ↔ Eq. 11 계산 0.040–0.186 S/cm — 원문 판정 *"remarkably well"* · R² · 오차 통계는 **없다** · 측정/계산 **0.74–1.37** (우리 산술, 8 점).
> ⇒ 결정 11 (CF = "모델 내부 기준선" · FULL/CF = "모델 내부 협착 비") 은 **이 틀과 맞는다 — 권고 유지** (§8).
>
> ⚠ **자매 논문 Holzer 2013 과 같은 8 시료인데 두 값이 다르다** (ε · σ_eff · τ_elc · r_min · r_max · β 는 같다): ① **τ_geo** — 이 원문 1.62–1.87 (평균 **1.77**) ↔ Holzer 평균 **1.62** (6/8 시료에서 이 원문이 10–14 % 높다 → δ 도 다르다) ② **Archie m 재료 배정** — 이 원문 olivine 2.31 · wollastonite 2.95 (**자료와 맞다**) ↔ Holzer 카드가 적은 Holzer p.2948 배정은 뒤바뀜.  §10.
> ⚠ 범위: **25 wt% KOH (액체) 가 채운 소결 세라믹 기공** · 8 시료 · 고체 전해질 · 입자 접촉 저항 · 수송 시뮬레이션 **없음**.

---

## 0. 결론 먼저 (메인이 물은 것 → 답)

| 질문 | 답 | 근거 (식 · 쪽) |
|---|---|---|
| 이 논문의 M-factor 식은? 경험 지수가 있나? | **"M-factor" 이름 없음.**  구조–전도 식은 **Eq. 11 σ_eff/σ₀ = ε·β/τ_geo** 하나 — 지수 전부 1, 맞춘 매개변수 0.  원문의 'm-factor' (결론 p.1456 "empirically derived m-factor") = Archie 지수 m | Eq. 11 (p.1448) · 초록 (p.1446) · 결론 (p.1456) |
| τ_geo 1 승은 어디서 왔나 | **균일 관 모형** (같은 길이 l_eff · 일정 지름 d 의 관, Eq. 4) + **Eq. 5 A_p = (π/4)Σd² = εA** → σ_eff/σ₀ = ε/τ (Eq. 6–7) → "adding the constriction factor (β) into Eq. 7" (Eq. 11).  경험값이 아니라 유도식의 지수 — 관이 τ 배 길어진 만큼의 기공 부피를 Eq. 5 가 세지 않는 데서 1 승이 남는다 (카드 작성자 해석 · §4-1) | Eq. 4–7 · Eq. 11 (p.1448) |
| Landesfeind Eq. 4 와 같은 식인가 | **같다** — N_M = σ₀/σ_eff = τ_geo/(ε·β) 는 Eq. 11 의 정확한 역수.  τ̄ (평균) 표기도 원문 τ_geo = 전 경로 평균 (Table 2) 과 맞다 ⇒ **τ_geo 지수 = 1 (닫힘)** | Eq. 11 · Table 2 (p.1452) · `landesfeind2016_…` Eq. 4 행 (A1374) |
| 맞춘 자료 · 적용 범위 · R² | **8 시료** (olivine 4 · wollastonite 4) · ε_tot 0.27–0.80 · β_geo 0.42–0.67 · τ_geo 1.62–1.87 · 액체 25 wt% KOH.  **R² · 오차 통계 없음** (*"remarkably well"* · *"excellent correspondence"*).  측정/계산 0.74–1.37, 평균 0.95 (우리 산술).  Archie m 은 계열당 4 점 log F–log ε_tot 직선 (그림 6a · (1, 1) 통과) — R² 미보고 (*"almost perfect linear trends"*) | Table 1 (p.1449) · 그림 6–7 · p.1454 |
| τ 는 기하 τ 인가 τ² 인가 | Eq. 11 의 τ = **τ_geo** (경로 길이 비 · 기하 · 1 승).  **τ_elc = ε σ₀/σ_eff** (Eq. 6) 는 값으로 **우리 tau2** 다 — 원문 이름은 'electric tortuosity' (factor 없음).  'tortuosity factor' 라는 이름은 원문이 **기하 τ = l_eff/L** (Eq. 3, Carman) 에 붙인다 | Eq. 3 (p.1447) · Eq. 6 (p.1448) · Table 1 |
| 정규화 (부피 · 단면 · σ₀) | ε = **ε_tot** = 단층촬영 c-PSD 기공률 (MIP 모사가 같은 총기공률 → *"entirely percolating … no isolated pores"*) · **σ₀ = 순수 25 wt% KOH 0.645 S/cm** (구조 없음 · Table 1 'KOH' 행 F = m = τ_elc = τ_geo = ε = 1) · σ_eff = 4-전극 EIS 의 순수 저항 R 을 시료 단면 A · 두께 L 로 (Eq. 6 · 원판 Ø 20 mm × 2.5 mm) · M 에 해당하는 양 = σ_eff/σ₀ = 1/F | p.1448–1449 · p.1453 |
| β 의 정의 · 측정법 | β = A_min/A_max = πr²_min/πr²_max (Eq. 9–10) = Petersen [12] 협착 인자의 역수 → 0–1.  **r_min = MIP 모사 PSD 의 r50** (병목 · 돌파 반경), **r_max = c-PSD 의 r50** (거품).  재현성: 기공 부피 · r50 의 SD 4–10 %, 대개 < 5 % [19] | p.1448 · p.1451 |
| "no fitting parameters" 의 범위 | **Eq. 11 계산 (σ_β) 에만** 해당.  Archie m (계열별 맞춤) · τ_elc–ε 의 로그 맞춤 (Comiti–Renaud [23], 식 · 계수 미인쇄) · Eq. 13–16 (맞춘 m 사용) 은 맞춤 · 서술이다.  후속 Holzer 2013 [24] 은 같은 자료에서 β 대신 **맞춘 사인식 δ_geo(β)** 를 넣었다 (`holzer2013_…` Eq. 9–10) | p.1446 · p.1454–1455 · Holzer 카드 |
| EIS σ_eff 와의 대조 결과 | 측정 0.031–0.254 ↔ 계산 0.040–0.186 S/cm.  **6/8 은 계산이 측정보다 높다** (저항 과소 −2 … −26 %) · ol 4 +14 % · wo 4 +37 % (우리 산술).  σ_EIS/σ_β = δ_elc/β_geo 이므로 이 무늬는 "β ≠ δ" 그 자체다 — 후속 Holzer 의 "β 판은 저항을 과소 예측" 과 **같은 무늬** (크기만 다름: τ_geo 집합이 다르다) | Table 1 · 그림 7 (p.1454) |
| Landesfeind · Holzer 카드가 이 논문을 옮긴 문장은 원문과 같은가 | Landesfeind Eq. 4 = 원식 그대로 (τ̄_geo 1 승) ✓.  Holzer 카드: ① Archie m 배정 (olivine 2.95 · wollastonite 2.31) 은 원 논문과 **반대** ② τ_geo 평균 1.62 ↔ 원 논문 1.77 ③ ε 정의 · σ_eff 정규화 [미확인] 은 이 원문으로 닫힘 (§10) | §10 |
| 결정 11 · TAU-07 · TAU-08 이 이 틀과 맞나 | **맞는다 — 권고 유지.**  원문의 무협착 기준 = 균일 관 모형 (β = 1, τ_elc = τ_geo ≥ 1) · 협착 양 = β_geo (기하) · δ_elc (EIS 역산, 기준 = τ_geo).  FULL/CF 는 기준이 CF 라 어느 쪽도 아니다 · 아래 첨자 'geo' 는 영상 기하 양에만 붙는다 | §8 |

---

## 1. 한 줄 요약
알칼리 수전해의 석면 격막을 대신할 **소결 세라믹 격막** (등축 olivine · 섬유상 wollastonite, ε 0.27–0.80) 을 **싱크로트론 X선 흡수 단층촬영 (740 nm)** 으로 재구성해 기공 구조를 세 서술자 — **ε_tot · 기하 τ_geo (skeleton Dijkstra) · constriction factor β_geo = (r_min/r_max)² (MIP 모사 r50 ÷ c-PSD r50)** — 로 재고, 같은 격막의 **4-전극 EIS 이온 전도도** (25 wt% KOH) 를 **맞춤 없는 Eq. 11 σ_eff/σ₀ = ε·β/τ_geo** 로 예측해 맞댄 논문이다.  핵심 관측: **τ_geo 는 ε 와 무관하게 1.62–1.87 로 평평한데 EIS 역산 τ_elc 는 2.0–5.6** — 그 격차는 경로 길이가 아니라 **병목 (협착)** 에서 온다고 결론한다.  우리에게는 **Landesfeind N_M = τ̄_geo/(εβ) 의 원식 (τ_geo 1 승 · 맞춤 0)**, **기하 협착 β ≠ 수송 협착 δ** 의 원자료, 그리고 **"모든 출입 쌍 ÷ 시료 길이" 라는 τ_geo 규약** (우리 τ_Dij · 벽 τ 와 같은 계열) 을 원문으로 준다 (수치는 액체 격막이라 전이 불가).

## 2. 메타
| 저자 | 저널/년 | DOI | 재료계 | 연구유형 |
|---|---|---|---|---|
| **D. Wiedenmann** (교신 · Univ. Fribourg, Dept. of Geosciences and FRIMAT), L. Keller (EMPA), **L. Holzer** (ZHAW ICP), J. Stojadinović, B. Münch, L. Suarez, B. Fumey, H. Hagendorfer, R. Brönnimann (EMPA), P. Modregger (Swiss Light Source, PSI · School of Biology and Medicine, Univ. Lausanne), M. Gorbar, U. F. Vogt, A. Züttel (EMPA), F. La Mantia (CES, Ruhr-Univ. Bochum), R. Wepf (ETH Zürich EMEZ), B. Grobéty (Univ. Fribourg) — 16 명 | **AIChE J. 59(5), 1446–1457 (May 2013)** — 'AIChE Letter: Transport Phenomena and Fluid Mechanics' | **10.1002/aic.14094** | 소결 세라믹 격막 (olivine · wollastonite) + 탄소 기공 형성제 · 기공 = **25 wt% KOH** (EIS) / 에폭시 (단층촬영) | **실험 + 3D 영상 분석 + 매개변수 수송 모형** (수송 시뮬레이션 없음) |

- 접수 2012-08-25 · 수정 2012-12-26 · 온라인 2013-04-01 (Wiley).  © 2013 American Institute of Chemical Engineers.  오픈액세스 표기 없음 (PDF 바닥글의 CC 문구는 Wiley 일반 문구).
- 연구비: Swiss Federal Commission for Technology and Innovation (CTI, project no. 8574.2 PFIW-IW) · Industry High Technology Ltd. (IHT) · 스위스 주 정부 · Univ. Fribourg · 일부 CIBM (UNIL · UNIGE · HUG · CHUV · EPFL) · Leenaards · Jeantet 재단.
- 배경: 많은 나라에서 금지된 **chrysotile 석면 가스 분리 격막** (알칼리 수전해) 의 대체재 프로젝트 (p.1449).
- 이 논문을 인용하는 정본 카드: `holzer2013_constrictivity_effective_transport_porous_layers` (ref [37], "(2012) AIChE J (in press)" — 같은 격막 자료를 β–δ 관점에서 재평가) · `landesfeind2016_tortuosity_eis_electrodes_separators` (ref [10], Eq. 4 의 constriction factor 출처 · τ̄_geo 의 "graph theory") · `tjaden2018_tortuosity_review_calculation_approaches` (ref [14]).
- 이 논문의 ref 24 = Holzer 2013 (J Mater Sci 48:2934–2952) — 단 **제목이 다르게** 적혀 있다 (§10 원문 대조 ⑬).

---

## 3. 핵심 수치
> 이 논문은 우리 소재 앵커 (porosity@P · σ_ion/e/thermal (고체) · E_SE · coverage · Z · Heckel) 를 **주지 않는다** → 전부 n/a.  주는 것은 ① 정의식 (§4-1) ② 격막 8 시료의 ε · τ_geo · τ_elc · β · δ · σ (Table 1 · 2, **본문 명시값**) ③ 측정 조건.

### 3-A. 본문 명시값 (stated, 쪽 순)
| 항목 | 값 | 조건 / 시료 | 쪽 |
|---|---|---|---|
| 격막 성형 | olivine (North Cape Minerals) 또는 wollastonite (Mial) 분말 + 탄소 기공 형성제 (Sigradur, HTW) + PVA 결합제 (Optapix PA 4 G, 20 wt% 수계) → 볼밀 혼합 → **일축 20 MPa** → Ø 50 mm × 약 4 mm → **1300 °C · 1 h** 소결 (승온 1 K/min · 냉각 3 K/min).  기공 형성제 비율 값은 미기재 [미확인] | 두 계열 | p.1449 |
| EIS 시편 | 연삭 · 연마로 **Ø 20 mm × 2.5 mm** · 25 wt% KOH (caustic potash) 로 점진 함침 | 8 시료 | p.1449 |
| EIS | 차분 저항법 [13] · **4-전극 셀** · **100 kHz – 0.1 Hz** · potentiostatic · Zahner IM6eX · 격막 없을 때 기준–감지 전극 간격 **64 mm** · 감지–기준 사이 **0.75 V + 10 mV AC** · 절연 격막이라 스펙트럼 = 실수부 Z′ 만 → **순수 저항** | — | p.1449 |
| 측정 온도 | **미기재** [미확인] | — | — |
| σ₀ (KOH) | **0.645 S/cm** — Table 1 'KOH' 행 (F 1.00 · m 1.00 · τ_elc 1.00 · τ_geo 1.00 · ε_tot 1.00 · ε_eff 1.00) | 25 wt% KOH | p.1449 |
| 단층촬영 시편 | 에폭시 (Araldit BY158 / Aradur21, Huntsman) 냉간 함침 — 20 mbar → 50 min 뒤 2 bar · 80 °C 12 h 경화 · 레이저 절단 **Ø 700 µm** 원기둥 | — | p.1449 |
| SRµCT | SLS **TOMCAT** (PSI) · 흡수 대비 · **15.5 keV** · 시야 0.78 mm · 1601 투영 → 2048 장 × 2048² px · 화소 **370 nm** | — | p.1449 |
| 분할 · 부분부피 | Avizo · 2048³ → 입방 부분부피 크롭 · 다운샘플 · median 필터 · 3D 문턱 이진화 → **660³ voxel @ 740 nm** (= 모서리 **488 µm**, 그림 5) · *"segmentation by 3-D thresholding can represent a significant source of errors"* [16] | — | p.1450 · p.1453 |
| PSD 재현성 | 기공 부피 · r50 의 SD **4–10 %**, 대개 **< 5 %** [19] | 방법 | p.1451 |
| ε_tot 범위 | olivine **0.27–0.44** · wollastonite **0.45–0.80** (c-PSD 기공률) · olivine 은 ε > 0.44 면 소결 중 붕괴 | — | p.1453 |
| 고립 기공 | MIP 모사가 같은 총기공률 → *"entirely percolating pore structures, that is, there are no isolated pores"* | 8 시료 | p.1453 |
| τ_geo | **1.62–1.87** (*"within a narrow range"*) · ε 와 무관 · 평균 **1.77** (그림 8c 기울기 서술 · 그림 6c 서술) | 8 시료 | p.1454 · p.1456 |
| Archie m | **olivine 2.31 · wollastonite 2.95** — 같은 ε_tot 에서 olivine 이 더 잘 전도 | 계열당 4 점 | p.1449 · p.1454 |
| ε_max (δ = 1 이 되는 기공률, Eq. 14) | **olivine 0.65 · wollastonite 0.75** | Archie m + τ_geo | p.1455 |
| wo 4 | *"the measured τ_elc and τ_geo are almost identical"* (2.02 · 1.84) · δ_elc 0.91 *"close to 1"* | ε 0.80 | p.1454 · p.1455 |
| 그림 8 오차 막대 | ε_tot 의 **5.0 %** (추정) · δ_elc 의 **7.1 %** · ε_eff 의 **8.7 %** | — | p.1455 |
| σ_ion · σ_e · κ_th (고체) · porosity@P · E_SE · coverage · Z · Heckel | **n/a** | — | — |

### 3-B. Table 1 (p.1449) · Table 2 (p.1452) — 전사 (stated)
| 시료 | σ EIS [S/cm] | σ_β tomo [S/cm] | F (Archie) | m | τ_elc (EIS) | δ_elc (EIS) | τ_geo (tomo) | r_min [µm] (MIP r50) | r_max [µm] (c-PSD r50) | β_geo | ε_tot | ε_eff (EIS) | 경로 수 n (Table 2) | τ_geo SD (Table 2) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| KOH | 0.645 | – | 1.00 | 1.00 | 1.00 | – | 1.00 | – | – | – | 1.00 | 1.00 | – | – |
| ol 1 | 0.031 | 0.040 | 20.98 | 2.31 | 5.61 | 0.32 | 1.82 | 1.87 | 2.87 | 0.42 | 0.27 | 0.09 | 398522 | 0.17 |
| ol 2 | 0.047 | 0.052 | 13.72 | | 4.42 | 0.42 | 1.87 | 2.57 | 3.74 | 0.47 | 0.32 | 0.14 | 298991 | 0.17 |
| ol 3 | 0.074 | 0.092 | 8.70 | | 3.63 | 0.49 | 1.77 | 3.74 | 4.80 | 0.61 | 0.42 | 0.20 | 193610 | 0.17 |
| ol 4 | 0.106 | 0.093 | 6.11 | | 2.71 | 0.64 | 1.74 | 4.32 | 5.74 | 0.57 | 0.44 | 0.28 | 129890 | 0.16 |
| wo 1 | 0.063 | 0.085 | 10.24 | 2.95 | 4.63 | 0.38 | 1.76 | 2.40 | 3.30 | 0.53 | 0.45 | 0.17 | 419079 | 0.16 |
| wo 2 | 0.092 | 0.099 | 7.04 | | 3.67 | 0.47 | 1.74 | 2.98 | 4.02 | 0.55 | 0.52 | 0.25 | 303893 | 0.15 |
| wo 3 | 0.140 | 0.143 | 4.62 | | 2.71 | 0.60 | 1.62 | 3.71 | 4.52 | 0.67 | 0.59 | 0.35 | 196060 | 0.10 |
| wo 4 | 0.254 | 0.186 | 2.54 | | 2.02 | 0.91 | 1.84 | 9.14 | 11.51 | 0.63 | 0.80 | 0.73 | 60269 | 0.24 |

- Table 1 각주 (원문): σ = EIS 측정 · 단층 매개변수로 계산 · F = Archie formation factor · m = series-specific constant · τ_elc = electric tortuosity · δ_elc = electric constrictivity · τ_geo = geometric tortuosity · r_min = MIP-PSD 의 50 vol % 반경 · r_max = c-PSD 의 50 vol % 반경 · β_geo = constriction factor · ε_tot = total porosity · ε_eff = effective porosity.
- Table 2 제목: *"Average Values of Geometric Tortuosities (τ_geo) in the z Direction, Amount of Considered Pore Paths (n) and Standard Deviations (SD)"* — τ_geo 값은 Table 1 과 같다.

### 3-C. 원문 안의 수치 정합 검사 (우리 산술 · Table 1 값만 씀)
| # | 검사 | 결과 |
|---|---|---|
| ① | F = σ₀/σ_EIS (σ₀ 0.645) | 8/8 반올림 안 (최대 차 ol 1 20.81 vs 20.98 = 0.8 %) → **F 의 기준은 순수 KOH σ** |
| ② | τ_elc = ε_tot·F (= ε_tot σ₀/σ_eff, Eq. 6) | 8/8 차 ≤ 1 % (ol 1 5.66 vs 5.61) → **τ_elc = 우리 tau2 식 그대로**, φ 자리 = ε_tot |
| ③ | δ_elc = τ_geo/τ_elc (= Eq. 12) | 8/8 차 ≤ 0.005 |
| ④ | ε_eff = τ_geo·σ_EIS/σ₀ (= Eq. 15 ∘ Eq. 12 = ε_tot·δ_elc) | 8/8 차 ≤ 0.006 → **표의 ε_eff 는 측정 σ 에서 나온 양** (Eq. 17 의 기하 정의로 잰 것이 아니다 — §10 ⑪) |
| ⑤ | β_geo = (r_min/r_max)² (Eq. 10) | 8/8 차 ≤ 0.004.  1 승 비 r_min/r_max 이면 0.65–0.82 → 표는 **제곱** (p.1454 본문 "the ratio (r_min/r_max) then gives …" 는 느슨한 표현 — §10 ③) |
| ⑥ | σ_β = σ₀·ε_tot·β_geo/τ_geo (Eq. 11) | ol 1–4 · wo 1 은 차 ≤ 2.8 % · **wo 2 +7.1 % · wo 3 +10.1 % · wo 4 −5.0 %** (재계산/표) — σ_β 에 쓴 입력값은 원문에 따로 없다 [원인 미확인] |
| ⑦ | 측정/계산 σ_EIS/σ_β | 0.775 · 0.904 · 0.804 · **1.140** · 0.741 · 0.929 · 0.979 · **1.366** → **0.74–1.37, 평균 0.95**.  = δ_elc/β_geo (Eq. 11 ÷ Eq. 12) 와 반올림 안에서 같다 |
| ⑧ | 같은 식을 **τ_geo²** 로 바꾸면 (σ₀εβ/τ_geo²) | 측정/계산 **1.27–2.65** (평균 1.67) — 원문 1 승 (0.74–1.37) 보다 크게 어긋난다.  ⚠ 이 판정은 τ_geo 의 정규화 (÷ L · 모든 쌍) 에 묶여 있다 |
| ⑨ | Archie m (ε_tot · F, (1, 1) 통과 log 맞춤) | olivine **2.33** · wollastonite **2.98** = 본문 2.31 · 2.95 와 맞다 (재료 배정 포함).  자유 절편 맞춤이면 olivine 2.28 (전인자 1.05) · wollastonite 2.43 (1.42) — 그림 6a 직선은 (1, 1) 을 지난다 |
| ⑩ | Eq. 14 ε_max = τ^(1/(1−m)) | τ = **1.77** (8 시료 평균) 이면 olivine 0.647 · wollastonite 0.746 = 본문 0.65 · 0.75.  어느 τ 를 넣었는지는 미기재 |
| ⑪ | τ_elc/τ_geo (= 1/δ_elc, 선형 '협착 배수') | **1.10–3.08** — 8/8 ≥ 1 (δ_elc ≤ 1) |
| ⑫ | √τ_elc/τ_geo (웹앱 "Constriction overhead" 꼴) | **0.77–1.30** — ol 4 **0.95** · wo 4 **0.77** 가 1 아래 (둘 다 δ_elc < 1 인 협착 기공망) |
| ⑬ | Bruggeman 배수 τ_elc·ε_tot^½ | **1.80–3.11** (액체 격막) |
| ⑭ | τ_geo 평균 (8 시료) | **1.770** = 본문 1.77 |
| ⑮ | 대표 부피 비 (부분부피 모서리 488 µm ÷ r_max) | 42 (wo 4) – 170 (ol 1) |

### 3-D. 그림 판독 (≈ · 추세 전용)
- 그림 6c: 두 τ_elc 추세 곡선 (olivine · wollastonite) 은 **ε_tot = 1.0 에서 τ ≈ 1 로 만난다** — 본문 *"close to 1.77"* 과 어긋난다 (§10 ④).
- 그림 4b · d (wollastonite PSD): **실선 · 점선 쌍이 다섯** (평탄부 ≈ 80 % 자홍 · ≈ 75 % 파랑 · ≈ 59 % 초록 · ≈ 52 % 빨강 · ≈ 45 % 검정) 인데 범례는 넷 (wo 1–4, wo 4 = 파랑).  Table 1 의 wo 4 (ε 0.80 · r_max 11.51 · r_min 9.14) 와 맞는 것은 **자홍** 곡선이다 (§10 ⑦).
- 그림 7: 7 점이 1:1 선 근처, **wo 4 (계산 0.186 → 측정 0.254)** 만 선 위로 크게 벗어난다.
- 그림 8c: 두 계열이 한 직선 (기울기 ≈ σ₀/1.77 = 0.364 S/cm, 우리 산술) 위 — 구성상 그렇게 된다 (§10 ⑪).

---

## 4. 정의 · 방법 (정독) ★
> DEM 양식의 "시뮬레이션 방법" 칸 (code · 접촉법칙 · E·ν·μ · 서보 · RVE · seed) 은 **해당 없음** — 실측 소결체의 3D 영상 + EIS + 대수 모형이다.  아래는 정의식 → 측정 사슬 → 논증 순서.

### 4-1. 정의식 — 원문 식 번호 · 쪽 그대로
| 식 | 원문 형태 | 쪽 | 원문 이름 · 뜻 |
|---|---|---|---|
| **Eq. 1** | u = ε³Δp/(kηS²L) | p.1447 | Carman 의 유량식 (Darcy · Blake [11] · Kozeny [6]) — S 기공 표면 · η 점도 · k Kozeny 상수 |
| **Eq. 2** | k = τ²k₀ | p.1447 | Kozeny 상수 = **τ² ×** 모양 인자 k₀ (Carman [3]) — 이 논문에서 τ² 가 나오는 유일한 자리 (투과율) |
| **Eq. 3** | τ = l_eff/L | p.1447 | ★ 원문 이름 **"tortuosity factor"** — 유효 기공 경로 길이 ÷ 시료 길이 (유동 방향).  *"Wyllie and Rose proposed the derivation of Carman's tortuosity factor from conductivity measurements"* |
| **Eq. 4** | G = σ₀π/(4τL)·Σd² | p.1448 | **균일 관 모형** (uniform tortuosity model [4,7,8]): 모든 기공 경로 = 같은 길이 l_eff 의 원관 · 경로 안 지름 d 일정 · 비전도 기지 |
| **Eq. 5** | A_p = (π/4)Σd² = εA | p.1448 | 관 단면 합 = 기공률 × 시료 단면.  ⚠ 카드 작성자 해석: 관이 길이 τL 이면 기공 부피는 (π/4)Σd²·τL 이라 ε = τ·(π/4)Σd²/A 가 된다 — Eq. 5 는 이 τ 를 세지 않는다.  그 결과 G = σ₀εA/(τL) 로 **τ 1 승** 이 남는다 (부피를 세면 ε/τ², Epstein 의 "경로 + 속도 변화" 꼴 — `tjaden2018_…` p.48 경유) |
| **Eq. 6** | τ_elc = σ₀RεA/L = σ₀ε/σ_eff | p.1448 | **electric tortuosity** — 단면 A_p 를 모르고도 R (또는 σ_eff) 와 ε 로 τ 를 얻는 식 |
| **Eq. 7** | ε = τ_elc·σ_eff/σ₀ | p.1448 | 같은 식 정리.  *"τ_elc reflects only the true geometrically defined tortuosity (τ_geo) of samples for which the uniform tortuosity model is applicable. In all other cases, τ_elc captures all microstructure effects that influence the conductivity, not only tortuosity."* |
| **Eq. 8** | σ_eff/σ₀ = ε^m | p.1448 | **Archie** [1] — normalized conductivity = 1/F (formation factor).  m = *"empirically derived formation- or series-specific constant"* — 형태 정보는 m 에 묻히고 *"it does not give any information, which features of the pore structure are relevant"* |
| **Eq. 9** | β = A_min/A_max | p.1448 | **constriction factor** — Petersen [12] 의 쌍곡선 목 원관 해석에서 협착 효과 ∝ A_max/A_min ('constriction factor') → *"For simplicity, in our work, we use the inverse ratio to obtain β-values between 0 and 1"* |
| **Eq. 10** | β = πr²_min/πr²_max | p.1448 | 단면을 목 반경 · 입구 반경으로 쓸 수 있는 원기둥 기공 |
| **Eq. 11** | **σ_eff/σ₀ = ε·β/τ_geo** | p.1448 | *"This reduction is taken into account by adding the constriction factor (β) into Eq. 7"* — 이 논문의 예측식 ("extended pore structure model").  *"there is no experimental data, with which to validate the introduction of this constriction factor"* 가 이 논문의 동기 |
| **Eq. 12** | δ_elc = σ_eff·τ_geo/(σ₀·ε_tot) | p.1455 | **electrical constrictivity** — Eq. 11 에 측정 σ_eff 와 구조 τ_geo · ε_tot 를 넣어 역산.  *"The relevance of the electrical constrictivity for structural investigations can be questioned in the same way as for the electrical tortuosity, because both are determined indirectly and may, therefore, not reflect a single specific microstructure feature."* |
| **Eq. 13** | δ_elc = τ_geo·ε_tot^(m−1) | p.1455 | Eq. 12 + Archie (Eq. 8) — 계열 추세선 |
| **Eq. 14** | ε_max = τ^(1/(1−m)) | p.1455 | δ = 1 (병목 영향 없음) 이 되는 기공률 → olivine 0.65 · wollastonite 0.75 |
| **Eq. 15** | ε_eff = δ·ε_tot | p.1455 | effective porosity — *"Constrictions due to pore necks limit the effective pore space available for mass transport"* |
| **Eq. 16** | ε_eff = τ_geo·ε_tot^m | p.1455 | Eq. 13 + 15 — *"if constrictivity is not known, the Archie's law together with the measured geometric tortuosity can be used for the calculation of ε_eff"* |
| **Eq. 17** | ε_eff = Σ(π/4)r²_min·l_eff (인쇄형) | p.1456 | *"the sum of all cross-sectional areas of the pore path constrictions, multiplied with the length of the pore path"* — ⚠ 인쇄형은 부피 차원 · 정규화 없음 (§10 ⑨) |
| **Eq. 18** | σ_eff/σ₀ = ε_eff/τ_geo | p.1456 | Eq. 8 · 16 에서 — m 과 무관한 선형식 → 그림 8c |

### 4-2. τ · 협착 이름 — 원문의 구분
- **τ (Eq. 3, "tortuosity factor")**: Carman [3] 의 l_eff/L.  원문은 이 이름을 **기하 경로 비** 에 쓴다 (p.1447).  같은 그룹의 Holzer 2013 은 *"τ_Carman = (l_eff/l₀)² vs τ_Kozeny = l_eff/l₀ … considerable confusion"* 이라 적는다 (`holzer2013_…` p.2937) — 같은 저자군 안에서도 'Carman 의 tortuosity factor' 가 1 승 (이 논문) ↔ 제곱 (Holzer) 으로 갈린다.
- **τ_elc (electric tortuosity, Eq. 6)**: EIS 로 간접 결정 — 값은 tau2.  균일 관 모형이 맞을 때만 τ_geo 와 같고, 아니면 *"captures all microstructure effects … not only tortuosity"* (p.1448).  *"Apparent variations of the 'electrical tortuosity' may thus not only be due to changes of the geometric tortuosity but also of other stereological parameters, the most prominent being the variation of pore diameters along the trajectories of the pores (bottlenecks, constrictivity)."* (p.1448).
- **τ_geo (geometric tortuosity)**: 단층상에서 직접 — 기공 skeleton 선 그래프에서 source → sink 최단 경로 (Dijkstra) 길이 ÷ **시료 입방체 길이 L**, **모든 source–sink 쌍** 의 평균 (p.1452 · 그림 3 캡션).
- **β_geo (constriction factor)**: 영상 직접 (PSD 두 개의 r50) · Eq. 9–10.
- **δ_elc (electric / electrical constrictivity)**: EIS 간접 · Eq. 12.  결론: *"the bottleneck effect is described in two ways: (1) by direct measurement of the r_min and r_max, which leads to the constriction factor (β) and (2) by indirect calculation of the constrictivity (δ) from EIS measurements. The relation between the constriction factor (β) and constrictivity is published elsewhere."* [24] (p.1456).
- **ε_tot vs ε_eff**: 서론 — ε_eff = 수송에 기여하는 기공 부피 · 차이는 고립 · 막다른 기공뿐 아니라 **협착된 경로** 때문 (p.1447).  이 시료들은 고립 기공 0 (p.1453) 이라 ε_eff < ε_tot 는 전부 협착 몫으로 해석된다.

### 4-3. 측정 사슬
| 단계 | 내용 | 쪽 |
|---|---|---|
| 1 시료 | 같은 격막에서 EIS 원판 (Ø 20 × 2.5 mm) 과 단층 원기둥 (Ø 700 µm) 을 따로 만든다 | p.1449 |
| 2 EIS | 4-전극 차분 저항법 → 양 · 음극 임피던스 · 이중층 영향을 떼어 격막의 순수 저항 R → σ_eff = L/(R·A) (Eq. 6 의 A · L = 시편 단면 · 두께).  세부 셋업은 ref 14 [미확인] | p.1449 |
| 3 SRµCT | 370 nm 재구성 → 660³ @ 740 nm 부분부피 · median · 3D 문턱 이진화 (Avizo) | p.1449–1450 |
| 4 PSD | Münch & Holzer [17] 의 두 크기 분포 — **c-PSD**: 기공망 안 여러 씨앗점에서 시작한 거리 지도 → 목 (국소 최소) 에 양쪽에서 접근 → 목의 인공 효과 없음 → 거품 크기 · **MIP 모사 PSD**: 수은 침투처럼 병목을 지나야 다음 거품에 배정 → 큰 부피가 목 반경에 배정 (*"break through diameter or the constricted radius"*) | p.1450–1451 |
| 5 β | 두 누적 곡선 (100 % 정규화, 그림 4c · d) 의 **r50** (50 vol % 분위) — MIP r50 = r_min · c-PSD r50 = r_max → β_geo = (r_min/r_max)² | p.1451 · p.1454 |
| 6 τ_geo | Avizo voxel skeleton → 관 조각 중심축 → **선 skeleton** (3D 그래프) → source · sink = 관 조각과 z 경계면의 교점 → Dijkstra [22] 최단 경로 · 길이는 벡터 계산 → source 하나에 반대면 sink 전부 (그림 3c 검정 선) · **모든 쌍** (그림 3d) → l_eff/L → 평균 (Table 2: 쌍 60,269–419,079 개) · Matlab 자체 코드 · 그래프 이론 [21] · 중심축 분석 [20] | p.1451–1452 |
| 7 예측 | Eq. 11 에 ε_tot · β_geo · τ_geo · σ₀ → σ_β (Table 1 'σ_β tomo') | p.1454 |

### 4-4. 논증 흐름 (Results and Discussion · Conclusions)
1. **기공률 · 입자 모양** — 둥근 olivine 은 등축 기공, 침상 wollastonite 는 길쭉한 기공 (p.1453).  평균 기공 반경은 ε 와 같이 커진다.
2. **τ_geo 는 평평** — *"Surprisingly, for both diaphragm series, no significant variation of τ_geo is observed over the entire range of porosity"* (1.62–1.87, p.1454) · 그림 5.
3. **β 는 ε 를 따라 움직인다** — *"the constriction factor (β) varies systematically as a function of porosity (ε), unlike the geometric tortuosity (τ_geo), which is nearly constant"* (p.1454).
4. **Archie** — 두 계열이 다른 직선 (m 2.31 · 2.95) → 같은 ε 에서 olivine 이 더 높은 σ (그림 6a · b).
5. **τ_elc** — ε 가 줄면 지수적으로 커지고 두 계열이 다른 추세 · Comiti–Renaud [23] 로그 관계로 맞춤 (그림 6c) · ε = 100 % 에서 두 추세가 τ_geo 근처 (≈ 1.77) 라는 서술 (그림과 어긋남 — §10 ④) · wo 4 에서 τ_elc ≈ τ_geo.
6. **Eq. 11 예측** — *"The calculated values reproduce the measured values remarkably well"* → *"electric transport across the investigated olivine and wollastonite diaphragms is only controlled by the intrinsic conductivity of the electrolyte and the three stereological parameters porosity, tortuosity, and constrictivity"* (p.1454–1455).
7. **δ_elc** (Eq. 12) — ε 와 같이 커지고 두 계열이 다른 추세 → *"structural differences between the two diaphragm series are also reflected by the different average pore neck dimensions"* · Eq. 13–14 → ε_max 0.65 · 0.75 (그림 8a).
8. **ε_eff** (Eq. 15–17) → Eq. 18 · 그림 8c: 두 계열이 한 선 (기울기 = τ_geo 1.77) → *"the ratio of effective porosity over tortuosity captures all microstructure features, which are relevant for the transport process under investigation"* (p.1456) — ⚠ 구성상 자명 (§10 ⑪).
9. **결론** — 기공률만으로는 부족 · τ_geo 는 평평해 구조를 *"not discriminating"* · *"the pore structure effects are dominated to a large degree by the size of pore neck constrictions"* · 복잡한 기공망 전체에서 constrictivity 를 정한 것은 *"the first time"* (p.1456).

### 4-5. 입자 처리 ★ (DEM 양식 항목)
- **해당 없음** — 입자 모형이 없다.  실측 소결체의 기공상을 영상으로 다룬다.  c-PSD · MIP 모사의 '구' 는 크기 탐침이지 입자가 아니다.
- 우리 축과 닿는 점: 전도상이 **연속 액체 기공** (위상이 우리 SE 입자망의 반대) — 병목 = 기공 목, 우리 = SE–SE 접촉 목.

### 4-6. 기법 미니 용어집
| 용어 | 원문 설명 (쪽) | 우리 쪽 대응 |
|---|---|---|
| normalized conductivity σ_eff/σ₀ = 1/F | Eq. 8 (p.1448) | **f** |
| formation factor F | σ₀/σ_eff (Table 1) | 1/f = N_M (⚠ 우리 docstring 의 'formation factor' 는 역수 — 메모 v2 `TAU-17`) |
| Archie m ('m-factor') | Eq. 8 · 결론 p.1456 | f = φ^m 의 지수 — **M-factor 아님** |
| tortuosity factor τ | l_eff/L (Eq. 3, p.1447) | ⚠ 값은 **τ_geo** — 우리 규칙의 'tortuosity factor' (tau2) 와 이름 충돌 |
| electric tortuosity τ_elc | ε σ₀/σ_eff (Eq. 6) | **tau2** |
| geometric tortuosity τ_geo | skeleton Dijkstra l_eff/L, 모든 쌍 평균 (p.1452) | **τ_geo** (`tau_geo_SE_dij` · τ_Dij — 같은 규약 계열, §7) |
| constriction factor β_geo | (r_min/r_max)² (Eq. 9–10) | 없음 — FULL/CF 와 다른 양 |
| electric constrictivity δ_elc | σ_eff τ_geo/(σ₀ ε_tot) (Eq. 12) | 열 없음 — τ_Dij/tau2_FULL 로 만들 수 있다 (§8) |
| effective porosity ε_eff | δ·ε_tot (Eq. 15) | 없음 (측정 σ 에서 나오는 양) |
| uniform tortuosity model | 같은 길이 · 일정 지름 관 (p.1448) | CF 가지와 같은 꼴의 기준 (§8) |
| c-PSD / MIP 모사 PSD · r50 | 거리 지도 거품 크기 / 병목 돌파 크기 (p.1450–1451) | 없음 |
| differential resistance method | 4-전극 EIS 의 격막 저항 [13] (p.1449) | — |

---

## 5. Figure set ★
| Fig | 쪽 | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|---|
| 1 | p.1447 | 세 기공 경로가 교차하는 2D 모식도 — 입구 i · 출구 j 를 잇는 점선 길이 l_eff · 시료 길이 L · 최소 반경 r_min.  *"τ_geo and the minimal pore radius along the pore path (constriction) determine the mass transport"* | τ_geo · r_min 의 뜻 한 장 |
| 2 | p.1450 | 재구성 2D 단면 (z 에 수직): olivine ε 0.27 · 0.44 / wollastonite ε 0.45 · 0.80 (밝음 = 입자, 어두움 = 에폭시 기공) · 축척 200 µm | 등축 vs 섬유상 기공 |
| 3 | p.1451 | (a) voxel skeleton (조각 굵기 · 색 = 기공 반경) (b) 선 skeleton + z 경계면의 source · sink (초록) (c) 2D 단면: 빨강 = 한 쌍의 최단 경로 · 검정 = source 하나에서 모든 sink 로 (d) 모든 쌍 최단 경로망 · 축 ×10⁵ (단위 미표기) | ★ **τ_geo 규약 그림** — "모든 쌍 ÷ L" (우리 벽 τ 와 같은 계열).  크롭 후보 |
| 4 | p.1452 | c-PSD (실선) vs MIP 모사 PSD (점선): (a) olivine (b) wollastonite 누적 기공 부피 % · (c) (d) 100 % 정규화 + 50 vol % 선 · r50 | ★ **β_geo 정의 그림** — 크롭 후보.  ⚠ (b) (d) 곡선 쌍 다섯 vs 범례 넷 |
| 5 | p.1453 | 8 시료 재구성 부피 + 3D 기공 경로 (모서리 488 µm) · ε · τ_geo 표지 | τ_geo 평평의 시각 증거 |
| 6 | p.1454 | (a) F vs ε_tot (log–log, 직선 (1, 1) 통과 · 점선 = 곧은 평행 등지름 관 m = 1) (b) σ vs ε_tot + Archie 맞춤 (c) **τ_elc (●▲) vs τ_geo (×, ≈ 1.8 평평) vs ε_tot** | ★ **tau2 ≠ τ_geo 의 원자료 그림** — 크롭 1 순위급.  축 이름 'tortuosity τ' 에 두 양 |
| 7 | p.1454 | 측정 σ_eff (EIS) vs Eq. 11 계산 σ (β_geo) · 1:1 선 | ★ **Eq. 11 (= Landesfeind Eq. 4) 의 유일한 검증 그림** — 크롭 1 순위 |
| 8 | p.1455 | (a) δ_elc vs ε_tot + Archie 추세 (b) ε_eff vs ε_tot (c) σ vs ε_eff — 한 직선 | δ ≠ β 의 원자료 · (c) 는 구성상 자명 (인용 주의) |
| Table 1 | p.1449 | 전 수치 (σ 측정 · 계산 · F · m · τ_elc · δ_elc · τ_geo · r_min · r_max · β_geo · ε_tot · ε_eff) | ★ **크롭 1 순위** — 이 카드 수치의 원천 |
| Table 2 | p.1452 | τ_geo · 경로 수 n · SD | τ_geo 표본 크기 |

## 6. Post-processing ★
- **무엇**: 3D 문턱 분할 기공률 · 거리 지도 c-PSD · 방향성 침투 MIP 모사 PSD · r50 → β_geo · voxel → 선 skeleton → Dijkstra 모든 쌍 τ_geo 평균 · 4-전극 EIS 순수 저항 → σ_eff · Archie log–log 직선 · Eq. 6 역산 τ_elc · Eq. 11 예측 · Eq. 12 역산 δ_elc · Eq. 14–18 서술식.
- **도구**: Avizo (분할 · skeleton) · 자체 Matlab (경로 길이) · Münch & Holzer [17] PSD 알고리즘 · SLS TOMCAT · Zahner IM6eX.
- **수치화 · 플롯 규약**: 분포의 대표값 = r50 · τ_geo = 경로 평균 (+ SD · n) · 측정 vs 계산 1:1 산점도 (그림 7) · 오차 = SD 표 (Table 2) 와 그림 8 의 고정 % 오차 막대.  통계 적합도 지표 (R² · RMSE) 는 내지 않는다.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md`
> ⚠ 기준값 파일은 이 브랜치에서 자리표시다 (`our_dem_baseline.md` §1) — 아래 우리 쪽 수치는 메인 리포 판단 메모 v2 (`docs/reviews/tau_conventions_judgment_v2_20261003.md`) 의 (유도) 값이고 절 · 행 번호를 단다.  이 카드에서 다시 계산하지 않았다.
> frame[5]: 이 논문은 **수송 서술자 반쪽** (영상 기하 + 측정 수송) — 역학 · 형상 변화 · 압밀 물리 (우리 MPM 반쪽) 는 없다.  frame[4]: 이 논문 값으로 우리 모델을 맞추지 않는다 — **정의 · 분해 틀 · τ_geo 규약** 만 가져온다.

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 이유 |
|---|---|---|---|
| 전도상 | 25 wt% KOH 가 채운 **기공** (연속) | **SE 입자** (DEM 구 · 접촉망) | 위상 반대 — 기공 목 vs 입자 접촉 목 |
| σ₀ | 순수 KOH **0.645 S/cm** (구조 없음, τ ≡ 1 행을 표에 둔다) | σ_grain 3.0 mS/cm = **펠릿값** (`CL-91`) | **기준 상태 다름** — 원문의 δ · β 분해는 구조 없는 σ₀ 를 전제한다 (결정 4) |
| φ 장부 | ε_tot = 단층 c-PSD 총기공률 (고립 0 → 총 = 연결) · 단층 시편 Ø 700 µm ↔ EIS 시편 Ø 20 mm 는 다른 조각 | φ_SE = 전 SE 구 부피 합 (비관통 포함 · 겹침 이중계상) | 같은 자리 (전도상 부피분율) · 장부 다름 |
| tau2 | τ_elc **2.02–5.61** | T_H 1.945–3646, 중앙 6.212 (메모 v2 T17, 유도) | 정의식 같음 (ε σ₀/σ_eff) · 다른 계 |
| τ_geo 규약 | skeleton 그래프 · **모든 source–sink 쌍** · **÷ 시료 길이 L** · 비주기 입방체 (488 µm) · 쌍 6 만–42 만 | T01 τ_Dij: SE 접촉 중심 그래프 · 무작위 ≤ 200 쌍 · **÷ 쌍의 Δz** · [1, 20) 절단 / T04 벽 τ: 벽 띠 사이 같은 규칙 · 주기 x–y (최소영상) | **같은 계열** ("모든 쌍 ÷ 두께 방향 거리" — 측면 변위가 분자에 들어간다).  Holzer (÷ 입출구 벡터) · Ender (출발점마다 최단 ÷ 두께) 와는 다른 규약.  우리는 주기 경계라 측면 변위가 반 상자 이하 → 같은 계열 안에서도 부풀림이 작다 |
| τ_geo 값 | 1.62–1.87 (ε 0.27–0.80 에서 평평) | T01 1.149–17.49 (중앙 1.484) · T04 130: 1.292–4.151 (1.494) · 64: 1.262–1.600 (1.365) | 다른 계 · 우리 넓은 끝은 문턱 근처 SE 적은 침대 (원문 범위 밖 — 원문은 전부 관통 · ε ≥ 0.27) |
| 분해 | **tau2 = τ_geo/β** (모형) · τ_elc = τ_geo/δ_elc (자료) — 선형 · 기준 = 기하 τ | **FULL/CF** = σ_CF/σ_full (같은 망, R_c 켜고 끔) | 다른 분해 — 기준이 τ_geo 냐 CF 냐 |
| 무협착 기준 상태 | 균일 관 모형 (β = 1): τ_elc = τ_geo ≥ 1 → σ_eff ≤ ε σ₀ · 그림 6a 점선 (곧은 평행 등지름 관, m = 1) | CF = 반쪽마다 입자 단면 πr² 원기둥 · T_CF < 1 이 26/157 (메모 v2 §3-6) | CF 는 그 기준의 **망 판** 이지만 τ ≥ 1 을 어긴다 → 원문 기준 상태라 부를 수 없다 |
| 협착 배수 (선형 tau2/τ_geo) | **1.10–3.08** (우리 산술) | 중앙값끼리 T_H/τ_Dij ≈ 4.2 (6.212 ÷ 1.484, 분포 아님) | 다른 계 · 우리 쪽은 hertz 1세대 R_c 과대 · 펠릿 σ₀ 포함 |
| √ 꼴 (웹앱 "Constriction overhead") | **0.77–1.30** · 2/8 < 1 (우리 산술) | √T_FULL/τ_Dij H 1.711 (IQR 1.37–2.10) · √T_CF/τ_Dij 0.80 (메모 v2 §3-5) | √ 꼴은 협착 기공망에서도 1 아래가 나온다 → 협착 지표가 아니다 (`TAU-08`) |
| Bruggeman 배수 τ_elc·ε^½ | **1.80–3.11** (우리 산술) | H 중앙 3.40 (IQR 2.54–6.71) (메모 v2 §3-5) | 같은 축 · 다른 계 |
| 예측 검증 | Eq. 11 맞춤 0 · 8 점 · 측정/계산 0.74–1.37 | 접촉망 = 수송 해 (실험 절대 대조는 결정 4 게이트 뒤) | 원문 예측은 표본 안 · 외부 검증 없음 |
| 비기하 계면 저항 | 없음 (액체 연속) | 없음 (FULL 의 Holm 도 완전 접촉의 기하 퍼짐 저항) | 둘 다 없다 |
| 수송 시뮬레이션 | **없음** (대수식) | 접촉망 Kirchhoff + STEP3 복셀 FV | 우리 FULL 해가 원문의 '측정 σ_eff' 자리에 온다 |

- **같은 양이 되는 조건 (우리 → Wiedenmann 틀)**: ① ε → φ_SE ② σ₀ → **구조 없는** SE 내부값 ③ σ_eff → FULL 해 (전체 단면 정규화) ④ τ_geo → T01/T04 계열 (모든 쌍 ÷ Δz — 원문과 같은 계열; 주기 경계 차이는 메타로) ⑤ 분해식의 τ_geo 지수 = **1** (원문 유도).
- **입경비 · 2D/3D**: 원문은 3D 단층 · 입자 모형 없음 · 기공 r50 1.9–11.5 µm.  우리 생산 기본 r_SE 0.5 µm · 코퍼스 r_SE/r_AM 0.10–0.47 (메모 v2 §3-8) 에 대응하는 '입경비' 개념이 원문에 없다.

---

## § τ 정의 대조 — 우리 규약 매핑
> 우리 규약 (CLAUDE.md ★★ τ 명명 규약 · 1저자 비준 2026-10-03): **f** = σ_eff/σ₀ · **tau2** = φ·σ₀/σ_eff (= 'tortuosity factor', 옛 이름 T) · **tau** = √tau2 · **τ_geo** = 최단 경로 / 두께 (수송 τ 아님) · **τ_e** = electrode tortuosity factor (우리에 없음).
> σ₀ 기준: 이 논문 = **순수 25 wt% KOH 벌크 액체** (0.645 S/cm, 구조 없음 · 온도 미기재) · 우리 = 펠릿값 σ_grain 3.0 mS/cm (`CL-91`).

| 원문 기호 (식 · 쪽) | 원문 이름 | 원문 정의 · 정규화 | 우리 양 | 판정 · 환산 |
|---|---|---|---|---|
| **σ_eff/σ₀** (Eq. 8 · 11 · 18) | normalized conductivity (= 1/F) | 전체 시편 단면 A · 두께 L 로 정규화한 σ_eff ÷ 순수 KOH σ₀ | **f** | 같은 양 |
| **F** (Table 1) | formation factor | σ₀/σ_eff (KOH 행 = 1) | 1/f = N_M | 같은 양 (⚠ 우리 docstring 'formation factor' = f 는 역수, `TAU-17`) |
| **m** (Eq. 8) | Archie series-specific constant ('m-factor') | σ_eff/σ₀ = ε^m | f = φ^m 의 지수 | M-factor 와 이름만 비슷한 다른 양 |
| **τ** (Eq. 3, p.1447) | **"tortuosity factor"** (Carman) | l_eff/L — 경로 길이 비 | **τ_geo** 자리 | ⚠ **이름 충돌** — 원문은 'tortuosity factor' 를 기하 τ 에 쓴다.  우리 문서로 옮길 때 이 이름을 옮기지 않는다 (우리 규칙: tortuosity factor = tau2 전용) |
| **τ** (Eq. 4) | (균일 관 모형의 τ) | G = σ₀π Σd²/(4τL) — 관 길이 = τL | 식의 자리 = **tau2** (측정값을 넣으면) | 모형 안에서는 τ_geo 로 해석, 측정 R 로 풀면 Eq. 6 의 τ_elc |
| **τ_elc** (Eq. 6 · Table 1) | electric tortuosity | **ε_tot σ₀/σ_eff** — φ = ε_tot (단층 총기공률), σ₀ = 순수 KOH | **tau2** | **같은 양** (8/8 ≤ 1 %, §3-C ②).  원문 이름에 'factor' 없음 |
| **τ_geo** (Table 1 · 2, p.1452) | geometric tortuosity | 선 skeleton Dijkstra 최단 경로 ÷ 시료 입방체 길이 L, 모든 source–sink 쌍 평균 | **τ_geo** (`tau_geo_SE_dij` · τ_Dij · 벽 τ) | **같은 범주 · 같은 규약 계열** (모든 쌍 ÷ 두께 방향 거리).  그래프 (기공 skeleton ↔ SE 접촉 중심) · 경계 (비주기 ↔ 주기 x–y) 다름 → 메타로 |
| √τ_elc | (원문에 없음) | — | **tau** | 원문은 √ 값을 쓰지 않는다 — 우리 웹앱 τ_Lap,eff 꼴 비교 (§3-C ⑫) 는 우리 산술 |
| **τ²** (Eq. 2) | Kozeny 상수 k = τ²k₀ 의 τ² | 투과율 (Carman) | τ_geo² | 전도 식에는 τ² 가 없다 — 같은 논문 안의 τ / τ² 공존 사례 |
| **β, β_geo** (Eq. 9–11) | constriction factor | (r_min/r_max)², 영상 PSD r50 | 없음 | **FULL/CF 와 다른 양** (기하 · 솔브 없음) |
| **δ_elc** (Eq. 12) | electric constrictivity | σ_eff τ_geo/(σ₀ ε_tot) = τ_geo/τ_elc | 열 없음 | 만든다면 **τ_Dij/tau2_FULL** (선형 · 기준 = 기하 τ) — 잔차 성격 |
| **ε_tot** | total porosity | c-PSD 기공률 (고립 0) | **φ_SE** (전도상 부피분율) | 같은 자리 · 장부 다름 |
| **ε_eff** (Eq. 15–17) | effective porosity | δ ε_tot (측정 σ 에서) | 없음 | 독립 서술자 아님 (§10 ⑪) |
| **σ₀** | conductivity of the liquid (KOH) | 0.645 S/cm, 구조 없음 | σ_grain 3.0 (펠릿) | **기준 상태 다름** |
| τ_e | — | — | (우리에 없음) | 원문 EIS 는 **관통 4-전극 · 절연 격막 · 실수부만** → 관통 tau2 부류 (Siroma T형 계열) — 전극 τ_e (대칭셀 TLM) 와 다르다 |

- ⚠ **같은 그림 축 'tortuosity τ' 에 두 양** (그림 6c): τ_elc (tau2 양) 와 τ_geo (경로 비).  인용할 때 축을 둘로 나눠 이름 붙인다.
- ⚠ **COMSOL 표기 (결정 5)**: τ_elc 는 COMSOL τ_F (f_e = ε/τ_F) 와 같은 자리 (1 승) — "τ 칸 = tau2" 관례의 또 한 예.  단 원문은 그 양을 'electric tortuosity' 로, 'tortuosity factor' 는 기하 τ 로 부르므로 **원문 이름을 COMSOL 칸 이름과 짝짓지 않는다**.

---

## 8. 적용 인사이트 (내 연구에 어떻게)

### M-factor 식과 지수의 원전
> 이름표 그대로 둔다.  ⚠ 원문에 'M-factor' 는 없고 'm-factor' (Archie 지수) 만 있다 — 우리 문서에서 둘을 섞지 않는다.

**(가) 원식 — 무엇인가**
- **Eq. 11 σ_eff/σ₀ = ε·β/τ_geo** (p.1448) — 저자 이름 "extended pore structure model, which includes the electrolyte conductivity and geometric pore parameters, for example, tortuosity (τ) and constriction factor (β), but no fitting parameters" (초록 p.1446).
- ⇒ **N_M = σ₀/σ_eff = τ_geo/(ε·β)** = Landesfeind 2016 Eq. 4 `N_M ≡ τ̄_geo/(ε·β)` 와 **글자 그대로 같은 꼴**.  τ̄ = 원문 τ_geo 의 정의 (경로 평균, Table 2) 와도 맞다.  β 는 원문의 **β_geo (영상 직접)** 다.

**(나) 지수 — 경험값인가**
| 항 | 지수 | 출처 | 맞춤? |
|---|---|---|---|
| ε | 1 | 균일 관 모형 (Eq. 4–7) | 아니다 |
| τ_geo | **1** | 같은 유도 — Eq. 5 의 A_p = εA 가정 (카드 작성자 해석: 관 부피의 τ 배를 세지 않음) | 아니다 |
| β | 1 | Petersen [12] 의 협착 효과 ∝ A_max/A_min 를 '더함' (Eq. 9–11) | 아니다 |
| (Archie) m | 2.31 · 2.95 | 계열당 4 점 log–log 직선 | **맞춤** — 예측식에는 안 들어간다 (Eq. 13–16 의 서술식에만) |
- 맞춘 자료 수 = **0** (Eq. 11) · 대조한 자료 = **8 시료** · 적용 범위 = ε_tot 0.27–0.80 · β_geo 0.42–0.67 · τ_geo 1.62–1.87 · 액체 KOH 기공 · **R² 미보고**.
- 이 자료 안의 정합 (우리 산술): τ_geo 1 승이면 측정/계산 0.74–1.37 · τ_geo² 로 바꾸면 1.27–2.65 → 1 승이 맞다.  ⚠ 단 이 비교는 원문 τ_geo 규약 (÷ L · 모든 쌍) 에 묶여 있다 — 같은 시료의 Holzer τ_geo (평균 1.62) 로는 β 판이 저항을 더 과소 예측한다 (`holzer2013_…` §3-B).

**(다) 경험 지수가 붙은 꼴 (ε^a·β^b/τ^c) · 'M = ε·β/τ²'**
- **이 논문에 없다.**  자매 논문 Holzer 2013 에도 없다 (`holzer2013_…` §0 · 같은 날 부록 §2).  두 원문 어디에도 'M = ε·β/τ²' 꼴은 없다 — 원식은 τ_geo **1 승**이다.
- 그런 맞춤식이 후속 문헌에 있다면 이 카드는 서지를 채우지 않는다 (규율 ⑥ — 원문 미열람) [미확인].

**(라) 메모 v2 §8-2 "Landesfeind Eq 4 (N_M ≡ τ̄_geo/(εβ)) 원식 — τ_geo 지수 [미확인] 닫기" → 닫힌다**
- 지수 = **1** (Eq. 11, p.1448) · 앞 묶음 부록 §2 마지막 행 "부분 해소 (Holzer)" → **해소 (Wiedenmann 원식)**.
- 덧붙일 한정어 셋: ① 그 1 승은 **유도식의 가정** (Eq. 5) 이지 자료가 정한 값이 아니다 ② β 는 **영상 PSD 의 r50 비** (기하) — 측정 N_M 에서 거꾸로 푼 β 는 원문의 δ_elc (Eq. 12) 이고 β_geo 와 다르다 (Table 1: 0.42–0.67 vs 0.32–0.91) ③ τ̄_geo 의 값은 **규약 (분모 · 쌍 선택) 에 따라 같은 시료에서 ≈ 10 % 흔들린다** (이 원문 1.77 ↔ Holzer 1.62, §10).

**(마) 결정 11 — CF 의 지위 · FULL/CF 의 이름이 이 틀과 맞나 → 맞는다 (권고 유지)**
1. **CF = "모델 내부 기준선" ✓** — 원문의 무협착 기준은 **균일 관 모형** (같은 길이 · 일정 지름, β = 1) 이고 그때만 τ_elc = τ_geo (p.1448).  그 모형 안에서는 β ≤ 1 · τ_geo ≥ 1 이라 **σ_eff ≤ ε σ₀ (τ_elc ≥ 1)** 이 늘 선다 — 실측 8/8 이 τ_elc ≥ τ_geo ≥ 1.62 (Table 1).  그림 6a 의 m = 1 점선 (곧은 평행 등지름 관) 이 그 극한이다.  우리 CF (반쪽마다 πr² 일정 단면 원기둥) 는 그 기준의 망 판이지만 T_CF < 1 이 26/157 (메모 v2 §3-6) → 원문 기준 상태라 부를 수 없다 → '모델 내부' 기준선이 맞다.
2. **FULL/CF = "모델 내부 협착 비" ✓** — 원문의 협착 양은 둘뿐이다: **β_geo** (크기 분포의 기하 비, 솔브 없음) · **δ_elc** (기하 τ_geo 를 기준으로 한 수송 잔차).  FULL/CF 는 기준이 CF 인 수송 비라 **어느 쪽도 아니다** → 영문에 *constriction factor* · *(electric) constrictivity* 를 쓰지 않는다.
3. 결정 11 근거 문장 *"연속체는 Wiener f ≤ φ (T ≥ 1)"* 에 원문 근거를 하나 더 붙일 수 있다: Eq. 11 (β ≤ 1 · τ_geo ≥ 1 ⇒ σ_eff/σ₀ ≤ ε) · Table 1 τ_elc 2.02–5.61.

**(바) TAU-07 ('geom' 오명 · CF 지위) → 원문이 지지**
- 원문 아래 첨자는 출처를 가른다: **'geo' = 단층 영상 기하** (τ_geo · β_geo) · **'elc' = EIS 수송** (τ_elc · δ_elc).  수송 솔브 (협착 0 이라도) 인 τ_Lap,geom 은 이 명명으로는 'elc' 쪽 양이다 → 'geom' 을 떼는 TAU-07 방향과 같다 (Holzer 와 같은 결론, 두 번째 원문 근거).

**(사) TAU-08 (협착 비의 이름 · 정의) → 원문 자료가 √ 꼴의 정의 결함을 직접 보인다**
- 원문 틀의 협착 배수는 **선형** τ_elc/τ_geo = 1/δ_elc = **1.10–3.08** (8/8 ≥ 1).  같은 8 시료를 웹앱 "Constriction overhead" 꼴 (√tau2/τ_geo) 로 쓰면 **0.77–1.30** 이고 **2/8 이 1 아래** (ol 4 0.95 · wo 4 0.77) — 둘 다 δ_elc < 1 인 협착 기공망인데도 (우리 산술 · 본문 표값).  ⇒ √ 꼴은 협착과 단조 관계조차 아니다 → TAU-08 의 "정의 결함" 판정을 **본문 명시값으로** 뒷받침한다.
- 원문 틀을 빌린다면 tau2/τ_geo (선형, = 1/δ) 와 이름 "Wiedenmann/Holzer 형 1/δ (잔차)" — 아니면 메모 v2 대로 "flux ÷ 기하".  같은 망 FULL/CF 는 메모 v2 이름 그대로 두고 기하 서술자 (β 류) 와 섞지 않는다.

**(아) 메모 v2 §3-5 → 결론은 서고 근거 문장을 고칠 후보 (§10 정정 후보 ②③④)**
- *"웹앱 Constriction overhead … 협착으로 읽을 수 없다 — 접촉 저항이 없는 연속 기공상도 1.24–1.59"* — 원문은 접촉 저항 없는 연속 액체 기공망의 τ_elc ≠ τ_geo 를 **병목 (협착)** 으로 돌린다 (p.1448 · p.1456) → Holzer 카드 정정 후보 ① 과 같은 결: "**접촉 (Holm) 협착 배수** 로 읽을 수 없다".  게다가 √ 꼴은 실측 협착 기공망에서 0.77–1.30 까지 내려간다 (위 (사)).
- √T_CF/τ_Dij "반대 방향" 행 — 실측 액체 기공망 2/8 이 √ 척도에서 τ_geo 보다 작다 (본문 표값) → "flux ≥ 기하" 는 √ 척도에서 법칙이 아니다 → CF 결함의 근거는 **T_CF < 1** (Wiener · Eq. 11 의 σ ≤ εσ₀) 로 둔다 (같은 날 부록 §0 ④ 와 같은 방향 · 표값 근거 추가).
- Bruggeman 행 — 격막 τ_elc·ε^½ **1.80–3.11** 은 본문 표값으로 재현된다 (Holzer 카드의 벡터 추출 1.8–3.1 확인).

**(자) 결정 16 묶음에 주는 그 밖의 인사이트**
- ① **τ_geo 규약은 값의 ≈ 10 % 를 정한다 (결정 15 메타 · T01/T04 라벨)** — 같은 8 시료에서 이 원문 (모든 쌍 ÷ L) 평균 1.77 ↔ Holzer 1.62.  6/8 시료의 비 1.10–1.14 는 "÷ 두께" 와 "÷ 입출구 벡터" 의 차 (균일 끝점 가정의 기하 기대값 E[√(1+d²)] ≈ 1.15, 우리 산술) 와 방향 · 크기가 맞지만 wo 3 · wo 4 (1.03 · 0.99) 는 설명 못 한다 [원인 미확인].  ⇒ 우리 `tau_geo_SE_dij` · τ_Dij 는 **이 원문과 같은 계열** (모든 쌍 ÷ Δz) 이다 — 문헌 τ_geo 와 나란히 놓을 때 Wiedenmann 표값이 같은 규약 짝이고, Holzer · Ender 값은 규약 표지를 단다.  Holzer 형 δ_net = τ_Dij/tau2_FULL (Holzer 카드 §8 ②) 도 이 ≈ 10 % 규약 폭을 그대로 물려받는다 → 메타 필수 (권고 변경 없음 · 보강).
- ② **결정 4 (순수 SE 게이트)** — 원문 Table 1 은 기준 상태를 **한 행으로 둔다** ('KOH': σ₀ · F = m = τ = ε = 1).  구조 없는 σ₀ 라서 가능한 일이다.  우리 σ₀ (펠릿) 는 구조가 있으므로 같은 행을 **측정으로** 채워야 한다 = 순수 SE 망 런 (hertz · CF) 의 T_pure → 사전등록 표에 "기준 상태 행" 을 명시적으로 둔다 (권고 변경 없음 · 형식 제안).
- ③ **ε_eff · Eq. 18 을 서술자로 쓰지 않는다** — 원문의 ε_eff 는 측정 σ 에서 나와 Eq. 18 이 항등식이 된다 (§10 ⑪).  우리 쪽에서 '유효 φ' 류 열을 σ 로 만들면 같은 순환이 생긴다.
- ④ **Archie m 은 계열 (공정 · 입자 모양) 표지다** — 원문: 같은 소결 이력 계열 안에서만 직선 · 모양이 다르면 m 이 다르다 (olivine 2.31 ↔ wollastonite 2.95).  우리 f = φ^m 을 코퍼스 전체에 하나로 맞추면 입경 · P:S 계열이 섞인다 (메모 v2 §3-8 입경비 가설과 같은 방향 — 원문은 입자 모양 축).
- ⑤ **대표 부피** — 원문 부분부피 모서리 ÷ r_max = 42–170 (우리 산술) · PSD SD 4–10 %.  우리 STEP3 d_h/dx ≳ 3.5 규칙 · RVE 판단에 쓰는 크기 감각 (권고 아님).

## 9. 인용 가능 문장 (deck/paper용)
- "The structure–conductivity relation of Wiedenmann et al. (AIChE J. 59, 1446, 2013), σ_eff/σ₀ = ε·β/τ_geo, contains no fitted exponents: porosity, constriction factor β = (r_min/r_max)² and geometric tortuosity all enter with power one; the MacMullin form N_M = τ̄_geo/(εβ) quoted by Landesfeind et al. (2016) is its exact inverse."
- "Their 'electric tortuosity' τ_elc = ε·σ₀/σ_eff is numerically our tortuosity factor (tau2), whereas the name 'tortuosity factor' is applied in that paper to the geometric path-length ratio l_eff/L; we therefore map by definition, not by name."
- "In tomograms of KOH-filled ceramic diaphragms (ε = 0.27–0.80), the geometric tortuosity stayed at 1.62–1.87 while impedance-derived tortuosities reached 5.61; the authors attribute the gap to pore-neck constrictions (Wiedenmann et al., 2013)."
- "Because the no-constriction reference of Wiedenmann et al. (uniform tubes, β = 1) always satisfies σ_eff ≤ εσ₀, our contact-free network branch, which can yield tau2 < 1, is a model-internal baseline, and the FULL/CF ratio is neither their constriction factor β nor their electric constrictivity δ."

## 10. 주의/한계 (over-claim 방지)
- ⚠ **액체 전해질 · 소결 세라믹 기공** (25 wt% KOH) — LPSCl 고체 입자망으로 **수치 전이 불가**.  가져오는 것은 원식 (지수) · 정의 · β ≠ δ · τ_geo 규약뿐이다.
- ⚠ **8 시료 · R² 없음** — "remarkably well" 은 산점도 판정이다.  측정/계산 0.74–1.37 · wo 4 +37 % (우리 산술).  외부 검증 · 다른 재료계 시험은 없다.
- ⚠ **"no fitting parameters" 는 Eq. 11 에만** — 서술식 (Eq. 13–16) 은 맞춘 m 을 쓴다.  r50 선택 (분위) 은 방법 선택이다.
- ⚠ EIS 측정 온도 · 기공 형성제 비율 · EIS 차분법 세부 · σ_β 계산 입력값은 원문에 없다 [미확인].
- ⚠ 단층 시편 (Ø 700 µm, 부분부피 488 µm) 과 EIS 시편 (Ø 20 mm × 2.5 mm) 은 **다른 조각** — 국소 대표성은 가정이다.
- ⚠ 원문 서술 · 그림 · 표의 어긋남이 여럿이다 (아래 원문 대조 기록) — 수치는 **Table 1 · 2 표값** 을 쓰고, 본문 서술 ("≈ 1.77 at 100 %" · "ratio (r_min/r_max)" · "(Table 2)") 은 표와 대조해 인용한다.
- ⚠ 우리 쪽 수치 (§7 · §8) 는 메모 v2 의 (유도) 값이고 이 카드에서 다시 계산하지 않았다.  중앙값끼리의 비는 침대별 분포가 아니다.

### 메모 v2 정정 후보 (판단 메모 v2 `docs/reviews/tau_conventions_judgment_v2_20261003.md` · 부록 `…_addendum_lit10_20261003.md` 문장 ↔ 이 원문)
| # | 자리 · 문장 | 원문 (쪽) | 제안 |
|---|---|---|---|
| ① | 메모 v2 §8-2 Wiedenmann 행 *"Landesfeind Eq 4 (N_M ≡ τ̄_geo/(εβ)) 원식 — τ_geo 지수 [미확인] 닫기"* · 부록 §2 마지막 행 *"부분 해소: Holzer 분해식의 τ_geo 는 1 승 … M-factor (ε·β/τ²) 꼴 · 지수는 이 논문에 없다"* | Eq. 11 σ_eff/σ₀ = εβ/τ_geo (p.1448) · 초록 "no fitting parameters" (p.1446) · Table 1 σ_β 재현 (5/8 ≤ 2.8 %) | **해소** — τ_geo 지수 = 1 (유도식 · 맞춤 아님).  'M = ε·β/τ²' 꼴 · 경험 지수는 **Wiedenmann 에도 없다** 를 덧붙인다 |
| ② | 메모 v2 §3-5 *"웹앱 Constriction overhead … 협착으로 읽을 수 없다 — 접촉 저항이 없는 연속 기공상도 1.24–1.59 를 낸다"* | 연속 액체 기공망의 τ_elc ≠ τ_geo = 병목 (p.1448 · p.1456) · √τ_elc/τ_geo 0.77–1.30 (Table 1, 우리 산술) | Holzer 카드 ① 과 같은 결론 (두 번째 원문): "**접촉 (Holm) 협착 배수** 로 읽을 수 없다 — √ 꼴은 협착 기공망에서 1 아래도 나온다" |
| ③ | 부록 §0 ④ · `comparison_vs_ours_DEM.md` J 절 *"Holzer √τ_elc/τ_geo 0.76–1.46 (격막 8 점)"* | 같은 8 시료의 원 표값 (p.1449) 으로 **0.77–1.30** (ol 4 0.95 · wo 4 0.77 < 1) | 범위가 τ_geo 집합에 달렸다고 적는다: "0.76–1.46 (Holzer τ_geo, 벡터 추출) · 0.77–1.30 (Wiedenmann 표값)" — 반례 수 1 → 2 |
| ④ | 부록 §2 *"§3-5 Bruggeman 행 … Holzer 격막 1.8–3.1×"* | τ_elc·ε_tot^½ = **1.80–3.11** (Table 1 표값, 우리 산술) | 근거를 본문 표값으로 (값 불변 · 보강) |
| ⑤ | `comparison_vs_ours_DEM.md` J 절 τ_geo 행 *"τ_geo = skeleton Dijkstra ÷ 입출구 거리 (Holzer)"* | 원 논문: **÷ 시료 입방체 길이 L · 모든 source–sink 쌍 평균** (p.1452 · 그림 3 캡션) | Wiedenmann 규약을 따로 적는다 — 우리 τ_Dij · 벽 τ (÷ Δz · 모든 쌍 표본) 와 같은 계열 (메인 판단) |

### 기존 카드 대조 (이 원문 ↔ 카드 서술 — 카드는 고치지 않았다 · 메인 판단)
| 카드 · 자리 | 카드 서술 | 이 원문 | 판정 |
|---|---|---|---|
| `landesfeind2016_…` Eq. 4 행 · ref [10] | N_M ≡ τ̄_geo/(ε·β), *"인쇄형은 τ̄_geo 1승 — 원 출처의 지수는 [미확인: Wiedenmann 2013 원문 미열람]"* | Eq. 11 = 같은 꼴, τ_geo 1 승 (p.1448) | ✓ 일치 → [미확인] 닫힘.  저자 16 명 목록도 원문과 같다 |
| `landesfeind2016_…` §τ 대조 β 행 | *"인쇄형대로면 β = τ̄_geo/T = τ_Dij/τ_Lap,eff²"* | 측정 σ 에서 거꾸로 푼 그 양은 원문의 **δ_elc** (Eq. 12) — 원문 β_geo 는 PSD r50 비 | 이름 정정 후보: "δ (역산) — β_geo (기하) 와 다름" |
| `landesfeind2016_…` 본문 τ_geo 행 (A1373–A1374) | τ_geo = 두 점의 최단 연결 ÷ **직선 길이** · τ̄_geo = 점쌍 평균 (graph theory [10]) | [10] 의 실제 정규화는 **÷ 시료 길이 L** (모든 쌍) — 직선 길이가 아니다 | Landesfeind 의 일반 정의와 [10] 의 규약이 다르다는 한정어 후보 (÷ 직선 길이면 [10] 표값보다 작아진다 — Holzer 1.62 가 그 방향, 원인 [미확인]) |
| `holzer2013_…` §3-A · §3-C ⑥ · §10 | Archie m *"olivine 2.95 · wollastonite 2.31 (원문 배정)"* — 벡터 추출로는 뒤바뀐 꼴이라 카드가 그 값의 인용을 막아 두었다 | 원 논문 Table 1 · p.1454: **olivine 2.31 · wollastonite 2.95** = 자료와 맞음 (우리 산술 2.33 · 2.98) | Holzer 2013 의 배정이 뒤바뀐 것으로 **확인** — 원 논문 값은 인용 가능 |
| `holzer2013_…` §3-B · §7 | τ_geo 1.56–1.86, 평균 **1.62** (그림 12 벡터 추출 · 본문 p.2949) | Table 1 · 2: **1.62–1.87, 평균 1.77** (p.1454 · p.1456).  나머지 (ε · σ_eff · τ_elc · r_min · r_max · β) 는 2–3 자리까지 같다 | **같은 시료 · 다른 τ_geo** — δ 도 다르다 (Holzer 0.285–0.792 ↔ 원 논문 0.32–0.91).  원인 [미확인] (분모 규약 가설은 §8 (자) ①) |
| `holzer2013_…` §3-C ② · 원문 대조 ⑨ | W4 δ: 그림 15 0.792 vs 그림 12 τ_geo 1.86 이면 0.92 | 원 논문 Table 1 W4: τ_geo 1.84 · δ_elc **0.91** | 원 논문은 Holzer 그림 12 · 16 쪽과 맞고 Holzer 그림 15 (0.792) 와 다르다 |
| `holzer2013_…` §10 | *"ε 의 정의 (총 / 연결) · σ_eff 의 단면 · 두께 정규화는 이 논문에 없다 (전작 [37]) [미확인]"* | ε_tot = c-PSD 총기공률 · MIP 모사 같음 → 고립 0 (p.1453) · σ_eff = R 을 시편 A · L (Ø 20 × 2.5 mm) 로 (Eq. 6 · p.1449) | ε 정의 **닫힘** (총 = 연결) · 정규화 **부분 닫힘** (차분법 세부는 ref 14) |
| `holzer2013_…` §3-C ⑤ · 원문 대조 ⑦ | 그림 11 '계산값' = 정확히 1.20 × σ₀ε/τ_geo [원인 미확인] | 원 논문에는 σ₀ε/τ_geo 계산 계열이 없고 σ₀ 는 0.645 하나뿐 · 원 τ_geo 를 넣어도 0.88–1.01 배 (방향 반대) | **닫히지 않음** [미확인 유지] |
| `holzer2013_…` §3-A EIS 행 | *"0.1–100 kHz"* | **100 kHz – 0.1 Hz** (p.1449) | 0.1 kHz 로 읽힐 수 있는 표기 — Holzer 원문 대조 [미확인] |
| `holzer2013_…` §2 메타 | 격막 자료 [37] = *"(2012) AIChE J (in press)"* · 같은 묶음 카드들은 AIChE J 59(5) 1446–1457 (2013) | AIChE J 59(5) 1446–1457 (May 2013) · 온라인 2013-04-01 | ✓ 확인 |
| `tjaden2018_…` ref [14] | 서지 · "3D 구조 → 이온 전도도를 기하 τ·협착으로 잇는 식" | 같음 | ✓ |

### 원문 대조 기록 (이 카드 작성 중 직접 확인한 것)
1. **Eq. 3 이름** (p.1447): l_eff/L 을 *"tortuosity factor"* 로 부른다 — 우리 규칙 (tau2 전용) 과 반대.  같은 쪽 Eq. 2 는 Kozeny 상수 k = **τ²**k₀.
2. **Eq. 4–5 유도** (p.1448): 관 단면 합을 εA 로 둬 τ 1 승이 된다 (카드 작성자 해석 — 원문은 이 가정을 논하지 않는다).
3. p.1454 *"The ratio (r_min/r_max) then gives the constriction factor (β_geo)"* — Eq. 10 · Table 1 은 **(r_min/r_max)²** (8/8 재현).  1 승이면 0.65–0.82.
4. p.1454 *"For a hypothetical porosity of 100%, both trends give a value, which is close to the observed geometrical tortuosity (i.e., close to 1.77)"* — 그림 6c 곡선은 ε_tot = 1 에서 **τ ≈ 1** 로 만난다 (판독) · Archie 를 넣은 τ_elc = ε^(1−m) 도 ε = 1 에서 1 (우리 산술).  어긋남.
5. p.1454 *"The excellent correspondence between measured and calculated conductivity (Table 2)"* — Table 2 는 τ_geo 표다.  대조는 **Table 1**.
6. Table 1 σ_β: 반올림된 표 입력으로 Eq. 11 을 다시 풀면 wo 2 · wo 3 · wo 4 가 +7.1 · +10.1 · −5.0 % 어긋난다 (나머지 ≤ 2.8 %) — 계산 입력값 미기재.
7. **그림 4b · d**: wollastonite 곡선 쌍이 다섯 (≈ 80 · 75 · 59 · 52 · 45 % 평탄부, 판독) — 범례 넷 · 표 넷.  wo 4 표값은 자홍 곡선과 맞고 파랑 (≈ 75 %) 곡선은 표에 대응 행이 없다.
8. **Eq. 14** 의 τ: ε_max 0.65 · 0.75 는 τ = 1.77 (8 시료 평균) 로 재현된다 — 본문은 어느 τ 인지 적지 않는다.
9. **Eq. 17** 인쇄형 ε_eff = Σ(π/4)r²_min·l_eff — 부피 차원 (시료 부피로 나누는 항 없음) · π/4 는 Eq. 4–5 에서 **지름** 과 짝인데 여기서는 반경 r_min 과 짝.
10. **그림 8 캡션**: δ_elc 오차 *"calculated according to Eq. 14"* — Eq. 14 는 ε_max 식 (δ_elc 는 Eq. 12–13).  ε_eff 오차 *"according to Eq. 17"* — 표의 ε_eff 는 Eq. 15 (측정 σ) 로 재현된다 (§3-C ④).
11. **Eq. 18 · 그림 8c 의 순환**: 표의 ε_eff = τ_geo σ_eff/σ₀ 이므로 σ_eff/σ₀ = ε_eff/τ_geo 는 **항등식**이고 두 계열이 한 선 (기울기 σ₀/τ_geo) 에 놓이는 것은 구성상 당연하다 — p.1456 의 *"captures all microstructure features"* 는 독립 검정이 아니다.  독립 검정은 그림 7 (σ_β) 뿐이다.
12. 초록 (p.1447) *"The lower constrictivity provides more pore space that can effectively be used for mass transport"* — δ · β 는 1 = 무협착 관례라 문자 그대로면 방향이 반대 (그림 8b: δ 가 클수록 ε_eff 큼).  'constrictivity' 를 '협착 정도' 뜻으로 쓴 것으로 보인다 [해석].
13. **ref 24** 제목 *"Quantitative description of bottlenecks in 3D-microstructures: a heuristic approach to calculate effective transport properties"* (J Mater Sci 2013;48:2934–2952) — 같은 권 · 쪽의 Holzer 카드 제목은 *"The influence of constrictivity on the effective transport properties of porous layers in electrolysis and fuel cells"*.  출판 전 가제로 보인다 [해석].
14. **ref 17** 연도 *"5008"* (J Am Ceram Soc 91:4059–4067) — 오식 (본문 그림 4 캡션은 "Münch and Holzer (2008)").

---

## 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 원문 ref | 목록 서지 (그대로) | 왜 볼 만한가 |
|---|---|---|
| 24 | Holzer L, Wiedenmann D, Münch B, Keller L, Prestat M, Gasser P, Robertson I, Grobéty B. Quantitative description of bottlenecks in 3D-microstructures: a heuristic approach to calculate effective transport properties. J Mater Sci. 2013;48:2934–2952. | 정본 카드 있음 (`holzer2013_…`, 출판 제목 다름) — β–δ 관계 · 같은 시료의 다른 τ_geo |
| 12 | Petersen EE. Diffusion in a pore of varying cross section. AIChE J. 1958;4:343–345. | constriction factor (A_max/A_min) 의 원전 — β 의 1 승 근거 |
| 17 | Münch B, Holzer L. Contradicting geometrical concepts in pore size analysis attained with electron microscopy and mercury intrusion. J Am Ceram Soc. 5008;91:4059–4067. | c-PSD · MIP 모사 알고리즘 원문 (연도 오식 그대로) |
| 14 | Stojadinovic J, Wiedenmann D, Gorbar M, La Mantia F, Suarez L, Zakaznova-Herzog V, Vogt UF, Grobéty B, Züttel A. Electrochemical characterization of porous gas separation diaphragms. ECS Electrochem Lett. 2012;1:F25–F28. | EIS 셋업 · 차분법 · σ_eff 정규화 세부 (이 카드의 [미확인]) |
| 13 | Fievet P, Szymczyk A, Aoubiza B, Pagetti J. Evaluation of three methods for the characterisation of the membrane-solution interface: streaming potential, membrane potential and electrolyte conductivity inside pores. J Membr Sci. 2000;168:87–100. | 차분 저항법의 출처 |
| 19 | Holzer L, Iwanschitz B, Hocker Th, Münch B, Prestat M, Wiedenmann D, Vogt U, Holtappels P, Sfeir J, Mai A, Graule Th. Microstructure degradation of cermet anodes for solid oxide fuel cells: quantification of nickel grain growth in dry and in humid atmospheres. J Power Sources. 2011;196:1279–1294. | PSD 재현성 SD 4–10 % 의 근거 |
| 20 | Lindquist WB, Lee SM, Coker DA, Jones KW, Spanne P. Medial axis analysis of void structure in three-dimensional tomographic images of porous media. J Geophys Res. 1996;101:8297–8310. | 중심축 skeleton τ_geo 의 선례 |
| 23 | Comiti J, Renaud M. A new model for determining mean structure parameters of fixed beds from pressure drop measurements: applications to beds packed with parallelepipedal particles. Chem Eng Sci. 1998;44:1539–1545. | 그림 6c 의 τ_elc–ε 로그 관계 (식 · 계수 미인쇄) |
| 4 · 7 · 8 | Engblom SO, Myland JC, Oldham KB, Taylor AL, Topic WC. J Appl Electrochem. 2003;33:51–59. · Myland JC, Oldham KB, Schiewe J, Taylor AL. Can J Chem. 1998;76:1688–1694. · Oldham KB, Topol LE. J Phys Chem. 1967;71:3007–3013. | 균일 관 모형 (Eq. 4–7) 의 출처 — τ 1 승 관례의 계보 |
| 1 · 3 · 9 | Archie GE. Trans AIME. 1942;146:54–62. · Carman PC. Flow of Gases Through Porous Media. 1956. · Wyllie MR, Rose WD. Nature. 1950;165:972. | Eq. 8 · Eq. 1–3 · 'Carman 의 tortuosity factor' 를 전도도에서 유도한 원전 |
| 18 | Diamond S. Mercury porosimetry: an inappropriate method for the measurement of pore size distributions in cement based materials. Cem Concr Res. 2000;30(10):1517–1525. | MIP 병목 효과 비판 — r_min 해석 |

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

<!-- digest 표준 양식 확장 (paper-level STANDALONE). ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · τ 묶음 형식 기준 = tjaden2018_… · landesfeind2016_… · taufactor_… 카드.
     이 논문은 시뮬레이션이 아니라 *정의 + 3D 영상 측정법 + EIS* 논문이다 → §4 = 정의식 · 측정 사슬, §8 = "협착 (constrictivity β) 정량 틀".
     쪽 표기 = 학술지 인쇄 쪽 (PDF n 쪽 = 인쇄 2933 + n 쪽 · PDF 1 = p.2934 … PDF 19 = p.2952).  식 · 그림 번호 = 원문 번호.  SI 없음.
     수식 · 표가 든 쪽은 원문을 그림으로 렌더해 대조했다 (텍스트 추출은 τ→s, β→b, δ→d, σ→r 로 깨뜨린다).
     값 표지: stated = 본문 · 캡션 원문 / 벡터 추출 = 그림이 PDF 안에 벡터 경로로 들어 있어 표지 중심 좌표를 축 눈금 글자 위치로 환산한 값
     (눈 판독보다 정밀하지만 본문 명시값이 아니다 → ≈ 표기) / 우리 산술 = 원문 · 추출 수치로 카드 작성자가 계산한 값. -->
# The influence of constrictivity on the effective transport properties of porous layers in electrolysis and fuel cells — 협착을 두 양으로 나눈다: 기하 constriction factor β = (r_min/r_max)² ↔ 수송 constrictivity δ, 실험 τ_exp ↔ 기하 τ_geo 엄격 구분 — Holzer (J. Mater. Sci. 2013)

> slug `holzer2013_constrictivity_effective_transport_porous_layers` · DOI `10.1007/s10853-012-6968-z` · type `exp + 3D image analysis (constrictivity β/δ 정의·측정 — FIB-SEM · SRµCT · c-PSD · MIP 모사 · skeleton Dijkstra τ_geo · 4-전극 EIS)` · PDF `1. The influence of constrictivity on the effective transport properties of porous layers in electrolysis and fuel cells.pdf` · digested `2026-10-03` · status ✅
>
> ★ **판정 요약 (이 카드의 목적 = 협착 정량 틀)** — 원문은 '협착' 을 **두 양**으로 나눈다: **β = constriction factor** = A_min/A_max = (r_min/r_max)² (Eq. 6, p.2938) — 3D 영상에서 바로 재는 **기하** 양 (r_min = MIP 모사의 r50 = 돌파 반경, r_max = c-PSD 의 r50 = 거품 크기) · **δ = constrictivity** — 측정 σ_eff 와 영상 ε · τ_geo 를 σ_eff/σ₀ = ε·δ/τ (Eq. 3, p.2937) 에 넣어 **역산** 하는 수송 양.  둘은 같지 않다 (β 0.42–0.67 ↔ δ 0.29–0.79, 사인 관계 Eq. 9–10).
> τ 도 둘이다: **τ_exp (= EIS 판 τ_elc) = ε·σ₀/σ_eff** (Eq. 2 역산, 제곱 없음) = **우리 tau2** · **τ_geo** = skeleton 그래프 Dijkstra 최단 경로 ÷ 입출구 벡터 길이 = **우리 τ_geo** — 원문이 *"must be strictly distinguished"* (p.2936).  분해식 안에서 τ_geo 는 **1 승** 이다: τ_exp = τ_geo/δ (Eq. 3) — 그림 16 의 예측 8 점을 이 꼴로 ≤ 0.3 % 재현 (우리 산술, §3-C).  **"M-factor" 이름 · ε^a β^b/τ^c 꼴의 맞춤 지수는 이 논문에 없다.**
> ⇒ 우리 **FULL/CF (같은 망에서 접촉 저항만 켜고 끈 비)** 는 β (기하) 도 δ (기하 τ 기준 잔차) 도 아니다 — 메모 v2 의 이름 "**모델 내부 협착 비**" · CF = "**모델 내부 기준선**" 은 이 틀과 맞는다 (§8 협착 정량 틀).
>
> ⚠ 범위: **액체 전해질 (25 wt% KOH) 이 채운 소결 세라믹 격막 기공** (olivine · wollastonite, ε 0.27–0.80) + SOFC 양극 (LSC) 의 3D 영상 시험.  고체 전해질 · 입자 접촉 저항 · 저항망 계산은 **나오지 않는다**.  원문은 유한요소 · 격자 볼츠만 수송 시뮬레이션을 **일부러 다루지 않는다** (p.2936).

---

## 0. 결론 먼저 (메인이 물은 것 → 답)

| 질문 | 답 | 근거 (식 · 쪽) |
|---|---|---|
| 이 논문의 τ 는 기하 τ 인가 τ² (tortuosity factor) 인가? | **둘 다 있고 이름이 다르다.** τ_exp · τ_elc = ε·σ₀/σ_eff — 값은 **tortuosity factor (우리 tau2)** 인데 원문은 'experimental / electrical tortuosity' (factor 없음) 라 부른다.  τ_geo = 경로 길이 비 (**우리 τ_geo**).  분해식 (Eq. 3 · 8 · 11) 의 τ 자리에는 **τ_geo 1 승** 이 들어간다 | Eq. 2 (p.2936) · 약어표 (p.2934) · p.2949 · Eq. 11 (p.2950) |
| τ² 관례는? | 원문은 **쓰지 않는다**: *"τ² was introduced in Eq. 2 instead of τ … the exponent of 2 is not rigorously derived, but it was motivated mainly by the intention to fit the exponential data with reasonable values for tortuosity (τ_exp)"* · τ_Carman = (l_eff/l₀)² vs τ_Kozeny = l_eff/l₀ 혼동을 지적 | p.2937 |
| 정규화 (부피 · 단면 · σ₀) | ε = 단층촬영 기공률 (전도상 = 액체 기공; 총 / 연결 구분은 이 논문에 없음 [미확인]) · σ_eff = 4-전극 EIS 의 순수 저항에서 (단면 · 두께 처리는 전작 [37], 이 논문 미기술 [미확인]) · **σ₀ = 25 wt% KOH 벌크 액체 0.645 S/cm** ("intrinsic conductivity in a non-structured media") · σ ↔ D 는 같은 식으로 바꿔 쓴다 | p.2936 · p.2940 |
| β 의 정의 · 측정법 | β = A_min/A_max = πr²_min/πr²_max = (r_min/r_max)² (Eq. 6) · β = 1/β_Petersen (Eq. 4) · r_min = **MIP 모사 r50** (돌파 반경 지배 · 시료 두께 > ID_crit 일 때 안정) · r_max = **c-PSD r50** (거품 · 비협착 영역 · 더 큰 부피 필요) | p.2938 · p.2941–2948 |
| β 는 "같은 망의 접촉 저항 유무 비" 와 같은 양인가? | **아니다.**  β 는 두 크기 분포의 대표 반경 비 (기하 · 솔브 없음 · 0–1, 작을수록 협착).  FULL/CF 는 같은 그래프의 두 수송 해의 비 (≥ 1, 클수록 협착).  원문 자신이 β ≠ δ 를 보인다 — 기하 비가 수송 비를 대신하지 못한다 | Eq. 6 · Fig. 15 · Fig. 16 (p.2950) |
| M-factor (ε·β/τ²) 분해와 지수? | **이 논문에 없다.**  있는 것: σ_r = σ_eff/σ₀ = ε·δ/τ_geo (지수 전부 1, 맞춤 아님) + δ_geo = f(β) 사인 맞춤 (a 0.3 · b 0.7 · c 0).  β 를 δ 자리에 바로 넣은 꼴 (σ_r = εβ/τ_geo) 은 원문 그림 16 의 'β-trend' 로, 저항을 **과소** 예측한다.  원문의 'm-factor' 는 Archie 지수 m (Eq. 1) 이다 — M-factor 와 다른 양 | Eq. 3 · 9 · 10 · 11 · Fig. 16 · p.2948 |
| 결정 11 (CF = "모델 내부 기준선" · FULL/CF = "모델 내부 협착 비") 이 이 틀과 맞나? | **맞는다 — 권고 유지.**  CF 는 원문의 δ = 1 기준 상태 ("cylindrical pores with constant radius" p.2937 · "straight pipes" p.2950 → σ_r = ε/τ_geo, τ ≥ 1) 의 망 판이지만 부피 비보존이라 T_CF < 1 이 나온다 → 원문 영역 (τ ≥ 1, Eq. 2) 밖 = **모델 내부** 기준선.  FULL/CF 는 기구 (목 폭에 반비례하는 저항) 는 원문의 협착과 같지만 기준이 τ_geo 가 아니라 CF 라 δ 가 아니다 → "constrictivity" · "constriction factor" 이름 금지 | §8 |

---

## 1. 한 줄 요약
다공층의 유효 수송을 ε · τ · δ 같은 **부피 평균 매개변수 몇 개로 기술할 수 있는가** 를 묻고, (i) 3D 영상 (FIB-SEM 15 nm · SRµCT 740 nm) 에서 **constriction factor β = (r_min/r_max)²** 를 재는 절차 — 거리 지도 기반 **c-PSD (r_max)** 와 **MIP 모사 (r_min = 돌파 반경)** — 를 SOFC 양극 (LSC) 으로 시험해 재현성 조건 (두께 > ID_crit ≈ 2–5 × 최대 입자 반지름, 침투 방향 무관) 을 세우고, (ii) 알칼리 수전해 격막 (olivine · wollastonite, ε 0.27–0.80) 에서 **기하 τ_geo 는 ε 와 무관하게 ≈ 1.6 으로 평평한데 EIS 로 역산한 τ_elc 는 5.6 까지** 오른다는 것을 보이며, 그 격차를 **constrictivity δ = τ_geo/τ_elc** (Eq. 3 역산) 로 옮겨 δ 와 β 사이의 **경험 사인 관계** (Eq. 9–10) 를 맞추고 영상만으로 저항을 예측한다 (Eq. 11, 그림 16).  우리에게는 **"τ_exp (= tau2) ≠ τ_geo, 그 사이를 메우는 것이 협착" 이라는 분해 틀** 과 **기하 협착 (β) ≠ 수송 협착 (δ)** 이라는 구분을 원문으로 못박아 주는 기준 논문이다 (수치는 액체 격막이라 전이 불가).

## 2. 메타
| 저자 | 저널/년 | DOI | 재료계 | 연구유형 |
|---|---|---|---|---|
| **L. Holzer** (교신, holz@zhaw.ch — ZHAW Institute of Computational Physics), D. Wiedenmann, B. Münch, L. Keller, M. Prestat, Ph. Gasser, I. Robertson, B. Grobéty (ZHAW · Univ. Fribourg · EMPA · ETH Zürich · Univ. St. Andrews) | **J. Mater. Sci. 48(7), 2934–2952 (2013)** — 분류 'Energy Materials & Thermoelectrics' | **10.1007/s10853-012-6968-z** | ① SOFC 양극 La₀.₆Sr₀.₄CoO₃₋Δ (LSC) 다공층 (방법 시험) ② 알칼리 수전해 격막 olivine · wollastonite 소결체 + 25 wt% KOH (β–δ 관계) | **실험 + 3D 영상 분석** (정의 · 측정법) — 수송 시뮬레이션 없음 |

- 접수 2012-05-11 · 승인 2012-10-15 · 온라인 2012-10-26.  © Springer Science+Business Media New York 2012 (오픈액세스 표기 없음).
- 사의: Thomas Hocker (ZHAW, 수송 모델링 토론) · Andre Hell (화염 분무 LSC 분말).  연구비 표기 없음.
- 격막 자료는 **전작 Wiedenmann et al. [37]** (본문 표기 "D Wiedenmann, L Keller, L Holzer, et al. (2012) AIChE J (in press)") 의 자료를 β 관점에서 **재평가** 한 것이다 (p.2948).  같은 묶음 카드들 (tjaden [14] · landesfeind [10]) 은 이를 AIChE J 59(5) 1446–1457 (2013) 으로 적는다 — 이 카드는 그 원문을 보지 않았다.
- 이 논문을 인용하는 정본 카드: `tjaden2018_tortuosity_review_calculation_approaches` (ref [13]: "τ² 는 높은 실험 τ 를 설명하려고 도입", τ_exp vs τ_geo) · `landesfeind2016_tortuosity_eis_electrodes_separators` (ref [6]: *"strictly distinguish between the effective tortuosity τ and the geometrical tortuosity τ_geo"* A1374) · `qin2026_bilayer_cathode_cgmd_dem_graded_thick_electrode` (ref [53], Holzer 틀).

---

## 3. 핵심 수치
> 이 논문은 소재 앵커 (porosity@P · σ_ion/e/thermal · E_SE · coverage · Z · Heckel) 를 **주지 않는다** → 전부 n/a.  주는 것은 ① 정의식 (§4-1) ② β · τ_geo · τ_elc · δ 의 측정값 (액체 격막 · LSC) ③ 측정 재현성 조건.

### 3-A. 본문 명시값 (stated, 쪽 순)
| 항목 | 값 | 조건 / 시료 | 쪽 |
|---|---|---|---|
| τ_geo (기하) | **≈ 1.6** (초록) · 평균 **1.62** — 두 계열 모두 ε 와 거의 무관 | olivine · wollastonite 격막 | p.2934 · p.2949 |
| τ_elc (EIS 역산) | **최대 5.6** ("unrealistically high") | 같음 | p.2949 |
| τ_exp 문헌 | 간접 측정으로 **최대 20** 까지 보고됨 — 입상 매질 경로의 기하 모형으로는 비현실적 [22] | 문헌 인용 | p.2937 |
| σ₀ | **0.645 S/cm** (25 wt% KOH) | 격막 기공 채움 전해질 | p.2940 |
| ε 범위 | olivine **0.27–0.44** · wollastonite **0.45–0.80** (탄소 기공 형성제 Sigradur 양으로 조절) | 일축 압축 성형체 **20 MPa** → **1300 °C** 소결 | p.2940 |
| EIS | 4-전극 셀 · **0.1–100 kHz** · Zahner IM6eX · 감지-기준 전극 사이 **0.75 V + 10 mV AC** · 절연 격막이라 허수부 없음 → **순수 저항** 만 | 격막 | p.2940 |
| SRµCT | SLS TOMCAT · 2048 장 · 2048 × 2048 px · 화소 **370 nm** · 15.5 keV · 시야 0.78 mm → 부분 입방체 **660³ voxel @ 740 nm** (binning) | 격막 | p.2940 |
| Archie m | **olivine 2.95 · wollastonite 2.31** (원문 배정) — ⚠ 벡터 추출 점으로는 재료가 뒤바뀐 꼴 (§3-C ⑥) | σ_eff = σ₀·ε^m 추세 | p.2948 |
| LSC 양극 | La₀.₆Sr₀.₄CoO₃₋Δ 화염 분무 · 이봉 (나노 **15–20 nm** + 마이크로 **> 1 µm**) · BET **29 m² g⁻¹** · 페이스트 고형 25 wt% (LSC **23 wt%** + 흑연 기공 형성제 Timrex KS4 d50 2 µm **2 wt%**) · Ce₀.₈Gd₀.₂O₁.₉ 위 스크린 인쇄 — 원문 *"using a 75-µm mesh with a thickness of 36 µm"* (36 µm 가 망 두께인지 인쇄층 두께인지 문장상 모호) · **850 °C** 소결 (시료 LSC2/G2N23_850_H) | 방법 시험 시료 | p.2939 |
| FIB-SEM | ZEISS NVision 40 (ETH EMEZ) · Pt 1 µm (20 × 20 µm) · 15 × 15 × 15 µm 자유 입방체 · 30 kV · 1.5 nA · ESB 1.2 kV · 2048 × 1536 px @ **7.5 nm** · 1300 장 @ **15 nm** 절편 → **15 nm** 등방 voxel · 관심 영역 **14.4 × 9.4 × 7.6 µm** | LSC | p.2939–2940 |
| 해상도 여유 | 평균 입자 **> 10 × voxel** (c-PSD r50 157 nm) · 좁은 목도 **4–5 × voxel** (MIP r50 66 nm) | LSC | p.2940 |
| MIP 모사 비용 | 약 1000³ voxel 에 **약 30 분** (다중 코어 · 96 GB RAM) — 더 큰 비용은 분할 매개변수 결정 같은 수작업 | LSC | p.2940 |
| β (LSC 고체상) | r_min 66 nm · r_max 157 nm → **β = 0.177** (그림 4) · 본문 **0.18** — *"documents the morphological limitations for transport processes (e.g. electronic or ionic conductivity), which are caused by the narrow contacts between the LSC-particles"* | LSC 입자상 | p.2943 · p.2944 |
| MIP-PSD 모양 | LSC 부피의 **> 90 %** 가 반지름 < 100 nm · **5 %** 만 > 200 nm · r30 70 nm → r70 55 nm (변동 **15 nm** 뿐) → r_min := **r50** | LSC | p.2944 |
| c-PSD r50 / MIP r50 | **2.5 배** (157 / 66) | LSC | p.2944 |
| ID_crit | **≈ 3 µm** (LSC) · 돌파 반경은 침투 깊이 **2–5 µm** = 최대 입자 반지름의 **2–5 배** 에서 도달 · 결론: *"For granular materials, ID_crit is approximately 2–5 times the radius of the largest particles"* | LSC | p.2943–2944 · p.2951 |
| 두께 시험 | 입방체 두께를 z 로 **75 nm 씩 1.5 µm 까지**, 그 뒤 **1.25 µm 씩 7.6 µm 까지** 늘려 MIP 반복 | LSC | p.2944 |
| LSC r_min · r_max vs 두께 | r_min 처음 **230 → < 100 nm (첫 2 µm)** → 3 µm 위 **66 nm 평탄** · r_max 는 > 6 µm 에서 **≈ 150 nm** 로 완만 · "β = **1.77**" 평탄 (⚠ 오식 의심 — §10 원문 대조 ③) · c-PSD 대표 두께 **> 6 µm** vs MIP ID_crit **3 µm** | LSC | p.2945 |
| 기공상 | MIP r50 **75 nm (입구) → 64 nm (4.5 µm)** → 5 µm 에서 작은 균열 때문에 '미니 돌파' → **84 nm** · β 기공 = **0.6 ± 0.05** · 기공 부피분율이 두께에 따라 **0.43 → 0.53** | LSC 양극 기공 | p.2945–2946 |
| 6 방향 침투 | LSC r50 **64 (± 1) nm** · 기공 r50 **84 ± 1 nm** — 방향 무관 | LSC | p.2946 |
| MIP-out (출구면만) | 6 방향 r50 이 **53–94 nm** 로 넓게 흩어짐 (본문 · 그림 9b 기공상 — 면적이 작아 대표성 부족) · 그림 9a: LSC MIP-out **52–63 nm**, "**up to 6 %** is apparently not connected" | LSC 양극 | p.2947 |
| MIP-in (입구면 평균) | LSC **154 nm** vs c-PSD 157 · 기공 **104 nm** vs c-PSD 108 → 3D c-PSD 사용 권고 | LSC (그림 10) | p.2948 |
| β–δ 사인 맞춤 | γ = aβ² + bβ + c, **a = 0.3 · b = 0.7 · c = 0** (Eq. 10) | 격막 8 점 | p.2950 |
| r_min vs r_max | 선: y = x (β = 1) · **y = 0.62x (β = 0.38)** · 맞춤 **y = 0.62x^1.12 (β 가변)** — β 가 기공 크기와 함께 커짐 | 격막 (그림 13) | p.2949 |
| σ_ion · σ_e · κ_th (고체) · porosity@P · E_SE · coverage · Z · Heckel | **n/a** | — | — |

### 3-B. 격막 8 시료 — 그림 11 · 12 · 13 · 14 · 15 · 16 벡터 추출 (≈, 본문 명시값 아님)
> 시료 짝짓기: 그림 11 · 12 · 14 의 ε 와 그림 13 · 15 의 β 가 같은 값으로 맞물리는 것으로 시료를 이었다 (O = olivine, W = wollastonite).  R = 비저항 [Ω·cm].  오른쪽 다섯 열은 **우리 산술**.

| 시료 | ε | σ_eff 측정 [S/cm] | τ_elc (그림 12) | τ_geo (그림 12) | r_max / r_min [µm] (그림 13) | β (그림 14) | δ (그림 15) | τ_geo/τ_elc | √τ_elc / τ_geo | τ_elc·ε^½ (Bruggeman 배수) | R 측정 / 예측 δ_geo / 예측 β (그림 16) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| O1 | 0.267 | 0.0306 | 5.61 | 1.62 | 2.87 / 1.87 | 0.425 | 0.285 | 0.289 | 1.46 | 2.90 | 32.6 / 34.2 / 22.1 |
| O2 | 0.322 | 0.0469 | 4.42 | 1.65 | 3.74 / 2.57 | 0.472 | 0.361 | 0.373 | 1.28 | 2.51 | 21.3 / 23.3 / 16.8 |
| O3 | 0.418 | 0.0740 | 3.63 | 1.56 | 4.80 / 3.74 | 0.607 | 0.440 | 0.430 | 1.22 | 2.35 | 13.5 / 10.4 / 9.53 |
| O4 | 0.443 | 0.1055 | 2.71 | 1.58 | 5.74 / 4.32 | 0.566 | 0.590 | 0.584 | 1.04 | 1.80 | 9.48 / 11.3 / 9.75 |
| W1 | 0.453 | 0.0629 | 4.63 | 1.58 | 3.30 / 2.40 | 0.529 | 0.345 | 0.342 | 1.36 | 3.12 | 15.9 / 12.6 / 10.2 |
| W2 | 0.522 | 0.0914 | 3.67 | 1.56 | 4.02 / 2.98 | 0.550 | 0.435 | 0.425 | 1.23 | 2.65 | 10.9 / 10.1 / 8.43 |
| W3 | 0.586 | 0.139 | 2.71 | 1.58 | 4.52 / 3.71 | 0.674 | 0.590 | 0.583 | 1.04 | 2.08 | 7.17 / 6.28 / 6.20 |
| W4 | 0.795 | 0.254 | 2.02 | 1.86 | 11.5 / 9.14 | 0.630 | 0.792 | **0.920** | **0.76** | 1.80 | 3.94 / 6.10 / 5.75 |

- τ_geo 8 점 평균 **1.62** (우리 산술) = 본문 평균 1.62 와 일치.  β (그림 13 의 (r_min/r_max)²) = 그림 14 의 β (차 ≤ 0.002).
- 예측 오차 (우리 산술, R_pred/R_meas − 1): **δ_geo 판 −23 … +55 %** (O3 −23 · W1 −21 · W4 +55 · 나머지 ±20 % 안) · **β 판 8 중 6 점 13–36 % 과소** (O4 +3 · W4 +46).  ⚠ δ_geo 의 사인 맞춤은 **같은 8 점** 으로 정했다 (표본 안 검사 — 외부 검증 아님).
- 그림 16 위 회색 추세선 (벡터 추출): δ-trend R_pred ≈ 1.03·R_meas − 0.5 · β-trend R_pred ≈ 0.60·R_meas + 2.5.
- Bruggeman 배수 τ_elc·ε^½ = T/T_Bruggeman (α = 0.5 관례 · 우리 산술): **1.8–3.1** (액체 격막).

### 3-C. 원문 안의 수치 정합 검사 (우리 산술 · 벡터 추출값)
| # | 검사 | 결과 |
|---|---|---|
| ① | τ_elc (그림 12) = ε·0.645/σ_eff (그림 11) | 8/8 차 ≤ 0.3 % → τ_elc 는 **Eq. 2 역산 그대로** (= 우리 tau2) |
| ② | δ (그림 15) = τ_geo/τ_elc = τ_geo·σ_eff/(σ₀·ε) | 7/8 차 ≤ 0.012 · **W4 만 0.792 vs 0.920** (그림 12 의 τ_geo 1.86 이면 0.92 · 그림 15 값이면 τ_geo ≈ 1.60 이어야 함) |
| ③ | 그림 16 β 예측 = R₀·τ_geo/(ε·β), R₀ = 1/0.645 | 8/8 차 ≤ 0.3 % |
| ④ | 그림 16 δ_geo 예측 = R₀·τ_geo/(ε·δ_geo), **δ_geo = [1 − cos(πγ)]/2** | 8/8 차 ≤ 0.3 % → 인쇄된 Eq. 9 의 **'+π/2' 는 부호 오식** (인쇄형 그대로면 δ_geo 0.33–0.73 = 보수값이 나와 그림 16 을 재현 못 한다) |
| ⑤ | 그림 11 '계산값' = σ₀·ε/τ_geo (본문 설명대로 Eq. 2 에 τ_geo 대입) | 8/8 이 정확히 **× 1.20** (1.200–1.203) — 같은 그림의 측정점 · 그림 12 · 15 · 16 은 σ₀ 0.645 와 맞는데 이 점들만 σ₀ ≈ 0.774 꼴 [원인 미확인] |
| ⑥ | Archie m (σ₀ 0.645 고정, 원점 통과 로그 맞춤) | olivine **2.33** · wollastonite **2.98** — 본문 배정 (olivine 2.95 · wollastonite 2.31) 과 **재료가 뒤바뀐 꼴**.  그림 11 에 그려진 추세선 자체는 자유 전인자 거듭제곱 (olivine ≈ 0.60·ε^2.25 · wollastonite ≈ 0.47·ε^2.52) 이고 라벨은 본문 배정을 따른다 [원자료 [37] 미열람 — 인용 금지 수준] |
| ⑦ | τ² 관례로 δ 를 다시 정의하면 (δ′ = τ_geo²/τ_elc) | W4 에서 **δ′ = 1.71 > 1** — δ ∈ [0, 1] (p.2937) 을 어긴다.  원문의 1 승 선택은 이 자료 안에서는 일관 |

---

## 4. 정의 · 방법 (정독) ★
> DEM 양식의 "시뮬레이션 방법" 칸 (code · 접촉법칙 · E·ν·μ · 서보 · RVE · seed) 은 **해당 없음** — 원문은 실측 미세구조의 3D 영상을 분석한다.  아래는 정의식 → 측정 사슬 순서.

### 4-1. 정의식 — 원문 식 번호 · 쪽 그대로
| 식 | 원문 형태 | 쪽 | 원문 이름 · 뜻 |
|---|---|---|---|
| **Eq. 1** | σ_r = σ_eff/σ₀ = 1/F = ε^m | p.2936 | relative conductivity σ_r · formation factor F = 1/σ_r · Archie 지수 m.  *"purely empirical … only holds for a series of samples from the same geological formation"* — 형태학적 특징을 구분하지 못한다 |
| **Eq. 2** | σ_eff/σ₀ = ε/τ, **0 ≤ ε ≤ 1, τ ≥ 1** | p.2936 | 지구과학 · 화공의 tortuosity 효과 식 ([22] Bhatia 1985).  측정 σ₀ · σ_eff · ε 를 넣어 푼 τ = **experimental tortuosity τ_exp** — *"must be strictly distinguished from the geometrical tortuosity (τ_geo)"* |
| **Eq. 3** | σ_eff/σ₀ = ε·δ/τ | p.2937 | constrictivity δ 를 더한 식 (van Brakel–Heertjes [29]).  δ ∈ [0, 1]: 0 = 막힌 기공 · **1 = 일정 반경 원기둥 기공**.  *"It contributes to a transport resistance, which is inverse proportional to the width of the bottlenecks."*  기하 정의가 없어 *"the constrictivity effect is tacitly included in (unrealistically high) τ_exp"* |
| **Eq. 4** | β_Petersen = A_max/A_min | p.2937 | Petersen [30] 단일 원통관 (쌍곡선 목, 주기 단면) 모형의 협착 인자 — A_min = 목 단면, A_max = 입구 / 비협착 '거품' 단면 |
| **Eq. 5** | D_eff/D₀ = 0.2122·ln(β_Petersen) | p.2937 | Petersen 그래프를 읽어 얻은 해석식 (원문 인쇄 그대로 — ⚠ β_P = 1 에서 0, 협착이 클수록 커지는 꼴: §10 원문 대조 ①).  Michaels [31]: 단면 변화 (β) 가 거품–목 간격보다 확산계수에 훨씬 큰 영향 |
| **Eq. 6** | **β = A_min/A_max = πr²_min/πr²_max = (r_min/r_max)²** | p.2938 | 이 논문의 constriction factor = 1/β_Petersen → 0–1 (δ 와 같은 방향).  무질서 미세구조에는 r_min · r_max 가 하나가 아니므로 **크기 분포** 로 정의 |
| **Eq. 7** | P_c = (2γ/R_c)·cos φ | p.2943 | (단순화한) Washburn 식 — 모세관 반경 R_c ↔ 압력 P_c (γ 표면장력, φ 젖음각).  MIP 모사의 곡률 = 침투 압력 |
| **Eq. 8** | δ = σ₀·τ_geo/(σ_eff·ε) (인쇄형) | p.2949 | 측정 (σ_eff, τ_geo, ε) 으로 δ 계산.  ⚠ 인쇄형은 Eq. 3 의 **역수** — 그림 15 값은 δ = σ_eff·τ_geo/(σ₀·ε) = τ_geo/τ_elc 를 따른다 (§3-C ②, §10 ④) |
| **Eq. 9** | δ_geo = [Sin((πγ) + π/2)]/2 + 1/2 (인쇄형) | p.2950 | β 에서 기하 constrictivity 예측 — 경계조건 (β = 1 → δ = 1 · β = 0 → δ = 0, p.2949–2950) 을 맞춘 사인 곡선.  ⚠ 인쇄 부호대로면 경계조건이 거꾸로 — 그림 15 곡선 · 그림 16 수치는 [1 − cos(πγ)]/2 (§3-C ④) |
| **Eq. 10** | γ = aβ² + bβ + c | p.2950 | a = 0.3, b = 0.7, c = 0 (a + b = 1 이라 γ(1) = 1 — 사실상 1 매개변수).  ⚠ 기호 γ 가 Eq. 7 (표면장력) 과 겹침 (약어표도 둘 다 적음, p.2934) |
| **Eq. 11** | **R_eff = R₀·τ_geo/(ε·δ_geo)** | p.2950 | 영상 매개변수 (ε · r_min · r_max · β · τ_geo) 만으로 비저항 예측.  τ_geo **1 승** (그림 16 재현으로 확인 — §3-C ④) |

### 4-2. τ 세 이름 — 원문의 구분
- **τ_exp** (experimental, p.2936): Eq. 2 를 측정값으로 푼 τ.  *"the geometrical aspects of τ_exp are always ill-defined because of the indirect determination method"* · *"experimental tortuosity is not a pure microstructure parameter, because it depends also on the transport regime and on the associated experimental parameters"* (수력 τ 는 압력 구배 · 점도 = 온도 · 조성 의존, p.2937).
- **τ_elc** (electrical, EIS 로 간접 결정 — 약어표 p.2934): 이 논문 격막에서의 τ_exp.  *"It is assumed that the high values for the electrical tortuosity do not signify such long pore pathways, but instead are caused by artefacts related to the indirect determination procedure. Other geometric features such as the constrictivity may be included in the electrical tortuosity"* (p.2949) · 그림 12 캡션: *"the experimental tortuosity erroneously includes the effect of bottlenecks, whereas the geometric tortuosity strictly only describes the pore paths lengths"*.
- **τ_geo** (geometric, 단층상에서 직접): *"The advantage of τ_geo … is the fact that it is geometrically defined (e.g. pore path lengths along the central axis are commonly measured)"* (p.2936).  불확실성 둘: ① skeleton 알고리즘 · 경로 정의가 3D 그래프 위상을 바꾼다 ② 경로 선택 기준 (최단 경로 [23] vs 최대 유동의 고투과 경로 [24]) — *"a proper use of τ_geo should always be based on a clear definition of the underlying algorithms to describe a reproducible methodology."*
- **τ vs τ² (p.2937)**: 높은 τ_exp 를 현실적으로 만들려고 **τ² 를 Eq. 2 에 넣는 관례** (Carman [2] · Kozeny [1] · Clennell [21]) · 유효 경로 길이 (l_eff)² 로 계산하는 저자들 → τ_Carman = (l_eff/l₀)², τ_Kozeny = l_eff/l₀ — *"which leads to considerable confusion"*.  원문 판정: 지수 2 는 엄밀히 유도되지 않았다.  대안 설명 = **간접 결정이 추가 기하 특징을 잘못 담는다** → 수송 모형에 그 특징 (협착) 을 따로 둔다 (Eq. 3).
- 원문은 수송 시뮬레이션 (FE · LB) 을 다루지 않는다: *"these simulations usually do not provide a quantitative description of the microstructure but rather they provide the effective transport properties directly"* (p.2936) → **flux 기반 τ 는 이 논문 틀에 없다**.

### 4-3. 가설 다섯 (p.2938)
| # | 가설 (요지) | 결과 (결론 절 p.2950–2951) |
|---|---|---|
| I | MIP 모사 → 협착 대표 치수 (통계 평균 r_min) | 확인 — 침투 방향 · 국소 불균질에 둔감 (두께 > ID_crit) |
| II | c-PSD → 비협착 거품 치수 (r_max) | 확인 — 단 불균질 · 구배에 더 민감 → 더 큰 부피 |
| III | MIP + c-PSD → 영상에서 β 직접 | 확인 — β 는 기공률 · 기공 크기와 양의 상관 → *"the bottleneck effect is stronger in low porosity materials and in fine-grained microstructures"* |
| IV | σ_eff (EIS) + τ_geo · ε (영상) → Eq. 3 으로 δ 간접 계산 → β (기하) ↔ δ (실험) 경험 관계 | 사인 함수 꼴 (Eq. 9–10) |
| V | 거시 유효 수송을 부피 평균 매개변수 (ε, r_min, r_max, β, τ_geo) + β–δ 관계로 계산 | 격막 두 계열에서 가능 — *"future studies will have to show for which types of materials, for which range of porosities and for which transport mechanisms (diffusion, conduction, flow) the fifth hypothesis is valid"* |
- 원문 자신의 한정어: *"the proposed parametric approach represents a heuristic solution and its validity has yet to be tested"* (p.2938) · *"no more than a heuristic approximation to a more complex problem"* (p.2951).

### 4-4. β 측정 사슬 — c-PSD · MIP 모사 (p.2941–2948, 그림 2–10)
| 단계 | c-PSD (r_max) | MIP 모사 (r_min) |
|---|---|---|
| 공통 개념 | 분할한 상 → **거리 지도** (각 voxel 의 상 경계까지 최단 거리) → 주어진 반지름의 구로 상을 경계를 넘지 않고 채울 수 있는 부피 분율.  구 곡률 = 침투 액체 (수은) 메니스커스 곡률 [20] | 같음 + **정해진 공간 방향의 침투** 단계 |
| 진행 | 거리 지도 극대점마다 큰 구에서 시작해 반지름을 줄이며 채운 부피 → 누적 곡선 (그림 2: 435 · 400 · 250 · 100 nm) | 곡률 반지름을 연속으로 줄인다 (= P_c 증가) — 반지름은 앞 경로의 **가장 작은 목** 을 통과해야만 다음 거품에 배정 → **병목 효과** |
| 무엇을 보나 | 목은 부피 기여가 작아 영향이 작다 → **부피 큰 거품 크기** (r_max) | 문턱 반지름에서 **돌파 (breakthrough)** → 큰 부피가 돌파 반지름에 배정 → **목 크기** (r_min) |
| 대표값 | **r50** (부피 50 % 분위) | **r50** — LSC 에서 r30 ↔ r70 차 15 nm 뿐이라 분위 선택 영향 작음 |
| 요구 부피 | 국소 불균질 (균열 · 상 분율 변화 · 큰 단일 입자) 에 민감 → LSC 에서 **> 6 µm** | 두께 > **ID_crit** (LSC ≈ 3 µm; 입상 2–5 × 최대 입자 반지름) 면 안정 · 균열이 시료를 관통하지 않으면 영향 작음 |
| 재현성 | MIP-in 6 방향 평균 ≈ c-PSD (그림 10) → **3D c-PSD 권고** | 6 방향 r50 ± 1 nm (그림 8) · MIP-out (출구면) 은 면적이 작아 53–94 nm 로 흩어짐 → **MIP-total 권고** |
| 상 | 기공 · 고체 둘 다 적용 (LSC 는 **고체 입자상** 에 침투 모사: *"the mercury intrusion, which is simulated through the network of the solid phase (not pores)"*, p.2943) | 같음 |
- 도구: 정렬 · 크롭 · 잡음 제거 · 분할 · 시각화 = Fiji · Avizo; 정량 (c-PSD · MIP-PSD) = 자체 Matlab · Java (Münch & Holzer [20]).

### 4-5. τ_geo 측정 (p.2941)
- 분할 기공망 → Avizo 의 voxel-skeleton (거리 지도의 능선을 세선화 → 기공 중심의 연결 voxel 사슬 · 중심 voxel 마다 최근접 경계 거리 저장) → 3D 그래프 [39] → **데이터 입방체 입구면 ↔ 출구면 최단 경로** 를 자체 Matlab 코드의 running Dijkstra [40] 로.
- 경로마다 **굽은 선의 길이 ÷ 입구–출구를 잇는 벡터의 길이** = τ_geo, 통계로 기술 (상세 Keller et al. [19, 41]).
- ⇒ 우리 τ_Dij 와 **같은 범주** (그래프 위 Dijkstra 최단 경로) 이나 그래프 (기공 skeleton vs SE 접촉 중심) · 분모 (입출구 벡터 길이 vs 두 끝 중심의 Δz) 가 다르다.

### 4-6. δ 의 역산과 예측 (p.2948–2950, 그림 11–16)
1. 측정 σ_eff (EIS) 는 ε 에 따라 지수적으로 오르고 두 재료가 다른 추세 (Archie m 이 다름) — m 은 *"do not explain which morphological features are controlling"* (p.2948).
2. **τ_geo · ε · σ₀ 를 Eq. 2 에 넣어 계산한 σ_eff 는 측정보다 훨씬 높고 두 재료가 한 추세** (그림 11) — 경로 길이 (τ_geo) 만으로는 형태를 못 담는다 (p.2949).
3. τ_geo ≈ 1.62 로 평평 vs τ_elc 최대 5.6 (그림 12) → 경로 길이가 아니라 **협착이 주된 미세구조 특징** (p.2949).
4. r_min vs r_max (그림 13): 일정 β 는 직선 · 실측은 약한 비선형 (y = 0.62x^1.12) → **기공이 클수록 β 증가**; β vs ε (그림 14): **기공률이 낮을수록 협착 강함**; 두 재료가 한 선에 안 놓임 — 입자 모양 (olivine 회전타원 · wollastonite 섬유) 차로 추정.
5. δ (Eq. 8, 역산) vs β (그림 15): β 0.4–0.6 에서 대각선 (β = δ) 보다 가파른 추세 → 경계조건 (0, 0) · (1, 1) 의 **사인 곡선** (Eq. 9–10).
6. 예측 (Eq. 11, 그림 16): δ_geo 판은 대각선을 따른다 · β 를 그대로 넣으면 (흰 기호) 대각선 아래 = **실제 저항 과소** · 작은 저항에서는 차가 작고, 전도도로 보면 더 작다 ([37]).

### 4-7. 입자 처리 ★ (DEM 양식 항목)
- **해당 없음** — 입자 모형이 없고 실측 소결체의 3D 영상을 분석한다.  c-PSD · MIP 의 '구' 는 크기 탐침이지 입자가 아니다 (이산 객체 분할의 어려움을 피하려고 고안한 **연속 크기 분포**, p.2941).
- 우리 축과 닿는 점: LSC **고체 입자상의 목** (소결 나노 입자 접촉) 을 β = 0.18 로 정량하고 그것이 전자 · 이온 수송을 제한한다고 적는다 (p.2944) — 단 **그 상의 수송 (δ) 은 재지 않았다**.  수송까지 잰 것은 액체 기공 (격막) 뿐이다.

### 4-8. 기법 미니 용어집
| 용어 | 원문 설명 (쪽) | 우리 쪽 대응 |
|---|---|---|
| relative conductivity σ_r | σ_eff/σ₀ (Eq. 1, p.2936) | **f** |
| formation factor F | 1/σ_r (Eq. 1) | 1/f = N_M (⚠ 우리 docstring 의 'formation factor' = σ_eff/σ_input 은 역수 — 메모 v2 `TAU-17`) |
| Archie 지수 m ('m-factor') | σ_r = ε^m (Eq. 1) | f = φ^m 의 지수 (Bruggeman m = 1.5) — **M-factor 아님** |
| experimental / electrical tortuosity τ_exp · τ_elc | Eq. 2 역산 τ = ε σ₀/σ_eff (p.2936 · p.2949) | **tau2** (우리 규칙상 'tortuosity factor') |
| geometric tortuosity τ_geo | skeleton 최단 경로 ÷ 입출구 벡터 (p.2941) | **τ_geo** (`tau_geo_SE_dij` 등) |
| constrictivity δ | Eq. 3 의 협착 인자, Eq. 8 로 역산 (p.2937 · p.2949) | 열 없음 — τ_Dij / tau2_FULL 로 만들 수 있다 (§8) |
| geometric constrictivity δ_geo | β 에서 사인 예측 (Eq. 9–10) | 없음 |
| constriction factor β | (r_min/r_max)² (Eq. 6) | 없음 — FULL/CF 와 다른 양 |
| β_Petersen | A_max/A_min = 1/β (Eq. 4) | — |
| c-PSD | 거리 지도 구 채우기 연속 크기 분포 (p.2941) | 없음 (우리 입자는 구라 반지름이 주어짐) |
| MIP 모사 · 돌파 반경 · ID_crit | 방향성 침투 · 문턱 곡률 · 돌파까지 침투 깊이 (p.2943–2944) | 없음 — 망에서 같은 뜻은 '임계 접촉 반경' (§8 ③) |
| MIP-total / MIP-out / MIP-in | 전체 부피 / 출구면 / 입구면 PSD (p.2947–2948) | — |
| bottleneck effect | 목이 수송을 지배하는 효과 (p.2943) | Holm 협착 R_c = 1/(2σa) ∝ 1/a (같은 스케일링 — 우리 해석) |

---

## 5. Figure set ★
| Fig | 쪽 | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|---|
| 1 | p.2939 | 원자료 2D 단면 — (a) LSC FIB 7.5 nm (14.25 µm 폭) (b) olivine 격막 SRµCT 740 nm (ε 32 %, 488.4 µm 폭) | 두 길이 척도 (nm 고체 목 · µm 기공) |
| 2 | p.2942 | c-PSD 방법 (Münch & Holzer [20] 재수록): 기공 → 거리 지도 → 반지름 435 → 400 → 250 → 100 으로 구 채우기 → 누적 c-PSD 곡선 | 크기 분포를 '이산 객체' 없이 정의하는 법 |
| 3 | p.2943 | LSC FIB 부피 (14.4 × 9.4 × 7.6 µm): (a) c-PSD 반지름 색 (0–1200 nm) (b) MIP 모사 (오른쪽 y–z 면에서 x 방향 침투, 0–820 nm, 끊긴 입자 검정) | 고체 입자상에 침투 모사 — 입자 목 = 병목 |
| 4 | p.2943 | LSC 상 c-PSD vs MIP-PSD 누적 곡선 — **r50 MIP 66 nm (r_min) · r50 c-PSD 157 nm (r_max) → β = 0.177** · MIP 의 '돌파' 수직 강하 | ★ **β 정의의 그림 한 장** — 크롭 1 순위 |
| 5 | p.2945 | MIP 모사 3D: (a) LSC — 입구 쪽 큰 반지름 → ≈ 3 µm (ID_crit) 뒤 균일 파랑 (b, c) 기공 — 협착 약함 · 뒤쪽 왼편 균열이 돌파 유발 가능 | ID_crit · 국소 균열의 영향 |
| 6 | p.2946 | 두께 75 nm → 7.5 µm 의 MIP-PSD 묶음 — (a) LSC: 두께↑ 에서 불연속 뚜렷, r50 은 ID_crit 위에서 66 nm 고정 (b) 기공: 덜 민감, 5 µm 에서 '미니 돌파' | 침투 깊이 vs 대표성 |
| 7 | p.2946 | 두께에 따른 r_min · r_max · β (+ LSC 분율 · 기공률) — (a) LSC β ≈ 0.1 (ID_crit) → ≈ 0.17 (7.6 µm) (눈 판독) (b) 기공 β ≈ 0.6 | ★ RVE 조건 — r_min 은 3 µm, r_max 는 > 6 µm 필요.  크롭 후보 |
| 8 | p.2947 | 6 방향 MIP-PSD (회색) vs c-PSD (검정) — LSC r50 64 · 157 nm, 기공 84 · 108 nm | 방향 재현성 ± 1 nm |
| 9 | p.2947 | MIP-out (출구면) 6 방향 — LSC 52–63 nm, 기공 53–94 nm · "up to 6 % … not connected" | 2D 면 통계의 한계 |
| 10 | p.2948 | MIP-in (입구면) 6 방향과 평균 vs c-PSD — 평균 154 ↔ 157 (LSC) · 104 ↔ 108 (기공) | r_max 는 3D c-PSD 로 |
| 11 | p.2948 | 격막 σ_eff vs ε — 측정 (EIS) 두 계열 + Archie 추세선 (m 2.95 · 2.31 라벨) + **τ_geo 로 계산한 σ_eff (훨씬 높음, 한 추세)** | ★ "경로 길이만으로는 σ 를 못 낸다" — 크롭 후보.  ⚠ 라벨 m 배정 · 계산값 × 1.20 (§3-C ⑤⑥) |
| 12 | p.2949 | **τ_geo (≈ 1.6, 평평) vs τ_elc (2.0–5.6)** vs ε | ★ τ_exp (= tau2) ≠ τ_geo 의 핵심 그림 — 크롭 1 순위.  축 이름은 둘 다 'Tortuosity (τ)' 인데 한쪽은 tau2 양, 다른 쪽은 경로 비 |
| 13 | p.2949 | r_min (MIP r50) vs r_max (c-PSD r50) [µm] — y = x (β 1) · y = 0.62x (β 0.38) · 맞춤 y = 0.62x^1.12 | 격막 기공 r_max 2.9–11.5 µm (벡터 추출) — 우리 SE 입자 크기와 비슷한 척도지만 상이 반대 |
| 14 | p.2950 | β vs ε — 기공률↓ → β↓ (협착↑), 두 재료가 한 선에 안 놓임 | 협착이 충전 상태와 같이 움직인다 (우리 Z 섞임 문제와 같은 꼴) |
| 15 | p.2950 | **δ (EIS 역산) vs β (영상)** + 사인 맞춤 + 대각선 β = δ | ★ **기하 β ≠ 수송 δ** — 크롭 1 순위.  사인 곡선은 (0,0)–(1,1) 을 지나 β 0.5 에서 ≈ 0.38 (Eq. 9 인쇄 부호와 반대) |
| 16 | p.2950 | 예측 비저항 (Eq. 9–11) vs 측정 (EIS) — δ_geo 판 (검정, 대각선 근접) · β 판 (흰색, 아래 = 과소) · 범례 "R_predicted = R₀*τ_geo/ε*x, where x = δ or β" | ★ 분해식 지수 확인 (τ_geo 1 승) — 크롭 후보.  ⚠ 범례 식은 'x 를 곱함' 처럼 읽히나 수치는 ÷(ε·x) |

## 6. Post-processing ★
- **무엇**: 분할 기공률 ε · skeleton 그래프 Dijkstra τ_geo · 거리 지도 c-PSD (r_max) · 방향성 MIP 모사 PSD (r_min, 돌파) · β = (r_min/r_max)² · 4-전극 EIS 순수 저항 → σ_eff · Archie 추세 · Eq. 2 역산 τ_elc · Eq. 3 역산 δ · δ–β 사인 맞춤 · Eq. 11 예측 · 예측 vs 측정 대각선 비교.
- **도구**: Fiji · Avizo (skeleton) · 자체 Matlab · Java (c-PSD · MIP 모사 · Dijkstra) · ZEISS NVision 40 FIB-SEM · SLS TOMCAT SRµCT · Zahner IM6eX.
- **수치화 규약**: 분포의 대표값은 **r50** · 두께 시험 (ID_crit) · 6 방향 시험 · MIP-total / -out / -in 비교로 대표성 판정 · 예측은 측정과 같은 단위 (비저항 Ω·cm) 대각선 그림.
- **품질 점검 항목**: voxel 대비 특징 크기 (입자 > 10 voxel, 목 4–5 voxel, p.2940) · 시료 두께 > ID_crit · c-PSD 는 더 큰 부피 · 불균질 (균열 · 상 분율 구배 · 큰 단일 입자) 영향.

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md`
> ⚠ 기준값 파일은 이 브랜치에서 자리표시다 (`our_dem_baseline.md` §1) — 아래 우리 쪽 수치는 메인 리포 판단 메모 v2 (`docs/reviews/tau_conventions_judgment_v2_20261003.md`) 의 (유도) 값과 CLAUDE.md 서술에서 가져왔고, 절 번호를 단다.
> frame[5]: 이 논문은 **수송 기술자 (transport descriptor) 반쪽** — 영상 기하 서술자 + 측정 수송.  역학 · 형상 변화 · 압밀 물리는 없다 (우리 MPM 반쪽에 해당하는 것 없음).  frame[4]: 이 논문 값으로 우리 모델을 맞추지 않는다 — **정의 · 분해 틀** 만 가져온다.

| 항목 | 이 논문 | 우리 | 같음 / 다름 · 이유 |
|---|---|---|---|
| 전도상 | 액체 KOH 가 채운 **기공** (연속상) | **SE 입자** (DEM 구 · 점접촉망) | 위상 반대 — 병목이 기공 목 vs 입자 접촉 목 |
| 미세구조 | 실측 소결 세라믹 3D 영상 (740 nm · 15 nm voxel) | LIGGGHTS 구 충전 (강체 + 겹침) | 우리 병목 크기는 영상 해상도가 아니라 겹침 → 접촉 반경 a 가 정한다 |
| σ₀ | **벌크 액체 0.645 S/cm** (구조 없음) | σ_grain 3.0 mS/cm = **펠릿값** (원장 CL-91 · 펠릿 안의 입자 목 포함) | **기준 상태 다름** — Holzer 형 분해 (δ 가 '모든 협착') 는 구조 없는 σ₀ 를 전제한다 |
| tau2 | τ_elc **2.0–5.6** (벡터 추출) | T_H 1.945–3646, 중앙 6.212 (메모 v2 §2 T17, 유도) | 정의식 같음 · 값은 다른 계 (전이 불가) |
| τ_geo | 1.56–1.86, 평균 1.62 — 기공 skeleton · 입출구 벡터 분모 | τ_Dij 1.149–17.49, 중앙 1.484 (메모 v2 T01) — SE 중심 꺾은선 · Δz 분모 | **같은 범주**, 이산화 · 분모 다름 |
| 분해 | **tau2 = τ_geo/δ** (선형, 기준 = 기하 τ) | **FULL/CF** = σ_CF/σ_full (같은 망, R_c 켜고 끔) | **다른 분해** — 기준이 τ_geo 냐 CF 냐 |
| 협착 기구 | 기공 목 (가변 단면) — *"resistance … inverse proportional to the width of the bottlenecks"* (p.2937) | Holm R_c = 1/(2σa) ∝ 1/a (FULL 에만) | 같은 스케일링 (우리 해석) — '협착' 이라는 이름의 기구는 같다 |
| δ = 1 기준 상태 | 일정 반경 원기둥 → σ_r = ε/τ_geo · τ ≥ 1 (Eq. 2) | CF = 반쪽마다 입자 단면 πr² 원기둥 · φ 는 구 부피 합 → T_CF < 1 이 26/157 (메모 v2 §3-6) | CF 는 그 기준 상태의 **망 판** 이지만 부피 비보존이라 원문 영역 (τ ≥ 1) 밖 |
| T_CF vs τ_geo | (기준 상태라면 T = τ_geo) | 중앙값끼리 T_CF 1.454 ÷ τ_Dij 1.484 ≈ **0.98** (메모 v2 §3-8 · T01; 우리 산술 — 침대별 비의 분포 아님) | 평균적으로 CF 는 원문 δ ≈ 1 자리에 앉지만 침대별로는 T < 1 이 있어 기준으로 못 쓴다 |
| 고체 목 β | LSC 소결 입자 목 **0.18** (수송 미측정) | 평균 a/r_SE 0.30–0.44 (메모 v2 §0 ⑤) → (a/r)² ≈ 0.09–0.19 (우리 산술) | 크기 대역만 비슷 — **정의 다름** (원문 r_min = 부피 가중 돌파 반경 r50, 우리 a = 접촉별 · (평균)² ≠ 평균 제곱) → 비교 주장 아님 |
| 비기하 계면 저항 | 없음 (액체 연속) | 없음 (FULL 의 Holm 도 완전 접촉의 기하 퍼짐 저항) | 둘 다 없다 — 원문 틀은 계면 저항을 다루지 않는다 |
| Bruggeman 배수 (T·ε^½) | 1.8–3.1 (우리 산술, 액체 격막) | H 중앙 3.40 (IQR 2.54–6.71) (메모 v2 §3-5) | 같은 축에서 말할 수 있다 — 다른 계 |
| 예측 검증 | δ_geo 8 점 표본 안 (−23 … +55 %) | 접촉망 = 수송 해 (외부 실험 대조는 결정 4 게이트 뒤) | 원문 예측은 같은 자료로 맞춘 사인식 |
| 수송 시뮬레이션 | **없음** (FE · LB 를 일부러 제외, p.2936) | 접촉망 Kirchhoff + STEP3 복셀 FV | 원문 틀에는 flux τ 가 없다 — 우리 FULL 해가 원문의 '측정 σ_eff' 자리에 온다 |

- **같은 양이 되는 조건 (우리 → Holzer 틀)**: ① ε → φ_SE (총 SE 부피분율) ② σ₀ → **구조 없는** SE 내부값 (펠릿값이면 펠릿 안 목 협착이 σ₀ 로 빠진다) ③ σ_eff → FULL 해 (전체 단면 정규화, 관통 z) ④ τ_geo → τ_Dij 계열 (분모 · 그래프 정의를 메타로) ⑤ 분해식의 τ_geo 지수 = **1** (원문 관례).
- **입경비 · 2D/3D**: 원문은 3D (단층) · 입자 모형 없음.  격막 기공 µm 척도 · LSC 나노 입자 — 우리 SE (생산 기본 r_SE 0.5 µm, CLAUDE.md) · 코퍼스 r_SE/r_AM 0.10–0.47 (메모 v2 §3-8) 과 직접 대응하는 '입경비' 개념이 없다.

---

## § τ 정의 대조 — 우리 규약 매핑
> 우리 규약 (CLAUDE.md ★★ τ 명명 규약 · 1저자 비준 2026-10-03): **f** = σ_eff/σ₀ · **tau2** = φ·σ₀/σ_eff (= 'tortuosity factor', 옛 이름 T) · **tau** = √tau2 · **τ_geo** = 최단 경로 / 두께 (수송 τ 아님) · **τ_e** = electrode tortuosity factor (우리에 없음).
> σ₀ 기준: 이 논문 = **벌크 액체 전해질** (25 wt% KOH, 0.645 S/cm, 구조 없음) · 우리 = 펠릿값 σ_grain 3.0 mS/cm (CL-91).

| 원문 기호 (식 · 쪽) | 원문 이름 | 원문 정의 · 정규화 | 우리 양 | 판정 · 환산 |
|---|---|---|---|---|
| **σ_r** (Eq. 1, p.2936) | relative conductivity | σ_eff/σ₀ — 거시 유효 / 구조 없는 매질 | **f** | 같은 양 |
| **F** (Eq. 1) | formation factor | 1/σ_r | 1/f = N_M | 같은 양.  ⚠ 우리 `network_conductivity.py` docstring 의 'formation factor' (= f) 는 역수 (`TAU-17`) |
| **m** (Eq. 1) | Archie 지수 ('m-factor') | σ_r = ε^m | f = φ^m 의 지수 | 구형 Bruggeman m = 1.5.  M-factor 와 이름만 비슷한 다른 양 |
| **τ** (Eq. 2, p.2936) | tortuosity | σ_eff/σ₀ = ε/τ, **τ ≥ 1**, 1 승 (Kozeny 형) | 식의 자리 = **tau2** | 원문은 이 τ 를 경로 길이 비로 **해석** 하지만, 측정값을 넣어 풀면 tau2 가 나온다 |
| **τ_exp** (p.2936) | experimental tortuosity | 측정 σ₀ · σ_eff · ε 로 Eq. 2 를 푼 τ = ε·σ₀/σ_eff | **tau2** | **같은 양** — 원문 이름에 'factor' 없음.  우리 규칙상 표기는 'tortuosity factor (tau2)' |
| **τ_elc** (p.2934 · p.2949 · 그림 12) | electrical tortuosity (EIS) | τ_exp 의 EIS 판 — 관통 4-전극 순수 저항 | **tau2** | 같은 양 (그림 12 = ε·0.645/σ_eff, 8/8 ≤ 0.3 % — §3-C ①).  σ₀ = 벌크 액체 |
| τ_Carman = (l_eff/l₀)² · τ_Kozeny = l_eff/l₀ (p.2937) | (문헌 사례) | 같은 '경로' τ 의 두 관례 | τ_geo² · τ_geo | 원문이 '혼동' 사례로 든다 — τ² 관례는 맞춤 편의 |
| **τ_geo** (p.2936 · p.2941) | geometric tortuosity | skeleton 그래프 Dijkstra 최단 경로 ÷ 입구–출구 벡터 길이 | **τ_geo** (`tau_geo_SE_dij` · τ_Dij,all · 벽 τ) | **같은 범주** — 그래프 (기공 skeleton ↔ SE 접촉 중심) · 분모 (입출구 벡터 ↔ Δz) 다름 → 메타로 적는다 (원문 요구: 알고리즘 명시) |
| √τ_elc | (원문에 없음) | — | **tau** | 원문은 √ 값을 쓰지 않는다 |
| **δ** (Eq. 3 · 8) | constrictivity | δ = τ_geo·σ_eff/(σ₀·ε) = **τ_geo/τ_exp** (Eq. 3 꼴 — 인쇄된 Eq. 8 은 역수) · ∈ [0, 1] | 열 없음 | 만든다면 **τ_Dij / tau2_FULL** (선형 · 기준 = 기하 τ) — 잔차 성격 (§8) |
| **δ_geo** (Eq. 9–10) | geometric constrictivity | β 에서 사인 예측 | 없음 | 보정 범위 β 0.42–0.67 (액체 기공 8 점) — 밖 외삽 금지 |
| **β** (Eq. 6) | constriction factor | (r_min/r_max)², r_min = MIP r50 (돌파), r_max = c-PSD r50 | 없음 | **FULL/CF 와 다른 양** (기하 vs 수송) |
| **β_Petersen** (Eq. 4) | Petersen constriction factor | A_max/A_min = 1/β | — | — |
| **ε** | porosity | 단층촬영 분할 기공률 (총 / 연결 구분 이 논문 미기술 [미확인]) | **φ_SE** (구 부피 합 · 전 SE) | 같은 자리 (전도상 부피분율) |
| **σ₀ · R₀** | intrinsic conductivity / resistivity of electrolyte | 0.645 S/cm · R₀ = 1/σ₀ | σ_grain (3.0, 펠릿) | **기준 상태 다름** |
| **R_eff** (Eq. 11) | effective resistivity | Ω·cm (거시) | 1/σ_full | 같은 자리 |
| τ_e | — | — | (우리에 없음) | 원문 EIS 는 관통형 (절연 격막 · 순수 저항) — 전극 τ_e (대칭셀 TLM) 와 다르다 |

- ⚠ **같은 그림 축 이름 'Tortuosity (τ)' 에 두 양** (그림 12): τ_elc 는 tau2 양, τ_geo 는 경로 비.  원문은 둘을 같은 축에 그려 '격차' 를 보이고 그 격차를 δ 로 부른다 — 우리가 이 그림을 인용할 때 **축을 둘로 나눠 이름 붙여야** 한다.
- ⚠ **COMSOL 표기와의 관계** (판정은 메모 v2 결정 5 소관): 원문 Eq. 2 의 τ 는 COMSOL τ_F (f = ε/τ_F) 와 **같은 자리** (1 승) 다 → 이 논문도 "τ 칸 = tau2" 관례의 한 예다.

---

## 8. 적용 인사이트 (내 연구에 어떻게)

### 협착 (constrictivity β) 정량 틀
> 이름표 그대로 둔다.  ⚠ 원문에서 **constrictivity = δ** (수송 역산) 이고 **β = constriction factor** (기하) 다 — "constrictivity β" 는 원문의 두 양을 한 이름으로 합친 것이니, 우리 문서에서는 β (기하) 와 δ (수송) 를 따로 부른다.

**(가) 틀 자체 — 원문이 주는 것**
| 층 | 원문 양 | 무엇에서 | 우리 쪽 대응 |
|---|---|---|---|
| 기하 · 경로 | τ_geo | 영상 skeleton Dijkstra | τ_Dij 계열 (`tau_geo_SE_dij`) |
| 기하 · 목 | β = (r_min/r_max)² | 영상 c-PSD · MIP 모사 (솔브 없음) | **없음** — 만든다면 접촉 반경 분포의 기하 서술자 (③) |
| 수송 · 전체 | τ_exp = τ_elc = ε σ₀/σ_eff | 측정 σ_eff | **tau2_FULL** (우리 FULL 해가 '측정 σ_eff' 자리) |
| 수송 · 잔차 | δ = τ_geo/τ_exp (Eq. 3, τ_geo 1 승) | τ_exp 와 τ_geo 의 비 | 열 없음 — τ_Dij / tau2_FULL (②) |
| 기하 → 수송 다리 | δ_geo = sin 맞춤 (β) | 경험식 (8 점) | 없음 |
| (원문 밖) | — | — | **tau2_CF · FULL/CF** — 같은 망의 R_c 0 가지와 그 비 |

- 분해식: **σ_eff/σ₀ = ε·δ/τ_geo ⇔ tau2 = τ_geo/δ** — 지수 전부 1 (맞춤 지수 없음) · τ² 관례 배제 (p.2937) · 그림 16 수치 재현 (§3-C ④).  "M-factor (ε·β/τ²)" 꼴과 그 지수는 이 논문에 없다 — 후속 문헌이 있다면 이 카드는 확인하지 않았다 [미확인].
- β 측정법: r_max = c-PSD r50 (거품) · r_min = MIP 모사 r50 (돌파 반경) · 두께 > ID_crit (입상 2–5 × 최대 입자 반지름) · c-PSD 는 더 큰 부피 · 6 방향 ± 1 nm (§4-4).
- 원문의 핵심 경험: **β ≠ δ** — 같은 시료에서 기하 협착 (β 0.42–0.67) 과 수송 협착 (δ 0.29–0.79) 이 다르고, β 를 δ 자리에 넣으면 저항을 과소 예측한다 (8 중 6 점 13–36 %, 우리 산술).

**(나) 결정 11 — CF 의 지위 · FULL/CF 의 이름이 이 틀과 맞나 → 맞는다 (권고 유지)**
1. **CF = "모델 내부 기준선" ✓** — 원문의 무협착 기준 상태는 δ = 1 = *"cylindrical pores with constant radius"* (p.2937) · *"pores form straight pipes"* (p.2950) 이고, 그때 σ_r = ε/τ_geo (Eq. 2) 이며 **τ ≥ 1** 이 식의 영역이다 (p.2936).  우리 CF 는 반쪽마다 입자 단면 πr² 의 **일정 단면 원기둥** 을 잇는 망이라 그 기준 상태의 망 판이지만, φ 를 구 부피 합으로 세어 부피 비보존 → T_CF < 1 이 26/157 (메모 v2 §3-6) → **원문 영역 밖**.  따라서 원문의 기준 상태라 부를 수 없고 '모델 내부' 기준선이 맞다.  (중앙값끼리 T_CF ≈ τ_Dij — §7 — 라 평균적으로는 원문 기준 상태 자리에 앉는다는 점도 같이 적을 만하다.)
2. **FULL/CF = "모델 내부 협착 비" ✓** — 기구는 원문의 협착과 같다 (목 폭에 반비례하는 저항, p.2937 ↔ Holm ∝ 1/a).  그러나 원문의 수송 협착 δ 는 **기하 τ_geo 를 기준** 으로 한 잔차이고, 기하 협착 β 는 **크기 분포의 비** 다.  FULL/CF 는 기준이 CF (원문에 없는 가지) 인 수송 비라 **δ 도 β 도 아니다**.  ⇒ 영문 표기에 *constrictivity* · *constriction factor* 를 쓰지 않는다 (원문 이름과 충돌).  T 기준으로 FULL/CF = 1/δ_model (기준 = CF) 꼴이라는 점만 대응으로 적는다.
3. 결정 11 의 근거 문장 *"연속체는 Wiener f ≤ φ (T ≥ 1) 를 지켜야 한다"* 에 **원문 근거 하나를 더 붙일 수 있다**: Holzer Eq. 2 의 정의역 τ ≥ 1 (p.2936).

**(다) TAU-07 ('geom' 오명 · CF 지위) → 원문이 TAU-07 을 지지한다**
- 원문에서 아래 첨자 'geo' 는 **영상 기하에서 (수송 자료 없이) 나온 양** 에만 붙는다: τ_geo (skeleton 경로) · δ_geo (β 로부터의 예측).  EIS 로 역산한 수송 양 (δ, τ_elc) 에는 'geo' 가 없다.  ⇒ 수송 솔브 (협착 0 이라도) 인 τ_Lap,geom 에 'geom' 을 붙이는 것은 원문 용법과도 어긋난다 — TAU-07 의 개명 방향과 같다.

**(라) TAU-08 (협착 비의 이름 · 정의) → 원문이 주는 정의 둘, 우리 비는 셋째**
- 원문 틀에서 '협착' 을 이름에 쓸 수 있는 양은 β (기하) 와 δ (= τ_geo/tau2, 수송 잔차) 둘뿐이다.  웹앱 "Constriction overhead" (τ_Lap,eff/τ_Dij = √tau2/τ_geo) 는 1/√δ′ (δ′ = τ_geo²/tau2 = **τ² 관례** 의 협착도) 꼴이라 원문 δ (τ_geo **1 승**) 와 지수 관례부터 다르다 — 원문 틀을 빌리려면 tau2/τ_geo (= 1/δ, 선형) 로 쓰고 이름은 "Holzer 형 1/δ (잔차)" 로, 아니면 메모 v2 대로 "flux ÷ 기하" 로 둔다.
- 같은 망 FULL/CF 는 원문에 없는 셋째 정의 — 메모 v2 의 이름 ("모델 내부 협착 비 (원기둥 bulk 기준)") 그대로 두고, **기하 서술자 (β 류) 와 섞지 않는다** (원문이 β ≠ δ 를 보였듯 우리도 (a/r)² 같은 기하 비가 FULL/CF 를 대신하지 못한다).

**(마) 판단 메모 v2 §3-5 → 결론은 서고, 근거 문장 둘을 고칠 후보 (§10 정정 후보 ①②)**
- *"웹앱 "Constriction overhead" (τ_Lap,eff/τ_Dij ≈ 1.7) 는 협착으로 읽을 수 없다 — 접촉 저항이 없는 연속 기공상도 1.24–1.59 를 낸다"* — 원문 틀에서는 연속 기공상의 flux/기하 격차 **자체가 협착** (기공 목, δ < 1) 이다: δ = 1 은 일정 반경 원기둥뿐 (p.2937) 이고, τ_elc 와 τ_geo 의 격차를 원문이 병목 효과로 돌린다 (그림 12 캡션 · p.2949) — Tjaden 도 같은 격차를 *"constrictions and pore necks"* 로 설명한다 (tjaden 카드 p.56).  ⇒ 바른 문장: "Constriction overhead 는 **접촉 (Holm) 협착 배수** 로 읽을 수 없다 — 연속 기공상의 목 협착 (원문 δ) 과 계산 정의 차가 같은 비에 들어간다".
- 표 행 (요지): √T_CF/τ_Dij 중앙 0.80 ↔ Tjaden "flux ≥ 기하" → "우리 CF 는 반대 방향" — √ 척도의 방향 검사는 원문 자료에서도 갈린다: 실측 액체 기공망 W4 (ε 0.80) 는 √τ_elc/τ_geo ≈ **0.76** (벡터 추출 · 우리 산술 — 한 점, skeleton τ_geo 의 부풀림 가능성).  원문 틀 (선형) 에서는 8/8 이 tau2 ≥ τ_geo (δ ≤ 1) 다.  ⇒ CF 결함의 근거는 **T_CF < 1 (Wiener · 원문 τ ≥ 1)** 이지 √T_CF/τ_Dij < 1 이 아니다.

**(바) 결정 16 묶음에 주는 그 밖의 인사이트**
- ① **CL-81 읽기 보강 (결정 11 의 복셀 ÷ 접촉망 대조 사전등록)** — 원문 틀에서 협착 δ 는 **단면 변화의 기하가 만드는 수송 효과** 다.  목을 해상하는 복셀 FV 는 해상도만큼 δ < 1 을 스스로 낸다 (CLAUDE.md CL-81 절도 *"기하 협착은 격자를 조이면 좋아진다"* 고 적는다).  반면 접촉망 CF 는 목을 πr² 원기둥으로 바꿔 협착을 0 으로 지운다.  ⇒ "복셀 σ 는 CF 가지 위" 는 **비기하 계면 저항 항이 0** 이라는 뜻으로만 맞고, 복셀 ÷ CF 비에는 (i) CF 과전도 (메모 v2 × 1/(0.6–0.8)) 와 (ii) **복셀이 해상한 목 협착 (d_h/dx 의존)** 이 함께 섞인다 → (ii) 도 사전등록 항목에 올린다 (우리 해석 · 미검증 — 권고 변경 아님, 보강).
- ② **Holzer 형 보조 서술자 후보 δ_net = τ_Dij / tau2_FULL** (선형) — 기준선을 CF 대신 이미 계산하는 기하 τ 로 둬 CF 부피 비보존 문제를 피한다.  대가: (a) 잔차다 — 원문도 τ_elc 에 인공물이 들어갈 수 있다고 적는다 (p.2949) (b) τ_geo 지수 관례 (1 vs 2) 에 따라 δ 가 τ_geo 배 (≈ 1.5 배) 달라진다 — 원문은 1 (c) τ_Dij 는 SE 중심 꺾은선 · Δz 분모 (원문은 skeleton · 입출구 벡터).  메모 v2 중앙값끼리 1.484 ÷ 6.212 ≈ 0.24 (우리 산술 — 분포 아님 · hertz 1세대 R_c 과대 · 펠릿 σ₀ 이중계상 포함) 로 원문 격막 δ 0.29–0.79 보다 작다.  열을 만든다면 τ 지수 관례 · τ_geo 정의를 메타로.  (결정 11 권고 변경 없음 — 선택 사항)
- ③ **β 의 망 판 (기하) 후보** — 원문 r_min 은 침투 모사의 **돌파 반경** 이 지배하는 r50 (p.2943–2944) = 퍼콜레이션 문턱의 목 크기다.  접촉망에서 같은 뜻의 양은 "접촉을 a 큰 순으로 켤 때 관통이 처음 생기는 임계 접촉 반경 a_c" (임계 경로) 이고 r_max 는 SE 반지름 r50 → β_net = (a_c / r50_SE)² 는 **솔브 없는 기하 서술자** 후보다.  ⚠ a 가 면적 모드에 달린다 (hertz c_cpl[22] vs physics — `LHS-25`) · 미구현 · 미검증 · 원문 사인식 (β 0.42–0.67 보정) 에 넣지 않는다 (LSC 고체 목 β 0.18 을 넣으면 δ_geo ≈ 0.045 가 나오지만 보정 범위 밖).
- ④ **σ₀ 기준 (결정 4 · CL-91)** — 원문의 δ · β 분해는 **구조 없는 σ₀** (벌크 액체) 를 전제한다.  SE 에 옮기면 σ₀ 가 결정립 내부값이어야 δ 가 '모든 목 협착' 을 뜻한다.  펠릿 σ₀ 위에서는 목 협착 일부가 σ₀ 안에 들어가고 FULL 의 Holm 이 다시 더한다 (메모 v2 §3-2 부분 이중계상) → **결정 4 (순수 SE 게이트) 를 지지 — 변경 없음**.
- ⑤ **τ_geo 는 알고리즘을 같이 낸다** (원문 p.2936 요구) — 우리 키 `tau_geo_SE_dij` 에 그래프 (SE 접촉 중심) · 분모 (Δz) · 표본 (≤ 200 쌍 · [1, 20) 절단) 을 메타로 (메모 v2 T01 한정어와 같은 방향).
- ⑥ **대표 부피 규칙** — 원문: 입상 매질 ID_crit ≈ 2–5 × 최대 입자 반지름, 크기 분포 (c-PSD) 는 그보다 큰 부피.  목 반지름은 4–5 voxel 로 해상 (p.2940) — 우리 STEP3 의 d_h/dx ≳ 3.5 규칙과 같은 크기 감각.

## 9. 인용 가능 문장 (deck/paper용)
- "Following Holzer et al. (J. Mater. Sci. 48, 2934, 2013), we keep the transport-derived tortuosity factor (their 'experimental' or 'electrical' tortuosity τ_exp = ε·σ₀/σ_eff, our tau2) strictly separate from the geometric tortuosity τ_geo obtained by shortest-path search, because the former also contains the bottleneck (constrictivity) effect."
- "In the constrictivity framework of Holzer et al. (2013), σ_eff/σ₀ = ε·δ/τ_geo with all exponents equal to one; the geometric constriction factor β = (r_min/r_max)² measured from tomograms is not equal to the transport constrictivity δ, and substituting β for δ underestimates the measured resistivity."
- "Geometric tortuosities of liquid-filled ceramic diaphragms stayed near 1.6 over porosities of 0.27–0.80, whereas impedance-derived tortuosities reached 5.6 (Holzer et al., 2013); the authors attribute the difference to bottleneck (constrictivity) effects and artefacts of the indirect determination, not to longer pathways."
- "Our contact-free network branch is the network analogue of the constant-radius reference state (δ = 1) of Holzer et al., but because it is not volume-consistent it can yield tau2 < 1; we therefore call it a model-internal baseline and the FULL/CF ratio a model-internal constriction ratio, distinct from both β and δ."

## 10. 주의/한계 (over-claim 방지)
- ⚠ **액체 전해질 · 소결 세라믹 기공** (KOH 격막) — LPSCl 고체 입자망으로 **수치 전이 불가**.  가져오는 것은 정의 · 분해 틀 · β ≠ δ 의 경험뿐이다.  LSC 고체상의 목 (β 0.18) 은 기하만 있고 수송 (δ) 은 재지 않았다.
- ⚠ **표본 8 점** (olivine 4 · wollastonite 4) — 사인식 (Eq. 9–10) 은 같은 8 점으로 맞춘 경험식이고 외부 검증이 없다 (원문: 'heuristic', 'validity has yet to be tested').  보정 범위 β 0.42–0.67 밖으로 쓰지 않는다.
- ⚠ 원문은 수송 시뮬레이션을 다루지 않는다 → **flux τ · 접촉망 · 저항망에 대한 원문 판정은 없다**.  §7–§8 의 대응은 원문 정의를 우리 망에 적용한 **우리 판단** 이다.
- ⚠ ε 의 정의 (총 / 연결) · σ_eff 의 단면 · 두께 정규화는 이 논문에 없다 (전작 [37]) [미확인].
- ⚠ 수치 다수가 **그림 벡터 추출값** (§3-B) — 축 눈금 글자 위치로 환산 · 표지 bbox 중심 = 데이터점 가정.  원문 내부 정합 (≤ 0.3 %) 으로 신뢰도는 높지만 **본문 명시값이 아니다**.
- ⚠ 원문 오식 · 불일치가 많다 (아래 원문 대조 기록) — 식을 인용할 때는 **그림 수치로 검산된 꼴** (Eq. 3 · Eq. 8 은 τ_geo σ_eff/(σ₀ε) · Eq. 9 는 [1 − cos(πγ)]/2) 을 쓰고 인쇄형과의 차이를 밝힌다.
- ⚠ Archie m 값 (2.95 · 2.31) 의 재료 배정은 의심스럽다 (§3-C ⑥) — 인용 금지 수준.
- ⚠ 우리 쪽 수치 (§7 · §8) 는 메모 v2 의 (유도) 값이고 이 카드에서 다시 계산하지 않았다.  중앙값끼리의 비 (T_CF/τ_Dij ≈ 0.98 · τ_Dij/T_H ≈ 0.24) 는 침대별 분포가 아니다.

### 메모 v2 정정 후보 (판단 메모 v2 `docs/reviews/tau_conventions_judgment_v2_20261003.md` 문장 ↔ 이 원문)
| # | 메모 v2 자리 · 문장 | 원문 (쪽) | 제안 |
|---|---|---|---|
| ① | §3-5 아래 *"Constriction overhead … 협착으로 읽을 수 없다 — 접촉 저항이 없는 연속 기공상도 1.24–1.59 를 낸다"* | δ = 1 은 일정 반경 원기둥뿐 (p.2937) · τ_elc–τ_geo 격차 = 병목 효과 (그림 12 캡션 · p.2949) | 결론 유지 · 근거 교체: "**접촉 (Holm) 협착 배수** 로 읽을 수 없다 — 연속 기공상의 목 협착 (Holzer δ) 과 계산 정의 차가 같은 비에 들어간다".  '협착 일반' 과 '접촉 저항' 을 구분 |
| ② | §3-5 표 행 (요지) √T_CF / τ_Dij **0.80** ↔ Tjaden "flux ≥ 기하" → "우리 CF 는 **반대 방향**" | 원문 틀은 τ_geo 를 **1 승** 으로 tau2 와 비교 (Eq. 2–3, p.2936–2937) · 실측 액체 기공 W4 √τ_elc/τ_geo ≈ 0.76 (그림 12 벡터 추출 · 우리 산술 · 한 점) | "√ 척도 (Tjaden/Cooper κ_geo 비교) 에서만" 한정어를 달고, CF 결함의 근거를 T_CF < 1 (Wiener · Holzer Eq. 2 의 τ ≥ 1) 로 명시 |
| ③ | §8-1 순위 2 *"τ_eff ↔ τ_geo 엄격 구분 + 협착 β"* (메인 지시의 "constrictivity β" 도 같은 결) | 원문 기호는 **τ_exp** (p.2936) · **τ_elc** (p.2934 · p.2949) — 'τ_eff' 는 Landesfeind 의 이름.  β = **constriction factor** (p.2934 · Eq. 6), constrictivity = **δ** (Eq. 3) | "τ_exp (τ_elc) ↔ τ_geo 엄격 구분 + constriction factor β (기하) · constrictivity δ (수송)" |
| ④ | §8-2 Wiedenmann 행 *"Landesfeind Eq 4 (N_M ≡ τ̄_geo/(εβ)) 원식 — τ_geo 지수 [미확인] 닫기"* | Holzer 2013 (같은 그룹 · 같은 격막 자료 [37]) 은 τ_geo **1 승** (Eq. 2 · 3 · 8 · 11; 그림 16 재현) · N_M = τ_geo/(ε·β) 는 원문 그림 16 의 **β 대입판** (과소 예측) 과 같은 꼴 | **부분 해소** 로 적는다 (보강 · 정정 아님).  Wiedenmann 원문 대조는 여전히 [미확인] |
| ⑤ | §3-5 표 Bruggeman 행 문헌 칸 | 격막 τ_elc·ε^½ = **1.8–3.1** (그림 11–12 벡터 추출 · 우리 산술) | 액체 기공 기준대로 한 줄 추가 (보강) |

### 원문 대조 기록 (이 카드 작성 중 직접 확인한 것)
1. **Eq. 5** (p.2937) 인쇄형 D_eff/D₀ = 0.2122·ln(β_Petersen) — β_P = 1 (무협착) 에서 0, 협착이 클수록 커진다 → 그대로는 뜻과 맞지 않는다.  원식은 [미확인: Petersen 1958 원문 미열람].
2. p.2938 *"For this case, the constriction factor directly relates to the relative diffusivity (see Eq. 5) and **β is identical with τ**"* — 문맥 (ε = τ = 1 인 단일 관) 상 δ 를 뜻한 것으로 보인다 [해석].
3. p.2945 *"it approaches a plateau with **β = 1.77** at thicknesses > 6 µm"* — Eq. 6 (β ≤ 1) · 그림 4 (0.177) · 그림 7a (> 6 µm 에서 ≈ 0.15–0.17, 눈 판독) 와 어긋남 → 0.177 의 오식으로 보인다 [해석].
4. **Eq. 8** (p.2949) 인쇄형 δ = σ₀τ_geo/(σ_eff ε) 은 Eq. 3 의 역수 — 그대로면 격막 8 점에서 δ = 6–127 (우리 산술, > 1).  그림 15 값은 δ = σ_eff τ_geo/(σ₀ ε) 를 따른다 (7/8 ± 0.012).
5. **Eq. 9** (p.2950) 인쇄형 '+π/2' — δ_geo(β = 0) = 1 · δ_geo(β = 1) = 0 이 되어 본문 경계조건 (p.2949–2950) · 그림 15 곡선과 반대.  그림 16 의 δ 예측 8 점은 [1 − cos(πγ)]/2 = [sin(πγ − π/2)]/2 + 1/2 로 ≤ 0.3 % 재현.
6. 그림 16 범례 "R_predicted = R₀*τ_geo/ε*x" — 'x 를 곱함' 으로 읽히나 수치는 ÷(ε·x) (Eq. 11).
7. 그림 11 '계산값' 8 점 = 정확히 1.20 × σ₀ε/τ_geo (σ₀ 0.645) — 같은 논문의 다른 그림들은 0.645 와 맞는다 [원인 미확인].
8. Archie m 배정 (p.2948) — 벡터 추출 점에 σ₀ 고정 맞춤하면 olivine 2.33 · wollastonite 2.98 (뒤바뀐 꼴) · 그려진 추세선은 자유 전인자 (≈ 0.60 ε^2.25 · 0.47 ε^2.52).
9. 그림 15 의 W4 (β 0.63) δ 0.79 ↔ 그림 12 τ_geo 1.86 으로 계산하면 0.92 — 그림 16 은 1.86 을 썼다 (β 판 재현).
10. 기호 γ 이중 사용 (Eq. 7 표면장력 · Eq. 10 이차식 — 약어표도 둘 다).  초록 τ_geo "1.6" ↔ 본문 1.62 (반올림).  그림 9a 축 'Cumulative LSD Volume' · 그림 14 축 'Porostiy' (오탈자).
11. 참고문헌 [37] 은 "(2012) AIChE J (in press)" 로만 적혀 있다.

---

## 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 원문 ref | 목록 서지 (그대로) | 왜 볼 만한가 |
|---|---|---|
| [37] | D Wiedenmann, L Keller, L Holzer, et al. (2012) AIChE J (in press) | 격막 원자료 (ε · σ_eff · τ_geo · ε_eff) 와 단면 · 두께 정규화 — 이 카드의 [미확인] 셋 (ε 정의 · m 배정 · 계산값 × 1.20) 을 닫는다.  Landesfeind Eq. 4 의 원식 (메모 v2 §8-2) |
| [29] | Van Brakel J, Heertjes PM (1974) Int J Heat Mass Transfer 17:1093 | Eq. 3 (εδ/τ) 의 원출처 — δ 정의 · τ 지수 관례 (Tjaden 식 4 의 τ 1 승 인쇄와 같은 계열) |
| [30] | Petersen EE (1958) AIChE J 4:343 | Eq. 4–5 의 원출처 — Eq. 5 인쇄형의 원식 확인 · 단일 관 협착 해석해 |
| [31] | Michaels AS (1959) AIChE J 5:270 | 단면 변화 vs 거품–목 간격의 상대 영향 — 접촉 반경 분포 vs 배위 간격 해석의 선례 |
| [20] | Münch B, Holzer L (2008) J Am Ceram Soc 91:4059 | c-PSD · MIP 모사 알고리즘 원문 — β 의 망 판 (§8 ③) 설계 참고 |
| [19] · [41] | Keller LM, Holzer L, Wepf R, Gasser P (2011) Appl Clay Sci 52:85 · Keller LM, Holzer L, Wepf R, Gasser P, Münch B, Marschall P (2011) Phys Chem Earth 36:1539 | τ_geo skeleton · 경로 정의 상세 — 우리 τ_geo 메타 비교 |
| [21] | Clennell MB (1997) In: Lovell MA, Harvey PK (eds) Developments in petrophysics. Geological Society Special Publication, London | τ 정의 총정리 ('guide through the maze') — τ vs τ² 관례 (Landesfeind 도 인용) |
| [22] | Bhatia SK (1985) J Catal 93:192 | Eq. 2 의 인용원 · "입상 매질에서 τ 20 은 비현실적" 의 근거 |
| [23] · [24] | Lindquist WB, Lee SM, Coker DA, Jones KW, Spanne P (1996) J Geophys Res 101:8297 · Hirsch LM, Schuette JF (1999) Comput Geosci 25:127 | 최단 경로 τ vs 고투과 경로 τ — 경로 선택 기준 차이 |
| [18] | Thiedmann R, Hartnig C, Manke I, Schmidt V, Lehnert W (2009) J Electrochem Soc 156:B1339 | 단층 영상 그래프 τ_geo 선례 |
| [25] · [26] | Boudreau BP (1996) Geochim Cosmochim Acta 60:3139 · Shen L, Chen Z (2007) Chem Eng Sci 62:3748 | τ_exp–ε 경험식 모음 (Shen & Chen 은 Tjaden 리뷰도 인용) |
| [3] | Archie GE (1942) Trans AIME 146:54 | Eq. 1 원전 |
| [44] | Diamond S (2000) Cem Concr Res 30:1517 | MIP 병목 효과의 고전 비판 — 돌파 반경 해석 |

- 이 논문 목록 밖: 같은 그룹의 후속 (M-factor 꼴 · 맞춤 지수) 이 있다면 **원문 확인 뒤** 에만 카드화한다 — 이 카드는 서지를 채우지 않는다 (규율 ⑥).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

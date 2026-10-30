# Rational Optimization of Cathode Composites for Sulfide-Based All-Solid-State Batteries — Tron et al. (*Nanomaterials* **2023**, 13, 327) · LPSCl 입도 (lp 수십 µm · sp 수 µm 이하 · lp 볼밀) · CAM 형태 · 도전재 · AM:SE 비 · 바인더 · 혼합 순서를 한 시험 규약으로 차례로 최적화

> slug `tron2023_rational_cathode_composite_optimization_lpscl` · DOI `10.3390/nano13020327` · type `exp (분말·캐스트 복합양극 파라미터 순차 최적화 · LPSCl 2 공급원 + 볼밀 · s/p-NMC811 · C65 vs VGCF · DC 분극 σ_e · AM:SE 5 비 · 첫 사이클 C/20 · 시뮬 없음)` · PDF `9134a378-8._Rational_optimization_of_cathode_composites_for_sulfide-based_all-solid-state_batteries.pdf` (본문 13 pp · **SI 미수령** — Fig. S1–S8 · Table S1 은 못 봤다) · digested `2026-10-30` · status ✅ · OA CC-BY

> topic: size_effect (SE 입도 효과)
> elements: Li, P, S, Cl, Ni, Co, Mn, Nb, O, C, In
> methods: EIS, DC polarization, galvanostatic cycling, tape casting, SEM, XRD
> ⚠ 다른 Tron 논문과 혼동 금지: 정본 `tron2023_lpscl_ccd_ambient_pressure` 는 같은 저자군의 **다른 논문** (LPSCl 임계전류밀도) 이다.

<!-- 실독 기록 (2026-10-30, litdb-curator)
     본문 13 쪽 전부 읽었다 (PyMuPDF 블록 추출 — 4 쪽 등에 'FOR PEER REVIEW' 겹친 글 층이 있어 pdftotext -layout 이 깨진다).
     SI 는 업로드되지 않았다 — SI 그림 · 표 내용은 본문이 말한 것만 옮기고 나머지는 [미확인].
     크롭 8 장 = 본문 그림 8 (패널 표지 (a)(b) 포함) — 전부 열어 확인했다.  본문에 표는 없다.
     표기 규약: 논문에 적힌 값 = stated · 그림에서만 읽은 값 = 판독 ≈ · 논문에 없는 계산 = 우리 산수.
     쪽 표기 = 논문 쪽 "n of 13" (PDF 쪽과 같다).  ★ 이 논문의 입도 결과 (Fig. 5) 는 숫자가 본문에 없다 → 전부 판독. -->

## 0. 이 digest 를 읽는 법 — 왜 지금 이 논문인가, 그리고 원문 판정

**계기 (2026-10-30)**: 50 kg 4차년도 DEM 보고 문헌 지도 `docs/50kg/report_y4/lit_se_size_map_20261030.md` §6 이 **8순위** 로 올렸다 —
*"입도만 다른 두 LPSCl 을 설계 변수와 함께 비교 (p5 · p7)"*.  원문 판정:

| Q | 판정 (한 줄) | 근거 |
|---|---|---|
| **Q1 입도** | **수치 없음.** lp-LPSCl (NEI · 상용) = *"large agglomerates of several tens of µm"* · sp-LPSCl (Solvay · 개발품) = *"smaller particles in the lower µm range"* / *"at most several µm"* · 셋째 = lp 를 p-xylene 습식 볼밀 (300 rpm · 2 × 1 h). SEM 은 SI (`Fig. S6`–`S8`, 못 봄) | p. 2 · p. 8 |
| **Q2 순수 SE σ** | **sp ≈ lp ≈ 2 × 10⁻³ S cm⁻¹** (펠릿 · 300 MPa · 0–300 MPa EIS) — 세 편 중 유일하게 **펠릿 σ 손해 없는 입도 비교**. 볼밀 lp 의 σ 는 **미보고** | p. 4–5 |
| **Q3 복합체 효과** | 67:30:3 wt% (= 40:55:5 vol%, **SE 55 vol%**) · s-NMC811 · C65 · C/20 첫 방전: **lp ≈136 · sp ≈160 · lp 볼밀 ≈157 mAh g⁻¹** (판독, 본문 수치 없음) → **≈1.18 배** | p. 8 · `Fig. 5` |
| **Q4 AM:SE 비 (우리 85 wt% 자리)** | sp · C65 2.5 wt% · AM:SE **70:30 → 90:10 wt%** (= 40:60 → 80:20 vol): 첫 방전 **≈160 / 149 / 135 / 102 / 13 mAh g_NMC⁻¹** (판독). **85:15 wt% (= 70:30 vol) 에서 −36 %, 90:10 에서 붕괴** | p. 8–9 · `Fig. 6` · `Fig. 8` |
| **Q5 조건** | 성형 **300 MPa** (우리 목표와 같다) · 측정 10 MPa · 1 mAh cm⁻² · C/20 · **첫 사이클만** · 셀 1 개씩 (반복 미기재) | p. 3–4 · `Fig. 1` |

⇒ **p5 판정**: 이 논문은 **"펠릿 σ 가 같은데 입도만 다른"** 비교라 구조 효과만 보기에 가장 깨끗하다 — 그러나 공급사 (NEI ↔ Solvay) 가 달라 합성 이력이 섞이고, 입도 수치가 없고, **SE 가 55 vol% 인 SE 풍부 조성에서 효과가 ≈1.18 배로 작다**.
**p7 판정**: 같은 계열 AM:SE 시험에서 **우리 설계점 85 wt% (= 70:30 vol) 가 성능이 꺾이기 시작하는 자리** 이고 90 wt% 에서 무너진다 — 우리 보고가 *"85 wt% 에서 이온 망이 어떻게 이어지나"* 를 묻는 이유의 실험 쪽 근거.
⚠ 입도 효과를 85 wt% 에서 시험하지는 않았다 (입도 시험은 67 wt% 하나).

---

## 1. 한 줄 요약

AIT (빈) 그룹이 황화물 (Li₆PS₅Cl) 복합양극의 설계 변수를 **같은 시험 규약** (1 mAh cm⁻² · C/20 · 첫 사이클 · 300 MPa 성형 · 10 MPa 측정 · In 대극) 으로 하나씩 고정해 가며 최적화한 실험 논문:
① 단결정 s-NMC811 > 다결정 p-NMC811 (161 vs 93 mAh g⁻¹, 액체 셀과 반대) ② C65 가 VGCF 보다 전자 전도 망을 훨씬 쉽게 만든다 (7 × 10⁻² vs ≤4 × 10⁻⁴ S cm⁻¹) ③ **작은 SE (sp · 볼밀 lp) 가 큰 SE (lp) 보다 낫다** (≈160 · ≈157 vs ≈136 mAh g⁻¹, 펠릿 σ 는 같음)
④ AM:SE **40:60–60:40 vol** 이 전극 무게 기준으로 대등하고 70:30 · 80:20 vol (= 85 · 90 wt%) 에서 급락 ⑤ SBS 바인더 2.5 wt% 가 용량을 깎는다 ⑥ SE+C65 를 먼저 섞는 순차 혼합이 약간 낫다.

## 2. 메타 / 동기 / 질문

| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Artur Tron\***, Raad Hamid, Ningxin Zhang, **Alexander Beutl\*** (AIT Austrian Institute of Technology, Vienna) | *Nanomaterials* **13**, 327 (2023) · 접수 2022-12-22 · 개정 2023-01-09 · 수락 01-11 · 게재 01-12 · CC BY | 10.3390/nano13020327 | **Li₆PS₅Cl** 둘 (lp = NEI 상용 · sp = Solvay 개발품) + lp 볼밀 · **LiNbO₃ 코팅 NMC811** 둘 (p = NEI 다결정 · s = Umicore 단결정) · C65 · VGCF · SBS · NBR · In 대극 | 실험 (분말 · 캐스트 복합양극 · 첫 사이클 · EIS · DC 분극) — **시뮬 없음** |

- **동기 (p. 1–2)**: 전해질 σ 가 아무리 높아도 복합양극 설계가 병목인데, 연구마다 변수 몇 개 · 시험 조건이 달라 비교가 안 되고 결과가 모순된다 (예: C65 가 분해를 부른다 [18] ↔ C65 가 최선 [13,20,25,26]).
- **질문**: 한 시험 규약으로 AM 형태 → SE 입도 → 도전재 → AM:SE 비 → 혼합 순서 → 바인더를 차례로 정하면 무엇이 남나.
- **자금 (p. 12)**: EU Horizon 2020 SUBLIME (No. 875028). 이해관계 *"no conflict"*. 시료 일부는 Solvay · Umicore 의 개발품.

## 3. 핵심 수치 총정리 ★

### 3a. 재료

| 항목 | 값 | 표기 · 출처 |
|---|---|---|
| lp-Li₆PS₅Cl | NEI Corp. 상용 · *"large agglomerates of several tens of µm"* · *"large particles up to several tens of µm and above"* | stated · p. 2 · p. 8 |
| sp-Li₆PS₅Cl | Solvay 개발품 · *"smaller particles in the lower µm range"* · *"particle sizes of at most several µm"* | stated · p. 2 · p. 8 |
| lp 볼밀 | 분말 3 g + p-xylene 10 mL · **300 rpm · 2 × 1 h** (1 h 뒤 30 min 휴지) — ref [14] 절차 · 입도 감소는 SEM · XRD (`Fig. S7`–`S8`) 로 확인했다고 적음 | stated · p. 8 |
| 두 SE 의 차이 | *"mainly differed in their particle sizes"* (저자 단언 · 순도 · 합성 정보 없음) | stated · p. 2 |
| p-NMC811 | NEI · **LiNbO₃ 코팅 다결정** · *"large particles of spherical shape"* (입도 수치 SI) | stated · p. 2 · p. 5 |
| s-NMC811 | Umicore 개발품 · **LiNbO₃ 코팅 단결정** · *"smaller particles with random shapes"* | stated · p. 2 · p. 5 |
| 도전재 | C65 (카본블랙) · VGCF | stated · p. 4 |
| 바인더 · 용매 | 전해질 필름 NBR (Perbunan 1846F) · PBMA · 양극 필름 SBS (M_w ≈169,000) · 용매 p-xylene · 디브로모메탄 (DBM) · 에틸아세테이트 (EtAc) — 분자체 1:20 건조 · 바인더 60 °C 진공 1 일 건조 | stated · p. 2 |

### 3b. 순수 SE 펠릿 · 전해질 필름 (`Fig. S2` 는 못 봄 — 본문 수치만)

| 항목 | 값 | 조건 | 표기 · 출처 |
|---|---|---|---|
| sp · lp 펠릿 σ | **둘 다 ≈2 × 10⁻³ S cm⁻¹** (*"similar"*) | ∅16 mm · ≈350 mg · **300 MPa** → ≈1000 µm · EIS 를 0 → 300 MPa 로 올리며 | stated · p. 4–5 |
| 볼밀 lp 펠릿 σ | **미보고** | — | — |
| 전해질 필름 σ | **≈1 × 10⁻³ S cm⁻¹** (분말의 절반) · 두께 ≈100 µm (300 MPa 압착 뒤) | NBR 바인더 · DBM:EtAc = 47:53 wt · 고형분 ≈50 wt% · THINKY 2000 rpm 3 min + 1000 rpm 2 min · 닥터블레이드 200 µm · PTFE 박 · 실온 24 h 건조 · ∅16 mm | stated · p. 2 · p. 5 |
| NBR 함량 | *"NBR (9 wt.%) was dissolved"* — 용액 농도로 읽히고 필름 중 바인더 분율은 [미확인] | | stated · p. 2 |
| 분리막 | 필름 3 장 (≈300 µm) — `Fig. 1` 은 *"Li₆PS₅Cl (NEI Corp., ~100 mg, ~300 µm)"* | | stated |

### 3c. 셀 · 시험 규약 (p. 3–4 · `Fig. 1`)

| 항목 | 값 | 표기 |
|---|---|---|
| 대극 | In 박 (0.127 mm · 99.99 %) ∅9 mm 를 강철 스페이서 (∅16 mm · 500 µm) 에 **300 MPa** 압착 → 두께 ≈40–50 µm · 지름 14–15 mm · In 용량 > 10 mAh | stated |
| 조립 | In 위 전해질 필름 3 장 → **300 MPa · 5 min** → 분말 또는 캐스트 양극 → 다시 **300 MPa · 5 min** · 측정 중 **10 MPa** (압력 셀, ref [24]) | stated |
| 로딩 | **1 mAh cm⁻²** (≈9–10 mg cm⁻²) | stated |
| 전류 · 전압 | **0.05 mA cm⁻² (C/20)** · 3.7–2.4 V vs In/LiIn (= 4.3–3.0 V vs Li) · Gamry Interface 1010E · 실온 | stated |
| 전류 선택 근거 | 전해질층의 임계전류밀도 (`Fig. S1`, 300 µm 막 · Li‖Li · 10 MPa · *"1C = 1 mA cm⁻²"*) 에 맞춤 + In 위 Li 석출 회피 | stated · p. 4 · p. 11 |
| 비교 대상 | **첫 충방전 한 사이클만** (*"maximum achievable specific energy"* + 첫 쿨롱효율) | stated · p. 4 |
| EIS | 1 MHz–1 Hz · 10 mV · PEIS | stated · p. 3 |
| σ_e | **DC 분극** 10–50 mV (10 mV 스텝) · 선형 적합 기울기 (ref [27]) · *"10 and 300 MPa"* 사이 압력 (그림은 10 · 50 · 100 MPa) | stated · p. 3 · `Fig. 4` |
| 양극 혼합 | AM · SE · CA 를 마노 유발로 손 혼합 (*"until a homogeneous mixture"*) · 기본 SE = sp | stated · p. 3 |
| 캐스트 양극 | 예비 혼합 분말 + 바인더 용액 → THINKY → Al 박 테이프 캐스팅 (≈1 mAh cm⁻²) → 실온 24 h → ∅15 mm | stated · p. 3 |
| 액체 대조 | AM : CA : PVdF = 90:05:05 · NMP · 120 °C 16 h 진공 · 2016 코인 · 1 M LiPF₆ EC:DEC 1:1 · Celgard 2400 · Li 15.6 mm · 3.0–4.3 V | stated · p. 3 |

### 3d. 결과 수치 — 단계별

| 단계 · 비교 | 값 | 표기 · 출처 |
|---|---|---|
| **AM 형태** (67:3:30 wt% AM:CA:SE) — 첫 방전 | **s-NMC811 161 · p-NMC811 93 mAh g⁻¹** | stated · p. 5 · `Fig. 2a` |
| 첫 충전 | s ≈227 · p ≈180 | 판독 ≈ · `Fig. 2a` |
| EIS (충전 전) | 벌크 ≈50 Ω (둘 다) · 양극 쪽 추가 저항 **s ≈10 Ω · p ≈60 Ω** | stated · p. 5 · `Fig. 2b` |
| 첫 쿨롱효율 (s-NMC811) | **71 %** | stated · p. 5 |
| 액체 셀 | p-NMC811 > s-NMC811 (`Fig. S4`, 못 봄) — 고체 셀과 반대 | stated · p. 5 |
| **도전재** (AM:SE:CA = 67:30:3 wt% = 40:55:5 vol%) — 첫 방전 | **C65 161 · VGCF 140 mAh g⁻¹** | stated · p. 6 · `Fig. 3a` |
| 첫 충전 | C65 ≈227 · VGCF ≈200 | 판독 ≈ |
| EIS (첫 방전 뒤) | 벌크 비슷 (≈42 Ω 절편, 판독) · VGCF 계면 저항이 더 큼 | stated / 판독 · p. 6 · `Fig. 3b` |
| **σ_e — VGCF** | ≈10 vol% 까지도 **≈4 × 10⁻⁴ S cm⁻¹** · 압력 의존 큼 | stated · p. 7 |
| VGCF 판독 (100 MPa) | 0 vol% ≈0.8 × 10⁻⁴ · 2.3 % ≈0.85 × 10⁻⁴ · 4.6 % ≈1.3 × 10⁻⁴ · 6.7 % ≈1.7 × 10⁻⁴ · 8.8 % ≈2.3 × 10⁻⁴ · 10.8 % ≈3.6 × 10⁻⁴ S cm⁻¹ · (50 MPa 10.8 % ≈1.6 × 10⁻⁴ · 10 MPa ≈0.3 × 10⁻⁴) | 판독 ≈ · `Fig. 4a` |
| **σ_e — C65** | **≈7 × 10⁻² S cm⁻¹** · 압력 의존 작음 · 2–3 wt% 로 *"almost three orders of magnitude"* ↑ | stated · p. 7 · p. 11 |
| C65 판독 | 2.3 vol% ≈0.2–0.45 × 10⁻² · 4.5 % ≈1.2–1.9 × 10⁻² · 6.6 % ≈4.5–5.7 × 10⁻² · 8.6 % ≈6.1–7.1 × 10⁻² · 10.5 % ≈6.9–7.3 × 10⁻² S cm⁻¹ · 시그모이드 변곡 ≈5.5–6 vol% | 판독 ≈ · `Fig. 4b` |
| 이후 고정 | C65 **2–3 wt% (4–5 vol%)** | stated · p. 8 |
| **SE 입도** (s-NMC811 · AM:SE:CA = 67:30:3 wt% = 40:55:5 vol%) — 첫 방전 | **lp ≈136 · sp ≈160 · lp 볼밀 ≈157 mAh g⁻¹** | 판독 ≈ · `Fig. 5` — 본문은 *"lower specific capacities"* (lp) · *"significant improvement"* 뿐 |
| 첫 충전 | lp ≈195 · sp ≈226 · lp 볼밀 ≈219 | 판독 ≈ · `Fig. 5` |
| 첫 쿨롱효율 | lp ≈70 · sp ≈71 · lp 볼밀 ≈72 % | 판독 + 우리 산수 |
| 방전 곡선 모양 | 세 곡선이 3.0 V 근방까지 거의 겹치다가 lp 가 ≈125 mAh g⁻¹ 부터 먼저 꺾인다 · 충전은 lp 가 위 (분극 큼) | 판독 · `Fig. 5` |

### 3e. AM:SE 비 계열 (sp · s-NMC811 · C65 2.5 wt% (4.5 vol%) · `Fig. 6` · `Fig. 8` 판독)

| AM:SE (wt) | (vol, 논문 표기) | 충전 / 방전 (mAh g_NMC⁻¹) | 충전 / 방전 (mAh g_electrode⁻¹) |
|---|---|---|---|
| 70:30 | 40:60 | ≈227 / **≈160** | ≈151 / ≈106 |
| 75:25 | 50:50 | ≈212 / **≈149** | ≈155 / ≈108 |
| 80:20 | 60:40 | ≈197 / **≈135** | ≈157 / ≈106 |
| **85:15** | **70:30** | ≈163 / **≈102** | ≈139 / ≈87 |
| 90:10 | 80:20 | ≈41 / **≈13** | ≈37 / ≈12 |
| 순차 혼합 AM+(CA+SE) | 0.55 | ≈221 / ≈154 | ≈168 / ≈116 |
| 순차 혼합 | 0.63 | ≈203 / ≈139 | ≈164 / ≈112 |

- 본문 (p. 8–9, stated): *"specific charge values given with respect to the active material decrease with increasing AM:SE ratios … The lower ionic conductivity is quite evident from the increasing overpotential"* · 전극 무게 기준으로는 **40:60–60:40 vol 이 대등** · **70:30 · 80:20 vol 에서 "drastic decrease"**.
- 저자의 기계적 해석 (p. 9, stated): *"For low AM:SE ratios … enough electrolyte particles are surrounding each active material particle to buffer mechanical stress … When less electrolyte is added, the NMC811 particles come in contact with each other, and densification is inhibited"* (ref [13]).
- 결론 (p. 11, stated): *"An AM:SE ratio between 40:60 and 60:40 is considered feasible"* · Bielefeld 2019 [21] 의 이론 최적 70:30 과 *"close"* (정의 · 단위 확인은 `bielefeld2019_microstructural_modeling_composite_cathode` 카드에서).

### 3f. 바인더 · 혼합 (p. 9–10)

| 항목 | 값 | 표기 · 출처 |
|---|---|---|
| 바인더 시험 | AM:SE (vol) **0.55** · C65 2.5 wt% + SBS 2.5 wt% (≈8 vol%) · 캐스트 | stated · p. 9 |
| 기대값 (무바인더 0.5 · 0.6 보간) | 충전 212–197 · 방전 149–135 mAh g⁻¹ | stated · p. 9 · `Fig. 7` |
| 실측 (SBS) | 충전 **166** · 방전 **115 mAh g⁻¹** | stated · p. 9 · `Fig. 7` |
| 저자 권고 | 바인더 ≤ 1 wt% (ref [35]) · 가공성과 균형 | stated |
| 순차 혼합 (SE+C65 먼저 → AM) | *"slight increase"* (`Fig. 8`, §3e 표) | stated / 판독 · p. 10 |

### 3g. 우리 산수 (논문 미보고)
- **입도 효과의 크기**: sp/lp ≈ 160/136 = **1.18** · 볼밀 lp/lp ≈ 157/136 = **1.15** (판독 기반).
- **AM 분율 꺾임**: 85:15 wt / 70:30 wt 첫 방전 비 ≈ 102/160 = **0.64** · 90:10 wt ≈ 13/160 = **0.08**.
- **판독 자기일관 검사**: 전극 기준 = AM 기준 × 전극 중 AM 질량분율 (C65 2.5 wt% 가정) — 70:30 wt → 160 × 0.6825 ≈ 109 (그림 ≈106) · 85:15 wt → 102 × 0.829 ≈ 85 (그림 ≈87) · 90:10 → 13 × 0.8775 ≈ 11 (그림 ≈12) ⇒ 두 패널 판독이 서로 맞는다.
- **wt ↔ vol 표기의 밀도 함의**: 논문이 적은 대응이 함의하는 ρ_AM/ρ_SE = 70:30 → 40:60 이면 **3.5** · 75:25 → 50:50 이면 3.0 · 80:20 → 60:40 이면 2.67 · 85:15 → 70:30 이면 2.43 · 90:10 → 80:20 이면 **2.25** (67:30 → 40:55 이면 3.07). 하나의 밀도 쌍이면 이 값이 일정해야 한다 ⇒ **vol 표기는 반올림 근사** — 계열 내 vol 간격을 정량으로 쓰지 말 것.
- **σ_e 대비**: C65 ≈7 × 10⁻² 는 VGCF (≤ ≈4 × 10⁻⁴) 의 ≈175 배 (stated 값 비).

---

## 4. 재료 & 방법 — 같은 축을 흉내 낼 때 필요한 조건 ★
§3a–§3c 표가 전부다. 핵심만:
- **SE 입도 비교** = 같은 조성 67:30:3 wt% (40:55:5 vol%) · s-NMC811 · C65 3 wt% · 손 혼합 · 300 MPa · 10 MPa 측정 · C/20 · 첫 사이클.
- **AM:SE 계열** = sp · s-NMC811 · C65 2.5 wt% · 같은 규약.
- **σ_e** = DC 분극 (10–50 mV) · 조성은 s-NMC811 + sp + 도전재 (AM:SE 비 미기재) · 압력 10 · 50 · 100 MPa (그림).
- **빠진 것**: SE · CAM 입도 수치 (SI 에 SEM 만) · 볼밀 lp 의 σ · 복합체 기공 · 복합체 이온 σ · 반복 셀 수 · 율특성 · 사이클 수명.

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 SE 분말과 필름 (§3.1)
두 LPSCl 펠릿이 같은 σ (≈2 mS cm⁻¹) — 펠릿 σ 가 입도에 둔감한 경우. 필름은 바인더 탓에 절반 (≈1 mS cm⁻¹).

### 5.2 AM 형태와 도전재 (§3.2 · `Fig. 2`–`4`)
단결정 s-NMC811 이 *"초기 접촉 면적이 커서"* 양극 계면 저항 (≈10 vs ≈60 Ω) 과 과전압이 작고 용량이 크다 (161 vs 93). 액체 셀에서는 반대 (균열 틈으로 전해액이 스며 접촉이 느는 효과가 고체에서는 없다).
도전재: C65 는 4–6 vol% 에서 시그모이드로 퍼콜레이션해 ≈7 × 10⁻² S cm⁻¹ 까지 가고, VGCF 는 10 vol% 에서도 ≈4 × 10⁻⁴ 로 낮고 압력에 민감하다 — *"VGCF 응집도 무시할 수 없다"*. 첫 사이클 쿨롱효율은 둘 다 비슷 (C65 가 분해를 부른다는 [18] 과 다름).

### 5.3 SE 입도 (§3.3 · `Fig. 5`)
lp (수십 µm 응집체) 는 *"poor contact between active material and electrolyte particles"* 로 용량이 낮고, sp · 볼밀 lp 는 *"significant improvement"* — 같은 경향이 ref [16] (Minnmann 2021) 에도 있다고 적는다. 본문에 숫자는 없다 (판독 ≈136 / ≈160 / ≈157).

### 5.4 AM:SE 비 (§3.3 · `Fig. 6`)
AM 기준 용량은 SE 를 줄일수록 단조 감소 (과전압 증가 = 이온 전도 부족). 전극 기준으로는 40:60–60:40 vol 이 평탄하고 70:30 부터 꺾인다. 기계적으로는 SE 가 적으면 NMC811 끼리 닿아 **치밀화가 막힌다** (저자 해석 · 측정 없음).

### 5.5 바인더 · 혼합 순서 (§3.4–3.5 · `Fig. 7`–`8`)
SBS 2.5 wt% 가 AM–SE 계면을 가려 방전 115 (기대 135–149) — 바인더는 최소로. SE+C65 를 먼저 섞으면 약간 오른다 (0.55 · 0.63 vol 에서 ≈154 · ≈139 mAh g_NMC⁻¹).

### 5.6 결론 (p. 11, stated)
AM 은 작은 입자 (단결정) · C65 2–3 wt% · AM:SE 40:60–60:40 vol · 바인더 최소 · 혼합 순서 중요. *"reporting not only the specific capacity with respect to the active material, but rather with respect to the overall composite electrode"* 를 강조.

## 6. 우선 질문 — 50 kg 4차년도 보고 쪽 (p1–p7) 기준 원문 대조

| 쪽 | 묻는 것 | 이 논문이 주는 것 | 못 주는 것 |
|---|---|---|---|
| p1 비교 틀 | 입도 · λ | 정성 입도 (수십 µm vs 수 µm) | **수치 PSD · CAM 입도 없음** → λ 불가 |
| p2 공간 점유 · 압밀 | 기공 · 치밀화 | *"AM 이 많으면 AM 끼리 닿아 치밀화가 막힌다"* (주장) | 기공 · 밀도 측정 없음 |
| p3 접촉 · 피복 | 계면 | s-NMC811 의 *"초기 접촉 면적"* 논리 · 양극 계면 저항 10 vs 60 Ω | 피복 · 접촉 수치 |
| p4 연결성 · 병목 | 이온 망 | AM 분율 ↑ → 과전압 ↑ (이온 전도 부족 해석) | σ_ion,eff · tortuosity |
| p5 구조 ↔ 물성 분리 | 펠릿 σ 손해 없는 입도 효과 | **sp ≈ lp 펠릿 σ (2 mS cm⁻¹) · 복합체 첫 방전 ≈1.18 배** — 펠릿 σ 비 = 1 인 문헌 점 | 볼밀 lp 의 σ · σ_eff · 입도 수치 |
| p6 두께 방향 | — | 없음 | — |
| p7 경향 · 다음 검증 | 방향 · 우리 85 wt% 맥락 | 작은 SE → 첫 방전 ↑ (67 wt%) · **85:15 wt (70:30 vol) −36 % · 90:10 붕괴** | 85 wt% 에서의 입도 효과 · 율 · 수명 |

## 7. 우리 DEM+MPM 대비 ★ (근거 = 작업 브랜치 CLAUDE.md · `docs/50kg/report_y4/storyline_draft1.md` · `lit_se_size_map_20261030.md`)

### 7a. 항목별 대조

| 항목 | 이 논문 | 우리 (50 kg 4차년도 DEM) | 차이 / 이유 |
|---|---|---|---|
| SE | LPSCl 두 공급원 (수십 µm 응집체 vs 수 µm 이하) + 볼밀 | LPSCl 단분산 구 0.7 · 1 · 2 · 3 µm | 재료는 같다 · 크기는 정성뿐 → sp 는 대략 우리 D1–D3 대역으로 읽힐 수 있지만 **확인 불가** |
| CAM | LiNbO₃ s-NMC811 (단결정 · 입도 SI) | NCM D6 µm 단일 | λ 불가 |
| 입도 시험 조성 | 67:30:3 wt% = **SE 55 vol%** (SE 풍부) | **85 wt% AM** | 입도 효과가 작게 나오기 쉬운 조성 (Shi 2019 λ 지도: 고 AM 분율일수록 λ 가 결정적 — `shi2019_high_am_loading_particle_size_assb` §A.2, 문헌 지도 표기 *"잠정"*) |
| AM:SE 계열 | 70–90 wt% (C65 2.5 wt%) | 85 wt% (탄소 없음) | **85:15 wt% 가 같은 자리** — 이 논문에서 꺾이기 시작하는 점 |
| 압력 | 성형 **300 MPa** · 측정 10 MPa | 300 MPa 목표 · 가압 상태 | 성형압이 같다 (세 편 중 유일). 단 우리는 언로딩 없는 가압 상태 |
| 순수 SE σ | sp = lp ≈ 2 mS cm⁻¹ | σ₀ 입력 · p5 손익분기선은 1저자 펠릿 실측 (1 µm 2.3 · 3 µm 5.1 mS cm⁻¹ → 2.217) | 이 논문 = 펠릿 σ 비 1 의 끝점 — 손익분기선이 1 이면 **구조 이득만으로 이긴다** 는 쪽의 문헌 사례 |
| 이온 수송 | 측정 없음 (과전압으로 추정) | f · tau2 · 연결성 · 협착 몫 | 우리가 채울 칸 |
| 기계 | *"AM 끼리 닿아 치밀화 저해"* (주장) | DEM 의 AM 골격 하중 차폐 (CLAUDE.md E_SE 보정 절: 강성 AM 골격이 300 MPa 를 지고 SE 는 덜 눌린다) · `calc_love_weber_stress` | **같은 기전을 DEM 이 정량할 수 있다** (p2 · p6) |
| 전자 | C65 ≈7 × 10⁻² · VGCF ≤4 × 10⁻⁴ S cm⁻¹ (DC 분극) | 4차년도 DEM 은 탄소 없음 · 전자 채널 = AM–AM 만 | 입도 주제 밖 — 곁가지 (§7c) |

### 7b. 50 kg 4차년도 보고 쪽 대응 (문헌 지도에 넣을 문장 후보)
- **p5**: 펠릿 σ 비 목록의 **아래 끝 (비 ≈1)** — *"공급원이 다른 두 LPSCl 은 펠릿 σ 가 같았고 (≈2 mS cm⁻¹), 작은 쪽 복합양극 (SE 55 vol%) 의 첫 방전이 ≈1.18 배였다 (Tron 2023, 판독)"*. 덱의 손익분기선 그림에 *"문헌의 펠릿 σ 비 범위 = 1 (Tron) · 1.9 (Calpa, 경로) · 1.25–3.28 (밀링 계열)"* 처럼 범위로 쓸 근거 중 하나.
- **p7 (★ 우리 설계점)**: *"같은 계열에서 85 wt% (70:30 vol) 가 꺾이기 시작하고 90 wt% 에서 무너진다 (C/20 · 300 MPa 성형 · 10 MPa 측정)"* — 85 wt% 에서 이온 망 연결 (p4) 을 묻는 이유의 실험 쪽 근거. ⚠ 같은 85 · 90 wt% 가 `lin2025_submicron_lpscl_cathode_li_kinetics` 의 ESI (`Fig. S11`–`S12`) 에서는 0.1C 첫 방전 ≈183 · ≈168 mAh g⁻¹ (판독) 로 무너지지 않는다 — 성형압 (640 vs 300 MPa) · 구속압 (50 vs 10 MPa) · SE · 도전재 · CAM 이 다 달라 **원인을 하나로 못 집는다**. 덱에서는 *"고 AM 분율의 성패는 공정 · 입도 조건에 걸린다"* 까지.
- **p2 · p6**: 저자의 *"AM 끼리 닿으면 치밀화가 막힌다"* 는 우리 DEM 이 **AM–AM 접촉 수 · 하중 분담 · 입자 응력 (Love–Weber)** 으로 직접 볼 수 있는 주장 — 보고에서 *"문헌 주장 ↔ 우리 계산"* 짝으로 쓸 수 있다 (가압 상태 · 시드 1 한정어 유지).
- **p1**: *"lower µm range"* · *"several tens of µm"* 같은 정성 입도는 우리 축에 점으로 못 올린다 — 지도 T1 칸에 *"수치 없음"* 표지.

### 7c. 문헌 지도 속 위치 + 곁가지
- 지도 §1 표에 넣을 행 (안): `tron2023_rational_cathode_composite_optimization_lpscl` | LPSCl lp (NEI, 수십 µm 응집체) · sp (Solvay, ≤ 수 µm) · lp 볼밀 — 수치 없음 | LiNbO₃ s-NMC811 · 67:30:3 wt% (40:55:5 vol%) · C65 | 펠릿 σ sp ≈ lp ≈ 2 mS/cm · 첫 방전 ≈136 / ≈160 / ≈157 mAh/g (판독) · AM:SE 70–90 wt% → 85 wt% −36 % · 90 wt% 붕괴 · 300 MPa 성형 | f(d) · 연결성 · AM:SE 축 | 용량 · σ_e (도전재) · 바인더.
- §2 빈도: T1 (SEM 은 SI · 수치 ✗) · T2 (✓ 평탄) · T3 (✗) · T4 (✗) · T5 (✗) · T6–T7 (✗) · T8 (✓ 도전재 축 — 입도 축 아님) · T9 (✗) · T10 (✓ 첫 사이클) · T11 (✗) · T12 (✗) · T14 (볼밀 XRD 는 SI).
- **곁가지 (σ_e, CL-46 맥락)**: VGCF 를 10 vol% 넣어도 ≈4 × 10⁻⁴ S cm⁻¹ (손 혼합 · 100 MPa) — 정본 카드들의 탄소 포함 황화물 복합양극 값 (예: `schlautmann2023_se_particle_size_composite_transport` §7c 표의 Lee 2025 34 · Kim 2024 38.6–65.2 mS cm⁻¹) 보다 **두 자릿수 아래** 이고, 무탄소 Schlautmann 0.26–0.41 mS cm⁻¹ 과 비슷한 자릿수다. ⇒ *"탄소가 있으면 σ_e 가 높다"* 가 아니라 *"탄소망이 이어져야 높다"* 는 기존 판독 (Lee 2025 PTFE 5 wt% → 0.011) 과 같은 방향의 사례 — 혼합법 · 응집이 지배.

### 7d. frame [4]/[5] 판정
- **frame [5]**: 이 논문은 **실험 (첫 사이클 용량 · EIS · σ_e)** 만 있고 미세구조는 말로만 있다 — 기공도 영상도 없다. 우리 DEM 이 줄 것 = 같은 300 MPa 에서 **85 wt% 의 AM 골격 · SE 망 연결 · f** — 이 논문의 *"치밀화 저해"* · *"이온 전도 부족"* 두 해석을 각각 기계 (p2 · p6) 와 수송 (p4) 지표로 나눠 볼 수 있다.
- **frame [4]**: 값 이식 금지 — 첫 사이클 · C/20 · 셀 1 개 · 판독값. 쓸 수 있는 것은 **방향** (작은 SE → 이득 · 85 → 90 wt% 꺾임) 과 **펠릿 σ 비 = 1 의 끝점**.
- 이전 가능성 경계: LPSCl ↔ LPSCl · 300 MPa ↔ 300 MPa 로 재료 · 성형압은 가장 가깝다. 그러나 입도 시험이 SE 55 vol% 라 우리 85 wt% 로 효과 크기를 옮길 수 없다.

---

## 8. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 시험 셀 모식 (양극 / Li₆PS₅Cl NEI ≈100 mg · ≈300 µm / In ≈40 µm) + 시험 조건 (1 mAh cm⁻² · C/20 · 첫 사이클 · 300 MPa 조립 · 10 MPa 측정 · RT) + 최적화 순서 | 비교 규약 (우리 300 MPa 와 같은 성형압) |
| 2 | (a) s- vs p-NMC811 첫 충방전 · (b) 충전 전 EIS (삽도 전체 범위) | 단결정 CAM 의 계면 저항 이점 (CAM 입도 축 — 우리 NCM D6 단일과 다름) |
| 3 | (a) C65 vs VGCF 첫 충방전 · (b) 첫 방전 뒤 EIS | 도전재 효과 (입도 주제 밖) |
| 4 | 비전자전도도 vs 도전재 vol% — (a) VGCF (10 · 50 · 100 MPa) · (b) C65 · 점선 = 시그모이드 적합 | 탄소 퍼콜레이션 (곁가지 §7c) |
| 5 | **lp · sp · lp 볼밀** 첫 충방전 (67:30:3 wt% · 40:55:5 vol%) | ★ 입도 효과 원자료 (판독 ≈136 / ≈160 / ≈157) — p5 · p7 |
| 6 | AM:SE (vol) 40:60–80:20 첫 충방전 — (a) mAh g_NMC⁻¹ · (b) mAh g_electrode⁻¹ | ★ **85 wt% 꺾임 · 90 wt% 붕괴** (p7 · 우리 설계점) |
| 7 | 캐스트 (SBS, AM:SE 0.55) vs 분말 0.5 · 0.6 첫 충방전 | 바인더 벌점 |
| 8 | 비용량 vs AM:SE (vol) — 일반 혼합 vs 순차 혼합 · (a) AM 기준 · (b) 전극 기준 | AM 분율 축의 요약 그림 — 우리 f(AM 분율) 그림의 문헌 짝 후보 |
| S1–S8 · Table S1 | CCD · σ–압력 · CAM/SE SEM · 액체 셀 · EIS · 볼밀 XRD · 배합 목록 | **SI 미수령 — 내용 [미확인]** (본문이 말한 것만 §3 에 옮김) |

## 9. Post-processing ★
- **용량**: 첫 사이클 충 · 방전 → mAh g_NMC⁻¹ 와 mAh g_electrode⁻¹ 두 정규화 (`Fig. 6` · `Fig. 8`) — 저자 권고 *"전극 기준도 같이 보고하라"*.
- **σ_e**: DC 분극 10–50 mV 스텝 → 정상 전류 → V–I 선형 기울기 → σ (ref [27]) · 도전재 vol% 에 대해 시그모이드 적합 → 퍼콜레이션 문턱 (`Fig. 4`).
- **EIS**: 충전 전 / 첫 방전 뒤 Nyquist 에서 벌크 절편 · 양극 쪽 반원 크기를 읽어 비교 (등가회로 적합 서술 없음).
- **펠릿 σ**: 0 → 300 MPa 가압 중 EIS (`Fig. S2`, 미수령).
- **기록**: 셀 1 개씩 · 오차 막대 없음 · 첫 사이클만.

## 10. 비판 / 주의 / 한계 ★ (over-claim 방지)

1. **입도가 수치로 없다** — *"several tens of µm"* · *"lower µm range"* · *"at most several µm"* 뿐 (SEM 은 SI, 이 카드에서 못 봤다). 우리 D 축에 점으로 못 올린다.
2. **입도와 공급원이 함께 바뀐다** — NEI 상용 vs Solvay 개발품. *"mainly differed in their particle sizes"* 는 저자 단언 (순도 · 할라이드 · 결정성 비교 없음). 볼밀 lp 는 같은 공급원이라 더 깨끗한 대조지만 **그 σ 가 없다**.
3. **입도 시험 조성이 SE 풍부** (SE 55 vol%) — 큰 SE 도 퍼콜레이션하기 쉬운 조성이라 효과 (≈1.18 배) 가 작다. 우리 85 wt% 로 크기 이식 금지.
4. **첫 사이클 · C/20 · 셀 1 개** — 율 · 수명 · 재현성 없음. 입도 결과는 **본문에 숫자가 없어 전부 판독**.
5. **wt ↔ vol 표기가 하나의 밀도 쌍으로 안 맞는다** (함의 ρ_AM/ρ_SE 3.5 → 2.25, §3g) — vol 값은 근사.
6. **σ_e 압력 범위 서술 불일치**: 방법은 *"10 and 300 MPa"*, 그림은 10 · 50 · 100 MPa. VGCF 점선은 *"sigmoidal fit"* 이라는데 범위 안에서 포화가 없어 문턱이 정해지지 않는다. σ_e 시료의 AM:SE 비 미기재.
7. **기계적 해석 (AM 끼리 닿아 치밀화 저해) 은 측정 없는 주장** — 기공 · 밀도 · 단면이 없다.
8. **SE 필름 NBR 9 wt%** 가 용액 농도인지 필름 분율인지 모호.
9. **"lower µm range" 의 sp 와 볼밀 lp 의 성능이 거의 같다** (≈160 vs ≈157) — 입도가 비슷해졌는지 SI 없이 확인 불가.
10. **혼동 주의**: 같은 1저자의 다른 논문 `tron2023_lpscl_ccd_ambient_pressure` 와 섞지 말 것 (CCD 시험은 이 논문에서 `Fig. S1` 한 장으로만 등장).

## 11. 적용 인사이트
- ① **p5 의 문헌 범위 아래 끝 = 1**: 펠릿 σ 가 입도에 무관한 LPSCl 쌍이 실재한다 (Tron · Schlautmann 4–40 µm 평탄과 같은 편) — 손익분기선 2.217 은 *"밀링 SE 일 때"* 의 시나리오이고, 손해가 없으면 구조 이득 그대로가 이득이다.
- ② **85 wt% 는 실험 문헌에서 '꺾이는 자리'**: 같은 규약 계열에서 85 wt% 가 −36 %, 90 wt% 가 붕괴 — 우리 보고의 p4 · p7 이 *"85 wt% 에서 SE 망이 얼마나 이어지나 · 입도로 얼마나 버티나"* 를 묻는 이유. 덱 문장은 *"문헌 (Tron 2023, C/20 · 300 MPa) 에서 85 wt% 는 성능이 꺾이기 시작하는 조성"* 까지.
- ③ **입도 효과는 조성에 걸린다**: SE 55 vol% 에서 ≈1.18 배 (이 논문) vs AM 79 wt% 에서 ≈3.35 배 (`calpa2019_small_li7p3s11_liquid_phase_composite_cathode`) — 재료 · 입도 차가 섞여 단정은 못 하지만 Shi 2019 의 *"고 AM 분율에서 λ 가 결정적"* (문헌 지도 표기 *"잠정"*) 과 같은 방향. 우리 85 wt% 는 효과가 큰 쪽이라는 예측을 p7 에 *"검증할 것"* 으로 둘 근거 (예측이지 결론이 아니다).
- ④ **AM–AM 접촉 = DEM 이 바로 볼 수 있는 주장**: 저자의 치밀화 저해 해석을 우리 AM–AM 접촉 수 · 하중 분담 · Love–Weber 응력으로 시험할 수 있다 (p2 · p6).

## 12. 인용 가능 문장 (영문 초안)
- *"Two Li₆PS₅Cl powders of different particle size (tens of µm agglomerates vs particles of at most a few µm) showed the same pellet conductivity (≈2 mS cm⁻¹), while the finer one gave a higher first discharge capacity in NMC811 composites at 67:30:3 wt% (≈160 vs ≈136 mAh g⁻¹, read from Fig. 5) [Tron 2023]."*
- *"Under one harmonized protocol (300 MPa assembly, 10 MPa operation, C/20), the first discharge capacity decreased from ≈160 to ≈102 mAh g⁻¹ when the AM:SE ratio increased from 70:30 to 85:15 wt% and collapsed (≈13 mAh g⁻¹) at 90:10 wt% [Tron 2023, Fig. 6, read]."*
- ⚠ 입도를 숫자로 적지 말 것 (원문에 없다).

## 13. 기법 용어 미니사전
- **lp / sp**: 저자 표기 — large-particle / small-particle Li₆PS₅Cl.
- **s-NMC811 / p-NMC811**: 단결정 (single-crystalline) / 다결정 (polycrystalline) NMC811 — 둘 다 LiNbO₃ 코팅.
- **C65**: 카본블랙 (Super C65 계열 · 비표면적이 큰 미세 탄소) · **VGCF**: 기상성장 탄소섬유.
- **DC 분극 σ_e**: 이온차단 조건에서 작은 계단 전압 → 정상 전류 → Ohm 기울기로 전자 전도도.
- **시그모이드 퍼콜레이션 적합**: 도전재 함량에 대한 σ 의 S 자 곡선 — 변곡점 ≈ 퍼콜레이션 문턱.
- **AM:SE (vol./vol.)**: 이 논문의 Fig. 8 x 축은 AM 부피분율 (0.4 = 40:60).
- **순차 혼합 AM+(CA+SE)**: SE 와 도전재를 먼저 섞은 뒤 AM 을 넣는 혼합 순서.
- **In/LiIn 대극**: In 박 — 첫 충전에서 LiIn 합금이 되며 기준 전위 ≈0.6 V vs Li (이 논문: 3.7 V vs In/LiIn = 4.3 V vs Li).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

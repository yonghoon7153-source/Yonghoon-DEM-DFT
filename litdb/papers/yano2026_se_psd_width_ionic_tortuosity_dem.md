# Li₆PS₅Cl 입도 분포 폭이 복합양극 이온 경로 tortuosity 에 미치는 영향 — 원 분말 (넓은 PSD) ↔ 습식 볼밀 분말 (좁은 PSD) 혼합 4 조성 · 차단전극 EIS + EDEM-EEPA DEM + A∗ 최단 경로 (입자 수 보정 τ∗) — Yano · Hofer · Ohsaki (교신) · … · Kwade · Michalowski (*J. Energy Storage* **2026**, 153, 120973)

> slug `yano2026_se_psd_width_ionic_tortuosity_dem` · DOI `10.1016/j.est.2026.120973` · type `experiment + DEM (EDEM 2024.1 EEPA · A* shortest-path τ_geo + 입자 수 보정 τ* · 차단전극 EIS σ_ion/σ_e · SEM · MPM/FEM 없음)` · PDF `d96b041b-1._Effect_of_size_distribution_of_solid_electrolyte_on_tortuosity_of_ionic_conductive_paths_A_combined_experimental_and_simulation_study.pdf` (본문 10 쪽 · SI 없음) · digested `2026-10-30` · status ✅ · OA CC-BY
> topic: size_effect (SE 입도 효과)
> elements: Li, P, S, Cl, Ni, Co, Mn, O
> methods: DEM (EEPA), shortest-path (A-star), EIS, SEM, wet ball milling, sedimentation PSD

<!-- 실독 기록 (2026-10-30)
     본문 10 쪽 전부 200 dpi 렌더로 읽고 pdftotext 로 인용문 대조. SI 없음 ("Data will be made available on request", p.8).
     그림 1 · 2 · 3 · 7 · 8a · 9 · 10 · 11 · 12 · 13 은 벡터 그림이라 PyMuPDF get_drawings 로 눈금선 · 표지 좌표를 직접 읽었다
     (축 = 눈금선 좌표 · 원/사각 = bbox 중심 · 위꼭지 삼각 = 무게중심) → litdb/figures/<slug>/digitized.csv.  그림 4 · 5 · 6 은 래스터.
     표지: [인쇄] = 본문 · 표 · 식에 적힌 값 · [벡터 판독] = 그림 벡터 좌표에서 읽은 값 (±0.1–1 %) · [판독] = 눈으로 읽은 값 ·
     [우리 산술] = 논문 밖 계산 · [미확인] = 원문에 없음.  쪽 = 저널 쪽 번호 (PDF 쪽과 같음, p.1–10).
     크롭 17 장 = 그림 1–13 + 표 1–4 (캡션 뺀 패널 영역) · 전부 열어 확인.
     중복 확인: 정본 litdb/papers/ 전수 (454 장) 에 DOI · "120973" · "Ohsaki" · 제목 낱말 grep → 이 논문 카드 없음 (Ohsaki 는 같은 그룹 카드의 공저자로만 나옴).
     ⚠ 문헌 지도 lit_se_size_map_20261030 §4 · §6 의 "Ohsaki 등" = 이 논문 — 1저자는 Takeru Yano, Ohsaki 는 교신저자. -->

## 0. 이 digest 를 읽는 법 — 우리 질문과 원문 판정

**계기 (2026-10-30)**: 50kg 4차년도 보고 (SE D50 0.7 · 1 · 2 · 3 µm **단분산 대리** · NCM D6 µm 단일 · 85 wt% · 300 MPa · LIGGGHTS DEM + 접촉망 Kirchhoff) 의 문헌 지도 §6 이 *"같은 SE · 같은 방법 계열로 PSD 폭 효과 — 단분산 대리의 직접 검증 · 반론"* 1순위로 올린 논문.

| Q | 판정 (한 줄) | 근거 |
|---|---|---|
| **Q1 PSD 폭이 결과를 바꾸나 (p1 한정어)** | 실험에서는 **바꾼다** — 원 분말 (넓은 PSD) 30 wt% → 볼밀 분말 (좁은 PSD) 30 wt% 로 복합체 σ_ion **≈ 5.1 × 10⁻⁴ → 1.9 × 10⁻⁵ S/cm (≈ 27 배)** · τ_eff **2.15 → 6.72**.  ⚠ 그러나 PSD 폭만 바뀐 것이 아니다: D50 1.76 → 1.27 µm · D90 5.6 → 3.2 µm · 습식 볼밀 (펠릿 σ 4.03 → 1.45 mS/cm) · 건조 응집체 (저자 SEM) 가 함께 움직인다.  중간 조성 (10 · 20 wt%) 은 0 wt% 와 오차 막대가 겹친다 | §3d · §3e · 그림 8a · 9 · [벡터 판독] |
| **Q2 기하 τ ↔ 수송 τ (p4)** | **우리 p4 메시지와 같은 구조** — DEM A\* 기하 τ_geo 는 **1.14–1.17 로 거의 평평**, 실험 τ_eff 는 2.13–6.72.  간극을 *"경로당 입자 수 N × 상수 α"* 한 항 (τ\* = (l + αN)/l0, α 를 0 wt% 한 점에 맞춤) 으로 메우면 0 → 10 wt% 상승은 일부 재현 (2.17 → 2.48), **30 wt% 의 6.7 은 재현 못 함 (2.54)** | 그림 11 · 12 · 13 · 식 (10)–(12) |
| **Q3 밀링 SE 의 σ 손해 (p5)** | 습식 볼밀 (400 rpm · 20 h) 펠릿 σ **4.03 → 1.45 × 10⁻³ S/cm (÷ 2.78)** — 지도 p5 의 밀링 σ 비 목록 (MIN24 1.25 · MIN21 1.33 · CRO 1.45 · SHI 2.3 · BAZ25 2.9) 에 **2.78** 추가.  이 경우 구조 (f) 도 함께 나빠졌다: f = σ_eff/σ₀ **0.127 → 0.013 (÷ 9.8)** [우리 산술] | p.3 · 그림 8a |
| **Q4 연화 안 한 DEM 의 밀도 (p2 · frame [2])** | EEPA · E_LPSCl **21 GPa (연화 없음)** · λp 0.642 DEM 이 400 MPa 에서 ρ_rel **0.728 → 0.722** (기공 ≈ 27–28 %).  실험값은 **그림마다 다르다** — 그림 7 **0.651 → 0.603**, 그림 10 **0.843 → 0.780**, 두 그림 비는 네 점 모두 **1.2952** (= 진밀도 혼합 규칙 차이로 보임 · 저자 설명 없음) | 그림 7 · 10 · §10-2 |
| **Q5 단분산 가정 — 지지 / 반론?** | **기하는 지지 · 수송은 경고.**  같은 논문의 DEM 에서 PSD 폭 (5 구간 이산 PSD) 은 기하 τ 와 밀도를 거의 안 바꾼다 (τ_geo ±1.5 % · ρ_rel −0.8 %).  그러나 **경로당 SE 입자 수 N (= 직렬 접촉 수) 은 20.5 → 26.3 (+28 %)** 로 움직인다 — 우리 망이 접촉마다 Holm 협착 저항을 넣는 바로 그 양이다.  ⇒ p1 에 *"단분산 대리는 같은 D50 에서 PSD 폭 (특히 거친 꼬리) 이 바꾸는 직렬 접촉 수를 담지 않는다"* 를 적을 것 | §7c |

⇒ **분류 한 줄**: *같은 LPSCl 에서 D50 이 아니라 PSD 폭 (거친 꼬리 유무) 을 바꾼 복합양극 실험 + DEM — "넓은 PSD 의 큰 입자가 우회로 (fast-track) 가 되어 경로당 입계 수와 이온 τ 를 줄인다" 는 주장 쪽이며, 실험 효과의 대부분은 밀링 · 응집 · D50 변화와 교란되어 있고 DEM 기하만으로는 재현되지 않는다.*

---

## 1. 한 줄 요약

NCM622 : Li₆PS₅Cl = 70 : 30 wt% 복합체에서 LPSCl 몫을 **원 분말 (D50 1.76 µm, 넓은 PSD)** 과 **습식 볼밀 분말 (D50 1.27 µm, 좁은 PSD)** 로 70:(30−x):x (x = 0 · 10 · 20 · 30) 섞어 400 MPa 로 펠릿을 만들고, 차단전극 EIS 로 σ_ion · σ_e 와 *"전도도 기반 tortuosity"* τ_eff = √(φσ₀/σ) 를 쟀다.
볼밀 분말이 늘수록 상대밀도 ↓ · σ_ion ↓ (30 wt% 에서 급락) · τ_eff ↑ (2.15 → 6.72) · σ_e 는 약간 ↑.
같은 PSD (5 구간 · 크기 ×10) 로 **EDEM-EEPA DEM** 침대를 만들고 **A\* 최단 경로**로 기하 τ_geo 를 재면 **1.14–1.17 로 거의 그대로** — 대신 경로에 든 입자 수 N 이 늘어난다 (평균 20.5 → 26.3).
입계 저항 대리 항 αN 을 경로 비용에 더한 τ\* (α 는 0 wt% 실험값에 맞춤) 가 0–20 wt% 경향은 따라가지만 30 wt% 급등은 못 따라간다 — 저자는 응집 · 경로 두께 · 계면 면적이 모델에 없어서라고 본다.
결론: *"넓은 PSD 의 큰 입자가 우회로를 만들어 이온 전도를 돕는다 (fast-track)."*  **용량 · 율 등 전지 성능은 재지 않았다.**

## 2. 메타 / 동기 / 질문

| 저자 | 저널/년 | DOI | 소재 (SE/CAM) | 연구유형 |
|---|---|---|---|---|
| **Takeru Yano**ᵃ'ᵇ'\* · Moritz Hoferᶜ'ᵈ · **Shuji Ohsaki**ᵃ'\*\* · Hideya Nakamuraᵃ · Satoru Watanoᵃ · Shusaku Asanoᵇ · Gen Inoueᵇ · Arno Kwadeᶜ'ᵈ · Peter Michalowskiᶜ'ᵈ (ᵃ Osaka Metropolitan Univ. 화공 · ᵇ Kyushu Univ. 화공 · ᶜ TU Braunschweig iPAT · ᵈ Battery LabFactory Braunschweig) · \* 교신 T. Yano (tyano@chem-eng.kyushu-u.ac.jp) · \*\* 교신 S. Ohsaki (shuji.ohsaki@omu.ac.jp) | *J. Energy Storage* **153** (2026) 120973 · Research papers · 접수 2025-10-19 · 수정 2026-01-15 · 승인 2026-02-02 · 온라인 2026-02-17 · CC BY | 10.1016/j.est.2026.120973 | **Li₆PS₅Cl (NEI Corp., D50 1.75 µm)** 원 분말 + 습식 볼밀 분말 · **NCM622 (BASF, D50 11 µm 표기)** · 70 : 30 wt% · **무탄소 · 무바인더** | 실험 (볼밀 · 원심 침강 PSD · 일축 성형 · 차단전극 EIS · SEM) + DEM (EDEM-EEPA) + A\* 최단 경로 |

- **키워드 (p.1)**: Discrete element method · All-solid-state batteries · Shortest-path algorithm · Tortuosity.
- **동기 (p.1–2)**: 이온 수송이 보통 율속 → 전극 안 이온 전도 개선이 핵심.  입도 *중앙값* 의 영향은 연구됐지만 (refs 27–32 — Calpa 2019 · Sakuda 2016 · Schlautmann 2023 · Shi 2020 · Park 2020 · Bazzoun 2025) *"the impact of particle size distribution width has not been addressed systematically"* (p.2).  AM 의 PSD 폭을 바꾸면 AM 충전 상태와 SE 망 변화가 얽히므로 **SE 의 PSD 만** 바꾼다 (p.2).
- **질문**: SE PSD 폭 → (i) 펠릿 밀도 · σ_ion · σ_e (ii) 전도도 기반 τ (iii) DEM 침대의 최단 경로 τ_geo 와 경로 입자 수 (iv) 입계 저항을 넣은 경로 비용이 실험 경향을 재현하나.
- **이해관계**: *"no known competing financial interests"* (p.8).  자금 JSPS KAKENHI 22KJ2617 · 24K23019 · JSPS–DFG JRPs-LEAD JPJSJRP20221606 · JST JPMJFS2138 (p.8).  데이터 = 요청 시 (p.8).

---

## 3. 핵심 수치 총정리 ★

### 3a. 재료 · PSD

| 항목 | 값 | 표기 | 출처 |
|---|---|---|---|
| CAM | LiNi₀.₆Co₀.₂Mn₀.₂O₂ (NCM622), BASF, **D50 = 11 µm** (본문) | [인쇄] | p.2 §2.1.1 |
| ⚠ CAM 실측 PSD | Lumisizer CDF (그림 1 파랑 선): **D10 6.58 · D50 8.66 · D90 11.40 µm** · span 0.56 · 분포 6.07–12.6 µm → 본문 *"D50 = 11 µm"* 와 다르다 (§10-12) | [벡터 판독] | 그림 1 |
| SE | Li₆PS₅Cl (LPSCl), NEI Corp., **D50 = 1.75 µm** | [인쇄] | p.2 §2.1.1 |
| 원 분말 (pristine) PSD | **D10 0.80 · D50 1.76 · D90 5.59 µm** · span (D90−D10)/D50 **2.73** · 분포 0.59–12.2 µm | [벡터 판독] | 그림 1 회색 선 |
| 볼밀 분말 (comminuted) PSD | **D10 0.76 · D50 1.27 · D90 3.19 µm** · span **1.91** · 분포 0.60–3.69 µm | [벡터 판독] | 그림 1 빨강 선 |
| PSD 측정 | 원심 침강 (Lumisizer, LUM GmbH) · 개수/부피 가중 [미확인] | [인쇄] | p.2 §2.1.2 |
| 저자 해석 | *"Pristine LPSCl had a broader size distribution than comminuted LPSCl because the coarse particles of pristine LPSCl were comminuted by ball milling."* | [인쇄] | p.2 |
| 크기비 λ = D_NCM/D_SE | 원 분말 **4.93** · 볼밀 **6.82** (실측 D50 기준) · 본문 D50 (11 / 1.75) 로는 6.29 | [우리 산술] | — |
| 조성 | NCM : LPSCl = **70 : 30 wt%** (*"corresponding to a volume ratio of 43.1 : 56.9"*) · LPSCl 몫 = 원 : 볼밀 = (30 − x) : x, **x = 0 · 10 · 20 · 30** | [인쇄] | p.2 §2.1.3 |
| ⚠ 부피비 출처 | 43.1 : 56.9 는 DEM 밀도 (4.750 · 1.540) 로 맞는 값 (NCM 43.07 vol%) · 본문 진밀도 (4.8 · 1.5) 로는 42.2 : 57.8 | [우리 산술] | 표 2 · p.2 |
| 진밀도 (ρ_rel 계산용) | NCM **4.8** · LPSCl **1.5 g/cm³** · 혼합물 = *"linear mixing rule determined from the mixing ratio"* | [인쇄] | p.2 |
| 도전재 · 바인더 | **없음** (분말 셋만 혼합) | [인쇄] | p.2 |

### 3b. 순수 LPSCl 펠릿 (원 분말 ↔ 볼밀 분말)

| 항목 | 원 분말 | 볼밀 분말 | 표기 · 출처 |
|---|---|---|---|
| σ (본문 *"Bulk ionic conductivities"*, 실은 r = R_bulk + R_g.b. 로 계산) | **4.03 × 10⁻³ S/cm** | **1.45 × 10⁻³ S/cm** | [인쇄] p.3 |
| 비 (원/볼밀) | **2.78** | | [우리 산술] |
| Cole–Cole 반원 끝 r (적합 곡선) | ≈ 146 Ω | ≈ 312 Ω | [벡터 판독] 그림 2 |
| r 비 2.14 ↔ σ 비 2.78 | 두 펠릿 두께 · 질량이 다르다는 뜻 (비 1.30) — 펠릿 치수 [미확인] | | [우리 산술] |
| 고주파 한계 | 반원이 다 안 보임 — *"limited measurement frequency range of 8 MHz"* (refs 43–44) | | [인쇄] p.2 |

### 3c. 복합체 상대밀도 — 두 그림이 다르다 ★

| x (볼밀 wt%) | 0 | 10 | 20 | 30 | 출처 |
|---|---|---|---|---|---|
| 그림 7 (실험 · **로그 y 축** 0.5–0.8) | **0.651** (0.624–0.677) | **0.639** (0.614–0.664) | **0.626** (0.598–0.654) | **0.603** (0.569–0.635) | [벡터 판독] |
| 그림 10 실험 (선형 축) | **0.843** (0.809–0.879) | **0.828** (0.796–0.867) | **0.811** (0.775–0.866) | **0.780** (0.737–0.823) | [벡터 판독] |
| 그림 10 DEM (400 MPa) | **0.728** | **0.727** | **0.724** | **0.722** | [벡터 판독] |
| 그림 10 / 그림 7 (실험) | **1.2952** | **1.2953** | **1.2953** | **1.2951** | [우리 산술] — 오차 막대 끝도 같은 비 |

- 본문: 그림 7 = *"relative densities of pellets with different mass fractions"* (p.5), 그림 10 = *"relative densities after compression at 400 MPa in both simulations and experiments"* (p.6) — 같은 400 MPa 실험인데 값이 다르다.
- 비가 **네 조성 · 오차 막대까지 상수**이므로 측정이 아니라 **정규화 (진밀도)** 차이다.  질량 가중 진밀도 0.7·4.75 + 0.3·1.54 = **3.787** ↔ 부피 가중 (조화평균) **2.922 g/cm³** 의 비 = **1.2958** 로 0.05 % 안에서 맞는다 (본문 진밀도 4.8/1.5 로 같은 계산을 하면 1.3176 — 안 맞음) [우리 산술 · 원인 추정].  ⇒ **그림 10 (부피 가중) 쪽이 혼합물 진밀도의 바른 규칙**이다.  ⚠ 저자 설명 없음.
- 성형 압력: 본문 2.1.3 은 *"compressed at 100–400 MPa"* 라 적지만 **결과는 400 MPa 만** 나온다 (압력 의존 그림 · 표 없음).  측정 중 구속압 **37.3 MPa** (p.5).

### 3d. 복합체 유효 전도도 (그림 8a · 차단전극 EIS · 25 °C 여부 [미확인])

| x (볼밀 wt%) | 0 | 10 | 20 | 30 | 출처 |
|---|---|---|---|---|---|
| **σ_ion** (S/cm) | **5.1 × 10⁻⁴** (1.55–8.46 × 10⁻⁴) | **2.2 × 10⁻⁴** (1.24–3.14) | **1.7 × 10⁻⁴** (1.27–2.13) | **1.9 × 10⁻⁵** (1.48–2.18) | [벡터 판독] |
| σ_e (S/cm) | 9.1 × 10⁻³ | 1.16 × 10⁻² | 1.04 × 10⁻² | 1.23 × 10⁻² | [벡터 판독] |
| σ₀ (펠릿 σ 의 선형 혼합) | 4.03 | 3.17 | 2.31 | 1.45 × 10⁻³ | [우리 산술 — 본문 "linear fraction mixing rule"] |
| f = σ_ion/σ₀ | **0.127** | **0.071** | **0.075** | **0.013** | [우리 산술] |
| σ_e/σ_ion | 17.8 | 52 | 60 | 660 | [우리 산술] |

- 본문 (p.6): *"The electronic conductivity (green triangle plots) increased slightly when the mass fraction of comminuted LPSCl exceeded 0%. In contrast, the ionic conductivity (blue square plots) decreased significantly with increasing mass fraction of comminuted LPSCl."*
- 저자 기전 (p.6, 그림 8b 모식): 볼밀 분말은 NCM–NCM 접촉엔 영향이 작지만 *"lengthened ion transport path lengths owing to the absence of large LPSCl particles and increased the number of interfacial particle interfaces, which exhibit lower ionic conductivity than bulk LPSCl."*
- ⚠ **x = 0 의 σ_ion 오차 막대 (1.55–8.46 × 10⁻⁴) 가 10 · 20 wt% 값을 포함한다** — 통계적으로 확실히 갈리는 것은 30 wt% 뿐 (반복 수 n [미확인]).
- σ_ion 0 → 30 wt% 하락 **27.3 배** ↔ 펠릿 σ₀ 하락 2.78 배 [우리 산술].
- 교차 점검 [우리 산술]: f(0) = 0.127 ↔ 정본 `schlautmann2023_se_particle_size_composite_transport` S (NCM811 70:30 wt%, LPSCl D50vol 4 µm) 의 0.254/2.2 = **0.115** — 같은 자릿수.

### 3e. 실험 "tortuosity" (식 (3) τ_eff = √(σ₀·φ/σ_eff))

| x | 0 | 10 | 20 | 30 | 출처 |
|---|---|---|---|---|---|
| τ_eff (그림 9 · 로그 1–10) | **2.15** | **2.88** | **2.78** | **6.72** | [벡터 판독] |
| τ_eff (그림 11 · 13 의 Exp.) | 2.13 / 2.14 | 2.86 / 2.87 | 2.77 / 2.78 | 6.70 / 6.72 | [벡터 판독] |
| 식 (3) 에서 역산한 φ | 0.583 | 0.584 | 0.580 | 0.581 | [우리 산술] (σ₀ 선형 혼합 · 그림 8a σ_ion) |
| τ_eff² (= 그들 정의의 τ²) | 4.61 | 8.28 | 7.75 | 45.1 | [우리 산술] |
| **우리 규약 tau2** = φ_SE·σ₀/σ (φ_SE = 0.578 × ρ_rel 그림 10) | **3.85** | **6.79** | **6.27** | **35.1** | [우리 산술] |
| 우리 규약 tau = √tau2 | 1.96 | 2.61 | 2.50 | 5.92 | [우리 산술] |

- **역산 φ ≈ 0.58 = 고체 기준 LPSCl 부피분율** (진밀도 4.8/1.5 로 0.578) — 기공이 빠진 φ 를 썼다 ⇒ 그들의 "tortuosity" 에 **기공 벌점이 섞여 있다** (§10-5).
- 저자 (p.6): *"The pellet composed of NCM and comminuted LPSCl, with a comminuted mass fraction of 30%, exhibited the highest tortuosity … SEs with a broad particle size distribution and minimal agglomeration improved ionic conductivity."*
- 교차 점검 [우리 산술]: 우리 규약 tau2(0) = 3.85 ↔ schlautmann2023 κ_ion,obs (S) **3.57** — 같은 자릿수.

### 3f. DEM · 최단 경로 결과

| x | 0 | 10 | 20 | 30 | 출처 |
|---|---|---|---|---|---|
| DEM ρ_rel (400 MPa) | 0.728 | 0.727 | 0.724 | 0.722 | [벡터 판독] 그림 10 |
| **τ_geo (A\*)** | **1.14** | **1.14** | **1.17** | **1.15** | [벡터 판독] 그림 11 (무게중심 · bbox 중심이면 +0.01) |
| 경로당 입자 수 N — 평균 | **20.5** | **23.3** | **23.6** | **26.3** | [벡터 판독] 그림 12 (정수 N 재표본 · 합 99.9–100.4 %) |
| N — 최빈 · N ≥ 25 몫 · 범위 | 19 · 19 % · 11–31 | 26 · 41 % · 15–33 | 23 · 37 % · 18–30 | 25 · **81 %** · 20–34 | [벡터 판독] |
| **τ\*** (α = 1.7 × 10⁻⁵, 0 wt% 에 맞춤) | **2.17** | **2.48** | **2.42** | **2.54** | [벡터 판독] 그림 13 |
| 실험 τ_eff (같은 그림) | 2.14 | 2.87 | 2.78 | 6.72 | [벡터 판독] |

- 본문 (p.6): *"The simulated tortuosity (black plots) increased slightly up to 20 wt% of comminuted LPSCl. However, the tortuosity decreased at 30 wt% … The relatively low tortuosity values (∼1) obtained in the numerical simulation were likely underestimated because the simulation considered only the shortest transport pathways."*  ⚠ 범례는 Sim = **빨강 삼각** (검정 = Exp.) — 본문 색 표기 오기.
- 본문 (p.7): *"At 30 wt%, all paths included more than 25 particles per path."* ⚠ 그림 12 녹색 곡선은 N 20–24 에 ≈ 19 % — "모든 경로" 는 과장 (§10-8).
- 본문 (p.7): α = 1.7 × 10⁻⁵ 를 *"to match the experimental value of τ_eff for τ\* under the mass fraction of comminuted LPSCl of 0 wt%"* · *"The value of α is believed to derive from grain boundary resistance, which is not fully understood."*  **단위 미기재** (그림 13 범례 기호는 *k*).

### 3g. 우리 산술 — 기하 · 척도

| 양 | 값 | 식 / 입력 |
|---|---|---|
| DEM 침대 두께 (0.5 × 0.5 mm 판) | **0.478 mm** (x = 0) · 0.482 mm (x = 30) | 0.087 mm³ / (0.25 mm² × ρ_rel) |
| 같은 값 (그림 4 표기 1 × 1 mm 판) | 0.120 mm — 최대 NCM (113.5 µm, ×10) 하나 두께.  그런데 그림 4 의 침대는 2 mm 상자 높이의 ≈ 절반 (≈ 0.9 mm) [판독] 이고 NCM 구는 판 폭의 ≈ 7 % (1 mm 판이면 ≈ 70 µm = 표 4 와 맞음) [판독] → **그림 4 는 1 mm 판으로는 자기정합이지만 0.087 mm³ 와는 안 맞는다** | 0.087 mm³ / (1 mm² × ρ_rel) |
| 실물 환산 (크기 ×10 되돌림) | 판 **50 × 50 µm** · 두께 ≈ 48 µm | ÷ 10 |
| 펠릿 두께 (8 g 이 다 금형에 들어갔다면) | ≈ **16 mm** (x = 0) · 17 mm (x = 30) | bulk 밀도 = 그림 10 ρ_rel × 2.922 → 8 g / (2.464 g/cm³ × 2.011 cm²) |
| ρ_rel 민감도 — LPSCl 결정밀도 1.87 g/cm³ (정본 schlautmann2023 Table S1 · faka2026 Table S5 값) 로 다시 정규화 | **0.758 · 0.745 · 0.730 · 0.702** (NCM 4.75) | 같은 bulk 밀도 ÷ 조화평균 3.249 |
| NCM 원래 E (DEM 은 절반) | 142 GPa | 71 × 2 (본문 *"half of its original value"*) |
| EEPA 끌림 힘 f0 비 | NCM–NCM : NCM–LPSCl : LPSCl–LPSCl = **1 : 0.400 : 0.250** = π/3·10⁻⁵ · 4π/3·10⁻⁶ · 5π/6·10⁻⁶ N → 대표 반경비 R_NCM/R_LPSCl = **4** 로 계산한 값 · f0 = 1.5πγR\* (γ 0.1 J/m²) 로 읽으면 R\* 22.2 · 8.9 · 5.6 µm (어느 반경을 썼는지 [미확인]) | 표 3 |
| τ\* − τ_geo (조성 비) | 1.03 · 1.34 · 1.26 · 1.40 → **1 : 1.31 : 1.23 : 1.36** | 그림 13 − 그림 11 |
| 평균 N (조성 비) | **1 : 1.14 : 1.15 : 1.28** | 그림 12 |
| ⇒ α 를 m 로 읽을 때 필요한 l0 | 0.34 · 0.30 · 0.32 · 0.32 mm (조성마다 다르고 0.48 mm 와도 안 맞음) | αN̄/(τ\*−τ_geo) |

---

## 4. 재료 & 방법 ★

### 4a. 습식 볼밀 (p.2 §2.1.2 · 표 1)
- Pulverisette 7 (FRITSCH) · LPSCl **8 g** + ZrO₂ 볼 **85 g (0.6–0.8 mm)** + **n-헥산 1 mL** (비극성) + **디부틸에터 0.1 mL** (극성) · 절차 = ref [42] (Minnmann 2021 JES) 기반.
- 표 1: 회전 **400 rpm** · 사이클 **40** · 운전 시간 **20 h** · 역회전 **ON**.  밀링 뒤 젖은 분말을 **120 °C 오븐 건조**.
- PSD = 원심 침강 (Lumisizer) — 개수/부피 가중 · 분산매 [미확인].

### 4b. 혼합 · 성형 · 상대밀도 (p.2 §2.1.3)
- NCM · 원 LPSCl · 볼밀 LPSCl = 70 : (30 − x) : x · **TURBULA T 2F 진탕 혼합 15 min**.
- **혼합 분말 8 g → ⌀16 mm 금형 → 일축 손 프레스 100–400 MPa** (결과 = 400 MPa).
- 상대밀도 식 (1): **ρ_rel = w / (π R_c² h ρ)** — w 분말 질량 · R_c 펠릿 반경 · h 두께 · ρ 진밀도 (NCM 4.8 · LPSCl 1.5 g/cm³ · 혼합 = 선형 혼합 규칙).

### 4c. 임피던스 (p.2–3 §2.1.4)
- ZENNIUM PRO (Zahner) · 셀 = **스테인리스 펀치 + PTFE 금형** (= 이온 차단 · 전자 통과 전극) · 주파수 *"from 100 to 8 MHz"* (하한 단위 [미확인]) · 구속압 37.3 MPa (p.5).
- 순수 LPSCl 펠릿: 식 (2) **σ_eff = h / (π R_c r)** (⚠ 인쇄 식에 R_c² 의 제곱이 빠짐 — §10-8) · r = 펠릿 저항 = **R_bulk + R_g.b.** · 등가회로 **R_ohm + (R_bulk ∥ CPE_bulk) + (R_g.b. ∥ CPE_g.b.)** (ZView, Scribner).
- 복합체 (혼합 전도체): 그림 3 — 두 반원.  **r₂ = r_e·r_ion/(r_e + r_ion)** (고주파: 두 경로 병렬) · **r₃ = r_e** (저주파: 이온은 강철에서 막힘) → r_e · r_ion → σ_e · σ_ion.  *"following the method proposed in Ref. [39]"* (ref 39 = Frankenberg 2024 Powder Technol. 고강도 믹서 DEM — 그 논문이 이 방법을 담는지 [미확인]).
- NCM 단독 펠릿 σ_e 는 *"short-circuiting"* 으로 못 쟀다 → **이온 τ 만** 계산 (p.3).
- 식 (3): **τ_eff = √(σ_eff,LPSCl · φ / σ_eff,CE)** — σ_eff,LPSCl = 그 조성의 펠릿 σ 를 *"linear fraction mixing rule"* 로 섞은 값 · φ = *"volume fraction"* (정의 미기재 → 역산 0.58 = 고체 기준) · refs [42, 45] (Minnmann 2021 · Bielefeld 2020).

### 4d. DEM (p.3–4 §2.2.1–2.2.2 · 표 2–4 · 그림 4) ★

| 항목 | 값 | 표기 |
|---|---|---|
| 코드 | **EDEM 2024.1 (Altair)** | [인쇄] p.3 |
| 운동식 | Newton 병진 · 회전 (식 4–5) | [인쇄] |
| 접촉 법칙 | **EEPA (Edinburgh Elasto-Plastic Adhesion, Thakur 2014 ref 46)** — 소성 · 점착 | [인쇄] p.3 |
| 소성비 | λp = 1 − k₁/k₂ = 1 − E₁\*/E₂\* (식 6) · δp = λp^(1/m) δn (식 7) · λp = 0 이면 완전 탄성 | [인쇄] |
| E\* · R\* | 1/E\* = (1−νi²)/Ei + (1−νj²)/Ej (식 8) · 1/R\* = 1/Ri + 1/Rj (식 9) | [인쇄] |
| NCM (표 2) | ρ **4.750 g/cm³** · ν **0.25** · E **71 GPa** (원래 값의 **절반** — 계산비용) · COR 0.25 · 정지마찰 0.5 · 구름마찰 0.01 | [인쇄] |
| LPSCl (표 2) | ρ **1.540 g/cm³** · ν **0.37** · E **21 GPa** (연화 없음) · COR 0.25 · 정지마찰 0.5 · 구름마찰 0.01 | [인쇄] |
| EEPA (표 3) | 일정 끌림 힘 f0: NCM–NCM **−1.047 × 10⁻⁵ N** · NCM–LPSCl **−4.189 × 10⁻⁶** · LPSCl–LPSCl **−2.618 × 10⁻⁶** · meso-surface energy **0 J/m²** · 접촉 소성비 NCM–NCM **0.38** · NCM–LPSCl **0.619** · LPSCl–LPSCl **0.642** · slope exponent **1.5** · tensile exponent **1** · tangential stiff multiplier **0.67** | [인쇄] |
| f0 설정 | Hertz–Mindlin + **JKR 의 0 겹침 점착력**에 맞춤 · 표면에너지 **0.1 J/m²** (refs 47–48) | [인쇄] p.3 |
| λp 출처 | NCM 0.38 (Cheng 2017 ref 49) · LPSCl 0.642 (Papakyriakou 2021 ref 50) · 이종 접촉 = 등가 소성비 0.619 (Yano 2024 ref 51) | [인쇄] p.3–4 |
| 전체 입자 부피 | **0.087 mm³** | [인쇄] p.3 |
| PSD | 실측 CDF 를 **20 % 구간 다섯**으로 나누고 각 구간의 중앙 지름 (= D10 · D30 · D50 · D70 · D90) 을 대표값으로 · **크기 ×10** (표 4: NCM 65.0 · 75.8 · 86.0 · 98.2 · 113.5 µm / 원 LPSCl 7.97 · 12.1 · 17.5 · 32.8 · 55.9 / 볼밀 7.61 · 10.9 · 12.7 · 19.3 · 31.8 µm) | [인쇄] p.4 |
| 척도 처리 | *"The same contact and material parameters were used for all cases without introducing additional scaling factors. Therefore, the results are intended to provide qualitative insights into mechanical behavior rather than to quantitatively reproduce experimental deformation."* | [인쇄] p.4 |
| 질량 분율 | NCM : 원 : 볼밀 = 70 : (30 − x) : x | [인쇄] |
| 기하 · 압축 | 수평 **주기 경계** · **0.5 × 0.5 mm 판** 위로 중력 낙하 충전 → **위 펀치 25 mm/s 하강** · 400 MPa (그림 10 본문) · ⚠ 그림 4 표기 **1 mm × 1 mm × 2 mm** (§10-6) | [인쇄] p.4 · 그림 4 |
| 언로딩 · 이완 · 밀도 판독 시점 | [미확인] | — |
| 시드 · 반복 | [미확인] | — |

### 4e. 입자 처리 ★ (우리 "무질서 처리" 칸)
- **형상**: 전부 **구** — NCM · LPSCl 모두.  실측 SEM 의 판상 · 각진 LPSCl, 응집체는 표현하지 않는다 (저자도 *"ignoring particle shapes"*, p.6).
- **PSD**: 실측 넓은 PSD 를 **5 개 이산 크기**로 (구간 20 %) — 단분산 아님 · 연속 분포도 아님.  크기 ×10 에 매개변수는 그대로 → 점착 (f0 일정) 대 하중 비가 실물과 달라진다 (§10-6).
- **소성**: EEPA 의 **접촉 소성** (하중 · 제하 강성비 λp) — 입자 **형상 소성 (유동) 아님**.  겹침 δ 는 기하 대리량이다 (우리 DEM 의 hysteresis 와 같은 층위).
- **점착**: 쌍 종류별 **일정 끌림 힘** (meso-surface energy 0) — 입자 크기 무관한 같은 힘 → 작은 입자일수록 상대 점착이 크다.  그러나 *"agglomeration structures observed in the experiments were not explicitly reproduced"* (p.7).
- **강성**: LPSCl **21 GPa 그대로** (우리 E_eff 1.35 GPa 연화와 반대 선택) · NCM 은 계산비용 때문에 **절반 (71 GPa)**.

### 4f. 최단 경로 (p.4 §2.2.3 · 그림 5)
- **A\* 탐색** (Hart 1968 ref 52) — Dijkstra 에 휴리스틱을 더한 것 (휴리스틱 0 이면 Dijkstra).
- 노드 = 입자 (DEM 자료에서 Python 으로 추출) · **간선 비용 = 입자 간 거리** · 휴리스틱 = **위 펀치 ↔ 아래 펀치 거리**.  노드가 LPSCl 만인지 · 간선 = 접촉 (겹침) 쌍만인지 [미확인 — 그림 5 의 경로는 회색 구만 보임].
- 식 (10) **τ_geo = l / l0** — l = 실제 최단 경로 비용 · l0 = 이상 경로 비용 (= 펀치 간 거리) · 저자 명칭 *"geodesic tortuosity factor"*.
- 식 (11) **τ_geo = √τ_eff** — *"conceptually discussed within the framework of the parallel pore model"* (⚠ §10-4).
- 조건마다 **시작 입자 100 개 → 100 경로 평균** (p.4–6).
- 식 (12) **τ\* = (l + αN) / l0** — N = 경로의 입자 수 · α = *"the coefficient derived from grain boundary resistance"* · 경로 비용을 *"transport-related costs that include resistance components [54]"* 로 넓힌 것 (p.7).

---

## 5. 결과 — 섹션별 상세 (그림 실독 포함)

### 5.1 PSD (그림 1)
- 실험 CDF (선) 와 DEM 입력 (막대, 크기 ÷10 로 그림) 을 한 축 (0.5–20 µm, 로그) 에.  막대 높이 0.2 · 0.4 · 0.6 · 0.8 · 1.0 = 20 % 구간 · 막대 위치 = 구간 중앙 지름 (원 LPSCl 막대 = 0.79 · 1.20 · 1.75 · 3.27 · 5.57 µm [벡터 판독] = 표 4 ÷ 10).
- 두 LPSCl 의 **D10 은 거의 같다 (0.80 vs 0.76 µm)** — 갈리는 것은 **거친 꼬리** (D90 5.59 vs 3.19 · 최대 12.2 vs 3.7 µm).  ⇒ 이 논문의 "넓은 / 좁은 PSD" = **"거친 꼬리가 있다 / 없다"** 에 가깝다.
- NCM 은 좁다 (span 0.56) · 6–12.6 µm.

### 5.2 순수 LPSCl 펠릿 (그림 2)
- 원 분말 반원 끝 ≈ 146 Ω · 볼밀 ≈ 312 Ω [벡터 판독], 그 뒤 저주파 꼬리 (차단전극).  고주파 쪽 반원이 잘림 (8 MHz 한계).
- σ: 4.03 → 1.45 mS/cm.  저자는 볼밀 분말의 σ 하락 원인을 따로 논하지 않는다 (입계 증가 · 결정성 손상 · 용매 잔류 등 [미확인]).

### 5.3 복합체 임피던스 (그림 3)
- 대표 (70:30, 원 분말) 곡선: 고주파 시작 ≈ 38 Ω · 첫 반원 끝 r₂ ≈ 216 Ω · 둘째 반원 끝 r₃ = r_e ≈ 310 Ω [벡터 판독] → r_ion ≈ 717 Ω [우리 산술].
- ⚠ 이 대표 곡선의 r_ion/r_e ≈ **2.3** 은 그림 8a 의 0 wt% σ_e/σ_ion ≈ **17.8** 과 안 맞는다 (같은 펠릿이면 같아야 함) — 다른 압력 · 다른 시료일 수 있음 [미확인] (§10-9).

### 5.4 SEM (그림 6 — **펠릿 표면**, 40 µm 눈금)
- 흰 입자 = NCM (둥근 5–12 µm 급) · 회색 = LPSCl.
- (a) 70:30:0: **판상 회색 LPSCl 덩어리 ≈ 25–40 µm** [판독] 가 보인다 — 측정 PSD 최대 (12.2 µm) 보다 크다 → 눌려 퍼진 응집체로 보인다 [추정].
- (b)–(d) 볼밀 포함: *"more uniform particle size distribution. However, instead of large LPSCl primary particles, agglomerates of fine comminuted LPSCL particles were observed"* (p.5).  (b) 는 어두운 영역 (기공 또는 촬영 대비 차 — 구분 불가) 이 유난히 많다 [판독].

### 5.5 상대밀도 (그림 7 · 10)
- 볼밀 분율 ↑ → ρ_rel ↓.  저자 해석 (p.6): ① 좁은 PSD 는 덜 치밀하게 쌓인다 ② 젖은 분말 건조 중 생긴 **미세 응집체가 진탕 혼합기에서 충분히 안 풀렸고**, 응집체는 밀도가 낮다.  Frankenberg 2025 (ref 26) 의 *"dispersive mixing is crucial"* 인용.
- DEM 도 같은 방향이지만 폭이 **≈ 10 배 작다** (DEM −0.006 vs 실험 −0.063, 그림 10).  저자: *"attributed to ignoring particle shapes and the relatively strong agglomeration of fine LPSCl particles. That is, a better mixing quality was achieved in the simulation than in the experiments."* (p.6).
- 절대값: DEM 0.722–0.728 < 실험 (그림 10) 0.780–0.843.  ⚠ 실험 쪽은 진밀도 규칙에 따라 0.60–0.65 (그림 7) 또는 0.70–0.76 (LPSCl 1.87 g/cm³ 로 재정규화) 까지 움직인다 (§3c · §3g).

### 5.6 전도도 (그림 8)
- (a) σ_e ≈ 1 × 10⁻² S/cm 로 거의 평평 (볼밀 첨가 시 약간 ↑) · σ_ion 5.1 × 10⁻⁴ → 1.9 × 10⁻⁵ S/cm.
- (b) 모식: 넓은 PSD (큰 노란 SE) 는 이온이 큰 입자를 관통해 짧게 · 좁은 PSD 는 작은 입자 사이를 굽이쳐 길게 — 전자 경로 (빨강 NCM) 는 둘 다 비슷.

### 5.7 tortuosity — 실험 (그림 9)
- 2.15 · 2.88 · 2.78 · 6.72 — **10 · 20 wt% 는 사실상 같고 30 wt% 만 튄다**.  저자: *"The addition of fine particles increased tortuosity, primarily due to the increased particle–particle interfaces and associated interfacial resistances."* (p.6).

### 5.8 DEM 최단 경로 (그림 5 · 11 · 12)
- 그림 5: 두 판 (펀치) 사이를 잇는 경로 예 — 큰 구 (원 분말의 거친 입자) 가 경로에 끼어 있다.
- 그림 11: τ_geo **1.14 · 1.14 · 1.17 · 1.15** — 실험 τ_eff 보다 훨씬 작다.  저자 이유 ① *"considered only the shortest transport pathways. In real composite electrodes, multiple complex paths contribute"* ② *"the grain boundary resistance … affected tortuosity; however, the simulation results did not consider grain boundary resistance"* · Sangrós 2025 (ref 53) *"the contact resistance is decisive"* 인용.
- 그림 12: 경로당 입자 수 분포 — 볼밀 분율 ↑ 이면 오른쪽 이동 (평균 20.5 → 26.3).  *"This suggests that the effect of the grain boundary resistance was stronger at 30 wt% than under other conditions."* (p.7).

### 5.9 수정 tortuosity τ\* (그림 13)
- α (= k) = 1.7 × 10⁻⁵ 를 0 wt% 에 맞춘 뒤: τ\* 2.17 · 2.48 · 2.42 · 2.54 ↔ 실험 2.14 · 2.87 · 2.78 · 6.72.
- 저자 (p.7–8): 30 wt% 의 큰 차는 *"SE particle agglomeration, particle–particle interfacial area, and ionic transport pathway thickness"* 때문 — 응집은 *"not explicitly reproduced"* · 경로 두께는 입자 크기에 달려 작은 입자일수록 τ 가 커질 수 있다 · *"these factors were not considered in the present simulation"*.
- **fast-track 해석** (p.8): *"when the particle size distribution was broad, the presence of large particles reduced the number of grain boundaries in the ionic conduction pathway. This can be considered a 'fast-track' effect. Moreover, inspection of simulation snapshots showed that large particles having a wide particle size distribution were included in the conduction pathways."*

### 5.10 결론 (p.8, 인쇄)
1. *"SEs with a broader particle size distribution exhibited higher ionic conductivity in the cathode layer than SEs with a narrower distribution."*
2. 전극 구조 생성 + 이온 경로 평가의 수치 방법을 만들었다.
3. *"larger particles can create bypass routes, enhancing ionic conductivity within the electrode layer."*
- 한계 (p.8): *"excessively large or small particles or strong asymmetric size distributions (i.e., mainly fine or coarse particles) may adversely affect connectivity with the active material"* · 앞으로 AM PSD · AM–SE 접촉 형태 · SE 응집 상태 · AM 이용률 (Kissel 2025 ref 56) 로 넓힐 것.

---

## 6. 우선 질문 — 원문 대조

### Q1. PSD 폭은 독립 변수였나?
- **아니다.** 축 하나 (볼밀 분율 x) 위에서 함께 움직인 것: ① PSD 폭 (span 2.73 → 1.91) ② **D50 (1.76 → 1.27 µm)** · D90 (5.59 → 3.19) ③ **밀링 손상** (펠릿 σ 4.03 → 1.45) ④ **건조 응집** (SEM · 저자 서술) ⑤ 상대밀도 (0.843 → 0.780, 그림 10).  저자도 ④ 를 30 wt% 불일치의 원인으로 든다.
- 그러니 *"넓은 PSD → 높은 σ_ion"* 은 실험상 **"원 분말 (거친 꼬리 포함 · 무밀링) → 높은 σ_ion"** 으로 읽어야 정확하다.

### Q2. 기하 τ 와 실험 τ 의 간극은 무엇으로 메웠나?
- 경로마다 **입자 하나에 일정 비용 α** (입계 저항 대리).  우리 망 언어로는 **"접촉마다 같은 직렬 저항"** — 접촉 면적 · σ 에 무관한 상수 하나다.  우리 접촉망은 같은 자리에 **Holm R = 1/(2σa)** (면적 의존) 를 넣는다.
- α 는 한 점 (0 wt%) 에 맞춘 **자유 매개변수**이고 단위 · l0 정의가 없어 재현할 수 없다 (§3g 마지막 줄 · §10-7).

### Q3. 볼밀 SE 의 σ 손해 vs 구조 이득 (p5 손익분기선의 형식)
- 이 데이터에선 **둘 다 손해**: 물성 σ₀ ÷ 2.78 · 구조 f ÷ 9.8 (0 → 30 wt%) [우리 산술].  지도 p5 의 *"구조 이득이 물성 손해를 넘는가"* 질문에서 **넘지 못한 사례** (단, 구조 손해는 응집 · 밀도 저하 탓이 크다).

### Q4. 연화 없는 DEM 이 실험 밀도에 닿나? (frame [2])
- E_LPSCl 21 GPa · EEPA λp 0.642 · 400 MPa → **ρ_rel 0.72–0.73 (기공 27–28 %)**.  실험 (그림 10 규칙) 0.78–0.84 보다 성기다 — 우리 frame [2] 의 *"강체구 + 탄성/접촉 소성만으로는 ~20 % 아래로 못 간다"* 와 같은 방향.
- ⚠ 실험 기준값 자체가 진밀도 규칙에 따라 0.60–0.84 범위로 흔들린다 → **"DEM 이 덜 치밀하다" 의 크기는 확정 불가**.

### Q5. 단분산 가정 → §7c.

---

## 7. 우리 DEM+MPM 대비 ★ (우리 쪽 근거 = `docs/50kg/report_y4/storyline_draft1.md` · 문헌 지도 `docs/50kg/report_y4/lit_se_size_map_20261030.md` · CLAUDE.md frame [1]–[5])

### 7a. 항목별 대조

| 항목 | 이 논문 | 우리 (50kg 4차년도) | 같음 / 다름 · 이유 |
|---|---|---|---|
| 재료 | NCM622 + LPSCl · 70 : 30 wt% (SE 56.9 vol% 고체 기준) · 무탄소 | NCM (D6 µm) + LPSCl · **85 wt% AM** · 무탄소 두 상 | SE 가 그들 쪽에서 부피 다수 · 우리 쪽은 AM 다수 → 퍼콜레이션 여유가 다르다 |
| SE 입도 | D50 1.76 (원) · 1.27 µm (볼밀) · 넓은 실측 PSD (5 구간) | D50 0.7 · 1 · 2 · 3 µm **단분산 대리** | 그들의 D50 은 우리 D1 ↔ D2 사이 |
| λ = D_AM/D_SE | **4.93 → 6.82** (실측 D50) | 8.57 · 6 · 3 · 2 | 우리 축 안 (D1 ↔ D2 · D0.7 ↔ D1 사이) |
| DEM 코드 · 접촉 | EDEM · **EEPA** (접촉 소성 λp + 일정 끌림 힘) | LIGGGHTS · 유효 입력 규약 (SE 1.35 GPa · 선행 이종기술 DEM 과 같은 계열) | 둘 다 **형상 소성 없음** (구 · 겹침 = 대리량) |
| SE 강성 | **21 GPa (연화 없음)** | 1.35 GPa (유효 · 물성 22 GPa 와 두 줄 표기) | 정반대 선택 — 그들 ρ_rel 0.72–0.73 (기공 27–28 %) @ 400 MPa |
| AM 강성 | 71 GPa (원래의 절반) | [이 카드 범위 밖] | — |
| 크기 척도 | **×10** (같은 매개변수) → 실물 환산 판 50 × 50 µm · 두께 ≈ 48 µm | 실크기 · 판 50 × 50 µm · 두께 ≈ 122–126 µm | 측방 크기가 실물 환산으로 같다 · 그들은 점착 대 하중 비가 실물과 다름 |
| 압력 · 상태 | 400 MPa (판독 시점 · 이완 [미확인]) | 목표 300 MPa · 판 고정 이완 끝 (D2 279.8 · D3 291.4 MPa) · 언로딩 없음 | — |
| 기공 | DEM 27–28 % (400 MPa) | 판 고정 D2 16.74 · D3 18.96 % (storyline §3) | 조성 · 압력 · E 규약이 다 달라 **수치 비교 금지** — 방향 (연화 없는 DEM 은 성김) 만 |
| 기하 τ | A\* · 간선 = 입자 간 거리 · 휴리스틱 = 펀치 거리 · 100 경로 평균 · **1.14–1.17** | 최단 경로 / 두께 (Dijkstra · `tau_geo_SE_dij` 계열) | 같은 양 (기하 τ) — 우리 D-series 값은 보고서 p4 정본 |
| 수송 τ | 실험 √(φσ₀/σ) (φ 고체 기준) · 모형 τ\* = τ_geo + αN/l0 | 접촉망 Kirchhoff + 접촉마다 Holm 협착 → f · tau2 = φ_SE·σ₀/σ_eff (φ = 전극 부피 기준) | **τ\* 의 αN = 우리 협착 저항의 1-매개변수 축약판** (면적 무관 상수) |
| 이름 | τ_eff (√ 값) · *"geodesic tortuosity factor"* = l/l0 | tau2 = 수송 tortuosity (τ² 쪽) · tau = √ · τ_geo = 기하 | 그들 τ_eff² ↔ 우리 tau2 (단 φ 기준 다름) · 그들 "factor" 는 τ² 가 아님 (우리 규약 위반 이름) |
| 전자 σ | 실측 ≈ 1 × 10⁻² S/cm (무탄소) | AM–AM 망 (p4 · 탄소 없음) | 그들 값은 다른 무탄소 카드보다 20–40 배 높음 (§10-10) → 비교 금지 |
| 전지 성능 | **없음** | 없음 (p7 다음 = 3D 전기화학) | 둘 다 구조 · 수송까지 |

### 7b. 문헌 지도 (`lit_se_size_map_20261030`) 에서의 자리 — 보고서 쪽별

| 쪽 | 이 논문이 주는 것 | 쓸 때의 한정어 |
|---|---|---|
| **p1** 비교 틀 | ★ *"PSD 폭이 결과를 바꾼다"* 한정어의 **같은 SE (LPSCl) 직접 사례** — 지도 §3 p1 *"빠진 것 = … PSD 폭이 결과를 바꾼다 한정어"* 를 채운다.  λ 4.9 → 6.8 이 우리 축 (2–8.57) 안 | 실험 효과는 밀링 · 응집 · D50 변화와 교란 · DEM 기하는 PSD 폭에 둔감 |
| **p2** 공간 점유 · 압밀 | 볼밀 (좁은 PSD + 응집) → 복합체 ρ_rel ↓ (그림 10 0.843 → 0.780) · DEM 은 같은 방향 · 1/10 크기 · 연화 없는 EEPA DEM 기공 27–28 % @ 400 MPa | 실험 ρ_rel 은 진밀도 규칙에 따라 0.60–0.84 (§3c) |
| **p4** 이온 망 연결성 · 병목 | ★ **기하 τ (1.14–1.17, 평평) ↔ 수송 τ (2.1–6.7, 움직임)** = p4 의 *"직선성 · 연결성 · 오믹 저항이 서로 다른 정보"* 의 외부 사례 · 그 간극을 *경로당 입자 수 × 입자당 저항* 으로 설명 → 우리 **협착 ↔ bulk 소산 몫** 그림의 문헌 짝 | τ\* 는 1 매개변수 맞춤 · 30 wt% 미재현 · 그들 τ_eff 의 φ 에 기공 섞임 |
| **p5** 구조 vs 물성 | 볼밀 LPSCl 펠릿 σ 비 **4.03 / 1.45 = 2.78** → 지도 p5 의 밀링 σ 비 목록에 추가 (덱의 5.1/2.3 = 2.217 보다 크다) · 이 사례에선 f 도 ÷ 9.8 (구조도 손해) | 밀링 조건 (습식 · 400 rpm · 20 h · 120 °C 건조) · σ 를 *"bulk"* 로 불렀지만 r = R_bulk + R_g.b. |
| **p7** 관측 경향 · 다음 | *"문헌 방향 (카드)"* 열에: **"PSD 폭 (거친 꼬리) ↓ → σ_ion ↓ · τ ↑ · ρ_rel ↓ (Yano 2026 · 밀링 · 응집 교란) · DEM 기하 τ 평탄"** | 용량 자료 없음 — "최적" 서사로 쓰지 않음 |
| p3 · p6 | 직접 기여 없음 (피복 · 두께 방향 분포 안 다룸) | — |

### 7c. ★ 단분산 가정 — 지지인가 반론인가
- **지지 쪽 (기하)**: 같은 논문의 DEM 에서 PSD 폭을 바꿔도 **τ_geo 1.14 → 1.17 (최대 +2.4 %)** · **ρ_rel 0.728 → 0.722 (−0.8 %)**.  5 구간 이산 PSD 로 넓이를 넣어도 *기하* 는 거의 안 움직인다 ⇒ 같은 D50 의 단분산 대리가 **기하 1차 근사**로는 크게 틀리지 않는다.
- **경고 쪽 (수송)**: 같은 DEM 에서 **경로당 SE 입자 수 N 은 20.5 → 26.3 (+28 %)**, N ≥ 25 인 경로 19 → 81 %.  우리 망은 **접촉마다 협착 저항**을 직렬로 넣으므로 N 이 곧 저항이다 — 그리고 CLAUDE.md 의 ps45 기록 (10-13, Hertz) 은 우리 수송 tortuosity 의 **73–75 % 가 SE–SE 접촉 협착**이고 협착을 뺀 같은 망은 1.25–1.79 라고 적는다.  ⇒ **우리 수송 지표는 바로 N 에 민감한 구조**이고, 단분산 대리는 같은 D50 에서 **거친 꼬리가 만드는 "fast-track" (N 감소) 을 담지 못한다**.
- **방향 [추정]**: 실제 넓은 분말은 같은 D50 의 단분산 침대보다 경로당 직렬 접촉이 **적을 수** 있다 → 단분산 대리의 수송 tortuosity 는 그런 분말 대비 **높게 나올 가능성**.  그러나 이 논문은 같은 D50 을 비교하지 않았으므로 크기 · 부호를 이 데이터로 확정할 수 없다.
- ⇒ **판정: 반론 아님 · 한정어 필요.**  p1 문구 제안: *"단분산 대리 입도 = D50 하나 — PSD 폭 (특히 거친 꼬리) 은 기하 τ 엔 작게, 경로당 직렬 접촉 수 · 실측 σ_ion 엔 크게 나타난다는 보고가 있다 (Yano 2026 · 실험 쪽은 밀링 · 응집 교란)."*
- ⚠ 이 논문은 우리 D-series 의 **방향** (D 를 바꿨을 때) 을 검정하지 않는다 — D50 은 축이 아니었다.  다만 λ > 1 영역 (4.9 → 6.8) 에서 *"더 고운 쪽이 직렬 계면 수 증가로 질 수 있다"* 는 실험 사례로 p7 의 *"반대 / 비단조"* 칸 해석에 쓸 수 있다 (Schlautmann 2023 의 λ < 1 *"작을수록 좋다"* 와 짝).

### 7d. frame [4] / [5]
- **frame [5]**: 이 논문은 **수송 절반 (실험 σ + 경로 기하)** 과 **충전 절반 (DEM 밀도)** 을 갖고, **역학의 형상 절반 (소성 유동 · 응집 · 파괴)** 이 없다 — 저자 스스로 응집 · 형상 · 경로 두께 결손을 든다.  우리 MPM (형상 소성) 과 접촉망 (면적 의존 협착) 이 채우는 칸이다.
- **frame [4]**: DEM 은 실험 PSD 만 받고 독립으로 돌렸다 (교차적합 없음) — 단 τ\* 의 α 는 **실험 한 점에 맞춘 값**이라 τ\* 의 0 wt% 일치는 검증이 아니다.  나머지 세 점 (10–30 wt%) 만이 예측이고, 그중 30 wt% 는 실패 = **모델 한계의 정량** (2.54 vs 6.72).

---

## 8. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | PSD: 실험 CDF (선: NCM · 원 · 볼밀) + DEM 5 구간 막대 (×10 축소 표시) · 0.5–20 µm 로그 | ★ **넓은 / 좁은 = 거친 꼬리 유무** (D10 같음 · D90 5.6 vs 3.2) — p1 PSD 폭 한정어의 그림 근거 |
| 2 | 순수 LPSCl 펠릿 Cole–Cole (원 · 볼밀 · 적합) · 반원 끝 r ≈ 146 · 312 Ω | 밀링 σ 손해 (p5) |
| 3 | 대표 복합체 Nyquist · r₂ = r_e r_ion/(r_e + r_ion) · r₃ = r_e | 혼합 전도체 차단전극 해석 형식 (§10-9 불일치) |
| 4 | DEM 계산 영역 (그림 표기 1 × 1 × 2 mm) · 회색 SE + 흰 NCM 구 | 영역 크기 (본문 0.5 mm 와 불일치 · §10-6) |
| 5 | A\* 결과 예 — 두 판 사이 경로 (큰 구 포함) | ★ fast-track 의 그림 (큰 입자가 경로에 낌) |
| 6 | 펠릿 표면 SEM (a) 70:30:0 (b) 70:20:10 (c) 70:10:20 (d) 70:0:30 · 40 µm | 응집 · 판상 LPSCl 덩어리 (측정 PSD 밖 크기) |
| 7 | 상대밀도 vs 볼밀 wt% (**로그 y**) 0.651 → 0.603 | §3c 정규화 문제 |
| 8 | (a) σ_e · σ_ion vs 볼밀 wt% (로그) (b) 넓은 ↔ 좁은 PSD 의 전자 · 이온 경로 모식 | ★ σ_ion 27 배 하락 · σ_e 평탄 |
| 9 | 실험 τ_eff vs 볼밀 wt% (로그 1–10) | 30 wt% 급등 |
| 10 | 상대밀도 실험 (오차) vs DEM (400 MPa) | 연화 없는 EEPA DEM 0.72–0.73 · 실험값과 그림 7 의 1.2952 배 |
| 11 | 실험 τ_eff vs DEM τ_geo (로그 1–7) | ★ **기하 τ 평탄 ↔ 수송 τ 변화** (p4) |
| 12 | 경로당 입자 수 분포 (4 조성) | ★ N = 직렬 접촉 수 — 우리 협착 저항의 개수 축 |
| 13 | τ\* (α = 1.7 × 10⁻⁵) vs 실험 | 1-매개변수 입계 보정의 성공 (0–20 wt%) · 실패 (30 wt%) |
| 표 1 | 습식 밀링 조건 (400 rpm · 40 cycles · 20 h · reverse ON) | p5 밀링 조건 |
| 표 2 | DEM 입자 물성 (NCM ρ 4.750 · ν 0.25 · E 71 / LPSCl ρ 1.540 · ν 0.37 · E 21 GPa · COR 0.25 · μs 0.5 · μr 0.01) | DEM 매개변수 대조 |
| 표 3 | EEPA (f0 셋 · meso-surface energy 0 · λp 0.38 / 0.619 / 0.642 · 지수 1.5 · 1 · 0.67) | 접촉 소성 · 점착 규약 |
| 표 4 | DEM 5 구간 지름 (×10) — NCM 65.0–113.5 · 원 7.97–55.9 · 볼밀 7.61–31.8 µm | PSD 이산화 방식 |

## 9. Post-processing ★
- **PSD**: Lumisizer CDF → 20 % 구간 중앙 지름 다섯 (= D10 · D30 · D50 · D70 · D90) → ×10.
- **밀도**: 두께 측정 → 식 (1) (진밀도 선형 혼합 — 규칙 모호 · §3c).
- **EIS**: ZView 등가회로 적합 → 펠릿 r = R_bulk + R_g.b. → 식 (2) · 복합체 두 반원 → r_e · r_ion → σ_e · σ_ion → 식 (3) τ_eff (σ₀ = 펠릿 σ 선형 혼합 · φ 고체 기준으로 보임).
- **DEM → 그래프**: 입자 정보 추출 (Python) → A\* (간선 = 입자 간 거리 · 휴리스틱 = 펀치 거리) → 100 경로 평균 τ_geo · 경로별 N 분포 → τ\* (α 한 점 맞춤).
- **그림**: 조성 4 점 · 오차 막대 = 표준편차로 보임 (반복 수 [미확인]) · DEM 은 오차 막대 없음 (시드 수 [미확인]).
- **우리 후처리 (이 카드)**: 그림 벡터 좌표 판독 (digitized.csv) · PSD D10/D50/D90 계산 · 그림 7 ↔ 10 비 · φ 역산 · 우리 규약 tau2 재계산 · DEM 침대 두께 · τ\* 재현 시도.

## 10. 비판 / 주의 / 한계 ★ (over-claim 방지)

1. **PSD 폭이 단독 변수가 아니다** — D50 · D90 · 밀링 손상 (σ₀ ÷ 2.78) · 건조 응집 · 상대밀도가 같은 축에서 움직인다 (§6 Q1).  저자의 *"broader PSD → higher σ_ion"* 은 *"무밀링 원 분말 → higher σ_ion"* 과 구분되지 않는다.
2. **실험 상대밀도가 두 그림에서 1.2952 배 다르다** (그림 7 ↔ 10, 네 점 · 오차 막대 모두) — 질량 가중 ↔ 부피 가중 진밀도 차 (1.2958) 로 설명됨 [우리 산술 · 원인 추정 · 저자 설명 없음].  게다가 LPSCl 진밀도 1.5 (본문) / 1.54 (DEM) 는 다른 정본 카드의 1.87 g/cm³ 보다 낮아 ρ_rel 이 부풀 수 있다 (1.87 로 다시 하면 0.70–0.76).  ⇒ **실험 ρ_rel 절대값 · "DEM 이 덜 치밀" 의 크기는 인용 금지**, 방향만.
3. **오차 막대가 겹친다** — x = 0 의 σ_ion 막대 (1.55–8.46 × 10⁻⁴) 가 10 · 20 wt% 값을 포함 · τ 그림엔 오차 막대 없음 · 반복 수 미기재 → 확실한 신호는 **30 wt% 하나**.
4. **τ 정의가 서로 어긋난다** — 식 (3) τ_eff 는 이미 √(φσ₀/σ) 인데 식 (11) τ_geo = √τ_eff 를 그대로 쓰면 τ_geo 가 4 제곱근이 된다 (병렬 기공 모델로는 τ_geo = τ_eff).  그림 11 은 둘을 같은 축에 직접 비교 (= 식 (3) 정의로 읽은 것으로 보임).  l/l0 를 *"tortuosity factor"* 라 부른다 — 우리 규약에서 *factor* 는 τ² 에만 쓴다.
5. **φ 에 기공이 빠졌다** — 역산 φ = 0.580–0.584 = 고체 기준 LPSCl 분율 (0.578) ⇒ τ_eff 에 기공 벌점이 섞임.  우리 규약 (φ = 전극 부피 기준) 으로 다시 하면 tau2 3.85 · 6.79 · 6.27 · 35.1 (§3e).
6. **DEM 척도 · 영역** — 크기 ×10 에 매개변수 그대로 · **f0 (일정 끌림 힘) 은 그대로인데 접촉력은 크기² 로 커져** 점착 대 하중 비가 실물의 ≈ 1/100 [우리 판단] — 응집이 안 나온 이유 후보.  NCM E 절반 · LPSCl E 21 GPa (연화 없음).  **본문 0.5 × 0.5 mm 판 · 입자 부피 0.087 mm³ (→ 두께 0.48 mm) ↔ 그림 4 표기 1 × 1 × 2 mm (침대 높이 ≈ 0.9 mm [판독] · NCM 구 ≈ 70 µm)** — 본문 수치끼리는 맞고 그림 4 는 그것과 안 맞는다 (어느 쪽이 실제 계산인지 [미확인]) [우리 산술].  이완 · 언로딩 · 시드 [미확인].
7. **τ\* 를 재현할 수 없다** — α 의 단위 · l0 정의 · 경로마다 평균하는 방식이 없다.  τ\* − τ_geo 의 조성 비 (1 : 1.31 : 1.23 : 1.36) 가 그림 12 평균 N 의 비 (1 : 1.14 : 1.15 : 1.28) 와 다르고, α 를 m 로 읽으면 필요한 l0 가 0.30–0.34 mm 로 조성마다 다르며 침대 두께 0.48 mm 와도 다르다 [우리 산술].  α 는 한 점 맞춤 자유 매개변수 — 0 wt% 일치는 검증 아님.
8. **본문 ↔ 그림 · 식 오기**: *"simulated tortuosity (black plots)"* ↔ 범례 Sim = 빨강 · *"all paths included more than 25 particles"* ↔ 그림 12 (≈ 19 % 는 N < 25) · *"30 vol% milled LPSCl"* (p.7) ↔ 나머지는 wt% · 식 (2) σ = h/(πR_c r) (R_c² 의 제곱 빠짐) · 그림 13 범례 *k* ↔ 본문 α · p.4 §2.2.3 *"reduces to \Dijkstra's algorithm"* 조판 잔재.
9. **대표 임피던스 (그림 3) 가 그림 8a 와 안 맞는다** — r_ion/r_e ≈ 2.3 ↔ σ_e/σ_ion ≈ 17.8 (0 wt%) — 같은 펠릿이면 같아야 한다 [우리 산술].
10. **σ_e ≈ 1 × 10⁻² S/cm (무탄소 70 : 30) 는 다른 무탄소 카드보다 20–40 배 높다** (schlautmann2023 0.26–0.41 · minnmann2021 0.56 mS/cm) — 원인 미상 → **절대 σ_e 인용 금지**, 경향 (거의 평평) 만.
11. **펠릿 형상** — 8 g · ⌀16 mm 면 두께 ≈ 16 mm [우리 산술 · 8 g 전량 투입 가정] (높이/지름 ≈ 1) → 금형 벽 마찰로 축 방향 밀도 구배 가능 · 압력 100–400 MPa 라 했지만 결과는 400 MPa 만.
12. **NCM D50 불일치** — 본문 11 µm ↔ 실측 CDF 8.66 µm (표 4 86.0/10 = 8.60).
13. **SEM = 펠릿 표면** (단면 아님) · (a) 의 회색 판상 LPSCl ≈ 25–40 µm 는 측정 PSD 최대 (12.2 µm) 보다 커서 **눌린 응집체**일 가능성 [판독 · 추정] → "큰 입자 우회로" 의 실물이 1차 입자가 아니라 응집체일 수 있다.
14. **전지 성능 없음** — 용량 · 율 · 사이클 없이 *"design guideline"* 으로 확장 (p.8) 은 외삽.
15. **데이터 · 코드 비공개** (요청 시) · SI 없음 · DEM 시드 · 경로 표본 정의 미기재.

## 11. 적용 인사이트
- ① **p1 한정어 문장 (제안)**: *"단분산 대리 = D50 하나.  같은 LPSCl 복합양극에서 PSD 폭 (거친 꼬리) 은 DEM 기하 τ 엔 거의 영향이 없지만 (1.14–1.17), 경로당 직렬 입자 수 (20.5 → 26.3) 와 실측 σ_ion (≈ 27 배, 밀링 · 응집 교란) 에는 크게 나타났다 (Yano 2026)."*
- ② **p4 의 정당화 재료**: 기하 τ 와 수송 τ 를 짝으로 보여 주는 이유를 외부 사례로 — 그들 DEM 에서 기하 τ 는 평평한데 수송은 움직인다.  우리 *협착 ↔ bulk 소산 몫* 은 그들의 *αN* 항을 **물리 (Holm · 접촉 면적) 로 푼 판**이라고 설명할 수 있다.
- ③ **p5 목록 보강**: 밀링 LPSCl 펠릿 σ 비 **2.78** (습식 · 20 h) — 덱의 2.217 (1 ↔ 3 µm) 보다 크다.  이 사례는 구조 f 도 함께 나빠져 (÷ 9.8) *"미립화 = 구조 이득"* 이 **응집을 막지 못하면 성립 안 함**을 보여 준다.
- ④ **우리 망으로 바로 할 수 있는 시험 [제안 · 새 런 필요 여부 = 1저자]**: 같은 D50 에서 PSD 폭만 다른 침대 (예: 단분산 vs 2–5 구간 이산) 를 만들어 **경로당 SE–SE 접촉 수 · τ_geo · tau2 · 협착 몫**을 비교 — 그들의 N 분포 (그림 12) 와 같은 그림이 나온다.  기존 도구: `calc_tortuosity_all` (기하) · `scripts/network_conductivity.py` · `scripts/tau_flux.py` (수송).
- ⑤ **연화 없는 DEM 의 밀도** (EEPA · E 21 GPa · 400 MPa → 기공 27–28 %) 는 frame [2] 의 *"연화 대신 실물 E 를 쓰면 성기다"* 쪽 외부 사례 하나 (단 실험 기준값 자체가 진밀도 규칙에 흔들림 · §10-2).
- ⑥ **분말 쪽 교훈**: PSD 는 D10 · D50 · D90 + 응집 상태 (SEM) 를 같이 적어야 한다 — 이 논문의 "넓은 / 좁은" 의 실체는 D90 (거친 꼬리) 이다.

## 12. 인용 가능 문장 (영문 초안)
- *"In NCM622/Li₆PS₅Cl (70:30 wt%) composites, replacing the as-received electrolyte (D50 ≈ 1.8 µm, broad distribution) by a wet-milled one (D50 ≈ 1.3 µm, narrow distribution) lowered the effective ionic conductivity by about one order of magnitude or more, while DEM shortest-path geometric tortuosity remained ≈ 1.1–1.2; the experimental effect is confounded by milling-induced conductivity loss and agglomeration [Yano 2026]."* (⚠ 수치는 그림 판독 — 각주)
- *"A DEM study found that the number of electrolyte particles along the shortest ionic path, rather than the geometric path length, changed with the electrolyte size distribution, and a per-particle path cost reproduced part of the experimental tortuosity trend [Yano 2026]."*
- 국문: *"같은 LPSCl 이라도 PSD 의 거친 꼬리를 없애면 (밀링) DEM 기하 tortuosity 는 거의 그대로인데 경로당 입자 수가 늘고 실측 이온 전도도는 크게 떨어진다 — 기하 τ 와 수송 τ 는 다른 정보다 (Yano 2026)."*

## 13. 기법 용어 미니사전
- **EEPA (Edinburgh Elasto-Plastic Adhesion)**: DEM 접촉 법칙 — 하중 · 제하 강성을 달리해 (소성비 λp) 영구 겹침을 남기고, 끌림 힘 (일정 f0 + 표면에너지 항) 으로 점착을 넣는다.  입자 **형상**은 변하지 않는다.
- **소성비 λp = 1 − k₁/k₂**: 하중 강성 k₁ 대 제하 강성 k₂ — 0 이면 완전 탄성.
- **JKR 점착력**: 탄성 구 두 개의 표면에너지에 의한 떼어내는 힘 (∝ γR\*).
- **A\* 탐색**: 목표까지의 추정 비용 (휴리스틱) 을 더해 Dijkstra 를 빠르게 한 최단 경로 알고리즘 — 휴리스틱이 0 이면 Dijkstra 와 같다.
- **τ_geo = l/l0 (기하 tortuosity)**: 최단 경로 길이 / 두께.  *수송 τ 아님.*
- **τ_eff (이 논문)**: √(φσ₀/σ_eff) = 우리 *tau* (√ 값) — 그 제곱이 우리 *tau2 (수송 tortuosity)* (φ 기준 다름).
- **τ\* = (l + αN)/l0**: 경로 길이에 *입자당 상수 비용 × 입자 수* 를 더한 수정 τ — α 는 입계 저항 대리 (1 점 맞춤).
- **fast-track 효과**: 넓은 PSD 의 큰 입자가 경로의 입계 수를 줄여 이온이 빨리 지나가는 길이 된다는 저자의 해석.
- **차단전극 (강철 펀치) 혼합 전도체 EIS**: 고주파 반원 끝 = 전자 ∥ 이온 병렬 저항 (r₂), 저주파 끝 = 전자 저항만 (r₃, 이온은 막힘).
- **Lumisizer**: 원심 침강 · 광투과로 입도 분포를 재는 장비.
- **상대밀도 ρ_rel**: 겉보기 밀도 / 진밀도.  혼합물 진밀도는 **부피 가중** (질량 분율 / 밀도의 조화평균) 이 맞다.

## 14. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로)

| 번호 | 서지 (원문 목록) | 왜 · 정본 카드 |
|---|---|---|
| 25 | S. Ohsaki, T. Yano, A. Hatada, H. Nakamura, S. Watano, Size control of sulfide-based solid electrolyte particles through liquid-phase synthesis, Powder Technol. 387 (2021) 415–420 | 서브 µm SE 크기 제어 (밀링 없이) — 카드 없음 |
| 26 | F. Frankenberg, … A. Kwade, Tailoring composite microstructure through milling for dry-processed sulfide-based solid-state battery cathodes, Small (2025) | 정본 `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` |
| 27 | M. Calpa, N.C. Rosero-Navarro, A. Miura, K. Tadanaga, … small-sized Li7P3S11 solid electrolyte prepared by liquid phase …, Electrochim. Acta 296 (2019) 473–480 | 지도 §6 순위 7 (밀링 없는 미립화) |
| 29 | E. Schlautmann, … W.G. Zeier, Impact of the solid electrolyte particle size distribution in sulfide-based solid-state battery composites, Adv. Energy Mater. 13 (2023) | 정본 `schlautmann2023_se_particle_size_composite_transport` |
| 30 | T. Shi, Q. Tu, Y. Tian, Y. Xiao, L.J. Miara, O. Kononova, G. Ceder, High active material loading in all-solid-state battery electrode via particle size optimization, Adv. Energy Mater. 10 (2020) | 정본 `shi2019_high_am_loading_particle_size_assb` |
| 31 | J. Park, … Y.M. Lee, Digital twin-driven all-solid-state battery …, Adv. Energy Mater. 10 (2020) | 정본 `park2020_digitaltwin_assb_foundational` |
| 32 | A.M. Bazzoun, … K.P. Birke, Parameter sensitivity analysis and calibration of a discrete element model …, Electrochim. Acta 535 (2025) | 정본 `bazzoun2025_dem_parameter_sensitivity_assb_cathode` |
| 39 | F. Frankenberg, M. Kissel, C.F. Burmeister, M. Lippke, J. Janek, A. Kwade, … stressing conditions in a high-intensity mixer, Powder Technol. 435 (2024) | 정본 `frankenberg2024_dem_high_intensity_mixer_assb` · 복합체 EIS 방법의 인용처 |
| 40 | M. So, G. Inoue, K. Park, K. Nunoshita, S. Ishikawa, Y. Tsuge, Simulation of the compaction of an all-solid-state battery cathode with coated particles using the discrete element method, J. Power Sources 530 (2022) | 정본 `so2022_dem_compaction_coated_particles_assb` |
| 41 | C. Sangrós Giménez, L. Helmers, C. Schilde, A. Diener, A. Kwade, Modeling the electrical conductive paths within all-solid-state battery electrodes, Chem. Eng. Technol. 43 (2020) 819–829 | 정본 `sangros2020_dem_electrical_conductive_paths_assb` (DEM + 최단 경로 선례) |
| 42 | P. Minnmann, L. Quillman, S. Burkhardt, F.H. Richter, J. Janek, … charge transport bottlenecks in composite cathodes …, J. Electrochem. Soc. 168 (2021) 040537 | 정본 `minnmann2021_jes_charge_transport_bottlenecks` (식 (3) 출처 · 밀링 절차) |
| 45 | A. Bielefeld, D.A. Weber, J. Janek, Modeling effective ionic conductivity and binder influence in composite cathodes …, ACS Appl. Mater. Interfaces 12 (2020) 12821–12833 | 정본 `bielefeld2020_effective_ionic_conductivity_binder` |
| 46 | S.C. Thakur, J.P. Morrissey, J. Sun, J.F. Chen, J.Y. Ooi, Micromechanical analysis of cohesive granular materials using the discrete element method with an adhesive elasto-plastic contact model, Granular Matter 16 (2014) 383–400 | 정본 `thakur2014_eepa_adhesive_elastoplastic_dem` |
| 48 | T. Yano, S. Ohsaki, H. Nakamura, S. Watano, Compression properties of bimodal powders with different plasticities …, Adv. Powder Technol. 34 (2023) 104245 | 같은 저자 이원 압축 DEM — 카드 없음 |
| 51 | T. Yano, S. Ohsaki, H. Nakamura, S. Watano, Numerical analysis of compression properties of the binary mixture of powder with different particle plasticities, J. Soc. Powder Technol. Japan 61 (2024) 144–153 | 등가 소성비 0.619 출처 — 카드 없음 |
| 53 | C. Sangrós Giménez, A. Pistoor, C. Willuhn, C. Schilde, A. Kwade, Modelling the electrical conductivity of lithium-ion battery electrodes via a bonded-particle approach, Adv. Powder Technol. 36 (2025) | 접촉 저항 지배 — 카드 없음 |
| 56 | M. Kissel, … J. Janek, Quantifying the impact of cathode composite mixing quality on active mass utilization and reproducibility of solid-state battery cells, Adv. Energy Mater. 15 (2025) 2405405 | 혼합 품질 ↔ 이용률 — 카드 없음 (`kissel2026_…` 은 다른 논문) |

## 🔗 관련 카드
- 같은 축 (SE 입도 · 복합양극): `schlautmann2023_se_particle_size_composite_transport` · `minnmann2021_jes_charge_transport_bottlenecks` · `shi2019_high_am_loading_particle_size_assb` · `bazzoun2025_dem_parameter_sensitivity_assb_cathode` · `bazzoun2026_dem_fem_rnm_ionic` · `frankenberg2025_milling_dry_processed_sulfide_cathode_microstructure` · `cronau2022_wet_milling_particle_size_ionic_conductivity` · 반례 짝 `yadav2021_lpscl_sieved_psd_impedance_tortuosity` (같은 날 digest).
- DEM · 최단 경로 · 응집: `sangros2020_dem_electrical_conductive_paths_assb` · `so2022_dem_compaction_coated_particles_assb` · `otani2025_dem_se_dispersion_aggregation_compression` · `thakur2014_eepa_adhesive_elastoplastic_dem` · `frankenberg2024_dem_high_intensity_mixer_assb`.
- 같은 그룹 (오사카): `nakamura2020_dry_coating_ncm_li3ps4_core_shell` · `kawaguchi2023_doe_electrode_fabrication_dry_coated_ncm_lps`.
- 순수 SE 입도: `faka2026_particle_size_consolidation_strain_lpscl`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

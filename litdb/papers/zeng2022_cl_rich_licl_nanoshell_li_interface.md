<!-- digest 표준 양식 (paper-level STANDALONE). 깊이 기준 = papers/zuo2022_chlorination_cathode_interface.md.
     2026-11-09 작성 (litdb-curator): 본문 13 pp + SI 20 pp + Source Data xlsx (35 시트 중 Figure1c · 1e · 2f · 3a · 8d 만 열었다).
     크롭 29장 (본문 10 + SI 16 + 표 3) 중 `Fig. 1` `Fig. 3` `Fig. 9` `Fig. 10` `Fig. S10` `Fig. S13` 6장을 실제로 보았다.
     자동 크롭이 `Fig. 1`(위쪽 잘림) · `Fig. 9`(패널 a–c 통째로 빠짐) 를 잘못 잘랐고 `Fig. 10` 은 놓쳤다 → 손으로 다시 잘라 figures.json 에 manual_crop 사유를 달았다.
     우리 값은 db/properties/canonical_registry.json · citation_hazards.json 규율 안에서 방향 · 모델 구성만 적었다 (수송 절대값 · 계간 순위 없음). -->

# Promoting favorable interfacial properties in lithium-based batteries using chlorine-rich sulfide inorganic solid-state electrolytes — Zeng et al. (*Nat. Commun.* **13**, 1909 (2022))

> slug `zeng2022_cl_rich_licl_nanoshell_li_interface` · DOI `10.1038/s41467-022-29596-8` · type `exp (계산 0 — DFT · AIMD · MLIP · grand-potential 없음)` · PDF 업로드 `038bce09-116._Promoting_favorable…pdf` (본문 13 pp) + `3856744e-116._Sup_Promoting_favorable…pdf` (SI 20 pp: Supplementary Fig. 1–16 · Table 1–3) + `4b067d6d-116._Sup_…xlsx` (Source Data 35 시트) · digested `2026-11-09` · status ✅
> elements: Li, P, S, Cl
> methods: XPS, Raman

> **저자**: **Dewu Zeng**¹ · Jingming Yao¹ · **Long Zhang**¹\* (교신 · `lzhang@ysu.edu.cn`) · Ruonan Xu¹ · Shaojie Wang² · Xinlin Yan³ · Chuang Yu⁴ · Lin Wang² — ¹ Clean Nano Energy Center, State Key Lab of Metastable Materials Science and Technology, **Yanshan Univ.** (Qinhuangdao) · ² CHiPS, Yanshan Univ. · ³ Institute of Solid State Physics, **TU Wien** · ⁴ **HUST** (Wuhan). 접수 2021-10-30 · 수리 2022-03-24 · Open Access. **[외부]**.
> 🔗 **Kang 2026 (site-specific customized SE · `kang2026_site_specific_customized_se_dendrite_tolerant_li_metal`) 의 참고문헌 [39–41] 묶음으로 인용됨 (사용자 지정 2026-11-09 · 이 편의 정확한 번호는 확인 못 함)** — 인용 문장 8: *"Cl⁻ 4d 치환 → 국소 음이온 전하밀도↓ → Li⁺ cage 연결↑ → 전도도↑"*. 세 편 중 **유일하게 x = 1.6 (= Kang 의 LPSC₁.₆ · 우리 modelc 명목 조성) 을 잰 편**인데, 그 네 고리 중 **④ (전도도) 만 직접** 보이고 ① 은 서론 인용 [20–22] 뿐이다 — 오히려 *"Cl-rich 시료의 Cl 다수는 격자가 아니라 입자 표면 LiCl 나노껍질"* 이라는 **①의 전제를 흔드는 관측**을 낸다. 판정 · 근거: **§12**.
> 🔗 리뷰 재인용으로 먼저 들어와 있던 편: `he2023_halogen_chemistry_solid_electrolytes.md` §11b (본문-ref 185) — 이 digest 가 그 원전이다.

---

## 0. 이 digest 를 읽는 법 — 먼저 읽을 것 다섯

1. **계산이 0 이다.** 결론의 기전 (LiCl 나노껍질 → Cl 이동 → LiCl 계면층 → 자기제한 · 덴드라이트 억제) 은 전부 **실험 관측 + 저자 추론**이다. σ 상승의 원인 (*"X⁻/S²⁻ 구조 무질서와 Li 공공 농도 증가"*, p.10) 은 **재지 않고 주장**한다.
2. **조성 대응**: `Cl-10` = Li₆PS₅Cl = 우리 **comp1 명목** · `Cl-16` = Li₅.₄PS₄.₄Cl₁.₆ = 우리 **modelc 명목** · `Cl-06` Li₆.₄PS₅.₄Cl₀.₆ · `Cl-13` Li₅.₇PS₄.₇Cl₁.₃ · `Cl-145` Li₅.₅₅PS₄.₅₅Cl₁.₄₅. ⚠ **명목 조성 ≠ 격자 조성** — x ≥ 1.3 은 LiCl 이 따로 있다 (Rietveld 2.7 / 3.2 / 4.4 vol%) · 이 논문의 핵심 주장 자체가 "Cl-rich 의 Cl 일부는 격자 밖" 이다.
3. **두 축이 반대로 간다**: Li 와의 **화학 안정성 (계면저항 증가 속도)** 은 Cl 이 많을수록 **단조 개선** (Cl-16 최고) · **덴드라이트 내성 (CCD · 0.5 mA cm⁻² 사이클)** 은 **x = 1.3 에서 최대, x = 1.6 에서 최저** (`Fig. 3a`). σ 가 가장 높은 Cl-16 이 CCD 가 가장 낮다.
4. **'LiCl' 은 EDS 로 Li 를 못 본 채 붙인 이름이다** (저자 자인, p.9: *"Because the Li element cannot be detected … the Cl-contained framework is considered to be LiCl"*). 나노껍질 · 55 µm 계면층 모두 "Cl 이 S · P 없이 보이는 곳" 이다 (§10-②).
5. **본 그림 (2026-11-09)**: `Fig. 1` (재크롭) · `Fig. 3` · `Fig. 9` (재크롭) · `Fig. 10` (손 크롭) · `Fig. S10` · `Fig. S13` — **6장**. 안 본 것: `Fig. 2` · `Fig. 4`–`Fig. 8` · `Fig. S1`–`Fig. S9` · `Fig. S11`·`Fig. S12`·`Fig. S14`–`Fig. S16` (본문 텍스트 · Source Data 로 대신) · 표 3장 (PDF 텍스트로 읽음). 그림에서만 읽은 값은 **`figure-read ≈`**, 우리가 계산한 값은 *우리 산수*.

---

## 1. 한 줄 요약

Li₇₋ₓPS₆₋ₓClₓ (x = 0.6–1.6) 다섯 조성을 같은 공정 (볼밀 + 12 h 소성 + **2 °C min⁻¹ 서냉**) 으로 만들어 Li 금속 계면을 비교했다 — Cl 이 늘수록 σ(24 °C) **1.6 → 8.8 mS cm⁻¹** · σ_e **4.2×10⁻¹¹ → 1.3×10⁻¹² S cm⁻¹** · Li|SE 계면저항 증가가 느려지지만 (600 h: Cl-06 209 → 9093 Ω · Cl-16 19 → 256 Ω), **CCD 는 x = 1.3 에서 최대 (1.04 mA cm⁻²) · x = 1.6 에서 최저 (0.56)**. 저자 해석: Cl-rich 시료는 **입자 표면에 LiCl 나노껍질 (Cl-13 ≈20 nm · Cl-16 ≈50 nm)** 이 서로 이어진 골격을 만들고, 사이클 중 그 Cl 이 Li 쪽으로 옮겨 **조밀 · 균일한 'LiCl 지배' 계면층 (Cl-13 55 ± 6 µm)** 을 다시 짓는다 — 껍질이 적당히 얇은 x = 1.3 이 덴드라이트를 가장 잘 견디고, 너무 두꺼운 x = 1.6 은 argyrodite 핵을 고립시켜 Li 필라멘트를 못 삼킨다. 서냉 없이 바로 급랭하면 껍질이 안 생긴다 (`Fig. S13`).

⚠ 결론부 일반화 *"a majority [of Cl] exists on the grain surfaces … while a minority on the argyrodite lattice"* (p.11) 는 **자기 Rietveld LiCl 분율 (Cl-16 4.4(5) vol% ≈ 0.3 LiCl/f.u. = 명목 Cl 의 ≈1/5 · *우리 산수*)** 과 차수가 안 맞는다 (§10-①).

---

## 2. 메타 / 동기 / 질문

| 항목 | 내용 |
|---|---|
| 조성 | Li₇₋ₓPS₆₋ₓClₓ x = 0.6 · 1.0 · 1.3 · 1.45 · 1.6 (Cl-06 … Cl-16) |
| 던지는 질문 | Cl 함량 (chlorinity) 이 **Li|argyrodite 계면** — 계면상 조성 · 미세구조 · 덴드라이트 억제 — 을 어떻게 바꾸나. 서론: "Cl-rich (a = 1.5) 는 Li 에 전기화학적으로 안정하지만 덴드라이트 침투는 못 막는다 [23 = Gil-González 2022]" 를 출발점으로 삼는다 |
| 서론의 구조 서술 (인용) | *"a higher chlorinity leads to stronger Cl⁻/S²⁻ site disorders, and moreover, a higher occupancy of Cl atoms at the 4d site … thereby achieving a faster ion transport with an ionic conductivity ~10 mS/cm [20–22]"* (p.2) — [20] Patel 2021 *Chem. Mater.* (Li₆₋ₓPS₅₋ₓClBrₓ) · [21] **Gautam 2021 *ACS Appl. Energy Mater.*** (Li₇₋ₓPS₆₋ₓClₓ 의 Li 분포) · [22] **de Klerk 2016 *Chem. Mater.*** (참고문헌 쪽에 번호가 일부 안 박혀 거꾸로 세어 정했다) |
| 핵심 장비 | cryo-STEM-HAADF/EDS (−170 °C · Themis Z 300 kV) · SEM-EDS 단면 · time-resolved / in situ EIS · XPS 반정량 · in situ Raman |
| 셀 | In\|SE\|In (σ) · Pt\|SE\|Pt (σ_e) · Li\|SE\|Li (CCD · 사이클 · 시간분해 EIS) · Li\|SE\|LNO@NCM622 · Li-In\|SE\|LNO@NCM811 (양극 촉매질은 **상용 LSPSC = Li₉.₅₄Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃** — argyrodite 는 분리막에만) |
| 압력 | 펠릿 250 MPa 냉간압축 · 측정 중 외압 ≈3 MPa (대칭셀) · 풀셀 6 MPa |
| 온도 | 24 °C (σ) · 24 ± 4 °C (셀 시험 — 실온 변동이 전압 요동으로 보인다고 저자 자인, p.5) |

---

## 3. 핵심 수치 총정리 ★

### 3a. 벌크 (`Fig. 1`, `Table S1`, Source Data `Figure1c`)

| 물성 | Cl-06 | Cl-10 | Cl-13 | Cl-145 | Cl-16 | 조건 / 출처 |
|---|---|---|---|---|---|---|
| σ_ion (mS cm⁻¹) | **1.6** | **3.6** | **5.3** | **6.1** | **8.8** | 24 °C · In\|SE\|In · **총 σ** (Nyquist 와 x 축 교점의 국소 최소 저항 — 입계/입내 분리 안 함, p.3) · 측정오차 3 % 이내 (방법) |
| σ_e (S cm⁻¹) | 4.2×10⁻¹¹ | 3.75×10⁻¹¹ | 1.04×10⁻¹¹ | — | 1.3×10⁻¹² | Pt\|SE\|Pt DC 5 mV (`Table S1`) |
| a (Å) | 9.890(1) | 9.841(1) | 9.817(1) | 9.805(1) | 9.788(1) | Rietveld (`Table S1`) — "선형 감소" (p.2) |
| LiCl (vol%) | 0 | 0 | 2.7(2) | 3.2(5) | 4.4(5) | Rietveld (`Table S1`) · x = 0.6 엔 Li₂S 흔적 |
| LiCl 껍질 두께 | 없음 | — | **≈20 nm** | — | **≈50 nm** | cryo-STEM-EDS 선 스캔 (p.9 · `Fig. 9d` · `Fig. S10`) |
| 결정성 | 결정 | 결정 | 약한 비정질 헤일로 | — | 약한 비정질 헤일로 | SAED (`Fig. 1d`) — *"against the expectation for some not yet known reasons"* |
| 분말 색 | 어두움 | — | 밝음 | — | 밝음 | `Fig. 1b` |

- `Fig. 1e` (Source Data `Figure1e`): Nyquist 첫 점 `≈` x = 0.6 **104.8 Ω** · 1.0 46.1 · 1.3 33.9 · 1.45 28.0 · 1.6 **17.6 Ω**. ⚠ Source Data 머리글은 "Zre (ohms)" 인데 값은 **kΩ** 로 들어 있다 (0.01761 → 그림 ≈17.6 Ω). σ 와 맞춰 보면 기하 인자 L/A 가 0.155–0.180 cm⁻¹ 로 조성 사이에 ±8 % 안이다 (*우리 산수* — 펠릿 두께 미기재).
- 격자 수축의 원인은 **"작은 Cl 반경 · Cl⁻/S²⁻ 자리 무질서 증가 · Li 공공 생성의 합으로 여겨진다"** (p.2 *"is considered the combining effects of …"*) — **4a/4d 점유 정련은 없다.**

### 3b. Li 계면 (`Fig. 2`–`Fig. 5`, `Table S2`·`Table S3`, Source Data `Figure2f`·`Figure3a`)

| 물성 | Cl-06 | Cl-10 | Cl-13 | Cl-16 | 조건 / 출처 |
|---|---|---|---|---|---|
| R_int 정치 (Ω) 0 → 600 h | 209 → **9093** | 61 → 568 | 50 → 486 | **19 → 256** | Li\|SE\|Li 휴지 · 100 h 마다 EIS · Rb(Rgb-CPEgb)(Rint-CPEint)W 적합 (`Table S2`) |
| R_int 사이클 (Ω) 0 → 400회 | 258 → 623 (200회) | 63 → 465 | 40 → **178** | 17 → **49** | 0.25 mA cm⁻² in situ EIS (`Table S3`) |
| **CCD (mA cm⁻²)** 3 배치 | 0.60 · 0.70 · 0.75 → **0.68 ± 0.062** | 0.93 · 0.95 · 0.98 → **0.95 ± 0.021** | 0.98 · 1.05 · 1.085 → **1.038 ± 0.043** | 0.525 · 0.56 · 0.595 → **0.56 ± 0.028** | 24 ± 4 °C · 시작 · 단계 35 µA cm⁻² (단계 시간 미기재) · Source Data `Figure3a` |
| 0.25 mA cm⁻² 장기 | 270회 단락 | 400회 경미 열화 | 400회 경미 열화 | 400회 거의 평탄 | `Fig. 3b–e` (반주기 0.5 h — `figure-read` 삽입 그림 주기 1 h) |
| 0.5 mA cm⁻² | 30회 안에 단락 | 30회 안에 단락 | **1000회 이상 단락 없음** | 30회 안에 단락 | `Fig. 5` |

- ⚠ 본문 p.3 *"those of Cl-13 and Cl-16 increase slowly from 50 and 19 Ω … to 486 and 256 Ω at **6000 h**"* — 표 · 그림은 **600 h** 다 (오기).
- ⚠ 본문 p.4 *"a high chlorinity especially for **Cl > 1.6** is favorable"* — x > 1.6 시료는 없다 (오기로 보임).

### 3c. 계면상 · 셀 (`Fig. 6`–`Fig. 10`, Source Data `Figure8d`)

| 항목 | Cl-06 | Cl-13 | 출처 |
|---|---|---|---|
| XPS P 2p (200회 뒤, at%) | PS₄³⁻ **48.42** · 환원 P 47.12 · Li₃P 4.46 | PS₄³⁻ **80.57** · 환원 P 17.09 · Li₃P 2.34 | Source Data `Figure8d` (본문 "81 at% vs 48 at%", p.7) |
| XPS S 2p (200회 뒤, at%) | PS₄³⁻ 54.69 · **Li₂Sₙ 5.46** · Li₂S 39.85 | PS₄³⁻ 72.36 · Li₂S 27.64 (Li₂Sₙ 없음) | 같은 시트 |
| SEM-EDS 계면층 | 거칠고 불균일 · 두께 수 – 50 µm · P₂S₅ 응집 > 10 µm | **매끈 · 균일 'LiCl 지배' 층 55 ± 6 µm** | `Fig. 9a–c` (Cl-06 200회 · Cl-13 400회) |
| in situ Raman (Li\|SE 단면, 0.1 mA cm⁻² 충전) | 3.6 V 부터 198 cm⁻¹ (P₂S₅) · 486 cm⁻¹ (Li₂Sₙ) 출현 · PS₄³⁻ 421 cm⁻¹ 급감 | 분해 봉우리 없음 · PS₄³⁻ 소폭 감소 | `Fig. 10c,d` |
| Li\|SE\|LNO@NCM622 (0.1 mA cm⁻²) | ICE 55 % · 용량 급감 · CE 80–100 % 요동 | ICE **68 %** · ≈137 mAh g⁻¹ 유지 | `Fig. 6` |
| Li-In\|SE\|LNO@NCM811 (0.5 mA cm⁻², 1000회) | ≈123 mAh g⁻¹ @50회 · ICE ≈66 % | ≈148 mAh g⁻¹ @50회 · ICE ≈66 % | `Fig. 7` · Cl-16 ≈145 (`Fig. S6`) |

---

## 4. 재료 · 방법 (계산 없음)

### 4a. 합성
- Li₂S (aladdin 99.9 %) · LiCl (aladdin 99.9 %) · P₂S₅ (Alfa Aesar 99.9 %) — 총 2 g · 마노 유발 15 분 → Fritsch P7 premium · WC 볼 ⌀10 mm · **100 rpm 1 h 예비 + 550 rpm 10 h** → 펠릿 · 석영관 진공 봉입 · **450–550 °C 12 h** (승온 5 °C min⁻¹) → **2 °C min⁻¹ 로 350 °C 까지 서냉 → 자연 냉각** → 유발로 분쇄.
- ⚠ 조성별 소성 온도가 "450–550 °C" 범위로만 적혀 있다 (어느 x 가 몇 °C 인지 없음).
- 냉각 대조 (`Fig. S13`, Cl-16): (a) 400 °C 까지 서냉 후 얼음물 급랭 → 껍질 **있음** (b) 바로 얼음물 급랭 → 껍질 **없음** ⇒ *"a slow cooling process at the high temperature regions is a crucial factor"* (p.10).

### 4b. 분석
- XRD Rigaku D/MAX-2500/PC (Cu Kα · 10–70° · **3° min⁻¹**) · 폴리이미드 막 (10–20° 헤일로) · Rietveld (프로그램 미기재) → a · LiCl 분율.
- cryo-STEM: Themis Z 300 kV · 단색기 · Cs 보정 · Super-X EDS · HAADF 41–200 mrad · **−170 °C · 용매 없이 Ar 퍼지 그리드** · ETEM Titan G2 (SAED).
- SEM-EDS Helios G4 CX · XPS Thermo K-Alpha+ · Raman Renishaw inVia 532 nm (자작 셀 · 석영창 ⌀10 mm · Li\|SE 단면 고정점).
- EIS Princeton P4000 0.1 Hz–1 MHz · σ_e DC 분극 Pt\|SE\|Pt 5 mV · 패러데이 상자.
- CCD 오차막대 = 3 배치 표준편차 (모집단 SD 식, n = 3).

### 4c. 이론 · 계산
- **없다.** 인용으로만: LiCl 띠틈 6.3 eV · Li₆PS₅Cl 2.2 eV [59,60] · LiCl 체적 · 전단 탄성률 31 · 20 GPa [59] (p.10–11) · 공간전하층 [56–58] (추측이라고 명시, p.10).

---

## 5. 결과 — 절별 상세 (그림 실독 포함)

### 5.1 구조 · σ (`Fig. 1`)
- `Fig. 1a`: 다섯 조성 모두 F-43m argyrodite 주상. x = 0.6 에 Li₂S (■ 22.3° 부근), x ≥ 1.3 에 LiCl (▼ 34.8° 부근) 흔적 (`figure-read`). 52–53° 확대창에서 봉우리가 x 와 함께 고각 이동 (보라 점선).
- `Fig. 1c` (`figure-read` = Source Data 값): σ 는 x = 0.6–1.45 에서 거의 직선 (1.6 → 6.1) 이다가 x = 1.6 에서 **꺾여 오른다** (8.8) — 본문 *"sharper increase"* (p.3). 같은 구간에 LiCl 분율은 3.2 → 4.4 vol% 로 는다.
- `Fig. 1d`: Cl-06 [001] 점 패턴 · Cl-13 [66\bar1] 줄무늬 · Cl-16 [001] 점 패턴 — 저자는 Cl-13 · Cl-16 의 약한 헤일로를 비정질 소량으로 읽는다.

### 5.2 Li 와의 화학 안정성 (`Fig. 2`, `Table S2`)
- 휴지 상태 600 h 동안 R_int 가 Cl-06 은 **43 배** (209 → 9093 Ω), Cl-16 은 **13 배** (19 → 256 Ω) (*우리 산수*). 시작값부터 Cl 이 많을수록 낮다.
- 결론: *"a suppressed chemical reactivity of argyrodite toward Li by increasing chlorinity"* (p.3) — **Cl 에 대해 단조**.

### 5.3 덴드라이트 · 장기 사이클 (`Fig. 3`, `Fig. 5`, `Fig. S4`)
- `Fig. 3a` (`figure-read` · Source Data 일치): 평균 CCD 0.68 → 0.95 → **1.04** → **0.56** — x = 1.3 정점, x = 1.6 이 x = 0.6 보다도 낮다. 배치 산포는 조성 차보다 작다 (Cl-16 SD 0.028).
- `Fig. 3b–e` (0.25 mA cm⁻²): Cl-06 은 ≈200 h 부터 분극이 커지다 270 h 단락 · Cl-10 · Cl-13 은 400 h 에 분극 ≈±0.05 V 로 경미 증가 · **Cl-16 은 400 h 평탄** (`figure-read`).
- `Fig. 5` (0.5 mA cm⁻²): **Cl-13 만 1000회 이상** — 나머지 셋은 30회 안에 단락. ⇒ 저자: *"Cl-13 with a moderate chlorinity possesses an (electro)chemical interface stability toward Li and a better Li dendrite suppression capability"* (p.5).

### 5.4 풀셀 (`Fig. 6`, `Fig. 7`, `Fig. S6`)
- Li\|SE\|LNO@NCM622: Cl-13 ICE 68 % > Cl-06 55 %. 첫 충전 3.7 V 아래 **산화 기울기**가 Cl-06 에서 더 완만 → 저자는 Li\|SE 쪽 계면상이 양극의 Li⁺ 저장 과정에까지 영향을 준다고 추측 (p.6).
- Li-In 음극으로 바꾸면 ICE 가 둘 다 ≈66 % 로 같아진다 → 3.7 V 아래 산화는 **Cl-06 의 Li 금속 불안정성 탓** (p.7).

### 5.5 계면상 (`Fig. 8`, `Fig. 9a–c`, `Fig. S7`–`Fig. S9`, `Fig. S15`)
- XPS (`Fig. 8`): Cl-06 은 Li₂S · 환원 P · Li₃P 에 **Li₂Sₙ (S–S)** 까지 · Cl-13 은 Li₂S 만 (Li₂Sₙ 없음). PS₄³⁻ 잔존 48 vs 81 at%.
- SEM-EDS (`Fig. 9a–c`, 실독): (a) 파단면 겹침 지도 — Cl-06 은 큰 응집 덩어리 (주황 · 파랑 섞임), Cl-13 은 고르게 흩어짐 (b) Cl-06 단면 — 노란 점선 사이 불규칙 띠 *"Rough and Inhomogeneous"* (c) Cl-13 단면 — 점선 사이 균일한 띠 *"Smooth and homogeneous LiCl layer, 55 ± 6 µm"* · 그 띠 안에서 **S · P 지도가 어둡고 Cl 만 있다**.
  - `figure-read`: 같은 Cl 지도 안에서 띠의 밝기는 위쪽 SE 영역과 **비슷하거나 더 어둡다** — 순수 LiCl 이면 Cl 질량분율이 SE 의 ≈5 배 (LiCl 83.6 wt% vs Li₅.₇PS₄.₇Cl₁.₃ 17.2 wt% · *우리 산수*) 라 훨씬 밝아야 한다 (§10-②).
- 사이클 뒤 XRD (`Fig. S15`, 본문): Cl-13 이 argyrodite 상을 더 많이 남긴다.

### 5.6 Cl 의 자리 — LiCl 나노껍질 (`Fig. 9d`, `Fig. S10`–`Fig. S13`)
- 본문 (p.9): *"unlike uniformly distributed P and S, the Cl atoms in Cl-16 (Fig. 9d) **primarily exist on the surface of each grain** by forming a nanoscale shell layer, which connects with each other and constructs a framework. **Only a part of Cl atoms locates inside the argyrodite lattice** to implement a successful doping."* · 껍질 두께 ≈50 nm (Cl-16) · ≈20 nm (Cl-13) · Cl-06 은 균일 → *"all Cl atoms are successfully substituted on the S sites"* (p.10).
- **그림 실독 (EDS 선 스캔 · `figure-read`)** — 입자 안쪽 평탄부의 Cl/S 계수비:

  | 시료 | Cl/S (안쪽) | 명목 Cl/S | 비 (측정/명목) | 테두리 Cl 봉우리 | 그림 |
  |---|---|---|---|---|---|
  | Cl-06 | ≈0.3/1.5 ≈ **0.2** | 0.11 | ≈1.8 | 없음 (함께 감소) | `Fig. S10a` |
  | Cl-13 | ≈2.4/5.3 ≈ **0.45** | 0.28 | ≈1.6 | 있음 (S 가 떨어진 뒤 ≈50 nm 더 남음) | `Fig. S10b` |
  | Cl-16 (서냉) | ≈0.65/1.9 ≈ **0.34** | 0.36 | **≈0.94** | 있음 (≈0.65 → ≈0.95 로 솟음 · 상자 "50 nm") | `Fig. 9d` |
  | Cl-16 (400 °C 서냉 후 급랭) | ≈0.65/2.7 ≈ 0.24 | 0.36 | ≈0.67 | 있음 | `Fig. S13a` |
  | Cl-16 (바로 급랭) | ≈0.75/1.9 ≈ 0.39 | 0.36 | ≈1.08 | 없음 | `Fig. S13b` |

  ⇒ 앞 두 시료로 EDS 감도비 (Cl/S 계수비 ÷ 원자비) 를 ≈1.6–1.8 로 잡으면 **Cl-13 의 안쪽 Cl 은 명목만큼 있다 (부족 없음)**, **서냉 Cl-16 은 기대의 ≈55 %** 다. 투영 (껍질 위 · 아래 두께 포함) · 계수 잡음 · k-인자 미보정의 정성 판독이지만, **"다수가 표면" 은 Cl-13 에 대해선 그림이 받치지 않고, Cl-16 에 대해선 '상당 부분 (≈절반 안팎)' 정도**로 읽힌다.
- `Fig. S11`: Cl-13 냉간압축 펠릿 SEM-EDS 7 영역 중 1 곳에만 ≈2 µm LiCl 덩어리 → 응집 LiCl 은 소량.
- `Fig. S14`: 400회 사이클 뒤 Cl-16 에서 껍질이 안 보인다 → *"Cl migration"* 추측의 근거 (p.10).

### 5.7 in situ Raman (`Fig. 10`, 손 크롭 · 실독)
- (c) Cl-06: PS₄³⁻ 421 cm⁻¹ 가 3.6 V 부터 약해지고, 점선 ≈486 cm⁻¹ (−S–S−, Li₂Sₙ) 가 `figure-read ≈`3.7–3.9 V 부터 뚜렷 (본문은 *"After charging to 3.6 V"* — 그림상 3.6 V 곡선에선 아직 흐리다) · 200 cm⁻¹ 부근 · 112–135 cm⁻¹ 어깨 (P₂S₅, > 4 V) (d) Cl-13: 4.3 V 까지 PS₄³⁻ 만, 세기 소폭 감소. 측정점은 Li\|SE 단면 (`Fig. 10b` 노란 점) — 충전 중 **음극 쪽** 계면이다.

---

## 6. 메커니즘 종합 (저자 서사 · p.10–11)

1. **서냉 + 고 Cl** → 소성 중 고용된 LiCl 이 냉각 때 입자 표면으로 *in situ* 석출 → 이어진 **LiCl 나노껍질 골격** (Cl-13 ≈20 nm · Cl-16 ≈50 nm).
2. 초기: 껍질이 argyrodite 와 Li 의 직접 반응을 막는다 (LiCl 6.3 eV 절연 · Li 에 안정).
3. 사이클: 전기장 아래 껍질의 Cl⁻ 가 Li 쪽으로 이동 → Li⁺ 와 다시 결합 → **조밀 · 균일 'LiCl 지배' 계면층** (자기제한 계면) → Li₂Sₙ · P₂S₅ 응집 억제.
4. 덴드라이트: LiCl 의 B/G 31/20 GPa · 전자절연 입계 → 침투 억제. 고전류 (0.5 mA cm⁻²) 에선 Li 가 계면층을 뚫는데, **Cl-13 은 얇은 껍질이 일부 소모돼 argyrodite 핵이 침투한 Li 와 반응해 끊어 낸다 (self-healing)** · **Cl-16 은 두꺼운 껍질이 핵을 고립시켜 Li 필라멘트를 못 삼킨다** · Cl-06 은 계면 열화 → 국소 전류 집중 → 단락.
5. σ: LiCl 은 이온전도가 나쁘지만 껍질이 수십 nm 로 얇고, *"we speculate that a space-charge layer exists between the argyrodite and the LiCl nanoshell"* (p.10) → σ 는 오히려 오른다 · 그 근본 원인은 *"X⁻/S²⁻ structural disorder and the Li vacancy concentration increase with increasing chlorinity"* (p.10 · **측정 없음**).

---

## 7. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`

> 이 논문은 계산이 0 이라 **값 대 값 비교는 없다**. 우리 쪽은 **모델 구성 · 방향**만 적는다. 수송 절대값 · comp1↔modelc 수송 순위는 원장상 인용 불가 (`canonical_registry.json` `md-ea-singleseed-anchor-v1` 의 `cross_composition_ranking` 금지 · comp1 provisional).

| 항목 | Zeng 2022 | 우리 | 판정 |
|---|---|---|---|
| **Cl 의 위치 (x = 1.6)** | 서냉 Cl-16: LiCl 4.4(5) vol% + ≈50 nm 껍질 · 안쪽 Cl 이 기대의 ≈55 % (`figure-read`) | modelc = **Cl 1.6 전량 격자** (62 원자 셀 · 4d = S²⁻ 2 + Cl⁻ 3 · `kb/results/lpscl_vs_lpscl16_v3_comparison.md` §II.2.5) | 🔴 **같은 물질이 아니다** — modelc 는 이 시료가 아니라 **'격자 고용 상한' 극한 모델** (he2023 digest §11b 와 같은 결론 · 이번에 원전으로 확인) |
| 격자 쪽 실제 조성 (*우리 산수*) | LiCl 4.4 vol% ≈ 0.32 LiCl/f.u. 를 단순 차감하면 격자 ≈ Li₅.₀₈PS₄.₄Cl₁.₂₈ (비정질 LiCl 이 더 있으면 Cl 더 적음) | modelc 명목 Li₅.₄PS₄.₄Cl₁.₆ | ⚠ 실험 'LPSC₁.₆' 의 격자 Cl 은 1.6 보다 작을 수 있다 — 계산 조성과 같은 줄에 놓을 때 명시 |
| σ 방향 | 8.8 vs 3.6 mS cm⁻¹ (Cl-16 vs Cl-10, 2.4×) | **인용 가능한 우리 순위 없음** (원장) | n/a — 문헌 방향만 기록 |
| σ_e | Cl 과 함께 **≈30 배 감소** (4.2×10⁻¹¹ → 1.3×10⁻¹²) | 띠틈 (fixed-occ nscf): comp1 · modelc 모두 같은 wide-gap 급 (차 +0.033 eV) | ✅ 해석: σ_e 30배는 **띠틈으로 설명 안 된다** → 결함 · 2차상 (LiCl 껍질) 지배로 읽는 게 맞다 (이 논문은 원인을 재지 않았다) |
| Li 쪽 0 V 산물 | Li₂S · Li₃P · 환원 P · LiCl (+ Cl-06 만 Li₂Sₙ · P₂S₅ 응집) | grand-potential 0 V: Li₂S + Li₃P + LiCl | ✅ 주산물 일치 · Li₂Sₙ · P₂S₅ 는 0 V 평형 산물이 아님 → 부분 환원 (동역학) |
| 덴드라이트 | CCD x = 1.3 최대 · x = 1.6 최저 | 대응 계산 없음 | n/a (§H 정직 목록) |

---

## 8. 적용 인사이트 ★

1. **Kang 8번 문장의 '①' 전제에 대한 반증 성격의 자료** (§12): 세 편 중 x = 1.6 을 잰 것은 이 편뿐인데, 이 편은 **4d 점유를 재지 않았고** 대신 "Cl-rich 의 Cl 일부 (저자 말로는 다수) 가 격자 밖 LiCl 껍질" 을 보였다. 그리고 그 비율은 **냉각 속도로 바뀐다** (`Fig. S13`). ⇒ "LPSC₁.₆ 에서 Cl⁻ 이 4d 의 S²⁻ 를 치환한다" 를 쓰려면 **그 시료의 열이력 + 점유 정련 (가능하면 중성자)** 이 같이 있어야 한다 — Kang 의 LPSC₁.₆ 는 열처리 온도 · 시간 · 냉각이 미기재이고 점유 정련도 없다.
2. **modelc 서술 규율 (원고 방어)**: modelc 를 *"Li₅.₄PS₄.₄Cl₁.₆ 실험 시료의 모델"* 이 아니라 *"Cl 1.6 을 전부 격자에 넣은 고용 상한 모델"* 로 쓴다 — 이 논문 `Table S1` (LiCl 4.4 vol%) · `Fig. 9d` · `Fig. S13` 이 그 문장의 원전이다.
3. **두 축 분리 (축 E)**: Li 와의 **화학 안정성** (R_int 증가 속도) 은 Cl 에 단조 · **덴드라이트 내성** (CCD) 은 비단조. "Cl-rich 가 음극에 좋다/나쁘다" 를 축 이름 없이 쓰지 않는다 — [GG] (LPSCl1.0 의 '적당한 불안정' 이 내부층에 최적) · Kang (LPSC₁.₆ CCD ≈ LPSC) 과 같은 방향의 증거가 하나 더 생겼다 (기전 설명은 셋이 다 다르다).
4. **σ_e 는 띠틈이 아니다**: Cl 과 함께 σ_e 가 30 배 줄었는데 우리 띠틈은 두 조성이 같은 급 — 실험 σ_e 를 우리 띠틈으로 '설명' 하는 문장을 쓰지 않는다.
5. **냉각 속도가 숨은 변수**: 같은 명목 조성의 문헌 σ 가 공정에 따라 크게 갈리는 이유 (축 A 의 Li₅.₄PS₄.₄Cl₁.₆ 3.3 ↔ 20.2 mS cm⁻¹ 행) 에 '냉각 중 LiCl 석출' 이 하나 더 들어간다.

---

## 9. Figure set ★

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | XRD (x 0.6–1.6) · 분말 색 · σ & a vs x · SAED · Nyquist | σ 1.6 → 8.8 · a 9.890 → 9.788 · LiCl 흔적 (x ≥ 1.3) — 재크롭 (위쪽 잘림 보정) |
| 2 | Li\|SE\|Li 휴지 600 h 시간분해 EIS + Bode + R_int vs 시간 | 화학 안정성 Cl 단조 (`Table S2`) — 안 봄 |
| 3 | CCD 3 배치 + 0.25 mA cm⁻² 400 h 사이클 | **CCD 비단조 (x = 1.3 최대 · 1.6 최저)** — 실독 |
| 4 | 0.25 mA cm⁻² 사이클 중 100회마다 in situ EIS | R_int 사이클 (`Table S3`) — 안 봄 |
| 5 | 0.5 mA cm⁻² 사이클 (Cl-13 1000회 · 나머지 < 30회 단락) | 고전류 덴드라이트 — 안 봄 (본문) |
| 6 | Li\|SE\|LNO@NCM622 용량 · 곡선 | ICE 68 vs 55 % — 안 봄 |
| 7 | Li-In\|SE\|LNO@NCM811 1000회 | 음극 영향 분리 — 안 봄 |
| 8 | 200회 뒤 Li\|SE 계면 XPS + 반정량 | PS₄³⁻ 81 vs 48 at% · Li₂Sₙ — 안 봄 (Source Data 로 수치) |
| 9 | SEM-EDS 파단면 · 단면 (Cl-06 · Cl-13) + cryo-STEM-EDS Cl-16 | **'LiCl 지배' 층 55 ± 6 µm · LiCl 껍질 ≈50 nm** — 재크롭 (a–c 복원) · 실독 |
| 10 | in situ Raman (Li\|SE 단면 · 충전 중) | Cl-06 Li₂Sₙ · P₂S₅ 출현 vs Cl-13 없음 — 손 크롭 · 실독 |
| S1 | Cl-10 TEM · SAED | 안 봄 |
| S2 | 전체 Nyquist (In\|SE\|In) | 안 봄 |
| S3 | Cl-06 · Cl-13 펠릿 SEM | 안 봄 |
| S4 | CCD 전압–시간 (단락 화살표) | 안 봄 |
| S5 | Cl-13 200회 뒤 Bode | 안 봄 |
| S6 | Li-In\|Cl-16\|LNO@NCM811 | Cl-16 ≈145 mAh g⁻¹ — 안 봄 |
| S7 | 0.25 mA cm⁻² 200회 (XPS · SEM 시료) | 안 봄 |
| S8 | 사이클 전 Cl-06 XPS | 안 봄 |
| S9 | 계면 EDS 지도 (Cl-06 · Cl-13) | 안 봄 |
| S10 | cryo-STEM-EDS Cl-06 (껍질 없음) · Cl-13 (≈20 nm) + 선 스캔 | **안쪽 Cl/S 판독 (§5.6)** — 실독 |
| S11 | Cl-13 펠릿 SEM-EDS 7 영역 | LiCl 응집 소량 — 안 봄 |
| S12 | Cl-16 반복 cryo-STEM | 안 봄 |
| S13 | Cl-16 냉각 대조 (서냉 → 급랭 vs 바로 급랭) | **껍질은 냉각 의존** — 실독 |
| S14 | 400회 뒤 Cl-16 STEM-EDS (껍질 소멸) | Cl 이동 추측 근거 — 안 봄 |
| S15 | 200회 뒤 계면 XRD | 안 봄 |
| S16 | 기전 모식도 | 안 봄 |
| Table S1 | σ · σ_e · a · LiCl vol% (5 조성) | 벌크 수치 원본 |
| Table S2 | 휴지 R_int (100 h 간격 · 오차 %) | 화학 안정성 수치 |
| Table S3 | 사이클 R_int (100회 간격) | 사이클 계면 수치 |

---

## 10. 비판 / 주의 (over-claim 방지) ★

1. 🔴 **"Cl 의 다수가 입자 표면" (p.11) 은 자기 정량과 맞지 않는다.** 근거는 cryo-STEM-EDS 지도 몇 입자 (정성) 다. 자기 Rietveld LiCl 분율은 Cl-16 **4.4(5) vol%** — 몰부피 (LiCl ≈34.0 Å³/f.u. · argyrodite a = 9.788 Å → 234.4 Å³/f.u.) 로 바꾸면 **≈0.32 LiCl/f.u. = 명목 Cl 의 ≈1/5** (*우리 산수*). '다수' 가 되려면 XRD 에 안 보이는 (비정질) LiCl 이 그 몇 배 있어야 한다. 격자상수가 x = 1.6 까지 거의 직선으로 줄어드는 것 (`Fig. 1c`) 도 격자 안 Cl 이 계속 는다는 쪽이다. 선 스캔 판독 (§5.6) 으로는 **Cl-13 은 안쪽 Cl 부족이 없고**, Cl-16 만 ≈절반 안팎이 테두리 쪽으로 읽힌다.
2. 🔴 **"55 ± 6 µm LiCl 지배 계면층" 은 EDS 가 Li 를 못 보는 상태에서 붙인 이름이다.** (i) 같은 Cl 지도에서 띠의 밝기가 SE 쪽과 비슷하거나 어둡다 (`figure-read`) — 순수 LiCl 이면 Cl 질량분율 ≈5 배 (ii) 질량 수지 (*우리 산수*): Cl-13 의 껍질 Cl (LiCl 2.7 vol% ≈ 0.19 LiCl/f.u.) 만으로 순수 LiCl 55 µm 를 지으려면 Cl 밀도비 ≈37 배 → **≈2 mm 두께 SE 의 껍질 Cl 을 다 모아야** 한다. 저자도 *"this LiCl layer should contain argyrodite and/or Li₃PS₄"* (p.9) 라 쓰지만, 띠가 **Li 금속 + Cl 함유상** 일 가능성은 다루지 않는다.
3. 🟠 **σ 상승의 원인은 측정되지 않았다.** "무질서 · Li 공공 증가" (p.10) 는 서론 인용 [14–15 · 20–22] 의 재진술이고 이 논문은 점유 정련 · NMR · 계산이 없다. σ 는 **총 σ** (입계 · LiCl 껍질 포함) 이고 공간전하 기여는 *"speculate"*. ⇒ 이 논문의 σ 를 '격자 무질서 효과' 의 근거로 인용하지 않는다.
4. 🟠 **Cl-06 "모든 Cl 이 S 자리에 치환" (p.10) 은 EDS 균일성에서 나온 과잉 해석**이다 — EDS 는 nm–µm 분포를 볼 뿐 자리 (4a/4d) 를 못 가린다.
5. 🟠 **소성 조건이 조성별로 안 적혀 있다** ("450–550 °C") · Rietveld 는 3° min⁻¹ 빠른 주사 · 프로그램 미기재 · LiCl 분율 오차가 값의 10 % 안팎 (4.4(5)).
6. 🟡 오기 · 표기: "6000 h" (→ 600 h, p.3) · "Cl > 1.6" (p.4, 그런 시료 없음) · Source Data `Figure1e` 단위 (kΩ 를 "ohms" 로) · ref 23 저자명 "Gil, G." (→ Gil-González, E.) · 초기 CCD 단계 시간 미기재.
7. 🟡 **풀셀 비교는 분리막만 바꾼 것**이다 — 양극 촉매질은 LSPSC 로 고정. 양극 쪽 Cl 효과를 읽는 근거로 쓰지 않는다.
8. 🟡 셀 시험 온도 24 ± 4 °C — 저자도 전압 요동을 실온 변동 탓으로 돌린다 (p.5). 0.5 mA cm⁻² 단락 사이클 수 비교에 그만큼의 여유를 둔다.

---

## 11. 인용 가능 문장 (영문 초안 · 조건 포함)

- "In Li₇₋ₓPS₆₋ₓClₓ prepared with slow cooling, the 24 °C total ionic conductivity rose from 1.6 to 8.8 mS cm⁻¹ for x = 0.6 → 1.6, while the critical current density peaked at x = 1.3 (≈1.04 mA cm⁻²) and was lowest at x = 1.6 (≈0.56 mA cm⁻²) (*Nat. Commun.*, 13, 1909 (2022))."
- "The same study detected LiCl as a separate phase for x ≥ 1.3 (4.4 vol% at x = 1.6 by Rietveld refinement) and Cl-enriched shells of about 20–50 nm on argyrodite grains by cryo-STEM-EDS, which disappeared when the sample was quenched directly after sintering."
- "Our Li₅.₄PS₄.₄Cl₁.₆ cell places all Cl in the lattice and therefore represents the solid-solution limit rather than an experimental sample, in which part of the chlorine can segregate as LiCl."
- ⛔ 쓰지 말 것: "the majority of excess Cl resides on grain surfaces" 를 단정으로 (자기 Rietveld 와 차수 불일치) · "a 55 µm LiCl layer forms at the Li interface" (EDS 는 Li 를 못 본다) · "Cl substitution increases conductivity through 4d-site disorder (Zeng 2022)" (점유를 재지 않았다) · 이 논문의 σ_e 를 우리 띠틈으로 설명.

---

## 12. Kang 2026 [39–41] 근거 대조 — 8번 문장 네 고리 (2026-11-09)

Kang 문장: *"In halogen-rich argyrodites such as LPSC1.6, Cl⁻ substitution for S²⁻ at the 4d sites lowers the local anionic charge density, which in turn enhances the connectivity of the Li⁺ cages and ultimately improves the ionic conductivity [39–41]."*

| 고리 | 이 논문 원문 (쪽 · 그림/표) | 방법 · 숫자 | 판정 |
|---|---|---|---|
| ① Cl 이 4d 자리에 | p.2 서론: *"a higher chlorinity leads to stronger Cl⁻/S²⁻ site disorders, and moreover, a higher occupancy of Cl atoms at the 4d site … [20–22]"* · p.2 결과: 격자 수축이 *"is considered the combining effects of … the increased Cl⁻/S²⁻ site disorders …"* | **인용 · 해석뿐** — 4a/4d 점유 정련 · 중성자 · NMR 없음 (Rietveld 는 a · LiCl 분율만, `Table S1`) | **안 보임** · 오히려 p.9 · p.11 의 *"Only a part of Cl atoms locates inside the argyrodite lattice"* · *"a majority exists on the grain surfaces"* 가 x = 1.6 에서 ① 의 전제 (Cl 이 격자에 들어간다) 를 **약화**한다 (정량은 §10-①) |
| ② 국소 음이온 전하밀도↓ | 없음 | — | **안 보임** |
| ③ Li⁺ cage 연결↑ | 없음 (cage · inter-cage · 확률밀도 · MSD 0) | — | **안 보임** |
| ④ 전도도↑ | p.3: *"increases linearly with increasing Cl concentration until x = 1.45, then shows a sharper increase to 8.8 mS/cm … for x = 1.6"* · 원인 p.10: *"The major reason is that the degree of X⁻/S²⁻ structural disorder and the Li vacancy concentration increase with increasing chlorinity"* | **실험** EIS 24 °C · 총 σ 1.6 / 3.6 / 5.3 / 6.1 / **8.8 mS cm⁻¹** (`Table S1` · `Fig. 1c`) · 원인 서술은 측정 없음 | **직접 (σ 값) · 원인은 주장만** — x = 1.6 의 σ 를 직접 잰 유일한 편 |

**메커니즘이 같은가** — **다르다.** 이 논문의 표제 기전은 *LiCl 나노껍질 → Cl 이동 → LiCl 지배 계면층 → 자기제한 · 덴드라이트 억제* (계면 미세구조) 이고, 벌크 σ 는 "무질서 + Li 공공" 을 인용으로 받고 "공간전하" 를 추측으로 보탠다. 전하밀도 · cage 연결 서사는 없다.

**판정 — Kang 8번 문장을 이 논문이**: **안 함 (④ 의 σ 값만 일부)**.
- "In halogen-rich argyrodites such as LPSC1.6" → **나옴** (x = 1.6 시료 실재) — 단 그 시료의 Cl 일부는 격자 밖 (LiCl 4.4 vol% + 껍질)
- "Cl⁻ substitution for S²⁻ at the 4d sites" → **안 나옴** (서론 인용 [20–22] = Patel 2021 · Gautam 2021 · de Klerk 2016 — 실제 근거는 그쪽)
- "lowers the local anionic charge density" → **안 나옴**
- "enhances the connectivity of the Li⁺ cages" → **안 나옴**
- "ultimately improves the ionic conductivity" → **σ 상승은 나옴 (실험)** · 그 원인이 ①–③ 이라는 것은 안 나옴
- Kang 쪽 함의: 같은 x = 1.6 에서 이 논문 CCD 가 가장 낮다 — Kang 의 *"LPSC₁.₆ 의 CCD 가 LPSC 와 같다"* (Kang digest §6) 와 같은 방향 (높은 σ ≠ 덴드라이트 내성).

---

## 13. 기법 용어 미니사전

- **chlorinity**: 이 논문의 말 — Li₇₋ₓPS₆₋ₓClₓ 의 x (명목 Cl 함량).
- **LiCl 나노껍질 · 골격 (nanoshell · framework)**: 입자 표면을 감싼 수십 nm Cl 농축층이 입자끼리 이어진 것. EDS 로 Li 를 못 보므로 'LiCl' 은 추정 이름이다.
- **cryo-STEM-EDS**: 시료를 −170 °C 로 유지한 채 주사투과전자현미경 + 에너지분산 X-선으로 원소 지도를 얻는다 — 전자빔 · 공기 손상을 줄이려는 것. 지도는 **두께 방향 투영**이다.
- **time-resolved EIS**: 셀을 쉬게 둔 채 일정 간격으로 임피던스를 재서 계면저항 (R_int) 이 시간에 따라 크는 속도 = 화학 반응성을 본다.
- **CCD (critical current density)**: 대칭셀 전류를 단계적으로 올려 단락이 나는 전류. 단계 크기 · 시간 · 압력 · 온도가 값을 좌우한다 — 여기선 35 µA cm⁻² 단계 · ≈3 MPa · 24 ± 4 °C · 3 배치.
- **self-limiting interphase**: 반응 산물층이 더 이상의 반응을 막아 스스로 멈추는 계면 (전자 절연 + 이온 전도).
- **space-charge layer**: 두 이온전도체 (또는 전도체–절연체) 경계에서 이동 이온이 재분배돼 생기는 전하층 — 복합체 σ 를 올릴 수 있다는 가설 (여기선 추측).
- **total σ (국소 최소 저항법)**: Nyquist 가 x 축에 가장 가까워지는 점의 저항으로 낸 σ — 입내 · 입계를 가르지 않는다.

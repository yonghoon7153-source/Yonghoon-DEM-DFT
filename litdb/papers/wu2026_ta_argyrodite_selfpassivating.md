# High-Conductivity Argyrodite Electrolyte with Self-Passivating Stability for Single-Electrolyte All-Solid-State Lithium Batteries — Wu et al. (Angew. Chem. Int. Ed. 2026)

> slug `wu2026_ta_argyrodite_selfpassivating` · DOI `10.1002/anie.202523225` · type `exp 주도 + DFT/AIMD 보조 (+ COMSOL phase-field)` · PDF `82ea256b-c0d36890(본문) + bc1e6898(SI)` · digested `2026-08-19` · status ✅ · 태그 **[외부]**

> elements: Li, P, S, Cl, Br, Ta, Nb, Mo, W, Ce, La, Fe, Y, Cr, As, Bi, Sb, Si, Ge, Sn, In, O, Ni, Co, Mn
> methods: DFT, AIMD, NEB, ICOHP, DOS, ESW, XPS, Raman

> **저자**: Xin Wu, Lixin Liang, Bingxuan Du, Yiwen Liu, Zhenjie Zhang, Yu Shi, **Shaochun Tang\***, **Guangjin Hou\***, **Haoshen Zhou\***, **Ping He\*** (Nanjing University 에너지과학공학 + 고체미구조 국가연구실 / 대련화물연구소 DICP) · *Angew. Chem. Int. Ed.* **2026**, 65, e23225 · VIP + Very Important Paper · 접수 2025-10-22 · 수리 2025-11-28 · online 2025-12-04 · 본문 12 pp + SI 36 pp (Fig 1–6, Fig S1–S26, Table S1–S12)

---

## 0. 이 digest 를 읽는 법

이 논문의 **주장은 두 층**이고 근거의 질이 서로 많이 다르다. 섞어 읽으면 안 된다.

1. **실험층 (강함)** — `Li5.5PS4.5Cl1.5−xBrx` 이중 할로겐 + P-자리 Ta⁵⁺ 치환으로 σ 12 mS/cm(30 °C), CCD 2.4 mA/cm², 대칭셀 1600 h, NCM811 full cell 1200 cyc 81 %, 10×6 cm² 파우치 200 cyc 96.4 %. XRD/Rietveld·XANES/EXAFS·MAS NMR·SLR NMR·XPS·ToF-SIMS·XR-CT 로 다각 검증. **여기까지는 재현 가능한 수치가 실려 있다.**
2. **계산층 (약함)** — 밴드갭 스크리닝(Fig. 2a, Fig. S5), cNEB 장벽(Fig. 3g), AIMD Li 확률밀도(Fig. 3h), ICOHP(Fig. 3k, Fig. S11), CDD/정전퍼텐셜(Fig. 3j, Fig. S10), COMSOL phase-field(Fig. 5g, Fig. S22). **이 층은 §4 감사에서 여러 군데가 무너진다.** 특히 **AIMD 300 K 20 ps 단독**과 **Ta 셀의 +22.8 % 부피 팽창**이 치명적이다.

그래서 이 digest 의 무게중심은 **§4 방법론 감사**·**§8 우리 대조**·**§11 놓친 부분/설정 오류 후보**에 있다. 실험 수치는 §3 에 정리해 두되 **소환값**으로만 쓴다 (우리 db 절대값과 섞지 않는다).

> ⚠ **전압 기준**: 이 논문은 전부 **vs Li/Li⁺** (In/InLi 환산 불필요). 그래서 우리 grand-potential onset 2.256 V 와 **같은 축**에서 비교할 수 있다 — 드문 경우다.

---

## 1. 한 줄 요약

**Cl/Br 이중 할로겐(음이온 무질서 최대) + P-자리 Ta⁵⁺ 6 mol% 로 σ 12 mS/cm 를 만들고, Ta 가 양극쪽엔 절연성 LiTaO₃(CEI)·음극쪽엔 금속성 Ta⁰(SEI)를 만들어 "자기부동태(self-passivating)"로 0.1–4.3 V 실용창을 얻었다** — 실험 성능은 최상급이지만, 그것을 설명하는 DFT 층(밴드갭 스크리닝·NEB·AIMD)은 **셀 크기·치환농도·시간척도가 주장과 맞지 않는다**.

---

## 2. 메타 / 동기

| 항목 | 내용 |
|---|---|
| 모체 | `Li5.5PS4.5Cl1.5` (Cl-rich argyrodite = **우리 modelc `Li5.4PS4.4Cl1.6` 의 사실상 동일 계열**) |
| 1단계 | 음이온: `Li5.5PS4.5Cl1.5−xBrx`, x = 0→1.5 · **x = 0.75 최적** (ΔS_conf 최대) |
| 2단계 | 양이온: `Li5.5P1−xTaxS4.5Cl0.75Br0.75`, x = 0→0.10 · **x = 0.06 최적** |
| 최종 | **`Li5.5P0.94Ta0.06S4.5Cl0.75Br0.75`** |
| 양극 | 단결정 NCM811 (무코팅! LNO/LZO 코팅 없음) |
| 음극 | bare Li 금속 (LMA) / 파우치는 graphite |
| 질문 | *"양극·음극 양쪽에 다 쓸 수 있는 **단일 전해질**을 만들 수 있나"* — 지금까지는 양극쪽 할라이드 + 음극쪽 황화물 **이중층**이 답이었다 |
| 착상 | **Al 용기가 진한 황산을 담는 이유 = Al₂O₃ 부동태막** → SE 도 분해되되 **치밀·이온전도·전자절연** 산물을 만들면 실용창이 넓어진다 (Fig. 1b) |
| 계산의 역할 | **선택 근거 제공** (어떤 M 을 P 자리에 넣을까 → 밴드갭 최대) + **사후 설명** (왜 빨라지나 → NEB/AIMD/ICOHP) |

---

## 3. 핵심 물성 (수치 총정리 — 전부 소환값)

### 3.1 음이온 시리즈 `Li5.5PS4.5Cl1.5−xBrx` (Table S1–S8, Fig. S3)

| x (Br) | 0 | 0.25 | 0.5 | **0.75** | 1.0 | 1.25 | 1.5 |
|---|---|---|---|---|---|---|---|
| a (Å, Rietveld) | 9.814 | 9.865 | 9.871 | **9.874** | 9.883 | 9.890 | 9.896 |
| ΔS_conf/R (Table S8) | 1.12 | 1.77 | 2.04 | **2.08** | 1.87 | 1.56 | 1.17 |
| σ (mS/cm, 30 °C) | 5 | 5.72 | 6.1 | **6.2** | 5.8 | 5.68 | 3.8 |

- ΔS_conf 최대점과 σ 최대점이 x = 0.75 에서 일치 → "혼합 할로겐 시너지".
- **⚠ σ 변동폭이 5.0 → 6.2 mS/cm (24 %) 뿐이고 오차막대가 없다.** 냉간가압 펠릿의 시료간 산포가 통상 이 정도다. 상관은 그럴듯하나 **인과 판정은 안 된다.**

### 3.2 Ta 시리즈 `Li5.5P1−xTaxS4.5Cl0.75Br0.75` (Fig. 2d–f)

| x (Ta) | 0 | 0.02 | 0.04 | **0.06** | 0.08 | 0.10 |
|---|---|---|---|---|---|---|
| σ (mS/cm, 30 °C) | 6.2 | 7.7 | 9.1 | **12** | 7.6 | 5.2 |
| Ea (eV, EIS 30–80 °C) | 0.32 | 0.31 | 0.30 | **0.28** | 0.30 | 0.34 |
| 2차상 | — | — | — | — | LiCl+미지 | LiCl+미지 |

- a: 9.874 → **9.908 Å** (x = 0.06; Table S9) = **+0.34 % 선형 / +1.03 % 부피** ← ★ §4·§11 에서 계속 쓰인다
- Rietveld R_wp: 6.21 %(무도핑, Fig. S8) / 6.06 %(Ta, Fig. 3a)
- Ta 자리 점유 4b 0.06 · P 0.94 (Table S9) — **정제에서 고정한 값인지 refine 한 값인지 불명** ⚠

### 3.3 전자·구조·계면

| 물성 | 값 | 조건 | 비고 |
|---|---|---|---|
| **밴드갭 (DFT PBE)** | 무도핑 **2.12** eV → Ta **2.66** eV | PBE, 단일 배열 | Nb 2.29 가 2위, 나머지 13종은 전부 2.12 아래 |
| **σ_e (전자전도도)** | 9.7×10⁻⁹ → **1.4×10⁻⁹ S/cm** | DC 분극 1 V, 1800 s (Fig. S13) | **6.9× 감소** |
| **NEB 장벽** | doublet+intra 0.50 → **0.31** eV · inter-cage 0.59 → **0.35** eV | cNEB, PBE | Fig. 3g |
| **SLR NMR Ea** | 고온 0.14 → **0.13** eV · 저온 0.10 → **0.05** eV | ⁷Li VT T₁, 14.1 T | Fig. 3f |
| **EIS Ea** | 0.32 → **0.28** eV | 30–80 °C, 6점 | Fig. 2f |
| **EXAFS Ta–S** | CN **4.11 ± 0.2**, d **2.26 ± 0.03 Å** | k 3–12 Å⁻¹, R 1.3–2.6 Å, k³ | Table S10 → **TaS₄ 사면체 확정** |
| **XANES** | Ta L₃ edge ≈ TaCl₅ | Fig. S9a | **Ta⁵⁺ 확정** |
| **실용 ESW** | **0.1 – 4.3 V** vs Li/Li⁺ | CV 0.1 mV/s, **3rd cycle** 접선 외삽 | Fig. 4a — **열역학 창 아님** |
| **1st cycle 산화 개시** | OCV **2.45 V** 부터 전류, 피크 ≈**3.4–3.5 V** (+16 µA) | CV cycle 1 | figure-read (Fig. 4a) |
| **1st cycle 환원 개시** | **0.76 V** | CV cycle 1 | 본문 명시 |
| **CCD** | **2.4** mA/cm² (Ta) vs **0.8** (무도핑) | 1 h step, Li/SE/Li | Fig. S15 / Fig. S18 |
| **대칭셀** | **>1600 h**, <60 mV (Ta) vs **278 h 단락** (무도핑) | 0.5 mA/cm², 0.5 mAh/cm² | Fig. 5a / Fig. S17a |
| **DFT 셀 부피** | **998 → 1226 Å³ (+22.8 %)** | Fig. S12c | ★ **실험 +1.03 % 와 22배 불일치** |
| Li(48h)-S₄ 부피 | 8.20 → 8.29 Å³ (+1.1 %) | Fig. 3l, figure-read ≈ | 2점만 |
| Li(24g)-S₃ 면적 | 7.09 → 7.20 Å² (+1.6 %) | Fig. 3l, figure-read ≈ | 2점만 |
| ICOHP | Li–S(Ta) −0.17 · Li–S(P) −0.62 · Ta–S 0.7 · P–S 1.6 eV | Fig. 3k | ⚠ 부호규약 §4.6 |

### 3.4 셀 성능 (Table S11 = 51편 횡비교)

| 구성 | 조건 | 초기 | 유지 |
|---|---|---|---|
| NCM811‖Ta-SE‖Li | 0.2C, 20 mg/cm², N/P 2.6, 3.0 mAh/cm² | 185.7 mAh/g | **100 %, 200 cyc** |
| " | 0.5C, 20 mg/cm² | 157.2 | **81.0 %, 1200 cyc** |
| " | 0.5C, **30 mg/cm²**, **N/P 1.8** | 138.7 | **81.0 %, 150 cyc** |
| rate | 0.1/0.2/0.5/1/2C | 200.6/188.8/146.6/113.2/59.3 mAh/g | 0.2C 복귀 188.5 |
| **파우치** NCM811‖Ta-SE‖graphite | 0.1C, **10×6 cm²**, 15 mg/cm² | **82.5 mAh** (1st CE 95.1 %) | **96.4 %, 200 cyc** |

셀 조립: PEEK Ø10 mm, SE 120 mg, 280 MPa(SE) → 350 MPa(양극), 운전 **20 MPa**. 파우치는 PTFE 건식(fibrillation) + 490 MPa 등방압 → 운전 **5 MPa**.

---

## 4. ★★ DFT/계산 방법 — 철저 감사 (1저자 요청)

> 표기: **✅ 본문/SI 명시** · **⚠ 추정(근거 병기)** · **⛔ 아예 없음**

### 4.0 코드 · 기본 세팅

| 항목 | 값 | 판정 |
|---|---|---|
| code | **이름 없음.** 그러나 SI 인용 [2] Blöchl PAW(1994), [3] **Kresse & Furthmüller PRB 54, 11169 (1996)** → **VASP** | ⚠ 추정(인용으로 사실상 확정) / 버전 ⛔ |
| functional | **PBE-GGA** | ✅ |
| vdW | 언급 없음 → 무보정 | ⛔ (황화물 층간 없으니 치명적이진 않음) |
| pseudo | **PAW** | ✅ (POTCAR 버전/valence 설정 ⛔) |
| E_cut (정적/NEB) | **520 eV** | ✅ |
| E_cut (AIMD) | **450 eV** | ✅ |
| k-mesh (정적/NEB) | **Γ-centered Monkhorst-Pack 2×2×4** | ✅ 값은 있으나 **셀이 없어 밀도 검증 불가** — §4.3 |
| k-mesh (AIMD) | **Γ-only 1×1×1** ("minimal") | ✅ |
| 수렴 | E 1×10⁻⁵ eV · F **0.01 eV/Å** · CG 500 ionic steps (정적) / E 5×10⁻⁵ eV (AIMD) | ✅ |
| **DFT+U** | **한 글자도 없음** | ⛔ — §4.4 에서 치명적 |
| **스핀 분극** | **한 글자도 없음**, Fig. S5 에 스핀분해 밴드 없음 | ⛔ / ⚠ 비분극 추정 |
| PREC | AIMD 에 **"low-precision mode"** 명시 | ✅ (그런데 이게 문제 — §4.5) |
| 셀 원자수 / 슈퍼셀 | **정적·NEB 는 ⛔.** AIMD 만 Fig. 3h 캡션에 **"in a 1×1×2 cell"** | ⚠ |

### 4.1 ★ AIMD 설정 — 1저자가 가장 궁금해한 부분

**SI 원문 전체 (이게 전부다):**
> *"AIMD simulations were performed in the NVT … A minimal Γ-centred 1×1×1 k-mesh, and a plane-wave energy cutoff of 450 eV were used… A Γ-centered k-point grid and low-precision mode were employed to balance computational efficiency. The structures were first statically relaxed and then heated from an initial temperature of 100 K to 300 K by velocity scaling over a period of 1 ps, and then **equilibrated at the desired temperature for 20 ps** in the NVT ensemble using a **Nosé-Hoover thermostat**. AIMD simulations were analyzed using **pymatgen-diffusion add-on package**. The Li-ion diffusion pathways were obtained by calculating the **probability density function** by averaging the number of Li-ions at each point in a uniform spatial grid for a given time frame."*

| 감사 항목 | 이 논문 | 우리 규약 | 판정 |
|---|---|---|---|
| **온도** | **300 K 단독** ✅ (Fig. 3h 캡션 *"at 300 K"* 로 재확인) | **600/800/1000 K 3점** (400/500 K 은 확산영역 미달로 판정 제외) | ⛔⛔ **치명** |
| **시간** | **20 ps** — 그것도 *"equilibrated"* 라고 적혀 있다 | prod **200 ps** (+ equilib 5 ps 별도) | ⛔ **10× 부족** |
| **시간간격 Δt** | ⛔ **없음** | 2 fs | ⛔ |
| **셀 크기** | 1×1×2 (≈ 9.99 × 9.99 × 19.99 Å, 원자수 ⛔) | 최소 수직폭 기준 유한크기 게이트 | ⚠ |
| **시간원점 (STO/MTO)** | ⛔ **없음** | **MTO 가 정본** (`lpsocl_beta_registry.json` 규칙) | ⛔ |
| **MSD 창** | ⛔ **MSD 자체를 안 보여준다** | **2–50 ps 고정** | ⛔ |
| **D 추출** | ⛔ **D 를 아예 안 뽑는다** | 자유절편 선형회귀 m/6 | — |
| **β (확산 지수) 게이트** | ⛔ | β̄ ≥ 0.80 (MTO) | ⛔ |
| **유한크기 여유 MSD@t vs (d/2)²** | 계산 안 함 (아래 우리 검산) | 자기 MSD 로 판정 | ⚠ |
| **시드 수** | **1** (명시 없음 = 1로 간주) | 3시드 (600 K) | ⛔ |
| **thermostat 파라미터** | Nosé-Hoover ✅, SMASS/주기 ⛔ | — | ⚠ |
| **NPT / 격자 완화** | NVT 고정 = PBE 완화 부피 | — | ⚠ (아래) |

#### ★ 검산 1 — 300 K · 20 ps 에 Li 는 얼마나 움직이나 (논문 자신의 σ 로)

σ = 12 mS/cm, n(Li) = 22/셀 ÷ 962.7 Å³ = 2.285×10²⁸ m⁻³ 로 Nernst–Einstein(H_R=1):

```
D(300 K) = σ k_B T / (n q²) = 8.5×10⁻¹² m²/s
MSD(20 ps) = 6 D t = 0.10 Å²      →  √MSD ≈ 0.32 Å
무도핑(6.2 mS/cm) :          0.053 Å²  →  √MSD ≈ 0.23 Å
```

**20 ps 궤적 전체에서 Li 한 개의 평균 변위가 0.2–0.3 Å 다.** 48h–48h doublet 거리(≈1.9–2.2 Å)의 1/8, inter-cage 거리(≈4 Å)의 1/15. **열진동 진폭 이하다.**

#### ★ 검산 2 — 논문 자신의 NEB 장벽으로 20 ps 안에 hop 이 몇 번?

ν₀ = 10¹³ s⁻¹, kT = 0.02585 eV, Li 44개(1×1×2), t = 20 ps:

| 경로 | E_a | τ(1 hop) | **20 ps 안 기대 hop 수 (셀 전체)** |
|---|---|---|---|
| 무도핑 inter-cage | 0.59 eV | 820 µs | **1.1×10⁻⁶** |
| 무도핑 intra-cage | 0.50 eV | 25 µs | **3.5×10⁻⁵** |
| Ta inter-cage | 0.35 eV | 76 ns | **0.012** |
| Ta intra-cage | 0.31 eV | 16 ns | **0.055** |
| (실험 σ 로 역산, d = 4 Å) | — | 3.1 ns | **0.28** |

⇒ **논문 자신의 장벽으로도, 실험 σ 로 역산해도, 20 ps 안에 hop 은 사실상 0회다.**
그러므로 **Fig. 3h 의 "expanded and interconnected 3D percolating network" 는 확산 사건을 본 것이 아니다.** 그 그림이 보여주는 것은 **평형 자리 주변의 열적 번짐(intra-cage 라이브레이션)** 이고, 두 패널의 차이는 (i) Ta 셀이 **22.8 % 더 크다**는 것(§4.2) 과 (ii) **등가면 isovalue 미기재**로 설명된다.

> 이건 "AIMD 를 했으면 D 를 내놔라" 라는 형식 지적이 아니다. **논문의 정성적 결론(percolation network 형성)이 자기 데이터의 시간척도로 지지되지 않는다**는 물리적 지적이다.

#### ★ 검산 3 — 유한크기는 (이번엔) 문제가 아니다 (공정하게)

1×1×2 셀 최소 수직폭 d ≈ 9.99 Å → (d/2)² = 24.9 Å². MSD(20 ps) ≈ 0.10 Å² ≪ 24.9 Å² → **유한크기 위반 없음.** 단 **확산이 아예 없어서** 그런 것이지 셀이 커서가 아니다. (대조: 우리 `lpsocl` 작은 셀은 MSD@50 ps 가 (d/2)² 를 **3.15× 초과** — 그건 진짜 확산이 있었기 때문. `kb/results/lpsocl_box_size_600K_2026_08_18.md`)

#### ★ NVT 부피 문제

AIMD 를 **PBE 완화 부피에서 NVT** 로 돌렸다. 무도핑 셀은 998 Å³ (a = 9.993 Å) vs 실험 9.874 Å → **+3.7 % 부피 과대**(PBE 통상). Ta 셀은 1226 Å³ (a ≈ 10.70 Å) vs 실험 9.908 Å → **+26 % 부피 과대**. 격자 부피는 argyrodite Li 이동장벽에 매우 민감하다. ⇒ **두 AIMD 셀이 서로 다른 정도로 팽창된 격자에서 돌아갔다.** 같은 잣대가 아니다.

### 4.2 ★★ 최대 설정 오류 후보 — Ta 모델의 치환농도·부피

**✅ 실측 (Fig. S12c, 확대해서 직접 봤다)**: DFT 최적화 단위셀 부피 **998 → 1226 Å³ = +22.8 %** (y축이 800 에서 시작해 시각적으로도 과장).
**✅ 실측 (Table S9 / Table S4)**: 실험 격자 9.874 → 9.908 Å = **+1.03 % 부피**.

```
DFT 팽창 +22.8 %  ÷  실험 팽창 +1.03 %  ≈  22 배 과대
```

**⚠ 원인 추정 (강한 추정, 산술 근거 있음)**: 998 Å³ ↔ a = 9.993 Å = **conventional F-43m 셀 1개** = P 자리 **4개**. Fig. S12b 에서 **Ta–S₄ 사면체가 딱 1개** 분홍 테두리로 강조돼 있다. ⇒ **1 Ta / 4 P = x = 0.25**, 명목 조성 x = 0.06 의 **4배**. (x = 0.06 ≈ 1/16 을 구현하려면 P 16개 = 2×2×1 슈퍼셀 ≈ 4000 Å³ 가 필요한데 그런 셀은 어디에도 없다.)

**파급 (이게 진짜 문제)**:
- Fig. 3g 의 NEB 장벽(0.50→0.31, 0.59→0.35 eV)이 **26 % 팽창한 격자**에서 계산됐다. argyrodite 장벽은 부피에 극도로 민감하다 — **장벽 감소분의 상당 부분이 Ta 화학이 아니라 인공 팽창**일 수 있다.
- Fig. 3h 의 Li 확률밀도 차이도 **더 큰 케이지** 때문일 수 있다.
- **논문 내부 모순**: Fig. 3l 은 같은 x = 0→0.06 구간에서 Li(48h)-S₄ 부피 **+1.1 %**, Li(24g)-S₃ 면적 **+1.6 %** 라고 한다. 셀이 22.8 % 커졌는데 그 안의 Li 다면체가 1.1 % 만 커질 수 없다. **Fig. S12c 와 Fig. 3l 은 같은 계산에서 나올 수 없다.**

### 4.3 k-mesh 감사

`Γ-centered 2×2×4` ✅ 값은 있는데 **어떤 셀에 대한 건지 없다** ⛔.
- 셀이 conventional cubic(≈10 Å 등방)이면 → **등방 셀에 비등방 메시**. c 축만 2배 촘촘 = 근거 없음.
- 셀이 1×1×2(10×10×20 Å)이면 → **가장 긴 축에 가장 촘촘한 메시**. 정반대다 (2×2×1 이 맞다).
- Fig. S5 의 k-path 가 **`Γ–X|Y–Z|R₂–Γ–T₂|U₂–Γ–V₂` = 삼사정계(TRI) 표준 경로**다(figure-read). 즉 S/Cl/Br 를 4a/4d 에 배치한 순간 대칭이 완전히 깨져 **삼사정계 셀**이 됐다. 삼사정계 격자벡터 길이를 안 주고 2×2×4 만 적으면 **k 밀도 검증이 원리적으로 불가능**하다.

### 4.4 ⛔ DFT+U · 스핀 부재 — 밴드갭 스크리닝(Fig. 2a)을 무너뜨린다

스크린한 15원소: Mo, W, Ce, La, Fe, Y, Cr, As, Bi, Sb, Si, Ge, Sn, Nb, Ta.
(Fig. S5 는 **패널 16개**인데 Fig. 2a 막대는 15개 — 한 패널 범례가 **`In`** 으로 읽힌다(figure-read, 저해상도). **In 은 계산해 놓고 막대차트에서 빠졌다** ⚠)

| 원소 | 보고 gap (eV) | 문제 |
|---|---|---|
| Mo | **0.001** | Mo 4d — U 필요. 사실상 금속 (Fig. S5 패널 1 에서 밴드가 E_F 를 가로지른다, figure-read) |
| W | **0.006** | W 5d — U 필요. Fig. S5 패널 2 는 −6~+5 eV 전체가 연속 (갭 없음, figure-read) |
| Ce | **0.031** | **Ce 4f** — PBE 가 4f 를 갭 안에 꽂는 교과서적 실패. U 없이는 무의미 |
| Fe | 0.82 | **Fe³⁺ d⁵ 고스핀** — 스핀분극 없으면 완전히 틀린다 |
| Cr | 0.92 | **Cr³⁺ d³** — 동일 |

⇒ **하위 5개(Mo/W/Ce/Fe/Cr)의 갭은 방법론적으로 인용 불가**다. 그런데 논문은 이 막대차트로 **"Ta 가 최고"** 를 결론짓는다. Ta⁵⁺·Nb⁵⁺ 은 **d⁰ 이고 P⁵⁺ 와 동가(isovalent)** 라 U/스핀이 필요 없다 — 즉 **Ta 가 1위인 건 우연히 맞은 것에 가깝고, 순위표 자체는 신뢰할 수 없다.**

추가로 **`Li_y`** 문제: Fig. 2a 범례가 `Li_yP0.9M0.1S4.5Cl0.75Br0.75` (figure-read — 확대해서 확인, 본문 캡션에는 `Li₇` 처럼 인쇄돼 있으나 그림 안은 명확히 `y`). **y 가 M 마다 어떻게 정해졌는지 어디에도 없다.** M 이 3+/4+/5+/6+ 로 흩어져 있으니 y 는 반드시 달라져야 하고, y 선택이 갭을 통째로 바꾼다. ⇒ **재현 불가능한 스크리닝.**

### 4.5 정적 DFT 기타

- **CG + 500 ionic steps, F < 0.01 eV/Å** ✅ — 표준. 다만 **격자까지 완화했는지(ISIF) ⛔**. Fig. S12 가 "unit-cell volume" 을 비교하니 완화한 것으로 보이나 명시 없음 ⚠.
- **"low-precision mode"** (AIMD): VASP `PREC=Low` 는 FFT 격자를 줄여 **egg-box 힘 오차**를 만든다. 450 eV 와 조합하면 S/Cl/Br 계엔 공격적이다 ⚠.
- **Γ-only + PREC=Low + 20 ps** = 계산비용을 최소화한 세팅. 정성 그림 이상을 요구할 수 없다.

### 4.6 ⚠ COHP/ICOHP — 부호 규약이 자기모순

**✅ 본문 명시**: *"The integrated COHP (ICOHP) value up to the Fermi energy serves as a measure of bonding strength, with **more negative values indicating stronger bonds**."*
**✅ Fig. 3k 실측값**: Li–S(Ta) **−0.17** · Li–S(P) **−0.62** · Ta–S **+0.7** · P–S **+1.6** eV.
**✅ 본문 결론**: *"…Ta–S and P–S … are 0.7 and 1.6 eV … confirming a significantly **stronger** interaction between Ta⁵⁺ and S²⁻ compared to P⁵⁺ and S²⁻."*

**⚠ 문제 (Fig. S11 을 직접 보고 확인)**: x축이 **`−COHP`** 라고 인쇄돼 있는데, P–S 곡선(Fig. S11a)의 **가장 큰 구조가 −17.5 eV / −14.5 eV 에서 −7.5 / −5.5 로 음수쪽**에 있다. 표준 LOBSTER 규약(−COHP > 0 = 결합)대로 읽으면 **PS₄³⁻ 의 가장 깊은 σ 결합 상태가 반결합**이라는 뜻이 되어 물리적으로 불가능하다. ⇒ **축 라벨이 `−COHP` 가 아니라 `COHP` 이거나, Fig. 3k 의 P–S/Ta–S 막대만 부호가 뒤집혀 있다.** 셋(축 라벨 / Fig. 3k 부호 / 본문 문장) 중 하나는 반드시 틀렸다.

**어느 결론이 살아남나**:
- ✅ **살아남음**: `|Li–S(Ta)| 0.17 < |Li–S(P)| 0.62` — **Ta 옆 S 의 Li–S 결합이 3.6× 약하다.** 같은 결합종끼리의 크기 비교라 부호규약과 무관. **논문 메커니즘의 핵심은 이거고, 이건 유효하다.**
- ⛔ **무너짐**: "Ta–S 가 P–S 보다 강하다" — 어떤 규약으로 읽어도 P–S(1.6) 가 Ta–S(0.7) 보다 크다. **결합 강도로 읽으면 정반대 결론이 나온다.**
- **크기 자체도 우리와 4–10배 차이** — §8.4 참조. **절대값 이식 금지.**

### 4.7 ⛔ 계면 계산 — 아예 없다 (1저자 질문 직답)

> **"계면 계산이 있으면 닫힌계인지 grand-potential 인지, hull 기준계가 무엇인지"** → **둘 다 아니다. 계면 열역학 계산이 0건이다.**

SEI/CEI 주장(§Self-passivating)의 근거는 전부 **실험**이다: XPS(Fig. 4d–f, Fig. S14, Fig. S21), ToF-SIMS 3D(Fig. 4g,h), XR-CT(Fig. 5b,f), DRT(Fig. 5d,e), 대칭셀(Fig. 5a).
계산이라고는 **COMSOL phase-field** 하나뿐이고 이건 **연속체 모델**이지 열역학이 아니다:
- Allen–Cahn 상장 + Nernst–Planck + Poisson (SI 3쪽), 계수는 Table S12.
- **⚠ 치명적 서술 공백**: Table S12 는 **단 하나의 파라미터 세트**만 준다 (D_i = 2.5×10⁻¹⁰ m²/s, σ_i = 1 S/m, T = 298.15 K, ω = 4, δ = 0.05 …). 그런데 Fig. 5g(Ta 전해질)와 Fig. S22(무도핑 전해질)는 **결과가 완전히 다르다** (균일 vs 덴드라이트 돌기). **두 계산에서 무엇을 다르게 넣었는지 아무 데도 없다.** ⇒ 이 시뮬레이션은 현재 상태로 **재현 불가능**하고, "Ta SEI 가 Li flux 를 균일화한다"는 결론을 지지하지 못한다.
- (공정을 위해: D_i 2.5e-10 과 σ_i 1 S/m 은 c₀ ≈ 1 M 희박용액 가정이면 Nernst–Einstein 으로 서로 **정합**한다. c₀ 가 Table S12 에 없을 뿐 — 이건 오류가 아니라 기재 누락.)

### 4.8 ⛔ 통계 — 전부 없음

| 항목 | 상태 |
|---|---|
| 시드 수 (AIMD) | 명시 없음 → **1** |
| 반복 펠릿 수 (σ, Ea) | ⛔ |
| 오차막대 | **논문 전체에 0개** (Fig. 2d, 2f, S3b 전부 없음) |
| 유의성 검정 | ⛔ |
| 펠릿 밀도 / 상대밀도 | ⛔ (σ = L/(R·πr²) 만) |
| EIS 등가회로 | ⛔ (절편 읽기로 추정) |
| Rietveld 오차 (esd) | ⛔ (R_wp 만) |

**그래서 σ 6.2 → 12 mS/cm (1.94×) 도, Ea 0.32 → 0.28 eV (−0.04) 도 "유의하다"고 주장된 적이 없다.** Ea 차이 0.04 eV 는 **50 K 폭(30–80 °C) 6점 Arrhenius 의 통상 피팅 오차(±0.01–0.02 eV)** 와 같은 자릿수다. σ 1.94× 는 크지만 단일 펠릿이다.

> 우리 규율과 대응: 우리도 **단일시드 1.33× 를 철회**한 적이 있다 (SEMIFINAL 2026-07-09). 같은 함정이다.

### 4.9 ⚠ 무질서 처리

- **DFT: 단일 정렬 배열 1개** (Fig. 3d 캡션 자체가 *"Ordered crystal structure"*). SQS ⛔, enumeration ⛔, 배열 앙상블 평균 ⛔.
- 실제 시료는 4a/4d 에 S/Cl/Br 가 섞여 있다 (Table S9: 4a = S 0.21/Cl 0.25/Br 0.54, 4d = S 0.29/Cl 0.56/Br 0.15 — **Cl 은 4d, Br 은 4a 선호**).
- **ΔS_conf 는 DFT 가 아니라 Rietveld 점유율에 해석식을 넣어 계산** (SI 4쪽). 즉 **무질서는 "지표"로만 쓰이고 계산 안으로 안 들어간다.**
- 파급: 단일 배열 NEB 는 **그 배열의 그 경로 장벽**이지 침투(percolating) 장벽이 아니다. 실제 무질서계의 유효 장벽은 분포의 최소경로가 지배해서 **훨씬 낮다** — 실제로 무도핑 NEB 0.50/0.59 eV 는 자기들 EIS **0.32 eV** 의 1.6–1.8배, NMR **0.14 eV** 의 3.6–4.2배다. **논문은 이 불일치를 언급하지 않는다.**

---

## 5. Figure set ★

> **내가 실제로 확대해 본 그림**: `Fig. 2` · `Fig. 3` · `Fig. 4` · `Fig. S5` · `Fig. S11` · `Fig. S12` (크로핑 PNG 6장).
> 나머지(Fig. 1, 5, 6 · Fig. S1–S4, S6–S10, S13–S26)는 **PDF 페이지 렌더 해상도로만** 봤다 — 축 눈금 수준의 정밀 판독은 안 했다.
> 크로핑 총 39장 (본문 6 + SI 23 + 표 10). 미추출 5건은 정상(빈 페이지 Fig. S15/S16/S21, 영역 없는 Table S5/S10).

| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a,b | 음이온/양이온 골격 모식 + 자기부동태 개념도 (열역학 불안정 → SEI/CEI → 실용창 확장) | **개념 프레임 차용 가능**: "분해량"이 아니라 "분해산물의 전자절연성"이 실용창을 정한다 — 우리 §B③ 논지와 동일 |
| **2a** | **P-자리 15원소 밴드갭 스크리닝** (Mo 0.001 → Ta 2.66 eV, 기준선 2.12 eV) · y축 **broken axis** | ⛔ **순위표 인용 금지** (U/스핀 부재, Li_y 미기재). 단 **PBE 무도핑 2.12 eV ↔ 우리 modelc 2.099 eV** 는 좋은 교차검증 |
| 2b | XRD x = 0–0.10, (311)/(222) 저각 이동, x ≥ 0.08 LiCl 2차상 | Ta 고용한계 ≈ 0.06–0.08 — **우리 도핑 cascade 의 고용한계 감각치** |
| 2c | Raman PS₄³⁻ ≈ 425 cm⁻¹ 저파수 이동 | 우리 Raman 앵커와 같은 밴드 |
| 2d,e,f | σ 볼케이노(6.2→**12**→5.2) · Arrhenius 30–80 °C 6점 · Ea(0.32→**0.28**→0.34) | **오차막대 0** — "volcano" 는 경향까지만 |
| 3a | Rietveld R_wp 6.06 %, a = 9.908 Å | 실험 팽창 +0.34 % — **Fig. S12 반박의 근거** |
| 3b,c | Ta L₃ wavelet/FT-EXAFS, Ta–S ≈1.8 Å (R+ΔR) | **Ta 가 4b 에 들어가 TaS₄ 를 만든다** = 우리 Track2 자리판정 방법의 외부 사례 |
| **3d,e** | 정렬 구조 모델 + 3경로(doublet / intra-cage / inter-cage) | 우리 BVSE 채널 해석과 같은 3분할 어휘 |
| 3f | ⁷Li SLR T₁ VT-NMR, 고온 0.14→0.13 · 저온 0.10→0.05 eV | **NMR Ea 앵커** — EIS(0.32)·NEB(0.59)와 3자 비교 (§8.2) |
| **3g** | **cNEB 장벽** 0.50→0.31 (doublet+intra) · 0.59→0.35 eV (inter-cage) | ⚠ **팽창 격자 의심** — 우리 NEB 와 직접 비교 금지 |
| **3h** | **AIMD Li 확률밀도** 1×1×2, 300 K | ⛔ **"percolation" 주장 지지 불가** (검산 2). 우리가 왜 600 K 부터 도는지의 **교과서적 반례** |
| 3i | ⁷Li 1.16/1.48 ppm · ³¹P 86.3/88.1 ppm MAS | ⚠ **그림 색배정 ↔ 본문 up-field 서술 모순** (§11-③) |
| 3j | P–S₄ vs Ta–S₄ 차전하밀도 (Ta 주변 e⁻ 축적) | 우리 CDD 그림 양식과 동일 |
| **3k** | ICOHP 4종 막대 | ⚠ 부호규약 (§4.6). **살아남는 건 Li–S(Ta) 0.17 < Li–S(P) 0.62** |
| 3l | Li(48h)-S₄ 부피 8.20→8.29 Å³ · Li(24g)-S₃ 면적 7.09→7.20 Å² | **2점 트렌드** + Fig. S12 와 내부모순 |
| 4a | CV 3사이클, 1st 산화피크 ≈3.4 V(+16 µA) → 3rd 접선 **0.1–4.3 V** | ⚠ **실용창(passivated)** — 우리 grand-potential 2.256 V 와 **혼용 금지**. 단 1st cycle 개시 2.45 V 는 우리 값과 가깝다 |
| **4d,e,f** | XPS S 2p / P 2p / **Ta 4f** — pristine TaS₄³⁻ 26.5 → CEI **LiTaO₃** 27.4/25.5 → SEI **금속 Ta⁰** 24.4/22.4 eV | ★★ **우리 cascade 와 직접 대조** (§8.5). SEI 에 금속이 있다 = 논문 자기 설계원칙과 충돌 |
| 4g,h | ToF-SIMS 깊이/3D: CEI(S²⁻·PS₃⁻·TaO₃⁻) · SEI(LiS⁻·Li₂P⁻·Ta⁺) | ⚠ **Ta⁺ 큐브는 거의 전부 최소값(분홍)** — SEI 의 Ta 농축 증거는 약하다 (figure-read) |
| 5a–f | 대칭셀 1600 h · XR-CT · Nyquist/DRT(R1–R5, 0–300 h 안정) | DRT 5피크 분해는 우리 임피던스 해석 참고 |
| 5g | COMSOL 전위·Li 농도 (SEI 있는 경우) | ⛔ **입력 미기재로 재현 불가** (§4.7) |
| 6a–k | 셀 성능 (1200 cyc 81 % · 30 mg/cm² · 파우치 96.4 %) | 성능 벤치마크로만 |
| S5 | 16 패널 밴드구조 (**삼사정계 k-path** · In 패널 존재) | **대칭이 완전히 깨진 셀**임을 드러내는 결정적 증거 |
| S11 | COHP 곡선 4종 | **부호규약 붕괴의 증거** |
| S12 | DFT 구조 2종 + **셀 부피 998 → 1226 Å³** | ★★ **최대 설정 오류 후보** |
| S13 | DC 분극 σ_e 9.7e-9 → 1.4e-9 S/cm + 갭 막대 | **갭 +0.54 eV 인데 σ_e 6.9× 만 감소** → §8.3 |
| Table S8 | ΔS_conf/R 7조성 | 무질서 지표 정량화 방식 |
| Table S9 | Ta 시료 Rietveld (4a/4d 점유) | **Cl→4d, Br→4a 선호** = anti-site 정보 |
| Table S10 | EXAFS 피팅 (Ta–S CN 4.11, 2.26 Å) | Ta 자리 확정 근거 |
| Table S11 | 51편 성능 횡비교 | 벤치마크 표 |
| Table S12 | COMSOL 계수 (**단일 세트**) | 재현 불가의 증거 |

---

## 6. 결과 — 섹션별 상세

### 6.1 다중 할로겐 도입 (Fig. S1–S3, Table S1–S8)

Li₂S + P₂S₅ + LiCl + LiBr 을 유성볼밀(500 rpm, 15 h, ZrO₂ 30:1) → 밀봉 앰플 500 °C 5 h. XRD/Raman 은 x = 0–1.5 전 조성에서 argyrodite 단상. Rietveld 로 4a/4d 점유를 뽑아 ΔS_conf 를 계산하니 **x = 0.75 에서 최대(2.08 R)**, σ 도 여기서 최대(6.2 mS/cm). 논문 논지: *혼합 할로겐 → 음이온 부격자 무질서 ↑ → Li 이동 촉진.*

**우리 시각**: 이건 **[Li25] CuBr₂ 이중도핑**, **[Kraft17]**, **[deKlerk16]** 이 이미 세운 축이다. 새로움은 "ΔS_conf 를 정량 서술자로 썼다"는 점 정도. 그리고 σ 변동폭이 24 % 뿐이라 **무질서-σ 인과의 결정적 증거는 아니다**.

### 6.2 P-자리 양이온 스크리닝 (Fig. 2a, Fig. S5)

**목표 함수 = 밴드갭 최대화.** 논거: *"A wider band gap is desired for SSEs to minimize electronic conductivity, thus suppressing self-discharge and mitigating Li dendrite growth."*
15원소 중 **Ta(2.66) > Nb(2.29) > 기준 2.12 > Sn(1.06) > … > Mo(0.001)**.

**⚠ §4.4 대로 이 순위표는 인용 불가.** 그리고 **§8.3 에서 보듯 목표 함수 자체도 자기 데이터로 검증되지 않는다** (갭 +0.54 eV ↔ σ_e 6.9× 만 감소, 예측은 3.4×10⁴×).

### 6.3 Ta 조성 최적화 (Fig. 2b–f, Fig. 3a–c, Fig. S6–S9)

- XRD: x ≤ 0.06 단상, x ≥ 0.08 LiCl + 미지상 → **고용한계 ≈ 0.06–0.08**
- (311)/(222) 저각 이동 → 격자 팽창 (Ta⁵⁺ 0.54 Å vs P⁵⁺ 0.2 Å, 논문 인용값)
- Raman 431.32 cm⁻¹ 저파수 이동 → PS₄ 국소 섭동
- XANES: Ta L₃ 엣지가 TaCl₅ 와 겹침 → **Ta⁵⁺**
- EXAFS: 주 피크 ≈1.8 Å (Ta–Cl/Ta–Ta 와 구분), wavelet 최대 ≈1.8 Å, **Ta–S CN 4.11 ± 0.2 · d 2.26 ± 0.03 Å** → **TaS₄ 사면체** (PS₄ 유사)
- σ 볼케이노 최대 **12 mS/cm @ x = 0.06** (무도핑의 1.94×), Ea 최소 0.28 eV
- x > 0.06 에서 σ 하락 = *"emergent heterogeneous phases disrupt the long-range ion conduction pathways"*

**⚠ 헤드라인 온도 주의**: σ 12 mS/cm 은 **30 °C** 측정값(Fig. 2d 캡션). 초록은 *"room temperature"* 라고 쓴다. Ea 0.28 eV 로 25 °C 환산하면 **≈10.0 mS/cm** (우리 환산). 20 % 낙관.

### 6.4 왜 빨라지나 — 4중 논증 (Fig. 3f–l)

논문이 쌓는 논리 사슬:

```
Ta⁵⁺(d⁰) 가 S²⁻ 와 더 강하게 상호작용
   → S²⁻ 의 Li⁺ 에 대한 정전인력 약화 (ICOHP Li–S: −0.62 → −0.17)
   → ⁷Li/³¹P 화학이동 변화 = Li 핵 전자밀도 ↑
   → Li(48h)-S₄ 다면체 팽창 (bottleneck 확장, Fig. 3l)
   → NEB 장벽 ↓ (0.59 → 0.35 eV)
   → AIMD Li 확률밀도 3D 연결 ↑ (Fig. 3h)
   → σ ↑ (12 mS/cm), Ea ↓ (0.28 eV)
```

**어느 고리가 버티나**:

| 고리 | 판정 |
|---|---|
| Ta⁵⁺–S 상호작용 강함 | ✅ EXAFS(TaS₄ 확정) + CDD(Fig. 3j) 로 독립 지지. ICOHP 부호는 §4.6 |
| Li–S(Ta) 가 Li–S(P) 보다 약함 | ✅ **부호규약 무관하게 성립** (0.17 < 0.62) — **사슬의 진짜 심장** |
| NMR 화학이동 근거 | ⚠ **그림-본문 방향 모순** (§11-③). 방향이 뒤집히면 이 고리는 **역방향** |
| bottleneck 팽창 | ⚠ 2점 트렌드 + Fig. S12 와 모순 |
| NEB 장벽 감소 | ⚠ **26 % 팽창 격자** 혐의. 그리고 무도핑 0.59 eV 는 실험 0.32 eV 와 1.8× 어긋남 |
| AIMD percolation | ⛔ **20 ps @300 K 에 hop 0회** (검산 2) |
| σ ↑ | ✅ 실측 (단일 펠릿, 오차막대 없음) |

⇒ **결론 자체(Ta 가 σ 를 올린다)는 실험으로 맞다. 그 인과 사슬의 계산 근거는 절반이 무너진다.**

### 6.5 자기부동태 — 실용 ESW (Fig. 4a–c)

- 셀: 산화쪽 `Li|SE|SE+KB(Pt)`, 환원쪽 `Pt|SE|Li` (KB 대신 Pt 를 쓴 이유 = *"avoids interference from lithium insertion currents in carbon materials at low potentials"* — **좋은 대조 설계다**)
- CV 0.1 mV/s: **1st cycle** — 환원 0.76 V 개시 + 0 V 근처 Li 석출 피크; 산화는 **OCV 2.45 V** 부터, **피크 ≈3.4–3.5 V (+16 µA)** (figure-read)
- **2nd/3rd cycle** — 전류가 급감. 3rd 접선 외삽으로 **0.1 – 4.3 V** 를 "practical ESW" 로 선언

**우리 해석**: 이건 **부동태화된 kinetic window** 다. 열역학 창이 아니다. 논문은 이 구분을 **명시적으로** 한다(Fig. 4b,c 가 정확히 "thermodynamic instability → self-passivating stability" 모식). **정직한 서술이다.** 다만 인용할 때 우리가 축을 붙여야 한다.

### 6.6 CEI / SEI 성분 (Fig. 4d–h, Fig. S14, Fig. S21)

| 위치 | 종 | XPS BE (eV) |
|---|---|---|
| pristine | PS₄³⁻ / TaS₄³⁻ | S 2p 161.5 · P 2p 131.5 · Ta 4f 26.5 |
| **CEI** (양극쪽) | 원소 S · P₂S₅ · **LiTaO₃** | S 165.3/163.0 · P 134.8/133.8 · Ta **27.4/25.5** |
| **SEI** (음극쪽) | Li₂S · Li₃P · **금속 Ta⁰** · LiCl · LiBr | S 161.3/160.0 · P 130.0/129.3 · Ta **24.4/22.4** · Cl 200.3/199.6 · Br 3d 69 |

ToF-SIMS: CEI 는 S²⁻/PS₃⁻/TaO₃⁻, SEI 는 LiS⁻/Li₂P⁻/Ta⁺ — 셋 다 표면에서 급감 → **박막 계면층 확인.**
대조군: **무도핑 SE 의 SEI 에는 Ta 계열이 당연히 없고**(Fig. S21), 278 h 에 단락, XR-CT 에 균열·보이드(Fig. S19, S20).

**⚠ 논문이 안 밝힌 것: CEI 의 LiTaO₃ 에 들어간 산소는 어디서 왔나.** 전해질 `Li5.5P0.94Ta0.06S4.5Cl0.75Br0.75` 에는 **O 가 없다.** 유일한 O 공급원은 **NCM811 격자산소**(또는 표면 탄산/수산화물). 즉 **"CEI 가 좋다"는 것은 곧 "양극이 산소를 내줬다"는 뜻**이다 — 이건 [Zuo22]·[Fan26] 이 말하는 O-방출 결합 문제와 정확히 같은 자리다. 논문은 이 대가를 계산에 넣지 않는다.

### 6.7 Li 금속 상용성 (Fig. 5, Fig. S15–S22)

CCD 2.4 (Ta) vs 0.8 mA/cm² (무도핑) · 대칭셀 >1600 h(<60 mV) vs 278 h 단락 · 0–300 h EIS/DRT 안정(R2, R3 = SEI 저항이 거의 불변) · XR-CT 에 덴드라이트·보이드 없음. **실험 근거는 충분하다.**
COMSOL(Fig. 5g, S22)만 §4.7 대로 재현 불가.

---

## 7. 전체 논증 흐름 (한눈에)

```
[음이온] Cl/Br 혼합 → ΔS_conf 최대(x=0.75) → σ 6.2 mS/cm
                                  │
[양이온] 밴드갭 스크리닝(15원소) → Ta 선택 ⚠(U/스핀 없음)
                                  │
        Ta⁵⁺ → 4b 자리 TaS₄ (XANES+EXAFS ✅)
                                  │
        Li–S 약화(ICOHP ✅) + bottleneck 팽창(⚠) + NEB↓(⚠) + AIMD(⛔)
                                  │
                        σ 12 mS/cm, Ea 0.28 eV ✅
                                  │
[계면]  분해는 일어난다(CV 1st) → 그러나 산물이 좋다
        CEI = LiTaO₃(절연) / SEI = Li₂S+Li₃P+LiCl+LiBr+Ta⁰
                                  │
                    2nd/3rd CV 전류 급감 = 부동태 ✅
                                  │
        실용창 0.1–4.3 V → 단일 전해질로 NCM811‖Li 1200 cyc 81 %
```

---

## 8. ★★ 우리 결과와의 대조 (1저자 요청 — digest 내부 절)

### 8.1 밴드갭 — 놀랍도록 가깝다 (그러나 우연에 가깝다)

| | 이 논문 | 우리 | 비고 |
|---|---|---|---|
| Cl-rich argyrodite PBE gap | **2.12 eV** (`Li5.5PS4.5Cl0.75Br0.75`) | **2.099 eV** (`modelc = Li5.4PS4.4Cl1.6`) | **Δ 0.02 eV** |
| — | — | 2.066 eV (`comp1 = Li6PS5Cl`) | |
| +O 도핑 | — | 2.2309 eV (LPSOCl) | |
| Ta 치환 | **2.66 eV** | (해당 없음) | |

**판정: △ 일치하지만 "확인"으로 쓰면 안 된다.**
- 둘 다 PBE → **둘 다 실험 대비 ~1 eV 과소** (우리 mBJ 3.11 / HSE 3.30 대조군 있음).
- 우리는 **fixed-occ nscf VBM/CBM 고유값** (DOS-threshold 금지 규율). 이 논문은 **판독법 미기재**.
- 이 논문 셀은 §4.3 대로 **삼사정계 단일 배열**, 우리도 단일 배열 — **무질서 배열에 따라 ±0.2–0.3 eV 흔들린다**.
- ⇒ **"둘 다 wide-gap insulator" 수준까지만.** 0.02 eV 일치는 자릿수 우연이다.

**Ta 2.66 eV 는 이식 금지**: §4.4 (U/스핀 없음, Li_y 미기재) + §4.2 (26 % 팽창 셀).

### 8.2 이온전도 Ea — 3자 비교표 (방법 축을 반드시 붙인다)

| 출처 | 조성 | Ea (eV) | 방법 | 온도범위 |
|---|---|---|---|---|
| **[Wu26]** | Li5.5PS4.5Cl0.75Br0.75 | **0.32** | EIS Arrhenius | 30–80 °C (6점, **오차 없음**) |
| **[Wu26]** | 위 + Ta0.06 | **0.28** | EIS | 동일 |
| **[Wu26]** | 무도핑 / Ta | **0.14 / 0.13** | ⁷Li SLR T₁ (고온측) | 14.1 T VT-NMR |
| **[Wu26]** | 무도핑 / Ta | **0.59 / 0.35** | **cNEB inter-cage** | 0 K, 단일 배열 |
| **우리** | modelc Li5.4PS4.4Cl1.6 | **0.224** (단일시드) / **0.197 ± 0.032** (3시드) | **MLIP-MD** UMA-s-1p1, MSD 2–50 ps | **600/800/1000 K** |
| **우리** | comp1 Li6PS5Cl | **0.253** (단일시드) | 동일 | 동일 |
| [LiGaF] | Li5.5PS4.5Cl1.5 | 0.28 | EIS | 실험 앵커 |
| [Xu26] | Li5.3PS4.3Cl1.7 → Nd-O | 0.292 → 0.278 | EIS | 실험 앵커 |

**판정**:
- **✅ 실험 EIS 끼리는 잘 맞는다** — [Wu26] 0.32/0.28 ↔ [LiGaF] 0.28 ↔ [Xu26] 0.292/0.278. Cl-rich argyrodite 의 실험 Ea 는 **0.28–0.32 eV 밴드**로 수렴한다.
- **⚠ 우리 MLIP-MD 0.197–0.253 은 실험보다 낮다** — 우리는 **단결정 주기셀·GB 없음**이고 **600 K 이상 외삽**이다. [Famprikis19]·[Fan26] 이 "황화물은 GB 기여가 작다"고 하지만 0.05–0.09 eV 차이는 GB + 온도외삽으로 설명 가능한 폭이다. **직접 대소 비교 금지.**
- **⛔ NEB 0.59 eV 는 어떤 실험값과도 안 맞는다** — 자기 EIS 의 1.8배, 자기 NMR 의 4.2배. 단일 배열 NEB 의 구조적 한계(§4.9)를 그대로 보여준다. **우리가 NEB 를 쓸 때 반드시 배열 앙상블을 돌려야 하는 이유의 외부 사례.**
- **Δ(Ta) 방향은 우리 Cl-rich 결과와 같다**: 치환/무질서 ↑ → Ea ↓, σ ↑. 우리 comp1→modelc 도 Ea 0.253 → 0.224 (−11.7 %), D(600 K) 2.56×. [Wu26] 는 Ea −12.5 %, σ 1.94×. **크기까지 비슷하다** — 다만 우리 건 UMA-MLIP, 저쪽은 EIS 라 **원인 축이 다르다**(우리는 vacancy+disorder, 저쪽은 P→Ta 화학).

### 8.3 ★ 전자전도도 — 논문 자신의 데이터가 논문의 스크리닝 논거를 반박한다

논문 논거: *"넓은 갭 → σ_e 낮음 → 자기방전·덴드라이트 억제"* → 그래서 Ta 선택.
논문 실측: gap **2.12 → 2.66 eV (+0.54)**, σ_e **9.7×10⁻⁹ → 1.4×10⁻⁹ S/cm (6.9× 감소)**.

진성(intrinsic) 캐리어라면 n_i ∝ exp(−E_g/2kT) 이므로:
```
예측 감소 = exp(0.54 / (2 × 0.02585)) = 3.4 × 10⁴ 배
실측 감소 = 6.9 배
```
**4자릿수 차이.** ⇒ **이 재료의 σ_e 는 밴드갭이 아니라 결함/불순물/입계가 지배한다.**

**우리 대조 (`kb/results/MASTER_structure_property_logic_2026_06_21.md` §[E]/[F])**: 우리도 comp1↔modelc 에서 gap 2.066 ≈ 2.099 로 **거의 같은데** 계면 거동은 다르다는 결론에 도달했고, "Cl-rich 가 양극서 더 나쁘다"의 원인에서 **전자전도도를 명시적으로 배제**했다. **[Wu26] 은 우리와 반대 방향(갭을 올려 σ_e 를 잡는다)으로 설계했는데, 자기 실측이 그 인과를 6.9배밖에 지지하지 못한다.** ⇒ **우리 배제 논증의 독립 외부 증거로 인용 가능.**

### 8.4 ICOHP — 크기가 4–10배 다르다, 절대값 이식 금지

| 결합 | [Wu26] Fig. 3k | 우리 LOBSTER (comp1 / modelc) | 비 |
|---|---|---|---|
| P–S | **1.6** (부호 ⚠) | **−5.944 / −6.000** | 3.7× |
| Li–S | −0.62 (P 근처) / −0.17 (Ta 근처) | **−1.592 / −1.717** (전체 평균) | 2.6× |
| Li–S (4d free S²⁻) | — | −2.566 / −2.516 (**불변 anchor**) | — |
| Li–Cl | — | −1.855 / −2.103 | — |
| Ta–S | 0.7 (부호 ⚠) | (없음) | — |

⇒ **적분창·정규화·기저가 다르다.** LOBSTER 여부조차 SI 에 없다. **크기 비교 금지, 같은 논문 안에서의 상대비만 인용 가능.**
**살릴 수 있는 것 하나**: `|Li–S(Ta)| / |Li–S(P)| = 0.27` — "Ta 이웃 S 는 Li 를 3.6배 약하게 잡는다"는 **비율**. 우리 modelc 의 `Li–Cl 4d 초강결합(−2.836)` 논지와 정확히 대칭(그쪽은 강화, 이쪽은 약화)이라 **결합강도-이동도 축**에서 나란히 놓을 수 있다.

### 8.5 ★★ 계면 — 우리 cascade 가 이 논문의 XPS 를 예측한다

우리 `db/properties/cascade_stability_axes.csv` (닫힌계 pseudo-binary, MP GGA/GGA+U) 의 **TaCl₅** 행:

```
0.1667 TaCl5 + 0.8333 Li  →  0.1667 Ta + 0.8333 LiCl        (dE_Li_metal = −930.3 meV/atom)
```

논문 XPS SEI 실측: **금속 Ta⁰ (24.4/22.4 eV) + LiCl (200.3/199.6 eV) + LiBr + Li₂S + Li₃P**.

⇒ **우리 닫힌계 계산이 이 논문의 SEI 주성분을 그대로 맞췄다.** (Ta₂O₅ 경로도 `0.1667 Ta2O5 + 0.8333 Li → 0.1667 Li5TaO5 + 0.1667 Ta` 로 **금속 Ta** 를 낸다.)

그리고 양극쪽:
```
0.2857 Ta2O5 + 0.7143 LiCoO2 → 0.1429 Co3O4 + 0.1429 Li(CoO2)2 + 0.5714 LiTaO3   (dE_LCO = −15.0 meV/atom)
0.8824 LiCoO2 + 0.1176 Li24TaP3(S5Cl3)3 → … + 0.1176 LiTaO3 + 1.059 LiCl + 0.3529 Li3PO4   (2.5 V, grand-potential)
```
⇒ **우리 grand-potential 계면 계산도 2.5 V 에서 LiTaO₃ 를 낸다** — 논문 XPS CEI 와 일치. **그리고 산소를 LiCoO₂ 에서 가져온다는 것까지 반응식이 말해 준다** (§6.6 의 미해결 질문에 우리 데이터가 답을 준다).

**결정적 비대칭 — 우리 `cascade_product_gaps.json` 조회:**

| 산물 | MP band gap (eV) | 어디에 | 판정 |
|---|---|---|---|
| **LiTaO₃** | **2.388** (mp-754345) | **CEI** | ✅ **광폭 절연체 — 부동태로 타당** |
| **Ta (금속)** | **0.0** (mp-42) | **SEI** | ⛔ **금속 — 전자 절연 실패 경로** |
| Ta₂P / TaP | 0.0 / 0.0 | (우리 예측 SEI) | ⛔ 금속 |
| Li₂(TaS₂)₃ / TaS₃ | 0.0 / 0.0 | (Ta₂O₅+LPSCl 경로) | ⛔ 금속 |
| Li₅TaO₅ | 3.902 | (Ta₂O₅+Li 경로) | ✅ 절연 |

⇒ **★ 이 논문의 최대 내부 긴장**: Fig. 1b 의 설계원칙은 *"in situ formed SEI and CEI … characterized by ionic conduction and **electronic insulation**"* 인데, **자기 XPS 가 SEI 안의 금속 Ta⁰ 를 보고한다.** 우리 693 반응 조사에서 **69 % 가 금속 산물**을 낸다는 결과와 정확히 같은 자리다. 논문은 이 Ta⁰ 를 *"Ta species … homogenizing both the potential distribution and the Li-ion flux"* (COMSOL) 로 **긍정적으로** 해석하는데, 그 COMSOL 은 §4.7 대로 입력이 없다.
**우리 판정: CEI 쪽(LiTaO₃) 은 우리 데이터가 지지, SEI 쪽(Ta⁰) 은 우리 데이터가 경고.**

### 8.6 산화창 — 우리 90종 cascade 에서 Ta 는 하위권이다

`db/properties/oxidation_stability_cascade_v2.csv` (grand-potential, MP GGA/GGA+U):

| 도펀트 경로 | ox_V | red_V | window | **90종 중 순위(ox 오름차순)** |
|---|---|---|---|---|
| **TaCl₅** (논문의 실제 전구체) | **1.717** | 1.59 | 0.127 | **4 / 90 (공동 최하위)** |
| **Ta₂O₅** | **2.027** | 1.717 | 0.31 | **29 / 90** |
| Nb₂O₅ | 2.061 | 1.738 | 0.323 | 35 / 90 |
| NbCl₅ | 1.717 | 1.61 | 0.107 | 3 / 90 |
| (pool 중앙값) | 2.14 | — | — | — |
| (pool 최대) | 2.356 | — | — | — |
| **우리 무도핑 기준 (comp1/modelc)** | **2.256** | **1.242** | **1.014** | — |

⇒ **우리 열역학 축에서는 Ta 계열이 산화 onset 을 올리지 못한다 — 오히려 내린다.**

**⚠ 이 대조의 한계를 반드시 같이 적는다**:
1. 우리 cascade 종은 **"UMA champion 조성"** 이고 조성이 다르다. TaCl₅ 종 = `Li24TaP3S15Cl9` ≈ `Li6(P0.75Ta0.25)S3.75Cl2.25` — **Ta 25 %, Cl 2.25** 로 논문(Ta 6 %, Cl 0.75+Br 0.75)과 딴판이다. **숫자 이식 금지, 방향성만.**
   (묘하게도 이 25 % 는 §4.2 에서 추정한 **논문 DFT 셀의 실제 Ta 농도와 같다.**)
2. 우리 축은 **0 압력 grand-potential** = 열역학 창. 논문의 0.1–4.3 V 는 **부동태화된 kinetic 창**. **다른 축이다.**
3. **그리고 이 둘이 충돌하지 않는다는 게 이 논문의 요점이다** — "열역학적으로 불안정하지만 산물이 좋아서 실용창이 넓다"(Fig. 1b). **우리 §B③ (분해량 ≠ 분해산물 품질, [Zuo22]) 과 같은 논리.**

### 8.7 ★ 계면 축 4종과의 대조 (`kb/results/interface_axes_90_2026_08_19.md`, 오늘)

우리 오늘 결과: **ESW ox_V ↔ 계면 ΔE 상관 r ≤ 0.23 (양극 3종 × 전압 5점 15칸 전부)** — **벌크 산화창은 계면 반응성을 예측하지 못한다.**

[Wu26] 의 설계 사슬은 **그보다 한 단계 더 멀다**:
```
벌크 밴드갭(Fig. 2a)  →  도펀트 선택  →  계면 안정성(Fig. 4,5)
    ↑ 우리가 검증 안 한 링크        ↑ 우리가 r ≤ 0.23 으로 부정한 링크보다 더 약함
```
- 우리는 **ox_V → 계면** 이 안 되는 걸 봤다. [Wu26] 은 **gap → 계면** 을 가정한다. gap 은 ox_V 보다도 계면과 멀다 (우리 §[E]/[F]: gap 은 comp1↔modelc 에서 거의 불변인데 계면 반응성은 다르다).
- **그럼에도 [Wu26] 의 계면 결과는 좋다.** 왜? **Ta 라는 원소가 우연히 양극쪽에서 LiTaO₃ 라는 좋은 산물을 만들기 때문**이지, 갭이 넓어서가 아니다. **선택 근거와 성공 원인이 다르다.**
- ⇒ **우리 r ≤ 0.23 판정의 가장 좋은 외부 사례연구다.** 세미나에서 쓸 수 있다: *"밴드갭으로 도펀트를 고른 논문이 성공했는데, 성공 원인은 갭이 아니라 분해산물이었다."*

### 8.8 AIMD 규약 대조 (우리 β 게이트 · 상자크기 · STO/MTO)

| | [Wu26] | 우리 (`lpsocl_beta_registry.json`, `lpsocl_box_size_600K_2026_08_18.md`) |
|---|---|---|
| T | **300 K 단독** | 600/800/1000 K (400/500 K 은 판정 제외) |
| 시간 | 20 ps ("equilibrated") | prod 200 ps + equilib 5 ps |
| 시드 | 1 | 3 (600 K) |
| 곡선 잣대 | ⛔ | **MTO 가 정본** (STO 는 시드산포 8.7배) |
| MSD 창 | ⛔ | 2–50 ps 고정 |
| β 게이트 | ⛔ | β̄ ≥ 0.80 |
| 유한크기 | 검사 안 함 (실제로는 위반 없음, 확산이 없어서) | 자기 MSD 로 MSD@50 vs (d/2)² |
| 상자 효과 | 미검토 | **작은 셀 → 3×3×1 로 D 가 1.65–1.70× 상승** (Welch p≈0.004) |
| D 인용 | 안 뽑음 | 절대값 인용 금지, 비율도 멀티시드만 |
| 힘 계산 | **AIMD (PBE, PREC=Low)** | **MLIP (UMA-s-1p1 omat)** — ⚠ 축이 다르다 |

**직접 교훈**: 우리가 `lpsocl` 600 K 에서 **상자만 3배 키워도 D 가 1.65× 움직이는 것**을 봤다. [Wu26] 은 그 아래 층 — **확산 자체가 없는 영역**에서 정성 그림을 그렸다. **우리 규약이 왜 필요한지의 완벽한 반례**이므로 kb 에 링크한다.

### 8.9 기계적 물성

**해당 없음** — 이 논문에 탄성상수·모듈러스 계산/측정이 **전혀 없다**. 냉간가압 압력(280/350/490 MPa)과 운전압(20/5 MPa)만 있다.
우리 축(`E_VRH` comp1 22.06 → modelc 27.66 GPa, `B₀` 26.23 → 21.71 GPa, C44 +71 %)과 **비교 지점이 없다.** 다만 **파우치 운전압 5 MPa** 는 우리 [Cronau21]/[Doux20] 계열 저압 논의의 실측 앵커로 쓸 수 있다.

---

## 9. Post-processing ★

| 무엇 | 도구 | 수치화/기록 방식 |
|---|---|---|
| 밴드구조·갭 | (미기재; VASP + 후처리 도구 불명) | Fig. S5 밴드플롯 16장 → Fig. 2a 막대 (**broken axis**) |
| Li 이동 장벽 | **cNEB** (climbing image) | Fig. 3g, 이미지 ~11개, 라벨은 보간 saddle 로 보임 |
| AIMD 확산 | **pymatgen-diffusion add-on** (현 `pymatgen-analysis-diffusion`) → `ProbabilityDensityAnalysis` | Fig. 3h 등가면. **isovalue 미기재** ⛔. **MSD/D 안 뽑음** |
| 결합 | **COHP/ICOHP** (LOBSTER 여부 ⛔) | Fig. S11 곡선 4개 + Fig. 3k 막대. **부호규약 붕괴** |
| 전하 | **차전하밀도(CDD)** + **정전퍼텐셜** | Fig. 3j, Fig. S10 (등가면/컬러맵, 값 없음) |
| 구조 지표 | Li(48h)-S₄ 부피 / Li(24g)-S₃ 면적 | Fig. 3l — **x = 0, 0.06 두 점만** |
| ΔS_conf | **해석식** `ΔS = −R(Σx_i ln x_i + Σx_j ln x_j)`, Rietveld 점유율 입력 | Table S8 |
| Rietveld | **GSAS** | Table S1–S7, S9 (R_wp 만, esd ⛔) |
| EXAFS | **Athena / Artemis** (Demeter) | Table S10, k 3–12 Å⁻¹, R 1.3–2.6 Å, k³ 가중, TaCl₅(mp-29831)/TaS₂(mp-10014) 경로 |
| 연속체 | **COMSOL** Allen–Cahn + Nernst–Planck + Poisson | Fig. 5g, Fig. S22, Table S12 (**단일 파라미터 세트**) |
| 계면 열역학 | **⛔ 없음** (hull·grand-potential·pseudo-binary 전무) | — |

---

## 10. 적용 인사이트 (우리 연구에)

### ① ★ "선택 근거"와 "성공 원인"이 다를 수 있다 — 우리 cascade 서사의 핵심 보강재
[Wu26] 은 **벌크 밴드갭**으로 Ta 를 골랐고 성공했다. 그런데 성공의 실제 메커니즘은 **계면 분해산물(LiTaO₃)** 이고, 밴드갭 논거는 자기 σ_e 데이터로 4자릿수 어긋난다(§8.3). **우리 오늘 결과(ox_V ↔ 계면 r ≤ 0.23)의 완벽한 사례연구**다. 세미나 슬라이드 한 장 값어치.

### ② ★ 우리 cascade 가 남의 XPS 를 맞췄다 — 검증 자산
`TaCl₅ + Li → Ta + LiCl`(닫힌계)이 [Wu26] SEI XPS(금속 Ta⁰ + LiCl)와 일치하고, `Ta₂O₅/LCO → LiTaO₃`(grand-potential 2.5 V)가 CEI XPS 와 일치한다. **`cascade_interface_*.jsonl` 의 외부 실험 검증 사례가 하나 늘었다** — [Zuo22] ToF-SIMS, [Sundar25] 에 이은 세 번째.

### ③ ★ 금속 산물 경고를 실물로 확인 — `cascade_product_gaps.json` 의 실전 의미
우리가 "693 반응 중 69 % 가 금속 산물" 이라고 했을 때 그게 실제 셀에서 뭘 뜻하는지 애매했다. **[Wu26] 은 그 금속(Ta⁰)이 SEI 에 실제로 박히는 걸 XPS 로 보여주고, 그것을 "좋은 것"으로 해석한다.** 우리는 이걸 반대로 읽는다: **Ta 도핑은 양극쪽엔 좋고(LiTaO₃ 2.388 eV) 음극쪽엔 위험하다(Ta⁰ 0.0 eV).** ⇒ **비대칭 도핑 / 구배 도핑**이라는 설계 아이디어가 나온다 (우리 Track 후보).

### ④ AIMD 규약 방어선 — 리뷰어 대응 카드
"왜 600 K 부터 도느냐"는 질문에 이제 **정량 반례**로 답할 수 있다: *Angew VIP 논문이 300 K 20 ps 로 확률밀도를 그렸는데, 자기 NEB 장벽으로도 실험 σ 로도 그 궤적 안 hop 기대값이 0.05회 이하다.* (§4.1 검산 2)

### ⑤ Cl 은 4d, Br 은 4a — anti-site 선호 실측 (Table S9)
우리 modelc 의 **4d-Cl anti-site 12.5 %** 모델과 직접 대응. [Wu26] Rietveld 는 Ta 시료에서 4d: Cl 0.56 / S 0.29 / Br 0.15, 4a: Br 0.54 / Cl 0.25 / S 0.21 로 **Cl–4d, Br–4a 분리**를 보여준다. 우리 배열 선택의 실험 근거로 인용 가능.

### ⑥ 실험 앵커 3개 추가
`Li5.5PS4.5Cl0.75Br0.75` **Ea 0.32 eV · σ 6.2 mS/cm(30 °C)** / Ta 치환 **0.28 eV · 12 mS/cm** / **σ_e 9.7e-9 → 1.4e-9 S/cm**. [LiGaF] 0.28, [Xu26] 0.292 와 함께 **Cl-rich 실험 Ea 밴드 0.28–0.32 eV** 를 굳힌다.

---

## 11. ★★ 놓친 부분 / 설정 오류 후보 (1저자 요청 — 별도 절)

> **✅ = 본문·SI·그림에 명시된 실측 · ⚠ = 우리 추정(근거 병기)**

### ① ⚠⚠ Ta DFT 셀이 명목 농도의 4배, 부피가 22배 과대 — **최우선 의심**
- ✅ Fig. S12c: 998 → **1226 Å³ (+22.8 %)**
- ✅ Table S4/S9: 실험 9.874 → 9.908 Å (**+1.03 % 부피**)
- ⚠ 998 Å³ = conventional 셀 1개 = P 4자리 → Fig. S12b 의 Ta–S₄ 1개 ⇒ **x_DFT = 0.25 ≠ 0.06**
- ⚠ 내부모순: Fig. 3l 은 같은 구간 Li 다면체 +1.1 % — Fig. S12c 와 양립 불가
- **파급**: Fig. 3g NEB · Fig. 3h AIMD · Fig. 3k ICOHP · Fig. 3j CDD **전부 이 셀 위에서 계산됐다**
- 🔗 우리 함정 카드: `kb/results/lpsocl_box_size_600K_2026_08_18.md` (상자만 바꿔도 D 1.65×)

### ② ⛔ AIMD 300 K · 20 ps 단독 — 확산 영역 밖
- ✅ SI: "heated 100 K → 300 K over 1 ps, then **equilibrated at the desired temperature for 20 ps**" + Fig. 3h 캡션 "at 300 K"
- ⚠ **production 구간이 따로 선언되지 않았다** — 20 ps 가 전부일 가능성
- ⚠ 검산: 20 ps 안 hop 기대값 **≤ 0.055회** (§4.1) → Fig. 3h 는 확산이 아니라 열진동 번짐
- ⚠ **등가면 isovalue 미기재** + **두 셀 부피 23 % 차이** → 두 패널은 같은 잣대가 아니다
- 🔗 `db/properties/lpsocl_beta_registry.json` (β 게이트·MTO 정본), `kb/results/lpsocl_box_size_600K_2026_08_18.md`

### ③ ⚠ NMR 화학이동 — **그림 색배정과 본문 서술이 반대**
- ✅ 본문: *"the ⁷Li resonance in the Ta⁵⁺-doped sample shifts **up-field to 1.16 ppm**, compared to **1.48 ppm** in the undoped"* + *"³¹P … similar **up-field** shift upon Ta substitution"*
- ✅ Fig. 3i (figure-read, 확대 확인): 범례 **청록 = 무도핑 / 적색 = Ta 도핑**. 인쇄된 숫자 색은 **1.48 ppm = 적색(Ta)**, **1.16 ppm = 청록(무도핑)**; ³¹P 도 **88.1 = 적색(Ta)**, **86.3 = 청록**. 두 패널 모두 적색이 고-ppm(=down-field) 쪽에 있다.
- ⇒ **그림대로면 Ta 도핑이 down-field 이동 = Li 핵 전자밀도 *감소***. 논문 메커니즘(*"increase in electron density at the Li nucleus"* → 정전인력 약화 → 빠름)이 **역방향이 된다.**
- **어느 쪽이 맞는지 논문만으로 판정 불가.** 인용 시 반드시 이 모순을 함께 적을 것.

### ④ ⛔ DFT+U · 스핀 분극 전무 (Fig. 2a 순위표 무효화)
- ✅ SI 계산절에 U·ISPIN 언급 0
- ⚠ Mo 0.001 / W 0.006 / Ce 0.031 eV = **U 없는 d/f 상태의 전형적 붕괴**; Fe(d⁵)·Cr(d³) 은 스핀 없이 계산 불가
- ⚠ Fig. S5 에 스핀분해 밴드 없음 → 비분극 추정

### ⑤ ⚠ `Li_y` 미기재 — 스크리닝 재현 불가
- ✅ Fig. 2a 범례 `Li_yP0.9M0.1S4.5Cl0.75Br0.75` (figure-read), Fig. S5 캡션도 `Li_y`
- ⛔ **M 별 y 값이 어디에도 없다.** M 이 3+~6+ 로 흩어져 있어 y 는 반드시 달라야 하고, y 가 갭을 지배한다

### ⑥ ⚠ k-mesh 2×2×4 — 셀 미기재로 검증 불가, 어느 해석으로도 비정합
§4.3. 게다가 Fig. S5 k-path 가 **삼사정계** → 등방 메시 가정 자체가 성립 안 함

### ⑦ ⚠ COHP 부호규약 붕괴 + Ta–S vs P–S 결론 역전
§4.6. **"Ta–S 가 P–S 보다 강하다" 는 인용 금지.** "Li–S 가 Ta 이웃에서 약하다"만 인용 가능

### ⑧ ⚠ COMSOL 두 케이스의 입력 차이 미기재 → 재현 불가
Table S12 는 파라미터 **1세트**뿐인데 Fig. 5g / Fig. S22 결과가 다르다. §4.7

### ⑨ ⚠ Rietveld 품질 — 무도핑 시료(Table S4)가 비물리적
- ✅ Table S4: 4a 점유합 = 0.21+0.33+0.54 = **1.08**, 4d = 0.39+0.46+0.25 = **1.10** (>1, 불가능)
- ✅ Uiso(Li1) = **1.375 Å²**, Uiso(S2) = **1.722 Å²** (통상 0.02–0.1)
- ✅ Li 총량 = 48×0.48 + 24×0.018 = 23.5/셀 = **5.87 Li/f.u.** vs 명목 5.5
- (대조: Ta 시료 Table S9 는 4a/4d 합이 정확히 1.00 ✓ — 두 정제의 품질이 다르다)
- ⇒ **ΔS_conf 2.08 이 이 점유율에서 나왔다** → 무질서-σ 상관의 기반이 흔들린다

### ⑩ ⚠ 산소 출처 미기재 (LiTaO₃)
전해질에 O 가 없다. §6.6. **우리 반응식이 답을 준다: LiCoO₂/NCM 격자산소.**

### ⑪ ⚠ "room temperature 12 mS/cm" 는 30 °C 값
✅ Fig. 2d 캡션 "at 30 °C". Ea 0.28 eV 로 25 °C 환산 시 **≈10.0 mS/cm** (우리 환산). 초록 표현이 20 % 낙관

### ⑫ ⚠ Fig. S5 에 `In` 패널이 있는데 Fig. 2a 막대에는 없다
figure-read (저해상도라 확신 ~80 %). 계산해 놓고 보고 안 한 원소가 있다면 선택 편향 신호

### ⑬ ⛔ 통계 전무
오차막대 0개, 반복수 0, 유의성 검정 0, 펠릿 밀도 0, EIS 등가회로 0. §4.8
🔗 우리 선례: 단일시드 1.33× 철회 (SEMIFINAL 2026-07-09), `db/properties/lpsocl_beta_registry.json`

### ⑭ ⚠ NEB 라벨 위치 (경미)
Fig. 3g 에서 인쇄된 0.50 / 0.59 eV 가 **실제 찍힌 최고 이미지점(figure-read ≈ 0.47 / 0.52)보다 위**에 있다. cNEB 보간 saddle 이면 정당하나, 이미지 개수·수렴기준(EDIFFG for NEB, SPRING) 미기재라 확인 불가

---

## 12. 인용 가능 문장 (deck / paper 용)

- "Wu et al. reached 12 mS cm⁻¹ at 30 °C in `Li5.5P0.94Ta0.06S4.5Cl0.75Br0.75` by combining Cl/Br mixed-halide disorder (ΔS_conf maximum at Cl0.75Br0.75) with 6 mol% Ta⁵⁺ on the P site." ✅
- "Their measured practical window of 0.1–4.3 V vs Li/Li⁺ is a **passivated, kinetic** window taken from the third CV cycle — the first-cycle anodic decomposition still starts at the OCV of 2.45 V, consistent with the S²⁻-limited thermodynamic onset (our grand-potential value 2.256 V)." ✅
- "XPS resolves an asymmetric Ta interphase: insulating LiTaO₃ at the cathode side and **metallic Ta⁰** at the Li-metal side — a distinction our MP-hull product-gap table reproduces (LiTaO₃ 2.388 eV vs Ta 0.0 eV)." ✅
- "In our 90-species grand-potential cascade, TaCl₅-derived argyrodite sits at the **bottom of the oxidation window (1.717 V, rank 4/90)**; Ta improves the practical window through decomposition-product quality, not through the intrinsic thermodynamic limit." ✅ (조성 차이 명시할 것)
- ⚠ **쓰면 안 되는 문장**: "Ta doping lowers the migration barrier from 0.59 to 0.35 eV" (26 % 팽창 셀 혐의) · "Ta–S is stronger than P–S" (부호규약) · "Ta gives the widest gap among 15 dopants" (U/스핀 부재) · "AIMD shows a percolating 3D Li network" (20 ps @300 K)

---

## 13. 주의 / 한계 (over-claim 방지)

1. **이 논문의 실험은 좋고 계산은 약하다.** 두 층을 같은 신뢰도로 인용하면 안 된다.
2. **σ·Ea 절대값은 소환값** — 우리 MLIP-MD D/Ea 와 절대비교 금지 (힘 계산 축이 다르다: PBE-AIMD vs UMA-MLIP; 그리고 저쪽 Ea 는 EIS).
3. **ICOHP 절대값 이식 절대 금지** (§8.4, 4–10배 차이).
4. **밴드갭 2.12 ≈ 우리 2.099 는 우연** — 둘 다 PBE, 둘 다 단일 배열, 판독법 미기재. "wide-gap insulator" 수준까지만.
5. **"Cl-rich 산화안정" 류 문장은 반드시 축을 붙인다** — 이 논문의 이득은 **B③(계면 산물 품질)** 축이지 **B①(내재 onset)** 이 아니다. B① 은 우리 데이터로는 오히려 하락한다(§8.6).
6. **우리 cascade 조성 ≠ 논문 조성** — Ta 25 %/Cl 2.25 vs Ta 6 %/Cl 0.75+Br 0.75. 방향성만.
7. **성능 비교표(Table S11)는 저자 선별** — 다른 그룹 값의 조건(N/P, 압력, 온도)이 통일돼 있지 않다.
8. **파우치 82.5 mAh / 10×6 cm² = 면적당 1.38 mAh/cm²** — 코인/펠릿 셀(3.0 mAh/cm²)의 절반 이하다. 스케일업 시 로딩이 내려갔다는 뜻.

---

## 14. 기법 용어 미니사전

- **ΔS_conf (configurational entropy)** — 한 결정학적 자리를 여러 종이 나눠 쓸 때의 혼합 엔트로피. `ΔS = −R Σ x_i ln x_i`. 값이 클수록 자리 점유가 무질서하다. 여기선 4a/4d 의 S/Cl/Br 만 센다. **열역학 안정성 지표가 아니라 무질서 정도의 척도**로 쓰였다.
- **SLR NMR (spin-lattice relaxation)** — ⁷Li 핵 스핀이 격자와 에너지를 주고받아 평형으로 돌아가는 속도 `1/T₁`. 이온이 **Larmor 주파수(여기선 ~233 MHz @14.1 T) 근처**로 뛸 때 최대가 된다. 그래서 T₁⁻¹ vs 1/T 는 봉우리를 만들고, **고온측 기울기 = 장거리 이동 Ea**, **저온측 = 국소(케이지 내) 운동**. EIS 와 달리 **입계를 안 본다** — 그래서 이 논문에서 NMR Ea(0.13–0.14) < EIS Ea(0.28–0.32) 다.
- **doublet / intra-cage / inter-cage jump** — argyrodite Li 이동의 3층. 48h–48h 쌍 안 도약(doublet, 가장 빠름) → 4d 주변 케이지 안 회전(intra-cage) → **케이지 사이 건너뛰기(inter-cage, 장거리 전도의 율속)**. 장거리 σ 는 inter-cage 가 정한다.
- **cNEB (climbing-image NEB)** — 초기·최종 구조 사이에 이미지들을 늘어놓고 밴드를 완화하되, 최고점 이미지 하나는 밴드 접선 방향으로 **거꾸로 밀어 올려** 정확한 saddle 을 찾는다. 0 K 단일 경로 값이라 **무질서계에선 배열마다 다르다.**
- **probability density function (AIMD)** — 궤적 전체에서 각 공간 격자점에 Li 가 있었던 빈도. 등가면을 그리면 "Li 가 다니는 길"처럼 보인다. **⚠ 확산이 없어도 열진동만으로 부피가 생긴다** — 그래서 시간척도 검증이 필수다.
- **ICOHP** — COHP(결정 궤도 해밀턴 밀도)를 E_F 까지 적분한 값. 표준 규약에서 **음수 = 결합, 크기 = 결합 세기**. LOBSTER 로 뽑는다. **적분창·기저·정규화가 다르면 크기가 통째로 달라진다** → 논문 간 절대비교 금지.
- **practical / passivated ESW** — CV 를 여러 사이클 돌린 뒤 전류가 잦아든 상태에서 읽는 창. **부동태막이 생긴 뒤의 kinetic 창**이라 열역학 창(grand-potential)보다 **항상 넓다**. 두 값을 같은 표에 넣으려면 축 이름을 반드시 붙인다.
- **DRT (distribution of relaxation times)** — 임피던스를 등가회로 대신 **완화시간 τ 분포**로 푼다. 봉우리 위치(τ)로 벌크/입계/SEI/전하이동을 분리한다. 여기선 R1–R5 5개로 분해했고 R2, R3 을 SEI 로 지정했다.
- **CCD (critical current density)** — 대칭셀에서 전류밀도를 계단식으로 올리며 단락(전압 붕괴)이 나는 지점. **덴드라이트 저항성의 실용 지표.**

---

## 15. 파일 · 그림 경로

- digest: `litdb/papers/wu2026_ta_argyrodite_selfpassivating.md`
- 크로핑 그림 39장 + 색인: `litdb/figures/wu2026_ta_argyrodite_selfpassivating/` (`figures.json`)
- 원본 PDF: `litdb/inbox/58. Wu2026_High-Conductivity_Argyrodite_SelfPassivating.pdf` (+ `58. Sup) …`)
- 대조에 쓴 우리 자료:
  - `litdb/our_dft_baseline.md`
  - `kb/results/interface_axes_90_2026_08_19.md`
  - `kb/results/lpscl_vs_lpscl16_FULL_report_2026_06_17.md`
  - `kb/results/MASTER_structure_property_logic_2026_06_21.md` §[D][E][F]
  - `kb/results/lpsocl_box_size_600K_2026_08_18.md`
  - `db/properties/lpsocl_beta_registry.json`
  - `db/properties/oxidation_stability_cascade_v2.csv`
  - `db/properties/cascade_stability_axes.csv`
  - `db/properties/cascade_interface_{90,li,carbon}.jsonl`
  - `db/properties/cascade_product_gaps.json`
  - `litdb/papers/sundar2025_oxide_coating_screening_lpscl.md`

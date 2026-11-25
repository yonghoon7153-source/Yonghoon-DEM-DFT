# Ionically Conductive Elastic Polymer Binder for Ultrahigh Loading Electrode in High-Energy-Density Lithium Batteries — Dong-Yeob Han et al. (Adv. Mater. 2025)

> slug `han2025_icep_binder_ultrahigh_loading_ncm811` ·
> DOI `10.1002/adma.202506266` · *Adv. Mater.* **2025, 37, 2506266** (issue 42) ·
> type `exp (바인더 합성·전기화학·후분석) + DFT 보조 (결합에너지 4점)` ·
> 접수 2025-04-02 · 개정 2025-06-13 · 온라인 2025-07-07 · © 2025 저자, CC BY-NC ·
> PDF `inbox/83. Han2025_ICEP_Binder_Ultrahigh_Loading_NCM811.pdf` (본문 **15 pp**) ·
> **SI `adma202506266-sup-0001-SuppMat.docx` (Experimental + Computational details + Fig S1–S28 + Table S1–S6) — 전문 확보·정독** ·
> digested `2026-08-29` · 태그 **[외부]** · status ✅
> (본문 15 pp + SI 전문 정독 · 크로핑 **7장 전수 실물 판독** + `Fig. 2g` 고배율 재렌더 5회 — §13)

> elements: Li, Ni, Co, Mn, O, C, H, N, S, F, P
> methods: DFT, XPS, Raman

<!-- 태그 근거 (2026-08-29):
     · elements — Li/Ni/Co/Mn/O = NCM811 양극 및 DFT 슬랩, C/H/N/O/S = ICEP 바인더
       (AN 의 C≡N, AMPS 의 SO₃H·아미드, PEO 의 에터 O), C/H/F = PVDF, P/F/Li = LiPF₆ 전해질
       (FT-IR PF₆⁻ 839 cm⁻¹ · XPS P 2p LiPFₓOᵧ/LiPF₆ · TOF-SIMS PO₂⁻·LiF₂⁻).
     · methods — 계산은 **DFT 하나뿐**(CASTEP, 결합에너지 4점). AIMD·MD·MLIP·NEB·DOS·Bader·COHP 0건.
       실험 쪽에서 목록에 있는 것은 XPS(C 1s·F 1s·P 2p)·Raman(Eg/A1g). ESW 는 넣지 않았다 —
       LSV 는 했지만 grand-potential/ESW 계산이 아니라 실험 전기화학창이다. -->

---

## 0. 이 digest를 읽는 법

이 논문은 **실험 논문**이다. NCM811 양극용 다기능 바인더(ICEP)를 RAFT 로 합성해
**62.4 mg cm⁻² / 12.5 mAh cm⁻²** 초고로딩 전극을 만들고, 이중적층 파우치에서
**377.6 Wh kg_cell⁻¹ / 1016.8 Wh L_cell⁻¹** 를 뽑았다.

**우리가 이 digest 를 만든 이유는 `Fig. 2g` 의 DFT 결합에너지 4점**이고,
그 판정에 필요한 계산 조건은 **본문이 아니라 SI 의 "Computational details" 절**에 있다.
본문 DFT 단락은 두 문장뿐이고 **숫자가 하나도 없다.** 본문만 읽으면 방법 판정이 불가능하다.

**SI 를 확보해 §4 를 확정했다.** 세 가지가 결정됐다:

1. **엔진 = CASTEP (평면파 DFT)** — PFP/Matlantis·M3GNet·CHGNet 같은 범용 NNP 가 **아니다.**
2. **`ICEP_AMPS (−H)` = 탈양성자 음이온이 아니다.** SI `Figure S13` 캡션이 못박는다 —
   *"ICEP_AMPS (-H) indicates **hydrogen transfer** from ICEP_AMPS to the NCM811 (001) surface."*
   H 가 계 안에 남아 있으므로 **조성 보존 · 총전하 0**. 그래서 SI 에 `NELECT`·배경전하·짝이온
   언급이 없는 것이 **정상**이다 — 필요가 없다. **"음이온으로 돌렸나" 라는 질문 자체가 성립하지 않는다.**
3. **남는 진짜 하자는 전하가 아니라 스핀이다** — `spin-polarized` + `U(Ni 6.0 eV)` 를 쓰면서
   **자기 배열(FM/AFM)도, H 이동으로 환원된 TM 의 상태 선택 규칙도 SI 에 한 줄이 없다** (§4.3, §10-①).

> ⚠ **전압 기준**: 전부 **Li/Li⁺** (반쪽셀 Li 금속 대극). In/InLi 환산 불필요.
> ⚠ **에너지밀도 기준 2종**이 섞여 있다 — **424.4 Wh kg⁻¹** = 코인셀·**패키지 제외**(`Fig. 6c`),
> **377.6 Wh kg_cell⁻¹** = 파우치·**패키지 포함**(`Fig. 6j`). 절대 섞지 말 것.

---

## 1. 한 줄 요약

AN(강성·C≡N) / AMPS(이온전도·SO₃H 수소결합) / PEO(유연·Li⁺ 배위) 세 기능을
**하나의 트리블록**([P(AN-co-AMPS)]₂-b-PEO₄₆)에 넣은 ICEP 바인더가,
PVDF 의 반데르발스 접착이 못 버티는 **건조 모세관 응력**을 탄성으로 흡수하고
NCM811 표면에 **≈7 nm 균일 피복**을 만들어 — 62.4 mg cm⁻² 초고로딩 전극을 균열 없이 성립시키고
CEI 를 얇게·균질하게 유지해 **94.6 % (60 cyc)** 유지율과 **377.6 Wh kg_cell⁻¹** 파우치를 냈다.
`Fig. 2g` 의 CASTEP DFT 는 이 서사에 "SO₃H–표면 O 수소결합" 이라는 원자 수준 근거를 붙이는
**보조 4점**이고, 그중 두 점(`(−H)`, `AN`)은 **본문에서 한 번도 언급되지 않는다.**

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저자 | **Dong-Yeob Han**, **Masud**, **Yeongseok Kim** (공동 1저자 3인), Saehyun Kim, Dong Gyu Lee, Junhyeok No, Hee Cheul Choi, Tae Kyung Lee, **Youn Soo Kim\***, **Soojin Park\*** |
| 소속 | POSTECH 화학과 · POSTECH 신소재공학과 · 동국대 의생명공학 · 경상국립대(GNU) 재료공학·융합기술 |
| 저널 | *Advanced Materials* **2025**, 37, 2506266 (본문 15 pp, Fig 6 + Scheme 1 / SI Fig S1–S28 + Table S1–S6) |
| 지원 | NRF (RS-2024-00405905, RS-2025-00554376, RS-2024-00405818) · nano-CT = **포항가속기 PLS-II 7C XNI** |
| 계 | **NCM811 (LiNi₀.₈Co₀.₁Mn₀.₁O₂) / 액체 카보네이트 전해질 / Li 금속** — ⚠ **황화물 전고체가 아니다** |
| 대조군 | **PVDF** 단일 (다른 바인더 대조 없음) |
| 연구유형 | 실험 주도 + **CASTEP DFT 결합에너지 4점** |

---

## 3. 핵심 수치 총정리

### 3.1 DFT (★ 이 digest의 주 관심)

| 모델 | 결합에너지 | PVDF 대비 | 본문 언급 |
|---|---|---|---|
| **ICEP_AN** | **−0.162 eV** | **0.23×** (PVDF보다 **약함**) | ❌ **없음** |
| **ICEP_AMPS** | **−1.819 eV** | 2.59× | 부등호만 ("stronger than PVDF") |
| **ICEP_AMPS (−H)** | **−2.243 eV** | 3.19× | ❌ **없음** (캡션 라벨뿐) |
| **PVDF** | **−0.703 eV** | 1 (기준) | 부등호만 |
| ΔE(AMPS → AMPS(−H)) | **−0.424 eV** | — | ❌ 비교 문장 자체가 없음 |

> ⚠ **네 값 전부 `figure-read ≈`** — `Fig. 2g` 막대 위 인쇄 숫자다.
> **본문에도 SI 본문에도 결합에너지 수치가 하나도 없다.** 본문이 쓰는 것은
> "AMPS > PVDF" **부등호 하나**뿐. 축은 `Binding energy (eV)`, 0.0 → −3.0, 0.5 눈금.

계산 조건 한 줄: **CASTEP · GGA-PBE · spin-polarized · ultrasoft PP · TS vdW · U(Ni 6.0/Co 3.4/Mn 3.9 eV) ·
컷오프 300 eV · 표면 최적화 Γ-only · (001) 8층 5×4 초격자 (32 Ni/4 Co/4 Mn) · 하단 2층 고정 · 진공 >15 Å** (§4)

### 3.2 바인더 필름 (역학·이온)

| 물성 | ICEP-8 | PVDF | 조건 |
|---|---|---|---|
| 파단신율 | **283 %** | 31.8 % | 인장 S-S, **10 mm min⁻¹** (`Fig. 1a`) |
| 인성(toughness) | **601.2 J m⁻³** | 151.8 J m⁻³ | ⚠ 단위 의심(§10-③) |
| 인장 최대응력 | ≈2.6–2.8 MPa (plateau) | ≈8.9 MPa @ ≈25 % | **figure-read** `Fig. 1a` |
| 압입 깊이 | **96.5 nm** | 120.0 nm | 나노압입 0.1 mN (Picodentor HM500) |
| 탄성률 E | **6.03 GPa** | 3.73 GPa | 나노압입 (⚠ §10-④) |
| 경도 H | **0.42 GPa** | 0.34 GPa | 나노압입 |
| 이온전도도 σ | **1.35 × 10⁻⁴ S cm⁻¹** | 0.65 × 10⁻⁴ | ⚠ **전해질 함침막** EIS (§8.2·§10-⑤) |
| Mn²⁺ 포집 | **126 ppm** | 27 ppm | 0.01 M Mn(ClO₄)₂ 침지 6 h, ICP-MS |
| Tg (PEO / P(AN-co-AMPS)) | **−56 / 85.2 °C** | — | DSC 2nd heating, 10 °C min⁻¹ |

조성 변주: **ICEP-5** 신율 212 % / 인성 290.8 · **ICEP-19** 167 % / 481 J m⁻³ → **ICEP-8 최적**.
분자량 ≈100 kDa (GPC, DMF+20 mM LiBr, **PMMA 표준** → 절대값 아님).

### 3.3 전극 (역학·형태)

| 물성 | ICEP-8 양극 | PVDF 양극 |
|---|---|---|
| 압입 깊이 (2.0 mN) | **936.1 nm** | 3345.2 nm |
| 탄성회복률 | **48.0 %** | 35.8 % |
| 탄성률 E | **1.57 GPa** | 0.11 GPa (**14×**) |
| 경도 H | **0.15 GPa** | 0.014 GPa (**11×**) |
| SAICAS cohesion (cutting) | **0.29 N** | 0.07 N |
| SAICAS adhesion (peeling) | **0.27 N** | 0.04 N |
| 바인더 피복 | **균일 ≈7 nm** (TEM) | 불균일·산발 응집 |
| 단면 두께 | ≈230 μm | ≈190 μm (편차 ≈7.3 μm) |

SAICAS: 다이아 블레이드 폭 1 mm, shear 45°, rake 20°, clearance 10°.
전극 조성 **NCM811 : Super P : 바인더 = 92 : 4 : 4** (SI), Al 박, 진공 70 °C 12 h 건조.

### 3.4 전기화학 (반쪽셀 18.8 mg cm⁻²)

| 항목 | ICEP-8 | PVDF |
|---|---|---|
| 초기 방전용량 | **193.8 mAh g⁻¹** | 181.9 |
| 초기 CE | **90.8 %** | 86.2 % |
| 1st 충전 과전압 | **3.77 V** | 3.89 V |
| 0.5C 유지율 | **85.5 % @ 170 cyc** | 28.9 % @ **80** cyc |
| 평균 CE (첫 70 cyc) | 99.8 % | 99.2 % |
| 2C/2C | 153 → **90.0 % @ 120 cyc** | ≈99 → 39.4 % @ 40 cyc |
| R_internal (GITT, 30 cyc 후) | **31.0 Ω** | 57.2 Ω |
| D_Li⁺ 평균 | **0.42 × 10⁻⁷ cm² s⁻¹** | 0.18 × 10⁻⁷ |
| LSV 산화 onset | > 5.0 V | > 5.0 V ⚠ (§10-⑦-4) |

셀 사양(SI): CR2032 · Celgard 2400 · **Li 300 μm** · **1.0 M LiPF₆ EC/EMC/DMC 3:5:2 v/v/v + 5 wt % FEC** ·
2.7–4.2 V · 25 °C · 형성 0.05 C.
율속 (figure-read `Fig. 3b`, 충전 0.2C 고정): 0.2C **197/185** · 0.5C **190/180** ·
1.0C **180/149** · 2.0C **144/96** · 복귀 0.5C **194/176** mAh g⁻¹.

### 3.5 후분석 (계면·구조)

| 항목 | ICEP-8 | PVDF |
|---|---|---|
| Li 음극 위 TM (ICP-MS) | Ni **73.9** / Co 7.1 / Mn 9.2 ppm | Ni **≥500** (축 절단) / Co ≈65 / Mn ≈46 ppm *(figure-read `Fig. 4a`)* |
| CEI 외층 (TOF-SIMS 스퍼터) | 0–43 s | 0–50 s |
| CEI 내층 총 스퍼터 | **≤108 s** | ≤283 s |
| XPS LiPFₓOᵧ/LiPF₆ (P 2p) | **0.24** | 0.79 |
| 암염(rock-salt)층 (STEM) | **≈3.1 nm** | ≈11.3 nm |
| EELS O K ΔE (표면) | ≈10–11 eV *(figure-read)* | ≈3 eV *(figure-read)* — 벌크 양쪽 ≈11–12 eV |
| nano-CT | 균열 거의 없음 | 심한 입자 분쇄·입계균열 |

nano-CT 사양(SI): 시야 **76 μm** / 픽셀 **44 nm** / **900 projections × 0.4 s** / filtered back-projection (Octopus).
Raman: 532 nm Nd:YAG. EELS ΔE 정의: O K pre-edge ≈528 eV ↔ main-edge ≈540 eV.

### 3.6 초고로딩 · 파우치

| 로딩 (mg cm⁻²) | 18.8 | 36.9 | 45.3 | 52.3 | 62.4 |
|---|---|---|---|---|---|
| 면적용량 (mAh cm⁻²) | 3.4 | 6.6 | 8.8 | 10.5 | **12.5** |
| 60 cyc 유지율 (0.1C) | — | — | — | **96.3 %** | **94.6 %** |

- **1 wt % 바인더**: 19.5 / 37.3 / 60.9 mg cm⁻² → **3.91 / 7.47 / 12.3 mAh cm⁻²**
- Li 금속 100 μm ≈ 20 mAh cm⁻² → **N/P 1.6–5.9**
- 코인셀 중량에너지밀도(**패키지 제외**): **424.4 Wh kg⁻¹ @ 62.4 mg cm⁻²**
  ↔ **PVDF 는 31.7 mg cm⁻² 이후 하락, 40.7 에서 균열·박리로 실패**
- **파우치(bi-stack)**: 한 면 코팅 양극 **3.0 × 4.0 cm × 2 장** + 양면 Li 100 μm (3.2 × 4.2 cm) ·
  로딩 **62.5 mg cm⁻² (본문) / 62.7 (SI)** ⚠ · 12.7 mAh cm⁻² · **N/P 1.57** · **E/C 2.5 g Ah⁻¹**
  → **304 mAh** (⚠ `Fig. 6j` 인셋은 **306 mAh**) · **377.6 Wh kg_cell⁻¹ / 1016.8 Wh L_cell⁻¹**
  → 40 cyc 후 **에너지밀도 유지 96.7 %**, 이후 급락 = **Li 금속 열화**(재조립 시험으로 양극 무결 확인)
- 무게 분포 (`Fig. 6h`): 양극 **47.2 %** · 전해질 **25.0 %** · 패키지 **18.6 %** · Li 4.6 % · 집전체 3.5 % · 분리막 1.1 %
- 다층 적층 **추정**(측정 아님, `Table S5`): 10 / 20 / 30 층 → **451.3 / 462.3 / 466.1 Wh kg⁻¹**
- Raman 균일성(4.3 V 완충): PVDF 상단 0.99 / 하단 0.84 (pristine 0.83) ↔ **ICEP-8 상단 0.98 / 하단 0.99**

---

## 4. DFT / 계산 방법 ★★ — **SI 확정판**

### 4.1 세팅 전표 (SI "Computational details" 원문 기반)

| 항목 | 값 | 출처 |
|---|---|---|
| **코드** | **CASTEP** (Clark et al. 2005, *Z. Kristallogr.* **220**, 567) — **평면파 DFT.** PFP/Matlantis·M3GNet·CHGNet 등 **범용 NNP 아님** | SI ref [2] |
| **범함수** | **GGA-PBE** (Perdew–Burke–Ernzerhof 1996) | SI ref [3] |
| **스핀** | **spin-polarized** ✅ (배열 지정은 **없음** — §4.3) | SI |
| **의퍼텐셜/기저** | **ultrasoft pseudopotential** + 평면파 | SI |
| **vdW 보정** | **Tkatchenko–Scheffler** (2009) ✅ | SI ref [4] |
| **최적화기** | **BFGS**, **원자 위치 + 셀 파라미터** 동시 | SI |
| **수렴 기준** | 에너지 **2 × 10⁻⁵ eV/atom** · 힘 **0.05 eV/Å** · 응력 **0.1 GPa** · 변위 **2 × 10⁻³ Å** · SCF **2 × 10⁻⁶ eV/atom** | SI |
| **컷오프** | **300 eV** | SI |
| **k-point** (Monkhorst–Pack) | **LiNiO₂ 단위셀 최적화 6 × 6 × 1** / **NCM811 (001) 표면 기하최적화 1 × 1 × 1 (Γ-only)** | SI ref [5] |
| **DFT+U** | **Ni 6.0 · Co 3.4 · Mn 3.9 eV** (d 오비탈 국소화) | SI ref [6] = Jain et al. 2011 (MP GGA/GGA+U 혼합) |
| **AIMD/MD** | **없음** (0 K 정적 최적화만) | SI 전수 검색 0건 |
| **dipole correction** | **언급 없음** | SI 검색 0건 |
| **자기 배열 (FM/AFM)** | **언급 없음** | SI 검색 0건 |
| **흡착 자세 탐색 절차·시드·오차막대** | **언급 없음** | SI 검색 0건 |
| **총전하/NELECT/jellium/짝이온** | **언급 없음** — 그리고 **필요 없다** (§4.3) | SI 검색 0건 |

**본문 쪽은 여전히 두 문장이 전부다** (원문 §4.2). 본문에는 코드·범함수·U·컷오프가 **하나도 없다.**

### 4.2 결합에너지 정의식 — **SI 식 (5) 원문**

> **SI, Computational details:**
> "The binding energies for system of the NCM811 surface were calculated by following equation (5):
> **Binding energy = E_total − (E_molecule + E_NCM811 surface)**
> where E_total, E_molecule, and E_NCM811 surface are the total energy of the system, **the energy of
> the PVDF, ICEP_AN, or ICEP_AMPS molecule**, and the energy of (001) surface of NCM811, respectively."

⇒ **관례적 분리-참조 흡착에너지**가 맞다 (음수 = 발열 = 유리).
⚠ **기준 분자 목록에 `(−H)` 가 없다** — PVDF / ICEP_AN / ICEP_AMPS **세 개만** 나열된다.
`(−H)` 계에 어느 기준을 썼는지는 SI 가 말하지 않는다 (§4.3-c).
BSSE·ZPE 보정, 면적 정규화는 언급 없음.

**본문 원문(참고)**:
> "To further elucidate the molecular origins of this interfacial behavior, we conducted density
> functional theory (DFT) calculations to investigate the binding interactions between model
> segments of the ICEP and PVDF polymers and the NCM811 surface (Figure S12). The ICEP structure
> was dissected into **two** representative functional blocks, denoted as ICEP_AN and ICEP_AMPS.
> Notably, ICEP_AMPS exhibited a significantly stronger binding affinity to the NCM811 surface
> compared to PVDF, primarily due to robust hydrogen bonding between the sulfonate group and
> surface oxygen atoms (Figure 2g and Figure S13). These DFT calculation results provide direct
> theoretical support for the experimentally observed interfacial adhesion..."

### 4.3 ⭐⭐ `ICEP_AMPS (−H)` 의 전하 상태 — **확정**

#### (a) SI `Figure S13` 캡션 — 결정적 문장 (원문)

> "**Figure S13.** Geometrically optimized structures of ICEP_AN, ICEP_AMPS, ICEP_AMPS (-H), and
> PVDF. **Note that ICEP_AMPS (-H) indicates hydrogen transfer from ICEP_AMPS to the NCM811 (001)
> surface.**"

#### (b) 그래서 각 질문의 답

| 질문 | 답 |
|---|---|
| 총전하 0 인가 −1 인가 | **0 (중성).** H 가 계 밖으로 나간 것이 아니라 **슬랩으로 옮겨갔다** → 조성 보존 |
| jellium / 배경전하 | **쓰지 않았고, 쓸 필요가 없다.** SI 언급 0건이 **정상** |
| NELECT 조정 | 동일 — **불필요** |
| 짝이온(Na⁺·Li⁺) 추가 | **없음 · 불필요** (cf. Kang 2025 는 Na⁺ 짝이온 방식을 택했다 — §7.2) |
| 뗀 H 의 참조상태 (H•, ½H₂, H⁺) | **질문 자체가 성립하지 않는다** — H 를 떼지 않았다 |
| 스핀 / 라디칼 | 계산은 `spin-polarized`. 그러나 **자기 배열·상태 선택 규칙은 없다** → (d) |

**⇒ 초판 판정 철회.** SI 확보 전에 "탈양성자 음이온일 가능성 / 참조가 달라 뺄셈이 성립 안 할 가능성"
을 열어 뒀는데, **`Figure S13` 캡션이 그 가능성을 닫는다.** `(−H)` 는 **화학흡착(양성자 전달) 상태**다.

#### (c) 뺄셈은 정의될 수 있다 — 단 **추론**이다

조성이 보존되므로, SI 식 (5) 의 기준 목록대로 `E_molecule = 온전한 ICEP_AMPS` 를
**양쪽에 똑같이** 쓰면 두 값의 차
`ΔE = −2.243 − (−1.819) = **−0.424 eV**` 는
**흡착 복합체 안에서 술폰산 H 가 표면 O 로 옮겨가는 에너지**가 된다 (음수 = 이동이 유리).

⚠ **단, SI 가 `(−H)` 계의 기준 분자를 명시하지 않았다.** 위는 "식 (5) 를 그대로 적용했을 것"
이라는 **우리 추론**이다. **확정으로 쓰지 말 것.**

#### (d) 🔴 남는 진짜 하자 — **슬랩 자기상태 선택 규칙이 없다**

H 가 표면 O 로 가면 **표면 O–H 가 생기고 TM 하나가 환원된다** (Ni³⁺ → Ni²⁺ 계열).
그런데 SI 는 `spin-polarized` 라고만 쓰고,
- **FM/AFM 배열 지정 없음**
- **환원된 TM 의 국소 스핀/전자 배치 선택 규칙 없음**
- **`(−H)` 와 나머지 셋이 같은 자기 branch 에서 나왔는지 확인 불가**

**우리 규율(`kb/methodology/estimand_before_running_2026_08_28.md`)의 위험 신호 세 개가 전부 켜져 있다** —
열린 껍질 · 자성 기판 · 산화환원 활성. 회신 O 의 문구를 그대로 적용하면,
필요한 것은 "같은 `NUPDOWN` 값" 이 아니라 **같은 state-selection policy** 이고, 그게 없다.
⇒ **−0.424 eV 는 "H 이동 에너지" 라는 이름은 얻었지만, 그 값이 어느 자기상태에서 나왔는지는 미정이다.**

#### (e) 🟠 `(−H)` 만 반응 좌표가 다르다 — 그런데 축이 그걸 말하지 않는다

`Fig. 2g` 의 네 막대 중 **셋(AN·AMPS·PVDF)은 물리흡착/수소결합**이고,
**하나((−H))만 화학흡착(양성자 전달)** 이다. 그런데 축 라벨은 넷 다 `Binding energy (eV)` 이고
막대는 나란히 있다. **독자는 이것을 "결합 세기 순위" 로 읽게 된다.**
같은 축에 두려면 반응 좌표가 다르다는 표시(색·구분선·주석)가 있어야 한다 — 없다.

#### (f) figure-read 로 미리 확인한 것 (SI 와 일치)

SI 를 보기 전 `Fig. 2g` 를 26–30× 로 재렌더해 원자 단위로 읽은 결과는 다음과 같았고,
**`Figure S13` 캡션과 정확히 일치한다.**

| 패널 | SO₃ 위 H | 표면 O 위 H | 점선(H-bond) 방향 |
|---|---|---|---|
| ICEP_AN | — | 없음 | 없음 (분자가 표면에서 떨어져 있다) |
| **ICEP_AMPS** | **있다** (S–O–**H** 온전) | 없음 | H → **아래** 표면 O |
| **ICEP_AMPS (−H)** | **없다** (맨 SO₃) | **있다** (표면 O–H) | 표면 H → **위** 술포네이트 |
| PVDF | — | 없음 | 없음 |

**⇒ 두 경우 모두 본문의 "수소결합" 서술이 맞다.** 이동 전에는 술폰산 O–H 가 주개,
이동 후에는 **표면 O–H 가 주개**이고 술포네이트가 받개다.
(⛔ "(−H) 엔 주개가 없는데 화살표가 있다" 는 초판 지적은 **철회**한다 — 틀렸다.)

### 4.4 AMPS ↔ AMPS(−H) 비교 문장 — **없다**

본문에서 두 값을 직접 비교하는 문장은 **존재하지 않는다.** 본문이 비교하는 유일한 쌍은
**ICEP_AMPS vs PVDF** 다 (§4.2 인용문).
- 본문은 *"dissected into **two** representative functional blocks, denoted as ICEP_AN and
  ICEP_AMPS"* 라고 **둘만** 이름을 댄다. `(−H)` 는 **세 번째 모델인데 본문에 존재하지 않는다.**
- `(-H)` 문자열은 **`Fig. 2g` 막대 라벨 · `Fig. 2` 캡션 · `Figure S13` 캡션** 에만 있다.
- **−2.243 eV 라는 최저값이 본문에서 한 번도 언급되지 않는다.**
- AN 이 PVDF 보다 **약하다**(−0.162 vs −0.703)는 사실도 본문에 없다.

⇒ 이 그림은 **본문 논증에 쓰이지 않은 데이터 2점**을 포함한다.

### 4.5 슬랩 모델 (SI 확정)

| 항목 | 값 |
|---|---|
| 표면 지수 | **(001)** |
| 조성 반영 | Ni : Co : Mn = **8 : 1 : 1** → **32 Ni · 4 Co · 4 Mn** (표면 모델 총 TM 40) |
| 층수 | **8층** |
| 측면 초격자 | **5 × 4** (x, y 축) |
| 고정 | **하단 2층 구속** (`Figure S12` 캡션) |
| 진공 | **> 15 Å** (`Figure S12` 캡션) |
| 리튬화 상태 | **미기재** |
| 종단(termination) 종류·선택 근거 | **미기재** (`termination` 검색 0건) |
| dipole correction | **미기재** |
| 면 선택 근거 | **미기재** |

**★ 우리 산술 — 슬랩이 얼마나 두꺼운가**
TM 40개 ÷ (5 × 4 = 20 사이트/층) = **TM 층 2겹**.
즉 "8층" 은 원자층 수(O–TM–O–Li 를 2회 반복)로 읽어야 앞뒤가 맞는다.
⇒ **TM 이 두 겹뿐인 얇은 슬랩**이고, 그중 **아래 2 원자층이 고정**돼 있다.
`Fig. 2g` 의 그림(위 O 종단 + 아래 Li 열 1줄)과도 정합한다.
격자상수 a ≈ 2.9 Å 기준 측면은 대략 **14 × 12 Å** 급 → **Γ-only 가 아주 넉넉하진 않다**(§10-⑥).

**⚠ (001) 면 선택** (우리 판단, 논문 주장 아님): 층상 R-3m 에서 (001)/(003) 은
**Li 확산 채널이 열리지 않는 basal 면**이다. 접착만 보려면 노출면적이 큰 basal 도 방어 가능하지만,
논문은 같은 그림으로 **Li 접근성·전하이동 kinetics** 서사까지 지지한다고 쓴다.
그 축의 정본 면은 **(104)** (우리 SDCP 가 쓰는 면)다.

### 4.6 MD

**없다.** SI·본문 전수 검색에서 `molecular dynamics`·`AIMD`·`NVT`·`NPT`·`thermostat`·`ensemble`·
`fs`·`ps` **0건**. 계산은 **0 K 정적 기하최적화 4점**이 전부다.

### 4.7 모델 분자 조각 (figure-read)

| 라벨 | 그림에서 읽은 조각 |
|---|---|
| **ICEP_AN** | C≡N 을 가진 **작은 나이트릴 조각**(탄소 2–3개, H 캡). 표면과 접촉·점선 없음 |
| **ICEP_AMPS** | **AMPS 단량체 조각** — `–CH₂–SO₃H` + gem-디메틸 C + 아미드 N–H + C=O 쪽 O |
| **ICEP_AMPS (−H)** | 위와 같은 골격, **SO₃ 의 H 만 표면 O 위로 이동** |
| **PVDF** | **VDF 반복단위 1개를 H 로 캡한 2탄소 조각**(CF₂ 탄소 + CH₃ 로 보임) |
| **PEO** | ⛔ **모델 없음** — 46-량체 중간블록이자 논문이 "Li⁺ 수송" 을 귀속시킨 블록인데 DFT 대상이 아니다 |

---

## 5. Figure set ★

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| Scheme 1 | a) PVDF vs ICEP 양극 모식(입계균열·박리 vs 균일 Li⁺/e⁻ 경로) b) RAFT 합성 4단계 + 기능기 색코딩(SO₃H=녹/아미드=청/CN=적/EO=황) | **기능 분담 그림의 표준 양식** — 우리 SDCP 논문 Scheme 1 템플릿. `x/y = [AN]/[AMPS]` 를 여기서 확정 |
| Fig. 1a | 인장 S-S. PVDF 8.9 MPa @25 % 급격 파단 / ICEP-8 2.7 MPa plateau, 283 % | **"강한 것 ≠ 질긴 것"** 의 교과서 그림. PTFE/PVDF 대비를 이 축으로 그릴 것 |
| Fig. 1b,c | 나노압입 하중-변위(0.1 mN) + E/H 막대 | ⚠ **축이 잘린 2축 막대**(H 축 0.30 시작) — 시각 과장. 따라하지 말 것 |
| Fig. 1d | FT-IR (전해질 침지 전후). O=S=O 1215→1220 / 1037→1042, C–S 626→629, N–H ≈1540 이동 | **SO₃–Li⁺ 상호작용의 진동 지문** — 우리 SDCP operando SO₃Li 주장의 실험 대응 기법 |
| Fig. 1e | 이온전도도 막대 1.35 vs 0.65 ×10⁻⁴ S cm⁻¹ | ⚠ **전해질 함침막** 값이다(SI) — "폴리머 고유 전도도" 로 인용 금지 (§10-⑤) |
| Fig. 1f | Mn²⁺ 포집 126 vs 27 ppm | **TM 킬레이션 정량 프로토콜**(0.01 M Mn(ClO₄)₂ 6 h + ICP-MS) — 그대로 이식 가능 |
| Fig. 2a,d | TEM 피복. PVDF 두껍고 불균일 / ICEP-8 균일 ≈7 nm | **"충분히 얇아야 Li 접근을 안 막는다"** 는 두께 상한 논거의 실물 |
| Fig. 2b,c,e,f | 상면 SEM + 3D 광학프로파일러 (±10 μm) | 전극 균일성 3스케일(nm/μm/mm) 논증 구성 |
| **Fig. 2g** | **★ DFT 결합에너지 4점 + 최적화 구조** (−0.162 / −1.819 / −2.243 / −0.703 eV, NCM811 (001)) | **우리 SDCP E_ads 판정의 문헌 대조군.** `(−H)` = **H 이동 상태**(SI 확정). ⚠ 반응 좌표가 다른 막대를 같은 축에 둠 · AN < PVDF 미언급 — §4·§7·§10 |
| Fig. 2h,i | SAICAS 모식(45°/20°/10°) + cutting/peeling F_h | **접착·응집을 한 장비로 분리 측정** — 우리 바인더 실험 요청 규약 |
| Fig. 2j | 전극 E/H 막대 (1.57/0.15 vs 0.11/0.014 GPa) | DEM 접촉강성 k_n 입력의 실측 앵커 후보 |
| Fig. 3a,b | 0.5C 장기(170 vs 80 cyc) + 율속(0.2–2.0 C) | PVDF 붕괴가 **65 cyc 근처 절벽** — 기계적 붕괴 서명 |
| Fig. 3c | R_internal & D_Li⁺ vs SOC/DOD (GITT) | ⚠ figure-read: **SOC ≈90–95 % 에서 두 곡선이 교차** — 본문의 "consistently higher" 와 어긋남 |
| Fig. 3d | 사후 DRT (1st / 50th), P1–P4 배정 | **DRT 피크 분리(P1′/P1″)로 SEI 불균질을 읽는** 해석 템플릿 |
| Fig. 3e,f | in situ GEIS-DRT 맵 (γ 0–30 Ω s⁻¹, τ 10⁻⁵–10¹ s, 0–2.75 h) | SI: **0.5 C·10 분 간격·10 mA·100 kHz–0.01 Hz** = 단일 충방전 |
| Fig. 4a | Li 음극 위 TM (ICP-MS) — 축 절단(0–100 / 480–500) | ⚠ **PVDF Ni 막대가 잘려 값을 못 읽는다**(≥500 ppm) |
| Fig. 4b,c | TOF-SIMS 깊이 프로파일 (내층 108 vs 283 s) | ⚠ **각 종을 자기 최대로 정규화** → 종 간 세기 비교 불가(본문은 비교함) |
| Fig. 4d | 3D TOF-SIMS 재구성 6종 × 2 | 같은 컬러스케일이라 이쪽이 세기 비교의 정본 |
| Fig. 5a,b | nano-CT 3D + XY TXM (스케일바 10 μm) | ⚠ 3D 렌더는 두 시료가 비슷해 보인다 — 차이는 2D 슬라이스에서만 선명 |
| Fig. 5c,d | STEM + FFT. 암염층 11.3 vs 3.1 nm | 표면 상전이 두께 정량 제시법(FFT A=rock-salt (111)/(200), B=layered (003)/(101)) |
| Fig. 5e,f | EELS O K + Co L/Ni L₃,L₂, 표면(0 nm)→벌크(20 nm) | ⚠ PVDF 표면 O K 가 거의 무특징인데 ΔE 를 읽음 (§10-⑧) |
| Fig. 6a,b | 로딩별 충방전 + 문헌 대비 면적용량 지도 | **"상용 양극" 음영(≤20 mg cm⁻², ≤4 mAh cm⁻²)** = 우리 원고에도 쓸 기준선 |
| Fig. 6c | 에너지밀도 vs 로딩 (**패키지 제외**) + 전극 사진 | ⚠ 424.4 는 코인셀·패키지 제외. 377.6 과 섞지 말 것 |
| Fig. 6d,e,f | 단면 SEM(100 μm) + Raman Eg/A1g 상/하단 | ⚠ 상단 스펙트럼이 거의 평평한데 비율 0.98/0.99 인용 |
| Fig. 6g | 로딩별 60 cyc (96.3 / 94.6 %) | 초고로딩 유지율의 정본 |
| Fig. 6h | 파우치 무게 파이 (양극 47.2 / 전해질 25.0 / 패키지 18.6 %) | **셀 수준 무게 회계**의 좋은 예 — 우리 ASSB 파우치 추정에 양식 이식 |
| Fig. 6i | 에너지밀도 vs 적층수, 문헌 S19–S26 | ⚠ **451–466 Wh kg⁻¹ 세 점은 속 빈 별 = 추정치** |
| Fig. 6j | 파우치 40 cyc 유지 96.7 % + 셀 모식 | ⚠ 인셋 **306 mAh** ↔ 본문 **304 mAh** |
| Fig. S12 | **DFT 모델 계** — "The bottom two layers are constrained. The vacuum spacing is over 15 Å." | 슬랩 사양의 유일한 출처(§4.5) |
| **Fig. S13** | **★ 최적화 구조 4종 + 결정적 주석** — "ICEP_AMPS (-H) indicates **hydrogen transfer** from ICEP_AMPS to the NCM811 (001) surface." | **`(−H)` 의 정의를 확정하는 유일한 문장**(§4.3) |
| Fig. S9 | 필름 σ 산출용 Nyquist + 표(직경·두께·R_b·σ) | σ 산출 절차 |
| Table S1 | ICEP 3종 합성·분자정보 | 조성 x/y |
| Table S2 | 문헌 바인더 전기화학 비교표 | `Fig. 6b` 의 출처 |
| Table S3 | 코인셀 에너지밀도 계산(패키지 제외) 상세 | 424.4 의 근거 |
| Table S5 | 다층 적층 에너지밀도 **추정** | `Fig. 6i` 속 빈 별의 근거 |

---

## 6. Post-processing / 분석 기법

**계산 쪽 후처리: 없다.** DOS·PDOS·Bader·Mulliken 전하·COHP·전하밀도차·ELF·NEB — SI 에도 0건.
결합에너지 4개와 구조 그림이 전부이고, **"왜 수소결합인가" 의 정량 근거(결합거리·전하이동·
결합차수)가 하나도 제시되지 않는다.** 그림의 파란 점선이 유일한 근거다.
`(−H)` 에서 **어느 TM 이 환원됐는지**를 보여줄 수 있는 양(자기모멘트·PDOS·Bader)이 전부 빠져 있다.

**실험 쪽 기법 카탈로그** (SI 기준 — 우리가 요청서 쓸 때 그대로 쓸 수 있게):

| 기법 | 장비 / 조건 (SI) | 무엇을 뽑았나 |
|---|---|---|
| GPC | Waters e2695, Styragel HR-4/5/6-DMF, **DMF + 20 mM LiBr, PMMA 표준** | Mw ≈100 kDa (**상대값**) |
| ¹H NMR | Bruker Avance 400, DMSO-d₆ | 조성비 |
| TGA / DSC | Scinco TGA-N-1000 / PerkinElmer DSC-4000, 10 °C min⁻¹, **2nd heating** | Tg 2개 |
| AFM | Jupiter XR, tapping phase | 상분리 도메인 |
| 인장 | DA-01 (Petrol LAB), **10 mm min⁻¹** | 신율·인성 |
| 나노압입 | Picodentor HM500 BASIC, **0.1 mN(필름) / 2.0 mN(전극)** | E, H, 깊이, 탄성회복 |
| FT-IR | Cary 600 | 밴드 이동 |
| ⁷Li NMR | (본문) d-DMSO | **0.00 → +0.05 ppm** |
| EIS (필름 σ) | VSP-300, 10 mV, 100 kHz–0.1 Hz, `SS‖필름‖SS` + **1 M LiPF₆ 전해질 100 μL 주입** | 식 (1) σ = L/(R_b A) |
| 전극 σ_e | SS 블로킹, **정전류 5 mA** | 식 (2) |
| ICP-MS | Thermo iCAP 6000 | Mn 포집 · Li 위 TM |
| SAICAS | SAICAS EN-EX (Daipla Wintes) | cohesion / adhesion |
| LSV | **3.0 → 5.0 V** (⚠ 본문은 3.0–6.0 V) | 산화 창 |
| GITT | 펄스 **0.1 A g⁻¹ 5 min** + 휴지 **30 min**, Weppner–Huggins 식 (3), V_M 20.33 cm³ mol⁻¹, M_B 97.28 g mol⁻¹ | D_Li⁺ · 식 (4) R_internal |
| in situ GEIS | **0.5 C**, 10 분마다, 10 mA, 100 kHz–0.01 Hz, 2채널 | DRT 맵 |
| TOF-SIMS | TOF-SIMS 5 (ION TOF) | CEI 두께·조성 |
| XPS | Thermo K-Alpha | **LiPFₓOᵧ/LiPF₆** |
| nano-CT | **PLS-II 7C XNI**, FOV 76 μm / 44 nm px, **900 proj × 0.4 s**, FBP (Octopus) | 입자 균열 3D |
| STEM-EELS | JEM ARM 200F, FIB(Helios 5 CX) 시편 | 암염층 · O K ΔE · Ni L₃/L₂ |
| Raman | WITec alpha 300R, **532 nm Nd:YAG** | Eg(440)/A₁g(530) |

---

## 7. 우리 계 대비 (`our_dft_baseline.md`)

### 7.1 물성 4축 — **전부 축 밖**

| 축 | 우리 (comp1 / modelc) | 이 논문 | 판정 |
|---|---|---|---|
| A 이온전도 | σ, Ea, D (황화물 벌크, MLIP-MD) | 바인더 **전해질 함침막** σ 1.35×10⁻⁴ S cm⁻¹ | ⛔ 다른 물질·다른 계 |
| B 산화안정 | grand-potential onset **2.256 V** (S²⁻-limited) | **LSV onset > 5.0 V** (액체 전해질 중 폴리머) | ⛔ 낱말만 같다 |
| C 기계 | E_VRH 22.06 / 27.66 GPa (SE 결정) | 바인더 필름 6.03 GPa · 전극 1.57 GPa | ⛔ 대상이 다르다 |
| D 전자구조 | gap 2.066 / 2.099 eV (PBE, fixed-occ) | **밴드 계산 없음** | — |

⇒ **`comparison_vs_ours.md` 의 A–D 표에는 수치 행을 만들지 않는다.**
([Jun26] `jun2026_ppma_econductive_binder_si_lowpressure_assb` 와 같은 취급.)

### 7.2 ★ 진짜 접점 — **바인더 흡착에너지의 전하 상태 처리**

우리 SDCP 프로그램은 **-SO₃ ↔ 층상 산화물 표면** 앵커링을 정확히 같은 양으로 재고 있다.

| 항목 | **Han 2025 (ICEP)** | **우리 SDCP** |
|---|---|---|
| 앵커 화학 | **SO₃H ↔ 표면 O 수소결합** (그리고 H 이동 상태) | **SO₃ ↔ 표면 Li 배위** (O···Li 2.09 Å) |
| 표면 | **NCM811 (001)**, 8층, 5×4, TM 2겹 | **LiNiO₂ (104)** |
| 코드/범함수 | **CASTEP · PBE · USPP · TS-vdW · U(6.0/3.4/3.9)** | **VASP PAW** (+ UMA MLIP 사전탐색) |
| 중성형 값 | **−1.819 eV** (AMPS) *(figure-read)* | **−0.7675 eV** (Li-top, pm1, box24) |
| 불소계 대조군 | **PVDF 조각 −0.703 eV** | **PTFE C₁₀F₂₂ −0.4124 eV** |
| 하전/변형 상태 | **H 이동(중성 유지)** — `(−H)` | **자가도핑 라디칼/폴라론** — `sdcp_doped` |
| 상태 선언 | ❌ 본문에 `(−H)` 자체가 없다 | ✅ `db/properties/sdcp_doped_closed_2026_08_28.json` 로 **명시적으로 마감** |
| 자세 산포·상자 수렴 | ❌ 없음 | ✅ 자세 4종 14.6 meV · box20↔24 0.32 meV |

⛔ **절대값을 나란히 놓지 않는다** — 면(001 vs 104)·코드·의퍼텐셜·U·조각 크기가 전부 다르다.
⭕ 구조적으로 같은 것은 **"불소계 대조군 대비 술폰산이 더 깊다"** 는 부호 방향 하나뿐이다.

**세 줄 요약**
1. **정당화가 아니라 대조군이다.** "Adv. Mater. 도 상태 선언 없이 실었으니 우리도" 가 아니라,
   우리 estimand 규율이 **문헌 관행보다 엄격하다**는 실증이다.
2. **그들이 우리보다 나은 점 하나** — **양성자 전달(해리흡착) 상태를 실제로 계산했다.**
   우리 neutral 계산은 `SO₃H` 온전한 상태만 본다. **표면 O 로의 H 이동 자세를 우리 자세 목록에
   추가**하면 "operando SO₃Li"(H↔Li 교환) 주장의 **0 K 전단계**가 생긴다.
   ⚠ 단 그때는 **참조·전하·스핀 규약을 estimand 카드에 먼저 적고** 들어가야 한다.
3. **우리가 아직 없는 양**: `(−H)` 막대는 우리 `U_PCET`(양성자-결합 전자이동)의
   **산화물 슬랩 버전**에 해당한다. 우리에겐 그게 없다 → `comparison_vs_ours.md` 에
   "우리가 만들어야 할 것" 으로 등록했다.

> 문헌-대-문헌 비교(**[Kang25]** `papers/kang2025_bollard_anchored_binder_dry_electrode.md` 의 **Na⁺ 짝이온** 방식
> vs 이 논문의 **H 이동** 방식)와 우리 쪽 해석 전문은 **`comparison_vs_ours.md` 의 🧲 바인더 흡착 전하상태 note** 와
> `kb/syntheses/binder_adsorption_charge_state_2026_08_29.md` 로 보냈다.
> ⚠ [Kang25] 는 **DFT 가 아니라 PFP/Matlantis 범용 NNP** 다 — 두 논문의 값을 같은 축에 두지 말 것.

### 7.3 부수 접점

- **LSV > 5.0 V**: 폴리머 두 종이 같은 onset. **우리 ESW 축과 무관**. ⛔ 2.256 V 와 같은 표에 두지 말 것.
- **전극 탄성률 1.57 / 0.11 GPa**: DEM 접촉강성 `k_n` 의 복합전극 스케일 앵커 후보(나노압입값 주의).
- **Mn²⁺ 킬레이션 프로토콜**: 우리 SDCP 가 "TM 용출 억제" 를 주장한다면 그대로 이식 가능.
- **⁷Li NMR +0.05 ppm**: 우리 "SO₃–Li⁺ 배위" 주장의 저비용 실험 검증 경로.

---

## 8. 결과 — 섹션별 상세

### 8.1 설계·합성 (Scheme 1, Fig. S1–S6, Table S1)

**설계 논리**: 고전 열가소성 엘라스토머(PS-b-PI-b-PS)의 하드-소프트-하드 구도에 **이온 기능**을 얹는다.
- **AN** — 극성 C≡N → 기계 강건성 + 활물질 친화
- **AMPS** — **SO₃H** 로 Li⁺ 전도 + 양극과 수소결합
- **EO (PEO₄₆)** — 에터 O 를 따라 Li⁺ 이동, 유연성

**구조**: `[P(AN-co-AMPS)]₂-b-PEO₄₆`. Scheme 1b 에서 **AN 이 x, AMPS 가 y** →
**ICEP-8 은 AN : AMPS ≈ 8 : 1** (§10-② 에서 중요해진다).

**합성** (본문 Scheme 1b + SI):
RAFT 제 합성 → PEG 와 에스터화 → **PEO₄₆-MCTA** (이관능 macro-CTA) →
`PEO₄₆-MCTA 200 mg (0.071 mmol) + ACVA 7.9 mg (0.028 mmol) + AMPS 2094 mg (14.2 mmol)
+ AN 9.29 mL (142 mmol) + 무수 DMSO 38 mL`, Ar, **80 °C 22 h** (⚠ Scheme 은 20 h),
에틸아세테이트 침전 → 진공 50 °C 건조 → **≈4.1 g**.
⇒ **투입 몰비 AN : AMPS = 142 : 14.2 = 10 : 1**.

**DSC 가 선택을 결정한다**: ICEP-8 만 PEO Tg −56 °C 로 가장 낮고 **PEO 결정성 완전 억제**.
ICEP-5(−18 °C)·ICEP-19(−25 °C)는 부분 결정성. AFM: ICEP-8 이 **뚜렷한 공연속 상분리**.

### 8.2 필름 물성 (Fig. 1)

**인장**: ICEP-8 **283 % / 601.2 J m⁻³** vs PVDF **31.8 % / 151.8 J m⁻³**.
조성 변주에서 신율과 인성이 **같이 가지 않는다** — ICEP-5 는 신율 212 %/인성 290.8
(이온 클러스터링이 기지를 굳히고 상분리 불량), ICEP-19 는 167 %/481 (AN 유리질이 강성).

> **figure-read 주의**: `Fig. 1a` 에서 **PVDF 의 최대응력이 3배 이상 높다**(8.9 vs 2.8 MPa).
> "ICEP 가 더 강하다" 가 아니라 "**더 질기다**" 이다.

**나노압입**: 0.1 mN 정하중, 96.5 vs 120.0 nm, E 6.03 vs 3.73 GPa, H 0.42 vs 0.34 GPa.

**전해질 상호작용** (`Fig. 1d`, S7–S8): 침지 후 1803 / 1774 cm⁻¹(카보네이트), 839 cm⁻¹(PF₆⁻).
**N–H ≈1540 cm⁻¹ 고파수 이동**, **O=S=O 1215→1220, 1037→1042**, **C–S 626→629**.
⁷Li NMR: LiPF₆ 단독 0.00 → ICEP-8 첨가 **+0.05 ppm** = Li⁺–술포네이트 배위.

**σ** (`Fig. 1e`, S9): **1.35 vs 0.65 ×10⁻⁴ S cm⁻¹**.
🔑 **SI 가 결정적 조건을 알려준다** — 필름을 Al 박에 캐스팅→70 °C 진공 12 h 건조 후
`SS‖필름‖SS` 로 조립하고 **측정 전 1 M LiPF₆ EC/EMC/DMC/FEC 전해질 100 μL 를 주입**한다.
⇒ 이 값은 **건조 폴리머의 고유 이온전도도가 아니라 전해질 함침막의 유효 전도도**다.
그래서 PVDF 가 10⁻⁴ 대를 내는 것이 물리적으로 **정상**이고(기공·팽윤 상의 액상 전해질 기여),
두 값의 차이에는 **팽윤도·기공률 차이가 섞여 있다**(§10-⑤).

**TM 킬레이션** (`Fig. 1f`): 0.01 M Mn(ClO₄)₂ 6 h → **126 vs 27 ppm**.

### 8.3 전극 다중스케일 균일성 (Fig. 2a–f, S10–S11)

- **nm (TEM)**: ICEP-8 **균일·연속 ≈7 nm** / PVDF 두껍고 산발적. 두께 논거가 양방향
  (덮되(보호) 얇아야(Li 접근)).
- **μm (SEM)**: ICEP-8 균일 분산 / PVDF 응집. 두께 ≈230 vs ≈190 μm, PVDF 는 지점 간 ≈7.3 μm 편차.
- **mm (3D 광학프로파일러)**: 1.0 × 1.0 mm 에서 ICEP-8 의 높이 편차가 훨씬 작다.
- **전자전도도**(Fig. S11, 5 mA 정전류 + 식 (2)): 같은 조성비에서 ICEP-8 양극이 더 높다.

### 8.4 DFT (Fig. 2g, S12, S13) — §4 참조

논증 구조: *분산이 좋다(실험) → 왜? → 수소결합(DFT) → 그래서 접착·응집이 세다(SAICAS)*.
DFT 는 **중간 고리 하나**를 담당하는데, 본문은 그 고리에서 **4점 중 2점만 쓰고**
(AMPS, PVDF), 나머지 2점(AN, `(−H)`)은 언급조차 하지 않는다.

### 8.5 접착·응집 (Fig. 2h–j, S14)

**SAICAS**: cutting = 전극 내부 **응집**, peeling = 집전체와의 **접착**.
- ICEP-8 **0.29 / 0.27 N** vs PVDF **0.07 / 0.04 N** (4× / 7×)
- figure-read `Fig. 2i`: ICEP-8 의 cutting F_h 가 깊이 0→80 % 에서 **0 → 0.45 N 증가**(진동 큼),
  PVDF 는 **전 깊이 0.07–0.10 N 평탄**.
- 전극 나노압입(2.0 mN): 936 vs 3345 nm, 탄성회복 48.0 vs 35.8 %,
  E 1.57 vs 0.11 GPa, H 0.15 vs 0.014 GPa.

### 8.6 전기화학·수송 (Fig. 3, S15–S19)

- **LSV**: 본문 *"from 3.0 to 6.0 V ... onset of oxidative current increase above 5.0 V"*
  ↔ **SI: "scanning from 3.0 V to 5.0 V"**. ⚠ 두 서술이 어긋난다(§10-⑦-4).
- 반쪽셀: 193.8 mAh g⁻¹ / ICE 90.8 % vs 181.9 / 86.2 %. **1st 과전압 3.77 vs 3.89 V**.
- **0.5C 장기**: ICEP-8 85.5 % @170 cyc. PVDF 는 **≈65 사이클에서 절벽**처럼 무너져 80 cyc 에 28.9 %.
  → 붕괴 형상 자체가 **점진적 화학 열화가 아니라 기계적 붕괴**의 서명.
- **2C/2C**: PVDF ≈99 → 39.4 % @40 cyc / ICEP-8 153 → **90.0 % @120 cyc**.
- **GITT**: R_internal 31.0 vs 57.2 Ω, D_Li⁺ 0.42 vs 0.18 ×10⁻⁷ cm² s⁻¹.
- **DRT** (`Fig. 3d`): 1st 사이클에 P1–P4 (계면반응 / 계면+전하이동 / 전하이동 / 전하이동+고체확산).
  50 cyc 후 **PVDF 의 P1 이 P1′·P1″ 로 분리** = SEI 이질·불안정 성장.
  figure-read: P4 세기 1st **255 vs 355 Ω**, 50th **55 vs 130 Ω**.
- **in situ GEIS-DRT** (`Fig. 3e,f`): PVDF 맵은 R_SEI·R_ct 대역에 **붉은 띠**, ICEP-8 은 거의 전면 파랑.
  낮은 SOC·높은 DOD 의 높은 R_ct 는 **공공 부족**(고리튬화 상에서 Li 이동도 낮음).

### 8.7 계면·구조 안정성 (Fig. 4, 5, S20–S22)

- **ICP-MS**: ICEP-8 쪽 Li 음극에 Ni 73.9 / Co 7.1 / Mn 9.2 ppm. PVDF 는 Ni **≥500 ppm**(축 절단).
  본문은 73.9 ppm 을 "그래도 용출은 일어난다" 는 정직한 단서로 쓴다.
- **TOF-SIMS**: 두 양극 모두 **이중층 CEI** — 바깥층(금속 유래, PVDF 0–50 s / ICEP-8 0–43 s),
  안쪽층(전해질 분해종). **내층 총 스퍼터 108 vs 283 s**.
  **MnF₂⁻ > NiF₂⁻ 역설** → Mn 이 불화물을 더 잘 만들고 이온화 효율이 높으며 Ni 는 NiO 로 간다.
- **XPS**: **P 2p 의 LiPFₓOᵧ/LiPF₆ = 0.24 vs 0.79**.
- **nano-CT**: PVDF 는 심한 분쇄·미세균열, ICEP-8 은 형태 보존 (단면 SEM Fig. S21 교차 확인).
- **STEM/FFT**: 표면 암염상 **11.3 vs 3.1 nm**.
- **EELS**: O K ΔE 가 ICEP-8 에서 유지 → Ni⁴⁺ 환원 억제. pre-edge 가 더 얕은 깊이 → 산소 손실 적음.
  Ni L₃/L₂ 가 표면→벌크로 더 가파르게 감소 → **Ni²⁺ 의 Li 층 침입 억제**.
- **dQ/dV**: PVDF 는 **3.65 V(H1→M)** 피크 크게 이동, ICEP-8 은 거의 고정.

### 8.8 초고로딩·파우치 (Fig. 6, S23–S28, Table S2–S6)

- 로딩 5수준 → 면적용량 선형 증가, 최고 **62.4 mg cm⁻² / 12.5 mAh cm⁻²** (단면 SEM 에 공극·균열 없음).
- **1 wt % 바인더**로도 3.91 / 7.47 / 12.3 mAh cm⁻².
- **에너지밀도 vs 로딩** (`Fig. 6c`, 패키지 제외, `Table S3`): ICEP-8 은 **424.4 Wh kg⁻¹** 포화.
  PVDF 는 31.7 mg cm⁻² 이후 하락, 40.7 에서 균열·박리(사진 인셋에 갈라진 전극).
- **Raman 두께방향 균일성**: PVDF 상단 0.99 / 하단 0.84 (pristine 0.83) → 집전체 근처 탈리튬 부족.
  ICEP-8 상단 0.98 / 하단 0.99 → 균일.
- **로딩별 60 cyc**(0.1C): 52.3 → 96.3 %, 62.4 → 94.6 %. PVDF 는 37.3 mg cm⁻² 에서도 54.7 %.
- **파우치**: bi-stack (한 면 코팅 3.0×4.0 cm × 2 + 양면 Li 100 μm 3.2×4.2 cm),
  **N/P 1.57**, **E/C 2.5 g Ah⁻¹** → 304 mAh, **377.6 Wh kg_cell⁻¹ / 1016.8 Wh L_cell⁻¹**, 96.7 % @40 cyc.
- **40 cyc 이후 급락은 양극이 아니라 Li 금속**: 해체→ICEP-8 양극만 세척→**새 Li·새 전해질로 재조립하니
  용량 유지**(Fig. S28). 원인 귀속 실험이 깔끔하다.
  결론: 고면적용량 + 희박전해질(E/C 2.5) 에서 카보네이트계는 불안정 SEI → **고전압 에터계 필요**.
- **다층 추정**: 10 / 20 / 30 층 → 451.3 / 462.3 / 466.1 Wh kg⁻¹ (**계산값**, `Table S5`).

---

## 9. 논증 흐름

```
후막 전극의 두 실패
  ① 건조 중 모세관 응력 → 바인더 이동(segregation) + 균열/박리
  ② 두께방향 Li⁺ 경로 부족 → 하단 미반응 → 유효용량 손실
        │
        ▼
바인더 3조건: 탄성 · 강한 접착(수소결합) · 이온전도
        │
        ▼
설계: [P(AN-co-AMPS)]₂-b-PEO₄₆ , x/y 로 튜닝 → ICEP-8
        │
        ├── 필름: 신율 283 % · 인성 4× · σ 2× · Mn 포집 4.7×
        │
        ├── 전극: ≈7 nm 균일 피복 → 3스케일 균일성 → 응집 4× / 접착 7×
        │        └── [DFT] "왜 균일한가" = SO₃H↔표면 O 수소결합 (Fig. 2g)   ← ★ 약한 고리
        │
        ├── 전기화학: R↓ · D_Li⁺ 2× · DRT 단일 R_SEI · 과전압 0.12 V↓
        │
        ├── 계면/구조: CEI 내층 2.6× 얇음 · 염분해 1/3 · TM 용출 ≥7× 감소
        │              암염층 11.3 → 3.1 nm · O K ΔE 유지 · 균열 소멸
        │
        └── 초고로딩: 62.4 mg cm⁻² → 424.4 Wh kg⁻¹(코인, 패키지 제외)
                     → 파우치 377.6 Wh kg_cell⁻¹ (남은 한계 = Li 금속)
```

**가장 약한 마디**: *"수소결합이 세다(DFT) → 그래서 분산이 균일하다"*.
DFT 는 **단분자 × 0 K × 진공 × 자세 1개**이고, 분산 균일성은
**슬러리 레올로지 × 건조 동역학 × μm 스케일**이다. 이 간극을 논문은 언급하지 않는다.

---

## 10. 비판 (⚠ 이 논문의 약점)

### ① 🔴 **상태 선택 규칙(state-selection policy)이 없다** — 가장 큰 하자
SI 는 `spin-polarized` 라고 쓰고 **U(Ni 6.0 eV)** 를 켠다. 그런데 `(−H)` 는
**H 가 표면으로 가면서 TM 하나를 환원시키는** 계다.
- **자기 배열(FM/AFM) 지정 없음**
- **환원된 TM 의 국소 스핀 선택 규칙 없음**
- **네 계가 같은 자기 branch 에서 나왔는지 확인 불가**

우리 규율의 위험 신호 3개(열린 껍질 · 자성 기판 · 산화환원 활성)가 전부 켜져 있고,
회신 O 의 문구대로 필요한 것은 "같은 U/NUPDOWN 값" 이 아니라 **같은 state-selection policy** 다.
⇒ **−0.424 eV 는 이름은 얻었지만(H 이동 에너지) 어느 상태에서 나왔는지는 미정이다.**

### ② 🔴 **조성 가중을 하면 결론이 뒤집힐 수 있다** (우리 산술, 논문 주장 아님)
- ICEP-8 = **AN : AMPS ≈ 8 : 1** (Scheme 1b, x/y ≈ 8; SI 투입비는 10 : 1).
- **AN 의 결합에너지 −0.162 eV 는 PVDF(−0.703)의 0.23배로 오히려 약하다.**
- 단순 조성 가중: `(8×(−0.162) + 1×(−1.819)) / 9 = **−0.347 eV/단위**` < PVDF **−0.703 eV/단위**.
- ⇒ **반복단위당으로 보면 ICEP-8 이 PVDF 보다 약하게 붙는다**는 계산이 나온다.
- 논문은 **AMPS 하나만 PVDF 와 비교**하고, AN 이 더 약하다는 사실을 본문에서 언급하지 않는다.
- ⚠ 한계도 정직하게: 흡착은 가법적이지 않고, 실제 접착은 **다가 접촉**이며 PEO 는 모델조차 없다.
  그러나 **논문 쪽에 이 반론이 아예 없다.**
- ⇒ **"ICEP 가 PVDF 보다 강하게 붙는다" 를 `Fig. 2g` 로 인용하면 안 된다.**
  인용 가능한 것은 **"AMPS 단위가 PVDF 단위보다 강하게 붙는다"** 까지.

### ③ ⚠ 인성 단위가 물리적으로 맞지 않는다
`Fig. 1a` 곡선을 적분하면 ICEP-8 ≈ 2.3 MPa × 2.83 ≈ **수 MJ m⁻³**.
논문 값 **601.2 J m⁻³** 은 3–4 자릿수 작다. 비(601.2/151.8 = 3.96)는 곡선과 정합
⇒ **단위 표기 오류로 보이나 확정 불가. 절대값 인용 금지, 비율만.**

### ④ ⚠ 인장 탄성률과 압입 탄성률이 100배 이상 어긋난다
`Fig. 1a` 초기 기울기로 읽은 인장 E 는 **수십 MPa 급**인데 나노압입은 **6.03 GPa**.
게다가 "탄성 바인더" 가 PVDF 보다 압입 탄성률이 **더 높다**는 결과 자체가 직관과 반대다.
원인 후보: 박막 위 **기판 효과**, 변형속도, 압입깊이/두께 비. 논문은 언급하지 않는다.
⇒ **필름 E 6.03 GPa 를 그대로 인용하지 말 것.**

### ⑤ ⚠ "바인더의 이온전도도" 라는 이름이 실제 측정과 어긋난다 *(초판 지적 수정)*
SI 를 보면 **측정 전 1 M LiPF₆ 전해질 100 μL 를 셀에 주입**한다.
⇒ 값은 **전해질 함침막의 유효 전도도**이고, PVDF 가 0.65×10⁻⁴ 를 내는 것은 **정상**이다
(초판에서 "PVDF 가 10⁻⁴ 는 불가능" 이라 쓴 것은 **철회**).
남는 문제는 **명명과 해석**이다 — 본문은 이 값을 *"ionic conductivity of the ICEP-8 binder"* 라 부르고
"AMPS 술폰산 + EO 산소가 이온을 옮긴다" 는 **분자 수준 기전**에 귀속시킨다.
그러나 함침막 값에는 **팽윤도·기공률·전해질 흡수량 차이**가 섞여 있어 그 기전만으로 2배를 설명할 수 없다.
또한 Li⁺ 수와 양성자 기여가 분리돼 있지 않다.
⇒ **σ 절대값은 "전해질 함침막 유효 전도도" 라고 명시해야만 인용 가능**, 기전 귀속은 인용 금지.

### ⑥ ⚠ 표면 최적화가 Γ-only · 컷오프 300 eV
5×4 초격자는 측면 ~14 × 12 Å 급이고, NCM811 은 **작은 갭/금속성에 가까운 상관 산화물**이다.
그 계의 표면 기하최적화를 **1×1×1 (Γ)** 로 하는 것은 얇다.
컷오프 **300 eV** 도 O 를 포함한 ultrasoft 계산의 통상 "fine" 기준보다 낮다.
수렴 시험(k-mesh·컷오프에 대한 E_bind 변화)이 **하나도 제시되지 않았다.**
또한 **U 값을 Jain 2011(MP, VASP PAW 기준으로 적합된 세트)에서 가져와 CASTEP+USPP 에 그대로 쓴다** —
U 는 투영자 규약에 의존하므로 코드 간 이식은 자명하지 않다.

### ⑦ ⚠ 본문 ↔ 그림 ↔ SI 불일치 4곳
1. **`Fig. 3c`**: 본문 *"consistently higher over the entire SOC and DOD ranges"*
   → 그림에서 **SOC ≈90–95 % 에서 교차**(ICEP 가 살짝 아래).
2. **`Fig. 1e`**: 막대 상단 **figure-read ≈1.29 ± 0.03 ×10⁻⁴** ↔ 본문 **1.35 ×10⁻⁴**.
3. **`Fig. 6j` 인셋 306 mAh** ↔ 본문 **304 mAh**; 파우치 로딩 **본문 62.5 ↔ SI 62.7 mg cm⁻²**.
4. **LSV 범위: 본문 3.0–6.0 V ↔ SI 3.0–5.0 V.**
   SI 가 맞다면 *"onset above 5.0 V"* 는 **스캔 종점 바로 그 자리**여서 onset 을 관측했다고 말하기 어렵다.

### ⑧ ⚠ TOF-SIMS·EELS·Raman 의 정량 근거가 약하다
- `Fig. 4b,c` 는 **각 이온종을 자기 최대로 정규화**한 곡선인데 본문은 그것으로 **종 간 세기 비교**를 한다
  (그 주장은 `Fig. 4d` 로만 가능).
- `Fig. 5e` 의 **PVDF 표면 O K 스펙트럼은 거의 무특징**인데 그 위에 ΔE 화살표를 그렸다.
- `Fig. 6e,f` 의 **상단 Raman 은 사실상 평평**한데 Eg/A₁g = 0.98–0.99 를 3자리로 인용.
  피크가 안 보이는 스펙트럼에서 세기비를 뽑는 절차가 기술돼 있지 않다.

### ⑨ ⚠ 축 절단·2축 막대가 차이를 시각적으로 과장한다
`Fig. 1c`(E 2–6.5 / H 0.30–0.45), `Fig. 1e`(0.4–1.4), `Fig. 4a`(0–100 / 480–500) 전부 잘린 축.
`Fig. 4a` 는 **PVDF Ni 막대가 잘려 값을 못 읽는다**.

### ⑩ ⚠ 대조군이 PVDF 하나뿐
"불소 없는 바인더" 를 내세우면서 **PAA·CMC/SBR 같은 F-free 대조군과의 비교가 없다.**

### ⑪ ⚠ `Fig. 6i` 의 상위 3점은 측정이 아니라 추정
451.3 / 462.3 / 466.1 Wh kg⁻¹ 은 **속 빈 별 = `Table S5` 계산치**인데
문헌 점과 **점선으로 이어져** 시각적으로 측정 우위처럼 보인다.
**실측 비교는 2층 377.6 vs 문헌 300–365 까지**가 정당하다.

### ⑫ ⚠ 계산 상세가 전부 SI 에만 있고 본문에는 한 줄도 없다
Adv. Mater. 형식상 Experimental 이 SI 로 가는 것은 흔하나,
**본문 DFT 단락에 코드 이름조차 없다.** 본문만 보는 독자는 이 4점이
**평면파 DFT 인지 범용 NNP 인지도 구분할 수 없다.** (실제로 이 digest 초판이 그 상태로 멈췄다.)

### ⑬ ⚠ "direct theoretical support" 라는 표현
**0 K·진공·단분자·자세 1개** 계산이 μm 스케일 분산과 N 단위 접착력의 "직접적 이론 근거" 는 아니다.
우리 원고에서 **쓰지 말아야 할 문장 형태**의 사례.

---

## 11. 기술 미니 용어집

| 용어 | 뜻 | 이 논문에서 |
|---|---|---|
| **RAFT** | 가역 첨가-분절 사슬이동 중합. CTA 로 분자량·구조 제어 | PEO₄₆-MCTA 를 **이관능** CTA 로 → 대칭 트리블록 |
| **macro-CTA** | 고분자 자체가 CTA | PEO₄₆-MCTA |
| **AMPS** | 2-아크릴아미도-2-메틸프로판술폰산. 강산성 SO₃H + 아미드 | 이온전도 + 수소결합 |
| **Tg 두 개** | 상분리된 블록마다 Tg 가 따로 보인다 | −56 °C(소프트) / 85.2 °C(하드) = **물리 가교** |
| **인성** | S-S 곡선 아래 면적. **강도와 다르다** | ICEP 는 약하지만 질기다 |
| **SAICAS** | 표면·계면 절삭 분석 | cutting=응집, peeling=접착 |
| **GITT** | 정전류 간헐 적정. 펄스-완화로 R·D 를 SOC 별로 | Weppner–Huggins 식 |
| **DRT** | 완화시간 분포. 임피던스를 τ 축으로 분해 | R_SEI(10⁻⁴–10⁻²) / R_ct(10⁻²–10⁰) |
| **GEIS** | 정전류 EIS. 사이클 중 in situ 가능 | 0.5 C, 10 분 간격 |
| **TOF-SIMS 깊이 프로파일** | 이온빔으로 깎으며 2차이온 질량분석. 깊이축 = 스퍼터 시간 | CEI 내층 108 vs 283 s |
| **암염(rock-salt) 상** | 표면이 Li 를 잃고 TM 이 Li 층으로 이동해 생기는 Fm-3m 상. Li 확산 차단 | 11.3 → 3.1 nm |
| **O K-edge ΔE** | O 1s → 미점유 TM 3d–O 2p 혼성(pre) ↔ TM 4sp(main) 간격. 산화상태 지시자 | Ni⁴⁺ 유지 = ΔE 큼 |
| **Ni L₃/L₂** | Ni 백색선 비. 크면 저산화(Ni²⁺) | Ni²⁺ 침입 판정 |
| **Eg/A₁g (Raman)** | M–O–M 굽힘(440) / M–O 신축(530). SOC 지시자 | 두께방향 탈리튬 균일성 |
| **N/P · E/C** | 음극/양극 용량비 · 전해질무게/용량(g Ah⁻¹) | 1.57 · 2.5 |
| **ultrasoft PP** | 평면파 컷오프를 낮추려 노름보존을 포기한 의퍼텐셜. CASTEP 기본 | 컷오프 300 eV |
| **Tkatchenko–Scheffler** | 전자밀도로부터 원자별 C₆ 를 유도하는 vdW 보정. D2 보다 환경 민감 | vdW 보정 |
| **BFGS** | 준-뉴턴 최적화기 | 원자+셀 동시 |
| **DFT+U** | 국소 d/f 오비탈 자기상호작용 보정. **값이 코드·투영자 규약에 의존** | Ni 6.0 / Co 3.4 / Mn 3.9 eV |
| **결합에너지 (흡착)** | `E_total − (E_molecule + E_slab)`. 음수 = 발열 = 유리 | SI 식 (5) |
| **양성자 전달 흡착(해리흡착)** | 산의 H 가 표면 O 로 옮겨가 `표면-OH + 음이온` 이 되는 흡착. **원자수 보존 → 중성** | `(−H)` (SI `Figure S13`) |
| **state-selection policy** | 허용 상태가 여럿일 때 어느 것을 "그 값" 으로 삼을지 정하는 규칙. 없으면 스칼라 estimand 가 정의되지 않는다 | 이 논문에 **없다**(§10-①) |

---

## 12. 인용 규율 (⛔ / ✅)

**⛔ 인용 금지**
- **결합에너지 절대값 4개** — 전부 `figure-read`(본문·SI 본문에 수치 없음) + Γ-only·300 eV·수렴시험 0 (§10-⑥)
- **`(−H)` 를 "탈양성자 술포네이트" 로 부르는 것** — **H 이동 상태**다 (SI `Figure S13`)
- **−0.424 eV 를 확정된 "H 이동 에너지" 로** — 기준 분자 명시가 없어 **추론**이고, 자기상태 미정 (§4.3c·§10-①)
- **"ICEP 가 PVDF 보다 강하게 붙는다"** — 조성 가중하면 뒤집힐 수 있다 (§10-②)
- **σ 를 "폴리머 고유 이온전도도" 로** — 전해질 함침막 값이다 (§10-⑤)
- **인성 절대값 (601.2 / 151.8 J m⁻³)**, **필름 E 6.03 GPa** (§10-③④)
- **451.3 / 462.3 / 466.1 Wh kg⁻¹** — 추정치 (§10-⑪)
- 424.4 와 377.6 을 **같은 축에** 두는 것
- 우리 SDCP E_ads 와 **나란히 놓는 것** — 면(001 vs 104)·코드·U·기준 전부 다름

**✅ 인용 가능**
- **계산 세팅 전표 그대로** (§4.1): CASTEP · PBE · spin-polarized · USPP · TS-vdW ·
  U(Ni 6.0/Co 3.4/Mn 3.9) · 300 eV · Γ-only(표면) · (001) 8층 5×4 · 하단 2층 고정 · 진공 >15 Å
- **결합에너지 정의식** SI 식 (5) 원문
- **`(−H)` 의 정의** — SI `Figure S13` 캡션 원문 (H 이동)
- **정성 순서**: AMPS(−H) < AMPS < PVDF < AN (결합 깊은 순)
- **"본문에 `(−H)` 도, 결합에너지 수치도 없다"** 는 사실 (§4.4)
- SAICAS (0.29/0.27 vs 0.07/0.04 N), 전극 나노압입 (1.57/0.15 vs 0.11/0.014 GPa)
- 암염층 3.1 vs 11.3 nm, CEI 내층 108 vs 283 s, XPS 비 0.24 vs 0.79
- 로딩·면적용량·유지율 (62.4 mg cm⁻², 12.5 mAh cm⁻², 94.6 % @60 cyc)
- 파우치 사양 (N/P 1.57, E/C 2.5 g Ah⁻¹, 377.6 Wh kg_cell⁻¹, 1016.8 Wh L_cell⁻¹, 96.7 % @40 cyc)
- 무게 파이 (양극 47.2 / 전해질 25.0 / 패키지 18.6 %)
- Mn 킬레이션 프로토콜과 값 (126 vs 27 ppm)

---

## 13. 무엇을 보고 무엇을 안 봤나

**본문**: 15 pp 전문 (PyMuPDF 텍스트 + 페이지 렌더).
**SI**: `adma202506266-sup-0001-SuppMat.docx` **전문** — Experimental / **Computational details** /
Fig S1–S28 캡션 / Table S1–S6 / Supporting References. **§4 는 전부 이 전문에 근거한다.**

**그림 크로핑** (`litdb/figures/han2025_icep_binder_ultrahigh_loading_ncm811/`, 7장):

| 파일 | 실물 판독 | 비고 |
|---|---|---|
| `fig_1.png` | ✅ | §10-③④⑤⑨ 의 근거 |
| `fig_2.png` | ✅ + **고배율 재렌더 5회** | `Fig. 2g` 를 26–30× 로 다시 그려 SO₃ 의 H 위치를 원자 단위로 확인 → **SI `Figure S13` 과 일치**(§4.3f) |
| `fig_3.png` | ✅ | `Fig. 3c` 교차 발견 (§10-⑦-1) |
| `fig_4.png` | ✅ | PVDF Ni 막대 축 절단 확인 |
| `fig_5.png` | ✅ | EELS ΔE figure-read |
| `fig_6.png` | ✅ + 인셋 재렌더 | 306 vs 304 mAh 불일치 (§10-⑦-3) |
| `sch_1.png` | ✅ | `x/y = [AN]/[AMPS]` 확정 (§10-② 의 근거) |

**⚠ 도구 버그 1건 발견·수정** (2026-08-29): `extract_figures.py` 가 `Scheme 1` 과 `Figure 1` 을
**둘 다 `fig_1.png` 로 저장**해 Scheme 1 이 통째로 사라졌다(`figures.json` 에는 `s1`·`f1` 두 행이
남아 "7장 추출" 로 보였다). `_fname_prefix()` 를 넣어 scheme → **`sch_`** 로 분리하고
selftest 5건(음성 2건 포함)을 추가했다. **다른 slug 의 기존 폴더는 소급되지 않는다 —
Scheme 이 있는 논문은 `--clean` 재실행이 필요하다.**

**안 본 것**: **SI 의 그림 본체**(캡션은 전부 읽었으나 docx 안의 이미지는 렌더하지 않았다).
특히 `Figure S12`(모델 계)·`Figure S13`(최적화 구조 4종) 의 **그림 자체**는 못 봤다 —
다만 `Fig. 2g` 가 같은 구조를 싣고 있어 §4.3 의 판독은 본문 그림으로 대체했다.

**figure-read 로만 얻은 값** (`≈` 유지): 결합에너지 4점 · `Fig. 1a` PVDF 최대응력 ≈8.9 MPa ·
`Fig. 1e` σ 막대 ≈1.29×10⁻⁴ · `Fig. 3b` 율속 5수준 · `Fig. 3d` DRT 피크 높이 ·
`Fig. 4a` PVDF Ni ≥500 ppm · `Fig. 5e,f` EELS ΔE ≈3 / ≈10–11 eV.

---

## 14. 후속 조치 (열린 항목)

1. **우리 SDCP 자세 목록에 "양성자 전달(해리) 흡착" 추가 검토** (§7.2-2).
   ⚠ `kb/templates/estimand_card.md` §1–3 을 **먼저** 채우고(참조·전하·**스핀 선택 규칙**),
   `db/governance/decisions.json` 에 proposed 로 등록한 뒤에. 이 논문이 빠뜨린 것이 정확히 그 규칙이다.
2. **`U_PCET` 의 산화물 슬랩 버전**을 우리 양 목록에 만들 것 — `comparison_vs_ours.md` §F-2 에 등록.
3. **`kb/methodology/estimand_before_running_2026_08_28.md` 에 외부 사례로 등록** —
   "게재 논문도 자성·산화환원 활성 슬랩에서 상태 선택 규칙 없이 두 상태를 나란히 찍는다."
4. **Mn²⁺ 킬레이션 프로토콜**(0.01 M Mn(ClO₄)₂, 6 h, ICP-MS) — SDCP 실험 요청서 후보.
5. **SAICAS 규약**(45°/20°/10°, 블레이드 1 mm) — 우리 바인더 접착 측정 시 이 조건을 쓰면
   이 논문 값(0.29/0.27 vs 0.07/0.04 N)과 **직접 비교 가능**해진다.
6. **Scheme 이 있는 기존 digest 폴더 재추출** — `extract_figures.py` 버그 수정 소급 (§13).

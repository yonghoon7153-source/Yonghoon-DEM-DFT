# NMC333 / NMC532 의 전자·이온 전달물성을 **리튬 함량 x 의 함수로** 실측 — Amin & Chiang (JES 2016, MIT)

> slug `aminchiang2016_nmc_electronic_ionic_transport_vs_li` · DOI `10.1149/2.0131608jes` · type `experiment (impedance + DC polarization, sintered pellet)` · PDF `Amin_Chiang_2016_JES_NMC333_NMC523_electronic_ionic_transport.pdf` · digested `2026-08-25` · status ✅

> ⚠ **ERRATUM 포함** (같은 PDF 8쪽, DOI `10.1149/2.0881610jes`, JES 163 (10) X7, 2016-08-23 게재):
> 본문 전체에서 **Li₁₋ₓNi₀.₅₀Mn₀.₂₀Co₀.₃₀O₂ → Li₁₋ₓNi₀.₅₀Mn₀.₃₀Co₀.₂₀O₂**, **NMC523 → NMC532** 로 정정.
> Ni 는 0.50 그대로이므로 아래의 "Ni 함량 방향" 논의는 영향 없다.  Mn/Co 만 뒤바뀐다.
> **이 카드는 그림·표의 원 라벨을 유지하되 조성을 언급할 때는 NMC532 로 적는다.**

---

## 1. 한 줄 요약

**첨가제·바인더 없는 단상(single-phase) 소결 펠릿**(96–98 % 상대밀도)에서 NMC 의 **전자전도도 σ_e 와
이온전도도 σ_ion·화학확산 D̃_Li 를 전자차단/이온차단 셀로 분리 측정**하고, **σ_e 를 리튬 함량 x 의
함수로 4–5 자릿수에 걸쳐 낸** 논문.  ⇒ **우리 σ_e 폼의 재료 앵커(σ_AM / σ_S / σ_P)를 실측 밴드에
대볼 수 있는, 리포에 있는 것 중 유일하게 "AM 고유값"인 외부 기준**이다.
**판정은 우리에게 불리하다 — §3 을 먼저 읽을 것.**

## 2. 메타

| 저자 | 소속 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|---|
| **Ruhul Amin**, **Yet-Ming Chiang\*** | MIT DMSE (+ QEERI, Hamad Bin Khalifa Univ.) | J. Electrochem. Soc. **163** (8) A1512–A1517 (2016) | 10.1149/2.0131608jes | Li₁₋ₓNi₀.₃₃Mn₀.₃₃Co₀.₃₃O₂ (**NMC333**) · Li₁₋ₓNi₀.₅₀Mn₀.₃₀Co₀.₂₀O₂ (**NMC532**, erratum) — 분말 TODA America | **실험** (EIS + DC 분극/탈분극, 소결 펠릿) |

- Open Access (CC BY-NC-ND).  투고 2015-12-31 / 개정 2016-04-19 / 게재 2016-05-13.
- 자금: DOE BES EFRC **NECCES** (Award DE-SC0012583).
- ⚠ **811 이 아니다.**  Ni 0.33 과 0.50 두 조성뿐이다.  우리 소재는 **NMC811**(Ni 0.80) → §3-4 외삽 경고.

---

## 3. ★★★ 미션 판정 — 우리 σ_e 재료 앵커(σ_AM 50 / σ_S 10 / σ_P 5 mS cm⁻¹) 대조 ★★★

> 이 카드를 만든 **단 하나의 이유**.  지도교수 질문 *"NMC811 의 electronic conductivity 가 effective
> value 라는 게 무슨 뜻이냐, 그럼 source 는 뭐냐"* 에 답하기 위한 절이다.

### 3-1. 우리 코드가 지금 실제로 쓰는 값 (2026-08-25 리포 실측, 읽기전용)

| 자리 | 기호 | 값 | **코드에 적힌 라벨** |
|---|---|---|---|
| `scripts/network_conductivity.py:53` — **DEM 접촉망 솔버(ground truth)** | `SIGMA_AM_ELECTRONIC` | **0.05 S cm⁻¹ = 50 mS cm⁻¹** | `# S/cm (50 mS/cm, NCM811 grain interior, **discharged**)` |
| `scripts/electronic_nested_cv.py:43` — σ_e 회귀 정규화 | `SIGMA_AM` | **50.0 mS cm⁻¹** | `# NCM811 grain conductivity [mS/cm]` |
| `scripts/hybrid_predictor.py:26` · `electronic_scaling_law.py:22` | `SIGMA_AM` | **50.0 mS cm⁻¹** | `(0.05 S/cm, NCM811)` |
| `scripts/generate_comparison_plots.py:5779–80` — **Stage 22.5 폼 LOCKED** | `_SIGMA_S_LOCKED` / `_SIGMA_P_LOCKED` | **10 / 5 mS cm⁻¹** | `corpus-fit ~9.1 / ~4.1, rounded` |
| `scripts/step3_sigma.py:79` — **STEP3 복셀 생산값** | `AM_S` / `AM_P` | **0.010 / 0.005 S cm⁻¹ = 10 / 5** | `⚠ corpus-fit endpoints, NOT a Trevisanello measurement` |
| `scripts/voxel_conductivity.py:109` — 레거시 미리보기 표 | `PHASE_SIGMA['electronic']['AM']` | **50.0 mS cm⁻¹** | 파일 자신이 `★생산 값은 step3_sigma 를 쓸 것(이 파일 값 인용/복사 금지)` |

⇒ **50 mS cm⁻¹ 은 "레거시 UI 상한" 이 아니다.**  DEM 접촉망 **ground-truth 솔버의 σ_bulk** 이고,
Stage 22.5 가 적합된 그 솔버 출력의 스케일을 정한다.  그리고 코드가 그것을 **"discharged"**
(= 완전 리튬화, x = 0) 라고 라벨하고 있다.  ★ 이 논문이 정면으로 재는 것이 바로 그 상태다.

### 3-2. 이 논문이 잰 밴드 (30 °C, DC, Fig 2c — digitized, §5-3 에서 3중 검증)

| x (Li₁₋ₓNMC) | NMC333 (S cm⁻¹) | NMC333 (mS cm⁻¹) | NMC532 (S cm⁻¹) | NMC532 (mS cm⁻¹) |
|---|---|---|---|---|
| 0 (완전 리튬화 = **discharged**) | 5.0 × 10⁻⁸ | **5.0 × 10⁻⁵** | 1.9 × 10⁻⁶ | **1.9 × 10⁻³** |
| 0.10 | 2.1 × 10⁻⁵ | 2.1 × 10⁻² | 2.8 × 10⁻⁴ | 2.8 × 10⁻¹ |
| 0.30 | 6.1 × 10⁻⁴ | 6.1 × 10⁻¹ | 9.9 × 10⁻⁴ | 9.9 × 10⁻¹ |
| 0.50 | 1.6 × 10⁻³ | 1.6 | 1.5 × 10⁻³ | 1.5 |
| 0.75 (**최대**, ≈4.7/4.8 V 충전) | 7.9 × 10⁻³ | 7.9 | **1.4 × 10⁻²** | **13.8** |

**측정 전 범위 = 5.0 × 10⁻⁸ … 1.4 × 10⁻² S cm⁻¹ = 5.0 × 10⁻⁵ … 13.8 mS cm⁻¹** (30 °C, x ≤ 0.75).

### 3-3. ★ 판정 (a) — 우리 값은 밴드의 어디인가

| 우리 값 | 밴드 안/밖 | 30 °C 측정 **최대**(13.8) 대비 | **discharged (x=0)** 대비 |
|---|---|---|---|
| **σ_AM = 50 mS cm⁻¹** | ⛔ **밖 (위)** | **3.6× 위** | **NMC333 대비 1.0 × 10⁶ ×** · NMC532 대비 2.7 × 10⁴ × |
| **σ_S = 10 mS cm⁻¹** | ✅ 안 — 단 **충전 끝단** (≈ NMC532 x ≈ 0.71) | 0.73× (아래) | NMC333 대비 2.0 × 10⁵ × · NMC532 대비 5.3 × 10³ × |
| **σ_P = 5 mS cm⁻¹** | ✅ 안 — **x ≈ 0.64–0.68** | 0.36× (아래) | NMC333 대비 1.0 × 10⁵ × · NMC532 대비 2.7 × 10³ × |

> ⚠ x-매핑은 우리 digitized Fig 2c 를 **로그 보간**한 DERIVED 값이다.  ±0.05 dex 디지타이즈 오차에서
> Δx ≈ ±0.02 수준.  **조성이 다르므로**(333/532 vs 우리 811) "우리 전극이 실제로 저 x 에 있다"는
> 주장이 아니라 **정렬용 눈금**이다.

**온도로 못 메운다 (DERIVED, 이 논문 E_a 로 외삽):** x = 0.75 에서 E_a 는 NMC532 **0.05 eV** ·
NMC333 **0.10 eV** 로 매우 작다.  30 → 100 °C (그들 측정 상한) 로 올려도
**NMC532 13.8 → 19.7 · NMC333 7.9 → 16.2 mS cm⁻¹** 뿐이다.
⇒ **측정 봉투 안(x ≤ 0.75, T ≤ 100 °C) 어디에서도 50 mS cm⁻¹ 에 닿지 않는다** (최소 2.5× 부족).

### 3-4. ★ 판정 (b) — 그 차이가 무엇으로 설명되는가 (탈리튬화 / 조성 / 측정종류)

**(i) 탈리튬화 — 이것이 가장 큰 몫이다. 그리고 "effective" 라는 말의 물리적 정당화다.**
σ_e 는 x = 0 → 0.75 에서 **NMC333 1.6 × 10⁵ 배 (5.20 자릿수)** · **NMC532 7.3 × 10³ 배 (3.87 자릿수)**
오른다.  초기 10 % 탈리튬화만으로 **NMC333 418× · NMC532 152×**.
⇒ **NMC 의 σ_e 는 단일 스칼라가 아니다.**  하나를 쓰려면 **어느 x 인지 반드시 명시**해야 하고,
그 말이 곧 "effective(= 운전점 평균)" 이다.  우리 코드의 `discharged` 라벨은 **가장 σ_e 가 낮은
지점을 가리키면서 값은 가장 높은 쪽**을 쓰고 있어 **라벨과 값이 반대 방향**이다.

**(ii) 조성 (811 vs 333/532) — 방향은 있으나 크기는 외삽 불가.**
- 이 논문의 유일한 조성 레버: **완전 리튬화 상태에서 NMC532(Ni 0.50) 가 NMC333(Ni 0.33) 보다 37.6× 높다.**
  저자 설명: *"Ni is considered an active conduction site which may facilitate electron hopping."*
- ⚠ **그런데 그 우위가 사라진다**: x = 0.3 에서 1.6× · x = 0.5 에서 0.9× (사실상 동일) · x = 0.75 에서 1.7×.
  저자 본문도 *"after 30 % delithiation both have similar electronic conductivity"* 라고 명시한다.
- ⇒ **811 방향 = UP, 단 x ≈ 0 근처에서만.**  **크기는 외삽 불가**: 조성이 2개뿐이고 함수형이 없으며,
  우리가 실제로 관심 있는 운전 구간(x ≳ 0.3)에서는 **Ni 효과 자체가 소멸**한다.
- ⛔ **절대값 전이 금지.**  아래 계산은 **"아무리 관대하게 외삽해도"** 를 보이기 위한 것이지 값이 아니다:
  Ni 0.33 → 0.50 의 37.6× 를 Ni 에 로그-선형이라 **가정**하고 0.80 까지 밀면 x = 0 에서
  1.9 × 10⁻⁶ × 37.6^(0.30/0.17) ≈ 1.3 × 10⁻³ S cm⁻¹ ≈ **1.3 mS cm⁻¹** — **여전히 50 의 1/38 이다.**
  ⚠ **이 외삽의 전제는 논문 자신의 데이터가 반증한다**(x ≥ 0.3 에서 Ni 효과 소멸).  **인용 금지, 예시용.**

**(iii) 측정 종류 — 이쪽에서 우리를 봐줄 여지가 가장 작다.**
이 논문 값은 **첨가제·바인더 없는 단상 소결 펠릿의 벌크(grain) 값**이다 (§4-2: C ≈ 5 × 10⁻¹¹ F 가
입계가 아니라 **grain** 임을 확인).  우리 `SIGMA_AM_ELECTRONIC` 의 라벨도 **"grain interior"** 다.
⇒ **종류가 같다.**  "우리는 유효값이라 다르다" 는 **이 축에서는 방패가 안 된다** — 라벨이 서로 같다.
남는 정당한 유효화 경로는 세 가지뿐이고, 셋 다 **값이 아니라 라벨을 고쳐야** 하는 종류다:
1. **운전 SOC** (위 (i)) — 가장 크고 가장 정당한 몫.
2. **탄소 데코레이션 럼핑** — DEM **접촉망** σ_e 폼(Stage 22.5)에는 **명시적 탄소상이 없다**.
   AM 표면의 카본블랙/VGCF 기여가 σ_S/σ_P 로 흡수되는 것은 방어 가능하다 (CL-47 이 σ_VGCF 100 을
   "유효 망 상수" 로 재라벨한 것과 **같은 인식론**, frame[2]).
   ⚠ 단 **STEP3 복셀에는 탄소상이 명시적으로 있다** → 거기서 같은 럼핑을 하면 **이중 계상**이다.
   다행히 STEP3 값은 10/5 라 밴드 안이다.
3. **입자 미세구조 / 코팅 / 도핑** (NCWA, LNO/LZO) — 이 논문 범위 밖. 훅만.

### 3-5. ★ 판정 (c) — 원고 표에 어떻게 적어야 정직한가 (문장 제안)

⛔ **지금 라벨은 못 쓴다**: `σ_AM = 50 mS/cm (NCM811 literature reference)` — **이 논문이 그 주장을
지지하지 않는다.**  NMC 의 additive-free 단상 실측은 이것이 사실상 유일하고(저자들 자신이
*"we know of no published measurements for NMC333 and NMC523 compositions"*), 그 밴드의
**최댓값보다도 3.6× 위**다.  리뷰어가 정확히 여기를 찌른다.

**✅ 제안 1 — σ_AM (솔버 σ_bulk) 각주**
> "σ_AM = 50 mS cm⁻¹ is an **effective, network-level material prefactor** for the AM electronic
> backbone; it is **not** an intrinsic single-phase NMC811 conductivity and no literature
> measurement is claimed for it.  For scale, the only additive-free, single-phase sintered-pellet
> measurement of NMC transport (Amin & Chiang, *J. Electrochem. Soc.* **163**, A1512 (2016);
> NMC333 and NMC532) gives 5 × 10⁻⁸ – 1.4 × 10⁻² S cm⁻¹ at 30 °C over x = 0 → 0.75 in Li₁₋ₓNMC.
> Our value lies **3.6× above the top of that band** and ~10⁶× above the fully lithiated state,
> and therefore lumps the state of charge, the carbon-decorated AM surface, and every
> sub-particle mechanism the contact network does not resolve."

**✅ 제안 2 — σ_S / σ_P (Stage 22.5 LOCKED 엔드포인트) 각주**
> "σ_S = 10 and σ_P = 5 mS cm⁻¹ are **corpus-calibrated endpoints** (fitted 9.1 / 4.1, rounded);
> the magnitude is **not** taken from literature.  They fall **inside** the measured NMC band of
> Amin & Chiang (2016) but only at the **strongly delithiated end** (x ≈ 0.6–0.7, ≈4 V vs Li/Li⁺),
> i.e. they are charged-state-like values.  At the discharged state the same measurement is
> 10³–10⁵ times lower, so σ_e of the AM phase must be read as an **operating-point average**."

**✅ 제안 3 — 표에 열 하나 추가 (가장 저렴하고 가장 효과적)**
σ 표에 **`kind`** 열을 만들어 `measured (bulk, sintered pellet)` / `effective (corpus-calibrated)` /
`effective network constant` 를 각 행에 붙인다.  CL-47 이 σ_VGCF 100 에 대해 이미 요구한 것과
**같은 규율**이고("범주 비대칭 주의: σ_SDCP 250 은 재료 앵커, σ_VGCF 100 은 유효 망 상수"),
한 줄로 리뷰어의 질문 전체를 선점한다.

**✅ 제안 4 — "effective" 의 정의를 본문에 한 번 못박기**
> "Throughout, *effective* means a lumped coefficient calibrated so that the **network-level**
> observable matches experiment, not a measured single-phase material constant — the same
> epistemic status as our softened E_eff = 1.35 GPa, which stands in for granular rearrangement
> that a rigid-sphere DEM cannot represent." (frame[2])

### 3-6. ★★ 보너스 — "문헌 산포 수 자릿수" 는 산포가 아니라 **SOC 축**이었다

리포의 열린 항목(`comparison_vs_ours_DEM.md` §B, Zhang23 절): *"NMC 전자전도는 SOC 의존이 크고
문헌이 수 자릿수 흩어진다 → 밴드로 다루고 감도 프로브로 검정"*.  **이 논문이 그 축을 직접 잰다.**
우리 digitized Fig 2c 로 기존 카드의 σ_AM 값들을 x 축에 올리면 (⚠ 전부 DERIVED · 조성 혼합 · **정렬용**):

| 출처 | σ_AM (mS cm⁻¹) | Fig 2c 로 읽은 대응 x | 성격 |
|---|---|---|---|
| Amin & Chiang **x = 0** (NMC333) | 5.0 × 10⁻⁵ | 0 | 측정 (완전 방전) |
| Amin & Chiang **x = 0** (NMC532) | 1.9 × 10⁻³ | 0 | 측정 (완전 방전) |
| **[Zhang23] Joule 2023** σ_AM (SI ref Wang 2018) | **0.05** | **x ≈ 0.07–0.15** | 모델 입력 |
| **[Oh 2026] Table S15** σ_NCM (단결정) | **2.45** | **x ≈ 0.56** | 모델 입력 |
| **우리 σ_P (LOCKED)** | **5** | **x ≈ 0.64–0.68** | corpus-fit |
| **우리 σ_S (LOCKED)** | **10** | **x ≈ 0.71** | corpus-fit |
| **[Oh 2026] Table S15** σ_NCWA (W-도핑 다결정) | **13.7** | **x ≈ 0.75 (측정 상한)** | 모델 입력 |
| **우리 σ_AM (솔버 σ_bulk)** | **50** | **x > 0.75 — 측정 범위 밖** | ⛔ |

⇒ **모델링 문헌이 쓰는 "NMC σ_e" 는 거의 전부 충전 상태 값이다.**  200×–10⁶× 로 보이던 불일치가
**하나의 단조 사다리**로 정렬된다.  ★ 이것 하나만으로도 `comparison_vs_ours_DEM.md §B` 의
"밴드로 다뤄라" 가 **"SOC 로 색인하라"** 로 승격된다.
⚠ **그리고 우리 50 만 사다리 밖에 있다.**

---

## 4. 실험 방법 ★ (우리 값이 "어떤 종류의 σ" 인지 가르는 자리)

### 4-1. 시료 — 왜 이 값이 "벌크" 인가
- 분말: **TODA America Inc.** (Battle Creek, MI) 의 NMC333 · NMC532 상용 분말.
- **340 MPa 로 가압**, ⌀ **14 mm** 원통 펠릿.
- **900 °C · 12 h · 대기(ambient) 소결**, 승온·냉각 **5 °C/min**.
- ⇒ **상대밀도 96–98 %** — 저자 표현: *"sufficiently high that the measured conductivity represents
  the **bulk value**."*
- **다공도 보정**: *"porosity reduces the effective cross-sectional area **in direct proportion** to the
  pore volume fraction, and the conductivity is therefore proportional to density"* ⇒ 96–98 % 에서
  보정은 **≤4 %**.  ⚠ 이 선형 가정 자체는 검증되지 않았고, 우리 Bruggeman/tortuosity 관점에서는
  **낙관적**이다 (그러나 4 % 규모라 판정에 무영향).
- 두께: σ 측정용 **0.30–0.80 mm** 연마.  D 측정용 별도 박형 **0.26–0.30 mm**, 면적 **0.219–0.158 cm²**.
- ★ **첨가제·바인더·복합화가 전혀 없다** — 저자 의도 그대로: *"the extrinsic effects due to binders,
  conductive additives, and particle microstructures that may be present in composite electrodes
  are avoided."*  ⇒ **우리 σ_AM 이 되려는 그 양(=AM 상 자체의 전도도)에 가장 가까운 실측.**

### 4-2. 전자전도도 σ_e — **이온차단(ion-blocking) 대칭셀**
- 셀: **Ag | NMC | Ag** (양면 Ag 페이스트 → **120 °C 하룻밤** 유기용매 제거), coin-cell 홀더 +
  양면 스테인리스 디스크.
- ⚠ **2-단자 대칭셀이다 — 4단자(4-probe)가 아니다.**  대신 **EIS 로 접촉/전극 기여를 분리**한다.
- **DC 분극** + **EIS** 둘 다 (Bio-logic **VMP3**), **200 kHz – 0.5 Hz**, **25–100 °C** (VWR 온도조절기,
  열전대로 시료 온도 측정), 승온·냉온 양방향 측정.
- **전자-지배 판정 3중**:
  1. Fig 1a: **2 × 10⁶ – 5 × 10⁻¹ Hz 에서 거의 완전한 반원 하나**.  등가회로 = **R ∥ CPE** (Fig 1b).
     `C = (R^(1−n)·Q)^(1/n)`, **n = 0.90–0.96**.
  2. **유도 커패시턴스 ≈ 5 × 10⁻¹¹ F** ⇒ *"originate from the **bulk (grains)**"* — 입계 임피던스에
     기대되는 값보다 **수 자릿수 작다** (ref 25 Baumann 학위논문 p.33).  ★ **GB 아님, grain 임.**
  3. **저주파에 두 번째 반원(추가 분극 과정)이 없다** ⇒ 전자 캐리어 지배.
     DC 로 재확인: 정전류 인가 시 전압이 **계단함수**로 올라 일정값 유지, 끊으면 계단함수로 하강
     (Fig 1c).  이온 기여가 크면 D_Li 가 정하는 시상수로 **느리게 완화**해야 한다 (refs 26–29).
- ★ **우리 매핑**: 이것은 **"소결 다결정 세라믹 벌크 = grain 지배"** 값이다.
  **복합체 유효(effective) 값이 아니고**, **단결정 값도 아니다** (다결정이지만 임피던스 호가 grain 지배).

### 4-3. 이온전도도 σ_ion + 확산 D̃ — **전자차단(electron-blocking) 대칭셀**
- 셀: **Li | PEO | NMC | PEO | Li** (Swagelok형).
- **PEO 차단층**: PEO (Scientific Polymer Products, **Mw 4,000,000**) + **LiI** (Aldrich 99.99 %)
  **6 : 1 몰비**, 건조 아세토니트릴에서 제막 (제법 상세는 ref 24).
- **EIS**: **200 kHz – 10 µHz**, AC 진폭 **10 mV**, 온도 함수.
- 스펙트럼 구조 (Fig 3a): **고주파 반원 1개** = 전자 + 이온 + **PEO 벌크** 총 저항 /
  **저주파 Warburg** = 전자 차단에 의한 **화학량론 분극(stoichiometric polarization)**.
  → Warburg 로부터 **이온저항** 획득, **Warburg 완화주파수**로부터 **이온 확산도**.
  Fig 3a 인셋: **5.23 × 10⁻⁵ Hz → D_Li = 5.54 × 10⁻⁸ cm² s⁻¹** (NMC333, 61 °C).
- 등가회로 (Fig 3b): **R1 – CPE1 – Ws1 – CPE2**, Zview 로 피팅.
- **DC 분극/탈분극** (Fig 4): 전압이 즉시 `I·R_el·R_ion/(R_el+R_ion)` 로 점프 → 차단된 전자의 부분전류가
  소멸 → **정상상태 `I·R_ion`**.  완화시간 **τ_δ = L²/(π²·D_Li)**.
  장시간 거동은 **Eq 1** (Wagner ref 26 / Yokota ref 27 / Maier ref 28):
  `U_ion = [i_p L/σ] + (σ_el/σ)[i_p L/σ_ion]{1 − (8/π²)exp[−(t/τ_δ)]}`
  → `ln|U(t) − U(∞)| vs t` 직선, **R > 0.99** (Fig 4b: 기울기 −5.0199 × 10⁻⁶ / −3.6528 × 10⁻⁶ s⁻¹ →
  **D_Li = 6.05 × 10⁻⁹ (분극) / 7.55 × 10⁻⁹ (탈분극) cm² s⁻¹**, ~50 °C).
- ⚠ **σ_ion 과 D_Li 는 250 mV 분극전압에 해당하는 Li 조성 구간에 대한 평균**이다 (저자 명시).

### 4-4. D_Li(x) — 단계적 갈바노 적정 + 탈분극
- 셀: **Li | separator (액체 전해질) | NMC | current collector** (전기화학 탈리튬화와 동일 구성).
- 고정량 Li 를 **C/200 및/또는 C/400 로 10 h** 뽑고 → **OCV 로 ≥25 h 완화** (Fig 5a).
- **탈분극(전압 완화) 곡선을 Eq 1 로 피팅**해 D̃_Li 추출 (Fig 5b: 기울기 −9.4057 × 10⁻⁶ s⁻¹, R = 0.99864).
- ⚠ **확산길이 = 시료 두께의 1/2 로 가정** (저자 명시, `The diffusion length was assumed throughout
  to be one half the sample thickness`).  ⇒ **D 의 절대값은 이 가정에 선형 비례**(L²).

### 4-5. 전기화학 탈리튬화 (σ_e(x) 시료 제작)
- Swagelok 셀: Li 금속 대극 / NMC 펠릿 작업극 / **1 M LiPF₆ in EC : DEC = 1 : 1 (몰비)** / Celgard 분리막.
- 펠릿 한쪽 면을 **흑연으로 문질러(burnish)** 집전체와 전기접촉 확보.
- **C/200 및/또는 C/400** 정전류, 연속 또는 간헐.
- 목표 조성 도달 후: **OCV 완화 → 해체 → 아세톤 + 순수 EC/DEC 세척 → 불활성 분위기 120 °C ≥24 h
  (Li 분포 균질화) → 양면 재연마**(표면 Li 염 제거).
- ⇒ **x = 0, 0.10, 0.30, 0.50, 0.75** 다섯 점.  x = 0.75 는 **NMC333 4.7 V · NMC532 4.8 V** 상한 충전에 대응.

### 4-6. Table I 요약 (원표 그대로)

| 대상 | 기법 | 셀 구성 | 무엇의 함수로 |
|---|---|---|---|
| 전자전도도 | EIS – AC | Ag/NMC/Ag | 온도, Li 함량 |
| 전자전도도 | EIS – DC | Ag/NMC/Ag | 온도, Li 함량 |
| 이온전도도 | EIS – AC | Li/PEO/NMC/PEO/Li | 온도 |
| 이온전도도 | EIS – DC | Li/PEO/NMC/PEO/Li | 온도 |
| 이온 확산도 | EIS – AC and DC | Li/PEO/NMC/PEO/Li | 온도 |
| 이온 확산도 | 탈분극 | Li/Separator(전해질)/NMC/집전체 | **Li 함량** |

---

## 5. 핵심 수치 ★ (stated / digitized 구분 필수)

### 5-1. 전자전도도 — 텍스트 서술 (**stated**)
- 초록: *"The electronic conductivity is found to increase with decreasing Li-content (increasing
  state-of-charge) **from ∼10⁻⁷ S cm⁻¹ to ∼10⁻² S cm⁻¹** over Li concentrations **x = 0.00 to 0.75**,
  corresponding to an upper charge voltage of **4.8 V** with respect to Li/Li⁺."*
- ⇒ **5 자릿수 상승**.  (⚠ ~10⁻⁷ 은 저자의 반올림 — 우리 digitized NMC333 x = 0 은 **5.0 × 10⁻⁸**,
  즉 10^−7.30.  서로 모순은 아니고 저자가 자릿수로 뭉갠 것.)
- 활성화에너지 범위: *"range from **0.42–0.05 eV (±0.03 eV)**"* — Saadoune & Delmas 의
  LixNi₀.₈₀Co₀.₂₀O₂ (ref 30) 와 같은 크기이며 **혼합원자가계 small-polaron 이동의 전형값**(ref 31).

### 5-2. 활성화에너지 E_a (Fig 2a/2b 라벨, **stated**; ±0.03 eV)

| 상태 | **NMC532** (Fig 2a) | **NMC333** (Fig 2b) |
|---|---|---|
| 완전 리튬화 (x = 0) | **0.42 eV** | **0.48 eV** |
| 10 % 탈리튬 (x = 0.10) | 0.16 | 0.29 |
| 30 % (x = 0.30) | 0.18 | 0.13 |
| 50 % (x = 0.50) | 0.12 | 0.12 |
| 75 % (x = 0.75) | **0.05** | **0.10** |

- 온도범위: Fig 2a 는 1000/T **2.8–3.4** (≈ 25–84 °C), Fig 2b 는 **2.6–3.4** (≈ 21–111 °C);
  본문 측정범위 서술은 **25–100 °C**.
- ✅ **라벨↔곡선 대응은 추론이 아니라 확정이다 — A.E. 숫자가 범례와 같은 색으로 인쇄돼 있다**
  (그림 렌더링으로 확인, `litdb/figures/…/fig_2.png`):
  Fig 2a — **0.42 빨강 = Lithiated · 0.16 검정 = 10 % · 0.18 보라 = 30 % · 0.12 초록 = 50 % ·
  0.05 파랑 = 75 %**.  Fig 2b — **0.48 빨강 = x 0 · 0.29 검정 = x 0.1 · 0.13 보라 = x 0.3 ·
  0.12 초록 = x 0.5 · 0.10 자홍 = x 0.75.**
  ★ **추가 독립 검증**: 마커를 직접 읽어 Arrhenius 회귀하면 NMC333 x = 0 곡선 **0.487 eV**(라벨 0.48),
  NMC532 리튬화 곡선 **0.431 eV**(라벨 0.42) — §5-3.
- ⚠ **NMC532 는 E_a 가 단조가 아니다** (10 % 0.16 < 30 % 0.18).  ±0.03 eV 오차 안이고, Fig 2a 에서
  30 %(보라)·50 %(초록) 두 곡선이 거의 겹친다 — **두 조성을 구분해 인용하지 말 것.**
- 물리: E_a 가 x 와 함께 **떨어진다** = 탈리튬화가 Ni³⁺/Ni⁴⁺ 혼합원자가 → 좁은 (Ni⁴⁺/Ni³⁺) 밴드에
  정공 생성 → 폴라론 호핑 장벽 감소.

### 5-3. σ_e(x) @30 °C — **digitized (TREND, ±0.05 dex ≈ ±12 %)**, 3중 검증

값은 **§3-2 표** 참조.  **디지타이즈 신뢰도**가 이 카드의 근거이므로 절차를 남긴다:
- PDF 의 Fig 2·6 은 **벡터 그래픽**이라 마커 중심 좌표를 그대로 뽑았다 (pymupdf `get_drawings`).
  픽셀 눈대중이 아니다.
- **x 축 검증**: 마커 중심이 x = **0.000 / 0.1001 / 0.3000 / 0.5001 / 0.7503** 으로 재현
  → 축 캘리브레이션이 **소수 3자리까지** 맞다.
- **교차검증 A (독립)**: Fig **2b** 의 NMC333 x = 0 Arrhenius 7점을 따로 읽어 회귀 →
  **E_a = 0.487 eV** (라벨 0.48) 이고, 30 °C 로 외삽하면 **log σ = −7.30** — Fig **2c** 의 −7.30 과 **동일**.
- **교차검증 B (독립)**: Fig **2a** 의 NMC532 리튬화 8점 → **E_a = 0.431 eV** (라벨 0.42),
  30 °C 외삽 **log σ = −5.73** — Fig 2c 의 −5.73 과 **동일**.
- **범례 시각 확인**: Fig 2c 는 **빨간 채운 원 = NMC333 / 검은 빈 사각 = NMC532**
  (⚠ Fig 6 은 **색이 반대** — 빨간 빈 원 = NMC532 / 검은 빈 사각 = NMC333).
- **정성 서술 4개와 전부 정합**: ① 리튬화 NMC532 > NMC333 (37.6×) ② x ≥ 0.3 에서 둘이 비슷 (1.6× / 0.9×)
  ③ 초기 탈리튬화에서 급상승 (NMC333 418×) ④ x = 0.5–0.75 사이 재상승 굴곡.
- Fig 2c 안의 전압 주석: **~3.65 V (x≈0.1) · ~3.80 (x≈0.3) · ~3.95 (x≈0.5) · ~4.10 (x≈0.75)**.
  ⚠ **근접 배치로 읽은 대응**이며, 이것은 **완화 후 OCV** 이지 §4-5 의 상한 충전전압(4.7/4.8 V) 이 아니다.

### 5-4. 이온전도도·확산도 — **Table II (완전 리튬화 시료, stated)**

| T (°C) | D (cm² s⁻¹) | σ_ion (S cm⁻¹) | 조성 | 기법 |
|---|---|---|---|---|
| 51 | 2.2 × 10⁻⁸ | **9.1 × 10⁻⁹** | NMC333 | AC |
| 61 | 5.5 × 10⁻⁸ | 2.1 × 10⁻⁸ | NMC333 | AC |
| 50 | 1.5 × 10⁻⁸ | **8.7 × 10⁻⁹** | NMC532 | AC |
| 60 | 4.5 × 10⁻⁸ | 9.3 × 10⁻⁹ | NMC532 | AC |
| 50 | 6.1 × 10⁻⁹ | 3.7 × 10⁻⁹ | NMC333 | DC (분극) |
| 50 | 7.6 × 10⁻⁹ | 3.7 × 10⁻⁹ | NMC333 | DC (탈분극) |

- 저자: *"This is to our knowledge the **first measurement** of these ion transport parameters in any
  **pure phase NMC** samples."*
- ⚠ **AC 와 DC 가 2–4× 차이** (같은 조성·같은 온도).  저자는 *"in good agreement"* 라 쓴다 —
  이 분야 기준으로는 맞지만, **우리가 인용할 때는 밴드(3.7–9.1 × 10⁻⁹ S cm⁻¹ @50 °C)로** 쓸 것.
- **D > σ_ion (수치상)** 의 설명: `D_Li ∝ σ_ion(x_ion/c_ion + x_eon/c_eon)` (Maier, ref 34).
  고온이라 캐리어 트래핑 최소 → x_ion, x_eon → 1; 희박결함 극한 `c_ion ≫ 1` → D 가 σ_ion 보다 큰 수치.
- **⚠ E_a(ion) 는 추출 불가** — PEO 막이 60 °C 이상에서 녹아 단락되므로 온도창이 너무 좁다 (저자 명시).

### 5-5. D̃_Li(x) @ RT — **Table III (stated)** + Fig 6

**Table III — 본 연구 + 문헌 비교 (원표 그대로)**

| 기법 | T (°C) | 조성 | D (cm² s⁻¹) | 출처 |
|---|---|---|---|---|
| AC | 60 | LiNi₀.₅₀Mn₀.₂₀Co₀.₃₀O₂ (NMC532) | 4.5 × 10⁻⁸ | 본 연구 |
| AC | 61 | LiNi₀.₃₃Mn₀.₃₃Co₀.₃₃O₂ (NMC333) | 5.5 × 10⁻⁸ | 본 연구 |
| DC | 50 | NMC333 | 7.6 × 10⁻⁹ | 본 연구 |
| **탈분극** | **25** | **Li₀.₉₀NMC333** (x = 0.10) | **4.1 × 10⁻¹⁰** | 본 연구 |
| **탈분극** | **25** | **Li₀.₂₅NMC333** (x = 0.75) | **1.3 × 10⁻¹⁰** | 본 연구 |
| **탈분극** | **25** | **Li₀.₉₀NMC532** (x = 0.10) | **4.6 × 10⁻¹⁰** | 본 연구 |
| **탈분극** | **25** | **Li₀.₂₅NMC532** (x = 0.75) | **2.5 × 10⁻¹⁰** | 본 연구 |
| GITT | 25 | NMC333 (리튬화) | ∼10⁻¹² | Wu 2012 (ref 19) |
| GITT | 25 | Li₀.₂₅NMC333 | ∼10⁻¹⁰ | Wu 2012 (ref 19) |
| GITT | 25 | NMC333 | ∼10⁻¹⁰ | Hao 2010 (ref 20) |
| CV | 25 | NMC333 | ∼5 × 10⁻¹⁴ | Gu 2015 (ref 21) |
| CV | 25 | NMC333 | ∼3 × 10⁻¹⁰ | Li 2014 (ref 23) |

- 본문: *"Our diffusivity data are higher, and lie between **5.0 × 10⁻¹⁰ to 1.3 × 10⁻¹⁰ cm² s⁻¹**
  over the lithium content from **x = 0.05 to x = 0.75**."*
- **Fig 6 digitized (NMC532, 빨간 원, 15점)** — Table III 두 점과 **정확히 일치**해 캘리브레이션 검증됨
  (x = 0.10 → 4.56 × 10⁻¹⁰ vs 표 4.6 × 10⁻¹⁰; x = 0.75 → 2.53 × 10⁻¹⁰ vs 표 2.5 × 10⁻¹⁰):

  | x | 0.05 | 0.10 | 0.15 | 0.20 | 0.25 | 0.30 | 0.35 | 0.40 | 0.45 | **0.50** | 0.55 | 0.60 | 0.65 | 0.70 | 0.75 |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
  | D (10⁻¹⁰ cm² s⁻¹) | 5.0 | 4.6 | 3.4 | 3.4 | 3.1 | 2.6 | 2.2 | 2.1 | 2.0 | **1.9 (최소)** | 2.2 | 2.3 | 2.4 | 2.4 | 2.5 |

- **NMC333 (검은 사각)**: Table III 의 두 stated 점(4.1 × 10⁻¹⁰ @x=0.10, 1.3 × 10⁻¹⁰ @x=0.75) 사이에서
  **x ≈ 0.55 부근 최소 ≈ 10^−10.06 ≈ 8.7 × 10⁻¹¹ cm² s⁻¹** (⚠ **이 최소값만 시각 판독** — 벡터
  추출에 검은 사각 계열이 안 잡혀 중간점은 digitize 하지 못했다.  **표 두 점은 stated 라 안전**).
- 본문 정성: *"the ionic diffusivity varies with x by **almost an order of magnitude in NMC333**,
  and somewhat less in NMC532"* — 우리 판독(4.1 → 0.87 × 10⁻¹⁰ = 4.7×)과 정합.
- **NMC532 > NMC333 전 구간** — 저자 설명: NMC333 의 **Mn⁴⁺ 농도가 더 높아** Li⁺ 와 상호작용이
  강해 이동도를 떨어뜨릴 수 있다.

### 5-6. ★ DERIVED — 우리가 직접 계산한 파생비 (stated ÷ digitized 혼합, 라벨 필수)

| 양 | 값 | 어떻게 |
|---|---|---|
| **σ_e / σ_ion (NMC333, 51 °C, 리튬화)** | ≈ **18** (t_ion ≈ 0.05) | σ_ion 9.1 × 10⁻⁹ (stated) ÷ σ_e 1.7 × 10⁻⁷ (Fig 2b Arrhenius 외삽) |
| **σ_e / σ_ion (NMC532, 50 °C, 리튬화)** | ≈ **6 × 10²** (t_ion ≈ 0.002) | σ_ion 8.7 × 10⁻⁹ (stated) ÷ σ_e 5.2 × 10⁻⁶ (Fig 2a 외삽) |
| **σ_ion(NMC) / σ_ion(LPSCl)** | ≈ **1/(3 × 10⁵)** | 9.1 × 10⁻⁹ S cm⁻¹ (51 °C) vs 우리 σ_grain 3.0 mS cm⁻¹ (25 °C) |
| **σ_ion(NMC) / σ_ion(LPSCl pellet)** | ≈ **1/(1 × 10⁵)** | 위 vs Bazzoun 펠릿 1.02 mS cm⁻¹ |
| **σ_e 상승배 (x 0 → 0.75)** | NMC333 **1.6 × 10⁵ ×** · NMC532 **7.3 × 10³ ×** | Fig 2c digitized |
| **σ_e 상승배 (x 0 → 0.10)** | NMC333 **418 ×** · NMC532 **152 ×** | Fig 2c digitized |
| **100 °C, x = 0.75 σ_e** | NMC532 **19.7** · NMC333 **16.2** mS cm⁻¹ | Fig 2c 값 × Arrhenius(E_a 0.05 / 0.10 eV) |

⚠ **AM 이온전도 비교는 온도가 불리하게 어긋나 있다** — NMC 는 **51 °C**, LPSCl 앵커는 **25 °C** 다.
NMC 의 E_a(ion) 은 추출 불가(§5-4)이나 양수일 것이므로 **RT 대비는 위 값보다 더 커진다**
⇒ **"AM 은 LPSCl 보다 이온적으로 ≥10⁵ 배 나쁘다"** 는 **보수적(하한) 서술**이다.

---

## 6. Figure set ★

| Fig | 내용 | **우리가 재사용할 것** |
|---|---|---|
| **1a** | 리튬화 NMC532 의 Ag/NMC/Ag 임피던스 (48 °C, 68 °C).  거의 완전 반원, Re(Z) ~1 × 10⁴–5 × 10⁴ Ω | "이온차단 셀에서 반원 1개 = 전자지배" 판정 템플릿 |
| **1b** | 등가회로 **R ∥ CPE** | 우리 EIS 모듈(`eis_drt_ica.py`) 의 최소 회로 대조 |
| **1c** | DC 분극 전압-시간 (30 % 탈리튬 NMC333).  0→120 mV **계단**, 0–1200 s | ★ **전자/이온 판별의 시간영역 지문** — 우리 STEP4 분극 해석과 같은 논리 |
| **2a** | **NMC532 Arrhenius** 5조성 (log σ vs 1000/T, −6…−2) + **색-일치 E_a 라벨** (빨강 Lithiated 0.42 → 파랑 75 % 0.05) | ★ σ_e(T) — 우리 온도의존 훅의 유일한 AM 앵커.  **30 %(보라)·50 %(초록) 곡선이 거의 겹침** |
| **2b** | **NMC333 Arrhenius** 5조성 (−8…−2) + **색-일치 E_a 라벨** (빨강 x=0 0.48 → 자홍 x=0.75 0.10) | ★ 동일.  **x = 0 곡선(빨강)이 우리 `discharged` 라벨의 직접 반증** — 25→110 °C 전 구간이 10⁻⁷ 대 |
| **2c** | ★★★ **σ_e vs x @30 °C, 두 조성** + OCV 주석 | ★★★ **이 카드의 핵심.  우리 σ_AM/σ_S/σ_P 판정의 근거** |
| **3a** | Li/PEO/NMC/PEO/Li 임피던스 (NMC333, 61 °C) + 고주파 인셋.  **5.23 × 10⁻⁵ Hz → D = 5.54 × 10⁻⁸ cm²/s** | 전자차단 셀 Warburg 로 σ_ion·D 를 동시에 뽑는 법 |
| **3b** | 등가회로 **R1–CPE1–Ws1–CPE2** | 위 |
| **4a** | DC 분극/탈분극 전압-시간 (~50 °C), 0–6 × 10⁵ s, 0–300 mV | τ_δ 규모 감각 (수 10⁵ s = 며칠) |
| **4b** | `ln|U−U∞|` vs t 피팅, **R = 0.99087 / 0.99754**, D = 6.05 / 7.55 × 10⁻⁹ | Eq 1 피팅 품질 |
| **5a** | NMC532 단계 적정 셀전압 vs 시간 (3.6→4.6 V, 0–600 h), 10 h 인가 + OCV 완화 | 우리 GITT-류 프로토콜 대조 |
| **5b** | 탈분극 피팅 (R = 0.99864) | 위 |
| **6** | ★ **D̃_Li vs x @RT, 두 조성** (log D −10.5…−9) | ★ **우리 STEP4 D_s 의 독립 대조** (§7-3) |

⚠ **오차막대 없음** — 어느 그림에도 반복측정 산포가 표시되지 않는다.  E_a 에만 ±0.03 eV 가 붙는다.
⇒ **replicate 밴드를 쓸 수 없다** (Bazzoun Table S1 과 대조적).

---

## 7. Post-processing ★ / 논지 흐름

### 7-1. σ_e 의 기전 (저자 논지)
1. **관찰**: σ_e 가 x 와 함께 단조 증가.  초기 탈리튬화에서 **급상승** → 기울기 완만 →
   **x = 0.5–0.75 사이 재상승 굴곡**.
2. **전자구조 논거**: Co³⁺, Ni²⁺, Ni⁴⁺ 는 모두 (t₂) 궤도가 **채워져 있어** 전자 비편재화가 어렵다.
   Ni 존재 하에서 Co 는 3+ → 4+ 산화가 잘 안 된다 (ref 32 Carlier/Delmas).
3. **기전**: 탈리튬화 → **Ni³⁺/Ni⁴⁺ 혼합원자가** → 좁은 (Ni⁴⁺/Ni³⁺) 밴드에 **정공** 형성 → σ_e↑.
4. **E_a 0.42–0.05 eV** = 혼합원자가계 **small polaron** 이동의 전형 (ref 31 Maxisch–Zhou–Ceder);
   Saadoune–Delmas 의 LiₓNi₀.₈₀Co₀.₂₀O₂ 와 같은 크기 (ref 30).
5. **x = 0.5–0.75 굴곡**: 자신들의 NCA 연구(ref 33)에서 60 % 탈리튬 이후 급상승을 **Co³⁺→Co⁴⁺ 소량
   산화**로 설명한 바 있고, NMC 패턴이 유사하므로 **Co 산화 개시 가능성** 제시.  ⚠ **직접 증거 없음
   (XAS 등 분광 미수행)** — 저자도 *"It seems that there may also be…"* 로 약하게 쓴다.
6. **조성 차**: 리튬화 NMC532 > NMC333 → **Ni 함량**.  30 % 탈리튬 이후 소멸.

### 7-2. D̃(x) 의 기전 — **여기가 이 논문에서 가장 미묘한 부분**
- **관찰**: D̃ 가 x = 0 → 0.5 에서 **감소**하고, x > 0.5 에서 **다시 증가**.
- **모순 지적 (저자 스스로)**: 문헌 구조연구(refs 12, 17)는 탈리튬화에 따라 **격자(c축)가 팽창**한다고
  보고한다.  c 축 팽창 = Li slab 간격 증가 = 이동 활성화에너지 **감소** = D **증가** 여야 한다
  (refs 35 Van der Ven–Ceder, 36 Kang–Ceder).  **관측은 반대다.**
  저자 표현: *"This is surprising"*, *"suggests more subtle cation ordering effects that remain to be resolved."*
- **x < 0.5 설명 (내인성)**: **Frenkel 점결함 평형**에서 확산이 **격자간(interstitial) 농도**에 의존한다면,
  공공(vacancy) 농도가 늘수록 격자간 농도는 줄어 D 가 **감소**한다.
- **x > 0.5 설명 (⚠ 외인성 = artifact)**: **electrochemical shock** (열충격의 전기화학판;
  Woodford–Carter–Chiang refs 37–39).  층상 산화물의 **이방성 화학팽창**이 결정립 간 **misfit 응력**을
  만들고(그 크기는 **SOC 의존이지 C-rate 의존이 아니다**), 생긴 **미세균열이 액체 전해질로 채워져
  빠른 수송경로**가 된다 → **유효 확산길이 감소** → **겉보기 D 증가**.
  ★ 저자 결론: **x > 0.5 의 이온 데이터는 진짜 물성이 아니다.**
- ★ **σ_e 는 이 균열에 영향받지 않는다**고 명시 (*"Electronic conductivity was not apparently affected
  by these effects"*).  ⇒ **σ_e(x) 곡선은 x = 0.75 까지 신뢰 가능, D(x) 는 x ≤ 0.5 까지만.**

### 7-3. 최종 결론 (Conclusions 절)
- NMC 는 x = 0.0–0.75 에서 **반도체적** 전자전도.
- σ_e 상승 = **Ni³⁺/Ni⁴⁺ 다가성**, **초기 10 % 탈리튬화에서 특히 급격**.
- **75 % 부근 2차 상승 굴곡** = Co³⁺/Co⁴⁺ 다가성 개시 가능성.
- D̃ 는 최소 x = 0.5 까지 **감소** — 격자상수 추세와 반대라 **cation ordering** 미해결 과제.
- ★★ **"chemical diffusion is always limited by lithium ion transport rather than electronic
  conductivity"** — 측정 전 구간에서.
- *"From the reported ion transport coefficients, kinetic requirements such as the **particle size**
  necessary for particular charge/discharge times can be readily calculated."*
  ⇒ **저자 자신이 이 데이터의 용도를 "입경 설계" 로 지목한다** — 우리 AM 입경 스윕과 같은 자리.

---

## 8. 우리 DEM+MPM 대비 (frame[4]·frame[5])

> ⚠ **이 논문에는 DEM·MPM·접촉역학이 하나도 없다.**  frame[4] 교차검증 상대가 **아니다** —
> **재료 입력 앵커**다.  분리 규약대로 접촉역학·DFT 는 섞지 않는다.

| 항목 | 이 논문 | 우리 | 판정 / 이유 |
|---|---|---|---|
| **σ_AM (솔버 σ_bulk)** | 5.0 × 10⁻⁸ … 1.4 × 10⁻² S cm⁻¹ (x 0→0.75, 30 °C) | **0.05 S cm⁻¹**, 라벨 `discharged` | ⛔ **밴드 밖 3.6× (최대 대비) · 라벨 상태 대비 10⁶×.  라벨 수정 필수** |
| **σ_S / σ_P (Stage 22.5 LOCKED)** | 위 밴드 | **10 / 5 mS cm⁻¹** | ✅ 밴드 **안**, 단 **충전 끝단(x ≈ 0.64–0.71)** — "top-of-charge-like" 로 서술 |
| **σ_AM_S / σ_AM_P (STEP3)** | 위 밴드 | **10 / 5 mS cm⁻¹** | ✅ 동일 판정.  코드가 이미 `corpus-fit endpoints, NOT a … measurement` 라 정직 |
| **σ_e 의 SOC 의존** | **4–5 자릿수** | **없음** (x 무관 스칼라) | ⚠ **정직한 모델 한계.**  방전 상태 전극의 σ_e 를 우리가 크게 과대평가한다 (→ §9-③) |
| **σ_e 의 조성 의존** | Ni 0.33 → 0.50 에서 **37.6×** (단 x=0 에서만) | `(σ_S·NCM_S)^(1−p)·(σ_P·NCM_P)^p` — **입경/결정성** 축만 | ⚠ 우리 폼에 **Ni 함량 축이 없다**.  단일 소재(811)만 쓰므로 지금은 무해 |
| **NCM(r) GB 인자** | ⚠ **입경 의존을 재지 않았다** (소결 펠릿, 결정립 크기 미보고) | `1/(1+(r/2µm)^1.5)` | ⚠ 이 논문은 이 인자에 **무관(silent)**.  Trevisanello 카드의 "오귀속" 판정은 **그대로 유지** |
| **AM 이온전도** | **9.1 × 10⁻⁹ S cm⁻¹** (51 °C) = LPSCl 의 **1/(3 × 10⁵)** | 이온망에서 **AM = 절연(σ_ion = 0)** | ✅✅ **우리 가정이 실측으로 정당화된다** — 이 카드 최대의 "우리에게 유리한" 결과 |
| **AM 전자전달수 t_e** | 리튬화에서도 **0.95–0.998** (DERIVED §5-6) | AM = 전자망 전용 | ✅ **상 배정이 옳다** — AM 은 리튬화 상태에서조차 전자 지배 |
| **D_s (STEP4)** | **1.3–5.0 × 10⁻¹⁰ cm² s⁻¹ = 1.3–5.0 × 10⁻¹⁴ m² s⁻¹** (RT, 화학확산) | poly 기본 **3 × 10⁻¹⁴ m² s⁻¹** · Chen2020 4 × 10⁻¹⁵ · SC 밴드 1.5 × 10⁻¹⁵–1 × 10⁻¹⁴ | ★ **우리 기본 3e−14 가 밴드 안 (§7-3 주의 필수)** · Chen2020 4e−15 는 **3–12× 아래** |
| **미세균열 → 빠른 경로** | x > 0.5 에서 **관측·명시** (electrochemical shock) | fracture(Auerbach) + dead-AM + `cycle_contact_ledger` | ★ **같은 기전을 반대 부호로 본다** (§9-④) |
| **모델링 검증 대상** | 없음 (순수 실험) | — | frame[4] 아님 |

### ★ 반드시 붙일 통제 경고 (over-claim 방지)
1. **소결 세라믹 ≠ 전극 입자.**  900 °C · 12 h 소결은 상용 CAM 분말과 **결정립 크기·화학량론·표면상**
   이 다를 수 있다.  ⚠ 논문은 **결정립 크기를 보고하지 않으며**, 자신들의 출발 분말과도 비교하지 않는다.
2. **조성 다름 (333/532 vs 우리 811).**  §3-4(ii) — **방향만, 밴드만, 자릿수만.**  절대값 전이 금지.
3. **2-단자 대칭셀.**  4-probe 가 아니다.  Ag 접촉저항이 EIS 로 분리됐다는 근거는 **"반원 1개 +
   C ≈ 5 × 10⁻¹¹ F"** 이며, 이는 강하지만 **접촉 기여의 정량 상한을 제시하지는 않는다.**
4. **digitized ≠ stated.**  §3-2·§5-3 표는 전부 digitized (±0.05 dex).  §5-4·§5-5 Table 은 stated.
   **혼동 금지** — 원고에는 stated 값을 쓰고, x-의존 곡선은 "digitized from Fig 2c (TREND)" 로.
5. **D 는 화학확산 D̃, 우리 D_s 는 고체확산.**  §7-3 주의 참조 — **같은 양이 아니다.**
6. **다공도 σ ∝ 밀도 선형 가정** (§4-1) — 96–98 % 라 ≤4 % 지만 검증되지 않은 규약이다.

---

## 9. 적용 인사이트 — 우리 연구에 어떻게 (실행 가능한 형태)

**① ★★★ σ 표에 `kind` 열 + SOC 표기 (원고, 즉시).**
`measured (bulk, sintered pellet)` / `effective (corpus-calibrated)` / `effective network constant`.
σ_AM 행에는 반드시 **"어느 x 를 대표하는지"** 를 적는다.  §3-5 제안 1–4 문장 그대로 쓸 수 있다.
CL-47 이 σ_VGCF 100 에 대해 요구한 **범주 라벨링 규율의 σ_AM 판**이다.

**② ★★ σ_AM 감도 프로브 (사전등록 대상, CL-48 형식).**
`SIGMA_AM_ELECTRONIC` 을 **0.05 → 0.0138 S cm⁻¹** (이 논문의 30 °C 실측 **최대**) 로 바꿔
σ_e **비(ratio)** 와 **절대값**이 각각 얼마나 움직이는지 잰다.
- 근거: **CL-39 가 σ_VGCF ×1.44 에서 비는 불변(ΔR = 0.0036)이고 절대값은 +39 % 움직임**을 이미 쟀다.
  σ_AM 은 채널이 다르므로 **그 결과를 그대로 못 옮긴다** → 별도 프로브가 필요하다.
- ⚠ **폼(Stage 22.5)은 건드리지 말 것** — CLAUDE.md A1 노트대로 엔드포인트는 코퍼스 적합값이고,
  솔버 σ_bulk 만 재조사한다.  σ_bulk 를 3.6× 낮추면 σ_e 사다리 전체가 이동하므로
  **원고 수치에 영향이 가는 변경이다 → 반드시 런 전에 등록.**
- 값 자체보다 **"비가 σ_AM 에 둔감한가"** 가 결론이다 — 둔감하면 우리 상대비교 결과 전부가 안전하고,
  라벨만 고치면 된다.

**③ ★★ SOC-의존 σ_e 훅 (신규 기능 후보).**
지금 우리 σ_e 는 **x 무관**이다.  이 논문이 **σ_e(x) 곡선을 그대로 제공**하므로,
STEP4 가 이미 x(t) 를 알고 있는 만큼 **`σ_AM(x) = σ_AM,ref · 10^(f(x))`** 형태로 연결할 수 있다.
- 즉시 효과: **방전 심부에서 전자망이 실제로는 훨씬 나쁘다** → 저 SOC 율특성 저하의 기전 후보.
- ⚠ **조성 전이 문제**가 그대로 남는다 (333/532 곡선을 811 에 못 씌운다) → **형상(shape) 만 빌리고
  진폭은 우리 σ_AM 으로 고정**하는 형태여야 한다 (§F1 ASSUMED-FORM 라벨).
- ⚠ 다른 훅과 충돌 점검: `--sigma-am-e` (voxel), `--cam nca` 프리셋, coating 프리셋.

**④ ★ x > 0.5 미세균열 = 우리 fracture 채널의 **외부 실험 증거**.**
저자는 **이방성 화학팽창 → 결정립 misfit 응력 → 미세균열**을, 그리고 그 크기가 **SOC 의존이지
C-rate 의존이 아님**을 명시한다 (refs 38, 39).
- 우리 `cycle_contact_ledger.py` 의 `--poly-mode expand-void` 가 **정확히 이 그림**이다
  (poly 내부 void, 계면 유지) — **이 논문이 그 가정의 문헌 근거가 된다.**
- ⚠ 부호 주의: **여기서는 균열이 D 를 *올린다*** (액체가 채워 빠른 경로).  **ASSB 에서는 SE 가
  못 들어가므로 반대 부호**다 (Trevisanello 카드가 이미 확립한 액체↔고체 역전).
  ⇒ **전이할 것은 "SOC-의존 misfit 응력 → 균열" 이라는 구동력뿐이고, 수송 결과는 전이 금지.**
- ★ 추가 정량: 저자는 **75 % 탈리튬 이상에서 시료가 셀 조립조차 불가능할 만큼 부서졌다**고 적는다
  (*"too fragile to assemble into cells, due to the intercalation-induced dimensional changes at the
  crystallite level"*).  = **x = 0.75 가 이 소재계의 기계적 실사용 상한** 이라는 실험 서술.

**⑤ ★ AM = 이온 절연체 가정의 정량 근거 (원고에 바로 쓸 수 있음).**
σ_ion(NMC) ≈ 9.1 × 10⁻⁹ S cm⁻¹ (51 °C) vs LPSCl 3.0 mS cm⁻¹ ⇒ **≥3 × 10⁵ 배 차 (보수적 하한)**.
우리 DEM 이온망이 AM 을 제외하는 것, STEP3 가 `PHASE_SIGMA['ionic']['AM'] = 0.0` 인 것이
**임의 가정이 아니라 실측이 지지하는 근사**임을 한 줄로 방어할 수 있다.

**⑥ ★ STEP4 D_s 의 독립 대조 — 단, 규약이 다르다.**
우리 poly 기본 **3 × 10⁻¹⁴ m² s⁻¹** 은 이 논문 RT 밴드 (1.3–5.0 × 10⁻¹⁴ m² s⁻¹) **안**이다.
⚠ **그러나 "일치" 라고 쓰면 안 된다** — 세 가지가 다르다:
1. **화학확산 D̃ vs 고체확산 D_s.**  D̃ = D_self × **열역학 인자**(단상 구간에서 10–100× 될 수 있음).
   D̃ 가 더 큰 것은 **당연**하고, 그것만으로 검증이 되지 않는다.
2. **확산길이 규약**: 이 논문은 **펠릿 두께의 1/2** 을 쓰고, Chen2020 계열은 **입자 반경**을 쓴다.
3. **x > 0.5 값은 저자 스스로 균열 artifact 라 했다** → 밴드의 상단이 오염돼 있다.
⇒ 정직한 서술: *"our default D_s lies within the range of the only pure-phase NMC chemical-diffusion
measurement, but the two are different coefficients (chemical vs solid-state) with different length
conventions, so this is a **plausibility check, not a validation**."*

---

## 10. 저자가 밝힌 한계 (원문 기반)

1. **σ_e 를 75 % 탈리튬화 이상에서 못 쟀다** — *"the samples became too fragile to assemble into
   cells, due to the intercalation-induced dimensional changes at the crystallite level."*
2. **x > 0.50 의 이온 데이터는 외인성(extrinsic)** — 전기화학 충격 미세균열이 액체 전해질로 채워져
   빠른 경로를 만든다 → 겉보기 D 증가.  **σ_e 는 영향 없다**고 명시.
3. **PEO 셀 60 °C 상한** — 막이 녹아 단락.  NMC532 는 60 °C 미만에서 주파수창이 부족해
   **저주파 모델 피팅을 완화주파수까지 외삽**했다 (⚠ 그 온도들의 D 는 **부분적으로 외삽값**).
4. **E_a(ion) 추출 불가** — 온도창이 좁아 신뢰할 수 없음.
5. **σ_ion·D 는 250 mV 분극에 해당하는 Li 조성 구간의 평균값.**
6. **확산길이 = 두께/2 가정** (전 구간).
7. **D̃(x) 추세가 격자상수 추세와 반대** — 미해결.  *"more subtle cation ordering effects that
   remain to be resolved."*
8. **문헌과의 불일치를 자기 데이터로 못 닫는다** — 기존 NMC333 D 문헌이 **10⁻¹⁴ ~ 10⁻¹⁰** 로
   4 자릿수 흩어져 있고 (Gu CV 5 × 10⁻¹⁴ vs Li CV 3 × 10⁻¹⁰), 저자는 *"extrinsic factors may contribute
   … due to the composite samples used, and that none may represent the pure single phase transport
   behavior"* 라고만 한다.
9. **Co 산화 가설에 직접 분광 증거 없음** (NCA 유사성 논증뿐).

### ⚠ 우리가 추가로 다는 한계 (논문이 말하지 않은 것)
- **결정립 크기 미보고.**  900 °C 12 h 소결체의 grain size 를 안 준다 → GB 밀도를 우리 NCM(r) 인자와
  대볼 수 없다.  ⇒ **이 논문은 NCM(r) 에 대해 무관(silent)** 이며, Trevisanello 오귀속 판정을 대체하지 않는다.
- **반복측정·산포 없음.**  단일 시료·단일 곡선.  밴드로 못 쓴다.
- **소결 후 조성 확인 없음** (대기 소결 900 °C 12 h 에서 Li 손실 가능성에 대한 XRD/ICP 보고 없음).
- **NMC811 에 대해서는 아무 말도 하지 않는다.**  ⇒ **811 값의 출처로 이 논문을 인용할 수 없다.**
  인용 가능한 것은 **"NMC 계열의 σ_e 밴드와 그 SOC 의존"** 뿐이다.

---

## 11. 기법 미니 용어집 (이 카드를 자립시키기 위해)

- **Ion-blocking cell (이온차단 셀)**: 전극(Ag)이 Li⁺ 를 주고받지 못하므로 정상상태에서 **전자만**
  전류를 나른다 → **σ_e** 를 잰다.  DC 에서 전압이 계단으로 서면 전자 지배.
- **Electron-blocking cell (전자차단 셀)**: Li|PEO|…  PEO 는 Li⁺ 전도체이나 전자 절연체 →
  정상상태에서 **이온만** 나른다 → **σ_ion**.  전자가 막히면서 생기는 농도 구배가 **Warburg(화학량론 분극)**.
- **Stoichiometric polarization**: 혼합전도체에서 한 캐리어를 막으면 시료 내부에 **조성(stoichiometry)
  구배**가 서며 생기는 분극.  그 완화시간이 **τ_δ = L²/(π²D̃)**.
- **CPE (constant phase element)** 와 `C = (R^(1−n)Q)^(1/n)`: 눌린(depressed) 호를 가진 실계에서
  **유효 커패시턴스**를 뽑는 표준식.  **n = 1 이면 이상 커패시터**.  여기서 n = 0.90–0.96.
- **커패시턴스로 grain / GB 판별**: 벌크(grain) 응답은 **~10⁻¹¹ F** 급, 입계는 **~10⁻⁹–10⁻⁷ F** 급.
  5 × 10⁻¹¹ F ⇒ **grain**.  (Brick-layer 모델의 표준 판별법.)
- **Small polaron hopping**: 전자(정공)가 국소 격자 변형과 함께 이동 → **열활성화**, E_a ~0.1–0.5 eV.
  혼합원자가(Ni³⁺/Ni⁴⁺)가 호핑 자리를 만든다.
- **화학확산 D̃ vs 자기확산 D_self**: `D̃ = D_self × (d ln a / d ln c)` (열역학 인자).
  **GITT/PITT/전압완화가 주는 것은 D̃** 이고, **입자 내 확산 모델(우리 STEP4)이 쓰는 것은 D_s** 다.
- **Electrochemical shock**: 열충격의 전기화학판.  삽입/탈리에 따른 **이방성 화학팽창**이 결정립 간
  misfit 응력을 만들어 균열을 낸다.  크기는 **SOC 의존, C-rate 무관** (Woodford–Carter–Chiang).

---

## 12. 인용 가능 문장 (deck / 원고용)

- "Amin and Chiang (*J. Electrochem. Soc.* **163**, A1512, 2016) measured the electronic and ionic
  transport of **additive-free, single-phase sintered NMC333 and NMC532 pellets** (96–98 % relative
  density) using ion-blocking (Ag/NMC/Ag) and electron-blocking (Li/PEO/NMC/PEO/Li) cells.  The
  electronic conductivity rises from **∼10⁻⁷ to ∼10⁻² S cm⁻¹** as x in Li₁₋ₓNMC goes from 0 to 0.75,
  with activation energies falling from **0.42–0.48 eV to 0.05–0.10 eV** — small-polaron transport
  enabled by Ni³⁺/Ni⁴⁺ mixed valence."
- "Because σ_e of NMC varies by four to five orders of magnitude across the operating window, **any
  single scalar AM conductivity is an operating-point average**; we therefore label ours *effective*
  and state the state of charge it represents."
- "The lithium-ion conductivity of pure-phase NMC is **∼9 × 10⁻⁹ S cm⁻¹ at 51 °C**, i.e. more than
  **five orders of magnitude below** argyrodite Li₆PS₅Cl.  This justifies treating the active material
  as ionically blocking in the composite ionic network."
- "The authors report that beyond 75 % delithiation the pellets **could no longer be assembled into
  cells** because of intercalation-induced dimensional change at the crystallite level, and attribute
  the apparent rise of D̃ above x = 0.5 to **electrochemically-induced microfracture** whose magnitude
  is state-of-charge — not C-rate — dependent."
- ⚠ **쓰면 안 되는 문장**: *"our σ_AM = 50 mS/cm agrees with literature"* / *"NMC811 σ_e ≈ 50 mS/cm
  (Amin & Chiang)"* — **이 논문은 811 을 재지 않았고, 잰 밴드의 최댓값보다 우리 값이 3.6× 위다.**

---

## 13. 관련 카드 (litdb 내부 교차참조)

- `trevisanello2021_sc_pc_ncm_cracking_diffusion` — **σ_S/σ_P 오귀속 판정의 원본.**
  이 카드가 그 판정을 **뒤집지 않는다**: Trevisanello 는 σ_e 를 안 쟀고, 본 논문은 SC/PC(결정성) 축을
  안 쟀다.  두 카드는 **서로 다른 구멍**을 메운다 — 본 카드는 **절대 밴드**, Trevisanello 는 **결정성 방향**.
- `oh2026_bimodal_composite_cathode` — Table S15 σ_NCWA 13.7 / σ_NCM 2.45 mS cm⁻¹ (모델 입력).
  §3-6 사다리에서 **x ≈ 0.75 / 0.56** 에 대응.
- `zhang2023_pfib_multiscale_imaging_4d_thick_cathode` — σ_AM 5 × 10⁻⁵ S cm⁻¹ (SI ref Wang 2018).
  §3-6 사다리에서 **x ≈ 0.07–0.15**.  `comparison_vs_ours_DEM.md §B` 의 "200× 불일치" 항목이
  **이 카드로 SOC 축으로 재해석된다.**
- `bazzoun2026_dem_fem_rnm_ionic` · `minnmann2022_designing_cathodes_solidstate` — **이온** 쪽 절대 앵커.
  본 카드는 그 **전자** 쪽 짝이다 (단 복합체 유효값이 아니라 **AM 상 재료값**).
- `luan2025_graded_cathode_400whkg_pouch` — φ_AM < 0.3 외삽 금지(퍼콜레이션).  **본 카드는 σ_AM 의
  *크기* 축, Luan 은 φ_AM 의 *문턱* 축** — 둘이 σ_e 폼의 서로 다른 유효범위 경계를 정한다.

---

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

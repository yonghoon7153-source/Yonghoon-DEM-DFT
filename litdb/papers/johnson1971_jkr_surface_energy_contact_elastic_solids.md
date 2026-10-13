<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 이웃 = faka2026_particle_size_consolidation_strain_lpscl.md ·
     스캔 고전 메타 형식 = molerus1975_theory_of_yield_cohesive_powders.md (DOI 미인쇄 동류).
     원문 = JSTOR 표지 1 쪽 + 본문 13 쪽 (600 ppi 1-bit 스캔, 텍스트층 OCR).  SI 없음.
     쪽 표기 = 인쇄 (학술지) 쪽.  PDF n 쪽 = 인쇄 (299 + n) 쪽 → PDF 2 = p.301 · PDF 4 = p.303 (Fig 1) · PDF 8 = p.307 (식 18–21) · PDF 14 = p.313.
     판독 규약: OCR 이 식을 깨뜨린다 (예: 식 (19) 가 "a3 = K (P + 3yTrTR …").  식 · 수치 · 그림 축은 전부 600 dpi 쪽 이미지에서 읽었다.
     값 표지: [인쇄] = 원문 본문 · 식 · 캡션 / [판독] = 그림에서 읽은 값 (litdb/figures/<slug>/digitized.csv) /
     [우리 산술] = 원문 식 · 값으로 한 계산 또는 이 논문 밖 값과 엮은 계산 (가정 명시) / [추정] = 우리 해석 / [미확인] = 원문에 없음. -->
# Surface energy and the contact of elastic solids — 표면 에너지가 있는 두 탄성 구의 접촉: 무하중에서도 유한한 접촉 반경 a³ = R(6γπR)/K · 떼는 힘 P = −(3/2)γπR (탄성률 무관) · γ = "energy of adhesion of **both** surfaces" — JKR 이론의 원전 (고무 · 젤라틴 구 실험) — Johnson · Kendall · Roberts (Proc. R. Soc. Lond. A 1971)

> slug `johnson1971_jkr_surface_energy_contact_elastic_solids` · DOI `[미확인]` · type `theory (adhesive elastic contact — energy balance, JKR) + experiment (optical contact radius of rubber · gelatine spheres, dry / water / SDS)` · PDF `303e5223-35._Surface_energy_and_the_contact_of_elastic_solids.pdf` · digested `2026-10-13` · status ✅
>
> **서지 (원문 인쇄)**: K. L. Johnson†, K. Kendall‡, A. D. Roberts§ — † University Engineering Department, Cambridge · ‡ Surface Physics Section, British Railways Technical Centre, Derby · § Surface Physics, Cavendish Laboratory, Cambridge · *Proc. R. Soc. Lond. A* **324**, 301–313 (1971) · "Printed in Great Britain" · Communicated by D. Tabor, F.R.S. — Received 5 February 1971 [인쇄 p.301].  JSTOR 표지: Vol. 324, No. 1558 (Sep. 8, 1971) · Stable URL `https://www.jstor.org/stable/78058` [인쇄 PDF 1 쪽].
> ⚠ **DOI 는 PDF 어디에도 인쇄돼 있지 않다** (표지 · 본문 14 쪽 텍스트층 검색 0 건) → `[미확인]` — 지어내지 않는다.
> ★ **이 카드가 맡는 일** — ① 정본 `hare2026_dem_pept_dry_mixing_nmc622_eirich` 의 ref [79] (JKR) 원전 · ② `dmt1975_adhesion_contact_deformation` 카드가 *"JKR 1971 = 유료/접근 불가"* 로 비워 둔 짝 · ③ 이종기술 논지 (`docs/hetero_thesis.md` §2-1) 의 **F = (3/2)π·W·R\*** 와 믹서 덱 (`scripts/make_mixer_deck.py`) 의 코팅 팔 (LC) 환산 · Codex HB-02 의 *"JKR pull-off 규약 2 배 모호"* 가 기대는 바로 그 식의 원문.
> **판독 원자료**: `litdb/figures/johnson1971_jkr_surface_energy_contact_elastic_solids/digitized.csv` (15 행 — Fig 2 · 3 · 4 · 5).

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 표면 에너지가 있으면 두 탄성 구는 Hertz 보다 큰 반경으로 붙고 (무하중에서도 a³ = R(6γπR)/K), 떼어 내려면 **P = −(3/2)γπR** 의 인장 하중이 필요하다 — 이 힘은 **탄성률과 무관**하다 [인쇄 식 (20)·(21) p.307].
여기서 γ 는 **두 표면을 합친 접착 에너지** (= 오늘의 접착일 W) 다 — 원문이 두 번 그렇게 정의하고 (p.304 · p.306), 운모 예 ("300 per surface" → γ 600, p.304) 와 고무 실측 (71 erg/cm² = *"각 표면 35"*, p.308) 도 그 규약으로 쓴다 [인쇄].

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ★ JKR 떼는 힘의 정확한 꼴 | **P = −(3/2)γπR** (식 21) · R = R₁R₂/(R₁+R₂) (식 9) · 탄성률 무관 ("which we note is independent of the elastic modulus") | [인쇄] p.305 · p.307 |
| ★ γ 는 표면 에너지인가 접착일인가 (Codex HB-02 의 "2 배 모호") | **접착일 W** — "γ is the energy per unit contact area (i.e. the two surfaces)" (p.304) · "γ is the energy of adhesion of *both* surfaces" (p.306, 식 14) · 실측 "total surface energy γ … 71 ± 4 erg cm⁻². This corresponds to an energy of 35 erg cm⁻² for each dry rubber surface" (p.308) · 운모 예 "γ = 600 … (for mica γ ≈ 300 erg cm⁻² per surface)" (p.304).  ⇒ 같은 물질이면 **P_c = (3/2)πWR\* = 3πγ_s R\*** (γ_s = 한 표면 에너지).  ⚠ 원문 스스로 식 (18) 뒤에서 γ 를 *"surface energy"* 라고도 부른다 — 하류 2 배 혼동의 뿌리 | [인쇄] p.304 · 306 · 307 · 308 |
| 무하중 접촉 반경 | a³ = R(6γπR)/K (식 20) · K = 4/3π(k₁+k₂) · k_i = (1−ν_i²)/(πE_i) | [인쇄] p.302 · 305 · 307 |
| 수정 Hertz (하중–반경) | a³ = (R/K)·{P + 3γπR + √[6γπRP + (3γπR)²]} (식 19) | [인쇄] p.307 |
| 근사 이론 (Hertz 응력 유지) | F_S ≈ πR₁R₂γ/(R₁+R₂) = πRγ (식 6) — 정확해 (식 21) 의 **2/3** | [인쇄] p.304 · [우리 산술] |
| 실험 검증 | 고무 (E 8×10⁶ dyn/cm² = 0.8 MPa) · 젤라틴 (3×10⁵ dyn/cm² = 30 kPa) · 광학 평활 (돌기 ≈20 nm) · 광학현미경으로 접촉 지름 | [인쇄] p.307–308 |
| 측정된 γ (= W) | 고무–고무 건조 **71 ± 4** · 고무 판 (Fig 3) 2×34 = 68 · 고무–물 계면 **3.4 ± 0.2** (한 계면) · 0.01 M SDS: 상한 0.05 · 젤라틴–Perspex **105 ± 10** (80–140) erg/cm² (= mJ/m²) | [인쇄] p.308 · 309 · 311 |
| 떼는 힘 실측 | 이론 근처 · 그러나 **점성 박리 (속도 의존)** 로 평형이 느림 — 예비 실험에서 ½–5 g 로 흩어짐 → "overload" 기법으로 재현성 확보 · 젤라틴은 음하중에서 이론과 "close agreement" | [인쇄] p.309–311 |
| 단단한 고체 (금속 · 유리) 에는? | **거칠기가 지배** — 돌기가 단단한 표면을 떼어 놓아 점착이 약하게 보이고, 접촉 면적 증가도 돌기 "penumbra" 때문 · "this approach … if one of the bodies is highly deformable" | [인쇄] p.312–313 |
| 우리 믹서 SJKR (CED) 와의 다리 | 원문에 없다 — §7-1 에서 유도: **떼는 힘을 맞추면 CED = [9·W·E\*²/(4π²R\*)]^{1/3}** · 이 식으로 LC 의 세 동종 쌍이 같은 W (parcel 규모 6.27–6.30 µJ/m²) 임을 확인 | [우리 산술] |

⛔ **한정어 (떼지 말 것)**: ① 이론은 **탄성 · 매끈한 구 · 준정적 · 점성 없음** ② 실험은 cm 크기 **고무 · 젤라틴** (E 0.03–0.8 MPa) — 우리 µm 분말 (LPSCl ≈ 22 GPa = 우리 DFT E_VRH · NCM811 다결정 2차입자 나노압입 138 ± 24 GPa · 미세인장 165 ± 7 GPa = 정본 `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile`) 과 탄성률이 10⁴–10⁷ 배 다르다 ③ 원문의 γ 는 **두 표면 합 (W)** — 표면 에너지 γ_s 와 섞지 않는다 ④ 원문은 **포아송비 값을 적지 않았다** — 이론선을 다시 그리는 우리 산술은 ν = 0.5 가정 ⑤ 단단한 고체에서 이 식의 매끈한 구 기하 (R\*) 가 성립한다는 근거는 원문에 없다 — 오히려 반대 서술 (p.312).

---

## 1. 한 줄 요약
매끈한 고무 · 젤라틴 구를 낮은 하중에서 맞대면 접촉원이 Hertz 예측보다 크고, 하중을 0 으로 낮춰도 유한한 크기에 머물며, 음의 하중을 걸어야 떨어진다 — 이것을 **탄성 에너지 · 하중의 위치 에너지 · 표면 에너지 (−γπa²) 의 합을 접촉 반경에 대해 최소화** 해 설명한다.
핵심은 표면 힘이 붙들고 있는 확대된 접촉원 가장자리에서 응력이 **인장 (무한대 특이)** 이 된다는 점 (Johnson 1958 의 평판 압자 해를 겹침) 이고, 그 결과 겉보기 Hertz 하중 P₁ = P₀ + 3γπR + √(6γπRP₀ + (3γπR)²) 가 나온다.
여기서 수정 Hertz 식 (19) · 무하중 반경 (20) · 떼는 힘 −(3/2)γπR (21) 이 따라 나오고, 떼는 힘은 탄성률과 무관하다.
고무–고무 (건조 · 물 · SDS) 와 젤라틴–Perspex 실험이 이 식을 맞히고, 물 속 접촉에서 얻은 계면 에너지로 Young 식이 예측한 접촉각 (64 ± 2°) 이 직접 잰 값 (66 ± 1°) 과 맞는다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| K. L. Johnson (Cambridge Univ. Engineering Dept.) · K. Kendall (British Railways Technical Centre, Derby) · A. D. Roberts (Cavendish Lab., Cambridge) | Proc. R. Soc. Lond. A **324**, 301–313 (1971) · 접수 1971-02-05 · D. Tabor 소개 | `[미확인]` (PDF 미인쇄) · JSTOR 78058 | **고무** (유리 거푸집 성형 · E 8×10⁶ dyn/cm²) · **젤라틴** (25 % 수용액 주조 · E 3×10⁵ dyn/cm²) · Perspex 평판 — **배터리 소재 아님** | 해석 이론 (에너지 평형) + 광학 접촉 반경 실험 |

| 원문 구조 | 쪽 | 내용 |
|---|---|---|
| 초록 · Introduction | 301–302 | 표면 힘 · 표면 에너지 · 고체 ↔ 액체 차이 |
| Observations on solid contact | 302 | Hertz 식 (1)–(2) · Roberts (1968a) · Kendall (1969) 의 "Hertz 보다 큰 접촉" 관찰 |
| Figure 1 | 303 | 접촉 기하 · 응력 분포 A/B/C · 하중–변위 경로 |
| Approximate theory | 304 | 식 (3)–(7) · F_S ≈ πRγ · 탄성률 무관 |
| Exact analysis | 304–307 | 식 (8)–(21) · 에너지 평형 · 안정 근 · 수정 Hertz · 떼는 힘 |
| Experimental | 307–311 | 고무 · 젤라틴 · Fig 2–5 · Young 식 (22) |
| Discussion · Conclusion | 311–313 | 금속 · 유리 점착 재해석 · 거칠기 · 결론 |
| References (21 편) | 313 | |

- 중복 확인 (2026-10-13): 정본 `litdb/papers/` 전수 목록에 johnson · jkr 파일 없음 · `git grep -i` 로 "contact of elastic solids" = `hare2026_…` 1 건 (인용) · "rspa.1971" · "jstor.org/stable/78058" 0 건 → 새 카드.

---

## 3. 핵심 식 · 수치 (★ 식 전수 — 600 dpi 쪽 이미지에서 옮겼다 · 식 영역 크롭 = `eq_*.png`)

### 3-1. 식 전수 [인쇄]
| 식 | 원문 (기호 그대로) | 뜻 | 쪽 · 크롭 |
|---|---|---|---|
| (1) | a₀³ = ¾π(k₁+k₂)·R₁R₂/(R₁+R₂)·P₀ · k₁ = (1−ν₁²)/(πE₁) · k₂ = (1−ν₂²)/(πE₂) | Hertz 접촉 반경 | p.302 · `eq_01_02_hertz.png` |
| (2) | δ³ = (9/16)π²(k₁+k₂)²·(R₁+R₂)/(R₁R₂)·P₀² | Hertz 중심 접근 | p.302 |
| (3) | U_S = −πa²γ — "where γ is the energy per unit contact area (i.e. the two surfaces)" | 잃는 표면 에너지 | p.304 · `eq_03_07_approximate.png` |
| (4) | F_S = −dU_S/dx | 표면 힘 | p.304 |
| (5) | x ≈ a²(R₁+R₂)/R₁R₂ | 이동량 ≈ δ (Hertz 기하) | p.304 |
| (6) | F_S ≈ πR₁R₂γ/(R₁+R₂) | **근사** 점착력 (탄성률 무관) | p.304 |
| (7) | P₀ ≈ πR₁R₂γ/(R₁+R₂) — 표면 힘이 접촉 크기를 크게 바꾸는 하중 규모 · 예: R₁ = R₂ = 2 cm, γ = 600 erg/cm² (운모 "≈300 per surface") → P₀ ≈ 2 g | 규모 판정 | p.304 |
| (8) | dU_T/da = 0 | 평형 조건 | p.304 · `eq_08_exact_setup.png` |
| (9) | a₀³ = RP₀/K · **R = R₁R₂/(R₁+R₂) · K = 4/3π(k₁+k₂)** | 일반화 Hertz | p.305 · `eq_09_11_hertz_apparent_load.png` |
| (10) | δ = a²/R | 하중점 이동 (Fig 1c 의 C) | p.305 |
| (11) | a₁³ = RP₁/K — P₁ = **겉보기 Hertz 하중** (Fig 1c 의 A) | 확대 반경 a₁ 의 등가 하중 | p.305 |
| U_E | U_E = U₁ − U₂ · U₁ = ∫₀^{P₁} (2/3)·P^{2/3}/(K^{2/3}R^{1/3}) dP = (2/5)·P₁^{5/3}/(K^{2/3}R^{1/3}) · 고정 반경 a₁ 에서 하중을 P₀ 로 뺄 때 δ = (2/3)·P/(K a₁) | 탄성 에너지 (A 로 Hertz 재하 → B 로 평판 압자식 제하) | p.305 · `eq_UE_tensile_edge.png` |
| (12) | U₂ = ∫_{P₀}^{P₁} (2/3)·P/(K a₁) dP = [1/(3K^{2/3}R^{1/3})]·(P₁² − P₀²)/P₁^{1/3} · U_E = [1/(K^{2/3}R^{1/3})]·[(1/15)P₁^{5/3} + (1/3)P₀²P₁^{−1/3}] | 저장 탄성 에너지 | p.306 · `eq_12_13_energies.png` |
| (13) | U_M = −P₀δ₂ = −P₀[δ₁ − (2/3)(P₁ − P₀)/(K a₁)] = [−P₀/(K^{2/3}R^{1/3})]·[(1/3)P₁^{2/3} + (2/3)P₀P₁^{−1/3}] | 하중의 위치 에너지 | p.306 |
| (14) | U_S = −γπa₁² = −γπ(RP₁/K)^{2/3} — **"where γ is the energy of adhesion of *both* surfaces"** | 표면 에너지 | p.306 · `eq_14_17_equilibrium.png` |
| (15) | U_T = U_E + U_M + U_S (세 항의 합 — 위 세 식) | 전체 에너지 | p.306 |
| (16) | dU_T/dP₁ = [P₁^{−4/3}/(9K^{2/3}R^{1/3})]·[P₁² − P₀² − 2P₁P₀ + 2P₀² − 6γπRP₁] | 평형 | p.306 |
| (17) | P₁² − 2P₁(P₀ + 3γπR) + P₀² = 0 · P₁ = P₀ + 3γπR ± √{(P₀ + 3γπR)² − P₀²} | 두 근 | p.306 |
| (18) | **P₁ = P₀ + 3γπR + √{6γπRP₀ + (3γπR)²}** — 안정 평형 = 양의 근 (둘째 미분 판정) | 겉보기 Hertz 하중 | p.307 · `eq_18_21_jkr_result.png` |
| (19) | **a³ = (R/K)·(P + 3γπR + √{6γπRP + (3γπR)²})** — γ = 0 이면 Hertz | 수정 Hertz | p.307 |
| (20) | **a³ = R(6γπR)/K** | 무하중 접촉 반경 | p.307 |
| 실근 조건 | 6γπRP ≥ −(3γπR)² ⇒ P ≥ −(3/2)γπR (원문 인쇄는 "6γπRP ≤ (3γπR)², P ≥ −3/2γπR" — 부호 표기는 §10-3) | | p.307 |
| (21) | **P = −(3/2)γπR** — "Separation of the spheres will just occur when … which we note is independent of the elastic modulus" | 떼는 힘 | p.307 |
| (22) | γ_S/V = γ_S/L + γ_L/V cos θ (Young) | 젖음 대조 | p.309 · `eq_22_young.png` |

- 응력 서술 (p.305): 표면 힘이 붙든 확대 접촉에서 *"the stresses between the surfaces are tensile at the edge of the contact area and only remain compressive in the centre"* · 정확한 분포는 Johnson (1958) · 접촉원 밖의 형상이 접선이 아니라 **수직으로 만난다** (Fig 1a 실선) — *"This change in profile was indeed observed by optical interferometry."*
- 가장자리 응력 (p.307): 이 분포는 접촉원 끝에서 **무한대 인장**이다 — *"In reality … the surfaces will separate slightly near the edge"* · 그러나 U_E 계산에는 "negligible error" · **Griffith 균열 기준과 같은 접근**.
- 근사 이론 (p.304): *"the force of adhesion F_S between convex surfaces does not depend upon the elastic moduli … both the surface energy and the elastic work vary as a²"* — 엄밀 해석이 크기만 바꾸고 이 결론은 유지.

### 3-2. 실험 조건 · 측정값 [인쇄]
| 항목 | 값 | 쪽 |
|---|---|---|
| 표면 | 광학 평활 · 돌기 ≈ **20 nm** · 낮은 탄성률이면 돌기를 누르는 힘 < 표면 인력 → "intimate contact" | 307–308 |
| 고무 | 유리 거푸집 성형 (Roberts 1968b) · **E = 8×10⁶ dyn/cm²** (= 0.8 MPa) | 308 |
| 젤라틴 | 25 % 수용액을 유리 거푸집에 주조 · **E = 3×10⁵ dyn/cm²** (= 30 kPa) | 308 |
| 측정 | 낮은 배율 광학현미경으로 접촉원 **지름** · 건조 · 윤활 (물 · 0.01 M SDS) | 308 |
| 포아송비 | **원문에 없음** | — |
| Fig 2 (고무 구 두 개, R₁ = R₂ = 2.2 cm) | 건조 total γ = **71 ± 4 erg/cm²** ("35 erg cm⁻² for each dry rubber surface") · 물 속: 고무–물 한 계면 **3.4 ± 0.2** · SDS: 최저 하중까지 Hertz | 308 |
| Young 대조 | 물방울 접촉각 예측 **64 ± 2°** ↔ 직접 측정 **66 ± 1°** · SDS 계면 에너지 상한 **0.05 erg/cm²** → cos θ > 1 → 퍼짐 (관찰됨) · *"the first time that the Young equation has been verified for contact angles greater than zero"* (저자 주장) | 309 |
| Fig 3 (고무 구 R = 2.2 cm ↔ 고무 판, 음하중) | 표면당 **34 erg/cm²** 로 **−0.3 g 보다 큰 하중**에서 이론과 "reasonable" · 떼는 하중 근처는 덜 맞음 — 접촉이 즉시 평형에 안 감 (높은 하중 수 초 → 0 근처 수 분) · *"viscous peeling forces which are rate dependent"* · 예비 실험의 떼는 하중 **½ – 5 g** 로 흩어짐 → 레버 + 마이크로미터 "overload" 로 평형 직후 점 확보 · 젤라틴이 더 잘 됨 (점성 지배 약함) | 309–310 |
| Fig 4 (젤라틴 구 R 2.45 · 7.9 · 25.5 cm ↔ Perspex 판) | 건조만 · γ (젤라틴–Perspex) **80–140, 평균 105 ± 10 erg/cm²** (주조마다 변동) | 311 |
| Fig 5 (같은 계, 무차원 · 음하중 포함) | "in close agreement with theory" | 311 |

### 3-3. ★ 그림 판독 (Fig 2–5) — `digitized.csv` [판독]
| 그림 · 계열 | 판독값 | 이론 대조 [우리 산술] |
|---|---|---|
| Fig 5 이론선 @ P/3γπR = −0.052 · −0.031 | ā = 1.229 · 1.239 | ā³ = P̄ + 1 + √(1 + 2P̄) → 1.237 · 1.246 (0.6–0.7 % 안) |
| Fig 5 떼는 하중 점선 위치 | P/3γπR = −0.496 | 식 (21) → −0.5 |
| Fig 2 건조 수정이론선 @ 0.113 g | 19·a = 1.23 (a = 0.065 cm) | — |
| Fig 2 물 · Hertz(SDS) 선 @ 0.10–0.11 g | 19·a = 0.68 · 0.46 | — |
| Fig 2 건조선 · Hertz 선 @ 9.2 g | 19·a = 2.29 · 2.00 | — |
| Fig 3 수정이론선 @ +0.06 g | 15·d = 2.50 (d = 0.167 cm) | — |
| Fig 3 수정이론선 왼쪽 끝 | (−0.68 g, 15·d = 1.60) | 떼는 하중 −(3/2)πWR (W = 68 mJ/m², R = 2.2 cm) = **−0.72 g** · 떼는 순간 반경 = 무하중의 4^{−1/3} = 0.63 배 |
| Fig 3 Hertz 선 @ 4.0 g | 15·d = 2.78 | — |
| Fig 4 무하중 평탄부 (0.1 g) ○ 2.45 · × 7.9 · □ 25.5 cm | 접촉 지름 0.555 · 1.39 · 2.75 cm | 식 (20) · E 3×10⁴ Pa · ν = 0.5 가정 · Perspex 강체 · W = 0.105 → **0.563 · 1.228 · 2.683 cm** |
| Fig 4 Hertz 선 (2.45 cm) @ 0.1 g | 0.174 cm | 같은 가정 → 0.153 cm |

- 정밀도: 600 dpi 크롭의 눈금 중심으로 축을 보정했다 · 선형축 ±1–2 % · 로그축 ±3–5 % (스캔 왜곡) · 선 · 기호 구분은 육안 · **추세 · 대조 전용**.
- ⇒ **Fig 4 · 5 는 원문 식과 원문 E 로 거의 그대로 재현된다** (젤라틴 2.45 · 25.5 cm 평탄부 1–3 % · 7.9 cm 는 13 % — 원문이 말한 "주조마다 γ 변동" 범위 80–140 안에서 설명 가능 [추정]).

### 3-4. [우리 산술] 원문 숫자로 다시 계산
| 계산 | 값 | 비고 |
|---|---|---|
| 식 (7) 예: πRγ, R = 1 cm, γ = 600 erg/cm² | 1,885 dyn = **1.92 gf** | 원문 "around 2 g" ✓ |
| 떼는 하중 −(3/2)πWR — Fig 2 (R = 1.1 cm, W 71) | 3.68 mN = **0.375 gf** | 고무 두 구 |
| 같은 식 — Fig 3 (R = 2.2 cm, W 68) | 7.05 mN = **0.719 gf** | 예비 실험 범위 ½ – 5 g 안 · 판독 곡선 끝 −0.68 g |
| 같은 식 — 젤라틴 (W 105) R = 2.45 · 7.9 · 25.5 cm | **1.24 · 3.99 · 12.9 gf** | |
| 무하중 반경 — Fig 2 (ν = 0.5 가정 → K = 7.11×10⁵ Pa) | a₀ = 0.0611 cm → 19·a₀ = **1.16** | 판독 1.23 (0.113 g) 과 5 % 안 |
| Fig 2 Hertz 선이 함의하는 K | (7.4–8.5)×10⁵ Pa (0.10 g · 9.2 g 두 점) | E = 8×10⁵ Pa 와 같은 크기 |
| Fig 3 이론선 두 개가 함의하는 K | Hertz 선 1.09×10⁶ · 수정이론선 (W 68) 1.11×10⁶ Pa | ⚠ Fig 2 보다 **≈1.4 배** — §10-2 |
| Young: cos θ = (35.5 − 3.4)/γ_L/V | **θ = 63.8°** (γ_L/V = 72.8 mN/m 가정 — 원문에 물 표면장력 값 없음) | 원문 64 ± 2° ✓ |

---

## 4. ★ 방법 — 해석 틀 · 입자 처리

### 4-1. 해석 틀 (p.304–307)
1. **근사 이론**: 접촉 응력이 여전히 Hertz 라고 보고 U_S = −πa²γ 를 이동량 x ≈ a²/R 로 미분 → F_S ≈ πRγ.  두 에너지가 모두 a² 에 비례해서 힘이 a 와 무관 → **탄성률 무관** (정성 결론은 엄밀 해석이 유지).
2. **엄밀 해석 (에너지 방법)**: 확대 반경 a₁ 의 상태를 두 단계로 만든다 — ① 표면 힘 없이 Hertz 로 P₁ 까지 재하 (Fig 1c O → A, 에너지 U₁) ② 반경 a₁ 을 고정한 채 P₀ 까지 제하 (A → B, 평판 압자처럼 δ = (2/3)P/(K a₁), 에너지 U₂).  U_E = U₁ − U₂ · U_M = −P₀δ₂ · U_S = −γπa₁² 를 더해 dU_T/dP₁ = 0.
3. 두 근 중 **안정 평형 = 양의 근** (식 18).  실근이 존재하는 한계가 떼는 하중 (식 21) — **하중 제어**에서의 분리 조건이다 (변위 제어는 이 논문에 없다).
4. 가장자리 무한대 인장은 실제로는 표면이 살짝 벌어져 유한해진다 — Griffith 균열 기준과 같은 근사 (에너지 계산 오차는 작다고 서술).

### 4-2. ★ 입자 처리 (DEM 판 "무질서 처리")
- **두 탄성 구 (또는 구–평판) 한 쌍** · 매끈한 표면 · 등방 선형 탄성 · 마찰 없음 · 소성 없음 · 점성 없음 (실험에서는 점성 박리가 보임 — 이론 밖).
- 형상: 접촉원 밖 형상이 표면 힘 때문에 **목 (neck)** 처럼 수직으로 만난다 — 즉 JKR 은 **탄성 형상 변화가 있는 점착** (강체 겹침이 아니다).
- 입자 분포 · 충전 · 다체 접촉 없음 → **쌍 접촉 법칙**이다.  분말 규모의 응집 · 유동은 이 논문 밖.

### 4-3. 기법 미니 용어집
- **γ (이 논문)** = 두 표면을 떼어 새로 만드는 단위 접촉 면적당 에너지 = 오늘의 **접착일 W** (같은 물질이면 응집일 W = 2γ_s).  원문이 "surface energy" 라고도 부르므로 읽을 때 늘 *both surfaces* 인지 확인.
- **γ_s (한 표면 에너지)** — 원문의 "energy … for each … surface" (고무 35 · 운모 300 erg/cm²).
- **매질 속 점착** — 물 속 고무 접촉은 고무–물 계면 **두 개**를 만든다 → 물 속 W = 2γ_SL = 6.8 erg/cm² (원문은 한 계면 3.4 로 보고) [인쇄 + 우리 산술].
- **겉보기 Hertz 하중 P₁** — 확대 반경 a₁ 을 Hertz 로 만들려면 필요한 하중.  P₁ − P₀ 가 표면 힘의 몫.
- **떼는 힘 (pull-off)** — 하중 제어에서 접촉이 더 버틸 수 없는 인장 하중 = (3/2)πγR.  떨어지는 순간에도 반경은 0 이 아니다 (무하중 반경의 4^{−1/3} = 0.63 배 [우리 산술 — 식 (19)]).
- **Young 식** — 고체–기체 = 고체–액체 + 액체–기체·cos θ.  원문은 접촉 실험으로 얻은 계면 에너지로 이 식을 검증.
- (원문 밖 · 참고) **Dupré 식** W₁₂ = γ₁ + γ₂ − γ₁₂ · **기하평균 규칙** W₁₂ ≈ 2√(γ₁γ₂) — 이 논문에는 없다 (`docs/hetero_thesis.md` §2-1 · 결합 규칙 원전 카드는 같은 묶음에서 따로 만든다).

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | (a) 반경 R₁ · R₂ 두 볼록체: Hertz 반경 a₀ (점선 형상, 접선) ↔ 표면 힘 있는 a₁ (실선, 수직으로 만남) · (b) 응력 분포 A = Hertz (a = a₁, P = P₁) · B = 실제 (Johnson 1958, a = a₁, P = P₀: 중심 압축 P · 가장자리 인장 T) · C = Hertz (a = a₀, P = P₀) · (c) 하중–변위: O → A (Hertz 재하) → B (고정 a₁ 제하) · C = 표면 힘 없는 점 | ★ JKR 접촉의 **목 · 가장자리 인장** — SJKR (겹침 면적 × CED) 에는 이 기하가 없다 (§7-2) |
| 2 | 고무 구 두 개 (R 2.2 cm): 19 × 접촉 반경 vs 하중 (로그–로그, 0.1–10 g) · + 건조 · ○ 물 · × SDS · 점선 Hertz · 실선 수정이론 | ★ 저하중에서 Hertz 이탈 · 매질이 W 를 줄인다 (물 2γ_SL · SDS ≈ 0) — 건식 ↔ 습식 공정의 점착 차이를 보는 틀 |
| 3 | 고무 구 (R 2.2 cm) ↔ 고무 판: 15 × 접촉 지름 vs 하중 (−1 … 4 g) · 오차막대 있는 음하중 점들 | 떼는 하중 근처의 **점성 · 속도 의존** — 실측 떼는 힘의 산포 원인 |
| 4 | 젤라틴 구 R 2.45 · 7.9 · 25.5 cm ↔ Perspex: 접촉 지름 vs 하중 (로그–로그, 0.1–100 g) | 무하중 평탄부가 R^{2/3} 로 커짐 (식 20) — §3-3 재현 |
| 5 | 같은 계 무차원: a(K/3γπR²) vs P/3γπR (−0.8 … 1.2) · 세 반경이 한 곡선 · 떼는 하중 −0.5 점선 | ★ JKR 무차원 곡선 — ⚠ 세로축 표기에 지수 1/3 누락 (§10-1) |
| eq (1)–(2) | Hertz | 기호 · 상수 |
| eq (3)–(7) | 근사 이론 · 운모 예 | 탄성률 무관의 정성 근거 |
| eq (8)–(11) · U_E | 평형 조건 · 일반화 Hertz · 겉보기 하중 · 탄성 에너지 경로 | 유도 사슬 |
| eq (12)–(17) | 에너지 세 항 · 평형 방정식 · 두 근 | γ 정의 문장 ("both surfaces") 포함 |
| eq (18)–(21) | 안정 근 · 수정 Hertz · 무하중 반경 · 떼는 힘 | ★ 결과식 원문 |
| eq (22) | Young 식 | 젖음 대조 |

## 6. Post-processing ★
- **원문**: 접촉 지름을 광학현미경으로 읽어 식 (19) 의 γ 하나를 맞춤 (맞춤 절차 · 오차 처리 서술 없음 — "±" 만 보고) · 무차원 그림 (Fig 5) 으로 세 반경을 한 곡선에 겹침.
- **안 한 것**: 포아송비 · 맞춤 잔차 · 반복 횟수 · 하중 제어 방식의 시간 기록 (속도 의존을 서술만).
- **이 카드에서 한 것**: Fig 2–5 판독 15 점 (`digitized.csv`) · 식 (19)–(21) 로 재계산 (§3-3 · 3-4) · 우리 SJKR 덱과의 대응식 유도 (§7-1).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 수치는 리포 출처를 병기해 적는다)

### 7-1. ★ JKR (W) ↔ 우리 믹서 SJKR (CED · Bond 수) — 대응식 [우리 산술]
- 우리 믹서 덱의 점착 = LIGGGHTS `cohesion sjkr` — **인력 = cohesionEnergyDensity × 겹침 접촉 면적** (소겹침 A ≈ 2πR\*δ) · 반발 = Hertz (4/3)E\*√R\*·δ^{3/2} (`scripts/make_mixer_deck.py` 주석 · `overlap_for_ced` · `bond_for_ced`).  Bo_code = 점착 지배 평형 인력 F_eq = (9/2)π³R\*²CED³/E\*² ÷ 입자 무게.
- 순 인력의 최대 (= SJKR 의 떼는 힘) 는 δ_po = (4/9)δ_eq 에서 **F_po = (4/27)·F_eq = (2/3)π³R\*²CED³/E\*²** (Codex HB-02 의 Bo_code = 6.75·Bo_po 와 같은 식).
- 이것을 JKR 식 (21) |P| = (3/2)πWR\* 와 같게 놓으면:

  **CED = [9·W·E\*² / (4π²·R\*)]^{1/3}  ⇔  W = 4π²·R\*·CED³ / (9·E\*²)**

  (소겹침 선형화 · 떼는 힘만 맞춘다 — 접촉 반경 · 접근량 · 이력은 맞추지 않는다.)
- **검산 (덱 값 대입)**: LC · LH 의 CED = `docs/reviews/mixer_highbo_prereg_20260927.md` §2-1 표 (생성기 실측) · LA 와 SE ref ×20 의 CED = `docs/reviews/mixer_cohesion_briefing_draft_20261002.md` §1-3 표 (⚠ 1저자 미보고 초안 — `docs/hetero_thesis.md` §3 — **값만** 빌렸다) · 생성기 상수 (parcel ⌀ SE 0.151 · AM_S 0.606 · AM_P 1.363 mm · E: SE 1×10⁷ (ref 2×10⁸) · AM 1.037×10⁹ Pa · ν SE 0.30 · AM 0.25 · `scripts/make_mixer_deck.py`).

| 팔 · 쌍 | CED (J/m³) | R\* | 이 식의 W (parcel 규모) | Bo_code (생성기 식) |
|---|---:|---:|---:|---:|
| LC · SE–SE (soft E) | 10,458 | 37.75 µm | **6.27×10⁻⁶ J/m²** | 0.213 |
| LC · SE–SE (ref ×20 E) | 77,057 | 37.75 µm | **6.27×10⁻⁶** | 0.213 |
| LC · AM_P–AM_P | 108,795 | 340.75 µm | **6.29×10⁻⁶** | 0.00109 |
| LC · AM_S–AM_S | 142,562 | 151.5 µm | **6.30×10⁻⁶** | 0.00553 |
| LA · AM_P–AM_P | 1,523,360 | 340.75 µm | 1.73×10⁻² (LC 의 ≈2.75×10³ 배) | 3.00 |
| LH · AM_P–AM_P | 3,563,475 | 340.75 µm | 0.221 (LC 의 ≈3.5×10⁴ 배) | 38.4 |

- ⇒ ① **LC (코팅 대리) 의 세 동종 쌍은 JKR 의미에서 같은 W** (0.3 % 안) — 생성기가 *"JKR 힘 스케일링으로 Bo 를 정의"* 한 것이 이 대응식으로 정확히 확인된다.  ② SE 경화 (×20) 의 **F₀ 보존 규칙 (CED ∝ E\*^{2/3}) = W 보존** — 같은 W 에서 강성만 바꾼 것이다 (강성 축 사전등록의 "Bo 불변" 과 같은 말).  ③ LA · LH 는 *"AM 표면이 SE 보다 10³–10⁴ 배 큰 W"* 세계 (논지 §2-6 · 브리핑 §1-5 와 같은 자릿수).
- ⚠ **parcel 규모의 W 다** — 실입자 W 로 옮기려면 CG 점착 규칙이 필요하고 (Bo 상사면 W_real = W_parcel/f², f = 151.4) 저장소 근거로 하나를 고를 수 없다 (논지 §2-6 · 브리핑 §1-4).  이 표는 *물성 인용 금지* — 팔 사이의 **비** 만 뜻이 있다.

### 7-2. JKR 과 SJKR 이 다른 점 (원문 근거 + 우리 산술)
| 항목 | JKR (이 논문) | 우리 SJKR | 결과 |
|---|---|---|---|
| 떼는 힘 | (3/2)πWR\* — **E 무관** (식 21) | (2/3)π³R\*²CED³/E\*² — **E 에 의존** | 같은 CED 로 E 를 연화하면 떼는 힘이 커진다 → 강성을 바꿀 때 CED ∝ E\*^{2/3} 로 따라가야 W 가 유지 (우리 F₀ 보존 규칙이 정확히 이것) |
| 무하중 접촉 | 접근 δ₀ = a₀²/(3R\*) · 목 · 가장자리 인장 (Fig 1) | 평형 겹침 δ_eq = (B/A)² | 떼는 힘을 맞추면 **δ_eq = 4.25 × δ₀(JKR)** [우리 산술] — 1 % 겹침 천장은 SJKR 고유 제약이지 JKR 물리의 제약이 아니다 |
| 분리 | 유한 반경에서 갑자기 (하중 제어 · 0.63 a₀) | δ → 0 에서 힘이 연속으로 0 (목 · 점프 없음) | 충돌 포획 · 이탈 에너지 (붙는 속도 상한) 는 JKR 과 다르다 [추정] — 브리핑 §1-6 의 "붙는 속도" 산술은 SJKR 식 기준 |
| 평형 힘 | P₁(P₀ = 0) = 6γπR = 떼는 힘의 4 배 [우리 산술 — 식 18] | F_eq = 떼는 힘의 6.75 배 | Bo_code (평형 기준) ↔ Bo_po (떼는 힘 기준) 를 섞지 않는다 (HB-02) |

### 7-3. ★ 벽 점착 규칙 (CED ÷ 6.25^{1/3}) — JKR 힘비 재현 검토 [우리 산술 · 추정]
- 생성기 주석: *"hare2026 은 JKR γ_pw/γ_pp = 1/6.25 = 힘비 1/6.25 · SJKR 은 F ∝ CED³ ⇒ CED ÷ 1.842"*.  JKR 원식으로는 같은 입자의 벽 접촉 R\* = r (평판) 이 입자–입자 R\* = r/2 의 **2 배**라 힘비 = (γ_pw/γ_pp)·2 = **0.32** 다.
- 우리 SJKR 에서 같은 입자의 떼는 힘 비 = (R\*_pw/R\*_pp)²·(1/6.25)/(E\*_pw/E\*_pp)² — 벽 접촉 = **쌍별 E\* · 평면벽 (R\* = 입자 반경)** (Codex 가 같은 사전등록 §2-1 의 정적 겹침을 이 규약으로 재계산했다 · 벽 E 1.48×10⁹ · ν 0.30).  이 규약에서 **SE 0.162 (JKR 0.32 의 0.51 배) · AM_P 0.452 (1.41 배)**.
- ⇒ 덱 주석이 이미 *"O(1) 불확실을 원고에 적을 것"* 이라 적은 그 불확실이 **상별로 반대 방향 (SE 약하게 · AM 세게)** 이다 [추정].  ⬜ 덱 검사 · 결정 = 1저자 (이 카드는 덱을 고치지 않는다).

### 7-4. ★ 이종기술 논지 (§2) 에 주는 것
- 논지 §2-1 의 **F_ij ≈ (3/2)π·W_ij·R\*_ij** = 이 논문 식 (21) 그대로 (γ → W).  논지 §2-3 의 194 · 38 · 1.8 배와 **γ_A/γ_S < 0.31** 은 이 식의 **매끈한 구 기하 (R\* = 입자 곡률)** 에 기댄다.
- DMT (2πWR\*) 로 바꿔도 **비 (ratio) 는 그대로** — 두 극한 모두 F ∝ W·R\* 이므로 0.31 문턱은 JKR/DMT 선택에 둔감하다 [우리 산술].  (Maugis 전이에서는 계수가 1.5–2 사이로 쌍마다 조금 달라질 수 있다 — 최대 33 % [추정].)
- ★ **원문 Discussion (p.312) 이 경고하는 것**: 단단한 고체 (금속 · 유리) 의 접촉은 **돌기가 지배**하고 실제 접촉은 기하 면적에 못 미친다.  LPSCl (E ≈ 22 GPa) · NCM811 (≈ 140–165 GPa, 위 한정어 ② 의 출처) 은 원문 기준으로 "high modulus" 쪽이다 [추정].  접촉이 입자 곡률이 아니라 **같은 크기의 돌기 반경**으로 정해지면 §2-3 의 기하 이득 (1.8 배) 이 사라지고, 기하평균 규칙 아래 SE–SE 우세 조건이 **γ_A/γ_S < 0.31 → < 1** 로 옮겨간다 [추정].  ⇒ §2-8 의 판가름 측정 (AFM 콜로이드 탐침 등) 에서 **거칠기 (돌기 반경) 를 함께 기록**해야 0.31 과 1 중 어느 문턱을 쓸지 정할 수 있다.
- 매질 효과: 물 속에서 W 는 2γ_SL (3.4 → 6.8 erg/cm²) 로 건조 71 의 1/10 — 습식 슬러리 공정과 건식 혼합의 점착은 같은 표면이어도 다른 수다 (Fig 2) [인쇄 + 우리 산술].

### 7-5. 기존 정본 카드와의 관계
- `dmt1975_adhesion_contact_deformation`: 그 카드의 *"JKR 1971 = 유료/접근 불가"* 는 이 카드로 해소.  그 카드의 *"Γ = Dupré 일 = 2γ_표면"* 표기는 이 원문 정의 ("both surfaces") 와 맞다.  ⚠ 그 카드의 *"우리 SE (R ≈ 0.25 µm, 비교적 단단) → JKR 이 아니라 DMT 체제"* 는 이 논문으로 판정할 수 없다 — 그 카드의 Tabor μ = (Rγ²/E\*²ε³)^{1/3} 꼴 (원전 카드 없음 [미확인]) 에 R\* 0.25 µm · E\* 12.7 GPa (E 22 · ν 0.37) · z₀ 0.4 nm · W 0.1–1 J/m² 를 넣으면 **μ ≈ 0.6–2.9 = 전이 영역** [우리 산술 · 가정 다수].
- `hare2026_dem_pept_dry_mixing_nmc622_eirich` §4.3: 그 카드가 인쇄 오타로 읽은 Hare 식 (7) 둘째 항의 γ 누락 — 원전 JKR 의 결과식 (19) 은 √{6γπRP + (3γπR)²} 꼴 (Hare 식은 E\*·a 매개 꼴이라 직접 대조는 안 된다).  Hare 의 γ_pp 0.25 · γ_pw 0.04 가 W 인지 γ_s 인지는 EDEM 규약 문서로 확인해야 한다 [미확인] — 그것이 HB-02 의 38.7 ↔ 77.4 를 가른다.
- `thorntonning1998_adhesive_elastoplastic_contact` (JKR + 소성 캡) · `pasha2014_linear_elastoplastic_adhesive_contact` · `thakur2014_eepa_adhesive_elastoplastic_dem`: JKR 을 DEM 접촉 법칙으로 확장한 계보 — 이 원문이 그 바닥 (탄성 · 하중 무관 점착).
- `otani2025_dem_se_dispersion_aggregation_compression` (JKR γ 0.1 균일) · `lischka2025_dem_eirich_intensive_mixer_dry_mixing` (cohesion number 로 γ 재계산): 모두 이 식의 γ 를 쓴다 — **그 γ 가 W 규약인지 각 카드에서 확인**.

### 7-6. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 탄성 쌍 접촉의 점착 역학 (접촉 크기 · 떼는 힘) — 우리 믹서 DEM 의 점착 법칙이 기대는 **접촉 단위 물리**.
- **없는 것**: 분말 규모 (충전 · 유동 · 혼합) · 소성 (무른 황화물의 하중 의존 점착) · 거칠기 · 정전기 · 속도 의존 (원문이 실험에서 본 점성 박리).  수송 (σ) 쪽은 해당 없음.

---

## 8. 적용 인사이트 (내 연구에 어떻게)
1. **"γ" 를 볼 때마다 W 인지 γ_s 인지 먼저** — 원전은 W (= 두 표면 합) 로 정의한다.  HB-02 의 2 배 모호는 원전이 아니라 하류 소프트웨어 · 논문의 규약 문제다 (Hare · EDEM 문서 확인 [미확인]).
2. **JKR ↔ SJKR 대응식 CED = [9WE\*²/(4π²R\*)]^{1/3}** — 논지 D2 (결합 규칙: W_AA · W_SS · W_AS → CED_ij) 를 덱에 내릴 때 바로 쓸 수 있다.  같은 식으로 LC = 단일 W 세계임을 확인했다.
3. **벽 규칙 검토 후보** — JKR 원식의 R\* 차이 (평판 = 2 배) 를 넣으면 현 벽 CED 규칙은 SE 벽을 0.5 배 · AM 벽을 1.4 배로 준다 [추정 · 덱 확인 전].
4. **거칠기가 0.31 문턱을 움직인다** — 단단한 µm 분말에서는 돌기 반경이 R\* 일 수 있다 (원문 Discussion) → 판가름 측정에 거칠기 기록 필수.
5. **떼는 힘 측정은 속도 · 대기 시간에 민감** (원문 Fig 3 서술) — AFM 콜로이드 탐침 계획 (§2-8) 에 접촉 시간 · 후퇴 속도를 고정 · 기록.

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Johnson, Kendall and Roberts (1971) showed that two elastic spheres separate at a tensile load P = −(3/2)γπR, independent of the elastic modulus, where γ is the energy of adhesion of both surfaces (i.e., the work of adhesion), and R = R₁R₂/(R₁+R₂)."
- "At zero applied load the JKR contact radius is finite, a³ = R(6γπR)/K, with K = 4/[3π(k₁+k₂)] and k_i = (1−ν_i²)/(πE_i)."
- "Matching the pull-off force of a linear-in-area (SJKR) cohesion model to the JKR value gives CED = [9WE*²/(4π²R*)]^{1/3} (our derivation, small-overlap limit)."
- 국문: *"JKR 원전의 γ 는 두 표면을 합친 접착일이다 — 같은 물질이면 떼는 힘은 3πγ_sR\* (γ_s = 한 표면 에너지) 이다 (Johnson 1971, p.306 · 308)."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **Fig 5 세로축 표기 결함**: 인쇄된 축 이름은 *a(K/3γπR²)* — 차원이 맞지 않는다 (길이 × 길이⁻³).  곡선 값은 **a·(K/3γπR²)^{1/3}** 일 때만 식 (19)–(21) 과 맞는다 (P = 0 에서 2^{1/3} = 1.26 · 떼는 점 0.794 — 판독 0.6–0.7 % 안).  ⇒ 지수 1/3 누락 [판독 + 우리 산술].
2. **Fig 2 ↔ Fig 3 의 K 불일치 후보**: Fig 2 Hertz 선이 함의하는 K ≈ (7.4–8.5)×10⁵ Pa 인데 Fig 3 의 두 이론선 (Hertz · 수정) 은 ≈1.1×10⁶ Pa 를 함의한다 [판독 + 우리 산술].  같은 고무라면 같아야 하는데 원문은 Fig 3 판 (flat) 의 E · ν 를 적지 않았다 → 원인 [미확인] (다른 고무 · 지지된 얇은 판 등 [추정]).  떼는 힘은 K 무관이므로 γ ≈ 68–71 결론에는 영향이 작다.
3. **실근 조건의 표기**: 원문은 "6γπRP ≤ (3γπR)², P ≥ −3/2γπR" 로 인쇄 — 근호 안 6γπRP + (3γπR)² ≥ 0 이 실제 조건이고, 첫 줄은 P < 0 일 때 **크기 |P|** 로 읽어야 성립한다 (부호 생략) [추정].  결과 (21) 은 정확.
4. **γ 용어 혼용**: 같은 γ 를 "energy per unit contact area (i.e. the two surfaces)" · "energy of adhesion of both surfaces" · "surface energy γ" (식 18 뒤) · "total surface energy" 로 부른다 — 숫자 정의는 일관 (늘 두 표면 합) 이지만 이름이 흔들려 하류 2 배 혼동의 원인이 된다.
5. **포아송비 미기재** — 이론선을 다시 그리려면 ν 가정이 필요하다 (ν = 0.5 로 Fig 2 · 4 는 5 % 안에서 재현).
6. **떼는 힘의 재현성** — 예비 실험 ½ – 5 g (10 배 산포) · "overload" 기법 뒤 "reasonably reproducible" (수치 산포 미보고) · 고무는 점성 박리가 지배 → **실측 pull-off 를 W 로 환산할 때 속도 의존을 통제하지 않으면 과대 · 과소 둘 다 가능**.
7. **전이 한계**: cm 크기 · E 0.03–0.8 MPa 고무 · 젤라틴 ↔ µm · GPa 분말.  원문 스스로 단단한 고체는 거칠기에 가려진다고 적는다 (p.312) — µm 황화물 · 산화물 분말에 매끈한 구 JKR 을 그대로 쓰는 것은 이 원문이 지지하지 않는다.
8. **"Young 식의 θ > 0 첫 검증"** 은 저자 주장 (p.309) — 독립 확인 [미확인].
9. **참고문헌 철자**: 본문 "McFarland & Tabor (1950)" (p.312) ↔ 목록 "McFarlane, J. S. & Tabor, D. 1950" (p.313) — 사소한 불일치.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유 한 줄)
| 서지 (원문 목록 그대로) | 왜 |
|---|---|
| Johnson, K. L. 1958 *Brit. J. appl. Phys.* **9**, 199. | 확대 접촉의 실제 응력 분포 (Fig 1b 곡선 B) — 인장 가장자리의 원전 |
| Kendall, K. 1969 Ph.D. dissertation, Cambridge University, England. | 유리 구의 "Hertz 보다 큰 접촉" — 단단한 고체 데이터 |
| Roberts, A. D. 1968a Ph.D. dissertation, Cambridge University, England. | 고무 구 관찰 원전 |
| Roberts, A. D. 1968b *Engng Mater. Des.* **11**, 579. | 광학 평활 고무 성형법 |
| Tabor, D. & Winterton, R. H. S. 1969 *Proc. R. Soc. Lond.* A **312**, 435. | 표면 힘 작용 거리 측정 리뷰 |
| Bradley, R. S. 1932 *Phil. Mag.* **13**, 853. | 강체 구 점착 (2πRγ 계열) — DMT 와의 비교축 |
| El-Refaie, M. & Halling, J. 1968 *Univ. Salford Report U.S.M.E.-T-5-68.* | 단단한 표면의 돌기 "penumbra" 접촉 — 거칠기 논점 |
| McFarlane, J. S. & Tabor, D. 1950 *Proc. R. Soc. Lond.* A **202**, 224. | 유리 구 점착 = 액체 메니스커스 — 습도 효과 |
| Bowden, F. P. & Tabor, D. 1950 *Friction and lubrication of solids*, part I. p. 299, London: O.U.P. | 금속 점착 (소성 연금속) |
| Good, R. J. 1952 *J. Am. chem. Soc.* **74**, 5041. | 액체 접촉 평형 (표면 에너지) |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- PDF 14 쪽 (JSTOR 표지 1 + 본문 13) 전부를 쪽 이미지 (110 · 220 · 400 · 600 dpi) 로 읽었다 · 텍스트층은 OCR 이라 식이 깨져 있어 식 (1)–(22) 은 전부 이미지에서 옮겼다 · 서지 = p.301 머리말 · JSTOR 표지.
- "½ to 5 g" (p.309) 은 OCR 이 "W to 5g" 로 깨뜨린 곳 — 400 dpi 확대로 확인.  Fig 5 세로축 이름은 600 dpi 확대로 확인 (지수 없음).
- 크롭 14 장 = Figure 1–5 (손 크롭, 600 dpi = 원본 스캔 해상도 · 캡션 포함) + 식 영역 9 장 (`eq_*.png`).  추출기 자동 경로는 OCR 캡션 ("FIGu:RE 1." 등) 때문에 Fig 4 · 5 만 잡았다 → 전부 손 크롭으로 통일.
- 정본 litdb 중복 확인: 파일 목록 + DOI · 제목 낱말 · JSTOR 번호 `git grep` — 이 논문 카드 없음.

## 🔗 관련 카드
- 점착 접촉 계보: `dmt1975_adhesion_contact_deformation` · `thorntonning1998_adhesive_elastoplastic_contact` · `pasha2014_linear_elastoplastic_adhesive_contact` · `thakur2014_eepa_adhesive_elastoplastic_dem` · `luding2008_cohesive_frictional_contact_models` · `molerus1975_theory_of_yield_cohesive_powders`.
- 이 식을 쓰는 DEM: `hare2026_dem_pept_dry_mixing_nmc622_eirich` · `lischka2025_dem_eirich_intensive_mixer_dry_mixing` · `frankenberg2024_dem_high_intensity_mixer_assb` · `otani2025_dem_se_dispersion_aggregation_compression` · `asylbekov2023_cb_fragmentation_pbe_dem_dry_mixing`.
- 우리 쪽: `lee2026_mechanical_halogen_argyrodite_drycoating` (AFM-FS W_ad).

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

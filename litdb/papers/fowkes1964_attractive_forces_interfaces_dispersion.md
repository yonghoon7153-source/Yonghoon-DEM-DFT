<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 이웃 = faka2026_… · 같은 묶음 = johnson1971_… · begat2004_… · garcia2017_… · vanoss1988_….
     원문 = 13 쪽 (Ind. Eng. Chem. "The Interface Symposium–5") · 컬러 JPEG 쪽 (p.40–41 · 43–44 · 47–48 · 50) 과 1-bit 쪽이 섞인 300 ppi 스캔 + OCR 텍스트층 · SI 없음.
     쪽 표기 = 인쇄 쪽 (PDF n 쪽 = p.(39 + n)).  식은 쪽 이미지 (150 dpi 전쪽 + 300 dpi 확대) 에서 옮겼다 (OCR 이 근호 · 위첨자를 깨뜨림).
     값 표지: [인쇄] = 원문 식 · 표 · 본문 / [우리 산술] = 원문 식 · 값 또는 다른 정본 카드 값으로 한 계산 / [추정] = 우리 해석 / [미확인] = 원문에 없음. -->
# Attractive Forces at Interfaces — 표면 자유에너지의 **분산 (London) 성분 γ^d** 를 도입하고, 계면을 건너는 상호작용이 분산력뿐이면 **γ₁₂ = γ₁ + γ₂ − 2√(γ₁^dγ₂^d)** (Fowkes 식 · 분산 성분의 기하평균) 로 계면 장력 · 퍼짐 · 접촉각 · 흡착 · 침지열 · Hamaker 상수 (A = 6πr²γ^d) 를 한 틀로 계산 · 금속 · 산화물 분말의 γ_S^d (≈ 60–148 mJ/m²) · 극성 "초과" 상호작용 표 — Fowkes (Ind. Eng. Chem. 1964)

> slug `fowkes1964_attractive_forces_interfaces_dispersion` · DOI `10.1021/ie50660a008` · type `theory + data compilation (dispersion component of surface free energy γ^d · geometric-mean combining rule for dispersion forces · interfacial tension, spreading, contact angle, adsorption/immersion, Hamaker constant · tables for liquids, polymers, metals, oxides)` · PDF `e9acc8f0-37._ATTRACTIVE_FORCES_AT_INTERFACES.pdf` · digested `2026-10-13` · status ✅
>
> **서지 (원문 인쇄)**: Frederick M. Fowkes (*"Director of Research, Sprague Electric Company, North Adams, Mass."* — p.47 저자 소개) · "THE INTERFACE SYMPOSIUM–5" · *Industrial and Engineering Chemistry* **Vol. 56, No. 12, December 1964**, pp. 40–52 [인쇄 쪽 머리 · 꼬리].
> DOI 출처: PDF 문서 메타데이터 (keywords "article doi: 10.1021/ie50660a008 … Industrial & Engineering Chemistry_56_12_…_40_52") + 매 쪽 인쇄 워터마크 경로 `…/article-pdf/56/12/40/13222437/ie50660a008.pdf` — 본문에는 DOI 문자열이 인쇄돼 있지 않다.
> ★ **이 카드가 맡는 일** — 이종기술 논지 (`docs/hetero_thesis.md`) §2-1 *"반데르발스 (분산력) 지배면 기하평균 규칙 W_ij ≈ 2√(γ_i·γ_j)"* 의 **원전** (Fowkes 판 = γ 가 아니라 **γ^d 의 기하평균**) · 산화물 분말의 분산 표면 에너지 값 (NCM 은 없음) · 극성 초과 상호작용의 크기 · Hamaker ↔ γ^d.
> (같은 묶음의 `vanoss1988_lifshitz_vdw_acid_base_interfacial` 가 이 틀을 LW + 산 · 염기로 확장한다 — Fowkes 의 "polar interactions do not follow the combining rule" 을 그 리뷰가 인용한다.)

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 계면을 건너는 인력이 **분산력뿐**이면 계면 장력은 **γ₁₂ = γ₁ + γ₂ − 2√(γ₁^dγ₂^d)** (식 1) — 즉 접착일 W₁₂ = γ₁ + γ₂ − γ₁₂ = **2√(γ₁^dγ₂^d)** [우리 산술 — 식 1 + Dupré] — 이고, 이것으로 Hg 의 γ^d = 200 ± 7 · 물의 γ^d = 21.8 ± 0.7 mJ/m² 를 얻으며 물–Hg 계면 장력을 424.8 (실측 426–7) 로 맞힌다 [인쇄 Table I–II · p.43].
⇒ 논지 §2-1 의 기하평균 규칙은 원전에서 **총 γ 가 아니라 분산 성분 γ^d 에 대한 것**이고, 분산 외 (극성 · 수소결합 · π) 상호작용은 **"초과" 항** 으로 따로 남는다 — 산화물 표면과 물의 초과는 336–368 mJ/m² 로 분산 몫 (94–102) 의 3.5 배 이상이다 [인쇄 Table IX · p.50].

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ★ 기하평균 규칙의 원전 꼴 | γ₁₂ = γ₁ + γ₂ − 2√(γ₁^dγ₂^d) (1) — 계면 = 두 "계면 영역" 의 장력 합 · 각 영역 장력 = 자기 γ − 상대의 분산 인력 √(γ₁^dγ₂^d) | [인쇄] p.42 · Fig 1 |
| 왜 기하평균인가 · 오차 | London 쌍 퍼텐셜 μ₁₁ = −(3/4)α₁²I₁/r₁₁⁶ (2) 의 합 → γ₁^d = −πN₁²α₁²I₁/(8r₁₁²) (3) · 이종 Σ₁₂^d (4) 를 Berthelot 기하평균 (5) 으로 근사 — **이온화 퍼텐셜이 50 % 달라도 오차 2 %** · 부피 요소 크기 차가 문제 (플루오로카본: CF₂ > CH₂) | [인쇄] p.42 |
| 실패 예 | 플루오로카본–탄화수소: 실측 상호작용이 분산 예측보다 **3–5 mJ/m² (20–25 %)** 약함 (Fig 7) · 불소 윤활유–물 계면 장력 예측 50.3 vs 실측 57.7 | [인쇄] p.50 |
| ★ 분산 성분 값 (고체) | 저에너지 고체 (접촉각, Table III): PTFE 19.5 · 파라핀 25.5 · PE 35.0 · PS 44.0 mJ/m² 등 · **금속 · 산화물 분말 (흡착 π_e, Table IV)**: Cu 60 · Ag 74 · Pb 99 · Sn 101 · Fe 89–108 · 흑연 115–132 · **Fe₂O₃ 107 · 아나타스 89–92 (N₂ 로 141) · SiO₂ 78 · SnO₂ 111 · BaSO₄ 76** · Table V: 루틸 143 · SnO₂ 118 · SiO₂ 123 (⚠ §10-2) · Hg 200 | [인쇄] Table III–V · p.45 · 47 |
| ★ 극성 "초과" 의 크기 | 고체–액체 (Table IX, π_e 기반): 산화물 (아나타스 · 실리카 · BaSO₄ · SnO₂) 과 **물: 초과 336–368** ↔ 분산 94–102 mJ/m² · n-프로판올 54–96 · 아세톤 58 · 벤젠 20–26 (π 결합) · 흑연–벤젠 20 · 액체–액체 (Table VII–VIII): Hg–알킬 요오드 · 머캅탄 · 니트로 ≈ 50 · 물–아닐린 · 아민 · 산 · 알코올 40–48 · 물–방향족 ≈ 15 | [인쇄] Table VII–IX · p.48–51 |
| Hamaker ↔ γ^d | A₁ = 6πr₁₁²γ₁^d (18) · A₁₂ = 6πr₁₁²(√γ₁^d − √γ₂^d)² (19, 물 속 입자) · 물 · 산화물 이온 · 금속 원자 · CH₂ 면 **6πr₁₁² = 1.44 × 10⁻¹⁴ (cm²)** | [인쇄] p.46–47 · Table V · Fig 5 |
| 퍼짐 · 접촉각 · 흡착 | S = 2√(γ_Oγ_W^d) − 2γ_O (6) · cos θ = −1 + 2√γ_S^d·(√γ_L^d/γ_L) (9) · π_e = 2√(γ_S^dγ_L^d) − 2γ_L (11) · γ_S^d = (π_e + 2γ_L)²/4γ_L^d (12) · 흡착열 · 침지열 (13) · (14) | [인쇄] p.43–46 |
| 계면 인장 강도 | 분산 인력의 미분으로 이상 강도: PE 70 × 10⁸ dyn/cm² · PE–철 105 × 10⁸ (r 4 Å) — 실측은 한 자릿수 낮다 ("crack initiation") | [인쇄] p.52 |
| NCM · LPSCl 값 | **없다** | [미확인] |

⛔ **한정어 (떼지 말 것)**: ① 1964 리뷰 · 값의 상당수는 당시 문헌 (흡착 π_e · 접촉각) 모음 ② 분말 값은 **탈기 · 청정** 표면 기준 (질소 · 아르곤 · 헵탄 증기 흡착) — 공기 중 분말 아님 ③ 기하평균은 **분산 성분**에만 · 극성 초과는 경우마다 측정 ④ 산화물 γ^d 값이 표마다 다르다 (실리카 78 ↔ 123, §10-2) — ±25 % 수준의 불확실 ⑤ 배터리 소재 (NCM · 황화물) 값 없음.

---

## 1. 한 줄 요약
표면 장력을 원인별 성분의 합으로 보고 (예: γ_Hg = γ_Hg^d + γ_Hg^m), **분산 성분 γ^d** 만이 모든 물질 사이에 작용한다는 점에 착안해, 포화 탄화수소 (분산력만 있는 기준 액체) 와의 계면 장력에서 γ^d 를 뽑는다 (Hg 200 · 물 21.8).
같은 식으로 퍼짐 계수 · 접촉각 (한 번의 측정으로 γ_S^d) · 증기 흡착의 퍼짐 압력 π_e (→ γ_S^d) · 흡착열 · 침지열 · Hamaker 상수 (A = 6πr²γ^d) 를 예측해 실측과 맞추고, 측정값과 분산 예측의 차를 **극성 초과 상호작용** (π 결합 · 쌍극자 · 수소결합 · 이온–쌍극자) 의 크기로 읽는다 (Hg–유기 액체 · 물–유기 액체 · 산화물–극성 액체 표).
접착에 대해서는 "저에너지 액체는 고에너지 고체를 적신다" 는 단순 규칙이 **분산 성분이 상호작용할 때만** 성립한다 (물이 청정 금속을 적시지 않는 이유) 고 결론하고, 분산 인력에서 계면 이상 인장 강도를 어림한다.

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| **F. M. Fowkes** (Sprague Electric Company, North Adams, Mass.) | Ind. Eng. Chem. **56** (12) 40–52 (1964) · "The Interface Symposium–5" | 10.1021/ie50660a008 (메타데이터 · 워터마크) | 이론 + 문헌 값 — 탄화수소 · 물 · Hg · 고분자 · 금속 (Cu · Ag · Pb · Sn · Fe) · 산화물 (Fe₂O₃ · TiO₂ · SiO₂ · SnO₂) · BaSO₄ · 흑연 | 이론 · 데이터 집성 |

| 원문 구조 | 쪽 | 내용 |
|---|---|---|
| 도입 · Model and Basic Assumptions | 40–43 | 표면 장력 = 성분 합 · Fig 1 · 식 (1)–(5) · Table I (Hg) · Table II (물) |
| Calculation of Interfacial Tension · Spreading Coefficients · Contact Angles | 43–44 | 식 (6)–(9) · Fig 2 · Fig 3 (Zisman 자료) |
| Free Energy of Adsorption of Vapors on Solids | 45 | 식 (10)–(12) · Table III · Table IV |
| Heats of Adsorption · Heats of Immersion | 46 | 식 (13)–(14) · Fig 4 |
| Long Range Attractive Forces | 46–47 | 식 (15)–(19) · Fig 5 · Table V |
| Evaluation of γ_L^d for Polar Liquids | 48 | Fig 6 · Table VI |
| Polar Interfacial Interactions (liquid/liquid · solid/liquid) | 48–51 | Table VII · VIII · IX |
| Fluorocarbon–Hydrocarbon Interactions · Application to Adhesion · Ultimate Tensile Strength | 50–52 | Fig 7 · 퍼짐 계수 · 인장 강도 |
| Nomenclature · Literature Cited (38) | 52 | |

- 중복 확인 (2026-10-13): 정본 `litdb/papers/` 전수 목록에 fowkes 파일 없음 · `git grep -i` "ie50660a008" · "Attractive forces at interfaces" 0 건 → 새 카드.

---

## 3. 핵심 식 · 수치 (★ 원문 그대로 — 크롭 `eq_*.png` · `tab_*.png`)

### 3-1. 식 [인쇄]
| 식 | 원문 | 뜻 | 쪽 · 크롭 |
|---|---|---|---|
| — | γ_Hg = γ_Hg^d + γ_Hg^m | 성분 분해 (분산 + 금속 결합) | p.40 |
| (1) | **γ₁₂ = γ₁ + γ₂ − 2√(γ₁^dγ₂^d)** — *"the geometric mean of the dispersion force components of the surface tension of the hydrocarbon and of the mercury"* | ★ Fowkes 식 | p.42 · `eq_01_03_geometric_mean_derivation.png` · Fig 1 |
| (2) | μ₁₁ = −(3/4)·α₁²I₁/r₁₁⁶ | London 쌍 퍼텐셜 | p.42 |
| (3) | γ₁^d = −πN₁²α₁²I₁/(8r₁₁²) (eV/cm² · ×1.602 × 10⁻¹² → erg/cm²) | 분산 표면 에너지 (쌍 합) · 물 (α 1.48 Å³ · I 12.6 V · N 3.34 × 10²² cm⁻³ · r 2.76 Å) → **25.4** erg/cm² | p.42–43 |
| (4) | Σ₁₂^d = −(πN₁N₂α₁α₂/4r₁₂²)·I₁I₂/(I₁ + I₂) | 이종 분산 상호작용 (12 최근접 이웃) | p.42 · `eq_04_05_pair_potential_error.png` |
| (5) | Σ₁₂^d ≅ (Σ₁₁^dΣ₂₂^d)^{1/2} = −(πN₁N₂α₁α₂/8r₁₁r₂₂)·I₁I₂/√(I₁I₂) — *"geometric mean relationship of Berthelot, London, Hildebrand"* · N₁ = N₂ · r₁₁ = r₂₂ · I₁ = I₂ 이면 (4) 와 같다 · **I 가 50 % 달라도 2 %** | 기하평균 근사의 오차 | p.42 |
| (6) | S = 2√(γ_Oγ_W^d) − 2γ_O (기름 O 가 물 W 위) | 퍼짐 계수 | p.43 · `eq_06_09_spreading_contact_angle.png` |
| (7)–(9) | γ_L cos θ = γ_S − γ_LS − π_e · γ_L cos θ = −γ_L + 2√(γ_L^dγ_S^d) − π_e · (π_e = 0) **cos θ = −1 + 2√γ_S^d·(√γ_L^d/γ_L)** | 접촉각 — cos θ vs √γ_L^d/γ_L 은 (−1 원점) 직선 · 기울기 2√γ_S^d → **한 번의 측정으로 γ_S^d** | p.43–44 |
| (10)–(12) | π_e = γ_S − (γ_L + γ_SL) · π_e = 2√(γ_S^dγ_L^d) − 2γ_L · **γ_S^d = (π_e + 2γ_L)²/4γ_L^d** | 증기 흡착 퍼짐 압력 → γ_S^d | p.45 · `eq_10_12_spreading_pressure.png` |
| (13) | ΔF°_ads = 2γ_L − 2√(γ_S^dγ_L^d) · ΔH°_ads = ΔF°_ads − T(dΔF°_ads/dT) = … | 흡착열 | p.46 · `eq_13_14_heats_adsorption_immersion.png` |
| (14) | ΔF_i = γ_SL − γ_S = γ_L − 2√(γ_S^dγ_L^d) · ΔH_i = … | 침지열 | p.46 |
| — | 평판 사이 인력 A/6πd³ (dyn/cm²) | 장거리 힘 | p.46 |
| (15)–(17) | A₁ = (3/4)π²N₁²α₁²I₁ · A₁₂ = √A₁² − 2√(A₁A₂)·(2√(I₁I₂)/(I₁ + I₂)) + √A₂² (물질 2 가 1 속) · Vold: A₁₂ = (√A₁ − √A₂)² | Hamaker | p.46 · `eq_15_17_hamaker_long_range.png` |
| (18) · (19) | **A₁ = 6πr₁₁²γ₁^d** · **A₁₂ = 6πr₁₁²(√γ₁^d − √γ₂^d)²** · 6πr₁₁² = 1.44 × 10⁻¹⁴ | ★ Hamaker ↔ γ^d | p.47 · `eq_18_19_hamaker_from_gamma_d.png` |
| — | S = γ_S − (γ_L − γ_SL) · S = √(γ_L^dγ_S^d) − 2γ_L (⚠ 둘 다 인쇄 오식 — §10-3) | 접착 응용 | p.51 |
| — | dΣ₁₂^d/dr₁₂ = −3Σ₁₂^d/r₁₂ (계면만) · −4/r₁₂ (벌크도) · ≈ −3.5/r₁₂ (강체 위 탄성체) · 2(dΣ₁₁^d/dr₁₁) = 8γ₁^d/r₁₁ · 2(dΣ₁₂^d/dr₁₂) = 7√(γ₁^dγ₂^d)/r₁₂ | 계면 이상 인장 강도 | p.52 · `eq_tensile_strength_interfaces.png` |

### 3-2. 표 [인쇄 — 단위 erg/cm² = mJ/m² · 20 °C]
| 표 | 내용 | 핵심 값 |
|---|---|---|
| I (p.42) | Hg 의 γ^d — 탄화수소 10 종과의 계면 장력 (γ_Hg = 484) | **200 ± 7** (194–211) · 표준편차 3.5 % |
| II (p.43) | 물의 γ^d — 탄화수소 8 종 (γ_W = 72.8) | **21.8 ± 0.7** (20.8–22.7) |
| III (p.45) | 저에너지 고체 γ_S^d (접촉각) | φ-dodecanoic acid on Pt 10.4 · 13.1 · HFP 18.0 · PTFE 19.5 · n-C₃₆H₇₄ 21.0 · n-octadecylamine on Pt 22.1 · paraffin 25.5 · Kel-F 30.8 · PE 35.0 · **PS 44.0** |
| IV (p.45) | γ_S^d (흡착 증기 π_e) | polypropylene 26 · 28.5 · graphite 123 (N₂) · 132 · 115 · 120 (헵탄) · Cu 60 · Ag 74 · Pb 99 · Sn 101 · Fe 108 (헵탄) · 106 (Ar) · 89 (N₂) · **ferric oxide 107** · **anatase 92 (헵탄) · 89 (부탄) · 141 (N₂)** · **silica 78** · **stannic oxide 111** · BaSO₄ 76 |
| V (p.47) | γ₂^d (실험) 와 물 속 A₁₂ 계산 | PTFE 19.5 → 8 × 10⁻¹⁶ erg · PE 35 → 2 × 10⁻¹⁴ · PS 44 → 5 × 10⁻¹⁴ · Cu 60 → 1.4 × 10⁻¹³ · anatase 91 → 3.5 × 10⁻¹³ · Fe₂O₃ 107 → 4.5 × 10⁻¹³ · graphite 110 → 5 × 10⁻¹³ · SnO₂ 118 → 5.5 × 10⁻¹³ · **SiO₂ 123** → 6 × 10⁻¹³ · **rutile 143** → 8 × 10⁻¹³ · Hg 200 → 1.3 × 10⁻¹² |
| VI (p.48) | 극성 유기 액체 γ_L^d (기준 고체 접촉각) | glycerol 63.4 → **37.0 ± 4** · formamide 58.2 → 39.5 ± 7 · methylene iodide 50.8 → 48.5 ± 9 · α-bromonaphthalene 44.6 → 47 ± 7 · dimethyl siloxanes 19.0 → 16.9 ± 0.5 · Fluorolube 20.2 → 14.0 ± 0.2 |
| VII (p.49) | Hg–유기 액체 초과 에너지 (γ₁₂^d − γ₁₂) | 요오드화 메틸 +55 · 에틸 머캅탄 +56 · 니트로에탄 +50 · 테트라브로모에탄 +41 · 아세트산 +34 · 올레산 +33 · 아닐린 0 · 디에틸 에테르 +5 · 알코올 −17 ~ +29 |
| VIII (p.49) | 물–유기 액체 초과 | 벤젠 +16.5 · 톨루엔 +15.4 · CCl₄ +6.3 · 부티로니트릴 +23.2 · 아닐린 +47.9 · 디부틸아민 +40.7 · 옥탄산 +42.8 · 시클로헥산올 +48.0 · 실록산 +12.1–12.6 |
| IX (p.51) | ★ 고체–액체 극성 초과 (π_e + 2γ_L − 2√(γ_S^dγ_L^d)) | graphite: 벤젠 20 · **anatase: 벤젠 26 · 프로판올 56 · 물 344** · **silica: 벤젠 20 · 아세톤 58 · 프로판올 84 · 물 368** · BaSO₄: 프로판올 96 · 물 362 · **SnO₂: 벤젠 26 · 프로판올 54 · 물 336** · 분산 항 2√(γ_S^dγ_L^d) = 94–118 |

### 3-3. 본문 수치 [인쇄]
- 물–Hg 계면 장력 예측 **424.8 ± 4.4** vs 실측 426–7 → 물–Hg 상호작용은 거의 분산력뿐 (쌍극자–금속 영상력 약함) [p.43].
- 파라핀 위 물 접촉각 예측 **111°** vs 실측 108–112° · Hg 예측 cos θ −0.8 vs 관측 −0.9 [p.44].
- 흑연 γ^d: 접촉각 (물 85.7°, π_e 19) 109 · 흡착열 (Graphon, n-헥산 5.0 kcal/mol, 54 Å²) 108 · π_e 115–132 · 침지열 97–120 · 루틸 139–148 vs 아나타스 ≈ 90 [p.45–46].
- 금속 분말 산화막 → H₂ 환원 뒤 π_e 감소: Cu 33 → 29 (γ^d 67 → 60) · Ag 38 → 37 (76 → 74) · Pb 51 → 49 (103 → 99) · Fe 54 → 53 (110 → 108) [p.45].
- *"The study of adsorption potentials of metals and oxides should eventually be done on ultraclean surfaces of known orientation. The values calculated from π_e measurements of adsorbed vapors on powdered solids are an average of several crystal faces and very probably have a high density of dislocations"* [p.45].
- 온도: 4 제곱 밀도 규칙 vs 8/3 제곱 — 78 K → 25 °C 에서 γ^d 감소 흑연 −2.2 / −1.6 % · 철 −2.7 / −2.1 % · 은 −4.3 / −3.1 % [p.46].
- 물 속 A₁₂ 실험 대조: arachidic acid 3–8 × 10⁻¹⁵ (γ^d 25–30) · polystyrene 5–6 × 10⁻¹⁴ · AgI 3–5 × 10⁻¹³ (γ^d 아마 80–100) · Se 2 × 10⁻¹³ → γ^d 72 · Au 1–6 × 10⁻¹² → 60–120 (⚠ §10-4) [p.47].
- 물이 퍼지려면 (S > 0) γ_S^d > **243** · 포름아마이드는 > 85 — 물은 흑연 · 산화막 없는 금속을 적시지 않는다 (White: 초청정 금은 물에 안 젖고 산화 금은 젖음 · Erb: 청정 Re · Ag · Pt · Pd · Au 물 접촉각 50–85°) [p.51].
- 벤젠 단분자층이 Hg–물 계면 장력을 30 erg/cm² 낮춰 물의 Hg 위 퍼짐 계수를 −14 → +16 으로 [p.51].
- 계면 인장 강도: PE (γ^d 35, r 4 Å) **70 × 10⁸ dyn/cm²** (105,000 psi) · PE–철 (√(γ₁^dγ₂^d) = 60) **105 × 10⁸** (157,000 psi) · *"measured tensile strengths are an order of magnitude lower, since failures are not the result of concerted breaking of bonds, but of crack initiation"* [p.52].

---

## 4. ★ 방법 — 틀 · 입자 처리

### 4-1. 틀 (Fig 1 · p.40–42)
- 표면 장력은 표면 "영역" 분자가 벌크 쪽으로 당겨져 늘어난 데 대한 일 (용수철 유비).  계면에서는 각 영역 분자가 자기 벌크와 **상대 상의 분산 인력**을 함께 받으므로 그 영역 장력 = γ_i − √(γ₁^dγ₂^d) → 두 영역의 합이 식 (1).
- 기준 액체 = 포화 탄화수소 (γ = γ^d) → 극성 · 금속 액체의 γ^d 를 계면 장력 하나로.  고체는 접촉각 (9) · 증기 흡착 π_e (12) · 흡착열 (13) · 침지열 (14) 로.
- 측정값 ↔ 분산 예측의 차 = 극성 초과 (Table VII–IX).

### 4-2. ★ 입자 처리
- 연속 평판 계면의 열역학 — 입자 · 접촉 역학 없음.  분말은 **흡착 측정의 기질** (비표면적 큰 분말의 평균 면 · 전위 밀도 높음, p.45) 로만 등장.
- 입자 사이 힘은 Hamaker 상수 (18)–(19) 를 거친 장거리 분산 인력으로 이어진다 — 구 기하는 이 논문에 없다 (구 기하 · 떼는 힘은 `johnson1971_jkr_surface_energy_contact_elastic_solids` · `dmt1975_adhesion_contact_deformation` · `vanoss1988_lifshitz_vdw_acid_base_interfacial` 식 28–32).

### 4-3. 기법 미니 용어집
- **γ^d (분산 성분)**: 표면 자유에너지 중 London 분산력 몫 — 모든 물질 사이에 작용하는 유일한 성분 (Fowkes 의 정의 · van Oss 의 γ^LW 는 이것을 Keesom · Debye 까지 넓힌 것).
- **퍼짐 압력 π_e**: 흡착막이 고체 표면 에너지를 낮춘 양 = γ_S − γ_SV.
- **임계 표면 장력 γ_c (Zisman)**: cos θ vs γ_L 외삽 cos θ = 1 의 γ_L — 분산력만의 액체로 정하면 γ_S^d 와 같다 (p.44).
- **퍼짐 계수 S**: γ_S − γ_L − γ_SL (> 0 이면 퍼짐).
- **Berthelot 기하평균**: 이종 분산 상호작용 계수 ≈ 동종 계수의 기하평균.

---

## 5. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1 | 액체 1 · 2 계면 영역 모식 — 각 영역 장력 γ_i − √(γ₁^dγ₂^d) · 합 = 식 (1) | ★ 기하평균 규칙의 물리 그림 — 논지 §2-1 의 원형 |
| 2 | 기름–물 퍼짐 계수 vs 기름 표면 장력 (순수 탄화수소 원 · 정제유 네모 · Zisman/Langmuir/Sawyer 측정) | 식 (6) 검증 |
| 3 | 저에너지 고체 넷 (PE · 파라핀 · C₃₆H₇₄ · 불소 단분자막) 위 cos θ vs √γ_L^d/γ_L — 원점 (−1) 을 지나는 직선 · 기울기 = 2√γ_S^d | ★ 접촉각 한 번으로 γ_S^d — 분말이면 wicking (vanoss1988 카드) |
| 4 | 침지열 vs γ_L (γ_S^d 90–150 곡선) · 루틸 네모 · 흑연 원 | 열량법 γ_S^d |
| 5 | 물 속 A₁₂ vs γ_S^d (식 19, 로그) — γ_S^d = 21.8 에서 0 | 매질 속 분산 인력 소멸 (습식 공정) |
| 6 | 기준 고체 9 종 위 극성 액체 접촉각 → γ_L^d (물 15–30 눈금) | 극성 액체 γ^d 결정 |
| 7 | 불소 액체 on 불소 고체 — 예측선 (실선) vs 실측 (점선) | ★ 기하평균 규칙의 실패 예 (20–25 %) |
| Table I · II (1 · 2) | Hg 200 ± 7 · 물 21.8 ± 0.7 | γ^d 기준값 |
| Table III · IV · V (3 · 4 · 5) | 고분자 · 금속 · 산화물 γ_S^d | ★ 산화물 γ^d 대역 |
| Table VI (6) | 극성 액체 γ_L^d | IGC · 접촉각 탐침 액체 |
| Table VII · VIII · IX (7 · 8 · 9) | 극성 초과 상호작용 | ★ 산화물–극성 상호작용의 크기 |
| 식 크롭 | `eq_*` (8 장) — 식 (1)–(19) · 접착 · 인장 강도 원문 | 식 원문 |

## 6. Post-processing ★
- **원문**: 계면 장력 · 접촉각 · π_e · 열량 자료를 식 (1) · (9) · (12) · (13) · (14) 에 넣어 γ^d 를 역산하고 독립 경로끼리 비교 (흑연 108 · 109 · 115–132 · 97–120).  평균 ± 표준편차만 (Table I · II · VI).
- **이 카드에서 한 것**: 물–Hg 424.7 · 파라핀 물 접촉각 110.6° · S > 0 문턱 243 · 85 · Table IX 분산 항에서 γ_S^d 역산 · 6πr² ↔ r = 2.76 Å · A₁₂ (19) 재계산 (§7 · §10).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 쪽 수치는 리포 출처를 병기)

### 7-1. ★ 논지 §2-1 · §2-3 을 Fowkes 꼴로 다시 읽으면 [우리 산술 · 추정]
- 원전의 규칙은 **W₁₂^d = 2√(γ₁^dγ₂^d)** (분산이 건너는 몫) 이고 동종 응집 W_ii = 2γ_i 는 **총** γ (분산 + 극성 + 금속 · 이온 …) 를 쓴다.  계면을 건너는 극성 상호작용이 있으면 **W₁₂ = 2√(γ₁^dγ₂^d) + I₁₂^p** (초과 항 — Table VII–IX 가 실측).
- ⇒ 논지 §2-3 의 SE–SE 우세 조건 W_SS/W_AS > 1.8 (매끈한 구 · AM_P) 을 이 꼴로 쓰면 **2γ_S / (2√(γ_A^dγ_S^d) + I_AS^p) > 1.8**.
  - I_AS^p = 0 이고 둘 다 분산뿐 (γ = γ^d) 이면 논지의 **γ_A/γ_S < 0.31** 그대로.
  - SE 가 분산 외 자기 응집 (극성 · 이온) 을 많이 가지면 (γ_S > γ_S^d) → SE–SE 쪽으로 기운다.
  - 산화물–황화물 사이 이온 · 쌍극자 초과 I_AS^p 가 크면 → AM–SE 쪽으로 기운다.
- 이 논문이 보여 주는 산화물 표면의 극성 초과 크기 (물 336–368 · 프로판올 54–96 · 벤젠 20–26 mJ/m², Table IX) 는 **분산 몫 (≈100) 과 같은 자릿수 이상** — 산화물이 끼는 계면에서 분산 기하평균만으로 W 를 정하면 크게 틀릴 수 있다는 정량 근거 [인쇄 + 추정].  단 NCM–LPSCl (고체–고체) 값은 없다 [미확인].

### 7-2. ★ 산화물 γ^d 대역 → NCM 의 자리 [추정 · 2 차 산술]
- 이 논문의 산화물 분말 γ_S^d: Fe₂O₃ 107 · 아나타스 89–92 (N₂ 141) · 루틸 139–148 · SnO₂ 111–118 · SiO₂ 78 / 123 · BaSO₄ 76 mJ/m² — **≈ 80–150 mJ/m²** (탈기 분말).
- 정본 `lippke2023_dem_drying_structure_formation_lib` 카드의 NMC–NMC Hamaker 2.11 × 10⁻¹⁹ J (2 차 인용) 를 이 논문의 A = 6πr²γ^d (6πr² = 1.44 × 10⁻¹⁸ m²) 로 바꾸면 **γ_NMC^d ≈ 147 mJ/m²** (van Oss 의 1.88 × 10⁻¹⁸ m² 로는 112 — `vanoss1988_…` §7-3) — 두 환산 모두 산화물 대역 안 [우리 산술].
- 정본 `garcia2017_nmc111_surface_energy_wulff_dft` 의 청정 DFT 벽개 (0.76–2.27 J/m²) 보다 5–20 배 작다 — 실온 분말의 분산 성분은 결합 절단 에너지가 아니다 [추정].
- 황화물 (LPSCl) γ^d 는 이 논문 · 정본 카드 어디에도 없다 [미확인] → 논지의 γ_A/γ_S 를 숫자로 놓으려면 SE 쪽 측정 (IGC 분산 성분 · 같은 묶음 IGC 리뷰 카드) 이 먼저다.

### 7-3. 우리 믹서 덱 (SJKR · CED) 과의 연결 [우리 산술]
- 쌍별 W_ij (위 7-1 꼴) → JKR 대응식 **CED_ij = [9·W_ij·E\*²/(4π²R\*)]^{1/3}** (`johnson1971_jkr_surface_energy_contact_elastic_solids` §7-1) → 덱 행렬.  현 덱 혼합쌍 min 규칙과의 차이는 `begat2004_cohesive_adhesive_balance_afm_colloid_probe` §7-3.
- 습식 ↔ 건식: 매질 속 A₁₂ = 6πr²(√γ₁^d − √γ₂^d)² — 입자 γ^d 가 매질 (물 21.8 · 용매) 에 가까우면 분산 인력이 사라진다 (Fig 5) — 건식 혼합 (기체 매질) 에서는 이 상쇄가 없다.

### 7-4. 측정 경로 (논지 §2-8) 에 주는 것
- 분말 γ_S^d 는 **증기 흡착 퍼짐 압력 π_e** (식 12) · 흡착열 · 침지열로도 잴 수 있다 — 접촉각 없이 (황화물 친화) [추정].  이 원리를 크로마토그래피로 옮긴 것이 IGC (같은 묶음 카드).
- 주의: 분말 값은 탈기 정도 · 산화막 · 면 평균에 민감 (π_e 산화 → 환원 Cu 67 → 60 · 표마다 실리카 78 ↔ 123).  NCM · LPSCl 측정은 **표면 이력 (드라이룸 노출 · 잔류 Li 염 · 가수분해)** 을 함께 적어야 한다.

### 7-5. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 표면 에너지 성분 · 결합 규칙 · 분산 값 · 극성 초과 — 쌍별 점착 입력의 물리 (D2 · D4 앞단).
- **없는 것**: 입자 접촉 역학 · 분말 유동 · 배터리 소재 값.

---

## 8. 적용 인사이트 (내 연구에 어떻게)
1. **기하평균은 γ^d 에** — 논지 §2-1 의 W_ij ≈ 2√(γ_iγ_j) 는 원전에서 "분산이 건너는 몫" 이다.  총 γ 로 쓰면 극성 · 이온 몫을 기하평균으로 잘못 섞는다.
2. **산화물 계면의 극성 초과는 분산 몫과 같은 자릿수 이상** (Table IX) — NCM (산화물) 이 낀 W 를 분산만으로 정하면 큰 오차가 날 수 있다.
3. **산화물 γ^d ≈ 80–150 mJ/m²** — NCM γ^d 의 사전 범위 [추정] · Hamaker 2.11 × 10⁻¹⁹ J 환산 112–147 과 맞는다.
4. **흡착 퍼짐 압력 · IGC 경로** — 액체 접촉 없이 분말 γ_S^d 를 재는 길 (황화물 후보).
5. **이상 강도는 실측보다 한 자릿수 크다** (결함 · 균열) — 계면 점착 에너지와 "떼는 힘" 사이에는 접촉 기하 · 결함이 끼어든다 (JKR · AFM 카드와 같은 교훈).

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "Fowkes (Ind. Eng. Chem. 1964) introduced the dispersion component γ^d of the surface free energy and showed that, when only dispersion forces act across an interface, γ₁₂ = γ₁ + γ₂ − 2√(γ₁^dγ₂^d), i.e., the work of adhesion is the geometric mean of the dispersion components."
- "Dispersion components measured on outgassed oxide powders (vapour-adsorption spreading pressures) lie at about 80–150 mJ m⁻² (e.g., Fe₂O₃ 107, anatase ≈ 90, SnO₂ 111–118 mJ m⁻²), and the polar excess interaction of water with these oxides (336–368 mJ m⁻²) is several times the dispersion term."
- 국문: *"기하평균 결합 규칙의 원전 (Fowkes 1964) 은 분산 성분 γ^d 에 대한 것이다 — 산화물이 낀 계면에서는 극성 초과 상호작용이 분산 몫보다 클 수 있다."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. **본문 식의 표기 불일치 둘** — 식 (5) 의 마지막 인자는 인쇄상 I₁I₂/√(I₁I₂) (= √(I₁I₂)) — 맞지만 읽기 어렵다 · 식 (16) 은 √A₁² · √A₂² 처럼 근호 안 제곱으로 인쇄 (= A₁ · A₂).
2. ★ **실리카 γ^d 가 표마다 다르다**: Table IV · 본문 (p.45 *"silica … (γ_S^d = 78), about the same as barium sulfate"*) = **78** ↔ Table V = **123** ↔ Table IX 헵탄 기준 분산 항 100 이 함의하는 γ_S^d ≈ **122.5** [우리 산술 — (100)²/(4 × 20.4)].  같은 방식으로 Table IX 의 아나타스 99 → 120 (Table IV · V 89–92) · BaSO₄ 99 → 120 (Table IV 76) — Table IX 는 다른 π_e 자료를 쓴 것으로 보인다 [추정].  ⇒ 산화물 γ^d 는 출처 따라 ±25 % 이상 흔들린다.
3. **p.51 퍼짐 계수 두 식의 오식**: "S = γ_S − (γ_L − γ_SL)" (부호 — p.43 의 S = γ_W − (γ_O + γ_OW) 와 맞으려면 +) · "S = √(γ_L^dγ_S^d) − 2γ_L" (계수 2 누락) — 본문 수치 (물 γ_S^d > 243 · 포름아마이드 > 85) 는 **2√(γ_L^dγ_S^d) − 2γ_L** 로만 나온다 [우리 산술: 72.8²/21.8 = 243.1 · 58.2²/39.5 = 85.8].
4. **금 A₁₂ 의 자릿수**: "gold (A₁₂ = 1 to 6 × 10⁻¹²) … 60 to 120 ergs per sq. cm." — 식 (19) 로 γ^d 60–120 은 A₁₂ **1.4–5.7 × 10⁻¹³** [우리 산술] (Table V 의 Cu 60 → 1.4 × 10⁻¹³ 과 같은 눈금) → "10⁻¹²" 는 한 자릿수 오식으로 보인다 [추정].  셀레늄 2 × 10⁻¹³ → 72 는 재현된다 (70.5).
5. **Hg on 파라핀 cos θ −0.8** (p.44) 은 Table III 파라핀 25.5 · γ_Hg^d 200 · γ_Hg 484 로 다시 계산하면 **−0.70** [우리 산술] — 어떤 γ_S^d 를 썼는지 [미확인].  (물 111° 는 110.6° 로 재현.)
6. **인장 강도 단위**: "105 × 10⁸ ergs/sq. cm." 는 dyn/cm² 여야 한다 (앞 문장 PE 는 dyn/cm²) · psi 환산 (105,000 · 157,000) 은 1 psi = 6.89 × 10⁴ dyn/cm² 기준 계산 (101,500 · 152,300) 보다 ≈ 3 % 크다 [우리 산술].
7. **분말 값의 상태** — 탈기 · 고온 처리 분말의 증기 흡착 (78 K · 90 K · 25 °C) — 공기 중 · 습도 있는 분말 표면과 다르다.  원문 스스로 "ultraclean surfaces of known orientation" 측정이 필요하다고 적는다.
8. **배터리 소재 값 없음** · 황화물 없음.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 10 | Fowkes, F. M., J. Phys. Chem. 66, 382 (1962). | γ^d 개념 (같은 저자 선행) |
| 15 | Girifalco, L. A., Good, R. J., J. Phys. Chem. 61, 904 (1957). | 기하평균 · Φ (vanoss1988 카드와 연결) |
| 16 | Graham, D., J. Phys. Chem. 68, 2788 (1964). | 폴리프로필렌 N₂ · Ar 흡착 → γ_S^d |
| 17 | Hamaker, H. C., Physica 4, 1058 (1937). | Hamaker 상수 |
| 19 | Harkins, W. D., "Physical Chemistry of Surface Films," Reinhold, N. Y., 1952 | π_e 자료 — 본문 p.49 가 Table IX 의 극성 증기 π_e 출처로 든다 |
| 21 | Harkins, W. D., Loeser, E. H., J. Chem. Phys. 18, 556 (1950). | 금속 · 산화물 π_e (Table IV) |
| 26 | Jura, G., Harkins, W. D., J. Am. Chem. Soc. 66, 1356 (1944). | 아나타스 흡착 |
| 6 | Boyd, G. E., Livingston, H. K., J. Am. Chem. Soc. 64, 2383 (1942). | 실리카 · BaSO₄ π_e (Table IV 78 · 76) |
| 28 | London, F., Trans. Faraday Soc. 33, 8–26 (1937). | 분산력 |
| 35 | Vold, M., J. Colloid Sci. 16, 1 (1961). | 식 (17) |
| 36 | White, M. L., J. Phys. Chem. 68, 3083 (1964). | 청정 금속의 물 비젖음 |
| 37 | Zisman, W. A., Ind. Eng. Chem. 55, 19 (1963). | 저에너지 고체 접촉각 (Fig 3 자료) |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 13 쪽 전부를 쪽 이미지 (100 · 150 dpi 전쪽 + 300 dpi 확대) 로 읽었다 · 식은 이미지에서 옮겼다 · 표 값은 이미지에서 칸마다 확인 (Table V 는 300 dpi 확대).
- 크롭 24 장 = Fig 1–7 · Table I–IX · 식 · 본문 영역 8 — 전부 손 크롭.  자동 추출은 쪽 전체가 한 장의 스캔 이미지라 다른 단 글자까지 잡아 (쪽 폭 전체) 쓰지 않았다.  컬러 JPEG 쪽 (p.40–41 · 43–44 · 47–48 · 50) 은 **220 dpi 회색조** (Fig 1 만 컬러 128 색) 로 렌더 — 원 스캔 300 ppi JPEG, 용량 때문.  1-bit 쪽은 300 dpi.  쪽 오른쪽 가장자리의 출판사 다운로드 워터마크 (세로 글자) 는 렌더 전 메모리 사본에서 텍스트만 지웠다 (스캔 이미지 · 그림 불변).
- 정본 litdb 중복 확인: 파일 목록 + "ie50660a008" · 제목 `git grep` 0 건.

## 🔗 관련 카드
- 같은 묶음: `vanoss1988_lifshitz_vdw_acid_base_interfacial` (LW + 산·염기 확장) · `johnson1971_jkr_surface_energy_contact_elastic_solids` · `begat2004_cohesive_adhesive_balance_afm_colloid_probe` · `garcia2017_nmc111_surface_energy_wulff_dft`.
- Hamaker 값: `lippke2023_dem_drying_structure_formation_lib` · 점착 접촉: `dmt1975_adhesion_contact_deformation`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

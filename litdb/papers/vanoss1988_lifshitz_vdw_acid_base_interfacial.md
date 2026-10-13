<!-- digest 표준 양식 확장 (paper-level STANDALONE).  ★ = 사용자가 특히 원한 항목.
     깊이 기준 = bazzoun2026_dem_fem_rnm_ionic.md · 형식 이웃 = faka2026_… · 같은 묶음 = johnson1971_… · begat2004_… · garcia2017_….
     원문 = 15 쪽 리뷰 (1-bit 300 ppi 스캔 + OCR 텍스트층) · 그림 없음 · 표 3 · 식 1–54 (+a·b·c) · 참고문헌 129 · SI 없음.
     쪽 표기 = 인쇄 쪽 (PDF n 쪽 = p.(926 + n)).  OCR 이 식을 깨뜨려 식은 전부 쪽 이미지에서 옮겼다.
     값 표지: [인쇄] = 원문 식 · 표 · 본문 / [우리 산술] = 원문 식 · 값 또는 다른 정본 카드 값으로 한 계산 / [추정] = 우리 해석 / [미확인] = 원문에 없음. -->
# Interfacial Lifshitz–van der Waals and Polar Interactions in Macroscopic Systems — 표면 장력 = LW (분산 · 반데르발스) 성분 + 산 · 염기 (AB, 전자 받개 γ⁺ · 전자 주개 γ⁻) 성분 · **기하평균 결합 규칙은 LW 성분에만 성립** (AB 는 비대칭: γ₁⁺γ₂⁻ · γ₁⁻γ₂⁺ 교차항) · 계면 장력이 **음수**가 될 수 있다 · 세 액체 접촉각으로 γ^LW · γ⁺ · γ⁻ 결정 · 산화물 · 황화물은 "particularly asymmetrical" — van Oss · Chaudhury · Good (Chem. Rev. 1988)

> slug `vanoss1988_lifshitz_vdw_acid_base_interfacial` · DOI `10.1021/cr00088a006` · type `review/theory (surface thermodynamics: Lifshitz–van der Waals + Lewis acid–base components of surface tension · combining rules · Young–Dupré contact-angle determination · Hamaker ↔ γ^LW · EL/AB/LW energy balance)` · PDF `8e4064d0-38._Interfacial_Lifshitz-van_der_Waals_and_polar_interactions_in_macroscopic_systems.pdf` · digested `2026-10-13` · status ✅
>
> **서지 (원문 인쇄)**: Carel J. van Oss\* (Depts of Microbiology and Chemical Engineering, SUNY Buffalo) · Manoj K. Chaudhury (Dow Corning Corp., Midland) · Robert J. Good (Dept of Chemical Engineering, SUNY Buffalo) · *Chem. Rev.* **1988**, 88, 927–941 · Received 1987-11-02 (Revised Manuscript Received 1988-07-08) · 판권 코드 0009-2665/88/0788-0927$06.50/0 [인쇄 p.927].
> DOI 출처: PDF 문서 메타데이터 (keywords "article doi: 10.1021/cr00088a006") + 매 쪽 인쇄 워터마크 경로 `…/article-pdf/88/6/927/1895921/cr00088a006.pdf` — 본문 머리말에는 DOI 문자열이 인쇄돼 있지 않다.
> ★ **이 카드가 맡는 일** — 이종기술 논지 (`docs/hetero_thesis.md`) §2-1 의 **기하평균 결합 규칙 W_ij ≈ 2√(γ_iγ_j)** 가 언제 성립하고 언제 깨지는지의 원전 · §2-7 *"극성 (산 · 염기) 성분 — 산화물 · 황화물 계면에서 기하평균 규칙이 깨질 수 있다"* 의 근거 · §4 D2 (쌍별 결합 규칙) 의 후보식.
> (Robert J. Good 의 저자 소개 [인쇄 p.928]: *"In 1957, with … Louis A. Girifalco and with Dr. Gerhard Kraus, he proposed the 'geometric mean' relation for the energy of adhesion between two phases across an interface and the energies of cohesion of the separate phase."* — 기하평균 규칙 창안자 본인이 공저한 "그 규칙의 한계" 리뷰다.)

---

## 0. 결론 먼저 — 우리 질문에 대한 답

**한 문장**: 기하평균 결합 규칙 γ₁₂ = (√γ₁ − √γ₂)² (⇔ W₁₂ = 2√(γ₁γ₂)) 은 **완전 무극성 (LW 만) 물질끼리에만** 성립하고 [인쇄 식 18 · p.930], 극성 (Lewis 산 · 염기) 상호작용은 **비대칭** — 받개 γ⁺ 와 주개 γ⁻ 의 **교차항** W₁₂^AB = 2(√(γ₁⁺γ₂⁻) + √(γ₁⁻γ₂⁺)) 로만 맞는다 [인쇄 식 33] — 그래서 계면 장력이 음수가 될 수도 있고 (식 38a · b), 총 γ 에 기하평균을 쓰면 경험 보정 Φ = 0.53–1.17 이 필요해진다 [인쇄 식 18b · p.933].
우리 논지에 대어 보면 [우리 산술 — §7-1]: **ΔW = W_AA + W_SS − 2W_AS = 2γ_AS (계면 장력의 두 배)** 이고, van Oss 꼴로 **ΔW = 2(√γ_A^LW − √γ_S^LW)² + 4(√γ_A⁺ − √γ_S⁺)(√γ_A⁻ − √γ_S⁻)** — 첫 항은 늘 ≥ 0 (논지 §2-2 의 식) 이지만 **둘째 항은 음수일 수 있다** ⇒ 한쪽이 더 산성 · 다른 쪽이 더 염기성이면 섞인 (AM–SE) 접촉이 에너지상 유리해진다 (begat2004 카드의 salbutamol–lactose 가 그 예).

| 우리 질문 | 이 논문이 주는 것 | 표지 · 쪽 |
|---|---|---|
| ★ 기하평균 규칙의 근거 · 범위 | **Good–Girifalco–Fowkes 결합 규칙** γ₁₂^LW = (√γ₁^LW − √γ₂^LW)² (18) = γ₁^LW + γ₂^LW − 2√(γ₁^LWγ₂^LW) (18a) — *"For all exclusively Lifshitz–van der Waals interactions, i.e., interactions between two completely apolar compounds 1 and 2"* · Dupré (19) 와 합치면 W₁₂^LW = 2√(γ₁^LWγ₂^LW) [우리 산술] | [인쇄] p.930 |
| ★ 극성 쪽은 | γ_i^AB = 2√(γ_i⁺γ_i⁻) (35) · ΔF₁₂^AB = −2(√(γ₁⁺γ₂⁻) + √(γ₁⁻γ₂⁺)) (33) · γ₁₂^AB = 2(√γ₁⁺ − √γ₂⁺)(√γ₁⁻ − √γ₂⁻) (37a) — **음수 가능** (γ₁⁺ > γ₂⁺ 이고 γ₁⁻ < γ₂⁻ 일 때 등, 38a · b) · *"Fowkes has pointed out that polar interactions do not follow the combining rule that is valid for apolar interactions; in other words, eq 18c is, in general, wrong"* | [인쇄] p.932–934 |
| ★ 산화물 · 황화물 | *"when 1 is a particularly asymmetrical material, such as an oxide, a sulfide, an alcohol, a ketone, an ether, etc., the value of √(γ₁⁻γ₂⁺) tends to be considerable, while γ₁^AB and √(γ₁⁺γ₂⁻) are close to zero"* — 즉 **단극성 전자 주개 (γ⁻ 큼 · γ⁺ ≈ 0)** 로 취급 (물을 상대로 한 문맥) | [인쇄] p.934 |
| 전체 표면 장력 | γ = γ^LW + γ^AB (42) · γ_i = −½ΔF_ii (16, 극성 · 무극성 모두) · 고체도 같은 정의 | [인쇄] p.930 · 931 · 933 |
| 측정법 | Young–Dupré (1 + cos θ)γ_L = 2(√(γ_S^LWγ_L^LW) + √(γ_S⁺γ_L⁻) + √(γ_S⁻γ_L⁺)) (41) — **액체 셋 (그중 둘은 극성) 의 접촉각**으로 고체의 γ^LW · γ⁺ · γ⁻ · 무극성 고체는 γ_S^LW 만 (24, 24a) · 분말은 wicking · 기준값 물 γ_W^LW 21.8 · γ_W⁺ = γ_W⁻ = 25.5 · γ_W^AB 51 · γ_W 72.8 mJ/m² (가정 기준) | [인쇄] p.931 · 933 · 935 · 937 |
| Hamaker ↔ γ^LW | γ_i = A_ii/(24πl₀²) (15) · l₀ = **1.58 ± 0.08 Å** · A_ii/γ_i^LW = **(1.88 ± 0.19) × 10⁻¹⁴ cm²** (±8 % 불확도) · Table III (액체 · 고분자 · 수은의 A · γ^LW) | [인쇄] p.930 · 938 |
| 거리 감쇠 · 구 | ΔF^LW = −A/12πd² (25) · 두 구 −AR/12d (28) · 구–평판 −AR/6d (29) · 힘 두 구 AR/12d² (32) · AB 는 지수 감쇠 exp(−d/λ), 물 λ ≈ 2 Å (44–45) | [인쇄] p.932 · 935 |
| 직접 힘 측정과의 대조 | 헥사데실 층 (물 속) 접촉 인력 실측 ≈ −60 mJ/m² ↔ 식 (43) · (16) −102.7 (이상) · 접촉각 (θ 95°) 로 −67 mJ/m² — "quite satisfactory" | [인쇄] p.939 |
| 황화물 · NCM 값 | **없다** — 실린 값은 유기 액체 · 고분자 · 수은 · 물 | [미확인] |

⛔ **한정어 (떼지 말 것)**: ① 수용액 · 생체 고분자 · 콜로이드 맥락의 리뷰 — 무기 분말 (NCM · LPSCl) 값은 없다 ② γ⁺ · γ⁻ 의 절대 눈금은 **물 기준값 25.5 / 25.5 를 가정**한 상대 척도 ("arbitrary (but plausible)") ③ 산화물 · 황화물의 "비대칭" 은 한 문장 (물을 상대로 한 서술) 의 분류이고 측정값이 아니다 ④ 이 틀의 성분 결정은 **접촉각 (액체)** 이 전제 — 공기 · 수분 민감 황화물에 그대로 쓰기 어렵다 (§7-4) ⑤ 원문에 식 · 표 인쇄 결함이 있다 (§10).

---

## 1. 한 줄 요약
반데르발스 힘을 Keesom · Debye · London 셋의 합으로 보고 Lifshitz 거시 이론으로 묶어 **LW 성분** 으로 정의하고 (Hamaker 상수 A 가 셋의 합에 적용된다), 그와 별개로 **Lewis 산 · 염기 (AB, 수소결합 포함) 성분**을 받개 γ⁺ · 주개 γ⁻ 두 매개변수로 비대칭하게 다룬다.
LW 는 기하평균 결합 규칙 (Good–Girifalco–Fowkes) 을 따르지만 AB 는 교차항 √(γ₁⁺γ₂⁻) + √(γ₁⁻γ₂⁺) 를 따르므로, 총 γ 에 기하평균을 쓰면 실측 계면 장력과 1.7–51 mJ/m² 까지 어긋난다 (Girifalco–Good 의 Φ 0.53–1.17).
이 틀로 Young–Dupré 식을 일반화해 액체 셋의 접촉각으로 고체의 γ^LW · γ⁺ · γ⁻ 를 얻고, 계면 장력 · 응집 · 접착 · 매질 속 상호작용 (소수성 인력 · 수화 반발 · 단극성 반발) 을 하나의 식 (43) · (52) 으로 계산한다.
수용 매질에서는 AB 항이 LW 보다 보통 10–100 배 크고 (p.936), Hamaker 상수와 γ^LW 는 A/γ^LW = 1.88 × 10⁻¹⁴ cm² 로 이어진다 (l₀ = 1.58 Å).

## 2. 메타
| 저자 | 저널/년 | DOI | 소재 | 연구유형 |
|---|---|---|---|---|
| **C. J. van Oss\*** · M. K. Chaudhury · R. J. Good (SUNY Buffalo · Dow Corning) | Chem. Rev. **88** (1988) 927–941 · 접수 1987-11-02 · 수정 1988-07-08 | 10.1021/cr00088a006 (메타데이터 · 워터마크) | 무관 (이론) — 표 값: 유기 액체 · 물 · PTFE · polystyrene · PMMA · 수은 · 저온 기체 | 리뷰 · 이론 (계면 열역학) + 실험 검증 사례 |

| 원문 구조 | 쪽 | 내용 |
|---|---|---|
| I. Introduction | 927–929 | Keesom · Debye · London · Hamaker · DLVO · 반발 반데르발스 · 소수성 · 수화 · 삼투 |
| II.A LW interactions (Lifshitz · 계면 LW · 인력/반발 · Young · 거리 감쇠) | 929–932 | 식 (1)–(32) · Table I–II |
| II.B Polar (AB) interactions (AB 열역학 · Young–Dupré · 양/음 계면 장력 · 단극성 · 감쇠) | 932–935 | 식 (33)–(45) · (16c) · (18b)–(18c) · (20a) · (43a)–(43b) |
| II.C Electrostatic · II.D Energy balance | 935–937 | 식 (46)–(51) |
| III.A Contact angle (Young · 액체 간 · 매질 속 · Hamaker ↔ γ^LW · AB 의 함의) | 937–939 | 식 (52)–(54) · Table III |
| III.B Electrokinetic · III.C Direct force measurement | 939–940 | 헥사데실 · 인지질 · PVA · PEG |
| IV. References (129) | 940–941 | |

- 중복 확인 (2026-10-13): 정본 `litdb/papers/` 전수 목록에 vanoss 파일 없음 · `git grep -i` "cr00088a006" · "polar interactions in macroscopic" 0 건 → 새 카드.

---

## 3. 핵심 식 (★ 원문 그대로 — 크롭 `eq_*.png` · `txt_*.png`)

### 3-1. LW (Lifshitz–van der Waals) [인쇄 p.929–932]
| 식 | 원문 | 뜻 |
|---|---|---|
| (9) · (10) | ΔF₁₁(l) = −A₁₁/(12πl²) · A₁₁ = (3kT/2) Σ′ₙ Σⱼ [(ε₁(iωₙ) − 1)/(ε₁(iωₙ) + 1)]^{2j}/j³ | Lifshitz Hamaker 상수 (유전 함수에서) |
| (14) | A₁₁ = [3/(16√2)]·(n₀² − 1)²/(n₀² + 1)^{1.5}·ħω_UV | Israelachvili 근사 (굴절률 · UV 흡수) |
| (15) | γ₁ = A₁₁/(24πl₀²) | Hamaker ↔ 표면 장력 |
| (16) | γ_i = −½ΔF_ii — *"surface tension … is defined as half of the free energy change due to cohesion of the material in vacuo"* | 정의 |
| (17) | γ_i = Σⱼ γ_i^j (Fowkes: 분산 · 극성 · 유도 · 수소결합 · 금속) | 성분 분해 |
| (18) · (18a) | γ₁₂^LW = (√γ₁^LW − √γ₂^LW)² = γ₁^LW + γ₂^LW − 2√(γ₁^LWγ₂^LW) | ★ 결합 규칙 (무극성 전용) |
| (19) | ΔF₁₂^LW = γ₁₂^LW − γ₁^LW − γ₂^LW (Dupré) | 진공 속 1–2 상호작용 |
| (16a) · (16b) | ΔF₁₂₁^LW = −2γ₁₂^LW (1 이 액체 2 속) · ΔF_ii^LW = −2γ_i^LW | |
| (20) · (21) | ΔF₁₃₂^LW = γ₁₂^LW − γ₁₃^LW − γ₂₃^LW = (√γ₁^LW − √γ₃^LW)(√γ₃^LW − √γ₂^LW) | 매질 3 속 상호작용 |
| (22)–(23) | 인력: γ₃ 가 γ₁ · γ₂ 둘보다 크거나 작을 때 · **반발**: γ₃ 가 둘 사이 (γ₁ > γ₃ > γ₂) | 반발 반데르발스 조건 |
| (24) · (24a) | γ_L(1 + cos θ) = 2√(γ_S^LWγ_L^LW) · 무극성 액체면 1 + cos θ = 2√(γ_S^LW/γ_L) | 무극성 Young |
| (25)–(27) | ΔF_d^LW = −A/(12πd²) · A = A_dispersion + A_orientation + A_induction + coupling · ΔF_d^LW = ΔF_d0^LW(d₀/d)² | 평판 감쇠 · *"it actually applies to all three electrodynamic interactions"* |
| (28) · (29) | 두 구 −AR/12d · 구–평판 (· 교차 원기둥) −Ar/6d (R ≫ d) | 구 기하 |
| (30)–(32) | 힘: 평판 A/6πd³ (압력) · 구–평판 AR/6d² · 두 구 AR/12d² | 떼는 힘 꼴 (d = d₀ 에서 DMT 와 같다 — §4-3) |
| d₀ | *"the best empirical value for d₀ (eq 27) is 1.58 ± 0.08 Å"* · Born 반발 미포함 | |

### 3-2. AB (Lewis 산 · 염기) [인쇄 p.932–935]
| 식 | 원문 | 뜻 |
|---|---|---|
| (33) | ΔF₁₂^AB = −2(√(γ₁⁺γ₂⁻) + √(γ₁⁻γ₂⁺)) | ★ 교차항 — 받개 1 × 주개 2 + 주개 1 × 받개 2 |
| (34) · (35) | ΔF_ii^AB = −4√(γ_i⁺γ_i⁻) · γ_i^AB = 2√(γ_i⁺γ_i⁻) | 자기 응집의 AB |
| (36) · (37) | ΔF₁₂^AB = γ₁₂^AB − γ₁^AB − γ₂^AB · γ₁₂^AB = 2(√(γ₁⁺γ₁⁻) + √(γ₂⁺γ₂⁻) − √(γ₁⁺γ₂⁻) − √(γ₁⁻γ₂⁺)) | |
| (37a) | γ₁₂^AB = 2(√γ₁⁺ − √γ₂⁺)(√γ₁⁻ − √γ₂⁻) | ★ 음수 가능 (Small 1953 이 같은 꼴) |
| (38a) · (38b) | γ₁₂^AB < 0: γ₁⁺ > γ₂⁺ 이고 γ₁⁻ < γ₂⁻ · 또는 반대 | |
| (39)–(41) | (1 + cos θ)γ_L = −ΔF_SL^tot · ΔF^tot = ΔF^LW + ΔF^AB · **(1 + cos θ)γ_L = 2(√(γ_S^LWγ_L^LW) + √(γ_S⁺γ_L⁻) + √(γ_S⁻γ_L⁺))** | ★ 세 액체 접촉각 → γ_S^LW · γ_S⁺ · γ_S⁻ |
| (42) | γ = γ^LW + γ^AB | |
| (16c) · (20a) | ΔF₁₃₁^tot = −2γ₁₃ · ΔF₁₃₂^tot = γ₁₂ − γ₁₃ − γ₂₃ | 매질 속 응집 · 접착 |
| (43) | γ₁₂ = (√γ₁^LW − √γ₂^LW)² + 2(√(γ₁⁺γ₁⁻) + √(γ₂⁺γ₂⁻) − √(γ₁⁺γ₂⁻) − √(γ₁⁻γ₂⁺)) | ★ 총 계면 장력 |
| (18b) | γ₁₂ = γ₁ + γ₂ − 2Φ√(γ₁γ₂) — Girifalco–Good 상호작용 매개변수 **Φ 0.53–1.17** | 총 γ 기하평균의 실패를 보정하던 경험 인자 |
| (18c) | γ₁₂ = (√γ₁^LW − √γ₂^LW)² + (√γ₁^AB − √γ₂^AB)² — *"does not furnish the right answer either"* · Fowkes: *"eq 18c is, in general, wrong"* | 극성 성분 기하평균도 틀림 |
| (43a) · (43b) | 비대칭 물질 1 (산화물 · 황화물 · 알코올 · 케톤 · 에테르): γ₁₂ ≈ (√γ₁^LW − √γ₂^LW)² + γ₂^AB − 2√(γ₁⁻γ₂⁺) | 물 상대: γ₂^AB = 51 · −2√(γ₁⁻γ₂⁺) 는 ≈ −6 ~ −49 mJ/m² |
| (44) · (45) | P(d) = P(d₀)exp(−d/λ) · ΔF^AB(d) = ΔF^AB(d₀)exp[(d₀ − d)/λ] · 물 λ ≈ 2 Å (이온 세기 크면 12 Å · 실측 130 Å 보고) | AB 감쇠 |
| (52) | ΔF₁₃₂^tot = γ₁₂^LW − γ₁₃^LW − γ₂₃^LW + 2[√γ₃⁺(√γ₁⁻ + √γ₂⁻ − √γ₃⁻) + √γ₃⁻(√γ₁⁺ + √γ₂⁺ − √γ₃⁺) − √(γ₁⁺γ₂⁻) − √(γ₁⁻γ₂⁺)] | 매질 속 이종 물질 상호작용 |
| (53a) · (53b) · (54) | A_ii/γ_i^LW = 3.01 × 10⁻¹⁴ cm² (Israelachvili, l₀ ≈ 2 Å) · A_ii/γ_i = 1.51 × 10⁻¹⁴ cm² (Fowkes) · A_ii = γ_i^LW/32πl_eq² (⚠ 인쇄 그대로 — §10-1) | Hamaker ↔ γ^LW |

### 3-3. 수치 · 표 [인쇄]
| 항목 | 값 | 쪽 |
|---|---|---|
| 물 기준 (가정) | γ_W⁺ = γ_W⁻ = **25.5** mJ/m² → γ_W^AB = 2√(γ_W⁺γ_W⁻) = **51** · γ_W^LW **21.8** · γ_W **72.8** | 933 · 935 |
| 단극성 반발 | γ⁻ 단극성 물질은 **γ⁻ ≥ 28 mJ/m²** 이면 물 속에서 서로 밀어낸다 (γ₁₂ < 0 → ΔF₁₂₁ > 0) · 예: DMSO · agarose · gelatin · dextran · PEG · RNA · cellulose acetate · PVA (γ⁻ 57 · PEG 64) | 935 · 940 |
| 무극성–물 | 대부분 무극성 물질 γ^LW ≈ 물 (21.8) → γ₁₃^LW < 1 → 물 속 ΔF₁₃₁^tot ≈ **−102 mJ/m²** (소수성 인력의 원천 = 물의 γ^AB) | 933 |
| 액체–물 계면 장력 | 유기 액체 γ 20–29 mJ/m² → 식 (18) 이면 γ₁₂ 10–17 이어야 하는데 실측 **1.7–51 mJ/m²** (Girifalco & Good 1957) | 933 |
| 에너지 균형 | 수용 매질에서 ΔF₁₃₁^AB 가 보통 LW 의 **10–100 배** · EL (ζ ≤ 15 mV) 의 수 배 | 936 |
| Table III l 값 | l_eq 평균 **1.36 ± 0.07 Å** (식 54) · l₀ **1.58 ± 0.08 Å** (식 15) · A/γ^LW = (1.88 ± 0.19) × 10⁻¹⁴ cm² | 938 |
| Table III 예 (A ×10²⁰ J · γ^LW mJ/m²) | PTFE 3.8 · 19 · water 4.62 · 21.8 · hexadecane 4.43 · 27.7 · glycerol 6.7 · 34 · polystyrene 6.58 · 8 (⚠ §10-2) · PMMA 7.11 · 40 · mercury 33 · 200 | 938 |
| 헥사데실 직접 측정 | 접촉 인력 ≈ **−60 mJ/m²** (Pashley 힘 측정) ↔ 식 (43)·(16) 이상값 −102.7 ↔ 접촉각 θ 95° 와 식 (41) 로 **−67** | 939 |

---

## 4. ★ 방법 — 틀 · 측정 사슬 · 입자 처리

### 4-1. 틀
- γ_i 를 응집 자유에너지의 절반 (−½ΔF_ii) 으로 정의 → 고체에도 같은 정의 (p.931).
- γ = γ^LW (Lifshitz: 분산 · 배향 · 유도 합) + γ^AB (2√(γ⁺γ⁻)).  금속 · 정전 (EL) 은 별도.
- 상호작용 자유에너지는 Dupré 식으로 계면 장력에서 얻고, 계면 장력은 LW 기하평균 + AB 교차항 (43).
- 매질 3 속 상호작용 ΔF₁₃₂ 는 (20) · (52) — 매질에 따라 인력 · 반발이 바뀐다.

### 4-2. 측정 사슬 (원문 §IIIA)
무극성 고에너지 액체 (α-bromonaphthalene · diiodomethane) 접촉각 → (24a) 로 γ_S^LW → 극성 액체 둘 (물 · glycerol: γ⁺ · γ⁻ 큼) 접촉각 → (41) 두 번 → γ_S⁺ · γ_S⁻ (p.937).  분말 · 입자는 **wicking** 으로 전진 접촉각 · 이력 (hysteresis) 은 표면 불균일의 신호 (전진 = 낮은 에너지 성분 · 후퇴 = 높은 성분).

### 4-3. ★ 입자 처리 · 우리 점착 식과의 연결
- 구–구 · 구–평판 LW 에너지 · 힘 (28)–(32) 는 Derjaguin 근사 (R ≫ d) · 강체 (변형 없음).  d = d₀ 에서 두 구의 힘 AR/12d₀² = **2πR\*·W^LW** (R\* = R/2, W^LW = 2γ^LW = A/12πd₀²) [우리 산술] — 즉 DMT (`dmt1975_adhesion_contact_deformation`) 의 떼는 힘과 같은 꼴 · JKR (`johnson1971_jkr_surface_energy_contact_elastic_solids`) 이면 계수 1.5.
- ⇒ 우리 믹서 CED 로 내리는 사슬 [우리 산술 · 추정]: γ_i^LW · γ_i^± (측정) → **W_ij = 2√(γ_i^LWγ_j^LW) + 2(√(γ_i⁺γ_j⁻) + √(γ_i⁻γ_j⁺))** (진공 · 건조 기체 매질) → JKR 대응식 CED_ij = [9W_ijE\*²/(4π²R\*)]^{1/3} (johnson1971 카드 §7-1).

### 4-4. 기법 미니 용어집
- **LW 성분 (γ^LW)**: Lifshitz 이론의 전기역학적 상호작용 (London 분산 + Keesom 배향 + Debye 유도) 몫 — 이 논문은 셋을 묶는다 (Fowkes 의 "분산 성분 γ^d" 보다 넓다).
- **AB 성분 · γ⁺ · γ⁻**: Lewis 산 (전자 받개) · 염기 (전자 주개) 매개변수 · γ^AB = 2√(γ⁺γ⁻).
- **단극성 (monopolar)**: γ⁺ 또는 γ⁻ 하나만 있는 표면 — 자기 AB 응집은 0 이지만 상대가 반대 성분을 가지면 강한 AB 접착.
- **Dupré 식**: ΔF₁₂ = γ₁₂ − γ₁ − γ₂ (= −W₁₂).
- **Girifalco–Good Φ**: 총 γ 기하평균을 실측에 맞추는 경험 인자.
- **wicking**: 분말 기둥에 액체가 스며드는 속도로 접촉각을 재는 법.

---

## 5. Figure set ★ (그림 없음 — 표 · 식 크롭)
| 크롭 | 내용 | 우리 활용 |
|---|---|---|
| Table 1 | 마이크로파 영역 유전 분산 (ethanol · methanol · glycerol · water: ε_∞ · ε₀ · Cole–Cole α · ω_MW) | Lifshitz Hamaker 계산 입력 |
| Table 2 | 분광 상수 (n₀² · ω_IR · ω_UV) — He … PTFE · 물 · 알칸 · 벤젠 · CS₂ · glycerol · PMMA | 식 (12)–(14) 입력 |
| Table 3 | ★ Hamaker 상수 · γ^LW · l_eq · l₀ (24 물질) | A ↔ γ^LW 환산 · ⚠ polystyrene 오기 |
| `eq_16_20_lw_combining_rule.png` | ★ 식 (16)–(20) · 결합 규칙 범위 문장 | 논지 §2-1 의 기하평균 근거 · 범위 |
| `eq_21_23_lw_repulsion_in_liquid.png` | 식 (21)–(23) 반발 반데르발스 | 습식 (용매) 에서 점착이 뒤집힐 수 있음 |
| `eq_24_young_apolar.png` | 식 (24) · (24a) | 무극성 액체로 γ^LW |
| `eq_25_32_decay_hamaker.png` | 식 (25)–(32) · d₀ 1.58 Å | 구 기하 힘 · DMT 연결 |
| `eq_33_37_acid_base.png` | ★ 식 (33)–(37a) | AB 교차항 · 음의 γ₁₂^AB |
| `eq_38_42_young_dupre.png` | 식 (38)–(42) · (16c) · (20a) | 세 액체 접촉각 측정식 |
| `eq_43_18b_interfacial_tension.png` | ★ 식 (43) · (18b) Φ | 총 계면 장력 · 기하평균 실패의 실측 |
| `eq_18c_43b_oxide_sulfide.png` | ★ 식 (18c) · (43a) · (43b) · "oxide, sulfide" 문장 · Fowkes "18c is wrong" | 산화물 · 황화물 = 비대칭 |
| `txt_monopolar_water_reference.png` | 단극성 · 물 기준값 25.5 · γ⁻ ≥ 28 반발 · 식 (44)–(45) | 기준 · 단극성 반발 |
| `eq_52_three_liquids.png` | §IIIA1 측정 절차 · 식 (52) | 측정 설계 |
| `eq_53_hamaker_vs_gammaLW.png` | 식 (53a) · (53b) | Hamaker ↔ γ |
| `eq_54_proportionality.png` | 식 (54) · 1.88 × 10⁻¹⁴ cm² · ±8 % | ★ 환산 상수 |
| `txt_hexadecyl_direct_force.png` | 헥사데실 −60 vs −67 vs −102.7 mJ/m² | 이론 ↔ 직접 힘 측정 |

## 6. Post-processing ★
- **원문**: 접촉각 → (24a) · (41) 연립 · Lifshitz 식 (10) · (12) · (14) 수치 적분 → Hamaker 상수 · l_eq · l₀ (Table III) · 직접 힘 측정과 대조.
- **이 카드에서 한 것**: Table III 의 l_eq · l₀ 를 식 (15) · (54) 로 재계산 (polystyrene 행 검사) · 헥사데실 −102.7 재현 · ΔW 항등식 · 정본 카드 Hamaker 값으로 γ^LW 환산 (§7).

---

## 7. 우리 DEM+MPM 대비 → `our_dem_baseline.md` (⚠ 정본 브랜치에서는 값 자리표시 상태 — 우리 쪽 수치는 리포 출처를 병기)

### 7-1. ★ 논지 §2-2 의 ΔW 를 이 틀로 다시 쓰면 [우리 산술]
- Dupré (W_ij = γ_i + γ_j − γ_ij, W_ii = 2γ_i) 만으로: **ΔW ≡ W_AA + W_SS − 2W_AS = 2γ_AS** — 논지의 ΔW 는 **AM–SE 계면 장력의 두 배** 다 (결합 규칙과 무관한 항등식).
- 기하평균 (LW 만) 이면 2γ_AS = 2(√γ_A − √γ_S)² ≥ 0 — 논지 §2-2 의 식 그대로.
- van Oss 꼴 (43) 이면 **ΔW = 2(√γ_A^LW − √γ_S^LW)² + 4(√γ_A⁺ − √γ_S⁺)(√γ_A⁻ − √γ_S⁻)** — 둘째 항은 **A 가 더 산성 · S 가 더 염기성 (또는 반대) 일 때 음수**.  그 크기가 첫 항보다 크면 **ΔW < 0** → 같은 상끼리가 아니라 **섞인 접촉이 에너지상 유리** (자발 분산 · 코팅 쪽).
- 정본 `begat2004_cohesive_adhesive_balance_afm_colloid_probe` 카드의 salbutamol sulfate–lactose 가 이 경우의 실측 예 (CAB 곱 0.050 → W_AB 가 기하평균의 4.49 배) — 반대로 budesonide–lactose 는 9.06 (0.33 배) 이라 첫 항 쪽 극단 (그 카드 §7-2).
- ⇒ 논지 §2-2 의 *"ΔW ≥ 0 — 표면 에너지가 다르면 같은 상끼리 붙는 배치가 늘 유리하다"* 는 **무극성 (LW) 가정의 결과** 이고, 산 · 염기 비대칭이 있으면 부호가 바뀔 수 있다.  ⚠ 논지 문서 수정은 1저자 비준 사항 — 이 카드는 근거만 적는다.

### 7-2. ★ 산화물 (NCM) · 황화물 (LPSCl) 을 이 틀에 놓으면 [인쇄 + 추정]
- 원문 분류: 산화물 · 황화물은 *"particularly asymmetrical"* — √(γ₁⁻γ₂⁺) (자기 γ⁻ × 상대 γ⁺) 가 크고 γ₁^AB · √(γ₁⁺γ₂⁻) 는 0 근처 = **단극성 전자 주개** (물을 상대로 한 문맥) [인쇄 p.934].
- 둘 다 순수 단극성 주개 (γ⁺ = 0) 라면 [우리 산술]: W_AA^AB = W_SS^AB = W_AS^AB = 0 → **건조 매질의 응집 · 접착은 LW 만** → 기하평균 W_ij = 2√(γ_i^LWγ_j^LW) 가 **γ^LW 에 대해** 성립한다.  이때 논지의 비 γ_A/γ_S 는 **γ^LW 의 비** 로 읽어야 하고, 총 γ (DFT 벽개 · 접촉각 총값) 를 쓰면 안 된다.
- 그러나 NCM 표면에는 노출 전이금속 · Li⁺ (Lewis 산 자리) · 잔류 LiOH/Li₂CO₃ (염기), LPSCl 에는 Li⁺ 와 S²⁻/Cl⁻ (주개) · 가수분해 생성물이 있다 — **γ⁺ 가 0 이라는 근거는 없다** [추정].  산 · 염기 교차항이 살아 있으면 §7-1 의 둘째 항이 NCM–LPSCl 을 서로 **더 끌어당기는** 쪽일 가능성 (NCM 쪽 산 자리 × LPSCl 주개) [추정] — 그러면 비코팅에서도 SE 가 NCM 에 붙는 쪽으로 기울어 논지 P1 이 약해진다.
- ⇒ 판가름에 필요한 양: γ_NCM^LW · γ_NCM^± · γ_SE^LW · γ_SE^± (또는 직접 CAB, begat2004 카드).  이 논문 자체에는 둘의 값이 없다 [미확인].

### 7-3. Hamaker ↔ γ^LW 환산으로 본 NCM [우리 산술 · 2 차 출처]
- 이 논문의 A/γ^LW = 1.88 × 10⁻¹⁸ m² (l₀ 1.58 Å) 에 정본 `lippke2023_dem_drying_structure_formation_lib` 카드의 **NMC–NMC A = 2.11 × 10⁻¹⁹ J** (그 카드 출처 Zhu 2011, 2 차 인용) 을 넣으면 **γ_NMC^LW ≈ 0.112 J/m² (112 mJ/m²)** · W_NMC–NMC^LW ≈ 0.22 J/m².  청정 DFT 벽개 (`garcia2017_nmc111_surface_energy_wulff_dft`, 0.76–2.27 J/m²) 의 1/7–1/20 수준 — 분산 성분 · 실온 표면이 결합 절단보다 훨씬 작다는 방향과 맞다 [추정].
- 같은 결합 규칙 (A₁₂ ≈ √(A₁₁A₂₂), l₀ 공통) 으로 lippke2023 카드의 **CB–NMC 9.5 × 10⁻¹⁹ J** 를 검사하면 기하평균 9.9 × 10⁻²⁰ J 의 **9.6 배** — 자릿수 오기 (×10⁻²⁰) 가능성 [추정 · 그 카드 원문 대조 필요].
- 황화물 Hamaker 상수는 정본 카드에 없다 (lippke2023 카드 §B-3) → LPSCl γ^LW [미확인].

### 7-4. ★ 측정 가능성 — 접촉각 틀을 황화물에 쓸 수 있나 [추정]
| 경로 | 이 논문 | NCM · LPSCl 에서 |
|---|---|---|
| 세 액체 접촉각 (식 41) | 무극성 고에너지 액체 1 + 극성 액체 2 (물 · glycerol) | ⛔ LPSCl 은 물 · 극성 양성자 용매와 반응 (H₂S) — 물 · glycerol 불가.  비양성자 · 무수 액체로 바꾸면 기준 γ⁺ · γ⁻ 값이 필요하고 용해 · 반응 여부 별도 확인 [미확인] |
| wicking (분말) | 분말 · 입자에 언급 | 글러브박스 · 무수 액체 조건이면 원리상 가능 [추정] — 같은 문제 (액체 선택) |
| 직접 힘 측정 | 표면력 장치 (헥사데실 −60 vs −67) | AFM 콜로이드 탐침 (begat2004 카드) — 건조 불활성 기체 · W 비를 직접 |
| Hamaker (분광) | Lifshitz 식 (10)–(14) | LPSCl · NCM 의 유전 함수 (UV · IR) 로 A 계산 → γ^LW (DFT 광학 계산으로도 가능) [추정] |
| 역기체크로마토그래피 | (이 논문에 없음) | 같은 묶음 IGC 리뷰 카드에서 다룬다 — 기체 탐침이라 액체 접촉 없음 |

### 7-5. 습식 ↔ 건식 (매질 효과)
- 매질 3 속 ΔF₁₃₂^LW 는 γ₃ 가 둘 사이면 **반발** (21–23) — 슬러리 용매 속에서 AM–SE (또는 AM–바인더) LW 상호작용이 뒤집힐 수 있다.  건식 혼합 (기체 매질 ≈ 진공) 에서는 LW 는 늘 인력 [인쇄 + 우리 산술].
- 정본 `johnson1971_jkr_surface_energy_contact_elastic_solids` 의 고무–고무: 물 속 W 가 건조의 1/10 — 같은 방향의 실측.

### 7-6. frame[5] — 어느 반쪽을 가졌나
- **가진 것**: 표면 에너지의 성분 분해 · 결합 규칙 · 측정식 — 우리 믹서 DEM 쌍별 점착 (D2) 의 **입력 물리**.
- **없는 것**: 입자 접촉 역학 (탄성 · 소성) · 분말 · 혼합 · 압밀 · 배터리 소재 값.

---

## 8. 적용 인사이트 (내 연구에 어떻게)
1. **기하평균은 γ^LW 에만** — 논지 §2-1 의 W_ij ≈ 2√(γ_iγ_j) 는 "γ = γ^LW (무극성)" 가정이다.  NCM (산화물) · LPSCl (황화물) 은 원문이 비대칭 (극성) 물질로 분류한다.
2. **ΔW = 2γ_AS** — 논지의 ΔW 를 "AM–SE 계면 장력의 두 배" 로 다시 쓰면, 산 · 염기 비대칭이 ΔW 를 음수로 만들 수 있음이 바로 보인다 (§7-1).
3. **D2 후보식** — W_ij = 2√(γ_i^LWγ_j^LW) + 2(√(γ_i⁺γ_j⁻) + √(γ_i⁻γ_j⁺)) → JKR 대응식으로 CED_ij.  현 덱의 min 혼합쌍 규칙은 이 식의 어느 경우와도 같지 않다 (begat2004 카드 §7-3).
4. **D4 · 측정에 필요한 것** — 총 γ 하나가 아니라 **γ^LW · γ⁺ · γ⁻ 셋** (두 소재 × 코팅 전후).  황화물은 액체 접촉각이 어렵다 → IGC (기체 탐침) · AFM · Lifshitz–DFT 경로.
5. **Hamaker ↔ γ^LW 1.88 × 10⁻¹⁸ m²** — 정본 카드의 Hamaker 값과 우리 γ 를 잇는 환산 상수 (±8 %).

## 9. 인용 가능 문장 (deck/paper용 — 표지 그대로)
- "The geometric-mean (Good–Girifalco–Fowkes) combining rule applies only to the Lifshitz–van der Waals component of surface tension; Lewis acid–base interactions are asymmetric and combine as 2(√(γ₁⁺γ₂⁻) + √(γ₁⁻γ₂⁺)) (van Oss, Chaudhury & Good, Chem. Rev. 1988)."
- "In that framework the interfacial tension, and hence the free energy difference between like and unlike contacts (ΔW = 2γ₁₂), can become negative when one material is the stronger electron acceptor and the other the stronger electron donor."
- "van Oss et al. classify oxides and sulfides among 'particularly asymmetrical' (predominantly electron-donor) materials."
- 국문: *"기하평균 결합 규칙은 무극성 (LW) 성분에만 성립한다 — 산화물 · 황화물처럼 산 · 염기 비대칭이 있는 표면에서는 같은 상끼리 붙는 쪽이 늘 유리하다는 결론 (ΔW ≥ 0) 이 성립하지 않을 수 있다 (van Oss 1988; 우리 산술)."*

## 10. 주의/한계 (over-claim 방지 · 원문 비판)
1. ★ **식 (54) 인쇄 결함**: "A_ii = γ_i^LW/32πl_eq²" — 차원이 맞지 않는다.  Table III 의 l_eq 열은 **A_ii = 32πl_eq²·γ_i^LW** 일 때만 재현된다 (물 1.452 Å = 표 1.45 · PTFE 1.410 = 1.41 · PMMA 1.330 = 1.33) [우리 산술].
2. ★ **Table III polystyrene γ^LW "8"**: 같은 행의 l_eq 1.31 · l₀ 1.51 Å 는 γ^LW **≈ 38 mJ/m²** 일 때만 나온다 (8 이면 2.86 · 3.30 Å) [우리 산술] — "38" 의 오식으로 보인다 [추정].  각주 d 의 "l₀ = 1.58 + 0.08 Å" 도 본문 (±0.08) 과 다르다.
3. **식 (28) · (29) 의 둘째 등식** "ΔF_d0^LW·Rd₀/12d" · "Rd₀/6d" 는 식 (25) 의 면적당 ΔF_d0 로는 차원이 맞지 않는다 (맞는 꼴은 ΔF_d0·πRd₀²/d · 2πRd₀²/d) [우리 산술] — 첫 등식 (−AR/12d · −AR/6d) 은 표준 Derjaguin 결과.
4. **본문 "eq 28a"** (p.934, "As a first approximation, eq 28a then becomes …(43b)") — 식 (43a) 를 가리키는 오기로 읽힌다.
5. **γ⁺ · γ⁻ 의 눈금은 가정 기준 (물 25.5/25.5)** — 다른 기준을 쓰는 문헌과 섞으면 절대값이 맞지 않는다.  비대칭 성분 비만 기준 무관.
6. **산화물 · 황화물 분류는 한 문장** — 측정값 · 인용 근거 (refs 34, 35 의 알코올 · 에테르 등) 가 무기 고체에 대해 무엇을 보였는지는 [미확인].
7. 리뷰의 응용 · 검증 사례는 **수용액 · 생체 고분자** 중심 — 건조 분말 점착 · 고체–고체 접촉 검증은 없다.
8. **결합 규칙 자체에 대한 논쟁** (산 · 염기 접근의 눈금 · 측정 재현성) 은 이 논문 이후 문헌의 몫 — 이 카드는 1988 원문 주장만 옮긴다.

## 11. 참고문헌 — 우리가 더 볼 것 (원문 목록 서지 그대로 + 이유)
| 번호 | 서지 (원문 목록 그대로) | 왜 |
|---|---|---|
| 10 | Fowkes, F. M. In Physicochemical Aspects of Polymer Surfaces; Mittal, K. L., Ed.; Plenum: New York, 1983; Vol. 2, p 583. | 극성 성분이 기하평균을 안 따른다는 Fowkes 의 지적 |
| 25 | Fowkes, F. M. In Surfaces and Interfaces; Burke, J. J., Ed.; Syracuse University Press: New York, 1967; Vol. 1, p 199. | Hamaker ↔ γ 비례 (53b) |
| 33 | van Oss, C. J.; Chaudhury, M. K.; Good, R. J. Adv. Colloid Interface Sci. 1987, 28, 35. | 단극성 · 기준값 |
| 34 | Chaudhury, M. K.; van Oss, C. J.; Good, R. J. J. Colloid Interface Sci., submitted. | 산화물 · 황화물 분류 근거 문헌 (계열) |
| 36 | Good, R. J.; Girifalco, L. A. J. Phys. Chem. 1960, 64, 561. | 기하평균 규칙 |
| 37 | Girifalco, L. A.; Good, R. J. J. Phys. Chem. 1957, 61, 904. | Φ 0.53–1.17 |
| 38 | Fowkes, F. M. J. Phys. Chem. 1962, 66, 382. | 성분 분해 |
| 49 | Israelachvili, J. N. Q. Rev. Biophys. 1974, 6, 341. | (14) · (53a) |
| 58 | Small, P. A. J. Appl. Chem. 1953, 3, 71. | (37) 의 선행 |
| 60 | Chaudhury, M. K. Thesis, SUNY/Buffalo, 1984. | Table I · III 계산 |
| 90 | Good, R. J. Colloid Surf. Sci. 1979, 11, 1–29. Good, R. J.; Neumann, A. W. Ibid. 1979, 11, 31–39. | 전진 · 후퇴 접촉각 · 이력 해석 |
| 91 | Ku, C. A.; Henry, J. D.; Siziwardane, R.; Roberts, L. J. Colloid Interface Sci. 1985, 106, 377. | ★ 분말 wicking 접촉각 — 분말 시료에 이 틀을 쓰는 경로 |
| 93 | Hough, D. B.; White, L. R. Adv. Colloid Interface Sci. 1980, 14, 3. | Hamaker 상수 계산 (Lifshitz) |
| 95 | Pashley, R. M.; McGuiggan, P. M.; Ninham, B. W.; Evans, D. F. Science (Washington, D.C.) 1985, 229, 1088. | 헥사데실 직접 힘 측정 (−60 mJ/m²) |

## 원문 대조 기록 (이 카드 작성 중 직접 확인한 것 · 2026-10-13)
- 15 쪽 전부를 쪽 이미지 (120 dpi 전쪽 + 300 dpi 확대) 로 읽었다 — OCR 텍스트층은 그리스 문자 · 위첨자 · 근호가 깨져 식은 이미지에서 옮겼다.  인용 문장은 이미지와 텍스트층을 대조.
- 그림 없음 (TOC · 본문에 그림 캡션 문자열 없음) · 표 3 · 식 크롭 13 (300 dpi = 원 스캔 해상도, 1-bit).  식 (54) · Table III polystyrene 행은 300 dpi 확대로 인쇄를 재확인했다.
- 정본 litdb 중복 확인: 파일 목록 + "cr00088a006" · 제목 낱말 `git grep` 0 건.

## 🔗 관련 카드
- 같은 묶음: `johnson1971_jkr_surface_energy_contact_elastic_solids` · `begat2004_cohesive_adhesive_balance_afm_colloid_probe` · `garcia2017_nmc111_surface_energy_wulff_dft`.
- Hamaker 값: `lippke2023_dem_drying_structure_formation_lib` · 점착 접촉: `dmt1975_adhesion_contact_deformation`.
- LPSCl 표면: `pustorino2025_lpscl_bulk_surface_mechanical_electronic_li_filament`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

# Halogen chemistry of solid electrolytes in all-solid-state batteries — He / Zhang / Xin* / Xu / Hu / Wu / Yang* / Tian* (Nature Reviews Chemistry 2023, 7, 826–842)

> slug `he2023_halogen_chemistry_solid_electrolytes` · DOI `10.1038/s41570-023-00541-7` · type **review (자체 계산 0 · 자체 실험 0 — 전 수치가 2차 인용)** · PDF `litdb/inbox/102._Halogen_chemistry_of_solid_electrolytes_in_allsolidstate_batteries.pdf` (본문 17 pp = 12 pp 본문 + refs 203) + SI `102._Sup_…pdf` (6 pp = Table S1 + SI refs 1–48) · digested `2026-09-09` · status ✅

> elements: Li P S F Cl Br I O Y Sc In Er Yb Ho Zr Hf Al Ca Si Ge Sn Mg Mn Cd Fe Zn Ag
> methods: dft, aimd, md, arrhenius, esw

> **저자·소속**: Bijiao He¹, Fang Zhang¹, **Yan Xin\***¹, Chao Xu¹, Xu Hu², Xin Wu³, **Yang Yang\***⁴⁻⁸, **Huajun Tian\***¹ — ¹華北電力大學(North China Electric Power Univ., Beijing) ²國家節能中心 ³中建三局 ⁴⁻⁸ Univ. of Central Florida. Published online **2023-10-13**.
> **태그: [외부·리뷰]** — 한양대 아님. **자체 DFT·실험 0건**(본문 전체에서 "DFT"·"first-principles"·"density functional" 는 **참고문헌 주석에만** 등장).

---

## 0. ⛔ 이 digest 를 쓰는 규율 — **리뷰는 2차 인용이다**

> **이 파일의 어떤 수치도 `db/properties/*` 에 직접 넣지 않는다.**
> 아래 모든 값은 **원 출처(ref 번호 + 저자·연도·저널)** 를 달아 뒀다. 우리가 실제로 인용할 때는
> **그 원 출처의 로컬 PDF 를 확보해 확인한 뒤**에 쓴다 (2026-07 Kim/Cui 교훈 — 링크만 보고 인용하다 물렸다).
>
> ⚠⚠ **번호 함정이 실재한다.** 본문 ref 번호(1–203)와 **SI ref 번호(1–48)는 완전히 다른 체계**다.
> 예: **본문 ref 18 = Peng 2023 리뷰**(Batteries & Supercaps) ↔ **SI ref 18 = Rao & Adams 2011**(Phys. Status Solidi A).
> 아래에서는 항상 `본문-ref N` / `SI-ref N` 로 구분해 적었다. **섞으면 잘못된 논문을 인용하게 된다.**
>
> `comparison_vs_ours.md` 의 **물성 4축(A/B/C/D) 표에 넣지 않는다** — 이 편은 값의 원전이 아니라
> **개관·방법·용어의 정본**이다. `🔧 방법/개관 원전` 블록에만 둔다.

### 이 리뷰가 **무엇의 정본인가** (우리가 왜 이걸 두는가)

> **우리 원고 서론에서 "왜 할로겐이고 왜 Cl 인가"를 3–5문장으로 세울 때, 그 문장들이 딛고 설
> field-map 이자 계보(1923→2021)의 정본이다.** 특히 **① argyrodite 4a/4d 자리 무질서 서사의
> 표준 서술**, **② Cl-과잉(Li₆₋ₓPS₅₋ₓCl₁₊ₓ)의 기전 도식(`Fig. 5a`)**, **③ 할로겐 조성별
> 실험 σ·Ea 47행 표(`Table S1`)** — 이 셋을 **한 곳에서 원 출처 번호와 함께** 주는 문헌이
> 우리 litdb 에 이것뿐이다. 반대로 **값의 근거로는 절대 인용하지 않는다.**

> 🎤 **관련 발표**: 없음 (2026-09-09 `litdb/talks/*.md` 인입 대기열 전수 검색 — 이 논문 행 없음).

---

## 1. 한 줄 요약

LiX(1923–1930) → Li₂MX₄ 스피넬 → **Li₃MX₆ 할라이드(2018 돌파)** → **LPSX 황화물 argyrodite/Li₇P₂S₈X** 로 이어지는
**할로겐 함유 고체전해질(HSE) 100년 계보**를 정리하고, 할로겐이 하는 일을 **(i) 큰 이온반경·약한 Li 쿨롱 결합 →
빠른 수송, (ii) 낮은 음전하(−1) → Li 공공 생성, (iii) 높은 표준 산화환원 전위 → 산화 안정** 세 축으로 환원한 뒤,
argyrodite 에서는 그것이 **"4a/4d 자리에 걸친 S²⁻/X⁻ 무질서 → inter-cage 점프 활성화"** 로 구현된다고 서술한
**개관 리뷰** — 자체 계산·실험은 하나도 없다.

---

## 2. 메타

| 항목 | 내용 |
|---|---|
| 저널/년 | ***Nature Reviews Chemistry* 7, 826–842 (December 2023)** · online 2023-10-13 |
| DOI | `10.1038/s41570-023-00541-7` |
| 다루는 계 | **Li–M–X 할라이드**(LiAlCl₄ · Li₂MX₄ · Li₃MX₆ · Li₂Sc₂/₃Cl₄) + **LPSX 황화물**(Li₆PS₅X argyrodite · Li₇P₂S₈X) |
| 연구유형 | **review** — 자체 계산 0 · 자체 실험 0 · 자체 합성 0 |
| 분량 | 본문 12 pp · Fig 7 · **표 0개(본문)** · refs **203** · SI 6 pp(**Table S1 = 47행**) + SI refs 48 |
| 자금 | NCEPU 학제간혁신 XM2212315 · NSFC 51821004 |

---

## 3. ★5 실험 σ·Ea 대표값 — `Table S1` **전문 이식** (전부 2차 인용)

> **원본은 SI 3 pp 에 걸친 47행 표다.** 좌표 기반으로 행 구조를 복원해 옮겼다(선형 텍스트 추출은
> 행이 밀려 잘못 붙는다 — 실제로 밀렸다). **`Ref.` 열은 SI 자체 번호(SI-ref)** 이고,
> 대응하는 **본문 ref 번호**를 우리가 병기했다.
> ⚠ **표에 조건이 거의 없다**: 압력·펠릿 밀도·전극·측정 주파수·시료 이력이 **한 칸도 없다.**
> 아래 값들을 서로 비교하는 것은 **같은 ref 안에서만** 의미가 있다.

### 3a. ★ **우리 계 — Li₆₋ₓPS₅₋ₓCl₁₊ₓ 계열** (Cl 단일 할로겐)

| x | 조성 | σ (S cm⁻¹) | Ea (eV) | 합성 | SI-ref → 본문-ref | 원 출처 |
|---|---|---|---|---|---|---|
| 0 | Li₆PS₅Cl | 1.9×10⁻³ | – | solid-phase | SI-18 → 116 | Rao & Adams, *Phys. Status Solidi A* **208**, 1804 (2011) |
| 0 | Li₆PS₅Cl | 7.4×10⁻⁴ | **0.11** | solid-phase | SI-19 → 131 | Rayavarapu et al., *J. Solid State Electrochem.* **16**, 1807 (2012) |
| 0 | Li₆PS₅Cl | 1.33×10⁻³ (298 K) | 0.33 | solid-phase | SI-20 → 117 | Boulineau et al., *Solid State Ion.* **221**, 1 (2012) |
| 0 | Li₆PS₅Cl | 1.62×10⁻³ (RT) | 0.296 | annealing | SI-21 → 170 | Yu C. et al., *Nano Energy* **69**, 104396 (2020) |
| 0 | Li₆PS₅Cl | 2.4×10⁻³ | – | solvent-engineered | SI-22 → 127 | Zhou L. et al., *ACS Energy Lett.* **4**, 265 (2019) |
| 0 | Li₆PS₅Cl | 1.1×10⁻³ (RT) | 0.16 | solid-phase | SI-23 → 171 | Rao et al., *Solid State Ion.* **230**, 72 (2013) |
| **0.25** | Li₅.₇₅PS₄.₇₅Cl₁.₂₅ | 3.0×10⁻³ | – | solvent-engineered | SI-22 → 127 | Zhou L. 2019 |
| **0.5** | Li₅.₅PS₄.₅Cl₁.₅ | **6.41×10⁻³** (RT) | **0.261** | annealing | SI-21 → 170 | Yu C. 2020 |
| **0.5** | Li₅.₅PS₄.₅Cl₁.₅ | 3.9×10⁻³ | – | solvent-engineered | SI-22 → 127 | Zhou L. 2019 |
| **0.5** | Li₅.₅PS₄.₅Cl₁.₅ (cold-pressed) | **9.4×10⁻³** (298 K) | 0.29 | solid-phase | SI-26 → **155** | **Adeli et al., *Angew. Chem. Int. Ed.* 58, 8681 (2019)** ← ✅ 우리 digest 있음 |
| **0.5** | Li₅.₅PS₄.₅Cl₁.₅ | **9.03×10⁻³** (RT) | 0.27 | solid-phase | SI-27 → 156 | Peng L. et al., *Chem. Eng. J.* **430**, 132896 (2022) |
| **0.5** | Li₅.₅PS₄.₅Cl₁.₅ (cold-pressed) | **1.02×10⁻²** (25 °C) | – | mech. alloying + rapid annealing | SI-28 → 157 | Jung W. D. et al., *Nano Lett.* **20**, 2303 (2020) |
| **0.7** | Li₅.₃PS₄.₃Cl₁.₇ | **~5×10⁻³** (25 °C) | – | solid-phase (**slow** heating) | SI-29 → 158 | Kitajima et al., *Mater. Today Commun.* **28**, 102727 (2021) |
| **0.7** | Li₅.₃PS₄.₃Cl₁.₇ | **~1.6×10⁻³** (25 °C) | – | solid-phase (**fast** heating) | SI-29 → 158 | Kitajima 2021 (같은 논문·같은 조성) |

> **★ 우리 modelc = Li₅.₄PS₄.₄Cl₁.₆ ⇒ x = 0.6.** 위 표에서 **x = 0.5 와 x = 0.7 사이**,
> 즉 **문헌이 가장 조밀하게 훑은 구간의 한복판**에 앉는다. 문헌 x=0.5 대의 상온 σ 는 3.9–10.2×10⁻³ S cm⁻¹,
> x=0.7 은 1.6–5×10⁻³ S cm⁻¹ 이다.
> ⛔ **이 숫자들을 우리 MLIP-MD σ 와 나란히 쓰지 않는다** (우리 규율: MLIP σ 절대값 인용 금지).

### 3b. Br·혼합 할로겐 (같은 계열, 비교용)

| 조성 | σ (S cm⁻¹) | Ea (eV) | 합성 | SI-ref → 본문-ref | 원 출처 |
|---|---|---|---|---|---|
| Li₆PS₅Br | 6.8×10⁻³ | – | solid-phase | SI-18 → 116 | Rao & Adams 2011 |
| Li₆PS₅Br | 7.2×10⁻⁴ | **0.17** | solid-phase | SI-19 → 131 | Rayavarapu 2012 |
| Li₆PS₅Br | 1.9×10⁻³ | – | solvent-engineered | SI-22 → 127 | Zhou L. 2019 |
| Li₆PS₅Br | 1.9×10⁻⁴ (RT) | – | ball-milling + liquid-phase | SI-24 → 126 | Yubuchi 2018 *ACS AEM* 1, 3622 |
| Li₆PS₅Br | 3.1×10⁻³ (25 °C) | – | multi-step liquid-phase | SI-25 → 125 | Yubuchi 2019 *JMCA* 7, 558 |
| **Li₅.₃PS₄.₃Br₁.₇** | **1.1×10⁻²** (25 °C) | **0.18** | annealing | SI-30 → **138** | **Wang P. et al., *Chem. Mater.* 32, 3833 (2020)** ← 1S3X 기전 원전 |
| Li₆PS₅Cl₀.₇₅Br₀.₂₅ | 3.2×10⁻³ | – | solvent-engineered | SI-22 → 127 | Zhou L. 2019 |
| Li₆PS₅Cl₀.₅Br₀.₅ | 3.9×10⁻³ | – | solvent-engineered | SI-22 → 127 | Zhou L. 2019 |
| Li₆PS₅Cl₀.₅Br₀.₅ | 3.63×10⁻³ (32 °C) | 0.31 | solid-phase | SI-33 → 160 | Wang H. 2019 *JPS* 412, 29 |
| Li₆PS₅Cl₀.₂₅Br₀.₇₅ | 3.4×10⁻³ | – | solvent-engineered | SI-22 → 127 | Zhou L. 2019 |
| Li₅.₆PS₄.₆Cl₁.₀Br₀.₄ | 9.16×10⁻³ (RT) | 0.25 | solid-phase | SI-31 → 163 | Subramanian 2022 *JPS* 520, 230849 |
| **Li₅.₃PS₄.₃ClBr₀.₇** | **2.4×10⁻²** (25 °C) | **0.155** | solid-phase | SI-32 → **164** | **Patel et al., *Chem. Mater.* 33, 1435 (2021)** — 리뷰가 "**to date 최고 argyrodite σ**"로 명시 |
| Li₆PS₅I | 2.2×10⁻⁴ | 0.26 | ball-milling | SI-18 → 116 | Rao & Adams 2011 |

### 3c. ★4 **이가원자가(aliovalent) 치환** — 이 리뷰의 답

| 조성 | 자리 | σ (S cm⁻¹) | Ea (eV) | SI-ref → 본문-ref | 원 출처 |
|---|---|---|---|---|---|
| **Li₅.₃₅Ca₀.₁PS₄.₅Cl₁.₅₅** | **Ca²⁺ → Li 자리** | **1.02×10⁻²** (RT) | 0.30 | SI-39 → **149** | **Adeli, Bazak, Huq, Goward, Nazar, *Chem. Mater.* 33, 146 (2021)** |
| Li₅.₄Al₀.₂PS₅Br | **Al³⁺ → Li 자리** | 2.4×10⁻³ (RT) | – | SI-38 → **133** | Zhang Z. et al., *J. Power Sources* **450**, 227601 (2020) |
| Li₆.₅₅P₀.₄₅Si₀.₅₅S₅I | **Si⁴⁺ → P 자리** | 1.1×10⁻³ (RT) | 0.19 | SI-37 → 150 | Zhang J. 2020 *ACS AMI* 12, 41538 |
| Li₆.₇P₀.₃Si₀.₇S₅I | Si⁴⁺ → P | 2.0×10⁻³ (RT) | – | SI-34 → 136 | Ohno 2019 *Chem. Mater.* 31, 4936 |
| Li₆.₃P₀.₇Sn₀.₃S₅I | Sn⁴⁺ → P | 1×10⁻⁴ (RT) | – | SI-34 → 136 | Ohno 2019 |
| Li₆.₆Ge₀.₆P₀.₄S₅I | Ge⁴⁺ → P | 5.4×10⁻³ (RT) | – | SI-35 → 134 | Kraft 2018 *JACS* 140, 16330 |

### 3d. 할라이드(Li–M–X) — 우리 계 아님, 맥락용 발췌

| 조성 | σ (S cm⁻¹) | Ea (eV) | SI-ref → 본문-ref | 원 출처 |
|---|---|---|---|---|
| Li₃YCl₆ / Li₃YBr₆ | 5.1×10⁻⁴ / 1.7×10⁻³ (RT) | 0.40 / 0.37 | SI-1 → 16 | Asano 2018 *Adv. Mater.* 30, 1803075 (**4 V급 돌파**) |
| Li₃ScCl₆ | 1.25×10⁻³ (RT) / **3.02×10⁻³** | 0.31 / **0.25** | SI-2 → 63 / SI-7 → 89 | Wang C. 2021 *Sci. Adv.* / Liang 2020 *JACS* |
| Li₃InCl₆ (water-mediated) | **2.04×10⁻³** (25 °C) | 0.347 | SI-5 → 62 | Li X. 2019 *Angew.* |
| Li₂Sc₂/₃Cl₄ | 1.5×10⁻³ (RT) | 0.34 | SI-16 → 80 | Zhou L. 2020 *EES* 13 |
| Li₂.₅Y₀.₅Zr₀.₅Cl₆ | 1.4×10⁻³ (25 °C) | 0.33 | SI-8 → 100 | Park K. 2020 *ACS Energy Lett.* (**Zr⁴⁺ aliovalent**) |
| **Li₃InCl₅.₆F₀.₄** | 1.37×10⁻³ (30 °C) | 0.28 | SI-11 → 111 | Chen X. 2022 *JPS* 545 |
| **Li₃InCl₄.₈F₁.₂** | **5.1×10⁻⁴** (RT) | – | SI-12 → 112 | Zhang S. 2021 *AEM* 11, 2100836 |
| Li₉.₅₄Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃ | 2.5×10⁻² (RT) | – | SI-36 (본문 미인용) | **Kato 2016 *Nat. Energy* 1, 16030** |

---

## 4. ★ DFT/계산 방법 — **없다. 그 사실이 이 절이다**

| 항목 | 이 논문 |
|---|---|
| code / functional / pseudo / k-points / ecut / supercell | **n/a — 자체 계산 0건** |
| DFT+U / AIMD / MLIP / 무질서 처리 | **n/a** |
| 자체 실험(합성·EIS·XRD·XPS) | **n/a — 0건** |
| 계산을 *인용*하는 곳 | ① 본문-ref **135 = de Klerk, Rosłoń & Wagemaker, *Chem. Mater.* 28, 7955 (2016)** — "DFT molecular dynamics" 로 명시(ref 주석). ② 본문-ref **140 = Kang & Han, *J. Phys. Chem. Lett.* 7, 2671 (2016)** — Li₇P₂S₈I 구조·σ "first-principles". ③ 본문-ref **165 = Fang & Jena, *Nat. Commun.* 13, 2078 (2022)** — Li₆.₂₅PS₅.₂₅(BH₄)₀.₇₅ σ **0.177 S cm⁻¹**, Ea **0.108 eV**(계산값). ④ 본문-ref **146 = Ong 2013 *EES* 6, 148** — δ-Li₃PS₄ σ 상한 4×10⁻³ 계산. ⑤ 본문-ref **138/162** — 1S3X 4d 배열 점프율. |
| Arrhenius 정의 | 본문에 **σ = σ₀ e^(−Ea/k_BT)** 를 명시적으로 씀(Summary and outlook) — 우리와 같은 형태 |

> ✅ **우리 litdb 가 이미 갖고 있는 원전**: ref 135 = `deklerk2016_diffusion_site_disorder_argyrodite` ·
> ref 132 = `kraft2017_lattice_polarizability_argyrodite_Li6PS5X` · ref 155 = `adeli2019_halide_substitution_boosting_argyrodite` ·
> ref 165 = `fang2022_argyrodite_transport_beyond_paddlewheel` · ref 116 = `rao2011_argyrodite_se_studies_bvse` ·
> ref 167 = `yun2023_deciphering_degradation_halide_vs_sulfide` · ref 194 = `taklu2021_cucl_dualdoping_air_stability_argyrodite`.
> ⇒ **리뷰의 핵심 주장 몇 개는 우리 1차 digest 로 직접 대조할 수 있었다** (§10 에 결과).

---

## 5. Figure set ★

> **크로핑 7장 + `Table S1` 1장 = 8장.** 자동 추출기가 **Fig 1·3·7 을 통째로 놓쳤고**
> **Fig 2·4·5 는 단(column) 경계에서 잘렸다** — 손으로 다시 잘랐다(§11 도구 버그 보고).

| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| 1 | **HSE 연표 1923→2021** + 각 계열 결정구조 썸네일 (LiAlCl₄ 1923 · LiX 이온전도 1930 · Li–LiI–AgI 박막전지 1969 · LiAlCl₄ σ 1977 · Li₂MCl₄ 1981 · Li₂ZnI₄ 올리빈 1989 · **Li₆PS₅X 2008** · Li₇P₂S₈I 2015 · **Li₃YBr₆/Li₃YCl₆ 4 V 2018** · Li₂Sc₂/₃Cl₄·LiₓScCl₃₊ₓ·Li₅.₄Al₀.₂PS₅Br·Li₃ErI₆ 2020 · 습식합성·Li 계면 2021) | **원고 서론 1문단의 뼈대 그대로.** "argyrodite 2008 / 할라이드 2018" 두 분기점만 인용해도 서론이 선다 |
| 2a | 할로겐 vs O²⁻·S²⁻ 4열 비교: **표준 산화환원 전위**(F 2.870 · Cl 1.358 · O 1.230 · Br 1.080 · I 0.536 · S **0.142**) / 전자배치 / **Pauling 전기음성도**(F 3.98 · O 3.44 · Cl 3.16 · Br 2.96 · I 2.66 · S 2.58) / **결정반경**(F 119 · O 126 · **Cl 167** · **S 170** · Br 182 · I 206 pm) | ★★★ **Cl⁻ 167 pm ≈ S²⁻ 170 pm (3 pm 차)** — 우리 comp1/modelc 의 **S/Cl 자리교환을 정당화하는 한 줄 숫자**. Br 은 12 pm, I 는 36 pm 차 → 무질서가 줄어드는 이유. **S 의 표준전위 0.142 V 가 Cl 1.358 V 의 1/10** → 우리 ESW "S²⁻-limited" 축과 같은 방향의 화학적 직관 |
| 2b | 할로겐의 전지 응용 지도(LIB/FIB/MIB/CIB/RFB/ASSB) — 우리 축 밖 | 인용 가치 낮음 |
| 3a–g | Li–M–X 계: 수용액/암모늄 습식합성 · Li₃MX₆ 결함화학 · LiAlCl₄ 단사 · Li₂MCl₄ 역스피넬 · Li₂Sc₂/₃Cl₄ 결손역스피넬 · **ccp(C2/m) Oct–Tet–Oct** vs **hcp(P-3m1/Pnma) Oct–Oct–Tet–Oct** 이동경로 | 우리 계 아님. **"음이온 부격자(ccp/hcp)가 이동경로를 결정한다"** 는 프레임만 가져올 것 |
| **4b** | ★ **Li₆PS₅X 결정학 범례**: **S/X (4a) · X/S (4d) · S (16e) · P (4b) · Li (24g, 48h)** + PS₄ 골격 + face-sharing **S₃X₂ 이중사면체**(Li1·Li2 포함) | ★★★ **자리 표기의 정본.** 이 리뷰는 free-anion 두 자리를 **4a / 4d** 로 부른다 — de Klerk 2016 의 **4c ≡ 이 리뷰의 4d**(케이지 중심). 우리 digest 매핑이 독립 확인됐다 |
| **4c** | ★ **케이지 그림**: Li₆PS₅Cl = 반점유 Li1 쌍 → **육각 국소경로** → **Cl 자리 둘레 pathway cage**(탈출구 ①②③④ 4개) / Li₆PS₅I = **Li1–Li2–Li1 삼중자리** → 아령형 국소경로 → **S 자리 둘레 cage** | ★★★ **"Cl 이 4d(케이지 중심)에 오면 케이지가 서로 연결된다"** 의 그림. 우리 comp2 disorder ensemble 의 물리 그림 그대로 |
| **4d** | ★ **점프 3종**: **doublet(48h–24g–48h)** · **intra-cage(48h–48h)** · **inter-cage(48h–48h)** | ★★★ de Klerk 3종 분해와 **같은 정의**. 우리 MSD/점프 분석 용어를 이 그림으로 고정 |
| 4e,f | δ-Li₃PS₄ · Li₄PS₄I 구조 | Li₇P₂S₈X 계 — 우리 축 밖 |
| **5a** | ★★ **Cl-과잉(excessive halogen doping) 기전 도식**: P(4b) 둘레 4개 4d 자리의 배열 → **1S3X(4d)** 가 최고 점프율 · 사슬 = **과잉 할로겐 → 음이온 무질서↑ → 4d 평균 음전하↓ → Li 재분포 → 24g 점유↑ → inter-cage 점프거리 단축 → 고속전도** | ★★★ **우리 modelc(Cl 1.6) 서사의 문헌 도식 그 자체.** "Cl↑ ⇒ 왜 빠른가"를 4단계로 쪼갠 유일한 그림. `Li₆PS₅X → Li₆₋ₓPS₅₋ₓX₁₊ₓ` 화살표에 **Li1(48h) → Li2(24g)** 전이가 명시 |
| **5b** | ★ **이중할로겐(dual-halogen) 기전 + 트레이드오프**: Li₆PS₅Cl(S3=4a, S1=4d) + Br⁻ 가 **두 자리 모두**로 → Li₆PS₅Cl₀.₂₅Br₀.₇₅, **D_Li–S = 2.3 Å** 표기. 사슬 = 반경↑→격자부피↑→Li–S 거리↑→Li 재분포→고속(녹색) / **분극률↑ → Ea↓(녹색) 그러나 σ₀↓(빨강 "Adverse effect")** / **음이온 무질서↓(빨강)** | ★★ **"Ea 만 보면 속는다"** 를 리뷰가 그림으로 인정한 자리. 우리 Arrhenius 해석(Ea 와 σ₀ 를 분리해 보라)의 문헌 근거 |
| 5c | Li₇P₂S₈I 부분결정상: Phase I Li₄PS₄I(저전도) ↔ Phase II δ-Li₃PS₄(고전도), 이중할로겐이 **비정질 기지를 δ-Li₃PS₄ → Li₄PS₄X 로 바꿔** 결정상을 δ-Li₃PS₄ 로 만든다 | 우리 축 밖(비정질 계). "상 분포가 σ 를 지배" 프레임만 |
| **6** | 셀 성능 산점도 — **비용량(mAh g⁻¹, 100–240) vs rate(C, 0–0.25)**, 14개 셀. 최고점 `figure-read ≈` **235 @ 0.1 C = TiS₂–Li₅.₄Al₀.₂PS₅Br–Li**(ref 133); Cl-rich 계는 NMC622–Li₅.₅PS₄.₅Cl₁.₅–Li-In `≈158 @ 0.05 C`(ref 156), LiCoO₂@LiNbO₃–Li₅.₅PS₄.₅Cl₁.₅–Li-In `≈150 @ 0.1 C / ≈110 @ 0.2 C`(ref 157) | ⚠ **인용 금지 수준.** 양극(LiCoO₂/NMC622/NMC811/TiS₂/LTO)·음극(Li/Li-In/In)·로딩·온도가 전부 다른데 한 축에 얹었다 — **전해질 순위를 말할 수 없는 그림**. §10 참조 |
| **7a,b** | 양극 쪽: SE 코팅 입자(점접촉 → 넓은 접촉면 → CEI) / 복합양극(CAM–도전재–HSE 삼중 접촉) | 우리 계면 슬랩 논의의 도식 배경 |
| **7c** | ★ Li₃MX₆ + Li: **`Li₃MX₆ + 3Li → 6LiX + M⁰`** → **혼합전도 계면(Li⁺·e⁻ 둘 다 통과, 그림에 차단 표시 없음)** → 급속 성장 | ★ 할라이드가 Li 금속에 못 쓰이는 이유의 정본 도식 |
| **7d** | ★★ Li₆PS₅X + Li: **Li₆PS₅Cl → Li₁₁PS₅Cl → {Li₂S, LiCl, S} → {Li₃P, LiCl, Li₂S}** 다단 분해 → **Li⁺-전도 계면(e⁻ 화살표에 빨간 ✗ = 전자 차단)** | ★★★ **우리 grand-potential 환원측(1.242 V)·SEI 서사의 그림 대응.** 7c 와 7d 를 나란히 놓은 것이 이 리뷰의 최고 산출물 |
| **7e** | Li–M–X SE + **LPSX 형 SE 를 얇은 버퍼층**으로 → Li 금속 | 이종 SE 적층 설계의 표준 그림 |
| **7f** | Li₆PS₅Cl/Li 계면: **공극 형성 → 국소전류 증가 → 덴드라이트 → 젖음성 개선으로 완화** | 우리 계면 축(E)의 정성 도식 |
| **Table S1** | 47행 σ·Ea·합성법 (§3 에 전문 이식) | ★★★ **이 리뷰의 실질적 산출물.** 본문이 아니라 **SI 에 있다** |

---

## 6. Post-processing ★

**없다.** BVSE·NEB·Bader·COHP/ICOHP·DOS/PDOS·ELF·grand-potential·탄성·phonon **전부 0건**.
도구(pymatgen·VESTA·LOBSTER·VASP) 언급 0회. 이 리뷰는 **후처리를 인용만 한다** —
그중 우리가 재현 가능한 것은 de Klerk 2016(AIMD 점프율 분해)뿐이고, 그 원전은 이미 우리 digest 에 있다.

---

## 7. ★1 **할로겐 자리 점유(site occupancy) — 이 리뷰의 정본 정리**

### 7a. 자리 정의 (⚠ 표기 함정 먼저)

| 자리 | Wyckoff | 이 리뷰의 라벨 | 무엇이 앉나 |
|---|---|---|---|
| PS₄³⁻ 의 P | **4b** | `P (4b)` | P |
| PS₄³⁻ 의 S | **16e** | `S (16e)` · Fig 5 에서는 `S2 (16e)` | S (불가침 — 할로겐이 여기 안 옴) |
| free-anion #1 | **4a** | `S/X (4a)` · Fig 5 에서는 `S3 (4a)` | S²⁻ 또는 X⁻ |
| free-anion #2 (**케이지 중심**) | **4d** | `X/S (4d)` · Fig 5 에서는 `S1 (4d)` | X⁻ 또는 S²⁻ |
| Li | **24g / 48h** | `Li (24g, 48h)` | Li2 = 24g(삼각면 중심, 전이상태) · Li1 = 48h(24g 위·아래 쌍) |

> ⚠⚠ **표기 대조표 (인용 전 반드시 확인)**
> · **이 리뷰의 4d ≡ de Klerk 2016 의 4c ≡ 케이지 중심 ≡ Kraft 2017 의 "site disorder" 가 측정하는 자리.**
> · F-43m 원점 선택 차이일 뿐 물리는 하나다. **"4c" 와 "4d" 를 같은 문장에 섞어 쓰지 말 것.**
> · 우리 `deklerk2016_…` digest §머리의 매핑 주석과 **이 리뷰가 독립적으로 일치**한다
>   (`Fig. 4c`: LPSCl = "pathway cage **around Cl** position" / LPSI = "pathway cage **around S** position").

### 7b. 어느 할로겐이 얼마나 무질서한가 — **원 출처와 함께**

| 할로겐 | 결정반경 (`Fig. 2a`) | S²⁻(170 pm) 와의 차 | 4a/4d 무질서 | 리뷰 서술 | 원 출처 |
|---|---|---|---|---|---|
| **Cl⁻** | **167 pm** | **−3 pm** | **있다(강함)** | "Cl and Br have similar ionic radii to S, resulting in **the disorder of X⁻ and S²⁻ at the 4a and 4d sites**" | 본문-ref 115 (Deiseroth 2008) · 131 (Rayavarapu 2012) |
| **Br⁻** | 182 pm | +12 pm | 있다 | 위와 동일 문장 | 동일 |
| **I⁻** | 206 pm | +36 pm | **없다(질서)** | "**there is no anionic site disorder in Li₆PS₅I**, in which I and S are **orderly located in 4a and 4d sites**, respectively" | 본문-ref 115, 131 |

**⇒ 리뷰가 명시한 인과**: 반경 차 → 무질서 여부 → 케이지 연결 여부 → σ.
본문(p832)은 Li₆PS₅Cl·Br 를 10⁻²–10⁻³ S cm⁻¹, Li₆PS₅I 를 **"only about 10⁻⁶ S cm⁻¹"** 이라 쓰면서
"결정구조는 비슷하다"고 대비시킨다(본문-ref 115).
그리고 리뷰는 **"할로겐이 도입하는 Li 공공의 정도로는 이 수 자릿수 차이를 설명 못 한다 — 원자 점유(atomic occupancy)에서 더 파고들어야 한다"** 고 못박는다. (원문: *"The degree to which the three halogen anions introduce Li vacancies does not account for the several-orders-of-magnitude difference … which should be further explored from the atomic occupancy."*)

> 🔴🔴 **그런데 그 10⁻⁶ 이 자기 SI 와 220배 어긋난다.**
> **본문 p832: Li₆PS₅I ≈ 10⁻⁶ S cm⁻¹** ↔ **`Table S1`(SI-ref 18, Rao & Adams 2011): Li₆PS₅I = 2.2×10⁻⁴ S cm⁻¹, Ea 0.26 eV.**
> 같은 논문 안에서 **같은 물질의 σ 가 220× 차이**나고, 하필 **argyrodite 절의 핵심 논증
> ("several-orders-of-magnitude difference")이 그 10⁻⁶ 위에 서 있다.**
> (본문의 "Cl·Br 10⁻²–10⁻³" 도 자기 표의 Li₆PS₅Cl 7.4×10⁻⁴ 를 벗어난다.)
> ⇒ **"Li₆PS₅I 는 10⁻⁶ 이라 수 자릿수 느리다" 를 이 리뷰로 인용하면 안 된다.**
> 안전한 서술은 **`Table S1` 기준 "Cl/Br 대비 I 는 한 자릿수 이상 낮다"**(2.2×10⁻⁴ vs 1.9–6.8×10⁻³)까지다.
> ✅ 참고: 우리 `deklerk2016` digest 는 이 차이의 **기전**(all-4a → inter-cage 0)을 갖고 있으므로,
> **기전은 de Klerk 로, 값은 원 실험 논문으로** 나눠 인용하면 이 함정을 피한다.

### 7c. 자리 분포가 점프 종류를 켜고 끈다 (★ 우리 disorder ensemble 의 문헌 근거)

리뷰는 먼저 점프를 3종으로 정의한다 (`Fig. 4d`) — **doublet(48h–24g–48h) · intra-cage(48h–48h) · inter-cage(48h–48h)**,
그리고 *"this jump process(inter-cage) has been revealed to dominate the macroscopic long-range ion transport"* 라고
**율속을 inter-cage 로 지목**한다(본문-refs 132–134). 그 다음에:

리뷰 본문 (p834, 본문-ref **135 = de Klerk 2016** 인용):

> "Theoretical models have shown that **no inter-cage jumps occur in Li₆PS₅Cl when all Cl anions are located in the 4a sites**, and **a drastic decrease in the doublet jump rate occurs when all Cl⁻ are placed at the 4d sites**. **The highest ionic conductivity can be obtained in an optimal Cl distribution of 1:3 over 4a and 4d sites**."

**✅ 우리 1차 digest 로 검증했다** (`deklerk2016_diffusion_site_disorder_argyrodite.md`):
- all-4a → intercage 점프 **0** (전 온도) ✓ 리뷰 서술과 일치
- all-4c(=4d) → doublet 점프율 26.11 → **0.21**×10¹⁰ s⁻¹ 로 급락 ✓ 일치
- 4a:4c = 1:3 (= 4c-Cl 75 %) 에서 limiting jump rate **1.99×**, σ_J **2.00×** ✓ 일치
⇒ **리뷰는 de Klerk 를 정확히 옮겼다.** 다만 **그 후 반박이 있다는 사실은 안 적었다** — §10 참조.

그리고 리뷰는 여기에 실무 한 줄을 더한다:

> "During synthesis, **the annealing temperature is closely related to the sample composition and structure and may be a factor affecting the halogen distribution**" (본문-ref **139** = Yu C. 2019 *JMCA* 7, 10412).

⇒ **무질서는 조성이 아니라 열이력으로도 움직인다.** (그 정량적 증거가 `Table S1` SI-ref 29 에 있다 — §8c.)

---

## 8. ★2 **할로겐 과잉(Cl-rich, x > 1) 이 무엇을 바꾸는가**

### 8a. 리뷰가 서술한 기전 사슬 (`Fig. 5a` + p834 본문)

```
과잉 할로겐 도핑 (Li₆PS₅X → Li₆₋ₓPS₅₋ₓX₁₊ₓ)
  → 4d 자리를 X 가 더 많이 차지 (S 치환 ↓)
  → 5가지 P 국소환경 {4S, 3S1X, 2S2X, 1S3X, 4X} 중 **1S3X 가 최고 점프율**   [본문-ref 138, 162]
  → 4d 음이온 중심의 **평균 음전하 ↓**
  → Li 케이지에 **공공 ↑**, Li 가 **24g(전이상태 자리) 점유 ↑**
  → 활성 전이상태의 **수명(lifetime) ↑**                                    [본문-ref 132]
  → **inter-cage 점프 거리 단축 → 장거리 수송 ↑**
```

> ★ 리뷰의 결정적 단서 (원문): *"These series of events indicate that the mixing of S²⁻ and X⁻ **strongly regulates the energy factor, which is not caused by Li deficiency**"* (본문-ref **162 = Feng X. et al., *Energy Storage Mater.* 30, 67 (2020)**, 제목이 바로 `Enhanced ion conduction by enforcing structural disorder in Li-deficient argyrodites Li₆₋ₓPS₅₋ₓCl₁₊ₓ`).
>
> ⇒ **"Cl-rich 가 빠른 것은 Li 공공이 늘어서가 아니라 에너지 지형(무질서)이 평탄해져서"** 라는 것이
> 이 리뷰의 공식 입장이다. **우리 modelc 서사를 "vacancy 증가" 로만 쓰면 문헌과 어긋난다.**

### 8b. 용해도 한계 — 리뷰가 유일하게 준 상한

> "For Li₆PS₅X-type SEs, **tuning the concentration of anions does not produce an unwanted heterophase within the allowable range of halogen ion solubility. Only when the concentration of halogens exceeds the maximum solubility can the ionic conductivity be reduced by the superfluous LiX.**"

⚠ **그 "maximum solubility" 의 수치는 안 준다.** (x 상한 미기재 — §12 gap 목록에 넣음.)
대비: Li₇P₂S₈X 계는 "LiX 도핑량에 강하게 의존하므로 **과잉 할로겐 전략을 쓸 수 없다**" 고 명시.

### 8c. ★ **조성 효과 vs 공정 효과 — 같은 표 안에서 갈린다**

| 비교 | σ 변화 | 무엇이 변수인가 |
|---|---|---|
| Yu 2020 (SI-21) x=0 → 0.5 | 1.62 → **6.41**×10⁻³ (**3.96×**), Ea 0.296 → **0.261** | **조성 (Cl 1.0→1.5)** — 같은 논문·같은 합성 |
| Zhou 2019 (SI-22) x=0 → 0.25 → 0.5 | 2.4 → 3.0 → **3.9**×10⁻³ (**1.63×**) | **조성** — 같은 논문·같은 합성 |
| **Kitajima 2021 (SI-29)** x=0.7 고정 | **~5×10⁻³ (느린 승온) vs ~1.6×10⁻³ (빠른 승온) = 3.1×** | **공정(승온속도)만** — 조성 동일! |
| Li₆PS₅Cl 문헌 산포 (SI-18/19/20/21/22/23) | 7.4×10⁻⁴ ~ 2.4×10⁻³ = **3.2×**, Ea **0.11 ~ 0.33 eV = 3.0×** | 논문 간 |

> 🔴 **이 표가 이 digest 에서 가장 중요한 경고다.**
> **Cl 1.0 → 1.5 의 조성 효과(≈4×)와, 같은 조성에서 승온속도만 바꾼 효과(≈3.1×)가 같은 크기다.**
> 그리고 **Li₆PS₅Cl 하나의 Ea 문헌 산포(0.11–0.33 eV)가 Cl-rich 로 얻는 ΔEa(≈0.035 eV)의 6배**다.
> ⇒ **"Cl-rich 가 σ 를 몇 배 올린다"는 문장은 반드시 "같은 논문 안에서" 라는 단서를 달아야 한다.**
> 우리 원고에서 modelc 의 이득을 말할 때 이 단서를 빠뜨리면 리뷰어가 정확히 이 표로 찌른다.

### 8d. ★ **우리 modelc(x = 0.6)가 이 계열 어디에 앉나**

```
x:      0        0.25      0.5              0.6          0.7
       ├────────┼─────────┼────────────────┼[modelc]────┼──────────►
문헌:  0.74–2.4  3.0       3.9–10.2         (없음)       1.6–5.0     ×10⁻³ S/cm
        (6편)    (1편)     (5편)                          (1편, 2점)
```
- **modelc 는 문헌이 조밀한 x=0.5 와, 데이터가 딱 1편뿐인 x=0.7 사이의 빈칸**에 있다.
- x=0.5 → 0.7 에서 문헌 σ 가 **꺾인다**(10.2 → 5.0×10⁻³, 다른 논문끼리라 결정적이진 않다).
  de Klerk 가 예고한 **"all-4d 가 되면 doublet 이 죽는다"** 의 실험 대응일 가능성 —
  ⇒ **우리 modelc 는 "아직 꺾이기 전인가, 꺾인 뒤인가" 를 계산으로 말할 수 있는 자리에 있다.** 강점.
- ⚠ 그러나 x=0.7 데이터가 **단 1편(Kitajima)**, 그것도 **승온속도로 3배가 흔들리는** 데이터다.
  **"x>0.5 에서 σ 가 꺾인다"를 이 표로 주장하면 안 된다.**

---

## 9. ★3 **산화·수분 안정성 축 — 할로겐 조성이 무엇을 바꾸나**

### 9a. 산화(oxidation) — 리뷰의 서술은 **정성적이고, 스스로 단서를 단다**

| 리뷰가 한 말 | 원문 위치 / 원 출처 | 우리 판정 |
|---|---|---|
| 할로겐 음이온(특히 F⁻·Cl⁻)은 **표준 산화환원 전위가 높다 → HSE 는 산화 안정성이 유리** | 서론, 본문-ref **23**(Yu T. 2021 *AEM* 11, 2101915), **24**(Kwak 2021 *AEM* 11, 2003190) + `Fig. 2a` | 화학적 직관 수준. **onset 수치 0개** |
| Li₂S–P₂S₅ 를 LiX 로 도핑하면 **ESW 가 넓어진다** | p832 | ⚠ **비교쌍이 "LPS(무할로겐) vs LPSX"** 다 — **argyrodite 내부의 Cl 1.0 vs 1.6 이 아니다** |
| **그러나** 계면 부반응으로 저항이 늘어 "**넓어진 ESW 가 고전압 양극과 맞지 않는다**" | p836, 본문-ref **167 = Yun 2023 *ESM* 59, 102787** ← ✅ 우리 digest 있음 | ★ **리뷰가 스스로 ESW 확장 주장을 되돌린 문장.** 우리 §B(4축 분리) 규율과 같은 방향 |
| Li₃MX₆ 는 "**할로겐이 유일한 음이온 + 강한 전기음성도 → 높은 전기화학 안정성**" | p836 | 우리 계 아님 |
| F 도핑 Li₃InCl₆: **in-situ F-rich CEI 로 실용 산화한계 >6 V** | 본문-ref **111 = Zhang S. 2021 *AEM* 11, 2100836** | 우리 계 아님. **"F 는 계면에서 이득"** 프레임만 |

> 🔴 **리뷰에 산화 onset 전압 수치가 단 하나도 없다.** ESW/분해전압/grand-potential 값 **0건**.
> ⇒ **이 리뷰를 산화안정성 *값*의 근거로 인용할 수 없다.** 프레임 문장에만 쓴다.

### 9b. 수분·공기 — **리뷰의 최대 공백**

| 계 | 리뷰가 준 것 | 원 출처 |
|---|---|---|
| Li₃Y₁₋ₓInₓCl₆ | In 함량↑ → **습도 내성↑** (수화 시 LiCl·H₂O + YCl₃·6H₂O 로 분해되지 않고 `Li₃Y₁₋ₓInₓCl₆·xH₂O` 중간체 형성) | 본문-ref **25** = Li X. 2020 *Nano Lett.* 20, 4384 |
| **Li₃InCl₄.₈F₁.₂** | **"Li–F 결합이 생겨 이온전도는 내려가지만(σ 1.37×10⁻³ → 5.1×10⁻⁴), 강직한 구조가 수분으로부터 보호된다"** | 본문-ref **112** = Chen X. 2022 *JPS* 545, 231939 |
| **Li₅.₅(P₀.₉Sn₀.₁)(S₄.₂O₀.₂)Cl₁.₆** | "**Sn·O 이중치환 → 수분 안정성 향상**" — **σ 값 없음** | 본문-ref **154 = Li G. et al., *Adv. Funct. Mater.* 33, 2211805 (2022)** |
| LiX 일반 | "LiX 는 **수분에 극도로 민감**, 비가역 열화 + 가역 수화물 + 비가역 부산물" | 본문-ref 202 |
| argyrodite 공기 안정성 | **H₂S 발생량·노출시간·RH 데이터 0건** | — |

> ★★★ **본문-ref 154 는 우리가 지금 당장 확보해야 할 논문이다.**
> `Li₅.₅(P₀.₉Sn₀.₁)(S₄.₂O₀.₂)Cl₁.₆` — **Cl 1.6 = 우리 modelc 와 정확히 같은 Cl 함량**에
> **O 를 넣은 계 = 우리 LPSOCl 축**. 제목이 곧 우리 조합이다:
> *"Sn–O dual-substituted **chlorine-rich** argyrodite electrolyte with enhanced **moisture and electrochemical stability**"*.

### 9c. ⚠ **Wang 2025 (O 도핑 σ 단조감소) 와의 대조 — 요청 ★3**

| 축 | `wang2025_pretrained_deep_potential_sulfide_sse` (`Fig. S11`) | **이 리뷰 (He 2023)** | 판정 |
|---|---|---|---|
| O 도핑 → σ | Li₅.₅PS₄.₅₋ₓOₓCl₁.₅, x 0→0.30 에서 **단조 감소 −41 %**(계산) / x 0→0.25 −37 %(실험) | **σ 를 아예 보고하지 않는다** (본문-ref 154 를 "수분 안정성 향상" 으로만 인용) | **⚠ 상충 아님 — 침묵이다.** 리뷰는 이 트레이드오프를 **확인도 반박도 하지 않는다** |
| 트레이드오프 존재 여부 | 캡션이 명시("moisture stability critical to industrial application") | **같은 모양의 트레이드오프를 다른 계에서 명시**: **F@Li₃InCl₆ → σ↓ + 수분보호↑** (본문-ref 112) | **✅ 방향 일치 — 다른 화학에서의 독립 사례** |
| 우리 결론 | — | — | **"작은 전기음성 음이온(O, F)을 넣으면 결합이 강해져 σ 를 잃고 안정성을 산다" 는 패턴이 O(황화물)·F(할라이드) 양쪽에서 관측된다.** 리뷰가 F 쪽 사례를 준 것이 Wang 2025 의 O 쪽 결과에 **간접 지지**가 된다 |

> ⇒ **우리 LPSOCl/+B₂O₃ 를 "개선"이라 쓸 때 축을 명시하라**는 규율은 **이 리뷰로도 유지된다.**
> 다만 **이 리뷰를 그 트레이드오프의 근거로 인용할 수는 없다** (argyrodite O 도핑의 σ 값이 없다).
> 근거로 쓸 것은 **본문-ref 154(Li G. 2022 AFM)** 와 **Wang 2025 `Fig. S11`** 이다.

---

## 10. ★4 **이가원자가(aliovalent) 도핑 — 이 리뷰는 어느 쪽인가**

### 🔴 결론: **이 리뷰는 "aliovalent 도핑이 σ 를 *올린다*" 쪽이다.** 명시적으로.

리뷰 본문 (p834, `Halogen-atomic substitution chemistry` 절 첫 문장):

> "**Aliovalent substitution of cations on the Li site¹³³,¹⁴⁹ or P site¹³⁴,¹³⁶,¹⁵⁰⁻¹⁵³ is often used to generate Li vacancies and increase the number of charge carriers.**"

그리고 Li–M–X 쪽에서도 같은 방향:

> "Irrespective of the equivalent-ion or aliovalent-ion substitution on the M sites, the induced structural conversion will alter the migration pathways … so that **a lower migration energy barrier is provided to achieve more rapid ion conduction**." (Zr⁴⁺ → Li₃MCl₆, 본문-ref 96·100·101)

### 자리·전하보상·수치 (원 출처와 함께)

| 도펀트 | 자리 | 전하보상 | σ (S cm⁻¹) | Ea (eV) | 원 출처 |
|---|---|---|---|---|---|
| **Ca²⁺** | **Li⁺ 자리** (Li₅.₃₅**Ca₀.₁**PS₄.₅Cl₁.₅₅) | Ca²⁺ 1개당 Li 공공 1개 | **1.02×10⁻²** (RT) | 0.30 | 본문-ref **149** = Adeli, Bazak, Huq, Goward, **Nazar**, *Chem. Mater.* **33**, 146 (2021) |
| **Al³⁺** | **Li⁺ 자리** (Li₅.₄**Al₀.₂**PS₅Br) | Al³⁺ 1개당 Li 공공 2개 | 2.4×10⁻³ (RT) | – | 본문-ref **133** = Zhang Z. 2020 *JPS* 450, 227601 |
| **Si⁴⁺** | **P⁵⁺ 자리** (Li₆.₅₅P₀.₄₅**Si₀.₅₅**S₅I) | **Li 가 늘어난다**(Li₆₊ₓ) | 1.1×10⁻³ | 0.19 | 본문-ref 150 = Zhang J. 2020 |
| **Ge⁴⁺** | P⁵⁺ 자리 (Li₆.₆**Ge₀.₆**P₀.₄S₅I) | Li 증가 | 5.4×10⁻³ | – | 본문-ref 134 = Kraft 2018 *JACS* |
| **Zr⁴⁺** | M³⁺ 자리 (Li₂.₅Y₀.₅**Zr₀.₅**Cl₆ 등) | Li 감소(Li₃₋ₓ) + 사면체 간극 생성 | 1.1–1.5×10⁻³ | 0.26–0.33 | 본문-ref 96·100·101 |
| **F⁻** | Cl⁻ 자리 (Li₃InCl₄.₈**F₁.₂**) | 등가 | **5.1×10⁻⁴ ← 감소** | – | 본문-ref 112 |
| **M²⁺ (Mg/Ca/Sr/Ba)** | In³⁺ 자리 (Li₃₋₂ₓMₓInBr₆) | 공공 생성 | **"ineffective"** | – | 본문-ref 104–107 |

### ⚠ 세 가지 정직한 단서 (우리가 붙인 것 — 리뷰는 안 붙였다)

1. **Ca 사례는 Cl-과잉과 교락(confounded)돼 있다.** `Li₅.₃₅Ca₀.₁PS₄.₅Cl₁.₅₅` 은 **Cl 1.55** 다.
   1.02×10⁻² 를 순수 Cl-rich `Li₅.₅PS₄.₅Cl₁.₅`(9.03–10.2×10⁻³) 와 비교하면 **차이가 사실상 없다.**
   ⇒ **이 표만으로는 "Ca 가 σ 를 올렸다"고 말할 수 없다.** Adeli 2021 원문의 자기 대조군이 필요하다.
2. **교락이 없는 증거는 I-쪽(P 자리)에 있다**: Li₆PS₅I 2.2×10⁻⁴ → Si 도핑 1.1–2.0×10⁻³ (**5–9×**),
   Ge 도핑 5.4×10⁻³ (**~25×**). ⇒ **P 자리 aliovalent 는 확실히 σ 를 올린다.**
3. 🔴 **리뷰의 문장 자체에 물리적 오류가 있다.** *"aliovalent substitution on the Li site **or P site** …
   to **generate Li vacancies** and increase the number of charge carriers"* — **P 자리 치환(Si⁴⁺/Ge⁴⁺→P⁵⁺)은
   Li 를 *늘린다*(Li₆₊ₓP₁₋ₓMₓS₅I). 공공을 만드는 게 아니라 채운다.** 두 자리를 한 문장에 묶으면서
   기전을 뭉갰다. (우리 `li2024_inf3_argyrodite_ultrathin_film.md` §14-⑱ 에서 **같은 오류**를 잡은 적 있다 —
   In³⁺→P⁵⁺ 를 "carrier↑ + vacancy↑ 동시" 로 쓴 사례. **분야 공통의 헐거운 문장이다.**)

### ⇒ **Liang 2026 스니펫과의 대질 (요청 ★4)**

| | 주장 | 이 리뷰의 대응 |
|---|---|---|
| **Liang 2026 (다른 리뷰)** | *"aliovalent doping 이 pristine Li₆PS₅Cl 대비 σ 를 낮춘다"* | ❌ **He 2023 은 정반대로 쓴다.** 본문 p834 첫 문장이 "generate Li vacancies and increase the number of charge carriers" 이고, `Table S1` 의 aliovalent 행들이 전부 pristine 이상이다 |
| **다만 He 2023 도 실패 사례를 안다** | — | ✅ **Li₃InBr₆ 계**: *"the vacancies brought by the aliovalent-ion substitution in Li₃InBr₆ are **ineffective**, and the distortion of the crystal lattice appears to **prevent the fast diffusion**"* (본문-ref 104–107). **단, 이건 할라이드지 argyrodite 가 아니다** |
| **σ 를 확실히 낮추는 치환은?** | — | ✅ **F⁻ → Cl⁻ (Li₃InCl₆)**: 1.37×10⁻³ → 5.1×10⁻⁴. **이건 등가(isovalent) 치환이지 aliovalent 가 아니다** |

> 🔴 **두 리뷰가 갈린다 — 그 자체가 소득이다.**
> **He 2023(Nat. Rev. Chem., 249회 인용) 은 argyrodite aliovalent 도핑을 σ 상승 전략으로 분류한다.**
> Liang 2026 이 그 반대를 말한다면, **어느 쪽도 1차 데이터가 아니므로 둘 다 인용하면 안 되고**,
> **원전 두 편(Adeli 2021 *Chem. Mater.* 33, 146 · Zhang Z. 2020 *JPS* 450, 227601)을 우리가 직접 확인해야 한다.**
> ⇒ 우리 **도펀트 cascade 의 site-rule 판정**(M³⁺ = Li_24g)에 직접 걸리는 문제다. §14 획득목록 1순위.

---

## 11. ★6 **계면(Li 금속·양극) 상용성 — 할로겐 관점**

### 11a. 리뷰의 핵심 이분법 (`Fig. 6` 하단 + `Fig. 7c` vs `Fig. 7d`)

| | **Li₃MX₆ (할라이드)** | **Li₆PS₅X (LPSX 황화물)** |
|---|---|---|
| **양극 쪽** | ✅ **좋다** — LiCoO₂ 등 고전압 양극과 직접(코팅 없이) 조합 가능, 넓은 ESW 확인 (본문-ref 16) | ⚠ **부족** — 확장된 ESW 도 고전압 양극에 못 미친다 → **LiNbO₃ 산화물 코팅 필요** (본문-ref 167·168·169) |
| **Li 금속 쪽** | ❌ **나쁘다** — `Li₃MX₆ + 3Li → 6LiX + M⁰`. **M³⁺ 환원 → Li₃M 합금 → 혼합 Li⁺/e⁻ 전도 계면 → 산화환원층이 멈추지 않고 자라 단락** (본문-ref 88·173·63·174). Li–In 합금 음극 or 버퍼층으로만 회피 | ✅ **상대적으로 좋다** — `Li₆PS₅Cl → Li₁₁PS₅Cl → {Li₂S, LiCl, S} → {Li₃P, LiCl, Li₂S}` 다단 분해로 **자기제한(self-limited) SEI** (본문-ref 175·176·174·181) |
| SEI 성분 성질 | LiX(절연) + **Li₃M(전자전도) ← 이것이 파탄 원인** | **Li₃P: σ_Li > 10⁻⁴ S cm⁻¹ (전자·이온 혼합전도)** (본문-ref 177·178) · **Li₂S·LiCl: 전자 절연 + 이온 전도** ⇒ 부동태화 |
| 남은 문제 | — | 중간상(S, Li₂S, LiCl) **부피팽창 → 덴드라이트** (본문-ref 175); **공극 → 국소전류 ↑ → 덴드라이트** (`Fig. 7f`, 본문-ref 183 = Kasemchainan 2019 *Nat. Mater.* 18, 1105) |

### 11b. ★ **Cl-rich 가 Li 금속 계면에서 하는 일** (우리 축 E 직결)

> "Notably, owing to the **moderate chlorine content and distribution**, the **halogen-rich LPSX-type SEs can exhibit excellent lithium compatibility**¹⁸⁵. The **excessive Cl content in the Li₆PS₅Cl SE does not change the argyrodite structure** because of a **minority of Cl on the lattice** to substitute the S. **The majority of Cl is distributed on the grain surfaces**, in which it forms **LiCl 'nanoshells'** that connect and build an **extended LiCl framework**. This microstructure has a synergistic effect with the **LiCl-dominated interfacial layer** and promotes the migration of Cl ions at the interface, so a **dense and uniform LiCl-dominated SEI is reconstructed during cycling.**"
> — 본문-ref **185 = Zeng, D. et al., *Nat. Commun.* 13, 1909 (2022)**

🔴 **이 문단은 우리에게 두 가지를 동시에 말한다 — 하나는 좋고 하나는 아프다.**
1. ✅ **좋은 쪽**: Cl-rich 는 σ 뿐 아니라 **Li 금속 계면(LiCl-dominated SEI)에서도 이득**이다.
   우리 `liu2022_cl_crystallization_interface_argyrodite`(LiCl-rich SEI)·`lu2025_tailoring_cl_rich_anode_licl` 와 **같은 서사**.
2. 🔴 **아픈 쪽**: **"과잉 Cl 의 다수는 격자가 아니라 입계(grain surface)에 있다"**.
   즉 **Zeng 2022 의 Cl-rich 시료에서 초과 Cl 은 상당 부분 벌크 4a/4d 자리에 안 들어갔다.**
   ⇒ 우리 modelc 는 **Cl 1.6 을 전부 격자에 넣은 단결정 셀**이다. **문헌 시료와 같은 물질이 아닐 수 있다.**
   **원고에서 modelc 를 "Li₅.₄PS₄.₄Cl₁.₆ 실험 시료의 모델" 이라고 쓰면 이 문단에 찔린다.**
   안전한 서술: *"the bulk-lattice limit of Cl incorporation"* / *"a fully lattice-substituted Cl-rich model"*.

---

## 12. ★7 **리뷰가 "아직 모른다"고 적은 것** (원고 gap 문장 재료)

| # | 리뷰의 원문 취지 | 위치 | 우리가 채울 수 있나 |
|---|---|---|---|
| G1 | "세 할로겐이 도입하는 **Li 공공의 정도로는 Li₆PS₅X 의 수 자릿수 σ 차이를 설명 못 한다 — 원자 점유에서 더 파고들어야 한다**" | p832 | ✅ **정면으로 우리 것** — comp2 disorder ensemble |
| G2 | "**최적 할로겐 분포를 실현하는 것이 Li₆PS₅X(X=Cl,Br) 설계의 중요한 고려사항**이고, 어닐링 온도가 그 인자일 수 있다" | p834 | ✅ 계산으로 분포-σ 지도를 그릴 수 있다 |
| G3 | 할로겐 **최대 고용한도(maximum solubility)의 수치를 안 준다** — 넘으면 잉여 LiX 로 σ 가 준다는 말만 | p834 | ⚠ 우리 DFT 로 형성에너지 기준 상한은 낼 수 있으나 실험 상한과는 다른 양 |
| G4 | "**희토류 HSE 의 이온전도·구조안정성 연구는 아직 초기 단계이고, 서로 다른 희토류의 역할을 더 밝혀야 한다**" | p838 | ✅✅ **우리 `ndo_lpscl16`(Nd) 의 존재 이유가 여기 적혀 있다.** 원고 서론에 그대로 인용 가능 |
| G5 | "**리튬 금속 음극과 여러 SE 의 상용성을 더 탐구해야 한다**"; LPSX 도 저항성 계면 문제 잔존 | p838 | ⚠ 계면은 우리 미완 축(W_ad 보류) |
| G6 | "SE **입도·입계상 조성·전해질 밀도**를 조절하는 공정기술 탐구 필요; 상(phase) 간·계면 이온전도 기전 규명 필요" | p838 | ❌ 우리 축 밖(DEM/미세구조 쪽) |
| G7 | "**할로겐을 SE 에 도입하는 LiX 이외의 대안 경로**가 필요하다 (LiX 의 수분 민감성 때문)" | p838 | ⚠ 합성 문제 |
| G8 | "HSE 는 불연성이지만 **잠재적 안전 위험이 여전히 있고**, 열안정성·열적 상용성을 충분히 고려해야 한다" | p838 | ❌ |
| G9 | `Fig. 6` 관련: "**이런 ASSB 의 고율(high-rate) 데이터가 아직 제한적이다**" | p836 | ❌ |

> ★ **원고 서론 gap 문장 1순위 = G1 + G4.**
> G1 은 "무질서를 원자 수준에서 다뤄야 한다"는 **분야 자체의 미해결 선언**이고,
> G4 는 **희토류(Nd) 도핑이 왜 열려 있는 문제인지**를 리뷰가 직접 적어 준 것이다.

---

## 13. ★8 **SI 에만 있는 것**

SI 는 6쪽이고 내용물은 **`Table S1` 하나뿐**이다. 그런데 그 하나가 **이 리뷰의 정량 자료 전부**다.

1. **`Table S1` = 47행 σ/Ea/합성법 표** (§3 에 전문 이식). **본문에는 이만한 표가 없다.**
   ⇒ **이 리뷰를 "수치 없는 리뷰" 로 넘기면 실질 산출물을 통째로 놓친다.**
2. 🔴 **SI 는 자체 참고문헌 번호(1–48)를 쓴다 — 본문(1–203)과 다르다.**
   같은 번호가 다른 논문을 가리키는 실제 사례:
   | 번호 | 본문 ref | SI ref |
   |---|---|---|
   | 18 | Peng et al. *Batteries & Supercaps* 6, e202200553 (2023) — **halogen-rich argyrodite 전용 리뷰** | Rao & Adams *Phys. Status Solidi A* 208, 1804 (2011) |
   | 26 | Zhao & Byon *AEM* 3, 1630 (2013) — Li–I₂ flow battery | **Adeli et al. *Angew.* 58, 8681 (2019)** |
   | 32 | Tian et al. *Nano Energy* 57, 692 (2019) — Na–I₂ | **Patel et al. *Chem. Mater.* 33, 1435 (2021)** |
   ⇒ **`Table S1` 의 값을 인용할 때 본문 번호를 쓰면 전혀 다른 논문을 인용하게 된다.** (§0 경고)
3. **SI 에만 있고 본문에 없는 논문**: **SI-ref 36 = Kato et al., *Nat. Energy* 1, 16030 (2016)**
   (Li₉.₅₄Si₁.₇₄P₁.₄₄S₁₁.₇Cl₀.₃, 2.5×10⁻² S cm⁻¹). 본문 203개 ref 안에 없다.
4. `Table S1` 에 **압력·펠릿밀도·전극·온도이력·측정법이 한 칸도 없다** — 그런데 표 안에는
   `Cold-pressed` 라벨이 **3행에만** 붙어 있다(SI-26·28). ⇒ **나머지 44행의 압력 조건은 알 수 없다.**
   (우리 `cronau2021_stack_pressure_ionic_conductivity` digest: 미세결정 황화물은 50–250 MPa 구간에서
   압력 의존이 크다. ⇒ **압력 미기재 σ 표를 서로 비교하는 것 자체가 위험하다.**)

---

## 14. 우리 DFT 대비 (comp1 / modelc / LPSOCl / ndo_lpscl16) → `our_dft_baseline.md`

| 항목 | 이 리뷰 (전부 2차 인용) | 우리 | 판정 |
|---|---|---|---|
| **Cl-rich → σ↑ / Ea↓** | Yu 2020(SI-21) 내부 비교 x 0→0.5: σ **3.96×**, Ea 0.296→**0.261**(−0.035 eV) | comp1→modelc: **D(600 K) 3.09→7.90×10⁻⁶ cm²/s (2.6×)**, Ea 0.253→0.224 eV(단일 궤적) / modelc 3-seed **0.197±0.032** | **✅✅ 방향·크기 정합.** ΔEa 문헌 −0.035 vs 우리 −0.029 — 같은 자릿수. ⛔ **σ 절대값은 비교하지 않는다**(우리 MLIP σ 인용 금지) |
| **기전 귀속** | **"에너지 지형(무질서)이지 Li 결핍이 아니다"** (본문-ref 162 Feng 2020) | 우리는 modelc 의 이득을 **disorder + vacancy** 로 설명해 왔다 | ⚠ **서사 교정 필요.** 문헌은 vacancy 설명을 **명시적으로 배제**한다. 우리도 "무질서 우선, vacancy 는 동반" 으로 쓰는 게 안전 |
| **자리 표기** | free-anion = **4a / 4d**, 케이지 중심 = **4d** | 우리·de Klerk digest = **4a / 4c(=4d)** | **✅ 매핑 확정.** 원고·발표에서는 **4a/4d 를 쓴다**(Nature Reviews·Kraft·Wang P. 관례) |
| **I 는 왜 느린가** | **자리 질서(I 전부 4a) → inter-cage 점프 0** | 우리 comp2 ordered(d=0) frozen 아티팩트가 같은 물리 | **✅ 우리 d-level 스캔의 문헌 프레임** |
| **산화 onset** | **수치 0건.** "LiX 도핑이 ESW 를 넓힌다"(정성) — **단 비교쌍은 LPS vs LPSX** | **comp1·modelc 모두 2.256 V (S²⁻-limited, 동일)** | 🔴 **표면상 상충 — 실제로는 다른 비교쌍이다.** 리뷰는 *황화물 유리에 LiX 를 넣는 것*을 말하고, 우리는 *argyrodite 안에서 Cl 1.0→1.6* 을 말한다. **섞으면 안 된다.** 우리 편은 **`banik2022_…`(S 가 VBM 을 pin → 단순 치환으론 산화 안정성 개선 불가)** 가 지지하고, 리뷰 자신도 본문-ref 167 로 ESW 확장 주장을 되돌린다 |
| **수분/O 도핑** | argyrodite σ 데이터 **0건**. F@Li₃InCl₆ 에서 **σ↓ + 수분보호↑** 사례만 | LPSOCl gap 2.2309 eV(전자구조 정본), MD σ 별도 판정 | **⚠ 리뷰는 침묵.** Wang 2025 `Fig. S11`(O 도핑 σ −41 %)과 **상충하지 않지만 지지도 안 한다**. 근거는 본문-ref 154 를 직접 확보해야 |
| **희토류 도핑** | "**초기 단계 — 역할 규명 필요**"(G4) | `ndo_lpscl16`(Nd·O 공도핑) 진행 중 | **✅ 우리 gap 문장의 외부 근거 확보** |
| **Cl 의 물리적 위치** | Zeng 2022: **과잉 Cl 의 다수가 입계(grain surface) LiCl 나노쉘**, 격자 치환은 소수 | modelc = Cl 1.6 **전량 격자 치환** 단결정 셀 | 🔴 **모델 한계 명시 필요.** "실험 Cl-rich 시료의 모델" 이 아니라 **"격자 고용 상한 모델"** 로 서술 |
| **밴드갭 / 전자구조** | **0건** | comp1 2.066 / modelc 2.099 / +B₂O₃ 1.9671 / LPSOCl 2.2309 eV | **n/a — 비교 대상 없음** |
| **기계적 물성** | "high deformability"(본문-ref 17) — **수치 0** | E_VRH 22.06 → 27.66 GPa · B₀ 26.23 → 21.71 GPa | **n/a** |
| **계면(Li 금속)** | `Fig. 7d`: Li₆PS₅Cl → Li₁₁PS₅Cl → {Li₂S,LiCl,S} → {Li₃P,LiCl,Li₂S}, **전자 차단 = 자기제한** | 우리 grand-potential 환원한계 1.242 V / OCV 1.717 V | **✅ 정성 정합** (분해 산물 종류가 우리 hull 산물과 같은 계열). ⛔ 전압 대 전압 비교는 리뷰에 수치가 없어 불가 |

> ⛔ **정정 2026-10-14 (사용자 '권고대로' · 트랙 우리 DFT 기준선)** — 위 행의 *'에너지 지형이지 Li 결핍이 아니다'* 는 Feng 2020 원문보다 세다. 원문은 AIMD 로 혼합이 Ea 를, 결핍이 σ 의 크기를 정한다고 쓰고 둘을 '완전히 분리하기 어렵다' 고 한다 (`papers/feng2020_li_deficient_argyrodite_cl_disorder.md` §7d-2). 우리 쪽 문장도 같이 고쳤다 — `db/properties/comp2_md_arrhenius.json` physics_verdict ('공공과 4d-Cl 둘 다 레버 · 우리 자료로는 우열을 못 가린다').

---

## 15. 적용 인사이트 — **우리 연구에 어떻게**

1. **`Fig. 5a` 사슬을 우리 modelc 서사의 골격으로 쓴다.** 지금 우리는 "Cl↑ → 공공↑ → 빠름" 으로 쓰는데,
   문헌 표준은 **"Cl↑ → 4d 무질서↑ → 4d 음전하↓ → Li 가 24g(전이상태)로 → inter-cage 거리 단축"** 이다.
   **24g 점유율**은 우리 UMA 궤적에서 바로 뽑을 수 있는 양이다 — **문헌 기전을 우리 데이터로 직접 시험하는 값싼 계산.**
2. **"조성 효과 ≈ 공정 효과" 를 방어선으로 삼는다.** §8c 의 Kitajima 3.1× 는 **우리 계산의 존재 이유**다:
   *"실험에서는 조성 효과와 열이력 효과가 같은 크기로 얽혀 있어 분리되지 않는다 — 계산은 조성만 바꾼다."*
   이건 리뷰어에게 먹히는 논거이고, **리뷰가 준 표로 증명된다.**
3. **modelc 는 문헌 데이터의 빈칸(x=0.6)에 있다.** x=0.5 는 5편, x=0.7 은 1편(그것도 3배 흔들림).
   ⇒ *"the composition window where the experimental record is thinnest and most process-sensitive"* 로 위치 지을 수 있다.
4. **본문-ref 154 (Sn–O 이중치환 Cl₁.₆ argyrodite) 를 즉시 확보한다.** 우리 LPSOCl 과 **Cl 함량까지 같다.**
   이게 있으면 우리 O 도핑 계가 "임의 조합" 이 아니라 **문헌 선례가 있는 조성** 이 된다.
5. **Zeng 2022 의 "입계 LiCl" 이 우리 모델의 한계를 정의한다.** 원고에 미리 한 문장 넣어 방어한다.

---

## 16. 인용 가능 문장 (deck / paper 용) — **전부 원 출처를 달아 쓴다**

- "Cl⁻ (167 pm) and S²⁻ (170 pm) have nearly identical crystal radii, which is why Cl/S site exchange over the 4a and 4d positions occurs in Li₆PS₅Cl, whereas the much larger I⁻ (206 pm) remains ordered on 4a — the structural origin of the several-orders-of-magnitude conductivity gap between Li₆PS₅Cl and Li₆PS₅I." *(He 2023 Nat. Rev. Chem. `Fig. 2a` + p832–833; 원 근거 refs 115, 131)*
- "In halogen-rich argyrodites Li₆₋ₓPS₅₋ₓX₁₊ₓ, the 1S3X configuration of the four 4d sites around P gives the highest jump rates, and the resulting enhancement has been attributed to the modified **energy landscape rather than to Li deficiency**." *(He 2023 p834; 원 출처 refs 138 = Wang P. 2020 Chem. Mater. 32, 3833 · 162 = Feng 2020 Energy Storage Mater. 30, 67)*
- "AIMD predicts that no inter-cage jumps occur when all Cl reside on 4a, that the doublet jump rate collapses when all Cl are placed on 4d, and that the conductivity is maximized at a 1:3 Cl distribution over 4a and 4d." *(He 2023 p834 요약; 원 출처 ref 135 = de Klerk 2016 Chem. Mater. 28, 7955 — **우리가 1차로 확인함**)*
- "Studies on the ionic conductivity and structural stability of **rare-earth-containing halogen solid electrolytes are still at an early stage**, and the roles of the different rare earths need to be further explored." *(He 2023 p838, Summary and outlook — **거의 원문 그대로 인용 가능한 gap 문장**)*
- "In chlorine-rich Li₆PS₅Cl, only a minority of the excess Cl substitutes S on the lattice; the majority is distributed on the grain surfaces as LiCl nanoshells that build an extended LiCl framework and a LiCl-dominated SEI." *(He 2023 p836; 원 출처 ref 185 = Zeng 2022 Nat. Commun. 13, 1909)*

---

## 17. 🔴 주의 / 한계 — **over-claim 방지 (비판)**

1. **자체 데이터 0.** 계산·실험·합성 전부 없다. **모든 수치가 2차 인용**이고, 상당수는 조건(압력·온도이력·전극)이
   탈락한 채 옮겨졌다. **값의 근거로 인용 금지.**
2. **`Table S1` 에 측정 조건이 없다.** 압력이 3행에만 적혀 있고 나머지 44행은 미상.
   황화물 미세결정 σ 는 stack pressure 에 크게 의존한다(`cronau2021` digest) ⇒ **행 간 비교는 원칙적으로 무효.**
3. **본문 ref 번호 ≠ SI ref 번호.** 같은 문서 안에서 두 체계가 충돌한다 (§13-2). **실무적 인용 위험이 크다.**
4. **`Fig. 6` 은 성능 비교로 쓸 수 없다.** 양극(LiCoO₂/NMC622/NMC811/TiS₂/Li₄Ti₅O₁₂)·음극(Li/Li-In/In)·
   로딩·온도가 전부 다른 14개 셀을 한 산점도에 얹었고, **셀마다 점이 1개씩**이라 rate 곡선도 아니다.
   최고점 235 mAh g⁻¹ 는 **TiS₂**(이론용량 ~239)이고 최저 110 은 LiCoO₂ 다 — **전해질이 아니라 양극을 본 것**이다.
   리뷰 스스로 "고율 데이터가 제한적" 이라 적었지만, **그림이 지지하는 결론이 무엇인지는 끝내 말하지 않는다.**
5. **`Fig. 2a` 축 이름이 틀렸다**: *"Standard redox potential (**eV**)"* — 값(2.870/1.358/1.230/1.080/0.536/0.142)은
   **표준환원전위 V vs SHE** 다(F₂/F⁻ 2.87 V 등). **eV 가 아니라 V.** 사소해 보이지만 그림에서 값을 옮길 때 단위가 따라간다.
6. **"1:3 최적" 을 확정 사실로 옮겼다.** 리뷰는 de Klerk 2016 을 정확히 옮겼지만,
   **그 최적치가 방법 의존이라는 사실은 안 적었다** — 우리 digest 가 이미 기록한 대로
   2024 MTP-MLIP 대규모 계산은 **σ 피크를 4d-Cl 25 %** 로 보고해 원전과 상충한다.
   원전 자체도 **분포당 단일 배열·단위셀·100 ps** 다. ⇒ **안전한 인용은 "중간 무질서에 최적이 존재한다(양 끝은 나쁘다)" 까지.**
7. **aliovalent 문장의 기전 오류** (§10-3): Li 자리 치환과 P 자리 치환을 한 문장에 묶어 "generate Li vacancies"
   라고 썼는데, **P 자리 Si⁴⁺/Ge⁴⁺ 치환은 Li 를 늘린다.** 방향이 반대다.
8. **산화 안정성 절이 비어 있다.** 제목이 "halogen chemistry" 인데 **ESW/산화 onset 수치가 단 하나도 없다.**
   할로겐 산화 안정성의 근거가 `Fig. 2a` 의 표준전위(수용액 화학!)와 정성 문장 두 개뿐이다.
   ⇒ **황화물 SE 의 산화 onset 은 S²⁻ 가 pin 한다**(우리 계산 + `banik2022`)는 결론과 **정면으로 대화하지 않는다.**
   리뷰는 이 논점을 다루지 못했다.
9. **공기/수분 안정성 절이 사실상 없다.** argyrodite 의 H₂S 발생·RH 노출 데이터 0건.
   `Table S1` 에 "air stability" 열이 없다. **할로겐 조성 ↔ 수분 안정성의 정량 관계를 이 리뷰에서 얻을 수 없다.**
10. **기계적 물성 0.** 서론에서 "good deformability"(본문-ref 17)를 HSE 의 장점으로 내세우고는
    탄성계수·경도·성형압 **수치를 하나도 주지 않는다.** 우리 축 C 와 접점 없음.
11. **불균형**: 본문 12쪽 중 Li–M–X 할라이드가 ~5쪽, argyrodite 는 ~2쪽이다.
    **argyrodite 를 찾아온 독자에게는 얇다.** 그 부족분을 채우는 전용 리뷰를 리뷰 스스로 가리킨다 —
    **본문-ref 18 = Peng, Yu, Cheng & Xie, "Halogen-rich lithium argyrodite solid-state electrolytes: a review",
    *Batteries & Supercaps* 6, e202200553 (2023)** ⇒ 획득 대상.
12. **`Fig. 4b` 범례의 `S/X (4a)` / `X/S (4d)` 순서**는 "다수/소수" 로 읽어야 앞뒤가 맞는데,
    **본문이 그 규약을 설명하지 않는다.** 원점 선택(4c vs 4d)을 아는 독자만 해독할 수 있다.
13. 🔴🔴 **본문과 자기 SI 가 220배 어긋난다 (가장 심각한 결함).**
    **본문 p832 "Li₆PS₅I is only about 10⁻⁶ S cm⁻¹"** ↔ **`Table S1` SI-18 "Li₆PS₅I 2.2×10⁻⁴ S cm⁻¹"**.
    본문의 "Cl·Br = 10⁻²–10⁻³" 도 자기 표의 Li₆PS₅Cl 7.4×10⁻⁴ 를 벗어난다.
    **argyrodite 절 전체의 출발 논증("several-orders-of-magnitude difference")이 이 10⁻⁶ 위에 서 있으므로**,
    결함이 주변부가 아니라 **핵심 주장에 걸린다.** ⇒ 이 리뷰에서 **Li₆PS₅X 의 σ 대비를 인용할 때는
    반드시 `Table S1` 값을 쓰고 본문 서술은 버린다.**

---

## 18. 🔧 도구 버그 보고 — `tools/litdb/extract_figures.py` (2026-09-09 실측)

| 증상 | 이 논문에서의 실측 | 원인 |
|---|---|---|
| **캡션이 그림과 다른 쪽에 있으면 통째로 누락** | **Fig 3(그림 p6 / 캡션 p7)**, **Fig 7(그림 p12 / 캡션 p13)** → "그래픽 없음(img0/draw0)" 으로 **제외됨** | 캡션 *위쪽* 영역만 검사 → 캡션 페이지 상단은 본문이라 그래픽 0 |
| **측면 캡션(side caption)이면 누락** | **Fig 1(p3)** — 캡션이 그림 **오른쪽 열**에 있음 → 위쪽은 여백 → 제외됨 | 위와 같은 기하 검증 |
| **2단 조판에서 단 경계에 잘림** | **Fig 2** (`x` 33.3→388.7, 페이지폭 595) — **결정반경 열 통째로 소실**; **Fig 5** (33.4→397.4) — c 패널 절반 소실; **Fig 4** (`y` 438.8→546.7 = 높이 108 pt) — **a·b·c 패널 전부 소실, d/e/f 띠만 남음** | 캡션 블록의 x 범위를 그림 폭으로 가정 |
| 정상 동작 | Fig 6(우측단 그림), Table S1 | — |

**조치**: 6장(Fig 1·2·3·4·5·7)을 손으로 bbox 재지정해 재렌더하고 `figures.json` 에 기록
(`note: "bbox manually corrected by curator 2026-09-09"` + `curator_note`).
⚠ **일반화 제안**: 캡션을 못 찾으면 **다음 페이지 상단 캡션 → 이전 페이지 전체**를 후보로 넣고,
bbox 는 **캡션 x 범위가 아니라 페이지 본문폭**을 기본값으로 쓰는 편이 안전하다.

---

## 19. ★ 우리 원고 · cascade 에 주는 것

### 19a. 서론(①)에서 인용할 문장 후보 — **원 출처 확인 목록** (로컬 PDF 확보 대상)

| 순위 | 쓸 문장 | 이 리뷰의 위치 | **확인해야 할 원 출처** | 우리 보유 |
|---|---|---|---|---|
| **1** | *"aliovalent 도핑이 argyrodite σ 를 올린다/내린다"* — **두 리뷰가 갈린 지점** | p834 첫 문장 + `Table S1` SI-39 | **Adeli, Bazak, Huq, Goward, Nazar, *Chem. Mater.* 33, 146 (2021)** (본문-ref 149) + **Zhang Z. et al., *J. Power Sources* 450, 227601 (2020)** (본문-ref 133) | ❌ **확보 필요 (1순위)** |
| **2** | *"Cl-rich 는 Li 결핍이 아니라 에너지 지형(무질서)으로 빨라진다"* | p834 | **Feng X. et al., *Energy Storage Mater.* 30, 67 (2020)** (본문-ref 162) + **Wang P. et al., *Chem. Mater.* 32, 3833 (2020)** (본문-ref 138) | ❌ **확보 필요 (2순위 — 우리 modelc 서사의 심장)** |
| **3** | *"Cl 1.6 + O 치환 argyrodite 가 수분·전기화학 안정성을 개선한다"* — **우리 LPSOCl 의 선례** | p834 | **Li G. et al., *Adv. Funct. Mater.* 33, 2211805 (2022)** — `Li₅.₅(P₀.₉Sn₀.₁)(S₄.₂O₀.₂)Cl₁.₆` (본문-ref 154) | ❌ **확보 필요 (3순위)** |
| **4** | *"과잉 Cl 의 다수는 격자가 아니라 입계 LiCl 나노쉘로 간다"* — **우리 모델 한계 선언용** | p836 | **Zeng D. et al., *Nat. Commun.* 13, 1909 (2022)** (본문-ref 185, OA) | ❌ 확보 필요 |
| **5** | *"희토류 HSE 연구는 초기 단계"* — **ndo_lpscl16 의 gap 문장** | p838 | **리뷰 자신을 인용하면 된다** (He 2023, Nat. Rev. Chem. 7, 826) | ✅ 이 파일 |
| 보 | argyrodite 할로겐-rich 전용 리뷰 | 본문-ref 18 | **Peng, Yu, Cheng & Xie, *Batteries & Supercaps* 6, e202200553 (2023)** | ❌ 확보 권장 |

> ★ **보너스 — Ea 만 보고 판단하지 말라는 근거**: 이중할로겐 도식(`Fig. 5b`)이 **분극률↑ → Ea↓(이득)과
> Arrhenius 전인자 σ₀↓(손해)를 동시에** 그려 놓았고, 무질서↓ 도 "adverse effect" 로 빨갛게 표시했다.
> 우리가 Arrhenius 를 보고할 때 **Ea 와 σ₀ 를 분리해 말해야 하는 이유**를 리뷰 그림이 직접 준다.

> ⚠ **위 1–4 는 우리가 아직 원문을 안 봤다.** He 2023 을 근거로 인용하면 **2차 인용**이 된다.
> 원고에 넣기 전에 반드시 로컬 PDF 로 확인한다 (2026-07 Kim/Cui 교훈).

### 19b. 도펀트 스크리닝 cascade 재설계에 주는 것

1. **site-rule 판정의 외부 압력**: 리뷰는 **Li 자리 aliovalent(Ca²⁺·Al³⁺)** 를 표준 전략으로 분류한다.
   우리 cascade 가 **M³⁺ = Li_24g** 로 26/26 수렴한 것과 **같은 방향**이다
   (⚠ 반대로 `wang2025_electronic_localization_yo_argyrodite` 의 Y@P_4b 주장과는 어긋난다 — 이미 그 근거를 §무효 판정).
   ⇒ **이 리뷰는 우리 site-rule 쪽 증거로 쓸 수 있다** (단, 정성 문장으로만).
2. **cascade 의 목적함수에 "24g 점유율" 을 넣을 근거**: `Fig. 5a` 가 24g 점유를 σ 의 중간 지표로 명시한다.
   UMA 궤적에서 싸게 뽑히는 양이므로 **T1 스크린 지표 후보**.
3. **cascade 가 다뤄야 할 자리 축**: 이 리뷰가 정리한 argyrodite 치환 자리는 **딱 3개** —
   **Li(24g/48h) · P(4b) · S(16e)/free-anion(4a·4d)**. 우리 cascade 의 자리 열거가 이 셋을 덮는지 점검할 것.
4. **⛔ cascade 에 넣으면 안 되는 것**: 이 리뷰의 σ·Ea 값. 전부 조건 미상의 2차 인용이라
   **ML 학습 라벨로도 쓰면 안 된다** (압력 미기재 44행).

# Influence of Lattice Polarizability on the Ionic Conductivity in the Lithium Superionic Argyrodites Li₆PS₅X (X = Cl, Br, I) — Kraft et al. (J. Am. Chem. Soc. 2017)

> slug `kraft2017_lattice_polarizability_argyrodite_Li6PS5X` · DOI `10.1021/jacs.7b06327` · type `exp (neutron + PDF + impedance + ultrasound; DFT 없음)` · PDF 본문 = 업로드 `664401af…`(10 pp, inbox #31 슬롯 대조 확인) · **SI = `litdb/inbox/31. Sup) Influence of Lattice Polarizability….pdf`(15 pp, inbox #31 Sup, 사용자 분류 `DFT`) — 2026-07-24 실물 대조 감사 완료(§3a 감사 노트)** + 업로드 SI `38f51c84…` · digested `2026-07-24` · status ✅
> elements: Li, P, S, Cl, Br, I
> methods: impedance-spectroscopy, ultrasonic-speed-of-sound, RUS, Debye-frequency, neutron-diffraction, Rietveld, synchrotron-PDF, Meyer-Neldel
> **저자**: Marvin A. Kraft, Sean P. Culver, Mario Calderon, Felix Böcher, Thorben Krauskopf, Anatoliy Senyshyn, Christian Dietrich, Alexandra Zevalkink, Jürgen Janek, **Wolfgang G. Zeier*** (JLU Giessen / TU München FRM II / Michigan State) · JACS 2017, 139, 10909−10918. Received 2017-06-22, Published 2017-07-25. **Not open access** (© ACS 2017; Hanyang 기관 접근).

---

## 0. 이 digest를 읽는 법 (우리에게 왜 최우선인가)
이 논문은 **우리 물질·조성과 정확히 같은** Li₆PS₅X 아지로다이트(X = Cl, Br, I 및 그 고용체 9종)에서 **"음이온 분극성(polarizability) ↔ 격자 무름(lattice softness) ↔ 이온전도"** 삼각관계를 실험으로 정면 규명한 **원본(anchor)** 이다. 우리 프로젝트가 지금 돌리는 두 계산 체인의 문헌 닻:
- **ε∞ 체인**(전자 유전율 = 전자 분극성 대리) ↔ Kraft가 *조작 변수*로 쓴 "anion polarizability"
- **elastic 체인**(B/G/E, C_ij) ↔ Kraft가 *직접 측정*한 lattice softness (ultrasonic **speed of sound** + **RUS 탄성텐서** + **Debye frequency**)

**핵심 발견 한 문장**: 무거운·더 분극성인 할라이드(Cl→Br→I)로 갈수록 격자가 **무르지고**(speed of sound↓, Debye freq↓), 그 결과 이온 이동 **활성화장벽 E_A는 낮아지지만** *동시에* **아레니우스 prefactor σ₀도 낮아진다**. 두 효과가 **상쇄**하기 때문에 "무른 격자 = 더 좋은 전도체"라는 통념은 틀리고, **최적 전도도는 중간 강성**(Li₆PS₅**Cl₀.₅Br₀.₅** = 우리 comp2!)에서 나온다.

> ⚠ **가장 중요한 개념 구분 (§7·§8·§12에서 반복)**: Kraft의 "polarizability"는 *입력 변수*(할라이드의 전자 분극성 화학 트렌드, α(Cl⁻)<α(Br⁻)<α(I⁻)), 그가 *측정*한 것은 **기계적 무름**(speed of sound / Debye / C_ij)이다. 우리 **ε∞ = 전자 분극성**(Kraft의 입력과 같은 물리량, 우리가 계산), 우리 **elastic/Debye/phonon = 기계적 무름**(Kraft가 잰 그 물리량). ε∞와 modulus는 *다른* 물리량이며, Kraft의 논지는 "둘이 상관한다"는 것이지 "같다"가 아니다. **Kraft의 메커니즘을 재현하려면 elastic 체인(+phonon 진동수)이 필요하고, ε∞ 단독은 분극성 *트렌드*만 준다.**

## 1. 한 줄 요약
Li₆PS₅X에서 Cl→Br→I 치환은 전도 경로·carrier 농도·결함형성E를 거의 안 건드리고 **오직 음이온 분극성·격자상수(=격자 무름)만** 바꾸는 이상적 모델계다. 무른 격자는 E_A를 낮추지만 **prefactor(attempt frequency ν₀ ∝ Debye freq, 이동 엔트로피 ΔS_m)도 함께 낮춰** σ를 되레 깎으므로, **σ 최적은 중간 강성 Li₆PS₅Cl₀.₅Br₀.₅**에 있다 → "soft lattice ≠ always better", 격자 강성은 **튜닝해야 할 대상**.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 모델계 | **Li₆PS₅X** 고용체 9종: X = Cl, Cl₀.₇₅Br₀.₂₅, **Cl₀.₅Br₀.₅(=comp2)**, Cl₀.₂₅Br₀.₇₅, Br, Br₀.₇₅I₀.₂₅, **Br₀.₅I₀.₅**, Br₀.₂₅I₀.₇₅, **I(=comp5 조성)** — 전부 공간군 **F4̄3m** cubic |
| 왜 이 계 | 할라이드 치환은 **음이온 분극성·격자상수만** 바꿈 (전도 경로·carrier·결함형성E 불변) → *분극성 하나*를 깨끗이 조절하는 이상적 model system |
| 질문 | "부드러운 음이온 격자 → 낮은 이동장벽"이라는 *자주 인용되나 검증 안 된* 관계를, 한 물질군 안에서 격자 dynamics를 *체계적으로* 바꿔 규명 |
| 방법 3축 | (1) 구조·무질서·점프거리 = **중성자 회절 + synchrotron PDF**; (2) 격자 무름 = **ultrasonic speed of sound(PE) + RUS 탄성텐서** → Debye; (3) 전도 = **온도의존 임피던스**(E_A, σ, prefactor) |
| 선행 맥락 | Zeller/Fischer(은할라이드 분극성↔oscillator strength), de Klerk & Wagemaker(anion disorder가 inter-cage 장벽↓), Meyer–Neldel rule(E_A↓↔prefactor↓ 보상), phonon-assisted diffusion(Adelstein/Wood, paddle-wheel/Jansen) |
| **DFT** | **없음** — 순수 실험. 이론은 hopping 이론(eq 1·5·6·7)의 해석적 대입뿐 |

## 3. 핵심 물성 (수치 총정리)
> ⚠ **출처 표기 규율**: **격자상수·무질서·점유율·불순물**은 SI Table S1–S14 (중성자 Rietveld / X-ray PDF) **정확값**. **속도·Debye·E_A·σ·prefactor·점프거리**는 SI에 *표가 없고* main **Fig 4/6/7·SI Fig S2의 데이터 포인트만** 존재 → **figure-read(≈)** 로 표기, 정밀도 한계 명시. 문헌값이므로 우리 db 절대값과 섞지 않음.

### 3a. 구조 (SI 정확값, 중성자 Rietveld)
| X in Li₆PS₅X | a (중성자, Å) | a (X-ray PDF, Å) | 음이온 4d 무질서* | Li 48h occ | Li 24g occ | 불순물 (중성자) |
|---|---|---|---|---|---|---|
| **Cl (=comp1)** | 9.8614(1) | 9.898(7) | ~62 % | 0.500 | 0 (없음) | 6.6 % Li₃PO₄ · 1.2 % LiCl |
| Cl₀.₇₅Br₀.₂₅ | 9.8911(1) | — | ~58 % | 0.500 | 0 | 4.3 % Li₃PO₄ · 1.0 % LiCl |
| **Cl₀.₅Br₀.₅ (=comp2)** | 9.9223(1) | 9.952(7) | ~50 % | 0.500 | 0 | 7.0 % Li₃PO₄ · 0.2 % LiCl |
| Cl₀.₂₅Br₀.₇₅ | 9.9530(3) | — | ~30 % | 0.456 | 0.088 | 1.8 % Li₃PO₄ · 2.3 % LiBr |
| Br | 9.9850(3) | 10.020(8) | ~22 % | 0.441 | 0.119 | 1.1 % Li₃PO₄ · 1.0 % LiBr |
| Br₀.₇₅I₀.₂₅ | 10.0336(3) | — | ~15 % | 0.412 | 0.175 | 1.1 % LiBr · 0.4 % Li₂CO₃ |
| **Br₀.₅I₀.₅** | 10.0722(3) | 10.109(8) | ~3.5 % | 0.409 | 0.183 | 0.8 % Li₃PO₄ · 0.5 % LiBr |
| Br₀.₂₅I₀.₇₅ | 10.1108(2) | — | ~1.6 % | 0.407 | 0.185 | 0.2 % Li₃PO₄ · 0.4 % LiBr |
| **I (=comp5 조성)** | 10.14135(6) | 10.181(8) | **0 %** | 0.391 | 0.219 | 1.5 % Li₃PO₄ · 1.6 % LiI |

*무질서 = 할라이드가 S²⁻ 자리(4d)에 앉은 비율(=Cl-2/Br-2/I-2 occ 합), SI 점유율표에서 계산. Fig 3c와 일치. **Cl 62 % → I 0 %로 단조 소멸** (I⁻ 반경 2.2 Å ≫ S²⁻ 1.84 Å라 섞이지 못함; Cl⁻ 1.81 ≈ S²⁻ 1.84 ≈ Br⁻ 1.96 Å라 잘 섞임).

> **✅ SI 실물 감사 (2026-07-24, `inbox/31. Sup)…pdf` 15 pp 전문 추출 대조)**: 위 표의 9조성 전값(a·Li/음이온 occ·무질서 %·불순물)이 SI **Table S6–S14**(중성자 Rietveld)·**S1–S5**(X-ray synchrotron PDF, 5조성)와 **전부 일치**. SI가 추가로 주는 것:
> - **중성자 fit 잔차**: Rwp 2.73–3.13 % · Rexp 2.01–2.13 % · χ² 1.71–2.26 (전조성 양호). X-ray PDF Rw는 17.8 %(Cl) → 9.3 %(I)로 단조 개선.
> - **Uiso(Li1 48h, 중성자) 0.070(2) → 0.024(1) Å² 단조 감소(Cl→I)** — Li 변위 파라미터가 I로 갈수록 축소. σ 3자릿수 하락·48h→24g 재배치와 방향 정합(*이 해석은 우리 것* — 저자는 SI에서 언급 안 함). X-ray 표(S1–S5)에서는 Li ADP를 0.05로 고정(좌표는 중성자값 고정) — Li에는 중성자 표가 원천.
> - X-ray 불순물 정량은 중성자와 소폭 다름(예: Cl 조성 X-ray 7.1 % Li₃PO₄·3.0 % LiCl vs 중성자 6.6 %·1.2 %) — 방법차, 인용은 중성자 기준 유지.
> - **속도·C_ij·E_A·σ·σ₀·점프거리 표는 SI에도 없음 확정** (SI 구성 = 결정학표 S1–S14 + Fig S1 G(r) overlay + Fig S2 Meyer–Neldel이 전부) → §14 figure-read(≈) 캐비앳 그대로 유효.
> 격자상수는 Vegard 법칙 선형 (**Cl 9.86 → I 10.14 Å, +2.8 %**) = 고용체 합성 성공 증거. Li는 48h→24g로 재배치: I로 갈수록 **48h occ 0.50→0.39↓, 24g(전이상태 삼각자리) occ 0→0.22↑** (큰 격자 = 24g 안정화).

### 3b. 격자 무름 (Fig 6a·7a, **figure-read ≈**)
| 지표 | Cl (comp1) | Cl₀.₅Br₀.₅ (comp2) | Br | Br₀.₅I₀.₅ (최연) | I | Cl→최연 변화 |
|---|---|---|---|---|---|---|
| v_long (PE) / ms⁻¹ | ~1480 | ~1360 | ~1280 | ~1130 | ~1200↑ | **−24 %** |
| v_trans (PE) / ms⁻¹ | ~1050 | ~980 | ~900 | ~800 | ~850↑ | **−24 %** |
| v_mean / ms⁻¹ | ~1050 | ~1000 | ~950 | ~900 | ~920↑ | **−14 %** |
| Debye freq ν_D / ×10¹² Hz | ~2.45 | ~2.30 | ~2.00 | ~1.90 | ~2.00↑ | **−22 %** |
> RUS 속도(v_long/v_trans, 빈 사각)는 PE보다 ~50–100 ms⁻¹ 높으나 **트렌드 동일**(독립 확인). 속도·Debye 모두 Cl→Br₀.₅I₀.₅까지 **단조 감소 후 순수 I에서 소폭 반등**(I는 무질서 0이라 오히려 약간 강성 회복). **→ 할라이드가 격자를 실측으로 무르게 만든다 (§7 우리 가설 판정 핵심).**

### 3c. 이온전도 (Fig 6b,c·7b·S2, **figure-read ≈**)
| 지표 | Cl (comp1) | Cl₀.₅Br₀.₅ (comp2) | Br | Br₀.₅I₀.₅ | I | 비고 |
|---|---|---|---|---|---|---|
| **σ_RT / S cm⁻¹** | ~1.3×10⁻³ | **~2×10⁻³ (최대!)** | ~1×10⁻³ | 감소 | **~1×10⁻⁶** | Fig 6c; 최적 = **comp2** |
| **E_A / eV** (임피던스 total) | **~0.44–0.46** | ~0.40 | ~0.35 | **~0.30–0.31 (최소)** | ~0.38↑ | Fig 6b |
| prefactor σ₀ / KScm⁻¹ | ~2.7×10⁷ (최대) | ~1.6×10⁶ | ~7×10³ | ~10³ (최소) | ~1.8×10³ | Fig 6b·S2 |
| jump freq ν₀ / ×10¹⁵ Hz | ~1.3 | — | ~1.0 | ~0.9 | ~0.8 | Fig 7b (eq 7, ν_D와 상관) |
> **σ 최적 = Cl₀.₅Br₀.₅(comp2) ~2 mS/cm.** E_A는 Cl→Br₀.₅I₀.₅까지 단조↓(0.46→0.30) 후 **순수 I에서 반등(0.38)** — I는 무질서가 0이라 장벽↑(de Klerk 예측). **문헌값(초록 사각, Fig 6c): Cl ~1×10⁻³, I ~3×10⁻⁷** (I가 3–4 자릿수 낮음 = Rao2011 4.6×10⁻⁷과 정합). prefactor σ₀는 E_A와 같은 방향(높은 E_A=높은 σ₀) = **Meyer–Neldel 보상(§5.6)**.

### 3d. 점프거리 (Fig 4·3d, **figure-read ≈**)
| 점프 | Cl | I | 방향 |
|---|---|---|---|
| **inter-cage** (거시 σ 율속) | ~2.7 Å | ~3.3 Å | **↑** (격자 팽창) |
| intra-cage | ~2.35 Å | ~2.55 Å | ↑ |
| doublet (48h–48h) | ~1.5 Å | ~1.2 Å | ↓ (Li 자리가 24g 쪽으로) |
| doublet 삼각자리 면적 (Fig 3d) | ~7.2 Å² | ~7.75 Å² | ↑ (24g 전이상태 안정화) |

## 4. 재료 & 방법 (실험) ★
- **합성**: 고상 반응. Li₂S+P₂S₅+LiX 화학량론, agate 분쇄 → 석영관(carbon-coated, 800 °C 예열·진공 밀봉) → **550 °C 2주**. 조성당 **3회 합성**(오차막대용). 등방압 펠릿(10 mm, 임피던스·속도용).
- **중성자 분말회절**: FRM II Garching **SPODL** 고분해능(λ=1.54817 Å, thermal), Debye–Scherrer, ³He 멀티검출기, V 용기 Ar. **Rietveld = GSAS-II**(pseudo-Voigt Thompson–Cox–Hastings); Na₂Ca₃Al₂F₁₄ 기기분해능 기준; **음이온 점유율을 마지막에 자유정련**해 무질서 정량. Li 좌표는 중성자로, ADP는 U_iso=0.05 고정.
- **Synchrotron X-ray PDF**: Diamond Light Source **I15**(λ=0.173369 Å, 71.52 keV, PerkinElmer 1621), Q_max=17 Å⁻¹, PDFgetX2→G(r), **PDFgui** F4̄3m 정련(1.8–30 Å). Li 좌표는 중성자 고정, S만 자유.
- **임피던스(EIS)**: SP300 Biologic, SUS 봉(10 mm, 3 ton 3 min), **−10 ~ 60 °C**, 7 MHz–100 mHz, 10 mV. **Bulk+GB 분리 불가 → 보고 σ = 전체(overall) 시료 전도도** (‼ 우리 bulk MD와 대비 시 핵심 caveat, §7). 조성당 3회.
- **Ultrasonic pulse-echo(PE)**: Epoch 600(Olympus), 5 MHz longitudinal+transverse, 펠릿 **Au(<200 nm) 코팅**(coupling fluid 부반응 차단), **85 % 치밀 시료**(불확실도 ~2 %).
- **Resonant Ultrasound Spectroscopy(RUS)**: RUSpec(Quasar), 30–350 kHz, Ar 글러브박스. **탄성텐서 C₁₁, C₁₂, C₄₄** 산출(RPModel, rms<0.5 %). *couplant 불필요 → 시료 분해 없음.*
- **속도→Debye 변환식**:
  - v_trans = √(C₄₄/d),  v_long = √((C₁₁+2C₁₂+4C₄₄)/(3d))  (d=기하밀도)
  - v_mean⁻³ = ⅓(v_long⁻³ + 2v_trans⁻³)  (eq 2)
  - Θ_D = (ħ/k_B)(6π²N/V)^{1/3} v_mean  (eq 3)
  - ν_D = (3N/4πV)^{1/3} v_mean  (eq 4)
- **hopping 이론(해석)**: σ = nZeμ, μ ∝ exp(−E_A/k_BT) (eq 1); σT=σ₀exp(−E_A/k_BT) (eq 5); **prefactor** σ₀ = [zn(Ze)²/k_B]·e^{ΔS_m/k_B}·a₀²·ν₀ (eq 6); **attempt freq** ν₀ = (1/a₀)√(2E_A/M_Li) (eq 7).

> ‼ **무질서 처리**: SQS·enumeration 없음(순수 실험). "무질서"는 **Rietveld로 정련한 음이온 4a/4d 점유율**로 정량. 이 부분이 우리 DFT의 무질서 처리(SQS/enumerate/single-config)와 대비되는 *실측 ground truth*.

## 5. 결과 — 섹션별 상세

### 5.1 구조 특성 (Fig 2·3, Table S1–S14)
- **Vegard 선형** a: Cl 9.86 → I 10.14 Å(중성자). PDF는 공간·시간평균이 달라 살짝 높음(9.90→10.18). 모든 고용체 단상(불순물 <5–8 wt%: Li₃PO₄·LiX·미량 Li₂CO₃).
- **PDF 이상거리 ~3.4 Å**(Fig 2b·S1): 구조모형으로 설명 안 됨, **Cl→I로 감소**. Dietrich의 ³¹P NMR 비정질 신호(Li₂P₂S₆-유사 glassy phase)와 정합 — 소량 비정질상 시사.
- **무질서 소멸(Fig 3c)**: Cl 62 % → Br 22 % → I 0 %. Cl⁻(1.81)·Br⁻(1.96)·S²⁻(1.84 Å) 반경 유사 → 잘 섞임; I⁻(2.2 Å) 너무 큼 → **무질서 불가**. **"disorder가 inter-cage 점프율을 높인다"(de Klerk)** → I는 이 이점을 잃음.
- **Li 재배치(Fig 3b·3d)**: 48h occ 0.50→0.39, 24g occ 0→0.22. 큰 격자·큰 24g 삼각면적(7.2→7.75 Å²)이 **전이상태(24g) 점유를 안정화** → I는 여기 Li가 갇힐 위험.

### 5.2 점프거리 (Fig 4)
격자 팽창으로 **inter-cage(2.7→3.3 Å)·intra-cage(2.35→2.55 Å) 거리 증가**, doublet(48h–48h) 거리 감소(1.5→1.2 Å). inter-cage가 거시 수송 율속 → 거리 증가는 장벽↑ 요인. **"거리 증가(장벽↑) vs 격자 무름(장벽↓)"의 경쟁**이 이 논문의 물리적 긴장.

### 5.3 격자 무름 측정 (Fig 6a) — 이 논문의 심장
- **더 분극성·무거운 할라이드 → 낮은 speed of sound**(Cl→Br₀.₅I₀.₅에서 v_long −24 %, v_mean −14 %), 순수 I는 무질서 0이라 소폭 반등.
- **PE와 RUS 두 독립 방법이 같은 트렌드** → 견고. (RUS 절대값 약간 높음 = 85 % 치밀 vs 완전 치밀 차이.)
- 높은 speed of sound = 강한 결합(높은 spring constant) = 높은 Debye/attempt frequency. **속도는 acoustic phonon 분지 기울기의 직접 척도.**
> **원문**: *"a high speed of sound, which directly indicates a more rigid lattice with stiffer bonds (reduced spring constant), corresponds to high Debye temperatures and high Debye frequencies."* — 높은 음속 = 강한 결합 = 높은 Debye = 높은 attempt frequency.

### 5.4 온도의존 전도도 (Fig 5)
아레니우스 등가과정 σT=σ₀exp(−E_A/k_BT) (eq 5)로 −10~60 °C 피팅. 등가회로 = 1 CPE/저항 병렬 + blocking CPE; apex 1.1×10⁶ Hz(C=1.2×10⁻⁹ F). **bulk/GB 미분리 → overall σ** (표준편차가 시료 밀도차 반영).

### 5.5 무름 ↔ 전도의 상관 (Fig 6b,c) — 핵심 반전
- **E_A 감소(무른 격자)**: Cl 0.46 → Br₀.₅I₀.₅ 0.30 eV. **BUT prefactor σ₀도 감소**(2.7×10⁷ → 10³ KScm⁻¹).
- **두 효과 상쇄 → σ_RT 최적은 중간 강성 Cl₀.₅Br₀.₅**(~2 mS/cm), 가장 무른 조성이 아님.
- **순수 I 예외**: 무질서 0 → E_A 반등(0.38) → I 계 저전도(~10⁻⁶)의 원인이 *격자 무름이 아니라 무질서 소멸 + prefactor 붕괴*임을 보임.
> **원문**: *"the effect of a softer lattice on the Arrhenius prefactor has so far been overlooked and leads to a decreasing conductivity of solid electrolytes with very soft lattices."* — 무른 격자의 prefactor 효과가 간과돼 왔고, 너무 무른 격자는 오히려 σ를 깎는다.

### 5.6 prefactor 물리 & Meyer–Neldel (eq 6·7, Fig 7b·S2)
- **prefactor(eq 6)** = carrier(n) × 점프거리²(a₀²) × **attempt frequency(ν₀)** × e^{ΔS_m/k_B}. 무른 격자 → 낮은 ν_D → 낮은 ν₀ → 낮은 σ₀. 또 낮은 E_A → (eq 7) 낮은 ν₀. 또 낮은 ΔS_m(진동 분배함수 비).
- **Fig 7b**: jump freq ν₀ vs Debye freq ν_D **상관**(점선 가이드) = "격자 무름이 실제로 이동 이온의 진동수를 낮춘다"의 직접 증거. 단 ν_D(~2×10¹²)는 ν₀(~10¹⁵)보다 **약 3자릿수 작음**(저자 인정: parabolic 근사·intracage 거리·P–S vs Li–anion 결합 평균의 한계).
- **Fig S2(Meyer–Neldel)**: log(σ₀) vs E_A **선형**(보상 법칙) — *무질서가 우세할 때만*. **순수 I(무질서 0)에서 선형성 붕괴** = disorder가 MN 보상의 조건임을 실험으로 보임.

## 6. 메커니즘 종합 (Fig 8 schematic)
할라이드 치환(Cl→Br→I) → (a) 음이온 **분극성↑**·**격자상수↑** → (b) **격자 무름**(spring constant↓, speed of sound↓, ν_D↓) → (c) 이동 이온의 **local oscillator 넓어짐** → **E_A↓ AND attempt frequency ν₀↓ AND ΔS_m 변화** → (d) σ₀↓. **E_A↓(σ↑ 요인)와 σ₀↓(σ↓ 요인)의 경쟁** → σ 최적 = 중간 강성(Cl₀.₅Br₀.₅). 병렬로 **무질서 소멸**(Cl 62→I 0 %)이 I에서 E_A를 도로 올림. **결론 패러다임 전환**: "부드러운 격자가 항상 좋다"는 통념은 틀리며, 격자 강성은 **최적화 대상**이다.

## 7. 우리 DFT 대비 (comp1/comp2/comp5/modelc) → `../our_dft_baseline.md`
> **문헌(측정) / 우리(DFT·MD) 열 분리, 절대값 혼합 금지.** Kraft = *할라이드 종류* 축(Cl↔Br↔I 교환); 우리 modelc = *Cl 함량* 축(별개). **comp1=Kraft Cl, comp2=Kraft Cl₀.₅Br₀.₅ 정확 일치**가 최강 닻.

| 항목 | **Kraft (측정)** | **우리 (방법)** | 일치/차이 + 이유 |
|---|---|---|---|
| **격자상수 a** | Cl 9.8614 / Cl₀.₅Br₀.₅ 9.9223 / I 10.14135 Å (중성자) | comp1 a≈10.055 Å (relaxed DFT) | **△ 방향 일치, 절대 +2 %**(PBE 과대팽창 통상). Vegard 선형은 공유 |
| **격자 무름(speed of sound·Debye)** | v_long Cl 1480→Br₀.₅I₀.₅ 1130 ms⁻¹(**−24 %**); ν_D 2.45→1.90×10¹² Hz(**−22 %**) | elastic 체인: comp1 relaxed **E_VRH 22.06 / B_VRH 25.51 / G_VRH 8.13 GPa · C₄₄ 7.98**; **comp2 elastic 진행중** | **△ 종류 같은 물리량(기계 강성), 직접 대응**. Kraft가 *할라이드로 강성을 실측으로 −15~24 % 바꿈* → §8 가설 판정. 우리 comp2가 comp1 대비 소폭 연화하면 정합 |
| **음이온 분극성(=polarizability)** | *입력 변수* α(Cl⁻)<α(Br⁻)<α(I⁻)(화학 트렌드; α 수치 미기재) | **ε∞**: comp2 ≈3.80 (n∞≈1.95) 완료 · comp1 DFPT 진행중 | **✓ 개념 대응(but 다른 물리량)**: 우리 ε∞ = 전자 분극성 = Kraft의 *입력*. Br(comp2)이 Cl(comp1)보다 분극성↑ → comp2 ε∞>comp1 예상, Kraft 트렌드와 방향 정합. **단 Kraft는 ε∞를 안 잼**(§12 구분) |
| **E_A 방향(Cl→Br)** | Cl ~0.46 → Cl₀.₅Br₀.₅ ~0.40 → Br ~0.35 eV (**↓**) | MD Ea(UMA): comp1 0.253 eV *(멀티시드 진행 참고값)*; comp2 미측정 | **✓ 방향 일치**(무름·무질서 → Ea↓). **⚠ 절대값 비교 금지**: Kraft E_A=*total(bulk+GB) 임피던스* 0.46 ≫ 우리 *bulk MD* 0.253 = **주로 방법차**(GB 포함 vs bulk, impedance vs AIMD), 실물리 차 아님 |
| **σ 할라이드 최적** | **Cl₀.₅Br₀.₅(=comp2)가 σ 최대 ~2 mS/cm** | comp2 σ 미측정(ε∞·elastic 중); comp1 AIMD RT-외삽 ~3.35 mS/cm | **○ 검증 예측**: Kraft가 comp2를 최적점으로 지목 → 우리 comp2 계산의 *기대 위치*(Ea↓·σ↑ vs comp1). 절대 σ는 UMA 과대라 방향만 |
| **σ 순위 Cl vs I** | Cl 1.3×10⁻³ ≫ I ~10⁻⁶ (3자릿수) | comp5(Li₆PS₅I) 별도 구조모형 | **✓ 방향**: I 저전도(무질서 0 + prefactor 붕괴) = Rao2011과 정합. **⚠ 우리 comp5=rhombo 모형 vs Kraft I=F4̄3m** → 구조모형 차 주의 |
| **prefactor 지배** | σ₀ 무름 따라 **10³–10⁷ 4자릿수 변동**(E_A보다 빨리) | Nd 도핑 σ-drop = **D0 prefactor 0.65× 지배**(Ea 0.224→0.227 불변) | **✓✓ 개념 정합**: Kraft "prefactor가 σ를 지배·softer≠better"가 우리 **prefactor-dominated Nd 분석**의 문헌 앵커 (§12 insight 2) |
| **무질서→전도** | Cl 62 % disorder = 고전도; I 0 % = 저전도 | modelc Cl-rich disorder↑ → D↑·Ea↓ (comp1→modelc 0.253→0.224) | **✓ 같은 레버(disorder)**, 다른 수단(Kraft=할라이드 종류 / 우리=Cl 함량). Rupp·Rao2011·GG·Liu와 한 줄 |
| **modulus vs modelc(Cl-rich)** | Kraft는 Cl-rich 미포함(n/a) | modelc E_VRH 27.66↑ / B0 21.71↓ (comp1 대비 방향 반대) | **✗ 범위 밖**: modelc=Li 공공/무질서 축, Kraft=할라이드 교환 축. Kraft로 modelc 강성 예측 불가 |

## 8. ★ 우리 가설 판정 — "할라이드는 modulus에 둔감한가?"
**우리 가설**: "우리 계에서 modulus는 P–S 골격이 지배하므로, 할라이드(Cl→Br→I) 치환은 ε∞·σ는 바꿔도 **bulk/shear modulus는 상대적으로 둔감**할 수 있다."

**Kraft의 판정 (정직하게, 조건부)**:
- **강한 형태(할라이드가 강성을 거의 안 바꿈)는 기각된다.** Kraft는 full-exchange(Cl→I)에서 **speed of sound −15~24 %, Debye freq −22 %**를 *실측*했다. 밀도 증가(무거운 I)를 보정해도 전단 탄성 C₄₄(∝ d·v_trans²)는 **약 −15~30 %** 감소(우리 back-of-envelope 추정: Cl d≈1.86 vs I d≈2.29 g/cm³ 보정 후). 즉 **할라이드는 격자 강성을 유의하게 무르게 만든다** — 음이온 부격자가 modulus에 *비무시* 기여.
- **약한 형태(P–S 골격이 baseline 강성을 세팅, 할라이드는 2차 변조)는 지지된다.** P–S가 뼈대 강성을 정하고, 그 위에 할라이드 분극성/크기가 **~15~24 %** 얹는 구조로 읽힌다.
- **우리에게 직접 관계있는 범위(comp1→comp2)에서는 변화가 훨씬 작다**: Cl→Cl₀.₅Br₀.₅는 **speed of sound ~−8 %, Debye ~−6 %**뿐(50 % Br만 치환). 게다가 속도 감소의 상당분은 **밀도 증가(무거운 Br) 효과**이지 순수 결합 연화가 아니다 (v∝√(C/ρ), ρ↑).

**→ 결론 (comparison_vs_ours용 판정)**: 
1. **가설의 강한 형태는 Kraft가 반증한다** — 할라이드는 modulus/speed-of-sound에 둔감하지 *않다*(full-exchange −15~24 %).
2. **우리 관심 범위(comp1→comp2, 50 % Br)에서는 소폭(~6~8 % 음속)** — "상대적 둔감"의 약한 형태는 성립. **comp2 elastic이 comp1 대비 ~5~10 % 연화(B/G 소폭↓)를 보이면 Kraft와 정합**; 만약 변화가 0이면 Kraft 트렌드와 *약한 긴장* → k-mesh·relaxed-ion·무질서 배열 점검 대상.
3. **주의**: Kraft는 **B/G를 따로 보고하지 않음**(speed of sound·Debye·C_ij만). 그러니 "Kraft가 B/G를 X % 바꿨다"는 직접 인용 불가 — 우리가 대조할 것은 **음속/Debye/C₄₄**이고, 우리 B/G 트렌드는 *같은 강성 물리량*으로서 나란히 놓는다.
4. **modelc(Cl-rich)는 Kraft 밖** — 그건 Li 공공/무질서 축이라 할라이드 교환으로 예측 불가(우리 modelc E_VRH↑는 disorder/C₄₄ 효과, Kraft의 연화와 다른 기전).

## 9. ★ polarizability의 조작적 정의 — 우리 ε∞와 같은 것을 재나?
| 질문 | Kraft | 우리 |
|---|---|---|
| "polarizability"의 정체 | **입력 변수**: 할라이드 자유이온 전자 분극성 화학 트렌드 α(Cl⁻)<α(Br⁻)<α(I⁻). **직접 측정 안 함**(α 수치 미기재), 문헌 트렌드로 라벨 | **ε∞**(DFPT/ph.x epsil) = 전자 유전율 = 전자 분극성의 거시 발현(Clausius–Mossotti). n∞=√ε∞. **직접 계산** |
| 실제로 *측정/계산*한 것 | **기계적 무름**: speed of sound(PE·RUS), Debye freq, 탄성텐서 C_ij + 구조(중성자·PDF) + σ/E_A/σ₀(임피던스) | ε∞(전자) · elastic B/G/E·C_ij(기계) · MD D/Ea |
| 물리량 종류 | 분극성=*라벨*, 무름=*측정 대상*(mechanical) | ε∞=electronic · elastic=mechanical |

**핵심 정리 (사용자 질문 직답)**:
- 우리 **ε∞ = 전자 분극성** = Kraft가 *입력 변수로 쓴 바로 그 물리량*(전자 구름 변형성). **같은 것을 잰다** — 단 Kraft는 ε∞를 *계산/측정하지 않고* 화학 트렌드로 가정만 함. 우리 ε∞ 값은 **Kraft가 안 준 정량**을 채운다.
- 그러나 Kraft의 **메커니즘에 실제로 들어가는 양은 전자 분극성이 아니라 격자 무름(spring constant / Debye / attempt frequency)** = **기계적/격자동역학 양**. 이건 우리 **elastic·phonon 체인**이 재는 것이지 ε∞가 아니다.
- 따라서: **우리 ε∞는 Kraft의 "polarizability" *라벨*과 일치(전자 분극성)하지만, Kraft가 잰 *메커니즘*(무름)과는 다른 물리량**이다. Kraft 논지 "분극성↑→무름↑"의 인과 사슬에서 **ε∞=원인(전자), elastic/Debye=결과(기계)**.
- **완전 대응하려면**: Kraft의 "lattice polarizability"(Li⁺가 지날 때 음이온 구름+골격의 *동적* 변형)는 **정적 유전율 ε₀ = ε∞ + 이온(격자)기여**에 더 가깝다. 우리 ε∞는 *전자(clamped-ion) 부분만* → **부분 대리**. Born 유효전하 + phonon 진동수(ε₀·ν_D)를 계산하면 Kraft의 무름과 정면 대응. **ε∞ 단독은 분극성 트렌드는 주지만 E_A·prefactor를 지배하는 연화 크기는 못 준다** — 이게 우리가 ε∞ 옆에 elastic/phonon을 나란히 돌려야 하는 이유.

## 10. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a,b | Li₆PS₅X F4̄3m 결정구조 + 3종 점프(intra-cage/doublet/**inter-cage=율속**) | 우리 inter-cage 율속 멘탈모델의 표준 도식 |
| 2a,b | 대표 Rietveld(중성자)·PDF G(r) fit + 불순물 | 무질서 정량 방법(음이온 점유율 자유정련) |
| **3a–d** | a↑(Vegard)·**무질서 62→0 %**·Li 48h↓/24g↑·삼각면적↑ | **무질서-소멸 곡선**(disorder→σ 레버) + 24g 전이상태 안정화 |
| 4 | inter/intra/doublet **점프거리 vs X** | 거리↑(장벽↑) vs 무름(장벽↓) 경쟁 |
| 5a,b | 아레니우스 plot + Nyquist(등가회로) | σT=σ₀exp(−E_A/kT) 피팅틀 |
| **6a** | **speed of sound(PE·RUS) vs X** — 무름의 직접 측정 | **§8 가설 판정의 원자료**(할라이드→강성 −24 %) |
| **6b** | **E_A↓ AND σ₀↓ (동시)** vs X | **핵심 반전**: 무름이 E_A·prefactor 둘 다 낮춤 |
| **6c** | **σ_RT 최적 = Cl₀.₅Br₀.₅(comp2)** + 문헌 | comp2가 최적점이라는 외부 지목 |
| 7a | Debye freq vs X (2.45→1.9×10¹² Hz) | Debye 정량(우리 phonon 체인 대조) |
| 7b | jump freq ν₀ vs Debye ν_D 상관 | 무름→attempt freq↓ 직접 증거 |
| 8 | lattice softening → oscillator 넓어짐 → E_A schematic | deck용 메커니즘 그림(초록 그림과 동일) |
| S1 | PDF 겹침(3.4 Å glassy, Cl→I 감소) | 비정질상 존재(우리 순수결정 모형 한계) |
| S2 | **Meyer–Neldel** log σ₀ vs E_A(무질서 우세시 선형) | prefactor 보상·disorder 조건 |
| S(Table)1–14 | 조성별 결정학 정확값 | §3a 표의 출처 |

## 11. Post-processing ★
- **중성자 Rietveld(GSAS-II)**: 음이온 4a/4d 점유율 자유정련 → **무질서 % 정량**. 기록 = a, occ, U_iso, R_wp/R_exp/χ².
- **Synchrotron PDF(PDFgui)**: local 구조·glassy phase 검출(3.4 Å). 기록 = G(r) fit R_w.
- **RUS(RPModel)**: 공명 스펙트럼 역산 → **C₁₁/C₁₂/C₄₄** (표로는 미공개, 속도로만 환산).
- **PE 초음파**: v_long·v_trans 직접 측정.
- **속도→Θ_D/ν_D** (eq 2–4): Debye 물성 산출.
- **임피던스→아레니우스**: E_A(기울기)·σ₀(절편). **Meyer–Neldel plot**(log σ₀ vs E_A).
- **hopping 이론 대입**(eq 6·7): prefactor 분해(ν₀·ΔS_m·a₀²), jump freq–Debye 상관.
> **우리 적용**: (1) **음이온 점유율 자유정련 = 무질서 ground truth**(우리 SQS/enumerate 검증 기준). (2) **속도→Debye→attempt freq 체인**이 우리 phonon/elastic 후속의 실험 표준. (3) **Meyer–Neldel plot**을 우리 dopant σ₀-분해(Nd prefactor 0.65×)에 그대로 적용 가능.

## 12. 적용 인사이트 (깊게)
1. **ε∞·elastic 두 체인의 문헌 정당화 확보**: 우리가 ε∞(전자 분극성)와 elastic(기계 강성)을 *나란히* 돌리는 이유가 Kraft 메커니즘 그 자체 — polarizability(원인)와 softness(결과)는 다른 물리량이니 둘 다 필요. **ε∞ 단독으로 σ/E_A를 논하면 불완전**; 무름(Debye/elastic)이 E_A·prefactor를 지배.
2. **"softer ≠ better"·prefactor 지배 = 우리 Nd 분석의 앵커**: Kraft가 σ₀ 4자릿수 변동으로 σ를 지배함을 실측 → 우리 **Nd σ-drop이 Ea 아니라 D0 prefactor(0.65×)로 설명**되는 것과 정확히 같은 물리(Meyer–Neldel/보상). deck: "문헌(Kraft)이 argyrodite에서 prefactor가 σ를 지배함을 실측, 우리 Nd 결과가 그 계열."
3. **comp2가 σ 최적점이라는 외부 예측**: Kraft가 Cl₀.₅Br₀.₅=우리 comp2를 σ 최대(~2 mS/cm)로 지목 → 우리 comp2 계산이 *어디 있어야 하는지*의 기대치. comp2 ε∞(3.80, Br로 분극성↑)·elastic(소폭 연화 예상)의 물리 스토리 확정.
4. **가설 정직화**: "할라이드가 modulus에 둔감" 강한 주장은 **금지**(Kraft가 −24 % 실측). 대신 "**P–S 골격이 baseline 강성, 할라이드는 ~15~24 % 2차 변조; 우리 comp1→comp2(50 % Br)는 ~6~8 %**"로 서술.
5. **E_A 절대값 교차검증의 방법 함정**: Kraft E_A(Cl)~0.46(=total 임피던스, GB 포함) vs 우리 MD 0.253(bulk) vs 구'Schlem 0.25'(⚠ 귀속 오류 판명 2026-07-28: DOI 10.1002/aenm.201903719는 Li3MCl6 논문 — LPSCl 0.25/0.22의 원전 미상(별도 확보 필요)) vs Rao2011 0.38(임피던스) — **방법마다 갈림**. bai2020이 comp1 0.253≈Schlem 0.25로 정합 언급한 것과 Kraft 0.46은 *다른 측정층*(total vs bulk). **우리 MD는 bulk 값이라 Kraft total과 직접 비교 금지, 방향만.**
6. **I는 전도 레버가 아님**: I 저전도 원인 = 격자 무름이 아니라 **무질서 소멸 + prefactor 붕괴**. Rao2025(I=상안정/계면 레버, 전도 아님)·Rao2011과 3중 정합.
7. **무질서 실측 ground truth**: Kraft의 Rietveld 점유율(Cl 62 %)이 우리 modelc SQS/enumerate 무질서 배열의 실험 검증 기준.

## 13. 인용 가능 문장 (deck/paper용)
- "Kraft et al. show experimentally that halide substitution in Li₆PS₅X softens the lattice (speed of sound −24 %, Debye frequency −22 % from Cl to Br₀.₅I₀.₅), lowering both the migration barrier *and* the Arrhenius prefactor, so the conductivity optimum sits at intermediate stiffness Li₆PS₅Cl₀.₅Br₀.₅ (= our comp2)."
- "The 'polarizability' Kraft tunes is the anion's electronic polarizability (our ε∞); what he *measures* is the mechanical softness (our elastic/Debye chain) — the two are correlated, not identical, so our ε∞ and elastic runs are complementary, not redundant."
- "Our prefactor-dominated Nd conductivity drop (constant E_A, D₀ ×0.65) is the Meyer–Neldel physics Kraft reports for the argyrodite series (σ₀ spans 10³–10⁷ KScm⁻¹)."
- "Halide substitution is *not* modulus-neutral (Kraft: −15–24 % full exchange); but over our comp1→comp2 window (50 % Br) the softening is modest (~6–8 % in sound speed), part of it a density effect."

## 14. 주의 / 한계 (over-claim 방지)
- **속도·Debye·E_A·σ·prefactor·점프거리는 SI에 표가 없음**(2026-07-24 SI 15 pp 실물 감사로 **확정** — SI는 결정학표 S1–S14 + Fig S1·S2뿐) → 전부 **Fig 4/6/7·S2 figure-read(≈)**, ±수 % 판독오차. 정량 인용 시 "figure-read" 명시.
- **E_A = total(bulk+GB) 임피던스** — bulk/GB 미분리(저자 명시). 우리 bulk MD Ea와 절대 비교 금지.
- **DFT 없음** — 이 논문엔 우리 방법(functional/k/무질서) 대조점 없음. 순수 실험 앵커.
- **B/G 미보고** — Kraft는 speed of sound·Debye·C_ij만. "Kraft B/G X %" 인용 불가.
- **α(폴라리자빌리티) 수치 미기재** — 트렌드(Cl<Br<I)만. 구체 ų 값은 교과서(이 논문 아님) → 인용 시 출처 구분.
- **C₄₄ ~−15~30 % 밀도보정**은 *우리 추정*(Kraft가 C_ij·밀도 표 미공개) — Kraft 보고값 아님.
- **순수 I 구조모형**: Kraft는 I도 F4̄3m cubic; 우리 comp5=별도(rhombo) 모형 → 구조 대조 주의.
- **85 % 치밀 시료**(PE) — 완전 치밀이면 속도 약간 높을 것(저자 인정). 트렌드는 유효.
- 우리 modelc(Cl-rich)·B₂O₃·LPSOCl 계열은 **Kraft 범위 밖**(할라이드 교환 축만).

## 15. 기법 용어 미니사전
- **Speed of sound(PE)**: pulse-echo로 종파(v_long)·횡파(v_trans) 전파속도 측정 → 결합강성(∝√(C/ρ))의 직접 척도. 높을수록 강성.
- **RUS(Resonant Ultrasound Spectroscopy)**: 시료 공명주파수 스펙트럼 역산 → 탄성텐서 C₁₁/C₁₂/C₄₄ 전체. couplant 불필요(분해성 시료 유리).
- **Debye frequency ν_D / temperature Θ_D**: 격자 최고 phonon 진동수/온도. 음속에서 eq 3·4로 환산. attempt frequency ν₀의 근사치로 씀.
- **Attempt frequency ν₀**: 이동 이온이 자리에서 진동하며 장벽을 "때리는" 빈도(TST). eq 7 = (1/a₀)√(2E_A/M). prefactor에 선형 기여.
- **Prefactor σ₀**: σT=σ₀exp(−E_A/kT)의 절편. carrier·점프거리²·attempt freq·이동엔트로피 e^{ΔS_m/k} 곱(eq 6).
- **Meyer–Neldel rule(보상법칙)**: 한 물질군에서 E_A↓가 σ₀↓와 선형 상관(log σ₀ ∝ E_A) — 장벽 이득이 prefactor 손실로 부분 상쇄.
- **Anion site disorder**: 할라이드(4a)와 free-S²⁻(4d)가 서로 자리를 바꿔 앉는 비율. inter-cage 장벽을 낮춰 superionic 유발. 반경이 비슷해야(Cl/Br≈S) 발생.
- **Polarizability(분극성)**: 전기장에 전자구름이 변형되는 정도(α). Cl⁻<Br⁻<I⁻. 거시 발현 = 전자 유전율 ε∞(=n∞²).
- **Inter-cage jump**: 이웃 Li 케이지 사이 hop = 장거리(dc) 수송 율속 단계. intra-cage/doublet는 빠름(non-limiting).

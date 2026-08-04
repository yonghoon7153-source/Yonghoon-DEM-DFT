# Electronic Localization Enables Long-Cycling Sulfides-Based All-Solid-State Lithium Batteries — Dewen Wang / Chong Liu (Angew. Chem. Int. Ed. 2025, VIP)

> slug `wang2025_electronic_localization_yo_argyrodite` · DOI `10.1002/anie.202501411` · type `exp + DFT/BVSE 보조` · PDF `2c40956f(본문 11p)` + `459bf7a1(SI 34p)` · digested `2026-08-04` · **2차 패스(본문 그림 픽셀 독립 검증) `2026-08-04` → §18** · status ✅
> elements: Li, P, S, Cl, Y, O
> methods: DFT, BVSE, DOS, PDOS, ELF, LOBSTER, XPS, Raman
> **저자**: Dewen Wang⁺, Chong Liu⁺(공동1저자), Ruoyu Wang, Tianran Zhang, Butian Chen, Tenghui Wang, Qi Lu, Wen Yin(CSNS 동관), **Xiangfeng Liu***(UCAS 베이징) · Angew 2025, 64, e202501411 (2025-01-17 접수 → 03-09 온라인, VIP)

---

## 0. 이 digest를 읽는 법
이 논문은 **"Li₆PS₅Cl(=우리 comp1)의 PS₄³⁻ 사면체에 Y³⁺(P자리)+O²⁻(S자리)를 소량(x=0.05) 넣어 'S 전자를 국재화'시키면 Li 금속 계면 환원분해가 억제되어 장수명이 된다"**는 음극(환원)-계면 논문이다. 실험 성능 데이터(CCD 0.7→1.5 mA/cm², 대칭셀 4800 h, LCO 풀셀 1300 cycle)는 인상적이지만, **계산 사슬(BVSE 장벽 1.11→0.61 eV, ELF/PDOS/Madelung "electronic localization")은 검증 밀도가 낮고 내부 모순이 많다**. 우리 관심사는 (a) BVSE를 σ 서사에 쓰는 방식이 우리 규율과 정면 충돌하는 지점, (b) Rietveld 산물이 BVSE에 그대로 유전되는 구조, (c) Y³⁺ 자리 배정이 우리 M³⁺ cascade site-rule(Li_24g)과 반대인 점이다. §6·§7·§8·§13이 그 비판 코어.

> ⚠ **조성 표기 주의**: 본문 herein 문장은 "Li6.1P0.95Y0.05**S4.25O0.75**Cl"로 쓰지만, 일반식 Li₆₊₂ₓP₁₋ₓYₓS₅₋₁.₅ₓO₁.₅ₓCl에 x=0.05를 넣으면 **S4.925O0.075**가 맞고 SI 표들(Table S1–S5 캡션)도 S4.925O0.075다. **본문 S4.25O0.75는 오타**(그 값은 x=0.5에 해당). 이 digest는 **Li6.1P0.95Y0.05S4.925O0.075Cl**(약칭 LPSC-YO)로 통일. (기존 INDEX 표기 S4.25O0.75는 본문 오타를 그대로 옮긴 것.)

## 1. 한 줄 요약
Li₆PS₅Cl에 Y₂O₃로 Y³⁺→P⁵⁺(4b)+O²⁻→S²⁻(16e) 5% 공치환(Li6.1P0.95Y0.05S4.925O0.075Cl) → σ 2.75→3.53 mS/cm(+28%)·Ea 0.375→0.34 eV·σ_e 6.33→1.55×10⁻⁷ S/cm(4×↓)·H₂S ~0.47→~0.30 cm³/g, 그리고 **Li 금속 계면에서 Li₂S/Li₃P 생성 절반 이하 + in-situ Li₂O 보호층** → CCD 1.5 mA/cm², 대칭셀 >4800 h(0.1 mA/cm²), LCO/Li-In 0.5C 1300 cycle "100%" — 메커니즘은 **"Y-4d/S-3p d–p 혼성이 S 전자를 국재화(ELF/PDOS)+Madelung 강화(−166.51→−175.07 eV/atom)해 Li→S 전자전달을 어렵게 한다"**는 전자구조 서사로 포장.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 비교쌍 | **LPSC = Li₆PS₅Cl (=우리 comp1 조성)** vs **LPSC-YO = Li6.1P0.95Y0.05S4.925O0.075Cl** (x=0, 0.02, 0.05, 0.08, 0.1 스캔, 0.05가 최적=고용한계) |
| 문제의식 | LPSC 2대 약점 = ① Li/LPSC 계면 연속 분해+덴드라이트(좁은 전기화학창), ② 대기 불안정(H₂S) |
| 전략 | "electron localization strategy": PS₄³⁻ 중심금속을 바꿔(d⁰ Y³⁺) **d–p 혼성으로 S 전자 국재화** → Li 금속과 S의 반응 억제. O는 HSAB hard-acid 짝으로 대기안정성+Li₂O interphase 담당 |
| 선행 대비 | soft-acid 도핑(Sb/Sn/In/Bi)·halide 치환(Adeli)과 달리 "사면체 중심 원자 교체→전자구조 재구성"을 전면에 |
| 셀 구성 | 분리막 SE=LPSC(-YO), **양극 복합재 catholyte는 별도의 LiDFOB-coated Li5.5P(Yx)S4.5Cl1.5**(SI 표기 모호, §13-11), 음극 Li 또는 Li-In |

## 3. 핵심 물성 (수치 총정리) — 전부 소환값
| 물성 | LPSC | LPSC-YO | 출처/조건 |
|---|---|---|---|
| σ (RT, EIS·In 차단전극) | ~2.75 mS/cm (그림 판독) | **3.53 mS/cm** (본문 명시) | Fig 2c; 100 mg·φ10 mm·800 µm 펠릿 |
| Ea (25–60 °C Arrhenius) | ~0.375 eV (그림 판독) | **0.34 eV** (본문 명시) | Fig 2b,c |
| σ_e (DC polarization 0.1–0.5 V) | **6.33×10⁻⁷ S/cm** | **1.55×10⁻⁷ S/cm** (4×↓) | Fig S9,S10 |
| BVSE "장벽" | **1.11 eV** | **0.61 eV** ("절반") | Fig 2d,e — §6에서 해부 |
| CV 산화 onset (Li/SE/SE+C, 0.1 mV/s) | >2.48 V 산화전류 큼 | 동일 onset, 전류↓ | Fig 2f |
| CV 환원 전류 (<1.83 V) | 큼 (P⁵⁺→P³⁻, S⁰→S²⁻ 라벨) | **유의미하게 작음** | Fig 2f |
| H₂S (150 mg, 75% RH, 60 min) | ~0.47 cm³/g (그림 판독) | **~0.30 cm³/g** | Fig 2g |
| CCD (Li 대칭셀) | 0.7 mA/cm² | **1.5 mA/cm²** | Fig 3a,b |
| 대칭셀 수명 0.1 mA/cm² | ~1000 h 후 과전압 급증 | **>4800 h** (본문; Table S6엔 4300) | Fig 3c |
| 대칭셀 0.5 mA/cm² | 조기 단락 (Fig S15) | **>1300 h** (Table S6엔 1350) | Fig 3d |
| GEIS-DRT 파괴 용량 | 1.6 mAh/cm²에서 단락 신호 | ≥2.4 mAh/cm² 안정 | Fig 3e–h |
| 계면 Li₂S 비율 (XPS S 2p 면적) | **21.3%** | **9.9%** (+Y-S-Li 6.6%) | Fig S17c,d |
| 계면 Li₃P 비율 (P 2p) | **9.0%** | **3.6%** (+P-O 5.4%) | Fig S17a,b |
| Li₂O (O 1s 528.5 eV) | — | **검출** (LiO⁻ SIMS 3D 균일) | Fig 4c,d |
| LCO/Li 0.1C 100cyc | 100.1 mAh/g, 77.2% | **112.0 mAh/g, 89.6%** | Fig 6a |
| LCO/Li-In 0.5C | 85.7% @400cyc (그림 84.9%) | **91.9 mAh/g, "100%" @1300cyc** | Fig 6d |
| rate 0.1→1.0C (Li-In) | 118.6→**23.6** mAh/g | 122.2→**62.5** mAh/g | Fig 6b |
| 격자 a (XRD Rietveld) | 9.84764 Å | **9.84824 Å (+0.0006 Å = +0.006%)** | §13-1 참조 |
| Raman PS₄³⁻ | 427.18 cm⁻¹ | 동일 (shift/splitting 없음) | Fig 1e |
| 밴드갭 | 본문·SI **미보고** → **2차 패스 그림 실측 ~2.1 eV** | 실측 **~2.55 eV** | Fig 5e 픽셀(§18.2) — DOS-threshold 판독, ±0.2–0.3 eV |

## 4. 재료·실험 방법
- **합성**: Li₂S(Alfa)+P₂S₅+LiCl+**Y₂O₃**(Aladdin, 99.9%) → 유성밀 500 rpm 10 h(지르코니아 1:40) → 펠릿, 석영관 밀봉 → **550 °C 10 h**(3 °C/min), 전 과정 Ar GB.
- **XRD**: Smartlab Cu Kα 10–70°, **FullProf** Rietveld. **NPD: CSNS MPI**(TOF, 동관 산란중성자원; 공저자 Wen Yin=시설), **GSAS-II**("GASA II"로 오기).
- Raman inVia 532 nm / XPS ESCALAB 250Xi(+Ar⁺ depth 0–150 s) / SEM SU8010+EDS / **TOF-SIMS PHI nanoTOF II**(3D 재구성) / ICP-OES.
- **전기화학**: PARSTAT 4000("PARSRAT" 오기). EIS 0.1 Hz–1 MHz·10 mV·25–60 °C. σ_e = DC 분극 0.1–0.5 V 계단. CV 0–5 V·0.1 mV/s(Li/SE/SE+C). 대칭셀: PEEK φ10, SE 300 MPa + Li foil 10 MPa. **GEIS+DRT**(0.2 mAh/cm² 간격).
- **풀셀**: catholyte=**LiDFOB-coated Li5.5P(Yx)S4.5Cl1.5**:LCO=3:7(6–10 mg), 분리막 SE 100 mg, 음극 Li 또는 Li-In, **무용매 dry**. 파우치(dry process)로 shear/puncture 시연.
- **대기안정성**: 밀폐 챔버 습도 제어, 75% RH, 60 min, H₂S 센서 기록.

## 5. 결과 — 섹션별 상세

### 5.1 구조 (Fig 1, S1–S7, Table S1–S5)
- XRD 전 조성 F-43m argyrodite; **x≥0.08에서 Li₂S·LiYS₂·미지상 불순물** → 고용한계 x=0.05.
- Rietveld: LPSC Rp 3.40/Rwp 4.96%; **LPSC-YO Rp 3.55/Rwp 5.41%**. NPD: LPSC Rw 3.96/GOF 5.71; **YO Rw 4.792/GOF 7.42** (GOF 7은 그리 좋은 fit이 아님).
- 사이트 모델(그들 setting): P/Y=4b, 자유음이온 자리=**4a+4d**(관례 4a+4c와 원점 선택 차이), Li=48h 단일 자리, S(PS₄)=16e, **O도 16e**(즉 PS₄→PS₃O 사면체 산소), Cl/S 자리혼합 4a 38.5%/4d 61.5% — 수치 자체는 Kraft/Adeli류 ~60/40 site-inversion 그림과 정합.
- 격자: +0.0006 Å "팽창"을 Y³⁺(그들 표기 162 pm)>P⁵⁺(110 pm) 근거로 설명 — §13-1(팽창이 사실상 0)·§13-2(반경 수치가 이온반경이 아님) 참조.
- XPS: P 2p에 PS₄ 131.8/132.8 eV 외 **"P–O" 신규 피크(본문 131.1/131.9 eV — 그림에선 ~133.5–134 eV 쪽. 본문 수치가 오타로 보임, §13-9)**; S 2p 160.1/161.1 eV = **Y–S 결합**; O 1s 531.34 eV = Li–O–P. Raman PS₄ 427.18 cm⁻¹ 불변.
- HRTEM 0.309 nm 격자무늬 vs Li₇PS₆ PDF (311) 0.297 nm — "약간 팽창"으로 설명하나 **+4%는 XRD의 +0.006%와 양립 불가**(§13-3). SAED (331)/(422) 다결정 링. EDS/ICP: Y·O 균일, 조성 "정합"(ICP 재계산 시 Li/(P+Y)≈7.1로 nominal 6.1보다 16% 높음 — §13-8).

### 5.2 이온전도 (Fig 2a–c, S8)
σ가 x=0.05까지 ↑ 후 ↓(불순물), Ea는 반대 경향. 3.53 mS/cm·0.34 eV가 최적. 해석: **① 큰 Y³⁺가 수송 채널 확장, ② aliovalent(Y³⁺→P⁵⁺)로 Li⁺ 2개/Y 추가(Li6+2x) → carrier↑**(NPD 근거 주장, §7-3에서 반박). "O 도핑은 원래 σ에 해로운데 Y가 상쇄"는 인정.

### 5.3 BVSE (Fig 2d,e + S11) — §6에서 전수 해부
LPSC 대비 LPSC-YO 경로 "확장"(빨간 원=O7 부근·Y2/Li52 부근), 60 Å 경로 에너지 랜드스케이프 최대 **1.11 → 0.61 eV** "절반".

### 5.4 σ_e (Fig S9, S10)
6.33×10⁻⁷ → 1.55×10⁻⁷ S/cm. "낮은 σ_e → 덴드라이트 억제" 서사. ⚠ 그러나 **베이스라인 6.33×10⁻⁷은 타 그룹 pristine LPSC 대비 ~60–200× 높음**(소환: [Adeli] 3×10⁻⁹, [Taklu] 8.75×10⁻⁹, [Yang25] 2.59×10⁻⁹, [Li25] 1.02×10⁻⁸ S/cm) — 개선 후 값도 남들 pristine보다 높다. §13-6.

### 5.5 CV (Fig 2f)
Li/SE/SE+C 반쪽셀 0–5 V. 산화(>2.48 V, 라벨 S²⁻→S⁰·P⁰→P⁵⁺)와 저전압 재산화(P³⁻→P⁰), 환원(<1.83 V, S⁰→S²⁻·P⁵⁺→P³⁻) 모두 LPSC-YO 전류↓. **onset 위치는 사실상 동일**(전류 크기만 차이) — "산화 안정성 개선"이 아니라 **분해 전류 감소**로 읽어야 함. 2.48 V는 우리 grand-potential 2.256 V(S-limited)+과전압과 정합(축 B①), Son2025 "<2.5 V"와도 일치.

### 5.6 대기안정성 (Fig 2g, S12, S13)
H₂S ~0.47→~0.30 cm³/g (75% RH). HSAB(경산 O가 S 자리 → 물과 친화 감소) + DFT 보조:
- **흡착E** (slab "end surface", ΔE_ad=E(unit+H₂O)−E_surf−E_H₂O): PS₄ **−1.69** / YS₄ **−0.92** / PS₃O **−0.78 eV** → 도핑 유닛이 물을 덜 붙잡음.
- **가수분해E** (사면체 유닛 반응): PS₄+H₂O→PS₃O+H₂S **−1.84** / PS₃O+H₂O→PS₂O₂+H₂S **−1.75** / **YS₄+H₂O→YS₃O+H₂S +4.13 eV**(강한 흡열). ⚠ 고립 사면체 수준 반응식 — 전하보상·격자환경·엔트로피 없음, +4.13 eV는 화학적으로 과대(§13-7). 방향성 논거로만.

### 5.7 Li 대칭셀·CCD·DRT (Fig 3, S14–S16)
- CCD 0.7→**1.5 mA/cm²**. 0.1 mA/cm²: LPSC ~1000 h에서 과전압 급증(공극+Li₂S/Li₃P 축적) vs YO **>4800 h**; 0.5 mA/cm²: LPSC 조기 단락(Fig S15) vs YO >1300 h. Cu/Li 반쪽셀: LPSC 83 h 단락 vs YO >100 h(120 h 표시).
- **GEIS-DRT**: τ≈10⁻⁶ s(전해질)·10⁻⁴ s(SEI) 피크가 LPSC는 1.6 mAh/cm² 스트리핑에서 소실(=연질단락), YO는 2.4 mAh/cm²+까지 유지. DRT로 "무엇이 먼저 죽는지"를 시간상수로 분리한 좋은 사례 — 차용 가치.

### 5.8 계면 화학 (Fig 4, S17, S18)
- **XPS depth(0–150 s Ar⁺)**: Li/LPSC → Li₂S(160.3/161.6 eV)·Li₃P(130.2 eV)가 깊이에 따라 **증가**(연속 분해); Li/LPSC-YO → 소량+깊이 무관, PS₄/YS₄ 피크 유지, **Li₂O 528.5 eV 검출**.
- 정량(S17 파이): Li₂S 21.3→9.9%, Li₃P 9.0→3.6%.
- **TOF-SIMS 3D**: YO 계면에 LiO⁻ 균일층(=Li₂O interphase), LiS⁻·Li₂P⁻는 LPSC 쪽이 밀집. SEM: LPSC 사이클 후 Li 표면 균열+부산물 vs YO 평탄.
- 종합: **환원분해 억제 + Li₂O 배리어**가 실험적으로 잘 짜인 부분. (단 Li₂O가 O 0.075/f.u.의 소량에서 "층"으로 나올 물량인지 정량 없음.)

### 5.9 DFT 메커니즘 (Fig 5, S19) — §8에서 사슬 해부
계면 슬랩 이완(LPSC의 PS₄ 붕괴 vs YO의 YS₄ 유지) → ELF(S 국재화) → PDOS(P-p/S-p p–p 혼성 vs Y-d/S-p d–p 혼성) → Madelung(−166.51 vs −175.07 eV/atom) → "전자 이동 어려움 → 계면 안정" 도식(Fig 5i,j).

### 5.10 풀셀 (Fig 6, S20–S22)
LCO/Li 0.1C: 112.0 mAh/g·89.6%/100cyc vs 100.1·77.2%. LCO/Li-In 0.5C: **91.9 mAh/g 시작, 1300 cycle "100%"** vs LPSC 85.7%/400(그림 84.9%). 0.1C 300cyc 89.7%(S20)·0.2C 350cyc 94.1%(S21). rate 1C에서 62.5 vs 23.6 mAh/g. 파우치 dry-process, 절단/천공 후에도 LED 점등. Table S7에서 11개 문헌 대비 최장 cycle 주장. ⚠ "100%/1300cyc" 정독: 0.5C 용량 91.9는 0.1C 용량(122)의 75%라 **낮은 활용률 셀은 열화가 늦게 보이는** 전형 + catholyte는 LiDFOB-coated 별도 SE(§13-11) → 이 수치는 "분리막+음극 축" 개선의 증거로만.

---

## 6. ★ BV/BVSE 워크플로 전수 추적 (요청 #1)

### 6.1 무엇으로 계산했나 (코드·파라미터)
- SI 원문: *"migration pathways of mobile Li⁺ were calculated based on the BVSE method and **Voronoi decomposition**, carried out on the **computing and data platform for electrochemical energy storage materials**[ref=Wong/Adams, Chem. Mater. 2021, 33, 625 = softBV **BVPA** 논문]. For comparison … also calculated using **SoftBV** software with a resolution of **ca. 0.1 Å**."*
- 즉 ① 이름은 "플랫폼"(문구는 상하이대 계열 전기화학 저장재료 플랫폼과 유사)인데 인용은 Adams softBV-BVPA 논문 — **두 트랙 모두 사실상 softBV 파라미터 계열**로 보임. ② 격자 해상도 ~0.1 Å(우리 0.25 Å보다 촘촘). ③ **스크리닝 인자·컷오프·Coulomb 항 설정·등가면 iso-level·경로 추출 알고리즘·장벽 정의(경로 최대값?) 전부 미공개** → 재현 불가 수준.
- "Voronoi decomposition"은 간극 네트워크 후보 자리 추출용(플랫폼 워크플로의 표준 전처리)으로 읽히며 결과 그림엔 별도 표시 없음.

### 6.2 입력 구조 — Rietveld 산물인가? (그렇다, 그리고 그게 문제)
- BVSE 그림(Fig 2d,e·S11)의 셀·원자 라벨(Li13…Li59, **Y2, O70/O7**)은 **정련 셀(a≈9.848 Å, F-43m)에 부분점유 Li 48h 자리를 전부 그려놓은 표시**와 일치. 즉 입력은 Table S2/S4의 Rietveld/NPD 구조다.
- **부분 점유 처리**: softBV는 부분점유 가중을 지원하지만, LPSC-YO 그림에 **이산 원자 라벨 Y2·O70**이 명시되어 있으므로 Y/O는 **가중이 아니라 명시적(정수 점유) 원자로 decorate한 정렬 스냅샷**일 가능성이 매우 높다. 근거 2: 점유 가중(Y 0.05·O 0.019)으로 넣었다면 장벽이 1.11→0.61 eV로 **2×나 움직일 수 없다**(섭동 가중 5% 이하).
- 그 스냅샷의 농도: 관례 셀(4 P/셀)에 Y 1개면 **P 사이트의 25%** — 실험 5%의 5배. O도 명시 원자 개수 불명(라벨 O70은 표시번호일 뿐). **몇 개를 어디에 넣었는지, 배열을 몇 개 시도했는지 일절 없음** → 단일 정렬 스냅샷.

### 6.3 Energy vs Reaction Coordinate (1.11 vs 0.61 eV)의 정체
- 60 Å 길이 경로를 따라 **BVSE 랜드스케이프 값을 찍은 것**(NEB 아님, DFT 아님). LPSC는 0.2–1.11 eV 톱니, YO는 0.2–0.61 eV로 평탄화. "장벽=경로 최대값"으로 읽힘.
- **빨간 원 2개**(Fig 2e): O7 부근(왼쪽)과 Y2/Li52-Li59 부근(중앙) — 등가면이 그 지점에서 이어짐="경로 확장"의 시각 근거. 본문은 "red line"이라 쓰나 그림엔 원(circle)만 있음.
- **자기 실험과의 불일치**: 그들 실측 Ea는 0.375/0.34 eV. BVSE 1.11/0.61 eV는 각각 3.0×/1.8× 과대이고, 심지어 **개선 후 BVSE 값(0.61)이 개선 전 실측(0.375)보다 크다**. BVSE 절대값은 수송 Ea가 아니라는 것을 스스로 보여주는 셈 — 그런데 본문은 "migration energy barrier … reduced by half"로 정량 서사에 사용.

### 6.4 "Y³⁺가 채널을 넓힌다" 주장 사슬 — 단계별 판정
| 단계 | 그들 근거 | 판정 |
|---|---|---|
| ① Y³⁺(162 pm)>P⁵⁺(110 pm) → 격자 팽창 | a +0.0006 Å (+0.006%) | ✗ 사실상 0(§13-1) + 반경 수치는 이온반경 아님(§13-2). Shannon 이온반경으로도 Y³⁺(VI) 0.90 Å vs P⁵⁺(IV) 0.17 Å로 대비는 실재하나 "격자 팽창" 증거는 없음 |
| ② aliovalent → Li 2개/Y 추가 → carrier↑ | "NPD 정련으로 Li↑ 확인" | △ NPD Li 점유 표가 그 주장을 지지하지 못함(§7-3): LPSC 0.3851(=Li4.6/f.u.?) → YO 정확히 0.5000(고정값 냄새) |
| ③ BVSE 장벽 절반 + 경로 확장 | 1.11→0.61 eV, O7/Y2 빨간 원 | ✗✗ 과대 표현: (a) 정렬 스냅샷 아마 25% Y로 과도핑, (b) **P⁵⁺→Y³⁺는 양이온 전하가 −2 되므로 BVSE의 정전 반발항이 국소적으로 낮아지는 건 반쯤 자동**(방법 내재 편향 — 낮은 전하 치환은 거의 언제나 국소 장벽을 낮춘다), (c) 절대값이 자기 실험과 3× 불일치, (d) 배열 통계 없음 |
| ④ 실측 σ +28%·Ea −0.035 eV | EIS | ✓ 실측 자체는 사실. 다만 +28%는 벌크 효과인지 입계/치밀화 효과인지 분리 안 됨 |
- 요약: **실험 σ 개선(소폭)은 신뢰, 그 기전을 설명한다는 BVSE 정량 서사는 방법 내재 편향+단일 스냅샷+자기 불일치로 근거 약함**.

## 7. ★ Rietveld 산물 의존성 — 정련 가정이 어떻게 유전되나 (요청 #2)

### 7-1. 점유율 표가 "정련"이 아니라 "고정"으로 보인다
- Table S2(XRD-YO): P/Y 점유가 **정확히 0.95/0.05**(nominal), O 16e도 **정확히 nominal 0.01875**, Cl 4a/4d **0.385/0.615는 LPSC와 자릿수까지 동일** → Y·O·Cl 점유는 **정련 변수로 풀지 않고 nominal로 constrain**한 것. 그러면 "XRD·NPD 정련이 Y@P 자리를 확인했다"(본문)는 **순환**이다: Y를 4b에 넣고 fit이 안 나빠졌다는 것뿐, 자리 판별력이 없다(5% Y·경X선 대비면 XRD로는 원래 거의 못 가른다).
- Table S1/S2의 Occ 열은 **행마다 관례가 다르다**: P·Cl·S는 FullProf식 m/M(예: 4b 만점 0.04167)인데 **Li 행은 직독 분율**(0.49589≈½)로 읽어야만 물리적으로 말이 됨(m/M로 읽으면 Li 47.6개/셀=Li11.9/f.u.). 표만으로 자기일관 해석이 불가능 — BVSE 입력을 남이 재현할 수 없다.

### 7-2. XRD vs NPD의 O 점유 16× 충돌
- **XRD(S2): 16e에 S 0.981/O 0.019** (nominal과 일치·고정) ↔ **NPD(S4): S 0.7000/O 0.3000**. 같은 시료에서 O 함량이 **16배** 다르다. NPD가 맞다면 조성식 자체(O0.075)가 무너지고(O≈1.2/f.u.), 고정값이라면 왜 0.30인지 설명이 없다. **본문은 이 충돌을 언급조차 안 함**. O 자리·양은 BVSE(Li–O R0=1.466 Å, 강한 국소 흡인)와 "PS₃O 유닛" 서사의 뿌리라, 이 불확정이 그대로 계산에 유전된다.
- S2(16e) 좌표도 NPD에서 0.11555→0.10452로 이동(P–O 단축과 정합) — 이건 그럴듯한 부분.

### 7-3. Li 자리 — 경원소 정련의 전형적 약점이 그대로
- 단일 48h 모델(24g/T5a 분리·간극 T2 없음). NPD Li 점유: LPSC **0.3851**(직독이면 Li 4.62/f.u. — Li6이어야 할 시료에서 23% 결손), YO **정확히 0.5000**(=Li 6.00/f.u., 소수점 4자리 반올림 없는 값=고정 냄새). 본문 "증가한 Li⁺ 농도를 NPD 정련으로 확인"의 실체가 이 두 숫자라면, **carrier↑ 주장의 실험 근거는 취약**하다(0.3851 자체가 비물리적이므로 상대비교 불능).
- ADP(U_iso) 미보고, XRD+NPD joint refinement 아님, Li-nuclear density(Fourier) 맵 없음.

### 7-4. 민감도 검증 여부
- **중성자: 있음**(CSNS MPI TOF — Li·O 감도 확보 시도 자체는 올바름). 그러나 위처럼 산출표가 상호모순이라 검증 효과 상실.
- **DFT 이완 교차검증: 사실상 없음** — 오히려 VASP 모델은 **O를 Cl 자리에 치환**(SI: "one Y and two O … for one P atom and two Cl atoms")해서 **정련 모델(O@16e=사면체 산소)과 다른 화학**을 계산했다. 즉 실험 구조↔DFT 구조↔BVSE 구조가 서로 다른 O 배치를 쓴다(§13-5). BVSE 민감도(배열·점유 흔들기) 테스트 없음.

## 8. ★ "Electronic localization" 주장 사슬 해부 (요청 #3)

### 8.1 무엇을 계산해서 "국재화"를 보였나
| 증거 | 내용 | 논평 |
|---|---|---|
| ① 계면 슬랩 이완 (Fig 5a,b / S19) | Li 슬랩+SE 슬랩 초기/최적화 구조: LPSC는 계면 PS₄가 분해(Li₂S·Li₃P 생성 방향), YO는 **YS₄가 원형 유지** | 0 K 단일 배열 geometry-opt **한 쌍**. 반응E·궤적·통계·슬랩 사양(면·두께·진공·정합변형) 전부 미보고. Y를 **계면 최상층에 배치**(S19b)한 모델 선택 자체가 결과에 유리 |
| ② ELF (Fig 5c,d) | LPSC: P·S 주위 비편재 / YO: **S 위에 강한 국재** | 실은 "P–S는 공유결합, Y–S는 이온결합"이라는 교과서 사실의 ELF 번역. 국재화=신규 발견이라기보다 재명명 |
| ③ PDOS (Fig 5e,f) | LPSC: VBM 근방 P-p/S-p **p–p 혼성**; YO: **Y-4d/S-3p d–p 혼성**(오비탈 분해 d_xy…d_x²−y²) | "at the Fermi level"은 부정확(절연체 — VBM 근방을 뜻함). d⁰ Y³⁺의 d 성분이 VB에 소량 섞이는 건 이온결합에서 일반적. 혼성→"전자 전달 어려움"의 정량 다리 없음 |
| ④ Madelung (Fig 5g,h; LOBSTER+Glasser) | PS₄ 유닛 −166.51 vs YS₄ **−175.07 eV/atom** → "Y–S Coulomb 강함→S가 단단히 묶임" | 형식전하가 다른 유닛(PS₄³⁻ vs YS₄⁵⁻)의 정전에너지 직접 비교 — 더 음전하인 유닛의 Madelung이 더 깊은 건 상당 부분 자명. 전하 partition(Löwdin?) 관례 미보고 |
| ⑤ 도식 (Fig 5i,j) | p–p="easy transfer electrons"→반응 / d–p="hard transfer"→안정 | 만화 수준 — 전자전달 장벽·redox 준위·계면 정렬(band alignment) 계산 없음 |

### 8.2 장수명과의 연결 고리(그들 논리)와 비약 지점
- 논리: S 전자 국재화 → Li 금속이 S에서 전자를 얻어 PS₄를 부수는 반응 억제(Li₂S/Li₃P↓, XPS/SIMS 정합) + σ_e 4×↓(전자 누설↓→SE 내부 Li 석출↓) + Li₂O interphase(전자절연 배리어) ⇒ 덴드라이트↓·4800 h·1300 cycle.
- **비약 1 — 열역학 부재**: 환원분해 억제를 말하려면 Li에 대한 반응에너지/convex hull(예: 우리 grand-potential: comp1 0 V → Li₃P+Li₂S+LiCl, 환원한계 1.242 V)이 필요한데 **분해 열역학 계산이 하나도 없다**. 5% Y가 벌크 환원 전위를 바꿀 수 없다는 게 오히려 열역학 상식이고, 실제 XPS에도 Li₂S/Li₃P가 (적지만) 있다 — 즉 개선은 **kinetic/passivation**인데 서사는 intrinsic 전자구조로 포장.
- **비약 2 — Y 효과와 O 효과 미분리**: Li₂O interphase는 O 도핑의 몫, "국재화"는 Y의 몫인데 **Y-only·O-only 대조 시료가 없다**. 성능 개선의 어느 몫이 어느 축인지 실험적으로 분리 불가.
- **비약 3 — 국재화↔σ_e 4×↓ 연결 없음**: σ_e는 wide-gap SE에서 결함/불순물 지배(외인성)인데, 벌크 혼성 그림으로 4× 차이를 설명하지 않음(그냥 병렬 나열).
- **비약 4 — 국재화 정량 지표 부재**: Bader/Löwdin 전하 변화량, S-3p 밴드폭/중심 이동, **ICOHP(P–S vs Y–S)** 같은 표준 정량이 없다. 특히 methods에 **COHP·COBI·ICOHP·ICOBI를 계산했다고 명시**해놓고 **본문·SI 어디에도 결과가 없다**(§13-4) — P–S 공유결합이 Y–S보다 강하게 나와(통상 |ICOHP| P–S≫Y–S) 서사와 어긋났을 가능성을 합리적으로 의심할 수 있는 대목.
- 공정하게: **계면 생성물 관찰(XPS depth+SIMS 3D+DRT)은 촘촘**하고, "덜 분해된다"는 현상 자체는 설득력 있음. 약한 것은 그 **원인을 '전자 국재화'라는 단일 전자구조 서사로 귀속**시키는 부분.

## 9. DFT/계산 방법 ★ (재현용 표 — 요청 #4)
| 항목 | 내용 (SI 원문 기준) | 재현 관점 논평 |
|---|---|---|
| code | VASP (**인용이 VASPKIT 논문[CPC 2021, 267, 108033]으로 잘못 달림**) | Kresse 인용 없음 — 후처리는 VASPKIT 사용 추정 |
| functional | PBE-GGA, PAW | vdW(D3) 없음, DFT+U 없음, hybrid 없음 |
| ecut | 500 eV | — |
| smearing | **1차 Methfessel–Paxton, σ=0.1 eV** | 절연체에 MP 1차는 비관례(보통 Gaussian/tetrahedron) — gap 재료엔 대개 무해하나 세팅 감각을 보여줌 |
| k-mesh | **5×5×5** | 어느 셀에 대한 mesh인지 불명; 관례 셀(~10 Å)이면 과밀한 편(우리 감각) |
| 수렴 | SCF 10⁻⁶ eV, force <0.03 eV/Å | — |
| 슬랩 | dipole correction z방향 | 계면 슬랩(면지수·층수·진공·변형) 사양 전무 |
| 도핑 모델 | **"3×5×5 supercell"에 Y 1개(P 자리)+O 2개(Cl 자리!) 치환** | ① 3×5×5 conventional이면 ~3900원자 — 5×5×5 k-mesh와 양립 불가, 오기 확실(1×1×1 관례셀 추정: 그러면 Y=25% P, O=50% Cl). ② **O를 Cl 자리에** — 실험 정련(O@16e, S 자리)·조성식(S5−1.5x)과 화학이 다름. 논문 내 3개 구조(정련/BVSE/VASP)가 서로 불일치 |
| 사이트 선호 | 형성E(원자 기준): Y@P+O@S **−4.27846** vs Y@Li+O@S **−4.26615 eV/atom** (Δ0.0123 eV/atom) → Y@P 결론 | 후보 배열 각 1개씩만·고립원자 기준E(열역학 안정성 아님)·**우리 M³⁺ cascade site-rule(전원 Li_24g)과 정반대**(§12) |
| AIMD / NEB / MLIP | 없음 / 없음 / 없음 | Ea·경로는 전부 BVSE에 위임 |
| DOS/PDOS | NBANDS 조정→WAVECAR→**LOBSTER** | 기저·basis set(pbeVaspFit?) 미보고 |
| LOBSTER 산출 | COHP·COBI·ICOHP·ICOBI·**Madelung**(Glasser 인용) | **Madelung만 보고, COHP/COBI류 결과 미제시** |
| ELF | VASP ELF 슬라이스 | iso/단면 사양 미보고 |
| H₂O 계산 | 흡착(슬랩 "end surface")·가수분해(유닛 반응) | 전하보상/용매화 없음, cluster성 근사 |
| 무질서 처리 | **없음** (정렬 스냅샷 1개; SQS/enumerate 부재) | Li 48h 부분점유·Cl/S 자리혼합을 어떻게 정수화했는지 미기술 |

## 10. Figure set ★ (전체)
| Fig | 내용 | 우리 참고 |
|---|---|---|
| 1a,b | XRD(Rp3.55/Rwp5.41)·NPD(Rw4.79/GOF7.42) Rietveld of YO | GOF·잔차 수준 확인용 |
| 1c | 구조모델(Y/P=4b, Cl=4a/4d, Li=48h, S=4a/16e/4d, O=16e) | **그들 setting 확인** — 우리 비교 시 4c↔4d 원점 주의 |
| 1d | x=0–0.1 XRD: x≥0.08 Li₂S·LiYS₂ 불순물 | 고용한계 x=0.05 |
| 1e | Raman 427.18 cm⁻¹ 불변 | PS₄ 골격 유지 |
| 1f–h | XPS P 2p(P–O 신규)·S 2p(Y–S 160.1/161.1)·O 1s(Li–O–P 531.34) | P–O 본문 BE 오타 의심(§13-9) |
| 1i–k | HRTEM 0.309 nm·SAED (331)/(422) | 0.309 vs XRD a 불일치(§13-3) |
| 2a,b | Nyquist·Arrhenius (x 5종) | — |
| 2c | σ·Ea bar: 3.53 mS/cm·0.34 eV @x=0.05 | LPSC 값은 그림 판독만 가능(본문 미기재) |
| 2d,e | **BVSE 등가면+60 Å 랜드스케이프 1.11/0.61 eV, O7·Y2 빨간 원** | §6 — 우리 규율과 충돌 지점 |
| 2f | CV: 산화>2.48 V·환원<1.83 V 전류↓ (S/P redox 라벨) | B① kinetic 데이터점 |
| 2g | H₂S ~0.47→~0.30 cm³/g | B④ moisture |
| 3a,b | CCD 0.7/1.5 mA/cm² | — |
| 3c,d | 대칭셀 0.1(>4800 h)·0.5 mA/cm²(>1300 h)+확대 | Table S6와 4300/4800 불일치(§13-10) |
| 3e–h | GEIS 3D + **DRT**(τ 10⁻⁶ SSE·10⁻⁴ SEI, 1.6 vs 2.4 mAh/cm²) | **DRT로 파괴모드 시간상수 분리 — 차용 가치 큼** |
| 3i | CCD vs 수명 3D 문헌 비교 | — |
| 4a–c | 계면 XPS depth: Li₂S·Li₃P 증가(LPSC) vs 억제+Li₂O 528.5 eV(YO) | E축 앵커 |
| 4d–g | SIMS 3D: LiO⁻ 균일층(YO)·LiS⁻/Li₂P⁻ 희박 | Li₂O interphase 시각화 |
| 4h–k | 사이클 후 Li 표면 SEM + 모식도 | — |
| 5a,b | 계면 슬랩 이완: PS₄ 붕괴 vs YS₄ 유지 | 단일 배열 0 K(§8) |
| 5c,d | ELF: S 국재화 | § 8 |
| 5e,f | PDOS: p–p vs **d–p 혼성**(Y-4d 분해) | § 8 |
| 5g,h | **Madelung −166.51 vs −175.07 eV/atom** | LOBSTER+Glasser; 유닛 전하 비대칭(§8) |
| 5i,j | easy/hard electron transfer 만화 | — |
| 6a–f | 풀셀: 0.1C(89.6 vs 77.2%)·rate·0.5C 1300cyc "100%"·파우치 | §5.10 주의 포함 |
| S3 | Y@P vs Y@Li 형성E(Δ0.0123 eV/atom) | §12 site-rule 충돌 |
| S11 | BVSE 전체 셀 등가면(라벨 Y2·O70) | 정렬 스냅샷 증거 |
| S12,S13 | H₂O 흡착·가수분해E | §5.6 |
| S17 | XPS 정량 파이(Li₂S 21.3→9.9%·Li₃P 9.0→3.6%) | (d) 라벨 합 110.3% 오류(§13-12) |
| S19 | 계면 슬랩 초기구조(Y가 계면층) | 모델 선택 편향 |
| Table S1–S4 | XRD/NPD 좌표·점유 | §7 — 관례 혼용·O 충돌 |
| Table S5 | ICP(Li 17.12/P 10.35/S 56.31/Y 1.35 wt%) | Li/(P+Y)≈7.1 재계산(§13-8) |
| Table S6,S7 | 대칭셀·풀셀 문헌 비교 | 4300 vs 4800 |

## 11. Post-processing ★
- **BVSE**: softBV 계열 플랫폼+SoftBV(0.1 Å), Voronoi 전처리. 기록=등가면 그림+경로 랜드스케이프 최대값(eV). ⚠ iso-level·경로 정의 미기록.
- **LOBSTER**: COHP/COBI/ICOHP/ICOBI+**Madelung(Glasser)** — 보고는 Madelung만. VASPKIT 후처리 추정.
- **ELF/PDOS**: VASP → 단면/오비탈 분해 곡선.
- **DRT**: GEIS→이완시간 분포, τ별 소자 배정(10⁻⁶ SSE/10⁻⁴ SEI), 용량축 색맵 — **정량 열화 추적 틀로 차용 추천**.
- **XPS depth + TOF-SIMS 3D**: 산물(Li₂S/Li₃P/Li₂O) 깊이·공간 분포, 파이 정량.

## 12. 우리 DFT 대비 (comp1/modelc + cascade) → `../our_dft_baseline.md`
| 항목 | 이 논문 | 우리 | 판정 |
|---|---|---|---|
| 호스트 조성 | LPSC=Li₆PS₅Cl | **comp1과 동일 조성** | 직접 비교 가능 축 |
| 산화 onset | CV 산화전류 >2.48 V (kinetic) | grand-potential **2.256 V**(S²⁻-limited, LiS4 제외) | **✓ 정합** — 2.48=열역학 2.256+과전압, [Son25] "<2.5 V"·[Banik] S-pin과 한 줄 |
| 환원 거동 | <1.83 V 환원전류, 산물 Li₂S·Li₃P(+Li₂O) | 환원한계 1.242 V, 0 V 산물 **Li₃P+Li₂S+LiCl** | **✓ 같은 chemistry**(축 E). 그들의 개선은 kinetic passivation — 우리 hull로는 조성 5% 차이의 환원전위 이동은 못 봄(계산도 안 했음) |
| BVSE 용법 | 장벽 절대값(1.11/0.61 eV)을 σ 서사로 헤드라인 | **BVSE=(BVS−1)², 채널%만, 원본 주기셀, 순위·절대값 인용 금지** | **✗✗ 규율 충돌** — 그들 값은 자기 실측 Ea(0.375/0.34)와 3×/1.8× 불일치. 우리가 BVSE 장벽을 Ea로 안 쓰는 이유의 살아있는 예 |
| Y³⁺ 자리 | **P(4b)** — 형성E Δ0.0123 eV/atom(배열 각 1개)+constrain된 정련 | **cascade M³⁺ site-rule: 26/26 전원 Li_24g**(O는 S_16e; Y₂O₃ 포함, host=modelc, UMA 스케일) | **⚠ 정면 충돌(방법·호스트 의존)** — 그들 Y@P는 +2Li(carrier↑), 우리 Y@Li는 donor-blocking. 어느 쪽이 맞는지에 따라 σ 기전이 정반대. 우리 쪽도 UMA·Cl-rich host라 직접 반증은 아님 → 검증 계산 가치(§14-①) |
| M³⁺ 도핑의 Li 수송 효과 | "장벽 절반" | cascade **bvs_li_proxy 0.83–0.92로 균일**(M³⁺ 종류 무관·Nd σ-drop 0.52×는 blocking) | **✗ 방향 상충** — 우리 데이터는 "M³⁺ 도핑은 Li 이동도를 거의 안 바꾼다". 단 사이트 모델이 다르니(P vs Li) 동일 조건 비교 아님 |
| σ_e | 6.33→1.55×10⁻⁷ S/cm | (우리 σ_e 실측 없음; wide-gap 축만) | 그들 LPSC 베이스라인이 [Adeli]3e-9·[Taklu]8.75e-9·[Yang25]2.59e-9 대비 60–200× 높음 — 시료 품질 의심 |
| band gap | 본문 미보고 → **Fig 5e 픽셀 실측 ≈2.07 eV**(LPSC) / ≈2.55 eV(YO) | comp1 **2.066** / modelc 2.099 eV (PBE fixed-occ nscf) | **✓ 정합** — 같은 PBE 스케일, 사실상 같은 자리. 우리 2.066이 특이값 아님을 타 그룹·VASP로 교차확인(§18.2). ⚠ 그들 값은 DOS-threshold 판독이라 **db 편입·절대값 인용 금지** |
| VBM character | Fig 5e: 밴드 가장자리 **S-p 독점**(P-p는 S-p의 2%) | comp1/modelc 둘 다 **VBM = S 3p** | **✓✓ 독립 확인** — 단 논문 본문은 이걸 "p–p 혼성 at Fermi level"이라 **반대로 서술**(§18.1) |
| O 2p 위치 | Fig 5e: O-p 무게의 **82%가 E<−2 eV**(S-p는 30%) | LPSOCl(+O) **O 2p 매몰**(site-PDOS, 창 −8..0 eV) | **✓✓ 정합** — 방법 다른데 결론 같음. 함의도 같음: O는 산화 onset을 못 움직인다(그들 CV onset 불변과 자기일관) |
| O 치환의 gap 효과 | +0.48 eV (2.07→2.55) | +0.16 eV (comp1 2.066 → LPSOCl 2.2309) | **✓ 방향 일치**, 크기 3배 — 그들 VASP 모델 O 농도가 훨씬 높은 탓(O@Cl 2개)으로 설명됨 |
| σ₀(전지수인자) 거동 | σ·Ea 실측이 **σ₀ 3.6× 감소**를 요구(§18.4) | cascade: M³⁺는 Li 이동도 거의 불변, **Nd는 σ 0.52× blocking** | **✓ 방향 일치(우리 쪽과)** — 그런데 논문 설명("carrier↑·채널 확장")과는 **반대**. 그들 자기 모순 |
| 무질서 처리 | 없음(정렬 스냅샷 1개) | disorder ensemble·SQS 계열 규율 | 우리 기준 미달 |
| O 도핑 위치 | 정련=16e(S자리) vs **VASP=Cl자리** vs BVSE=불명 | 우리 LPSOCl(+O)는 S자리 O, gap 2.2309 eV | 그들 내부 불일치(§13-5) |
| Ea 실험 | 0.375→0.34 eV (EIS 벌크+입계) | comp1 MLIP-MD 0.253 (단일궤적; modelc 3-seed 0.197±0.032) | 방법 다름(EIS vs 벌크 MD) — 방향만: 우리가 벌크라 낮은 게 정상 |
| H₂S·대기 | 0.47→0.30 cm³/g+YS₄ 가수분해 +4.13 eV | (축 B④ 소환값 참조: [Yang25] 3.2→2.3, [Taklu] 1.07→0.49) | 절대값은 챔버 조건 의존 — 상대 개선 ~35%만 |

## 13. ★ 헛점 후보 목록 (요청 #5)
1. **격자 "팽창" +0.0006 Å(+0.006%)** — Rietveld 격자상수의 통상 재현성(시료 재장착·영점)에 묻히는 크기. Y 5% 편입의 구조 증거로 부족. (비교: [Liu] Cl-rich는 0.04 Å 변화.)
2. **"ionic radius Y 162 pm / P 110 pm"** — 이온반경이 아님(Shannon: Y³⁺(VI) 90 pm, P⁵⁺(IV) 17 pm; 162/110은 원자/공유 반경 계열). 결론 방향은 유지되나 수치 인용은 오염.
3. **HRTEM 0.309 nm vs 자기 XRD** — a=9.848 Å이면 d(311)=0.297 nm. +4% 차이를 "slight lattice expansion"으로 설명 — XRD +0.006%와 양립 불가(국소 측정 오차가 정직한 설명).
4. **COHP/COBI/ICOHP/ICOBI "계산했다"고 쓰고 결과 미제시** — 결합세기 정량이 서사(P–S 약함/Y–S 강함?)와 어긋났을 가능성. Madelung(정전)만 취사선택한 인상.
5. **구조 3원 불일치** — 정련(O@16e·S자리) ↔ VASP(O@Cl자리) ↔ BVSE(이산 Y/O decorate, 배치 미공개). "같은 물질"을 계산했다고 보기 어려움.
6. **σ_e 베이스라인 이상** — LPSC 6.33×10⁻⁷ S/cm는 문헌 pristine 대비 최대 200×. "4× 개선"의 출발점이 오염되어 있고, 개선 후에도 타 그룹 pristine보다 높음.
7. **YS₄ 가수분해 +4.13 eV** — 전하 비보상 고립 유닛 반응. 부호(흡열) 이상의 의미 부여 금지.
8. **ICP "well consistent" 주장** — 재계산 시 Li/(P+Y)≈7.06(nominal 6.1, +16%), Y/(P+Y)≈0.0435(−13%). Cl·O는 미측정. "정합"은 후한 표현.
9. **XPS P–O 본문 BE(131.1/131.9 eV)** — P–S(131.8/132.8)보다 낮은 P–O는 화학적으로 역방향; 그림은 ~133.5–134 eV. 본문 수치 오타 유력.
10. **내부 수치 불일치** — 대칭셀 0.1 mA/cm²: 본문 "4800 h" vs Table S6 "4300 h"; 0.5: "1300" vs "1350". Fig S17d 파이 라벨 합 110.3%(89%+21.3%). Table S1 캡션에 도핑 조성+(x=0) 혼재. GSAS-II→"GASA II", PARSTAT→"PARSRAT" 등 전반적 교정 품질.
11. **"100%/1300 cycle"의 실험 설계** — ① 0.5C 용량 91.9=0.1C의 75%(저활용 셀은 열화가 늦게 보임), ② catholyte가 **LiDFOB-coated 별도 Cl-rich SE**(연구 대상 SE가 아님; LPSC 셀과 YO 셀에서 catholyte가 동일한지 표기 모호), ③ 음극 Li-In(합금) — 즉 이 수치는 양극축 개선도, 연구 SE의 산화 내성도 아니고 **분리막/음극축**의 개선. "100%"는 CE 반올림+저활용의 합작일 개연성.
12. **통계 전무** — 셀 반복수(n), 오차막대, BVSE 배열 앙상블, DFT 배열 샘플링 모두 없음. 대칭셀·CCD는 단일 셀 서사.
13. **순환 구조** — Y@4b를 가정한 정련("확인") → 그 구조로 BVSE("채널 확장") → 그 결론으로 실험 σ 해석. 각 고리는 독립 검증 없이 서로를 인용.
14. **"electronic localization"의 인과 비약** — §8.2의 4개 비약(열역학 부재·Y/O 미분리·σ_e 연결 없음·정량지표 부재).
15. **⭐ [2차] "p–p hybridization at the Fermi level"이 자기 Fig 5e와 어긋난다** — 밴드 가장자리에서 P-p는 S-p의 **2%**(P-p 봉우리는 −4.4 eV). LPSC의 VBM은 사실상 **순수 S 3p**다. 게다가 도핑 후 Y-d가 가장자리에 **18%** 들어오므로, "비편재→국재" 서사와 양이온 성분의 변화 방향이 **반대**다. → §18.1. **1차의 "용어 부정확" 판정을 "사실 오류"로 승격.**
16. **⭐ [2차] σ·Ea 쌍이 "carrier 증가" 설명과 모순** — σ 1.29× / ΔEa 0.040 eV ⇒ 전지수인자 σ₀가 **3.6× 감소**해야 성립. 논문 설명(채널 확장+carrier 증가)은 σ₀ 증가 방향. 결론은 ΔEa>0.0065 eV면 성립해 **판독 정밀도에 둔감**. → §18.4.
17. **[2차] Fig 2d/e BVSE 두 패널의 표본 비대칭** — LPSC 프로파일이 LPSC-YO보다 현저히 조밀·불규칙 → 경로/샘플링이 서로 다름. iso-level 미표기까지 겹쳐 "1.11→0.61 = 절반"의 비교 가능성 자체가 흔들린다. → §18.5.
18. **[2차] Fig 5 캡션 원소 표기 오류 2건** — "S 2p"(→ S 3p, 2p는 내각 XPS 준위) · "**Y 3d**"(→ Y 4d, Y에 3d 껍질 없음). → §18.6.
19. **[2차] Arrhenius 창 35 K(25–60 °C)·5점·오차 미보고** — 조성 간 Ea 차 0.040 eV의 유의성 판정 불가. → §18.8.
20. **[2차] 0.5C 용량 불일치** — Fig 6b rate 86.1 vs Fig 6d 사이클 초기 91.9 mAh/g(=Fig 6b의 0.4C 값과 동일). → §18.9.

## 14. 적용 인사이트 (우리 캠페인에)
- **① Y@P(4b) vs Y@Li(24g) site-preference 검증 계산 가치** — 우리 cascade는 M³⁺ 전원 Li_24g(UMA·modelc host), 이 논문은 Y@P(4b)(PBE 형성E 2배열+constrained 정련). comp1 host에서 Y@4b(+2Li) vs Y@24g(−2Li)를 **같은 DFT 기준**으로 형성E·BVSE 채널%·(가능하면 MLIP-MD Ea)로 갈라보면, 이 논문 기전의 사활+우리 site-rule의 host 의존성을 동시에 판정할 수 있다. (Y³⁺→P⁵⁺면 carrier가 +2Li, Y³⁺→Li⁺면 −2Li — **부호가 반대**라 σ 기전이 정반대로 갈림.)
- **② BVSE 규율의 반면교재** — "BVSE 장벽 절대값을 Ea/σ 서사로 쓰면 자기 실험과 3× 어긋난다"의 출판 사례. 우리 채널%-only 규율의 근거 각주로 인용 가능.
- **③ DRT 열화 추적 차용** — τ(10⁻⁶ SSE/10⁻⁴ SEI)×스트리핑 용량 색맵으로 "무엇이 언제 죽는지" 분리 — 우리 계면 논의(축 E)의 실험 파트너 기법으로 명기.
- **④ Li₂O interphase = wide-gap 절연 산물 가족** — LiCl([Lu]·[Li25])·LiF 계열과 같은 축 E 서사. O-도핑 argyrodite(우리 LPSOCl, +B₂O₃)의 음극 방어 논리로 소환 가능(단 물량 정량 없음 명시).
- **⑤ CV 2.48 V** — 우리 2.256 V(S-limited) 위 kinetic overshoot 데이터점 하나 추가(B①). "치환으로 onset은 안 움직인다"([Banik])와도 정합(YO도 onset 동일, 전류만↓). [2차] Fig 2f 전류 실측으로 확정: >2.5 V에서 두 시료 **~1×**(§18.7).
- **⑥ ⭐[2차] 외부 교차검증 카드 3장** — 이 논문의 Fig 5e는 (a) LPSC PBE gap **≈2.07 eV**(우리 comp1 2.066), (b) **VBM = S 3p 독점**, (c) **O 2p 매몰**을 전부 독립적으로 보여준다(§18.2·18.3). 우리 세 결과가 "우리 세팅 탓"이 아님을 **다른 그룹·VASP·같은 PBE**로 받칠 수 있는 드문 카드다. 단 gap 절대값은 그림 판독이라 **"wide-gap 2 eV대·O가 넓히는 방향" 수준까지만** 인용.
- **⑦ ⭐[2차] "자기 그림으로 반박되는 전자구조 서사"의 사례** — §18.1(p–p 혼성)·§18.4(σ₀ 방향)은 **PDOS를 정성 그림으로만 쓰면 어떻게 틀리는지**의 교보재다. 우리 site-PDOS 규율(⟨3p⟩ mean-3p를 **그림 표시 창과 동일한 −8..0 eV 창**에서 정량화)이 왜 필요한지의 각주로 인용 가능 — §14-②(BVSE 채널%-only)와 같은 역할.

## 15. 인용 가능 문장 (deck/paper용)
- "Wang et al. (Angew 2025) report that 5% Y/O co-substitution in Li₆PS₅Cl suppresses interfacial Li₂S/Li₃P formation (21.3→9.9% / 9.0→3.6% in XPS) and forms an in-situ Li₂O interphase, extending Li-symmetric cycling to >4800 h — an anode-axis (kinetic passivation) improvement, with the oxidation onset unchanged (~2.48 V CV), consistent with our S²⁻-limited 2.256 V."
- "Their BVSE 'barrier halving' (1.11→0.61 eV) exceeds their own measured Ea (0.375/0.34 eV) by 2–3×, illustrating why we restrict BVSE to channel-fraction descriptors rather than absolute migration barriers."
- "The claimed Y-site (P 4b, +2 Li carriers) conflicts with our UMA cascade site rule (all 26 M³⁺ dopants on Li 24g); the two models predict opposite carrier changes and remain untested against each other."
- [2차] "Their own PBE PDOS (Fig 5e) places the Li₆PS₅Cl valence-band edge on essentially pure S 3p — P p-character is ~2% of S there, with the genuine P–S p–p bonding state 4 eV lower — independently supporting the S-3p-dominated VBM we obtain for comp1."
- [2차] "In the O-substituted argyrodite, 82% of the O 2p weight lies more than 2 eV below the valence-band edge, consistent with our LPSOCl result that O 2p is buried and therefore cannot shift the S²⁻-limited oxidation onset."

## 16. 주의/한계 (재인용 시)
- LPSC σ 2.75/Ea 0.375는 **그림 판독**(본문 수치 없음) — "≈" 필수.
- 조성은 **S4.925O0.075**로 쓸 것(본문 S4.25O0.75는 오타).
- BVSE 1.11/0.61 eV는 **수송 Ea가 아님** — 인용 시 반드시 "BVSE landscape 값, 실측 Ea와 3× 불일치" 단서.
- "100%/1300 cycles"는 Li-In·0.5C·저활용·coated-catholyte 조건부 — 무단서 인용 금지.
- Madelung −166.51/−175.07 eV/atom은 **유닛 전하가 다른 비교** — 정전 안정성 순위로 이식 금지.
- 우리 cascade Y₂O₃ 수치(de_post_anneal −0.99 eV/atom 등)는 **UMA 스케일·modelc host 내부 비교 전용** — 이 논문 PBE 값과 절대 비교 금지.
- **[2차] 밴드갭 2.07/2.55 eV는 그림 판독(DOS-threshold)** — CLAUDE.md 규율상 **db 편입 금지·절대값 인용 금지**. 허용 문장은 "그들 PBE PDOS도 wide-gap 2 eV대, O가 넓히는 방향까지 우리와 같다"까지(±0.2–0.3 eV 병기).
- **[2차] 그들 PDOS 인용 시 "S 2p"를 그대로 옮기지 말 것** — 캡션 오타다. 가전자대는 **S 3p**(우리 site-PDOS 서술자와 같은 궤도). Y도 3d가 아니라 **4d**.
- **[2차] LPSC σ·Ea(2.74 mS/cm·0.380 eV)는 픽셀 실측값** — 본문에 숫자가 없다. 인용 시 "Fig 2c 판독" 명시.

## 17. 기법 용어 미니사전 (§18은 그 아래)
- **BVSE (bond-valence site energy)**: 결합원자가 불일치 |BVS−1|²+정전항으로 만든 정적 에너지 지도. 채널 연결성 판별엔 유용, **절대 장벽≠Ea**.
- **Voronoi decomposition**: 결정 간극을 Voronoi 다면체로 분할해 이동 이온 후보 자리/병목 추출(플랫폼 전처리).
- **ELF**: 전자 국재화 함수(0–1). 공유결합=결합축 국재, 이온결합=음이온 위 국재 — "이온성 지도"에 가까움.
- **Madelung energy (LOBSTER/Glasser)**: 점전하 정전 격자에너지를 부분전하로 평가. 전하 partition 관례에 민감.
- **d–p orbital hybridization**: 전이금속 d와 리간드 p의 혼성 — d⁰ 양이온에선 VB 상단에 d 성분 소량 혼입이 일반적.
- **DRT (distribution of relaxation times)**: 임피던스를 τ 스펙트럼으로 역변환해 소자(SSE/SEI/전하이동)를 시간상수로 분리.
- **GEIS**: 정전류 하 임피던스 — 작동 중 계면 추적.
- **CCD**: 대칭셀 단락 임계 전류밀도(계면+미세구조 총합 지표).
- **MPI (CSNS)**: 중국 산란중성자원 Multi-Physics Instrument — TOF 중성자 회절(경원소 Li/O 감도 확보용).

---

## 18. ★★★ 2차 패스 — 본문 그림 **픽셀 독립 검증** (2026-08-04)

**1차 패스**(같은 날 앞선 세션)는 본문 + **SI 34 pp**의 텍스트·표를 정독했다. 이번 패스는 통로가 다르다:
사용자가 inbox `52.`(본문 PDF 11 pp, **SI 없이**)를 다시 넣었고, 이번엔 그림을 **600–900 dpi로 렌더해
축 프레임·눈금·막대·곡선을 픽셀로 실측**한 뒤 인쇄된 문장과 대조했다.
재현 코드 **`tools/litdb/wang2025_fig_verify.py`** (PyMuPDF + PIL만, numpy 없음 — `ren2026_fig_verify.py` 선례 준용),
출력 `litdb/inbox/_52_verify_out.txt`.

> **결과 요약**: 1차가 "미보고 / 비교 불가"로 남긴 **밴드갭 칸이 채워졌고**(§18.2 — 우리 comp1과 정합),
> 1차가 "부정확한 표현" 수준으로 넘어간 **PDOS 주장은 자기 그림에 의해 정면 반박된다**(§18.1).
> **신규 4건**(§18.1·18.2·18.3·18.4). 1차의 판정은 하나도 뒤집히지 않았고, 두 건이 더 강해졌다.

### 18.1 ✗✗ **신규·최중요** — "p–p hybridization **at the Fermi level**"은 자기 Fig 5e가 부정한다

본문(p. 8) 원문: *"PDOS results show that P-p orbitals and S-p orbitals of PS₄ tetrahedron of LPSC exhibit
**p–p orbital hybridization at the Fermi level**, which explains the electron delocalization of the PS₄ tetrahedron
in the ELF analysis."* — 이 문장이 LPSC 쪽 기전의 **출발점**이다(그래야 "YO는 다르다"가 성립).

1차 §8.1은 이걸 *"'at the Fermi level'은 부정확(절연체 — VBM 근방을 뜻함)"* 이라는 **용어 문제**로 넘겼다.
픽셀 실측 결과 **용어 문제가 아니라 사실 문제**다. Fig 5e 상단 패널에서 곡선 높이(px):

| E (eV) | P-p | S-p | P/S |
|---:|---:|---:|---:|
| **−4.4** | **193** | **178** | **108%** ← 진짜 p–p 결합상태 |
| −3.5 | 13 | 43 | 30% |
| −2.0 | 10 | 184 | 5% |
| **−0.8** (S-p VBM 봉우리) | **7** | **457** | **2%** |
| −0.2 | 4 | 67 | 6% |

> 🔑 **P-p의 봉우리는 −4.4 eV — VBM보다 4 eV 아래다.** 거기서는 P-p ≈ S-p(108%)로 진짜 P–S σ 결합상태가 맞다.
> 그러나 **밴드 가장자리(그들이 말한 "Fermi level")에서 P-p는 자기 최대치의 4%, S-p의 2%밖에 안 된다.**
> 즉 **LPSC의 VBM은 사실상 순수 S 3p**이고, 논문이 "PS₄ 사면체의 전자 비편재화"의 근거로 든
> p–p 혼성은 **그 자리에 없다**.
>
> **우리 데이터와의 관계**: 우리 comp1/modelc VBM character = **S 3p** (`our_dft_baseline.md` §핵심발산).
> 이 논문의 Fig 5e는 **우리 결과를 독립적으로 재확인**해준다 — 그들 본문 문장만 빼면.
> free-S site-PDOS ⟨3p⟩ −1.1 eV 서사(축 B①)와도 한 줄.

**그리고 방향이 오히려 반대다.** 하단 패널(LPSC-YO)에서 Y-d는 **VBM 봉우리(−0.55 eV)에만** 나타난다
(Y-d 79 px vs S-p 442 px = **18%**), 가전자대 나머지 구간에서는 0이다.

| | 밴드 가장자리의 양이온 성분 |
|---|---|
| LPSC (도핑 전) | P-p = S-p의 **2%** (사실상 없음) |
| LPSC-YO (도핑 후) | Y-d = S-p의 **18%** |

> 🔑 **도핑은 밴드 가장자리의 양이온 성분을 없앤 게 아니라 새로 만들었다**(2% → 18%).
> 논문 서사("비편재 → 국재")의 전자구조적 방향과 **정반대**로 읽힌다.
> 공정하게: Y-d 혼입이 S 3p를 **아래로 밀어 안정화**한다는 해석은 가능하다(§18.2의 gap 증가와 정합).
> 그러나 그 해석은 논문에 없고, 논문이 실제로 쓴 "p–p vs d–p" 대비는 **자기 그림에서 성립하지 않는다.**

### 18.2 ✅ **신규** — 밴드갭을 그림에서 뽑았다: **~2.1 / ~2.55 eV** (1차의 "비교 불가" 칸이 채워짐)

Fig 5e에는 갭이 그려져 있는데 본문·SI 어디에도 숫자가 없다. 축 눈금(−6…+6 eV, 101.75 px/eV)을 잡고
S-p 곡선이 **연속 5열 이상 임계 위로** 올라오는 지점을 밴드 가장자리로 정의해 실측:

| | VBM | CBM | **gap** |
|---|---:|---:|---:|
| LPSC | +0.30 eV | +2.38 eV | **≈ 2.07 eV** |
| LPSC-YO | +0.22 eV | +2.76 eV | **≈ 2.55 eV** |

- SI가 밝힌 계산 수준은 **PBE-GGA/PAW, ecut 500 eV**(§9). PBE 스케일에서 LPSC ~2.1 eV는 **정상 범위**이고,
  **우리 canonical comp1 2.066 eV**(fixed-occ nscf VBM/CBM 고유값)와 사실상 같은 자리다.
  → 우리 2.066이 특이값이 아님을 **다른 그룹·다른 코드(VASP)·같은 functional**로 교차확인한 셈.
- **O 치환이 갭을 넓힌다**: 그들 +0.48 eV, **우리 comp1 2.066 → LPSOCl(+O) 2.2309 = +0.16 eV**.
  **방향 일치, 크기는 그들이 3배** — 그들 VASP 모델의 O 농도가 훨씬 높기 때문으로 보인다
  (§13-5: VASP 모델은 O를 **Cl 자리에 2개** = 관례셀이면 Cl의 50%, 실험 조성 O0.075와 자릿수가 다름).
  즉 **크기 차이는 실물 차이가 아니라 모델 농도 차이**로 설명된다.

> ⚠⚠ **인용 규율**: 이 2.07/2.55는 **그림에서 읽은 DOS-threshold 값**이다.
> CLAUDE.md의 "band gap = fixed-occ nscf VBM/CBM 고유값만 인정, DOS-threshold 판독 금지(~0.3 eV 과소)"가
> 그대로 적용된다 — **우리 db에 넣지 않고, 문헌 절대값으로도 인용하지 않는다.**
> 쓸 수 있는 문장은 딱 하나: **"그들 PBE PDOS도 wide-gap 2 eV대이고 O 치환에서 갭이 넓어지는 방향까지 우리와 같다."**
> (±0.2–0.3 eV 필수 병기.)

### 18.3 ✅ **신규** — O 2p는 **S 3p VBM 아래로 매몰**돼 있다 (우리 LPSOCl 결과의 독립 확인)

Fig 5e 하단 패널에서 색별 곡선 높이를 −6…+0.3 eV 구간에서 적분해 "깊은 쪽(E < −2 eV) 비율"을 냈다:

| 성분 | E < −2 eV 무게 비율 | 봉우리 위치 |
|---|---:|---|
| **O-p** | **82%** | −5.5 eV, −2.8 eV |
| S-p | 30% | **−0.55 eV** (VBM) |

> 🔑 **O 2p 무게의 82%가 VBM에서 2 eV 이상 아래**에 있고, 밴드 가장자리는 S 3p가 독점한다.
> = 우리 **LPSOCl(+O) "O 2p 매몰"** 결과와 같은 그림. 우리 쪽은 site-PDOS 정량(창 −8..0 eV)으로,
> 이쪽은 원소분해 PDOS로 — **방법이 다른데 결론이 같다**(축 B① 보강).
> 함의도 같다: **O 치환은 산화 onset을 움직이지 못한다**(가장자리가 여전히 S 3p이므로).
> 실제로 이 논문 CV(Fig 2f)에서도 **산화 onset은 LPSC/LPSC-YO 동일하고 전류만 줄었다**(§5.5) — 자기 일관.

### 18.4 ⚠ **신규** — Fig 2c 실측: σ·Ea 두 값이 **carrier 증가 설명과 아귀가 안 맞는다**

LPSC 쪽 σ·Ea는 본문에 숫자가 없어 1차는 "~2.75 mS/cm·~0.375 eV (그림 판독)"로 뒀다. 막대를 픽셀로 실측
(**x=0.05 행이 인쇄 라벨 3.53 / 0.34를 그대로 재현** → 축 보정 검증됨):

| x | σ (mS/cm) | Ea (eV) |
|---|---:|---:|
| **0 (LPSC)** | **2.74** | **0.380** |
| 0.02 | 3.36 | 0.361 |
| **0.05 (LPSC-YO)** | **3.54** | **0.340** ← 인쇄 라벨과 일치 |
| 0.08 | 2.66 | 0.351 |
| 0.1 | 2.57 | 0.351 |

Arrhenius 자기일관성 검사 (298 K, σT = σ₀·exp(−Ea/kT)):

- 실측 σ 비 = 3.54/2.74 = **1.29×**
- ΔEa = 0.040 eV **만으로** 기대되는 비 = exp(0.040/0.02569) = **4.70×**
- ⇒ 아귀를 맞추려면 **전지수인자 σ₀가 3.6× 감소**해야 한다.

> 🔑 그런데 논문의 설명(p. 4)은 *"aliovalent substitution of the large-size Y³⁺ to P⁵⁺ **enlarges the Li⁺ transport
> channels and increases the Li⁺ carrier concentration**"* — **둘 다 σ₀를 올리는 방향**이다.
> 자기 데이터는 σ₀가 **내려갔다**고 말한다. 즉 **"채널 확장 + carrier 증가"는 자기 σ·Ea 쌍으로 지지되지 않는다.**
> 물리적으로 더 자연스러운 읽기: Y/O 치환이 **일부 Li 자리를 막거나(O의 강한 국소 흡인, Li–O R0 1.466 Å)
> 이동 가능 자리 수·시도빈도를 줄이면서** 장벽만 살짝 낮췄다 — 이건 우리 cascade 결과
> (**M³⁺ 도핑은 Li 이동도를 거의 안 바꾸고, Nd는 σ 0.52×로 blocking**)와 **오히려 같은 방향**이다.
>
> **민감도**: LPSC의 Ea(0.380)는 픽셀 판독이라 오차가 있다. 그러나 "σ₀ 감소" 결론은
> **ΔEa > 0.0065 eV이기만 하면 성립**한다(= kT·ln 1.29). 인쇄된 0.34와 어떤 합리적 LPSC 값을 넣어도
> 부호는 안 바뀐다 — **결론은 판독 정밀도에 둔감**하다.
> ⚠ 단, σ는 벌크+입계 합산이므로 σ₀ 감소를 "벌크 carrier 감소"로 곧장 번역하면 안 된다
> (치밀화·입계 기여가 σ₀에 섞인다). 말할 수 있는 건 **"논문이 든 설명은 자기 수치와 맞지 않는다"**까지다.

### 18.5 ⚠ **1차 판정 보강** — Fig 2d/e BVSE 두 패널은 **표본이 서로 다르다**

1차 §6.3은 1.11/0.61 eV가 "60 Å 경로의 최대값"임을 밝혔다. 픽셀로 두 프로파일을 나란히 보면 하나 더 보인다:
**LPSC(파랑) 곡선은 마커가 훨씬 조밀·불규칙**하고(톱니 봉우리 다수, 1.11 eV 봉우리가 4곳에 불규칙 분포),
**LPSC-YO(보라)는 눈에 띄게 성기고 매끄럽다**(준주기적 톱니).

> 같은 알고리즘·같은 샘플링으로 뽑은 두 경로라면 격자상수가 0.006% 다른 두 구조에서
> **점 밀도와 봉우리 규칙성이 이렇게 다를 이유가 없다.** 경로 선택 또는 샘플링 간격이 서로 달랐다는 뜻이고,
> 그러면 **"1.11 → 0.61 = 절반"은 두 표본을 비교한 값**이 된다.
> 1차 §6.4-③ 판정(✗✗ 과대 표현)을 **한 단계 더 강화**한다: 방법 내재 편향·단일 스냅샷·자기 실측과 3× 불일치에
> **표본 비대칭**이 추가된다.
> (덧: 두 패널 어디에도 **iso-level이 없다.** 등가면 두 장을 눈으로 비교시키면서 등고선 값을 안 주는 건
> 우리 BVSE 규율 — "채널% = above-min ≤ iso, iso 명시" — 의 정반대다.)

### 18.6 ⚠ **신규(경미)** — Fig 5 캡션의 원소 배치 표기 2건이 틀렸다

Fig 5 캡션 원문: *"f) PDOS for **S 2p** in LPSC and **Y 3d** in LPSC-YO."*

- **S 2p → S 3p**: S 2p는 결합에너지 ~162 eV의 **내각 준위**(그들 XPS Fig 1g가 재는 바로 그것)다.
  −6…+6 eV 창의 가전자대 곡선은 **S 3p**다. 그림 범례 자체는 "S-p"로 옳게 적혀 있어 캡션만 오염.
- **Y 3d → Y 4d**: Y(Z=39)는 [Kr]4d¹5s². **3d는 Y에 존재하지 않는 껍질**이다. 본문(p. 8)은 "Y-d"로만 써서 무사.

> 실질 해석엔 영향 없지만, **XPS 표기와 가전자 PDOS 표기를 섞어 쓴 흔적**이라 §13-10(전반적 교정 품질)에 합류한다.
> 우리 쪽 함의: 우리 캠페인의 표준 서술자가 **site-PDOS ⟨S 3p⟩ mean-3p**이므로,
> 이 논문을 인용할 때 "S 2p"로 옮겨 적으면 우리 지표와 충돌한다 — **인용 시 S 3p로 교정할 것.**

### 18.7 ✅ **재확인(신규 수치)** — Fig 2f CV 전류 실측

| 특징 | LPSC | LPSC-YO | 비 |
|---|---:|---:|---:|
| 환원 피크 전류 (~0 V) | −0.24 mA | −0.15 mA | 0.62× |
| 재산화 피크 (~0.45 V, P³⁻→P⁰) | +0.070 mA | +0.030 mA | 0.43× |
| >2.5 V 산화 전류 | ~0.02 mA | ~0.02 mA | **~1×** |

> 1차 §5.5의 판정("onset은 사실상 동일, 전류 크기만 차이")을 **수치로 확정**한다.
> 고전압 쪽은 **두 시료가 구별되지 않는다** — 논문 본문도 이건 정직하게 인정한다
> ("LPSC-YO electrolyte also shows similar results, thus surface modification strategy need be carried out
> when matching well with high voltage cathode").
> ⇒ 이 논문은 **음극축 논문**이라는 1차 결론이 CV 전류로도 확인된다. 축 B(산화)에는 이식 금지.

### 18.8 ⚠ **신규(경미)** — Arrhenius 창이 **35 K**뿐이다

Fig 2b의 x축 데이터 범위는 1000/T ≈ **3.00 → 3.35**, 즉 **T ≈ 333 → 298 K (25–60 °C)**, 5점.
5개 조성의 Ea 차이가 최대 0.040 eV인데, 이 폭의 창에서 5점 회귀로 뽑은 값이다.

> 오차막대·반복셀(n)이 없어 **0.380 vs 0.340의 유의성을 판정할 수 없다.**
> §13-12(통계 전무)에 합류. 인용 시 "25–60 °C, 단일 셀, 오차 미보고" 단서 필수.

### 18.9 ⚠ **신규(경미)** — 0.5C 용량이 두 그림에서 다르다

- Fig 6b (rate test): 0.5C = **86.1 mAh/g**
- Fig 6d (장기 사이클): 0.5C **초기 방전 91.9 mAh/g**

91.9는 Fig 6b의 **0.4C 값과 정확히 같은 숫자**다. rate 시험과 사이클 시험이 다른 셀일 수는 있으나,
같은 0.5C에서 6.7% 차이 + 인접 rate 값과의 일치는 **전사 오류를 의심할 만하다**. §13-10에 합류.
(수명 서사 자체엔 영향 없음 — 오히려 §13-11의 "저활용률" 논점을 강화한다: 91.9는 0.1C 122.2의 **75%**.)

### 18.10 이번 패스가 바꾼 것 / 안 바꾼 것

| | |
|---|---|
| **채워짐** | §3 밴드갭 칸(미보고 → 그림 실측 ~2.1/~2.55 eV), §12 밴드갭 행(비교 불가 → **정합**) |
| **강해짐** | §6.4-③ BVSE 판정(+표본 비대칭 §18.5) · §13-12 통계 전무(+§18.8) · §13-10 교정 품질(+§18.6, §18.9) |
| **뒤집힘** | 없음 |
| **신규 비판** | §18.1(PDOS 주장이 자기 그림에 반박됨 — **1차의 "용어 부정확"에서 "사실 오류"로 승격**), §18.4(σ₀ 방향 모순) |
| **신규 우호 소견** | §18.2·§18.3 — 그들 PBE PDOS는 **우리 comp1 gap·VBM(S 3p)·O 2p 매몰을 독립 확인**해준다. 이 논문에서 우리가 **믿고 쓸 수 있는 계산 결과는 사실상 이 세 가지**(그리고 논문이 강조하지 않는 것들)다 |

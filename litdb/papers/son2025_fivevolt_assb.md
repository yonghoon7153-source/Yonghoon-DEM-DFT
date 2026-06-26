# Five-volt-class high-capacity all-solid-state lithium batteries — Son et al. (Nature Energy 2025)

> slug `son2025_fivevolt_assb` · DOI `10.1038/s41560-025-01865-y` · type `exp (+ DFT 보조)` · PDF `ec535528-27._Fivevoltclass…assb.pdf` · digested `2026-06-26` · status ✅
> **저자**: Jun Pyo Son, Juhyoun Park, Hae-Yong Kim, Jae-Seung Kim (공동1저); … Dong-Hwa Seo (KAIST), Kyung-Wan Nam (Dongguk), **Yoon Seok Jung (Yonsei)** (교신). Yonsei·Dongguk·KAIST·UNIST·POSTECH·PAL·BNL.
> **소속 판정**: **[외부]** — Yonsei(정윤석)·Dongguk(남경완)·KAIST(서동화) 중심. **우리 그룹(한양대 Jong-Won Lee / Yong Min Lee / Kuk Young Cho 계보) 아님**. ⚠ Yonsei = 우리 그룹 동반 [KimICCF]/[KimCA]의 Yong Min Lee와 *같은 학교지만 다른 그룹*(정윤석 ≠ 이용민) → "우리 그룹"으로 태그 금지.
> Nature Energy 10, 1334–1346 (2025년 11월호). Received 2024-07-30, Accepted 2025-08-11.

---

## 0. 이 digest를 읽는 법 — **우리 산화/코팅 서사의 실험 캡스톤**
이 논문은 우리 litdb의 **[Banik] "S-pin → 황화물 SE는 intrinsic하게 고전압 못 감 → 코팅/타 물질군 필요"** 명제의, 그리고 우리 그룹 **cathode-interface 3부작([Cha]/[Kang25]/[Kang])**의 "**계면을 관리/차단해야 고전압 NCM-LPSCl이 산다**"는 문제설정의, **정면 실험 캡스톤**이다. 다만 이 논문이 택한 답은 *황화물의 계면 관리*가 아니라 **황화물·산화물 코팅을 *버리고* 새 불소계(fluoride) SE — LiCl–4Li₂TiF₆ (이하 LiCl–4LTF) — 를 차폐층(shielding layer)으로 쓰는 것**이다.

핵심 줄거리:
1. **5 V급 양극(Mn 스피넬 LiNi₀.₅Mn₁.₅O₄, LNMO)** 을 ASSB에서 쓰려면, 그 표면과 접하는 물질이 **>5 V에서 산화 안정**해야 한다.
2. **황화물 SE(LPSCl 포함)는 이게 불가능** — 본문이 직접 "sulfide SEs exhibit limited electrochemical stability (<2.5 V vs Li/Li⁺)"라고 명시(p.1334). 우리 grand-potential 2.256 V(S²⁻-limited)·[Banik] S-pin과 **정확히 같은 진단**.
3. **할라이드(chloride) SE도 ~4.3 V부터 분해** 시작("degradation initiates above ~4.3 V" for chloride SEs, p.1335) — Li₃YCl₆·Zr-oxychloride가 3.7/4.1 V부터 산화전류. 5 V는 못 감.
4. **기존 코팅(LiNbO₃ = LNbO)** 은 산소방출로 분해·실패.
5. **해법 = LiCl–4LTF (불소계 SE)** — >6.7 V까지 산화 안정(Li₂TiF₆ 기준), σ = 1.7×10⁻⁵ S/cm(불소계 중 최고급, Li₂TiF₆보다 ~2 자릿수↑). 이 층을 LNMO에 dry-coating하면 5 V급에서 셀이 돈다: 106 mAh/g @2C·500 cyc·75.2 % retention.

> ⚠ **전압 기준**: 본문은 셀 측정 대부분 **Li/Li⁺ 또는 In/InLi** 혼용. CV·코팅셀 그래프는 *vs Li/Li⁺*(LNMO 4.7 V 평탄), full-cell·CCD는 *vs Li-In* (오른쪽 축). **5 V급·4.7 V·6.7 V는 모두 Li/Li⁺ 기준.** 우리 grand-potential(2.256 V vs Li/Li⁺)과 비교할 땐 같은 Li/Li⁺ 기준이라 직접 정합.

---

## 1. 한 줄 요약
황화물(LPSCl, <2.5 V)·할라이드(>4.3 V 분해)·기존 산화물코팅(LiNbO₃, 산소방출 분해) 모두 5 V급 LNMO 양극을 못 버틴다 — **새 불소계 SE인 LiCl–4Li₂TiF₆(σ 1.7×10⁻⁵ S/cm, 산화안정 >6.7 V)** 를 차폐층으로 쓰면 LNMO가 5 V급에서 안정(106 mAh/g·2C·500 cyc·75.2 % retention) + 초고면적용량 35.3 mAh/cm² 달성. **"황화물 SE는 고전압 직접접촉 불가 → 산화안정 차폐 SE가 필요"** 라는 우리 산화/코팅 서사를 실험으로 못박는 캡스톤.

## 2. 메타 / 동기
| 항목 | 내용 |
|---|---|
| 핵심 신소재 | **LiCl–4Li₂TiF₆ (LiCl–4LTF)** — 불소계(fluoride) SE/차폐층. xLiCl–(1−x)Li₂TiF₆, **x=0.2 최적** |
| 양극(고전압) | **LiNi₀.₅Mn₁.₅O₄ (LNMO)** = 5 V급 Mn 스피넬(Ni²⁺/Ni⁴⁺ @~4.7 V). + 검증용 LiCoMnO₄(LCMO, 5.3 V), LiFe₀.₅Mn₁.₅O₄(LFMO), Li-rich layered |
| 분리막 SE | **Li₅.₅PS₄.₅Cl₁.₅ (LPSCl)** = 황화물(우리 modelc 근처 조성), 일부 셀은 Li₃YCl₆/Zr-oxychloride |
| 질문 | (a) 왜 기존 SE/코팅은 5 V를 못 버티나? (b) 산화안정 + 고-σ를 동시에 가진 차폐 SE를 어떻게 만드나? |
| 비교군 | **Bare LNMO** vs **LiNbO₃-coated (LNbO)** vs **LiCl–4LTF-coated** (+ liquid electrolyte 대조) |
| 갭 | 황화물·할라이드 SE는 고전압서 분해; 불소계는 산화안정하나 **σ가 극도로 낮아**(Supplementary Table 3) 차폐층으로 거의 미탐구 → 이 논문이 σ 2 자릿수↑로 돌파 |

## 3. 핵심 물성 (수치 총정리)
### 3.1 LiCl–4LTF 자체 (신소재)
| 물성 | 값 | 조건/출처 |
|---|---|---|
| 조성 최적 | **x=0.2: 0.2LiCl–0.8Li₂TiF₆ = LiCl–4Li₂TiF₆** | Fig 1a (xLiCl–(1−x)Li₂TiF₆, x=0–0.4 스캔) |
| **σ_Li⁺ (RT, 30 °C)** | **1.7×10⁻⁵ S/cm** | Fig 1a. Li₂TiF₆(5.8×10⁻⁸)보다 **>2 자릿수↑**, 불소계 SE 중 최고급 |
| 활성화E Ea | **0.53 eV** | Fig 1a Arrhenius |
| σ_e (전자전도) | 4.69×10⁻⁹ S/cm | Supplementary (낮음=좋음, 전자절연) |
| **산화안정(분해 onset)** | **>6.7 V** (Li₂TiF₆ 기준, grand-potential 계산) | Fig 3b·Supplementary Table 40. CV는 LiCl–4LTF·Li₂TiF₆ 둘 다 **5.5 V까지 산화전류 미미** |
| 합성 | mechanochemical (LiCl + LiF + TiF₄ ball-mill) | Methods. ZrO₂–2Li₂ZrCl₆ 등도 동일 |
| 결정구조 | tetragonal P4₂/mnm (ICSD 256029) Li₂TiF₆ + cubic LiCl, **불순물상 없음** | Fig 1b–d (synchrotron HRPD) |
| 건조대기 안정성 | reasonable dry-air stability | Supplementary Note 1 |

### 3.2 LiCl–4LTF-coated LNMO 셀 성능 (5 V급)
| 물성 | LiCl–4LTF | LNbO(LiNbO₃) | Bare | 조건 |
|---|---|---|---|---|
| 초기 방전용량 (0.1C) | **130 mAh/g** | 108 | 37 | Fig 3d, CAM 5.5 mg/cm², 70 MPa, 30 °C |
| rate 2C 용량 | **93.3 mAh/g** | < | < | Fig 3e ("unparalleled") |
| **2C·500 cyc retention** | **75.2 %** (106 mAh/g @2C) | 분해·실패 | — | Abstract·Conclusion |
| 1C·200 cyc retention | **77.1 %** | LNbO 급격 fade(<10 cyc) | — | Fig 3f, 120 mA/g |
| 계면저항 R_int (50 cyc 후) | **0.1 kΩ·cm²** | b-LNbO 1.96 / LNbO 0.65 kΩ·cm² | — | Supplementary Figs 40–41 |
| ESW (코팅 LNMO, vs Li/Li⁺) | **3.0–5.3 V 안정** (35.3 mAh/cm²) | — | — | 본문 p.1335 |

### 3.3 초고면적용량·후막·확장
| 물성 | 값 | 조건 |
|---|---|---|
| **초고면적용량** | **35.3 mAh/cm²** (137 mAh/g) | Fig 5f, CAM **257.4 mg/cm²**, **1.8 mm 후막** 전극, 70 MPa, 30 °C |
| 에너지밀도 (vs 5 mAh/cm² 통상) | 57 %↑ (718→**958 Wh/L**급) | 본문 p.1342 (LNMO 704 Wh kg_CAM⁻¹) |
| **저전압 확장(2.3 V cutoff)** | **258 mAh/g** (959 Wh kg_CAM⁻¹) | Fig 5c, Ni²⁺/Ni⁴⁺(146)에 더해 Mn³⁺/⁴⁺ @~2.7 V 활용; 2.3–5.0 V |
| LCMO(5.3 V급) | 88 mAh/g·50cyc 82.0 % | Fig 5a, LCMO|(ZrO₂–LZCF)|LPSCl|Li-In, 3.0/5.3 V |
| LFMO | 132 mAh/g @0.1C | Fig 5b, 3.0/5.3 V |
| pouch full cell (LNMO|Li) | — | Fig 5d,e, 11.8 mg/cm², 5 MPa, 200 cyc |
| pouch (LNMO|Ag-C anode-less) | 5 MPa@30 °C 작동 | Methods |

### 3.4 **다른 SE/코팅의 산화 한계 (= 우리 산화 서사 직접 데이터)** ★
| 물질 | 산화전류 onset (vs Li/Li⁺) | 출처 |
|---|---|---|
| **황화물 LPSCl** | "**<2.5 V**" 명시 (intro, p.1334) | 본문 + Fig 3b operating-window 막대 |
| Li₃YCl₆ (LYC, 할라이드) | **3.7 V**부터 산화전류 (CV Fig 3a) | Fig 3a,b |
| ZrO₂–2Li₂ZrCl₆F (Zr-oxychloride) | **4.1 V**부터 | Fig 3a,b |
| 할라이드(일반) | "degradation initiates above **~4.3 V**" | p.1335 |
| LiNbO₃ (기존 코팅) | **3.86 V**까지만 안정, 그 위 산소방출 분해 | Supplementary Table 40, Fig 4k |
| **Li₂TiF₆ / LiCl–4LTF** | **5.5 V까지 미미, 계산 >6.7 V** | Fig 3a,b |

## 4. 재료 & 방법
- **합성**: 모두 mechanochemical(ball-mill). LiCl–4LTF = LiF + TiF₄ + LiCl (질량비 1/45, 190 rpm 10 h). LPSCl(σ 3 mS/cm), Li₃YCl₆, ZrO₂–LZCF(=ZrO₂–2Li₂ZrCl₆F from Li₂O+ZrCl₄+ZrF₄), LiNbOCl₄ 등.
- **코팅**: LNMO에 LiCl–4LTF를 **mechanical dry-coating**(ZrO₂ ball, 200 rpm 1 h) — 5 wt% LNbO sol-gel과 대비. SEM/EDXS로 수백 nm LiCl–4LTF 입자가 LNMO 표면 분포 확인(Fig 3c, O/F 맵).
- **셀**: SE/C CV는 (SE+C)|LPSCl|(Li-In). 코팅셀 = LNMO|(ZrO₂–LZCF)|LPSCl|(Li-In), 3.0–5.0 V, 0.1C(12 mA/g). full = LNMO|LPSCl|Li(또는 Ag-C), 30 µm Li.
- **분석기법**: synchrotron HRPD(PAL 9B·NSLS-II) + Rietveld(Fullprof) · XAS(Cl/Ti/Nb K-edge, TEY+TFY; Demeter) · PDF(G(r), Q 0.1–21 Å⁻¹; xPDFsuite) · in-situ XRD(SOC 추적) · ToF-SIMS · ex-situ XPS · HRTEM·HAADF-STEM-EELS(Mn L-edge) · ⁷Li MAS-NMR · Raman/IR · HF sensor.
- **이론(DFT)**: §8 참조. grand-potential 분해창 + AIMD(σ 메커니즘) + enumeration(무질서) + interface pseudo-binary ΔE_rxn.

## 5. 결과 — 섹션별 상세

### 5.1 LiCl–4LTF 특성화 (Fig 1)
- **σ 돌파(Fig 1a)**: x=0.2서 σ 1.7×10⁻⁵ S/cm(30 °C)·Ea 0.53 eV. 불소계 SE 중 최고, Li₂TiF₆(5.8×10⁻⁸)보다 >2 자릿수↑. (그래도 황화물 mS/cm 대비 ~2.5 자릿수 낮음 — *차폐층*이라 OK.)
- **구조(Fig 1b–d)**: Li₂TiF₆ = TiF₆·LiF₆ 팔면체 골격(tetragonal P4₂/mnm). HRPD·XAS·PDF·XPS·XRF 종합 → **합성 중 Cl 손실** + **Li₂TiF₆ 표면영역에서 Ti⁴⁺→Ti³⁺ 환원(reduced Li₂TiF₆)**. Cl K-edge XAS(Fig 1e): 2,820/2,826 eV pre-edge = Ti–Cl 공유결합(Cl1s→Ti3d 혼성) → Cl이 **표면국소영역에서** Li₂TiF₆ 격자에 치환(bulk 균일 아님).
- **Ti L-edge TEY(Fig 1f)**: t₂g/eg 비 0.700→0.644(표면) = 표면에서 Ti⁴⁺ 환원. PDF(Fig 1g)·HAADF-STEM-EELS가 표면 국소 구조 불균일 확증.

### 5.2 σ 향상 메커니즘 — DFT (Fig 2) ★
- enumeration으로 3 모델구조 제안: ① Li 증가(Li₂.₁₂₅TiF₆, Cl₂ 방출+Ti 환원), ② Cl 치환(Li₂TiF₅.₈₇₅Cl₀.₁₂₅), ③ 둘 다(Li₂.₁₂₅TiF₅.₈₇₅Cl₀.₁₂₅). 형성E 계산 → 자발형성 확인.
- **AIMD(Fig 2c)**: Cl 치환·Li 증가 둘 다 D↑. Li₂.₁₂₅TiF₅.₈₇₅Cl₀.₁₂₅가 가장 완만한 Arrhenius 기울기(낮은 Ea). topology 분석(Fig 2b): **Cl 치환이 큰 음이온 도입으로 Li 채널을 distort·확장** → channel size 분포 우측 이동. Li 확률밀도(Fig 2d)도 Cl/Li 증가 시 확장.
- 결론: **σ 향상 = (a) Cl 치환에 의한 Li 운반자 농도↑ + 채널 확장 + (b) reduced Li₂TiF₆의 Li 증가** — 둘 다 **표면영역**에서 우세(bulk는 Li₂TiF₆ with Ti⁴⁺ 유지).

### 5.3 **CV — 다른 SE의 산화 한계 (Fig 3a,b)** ★★ — *우리 산화 서사 직접 데이터*
- (SE+C)|LPSCl|(Li-In), 0.1 mV/s, 5.5 V까지.
- **Li₃YCl₆ 3.7 V·ZrO₂–LZCF 4.1 V부터 큰 산화전류** vs **Li₂TiF₆·LiCl–4LTF는 5.5 V까지 산화전류 미미**(Fig 3a 인셋).
- Fig 3b 막대: SE 산화안정창 + 차폐물질 + CAM 작동창을 한 그림에. LPSCl·LYC·Zr-oxychloride < LiNbO₃(3.86 V) ≪ **Li₂TiF₆(>6.7 V)**. CAM 작동: NCM 4.x·**LNMO ~4.9 V·LiCoMnO₄ 5.3 V**.
- 🔑 **이게 우리 핵심**: "황화물 LPSCl <2.5 V"가 *본문 그림으로* 박혀 있음. 우리 grand-potential 2.256 V·[Banik] S-pin과 **같은 진단** + 할라이드도 ~4 V 한계 → **5 V는 불소계만 가능**.

### 5.4 코팅 LNMO 셀 (Fig 3d–f)
- 초기 충방전(Fig 3d): LiCl–4LTF 130 > LNbO 108 > Bare 37 mAh/g. ~4.0 V까지 sloping(Mn³⁺/⁴⁺)은 비슷하나 **Ni²⁺/⁴⁺ 고전압 영역(4.7 V)서 발산** — bare/LNbO는 분극·부반응으로 용량↓.
- rate(Fig 3e): LiCl–4LTF가 2C 93.3 mAh/g로 압도. 율속 순위 LiCl–4LTF > LNbO ≈ liquid > b-LNbO > Bare.
- 장기(Fig 3f, 1C 200 cyc): LiCl–4LTF **77.1 % retention** vs **LNbO 급격 fade(<10 cyc)** — LNbO는 고전압서 산소방출로 분해·실패. EIS: 50 cyc 후 R_int LiCl–4LTF **0.1** ≪ LNbO 0.65 ≪ b-LNbO 1.96 kΩ·cm².

### 5.5 **LNbO vs LiCl–4LTF 계면 (Fig 4)** ★ — *분해 메커니즘*
- HRTEM/FFT(Fig 4a–d): **LNbO-coated LNMO**는 cycling 후 표면에 **Mn₃O₄ 스피넬상** 출현(LNMO spinel→Mn₃O₄) + ~10 nm amorphous LNbO 직하. **LiCl–4LTF-coated**는 cycling 후에도 core·표면 모두 **결정구조 유지**.
- STEM-EELS Mn L-edge(Fig 4e,f): LNbO엔 표면 **Mn 환원**(Mn₃O₄), LiCl–4LTF엔 없음.
- ex-situ XPS(Fig 4g,h)·ToF-SIMS(Fig 4i,j): **LNbO**서 Y₂O₃·YOCl·ClOₓ·YO⁻·OCl⁻ 진화 = catholyte(LYC) 불안정 + **LNbO 분해 시 산소방출**(Nb K-edge XANES). **LiCl–4LTF**서는 Y₂O₃·ClOₓ 미미.
- **메커니즘(Fig 4k,l)**: LNbO 고전압 불안정 → 산소방출 동반 부반응 → 절연성 **Mn₃O₄** 계면형성 → 저항↑·실패. LiCl–4LTF는 안정·intact → 저항↓.

### 5.6 다양한 시스템 검증·확장 (Fig 5)
- **LCMO(5.3 V급, Fig 5a)**: LiCl–4LTF로 88 mAh/g·50cyc 82.0 %. → **5.3 V까지 push 가능**.
- **LFMO(Fig 5b)**: 132 mAh/g, 저원가 Co-free.
- **LNMO 저전압 확장(Fig 5c)**: 2.3 V cutoff서 **258 mAh/g**(Mn³⁺/⁴⁺ @2.7 V 추가 활용) = 959 Wh kg_CAM⁻¹.
- **pouch(Fig 5d,e)**: LNMO|LPSCl|Li, 200 cyc 안정. anode-less(Ag-C)도 작동.
- **초고면적용량(Fig 5f–i)**: 1.8 mm 후막·257.4 mg/cm²로 **35.3 mAh/cm²**(137 mAh/g) — ASSB 최고급, 통상 5 mAh/cm² 대비 57 % 에너지↑.

## 6. 메커니즘 종합
1. **고전압 양극(LNMO 4.7 V·LCMO 5.3 V) 작동 = 표면 접촉물질의 산화안정성이 율속.**
2. **황화물(LPSCl <2.5 V)·할라이드(~4 V)·기존 산화물코팅(LiNbO₃ 3.86 V) 전부 부족** → 고전압서 산화분해·산소방출·절연상(Mn₃O₄) 형성 → R_int↑·용량fade.
3. **불소계 LiCl–4LTF는 >6.7 V 산화안정 + σ 1.7×10⁻⁵**(불소계로 이례적 고-σ, Cl 치환·Li 증가가 채널 확장) → 차폐층으로 LNMO를 SE/CAM 분해에서 격리.
4. 결과: 5 V급 LNMO·5.3 V LCMO가 ASSB에서 장수명 + 초고면적용량.

## 7. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`
| 항목 | 이 논문 (Son) | 우리 (DFT) | 일치 / 이유 |
|---|---|---|---|
| **황화물 SE 산화 한계** | LPSCl "**<2.5 V**" 명시(intro·Fig 3b) | comp1/modelc grand-potential onset **2.256 V**(S²⁻-limited, LiS4 제외; 포함 2.14) | **✓✓✓ 정량 일치** — 우리 2.256 V가 본문 "<2.5 V"와 직접 부합. 우리 0-pressure thermo onset이 본문 정성진술의 *수치 근거* |
| **왜 황화물이 고전압 못 가나** | "limited electrochemical stability" (정성) | **VBM=S 3p가 산화 onset을 pin**(S²⁻→S⁰), 치환 무관 | **✓ 메커니즘 보강** — 본문은 *현상*만, 우리+[Banik]가 *원인*(S backbone). 둘 상보 |
| **할라이드 SE 산화** | LYC 3.7·Zr-oxychloride 4.1·"~4.3 V부터 분해" | (우리 hull에 Y/Zr 없음 → 미계산) ⚠ | △ **범위 밖** — Cl-Li-Nd-O-P-S 6원소 hull에 Y/Zr 없음 → 정량 불가. [Cha] Zr-hull 향후과제와 동일 gap |
| **차폐 SE(불소계) 산화안정** | LiCl–4LTF >6.7 V (grand-potential) | (우리 Ti/F hull 없음 → 미계산) | △ **범위 밖** — 단 *방법은 동일*(grand-potential 분해창) → 우리 도구로 재현 가능한 chemsys |
| **고전압 분해 산물** | LNbO→산소방출→Mn₃O₄; bare LNMO 부반응 | 우리 interface_reactivity·산화 staircase(P₂S₅계+S+LiCl) | △ **다른 양극계**(LNMO spinel/O-release vs LiCoO₂) → 직접 산물비교 부적절. 단 "고전압 O방출→절연상" 큰 그림은 [Zuo]/[Kang25] O-release와 결 같음 |
| **modelc 조성** | LPSCl = Li₅.₅PS₄.₅Cl₁.₅ (분리막) | modelc = Li₅.₄PS₄.₄Cl₁.₆ (근접, 동일시 금지) | — 본문 LPSCl는 *분리막*(고전압 직접접촉 안 함, 차폐가 보호); 우리 modelc도 같은 Cl-rich 패밀리 |
| **σ (Cl 치환 효과)** | LiCl–4LTF서 Cl 치환→채널 확장·σ↑(AIMD) | modelc Cl-rich D↑ 2.6×·채널 확장(disorder) | **✓ 결 동일** — *다른 모재*(TiF₆ vs PS₄)지만 "큰 음이온 도입→Li 채널 distort/확장→D↑" **메커니즘 동형**. 단 절대 σ·Ea 직접비교 금지(모재 다름) |
| **DFT functional/방법** | VASP/PBE/PAW/520 eV/enumeration/AIMD-NVT | 우리 VASP-등가/PBE/AIMD(UMA-MLIP surrogate)/grand-potential | **✓ 동일 백본** — grand-potential(pymatgen)·AIMD-MSD→D·enumeration 모두 우리 노선 |

> **핵심 정직성**: 이 논문은 **불소계(Ti/F)·할라이드(Y/Zr) chemsys** 라 우리 6원소 hull(Cl-Li-Nd-O-P-S)로 *수치 재현 불가*. 비교는 **(a) 황화물 LPSCl 산화 한계(우리 2.256 V ↔ 본문 <2.5 V, ✓✓✓), (b) σ 향상 메커니즘(Cl→채널확장, 결 동일), (c) 방법 백본 동일** 세 곳에서만 엄밀하고, 차폐 SE 자체 수치는 "방법은 같으나 우리 hull 밖"으로 정직히 한정.

## 8. DFT/계산 방법 ★
- **code / version**: VASP (Vienna Ab-initio Simulation Package).
- **functional + vdW**: **GGA-PBE**. vdW 언급 없음(불소계 이온결정 → vdW 비핵심).
- **pseudo / PAW**: **PAW (projector-augmented wave)**.
- **k-points / ecut / supercell / nat**: plane-wave cutoff **520 eV**; cell/atomic position relax **forces <0.05 eV/Å**; Li₂TiF₆ 초기구조 = MP **mp-7603**; **2×2×1 supercell** (a=b=9.20152, c=8.84076 Å) 전 DFT 공통; AIMD는 **1×1×1 supercell**, **Γ-centered** k-grid.
- **DFT+U**: 명시 없음(n/a — Ti⁴⁺/³⁺이나 U 미적용 추정).
- **AIMD**: **NVT ensemble**, **Nosé–Hoover thermostat**(period 80 fs), **2 fs step**, **200 ps**/온도, 100 K→holding(1,000–1,400 K) 2 ps 가열 후. D = MSD 선형피팅(pymatgen diffusion analyzer).
- **MLIP**: 없음(전 ab-initio).
- **무질서 처리** ★: **enumeration method** — partial occupancy 자리의 가능한 원자배열을 체계적으로 생성. **pymatgen TopographyAnalyzer**로 Li 삽입자리 preselect(16 tetrahedral) → 30 config 중 **lowest Ewald-summation** 선택 → DFT relax 후 **lowest total energy** 채택. Cl 치환은 48 F 자리서 비율맞춰 enumerate. (= SQS 아님, *enumerate→Ewald→DFT lowest-E* 노선)
- **계면 안정성(interface pseudo-binary)**: ΔE_rxn(C_SE, C_CM, x) = E_eq(xC_SE+(1−x)C_CM) − xE(C_SE) − (1−x)E(C_CM). LNMO **fully delithiated(Ni₀.₅Mn₁.₅O₄)** 기준, SE formula unit당 정규화.
- **grand-potential 분해창** ★: **pymatgen**의 grand potential phase diagram. ΔE_D = E_eq(phase equilibria, µ_Li) − E_material(phase) − Δn_Li·µ_Li. **환원·산화 onset 둘 다** µ_Li 함수로 결정. MP 안정상 사용, MP에 없는 상은 동일 DFT 파라미터로 별도 계산. → **우리 `oxidation_stability` grand-potential과 정확히 동일 방법**.
- **topology**: **Zeo++**로 AIMD 궤적의 Li 채널 크기 분석(Fig 2b). diffusion channel size from Li trajectory.

## 9. Figure set ★
| Fig | 내용 | 우리 활용 |
|---|---|---|
| 1a | xLiCl–(1−x)Li₂TiF₆ Arrhenius σ (x=0.2 최적 1.7×10⁻⁵) | 불소계 SE σ landscape(차폐층 σ 요건) |
| 1b–d | Li₂TiF₆ 결정구조·HRPD·Rietveld(불순물 없음) | 구조 정량(우리 직접 활용 적음) |
| 1e | **Cl K-edge XAS** pre-edge(Ti–Cl 공유) | Cl 치환 국소 동정법(우리 Cl XAS 참고) |
| 1f | Ti L-edge TEY(표면 Ti⁴⁺→³⁺) | 표면 환원 동정 |
| 1g | **PDF G(r)** 단거리 구조 불균일 | PDF로 계면 불균일 보는 법 |
| 2a–d | **DFT/AIMD σ 메커니즘** (enumerate 구조·channel size·Arrhenius·Li 확률밀도) | **Cl 치환→채널 확장→D↑** = 우리 modelc Cl-rich 메커니즘의 *타 모재 동형 증거* |
| **3a** | **CV: LYC 3.7·Zr-OCl 4.1·Li₂TiF₆ >5.5 V 산화전류** | ★ **우리 산화 서사 직접 데이터** — 황화물/할라이드 한계 vs 불소계 안정 |
| **3b** | **SE 산화창 + 차폐물질 + CAM 작동창 막대** | ★★ **"LPSCl<2.5 V·할라이드~4 V·LiNbO₃ 3.86·Li₂TiF₆ 6.7 V" 한 그림** — deck 산화 슬라이드에 *그대로* 인용 |
| 3c | SEM/EDXS 코팅 LNMO(O/F 맵) | dry-coating 형태 |
| 3d–f | 코팅 LNMO 충방전·rate·200cyc | 코팅 효과 정량(130 vs 37 mAh/g) |
| **4a–l** | **LNbO vs LiCl–4LTF 계면**(HRTEM·EELS·XPS·ToF-SIMS·메커니즘) | ★ 고전압 코팅 분해 메커니즘(산소방출→Mn₃O₄) = [Kang25]/[Zuo] O-release 결 |
| 5a–i | LCMO 5.3 V·LFMO·저전압확장·pouch·35.3 mAh/cm² | 범용성·초고용량 |
| ED Fig 1 | Ni-rich·Li-rich layered도 LiCl–4LTF 효과 | 차폐 SE 일반성 |

## 10. Post-processing ★
- **grand-potential ESW**(pymatgen): SE·차폐물질 산화/환원 onset을 µ_Li 함수로. 기록 = onset V(Fig 3b 막대)·Supplementary Table 40. → **우리 oxidation_stability.json과 동일 산출물·동일 도구**.
- **interface pseudo-binary ΔE_rxn**(pymatgen): SE–CAM(delithiated) 반응E. 기록 = eV/f.u.
- **AIMD-MSD→D**(pymatgen diffusion analyzer) + Arrhenius Ea + **Zeo++ channel size** + Li 확률밀도. 기록 = D(T)·Ea·channel 분포(violin).
- **enumeration**(pymatgen, TopographyAnalyzer + Ewald): 무질서/부분점유 → 대표구조.
- **XAS**(Demeter/Athena): Cl/Ti/Nb K-edge, pre-edge·white-line·TEY vs TFY(표면 vs bulk).
- **PDF**(xPDFsuite, Dioptas): G(r) 단거리, 계면 불균일.
- **HAADF-STEM-EELS**(Mn L-edge): 산화상태 line-scan(Mn₃O₄ 검출).
- **ToF-SIMS·XPS**: 분해종(Y₂O₃·ClOₓ·YOCl·OCl⁻) depth/표면.
- **in-situ XRD**: SOC(격자) 추적.
> 우리 적용: **grand-potential 차폐물질 스크린**(우리 도구로 Ti/F·Y/Zr chemsys 확장 시 직접 차용 가능) + **Cl 치환→채널 확장 AIMD/Zeo++ 틀**이 우리 modelc 메커니즘과 동형.

## 11. 우리 그룹 cathode-interface 3부작·산화 서사와의 연결 ★★
> 이 논문은 **[Banik] "S-pin→코팅/타 물질군 필요"** 와 우리 그룹 **[Cha]/[Kang25]/[Kang] "고전압 NCM-LPSCl 계면은 관리해야 산다"** 의 *실험적 캡스톤*. 다만 **답의 위치가 다르다** — 우리 그룹 3부작은 *황화물을 유지한 채 계면을 관리*(코팅/도핑/통합), Son은 *황화물·기존산화물을 버리고 새 불소계 SE로 교체*. 같은 문제설정(고전압 산화)에 대한 **두 갈래 해법** → deck에서 "황화물 계면관리(우리 그룹) vs 차폐 SE 교체(Son)"로 *나란히* 제시하면 산화 서사가 완성.

| 우리 자산 | 이 논문이 주는 것 | 정합·해석 |
|---|---|---|
| **우리 grand-potential 2.256 V (S²⁻-limited)** | LPSCl "**<2.5 V**" 본문 명시 + Fig 3b 막대 | **✓✓✓ 직접 정량 확증** — 우리 0-pressure thermo onset이 *Nature Energy 본문 진술*과 부합. "우리 계산이 5V 논문의 출발 전제를 수치로 뒷받침" |
| **[Banik] S-pin: 치환으론 황화물 산화창 못 늘림** | "5 V는 황화물·할라이드 다 불가, 새 물질군(불소계) 필요" — *물질군 교체로* 응답 | **✓ Banik 결론의 실험 실현** — Banik이 "코팅/타 물질군 필요"라 했고, Son이 *타 물질군(불소계 차폐 SE)* 으로 5 V 달성. **단 Banik은 SE intrinsic, Son은 차폐층** = 같은 결론의 다른 구현 |
| **우리 그룹 [Cha] 할라이드 dual-compat 코팅** | 할라이드(LYC/Zr-OCl)도 ~4 V서 분해 = **할라이드 코팅의 고전압 천장** | **✓ 보강·한계 동시** — [Cha] LZC가 NCM 4.x V엔 좋지만, **5 V급(LNMO)엔 할라이드도 부족**(Son Fig 3a) → 우리 그룹 할라이드 코팅 서사의 *전압 상한*을 Son이 명시. deck: "할라이드 코팅=NCM 4 V급 / 불소계 차폐=5 V급" |
| **우리 그룹 [Kang25] SE 코팅 SOC 균일화** | LiCl–4LTF dry-coating도 "코팅으로 계면 관리" 같은 철학 | **✓ 같은 큰 틀**(코팅으로 고전압 계면 보호) — 단 [Kang25]=황화물 자체코팅·SOC강하, Son=불소계 차폐·산화차단 = *다른 레버* |
| **우리 [Kang]/[Zuo] 고전압 O-release** | LNbO 분해 시 **산소방출→Mn₃O₄ 절연상**(Fig 4k) | **✓ O-release 보편성** — [Zuo] NCM O₂방출, [Kang25] NCM, Son LNMO·LNbO 모두 "고전압 O방출이 계면 분해 구동" — 우리 산화 staircase의 cathode-O 동반분해와 결 일치 |
| **우리 modelc Cl-rich σ↑(채널 확장)** | LiCl–4LTF서 Cl 치환→**채널 distort·확장→D↑**(AIMD, Fig 2) | **✓ 메커니즘 동형(타 모재)** — PS₄(우리) vs TiF₆(Son) *다른 골격*인데 "큰 음이온/Cl 도입→Li 채널 확장→D↑"가 **공통** → "Cl이 σ를 올리는 물리는 모재 무관하게 채널 확장"이라는 우리 주장의 외부 평행 |

🔑 **세 결론 (deck용)**:
1. **우리 산화 진단의 외부 캡스톤**: "황화물 LPSCl <2.5 V(우리 2.256 V·S-pin)·할라이드 ~4 V → 5 V는 둘 다 불가"가 *Nature Energy 본문 그림*(Fig 3b)으로 박힘. 우리 grand-potential·[Banik]이 *왜* 못 가는지(S backbone), Son이 *그래서 무엇이 필요한지*(불소계 차폐) — 진단-처방 한 쌍.
2. **우리 그룹 cathode-interface 라인의 전압 천장 표시**: [Cha] 할라이드 dual-compat 코팅은 NCM 4 V급엔 유효하나, **5 V급(LNMO)엔 할라이드조차 부족** → 우리 그룹 코팅 서사를 "4 V급 계면관리"로 정확히 위치시키고, 5 V급은 *물질군 교체(불소계)* 영역임을 분리. **이걸 명명 안 하면 우리 코팅 결론을 5 V로 over-extend하는 실수.**
3. **Cl→채널 확장 σ 메커니즘의 모재 무관 평행**: TiF₆계서도 Cl 치환이 우리 PS₄계 modelc와 같은 "채널 확장→D↑"를 줌 → 우리 Cl-rich σ↑ 물리가 골격에 robust.

## 12. 인용 가능 문장 (deck/paper용)
- "Son et al. (Nat. Energy 2025) explicitly place sulfide LPSCl oxidation below 2.5 V — quantitatively matching our grand-potential onset of 2.256 V (S²⁻-limited), and confirming that 5 V-class cathodes require an oxidatively stable shielding layer rather than direct sulfide contact."
- "Their result is the experimental realization of the Banik S-pin conclusion: since intrinsic sulfide oxidation cannot be raised by substitution, 5 V operation needs a different material class (here, a fluoride SE, LiCl–4Li₂TiF₆, stable to >6.7 V)."
- "Even halide SEs (Li₃YCl₆ 3.7 V, Zr-oxychloride 4.1 V) decompose well below 5 V — marking the voltage ceiling of our group's halide-coating line ([Cha]) at the ~4 V (NCM) regime, with 5 V-class spinels (LNMO/LCMO) requiring a fluoride shield."
- "Cl substitution widens the Li conduction channel and raises diffusivity in the TiF₆ framework just as it does in our PS₄ argyrodite (modelc) — the σ-boosting role of Cl is framework-robust."

## 13. 주의 / 한계 (over-claim 방지)
- **chemsys 불일치**: LiCl–4LTF(Ti/F)·LYC/Zr-OCl(Y/Zr) 모두 **우리 6원소 hull(Cl-Li-Nd-O-P-S) 밖** → 차폐 SE·할라이드 산화창 수치는 우리가 *재현 못 함*(방법만 동일). "우리가 6.7 V를 검증했다"식 금지.
- **"우리 grand-potential ↔ <2.5 V" 정합은 *황화물 LPSCl 한 줄*에서만 엄밀** — 나머지(불소계 6.7 V·할라이드 4 V)는 *본문이 계산한 것*이지 우리 값 아님.
- **양극계 다름**: Son = LNMO spinel(Mn₃O₄·O-release)·LCMO. 우리 interface_reactivity 기준은 LiCoO₂ → 분해 *산물*직접비교 부적절(큰 그림 O-release만 공유).
- **σ·Ea 절대값 비교 금지**: LiCl–4LTF σ 1.7×10⁻⁵·Ea 0.53 eV는 *불소계* — 우리 황화물 mS/cm·Ea 0.22–0.25와 비교 불가(차폐층 vs 분리막, 모재 다름). Cl→채널확장 *메커니즘*만 공유.
- **우리 그룹 아님**: Yonsei 정윤석/Dongguk 남경완/KAIST 서동화 — 한양대 Jong-Won Lee 라인 아님. Yonsei라도 이용민([KimICCF]/[KimCA])과 다른 그룹 → **[외부]**.
- **modelc ≠ Son LPSCl**: Son 분리막 = Li₅.₅PS₄.₅Cl₁.₅, 우리 modelc = Li₅.₄PS₄.₄Cl₁.₆ (동일시 금지).
- **DFT 디테일 일부 미공개**: DFT+U(Ti) 명시 없음; AIMD 1×1×1 셀(작음)·MLIP 없음 → 절대 D는 size/배열 민감.

## 14. 기법 용어 미니사전
- **fluoride SE (불소계 고체전해질)**: F⁻ 음이온 골격(여기 TiF₆²⁻). 산화안정성 높으나(F가 깊은 p-band) σ 낮음 — 이 논문이 σ 2 자릿수↑로 차폐층화.
- **shielding layer (차폐층)**: 고전압 양극과 SE/분해상을 *공간적으로 격리*하는 코팅/계면층. 산화안정 + 고-σ 필요.
- **5 V-class cathode**: ~5 V(vs Li/Li⁺)서 redox하는 양극 — LNMO(Ni²⁺/⁴⁺ 4.7 V), LiCoMnO₄(5.3 V), LiFe₀.₅Mn₁.₅O₄.
- **grand-potential phase diagram**: µ_Li를 변수로 SE의 환원/산화 분해 onset을 주는 열역학 도구(Mo 2012, pymatgen) — **우리 oxidation_stability와 동일**.
- **interface pseudo-binary ΔE_rxn**: SE와 CAM을 몰비 x로 섞었을 때 가장 안정한 convex-hull 에너지 − 두 끝점 = 계면 반응성(음수=분해).
- **enumeration (무질서 처리)**: 부분점유 자리의 모든 가능한 정수배열을 생성→Ewald/DFT로 최저E 선택 (SQS의 결정질 대안).
- **Mn₃O₄**: LNMO 스피넬이 고전압 부반응(산소방출)으로 표면에 형성하는 *절연성* 환원상 — R_int↑의 주범.
- **Zeo++**: 이온 궤적/다공구조의 채널(병목) 크기 기하분석 도구.
- **TEY vs TFY (XAS)**: total electron yield(표면 ≤수 nm) vs fluorescence yield(bulk) — 표면 vs 벌크 산화상태 분리.

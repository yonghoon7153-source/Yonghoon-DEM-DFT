# ⭐필독 / 우리-랩 — Customizing the Morphology and Microstructure of Single-Crystalline Ni-rich Layered Cathode Materials for All-Solid-State Batteries — Jung et al. (Chem. Eng. J. 2023)

> slug `jung2023_single_crystal_ncm_morphology` · DOI `10.1016/j.cej.2023.144381` · type `exp (morphology / electrochemistry / mechanical)` · PDF `Jung_2023_ChemEngJ_SingleCrystalNCM_Morphology_main.pdf` (+ `_SI.docx`) · digested `2026-06-26` · status ✅
>
> ## ★★★ 우리 랩(Hanyang, **Jong-Won Lee** 공동교신) 자체 논문 — 우리 DEM의 AM_P(다결정)/AM_S(단결정) 구분의 실험적 기초 ★★★
> 저자 = **Jae Yup Jung, KyungSu Kim, Joo Hyeong Suh, Hyun-seung Kim, Min Jae You, Kern-Ho Park, Jun Ho Song,
> Ji-Sang Yu, Jong-Won Lee\*(Hanyang Univ.), Woosuk Cho\*(KETI), Min-Sik Park\*(Kyung Hee Univ.)**.
> (Hyun-seung Kim, KyungSu Kim 은 다른 랩 논문 — Kim 2023/Kang 2025 — 과 저자 중복.)
> **이 논문은 Kang 2025의 reference [30]** 이며, **단결정(SC) vs 다결정(PC) NCM**이 ASSB에서 왜 다르게 거동하는지를
> 정한 우리 랩의 실험 기준점이다.  우리 DEM이 양극활물질(AM)을 **크기 + 종류(AM_P 다결정·큰 입자 vs AM_S 단결정)**로
> 나누는 그 구분의 **물리적·실험적 근거가 바로 이 논문**이다.
>
> > ★ **우리에게 왜 중요한가 (3줄):** (1) **PC = 우리 AM_P** (submicron 1차입자 응집체, 입계(GB)·내부 공극 보유, 균열
> > 취약), **SC = 우리 AM_S** (단결정 monolith, GB-less·공극 없음, 균열 억제, 더 단단·치밀) — 우리 DEM의 AM 분리가
> > 자의적 라벨이 아니라 *이 실험 물성 차이*에 뿌리를 둔다. (2) **PC는 깨지고 SC는 안 깨진다** (입계+내부공극 = 균열
> > 시드; SC 경도 972.7 MPa ≫ PC 113.3 MPa) → 우리 **Auerbach 파괴/fracture-aware σ(f_intact, frac_severe)** 에
> > *결정성(SC vs PC) 의존 파괴역치* 항을 실험으로 정당화한다. (3) **PC 입계·내부공극 = Li⁺/전자 ambipolar 확산
> > 병목**, SC monolith = 자유 확산 → 우리 **σ_electronic Trevisanello NCM(r) 내부-GB 보정항**의 실험적 근거.

---

## 1. 한 줄 요약
**단결정(SC)-NCM**(monolithic·입계없음·결함없음·고경도·고밀도)이 **다결정(PC)-NCM**(submicron 1차입자 응집체·입계+내부공극
보유)보다 **ASSB에서 더 우수**하다 — (i) SC는 SE와의 **친밀한 고체-고체 접촉 + monolith를 통한 향상된 (ambipolar)
Li⁺/e⁻ 확산**을, (ii) PC의 **입계·내부공극은 Li⁺/전자 전달 병목**이자 제조·사이클 중 **균열 시드**가 되어 비활성 파편을
고립시켜 용량을 떨어뜨리기 때문.  SC는 **미세균열·입자파괴를 억제**한다.  합성은 wet-milling(IPA)+post-heat
(675 °C/6 h O₂)로 morphology를 제어, ASSB(NCM:LPSCl:SuperP=60:35:5, 437 MPa, In/Li)에서 **SC 5C 용량유지 74.0 %
vs PC 41.6 %**, **150 cyc 유지 84.9 % vs 65.6 %**.

> ★ **주의 — 이 논문은 압밀 porosity나 σ(전도도)를 직접 정량 측정하지 않는다** (LIB·ASSB 전기화학 + morphology +
> 입자경도/밀도가 정량 앵커).  porosity·σ_ionic 칸은 n/a.  우리 압밀/전달 앵커(Minnmann 10 %, Bazzoun σ 등)와
> 직접 수치 비교 금지.  이 논문이 우리에게 주는 것은 **SC vs PC 라는 *재료 클래스* 차이의 정량 물성**(경도·밀도·
> 확산·균열·용량유지)과 그것이 ASSB 전달·역학에 미치는 *방향*이다.

## 2. 메타
| 항목 | 값 |
|---|---|
| 저자 | **Jae Yup Jung**ᵃ·ᵇ, KyungSu Kimᵇ, Joo Hyeong Suhᵃ, Hyun-seung Kimᵇ, Min Jae Youᵃ, Kern-Ho Parkᵇ, Jun Ho Songᵇ, Ji-Sang Yuᵇ, **Jong-Won Lee**ᶜ\*, **Woosuk Cho**ᵇ\*, **Min-Sik Park**ᵃ\* |
| 소속 | ᵃKyung Hee Univ.(Advanced Materials Eng. for Information & Electronics, BK21 Four) · ᵇKETI(Advanced Batteries Research Center, Seongnam) · ᶜ**Hanyang Univ.**(Division of Materials Science & Engineering) |
| 저널/년 | **Chemical Engineering Journal 470 (2023) 144381** |
| DOI | 10.1016/j.cej.2023.144381 (Received 2023-04-05, Revised 2023-05-26, Accepted 2023-06-23) |
| 소재 (CAM/SE/도전제) | **CAM = Ni-rich NCM LiNi₀.₈₂Co₀.₁₂Mn₀.₀₆O₂ (Ni 82 at%)**, 두 morphology = **PC-NCM(다결정)·SC-NCM(단결정)** · **SE = argyrodite LPSCl Li₆PS₅Cl** · 도전제 = Super P carbon |
| 조성 (ASSB 복합양극) | **NCM:LPSCl:Super P = 60:35:5 wt%** (복합양극 10 mg) |
| 셀 | **ASSB**: Al foil/cathode/SE pellet/Li-In (적층); SE 분리막 = LPSCl 100 mg(10 mm dia) 펠릿; 양면 가압 **437 MPa**; In foil(0.1 mm) + Li foil, torque 11 N·m. **LIB 대조군**: NCM:Super P:PVDF=90:5:5, NMP 슬러리, Al foil, 200 kgf/cm² roll-press, 17.0 mg, 1.131 cm², CR2032 half-cell, Li 금속/PE 분리막, 1 M LiPF₆ in EC:EMC(1:2 v/v) |
| 압력 | **제조(ASSB) 437 MPa** / LIB roll-press 200 kgf/cm² |
| 시험 조건 | LIB: 3.0–4.3 V(또는 4.5 V) vs Li/Li⁺, 0.1–5.0 C(1 C=200 mA/g). ASSB: 3.7·3.9 V vs In-Li/Li⁺ cut-off, 0.05–5.0 C, 30 °C, dry room |
| 연구유형 | **실험** — morphology(FESEM/cross-section/TEM-FFT/SEM-EDS), 구조(XRD/Table S1 lattice), 기계(micro-indenter 입자경도/tap density/BET), 전기화학(LIB·ASSB rate·cycling·GITT·EIS Nyquist) |
| 비교군 | **PC-NCM**(800 °C, 구형 다결정 ~600 nm 1차입자 응집, D50 4.9 µm) vs **SC-NCM**(900 °C as-prep → wet-mill → 675 °C post-heat, monolithic, D50 5 µm) |

## 3. 핵심 물성 (수치)

> 데이터 CSV → `docs/data/jung2023_single_crystal_ncm_morphology.csv`.

| 물성 | 값 | 조건 | stated/digitized | 비고 |
|---|---|---|---|---|
| **입자 경도 (particle hardness)** | **SC 972.7 / PC ~113.3 MPa** | micro-indenter MCT-W500 응력-변형 곡선 peak | stated | ★ **SC가 PC보다 ~8.6× 단단** — monolith·고밀도. ASSB 고압(437 MPa)에서 안정 계면 유지의 핵심 |
| 입자 경도 (LE 침지 후) | SC 유지 / PC 급감 | 액체전해질 침지 후 (Fig S8) | stated(정성) | ★ PC는 입계가 LE에 공격당해 경도↓; SC는 유지 |
| tap density | **SC 2.10 / PC 2.02 g/cm³** | porosity analyzer + tap (Fig S5b) | stated | SC가 더 치밀(particle density 높음) |
| BET 표면적 | **SC 0.23 / PC 0.28 m²/g** | N₂ 등온선 (Fig S5a) | stated | SC가 낮음(monolith); PC 높음(1차입자+내부공극) |
| D50 (입경) | **SC 5.0 / PC 4.9 µm** | PSA(MICROTRAC) + FESEM | stated | SC 최적(675 °C). PC = ~600 nm 1차입자의 구형 응집 |
| D50 (SC 합성 경로) | as-prep **13.0** → wet-mill **4.5** → 675 °C **5.0** → 700 °C **7.0 µm** | PSA | stated | 900 °C as-prep 너무 큼/응집; wet-mill 축소+표면손상; 700 °C 재응집 |
| PC 1차입자 크기 | ~**600 nm** | FESEM (Fig 2b) | stated | PC = submicron 1차입자 응집체 |
| 격자 c | PC **14.1811** / SC **14.1929 Å** | XRD Rietveld (Table S1) | stated | SC c↓ = Li-deficiency(Li/TM<1, post-heat 중 Li loss). (003)/(104) peak shift |
| TM 비율 Ni:Co:Mn | **82:12:6** | ICP-MS | stated | Ni 82 at% (Ni-rich) |
| **ASSB 1st 가역용량** | **SC 187.0 / PC 185.0 mAh/g** | 0.05 C, 437 MPa, In-Li | stated | ★ **ASSB에서 SC>PC** (LIB와 반대!) |
| ASSB 1st ICE | **SC 79.9 / PC 78.3 %** | 0.05 C | stated | SC 효율↑ (ASSB) |
| **ASSB 5C 용량유지** | **SC 74.0 / PC 41.6 %** | 5C vs 0.1C, cut-off 3.9 V In-Li | stated | ★★ **SC가 고율에서 압도** — PC 입계+공극 병목 |
| **ASSB 150 cyc 유지** | **SC 84.9 / PC 65.6 %** | 0.5 C, cut-off 3.9 V | stated | ★★ SC 장수명 우위(균열억제) |
| LIB 100 cyc 유지 | SC 75.0 / PC 62.9 % | 0.5 C, 3.0–4.3 V | stated | LIB에서도 SC 약간 우위 |
| 균열(사이클 후) | SC **억제** / PC **광범위** | cross-section FESEM 100·150 cyc 후 (Fig 5a/b, 7) | stated(정성) | ★★ PC = 입계 따라 균열; SC monolith = integrity 유지 |
| **σ_ionic / σ_e / σ_thermal / porosity / Z / Heckel** | **n/a** | — | — | ★ 이 논문은 전도도·porosity·배위수·Heckel 미측정 |

## 4. 시뮬레이션 방법 ★

> ★ **이 논문은 시뮬레이션이 없는 순수 실험 논문이다.**  DEM/MPM/FEM/RNM 어느 것도 없음.  "방법"은 합성·특성화·
> 전기화학 프로토콜.  우리 DEM+MPM과의 연결은 §7에서 *재료 물성·메커니즘 방향*으로 한다(§4가 아니라).

- **합성 (PC-NCM)**: Ni₀.₈₂Co₀.₁₂Mn₀.₀₆(OH)₂ 전구체(공침, ~5 µm 구형) + LiOH 화학량론 혼합 → **800 °C/24 h O₂**
  소성 → 구형 다결정 응집체(1차입자 ~600 nm, D50 4.9 µm).
- **합성 (SC-NCM)**: 동일 전구체 + LiOH → **900 °C** 소성(monolith 성장 목적, 그러나 as-prep는 응집·D50 13 µm,
  불규칙형) → **wet-milling**(IPA 용액, **150 rpm × 20 min, 6회 반복**, 120 °C 진공건조)으로 입자 분리(D50 4.5 µm,
  단 표면 기계손상) → **post-heat 600–700 °C/6 h O₂**(표면 구조회복; **675 °C 최적** → D50 5 µm, 구조손상 없음;
  600 °C 회복부족→율특성↓, 700 °C 재응집→D50 7 µm).
- **구조특성화**: FESEM(JSM-7000F)+EDS, cross-section(IB-19520CCP cooling polisher, −50 °C → JSM-IT200),
  TEM(ARM-200F)+FFT, XRD(Empyrean, R-3m space group, JCPDS 82-1495), micro-indenter(**MCT-W500, Shimadzu**)로
  입자경도, PSA(S3500, MICROTRAC) 입도, porosity analyzer(TriStar II 3020)+BET, tap density(FL33426), ICP-MS(Aurora M90).
- **전기화학**: LIB(CR2032, 0.1–5.0 C, 3.0–4.3/4.5 V), ASSB(437 MPa, In-Li, 0.05–5.0 C, 3.7/3.9 V cut-off,
  TOYO TOSCAT-3100/3000L), **GITT**(10 min 펄스 @0.1 C + 1 h 이완, WBCS3000L)로 Li 확산속도(cathodic 분극 ΔV),
  **EIS Nyquist**(VSP-300 Bio-Logic, 15 mV, 7 MHz–10 mHz, 30 °C)로 R_ct.

## 5. Figure set ★
| Fig | 내용 (무엇을 보여주나) | 우리가 참고할 점 |
|---|---|---|
| **1** | 모식도: PC-NCM(a) vs SC-NCM(b) 복합전극의 Li⁺ 전달. 사이클 후 단면: **PC = "Voids and cracks"(빨강) 표시 + Li⁺ 우회**, SC = "Free migration"(직선 화살표) | ★★ **우리 AM_P(PC, 공극+균열) vs AM_S(SC, monolith)** 그림의 원형. PC 입계·공극이 Li⁺ 병목+균열이라는 핵심 모식 |
| **2** | FESEM: (a)전구체 (b)800 °C PC (c)900 °C as-prep SC (d)wet-mill SC (e)675 °C SC (f)PSD 비교 히스토그램 | SC 합성경로(13→4.5→5 µm)·PC 응집형. (f)에서 SC monodisperse vs as-prep 광폭 |
| **3** | (a)XRD 패턴 + (003)/(104) 확대(SC peak shift) (b)**TEM-FFT**: PC 단면(내부공극·결함 다수) vs SC 단면(GB·공극 없음, 깨끗한 (104)/(107)/(003) FFT) (c)**입자경도 응력-변형곡선: SC 972.7 MPa vs PC ~113.3 MPa** | ★★ (b)가 **PC 내부공극+입계 = SC 없음**의 직접 증거 = 우리 AM_P/AM_S 구분의 microstructure 근거. (c) = 우리 DEM E/H + Auerbach P_c 에 **SC/PC 경도차** 부여 근거 |
| **4** | LIB: (a)PC (b)SC 전압프로파일 (c)**GITT ΔV-vs-SOC: LIB에서 PC < SC** (d)0.5C 100cyc 사이클(SC 75 vs PC 62.9 %) | LIB에서는 PC가 분극 작음(LE가 1차입자 침투 → 짧은 확산). ASSB와 *반대* — 매질의존성 강조 |
| **5** | LIB 100cyc 후 cross-section FESEM: (a)PC(균열 다수) (b)SC(균열 억제) + (c)PC (d)SC dQ/dV(1/50/100th) | ★ PC 균열 = LE가 침투→입계 부식·금속용출→열화. SC 균열억제 |
| **6** | ASSB: (a)PC (b)SC 전압프로파일 (c)**rate 용량유지: SC 74 vs PC 41.6 % @5C** (d)**GITT ΔV-vs-SOC: ASSB에서 SC < PC (LIB와 반대!)** (e)**모식: PC "Hinderance of grain boundary"(녹색 코어 Li⁺ 막힘) vs SC "Free migration"(단일 농도구배 자유확산)** | ★★ (c)(d) = **SC ASSB 전달 우위의 정량/반전**. (e) = 우리 σ_e Trevisanello 내부-GB 항의 *그림 근거* (PC 입계 = ambipolar 병목) |
| **7** | ASSB 150cyc: (a)사이클(SC 84.9 vs PC 65.6 %) + cross-section (b)PC 사이클전 (c)SC 사이클전 (d)PC 150cyc후(균열) (e)SC 150cyc후(integrity) | ★★ **PC 입계균열 vs SC 무균열의 ASSB 장기 증거** = 우리 fracture-aware σ의 결정성-의존 방향 |
| **S1** | FESEM (PC/as-prep SC/wet-mill SC/SC) | morphology 경로 보조 |
| **S2** | SEM-EDS 매핑(PC/SC) — TM 균일분포 | 조성 균일성 |
| **S3** | SC 최적화(600/650/675/700 °C) FESEM+PSD | 675 °C 최적(D50 5 µm) |
| **S4** | LIB rate(as-prep/600/650/675/700 °C SC) | post-heat 온도-율특성 |
| **S5** | (a)BET(SC 0.23/PC 0.28) (b)tap density(SC 2.10/PC 2.02) | ★ 정량 표면적·밀도 |
| **S6** | LIB 3.0–4.3 V: (a)PC (b)SC 전압 (c)rate (d)cycle | LIB 대조 |
| **S7** | **LIB Nyquist(PC/SC, 1st 충전상태): PC R_ct < SC** | LIB에서 PC 계면저항 작음(큰 활성계면) |
| **S8** | **입자경도(LE 침지 전/후): PC 급감 vs SC 유지** | ★ PC 입계의 LE 화학취약성 |
| **S9** | ASSB rate(as-prep/wet-mill/675 °C SC) | post-heat ASSB 효과 |

## 6. Post-processing ★
- **무엇**: 시뮬 post-processing 없음(실험 논문).  데이터 분석 = **GITT 분극 ΔV(SOC 의존)** 로 Li 삽입 kinetics 비교,
  **EIS Nyquist 2nd semicircle = R_ct**(전하전달저항), **dQ/dV(미분용량)** 로 과전압·상전이 추적, **XRD Rietveld**(c 격자),
  **micro-indenter 응력-변형 → 입자경도(MPa)**, **PSA D50 + 히스토그램**, **N₂ BET + tap density**.
- **도구**: WonATech WBCS3000L(GITT), Bio-Logic VSP-300(EIS), TOYO TOSCAT(사이클), Empyrean+PANalytical(XRD),
  MCT-W500 Shimadzu(경도), MICROTRAC(PSA), TriStar II/FL33426(BET·tap).
- **수치화·기록**: 정량값 = 경도 972.7/113.3 MPa, tap 2.10/2.02, BET 0.23/0.28, D50, 용량 187/185, ICE 79.9/78.3,
  rate 74/41.6 %, cycle 84.9/65.6 %, lattice c.  **정성값**(우리가 추세로만) = GITT ΔV 대소, R_ct 대소, 균열 정도,
  Free migration vs hindrance 모식.

## 7. 우리 DEM+MPM 대비  →  `our_dem_baseline.md`

> ★ 이 절이 이 digest의 핵심이다.  이 논문은 시뮬이 없으므로 method 대비가 아니라 **재료·메커니즘 대비**다.
> 우리 모델의 *세 가지 설계 선택*(AM_P/AM_S 분리, Auerbach 결정성-파괴, σ_e Trevisanello GB항)이 이 실험 논문에
> 뿌리를 둔다는 것을 명시적으로 연결한다.

### 7-A. ★★ AM_P(다결정) / AM_S(단결정) 분리의 실험 근거
| 항목 | 이 논문 (실험) | 우리 DEM | 연결 |
|---|---|---|---|
| **다결정 AM** | **PC-NCM**: ~600 nm 1차입자 구형 응집, **입계 + 내부공극** 보유, D50 4.9 µm, BET 0.28, tap 2.02, 경도 ~113.3 MPa | **AM_P** (보통 더 큰·다결정 양극입자) | ★★ **PC = AM_P**: 다결정·내부공극·연질·균열취약 |
| **단결정 AM** | **SC-NCM**: monolith, **입계없음·내부공극없음·결함없음**, D50 5 µm, BET 0.23, tap 2.10, 경도 972.7 MPa | **AM_S** (단결정 양극입자) | ★★ **SC = AM_S**: monolith·고밀도·고경도·무균열 |
| **분리 정당성** | TEM-FFT(Fig 3b): SC = 깨끗한 단결정 회절, PC = 내부공극·결함 다수 → *물리적으로 다른 재료 클래스* | 우리는 AM을 크기 **+ 종류(P/S)** 로 split | ★ 우리 AM_P/AM_S 분리가 *라벨이 아니라 실측 microstructure 차이*에 근거 |

→ **결론**: 우리 DEM이 AM을 P/S로 나누는 것은 이 논문이 정량화한 **morphology·경도·밀도·내부공극의 실재 차이**를
반영한 것.  특히 AM_S(단결정)는 더 단단·치밀(경도 8.6×, tap +4 %), 우리 DEM 접촉역학에서 AM_S에 **더 높은 E/H,
더 낮은 internal-void 보정**을 줄 실험 근거가 된다.

### 7-B. ★★ Auerbach 파괴 / fracture-aware σ — *결정성(SC vs PC) 축* 추가
| 항목 | 이 논문 (실험) | 우리 DEM | 연결 |
|---|---|---|---|
| **PC 균열** | 제조·사이클 중 **입계 따라 균열**(intergranular), 내부공극 = 균열시드 → 파편 고립 → 용량fade. 150 cyc 후 광범위(Fig 7d) | Auerbach P_c, fracture-aware `f_intact`, `frac_severe` | ★★ PC = 낮은 파괴역치(입계+공극 = 약점) |
| **SC 균열억제** | monolith·고경도 → **미세균열·입자파괴 억제**, 150 cyc 후 integrity(Fig 7e) | 동상 | ★★ SC = 높은 파괴역치(GB-less·고경도) |
| **역치-경도 연결** | 경도 SC 972.7 ≫ PC 113.3 MPa (Auerbach P_c ∝ K_IC²/E, 경도↑ 보통 K_IC↑) | 우리 Auerbach P_c = f(E, K_IC) | ★ **결정성-의존 P_c**: SC harder + GB-less → 더 높은 fracture threshold 항 정당화 |

→ **랩 cracking story의 *결정성 축* 추가**:
 - **Kang 2025** = *큰 입자(10 µm)일수록* 사이클 균열↑ (**크기 축**).
 - **Kim 2023** = *anode 고변형* chemo-mech 균열 (**변형 축**).
 - **Jung 2023(본 논문)** = *다결정(PC)이 단결정(SC)보다* 균열↑ (**결정성 축**).
 → 우리 fracture 모델은 **크기(Kang) × 변형(Kim) × 결정성(Jung)** 3축으로 실험 정렬 가능.  fracture-aware
   `f_intact`/`frac_severe`가 AM_P(다결정)에서 더 크게 발화하도록(낮은 P_c) 두는 것이 이 논문으로 정당화된다.

### 7-C. ★★ σ_electronic Trevisanello NCM(r) 내부-GB 보정항의 실험 근거
| 항목 | 이 논문 (실험) | 우리 σ_e | 연결 |
|---|---|---|---|
| **PC 내부 GB = 전달 병목** | 입계+내부공극이 **Li⁺ AND 전자(ambipolar) 확산 저항**↑ (본문 명시), Fig 6e "Hinderance of grain boundary"(코어 Li⁺ 막힘) | σ_e 폼의 **NCM(r) = 1/(1+(r_AM/2)^1.5)** Trevisanello GB 보정 (입자 내부 GB 밀도 인자) | ★★ PC 내부-GB = σ_e 감소 = 우리 NCM(r) 항이 잡는 바로 그 물리 |
| **SC monolith = 자유 전달** | GB-less monolith → "Free migration", **향상된 ambipolar 확산** (Fig 1b, 6e) | SC(AM_S) → NCM(r) 페널티 작음 | ★ SC = 내부-GB 없음 → σ_e 높음 |
| **ASSB GITT 반전** | **ASSB에서 SC ΔV < PC**(Fig 6d, LIB와 반대) — ASSB는 고체확산이 지배 → SC monolith가 유리 | 우리 σ_e/σ_ionic 가 ASSB 고체전달 모델 | ★ ASSB에서 SC 전달우위 = 우리 전달 폼의 SC>PC 방향 검증 |

→ **결론**: 우리 σ_e 폼이 쓰는 Trevisanello "단결정 vs 다결정 내부-GB 밀도" 인자는 이 논문이 **실험으로 직접 보인**
 *PC 내부-GB ambipolar 병목 vs SC 자유확산*에 근거한다.  특히 **LIB↔ASSB 반전**(LIB: PC 우세 ← LE가 1차입자 침투해
 짧은 확산; ASSB: SC 우세 ← LE 없이 monolith 고체확산이 지배)은 우리가 *ASSB 맥락에서* SC(AM_S)의 전달우위를 두는 것을
 정당화한다.

### 7-D. 입자 경도/밀도 → DEM 접촉역학(E, H) + Auerbach
- SC 경도 972.7 MPa, PC 113.3 MPa (8.6×), tap density SC 2.10 > PC 2.02 → 우리 DEM이 **AM_S에 더 높은 경도 H,
  더 높은 particle density**를 줄 실험 근거.  Auerbach P_c·Tabor 소성 접촉면적(H가 cap에 들어감)에서 AM_S/AM_P가
  *다른 H*를 갖도록 하는 것이 이 논문으로 정당화.  단, 우리 DEM은 CAM을 보통 rigid(E_CAM 140 GPa)로 두므로 이
  경도차는 **fracture 역치·plastic 접촉면적 cap**에서 주로 작동(탄성 압밀이 아니라).

### 7-E. Frame[5] 분업 — 무엇을 우리가 하고 무엇을 안 하나
| 축 | 이 논문(실험·사이클·합성) | 우리 DEM+MPM |
|---|---|---|
| **압밀-순간 구조** | 안 다룸(전기화학·morphology 중심) | ★ **우리 영역**: P/S 패킹, porosity, Furnas-dip, 접촉망 |
| **전달 σ** | 정성(GITT ΔV, R_ct)만 | ★ **우리 영역**: σ_ionic/e/thermal 정량(Kirchhoff). 이 논문의 SC>PC 방향을 우리가 *수치화* |
| **파괴 역치** | 균열 *정도*(SEM, 정성) | ★ **우리 영역**: Auerbach P_c, f_intact 정량. 이 논문이 *결정성 의존 방향* 제공 |
| **사이클 중 확산/열화** | ★ **그들 영역**(GITT D_Li, 100/150 cyc fade, dQ/dV) | 우리 DEM+MPM은 *압밀-순간*만 — **사이클 확산·용량fade 안 함** |
| **합성/morphology 제어** | ★ **그들 영역**(wet-mill, post-heat 675 °C) | 우리는 합성 안 함 — 주어진 morphology(P/S)를 input으로 받음 |
| **입자 형상변화(소성)** | 안 다룸 | ★ **MPM 영역**(SE 소성 morphology). 단 CAM은 rigid |

## 8. 적용 인사이트 (내 연구에 어떻게)
- ① **AM_P/AM_S 분리에 *재료 물성* 부여**: 이 논문의 SC vs PC 정량차(경도 972.7/113.3, tap 2.10/2.02, BET 0.23/0.28,
  내부공극 유/무)를 우리 DEM의 AM_S/AM_P 파라미터화 근거로 인용.  AM_S = 더 단단·치밀·무공극·높은 P_c;
  AM_P = 연질·내부공극·낮은 P_c.  CSV: `docs/data/jung2023_single_crystal_ncm_morphology.csv`.
- ② **fracture 모델 *결정성 축***: fracture-aware `f_intact`/`frac_severe`·Auerbach P_c 가 AM_P(다결정)에서 더 크게
  발화하도록 결정성-의존 항을 두고, Kang 2025(크기)·Kim 2023(변형)과 함께 **3축(크기·변형·결정성)** 으로 실험 정렬.
- ③ **σ_e Trevisanello NCM(r) 항의 *랩 실험 앵커*로 인용**: PC 내부-GB ambipolar 병목 vs SC 자유확산(Fig 1b/6e)을
  우리 σ_e 폼의 단결정-vs-다결정 GB 밀도 인자의 *우리 랩 실험적 근거*로 명시.  ASSB-context(LIB↔ASSB 반전)에서
  SC 전달우위 방향 일치.
- ④ **검증 방향**: 우리 DEM+MPM에 동일 조성(NCM:LPSCl:SuperP=60:35:5, 437 MPa)으로 AM_P vs AM_S 케이스를 돌려
  *우리가 예측하는 σ·porosity·f_intact* 가 이 논문의 *SC>PC 전달·무균열 방향* 과 정합하는지 cross-check
  (수치 절대비교 아니라 부호·순서; 이 논문은 σ 절대값 미측정).

## 9. 인용 가능 문장 (deck/paper용)
- "Our DEM separation of the cathode active material into polycrystalline (AM_P) and single-crystalline (AM_S)
  populations is grounded in our own laboratory's experimental contrast (Jung et al., Chem. Eng. J. 2023):
  single-crystal NCM is monolithic, grain-boundary-free and far harder (particle hardness 972.7 vs 113.3 MPa)
  than the polycrystalline aggregate, which carries internal voids and grain boundaries that act as transport
  bottlenecks and crack nucleation sites."
- "The single-crystal cathode's suppression of microcracking and its enhanced ambipolar Li⁺/e⁻ diffusion in an
  ASSB (5C retention 74.0 % vs 41.6 % for polycrystalline; 150-cycle retention 84.9 % vs 65.6 %) provide the
  experimental basis for the crystallinity-dependent fracture threshold (Auerbach) and the Trevisanello
  internal-grain-boundary correction in our σ_electronic form."

## 10. 주의/한계 (over-claim 방지)
- **시뮬 없음·실험만**: 이 논문에서 DEM/MPM/transport-σ/porosity/Heckel 수치는 **얻을 수 없다**.  우리가 가져가는
  것은 *재료 클래스 물성차*(경도·밀도·공극·균열)와 *전달 방향*(SC>PC, ASSB)뿐.  σ_ionic/e/thermal 절대 앵커로 쓰면 안 됨.
- **GITT ΔV·R_ct·균열정도는 정성**(대소만) → 우리 모델 *부호·순서* 검증에만, 절대 수치 fit 금지.
- **소재 = NCM811-계 (Ni 0.82)** ✓ 우리 NMC811과 정합(Ni-rich layered).  단 **LIB↔ASSB 반전** 주의: LIB에서는
  PC가 분극↓(LE가 1차입자 침투→짧은 확산)이라 *오히려 PC 우세* — 우리 모델은 **ASSB 맥락**(SC 우세)만 가져와야 함.
  LIB 결과를 ASSB 방향으로 잘못 전이 금지.
- **사이클 열화·합성은 우리 영역 밖**(frame[5]): 우리 DEM+MPM은 *압밀-순간* 구조·전달·파괴역치만.  이 논문의
  100/150 cyc fade·GITT D_Li·wet-mill/post-heat 합성은 우리가 모델하지 않음 — "우리가 이걸 재현한다"고 주장 금지.
- **CAM rigid 가정**: 우리 DEM은 CAM(NMC811)을 보통 rigid(E 140 GPa)로 둔다 → 이 논문의 경도차(SC/PC 8.6×)는 우리
  탄성 *압밀*이 아니라 **fracture 역치·Tabor plastic 접촉면적 cap**에서 작동.  "SC가 더 단단해서 *덜 압밀된다*"는
  과대해석 금지(압밀은 SE 소성이 지배).
- **digitized 없음**: 본 digest의 수치는 전부 본문/표 stated 값(경도·용량·유지율·BET·tap·D50·lattice).  Fig에서
  눈으로 읽은 근사값은 사용 안 함.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

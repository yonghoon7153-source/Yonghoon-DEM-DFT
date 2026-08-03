# Enabling Moisture and Interfacial Stability in Sulfide Solid Electrolytes via a Processable Organic Coating Strategy for High-Voltage All-Solid-State Batteries — Qian et al. (Angew. Chem. Int. Ed. 2026)

> slug `qian2026_decanoate_coating_lpscl_moisture_interface` · DOI `10.1002/anie.9983580` (Angew. Chem. Int. Ed. 2026, e9983580 — ⚠ 비정상 DOI 번호 체계, early-view 플레이스홀더 의심) · type `exp (코팅·전기화학) + DFT 보조(분자 conformer + 슬랩 표면E + 흡착 결합E)` · PDF `inbox/44. Enabling Moisture…pdf` (본문 12 pp) + `inbox/44. Sup) Enabling Moisture…pdf` (SI: Methods + Fig S1–S16 + Table S1–S4) · digested `2026-08-03` · 태그 **[외부]** · 사용자 분류 폴더 `DFT` · status ✅
> elements: Li, P, S, Cl, C, O, H, Ni, Co, Mn, In
> methods: DFT, XPS, ToF-SIMS, FTIR, XRD, EIS, CV, cryo-TEM, FIB-SEM, EDX
> **저자**: Lanting Qian, Cameron Dean, Ivan Kochetkov, Hengning Chen, Yangyang Huang, **Linda F. Nazar\*** (lfnazar@uwaterloo.ca) — Department of Chemistry, Waterloo Institute of Nanotechnology, **University of Waterloo**, Ontario, Canada.
> Received 2026-01-03 / Revised 2026-05-11 / Accepted 2026-05-20. Open access (CC-BY). SI 원본 파일명 `anie73015-sup-0001-SuppMat.docx`.
> **그룹 계보**: **Nazar = [Adeli] (adeli2019 halide substitution) 교신저자와 동일**, **[Zuo] (zuo2022) 공저자**. Ivan Kochetkov는 [Adeli] 공저자와 동일 인물. → 우리 litdb 안에서 **Waterloo/Nazar 라인 3번째 논문**이자, **[Adeli] 조성축(Cl-rich) → [Zuo] 계면축 → 본 논문 코팅축**으로 이어지는 같은 그룹의 세 번째 레버.

---

## 0. 이 digest를 읽는 법

이 논문은 **"황화물 SE의 두 고질병(수분 민감·고전압 산화)을 SE 입자 *표면 유기 코팅* 하나로 동시에 잡을 수 있나?"** 를 묻는다.
답: **데칸산(decanoic acid, C10 지방산) 2 wt%를 LPSCl 입자에 용액 코팅(25 nm 비정질 conformal)** 하면 (a) 39 % RH 2 h 노출을 견디고, (b) NCM85 무코팅 양극과 4.3 V까지 안정 순환하며, (c) Li 금속 대칭셀 1000 h를 간다.

> ⚠ **우리 캠페인 관점에서 이 논문의 위치를 먼저 못 박아 두자.**
> - 레버가 **조성(Cl 증량·도핑)이 아니라 SE 입자 표면 코팅**이다 → `comparison_vs_ours.md` **B③ "레버 = SE 코팅"** 칸([Kang25] SE 코팅 균일화)의 **유기·저온 버전**이자, **B④ moisture** 칸([Yang25] O 격자도핑 / [Zhu20] 열역학 지도)의 **코팅 버전**.
> - **산화 안정성 개선의 기전이 "창을 넓혔다"가 아니라 "전자를 막았다"** — 저자들도 명시적으로 *electronically insulating DA layer → limits electron transfer* 라고 쓴다. 즉 **B① intrinsic onset은 안 건드린다**. 우리 "onset은 S²⁻-pin으로 불변, 이득은 전자 절연 CEI에서 온다"는 서사의 **외부·실험 증거**다.
> - **DFT는 보조**지만, 우리에게 특히 값진 게 하나 있다: **LPSCl 저지수 슬랩 표면에너지 6종 표(Table S2)** — 우리 `adhesion.json` γ_SE(UMA melt-quench)의 **첫 외부 DFT 대조군**이다(§7).

> ⚠ **전압 기준**: 본문은 대부분 **Li⁺/Li 기준**으로 쓴다(2.8–4.3 V, "oxidative decomposition above 2.5 V versus Li⁺/Li"). 셀의 대극은 Li–In 또는 Li 금속인데, **셀 전압창 2.8–4.3 V는 Li⁺/Li 환산값으로 읽어야 한다**(Li–In 기준이면 +0.62 V 차이). 논문이 매 그림마다 기준을 다시 명시하진 않는다 → 인용 시 "vs Li⁺/Li"로 통일.

---

## 1. 한 줄 요약

**LPSCl 입자에 데칸산 2 wt%를 용액 코팅(25 nm, COO–Li 화학결합)** 하면 소수성 C10 사슬의 물리 차단 + 표면 산화-S 부동태층이 합쳐져 **39 % RH 2 h 노출 후에도 σ > 1 mS/cm(유지율 91 %)** 를 지키고, 동시에 **전자 절연막으로 작동해 무코팅 NCM85와 4.3 V 순환에서 SE 산화분해(SOₓ/POₓ)를 억제** → **150 cyc 96 % 유지(bare 61 %)·R_cathode 104 Ω(bare 461 Ω, 4.4×)·Li 대칭셀 1000 h(bare 230 h)** 를 달성한다. **고온 소결·복잡 공정 없이** 되는 게 세일즈 포인트.

---

## 2. 메타 / 동기

| 항목 | 내용 |
|---|---|
| 코팅제 | **데칸산 (decanoic / capric acid, C₉H₁₉COOH; 논문은 데칸산염 표기 `C10H19O2` = DA)** · MSE Supplies 99.5 % |
| SE | **상용 LPSCl (Ampcera)** — 자체 합성 아님 |
| 양극 | **무코팅 NCM85** = LiNi₀.₈₅Mn₀.₁Co₀.₀₅O₂ (BASF, D50 ~4–5 µm) — **양극 코팅을 일부러 안 씀**(코팅 부담을 SE 쪽으로 옮긴 게 논지) |
| 음극 | Li–In (기본) / **Li 금속**(후반부) |
| 질문 | 황화물 SE의 **수분 민감성 + 고전압 산화 불안정**을 *하나의 저비용 처리*로 동시 해결 가능한가 |
| 갭 | 기존 해법은 (a) 양극 입자 코팅(Al₂O₃/ZrO₂/Li₂SiO₃/LiNbO₃/Li₂ZrO₃ — 복잡·고온) 또는 (b) 음극 보호층 — **양쪽 다 하면 공정 복잡도·비용 폭증**. SE 자체 표면 개질은 상대적으로 드묾 |
| 전략 논리 | **"양극·음극을 각각 코팅하지 말고, 둘 다와 접하는 SE를 코팅하라"** — 한 번의 처리로 양쪽 계면 동시 커버 (**dual protection**) |
| 저자 자기인용 | ref [38] Huang/Zhou/Li/Yu/**Nazar**, *"Waxing Bare High-Voltage Cathode Surfaces"* ACS Energy Lett. 2023 — **같은 DA 코팅을 NCM 쪽에 했던 선행**. 이 논문은 그 코팅을 **SE 쪽으로 옮긴 것** |

---

## 3. 핵심 수치 총정리

### 3a. 코팅 그 자체
| 항목 | 값 | 출처 |
|---|---|---|
| 코팅 두께 | **~25 nm, conformal·비정질** | Cryo-TEM Fig 1a |
| 코팅 조성 | **C, O 균일 분포** | EDX Fig 1b |
| 결합 형태 | **O–C=O(카복실) 신호 급증 → COO–Li 형성** | C 1s XPS Fig 1c,d + FTIR Fig 1e |
| FTIR 신규 밴드 | **~3000–2800 cm⁻¹** (–CH₂– C–H stretch), **~1700–1350 cm⁻¹** (C–O/C=O stretch) | Fig 1e (⚠ 본문이 두 대역의 귀속을 서로 바꿔 쓴 문장이 있음 — §12) |
| 최적 함량 | **2 wt%** | Table S3 + Fig S8 |
| 벌크 구조 | **PXRD 변화 없음** | Fig S2 |
| 입자 형상 | bare와 동일, 응집 없음 | SEM Fig S1 |

### 3b. σ vs DA 함량 (Table S3, 26 ± 1 °C)
| DA wt% | σ (mS/cm) |
|---|---|
| 1 | 1.4 |
| **2 (최적)** | **1.3** |
| 5 | 0.7 |
| 10 | 0.2 |

> **읽는 법**: 코팅은 **σ를 사는 게 아니라 파는** 거래다. 2 wt%에서 이미 손실이 있고, 5 wt%부터 절반 이하로 꺾인다(Fig S8에서 5 wt% 셀 용량도 확 떨어짐). ⚠ **bare LPSCl(Ampcera)의 σ 절대값이 본문·SI 어디에도 명시되어 있지 않다** — 코팅에 의한 σ 손실률을 독자가 계산할 수 없다(§12 한계).

### 3c. 수분 안정성 (39 % RH, 실내 습도)
| 항목 | bare LPSCl | DA-LPSCl |
|---|---|---|
| XRD (노출 중) | **즉시 Li₂O₂ + LiCl 반사 출현** | **2 h까지 변화 없음** |
| σ (노출 시간 함수) | 즉시 하락, 2 h까지 계속 | 2 h 후 **소폭 하락만** |
| σ 유지율 (Table S4) | — | **91 %**, 노출 후 **1.13 mS/cm** |
| S 2p XPS (30 min 노출 후) | **163.2 eV 원소 S 급증** | 노출 전후 **거의 불변** |
| P 2p XPS (Fig S7) | 정상 | **신호 거의 없음** = 표면이 산화-S + 탄소사슬로 덮임 |

**S 2p 귀속 (수분 섹션)**: 161.6 eV = PS₄³⁻ 황화물 · 163.2 = **원소 S**(황화물 산화) · 166.6 = **thiosulfate** · 168 = **polythiosulfate**.

### 3d. 문헌 대비 표 (Table S4 — SI 원표, 조건 제각각이라 순위 인용 금지)
| Material | 노출 시간 | RH | 코팅 후 σ (mS/cm) | σ 유지율 | 원전 |
|---|---|---|---|---|---|
| OScA-LPSCl (oxysulfide) | 30 min | 35 % | 3.02 | 83 % | Jung, ACS Omega 2020 |
| Li₆.₀₃P₁₋ₓSe₀.₀₃S₅Cl | 30 min | 10 % | 3.06 | 57 % | Kim, Electrochim. Acta 2023 |
| ZSM-5 zeolite-LPSCl | 1 h | 50 % | 1.27 | 31 % | Lee & Park, JMCA 2021 |
| LPSBI-Bromo | 2 h | 0.5 % | 2.8 | 89 % | Yu, ACS AMI 2022 |
| **UDSH@LPSCl** (undecanethiol) | 5 h | 33 % | 2.1 | 86 % | **Liu, Nat. Commun. 2025** |
| **UDSH@LPSCl** | 3 days | 33 % | 2.1 | 38 % | 동상 |
| OPA-LPSClBr (phosphonic acid) | 24 h | <1 % | 2.5 | 92 % | Fadillah, Adv. Mater. 2025 |
| g-C₃N₄-LPSCl | 3 h | 20 % | 0.6 | 72 % | Luo, EEM 2024 |
| PBS@LPSCl (polyborosiloxane) | 1 h | 50 % | N/A | ~90 % | Hong, CEJ 2025 |
| F-PDMS@LPSCl | 72 h | <1 % | 2.0 | 49 % | Kim, AEM 2023 |
| Al₂O₃@LPSCl (ALD) | 4 h | dry O₂ | 1.7 | N/A | Hood, Adv. Mater. 2023 |
| **DA-LPSCl (this work)** | **2 h** | **39 %** | **1.13** | **91 %** | — |

> ⚠ **이 표는 "누가 최고"를 말하지 않는다.** RH가 <1 %에서 50 %까지, 시간이 30 min에서 3일까지 흩어져 있다(저자도 "despite the wide variation in testing conditions"라고 인정). **의미 있는 축은 σ 절대값이 아니라 (RH × 시간) 대비 유지율**이고, 그 축에서 DA(39 % / 2 h / 91 %)는 상위권이되 **UDSH(33 % / 5 h / 86 %)** 와 실질 동급이다. **DA-LPSCl의 σ 절대값(1.13)은 표에서 가장 낮은 축**이다 — 수분 내성을 σ로 산 거래.
> ⚠ SI 본문의 참고문헌 번호(표에는 15–24로 인쇄)와 SI 참고문헌 목록(14–23)이 **일관되게 1씩 어긋난다**. 위 표의 원전 귀속은 *내용 대조*로 확정한 것이다.

### 3e. 전기화학 (Li–In 음극 · 무코팅 NCM85 · 2.8–4.3 V · 0.2 C, 1C = 200 mA/g)
| 항목 | bare LPSCl | DA-LPSCl (2 wt%) |
|---|---|---|
| 초기 방전용량 | 163 mAh/g | **175 mAh/g** |
| **초기 CE** | **60 %** | **83 %** |
| 초기 충전 프로파일 | **<3.5 V 완만한 sloping 구간(= LPSCl 산화)** | **없음** |
| Rate 0.2 C | 162 mAh/g | **183 mAh/g** |
| Rate 1 C | 55 mAh/g | **104 mAh/g** |
| 150 cyc @0.2 C | 99 mAh/g, **61 % 유지** | 168 mAh/g, **96 % 유지** |
| 4.6 V 컷오프, 110 cyc | — | **91 % 유지** (Fig S9) |
| 고로딩 21 mg/cm² | — | **초기 3.2 mAh/cm², 150 cyc 81 %** (Fig S10) |
| **R_cathode (150 cyc 후, TLM)** | **461 Ω** | **104 Ω (4.4× 낮음)** |
| CV 산화 onset | **2.5 V에서 뚜렷한 anodic 전류** | **같은 구간 전류 크게 억제** |
| 순환 후 S 2p 원소 S(163.1 eV) | 강함 | **억제됨** |
| ToF-SIMS SO₂⁻/SO₃⁻/PO₂⁻/PO₃⁻ | 광범위 형성 | **훨씬 약함** |
| FIB 단면 (150 cyc) | intragranular crack 다수 | **crack 현저히 감소** |

**순환 후 S 2p 귀속 (계면 섹션)**: 160.2 eV = **free S²⁻**(argyrodite 4d 자유 황) · 161.1 = **PS₄³⁻** · 163.1 = **원소 S**(산화 산물).
> ⚠ **같은 논문 안에서 PS₄³⁻ 귀속이 161.6(수분 섹션) ↔ 161.1(계면 섹션)로 0.5 eV 다르다** — 다른 피팅·보정. BE 인용 시 어느 섹션인지 반드시 병기(§12).

### 3f. Li 금속 (대칭셀 0.5 mA/cm², 1.0 mAh/cm²; 풀셀 35 MPa, 7 mg/cm²)
| 항목 | bare LPSCl | DA-LPSCl |
|---|---|---|
| Li‖Li 대칭셀 수명 | **230 h 단락**(초록·결론) / **200 h**(서론) — ⚠불일치 | **1000 h 안정**(분극 소폭 증가) |
| 펠릿 공극률 (Fig S15) | **10.1 %** | **6.9 %** (2 wt%; 상대 −31 %) |
| 100 cyc @0.2 C | 97 mAh/g (**57 %**) | 166 mAh/g (**94 %**) |
| 300 cyc @0.2 C | (급락) | 143 mAh/g (**81 %**) |
| 초기 20 cyc 평균 CE | **90 %**(낮음) | (높음, 수치 미제시) |
| 순환 후 Li 표면 SEM | 거칠음 = 불균일 석출 | **매끈** |

**기계 물성 논거(문헌 인용값)**: 지방산 탄성계수 **0.1–2 GPa** ≪ LPSCl **~30 GPa**; DA 융점 **31–32 °C**(낮은 융점 = 낮은 강성).

---

## 4. 재료 & 실험 방법 (SI Methods 전문)

**코팅 합성 (핵심 레시피 — 재현 가능)**
1. Ar 분위기에서 **데칸산을 톨루엔에 용해, 3 h 교반**
2. **LPSCl 투입 후 overnight 교반**
3. **140 °C, N₂ 유동 하에서 증발 (500 rpm 교반)**
4. **120 °C, 12 h 진공 건조**(BUCHI glass oven) — 잔류 톨루엔 제거
   > 고온 소결·ALD·볼밀 전무. **용해→교반→증발→건조**가 전부 = "processable" 주장의 근거.
5. (수분 노출 실험 후) 펠릿을 80 °C 건조 → 글로브박스 이송 → 재분쇄 → σ 측정

**셀 제작**
- 분리막: PEEK 실린더에 SE 분말 **120 mg, 250 MPa 1 min** 가압
- 복합양극: argyrodite : 무코팅 NCM85 = **2 : 8 (wt)**, 마노유발 **15 min** 수동 그라인딩 → 펠릿 위에 **2 ton, ~3 min** 가압
- 음극: In 포일(⌀10 mm, 0.1 mm) + Li ~1.5 mg → Li–In 합금 / 또는 Li 포일(칼날 연마)
- **초기 스택 압력 ~35 MPa** (custom cell), 25 °C, VMP3/MACCOR

**분석**
- XRD: PANalytical Empyrean, Cu-Kα. 코팅 전후 비교는 **Kapton 밀봉**, 수분 노출 실험은 **Kapton 없이**
- Cryo-TEM: Titan 80-300 LB · SEM/FIB: Zeiss FE-SEM
- XPS: Thermo Fisher K-Alpha, monochromated Al-Kα
- **ToF-SIMS**: ION-TOF 5, 30 keV 클러스터 건, **200 × 200 µm²**, 256 × 256 px, 전류 ~0.3 pA, stop 5 × 10¹² ions/cm², SurfaceLab 7.2. **모든 2차이온을 total ion count로 정규화**, 넓은 면적 = 샘플링 편향 최소화
- EIS: Bio-Logic SP-200, 100 mHz–1 MHz, 25 °C, **RelaxIS** 피팅, **TLM(blocking BC)** (Fig S12)
- **CV**: SE + 카본나노섬유 **95 : 5** 복합전극 / LPSCl 펠릿 / Li–In, **200 MPa**, **0.1 mV/s**, OCV → 5.0 V → 역스캔

---

## 5. 결과 — 섹션별 상세

### 5.1 (§2.1) 코팅 형태 — "정말 붙어 있나"
Cryo-TEM에서 **25 nm 비정질 conformal 층**이 LPSCl 입자를 감싼다. EDX로 C·O가 표면에 균일. C 1s XPS에서 **O–C=O 성분이 bare 대비 크게 증가**. FTIR에서 지방산 특유의 **–CH₂– stretch(~3000–2800)** 와 **C–O/C=O stretch(~1700–1350)** 신규 밴드 → 저자 결론: **표면에 lithium decanoate(–COO–Li)가 생성**. PXRD·SEM은 벌크·형상 불변.

> 🔑 **여기서 이미 "화학 결합"이 주장된다** — 단순 물리 흡착이 아니라 표면 Li와의 산-염기 반응. 이걸 뒷받침하려고 §2.2 DFT를 붙인 구조다.

### 5.2 (§2.2) DFT — 코팅이 표면에 *화학적으로* 붙는가 ★★

**논리 흐름**: (i) 코팅층의 벌크 구조를 모르니 **고립 DA 분자**부터 → (ii) LPSCl **어느 면**을 볼지 정하고 → (iii) 그 면에 DA를 **어느 배향으로** 붙일지 스캔.

**(i) 분자 conformer (Gaussian 16, Table S1)**
PubChem에서 10개 conformer를 받아 DFT 최적화 → 상대에너지(K 단위)로 300 K Boltzmann 분포:

| conformer | ΔE (K) | 확률 |
|---|---|---|
| **1 (linear)** | 0.0 | **69.8 %** |
| 8 | 274.9 | **27.3 %** |
| 3 | 1072.2 | 1.8 % |
| 6 | 1411.9 | 0.6 % |
| 5 | 1628.3 | 0.3 % |
| 9 | 1715.5 | 0.2 % |
| 2 / 4 / 7 / 10 | 4015.9 / 4234.0 / 8114.8 / 4479.1 | ~0 % |

→ **linear conformer(카복실기와 CH₃ 말단이 최대 이격)가 ~70 %** → 이후 모든 표면 계산에 이 배좌만 사용.
> ✔ 검산: ΔE = 274.9 K → e^(−274.9/298) = 0.398, 69.8 % × 0.398 = 27.8 % ≈ 표의 27.3 %. **Table S1은 내부 정합**(추출 시 열 정렬이 어긋나 보이지만 값 자체는 맞다).

**(ii) 표면 선택 (VASP, Table S2)** — **우리에게 가장 값진 표**

| Miller | 표면 조성(termination) | 시뮬레이션 슬랩 | **표면E (J/m²)** |
|---|---|---|---|
| 010 | S | Li₃₇P₈S₃₅Cl₁₁ | 0.70 |
| 010 | Li | Li₄₁P₈S₃₅Cl₁₁ | 0.44 |
| **010** | **Li₅SCl** | **Li₃₆P₆S₂₈Cl₁₀** | **0.40 ← 선택** |
| 010 | Li₇SCl | Li₄₀P₆S₂₈Cl₁₀ | 0.72 |
| 011 | Li₄S₂ | Li₃₂P₆S₂₆Cl₁₀ | 0.48 |
| 011 | Li₄S₂ | Li₃₄P₆S₂₈Cl₈ | 0.70 |

→ **"sulfur-poor (010)"** = Li₅SCl 종단이 최저 0.40 J/m² (Fig S3). **S-종단(0.70)이 가장 나쁘고, Li 과잉(Li₇SCl 0.72)도 나쁘다 — Li·S·Cl이 섞인 중간 종단이 최저**라는 게 물리적으로 읽을 만한 대목.

**(iii) 결합에너지 (10 configuration = 표면 5자리 × 배향 2종)**
- `E_bind = E(surface + DA) − E(surface) − E(DA molecule)` (Eqn. S3)
- 초기 배치: 표면에서 **2 Å 이격**, **분자를 표면에 수직**으로. 평행 배향은 **계산 비용**(주기 이미지와 10 Å 확보 필요) + **물리적 비현실성**(vdW만·사슬 배좌 엔트로피 손실) 이유로 제외.
- 표면 자리 5곳은 "각 원소 최소 1개 + 넓은 공간 분포" 기준으로 선택(Fig S5).
- 슬랩 반대면은 **구속 없이** 두었고, 이완 중 움직이지 않음을 확인(Fig S6) → 슬랩 두께·진공 충분 근거.

**결과**
| 배향 | E_bind | 거리 | 해석 |
|---|---|---|---|
| **극성 머리(–COOH) → 표면** | **−0.16 ~ −0.98 eV** (최강 **−0.98**) | **Li–O 1.9 Å** | **화학결합**. Li–OH 결합길이 1.9–1.95 Å와 비슷 → **HCl 방출을 동반한 lithium decanoate(–COO–Li) 생성**으로 해석 |
| 비극성 꼬리(alkyl) → 표면 | **0.077 eV**(⚠ 부호가 양수로 인쇄됨 — −0.077의 오식으로 보임) | **> 2.5 Å** | **vdW뿐** |

🔑 **결론**: DA는 **머리로 붙는다**. 붙고 나면 표면에 **–COO–Li 관능기**가 남고, 저자들은 이것이 **Li⁺ 전도를 방해하지 않는(투과 가능한) 층**이라고 주장한다(자기인용 ref [38] "waxing" 논문 + 폴리머 전해질 문헌 [39,40]). FTIR과 일관.

### 5.3 (§2.3) 수분 안정성 — 두 개의 서로 다른 보호막

**XRD (Fig 3a,b)**: bare는 **즉시** Li₂O₂ + LiCl 생성. DA-LPSCl은 **2 h까지 무변화**.
**σ (Fig 3c)**: bare 즉시 하락·계속 진행 vs DA 2 h 후 소폭.
**XPS S 2p (Fig 3d,e)**: bare는 30 min 노출로 **원소 S(163.2 eV) 급증**. DA는 노출 전후 거의 동일.

🔑 **가장 흥미로운 관찰**: **DA-LPSCl은 코팅 직후부터 이미 원소 S와 thiosulfate가 표면에 존재**한다. 저자 해석 — **DA의 –COOH가 LPSCl 표면을 살짝 산화시켜 놓았고, 그 산화-S 종이 오히려 부동태층(passivating interphase)으로 작동**해 추가 가수분해를 막는다. P 2p 신호가 거의 없다(Fig S7)는 것은 표면이 **산화-S + 탄소사슬**로 덮여 있음을 뜻한다(⚠ XPS 탐침 깊이 한계로 **아래층 phosphate 존재는 배제 못 함**, 저자 자인).

→ **보호 기전은 2중**:
1. **화학적 부동태** — 코팅 반응이 만든 얇은 산화-S 층
2. **물리적 장벽** — C10 소수성 알킬 사슬이 H₂O 접근·확산을 차단

### 5.4 (§2.4) 전기화학 — 무코팅 NCM85로 4.3 V

첫 사이클이 결정적이다. **bare는 <3.5 V에 완만한 sloping 구간**이 있는데 이게 **LPSCl 산화**의 지문이고, **DA에는 그 구간이 없다**. 그 결과가 **초기 CE 60 → 83 %**, 초기 방전 163 → 175 mAh/g.

율속에서 격차가 벌어진다: **1 C에서 55 → 104 mAh/g (약 2×)**. 저자 해석 — bare는 순환 중 생성된 **절연성 POₓ/SOₓ**가 계면 저항을 올려 고율속에서 무너진다.

수명: **150 cyc에서 96 % vs 61 %**. 저자는 이 성능이 NCM에 **LiNbO₃·Li₂ZrO₃·Li₃BO₃–Li₂CO₃·Li₂HfO₃/HfO₂ 코팅을 한 셀들과 동급 이상**이라 주장(예: LiNbO₃ 84 %/75 cyc, Li₂HfO₃/HfO₂ 81 %/200 cyc@45 °C).

확장 데이터: **4.6 V 컷오프 110 cyc 91 %**, **고로딩 21 mg/cm² → 3.2 mAh/cm², 150 cyc 81 %**(상용 LIB와 겨루려면 >3 mAh/cm² 필요하다는 자기 기준을 충족).

### 5.5 (§2.5) 개선의 기원 — 4개 기법의 삼각측량

**(a) EIS + TLM (Fig 5a, S12)** — 순환 전 두 셀의 bulk 저항은 비슷. 150 cyc 후 **R_cathode: bare 461 Ω vs DA 104 Ω (4.4×)**. Zuo와 같은 **TLM(blocking boundary) 분해** 방법론.

**(b) CV (Fig S11)** — bare는 **2.5 V에서 뚜렷한 anodic onset**, DA는 같은 구간 억제. 저자 귀속: **"전자 절연성 DA층이 전자 전달을 제한"** → *practical* oxidative stability 향상.
> 🔑🔑 **이 문장이 이 논문에서 우리에게 가장 중요한 한 줄이다.** 저자 스스로 **열역학적 창 확대가 아니라 전자 전달 차단(동역학)** 이라고 못 박았다. → 우리 **B①(무승부, S²⁻-pin) / B③(계면, 레버로 승부)** 축 분리와 **정확히 같은 프레임**.

**(c) XPS + ToF-SIMS (Fig 5b,c)** — 순환 후 복합양극에서 **원소 S(163.1 eV)가 bare에만 강하게** 나타남. ToF-SIMS는 **SO₂⁻·SO₃⁻·PO₂⁻·PO₃⁻ 조각이 bare에서 광범위, DA에서 훨씬 약함**. 이 열화는 **NCM 표면으로의 산소 확산**이 구동한다고 봄(Yamagishi ref[48], **Zuo ref[49]** 인용).

**(d) FIB-SEM (Fig 5e, S13, S14)** — **양쪽 다 intragranular crack**이 있고 입자 코어에서 시작해 방사상으로 전파. 그런데 **DA 쪽 파단 정도가 뚜렷하게 작다**.

🔑 **이 논문의 중심 메커니즘 주장**:
> 얇은 표면층이 NCM의 *부피 변화 자체*를 막을 리는 없다. 그런데도 crack이 줄었다 → **crack은 격자 변형의 직접 결과가 아니라 계면 화학 반응성의 *증상***이다.
> 경로: 절연성 SOₓ/POₓ 형성 → **국소 고전류밀도** → NCM 입자에 추가 기계 응력 + 고전압 산화 시 **기체 부산물(S 함유) 방출** → 파단 촉진.
> 근거 정렬: Manthiram 그룹(Lee/Su/Mesnier/Cui/Manthiram, Joule 2023 — "cracking vs surface reactivity") + Park et al. (AFM 2025).

### 5.6 (§2.6) Li 금속 — 소프트 코팅의 두 번째 역할

**대칭셀**: DA **1000 h** 안정 vs bare **230 h 단락**(덴드라이트). DA 셀 성능이 **Li/LiPON/LPSCl/LiPON/Li**(Su et al., EES 2022) 구성과 동급이면서 면적용량은 더 높다.

**기전 주장 (Fig 6b)**:
1. **기계적 순응** — 지방산 E ≈ 0.1–2 GPa ≪ LPSCl ~30 GPa (융점 31–32 °C가 낮은 강성의 방증). 스택 압력 하에서 변형하며 Li와 **밀착 wetting**, void 형성 억제, plating/stripping 응력 흡수.
2. **치밀화** — 2 wt% DA 펠릿 공극률 **6.9 % vs bare 10.1 %**. (Liu et al., ACS Energy Lett. 2025 — undecanethiol **표면 윤활에 의한 치밀화** 와 같은 현상; ⚠ 본문은 이걸 "enhances SE pellet porosity"라고 **정반대로 표기** — §12)
3. **균일 석출** — 순환 후 Li 표면 SEM이 bare는 거칠고 DA는 매끈(Fig S16).

**풀셀(Li 금속, 35 MPa, 7 mg/cm²)**: DA 100 cyc **166 mAh/g (94 %)**, 300 cyc **143 mAh/g (81 %)**. bare 100 cyc **97 mAh/g (57 %)**, 초기 20 cyc 평균 CE **90 %**.
저자 해석: **35 MPa는 낮은 압력**이라 bare는 접촉 불량 → void → 지속적 부반응 → CE 낮음. 고압에선 void가 기계적으로 붕괴되어 CE가 급상승하는데, **DA 셀은 이 압력 의존성이 거의 사라진다**(Fig 6e) — 소프트 코팅이 나노 void를 메워 **낮은 스택압에서도 밀착**.

> 🔑 **저압 작동 = 우리 DEM/제조 축과 직결되는 실용 주장** (§8).

---

## 6. 전체 논증 흐름

```
DA 용액코팅 (25 nm, 저온)
   ├─ [화학] FTIR + C1s XPS + DFT(−0.98 eV, Li–O 1.9 Å) ⟹ COO–Li 화학결합 (물리흡착 아님)
   │
   ├─ [수분] 소수성 C10 물리장벽 + 코팅이 만든 산화-S 부동태
   │        ⟹ XRD 무변화(2 h) · σ 91 % 유지 · S2p 불변
   │
   ├─ [양극] 전자 절연층 ⟹ CV 억제 · 첫충전 sloping 소실 · CE 60→83 %
   │        ⟹ ToF-SIMS SOx/POx ↓ · XPS 원소S ↓ ⟹ R_cat 461→104 Ω
   │        ⟹ crack ↓ (계면화학이 파단의 원인, 격자변형 아님) ⟹ 150cyc 96 %
   │
   └─ [음극] 소프트(0.1–2 GPa) + 치밀화(공극 10.1→6.9 %)
            ⟹ 밀착·균일석출 ⟹ 대칭셀 1000 h · 저압(35 MPa) 풀셀 300cyc 81 %

⟹ "하나의 저비용 코팅이 수분 + 양극 + 음극 3곳을 동시에 커버"
```

---

## 7. DFT / 계산 방법 ★ (SI "Theoretical Calculations" 전문)

### 7a. 분자부 (conformer)
- **code**: **Gaussian 16 Rev. C.01**
- **basis**: **Dunning correlation-consistent quadruple-zeta (cc-pVQZ) + diffuse 증강(= aug-cc-pVQZ)**
- **dispersion**: **Grimme D3**
- **functional**: **⚠ 미기재** — "Best-Practice DFT Protocols"(Bursch/Grimme, Angew 2022)를 따랐다고만 함. **재현 불가 수준의 누락**(§12)
- **입력 생성**: **ASE**
- **후처리**: 상대에너지 → **300 K Boltzmann 분포**(Eqn. S1 분배함수, S2 확률). ⚠ **전자에너지만** — ZPE·열보정·엔트로피 없음
- 초기 구조 10종: **PubChem "Capric Acid"** 항목에서 수급

### 7b. 슬랩부 (표면 + 흡착)
- **code**: **VASP** (Kresse 1993/1996)
- **method**: **PAW** (Blöchl)
- **functional**: **GGA-PBE** (vdW/D3 **없음** — ⚠ §12)
- **ecut**: **520 eV** (= Materials Project 표준)
- **k-points**: **Monkhorst–Pack, 밀도 ≥ 300/N** (N = 원자수) — 즉 원자수에 반비례하는 자동 밀도
- **수렴**: 에너지 **1e-5 eV**, 힘 **0.01 eV/Å**
- **초기 구조**: **Materials Project `mp-985592`** (argyrodite)
- **슬랩 생성**: **pymatgen** (`SlabGenerator` + VASP 입력 자동 생성), **대칭 저지수 면**
- **진공**: 표면E 계산 **10 Å 양면** / 흡착 계산 **분자 쪽만 15 Å**
- **이완**: **전 원자 자유**(반대면 무구속) — Fig S6로 반대면 정지 확인 = 두께·진공 타당성 검증
- **무질서 처리**: **없음** — `mp-985592` 단일 질서 배열. **argyrodite의 4a/4d Cl/S site disorder를 전혀 다루지 않는다** (⚠ 우리 [Adeli] 중성자 점유율 0.615/0.834 기준으로 보면 큰 단순화)
- **DFT+U / spin**: 미기재
- **흡착 배위 샘플링**: 표면 5자리 × 배향 2종 = **10 configuration**, 초기 이격 2 Å, **수직 배향만**

### 7c. 슬랩 조성으로 읽는 비화학량론
Table S2 슬랩 조성이 `Li₃₆P₆S₂₈Cl₁₀`, `Li₃₇P₈S₃₅Cl₁₁` 등으로 **P:S:Cl 비가 종단마다 다르다** → 표면E 비교가 **같은 화학퍼텐셜 기준으로 정규화되었는지 불명**. 비화학량론 슬랩의 표면E는 원래 **μ 의존(Wulff/chempot 다이어그램)** 인데, SI엔 μ 처리 언급이 없다. → **표면E 절대값·서열은 "이 논문 조건에서"로 한정 인용**(§12).

---

## 8. Figure / Table set ★

### 본문
| Fig | 내용 | 우리 활용 |
|---|---|---|
| **1a** | Cryo-TEM: 25 nm 비정질 conformal 코팅 | 코팅 두께 스케일 레퍼런스 |
| 1b | EDX map: C, O 균일 | 코팅 균일도 증명 포맷 |
| 1c,d | C 1s XPS bare vs DA (**O–C=O** 증가) | **유기 코팅 검증의 표준 XPS 지문** |
| 1e | FTIR (–CH₂– 3000–2800, C–O/C=O 1700–1350) | 우리 SDCP 분자계 FTIR 대조에 재활용 가능 |
| **2** ★ | **DFT 결합E(파랑)·거리(초록)·흡착 기하** — 극성 머리 vs 비극성 꼬리 | **분자-표면 흡착 계산의 그림 양식** (우리 코팅/도판트 흡착 계산 시 이 레이아웃 차용) |
| 3a,b | XRD 시계열 (bare: Li₂O₂ ★red + LiCl ★black 즉시 / DA: 2 h 무변화) | **수분 열화 정량의 표준 그림** |
| 3c | σ vs 노출시간 | B④ 축 관측량 포맷 |
| 3d,e | S 2p XPS 노출 전후 | **161.6/163.2/166.6/168 eV 4종 귀속 = 우리 XPS anchor 대조표** |
| 3e(도식) | LPSCl 수분 열화 모식 | deck용 |
| 4a,b | 초기 충방전 (DA는 <3.5 V sloping 없음) | **"SE 산화의 전기화학 지문" 판독법** |
| 4c | Rate (0.2 C 183/162, 1 C 104/55) | 계면 저항 → 율속 병목 논거 |
| 4d,e | 150 cyc (96 % vs 61 %) | 성능 인용 |
| **5a** | Nyquist + TLM (R_cat 104 vs 461 Ω) | **[Zuo] TLM과 동일 방법론 — 계면 열화 정량 틀** |
| 5b | 순환 후 S 2p (160.2/161.1/163.1) | **free S²⁻ 분리 피팅 = 우리 free-S site-PDOS 서사의 실험 관측량** |
| **5c** | **ToF-SIMS SOₓ/POₓ heat map** | **[Zuo] Fig 4·5와 같은 종·같은 도구 → 3편 교차검증** |
| 5d | 보호 기전 모식 | deck |
| 5e | FIB 단면 (crack 비교) | 파단 = 계면화학 증상 논거 |
| 6a | Li‖Li 대칭셀 (1000 h vs 230 h) | 음극축 인용 |
| 6b | Li 계면 안정화 모식 | deck |
| 6c,d | Li 금속 풀셀 35 MPa | **저압 작동 = 제조축 연결** |
| 6e | 복합양극 내 DA 역할 모식 | deck |

### SI
| 항목 | 내용 | 우리 활용 |
|---|---|---|
| Fig S1 | SEM (형상·응집 무변화) | — |
| Fig S2 | XRD (Kapton 밀봉, 코팅 전후) | 벌크 무변화 대조군 |
| **Fig S3** ★ | **최안정 (010) 면, 0.4 J/m²** | **우리 슬랩 파이프라인 facet 선택 근거** |
| Fig S4 | DA conformer 10종 시각화 | — |
| Fig S5 | 선택된 5개 흡착 자리 | 자리 샘플링 설계 참고 |
| Fig S6 | 슬랩 반대면 정지 확인 | **슬랩 두께 타당성 검증 관행 — 우리도 채택할 만함** |
| Fig S7 | P 2p XPS (bare vs DA — DA는 신호 거의 없음) | 표면 피복률 증거 |
| Fig S8 | 5 wt% DA 셀 충방전 (성능 저하) | 과코팅 페널티 |
| Fig S9 | **4.6 V 컷오프 110 cyc 91 %** | 고전압 확장 |
| Fig S10 | **고로딩 21 mg/cm², 3.2 mAh/cm²** | 실용 로딩 |
| **Fig S11** | **CV (bare 2.5 V onset, DA 억제; 1–3 cyc)** | **B① vs B③ 분리의 실험 증거** |
| Fig S12 | TLM 등가회로 | 피팅 모델 |
| Fig S13,14 | FIB 단면 (DA / bare, 200 MPa 조립) | — |
| **Fig S15** | **공극률 bare 10.1 / 2 wt% 6.9 %** | **DEM/제조축 직결** |
| Fig S16 | 순환 후 Li 표면 SEM | 석출 균일도 |
| **Table S1** | conformer 에너지·확률 | Boltzmann 후처리 양식 |
| **Table S2** ★★ | **표면 종단 6종 × 표면E** | **우리 γ_SE 외부 DFT 대조군 (§9)** |
| **Table S3** | σ vs DA wt% (1.4/1.3/0.7/0.2) | **코팅량 trade-off 정량** |
| **Table S4** | 표면개질 LPSCl 11종 수분 비교 | **B④ 문헌 지도 (조건 제각각 — 순위 인용 금지)** |

---

## 9. Post-processing ★

| 무엇 | 도구 | 수치화·기록 방식 |
|---|---|---|
| **분자 conformer 앙상블** | Gaussian 16 + **ASE**(입력 생성) + PubChem(초기 구조) | 상대에너지를 **K 단위**로 표기 → **분배함수 Z = Σe^(−Eᵢ/k_BT)** → **P(Eᵢ)** 로 표 작성. **최다 확률 배좌 1개만 후속 계산에 사용** |
| **슬랩 생성·표면E** | **pymatgen** (슬랩 + VASP 입력) | 대칭 저지수 면 전수 → **Miller / termination 조성 / 슬랩 화학식 / γ (J/m²)** 4열 표 |
| **슬랩 타당성 검증** | 시각적 이완 궤적 | **"반대면 원자가 안 움직였다"를 Fig로 제시**(구속 대신 사후 검증) |
| **흡착 결합E** | VASP | `E_bind = E(slab+mol) − E(slab) − E(mol)`, **10 config 스캔**, 그림에 **결합E(파랑) + 결합거리(초록)** 를 기하와 함께 병기 |
| **결합 성격 판별** | 결합길이 비교 | **Li–O 1.9 Å ≈ Li–OH 1.9–1.95 Å** → 화학결합 / **>2.5 Å** → vdW. ⚠ **전하해석(Bader)·COHP 없음** |
| **TLM 임피던스** | **RelaxIS** | blocking BC 전송선 모델 → **R_bulk / R_cathode 분리**, 순환 전후 비교 |
| **ToF-SIMS** | SurfaceLab 7.2 | **total ion count 정규화** → 정규화 이미지에서 강도 추출 → heat map. **200 × 200 µm²**(NCM D50 ~5 µm 다수 포함) = 샘플링 편향 최소화 |
| **XPS 피팅** | — | S 2p는 **2p₃/₂ 기준 BE**로 성분 분해(3–4성분) |
| **공극률** | 상대밀도 측정 | 상대밀도 → 공극률 % |

> 우리 적용: **(a) pymatgen 슬랩 전수 + termination별 γ 표**, **(b) 흡착 결합E 스캔 그림 양식(E + 거리 동시 표기)**, **(c) 슬랩 반대면 정지 검증 Fig** 3가지는 우리 slab/adhesion 파이프라인에 바로 이식 가능.

---

## 10. 우리 DFT 대비 (comp1 / modelc) → `../our_dft_baseline.md`

| 항목 | 이 논문 | 우리 | 일치 / 차이 + 이유 |
|---|---|---|---|
| **표면E (LPSCl)** | **(010) Li₅SCl 종단 0.40 J/m²** (범위 0.40–0.72; PBE 결정질 슬랩) | `adhesion.json` γ_SE: **comp1 1.211** · comp2 1.189 · **comp3 0.565 · comp4 0.450 · comp5 0.470 J/m²** (UMA-s-1p2 **3000 K melt-quench 비정질** 표면) | **△ 부분 일치 — 그러나 이게 우리 γ_SE의 첫 외부 DFT 앵커다.** 그들의 0.40 은 우리 **Li-결손(Cl-rich) 조성대 0.45–0.57 밴드 한복판**에 떨어진다. 반면 우리 **comp1(Li₆, 무공공) 1.211 은 3× 높다**. 흥미로운 건 그들도 **Li₇SCl(Li 과잉) 0.72 > Li₅SCl 0.40** — "**Li 과잉 종단이 비싸다**"는 방향이 우리 "공공이 표면E를 낮춘다"(kb/methodology/adhesion_energy.md)와 **같은 부호**. ⚠ **단 방법이 3중으로 다르다**(PBE-DFT 결정질 저지수 vs UMA 비정질 melt-quench, 종단 정의, 비화학량론 μ 처리 유무) → **"우리 값이 검증됐다" 금지, "같은 자릿수·같은 방향" 까지만** |
| **산화 onset** | **CV anodic onset 2.5 V** (SE+CNF 95:5, 0.1 mV/s, vs Li⁺/Li) · 서론도 "> 2.5 V에서 산화분해" | **grand-potential 2.256 V** (LiS4 제외) / 2.14 (포함) · OCV 1.717 V | **✓ 정합.** 우리 열역학 onset 2.26 < 실험 apparent onset 2.5 V — **이론 < 실험(kinetic 지연)** 방향이 맞고 격차 0.24 V. [GG] K_eff=0 2.40 V, [Zuo] 동일 peak, [Rupp] 2.0–2.2 V 밴드와 한 줄. **B① 무승부 축 재확인** |
| **코팅이 onset을 옮기나** | **아니다** — 저자 명시 "**electronically insulating** DA layer **limits electron transfer**" → *practical* oxidative stability | 우리 cascade: 대부분 도판트가 **2.14 V pin**, B₂O₃만 2.317(+0.18) 등 소수 예외 | **✓✓✓ 프레임 동일.** 이 논문은 **열역학 창을 못 넓힌다는 걸 저자가 자인**하고 이득을 **전자 절연**에 귀속. = 우리 **"onset은 S²⁻-pin·이득은 전자 절연 CEI(Nd/B₂O₃)"** 서사의 **외부·실험·독립 증거**. deck에 그대로 인용 가능 |
| **분해 산물** | ToF-SIMS **SO₂⁻·SO₃⁻·PO₂⁻·PO₃⁻** + XPS **원소 S 163.1 eV** | `interface_reactivity`: **Li₃PO₄ · Li₂SO₄ · Li₂S · LiCl · Co₉S₈**(vs LiCoO₂); 산화 staircase 2.14 폴리설파이드 → 3.06 원소 S | **✓✓ 같은 산물군.** phosphate(PO₃⁻)·sulfate/sulfite(SO₃⁻)·원소 S 3종이 우리 grand-potential 산물과 1:1. **[Zuo] Fig 4·5와 같은 종·같은 도구** → **황화물 양극 계면 산화 산물 = 3편(Zuo/Liu/Qian) 독립 확증** |
| **XPS BE anchor** | S 2p₃/₂: **160.2 free S²⁻** · **161.1/161.6 PS₄³⁻** · **163.1/163.2 원소 S** · 166.6 thiosulfate · **168 polythiosulfate** | `xps_reference_sei.csv`: **Li₂S 160.2** · **PS₄ thiophosphate 161.6** · **Li₂SO₄ 168.0** | **✓✓✓ 3점 정확 일치**(160.2 / 161.6 / 168.0). 우리 anchor 테이블이 이 논문 계면·수분 화학을 BE 수준으로 커버함을 재확인. **추가 획득: thiosulfate 166.6 eV** = 우리 테이블에 **없던 중간산화 S 종** → anchor 후보(§11 ⑤) |
| **탄성계수 (LPSCl)** | **"~30 GPa"** (문헌 인용, 출처 미명시) | **E_VRH comp1 22.06 / modelc 27.66 GPa** (DFT relaxed-ion) | **✓ 정합.** 우리 modelc 27.66이 그들 "~30"과 사실상 같은 값. ⚠ 그들은 출처 없는 round number라 **우리 값을 그들 값으로 검증했다고 쓰면 안 됨**; 반대로 **우리 DFT 값이 실험/문헌 통념대로 나온다**는 sanity check로만 |
| **Li–O 결합길이** | **1.9 Å** (표면 Li–carboxylate O, 화학결합 판정 기준) | `b2o3_bond_lengths.json`: **P–O 1.556** · B–S 1.827 · Li–S 2.486 · Li–Cl 2.525 Å (Li–O 항목은 미기록) | **△ 직접 비교 불가** (우리 B₂O₃/LPSOCl 계는 Li–O 통계를 아직 안 뽑음). **후속 액션**: 우리 O-doped 계에서 **Li–O 평균 결합길이를 추출**하면 그들 1.9 Å 기준과 직접 대조 가능 (§11 ④) |
| **무질서 처리** | **없음** — `mp-985592` 질서 단일 배열 슬랩 | 우리는 **[Adeli] 중성자 점유율(4a-Cl 0.615 / 4d-Cl 0.834 / Li 48h 0.456) decorate** | **✗ 그들이 훨씬 단순.** 그들 표면E·결합E는 **site disorder 평균이 아니라 한 배열의 값** → **±(수십 meV ~ 0.1 eV) 배열 편차 미평가**. 우리 무질서 규율이 이 지점에서 우위 |
| **vdW 처리** | 분자부만 **D3**, **슬랩·흡착부엔 vdW 없음(순수 PBE)** | 우리 슬랩/흡착 계산 관행 | **✗ 그들 약점.** **비극성 꼬리 −0.077 eV = 물리흡착인데 PBE엔 vdW가 없다** → 이 값은 **구조적으로 과소평가**. "머리 vs 꼬리 −0.98 vs −0.077" 대비는 **정성적으론 맞아도 정량 배율(12×)은 인용 금지** (§12) |
| **가수분해 열역학** | **계산 0** (실험 XRD/XPS만) | 우리도 **ΔG_hyd 계산 0** ([Zhu20] 레시피 보유) | **✗ 양쪽 다 공백.** 이 논문은 B④를 **실험으로만** 다룸. → 우리가 [Zhu20] 레시피로 **DA/유기 코팅의 열역학 판정**을 하기는 여전히 어려움(유기물이 MP hull 밖) — **정직하게 "코팅 축은 우리 hull 밖"** 으로 유지 |

---

## 11. 적용 인사이트 (우리 캠페인에 어떻게)

1. **🔑 B① / B③ 축 분리의 외부 실증 확보.** "코팅으로 산화 안정성이 좋아졌다"는 논문이 **스스로 열역학이 아니라 전자 절연이라고 명시**한다. → deck에서 "**intrinsic onset은 S²⁻-pin으로 불변(우리 2.256 V·Banik S-pin), 실전 이득은 전자 절연 CEI에서 온다**"를 말할 때 **Nazar 그룹 실험 논문을 근거로 붙일 수 있다**. `comparison_vs_ours.md` **B③ "레버 = SE 코팅"** 칸에 [Kang25](무기·SOC 균일화) 옆에 [Qian26](유기·전자 절연)을 **다른 기전으로** 나란히 세운다.

2. **🔑 우리 γ_SE(UMA)의 첫 외부 DFT 대조군.** Table S2는 **LPSCl 저지수 슬랩 표면E의 공개 DFT 값**이다. 우리 `adhesion.json` γ_SE는 지금까지 **외부 검증 0**이었는데, 이제 **0.40 J/m²(Li₅SCl (010))** 라는 기준점이 생겼다. 후속 액션 2가지:
   - (a) 우리 **crystalline slab MQA(adhesion_v5, in_progress)** 에서 **(010) Li₅SCl 종단을 명시적으로 포함**해 직접 비교
   - (b) **comp1 γ_SE 1.211**이 그들 어느 종단(S-종단 0.70? 그 이상?)에 대응하는지 확인 — **우리 melt-quench 표면이 결정질 최저면보다 비싸게 나오는 게 물리적인지 방법 artifact인지** 판정. **비정질 표면은 원래 더 비쌀 수 있으므로 artifact 단정 금지.**

3. **B④ moisture 축의 "코팅 레버" 칸 신설.** 지금 B④는 [Zhu20](열역학 지도) + [Yang25](O 격자도핑) + [Wang22](열) 구성인데, 여기에 **표면 코팅 레버**가 통째로 빠져 있었다. Table S4가 **그 레버의 문헌 지도 11종을 한 표로** 준다. ⚠ 단 **조건이 제각각(RH <1–50 %, 30 min–3일)이라 순위 인용 금지**, "레버 존재·대략 수준"까지만.

4. **Li–O 1.9 Å 판정 기준을 우리 O-doped 계에 적용.** 그들은 "Li–O 1.9 Å ≈ Li–OH → 화학결합"이라는 **간단한 결합길이 판정**을 쓴다. 우리 `b2o3_bond_lengths.json`엔 **Li–O 항목이 없다** → **LPSOCl/+B₂O₃ 구조에서 Li–O 통계를 뽑아 추가**하면 (a) 그들 기준과 직접 대조, (b) 우리 ICOHP(P–O −8.43)와 결합길이의 짝을 완성.

5. **XPS anchor 확장 — thiosulfate 166.6 eV.** 우리 `xps_reference_sei.csv`는 **Li₂S 160.2 / PS₄ 161.6 / Li₂SO₄ 168.0** 3점을 가지고 있는데, 이 논문이 **원소 S 163.2**와 **thiosulfate 166.6**를 채워 준다. → **S 산화 사다리 5점(160.2 → 161.6 → 163.2 → 166.6 → 168.0)** 이 완성된다. 우리 산화 staircase(2.14 폴리설파이드 → 3.06 원소 S)의 **XPS 대응표**로 바로 쓸 수 있다. ⚠ 이 논문 값은 **실험 BE, 우리 anchor는 문헌/ΔSCF** — 출처 열 구분해 등록.

6. **제조·DEM 축 연결 (공극률 10.1 → 6.9 %).** 소프트 유기 코팅이 **표면 윤활 → 냉간가압 치밀화**를 일으킨다(Liu ACS Energy Lett. 2025와 같은 현상). 이건 **우리 DEM 캠페인의 입자 표면 마찰계수 파라미터에 직접 대응하는 실험 관측량**이다 — DEM 쪽에서 "코팅으로 μ를 낮추면 상대밀도가 얼마나 오르나"의 **실측 앵커**로 쓸 수 있다.

7. **"crack은 계면 화학의 증상" 명제.** 얇은 코팅이 부피변화를 못 막는데도 crack이 준다 → **파단의 1차 원인이 격자 변형이 아니라 계면 반응성**. 이건 우리 `intergranular_cracking_nmc811_jmca2023` / `bucci2017` / DEM-기계 축과 **정면으로 맞물리는 주장**이고, 우리가 chemo-mechanical 커플링을 논할 때 **"화학 → 국소 전류밀도 → 응력"** 경로를 인용할 근거다. ⚠ 단 이 논문의 증거는 **FIB 단면 정성 비교**뿐(정량 crack density 없음) → **"제안된 메커니즘"** 으로만.

8. **우리가 이 논문보다 잘 할 수 있는 것 (기여 여지).** 그들의 DFT는 (i) **무질서 없음**, (ii) **슬랩에 vdW 없음**, (iii) **HCl 방출 반응E 미계산**(결합길이로 추론만), (iv) **Bader/COHP 없음**, (v) **피복률 의존성 없음**(단분자 1개만), (vi) **functional 미기재**. → 우리 파이프라인(무질서 decorate + LOBSTER ICOHP + Bader + 표면 흡착)으로 **"유기 코팅이 argyrodite 표면에 어떻게 붙나"를 훨씬 엄밀하게** 다시 할 수 있다. **coating adsorption = 우리 slab 파이프라인의 자연스러운 다음 타깃.**

---

## 12. ⚠ 주의 / 한계 (over-claim 방지 · 이 논문에 대한 비판)

### 계산 쪽 (우리에게 직접 관련)
1. **Gaussian 계산의 functional이 명시되지 않았다.** basis(cc-pVQZ+diffuse)·dispersion(D3)만 있고 **범함수가 없다** → conformer 에너지 재현 불가. Table S1을 인용할 땐 "범함수 미기재"를 반드시 병기.
2. **슬랩·흡착 계산에 vdW 보정이 없다(순수 PBE).** 그런데 **비극성 꼬리 흡착은 정의상 vdW 지배**다. 따라서 **−0.077 eV는 구조적 과소평가**이고, "머리가 꼬리보다 12배 강하다"는 **정량 배율 인용 금지**. 정성 결론(머리로 붙는다)만 살아남는다. — 분자부엔 D3를 쓰면서 슬랩부엔 안 쓴 건 **방법론적 비일관**.
3. **꼬리 결합E 부호가 양수(+0.077 eV)로 인쇄**되어 있다. 본문 문맥("binding energies are significantly weaker")상 **−0.077의 오식**으로 읽히지만, **원문 그대로면 흡착이 불안정하다는 뜻** — 인용 시 원문 표기 병기.
4. **무질서 전무.** `mp-985592` 단일 질서 배열. argyrodite의 4a/4d Cl/S disorder([Adeli] 실측 0.615/0.834)를 무시 → **표면 종단 조성·표면E·흡착 자리 모두 배열 의존**인데 오차 미평가.
5. **비화학량론 슬랩의 μ 처리 불명.** Table S2 슬랩들은 P:S:Cl 비가 서로 다른데(P₆ vs P₈, S₂₈ vs S₃₅) **화학퍼텐셜 기준 정규화 언급이 없다** → **종단 간 표면E 서열이 μ 선택에 따라 바뀔 수 있다**. "0.40이 최저면"은 **이 논문 조건 한정**.
6. **HCl 방출은 계산되지 않았다.** "Li–O 1.9 Å ≈ Li–OH 1.9–1.95 Å → HCl 방출로 lithium decanoate 생성"은 **결합길이 유추**일 뿐, **반응 에너지·전하 이동(Bader)·COHP 어느 것도 없다**. HCl은 셀 안에서 무해하지 않은 부산물인데 **검출 시도조차 없다** — 실험적으로도 미확인.
7. **피복률 1분자.** 실제 25 nm 층은 다층 조립인데 계산은 **고립 분자 1개**. 사슬-사슬 상호작용·패킹·Li⁺ 투과 경로는 **전혀 다루지 않는다**. 저자가 주장하는 "COO–Li가 Li⁺ 전도를 돕는다"는 **계산으로 뒷받침되지 않고 문헌 인용뿐**.
8. **평행 배향 배제의 근거가 약하다.** 비용 + "엔트로피 페널티"라고 했지만, **실제 지방산 단분자막은 흔히 기울어져 패킹**한다. 수직 배향만 본 건 **모델 한계**로 명시 필요.

### 실험·서술 쪽
9. **bare LPSCl의 σ 절대값이 없다.** Table S3은 DA 함량별 값만 준다 → **코팅에 의한 σ 손실률을 계산할 수 없다**. (상용 Ampcera LPSCl은 통상 ~1.5–3 mS/cm이나 **이 논문이 측정값을 안 줬으므로 추정 금지**.)
10. **Table S3(2 wt% = 1.3 mS/cm)과 Table S4(코팅 후 1.13 mS/cm, 유지율 91 %)가 어긋난다.** 1.13이 노출 후 값인지 코팅 직후 값인지 표 헤더("Conductivity after coating")로는 모호. **초록·결론의 "> 1 mS/cm 유지"만 안전한 인용.**
11. **논문 내부 수치 불일치 3건**:
    - 초록/§2.4 "**150 cyc 96 %**" ↔ 서론 "**300 cyc 90 %**" (Li–In). 어느 쪽 실험인지 불명 → **150 cyc 96 %만 인용**.
    - 초록/결론 "대칭셀 bare **230 h**" ↔ 서론 "**200 h**".
    - 그림 번호 오기: 본문이 TLM을 "Figure S7"(실제 S12), 고로딩을 "Figure S9"(실제 S10), FIB-EDX를 "Figures S8/S9"(실제 S13/S14)로 지시.
12. **PS₄³⁻ BE가 섹션마다 다르다(161.6 vs 161.1 eV).** 우리 anchor(161.6)와 비교할 땐 **수분 섹션 값**을 쓰고, 계면 섹션 값은 별도 취급.
13. **Liu et al. 인용 오기**: "coating LPSCl with undecanethiol **enhances SE pellet porosity**" — 원논문 제목이 *Densifying Solid Electrolytes Through Surface Lubrication*이고 본 논문 자신의 데이터도 **공극률 감소**다. **"reduces porosity"의 오기**.
14. **FTIR 대역 귀속이 문장 안에서 뒤바뀌어 있다** (3000–2800을 C–H, 1700–1350을 C–O라고 써야 하는데 순서가 꼬임). 화학적으로는 **3000–2800 = C–H, 1700–1350 = C=O/C–O** 가 맞다.
15. **Table S4는 순위표가 아니다.** RH·시간이 제각각(자인). **"DA가 최고"라는 주장은 이 표로 성립하지 않는다** — UDSH(33 %/5 h/86 %)가 더 가혹한 조건이다.
16. **DA-LPSCl은 코팅 직후 이미 표면이 산화되어 있다**(원소 S + thiosulfate). 저자는 이를 "부동태화"라고 긍정 해석하지만, **σ 손실(Table S3)과 같은 원인일 가능성**을 배제하지 못했다. **"손실 없는 코팅"이 아니다.**
17. **장기 수분 데이터 없음** — 2 h가 최장. **드라이룸 실사용(수 시간~일 단위)** 주장엔 부족.
18. **양극 vs 음극 이득의 분리가 안 되어 있다.** 같은 코팅이 3곳(수분·양극·음극)에서 동시에 작동하는데, 풀셀 성능 향상 중 **어느 몫이 양극 계면이고 어느 몫이 저압 접촉 개선인지** 실험적으로 분리되지 않았다.
19. **DOI(`10.1002/anie.9983580`)가 Wiley 통상 체계(anie.2026xxxxx)와 다르다.** SI 파일명은 `anie73015`. **최종 인용 전 DOI 재확인 필요.**

---

## 13. 인용 가능 문장 (deck / 원고용)

- "Qian et al. attribute the improved anodic stability of their coated argyrodite explicitly to the **electronically insulating nature** of the organic layer limiting electron transfer — i.e. a *kinetic* barrier, not a widened thermodynamic window. This is consistent with our grand-potential result that the intrinsic oxidation onset of Li₆PS₅Cl and Li₅.₄PS₄.₄Cl₁.₆ is identical (2.256 V, S²⁻-limited) and cannot be moved by composition alone."
- "Their PBE surface energies for low-index Li₆PS₅Cl slabs (0.40–0.72 J m⁻², lowest for the Li₅SCl-terminated (010) facet) provide the first external DFT reference for our UMA-derived γ_SE values (0.45–1.21 J m⁻²), with the Li-deficient compositions falling in the same 0.4–0.5 J m⁻² band."
- "The S 2p binding energies reported here (160.2 free S²⁻, 161.6 PS₄³⁻, 163.2 S⁰, 166.6 thiosulfate, 168 polythiosulfate) match our SEI anchor table to within 0.1 eV at three points and extend it with an intermediate thiosulfate marker."
- "ToF-SIMS SOₓ/POₓ mapping in coated vs bare composite cathodes reproduces the same decomposition species that our grand-potential interface reactivity predicts (phosphate, sulfate, elemental sulfur, LiCl) — now confirmed independently across Zuo (2022), Liu (2025) and Qian (2026)."
- "A 25 nm soft organic layer reduced the SE pellet porosity from 10.1 % to 6.9 % and largely removed the stack-pressure dependence of the first-cycle Coulombic efficiency — a direct experimental anchor for surface-friction parameters in our DEM compaction model."
- ⚠ 쓰면 안 되는 문장: "*이 논문의 DFT가 우리 표면에너지를 검증한다*"(방법 3중 상이) · "*DA 코팅이 산화 창을 넓힌다*"(저자 주장과 반대) · "*Table S4에서 DA가 최고 수분 안정성*"(조건 비교 불가) · "*머리가 꼬리보다 12배 강하게 결합*"(vdW 부재로 배율 무효).

---

## 14. 기법 용어 미니사전

- **DA (decanoic acid / capric acid)**: C₉H₁₉COOH, 탄소 10개 포화 지방산. 융점 31–32 °C. 논문은 표면에 붙은 형태를 **decanoate(C₁₀H₁₉O₂⁻)** 로 표기.
- **conformal coating**: 입자 표면 굴곡을 그대로 따라 균일 두께로 덮는 코팅(vs 섬 형태 island 성장).
- **Cryo-TEM**: 저온에서 빔 손상을 줄여 관찰 — 유기·황화물처럼 빔에 약한 시료의 계면층을 보는 표준.
- **conformer / Boltzmann 앙상블**: 분자의 회전이성질체. 상대에너지에서 **P(Eᵢ) = e^(−Eᵢ/k_BT) / Z** 로 실온 존재 비율을 구한다.
- **cc-pVQZ (+diffuse)**: Dunning의 correlation-consistent quadruple-zeta 기저함수. diffuse 증강 = aug- 접두. 분자 계산에선 고급 기저.
- **D3**: Grimme의 경험적 분산(vdW) 보정. **PBE 자체엔 vdW가 없다** — 물리흡착 계산엔 필수.
- **termination (표면 종단)**: 결정을 어느 원자층에서 자르냐. 같은 Miller 지수라도 종단이 다르면 표면E가 크게 다르다(이 논문 (010)에서 0.40 vs 0.72).
- **표면에너지 γ (J/m²)**: 벌크를 쪼개 새 표면 1 m²를 만드는 비용. 낮을수록 그 면이 잘 노출된다(Wulff 형상 지배).
- **E_bind (흡착 결합에너지)**: `E(슬랩+분자) − E(슬랩) − E(분자)`. 음수 = 붙는 게 이득.
- **TLM (transmission line model)**: 다공성 복합전극의 임피던스를 이온·전자·전하이동 저항으로 분해하는 등가회로. 여기선 blocking boundary condition으로 R_cathode 추출.
- **ToF-SIMS**: 이온빔으로 표면을 때려 나온 2차이온을 질량분석 → 분자 조각 수준(SO₂⁻, PO₃⁻ …) 공간 분포. XPS보다 검출 감도가 수 자릿수 높다.
- **thiosulfate / polythiosulfate**: S₂O₃²⁻ 계열 중간 산화 황종. XPS S 2p 166–168 eV 대역.
- **initial CE (초기 쿨롱 효율)**: 첫 사이클 방전/충전 용량비. SE 산화 같은 비가역 부반응이 크면 낮아진다 — **첫 사이클이 계면 반응성의 가장 민감한 지표**.
- **intragranular cracking**: 다결정 NCM 2차입자 내부 **1차입자 안쪽**을 가로지르는 균열(입계 균열 = intergranular과 구분).
- **stack pressure**: 전고체셀 조립·작동 중 가하는 축압. 낮을수록 실용적이지만 접촉 유지가 어려워진다(이 논문 35 MPa = 상대적 저압).

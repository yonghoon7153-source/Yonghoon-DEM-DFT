# PAMPS-그래프팅 CNT 도전제로 고면적하중 전극 + 캐소드→애노드 crosstalk — Jung (Adv. Mater. 2026)

> slug `jung2026_pamps_cnt_crosstalk_high_loading_lmb` · DOI `10.1002/adma.202516395` · type `exp+DFT+MD` · PDF `72._Advanced_Materials__2025__Jung__Enhanced_Kinetics_and_Dual_Interfacial_Stability_in_High_Areal_Loading_Electrodes_for.pdf` · digested `2026-09-03` · status ✅

---

## 0. ★★★ 결론 먼저 — 우리 원고 `[36]` 인용의 정체 (provenance 판정)

**요청 사유**: 우리 SDCP 원고가 LPSCl+바인더 펠릿 전도도 문장 끝에 이 논문을 `[36]` 으로 달고,
그 수치(3.57 / 0.97 / 2.86 mS/cm)가 **D13 펠릿 보정**을 실제로 구동한다
(`docs/reviews/pellet_calib_freeze_20260825.md`, 작업 브랜치 `manuscript-track`).

### 판정 (본문 13 pp + SI 전수 판독 결과)

| 질문 | 답 | 근거 |
|---|---|---|
| 3.57 / 0.97 / 2.86 mS/cm 가 이 논문 값인가? | **아니다.  이 논문에 없다.** | 이 논문은 **LPSCl 을 한 번도 안 쓴다** · **황화물 SE 0회** · **펠릿 0회** · **9:1 바인더:SE 혼합 0회** · **DC 분극 σ_e 측정 0회** |
| 그럼 어디 값인가? | **우리 원고 저자(실험 협력자)의 자체 측정** | 원고 문장이 `(Figures 2h and S8)` · σ_e 는 `(Figures 2i and S9)` = **우리 원고 자신의 그림**을 가리킨다 |
| `[36]` 은 무슨 역할인가? | **지지·선례(supporting precedent) 인용**, 데이터 출처 아님 | 같은 문단의 인용 패턴이 전부 그렇다 — `[34]` Alessandri = PEDOT Raman 귀속 · `[35]` Patil/Wudl/Heeger 1987 = self-doping 개념 원전 · `[37]` = 두 바인더 역할분담.  **전부 자기 측정 문장 끝에 붙는 근거 인용** |
| 이 논문이 지지하는 명제는? | "**술폰산(-SO₃H) 관능 고분자는 Li⁺ 수송을 막지 않고 오히려 돕는다**" | 이 논문 **PAMPS 필름 σ_ion = 6.05×10⁻⁴ S/cm ≈ PAM 필름의 2배** (본문 stated) + "sulfonic acid groups that facilitate Li⁺ transport" |
| **압력·온도 규약을 여기서 확정할 수 있나?** | **아니다.  이 논문에서는 원리적으로 불가능하다.** | 재는 대상 자체가 다르다 (액체 전해질 코인셀 · 팽윤 고분자 필름).  우리 펠릿의 성형압/측정압/온도는 **원고 저자에게 직접 물어야 한다** |

### ⇒ **사용자가 요청한 결론 문장**

> **"D13 에서 쓴 3.57 / 0.97 / 2.86 mS/cm 는 Jung 2026 (Adv. Mater. 38, e16395) 의 값이 아니다.
> 우리 원고 저자의 자체 측정(Fig 2h·2i·S8·S9)이고, `[36]` 은 '술폰산 고분자가 Li⁺ 수송을 돕는다'
> 는 명제의 선례 인용이다.  그 측정의 압력·온도 규약은 이 논문에도, 우리 원고 Experimental
> Section 에도 **적혀 있지 않다** (⇒ `조건 미기록`).  원고 저자 확인 전까지 D13 앵커는
> '압력·온도 미기록' 라벨을 달고 인용해야 한다."**

### 우리 원고가 실제로 적어 놓은 조건 (교차확인, `Manuscript v6` Experimental Section)

| 항목 | 기재 여부 | 값 |
|---|---|---|
| 혼합비 | ✅ | LPSCl : 바인더 = **9:1 wt** |
| σ_ion 방법 | ✅ | **ion-blocking 대칭셀 EIS** |
| σ_e 방법 | ✅ | **DC 분극 0.5 V, 30 min** |
| EIS 주파수·진폭 | ✅ | Bio-Logic SP-300, **7 MHz – 10 mHz**, AC **5 mV** |
| **펠릿 성형압** | ❌ **미기재** | (셀 조립압 433 MPa / 200 MPa 는 **mold cell** 용이지 이 펠릿 아님) |
| **측정 시 인가압** | ❌ **미기재** | — |
| **온도** | ❌ **미기재** | (30 °C 는 **사이클 시험** 조건으로만 적혀 있다) |
| 펠릿 두께·면적·전극재질 | ❌ **미기재** | — |

⚠ 이것은 정확히 **VGCF 83 S/cm 사고와 같은 구조**다 — 조건 없는 값이 앵커가 되어 있다.
차이는 여기선 **출처가 우리 안에 있다**는 것뿐이라 **물어보면 닫힌다**.

---

## 1. 한 줄 요약

**액체 카보네이트 전해질 Li-metal 전지**에서, CNT 표면에 **PAMPS**(poly(2-acrylamido-2-methylpropane
sulfonic acid))를 자유라디칼 그래프팅해 ① CNT 응집을 풀고 ② 술폰산기로 Li⁺ 수송을 보태고
③ 고전압에서 술폰산이 산화 분해되며 나온 **HSO₃⁻ 가 전해질을 타고 애노드로 건너가(crosstalk)**
Li₂SO₃/Li₂SO₄-rich SEI 를 만들어 **양쪽 계면을 동시에 안정화** — 58.4 mg cm⁻²(11.7 mAh cm⁻²)
전극 캐스팅과 **453.2 Wh kg⁻¹ 파우치셀**까지 간다.
**우리에겐 소재계가 다르다 (황화물 ASSB 아님 · 액체 LIB)** — 값의 자리는 **[36] 인용의 provenance
확정**과 **술폰산-고분자 이온전도 필름 앵커 한 점**, 그리고 **4-point probe vs 2-전극 DC 라는
측정 규약 대비**다.

---

## 2. 메타

| 항목 | 값 |
|---|---|
| 저자 | Jaeho Jung, Sungho Kim, Youngbi Kim, Seoha Nam, Yeongseok Kim, Jeongyun Bae, **Jeong Woo Han\***, **Soojin Park\*** (J.J·S.K·Y.K 동등기여) |
| 소속 | POSTECH 화학과 / POSTECH 화공 / **서울대 재료공학부 (Han 그룹 = 계산)** |
| 저널 | **Adv. Mater. 2026, 38, e16395** (Received 2025-08-22 · Revised 2025-11-10 · **Published online 2025-11-27**) |
| DOI | 10.1002/adma.202516395 |
| 소재계 | **NCM811 (POSCO Chemical) + 액체 카보네이트 전해질 + Li 금속 (40 µm, Honjo)** — ⚠ **황화물 SE 없음** |
| 도전제 | CNT (Jaewon Industrial) — B-CNT / PAM-CNT / **PAMPS-CNT** |
| 바인더 | **PVDF (KUREHA KF1100, Mₙ 168.8 kg/mol, PDI 2.94)** — ⚠ **PTFE 아님, SDCP 아님** |
| 연구유형 | 실험 주도 (합성·전기화학·표면분석) + **DFT(VASP/Gaussian16) + MD(LAMMPS/Matlantis/AIMD)** |
| 자금 | NRF (MSIT) RS-2025-06132971, NRF-2021R1A2C3004019 |
| Data availability | "available from the corresponding author upon reasonable request" (원자료 공개 없음) |

---

## 3. 핵심 수치 — 전수 (stated / digitized 구분)

### 3.1 그래프팅·구조 (전부 stated)

| 물성 | 값 | 조건 | 출처 |
|---|---|---|---|
| 그래프팅 함량 (TGA) | PAM-CNT **3.61 wt%** · PAMPS-CNT **3.98 wt%** | RT→500 °C, 10 °C/min | 본문+Fig S1a, stated |
| Raman D/G | D ≈**1350** · G ≈**1590** cm⁻¹ (전 시료 보존) | 532 nm | stated |
| PAM 특성 피크 | **846, 1142, 1287, 1433** cm⁻¹ | | stated |
| PAMPS 특성 피크 | **770, 1038** cm⁻¹ (술폰산기 진동) | | stated |
| I_D/I_G | B-CNT < PAM-CNT, PAMPS-CNT (결함 증가) | | Fig S1b, 정성 |
| XPS S 2p | **169.0 eV** = SO₃H | PAMPS-CNT | stated |
| XPS N 1s | **399.8 eV** (–NH₂) · **401.8 eV** (C–N) | PAM-CNT | stated |

### 3.2 ★★ 전도도 — 우리 관심축

| 시료 | σ | 방법 | 조건 기재 상태 | stated/digitized |
|---|---|---|---|---|
| **PAMPS 자립필름** | **6.05 × 10⁻⁴ S/cm** (=0.605 mS/cm) | SS \| 필름 \| SS 샌드위치 + **전해질 주입** 후 EIS | ⚠ **두께·면적·온도·압력 전부 미기재** (σ=L/RA 인데 L·A 없음) | **stated (본문)** |
| PAM 자립필름 | ≈ **3.0 × 10⁻⁴ S/cm** ("PAMPS 가 약 2배") | 동일 | 동일 | 본문은 "≈2배"만 stated · **막대값은 Fig S4b digitized (TREND)** |
| B-CNT | ≈ **8.5 ± 1.0 S/cm** | **4-point probe** (CMT-100S) | ⚠ **시편 정체 모호** (아래 ⚠ 참조) | **Fig S5 digitized (TREND)** |
| PAM-CNT | ≈ **3.0 ± 0.35 S/cm** | 동일 | 동일 | digitized |
| PAMPS-CNT | ≈ **8.45 ± 0.7 S/cm** (= B-CNT 와 동급) | 동일 | 동일 | digitized |

⚠⚠ **Fig S5 시편이 무엇인지 논문 안에서 엇갈린다** — SI Methods 는
"The electrical conductivities of **each electrode** were measured using the four-point probe technique",
Fig S5 캡션은 "Electronic conductivity results of **CNTs**".  본문은
"PAMPS-CNTs maintained electronic conductivity levels comparable to those of B-CNTs, a result of their
highly dispersed and uniform **electrode structure**" — 전극 쪽 읽기를 시사하나 확정 불가.
⇒ **8.5 S/cm 을 "CNT 분말 σ" 로도 "전극 σ" 로도 단정하지 말 것.**  둘 다 함의가 다르다 (§7.4).

### 3.3 분산·형태 (3D 레이저 현미경, 270 × 210 µm 영역)

| 전극 | z-범위 (표면 요철) | stated/digitized |
|---|---|---|
| B-CNT | **±21 µm** | Fig 2d 축 라벨 (figure-stated) |
| PAM-CNT | **±16 µm** | Fig 2e |
| **PAMPS-CNT** | **±14 µm** (가장 균일) | Fig 2f |

- SEM/TEM(Fig S6·S7): B-CNT **심한 응집** vs PAMPS-CNT **균일·비엉킴**.
- 분산 안정성(Fig S8, DI water & NMP, bath sonication): PAMPS-CNT > PAM-CNT > B-CNT;
  B-CNT 는 점진적 상분리, **PAMPS-CNT 는 1개월 후에도 균일**.
- 기전(본문): PAMPS 의 –HSO₃ 가 NMP 극성 도메인과 강하게 상호작용 + AMPS 의 메틸기가 CNT 와
  소수성 상호작용 → NMP 친화도 ↑.

### 3.4 계면 (50 사이클 @0.5 C, 4.5 V 상한 후 회수)

| 관측 | B-CNT | PAMPS-CNT | 방법 |
|---|---|---|---|
| **NCM 표면 rock-salt 층 두께** | **≈15.5 nm** | **≈2.78 nm** (5.6배 얇음) | FIB-TEM + FFT, stated |
| 캐소드 XPS S 2p | 없음 | **SO₃²⁻(167.2) · SO₄²⁻(169.2 eV)** 검출 | stated (Table S1 귀속표) |
| 캐소드 P 2p | LiₓPOF_y·LiₓPF_yO_z 우세 | **LiₓPF_y 증가 = LiPF₆ 분해 억제** | stated |
| ToF-SIMS 캐소드 | PO₂⁻ 강함 | **SO₃⁻ 검출 · PO₂⁻ 억제** | Fig 3b/S15 |
| 애노드 XPS S 2p | 없음 | **SO₄²⁻ · SO₃²⁻ · Li₂S(160.4 eV)** | stated (Table S2) |
| 애노드 F 1s | | **LiF(684.7 eV) 크게 증가** = salt-derived SEI | stated |
| 애노드 ToF-SIMS | 유기종 많음 | **LiF⁻ 높고 SO₃⁻ 공존, 유기 감소** | Fig 3f/S20 |
| 애노드 SEM 표면 | **다공성(dendritic)** | **치밀(compact)** | Fig 3g/h |
| ¹⁹F NMR (회수 전해액) | HF 많음 | **PF₆⁻ 잔량 ↑ · HF ↓** | Fig S18 |

### 3.5 crosstalk 정량 (EA · CIC, 캐소드 내 S 추적)

| 사이클 | EA 황 함량 감소 | CIC SO₄²⁻ 감소 |
|---|---|---|
| 30 | **≈50 %** | **56 %** |
| 50 | **60 %** | **62 %** |

⇒ 술폰산 부분이 **전기화학적으로 소모되어 캐소드를 떠난다** = crosstalk 의 직접 물질수지 증거.

### 3.6 계산 (DFT / MD, 전부 stated)

| 양 | 값 | 방법 |
|---|---|---|
| LiOH + PAMPS 산화 → **HSO₃⁻ 생성 활성화장벽** | **0.48 eV** | Gaussian16 B3LYP/6-311G(d,p), TS = 허수진동 1개 |
| HSO₃⁻ **흡착E on Li(100)** | **−4.85 eV** | VASP PBE-D3 |
| PF₆⁻ 흡착E on Li(100) | **−7.17 eV** | 동일 |
| **H₂ 발생 장벽** (LiOH + HSO₃⁻) | **6.75 eV** (= 사실상 불가) | ⇒ Li₂SO₃ + LiOH 경로가 우선 |
| LUMO | HSO₃⁻ ≈ PF₆⁻ 수준 (유기용매는 훨씬 낮음) | Fig 4d/S25 |
| 확산계수 (MD) | HSO₃⁻ < Li⁺, PF₆⁻ 이나 "분리막 통과에 충분" | Fig 4c (수치는 그림) |
| AIMD/Matlantis | HSO₃⁻ 가 Li(100) 위에서 **20 fs · 80 fs 만에 SO₂ + OH⁻ 로 절단** | Fig S27/S28 |

### 3.7 전기화학 성능 (전부 stated)

| 조건 | 결과 |
|---|---|
| 형성 (0.05 C, 2.8–4.3 V) | PAMPS-CNT 과전압 최소 (Fig 2g) |
| **3 mAh cm⁻², 1 C, 4.3 V cut, Li 40 µm** | **PAMPS-CNT: 220 사이클에 70 % 유지** (B-CNT 저용량 · PAM-CNT 급락) |
| **4.5 mAh cm⁻², 0.3 C, 4.5 V cut** | B-CNT **60.8 % @ ~140 cyc** · **PAMPS-CNT 69.5 % @ 210 cyc** |
| **6.0 mAh cm⁻², S-free 전해질** (LiDFOB:DME:TTE = **1:2.2:3 몰비**), 0.2 C/0.3 C, 4.5 V | 두 셀 모두 **150 사이클 70 %**; 4.5 V 운전은 PAMPS 가 **100 사이클 안정**, B-CNT 는 **90 사이클 전에 70 % 미만** |
| 로딩 상한 | **B-CNT: 30 mg cm⁻²(6.0 mAh cm⁻²) 초과 시 심각한 크랙 → 셀 실패** (Fig S35) · **PAMPS-CNT: 58.4 mg cm⁻²(11.7 mAh cm⁻²) 균일 캐스팅** (Fig S36) |
| LSV | PAMPS-CNT **5.0 V 초과까지 안정** (B/PAM 보다 우수); 고분자-코팅 Al 은 PAMPS 쪽이 **약간** 더 산화 안정 |
| CA @4.9 V | PAMPS-CNT **정상상태 전류 최저** |
| **파우치 (bi-stack, 355 mAh)** | 8.5 mAh cm⁻² 캐소드 + 40 µm Li, **N/P 0.94**, **453.2 Wh kg_cell⁻¹**, **70 % @ 70 사이클**, 전압프로파일 50 사이클 안정 |
| 파우치 #2 | 6.0 mAh cm⁻², **N/P 1.33**, 0.2 C·4.5 V → **84.7 % @ 100 사이클** |
| 3전극 애노드 과전압 | PAMPS-CNT 가 **≈50 mV 낮음** (본문 stated; ⚠ Fig 5c/d 주석은 −0.186 → −0.132 **"mV"** 로 적혀 있어 단위 표기가 본문과 어긋난다 — Δ=0.054 이므로 **V 가 맞는 것으로 보인다**) |

### 3.8 Table S3 — 파우치셀 에너지밀도 산정 (전수 전사)

| 부품 | 파라미터 | 값 |
|---|---|---|
| NCM811 캐소드 | 면적용량 (편면) | **8.5 mAh cm⁻²** |
| | 방전 비용량 | **200 mAh g⁻¹** |
| | 전압창 | **2.8–4.5 V** |
| Al foil | 두께 | **20 µm** |
| Li 금속 애노드 | 두께 | **40 µm** |
| | 면적용량 (편면) | **8.0 mAh cm⁻²** |
| | **N/P** | **0.94** |
| 전해질 | **E/C** | **2 g Ah⁻¹** (희박) |
| | 무게 | **0.71 g** |
| 분리막 | 총 두께 | **20 µm** |
| 실링 | Al 파우치 무게 | **0.53 g** |
| 셀 | 시험 온도 | **25 °C** |
| | 평균 방전전압 | **~3.77 V** |
| | 방전용량 | **355 mAh** |
| | 총 무게 | **2.95 g** |
| | **비에너지** | **453.2 Wh kg⁻¹** |

### 3.9 Table S4 — 문헌 파우치셀 대비 (전수 전사)

| | Wh kg⁻¹ | Ah | 수명 | E/C (g/Ah) | 캐소드 / 로딩 (mg cm⁻²) | 면적용량 (mAh cm⁻²) | N/P |
|---|---|---|---|---|---|---|---|
| **This work** | **453** | 0.355 | **70** | **2** | NCM811 / **42.5** | **8.5** | **0.94** |
| R56 (Angew 2022) | 300 | 1.1 | 200 | 2.73 | NCM622 / 11.1 | 2.0 | 2.5 |
| R57 (Nat. Energy 2019) | 300 | 1.0 | 200 | 3.0 | NCM622 / 21.4 | 3.8 | 2.6 |
| R58 (Nat. Commun. 2022) | 325 | 2.51 | 200 | 2.7 | NCM811 / 20 | 3.8 | 2.6 |
| R59 (ACS EL 2022) | 340 | 1.8 | 200 | 3.0 | NCM811 / 17.7 | 3.5 | 2.0 |
| R60 (Nano Energy 2022) | 350 | 3.0 | 100 | 2.5 | NCM811 / 27.9 | 6.5 | 1.7 |
| R61 (JMCA 2021) | 356 | 2.62 | 100 | 3.0 | NCM811 / 20.0 | 3.8 | 2.1 |
| R62 (Angew 2021) | 357 | 2.5 | 50 | 3.0 | NCM811 / 11.14 | 5.1 | 2.0 |

⇒ **면적용량·N/P 로 이긴 대신 수명(70 cyc)·용량(0.355 Ah)은 비교군에서 가장 작다** — 정직하게 읽을 것.

---

## 4. 방법 ★ (전 조건, 본문 + SI Supplementary Methods 전수)

### 4.1 재료·합성
- 단량체: **AM** (acrylamide) · **AMPS** (2-acrylamido-2-methyl-1-propanesulfonic acid), Sigma-Aldrich.
- 개시제: **APS(ammonium persulfate) 98 %**, 0.05 g / 40 mL H₂O.
- 그래프팅: CNT 를 **DMF:H₂O = 10:90 v/v, 총 100 mL** 에 tip sonication 분산 → N₂-퍼지 3구 플라스크 →
  APS 용액 + **단량체 5 g / 20 mL H₂O** 투입 → **60 °C 교반**, **AM 24 h · AMPS 3 h** →
  **셀룰로오스 아세테이트 0.8 µm** 여과 → **진공 70 °C, 8 h** 건조.
- ⚠ **AMPS 만 반응시간이 8배 짧다**(3 h vs 24 h) — 두 그래프트의 사슬길이/밀도가 같다고 볼 근거 없음.
  그런데 TGA 함량은 3.61 vs 3.98 wt% 로 비슷 ⇒ **사슬 길이·분자량은 미측정 자유도**.

### 4.2 전극·셀
- 캐소드: **NCM811 : PVDF : (B/PAM/PAMPS)-CNT = 94 : 3 : 3 wt**, NMP 슬러리, Al 박 캐스팅,
  **진공 120 °C, 8 h** 건조.  코인셀 로딩 **15.0–58.4 mg cm⁻²**, 파우치 전극 **42.5 mg cm⁻²**
  (SI Methods 는 전극 크기를 "20 cm²", Table S3/Fig S38 계는 두면 캐소드 **21 cm²** — 소소한 불일치).
- ⚠ **캘린더링/압연 압력·전극 두께·기공률 전부 미기재.**
- 코인셀: **CR2032 (Welcos)**, 전해질 **40 µL**, 분리막 **PP Celgard 2400**, Li 금속 대극, Ar 글로브박스.
- 전해질(주): **1.3 M LiPF₆ in EC:DEC = 3:7 v/v + 10 wt% FEC** (Soulbrain).
- 전해질(S-free 고급): **LiDFOB : DME : TTE = 1 : 2.2 : 3 몰비**.
- 3전극: WE = NCM 캐소드, CE = **40 µm Li foil**, RE = **링형 Li**.
- 파우치: **bi-stack**, 두면 캐소드(21 cm², 8.5 mAh cm⁻²) + 애노드(26 cm²), 2.8–4.5 V,
  형성 0.05 C → 이후 0.1 C.
- ⚠ **스택 압력(외부 가압) 규약 없음** — 액체계 코인/파우치라 우리 ASSB 의 운전압 축이 통째로 없다.

### 4.3 ★★ 전기화학 측정 조건 (사용자 항목 ①의 실제 답)

| 측정 | 장비 | 조건 | ⚠ 미기재 |
|---|---|---|---|
| **이온전도도 (필름)** | BioLogic **SP-300** | EIS **1 MHz → 100 mHz**; SS \| 자립필름 \| SS + 전해질 주입 | **AC 진폭 · 온도 · 압력 · 필름 두께 · 면적 전부 미기재** |
| **전자전도도** | **CMT-100S** (Advanced Instrument Technology) | **4-point probe** | 시편 정체(전극 vs CNT) · 두께 · 온도 미기재 |
| 전극-수준 이온수송 | 2032 코인셀 + **PEEK 와셔** | EIS → DRT.  와셔로 전극 치수를 한정해 **분리막 기여를 제외** (Fig 2c/S3) | 정량 R_ion 값 없음 (DRT 형태만) |
| LSV | SP-300 | **1 mV s⁻¹, 3.0 → 5.5 V**, WE = Li metal | |
| CA (chronoamperometry) | SP-300 | **8 h @ 4.5 / 4.7 / 4.9 V** | |
| **GITT** | SP-300 | **0.5 C, 8 min 펄스 + 24 min 휴지**, 2.8–4.5 V, 충·방전 양방향 | |
| **PITT** | SP-300 | **50 mV 스텝, 스텝당 3 h**, 2.8–4.5 V | |
| 사이클 | WBCS-3000 (Wonatech) | **25 °C**, 2.8–4.3 V (형성 0.05 C) 후 1 C / 0.3 C 등 | |
| DRT | **DRTtools** (Ciucci 그룹, MATLAB) | Z(ω) → γ(τ), R∞ 옴 성분 분리 | 정규화 파라미터 λ 미기재 |

**내부저항 식 (Eq 1)**: `R(Ω) = |CCV − QOCV| / |I_applied|`
**PITT 확산계수 (Eq 2)**: `D_Li = (d ln I/dt)(4L²/π²)`, L = **전극 두께**
  ⚠ **그런데 전극 두께가 논문 어디에도 없다** ⇒ D_Li 절대값(≈(0.4–1.0)×10⁻⁷, Fig 5b, 단위 미표기)
  은 **재현 불가**.  단위조차 패널에 안 적혀 있다 (통상 cm² s⁻¹).  **절대값 인용 금지, 순서만.**

### 4.4 DFT
- **VASP**, **PAW**, **스핀 분극**, **PBE(GGA)** + **Grimme D3**.
- **cutoff 400 eV**, **k = 5×5×1 Monkhorst-Pack**, SCF **2×10⁻⁴ eV**, 힘 **0.03 eV/Å** (conjugate gradient).
- 분자 경로: **Gaussian16, B3LYP/6-311G(d,p)**, TS 는 **허수진동 1개**로 확인.
- 슬랩: **Li(100)** (흡착E 계산).  ⚠ **슬랩 두께·진공·dipole 보정 미기재** (우리 원고 DFT 절과 대비:
  우리는 LiNiO₂(104) 1×4 4층 192원자 + 15 Å 진공 + dipole 보정을 명시).

### 4.5 MD
- **LAMMPS**, **Δt = 0.5 fs**, **NVT + Nosé-Hoover**, **2.5 ns**, 상온, **PPPM**, 주기경계.
- 조성 **LiPF₆ : EC : DEC : FEC : HSO₃⁻ = 95 : 329 : 422 : 74 : 3**.
- 초기구조 **Packmol (2.5 Å 간격)**, 용매 파라미터는 **AmberTools + RESP (B3LYP/6-31G(d,p))**,
  Li 파라미터는 문헌(Tenney & Cygan).  MSD → D, 체류시간 = autocorrelation 적분.
- **Matlantis (PFP universal NNP)** + **AIMD**: NVT, **Δt = 1 fs**, 상온 — Li(100) 계면 반응 확인.

### 4.6 ★ "입자 처리" 축 — 이 논문에는 **없다**
DEM/MPM/FEM/RNM **0회**.  입자 형상·PSD·접촉망·압밀·기공률 **전부 부재**.
⇒ frame[5] 로 말하면 이 논문은 **역학 절반도 수송 절반도 안 가진다** — 그 대신
**계면 화학(DFT/MD) + 셀 전기화학**이라는 우리 두 축 **바깥** 축을 가진다.

---

## 5. Figure set ★ (본문 6 + SI 40 + Table 4 = 전수)

### 본문
| Fig | 내용 | 우리가 쓸 수 있는 것 |
|---|---|---|
| 1 | B-CNT(응집) vs PAMPS-CNT(분산) 모식 + crosstalk 개념도 | 개념도 — **인용 가치 낮음** |
| **2a** | Raman (CNT/PAM/PAMPS + 3 CNT) | PAMPS 770·1038 cm⁻¹ = 우리 SDCP Raman(PEDOT+SO₃H, 원고 Fig 2c) **분석 프로토콜 선례** |
| **2b** | XPS S 2p (169.0 SO₃H) · N 1s | 우리 SDCP 술폰산 XPS 귀속의 **문헌 대조점** |
| **2c** | **EIS-DRT, PEEK 와셔 코인셀** — γ(τ) vs τ (1e-6~1 s) | ★ **분리막을 빼고 전극만의 이온수송을 보는 셀 설계**.  τ≈0.2 s 대피크: PAM-CNT 최대 > B-CNT > PAMPS-CNT (digitized) |
| **2d–f** | 3D 레이저 현미경 270×210 µm | ★ **분산도의 정량 대리변수 = 표면 z-범위 ±21 / ±16 / ±14 µm**.  우리 SDCP 분산 주장에 **같은 계측 도입 후보** |
| 2g | 형성 사이클 전압곡선 | PAMPS 과전압 최소 |
| **2h** | **형성 후 EIS-DRT** — `R_interface`(τ 5e-5~5e-3) 와 `R_CT`(τ 5e-3~5e-1) **창을 명시적으로 라벨** | ★★ **DRT τ-창 ↔ 물리항 대응의 문헌 사례** — 우리 STEP4/EIS-DRT(v3-1) 의 τ-창 명명 규약에 직접 참고 |
| 2i / 2j | 장기 사이클 (3 mAh cm⁻² 1C 4.3V / 4.5 mAh cm⁻² 0.3C 4.5V) | 수명 수치 (§3.7) |
| 3a | 캐소드 XPS S 2p, P 2p | LiPF₆ 분해 억제 |
| 3b | **ToF-SIMS 3D 뎁스 (SO₃⁻, PO₂⁻)** | 3D 화학 맵핑 — 우리 SEM-EDS 대비 상위 기법 |
| **3c/3d** | **FIB-TEM + FFT: rock-salt 15.5 nm vs 2.78 nm** | ★ 표면상 전이 두께의 정량 — 우리 CEI/열화 서술의 **길이스케일 앵커** |
| 3e/3f | 애노드 XPS(S 2p, F 1s) · ToF-SIMS(SO₃⁻, LiF⁻) | crosstalk 도착 증거 |
| 3g/3h | 애노드 SEM 상면 (다공 vs 치밀) | 덴드라이트 억제 |
| **4a** | **EA + CIC 로 캐소드 S 소모 추적 (0/30/50 cyc)** | ★★ **첨가제가 "소모되는 반응물"임을 물질수지로 보인 드문 그림** — 우리 SDCP 안정성 주장에 필요한 대조 실험 설계 |
| 4b | DFT 반응경로 (PAMPS + LiOH → HSO₃⁻, 0.48 eV) | 장벽값 |
| 4c | MD 확산계수 (Li⁺, PF₆⁻, HSO₃⁻) | 수치는 그림만 |
| 4d | HOMO/LUMO (DEC, EC, FEC, PF₆⁻, HSO₃⁻) | LUMO 비교 |
| 4e | HSO₃⁻ + Li + LiOH → Li₂SO₃ 경로 | |
| 4f | crosstalk 기전 모식 | |
| **5a** | **GITT 내부저항 vs 전압** (충전 3.6→4.5, 방전 4.4→3.4) | ★ 우리 GITT ΔEs/ΔEt(원고) 와 **같은 계측**.  PAMPS 가 전 구간 최저; 충전 말단에서 B-CNT 가 급상승 (~165 Ω, digitized) |
| **5b** | **PITT D_Li vs 전압** | ⚠ **단위 미표기 + L 미기재 ⇒ 절대값 인용 금지**, 순서만 (PAMPS > B ≈ PAM, 4.5 V 에서 격차 최대) |
| **5c/5d** | **3전극 in-situ EIS-DRT 등고선 (τ 1e-4~1e2 s vs SOC) + 캐소드/애노드 전압 분리** | ★★ **우리가 안 가진 것**: 셀 전압을 캐소드·애노드로 **분해**하고 동시에 DRT 를 SOC 축으로 펼친다.  B-CNT 는 τ≈1 s 밴드(확산·입자간)가 강하고 PAMPS 는 없다 ⇒ **RDS 이동** |
| 6a | 고로딩 전극 제조 모식 | |
| **6b** | 로딩 37.4–58.4 mg cm⁻² 사이클 (0.1 C, 4.5 V) | ★ **초고로딩에서도 전자·이온 경로가 살아 있다는 직접 증거** |
| 6c/6d | 6.0 mAh cm⁻² S-free 전해질 장기 사이클 + 전압곡선 | |
| 6e/6f | 파우치 사이클 + 전압곡선 | |
| **6g** | 문헌 파우치셀 지형도 (>2.0 mAh cm⁻²) | = Table S4 의 그림판 |

### SI (전 40 그림 · 4 표 — 전수 확인)
S1 TGA+I_D/I_G · S2 TEM/EELS(PAMPS-CNT S 맵) · **S3 PEEK 와셔 셀 모식 + Nyquist(블로킹, 반원 없음·HF 절편 ~5–10 Ω)** ·
**S4 필름 Nyquist + σ_ion 막대 (PAM ~3.0 / PAMPS ~6.05 ×10⁻⁴ S/cm)** · **S5 4-point probe σ_e 막대** ·
S6 SEM(B vs PAMPS) · S7 TEM · S8 분산 안정성(5 min·1 개월, 물·NMP) · S9 형성 후 EIS ·
S10/S11 전압프로파일(1C·0.3C) · **S12 LSV (a: CNT/Al, b: 고분자-코팅 Al)** · S13 CA(4.5/4.7/4.9 V) ·
S14 캐소드 XPS O1s·C1s · S15 ToF-SIMS 표면정량 · S16 고배율 STEM(rock-salt/layered) ·
S17 FIB-SEM 단면(PAMPS 매끈 · B-CNT 크랙) · **S18 ¹⁹F NMR (PF₆⁻ 잔량·HF 생성비)** ·
S19 애노드 XPS P2p·C1s·O1s · S20 애노드 ToF-SIMS 정량 · S21 애노드 N1s + Li₃N/CN⁻ ·
S22 PAMPS 산화경로 2갈래 · S23 ¹H NMR (충전상태 HSO₃⁻ 검출) · **S24 MD 초기구조 + 조성표** ·
S25 분자궤도 · S26 Li(100) 흡착 기하·에너지 · S27 AIMD 분해(20/80 fs) · S28 Matlantis(전해질 유/무) ·
S29 HSO₃→LiSO₃→Li₂SO₃ 경로 · **S30 H₂ 발생 6.75 eV** · S31 SO₃→SO₄²⁻ 산화 ·
S32 GITT 프로파일 · S33 PITT 프로파일 · S34 in-situ DRT(3전극) · **S35 B-CNT 30 mg cm⁻² 크랙 사진** ·
**S36 PAMPS-CNT 5.1/7.9/11.7 mAh cm⁻² 전극 사진 + 전압곡선** · S37 6 mAh cm⁻² 전압곡선 ·
S38 파우치 모식 · S39 파우치 형성 전압곡선 · S40 6 mAh cm⁻² N/P 1.33 파우치.
표: **S1** CEI XPS 결합에너지 귀속 · **S2** SEI XPS 귀속 · **S3** 파우치 에너지밀도(§3.8) · **S4** 문헌 비교(§3.9).

⚠ **SI 에 우리가 찾던 것은 없었다** — LPSCl·황화물·펠릿·9:1·DC 분극·성형압·측정압 **전부 0건**.

---

## 6. Post-processing ★

| 기법 | 무엇을 뽑나 | 도구 | 우리 대응 |
|---|---|---|---|
| **DRT** (Z(ω) → γ(τ)) | 임피던스 스펙트럼을 **τ-도메인 피크**로 분해 → R_interface / R_CT / 확산·입자간 / Li 도금-박리를 **창으로 명명** | **DRTtools** (ciuccislab, MATLAB) | 우리 `scripts/eis_drt_ica.py` (v3-1) 와 **같은 도구 계보**.  ★ τ-창 명명이 우리보다 명시적 |
| **in-situ DRT 등고선** | γ(τ) 를 **SOC 축**으로 펼쳐 RDS 이동을 본다 | 동일 + 3전극 | ★ 우리에게 없음 — STEP4 시간전개에 얹을 수 있는 표현형 |
| **GITT** | CCV−QOCV / I → 내부저항 vs SOC | SP-300 | 우리 원고 GITT(ΔEs/ΔEt @SOC50) 와 동일 계열 |
| **PITT** | d ln I/dt · 4L²/π² → D_Li | SP-300 | ⚠ L 미기재로 절대값 불가 |
| **TGA** | 그래프팅 wt% 정량 | TGA 500 | 우리 SDCP 함량 정량에 이식 가능 |
| **EA + CIC** | 캐소드 내 S / SO₄²⁻ **절대 함량의 사이클 소모** | — | ★★ **첨가제 소모 물질수지** — 우리 SDCP "안정하다" 주장의 **반증 가능한 대조 실험** |
| **ToF-SIMS 3D depth** | Bi⁺(25 keV, 1 pA) 프로브 / Cs⁺(2 keV, 100 nA) 스퍼터, **500×500 µm** 크레이터, <5×10⁻¹⁰ torr | TOF-SIMS 5 | 화학종 3D 분포 |
| **FIB-TEM + FFT** | rock-salt/layered **상 두께 nm 단위** | Helios G5 + Spectra Ultra (double-Cs) | 표면상 전이 정량 |
| **3D 레이저 현미경** | 표면 z-요철 통계 (270×210 µm) | KEYENCE VK-X3050 | ★ 분산 균일도의 **비파괴 정량** |
| **4-point probe** | 접촉저항이 **제거된** σ_e | CMT-100S | ★★ §7.4 의 핵심 대비축 |
| MSD → D · autocorrelation → 체류시간 | MD 후처리 | LAMMPS | |

---

## 7. 우리 DEM+MPM 대비 → `comparison_vs_ours_DEM.md`

### 7.1 provenance (§0 요약 재게)
`[36]` = **선례 인용**.  D13 의 3.57/0.97/2.86 은 **우리 원고 자체 측정**.  압력·온도 **양쪽 문서 모두 미기재**.

### 7.2 사용자 5개 질문 대조표

| # | 질문 | 이 논문의 답 |
|---|---|---|
| ① | 펠릿 측정 조건 (압력·온도·두께·면적·전극재질·EIS 대역·DC 조건) | **해당 측정이 없다.**  가장 가까운 것은 *필름* σ_ion (EIS **1 MHz–100 mHz**, SS 전극, 전해질 주입) 인데 **두께·면적·온도·압력 전부 미기재**.  σ_e 는 **4-point probe** 라 DC 분극과 물리가 다르다 |
| ② | 바인더 종류·함량, 9:1 인가 | **PVDF 3 wt%** (NCM:PVDF:CNT = **94:3:3**).  **PTFE 없음 · SDCP 없음 · 9:1 없음.**  그래프팅 고분자는 CNT 위에 **3.61 / 3.98 wt%** |
| ③ | σ_e 측정이 벌크만인가, 계면 접촉저항이 섞이나 | **이 논문은 4-point probe = 접촉저항 원리적 제거**(전류·전압 프로브 분리).  ⇒ **우리 원고의 2-전극 DC 분극과는 다른 규약**.  아래 §7.4 가 이 대비를 D13/CL-38 에 연결 |
| ④ | 고면적하중 전극의 병목 | **① 1차 병목은 수송이 아니라 *가공성*** — B-CNT 는 **30 mg cm⁻² 위에서 크랙으로 셀이 죽는다**(Fig S35).  ② 가공성이 풀린 뒤의 병목은 **이온·고체확산·입자간 저항** — in-situ DRT 에서 B-CNT 의 RDS 는 **저주파(확산+입자간)** 이고 PAMPS-CNT 는 **전하이동 영역으로 이동**하면서 값도 낮다.  ③ **전자는 병목이 아니다** — σ_e(4pp)가 B-CNT ≈ PAMPS-CNT (8.5 vs 8.45) 로 **같은데** 성능은 크게 갈린다 |
| ⑤ | "Dual interfacial stability" 의 두 계면 | **캐소드 CEI (NCM811 \| 액체전해질)** 와 **애노드 SEI (Li 금속 \| 액체전해질)**.  ⇒ **집전체 계면이 아니다.**  우리 C-SUS/집전체 축은 **여기서 정량화되지 않는다**.  유일한 인접 관측은 Fig S12b (고분자-코팅 Al 의 산화 안정성이 PAMPS 쪽이 **"약간"** 우수 — 정량 없음) |

### 7.3 ★★ §7.4 로 가기 전: 값 이식 가능/불가 표

| 이 논문 값 | 우리 축 | 이식 가능? |
|---|---|---|
| PAMPS 필름 σ_ion **0.605 mS/cm** | binder-voxel σ_b (W2) | 🔶 **밴드로만**.  액체-팽윤 필름 ≠ 건식 SDCP.  **절대 이식 금지** |
| 4pp σ_e **8.5 / 3.0 / 8.45 S/cm** | σ_VGCF · 전극 σ_e | ⚠ **시편 정체 모호 → 앵커 불가**, "규약 감도"의 증거로만 |
| rock-salt **15.5 → 2.78 nm** | CEI 두께·열화 | 🔶 액체계 값 — 길이스케일 감각으로만 |
| 로딩 **58.4 mg cm⁻² / 11.7 mAh cm⁻²** | 고로딩 상한 | ❌ 액체 전해질이 기공을 채운다 — ASSB 와 물리가 다름 |
| **453.2 Wh kg⁻¹** 파우치 | 셀-레벨 | ❌ 액체 Li-metal 셀 |
| DFT/MD 수치 (0.48 eV, −4.85 eV …) | 우리 DFT | ❌ 다른 계면(Li(100)/유기전해질) |
| **측정 규약**(4pp vs 2전극 DC, DRT τ-창, PEEK 와셔, EA/CIC) | 방법론 | ✅ **여기가 이 논문의 진짜 이식 가능분** |

### 7.4 ★★★ CL-38(σ_e 440배)에 대한 이 논문의 기여 — 전제 검사

사용자 지적: *"우리 판정이 '펠릿 DC = 벌크' 라는 전제 위에 있다."*  두 갈래로 나눠 답한다.

**(a) 펠릿 σ_e (D13 의 0.30 / 0.12 / 1.53 ×10⁻⁷ S/cm) — 전제는 안전하다 (우리 산술).**
2-전극 DC 분극에서 측정 저항 = R_bulk + R_contact.  13 mm 다이(A ≈ 1.33 cm²)·두께 0.5 mm 가정 시
`R_bulk = t/(σA) = 0.05/(3×10⁻⁸ × 1.33) ≈ 1.3 MΩ`.  전극-펠릿 접촉저항은 아무리 나빠도 kΩ 급이다
⇒ **기여 < 0.1 %**.  **거의 절연인 펠릿에서는 DC = 벌크가 성립한다.**
⚠ 단 이것은 **우리가 한 자릿수 산술**이지 논문이 준 값이 아니다 (두께·면적 둘 다 미기재라
**가정 위의 계산**).  방향은 워낙 강해 결론이 뒤집힐 여지가 없다.

**(b) 복합 캐소드 σ_e (CL-38 의 440배) — 이 논문이 전제를 *흔든다*.**
CL-38 의 실험쪽 값은 **대칭셀 TLM 의 전자 레일** (R_ele 59.7 → 48.5 Ω·cm² ⇒ σ_e ≈ 1.21×10⁻⁴ S/cm,
두께 72.48 µm) 이고 우리 모델은 0.0727 S/cm 다.  여기에 **세 번째 규약**을 얹으면:

| 규약 | 값 | 계 |
|---|---|---|
| **면내 4-point probe** (Jung Fig S5) | **≈8.5 S/cm** | 액체 LIB 전극, NCM811+3 wt% CNT+3 wt% PVDF (⚠ 시편 정체 모호) |
| **우리 복셀 FV** (vox 0.15, 8팔) | **0.0727 S/cm** | 건식 ASSB, VGCF 3 wt% + LPSCl 27 wt% |
| **관통면 대칭셀 TLM** (우리 원고 Fig 4c) | **1.21×10⁻⁴ S/cm** | 건식 ASSB 동일 전극 |

★ **세 값이 5 자릿수에 걸쳐 있고, 순서가 "면내 > 시뮬 > 관통면" 이다.**
⇒ **"440배 과대" 라는 말은 '어느 규약 대비' 를 안 적으면 뜻이 없다.**  TLM 쪽에서 보면 우리가
600배 크고, 4pp 쪽에서 보면 우리가 **117배 작다.**
⚠⚠ **그렇다고 CL-38 이 뒤집히지는 않는다** — Jung 전극은 **LPSCl 이 0 %** 고 **탄소가 CNT** 이며
**측정 방향이 면내**다.  세 축이 동시에 달라 **정량 반증이 아니다**.  이 논문이 주는 것은
**"σ_e 절대값은 규약(면내/관통면·2전극/4탐침·시편)이 자릿수를 정한다"** 는 **경고**이고,
그 경고는 CL-38 의 서술에 **'규약을 명시하라'** 는 요구를 추가한다.
⇒ 제안: CL-38 문장을 **"우리 σ_e 는 *동일 전극의 관통면 TLM 대비* ~440배 크다"** 로
규약을 붙여 고정하고, 면내 4pp 축은 **미측정 항목**으로 열어 둔다 (우리 원고에는 SSRM 저항맵은
있으나 4pp 없음).

### 7.5 binder-필름 σ_ion 클래스 — **"~0.1 mS/cm 수렴" 이 깨진다**

`comparison_vs_ours_DEM.md` §B 는 "전도-binder 클래스 ~0.1 mS/cm 가 독립 2편에서 수렴"
(Kang(J) PC_PTFE **0.131** · Han ICEP-8 **0.135** mS/cm) 이라고 적고 있다.
**이 논문이 세 번째 점을 준다 — 그리고 수렴하지 않는다.**

| 문헌 | 필름 | σ_ion (mS/cm) | 측정계 |
|---|---|---|---|
| Kang(J) 2025 | PTFE | **0.00488** | SS \| 필름 \| **액체전해질** \| SS |
| Kang(J) 2025 | PAA_PTFE / PC_PTFE / CMC_PTFE / PVdF_PTFE | 0.127 / **0.131** / 0.178 / **0.255** | 동일 |
| Han 2025 | ICEP-8 (PVDF 0.065) | **0.135** | SS \| 필름 \| SS (팽윤 추정) |
| **Jung 2026 (이 논문)** | **PAM** | **≈0.30** (digitized) | SS \| 자립필름 \| SS **+ 전해질 주입** |
| **Jung 2026 (이 논문)** | **PAMPS** | **0.605** (stated) | 동일 |

⇒ **클래스는 0.005 (PTFE) → 0.13–0.26 (극성 바인더) → 0.30–0.61 (술폰산 관능)** 로
**두 자릿수 이상 퍼진다**.  "~0.1 mS/cm 하나로 대표" 는 **철회 대상**이고, 맞는 서술은
**"PTFE 만 유독 2–3자릿수 낮고, 그 위는 관능기에 따라 0.13→0.61 로 계속 올라간다"** 이다.
★ 방향이 물리적으로 정합 — **–SO₃⁻ 고정음이온이 Li⁺ transference 를 높이는 것**은
self-doping 과 같은 화학이다(우리 SDCP 의 설계 논거 자체).

### 7.6 ⚠ 눈에 띄는 수치 일치 — **검증으로 쓰지 말 것**

| | 값 |
|---|---|
| 우리 D13 역산 **σ_ion(SDCP)\*** | **0.62 × 10⁻³ S/cm** (= 0.62 mS/cm) |
| 이 논문 **PAMPS 필름 σ_ion** | **0.605 × 10⁻³ S/cm** |

**2.5 % 차.**  그러나 **우연 등급**으로만 기록한다 — 셋이 동시에 다르다:
① **재료**: PAMPS(비공액 폴리전해질, CNT 그래프트) ≠ SDCP(자가도핑 **PEDOT** 백본 + ether-링크
   메틸분지 술폰산 side chain, `docs/sdcp_master.md` §1.1).
② **측정계**: **액체전해질 팽윤 필름**(Li⁺ 가 용매화되어 자유롭게 흐름) ≠ **건식 ASSB 펠릿**.
③ **양의 정체**: 우리 0.62 는 **측정값이 아니라 RVE 브래킷 보간 역산값**이고 그 문서 자신이
   *"RVE-규약 의존값 — 상수로 이식 금지"* 라고 못박았다 (MG 점추정 0.066e-3 의 **9.4배**).
⇒ **"문헌이 우리 0.62 를 지지한다" 는 문장은 쓰면 안 된다.**  쓸 수 있는 것은
*"술폰산 관능 고분자의 이온전도는 10⁻⁴–10⁻³ S/cm 대역에 있고, 우리 역산값이 그 대역 안에 든다"*
= **자릿수 정합(Tier 1)** 뿐이다.

### 7.7 PTFE 이온 차단 잔차 −26.1 % 에 대해

D13 STAGE 1.5 는 표적 F = 0.97/3.57 = 0.27171 이 **vox 0.12 격자에서 도달 불가**여서
block\* = 0.17 µm (F 0.2008) 를 골랐고 **−26.1 % 잔차**를 남겼다.
**이 논문은 그 잔차를 설명하지 못한다** — PTFE 를 안 쓰고 펠릿도 없다.
다만 **간접적 방향 정보**는 있다: Kang(J) 2025 가 PTFE 필름 σ_ion 을 **4.88×10⁻⁶ S/cm**
(다른 바인더의 1/30–1/50) 로 재었고, 이 논문의 PAMPS 0.605 mS/cm 과 함께 보면
**"PTFE 는 완전 절연이 아니라 매우 낮은 이온전도상"** 이다.  우리 v1 표현은 PTFE 셀을
**완전 차단(sid 9)** 으로 찍는다 ⇒ **표현이 실물보다 강하게 막는다** ⇒ 예측 F 가
**실측보다 작게** 나오는 방향과 **부호가 맞는다**(예측 0.2008 < 실측 0.2717).
★ ⇒ **잔차의 일부는 "PTFE = 완전 절연" 규약 자체일 수 있다** — 유한 σ_PTFE(≈5×10⁻⁶ S/cm)
훅을 넣어보는 것이 **사전등록 가능한 다음 팔**이다 (⚠ 지금은 가설이지 측정 아님;
격자 양자화 축과 **교락**되므로 한 번에 하나만 바꿀 것).

---

## 8. 적용 인사이트 (우리 연구에 어떻게)

1. **★★ [36] 인용 문장을 고쳐 쓸 근거를 확보했다.**  현재 위치(자기 측정 문장 끝)는 애매해
   심사자가 "이 값이 [36] 것인가?" 로 읽을 수 있다.  → **"…, consistent with the enhanced Li⁺
   transport reported for sulfonate-functionalized polymer/carbon frameworks.[36]"** 처럼
   **선례임이 문장에서 드러나게** 분리하는 것이 안전하다.
2. **★★ D13 앵커에 '조건 미기록' 라벨을 붙이고 협력자에게 5개를 묻는다**: 성형압 · 측정 시
   인가압 · 온도 · 펠릿 두께/면적 · 블로킹 전극 재질.  ⇒ 답이 오면 D13 규약이 **한 번에 닫힌다**.
3. **★★ CL-38 서술에 규약을 못박는다** (§7.4).  "440배" 앞에 **"관통면 대칭셀 TLM 대비"** 를
   붙이고, 면내 4pp 축이 **미측정**임을 F 목록에 올린다.
4. **★ binder σ_ion 클래스 서술을 갱신한다** (§7.5) — "~0.1 mS/cm 수렴" 철회, 관능기 의존 밴드로.
5. **★ 분산 균일도의 비파괴 정량 = 3D 레이저 현미경 z-범위** (±21/±16/±14 µm over 270×210 µm).
   우리 SDCP 분산 주장은 지금 SEM/EDS 정성인데, 이 계측은 **한 숫자로 비교** 가능하고 장비 문턱이 낮다.
6. **★ 첨가제 소모 물질수지(EA + CIC)** — SDCP 가 사이클 중 **소모되는가**는 우리가 한 번도
   안 물은 질문이다.  이 논문은 술폰산이 **30 사이클에 절반** 사라진다고 보였다.  SDCP 는
   PEDOT 공액 백본이라 상황이 다르겠지만, **"안 변한다"는 가정을 재는 실험이 존재한다**는 것이 핵심.
7. **★ in-situ 3전극 DRT 등고선(τ × SOC)** — 우리 STEP4 v2 시간전개가 낼 수 있는 표현형인데
   지금은 안 낸다.  RDS 가 SOC 에 따라 어느 τ-창으로 이동하는지가 **모델↔실험을 τ 축에서
   직접 맞대는** 자리다 (frame[4] 교차검증의 새 접점).
8. 🔶 **PTFE 유한 σ_ion 훅** (§7.7) — D13 −26.1 % 잔차의 후보 채널.  ⚠ 격자 양자화와 교락되므로
   **사전등록 후** 단일 축으로만.

---

## 9. 인용 가능 문장 (deck/paper 용)

- "Sulfonate-functionalized polymers are not ionic blockers: a free-standing PAMPS film reaches
  **6.05 × 10⁻⁴ S cm⁻¹**, about twice the non-sulfonated PAM analogue (Jung et al., *Adv. Mater.*
  2026, 38, e16395)." — ⚠ 반드시 **"electrolyte-soaked film"** 을 함께 적을 것.
- "Polymer grafting removed the CNT-aggregation limit on areal loading: bare CNT electrodes crack
  above **30 mg cm⁻² (6.0 mAh cm⁻²)**, whereas PAMPS-grafted CNT electrodes cast uniformly at
  **58.4 mg cm⁻² (11.7 mAh cm⁻²)**."
- "With the electronic conductivity held essentially constant (4-point probe **8.5 vs 8.45 S cm⁻¹**),
  the improvement came from dispersion, ionic transport and interfacial chemistry — evidence that in
  CNT-containing thick electrodes the electronic rail is not the bottleneck."
- "Electrode-level electronic conductivities differ by orders of magnitude depending on the measurement
  convention (in-plane 4-point probe vs through-plane symmetric-cell TLM); absolute σ_e comparisons
  must state the convention." — ★ **우리 §7.4 논지, 이 논문은 in-plane 쪽 예시**.
- ⛔ **쓰면 안 되는 문장**: "Jung et al. measured LPSCl–binder pellet conductivities of 3.57/0.97/2.86
  mS cm⁻¹" — **이 논문에 그런 측정이 없다.**

---

## 10. 주의 / 한계 (over-claim 방지)

1. ⚠⚠ **소재계가 우리와 다르다** — **액체 카보네이트 전해질 Li-metal 셀**.  황화물 SE 0회, 건식공정
   0회, 스택압 0회, 기공률 0회, PTFE 0회.  **압밀·수송 절대축 비교 불가.**
2. ⚠⚠ **`[36]` 은 수치 출처가 아니다** (§0).  D13 의 3.57/0.97/2.86 은 **우리 원고 자체 측정**.
3. ⚠⚠ **필름 σ_ion 의 기하가 없다** — 두께·면적 미기재인데 σ = L/(R·A) 다.  **6.05×10⁻⁴ 는
   저자 산출값을 그대로 받는 것**이고 우리가 재현/검산할 수 없다.  **압력·온도도 미기재.**
4. ⚠⚠ **Fig S5 시편 정체 모호** (SI Methods "each electrode" vs 캡션 "CNTs").  8.5 S/cm 을
   **CNT 분말 앵커로도 전극 앵커로도 쓰지 말 것** — 이것이 정확히 **VGCF 83 S/cm 사고와 같은 유형**이다.
5. ⚠ **PITT D_Li 절대값 사용 금지** — Eq (2) 의 L(전극 두께)이 논문 어디에도 없고 Fig 5b 패널에
   **단위조차 없다**.  순서(PAMPS > B ≈ PAM)만.
6. ⚠ **Fig 5c/d 단위 표기 불일치** — 본문 "reduced by 50 mV" vs 주석 "−0.186 mV / −0.132 mV"
   (Δ = 0.054).  **V 가 맞는 것으로 보이나 논문이 스스로 어긋난다** ⇒ 이 값 인용 시 반드시 표기.
7. ⚠ **전극 크기 불일치** — SI Methods "20 cm²" vs Table S3/Fig S38 계 "21 cm²".  경미하나 기록.
8. ⚠ **AMPS 3 h vs AM 24 h** — 두 그래프트의 사슬길이/분자량 미측정.  "PAM 대비 PAMPS 우수" 의
   일부가 **고분자 사슬 자체의 차이**일 수 있다 (관능기만의 효과로 단정 금지).
9. ⚠ **수명은 비교군 중 가장 짧다** (파우치 **70 사이클**; Table S4 비교군 50–200).
   453 Wh/kg 헤드라인만 인용하면 불균형.
10. ⚠ **디지타이즈 값**(PAM 필름 0.30 mS/cm · 4pp 8.5/3.0/8.45 S/cm · DRT 피크 높이 · GITT 저항값)은
    **TREND only**.  false precision 금지.
11. ⚠ **frame[5] 위치**: 이 논문은 **DEM 절반도 MPM 절반도 갖지 않는다** — 입자·접촉망·형상소성·
    기공률 전부 없음.  우리 두 축 **바깥**(계면화학 + 셀 전기화학)에 있으므로,
    frame[4] 의 "독립 측정" 상대가 **아니다**.  방법론·선례 인용으로만 쓴다.
12. ⚠ **§7.4 의 산술은 우리 것**이다 (펠릿 R_bulk ≈ 1.3 MΩ 추정은 두께 0.5 mm·13 mm 다이 **가정**).
    논문이 준 값이 아니다.

---

## 11. SI 전수 훑기 — 우리가 찾던 것의 부재 확인 (negative result 기록)

`docx` 를 XML 로 풀어 **본문·표·그림 캡션·참고문헌 전부** 를 훑은 결과:

| 검색어 | 히트 |
|---|---|
| LPSCl / Li₆PS₅Cl / argyrodite / sulfide SE | **0** |
| pellet / die / 성형압 / MPa | **0** (셀 조립압·스택압 기재 자체가 없다) |
| ion-blocking symmetric cell | **0** (필름 EIS 는 SS \| film \| SS + 전해질) |
| DC polarization / chronoamperometry for σ_e | CA 는 **산화안정성용**(4.5/4.7/4.9 V, 8 h) — **σ_e 측정 아님** |
| 9:1 | **0** |
| 온도 (전도도 측정) | **0** — 25 °C 는 사이클/파우치 시험에만 |
| PTFE | **0** |
| 전극 두께 (µm) | **0** |
| 기공률 | **0** |

⇒ **①②③ 항목은 이 논문에서 원리적으로 답이 나오지 않는다.**  이 카드가 그 사실 자체를 정본화한다.

---

## 🗨️ Q&A 로그

### Q1 · 2026-09-03 · "D13 의 3.57/0.97/2.86 이 이 논문 값인가?"
**아니다.**  본문 13 pp + SI(Methods·40 그림·4 표) 전수 판독에서 LPSCl·펠릿·9:1·DC 분극 **전부 0건**.
우리 원고 문장이 `(Figures 2h and S8)` / `(Figures 2i and S9)` 로 **자기 그림**을 가리키고,
`[36]` 은 같은 문단의 `[34]`(Raman 귀속)·`[35]`(self-doping 원전)·`[37]`(역할분담)과 **같은 위치·같은
기능의 선례 인용**이다.  ⇒ **자체 측정 + 선례 인용.**

### Q2 · 2026-09-03 · "그럼 압력·온도는?"
**두 문서 모두 미기재.**  우리 원고 Experimental Section 은 9:1 · ion-blocking EIS · DC 0.5 V/30 min ·
7 MHz–10 mHz · 5 mV 까지만 적고 **성형압·측정압·온도·펠릿 치수를 안 적는다** (433/200 MPa 는
mold cell 조립압이라 이 펠릿과 별개).  ⇒ **원고 저자 확인 필요** — 이것이 D13 을 닫는 유일한 경로다.

### Q3 · 2026-09-03 · "DC 분극이 벌크만 재나? (CL-38 전제)"
**펠릿에서는 예** (σ_e ≈ 3×10⁻⁸ S/cm → R_bulk ≈ MΩ 급, 접촉저항 kΩ 급 ⇒ 기여 <0.1 %; ⚠ 우리 산술).
**복합 캐소드에서는 규약이 자릿수를 정한다** — 이 논문의 **면내 4-point probe ≈8.5 S/cm** 를
우리 시뮬 0.0727 · 관통면 TLM 1.21×10⁻⁴ 와 나란히 놓으면 **5 자릿수**가 벌어진다.
⇒ CL-38 의 "440배" 는 **"관통면 TLM 대비"** 라는 규약과 함께만 인용할 것 (§7.4).
⚠ 이것은 CL-38 의 **반증이 아니다** (재료·탄소종·측정방향 3축 동시 상이).

# Oh 2026 (Journal of Power Sources 689, 240698) — SiOx 탄소코팅 두께가 이온/전자 수송 BALANCE + 균일분산을 결정

**인용:** Jihwan Oh†, Seungyeop Choi†, Youyeong Shin, Sun Hyu Kim, Cheol Bak, Wonseok Yang,
Gyuna Bae, Eunji Kim, Chung-Seok Oh, Yong Min Lee\*, "Optimized Carbon Coating on SiOx
Enables Balanced Ion/Electron Transport and Uniform Dispersion in SiOx/Graphite Composite
Electrodes", *Journal of Power Sources* **689** (2026) 240698,
DOI 10.1016/j.jpowsour.2026.240698 (PII S0378-7753(26)…). MDB 2025 특별호("Progresses and
Challenges"). 접수 2026-04-04, 수정 2026-05-29, 게재확정 2026-06-10, online 2026-06-17. © 2026 Elsevier.

**소속:** Yonsei University — (a) Dept. of Battery Engineering, (b) Dept. of Chemical & Biomolecular
Engineering(Seoul 03722) + (c) ActRO Corporation New Business Development Team 1(Yongin-si 16954).
= 이용민 **Digital Twin Battery Lab (DTBL)**. †Jihwan Oh, Seungyeop Choi 동등기여. 교신
yongmin@yonsei.ac.kr. **이해상충 없음.** 지원: KIAT/MOTIE(RS-2024-00420590, HRD Program for
Industrial Innovation).

**소재계:** ★ **SiOx(0<x<2, Daejoo Electronic Materials) 음극 활물질**에 **CVD 아세틸렌(C₂H₂)
탄소코팅**(thin/moderate/thick = 목표 1/3/4 wt%, TGA 실측 **0.95/2.91/4.18 wt%**) +
**인조흑연(Shanshan Technology)** 블렌드 음극; CBD = **Super C65T(Imerys) + MWCNT(Nanografi) +
Na-CMC(Daiichi Kogyo) + SBR(BM-400B, Zeon)** 수계; full-cell 양극 = **NCM622(LiNi₀.₆Co₀.₂Mn₀.₂O₂,
L&F)**; 전해질 **1.15 M LiPF₆ EC/EMC 3:7(v/v) + 10 wt% FEC**.
★★ **우리 LPSCl sulfide ASSB가 아니다** — **SiOx/흑연 음극 + 액체전해질 일반 LIB**. 이 그룹(연세대
DTBL)의 **#284** 논문 — `docs/literature_yonsei_dtbl_2026.md` 항목 갱신본.

**한 줄 핵심 변수:** **SiOx 위 탄소코팅층(carbon coating layer, CCL) 두께** — bare / thin-C / moderate-C
/ thick-C 4종. SiOx@thin/moderate/thick-C는 코팅층(CCL)+코어(SiOx)를 합쳐 **단일 활물질 성분**으로 취급
(활물질 분율도 CCL 포함 질량 기준 계산).

DB 동반 파일: `docs/data/densification_porosity_db.csv` 등 수치 DB에는 추가하지 않음(이 논문은 흑연/액체
LIB → σ/porosity 절대앵커 아님 — Bazzoun/Varkey/Minnmann이 앵커 담당). 주요 수치는 본 MD 표에 모두 정리.
SI(`SI_284_carbon_coating.txt` = Fig S1–S11 캡션 + Table S1 OWRK 표)는 디제스트 본문에 반영. SI에
동영상/머신판독불가 자료 없음.

---

## ★ 한 문장 결론 — 이게 무엇이고 우리에게 왜 중요한가

**SiOx 위 탄소코팅 두께가 이온↔전자 수송 BALANCE를 지배한다.** **두꺼운 코팅** → 전자전도↑(연속
도전경로 형성)이지만 **Li⁺ 수송을 가로막아 전하전달저항(Rct)·분극↑**; **얇은 코팅** → 전자경로 불충분;
**중간(moderate, ~2.91 wt%)** = 이온/전자 균형 → **전극저항↓·ICE↑·rate·cycling 최우수**. 그리고
탄소코팅은 SiOx의 **표면에너지를 CBD에 더 가깝게** 바꿔 **SiOx–CBD 상호작용↑ → 활물질·CBD가 전극 안에서
더 균일하게 분산**(SSRM 저항맵 + work-of-adhesion + 유변학으로 입증).

**우리 hook(가장 중요):** 이 논문의 **"두꺼운 탄소 → 전자↑·이온↓, 중간이 균형"** 은 우리 CBD 작업의
**SuperP-vs-VGCF 이온/전자 trade-off와 정확히 같은 긴장**이다 — 우리는 **SuperP가 전자는 1.3× 더
보태지만 SE 이온망을 1.8× 더 막는다(σ_ionic 0.0168 < VGCF 0.0298)**를 voxel FV로 측정했다. Oh 2026은
**같은 trade-off를 "탄소 양/두께" 축에서** 실험으로 보이고, **"중간 최적"이라는 우리가 아직 정량화 안 한
balance point**를 실험적으로 제시한다. ⇒ **우리 CBD trade-off 그림을 풍부하게 만드는 독립 실험 증거**이지
모델 하자를 드러내는 건 아니다(아래 §7에서 "concept/method는 전이, 절대값은 비전이" 명확화). 추가로
**SSRM 분산맵 + 표면에너지/work-of-adhesion → 분산도** 측정법은 우리 additive 분산 morphology(SuperP
distributed vs VGCF concentrated)에 **분산 metric 후보**로 이식 가능.

---

## 1. 배경 / 동기 (Introduction, p.2)

- 고에너지밀도 수요 → 실리콘(Si)이 차세대 음극 후보(이론용량 Li₂₂Si₅ ~4200 mAh/g ≫ 흑연 372 mAh/g).
  그러나 **>300% 부피팽창 → 입자 분쇄(pulverization) + 불안정 SEI → 급속 용량열화**.
- 완화책: (i) Si를 **나노스케일**로 줄여 기계 strain 완화, (ii) ★ **SiOx** — Si 나노도메인이 비정질 SiO₂
  매트릭스에 3차원 분산 → 부피팽창 ~290%로 완화. 첫 리튬화 때 SiO₂가 활성상(Li₂Si₂O₅, Si) + **비활성상
  (Li₂SiO₃, Li₄SiO₄, Li₂O)**으로 전환 → 비활성상이 **기계적으로 견고한 완충 매트릭스**로 부피팽창 억제.
- ❗ **그러나 SiOx는 (a) 낮은 전기전도도 + (b) 낮은 ICE**(초기 리튬화에서 비활성상 생성에 Li 소모)로 고통.
- ★ **탄소코팅**이 표준 해법: (i) **전기전도도↑**, (ii) 전해질↔활물질 **직접접촉 차단 → 계면 안정화**
  (SEI 부반응 억제). 기존 연구는 구조설계·합성법·전구체/공정에 따른 형태 위주. **그러나 탄소코팅 "두께"가
  전기화학성능·전극미세구조를 어떻게 결정하는지는 충분히 이해 안 됨**(refs 43,44). 특히 코팅두께가
  **전자↔Li⁺ 수송 trade-off**를 결정적으로 좌우할 것으로 예상. 또 코팅이 만드는 **표면개질**이
  **활물질↔CBD 상호작용**(분산)에 영향 → 복합전극 미세구조·수송경로 변화.
- **본 연구(명시):** **CVD로 코팅두께를 정밀제어한 carbon-coated SiOx**(용액기반 기존법보다 정밀) →
  rate/cyclability로 **이온/전자 균형을 주는 최적 두께** 규명 + **SSRM으로 코팅-유도 표면개질이 활물질·CBD
  분산도에 미치는 영향** 해명. 목표 = SiOx 음극용 **탄소코팅 설계지침**.

**약어 정리:** CCL = carbon coating layer(SiOx 위 탄소층). CBD = carbon-binder domain(도전재+바인더 복합상,
여기선 Super C65T + MWCNT + Na-CMC + SBR). SSRM = scanning spreading resistance microscopy(주사확산저항
현미경 — 저항대비 분산맵). OWRK = Owens-Wendt-Rabel-Kaelble(표면에너지 분해법). DCIR = DC internal
resistance. GITT = galvanostatic intermittent titration. DRT = distribution of relaxation times. ICE =
initial Coulombic efficiency. SAICAS = surface and interfacial cutting analysis system(접착/응집강도).

---

## 2. 소재 & 제작 (Experiments, §2, p.2–3)

### 2.1 Carbon-coated SiOx 합성 (CVD, §2.1) — ★ 핵심 공정
Bare SiOx(0<x<2, Daejoo Electronic Materials) 분말 6 g을 graphite boat에 균일 적재(일정 bed height) →
CVD 반응기 중앙. **아세틸렌(C₂H₂)을 탄소원**으로, 목표 탄소함량 1/3/4 wt%에 맞춰 조건 최적화. 캐리어=고순도 N₂.

| 샘플 | 목표 C | C₂H₂ 농도 | 반응온도 | 반응시간 | 총가스유량 | 비고 |
|---|---|---|---|---|---|---|
| **SiOx@Thin-C** | 1 wt% | 3% | **800 °C** | 30 min | 600 sccm | 단일코팅 |
| **SiOx@Moderate-C** | 3 wt% | 1% | **900 °C** | 120 min | 600 sccm | 단일코팅 |
| **SiOx@Thick-C** | 4 wt% | 3% → 0.5% | **950 °C** | 1차 11 min → 2차 56 min | 4800 sccm | **2단계 코팅** |

→ thick은 **2-step**(1차 950 °C·11 min C₂H₂ 3%, 2차 동온·56 min C₂H₂ 0.5%, 유량 4800 sccm)으로 더 두껍고
조밀한 층 형성. **TGA 실측 탄소함량: thin 0.95 / moderate 2.91 / thick 4.18 wt%**(목표 1/3/4 wt% 근사).

### 2.2 전극 제작 (§2.2)
- **양극(NCM622):** NCM622 : Super P : PVDF(Solef 6020) = **96:2:2 wt%**, NMP 슬러리, planetary mixing.
  Al foil(15 µm), doctor blade, **130 °C 2 h** 건조 → gap-control roll-press(CLP-2025, CIS) **밀도 3.5 g/cm³**.
  **mass loading 17.6 mg/cm² (≈ areal capacity 3.0 mAh/cm²)**.
- **SiOx/graphite 음극:** SiOx : 인조흑연 : Super C65T : MWCNT : Na-CMC : SBR = **80:9:1:5:1.5:5 wt%**,
  DI water 수계 planetary mixing. Cu foil, doctor blade, **60 °C 2 h** 건조 → roll-press **밀도 1.5 g/cm³**.
  **mass loading 4.8 mg/cm² (≈ areal capacity 3.18 mAh/cm²)**.
  ★ **carbon-coated SiOx는 CCL+코어를 합친 질량으로 활물질 분율 계산 → SiOx@thin/moderate/thick-C를
  단일 활물질 성분으로 취급.**(SiOx 코어만이 아님.)
- **SiOx-only 음극(half-cell SiOx 평가용):** SiOx : Super C65T : MWCNT : Na-CMC : SBR = **80:9:1:5.5**…
  (본문 "80:9:1:5:5" → SiOx:C65T:MWCNT:CMC:SBR), DI water, **60 °C 2 h** 건조 → roll-press **1.5 g/cm³**,
  **mass loading 1 mg/cm² (≈ 1.2 mAh/cm²)**.

### 2.3 셀 조립 (§2.3)
- **Full-cell:** 2032 coin, SiOx/graphite‖NCM622, Ar 글러브박스(dew point < −80 °C). 양극 Ø14 / 음극 Ø16,
  **PE separator(14 µm, W-SCOPE) Ø18**, 60 °C 진공건조 12 h. 전해질 **1.15 M LiPF₆ EC/EMC 3:7(v/v) +
  10 wt% FEC**(Enchem).
- **Half-cell:** SiOx/graphite ‖ Li metal(200 µm, Honjo), PE separator. 펀칭 Ø14/16/18, 동일 전해질.
- **Single-layer pouch(48 mAh):** dry room(dew point < −60 °C). NCM622 양극 **40×40 mm²**, SiOx/graphite
  음극 **42×42 mm²**, PE separator 50×50 mm², Al pouch film(150 µm, DNP). lead-tab welding → 진공건조
  60 °C 12 h → 코인셀과 동일 전해질 주입 → 밀봉.

### 2.4 탄소코팅 특성분석 (§2.4)
- **TEM(JEM-2100F, JEOL):** CCL 형태·두께. **TGA(Discovery TGA550, TA Instruments):** 탄소함량,
  O₂ 분위기, 승온 **10 °C/min, ~600 °C까지**.

### 2.5 분산도 분석 (§2.5) — ★ 우리가 이식할 핵심 방법
- **SSRM(scanning spreading resistance microscopy):** 활물질·CBD 분포(저항대비)를 **공간맵**으로. 전극
  조성 **SiOx : Super C : MWCNT : Na-CMC : SBR = 85:4.5:0.5:5:5 wt%**, **밀도 1.5 g/cm³, mass loading
  3.92 mg/cm²(≈ 5 mAh/cm²)**. 글러브박스 내 AFM(NX10, Park Systems), **전도성 다이아 AFM 팁(DDESP-V2)**,
  **point-in-point 모드, 스캔 15 µm × 15 µm**. → 저항이 낮은(파랑) = 활물질, 높은(빨강) = CBD 영역으로
  ★ **CBD 분산 균일도를 저항맵으로 시각화·정량**.
- **유변학(rheology):** SiOx 슬러리 점도 vs **전단속도 0.01–1000 s⁻¹**(MCR 702e, Anton Paar, 25 °C).
- **표면에너지 / work-of-adhesion(OWRK):** SiOx 분말을 pellet(500 MPa·90 s)으로 압축, **CBD 필름**(Super C
  : MWCNT : Na-CMC : SBR = 85.5:9.5:2.5:2.5 wt%)도 제작. **DIW(극성)·DIM(diiodomethane, 비극성)** 접촉각
  측정 → OWRK로 **분산(dispersive)·극성(polar) 표면에너지 성분** 분리. **두 고체상 간 work-of-adhesion**:
  ```
  W_Adh = 2( √(γ₁ᵈ·γ₂ᵈ) + √(γ₁ᵖ·γ₂ᵖ) )        (식, OWRK 기반)
  ```
  (γᵈ=분산성분, γᵖ=극성성분; 1,2 = 접촉하는 두 고체상.)

### 2.6 전기화학 측정 (§2.6)
- 12 h aging(전해질 침투). **pre-cycling = formation 1사이클 + 안정화 3사이클**: formation 0.1C CC discharge
  → 0.005 V, 0.1C charge → 2.0 V; 안정화 0.2C CC/CV discharge + 0.2C CC charge(2.5–4.25 V).
- **DCIR(HPPC):** 5C 방전펄스 10 s + 40 s 휴지 + 5C 충전펄스 10 s → **10–90% SOC 10% 간격** 충·방전 DCIR.
- **GITT:** 0.1C 펄스 + 90 s 휴지. **CV:** scan rate **0.2–0.5 mV/s**(0.2/0.3/0.4/0.5), **SiOx 기여
  전압영역 0.4–0.6 V**의 peak current vs √(scan rate).
- **Rate(full-cell):** 충전전류 **0.2C → 5C(0.2/0.5/1/2/3/5/0.2C)**, 방전 0.2C CC/CV 고정.
- **Cycling:** **0.2C CC/CV 충전 + 0.5C CC 방전**(full-cell 100사이클 @0.5C).
- **EIS:** VSP-300(BioLogic), **5 MHz–50 mHz**. **bulk 전기저항 + 계면 전기저항**: RM2610(HIOKI),
  **50 mA, 5 V**. 전 측정 25 °C.

### 2.7 Post-mortem (§2.7)
- **XPS(K-Alpha, Thermo):** pre-cycling 후 SEI 조성(C 1s, F 1s). **단면 SEM(FE-SEM, JSM-7610F-Plus, JEOL):**
  사이클 전·후 미세구조; ion-beam cross-section polisher(IB-19510CP)로 평탄 단면. **SAICAS(Daipla Wintes):**
  stainless 블레이드(폭 1 mm, 절삭속도 2 µm/s)로 **응집(cohesive)·접착(adhesive) 강도**.

---

## 3. 핵심 메커니즘 — 왜 "중간 두께"가 이온/전자 균형인가 (Fig 6 개념도)

**(1) 탄소코팅 = 전자전도 향상 + 계면 보호.** SiOx 표면에 연속 도전탄소층(CCL) → **입자간 전자경로 형성**
+ 전해질 직접접촉 차단 → SEI 부반응 억제(ICE↑). 코팅↑ → 전자전도↑(연속성↑).

**(2) ❗ 그러나 두꺼운 코팅 = Li⁺ 확산 장벽.** 전해질의 Li⁺가 SiOx에 도달하려면 **먼저 CCL을 통과**해야
함 → 과도하게 두꺼운 CCL은 **Li⁺ 수송경로를 늘려 저항↑(특히 Rct, charge-transfer)** + **분극↑**. ⇒
**thick-C는 전자전도는 최고지만 Li⁺ 접근성↓ → Rct↑ → rate·분극 악화**.

**(3) thin-C = 전자경로 불충분.** 얇은 CCL은 **반복 충방전·대(大) 부피변화에서 입자간 전기접촉 유지 실패**
→ interparticle 접촉 점진 열화 → 전자전도망 단절.

**(4) ★ moderate-C = balance.** 충분히 도전적인 탄소망(전자↑)을 유지하면서도 **과도하게 두껍지 않아 Li⁺
수송 방해 최소** → **최저 임피던스·최고 rate·안정 cycling**. = "이온/전자 균형은 코팅두께의 trade-off."

**(5) 분산 메커니즘(병렬 효과).** 탄소코팅이 SiOx **표면에너지를 도전재(CBD)에 더 가깝게** 만듦 → SiOx↔CBD
상호작용↑ → 수계 슬러리에서 **도전재의 국소 소수성 응집 억제 → CBD가 더 균일하게 분산**(SSRM 저항맵에서
bare는 CBD 응집덩어리(파랑 활물질 사이 빨강 CBD가 뭉침), 코팅품은 균질). 균일 CBD = **균질 전자경로·pore
구조 → R_ion↓**(덜 우회하는 이온경로).

⇒ 우리 식으로: **"탄소는 전자를 보태지만 이온을 막는다 — 너무 적으면 전자망 부족, 너무 많으면 이온 차단,
중간이 최적"**. 이건 우리 CBD SuperP-vs-VGCF 작업(carbon ADDS σ_e but BLOCKS σ_ionic)과 **동일한 ion/
electron trade-off**를 **코팅두께 축**에서 본 것이며, **우리가 아직 정량화 안 한 "balance point" 개념**을
실험으로 제시한다.

---

## 4. 섹션별 결과 — 모든 수치 (Results & Discussion, §3, p.3–8)

### 4.1 탄소코팅 형태·함량·전기전도 (Fig 1)

**TEM 코팅두께(Fig 1a–d, Fig S1):**
- **bare SiOx:** 매끈한 표면, CCL 없음(Fig 1a).
- **SiOx@thin-C:** **두께 ~4–5 nm의 conformal CCL**이 SiOx 표면을 균일하게 덮음(Fig 1b).
- **moderate-C → thick-C:** CCL 두께 점진 증가. ★ **thick-C의 CCL은 더 조밀·치밀(denser, more compact)**
  → 코팅 구조 연속성↑(Fig 1c,d). (구체 nm 값은 본문 미기재 — TEM 정성.)

**TGA 탄소함량(Fig 1e):** ★ **thin 0.95 / moderate 2.91 / thick 4.18 wt%** — CCL 두께와 일관된 점진 증가.

**Raman(Fig S2):** bare 대비 코팅품은 **SiOx 관련 peak 약화** + 뚜렷한 **D·G band**(탄소). SiOx-related
peak 상대강도가 thin→thick으로 증가(탄소 coverage 증가와 일치). 단 **D/G band profile은 코팅품끼리 유사**
→ 코팅두께 증가에도 **CCL의 구조적 특성(흑연화도 등)은 대체로 유지**.

**Bulk 전기저항률 + 계면 전기저항(Fig 1f,g):** 모든 코팅품이 bare보다 낮음(탄소코팅 → 전기전도↑).
| 샘플 | Bulk 전기저항률 (Ω·cm) | 계면 전기저항 (mΩ·cm²) |
|---|---|---|
| **bare SiOx** | ~**0.033** (분포 0.027–0.040) | ~**1.7** (1.4–2.1) |
| **SiOx@thin-C** | ~**0.018** | ~**1.0** |
| **SiOx@moderate-C** | ~**0.013** | ~**0.6** |
| **SiOx@thick-C** | ~**0.012** | ~**0.5** |
- (값은 Fig 1f,g box-plot에서 디지타이즈 — **TREND only**, 절대정밀 아님.)
- ★ **bulk·계면 저항 모두 bare → thin → moderate로 점진 감소**, **moderate↔thick은 미미한 차이만**
  → **고(高) 탄소함량에서 전기전도 개선이 saturate**(추가 이득 한계). = "전자 쪽은 moderate에서 이미 충분."

**초기 용량-전압 + ICE(Fig 1h,i,j):** carbon-coated가 bare보다 ICE 뚜렷 개선(half·full 모두).
| 샘플 | Half-cell ICE (%) | Full-cell ICE (%) |
|---|---|---|
| **bare SiOx** | **73.6** | **58.7** |
| **SiOx@thin-C** | **80.0** | **69.1** |
| **SiOx@moderate-C** | **81.6** | **73.1** |
| **SiOx@thick-C** | **81.5** | **71.8** |
- (Fig 1j 막대 라벨.) ★ **ICE는 코팅 시 큰 폭 상승**(half 73.6→~81.6, full 58.7→~73)하지만 **moderate↔
  thick은 거의 같음**(half 81.6 vs 81.5; full 73.1 vs 71.8). → ICE 개선도 **고탄소에서 saturate**.
- ICE 개선 원인: **보호 CCL이 SiOx↔전해질 직접접촉을 줄여 과도한 계면 부반응 억제**. SiOx half-cell(Fig S3)도
  코팅 시 ICE 개선 확인.

**XPS(pre-cycled 전극, Fig S4):** 코팅품(thin/moderate/thick)에서 **Li₂CO₃·LiF signal 증가** → CCL이
SEI 화학을 변화(보호막 효과). C 1s·F 1s 분석.

### 4.2 CBD 분산도 — SSRM·표면에너지·유변학 (Fig 2)

★ 핵심 발견 2: **탄소코팅이 SiOx 표면개질 → CBD 분산 균일화.**

**SSRM 단면 저항분포(Fig 2a–d):** 저항맵 — **파랑 = SiOx & void(저저항)**, **빨강 = 도전재+탄소코팅층
(고저항? — 캡션상 "Conductive additives & Carbon coating layer")**. (주: 캡션 색범례가 본문 서술과
반대로 읽힐 수 있어 디지타이즈 주의 — 본문 해석을 따름.)
- ★ **bare SiOx:** **국소 응집된 저저항 영역**(CBD aggregation; Fig 2a에 "CBD aggregation" 표기) →
  **CBD가 뭉쳐 불균일 분포** → 이질적 전자경로·pore 구조.
- ★ **carbon-coated(thin/moderate/thick):** **CBD가 더 균질 분포**(고저항=빨강 도메인이 고르게 퍼짐) →
  분산 균일도↑. → Fig 1f,g의 **낮은 저항 편차**(균질 전자망)와 일치.

**Work of adhesion (SiOx↔CBD, OWRK; Fig 2e + Table S1):**
| 샘플 | 접촉각 DIW (°) | 접촉각 DIM (°) | γᵈ (mN/m) | γᵖ (mN/m) | γ_total (mN/m) | **W_adh with CBD (mN/m)** |
|---|---|---|---|---|---|---|
| **bare SiOx** | 43 | 38 | 40.60 | 21.60 | 61.20 | **99.9** |
| **SiOx@Thin-C** | 56 | 9 | 50.18 | 11.10 | 61.28 | **107.3** |
| **SiOx@Moderate-C** | 49 | 7 | 50.42 | 14.43 | 64.85 | **108.6** |
| **SiOx@Thick-C** | 54 | 5 | 50.61 | 11.92 | 62.53 | **107.9** |
| **CBD** (필름) | 53 | 5 | 50.6 | 0.97 | 51.57 | — |
- ★ **W_adh(SiOx↔CBD): bare 99.9 → thin 107.3 / moderate 108.6 / thick 107.9 mN/m** → 코팅 시 모두 증가
  (**moderate 최고**). = 탄소코팅이 **SiOx↔CBD 계면 상호작용 강화** → 더 양립가능한 표면.
- 물리: **bare SiOx는 극성성분 γᵖ=21.6**(친수성)인데 **CBD는 γᵖ=0.97**(거의 비극성/소수성). 탄소코팅이
  SiOx의 **γᵖ를 11–14로 낮추고 γᵈ를 50대로 올려** CBD(γᵈ 50.6)와 **분산성분이 일치** → 표면에너지가
  **도전재(CBD)에 가까워짐** → 수계 슬러리에서 **도전재 국소 소수성 응집 억제 → 균일분산**.

**유변학(Fig 2f):** 모든 슬러리 전형적 shear-thinning(전단속도↑ → 점도↓). ★ **bare SiOx 슬러리는 저전단
영역에서 높은 점도**(강한 응집덩어리 존재 → 전단으로 깨지며 점도 급강하). **coated 슬러리는 저전단 점도↓ +
점도 변화 완만**(덜 응집·더 균일 분산상태). → 탄소코팅이 분산 촉진을 재확인.

**대칭셀 EIS R_ion(Fig 2g):** ★ **coated SiOx 전극이 bare보다 낮은 이온저항(R_ion)** → **더 균질한 pore
구조 + 덜 우회하는(less tortuous) 이온경로**(개선된 CBD 분산 덕). (Nyquist Z′-Z″ plot, blocking 대칭셀.)

### 4.3 DCIR·rate·DRT — 이온/전자 균형의 전기화학 (Fig 3)

★ 핵심 발견 3: **moderate-C가 이온/전자 균형으로 최저저항·최고 rate.**

**DCIR vs SOC(HPPC, 5C 펄스 10 s; Fig 3a 충전 / Fig 3b 방전):**
- ★ **charge·discharge DCIR 모두 bare → thin → moderate로 점진 감소** → **CBD 분산 개선(thin·moderate) +
  도전 CCL 증가에 따른 전자수송 강화** 덕.
- ❗ **thick-C는 moderate보다 DCIR 높음** → 원인: **두꺼운 CCL이 Li⁺ 수송 장벽**(전해질 Li⁺가 SiOx 도달
  전 CCL 통과 → 경로 연장 → 저항↑). (Fig 3a,b에서 thick 곡선이 moderate 위.)

**Rate capability(full-cell, Fig 3c):** 충전전류 0.2/0.5/1/2/3/5/0.2C, 방전 0.2C 고정.
- ★ **SiOx@moderate-C = 전 C-rate에서 최우수, 특히 고율(최대 5C)에서 차이 큼** → **moderate 코팅두께가
  전자↔이온 최적 균형 제공**. (Fig 3c areal capacity vs cycle number; 0.2C ~2.x → 5C에서 분리.)

**GITT(Fig S6):** ★ **moderate-C가 다른 샘플보다 낮은 분극** → 코팅의 이로운 효과 재확인.

**CV scan rate(Fig S7,S8):** 0.2–0.5 mV/s. peak current vs √(scan rate)(Fig S8). ★ **coated가 bare보다
높은 기울기 → 탄소코팅 후 화학확산(chemical diffusion) 개선.** → SiOx 반응동역학 개선.

**SOC-의존 EIS + DRT(Fig 3d–g EIS, Fig 3h–k DRT):** half-cell, 10–90% SOC 20% 간격.
- ★ **bare → thin → moderate로 전 SOC 범위 임피던스 감소.**
- ❗ **thick-C는 moderate보다 높은 임피던스**(특히 Rct↑) — **두껍고 조밀한 CCL이 전자전도뿐 아니라
  Li⁺ 접근·전하교환을 포함하는 전체 계면과정을 늘려 Rct↑**.
- **DRT 분해(Fig 3h–k):** 저주파/중간/고주파 feature를 **Warburg(Z_W) / Rct / SEI(R_SEI)**로 귀속. ★
  **moderate-C가 가장 작은 Z_W·Rct·R_SEI** → **moderate 코팅이 이온/전자 균형 수송을 가능케 함**(정량
  근거).

### 4.4 Cycling·미세구조·기계강도 (Fig 4, Fig 5)

★ 핵심 발견 4: **moderate-C가 cycling 안정성·미세구조 무결성·기계강도 최우수.**

**Full-cell cycling(SiOx/graphite‖NCM622, 100사이클 @0.5C; Fig 4a 용량/CE, Fig 4b retention):**
- 초기: bare가 **낮은 ICE 때문에 초기 방전용량 상대적 낮음**(Fig 1i). 사이클 진행 → **용량유지가 bare →
  moderate로 점진 개선**.
- ★ **SiOx@moderate-C = 최고 용량유지율**(Fig 4b). CCL이 **interparticle 접촉↑로 전자경로 개선 + 대(大)
  부피변화에도 입자 연결성 유지**.
- ❗ **thick-C는 moderate보다 낮은 용량유지** → **과도한 코팅이 SiOx의 가역 전기화학 반응을 제한**(Li⁺
  접근 저하).

**Cycling 후 EIS(Fig 4c pre-cycling / Fig 4d after 100 cyc / Fig 4e fitted R_SEI·Rct):**
- ★ **moderate-C가 pre-cycling·100사이클 후 모두 최저 임피던스**(half-cell 추세와 일치, Fig 3d–g).
- **100사이클 후 샘플간 임피던스 격차가 더 벌어짐** → **moderate가 R_SEI·Rct를 가장 안정적으로 유지**.
  (Fig 4e: pre-cycling 대비 100사이클 후 R_SEI·Rct 증가폭이 moderate에서 최소.)
- → **moderate가 더 높은 용량(누적)을 내면서도 더 낮은 임피던스** = "안정 계면·전하수송."
- (Fig S10: 70사이클 후 **bulk 전기저항률·계면 전기저항도 moderate가 최저** — cycling 후에도.)

**Pouch cell 검증(48 mAh single-layer, 70사이클 @0.5C; Fig 5a 모식, Fig 5b cycling, Fig S9 사진):**
- ★ **coin과 일치 — coated가 bare보다 높은 초기방전·우수 유지율, moderate-C가 70사이클 최고 유지.**

**단면 SEM 형태진화(70사이클 후, Fig 5c before / Fig 5d after):**
- ★ **bare·thin·thick = 큰 전극 swelling + 심한 crack** / **moderate = 작은 두께변화·적은 구조손상.**
- **두께(70사이클 후, Fig 5d 라벨): bare ~93 µm > thin ~80(?) ≈ thick ~80 µm > moderate ~70 µm**(가장 작은
  팽창; 정확 값은 Fig 5d µm 라벨 — bare 93, moderate 70, thick ~80). ❗ **bare의 가장 큰 두께변화** =
  **poor CBD 분산이 국소 비균일 반응·interparticle 접촉 열화 → 비균일 구조진화 → 기계열화 가속**.

**SAICAS 기계강도(70사이클 후, Fig 5e 모식, Fig 5f cohesive, Fig 5g adhesive):**
| 샘플 | Cohesive strength (N/m) | Adhesive strength (N/m) |
|---|---|---|
| **bare SiOx** | **112.3** | **120.2** |
| **SiOx@thin-C** | **129.0** | **138.5** |
| **SiOx@moderate-C** | **147.0** | **196.5** |
| **SiOx@thick-C** | **134.6** | **149.9** |
- ★ **moderate-C가 cohesive·adhesive 둘 다 최고**(147.0 / 196.5 N/m). bare·thin·thick은 낮음. → **사이클 후
  증가한 porosity와 일관**(SEM Fig 5c,d). **구조열화 = crack 전파·집전체 박리 위험↑** → **moderate의 더
  균일한 전기화학 반응이 구조손상 억제 + 기계무결성 보존**. ⇒ **대(大) 부피변화 SiOx 음극에 최적 탄소코팅이
  기계무결성의 key.**

### 4.5 종합 메커니즘 (Fig 6 개념도)
- **bare:** SiOx↔CBD 약한 상호작용 → **CBD 응집(inhomogeneous)** → 이질적 미세구조.
- **carbon-coated:** 표면개질로 SiOx↔CBD 양립↑ → **CBD 균일분포**.
  - **thin-C:** CCL이 전자경로 개선하나 **반복 충방전 하 입자접촉 유지 불충분** → interparticle 접촉 점진 열화.
  - **thick-C:** 충분히 도전적 탄소망이나 **과도하게 두꺼워 Li⁺ 수송경로 연장 → Rct↑ → 비효율 반응.**
  - ★ **moderate-C:** **적절한 두께 → 대(大) 부피변화에도 전자전도망 보존 + 효율적 Li⁺ 수송** = **이온/
    전자 균형**(Fig 6 빨간 박스 "Balanced ion/electron transport"; "Facilitated ion transport" ←
    화살표와 "Facilitated electron transport" → 화살표가 moderate에서 교차).

---

## 5. 그림 한 장씩 — 무엇을 보이고 우리가 쓸 것

### 본문 Figures
- **Fig 1 (p.4):** (a–d) **TEM**(bare 매끈 / thin ~4–5 nm conformal / moderate·thick 점진 두꺼움, thick
  조밀). (e) **TGA**(0.95/2.91/4.18 wt%). (f) **bulk 전기저항률**(bare 0.033→thin 0.018→mod 0.013→thick
  0.012 Ω·cm, mod≈thick). (g) **계면 전기저항**(1.7→1.0→0.6→0.5 mΩ·cm²). (h) half-cell·(i) full-cell
  초기 전압곡선. (j) **ICE 막대**(half 73.6/80.0/81.6/81.5; full 58.7/69.1/73.1/71.8). → ★ **코팅 형태·함량·
  전자전도 saturate**(우리 "전자는 적정량에서 충분" 대응).
- **Fig 2 (p.5):** ★ 분산 핵심 — (a–d) **SSRM 단면 저항맵**(bare CBD 응집 vs coated 균질). (e) **work-of-
  adhesion 막대**(99.9/107.3/108.6/107.9, moderate 최고). (f) **유변학**(bare 고점도·급강하 vs coated 저점도·
  완만). (g) **대칭셀 EIS R_ion**(coated < bare). → ★ **SSRM 분산맵 + 표면에너지/W_adh + 유변학 = 분산
  정량 3종**(우리 additive 분산 morphology metric 후보).
- **Fig 3 (p.6):** ★ 이온/전자 균형 — (a) **charge DCIR vs SOC**, (b) **discharge DCIR vs SOC**(bare>thin>
  moderate; **thick>moderate**). (c) **rate capability**(0.2–5C; moderate 최우수, 고율 차이 큼). (d–g)
  **SOC-EIS**(bare/thin/moderate/thick; moderate 최저). (h–k) **DRT**(Z_W·Rct·R_SEI; moderate 최소). → ★
  **moderate = balance의 정량 증거**(thick의 Rct↑ = 이온차단).
- **Fig 4 (p.7):** full-cell cycling — (a) **100사이클 용량/CE**, (b) **retention**(moderate 최고). (c)
  **pre-cycling EIS**, (d) **100사이클 후 EIS**, (e) **fitted R_SEI·Rct 막대**(pre vs 100cyc; moderate
  증가폭 최소). → 장기 안정성 + 계면 안정.
- **Fig 5 (p.8):** ★ 미세구조·기계 — (a) **pouch 모식**, (b) **pouch 70사이클**. (c) **before SEM**, (d)
  **after 70cyc 단면 SEM**(bare 93 µm·crack / moderate 70 µm·적은 손상). (e) **SAICAS 모식**, (f) **cohesive
  (112.3/129.0/147.0/134.6 N/m)**, (g) **adhesive(120.2/138.5/196.5/149.9 N/m)**(moderate 최고). → ★
  **코팅→균일반응→구조·기계 무결성**(우리 coverage/기계 대응).
- **Fig 6 (p.9):** ★ 종합 개념도 — bare(CBD 응집) vs coated(CBD 균일) + thin/moderate/thick의 이온(←)·
  전자(→) 수송 화살표, **moderate에서 "Balanced ion/electron transport"**. → ★ **이온/전자 trade-off 1장
  요약**(우리 SuperP-vs-VGCF 그림과 직접 대응).

### SI Figures (S1–S11) + Table S1
- **Fig S1:** bare/thin/moderate/thick **TEM**(본문 Fig 1a–d 보강 — 코팅두께 비교).
- **Fig S2:** **Raman**(bare vs 3코팅; SiOx peak 약화 + D/G band; D/G profile 코팅품 유사 = CCL 구조 유지).
- **Fig S3:** **Li‖SiOx half-cell 초기 용량-전압**(SiOx 자체에서도 코팅 시 ICE 개선).
- **Fig S4:** **XPS**(pre-cycling 후 SiOx/graphite 전극) — C 1s(a–d) + F 1s(e–h), bare/thin/moderate/thick.
  코팅품 **Li₂CO₃·LiF↑**(SEI 보호막 효과).
- **Table S1:** ★ **OWRK 표면에너지 + work-of-adhesion**(위 §4.2 표 — γᵈ/γᵖ/γ_total + W_adh; CBD 필름 포함).
- **Fig S5:** **접촉각 이미지**(DIW·DIM on CBD film / bare / thin / moderate / thick).
- **Fig S6:** **GITT 곡선**(Li‖SiOx/graphite half-cell; moderate 최저 분극).
- **Fig S7:** **CV @0.2–0.5 mV/s**(bare/thin/moderate/thick 각각).
- **Fig S8:** **peak current vs √(scan rate)**(coated 기울기↑ = 확산 개선).
- **Fig S9:** **48 mAh pouch 디지털 사진**(bare/thin/moderate/thick).
- **Fig S10:** **70사이클 후 (a) bulk 전기저항률 + (b) 계면 전기저항**(0.5C; moderate 최저 — cycling 후에도).
- **Fig S11:** **SAICAS 측정 CCD 이미지**(전극 adhesive·cohesive 절삭).

---

## 6. 기술 미니용어집 (우리 맥락)

- **CCL (carbon coating layer):** SiOx 입자 표면의 CVD 탄소층(thin ~4–5 nm conformal → thick 조밀). 활물질
  분율은 **CCL+코어** 질량 기준 → **단일 활물질 성분**으로 취급(우리 AM 한 상에 코팅이 붙은 셈).
- **이온/전자 수송 BALANCE:** 코팅↑ → **σ_electron↑**(연속 도전망)이나 **Li⁺ 확산 장벽↑**(CCL 통과 필요)
  → Rct↑·분극↑. ★ **중간 두께가 둘의 최적 trade-off.** = 우리 σ_ionic↔σ_electronic의 긴장.
- **SSRM (scanning spreading resistance microscopy):** 전도성 AFM 팁으로 **국소 확산저항**을 매핑 → 저저항
  (활물질) vs 고저항(CBD) 공간분포 → **CBD 분산 균일도 시각화·정량.** 우리는 분산을 morphology(좌표)로
  보지만 SSRM은 **저항대비 맵** — 우리 voxel σ 맵의 실험 대응.
- **OWRK / work-of-adhesion:** 접촉각(극성 DIW + 비극성 DIM)으로 표면에너지를 **분산성분 γᵈ + 극성성분 γᵖ**로
  분해 → 두 고체상 간 **부착일 W_adh = 2(√(γ₁ᵈγ₂ᵈ)+√(γ₁ᵖγ₂ᵖ))**. **W_adh↑ = 두 상이 더 잘 붙음·양립.**
  탄소코팅이 SiOx γᵖ를 낮춰(21.6→11–14) CBD(γᵖ 0.97)에 가깝게 → 분산 개선. 우리 `--coh`(SE cold-weld·vdW
  부착)와 같은 "계면 부착" 물리축이나, **우리는 SE-SE/SE-AM 접착, 그들은 활물질-CBD 접착**.
- **DCIR / DRT:** HPPC 펄스로 SoC별 DC 내부저항; DRT는 EIS를 완화시간 분포로 분해해 **Warburg(Z_W, Li⁺
  확산)·Rct·R_SEI**를 분리. = 우리 transport(저항=1/σ) + 우리가 못 하는 **시간상수 분해**.
- **Rct (charge-transfer resistance):** 계면 전하전달 저항. ★ **thick-C에서 Rct↑** = 두꺼운 CCL의 Li⁺
  접근 차단이 전하교환을 늦춤 = "이온 차단"의 직접 지표. 우리엔 직접 대응 없음(우리는 bulk σ).
- **ICE (initial Coulombic efficiency):** 첫 사이클 효율. SiOx는 비활성상 생성으로 ICE 낮음 → 코팅이 계면
  부반응 억제로 개선(73.6→81.6% half). 우리 ASSB transport 모델엔 **ICE 축 없음**(전기화학 부반응).
- **CBD (carbon-binder domain):** 여기선 Super C65T + MWCNT + Na-CMC + SBR. 우리 CBD(SuperP/VGCF/PTFE)와
  같은 도전재+바인더 복합상 — **MWCNT = 우리 VGCF(1D 섬유), Super C65T = 우리 SuperP(0D 카본블랙)** 대응.
- **SAICAS:** 미세블레이드 깊이별 절삭 → cohesive(전극 내부 응집)·adhesive(전극↔집전체 부착) 강도. 우리
  `--coh` / binder cohesion 측정법 대응.

---

## ★ 7. 비교 vs 우리 DEM+MPM (CBD) (frame [1]–[5])

⚠ **대전제(맨 먼저, #285/#286과 동일):** 이 논문은 **SiOx/흑연 음극 + 액체전해질 일반 LIB**다 — 우리
**LPSCl sulfide ASSB(고체전해질, 무전해질 contact-network)**가 **아니다**. 따라서:
- **전기화학 절대값은 전이 불가.** 그들의 용량·ICE(73.6→81.6%)·DCIR·Rct·rate·retention은 **흑연/SiOx +
  액체전해질**의 값이고, 우리 σ_ionic/e는 **SE/AM 입자 접촉망의 Kirchhoff/Holm 전도**다 — 물리 메커니즘
  자체가 다름(전해질-매개 Li⁺ 확산 vs solid contact 전도). **수치 σ/porosity 앵커는 Bazzoun(LPSCl,
  `docs/lit_bazzoun2026_dem_fem_rnm.md`) / Varkey / Minnmann이 담당** — 이 논문에서 가져오지 않는다.
- 가져올 것은 **(a) 이온/전자 수송 trade-off 개념**(탄소 = 전자↑·이온↓, 중간 최적 — 우리 CBD blocking과
  동일 긴장), **(b) 분산 측정/정량 방법**(SSRM·표면에너지/W_adh·유변학 → 분산도), **(c) 정성 추세**(균일분산
  → 균질 전자망·덜 우회 이온경로 → 저항↓).

### (a) ★ 이온/전자 trade-off — 우리 CBD SuperP-vs-VGCF와 동일 긴장 (가장 강한 연결)
- **그들(코팅두께 축):** 탄소코팅 두께↑ → **전자전도↑(bulk 저항률 0.033→0.012 Ω·cm) BUT Li⁺ 수송 차단
  ↑(thick-C에서 Rct↑·DCIR↑·분극↑)**. ★ **moderate(~2.91 wt%)가 이온/전자 균형 = 최저 임피던스·최고 rate·
  최고 cycling.** 즉 **"탄소를 더 넣을수록 전자는 좋아지지만 이온은 나빠진다 — 중간이 최적"**.
- **우리(도전재 종류·분산 축, `docs/cbd_morphology_roadmap.md`):** voxel FV로 real_10에서 측정 —
  **SuperP가 VGCF보다 전자 1.3× vs 1.1× 더 보태지만(WITHOUT-CBD 6.464 → SuperP 8.564 vs VGCF 7.414
  mS/cm), SE 이온망은 1.8× 더 막는다(σ_ionic SuperP 0.0168 < VGCF 0.0298 mS/cm)**. = **carbon ADDS
  electron, BLOCKS ion.**
- ✅ **동일 물리축의 독립 확증:** Oh 2026의 **"탄소↑ → 전자↑·이온↓"** 는 우리 **"carbon ADDS σ_e but
  BLOCKS σ_ionic"** 와 **정확히 같은 ion/electron trade-off**다. 그들은 **탄소 양/두께** 축에서, 우리는
  **도전재 종류/분산** 축에서 같은 긴장을 본다. → **우리 CBD trade-off 서사의 독립 실험 증거**(우리 voxel
  결과가 고립된 수치가 아니라 일반 물리임을 뒷받침).
- ★ **우리가 아직 안 한 것을 그들이 줌 = "balance point" 개념:** 우리 CBD 작업은 **SuperP가 전자 win·VGCF가
  이온 win**을 "각 채널 따로" 보고했지, **"이온+전자 종합 최적 탄소량/분산"** 이라는 **단일 balance point**는
  정량화 안 했다(우리 결론은 "VGCF가 all-round safer, SuperP가 real_10 1 wt% 전자 win"이었음). Oh 2026은
  **moderate-C라는 명시적 balance optimum**을 실험으로 제시 → ★ **우리도 σ_e·σ_ionic을 동시최적화하는
  "탄소 loading sweep → 종합 transport balance" 분석을 추가할 동기**(예: 우리 CBD wt%를 0.5→4 wt% sweep
  하며 σ_e gain vs σ_ionic loss를 동시 plot → 우리만의 balance curve). 우리 roadmap의 PENDING "higher
  carbon loading(4 wt%) VGCF-regime 테스트"가 이 balance sweep의 시작점.
- ⚠ **비전이(주의):** 그들의 trade-off는 **CCL이 Li⁺의 전해질→활물질 경로를 막는 것**(전해질-매개)이고,
  우리 blocking은 **SuperP 입자가 SE 이온 packing을 물리적으로 교란하는 것**(solid SE network)이다 —
  **메커니즘이 다르므로 절대 수치/임계 탄소량은 전이 안 됨**. 또 그들 thick-C의 "이온차단"은 **Rct(계면
  전하전달)** 로 나타나는데 **우리 σ_ionic 모델엔 Rct 항이 없다**(우리는 bulk contact-network σ) → 직접
  대응 metric 부재. **개념(탄소↑→이온↓·전자↑, 중간 최적)만 이식, 폼·수치 차용 금지.**

### (b) ★ 분산 측정/정량 방법 — SSRM·W_adh → 우리 additive 분산 morphology metric
- **그들:** 분산을 **3가지로 정량** — (i) **SSRM 저항맵**(bare CBD 응집 vs coated 균질, 공간 저항대비),
  (ii) **work-of-adhesion**(OWRK; bare 99.9 → coated ~108 mN/m, 표면에너지 매칭), (iii) **유변학**(bare
  고점도·급강하 = 응집 vs coated 저점도·완만 = 균일). → **분산 균일 = 균질 전자망 + 덜 우회 이온경로 →
  R_ion↓·DCIR↓.**
- **우리(`scripts/additives.py` + cbd_morphology_roadmap):** 우리는 CBD 분산을 **morphology(좌표 분포)** 로
  본다 — **SuperP = 1.4 M distributed aggregates(분산), VGCF = 32 k concentrated long fibres(응집)**;
  PTFE는 **nucleate_frac으로 carbon에 co-locate**(CBD 형성). 우리는 분산을 **"PTFE within 0.5/1.0 µm of
  SuperP = 26/79%"** 같은 **근접도**로 정량하나, **"전극 전체에서 얼마나 균일하게 퍼졌나"** 라는 **분산
  균일도(uniformity) 스칼라 metric은 없다.**
- ★ **이식 후보 1 — 분산 균일도 metric:** 그들 SSRM 저항맵의 **공간 균질도**를 우리 식으로 = **voxel
  carbon occupancy의 공간분포 균일도**(예: 격자 셀별 carbon 부피분율의 변동계수 CV, 또는 nearest-carbon
  거리분포의 분산, 또는 carbon 클러스터 크기분포). SuperP(분산)는 낮은 CV, VGCF(응집)는 높은 CV가 나올
  것 → **우리 morphology 결과를 "분산 균일도"라는 단일 수치로 요약**해 SSRM 추세(coated 균질)와 대응. 우리
  voxel FV 입력(carbon 셀맵)에 이미 데이터가 있으니 **후처리 metric만 추가**하면 됨.
- ★ **이식 후보 2 — work-of-adhesion으로 분산 예측:** 그들은 **표면에너지 매칭(γ 분해) → W_adh → 분산
  균일도** 인과를 세움. 우리 `--coh`(SE cold-weld·vdW 부착, σ에 무영향이나 wallP에 영향)는 **SE-SE/SE-AM
  부착**만 다룬다. **carbon↔SE / carbon↔AM 표면에너지 매칭(W_adh)** 을 넣으면 **"어떤 도전재가 어디에 잘
  붙나(분산)"** 를 물리적으로 예측 가능 → 현재 우리 `nucleate_frac=0.6`(carbon에 PTFE co-locate)·
  `surface_frac=0.70`(SuperP가 AM 코팅) 같은 **경험 파라미터를 표면에너지로 근거화**할 후보. (단 LPSCl SE +
  sulfide 표면에너지는 그들 SiOx/CBD와 다르므로 **프레임만 이식, 수치는 우리 측정 필요.**)
- ⚠ **비전이:** 그들 SSRM은 **저항대비**(활물질 저저항 vs CBD 고저항)인데, 우리 LPSCl는 **SE가 이온전도체·
  AM이 전자전도체**라 저항대비 부호가 다름 → SSRM 맵 해석 직접 차용 금지. **방법론(공간 균질도 정량)** 만 이식.

### (c) thick-C의 "이온차단" = 우리 CBD ionic-blocking과 같은 방향, 다른 주체
- **그들:** **thick-C가 Li⁺ 수송을 막아 Rct↑** — 탄소(CCL)가 활물질↔전해질 사이 **Li⁺ 장벽**.
- **우리:** **SuperP가 SE 이온 packing을 막아 σ_ionic↓**(0.0168 < VGCF 0.0298) — 탄소(SuperP 입자)가
  **SE 이온망을 교란**. (`--fibre`는 ionic 무변화 = carbon이 SE σ_ionic mask에 안 들어감; blocking은 MPM
  SE-rearrangement.)
- ✅ **방향 일치:** 둘 다 **"탄소가 이온수송을 방해한다"** — 우리 finding이 **일반적 물리**임을 그들이 음극/
  액체계에서 독립 확인. 단 **주체가 다름**: 그들은 **연속 코팅층(barrier)**, 우리는 **분산 입자(packing
  교란)**. ⇒ **우리 CBD blocking이 "특이한 시뮬 artifact"가 아니라 실험적으로도 보이는 일반 trade-off**임을
  강화(모델 신뢰도↑).

### (d) frame[5] 분업 — 우리 우위 명확화
- **그들:** **post-mortem 측정(TEM/SSRM/EIS/DCIR/GITT/SAICAS/SEM) + 분산 정량 + 전기화학.** 강력하지만:
  **입자스케일 압축역학 예측 없음**(고정 미세구조), **explicit 접촉 σ triad 없음**(EIS 거시저항만),
  **소성 morphology·void-fill 예측 없음**, **압력→미세구조→σ 예측 없음.**
- **우리 DEM+MPM:** **압력→미세구조→σ(ionic/e/thermal triad) 예측** + **MPM 소성 morphology·void-fill** +
  **voxel FV로 carbon network σ_e gain·σ_ionic blocking 정량**(그들 SSRM의 mechanistic 버전) + fracture.
- ⇒ **이상 워크플로:** 우리 DEM+MPM이 CBD morphology를 생성/예측 → 그들식 **SSRM 분산 균일도·W_adh**로
  분산 검증 → 그들식 **DCIR/DRT(Rct·Z_W 분해)** 로 이온/전자 균형 닫기. 이 논문은 **우리 CBD trade-off의
  실험 reference + 분산 측정법 공급원**이지 입력단 경쟁자가 아니다. (frame[5] 재확인 — 그들엔 입자스케일
  예측·접촉 σ가 없음.)

### 비교 요약표
| 축 | Oh 2026 (SiOx/흑연·액체) | 우리 (LPSCl ASSB, CBD) | 이식/판정 |
|---|---|---|---|
| 소재 | SiOx + 흑연 + 액체전해질 | LPSCl SE + NMC811 | ⚠ 전기화학 절대값(용량·ICE·Rct·rate) 전이불가 |
| 이온/전자 trade-off | 코팅↑→전자↑·이온↓, **moderate 균형** | SuperP 전자 1.3×·이온 0.0168 vs VGCF | ✅ **동일 긴장 독립확증** + balance point 개념 이식 |
| 탄소의 이온차단 | thick-C → Rct↑(전해질-매개 Li⁺ 장벽) | SuperP → σ_ionic↓(SE packing 교란) | ✅ 방향 일치(다른 주체); 우리 blocking 일반성 강화 |
| 분산 정량 | SSRM 저항맵 + W_adh + 유변학 | morphology 근접도(분산 균일도 스칼라 無) | ★ **분산 균일도 metric + W_adh 분산예측** 이식 후보 |
| balance optimum | moderate-C 명시적 최적 | 채널별 win만(종합 optimum 無) | ★ **탄소 loading sweep → 종합 σ balance curve** 추가 동기 |
| 측정 vs 예측 | post-mortem 측정(고정 구조) | 압력→구조→σ 예측 + 소성 morphology | 우리 우위(그들엔 입자스케일 예측·접촉 σ 없음) |
| 우리 고유 | (없음) | DEM 접촉 σ triad + MPM 소성 + fracture + voxel FV | frame[5] 분업 재확인 |

---

## ★ 8. 우리 작업에 넣을 가장 날카로운 인사이트 3–5가지

1) ✅ **우리 CBD ion/electron trade-off가 일반 물리임을 독립 확증 — 모델 하자 아님, trade-off 그림 풍부화.**
   Oh 2026은 **"탄소↑ → 전자↑·이온↓, 중간이 최적"** 을 SiOx 코팅두께 축에서 실험으로 본다. 우리 voxel FV의
   **"SuperP 전자 1.3× win BUT 이온 1.8× blocking(0.0168<0.0298)"** 와 **정확히 같은 ion/electron 긴장**이다.
   → 우리 CBD blocking finding이 **시뮬 artifact가 아니라 실험적으로도 나타나는 일반 trade-off**임이 강화
   (모델 신뢰도↑). 이건 **flaw를 드러내는 게 아니라 우리 trade-off 서사를 enrich**한다.

2) ★ **우리가 안 한 "balance point"를 그들이 줌 — 탄소 loading sweep → 종합 σ balance curve 추가.**
   우리 CBD 작업은 **채널별 승자**(SuperP=전자, VGCF=이온)만 보고했고 **이온+전자 종합 최적 탄소량**은
   정량화 안 했다. Oh 2026의 **moderate-C 명시적 최적**은 **"탄소를 sweep하며 σ_e gain vs σ_ionic loss를
   동시 plot → balance optimum"** 분석의 동기다. → ★ **우리 CBD wt%를 0.5→4 wt% sweep**(roadmap의 PENDING
   4 wt% VGCF-regime 테스트가 시작점)하며 **voxel σ_e·σ_ionic을 동시 측정 → 우리만의 balance curve**를
   그리면, SuperP/VGCF 각각의 "종합 최적 loading"을 정량할 수 있다(그들 moderate의 우리 버전).

3) ★ **분산 균일도 metric을 우리 voxel/morphology에 추가 — SSRM의 mechanistic 버전.**
   그들은 분산을 **SSRM 저항맵 공간균질도 + work-of-adhesion + 유변학**으로 3중 정량한다. 우리는 분산을
   **morphology 좌표·근접도**로 보지만 **"전극 전체 균일도" 단일 수치가 없다.** → 우리 voxel carbon 셀맵에서
   **carbon occupancy의 공간 변동계수(CV) / nearest-carbon 거리분포 분산 / 클러스터 크기분포**를 후처리로
   계산하면 **SuperP(낮은 CV=분산) vs VGCF(높은 CV=응집)** 를 단일 수치로 요약 → 그들 SSRM 추세와 대응.
   추가로 **carbon↔SE/AM work-of-adhesion(표면에너지 매칭)** 을 넣으면 우리 `nucleate_frac`·`surface_frac`
   경험 파라미터를 **물리적으로 근거화**(어떤 도전재가 어디 잘 붙나)할 수 있다(단 LPSCl 표면에너지는 우리 측정 필요).

4) ★ **frame[5] 재확인 + 우리 우위:** 이 논문은 **post-mortem 측정(SSRM/EIS/DCIR/DRT/SAICAS) + 분산 정량**
   으로 강하나 **입자스케일 압축역학·explicit 접촉 σ triad·소성 morphology·압력→구조 예측이 없다**(고정
   미세구조). 우리 DEM+MPM은 **압력→미세구조→σ를 예측**하고 **voxel FV로 carbon network의 σ_e gain·
   σ_ionic blocking을 mechanistic하게 정량**(그들 SSRM 저항맵의 인과 버전)한다. ⇒ **이상 워크플로 = 우리가
   CBD morphology 생성/예측 → 그들식 분산·DRT로 검증.** 이 논문은 우리 파이프라인의 **출력단(분산·이온/전자
   균형 검증) 청사진**이지 경쟁자가 아니다.

### 보너스 실행 항목
- **#284 인덱스 갱신**(아래 완료): web-abstract 수준 → 검증 수치(TGA 0.95/2.91/4.18 wt%, bulk 저항률
  0.033→0.012 Ω·cm, 계면저항 1.7→0.5 mΩ·cm², ICE half 73.6→81.6%·full 58.7→73.1%, W_adh 99.9→108.6 mN/m,
  SAICAS cohesive 112→147·adhesive 120→196 N/m, 70cyc 두께 bare 93 vs moderate 70 µm)로 교체.
- ⚠ **혼동 금지(#285/#286과 역할 구분):**
  - **#284(이 논문, SiOx/흑연·액체):** **CBD ion/electron trade-off 독립확증 + 분산 측정법(SSRM/W_adh)
    + balance point 개념** 공급원. **수치 σ/porosity 앵커 아님.**
  - **#285(Hong, 단결정 NCMA·액체):** **rigid-AM 검증 + 점탄성 spring-back 미구현 한계** 지목.
  - **#286(Yoo, 흑연·액체):** **Phase 5 z-구배 설계 + 토모 정량(τ/PNM) + 전기화학시뮬 workflow** 청사진.
  - **σ/porosity 절대앵커는 Bazzoun(LPSCl)·Varkey(halide)·Minnmann(LPSCl cold-press)이 담당** — 이 셋과
    혼동 금지.
- **balance curve sweep**(인사이트 2)을 cbd_morphology_roadmap의 PENDING "4 wt% VGCF-regime 테스트"와
  통합 — 단일 loading이 아니라 **0.5→4 wt% 연속 sweep으로 σ_e·σ_ionic 동시 plot**하면 Oh 2026의 moderate-C
  optimum에 대응하는 **우리 balance optimum**을 얻음.

# 연세대 Digital Twin Battery Lab (Yong Min Lee 그룹) — 2026 논문 트리아지 + 우리 모델 매핑

**출처:** 연구실 Publication 리스트 2026 (논문 #260–286, 총 27편).  이 그룹은 우리 DEM+MPM
프로젝트와 **같은 도메인**(digital-twin 미세구조 모델링 + dry-processed electrode + sulfide ASSB +
2D→3D 합성 + CBD/transport)에서 활동 → 직접 인사이트 소스.

**이 문서의 역할:** 27편을 (1) 우리 프로젝트 관련도로 등급화, (2) 테마로 묶고, (3) 각 논문의 핵심
인사이트 → **우리 DEM/MPM/transport/Phase1-5 로드맵 어디에 꽂히는지** 매핑.  ★★★=직접 우리 도메인
(PDF 받아 litdb 풀 디제스트 필수), ★★=강하게 관련, ★=주변부, ·=타 화학계(카탈로그만).

⚠ 웹 초록·검색으로 확인한 내용 기반 — 풀 디제스트(수치/그림/방법 전체)는 PDF 필요.  상위 논문은
PDF 받으면 `docs/lit_<author>2026_<topic>.md`로 litdb-curator 풀 디제스트 예정.

---

## ★★★ TIER-1 — 우리 방법론 그 자체 (digital-twin / 2D→3D / bimodal)

### #266 — Bimodal Composite Cathodes, Chemo-Mechanical Integrity & Kinetics for ASSB  ⭐최우선  ✅✅ 풀 디제스트 완료 (HEADLINE 1:1 검증)
ACS Energy Letters **11** (2026) 2103-2114 (Open Access **CC-BY 4.0**, IF 17.5).  Hyeonseong Oh†, Uigyeong Jeong† …
**Yong Min Lee**, Jongsoon Kim, Junyoung Mun, … **Jong-Won Lee\*, Sang-Young Lee\*, Hun-Gi Jung\***.
DOI 10.1021/acsenergylett.5c03923.  ★ **풀 디제스트:** `docs/lit_oh2026_bimodal_composite_cathode.md`.
⚠ **저자 정정:** 초안의 "Yoon Seok Jung 공저"는 **오류** — 실제 저자에 Yoon Seok Jung 없음, 교신은 **Hun-Gi Jung**(KIST).
★★ **소재계 = 우리 정확한 소재계 + 정확한 조건:** 큰 다결정 **NCWA**(LiNi₀.₈₈Co₀.₁₀W₀.₀₁Al₀.₀₁O₂, D₅₀ 10.2 µm =
우리 **AM_P**) + 작은 단결정 **NCM**(LiNi₀.₈₂Co₀.₁₃Mn₀.₀₅O₂, D₅₀ 5.5 µm = 우리 **AM_S**) + **S-LPSCl1.5**(argyrodite
황화물, D₅₀ 0.72 µm, σ 3.09 mS/cm) + Super P + LTO 음극, **CAM:SSE:CC 90:9.5:0.5 wt%, 300 MPa 냉간압축**.  ⇒
**우리 `input_2mAh_a9_50` P:S sweep(AM:SE 90:10, P:S 0:10→10:0, 300 MPa)과 정확히 같은 실험**(P:S = poly:single =
큰:작은, 라벨까지 일치).
- **핵심:** bimodal = 큰 다결정 + 작은 단결정 CAM 블렌드 → packing↑·porosity↓ → **ionic tortuosity↓ → Li⁺ 전달↑**
  + (응력 *완화* 아닌) **균일 응력 *분산*으로 chemo-mechanical 건전성↑**.  **CAM7:3(poly:single 7:3)이 최적** —
  최저 porosity(2D 7.55% / He 8.83%) · 최저 τ_ion(11.13) · 최고 rate · VED 2649 Wh/L · **87.80% retention @200 cyc**.
- **★★ EXACT 수치(Table S1/S5/S6/S9/S12/S15):**
  - porosity 2D: 16.80/10.18/**7.55**(7:3 min)/10.93/17.96 %; He pycnometry: 12.78/10.28/**8.83**(7:3 min)/10.57/11.58 %.
  - τ_ion(MacMullin류 ε/(σ_eff/σ_bulk)): 13.08/12.13/**11.13**(7:3 min)/12.84/16.08.
  - σ_eff,ion: 0.042/0.049/**0.055**(7:3 peak)/0.046/0.034 mS/cm; σ_eff,e: 4.09/2.99/2.37/2.16/0.95 mS/cm(큰 NCWA↑→σ_e↑).
  - tap density 복합: 3.28/3.45/**3.59**(7:3)/3.43/3.26 g/cc; SE 부피 17.7–19.8 vol%.
  - 시뮬(GeoDict FVM + COMSOL FEM, 40×40×t µm³, voxel 0.1µm) ↔ 실측 편차 σ_ion **1.98%** / σ_e **3.66%**(그들 frame[4]).
  - ★★ **재료 물성(Table S15): E_SE = 22 GPa**(= 우리 real 24·Bazzoun 22.1과 정합; 우리 E_eff 1.35는 softened proxy),
    ν_SE 0.30, σ_SE 10, σ_NCWA **13.7** ≫ σ_NCM **2.45** mS/cm(σ_e가 큰 NCWA서 높은 이유), Holm형 R_c(SE-SE 4.5e-6 Ω·m²).
- **★★★ 우리 a9_50 sweep과 1:1 (frame[4] 교차검증 — HEADLINE):**
  - **porosity dip ✅ 모양 1:1:** #266 2D 7.55/He 8.83 @CAM7:3(양 끝 UCC↑) ↔ 우리 DEM 12.70 @p06(양 끝 mono-modal↑).
    Furnas/de Larrard bimodal dip을 우리 rigid DEM이 독립 재현.  최적위치 #266 7:3(poly 0.7) ↔ 우리 6:4(poly 0.6) =
    sweep 간격 0.2에서 인접 = **0.6–0.7 sweet spot**.
  - **물리 porosity 절대값 ✅ like-for-like:** #266 He pycnometry(8.83% @CAM7:3, 3D 물리) ↔ 우리 **MPM 소성**(10.44%
    @p06) — **~1.5%p 차로 매칭**(MPM이 #266 He 범위).  우리 **DEM rigid**(12.70%)는 He보다 약간 위(= rigid floor,
    소성 flow 부재); **2D-SEM(7.55%)은 셋 중 최저**(단면 누락).  → **#266 He = MPM(소성); dip 모양 = DEM(rigid Furnas)**.
  - **σ_ionic peak ✅ 위치 1:1:** #266 0.055 @CAM7:3 ↔ 우리 0.0506 @p06.  절대 같은 자릿수(envelope 0.03–0.14 mS/cm,
    Bazzoun+#271+#266 통합).  τ dip도 우리 τ_Laplace,eff(3.29 @p06) ↔ #266 τ_ion(11.13)으로 추세 1:1(정의 달라 절대 X).
  - **기계취약 = 큰 다결정 ✅ 1:1:** #266 ΔP·D1(기계열화) max @CAM10:0 ↔ 우리 fracture severe 63% @p10(큰 다결정 분쇄);
    작은 단결정은 #266 ΔP min·우리 AM_S intact(#285 단결정 균열억제 일관).
  - ⚠ **σ_e 방향은 가정-의존:** #266 σ_NCWA 13.7 ≫ σ_NCM 2.45(큰 NCWA→σ_e↑) vs 우리 σ_e는 입자수·접촉수 지배로 작은
    NCM서↑ → 표면 부호 반대.  ⚠ **우리 σ_e 끝점 가정(σ_S-poly 10 > σ_P-single 5)이 #266과 부호 반대** → 재검토 항목.
- **★ audit 마감(유저가 fold):** #3(bimodal) ✅ qualitative → **✅ QUANTITATIVE**(우리 a9_50이 dip·최적·σ_ion·끝점 1:1 재현);
  #6(porosity) ⏳ pending → **✅**(우리 MPM 10.44% ↔ #266 He 8.83% like-for-like; DEM = rigid-floor offset 명시 조건부).
- **★ DB 후보(직접 추가 안 함, 디제스트 §9):** densification_porosity_db.csv에 oh2026 per-composition He porosity 5행
  (E_SE=22, He=물리); 새 `docs/data/oh2026_sigma_ionic.csv`에 σ_ion/σ_e/τ_ion 5행(LPSCl1.5 100 MPa, 같은 자릿수 envelope).
- ⚠ **전이 경계:** SE = Li₅.₅PS₄.₅Cl₁.₅(Cl-rich, σ_bulk 3.09) ≠ 우리 Li₆PS₅Cl(같은 argyrodite, Cl↑); porosity(370 MPa
  He 펠릿)·σ(100 MPa)·양극(300 MPa) 압력 상이; τ_ion = MacMullin류(11–16) ≠ 우리 측지 τ → **추세·peak·자릿수 1:1,
  절대 정밀 비교는 σ_ionic·He-porosity로 제한**.  시뮬 = rigid sphere/polyhedron + 연속체(소성 SHAPE 없음 = 우리 DEM과
  같은 한계, MPM이 보완).

### #263 — Stochastic 3D Microstructures from 2D Images (polymeric separators)  ⭐Phase 4 청사진
Advanced Energy Materials 16(10) (2026) e70730 (Back Cover, IF 25.5).  Youyeong Shin†, Suhwan Kim† … Yong Min Lee.  DOI 10.1002/aenm.70730.
- **핵심:** 2D 이미지에서 구조 파라미터 추출 → **stochastic하게 3D 가상 미세구조 생성** → 전기화학
  성능 예측.  separator digital-twin.  핵심 구조 파라미터를 **독립적으로 변화** → 미세구조↔이온수송
  관계 규명 → 합리적 설계.  (phase-contrast nano-CT로 lamellae + 2D SEM로 sub-100nm fibril을
  stochastic 재구성 → 3D 통합.)
- **우리 모델 매핑 (= 우리 Phase 4-5 그 자체):**
  - **"예측 수치 → 2D 이미지 → 3D 미세구조"가 정확히 우리 Phase 4** (`scripts/extract_2d_microstructure.py
    synthesize_microstructure`의 targets-only 진입점).  이 논문이 **published blueprint**.
  - "구조 파라미터 독립 변화 → 수송 예측" = 우리 predictor(design knobs → metrics) + 합성 파이프라인.
  - 2D→3D stochastic 재구성 = 우리 z-stacking/layered 합성(Phase 5)에 직접 이식할 방법.
  - **ACTION:** 이들의 2D-param-추출 → stochastic-3D-생성 방법을 우리 synth와 비교; 우리 합성이 같은
    구조 파라미터(porosity, tortuosity, 입경분포)를 보존하는지 검증 프레임으로 채택.

### #271 — Unveiling Degradation of Sulfide Composite Cathodes, Digital-Twin: Dry vs Wet Binder  ⭐⭐ TIER-1 (우리 소재계 = σ 절대앵커)  ✅ 풀 디제스트 완료
Energy Storage Materials **86** (2026) 104930 (IF 19.3), DOI 10.1016/j.ensm.2026.104930.  Seung-Bo Hong†,
**Hyobin Lee†**(digital-twin 모델러) … Yong Min Lee\*, Un-Hyuck Kim\*, Dong-Won Kim\* (Hanyang + DGIST +
Yonsei DTBL).  접수 2025-12-01 / 게재확정 2026-01-26.  ★ **풀 디제스트:**
`docs/lit_hong2026_sulfide_cathode_binder_digitaltwin.md`.
★★ **소재 = Li₆PS₅Cl(LPSCl) 황화물 SE + NCM CAM, ASSB = 우리 정확한 소재계**(Bazzoun과 동일).  ⇒
**#284/#285/#286(액체 LIB)과 결정적으로 다르게 σ_ionic·porosity·retention 절대값이 (조건 매핑 후) 전이
가능 → 검증 앵커.**  σ/porosity 앵커군 = **Bazzoun(LPSCl) + #271(LPSCl) + Varkey(halide) + Minnmann**.
⚠ **#285(Rakhwi Hong, 단결정NCMA·액체)와 다른 논문**(같은 "Hong"이나 #271=Seung-Bo Hong/ASSB — 혼동 금지).
- **핵심:** sulfide ASSLB 복합양극을 **4구성(Pwd 무바인더 / S-Pwd 용매만 / NBR wet / PTFE dry)**으로
  제작해 용매↔바인더 decouple.  **PTFE = confined fibril망(최소 coverage) → 연속 Li⁺ 경로·void 최소 →
  retention 최고**; **NBR = 깊이침투·광범위 coverage → Li⁺ 차단 + 계면 void 성장 + LPSCl 산화분해(sulfate→
  rock-salt) 가속**.  **용매효과는 minor, 바인더 공간분포가 dominant.**  디지털트윈 = **GeoDict GrainGeo
  재구성 + ConductoDict FV**(σ_ionic는 입력, coverage·current density 출력 = reconstruct-from-measurement).
- **핵심 수치:** ★★ **σ_ionic Pwd 0.087 / S-Pwd 0.079 / PTFE 0.064 / NBR 0.042 mS/cm**(Table S2; σ_e
  1.11/1.07/0.85/1.10); **retention@100cyc 0.33C: PTFE 94.6 > Pwd 92.0 > S-Pwd 87.1 > NBR 85.4%**(Table S1);
  **pore volume PTFE 22.3 / Pwd 28.7 / NBR 29.4 vol%**(Fig 2f); **AM coverage(디지털트윈) LPSCl/CBD =
  Pwd 35/5 · NBR 26/27 · PTFE 36/9 %**(Fig 2c); **Δ(ΔP)_Q(부피팽창) NBR 1.99 vs PTFE 1.74**(Pwd 1.88/S-Pwd
  1.89); **bulk LPSCl σ 1.87 → 0.53 mS/cm(28% 잔존, butyl butyrate)**(Fig S7, XRD 변화無); **R₁@2.4V NBR
  17.4 vs PTFE 12.8 Ω**, R₂(NBR 급발산 vs PTFE 포화); **XPS S 2p 100th SO₄²⁻ NBR 4.4%(PTFE 無)**;
  **rock-salt 깊이 NBR 17–22 vs PTFE 8–10 nm**(SAED); SAICAS PTFE ≈ 2× NBR.  활물질 loading 30 mg/cm².
  조성 NCM:LPSCl:Super C:바인더 = 75:22.5:1.5:1(PTFE/NBR).
- **우리 모델 매핑 (★ TIER-1 — σ_ionic 절대 검증 + audit #1/#5 진전; 수치 전이됨):**
  - **(a) ✅✅ σ_ionic 절대값 in-range:** 그들 LPSCl 양극 σ_ionic **0.042–0.087** ⊂ 우리 DEM 범위
    (~0.04–0.18); Bazzoun(0.065–0.137)과 합쳐 **LPSCl+NCM 실측 envelope ≈ 0.04–0.14 mS/cm** → **우리 절대
    σ_ionic이 "외삽 1점(Bazzoun)"에서 "2개 독립 EIS 실측에 둘러싸인" 상태로 격상**(audit #1 다점화).  추세
    (coverage/φ_SE↓→σ↓) 일치.  ⚠ 압력 350/400/300 MPa + vol% 매핑은 정밀 1:1 전 보정 필요.
  - **(b) ✅ bulk σ_grain 정합:** Hong 1.87 ∈ (Bazzoun pellet 1.02, Cronau 단결정 3.0) — GB-포함 다결정
    범위 일관.  우리 σ_grain=3.0+Cronau(r_SE) 점검(이중계상 주의).
  - **(c) ❗ PTFE 양의 역학효과(audit #5):** 우리는 PTFE를 **σ=0 obstacle(차단=음효과)**로만 모델 → 이
    논문의 **PTFE void-억제(−6.4%p pore)·팽창↓(1.74)·접착 2×**(양효과, retention 지배)를 누락.  ⇒ MPM에서
    **PTFE를 cohesion-부여 결합상(`--coh` PTFE항)**으로 → void-억제 재현; net σ_ionic = "차단 − densification
    회복"(그들 0.064에 맞추려면 양효과 필요).  audit #5에 "PTFE 기계적 void-억제 미반영" 신규 항목 근거.
  - **(d) 디지털트윈 = GeoDict reconstruct(출력단):** σ_ionic 입력·coverage/current density 출력 =
    `positioning_vs_geodict.md`의 "GeoDict는 구조를 줘야 함"을 **ASSB 양극 사례로 재확인** → 우리 공정→구조
    **predict(입력단) + Kirchhoff/Holm 접촉망** superset 강화.  그들 AM-coverage % = 우리 Stage-E coverage
    검증 reference.
  - **(e) ⚠ 비전이:** NBR(wet 공정) = 우리 모델 없음(process-specific).  시간(cycling) 화학-기계 열화
    (void 성장·rock-salt·sulfate) = 우리도 그들 디지털트윈도 단일 스냅샷 → 공통 GAP(Phase 4 후보).
  - **★ DB 후보:** §11(디제스트) — LPSCl porosity@350MPa(Pwd 28.7/NBR 29.4/PTFE 22.3) + σ_ionic 4점.
    `densification_porosity_db.csv` + `bazzoun2026_sigma_ionic.csv` 추가 후보(유저 결정).

### #262 — Digital Twin Mechanical Degradation Diagnostics, Si Anode Microstructure  ★★★
Small 22(3) (2026) e07883 (IF 11.8).  Jaejin Lim†, Junhyeok Choi† … Hyobin Lee, Yong Min Lee.  DOI 10.1002/smll.202507883.
- **핵심:** Si 부피변화 >300% → 접촉손실/박리/균열.  **FIB-SEM 토모그래피 3D 재구성** + Li⁺확산·계면
  반응·농도의존 기계변형 **결합 시뮬**.  충전율 0.5C→4C이 SoC 제한으로 응력↓ → 기계 열화 완화.
  응력기반 파괴 진단 digital-twin.
- **우리 모델 매핑:**
  - FIB-SEM 3D 재구성 = 우리 미세구조; **결합 전기-화학-기계** = 우리 MPM(mechanics)+DEM(transport).
  - "응력기반 파괴" ~ 우리 **fracture(Auerbach/Holm)** + MPM 응력장.  C-rate→응력→열화는 응력장
    degradation metric 아이디어.
  - digital-twin이 우리 프레임과 동일 → 그들의 결합 방식(Phase 4 PyBaMM과 연결될) 참고.

### #281 — Microstructure-Guided Reactant Transport, Architected 3D Air Electrodes (Li-O₂)  ★★ (→ Phase 4 blueprint급)  ✅ 풀 디제스트 완료
Journal of Power Sources **686** (2026) 240471 (IF 8.4), DOI 10.1016/j.jpowsour.2026.240471.  Suhwan Kim†,
Seungwon Jung† … Seokwoo Jeon\*(KU), Yong-Mook Kang\*(KU/UCSD), Yong Min Lee\*(Yonsei DTBL).  접수
2026-04-16 / 게재확정 2026-05-19.  MDB 2025 특별호.  ★ **풀 디제스트:**
`docs/lit_kim2026_a3d_air_electrode_microstructure_transport.md`.
⚠ **소재 = Li–O₂ 전지(금속-공기) 공기극** — Li metal 음극, **O₂ 가스**(주변 공기) + 액체전해질
(**1 M LiCF₃SO₃ in TEGDME**) 중 Li⁺, 방전생성물 **Li₂O₂**, 양극 골격 **Ni**(A3D BCT/diamond 또는 foam).
**우리 LPSCl sulfide ASSB가 전혀 아님** → **모든 전기화학·구조 절대값(용량·과전압·SSA·D_O₂·σ) 전이불가**.
가져올 것은 **METHODOLOGY 3종**(아래) — 수치 σ/porosity 앵커 아님(Bazzoun/Varkey/Minnmann/#266이 담당).
- **핵심:** **3D 디지털트윈 구조분석(GeoDict) + 1D 전기화학 모델(COMSOL) 결합**으로 architected-3D(A3D)
  공기극 미세구조 → reactant(O₂·Li⁺) 수송 엔지니어링. **구조변수(SSA·porosity·유효 D_O₂·유효 σ_e/σ_ion)를
  독립 변화시켜 산소수송·반응국소화·방전용량·과전압을 분리(decouple)**. ★ **단위셀 주기↓ → SSA↑(반응
  site↑) but pore 좁아짐 → 유효 D_O₂↓ → 고율 용량 제한(trade-off)** → **diamond 단위셀(잘 연결된 pore
  network) + electropolishing 표면공학(D300EP)**으로 SSA↑를 산소수송 보존과 양립 → **+37% 용량**.
- **방법:** **GeoDict 2025**(STL→voxel **0.01 µm**; ProcessGeo 'Repeat'·GrainGeo 'Roughen Surface'·
  FoamGeo·**MatDict**=SSA·**ConductoDict**=유효 σ_e/σ_ion·**DiffuDict**=유효 D_O₂) + **COMSOL 6.3 1D
  전기화학**(방전 ORR만; separator|air electrode|GDL 3도메인; 'Lithium-Ion Battery'+'Transport of Diluted
  Species in Porous Media'+'Domain ODEs and DAEs'; Li₂O₂ **film형 성장**(50 Ω·m²) → SSA·porosity↓·기공막힘).
  = 이 그룹 **3번째 GeoDict 활용**(#286 τ/PNM, #284 W_adh 다음).
- **핵심 수치:** A3D vs foam — 유효 **σ_e 2.51×10⁵ vs 0.40×10⁴ S/cm**(6배↑), **SSA 1.02×10⁷ vs 0.88×10⁵
  m²/m³**(~116배↑), porosity 45.6 vs 80.2 %; BCT B600/B500/B400/B300(Table S3) **SSA 1.02/1.69/2.10/2.88
  ×10⁷**(period↓ 단조↑), **유효 D_O₂ 0.92/1.67/1.29/1.46 ×10⁻⁸ cm²/s**(비단조, B500 최대), porosity
  45.6/56.9/51.1/54.3 %; 고율 용량 **B500 최대**(SSA 최고 B300 아님 — D_O₂가 지배), 과전압 B300 최소;
  decouple — **0.01 mA/cm²(저율): porosity가 용량 지배**(±15%p→±~30% 용량), **0.05(고율): SSA가 지배**
  (절반→−34.6%, 2배→+37.9%), **D_O₂ 비단조**(고율 1.5×에서 anomalous 열화→국소집중·기공막힘); 전자/이온
  전도도 변화는 무영향(rate-limiting 아님); **D300EP areal capacity B500/D400 대비 +37%**(고율). 1D 모델
  Table S2 전체셋(공기극 8/GDL 192/separator 420 µm; t₊ 0.92; D_O₂ 4.17e-8; O₂농도 9.46 mol/m³; 전류
  0.01/0.05/0.10 mA/cm²).
- **우리 모델 매핑 (★ METHODOLOGY 3종 — 수치 앵커는 Bazzoun/Varkey/Minnmann/#266):**
  - **(a) ✅ GeoDict ConductoDict/DiffuDict ↔ 우리 `voxel_conductivity.py` FV:** 둘 다 voxel에 ∇·(σ∇φ)=0
    (전도)/정상상태 Fick(확산) → 균질화 유효물성. **수학적으로 동일**(상용판). ✅ 우리 voxel FV 접근 확증.
    우리가 이미 정리한 한계(점접촉 sub-voxel→constriction 못 잡음, `voxel_conductivity_crossvalidation.md`)
    동일 적용 — 정렬골격(A3D/AM)엔 맞고 granular SE엔 DEM Holm 필요(frame[5]). ★ **DiffuDict(유효 D_eff/τ)는
    우리에게 없음** → voxel FV에 확산모드 추가 → contact-network τ와 frame[4] 교차검증 이식 후보.
  - **(b) ★★ 미세구조→effective→COMSOL 1D ↔ 우리 미세구조→effective→PyBaMM Phase 4 = published blueprint:**
    그들 COMSOL 1D(effective ε/τ/σ/D 주입→방전곡선, Table S2) = 우리 PyBaMM DFN
    (`{"transport efficiency":"tortuosity factor"}`로 τ 주입 + σ 주입). 결합 디테일 3종 직접채택:
    (i)핵심전극=측정 effective·보조도메인=Bruggeman ε^1.5 혼용, (ii)동역학 파라미터는 문헌+실험fit 후 고정·
    구조변수만 변화, (iii)방전부터·충전은 추가물리로 분리. ⚠ 방정식/물성은 Li-O₂ 특유→ASSB로 교체
    (단일이온 t₊≈1·접촉저항·무O₂).
  - **(c) ★ 구조변수 decouple→성능 귀속 ↔ 우리 predictor(knobs→metrics→성능):** 사고 동형(그들=물리모델
    1변수 sweep, 우리=ML 다변수). ★ **DOD colormap(작동조건이 어느 변수 지배) + 5축 레이더(다목적 구조-물성
    균형)** 시각화를 우리 predictor 출력에 이식 후보.
  - **우리 우위:** 그들은 **고정 미세구조(CAD/리소그래피) + GeoDict + 1D 전기화학(출력단)**; 우리 DEM+MPM은
    **압력→미세구조 예측(입력단) + 소성 morphology + 접촉 σ triad + granular constriction + fracture**. ⇒
    이상 워크플로 = 우리가 미세구조 생성/예측 → GeoDict식 effective(우리 voxel FV) → 그들식 1D 전기화학
    (우리 Phase 4). frame[5] 분업 재확인(그들엔 입자스케일 압축예측·접촉 σ triad 없음 — 논문도 자인:
    "1D framework relies on volume-averaged effective properties... cannot capture pore-scale
    heterogeneities"). ⚠ Stage-2 audit 영향 없음(Li-O₂ 외래 + Phase-4 결합 방법론 → transport 판정에 새
    벤치 없음); Phase 4 결합 프로토콜은 `stage4_electrochem_research.md` 반영 가치.

---

## ★★ TIER-2 — Dry-processed electrode / ASSB / CBD / 압축 (강하게 관련)

### #285 — Modulating CBD Viscoelasticity Suppresses Time-Dependent Spring-Back (Single-Crystal Cathodes)  ★★★  ✅ 풀 디제스트 완료
Energy Storage Materials (2026), DOI 10.1016/j.ensm.2026.105321 (PII S2405-8297(26)00453-8, ENSM 105321,
IF 19.3).  Rakhwi Hong†, Jingyu Choi† … Yong Min Lee\* (Yonsei DTBL).  접수 2026-04-03 / 게재확정 2026-06-20.
★ **풀 디제스트:** `docs/lit_hong2026_cbd_viscoelasticity_springback.md`.
⚠ **소재 = 단결정 NCMA(LiNi₀.₈₆₅Co₀.₀₅₄Mn₀.₀₇₅Al₀.₀₀₇O₂) 양극 + CBD(Super P+PVDF) + 액체전해질
(1.15 M LiPF₆ EC/EMC 3:7) 일반 LIB** — **우리 LPSCl sulfide ASSB가 아님** → 전기화학 절대값 전이불가.
**단 #286(흑연 pore 수송, 무관)과 달리 이 논문은 입자/CBD 역학(단결정 견고성·균열·압축·spring-back·CBD
점탄성)이 주제 → 역학은 (주의해서) 전이됨.**
- **핵심:** **단결정 CAM은 견고 → 균열·변형으로 에너지 못 빼므로 압축응력이 무른 점탄성 CBD로 몰림.**
  CBD 점탄성은 온도의존: **RT(25°C) → 탄성 CBD → 응력저장 → 시간의존 spring-back**(3주 **58→61.7 µm,
  +4 µm**); **HT(80°C) → 사슬이동도↑ → 점성/compliant CBD → 응력소산 → spring-back 억제**(3주 **+1 µm**).
  다결정은 입계균열로 소산 → spring-back 무(Table S1: 66 µm 유지). 코드 **RC-P/RC-S/HC-P/HC-S**(RT/HT ×
  pristine/3주stored).
- **핵심 수치:** spring-back RC-S +4 µm vs HC-S +1 µm; **500사이클 retention HC-P 69.9% / HC-S 67.2% /
  RC-P 62.6% / RC-S 32.4%(최악)**; bulk 전자저항 pristine 0.50 → stored 0.56 Ω·cm; **nanoindentation h_max
  RT 1193 → HT 1948 nm**, **dissipation ratio 0.62 → 0.67**; **DMA E′ HT −41.2%**(tan δ는 온도↑→↑);
  치밀화효율 RT는 roll gap 60 µm·HT는 70 µm에서 목표밀도; **CAM–CBD 계면접촉 HC-S +25%**, **유효 σ_e
  +50%**(RC-S 0.19 → HC-S 0.32); CAM/CBD σ_e = **0.7 / 500 S/m**(Table S2). 검증 = 2D SEM 재구성 +
  GeoDict(MatDict/PoreDict/ConductoDict) + DMA + nanoindentation + HPPC/EIS.
- **우리 모델 매핑 (★ 역학 검증 + spring-back 한계 지목 — 수치 σ/porosity 앵커는 Bazzoun/Varkey/Minnmann):**
  - **(a) ✅ 검증:** "단결정=견고 → 압축이 무른 상으로 몰림" = **우리 MPM rigid-AM scaffold + soft-plastic
    SE 분담의 실험 정당화**(우리 AM_S=single-crystal을 `--am-scaffold` 고정 obstacle로 둔 게 옳음).
    Stage-2 audit #7의 단결정 견고성 측면을 **검증**으로 굳힘.
  - **(b) ❗ 균열 GAP:** 다결정 입계균열→에너지소산→spring-back억제는 **역학 균열 역할**. 우리 DEM 균열은
    **transport(σ↓, Auerbach/Holm)만**, MPM은 균열 자체 없음(AM=rigid). (i)균열→두께 연결 + (ii)poly>single
    균열경향 **둘 다 없음** → chemo-mechanical(Phase 4) 한계.
  - **(c) ❗ 시간의존 spring-back 재현 불가(핵심):** 그들 spring-back = **점탄성=시간의존(3주)+온도의존**.
    우리 MPM = **rate-independent J2**(시간·점성·온도 전무), hold-relax는 ~40 substep **순간 settling**
    (`mpm3d_compaction.py:636-642`). ⇒ **구조적으로 시간의존 spring-back 재현 불가** = CLAUDE.md "springback
    validation pending"의 **정체**. **하자 아닌 미구현 물리**(정적 압축 종점은 옳게 줌). 해결 = MPM에
    **점탄성 요소(SLS=Maxwell+병렬스프링) + η(T)/E(T) DMA 캘리브** 추가. 이 논문이 검증데이터 제공.
  - **(d) ❗ CBD 역학 활성화:** 그들 **CBD 점탄성 = THE 설계변수**(spring-back 지배). 우리 `additives.py`
    CBD = 기하/부피/전자블로킹만(역학 없음). spring-back 다루려면 **CBD를 능동 점탄성 역학체로**(MPM에 CBD
    material point + 점탄성 + σ_e). transport-only Stage-2엔 불필요.
  - **(e) ❗ Calendering 온도축 GAP:** RT/HT가 그들 핵심 dial. 우리는 압력/변위만(온도·roll gap 없음). η(T)/
    E(T) 넣어야 온도효과 예측가능. ⚠ ASSB는 cold-press가 표준 → 온도축은 일반 LIB 확장/ASSB 고온공정 시만 우선.
  - **★ 워크플로 이식:** 2D SEM 재구성→GeoDict(계면접촉면적·pore size·**전류밀도 국소화/분산 맵**·유효 σ_e)
    = 우리 `voxel_conductivity`/`viz_mpm_continuum` 출력 추가 후보(#286과 동일 도구 — 전류밀도 localization
    맵은 우리 StageE coverage/force-chain 대응 시각지표).
  - **우리 우위:** 그들은 **post-mortem 2D 재구성 + 연속체 전자전도**; 우리 DEM+MPM은 **압력→미세구조→σ
    triad 예측 + 소성 morphology + 압축역학**. frame[5] 분업 재확인(그들엔 입자스케일 예측 없음).

### #276 — Materials/Process-Driven Microstructural Engineering for Dry-Processed Electrode (리뷰)  ★★ → ★★★(positioning anchor)  ✅ 풀 디제스트 완료
Materials Horizons **13** (2026) 3149-3177 (Back Cover, IF 11.4, Open Access).  DOI 10.1039/d5mh02484f.
Gwonsik Nam†, Jaejin Lim†, Seungyeop Choi† … **Yong Min Lee\*** (Yonsei DTBL + POSCO).  ★ **풀 디제스트:**
`docs/lit_nam2026_dpe_microstructure_review.md`.
★ **이 그룹(이용민 DTBL)의 자기 도메인 리뷰 = 우리 DEM+MPM 프로젝트 전체의 FRAMEWORK/POSITIONING 논문.**
⚠ **일반 Li-ion DPE 리뷰**(우리 LPSCl sulfide ASSB가 specifically 아님) → **정량 셀 절대값(mAh/g·ICE·
retention)은 Li-ion 맥락**. 그러나 **(a) 미세구조 엔지니어링 framework, (b) 4단계 공정 taxonomy, (c) 미세구조-
특징 어휘, (d) 정성 DPE 사실/에너지%는 DIRECTLY 전이**(DPE는 ASSB 양극 선도경로 + 미세구조 물리 화학계 무관;
리뷰가 LPSCl 사례 직접 인용 ref 57·119·148). **수치 σ/porosity 앵커가 아니라 framework 앵커**(앵커는
Bazzoun/Varkey/Minnmann/#266).
- **핵심:** DPE 제조를 **4단계(powder mixing · kneading · laminating · **calendering**)**로 해부 + **3대
  결함(non-uniformity · delamination · heterogeneous densification/crack)**의 기원 + 소재(AM/도전재/binder-
  PTFE&대안/집전체) 혁신을 **미세구조 최적화 관점**으로 종합. **bi-directional material↔process interplay**가
  미세구조를 빚는다는 thesis(소재 혁신이 공정한계 완화, 공정전략이 소재제약 수용).
- **★ 미세구조 5대 핵심특징(= 우리 DEM+MPM 출력 1:1):** ① 각 성분 spatial distribution/morphology, ②
  **AM–CBD interfacial contact**(= 우리 coverage/Tabor), ③ **effective active surface area(ASA)**(= 우리
  ASA), ④ **ion-percolation tortuosity**(= 우리 τ_Laplace,eff/τ_Dijkstra + σ_ionic C(τ)), ⑤
  **electron-conduction continuity**(= 우리 σ_e 접촉망/CN/percolation). → rate/cycle/energy/safety 결정.
- **★ 정량 DPE 사실(positioning 인용):** drying+회수 = full-cell 제조에너지 **46.84%**; NMP 회수 ~10 kWh/kg
  (잠열 **45×**); DPE 전환 → **CAPEX·OPEX 각 −20%·장비 −30%·coating +20%·CO₂ −60%**(WPE 2.3 kg CO₂/kWh);
  loading **20→70 mg/cm²(~75→200 µm)** → 비활성 21→6%·GED 475→541 Wh/kg; binder **<1 wt%** self-standing.
  PTFE 피브릴화(Maxwell, 2022 Tesla Model Y). LPSCl+PTFE(H) ASSB 사례 209.7 mAh/g·97.4%@300cyc(ref 85).
- **★ 매핑(positioning의 심장):** 리뷰=**DESCRIPTIVE**(정성), 우리 DEM+MPM=**PREDICTIVE**(압력→미세구조→σ
  triad + 소성 morphology + fracture). ⇒ 우리 작업 = **이 리뷰가 정의한 미세구조 엔지니어링 framework의 정량
  엔진.** calendering(§3.4 feed/nip·bimodal void-fill·crack) = 우리 압축; mixing/분산 = CBD seeding(SuperP/
  VGCF); bimodal PC+SC(Fig 6b/c, ref 116/**119 LPSCl**) = 우리 **Furnas dip + #266 P:S 7:3 + 12:4:1**;
  frame[5] 분업(transport 특징 = DEM / mechanics 특징 = MPM)을 리뷰가 둘 다 명명 → 분업의 독립 정당화.
- **★ honest GAP:** **delamination/집전체 adhesion**(§3.3, 3대 결함의 하나) = 우리 미모델(bulk RVE만);
  kneading 피브릴화 rheology(우리는 fibril 형태만 seeding); calendering 온도/전단장(우리 압력만); PTFE
  defluorination ICE 손실(우리 PTFE 기계/부피만). → 논문에서 "bulk 미세구조 집중, 집전체 계면은 future work".
- **ACTION:** intro/significance에서 우리 작업을 **이 framework의 정량 엔진**으로 인용(5특징↔우리출력 표);
  압축을 "calendering(densification)"으로 재명명; bimodal/dip을 Fig 6b/c 근거로 강화; 에너지% 사실을 "왜
  DPE/우리 작업이 중요한가" 동기로. ⚠ **수치 앵커 아님 — framework 앵커**(혼동 금지).

### #275 — Continuous Carbon Nanotube Sheath, Dry-Processed Thick Electrodes  ★★  ✅ 풀 디제스트 완료
Joule **10** (2026) 102392 (IF 37.1), DOI 10.1016/j.joule.2026.102392.  Jin Kyo Koo†, Jaejin Lim† …
Hyun-seung Kim\*, **Yong Min Lee\***, Young-Jun Kim\* (SKKU SAINT/SIEST + Yonsei DTBL).  ★ **풀 디제스트:**
`docs/lit_koo2026_swcnt_sheath_thick_electrode.md`.
⚠ **소재 = NCMA(LiNi₀.₈Co₀.₁₅Mn₀.₀₃Al₀.₀₂O₂) 양극 + 인조흑연 음극 + 액체전해질(1.15 M LiPF₆ EC:DEC:DMC
25:45:30 +1% VC +1% LiPO₂F₂) dry-to-dry 일반 LIB** — **우리 LPSCl sulfide ASSB가 아님** → 셀 전기화학
절대값(Wh/L·SOC·τ·D_eff) 전이불가. ★ **단 CARBON-MORPHOLOGY 물리(연속 1D sheath가 두꺼운 전극 전도를
이기고, discrete 도전재는 이온채널을 막음)는 소재-일반 → 우리 voxel CBD 발견에 직접 전이.** 수치 σ/porosity
앵커 아님(Bazzoun/Varkey/Minnmann/#266 담당).
- **핵심:** NCMA 입자를 **SWCNT로 zeta-potential 변조 wrapping**(양이온 고분자 PDDA: NCMA −33.8 → PDDA-NCMA
  +14.2 → SWCNT −35.0 부착 → 합성물 **−1.92 mV near-neutral** = 완전 conformal coverage) → **연속·vein-like
  도전 sheath**. 도전재 별도첨가 0(SWCNT 0.2 wt%만) + PTFE 0.3 wt% → **활물질 99.7 wt%, ρ ~4.0 g/cm³**,
  초후막 >11 mAh/cm²(~200 µm). **"통합 활물질-도전재"** = 도전재를 표면통합해 기공(이온채널)을 비움 → 전자·
  이온 동시 균질.
- **검증:** FE-SEM/HR-TEM/AFM(conformal wrapping) + zeta + EDS(C가 Ni/Co/Mn/Al co-localized) + Raman(RBM+G/D) +
  XRD(구조 유지) + 분말전도 + KPFM(work function=SOC 균질도) + SAICAS + SSRM(사이클 전후) + HAADF-STEM/EELS +
  **3D digital twin(FIB-SEM 토모 820장 → GeoDict 2023 effective + PNM + 2C 방전 전기화학 2.15% 오차 + VMS)**.
- **핵심 수치:** zeta **−33.8/+14.2/−35.0/−1.92 mV**; 분말전도 (NCMA+CB)0.06 vs SWCNT-NCMA **0.20 S/cm**(>3×);
  4종 전극 밀도 CB-wet 3.6 / SWCNT-wet 3.8 / **SWCNT-dry 4.0** g/cm³(조성 99.7(99.5:0.2):0:0.3 = AM:CB:PTFE);
  저항 vs Q_areal CB-wet 10→40 Ω·cm+균열 vs **SWCNT-dry 5–10 안정**; KPFM CB-wet 넓은분포(heterogeneous SOC)
  vs **SWCNT-dry 5.95 eV 단일peak(homogeneous SOC)**; SAICAS 접착 SWCNT-dry 0.47(0.3% PTFE) vs CB-wet 0.43 N
  (1.0% PVDF); digital-twin **closed pore CB-wet 2× / tortuosity 2.31 vs 1.28 / 유효확산 D_eff 1.0e-11 vs
  2.5e-11 m²/s(2.5×) / 전해질구배 29.7 vs 7.8 mM/µm**; 30cyc 유지 SWCNT 84–90% vs CB 58–68%; **300cyc 81%·
  CE 99.64% vs CB-wet 72.7%·99.43%**; SSRM 300cyc 저항 CB-wet 6.62 vs SWCNT-dry 0.6 GΩ; rock-salt CB-wet ~9
  vs SWCNT-dry ~2–4 nm; 급속충전 3C **80% SOC 20분(SWCNT-dry) vs 30분(CB-wet)**, CC-mode SOC 92 vs 65%;
  **10 Ah pouch VED 945 Wh/L · GED 315 Wh/kg**(Table S10; +33% vs conventional @3C), **78%@500cyc**.
- **우리 모델 매핑 (★★ 우리 voxel CBD 발견의 EXPERIMENTAL PROOF — 전자+이온 두 축; 수치 σ 앵커는 Bazzoun/Varkey/Minnmann):**
  - **(a) ✅✅ 전자축 증명:** #275 서론 **"conventional additives… fail to form continuous networks"** =
    우리 carbon-only **σ=0**(discrete carbon 6-7% 셀 ≪ 31% 3D 퍼콜 threshold → 두꺼운 전극 self-percolate
    불가, gap-filler). #275는 정확히 이걸 **continuous SWCNT sheath**로 해결(Fig 2C CB-wet 10→40 Ω·cm+균열 vs
    SWCNT-dry 5–10; KPFM 균일 SOC) → **우리 전자 발견의 실험적 증명**(시뮬 artifact 아님 = 두꺼운 전극 실제 제약).
  - **(b) ✅✅ 이온축 증명:** #275 서론 **"obstruct ion-transport channels"** = 우리 **SuperP σ_ionic
    0.0168 < VGCF 0.0298(1.8× blocking)**. #275는 도전재를 표면통합해 채널을 비움(digital-twin closed pore
    2×·τ2.31·D_eff 2.5×·농도구배 큼) → **우리 이온 발견의 실험적 증명**(주체 다름: 그들 전해질기공 vs 우리 SE망,
    물리방향 동일=discrete가 이온채널 막음).
  - **(c) ★ 제3 morphology(미모델):** SWCNT **conformal sheath(surface-conformal, vein-like)** = 우리
    SuperP(분산점)도 VGCF(interstitial 섬유)도 아닌 **제3 morphology** — 두꺼운 전극의 실제 승자(우리 1 wt%
    SuperP/VGCF는 둘 다 gap-filler, 945 Wh/L 못 줌). → 우리 SuperP-vs-VGCF 결론은 **interstitial/distributed
    한정**(정직한 한계); ★ **`additives.py`에 `surface_conformal`(AM 표면 voxel 도전상 코팅) future 옵션** 추가
    → voxel σ_e가 두꺼운 전극서 percolate하는지 + LPSCl SE 이온접촉 trade-off 테스트.
  - **(d) ★ digital twin = 우리 voxel/Phase-4 blueprint:** GeoDict effective(τ/D_eff 2.5×/closed pore/PNM) +
    1D 전기화학(2.15%) = 우리 voxel FV(σ)+PyBaMM(#281/#286 동일 도구). ★ 이식: **(i) voxel FV에 확산모드 →
    D_eff/τ 출력**(그들 2.5× ↔ 우리 contact-network τ frame[4] 교차검증; #281 DiffuDict); **(ii) PNM pore-side
    지표**(기공 CN·connectivity·closed pore = 우리 dead-SE 고립채널 기공판).
  - **우리 우위:** 그들은 **post-mortem 측정(SSRM/KPFM/EELS) + digital-twin(고정 토모 미세구조)**; 우리 DEM+MPM은
    **압력→미세구조→σ triad 예측 + 소성 morphology + voxel FV로 carbon σ_e gain·σ_ionic blocking mechanistic
    정량(그들 digital-twin의 인과버전)**. frame[5] 분업 재확인(그들엔 입자스케일 압축예측·접촉 σ triad·소성 없음).
    ⚠ **#284와 혼동 금지:** #275 = **morphology(연속 sheath가 discrete를 이김 = 우리 SuperP/VGCF 발견 증명 +
    제3 morphology)**; #284 = **양/두께(탄소↑→전자↑·이온↓, 중간 최적 = balance curve)** — 서로 보완.

### #286 — Porosity-Gradient Dry-Processed Graphite + Deformable Primer Layer  ★★  ✅ 풀 디제스트 완료
Energy Storage Materials (2026), DOI 10.1016/j.ensm.2026.105331 (ENSM 105331, IF 19.3).  Hyundong Yoo†,
Jaejin Lim† … Yong Min Lee\*, Hansu Kim\* (Hanyang+Yonsei).  ★ **풀 디제스트:**
`docs/lit_yoo2026_porosity_gradient_dry_electrode.md`.
⚠ **소재 = 천연흑연 음극 + 액체전해질(1M LiPF₆ EC/EMC 3:7 +10% FEC) 일반 LIB** — **우리 LPSCl sulfide
ASSB가 아님** → 절대 transport 값 전이불가. 가져올 것은 **설계개념·측정방법·정성추세**(수치 앵커 아님).
- **핵심:** **PL(primer layer) binder 변형성**(PVDF가 가장 무름, 압축/탄성계수 **6.31/15.99 MPa** vs
  PAA·CMC 약 2배)을 선택하면 라미네이션 **비대칭응력 → 자발적 z-porosity 구배**(위 다공·아래 치밀).
  전체 porosity는 같아도(MIP **32.2–33.3%**) z-분포만 다름. **DPE@PVDF-PL = 가장 가파른 구배(top↔bottom
  Δ24.5%p vs WPE 5.6%p)**.
- **검증:** 3D XCT(250 nm) + FIB-SEM 토모(46.52 nm, 800장, CNN 분할) + GeoDict 확산-τ + PNM(MATLAB) +
  BESTmicro 3D 전기화학시뮬.
- **핵심 수치:** tortuosity **PVDF 1.86 < PAA 1.98 < WPE 3.09**(확산시뮬, EIS도 같은 순서); PNM
  coordination number **PVDF 4.20 / PAA 4.44 ≫ WPE 2.94**; connectivity bandwidth 표준편차
  0.1581/0.1309/0.0976(PVDF 장거리연결 최고); **3C 방전 305 vs WPE 258 mAh/g**, 3C CC용량 **80.2 vs 23.3**;
  full-cell 3C CC-SOC **PVDF 27.89% vs WPE 14.31%**; AM↔PL 접촉면적 PVDF +45%(표면높이차 12.1 µm);
  ICE DPE 85–87% < WPE 92.7%(**PTFE 탈불소화** → LiF+비정질탄소, dQ/dV 0.2–0.8 V·XPS).
- **우리 모델 매핑 (★ 방법/설계 청사진 — 수치 앵커는 Bazzoun#가 담당):**
  - **(a) Phase 5 z-layer:** porosity-gradient = 우리 **z-band 합성**(`extract_2d_microstructure.py`
    K=8 stratified, line 668) + tortuosity pore elongation(line 826)의 **published 실증** → Phase 5를
    **band별 다른 porosity 구배**로; 출력에 **"두께방향 porosity(z) 프로파일" + top↔bottom Δ** metric 추가.
  - **(b) tortuosity:** 그들 **EIS 식(1) ↔ 확산시뮬 식(2, ε/τ²·D_e)** 2-방법 교차검증 = 우리 σ_ionic
    C(τ)의 τ(Laplace/Dijkstra) 선택 템플릿(우리는 실측 τ 없음). ⚠ pore-도메인 Bruggeman형 → 폼 차용 금지.
  - **(c) PTFE:** 그들 1D피브릴 pore↑ = 우리 `additives.py` PTFE fibril 형태 반영됨; **탈불소화 ICE손실은
    우리 미모델**(일반 LIB 확장시 ICE 항 후보; ASSB는 관련 낮음).
  - **(d) 토모그래피:** FIB-SEM→GeoDict-τ + PNM(coordination·connectivity matrix)을 우리
    `voxel_conductivity`/`mpm3d`에 이식 — 특히 **pore-side 지표**(우리는 particle-contact CN만) +
    확산-τ↔contact-σ frame[4] 교차검증.
  - **(e) 농도분극:** BESTmicro 3D FVM(BV+Fick, 3C CC-CV 0.005 V cutoff) = 우리 **Phase 4(PyBaMM) 흑연계
    reference workflow**. ⚠ ASSB는 전해질농도분극 대신 SE-network σ가 지배 → 적응 필요.
  - **우리 우위:** 그들은 **post-mortem 고정 미세구조 + 연속체 확산**; 우리 DEM+MPM은 **압력→미세구조→σ
    예측 + 소성 morphology + 접촉 σ triad + fracture**. ⇒ 이상 워크플로 = 우리가 미세구조 생성/예측 →
    그들식 토모-정량 검증 → 그들식 전기화학시뮬로 농도분극 닫기. frame[5] 분업 재확인.

### #284 — Optimized Carbon Coating on SiOx, Balanced Ion/Electron Transport + Uniform Dispersion  ★★  ✅ 풀 디제스트 완료
Journal of Power Sources **689** (2026) 240698 (IF 8.4), DOI 10.1016/j.jpowsour.2026.240698.  Jihwan Oh†,
Seungyeop Choi† … Yong Min Lee\* (Yonsei DTBL + ActRO Corp.).  접수 2026-04-04 / 게재확정 2026-06-10.
MDB 2025 특별호.  ★ **풀 디제스트:** `docs/lit_oh2026_carbon_coating_siox_ion_electron_balance.md`.
⚠ **소재 = SiOx(0<x<2) + 인조흑연 음극 + 액체전해질(1.15 M LiPF₆ EC/EMC 3:7 + 10% FEC) 일반 LIB**,
full-cell 양극 NCM622 — **우리 LPSCl sulfide ASSB가 아님** → 전기화학 절대값(용량·ICE·Rct·rate) 전이불가.
가져올 것은 **이온/전자 trade-off 개념 + 분산 측정법(SSRM/W_adh) + 정성추세**(수치 σ/porosity 앵커 아님 —
Bazzoun/Varkey/Minnmann이 담당).
- **핵심:** **CVD 아세틸렌 탄소코팅 두께(thin/moderate/thick = TGA 0.95/2.91/4.18 wt%)가 이온↔전자 수송
  BALANCE를 지배.** **두꺼운 코팅 → 전자전도↑(연속 도전망) BUT Li⁺ 수송 차단 → Rct↑·분극↑**; **얇은 코팅 →
  전자경로 불충분**; ★ **moderate(~2.91 wt%) = 균형 → 최저 임피던스·최고 rate·최고 cycling.** 또 탄소코팅이
  SiOx **표면에너지를 CBD에 가깝게** 바꿔(γᵖ 21.6→11–14) **SiOx–CBD 상호작용↑ → CBD 균일분산**(bare는 응집).
- **검증:** TEM(코팅두께) + TGA(C wt%) + **SSRM 저항맵(분산)** + OWRK 표면에너지/work-of-adhesion + 유변학 +
  EIS/DCIR/GITT/CV/DRT + SiOx/graphite‖NCM622 full-cell + 48 mAh pouch + SAICAS + post-mortem SEM/XPS.
- **핵심 수치:** TEM thin **~4–5 nm conformal**, thick **조밀**; bulk 전기저항률 bare **0.033 → thin 0.018 →
  moderate 0.013 → thick 0.012 Ω·cm**(moderate≈thick saturate); 계면 전기저항 **1.7→1.0→0.6→0.5 mΩ·cm²**;
  **ICE half 73.6/80.0/81.6/81.5%, full 58.7/69.1/73.1/71.8%**(moderate≈thick saturate); **work-of-adhesion
  (SiOx↔CBD) bare 99.9 → thin 107.3 / moderate 108.6 / thick 107.9 mN/m**(moderate 최고); DCIR·DRT(Z_W·Rct·
  R_SEI) **moderate 최소**(thick은 Rct↑=Li⁺ 차단); 70사이클 후 단면 두께 **bare ~93 vs moderate ~70 µm**;
  **SAICAS cohesive 112.3/129.0/147.0/134.6 N/m, adhesive 120.2/138.5/196.5/149.9 N/m**(moderate 최고).
  조성: SiOx/graphite 음극 80:9:1:5:1.5:5(SiOx:흑연:Super C65T:MWCNT:Na-CMC:SBR), NCM622 양극 96:2:2.
- **우리 모델 매핑 (★ CBD ion/electron trade-off 독립확증 + 분산 측정법 — 수치 σ 앵커는 Bazzoun/Varkey/Minnmann):**
  - **(a) ✅ 이온/전자 trade-off 독립확증:** 그들 "탄소↑→전자↑·이온↓, moderate 균형" = 우리 CBD
    **"SuperP 전자 1.3× win BUT 이온 1.8× blocking(σ_ionic 0.0168 < VGCF 0.0298)"**(`docs/cbd_morphology_roadmap.md`)와
    **동일 ion/electron 긴장**(그들=탄소 양/두께 축, 우리=도전재 종류/분산 축). → 우리 CBD blocking이
    **시뮬 artifact 아닌 일반 trade-off**임을 강화(모델 신뢰도↑, flaw 아님 = trade-off 그림 enrich).
  - **(b) ★ balance point 개념:** 우리 CBD는 **채널별 승자**(SuperP=전자, VGCF=이온)만 보고, **종합 최적
    탄소량(balance optimum)은 미정량**. 그들 **moderate-C 명시적 최적**이 동기 → ★ **탄소 wt% 0.5→4 sweep
    하며 voxel σ_e gain vs σ_ionic loss 동시 plot → 우리 balance curve**(roadmap PENDING 4 wt% 테스트가 시작점).
  - **(c) ★ 분산 측정법 이식:** 그들 **SSRM 저항맵 공간균질도 + W_adh(표면에너지 매칭) + 유변학**. 우리는
    분산을 morphology 근접도로만 봄(균일도 스칼라 無) → **voxel carbon occupancy 변동계수(CV) / nearest-carbon
    거리분포**로 SuperP(분산=낮은 CV) vs VGCF(응집=높은 CV) 단일수치화; **carbon↔SE/AM W_adh**로 우리
    `nucleate_frac`/`surface_frac` 경험치 물리근거화(단 LPSCl 표면에너지 우리 측정 필요).
  - **(d) thick-C 이온차단 = 우리 blocking 방향일치(다른 주체):** 그들 thick=**연속 코팅층 barrier(Rct↑,
    전해질-매개)**, 우리 SuperP=**분산 입자 SE-packing 교란(σ_ionic↓)** → 방향 동일, 주체 다름.
  - **우리 우위:** 그들은 **post-mortem 측정(고정 구조)**; 우리 DEM+MPM은 **압력→미세구조→σ triad 예측 +
    소성 morphology + voxel FV(carbon σ_e gain·σ_ionic blocking mechanistic 정량 = 그들 SSRM의 인과버전)**.
    frame[5] 분업 재확인(그들엔 입자스케일 예측·접촉 σ 없음). ⚠ 절대 전기화학값(Rct·ICE) 전이불가(액체/음극).

### #264 — Multi-Faceted Binder via Thiol-Ene Click, Low-Pressure-Operable ASSB  ★★ TIER-2 (우리 소재계지만 BINDER 화학)  ✅ 풀 디제스트 완료
Advanced Functional Materials **36** (2026) e16017 (Open Access, IF 19.9).  Young Joon Park, Kyu Tae Kim …
**Yong Min Lee**(공저), … **Yoon Seok Jung\***(교신, Yonsei) + DGIST + LG Energy Solution.
DOI 10.1002/adfm.202516017.  접수 2025-06-23 / online 2026-01-28.  ★ **풀 디제스트:**
`docs/lit_park2026_thiolene_sbr_binder_assb.md`.
★ **소재 = Li₆PS₅Cl(LPSCl) + 단결정 NCM, ASSB = 우리 소재계**(#271/Bazzoun과 동일).  **그러나 주제 =
BINDER 화학** → **TIER-2**(σ/porosity 절대 앵커 아님; 관련도 = 중간, binder-mechanics 레버 중심).
⚠ **#271(Hong S-B, σ 절대 앵커)과 역할 다름** — 혼동 금지(#264=Park/Jung/SBR-wet/물리만 전이,
#271=Hong/PTFE·NBR/수치 전이).
- **핵심:** **SBR(슬러리/wet 바인더)를 thiol-ene click으로 두 갈래 개질** — (i) **3MPA grafting**(COOH →
  접착↑) (ii) **TMPT cross-linking**(삼관능 thiol → 3D 망 → modulus·탄성↑).  ★ **"가교(modulus)가 접착보다
  저압 성능에 훨씬 결정적".**  in-situ click(전구체를 슬러리에 함께 넣고 건조 중 반응 → 슬러리 공정성 유지).
  - **검증 수치:** retention **X-SBR(X10) 75% vs SBR 68%** @100cyc; 초기 방전 **163 vs 133 mAh/g**(g-SBR
    138 — 접착 최고지만 marginal); **Young's modulus SBR 0.78 → X6 6.36 → X10 14.31 → X14 23.53 MPa**
    (X10 = 18×; X14는 과가교 agglomeration으로 retention 하락 → **X10 최적, 비단조**); 가교밀도 15.7/19.5/
    25.6 ×10⁻⁵ mol/cm³; **vinyl/trans 1.327→0.914→0.854**(thiol이 vinyl 우선 반응); SAICAS g-SBR 389(@계면)
    /peel 150 N/m(접착 압도); 나노인덴 탄성회복 **X10 66.3 vs SBR 38.2%**; DCIR **X10 92.2 vs SBR 124.5 Ω**;
    OEP ΔP·in-situ XRD·단면 SEM 균열면적 **6→4%**(가교가 NCM 부피변화 delamination 억제); LPSCl 내성(SI
    Note 1) pristine **2.6 → p-xylene 1.6 mS/cm**(공정 안전성, σ 앵커 아님).  **작동압 0.3 MPa**(70 MPa 비교).
- **★ 우리 매핑(정직한 중간 관련도 — binder-mechanics 레버):**
  - **(A) MPM binder-cohesion E3 레버 보강 ★:** "cross-link → modulus↑ → strain 저항 → 전극 무결성" =
    우리 **MPM `--coh`(binder-cohesion, audit E3)**의 물리.  현재 E3는 #271 PTFE(dry) void-억제로 동기 →
    **#264가 SBR(wet) 쪽 동일 결론 추가**(두 입력원 수렴: binder 기계물성/분포 → ASSB 무결성).
  - **(B) cohesion은 "최적점 있는" 항:** X14 과가교→agglomeration→retention↓(비단조) → `--coh`를 단조가
    아닌 **상한/최적 곡선**으로; **바인더 modulus(MPa)는 SE E_eff(1.53 GPa)와 별개 항**으로 분리.
  - **(C) "접착보다 modulus"**: g-SBR(접착 최고) marginal vs X-SBR(modulus) dominant → 우리 `--coh`가
    adhesion 별항보다 cohesion(망 강성) 우선하는 방향 확증.
- ⚠ **비전이/주의:** (a) **SBR=wet/슬러리 공정**(우리 dry PTFE·#271 NBR과 같은 부류, 합성 화학은 우리 물리
  밖); (b) **0.3 MPa = 셀 작동/스택압 ≠ 우리 300 MPa 제조압**(다른 압력 축 — 섞지 말 것; #264 자체도 70 MPa
  고압선에선 바인더 차이 작음); (c) **σ_ionic 절대 앵커 아님**(양극 σ 표 없음 — LPSCl+NCM σ 앵커는 #271/
  Bazzoun 유지); (d) 시간(cycling) 화학-기계 열화 = 우리 단일 스냅샷 밖(Phase 4 후보, #271과 공통 GAP).

### #270 — Ion-Conducting Cavity Filler, In-Situ SEI in Sulfide SE Sheets (ASSB)  ★★
Chemical Engineering Journal 529 (2026) 173036 (IF 12.5).  Minjae Kim†, Yongjun Kwon† … Yong Min Lee.
- **핵심(제목):** sulfide SE sheet의 cavity를 이온전도성 filler로 채워 in-situ SEI.
- **매핑:** sulfide SE sheet + cavity 충전 = 우리 **SE void-fill(MPM)** + SE 퍼콜레이션.  filler가 cavity
  메움 = 우리 SE 조밀화.

### #268 — Calendering-Induced Interfacial Reconfiguration, Li Metal Powder Electrodes  ★★
EES Batteries 2 (2026) 464-474 (Front Inside Cover).  Dongyoon Kang†, Sun Hyu Kim†, Jaejin Lim† … Yong Min Lee.
- **핵심(제목):** **calendering(압연)**이 Li metal powder 전극 계면 재구성 → 전기화학 활성화.
- **매핑:** **calendering = 압축**(우리 MPM/DEM).  압력하 계면 재구성 = 우리 contact-area 진화(Stage-E).

---

## ★ TIER-3 — 주변부 (transport / 기계 / binder)

- **#260** Regularly Arranged Micropore, Li-Ion Transport in SiOx/Graphite — *Nano-Micro Letters* 18(75) (IF 38.5).
  정렬된 micropore → 효율 수송 = 우리 porosity/tortuosity → σ_ionic; ordered vs random pore = 패킹.
- **#283** Primer Layer Design, Dry Electrode-CC Interfaces — *ACS Energy Letters* (IF 17.5).  dry 전극 접착/계면(주변부).
- **#267** Surface/Interfacial Cutting, Adhesive Strength Measurement — *J. Energy Storage* 150 (IF 10.7).
  접착강도 = 우리 binder/cohesion(--coh) 측정법.
- **#282** Charge-Engineered Cellulose Nanofibril Binders, PFAS-free High-Loading — *Nature Communications* (2026),
  DOI 10.1038/s41467-026-73909-0 (Open Access).  Sang-Woo Kim†, Nag-Young Kim† … **Yong Min Lee(공저)** …
  Won Bo Lee\*(SNU), Sang-Young Lee\*(Yonsei) + UNIST.  ✅ **풀 디제스트:** `docs/lit_kim2026_charge_engineered_cnf_binder.md`.
  ⚠ **LEAD = Sang-Young Lee + Won Bo Lee + UNIST; Yong Min Lee는 공저자(주도 아님)** → DTBL 핵심(#266/#285/#286)보다 협업·주변부.
  - **핵심:** 목재 유래 셀룰로오스 나노피브릴을 **4급 암모늄(−N(CH₃)₃⁺)으로 양이온화(c-CNF, ζ +31.9 mV·DS 0.39·직경 38 nm)** →
    슬러리에서 **정전기 반발로 분산 안정화** + 건조 후 **강한 수소결합으로 접착·구조 무결성** → **PFAS(PVDF)·NMP 없이**
    초고로딩 **113 mg/cm²·밀도 3.65 g/cm³·면적용량 22.5 mAh/cm²·1781.5 Wh/L·431.8 Wh/kg**(바인더 1 wt%) NCM811 양극.
    PVDF 대비: t_Li+ **0.83 vs 0.54**, 토르투오시티 **3.6 vs 6.8**, 접착일(Fowkes) 활물질/도전재 **107.1/103.6 vs 78.40/77.56 mN/m**,
    peel 접착 **157.3 vs 14.2 N/m**, 전극전도도 0.23 vs 0.16 S/cm, 흑연‖NCM811 300cyc **88% vs 80%**.
  - **DFT:** **VASP GGA-PBE PAW(cutoff 450 eV)** — MEP/ESP 맵(c-CNF 양전하) + 결합에너지(−OH···−OH **−0.64 eV** ≈ 10× PVDF −F···H− −0.07;
    MD Al₂O₃ 슬랩 c-CNF **−1204.8 vs** PVDF **−530.26 kJ/mol**) + 음이온 교환(TFSI⁻ MEP −0.025 Ha/e·ΔG −46.7 kJ/mol → PF6⁻ 자발 치환).
    보충데이터 16종 = Gaussian-cube SCF density/ESP(PVDF/b-CNF/c-CNF/TFSI/PF6/Cl).
  - **우리 모델 매핑 (★ TIER-3 / 주변부 — 모델 영향 0):** ⚠ **분자스케일 바인더 화학 + 액체전해질 NCM811 LIB** —
    우리 LPSCl sulfide ASSB의 연속체/접촉망 DEM+MPM과 소재·스케일·물리 모두 다름.  접점은 **맥락 3가지뿐**:
    (a) **PFAS-free 바인더 = 우리 additives.py가 기하로만 모델하는 PTFE(역시 PFAS)의 대안 맥락**(바인더 화학 미모델);
    (b) **전하→분산 개념이 우리 CBD 분산균일도(E2)에 개념적 인접**하나 메커니즘 다름(분자 표면전하/DLVO vs 기하 seeding) → 수치 전이 無;
    (c) **고로딩 양극 맥락**(단 그들 한계=Peclet 수직분리·전해질 침투는 ASSB엔 없음).  ✗ **transport/압축/σ 앵커 아님**(Bazzoun/Varkey/Minnmann/#266 담당).
    ✗ **#284와 혼동 금지** — 이건 바인더 교체(c-CNF가 분산·접착·t_Li+·전도 all-win)이라 우리 SuperP-vs-VGCF **ion/electron trade-off와 대응 안 됨**
    (그 trade-off 확증·분산정량법은 #284가 공급).  ✗ 그들 DFT=분자 MEP, 우리 DFT-DEM=입자스케일 → 스케일 달라 상보 아님.  **TIER-3 유지.**

---

## ★ 보충 / FRAMEWORK 리뷰 (#260-286 리스트에 번호 없음 — supplementary references)

> 이 그룹의 **peer-reviewed가 아닌 리뷰/매거진 글**(또는 리스트 외 framework 자료).  **수치 앵커가 아니라
> TAXONOMY/positioning 공급원**.  번호를 부여하지 않고 제목으로 파일링.

### (보충) E.Chem Magazine 2024 digital-twin review — 디지털 트윈 모델링·시뮬레이션 (한국어 총설)  ★★★(positioning NAMING)  ✅ 풀 디제스트 완료
**E.Chem 매거진(전기화학 매거진) Vol. 16, No. 1 (2024), pp. 20-37** — "디지털 트윈 모델링과 시뮬레이션: 배터리
연구를 위한 새로운 분석 및 설계 도구."  최준혁·임재진·정승원·홍낙휘·김수환·**이효빈(Hyobin Lee)**·박주남·**이용민
(Yong Min Lee)\***(연세대 배터리공학·화공생명 = DTBL + DGIST + LG에너지솔루션).  ★ **풀 디제스트:**
`docs/lit_choi2024_digital_twin_review_echem.md`.
⚠ **동료심사 저널 논문 아님(일반총설/Korean popular-science review) → #260-286 리스트에 번호 없음 → 번호 안 매김.**
⚠ **수치 앵커 아님** — LPSCl σ/porosity 절대 앵커는 Bazzoun/Varkey/Minnmann/#266.  **유일한 가치 = TAXONOMY/
positioning**(top-down/bottom-up · multi-scale · 미세구조 descriptor 어휘 · DTP/DTI).
- **★★ 결정적:** 본문 Fig 1b/2d/3/4e/5/6/7 전부 **"[Ref 127 재구성 ⓒ 2024 ACS]"** = **S. Kim, H. Lee, J. Lim,
  J. Park, Y. M. Lee, _ACS Energy Lett._ 2024, 9, 5225-5239**(DOI 10.1021/acsenergylett.4c01931).  ⇒ **이 한국어
  총설 = 그룹 자신의 ACS EL 2024 도구논문(이효빈·임재진 공저 = DTBL 모델러)의 한국어 확장판** → top-down/bottom-up
  분류는 **우리가 비교/이식하는 바로 그 그룹의 자기 방법론 진술**(positioning 최강 근거).  ⚠ peer-review 인용은
  이 총설 대신 **ACS EL 원본(Ref 127)을 쓰는 게 안전** — 후속 디제스트 후보.
- **핵심:** (1) **atom→particle→electrode→cell→pack** multi-scale 지도(Fig 1a; electrode 스케일 도구 = **DEM·FVM**
  명시 = 우리 위치); (2) 미세구조 **5요소 descriptor**(Fig 1b: AM size/shape/orientation/coating/**crack** · 도전재
  shape/distribution/**connection** · binder shape/distribution/**surface coverage** · 전극 **contact area/porosity/
  tortuosity/pore network**/homogeneity · separator); (3) **DTP(설계측)/DTI(물리연결측)**; (4) ★ **하향식(top-down/
  reconstruction: XCT/FIB-SEM 측정구조 재구성) vs 상향식(bottom-up/formation: 설계파라미터→DEM/FVM/확률생성)**(Fig 3,
  LPSCl+NCM 70wt% 예시!); (5) 구조-해상 분석(Fig 4: connectivity·SE void·contact loss; SW Avizo/GeoDict/TauFactor/
  Fiji); (6) 다중물리(Fig 5: 압축 변위·von Mises·발열); (7) AI surrogate(Fig 6a 100×) + 압연 DEM 공정모델(Fig 6c
  압축-spring back-접촉/τ) + 동적 시뮬 전망(Fig 7).
- **★ positioning(이 리뷰의 핵심 활용):** **top-down(reconstruction)/bottom-up(formation) 분류 = `positioning_vs_
  geodict.md`의 "GeoDict=구조-given 특성화 / 우리=공정→구조 예측"과 정확히 동일.**  ⇒ 우리 DEM+MPM = **bottom-up/
  formation**(리뷰가 DEM·FVM을 그 도구로 명시; 우리는 그 중 process-physics-driven 하위유형 = 확률배치 아닌 압축역학);
  GeoDict 논문(#266/#271/#281/#284/#286/#275) = **top-down/reconstruction**.  **Fig 1b descriptor(crack/connection/
  surface coverage/contact area/porosity/tortuosity/pore network/dead particle) = 우리 출력(fracture/percolation/
  coverage/StageE/porosity/τ/dead-SE) 1:1.**  리뷰=DESCRIPTIVE(방법론 survey), 우리=PREDICTIVE(압력→미세구조→σ) →
  우리 = framework의 정량 엔진.  우리 고유 edge = granular constriction σ(Kirchhoff/Holm, 연속체 voxel FV가 놓침).
- **★ honest gap:** top-down 재구성(우리는 bottom-up 전용 — GeoDict/토모 담당, frame[5]); 입자 orientation/coating
  (우리 등방 구); **spring-back(Fig 6c)/동적 균열(Fig 7b)**(우리 rate-independent J2 미구현, #285 한계); delamination
  (bulk RVE만, #276 §3.3 gap); LBM 유동/SEI(ASSB 관련 낮음).
- **★ #276과 구별:** **#276(Nam 2026, Mater. Horiz.) = DPE 공정 taxonomy**(4단계 mixing/kneading/laminating/
  **calendering**=압축); **이 리뷰 = 디지털 트윈 방법론 taxonomy**(top-down/bottom-up).  교차인용 — 공정(#276) ×
  방법론(이 리뷰)의 교차점에 우리 작업.  cross-link: `lit_nam2026_dpe_microstructure_review.md` + `positioning_vs_
  geodict.md`.
- **ACTION:** intro/significance에서 top-down/bottom-up을 **Choi 2024 / Ref 127(Kim 2024 ACS EL)** 인용으로 명시
  ("우리=bottom-up/formation process-physics-driven, GeoDict 논문=top-down/reconstruction"); Fig 1a electrode
  스케일에 우리 배치(E softening 정당화); Fig 1b descriptor 어휘 채택; 우리를 DTP로 명명.

---

## · TIER-4 — 타 화학계 (카탈로그만; 우리 모델 직접 관련 낮음)

| # | 제목(요약) | 저널 | 비고 |
|---|---|---|---|
| 280 | 탄성 Li metal anode — 나노-크럼플+마이크로-오목 PDMS 집전체 + 친리튬 TREN SAM (LEAD=Cho/Ko/Back, **Y.M.Lee 공저**). E_host 31.4 MPa·핵생성 124.5→11.0 mV·대칭 ~2,600 h@1/1·~2,100 h@3/3·LFP 90.2%@1,000(1C). 음극 도금 계면공학+액체 LFP → 모델 영향 0; 응력완화 테마만 MPM/#285에 먼 인접. 디제스트 `docs/lit_choi2026_elastomeric_li_metal_anode.md` | Adv. Energy Mater. (25.5) | Li metal anode |
| 279 | 전자-이온 폴리머 복합막(EIPC=GO+PAA 8:2·~1.5µm) + PCET로 Zn 음극 안정화 (LEAD=Song/Seo/Kwak, **Y.M.Lee 공저**). DOD ≈51%·calendar 300 h·CE 99.70%@3000·MnO₂ 파우치 N/P 0.74·DOD ≈85%·25.8 mg cm⁻²; t_Zn²⁺ 0.82·탈용매 E_a 28.23→9.44 kJ mol⁻¹·I_corr 1.85→0.47·002 I-ratio 0.42→1.13·Zn²⁺흡착 −6.23→−7.42 eV. 수계 Zn²⁺ **음극** 코팅막·PCET·탈용매 → 모델 영향 0; "전자-이온"=음극막 혼합전도(우리 양극 σ_e/σ_ionic triad 아님, 동음이의). 디제스트 `docs/lit_cho2026_eipc_zn_anode_azib.md` | Energy Storage Mater. (19.3) | Zn-ion |
| 278 | Na 층상 cathode, Bi 치환 공기·수분 안정화 | Chem. Eng. J. (12.5) | Na cathode |
| 277 | Dual-layer anode 보호, lean-electrolyte Li-S | J. Energy Storage (10.7) | Li-S |
| 274 | High-Ni cathode, 수분응답 dehumidifying separator | ACS Nano (17.3) | separator/High-Ni |
| 273 | 초박막 세라믹(Al₂O₃ ~22.7 nm RF 스퍼터, 바인더-free) 코팅 건식 이축연신 PP 분리막(C-DB-PP) — 이온수송↔내부단락 균형 (LEAD=**Y.M.Lee 교신**). DB-PP porosity 64%·σ_ionic 0.982 → C-DB-PP 1.254 mS/cm(+27.7%)·접촉각 103.5→80.7°·전해질흡수 92.8→145%·열수축유지 88.8→95.1%·T_sc 46→77 h(+67.4%, 이론 331)·Li‖NCM622 >70%@600cyc(DB-PP는 400cyc 급락). 분리막 막공학+액체 Li metal LIB → 모델 영향 0; porosity-tortuosity→이온수송 정성물리만 우리 σ_ionic C(τ)에 먼 인접(연신-고분자막 다공 ≠ 입상 압축양극 다공). 디제스트 `docs/lit_park2026_ceramic_pp_separator.md` | Chem. Eng. J. (12.5) | separator |
| 272 | Passivation 불균일 제거, Li/Zn/Mg 도금 | Chem (19.1) | metal plating |
| 269 | Stepwise activation Zn 증착, flowless Zn-Br | Small (11.8) | Zn-Br |
| 265 | Nb-doped Ni-rich multiphase cathode 소재 | Nature Nanotech. (37.5) | cathode 소재 |
| 261 | 2D polymeric metal phthalocyanine, Li metal full cell | eScience (52.9) | 2D 소재 |

---

## ⇒ 우리 모델에 넣을 인사이트 — 실행 우선순위

| 순위 | 논문 | 인사이트 | 우리 모델 hook | 상태 |
|---|---|---|---|---|
| 1 | #266 | bimodal P:S 7:3 → tortuosity↓ → σ↑, 87.8%@200cyc | **P:S 7:3 production + Furnas dip 실험 앵커** | PDF로 수치 추출 → validation corpus |
| 2 | #263 | 2D param → stochastic 3D → transport 예측 | **Phase 4-5 합성 published blueprint** | 방법 비교/이식 |
| 2.5 | #281 | 미세구조→GeoDict effective→1D 전기화학(COMSOL)→방전; 구조변수 decouple | **★ Phase 4 결합 blueprint(=우리 voxel FV→PyBaMM) + DiffuDict(유효 D_eff/τ) 이식 + predictor decouple** | ✅ 풀 디제스트 (`lit_kim2026_...md`); ⚠Li-O₂ 외래→METHODOLOGY만, 수치앵커 아님 |
| 3 | #271 | ★ LPSCl+NCM ASSB σ_ionic(Pwd 0.087/PTFE 0.064/NBR 0.042) + PTFE void↓(22.3 vs 28.7 vol%) + GeoDict reconstruct | **★ σ_ionic 절대 검증 앵커(Bazzoun에 이은 2번째 같은-소재계, audit #1 다점화) + PTFE 양의 역학효과(audit #5) + positioning 재확인** | ✅ 풀 디제스트 (`lit_hong2026_sulfide_cathode_binder_digitaltwin.md`); ★ 우리 소재계 → 수치 전이됨 |
| 4 | #285 | 단결정=견고→압축이 CBD로; CBD 점탄성→시간의존 spring-back; HT 억제 | **(✅)rigid-AM 검증 + (❗)점탄성 spring-back 미구현 한계** | ✅ 풀 디제스트 (`lit_hong2026_...md`); ⚠단결정NCMA/액체→역학만 전이 |
| 5 | #286 | porosity 구배(z) + 토모 정량(τ/PNM) + 전기화학시뮬 | **Phase 5 z-layer + 토모 방법 이식 + Phase 4 workflow** | ✅ 풀 디제스트 (`lit_yoo2026_...md`); ⚠흑연/액체→방법·개념만, 수치앵커 아님 |
| 5.7 | #276 | **DPE 4단계 taxonomy + 미세구조 5특징 + 양방향 material↔process interplay (리뷰)** | **★ 우리 DEM+MPM 전체의 FRAMEWORK/POSITIONING — 5특징↔우리출력 1:1; calendering=압축; descriptive↔우리 predictive 엔진** | ✅ 풀 디제스트 (`lit_nam2026_...md`); ⚠일반 Li-ion DPE 리뷰→framework/positioning 앵커(수치 앵커 아님) |
| 5.8 | (보충) E.Chem 2024 digital-twin review (=Ref 127 ACS EL 2024 한국어판) | **★ top-down(reconstruction) vs bottom-up(formation) 분류 + atom→pack multi-scale + Fig 1b descriptor + DTP/DTI** | **★★★ positioning NAMING — 우리=bottom-up/formation(process-physics), GeoDict 논문=top-down/reconstruction; Fig 1b descriptor↔우리출력 1:1; positioning_vs_geodict.md 정당화** | ✅ 풀 디제스트 (`lit_choi2024_digital_twin_review_echem.md`); ⚠peer-review 아닌 총설→번호 없음, framework/positioning 앵커(수치 앵커 아님) |
| 5.5 | #284 | 탄소코팅↑→전자↑·이온↓, moderate 균형; SSRM/W_adh 분산정량 | **CBD ion/electron trade-off 독립확증 + balance curve sweep + 분산 균일도 metric** | ✅ 풀 디제스트 (`lit_oh2026_...md`); ⚠SiOx흑연/액체→개념·방법만, 수치앵커 아님 |
| 6 | #275 | 연속 SWCNT sheath, thick 전극; "discrete 도전재 연속망 실패 + 이온채널 막음" | **★★ 우리 voxel CBD 발견(전자 σ=0 퍼콜 + 이온 1.8× blocking)의 EXPERIMENTAL PROOF + 제3 morphology(conformal sheath) + digital-twin(D_eff/PNM) blueprint** | ✅ 풀 디제스트 (`lit_koo2026_...md`); ⚠NCMA/흑연/액체 dry→morphology 물리만, 수치앵커 아님 |
| 7 | #262 | FIB-SEM 3D + 결합 chemo-mech, 응력 파괴 | digital-twin 프레임 + fracture | Phase 4 연결 |
| 8 | #264 | SBR thiol-ene 개질(접착 grafting + 가교 cross-linking); "가교 modulus가 접착보다 저압 무결성에 결정적"(retention 75 vs 68%, modulus 0.78→14.31 MPa 18×) | **★ MPM binder-cohesion E3 레버 보강(modulus→무결성, #271 PTFE와 쌍둥이 근거); cohesion 최적/상한·바인더≠SE modulus** | ✅ 풀 디제스트 (`lit_park2026_...md`); ⚠우리 소재계나 binder-화학·SBR=wet·0.3 MPa 작동압≠300 MPa 제조압 → 물리만 전이, σ/porosity 앵커 아님 |
| 8b | #268/#270 | calendering(압연) 계면 재구성 / SE cavity 이온전도 filler | 압축·압력 축 + SE void-fill | 맥락 인용 |

**다음 단계:** 위 #266/#263/#271/#285/#262 PDF를 받으면 각각 `docs/lit_<author>2026_<topic>.md`로
litdb-curator 풀 디제스트(수치·그림·방법 전체) → comparison_vs_ours에 우리 DEM+MPM과 1:1 비교 추가.
PDF 없이도 위 인덱스·매핑은 즉시 우리 로드맵(Phase 1-5)·CLAUDE.md 서사에 반영 가능.

**출처(검증):** [#271 Yonsei Pure](https://yonsei.elsevierpure.com/en/publications/unveiling-degradation-mechanisms-of-sulfide-based-composite-catho/) ·
[#263 AEM](https://advanced.onlinelibrary.wiley.com/doi/10.1002/aenm.70730) ·
[#266 ACS EL](https://pubs.acs.org/doi/10.1021/acsenergylett.5c03923) ·
[#262 Small](https://onlinelibrary.wiley.com/doi/10.1002/smll.202507883) ·
[#276 Mater. Horiz.](https://pubs.rsc.org/en/content/articlelanding/2026/mh/d5mh02484f) ·
[#264 AFM](https://advanced.onlinelibrary.wiley.com/doi/10.1002/adfm.202516017)

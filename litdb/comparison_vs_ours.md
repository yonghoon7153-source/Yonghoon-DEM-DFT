# 🔬 문헌 ↔ 우리 DEM+MPM — 차이 + 적용 인사이트

> 기준값: `our_dem_baseline.md`. 각 축마다 "문헌이 뭐라 하나 / 우리가 뭐라 하나 / 왜 다른가 / 어떻게 쓰나".
> 현재 digest: Varkey2026·So2021·Martin-Bouvard2003·Bouvard2000(압밀), Bazzoun2026(전달),
> McGeary1961(패킹), **Lee2025·Minnmann2021 JES·Doux2020·Cronau2021(실험 앵커 — 우리 NCM/LPSCl 소재계)**,
> **★ Bielefeld2019(우리와 가장 가까운 *구조-모델링 peer* — GeoDict stochastic-placement percolation, Janek 그룹)**,
> **★ Bielefeld2020(=2019의 *σ-추가 후속편*, 같은 1저자·GeoDict — flux-PDE 연속체 σ_eff,ion+τ²+바인더 영향; ⚠위시리스트 "2022"=오기, 실제 2020)**.
> elasto-plastic 종합 = `elasto_plastic_feasibility.md`. ★ **Minnmann 2021 JES = 우리 porosity/σ_ion/τ 앵커의
> 진짜 출처** (digest `docs/lit_minnmann2021_jes_charge_transport_bottlenecks.md`; 2022 Perspective 아님).
>
> ★ **Stack-pressure 3종 압력 구분 (Doux2020 + Cronau2021 + Minnmann2021):** **제조압(fab ~300–490 MPa)**
> = 압밀/porosity/Heckel(우리 300, Heckel P_y 138) ≠ **측정/작동압(stack ~5–70 MPa)** = 계면접촉/creep/σ-측정
> (Doux 5 MPa 최적 / Minnmann 측정 40 / Cronau sputter 5–10). Doux digest `docs/lit_doux2020_stack_pressure_assb.md`,
> Cronau `docs/lit_cronau2021_stack_pressure_ionic_conductivity.md`.
>
> ★ **Lee2025 (Nat. Commun. 2025, UCSD+LGES)** 는 유일하게 **우리와 완전히 같은 소재계**(LPSCl + NCM811/82 +
> **VGCF + PTFE** 둘 다)의 **순수 실험** 막 논문 → 시뮬 경쟁 아니라 **frame[4] 외부 실험 앵커**.  세 곳에 매핑:
> (B) PTFE% σ 페널티 + 조성별 σ 실측 = 우리 σ_e/σ_ionic·Stage-2 보정/검증; (C) binder-VGCF fibril망 = 우리 CBD
> morphology 모델 검증 + PC/SC-NCM 균열 = 우리 AM 파괴 검증.  데이터 `docs/data/lee2025_transport_anchors.csv`.

## A. 압밀 / porosity (E_SE 강성이 floor를 정한다)
- 문헌: Varkey(halide E=10.58) separator floor **21 %** / cathode **37 %** @350 MPa (강체 구, <20 % "추구 안 함").
- 우리: LPSCl pure-SE **~10 %** @300, real_14 **15.6 %** — 같은 압력 **약 2× 더 치밀**.
- ★ **porosity 앵커 출처 확정(Minnmann 2021 JES PDF 직접 확인, digest `docs/lit_minnmann2021_jes_charge_transport_bottlenecks.md`):**
  "Minnmann porosity 14 %/13–17 %"는 **Minnmann *2022* AEM Perspective가 아니라 Minnmann *2021* JES 040537**
  (NCM622+LPSCl, **압밀 380 MPa**, EIS-TLM **측정 40 MPa**; **복합 양극** avg 14 %, range 13–17 % @Table SIII,
  σ_ion,eff **0.17 mS/cm @ 42 vol% NCM**, **τ_ion 2.07 = √(tortuosity factor τ²=4.3)**)에서 옴 — **세 앵커
  전부 PDF 본문 stated 확인**. ⚠ **τ vs τ² 구분**: 논문 Fig 2b 세로축 = τ²(=σ_0·φ/σ_eff, Eq 4 = 우리
  τ_Laplace,eff 정의); 우리 2.07 = √(τ²=4.3). 인용 시 "τ_ion 2.07 (=√(τ²=4.3))" 병기. ⚠ 이 14 %는 **복합
  양극** porosity지 **pure-SE 아님**(이 논문은 pure-SE를 측정 안 함). **밀도 87 %@300 MPa = Sakuda 2013**
  (75Li₂S-25P₂S₅). **pure-SE 10 % = 우리 MPM 3D(σ_y 0.30) 보정 수렴값**(2021 JES/Sakuda cold-press 거동 위).
  2022 Perspective는 **porosity 수치 0개(전부 정성)** — 수치 cite 시 *반드시* 2021 JES/Sakuda를.
  (+ refs.bib @Minnmann2021이 엉뚱한 040502/abf3a3 가리킴 → **040537/abf8d7** 정정.) ⇒ 압력 **3종 구분 필수**:
  우리 **300 MPa = 제조(cold-press)** ≈ 그들 압밀 380 MPa; 그들 σ/cycling 측정 = **40 MPa**; 작동은 수~수십 MPa.
- 왜 다른가: (a) halide E가 우리 E_eff 1.35보다 ~8× 뻣뻣 → 더 높은 잔류 porosity (우리 MPM E-sweep과 정합);
  (b) 우리 DEM 연화 + MPM 소성 흐름이 강체 구 floor(~20 %) 아래로 도달.
- 인사이트: **우리 porosity 관계식에 E_SE(강성) 항 + 조성 항 필수.** ~20 %는 강체 구 하드 floor.
  Heckel `ln(1/(1−D))=K·P+A` 후보 (우리 R²=0.965, P_y=138). 둘 다 ~100 MPa 탄성→소성 무릎 (= 우리 P_y).
- **So 2021** (LPS+Si, real E=24 + **H-cap** F_th=2/3·H·A_con): 연화 없이 rel.density 0.30→**0.98**@600 MPa →
  **항복캡이 우리 18× 연화 역할**. ⇒ '연화 irreducible'은 강체 구 본질이 아니라 *우리 DEM에 항복캡 없는 탓*
  (`elasto_plastic_feasibility.md`). Varkey '<20% 안 함'도 물리 floor 아닌 계산비용.
- **Bouvard 2000**: 경상↑ → 고압 porosity↑ (Astroloy 0.995→0.86 @0→35 vol% alumina) = 우리 AM↑→porosity↑;
  '온도↑→σ_y↓→압밀↑'은 우리 E_eff 연화의 실험적 정당화. **Martin–Bouvard 2003**: 거시응력이 E₂/E₁=10→100서
  <3% 변화 → **rigid-AM 가정 외부 면허**.
- **★ Doux 2020 (LPSCl + Li-metal, 실험, =우리 SE) — 18 % floor + 제조/작동압 분리**:
  - **LPSCl 펠릿 porosity 18 %** (rel.density 82.1 %, Table S2 80.3–84.9 %) **@370 MPa cold-press** →
    ★ **same-material 실측이 우리 "rigid-sphere ~20 % floor" 를 확증**(압력으로 못 닫는 잔류공극). 우리 pure-SE
    **10 %**(연화+소성)는 *이 18 % 아래로* 도달 → **연화/소성이 floor 를 깬다**는 논증의 직접 대조점.
    `docs/data/{doux2020_stack_pressure,densification_porosity_db}.csv`.
  - **제조압 vs 작동압 분리 (§8 명문장):** "펠릿은 이미 **370 MPa** 로 cold-press 되어 **작동 stack
    pressure(5–75 MPa)의 역학은 단락에 영향 없다**" → **제조압=압밀/porosity/Heckel**, **작동압=계면접촉/creep**
    가 *다른 물리* 임을 실험 분리. ⇒ 우리 **"300 MPa=제조(Heckel P_y=138) vs 작동 수~수십 MPa"** 인식의
    **권위 있는 LPSCl 근거**. Heckel P_y 도 *제조압* 무릎이지 작동압 아님 — 구분 흐려지지 않게 cite.
  - **soft 상이 공극으로 흐른다(거시물리 일치, 단 주체 다름):** Doux = **Li metal** 이 LPSCl 의 *기존* 18 %
    공극으로 creep(Li 항복 0.8 MPa, 작동압이 ~6–100×); 우리 MPM = **SE 입자 자신**의 소성 void-fill. 같은
    *종류*의 물리지만 **상(Li≠SE)이 달라** Doux 가 우리 SE 소성을 *직접* 검증하는 건 아니고 **간접 보강**
    (LPSCl 은 압력민감 soft/다공 시스템). ⚠ over-claim 금지.
  - ⚠ **Li-metal 단락 논문** → 단락시간·용량·dendrite 수치 전사 금지, **SE 압력-역학·porosity 만**.
- **★ Lee 2025 (LPSCl + NCM811 + VGCF + PTFE, 실험, 건식 co-rolling) — 작동압의 *공정-인과* 추가**
  (docs digest `docs/lit_lee2025_corolling_dryprocess_assb.md`; papers digest는 σ·CBD·파괴 owns):
  - **제조압 vs 작동압 *명시 분리*(공정 레벨):** 셀을 **500 MPa 로 press**(pouch CIP 500)하되 **2–5 MPa
    로 cycle** → 우리 **"300 MPa 제조(Heckel P_y 138) ≠ 수~수십 MPa 작동"** 인식의 *공정* 버전. 그들 제조
    500 MPa = 우리 300 MPa cold-press·Doux 370·Minnmann 380·Sakuda >350 과 같은 "수백 MPa 냉간가압" 계열.
  - ★ **작동압의 *인과*: 계면 품질이 작동압 하한을 정한다.** Doux 가 "**5 MPa 최적**"(현상)이라면 Lee 는
    **"co-rolling 으로 robust 융합 계면을 만들면 *2 MPa* 까지 낮춰도 >80 % 500 cyc"**(공정→작동압). 증거 =
    사이클 후 **계면 void-ratio**(SSE 대비, 75→2 MPa): **co-rolled 1.9→3.5**(거의 안 늘음) vs **freestanding
    4.0→15.5**(급증). → "**고압-제작 + 저압-운용**" 실용전략의 LPSCl 직접 실증 (Doux 비가역 이력과 결합).
  - **셀 압력 protocol = 우리 MPM servo/hold:** Supp Fig 25 **fixed gap**(ΔP≈−1.5/cyc) vs **constant
    pressure**(스프링, ΔP≈−0.1) ↔ 우리 **hold**(변위정지) vs **servo**(const-σ). 우리가 scaffold 에서
    servo→over-compact→**hold 채택**한 것과 같은 물리 (저압 장기 cycling 은 const-P 필요) → 우리 protocol
    선택의 실험 정당화. **압력 4종 위치:** 작동 하단 = Lee **2 MPa**(< Doux 5 < Minnmann 측정 40 < Cronau 5–50).
  - ⚠ **정량 압밀 porosity 없음** (void = *사이클 후 계면 void 상대비* ImageJ, 제조 porosity 아님) → 우리
    DEM 15.6 %/MPM 16.7 % 와 **직접 비교 금지**. densification CSV 의 Lee 행은 *압력-구분 컨텍스트*(작동압
    2/75 MPa retention)로만, **porosity 칸 비움**. 제조압도 500 MPa(우리 300 과 다름) → 밀도 절대 동일시 금지.
- **★ Sakuda 2013 (75/80Li₂S·25/20P₂S₅ glass, 실험, 황화물-기계물성 고전) — 우리 두 토대 앵커의 원전**:
  - ★ **E_SE 24 GPa 의 1차 출처**: 초음파 측정 **18–25 GPa** (75Li₂S·25P₂S₅ = **24**, 50Li₂S·50P₂S₅ = 18; 산화물
    50Li₂O·50P₂O₅ = 50 ≈ 2×). → 우리 **real-bulk 22–24** = Sakuda 24 ∩ Bazzoun 22.1(LPSCl). **E_eff 1.35(DEM)/1.53(MPM)
    = 이 24 의 18× 연화 프록시** — Sakuda 가 "real E 가 뻣뻣함"을 *측정*으로 확정 → "1.35 는 임의 아니라 *측정된 24 의
    연화*"라는 frame[2] 논거의 measurement 근거. ⚠ Sakuda 24 = *재료 고유 E*(hot-press 고밀도 펠릿 초음파) → 우리
    **real-bulk 칸에만** 매핑, *압밀-bed* E_eff 와 층위 다름(직접 동일시 금지).
  - ★ **"황화물은 상온 가압만으로 치밀화(room-temperature pressure sintering)" 의 1차 출처**: 산화물 LLZO 는 1000 ℃+
    소결 필요(Fig 1) vs 황화물은 냉간가압만으로 입계 소멸(Fig 2b→d, Fig 3 입자 유합). → 우리 **DEM cold-press @300 +
    MPM 소성 void-fill** 전제의 물리적 정당화. Sakuda SEM(입자 *유합·성장* = 진짜 SHAPE 변화)= 우리 **MPM morphology
    (코어보존+경계평탄화)가 모사하려는 바로 그 현상** → 강체-구 DEM 한계를 *실험이 직접 지적* → MPM 이 메우는 게 옳음(frame[5]).
  - ⚠ **밀도 앵커 PROVENANCE 정정**: 우리 "**87 %@300 MPa (porosity 13 %)**"는 **본문에 stated 되어 있지 않다.** 본문 stated =
    **">90 % @ over 350 MPa"** (porosity <10 %) 뿐. "87 %@300"은 **Fig 2a 곡선 digitized 추세값**(±, 본문에 300 MPa 정밀값
    없음). → cite 시 **"Sakuda Fig2a digitized ~87 %@~300 (TREND); stated >90 %@>350 MPa"**. 소재 = 75Li₂S·25P₂S₅ **glass**
    (≠ LPSCl). 우리 DEM pure-SE 90 % 는 **>350 MPa stated 와 정합**(300 digitized 와도 추세 일치하나 *압력 다름* 주의).
  - **σ-vs-P 무릎(Fig 4)**: 냉간 **0.31** / bulk **0.34 mS/cm** (75Li₂S·25P₂S₅), 70 MPa 서 ~10⁻⁴ 급상승→포화 = Bazzoun
    σ@400 포화 / 우리 Heckel P_y 138 / Doux 접촉@~25 MPa 와 **같은 계열**. ⚠ **σ 절대값(0.31) 전이 금지** — Li₃PS₄ glass σ ≪
    LPSCl(~1–3, ~10×↑), *형태/추세*만.
  - **"three-way agreement" 정직 재서술**: DEM(LPSCl, 300 MPa, ~10/15.6 %) ↔ Minnmann2021(NCM622+LPSCl 복합, 380 MPa,
    13–17 %) ↔ Sakuda(75Li₂S·25P₂S₅ glass, stated >90 %@>350) = **"황화물-유리계가 수백 MPa 냉간가압서 porosity ~10–17 %로
    치밀화"라는 *거동(추세)*의 3중 정합** — *같은 소재·같은 압력의 byte-identical 일치 아님.* Sakuda 기여 = same-family
    거동·E·물리 앵커(절대 porosity 정밀값은 LPSCl 쪽 Minnmann/Doux/우리 DEM 소유). `docs/data/densification_porosity_db.csv`.

## B. 전달 삼중항 — σ_ionic은 교차검증, σ_e/σ_thermal은 우리만
- **★ Minnmann 2021 JES (NCM622+LPSCl, 우리 소재계, EIS-TLM 1차 측정)**: σ_ion,eff **0.17 mS/cm @ 42 vol% NCM**
  (= 우리 DEM σ_ionic 0.04–0.18 상단과 일치!), **τ_ion 2.07 (=√(τ²=4.3))**, σ_el,eff 0.56 (τ_el²=7.4).
  CAM vol% 25–61 스윕: **CAM↑→σ_ion↓ / τ_ion²↑(2.4→15.3)**, **σ_el↑ / τ_el²↓(120→4.3)**, 42 vol% 교차·최적.
  τ_el²=120 @25 vol% = **전자 percolation 실패**(= Park 2020 90 wt% / 우리 σ_e f_p 항). **size: fine SE →
  σ_ion,eff↑ (bulk 1.6→1.2 mS/cm로 오히려↓에도) = packing/τ 효과** — 우리 "size=PACKING not overlap" 정확 일치.
  Eq 4 τ²=σ_0·φ/σ_eff = **우리 τ_Laplace,eff 정의 동일**(단 그들 = constriction 미포함 → 우리 Stage-E가 그
  constriction 포함 → 보정 lever). bulk LPSCl 1.6 mS/cm = 또 하나의 bulk 앵커. → **우리 σ_ionic·τ 의 최강
  same-material 실험 절대 검증점.** (그들 42 vol% NCM → 우리 φ_SE≈58 vol% 매핑 후.)
- 문헌(Bazzoun, **LPSCl 동일소재 + LIGGGHTS 동일코드**): RNM = 우리 Holm/Kirchhoff 그대로
  (R=1/(2σr_c), Σ(φi−φj)/R=0). 실험 σ_eff,ion **0.137/0.101/0.065 mS/cm @ f_CAM 70/75/80** (400 MPa, EIS).
- 우리: 같은 솔버 물리. 추세 일치 — 작은 SE→σ↑, CAM↑→σ↓, 압력↑→σ↑(~400 포화 ≈ 우리 P_y 138).
- 차이: 그들 RNM은 **구속저항만**(field spreading 없음) → 고-CAM서 과소(80 % RNM 0.031 ≪ exp 0.065);
  우리 Stage-E 소성 접촉면적이 이 과소를 일부 보정. 그들은 σ_e/σ_thermal 없음(우리 삼중항 우위).
- 인사이트: **Bazzoun 실험 σ_eff,ion = 우리 σ_ionic의 외부 절대 검증점** (그들 vol% CAM:SE → 우리 φ_SE 매핑 후).
  "missing direct validation"(다중압력 LPSCl σ_ionic) 확보.
- **★ Doux 2020 (LPSCl, 실험) — 접촉-vs-압력 포화 + 비가역 (σ-vs-P 와 같은 계열)**:
  - Li 대칭셀 **임피던스 500→110→50→40→35→32 Ω** (1→5→10→15→20→25 MPa) → **~20–25 MPa 에서 포화**(plateau).
    ★ **압력↑→접촉↑→포화** = 우리 Heckel knee(P_y 138) / Bazzoun σ-포화@400 MPa 와 **같은 계열**의 "압력으로
    접촉 좋아지다 수확체감" 곡선. **단 Doux 는 Li/SE *계면* 접촉저항(Ω)**, 우리·Bazzoun 은 SE/SE *벌크망 σ* →
    **추세만** 비교(절대 직접대조 금지). 다중압력 σ 의 직접 데이터는 Bazzoun(RNM)·Cronau(protocol) 소유.
  - **비가역 이력:** 25→5 MPa release 시 임피던스 **초기 5 MPa 의 절반 이하(110→50 Ω)** 로 유지 → **압밀=비가역
    소성**(우리 MPM 영구변형·overlap 잔류·Heckel 비가역)의 거시 증거. ⇒ "**고압-제작 + 저압-운용**" 실용전략 근거.
  - **bulk LPSCl σ_pellet 2–2.5 mS/cm** (cold-press, GB+공극 포함) = Cronau µC-Br ~2.4 / Lee pristine 2.19 /
    Bazzoun pellet 1.02 / 우리 채택 3.0(단결정-라벨) 사이의 **또 하나의 LPSCl bulk 앵커** (스프레드로만, 절대대조 금지).
- **★ Lee 2025 (LPSCl + NCM811/82 + VGCF + PTFE, 실험)**:
  - **PTFE wt% σ 페널티 곡선** (Supp Fig 5, CAM:SSE:VGCF 80:17:3 고정, 75 MPa):
    PTFE 0.5 / 2 / 5 wt% → **σ_ionic 0.069 / 0.024 / 0.007 mS/cm** AND **σ_e 34 / 4.5 / 0.011 mS/cm** (≈3,000×↓).
    → ★ **우리가 못 갖던 데이터**: 우리 σ_e/σ_ionic 폼은 도전제 *추가*만 반영하고 **바인더가 접촉 막고 절연**하는
    페널티가 없음.  **Stage-2 흡수 1순위** — CBD가 σ_e에 *기여*(VGCF망)하면서 PTFE wt%↑면 **양쪽 다 급감**하는 비단조성.
  - **조성별 절대 σ 실측** (0.5 wt% production 양극): σ_ionic **0.076** (co) / 0.069 (free), σ_e **33–34** (VGCF망) mS/cm
    → 우리 σ_ionic(LOOCV 0.975)·σ_e(0.953) 폼의 추가 외부 절대점 (단 그들 VGCF 3·PTFE 0.5 wt% ≠ 우리 1·1 → 함량 보정 후 매핑).
  - **bulk LPSCl σ_ionic = 2.19 mS/cm** (pristine pellet) / 1.64 (ball-mill <1 µm) → Bazzoun pellet **1.02**·Cronau 단결정
    **3.0** 사이 = **세 번째 LPSCl bulk 앵커** (측정·입자·GB 차이 스프레드로만 사용, 절대 직접대조 금지).
  - 차이/주의: 실험이라 **솔버 없음**(우리 Kirchhoff/Holm·삼중항 σ_i/σ_e/σ_thermal 우위 유지); σ_ionic(SSE) 1.04(co)<1.29(free)는
    압밀 차 아니라 **측정 형상차**(free 500 µm vs co 50 µm) — intrinsic σ 비교 주의.

- **★ Bielefeld 2019 (GeoDict 구조-모델링, Janek 그룹, 우리와 가장 가까운 *구조-모델링 peer*) — percolation 추세는
  교차검증, 단 σ는 *안 풂***  (digest `docs/lit_bielefeld2019_microstructural_modeling_composite_cathodes.md`):
  - **σ 절대값 *미산출*:** 이 논문은 유효 전도도를 *안 푼다* — **percolation 존재 + cluster 부피(utilization) + 기하
    active interface**까지만.  constriction/contact 저항은 **명시적으로 "future work"**(ref 36 = **Greenwood 1966**,
    우리 Holm 1967과 같은 계보).  ⇒ 우리 σ_ionic 0.04–0.18·Bazzoun 0.137 과 **σ 직접 수치 비교 불가** — 비교 가능한 건
    *percolation 임계·utilization·active interface 추세*뿐.  ★ **바로 이 칸(constriction σ)을 우리(+같은 그룹 후속
    Bazzoun RNM)이 채움** = 우리 transport novelty의 정확한 위치.
  - **추세 일치(frame[4] 구조 descriptor):** (i) **고-AM → 이온 한계(AM>79 vol%), 저-AM → 전자 한계(AM<69 vol%),
    중간 좁은 창(69–79 vol%)**(Fig7) = 우리 dead-SE/dead-AM 양끝 + Minnmann 2021 "CAM↑→σ_ion↓·σ_e↑·42 vol% 교차"와
    같은 trade-off; (ii) **작은 입자 → 저-분율 percolation**(Fig5–6) = 우리 size=packing; (iii) **utilization θ_ν=V_c/V_ν**
    = 우리 f_AM^cc/dead-AM; (iv) **β=0.41**(3D site-perc, Fig4) = 우리 √(φ−φc)·φ^4 percolation-backbone 지수 이론 정당화.
  - **흡수할 정량식:** 전자 percolation 임계 **p_c=7.83·ln(d_AM/µm)+36.67 vol%**(Fig6) → 우리 σ_e 입경 의존·dead-AM
    임계와 대조.  **이상 조성 62/38(5%)·66/34(10%)·72/28 vol%(20%)**(=NCM622+LPS 80/82/86 wt%) → 우리 production core
    (AM 70–85 wt%) 상단과 정합 + porosity↑→AM↑ 이동.  데이터 `docs/data/bielefeld2019_percolation_thresholds.csv`.
  - ⚠ **placement(입력 porosity) ≠ 우리 압밀(측정 porosity)** → σ·porosity 절대 동일시 금지, *구조 추세만*.  재료-무관
    (NCM+LPS는 wt% 환산용 예시) → 소재-특이 절대값 끌어오기 금지.

- **★ Bielefeld 2020 (GeoDict flux-PDE σ_eff + 바인더, Janek 그룹) — 2019의 *σ-추가 후속편*; σ는 *연속체*로 풂(constriction
  없음=상한), 바인더-블로킹은 우리 CBD 직접 cross-check** (digest `docs/lit_bielefeld2020_effective_ionic_conductivity_binder.md`,
  CSV `docs/data/bielefeld2020_sigma_binder.csv`; ⚠위시리스트 "2022"=오기, 실제 **2020**):
  - **★ σ-method = 연속체 flux-PDE(EJ-HEAT, ∇·(−σ∇φ)=0, voxel harmonic avg) → point-contact constriction *없음***:
    2019가 "σ=future work(Greenwood)"로 미룬 σ_eff,ion+τ²를 *이 논문이 풀었다* — 단 **SE 상을 연속 매질로** 다뤄
    **SE-SE 점접촉 수렴저항(Holm/Greenwood)을 입자별로 안 푼다**(넣는 건 AM/SE *면*접촉저항 40 Ω·cm²뿐). ⇒ σ_eff,ion =
    **강체-접촉 granular망의 상한(upper bound)** → ★ **우리 Kirchhoff/Holm σ_ionic·Bazzoun RNM σ는 그 아래로 좁힘만큼
    깎인다**(절대 동일시 금지, 우리가 *더하는* 핵심 = constriction). σ-검증은 **Kato재구성 0.68 vs 실측 0.73 mS/cm 1점**
    (LCO+LGPS, NCM811+LPSCl 아님 → 소재 절대전이 금지, 추세/방법만).
  - **추세 일치(frame[4] 구조 descriptor):** (i) **CAM↑→σ_eff,ion↓**(Fig1, 선형) = 우리 σ_ionic + Minnmann2021 + Bazzoun;
    (ii) **porosity↑→σ_eff↓(5% void가 20% void 대비 σ *2×*, Fig4)** = 우리 √φ_eff·porosity-중심 모델링; (iii) **고-AM서
    σ_eff abrupt drop(65:35 초과)** = 우리 dead-SE; (iv) **τ²-vs-조성 2→10** = 우리 τ_Laplace/R_brug.
  - **★ Bruggeman 4× 과소(Fig2, Eq18/19):** 표준 Bruggeman τ²=ε^(−1/2)가 모델 τ²를 *4배* 과소평가, 수정 γ·ε^(−α)는
    α∈[2.02,1.21]·γ∈[0.32,0.67]로 비물리 → ★ **우리 R_brug_over_full_physics(σ_thermal Ridge) 사용·Bruggeman 불신의
    권위 있는 외부 근거**.
  - **입경 효과 = 부호 같되 *채널 반대*(주의):** 그들 **작은 AM→이온 σ_eff↓·τ²↑**(작은 AM=우회 장애물 多) vs 우리·Bazzoun
    **작은 SE→σ↑**(작은 SE=전도체 접촉 多) — **모순 아님**: SE 잘게·AM 굵게 = 이온 최적(같은 그림); + 2019 "작은 AM→전자↑"
    합치면 **작은 AM = 전자↑·이온↓ trade-off**.
  - **★ 바인더(CBD) 영향 = 우리 CBD/voxel σ-블로킹 직접 cross-check** (Fig5, V(B):V(AM)=0.05/0.10, *interfacial meniscus*
    배치): **σ_eff급감 + τ² 4.2→6.4→10(70:30) + active interface −17~43%(저-AM)·−29~82%(고-AM)**. "binder impedes/blocks
    ionic pathways; not all SE particles contribute." = ★ **우리 voxel σ_ionic 블로킹(SuperP 0.0168<VGCF 0.0298 mS/cm,
    SuperP ~1.8× 더 막음)·#271 Hong PTFE(0.087→0.064, −26%)·Lee2025 PTFE(0.069→0.007, −90%)와 同 σ-블로킹 물리.**
    - ⚠ **배치 차이:** 그들 = **AM 표면 interfacial meniscus** → *AM/SE active interface*를 우선 막음(고-AM −82%); 우리
      voxel = *SE 이온망 bulk* 차단. → **interfacial(그들) vs bulk(우리) 배치 비교가 cross-check 거리.**
    - ⚠ **둘 다 *양의 역학효과 없음*:** Bielefeld·우리 voxel 둘 다 바인더를 σ=0 obstacle(전도 차단)로만 봄 → **#271 Hong이
      지적한 PTFE void-억제(28.7→22.3 vol% densification 도움)가 *둘 다* 빠짐** → MPM/DEM 역학에서 보강.
    - ★ **흡수 타깃:** (i) **active interface 손실의 고-AM 비선형성(−43~82%)** → 우리 coverage/A_AM-SE 폼에 바인더 항
      추가 시 고-AM서 더 급감하게; (ii) interfacial vs bulk 배치 RVE 비교; (iii) void-fill 역학효과(Hong).
  - ⚠ **placement(입력 porosity, 2019 계승) ≠ 우리 압밀(측정 porosity)** → σ·porosity 절대 동일시 금지, 추세만; σ-검증계
    **LCO+LGPS**(NCM811+LPSCl 아님) → σ 절대전이 금지; 바인더 morphology = *형상 없는 meniscus*(실제 PTFE fibril/SuperP
    응집 morphology 효과 없음).

## C. 역학 / morphology — MPM 고유 (문헌 DEM은 형상 못 바꿈)
- 문헌: Varkey "elasto-plastic"은 **CONTACT 힘법칙만**(Thornton–Ning), 입자는 완벽 구 — "구=타협,
  현실 형상=향후 과제" 명시. Bazzoun도 구만.
- 우리: MPM 진짜 소성 형상변화(SEM 일치), void-fill flow, Σdg 변형장.
- 왜: 강체 구 DEM·단상 연속체는 granular 재배열을 못 잡아 둘 다 연화 럼핑 필요 (frame [1]/[2]).
- 인사이트: **morphology·소성 floor(<20 %)·변형장 = 우리 MPM이 메우는 간극** (Varkey가 스스로 인정 = frame[5] 확증).
- **Martin–Bouvard 2003** 2-메커니즘 분해: 경상 force-network(K_h≈1.3@20→1.8@40 vol%, N₂₂/N₁₁→3.5) = 우리
  AM load-shielding / 연상 excluded-volume 과변형(+20–40%) = 우리 MPM void-fill → **복합 porosity 관계식 두 항**.
- **So 2021** Fig5–6: Si AM-AM 응력집중(2.5→5.9 GPa, overlap 0.007)·SE-SE는 H_SE 캡 = 우리 real_14 AM-shielding
  (SE overlap 1.75%)을 다른 소재로 독립 재현.
- **★ Lee 2025 (실험) — 우리 MPM/CBD/파괴 모델의 실험 검증 (frame[4])**:
  - **binder-VGCF fibril 망 SEM** (Fig 3h,i + Supp Fig 17/18): 계면을 가로지르는 **꼬불꼬불(squiggle) 곡선 섬유망**이
    VGCF를 그물치고 SSE-전극을 잇는 것을 *실측* + 5단계 fibrillation 모식(접촉→shear 이동→stretched&fibrillated→
    새 접촉→반복).  → ★ **우리 PTFE CBD 모델의 실험 검증** (`docs/cbd_morphology_roadmap.md` batch1: **curl(worm-like) +
    nucleate-on-carbon + shear-draw d∝√(V/L)**) — 우리 시드 모델이 *literature/실험-grounded*임을 직접 인용 가능.
    단 그들은 *막 제조 shear* 공정 — 우리 RVE는 그 공정을 재현 안 함(개념 검증으로만 사용).
  - **PC-NCM 균열 / SC-NCM 무손상** (Fig 2b,c + Supp Fig 6–8, 300→500 MPa서 PC 균열↑·debris): → ★ **우리 DEM
    AM_P(다결정) 파괴(92:8 8mAh서 37–40%)·AM_S rigid 가정의 실험 라이선스** (Auerbach/fracture-Holm 검증점).
    PC는 *진짜로 깨지고* PTFE는 *진짜로 소성 draw* → rigid-sphere 한계를 우리 MPM(형상)·fracture(균열)가 메우는 게 옳다는 실험 근거.
  - **바인더 연화 DMA 67%↓**(30→120 °C, Supp Fig 10) = 우리 E_eff 18× 연화의 *바인더 측* 물리(온도↑→σ_y↓→압밀↑, Bouvard2000과 결 같음).
  - 우리 우위(그들 없음): 정량 porosity·Heckel·coordination·coverage% · MPM 정량 변형장 Σdg·void-fill flow ·
    명시적 접촉망 σ 삼중항.  그들 void는 *사이클 후 계면 void 상대비*(ImageJ)지 압밀 porosity 아님 → 우리 15.6%와 직접 비교 금지.

## D. 패킹 / Furnas dip — DEM·기하 소유, 소성 MPM 불가
- 문헌: Varkey RCP/rigid → dip @ AM 70–80 wt% (de Larrard 기하). Bazzoun 작은 SE→packing↑→σ↑(size=packing).
- 우리: DEM·de Larrard dip @ AM 70–85; **소성 연속체 MPM은 dip 재현 못 함**(material sweep로 증명, frame[4]).
- 인사이트: dip은 초기 강체 구 패킹(기하)에 산다 → DEM(또는 de Larrard)이 소유. porosity-incl-dip은 DEM.
- **McGeary 1961**(Furnas-dip 실험 원전, **소성변형 없음** 명시): 1size 62.5→binary 86(임계비 d_c/d_f≥**7**,
  삼각공극 0.154·d_c)→ternary 90→quaternary 95.1%. 우리 AM:SE 12:1(≫7, dip 깊음)·4:1(<7, 부분충전)이 조성별
  dip 깊이를 McGeary 무릎으로 설명 → **(조성×크기비) 기하항**(E-stiffness 항과 별개) 근거.
- **So 2021** φ_SE^crit=**0.13**(ball-milled aggregate) vs 우리 σ_ionic φc 0.195–0.20(mono) → 응집이 저-φ 침투
  허용 = SE-dispersion 축 후보. **Bouvard 2000** percolation 임계 = f(크기비): 0.32(r=1)→0.18(r=2) = dip의
  rigid-skeleton 기하 기원(alumina inclusion 균열이 하중분담 증거).
- **★ Bielefeld 2019 (구조-모델링) — Furnas dip을 *다루지 않음*(단봉 PSD)**: AM PSD = **uniform 단봉**만;
  **bi/tri-modal은 *향후 과제*로 명시 보류** → 그들 "입경 효과"(Fig5–6)는 단봉 입경 *크기* 효과(작은 입자→저-분율
  percolation)지 *분포* 효과(dip)가 아니다.  ⇒ ★ **dip은 그들이 비운 칸 → 우리 bimodal 12:4:1 + 정량 dip(AM 70–85
  wt%, de Larrard/McGeary)이 채움**.  단 그들 이상 조성(62/38~72/28 vol%)·전자 percolation 임계는 *강체-구 패킹* 산물
  이라 우리 dip의 *조성 위치*와 같은 기하 계보(비교는 추세만).
- **★ Bielefeld 2020 (σ-추가 후속편) — multimodal은 시도하나 *dip 미측정*(porosity 15% 고정)**:
  2020은 **trimodal 1:1:2(de Larrard ideal packing geometry, r_M=(√2−1)r_L·r_S=(√(3/2)−1)r_L) 한 케이스**를 시도하나,
  그 목적은 **이온 tortuosity 저감**(τ²_tri 5.55 < τ²_mono 6.40, vanishing-입경 극한)뿐 — **porosity는 15% 고정**이라
  ★ **porosity-vs-AM% dip(최소)을 *측정하지 않는다*.** ⇒ 우리 bimodal 12:4:1 + 정량 dip(AM 70–85 wt%, de Larrard/
  McGeary)과 비교할 **dip 데이터 없음**(그들 trimodal은 de Larrard *geometry*를 빌리되 *이온 τ* 관점). dip은 여전히
  그들이 비운 칸 → 우리(또는 de Larrard 기하)가 소유. 단 trimodal이 *τ²를 낮춘다*(packing 개선)는 결론은 우리 "bimodal
  packing↑" 방향과 정합.
- **★ Minnmann 2022(설계 Perspective, 정성)**: **tailored(bimodal/multimodal) PSD가 모든 축
  (확산·전자·이온 percolation·계면열화·GB) 최적**(Fig 6 4분면) + **작은 SE + 큰 CAM/SE 비 = 패킹밀도↑**
  (§3.1) → ★ **우리 bimodal 12:4:1 + Furnas dip의 권위 있는 정성 근거**. 단 *dip 위치/깊이는 이 논문에
  없음*(정성 "bimodal이 좋다"까지) → McGeary/de Larrard 기하(우리)가 *정량*을 소유. 우리 차별점 =
  정량 dip(AM 70–85 wt%)을 추가. **CAM 60–70 vol% 최적**(§2.1)이 우리 production core(AM 70–85 wt% ≈
  SE 30–50 % of solid)와 정합.

## E. 우리 계산이 문헌을 "검증/교차검증"하는 지점 (강점으로 쓸 것)
- **★ Minnmann 2021 JES = 우리 porosity·σ_ion·τ 앵커의 1차 출처 + 최강 same-material 실험 검증**:
  σ_ion,eff 0.17 mS/cm @42 vol% NCM ⊂ 우리 DEM σ_ionic 0.04–0.18; 복합 porosity 13–17 % ≈ 우리 real_14 15.6 %;
  τ_ion²(Eq 4) = 우리 τ_Laplace,eff 정의; "fine SE→σ_eff↑ = packing/τ" 결론 일치; utilization(ion+e 둘 다
  연결) = 우리 dead-AM. (frame[4] 외부 실험 앵커 — 같은 NCM/LPSCl 매트릭스.)
- ★ **Bielefeld 2019 = 우리 *구조 파이프라인*의 가장 가까운 peer + 우리 3대 novelty의 정확한 위치를 드러냄**:
  Janek 그룹 자신의 GeoDict 구조-모델링이 (i) 구조를 *랜덤 배치*(우리는 *압축해 예측*), (ii) σ를 *안 풂*(우리는
  Kirchhoff/Holm 삼중항), (iii) *단봉 입경*(우리는 bimodal+dip)이라, **"공정→구조 예측 + 접촉망 σ + 소성 morphology"**
  세 portion이 *정확히 그들이 비운 칸*에 들어감.  ★ **같은 그룹의 후속 Bazzoun 2026이 *바로 그 σ 솔버*(RNM/Holm)를
  추가** = Bielefeld(percolation, 2019) → Bazzoun(RNM σ, 2026) → 우리(σ 삼중항+MPM) 라는 *그룹-내부 진화*가 우리
  방향이 옳다는 증거.  percolation 추세(작은 입자→percolation↑·utilization·active interface·β=0.41·good-perf
  porosity ~21%)는 frame[4] 구조 descriptor 교차검증(σ 절대값은 그들이 없어 불가).
- ★ **Bielefeld 2020 = 그룹-진화 가운데토막 + σ-추가가 우리 방향임을 보이는 증거**: Janek 그룹의 σ-솔버는 **2019(σ
  없음) → 2020(*이 논문*: 연속체 flux-PDE σ_eff+τ²+바인더, 같은 1저자) → Bazzoun2026(RNM/Holm constriction σ+실험)** 으로
  *스스로* 정교화돼왔다. ★ **2020 = 우리(contact-network constriction) 방향으로 가는 *중간 단계***: 연속체 flux-PDE는
  granular 점접촉 좁힘을 빼서 σ를 *상한*으로 평가하고, Bazzoun과 우리는 그 constriction을 *되돌려* 넣는다. ⇒ "공정→구조
  예측 + **granular constriction σ 삼중항** + MPM 소성"이라는 우리 3대 portion은 이 그룹이 *걸어온 궤적의 자연스러운 끝*에
  놓인다 (positioning 최강 근거). + 바인더도 같은 궤적: 2019(carbon-free 배제) → **2020(*처음으로* CBD를 ASSB 미세구조
  모델에 추가)** → 우리(voxel σ-블로킹 + Hong/Lee 실험 cross-check + MPM/DEM void-fill 역학). σ_eff 추세(CAM↑→σ↓·
  porosity↑→σ 2×·Bruggeman 4× 과소·고-AM abrupt drop)는 frame[4] 구조 descriptor 교차검증(σ 절대값은 *연속체 상한*이라
  *추세*만; 절대 교차검증은 Bazzoun RNM·Minnmann 실험 소유).
- Bazzoun RNM(Holm+Kirchhoff) = 우리 네트워크 솔버 → 같은 물리, 추세 일치 (frame[4] 독립 교차검증).
- Bazzoun 실험 σ_eff,ion + 다중압력 = 우리가 부족했던 **외부 실험 앵커** 제공.
- Varkey E_SE=10.58·floor 21/37 % = 우리 "E 강성 → floor" 가설의 stiffer-SE 데이터점.
- Varkey 탄성→소성 무릎 ~100 MPa = 우리 Heckel P_y 138 재현(소재 일반성).
- ★ Minnmann 2022 §5.4 = Janek 그룹 리뷰가 **"미세구조 mechanical model을 echem·thermal과 결합 + CAM을
  다른 형상·크기·탄성으로 재고"를 명시 요구** → **우리 DEM(transport σ 삼중항)+MPM(소성 SHAPE morphology)
  분업이 그 권고의 직접 구현**. "구형 CAM 권고 + 비구형 재고"는 우리 MPM SHAPE 소성 간극 + Varkey/Bazzoun
  "구=타협" 한계와 같은 계보 → **frame[5] 분업이 문헌 권위로 정당화.**

## F. 우리가 아직 못 하는 것 / 흡수할 것 (정직 목록 → 향후)
- **FEM 연속체 transport 기준** 없음 (Bazzoun COMSOL 보유) — RNM↔FEM 대조틀 흡수 가치.
- **★ Bielefeld 2019 이 *앞서는* 것 (정직):** **GeoDict 성숙도**(상용 voxel 재료-연구소)·**Hoshen-Kopelman cluster
  분석**·**깨끗한 percolation power-law(β=0.41) + 입경-percolation 로그식(p_c=7.83·ln d+36.67)** + **porosity별 이상
  조성의 체계적 스윕(5/10/20%)**.  ★ **분류:** 그들 = **top-down / stochastic placement**(porosity·조성·입경=입력,
  랜덤 배치 + 사후 겹침조정; GeoDict ConductoDict/DiffuDict 계보, 단 σ PDE까지 안 가고 percolation cluster까지) —
  우리 NOVELTY.md §1 "top-down/reconstruction(필드 주류)" 열·§4 portion map **역할 A(percolation 추세 anchor)+M
  (methodology peer)**.  우리 = **bottom-up/process-physics formation**.  ⚠ 그들 *비운 칸*(σ·소성 SHAPE·dip·공정
  예측)이 우리 novelty지만, *구조-기하 분석 도구*(Hoshen-Kopelman·power-law fit)는 우리도 갖춘 것 — 흡수보다 *정당화
  근거*로 사용(우리 f_perc/percolation 지수가 그들 β=0.41과 같은 universality class).
- **다중압력 Heckel(LPSCl powder) 실측** — 우리 직접앵커 부족; Bazzoun σ-vs-P / Varkey P-vs-porosity로 보강.
- **명시적 바인더(SBR/CB/PTFE) 역학·이온저항 R_b** — Varkey/Bazzoun 보유, 우리 미모델.
- **multi-contact 구속항 F_mc** (Varkey) vs 우리 18× 연화 — 같은 증상(ρ>0.7 과강성) 다른 처방, 비교연구 거리.
- **항복캡 접촉**(So 2021 H-cap / Thornton–Ning p_y) — real E로 18× 연화 **제거** 가능 경로(1순위, `elasto_plastic_feasibility.md`).
- **비구형 입자**(Bouvard 각질 inclusion이 압밀 더 방해; Martin–Bouvard truncated sphere = SHAPE flow 없음) —
  우리 DEM·MPM 둘 다 구만 = 23년째 문헌 공통 한계(M&B2003→Varkey2026→Bazzoun2026), frame[5] 일관 확증.
- **Storåkers 소성 접촉면적** A=2πc(m)²rh (Martin–Bouvard, c(m) 0.5→1.45) — 우리 Stage-E(Tabor+volume)와 A/B 비교 거리.

---
## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

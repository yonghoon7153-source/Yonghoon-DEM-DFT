# 🔬 문헌 ↔ 우리 DEM+MPM — 차이 + 적용 인사이트

> 기준값: `our_dem_baseline.md`. 각 축마다 "문헌이 뭐라 하나 / 우리가 뭐라 하나 / 왜 다른가 / 어떻게 쓰나".
>
> ## ⭐필독 / 우리-랩 — **Jong-Won Lee 그룹(Hanyang) 자매 논문 2편** = 모델이 따라가야 할 실험 trend의 기준점.
> 두 논문은 **같은 NCA/NCM–LPSCl 계면의 두 렌즈** (Junhee Kang 공통저자):
> - **Kang & Shin 2025 (ACS AMI 17, 60558) = *역학/균열*.** 소재 NCA(Ni₀.₈₈)+LPSCl; bimodal 패킹 이득 ↔ **큰 입자
>   사이클 균열**(유지 47.7%/67.3%@100cyc); 균열 driver = **Li 농도·응력 구배(큰 입자 ~10×)**, 가압 아님; FEM =
>   **Voronoi 다결정 + cohesive-zone damage**; **E_NCA=175·E_LPSCl=22.1**. 축: A 패킹-균열 대가 / B EIS-TLM 열화
>   시그니처 / C FEM cohesive-zone ↔ 우리 MPM J2 / F 사이클 chemo-mechanics. digest `papers/kang2025_toughened_bimodal_nca_lzo.md`.
> - **Kim, Kang, Park, Lee 2025 (Electrochim. Acta 542, 147413) = *임피던스/반응속도*.** 소재 **NCM811(=우리
>   production)+LPSCl+SuperP** (62:37/72:27/82:17 wt%) + 할라이드 LZC; **modified TLM**(이온 z₁/전자 z₃ 두 레일 +
>   계면 z₂ crossrail)으로 **R_ion·R_ct·C_dl·고상확산(Warburg) *동시 분해*** = 우리 Kirchhoff/Holm σ-솔버의 실험
>   카운터파트 (단 우리는 z₁만 → R_ct·C_dl·확산·E_a 는 **우리 미보유**); **bulk σ LPSCl 1.6=Minnmann 1.6**·LZC
>   할라이드 0.51; **GB≈bulk**(우리 Cronau GB 인자 정당화); **uncoated R_ct=coated 의 ~20×**(=Kang 분해→균열의
>   *kinetics* 짝); T-스윕 **E_a 서열 R_ct≫GB>확산>bulk**. 축: B σ_ionic 3번째 TLM 앵커+GB / C 코팅 화학 패시베이션 /
>   D 할라이드 cross-check / **F R_ct·C_dl·E_a 미보유 새 축**. digest `papers/kim2025_impedance_decoupling_tlm_assb.md`,
>   CSV `docs/data/kim2025_tlm_kinetics_anchors.csv`.
> ★ **두 자매 논문의 연결:** 같은 황화물-계면 산화분해가 *역학*(균열, Kang)과 *kinetics*(R_ct↑ ~20×, Kim) 양쪽으로
> 나타나며, 우리 DEM+MPM 은 그 *구조→수송 σ* 를 채운다 → **structure-σ(우리) / mechanics(Kang) / kinetics(Kim) 3자 분업.**
>
> 현재 digest: **⭐Kang&Shin2025(랩 자체논문, NCA+LPSCl)**, Varkey2026·So2021·Martin-Bouvard2003·Bouvard2000(압밀), Bazzoun2026(전달),
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

- **★⭐(우리-랩) Kang & Shin 2025 (NCA+LPSCl, 실험+FEM) — bimodal 패킹 이득의 *역학적 대가* + NCA/LPSCl E 앵커**:
  - **bimodal 패킹 이득 = 우리 Furnas-dip 이득과 같은 물리** (단 *역학 대가* 추가): 3+10 µm bimodal NCA → 펠릿
    **0.74→0.68 mm**(패킹↑·두께↓)·**부피로딩 1.1×**·R_ele *크게 낮음*(큰 입자 전자 percolation) = 우리 "bimodal
    porosity↓·전자망↑"과 정합.  ★ **그러나** 큰 10 µm 입자 사이클 균열로 **유지 47.7 %(bimodal) vs 67.3 %(단봉)
    @100 cyc** → 우리 dip/packing 작업이 *순이득*으로만 보던 bimodal에 **"큰 입자 균열 리스크"** caveat 추가 근거
    ("toughened" = 랩 목표가 *균열 억제*).  ⚠ 단 **압밀 porosity 미보고**(펠릿 *두께*만) → 우리 DEM 15.6 %·Minnmann
    14 %·Doux 18 %와 **직접 비교 금지**.
  - **E_LPSCl = 22.1 GPa**(FEM) = **Bazzoun 2026(22.1) ∩ 우리 real-bulk ~24** → SE-모듈러스 앵커 *3중 확인*(우리
    E_eff 1.35/1.53는 그 연화 프록시).  **E_NCA = 175 GPa** ≠ 우리 NMC811 140 → CAM 모듈러스 옵션 재고(아래 §C/§F).
  - **가압 응력 ≪ 확산 응력 (맥락 분리 필수):** 그들 FEM = 가압 응력(stack 200/fab 400 MPa, *수백 MPa*) ≪ Li
    deintercalation 확산-유발 응력(*최대 GPa*) → **사이클 균열에 가압 기여 미미**.  ⚠ 이는 *사이클 균열* 맥락 한정 —
    우리 *압밀 porosity/Heckel*에서는 압력이 주역(제조 300 MPa, P_y 138).  "압력 기여 미미"를 우리 압밀 결론으로
    전이 금지.  같은 그룹이 **fab 400 / operating 200 MPa 명시 분리** = Doux/Lee2025 "제조≠작동"과 합류(단 operating
    200은 Doux 최적 5보다 높은 고압 운용).

- **📌 Li(Yang) 2026 ECER 리뷰원고(심사중, `papers/li2026_sulfide_stability_review_ecer.md`) — 압밀 전제·압력 3축의 리뷰급 종합**:
  - **냉간압밀 전제 문장**: "sulfide SEs **densify under conventional pressure conditions** → 양·음극과 양호한 고-고 접촉"
    ↔ oxide는 >1000 °C 소결 — 우리 300 MPa cold-press DEM+MPM 파이프라인 전체의 전제를 리뷰가 명문화 (§2.3).
  - ★ **압력의 3축 등장** (우리 fab-vs-operating 구분의 확장판): ① 압밀축 — 압력↑ → porosity↓·CAM-SE 실접촉면적↑ →
    R_ct+R_bulk 동시↓, **단 과압 → tortuosity↑·이방 접촉구조**(가압방향 접촉↑ ↔ 측방 pore-지배 약접촉 잔존)[151 Sakka
    JMCA 2022] = 우리 DEM 압력스윕·τ_Laplace 이방성 검증거리(신규); ② 열축 — **성형압↑ → 계면 치밀 비정질 P₂Sₓ층 in-situ
    형성 → 총발열 −40–50 %**[106–109] (압력-열안전 커플); ③ 작동압축(음극) — void 수축/안정/성장 상도(P 0–20 MPa ×
    i 0–40 mA/cm²)[189] + **Li 변형기구 지도 → CCD vs stack pressure 예측**[191] + "well-defined pressure window"
    (부족→void / 과압→GB Li 압입) = Doux2020 5 MPa 최적·Lee2025 2 MPa 합류.  미래방향 ③ "**저압/무가압 설계**"가
    리뷰의 결론 = 우리 300 MPa 압밀구조의 저압 unload 접촉/σ 유지율 시뮬이 정확히 그 요구.
  - 기계축 물성: **E 10–30 GPa·K_IC 0.2–0.4 MPa·m^½**(§C 참조) — porosity floor의 E-의존(우리 A축 논지)과 정합.
  - ⚠ 리뷰=2차출처·자체 데이터 0 — cite는 1차([151],[191] 등)로; porosity 절대값 없음(우리 Minnmann/Doux/Sakuda 유지).

## B. 전달 삼중항 — σ_ionic은 교차검증, σ_e/σ_thermal은 우리만
- **★ Minnmann 2021 JES (NCM622+LPSCl, 우리 소재계, EIS-TLM 1차 측정)**: σ_ion,eff **0.17 mS/cm @ 42 vol% NCM**
  (= 우리 DEM σ_ionic 0.04–0.18 상단과 일치!), **τ_ion 2.07 (=√(τ²=4.3))**, σ_el,eff 0.56 (τ_el²=7.4).
  CAM vol% 25–61 스윕: **CAM↑→σ_ion↓ / τ_ion²↑(2.4→15.3)**, **σ_el↑ / τ_el²↓(120→4.3)**, 42 vol% 교차·최적.
  τ_el²=120 @25 vol% = **전자 percolation 실패**(= Park 2020 90 wt% / 우리 σ_e f_p 항). **size: fine SE →
  σ_ion,eff↑ (bulk 1.6→1.2 mS/cm로 오히려↓에도) = packing/τ 효과** — 우리 "size=PACKING not overlap" 정확 일치.
  Eq 4 τ²=σ_0·φ/σ_eff = **우리 τ_Laplace,eff 정의 동일**(단 그들 = constriction 미포함 → 우리 Stage-E가 그
  constriction 포함 → 보정 lever). bulk LPSCl 1.6 mS/cm = 또 하나의 bulk 앵커. → **우리 σ_ionic·τ 의 최강
  same-material 실험 절대 검증점.** (그들 42 vol% NCM → 우리 φ_SE≈58 vol% 매핑 후.)
- **★⭐(우리-랩) Kim·Kang·Park·Lee 2025 (NCM811+LPSCl, 실험 EIS-modified-TLM) — σ_ionic *3번째* TLM 앵커 + GB 분리 측정**:
  - **bulk σ_ion LPSCl = 1.6 mS/cm = Minnmann 1.6 정확히 일치** → 같은 소재 두 독립 측정 일치 = 우리 bulk 앵커
    스프레드 {Cronau 3.0, Lee 2.19, **이 논문 1.6 = Minnmann 1.6**, Bazzoun 1.02} 의 신뢰 보강 (절대 직접대조 금지).
    할라이드 LZC = **0.51 mS/cm**(LPSCl 의 ~1/3).
  - **R_ion 측정·분해 (대칭셀 LNO-coated, bulk+gb):** 62 wt% **34.9** / 72 **48.1** / 82 **19.0** Ω·cm² → **82 wt%
    최저 이온저항**(같은 분말질량 → CAM↑ → 부피↓ → thin·compact → 이온 percolation↑). → 우리 σ_ionic 직접 외부
    앵커 (⚠ wt% 62:37/72:27/82:17 → vol% → φ_SE 매핑 선행; 대략 62 wt% ≈ φ_SE 0.45–0.50, 82 wt% ≈ 0.25).
    ★ **단 "R_ion 이 깨끗이 분리된 셀"(대칭셀/uncoated)만** 쓸 것 — coated full-cell 은 R_ct 와 lumped (§5.5 Morasch
    R_int/R_i 교훈: 비 작으면 영역 겹침).
  - ★ **GB(입계) 를 *분리 측정* → 우리 Cronau(r_SE) GB 인자 정당화:** **R_i,gb ≈ R_i,bulk 또는 더 큼**(62: bulk
    9.3 vs gb 25.6; uncoated 82: bulk 59.7 vs gb 209.5) + **GB 가 온도에 더 민감**(62: gb 25.6→3.1 vs bulk 9.3→6.0
    over 30→60°C). → 우리가 σ_grain prefactor 에 럼핑한 Cronau GB 인자가 옳은 방향(입계가 이온수송 주 병목)임을
    *분리 측정*으로 확증. ★ 흡수 후보: GB 저항의 입경/온도 의존을 우리 σ_grain 에 명시.
  - 차이/주의: 그들 R_ion 은 **측정+TLM 피팅** 값(예측 솔버 아님) → frame[4] 외부 검증. 우리 σ_ionic(계산)·삼중항·
    Stage-E·MPM 우위 유지. CAM=NCM811(=우리 production, Kang 의 NCA 보다 정확) 단 입경 PSD 미보고 → 절대 매칭 주의.
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
- **★ Kang(Jihyeon) 2025 (bollard binder, LIB 건식) — 바인더 σ 페널티의 *바인더별* 세분 근거** (상세 §C):
  바인더 필름 σ_ion **PTFE 4.88e-6 → PC_PTFE 1.31e-4 S/cm (27×)** — 앵커형 극성 바인더는 "완전 차단"이 아니라
  "약한 이온 전도상".  우리 W2 whatif 는 PTFE **σ_ion×0.74 고정** 페널티(바인더 종류 무관) → **바인더별 σ_ion
  입력으로 세분**할 문헌 근거(SDCP·PC류 극성/도전 바인더는 PTFE보다 덜 막음).  ⚠ 액체전해질 팽윤 필름 값 —
  ASSB SE-neck 차단과 물리 다름, **비율·방향만**.  양극 σ_e 1.30 S/cm(최고)는 분산효과(§C) — σ_e 폼의 바인더
  항이 아니라 A5 dispersion 축 증거.
- **★ Han 2025 (ICEP 이온전도 탄성 binder, Adv. Mater. 2506266, ⚠액체 LIB *습식* — Kang(J) bollard의 습식 자매편) —
  "binder=σ0 차단자"를 깨는 클래스의 *두 번째 독립점* + 7 nm coat ASR 스케일**
  (digest `papers/han2025_icep_conductive_elastic_binder.md`, CSV `docs/data/han2025_icep_binder_anchors.csv`):
  - **binder 필름 σ_ion 0.135 mS/cm**(ICEP-8, RT EIS SS|film|SS; PVDF 0.065 — 건식 PVDF로 불가능한 값 →
    둘 다 전해질-swollen 추정, SI 확인 필요) = σ_LPSCl bulk 1.6(Minnmann/Kim2025)의 **~1/12**.
    ★ **Kang(J) PC_PTFE 0.131 mS/cm와 사실상 동값 → "전도-binder 클래스 ~0.1 mS/cm" 가 독립 2편에서 수렴** —
    W2 binder-voxel σ_b 파라미터의 대표값으로 채택 가능(0 = PTFE ↔ 1.3e-4 S/cm급 = ICEP/PC/SDCP류).
  - **★ 7 nm coat의 film-ASR 스케일 논증(우리 유도, 논문 stated 아님)**: R = t/σ_b → ICEP ~7 nm 균일 coat ≈
    **5×10⁻³ Ω·cm²**(무시) vs 같은 7 nm 절연-binder(σ≲1e-10 S/cm) ≥ **10³–10⁴ Ω·cm²**(지배) — Bielefeld2020
    AM/SE 면접촉 40·Kim2025 R_ct 22–453 Ω·cm² 예산 대비 **"AM-coat 허용여부는 binder 화학이 정한다"**.
    → A4/W2에서 coat형 binder는 σ_b에 따라 계면 conductance 수정항으로(차단↔투명 스위치).
  - **셀-레벨 발현 사슬(실측)**: binder-σ 2.1× → GITT **D_Li 0.42 vs 0.18 ×10⁻⁷ cm²/s·R_internal 31.0 vs
    57.2 Ω** → z-Raman redox 균일(PVDF 바닥 E_g/A₁g 0.84 = 미반응) → **로딩 상한 62.4 vs ~40.7 mg/cm²** —
    "binder 수송성이 두께 상한을 정한다"의 정량 사슬(우리 Phase-5 graded-z 출력이 예측해야 할 관측량).
  - ⚠ 액체-swollen 전도 메커니즘 개연 → **건식 ASSB(SDCP dry)로 σ 절대값 이식 금지**(SDCP 자체 측정 필요);
    복합 σ_eff·porosity·조성·캘린더링 전무(습식 LIB, Experimental=SI-only) → 압밀·수송 절대축 비교 불가,
    **binder 물성 앵커 전용**.

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
    (AM 70–85 wt%) 상단과 정합 + porosity↑→AM↑ 이동.  데이터 `docs/data/bielefeld2019_percolation.csv`.
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

- **★⭐(우리-랩) Kang & Shin 2025 (실험 EIS-TLM) — 사이클 *열화 시그니처* (정적 우리 σ엔 없는 시간축)**:
  - **Z-type TLM 분해**(회로 Fig S6: r_Ohmic—(r_anode‖cpe)—양극[r_ion + (cpe_int‖(r_int+Z_w))]) → **R_ion(이온망)
    거의 불변**(B-NCA 5.7→6.7) **vs R_int(계면) 113.5→501.8(4.4×)·R_w(Warburg) 70.7→353.4(5×) 급등**(75→100 cyc).
    ★ **"R_ion stable / R_int+R_w rising" = 균열의 명확한 시그니처** — **R_w ∝ δ_s**(eq 2, 확산거리) → 큰 입자 =
    긴 δ_s = 큰 R_w; 균열이 tortuosity↑로 R_w 추가 증가.  U-NCA는 R_int 1.5×·R_w 2.1×로 완만(안정).
  - 차이/주의: 그들 R_ion/R_int/R_w는 **실험 측정값 + TLM 피팅**이지 *예측 솔버* 산출이 아니다(FEM은 σ_ion=0.02
    S/m·σ_e=1 S/m을 *입력*만, σ_eff를 *안 풂*) → 우리 Kirchhoff/Holm σ-솔버와 **방법이 다름**.  우리는 *정적* σ만
    예측 → 이 "사이클 R_int/R_w↑" 열화 패턴은 **우리 미보유 시간축**(흡수 후보 = backlog B6에 *사이클-Warburg*).
  - **LZO 코팅이 R_w를 고정**(50→100 cyc **+1.2 Ω·cm²만** vs bare +176.7) = 균열 억제 직접증거 → "코팅→계면
    안정→δ_s 유지→R_w 평탄"의 transport 입증.

- **📌 Li(Yang) 2026 ECER 리뷰원고(심사중) — 조성 균형·carbon·구배·면용량의 리뷰 좌표 (B축 서사 보강)**:
  - **조성 = 이온-전자 동적 균형**: CAM 과다 → SE 망 파편화 → 분극·용량저하 / SE 과다 → CAM 분산 → 전자망 단절
    [143 Fig 9a: CAM 40–90 wt% × 입경 3.0/6.2/10.3 µm 채널단절 지도] = 우리 AM%-σ 트레이드오프·dead-AM 경고·σ_e f_p
    항의 리뷰판 — 우리 결과를 문헌 프레임에 얹을 때 이 그림 인용.
  - ★ **carbon 부피점유 [147] = 우리 랩 Kim2024(AFM 34,2409318) 그대로 인용됨**(Fig 9c) — "구형 CB가 SE 유효부피 점유·
    Li⁺ 채널 협착·국부 전자농집→황화물 분해 가속; fiber/flake 우위" = 우리 A4/A5·CBD voxel·SuperP-vs-VGCF 형상 구분의
    앵커 계보가 리뷰급 승인을 받은 것.
  - **구배 전극**: 집전체측 carbon↑/분리막측 SE↑[149] + **3-layer NCM83/LPSCl σ_e/σ_ion sim+exp 실증**[152 Schlautmann
    2025 ACS EL] = **A7 Phase-5 graded-z 직접 문헌 앵커** (Fig 10c).
  - **면용량 목표선**: 현 1–2 → **>3 mAh/cm²** 필요[144] → 우리 SDCP 3.18 mAh 캠페인 = 목표선 위 사례로 포지셔닝.
  - **코팅 4요건+두께 딜레마**[154]: σ_ion↑·σ_e↓·화학안정·기계유연 + "얇음=차단실패/두꺼움=이온저항" = 우리 STEP4
    ASR_film hook·SDCP σ_SDCP {15/50/150/1500} 스윕(+0.8→+63.4 %)이 정량으로 답하는 질문 구조.
  - **Kim YJ 2024 [150] (ESM 71,103607)**: 3D 미세구조 위 SOC·전해질 전류밀도·활성/비활성 NCM·von Mises σ 동시 시각화 =
    우리 STEP3/STEP4 voxel 그림과 가장 유사한 문헌 그림 → **WISHLIST digest 후보**.
  - ⚠ 리뷰 자체는 σ 수치 앵커 없음(σ_eff 실측은 Minnmann/Bazzoun/Kim2025 유지); 재료군 σ 범위(황화물 10⁻⁴–10⁻² S/cm)만.

## C. 역학 / morphology — MPM 고유 (문헌 DEM은 형상 못 바꿈)
- 문헌: Varkey "elasto-plastic"은 **CONTACT 힘법칙만**(Thornton–Ning), 입자는 완벽 구 — "구=타협,
  현실 형상=향후 과제" 명시. Bazzoun도 구만.  **★ Duquesnoy 2023(ARTISTIC 캘린더링 DEM)도 rigid-구형**(CBD-shrink 건조=
  부피연산, 형상소성 없음) → **제조시뮬 최전선 3편(Varkey·Bazzoun·Duquesnoy)이 모두 형상소성 없음 = frame[5] *3중* 독립확증**
  (우리 MPM 이 메우는 형상-morphology 절반이 세 논문 다 빠짐).
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

- **★ Kang(Jihyeon) 2025 (Adv. Mater. 2416872, 중앙대+현대차, LIB 건식전극 — ⚠랩 Junhee Kang 아님) — "bollard hitch"
  앵커 바인더 = 우리 SDCP 화학앵커의 개념-클래스 독립 선례** (digest `papers/kang2025_bollard_anchored_binder_dry_electrode.md`,
  CSV `docs/data/kang2025_bollard_binder_anchors.csv`):
  - **앵커링 물리 (그들)**: PC(PAA-grafted CMC)가 NMC 산화물 표면에 **Na⁺-매개 화학흡착** — MLP-DFT E_ads
    **PC_2Na −2.24 ≫ PC_1Na −1.12 ≫ 극성쌍극자 −0.37 ≫ PTFE vdW −0.09 eV**; PTFE fibril은 bollard의 자유 Na에
    **Na–F −0.35 eV**(PTFE-NMC의 2–4.5×) + PAA 가지 물리얽힘으로 계류.  400 K NVT-MD 10 ps: PTFE-only 탈착
    (표면거리 4.2→6.6 Å) vs PC 동반 계류(4.5–4.9 Å).  XPS F1s Na–F>C–F로 실험 확인.
  - ★ **우리 SDCP와 판정 — 같은 개념-클래스, 4가지 차이**: 둘 다 "CAM 산화물 표면 *이온성* 화학흡착이 PTFE
    vdW-only 접착을 대체"; 이온성≫극성≫vdW 사다리 = 우리 **doped(−4.797) ≫ neutral(−3.02 eV)** 방향의 분자스케일
    외부 확인(frame[4]-형).  차이: (i) 그들 **양이온 Na⁺ 표면 브리지** vs 우리 **음이온 −SO₃⁻ Li-O층 삽입**(O–Li
    1.83 Å×2); (ii) 그들 **이중-바인더**(절연 bollard + PTFE rope 0.6 wt% 유지) vs 우리 **단일 도전바인더**(SDCP가
    앵커+전자전도 겸업, PTFE-free 지향); (iii) 그들 σ_e 1.30 S/cm 최고는 **분산/3D망 효과**(PC 절연) — 우리 SDCP
    전도축과 다른 채널(=A5 dispersion 증거); (iv) 역학 매핑은 우리가 앞섬(footprint→γ 0.93 J/m²→coh) vs 그들
    fragment E_ads에서 종료.  ⚠ 절대 E 비교 금지(fragment·facet·코드 다름) — 서열만.
  - **bollard 형상 = 우리 SDCP 시딩과 동형**: bollard = NMC 표면 **불연속 앵커 입자/패치 + 입자간 fibril 스팬**
    (EDS Na 균일분포) — conformal 필름이 아니라 우리 additives.py SDCP `particle` regime + `surface_frac`(AM-앵커
    분율 bias) 그림과 일치; `seed_coat` conformal 필름은 SuperP coat_block 쪽.  SDCP+PTFE 콤보 시 fibril이
    앵커입자에서 nucleate하는 bias가 그들 모델의 시딩 번역.
  - **A3 binder-cohesion 실험앵커 (계층 구분 필수)**: 계면(그들 E_ads비 25×·우리 γ비 ~10×) ≫ 시스템 peel
    **1.68×**(0.9615/0.5733 N/cm, 전극↔Al — N/cm≈J/m² 규모 96/57 = 소성산일 포함 → 우리 DFT γ 0.93 J/m²와 100×
    층위차, **비율만 전이**).  사이클 R_ct 성장(39→48 vs 68.65→91.52 Ω)·**PTFE계 NMC 2차입자 파쇄 vs PC계 무균열**
    (100 cyc) = binder cohesion↔AM 파괴 결합의 실험짝(우리 Auerbach는 압밀-접촉응력만 — driver 다름, 정성).
  - **PTFE fibrillation 하한 + 혼합 앵커**: dough 성립 PTFE **0.6 wt%**(bollard 지원; 0.2 wt% 실패) vs **2 wt%**
    (단독) = 우리 `--ptfe-fibril`/PTFE-wt 축의 첫 문헌 하한.  혼합법→2C 용량 STD **16.52→5.59(planetary)→4.28
    (ballmill×3)** = **A5 dispersion-CV 정량 실험앵커** + ADDITIVE_PROCESS(ballmill 우위) 방향 정합.
  - ⚠ **LIB 액체전해질 — 이온위상 역전**: 그들 "porosity↑(25.9% 또는 ~22.3% — 본문 문장 중의적; PVdF 17.7%)·
    τ 1.30 = 장점"은 pore=전도체 논리 → 우리 ASSB(SE망=전도체, porosity=죽은 공간)로 부호까지 반대 — 절대 전이
    금지.  바인더 필름 E도 MPa-스케일(PTFE 3.50/PC_PTFE 0.15 MPa, 다공 시트) — 우리 ADD dict PTFE 0.30 GPa와
    1000× 층위차, 서열만.
- **★ Han 2025 (ICEP, 실험+DFT흡착, 액체 LIB 습식) — binder 역학·접착 앵커 + coat-morphology + 전극-스케일 유효 E 실측**
  (digest `papers/han2025_icep_conductive_elastic_binder.md`; Kang(J) bollard와 자매 — 그들 *건식 앵커-입자+fibril*,
  이들 *습식 conformal-coat*):
  - **binder 3-morphology 분류 완성(화학×공정이 형상을 정한다)**: **ICEP = NCM811 위 ~7 nm 균일 coat**(습식,
    수소결합 구동 — DFT NCM811(001) AMPS −1.8~−2.2 eV ≫ PVDF vdW −0.70) / **PVDF = aggregate**(습식, 약흡착
    → 산발 응집) / **PTFE = fibril**(건식 전단, Lee2025·우리 CBD) (+Kang(J) bollard = 앵커입자+fibril 하이브리드).
    ★ **시딩 규칙 흡수: coat(7 nm)는 sub-voxel(우리 복셀 ~0.14 µm의 1/20) → resolved 상 금지, 계면 성질
    (접촉 conductance/coverage modifier)로**; fibril/앵커입자만 resolved 시딩(additives.py).
  - **A3 `--coh` 역학 앵커**: 필름 인장 연신 **283 %**(PVDF 31.8)·flow **~2.7 MPa**(digitized) = binder-bridge
    인력 σ 스케일; SAICAS 박리 **0.27 N@1 mm ≈ 270 N/m**(우리 환산; cohesion 0.29 N ≈ 290; PVDF 40/70) —
    apparent peel(소성 소산 포함) → Bucci 고유 G_c 4 J/m²와 층위 다름, bond-파괴에너지 **상한측**으로만.
    ⚠ **필름 E는 프로브 3-decade 스프레드**: 나노압입 6.03 GPa(표면 유리질 hard-block) vs 인장 초기 ~10–25 MPa
    (digitized, 벌크 엘라스토머 망) → MPM binder상 E는 MPa-급(bulk)으로, 6 GPa 입력 금지.
  - **전극 나노압입 E 1.57 GPa ≈ 우리 MPM champion E_eff 1.53** — 물리 기원 다름(다공 폴리머-복합 압입 vs
    granular 연화 프록시; 우연 일치 flag)이나 **"전극-스케일 유효강성 O(1 GPa)" 밴드의 실측 동반자**(구성상
    벌크 E 수십~수백 GPa가 전극 스케일에서 1–2 GPa로 내려온다는 우리 서사의 외부 실측점). PVDF 전극 0.11 GPa
    = binder가 전극 유효 E를 10× 흔든다는 실측 → binder 역학이 전극-스케일 modulus의 1차 변수.
  - **binder→AM 파괴 커플링(직접 구조 증거)**: 사이클 후 nano-CT/TXM — PVDF 분쇄(pulverization)+입계균열 vs
    **ICEP 무손상**; rock-salt 상전이층 3.1 vs 11.3 nm → binder 접착·탄성이 균열 전파/박리 억제. ⚠ driver =
    *사이클 Li-구배*(습식 건조응력 + 탈리튬) ≠ 우리 압밀-Auerbach 접촉응력 — A3 bond 도입 시 fracture 축
    기대효과의 *방향* 근거로만(정량 전이 금지). 건조 모세관응력-균열 축 자체는 습식 전용(우리 건식 무관).
  - **모델링 패럴렐:** 그들 FEM = 2D **Voronoi 다결정 NCA + cohesive-zone 입계 박리(취성), damage scalar D(0→1)**,
    전변형 ε = ε^e + ε_d (ε_d = Ω/3·Δc_Li, Ω = 5.9 % 부피변화).  우리 MPM = 3D/2D **J2 연속체 소성 *형상* 흐름(연성),
    누적소성변형 Σdg**.  ★ **둘 다 연속체 + 손상/소성 변수**지만 **파괴 메커니즘 다름**: 그들 *취성 입계 cohesive 박리*
    ↔ 우리 *연성 소성 void-fill*.  damage D ↔ Σdg는 *개념* 대응(동일시 금지).  ⇒ **시간축 분업**: 사이클 chemo-
    mechanical = cohesive-zone(랩 FEM), 압밀 plastic = J2(우리) → frame[5] 확장(MPM 문서에 명문화 제안).
  - **★ 크기-의존 파괴 (우리 Auerbach/fracture-aware σ의 *크기* 방향을 못 박음):** **큰 입자(10 µm)가 작은 입자
    (3 µm)보다 압도적 균열** — c_Li 구배 **~10×**, σ_Mises 구배 큼, **damage→1 다중 입계(완전박리)**.  우리 DEM
    fracture(AM_P 92:8 8mAh서 37–40 % cracked)·f_intact·frac_severe는 *크기-의존성 명시 안 함* → **AM_P(큰 다결정)
    일수록 fracture↑** 하도록 Auerbach 임계를 입경-스케일링(σ_crit ∝ 1/√d 또는 접촉응력 ∝ 입경)으로 보강.
    - ⚠ **driver 다름 명시:** 그들 = *사이클 Li-구배*(NCA/LPSCl 계면분해 → 농도·응력 불균일); 우리 DEM = *압밀 접촉
      응력*(Auerbach).  "큰 입자 깨짐"은 공통이나 *원인이 다름* → 우리는 *압밀-시점* 균열만 표현(접촉응력 ∝ 입경 버전
      흡수), *사이클* 균열은 frame[5] 미보유로 명시.  Lee2025 "PC-NCM 깨짐/SC-NCM 무손상"·우리 DEM AM_P 파괴와 같은
      "다결정 2차입자가 깨진다" 계보.
  - **계면 화학열화 → 균열 (우리 *전혀* 미모델 축):** "**NCA/LPSCl 계면분해(XPS: Li₂Sₙ 163.0·PO₄³⁻ 134.4 eV) →
    Li-구배 → 응력 → 균열**" 인과 = 우리가 안 다루는 *계면 화학* 축.  **LZO 6–8 nm 비정질 코팅**이 이를 패시베이션
    (XPS 부산물 억제 → 구배·damage 모두 완화, Fig 5f–h) → 우리 coverage(*기계* 접촉면적)와 **종류 다른** *화학*
    코팅(backlog A4 carbon coating과도 다름).  future "계면" 축의 실험 근거로 기록.

- **📌 Li(Yang) 2026 ECER 리뷰원고(심사중) — 기계축 물성·chemo-mech 결합의 리뷰 좌표 (C축 물성 입력 + A10 시간축)**:
  - **물성 앵커**: **E(황화물) 10–30 GPa**(우리 real 22–24 정합; E_eff 1.35/1.53=연화 프록시 서사 유지) ·
    **K_IC 0.2–0.4 MPa·m^½**[122–124 McGrogan 계열] = SE 취성균열(backlog D6, damage/cohesive-MPM) 구현 시 물성 입력.
  - ★ **임계입경 규칙**: 계면반응 부피팽창 하 **>~3 µm → 탄성변형에너지 축적 → 파편화** / **<1 µm → 협조변형(균열 회피)**
    [72,74] = 우리 r_SE 크기효과·Cronau(r_SE)·A9 크기-파괴 압밀분의 독립 문헌 지지 — fracture-aware σ(f_intact)와 연결.
  - **chemo-mechanical 결합 파괴**(§4.1.4): CAM 팽창수축 ↔ SE 산화분해 **부피수축** 역방향 → 계면 응력집중 누적 → CAM
    균열·2차입자 파편화·SE-CAM 접촉 상실; in-situ 측정 "전해질 산화 부피변화가 응력축적 주요 원인"[141 operando pressure]
    = 우리 MPM 응력장·void-fill이 표현할 물리의 *사이클* 구동판(A10 공백; Bucci·Alabdali 계열과 같은 칸).
  - **음극 압밀역학 곡선**: 합금 음극 **상대밀도 vs 정규화압력 σ/σ_y**(액체 vs SE, Al/Sn/In)[210 Nat Mater 24,907] +
    "stack pressure를 합금 σ_y에 정합"[209] = 우리 Heckel/σ_y 언어가 음극 설계에 등장한 외부 사례.
  - **덴드라이트 wedge-opening**[177 Ning Nature 618]: 균열 후단 Li 주입 쐐기 → K_IC 초과 시 관통 — 우리 fracture 모듈
    (양극 복합재 Auerbach)의 음극판(미보유; Li금속·분리막 SE 없음) — over-claim 금지 경계 명확.
  - ⚠ 리뷰의 "황화물 소성 변형성"은 정성 서술 — CONTACT-소성 vs SHAPE-소성 구분 없음; frame[1]/[2] 구분을 소급 적용하지
    말 것. 기계 수치는 재료군 대표값(LPSCl 특정은 Sakuda 24·Kang/Bazzoun 22.1이 더 정밀).

## D. 패킹 / Furnas dip — DEM·기하 소유, 소성 MPM 불가
> ★ **할라이드 cross-check (Varkey ↔ Kim 2025):** Varkey 2026 (할라이드 Li₃YBrCl₆) = 할라이드 *압밀/σ* (E=10.58 →
> stiffer → floor 21/37 %); **Kim 2025 (할라이드 Li₂ZrCl₆ LZC) = 할라이드 *계면 kinetics*** (bulk σ 0.51 < LPSCl
> 1.6, BUT R_ct 가 LPSCl 보다 *낮음* = 산화안정성↑). ⇒ **할라이드 = "안정하나 σ 낮음"** 의 두 측면(압밀 Varkey /
> kinetics Kim). 우리가 할라이드로 확장 시 E·σ·R_ct 셋 다 재보정 필요.
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

- **★★ Duquesnoy 2023 (Franco/ARTISTIC, LIB NMC111 습식) = 우리 5-Phase 로드맵의 *published archetype* — 최적화 loop 전체가
  흡수 대상** (digest `papers/duquesnoy2023_ml_multiobjective_manufacturing_optimization.md`, CSV
  `docs/data/duquesnoy2023_manufacturing_optimization.csv`).  **they-lead / we-lead / adopt** 로 정리:
  - **THEY LEAD (그들이 앞섬 — 우리 Phase 3–5 미완):**
    - ★ **닫힌 역설계 loop 완성·published·실험검증:** 물리시뮬(CGMD 슬러리→CBD-shrink 건조→DEM 캘린더링, LAMMPS 174건)
      → **Sobol(+Saltelli) DOE** space-filling → **SISSO** symbolic regression(물성=Σc_i·d_i, 3-descriptor, l₀; R² 0.91–0.985)
      → **베이지안 다목적최적화**(GP + **GP-Hedge**(LCB+EI+PI) + 스칼라화 **C_f=¼[Σy²_min+Σ(1−y)²_max]** 등가중, 300-iter)
      → 역설계 최적 **AM/SC/CD=90.4/58.1/28.4 %** → **실물 전극 제작·EIS 검증**(τ 1.8·density 2.6·porosity 29 %).
      우리는 Phase 1(σ 삼중항 스케일링)만 완료, Phase 3–5(predictor→2D synth→layering)는 계획만 → **그들 loop 기계장치가
      우리 로드맵의 de-risking + 직접 청사진.**
    - **SISSO auto symbolic-regression:** 우리 σ 폼은 *손유도 physics-prior + OLS/Ridge*.  SISSO 는 feature-space(연산자
      {+,−,×,²,³,⁻¹,√,³√,log,exp} 재귀 rung) + l₀ screening 으로 *자동* 발견.  우리에겐 없는 도구.
    - **Sobol space-filling DOE:** 우리 corpus 는 ad-hoc + `active_learning_suggest.py`(exploit corner 수렴) → **exploration 약함**.
    - **자체 실험 fabrication:** ML 최적전극을 실제로 만들어 검증(우리는 문헌 앵커 차용).
  - **WE LEAD (우리가 앞섬 — 그들 비운 칸 = 우리 novelty 위치):**
    - ★ **구조→σ 기계론 (그들 black-box):** SISSO 는 제조→물성 *직결*, 구조 우회 → "왜" 못 답함.  우리는 DEM+MPM 구조 →
      Kirchhoff/Holm σ → 스케일링 → 구조 descriptor(φ·CN·cov·τ·percolation)가 인과 설명.
    - ★ **전달 삼중항 + Holm constriction + Stage-E 소성면적:** 그들 = **tortuosity(pore 이온 proxy 1채널) + GeoDict σ_e(연속체=
      constriction 없는 *상한*, Bielefeld2020 계열)**.  σ_ionic·σ_thermal·명시 접촉망 **전무**.  ⚠**이온위상 반전**(그들 pore=이온
      전도체 / 우리 SE망=이온전도체) → transport 절대·부호 전이 금지, loop 방법론만.
    - ★ **MPM 진짜 소성 morphology (frame[5]):** rigid-구형 캘린더링(형상소성 없음)+CBD-shrink(부피연산) = **Varkey/Bazzoun
      과 같은 frame[1] 한계** → *제조시뮬 최전선 3편(Varkey·Bazzoun·Duquesnoy)이 다 형상소성 없음* = frame[5] 3중 독립확증.
    - ★ **Furnas dip + bimodal 12:4:1 정량** (그들 단일 CAM 상, dip 없음).
    - **DEM↔MPM 상보 프레임 [1]–[5]** (그들 단일 파이프라인, 우리 교차검증 엄밀성).
  - **ADOPT (구체 흡수 action, 우선순위):**
    1. **★★ Sobol(+Saltelli) DOE = 다음 sim batch 즉시 적용** — 우리 (AM·P:S·r_SE·P) hyper-rectangle 에 low-discrepancy 깔아
       σ_ionic close-out 이 지목한 구조 gap(CN≥7·중간두께) 균일 충전.  `active_learning_suggest.py` 에 Sobol seed 모드(explore+exploit).
    2. **★★ SISSO 를 우리 corpus 에 돌려 σ 폼 *교차검증*** — √φ_eff·CN²·√cov 류를 재발견하면 손유도 폼의 독립 확증(frame[4]).
       ⚠ SISSO `Σc_i·d_i`=단일-backbone 선형결합 = 우리가 σ_thermal 에서 *실패 판정*한 pure-power-law → **σ_thermal 은 SISSO 도
       한계 예상**(우리 "Ridge irreducible/multi-pathway" 논지 강화); σ_ionic·σ_e(단일 backbone)는 궁합 좋을 것.  Phase-3 per-metric
       엔진 후보(hand-form 과 병렬 fit, CV R² 비교).
    3. **★★ GP + GP-Hedge + 스칼라화 = Phase 3–5 역설계 loop** — 그들 Eq 3 스칼라화 채택하되 **가중치는 application 별**
       (fast-charge=τ·σ_e↑ / high-energy=density↑; 그들도 명시).  우리 metric set(σ_ionic/σ_e/σ_thermal·porosity·coverage·dip)로 확장.
       Phase-3(predict)→4(`extract_2d_microstructure.py synthesize_microstructure`)→5(layered)를 하나의 BO loop 로.
    4. **PDP + KDE + radar 해석 패널** — 그들 Fig 4(2D PDP 민감도)·5A(KDE 위치)·6(극단 radar)을 우리 webapp group-compare 에.
  - ⚠ **caveat (§10 digest):** LIB 습식·NMC111·이온위상 반전·rigid-구형·black-box·단일 CAM 상·등가중 proof-of-concept·
    Table 1 R²=0.933 표오류(CI95 신뢰)·mass loading 본문15–40 vs 실험6.7 불일치.  → **loop 방법론만 흡수, transport/역학 물리결론 전이 금지.**

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
- **★ Kang(Jihyeon) 2025 (bollard binder) 가 갖고 우리가 미보유 (SDCP/A3 흡수 후보):**
  - **MD hold-test(동역학 검증)** — 우리 SDCP E_bind는 single-point; 그들은 400 K NVT-MD로 "앵커가 시간축에서도
    잡아둠"(PTFE 4.2→6.6 Å 탈착 vs 계류 4.5–4.9 Å)을 시연 → SDCP-NCM MLIP MD 탈착시험 이식(A4′ 검증 ④의 계산 짝).
  - **바인더-바인더 결합 정량(Na–F −0.35 eV)** — anchored-binder↔PTFE 커플링 에너지.  우리 비교셋(VGCF+PTFE /
    SDCP-only)에 **SDCP+PTFE 콤보** 추가 시 대응 결합(술폰산/티오펜–F?)이 미계산 칸 — "앵커가 rope 필요량을
    줄인다"(그들 7:3 최적, PTFE 2→0.6 wt%) 가설의 우리 프레임 시험 거리.
  - **혼합→성능 산포 정량(STD 16.52→4.28)** = A5 dispersion-CV 실험앵커; **fibrillation 하한(0.6 wt%)** =
    `--ptfe-fibril` magnitude 앵커 — 둘 다 우리 morphology knob의 미앵커 magnitude를 잡아줄 데이터.
- **★ Han 2025 (ICEP) 가 갖고 우리가 미보유 (SDCP/A3/W2/Phase-5 흡수 후보):**
  - **z-분해 반응 균일성 실측(confocal Raman E_g/A₁g top/bottom)** — PVDF 바닥 0.84(미반응) vs ICEP 0.99(균일)
    = **Phase-5 graded-z 가 내보내야 할 관측량의 실험 원형**; 우리 layered-composite 출력에 "z별 활용/반응도
    프록시" readout 추가 시 이런 실험과 직접 접점.
  - **습식 건조 공정축(모세관응력→binder segregation→균열·박리)** — 우리 solvent 미모델(건식이라 불요하나
    습식 문헌 비교 시 이 driver 를 우리 압밀-접촉응력과 혼동 금지); Lyu2025 drying-DEM 이 시뮬 짝.
  - **binder 관능기 화학 → 접착·킬레이션·CEI 사슬**(DFT 흡착 + Mn²⁺ 킬레이션 126 vs 27 ppm + TOF-SIMS CEI
    108 vs 283 s) — 우리 coverage(기계 접촉면적)와 종류 다른 *화학* 계면축(Kang/Kim 랩 축·LZO/LNO 코팅과 동류).
  - **binder-σ → 셀 kinetics 정량 사슬(GITT D_Li·R_internal·DRT P1–P4)** — 우리 σ-솔버 밖(z₂ crossrail 계열,
    Kim2025 R_ct 축과 동류).  SDCP 논증서 "전도 binder 의 셀-레벨 이득" 인용점.
  - **사이클 chemo-mechanics(volume change + cohesive-zone 입계 박리)** — 우리 MPM/DEM은 *압밀*만, *사이클* 부피변화
    (NCA 5.9 %)·입계 균열 미모델.  그들 FEM(Voronoi + CZM damage)이 그 칸 → frame[5] *시간축* 분업으로 위치.
  - **크기-의존 파괴의 정량 driver(Li-구배 10×)** — 우리 Auerbach는 크기-의존성·Li-구배 미반영 → AM_P 입경-스케일링
    파괴로 보강(§C).  ★ 랩 핵심 = "큰 입자 깨짐" → 우리 모델이 *반드시* 반영해야 할 방향.
  - **NCA(E=175) CAM 옵션** — 우리는 NMC811(140)만.  랩 소재가 NCA → `our_dem_baseline.md §0`에 NCA 행 추가 +
    σ_e(NCA) 재보정 제안.
  - **계면 화학열화(XPS 부산물) → 균열 체인** — 우리 *전혀* 미모델.  LZO 같은 *화학* 코팅 효과(coverage=기계와 다름).
  - **EIS-TLM 사이클 시그니처(R_ion 불변 / R_int·R_w 급등)** — 우리 정적 σ엔 없는 *열화 시간축*(backlog B6 사이클-Warburg).
- **★⭐(우리-랩) Kim·Kang·Park·Lee 2025 이 갖고 우리가 미보유 — *계면/확산 kinetics* (frame[5] 의 새 빈 칸, 자매 Kang 보완):**
  - ★ **계면 전하전달 R_int(=R_ct) + 이중층 C_dl + 고상확산 Warburg(R_w/T_w/α) = 우리 σ-솔버가 *전혀* 안 잡는 칸.**
    우리 Kirchhoff/Holm 솔버는 modified TLM 의 **z₁(이온수송) 레일만** 계산 → crossrail z₂(R_ct·C_dl·Warburg)는
    통째로 우리 모델 밖. ⇒ "우리가 이걸 cross-validate" 가 *아니라* "우리가 *안 갖는* 것을 실험이 보여줌"으로 정직히.
    → `our_dem_baseline.md §4` + 여기 F 에 "**계면 전하전달·이중층·고상확산 kinetics = EIS-TLM(Kim 2025) 영역**" 명시.
  - ★ **uncoated NCM811/LPSCl R_ct = LNO-coated 의 ~20×**(62: 22.4→453.4 Ω·cm²) = 산화분해가 전하전달을 ~20× 느리게.
    **= Kang 2025 "계면분해→Li-구배→균열"(역학)의 *kinetics* 짝**(같은 황화물-계면 분해, 한쪽은 균열·한쪽은 R_ct↑).
    LNO(Kim)·LZO(Kang) 둘 다 *화학* 패시베이션 코팅(우리 coverage=*기계* 와 종류 다름). → "계면"을 랩 *공동 future 축*
    (structure-σ 우리 / mechanics Kang / kinetics Kim) 으로 명문화.
  - ★ **T-dependent σ (활성화에너지) = 우리 *미보유* 온도축 (model extension 후보).** 온도 스윕 → **E_a 서열
    R_ct(~0.42 eV) ≫ R_i,gb(~0.6 eV) > R_w > R_i,bulk**(작음); R_ct·GB 가 가장 thermally-activated(율속). ⚠ E_a
    절대값은 논문이 명시 표로 안 줌 → R(T) 3점 Arrhenius 추정(TREND-only). 우리 σ-솔버는 *상온 단일* → σ(T) =
    σ(300K)·exp[−E_a/k(1/T−1/300)] 형태로 T-축 추가 가능. (우리 σ_thermal=*열전도*지 *전도도의 온도의존* 아님 — 다른 축.)
  - ★ **modified TLM 2-BC 분해 = 우리 솔버 검증의 *방법론* 교훈:** R_int/R_i 비가 작으면(coated full-cell) 이온수송·
    전하전달 영역이 *겹쳐* full-cell 단독 분석이 오해 → **대칭셀/uncoated 병용 필수**(Morasch). ⇒ 우리가 실험 R_ion 을
    σ_ionic 앵커로 쓸 때 *깨끗이 분리된 셀의 R_ion* 만 쓸 것 (Bazzoun/Minnmann 이 대칭셀/full-blocking 쓴 이유).
  - **도전제 형상(0D Super P vs 1D VGCF):** VGCF 가 전자저항·R_int 둘 다 낮춤(1D 전자망 + SE-카본 계면면적↓ → 산화분해↓)
    = Lee 2025 VGCF σ_e 와 같은 결 → 우리 σ_e 도전제 형상 구분 약함 보강(우리 production = Super P 0D 가정).

- **📌 Li(Yang) 2026 ECER 리뷰원고(심사중) — 우리 미보유칸의 가장 체계적 카탈로그 (F축 지도; digest
  `papers/li2026_sulfide_stability_review_ecer.md` §13c)**:
  - **화학 축 전체 미보유 (우리 DEM/MPM/STEP4 모두 반응항 없음):** ① 공기 — H₂S/가수분해/HSAB(H₂O 흡착 E_ad LPSC −1.63
    → O/F 치환 −1.19 eV; DFT 흡착에너지 스타일은 우리 E_bind 트랙 참고) ② 용매 — 극성/donor-number 공격(건식공정 정당화
    문헌) ③ 열 — 고유 400–500 °C ↔ NCM O-방출 200–300 °C 계면 발열(성형압→P₂Sₓ층→발열 −40–50 % 커플) ④ 전기화학 —
    LGPS 창 1.7–2.1 V·산화 ~2 V·분해 캐스케이드(LPSCl→Li₃PS₄→P₂S₅→P₂O₅·LiCl·SOₓ)·계면 3분류(안정/MCI/패시베이션)
    [116] — STEP4-v2 전압경계·SDCP 부산물 해석의 화학 맥락으로만 차용.
  - **덴드라이트·Li/SE 계면 물리 미보유:** SE 내부 핵생성(pore·GB·전자전도 시너지→CCD↓)·wedge-opening 성장[177]·
    void 진화(탈리속도>공공확산)[186,188] — Li금속·분리막 SE가 우리 도메인 밖. 단 **작동압 창 정량(void 상도[189]·Li
    변형지도→CCD[191])**은 우리 fab-vs-operating 구분의 음극판으로 인용 가치.
  - **사이클 시간축(A10)**: 리뷰 미래방향 ② "in-situ + 멀티스케일 시뮬로 동적 계면 진화" = 우리 A10(사이클 chemo-mech)
    칸의 리뷰급 수요 선언; 사이클 후 void XCT 3.95→1.19 %[161] = 그 축의 목표 데이터 스타일.
  - **SCL(공간전하층) 뉘앙스**: "SCL은 유일 원인 아님 — 화학 부산물 축적이 더 직접적"[116,133,136] — 계면 임피던스
    해석 시 SCL 과대해석 경계(우리 STEP4 ASR 해석에도 적용).
  - ★ **역방향 확인(우리가 채우는 칸):** 이 리뷰가 "구조→수송 정량"을 [140 Bielefeld·150 voxel-sim·151 압력-구조·152
    구배] 단 4편 인용으로 처리 = 239 refs 분포 자체가 **우리 DEM σ-삼중항+MPM morphology+STEP4 DFN 공백의 증명**;
    +**우리 랩 Kim2024를 ref[147]로 인용** = 우리 앵커 계보의 리뷰급 승인. 미래방향 ①(고유안정 재료설계)·④(평가 표준화 —
    두께·로딩·시험압력·사이클 조건 통일)은 우리 범위 밖이되 ④는 fab≠operating 압력구분(Doux 합류) 서사 지원.
  - ⚠ **미출판 심사중 원고(ECER-D-26-00097)** — 인용은 "manuscript under review"로만, 수치는 1차문헌 cite.

---
## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

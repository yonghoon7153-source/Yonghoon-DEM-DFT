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
> **★★★Zunker&Kamrin 2024 I·II + 2025(MDR 접촉모델 3부작 — *우리 18× 연화의 가장 강한 반례 후보* + 층(2.75) 신설; §A·§C·§F)**,
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
>
> ## 🎤 발표 덱 (papers/ 보다 한 등급 낮음 — `talks/README.md`)
> **[YMLee26-DTBL]** `talks/lee2026_yonsei_dtbl_ai_electrode_digitaltwin.md` — **이용민(연세대 DTBL),
> "AI를 활용한 전극 미세구조 디지털화 기술과 물리 기반 배터리 시뮬레이션"** (2026 Korean Battery Symposium,
> 8/21, 자료집 pp.259–278, 인쇄 슬 39장; 사용자 분류 `(미분류)`).  **우리 DEM+MPM 계보의 *상류 그룹이 스스로
> 그린 2026년 지도 + 자기 한계 목록***.  정본 4편은 이미 보유 — `papers/park2020_...`·`kim2024_...`·
> `lim2025_...`·`song2025_...` → **수치 인용은 논문에서, 덱은 지도로만.**
> - **✅ 재확인된 우리 positioning 2건**: ① 2026년 발표에서도 구조 *생성*은 **PSA/SEM 기반 규칙 배치**(GrainGeo,
>   seed 1–5)로 유지 = **압축 물리 미시뮬** → 우리 predict-from-powder 차별 유지; ② 캘린더링은
>   **reconstruct-then-compress**(ElastoDict) → 우리와 형제·직교(§C 참조).
> - **🆕 새로 드러난 우리 공백 2건 (이 덱이 아니었으면 몰랐다)**: ① **DEM 슬러리 믹싱 + "2nd solvent" 모세관
>   가교로 CBD migration 억제**(슬 34, ACS EL 10 (2025) 6223-6235) — **같은 도구(DEM), 다른 물리(습식·모세관)**
>   → `positioning_vs_geodict.md` 의 "DEM은 우리 것" 뉘앙스를 **"건식 압밀 + granular constriction σ + 소성 MPM"**
>   으로 좁혀 다시 써야 함; ② **OWRK 기반 work of adhesion·계면에너지 실측**(슬 33) = 우리 DEM 부착
>   파라미터(DMT/JKR) 문헌 차용을 **측정량으로 바꾸는 경로**.  둘 다 **정본 미보유 → 수치 인용 금지.**
> - **🆕 우리에게 유리한 새 논거 1건**: 슬 22 **"황화물 SE·폴리머는 *측정 과정 자체가* 구조를 왜곡한다"**
>   (공기 부반응 / 열손상) ⇒ **재구성(top-down)이 원천적으로 취약한 소재계에서 bottom-up 생성의 가치가 커진다**
>   = 우리 positioning의 *소재-특이* 정당화(기존 문서에 없던 각도).  ⚠ 정본(Chem. Eng. J. 522 (2025) 167791 /
>   AEM (2026) e05319) 확보 전 **인용 금지**(digest §13-3).
> - **저비용 흡수 1순위**: **REV/voxel 수렴을 *비용축과 함께* 한 장에 보고하는 그림 양식**(슬 19 —
>   voxel 50–600 nm × domain 15→90 µm × 메모리/시간).  우리 domain·voxel 선택 근거 문서화 공백을 메움.
> - ⚠ **소재계 혼재 주의**: 덱의 캘린더링·CBD migration·OWRK·DEM 믹싱은 **LIB 액체계(NCM622/811+PVDF/NMP)**,
>   구조 생성/검증만 **황화물 ASSB(NCM711+LPSCl+NBR)**.  같은 표에 섞지 말 것.
>
> **[Moon26-CAU]** `talks/moon2026_cau_llm_agent_battery_automation.md` — **문장혁(중앙대 에너지시스템),
> "AI 기반 배터리 연구 자동화: LLM 기반 연구 분석에서 AI-Agent 전극 모델링까지"** (전지기술 심포지엄 2026
> 기술세션 3-4, 8/21, 자료집 pp.297–318; **덱 실물 전 22 pp 독립 재판독 2026-08-03**, 사용자 분류 `(미분류)`).
> 본체는 **LLM 다중 에이전트(BEARS)** 지만, 04부(슬 25–39)가 통째로 **전극 미세구조 생성–검증–FEM** 이라
> 우리 DEM 축과 직접 겹친다.  ⚠ **소재계는 흑연 음극(LIB)** — 황화물 ASSB 아님.  같은 표에 섞지 말 것.
> - **🆕 그들 파이프라인 = ARTISTIC 골격 + 에이전트 운전** (슬 28, 재판독으로 새로 편입):
>   `합성 실험 설계 → 제조 물리 모델링(Slurry→Drying→Calendering) → 전극 물성 계산(전자전도도·굴곡도·
>   활성표면적·밀도) → 결정론적 학습(surrogate) → 다목적 최적화` + 실험설계로 되먹임.  단계 대 단계로
>   `papers/ngandjong2021_dem_calendering_digital_twin.md`·`papers/duquesnoy2023_ml_multiobjective_manufacturing_optimization.md`
>   와 대응한다 ⇒ **BEARS는 새 물리가 아니라 ARTISTIC 파이프라인의 자동 운전 버전**.  우리 차별은
>   `positioning_vs_geodict.md` 가 좁힌 정의(**건식 압밀 + granular constriction σ + 소성 MPM**)로 그대로 유지.
> - **🆕 우리 bimodal 명제와 같은 물리, 다른 도구 — 단 트레이드오프까지 옮길 것** (슬 37–38):
>   흑연 전극 **80개(Single 55 / Binary 19 / Gradient 6)** 를 고정 로딩(**30 × 30 µm footprint · 8 mg/cm² ·
>   95:3:2**)에서 생성 → 구조공간(`D_eff = D·ε^β`, τ_z vs ε, 가이드 α=1.9 Ebner/1.7/1.5 sphere) → **5개만**
>   전기화학 검증.  **3C: HC05 binary 56.8 > HC06 53.4 > GRD01 45.4 > SPH010 33.6 > HC01 single 16.8 mAh/g
>   (= 3.38×)**, 그러나 **0.5C 에서는 binary 가 single 대비 −6.4 %**.  ⇒ 우리 bimodal DEM 결과를 번역할 때
>   **"고율에서만 역전"** 으로 써야 정확하다(고율 이득만 인용하면 문헌 부풀리기).  ⛔ 덱 소환값, 절대값 인용 금지.
> - **🆕 굴곡도 단독으로 rate 를 설명 못 한다는 외부 관찰**: **SPH010 은 τ_z ≈ 1.55 로 5개 중 최저인데 3C 순위 4위**.
>   우리 DEM/BVSE 문서의 "단일 기술자로 순위 매기지 않는다" 규율의 외부 근거.  ⚠ SPH010 만 입자 형상이 달라
>   (구형) 변수 분리가 안 돼 있다 — **관찰까지만, 인과 단정 금지**.
> - **🆕 확보 1순위 정본 (`papers/` 미보유)**: 슬 32가 인용한 **Chouchane, Yao, Cronk, Zhang, Meng,
>   "Improved Rate Capability for Dry Thick Electrodes through FEM and Machine Learning Coupling",
>   *ACS Energy Lett.* 2024, 9, 4** — `Library of Real Particles → Stochastic Generation → FEM → 입자별 평균 SOD →
>   Random Forest` 워크플로.  **Chouchane 은 ARTISTIC(Franco) → Meng 그룹 계보**라 우리 DEM 트랙의 직접 선행이다.
> - **🆕 검증 지표 공백 노출**: Validator Agent 가 생성 구조에 **8종 구조 검증 지표**(형태·수송·통계)를 돌린다고만
>   적혀 있고 항목은 미공개(digest Q7).  우리 DEM 산출 구조에도 같은 종류의 **고정 검증 세트**가 없다 —
>   `kb/open_items.md` 후보.
> - **🆕 파이프라인 상하류 접점이 포맷 수준까지 특정됨**: 슬 39 Simulator 단계의 solver 실행이 **DIS / EIS / P2D**.
>   우리 M5(P2D 파라미터 export)의 소비자가 구체화됐다.  또 그들 메모리층 이름이 **`docs/knowhow (INDEX.md)`** 로,
>   우리 `litdb/INDEX.md` 와 **같은 부품**이다 — 우리에게 없는 건 저장소가 아니라 그 위의 orchestration 루프.
> - ⚠ **덱 등급**: BEARS 는 arXiv, Battery-Sim-Agent 는 ICLR 2026 under review.  **수치 인용 금지**,
>   구조·절차만 가져온다.

## A. 압밀 / porosity (E_SE 강성이 floor를 정한다)

> ⭐ **2026-08-05 추가 — [Famprikis19] (Nature Materials 2019 리뷰, `papers/famprikis2019_fundamentals_inorganic_sse.md`) 가 이 축에 준 것**
> **DEM 을 하지 않는다(단어 0회). Bruggeman·tortuosity 식도 없다. 기공률·상대밀도·성형압·입경 수치도 없다.**
> 그럼에도 **DEM 이 왜 필요한지를 가장 권위 있는 형태로 정의해 놓은 문헌**이라 여기 기록한다.
> - **정량은 딱 2개**: 복합양극 SE 부피분율 **< 50 %**(에너지밀도 + **전자 percolation**) / **> 25 %**(**이온 percolation** 한계 회피) — 둘 다 **ref 68 = [Bielefeld19]**(우리 digest 보유). 그리고 **"이 문턱은 입도(분포)의 함수이며, 입자가 작을수록 전자·이온 문턱이 둘 다 낮아지고 전하이동 유효면적이 커진다"**(refs 68,74,76). ⇒ **우리 DEM 조성 sweep 의 경계조건으로 바로 사용 가능한 유일한 정량 제약.**
> - **ASR = t/σ** 이고 *"계면 임피던스 기여는 **복합체 단위부피당 이온접촉 면적** 에만 의존한다"*(ref 68) ⇒ **접촉면적을 계산하는 일 = 계면 임피던스를 계산하는 일.** 단 리뷰가 trade-off 를 명시: **"바로 그 접촉면적이 사이클 중 저항성 계면 형성·열화에 노출되는 면적"**.
> - **기공률 ↓ ⇒ 전도도 ↑**, 기구는 **grain–grain / particle–particle 접촉 강화** — **산화물(ref 55 = Kim 2016, hot-pressed LLZO **상대밀도↔기계물성**)·황화물(ref 58 = [Sakuda13], 우리 digest 보유) 양쪽에서 확인**. 기공은 **tortuous 경로 + 불균일 전류밀도**를 낳는다(단어만, 식 없음).
> - **`Fig. 1` 캡션이 기공률을 "비활성 부피"로 명시**: *"inactive volume (solid electrolyte, current collectors, **porosity**) should be minimized"*.
> - **황화물·보로하이드라이드는 연질이라 상온에서도 치밀화 가능**, 산화물은 소결 필요. **냉간가압이 랩 표준이나 스케일업·경질 산화물엔 제한적**(ref 118 Schnell). SPS 는 미세구조 정밀제어의 기준이나 **비용상 금지적**(refs 51,117). → `Fig. 7` 의 **'Pellet-type'(건식·냉간가압) vs 'Sheet-type'(슬러리)** 두 종착점이 우리 DEM 시나리오 분기와 정확히 대응.
> - 균열 전파 제어 인자 = **입경(ref 55)·기공률·기존 균열(ref 12)·기공 연결성(ref 137 Shen/Hatzell, 싱크로트론 토모그래피)** — **기공 연결성은 DEM 출력 그 자체**.
> - **Li 금속 항복강도 ~0.8 MPa**(ref 144 = Masias 2019, 탄성·**소성·크리프** 전부) 이고 금속음극은 **MPa 급 압축응력** 하 ⇒ **Li 는 항상 소성 영역** = DEM Li 접촉모델의 σ_y 앵커.
>
> **★ 가장 중요한 한 줄 (포지셔닝)** — `Fig. 2` 의 방법 스팬 바를 보면 **NMR·MD 는 Å–nm 에서 끝나고 그 위는 곧바로 `Continuum modelling`·`Impedance spectroscopy` 로 점프한다. µm 입자 스케일의 이산(discrete) 역학 방법이 사다리에 없다.**
> 그런데 같은 그림의 **Device(mm) 칸에는 `Contact area` 가 서술자로 그려져 있다.** continuum 은 접촉면적을 **입력으로 받는** 방법이지 **만들어내는** 방법이 아니다.
> ⇒ **DEM 이 정확히 그 빈칸이다. 우리 repo 이름(DEM-DFT)의 정당화가 이 그림 한 장으로 끝난다** — DFT 가 왼쪽 끝(E_hop·E/G·γ·ESW), DEM 이 가운데(패킹·기공률·접촉면적·배위수), continuum/EIS 가 오른쪽. **deck 표지 슬라이드 1순위.**
> ⚠ 정직하게: 2019년에는 SSB DEM 문헌이 거의 없었다(우리 litdb DEM 논문 대부분 2020–2026). **리뷰의 오류가 아니라 연대적 공백** — 그래서 *"Famprikis 2019 가 정의한 빈칸을 2020년대 DEM 이 메웠다"* 는 서사가 성립한다.
>
> **DEM 입력 파라미터 조달 현황** (digest §6.2 전체 표):
> | 입력 | 조달처 | 상태 |
> |---|---|---|
> | 법선강성 k_n (∝E) | 우리 `elastic.json` relaxed-ion **E_VRH 22.06(comp1)/27.66(modelc) GPa** ↔ 리뷰 소환 실측 **E ≈ 20 GPa**(ref 108) | ✅ 자급 + 외부 앵커 일치 |
> | 접선강성 k_t (∝G) | 우리 **G_VRH 8.13 GPa** ↔ 리뷰 소환 **G ≈ 7 GPa** | ✅ 자급 + 일치 |
> | 점착 Δγ (JKR/DMT) | 우리 `adhesion.json` **γ_SE 1.211 / W_ad 1.107±0.027 J/m²** ↔ 리뷰 **γ_xfc 정의만(수치 0)** | ⚠ 정의 일치, 문헌 수치 없음 |
> | pull-off 응력 σ_adh | 리뷰 = **개념 + 계면저항과의 상관 실증(ref 107)**, 수치 없음 | ⚠ 우리 W_ad→σ_adh 환산 미수행 |
> | Li 소성 σ_y | **0.8 MPa** (ref 144) | ⚠ **외부 조달 완료** |
> | SE 입자 σ_y | 없음 | ❌ 공백 |
> | 파쇄 판정 K_Ic | **리뷰에 수치 0** ("**미세구조 의존 → 실험으로만 결정**") | ❌ 공백 (litdb 유일 소환값 = [Fan26] 0.2–0.4 MPa·m¹ᐟ²) |
> | 마찰계수 µ | 리뷰에 **언급조차 없음** | ❌ 이 리뷰 밖 |
> | 혼합 제약 φ_SE | **25 % ≤ φ_SE ≤ 50 %** (ref 68) | ✅ **바로 사용 가능** |
>
> **조달 추천 (전부 litdb 미보유, 우선순위순)**: ① **ref 75** Froboese …**Kwade** 2019 *JES* 166, A318 — ASSB 전극의 **미세구조↔이온전도도**(tortuosity 실측) ② **ref 137** Shen, Dixit, Xiao, **Hatzell** 2018 *ACS EL* 3, 1056 — **기공 연결성↔덴드라이트, X-ray 토모그래피** ③ **ref 144** Masias 2019 *JMS* 54, 2585 — **Li 금속 탄성·소성·크리프** ④ **ref 55** Kim 2016 *JACerS* 99, 1367 — **상대밀도↔기계물성**(hot-pressed LLZO) ⑤ **ref 108** McGrogan 2017 *AEM* 7, 1602011 — E/G 실측 원전(시편 밀도 확인용).

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
- ★★★ **정정 2026-08-25 — multi-contact `F_mc` 는 우리 18× 연화와 *부호가 반대다*** (원전 digest
  `papers/giannis2021_stress_based_multicontact_dem.md`; 그동안 Varkey 2026 의 2차 인용으로만 갖고 있었다):
  - 원전 결론 문장 그대로 — *"The new multi-contact approach is able to provide a **higher force at a given
    displacement** than the classical DEM"*. Fig 7·9 도 **MC-stress 가 최대겹침을 가장 작게** 만든다.
    ⇒ **침대를 뻣뻣하게 = 같은 압력에서 porosity ↑.** 우리 연화는 겹침을 **늘리는** 장치 = 반대 방향.
  - 그래서 `elasto_plastic_feasibility.md §1 경로 B` 와 `papers/varkey2026_*.md §7` 의 *"같은 증상(치밀영역
    **과강성**) 다른 처방"* 은 **틀린 서술**이다. 고쳐야 할 것은 과강성이 아니라 **under-stiffness**(고변형에서
    힘을 과소예측). ⚠ varkey 카드의 **Supplementary 절은 이미 "TN 단독이 FEM 을 under-predict"** 라고 옳게
    적어 두어 **본문 표와 SI 절이 서로 모순**이었다 — 이 정정으로 SI 쪽이 맞는 것으로 확정.
  - **우리 침대에 대입한 크기** (★ 우리 유도, 논문 수치 아님 — 유도·검산은 카드 §7-4):
    `ΔF/F = k·β·ν·C·(δ/d)`, k = 0.25…1.5 (논문 **자신의** 정규화 3종 × branch-vector 2종 = **6× 모호**),
    β = 1.65–5.17 (논문 전 범위, **LPSCl 실측 n/a**), ν = 0.37, C ≈ 6.5.
    | 우리 침대 | δ/d | ΔF/F | 필요 연화 18× → |
    |---|---|---|---|
    | pure-SE (Cronau ⟨δ⟩ ≈ 11 % of d) | 0.11 | **+11 … +205 %** | **20× … 55×** |
    | production 복합 (AM 차폐, ⟨δ⟩ 1.75 %) | 0.0175 | **+2 … +33 %** | **18× … 24×** |
    ⇒ **경로 B 는 18× 연화를 제거하지 못한다 — 오히려 늘린다.** 크기도 부족(힘 최대 3.05× vs 연화 18×).
    복합양극에선 사실상 무시 수준(+2…+33 %)이고 의미가 생기는 곳은 **pure-SE separator/펠릿뿐**.
  - **올바른 짝짓기**: 항복캡(경로 A)은 치밀영역을 *과도하게 물러지게* 만들고(Varkey SI Fig S1: Thornton–Ning
    단독이 5 mm 에서 FEM 9.7 vs **5.7**×10⁴ N), **F_mc 가 바로 그것을 되돌리는 짝**이다.
    ⇒ **F_mc = 연화의 경쟁자가 아니라 경로 A 의 파트너.** Varkey 스택(TN + F_mc)이 이미 조립된 레시피.
  - ⚠ **압력·소재 전이 한계**: Giannis 2021 의 최대 응력은 **유리 45 MPa**(우리 300 MPa 의 1/6.7)이고
    **porosity·상대밀도를 한 번도 보고하지 않는다.** "ρ>0.7 에서만 유효"는 **Varkey 의 서술이지 Giannis 의 것이 아님.**
    소재도 하이드로겔(23.3 kPa)·고무(1.85 MPa)·**유리(65 GPa)** 뿐 — LPSCl(22–24 GPa)에 그나마 가까운 건 유리.
    저자 outlook 이 *"elasto-plastic behaviour at **high stress levels**"* 를 **향후 과제**로 명시 = 우리 300 MPa 영역은
    이 모델의 검증 밖. 유리도 *"brittle 이라 **elastic part 만** 본다"*.
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

- **★ Luan 2025 AFM (`luan2025_graded_cathode_400whkg_pouch`) — 압력 층위는 완벽히 일치, 그런데 porosity 를 안 준다.**
  산업 파일럿(GRINM)이 **우리와 같은 소재계·같은 성형압**으로 4 mAh cm⁻² graded 양극과 5 Ah 파우치를 만들었다:
  **양극 성형 300 MPa (= 우리 production 과 동일)** · SE층 예압 100 · 셀 consolidation 200 ·
  **파우치 등방압(isostatic) 500 MPa 2 min** · **사이클 중 스택압 30 MPa**.
  ⇒ **fab-vs-operating 3종 압력 구분(Doux/Cronau/Minnmann)의 4번째 실물 사례**이고, 작동압 밴드에
  **30 MPa** 가 추가된다(Doux 5 최적 · Minnmann 40 측정 · Lee2025 2 · **Luan 30 운전**).
  - ⛔ **그런데 porosity·전극밀도·두께가 논문 어디에도 없다**(SI Fig S6b 가 단면 두께 그림이나 우리 SI PDF 미보유).
    같은 300 MPa·같은 소재인데 **우리 real_14 15.6 % 를 검증할 유일한 기회를 놓쳤다** → A축 정량대조 **불가**.
    **위시리스트: SI 원본 확보 시 Fig S6b 두께로 대조 성립.**
  - ⚠ **등방압 500 ≠ 단축 300.** 파우치 공정은 유체 등방압이라 편차응력 상태가 우리 단축 다이와 다르다 →
    **porosity·이방 tortuosity·접촉면적 전이 금지**(같은 MPa 라도 같은 압밀이 아니다).
  - ★ **DERIVED(ours) 두께 환산 — 우리 RVE 가 얇다**: 그들 4 mAh cm⁻² 는 (200 mAh g⁻¹, CAM 91.5 wt%,
    ρ_electrode 3.2–3.4 g cm⁻³ **ASSUMED**) ⇒ **≈65–70 µm**. 우리 real_14 는 **30.3 µm ≈ 1.6–2 mAh cm⁻²**.
    그리고 그들 Fig 2d 는 **1 mAh cm⁻² 에선 CAM 95 % 도 멀쩡**하다고 한다 ⇒ **우리 production RVE 두께대는
    구배 효과가 거의 안 나타나는 영역**이다. Phase-5 층상 케이스는 **두께 2–2.5×** 로 키워야 신호가 난다
    (⚠ MPM 격자 부담 + `d_h/dx ≳ 3.5` 규칙 재점검 동반).

- **★★ [Zhang23] (Joule 2023, `papers/zhang2023_pfib_multiscale_imaging_4d_thick_cathode.md`) — 압밀이 균열의 주범이라는 *3D 실측***
  (⚠⚠ **액체 전해질 LIB**. chemistry 게이트 = liquid → **FORM·METHOD-ONLY**. AM 만 NMC811 로 우리와 동일):
  - ★★ **압연 균열 vs 사이클 균열의 크기 분리 (우리가 못 재던 값)**: PFIB-SEM 3D 로 **원(raw) NMC811 분말
    0.12 % → 압연된 pristine 전극 7.13 %** (균열 부피 / 이차입자 부피). 15 사이클 후는 **7.77 %(+9 % 상대,
    4.4 V) / 8.85 %(+24 %, 4.7 V)** 에 그친다. ⇒ **균열의 지배적 기여자는 사이클이 아니라 압밀(압연)이다** —
    **우리가 이미 모델링하는 단계**가 열화의 최대 원천임을 실측이 말해 준다. 우리 Auerbach fracture ·
    MPM crack-void 스캐폴드의 **방향·순서 검증 표적**.
    ⚠ **절대치 인용 금지 3가지**: (a) **압연압 미보고**(우리 300 MPa 단축 냉간가압과 같은 상태인지 불명),
    (b) **주변 매질이 CBD/공극**(우리는 SE 분말이 하중을 나눠 받는다 = AM 차폐 구조가 다름),
    (c) **n=1, error bar 없음, 15 사이클로 짧음**. ⇒ 쓸 것은 **"압연 ≫ 사이클" 이라는 순서와 ×59 자릿수**뿐.
  - ⚠ **porosity 는 부호가 반대다** — 그들 **29 %(세그멘테이션) / 25 %(Methods)** 는 **설계 목표**(전해액 통로)이고,
    같은 값이 황화물 ASSB(우리 7.4–15.6 %)에서는 **실패**다. 우리 코퍼스 상단(32.8 %)이 그들 값을 포함하지만
    **"같은 수, 반대 의미"** 로만 기록할 것. **압밀곡선·Heckel 대조 대상 아님**(그들에게 압밀 모델 자체가 없다).
  - ★ **두께방향 비균질이 실재한다는 실측**(Fig 1D): CBD 는 평탄한데 **NMC 부피분율이 집전체로부터 ~45–55 µm
    구간에서 48–50 %로 함몰**하고 pore 가 35–40 %로 상승. ⇒ 우리 **graded-z(백로그 A7)·Phase-5 층상**의
    "제조가 만드는 비균질" 전제에 대한 **외부 실측 지지**(정성).
  - **두께·면용량 접점**: 그들 **80–85 µm / 6 mAh cm⁻² / 30 mg cm⁻² / 비활성 5 wt%**. **우리 6 mAh 트랙
    (111–116 µm, RVE 50×50 µm, 300 MPa, AM:SE ≈ 81.6:18.4 wt%)과 면용량이 정확히 같다** — 같은 면용량에서
    우리가 더 두꺼운 것은 **SE 가 부피를 먹기 때문**이지 설계 열위가 아니다(원고에서 반드시 이렇게 쓸 것).
  - ⚠ **그들 "두께 임계 ≈ 240 µm"(−30 % 용량 @C/3, Fig S9)는 전이 금지** — 기전이 **액체 전해질의 농도구배**다.
    황화물은 단일이온 전도체라 그 항이 없고 한계는 **퍼콜레이션**이다. **개념(임계가 존재한다)만** 전이,
    **값과 기전은 우리가 따로 내야 한다.** ★ 부수적으로 이 그림이 방법론 논거를 준다 — 이미징-우선 논문조차
    **두께를 설계변수로 삼는 순간 실측을 버리고 확률생성 전극으로 갈아탔다**(§F 참조).

- **★★ Alabdali 2023 (`alabdali2023_cgmd_wet_manufacturing_ssb_cathode`, JPS 580, 233427) — Weitze 의 *선행편*.
  같은 그룹·같은 습식 사슬의 1호(구형 AM, LAMMPS CGMD)이고, 압밀 축은 Weitze 보다도 더 비어 있다.**
  - **ε–압연도 3점 (fig-label)**: **35 %(0 %) / 21 %(25 %) / 15 %(50 %)**, 두께 **46 → 23 µm**(Fig 1).
    ⚠ 같은 논문 Fig 3a/3b 의 프로파일 종단은 **≈63 → ≈30 µm** 로 **1.37배 다르고 논문이 설명하지 않는다**
    → 두께 인용 시 **어느 그림 기준인지 명시**.
  - ⚠⚠ **압력·평판 하강속도가 어디에도 없다** (Weitze 와 같은 결함이되 **더 심하다** — Weitze 는 springback 이라도 낸다).
    ⇒ **Heckel/P_y 대조 원천 불가**.  우리 300 MPa·P_y=138·H_AM 축은 **이 계열 2편 전체에 대해 독립 우위**.
  - ⚠ **ε_cal 15 % ↔ 우리 real_14 15.6 % 는 "우연"으로 취급**: (i) 압력 미상 (ii) CBD 가 3.4 wt% 로 **≈20 vol%**
    를 먹는 다른 고체 조성 (iii) porosity 정의 미보고(우리 **ε_sphere 아님**) (iv) 그들 값은 **CBD 나노공극 제외**
    인데 실험 대조(≈50 %)는 **CBD 를 50 % 나노공극으로 치는 다른 규약**에서 한다(=한 표에 넣지 말 것).
  - ★★ **재료 강성이 *아예* 없다** (Weitze 는 JKR E=135 GPa 라도 준다).  유일한 강성 = GH `k_n`,
    **DERIVED(ours)** 단위환산 `1 pg µm⁻¹ µs⁻² = 1 kPa` ⇒ **건조 k_n = 1.0×10⁵ Pa**; `k_n≡(4/3)E*` 로 읽으면
    **E\* ≈ 7.5×10⁴ Pa** = 우리 E_eff **1.35 GPa 의 1/13,500**, 실물 LPSCl 22–24 GPa 의 **~1/2×10⁵**.
    게다가 건조 AM(d=10 µm) LJ 우물 **ε = 1 pJ = 2.4×10⁸ kT** 라 **법선 반발의 주역은 Hertz 가 아니라 LJ 로 보인다**
    (자릿수 논증, ours — 논문은 이 분해를 안 한다).  ⇒ **Varkey(halide E 10.58 → floor 21/37 %) 식 E→floor
    사다리에 이 논문을 얹지 말 것.**
  - ★ **"고체다움"의 표현이 우리와 종류가 다르다 — 연화(softening)가 아니라 *단계별 FF 재파라미터화*.**
    슬러리→건조에서 **LJ 우물 ×19–455 · k_n ×1000 · 마찰 X_µ 0.016→12.5(×780)**.  우리 규약은 실제 E 를
    **명시하고 배수로 낮춰(18×) 감사 가능**한데, 그들은 **참조 물성이 없어 감사 자체가 불가능**하다.
    ⚠ 공정하게: 젖은 슬러리와 마른 전극을 **다른 FF 로 표현하는 것 자체는 물리적으로 타당**하고, **그 단계 전이는
    우리가 갖고 있지 않다**.

- **★★★ Coetzee 2017 (Powder Technol. 310, 104–142, `papers/coetzee2017_dem_calibration_review.md`) —
  "E_eff = 1.35 GPa 18× 연화가 정당한 방법론인가"에 대한 *방법론 정본*.  A 축에 붙이는 이유: porosity floor
  논쟁의 근거가 되는 그 E_eff 를 **어떻게 정했느냐**가 여기서 판정되기 때문.**
  (⚠ 배터리 무관 — 파쇄암·모래·곡물·유리구슬의 **저응력 벌크 핸들링** 리뷰.  `Heckel` 0회, `plastic` **1회**.
   **방법론만 전이, 파라미터·가드레일 전이 금지.**)
  - **① 벌크 역보정은 표준이다 — 이 축의 헤드라인.**  리뷰는 두 학파를 명명하고
    (**Direct Measuring** vs **Bulk Calibration**), 역보정을 *"a calibration approach in the **true sense of
    the word**"*(p.106) · *"**by far the most popular** approach"*(p.138) 로 규정한다.  결정적 문장(§9 p.138):
    *"the particle **shape can be simplified** and **assumptions in terms of the contact model can be made**.
    The calibration process will then **reduce the effect that these simplifications … might have** on the bulk
    behaviour since **the other parameters will compensate for it.**"*
    ⇒ **우리 18× 연화의 인식론(frame[2]: "결손 럼핑 프록시")을 문헌 규범으로 뒷받침하는 유일한 카드.**
  - **② 직접 측정은 우리 입경대에서 원리적으로 불가.**  리뷰: 직접측정 시도는 전부 *"**millimetre and above**
    size range"*(p.106), 최소 사례가 **500 µm** 입자의 접촉 마찰[218](p.134).  우리 LPSCl SE ≈ **직경 1–3 µm**
    = **2–3 자릿수 아래** ⇒ *"the Direct Measuring Approach is not available at our particle scale"* 는
    **인용으로 방어되는 문장**.
  - **③ 우리 시험 종류가 리뷰의 표준 목록 안에 있다.**  Table 1 (p.124) `Uniaxial compression test (bulk
    stiffness)` + Table 3 (p.137) `Confined bulk stiffness (**oedometer**)` — **그 행에서 관계가 조사된 유일한
    파라미터가 접촉강성**.  이유(§5.5 p.131): *"the confined uniaxial compression test was **only** influenced
    by the particle stiffness while the particle-particle friction coefficient had **no significant effect**"*
    ⇒ **구속 단축압축 = 강성을 고립시키는 시험**.  우리 300 MPa 냉간압축이 정확히 이 칸.
  - **④ 강성 낮추기의 두 갈래를 절대 섞지 말 것 (인용 규율).**
    · **(a) 보정**: 측정된 벌크응답에 맞춰 강성을 정함 (Table 1 의 8개 시험족).  ← **우리는 여기.**
    · **(b) 속도**: 타임스텝을 키우려 강성 감소 (§7 p.135–136).  정당성 조건 = **"벌크가 안 변할 것"**.
      실측 폭: Hart ÷100(÷1000까지 무해) · Goetsch ÷21(더 줄이면 유량 변화) · Yan **E 0.02→200 GPa 거시량 무영향** ·
      Xu **70 MPa vs 70 GPa, 배출률 편차 2.7 %·계산 31.6×** · Chung&Ooi ÷10⁴ (평균력 무영향, **힘 요동만 감소**).
      가드레일: Cleary **0.1–0.5 %** · Paulick **≤ 반지름의 1 %** · Höhner **≤4 %**(그 계 한정).
    ⚠ **(b)의 가드레일로 우리를 방어해도, 그것으로 우리를 재도 안 된다** — 우리는 벌크가 *바뀌기를* 원해서 낮췄다.
    다만 **사실 고지**: 우리 pure-SE ⟨δ⟩ ≈ **직경의 11–12 % = 반지름의 22–24 %** → Paulick 기준의 **~22×**.
    (그 영역에서 ε_sphere↔ε_union 규약차가 커진다 — 우리 실측 **1.251 %p**.  porosity 규약 명시 필수.)
  - **⑤ "밀할수록 강성이 더 중요하다" — Paulick [235] (p.136)**: *"the **denser** the system, the **more
    important** the stiffness value becomes"* + **접촉강성↔벌크강성 선형**(Lommen [81] 구속압축에서도 확인).
    ⇒ 300 MPa 로 잼된 침대에서 **E 는 최대 민감 레버**라는 방향이 전이되고, **우리 MPM 의 "E 가 지배 레버,
    σ_y 아님"** 관측과 부호가 같다.
  - **⑥ 연화의 *방향*에 문헌 기전이 하나 있다 (배수는 n/a).**  §8 (p.136) **Van Lew et al. [236]** —
    세라믹 펠릿 42개 E 를 개별 측정해 **Weibull 분포**로 DEM 단축압축에 넣으면 *"the sample with a distribution
    in Young's modulus showed a **softer response** compared to the sample with a constant Young's modulus"*
    (+ 파단 입자 비율도 낮아짐).  같은 방향 두 번째 사례 = **Molenda [230]** μ 분포 → 더 무른 응답.
    ⇒ **불균질을 단일 유효값으로 럼핑하면 그 유효값은 재료값보다 낮아야 한다**는 *방향*만 인용 가능.
    ⛔ **배수(18×)를 이 문헌으로 정당화 금지** — 두 논문 모두 배수 미보고.
  - **⑦ 응력 규칙 — 우리에게 유리하고 동시에 불리하다.**  리뷰는 응용 응력의 수치를 **거의 명시하지 않는다**
    (`kPa` 유효 0회; "<10 kPa" 는 **논문 stated 가 아니라 우리 추론**).  대신 **응력 의존을 두 번 규정**:
    Li [189] (p.129) *"the parameter and property values are **stress dependent** and the stress levels used
    in the calibration experiment should be **carefully selected**"* · Franco [196] (p.130) *"perform the shear
    tests … **in the range of normal stresses expected in the final application**"*.
    ✅ 우리는 **300 에서 보정 → 300 에서 사용** = 규칙 충족.  ⚠ 그러나 **100/200/600 MPa 로 쓰는 것은 외삽**
    → Heckel 4압력을 **적합이 아니라 예측 정확도**로 보고해야 방어된다 (§F 신설 항목 참조).
  - ⛔ **넘지 말 것**: *"Coetzee 가 우리 18× 를 승인한다"* (강성을 **치밀화 목표**에 맞춘 사례는 리뷰에 **0건**) ·
    *"리뷰가 Heckel 을 표준 시험으로 든다"* (`Heckel` **0회**) · 리뷰 안의 **μ·E·COR 수치를 우리 표로 옮기는 것**.

- **★★★ Zunker & Kamrin 3부작 (2026-08-25 신설) — 우리 18× 연화의 가장 강한 반례 후보**
  (digest `papers/zunker2024_mdr_contact_model_partI.md` · `papers/zunker2024_bulk_elastic_partII.md` ·
  `papers/zunker2025_dem_large_deformation_compaction.md`.  ⚠ **소재 = 제약 부형제 MCC(Avicel PH102)**,
  황화물 아님 — **방법·무차원군·판정만** 전이, 절대값 전이 금지):
  - **판정 요지**: 접촉 **LAW 자체**는 재료별 보정이 **0** 이다 (피팅 = 정규화 경화곡선 상수 2개
    `p̄/Y = 1.75·exp(−4.4 δ/R) + 1`, **전 재료 공통**).  ⇒ **"E 를 18× 낮추지 않고 실제 물성으로 대변형
    압밀"이 실제로 성립한다.**  ⚠ 단 **DEM 전체를 돌리려면 자유변수가 6–8개** (Y 피팅 · **ψ_b 0.08→0.5
    튜닝** · µ_t 0.7 · µ_t,wall 0.1 · µ_roll 0.6 · t_p 50 · 겹침캡 0.75 · CoR) → **"무보정" 인용 금지.**
    ★ 정확한 대비 = **"우리는 자유변수가 적지만 하나가 물성을 18× 왜곡한다 / 그들은 더 많지만 어느 것도
    물성을 왜곡하지 않는다"** — 이 축에서 **우리가 불리하다.**
  - ★★ **구조적 이유 (인용 가능)**: 완전소성 접촉력은 `F ≈ p_Y(δ)·A_geo(δ)` 로 **E 가 들어가지 않는다.**
    항복캡 없는 선형 접촉은 `F ∝ E·δ` 라 **E 를 낮추는 것 외에 δ 를 키울 방법이 없다.**
    ⇒ **18× 연화 = 빠진 항복캡의 대역(surrogate)** 이 가장 절약적인 설명이 된다 (frame[2] 서사 정정 필요).
  - ★ **우리 접촉은 이미 항복점을 한참 지났다 (DERIVED — Zunker eq.(41) 을 LPSCl 로 평가)**:
    E = 22.1, ν = 0.37 → E*_c = 12.80 GPa.  구-구 환산 항복겹침 `δ_Y/R = 0.13 / 1.12 / 4.12 %`
    (σ_y = 0.05 / 0.15 / 0.30 GPa).  우리 실측 **composite 14.8 % · pure-SE 22 %**
    ⇒ **3.6×–169× 초과, σ_y = 0.15 기준 13× 초과.**  ⛔ 우리 계산 — 논문 수치로 인용 금지.
  - ⚠ **그래도 "연화가 틀렸다"로 못 가는 이유 3가지**: ① **우리 MPM 은 항복캡(J2, σ_y 0.15–0.30)을 갖고도
    연화가 필요했다** (E=24 → 33–38 % porosity); ② **Zunker 3편 어디에도 porosity/상대밀도 수치가 0개** —
    검증 타깃이 **σ_axial(ε)·σ_radial(ε)** 이지 porosity(P) 가 아니다.  "연화 없이 실험 porosity 도달"은
    **아무도 보이지 않았다**; ③ MCC(연성 유기물, 파쇄 없음) ≠ LPSCl(취성, >3 µm 파쇄 — Fan 2026 §3.5)이고
    **이 모델에 파쇄가 없다.**
  - **압력은 우리 영역에 닿는다**: tableting 최대 축응력 **240 MPa** (우리 300 · Doux 370 · Minnmann 380 계열),
    최대 반경응력 **147 MPa**(측압비 0.61, DERIVED), **잔류 반경응력 15 MPa**, 배출 1.2(exp)/1.5(sim) MPa,
    탄성회복 축변형 0.08(압축체 높이 대비 13.1 %, DERIVED).  ⇒ **porosity 는 비교 불가, 압력만 대응.**
  - ★ **초기 패킹은 우리와 같은 bottom-up** — die fill(20,000 입자 삽입 + 중력침전) → 압축 → 해제 → 배출.
    **XCT 수입은 세 논문 어디에도 없다** ⇒ `positioning_vs_geodict.md` 의 생성 vs 재구성 축에서 **우리 편.**
  - ★★ **결정 실험 (미실행, 최우선)**: 그들 LAMMPS 브랜치(`github.com/willzunker/lammps`, `mdr` 브랜치,
    commit `c6159505`, GPL v2)로 **pure-LPSCl** 을 실제 물성(E 22.1 · ν 0.37 · σ_y {0.05, 0.15, 0.30} ·
    **κ = 우리 DFT B₀ 26.23**)으로 **100/200/300/600 MPa** 압밀 → **연화 없이 Minnmann 10 % @300 이 나오나.**
    단일재료라 그들 미해결 제약(2상 불가)에 안 걸린다.  판정선은 카드 ③ §12-① 에 등록.
    ⚠ 비용 (DERIVED): 그들 규칙 `Δt = 0.35√(m/k)`, `k = κ·R_min` → 우리 SE 는 **Δt ≈ 9×10⁻¹¹ s**;
    실제 E 로 가면 Rayleigh 스케일로 **스텝 수 4배**.

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

- **★★ Nam 2026 ACS EL (primer layer / 집전체 계면, `nam2026_primer_layer_dry_electrode_collector`) — ① Holm ½ 의 독립 재현 ② `R_collector` 3-직렬 분해 ③ "층위 혼동" 경고**:
  - ★ **j_peak ∝ A_contact^(−0.54)** — AFM 실측 primer 지형 위에서 **ΔV=1 V Ohm 정상상태**(= 우리 STEP3 복셀 FV 와
    동형 방정식)를 풀어 얻은 **계면 전류집중 계수** 1.62 / 1.30 / 1.20 (C100 / S100 / S50C50) 을 **상대 접촉면적**
    1.00 / 1.54 / 1.72 (본문 stated) 에 대해 로그회귀 → **기울기 −0.541** (쌍별 −0.510 / −0.553).
    ⇒ 우리 σ_ionic `cov^½` · σ_e `√A_AM-AM` 의 뿌리인 **Holm 1967 협착 1/√A 를 서로 보정한 적 없는 경로가 재현**
    (frame[4]). ⚠ **n=3 · j 는 도판 판독 → "consistent with ½" 까지만, 지수 인용 금지.**
    **→ 3차 확인 도구 완성 (2026-08-11)**: `scripts/holm_exponent_from_field.py` (selftest 17/17).
    ★ 설계 요점 = **크기 교란 통제** — A = (cov/100)·4πr² 이라 log A = log cov + 2 log r 이고, j 가 다른 이유로 r 에
    의존하면 순진한 회귀가 크기효과를 협착 지수로 착각한다 → `partial_slope`(log j ~ log A + log r) 가 **정본**,
    naive 는 문헌 3-점 집계와 같은 형태라는 이유로만 병기. selftest 가 재현: r^0.8 을 섞으면 naive 는 |편향|>0.10
    인데 partial 은 −0.5 를 0.03 안에서 지킨다. ⚠ payload 의 `je` 는 입자 복셀 **평균** |J_z| 이지 peak 이 아니라
    (Nam 은 peak) 결과는 **하한**으로 읽을 것. **실데이터 실행 대기**(payload 는 WSL/V100 쪽).
  - ★ **`R_collector` 는 한 덩어리가 아니라 3-직렬**: `R_(CC|primer)` + `R_(primer,bulk)` + **`R_(primer|electrode)`(지배항)**.
    증거 = **C100(순수 CNT)이 앞 두 항 최소**(CNT σ 최고 · **porosity ~4 %** 최저 · primer↔CC 계면저항 최저)**인데
    전극-레벨 계면저항은 최대**. ⇒ 우리 `rint_eis_anchors.csv` 의 `carbon_coated`/`C-SUS_primer` 를 **"코팅 유무"
    1-노브로 두면 안 되고 (조성·두께·거칠기·순응성) 4-노브**로 봐야 한다. 기존 앵커 `collector_coated_pristine =
    3.5–10 Ω·cm²(~5× bare)` 의 **밴드 폭이 실은 조성 자유도**일 가능성.
  - **배수 비교 (order-of-magnitude 만)**: 그들 사이클후 Nyquist **w/o 330 Ω : best(S50C50/S25C75) 78 Ω ≈ 4.2×**
    vs 우리 랩 cycled **bare-Al SBE 110 : C-SUS 30 ≈ 3.7 Ω·cm²배**. 방향·크기 유사하나 ⚠ **그들은 Ω(면적 미기재,
    Ω·cm² 변환 불가)·액체 LIB·200 cyc**, 우리는 **Ω·cm²·황화물·1000 cyc** → **정량 앵커 아님, 정성 corroboration.**
    ⚠ 게다가 **같은 연세대 DTBL 그룹**이라 우리 Fig6e 유래 앵커와 완전 독립이 아닐 수 있다.
  - **"층위 혼동" 경고 = 우리가 두 번 겪은 함정의 문헌판**: (i) primer 단독으론 최고인 C100 이 전극을 얹으면 최악
    ↔ 우리 **SDCP σ_e +52 % 인데 하중분담 10→7 % 역행(직렬 시그니처)**; (ii) 그들 Fig 4d 전류 컬러바 **0–5 A/cm² 는
    @ΔV=1 V 프로브 스케일**(실제 1C = 4.0 mA/cm² → 3 오더 차) ↔ 우리 **@1V 수송프로브 ≠ @1C 운전** 라벨링 규약.
    ⇒ **일반화: 국소 전도도 개선은 그것이 직렬 병목이 아닐 때만 전달된다.**
  - **인용 가능 수치(stated)**: SAICAS 접착 **345(w/o) → 586/568/550/477/448 N/m**(S100→C100, +70…+30 %) ·
    Sq **70±8 / 69±9 / 71±15 / 98±16 / 198±49 nm** · **탄성회복비 61.5→93.5 %**(digitized) · 5C **1.12 mAh/cm²
    (28.7 %) vs w/o 0.27(6.9 %)** · 200 cyc 유지율 **89 / 84.3 / 79.2 / 78.8 / 77.7 / 66.4 %** · 1C = 4.0 mA/cm² ·
    PTFE **18** / Al **40** / primer **~60 mN/m** · CB **37 nm** / MWCNT **⌀12 nm** · primer **~0.5 mg/cm²**.
  - ✅ **SI 확보 완료 (2026-08-11, PDF 38 p — DOCX 아니었다)** ⇒ **이제 R_collector 절대 앵커를 준다**:
    - ★ **전극↔집전체 계면 ASR (Fig S8b)**: **w/o primer 32.0 → 최적(S25C75/S50C50) 15.9/16.2 mΩ·cm² (2.0×↓)**.
      같은 그림 (a) 의 **벌크 저항률은 404–441 mΩ·cm 로 조성 무관**(오차 안) ⇒ **primer 가 바꾸는 것은 계면 항 하나뿐**
      임이 실측으로 분리돼 있다. `docs/data/rint_eis_anchors.csv` 에 6 행 등록(nam2026_Rcoll_*).
      ⚠ 측정 = **전극 저항 측정기(DC·무전해액)** → chemistry 무관한 **전자 접촉 ASR** 이라 액체계 논문이지만
      우리 R_collector 항에 **형태·크기 모두 쓸 수 있다**(σ 나 R_ct 처럼 전이 금지 대상이 아니다).
    - ★ **크기 판정**: 우리 코퍼스 중앙값(n=85, L=97.6 µm) ASR_ion **64.9** / ASR_e **1.400 Ω·cm²** 대비
      R_collector 0.0320 = **ASR_ion 의 0.049 % · ASR_e 의 2.29 %** (최적 primer 0.0159 → 1.14 %).
      ⇒ **이온 경로엔 무시 가능, 전자 경로엔 2 % 급 실재 항.** "집전체를 고쳐 성능을 올린다"는 서사는
      **이온 경로가 46× 큰 우리 황화물 스택으로 그대로 오지 않는다** — 유계 소항으로 둘 것.
    - ★ **DCIR 성장 배수가 조성 무관** (Fig S15a→S20a, @50 % SoC): w/o **42→93.5 (2.23×)** vs S50C50
      **17.5→40.5 (2.31×)** — 절대값은 2.4× 차인데 배수는 2.1–2.6× 같은 밴드. ⇒ **집전체 계면 개선은
      R_int(N) 의 *절편* 만 낮추고 *기울기(열화율)* 는 바꾸지 않는다** = 우리 다-항 분해에서
      **R_collector(N) 은 지배적 N-의존 항이 아니다**(성장은 R_chem·접촉손실 쪽). ⚠ 액체계 + 사이클 수 미명시
      → `FORM/METHOD-ONLY`, 배수 자체를 황화물로 전이 금지.
    - Fig S10 원도판 확인 **1.00 / 1.55 / 1.72** (본문 stated 1.54/1.72 와 일치) → −0.54 지수의 x 축 확정.
    - Table S2 그들 σ_e 모델 입력: NCM622 **0.453** · CBD **375** · primer **800 S/m** (전부 문헌 인용).
      ⚠ 우리 σ_AM(e) LOCKED 10/5 mS/cm = 1000/500 S/m 과 **3 오더 차** — 그들은 분말/단결정 고유값, 우리는
      코퍼스-fit 엔드포인트라 **다른 양**이다(누가 맞나 묻지 말 것). 그들 CBD 375 ↔ 우리 carbon 1000 S/m 은 같은 자리·2.7× = 같은 오더 ✓.
    - **여전히 못 쓰는 것**: R_ct/R_film/DCIR 의 **Ω → Ω·cm² 변환**(SI Experimental 에도 코인셀 **전극 지름 없음**,
      2032 형이라는 것만) · peel 의 **N → N/m**(시편 폭 미명시 → SAICAS 345–586 N/m 과도 비교 불가) · **사이클 수**.
    - 원본 추출표: `docs/data/nam2026_primer_si_values.csv` (stoic-knuth). 그림 33 장 크로핑 완료(`litdb/figures/`).
  - ⚠ **액체계 NCM622‖흑연** — ASSB 아님. 액체는 전해액이 공극을 채워 이온경로를 보전하지만 **ASSB 는 접촉면적이
    이온·전자 유일 경로** → 접촉면적 효과는 ASSB 에서 **더 커야** 한다(추정, 검증 안 됨). **절대 σ·R 전이 금지.**
  - ⚠ **본문 자체 오류**(카드 §4.3): "**E 가 Super P 와 함께 단조 증가**"는 Fig 3f 판독과 어긋남
    (S75C25 52 < S50C50 77) → "S100 만 3× 뻣뻣"으로 축소. **(유효)**
  - ✅ **OWRK 판정 정정 (2026-08-11, SI Table S3/S4 로 검정)** — 이전 "인용 금지"는 **부분 철회**:
    - 실측 분해(mN/m): **Al 34.1/1.0 · PTFE 15.4/1.0** · primer 45.4–48.0 / 10.1–19.5 · NCM622 37.8/23.6.
      이 값으로 `W = 2√(γ₁ᵈγ₂ᵈ)+2√(γ₁ᵖγ₂ᵖ)` 를 다시 계산하면 **Table S4 의 9 개 값을 전부 ±0.12 안에서 재현**
      (W(Al↔PTFE) 계산 47.83 vs stated 47.8) → **그들의 산술은 정확하다.**
    - **내 반증 예측(“primer γᵈ≈40 이면 이득 0”)은 틀렸다** — primer 분산 성분이 **45–48 로 Al 34.1 보다 훨씬 커서**
      W(PTFE↔primer) 59.2–63.2 vs W(PTFE↔bare Al) **47.8** = **+23.8~32.1 %**. ⇒ **"코팅하면 PTFE 친화도가 오른다"는
      인용 가능.**
    - **단 더 날카로운 반증이 남는다**: W 는 **조성 순위를 설명하지 못한다**. W 내림차순
      S100 63.2 > S25C75 62.1 > **C100 61.9** > S75C25 60.6 > S50C50 59.2 vs peel(Fig S3c) 내림차순
      S25C75 0.86 > S100 0.83 > S75C25 0.77 > S50C50 0.73 > **C100 0.59** — Spearman **+0.60 (n=5)**,
      **C100 은 W 3 위인데 peel 꼴찌**. ⇒ **표면에너지는 bare→primer 계단(+25 % 남짓)만 설명하고, primer 조성 간
      순위는 §3.4 거칠기·비가역 변형(기계적 물림)이 만든다 = 두 기전이 직렬로 다른 일을 한다.**
      (원래 카드의 직관보다 오히려 강한 진술이고, **SI 없이는 쓸 수 없던 문장**이다.)

- **★★ Luan 2025 AFM (`luan2025_graded_cathode_400whkg_pouch`) — 이온/전자 비대칭의 실험판 + σ_e 폼의 유효범위 하한.**
  - ★ **LPSC bulk σ_ion = 2 ± 0.1 mS/cm (stated)** → 펠릿급 앵커 **4번째**: Bazzoun **1.02** · Minnmann **1.6** ·
    Kim2025 **1.6** · **Luan 2.0**. ⇒ 펠릿 밴드 **1.0–2.0**, Cronau 단결정 **3.0** 아래 = GB 포함 서열 일관 ✓
    (우리 `σ_grain = 3.0 × Cronau(r_SE)` 의 이중계상 점검이 또 한 번 통과).
    ⛔ **복합 σ_ion 은 측정 안 함** → 이온 절대앵커는 여전히 Bazzoun/Minnmann 뿐.
  - ★★ **σ_e vs SE 함량 (Fig 7b, DC 분극 9점, carbon 0.5 wt% 고정): SE 10→90 wt% 에서 ~6 자릿수 붕괴**,
    그리고 **용량이 같은 자리(50→60 wt%)에서 함께 붕괴** (Fig 7a: 용량 **≈127 → ≈7 mAh g⁻¹**).
    **DERIVED(ours)** ρ(4.8/1.86/2.0) 환산 시 붕괴 위치 = **φ_AM(of solid) ≈ 0.28 → 0.20** = 3D 구충전
    퍼콜레이션 문턱대. ⇒ **우리 σ_e Stage 22.5 폼에는 φ_AM 문턱항이 없다**(φ_AM⁴ 뿐).
    우리 corpus 는 AM 60–95 wt% = **φ_AM(solid) 0.37–0.88 로 전부 문턱 위**라 폼은 안전하지만,
    **"φ_AM(of solid) < 0.3 외삽 금지"** 를 `our_dem_baseline.md §4` 와 σ_e 문서에 못박을 것.
  - ★★ **용량은 SE 함량에 대해 단봉(dome), 최적 SE ≈ 20 wt%** — "SE 많을수록 이온경로가 좋다"의 실험 반증.
    SE 를 더 넣으면 절연체 부피가 늘어 **전자망이 죽는다** = 우리 σ_e/σ_ion trade-off 서사(Kim2024 carbon
    부피점유 · Cho2024 VGCF 양면성)의 **SE 쪽 대칭 사례**.
  - ★★★ **frame[4] 교차검증 — "전자망은 싸고 병목은 이온"을 우리가 숫자로 갖고 있다.**
    Luan: **이온 구배 = +10.0 %(vs uniform)/+15.0 %(vs reverse) 실험**, **전자(도전재) 구배 = ≈+2 % 시뮬뿐**,
    본문 stated *"even limited amounts of conductive agent can fulfill the electronic transport requirements."*
    우리 STEP4 운전-φ(z): **2C 옴강하 = 전자 0.01–0.03 mV vs 이온 84–90 mV (≈3000–9000×)**.
    ⇒ 완전히 다른 두 경로(실측+COMSOL 연속체 ↔ 우리 Kirchhoff 접촉망+STEP4)가 **같은 비대칭**을 낸다.
    **우리가 그들 정성 주장의 정량 근거**다 (§E 로도 중복 기재).
    ⚠ **조건부**: 이 비대칭은 **CAM-rich 영역 한정**. Luan Fig 7a/b 가 SE ≥ 50 wt% 에서 **전자가 율속으로 역전**
    됨을 보였고 우리 corpus 는 그 영역에 없다 → 두 결과는 서로의 유효범위를 보완하는 관계.
  - ⚠⚠ **σ_e 절대값 인용 금지 — 100× 단위 결함.** 본문 Experimental 은 COMSOL 입력을
    **"0.5 % carbon → 1.7 S m⁻¹, 0 % → 0.0017 S m⁻¹"**(= 17 / 0.017 mS cm⁻¹)이라 적는데,
    Fig 7b 는 가장 가까운 조성에서 **≈0.17–2 S cm⁻¹** 을 보인다 — 정확히 **cm↔m 100×** 어긋남.
    어느 쪽이 오기인지 논문으로 판별 불가. **쓸 것은 (a) 6-decade 하강의 모양, (b) 붕괴 φ_AM, (c) 용량-σ_e
    동시붕괴 뿐.** 참고로 **우리 σ_e ≈ 1–3 mS cm⁻¹**(real_9 Stage-E 1.056–1.087 · SDCP SBE 1.979 / DBE 3.002)는
    그들 두 COMSOL 입력값 **0.017 < 1–3 < 17 사이**에 낀다 = 자릿수 정합(절대 일치 주장 금지).
  - ⚠ **DRT 정량값 없음.** τ 대역 배정(10⁻⁶–10⁻⁴ R_CEI / 10⁻¹–10⁰ R_ct / 10⁰–10¹ 확산)만 stated 이고
    **R 값 표가 없다** → 우리 v3-1 `eis_drt_ica.py` 의 **판독 양식 레퍼런스**로만 (앵커 아님).

- **★★ [Zhang23] (Joule 2023, `papers/zhang2023_pfib_multiscale_imaging_4d_thick_cathode.md`) — *유효 σ 를 아예 내지 않는* 최전선 4D 모델**
  (⚠⚠ 액체 LIB → **이온상 반전**: 그들 pore = 이온전도체 / 우리 SE 고체망 = 이온전도체):
  - ★★ **그들 파이프라인에 유효 전도도 출력이 없다.** σ_AM·σ_CBD·σ_e(전해액)를 **입력**으로 받아 3D-분해
    Newman 해 안에서 소비할 뿐, **σ_eff,ion·σ_eff,e 를 보고하지 않는다.** ⇒ **우리 이중 이산화(접촉망
    Kirchhoff+Holm **및** STEP3 복셀 FV)가 이 축을 통째로 앞선다.** frame[4] 교차검증 상대가 **아니다**
    (물리계가 다르고, 애초에 비교할 출력이 없다).
  - ★★ **σ_AM 앵커 불일치 — 200×** (전이 **가능**: AM 은 NMC811 로 동일, 전해질 무관):
    그들 **σ_AM = 5×10⁻³ S m⁻¹ = 5×10⁻⁵ S cm⁻¹ = 0.05 mS cm⁻¹** (SI ref [S2] Wang 2018, 혼합전도 층상
    LTMO 의 전자/이온 분리측정) vs **우리 STEP3 σ_AM_S = 1×10⁻² S cm⁻¹**, Stage 22.5 LOCKED 엔드포인트
    **10 / 5 mS cm⁻¹**. ⇒ **우리가 100–200× 높다.** 우리 값이 과대면 **σ_e 를 과대평가하는 방향**이다.
    ⚠ NMC 전자전도는 **SOC 의존이 크고 문헌이 수 자릿수 흩어진다** → **밴드로 다루고 감도 프로브로 검정**
    (CL-48 σ_VGCF 프로브와 같은 방식). Stage 22.5 엔드포인트는 **코퍼스 적합값이지 재료 실측이 아님**
    (CLAUDE.md A1 CLOSED 노트) → **폼은 건드리지 말고 STEP3 입력만 재조사.**
  - **σ_CBD = 700 S m⁻¹ = 7 S cm⁻¹** (균질 CBD 도메인, ε_CBD=0.5 미세공극이 전해액으로 참) vs 우리
    **σ_VGCF 100 S cm⁻¹**(CL-47 이 "유효 망 상수"로 재라벨) · **σ_SDCP 250**. **객체 정의가 다르다**
    (도메인 vs 섬유 재료값)이나, **우리 100 이 상당히 높은 쪽**임을 보여주는 외부 참조점. ⚠ 그들 단일 σ +
    ε=0.5 축약은 **우리 CL-47 이 σ_VGCF 에 대해 지적한 것과 같은 종류의 럼핑** — 비판이 서로 대칭이다.
  - ★ **우리 σ_e 밴드 위치는 이 논문으로 안 바뀐다** — 그들이 **전극 유효 σ_e 를 안 냈기 때문**이다.
    놓을 수 있는 배치는 `상 값(그들 CBD 7,000 mS cm⁻¹) ≫ 전극 유효 σ_e(우리 SBE 73 / PTFE 차단 54.6,
    문헌 Lee 2025 34 · Kim 2024 38.6–65.2) ≫ AM 상 값(그들 0.05)` 뿐. **CL-46 판정은 유지.**
  - ⚠⚠ **τ 비교 함정 (기록 필수)**: 그들 **flow tortuosity 1.54 / 1.49 / 1.53**(pristine/저전압/고전압, **사이클
    불변**)은 **공극상의 Stokes 유동 tortuosity**다 — Avizo 절대투과율 시뮬의 유속장에서 **Koponen 1996
    `τ_v = Σ|V|/ΣV_i`** 로 계산(등방 100 nm 복셀 리샘플). 우리 **SE 접촉망 τ 중앙 1.43(1.15–4.44)** 과
    **숫자는 가깝지만 상도 물리도 다르다**(유동 ≠ 확산 ≠ 전도). **"우연한 근접"으로만 기록하고 비교 주장 금지.**
    굳이 대응시킬 상대는 우리 **STEP3 pore-τ** 인데, 황화물 침대는 공극이 거의 닫혀 있어(closed-from-top
    99.2 % 사례) 값이 폭발한다 = **애초에 대응하지 않는 양**이다.
  - ★★ **퍼콜레이션 지표는 전이 가능** (기하량, 전해질 무관): 그들은 **CBD 연결성 맵에서 "최대 응집체가
    전체 CBD 의 몇 %"** 로 퍼콜레이션을 정량한다 — **슬러리 23.6 % vs 건식 57 %** (LNMO 후막, 2D PFIB 세그).
    **우리 f_perc / 최대 클러스터 지표와 정의가 같다.** ⇒ **우리 첨가제 침대(VGCF/SuperP/SDCP)에서
    "최대 탄소 클러스터 부피분율"을 표준 출력으로 뽑으면 이 값과 직접 대비 가능** (A4 감사에서 이미
    "carbon cluster 85개 + 99.4 % 연결"을 잰 적 있다 = 같은 종류의 양). **σ_e 이득을 퍼콜레이션 언어로
    설명하는 통로** → 백로그 후보.
  - **D_AM = 1×10⁻¹⁵ m² s⁻¹** (SI ref [S8] Geng 2022) vs 우리 STEP4 poly 기본 **3×10⁻¹⁴**, SC 밴드
    1.5×10⁻¹⁵–1×10⁻¹⁴ (`docs/ncm_sc_poly_electrochem_anchors.md`) ⇒ **그들이 우리 기본보다 30× 느리고**
    우리 SC 밴드 하단 근처다. **직접 대조 대상**(AM 고유값).
  - **C_s,max = 32,286 mol m⁻³** vs 우리 STEP4 c_max **63,104**(PyBaMM Chen2020 기계추출) — **~2배 차**.
    그들 값이 실사용 stoich 창을 이미 접은 값일 가능성이 있으나 **원문에 설명 없음** → 인용 시 주의.
  - ★ **Bruggeman 지수 p_electrolyte = 0** — 미세구조가 **명시 분해**돼 있어 균질화 보정이 필요 없다는
    선언이다(분리막만 1.5). **우리 STEP3 복셀 FV 도 같은 논리** ⇒ 우리가 Bruggeman 을 쓰지 않는 것에 대한
    **문헌 정당화 문장**으로 쓸 수 있다.

- **★★ Alabdali 2023 (`alabdali2023_cgmd_wet_manufacturing_ssb_cathode`) — 같은 그룹 선행편.  σ_e 를 *절대값*으로
  주는 드문 문헌이고, 위 Weitze 항목의 열린 질문(σ_CBD 얼마?)에 **숫자를 준다**.**
  - **입력 (stated)**: **σ_AM(NMC622) = 0.005 S m⁻¹** · **σ_CBD = 15.93 S m⁻¹** [refs 36–38].
    ⇒ **σ_CBD/σ_AM = 3186배** ⇒ **그들 δ_e 는 사실상 *CBD 망* 관측량**이고 AM 전자경로는 죽어 있다.
    우리 Stage 22.5 σ_e 는 **φ_AM⁴ = AM backbone** 관측량 ⇒ **같은 이름의 양이 서로 다른 상을 재고 있다.**
  - **출력 (digitized, Fig 4a)**: δ_e = **2.43 → 3.27(최대, 압연 30 %) → 1.63 S m⁻¹** = **24.3 → 32.7 → 16.3 mS/cm**.
    ★ **밴드 배치**: `그들 16–33 < 실험 34–65 (Lee 2025 34 · Kim 2024 38.6–65.2) ≲ 우리 54.6(PTFE 차단)–73(PTFE 미표현)`
    ⇒ **두 모델이 실험을 아래·위에서 감싼다.**  방향 설명 3가지 = ① **바인더 규약이 정반대**(그들: SBS 를
    *도전상 CBD 안에* 녹임 / 우리: PTFE 를 절연 또는 차단) ② **AM 전자경로 사망**(σ_AM 0.005 S/m)
    ③ **격자**(그들 voxel 미보고).  ⇒ **정확도 비교가 아니라 규약 대조로만 인용**.
  - ★★ **위 Weitze 항목에 대한 교차-보강 (DERIVED, ours)**: Weitze 는 σ_e 를 **CBD 벌크=1 로 정규화**만 하고
    σ_CBD 절대값을 안 준다(그래서 "우리 밴드에 앉으려면 σ_CBD ≈ 30–65 S/cm 필요"라는 역산이 열려 있었다).
    **같은 그룹의 이 선행편이 실제로 쓴 값은 15.93 S m⁻¹ = 0.159 S cm⁻¹** — 필요값의 **1/190 ~ 1/410** 이다.
    Weitze 가 같은 값을 썼다면(⚠ Weitze 본문에 명시 없음, 다만 **GeoDict 방법 자체를 ref [16]=이 논문에 위임**한다)
    Weitze 의 절대 σ_e ≈ 1.15×10⁻³ × 0.159 S/cm ≈ **0.18 mS/cm = 실험 밴드의 1/190~1/360**.
    ⇒ **"그들 σ_e 가 우리 밴드 안"이라고 쓰지 말라**는 위 경고가 **숫자로 뒷받침된다.**
    ⚠ 어디까지나 *조건부 추론*이다 — Weitze 의 σ_CBD 가 실제로 무엇인지는 **여전히 미확인**.
  - ★ **이온축**: τ_g = **10.2(0 %) → 5.15(30 %) → 2.21(50 %)**, D_eff = 0.21 → 5.25 (그림 축 `dm² s⁻¹`, 물리적으로
    성립 안 함).  **DERIVED(ours) 해독**: τ=√(η/D_eff) 에 Fig 3b/3c 의 **η ≈ 22 %(건조) / 26–28 %(50 %)** 를 넣으면
    **찍힌 τ 를 소수 첫째자리까지 재현**(10.24 / 2.21–2.31) ⇒ **플롯된 D_eff 는 벌크 대비 %** 다.
    ⇒ **formation factor D_eff/D_SE = 0.21 % → 5.25 %**.
  - ★ **CL-26 규율(intrinsic σ 맞추고 비교) 두 번째 적용**: Bazzoun 실측 formation factor **0.134**(=0.137/1.02) 대비
    **50 % 압연조차 1/2.6**, 건조 상태는 **1/64**.  원인 후보 = **φ_SE ≈ 22 vol%**(Bielefeld 이온 percolation 하한
    25 % *아래*) + **SE 가 굵다**(⌀1–8 µm, AM:SE 지름비 2.5 — 우리 12:4:1 의 12 와 대비) → 목이 길고 성기다.
  - ⚠⚠ **격자수렴·시드·오차막대가 전부 없다** — voxel 크기조차 미보고, 압연도당 1런, Fig 3·4 무오차막대.
    우리 SR-01 실측(vox 0.4→0.15 에서 σ_e 비 **+42.15 → +8.49 %**, σ_ion 비 **부호 반전**)에 비추면
    **그들 δ_e·τ_g 절대값에는 정량화되지 않은 격자의존이 남아 있다**(우리 판정).
  - ★ **실행 가능한 대조 (frame[4], 소재 전이 없음)**: 그들은 **상별 σ·조성·porosity 를 전부 공개**했다 ⇒
    우리 `voxel_conductivity.py`/`step3_sigma.py` 로 **같은 φ·같은 σ 의 합성 침대**를 만들어 δ_e 자릿수를
    재현해 보는 **복셀 솔버 외부 대조**가 가능하다.  ⚠ 구조 파일은 비공개 → **"같은 조성·같은 σ 에서 같은
    자릿수인가" 수준**까지만.

- **★★ Zhang 2026 (`zhang2026_dryprocess_electrode_architecture_cell_level`, *Nature Energy*,
  DOI 10.1038/s41560-026-01981-3) — σ_e 를 *숫자로 내지 않으면서* σ_e 축의 지배 descriptor 를 실측으로 특정한 편.**
  ⚠⚠ **chemistry 게이트 = 액체계 LIB** (본문+SI 전수 grep: sulfide/argyrodite/LPSCl **0회**) ⇒ **FORM/METHOD-ONLY**.
  **이온상이 반전**돼 있다 — 여기서 이온을 나르는 것은 **공극 속 액체**다.
  - **① 헤드라인 (stated)**: PFIB-SEM 대면적 단면에서 **최대 연결 CBD 클러스터 = 건식 61.2 % vs 슬러리 17.1 %**
    (전체 CBD 화소 대비, **3.58배**).  그런데 **두께방향 CBD 균일도는 건식이 오히려 나쁘다**(std **1.15 vs 1.00 %**).
    ⇒ 논문 원문: *"uniformity alone does not capture conductive network efficiency; **CBD connectivity is the
    primary determinant of effective electronic percolation**."*
  - ★★★ **② Source Data(xlsx, SI Fig 11 원수치) 재분석 — 논문 본문에 이 숫자가 없다.
    ⚠ 이 집계는 2026-08-11 세션이 이미 했고, 이번 원문 대조로 *삼중 일치*했다** (재유도 불필요):
    3D 토모 **슬라이스별** 최대 percolating CBD 분율 = 슬러리 **0.3836 ± 0.1383 (n = 135)** ·
    건식 **0.5359 ± 0.0985 (n = 121)** (모집단 sd) ⇒ **평균비 1.397** · **중앙값비 1.61** ·
    **sd −28.8 %** · **CV 0.360 → 0.184 (절반)** · **Cohen d ≈ 1.25**.
    z-깊이 **33.75 / 30.25 µm** (250 nm 슬라이스) ✓ 본문 "~30 µm" ⇒ **n 이 다른 것은 깊이가 다르기 때문**(슬라이스를 버린 게 아니다).
    자기상관 **lag-1 r = 0.567 / 0.663**, τ_int **5.11 / 6.86** ⇒ **n_eff 26.4 / 17.6**
    ( = `docs/plan_vgcf_ptfe_coupling_20260811.md` §1-(b) 의 **Codex CR-04 값과 소수 첫째 자리까지 동일**).
    ⇒ ★ 원시 n 으로 계산한 Welch **t = 10.19 는 표준오차 기준 ≈ 2.4배 낙관적**이다.
    ⚠⚠ **그래도 t 를 유의성 검정으로 인용하지 말 것** — workbook 에 **독립 재구성 수·시료/볼륨 ID 가 없어**
    어떤 ESS 를 써도 *공정 수준* CI 가 되지 않는다 (CR-04).  **AR(1) 민감도 구간 `[1.19, 1.64]`** 까지가 한계.
    안전한 문장 = *"두 슬라이스 계열에서 평균·중앙값·경험적 순위의 **방향이 일치한다**"*.
    ⚠⚠ **`1.397` 과 `3.579` 를 "관측창 의존 밴드" 라고 쓰지 말 것** (**Codex CR-05 로 철회된 표현**).
    둘은 **집계 함수와 선택 위치가 다른 두 통계**다 — `1.397` = **전 슬라이스 기술평균비**,
    `3.579` = 저자가 **골라 제시한 representative connectivity map 의 비**.
    (원자료에서 **17.1 % 는 슬러리 분포 최하단 근처(min 0.163), 61.2 % 는 건식 상단(p75 0.587 위)** — 원문 대조로 재확인.)
    **둘 다 calibration/validation bound 가 아니다.**  나란히, 각자의 정의와 함께만 적는다.
    ★ **원문 대조가 새로 더한 것 3건**:
    (a) **30 µm 축은 전극 두께(~105–125 µm)를 담을 수 없다** ⇒ 슬라이스는 **밀링 방향의 평행 단면**이고
        **대응(paired) 비교가 원리적으로 불가** — 계획서의 추론(*"독립 밀링 볼륨, 공통 index 상관 −0.03"*)이 기하로 확인된다.
    (b) **SI Fig 11 은 바이올린 플롯이고 슬러리 분포가 육안으로 이봉(bimodal)** (~30 % · ~50 % 두 로브) ⇒
        평균 > 중앙값의 *이유*이자, 단면 한 장이 어디에도 착지할 수 있다는 시각적 근거.
    (c) `Normalized_Largest_Fraction` 의 **정규화 분모가 SI 어디에도 정의돼 있지 않다** (캡션 전수 확인) ⇒
        본문의 "of total CBD pixels" 와 **같은 양이라는 진술이 없다** ⇒ **검증 게이트로 쓸 수 없다**.
    ⚠ 덧붙여 **분할 파이프라인이 둘**이다 (2D = Fiji Weka + MATLAB 8-이웃 / 3D = Avizo 딥러닝 + opening).
    ★ 이 사례의 교훈은 우리 **SR-01 이 자기 자신에게 적용한 규율**(vox 0.4 헤드라인 +42.15 % → 조이면 +8.49 %)과
    같은 종류다 — **"헤드라인 배수는 그것을 만든 집계 함수·선택 위치와 함께 적는다."**
  - ★★ **③ 접촉저항을 *어느 솔버에서도* 다루지 않는다** (우리 관심축의 정면):

    | | **CGMD** | **COMSOL** |
    |---|---|---|
    | 섬유–섬유 접촉이 객체인가 | **그렇다** (LJ) | **아니다** (CBD = 균질 연속상) |
    | 전기전도를 푸는가 | **아니다** | 그렇다 |
    | ⇒ 접촉저항 | 정의 자체가 없다 | **융합돼 삭제** |

    ⇒ **"섬유가 이산적인 곳에서는 σ 를 안 풀고, σ 를 푸는 곳에서는 섬유가 없다."**
    우리 `network_conductivity.py` 의 **접촉당 Holm 협착 R = 1/(2σ r_c) + Kirchhoff** 는 그들 어느 단계에도 없다.
  - **④ σ 입력 (stated, Supplementary Table 7)**: **σ_CBD = 700 S m⁻¹ = 7 S cm⁻¹** · **σ_NMC = 5×10⁻³ S m⁻¹**
    (비 **1.4×10⁵**).  ⚠⚠ **`zhang2023` Joule Table S3 과 완전히 같은 두 수**(같은 그룹, 3년 간격, refs Chen 2010/2017)
    ⇒ **문헌 앵커를 셀 때 2개가 아니라 1개다.**  "두 논문이 서로를 뒷받침한다"고 쓰지 말 것.
  - ★★ **⑤ 우리 CL-47 규약과의 접점 (DERIVED, ours)**: 탄소:바인더 **5:2 (질량)** ⇒ CBD **고체** 중 탄소 **73.3 vol%**.
    Bruggeman(σ_CBD = σ_C·φ_C^1.5)으로 탄소상 σ 를 역산하면 CBD 나노공극 **0 / 30 / 50 %** 에서
    **11.1 / 19.0 / 31.5 S cm⁻¹**.
    ⇒ 우리 생산 **σ_VGCF = 100 S cm⁻¹** 의 **1/3 ~ 1/9**, CL-47 이 확정한 **VGCF 분말 문헌값 83** 의 **1/2.6 ~ 1/7.5**.
    ★ **판정 = "우리가 틀렸다"가 아니라 "같은 인식론의 다른 눈금"**: 두 모델 **모두 복셀/메시 융합으로
    섬유–섬유 접촉저항을 삭제**하고 그 결손을 상수 하나에 lumping 한다 (CL-47: *"DEM E_eff 18배 연화와
    같은 인식론, frame[2]"*).  다만 **그들 쪽 앵커가 *실측 CBD 필름*이라 더 강하고, 값은 더 보수적**이다.
    ⚠ **객체가 다르다** — 그들 CBD 에는 **바인더 + 나노공극이 이미 포함**돼 있고, 우리 VGCF 상에는 없다
    (PTFE 는 별도 상, `sigma_ptfe` 기본 0).  같은 표에 놓을 때 **반드시 이 문장을 붙일 것**.
    ⇒ **CL-47 서술 정밀화**: "우리 100 이 문헌 융합-규약의 *중앙*" 이라고 쓰면 **과하다** →
    **"문헌 융합-규약 σ_carbon 은 대략 10–100 S cm⁻¹ 대에 흩어져 있고 우리는 그 상단에 있다."**
    (⚠ CL-47 의 결론 자체 — 우리 100 은 옹호 가능한 유효 망 상수 — 는 **유지**된다.)
  - ⛔ **⑥ σ_eff 를 한 번도 내지 않는다.**  COMSOL 은 **전류밀도 필드**(log₁₀ J, −10…+10 A m⁻²)와
    **입자 평균 전류밀도**(건식 **4.6×10⁻⁵** vs 슬러리 **1.0×10⁻² A m⁻²**, **217배**)만 낸다.
    ⇒ **우리 σ_e 절대값(54.6–73 mS cm⁻¹)과 숫자로 만날 수 없다.  descriptor 로만 만난다.**
  - ⚠ **⑦ 메시가 진짜 3D 가 아니다** — Methods 원문 *"by **stacking two identical images together**"*
    ⇒ **2D 단면의 z-압출**(Iso2Mesh, ~5 M 사면체).  연결성이 논지의 핵심인데 **면외 연결이 인위적으로 완전**하다.
    (우리 판단: 두 전극 모두를 구제하되 원래 더 끊긴 슬러리를 더 많이 구제 ⇒ **콘트라스트 축소 = 보수적** 방향일
    가능성이 크나 **미검증**.)
  - ★ **⑧ 즉시 실행 가능한 대조 (신규 지표)**: 우리 STEP3 는 이미 연결성분을 계산한다
    (rnm_sigma 연결성분 제한 수정, 2026-07-22).  **탄소상 최대 연결성분 / 전체 탄소 복셀**을 SBE vs DBE 로 내면
    **그들과 같은 종류의 양**이 생기고, 우리 σ_e 이득(구 스탬프 규약 **+12.3 %**)이 **부피 때문인지 연결성 때문인지**
    를 가르는 **교차확인 축**이 된다 (CL-44/45 판정 = "주된 원천은 새 도체 부피"의 독립 확인).
  - ⚠ **⑨ 이온축은 τ 한 개뿐**: **TauFactor τ = 건식 2.49 / 슬러리 2.87**, porosity **미보고**.
    ★ **규약 역판정 (DERIVED, ours)**: 그들이 말한 **"~33 % D_eff 증가"** 는 **오직 `D_eff ∝ ε/τ²` 로만 재현**된다
    (**+32.9 %**); TauFactor 자신의 규약 `D_eff = ε·D/τ` 로는 **+15.3 %** 다.
    ⇒ **한 논문 안에서 τ 규약이 미끄러졌다** (또는 표기된 값이 √τ_factor 다).  논문은 이 구분을 하지 않는다.
    ★ **우리 τ_Laplace/τ_Dijkstra/τ_geo 삼중 규약 경고의 외부 사례** — 원고에서 τ 를 쓸 때마다
    **관계식을 같은 줄에 적는다**를 규율로 굳힐 근거.
    ⚠ 같은 그룹 `zhang2023` 은 같은 소재계에서 **flow τ = 1.54** 를 냈다 (**1.9배 차** — 정의가 달라 **비교 금지**).

## C. 역학 / morphology — MPM 고유 (문헌 DEM은 형상 못 바꿈)
- 문헌: Varkey "elasto-plastic"은 **CONTACT 힘법칙만**(Thornton–Ning), 입자는 완벽 구 — "구=타협,
  현실 형상=향후 과제" 명시. Bazzoun도 구만.  **★ Duquesnoy 2023(ARTISTIC 캘린더링 DEM)도 rigid-구형**(CBD-shrink 건조=
  부피연산, 형상소성 없음) → **제조시뮬 최전선 3편(Varkey·Bazzoun·Duquesnoy)이 모두 형상소성 없음 = frame[5] *3중* 독립확증**
  (우리 MPM 이 메우는 형상-morphology 절반이 세 논문 다 빠짐).
- 우리: MPM 진짜 소성 형상변화(SEM 일치), void-fill flow, Σdg 변형장.
- 왜: 강체 구 DEM·단상 연속체는 granular 재배열을 못 잡아 둘 다 연화 럼핑 필요 (frame [1]/[2]).
- 인사이트: **morphology·소성 floor(<20 %)·변형장 = 우리 MPM이 메우는 간극** (Varkey가 스스로 인정 = frame[5] 확증).
- ★★ **frame[5] 4중 확증 — 그것도 *우리 접촉법칙의 저자 본인*이** (2026-08-25, `papers/giannis2021_stress_based_multicontact_dem.md` §1):
  **S. Luding 이 공저**한 Giannis 2021 이 서론에서 MPFEM·FEM-DEM·**MPM**·BPM 을 *"단일 입자의 **이방성 변형**과
  **변형 후 임의 형상**을 다룰 수 있는 방법 — 그러나 **높은 계산비용이 많은 입자 수에서의 사용을 막는다**"* 로 정리하고,
  그래서 **DEM + 접촉법칙 보정** 쪽을 택한다고 명시한다. ⇒ **"형상은 MPM, 규모는 DEM"** 이라는 우리 분업이
  *우리 hooke/hysteresis 정의서를 쓴 사람 자신*의 문장으로 외부 확증된다. 우리 scaffold 커플링(DEM 골격 + SE 만 MPM)은
  그가 지적한 **비용 장벽을 우회하는 형태**이므로, 이 문장은 우리 방법 선택의 정당화로도 그대로 쓸 수 있다.
  ⚠ 단 Giannis 2021 자신은 **소성이 아예 없다**(기반 = 순수 Hertz) — 형상은커녕 **접촉 소성도 없다**. 층위 ① 탄성 non-binary.

- **★★★ 2026-08-25 정정 — 층위 지도에 새 칸 "층(2.75)" 이 생겼다 (Zunker & Kamrin 2024 I·II / 2025)**
  (digest 3장 = `papers/zunker2024_mdr_contact_model_partI.md` 외 2).  **위 "문헌 DEM 은 형상 못 바꿈" 은
  *자유형상* 에 대해서만 참이다.**
  | 층 | 정의 | Varkey · Bazzoun · Duquesnoy · So | **Zunker 2024 I+II / 2025** | 우리 DEM | 우리 MPM |
  |---|---|:--:|:--:|:--:|:--:|
  | (1) 접촉 힘-변위 LAW | 항복 → 소성분기 + 잔류겹침 | ✅ (Varkey·So) | ✅ **δ-의존 경화곡선** | ✗ | ✅ J2 |
  | (2) 접촉 AREA 소성 | 소성 접촉면적 | △ / ✅(So) | ✅ 비압축 반영 해석식 | ✅ Stage-E(사후) | — |
  | (2.5) 다중이웃 결합 | 이웃 접촉이 이 접촉을 바꿈 | ✅ **평균장** F_mc(Varkey) | ✅ **기하·부피보존**(평균장 아님) | ✗ | ✅ exact |
  | **★(2.75) 매개변수 형상 상태** | 형상이 상태변수로 살아 **힘·신규접촉·공극소멸 판정**에 되먹임 | ✗ | ✅✅ **R 성장 + 잘린 구관** | ✗ | (상위) |
  | (3) **자유형상** SHAPE 소성 | 임의 형상·내부 유동·변형장 | ✗ | **✗** | ✗ | ✅ **진짜** |
  - **무엇이 실제로 변하나**: 입자당 **겉보기반경 R**(스칼라 1개) + 접촉당 **δ_max** → `R 의 구 − 접촉마다
    잘린 구관`.  **사후 역산이 아니다** — 그 상태가 (i) 기존 접촉의 힘을 올리고 (ii) **상대변위 0 인 2차
    접촉을 새로 만들고** (iii) `A_free/A_tot` 로 **벌크탄성(공극소멸)을 발동**시킨다.  변형형상을 **재구성해
    FEM 과 대조**까지 한다 (2025 §5, 접촉패치 5개 일치).
  - **여전히 못 하는 것 = 우리 MPM 이 지키는 영역**: **이방 배럴링 · 비축대칭 유동 · 재료 국소이동(void-fill
    의 흐름 자체) · 오목 프로파일**(모델은 항상 볼록, 실제는 δ_o,max/R_o>0.15 에서 오목-볼록) **· 파쇄 ·
    내부 응력/변형장**.  고구속에서는 구관 교차로 R 성장이 **붕괴**해 아예 **동결**시킨다 (Part II §4.3.3).
  - ⇒ **정본 문장 정정**: ~~"층(3) 입자 형상 소성은 23년째 아무도 못 함"~~ →
    **"층(3) *자유형상* 소성은 DEM 에서 여전히 아무도 못 한다.  그러나 층(2.75) — 형상을 매개변수 상태변수로
    들고 물리에 되먹이는 것 — 은 2024 에 열렸다."**
    `our_dem_baseline.md` §3 의 *"진짜 소성 입자 형상변화"* 도 **"*자유형상* 소성 · 내부 변형장 · 비축대칭
    유동 · 재료이동 기반 void-fill"** 으로 **좁혀 다시 쓸 것.**
  - ★ **부수 성과 (우리에게 유리)**: 그들 부피부기 `ΔV = −ΔV_e`(소성 등적) + `V_geo = (4/3)πR³ − Σ(π/3)δ²(3R−δ)`
    는 **우리 `ε_sphere`(= ΣV_o) 와 tr(ε̄) ≈ 1 % 이내로 같은 양**이다 ⇒ **ε_sphere 규약이 외부 역학으로 지지된다**
    (`ε_union` 은 잘린 부피를 되돌리지 않아 고체 과소계상 = 우리가 "상한/sanity 용"으로 강등한 것과 정합).
    ⚠ 공통 실패도 같다 — 구관이 심하게 교차하면 둘 다 무효(그들 ΔR 음수 ↔ 우리 ε_sphere 음수).
  - ★ **Varkey `F_mc` ↔ Zunker `F_Bulk` = 같은 증상 다른 처방** (상세 = 카드 ② §7-2):
    Varkey 는 **평균장 1항(β=0.5)** 으로 럼핑 + **상시 연속**; Zunker 는 **2기구로 분해**(R 성장 = 기하
    다중이웃 / 벌크 = 공극소멸) + **문턱 스위치 `A_free/A_tot < ψ_b`**.  필요물성 Varkey ν vs
    **Zunker κ (= 우리 DFT B₀ 26.23 을 그대로 사용 가능)**.
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

- **★ Nam 2026 primer (`nam2026_primer_layer_dry_electrode_collector`) — frame[5] 의 "빈칸"이 문헌에 노출된 사례 + 소성분율 실측**:
  - 그들 **기전 서사 = "Super P-rich primer 는 비가역(소성) 변형으로 mechanical interlocking 한다"** 인데, **이를
    시뮬레이션하지 않는다** — DT 모델은 AFM 지형을 **정적 기하로 import** 하고 AM 을 **패킹 배치**할 뿐,
    **라미네이션/캘린더링 압축 물리가 없다.** ⇒ Varkey·Bazzoun·Duquesnoy 에 이어 **frame[5] 4번째 독립 확증**
    (형상/순응 소성이 빠진 최전선 논문).
  - ★ **그런데 이번엔 검증 타깃까지 숫자로 나와 있다**: 상대 접촉면적 **1.00 (C100) / 1.54 (S100) / 1.72 (S50C50)**.
    구성도 우리 scaffold-MPM 에 이상적 — **AM(NCM, ~140 GPa) 고정 + primer 만 소성**, 강성비 **~10³**
    (primer E ≈ **50–150 MPa**, 우리 SE↔AM 대비보다 훨씬 극단). ⇒ **P-6: MPM 으로 primer 순응 → 접촉면적 예측 →
    1.00/1.54/1.72 대조 = "남의 논문의 미검증 기전"을 우리가 검증하는 논문성 있는 과제.**
  - **소성/탄성 분율의 드문 실측**: 나노압입 **탄성회복비 61.5 %(S100) → 93.5 %(C100)** = 비가역 분율 **38.5 → 6.5 %,
    ~6 배**; 독립적으로 **E/H = 12.5 → 2.2 (5.7 배)** 도 같은 방향(소성지수 ψ ∝ E/H). 두 무관한 지표가 같은 결론.
    ⇒ **우리 δ-overlap 소성 프록시/Stage-E 소성면적의 "얼마나 소성적인가"에 대한 외부 스케일 감각.**
    ⚠ **대상이 카본/CMC primer 층**이지 LPSCl 이 아니다 → **CBD·carbon·PTFE 상**의 후보 파라미터이지 **SE 값 아님**.
  - ⚠ **접착 345–586 N/m 을 G_c 와 등치 금지** — SAICAS 는 마이크로블레이드가 전극층을 **절삭하며 소산하는 전체 일**
    (소성절삭+마찰+계면분리) 이라 차원만 J/m² 와 같을 뿐 **계면 파괴에너지가 아니다.** 우리 Bucci **G_c 2.8±1.8 J/m²**
    와 100× 차이는 물성차가 아니라 **측정량 차이**. 쓸 수 있는 건 **상대비(+30…+70 %, 조성 스팬 1.31×)** 뿐.

- **★ Luan 2025 AFM — frame[5] *5번째* 독립 확증 + PTFE fibril 실사 + 층 계면 설계지침.**
  - ★★ **판정: 입자-레벨 시뮬이 전혀 없다.** COMSOL phase-field 는 **2-region 균질 연속체**(Table S1 이 각
    region 의 SE 부피분율만 지정)로, **입자·접촉·공극이 없다.** Fig 4a–c 의 구(球) 그림은 **개념 모식도**이지
    계산 도메인이 아니다. σ_e 조차 **미공개 퍼콜레이션 상관식** 2점(0.5 %/0 % carbon)으로 주입한다.
    ⇒ **Varkey(구형 DEM·형상소성 없음) → Bazzoun(구형 DEM+RNM) → Duquesnoy(제조 DEM+ML) → Nam(DPE)** 에 이어
    **다섯 번째**이고, 앞의 넷과 성격이 다르다: **이번엔 DEM 조차 없다.** 즉 산업 파일럿은
    **"설계는 층 단위 조성으로, 미세구조는 안 푼다"** ⇒ **우리 DEM(패킹·접촉망 σ) + MPM(소성 형상)이
    그 빈칸 전체**라는 사실이 *실증 스케일에서* 확인된다.
  - ★ **PTFE fibril 실사 (Fig 6e, 2 µm 스케일)**: 건식 롤프레스 후 PTFE 가 실(fibril)로 늘어나 CAM 입자를
    묶고 있는 SEM. 우리 **F1 PTFE 브릿지 훅의 형태 근거** 확보. ⚠ 다만 **fibril 직경·밀도·강성 수치 없음**
    → 여전히 **훅만**, "PTFE = 절연 배선, 기계 기여 0" 규약은 그대로(§F1).
  - ★★ **Phase-5 층 계면 설계지침 (Fig 6d)**: 두 층을 따로 만들어 롤프레스로 합친 뒤 단면 SEM 에
    **뚜렷한 계면이 없다**(stated: *"no clearly distinguishable interface"*; PTFE fibril 이 층을 가로지름).
    ⇒ **우리 Phase-5 z-stacking 에서 날카로운 조성 계단을 만들면 비물리적** — smooth interface(혹은 수 µm
    혼합대)로 가야 한다. 현행 2D synth 는 z-band 를 지원하나 **계면 폭 규약이 없다 → 추가 필요.**
  - CAM 균열·응력·팽창: **다루지 않음**(XRD (003) broadening 증가를 "구조 무질서·응력 축적"이라 한 줄 언급뿐).
    우리 Auerbach fracture·MPM 응력장·A10 사이클 chemo-mech 는 그대로 우리 고유.

- **★★ [Zhang23] (Joule 2023, `papers/zhang2023_pfib_multiscale_imaging_4d_thick_cathode.md`) — 열화를 *관측*한 쪽 vs *모델링*한 쪽 (정확한 상보)**
  (⚠⚠ 액체 LIB. 균열/접촉손실은 **NMC811 고유 기계현상**이라 정성 전이 가능성이 상대적으로 높다):
  | | 그들 (Zhang23) | 우리 |
  |---|---|---|
  | **입자 균열** | **관측만** — 균열/NMC **7.13 → 7.77(+9 %) → 8.85 %(+24 %)**; 원분말 **0.12 %** | **모델만** — Auerbach, **CZM Bucci G_c 2.8±1.8 J m⁻²**(K_IC 0.2–0.4 MPa·m^½ 환산 3.24 와 16 % 차 = 독립 이중화), fracture-aware Holm `f_intact`, MPM crack-void |
  | **AM↔CBD 접촉손실** | **관측만** — NMC–CBD 접촉면적/NMC 표면적 **29 → 26 → 23 %** | **모델만** — `cycle_contact_ledger` f_broken·A_rel·R_ct 몫·σ_rel·Γ\*; 첫 실런 **mono R_ct 1.05× vs bimodal 1.51×** |
  | **계면상(CEI/SEI)** | **처방 저항막** `ΔΦ = (Z/σ_CEI)·i`, **kinetics 없음·두께 불변**; 분포는 **16구역 평균 5→20 nm 선형 + 구역내 가우시안 σ=0.15µ**(전체 3–28 nm), cryo-TEM 실측(20 vs 5 nm)에 맞춰 **입력** | **R_int(N) 다항 분해**(R_contact[Holm+R_ct] + R_tort + R_chem(N) + R_collector(N) + Δ_special), 성장은 **assumed-form 밴드** |
  | **kinetics** | **없음**(SI 가 자인) | **없음**(양끝 고정 assumed-form) — **무승부** |
  | **역학 일반** | **모델에 전혀 없음** — 압밀·응력장·소성·형상변화 0 | DEM 압밀 + **MPM J2 진짜 형상소성**(코어보존+경계평탄화 SEM 정합), 부피보존 void-fill, 누적소성변형장, Heckel P_y 138 |
  - ★★ **되먹임 사슬이 모델로 닫히지 않는다(그들 한계)**: 논문이 주장하는 사슬은 *"불균일 CEI → SOD 불균일 →
    균열 → 접촉손실 → 전자망 약화"* 인데, **관측된 −20 % 접촉손실이 모델의 σ_CBD 나 반응면적으로 되먹임되지
    않는다.** 즉 **사슬의 절반은 모델 밖**이다. ⇒ 우리 A10 접촉원장이 **정확히 그 닫히지 않은 반쪽**을 한다
    (단 우리는 관측이 없다) = **frame[5] 상보의 교과서적 사례.**
  - ★ **우리가 가져갈 형식 2개**: (a) **정규화 규약** — 균열은 *이차입자 부피*로, 접촉면적은 *AM 총표면적*으로
    나눠 보고(샘플 간 입자밀도 차 제거). 우리 fracture/coverage 지표도 같은 규약을 쓰면 외부 대조가 열린다.
    (b) **계면상 z-처방 레시피**(16구역 선형 + 가우시안) → 우리 STEP5/R_int(N) 의 assumed-form 을
    **문헌-형식으로 승격**. **값은 액체 전용이라 황화물 것으로 갈아 끼울 것.**
  - ⚠ **coverage 와 직접 비교 금지**: 그들 "접촉면적 29 %"는 **NMC 표면 중 CBD 와 닿은 비율**이고, 우리
    coverage 는 **AM 표면 중 SE 가 덮은 비율**(Hertz 16 % / Tabor 52 %, real_14)이다. **상대(CBD vs SE)가
    다르므로 값 비교는 무의미** — 변화율(−10 %/−20 %)의 **크기 감각**만 쓸 것.

- **★ Alabdali 2023 (`alabdali2023_cgmd_wet_manufacturing_ssb_cathode`) — 소성이 *한 층도* 없다 (Weitze 보다 한 칸 아래).**
  - 접촉 = **LJ(12-6 점착·반발) + 순수 Hertz(항복 캡 없음) + Coulomb 마찰**.  **형상변화·잔류겹침·void-fill 전부 부재**,
    springback 도 없다.  ⇒ **접촉모델 층위지도**: `Schreiner EEPA(접촉소성) ≳ Varkey Thornton–Ning(접촉소성)
    > Weitze JKR(탄성+점착, 형상 resolved) ≳ 본 논문(탄성+점착, 구)` — **SHAPE 소성은 넷 다 없음 = 우리 MPM 고유 칸**
    (frame[5] *4중* 독립확증으로 갱신).
  - ★★ **소성 부재가 *관측량을 망가뜨린 자리*가 눈에 보인다**: δ_e 가 **30 % 압연에서 정점(3.27 S/m) 뒤 50 %에서
    1.63 S/m 로 반토막**나고, 저자는 *"the partial occupation of the volume of CBD particles by other materials due to
    high pressure, **which is a limitation shown by the model**"* 이라 적고 **"이 모델은 압연도 ~35 % 까지만 쓸 만하다"**
    고 스스로 유효구간을 좁힌다.  **우리 해석**: 소성으로 흐르지 못하는 강체 구가 서로를 밀어내며 CBD 상을
    기하적으로 잠식하는 것 = **연화·소성 부재의 직접 대가**.  Fig 3c 가 그 자리를 보여준다(상부 24–28 µm 에서
    pore·CBD → 0.03–0.05, AM → 0.74).
  - ★ **우리 쪽 양방향 진단 실험**: 우리 DEM+MPM 압밀 스윕에서 **같은 비단조 붕괴가 나오면 안 된다**(소성이 있으므로).
    안 나오면 "강체-구 인공물" 진단이 교차검증되고, 나오면 우리 첨가제 상 처리(CBD 대응 = VGCF/SDCP)를 의심해야 한다.
  - ⚠ **헤드라인 "최적 압연도 ≈ 40 %"(δ_e/τ_g 최대)는 저자 자신의 유효구간(≲35 %) 밖**이고, 분자 δ_e 가 이미
    인공적으로 꺾인 뒤에 생긴 최대다(δ_e↓·τ_g↓ 구간에서 비의 최대 위치는 분자의 인공붕괴가 정한다).
    ⇒ **그 40 % 를 정량 인용하지 말 것.**

- **★★★ PyCompact 2026 (`pycompact2025_dem_mpfem_workflow`) — 층 3(입자 형상 소성)이 *연속체 소관*임을
  제3자가 문장으로 적고 구현했다.  단 우리에게 불리한 칸이 하나 있다.**
  (⚠⚠ **Fe–Si–Al–P 금속분말 @1400–2000 MPa** — 절대값 전이 0건, 방법론만.)
  - **① 인용 가능한 제3자 진술 3종** (원문): DEM 은 *"assumptions of rigid or simplified particle shapes
    that **neglect internal deformation**"* / MPFEM 은 *"each particle is modeled as a **deformable finite
    element body** … localized plasticity at contact points"* 이고 그것이 *"**essential** for accurately
    predicting high-pressure compaction behaviour"* / 대칭으로 균질화 FEM 은 *"**overlooks the discrete
    nature of particles**, leading to inaccuracies in modeling **low-density stages where particle
    rearrangement dominates**"*.  ⇒ **frame[5] 분업(DEM=재배열·패킹 / 연속체=형상소성)이 우리 편의가
    아니라 방법론의 구조**라는 논증이 외부 문장으로 닫힌다.  ⚠ "essential" 은 **그들의 고압 금속압축
    맥락**이므로 한정어와 함께 인용할 것.
  - **② 층위지도 갱신** — 이 논문은 **접촉 LAW 층(Luding/EEPA/Thornton–Ning, 우리 "경로 A")을 통째로
    우회**하고 입자마다 tet 메시를 깐다.  PEEQ **1.3(=130 %)**, 구 → 다면체(Fig 4e/f).
    ⇒ 한 줄 규칙: **"층 3 에 도달하는 길은 둘뿐 — 입자마다 연속체를 메시하거나(MPFEM), 입자 없는
    연속체로 상 전체를 흘리거나(MPM).  접촉 LAW 를 아무리 정교화해도 층 3 에는 못 간다."**
  - **③ ★ PEEQ 무늬가 우리 MPM champion 과 같다** — 접촉/네크 붉음(0.8–1.3) + **코어 파랑**(0.1–0.3)
    = **core-preserved + boundary-flattening**.  우리가 SEM 으로 맞춘(`vis_zoom ④`, E 1.53/σ_y 0.15)
    그 무늬를 **다른 재료·다른 이산화(Lagrangian FE)** 가 재현한다 ⇒ 형상소성 morphology 가
    **재료·이산화에 둔감한 보편 무늬**라는 (약한) 증거.
  - **④ ⚠ 우리에게 불리한 칸 = 접촉과 형상소성을 *한 이산화 안에서 동시에* 갖는다.**
    | | 명시적 접촉 | 진짜 형상소성 | 그래서 필요한 우회로 |
    |---|---|---|---|
    | **우리 DEM** | ✓ 강체 구 접촉망 | ✗ | **Stage-E** (겹침 δ → 소성 접촉면적, Tabor/volume 캡) |
    | **우리 MPM** | ✗ 격자 암묵(같은 셀 = no-slip 융합) | ✓ | **기하/변형 coverage** (Hertz 0.13 / Tabor 0.26 µm 밴드) |
    | **MPFEM** | ✓ penalty + Coulomb µ | ✓ | 없음 |
    ⇒ MPFEM 이면 **변형 접촉면적 a(δ) 위에서 Holm 협착저항**을 바로 계산할 수 있다 =
    **Stage-E 근사의 상위 대체재가 원리적으로 존재한다.**  그들 Fig 3(f) 는 µ 0.1→0.3 이 RD 를
    **84.2→86.0 %**(digitized) 움직인다고 보여준다 = 우리 MPM 이 통째로 못 갖는 자유도.
    ⚠ 단 **이 논문은 전달물성을 한 번도 계산하지 않는다** — 가능성이지 실증이 아니다.
  - **⑤ 그럼에도 우리 규모에선 MPM 이 옳다 (비용이 자릿수)**: 그들 실측 **569 입자 / 2000 el = 9 h /
    24 CPU**, 입자수 스케일 지수 **1.34–2.43**(Table 1).  `derived(ours)` 우리 real_14 의 **SE 32,832 개**
    로 환산하면 입자수만으로 **22–164일**, ⌀1 µm 의 **explicit dt 벌금 ×16** 을 곱하면 **≈1년**(24 CPU),
    요소 **65.7 M**.  ⇒ 방어 가능한 문장: *"MPM 을 고른 이유는 침대 규모와 대변형 견고성이지 접촉
    표현의 우수성이 아니다."*
  - **⑥ ★ 실행 가능한 절충 (신규 백로그)**: **소형 SE-only REV(100–500 입자)** 를 OpenRadioss MPFEM 으로
    한 번 돌려 **변형 접촉면적 a(δ) 분포**를 뽑고, 그것을 **우리 Stage-E 의 외부 검증**으로 쓴다.
    그들 실측 스케일이면 **수 시간~하루 급**.  성공하면 *"Stage-E 는 근사인가 정당한가"* 를 처음으로
    외부에서 잰다.
  - ⚠ **그들 쪽 결함도 함께 기록**: **"convergence" 라고 적었지만 Fig 3(e) 는 2000→2500 el 에서
    `derived(ours)` **−5 %** 로 단조 감소 중**이고 실제 선택 근거는 본문이 밝힌 **런타임 9 h vs 36 h** 다.
    우리 CL-41(vox 0.15→0.115 미수렴)과 **같은 상황·다른 라벨** — 인용할 때 그 차이를 살릴 것.

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

- **★ Luan 2025 AFM — 입경은 거의 같고 *분포 형태*가 다르다 (단봉 AM), 그리고 dip 데이터가 없다.**
  | 항목 | Luan (stated, SI Fig S2) | 우리 | 판정 |
  |---|---|---|---|
  | CAM 입경 | **NCM88 3–5 µm 단봉** | AM_P/AM_S **bimodal** (12:4:1 = AM_P:AM_S:SE) | ⚠ **단봉 vs bimodal** → dip 위치·깊이 다름 |
  | SE 입경 | **LPSC 1–2 µm** | r_SE 0.5–1.5 µm (**production ⌀1.0**) | ★ **거의 동일** |
  | 크기비 AM:SE | ≈ **2.7 : 1** (D50 추정) | mono 4:1~8:1 / bimodal 12:4:1 | ★ 우리 **mono-AM_S(4:1)** 케이스에 가장 가까움 |
  | 도전재 | Super P **60–80 nm** | Super P 0D 가정 | ★ 우리 가정과 일치 |
  | CAM wt% 범위 | **80–95 wt%** | corpus **60–95 wt%** | ★ **그들 전 범위가 우리 corpus 안** = 우리가 그들 설계창을 커버 |
  | porosity / Furnas dip | **측정 없음** | dip AM 70–85 wt% | ⛔ 대조 불가 |
  - ★ **Fan 2026 §3.5 입경 설계창 재확인**: 상용 LPSC **1–2 µm** 는 파쇄 임계(>3 µm) 아래 = **협동변형 영역**.
    우리 production **r_SE = 0.5 µm (⌀1.0)** 이 이온(Cronau 무손실 최대 크기) ∧ 기계(협동변형) 두 축 최적점에
    동시 착지한다는 사후 정당화의 **네 번째 사례**(산업 파일럿이 실제로 그 창 안의 분말을 쓴다).
  - ⚠ **그들의 "SE 함량 최적 ≈ 20 wt%"(Fig 7a)는 *패킹* dip 이 아니라 *전자 퍼콜레이션* dome** 이다.
    우리 Furnas dip(기하 패킹, porosity 축)과 **다른 물리** — 같은 그림·같은 표에 섞지 말 것.
    (우연히 둘 다 "중간 조성이 최적"이라 혼동하기 쉽다.)

## E. 우리 계산이 문헌을 "검증/교차검증"하는 지점 (강점으로 쓸 것)
- ★★ **Giannis 2021 의 β 가 정말 자유변수인지 — 우리가 저자보다 잘 판정할 수 있다** (2026-08-25 신설,
  카드 `papers/giannis2021_stress_based_multicontact_dem.md` §4.6):
  eq 10 에서 β 와 ν 는 **항상 곱으로만** 등장하는데, 논문의 4개 보정값을 그 곱으로 다시 쓰면
  **β·ν = 0.787 (고무 단일 구) / 0.800 (고무 침대) / 0.825 (하이드로겔 침대) / 1.241 (유리)** —
  **E 가 23.3 kPa → 65 GPa 로 2.8×10⁶ 배 변하는 동안 1.58× 폭 안**에 들어오고 셋은 ±2.4 % 로 뭉친다.
  저자들은 이 조합을 **보고하지 않았고**, β 단독의 3.1× 차이를 "뻣뻣하면 접촉면적이 작아서"로 설명한다 —
  그 차이의 **2.08배는 그냥 ν(0.5→0.24)** 이고 남는 건 1.5× 뿐이다.
  ⚠ **남은 1.5× 를 물리로 귀속할 수 없다**: 보정항은 **배위수 C 에 비례**하는데 유리 케이스는 입자 **17개**(원통)라
  C 가 514-입자 침대보다 낮을 것이고, **논문이 C 를 한 번도 보고하지 않아** 분리 불가.
  ★ **우리는 침대의 C 를 정확히 안다** ⇒ `ΔF/F = k·β·ν·C·(δ/d)` 를 우리 침대에 걸어 **C-보정된 β 를 재추출**하면
  논문이 못 한 분리를 할 수 있다. 성공하면 결론은 **"β 는 자유변수가 아니다 (β ≈ 0.8/ν)"** — 원저자보다 앞선 기여.
  (그 가설대로면 우리 LPSCl ν=0.37 → **β ≈ 2.1–3.4**, 새 보정 없이 쓸 값.)
  ⚠ **논문의 주장이 아니라 우리 재분석**이다 — 4점·3재료·C 미보고. 인용 시 반드시 그렇게 표기.
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

- **★★★ Luan 2025 AFM — 이 문헌의 핵심 주장을 *우리가 숫자로 갖고 있다* (E축 최상급 사례).**
  Luan 의 논문 제목·서사 전체가 "**이온 flux 와 전자 flux 는 두께를 가로질러 정반대 프로파일**"(Fig 3c)이라는
  개념 위에 서 있는데, 정작 그 비대칭을 **정량화하지 않는다**(그림은 모식도, 시뮬은 방전시간 s 단위 비교).
  **우리 STEP4 운전-φ(z) export 는 그 값을 직접 준다: 2C 옴강하 = 전자 0.01–0.03 mV vs 이온 84–90 mV.**
  - ⇒ 발표/원고 문장: *"문헌은 이온/전자 flux 비대칭을 개념으로 제시했고(Luan 2025), 우리 STEP4 는 그것을
    ~10³–10⁴ 배의 옴강하 비로 정량한다."* — **frame[4] 교차검증**(서로 보정한 적 없는 두 경로).
  - ⚠ **프레임 정합 필수**: 우리 φ 비교는 **@1C 운전 프레임** 값이어야 한다(@1V 수송프로브는 비운전 —
    CLAUDE.md 필드 라벨링 규약). Luan 은 0.1–1 C 운전이므로 @1C 프레임끼리 비교.
  - ★ **총량 보존 게이트의 방법론적 승인**: Luan 실험 3배치(93:6:1 / 91.5:7.5:1 / 90:9:1 재배치)와 COMSOL
    Table S1(0.1875·0.25·0.3125, 평균 0.25 고정) **둘 다 총량을 고정하고 위치만 바꿨다**. 우리
    `--poro-grad` 의 "총 porosity 고정, 프로파일만 이동 + 마지막 pass UNGATED 폴백" 설계와 **같은 규율** ✓
  - ★ **반증 가능한 예측 하나 (우리가 먼저 맞힐 수 있다)**: Luan DRT 는 **positive 가 10⁰–10¹ s 대역에서
    오히려 저항이 높다**(SE-lean 93 % CAM 층의 국소 단거리 이온수송 제한, stated)고 인정한다.
    우리 STEP4 층별 반응분포도 **SE-lean 층에서 국소 과전압 증가**를 보여야 한다 — 보이면 층내 국소
    이온부족을 잡는다는 증거, 안 보이면 정량화된 모델 한계(frame[4]).

- **★ Alabdali 2023 (`alabdali2023_cgmd_wet_manufacturing_ssb_cathode`) — 우리가 *그 논문의 데이터를 사용 가능하게 만든* 사례 3건.**
  - ★★ **(검산 1) 축 단위가 성립하지 않는 D_eff 를 해독했다.**  Fig 4b 좌축은 `D_eff [dm² s⁻¹]` 인데 이 단위로는
    물리량이 성립하지 않는다.  그런데 본문 정의 **τ = √(η/D_eff)** 에 **Fig 3b/3c 에서 읽은 η(≈22 %(건조) /
    26–28 %(50 % 압연))** 를 대입하면 **찍힌 τ_g 를 소수 첫째자리까지 재현**한다(10.24 vs 10.17 · 2.21–2.31 vs 2.21).
    ⇒ **플롯된 D_eff 는 "벌크 대비 %"** 이고, 그러면 **formation factor = 0.21 % → 5.25 %** 로 **비로소 인용 가능**해진다.
    논문은 이 연결을 하지 않는다 — **우리가 이은 것**.
  - ★ **(검산 2) 조성 wt% ↔ vol% 교차검증.**  stated 69.0 / 27.6 wt% 를 문헌 밀도(NMC622 ≈ 4.7 · LPSCl ≈ 1.64 g cm⁻³,
    ⚠ **논문 미제공, 우리가 대입**)로 환산하면 **AM:SE = 46.6 : 53.4 vol%**, Fig 3b 판독은 **48.8 : 51.2** —
    ±3 %p 이내.  ⇒ "69/27.6 은 wt% 다"라는 해석과 우리 Fig 3b 판독이 **서로를 검증**한다.
  - ★ **(검산 3) Fig 4c 는 Fig 4a·4b 에서 재생된다.**  digitized δ_e/τ_g 를 직접 계산해 최대값으로 정규화하면
    Fig 4c 막대와 일치하고 **최대 위치도 40 %** 로 같다 ⇒ **세 패널의 digitize 가 상호검증**됐다
    (우리 digitize 신뢰도의 자체 감사).
  - ⚠ **반대로 우리가 그들에게 요구할 자리**: **격자수렴**.  그들은 voxel 크기조차 안 적었고 우리는 같은 종류의
    복셀 FV 에서 격자만으로 σ_e 비가 **+42.15 → +8.49 %**, σ_ion 비는 **부호까지 뒤집힌다**는 것을 실측해
    **자기 헤드라인을 철회**했다(SR-01).  ⇒ **"우리가 문헌을 검증하는" 축이 아니라 "우리 규율이 문헌보다 앞선"
    축**으로 쓸 것.

## F. 우리가 아직 못 하는 것 / 흡수할 것 (정직 목록 → 향후)

- **★★★ 보정 규범 미충족 4건 — Coetzee 2017 기준 (2026-08-25 신설, `papers/coetzee2017_dem_calibration_review.md`).**
  리뷰가 요구하는 것 중 **우리가 아직 못 한 것**만 모았다.  §A 의 Coetzee 항목(우리에게 유리한 쪽)과 짝이다.
  - **F-C1 · 유일성을 한 번도 시험하지 않았다.**  리뷰 처방(§5 p.123): *"more than one experiment should be
    conducted and **each experiment should isolate a single parameter** …, or the combined results from more
    than one experiment should provide a unique set."*  우리는 **1 관측량(porosity@300) → 1 파라미터(E_eff)**
    이고, μ·COR·ν 는 문헌값 고정이다.  형식상 유일하지만, "구속 단축압축이 마찰에 둔감하다"는 근거가
    **Coetzee & Els [25]/[205] 의 파쇄암·옥수수·저응력 결과**를 빌려온 것이고 **우리 계에서 재현된 적이 없다**.
    → **실행**: E_eff 고정, μ_pp·μ_pw·COR ∈ {0.2, 0.4, 0.6} OAT 로 ε@300 을 재는 **민감도표 1장**
    (기존 pure-SE 침대 재압축 6–9 런).  ∂ε/∂μ ≈ 0 이 나와야 "우리 보정은 파라미터를 고립시킨다"고 **쓸 자격**이 생긴다.
    ★ 설계는 베낄 것이 있다 — `bazzoun2025_dem_parameter_sensitivity_assb_cathode` 가 **우리 소재계·같은 LIGGGHTS**
    에서 8입력 OAT 를 이미 했다(μ_CAM-SE 최강 민감).
  - **F-C2 · 검증이 보정과 "충분히 다르지" 않다.**  리뷰(§2 p.106): *"the calibration experiment **is different
    from** the final experiment"*; (§5.2 p.125, Derakhshani 비판): *"It would be better to perform a validation
    experiment **totally different** … because if it is very similar, the mechanisms involved would be similar
    and **one would expect good results**."*  우리 3대 검증을 이 자로 재면 —
    · **Heckel 4압력** = 같은 시험의 다른 하중 (같은 기전) · **Cronau overlap 11–12 %** = 같은 런의 다른 관측량 ·
    · **독립 MPM 이 같은 18× 요구** = §8 (p.136) 이 허용하는 *"results from other numerical analyses"* ✅ 유효,
      단 인용 시 **frame[4] 조건(서로에게 맞추지 않았음)** 을 반드시 병기해야 순환이 아니다.
    → **가장 규범-정합적인 한 수** = 압밀 보정을 **전달 실험**(Bazzoun σ_eff,ion EIS · Minnmann EIS-TLM · Oh bimodal)
    으로 검증 (기전이 완전히 다름).
  - **F-C2′ · 그런데 리뷰의 두 번째 요구가 그 길을 막을 수 있다.**  리뷰는 *검증시험이 그 파라미터에 **민감**해야*
    한다고 요구한다(§5.2 p.125).  그런데 우리 사내 실측은 **σ 가 E_eff 에 둔감**하다고 말한다 —
    *"σ_ionic 은 E 가 아니라 porosity 를 따른다"*, *"E 1.35 ≡ 1.5 는 구조·역학·전달 전 축에서 동일 regime"*.
    ⇒ **σ-검증을 쓰기 전에 σ 의 E-민감도를 먼저 재야 한다.**  둔감으로 판명되면 후보를 바꾼다:
    (a) 조성 스윕 **Furnas dip 위치**(기하 지배 → E 의존성이 porosity 와 다름) (b) **다압력 두께·스프링백**.
    ★ 부작용은 오히려 기회다 — σ 가 porosity 에만 민감하다면 **실질 보정변수는 porosity** 이고,
    *"E_eff is the **micro parameter** adjusted so that the assembly reproduces the measured **macro** porosity;
    it is a **model parameter**, not the SE Young's modulus"* 가 리뷰 §1(p.105)과 정확히 같은 어법이 된다.
  - **F-C3 · 강성↔배위수 결합이 전달 그래프를 오염시킬 수 있다 (미측정).**  **Ng & Asce [193]** (p.130):
    *"**Decreasing the particle stiffness resulted in a higher coordination number** and these two effects
    balanced each other"* — 역학은 상쇄돼도 **접촉망은 바뀐다**.  우리는 E_eff 를 **역학(porosity)** 으로 정한 뒤
    **그 침대의 접촉망**으로 σ 삼중항을 푼다 ⇒ **역학 보정이 전달 그래프를 정의한다**.  사내 확인은
    **1.35 ↔ 1.5 구간뿐**(overlap 1.75 vs 1.74 %, ⟨δ⟩ 0.0739 vs 0.0743 µm = 동일 regime)이고
    **24 → 1.35 구간은 미측정**.
    → **실행**: 같은 침대를 E = {24, 5, 1.35} 로 압축해 **Z(배위수)·접촉면적 분포·σ 삼중항**을 나란히.
    Stage-E(Tabor+volume) 면적 재유도가 이 오염을 얼마나 흡수하는지가 그 표에서 보인다.
  - **F-C4 · 다압력 사용은 리뷰 기준 외삽이다.**  Li [189] (p.129) / Franco [196] (p.130) 의 "보정 응력 = 응용
    응력" 규칙은 300 MPa 에서는 지켜지지만 **100/200/600 으로 확장하는 순간 우리를 문다**.  방어 가능한 유일한
    서술: *"E_eff 는 300 MPa 에서만 맞추었고 나머지 압력은 **예측**"* + Heckel R²=0.965 를 **적합도가 아니라
    예측 정확도**로 제시.  ⚠ **원고·CLAUDE.md 현행 표기("DEM pure-SE 4압력")는 적합만 적혀 있어 오해 소지** — 문구 점검 필요.
  - **F-C5 · 구(sphere) + rolling friction 없음의 원리적 한계 (해소 불가, 고지 대상).**  **Coetzee [62]** (p.113):
    *"Spherical particles without rolling friction … **could not be calibrated** … **even when high particle
    friction coefficients were used**."*  + **Santos [170]** (p.125): 구형 입자는 보정값이 *"**cannot be
    generalised**"*.  우리 타깃은 마찰이 아니라 porosity 라 직격은 아니나, **우리 침대의 전단강도는 원리적으로
    과소**이고 그 결손도 E_eff 에 흘러든다.  ⇒ `E_eff = 1.35 GPa` 은 **{구 근사 + hooke/hysteresis + 재배열·
    GB slide·미세파괴 결손}의 합산 상수**로만 보고할 것 (우리 frame[2] 서술 그대로 — 리뷰가 그것을 **지지**한다).
  - **F-C6 · 보고 서식 (저비용, 즉시 흡수).**  리뷰 §1 (p.105) 은 *"**whether they were measured or calibrated
    is not clear**"* 를 문헌의 결함으로 지목하고, 리뷰 자신은 **Table 1(bulk-calibrated) / Table 2(directly
    measured)** 로 **provenance 별로 표를 가른다**.  → 우리 SI 파라미터 표에 **`source`(measured/calibrated/
    literature/assumed) + `code` + `contact law` + `value type`(particle vs contact)** 열 추가.
    ⚠ **"리뷰가 이 서식을 규정한다"고 쓰면 과장** — 명시 처방은 없다(=n/a).  근거는 §1 의 결함 지적 + 리뷰의 자기 실천.
    ★ 특히 §4 (p.122): 코드에 따라 **입자강성 지정 vs 접촉강성 지정**이 다르고 후자는 **직렬 두 스프링 = 절반**
    이므로, `E_eff` 가 **재료(입자) 입력값**임을 표에 못 박아야 한다.
  - **F-C7 · 그림 양식 2종 (즉시 흡수).**  **Fig 32/33** = *보정 곡선 + 실험 min/avg/max 수평 밴드*
    (우리 `ε vs E_eff` 곡선 + Minnmann 밴드로 바로 재현 가능) · **Fig 25** = *두 관측량의 등고선 교차 = 유일해*
    (F-C1 과 F-C2 를 **한 장에** 해결하는 목표 그림).

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
- ~~**multi-contact 구속항 F_mc** (Varkey) vs 우리 18× 연화 — 같은 증상(ρ>0.7 과강성) 다른 처방~~
  ⛔ **2026-08-25 정정 (원전 Giannis 2021 digest)** — *같은 증상이 아니고 부호가 반대다*. §A 정정 블록 참조.
  ★ **대신 이 자리에 남는 진짜 공백 = 배위수 의존 접촉강성.** `ΔF/F ∝ C` (카드 §7-2·7-4):
  Hertz 도 `hooke/hysteresis` 도 **한 입자에 접촉이 몇 개인지 모른다.** 같은 겹침이라도 잘 구속된 입자의 접촉이
  더 뻣뻣하다는 물리가 **우리 DEM 에 전혀 없다.** 우리는 C 를 **전달**(σ_ionic ∝ CN²)에만 쓰고 **역학엔 안 쓴다.**
  ⇒ 새 예측(미시험): MC-stress 를 켜면 **SE-rich(고 C) 침대가 AM-rich 보다 더 뻣뻣해져 Furnas dip 의 SE-rich flank 가
  올라간다** = "dip 은 순수 기하"(frame[3]) 판정에 대한 **직교 시험**.
  ★ **이식 난이도 재평가**: 원전은 **Ansys Rocky 가 아니라 LIGGGHTS 에 구현**했고 **부록에 2-pass pseudo-code 를 공개**했다.
  `Σ l⊗f` 는 LAMMPS/LIGGGHTS 의 **`compute stress/atom`(per-atom virial)** 그 자체 = 재료가 이미 있다
  (⚠ V_p 로 안 나눔 · 부호 규약 확인 필요). 비용은 **classical 대비 5.7–6.4×**(514 입자 실측) — 우리 36k–73k 침대엔 실부담.
  ⇒ 경로 B 는 "상용/커스텀 필요"에서 **"가능하지만 부호가 안 맞아 지금은 이득 없음"** 으로 재분류.
- **항복캡 접촉**(So 2021 H-cap / Thornton–Ning p_y) — real E로 18× 연화 **제거** 가능 경로(1순위, `elasto_plastic_feasibility.md`).
  ★ **Giannis 2021 이 이 우선순위를 강화한다**: 세 처방(우리 18× 연화 / 항복캡 / multi-contact) 중 **부호가 맞고
  자유변수가 0인 것은 항복캡뿐**이다. Giannis 의 β 는 저자 표현 그대로 *"**adjustable dimensionless empirical**
  geometric prefactor … **must be carefully calibrated depending on the type of the material**"* = **우리 E_eff 와 같은
  1-파라미터 보정**(유도 아님, FEM 유도는 outlook). 단 구조는 그쪽이 낫다 — **β 는 별도 항에 격리되고 E·ν 는 실측값
  그대로**인 반면 **우리 E_eff 는 측정 물성 자리를 덮어써 하위 계산(Hertz 접촉반경·k_n·k_t·파속·timestep·Stage-E 입력)
  전체를 오염**시킨다. ⇒ 우리 연화의 진짜 약점은 "경험적"이 아니라 **"물성 자리를 점유한다"** 는 것이고, 그걸 없애는
  것은 **경로 A** 다.
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

- **🎤 [YMLee26-DTBL] 발표 덱이 새로 노출한 우리 공백 2건 + 저비용 흡수 1건**
  (`talks/lee2026_yonsei_dtbl_ai_electrode_digitaltwin.md` §8c–8d·§12; ⚠ **덱 등급** — 수치 인용 금지):
  - ★ **습식 DEM(슬러리 믹싱) + 모세관 가교 = 우리 DEM 접촉모델의 미보유 물리.** 그들은 **NCM/NMP/2nd solvent**
    3성분 DEM으로 *"bulk 용매와 비혼화성인 소량의 2nd solvent가 입자 사이에 모세관 구조를 만들어 CBD migration을
    억제한다"* 를 보인다(입자 간 간극에 2nd solvent 집중, 표면에 NMP). **우리 DEM은 건식 분말 압밀 전용**이고
    접촉모델은 DMT/JKR 부착 + 소성뿐 → **액상 가교 힘 항이 없다**. ⇒ ① positioning 문장을 **"DEM은 그들도 쓴다
    (습식 믹싱) / 우리는 건식 압밀 + granular constriction σ + 소성 MPM"** 으로 좁혀 재작성(현행
    `positioning_vs_geodict.md` 는 이 사실을 반영하지 않음), ② 습식/건식 공정 비교가 필요해지면 모세관 가교가
    선행 흡수 항목. **정본 미보유(ACS Energy Lett. 10 (2025) 6223-6235) → 위시리스트 1순위.**
  - ★ **OWRK 기반 work of adhesion / 계면 표면에너지 실측** — NCM·CB·PVDF × (NMP / 2nd solvent) 를
    접촉각→OWRK 로 정량. **우리 DEM 부착 파라미터는 전부 문헌 차용**이라, 이건 *우리 입력을 실험으로 고정하는
    경로*다(실험 협업 제안 소재). 같은 논문 소속 → 정본 미보유.
  - **저비용 흡수(즉시 가능):** **REV/voxel 수렴을 정확도-비용 2축으로 한 장에 보고하는 그림 양식**
    (덱 슬 19: voxel 50/75/150/300/600 nm @ domain 30³ µm + domain 15→90 µm @ voxel 75 nm + voxel수 대
    메모리/시간). 우리는 domain·voxel 선택 근거를 수치로 남기지 않는다. ⚠ 그들 절대 시간·메모리
    (~250–280 M voxel → 45–57 GB, 2.5–3 day)는 하드웨어·GeoDict 의존 → **우리 벤치마크 아님, 형상만.**

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

- **★★ Luan 2025 AFM — 우리 Phase-5 / 백로그 A7 이 *잘못된 물리량을 구배하고 있었다* + 미보유 목록.**
  (digest `papers/luan2025_graded_cathode_400whkg_pouch.md` §8 P-1…P-7)
  - ★★ **A7 의 노브 오정렬 (가장 큰 소득).** 현행 `extract_2d_microstructure.py --poro-grad` 는
    **porosity(z)** 를 구배한다(출처 #286 Yoo = **흑연/액체계 급속충전**). **Luan 이 구배하는 것은
    조성 φ_SE(z) 이지 porosity 가 아니다.** 두 노브는 다른 물리다 —
    porosity 구배 = *공극이 어디 있나* / **SE 구배 = *이온 도체가 어디 있나*(ASSB, 우리 소재계)**.
    ⇒ **신설 제안 `--se-grad [−1..1]`** (>0 = 분리막쪽 SE-rich = Luan positive), 규약은 `--poro-grad` 와 동일
    (**총 SE 고정** · K=8 밴드 리포트 · 마지막 pass UNGATED 폴백 · 부호 규약 y=0 집전체 / 상단 분리막).
    **검증 케이스를 논문이 다 지정해준다**:
    | 런 | φ_SE (집전체측 / 분리막측) | 출처 |
    |---|---|---|
    | exp-Ⅰ positive | **0.140 / 0.201** | 실험 93:6:1 ǀ 90:9:1 (**DERIVED vol%**, ρ 4.8/1.86/2.0 ASSUMED) |
    | exp-Ⅱ uniform | 0.171 / 0.171 | 91.5:7.5:1 |
    | exp-Ⅲ reverse | 0.201 / 0.140 | — |
    | sim-Ⅰ/Ⅱ/Ⅲ | **0.1875/0.3125 · 0.25/0.25 · 0.3125/0.1875** | **Table S1 그대로 (stated)** |
    → STEP3 로 밴드별 σ_ion·σ_e·τ, STEP4 로 반응분포·용량 → **순서 positive > uniform > reverse** 재현 여부.
    **방향·순서만 요구하고 절대값은 요구하지 않으므로 안전한 외부 앵커.**
    ⚠ **COMSOL 조성 ≠ 실험 조성**: 시뮬 평균 φ_SE 0.25·대비 0.125 vs 실험 DERIVED 0.171·0.061
    (평균 **1.5×**, 대비 **2.05×**). 그래서 시뮬의 reverse 페널티(+45 %)가 실험(+15 %)의 3배 — **두 세트를
    같은 축에 놓지 말 것**, 우리 검증도 두 세트를 **따로** 돌릴 것.
  - ★ **`--cb-grad` 의 방향 답이 생겼다 (크기는 무시할 만함).** A7 규약은 "carbon:binder optimum 은 재료의존
    (#286 gradient vs #20 uniform) → 둘 다 노출, 고르지 않음" 이었다. **황화물-ASSB 도전재 축에 대해
    Luan 이 답한다: reverse(집전체 rich), 이득 ≈2 %** (Fig 7c: 0.05/0.95 에서 1040 vs 1020 s, figure-read).
    ⇒ A7 문서에 **방향만 기록**. ⚠ 이는 **COMSOL 전용**(도전재 구배 실험 대조군 없음) → **기본값 변경 근거로는
    약함**. ⚠ 우리 `--cb-grad` 는 **carbon:binder 비**, Luan 은 **carbon:총량** — 매핑 시 바인더 축 분리 필요.
  - ★ **설계창을 ML 폐루프의 제약으로.** §3-4 표(CAM 분율 × 면적용량 → 명목용량 도달 여부:
    **1 mAh 95 % ✓ / 2 mAh 93 % ✓·95 % ⛔ / 4 mAh 90 % 천장·93 % ⛔**) + Fig 1b,c(400 Wh kg⁻¹ =
    CAM > 80 wt% ∧ 면적용량 > 4 mAh cm⁻²) ⇒ `scripts/ml_design_loop.py` 의 **feasible-region 외부 제약**.
    예측기가 "CAM 95 % @ 4 mAh cm⁻²" 를 최적으로 뱉으면 **문헌이 이미 기각한 설계**로 게이트 가능.
    ⚠ 이 창은 **σ_SE = 2 mS/cm · r_SE = 1–2 µm 조건부**(논문 자신이 명시) — SE 를 바꾸면 창이 이동.
  - **우리 미보유(그들 보유)**: 실제 사이클(50 cyc 92.9 %) · **5 Ah 파우치 스케일업** · 건식 롤프레스 층별 적층
    실공정 · **TOF-SIMS Li 공간분포 / XRD 깊이별 탈리튬화**(= 우리 STEP4 SOC(z) 의 실험 검증 수단) ·
    GITT/CV/DRT 반응속도론 분해(z₁ 이온레일만 있는 우리의 결손, Kim2025 와 같은 칸) · Si 음극 풀셀.
  - **역으로 그들이 미보유(우리 보유)**: porosity·두께·밀도 · 접촉망 σ 삼중항 · Holm 협착 ·
    퍼콜레이션/배위수/coverage · tortuosity · Furnas dip · 소성 형상변화 · 응력장 · 균열 · Heckel
    — **즉 미세구조 전체.**
  - ⚠ **인용 시 반드시 병기할 4가지**: ① **404 Wh kg⁻¹ = stack-level**(파우치필름·탭 제외; 본문 Eq (1) 은
    M_package 포함이라 **본문↔SI 불일치**) ② **404 셀은 85 %/88 % 이층**이라 91.5 % 구배 실험과 **다른 조성**
    ③ **σ_e 절대값 100× 단위결함** ④ **porosity·두께 미보고**.

- **★★ [Zhang23] (Joule 2023, `papers/zhang2023_pfib_multiscale_imaging_4d_thick_cathode.md`) — 우리가 *원리적으로* 못 하는 것의 가장 선명한 목록**
  (⚠⚠ 액체 LIB. 그래도 "무엇을 못 하는가"는 chemistry 와 무관하게 성립한다):
  - **우리에게 없는 것 5가지 (정직 목록)**: ① **실측 미세구조**(PFIB-SEM 3D 재구성 — 우리 구조는 전부 모델
    산물이다; 같은 축의 다른 사례 = `lim2025_virtual_calendering_framework` "reconstruct-then-compress")
    ② **실제 열화 관측**(균열 부피·접촉면적·CEI 두께를 **잰 적이 없다** — 우리 f_broken·A_rel·R_int(N) 는 전부
    모델/assumed-form) ③ **나노스케일 계면상의 z-분해 실측**(20 vs 5 nm 같은 값을 우리는 만들 수 없다)
    ④ **자체 전기화학 셀 데이터**(유지율·CE·전압곡선) ⑤ **세그멘테이션 실무 규약**(pore-back artifact 보정 등).
    ⚠ ⑤ 는 우리 복셀 규약 함정(SDCP 스탬프 표현부피 CL-25/33/34)과 **같은 종류의 문제**라는 점만 인식.
  - ★★ **반대로, 이 논문이 우리 novelty 를 *스스로* 증명하는 자리 (원고에 쓸 것)**: 이미징-우선 파이프라인은
    **실측 1건에 묶인다.** 그래서 **두께를 설계변수로 삼는 순간(Fig S9, 80/160/240 µm) 실측을 버리고
    "확률적으로 생성한(stochastically generated) 전극"으로 갈아탔다.** ⇒ 문장 후보:
    *"Even an imaging-first study must abandon the measured microstructure the moment thickness becomes a
    design variable — which is precisely the capability a process-physics generative pipeline supplies."*
    ⚠ **정직 조항**: 그들 생성기의 사양·검증은 **미보고**다 → **"우리 생성기가 더 물리적"이라 단정하지 말고**
    **"그들도 스윕에는 생성구조가 필요했다"** 는 사실만 쓸 것.
  - ⚠ **흡수 불가 (구조적)**: 그들 강점은 **장비**(Xe⁺ PFIB, 슬라이스당 84 s × 330 슬라이스, Avizo/INNOV 사슬)
    에서 온다 — 코드로 메울 수 없다. 대신 **협업/데이터 차용**이 유일한 경로이고, 그 경우에도 **액체계라
    우리 소재계에 직접 못 쓴다** ⇒ 우리에게 필요한 것은 **황화물 ASSB 의 동급 PFIB 데이터**다(현재 litdb 부재).
  - **흡수 가능 (즉시)**: ① 정규화 규약(균열/이차입자, 접촉면적/AM표면) ② 계면상 z-처방 형식(16구역+가우시안)
    ③ **최대 응집체 % 퍼콜레이션 지표**(§B) ④ Koponen flow-τ 계산법(우리 pore-τ 참조) ⑤ 두께 스윕 프로토콜.
  - ⚠ **그들도 못 한 것(우리와 공통)**: 열화 kinetics · 격자수렴 시험 · 세그멘테이션 불확실도 · 반복(n=1) ·
    **모델 출력의 직접 실험검증(0건)**. ⇒ "문헌 최전선도 kinetics 는 없다"는 것이 우리 assumed-form 밴드의
    **방어 논거**가 된다(면죄부가 아니라 field-level 상태 서술로).

---

- **★ Alabdali 2023 (`alabdali2023_cgmd_wet_manufacturing_ssb_cathode`) — 우리에게 없는 것 3 + 있는 줄 알았던 것 1.**
  - **① ★ 슬러리 *유변학* 보정 — 원천 없음, 그리고 이 축은 Weitze 에도 없다.**  그들은 **비평형 CGMD 로
    점도-전단율 곡선을 만들어** 자체 유변계(Kinexus) 측정과 맞춘다(**7×10⁷ step × Δt 0.001 µs = 시뮬 70 ms**,
    전단율당 ≈ 2일).  우리는 **젖은 상태를 모델하지 않으므로 이 축의 관측량 자체가 없다**.
    ⚠ 단 **일치는 20–200 s⁻¹ 평탄역 한정**이고(실험 곡선의 shear-thinning 가지 0.1–10 s⁻¹ 는 시뮬 점이 아예 없다),
    그 구간 실험 오차막대가 **±30 % 급**이다 ⇒ **판별력이 가장 낮은 곳에서 맞춘 일치**로 평가해야 한다.
  - **② 건조(용매 제거)** — CBD bead **7.5 → 3.0 µm 순간 축소**(부피 **1/15.6**) + FF 교체.  우리 미보유.
    ⚠ ASSB 주류가 건식이라 **우선순위는 낮다**(경로가 다른 것이지 뒤처진 것이 아니다).
  - **③ 공정 상류(혼합·코팅·건조조건) → 구조의 입력 축** — 우리 설계 노브는 조성·입경·압력에서 시작한다.
  - **④ ⚠ "우리에게만 없는 줄 알았던 것" 정정 — σ 실측은 *양쪽 다* 없다.**  그들은 **δ_e·τ_g 를 실험과 대조한 적이
    없고**(예측만), 우리도 **우리 침대 조성의 σ_e/σ_ion 자체 실측이 리포에 없다**(CL-34).  ⇒ 이 칸은
    **공동 공백**이며, 우리 쪽 해소 경로(Lee 2025 조성 80:17:3:0.5 로 같은-조성 대 같은-조성 침대 1건)가
    **이미 CL-46 에 적혀 있다**.
  - ★ **흡수 판단**: ①은 **ASSB 습식을 다루게 될 때만** 흡수(현재 우선순위 낮음), ②③은 **경로가 달라 흡수 불요**,
    ④는 **우리 쪽에서 먼저 닫아야 할 것**.  ⇒ 이 논문에서 실제로 가져올 것은 **유변학 방법론이 아니라
    §C-3 의 수치 목록**(SE PSD 7계급 · 상별 σ 입력 · δ_e/τ_g/formation factor · ε–압연도 3점)이다.

- **★★ PyCompact 2026 (`pycompact2025_dem_mpfem_workflow`) — 우리에게 없는 축 2개 + 잠재 결함 1개.**
  - **① 제하(unloading) / springback 을 우리는 안 푼다.**  그들은 하중–제하를 끝까지 풀고 **상대밀도를
    제하 후**(제하 중 **5 MPa** 도달 시점 규약)에 잰다.  우리는 하중 중/플래튼 정지 시점의 porosity 를
    보고한다.  ⇒ **규약이 다르다** — 문헌 절대값과 나란히 놓을 때 이 칸을 먼저 확인해야 한다.
    ★ 훔칠 형식 = **porosity–pressure 하중+제하 루프 한 장**(그들 Fig 4b).  점이 아니라 루프로 그리면
    springback 이 눈에 보인다.
  - **② ⚠ 잠재 결함 — 18× 연화는 제하 축에서 비물리적일 것이다.**  `derived(ours)` 탄성 회복변형 P/E:
    그들 **2000 MPa / 170 GPa = 1.2 %** · 우리 **MPM**(300 MPa, K=25.5 GPa @ν0.49) = **체적 1.2 %** ✓
    · 우리 **DEM**(300 MPa, E_eff 1.35, ν0.3 ⇒ K 1.125 GPa) = **체적 26.7 %** ⚠.
    ⇒ **우리 MPM 의 stiff-bulk(ν=0.49) 선택이 제하 축에서 정확히 실재 분말과 같은 자리**에 있고,
    **DEM 의 연화는 제하를 풀면 무너진다**.  지금은 제하를 안 풀어 **노출되지 않은 잠재 한계**다.
    ⚠⚠ **미해결 질문**: 우리 실험 앵커(**Minnmann pure-SE 10 % @300 MPa**, **Cronau overlap 11–12 %**)가
    **가압 중** 측정인지 **해압 후** 측정인지 — 후자면 우리 DEM porosity 를 **다른 규약의 값에 맞춘 것**이
    된다.  ⇒ **문헌 재확인 필요** (이 카드가 만든 질문, 미해결).
  - **③ 오픈 도구 정보**: **OpenRadioss(AGPL, 무료) = explicit 대변형 접촉 FE**.  ABAQUS 대비
    **7 h vs 5 h**(Table 3, 같은 문제·24 CPU) = **1.4배 느림이 라이선스 0원의 대가**.
    ⇒ 위 §C-⑥(소형 SE-only REV 로 Stage-E 외부검증)의 **실행 수단**이 확보된 셈.
  - ⚠ **흡수하지 않을 것**: 그들의 `MeshMatGen.ipynb` 자동메시(구 재생성 → tet)는 **LS-PrePost 포맷·GUI
    proj→k 라운드트립 해킹**에 묶여 있고, 우리는 애초에 **구를 다시 만들지 않는다**(복셀 union 으로 상을
    굽는다 — 압축된 침대를 넘기는 우리에겐 겹침 δ 가 커서 구 재생성이 **원리적으로 불가**).

- **★★★ Zunker & Kamrin 3부작 (2026-08-25) — 우리 공백 5건 + 흡수 우선순위** (카드 3장 참조)
  - **THEY LEAD (우리가 못 하는 것)**
    1. ★★★ **δ-의존 항복캡** `p_Y/Y = 1.75e^{−4.4δ/R} + 1` (2.75 → 1.0).  우리는 재하에 캡이 **없고**
       Stage-E 가 **사후에 상수 H(2.8–3.0Y)** 로 면적만 보정한다.  **우리 overlap 에서 참값은 2.08–2.26 Y**
       (DERIVED) ⇒ `A_tabor = F/H` 가 **24–44 % 과소**, σ_ionic ∝ √cov 이므로 **σ 가 12–20 % 과소**.
       ★ Jackson–Green 2005 가 **같은 방향**을 이미 지시 = **2 독립 출처** → 채택 근거 강화.
    2. ★★ **공극소멸 감지 `A_free/A_tot`** — 우리 DEM 은 "흘러들어갈 곳이 남았나"를 **모른다**.
    3. ★★ **2차 접촉 자동 생성** (상대변위 0 인데 반경팽창으로 생기고, 제하 후에도 **힘이 남는다**).
    4. ★ **제하 곡선이 저절로 나온다** (비선형 + 소성누적에 따른 강성증가까지 FEM 일치) — 우리 spring-back
       정량이 필요해지면 여기.
    5. ★ **잔류 반경응력**(실험 15 MPa) 을 재현한다 = **우리에게 없는 새 실험 대조축**.
       ⚠ 우리 RVE 는 측방 주기경계라 **벽이 없어** 그대로는 못 잰다 → 벽 있는 케이스가 필요.
  - **WE LEAD (그들이 못 하는 것)**
    1. **2상(SE + CAM)** — 그들은 *"varying material properties as **future work**"* 라고 **명시**한다
       (2025 §2.2).  ⇒ **우리 복합양극은 그 코드로 오늘 못 돌린다.**
    2. **전달 삼중항 σ_ion/σ_e/σ_thermal + Holm 협착 + Stage-E** — 그들은 전달이 **아예 없다**.
    3. **파쇄(Auerbach) · fracture-aware Holm** — 그들 모델에 **파쇄 없음**.  LPSCl 은 >3 µm 에서 파쇄한다.
    4. **다중압력 Heckel (100/200/300/600)** — 그들은 **프로토콜 하나**(0→0.4→0)뿐이다.
    5. **porosity 를 관측량으로 낸다** — 그들은 **세 편 통틀어 porosity 수치가 0개**다.
    6. **극단 다분산 12:4:1(반경비 0.083)** — 그들 검증은 **0.25 까지**이고 거기서 이미 최악이었다.
    7. **자유형상 소성 · 내부 변형장**(MPM) — §C 의 층(3).
  - **ADOPT (우선순위순, 앞의 둘은 DEM 재실행 불필요)**
    1. **Stage-E 상수 H → δ-의존 경화곡선** (비용 ≈ 0).  ⚠ 선행: 코드가 H 를 정확히 몇으로 쓰는지 확인
       (`network_conductivity.py` 5-regime) + **구-구↔구-평면 δ 환산 규약**(동일반경이면 δ_sf = δ_ss/2;
       12:1 이면 **SE 가 겹침의 92 %** — Zunker 2025 eq 3/4, DERIVED).
    2. **`A_free/A_tot` 후처리 추가** (LIGGGHTS 덤프만으로 계산).  용도: 벌크구간 진입 판정 / coverage 의
       새 분모 / MPM `d_h/dx` 트랙과의 상관.
    3. **결정 실험 = pure-LPSCl 을 그들 LAMMPS 브랜치로** (§A 의 신설 블록에 판정선 등록).
    4. **무차원 보고 규약** `F/(E R_o²)` · `δ_o/R_o` · `p̄/Y` · `A_C/(πR_o²)` · `V/V_o` 채택 →
       우리 접촉-수준 그림을 **문헌과 직접 겹쳐 그릴 수 있다.**
    5. **위상 페널티는 우리 규약에서 *비활성*** (동일크기 삼중항 발동 문턱 **δ/R > 0.30**, 우리는 0.15–0.22,
       DERIVED) ⇒ *"우리 겹침은 관통형 가짜 접촉을 만들지 않는다"* 를 **정량 방어문장**으로 쓸 수 있다.
       ⚠ 반대로 **강한 다분산에서는 홈에 낀 작은 SE 가 정당한 AM–AM 접촉을 소거할 위험**이 있다
       (거리 기반 중심판정이 크기를 모름; 카드 ③ §5-3b 의 기하 계산).  **크기-인지 중심판정** 제안은
       우리 몫 = 작은 방법론 기여 후보.
  - ⚠ **파라미터 전이 3대 함정**: ① `Δγ` — 그들 450 J/m² 는 **유효 파괴에너지**(K_Ic 역산), 우리 DFT
    `W_ad = 1.107 J/m²` 는 **열역학** 값 (**400× 차이**) → LPSCl 은 `G_c = K_Ic²(1−ν²)/E ≈ 3.24 J/m²`
    (K_Ic 0.3, E 24; Fan 2026 §3.5) 를 쓸 것.  ② 점착 유효조건 `2a/r_Ip ≈ 1.9` (DERIVED) 로 **소규모 항복
    조건이 LPSCl 에서 경계** → 점착 분기 켜기 전 eq (49) 실제 평가 필수.  ③ δ 환산 규약(위 ①-1).

## G. AM 입자 **내부**(sub-particle) 미세구조 — 우리 축 **아래 한 칸**, 접점은 방법론뿐 (2026-08-25 신설)

> **왜 새 축인가**: A(압밀/porosity) · B(전달 삼중항) · C(역학/morphology) · D(패킹) 는 전부 **입자 여러 개 =
> 전극 스케일**이다. 입자 **한 개 안의 grain 배열·결정방위·GB 손상**을 다루는 문헌이 들어올 자리가 없었다.
> 억지로 C 에 넣으면 "morphology" 라는 낱말만 같고 스케일이 달라 축이 오염된다.
> ⛔ 이 축은 **`comparison_vs_ours.md` 의 DFT 물성축 A–I 와 무관**하다 (밴드갭·E_a·σ_ion·ICOHP 없음).

```
DFT/MLIP  :  원자·셀            → 밴드갭 · E_a · ICOHP · ESW      (comparison_vs_ours.md)
─────────────────────────────────────────────────────────────────
축 G (신설):  입자 1개 안        → grain 배열 · 결정방위 · GB damage
A–D (기존) :  입자 여러 개·전극  → 패킹 · porosity · τ · σ_eff · 압밀
```

**[Yang26-BML]** `talks/yang2026_ncm_radial_microstructure_ml.md` — **양수영(한양대 BML),
"Multiphysics and machine-learning-guided design of radial cathode microstructures"**
(BML Research Seminar 2026-08-18, 슬라이드 21장 + 40분 16초 녹취). ⚠ **덱 등급 — `talks/README.md`.
게다가 L&F 제공 소재 + 미출판 + 회사가 출판 반대 → 수치 인용 금지.**

- **소재계가 우리와 다르다**: **액체전해질 LIB** (Li‖NCM96 하프셀, PVDF/Super P 94:3:3).
  황화물 ASSB 아님. 발표자 본인도 *"전고체보다는 LIB 로 진행하는 게 맞는 주제"* 라고 말했다.
  ⇒ **같은 표에 우리 LPSCl 수치와 섞지 말 것.**
- **🚩 이름이 같고 뜻이 다른 것 — `D₅₀`**: 저쪽은 **2차 입자 1개의 지름(설계 입력, 10–15 µm,
  L&F 공정 제약)**, 우리는 **분말 PSD 중앙값(측정 요약값)**. 나란히 쓰면 안 된다.
  굳이 쓰려면 `D50^(particle,design)` 으로 구분.
- **파라미터가 겹치나 → 사실상 안 겹친다.** 저쪽 5개 중 `D₅₀` 만 이름이 같고 뜻이 다르며,
  `D_seed · W_seed · W_radial · AR` 은 **입자 내부 grain 기술자**라 우리 DEM 에 대응량이 없다.
- **⛔ 우리 데이터에서 뽑을 수 있나 → 없다.** 우리 DEM 은 입자를 **구/강체**로 다뤄 **내부 grain
  구조 자체가 없다.** LIGGGHTS dump 에 `D_seed/W_seed/W_radial/AR` 에 대응하는 필드가 존재하지
  않는다. 게다가 **repo 에 `tools/liggghts*` 가 현재 없다**(`tools/` 31개 항목 전수 확인,
  2026-08-25) — DEM 축은 지금 **문헌·설계 문서만** 있고 실행 코드가 없다.
- **⛔ 타깃도 우리에게 없다.** `Q_CC`(P2D/전기화학 모델 필요) · `Damage`(cohesive-zone GB 모델 필요)
  둘 다 미보유. `σ` 는 우리 MPM 이 낼 수 있으나 **입자 내부가 아니라 입자 사이** 응력이다.
- **✅ 실제로 가져올 것 (수치 아님, 양식·규율 3개)**:
  1. **`Fig. 16` 히트맵 양식** — 열 합 100% 정규화 mean|SHAP| (설계변수 5 × 디스크립터 11).
     우리 DEM 민감도(접촉강성·마찰·점착·PSD → porosity/τ/σ_eff)를 **한 장으로** 요약하는 데
     축 이름만 갈아 쓸 수 있다. `bazzoun2025_dem_parameter_sensitivity_assb_cathode` 의
     민감도 결과를 이 양식으로 다시 그리는 게 가장 싼 적용.
  2. **디스크립터를 영역별로 분해하는 습관** (저쪽: particle / seed / radial 3분해).
     우리는 대부분 **전극 전체 평균 1개**만 낸다 → **"분리막 접촉층 / 벌크 / 집전체 접촉층"**
     3분해로 옮기면 **같은 계산에서 디스크립터가 3배**가 된다. 추가 계산 0.
  3. **"경계해 = 제약 신호" 규율** — 저쪽 최적해가 `D₅₀ = 10`(하한 정확히) · `W_radial = 0.302`
     (하한 0.30 근접) 로 **설계상자 모서리에 붙었다.** ⇒ 최적이 아니라 **범위가 물린 것**.
     우리 파라미터 스윕에도 같은 판정 규율이 없다.
- **⚠ 정본이 아니라 덱이라서 못 하는 판정**: "저쪽은 3D 를 안 한다"·"메시 수렴을 안 했다" 같은
  **부재 주장 금지**(`talks/README.md` §3). 덱에 안 나온 것뿐이다.
  단 **발표자가 스스로 인정한 한계**는 인용 가능: *"기계 시뮬레이션은 메시에 의존해서
  [대리모델] 성능이 잘 안 나온다"* (역학 R² 천장 ≈0.89 의 원인).
- **★ 우리 positioning 에 생긴 변화**: `positioning_vs_geodict.md` 의 스케일 사다리에
  **sub-particle 칸이 비어 있었다**는 것이 이 덱으로 드러났다. 우리 DEM 은 이 덱의 입자를
  **점 하나**로 보고, 이 덱은 우리 입자 하나를 **통째로 확대**한다 ⇒ **경쟁이 아니라 상하 맞물림.**
  `kang2025_toughened_bimodal_nca_lzo`(Voronoi 다결정 + cohesive-zone damage FEM, 우리-랩 정본)가
  이 축에서 **덱보다 상위 등급의 정본**이다 — 인용은 그쪽으로.
- **★ 종적 관측점 2개**: `kb/projects/ml_opportunities_from_lab_ppt_2026_07.md` (2026-07-27,
  **모델 315개**, 파라미터 **7개**, "추후 ML 예정") → 이 덱 (2026-08-18, **2500 생성 / 1911 성공**,
  파라미터 **5개**로 통합, **내부 기공 축 삭제**). **4주에 6.1배.** 랩 ML 파이프라인의 실제 속도.
- **➡ cascade(DFT 축) 로의 방법론 이전은 여기 적지 않는다** — 축이 다르므로 별도 카드:
  `kb/methodology/microstructure_ml_transfer_to_cascade_2026_08_25.md`.

## 🗨️ Q&A 로그
<!-- "Q&A 작성해줘" 트리거 시 직전 질문/답 누적 -->

<!-- ↓↓ 2026-08-19 병합: 다른 워크트리(tmp-litdb-58)에서 온 추가분 ↓↓ -->
- **★ Wang & Wang 2026 (`wang2026_dryprocess_thick_cathode_failure_ncm94`) — 건식 후막의 *두께* 는 주는데 *porosity* 는 안 준다 (Luan 과 같은 병).**
  건식 자립막(NCM94:LPSCl:VGCF:PTFE = 80:18:1:1, 6.5 mAh cm⁻²) 의 **미가압 두께 177.3 µm** 와
  **300 사이클 후 셀 안 두께 127.1 / 131.4 / 138.9 / 128.4 µm** (3.5/3.6/3.7/3.8 V) 를 SEM 으로 준다.
  - ✅ **가정 무관한 유일한 수치 = 두께 감소율 −21.7 … −28.3 %** (두 값 모두 stated SEM).
    ⚠ 단 이것은 **≈500 MPa 성형(우리 DERIVED, 4 t / Ø10 mm 가정) + 300 사이클** 의 **합**이라
    우리 MPM 압밀량과 1:1 대응이 아니다. "건식 자립막은 셀 조립에서 두께의 약 1/4 를 잃는다" 는
    **공정 규모 감각**까지만.
  - ⛔ **porosity·전극밀도·로딩(mg cm⁻²) 전부 미보고.** 우리가 유도하려면 (i) 비용량 200–207 mAh g⁻¹
    (ii) ρ_SE 1.64–2.0 (iii) 사이클후두께≈가압후두께 — **3-가정**이 필요하고 결과가 **ε ≈ 8.6–24.8 %** 로
    벌어진다(4셀 × 가정 폭; 중앙 ~15–18 %). **우리 SBE/DBE 7.9 % 의 앵커로 쓰지 말 것.**
  - ⚠ **사이클 후 두께가 컷오프 전압 순서를 안 따른다**(3.7 V 가 최대 138.9 µm). 산포 6.6 %p 는
    셀-간 편차 ≳ 전압효과 ⇒ 여기서 팽창/수축 추세를 읽으면 안 된다.
  - ★ **DERIVED(ours) SE/solid = 34–38 vol%** (ρ_SE 1.64–2.0) ⇒ **우리 46.7 % 보다 AM-rich**.
    두께는 **127–177 µm vs 우리 72.5 µm (1.8–2.4×)**. ⇒ 같은 계열이되 **더 두껍고 더 AM-rich** =
    수송 제한이 우리보다 강한 침대.
  - ★ **성형/운전 압력 원장 갱신**: 성형 **≈500 MPa**(우리 300), **운전 스택압 200 MPa (Li–In) / 110 MPa (LTO)**.
    ⚠⚠ **이 운전압은 우리 작동압 원장 최상단**이다 — Doux 5 (최적) · Lee2025 2 · Luan 30 · Minnmann 40 MPa.
    즉 **이 셀은 성형압에 가까운 상태로 계속 운전**되어 **저압 void 형성 영역을 아예 안 지난다.**
    본문의 *"100–200 MPa 는 성능에 악영향 없다"* 주장은 **인용 근거가 없다**(⚠ 미검증 주장).

- **★★ Weitze 2024 (`wet_processing_resolved_am_ssb_cathode_manufacturing`, SI 재판독 2026-08-19) — *실제 형상*을 넣고도 압밀 물리가 비어 있는 사례 + 우리가 없는 springback 앵커.**
  ASSB 습식(슬러리→건조→압연) DEM.  **SI 가 접촉 파라미터를 처음으로 열어줬다**(초판 digest 는 본문만 봤다).
  - ★★ **JKR 쌍-유효 영률 E = 135×10⁶ (SI 단위 → 우리 환산 **135 GPa**) 가 AM–AM · AM–SE · **SE–SE 에 똑같이** 걸린다.**
    실물 LPSCl 은 22–24 GPa, 우리 DEM 유효값은 **1.35 GPa** ⇒ **그들 SE 접촉은 실물의 ~6배, 우리 규약의 ~100배 뻣뻣**.
    본문에 **"plastic/plasticity" 가 0회**, 항복 캡 없음, **절대압(MPa) 판독 0회**.
  - ★ **DERIVED(ours)** Hertz 평균접촉압 p̄=(4/3π)E*√(δ/R): E*=135 GPa·R_eff=0.2425 µm 이면 **δ=10 nm 에서 p̄≈11.6 GPa**,
    항복 개시(p̄≈1.1σ_y, 우리 σ_y=0.15 GPa)에 대응하는 겹침은 **δ≈2 pm**.  ⇒ **그들 모델은 LPSCl 이 항복하기
    시작하는 지점조차 표현할 자유도가 없다.**  같은 산술을 우리 E_eff=1.35 GPa 에 하면 항복 개시가 **δ/R_eff≈8.3 %** 이고
    우리 **pure-SE 실측 ⟨δ⟩≈지름의 11 %**(Cronau 대조) ⇒ **δ/R_eff≈0.44 = 항복 개시의 5배** = 확실히 소성 영역
    ⇒ **18× 연화가 접촉을 소성 스케일에 올려놓는 장치**(frame[2]) 재확인.
  - ⚠ **porosity floor 29 % 를 강성으로 귀속하지 말 것.**  같은 SI 가 **CBD 쌍 E = 1–20 kPa**(초연질)로 주고
    그 CBD 가 ~10 vol% 를 차지한다 + **압력 축이 아예 없다**(압연도 0–0.45 만).  ⇒ Varkey(halide E 10.58 → 21/37 %)
    처럼 **E→floor 사다리에 그대로 얹을 수 없다**.  대비는 정성으로만.
  - ★★ **우리가 없는 정량 앵커 = springback.**  DERIVED(ours, 고체부피 보존 + Fig 6 digitized 10점
    0.578/0.559/0.539/0.517/0.492/0.464/0.428/0.390/0.341/**0.291**): 탄성회복 = **압축량의 10–15 %**
    (압연도 0.1 에서 15 % → 0.45 에서 10 %), 압연도 0.45 에서 relaxed 두께 **≈23.8–24.6 µm**(초기 40, 눌림 22)
    — **Fig 5 의 45 % 곡선 종단 ≈24 µm 와 자기일관** ✓.  Sangrós 2019 LIB 점탄성 회복 ~17 % 와 같은 자릿수.
    ⇒ **우리 MPM 제하(unload) 검증 타깃**(우리 DEM=hold, MPM=hold/servo 라 회복을 산출로 안 낸다).
  - ⚠ **압밀곡선 모양이 가속형**(고압연에서 더 가파름) = 실제 분체 압밀의 **감속형(Heckel)과 반대**.
    우리 해석: 소성이 없어 저하중에서 안 눌리고, 고하중에서 roll 이 기하로 밀어넣는 서명.  **Heckel 과 겹치기 금지**(x축이 압력이 아님).

- **★★ Wang & Wang 2026 (`wang2026_dryprocess_thick_cathode_failure_ncm94`) — σ 는 하나도 안 주지만, DRT 가 *우리 접촉망 항을 이름으로 분리*해 준다.**
  - ⛔ **먼저 정직하게 못 주는 것부터**: **복합체 σ_e·σ_ion 실측 0건** (DC 분극·4-probe·블로킹셀·TLM 전부 없음).
    ⇒ **우리 모델 SBE σ_e 73 mS cm⁻¹ (PTFE 미차단) / 54.6 (PTFE 차단) 을 이 논문으로 검증도 반박도 못 한다.**
    현행 앵커 밴드(**Lee 2025 34 @VGCF 3 + PTFE 0.5 · Kim 2024 38.6–65.2**)는 **그대로 유지**.
    **PTFE 함량 스윕도 없다**(1 wt% 한 점) ⇒ **Lee 2025 SI Fig 5 가 여전히 유일한 PTFE↔σ 곡선**이다.
    그들 레시피는 **VGCF 1 wt%(우리·Lee 의 1/3) + PTFE 1 wt%** 라 설령 쟀더라도 우리 값과 직접
    비교가 불가능했을 것이다. ⚠ Lee 곡선을 1 wt% 로 로그보간(≈12 mS cm⁻¹)해 그들 값을 추정하는 것은
    **두 논문을 가로지르는 검증 불가 외삽** — 수치로 쓰지 말 것.
  - ⛔ **집전체 계면저항도 분리 안 됨** (R_s 에 섞임) ⇒ 우리 `R_collector` 12–110 Ω cm² 시나리오와 대조 불가.
    그 축의 정본은 계속 `nam2026_primer_layer_dry_electrode_collector`.
  - ★ **DERIVED(ours) 분리막 σ_ion ≈ 4.3–5.4 mS cm⁻¹** — R_s = 9.4 Ω cm² (1st) · 60 mg 펠릿 · Ø10 mm 다이 ·
    ρ_pellet 1.5–1.9 g cm⁻³ **ASSUMED** ⇒ t ≈ 400–510 µm, σ = t/R_s.
    ⚠⚠ **우리 bulk LPSCl 앵커 사다리에 같은 줄로 올리지 말 것** — 그들 SE 는 **Li₅.₄PS₄.₄Cl₁.₆ (Cl-rich)**
    이고 우리·Cronau(3.0 단결정)·Lee2025(2.19 펠릿)·Minnmann/Kim(1.6)·Bazzoun(1.02)은
    **Li₆PS₅Cl** 이다. **"Cl-rich 계열이 더 빠르다"는 방향 정합**으로만 기록.
  - ★★★ **진짜 소득 = DRT τ-축 귀속 (Table S2, stated)**:
    | 피크 | τ (s) | 그들 귀속 | 우리 대응 |
    |---|---|---|---|
    | **D1** | **10⁻⁶–10⁻⁵** | **양극 입자 간 고체–고체 접촉저항** | ★★ **우리 Kirchhoff/Holm R = 1/(2σ r_c) 접촉망 항 그 자체** |
    | **D2** | 10⁻⁵–10⁻² | 양극 **계면상(interphase)** 내 이온수송 | 우리 STEP3 σ_ion + (우리에겐 없는) CEI |
    | **D3·D4** | 10⁻²–10⁰ | 양극 표면 **전하이동** | 우리 STEP4 Butler–Volmer i₀ |
    **한 사이클(SOC 8+7 점) 동안 D1 은 안정하고 D2·D3·D4 만 움직인다** (Fig 5c·e, stated).
    ⇒ **"정적 접촉망 위에서 σ 를 풀고 열화는 그 위 화학층으로 얹는다"** 는 우리 아키텍처의 실험 지지.
    ⚠ **적용 창은 *한 사이클*이다** — 50 사이클 축(Table S1)에서는 **R_ct2 가 83.8 → 939.7 Ω cm² = ×11.2**.
    "300 사이클 동안 접촉망 불변"으로 확대하면 **틀린다**.
  - ★ **R(N) 3항 실측 (Table S1, 0.1C, 2–3.5 V, 200 MPa)** — 우리 `rint_eis_anchors.csv` 두 번째 앵커 후보:
    | | 1st | 10th | 20th | 30th | 40th | 50th | (ours) × |
    |---|---|---|---|---|---|---|---|
    | R_s | 9.4 | 8.6 | 8.5 | 8.9 | 8.6 | 8.6 | ×0.92 |
    | R_ct1 (Li–In) | 12.5 | 36.1 | 36.5 | 29.4 | 42.7 | **55.4** | **×4.43** |
    | R_ct2 (양극) | 83.8 | 108.0 | 134.1 | 218.7 | 307.1 | **939.7** | **×11.2** |
    (ours) 양극 ASR 분담 **79.3 % → 93.6 %**; 10-사이클 배수 1.29→1.24→1.63→1.40→**3.06** = **가속·초선형**,
    단일 멱함수 불가(국소 지수 0.75 → 1.35). ⚠ 점 6개·오차막대 없음 → **지수는 지시값**.
    ⚠⚠ **논문 본문의 *"R_s·R_ct1 변화 미미"* 는 자기 표와 모순** — R_ct1 은 **4.4×** 다.
    **R_s 만 진짜 안정**. 인용 시 반드시 교정.
  - ★ **자기일관성 교차검증(ours)**: Fig 2d 분극 기저 **≈0.05 V** @0.1C(= 0.65 mA cm⁻², ours 유도) ⇒
    ASR ≈ **77 Ω cm²** — Table S1 1st R_ct2 = 83.8 과 잘 맞는다. ⚠ "분극 과전압"의 정의(η vs ΔV)가
    미공개라 38–77 Ω cm² 로 2× 갈린다 → **인용 금지, 정합 확인용**.
  - ⚠⚠ **GITT D_Li 절대값 인용 금지** — 그들 log D ≈ **−7.4 … −7.9 (cm² s⁻¹)** 는 우리 앵커
    (`docs/ncm_sc_poly_electrochem_anchors.md`: SC 1.5e-15–1e-14 · poly 4e-15–3e-14 m² s⁻¹) 보다
    **100–1000× 크다**. **특성면적 규약 미공개** (ours 가설: 기하 전극면적 사용 → D ∝ S⁻² 과대).
    쓸 수 있는 것은 **"H2→H3 구간에서 D 가 떨어진다"는 같은 셀 안의 상대 추세**뿐.

- **★★ Weitze 2024 — 무차원 σ 를 *형성인자*로 읽으면 우리·Bazzoun 과 한 표에 앉는다 (2026-08-19 재판독의 최대 소득).**
  그들 GeoDict 값은 **이온=SE 벌크, 전자=CBD 벌크를 1.0 으로 정규화**한 것이라 **정의상 F = σ_eff/σ_bulk = φ/τ 인 순수 기하량**이다
  (SE 만 이온 전도 + 선형 문제 ⇒ 그들이 어떤 절대 σ 를 넣었든 F 는 불변).  ⇒ **"무차원이라 비교 불가" 는 반만 맞다.**

  | 출처 | F = σ_eff/σ_bulk | **N_M = 1/F** | 조건 |
  |---|---|---|---|
  | **Weitze 2024** (digitized Fig 8) | **0.0135** | **74** | 압연 45 %, porosity 0.291, φ_SE≈0.18, **압력 미보고** |
  | **Bazzoun 2026 실험** (stated) | **0.134** (=0.137/1.02) | **7.5** | f_CAM 70 wt%, **400 MPa**, full-blocking EIS |
  | **우리 STEP3 SBE** | **0.052 / 0.131 / 0.166** | **19 / 7.6 / 6.0** | vox 0.4/0.3/0.25 µm (**격자 미수렴**, SR-01) |

  - ★★ **그들은 실험의 1/10 이다** — 이 문장만이 규약에 둔감하게 강건하다.  ⚠ 우리 F 는 σ_bulk 기준을 **3.0(단결정)**
    으로 잡은 값이라 Bazzoun 의 **펠릿 1.02** 기준과 규약이 다르다(펠릿 기준이면 우리 F 는 3배) — CLAUDE.md 가
    이미 표시한 **σ_grain 이중계산** 자리다.  우리↔Bazzoun 비교에는 반드시 기준을 붙일 것.
  - ★★★ **원인은 조성이 아니라 연결성이다.**  그들 **SE/solid ≈ 0.18/0.65 = 28 %** 로 **우리 real_14 의 26–27 % 와 거의 같고**,
    φ_SE(전체 기준)도 0.18 vs 우리 0.23 으로 비슷하다.  거의 같은 SE 함량에서 **형성인자만 한 자릿수 낮다**
    ⇒ 차이는 **접촉망 연결성(=압밀 물리)**.  우리 압밀 물리 우위의 **가장 깔끔한 정량 근거**.
  - ★★ **DERIVED(ours) τ_SE = φ_SE/F**: 압연 5 % 에서 **≈375**, 45 % 에서 **≈13** (Bazzoun 실험 ≈4.0; Bruggeman τ=φ^-0.5
    는 φ=0.18 에서 2.4 → F_B=0.076 ⇒ 그들은 유효매질보다 **5.6배**, 저압연에서는 **145배** 나쁘다).
    **φ_SE≈0.15–0.18 은 문헌 이온-percolation 문턱 φ_SE≳25 %(Bielefeld 2019, Famprikis 리뷰 경유) 아래**
    ⇒ 그들의 "압연하면 σ_ion 34배" 는 **문턱을 향해 기어오르는 곡선**이지 문턱 위 운전 영역의 치밀화 응답이 아니다.
    ★ 이것은 우리 **G4 가드**(Stage 22.5 를 φ_AM<0.3 에서 외삽 금지 — 멱함수는 문턱 붕괴를 못 그린다)와
    **같은 물리를 다른 상에서** 본 사례다. 문헌 근거로 인용 가치.
  - ⛔ **전자 축은 밴드에 못 앉힌다**: σ_e = 1.13×10⁻³ × σ_CBD,bulk 인데 **σ_CBD,bulk 가 논문·SI 어디에도 없다(n/a)**.
    역산하면 우리 밴드(Lee 34 · Kim 38.6–65.2 · 우리 SBE **73** PTFE 미차단 / **54.6** 차단)에 앉으려면
    **σ_CBD ≈ 30–65 S/cm** 여야 하고 그 값 자체는 우리 탄소 규약(100 S/cm, CL-47 분말 83)과 같은 자릿수지만,
    **가정 위의 숫자다** ⇒ 원고에 "그들 σ_e 는 우리 밴드 안" 이라고 **쓰지 말 것**.
  - ⚠ **방법 수준 vs 결과 수준을 섞지 말 것** (초판 digest 의 정정): 접촉·계면 저항 항이 없다는 것은 *방법* 상한 논거이고,
    *결과* 는 실험보다 10배 낮다.  게다가 **GeoDict voxel 크기를 보고하지 않아** 목(neck) 기하가 감사 불가다 —
    우리 자신이 CL-25 로 그 노브가 σ 를 크게 흔든다는 것을 **실측**했다는 점이 진짜 방법론적 우위.

- **★★★ Wang & Wang 2026 (`wang2026_dryprocess_thick_cathode_failure_ncm94`) — 이 축에 세 가지를 준다: 실측 복합막 E · in-situ 압력 · "SEM 아래의 파손".**

  **(C-1) ★★ AFM 로 잰 건식 복합막 Young's modulus = 1.263 / 2.248 / 3.056 GPa (Fig S3, stated)**
  논문이 *"good local mechanical integrity"* 한 줄로 흘려보낸 값인데, 우리에겐 **frame[2] 서사의
  첫 같은-공정 실측 밴드**다. E 사다리가 이렇게 채워진다:
  **LPSCl 결정 22–24 (우리 relaxed-ion E_VRH 22.06 · Bazzoun 22.1) → thiophosphate 유리 실측 ≈20 →
  건식 *복합 다공막* 실측 1.3–3.1 GPa** ⇒ **형태만으로 한 자릿수 하락.**
  우리 **E_eff 1.35 (DEM) / 1.53 (MPM champion)** 이 그 밴드 안에 놓인다.
  ⚠⚠ **같은 물리량이 아니다 — 이 구분을 카드·원고·발표에서 반드시 유지할 것**:
  | | 우리 E_eff | 그들 AFM E |
  |---|---|---|
  | 대상 | **SE 입자 하나의 접촉/구성 강성** | **복합막 표면의 압입 응답** |
  | 포함 | granular 재배열·GB slide·micro-fracture 를 **럼핑** | NCM+SE+PTFE+**공극** 국소 혼합 |
  | 방법 | 실험 porosity 에 맞춘 역산 | 힘–거리 + **미공개 접촉모델** |
  | 산포 | — | **3점에 2.4×** |
  ⛔ **금지 문장**: "우리 1.35 GPa 가 실측 2.19 GPa 와 일치한다."
  ✅ **허용 문장**: "건식 황화물 복합막의 µm-스케일 유효 모듈러스는 **실측으로 1.3–3.1 GPa** 이며
  LPSCl 단결정보다 **한 자릿수 낮다**. 우리 연화 E_eff 는 물성이 아니라 프록시지만 **그 프록시가
  놓인 자리는 실측 가능한 복합막 강성 밴드 안**이다." ⇒ *"18× 연화가 자의적"* 비판에 대한 **최선의 방어선**.

  **(C-2) ★★ in-situ 스택압 궤적 — SC 양극은 충전에 *수축*한다 (Fig 6, 110 MPa, LTO zero-strain 대극)**
  | 양 | 값 | 출처 |
  |---|---|---|
  | 충전 중 급강하 | **≈ 2 MPa** | stated |
  | 시작 → 충전1 최소 | **107.60 → 105.65 MPa (−1.95, 1.81 %)** | digitized |
  | 방전1 후 회복 | ≈106.45–106.6 (**미복귀**) | digitized |
  | 충전2 최소 | **105.35 MPa** | digitized |
  | **바닥 래칫** | **−0.30 MPa / cycle** | ours |
  | 2 사이클 누적 비가역 | **1.29 MPa = 1.20 %** | ours |
  | 가역 진폭 축소 | 1.95 → 1.37 MPa | ours |
  ★ **부호가 우리 A10 `cycle_contact_ledger.py --poly-mode` 분기를 지지한다**:
  이 양극은 **SC(단결정) 단독** NCM94 이고 **충전 = 압력 감소 = 수축** 이다 ⇒ **SC = 수축 → 계면 debond**
  (Parks 의 poly **+19 % 팽창**과 부호 반대 = 우리가 `expand-void`/`shrink-proxy` 를 갈라 놓은 근거 정합).
  ⚠ **유보 3**: ① **스택 강성 미공개 → ΔP 를 Δ부피로 못 옮긴다** ("2 MPa = X % 수축" 금지)
  ② 조립압 110 → 측정 시작 **107.6 = 이미 2.4 MPa 완화**돼 있고, 초기 12 h 의 완만한 하강은
  **점탄성 크리프와 구별되지 않는다**(휴지-only 대조군 없음) — 그들이 이를 "가역 구조변화"라 귀속한 것은 미검증
  ③ LTO 의 zero-strain 성도 이 논문에서 확인하지 않았다(문헌 상식 가정).

  **(C-3) ★★ "SEM 은 멀쩡한데 압력은 안 돌아오고 저항은 11배" = 우리 CZM 의 존재 증명**
  같은 셀에서 사후 SEM(Fig S9–S16)은 **박리·크랙·구조손상 없음**이라 하고, in-situ 압력은
  **1.20 % 비가역 손실**, EIS 는 **R_ct2 83.8 → 939.7 Ω cm²** 를 준다.
  ⇒ **파손이 SEM 조사 해상도 아래에 있다.** 우리 접촉원장/CZM(Bucci G_c 2.8±1.8 J m⁻²)이 다루는
  스케일이 정확히 거기이고, 이 논문은 그 스케일의 존재를 **세 독립 관측의 불일치로** 증명한다.
  ⚠ 그러나 그들은 **G_c·K_IC·균열밀도를 하나도 안 쟀다** ⇒ **우리 CZM 파라미터 보정에는 못 쓴다.**
  이것은 *"표적이 실재한다"* 는 증거이지 *"표적의 값"* 이 아니다.

- **★★ Weitze 2024 — *형상까지 넣은* 논문이 "계면이 안 자란다"를 자인한다 + 우리 coverage 두 밴드의 외부 대조점.**
  - **자인 문장(정확히)**: Fig 7 논의 — *"once contact has been established between two or more spheres, no matter how much
    the microstructure is compressed, two phases will not be able to increase their contact area, **since we do not allow for
    much overlap between the different spheres during the calendering stage in the first place**"*; 결론 — *"we were unable to
    observe an increase in interfacial area between different materials on account of their **spherical and rigid** nature …
    considered as a limitation of the model"*; 그리고 σ 논의 — *"**we would expect even higher values for larger interfacial
    areas between materials**"*.  ⇒ **소성 계면성장의 부재가 σ 를 아래로 끌어내린다는 것을 저자가 안다.**
  - ★ **DERIVED(ours) — 그들 AM 표면의 SE 피복률**: Fig 7 digitized 로 A(AM–SE)/[A(AM–SE)+A(AM–CBD)+A(AM–Pore)]
    = 1.08/(1.08+0.72+5.70) = **14.4 %** (압연 5 %) → 1.25/(1.25+0.68+4.05) = **20.9 %** (45 %).
    ⇒ 우리 **Hertz coverage 16–18 %** · **MPM 기하 ground-truth 16 %(gap≤0)** 와 **같은 밴드**,
    우리 **Tabor 소성-확산 coverage 48–52 %** 와는 **다른 밴드**.  ★ "탄성-접촉 피복 vs 소성-확산 피복" 두 밴드를
    가르는 **외부 대조점**이 생겼다 (⚠ 그들 porosity 30–57 % vs 우리 15.6 % — 밀도가 크게 다르다).
  - ⚠ **초판 digest 정정**: AM–SE 는 "거의 일정" 이 아니라 **1.08 → 1.25 (+16 %)** 로 **유일하게 오르는 상-상 계면**이다
    (CBD–SE 1.95→1.82, CBD–AM 0.72→0.68 은 평/하락).  다만 상승분의 대부분은 **AM–Pore 감소의 반사**이지
    접촉면적 성장이 아니다(저자 진단과 일치).
  - ⚠ **논문 자체의 설명 오류 1건(우리 판단)**: 저자는 Fig 7 의 서열(SE–Pore 11.5 ≫ AM–Pore 5.7)을 *"SE has the highest
    volume"* 으로 설명하는데, **자기 Fig 5 가 φ_AM(0.27–0.35) > φ_SE(0.15–0.18)** 을 보여준다.  올바른 이유는
    **비표면적**(S/V=6/d; Ø1.0 SE vs Ø4.5 AM) — φ×6/d 로 계산하면 SE:AM ≈ 2.5 로 관측 2.0 과 정합.
    ⇒ 결과 수치는 무영향, **설명만 틀렸다**.  인용 시 이유를 바꿔 쓸 것.

- **⛔ Wang & Wang 2026 (`wang2026_dryprocess_thick_cathode_failure_ncm94`) — 이 축에 *아무 것도* 주지 않는다 (정직 기록).**
  CAM 이 **NCM94 단결정 2–4 µm 단일 모드**이고 입도·PSD 스윕이 없다. packing 지표(배위수·접촉면적·
  tortuosity·porosity) 전부 미측정. ⇒ **dip·Furnas·bimodal 축 기여 0.** 같은 건식·황화물 계열이라도
  **D 축에서는 인용할 것이 없다**는 것을 명시해 둔다(나중에 "건식 논문이니 여기도 쓰겠지" 하고 찾지 않도록).

- **★ Wang & Wang 2026 (`wang2026_dryprocess_thick_cathode_failure_ncm94`) — 우리가 *그들에게* 해 준 검산 2건 + 우리 가정의 유효창 1건.**
  - ★ **(검산 1) 그들 데이터의 내부 자기일관성**: Fig 2d 분극 기저 **≈0.05 V** (digitized) 를 0.1C
    (= **0.65 mA cm⁻²**, ours 유도) 로 나누면 ASR ≈ **77 Ω cm²** 이고, 이는 Table S1 1st cycle
    **R_ct2 = 83.8 Ω cm²** 와 맞는다. 논문은 두 그림을 연결하지 않는다 — **우리가 이은 것**.
    ⚠ "분극 과전압"의 정의(η vs 히스테리시스 ΔV)가 미공개라 38–77 Ω cm² 로 2× 갈린다 → 정합 확인용.
  - ★ **(검산 2) 양극이 ASR 을 지배한다는 것의 정량화**: Table S1 세 항을 더하면 총 ASR 이
    **105.7 → 1003.7 Ω cm² (×9.5)** 이고 **양극 분담이 79.3 % → 93.6 %** 로 커진다 (ours 유도, 논문 미제시).
    ⇒ 우리 STEP4/R_int 가 *"양극 계면이 지배한다"* 를 **가정**으로 쓰는 것의 **실험 근거**.
    같은 계산이 **논문 본문의 오류도 잡는다** — *"R_ct1 변화 미미"* 는 **4.4×** 로 틀렸고, 안정한 것은 R_s 뿐이다.
  - ★ **(유효창) 정적 접촉망 가정의 실험적 경계**: DRT D1(= 우리 Holm 접촉망 항)이 **한 사이클 내내 안정**
    하다는 관측은, 우리 네트워크 솔버가 **정적 구조 위에서 σ 를 푸는 것**의 **유효 시간창을 실험으로 그어 준다**
    ("SOC 스윕 안에서는 접촉망을 고정해도 된다"). ⚠ 그 창은 **50 사이클 축에서 깨진다**(R_ct2 ×11.2).

- **★ Wang & Wang 2026 (`wang2026_dryprocess_thick_cathode_failure_ncm94`) — 우리 모델에 *없는 축* 5개를 이름으로 드러낸다.**
  1. ★★ **시간구동(캘린더) 열화** — **모든 컷오프에서 0.1C 가 0.5C 보다 빨리 죽는다**
     (3.5 V: 50 cyc 후 **87.1 % vs 98.3 %**; 3.8 V: **77.5 % vs 91.7 %**). (ours) 시간 환산
     0.1C 50 cyc ≈ **1000 h** vs 0.5C ≈ **200 h** (5×) ⇒ 페이드는 1.7–2.7× = **시간과 상관은 분명하나 선형 이하**.
     우리 STEP5/열화·`rint_cycle_traj.py` 는 **전부 사이클 인덱스**이고 **시간 항이 없다.**
     ⇒ **백로그 1순위 후보** (사이클수만으로 열화를 매기면 저율 셀을 낙관 예측한다).
     ⚠ 그들의 두 번째 해석(**고율의 순간응력이 계면을 "self-healing" 재구성**)은 **증거 0의 사변**이다 —
     같은 데이터가 "저율은 시간이 길어 부반응이 더 진행" 하나만으로 설명된다. 채택 금지.
  2. **CEI / 계면상 그 자체** — DRT D2(계면상 내 이온수송)가 커지는데 우리 상(phase) 목록
     (AM · SE · VGCF · PTFE · SDCP · pore) 에는 **계면상이 없다**.
  3. **화학 분해종의 저항 기여** — 사이클 후 XPS 가 **P=O · Li₂S · SO₃²⁻ · SO₄²⁻ · Sₓ²⁻** 를 보이고
     **컷오프가 높을수록 종이 늘어난다**(3.5 V 2종 → 3.8 V 4종, Sₓ²⁻ 는 3.8 V 에서만).
     우리는 이 절연/고저항 상을 **그리지 않는다**. ⚠ 그들도 **정량(원자%·층두께) 은 안 준다** → 상 부피 배정 불가.
  4. **AM 벌크 열화** — **I(003)/I(104) 1.99 → 1.72 / 1.68 / 1.53 / 1.40** (300 cyc, 컷오프 단조).
     우리 AM 은 전기화학적으로 **균질·불변**이다.
  5. **작동압 영역 자체** — 우리 침대는 300 MPa 성형 상태로 **고정**이고 **압력 해제/재가압 경로가 없다**.
     그들은 **200 MPa (Li–In) / 110 MPa (LTO)** 에서 운전하며 **사이클 중 압력이 1.2 % 비가역 감소**한다.
  ⚠ **이 논문으로 못 채우는 우리 축(정직 표기)**: **복합체 σ_e·σ_ion 실측 0** · **PTFE 함량 스윕 0** ·
  **집전체 계면 분리 0** · porosity/로딩/다압력/Heckel 0 · packing·bimodal 0 · G_c/K_IC 0 · 시뮬 0.

- **★ Weitze 2024 (2026-08-19 SI 재판독) — 우리가 *원리적으로* 못 하는 3칸이 다시 확인됐다.**
  - **① 비구형 AM 형상**: LIGGGHTS `multisphere` 로 가능은 하나 production 에 없다.  ⚠ **단 사정거리를 좁혀야 한다** —
    그들의 resolved 는 **AM 한 상뿐**이고, **SE 는 nano-CT 가 SE/CBD/carbon 을 구별 못 해 원리적으로 resolved 불가**
    (저자 명시)라 **단분산 Ø1.0 µm 완전 구**다.  ⇒ ASSB 이온수송의 주역 상에서 그들의 형상 우위는 **적용되지 않는다**.
    우리가 뒤진 칸은 *패킹·기하 사실성*이지 *이온 수송*이 아니다.
  - **② springback / 제하 탄성회복**: 그들은 roll 을 등속 후퇴시켜 회복을 낸다.  우리는 산출로 안 낸다.
    ⇒ **흡수 가치 실재** — 위 §A 의 DERIVED 10–15 % 를 MPM unload 검증 타깃으로.
  - **③ 슬러리·용매·건조 + nano-CT→segmentation→입자추출 자산**: 원천 없음(우리는 건식 지향이라 경로가 다르다).
  - ⚠ **"실험 앵커" 축은 정직하게 동급인 부분이 있다**: 그들의 실험 2점(밀도 1.353±0.001, 건조 porosity 0.53±0.03)은
    **둘 다 보정 타깃으로 소비**돼 held-out 이 0 이고 압연 단계는 앵커가 아예 없다(저자 자인) — 우리가 앞선다.
    그러나 **우리 E_eff=1.35 GPa 도 porosity 보정값**이라 *보정-앵커 축 자체*는 동급이고,
    우리 우위는 **남겨둔 앵커의 수**(Cronau overlap · Bazzoun σ · SEM · Lee/Kim σ_e 밴드 · DEM↔MPM frame[4])에 있다.


---

- **★★ Zhang 2026 (`zhang2026_dryprocess_electrode_architecture_cell_level`, *Nature Energy*) —
  우리 DEM 압밀에 *원리적으로 없는* 자유도 = 전단(shear).  그리고 그들에게도 없는 것 6.**
  ⚠ 액체계 LIB (**FORM/METHOD-ONLY**) — 아래는 전부 *공정 축*의 형태 논의이고 절대값 전이가 아니다.
  - **그들이 하는 것 3단**: ① 실험 = **100 °C · 10 min · 전단응력 1–5 MPa** 건식혼합 → PTFE **피브릴화** →
    VGCF 와 얽힘 ② CGMD = **LAMMPS, Martini-3 유래 LJ 12-6 + 조화 결합/각**, 373.15 K,
    **±x/±y/±z 교대 방향력 ~5 MPa × 12 ns × 30 사이클**, 박스 **1.5³ µm³**, **VGCF 10 사슬(30 비드, R 50 nm)
    + PTFE 500 사슬(70 비드, R 14 nm, L 1,035 nm)** ③ 화학 = 전단이 VGCF 표면 –OH 를 **C=O 로 변태**
    (XPS O1s **533 → 531 eV**; –OH **43.1 → 8.0 %**, C=O **≈0 → 55.3 %**; Raman **I_D/I_G 0.10 → 0.20**).
    결과: RDF 피크 **8.7 → 11.8** (r ≈ 60 nm) · **RoG 60 → 45 nm**(≈ 섬유반경 50) · **섬유간거리 360 → 250 nm**.
  - ★★ **우리에게 없는 것 — 5칸, 정확히**:
    **①** 혼합/전단 단계 자체가 없다 (우리는 **무작위 삽입 → 정착 → 일축 압밀 300 MPa**; 전단 이력 0 스텝).
    **②** 첨가제가 **동역학 객체가 아니다** — VGCF/PTFE/SDCP 는 DEM 입자가 아니라 MPM 복셀에 **사후 seeding**
    (`seed_sdcp` · `seed_sheath` · `--fibre`) ⇒ 그들 것은 움직이고 감기고 끌어당기는데, 우리 것은 찍힌 자리에 영원히 있다.
    **③** **바인더–탄소 결합에너지가 없다** — 우리 PTFE 는 절연 차단상(`sigma_ptfe` 기본 0)이고 VGCF 와 인력 0.
    그들은 **ε(VGCF–PTFE) > ε(PTFE–PTFE)** 로 감김을 만든다.
    **④** **섬유 굽힘·감김 자유도가 없다** — 우리 VGCF 는 **직선 선분 스탬프**(폴리라인).
    **⑤** **온도가 없다** — 우리 DEM 은 **비열적 granular dynamics**, 그들은 373.15 K 서모스탯 MD.
  - ⚠ **그들 전단 모델에도 없는 것 6 (대칭적 정직)**:
    **(a) 박스에 NMC 가 아예 없다** (2성분 VGCF+PTFE 박스) ⇒ 실제 전단이 일어나는 *AM 사이 좁은 틈*의 구속을 안 본다.
    **(b) 압밀/캘린더링이 CGMD 밖**이다 (최종 도전망을 정하는 단계가 모델 밖).
    **(c) 전도도를 안 낸다** ⇒ "전단 → 도전망 → σ_e" 의 마지막 화살표가 **정성**이다.
    **(d) force field 수치가 하나도 없다** (ε·σ·r_c·k_bond·k_angle 전부 미보고) ⇒ **재현 불가**.
    ⚠ 같은 그룹 Alabdali 2023 은 **SI Table S1 로 FF 전문을 공개**했다 — **명백한 퇴보**.
    **(e) 시드·반복·오차막대 0**, 그리고 **Fig 3f 가 수렴하지 않았다**(섬유간거리가 ~660 ns 끝까지 단조 하강, 평탄역 없음)
    ⇒ "~250 nm" 는 평형값이 아니라 **스냅샷**.  (프로토콜 합 **445 ns** vs 그림 x축 **~660 ns** 불일치도 미해소.)
    **(f) 기하가 전극과 어긋난다** (`DERIVED, ours`, 자릿수 논증):
    · **PTFE : VGCF 부피비**가 박스에서 **2.7–3.4 : 1** 인데 실제 전극(탄소:바인더 5:2 질량)은 **0.36 : 1**
      ⇒ **섬유 1개당 바인더가 실제의 약 7.4–9.4배** ⇒ 감김/코팅 정도는 **상한(upper bound)**.
    · **섬유 aspect** — 30 비드 × R 50 nm 를 **1.5 µm 박스**에 넣으면 최대 aspect **≈ 15**, 실물 **>200 의 1/13**.
      (비드가 접하면 길이 3.0 µm > 박스라 **기하 자체가 모순**이거나 섬유가 주기경계를 관통해야 한다.)
      percolation 은 aspect 에 극도로 민감한 양이므로 **이 축소는 결론의 방향까지 바꿀 수 있다**.
  - ⇒ ★★ **원고용 정확한 문장**:
    > *"Dry-processing 문헌은 전단이 도전망을 만든다고 본다 (Zhang 2026, Nat. Energy).  그 축은 우리 DEM 압밀
    > 파이프라인에 원리적으로 없다 — 우리는 전단 이력 없이 일축 압밀만 하고, 탄소·바인더는 동역학 객체가 아니라
    > 사후 seeding 된다.  다만 그 문헌의 전단 모델 자체도 활물질·압밀·전도도를 포함하지 않는 2성분 박스이므로,
    > **현재 어느 모델도 '전단 → 도전망 → σ_e' 를 하나의 사슬로 잇지 못한다.**"*
  - ★ **저비용 흡수 후보 (신규 코드 거의 불필요)**: 우리가 못 하는 것은 *전단 동역학*이지 *전단의 결과*가 아니다.
    **"바인더가 섬유 주변에 편재한다"** 는 결과 상태는 우리 **`seed_sheath`**(A14 SWCNT sheath 배선)로 **이미 표현 가능**하다.
    ⇒ **VGCF 주변 PTFE 편재를 켜고 σ_e 감도를 재는 프로브**가 즉시 가능.
    ⚠ **앵커 없음 → 스윕 전용, 생산 규약 아님 (§F1).**
  - ★ **새로 드러난 우리 공백 2건 (이 논문이 아니었으면 몰랐다)**:
    **① "균일도" 를 진단 지표로 쓰는 것이 부적절할 수 있다** — 이 논문은 **두께방향 CBD 균일도가 같아도
    (오히려 건식이 나쁨: std 1.15 vs 1.00 %) 연결성이 3.6배 다를 수 있다**는 것을 실측했다.
    우리 **A7 graded-z(`--poro-grad`)** 진단은 프로파일 균일성을 본다 ⇒ **"최대 연결성분 분율"이 지표 목록에 빠져 있다.**
    **② 도전재의 *비표면적* 축이 우리 모델에 없다** — 그들 설계원리 2 = *"탄소 비표면적을 최소화해
    탄소–전해질 접촉을 줄인다"*(VGCF **BET 18.6 m² g⁻¹**, MWCNT 200–450 의 1/10~1/24).
    우리 σ_e 모델(STEP3 · Stage 22.5)은 **부피/연결성만** 본다.  ⇒ 우리 백로그 **#30 (carbon–SE 면적 → SE 분해)**
    가 이미 그 자리를 잡아 두었고, **이 논문이 그 훅에 외부 정당화를 준다** (⚠ 소재계는 다름).
  - ★ **셀-레벨 설계대 대조 (DERIVED, ours)**: ρ_NMC 4.8(★ 그들 Sup Table 7 의 Capacity 식이 스스로 쓴 값)·
    ρ_VGCF 2.0 · ρ_PTFE 2.2 · ε = 30 %(그들 목표) 로 환산 ⇒
    **99 wt% · 30 mg cm⁻² 건식막 ≈ 91.4 µm · 3.32 g cm⁻³** (93 wt% 는 **105.0 µm · 3.07**).
    우리 **6 mAh 트랙 111–116 µm** 와 **같은 체급**이다 ⇒ *"우리 후막 트랙은 최전선 LIB 건식 전극과 같은 설계대"*
    라고 **말할 수 있다**.  ⚠ 단 **불활성 비율은 비교 불가**(그들 "불활성"에 SE 가 없다; 우리 SE 18 wt% 는
    불활성이 아니라 **이온 경로**) · **에너지밀도도 비교 불가**(그들은 **material-level 868 Wh kg⁻¹** 만,
    **셀-레벨 Wh kg⁻¹·Wh L⁻¹ 은 0개** — 제목이 "cell level" 인데도).
    셀-레벨 수치는 `luan2025_graded_cathode_400whkg_pouch`(404 Wh kg⁻¹ ASSB 파우치)에서 인용할 것.
  - ★★ **⑩ 2026-08-11 VGCF/PTFE 계획서와의 관계 — 이 논문은 그 계획서의 *원전*이다** (카드가 늦게 만들어졌다).
    정본: `docs/plan_vgcf_ptfe_coupling_20260811.md` + `docs/reviews/codex_review_request_vgcf_ptfe_plan_20260811.md`.
    카드 §14 가 그 계획서의 열린 질문(Q-B1~B3 · Q1~Q5)에 **원문 대조로** 답한다.  요약:
    · **인용값 13행 전부 원문과 일치** ⇒ 계획서의 결정은 **잘못 옮겨 적은 값 때문에 흔들리지 않는다**.
    · **P3(PTFE 매개 VGCF 배치상관) DROP 유지 — 원문이 근거 3개를 더 준다**:
      (6-a) CGMD 박스의 **PTFE:VGCF 가 실제 전극의 7.4–9.4배** ⇒ −31 % 는 **상한**
      (6-b) **Fig 3f 미수렴**(~660 ns 까지 단조 하강, 평탄역 없음) + 프로토콜 합 445 ns ↔ 그림 660 ns **불일치**
            ⇒ 250 nm 는 **평형값이 아니라 스냅샷**
      (6-c) 모델 섬유 **aspect ≈ 15–30** (실물 >200 의 1/13), 그리고 30 비드×R50 nm 는 1.5 µm 박스와 **기하가 모순**
      ⇒ 계획서의 *"방향만 남는다"* 에 **"그 방향조차 바인더 과잉·미수렴·aspect 축소 위에서 잰 것"** 을 덧붙인다.
    · **Q2(VGCF 기본등급) 유지** — ★ 새 논거: **논문 자신의 CGMD 도 AR>200 을 모델하지 않는다**(박스상 AR 15–30)
      ⇒ *"우리 σ_e 폼이 잘못된 형상 위에서 fit 됐다"* 는 **이 논문으로 지지되지 않는다**.  Stage 22.5 동결 유지.
    · **Q4(PTFE §F1 앵커) 확정: 메우지 않는다** — 원문이 두 곳에서 PTFE 를 *"before fibrillation"* /
      *"initial particulate morphology prior to shear-induced fibrillation"* 로 명시.  우리 PTFE_D/L 은 **섬유화 후**.
      그리고 논문은 **섬유화 후 치수를 아무 데도 정량하지 않는다**.
    · **Q5(#30 carbon-SE 면적 유비) 성립하되 형태까지만** — 기전 형태(탄소 표면 전자전달 → 전해질 산화)는 같고
      **반응 상대가 액체 카보네이트 vs 고체 LPSCl 로 달라 속도상수 전이 불가** ⇒ **#30 을 "면적만 계산, 속도는 §F1"**
      로 둔 현재 설계가 옳다.  (⚠ 이 논문은 속도상수를 안 준다; LSV 조차 Al 공식으로 부분 오염.)
    · ⚠ **계획서에 좁혀야 할 표현 2건 (원문 정독으로 발견)**:
      ① 계획서 §1-(d) 가 217× AM-우회비를 우리 per-AM `je` 와 *"같은 부류·같은 이산화"* 라고 썼는데,
         그 COMSOL 메시는 **2D 단면을 z 로 복제한 준-2D 압출체**다 (*"stacking two identical images together"*)
         — 우리 STEP3 는 진짜 3D 복셀이므로 **"같은 이산화" 는 과하다**.
      ② 그 대조의 σ 는 **`zhang2023` 과 같은 상수표**(σ_CBD 700 · σ_NMC 5e-3)라 **독립 앵커가 아니다**
         ⇒ 앵커 CSV 에 **`same-source as zhang2023` 플래그**가 필요하다.
    · ⚠ **τ 2.49/2.87 을 앵커 CSV 에 넣지 말 것** — 규약이 논문 안에서 미끄러진다 (위 ⑨).

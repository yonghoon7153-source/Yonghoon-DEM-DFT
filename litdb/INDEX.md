# 📚 LITDB — DEM+MPM ASSB 압밀·전달 문헌 인덱스

> 갱신: 2026-06-26. 각 논문 상세는 `papers/<slug>.md` (digest), 우리 대비는 `comparison_vs_ours.md`,
> 기준값은 `our_dem_baseline.md`. 수치 CSV는 `docs/data/<slug>_*.csv`.

Status 범례: ✅ digest 완료 · ⬜ PDF만(미digest) · 📄 메타만

## DEM/MPM 압밀 · 전달 (composite ASSB)

| 논문 (제1저자 년) | 저널 | 소재 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|---|
| **Lee 2025** | Nat. Commun. 16, 4200 | **LPSCl + NCM811/82 + VGCF + PTFE** (= 우리 소재·도전제 전부) | **실험**(no sim) **건식 co-rolling 박막**(SSE 50µm + 양극 80wt%AM 5mAh/cm²); ★★**저작동압 2 MPa>80% 500cyc**(75 MPa>95%) = robust 융합 계면(계면 void 75→2 MPa: free 4.0→15.5 vs co 1.9→3.5); 제조 500 MPa·작동 2/5 MPa **명시 분리**(=fab-vs-operating, Doux/Minnmann 합류); ★PTFE 0.5/2/5 wt%→σ_e 34/4.5/0.011·σ_i 0.069/0.024/0.007; ★binder-VGCF fibril망(=우리 CBD); ★PC-NCM 깨짐/SC-NCM 무손상; 310 Wh/kg·805 Wh/L | exp | ✅✅ | `lee2025_corolling_dryprocess_lpscl_ptfe` (papers) + `docs/lit_lee2025_corolling_dryprocess_assb` (공정/압력) |
| **Bazzoun 2026** | J. Power Sources 661, 238682 | **LPSCl + NMC811** | DEM+FEM+RNM σ_eff,ion; 실험 0.137/0.101/0.065 mS/cm @f_CAM 70/75/80; RNM=Holm/Kirchhoff; E_SE=22.1 | DEM+FEM+RNM | ✅ | `bazzoun2026_dem_fem_rnm_ionic` |
| **Varkey 2026** | Adv. Powder Tech. 37, 105338 | halide Li₃YBrCl₆ + NMC811 | multi-contact 탄소성 DEM; separator floor 21% / cathode 37% @350MPa; E_SE=10.58; CONTACT-소성만(구) | DEM | ✅ | `varkey2026_multicontact_elastoplastic_dem` |
| **So 2021** | J. Power Sources 508, 230344 | LPS(Li₂S–P₂S₅) + Si음극 | 3D DEM(소성 cold-press, **H-cap real E=24**); rel.density 0.30→**0.98**@600MPa, φ_SE^crit=0.13, AM-AM 응력 5.9 GPa | DEM | ✅ | `so2021_dem_mold_pressure_assb_coldpress` |
| **Martin & Bouvard 2003** | Acta Mater. 51 | soft+hard 구 혼합 | DEM 냉간압밀; 2-메커니즘(force-network K_h + excluded-volume 과변형), Storåkers 소성접촉, 거시응력 E₂/E₁=10→100서 <3% | DEM | ✅ | `martinbouvard2003_dem_composite_cold_compaction` |
| **Bouvard 2000** | Powder Technol. 111, 231 | 경(세라믹)+연(금속) 혼합 | 압밀 2체제(재배열/연-변형) + percolation 임계 vs 크기비(0.32@r=1→0.18@r=2); SE+AM dip 원형 | exp+theory | ✅ | `bouvard2000_hard_soft_powder_densification` |

## 구조-모델링 peer (microstructure generation + percolation/접촉 — 우리 DEM 구조 파이프라인의 직접 비교)

| 논문 (제1저자 년) | 저널 | 소재 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|---|
| **★ Bielefeld 2019** | J. Phys. Chem. C 123, 1626 | NCM-811/622 + LPS (사실상 재료-무관: shape/size/overlap만) | ★ **GeoDict 구조-모델링 (Janek 그룹) — 우리와 *가장 가까운* 구조-모델링 peer.** **stochastic placement**(AM 구 no-overlap + SE polyhedra overlap, 사후 겹침조정) → **Hoshen-Kopelman** percolation(이온/전자 cluster)·utilization·active interface.  ★ **σ는 *안 풂*(percolation 존재+cluster 부피까지; constriction=ref36 Greenwood future work)**·**단봉 PSD**(bi/tri-modal 보류)·porosity/조성/입경=*입력*.  p_c(전자)=**7.83·ln(d)+36.67 vol%**(Fig6)·β=**0.41**(3D site-perc, Fig4)·이상조성 **62/38·66/34·72/28 vol%@porosity 5/10/20%**·전자한계<69·이온한계>79 vol%(Fig7)·good-perf porosity **~21%**(Fig9, ≠압밀floor 의미). carbon-free(=Strauss ref13). ⇒ **top-down/placement** — 우리 bottom-up/압축+σ삼중항+MPM이 *비운 칸* 채움; Bazzoun2026(같은 그룹 RNM σ)이 후속으로 σ 추가 | continuum (GeoDict, voxel percolation) | ✅(docs) | `docs/lit_bielefeld2019_microstructural_modeling_composite_cathodes.md` |
| **★ Bielefeld 2020** ⚠(위시리스트 "2022"=오기, 실제 **2020**) | ACS Appl. Mater. Interfaces 12, 12821 | NCM811 + LPSCl(σ_bulk 2.7 mS/cm); σ-검증계는 LCO+LGPS | ★ **Bielefeld 2019의 *σ-추가 후속편*(같은 1저자·GeoDict).** 2019가 미룬 **σ_eff,ion + τ²**를 GeoDict **flux-PDE**(EJ-HEAT 연속체, ∇·(−σ∇φ)=0)로 *풀고*, ★ **바인더(CBD) 영향**(SE 이온망 차단)까지 추가.  ★ σ-method = **연속체 flux-PDE** → **point-contact constriction(Holm/Greenwood) *없음* = σ 상한**(AM/SE 면접촉저항 40 Ω·cm²만; SE-SE 좁힘 빠짐); Bazzoun/우리가 constriction 되돌림.  σ_eff 0.07–0.62 mS/cm·**Kato재구성 0.68 vs 실측 0.73**(검증 1점, LCO+LGPS)·τ² 2→10·**Bruggeman 4× 과소**(Fig2, =우리 R_brug 근거)·**5% void가 20% void 대비 σ 2×**(Fig4)·작은 AM→σ↓τ²↑(이온 장애물; 우리 작은 SE→σ↑와 *반대 채널·같은 그림*).  ★ **바인더 V(B):V(AM) 0.05/0.10 → σ_eff급감·τ² 4.2→6.4→10·active interface −17~43%/−29~82%(고-AM 비선형)**(Fig5, interfacial meniscus 배치) = 우리 CBD/voxel σ-블로킹(SuperP 0.0168<VGCF 0.0298)·#271 Hong PTFE·Lee2025 직접 cross-check.  단봉+trimodal 1케이스(1:1:2 de Larrard) → **dip 미측정**(porosity 15% 고정). C-rate Table1(SE<5 mS/cm thick 불가, 타깃 10). ⇒ **그룹-진화 가운데토막: 2019(σ없음)→2020(연속체σ+바인더)→Bazzoun2026(RNM/constriction σ)→우리(삼중항+MPM)** | continuum (GeoDict, voxel flux-PDE σ_ion) | ✅(docs) | `docs/lit_bielefeld2020_effective_ionic_conductivity_binder.md` + `docs/data/bielefeld2020_sigma_binder.csv` |

## 패킹 기하 (geometric packing — Furnas dip 근거)

| 논문 (제1저자 년) | 저널 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|
| **McGeary 1961** | J. Am. Ceram. Soc. 44(10) | 강체 구(금속 shot) bimodal/multimodal 충전 62.5→86→90→95.1%, 임계비 **7:1**(0.154·d_c); **소성변형 없음** = Furnas-dip 기하 원전 | exp | ✅ | `mcgeary1961_bimodal_sphere_packing` |

## 실험 1차 앵커 (EIS-TLM / 측정값)

| 논문 (제1저자 년) | 저널 | 소재 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|---|
| **★ Minnmann 2021 JES** | J. Electrochem. Soc. 168, 040537 | **NCM-622 + LPSCl** (= 우리 소재계) | ★★ **우리 porosity/σ_ion/τ 앵커의 진짜 출처.** EIS-TLM 1차 측정: **복합 porosity 14 % (13–17 %, dry-mix 380 MPa)** · **σ_ion,eff 0.17 mS/cm @ 42 vol% NCM** · **τ_ion 2.07 (=√(τ²=4.3))** · σ_el,eff 0.56 (τ_el²=7.4) · LPSCl bulk 1.6 mS/cm · NCM 전자 10 mS/cm. CAM vol% 25–61 스윕(CAM↑→σ_ion↓/τ↑), 42 vol% 154 mAh/g 최적; carbon-free 고-CAM; fine SE→σ_ion,eff↑(packing/τ). | exp (EIS-TLM+cycling) | ✅(docs) | `docs/lit_minnmann2021_jes_charge_transport_bottlenecks.md` |
| **★ Doux 2020** | Adv. Energy Mater. 10, 1903253 | **LPSCl + Li-metal** (+LNO-NCA full cell) (= 우리 SE) | ★ **작동압(operating) vs 제조압(fabrication) 앵커.** Li 대칭셀 단락시간: **75→0, 25→48, 20→190, 15→272, 10→474, 5 MPa→∞(>1000h)** → 최적 작동 **5 MPa**(≥25 단락, Li가 SE 공극으로 creep=기계적 단락). 임피던스 **500→32 Ω(@25 포화), release 비가역(110→50)**. ★ 펠릿 **porosity 18 %(rel.dens 82.1 %)@370 MPa** = 강체-구 floor 실험 확증. σ_pellet 2–2.5 mS/cm. full cell 229 cyc/80.9 %@5 MPa. ⚠ Li-metal 단락 논문 → SE 압력-역학만 전사 | exp (in-situ P-cell + XCT/XRD) | ✅(docs) | `docs/lit_doux2020_stack_pressure_assb.md` |
| **★ Cronau 2021** | ACS Energy Lett. 6, 3072 | sulfide SE 6종 (µC-Li₆PS₅**Br** 등, **단결정·Cl 측정 無**) | ★ **stack pressure 가 σ *측정* 신뢰성을 좌우**(측정 protocol). σ_grain=3.0 출처판정: 본 논문 아님(µC-Br plateau ~2.4 + 타 LPSCl 종합); Cronau(r_SE)=결정도/GB 인자(breakpoint 미지지). 제조압 400–500 + 작동 5–50 MPa 권고 | viewpoint (exp) | ✅(docs) | `docs/lit_cronau2021_stack_pressure_ionic_conductivity.md` |
| **★ Sakuda 2013** | Sci. Rep. 3, 2261 | **75/80Li₂S·25/20P₂S₅ glass**(=Li₃PS₄ 조성 유리, **NOT LPSCl**) + LiCoO₂ 셀 | ★ **황화물-기계물성 고전 + 우리 두 토대 앵커의 원전.** (1) **E_SE 18–25 GPa, 75Li₂S·25P₂S₅=24**(초음파, stated) = 우리 real-bulk 24 의 출처(E_eff 1.35/1.53 = 그 연화 프록시); (2) "**상온 가압소결**"(산화물과 달리 냉간 치밀, Fig2·3 입계소멸) = 우리 cold-press+MPM void-fill 물리 토대. 밀도: **stated ">90 %@>350 MPa"**(porosity<10), ~87 %@300 = **Fig2a digitized 추세**. σ 냉간 0.31/bulk 0.34 mS/cm. ⚠ glass≠LPSCl → 물리·E 전이 OK, σ·밀도 절대값 전이 금지 | exp (밀도-P + 초음파E + EIS + 셀) | ✅(docs) | `docs/lit_sakuda2013_sulfide_mechanical_property.md` |

## 설계 Perspective (정성 — 수치 앵커 아님)

| 논문 (제1저자 년) | 저널 | 소재 | 핵심값 | type | status | slug |
|---|---|---|---|---|---|---|
| **Minnmann 2022** | Adv. Energy Mater. 12, 2201425 | NCM/LFP/LMO/conv + sulfide/halide SE (우리 LPSCl+NCM 설계공간) | ★ **설계 Perspective(1차데이터 아님)**; porosity/σ **측정값 0개**(전부 정성); 설계임계만: CAM 60–70 vol% 최적·3–5 µm CAM·작은 SE+큰 CAM/SE비·tailored PSD·SE 고tortuosity(C(τ) 정당화)·§5.4 결합 mech-echem-thermal 모델 호명. **★ 우리 "Minnmann porosity 14 %/13–17 %/τ 2.07" 앵커는 이 논문 아님 → Minnmann 2021 JES 040537 / Sakuda 2013** (digest §0) | review | ✅(docs) | `docs/lit_minnmann2022_designing_cathodes_solidstate.md` |

> ★ **PROVENANCE 확정 (2026-06-26, Minnmann 2021 PDF 직접 확인):** porosity 13–17 %·σ_ion_eff 0.17·τ_ion 2.07 = **Minnmann *2021 JES* 040537**(NCM622+LPSCl, **압밀 380 MPa**, EIS-TLM **측정 40 MPa**, **42 vol% NCM** 기준). 세 앵커 전부 PDF 본문서 stated 확인 (τ_ion 2.07 = √(tortuosity factor τ²=4.3) — τ vs τ² 구분 필수). 밀도 앵커 = **Sakuda 2013**(75Li₂S·25P₂S₅ **glass**, ≠LPSCl): **stated ">90 %@>350 MPa"(porosity<10)** — "**87 %@300 MPa**"는 **Sakuda Fig2a 에서 digitized 한 추세값**(±, 본문에 300 MPa 정밀값 **없음**); pure-SE 10 % = 우리 MPM 보정 수렴값(Minnmann 논문은 *복합* porosity만 줌, pure-SE 아님). 2022 AEM Perspective는 **정량 데이터 없음.** + `refs.bib @Minnmann2021`이 엉뚱한 040502/abf3a3을 가리킴 → **040537/abf8d7**로 정정 권고. 저자 = Philip Minnmann, **Lars Quillman**, Simon Burkhardt, Felix H. Richter, Jürgen Janek.

## 통합된 기존 노트 (→ papers/ digest로 흡수)
- `docs/lit_varkey2026_multicontact_dem.md` (한국어 노트) → `papers/varkey2026_*` ✅ + `docs/data/{densification_porosity_db,varkey2026_ionic_vs_pressure}.csv`
- `docs/lit_bazzoun2026_dem_fem_rnm.md` (한국어 노트) → `papers/bazzoun2026_*` ✅ + `docs/data/bazzoun2026_sigma_ionic.csv`
- **Lee 2025** (실험 앵커) → `papers/lee2025_*` ✅ (σ·CBD·파괴 관점) + **`docs/lit_lee2025_corolling_dryprocess_assb.md`** ✅ (★ **공정(co-rolling) + 저작동압 2 MPa + fab-vs-operating** 관점, Doux/Minnmann 압력구분 합류) + `docs/data/lee2025_transport_anchors.csv` (PTFE% σ 페널티 + 조성별 σ + bulk 앵커); CBD 검증 → `docs/cbd_morphology_roadmap.md`
- `docs/literature_coverage/` json DB: contact_mechanics_db, coverage_db, packing_regime_db (수치 참조용 유지)

## 주제별 종합 문서
- `elasto_plastic_feasibility.md` — elasto-plastic 접촉모델 실행가능성·적용·우리 모델 대비 장단점
  (Varkey/So/M&B 종합; ★ So 2021 H-cap = 18× 연화 대체 경로).

## 현황
papers/ digest 7편 ✅ (**Lee2025**(실험 앵커, =우리 소재 전부) · Bazzoun · Varkey · So2021 · Martin-Bouvard2003 · Bouvard2000 · McGeary1961)
+ docs/ digest: **Minnmann 2021 JES**(★ porosity/σ_ion/τ 앵커 진짜 출처, EIS-TLM) · Minnmann 2022(설계 Perspective)
· **★ Doux 2020**(작동압 vs 제조압 LPSCl 앵커, porosity 18 %@370 MPa) · **Cronau 2021**(stack pressure σ-측정 protocol)
· **★ Sakuda 2013**(황화물-기계물성 고전; E_SE 24 GPa 원전 + "상온 가압소결" 원전; 밀도 stated >90 %@>350 MPa)
· **★ Bielefeld 2019**(★ 우리와 가장 가까운 *구조-모델링 peer*; GeoDict stochastic-placement percolation, Janek 그룹;
  σ 안 풂·단봉 PSD·porosity=입력 → top-down/placement; p_c=7.83·ln(d)+36.67·β=0.41·이상조성 62/38~72/28 vol%; CSV `docs/data/bielefeld2019_percolation_thresholds.csv`)
· **★ Bielefeld 2020**(⚠위시리스트 "2022"=오기, 실제 **2020**; ★ Bielefeld 2019의 *σ-추가 후속편*, 같은 1저자·GeoDict;
  2019가 미룬 **σ_eff,ion+τ²를 flux-PDE(EJ-HEAT 연속체)로 풀고 바인더(CBD) 영향 추가**; σ-method = **연속체 PDE → constriction 없음=σ상한**;
  Bruggeman 4× 과소·5% void→σ 2×·**바인더 V(B):V(AM) 0.05/0.10→σ급감·τ² 4.2→10·active interface −17~82%**(우리 CBD/voxel σ-블로킹 cross-check);
  **그룹-진화: 2019(σ없음)→2020(연속체σ+바인더)→Bazzoun2026(RNM/constriction)→우리**; CSV `docs/data/bielefeld2020_sigma_binder.csv`).
**Stack-pressure 3종 압력 구분 완성:** 제조(fab ~300–490 MPa: Minnmann 380 / Doux·Cronau 370–490) ≠ 측정/작동(stack ~5–70 MPa:
Doux 5 최적 / Minnmann 측정 40 / Cronau sputter 5–10·WC 30–50). 데이터 `docs/data/doux2020_stack_pressure.csv`,
`cronau2021_stack_pressure_ionic.csv`, `minnmann2021_sigma_tau_porosity.csv`.
새 PDF 업로드 후 "논문 에이전트 실행해줘"로 추가.

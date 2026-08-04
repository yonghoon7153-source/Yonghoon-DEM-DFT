# 🧱 LITDB — DEM · MPM 축 인덱스

> **이 파일은 `tools/litdb/build_index.py` 가 생성한다 — 손으로 고치지 말 것.**
> 논평·우선순위가 붙는 SE 축 인덱스는 `INDEX.md` (사람이 큐레이션).
> digest 95편 · 생성 2026-08-05

왜 따로 두나 — `INDEX.md` 는 argyrodite 전해질 축이라 접촉역학·MPM·건식전극
digest 가 들어갈 자리가 없다. 그래서 한때 64편이 **어느 인덱스에도 없었다**
(open_items #7). 축을 나누고 생성으로 바꿔 그 구멍을 닫는다.

## MPM · 연속체 (6편)

| slug | 논문 | 유형 | digest | 그림 |
|---|---|---|---|---|
| `choi2024_digital_twin_review_echem` | Choi 2024 (E.Chem 매거진 총설, Vol.16 No.1) — 디지털 트윈 모델링·시뮬레이션 ★ 우리 DEM+MPM의 top-down/bottom-up POSITIONING을 NAMING하는 framework 리뷰 | tool·digital-twin 총설 | 2026-07-28 | — |
| `devaucorbeil2020_mpm_after_25_years_review` | MPM after 25 years: theory, implementation, applications (리뷰) — de Vaucorbeil, Nguyen, Sinaie, Wu (Adv. Appl. Mech. 2020) | MPM 리뷰(review) | 2026-06-26 | — |
| `klar2016_dp_sand_animation` | 모래(sand) 애니메이션을 위한 Drucker-Prager 탄소성 — Klár (ACM TOG 2016, SIGGRAPH) | MPM | 2026-06-26 | 🖼 17 |
| `lim2025_virtual_calendering_framework` | Lim 2025 (Small 21, 2410485) — Virtual Calendering Framework: 3D-재구성 양극으로 가상 캘린더링 검증 + 전극설계 최적화 ★★★ 우리 DEM+MPM 압축의 가장 직접적인 방법론적 형제 (reconstruct-then-compress vs 우리 predict-from-pow | FEM·calendering | 2026-07-28 | — |
| `nam2026_dpe_microstructure_review` | Nam 2026 (Materials Horizons REVIEW, 13, 3149-3177) — 건식전극(DPE) 미세구조 엔지니어링 리뷰 ★ 우리 DEM+MPM 프로젝트의 FRAMEWORK/POSITIONING 논문 | DEM | 2026-07-28 | — |
| `stomakhin2013_mpm_snow_elastoplastic` | 눈(snow) 시뮬레이션을 위한 Material Point Method — Stomakhin (ACM TOG 2013, SIGGRAPH) | MPM | 2026-06-26 | 🖼 12 |

## 접촉역학 · 소성 (DEM 이론) (18편)

| slug | 논문 | 유형 | digest | 그림 |
|---|---|---|---|---|
| `bouvard2000_hard_soft_powder_densification` | 경/연 분말 혼합물의 가압 압밀 거동 — Bouvard (Powder Technology 2000) | exp+theory(review) | 2026-06-23 | — |
| `dmt1975_adhesion_contact_deformation` | Effect of Contact Deformations on the Adhesion of Particles (DMT 이론) — Derjaguin, Muller, Toporov (J. Colloid Interface Sci. 1975) | continuum (점착 접촉역학 이론) | 2026-06-26 | 🖼 1 |
| `electromechanical_contact_model_particulate_systems` | An electro-mechanical contact model for particulate systems — Chao Zhang (Powder Technology 2024) | DEM (Hertz-Mindlin 역학 + Holm/constriction 전기접촉저항 + Kirchhoff | 2026-06-26 | — |
| `jacksongreen2005_fem_elastoplastic_hemispherical_contact` | 탄소성 반구–강체평판 접촉의 유한요소 연구 — Jackson & Green (J. Tribology 2005) | FEM (continuum, single-contact) | 2026-06-26 | — |
| `kogutetsion2002_ep_sphere_rigid_flat` | 변형 탄소성 구 ↔ 강체 평판 접촉의 탄소성 FEM 해석 (KE 모델) — Kogut & Etsion (J. Appl. Mech. 2002) | FEM (continuum, single-contact) | 2026-06-26 | 🖼 8 |
| `luding2008_cohesive_frictional_contact_models` | 점착·마찰 분말의 접촉모델 (인장 가능 LAW) — Luding (Granular Matter 2008) | DEM (contact-LAW theory) | 2026-06-26 | — |
| `martinbouvard2003_dem_composite_cold_compaction` | 연질+경질 분말 혼합물의 냉간 압밀을 DEM으로 — Martin & Bouvard (Acta Materialia 2003) | DEM | 2026-06-23 | — |
| `mcgeary1961_bimodal_sphere_packing` | 구형 입자의 기계적 패킹 — 크기비·다성분 최대 충전밀도의 고전 — McGeary (J. Am. Ceram. Soc. 1961) | exp | 2026-06-23 | — |
| `mesarovicfleck2000_dissimilar_elastoplastic_indentation` | 비대칭(dissimilar) 탄소성 구의 무마찰 압입 — Mesarović & Fleck (Int. J. Solids Struct. 2000) | FEM (continuum, single-contact) | 2026-06-26 | — |
| `oh2026_bimodal_composite_cathode` | Oh 2026 (ACS Energy Letters 11, 2103-2114) — Bimodal 복합양극: 큰 다결정 + 작은 단결정 CAM → packing·porosity·tortuosity 최적화 ★★★ 우리 정확한 소재계 + 정확한 조건 + 우리 a9_50 P:S sweep의 HEADLINE 실험 검증 | experiment | 2026-07-28 | — |
| `pasha2014_linear_elastoplastic_adhesive_contact` | 선형 탄소성·점착 접촉 변형 모델 (미세 점착분말용 piecewise-linear LAW) — Pasha (Granular Matter 2014) | DEM (contact-LAW theory + EDEM 구현/검증) | 2026-06-26 | — |
| `schreiner2020_dem_calendering_lib` | LIB 전극 calendering(압연)을 DEM으로 — NMC622 양극 · **EDEM(상용) + EEPA 탄소성 접촉 + Bonding(Potyondy–Cundall)** · 3-모듈 **"USER TOOL"**(공정 파라미터 *예측*) — Schreiner·Klinger·Reinhart (Procedia CIRP  | DEM (EDEM 상용, EEPA+Bonding; 나노압입 보정 + 공정 USER TOOL) | 2026-06-27 | — |
| `shi2019_high_am_loading_particle_size_assb` | 입자 크기비 λ=D_CAM/D_SE 로 고-CAM 로딩(>50 vol%) 달성 — 우리와 *같은 LIGGGHTS DEM + Hertz* 로 "작은 SE + 큰 CAM"을 모델+실험 동시 증명 — Shi (Ceder 그룹, Adv. Energy Mater. 2019/2020) | mixed (DEM-LIGGGHTS modeling + experiment) | 2026-06-26 | — |
| `so2022_dem_contact_model_assb_compaction_sintering` | ASSB 전극 압밀·소결 DEM을 위한 접촉모델 (탄성+소성+점탄성 + 소결 + 면적/스프링 인자) — So (MethodsX 2022) | DEM | 2026-06-26 | 🖼 10 |
| `storakers1997_similarity_inelastic_contact` | 비탄성 접촉의 자기상사(similarity) 해석 — Storåkers, Biwa & Larsson (Int. J. Solids Struct. 1997) | continuum (self-similar inelastic single/pair contact theory | 2026-06-26 | 🖼 4 |
| `thakur2014_eepa_adhesive_elastoplastic_dem` | EEPA 점착 탄소성 접촉모델 (면적의존 점착) — 응집 분말의 미시역학 — Thakur (Granular Matter 2014) | DEM (contact-LAW theory + uniaxial calibration) | 2026-06-26 | — |
| `thorntonning1998_adhesive_elastoplastic_contact` | 점착 탄소성 구의 stick/bounce — 항복압 캡(p_y) 접촉 LAW의 정의서 — Thornton & Ning (Powder Technology 1998) | DEM (contact-LAW theory) | 2026-06-26 | — |
| `varkey2026_multicontact_elastoplastic_dem` | 응력기반 multi-contact 탄소성 모델로 SE separator·양극 압밀 DEM — Varkey (Adv. Powder Tech. 2026) | DEM | 2026-06-23 | — |

## 복합양극 미세구조 · percolation (15편)

| slug | 논문 | 유형 | digest | 그림 |
|---|---|---|---|---|
| `bielefeld2019_microstructural_modeling_composite_cathode` | 복합 양극의 3D 미세구조 모델링 — percolation 이론으로 이온·전자 전도 클러스터 분석 — Bielefeld (J. Phys. Chem. C 2019) | continuum (geometric microstructure + percolation) | 2026-06-26 | 🖼 11 |
| `bielefeld2020_effective_ionic_conductivity_binder` | Bielefeld 2020 (ACS Appl. Mater. Interfaces 12, 12821−12833) — 유효 이온전도도 + 바인더 영향 모델링 (Janek 그룹, GeoDict — ★ Bielefeld 2019의 σ-추가 후속편) | FEM·digital-twin | 2026-07-28 | 🖼 7 |
| `chen2011_percolation_micromodel_composite_electrode` | 다분산 입경 복합전극의 유효물성 예측 — *해석적* percolation 미시모델 (CN·percolation·TPB·σ_inter/intra·hydraulic pore 닫힌식) — Chen (J. Power Sources 2011) | continuum (analytic percolation micro-model — closed-form, N | 2026-06-26 | — |
| `jung2023_single_crystal_ncm_morphology` | 필독 / 우리-랩 — Customizing the Morphology and Microstructure of Single-Crystalline Ni-rich Layered Cathode Materials for All-Solid-State Batteries — Jung et al. (Chem. Eng. J. 2023) | exp (morphology / electrochemistry / mechanical) | 2026-06-26 | 🖼 7 |
| `kim2024_carbon_volumetric_occupation_se_domain` | 필독 / 우리-랩 — Accelerated Degradation of ASSBs Induced through Volumetric Occupation of the Carbon Additive in the SE Domain — Kim, Park, Kang, …, Lee, Sun, Cho (Adv. Funct. Mater. 2 | exp | 2026-06-26 | 🖼 5 |
| `kim2026_a3d_air_electrode_microstructure_transport` | Kim 2026 (Journal of Power Sources 686, 240471) — 디지털트윈 미세구조(GeoDict) → 유효물성 → 1D 전기화학(COMSOL)으로 A3D 공기극 수송 설계 | FEM·digital-twin | 2026-07-28 | — |
| `minnmann2021_jes_charge_transport_bottlenecks` | Minnmann 2021 JES — 복합 양극 전하수송 병목 정량화 (EIS-TLM) ★ 우리 porosity/σ_ion/τ_ion 앵커의 진짜 출처 | DEM | 2026-07-28 | — |
| `minnmann2024_microstructure_porosity_visualization` | 복합 양극 미세구조·porosity → SSB 성능을 FIB-SEM 토모그래피로 *시각화* — Minnmann (J. Electrochem. Soc. 2024, Editors' Choice) | exp | 2026-06-26 | 🖼 8 |
| `nisar2024_dem_effective_electrical_conductivity_sps` | 부분소결 다공성 재료의 유효 전기전도도를 위한 DEM 저항망 모델 (sinter-neck conductance) — Nisar (Comp. Part. Mech. 2024) | DEM+RNM | 2026-06-26 | — |
| `reisacher2023_percolation_sulfide_carbon_matrix` | #27 (★ 우리 EXACT SE) — Percolation Behavior of a Sulfide Electrolyte–Carbon Additive Matrix for Composite Cathodes in All-Solid-State Batteries — Reisacher, Kaya, Knoblauch (Batteri | exp | 2026-06-26 | 🖼 8 |
| `sangros2020_dem_electrical_conductive_paths_assb` | ASSB(폴리머 SSB) 복합 양극의 **전자 전도경로**를 DEM으로 — A* 경로탐색 + 실린더-저항 등가회로 + percolation, LFP+CB+PEO — Sangrós Giménez (Chem. Eng. Technol. 2020) | DEM (LIGGGHTS) + A* 경로탐색 + 등가회로 σ + skeleton τ | 2026-06-26 | — |
| `so2022_dem_compaction_coated_particles_assb` | SE-코팅(core-shell) vs 입자-혼합 ASSB 양극의 DEM 냉간압밀 — tortuosity·AM damage·percolation + 코팅의 σ_e 차폐 — So (J. Power Sources 2022) | DEM | 2026-06-26 | — |
| `tailored_cathode_microstructure_low_pressure_assb` | Tailored Cathode Composite Microstructure Enables Long Cycle Life at Low Pressure for ASSBs — Zhou et al. (ACS Energy Lett. 2025) |  | 2026-06-26 | — |
| `taufactor_tortuosity_factor_tomography_tool` | TauFactor — voxel 미세구조에서 정상상태 확산(Laplace)을 풀어 tortuosity FACTOR τ 를 직접 계산하는 오픈소스 MATLAB 툴 — Cooper (SoftwareX 2016) | tool (voxel Laplace-solve, post-processing) | 2026-06-26 | — |
| `yoo2026_porosity_gradient_dry_electrode` | Yoo 2026 (Energy Storage Materials, ENSM 105331) — Porosity-구배 건식 흑연 전극 + 변형성 Primer Layer | MPM | 2026-07-28 | — |

## 공정 — 캘린더링 · 압축 · 건식전극 (22편)

| slug | 논문 | 유형 | digest | 그림 |
|---|---|---|---|---|
| `bak2024_binder_distribution_multilayer` | Bak 2024 (Chemical Engineering Journal 483, 148913) — 바인더 z-분포 제어 다층 모델전극 + Digital-Twin | MPM | 2026-07-28 | 🖼 6 |
| `bzox_dry_zro2x_nmc_shell_coating_sulfide_assb` | → superseded by `choi2026_bzox_dry_zro2x_nmc_shell_coating.md` |  | — | — |
| `cho2024_conflicting_roles_conductive_additive` | 필독 / 우리-랩 — Conflicting roles of conductive additives in controlling cathode performance in ASSBs — Cho, Yun, Kang, Kim, Lee (Electrochimica Acta 2024) | exp + AC-impedance decoupling (modified TLM) + DC-polarizati | 2026-06-26 | 🖼 6 |
| `duquesnoy2023_ml_multiobjective_manufacturing_optimization` | 물리기반 시뮬 합성데이터 + ML(SISSO+베이지안 다목적최적화)로 LIB 전극 제조 역설계 — Duquesnoy (Energy Storage Mater. 2023) | mixed (CGMD+DEM physics-sim + SISSO ML + Bayesian multi-obje | 2026-07-10 | — |
| `frankenberg2024_dem_high_intensity_mixer_assb` | ASSB 복합양극을 *고강도 믹서(high-intensity mixer)* 로 만드는 공정을 DEM으로 — coarse-graining + **force-scaling**(접촉력 스케일링) + 3단계 보정으로 stressing condition을 추출하고, 그것을 미세구조·풀셀 용량에 연결 — Frankenberg (Po | DEM (Rocky 2023 R1, coarse-grained + force-scaling, 3-step c | 2026-06-26 | — |
| `han2025_icep_conductive_elastic_binder` | 이온전도성 탄성 고분자(ICEP) 바인더로 초고로딩 NCM811 전극 — Han (Adv. Mater. 2025) | exp (+DFT 흡착) | 2026-07-08 | — |
| `hong2026_sulfide_cathode_binder_digitaltwin` | Hong 2026 (Energy Storage Materials 86, 104930) — 황화물 복합양극 열화 메커니즘 (디지털트윈): Dry(PTFE) vs Wet(NBR) 바인더 ★우리 소재계(LPSCl+NCM) | FEM·digital-twin | 2026-07-28 | — |
| `jun2026_ppma_econductive_binder_si_lowpressure_assb` | Electron-conductive binder for silicon negative electrode enabling low-pressure all-solid-state batteries — Jun & Jeong et al. (Nat. Commun. 2026) | exp (계산 0) | 2026-07-15 | 🖼 5 |
| `kang2025_bollard_anchored_binder_dry_electrode` | Bollard-Anchored Binder System for High-Loading Cathodes Fabricated via Dry Electrode Process — Kang, Jihyeon (Adv. Mater. 2025) | exp + MLP-DFT/MD (molecular) | 2026-07-08 | — |
| `kim2026_charge_engineered_cnf_binder` | Kim 2026 (Nature Communications, DOI 10.1038/s41467-026-73909-0) — 전하조작(charge-engineered) 셀룰로오스 나노피브릴 바인더로 PFAS-free 고로딩 양극 | experiment | 2026-07-28 | — |
| `koo2025_cnt_wrapped_sc_nca_dry_cathode` | Koo 2025 (Energy Storage Materials 78, 104270) — anti-solvent로 MWCNT 감싼 단결정 SC-NCA dry 양극 (99.6 wt%, 4.0 g/cm³) ★ #275(Joule 2026)의 2025 PRECURSOR / SISTER 논문 | FEM·digital-twin | 2026-07-28 | — |
| `koo2026_swcnt_sheath_thick_electrode` | Koo 2026 (Joule 10, 102392) — 연속 SWCNT sheath가 두꺼운 dry 전극에서 초고에너지밀도 + 급속충전 (★ 우리 CBD SuperP-vs-VGCF 발견의 실험적 증명) | FEM·digital-twin | 2026-07-28 | — |
| `lee2025_corolling_dryprocess_lpscl_ptfe` | Co-rolling dry-process로 만든 박막 LPSCl SSE — robust 계면 + 저압(2 MPa) 작동 — Lee (Nat. Commun. 2025) | exp | 2026-06-24 | — |
| `liu2025_dry_processing_high_energy_li_batteries_review` | 건식공정(DPT)으로 고에너지밀도 Li 전지 전극·SE막 만들기 — DPC / 분무 / 압출 / **바인더 섬유화(PTFE)** 4대 기법 총설, LIB→ASSB 적용 — Liu et al. (Small 2025, 리뷰) | REVIEW (건식공정 총설; 실험·시뮬 *원저 아님* — 문헌 종합) | 2026-06-26 | — |
| `lyu2025_3d_dem_drying_calendering_lib` | LIB 전극 구조진화를 건조+압연 한 번에 — 3D RVE DEM(AM + carbon-binder domain + 용매 + 입자접촉), 3-stage 건조법 + 압연→σ_e·두께방향 응력 — Lyu (Int. J. Electrical Power & Energy Systems 2025) | DEM (3D RVE, 건조+압연 연속; exp 검증) | 2026-06-26 | — |
| `mun2025_dry_electrode_technology_assb_review` | 차세대 ASSB를 위한 건식전극(dry electrode) 기술 — 무용매 제조(dry-mixing·PTFE 섬유화·calendering·co-rolling) 종합 리뷰 — Mun (Advanced Materials 2025) | review (exp/process; no DEM/MPM/FEM) | 2026-06-26 | — |
| `ngandjong2021_dem_calendering_digital_twin` | LIB 전극 calendering(압연)을 DEM으로 — AM + carbon-binder domain 명시 + 슬러리→건조→압연→전기화학 "디지털 트윈" 파이프라인 — Ngandjong (J. Power Sources 2021) | DEM (+ CGMD 슬러리/건조 + FEM 전기화학; exp 검증) | 2026-06-26 | — |
| `park2026_thiolene_sbr_binder_assb` | Park 2026 (Adv. Funct. Mater. 36, e16017) — Thiol-Ene Click으로 SBR 바인더 다면 개질(접착 grafting + 가교 cross-linking), 저압 작동 ASSB ★우리 소재계(LPSCl+NCM)·BINDER-화학 중심 | MPM | 2026-07-28 | — |
| `sangros2019_dem_calendering_lib_electrode` | LIB 전극 calendering(압연)을 DEM으로 — 단일 NMC 입자 탄소성 접촉모델(나노압입 보정) + 바인더 bond 모델 + ~17% 점탄성 회복 — Sangrós Giménez (Powder Technology 2019) | DEM (in-house, 나노압입 실험 보정 + calendering 실측 검증) | 2026-06-26 | — |
| `sangros2020_lib_electrode_dem_mech_elec_ionic` | LIB 전극의 역학·전기·이온 거동을 DEM으로 — calendering + 바인더 bond 모델 + 삼중 전달 — Sangrós Giménez (Energy Technology 2020) | DEM (+ analytic homogenization, exp 검증) | 2026-06-26 | — |
| `so2021_dem_mold_pressure_assb_coldpress` | 몰드압력이 ASSB 압밀·이온전도도에 미치는 영향 — 소성변형 포함 3D DEM cold-press 모델 — So (J. Power Sources 2021) | DEM | 2026-06-23 | — |
| `wet_processing_resolved_am_ssb_cathode_manufacturing` | ASSB 양극을 *습식공정*(슬러리→건조→압연)으로 — *실제 형상(resolved, multisphere)* AM 입자를 nano-CT에서 추출해 DEM 제조 시뮬 + GeoDict로 σ_ionic·σ_e 산출 — Weitze / Franco (Energy Storage Materials 2024) | DEM (LAMMPS, multisphere resolved-AM; wet-process slurry→dry | 2026-06-26 | — |

## 화학-기계 열화 · 계면 (10편)

| slug | 논문 | 유형 | digest | 그림 |
|---|---|---|---|---|
| `bucci2017_chemomech_failure_assb_cycling_czm` | frame[5] 시간축 / 사이클-균열 — Modeling of internal mechanical failure of all-solid-state batteries during electrochemical cycling, and implications for battery design — Bucci, Swamy, Chi | FEM (coupled electro-chemo-mechanical) + CZM (cohesive-zone  | 2026-06-26 | 🖼 5 |
| `bucci2018_mechanical_instability_interface_delamination` | Mechanical instability of electrode-electrolyte interfaces in solid-state batteries — Bucci, Talamini, Renuka Balakrishna, Chiang, Carter (Phys. Rev. Materials 2018) | continuum (1D radially-symmetric analytical, cohesive-zone f | 2026-06-26 | 🖼 8 |
| `dem_mechanical_stresses_ssb_electrode_cycling` | frame[5] *사이클 응력* DEM — Understanding mechanical stresses upon solid-state battery electrode cycling using the discrete element method — Alabdali, Zanotto, Chouchane, Ngandjong, Vi | DEM (LIGGGHTS, Hertz; uniaxial+isostatic compaction → cyclic | 2026-06-26 | — |
| `interfacial_impedance_formulation_assb_cathode` | 복합 양극 계면 임피던스 *정식화*(TLM 등가회로)로 고에너지·고출력 ASSB 설계규칙 도출 — Choi 외 (ACS AMI 2024) | exp + equivalent-circuit modeling (TLM / de Levie) | 2026-06-26 | — |
| `intergranular_cracking_nmc811_jmca2023` | Direct observations of electrochemically induced intergranular cracking in polycrystalline NMC811 particles — Parks et al. (J. Mater. Chem. A 2023) | exp (operando-style ex-situ X-ray nano-CT) + phase-field FEM | 2026-06-26 | 🖼 5 |
| `kang2025_toughened_bimodal_nca_lzo` | 필독 / 우리-랩 — Toughened Bimodal Cathodes for ASSBs via Controlled Interfacial Heterogeneity — Kang & Shin (ACS Appl. Mater. Interfaces 2025) | exp + FEM (electrochemo-mechanical) | 2026-06-26 | — |
| `kim2023_chemomech_failure_highstrain_anode` | 필독 / 우리-랩 — Chemo-mechanical Failure of Solid Composite Cathodes Accelerated by High-Strain Anodes — Kang & Shin (Energy Storage Materials 2023) | exp + FEM (electrochemo-mechanical) | 2026-06-26 | 🖼 6 |
| `kim2025_impedance_decoupling_tlm_assb` | 필독 / 우리-랩 — Multiple-reaction kinetics of composite electrodes for sulfide-based ASSBs: Impedance decoupling (modified TLM) — Kim, Kang, Park, Lee (Electrochimica Acta 2025) | exp + equivalent-circuit modeling (modified TLM) | 2026-06-26 | 🖼 6 |
| `so2021_dem_fabrication_degradation_ductile_particles` | frame[5] *사이클 열화 DEM* — Simulation of Fabrication and Degradation of All-Solid-State Batteries with Ductile Particles — So, Inoue, Hirate, Nunoshita, Ishikawa, Tsuge (J. Electroche | DEM (소성 ductile-particle contact model + 2-step fabrication→ | 2026-06-26 | — |
| `yun2023_deciphering_degradation_halide_vs_sulfide` | 필독 / 우리-랩 / ★최애 — Deciphering the critical degradation factors of solid composite electrodes with halide electrolytes: Interfacial reaction versus ionic transport — Yun, Shin, Hoan | exp (impedance decoupling, SSRM/FS local mapping) + FEM (vol | 2026-06-26 | 🖼 5 |

## Digital twin · ML 최적화 (3편)

| slug | 논문 | 유형 | digest | 그림 |
|---|---|---|---|---|
| `kim2024_digital_twin_acsenergyletters` | Kim 2024 (ACS Energy Letters, 동료심사 ORIGINAL) — Digital Twin Battery Modeling and Simulations ★ 우리 top-down/bottom-up POSITIONING의 PEER-REVIEWED 인용원 (= "Ref 127") | tool·digital-twin review | 2026-07-28 | 🖼 6 |
| `lee2023_sicspe_digitaltwin_assb` | Lee 2023 (Battery Energy 2, 20220061) — 디지털트윈 기반 SIC-SPE vs LPSCl 복합양극 구조·전기화학 분석 ★ DTBL 디지털트윈 계보의 가장 이른 논문(2023) + LPSCl 전극 구조지표 | DEM | 2026-07-28 | — |
| `park2020_digitaltwin_assb_foundational` | Park 2020 (Adv. Energy Mater. 10, 2001563) — Digital-Twin-Driven All-Solid-State Battery: 물리·전기화학 거동 규명 ★ DTBL 디지털트윈 계보의 시조(FOUNDATIONAL ROOT, 2020) | FEM·digital-twin | 2026-07-28 | 🖼 26 |

## 기타 (21편)

| slug | 논문 | 유형 | digest | 그림 |
|---|---|---|---|---|
| `bazzoun2025_dem_parameter_sensitivity_assb_cathode` | DEM 파라미터 민감도 분석 + 캘리브레이션 — 냉간가압 ASSB 양극 미세구조 (Bazzoun & Piruzjam, Electrochim. Acta 2025) | DEM | 2026-06-26 | — |
| `bazzoun2026_dem_fem_rnm_ionic` | DEM-기반 미세구조 생성 + FEM·RNM으로 복합 양극 이온전도도 평가 — Bazzoun (J. Power Sources 2026) | DEM+FEM+RNM | 2026-06-23 | — |
| `boschpadros2014_dem_liggghts_msc_thesis` | Discrete element simulations with LIGGGHTS — Carles Bosch Padrós (Swansea MSc Thesis, 2014) | DEM (LIGGGHTS — methods/validation thesis) | 2026-06-26 | 🖼 4 |
| `cho2026_eipc_zn_anode_azib` | Cho 2026 (Energy Storage Materials 89 (2026) 105186, DOI 10.1016/j.ensm.2026.105186) — 전자-이온 폴리머 복합막(EIPC=GO+PAA) + PCET 반응으로 Zn 음극 안정화 (수계 Zn-ion, AZIB) | DEM | 2026-07-28 | — |
| `choi2026_elastomeric_li_metal_anode` | Choi 2026 (Advanced Energy Materials, DOI 10.1002/aenm.71104) — 친리튬(lithiophilic) 단분자층 + 나노-크럼플/마이크로-오목 탄성 Li metal anode | DEM | 2026-07-28 | — |
| `deysher2022_transport_mechanical_aspects_assb_review` | Transport and mechanical aspects of all-solid-state lithium batteries — Deysher & Ridley, Meng (Materials Today Physics 2022) [REVIEW] | REVIEW (전달 + 역학, 실험 특성화 중심 — 자체 시뮬레이션 없음) | 2026-06-26 | — |
| `doux2020_stack_pressure_assb` | Doux 2020 (Adv. Energy Mater. 10, 1903253) — Stack Pressure: 작동압력(operating) vs 제조압력(fabrication)의 정전적(canonical) LPSCl 앵커 | DEM | 2026-07-28 | — |
| `hollmann2025_tabpfn_tabular_foundation_model` | Hollmann 2025 — TabPFN: 소데이터 표형(tabular) 파운데이션 모델 (Nature) |  | — | — |
| `hong2026_cbd_viscoelasticity_springback` | Hong 2026 (Energy Storage Materials, ENSM 105321) — CBD 점탄성이 단결정 cathode의 시간의존 Spring-Back을 억제 | FEM·digital-twin | 2026-07-28 | — |
| `huang2025_dem_lbm_heat_conduction_composite_cathode` | DEM으로 생성한 3D 복합 양극 미세구조에 3D Lattice Boltzmann 열전도 모델로 ETC를 푼 연구 — Huang (J. Energy Storage 2025) | DEM+LBM (mixed) | 2026-06-26 | 🖼 21 |
| `kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review` | Intertwined Nature of Electrochemical Reactions and Mechanical Instability in Sulfide-Based All-Solid-State Batteries — Kang, Shin, Lee & **Jong-Won Lee** (Chem. Commun. *Feature A | review (Feature Article; exp+DFT+FEM 문헌 종합, 자체 신규 데이터 無) | 2026-06-26 | — |
| `kim2025_conductive_agent_se_coating_cathode` | Impact of Conductive Agents in Sulfide Electrolyte Coating on Cathode Active Materials for Composite Electrodes in All-Solid-State Batteries — Kim et al. (Battery Energy 2025) | exp (전극 제작·미세구조·전기화학 — DFT/계산 없음) | 2026-06-25 | 🖼 5 |
| `lee2024_multiphysics_dem_fem_initial_pressure_assb` | 초기압력의 ASSB 역학·전기화학 성능 영향 — DEM+FEM 멀티피직스 (Lee, J. Energy Storage 2024) | DEM+FEM (mixed, echem-mech coupled) | 2026-06-26 | — |
| `lee2026_eecfp_dnn_electrolyte_ce_lmb` | Interpretable Enhanced-ECFP-Guided Deep Learning for Rational Electrolyte Design and Coulombic Efficiency Prediction in Lithium Metal Batteries — Lee et al. (Energy Storage Materia | exp(셀·Raman·SEM·XPS) + ML(e-ECFP/DNN/SHAP) — **자체 DFT/MD 0** | 2026-07-17 | — |
| `minnmann2022_designing_cathodes_solidstate` | Minnmann 2022 (Adv. Energy Mater. 12, 2201425) — "Designing Cathodes and Cathode Active Materials for Solid-State Batteries" (설계 Perspective) | DEM | 2026-07-28 | — |
| `oh2026_carbon_coating_siox_ion_electron_balance` | Oh 2026 (Journal of Power Sources 689, 240698) — SiOx 탄소코팅 두께가 이온/전자 수송 BALANCE + 균일분산을 결정 | FEM·digital-twin | 2026-07-28 | — |
| `park2026_ceramic_pp_separator` | Park 2026 (Chemical Engineering Journal 532 (2026) 174523, DOI 10.1016/j.cej.2026.174523) — 초박막 세라믹(Al₂O₃ 스퍼터) 코팅 건식 이축연신 PP 분리막(C-DB-PP): 이온수송 ↔ 내부단락저항 균형 (Li metal battery) | DEM | 2026-07-28 | — |
| `sakuda2013_sulfide_mechanical_property` | 황화물 SE의 "유리한 기계적 물성" — 상온 가압소결·Young's modulus·이온전도도 — Sakuda (Sci. Rep. 2013) | DEM | 2026-07-28 | — |
| `schneider2023_particle_size_pressure_transport` | 입자크기·압력이 빠른 이온전도체 t-Li₇SiPS₈ 의 수송물성에 미치는 영향 — DEM 압밀 + Heckel + FVA σ — Schneider (Adv. Energy Mater. 2023) | DEM+FVA(continuum) + exp(EIS) + AIMD | 2026-06-26 | — |
| `shenouda2020_dem_metal_powder_am_liggghts_tutorial` | 금속분말 AM을 위한 DEM 해석 + LIGGGHTS-PUBLIC 시뮬레이션 튜토리얼 — Shenouda & Hoff (LLNL 기술보고서 2020) | DEM (LIGGGHTS-PUBLIC; AM 분말 흐름/안식각 + 단계별 튜토리얼) | 2026-06-26 | 🖼 25 |
| `song2025_electrochemo_mechanical_microelectrode_ees` | Song 2025 (Energy & Environmental Science 18, 3129-3147) — 미세전극(microelectrode) electrochemo-mechanical 디지털트윈: FIB-SEM 재구성 + 전성분 고유물성 → 셀전압 >98% 검증 + 입자↔셀 괴리 3메커니즘 + 폴리머 바인더 VISCOP | FEM·electrochemo-mechanical | 2026-07-28 | — |

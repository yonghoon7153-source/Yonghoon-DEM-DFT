# 리포 데이터 목록 — 2026-08-25 전수 조사

> 왜: 윈도우 재설치로 webapp 데이터를 잃고 **무엇이 git 에 남아 있나**를 전수로 확인했다.
> 이 파일은 그 조사 결과다.  다음에 같은 사고가 나면 **여기부터 본다**.

> ⚠ 자동 생성 — 행/열 수는 조사 시점 값이다.

## 케이스 표 (복원의 원천)

| 파일 | 행 | 열 | 크기 | 케이스 키 |
|---|---|---|---|---|
| `docs/data/case_master.csv` | 163 | 421 | 485 KB | `case` |
| `docs/data/design_performance_corpus.csv` | 291 | 354 | 2450 KB | `name` |
| `docs/case_summary.csv` | 85 | 308 | 222 KB | `case_id` |
| `docs/data/case_3d_collection.csv` | 155 | 19 | 15 KB | `case` |
| `docs/data/mpm_dem_porosity_reliability.csv` | 117 | 16 | 21 KB | `case` |
| `docs/full_ranking.csv` | 85 | 34 | 18 KB | `—` |
| `validation_all_cases.csv` | 80 | 11 | 6 KB | `—` |
| `all_dem_porosity.csv` | 80 | 14 | 7 KB | `case_id` |

★ **`docs/data/case_master.csv` 가 복원의 정본이다** — 163 케이스 × 421 지표.
  "전체 복사 (AI용)" 로 먹인 내용(입자·접촉·배위수·네트워크·취성·MPM)이 여기 누적돼 있다.

## 그 밖의 CSV (docs/data)

| 파일 | 행 | 열 |
|---|---|---|
| `a3_binder_sweep_2pressure.csv` | 10 | 4 |
| `additive_test_campaign_6mAh_real_4.csv` | 33 | 3 |
| `bazzoun2025_dem_sensitivity.csv` | 107 | 11 |
| `bazzoun2026_S1_replicates.csv` | 15 | 11 |
| `bazzoun2026_sigma_ionic.csv` | 20 | 11 |
| `bielefeld2019_percolation.csv` | 100 | 5 |
| `bielefeld2020_sigma_binder.csv` | 88 | 4 |
| `bucci2017_fracture_czm.csv` | 80 | 7 |
| `bucci2018_delamination.csv` | 54 | 4 |
| `chen2011_percolation_micromodel.csv` | 119 | 6 |
| `cho2024_conflicting_roles_conductive_additive.csv` | 25 | 3 |
| `cronau2021_stack_pressure_ionic.csv` | 27 | 3 |
| `dem3d_dip_sweep.csv` | 15 | 5 |
| `dem_cycling_stresses.csv` | 94 | 8 |
| `dem_design_points.csv` | 132 | 15 |
| `dem_input_values_20260818.csv` | 130 | 37 |
| `densification_porosity_db.csv` | 23 | 11 |
| `deysher2022_review_anchors.csv` | 42 | 8 |
| `dmt_derjaguin1975_adhesion.csv` | 21 | 8 |
| `doux2020_stack_pressure.csv` | 38 | 3 |
| `duquesnoy2023_manufacturing_optimization.csv` | 30 | 3 |
| `electromechanical_contact_model.csv` | 92 | 7 |
| `esse_calibration_2mAh_real_9.csv` | 7 | 16 |
| `frankenberg2024_mixer_stresses.csv` | 81 | 9 |
| `han2025_icep_binder_anchors.csv` | 42 | 9 |
| `heckel_pure_se_dem.csv` | 16 | 5 |
| `heckel_real14_composite_multiP.csv` | 43 | 18 |
| `hong2026_sigma_ionic.csv` | 9 | 7 |
| `huang2025_etc_vs_microstructure.csv` | 67 | 3 |
| `input_2mAh_a7_50_ps_sweep.csv` | 10 | 4 |
| `interfacial_impedance_formulation.csv` | 77 | 7 |
| `intergranular_cracking_nmc811_2023.csv` | 119 | 7 |
| `jacksongreen2005_evolving_hardness_contact.csv` | 60 | 1 |
| `jam_320.csv` | 13 | 7 |
| `jam_320_ps37.csv` | 13 | 7 |
| `jam_320_ps55.csv` | 13 | 7 |
| `jam_512.csv` | 13 | 7 |
| `jam_512_ps37.csv` | 13 | 7 |
| `jam_512_ps55.csv` | 13 | 7 |
| `jung2023_single_crystal_ncm_morphology.csv` | 44 | 8 |
| `kang2025_bimodal_nca_lzo_anchors.csv` | 102 | 4 |
| `kang2025_bollard_binder_anchors.csv` | 67 | 2 |
| `kim2023_chemomech_failure_highstrain_anode.csv` | 114 | 3 |
| `kim2024_carbon_volumetric_occupation_se_domain.csv` | 77 | 4 |
| `kim2025_tlm_kinetics_anchors.csv` | 68 | 4 |
| `klar2016_dp_sand_params.csv` | 26 | 6 |
| `kogut_etsion2002_ep_contact_fits.csv` | 33 | 8 |
| `lee2024_dem_fem_pressure.csv` | 99 | 9 |
| `lee2025_transport_anchors.csv` | 14 | 15 |
| `lhs_design_20260818.csv` | 130 | 39 |
| `liu2025_dryprocess_se_films_cathodes.csv` | 26 | 8 |
| `luding2008_cohesive_frictional_contact_models.csv` | 20 | 11 |
| `lyu2025_drying_calendering.csv` | 55 | 9 |
| `mesarovicfleck2000_dissimilar_elastoplastic_indentation.csv` | 49 | 2 |
| `minnmann2021_sigma_tau_porosity.csv` | 13 | 16 |
| `minnmann2024_porosity_performance.csv` | 46 | 14 |
| `mpm_corner_realizability.csv` | 84 | 10 |
| `mpm_coverage_plastic_vs_rigid.csv` | 2 | 15 |
| `mpm_dpc_heckel_sweep.csv` | 8 | 10 |
| `mun2025_dry_electrode_cell_table.csv` | 25 | 23 |
| `nam2026_primer_si_values.csv` | 69 | 9 |
| `ncm_sc_poly_ds_i0_anchors.csv` | 14 | 10 |
| `ngandjong2021_dem_calendering.csv` | 45 | 9 |
| `nisar2024_sigma_porosity.csv` | 36 | 10 |
| `oh2026_bimodal_sigma_porosity.csv` | 12 | 8 |
| `packing_dip_model.csv` | 21 | 7 |
| `packing_dip_model_ps37.csv` | 21 | 7 |
| `packing_dip_model_ps55.csv` | 21 | 7 |
| `packing_dip_model_ps73.csv` | 21 | 7 |
| `park2020_asse_benchmark.csv` | 19 | 2 |
| `particulate_se_size_sweep.csv` | 17 | 2 |
| `pasha2014_linear_elastoplastic_adhesive_contact.csv` | 35 | 8 |
| `percolation_2d_fit.csv` | 65 | 15 |
| `percolation_2d_fit_v2.csv` | 66 | 11 |
| `porosity_decomposition.csv` | 99 | 12 |
| `porosity_production_final.csv` | 99 | 10 |
| `porosity_regression_predictions.csv` | 35 | 10 |
| `real14_am_scaffold.csv` | 457 | 6 |
| `real14_se_scaffold.csv` | 32832 | 6 |
| `reisacher2023_percolation.csv` | 76 | 5 |
| `rint_eis_anchors.csv` | 36 | 16 |
| `sangros2019_calendering.csv` | 28 | 16 |
| `sangros2020_electrical_paths.csv` | 96 | 4 |
| `sangros2020_lib_electrode_dem_mech_elec_ionic.csv` | 22 | 13 |
| `sc_poly_preset.csv` | 4 | 6 |
| `schneider2023_sigma_size_pressure.csv` | 50 | 3 |
| `schreiner2020_calendering.csv` | 31 | 7 |
| `sdcp_comparison_runs.csv` | 26 | 4 |
| `se_response_real14.csv` | 25 | 2 |
| `shi2019_am_loading.csv` | 106 | 9 |
| `so2021_fabrication_degradation.csv` | 78 | 8 |
| `so2022_coated_particles.csv` | 70 | 4 |
| `so2022_contact_model_params.csv` | 36 | 7 |
| `sr01_carbon_network.csv` | 5 | 26 |
| `sr01_carbon_network_corrected.csv` | 5 | 29 |
| `sr01_realbed_ab.csv` | 5 | 26 |
| `stomakhin2013_mpm_snow_params.csv` | 16 | 6 |
| `storakers1997_similarity_inelastic_contact.csv` | 61 | 2 |
| `tailored_cathode_low_pressure.csv` | 71 | 3 |
| `thakur2014_eepa_adhesive_elastoplastic_dem.csv` | 56 | 8 |
| `thorntonning1998_adhesive_elastoplastic_contact.csv` | 67 | 2 |
| `varkey2026_ionic_vs_pressure.csv` | 7 | 8 |
| `vgcf_dilate_cho_calibrated.csv` | 7 | 2 |
| `wet_processing_resolved_am.csv` | 66 | 9 |
| `yun2023_deciphering_degradation_halide_vs_sulfide.csv` | 102 | 3 |

## 스캐폴드 · 재현 입력

- `dem_scripts/case09_E05x.liggghts` (168 줄)
- `dem_scripts/case09_E15x.liggghts` (168 줄)
- `dem_scripts/particulate12_seed.liggghts` (166 줄)
- `dem_scripts/thin6_seed.liggghts` (172 줄)
- `dem_scripts/thin9_seed.liggghts` (173 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_0_10__am_scaffold.csv.gz` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_0_10__fracture_scaffold.csv.gz` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_0_10__harvest.sh` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_0_10__mpm_input.json` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_0_10__run_a1_anchors.sh` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_0_10__run_mpm.sh` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_0_10__se_scaffold.csv.gz` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_10_0__am_scaffold.csv.gz` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_10_0__fracture_scaffold.csv.gz` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_10_0__harvest.sh` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_10_0__mpm_input.json` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_10_0__run_a1_anchors.sh` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_10_0__run_mpm.sh` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_10_0__se_scaffold.csv.gz` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_3_7__am_scaffold.csv.gz` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_3_7__fracture_scaffold.csv.gz` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_3_7__harvest.sh` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_3_7__mpm_input.json` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_3_7__run_a1_anchors.sh` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_3_7__run_mpm.sh` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_3_7__se_scaffold.csv.gz` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_5_5__am_scaffold.csv.gz` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_5_5__fracture_scaffold.csv.gz` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_5_5__harvest.sh` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_5_5__mpm_input.json` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_5_5__run_a1_anchors.sh` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_5_5__run_mpm.sh` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_5_5__se_scaffold.csv.gz` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_7_3__am_scaffold.csv.gz` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_7_3__fracture_scaffold.csv.gz` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_7_3__harvest.sh` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_7_3__mpm_input.json` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_7_3__run_a1_anchors.sh` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_7_3__run_mpm.sh` (- 줄)
- `docs/data/kit_ps_scaffolds/kit_ps_7_3__se_scaffold.csv.gz` (- 줄)
- `docs/data/real14_am_scaffold.csv` (458 줄)
- `docs/data/real14_se_scaffold.csv` (32833 줄)

⚠ `real14_{am,se}_scaffold.csv` 만 **입자 좌표**를 담는다 (type,x,y,z,r) — 3D 복원 가능한 유일한 케이스.
  `kit_ps_*__mpm_input.json` 은 **지표만** (좌표 없음).

## docs/*.md (정본 서술)

총 162편.

| 파일 | 첫 제목 |
|---|---|
| `CASE_NAMING.md` | Case naming convention reference |
| `Formula_Catalog.md` | Scaling Law Formula Catalog: 전체 시도 수식 목록 |
| `GRADING_STORY.md` | Grading philosophy & weight rationale |
| `PHASE_C_SUMMARY.md` | Phase C — Static figures (Summary) |
| `Packing_Regime_Analysis.md` | Binary Packing Regime Transition Analysis |
| `References_and_Methodology.md` | DEM Simulation Methodology & References Database |
| `Reviewer_Defence_Notes.md` | Reviewer-Defence FAQ Notes — Sensitivity Analyses & Alternative-Value  |
| `Scaling_Law_Report_Full.md` | DEM-Based Ionic Conductivity Scaling Law: Complete Report |
| `TODO_post_stage_e_rerun.md` | Pending: post `find_and_rerun_stage_e.py --all` UI refresh |
| `Tabor_framework_reference.md` | Tabor Elastic-Plastic Framework — Reference & Meeting-Defence Doc |
| `a10_cycle_chemomech_design.md` | A10 — 사이클 chemo-mechanics 설계 (부피변화 → 접촉손실 → σ(N)·R_int(N)) |
| `a1_sigma_e_direction_closeout.md` | A1 — σ_e composition-direction (σ_S/σ_P endpoints): CLOSE-OUT (2026-06 |
| `a1_v2_cycle_ratchet_design.md` | A-1 v2 — 반복사이클 MPM: ★설계 리뷰서 기각 → 재scope (2026-07-23) |
| `a3_binder_sweep_result.md` | A3 PTFE binder sweep — GPU result + honest reframe (2026-06-30) |
| `a3_reflow_calibration.md` | A-3 reflow "캘리브" — ★부분 철회 / 정직 재작성 (2026-07-22, 3렌즈 적대리뷰 후) |
| `a5_a6_metrics_closeout.md` | A5(분산 CoV) + A6(pore-τ) CLOSEOUT — 2026-07-14 |
| `a9_50_ps_sweep_vs_bimodal266.md` | a9_50 P:S sweep — bimodal 최적점 + DEM↔MPM frame[5] 시연 (#266 독립 검증) |
| `additive_process_matrix.md` | Additive × mixing process matrix (the A4 plug-board) — 2026-06-30 |
| `additive_sheath_a14.md` | A14 — surface_conformal SWCNT sheath (제3 도전재 morphology) — 2026-07-21 |
| `additive_test_campaign.md` | 첨가제 테스트 캠페인 — input_6mAh_real_4 (ball-mill, step-by-step) |
| `am_load_balance_and_se_curve_20260805.md` | AM 하중-분담 정지 모델 · SE 응답곡선 재생성 · 다압력 판별실험 (2026-08-05) |
| `automation_result_register.md` | 결과회수 자동화 + 자동 동기화 파이프라인 (MCP/CD) |
| `backlog_solved_vs_todo.md` | Backlog — 해결 vs 잔여 (통합 분류, 2026-07-18) |
| `cbd_morphology_roadmap.md` | CBD / conductive-additive morphology roadmap (PTFE + carbon) |
| `coating_preset_heterotech.md` | 이종기술 코팅 프리셋 (webapp v3, #33) |
| `codex_crosscheck_response_20260807.md` | Codex 교차검증 회답 (2026-08-07) |
| `codex_dem_mpm_response_20260811.md` | Codex 적대리뷰 회답 — DEM–MPM 연계 (2026-08-11) |
| `codex_followup_20260810.md` | Codex 업데이트 팔로우업 — 2026-08-10 |
| `codex_reverification_response_20260807.md` | Codex 재검증 회답 (2026-08-07, 2회차) |
| `codex_review_request_20260811_rc5.md` | Codex 리뷰 요청 — RC5 전건 + thermal 근본수정 + STEP3 (2026-08-11) |
| `codex_review_request_20260811_rc6.md` | Codex 독립검증 요청 — RC6 전건 (2026-08-11, 7회차) |
| `codex_round3_response_20260807.md` | Codex 교차검증 3회차 회답 (2026-08-07) |
| `codex_round4_response_20260807.md` | Codex 교차검증 4회차 회답 (2026-08-07) |
| `codex_round5_response_20260811.md` | Codex 5회차 회답 — RC5 / F-18 (늦은 처리, 2026-08-11) |
| `comsol_trackb_pipeline.md` | Track-B — DEM/MPM → COMSOL 파이프라인 (payload → comsol_pkg → .mph) |
| `contradiction_audit_20260720.md` | 코드/md 모순점 감사 (2026-07-20) |
| `data_inventory_20260825.md` | 리포 데이터 목록 — 2026-08-25 전수 조사 |
| `defense_review_20260720.md` | Defense-grade 초정밀 리뷰 — 2026-07-20 (오늘 작업 전체) |
| `degradation_model_map.md` | 진짜 열화 전극 모델 — 전체 지도 (plain, 2026-07-22) |
| `dem3d_composite_overshielding.md` | 3D DEM composite over-shielding — exhaustive lever screen (2026-06-15) |
| `dem_mpm_coupling_review_request_20260811.md` | DEM–MPM 연계 준비상태 정리 + Codex 리뷰 요청 (2026-08-11) |
| `dem_perturbation_layer.md` | DEM post-compaction PERTURBATION LAYER (`scripts/dem_perturbation.py`) |
| `digest_model_application_backlog.md` | Digest → MODEL APPLICATION backlog (안 적용한 것 추적, LIVING) |
| `eis_drt_ica_cv.md` | v3-1 — EIS / DRT / ICA / CV (물리-기반, `scripts/eis_drt_ica.py`) |
| `electronic_conductivity_derivation.md` | Logical Derivation of the Electronic Conductivity Formula for All-Soli |
| `esse_calibration_2mAh_real_9.md` | E_SE calibration — 2mAh_real_9 (실험 2mAh_9 대응) |
| `fibre_rod_mpm_design.md` | Tier-2: emergent fibre buckling in the MPM (sub-grid rod) — design |
| `fracture_to_mpm_crackvoid.md` | 취성 파괴 → MPM crack-void (초기압밀 균열의 형태적 결과) |
| `handoff_README_liggghts_raw.md` | 후막 복합양극 DEM (LIGGGHTS) raw 데이터 — 인수인계 README |
| `ionic_scaling_law_experiments.md` | Ionic Scaling Law — Troubleshooting Log |
| `joule_hotspot.md` | 29 — Cycle Joule I²R 발열 hot-spot |
| `lab_ai_workflow_conventions.md` | 랩 AI 워크플로 규약 — "AI coding agent 설치 및 활용" 2편 digest (2026-07-16) |
| `lab_weekly_20260727_digest.md` | 랩 주간보고 digest (2026-07-27) — 양수영 ML DB화 + 윤태영 바이모달 ↔ 우리 구현 대조 |
| `lhs_design_dataset_20260818.md` | AI 학습용 DEM 데이터셋 설계 — LHS (2026-08-18) |
| `lit_bak2024_binder_distribution_multilayer.md` | Bak 2024 (Chemical Engineering Journal 483, 148913) — 바인더 z-분포 제어 다층 모 |
| `lit_bazzoun2026_dem_fem_rnm.md` | Bazzoun 2026 (J. Power Sources 661, 238682) — DEM + FEM + RNM 이온전도도 (우 |
| `lit_bielefeld2019_microstructural_modeling_composite_cathodes.md` | Bielefeld 2019 (J. Phys. Chem. C 123, 1626–1634) — 복합 양극 미세구조 모델링 (Jan |
| `lit_bielefeld2020_effective_ionic_conductivity_binder.md` | Bielefeld 2020 (ACS Appl. Mater. Interfaces 12, 12821−12833) — 유효 이온전도 |
| `lit_cho2026_eipc_zn_anode_azib.md` | Cho 2026 (Energy Storage Materials 89 (2026) 105186, DOI 10.1016/j.ens |
| `lit_choi2024_digital_twin_review_echem.md` | Choi 2024 (E.Chem 매거진 총설, Vol.16 No.1) — 디지털 트윈 모델링·시뮬레이션 ★ 우리 DEM+MPM |
| `lit_choi2026_elastomeric_li_metal_anode.md` | Choi 2026 (Advanced Energy Materials, DOI 10.1002/aenm.71104) — 친리튬(li |
| `lit_cronau2021_stack_pressure_ionic_conductivity.md` | Cronau 2021 (ACS Energy Lett. 6, 3072−3077) — Stack-pressure 딜레마: 미세결정 |
| `lit_doux2020_stack_pressure_assb.md` | Doux 2020 (Adv. Energy Mater. 10, 1903253) — Stack Pressure: 작동압력(oper |
| `lit_hong2026_cbd_viscoelasticity_springback.md` | Hong 2026 (Energy Storage Materials, ENSM 105321) — CBD 점탄성이 단결정 catho |
| `lit_hong2026_sulfide_cathode_binder_digitaltwin.md` | Hong 2026 (Energy Storage Materials 86, 104930) — 황화물 복합양극 열화 메커니즘 (디지 |
| `lit_kim2024_digital_twin_acsenergyletters.md` | Kim 2024 (ACS Energy Letters, 동료심사 ORIGINAL) — Digital Twin Battery Mo |
| `lit_kim2025_conductive_agent_se_coating_assb.md` | Kim 2025 (Battery Energy 4, e70044) — SE-coating-on-CAM에 들어가는 도전재(Supe |
| `lit_kim2026_a3d_air_electrode_microstructure_transport.md` | Kim 2026 (Journal of Power Sources 686, 240471) — 디지털트윈 미세구조(GeoDict)  |
| `lit_kim2026_charge_engineered_cnf_binder.md` | Kim 2026 (Nature Communications, DOI 10.1038/s41467-026-73909-0) — 전하조 |
| `lit_koo2025_cnt_wrapped_sc_nca_dry_cathode.md` | Koo 2025 (Energy Storage Materials 78, 104270) — anti-solvent로 MWCNT 감 |
| `lit_koo2026_swcnt_sheath_thick_electrode.md` | Koo 2026 (Joule 10, 102392) — 연속 SWCNT sheath가 두꺼운 dry 전극에서 초고에너지밀도 +  |
| `lit_lee2023_sicspe_digitaltwin_assb.md` | Lee 2023 (Battery Energy 2, 20220061) — 디지털트윈 기반 SIC-SPE vs LPSCl 복합양극 |
| `lit_lee2025_corolling_dryprocess_assb.md` | Lee 2025 (Nat. Commun. 16, 4200) — 건식 co-rolling 공정으로 박막 SSE + 친밀 계면 → |
| `lit_lim2025_virtual_calendering_framework.md` | Lim 2025 (Small 21, 2410485) — Virtual Calendering Framework: 3D-재구성 양 |
| `lit_minnmann2021_jes_charge_transport_bottlenecks.md` | Minnmann 2021 JES — 복합 양극 전하수송 병목 정량화 (EIS-TLM) ★ 우리 porosity/σ_ion/τ_ |
| `lit_minnmann2022_designing_cathodes_solidstate.md` | Minnmann 2022 (Adv. Energy Mater. 12, 2201425) — "Designing Cathodes a |
| `lit_nam2026_dpe_microstructure_review.md` | Nam 2026 (Materials Horizons REVIEW, 13, 3149-3177) — 건식전극(DPE) 미세구조 엔 |
| `lit_oh2026_bimodal_composite_cathode.md` | Oh 2026 (ACS Energy Letters 11, 2103-2114) — Bimodal 복합양극: 큰 다결정 + 작은  |
| `lit_oh2026_carbon_coating_siox_ion_electron_balance.md` | Oh 2026 (Journal of Power Sources 689, 240698) — SiOx 탄소코팅 두께가 이온/전자 수 |
| `lit_park2020_digitaltwin_assb_foundational.md` | Park 2020 (Adv. Energy Mater. 10, 2001563) — Digital-Twin-Driven All-S |
| `lit_park2026_ceramic_pp_separator.md` | Park 2026 (Chemical Engineering Journal 532 (2026) 174523, DOI 10.1016 |
| `lit_park2026_thiolene_sbr_binder_assb.md` | Park 2026 (Adv. Funct. Mater. 36, e16017) — Thiol-Ene Click으로 SBR 바인더  |
| `lit_sakuda2013_sulfide_mechanical_property.md` | 황화물 SE의 "유리한 기계적 물성" — 상온 가압소결·Young's modulus·이온전도도 — Sakuda (Sci. Re |
| `lit_song2025_electrochemo_mechanical_microelectrode_ees.md` | Song 2025 (Energy & Environmental Science 18, 3129-3147) — 미세전극(microe |
| `lit_trevisanello2021_sc_pc_ncm_cracking_diffusion.md` | Trevisanello 2021 (Adv. Energy Mater. 11, 2003400) — 다결정 vs 단결정 NCM: 입 |
| `lit_varkey2026_multicontact_dem.md` | Varkey 2026 (Adv. Powder Tech. 37, 105338) — 다중접촉 탄소성 DEM |
| `lit_yoo2026_porosity_gradient_dry_electrode.md` | Yoo 2026 (Energy Storage Materials, ENSM 105331) — Porosity-구배 건식 흑연 전 |
| `litdb_application_table.md` | litdb → 모델 적용표 (#33 phase-1) — webapp v3 (ML·이종기술) 스코핑 |
| `literature_dry_assb.md` | Literature Archive — Dry-Process / Solvent-Free All-Solid-State Batter |
| `literature_review_dem_mpm_assb.md` | 📖 전고체전지 복합양극 DEM+MPM 모델링 — 문헌 종합 리뷰 |
| `literature_yonsei_dtbl_2026.md` | 연세대 Digital Twin Battery Lab (Yong Min Lee 그룹) — 2026 논문 트리아지 + 우리 모델  |
| `manuscript_sdcp_sigma_e_mechanism.md` | SDCP σ_e 메커니즘 — ⛔ HISTORICAL (2026-07-15 판; 2026-08-13 결론 철회) |
| `ml_application_map_dem_pipeline.md` | ML 적용 지도 — 느린 파이프라인 구간 × TabPFN/랩-ML (2026-07-21) |
| `ml_design_loop.md` | 33 v3 ML: Duquesnoy 설계 폐루프 (`scripts/ml_design_loop.py`) |
| `ml_v3_surrogate_cycling.md` | v3-2/v3-3 — ML 사이클수명 surrogate + 오픈소스 cycling 인제스트 (MLIP식) |
| `mpm3d_calibration.md` | 3D MPM compaction — calibration & composite finding (2026-06-16) |
| `mpm_coverage_plastic_vs_rigid.md` | MPM coverage — PLASTIC vs RIGID: why the values are usable (2026-06-21 |
| `mpm_dem_wallP_crossvalidation.md` | DEM ↔ MPM per-case cross-validation @ 512 — wallP boundary-load readou |
| `mpm_dip_resolution_invariance.md` | Furnas dip — resolution-invariant measurement (2026-06-07) |
| `mpm_dpc_cap_crosscheck.md` | DPC volumetric cap × resolved-grain MPM — cross-check (FINDING) |
| `mpm_lpscl_compaction_summary.md` | MPM LPSCl 2D compaction — consolidated summary (2026-06-08) |
| `mpm_platen_kinematic_stop_defect.md` | MPM scaffold 압밀 — 플래튼 비준정적 하강 결함 |
| `mpm_scaffold_reliability_and_am_freeze.md` | MPM scaffold — AM-freeze 근거 + porosity 신뢰성 regime map (절대값 · 트랜드) |
| `mpm_wallP_conditional_troubleshooting.md` | TROUBLESHOOTING — scaffold MPM SE-poor over-compression → wallP 조건부 fi |
| `nca_material_preset.md` | A8 — NCA(Ni₀.₈₈) CAM 재료 프리셋: 물성 출처-교차검증 + 배선 결정 (2026-07-21) |
| `ncm_sc_poly_electrochem_anchors.md` | NMC811 소립 단결정(SC) vs 대립 다결정(PC) 전기화학 앵커 — D_s · i0 |
| `paper_brittle_caveat.md` | Paper Caveat — Brittle Reframe Framework |
| `phase_b_pipeline_provenance_20260807.md` | Phase B 구현 기록 — network/Stage E 세대 분리 (2026-08-07) |
| `pipeline_step1_to_step5_guide.md` | 황화물 전고체전지 양극 통합 시뮬레이션 — STEP1 → STEP5 최종 설명서 |
| `plan_se_grad_20260811.md` | 계획서 — `--se-grad`: SE 조성 구배 (Luan 2025 → Phase 5 / A7 확장) |
| `plan_vgcf_ptfe_coupling_20260811.md` | 계획서 — Zhang/Meng/Franco 2026 (Nature Energy) 를 우리 첨가제 모델에 반영할 것인가 |
| `porosity_regression_final.md` | 전극 공극률(Porosity) 회귀식 — 문헌 기반 다차원 모델 |
| `porosity_subum_se_investigation.md` | sub-µm SE 크기효과 — 응집 sigmoid 가설 검증 (REFUTED) |
| `porosity_wave_shape_physics.md` | Porosity Wave-Shape Physics Decomposition |
| `positioning_in_dt_lineage.md` | 디지털트윈 전극 계보 안에서 우리의 자리 |
| `positioning_vs_geodict.md` | Positioning — 우리 DEM+MPM 파이프라인 vs GeoDict (상용) — "돈 내고 쓰는 GeoDict 이상" |
| `post_porosity_roadmap.md` | Post-porosity roadmap — DEM/모델 개선 + PTFE/VGCF/SuperP webapp + dem-anal |
| `project_ceramic_catholyte_singlecrystal.md` | 국책과제 컨텍스트 — 세라믹 catholyte 기반 단결정 양극재 후막전극 (RS-2025-25463211) |
| `project_rint_fullcell_cycling.md` | PROJECT — 집전체 계면저항(R_int) + 측정-앵커 풀셀/사이클 모델 확장 |
| `ps_series_t60_op90_preregistration.md` | P:S 5종 시리즈 (T60°C · P_op 90 MPa · VGCF1+PTFE1) — 사전등록 |
| `ptfe_binder_bridge_degradation.md` | PTFE 바인더-브릿지 열화 (#31) — F1-style OFF 기본 튜너블 훅 |
| `real_degrading_electrode_design.md` | 진짜 열화하는 전극(real degrading electrode) — 하이브리드 사이클 chemo-mech 설계 |
| `remaining_work_survey_20260724.md` | 남은 작업 종합 서베이 (2026-07-24, 5-스캐너 워크플로 wf_17cb6734) |
| `report_mpm_and_sigma_usability_20260819.md` | MPM 과 유효전도도 — 지금 무엇을 쓸 수 있는가 (2026-08-19 보고) |
| `review_20260730_temperature_cycle_axis.md` | 온도·사이클열화 축 적대리뷰 (2026-07-30, HEAD baf34936) |
| `rint_anchor_db_research.md` | Phase 0 — R_int/EIS/cycling 앵커 조사 결과 (2026-07-20) |
| `rint_reference_growthlaw_design.md` | 문헌-앵커 generalizable reference R_int(N) 설계 (Phase 1) |
| `sdcp_318_base_sbe_dbe_comparison.md` | 3.18mAh 실조성 세트 — base / SBE / DBE 전수 비교 (2026-07-15; ⛔ 해석 부분 2026-08-1 |
| `sdcp_manuscript_anchors.md` | SDCP 매뉴스크립트 앵커 (Figures_v7, 2026-07-09 추출) — 모델 재배선 근거 |
| `sdcp_master.md` | SDCP 통합 마스터 문서 |
| `se_curve_transfer_verdict_20260806.md` | SE 응답곡선 σ(φ) — 베드-전이 검증 결과 (2026-08-06) |
| `seminar_20260806_glossary.md` | 세미나 용어·기호 규약 + 레퍼런스 (2026-08) |
| `seminar_20260806_script.md` | Research Seminar 2026-08 — 슬라이드 대본 + Defense 준비 (초안 v2) |
| `server_bootstrap_runbook.md` | 서버 부트스트랩 런북 — GPU 인스턴스 껐다 켤 때마다 이것만 (2026-07-27 정본) |
| `server_setup.md` | New-server setup — DEM (LIGGGHTS) + MPM (Taichi) + Python + webapp |
| `session_20260723_overnight_progress.md` | 2026-07-23 오버나잇 세션 진행 (정본) |
| `session_20260723_progress.md` | 진행 브리핑 — 2026-07-23 세션 (branch: claude/stoic-knuth-NObVQ) |
| `session_20260811_progress.md` | 세션 진행 원장 — 2026-08-11 (compact 전 스냅샷) |
| `session_20260819_litdb_pending.md` | 진행 중 — litdb 정본 4편 작업 (2026-08-19, 압축 대비 스냅샷) |
| `sigma_e_stage21_history.md` | Stage 21 FINALIZED — CLAUDE.md 에서 발췌한 전문 |
| `sigma_ionic_physics_derivation.md` | σ_ionic Production Form — Physical Derivation |
| `stage2_model_audit_vs_literature.md` | Stage-2 모델 하자 감사 (audit) — Yonsei DTBL 2026 + 관련 문헌 대조 |
| `stage4_electrochem_research.md` | Stage 4 — electrochemical cell simulation (DFN) research foundation |
| `step3_sigma_network.md` | STEP3 v1 — 전자전도 voxel 저항망 (σ_e_eff + 입자별 전류밀도) |
| `step4_ac_solve_design.md` | STEP4 완전 AC-solve 설계 (미세구조-해상 EIS, 연구트랙 킥오프 2026-07-24) |
| `step4_acceleration_literature_20260803.md` | STEP4 가속 — 문헌 조사 (2026-08-03) |
| `step4_assb_window_review.md` | STEP4 방전창(x0/x100) — ASSB vs-Li 재산정 리뷰 + 준비 (PENDING) |
| `step4_bottleneck_analysis_20260727.md` | STEP4 2C 병목 해부 — near-null 근본원인 · 게이트 정정 · 치료 레이어링 (2026-07-27) |
| `step4_reaction_current.md` | STEP4-v1 — 저율 충전 반응전류 분포 (랩 slide-20 물리판) |
| `step4_v2_design.md` | STEP4-v2 설계 — 시간적분 + 구형확산 + 비선형 BV (voxel-DFN, SSB) (2026-07-15 구현 현행판 |
| `step4_v2_explainer_for_students.md` | STEP4-v2 충방전 시뮬레이션 — 처음 보는 사람을 위한 해설서 |
| `step5_cycle_degradation.md` | STEP5 — 사이클 열화 (cycle degradation): "진짜 열화 전극" (정의 2026-07-23) |
| `step6_surrogate_design.md` | scripts/step6_surrogate.py v1 설계·구현 기록 — MLIP식 전기화학 surrogate (STEP6) |
| `sulfide_se_mechanical_anchors.md` | 황화물 SE 기계 안정성 — Fan 2026 §3.5 를 우리 모델에 맞춰본 기록 (2026-08-06) |
| `symposium_2026_kbs_digest.md` | 2026 전지기술 심포지엄 digest — 이용민(연세대) · 문장혁(중앙대) |
| `temp_pressure_capability.md` | 온도·압력 대응 능력 감사 (Temperature / Pressure Capability Audit) |
| `thermal_conductivity_derivation.md` | Logical Derivation of the Thermal Conductivity Formula for All-Solid-S |
| `v100_step4_handoff.md` | STEP 4 격자 스윕 — 메모리 예산 + (예비) V100 이관 (2026-08-18) |
| `v29_formula_terms.md` | v29 FINAL Formula — 각 항의 물리적 의미와 함수 형태 |
| `vgcf_carbon_catalyzed_se_decomposition.md` | VGCF carbon-촉매 SE 분해 → STEP5 화학열화 (#30) |
| `voxel_conductivity_crossvalidation.md` | Voxel σ solver ↔ DEM network solver — frame[4] cross-validation (AMS_S |
| `zip_physics_audit.md` | Additive recipe → MPM-input (zip) physics audit — 2026-06-30 |

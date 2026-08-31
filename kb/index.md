# kb 카탈로그 (생성물 — 손으로 고치지 말 것)

> `python3 tools/kb_wiki.py index` 가 만든다 · 2026-08-31 · managed-files: 318

규칙: kb/SCHEMA.md · 열린 질문: kb/questions/ · 논지 카드: kb/syntheses/ · 원장: kb/open_items.md · 문헌: litdb/INDEX.md

## concepts/ (11)
- `kb/concepts/bandgap.md` — Band gap — 밴드 갭 (전자 밴드 간극)
- `kb/concepts/beta-gate.md` — β 게이트 — 확산영역 판정 (diffusive-regime gate)
- `kb/concepts/bvse.md` — BVSE — Bond Valence Site Energy (결합가 자리 에너지)
- `kb/concepts/cohp.md` — COHP / ICOHP / ICOBI — 결합 분석 (Crystal Orbital 재투영)
- `kb/concepts/dft.md` — DFT — Density Functional Theory (밀도범함수이론)
- `kb/concepts/elastic.md` — Elastic constants — 탄성상수 $C_{ij}$ 와 VRH 평균
- `kb/concepts/md.md` — MD (MLIP) / MSD / Arrhenius — 분자동역학 이온수송
- `kb/concepts/neb.md` — NEB / CI-NEB — 최소에너지경로 (Nudged Elastic Band)
- `kb/concepts/ordered_vs_disordered.md` — Ordered vs Disordered — 어떤 LPSCl 구조로 계산할 것인가
- `kb/concepts/oxidation_vs_mechanical.md` — 산화안정성과 기계적물성 — 정의부터 DFT 계산까지 ○미열람
- `kb/concepts/sdcp_self_doping_explainer_2026_08_26.md` — 자기도핑(self-doping)이란 무엇인가 — 프로톤이 아니라 수소 원자를 뗀다 ○미열람

## physics/ (6)
- `kb/physics/260617_Nd2O3_doping_bandgap_narrowing_mechanism.md` — Nd₂O₃ 도핑 LPSCl 밴드갭: 왜 O 도핑인데 갭이 좁아지나
- `kb/physics/br_substitution_effects.md` — Br Substitution Effects on Argyrodite Mechanical Properties
- `kb/physics/li_ordering_sensitivity.md` — Li Ordering Sensitivity
- `kb/physics/nd_4f_doping_consolidated_corrected_2026_06_24.md` — Nd / 란탄족 4f 도핑 — 통합·교정 노트 (March 개념노트 + June DFT/MP 결합)
- `kb/physics/vacancy_effects.md` — Vacancy Effects in Argyrodite
- `kb/physics/vacancy_mechanism_corrected_2026_05_08.md` — Vacancy + Halogen Distribution → Adhesion: Corrected Mechanism

## methodology/ (48)
- `kb/methodology/PHASE1_QUICKSTART_doping.md` — Phase 1 Quickstart Guide
- `kb/methodology/adhesion_calibration_decision_2026_05_17.md` — Adhesion Calibration Decision — 2026-05-17
- `kb/methodology/adhesion_energy.md` — Adhesion Energy (Wad) Calculation
- `kb/methodology/adhesion_methods_comparison.md` — Adhesion Methods Comparison — v2 / v5 crystalline / MQA 500K
- `kb/methodology/agent_toolkit_adoption_2026_08_11.md` — 외부 에이전트 툴킷 3종(ponytail · caveman · superpowers) 검토와 선별 채택 ○미열람
- `kb/methodology/argyrodite_mechanical_pipeline.md` — Argyrodite Mechanical Properties — Multi-scale Computational Pipeline (v2)
- `kb/methodology/b2o3_analysis_plan.md` — B₂O₃-doped champion — 추가 분석 plan (배위·결합·testable)
- `kb/methodology/b2o3_doping_chemistry.md` — B2O3 Doping in LPSCl1.6 (BO-LPSC) — Chemistry Framework
- `kb/methodology/beta_gate_seed_policy.md` — 확산영역 게이트(β)와 시드 정책 — 언제 시드를 더 넣어도 되나
- `kb/methodology/cascade_composition_family_2026_08_16.md` — 캐스케이드 조성족 섞임 — 보편적 Cl 개선은 반증, 원소 수준 인과는 여전히 열림 ○미열람
- `kb/methodology/cascade_design_contract_2026_08_28.md` — cascade 3,615행은 237설계였다 — 표본 계약을 다시 쓴다 ○미열람
- `kb/methodology/cascade_pipeline_anatomy_2026_08_13.md` — cascade 273 캠페인 해부 — 왜 풀이 47인가 (코드 계보 실측) ○미열람
- `kb/methodology/cascade_rerank_runbook_2026_08_25.md` — cascade 재랭킹 런북 ①~⑤ — li_mobility_score 복구 후 실행 ○미열람
- `kb/methodology/coating_descriptor_catalog.md` — 황화물 코팅 소재 Descriptor Catalog
- `kb/methodology/computational_methods_canonical.md` — 계산 방법 Canonical — 단일 기준 (2026-07-23 재정리 · **2026-08-20 축 4개 추가**)
- `kb/methodology/defect_cell_size_metric_2026_08_16.md` — 점결함 셀 크기의 정본 지표 — λ₁(최단 격자 병진), 면 높이 아님 ○미열람
- `kb/methodology/dopant_screening_funnel_2026_06_13.md` — Dopant screening funnel provenance + multi-cation motif generalization
- `kb/methodology/dopant_site_preference_literature.md` — Dopant Site Preference — Literature-Anchored Heuristic Assignments (v4.5.26)
- `kb/methodology/doping_pipeline_critical_review.md` — Doping Pipeline — Critical Self-Review (2026-05-16, v4 championship)
- `kb/methodology/doping_substitution_algorithm.md` — LPSCl 도핑 / 치환 알고리즘
- `kb/methodology/elastic_constants.md` — Elastic Constants Calculation
- `kb/methodology/electron_localization_framework_2026_07_08.md` — 전자 국소화 프레임워크 — LPSCl이 작동하는 이유, B₂O₃ 도핑이 그것을 강화하는 방식
- `kb/methodology/eos_fitting.md` — EOS Fitting — Birch-Murnaghan Equation of State
- `kb/methodology/esp_z590_setup.md` — esp-Z590-AORUS-MASTER Server Setup (new home/lab server)
- `kb/methodology/estimand_before_running_2026_08_28.md` — 여덟 번 계산하고 여덟 번 반려된 이유 — 우리는 '제대로 돌렸나'만 리뷰했다 ○미열람
- `kb/methodology/esw_grandpotential_staircase_explained.md` — 전기화학 안정성 창(ESW) — 전압별 분해 staircase 완전 해설
- `kb/methodology/external_review_response_2026_05_16.md` — External Review Response (2026-05-16)
- `kb/methodology/handoff_2026_08_20_night.md` — 인수인계 2026-08-20 밤 — 밤새 도는 것 · 아침에 볼 것 ○미열람
- `kb/methodology/hard_dopant_handling_protocol.md` — Hard / Compound Dopant Handling Protocol (doping cascade)
- `kb/methodology/kisti_setup.md` — KISTI Neuron — Software Installation & Environment Guide
- `kb/methodology/kserver116_setup.md` — kserver116-27 Server Setup (new lab server)
- `kb/methodology/li3nd_metal_protocol_note_2026_08_11.md` — Li₃Nd 독자 계산 — 착수 전 프로토콜 점검 (금속 · frozen-4f)
- `kb/methodology/li_adatom_neb_protocol.md` — Li Adatom Diffusion NEB Protocol — UMA + DFT Verification
- `kb/methodology/li_annealing.md` — Li Annealing — Thermal Li Sublattice Re-optimization
- `kb/methodology/litdb_shared_branch_convention_2026_08_19.md` — litdb 는 브랜치를 넘어 공유된다 — DEM 세션과 같은 서랍을 쓴다 ○미열람
- `kb/methodology/llm_wiki_adoption_2026_08_11.md` — LLM 위키 규율 채택 기록 — Karpathy 패턴(llm-wiki-kit 260730)의 이 repo 번안 ○미열람
- `kb/methodology/md_adaptive_v2_protocol_2026_08_27.md` — MD 생산길이 표준 — `MDadaptive-v2` (200 ps 고정을 순차 연장으로 바꾼다) ○미열람
- `kb/methodology/md_conductivity_protocol.md` — MD 이온전도도 추출 프로토콜 (논문용 — 고정 설정)
- `kb/methodology/microstructure_ml_transfer_to_cascade_2026_08_25.md` — 미세구조 ML 세미나에서 cascade 로 이전 가능한 것 — 화학이 아니라 설계·평가 방법론 ○미열람
- `kb/methodology/modelC_v2_slab_fix.md` — modelC v2 Slab Construction — Convention Fix
- `kb/methodology/nd_vs_O_isolation_campaign_2026_06_18.md` — Nd vs O 분리 — "Nd가 특별한가, O 운반체일 뿐인가" 정량 캠페인
- `kb/methodology/offline_archive_index_2026_08_20.md` — 오프라인 백업 인덱스 — repo 밖에 있는 원자료가 어디 있나 ○미열람
- `kb/methodology/probe_language_reference.md` — Probe 언어 레퍼런스 — 각 계산이 무엇이고, 어떻게 구하고, 논문/figure에 어떻게 쓰는가
- `kb/methodology/ps4_libration_dopant_2026_08_28.md` — T16 — PS₄ 는 안 돈다(재확인). 그런데 **+O 가 흔들림 원뿔을 좁힌다**(신규) ○미열람
- `kb/methodology/selftest_blind_spots_2026_08_28.md` — selftest 를 통과한 채 나간 버그 9건 — 우리 테스트가 못 보는 네 곳 ○미열람
- `kb/methodology/site_preference_protocol_2026_08_11.md` — LiNiO₂(104) 자리 선호 · 자세 스크리닝 프로토콜 v1
- `kb/methodology/terminology_register.md` — 🗣 용어 대장 — 우리 말 → 필드 표준어 → 근거
- `kb/methodology/vanhove_plateau_70traj_2026_08_28.md` — van Hove 70궤적 — 고원은 세 계 공통이고, 고원 안 온도차는 대부분 못 읽는다 ○미열람

## results/ (93)
- `kb/results/MASTER_structure_property_logic_2026_06_21.md` — Structure–Property Relationship of Argyrodite SEs — 통합 논리 (MASTER)
- `kb/results/adhesion_100seeds_analysis.md` — Adhesion Energy — Complete Analysis (2026-04-17)
- `kb/results/adhesion_final.md` — Adhesion Energy — Final Results (2026-04-14, CONFIRMED)
- `kb/results/adhesion_methodology_detail.md` — Adhesion Calculation — Detailed Methodology
- `kb/results/adhesion_troubleshooting.md` — Adhesion Troubleshooting Log
- `kb/results/adhesion_v23_v24_v25_extraction_complete.md` — Adhesion v23-v25 Maximum Extraction — Complete (2026-05-07)
- `kb/results/adhesion_v26_method_stresstest_2026_05_07.md` — Adhesion v26 + v26b — All Method Stress-Test (2026-05-07)
- `kb/results/adhesion_v5_full_report.md` — Adhesion v5 — Crystalline Slab xy-shift 방법론 상세 보고서
- `kb/results/adhesion_v9_to_v22_session_2026_05_07.md` — Adhesion Method Iteration v9-v22 — Session Report (2026-05-07)
- `kb/results/argyrodite_literature_review_2026_06_26.md` — Argyrodite 황화물 고체전해질 — 문헌 종합 리뷰 + 우리 DFT 프로그램 적용 맵 (2026-06-26)
- `kb/results/argyrodite_review_comprehensive_2026_06_26.md` — Lithium Argyrodite 황화물 고체전해질: 구조–수송–안정성–계면–기계의 통합 리뷰
- `kb/results/b2o3_SEMIFINAL_report_2026_07_09.md` — B₂O₃-doped LPSCl1.6 챔피언 — Semi-Final 통합 보고서
- `kb/results/b2o3_anode_interface_2026_06_30.md` — B₂O₃-doped 챔피언의 anode 계면 안정성 — Li-metal에선 **악화**, Li-In에선 **완화**
- `kb/results/b2o3_anode_interface_MD_dynamics_2026_07_06.md` — B₂O₃ champion — anode 계면 **동역학** MLIP-MD: 도핑이 Li-metal 분해를 **억제** (열역학 worst-case 반전)
- `kb/results/b2o3_anode_interface_campaign_2026_07_07.md` — B₂O₃ anode 계면 — 통제 campaign 확정판: **"6× 억제" 철회**, 도핑 ≈ 무도핑(악화 없음), BS₃ 강건·LiB 없음
- `kb/results/b2o3_arrhenius_curvature_2026_08_23.md` — b2o3 아레니우스가 800 K 위에서 굽는다 — 단일 Ea 를 철회한다 ○미열람
- `kb/results/b2o3_bond_lengths_2026_06_29.md` — B₂O₃-doped LPSCl1.6 챔피언의 결합길이 분석 (+ 4a/4d Cl 부분별 Li–Cl)
- `kb/results/b2o3_bvse_channel_2026_07_02.md` — B₂O₃ 도핑 → Li 채널 확장 (BVSE, b2o3 vs LPSCl1.6)
- `kb/results/b2o3_cdd_2026_07_02.md` — B₂O₃ 챔피언 — CDD 전하밀도차 (슬라이드 24의 b2o3 판)
- `kb/results/b2o3_champion_coordination_2026_06_29.md` — B₂O₃-doped LPSCl 챔피언 구조의 국소 배위: 삼각 BS₃ + free-S + phosphate P–O
- `kb/results/b2o3_champion_status_2026_07_03.md` — B₂O₃ Champion — 작업 현황 (2026-07-03)
- `kb/results/b2o3_charge_bader_lowdin_2026_06_30.md` — B₂O₃-doped 챔피언 — Bader + Löwdin 전하 → 산화상태 + XPS BE 경향
- `kb/results/b2o3_convex_hull_2026_06_29.md` — B₂O₃-doped LPSCl1.6 convex-hull 안정성: 준안정(37.5 meV/atom), 분해산물이 BS₃를 예측
- `kb/results/b2o3_elastic_analysis_2026_07_03.md` — B₂O₃ Champion — 탄성상수(Cij) 분석과 한계 (2026-07-03)
- `kb/results/b2o3_elf_covalency_2026_07_02.md` — B₂O₃ 챔피언 — ELF 결합 공유결합성 (슬라이드 19의 b2o3 판)
- `kb/results/b2o3_interface_window_integrated_2026_06_30.md` — B₂O₃-doped 챔피언 — anode(Li, Li-In) + cathode 계면을 **하나의 전기화학 창**으로 통합
- `kb/results/b2o3_md_600K_multiseed_2026_07_02.md` — B₂O₃ MD 이온전도도 — 600K 다중시드 error bar (Ea = 0.21 ± 0.03 eV)
- `kb/results/b2o3_phonon_stability_2026_06_30.md` — B₂O₃-doped LPSCl1.6 챔피언의 동역학적 안정성 (UMA Γ-point phonon)
- `kb/results/b2o3_voronoi_disorder_2026_07_02.md` — B₂O₃-doped 챔피언 — Voronoi 부피 disorder 분석 (slide 9/17의 b2o3 판)
- `kb/results/b2o3_vs_lpscl16_md_2026_07_02.md` — B₂O₃-doped vs LPSCl1.6 — MD 이온수송 종합 비교 (아레니우스·전도도·D분해·저온)
- `kb/results/branch_state_2026_08_30.md` — 브랜치 현황 지도 2026-08-30 — 지금 살아 있는 것과 죽어 있는 것 ○미열람
- `kb/results/bvse_3system_conclusions_2026_07_21.md` — BVSE 3-시스템 결론 — LPSCl1.6 / LPSOCl(+O) / +B₂O₃ (2026-07-21 확정)
- `kb/results/bvse_cubic_approx_2026_07_16.md` — BVSE 큐빅 근사 — "이상화 셀" 지적 대응 + LPSOCl 첫 BVSE (2026-07-16)
- `kb/results/cascade_v23_literature_grounding_2026_06_25.md` — Cascade v23 — 문헌 기반 검증·novelty·reconciliation (2026-06-25)
- `kb/results/champion_pool_size_bias_2026_08_18.md` — 챔피언 점수는 후보를 몇 개 뽑았느냐에 지배된다 — best-of-N 편향이 종간 산포보다 크다 ○미열람
- `kb/results/comp1_supercell_md_reassessment_2026_08_20.md` — comp1 2×2×2 MD 궤적 재판정 — 밴을 풀었다 (정본 승격은 아니다) ○미열람
- `kb/results/deck_ionic_section_additions.md` — Slides 4–7 (Ionic conductivity) — 추가 슬라이드 콘텐츠 (2026-06-21)
- `kb/results/doping_273_qa_log.md` — 273 Doping Cascade — QA Log
- `kb/results/dualx_blocking_2026_06_29.md` — dual-x 도핑 농도 스크리닝: Li-channel blocking_fraction (x=0.0625 vs 0.25)
- `kb/results/elastic_0K_protocol_status.md` — 0K Cij DFT Protocol Status (Paper #1)
- `kb/results/halogen_wad_refutation.md` — Wad Mechanism Refutation — 직관적 설명
- `kb/results/handoff_2026_08_29_stage_a.md` — 인수인계 2026-08-29 — Stage A 제출·회수 (보조 세션용) ○미열람
- `kb/results/interface_axes_90_2026_08_19.md` — 계면 축 4종을 90종에 붙였다 — 우리 산화 창은 계면을 예측하지 못한다 ○미열람
- `kb/results/interface_reactivity_v2_voltage_resolved_2026_06_21.md` — Voltage-resolved SE/cathode interface reactivity (v2) — 2026-06-21
- `kb/results/ionic_cage_descriptors_comp1_modelc.md` — LPSCl vs LPSCl1.6 — ionic conductivity, NEB-free geometric descriptors
- `kb/results/ionic_conductivity_full_explained_2026_06_21.md` — 이온전도도 완전 정리 — LPSCl(comp1) vs LPSCl₁.₆(modelc)
- `kb/results/ionic_conductivity_synthesis_comp1_modelc.md` — Ionic conductivity: LPSCl (comp1) vs LPSCl1.6 (modelC) — full synthesis
- `kb/results/li3nd_endpoint_asymmetry_2026_08_12.md` — li3nd NEB 끝점 2.07 eV — 수치 인공물이 아니라 실제 자리 차이 ○미열람
- `kb/results/li_interface_md_takeaways_2026_07_08.md` — Li|전해질 계면 MD — 이 시뮬레이션에서 우리가 얻은 것
- `kb/results/li_neb_anode_free_report.md` — Li Adatom Diffusion on Anode-Free SSB Interphases — Li3N vs LiC6
- `kb/results/litdb_aimd_survey_2026_08_04.md` — litdb AIMD 전수 조사 — "문헌 AIMD는 몇 ps를 돌았나" (2026-08-04)
- `kb/results/litdb_session_map_2026_06_26.md` — litdb 세션 맵 (2026-06-26) — deck/논문용 1장 인덱스
- `kb/results/lpscl_structural_analysis_v3.md` — LPSCl vs LPSCl1.6 — 구조/결합 정밀 분석 (v3, DFT V0)
- `kb/results/lpscl_vs_lpscl16_FULL_report_2026_06_17.md` — LPSCl (comp1) vs LPSCl1.6 (modelC) — 종합 비교 보고
- `kb/results/lpscl_vs_lpscl16_v3_comparison.md` — LPSCl vs LPSCl1.6 — v3 완성형 비교 (Pipeline v2 §8)
- `kb/results/lpsocl_box_size_600K_2026_08_18.md` — LPSOCl 600 K 상자 크기 — D 는 1.5~1.7× 눌렸고, β 는 MTO 잣대에서 +0.05 움직인다 ○미열람
- `kb/results/manuscript_dft_today_2026_08_29.md` — 오늘 원고에 넣을 수 있는 DFT 문장 — 새 계산 없이 ○미열람
- `kb/results/md_beta_estimator_disagreement_2026_08_25.md` — β 는 시간·이온 대조를 못 가른다 — MTO/STO 가 순위를 뒤집는다 ○미열람
- `kb/results/mlip_md_diffusive_gate_2026_08_01.md` — MLIP-MD 확산영역 게이트 — 저이동도 계의 Ea 는 전부 인용 보류 (2026-08-01)
- `kb/results/nd2o3_FINAL_summary_2026_06_24.md` — Nd₂O₃-doped LPSCl1.6 — **최종 종합 (FINAL capstone)**
- `kb/results/nd2o3_O_effect_transfer_2026_06_24.md` — Nd₂O₃-LPSCl1.6 — **O 효과 중심** 정리 (transfer용)
- `kb/results/nd2o3_master_findings_2026_06_18.md` — Nd₂O₃-LPSCl1.6 — 종합 결과 + 메커니즘 (master findings, 문헌 매핑)
- `kb/results/nd_anode_cathode_sei_formation_2026_06_24.md` — 음극향·양극향 SEI 이점 — **formation energy로 본 산물 선택** (Nd₂O₃-LPSCl1.6)
- `kb/results/nd_oxidation_onset_honest_2026_06_24.md` — Nd₂O₃ 도핑 — 산화안정성 cost vs SEI passivation 이점 (정직한 정리)
- `kb/results/nd_xps_literature_basis_2026_06_30.md` — Nd 3d XPS — 왜 DFT로 못 구하고 문헌(실험)값을 쓰는가 + 확실한 출처
- `kb/results/neb_cell_size_trend_2026_08_20.md` — NEB 셀 크기 추세 — 작은 셀이 장벽을 1.3~3.3배 부풀린다 (UMA 정찰 6홉/4화합물) ○미열람
- `kb/results/oxidation_stability_VBM_vs_grandpotential_report_2026_06_18.md` — 보고서 — 산화안정성: VBM/UPS가 아니라 Grand-Potential 분해창으로 평가 (LPSCl vs LPSCl1.6)
- `kb/results/paper_figure_plan_v3.md` — Paper Figure / Table Plan — LPSCl vs LPSCl1.6 v3
- `kb/results/presentation_script_BVSE_ionic_2026_06_19.md` — 발표 스크립트 — 이온전도성: BVSE로 본 anti-site Cl 효과 (DFT 슬라이드)
- `kb/results/presentation_script_LPSCl_vs_LPSCl16_2026_06_18.md` — 발표·보고용 스크립트 — LPSCl vs LPSCl1.6 (16 슬라이드, 상세판)
- `kb/results/redox_orbital_control_PS4_vs_BS3_2026_07_08.md` — 왜 P–S만 끊기고 B–S/P–O는 사는가 — σ\* 궤도 제어 (환원분해의 미시 메커니즘)
- `kb/results/report_mechanical_electronic_2026_06_21.md` — 보고용 정리 (2026-06-21) — 역학·전자밀도 descriptor + 구조 + 시각화 가능성
- `kb/results/screen_volume_vs_energy_2026_08_18.md` — 부피로 떨어뜨린 100개가 "에너지로는 멀쩡한" 진짜 이유 — 조성 섞임이지 구조가 아니다 ○미열람
- `kb/results/sdcp_linio2_binding_report.md` — SDCP Binder Anchoring on LiNiO₂ (104)
- `kb/results/sdcp_master_summary_2026_07_16.md` — SDCP 종합 정리 — 오비탈 · 작용기 · DFT (마스터)
- `kb/results/sdcp_ptfe_site_screen_summary_2026_08_11.md` — 자리 선호 스크리닝 — UMA 로 무엇을 봤고, 왜 값이 안 나왔고, VASP 에 무엇을 넘겼나
- `kb/results/sdcp_slab_plateau_broken_2026_08_03.md` — SDCP 슬랩 plateau 를 깼다 — 원인은 계가 아니라 Broyden 이력 (2026-08-03)
- `kb/results/sdcp_wave1_citable_2026_08_25.md` — SDCP wave1 인용 확정본 — 논문에 쓰는 값 한 장 (basin 일치분) ○미열람
- `kb/results/sdcp_wave1_explainer_2026_08_25.md` — SDCP wave1 결과 읽는 법 — 바인더가 NCM 표면 어디에 붙나 ○미열람
- `kb/results/sdcp_wave1_vasp_return_2026_08_25.md` — SDCP wave1 VASP 회신 — 자기 basin 이 갈랐다 (E_ads · 자리선호) ○미열람
- `kb/results/section1_system_design.md` — Section 1 (Deep Dive) — 시스템 설계의 과학적 논리
- `kb/results/section2_bader_cross_comp.md` — Section 2 — Bader Charge Cross-Composition: 4 Trends + 3 Anomaly Fingerprints + Br Effect on PS₄
- `kb/results/sei_cc333_nd_lattice_hop_2026_08_17.md` — cc333 — 같은 c-c 홉이 맞다. 3×3×3 에서 Nd 격자 재배열이 풀린다 ○미열람
- `kb/results/session_handoff_2026_07_22.md` — 세션 핸드오프 — 2026-07-21 밤 → 07-22 새벽
- `kb/results/session_timelog_2026_06_04.md` — Session Timelog — 2026-06-04/05 (multi-track)
- `kb/results/single_li_neb_invalid_argyrodite_2026_08_21.md` — 무질서 Li₆PS₅Cl 에서 단일 Li NEB 는 성립하지 않는다 — 세 설정으로 확인 ○미열람
- `kb/results/site_preference_bar_meaning_2026_08_18.md` — 자리 선호 그림의 막대는 시드가 아니라 도핑 수준이다 — 그리고 6종은 자리가 바뀐다 ○미열람
- `kb/results/site_preference_findings_2026_06_19.md` — Dopant site preference (antisite-swap, all-UMA) — 81-system screen
- `kb/results/site_thermodynamics_explained.md` — Site Distribution Thermodynamics — 왜 각 comp가 그 분포로 가장 안정한가?
- `kb/results/slide2_lit_summary_revised_2026_06_21.md` — Slide 2 (Literature summary) — 개정 (2026-06-21)
- `kb/results/uma_force_accuracy_li3ps4_2026_08_19.md` — UMA-s-1p1(omat) 힘 정확도 — Li₃PS₄ DFT 라벨 벤치 (외부 데이터, DFT 0회) ○미열람
- `kb/results/vgcf_hbn_figure_plan.md` — VGCF/h-BN 원고 — 층수 연구를 어디에 둘 것인가 (2026-07-31 결정)
- `kb/results/vgcf_hbn_gallery_mechanism_2026_07_30.md` — h-BN@VGCF — 209 meV 층수효과의 정체: confinement 확정 (2026-07-30)

## reviews/ (73)
- `kb/reviews/ECERD2600097_review_notes.md` — 📝 리뷰 노트 — ECER-D-26-00097 (Fan 외, *Stability Issues in Sulfide-Based ASSB*)
- `kb/reviews/codex_AA_prompt_stageA_v5_regate_2026_08_29.md` — Codex 재검토 요청 AA — 회신 Z 의 P0 8건 처리 후 Stage A v5 재게이트 ○미열람
- `kb/reviews/codex_AB_prompt_stageA_v9_regate_2026_08_29.md` — Codex 재검토 요청 AB — 회신 AA 의 P0 5건 + Q2 처리, 그리고 자체검토에서 나온 넷 ○미열람
- `kb/reviews/codex_AC_prompt_manuscript_v8_crosscheck_2026_08_30.md` — 회신 AC 요청 — 원고 v6 · SI v6 대조 (Methods/Table v8) ○미열람
- `kb/reviews/codex_AD_prompt_stageA_v10_final_regate_2026_08_30.md` — 회신 AD 요청 — Stage A v10 최종 재게이트 (P0 8건 처리 후) ○미열람
- `kb/reviews/codex_AE_prompt_stageA_v13_submit_gate_2026_08_30.md` — 회신 AE — 제출 게이트: sdcp_stageA_v13 + holdout_v4 (42잡) GO/NO-GO ○미열람
- `kb/reviews/codex_AG_prompt_stageA_go_nogo_2026_08_30.md` — 회신 AG — Stage A 최종 GO/NO-GO: 회신 AF P0 넷을 닫았다
- `kb/reviews/codex_AH_prompt_am_i_lost_2026_08_30.md` — 회신 AH — 이걸 꼭 해야 하나: 길을 잃은 것 아닌지 판정 요청
- `kb/reviews/codex_AI_prompt_current_head_2026_08_30.md` — 회신 AI — 현재 HEAD 기준 재검토 + 비례성 판정 (AH 미회신 병합)
- `kb/reviews/codex_AJ_prompt_c12_submit_2026_08_30.md` — 회신 AJ — C-12 구현 완료 + 선언된 이탈 하나(clean slab) + 발송 승인 요청
- `kb/reviews/codex_AK_prompt_lpsocl_box331_md_2026_08_30.md` — 회신 AK — LPSOCl 3×3×1 MD 를 던지기 전에: estimand 와 범위
- `kb/reviews/codex_AK_reply_lpsocl_box331_md_2026_08_30.md` — 회신 AK 접수 — 조건부 GO (Q2=C). β 게이트를 되살린 것은 우리 실수였다
- `kb/reviews/codex_AL_prompt_cascade_d_rel_2026_08_30.md` — 회신 AL — cascade 39설계 D_rel 을 던지기 전에: 예측기가 자기 자신을 재현 못 한다
- `kb/reviews/codex_AL_reply_cascade_d_rel_2026_08_30.md` — 회신 AL 접수 — NO-GO. 내 '같은 구조' 전제가 틀렸다
- `kb/reviews/codex_AM_prompt_c12_incar_2026_08_31.md` — 회신 AM — C-12 INCAR 실물 감사: 진공 시험이 진공만 재지 않는다
- `kb/reviews/codex_AM_reply_c12_incar_2026_08_31.md` — 회신 AM 접수 — NO-GO. 분석기가 자기 번들을 못 읽는다
- `kb/reviews/codex_AN_prompt_c12_v7_2026_08_31.md` — 회신 AN — C-12 v7 재심: estimand 를 고정기하 단일점으로 되돌렸다
- `kb/reviews/codex_AP_prompt_c12_v14_2026_08_31.md` — 리뷰 요청 AP — C-12 v14 (회신 AO 해제조건 9건 이행) ○미열람
- `kb/reviews/codex_AQ_prompt_c12_v15_2026_08_31.md` — 리뷰 요청 AQ — C-12 v15 (회신 AP 해제조건 12건 이행) ○미열람
- `kb/reviews/codex_AR_reply_c12_v15_2026_08_31.md` — 회신 AR — c12 v15 NO-GO (해제조건 10건) ○미열람
- `kb/reviews/codex_AS_prompt_c12_v16_2026_08_31.md` — 리뷰 요청 AS — C-12 v16 (회신 AR 해제조건 10건 이행) ○미열람
- `kb/reviews/codex_AT_prompt_c12_v17_2026_08_31.md` — 리뷰 요청 AT — C-12 v17 (회신 AS 해제조건 10건 이행) ○미열람
- `kb/reviews/codex_A_cascade_ml_2026_08_20.md` — 교차리뷰 A — cascade 파이프라인 + 머신러닝 (codex 작업지시서) ○미열람
- `kb/reviews/codex_B_neb_md_tools_2026_08_20.md` — 교차리뷰 B — NEB · MD · 도구 (codex 작업지시서) ○미열람
- `kb/reviews/codex_C_funnel_2026_08_20.md` — 교차리뷰 C v2.1 — cascade 깔때기는 잘 작동했나 (codex 2라운드 종료) ○미열람
- `kb/reviews/codex_D_symposium_talk_standard_2026_08_25.md` — 교차리뷰 D — 심포지엄 세션(덱+녹취) 표준 (codex 작업지시서) ○미열람
- `kb/reviews/codex_E_sdcp_wave1_gate_2026_08_25.md` — 교차리뷰 E — SDCP wave1 게이트 수정·물리 결론 (판정 수령 + 반영) ○미열람
- `kb/reviews/codex_F_beta_null_model_2026_08_27.md` — 교차리뷰 F — β 귀무모형이 뒤집혔다 (08-11 Q1 재개 + 신규 3건) ○미열람
- `kb/reviews/codex_G_reply_to_F_2026_08_27.md` — 교차리뷰 G — 회신 F 수용 보고 + 후속 질문 (R3 설계·D_inc 오차·N_eff) ○미열람
- `kb/reviews/codex_H_reply_to_G_2026_08_27.md` — 교차리뷰 H — 회신 G 반영 보고 + 새 질문 5건 (200 ps 표준이 block 바닥 아래다) ○미열람
- `kb/reviews/codex_I_neb_cc333_worth_it_2026_08_27.md` — 교차리뷰 I — 3주짜리 NEB 를 재개할 값어치가 있나 (싼 우회로가 물리적으로 막혔다) ○미열람
- `kb/reviews/codex_I_reply_neb_hold_2026_08_27.md` — 회신 I — 3주 NEB 는 HOLD (영구 폐기 아님). 우리 잠정판단 N3 이 기각됐고 P0 3건이 나왔다 ○미열람
- `kb/reviews/codex_J_prereq_go_nogo_2026_08_27.md` — 교차리뷰 J — 선행검사 2건 GO/NO-GO (돌리기 전에) ○미열람
- `kb/reviews/codex_K_what_next_after_seminar_2026_08_28.md` — 교차리뷰 K — 세미나 이후 무엇을 할 것인가 (데이터·모델은 늘었는데 축이 비어 있다) ○미열람
- `kb/reviews/codex_L_vanhove_regimes_2026_08_28.md` — 교차리뷰 L — van Hove 33궤적: 고원·시드폭발·독립재현 셋이 진짜인가 ○미열람
- `kb/reviews/codex_M_sdcp_wave15_close_2026_08_28.md` — 교차리뷰 M — SDCP wave1.5 마감: basin-매칭 참조·자리선호 종결·라디칼 닫기 설계 ○미열람
- `kb/reviews/codex_N_estimand_discipline_2026_08_28.md` — 교차리뷰 N — estimand 규율·마감 규율: 이게 작동할 규율인가, 아니면 또 하나의 안 읽는 문서인가 ○미열람
- `kb/reviews/codex_O_prompt_sdcp_doped_estimand_2026_08_28.md` — Codex 회신 O 요청 프롬프트 — SDCP doped estimand 카드 (계산 전 심사) ○미열람
- `kb/reviews/codex_O_sdcp_doped_estimand_reply_2026_08_28.md` — 회신 O — SDCP doped estimand 카드 전면 반려 (P0, 슬랩 NO-GO) ○미열람
- `kb/reviews/codex_P_prompt_wave1_incar_audit_2026_08_28.md` — Codex 회신 P 요청 프롬프트 — wave1 INCAR 전수 감사 + doped 마감 심사 ○미열람
- `kb/reviews/codex_P_wave1_incar_audit_reply_2026_08_28.md` — 회신 P — INCAR 감사 fail-open · 추출부호 철회 · LREAL 회계 정정 (P0 3건) ○미열람
- `kb/reviews/codex_Q2_prompt_claim_and_normalization_2026_08_29.md` — Codex 회신 Q 요청 (재작성) — 기전이 철회된 뒤 원고가 쓸 수 있는 문장과 그 정규화 ○미열람
- `kb/reviews/codex_Q_prompt_neutral_ptfe_closure_2026_08_28.md` — Codex 회신 Q 요청 프롬프트 — neutral·PTFE 마감과 0.346 eV 헤드라인 심사 ○미열람
- `kb/reviews/codex_R2_doped_reopen_v3_reply_2026_08_28.md` — 회신 R2 — Stage 0 재차 NO-GO: 빌더 실물이 카드와 불일치 (P0 6건 + 최소수정 8) ○미열람
- `kb/reviews/codex_R2_prompt_doped_reopen_v3_2026_08_28.md` — Codex 회신 R2 요청 프롬프트 — 재개 설계 v3 재심사 (회신 R 조건 8 반영 확인) ○미열람
- `kb/reviews/codex_R3_doped_reopen_impl_reply_2026_08_28.md` — 회신 R3 — Stage 0 재차 NO-GO: 실측 fail-open 5건 + 관측량 회수 계약 (GO 요건 9) ○미열람
- `kb/reviews/codex_R3_prompt_doped_reopen_impl_2026_08_28.md` — Codex 회신 R3 요청 프롬프트 — 최소수정 8 구현 재제출 (실물 .inp·manifest·음성 e2e 첨부) ○미열람
- `kb/reviews/codex_R4_doped_reopen_impl2_reply_2026_08_29.md` — 회신 R4 — 조건부 GO: 중성 Stage A 8개 ORCA Opt만 승인, Stage 0·B·hybrid 전부 NO-GO ○미열람
- `kb/reviews/codex_R4_prompt_doped_reopen_impl2_2026_08_28.md` — Codex 회신 R4 요청 프롬프트 — R3 P0 전건 구현 재제출 (receipt·analyzer·계약 증빙) ○미열람
- `kb/reviews/codex_R_doped_reopen_v2_reply_2026_08_28.md` — 회신 R — Stage 0 NO-GO: 재심사 조건 8 (U_eff 자료부재 · 기체상 retention 자명 · conditioning 오염) ○미열람
- `kb/reviews/codex_R_prompt_doped_reopen_v2_2026_08_28.md` — Codex 회신 R 요청 프롬프트 — doped 재개 설계 v2 의 계산 전 심사 ○미열람
- `kb/reviews/codex_S_prompt_backbone_polaron_estimand_2026_08_31.md` — 리뷰 요청 S — SDCP 백본 폴라론 estimand (계산 전, §1–3 선심사) ○미열람
- `kb/reviews/codex_S_prompt_t13_msd_length_2026_08_29.md` — Codex 회신 S 요청 프롬프트 — T13 (MSD 생산길이 200 ps 타당성) 판정 + ⏭-2 착수 가부 ○미열람
- `kb/reviews/codex_T_prompt_polaron_pilot_seeds_2026_08_31.md` — 리뷰 요청 T — 폴라론 pilot, phase S 착수 전 (seed 생성 완료) ○미열람
- `kb/reviews/codex_T_prompt_sdcp_binding_energy_path_2026_08_29.md` — Codex 회신 T 요청 — 중성 SO₃H 흡착에너지를 원고에 넣는 최단 경로 ○미열람
- `kb/reviews/codex_T_reply_polaron_pilot_2026_08_31.md` — 회신 T — 폴라론 pilot phase S 착수 NO-GO (P0 4건 · 해제조건 6건) ○미열람
- `kb/reviews/codex_U_prompt_neutral_close_plan_2026_08_29.md` — Codex 회신 U 요청 — 중성 SDCP 흡착 **닫힘 조건 사전등록** + 자세·기준 동시 교정 계획 ○미열람
- `kb/reviews/codex_V_prompt_closure_incar_audit_2026_08_29.md` — Codex 회신 V 요청 — closure 번들 INCAR 실물 감사 (던지기 전 마지막 관문) ○미열람
- `kb/reviews/codex_W_prompt_mlip_selector_validity_2026_08_29.md` — Codex 회신 W 요청 — MLIP 를 후보 선택기로 쓰는 것이 이 계에서 성립하나 (실측 오프셋 첨부) ○미열람
- `kb/reviews/codex_X_bundle_reply_2026_08_29.md` — Codex 회신 X — prospective 번들 NO-GO · P0 6건 · Stage A/B 재설계 ○미열람
- `kb/reviews/codex_X_prompt_prospective_bundle_ready_2026_08_29.md` — Codex 회신 X 요청 — prospective 번들 40잡, 던지기 전 최종 감사 (실물 첨부) ○미열람
- `kb/reviews/codex_stats_question_2026_08_11.md` — Codex 질문 — 통계 판정 3건 (β 귀무분포 · 사다리 설계 · BVSE 부호 · 판정바닥 ddof)
- `kb/reviews/section3_review_candidates.md` — 📋 §3 리뷰 코멘트 후보 — 소거법 작업용 (ECER-D-26-00097)
- `kb/reviews/section3_review_comments_compressed.md` — Comments on Section 3 (Intrinsic Stability of Sulfide SEs) — 압축판 v2
- `kb/reviews/sei_neb_li3nd_rereview_request_2026_08_11.md` — 재리뷰 요청 — SEI NEB 6종 · Li₃Nd 금속 분기 · P2 범위 축소 (착수 직전)
- `kb/reviews/self_audit_2026_08_06.md` — 🔍 자체 적대적 리뷰 — 2026-08-05~06 커밋 66개 (136 파일)
- `kb/reviews/site_screen_codex_crossreview_2026_08_11.md` — Codex 교차검증 요청 — `site_screen.py` (자리 선호·자세 스크리닝)
- `kb/reviews/site_screen_codex_crossreview_reply_2026_08_11.md` — 회답 — Codex `site_screen.py` × `ptfe_linio2_uma` 교차검증
- `kb/reviews/site_screen_codex_round3_request_2026_08_11.md` — Codex 교차검증 Round 3 요청 — DFT+U 인계 · 쌍 선택 · 최종 수치
- `kb/reviews/site_screen_selfreview_2026_08_11.md` — site_screen 자체 코드리뷰 (2026-08-11) — 10건 전부 실재 · 전건 수정
- `kb/reviews/vasp_bundle_codex_reply_2026_08_11.md` — Codex 회신 접수 — VASP 번들 HOLD · v2 작업 목록
- `kb/reviews/vasp_bundle_codex_request_2026_08_11.md` — Codex 검토 요청 — VASP 외주 원샷 번들 (자리 선호 + E_ads)
- `kb/reviews/vasp_bundle_v2_rereview_request_2026_08_11.md` — Codex 재검토 요청 — VASP 번들 v2 (HOLD 10항 반영 완료 · 발송 GO/NO-GO)

## reports/ (3)
- `kb/reports/paper_first_author_requests_2026_08.md` — 논문 1저자 요청 — 답변 누적 (2026-08~)
- `kb/reports/sdcp_preliminary_final_2026_08_03.md` — SDCP 예비 최종 보고서 (2026-08-03)
- `kb/reports/sdcp_review_action_plan_2026_08_03.md` — SDCP 파이프라인 — 리뷰 2건 통합 실행계획 (2026-08-03)

## projects/ (20)
- `kb/projects/MULTI_CATEGORY_BATCH_PLAN_v22.md` — Multi-Category Multi-Compound Batch Plan — Paper #2 (v4.5.18)
- `kb/projects/MUST_READ_digital_twin_north_star.md` — 🚨🚨🚨 MUST READ — AI 계산 스크리닝 플랫폼 North Star (구: Digital Twin)
- `kb/projects/PRESENTATION_digital_twin_overview.md` — AI 계산 기반 스크리닝 플랫폼 — 발표용 종합 정리 (구: Digital Twin)
- `kb/projects/cascade_pipeline_fixes_2026_08_19.md` — cascade 파이프라인 수정 목록 — codex 교차리뷰용 (2026-08-19 전수 정독 산물) ○미열람
- `kb/projects/cascade_v23_review_2026_07_11.md` — Cascade v23 전체 리뷰 — 의도 지도 · 빠진 것 점검 · 후보군 구축 (2026-07-11)
- `kb/projects/collab_rietveld_request_2026_07.md` — 협업자 Rietveld 데이터 요청 문안 + stable phase 사용현황 정리 — 2026-07-28
- `kb/projects/decision_registry_design_2026_08_20.md` — 결정 레지스트리 설계 v2.1 — codex 3차 P0 반영 (MVP core 4결정) ○미열람
- `kb/projects/digital_twin_roadmap.md` — 디지털 트윈 + ML Screening 프로젝트 로드맵
- `kb/projects/digital_twin_v2_roadmap.md` — Argyrodite Digital Twin Network — Long-term Vision (v2 roadmap)
- `kb/projects/external_review_prompt_digital_twin_2026_05_18.md` — External Review Prompt — Digital Twin Platform Readiness (2026-05-18)
- `kb/projects/li_neb_anode_free.md` — Li Adatom Diffusion on Anode-Free SSB Interphases
- `kb/projects/ml_opportunities_from_lab_ppt_2026_07.md` — 랩 ML 파이프라인(TabPFN)과 우리 캠페인의 접점 — 2026-07-28
- `kb/projects/mlip_next_campaigns_2026_07.md` — MLIP(UMA) 차기 캠페인 후보 제안서 — cascade 확장 7건
- `kb/projects/screening_roadmap_2026_07.md` — AI 계산 스크리닝 로드맵 — 문헌 7편(2013–2020) 대비 우리 좌표와 실행 항목
- `kb/projects/sdcp_linio2_binding.md` — SDCP–LiNiO₂ Binding Anchoring Scan
- `kb/projects/sdcp_master_v2_2026_07_11.md` — Self-Doped Conducting Polymer 전도성 바인더 — 물질·계면화학·매뉴스크립트·모델·로드맵 단일 레퍼런스 **v2**
- `kb/projects/sdcp_phaseB_direction_2026_08_06.md` — 🎯 SDCP Phase-B 방향 정리 (2026-08-06)
- `kb/projects/sdcp_v7c_structure_spectroscopy_report_2026_07_10.md` — SDCP v7c — 구조·분광 판정 보고 (입문자용 완전판)
- `kb/projects/sei_products_2026_08_06.md` — SEI 분해상 6종 캠페인 — 확산장벽 · 형성전위 · 밴드갭
- `kb/projects/symposium_2026_competitive_analysis.md` — 전지기술 심포지엄 2026 — 경쟁 좌표 분석 (이상욱 / 문장혁)

## questions/ (9)
- `kb/questions/doped_declared_state_feasibility_2026_08_29.md` — doped E_ads 를 '상태 선언' 으로 살릴 수 있나 — NUPDOWN 은 홀 위치를 안 묶는다 ○미열람 [open]
- `kb/questions/esw_reduction_limit_field_2026_08_28.md` — `reduction_limit_V` 는 환원한계가 아닌 것 같다 — breakpoint 하나 아래를 가리킨다 ○미열람 [open]
- `kb/questions/lpsocl_low_beta_mechanism.md` — 저β 런의 정체 — 케이지 절편인가, 진짜 sub-diffusion인가, 느린 전이인가 ⚠disputed ○미열람 [active]
- `kb/questions/sdcp_backbone_polaron_estimand_2026_08_31.md` — H-제거 n=6 라디칼 상태지도 — estimand 카드 v2 (회신 S 반영) ○미열람 [open]
- `kb/questions/sdcp_doped_estimand_2026_08_28.md` — SDCP doped 흡착 — estimand 카드 (계산 전에 리뷰로 보내는 §1–3) ○미열람 [active]
- `kb/questions/sdcp_doped_reopen_v2_2026_08_28.md` — sdcp_doped 재개 설계 v2 — 회신 O 재승인 조건 7 을 실제로 채우는 카드 ○미열람 [answered]
- `kb/questions/sdcp_doped_reopen_v3_2026_08_28.md` — sdcp_doped 재개 설계 v3 — 회신 R 재심사 조건 8 반영 (Stage 0 재심사용) ○미열람 [active]
- `kb/questions/sdcp_site_preference.md` — SDCP 조각은 LiNiO₂(104)에서 Li 자리와 Ni 자리 중 어디에 붙는가 ○미열람 [active]
- `kb/questions/sdcp_stageA_holdout_selector_2026_08_30.md` — estimand 카드 — Stage A 홀드아웃: UMA 선택기가 DFT 순위를 맞히나 ○미열람 [open]

## syntheses/ (6)
- `kb/syntheses/binder_adsorption_charge_state_2026_08_29.md` — 음이온성 바인더의 흡착에너지 — ICEP 의 (−H) 는 탈양성자가 아니라 H 이동이었다 ○미열람
- `kb/syntheses/li3n_barrier_revision_defense_2026_08_12.md` — Li3N(001) 장벽 — 리비전 방어 카드 (AF-ASSB 원고 v5) ○미열람
- `kb/syntheses/md_sampling_variance_defense_2026_08_25.md` — 왜 3시드·200 ps·β 게이트인가 — 짧은 단일 런은 산포를 없애지 않고 가린다 ○미열람
- `kb/syntheses/nd_doping_two_axis_verdict.md` — Nd₂O₃ 도핑 — 열역학 창과 전자구조가 **같은 방향으로** 진다 ○미열람
- `kb/syntheses/why_so3h_not_deprotonated_2026_08_29.md` — 왜 SO₃H 만 계산했나 — 원고에 그대로 쓸 근거 5 ○미열람
- `kb/syntheses/xu2026_li_nd_rebuttal.md` — Xu 2026 의 "Li–Nd alloy SEI" 주장은 열역학·전자구조로 기각된다 ○미열람

## platforms/ (2)
- `kb/platforms/literature_db_tools.md` — Literature DB 자동화 도구
- `kb/platforms/ml_automation_platforms.md` — ML / Automation Platform Survey

## descriptors/ (1)
- `kb/descriptors/coating_descriptor_catalog.md` — 황화물 코팅 소재 Descriptor Catalog

## papers/ (19)
- `kb/papers/adhesion_charts_comparison.md` — Adhesion Charts — 20 seeds vs Selected 5 seeds
- `kb/papers/adhesion_literature_review.md` — Adhesion Interface Modeling — Literature Summary
- `kb/papers/choi2025_adoption_guide.md` — Choi 2025 — Adoption Guide for Our Paper
- `kb/papers/computational_methods_draft.md` — Computational Methods — FINAL VERSION (2026-04-16)
- `kb/papers/draft_v1.md` — Beyond Electrochemistry: Tailoring Mechanical Properties of Halogen-Substituted Argyrodites
- `kb/papers/final_report_v2.md` — LPSCl Manuscript — Final Report v2 (Updated 2026-04-17)
- `kb/papers/lpscl_vs_lpscl16_20min_script.md` — LPSCl vs LPSCl₁.₆ — 20분 학회 발표 대본 (full)
- `kb/papers/lpscl_vs_lpscl16_seminar_script_outline.md` — LPSCl vs LPSCl₁.₆ 세미나 — 발표 개요 + 통합 대본 (2026-06-11)
- `kb/papers/lpscl_vs_lpscl16_seminar_v1.md` — LPSCl vs LPSCl₁.₆ Seminar — Slide Master v1
- `kb/papers/mechanism_anion_O_descriptor.md` — 메커니즘 — 할로겐 치환 Argyrodite / NCM 계면 접착
- `kb/papers/narrative_with_literature_steps.md` — Paper #1 Narrative — Literature-Grounded Step-by-Step Guide
- `kb/papers/origin_adhesion_guide.md` — Adhesion Bar Chart — Origin Guide (BML Standards)
- `kb/papers/paper2_FINAL_briefing_2026_05_08.md` — Paper #2 — SE/NCM Adhesion: Final Comprehensive Briefing
- `kb/papers/paper2_briefing_2026_05_08.md` — Paper #2 — SE/NCM Adhesion Mechanism: Briefing for First-Time Reader
- `kb/papers/reviewer_qa_methods.md` — Reviewer Q&A Preparation — Computational Methods
- `kb/papers/si_figures_plan.md` — SI Figures Plan — Choi 2025 Analogs
- `kb/papers/verified_refs_2026_05.md` — Verified Literature References — Paper #1 (2026-05-05)
- `kb/papers/vesta_adhesion_figure_settings.md` — VESTA Adhesion Figure Settings (Paper)
- `kb/papers/vesta_settings_guide.md` — VESTA Settings for Adhesion Interface Figure

## literature_db/ (3)
- `kb/literature_db/damore_2022_lpscl_symmetry_breaking_qha.md` — D'Amore et al. 2022 — LPSCl 대칭 깨짐 (phonon + QHA)
- `kb/literature_db/pustorino_2025_lpscl_li_ordering_mechanical.md` — Pustorino et al. 2025 — LPSCl Li ordering → 기계적/전자 물성
- `kb/literature_db/sundar_2025_lpscl_coating.md` — 📄 Sundar et al. 2025 — Computationally-Guided LPSCl Oxide Coating

## seminars/ (24)
- `kb/seminars/Research_Seminar_2026_08_cascade_final_README.md` — Research Seminar — Cascade final package
- `kb/seminars/Research_Seminar_2026_08_cascade_final_defense_QA_ko.md` — Research Seminar — Cascade Defense Q&A
- `kb/seminars/Research_Seminar_2026_08_cascade_final_script_ko.md` — Research Seminar — Cascade final speaker script
- `kb/seminars/Research_Seminar_2026_08_cascade_final_source_ledger.md` — Research Seminar — Slide Source Ledger
- `kb/seminars/Research_Seminar_2026_08_cascade_final_terminology_symbols.md` — Research Seminar — 용어·기호 규약
- `kb/seminars/cascade_content_edit_directive_2026_08_11.md` — Cascade 세미나 내용 편집 지시서 — 기준본 24장 (Codex 편집용)
- `kb/seminars/cascade_deck_3to7_script_2026_08_20.md` — cascade 세미나 — 덱 3~7장 대본 (재정비판) ○미열람
- `kb/seminars/cascade_deck_8to12_script_2026_08_20.md` — 세미나 대본 — 덱 8~12장 (후보군 · 자리 · 구조생성 · MLIP 스크리닝) ○미열람
- `kb/seminars/cascade_dopant_screening_story_2026_08.md` — LPSCl 도펀트 스크리닝 — 연구세미나 대본 (v6 · 덱과 1:1) ○미열람
- `kb/seminars/cascade_final_release_review_2026_08_11.md` — 최종 release 감사 보고 — Research_Seminar_2026_08_cascade_final (28장)
- `kb/seminars/cascade_release_speaker_script_v2_ko.md` — 발표 대본 v2 — Research_Seminar_2026_08_cascade_release (29장, A3b 레이더 포함)
- `kb/seminars/cascade_seminar_2026_08_build_v3.md` — 🎤 Research Seminar **BUILD SHEET v3** — 사진만 붙이면 끝나는 판
- `kb/seminars/cascade_seminar_2026_08_script.md` — 🎙 Research Seminar 대본 — Screening cascade for sulfide SEs
- `kb/seminars/cascade_seminar_2026_08_spec.md` — 🎤 Research Seminar spec — DFT-based screening cascade for sulfide SEs
- `kb/seminars/cascade_seminar_2026_08_spec_codex.md` — Research Seminar spec — A gated MLIP-to-DFT screening cascade for LPSCl modification
- `kb/seminars/cascade_seminar_2026_08_spec_v2.md` — 🎤 Research Seminar spec **v2** — Screening cascade for sulfide SEs
- `kb/seminars/cascade_seminar_supporting_materials_README.md` — Cascade seminar supporting materials
- `kb/seminars/cascade_speaker_script_FINAL_ko.md` — 발표 대본 최종본 — Research Seminar 2026-08 · Cascade
- `kb/seminars/cascade_speaker_script_audit_rev6_ko.md` — Cascade audit-first research seminar — Korean master script
- `kb/seminars/cascade_speaker_script_rev2_ko.md` — 발표 대본 최종본 — Research Seminar 2026-08 · Cascade
- `kb/seminars/cascade_speaker_script_rev3_FINAL_ko.md` — 발표 대본 — Research Seminar 2026-08 · Cascade **rev3 (정본)**
- `kb/seminars/cascade_speaker_script_rev4_ko.md` — Cascade rev4 발표 대본 — Research Seminar 2026-08 ○미열람
- `kb/seminars/cascade_speaker_script_round3_ko.md` — Cascade round-3 audit research seminar — Korean master script
- `kb/seminars/seminar_redirect_2026_08_11.md` — 세미나 방향 전환 브리프 (2026-08-11 밤) — Codex 재구성용 재료 목록

## elements/ — 118개 (생성물/템플릿, 목록 생략)
## templates/ — 3개 (생성물/템플릿, 목록 생략)

## litdb/ — digest 202개 (정본 목록: litdb/INDEX.md)

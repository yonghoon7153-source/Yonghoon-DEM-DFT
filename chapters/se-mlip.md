# 원자간 퍼텐셜(MLIP) 방법론

전해질 · 계면 · 장 `se-mlip` · 논문 22편 · 읽기 카드 22편

> 범용 MLIP의 정확도와 적용 범위, 미세조정, 불확실도 추정.

## 장 서문 — 범용 MLIP의 평균 오차는 이온 이동 정확도를 보증하지 않는다

*읽기 카드 22편을 엮어 쓴 글 · 항목 30개 중 30개 검증 통과 · 2026-11-10*

범용 MLIP을 고체전해질과 계면에 그대로 써도 되는지, 안 되면 무엇으로 고치고 그 오차를 어떻게 재는지를 묻는 논문들이다. [근거: Agarwal et al. 2026 (`agarwal2026_umlip_applicability_domain_ssb_interfaces`); Chang et al. 2026 (`chang2026_performance_based_mlip_selection_sse`); Zhang et al. 2026 (`zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill`); Grasselli et al. 2025 (`grasselli2025_uncertainty_era_ml_atomistic`)]

여러 논문이 평균 힘과 에너지 오차가 작아도 장벽, 확산계수, 계면 힘, 상대 안정성 순서가 틀릴 수 있음을 보였고, 적은 DFT로 미세조정하면 그 오차가 준다고 보고했다. [근거: Zhang et al. 2026 (`zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill`); Wang et al. 2025 (`wang2025_pretrained_deep_potential_sulfide_sse`); Alghamdi et al. 2026 (`alghamdi2026_finetuning_strategies_li_diffusion_mace`); Agarwal et al. 2026 (`agarwal2026_umlip_applicability_domain_ssb_interfaces`); Kalikadien · Pidko 2026 (`kalikadien2026_uma_tm_catalyst_conformer_ranking`)]

불확실도는 분포 안에서만 오차를 따르고, 확산계수 같은 수송계수로 전파하는 이론은 아직 없다. [근거: Kurniawan et al. 2026 (`kurniawan2025_comparative_ensemble_uq_nnip`); Grasselli et al. 2025 (`grasselli2025_uncertainty_era_ml_atomistic`); Imbalzano et al. 2020 (`imbalzano2021_committee_uq_md_thermodynamic_averages`)]

### 정적 오차의 한계

평균 힘과 에너지 오차가 작다는 것이 이온 이동 물성이나 상대 안정성의 정확도를 뜻하지 않는다. Zhang et al. 2026에서 MACE-MP-0는 세 전해질의 AIMD 시험 세트에서 힘 RMSE 0.16 eV/Å를 냈지만, Li 확산계수 RRMSE는 60.8 %였다. Kalikadien & Pidko 2026에서 UMA-s-1.1은 DFT와 R² 0.96–0.97로 맞았지만 리간드별 순위 신뢰율은 Mn 44 %까지 떨어졌다. 검토 측은 이 Mn 값이 배열 네 개의 완벽 순위 비율이라 강직계 값과 같은 척도가 아니라고 본다. Makino et al. 2026도 R²와 RMSE는 내삽 정확도만 재며 안정한 MD를 보증하는 힘 오차 기준은 없다고 적었다. [근거: Zhang et al. 2026 (`zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill`); Kalikadien · Pidko 2026 (`kalikadien2026_uma_tm_catalyst_conformer_ranking`); Makino, …, Takamoto, Shinagawa, Asano, Nakayama 2026 (`makino2026_mlip_battery_materials_review`)]

범용 모델이 확산을 어느 쪽으로 틀리는지는 논문마다 엇갈린다. Wang et al. 2025는 fine-tune하지 않은 범용 모델의 LGPS 장벽이 DFT의 1/3 수준이어서 상온 확산을 과대평가한다고 적었다. Alghamdi et al. 2026의 MACE-MPA-0는 LiF 속 Li의 Ea를 기준에 가깝게 맞히면서도 450 K에서 D를 49 % 낮게 냈다. 검토 측은 이 논문에서 fine-tune 뒤의 일치가 지수앞인자와 장벽항의 상쇄이며 423 K 아래에서는 과대평가로 뒤집힌다고 본다. 기준도 달라서 Wang et al. 2025는 AIMD와 실험에, Alghamdi et al. 2026은 같은 그룹의 DeePMD 모델에 견주었다. [근거: Wang et al. 2025 (`wang2025_pretrained_deep_potential_sulfide_sse`); Alghamdi et al. 2026 (`alghamdi2026_finetuning_strategies_li_diffusion_mace`)]

### 계면과 분포 밖

범용 MLIP은 Li 계면에서 총에너지보다 힘과 안정성 순서를 틀린다. Agarwal et al. 2026은 OMat24로 사전학습한 여섯 모델을 미세조정 없이 스물네 개의 Li 금속 계면에 대어, 총에너지 MAE는 모델 평균 < 15 meV/atom이지만 힘 오차가 계면 원자와 계면 수직 성분에 몰린다고 보고했다. 사전학습 자료의 영역 밖 원자는 평균 힘 오차가 114 meV/Å로 영역 안의 54 meV/Å보다 컸다. 다중음이온 계면의 안정성 순서는 어느 모델도 다 맞히지 못했고, 원문은 단일 음이온 계면의 정성 스크리닝까지만 가능하다고 결론지었다. 검토 측은 다중음이온과 단일 음이온의 구분이 Li 금속에 불안정한가와 겹쳐 있어 오차의 원인을 가를 수 없다고 본다. [근거: Agarwal et al. 2026 (`agarwal2026_umlip_applicability_domain_ssb_interfaces`)]

계면이나 분포 밖 정확도를 내세운 다른 논문들도 검증이 그 영역까지 닿지 않는다. Liu et al. 2026의 FIRE는 계면 구조로 학습했지만 물성 검증은 단일상 벌크 세 계에서만 했고, 검토 측은 계면에서 정확하다는 주장이 아직 증명되지 않았다고 본다. Wood et al. 2026의 UMA 논문이 OOD라 부른 시험셋도 OMat24와 같은 DFT 설정으로 만든 데이터라고 검토 측은 지적한다. Wang et al. 2026은 Li₆PS₅Cl에서 MPtrj 계열 체크포인트의 힘 투영 기울기가 0.63–0.87로 감쇠를 보였지만 BaTiO₃에서는 다섯 모델 모두 1보다 컸다고 적었다. 원문은 두 시험의 범함수와 배치가 달라 이 차이를 재료 탓으로만 돌릴 수 없다는 단서를 달았다. [근거: Liu et al. 2026 (`liu2026_ai_ready_finetuning_solid_solid_interfaces`); Wood, Dzamba, Fu, Gao, Shuaibi, Barroso-Luque et al. 2026 (`uma2026_family_of_universal_models_for_atoms`); Wang et al. 2026 (`wang2026_umlff_review_softening_forgetting_longrange`)]

### 미세조정의 이득

적은 DFT로 미세조정하면 목표 계의 이동 물성과 에너지 오차가 준다는 데 논문들이 같은 쪽에 선다. Zhang et al. 2026은 수백 개 DFT로 파인튜닝한 MACE의 확산계수 RRMSE 평균이 13.22 %였다고 보고했다. Wang et al. 2025에서 훈련에 없던 Li₂B₂S₅의 에너지 MAE는 스무 프레임 fine-tune으로 162.65에서 3.44 meV/atom으로 줄었다. Alghamdi et al. 2026도 소량 fine-tune으로 MACE의 D 과소평가를 줄였지만, 결과를 가른 것은 데이터 양보다 bulk와 침입형 구조의 비율이었다. 이 논문의 기준은 DeePMD 모델이어서 DFT 참값에 가까워졌다고는 말할 수 없다고 검토 측은 본다. [근거: Zhang et al. 2026 (`zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill`); Wang et al. 2025 (`wang2025_pretrained_deep_potential_sulfide_sse`); Alghamdi et al. 2026 (`alghamdi2026_finetuning_strategies_li_diffusion_mace`)]

출발 파운데이션의 무게는 두 MACE 논문에서 엇갈린다. Tompa & Varga-Umbrich 2026은 Li₆PS₅Cl에서 여덟 체크포인트를 같은 레시피로 fine-tune했을 때 MP-0a가 가장 나빴다며, 전략보다 파운데이션 품질과 E₀ 초기화가 먼저라고 적었다. 같은 논문에서 model-aware reestimation은 학습 없이 SPICE E₀ 오차를 3.13 eV에서 0.33 eV로 줄였다. Liu et al. 2026의 튜토리얼은 LGPS에서 세 MACE 파운데이션의 최종 힘 RMSE가 14.88–15.84 안에 들어 출발점의 선택이 결과를 크게 바꾸지 않았다고 적었다. 이 튜토리얼은 LiGePS에서 고른 최적 설정을 다른 계로 옮기면 이득이 0–4%로 준다고도 적었다. [근거: Tompa & Varga-Umbrich 2026 (`tompa2026_finetuning_mlip_foundation_strategies`); Liu et al. 2026 (`liu2026_finetuning_umlip_tutorial`)]

### 망각과 MD 안정성

넓게 쓸 모델을 만들 때는 사전학습 데이터를 섞는 replay가 견고성을 지킨다는 보고가 모인다. Tompa & Varga-Umbrich 2026에서 naive fine-tune은 좁은 표적 하나에서 가장 정확했지만, NaCl의 PES 구멍 비율을 50 GPa에서 9.4에서 34.4%로 늘렸다. multihead와 pseudolabel replay는 모든 조건에서 파운데이션 수준이거나 그 이하였다. Liu et al. 2026의 FIRE도 여섯 계 모두에서 replay가 replay 없는 미세조정보다 RMSE가 낮았다. Mazitov et al. 2025의 LoRA 뒤에는 MAD 기저 성능이 에너지 기준 3–19배 나빠져, 검토 측은 범용성이 사실상 사라진다고 판단한다. [근거: Tompa & Varga-Umbrich 2026 (`tompa2026_finetuning_mlip_foundation_strategies`); Liu et al. 2026 (`liu2026_ai_ready_finetuning_solid_solid_interfaces`); Mazitov et al. 2025 (`petmad2026_lightweight_universal_interatomic_potential_mad`)]

MD 안정성은 정적 정확도와 따로 움직이며, 힘을 에너지 기울기로 얻는 보존성이 그 한 축이다. Chang et al. 2026에서 다섯 모델의 형성에너지 MAE는 모두 10 meV/atom 아래여서 구분이 안 됐고, 비보존 모델 ORB v2와 EqV2만 Li₆PS₅Cl NVT MD에서 총에너지가 단조 상승했다. Mazitov et al. 2025에서도 힘을 직접 예측하는 head는 BMIM-Cl NVE에서 운동에너지가 폭주했다. Zhang et al. 2026은 from scratch 모델이 LGPS에서 800개를 써도 100 ps를 버티지 못했고, 파인튜닝 모델은 사전학습 모델의 매끄러운 단거리 PES를 물려받아 안정하다고 적었다. Wood et al. 2026의 UMA 논문이 MD에서 보인 검증은 NVE 에너지 보존의 통과 여부뿐이며, 확산계수나 이온전도도는 원문에 없다. [근거: Chang et al. 2026 (`chang2026_performance_based_mlip_selection_sse`); Mazitov et al. 2025 (`petmad2026_lightweight_universal_interatomic_potential_mad`); Zhang et al. 2026 (`zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill`); Wood, Dzamba, Fu, Gao, Shuaibi, Barroso-Luque et al. 2026 (`uma2026_family_of_universal_models_for_atoms`)]

### 불확실도의 범위

committee와 앙상블의 산포는 분포 안에서는 오차와 상관하지만 외삽 영역에서는 믿기 어렵다. Carrete et al. 2023은 deep ensemble이 committee를 체계적으로 이기지 못했고, SrTiO₃ bulk에서 committee 불확실도와 오차의 Spearman 상관이 0.90이었다고 보고했다. Agarwal et al. 2026의 여섯 모델 위원회도 원자 힘에서 r = 0.81로 오차와 상관했지만, 검토 측은 위원회 표준편차가 실제 오차를 과소 추정한다고 본다. Kurniawan et al. 2026에서는 네 앙상블 모두 다이아몬드 cold curve에서 σ가 오차를 따라가지 못하고 오히려 줄었다. Grasselli et al. 2025는 모델 형태가 틀리면 멤버 전원이 같은 틀린 예측에 합의해 불확실도가 인위적으로 낮아진다고 정리했다. [근거: Carrete et al. 2023 (`carrete2023_deep_ensembles_vs_committees`); Agarwal et al. 2026 (`agarwal2026_umlip_applicability_domain_ssb_interfaces`); Kurniawan et al. 2026 (`kurniawan2025_comparative_ensemble_uq_nnip`); Grasselli et al. 2025 (`grasselli2025_uncertainty_era_ml_atomistic`)]

불확실도를 정적 열역학 평균까지 전파하는 방법은 있지만 수송계수로 가는 이론은 없다. Imbalzano et al. 2020은 보정한 committee 산포를 궤적 하나의 재가중으로 열역학 평균까지 전파했고, 액체 물에서 보정계수 α = 2.1을 얻었다. 검토 측은 이 방법이 확산 같은 동역학 관측량을 다루지 않는다고 본다. Grasselli et al. 2025도 스펙트럼과 수송계수에는 엄밀한 전파 이론이 없고 여러 궤적을 돌리는 무차별 방식뿐이라고 적었다. 두 논문 모두 편향보정 캘리브레이션에는 멤버가 적어도 M = 4 필요하다고 적었다. [근거: Imbalzano et al. 2020 (`imbalzano2021_committee_uq_md_thermodynamic_averages`); Grasselli et al. 2025 (`grasselli2025_uncertainty_era_ml_atomistic`)]

### 이 장의 값

| 값 | 표기 | 근거 |
|---|---|---|
| MACE-MP-0 Li 확산계수 RRMSE | ~60.8 % | Zhang et al. 2026 (`zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill`) |
| 파인튜닝 후 확산계수 RRMSE 평균 | 13.22 % | Zhang et al. 2026 (`zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill`) |
| MACE-MPA-0 D 과소평가(LiF) | 450 K 49 % / 500 K 42 % | Alghamdi et al. 2026 (`alghamdi2026_finetuning_strategies_li_diffusion_mace`) |
| W_adh RMSE, Li 계면 여섯 모델 | 0.38–0.60 J/m² | Agarwal et al. 2026 (`agarwal2026_umlip_applicability_domain_ssb_interfaces`) |
| CHGNet 힘 투영 기울기, Li₆PS₅Cl | 0.6269 | Wang et al. 2026 (`wang2026_umlff_review_softening_forgetting_longrange`) |
| UMA-s-1.1 순위 신뢰율, Mn 착물 | Mn 44 % | Kalikadien · Pidko 2026 (`kalikadien2026_uma_tm_catalyst_conformer_ranking`) |
| naive fine-tune PES 구멍, NaCl | 34.4% | Tompa & Varga-Umbrich 2026 (`tompa2026_finetuning_mlip_foundation_strategies`) |
| 편향보정 캘리브레이션 최소 멤버 | M = 4 | Grasselli et al. 2025 (`grasselli2025_uncertainty_era_ml_atomistic`) |

### 아직 열린 문제

- 범용 모델이 확산을 과대평가하는지 과소평가하는지가 정해지지 않았다. Wang et al. 2025는 과대평가를, Alghamdi et al. 2026은 450 K 과소평가를 보고했고, 두 논문과 Zhang et al. 2026은 UMA를 시험하지 않았으며 Wood et al. 2026의 UMA 논문에는 확산 검증이 없다. [근거: Wang et al. 2025 (`wang2025_pretrained_deep_potential_sulfide_sse`); Alghamdi et al. 2026 (`alghamdi2026_finetuning_strategies_li_diffusion_mace`); Zhang et al. 2026 (`zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill`); Wood, Dzamba, Fu, Gao, Shuaibi, Barroso-Luque et al. 2026 (`uma2026_family_of_universal_models_for_atoms`)]
- 확산계수 같은 수송계수에 모델 불확실도를 전파하는 이론이 없다. 지금 있는 것은 정적 평균까지의 재가중 전파와 여러 궤적을 돌리는 무차별 방식뿐이다. [근거: Grasselli et al. 2025 (`grasselli2025_uncertainty_era_ml_atomistic`); Imbalzano et al. 2020 (`imbalzano2021_committee_uq_md_thermodynamic_averages`)]
- 계면 정확도는 아직 계면 물성으로 검증되지 않았다. Agarwal et al. 2026의 동역학 일치는 기준 계산 없이 모델끼리 견준 결과이고 Li₆PS₅Cl 같은 황화인산염 계면을 다루지 않았으며, Liu et al. 2026의 FIRE는 물성을 벌크 세 계에서만 검증했다. [근거: Agarwal et al. 2026 (`agarwal2026_umlip_applicability_domain_ssb_interfaces`); Liu et al. 2026 (`liu2026_ai_ready_finetuning_solid_solid_interfaces`)]
- 능동학습과 미세조정이 DFT를 얼마나 아끼는지는 측정되지 않았다. Wilson et al. 2022는 새 DFT를 돌리지 않아 절감 배수가 없고 검토 측은 그 결과를 정확도가 아닌 재현성의 근거로 보며, Zhang et al. 2026은 DFT 총비용을 적지 않았다. [근거: Wilson et al. 2022 (`wilson2022_batch_active_learning_interatomic_potentials`); Zhang et al. 2026 (`zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill`)]

### 먼저 읽을 논문

1. Zhang et al. 2026 (`zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill`) — 평균 오차와 이동 물성 오차의 간극, 소량 파인튜닝, MD 안정성을 고체전해질 세 계에서 한꺼번에 보여 준다.
2. Agarwal et al. 2026 (`agarwal2026_umlip_applicability_domain_ssb_interfaces`) — 범용 MLIP의 계면 적용 영역을 시험했고, 우리가 쓰는 것과 같은 UMA-s-1p1 omat 체크포인트가 비교에 들어 있다.
3. Chang et al. 2026 (`chang2026_performance_based_mlip_selection_sse`) — Li₆PS₅Cl에서 정적 형성에너지 오차가 아니라 MD 에너지 보존성이 모델을 가른다는 것을 보여 준다.
4. Tompa & Varga-Umbrich 2026 (`tompa2026_finetuning_mlip_foundation_strategies`) — Li₆PS₅Cl을 포함한 다섯 계에서 fine-tune 전략, E₀ 초기화, replay와 망각을 한 틀로 비교한다.
5. Grasselli et al. 2025 (`grasselli2025_uncertainty_era_ml_atomistic`) — 불확실도 공식, 캘리브레이션, 전파의 한계를 정리해 다른 UQ 논문을 읽을 어휘를 준다.

## 이 장의 논문 (22편)

| digest | 저자 · 연도 | 제목 | 한 줄 결론 |
|---|---|---|---|
| `shapeev2016_moment_tensor_potentials` | Shapeev 2016 | Moment Tensor Potentials: A Class of Systematically Improvable Interatomic Potentials | 모멘트 텐서 축약 기저는 불변 다항식을 스팬하고 계수에 선형이어서, 텅스텐에서 GAP과 같은 힘 정확도를 훨씬 적은 기저와 짧은 시간으로 낸다. |
| `imbalzano2021_committee_uq_md_thermodynamic_averages` | Imbalzano et al. 2020 | Uncertainty estimation by committee models for molecular dynamics and thermodynamic averages | 보정한 committee 산포를 재가중과 선형화로 정적 열역학 평균까지 전파하고, 오차를 관측량 항과 퍼텐셜 항으로 나눈다. |
| `wilson2022_batch_active_learning_interatomic_potentials` | Wilson et al. 2022 | Batch active learning for accelerating the development of interatomic potentials | greedy 조건부 배치 능동학습은 평균 오차보다 시드 간 재현성을 크게 바꿔, 121개 계수가 약 2,000 구조에서 수렴했다. |
| `carrete2023_deep_ensembles_vs_committees` | Carrete et al. 2023 | Deep ensembles vs committees for uncertainty estimation in neural-network force fields: Comparison and application to active learning | deep ensemble은 같은 양을 잴 때 committee를 체계적으로 이기지 못했고, 학습 데이터 품질이 섞였을 때만 우위를 보였다. |
| `park2024_sevennet_parallel_gnn_md` | Park et al. 2024 | Scalable Parallel Algorithm for Graph Neural Network Interatomic Potentials in Molecular Dynamics Simulations | 통신 반경을 컷오프로 묶고 층마다 통신을 반복해 등변 GNN 포텐셜을 LAMMPS 다중 GPU MD로 확장했다. |
| `choi2025_mlip_cu_taxn_interfacial_adhesion` | Choi et al. 2025 | Atomistic Insights into Cu/Amorphous-Ta x N Interfacial Adhesion via Machine Learning Interatomic Potentials: Effects of Stoichiometry and Interface Construction | MLIP 기반 SMD와 Jarzynski 환산으로 Ta가 많고 섞임이 큰 계면일수록 Cu 접착이 강해짐을 보였다. |
| `grasselli2025_uncertainty_era_ml_atomistic` | Grasselli et al. 2025 | Uncertainty in the era of machine learning for atomistic modeling | MLIP 불확실도 정량화를 식 하나로 묶고, 수송계수 같은 시간의존 관측량으로의 전파 이론은 아직 없다고 정리한 Perspective다. |
| `petmad2026_lightweight_universal_interatomic_potential_mad` | Mazitov et al. 2025 | PET-MAD as a lightweight universal interatomic potential for advanced materials modeling | 범용 PET-MAD는 Li₃PS₄ 이온전도도를 포함한 여섯 사례에서 전용 모델과 가까운 관측량을 낸다. |
| `wang2025_pretrained_deep_potential_sulfide_sse` | Wang et al. 2025 | A pre-trained deep potential model for sulfide solid electrolytes with broad coverage and high accuracy | 황화물 전해질의 비평형 구조까지 DPA-2에 학습시키면 범용 MLIP의 장벽 과소평가와 확산 과대평가가 크게 준다. |
| `agarwal2026_umlip_applicability_domain_ssb_interfaces` | Agarwal et al. 2026 | Applicability Domain of Universal Machine Learning Interatomic Potentials at Solid-State Battery Interfaces | 사전학습 범용 MLIP은 단일 음이온 Li 계면의 정성 스크리닝까지만 쓸 수 있고, 다중음이온 계면에는 계면 전용 미세조정 자료가 필요하다. |
| `alghamdi2026_finetuning_strategies_li_diffusion_mace` | Alghamdi et al. 2026 | Comparing fine-tuning strategies for machine learning force fields in lithium-ion diffusion | 파운데이션 MACE는 LiF 속 Li의 Ea를 맞히지만 D는 크게 낮게 낸다. 소량 fine-tune이 그 오차를 줄이며, 결과는 데이터 조성이 좌우한다. |
| `chang2026_performance_based_mlip_selection_sse` | Chang et al. 2026 | Performance-Based Selection of Machine Learning Interatomic Potentials for Studying Solid-State Electrolytes | 정적 형성에너지 오차로는 범용 MLIP 다섯 종이 구분되지 않았고, MD 에너지 드리프트가 보존 모델 SevenNet을 고르게 했다. |
| `kalikadien2026_uma_tm_catalyst_conformer_ranking` | Kalikadien · Pidko 2026 | Performance of Meta’s Universal Model for Atoms across the Conformational and Configurational Space of Diverse Transition-Metal Catalysts | UMA-s-1.1은 DFT와 R² 0.96–0.97로 맞지만 리간드별 순위 신뢰율은 44–84 %에 그친다. |
| `kurniawan2025_comparative_ensemble_uq_nnip` | Kurniawan et al. 2026 | Comparative study of ensemble-based uncertainty quantification methods for neural network interatomic potentials | 네 가지 앙상블 모두 분포 안에서는 σ가 오차와 상관하지만, 외삽 영역에서는 σ가 평탄해지거나 감소한다. |
| `liu2026_ai_ready_finetuning_solid_solid_interfaces` | Liu et al. 2026 | An AI-Ready Fine-Tuning Framework for Accurate Machine-Learning Interatomic Potentials in Solid–Solid Battery Interfaces | MACE-MP-0 미세조정에 replay를 넣으면 여섯 계 모두 오차가 줄지만, 물성 검증은 벌크에 그친다. |
| `liu2026_finetuning_umlip_tutorial` | Liu et al. 2026 | Fine-tuning universal machine-learned interatomic potentials: A Tutorial on methods and applications | MACE 파운데이션 세 종을 같은 레시피로 미세조정하면 여러 계에서 오차가 줄지만, 최적 설정은 계마다 다르다. |
| `makino2026_mlip_battery_materials_review` | Makino, …, Takamoto, Shinagawa, Asano, Nakayama 2026 | Machine-Learned Interatomic Potentials for Battery Materials: From Fundamental Methodology to Emerging Applications in Electrodes, Electrolytes, and Interfaces | 배터리 MLIP을 두 축으로 분류하고 147편을 정리했다. 정적 RMSE는 내삽 정확도만 잰다고 적었다. |
| `phuthi2026_mlip_ssb_perspective` | Phuthi et al. 2026 | Machine Learning Interatomic Potentials for Modeling Solid-State Batteries | 파운데이션 퍼텐셜은 먼저 써 볼 도구이고, 설득력 있는 주장은 ab initio나 검증된 custom/fine-tuned MLIP에 기대야 한다. |
| `tompa2026_finetuning_mlip_foundation_strategies` | Tompa & Varga-Umbrich 2026 | Fine-tuning MLIP foundation models: strategies for accuracy and transferability | 전략 선택보다 파운데이션 품질, E₀ 초기화, 안정적 학습이 먼저이고, 넓게 쓸 모델에서는 replay만 견고성을 지켰다. |
| `uma2026_family_of_universal_models_for_atoms` | Wood, Dzamba, Fu, Gao, Shuaibi, Barroso-Luque et al. 2026 | UMA: A Family of Universal Models for Atoms | MoLE로 활성 파라미터를 묶은 범용 MLIP 계열은 재료 벤치마크에서 최고 수준이지만, MD 검증은 에너지 보존까지다. |
| `wang2026_umlff_review_softening_forgetting_longrange` | Wang et al. 2026 | Universal machine learning force fields for materials simulation: from model construction to complex-system applications | 범용 MLFF의 신뢰성은 과제마다 그 관측량으로 따로 검증해야 하고, Li₆PS₅Cl에서 본 힘 감쇠는 일반적 결과가 아니다. |
| `zhang2026_minimum_abinitio_data_mlip_mace_finetune_nep_distill` | Zhang et al. 2026 | Constructing machine learning interatomic potentials with minimum amount of ab initio data | 범용 MLIP는 평균 오차가 작아도 장벽과 확산계수를 크게 틀리며, 약 200개 DFT 파인튜닝과 NEP 증류로 이를 고칠 수 있다. |

# 스크리닝 · 기술자 · 머신러닝

전해질 · 계면 · 장 `se-ml` · 논문 20편 · 읽기 카드 20편

> 고속 계산 스크리닝, 기술자 설계, 능동학습과 대리모형.

## 장 서문 — 싼 대리값은 순위를 맞히지만 값과 외삽은 아직 못 믿는다

*읽기 카드 20편을 엮어 쓴 글 · 항목 30개 중 30개 검증 통과 · 2026-11-10*

고속 스크리닝, 기술자 설계, 능동학습 논문들은 비싼 계산이나 실험을 싼 대리값으로 얼마나 대신할 수 있는지를 묻는다. [근거: Sendek et al. 2017 (`sendek2017_ml_screening_12k_conductors`); Kahle et al. 2020 (`kahle2020_ht_aimd_screening`); Hu, Dong, Feng, Hu & Hu 2026 (`hu2026_foundation_model_surrogates_active_learning`)]

대리값은 후보를 거르고 순위를 매기는 데까지는 해낸다. 절대값을 맞히는 일과 처음 보는 원소나 화학족에서 맞히는 일은 아직 보증하지 못한다. [근거: Kahle et al. 2020 (`kahle2020_ht_aimd_screening`); Sjølin et al. 2023 (`sjolin2023_accelerated_workflow_antiperovskite_sse`); Steven K. Kauwe 박사학위논문 2021 (`kauwe2021_ml_materials_properties_dissertation_sparks`)]

능동학습의 이득은 무작위 대조군 없이 보고되어 아직 그 크기를 말할 수 없다. [근거: Ma et al. 2025 (`ma2025_active_learning_electrolyte_solvent_screening_anodefree`); Hu, Dong, Feng, Hu & Hu 2026 (`hu2026_foundation_model_surrogates_active_learning`); Aqib et al. 2026 (`aqib2026_multifidelity_active_learning_alloy_design`)]

### 어느 단이 거르나

여러 깔때기에서 후보를 가장 많이 줄인 것은 전도도 예측이 아니라 안정성과 전기화학 게이트였다. Sendek et al. 2017은 Li 함유 12,831종에 네 게이트를 걸어 317종을 남겼고, 분류기를 거쳐 21종이 남았다. 같은 분류기만 쓰면 1,408종이 남았다. Sjølin et al. 2023의 antiperovskite 깔때기에서는 hull 단이 가장 강했고, 1317 조성에서 남은 14종은 모두 이미 알려진 물질이었다. Jung et al. 2026에서는 DFT 전기화학 창 단계의 탈락률이 97.6 %였다. [근거: Sendek et al. 2017 (`sendek2017_ml_screening_12k_conductors`); Sjølin et al. 2023 (`sjolin2023_accelerated_workflow_antiperovskite_sse`); Jung et al. 2026 (`jung2026_scalable_ai_dual_doped_lgps`)]

게이트를 통과한 뒤의 개선 폭과 대조 기준은 얇다. Jung et al. 2026에서 21종과 LGPS의 V_red는 모두 1.717 V였고, 검토 측은 개선이 산화쪽 +60 mV뿐이라고 본다. Honrao et al. 2021은 자체 DFT 없이 softBV 장벽과 grand-potential 창으로 코팅 후보 26종을 골랐고, 계면 반응에너지는 계산하지 않았다. Park et al. 2026의 Ni 불화물 다섯 종도 이온 수송 단이 없는 깔때기에서 나왔다. 검토 측은 Jain et al. 2026 리뷰가 옮긴 13건 캠페인 중 입력과 통과 수를 밝힌 것이 2건뿐이라고 본다. [근거: Jung et al. 2026 (`jung2026_scalable_ai_dual_doped_lgps`); Honrao et al. 2021 (`honrao2021_interpretable_ml_sse_anode_coatings`); Park et al. 2026 (`park2026_mattergen_fluoride_ion_electrolyte`); Jain et al. 2026 (`jain2026_ml_pipelines_solid_state_electrolyte_design`)]

### 대리값은 순위까지

싼 대리 계산은 비싼 계산의 값을 재현하지 못하고 순위만 맞혔다. Kahle et al. 2020 원문은 pinball이 FPMD 확산계수를 정량 재현하지 못한다고 스스로 적었다. 대신 pinball 최상위 분위 후보의 71%가 FPMD 기준을 넘었고, 최하위 분위는 21%였다. Sjølin et al. 2023의 S-NEB는 CI-NEB 대비 MAE 73 meV였고, 원문은 장벽 추정보다 순위 매기기에 더 맞는다고 적었다. 검토 측은 기준 CI-NEB가 내부 이미지 1개뿐이고 w_S를 같은 표본에서 적합했으므로 73 meV를 적합잔차로 본다. [근거: Kahle et al. 2020 (`kahle2020_ht_aimd_screening`); Sjølin et al. 2023 (`sjolin2023_accelerated_workflow_antiperovskite_sse`)]

경험적 장벽이나 문헌 라벨 위의 회귀 성능도 같은 단서를 단다. Zhao et al. 2021 원문은 시험 R² 0.820을 보고했지만, 검토 측은 정의대로 계산하면 0.7661이라고 본다. Honrao et al. 2021 원문은 softBV 장벽으로 이온전도도를 바로 추정하지 말라고 적었다. Fujimura et al. 2013의 SVR은 log σ 예측오차가 0.373이고, 검토 측은 예측 지도를 등급으로만 읽어야 한다고 본다. 우리 BVSE 실측에서는 comp1 E_3D 0.2734가 modelc 0.4785보다 낮아 MD 순위와 정반대였고, 그래서 우리는 Zhao 모델을 도펀트 랭킹의 채점 함수로 쓰지 않는다. [근거: Zhao et al. 2021 (`zhao2021_hecs_descriptors_argyrodite_activation_energy`); Honrao et al. 2021 (`honrao2021_interpretable_ml_sse_anode_coatings`); Fujimura et al. 2013 (`fujimura2013_ml_conductivity_origin`)]

### 무엇이 확산을 정하나

확산을 설명하는 구조 기술자는 여럿 나왔지만 가리키는 물리가 서로 다르다. Fujimura et al. 2013은 92조성에서 D₁₆₀₀이 격자 부피와 거의 무관하고 팔면체 Li 점유율 p_Oct가 1차 인자라고 적었다. Honrao et al. 2021의 GB 회귀에서는 부격자 충전율 SPF가 PFI 0.31로 1위였다. Kim et al. 2025는 황화물 네 조성에서 준안정 edge-sharing 상의 600 K 확산계수가 corner-sharing 상보다 at least 2 orders of magnitude 높다고 적었다. 검토 측은 그 차이가 두 조성에서만 깨끗하고, σ는 한 번도 계산되지 않았다고 본다. [근거: Fujimura et al. 2013 (`fujimura2013_ml_conductivity_origin`); Honrao et al. 2021 (`honrao2021_interpretable_ml_sse_anode_coatings`); Kim et al. 2025 (`kim2025_csp_metastable_edge_sharing_sse`)]

아지로다이트에서는 두 기술자가 다른 라벨 위에서 경쟁한다. Zhao et al. 2021은 BVSE 라벨에서 음이온 평균 반경 r_anion을 VIP 1위로 꼽았고, Li 함량 기술자는 컷 아래였다. 검토 측은 BVSE가 Li–Li 상관을 보지 못하므로 이 결과가 라벨의 성질이라고 본다. Jun · Lee 2022는 AIMD 45개 배열에서 케이지 반지름 STD가 작을수록 전도도가 높다고 보고했다. 검토 측은 이 기술자가 조성 층위에서는 유효하지만, 할로겐 과잉 9개 조성군 중 4개에서 최소 STD 배열이 최속이 아니었다고 본다. [근거: Zhao et al. 2021 (`zhao2021_hecs_descriptors_argyrodite_activation_energy`); Jun · Lee 2022 (`jun2022_argyrodite_ion_cage_size_descriptor`)]

### 고온 외삽과 실측

고온 계산을 실온으로 외삽한 값은 여러 논문에서 근거가 약하다. Fujimura et al. 2013 원문은 523 K 아래에서 실험 활성화에너지가 커지는 굴절을 팔면체 Li 질서화로 해석하고, 이를 ML 도입의 근거로 삼았다. Jung et al. 2026의 Li₉P₃OS₁₁은 외삽 σ가 17.28 mS/cm였다. 검토 측은 이 물질의 확산계수가 1300 K에서 네 종 중 최하위라서 1위가 외삽에서만 생긴다고 본다. Jain et al. 2026 리뷰도 확산 기구가 바뀌거나 상전이가 있으면 Arrhenius 외삽을 믿기 어렵다고 경고했다. [근거: Fujimura et al. 2013 (`fujimura2013_ml_conductivity_origin`); Jung et al. 2026 (`jung2026_scalable_ai_dual_doped_lgps`); Jain et al. 2026 (`jain2026_ml_pipelines_solid_state_electrolyte_design`)]

비교 기준이 되는 실측값도 하나로 정해지지 않는다. Cho et al. 2025의 A1은 관행 프로토콜에서 7.45 mS/cm, 가압 프로토콜에서 13.02 mS/cm였다. 검토 측은 계산과 실험이 잘 맞는 그림이 가압 값을 골라야 성립한다고 본다. Jun · Lee 2022에 대해 검토 측은 Li₆PS₅I의 PBE AIMD 값 0.84 mS/cm가 실험 대비 200–400× 과대라고 적었다. Kahle et al. 2020에서는 Li₆PS₅I의 1000 K와 750 K D_Li가 사실상 같았고, 검토 측은 이를 cage 안 rattling을 D로 읽은 것으로 본다. [근거: Cho et al. 2025 (`cho2025_multicompositional_argyrodite_experimental_active_learning`); Jun · Lee 2022 (`jun2022_argyrodite_ion_cage_size_descriptor`); Kahle et al. 2020 (`kahle2020_ht_aimd_screening`)]

### 분할과 대조군

보고된 ML 성능의 다수는 랜덤 분할이나 같은 데이터 안의 검증에서 나왔다. Kauwe 2021 학위논문은 같거나 비슷한 데이터가 train과 test에 함께 있지 않게 하라고 규정했다. 학습에 없던 원소로 넘어가자 그림에서 읽은 logistic 평균 PR-AUC가 0.79에서 0.54로 떨어졌다. 검토 측은 Tu et al. 2027의 R² 0.99가 랜덤 90/10 분할과 입력 속 동결값 위의 값이라고 본다. Jain et al. 2026 리뷰는 LOGO-CV를 권하지만, 검토 측은 group-out 검증을 실제로 수행한 SSE 사례가 없다고 확인했고, 우리 쌍 LOOCV 0.0892에서 LODO −0.1805로 떨어진 결과가 그 자리에 들어간다. [근거: Steven K. Kauwe 박사학위논문 2021 (`kauwe2021_ml_materials_properties_dissertation_sparks`); Tu et al. 2027 (`tu2026_diffusion_descriptor_ml_li_sse_interface`); Jain et al. 2026 (`jain2026_ml_pipelines_solid_state_electrolyte_design`)]

능동학습 논문들은 무작위 탐색보다 나은지를 재지 않았다. Ma et al. 2025와 Hu et al. 2026에는 랜덤 팔이 없다. 검토 측은 Ma et al. 2025의 out-of-batch RMSE가 여섯 배치 모두 라벨 표준편차보다 컸다고 본다. 검토 측은 Aqib et al. 2026의 고정확도 평가 절감 대부분이 코드에 박힌 확률 스케줄에서 왔다고 본다. Cho et al. 2025는 검토 측이 1라운드를 무작위 기준으로 삼아 재계산하자 적중률 증가가 15×였고, 공정을 맞추면 4.5×로 줄었다. [근거: Ma et al. 2025 (`ma2025_active_learning_electrolyte_solvent_screening_anodefree`); Hu, Dong, Feng, Hu & Hu 2026 (`hu2026_foundation_model_surrogates_active_learning`); Aqib et al. 2026 (`aqib2026_multifidelity_active_learning_alloy_design`); Cho et al. 2025 (`cho2025_multicompositional_argyrodite_experimental_active_learning`)]

### 이 장의 값

| 값 | 표기 | 근거 |
|---|---|---|
| Sendek 깔때기 입력 Li 화합물 수 | 12,831종 | Sendek et al. 2017 (`sendek2017_ml_screening_12k_conductors`) |
| pinball 최상위 분위 FPMD 성공률 | 71% | Kahle et al. 2020 (`kahle2020_ht_aimd_screening`) |
| antiperovskite S-NEB 대 CI-NEB MAE | 73 meV | Sjølin et al. 2023 (`sjolin2023_accelerated_workflow_antiperovskite_sse`) |
| 아지로다이트 PLS 시험 R² 재계산 | 0.7661 | Zhao et al. 2021 (`zhao2021_hecs_descriptors_argyrodite_activation_energy`) |
| LGPS 이원도핑 DFT ECW 탈락률 | 97.6 % | Jung et al. 2026 (`jung2026_scalable_ai_dual_doped_lgps`) |
| A1 상온 σ, 관행 프로토콜 | 7.45 mS/cm | Cho et al. 2025 (`cho2025_multicompositional_argyrodite_experimental_active_learning`) |
| Li/SSE 계면 γf GBRT, 랜덤 분할 | R² 0.99 | Tu et al. 2027 (`tu2026_diffusion_descriptor_ml_li_sse_interface`) |
| γ-LISICON SVR log σ 예측오차 | 0.373 | Fujimura et al. 2013 (`fujimura2013_ml_conductivity_origin`) |

### 아직 열린 문제

- 능동학습과 다중정확도 탐색이 무작위 탐색보다 얼마나 적은 평가로 최적에 닿는지는 어느 논문도 대조군으로 재지 않았다. [근거: Ma et al. 2025 (`ma2025_active_learning_electrolyte_solvent_screening_anodefree`); Hu, Dong, Feng, Hu & Hu 2026 (`hu2026_foundation_model_surrogates_active_learning`); Aqib et al. 2026 (`aqib2026_multifidelity_active_learning_alloy_design`)]
- 아지로다이트 전도도를 가르는 기술자가 BVSE 라벨의 음이온 반경인지 AIMD의 케이지 크기 균일도인지 정해지지 않았다. edge-sharing이 유리하다는 황화물 결과도 corner-sharing이 좋다는 산화물 연구와 충돌한 채 남아 있다. [근거: Zhao et al. 2021 (`zhao2021_hecs_descriptors_argyrodite_activation_energy`); Jun · Lee 2022 (`jun2022_argyrodite_ion_cage_size_descriptor`); Kim et al. 2025 (`kim2025_csp_metastable_edge_sharing_sse`)]
- 싼 층에서 버린 후보 가운데 진짜 최적이 있었는지는 감사되지 않았다. MatterSim parity는 문턱 통과자만 그렸고, 다중정확도 저정확도 층과 3단 재채점 깔때기도 거짓 음성을 따로 재지 않았다. [근거: Park et al. 2026 (`park2026_mattergen_fluoride_ion_electrolyte`); Aqib et al. 2026 (`aqib2026_multifidelity_active_learning_alloy_design`); Basu 2026 (`basu2026_multifidelity_bandit_dopant_screening_funnel`)]
- 부분점유 무질서 구조는 MD 깔때기 입구에서 빠졌고, 치환 조성이 단상으로 존재하는지 판정하는 게이트도 없어 무질서 고용체 후보는 아직 체계적으로 걸러지지 않는다. [근거: Kahle et al. 2020 (`kahle2020_ht_aimd_screening`); Liu 2026 (`liu2026_ab_site_substitution_high_entropy_perovskite_al`)]

### 먼저 읽을 논문

1. Kahle et al. 2020 (`kahle2020_ht_aimd_screening`) — 대리 MD가 값은 틀리고 순위만 맞혔다는 이 장의 중심 결론을 깔때기 전체와 오차 규율로 보여 준다.
2. Sendek et al. 2017 (`sendek2017_ml_screening_12k_conductors`) — 물리 전제조건 게이트가 ML 분류기보다 후보를 더 많이 거른 깔때기의 원형이다.
3. Steven K. Kauwe 박사학위논문 2021 (`kauwe2021_ml_materials_properties_dissertation_sparks`) — 분할과 누출 규범, 처음 보는 원소 앞에서 ML이 약해진다는 결과가 뒤 논문들의 성능 수치를 읽는 잣대가 된다.
4. Jun · Lee 2022 (`jun2022_argyrodite_ion_cage_size_descriptor`) — 아지로다이트 기술자를 AIMD로 세우고 검토 측이 조성 층위와 배열 층위의 한계를 가른 사례다.
5. Hu, Dong, Feng, Hu & Hu 2026 (`hu2026_foundation_model_surrogates_active_learning`) — 능동학습 대리모형의 불확실도 보정 주장과 랜덤 팔이 빠진 비교 설계의 구멍을 함께 보여 준다.

## 이 장의 논문 (20편)

| digest | 저자 · 연도 | 제목 | 한 줄 결론 |
|---|---|---|---|
| `fujimura2013_ml_conductivity_origin` | Fujimura et al. 2013 | Accelerated Materials Design of Lithium Superionic Conductors Based on First‐Principles Calculations and Machine Learning Algorithms | 1600 K FPMD 확산계수, 전이온도 Tc, 부피를 실험 전도도 95점과 SVR로 묶어 γ-LISICON의 373 K 전도도 지도를 그렸다. |
| `sendek2017_ml_screening_12k_conductors` | Sendek et al. 2017 | Holistic computational structure screening of more than 12 000 candidates for solid lithium-ion conductor materials | 실측 40종으로 학습한 5특징 로지스틱 회귀와 네 가지 물리 게이트로 Li 화합물 12,831종을 21종으로 좁혔고, 전제조건 게이트가 더 많이 걸렀다. |
| `kahle2020_ht_aimd_screening` | Kahle et al. 2020 | High-throughput computational screening for solid-state Li-ion conductors | 실험 구조 4,963종을 pinball MD와 FPMD로 걸러 신규 fast-ion conductor 다섯 종을 찾았고, pinball은 값이 아닌 순위만 맞혔다. |
| `honrao2021_interpretable_ml_sse_anode_coatings` | Honrao et al. 2021 | Discovery of novel Li SSE and anode coatings using interpretable machine learning and high-throughput multi-property screening | softBV 장벽과 grand-potential 창으로 MP의 Li 화합물을 걸러 음극 코팅 26종을 뽑고, GB 회귀와 SHAP·PFI로 장벽을 좌우하는 특징을 짚었다. |
| `kauwe2021_ml_materials_properties_dissertation_sparks` | Steven K. Kauwe 박사학위논문 2021 | Machine Learning of Materials Properties | ML은 DFT 데이터 밖의 상위 1% 물질을 분류로 상당 부분 찾아내지만, 처음 보는 원소와 도핑 앞에서는 약하다. |
| `zhao2021_hecs_descriptors_argyrodite_activation_energy` | Zhao et al. 2021 | Machine learning prediction of activation energy in cubic Li-argyrodites with hierarchically encoding crystal structure-based (HECS) descriptors | BVSE 라벨 50개를 HECS 기술자 32개로 PLS 회귀하면 음이온 평균 반경이 Ea를 가장 잘 설명한다. |
| `jun2022_argyrodite_ion_cage_size_descriptor` | Jun · Lee 2022 | Designing a descriptor for the computational screening of argyrodite-based solid-state superionic conductors: uniformity of ion-cage size | free anion 주위 Li 케이지 반지름의 표준편차가 작을수록 아지로다이트의 Li⁺ 전도도가 높다. |
| `sjolin2023_accelerated_workflow_antiperovskite_sse` | Sjølin et al. 2023 | Accelerated Workflow for Antiperovskite‐based Solid State Electrolytes | 대리 NEB는 CI-NEB의 상위 후보 집합을 싸게 재현했다. 다만 1317 조성 스크리닝이 남긴 14종은 모두 이미 알려진 물질이었다. |
| `cho2025_multicompositional_argyrodite_experimental_active_learning` | Cho et al. 2025 | Discovering Multi‐Compositional Li‐Argyrodite Solid‐State Electrolytes via Experimental Active Learning | 대리모델 없이 실측 σ로 PSO를 다섯 라운드 돌려 P-free Ge-Si-Sb argyrodite A1을 찾았고, Ge는 음극쪽 안정성을 높였다. |
| `kim2025_csp_metastable_edge_sharing_sse` | Kim et al. 2025 | Machine Learning-Assisted Crystal Structure Prediction of Solid-State Electrolytes Reveals Superior Ionic Conductivity in Metastable Edge-Sharing Phases | MTP 기반 CSP로 찾은 황화물 네 조성에서 준안정 edge-sharing 상이 가장 안정한 corner-sharing 상보다 600 K Li 확산계수가 크다. |
| `ma2025_active_learning_electrolyte_solvent_screening_anodefree` | Ma et al. 2025 | Active learning accelerates electrolyte solvent screening for anode-free lithium metal batteries | 가우스 과정 네 개를 합친 대리모델과 기대 개선 획득으로 일곱 라운드를 돌려 F5DEE와 비슷한 용량의 에테르 용매를 찾았다. |
| `aqib2026_multifidelity_active_learning_alloy_design` | Aqib et al. 2026 | A multi-fidelity active learning framework for accelerated alloy design | 세 방법이 모두 같은 Invar 조성에 닿지만, MFAL의 고정확도 절감은 코드에 박힌 확률 스케줄에서 나온다고 검토 측은 본다. |
| `basu2026_multifidelity_bandit_dopant_screening_funnel` | Basu 2026 | Accelerated Dopant Screening in Oxide Semiconductors via Multi-Fidelity Contextual Bandits and a Three-Tier DFT Validation Funnel | MF-OFUL은 DFT 호출 상당 부분을 대리모델로 대신했고, PBE+U와 이온완화 재채점은 PBE 단독의 정성적 오분류를 드러냈다. |
| `hu2026_foundation_model_surrogates_active_learning` | Hu, Dong, Feng, Hu & Hu 2026 | Foundation-Model Surrogates Enable Data-Efficient Active Learning for Materials Discovery | TabPFN을 대리모형으로 쓰면 최적점 탐색에 드는 추가 평가 수가 줄고, 원문은 그 원인을 정확도보다 불확실도 보정에서 찾는다. |
| `jain2026_ml_pipelines_solid_state_electrolyte_design` | Jain et al. 2026 | Machine learning pipelines for the design of solid-state electrolytes | 원문은 SSE 발견의 ML 파이프라인을 네 단으로 정리했고, 검토 측은 깔때기의 성능 회계가 비어 있다고 본다. |
| `jung2026_scalable_ai_dual_doped_lgps` | Jung et al. 2026 | Scalable AI-accelerated design of dual-doped LGPS electrolytes for next-generation solid-state batteries | ML 대리모형, DFT 전기화학 창, AIMD로 LGPS 이원도핑 후보를 네 종까지 좁혔지만 환원 한계는 모든 후보에서 같았다. |
| `liu2026_ab_site_substitution_high_entropy_perovskite_al` | Liu 2026 | Substitutional Effects at A- and B-Sites in High-Entropy ABO₃ Perovskites: Insights from Machine Learning-Accelerated Simulations and Active Learning — G. Liu et al. (WPI) | LaCoO₃의 A자리와 B자리를 따로 5원 고엔트로피화해 MLIP 라벨과 BNN 능동학습으로 조성-물성 지도를 만들었지만, 상 존재 판정은 없다. |
| `park2026_mattergen_fluoride_ion_electrolyte` | Park et al. 2026 | Generative Inverse Design of Solid-State Fluoride-Ion Electrolyte Candidates in Data-Sparse Chemical Space | Ehull만 조건으로 건 MatterGen과 다단 선별로 F⁻ 전해질 후보 Ni 불화물 다섯 종을 얻었으나 이온 수송은 확인하지 않았다. |
| `sun2026_ml_sulfur_additive_lnmo_graphite_bdtt` | Sun et al. 2026 | Screening “Cathode-Stable and Anode-Reactive” Sulfur-Based Additives for LiNi0.5Mn1.5O4\|\|Graphite Pouch Cells via a Machine Learning Approach | ML로 S=O가 HOMO를 낮춘다는 원리를 얻고 DFT로 BDTT를 골라 45 °C 파우치 유지율을 크게 올렸다고 보고하지만, 산화 쪽 검증은 없다. |
| `tu2026_diffusion_descriptor_ml_li_sse_interface` | Tu et al. 2027 | A diffusion descriptor integrated machine learning approach toward the discovery of solid-state electrolytes for lithium metal batteries | 전해질을 얼린 싼 계산값을 기술자로 넣으면 계면 형성에너지와 장벽을 높은 R²로 맞히지만, 그 R²는 랜덤 분할 위의 값이다. |

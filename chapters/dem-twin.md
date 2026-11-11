# 디지털 트윈과 최적화

전극 미세구조 · 공정 · 장 `dem-twin` · 논문 9편 · 읽기 카드 9편

> 제조 사슬의 대리모형과 다목적 최적화.

## 장 서문 — 대리모형의 가속은 물리 투영과 단순 기준선에 기댄다

*읽기 카드 9편을 엮어 쓴 글 · 항목 30개 중 30개 검증 통과 · 2026-11-10*

전극 미세구조를 가상으로 만들고, 제조 사슬의 비싼 물리 계산을 대리모형으로 줄이고, 그 위에서 조성과 공정을 고르는 것이 여기서 다루는 질문이다. [근거: Park et al. 2020 (`park2020_digitaltwin_assb_foundational`); Duquesnoy et al. 2023 (`duquesnoy2023_ml_multiobjective_manufacturing_optimization`); Galvez‐Aranda et al. 2024 (`galvezaranda2024_time_dependent_dl_calendering_microstructure`); Galvez-Aranda et al. 2025 (`galvezaranda2025_paml_vgg16_dem_slurry_drying`); Vijay et al. 2025 (`vijay2025_hybrid_cgmd_dl_slurry_microstructure`); Wang et al. 2027 (`wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn`)]

규칙기반 디지털트윈과 물리 합성데이터 위의 베이지안 최적화는 설계창과 최적 조건을 내놓았고, 그 일부를 실험과 맞췄다. [근거: Park et al. 2020 (`park2020_digitaltwin_assb_foundational`); Duquesnoy et al. 2023 (`duquesnoy2023_ml_multiobjective_manufacturing_optimization`)]

대리모형들은 계산 시간을 줄였다고 보고했다. 검토 측은 구조를 실제로 만드는 것이 뒤에 붙은 물리 계산이라고 보고, 단순 기준선도 같은 몫을 한다고 본다. [근거: Galvez‐Aranda et al. 2024 (`galvezaranda2024_time_dependent_dl_calendering_microstructure`); Galvez-Aranda et al. 2025 (`galvezaranda2025_paml_vgg16_dem_slurry_drying`); Vijay et al. 2025 (`vijay2025_hybrid_cgmd_dl_slurry_microstructure`); Wang et al. 2027 (`wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn`)]

### 구조를 만드는 두 길

두 총설은 3D 구조체 형성을 두 갈래로 나눴다. 하나는 영상에서 재구성하는 하향식이고, 다른 하나는 설계 파라미터에서 생성하는 상향식이다. Choi 2024와 Kim 2024는 전극 스케일(10⁻⁴ m)에 DEM과 FVM을 놓았다. 검토 측은 두 총설의 상향식에 확률적 생성이 포함된다고 본다. 그래서 압축 물리로 구조를 만드는 방식과는 구분해야 한다는 판단이다. Choi 2024는 동료심사를 거치지 않은 매거진 총설이어서 검토 측은 이를 분류와 어휘의 근거로만 쓴다. [근거: Choi 2024 (`choi2024_digital_twin_review_echem`); Kim et al. 2024 (`kim2024_digital_twin_acsenergyletters`)]

장 안의 논문들은 구조를 만드는 방식이 서로 다르다. Park 2020은 압축을 계산하지 않고 PSA와 SEM 자료에 따라 입자를 규칙으로 배치했다. LPSCl은 NCM 사이 간극에 놓았다. Duquesnoy 2023, Galvez-Aranda 2024, Galvez-Aranda 2025, Vijay 2025는 CGMD 슬러리, 건조, DEM 압연으로 이어지는 물리 사슬에서 구조를 얻었다. Wang 2027은 BIB-SEM 영상으로 학습한 생성기로 부피 하나를 재구성했다. 우리 DEM+MPM은 bottom-up 형성 범주 가운데 압축 역학으로 구조를 만드는 process-physics 하위유형으로 자리매김한다. [근거: Park et al. 2020 (`park2020_digitaltwin_assb_foundational`); Duquesnoy et al. 2023 (`duquesnoy2023_ml_multiobjective_manufacturing_optimization`); Galvez‐Aranda et al. 2024 (`galvezaranda2024_time_dependent_dl_calendering_microstructure`); Galvez-Aranda et al. 2025 (`galvezaranda2025_paml_vgg16_dem_slurry_drying`); Wang et al. 2027 (`wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn`); Kim et al. 2024 (`kim2024_digital_twin_acsenergyletters`)]

### 조성과 공정의 설계창

Park 2020에서 조성 설계창을 정한 것은 고립 입자와 이온 경로의 끊김이다. NCM 90 wt%에서는 LPSCl dead particle이 seed에 따라 최대 19.82%까지 늘었고, 유효 이온 전도도는 계산할 수 없었다. 원문은 NCM 60–80 wt%를 적절한 설계 범위로 결론지었다. NCM이 60에서 80 wt%로 늘면 0.1C에서도 비용량이 20 mAh/g 줄었다. 원문은 이 감소를 접촉 면적이 줄어든 탓으로 보았다. [근거: Park et al. 2020 (`park2020_digitaltwin_assb_foundational`)]

Duquesnoy 2023의 공정 최적해는 범위의 끝이 아니라 균형점에 놓였다. 베이지안 다목적최적화가 고른 조건은 AM% 90.4, SC% 58.1, CD% 28.4다. 한 물성만 극대화한 극단 조건은 다른 물성을 잃었다. 반올림한 조건으로 만든 실제 전극의 tortuosity factor는 1.8 ± 0.4였다. 두 논문은 다루는 계가 다르다. Park 2020은 LPSCl 복합양극이고, Duquesnoy 2023은 액체 전해질 습식 NMC111 양극이다. [근거: Duquesnoy et al. 2023 (`duquesnoy2023_ml_multiobjective_manufacturing_optimization`); Park et al. 2020 (`park2020_digitaltwin_assb_foundational`)]

### 가속은 어디서 오나

세 대리모형은 모두 물리 궤적의 일부를 건너뛰고, 그 뒤에 다시 물리 계산을 붙인다. Galvez-Aranda 2025에서 짧은 DEM 투영은 학습 조성의 porosity 오차를 nDEM 0의 59.7 %에서 nDEM 5000의 3.9 %로 줄였다. 검토 측은 구조를 만드는 것이 이 물리 투영자라고 본다. Vijay 2025의 예측 구조도 NEMD에 바로 넣으면 입자가 사라졌다. 그래서 CGMD 평형화 한 스텝을 거쳐야 했다. [근거: Galvez-Aranda et al. 2025 (`galvezaranda2025_paml_vgg16_dem_slurry_drying`); Vijay et al. 2025 (`vijay2025_hybrid_cgmd_dl_slurry_microstructure`)]

보고된 가속 배수는 검토 측이 다시 계산하면 크게 줄어든다. Galvez-Aranda 2024에 대해 검토 측은 매 프레임 실제 DEM lag를 먹인 채점이라면 188×가 대리모형 가속이 아니라고 본다. 다만 이를 단정하지는 않는다. Galvez-Aranda 2025의 본문 배수 14.25×는 시드 프레임 비용을 넣으면 검토 측 계산으로 4.77×가 된다. Vijay 2025에는 가속 배수가 없고, 검토 측이 유도한 상한은 사슬 전체 ≈1.10–1.13×다. [근거: Galvez‐Aranda et al. 2024 (`galvezaranda2024_time_dependent_dl_calendering_microstructure`); Galvez-Aranda et al. 2025 (`galvezaranda2025_paml_vgg16_dem_slurry_drying`); Vijay et al. 2025 (`vijay2025_hybrid_cgmd_dl_slurry_microstructure`)]

### 단순 기준선과의 비교

학습 모형을 단순 기준선과 나란히 놓은 두 논문에서는 기준선이 대부분을 설명했다. Vijay 2025는 10번째 프레임 좌표를 아핀 스케일링한 기준선을 두었다. ASSB AM–AM RDF에서 예측의 Fréchet 거리는 0.564로, 기준선의 0.314보다 컸다. 검토 측은 신경망이 구조 완화가 아니라 아핀 축소를 재현했다고 본다. Wang 2027에서는 CBD-기공 분율 φ 하나의 이차식이 5 분할 평균 R² 0.905 ± 0.003으로 GNN의 0.880 ± 0.013을 앞섰다. [근거: Vijay et al. 2025 (`vijay2025_hybrid_cgmd_dl_slurry_microstructure`); Wang et al. 2027 (`wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn`)]

Hollmann 2025는 소규모 표 데이터에서 튜닝 없이 쓰는 학습기를 제시했다. 원문에서 기본값 TabPFN은 10,000행·500특징 이하의 벤치마크에서 4시간 튜닝한 CatBoost·XGBoost보다 높은 점수를 냈다. 원문은 이 모형이 외삽에 취약하고 해석가능성을 보장하지 않는다고 적었다. 우리 코퍼스는 n=88–132 케이스 규모여서 TabPFN이 강한 영역에 든다. 우리는 이를 물리 스케일링 법칙의 대체가 아니라 빠른 베이스라인과 잔차 신호 탐색에 쓴다. [근거: Hollmann 2025 (`hollmann2025_tabpfn_tabular_foundation_model`)]

### 무엇과 견주어 검증하나

여러 논문이 보고한 일치는 독립 실험이 아니라 물리 계산이나 자기 데이터와의 일치다. 검토 측은 Park 2020의 LPSCl 고유 전도도 식이 자기 실측에 맞춘 것이라면 이온 쪽 일치가 일부 순환이 된다고 본다. Galvez-Aranda 2024의 비교 기준은 DEM이고 신규 실험이 없다. Wang 2027의 조각은 모두 재구성 부피 하나에서 나왔고, K는 복셀 FE 라벨이다. Duquesnoy 2023의 σ_e는 실험으로 측정되지 않았다. [근거: Park et al. 2020 (`park2020_digitaltwin_assb_foundational`); Galvez‐Aranda et al. 2024 (`galvezaranda2024_time_dependent_dl_calendering_microstructure`); Wang et al. 2027 (`wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn`); Duquesnoy et al. 2023 (`duquesnoy2023_ml_multiobjective_manufacturing_optimization`)]

고체전지로 옮길 수 있는 것은 값보다 방법이다. Duquesnoy 2023의 tortuosity는 pore 이온 proxy여서 우리 ASSB의 σ_ionic과 압력 의존 부호가 반대다. Galvez-Aranda 2024는 압축을 압력이 아니라 CD %로 나타냈기 때문에 MPa 축으로 옮길 점이 없다. Vijay 2025의 ASSB 계산은 슬러리 단계에서 멈춰 압연 공극률이 없다. NMC-111의 41–54 % 공극률은 액체 전해질 LIB 값이어서 우리 ASSB 10–16 %와 절대 비교하지 않는다. [근거: Duquesnoy et al. 2023 (`duquesnoy2023_ml_multiobjective_manufacturing_optimization`); Galvez‐Aranda et al. 2024 (`galvezaranda2024_time_dependent_dl_calendering_microstructure`); Vijay et al. 2025 (`vijay2025_hybrid_cgmd_dl_slurry_microstructure`)]

### 이 장의 값

| 값 | 표기 | 근거 |
|---|---|---|
| NCM 90 wt% LPSCl dead particle 최대 | 19.82% | Park et al. 2020 (`park2020_digitaltwin_assb_foundational`) |
| NCM 60에서 80 wt% 비용량 감소, 0.1C | 20 mAh/g | Park et al. 2020 (`park2020_digitaltwin_assb_foundational`) |
| NMC111 BO 최적 AM% | 90.4 | Duquesnoy et al. 2023 (`duquesnoy2023_ml_multiobjective_manufacturing_optimization`) |
| 최적조건 전극 실측 tortuosity factor | 1.8 ± 0.4 | Duquesnoy et al. 2023 (`duquesnoy2023_ml_multiobjective_manufacturing_optimization`) |
| 압연 1D-CNN 단계당 추론 시간 | 15 s / step | Galvez‐Aranda et al. 2024 (`galvezaranda2024_time_dependent_dl_calendering_microstructure`) |
| 건조 하이브리드 본문 가속 배수 | 14.25× | Galvez-Aranda et al. 2025 (`galvezaranda2025_paml_vgg16_dem_slurry_drying`) |
| 시드 포함 가속 천장, 검토 측 계산 | 6.67× | Galvez-Aranda et al. 2025 (`galvezaranda2025_paml_vgg16_dem_slurry_drying`) |
| NCM811 K, φ 이차식 5 분할 평균 R² | 0.905 ± 0.003 | Wang et al. 2027 (`wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn`) |

### 아직 열린 문제

- Galvez-Aranda 2024의 추론 프로토콜은 적혀 있지 않다. 대리모형이 자기 출력만으로 궤적을 이어 가는지, 매 프레임 DEM 값을 받는지가 정해지지 않았다. 검토 측은 이를 가장 큰 미해결 문제로 본다. [근거: Galvez‐Aranda et al. 2024 (`galvezaranda2024_time_dependent_dl_calendering_microstructure`)]
- 학습 범위 밖으로의 일반화는 어느 논문에서도 확인되지 않았다. 검토 측은 Galvez-Aranda 2025의 외삽 heat map이 학습 조성 heat map의 행 치환 복사본이라고 본다. Galvez-Aranda 2024는 CD 20–50 % 밖에서 비물리적 거동이 나올 수 있다고 적었다. Wang 2027은 부피 사이 일반화를 보이지 않았다. [근거: Galvez-Aranda et al. 2025 (`galvezaranda2025_paml_vgg16_dem_slurry_drying`); Galvez‐Aranda et al. 2024 (`galvezaranda2024_time_dependent_dl_calendering_microstructure`); Wang et al. 2027 (`wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn`)]
- 고체전지의 압력 축에서 돌아가는 대리모형은 아직 없다. Park 2020은 압력 변화를 다루지 않았고, Galvez-Aranda 2025에는 압력이나 응력 변수가 없다. 우리는 surrogate의 축이 TF가 아니라 wallP여야 한다고 본다. [근거: Park et al. 2020 (`park2020_digitaltwin_assb_foundational`); Galvez-Aranda et al. 2025 (`galvezaranda2025_paml_vgg16_dem_slurry_drying`)]
- Park 2020의 유효 전도도 일치는 아직 열린 문제다. 원문에는 tortuosity 값과 산출법이 없다. 검토 측 판독으로는 전자 실험점이 시뮬레이션 범위 위쪽에, 이온 실험점이 아래쪽에 붙는다. [근거: Park et al. 2020 (`park2020_digitaltwin_assb_foundational`)]

### 먼저 읽을 논문

1. Kim et al. 2024 (`kim2024_digital_twin_acsenergyletters`) — 동료심사를 거친 총설로 top-down과 bottom-up 분류와 숨겨진 미세구조 파라미터의 어휘를 먼저 잡아 준다.
2. Park et al. 2020 (`park2020_digitaltwin_assb_foundational`) — 우리와 같은 NCM711, LPSCl, NBR 계의 디지털트윈이라 설계창과 검증의 한계를 가장 가까운 계에서 보여 준다.
3. Duquesnoy et al. 2023 (`duquesnoy2023_ml_multiobjective_manufacturing_optimization`) — 물리 합성데이터, 대리모델, 베이지안 최적화, 실험 확인으로 닫힌 최적화 loop 전체를 한 편에서 보여 준다.
4. Galvez-Aranda et al. 2025 (`galvezaranda2025_paml_vgg16_dem_slurry_drying`) — DL이 프레임을 건너뛰고 DEM이 되돌리는 분해와 가속 배수에 대한 검토 측 재계산을 함께 보여 준다.
5. Wang et al. 2027 (`wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn`) — 단순 조성 기준선이 학습 모형을 앞서는 사례로, 대리모형을 기준선과 견주는 규율을 보여 준다.

## 이 장의 논문 (9편)

| digest | 저자 · 연도 | 제목 | 한 줄 결론 |
|---|---|---|---|
| `park2020_digitaltwin_assb_foundational` | Park et al. 2020 | Digital Twin‐Driven All‐Solid‐State Battery: Unraveling the Physical and Electrochemical Behaviors | 규칙기반 3D 디지털트윈 전극으로 NCM 60–80 wt%가 적절하고 90 wt%에서는 LPSCl 이온 경로가 끊긴다는 것을 보였다. |
| `duquesnoy2023_ml_multiobjective_manufacturing_optimization` | Duquesnoy et al. 2023 | Machine learning-assisted multi-objective optimization of battery manufacturing from synthetic data generated by physics-based simulations | 제조 시뮬레이션 합성데이터에 SISSO 대리모델과 베이지안 다목적최적화를 얹어 NMC111 양극의 균형 제조조건을 찾고 실험으로 확인했다. |
| `choi2024_digital_twin_review_echem` | Choi 2024 | Choi 2024 (E.Chem 매거진 총설, Vol.16 No.1) — 디지털 트윈 모델링·시뮬레이션 우리 DEM+MPM의 top-down/bottom-up POSITIONING을 NAMING하는 framework 리뷰 | 배터리 디지털 트윈은 미세구조의 숨겨진 파라미터를 찾는 도구이고, 3D 구조체는 하향식과 상향식 두 방법으로 만든다. |
| `galvezaranda2024_time_dependent_dl_calendering_microstructure` | Galvez‐Aranda et al. 2024 | Time‐Dependent Deep Learning Manufacturing Process Model for Battery Electrode Microstructure Prediction | 직전 세 프레임으로 다음 복셀 격자를 내는 1D-CNN이 DEM 압연을 재현하지만, 계면 오차가 가장 크고 추론 방식은 적혀 있지 않다. |
| `kim2024_digital_twin_acsenergyletters` | Kim et al. 2024 | Digital Twin Battery Modeling and Simulations: A New Analysis and Design Tool for Rechargeable Batteries | 디지털 트윈의 3D 구조 생성을 top-down 재구성과 bottom-up 형성으로 나누고, 숨겨진 미세구조 파라미터와 성능의 연결을 정리한 총설이다. |
| `galvezaranda2025_paml_vgg16_dem_slurry_drying` | Galvez-Aranda et al. 2025 | Physics-Assisted Machine Learning for the Simulation of the Slurry Drying in the Manufacturing Process of Battery Electrodes: A Hybrid Time-Dependent VGG16-DEM Model | 입자별 CNN이 건조 DEM 프레임을 통째로 건너뛰고, 수천 step의 실제 DEM이 겹침을 풀어 구조를 만든다. |
| `hollmann2025_tabpfn_tabular_foundation_model` | Hollmann 2025 | Hollmann 2025 — TabPFN: 소데이터 표형(tabular) 파운데이션 모델 (Nature) | 합성 데이터셋으로 사전학습한 TabPFN은 경사하강 없이 한 번의 forward pass로 소규모 표 데이터에서 튜닝된 GBDT를 능가한다. |
| `vijay2025_hybrid_cgmd_dl_slurry_microstructure` | Vijay et al. 2025 | A hybrid modelling approach coupling physics-based simulation and deep learning for battery electrode manufacturing simulations | CGMD 슬러리 앞 10 프레임으로 평형 좌표를 예측하는 Slurry-NN을 넣어도 점도와 압연 공극률은 순수 물리 계산과 비슷했다. |
| `wang2027_ncm811_effective_bulk_modulus_mapper_dfs_gnn` | Wang et al. 2027 | Accelerating NCM811 cathode effective bulk-modulus prediction for lithium-ion batteries: A geometry-reduction-based graph neural network | Mapper-DFS 그래프 GNN은 3D CNN보다 계산 시간을 크게 줄였지만, CBD-기공 분율 하나의 이차식이 GNN보다 K를 더 잘 맞췄다. |

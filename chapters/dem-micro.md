# 복합양극 미세구조

전극 미세구조 · 공정 · 장 `dem-micro` · 논문 68편 · 읽기 카드 68편

> 공극률, 굴곡도, 이온 · 전자 경로의 연결성.

## 장 서문 — 복합양극의 이온 경로는 공극과 접촉이 막는다

*읽기 카드 68편을 엮어 쓴 글 · 항목 32개 중 32개 검증 통과 · 2026-11-10*

복합양극 안에서 이온과 전자가 어떤 경로로 흐르는지, 그리고 무엇이 그 경로를 끊는지가 이 장의 질문이다. [근거: Minnmann et al. 2021 (`minnmann2021_jes_charge_transport_bottlenecks`); Bielefeld et al. 2019 (`bielefeld2019_microstructural_modeling_composite_cathode`); Deysher et al. 2022 (`deysher2022_transport_mechanical_aspects_assb_review`)]

실험은 CAM이 적으면 전자 경로가, 많으면 이온 경로가 막힌다는 쪽으로 모였다. 공극, 바인더, 도전재가 이온 경로를 더 끊는다는 결과도 여러 편에서 나왔다. [근거: Minnmann et al. 2021 (`minnmann2021_jes_charge_transport_bottlenecks`); Minnmann et al. 2024 (`minnmann2024_microstructure_porosity_visualization`); Bielefeld et al. 2019 (`bielefeld2020_effective_ionic_conductivity_binder`); Cho et al. 2024 (`cho2024_conflicting_roles_conductive_additive`); Kim et al. 2024 (`kim2024_carbon_volumetric_occupation_se_domain`)]

굴곡도의 정의와 측정법은 논문마다 다르다. 그래서 값을 나란히 놓기 어렵고, 연속체 계산이 빠뜨린 접촉 저항의 크기도 아직 정해지지 않았다. [근거: Tjaden et al. 2018 (`tjaden2018_tortuosity_review_calculation_approaches`); Landesfeind et al. 2016 (`landesfeind2016_tortuosity_eis_electrodes_separators`); Nguyen et al. 2020 (`nguyen2020_electrode_tortuosity_factor`); Cooper et al. 2016 (`taufactor_tortuosity_factor_tomography_tool`); Bielefeld et al. 2019 (`bielefeld2020_effective_ionic_conductivity_binder`)]

### τ는 무엇을 재나

같은 이름의 굴곡도가 서로 다른 양을 가리킨다. Tjaden et al. 2018은 계산법을 기하 계열과 flux 계열로 나누었다. 원문은 같은 시료에서 flux 값이 기하 값보다 높다고 적었고, 검토 측은 그 배수를 세 쌍에서 1.24–1.59배로 계산했다. Landesfeind et al. 2016은 자신의 τ가 다른 문헌에서 흔히 τ²로 나타난다고 적었다. Wiedenmann et al. 2013과 Holzer et al. 2013은 격막에서 τ_geo가 1.62–1.87로 평평한 반면 EIS로 역산한 τ_elc는 2.02–5.61에 걸친다고 보고했고, 그 격차를 협착으로 설명했다. [근거: Tjaden et al. 2018 (`tjaden2018_tortuosity_review_calculation_approaches`); Landesfeind et al. 2016 (`landesfeind2016_tortuosity_eis_electrodes_separators`); Wiedenmann et al. 2013 (`wiedenmann2013_pore_structure_ion_conductivity_ceramic_diaphragms`); Holzer et al. 2013 (`holzer2013_constrictivity_effective_transport_porous_layers`)]

관통형 τ와 차단 임피던스로 얻는 τ_e는 균질한 구조에서만 같다. Nguyen et al. 2020의 2층 구조에서 관통형 τ는 방향과 무관하게 7.4였다. 같은 구조의 τ_e는 조밀층의 위치에 따라 4.0에서 11.9로 바뀌었다. Morasch et al. 2018은 총 이온 저항이 같아도 고저항층이 분리막 쪽에 있으면 차단 EIS의 겉보기 τ가 커진다고 보였다. Kaiser et al. 2018에서는 SE 분율 ε 0.3일 때 TLM 값이 Li⁺ 전류 값보다 거의 한 자릿수 높았다. [근거: Nguyen et al. 2020 (`nguyen2020_electrode_tortuosity_factor`); Morasch et al. 2018 (`morasch2018_binder_gradient_impedance_tortuosity`); Kaiser et al. 2018 (`kaiser2018_ion_transport_limitations_assb_sulfide_electrodes`)]

### 접촉 항이 빠진 계산

영상이나 복셀 위에서 푸는 연속체 계산은 SE 입자 사이의 접촉 저항을 담지 않는다. 그래서 검토 측은 그 결과를 상한으로 읽는다. Bielefeld et al. 2019의 유효 이온전도도 계산에서는 바인더만 넣어도 70 vol% AM의 τ²가 4.2에서 10으로 올랐다. Landesfeind et al. 2018은 액체 LIB 전극에서 EIS τ가 단층촬영값의 ~2배라고 보고했다. 원문은 그 원인으로 미해상 바인더와 탄소를 지목했고, 검토 측은 이를 추론으로 본다. [근거: Cooper et al. 2016 (`taufactor_tortuosity_factor_tomography_tool`); Bielefeld et al. 2019 (`bielefeld2020_effective_ionic_conductivity_binder`); Landesfeind et al. 2018 (`landesfeind2018_tortuosity_impedance_vs_tomography`)]

접촉 자체가 전도를 정한다는 실측도 있다. Otani et al. 2023은 순수 LPSCl 층의 전도 저하가 주로 입자 접촉 면적에서 온다고 결론지었다. 단일상 펠릿을 누르며 잰 Miß et al. 2026은 공극이 큰 영역에서는 계면 접촉이 전도도를 정하고, 공극이 작은 영역에서는 공극이 정한다고 적었다. [근거: Otani et al. 2023 (`otani2023_ionic_conductivity_path_resistance_separation_model`); Miß et al. 2026 (`miss2026_insitu_conductivity_porosity_pressure_compaction`)]

### 계산과 실측의 어긋남

실측과 맞대면 두 계산 계열의 오차가 고-CAM 조성에서 반대 방향으로 간다. Ketter et al. 2025의 복셀 저항망은 순수상 펠릿값만 입력으로 받았다. 검토 측은 이 망이 고-NCM 조성에서 σ_ion을 10.7–58× 과대 예측한다고 본다. Bazzoun et al. 2026의 RNM은 접촉 구속저항만 담으며, 검토 측은 그 값이 고-CAM에서 실측보다 낮다고 본다. Lee et al. 2026의 PTFE 양극 재구성에서는 복셀 FV로 계산한 σ_ion이 6.9 × 10⁻⁵ S cm⁻¹, 실측이 4.85 × 10⁻⁵ S cm⁻¹로 계산 쪽이 높았다. [근거: Ketter et al. 2025 (`ketter2025_resistor_network_models_predict_transport_properties`); Bazzoun et al. 2026 (`bazzoun2026_dem_fem_rnm_ionic`); Lee et al. 2026 (`lee2026_unveiling_ptfe_dry_electrode_digital_twin`)]

입계를 어떻게 넣느냐도 결과를 바꾼다. Neumann et al. 2021은 garnet의 입계를 입자 사이 복셀 면의 계면 조건으로 넣어야 유효 이온전도도 감소가 실험 자릿수에 다가간다고 보였다. 검토 측은 그 일치가 bulk σ를 낮춘 두 번째 조정 뒤에 얻은 결과라고 본다. [근거: Neumann et al. 2021 (`neumann2021_garnet_3d_structure_grain_boundaries_li_transport`)]

### 이온 병목의 원인

CAM이 늘면 이온 경로는 거듭제곱으로 빠르게 나빠진다. Minnmann et al. 2021은 NCM-622와 Li₆PS₅Cl 양극에서 42 vol%일 때 이온 τ² 4.3을 냈다. Kaiser et al. 2018은 LPSI 유리 전극에서 Bruggeman 지수 5.6–5.7을 보고했고, 검토 측은 이를 전인자가 있는 맞춤선의 국소 기울기로 본다. Bazzoun et al. 2026은 f_CAM 70/75/80 wt% 양극의 이온전도도를 0.137 / 0.101 / 0.065 mS/cm로 실측했다. [근거: Minnmann et al. 2021 (`minnmann2021_jes_charge_transport_bottlenecks`); Kaiser et al. 2018 (`kaiser2018_ion_transport_limitations_assb_sulfide_electrodes`); Bazzoun et al. 2026 (`bazzoun2026_dem_fem_rnm_ionic`)]

공극은 부피보다 SE 통로를 잘게 나누는 형태로 이온 수송을 막는다. Hlushkou et al. 2018의 재구성에서 공극을 SE로 채우자 τ_diff가 1.74에서 1.27로 떨어졌다. 검토 측은 그 공극에 안정화 수지가 섞여 있다고 본다. Minnmann et al. 2024는 SE 입경을 줄여 공극을 줄이자 CAM 이용률이 62에서 77 %로 올랐다고 적었다. Froboese et al. 2019의 유리구 모델 전극에서는 작은 입경이 오히려 공정 기공을 늘렸고, 검토 측은 이 결과에서 입경 효과와 기공 효과를 가를 수 없다고 본다. [근거: Hlushkou et al. 2018 (`hlushkou2018_void_space_ion_transport_assb_cathode`); Minnmann et al. 2024 (`minnmann2024_microstructure_porosity_visualization`); Froboese et al. 2019 (`froboese2019_microstructure_ionic_conductivity_assb_electrode`)]

### 도전재의 득과 실

도전재는 전자 경로를 빠르게 잇는다. 그러나 SE가 적은 전극에서는 이온 경로를 끊고 SE 분해를 키운다. Reisacher et al. 2023은 활물질 없는 LPSCl과 C65 매트릭스의 전자 percolation 임계를 약 4 wt%로 정했다. 검토 측은 이 매트릭스가 2.07 MPa로만 눌렸으므로 절대값을 압밀 양극에 옮길 수 없다고 본다. Cho et al. 2024에서 VGCF는 88 wt% 전극의 이온·계면 저항과 굴곡도를 키우고 LPSCl 산화 분해를 가속했다. Kim et al. 2024는 carbon이 SE 도메인을 부피로 점유한다고 보았고, 섬유형 CF가 구형 SC보다 이온전도도와 수명을 지켰다고 보고했다. [근거: Reisacher et al. 2023 (`reisacher2023_percolation_sulfide_carbon_matrix`); Cho et al. 2024 (`cho2024_conflicting_roles_conductive_additive`); Kim et al. 2024 (`kim2024_carbon_volumetric_occupation_se_domain`)]

무탄소 전극에서는 활물질 자체가 전자 경로가 되며, 그 전도도는 리튬 함량에 따라 자릿수 단위로 변한다. Amin · Chiang 2016의 NMC 소결 펠릿에서 전자전도도는 탈리튬화와 함께 ∼10⁻⁷ S cm⁻¹에서 ∼10⁻² S cm⁻¹로 올랐다. Asano et al. 2017의 복합 양극에서도 충전하자 전자 전도도가 크게 올랐다. 도전재를 넣는 방식도 결과를 바꾼다. SE 코팅 중 도전재를 넣은 Kim et al. 2025에서 Super P는 코팅층 전자전도도를 3.3×10⁻²에서 1.0×10⁻⁵ S/cm로 떨어뜨렸고, VGCF는 전도도를 지켰다. [근거: Amin · Chiang 2016 (`aminchiang2016_nmc_electronic_ionic_transport_vs_li`); Asano et al. 2017 (`asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity`); Kim et al. 2025 (`kim2025_conductive_agent_se_coating_cathode`)]

### 탄소 접합의 저항

탄소 섬유와 튜브가 이룬 망의 전도도는 섬유 자체보다 섬유 사이 접합이 정한다. Endo et al. 2001은 흑연화 VGCF 단섬유의 저항률을 1×10⁻⁴ Ω cm로 적었다. 같은 섬유의 압분체 저항률은 충전밀도와 섬유 간 접촉에 크게 좌우된다고 원문은 적었다. Li et al. 2007의 계산에서 망 전도도는 접촉 저항에 반비례했고 CNT 고유 전도도와는 무관했다. Nirmalraj et al. 2009는 SWCNT 접합 평균을 단일 튜브끼리 98 kΩ, 큰 다발끼리 2,677 kΩ으로 쟀고, 검토 측은 필름 전도도와의 비례가 세 점으로 얻은 상관이라고 본다. [근거: Endo et al. 2001 (`endo2001_vgcf_basic_properties_battery_applications`); Li et al. 2007 (`li2007_tunneling_resistance_cnt_composites`); Nirmalraj et al. 2009 (`nirmalraj2009_swcnt_network_junction_resistance`)]

접합 하나의 저항은 접촉의 기하와 상태에 따라 크게 달라진다. Fuhrer et al. 2000은 교차한 금속 SWCNT 접합을 4 단자로 재어 200 kΩ을 얻었다. 이 논문의 계산은 기판 접촉력이 만든 변형이 있어야 실험 투과율에 맞는다고 보였다. Hamasaki et al. 2022는 나란한 MWCNT의 짧은 겹침에서 계면 저항이 겹침 길이에 반비례한다고 쟀고, 계면 전도도를 2 × 10² – 4 × 10³ S/m로 냈다. Banerjee et al. 2019의 실험 없는 전송선 계산은 겹침이 전달 길이를 넘으면 접촉 저항이 포화한다고 보였다. [근거: Fuhrer et al. 2000 (`fuhrer2000_crossed_nanotube_junctions`); Hamasaki et al. 2022 (`hamasaki2022_single_parallel_contact_mwcnt_conductivity`); Banerjee et al. 2019 (`banerjee2019_tunneling_tlm_parallel_nanoscale_contacts`)]

### 이 장의 값

| 값 | 표기 | 근거 |
|---|---|---|
| NCM-622 42 vol% 양극 이온 τ² | 4.3 | Minnmann et al. 2021 (`minnmann2021_jes_charge_transport_bottlenecks`) |
| LPSCl/NMC811 실측 σ_ion, f_CAM 70/75/80 | 0.137 / 0.101 / 0.065 mS/cm | Bazzoun et al. 2026 (`bazzoun2026_dem_fem_rnm_ionic`) |
| LPSI/LCO 재구성 확산 τ_diff | 1.74 | Hlushkou et al. 2018 (`hlushkou2018_void_space_ion_transport_assb_cathode`) |
| 1 mm 강구 충전 τ_EIS | 1.56 | Landesfeind et al. 2018 (`landesfeind2018_tortuosity_impedance_vs_tomography`) |
| 2층 구조 τ_e (조밀층 위치별) | 4.0 / 11.9 | Nguyen et al. 2020 (`nguyen2020_electrode_tortuosity_factor`) |
| LPSCl+C65 전자 percolation 임계 | 3 < p_c < 5 wt% | Reisacher et al. 2023 (`reisacher2023_percolation_sulfide_carbon_matrix`) |
| 복셀 RN 고-NCM σ_ion 과대 배수 | 10.7–58× | Ketter et al. 2025 (`ketter2025_resistor_network_models_predict_transport_properties`) |
| SWCNT 단일 튜브 접합 평균 저항 | 98 kΩ | Nirmalraj et al. 2009 (`nirmalraj2009_swcnt_network_junction_resistance`) |

### 아직 열린 문제

- 관통형 τ와 τ_e 가운데 어느 쪽이 실제 전극 성능을 더 잘 예측하는지는 입증되지 않았다. Nguyen et al. 2020의 τ_e 권고는 모델 정합성 논리와 수치 예시에 기댄 것이다. Morasch et al. 2018도 편향의 크기를 모의에서만 정했다. [근거: Nguyen et al. 2020 (`nguyen2020_electrode_tortuosity_factor`); Morasch et al. 2018 (`morasch2018_binder_gradient_impedance_tortuosity`)]
- 황화물 SE 입계의 몫을 두고 카드가 엇갈린다. Islam et al. 2026의 2D phase-field 계산은 입계 단독 효과가 거의 없다고 냈다. 반면 Kim et al. 2025의 임피던스 분리와 Choi et al. 2024는 입계 저항이 bulk와 맞먹거나 이온 저항의 대부분을 차지한다고 보고했다. 검토 측은 Islam et al. 2026의 결론을 끊긴 2D 입계 맵의 산물로 본다. [근거: Islam, Katsube, Ji 2026 (`islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell`); Kim et al. 2025 (`kim2025_impedance_decoupling_tlm_assb`); Choi et al. 2024 (`interfacial_impedance_formulation_assb_cathode`)]
- 압력과 하중 제거가 수송을 어떻게 바꾸는지는 아직 반쪽만 재어졌다. Miß et al. 2026의 첫 압밀 자료에서 전자 tortuosity는 한 자릿수 떨어졌고 이온 쪽은 거의 평평했다. 검토 측은 이온 쪽이 평평해 보이는 것이 정규화의 산물일 수 있다고 보며, 이 자료에는 하중 제거 구간이 없다. Bazzoun et al. 2025의 탄성 강체구 DEM은 고-CAM 구간에서 실험과 크게 어긋났다. [근거: Miß et al. 2026 (`miss2026_pressure_tortuosity_composite_cathode_coating`); Bazzoun et al. 2025 (`bazzoun2025_dem_parameter_sensitivity_assb_cathode`)]
- 후막 양극의 두께 방향 반응 분포를 정하는 기전은 정해지지 않았다. Stavola et al. 2023은 CAM 분율에 따라 먼저 반응하는 쪽이 뒤집힌다고 보고했다. Kim et al. 2026의 중성자 영상은 저전류에서 가운데 띠가 가장 크게 반응한다고 보였다. 검토 측은 앞 논문의 τ² 표 계산을 의심하고, 뒤 논문의 기전 근거가 논문 밖에 있다고 본다. [근거: Stavola et al. 2023 (`stavola2023_thick_nmc111_lpscl_lithiation_gradient_tortuosity`); Kim et al. 2026 (`kim2026_operando_neutron_thick_nmc811_interior_hotspot`)]

### 먼저 읽을 논문

1. Tjaden et al. 2018 (`tjaden2018_tortuosity_review_calculation_approaches`) — 굴곡도의 정의와 계산 계열을 정리한 리뷰라서, 뒤 논문들의 τ가 어느 양인지 가릴 기준을 준다.
2. Minnmann et al. 2021 (`minnmann2021_jes_charge_transport_bottlenecks`) — 전고체 복합양극에서 CAM 분율에 따른 전자와 이온 병목을 한 계에서 함께 잰 기준 실험이다.
3. Nguyen et al. 2020 (`nguyen2020_electrode_tortuosity_factor`) — 관통형 τ와 차단 임피던스 τ_e가 언제 갈리는지 보여 주어 EIS 값을 읽는 법을 정해 준다.
4. Bielefeld et al. 2019 (`bielefeld2020_effective_ionic_conductivity_binder`) — Bielefeld et al. 2019의 유효 이온전도도 편으로, 접촉 저항 없는 연속체 계산이 조성과 바인더에 어떻게 반응하는지 보여 준다.
5. Bazzoun et al. 2026 (`bazzoun2026_dem_fem_rnm_ionic`) — DEM 구조 위 RNM 계산을 같은 소재계의 EIS 실측과 맞대어 계산과 실측의 거리를 보여 준다.

## 이 장의 논문 (68편)

| digest | 저자 · 연도 | 제목 | 한 줄 결론 |
|---|---|---|---|
| `fuhrer2000_crossed_nanotube_junctions` | Fuhrer et al. 2000 | Crossed Nanotube Junctions | 교차 SWCNT의 금속–금속 접합은 약 200 kΩ이고 금속–반도체 접합은 Schottky 장벽 때문에 두 자릿수 덜 통한다. |
| `endo2001_vgcf_basic_properties_battery_applications` | Endo et al. 2001 | Vapor-grown carbon fibers (VGCFs) | 서브마이크론 VGCF는 흑연화하면 단섬유 저항률이 1×10⁻⁴ Ω cm로 낮아지지만, 압분체의 저항률은 충전밀도와 섬유 간 접촉에 크게 좌우된다. |
| `lindblad2005_surface_area_weighted_local_configurations` | Lindblad 2005 | Surface area estimation of digitized 3D objects using weighted local configurations | m-cube의 열세 가지 경우에 가중을 주는 국소 추정기는 평면에서 불편이고, 구 묶음으로 A₁ = 0.636을 정해 작은 물체 편향도 줄였다. |
| `li2007_tunneling_resistance_cnt_composites` | Li et al. 2007 | Dominant role of tunneling resistance in the electrical conductivity of carbon nanotube–based composites | 교차 CNT 사이 절연막의 터널 저항은 막 두께에 지수적으로 커지고, 이 접촉 저항이 복합체 망의 전도도를 정한다. |
| `nirmalraj2009_swcnt_network_junction_resistance` | Nirmalraj et al. 2009 | Electrical Connectivity in Single-Walled Carbon Nanotube Networks | 전도성 AFM으로 잰 SWCNT 접합 저항은 다발 크기와 화학 처리에 따라 크게 달랐고, 필름 전도도는 그 역수에 비례했다. |
| `thorat2009_quantifying_tortuosity_porous_liion` | Thorat et al. 2009 | Quantifying tortuosity in porous Li-ion battery materials | 액체 LIB 활물질 막의 τ는 τ = 1.8 ε^−0.53으로 맞고, 지수는 Bruggeman과 같지만 값은 거의 두 배다. |
| `ziegel2010_surface_area_measure_digitizations` | Ziegel · Kiderlen 2010 | Estimation of surface area and surface area measure of three-dimensional sets from digitizations | 2×2×2 배치 수에 가중을 주는 국소 넓이 추정기는 점근 최악 상대오차 3.98 %가 한계이고, 같은 배치 수로 법선 분포도 추정한다. |
| `chen2011_percolation_micromodel_composite_electrode` | Chen et al. 2011 | Percolation micro-model to predict the effective properties of the composite electrode with poly-dispersed particle sizes | 다분산 복합전극을 닫힌식 percolation 모델로 풀었다. PSD가 넓으면 TPB는 줄고, 임계는 낮아지며, 입자 간 이온전도는 오른다. |
| `ender2011_3d_reconstruction_composite_cathode` | Ender et al. 2011 | Three-dimensional reconstruction of a composite cathode for lithium-ion cells | FIB/SEM 재구성으로 카본블랙, LiFePO₄, 기공을 나눴고, 세 굴곡도 중 FEM 값이 가장 믿을 만하다고 원문은 판정했다. |
| `holzer2013_constrictivity_effective_transport_porous_layers` | Holzer et al. 2013 | The influence of constrictivity on the effective transport properties of porous layers in electrolysis and fuel cells | 격막의 τ_geo는 평평한데 EIS 굴곡도는 크게 올라, 그 격차를 협착 δ로 보고 기하 β와 사인식으로 이었다. |
| `wiedenmann2013_pore_structure_ion_conductivity_ceramic_diaphragms` | Wiedenmann et al. 2013 | Three‐dimensional pore structure and ion conductivity of porous ceramic diaphragms | 단층촬영으로 잰 기공률, 기하 굴곡도, 협착 인자만으로 KOH 함침 격막의 EIS 전도도를 맞춤 없이 예측했다. |
| `siroma2015_transmission_line_model_porous_electrode_impedance` | Siroma et al. 2015 | Mathematical solutions of comprehensive variations of a transmission-line model of the theoretical impedance of porous electrodes | 다공 전극 전송선 모델을 Z, T, E, 범용형으로 잇는 모든 경계조건의 임피던스 해를 모으고, 다층용 TML-Y 변환을 유도했다. |
| `aminchiang2016_nmc_electronic_ionic_transport_vs_li` | Amin · Chiang 2016 | Characterization of Electronic and Ionic Transport in Li₁₋xNi0.33Mn0.33Co0.33O₂(NMC₃₃₃) and Li₁₋xNi0.50Mn0.20Co0.30O₂(NMC₅₂₃) as a Function of Li Content | 첨가제 없는 NMC 소결 펠릿에서 전자전도도는 탈리튬화와 함께 크게 오르고, 화학확산은 언제나 Li 이온 수송이 제한한다. |
| `landesfeind2016_tortuosity_eis_electrodes_separators` | Landesfeind et al. 2016 | Tortuosity Determination of Battery Electrodes and Separators by Impedance Spectroscopy | 차단 조건 EIS로 잰 effective tortuosity τ=ε·N_M은 분리막과 전극 모두 구형 Bruggeman 값보다 크다. |
| `taufactor_tortuosity_factor_tomography_tool` | Cooper et al. 2016 | TauFactor: An open-source application for calculating tortuosity factors from tomographic data | TauFactor는 분할된 voxel 미세구조에서 ∇²C=0을 직접 풀어 τ = ε·D/D_eff를 빠르고 재현성 있게 계산하는 오픈소스 툴이다. |
| `asano2017_ncm111_li3ps4_composite_electronic_ionic_conductivity` | Asano et al. 2017 | Electronic and Ionic Conductivities of LiNi1/3Mn1/3Co1/3O₂-Li₃PS₄Positive Composite Electrodes for All-Solid-State Lithium Batteries | 충전 전 복합 양극은 이온 전도도가 전자 전도도보다 높고, 충전하면 전자 전도도가 크게 오르며, 원문은 율 특성을 이온 전도가 제한한다고 결론짓는다. |
| `cooper2017_simulated_impedance_diffusion_porous_media` | Cooper et al. 2017 | Simulated impedance of diffusion in porous media | 복셀 구조의 확산 임피던스를 주파수 영역에서 직접 풀면 개방계 저주파 절편은 τ/ε이고, 스펙트럼 모양은 구조에 따라 갈린다. |
| `malifarge2017_tortuosity_symmetric_cell_impedance_tlm` | Malifarge et al. 2017 | Determination of Tortuosity Using Impedance Spectra Analysis of Symmetric Cell | 전자 레일을 포함한 두 레일 TLM으로 차단 대칭셀 임피던스 전체를 맞추면 기공 tortuosity τ₂를 직접 얻는다. |
| `hlushkou2018_void_space_ion_transport_assb_cathode` | Hlushkou et al. 2018 | The influence of void space on ion transport in a composite cathode for all-solid-state batteries | void 13.2 vol%가 SE 상을 가늘고 굽은 통로로 나눠 τ_diff를 1.27에서 1.74로 올린다. |
| `kaiser2018_ion_transport_limitations_assb_sulfide_electrodes` | Kaiser et al. 2018 | Ion transport limitations in all-solid-state lithium battery electrodes containing a sulfide-based electrolyte | LTO와 LPSI 유리 복합 전극에서 두 임피던스법은 ε 0.4 이상에서 같은 τ_eff를 주고, SE가 적을수록 이온 수송이 가파르게 막힌다. |
| `kato2018_thick_electrode_assb_cycle_tortuosity` | Kato et al. 2018 | All-Solid-State Batteries with Thick Electrode Configurations | 농도 구배가 없는 옴 한계 식을 율속 자료에 맞춰 LiCoO₂ 양극 τ 2.47, 흑연 음극 τ 3.32를 임피던스 없이 얻었다. |
| `landesfeind2018_tortuosity_impedance_vs_tomography` | Landesfeind et al. 2018 | Tortuosity of Battery Electrodes: Validation of Impedance-Derived Values and Critical Comparison with 3D Tomography | EIS 굴곡도는 강구 충전에서 Bruggeman과 맞았고, 같은 코팅의 단층촬영값보다 ~2배 커 미해상 바인더와 탄소가 원인으로 지목됐다. |
| `morasch2018_binder_gradient_impedance_tortuosity` | Morasch et al. 2018 | Detection of Binder Gradients Using Impedance Spectroscopy and Their Influence on the Tortuosity of Li-Ion Battery Graphite Electrodes | 같은 총 이온 저항이라도 고저항층이 분리막 쪽이면 차단 EIS의 겉보기 τ가 커지고, 집전체 쪽이면 작아진다. |
| `pouraghajan2018_tortuosity_polarization_interrupt_vs_blocking_electrolyte` | Pouraghajan et al. 2018 | Quantifying Tortuosity of Porous Li-Ion Battery Electrodes: Comparing Polarization-Interrupt and Blocking-Electrolyte Methods | 상용 LIB 전극 넷에서 두 측정법의 τ는 불확도 안에서 맞았고, 큰 차이는 박리 팽창에서 왔다. |
| `tjaden2018_tortuosity_review_calculation_approaches` | Tjaden et al. 2018 | Tortuosity in electrochemical devices: a review of calculation approaches | 굴곡도는 τ와 τ²가 섞여 쓰이고 계산법마다 값이 체계적으로 달라, 거듭제곱과 계산 계열을 구분해야 한다. |
| `wang2018_lco_nmc_electronic_ionic_conductivity_vs_ni` | Wang et al. 2018 | Separating electronic and ionic conductivity in mix-conducting layered lithium transition-metal oxides | 치밀 펠릿의 σ_e는 Ni가 늘수록 커지지만, Ni-rich NMC의 큰 σ_i 주장은 검토 측 점검을 통과하지 못한다. |
| `banerjee2019_tunneling_tlm_parallel_nanoscale_contacts` | Banerjee et al. 2019 | A Two Dimensional Tunneling Resistance Transmission Line Model for Nanoscale Parallel Electrical Contacts | 나란한 겹침 접촉을 터널 전류와 결합한 전송선 모형으로 풀면 접촉 저항은 간극에 지수적으로 오르고 긴 겹침에서 포화한다. |
| `bielefeld2019_microstructural_modeling_composite_cathode` | Bielefeld et al. 2019 | Microstructural Modeling of Composite Cathodes for All-Solid-State Batteries | 작은 AM 입자와 낮은 공극률이 이온·전자 클러스터 연결을 돕고, 두께는 얇은 전극에서만 겉보기 차이를 낸다. |
| `bielefeld2020_effective_ionic_conductivity_binder` | Bielefeld et al. 2019 | Modeling Effective Ionic Conductivity and Binder Influence in Composite Cathodes for All-Solid-State Batteries | 연속체 전도 계산으로 AM 분율, 입경, 공극, 바인더가 유효 이온전도도와 τ²를 좌우함을 정량했다. |
| `froboese2019_microstructure_ionic_conductivity_assb_electrode` | Froboese et al. 2019 | Effect of Microstructure on the Ionic Conductivity of an All Solid-State Battery Electrode | 비활성 유리구 모델 전극에서 분율이 40 %를 넘으면 작은 입경일수록 기공이 늘고 이온전도도가 더 떨어진다. |
| `park2019_electrode_design_methodology_assb_3d` | Park et al. 2019 | Electrode design methodology for all-solid-state batteries: 3D structural analysis and performance prediction | 복셀 구조 해석에서 LSTP를 30에서 20 wt%로 줄이면 이온 MacMullin 수가 178에서 28,556으로 뛴다. |
| `nguyen2020_electrode_tortuosity_factor` | Nguyen et al. 2020 | The electrode tortuosity factor: why the conventional tortuosity factor is not well suited for quantifying transport in porous Li-ion battery electrodes and what to use instead | 이온은 고/액 계면까지만 가면 되므로 관통 flux로 정한 τ 대신 차단 대칭셀 임피던스로 정한 τ_e를 P2D에 쓰라고 원문은 권한다. |
| `sangros2020_dem_electrical_conductive_paths_assb` | Sangrós Giménez et al. 2020 | Modeling the Electrical Conductive Paths within All‐Solid‐State Battery Electrodes | DEM 구조에서 A* 경로탐색과 실린더 저항 회로로 구한 전자전도도는 percolation 이론보다 실측에 가깝고, CB가 늘면 이온 전도는 준다. |
| `minnmann2021_jes_charge_transport_bottlenecks` | Minnmann et al. 2021 | Editors’ Choice—Quantifying the Impact of Charge Transport Bottlenecks in Composite Cathodes of All-Solid-State Batteries | EIS-TLM으로 NCM-622/Li₆PS₅Cl 양극의 부분 전도도와 τ²를 재어, 비용량 최적이 두 병목 사이인 42 vol% CAM 근처임을 보였다 |
| `neumann2021_garnet_3d_structure_grain_boundaries_li_transport` | Neumann et al. 2021 | Effect of the 3D Structure and Grain Boundaries on Lithium Transport in Garnet Solid Electrolytes | 입계를 입자 사이 복셀 면의 계면 조건으로 넣어야 다공 garnet의 유효 이온전도도 감소가 실험 자릿수에 다가간다. |
| `deysher2022_transport_mechanical_aspects_assb_review` | Deysher et al. 2022 | Transport and mechanical aspects of all-solid-state lithium batteries | SE 벌크 전도도는 충분해졌으므로 이제 복합 양극 내부의 전달과 부피변화 역학이 전고체전지의 율속 병목이라고 정리한 리뷰다. |
| `hamasaki2022_single_parallel_contact_mwcnt_conductivity` | Hamasaki et al. 2022 | Electrical conductivity of a single parallel contact between carbon nanotubes | 두 MWCNT의 나란한 접촉 저항은 짧은 겹침에서 길이에 반비례하고, 수백 nm를 넘으면 튜브 본체 저항이 지배한다. |
| `minnmann2022_designing_cathodes_solidstate` | Minnmann et al. 2022 | Designing Cathodes and Cathode Active Materials for Solid‐State Batteries | 고체전지 복합양극은 CAM과 SE의 함량, 입자 크기, 분포, 계면을 함께 맞춰야 한다는 정성 설계 지침을 제시한다. |
| `so2022_dem_compaction_coated_particles_assb` | So et al. 2022 | Simulation of the compaction of an all-solid-state battery cathode with coated particles using the discrete element method | core-shell SE 코팅은 25 MPa에서도 SE percolation이 90 %를 넘지만, 저압에서는 AM-AM 전자 접촉을 차폐한다. |
| `lee2023_sicspe_digitaltwin_assb` | Lee et al. 2023 | Digital‐twin‐driven structural and electrochemical analysis of Li⁺ single‐ion conducting polymer electrolyte for all‐solid‐state batteries | SIC-SPE 전극은 SE 부피분율, 굴곡도, 활물질 접촉에서 LPSCl 전극보다 유리해 10배 낮은 고유 전도도에도 대등한 용량을 낸다. |
| `otani2023_ionic_conductivity_path_resistance_separation_model` | Otani et al. 2023 | Ionic conductivity prediction model for composite electrodes and quantification of ionic conductivity reduction factors in sulfide-based all-solid-state batteries | LPSCl 층의 전도 저하는 주로 입자 접촉 면적에서 오고, 복합양극은 β 1.5와 β 4 두 Bruggeman 계수의 곱으로 예측된다. |
| `reisacher2023_percolation_sulfide_carbon_matrix` | Reisacher et al. 2023 | Percolation Behavior of a Sulfide Electrolyte–Carbon Additive Matrix for Composite Cathodes in All-Solid-State Batteries | LPSCl과 C65 도전 매트릭스의 전자 percolation 임계는 약 4 wt%이고, 그 위에서 전도는 전자 ohmic으로 바뀐다. |
| `stavola2023_thick_nmc111_lpscl_lithiation_gradient_tortuosity` | Stavola et al. 2023 | Lithiation Gradients and Tortuosity Factors in Thick NMC111-Argyrodite Solid-State Cathodes | 후막 무탄소 NMC111–LPSC 양극은 C/10에서도 두께 방향 반응 분포가 크고, CAM 70과 80 wt% 사이에서 먼저 반응하는 쪽이 뒤집힌다. |
| `cho2024_conflicting_roles_conductive_additive` | Cho et al. 2024 | Conflicting roles of conductive additives in controlling cathode performance in all-solid-state batteries | VGCF는 전자저항을 늘 낮추지만, SE가 적은 전극에서는 이온망을 끊고 LPSCl 분해를 가속해 성능을 떨어뜨린다. |
| `interfacial_impedance_formulation_assb_cathode` | Choi et al. 2024 | Formulating Interfacial Impedances for Designing High-Energy and High-Power All-Solid-State Battery Cathodes | 복합 양극의 낮은 이온전도는 SE 입계 저항 때문이고, 입경에 따른 입계 저항과 전하전달 저항의 trade-off는 bimodal CAM으로 풀린다. |
| `kim2024_carbon_volumetric_occupation_se_domain` | Kim et al. 2024 | Accelerated Degradation of All‐Solid‐State Batteries Induced through Volumetric Occupation of the Carbon Additive in the Solid Electrolyte Domain | 도전 carbon은 SE 도메인을 부피로 점유해 Li⁺ 경로를 막고 SE 산화분해를 촉매하며, 섬유형 carbon이 이를 줄인다. |
| `minnmann2024_microstructure_porosity_visualization` | Minnmann et al. 2024 | Editors’ Choice—Visualizing the Impact of the Composite Cathode Microstructure and Porosity on Solid-State Battery Performance | SE 입경을 줄이면 복합 양극이 균질해져 공극과 이온 굴곡도가 줄고, CAM-ISE 계면과 CAM 이용률이 늘어난다. |
| `nisar2024_dem_effective_electrical_conductivity_sps` | Nisar et al. 2024 | Discrete element model for effective electrical conductivity of spark plasma sintered porous materials | 부피보존 neck 반경과 neck 내부 입계 저항을 넣은 DEM 저항망이 SPS 소결 NiAl의 실측 전기전도도와 근사 일치했다. |
| `bazzoun2025_dem_parameter_sensitivity_assb_cathode` | Bazzoun et al. 2025 | Parameter sensitivity analysis and calibration of a discrete element model for optimizing all-solid-state-battery cathode microstructures | 강체구 DEM에서 μ_CAM-SE가 percolation과 공극률에 가장 민감했고, 모델은 고-CAM 로딩에서 실험과 어긋났다. |
| `huang2025_dem_lbm_heat_conduction_composite_cathode` | Huang et al. 2025 | Modelling heat conduction in 3D composite cathode microstructures of all-solid-state batteries | DEM으로 만든 LCO/LLZO 복합 양극에서 LBM으로 구한 유효 열전도도는 공극률, 체적비, 입자크기에 좌우되고 굴곡도도 무시할 수 없다. |
| `ketter2025_resistor_network_models_predict_transport_properties` | Ketter et al. 2025 | Using resistor network models to predict the transport properties of solid-state battery composites | voxel 저항망은 NCM83–LPSCl 복합양극의 σ와 κ 조성 의존을 따라가지만 이온 문턱 근처에서는 σ_ion을 크게 과대 예측한다. |
| `kim2025_conductive_agent_se_coating_cathode` | Kim et al. 2025 | Impact of Conductive Agents in Sulfide Electrolyte Coating on Cathode Active Materials for Composite Electrodes in All‐Solid‐State Batteries | SE 코팅 중 넣은 0D Super P는 코팅층에 응집해 전자전도를 떨어뜨리고, 1D VGCF는 전자경로를 만들어 성능을 지킨다. |
| `kim2025_impedance_decoupling_tlm_assb` | Kim et al. 2025 | Multiple-reaction kinetics of composite electrodes for sulfide-based all-solid-state batteries: Impedance decoupling | 두 경계조건을 둔 modified TLM과 대칭셀, 3-전극 풀셀 EIS로 NCM811/LPSCl 복합 양극의 여러 반응 저항을 분리했다. |
| `luan2025_graded_cathode_400whkg_pouch` | Luan et al. 2025 | Electrode Engineering Strategy for 400 Wh kg −1 All‐Solid‐State Pouch Cells: Spatial Optimization of Charge Carriers Based on Electron and Ion Transport Flux | 조성 총량을 고정한 채 SE를 분리막쪽에 몰면 두꺼운 황화물 양극의 용량과 율특성이 오르고, 이를 건식 파우치로 옮겼다. |
| `song2025_electrochemo_mechanical_microelectrode_ees` | Song et al. 2025 | A microstructural electrochemo-mechanical model of high-nickel composite electrodes towards digital twins to bridge the particle and electrode-level characterizations | FIB-SEM으로 재구성한 NMC711 복합양극에 성분별 고유물성을 넣으면 셀 전압이 재현되고, 셀의 과전압은 세 가지 메커니즘으로 설명된다. |
| `bazzoun2026_dem_fem_rnm_ionic` | Bazzoun et al. 2026 | Integration of DEM-based microstructure generation with FEM and RNM simulations for evaluating ionic conductivity in composite cathodes of all-solid-state batteries | DEM으로 만든 Li₆PS₅Cl/NMC811 양극 구조에서 FEM과 RNM이 이온전도도의 조성, 압력 추세를 내고 EIS로 검증된다. |
| `cronk2026_lis_positive_electrode_geometry_fem` | Cronk et al. 2026 | A highly utilized and practical lithium-sulfur positive electrode enabled in all-solid-state batteries | S 입경을 마이크론으로 맞추고 1-step 밀링으로 계면상을 만들면 LPSCl 기반 Li–S 전고체 양극의 이용률과 수명이 함께 오른다. |
| `islam2026_microstructure_resolved_impedance_lpscl_symmetric_cell` | Islam, Katsube, Ji 2026 | Microstructure-Resolved Impedance Modeling SSB MAIN | Li/Li₆PS₅Cl/Li 대칭셀 계산에서 기공과 SEI는 임피던스를 키웠고 입계 단독 효과는 거의 없었으나, 실험 검증은 없다. |
| `kim2026_a3d_air_electrode_microstructure_transport` | Kim et al. 2026 | Microstructure-guided reactant transport engineering in architected three-dimensional air electrodes for high-performance Li–O2 batteries | A3D 공기극은 SSA와 산소수송 경로를 함께 지켜야 하며, diamond 단위셀과 전해연마가 그 균형을 가장 잘 맞췄다. |
| `kim2026_operando_neutron_thick_nmc811_interior_hotspot` | Kim et al. 2026 | Interior transport–degradation hotspots in high-loading NMC811 sulfide all-solid-state batteries revealed by operando neutron imaging | 후막 NMC811–LPSCl 양극에서 저전류 반응은 가운데 띠에 몰리고, 전류를 두 배로 올리면 SE 계면 쪽에 Li 결핍 띠가 생긴다. |
| `lee2026_unveiling_ptfe_dry_electrode_digital_twin` | Lee et al. 2026 | Unveiling the Structural Advantages in PTFE‐Based Dry‐Processed Electrodes for Sulfide‐Based All‐Solid‐State Batteries via 3D Microstructure‐Resolved Analysis | 같은 LPSCl 부피에서 PTFE 0.2 wt%가 NCM 위 in situ 코팅과 고른 분산을 만들어 이온과 전자 전도도를 함께 높였다. |
| `miss2026_insitu_conductivity_porosity_pressure_compaction` | Miß et al. 2026 | Experimental Setup for In Situ Determination of Conductivity–Porosity–Pressure Relationships during Compression of Solid Electrolytes and of Cathode Active Materials | 하중 아래 두께로 공극을 내면 ε 0.17–0.2보다 큰 쪽은 계면 접촉이, 작은 쪽은 공극이 전도도를 정한다. |
| `miss2026_pressure_tortuosity_composite_cathode_coating` | Miß et al. 2026 | Pressure‐Dependent Electronic and Ionic Tortuosities During Fabrication of Composite Cathodes for All‐Solid‐State Batteries: Influence of Active Material Particle Morphology, Volume Fraction, and Coating | 첫 압밀 동안 복합 양극의 τ_eon은 압력으로 한 자릿수 떨어지고 τ_ion은 약하게 변하며, 형상 차이는 혼합이 만든 미세구조가 정한다. |
| `oh2026_bimodal_composite_cathode` | Oh et al. 2026 | Bimodal Composite Cathodes Advancing the Chemo-Mechanical Integrity and Kinetics for All-Solid-State Batteries | 작은 단결정 NCM이 큰 다결정 NCWA 사이 틈을 채우면 공극률과 이온 굴곡도가 낮아지고, 7:3 조성에서 속도 특성과 수명이 함께 가장 좋다. |
| `oh2026_carbon_coating_siox_ion_electron_balance` | Oh et al. 2026 | Optimized carbon coating on SiOx enables balanced ion/electron transport and uniform dispersion in SiOx/Graphite composite electrodes | CVD 탄소코팅이 두꺼울수록 전자전도는 좋아지지만 Li⁺ 수송이 막혀, 중간 두께가 저항, rate, 수명에서 가장 낫다. |
| `pan2026_thesis_rate_capable_energy_dense_cathode_composites` | Bonian Pan 2026 | Engineering Rate Capable, Energy-Dense Lithium-Ion Battery Cathode Composites | 액체 LIB 양극에서 2층 기공 구배와 SWCNT·그래핀 혼성 도전재는 고율 용량을 올렸고, LMO에 입힌 LFP 셸은 직렬 수송 장벽이 됐다. |
| `zhang2026_polymer_electrolyte_modeling_perspective` | Zhang et al. 2026 | Modeling Approaches for Polymer-Based Electrolytes in Advanced Batteries: Bridging Processing, Structure, and Performance | 고분자계 전해질 모델을 네 축으로 분류하면 이온겔 연구는 분자, 기전, 비결합에 몰리고 메조 축척과 완전결합은 비어 있다. |
| `zhou2026_gyroid_structural_electrolyte_stiffness_ionic_tradeoff` | Zhou et al. 2026 | Microstructure-resolved modeling of gyroid structural electrolytes: Mechanical and transport behavior | 공극률은 강성과 이온전도를 서로 반대로 바꾸고, 셀의 축 늘림은 한 방향의 둘을 함께 올리고 가로 방향에서는 함께 내린다. |

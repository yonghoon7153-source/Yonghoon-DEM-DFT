# 접촉역학과 소성

전극 미세구조 · 공정 · 장 `dem-contact` · 논문 48편 · 읽기 카드 48편

> 탄소성 접촉 모형, 점착, 분말 치밀화 이론.

## 장 서문 — 고밀도 압밀은 항복 캡과 다체 보정을 함께 요구한다

*읽기 카드 48편을 엮어 쓴 글 · 항목 30개 중 28개 검증 통과 · 2026-11-10*

탄소성 입자 접촉의 평균압과 접촉면적이 고밀도 압밀까지 어떻게 변하는지, 그리고 이를 DEM 접촉 법칙에 어떻게 담을지가 질문이다. [근거: Mesarovic · Fleck 2000 (`mesarovicfleck2000_dissimilar_elastoplastic_indentation`); Kogut · Etsion 2002 (`kogutetsion2002_ep_sphere_rigid_flat`); Jackson · Green 2005 (`jacksongreen2005_fem_elastoplastic_hemispherical_contact`); Luding 2008 (`luding2008_cohesive_frictional_contact_models`); Zunker · Kamrin 2024 (`zunker2024_mdr_contact_model_partI`)]

단일 접촉의 경도 천장과 독립 접촉 한계는 FEM으로 정리되었다. 그러나 널리 쓰는 DEM 법칙에는 항복압 캡이 없고, 다체 보정은 β나 ψ_b 같은 맞춤 값에 기댄다. [근거: Mesarovic · Fleck 2000 (`mesarovicfleck2000_dissimilar_elastoplastic_indentation`); Kogut · Etsion 2002 (`kogutetsion2002_ep_sphere_rigid_flat`); Luding 2008 (`luding2008_cohesive_frictional_contact_models`); Thakur et al. 2014 (`thakur2014_eepa_adhesive_elastoplastic_dem`); Giannis et al. 2021 (`giannis2021_stress_based_multicontact_dem`); Zunker · Kamrin 2024 (`zunker2024_bulk_elastic_partII`)]

이 법칙들을 황화물 고체전해질에 쓰려면 탄성률, 경도, 이론밀도를 넣어야 하는데, 이 입력값이 논문마다 엇갈린다. [근거: Sakuda et al. 2013 (`sakuda2013_sulfide_mechanical_property`); So et al. 2021 (`so2021_dem_mold_pressure_assb_coldpress`); Lee et al. 2025 (`lee2025_heckel_argyrodite_powder_densification_nanoindentation`); Var et al. 2026 (`var2026_sulfide_se_mechanical_properties_local_indentation_pellet`)]

### 접촉 평균압의 천장

단일 탄소성 접촉의 평균압은 항복 뒤 곧바로 상수가 되지 않고 경도 근처까지 오른다. Mesarovic·Fleck 2000은 평균압이 1.1 σ_y에서 항복을 시작하고, aE*/R₀σ₀가 50 이상이면 plateau에 머문다고 보였다. Kogut·Etsion 2002는 구와 강체평판의 접촉에서 ω/ω_c=110에 이르러야 평균압이 H = 2.8·Y가 된다고 적었다. 두 계산은 모두 무마찰 단일 접촉이다. [근거: Mesarovic · Fleck 2000 (`mesarovicfleck2000_dissimilar_elastoplastic_indentation`); Kogut · Etsion 2002 (`kogutetsion2002_ep_sphere_rigid_flat`)]

큰 접촉에서도 경도가 상수로 남는지를 두고 논문들이 갈린다. Jackson·Green 2005는 경도가 a/R에 따라 줄어 작은 접촉 극한에서만 H_G/σ_y = 2.84라고 적었고, 이 식은 a/R≤0.412 자료로 맞춘 것이다. Mesarovic·Fleck 2000도 유한변형 영역에서 평균압이 다시 떨어진다고 보았다. Zunker·Kamrin 2024 Part I의 경화곡선은 작은 변위 극한 2.75에서 시작해 원기둥 단축압축 값까지 내려간다. 반면 Kogut·Etsion 2002는 완전소성에 든 뒤 평균압을 상수로 둔다. [근거: Jackson · Green 2005 (`jacksongreen2005_fem_elastoplastic_hemispherical_contact`); Mesarovic · Fleck 2000 (`mesarovicfleck2000_dissimilar_elastoplastic_indentation`); Zunker · Kamrin 2024 (`zunker2024_mdr_contact_model_partI`); Kogut · Etsion 2002 (`kogutetsion2002_ep_sphere_rigid_flat`)]

### 캡 없는 법칙과 연화

DEM에서 널리 쓰는 이력 선형 법칙들은 소성 분기를 두지만 접촉압을 경도로 묶지 않는다. Luding 2008은 제하 뒤 영구 겹침 δ₀ = (1−k₁/k₂)·δ_max를 남기는 법칙을 주었다. Pasha et al. 2014와 Thakur et al. 2014는 그 위에 소성과 함께 커지는 점착을 얹었고, 검토 측은 세 법칙 모두에 항복압 캡이 없다고 본다. Thornton·Ning 1998은 접촉압이 p_y에 닿으면 더 오르지 않는 캡을 두어 소성 분기를 직선으로 만든다. 우리 hooke/hysteresis 법칙은 이 캡이 없어 E_SE를 24에서 1.35 GPa로 18× 낮춰 보상하고 있다. [근거: Luding 2008 (`luding2008_cohesive_frictional_contact_models`); Pasha et al. 2014 (`pasha2014_linear_elastoplastic_adhesive_contact`); Thakur et al. 2014 (`thakur2014_eepa_adhesive_elastoplastic_dem`); Thornton · Ning 1998 (`thorntonning1998_adhesive_elastoplastic_contact`)]

항복 캡을 넣는 접근과 강성을 낮추는 접근은 근거로 삼는 결과가 서로 다르다. So et al. 2021과 So et al. 2022는 두 입자 중 낮은 경도와 접촉면적으로 임계력 F_th를 정했다. 그 덕분에 LPS의 E_SE 24 GPa를 그대로 쓰고도 Sakuda 실험의 상대밀도를 맞췄다. Paulick et al. 2015는 오버랩이 입자 지름의 1 %보다 작으면 강성을 낮춰도 결과가 크게 바뀌지 않는다고 정리했지만, 검토 측은 리뷰의 최대 응력이 96 kPa라 고압 압밀에 옮길 수 없다고 본다. Van Lew et al. 2015가 실측한 입자별 E 연화는 우리 18× 연화의 방향만 지지하고 크기는 지지하지 않는다. [근거: So et al. 2021 (`so2021_dem_mold_pressure_assb_coldpress`); So et al. 2022 (`so2022_dem_contact_model_assb_compaction_sintering`); Sakuda et al. 2013 (`sakuda2013_sulfide_mechanical_property`); Paulick et al. 2015 (`paulick2015_elastic_particle_properties_dem_review`); Van Lew et al. 2015 (`vanlew2015_modifying_youngs_modulus_distribution`)]

### 독립 접촉이 깨지는 곳

접촉을 서로 독립으로 보는 가정이 깨지는 밀도는 논문마다 조금씩 다르게 제시된다. Mesarovic·Fleck 2000의 B2 단위셀 계산에서는 상대밀도 0.82 아래에서만 이 가정이 유효했다. Arzt 1982는 D ≈ 0.9 뒤 이웃 접촉면이 부딪쳐 배위수가 급증하며, 그 구간에서는 모델이 엄밀히 무효라고 적었다. Martin·Bouvard 2003은 엄밀히 0.85–0.90 이전까지만 유효하다고 보았다. 검토 측은 같은 근거로 Storåkers et al. 1997의 면적 인자 c²도 고밀도에서는 무효라고 본다. [근거: Mesarovic · Fleck 2000 (`mesarovicfleck2000_dissimilar_elastoplastic_indentation`); Arzt 1982 (`arzt1982_particle_coordination_densification_spheres`); Martin · Bouvard 2003 (`martinbouvard2003_dem_composite_cold_compaction`); Storåkers et al. 1997 (`storakers1997_similarity_inelastic_contact`)]

다체 효과를 넣는 처방들은 모두 고밀도 접촉을 더 뻣뻣하게 만들지만, 맞춤 값이 남는다. Gonzalez·Cuitiño 2012는 다른 접촉력이 만든 원거리 변형을 접근량에 더했다. 그 결과 정수압 BCC에서 2차 접촉이 Hertz의 ρ_R = 1.04보다 이른 ρ_R = 0.95에서 생긴다고 예측했다. Giannis et al. 2021의 응력 trace 보정항은 β를 재료마다 맞췄고, Varkey et al. 2026은 같은 꼴의 구속항을 β=0.5로 써서 halide 분리막 두께를 실험과 <1 % 안에서 맞췄다. Zunker·Kamrin 2024 Part II는 남은 자유표면 비율이 문턱 ψ_b 아래로 내려가면 벌크탄성 힘을 켜며, 이 처방들은 접촉을 무르게 하는 우리 DEM의 E 연화와 방향이 반대다. [근거: Gonzalez · Cuitiño 2012 (`gonzalez2012_nonlocal_contact_confined_granular`); Giannis et al. 2021 (`giannis2021_stress_based_multicontact_dem`); Varkey et al. 2026 (`varkey2026_multicontact_elastoplastic_dem`); Zunker · Kamrin 2024 (`zunker2024_bulk_elastic_partII`)]

### 무른 입자 압밀식

입자 형상 변화를 직접 푼 계산과 실험은 압밀을 배위수 증가 법칙과 단일 입자 압축 법칙의 곱으로 기술한다. Cantor et al. 2020과 Cárdenas-Barrantes et al. 2020은 2D 원판에서 Z − Z0가 (φ − φ0)^0.5에 비례하며, 그 계수가 약 5.1이고 마찰과 무른 비율에 무관하다고 적었다. Cárdenas-Barrantes et al. 2022의 실리콘과 PVC 원기둥 실험에서는 이 계수가 4.9로 나왔다. 같은 해 3D 탄성 구 계산에서는 계수 ψ가 약 8.5였고 압밀 식의 꼴도 2D와 달랐다. 이 3D 계산에서 Hertz 점접촉 DEM은 jammed 근처에서만 맞았다. [근거: Cantor et al. 2020 (`cantor2020_compaction_model_highly_deformable_particles`); Cárdenas-Barrantes et al. 2020 (`cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd`); Cárdenas-Barrantes et al. 2022 (`cardenasbarrantes2022_soft_hard_grains_compaction_experiment_dic`); Cárdenas-Barrantes et al. 2022 (`cardenasbarrantes2022_soft_spheres_3d_compaction_nscd`)]

이 식들은 매개변수 없이 예측한다고 원문이 주장하지만, 검토 측은 이 주장에 일관되게 이견을 단다. 검토 측은 φmax가 곡선마다 맞춘 값이라고 보며, Cantor et al. 2020에서는 같은 계산에 맞춘 값을 셋으로 센다. 단단한 입자가 많을수록 도달 밀도가 낮아진다는 점은 여러 논문이 같은 방향으로 보인다. Bouvard 2000의 HIP 실험에서는 Astroloy에 alumina를 35 vol% 넣자 상대밀도가 0.995에서 0.86으로 떨어졌다. Martin·Bouvard 2003의 DEM과 So et al. 2021의 AM-AM 응력 집중도 경질 입자가 압밀을 막는다는 쪽을 가리킨다. [근거: Cantor et al. 2020 (`cantor2020_compaction_model_highly_deformable_particles`); Cárdenas-Barrantes et al. 2020 (`cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd`); Bouvard 2000 (`bouvard2000_hard_soft_powder_densification`); Martin · Bouvard 2003 (`martinbouvard2003_dem_composite_cold_compaction`); So et al. 2021 (`so2021_dem_mold_pressure_assb_coldpress`)]

### 점착은 무엇으로 재나

점착 접촉의 떼는 힘은 이론마다 계수가 다르고, 소성이 끼면 압밀 이력에 따라 커진다. Johnson et al. 1971은 P = −(3/2)γπR를, Derjaguin et al. 1975는 2πRγ를 준다. 검토 측은 두 값의 차이가 점착이 작용하는 위치를 다르게 가정한 데서 나온다고 본다. JKR의 γ는 두 표면을 합친 접착일이라, 한 표면의 에너지와 섞어 쓰면 떼는 힘이 2배 어긋난다. Molerus 1975는 소성 평탄화가 응집력을 얼려 H = κN이 된다고 보았고, Pasha et al. 2014와 Thakur et al. 2014는 이 결합을 DEM 법칙에 담았다. [근거: Johnson · Kendall · Roberts 1971 (`johnson1971_jkr_surface_energy_contact_elastic_solids`); Derjaguin et al. 1975 (`dmt1975_adhesion_contact_deformation`); Molerus 1975 (`molerus1975_theory_of_yield_cohesive_powders`); Pasha et al. 2014 (`pasha2014_linear_elastoplastic_adhesive_contact`); Thakur et al. 2014 (`thakur2014_eepa_adhesive_elastoplastic_dem`)]

분말의 점착 수준을 하나의 벌크 지표로 정하기는 어렵다. Grey·Beddow 1968에서는 분무 구리에 기름을 섞는 동안 Hausner 비가 거의 변하지 않았지만, 회전 원통 최대각은 크게 올랐다. Nase et al. 2001은 정지 더미가 Bo_g ≈ 1에서 갈리지만, 회전 드럼은 충돌 수 Co로 보아야 전이가 드러난다고 적었다. Roessler·Katterfeld 2019는 안식각 대신 원통을 들어 올릴 때 기둥이 거치는 상 전이를 기준으로 SJKR의 CED를 보정했다. Begat et al. 2004는 같은 AFM 탐침으로 잰 떼는 힘의 비를 써서 접촉 기하를 지우고, 응집과 접착의 균형을 직접 쟀다. [근거: R. O. Grey · J. K. Beddow 1968 (`grey1969_hausner_ratio_metal_powders`); Nase · Vargas · Abatan · McCarthy 2001 (`nase2001_granular_bond_collision_number_wet_cohesion`); Roessler · Katterfeld 2019 (`roessler2019_dem_cohesive_aor_cylinder_lift_calibration`); Begat · Morton · Staniforth · Price 2004 (`begat2004_cohesive_adhesive_balance_afm_colloid_probe`)]

### 이 장의 값

| 값 | 표기 | 근거 |
|---|---|---|
| 구와 강체평판 완전소성 경도 | H = 2.8·Y | Kogut · Etsion 2002 (`kogutetsion2002_ep_sphere_rigid_flat`) |
| 독립접촉 유효 한계 상대밀도(3D B2) | 0.82 | Mesarovic · Fleck 2000 (`mesarovicfleck2000_dissimilar_elastoplastic_indentation`) |
| 압밀 한계 최종 배위수 Z(D=1) | 13.69 | Arzt 1982 (`arzt1982_particle_coordination_densification_spheres`) |
| 75Li₂S·25P₂S₅ 유리 영률 | 24 GPa | Sakuda et al. 2013 (`sakuda2013_sulfide_mechanical_property`) |
| LPS 응집체 SE percolation 임계 | φ_SE^crit = 0.13 | So et al. 2021 (`so2021_dem_mold_pressure_assb_coldpress`) |
| LPSCl 최대 이온전도도(135 MPa) | 3.3 mS/cm | Thompson et al. 2026 (`thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography`) |
| 벌크탄성 발동 문턱 ψ_b 권장값 | 0.08 | Zunker · Kamrin 2024 (`zunker2024_bulk_elastic_partII`) |

### 아직 열린 문제

- SE 입자의 경도 입력값이 정해지지 않았다. So et al. 2021과 So et al. 2022는 LPS 경도를 1.9 GPa로 두었고, Var et al. 2026은 400 MPa 펠릿의 Li₆PS₅Cl 입자에서 H = 665 MPa를 쟀다. 두 값은 서로 다른 물질에서 나온 것이다. Var et al. 2026은 완전 소성 압밀식이 필요한 압력을 낮게 준다고 보고 배수 3 보정을 썼지만, 검토 측은 이 보정을 자료 세 점에 맞춘 값으로 본다. Jackson·Green 2005처럼 큰 접촉에서 경도가 줄어든다면, 상수 H 가정이 어느 밀도까지 통하는지 답이 없다. [근거: So et al. 2021 (`so2021_dem_mold_pressure_assb_coldpress`); So et al. 2022 (`so2022_dem_contact_model_assb_compaction_sintering`); Var et al. 2026 (`var2026_sulfide_se_mechanical_properties_local_indentation_pellet`); Jackson · Green 2005 (`jacksongreen2005_fem_elastoplastic_hemispherical_contact`)]
- 다체 보정의 맞춤 값을 다른 재료로 옮길 수 있는지 모른다. Zunker·Kamrin 2024 Part II는 ψ_b = 0.08을 권했지만, Zunker et al. 2025는 실험에 맞춰 0.5로 튜닝했다. Giannis et al. 2021의 β는 재료마다 1.65에서 5.17까지 달랐다. 검토 측은 P_ij 정규화 규약의 차이 때문에 β를 옮길 때 최대 6× 오차가 생긴다고 본다. [근거: Zunker · Kamrin 2024 (`zunker2024_bulk_elastic_partII`); Zunker, Dunatunga, Thakur, Tang, Kamrin 2025 (`zunker2025_dem_large_deformation_compaction`); Giannis et al. 2021 (`giannis2021_stress_based_multicontact_dem`)]
- Li₆PS₅Cl의 공극 절대값은 분모부터 엇갈린다. Lee et al. 2025는 이론밀도를 1.64 g/cm³로 썼고, Var et al. 2026은 진밀도를 1.87 g/cm³로 썼다. 검토 측은 두 값 모두 근거가 불분명하다고 본다. Thompson et al. 2026의 흡수 밀도는 ≥800 MPa에서 결정밀도보다 커지므로, 검토 측은 경향으로만 읽으라고 본다. [근거: Lee et al. 2025 (`lee2025_heckel_argyrodite_powder_densification_nanoindentation`); Var et al. 2026 (`var2026_sulfide_se_mechanical_properties_local_indentation_pellet`); Thompson et al. 2026 (`thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography`)]
- SE 분말의 점착 수준을 정박할 측정이 아직 없다. Begat et al. 2004의 CAB는 힘의 비만 주며, 35 % RH에서 잰 값이라 모세관 항이 섞여 있다. Deng et al. 2021의 장치는 기판을 바꿔도 값이 거의 같아 이종 쌍을 가르지 못하고, 검토 측은 그 Bond 수가 탈착 감속도의 g 배수라고 본다. Matsusaka et al. 2010은 이종 재료의 마찰 대전을 정리했지만 배터리 소재 자료는 다루지 않는다. [근거: Begat · Morton · Staniforth · Price 2004 (`begat2004_cohesive_adhesive_balance_afm_colloid_probe`); Deng et al. 2021 (`deng2021_mechanical_surface_energy_tester_bond_number`); Matsusaka et al. 2010 (`matsusaka2010_triboelectric_charging_powders_review`)]

### 먼저 읽을 논문

1. Mesarovic · Fleck 2000 (`mesarovicfleck2000_dissimilar_elastoplastic_indentation`) — 단일 접촉의 평균압 영역과 독립접촉 한계를 한 지도로 정리해, 다른 논문의 결과를 놓을 기준이 된다.
2. Luding 2008 (`luding2008_cohesive_frictional_contact_models`) — 우리 DEM이 쓰는 hooke/hysteresis 법칙의 원식이라 캡 없는 법칙 논의의 출발점이다.
3. Cárdenas-Barrantes et al. 2020 (`cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd`) — 강체와 무른 입자 혼합의 압밀을 배위수와 단일 입자 응답으로 풀어 무른 입자 갈래의 중심에 있다.
4. So et al. 2022 (`so2022_dem_contact_model_assb_compaction_sintering`) — 경도 기반 항복과 평형 overlap으로 실제 E_SE를 쓴 채 LPS 압밀을 실험에 맞춘 배터리 DEM이다.

## 이 장의 논문 (48편)

| digest | 저자 · 연도 | 제목 | 한 줄 결론 |
|---|---|---|---|
| `kakar1967_deformation_theory_hot_pressing` | Kakar · Chaklader 1967 | Deformation Theory of Hot-Pressing | 부피 보존 잘린 구 모델은 D − D₀ = (3/2)D₀(a/R)²를 주지만, 납과 사파이어 실측은 미끄러짐과 재적층 때문에 모델보다 더 치밀하다. |
| `grey1969_hausner_ratio_metal_powders` | R. O. Grey · J. K. Beddow 1968 | On the Hausner ratio and its relationship to some properties of metal powders | 탭 밀도 대 겉보기 밀도 비는 건조 구리 분말에서 흐름과 동적 안식각을 따르지만 흐름 시간과 안식각을 대신하지 못한다. |
| `johnson1971_jkr_surface_energy_contact_elastic_solids` | Johnson · Kendall · Roberts 1971 | Surface energy and the contact of elastic solids | 표면 에너지를 넣은 에너지 평형으로 접촉 반경과 떼는 힘 P = −(3/2)γπR을 얻었고, 이 떼는 힘은 탄성률과 무관하다. |
| `dmt1975_adhesion_contact_deformation` | Derjaguin et al. 1975 | Effect of contact deformations on the adhesion of particles | 탄성 구와 평면의 pull-off 힘은 접촉 변형과 무관하게 점접촉 값 2πRγ이며 반경의 1차에 비례한다. |
| `molerus1975_theory_of_yield_cohesive_powders` | Molerus 1975 | Theory of yield of cohesive powders | 무작위 단분산 구 충전의 평균 접촉력과 소성 평탄화로 H = κN을 얻고 유효 항복궤적 tan φ_e = (1+κ) tan ρ를 유도했다. |
| `arzt1982_particle_coordination_densification_spheres` | Arzt 1982 | The influence of an increasing particle coordination on the densification of spherical powders | 고정된 Voronoi 셀 안에서 구가 자라는 기하로 배위수와 접촉면적을 상대밀도의 닫힌 식으로 주고 압밀과 소결에 적용했다. |
| `storakers1997_similarity_inelastic_contact` | Storåkers et al. 1997 | Similarity analysis of inelastic contact | 동차함수 재료의 비탄성 접촉은 평면 펀치 해와 누적 중첩으로 풀리고, 면적 인자 c²는 결합지수 1/m+1/n 하나로 정해진다. |
| `thorntonning1998_adhesive_elastoplastic_contact` | Thornton · Ning 1998 | A theoretical model for the stick/bounce behaviour of adhesive, elastic-plastic spheres | Hertz 탄성, p_y 항복, 선형 소성, 큰 반경 제하의 네 단계 법칙으로 점착 탄소성 구의 반발계수를 닫힌 식으로 풀었다. |
| `bouvard2000_hard_soft_powder_densification` | Bouvard 2000 | Densification behaviour of mixtures of hard and soft powders under pressure | 연상 항복응력과 압력의 크기에 따라 경입자가 압밀을 돕기도 하고, percolating 골격을 이뤄 막기도 한다. |
| `mesarovicfleck2000_dissimilar_elastoplastic_indentation` | Mesarovic · Fleck 2000 | Frictionless indentation of dissimilar elastic–plastic spheres | 평균 접촉압은 1.1 σ_y에서 항복을 시작해 경도 plateau까지 오르고, 큰 접촉에서는 다시 떨어진다. |
| `nase2001_granular_bond_collision_number_wet_cohesion` | Nase · Vargas · Abatan · McCarthy 2001 | Discrete characterization tools for cohesive granular material | 정지 더미와 호퍼는 Bo_g ≈ 1에서 급변하지만, 회전 드럼은 Bo_g가 아니라 충돌 수 Co로 보아야 전이가 드러난다. |
| `kogutetsion2002_ep_sphere_rigid_flat` | Kogut · Etsion 2002 | Elastic-Plastic Contact Analysis of a Sphere and a Rigid Flat | 강체 평판에 눌린 탄소성 구의 하중, 면적, 평균압은 두 구간 멱법칙을 따르고 ω/ω_c=110에서 완전소성에 든다. |
| `martinbouvard2003_dem_composite_cold_compaction` | Martin · Bouvard 2003 | Study of the cold compaction of composite powders by the discrete element method | 연질과 경질 구의 혼합 분말을 DEM으로 압밀해, 경질 입자가 압밀을 저지하는 두 메커니즘을 정량적으로 나누었다. |
| `begat2004_cohesive_adhesive_balance_afm_colloid_probe` | Begat · Morton · Staniforth · Price 2004 | The cohesive-adhesive balances in dry powder inhaler formulations I direct quantification by atomic force microscopy | AFM 콜로이드 탐침 하나로 자기 물질과 상대 물질 결정면의 떼는 힘 비를 재면 접촉 기하를 지우고 응집과 접착의 균형을 정량할 수 있다. |
| `jacksongreen2005_fem_elastoplastic_hemispherical_contact` | Jackson · Green 2005 | A Finite Element Study of Elasto-Plastic Hemispherical Contact Against a Rigid Flat | 탄성-완전소성 반구를 강체평판에 누르면 평균 접촉압 한계가 a/R 값에 따라 2.84σ_y에서 σ_y까지 내려간다. |
| `luding2008_cohesive_frictional_contact_models` | Luding 2008 | Cohesive, frictional powders: contact models for tension | 점착 탄소성 이력 선형 스프링 하나로 압밀, 응력완화, 인장·압축 강도시험까지 재현하고, 인장강도는 점착 강성 k_c가 정한다. |
| `matsusaka2010_triboelectric_charging_powders_review` | Matsusaka et al. 2010 | Triboelectric charging of powders: A review | 분말의 마찰 대전은 주로 유효 일함수 차를 따른 전자 이동이고, 두 모형 모두 반복 충돌에서 전하가 평형값에 지수 접근한다고 준다. |
| `gonzalez2012_nonlocal_contact_confined_granular` | Gonzalez · Cuitiño 2012 | A nonlocal contact formulation for confined granular systems | 다른 접촉력이 만드는 원거리 변형을 접근량에 더한 무보정 탄성 법칙은 구속된 입상계에서 Hertz보다 큰 하중과 이른 2차 접촉을 예측한다. |
| `sakuda2013_sulfide_mechanical_property` | Sakuda et al. 2013 | Sulfide Solid Electrolyte with Favorable Mechanical Property for All-Solid-State Lithium Battery | Li₂S–P₂S₅ 유리는 상온 냉간가압만으로 치밀해지고, 18–25 GPa의 중간 탄성률을 가져 전고체전지에 유리하다. |
| `boschpadros2014_dem_liggghts_msc_thesis` | Carles Bosch Padrós 2014 | Discrete element simulations with LIGGGHTS | LIGGGHTS의 Hertz/history 접촉식과 사용법을 정리했지만, 결과는 정량 검증이 없는 정성 데모에 그쳤다. |
| `pasha2014_linear_elastoplastic_adhesive_contact` | Pasha et al. 2014 | A linear model of elasto-plastic and adhesive contact deformation | pull-off를 소성 평탄화 면적의 표면에너지 일로 유도한 선형 접촉모델이 Thornton–Ning 모델의 충돌 거동을 거의 재현한다. |
| `thakur2014_eepa_adhesive_elastoplastic_dem` | Thakur et al. 2014 | Micromechanical analysis of cohesive granular materials using the discrete element method with an adhesive elasto-plastic contact model | EEPA 접촉모델은 접촉 소성 λ_p가 응집강도의 응력이력 의존성을 만든다는 것을 보이며 석회석 flow function을 재현한다. |
| `paulick2015_elastic_particle_properties_dem_review` | Paulick et al. 2015 | Review on the influence of elastic particle properties on DEM simulation results | 강성을 낮춰도 희박계 결과는 거의 그대로지만, 조밀계에서는 벌크계수와 접촉력 분포가 달라진다 |
| `vanlew2015_modifying_youngs_modulus_distribution` | Van Lew et al. 2015 | Modifying Young's modulus in DEM simulations based on distributions of experimental measurements | 단일 pebble 압쇄로 잰 입자별 E는 벌크값보다 낮고, 이를 넣은 DEM 침대는 더 무르다. |
| `roessler2019_dem_cohesive_aor_cylinder_lift_calibration` | Roessler · Katterfeld 2019 | DEM parameter calibration of cohesive bulk materials using a simple angle of repose test | 점착 분말에는 안식각 대신 원통 인양 중 기둥의 상 전이와 굽힘 윤곽이 재현성 있는 보정 기준이 된다. |
| `vu2019_soft_grain_compression_beyond_jamming_dic` | Vu · Barés 2019 | Soft-grain compression: Beyond the jamming point | 입자 안 변형장 통계는 재밍점과 함께 재료마다 자리가 다른 두 번째 교차를 드러낸다고 원문은 결론 짓는다. |
| `cantor2020_compaction_model_highly_deformable_particles` | Cantor et al. 2020 | Compaction Model for Highly Deformable Particle Assemblies | 초탄성 원판 1500개의 등방 압축에서 단일 입자 상자 법칙과 배위수 법칙을 곱해 압밀 식을 세웠다 |
| `cardenasbarrantes2020_rigid_deformable_mixture_compaction_nscd` | Cárdenas-Barrantes et al. 2020 | Compaction of mixtures of rigid and highly deformable particles: A micromechanical model | 2D 강체-초탄성 원판 혼합물의 압밀은 단일 입자 상자 응답과 배위수 법칙으로 기술되고, 거시 적합량은 φmax(κ) 하나다. |
| `bares2021_soft_rigid_mix_experiment_dic_proceedings` | Barés et al. 2021 | Highly strained mixtures of bidimensional soft and rigid grains: an experimental approach from the local scale | 실리콘과 PVC 원기둥 혼합을 2D로 눌러 DIC로 재니 변형은 무른 입자에 몰리고 접촉 길이는 φ에 선형으로 늘었다. |
| `cardenasbarrantes2021_soft_pentagons_compaction_micromechanics_nscd` | Cárdenas-Barrantes et al. 2021 | Micromechanical description of the compaction of soft pentagon assemblies | 2D 무른 오각형과 원판의 압밀은 거시적으로 비슷하고, 차이는 마찰에 따른 재배열과 도달 밀도에서 나오며 압밀 식은 다각형으로 넓혀진다. |
| `cardenasbarrantes2021_soft_rigid_mix_compaction_proceedings` | Cárdenas-Barrantes et al. 2021 | A micro-mechanical compaction model for granular mix of soft and rigid particles | 강체와 무른 원판 혼합의 등방 압밀은 단일 입자 압축 법칙과 배위수 증가 법칙을 묶은 식 하나로 기술되고, 거시 적합 변수는 φmax 하나다. |
| `demirtas2021_mpfem_hollow_sphere_die_compaction` | Demirtas · Klinzing 2021 | Understanding die compaction of hollow spheres using the multi-particle finite element method (MPFEM) | 입자마다 FE 메시를 준 3D MPFEM으로 중공 구를 압밀하면 껍질이 얇을수록 낮은 응력에서 전면 항복하고, 좌굴로 접촉이 다시 열린다. |
| `deng2021_mechanical_surface_energy_tester_bond_number` | Deng et al. 2021 | A study of particle adhesion for cohesive powders using a novel mechanical surface energy tester | 분말 단층을 떨어뜨려 50 % 탈착 감속도로 Bond 수를 얻었으나, 검토 측은 그 값이 1 + a₅₀/g와 같다고 본다. |
| `giannis2021_stress_based_multicontact_dem` | Giannis et al. 2021 | Stress based multi-contact model for discrete-element simulations | 응력 trace 보정항으로 접촉을 서로 묶어, 고전 DEM이 놓친 고변형 강화를 보정 계수 β 하나로 회복했다. |
| `papakyriakou2021_mechanical_behavior_inorganic_li_solid_electrolytes_nanoindentation` | Papakyriakou et al. 2021 | Mechanical behavior of inorganic lithium-conducting solid electrolytes | 글러브박스 안 온도 가변 나노압입에서 황화물은 산화물보다 무르고, 모든 고체전해질이 작은 점탄성 손실과 전위 지배 크리프를 보였다. |
| `so2021_dem_mold_pressure_assb_coldpress` | So et al. 2021 | Effect of mold pressure on compaction and ion conductivity of all-solid-state batteries revealed by the discrete element method | 접촉 소성을 넣은 3D DEM이 압밀을 재현했고, 응집체 SE의 이온전도는 φ_SE^crit = 0.13의 percolation식을 따른다. |
| `cardenasbarrantes2022_soft_hard_grains_compaction_experiment_dic` | Cárdenas-Barrantes et al. 2022 | Experimental validation of a micromechanically based compaction law for mixtures of soft and hard grains | 실리콘과 PVC 원기둥 혼합을 일축으로 누르며 입자 내부 변형을 DIC로 재어, 일축 압밀 식과 국소-전역 선형 관계를 보였다. |
| `cardenasbarrantes2022_soft_spheres_3d_compaction_nscd` | Cárdenas-Barrantes et al. 2022 | Three-dimensional compaction of soft granular packings | 입자별 유한요소로 탄성 구를 3D 압밀하면 Hertz DEM은 jammed 근처에서만 맞고, 압밀 식의 꼴은 2D와 다르다. |
| `so2022_dem_contact_model_assb_compaction_sintering` | So et al. 2022 | Contact model for DEM simulation of compaction and sintering of all-solid-state battery electrodes | Maxwell 모델에서 유도한 평형 overlap 변화율 식에 항복, 융착, 면적·스프링 보정을 묶어 LPS 압밀을 Sakuda 실험에 맞췄다. |
| `sharma2023_nmc_single_crystal_anisotropic_nanoindentation` | Sharma et al. 2023 | Nanoindentation measurements of anisotropic mechanical properties of single crystalline NMC cathodes for Li-ion batteries | NMC622 결정립 108곳의 압입과 EBSD 방위로 C_ij를 구했고, VRH 평균은 E 140.16 GPa, ν 0.253이다. |
| `electromechanical_contact_model_particulate_systems` | Zhang et al. 2024 | An electro-mechanical contact model for particulate systems | Hertz 접촉반경을 Holm 접촉저항과 벌크저항에 넣고 nodal 망으로 풀면 금속 입자계의 힘에 따른 전기저항이 해석해와 실험을 따른다. |
| `zunker2024_bulk_elastic_partII` | Zunker · Kamrin 2024 | A mechanically-derived contact model for adhesive elastic-perfectly plastic particles, Part II: Contact under high compaction—modeling a bulk elastic response | 공극이 사라진 입자의 급격한 강성 상승을 자유표면 비율 문턱과 벌크탄성률 하나로 유도한 힘으로 재현한다. |
| `zunker2024_mdr_contact_model_partI` | Zunker · Kamrin 2024 | A mechanically-derived contact model for adhesive elastic-perfectly plastic particles, Part I: Utilizing the method of dimensionality reduction | 차원축소법 위에서 소성을 1D 압자 형상의 연속 변화로 다루면 물성 다섯 개로 대변형 점착 탄소성 접촉을 예측한다. |
| `lee2025_heckel_argyrodite_powder_densification_nanoindentation` | Lee et al. 2025 | Characterization of densification behavior and mechanical properties of solid electrolyte powders for all solid-state batteries | 펀치 탄성을 뺀 다이 압축 Heckel 곡선의 단계 II 기울기 K가 나노압입 H/E와 같은 소성 순위를 준다. |
| `zunker2025_dem_large_deformation_compaction` | Zunker, Dunatunga, Thakur, Tang, Kamrin 2025 | 실험검증된 대변형 압밀 DEM (Experimentally validated DEM for large deformation powder compaction: mechanically-derived contact model and screening of non-physical contacts) | 가상 강체평면과 삼중항 위상 페널티로 MDR 접촉을 다체로 넓힌 DEM이 MPFEM과 Avicel 정제 실험의 응력을 재현했다. |
| `thompson2026_high_pressure_densification_lps_lpscl_xrd_tomography` | Thompson et al. 2026 | High Pressure Densification Investigation of Li₃PS₄ and Li₆PS₅Cl Solid Electrolytes using Combine X‐Ray Diffraction, X‐Ray Absorption Tomography and Ionic Measurement | LPSCl은 GPa 압력에서 두 단계로 치밀해지고, 감압 때 격자는 돌아오지만 선폭과 전도도 변화는 남는다. |
| `var2026_sulfide_se_mechanical_properties_local_indentation_pellet` | Var et al. 2026 | The mechanical properties of solid sulfur electrolytes: a local approach for a multiscale design | 오일 보호 고속 나노압입으로 잰 Li₆PS₅Cl 입자 값을 넣으면 완전 소성 압밀식이 실제 압력을 약 3배 낮게 준다. |
| `varkey2026_multicontact_elastoplastic_dem` | Varkey et al. 2026 | DEM simulation of solid-electrolyte separator and cathode densification using a stress-based multi-contact elasto-plastic model | 강체 구 DEM에 응력기반 다중접촉 구속항을 더하자 halide 고체전해질 분리막과 양극의 압밀 두께가 실험과 1 % 안쪽으로 맞았다. |

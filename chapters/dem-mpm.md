# MPM과 연속체 모형

전극 미세구조 · 공정 · 장 `dem-mpm` · 논문 13편 · 읽기 카드 13편

> 물질점법과 연속체 구성 모형.

## 장 서문 — 붙는 단일 속도장을 푸는 접촉 표현이 압밀 계산을 가른다

*읽기 카드 13편을 엮어 쓴 글 · 항목 29개 중 29개 검증 통과 · 2026-11-11 · 낡음: 그 뒤 이 장의 카드가 바뀌었다 (센서가 자정 뒤 다시 쓴다)*

격자 속도장이 하나인 MPM은 닿은 물체를 미끄럼 없이 붙인다. 이 장의 접촉 논문들은 이 붙음을 네 가지 길로 풀어 왔다. 알갱이별 속도장, 견인력 분리 판정, 손상장 기울기 분할, 입자별 격자가 그 길이다. [근거: Bardenhagen, Brackbill & Sulsky 2000 (`bardenhagen2000_mpm_granular_multibody_frictional_contact`); Bardenhagen, Guilkey 외 4 인 2001 (`bardenhagen2001_mpm_improved_contact_granular_stress_waves`); Homel · Herbold 2017 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`); de Vaucorbeil, Nguyen, Sinaie, Wu 2020 (`devaucorbeil2020_mpm_after_25_years_review`); Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`)]

2D 변형 입자 압밀에서는 재밍 뒤 입자 형상 변화가 치밀화를 지배하고, 배위수가 같은 제곱근 법칙을 따른다는 데까지 확인됐다. 3D 조밀 충전, 제하, 실험 검증은 대부분 비어 있다. [근거: Nguyen et al. 2017 (`nguyen2017_mpm_bpm_deformable_particle_compaction`); Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`); Mohammadhosseinzadeh et al. 2026 (`pycompact2025_dem_mpfem_workflow`); Bardenhagen et al. 2005 (`bardenhagen2005_mpm_foam_densification_simulation`)]

구성식은 F = F_E·F_P 곱분해와 return mapping 골격을 유지한 채 항복면만 바꿔 왔다. 실린 물성 절대값은 거의 옮겨 쓸 수 없다. [근거: Stomakhin et al. 2013 (`stomakhin2013_mpm_snow_elastoplastic`); Klár et al. 2016 (`klar2016_dp_sand_animation`); Lawrence et al. 2008 (`lawrence2008_single_vgcnf_elastic_modulus_morphology`)]

### 붙는 접촉을 어떻게 푸나

단일 속도장 MPM이 접촉을 붙임으로 처리한다는 진단이 접촉 연구의 출발점이다. de Vaucorbeil et al. 2020은 no-slip과 no-penetration 접촉이 단일 속도장에 추가 비용 없이 내재한다고 적었다. Bardenhagen et al. 2000은 알갱이마다 격자 속도장을 따로 풀었다. 이 장을 질량중심장과 노드마다 비교해 짝 탐색 없이 분리와 Coulomb 미끄럼을 걸었다. Bardenhagen et al. 2001은 분리를 수직 견인력이 압축인지로 판정하게 고쳤고, γ = 0.5로 작은 격자 질량에서 보정이 폭주하는 것을 막았다. [근거: de Vaucorbeil, Nguyen, Sinaie, Wu 2020 (`devaucorbeil2020_mpm_after_25_years_review`); Bardenhagen, Brackbill & Sulsky 2000 (`bardenhagen2000_mpm_granular_multibody_frictional_contact`); Bardenhagen, Guilkey 외 4 인 2001 (`bardenhagen2001_mpm_improved_contact_granular_stress_waves`)]

알갱이별 장의 다음 걸림돌은 장 수와 메모리다. 우리 산술로 알갱이별 장은 약 30 TB이고, 노드당 두 장이면 1.81 GB다. Homel and Herbold 2017은 손상장이나 표면 표지의 기울기로 노드마다 물질을 두 장에 나눴다. 2D에서 이 방식의 덧비용은 +30–50 %였다. Hu et al. 2018의 CPIC는 강체 표면 양쪽만 가르고 변형체끼리는 단일 속도장으로 남긴다. Nguyen et al. 2017과 Nezamabadi et al. 2022는 입자마다 자기 격자를 두고 Contact Dynamics로 접촉을 풀었다. [근거: Bardenhagen, Brackbill & Sulsky 2000 (`bardenhagen2000_mpm_granular_multibody_frictional_contact`); Homel · Herbold 2017 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`); Hu et al. 2018 (`hu2018_mls_mpm_cpic_two_way_rigid_coupling`); Nguyen et al. 2017 (`nguyen2017_mpm_bpm_deformable_particle_compaction`); Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`)]

### 재밍 뒤 무엇이 압밀하나

2D 변형 입자 압밀 두 편은 재밍 뒤에는 재배열이 아니라 입자 형상 변화가 치밀화를 지배한다고 보았다. Nguyen et al. 2017은 Φ0 = 0.8 이후 배위수가 (Φ−Φ0)^0.5로 늘고 마찰 영향은 작다고 적었다. Nezamabadi et al. 2022는 입자에 소성을 넣었고, 소성 입자가 탄성 입자보다 낮은 응력으로 공극을 채운다고 적었다. 같은 제곱근 법칙은 재료와 무관하게 성립했다. 두 곡선은 σ ≳ 0.35 MPa에서 갈라졌고, 이 값은 입자 항복응력 0.4 MPa보다 낮다. [근거: Nguyen et al. 2017 (`nguyen2017_mpm_bpm_deformable_particle_compaction`); Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`)]

3D나 다른 재료에서는 남는 기공의 해석이 엇갈린다. Bardenhagen et al. 2005는 탄성 발포체 단위 셀을 비압축 기준의 완전 치밀화 지점까지 눌렀고, 그 지점에서도 기공 약 35%가 남는다고 적었다. 원문은 뼈대가 서로 걸려 기공이 갇힌다고 해석했다. 검토 측은 붙는 접촉이 격자 크기의 틈을 가둬, 남은 기공 일부가 해상도 탓일 수 있다고 본다. Mohammadhosseinzadeh et al. 2026은 DEM 패킹을 입자별 FE로 넘겨 Fe–Si–Al–P 분말을 눌렀고, 상대밀도 최대 편차를 2.5 %로 보고했다. 검토 측은 이 결과의 메시 수렴이 확인되지 않았고, 마찰 µ가 사실상 보정 노브라고 본다. [근거: Bardenhagen et al. 2005 (`bardenhagen2005_mpm_foam_densification_simulation`); Mohammadhosseinzadeh et al. 2026 (`pycompact2025_dem_mpfem_workflow`)]

### 구성식의 골격과 항복면

탄소성 MPM 구성식은 같은 곱분해 골격을 유지한 채 항복면만 바꿔 왔다. Stomakhin et al. 2013은 F = F_E·F_P로 나눈 탄성부의 특이값을 임계 구간으로 클램프했다. 압축 경화는 Lamé 계수에 지수로 넣었다. Klár et al. 2016은 같은 골격에 점착 없는 Drucker-Prager 원뿔을 얹었다. 사영은 Hencky 변형률 공간에서 부피를 보존하며, 세 경우의 닫힌형으로 정리된다. Nezamabadi et al. 2022는 von Mises 항복면에 이선형 등방 경화를 붙였다. [근거: Stomakhin et al. 2013 (`stomakhin2013_mpm_snow_elastoplastic`); Klár et al. 2016 (`klar2016_dp_sand_animation`); Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`)]

우리 코드는 특이값 클램프 자리에 von Mises J2 사영을 넣었다. 우리 DPC 실험에서 cap을 더하자 300 MPa 압밀이 11 %에서 0.8 %로 나빠졌다. 검토 측은 거의 비압축인 LPSCl 입자에 부피 수축을 허용한 탓으로 본다. LPSCl 입자는 bulk 24 GPa라 300 MPa 가압에서 부피가 변하지 않는다. 이 결과는 resolved-grain에 J2를 쓰고 REV에 DP와 cap을 쓰는 분업의 근거가 된다. [근거: Stomakhin et al. 2013 (`stomakhin2013_mpm_snow_elastoplastic`); Klár et al. 2016 (`klar2016_dp_sand_animation`)]

### 준정적과 시간 척도

명시적 MPM으로 느린 과정을 풀려면 파속과 하중 속도의 간극을 인위로 메워야 하고, 그 판정은 대체로 눈 대조에 머문다. Bardenhagen et al. 2005는 판 속도를 종파속의 3 %로 두고 인공 점성을 더했다. 원문은 절반 속도 런과 응답이 비슷하다고 판정했다. 검토 측은 구조가 무너지는 구간에서 두 속도의 평균 반력이 35 % 다르다고 본다. Gritton et al. 2017은 탄성파 간격이 확산 간격보다 10 자리쯤 작아 밀도를 인위로 올렸고, 두 쌍의 형상을 견주어 차이가 작다고 판정했다. [근거: Bardenhagen et al. 2005 (`bardenhagen2005_mpm_foam_densification_simulation`); Gritton et al. 2017 (`gritton2017_mpm_chemomechanical_coupling_silicon_anode`)]

우리 판 Mach 0.01–0.03은 Bardenhagen et al. 2005의 설정과 같은 자릿수다. 그래서 절반 속도 대조를 수로 판정하는 시험 꼴을 그대로 가져올 수 있다. 우리 실측에서는 판 Mach를 바꿔도 기하는 같고 정착 응력만 움직였다. 그래서 형상만 본 Gritton et al. 2017의 시험은 우리 판 반력 판독의 근거가 되지 못한다. [근거: Bardenhagen et al. 2005 (`bardenhagen2005_mpm_foam_densification_simulation`); Gritton et al. 2017 (`gritton2017_mpm_chemomechanical_coupling_silicon_anode`)]

### 검증과 물성값의 한계

이 장의 방법 논문 대부분은 정량 검증 범위가 좁다. Stomakhin et al. 2013과 Klár et al. 2016의 결과는 렌더 프레임과 정성 비교뿐이다. Klár et al. 2016의 씬 영률은 실제 모래값에서 100× 연화한 값이다. Hu et al. 2018의 정량 검증은 MLS-MPM과 전통 MPM 두 이산화의 에너지 곡선 비교가 전부다. Homel and Herbold 2017의 자기 접촉 판정은 그림을 눈으로 대조한 것이다. [근거: Stomakhin et al. 2013 (`stomakhin2013_mpm_snow_elastoplastic`); Klár et al. 2016 (`klar2016_dp_sand_animation`); Hu et al. 2018 (`hu2018_mls_mpm_cpic_two_way_rigid_coupling`); Homel · Herbold 2017 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`)]

물성 입력값도 출처가 약하다. Lawrence et al. 2008은 Pyrograf III 단섬유 17가닥의 굽힘 탄성률이 6 to 207 GPa로 퍼진다고 적었다. 검토 측은 이 값이 양단고정 가정에 기댄 겉보기 값이라, 낮은 값이 실제보다 낮게 나왔을 수 있다고 본다. 우리 VGCF 가정값 10 GPa는 17가닥 중 16가닥보다 낮아 이 논문을 출처로 걸 수 없다. 대신 우리 민감도 창 1–100 GPa가 14가닥을 덮는다. [근거: Lawrence et al. 2008 (`lawrence2008_single_vgcnf_elastic_modulus_morphology`)]

### 이 장의 값

| 값 | 표기 | 근거 |
|---|---|---|
| 발포체 완전 치밀화 근처 남는 기공 | 35% | Bardenhagen et al. 2005 (`bardenhagen2005_mpm_foam_densification_simulation`) |
| Pyrograf III 단섬유 굽힘 탄성률 범위 | 6 to 207 GPa | Lawrence et al. 2008 (`lawrence2008_single_vgcnf_elastic_modulus_morphology`) |
| MPM 접촉 안정화 스케일(모든 사례) | γ = 0.5 | Bardenhagen, Guilkey 외 4 인 2001 (`bardenhagen2001_mpm_improved_contact_granular_stress_waves`) |
| 기울기 분할의 SF 대비 덧비용(2D) | +30–50 % | Homel · Herbold 2017 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`) |
| 2D 원판 집합체 재밍 충전율 | Φc ≃ 0.8 | Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`) |
| 2D 소성/탄성 응답 분기 응력 | σ ≳ 0.35 MPa | Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`) |
| 2D 원판 압밀 최대 평균 배위수 | 5.5 | Nguyen et al. 2017 (`nguyen2017_mpm_bpm_deformable_particle_compaction`) |
| Fe–Si–Al–P 상대밀도 최대 편차 | 2.5 % | Mohammadhosseinzadeh et al. 2026 (`pycompact2025_dem_mpfem_workflow`) |

### 아직 열린 문제

- 조밀한 3D 다접촉 노드에서 분리 가능한 접촉이 어떻게 움직이는지는 시험되지 않았다. Bardenhagen et al. 2001은 접촉 노드당 물체 둘 이하로 분석을 좁혔다. Homel and Herbold 2017은 장이 셋 이상이면 침투를 엄밀히 막지 못한다고 적었다. Nezamabadi et al. 2022의 입자별 격자 방식도 3D와 강체 AM 혼합은 다루지 않았다. [근거: Bardenhagen, Brackbill & Sulsky 2000 (`bardenhagen2000_mpm_granular_multibody_frictional_contact`); Bardenhagen, Guilkey 외 4 인 2001 (`bardenhagen2001_mpm_improved_contact_granular_stress_waves`); Homel · Herbold 2017 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`); Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`)]
- 셀 크기만 한 접촉 틈이 압밀 기공률을 얼마나 올리는지 정해지지 않았다. Homel and Herbold 2017은 이 틈 때문에 알갱이 압밀의 밀도가 어긋날 수 있다고 적었다. 검토 측은 Bardenhagen et al. 2000의 접촉과 Bardenhagen et al. 2005의 남는 기공에서 같은 계통 오차를 의심한다. [근거: Homel · Herbold 2017 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`); Bardenhagen, Brackbill & Sulsky 2000 (`bardenhagen2000_mpm_granular_multibody_frictional_contact`); Bardenhagen et al. 2005 (`bardenhagen2005_mpm_foam_densification_simulation`)]
- 제하와 탈압 단계는 거의 비어 있다. Bardenhagen et al. 2005와 Nezamabadi et al. 2022에는 제하 계산이 없다. 검토 측은 견인력 분리 판정을 제하를 다루기 위한 최소 조건으로 본다. Mohammadhosseinzadeh et al. 2026의 제하 후 상대밀도는 5 MPa 문턱 선택에 민감하다고 검토 측은 본다. [근거: Bardenhagen et al. 2005 (`bardenhagen2005_mpm_foam_densification_simulation`); Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`); Bardenhagen, Guilkey 외 4 인 2001 (`bardenhagen2001_mpm_improved_contact_granular_stress_waves`); Mohammadhosseinzadeh et al. 2026 (`pycompact2025_dem_mpfem_workflow`)]

### 먼저 읽을 논문

1. de Vaucorbeil, Nguyen, Sinaie, Wu 2020 (`devaucorbeil2020_mpm_after_25_years_review`) — MPM 변종, 접촉, 파괴 갈래를 한 틀로 정리해 나머지 논문의 위치를 잡아 준다.
2. Bardenhagen, Brackbill & Sulsky 2000 (`bardenhagen2000_mpm_granular_multibody_frictional_contact`) — 단일 속도장이 붙음을 만든다는 진단과 알갱이별 장 접촉 알고리즘의 원형이 여기서 나온다.
3. Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`) — 입자별 격자 MPM으로 소성 입자 압밀을 푼 사례이고, 우리 다속도장 후보의 실현 가능성 근거다.
4. Homel · Herbold 2017 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`) — 노드당 두 장으로 장 수와 메모리 문제를 피하는 길을 보인다.
5. Hu et al. 2018 (`hu2018_mls_mpm_cpic_two_way_rigid_coupling`) — 우리 Taichi MLS-MPM 이산화의 인용 원전이다.

## 이 장의 논문 (13편)

| digest | 저자 · 연도 | 제목 | 한 줄 결론 |
|---|---|---|---|
| `bardenhagen2000_mpm_granular_multibody_frictional_contact` | Bardenhagen, Brackbill & Sulsky 2000 | The material-point method for granular materials | 알갱이별 격자 속도장을 공통 질량중심장과 비교하면 짝 탐색 없이 분리와 Coulomb 미끄럼이 되고, 전단 변형 양상이 크게 달라진다. |
| `bardenhagen2001_mpm_improved_contact_granular_stress_waves` | Bardenhagen, Guilkey 외 4인 2001 | An improved contact algorithm for the material point method and application to stress propagation in granular material | 수직 견인력이 압축인 동안 접촉을 유지하고 작은 격자 질량에서 보정을 줄인 MPM 접촉이 3D 구 해석해와 광탄성 무늬를 정성적으로 재현한다. |
| `bardenhagen2005_mpm_foam_densification_simulation` | Bardenhagen et al. 2005 | Insight into the physics of foam densification via numerical simulation | 입자 기법 GIMP로 탄성 발포체 단위 셀을 공칭 변형률 90 %까지 누르자, 비압축 기준의 완전 치밀화 지점에서도 기공 약 35 %가 남았다. |
| `lawrence2008_single_vgcnf_elastic_modulus_morphology` | Lawrence et al. 2008 | Elastic Properties and Morphology of Individual Carbon Nanofibers | 같은 섬유의 굽힘 탄성률과 벽 형태를 짝지어 재면 값이 6에서 207 GPa까지 퍼지고, 외벽 비율과 벽 두께가 이를 가른다. |
| `stomakhin2013_mpm_snow_elastoplastic` | Stomakhin et al. 2013 | A material point method for snow simulation | F = F_E·F_P 곱분해와 특이값 클램프 return mapping을 쓴 MPM이 하나의 구성식으로 눈의 흐름, 뭉침, 파쇄를 재현한다. |
| `klar2016_dp_sand_animation` | Klár et al. 2016 | Drucker-prager elastoplasticity for sand animation | 점착 없는 Drucker-Prager 원뿔을 Hencky 변형률 공간에서 부피를 보존하며 사영하면 MPM으로 모래의 흐름과 붕괴를 재현할 수 있다. |
| `gritton2017_mpm_chemomechanical_coupling_silicon_anode` | Gritton et al. 2017 | Using the material point method to model chemical/mechanical coupling in the deformation of a silicon anode | MPM 입자에 리튬 농도를 싣고 밀도를 인위로 올려 규소 나노기둥의 리튬화와 탈리튬화를 3D로 풀었다. |
| `homel2017_mpm_field_gradient_partitioning_fracture_self_contact` | Homel · Herbold 2017 | Field‐gradient partitioning for fracture and frictional contact in the material point method | 손상장 기울기로 노드마다 물질을 두 속도장에 나누면 알갱이 수와 무관하게 파괴 뒤 마찰 접촉과 자기 접촉을 다룰 수 있다. |
| `nguyen2017_mpm_bpm_deformable_particle_compaction` | Nguyen et al. 2017 | Compaction of granular materials composed of deformable particles | 2D 무른 입자 압밀에서 형상 변화가 치밀화를 지배하고, 마찰 영향은 작으며, 배위수는 두 방법 모두 (Φ−Φ0)^0.5를 따른다. |
| `hu2018_mls_mpm_cpic_two_way_rigid_coupling` | Hu et al. 2018 | A moving least squares material point method with displacement discontinuity and two-way rigid body coupling | MLS-MPM은 APIC의 C_p로 힘과 변형구배를 구해 전달을 약 두 배 빠르게 하고, CPIC는 격자 한 장에서 강체 표면 양쪽 재료를 따로 움직이게 한다. |
| `devaucorbeil2020_mpm_after_25_years_review` | de Vaucorbeil, Nguyen, Sinaie, Wu 2020 | Material point method after 25 years: Theory, implementation, and applications | MPM 25년을 정리한 첫 종합 리뷰로, 변종, 접촉, 파괴, 응용, 코드, 타 방법과의 비교를 한 틀에 묶었다. |
| `nezamabadi2022_mpm_cd_plastic_particle_compaction` | Nezamabadi et al. 2022 | Modelling the compaction of plastic particle packings | 입자별 격자 MPM과 CD로 2D 원판 300개를 압축하자 재밍 뒤 형상 변화가 압밀을 지배했고, 소성 입자는 더 낮은 응력으로 공극을 채웠다. |
| `pycompact2025_dem_mpfem_workflow` | Mohammadhosseinzadeh et al. 2026 | PyCompact: An integrated workflow for discrete element method–multi-particle finite element method for powder compaction simulation | LIGGGHTS 침강 패킹의 (x, y, z, r) 표만 OpenRadioss MPFEM으로 넘겨 압축과 제하를 다시 풀었고, 상대밀도 편차는 최대 2.5 %였다. |

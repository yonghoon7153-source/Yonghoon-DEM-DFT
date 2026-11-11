# MPM과 연속체 모형

전극 미세구조 · 공정 · 장 `dem-mpm` · 논문 11편 · 읽기 카드 11편

> 물질점법과 연속체 구성 모형.

## 장 서문 — 닿은 입자를 떼어 놓는 접촉 표현이 압밀 MPM의 관건이다

*읽기 카드 11편을 엮어 쓴 글 · 항목 33개 중 33개 검증 통과 · 2026-11-10*

변형 입자 집합체를 MPM으로 누르려면 두 가지를 정해야 한다. 하나는 닿은 입자를 어떻게 떼어 놓고 미끄러지게 할지다. 다른 하나는 각 입자를 어떤 구성식으로 변형시킬지다. [근거: Bardenhagen, Brackbill & Sulsky 2000 (`bardenhagen2000_mpm_granular_multibody_frictional_contact`); Homel · Herbold 2017 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`); Stomakhin et al. 2013 (`stomakhin2013_mpm_snow_elastoplastic`); Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`)]

접촉 알고리즘과 탄소성 구성식의 골격은 2D 검증과 그래픽스 시연 단계까지 와 있다. 변형 입자 압밀 계산은 2D 원판 300개를 쓴 두 편과 3D MPFEM 한 편이 전부다. [근거: Bardenhagen, Brackbill & Sulsky 2000 (`bardenhagen2000_mpm_granular_multibody_frictional_contact`); Bardenhagen, Guilkey 외 4 인 2001 (`bardenhagen2001_mpm_improved_contact_granular_stress_waves`); Homel · Herbold 2017 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`); Nguyen et al. 2017 (`nguyen2017_mpm_bpm_deformable_particle_compaction`); Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`); Mohammadhosseinzadeh et al. 2026 (`pycompact2025_dem_mpfem_workflow`)]

3D 압밀, 한 노드에 여러 물체가 만나는 조밀 충전, 제하는 아직 어느 MPM 카드에서도 시험되지 않았다. [근거: Bardenhagen, Guilkey 외 4 인 2001 (`bardenhagen2001_mpm_improved_contact_granular_stress_waves`); Homel · Herbold 2017 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`); Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`)]

### 닿은 입자가 붙는 문제

격자 노드마다 속도가 하나인 MPM은 닿은 물체 사이에 미끄럼 없는 접촉을 자동으로 건다. Bardenhagen et al. 2000은 이 단일 장이 물체끼리 파고들지는 못하게 막지만 미끄럼도 막는다고 적었다. de Vaucorbeil et al. 2020은 no-slip, no-penetration 접촉이 MPM에 내재해 추가 비용이 들지 않는다고 정리했다. Homel & Herbold 2017은 이 상태를 single-field(SF) 해라 부르고, 손상이나 연화가 있으면 계면에 인공 용접이 생길 수 있다고 적었다. Hu et al. 2018은 원인을 입자 핵이 경계 너머의 노드와도 자료를 주고받는 데서 찾았다. [근거: Bardenhagen, Brackbill & Sulsky 2000 (`bardenhagen2000_mpm_granular_multibody_frictional_contact`); de Vaucorbeil, Nguyen, Sinaie, Wu 2020 (`devaucorbeil2020_mpm_after_25_years_review`); Homel · Herbold 2017 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`); Hu et al. 2018 (`hu2018_mls_mpm_cpic_two_way_rigid_coupling`)]

우리 Taichi MLS-MPM은 격자 속도장이 하나여서 이 알고리즘들을 넣기 전의 기준선에 해당한다. 그래서 우리 계산에서는 모든 접촉이 붙음 체제로 동작한다. 미끄럼이 하중 경로를 늦추는 응답은 원리상 나오지 않는다. 닿은 SE 입자가 한 덩어리로 붙어서, 우리 모델은 연화 없이 분말 압밀을 재현하지 못했다. [근거: Bardenhagen, Brackbill & Sulsky 2000 (`bardenhagen2000_mpm_granular_multibody_frictional_contact`); Bardenhagen, Guilkey 외 4 인 2001 (`bardenhagen2001_mpm_improved_contact_granular_stress_waves`); Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`)]

### 속도장을 나누는 길

해법들은 속도장을 어떤 단위로 나누는지에서 갈린다. Bardenhagen et al. 2000은 알갱이마다 격자 속도장을 따로 풀고 질량중심 속도장과 노드마다 비교했다. 짝 탐색이 없어서 비용이 알갱이 수에 선형이라고 원문은 적었다. Bardenhagen et al. 2001은 이 판에서 분리 판정을 고쳐, 수직 견인력이 압축인 동안에는 접촉을 유지하게 했다. 또 작은 격자 질량에서 보정을 줄이는 γ를 더했고, 모든 사례에 γ = 0.5를 썼으며 0.5 미만에서는 침투가 생겼다. [근거: Bardenhagen, Brackbill & Sulsky 2000 (`bardenhagen2000_mpm_granular_multibody_frictional_contact`); Bardenhagen, Guilkey 외 4 인 2001 (`bardenhagen2001_mpm_improved_contact_granular_stress_waves`)]

뒤의 방법들은 장 수를 줄이거나 갈라지는 곳을 좁힌다. Homel & Herbold 2017은 손상장 기울기로 노드마다 물질을 두 장에만 나눠, 알갱이 수와 무관하게 파괴 뒤 접촉을 풀었다. 덧비용은 2D 16 스레드에서 +30–50 %였다. Hu et al. 2018의 CPIC는 강체 표면 양쪽만 가르며, 변형체끼리는 여전히 단일 속도장이다. Nezamabadi et al. 2022는 입자마다 자기 배경격자를 두고, 입자 사이 접촉을 Contact Dynamics로 풀었다. [근거: Homel · Herbold 2017 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`); Hu et al. 2018 (`hu2018_mls_mpm_cpic_two_way_rigid_coupling`); Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`)]

우리 산술로는 SE 씨앗 32,832개 규모에서 알갱이별 장을 통째로 두면 ≈ 30 TB가 된다. 노드당 두 장이면 1.81 GB여서, 우리는 Homel & Herbold 2017의 방식이 장 수와 메모리 문제를 피하는 길이 된다고 본다. 우리가 해 볼 가장 싼 첫 단계는 다중 속도장 없이 벽과 AM 노드에 Bardenhagen et al. 2000의 식 (23)을 적용하는 것이다. 검토 측은 CPIC 임펄스를 AM 강체 운동에 돌려주는 일을 후보 A로 본다. [근거: Bardenhagen, Brackbill & Sulsky 2000 (`bardenhagen2000_mpm_granular_multibody_frictional_contact`); Homel · Herbold 2017 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`); Hu et al. 2018 (`hu2018_mls_mpm_cpic_two_way_rigid_coupling`)]

### 탄소성 구성식의 계보

탄소성 MPM의 골격은 변형구배를 F = F_E·F_P로 곱분해하고 return mapping을 거는 것이다. 논문마다 바뀌는 것은 항복면이다. Stomakhin et al. 2013은 탄성부 특이값을 [1−θ_c, 1+θ_s] 구간으로 클램프하고, 압축 경화를 Lamé 계수의 지수에 넣었다. Klár et al. 2016은 Hencky 변형률 공간에서 점착 없는 Drucker-Prager 원뿔로 사영했다. 옆면 사영은 부피를 보존하는 non-associative 방향을 따른다. Nezamabadi et al. 2022는 von Mises에 이선형 등방 경화를 붙였다. [근거: Stomakhin et al. 2013 (`stomakhin2013_mpm_snow_elastoplastic`); Klár et al. 2016 (`klar2016_dp_sand_animation`); Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`)]

우리 코드는 Stomakhin et al. 2013의 특이값 클램프 자리에 von Mises J2 항복면 사영을 넣었다. 우리 DPC 실험에서는 cap을 더하자 300 MPa 압밀이 11 %에서 0.8 %로 나빠졌다. 검토 측은 거의 비압축인 LPSCl 입자에 입자 부피 수축을 허용한 탓으로 본다. 그래서 우리는 resolved-grain에 J2를, homogenized REV에 DP와 cap을 쓰는 분업의 근거를 Klár et al. 2016에서 찾는다. [근거: Stomakhin et al. 2013 (`stomakhin2013_mpm_snow_elastoplastic`); Klár et al. 2016 (`klar2016_dp_sand_animation`)]

### 재밍 뒤 압밀의 주인

2D 변형 입자 압밀을 다룬 두 편은 재밍 뒤 치밀화를 입자 형상 변화가 지배한다는 데서 일치한다. Nguyen et al. 2017은 Φ0 ≃ 0.8까지 재배열이 일어나고, 그 뒤 배위수가 (Φ−Φ0)^0.5로 는다고 적었다. Nezamabadi et al. 2022도 Φc ≃ 0.8을 전환점으로 보았다. 초과 배위수는 탄성, 소성과 무관하게 (Φ−Φc)^0.5를 따랐다. 소성 입자는 탄성 입자보다 낮은 응력으로 공극을 채웠고, 두 곡선은 σ ≳ 0.35 MPa에서 갈라졌다. 이 값은 입자 항복응력 0.4 MPa보다 낮다. [근거: Nguyen et al. 2017 (`nguyen2017_mpm_bpm_deformable_particle_compaction`); Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`)]

두 편이 입자 변형을 연속체로 푼 이유는 점접촉 법칙이 큰 변형에서 깨지기 때문이다. Nguyen et al. 2017의 MPM 원판은 ε > 0.05에서 2D Hertz 직선을 벗어났다. Nezamabadi et al. 2022는 Hertz 접촉이 약 10% 변형률까지만 유효하다고 적었다. Nguyen et al. 2017은 마찰이 Φ에는 영향이 없고 Z에만 작게 작용한다고 적었다. 검토 측은 MPM이 탄성이고 BPM이 소성이어서, 두 방법의 차이를 표현 방식 탓으로 돌릴 수 없다고 본다. [근거: Nguyen et al. 2017 (`nguyen2017_mpm_bpm_deformable_particle_compaction`); Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`)]

3D 압밀을 실험과 맞춘 것은 Mohammadhosseinzadeh et al. 2026의 입자별 FE 한 편이다. Fe–Si–Al–P 분말을 2000 MPa까지 눌렀을 때 상대밀도 최대 편차는 2.5 %였다. 검토 측은 메시 수렴이 확인되지 않았고 마찰 µ가 사실상 보정 노브라고 본다. 이 워크플로는 압축 전에 DEM 좌표를 넘긴다. 우리 scaffold는 300 MPa 압축이 끝난 뒤에 넘긴다. [근거: Mohammadhosseinzadeh et al. 2026 (`pycompact2025_dem_mpfem_workflow`)]

### 검증 깊이와 옮길 값

접촉 알고리즘 논문들은 해석해 대조에서 해상도 규칙을 남겼다. Bardenhagen et al. 2000은 경사면 원판이 지름당 16 요소에서 강체 해석해와 잘 맞는다고 적었다. Bardenhagen et al. 2001은 3D 구가 지름당 8 셀 이상에서 수렴하고, 지름 4 셀에서는 구르지 못한다고 적었다. 우리 SE 1 µm 입자는 현재 격자에서 지름당 약 7 셀이다. 이는 Bardenhagen et al. 2001이 구름을 확인한 8 셀 바로 아래다. [근거: Bardenhagen, Brackbill & Sulsky 2000 (`bardenhagen2000_mpm_granular_multibody_frictional_contact`); Bardenhagen, Guilkey 외 4 인 2001 (`bardenhagen2001_mpm_improved_contact_granular_stress_waves`)]

그래픽스 논문들은 알고리즘 골격만 옮길 수 있다. Stomakhin et al. 2013과 Klár et al. 2016은 결과를 렌더 프레임으로만 냈다. Klár et al. 2016의 영률은 실제 모래값에서 100× 연화한 값이다. Hu et al. 2018의 정량 검증은 두 이산화끼리의 에너지 곡선이 전부다. de Vaucorbeil et al. 2020은 MPM이 매우 고운 격자에서 수렴하지 않는다고 적었다. [근거: Stomakhin et al. 2013 (`stomakhin2013_mpm_snow_elastoplastic`); Klár et al. 2016 (`klar2016_dp_sand_animation`); Hu et al. 2018 (`hu2018_mls_mpm_cpic_two_way_rigid_coupling`); de Vaucorbeil, Nguyen, Sinaie, Wu 2020 (`devaucorbeil2020_mpm_after_25_years_review`)]

입력 물성의 근거도 좁다. Lawrence et al. 2008은 개별 탄소나노섬유의 굽힘 탄성률을 쟀고, 그 값은 6 to 207 GPa로 퍼졌다. 우리가 가정한 VGCF 탄성률 10 GPa는 17가닥 중 16가닥보다 낮아서 이 논문을 출처로 걸 수 없다. 우리 민감도 창 1–100 GPa는 17가닥 중 14가닥을 덮는다. 그 창에서 우리 결과는 Δε 0.18 %p, Δσ_e ≤ 0.25 %만 움직였다. [근거: Lawrence et al. 2008 (`lawrence2008_single_vgcnf_elastic_modulus_morphology`)]

### 이 장의 값

| 값 | 표기 | 근거 |
|---|---|---|
| 접촉 스케일 γ, 모든 사례 | γ = 0.5 | Bardenhagen, Guilkey 외 4 인 2001 (`bardenhagen2001_mpm_improved_contact_granular_stress_waves`) |
| 두 장 분할의 SF 대비 덧비용, 2D | +30–50 % | Homel · Herbold 2017 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`) |
| CPIC 덧비용, 바나나 절단 | 6% | Hu et al. 2018 (`hu2018_mls_mpm_cpic_two_way_rigid_coupling`) |
| 기준 마찰각, 모래 DP | φ_F = 30° | Klár et al. 2016 (`klar2016_dp_sand_animation`) |
| 2D 원판 압밀 재밍 충전율 | Φc ≃ 0.8 | Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`) |
| 2D 집합체 최대 평균 배위수 | 5.5 | Nguyen et al. 2017 (`nguyen2017_mpm_bpm_deformable_particle_compaction`) |
| 탄소나노섬유 굽힘 탄성률 범위 | 6 to 207 GPa | Lawrence et al. 2008 (`lawrence2008_single_vgcnf_elastic_modulus_morphology`) |
| MPFEM 상대밀도 최대 편차 | 2.5 % | Mohammadhosseinzadeh et al. 2026 (`pycompact2025_dem_mpfem_workflow`) |

### 아직 열린 문제

- 한 노드에 셋 이상의 물체가 만나는 조밀 충전에서 접촉이 어떻게 동작하는지는 비어 있다. Bardenhagen et al. 2001은 분석을 접촉 노드당 물체 둘 이하로 좁혔다. Homel & Herbold 2017은 장이 셋 이상이면 쌍별 힘이 침투를 엄밀히 막지 못한다고 적었다. Bardenhagen et al. 2000에는 압밀 계산이 없다. [근거: Bardenhagen, Brackbill & Sulsky 2000 (`bardenhagen2000_mpm_granular_multibody_frictional_contact`); Bardenhagen, Guilkey 외 4 인 2001 (`bardenhagen2001_mpm_improved_contact_granular_stress_waves`); Homel · Herbold 2017 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`)]
- 셀 크기만 한 접촉 틈이 압밀 밀도를 얼마나 바꾸는지는 측정되지 않았다. 검토 측은 Bardenhagen et al. 2000에서 이 틈이 압밀 기공률을 올리는 계통 오차가 될 수 있다고 본다. Homel & Herbold 2017도 알갱이 압밀에서 연속체 밀도가 입자 밀도와 어긋날 수 있다고 적었다. [근거: Bardenhagen, Brackbill & Sulsky 2000 (`bardenhagen2000_mpm_granular_multibody_frictional_contact`); Homel · Herbold 2017 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`)]
- 입자별 장 MPM이 3D와 우리 규모에서 작동하는지는 아직 모른다. 강체 AM이 섞인 계와 제하도 시험되지 않았다. 우리는 Nezamabadi et al. 2022를 실현 가능성의 근거로만 삼는다. 검토 측은 소성 계면의 제하 값이 Bardenhagen et al. 2001로 보장되지 않는다고 본다. [근거: Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`); Bardenhagen, Guilkey 외 4 인 2001 (`bardenhagen2001_mpm_improved_contact_granular_stress_waves`)]
- 고충전율에서 모델과 계산이 벌어지는 원인이 해상도인지는 가려지지 않았다. Nezamabadi et al. 2022에는 격자 간격과 수렴 시험이 없다. Mohammadhosseinzadeh et al. 2026에서는 요소 수를 늘리자 95 % 밀도 축응력이 1650에서 1310 MPa로 평탄부 없이 줄었다. [근거: Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`); Mohammadhosseinzadeh et al. 2026 (`pycompact2025_dem_mpfem_workflow`)]

### 먼저 읽을 논문

1. de Vaucorbeil, Nguyen, Sinaie, Wu 2020 (`devaucorbeil2020_mpm_after_25_years_review`) — MPM 변종, 접촉, 파괴 처리의 계보를 한 장의 지도로 먼저 잡아 준다.
2. Bardenhagen, Brackbill & Sulsky 2000 (`bardenhagen2000_mpm_granular_multibody_frictional_contact`) — 단일 속도장이 닿은 물체를 붙이는 문제와 다중 장 접촉의 원형 알고리즘을 처음 제시한다.
3. Nezamabadi et al. 2022 (`nezamabadi2022_mpm_cd_plastic_particle_compaction`) — 입자별 격자로 붙음을 없애고 2D 소성 원판 압밀을 푼 선례로, 우리 후보 A′의 근거다.
4. Homel · Herbold 2017 (`homel2017_mpm_field_gradient_partitioning_fracture_self_contact`) — 노드당 두 장으로 장 수와 메모리 문제를 피하는 확장 경로를 보여 준다.
5. Hu et al. 2018 (`hu2018_mls_mpm_cpic_two_way_rigid_coupling`) — 우리 Taichi MPM substep()이 따르는 MLS-MPM 이산화의 인용 원전이다.

## 이 장의 논문 (11편)

| digest | 저자 · 연도 | 제목 | 한 줄 결론 |
|---|---|---|---|
| `bardenhagen2000_mpm_granular_multibody_frictional_contact` | Bardenhagen, Brackbill & Sulsky 2000 | The material-point method for granular materials | 알갱이별 격자 속도장을 공통 질량중심장과 비교하면 짝 탐색 없이 분리와 Coulomb 미끄럼이 되고, 전단 변형 양상이 크게 달라진다. |
| `bardenhagen2001_mpm_improved_contact_granular_stress_waves` | Bardenhagen, Guilkey 외 4인 2001 | An improved contact algorithm for the material point method and application to stress propagation in granular material | 수직 견인력이 압축인 동안 접촉을 유지하고 작은 격자 질량에서 보정을 줄인 MPM 접촉이 3D 구 해석해와 광탄성 무늬를 정성적으로 재현한다. |
| `lawrence2008_single_vgcnf_elastic_modulus_morphology` | Lawrence et al. 2008 | Elastic Properties and Morphology of Individual Carbon Nanofibers | 같은 섬유의 굽힘 탄성률과 벽 형태를 짝지어 재면 값이 6에서 207 GPa까지 퍼지고, 외벽 비율과 벽 두께가 이를 가른다. |
| `stomakhin2013_mpm_snow_elastoplastic` | Stomakhin et al. 2013 | A material point method for snow simulation | F = F_E·F_P 곱분해와 특이값 클램프 return mapping을 쓴 MPM이 하나의 구성식으로 눈의 흐름, 뭉침, 파쇄를 재현한다. |
| `klar2016_dp_sand_animation` | Klár et al. 2016 | Drucker-prager elastoplasticity for sand animation | 점착 없는 Drucker-Prager 원뿔을 Hencky 변형률 공간에서 부피를 보존하며 사영하면 MPM으로 모래의 흐름과 붕괴를 재현할 수 있다. |
| `homel2017_mpm_field_gradient_partitioning_fracture_self_contact` | Homel · Herbold 2017 | Field‐gradient partitioning for fracture and frictional contact in the material point method | 손상장 기울기로 노드마다 물질을 두 속도장에 나누면 알갱이 수와 무관하게 파괴 뒤 마찰 접촉과 자기 접촉을 다룰 수 있다. |
| `nguyen2017_mpm_bpm_deformable_particle_compaction` | Nguyen et al. 2017 | Compaction of granular materials composed of deformable particles | 2D 무른 입자 압밀에서 형상 변화가 치밀화를 지배하고, 마찰 영향은 작으며, 배위수는 두 방법 모두 (Φ−Φ0)^0.5를 따른다. |
| `hu2018_mls_mpm_cpic_two_way_rigid_coupling` | Hu et al. 2018 | A moving least squares material point method with displacement discontinuity and two-way rigid body coupling | MLS-MPM은 APIC의 C_p로 힘과 변형구배를 구해 전달을 약 두 배 빠르게 하고, CPIC는 격자 한 장에서 강체 표면 양쪽 재료를 따로 움직이게 한다. |
| `devaucorbeil2020_mpm_after_25_years_review` | de Vaucorbeil, Nguyen, Sinaie, Wu 2020 | Material point method after 25 years: Theory, implementation, and applications | MPM은 격자를 매번 되돌려 mesh distortion 없이 대변형, 접촉, 파괴를 다루고, 25년 동안 여러 변종과 응용으로 갈라졌다. |
| `nezamabadi2022_mpm_cd_plastic_particle_compaction` | Nezamabadi et al. 2022 | Modelling the compaction of plastic particle packings | 입자별 격자 MPM과 CD로 2D 원판 300개를 압축하자 재밍 뒤 형상 변화가 압밀을 지배했고, 소성 입자는 더 낮은 응력으로 공극을 채웠다. |
| `pycompact2025_dem_mpfem_workflow` | Mohammadhosseinzadeh et al. 2026 | PyCompact: An integrated workflow for discrete element method–multi-particle finite element method for powder compaction simulation | LIGGGHTS 침강 패킹의 좌표와 반지름만 OpenRadioss MPFEM에 넘겨 압축을 풀고 상대밀도를 실험과 2.5 % 안에서 맞췄다. |

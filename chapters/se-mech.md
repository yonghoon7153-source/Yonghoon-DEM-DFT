# 기계 · 열 물성과 막 공정

전해질 · 계면 · 장 `se-mech` · 논문 9편 · 읽기 카드 9편

> 탄성 상수, 압력에 따른 전도도, 열전도, 전해질 막 제조.

## 장 서문 — 황화물 전해질의 물성 값은 모델과 압력 조건에 묶여 있다

*읽기 카드 9편을 엮어 쓴 글 · 항목 30개 중 29개 검증 통과 · 2026-11-10 · 낡음: 그 뒤 이 장의 카드가 바뀌었다 (센서가 자정 뒤 다시 쓴다)*

아홉 편은 황화물 고체전해질이 얼마나 무른지 묻는다. 이어서 그 무름이 탄성 계산, 전도도 측정, 열전도, 막과 셀 성능에 어떻게 드러나는지를 다룬다. [근거: Deng et al. 2016 (`deng2016_elastic_superionic_electrolytes_dft`); Cronau et al. 2021 (`cronau2021_stack_pressure_ionic_conductivity`); Böger et al. 2023 (`boger2023_thermal_conductivity_argyrodite_lgps`); Torii et al. 2025 (`torii2025_lpscl_mechanical_anisotropy_dft`); Cao et al. 2026 (`cao2026_dual_binder_18um_sulfide_electrolyte_film`); Jung et al. 2026 (`jung2026_sio2_cosubstitution_mechanical_argyrodite`)]

계산은 Li₆PS₅Cl이 무르고 탄성이 거의 등방이라는 데 모인다. 절대값은 범함수와 질서 모델에 따라 달라진다. [근거: Deng et al. 2016 (`deng2016_elastic_superionic_electrolytes_dft`); Torii et al. 2025 (`torii2025_lpscl_mechanical_anisotropy_dft`); Jung et al. 2026 (`jung2026_sio2_cosubstitution_mechanical_argyrodite`)]

실험값은 적층압, 밀링, 공극, 바인더에 따라 움직인다. 그래서 많은 수치가 펠릿이나 막의 조건과 떼어 낼 수 없다. [근거: Cronau et al. 2021 (`cronau2021_stack_pressure_ionic_conductivity`); Cronau et al. 2022 (`cronau2022_wet_milling_particle_size_ionic_conductivity`); Böger et al. 2023 (`boger2023_thermal_conductivity_argyrodite_lgps`); Cao et al. 2026 (`cao2026_dual_binder_18um_sulfide_electrolyte_film`)]

### 계산 탄성값의 폭

Li₆PS₅Cl의 계산 탄성률은 모두 무른 영역에 들지만 범함수에 따라 절대값이 갈린다. Deng et al. 2016은 PBEsol로 E=22.1, G=8.1 GPa를 얻었다. Torii et al. 2025는 PBE-D3로 E=27.4, B=34.7 GPa를 얻었다. 검토 측은 Torii et al. 2025의 값이 D3 보정 때문에 D3 없는 PBE 값보다 계통적으로 높다고 본다. [근거: Deng et al. 2016 (`deng2016_elastic_superionic_electrolytes_dft`); Torii et al. 2025 (`torii2025_lpscl_mechanical_anisotropy_dft`)]

두 계산의 원자 배치를 두고 카드가 엇갈린다. Torii et al. 2025는 Deng et al. 2016이 SQS 모델로 A=0.92를 보고했다고 적었다. 검토 측은 Deng et al. 2016에 SQS가 없고 Li를 24g 자리에만 둔 완전 질서 모델이며, 0.93은 인쇄된 Cᵢⱼ로 검토 측이 유도한 값이라고 확인했다. Deng et al. 2016의 계산은 할라이드를 Cl에서 I로 바꾸면 E가 +36 % 단단해진다. 검토 측은 이 방향이 실험과 반대라고 본다. [근거: Deng et al. 2016 (`deng2016_elastic_superionic_electrolytes_dft`); Torii et al. 2025 (`torii2025_lpscl_mechanical_anisotropy_dft`)]

### 강성의 득과 실

전해질이 무른 것이 유리한지는 논문마다 보는 장면이 다르다. Deng et al. 2016은 무른 thiophosphate가 냉간가압만으로 치밀해지고 양극의 격자 변화를 받아 주며 접촉을 유지한다고 적었다. Jung et al. 2026은 Si와 O를 공치환해 전해질을 단단하게 하자 NCM 복합 양극의 접촉 손실이 줄고 500 사이클 용량유지율이 83.9에서 90.8 %로 올랐다고 적었다. 그 대가로 이온전도도가 떨어졌다. 검토 측은 분리층까지 각자의 SE를 써서 셀 차이를 양극 안 SE의 효과만으로 돌릴 수 없다고 보고, DFT에서도 공치환 26.70 GPa가 Si 단독 27.79 GPa보다 무르다고 지적한다. [근거: Deng et al. 2016 (`deng2016_elastic_superionic_electrolytes_dft`); Jung et al. 2026 (`jung2026_sio2_cosubstitution_mechanical_argyrodite`)]

파괴의 관점에서는 강성보다 결함과 전단이 관건으로 나온다. Deng et al. 2016은 강성보다 치밀하고 균열 없는 상태가 실제 관건이라고 결론지었다. Torii et al. 2025는 Li₆PS₅Cl이 {001} 면 전단에서 변형률 0.007에 응력이 급락한다고 계산했다. Tian et al. 2020은 LiPON 박막 셀에서 분해 계면층의 수축이 충전보다 큰 응력을 만든다고 계산했다. 검토 측은 그 10–27 GPa가 실제 응력이 아니라 선형 탄성이 깨진다는 신호이고, 황화물은 모델에 없다고 본다. [근거: Deng et al. 2016 (`deng2016_elastic_superionic_electrolytes_dft`); Torii et al. 2025 (`torii2025_lpscl_mechanical_anisotropy_dft`); Tian et al. 2020 (`tian2020_electrochemo_mechanical_stress_assb`)]

### 전도도와 측정 조건

황화물 펠릿의 전도도는 결정도 클래스에 따라 압력 의존이 다르다. Cronau et al. 2021은 비정질과 유리세라믹이 제작압으로 비가역 소결되어 낮은 적층압에서도 값이 평탄하다고 적었다. 미세결정은 소결되지 않아 200–250 MPa 이상의 적층압이나 펠릿 어닐링이 있어야 평탄값에 닿았다. µC-Li₆PS₅Br은 펠릿 어닐링 전 0.59 mS/cm에서 어닐링 뒤 2.40 mS/cm가 되었다. 검토 측은 이 0.59가 SI 원 데이터 판독값과 맞지 않는다고 본다. [근거: Cronau et al. 2021 (`cronau2021_stack_pressure_ionic_conductivity`)]

입자를 줄이는 공정도 전도도를 깎는다. Cronau et al. 2022에서는 습식 밀링 시간이 길수록 전도도가 2.5에서 0.36 mS/cm까지 떨어졌고, 첫 방전 용량은 2 h에서 가장 높았다. 검토 측은 입경과 밀링 손상이 밀링 시간 하나로 함께 움직였으므로 전도도를 입자크기의 함수로 말할 수 없다고 본다. 우리 σ_grain 3.0 mS/cm는 Cronau et al. 2021 SI의 µC-Li₆PS₅Cl 펠릿 고적층압 평탄의 하단으로 추적되므로 단결정이나 grain-interior 라벨을 빼야 한다. Cronau et al. 2022에는 Li₆PS₅Cl 측정도 반경별 구간값도 없어 우리 Cronau(r_SE) 구간값은 프로젝트 가정으로 표기한다. [근거: Cronau et al. 2021 (`cronau2021_stack_pressure_ionic_conductivity`); Cronau et al. 2022 (`cronau2022_wet_milling_particle_size_ionic_conductivity`)]

### 열전도와 공극 보정

Böger et al. 2023은 공극을 외삽으로 뺀 다섯 황화물의 치밀 κ_SE가 좁은 범위에 모인다고 보고했다. 폭은 0.49–0.71 W m⁻¹ K⁻¹이고, 공극 지수 α는 2.1–3.2로 구형 이론값 1.5보다 가팔랐다. κ_SE는 측정 온도 범위에서 거의 변하지 않았고, 검토 측은 이를 유리와 비슷한 diffuson 거동에 가깝다고 본다. 원문은 Li₆PS₅Cl의 포논 가지 대부분이 거의 무분산이라 군속도가 매우 낮다고 적었다. [근거: Böger et al. 2023 (`boger2023_thermal_conductivity_argyrodite_lgps`)]

검토 측은 이 값이 단결정 값이 아니라 소결 펠릿을 외삽한 다결정 값이라고 본다. 실온 κ_SE는 SI에 숫자로 없고, 다른 문헌이 인용한 0.66도 SI에서 찾지 못했다. 같은 그룹의 다른 배치 펠릿은 같은 φ에서 0.74배여서 검토 측은 배치 의존이 크다고 본다. 우리 두 솔버의 κ_SE 0.7 W m⁻¹ K⁻¹은 173 K 치밀 외삽값과 같다. 검토 측은 출처 라벨을 이 SI로 바꿀 수 있다고 판단한다. [근거: Böger et al. 2023 (`boger2023_thermal_conductivity_argyrodite_lgps`)]

### 막 공정과 응력 분산

건식 막 공정에서는 바인더가 전도도를 얼마나 덜 깎는지가 쟁점이다. Cao et al. 2026은 PTFE 전구막에 LiTFSI-PMEMA를 접어 넣고 열압연을 반복해 18 µm, 1.56 mS cm⁻¹ 자립막을 만들었다. 검토 측은 이 값이 1 wt% PTFE 전구막의 2.67 mS cm⁻¹보다 낮으므로 전도성 바인더가 PTFE보다 덜 막는다는 수준까지만 말할 수 있다고 본다. 검토 측은 DFT 장벽 서열도 같은 논문의 실측과 차수가 맞지 않는다고 본다. [근거: Cao et al. 2026 (`cao2026_dual_binder_18um_sulfide_electrolyte_film`)]

Yuan et al. 2026은 PEO-LiTFSI 막에 SiO₂ 나노시트를 층층이 넣어 셀 압력 증가를 줄였다고 보고했다. 원문은 이를 응력 분포가 고르게 되어 석출이 균일해진 결과로 설명했다. 검토 측이 원자료로 다시 잰 변동계수는 두 셀이 거의 같았다. 차이는 평균 압력 증가량에 있었고, bare가 +0.075 MPa, layered가 +0.020 MPa였다. 검토 측은 FEM, 위상장, DFT도 응력 효과를 따로 떼어 내지 못했다고 본다. [근거: Yuan et al. 2026 (`yuan2026_layered_composite_electrolyte_stress_homogenization_li_metal`)]

### 이 장의 값

| 값 | 표기 | 근거 |
|---|---|---|
| Li₆PS₅Cl E와 G (PBEsol, 질서 모델) | E=22.1 / G=8.1 GPa | Deng et al. 2016 (`deng2016_elastic_superionic_electrolytes_dft`) |
| Li₆PS₅Cl 전단 파괴 변형률 ({001}) | 0.007 (0.7 %) | Torii et al. 2025 (`torii2025_lpscl_mechanical_anisotropy_dft`) |
| Monroe–Newman 임계 전단탄성률 | 4.2 GPa | Deng et al. 2016 (`deng2016_elastic_superionic_electrolytes_dft`) |
| µC 황화물 펠릿 평탄 도달 적층압 | > 200–250 MPa | Cronau et al. 2021 (`cronau2021_stack_pressure_ionic_conductivity`) |
| 황화물 다섯 종 치밀 κ_SE 폭 | 0.49–0.71 W m⁻¹ K⁻¹ | Böger et al. 2023 (`boger2023_thermal_conductivity_argyrodite_lgps`) |
| 18 µm 건식막(USF) 이온전도도 | 1.56 mS cm⁻¹ | Cao et al. 2026 (`cao2026_dual_binder_18um_sulfide_electrolyte_film`) |
| LPSiSOCl AFM Young's modulus | 21.2 GPa | Jung et al. 2026 (`jung2026_sio2_cosubstitution_mechanical_argyrodite`) |

### 아직 열린 문제

- Li 무질서가 argyrodite 탄성에 주는 영향은 문헌에 계산이 없다. Deng et al. 2016과 Torii et al. 2025는 질서 모델이고, Deng et al. 2016의 할라이드 경향은 검토 측이 보기에 실험과 반대다. [근거: Deng et al. 2016 (`deng2016_elastic_superionic_electrolytes_dft`); Torii et al. 2025 (`torii2025_lpscl_mechanical_anisotropy_dft`)]
- 전해질을 단단하게 하는 것이 셀에 이로운지는 정리되지 않았다. Deng et al. 2016은 무름의 접촉 이점을 들었고, Jung et al. 2026의 반대 결과는 분리층 SE 차이와 반복수 부재로 검토 측이 방향성 논증으로만 읽는다. [근거: Deng et al. 2016 (`deng2016_elastic_superionic_electrolytes_dft`); Jung et al. 2026 (`jung2026_sio2_cosubstitution_mechanical_argyrodite`)]
- 입자크기만 바꾼 전도도 측정이 없다. Cronau et al. 2022는 입경과 밀링 손상이 섞여 있고, Cronau et al. 2021 쪽에서도 입자 반경에 따른 breakpoint 수치는 측정된 적이 없다. [근거: Cronau et al. 2021 (`cronau2021_stack_pressure_ionic_conductivity`); Cronau et al. 2022 (`cronau2022_wet_milling_particle_size_ionic_conductivity`)]
- 황화물 전해질에서 분해나 석출이 만드는 응력과 그 분포는 아직 잰 사람이 없다. Tian et al. 2020은 LiPON만 모델했고, Yuan et al. 2026의 응력 균질화는 검토 측이 보기에 측정으로 보이지 않았다. [근거: Tian et al. 2020 (`tian2020_electrochemo_mechanical_stress_assb`); Yuan et al. 2026 (`yuan2026_layered_composite_electrolyte_stress_homogenization_li_metal`)]

### 먼저 읽을 논문

1. Deng et al. 2016 (`deng2016_elastic_superionic_electrolytes_dft`) — 여섯 물질군 23종의 전체 탄성텐서를 한 방법으로 계산해 이후 탄성 비교의 기준점이 된다.
2. Torii et al. 2025 (`torii2025_lpscl_mechanical_anisotropy_dft`) — 같은 Li₆PS₅Cl을 다른 범함수로 계산하고 전단 취성을 더해 Deng et al. 2016과 나란히 읽기 좋다.
3. Cronau et al. 2021 (`cronau2021_stack_pressure_ionic_conductivity`) — 황화물 전도도가 제작압과 적층압에 어떻게 묶이는지 보여 실험값을 읽는 기준을 준다.
4. Jung et al. 2026 (`jung2026_sio2_cosubstitution_mechanical_argyrodite`) — 강성 변화와 셀 열화를 한 줄로 이어 강성의 득실 쟁점을 실험 쪽에서 보여 준다.
5. Böger et al. 2023 (`boger2023_thermal_conductivity_argyrodite_lgps`) — 공극 보정 방식과 치밀 외삽값의 한계를 한 논문 안에서 볼 수 있다.

## 이 장의 논문 (9편)

| digest | 저자 · 연도 | 제목 | 한 줄 결론 |
|---|---|---|---|
| `deng2016_elastic_superionic_electrolytes_dft` | Deng et al. 2016 | Elastic Properties of Alkali Superionic Conductor Electrolytes from First Principles Calculations | PBEsol로 23종 초이온 전도체의 전체 탄성텐서를 계산해 thiophosphate가 가장 무르고 연성임을 보였다. |
| `tian2020_electrochemo_mechanical_stress_assb` | Tian et al. 2020 | Evaluation of The Electrochemo-Mechanically Induced Stress in All-Solid-State Li-Ion Batteries | Si/LiPON/LiCoO₂ 박막 셀에서 LiPON 분해 계면층의 부피 수축이 1.2 C 충전보다 큰 최대 제1주응력을 만든다고 계산했다. |
| `cronau2021_stack_pressure_ionic_conductivity` | Cronau et al. 2021 | How to Measure a Reliable Ionic Conductivity? The Stack Pressure Dilemma of Microcrystalline Sulfide-Based Solid Electrolytes | 비정질과 유리세라믹은 제작압으로 소결되지만 미세결정은 소결되지 않아, 측정 때의 적층압이 전도도를 좌우한다. |
| `cronau2022_wet_milling_particle_size_ionic_conductivity` | Cronau et al. 2022 | Ionic Conductivity versus Particle Size of Ball‐Milled Sulfide‐Based Solid Electrolytes: Strategy Towards Optimized Composite Cathode Performance in All‐Solid‐State Batteries | 저에너지 습식 밀링으로 SE 입자를 1 µm까지 줄이면 용량이 오르지만, 전도도 하락이 커져 2 h에서 용량이 최대가 된다. |
| `boger2023_thermal_conductivity_argyrodite_lgps` | Böger et al. 2023 | Thermal Conductivities of Lithium-Ion-Conducting Solid Electrolytes | 밀도가 다른 펠릿의 LFA 값을 Bruggeman 식으로 외삽하면 다섯 고체전해질의 치밀 κ_SE는 0.49–0.71 W m⁻¹ K⁻¹이고, 공극 지수는 1.5보다 크다. |
| `torii2025_lpscl_mechanical_anisotropy_dft` | Torii et al. 2025 | First-Principles Investigation of Mechanical Properties and Anisotropy of Argyrodite Li₆PS₅Cl Crystal Electrolytes | Li₆PS₅Cl은 인장에는 변형률 0.2까지 선형으로 버티지만 전단에는 변형률 0.007에서 Li₄Cl 형성과 함께 파괴된다. |
| `cao2026_dual_binder_18um_sulfide_electrolyte_film` | Cao et al. 2026 | Dual‐Binder‐Enabled 18‐µm‐Thick High‐Conductivity Sulfide Electrolyte Film for High‐Energy‐Density All‐Solid‐State Batteries | PTFE 전구막에 LiTFSI-PMEMA를 접어 넣어 18 µm, 1.56 mS cm⁻¹ 막을 얻었지만, DFT 기반 수송 기전은 근거가 약하다. |
| `jung2026_sio2_cosubstitution_mechanical_argyrodite` | Jung et al. 2026 | Enhancing the Mechanical Properties of Solid Electrolytes for Crack‐Resistant Cathodes in All‐Solid‐State Batteries | Li₆PS₅Cl에 Si와 O를 공치환해 탄성률을 올리자 NCM 복합 양극의 접촉 손실과 용량 감소가 줄었고, 대가로 이온전도도가 떨어졌다. |
| `yuan2026_layered_composite_electrolyte_stress_homogenization_li_metal` | Yuan et al. 2026 | Stress homogenization enabled by a layered composite electrolyte for high-performance all-solid-state lithium metal batteries | 층상 SiO₂ 나노시트 막은 셀 압력 증가를 줄이고 셀 수명을 늘렸다. 그러나 응력 분포가 고르게 된다는 것은 측정으로 보이지 않았다. |

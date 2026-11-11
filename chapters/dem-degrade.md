# 화학-기계 열화와 계면

전극 미세구조 · 공정 · 장 `dem-degrade` · 논문 31편 · 읽기 카드 31편

> 균열, 박리, 응력에 따른 계면 저항 변화.

## 장 서문 — 복합양극 열화는 입계 균열과 계면 분해가 함께 만든다

*읽기 카드 31편을 엮어 쓴 글 · 항목 30개 중 30개 검증 통과 · 2026-11-10*

이 장의 질문은 황화물 전고체 복합양극에서 균열, 박리, 계면 분해가 저항과 용량을 어떻게 깎는가이다. 리뷰들은 분해와 기계 불안정이 서로를 키우는 되먹임으로 이를 정리한다. [근거: Gandla et al. 2026 (`gandla2026_layered_cathode_degradation_diagnostics_review`); Kang et al. 2026 (`kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review`); Li et al. 2026 (`li2026_electrochemomechanical_coupling_asslmb_review`)]

실험들은 다결정 입자의 입계 균열과 양극 계면의 화학 분해를 각각 관찰했다. 그러나 한 셀에서 임피던스 성장을 기계 몫과 화학 몫으로 나눈 연구는 아직 없다. [근거: Parks et al. 2023 (`intergranular_cracking_nmc811_jmca2023`); Yun et al. 2023 (`yun2023_deciphering_degradation_halide_vs_sulfide`); Wang et al. 2026 (`wang2026_dryprocess_thick_cathode_failure_ncm94`); Gandla et al. 2026 (`gandla2026_layered_cathode_degradation_diagnostics_review`)]

모델은 박리와 균열이 시작되는 부피변화 임계와 압력 효과의 방향을 준다. 다만 대부분 2D, 단일 실현, 실험 미검증이어서 추세 수준에서만 쓸 수 있다. [근거: Bucci et al. 2017 (`bucci2017_chemomech_failure_assb_cycling_czm`); Bucci et al. 2018 (`bucci2018_mechanical_instability_interface_delamination`); So, Inoue, Hirate, Nunoshita, Ishikawa, Tsuge 2021 (`so2021_dem_fabrication_degradation_ductile_particles`); Alabdali et al. (`dem_mechanical_stresses_ssb_electrode_cycling`)]

### 입자는 어디서 깨지나

다결정 Ni-rich 입자가 충전 중 입계를 따라 깨진다는 데 여러 측정이 모인다. Parks et al. 2023은 같은 NMC811 입자를 충전 전후 nano-CT로 찍어 부피가 평균 +19 % 늘었고 그 대부분이 입계 균열 공극이라고 적었다. Wheatcroft et al. 2023의 SEM 내 압축에서 원뿔팁 명목강도는 pristine 67 ± 21 MPa에서 4.3 V 충전 뒤 11 ± 4 MPa로 떨어졌다. Sedlatschek et al. 2026은 2차입자 속 입계를 미세인장으로 당겨 특성강도 745 MPa의 취성 파괴를 보고했다. [근거: Parks et al. 2023 (`intergranular_cracking_nmc811_jmca2023`); Wheatcroft et al. 2023 (`wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem`); Sedlatschek et al. 2026 (`sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile`)]

입계를 없애거나 큰 입자를 보호하면 균열이 줄어든다. Jung et al. 2023은 ASSB에서 단결정 NCM의 150 사이클 유지율이 84.9 %로 다결정의 65.6 %보다 높고 균열도 적다고 보고했다. Kang et al. 2025는 bimodal NCA에서 큰 입자에 입계 균열이 생기고 LZO 코팅이 이를 막는다고 적었다. Lee et al. 2026은 분리막 쪽 큰 다결정 입자에 균열이 몰리고 소형 단결정 상층이 이를 줄인다고 보였다. Parks et al. 2023, Wheatcroft et al. 2023, Lee et al. 2026은 액체 전해질 셀 결과라 고체전지에는 방향만 옮길 수 있다. [근거: Jung et al. 2023 (`jung2023_single_crystal_ncm_morphology`); Kang et al. 2025 (`kang2025_toughened_bimodal_nca_lzo`); Lee et al. 2026 (`lee2026_microcrack_tolerant_bilayer_cathode_chemomech_fastcharging`); Parks et al. 2023 (`intergranular_cracking_nmc811_jmca2023`); Wheatcroft et al. 2023 (`wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem`)]

### 화학이냐 기계냐

LPSCl 양극의 임피던스 분해에서 가장 크게 자란 성분은 대개 계면 저항이다. Yun et al. 2023에서 NCM-LPSCl의 계면 저항 R_int는 사이클 뒤 982.3 Ω·cm²까지 커졌고 이온수송 저항은 조금만 늘었다. Wang et al. 2026의 건식 후막에서도 R_ct2가 50 사이클 동안 939.7 Ω cm²까지 커졌고 분리막 벌크 저항은 거의 그대로였다. Jung et al. 2019는 전위 없이 SOC 0에 두기만 해도 베어 NCM의 입계 이온 저항이 389 Ω 늘고 LiNbO₃ 코팅 NCM은 21 Ω에 그친다고 보고했다. [근거: Yun et al. 2023 (`yun2023_deciphering_degradation_halide_vs_sulfide`); Wang et al. 2026 (`wang2026_dryprocess_thick_cathode_failure_ncm94`); Jung et al. 2019 (`jung2019_cathode_electrolyte_chemical_reaction_sulfide_assb`)]

균열과 분해의 인과 방향을 두고 해석이 갈린다. Kang et al. 2023은 Li-In 음극의 부피변화가 양극 안에 동적 접촉을 만들고, 그 결과 계면저항과 확산저항이 급등하며 NCA 입계 균열이 생긴다고 적었다. Kang et al. 2025는 계면 분해로 생긴 Li 불균일을 큰 입자 균열의 주범으로 보았다. Gandla et al. 2026은 균열이 이온 접촉을 좁은 수송 목으로 바꾸는 수송 사건으로서 용량 감소를 지배한다고 판정했다. Yun et al. 2023은 할라이드 LIC에서는 계면반응보다 가압 균열에 따른 이온수송 손실이 열화를 정한다고 보여, 지배 인자가 전해질 소재에 따라 갈린다. [근거: Kang et al. 2023 (`kim2023_chemomech_failure_highstrain_anode`); Kang et al. 2025 (`kang2025_toughened_bimodal_nca_lzo`); Kang et al. 2026 (`kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review`); Gandla et al. 2026 (`gandla2026_layered_cathode_degradation_diagnostics_review`); Yun et al. 2023 (`yun2023_deciphering_degradation_halide_vs_sulfide`)]

### 제조압과 작동압

압력은 제조 단계와 작동 단계에서 서로 다른 역할을 한다. So et al. 2021의 2D DEM은 제조압이 높을수록 Si 팽창에 따른 균열과 영구 전도도 감소가 작다고 예측했다. Alabdali et al.의 DEM은 등방 저압 압밀이 단축 375 MPa와 비슷한 전도도를 내면서 입자 응력을 6–16 MPa 사이로 낮춘다고 적었다. Kang et al. 2023과 Kang et al. 2025는 가압 응력이 GPa급 확산 유발 응력보다 훨씬 작아 사이클 중 균열 기여가 작다고 보았고, 검토 측은 이 진술을 사이클 중 균열에 한정한다. [근거: So, Inoue, Hirate, Nunoshita, Ishikawa, Tsuge 2021 (`so2021_dem_fabrication_degradation_ductile_particles`); Alabdali et al. (`dem_mechanical_stresses_ssb_electrode_cycling`); Kang et al. 2023 (`kim2023_chemomech_failure_highstrain_anode`); Kang et al. 2025 (`kang2025_toughened_bimodal_nca_lzo`)]

낮은 작동압은 Li 금속과 바인더의 문제를 바꾼다. Doux et al. 2020에서 LPSCl Li 대칭셀은 압력이 높을수록 Li가 펠릿 공극으로 creep해 빨리 단락했고, 5 MPa에서는 1000 h 넘게 단락이 없었다. Park et al. 2026은 0.3 MPa 작동에서 가교 SBR이 접착 강화형보다 용량과 수명을 크게 개선했고 고압에서는 차이가 작았다고 적었다. Jun et al. 2026의 전도성 바인더 이점도 저압에 한정되고 고압에서는 PVDF가 앞섰다. Gandla et al. 2026은 실용 적층압 ≤2 MPa에서 장기 검증된 코팅이 없다고 적었다. [근거: Doux et al. 2020 (`doux2020_stack_pressure_assb`); Park et al. 2026 (`park2026_thiolene_sbr_binder_assb`); Jun et al. 2026 (`jun2026_ppma_econductive_binder_si_lowpressure_assb`); Gandla et al. 2026 (`gandla2026_layered_cathode_degradation_diagnostics_review`)]

### 모델이 준 임계값

해석과 수치 모델은 박리와 균열의 임계를 수 % 부피변화에서 찾는다. Bucci et al. 2018은 대부분의 물성 조합에서 부피 ~7.5 % 변화면 계면 박리가 시작된다고 적었다. Bucci et al. 2017은 팽창 7.5 % 미만과 G_c 4 J/m² 이상을 함께 만족해야 SE 균열이 억제된다고 계산했다. 두 모델 모두 소재를 지정하지 않았고 검증이 없어 검토 측은 추세와 임계만 믿을 만하다고 본다. [근거: Bucci et al. 2018 (`bucci2018_mechanical_instability_interface_delamination`); Bucci et al. 2017 (`bucci2017_chemomech_failure_assb_cycling_czm`)]

SE 강성이 열화에 유리한지에서 모델끼리 엇갈린다. Bucci et al. 2017은 E_SE ~15 GPa의 compliant SE가 더 잘 깨진다고 보고 sulfide가 bulk형 전지에 유리하다는 추측을 반박했다. Bucci et al. 2018은 무른 SE가 박리 개시를 늦추지만 핵생성 뒤에는 전파를 불안정하게 만든다고 적었다. Li et al. 2026 총설이 인용한 Farzanian 모형은 E < 20 GPa 황화물이 양극 결함을 억제한다고 보아 방향이 다르다. Yun et al. 2023의 FEM은 강성보다 전해질의 소성 유무가 균열을 가른다고 보았다. [근거: Bucci et al. 2017 (`bucci2017_chemomech_failure_assb_cycling_czm`); Bucci et al. 2018 (`bucci2018_mechanical_instability_interface_delamination`); Li et al. 2026 (`li2026_electrochemomechanical_coupling_asslmb_review`); Yun et al. 2023 (`yun2023_deciphering_degradation_halide_vs_sulfide`)]

### 물성값의 측정 척도

같은 물질의 역학값이 측정 척도에 따라 크게 갈린다. Song et al. 2025는 다공 Li₆PS₅Cl mm 시편에서 E 4.7 ± 1.1 GPa를 얻어 나노압입 문헌값 28.0 GPa보다 크게 낮다고 적었다. Xu et al. 2017은 NMC532 이차입자의 계면 K_c를 0.102 ± 0.03 MPa·m^½로 재어 소결 펠릿의 약 3분의 1로 보고했다. Stallard et al. 2022는 압흔이 결정립보다 커지면 입계 파쇄로 E와 H가 떨어진다는 틀로 이런 차이를 정리했다. [근거: Song et al. 2025 (`song2025_porous_argyrodite_modulus_fracture_toughness`); Xu et al. 2017 (`xu2017_nmc532_nanoindentation_modulus_hardness_toughness`); Stallard et al. 2022 (`stallard2022_cathode_mechanical_properties_review`)]

파괴인성은 대부분 직접 잰 값이 아니다. Stallard et al. 2022의 다결정 NMC333 K_IC 0.05–0.3 MPa·m^½는 결함을 결정립 절반으로 가정해 강도에서 역산한 범위다. Wheatcroft et al. 2023은 K_IC를 재지 않았고, Sedlatschek et al. 2026의 입계 파괴에너지도 다른 논문의 인성을 빌려 유도한 값이다. Sedlatschek et al. 2026에서는 같은 입자의 인장 영률 165 ± 7 GPa와 나노압입 영률 138 GPa도 서로 달랐다. Li et al. 2026 총설의 물성 표는 다공 펠릿 벌크값과 치밀체 값을 부류 표시 없이 섞었다고 검토 측은 본다. [근거: Stallard et al. 2022 (`stallard2022_cathode_mechanical_properties_review`); Wheatcroft et al. 2023 (`wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem`); Sedlatschek et al. 2026 (`sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile`); Li et al. 2026 (`li2026_electrochemomechanical_coupling_asslmb_review`)]

### 이 장의 값

| 값 | 표기 | 근거 |
|---|---|---|
| 박리 개시 부피변화, 해석 모델 | ~7.5 % | Bucci et al. 2018 (`bucci2018_mechanical_instability_interface_delamination`) |
| NMC811 2차입자 부피팽창, 4.5 V 충전 | +19 % | Parks et al. 2023 (`intergranular_cracking_nmc811_jmca2023`) |
| NMC811 원뿔팁 명목강도, 4.3 V 충전 | 11 ± 4 MPa | Wheatcroft et al. 2023 (`wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem`) |
| NMC811 입계 특성강도, 미세인장 | 745 MPa | Sedlatschek et al. 2026 (`sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile`) |
| 다공 Li₆PS₅Cl 벌크 영률, 굽힘 | 4.7 ± 1.1 GPa | Song et al. 2025 (`song2025_porous_argyrodite_modulus_fracture_toughness`) |
| NCM-LPSCl 사이클 후 계면 저항 | 982.3 Ω·cm² | Yun et al. 2023 (`yun2023_deciphering_degradation_halide_vs_sulfide`) |
| 건식 후막 50 사이클 R_ct2 | 939.7 Ω cm² | Wang et al. 2026 (`wang2026_dryprocess_thick_cathode_failure_ncm94`) |
| LPSCl Li 대칭셀 무단락, 5 MPa | >1000 h | Doux et al. 2020 (`doux2020_stack_pressure_assb`) |

### 아직 열린 문제

- 임피던스 성장과 용량 손실에서 균열과 접촉 손실의 몫, 계면 분해의 몫이 각각 얼마인지는 한 셀 안에서 나눠 잰 연구가 없다. 계면 저항 우세 결과와 균열이 수송을 지배한다는 판정이 함께 서 있다. [근거: Gandla et al. 2026 (`gandla2026_layered_cathode_degradation_diagnostics_review`); Yun et al. 2023 (`yun2023_deciphering_degradation_halide_vs_sulfide`); Wang et al. 2026 (`wang2026_dryprocess_thick_cathode_failure_ncm94`)]
- compliant 황화물 SE가 균열과 박리를 억제하는지 키우는지는 모델마다 답이 다르다. 강성 대신 소성을 기준으로 보는 FEM도 있어 기준 물리량부터 정해지지 않았다. [근거: Bucci et al. 2017 (`bucci2017_chemomech_failure_assb_cycling_czm`); Bucci et al. 2018 (`bucci2018_mechanical_instability_interface_delamination`); Li et al. 2026 (`li2026_electrochemomechanical_coupling_asslmb_review`); Yun et al. 2023 (`yun2023_deciphering_degradation_halide_vs_sulfide`)]
- 입자 간 접촉망이 장기 사이클에서 유지되는지는 열려 있다. Wang et al. 2026의 접촉 피크 안정은 한 사이클 안의 관측이고, 검토 측은 압력의 비가역 손실이 SEM에 보이지 않는 접촉손실을 가리킨다고 본다. 다른 연구들은 사이클 뒤 공극과 접촉 손실 부피가 늘었다고 보고했다. [근거: Wang et al. 2026 (`wang2026_dryprocess_thick_cathode_failure_ncm94`); Gandla et al. 2026 (`gandla2026_layered_cathode_degradation_diagnostics_review`); Li et al. 2026 (`li2026_electrochemomechanical_coupling_asslmb_review`)]
- 입계 균열과 강도 저하의 정량값 다수는 액체 전해질 셀에서 왔고, 고체전지 압밀 조건에서 같은 크기로 일어나는지는 확인되지 않았다. 단결정 입자의 직접 관찰 비교도 Parks et al. 2023에는 없다. [근거: Parks et al. 2023 (`intergranular_cracking_nmc811_jmca2023`); Wheatcroft et al. 2023 (`wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem`); Lee et al. 2026 (`lee2026_microcrack_tolerant_bilayer_cathode_chemomech_fastcharging`); Xu et al. 2017 (`xu2017_nmc532_nanoindentation_modulus_hardness_toughness`)]

### 먼저 읽을 논문

1. Gandla et al. 2026 (`gandla2026_layered_cathode_degradation_diagnostics_review`) — 진단 신호, 기전, 완화책을 열화 연쇄로 묶고 실용 조건의 공백을 정리해 장 전체의 지도 역할을 한다.
2. Bucci et al. 2018 (`bucci2018_mechanical_instability_interface_delamination`) — 부피변화에 따른 계면 박리 임계를 닫힌형 식으로 주어 이후 모델과 실험을 읽는 기준선이 된다.
3. Yun et al. 2023 (`yun2023_deciphering_degradation_halide_vs_sulfide`) — 같은 양극 설계에서 황화물은 계면반응, 할라이드는 가압 균열로 열화가 갈리는 것을 임피던스 분해로 보여 준다.
4. Parks et al. 2023 (`intergranular_cracking_nmc811_jmca2023`) — 같은 NMC811 입자를 충전 전후로 찍어 입계 균열이 전기화학으로 생기는 것을 직접 보인다.
5. Song et al. 2025 (`song2025_porous_argyrodite_modulus_fracture_toughness`) — 다공 Li₆PS₅Cl의 벌크 영률과 파괴인성을 같은 시편에서 재어 나노압입값과 척도 차이를 드러낸다.

## 이 장의 논문 (31편)

| digest | 저자 · 연도 | 제목 | 한 줄 결론 |
|---|---|---|---|
| `dem_mechanical_stresses_ssb_electrode_cycling` | Alabdali et al. | Understanding mechanical stresses upon solid-state battery electrode cycling using discrete element method | 황화물 복합양극에서 등방 1–5 MPa 압밀은 단축 375 MPa와 비슷한 전도도를 내면서 입자 응력을 크게 낮추고, 사이클 중 응력은 AM과 SE 사이를 오간다. |
| `bucci2017_chemomech_failure_assb_cycling_czm` | Bucci et al. 2017 | Modeling of internal mechanical failure of all-solid-state batteries during electrochemical cycling, and implications for battery design | 전극입자 팽창이 7.5 % 미만이고 SE 파괴에너지가 4 J/m² 이상이면 사이클 균열이 억제되며, compliant SE는 오히려 더 잘 깨진다. |
| `xu2017_nmc532_nanoindentation_modulus_hardness_toughness` | Xu et al. 2017 | Mechanical and Structural Degradation of LiNixMnyCozO₂Cathode in Li-Ion Batteries: An Experimental Study | NMC532 이차입자의 E, H, 계면 K_c는 소결 펠릿보다 낮고, 탈리튬화와 사이클을 거치며 함께 떨어진다. |
| `bucci2018_mechanical_instability_interface_delamination` | Bucci et al. 2018 | Mechanical instability of electrode-electrolyte interfaces in solid-state batteries | 대부분의 물성 조합에서 부피 ~7.5 % 변화면 계면 박리가 시작되고, 무른 SE와 큰 계면에너지만 25 %까지 견딘다. |
| `jung2019_cathode_electrolyte_chemical_reaction_sulfide_assb` | Jung et al. 2019 | Understanding the effects of chemical reactions at the cathode–electrolyte interface in sulfide based all-solid-state batteries | 전위 없이 SOC 0에서 두기만 해도 베어 NCM과 argyrodite 계면에 반응 산물과 균열이 생겨 입계 이온 저항이 크게 늘고, LiNbO₃ 코팅이 이를 억제한다. |
| `doux2020_stack_pressure_assb` | Doux et al. 2020 | Stack Pressure Considerations for Room‐Temperature All‐Solid‐State Lithium Metal Batteries | LPSCl Li-metal 셀은 stack pressure가 높을수록 Li가 SE 공극으로 creep해 빨리 단락되고, 5 MPa에서는 1000 h 넘게 안정했다. |
| `so2021_dem_fabrication_degradation_ductile_particles` | So, Inoue, Hirate, Nunoshita, Ishikawa, Tsuge 2021 | Simulation of Fabrication and Degradation of All-Solid-State Batteries with Ductile Particles | 연성 입자 DEM으로 보면 사이클 중 SE 전도도 손실은 균열이 키운 굴곡도가 지배하고, 높은 제조압이 그 손실을 줄인다. |
| `stallard2022_cathode_mechanical_properties_review` | Stallard et al. 2022 | Mechanical properties of cathode materials for lithium-ion batteries | 양극재 E·H는 압흔/결정립 비가 0.1을 넘으면 입계 파쇄로 떨어지고, 강도 자료로 본 다결정 NMC333의 K_IC는 0.05–0.3 MPa·m^½로 추정된다. |
| `intergranular_cracking_nmc811_jmca2023` | Parks et al. 2023 | Direct observations of electrochemically induced intergranular cracking in polycrystalline NMC811 particles | 4.5 V 충전 전후 같은 NMC811 입자를 비교하자 입계 균열이 생겼고 입자 부피 증가는 대부분 균열 공극 때문이었다 |
| `jung2023_single_crystal_ncm_morphology` | Jung et al. 2023 | Customizing the morphology and microstructure of single-crystalline Ni-rich layered cathode materials for all-solid-state batteries | 단결정 NCM은 입계와 내부 공극이 없어 ASSB에서 고율 용량과 사이클 수명이 다결정보다 높고 균열도 억제된다. |
| `kim2023_chemomech_failure_highstrain_anode` | Kang et al. 2023 | Chemo-mechanical failure of solid composite cathodes accelerated by high-strain anodes in all-solid-state batteries | Li-In 음극의 부피변화가 양극 안에 동적 접촉과 계면 불균일을 만들고, 그 결과 NCA 입계 균열과 용량 급락이 일어난다. |
| `spencerjolly2023_ag_graphite_interlayer_operando_xrd` | Spencer-Jolly et al. 2023 | Structural changes in the silver-carbon composite anode interlayer of solid-state batteries | Li는 흑연에 먼저 들어간 뒤 Ag와 화학적으로 합금되며, Ag는 CCD를 올리지 않고 집전체 쪽 석출층을 균일하게 만든다. |
| `tron2023_lpscl_ccd_ambient_pressure` | Tron et al. 2023 | Critical Current Density Measurements of Argyrodite Li₆PS₅Cl Solid Electrolyte at Ambient Pressure | 스택압 0.20–0.28 MPa의 상용 셀에서 Li₆PS₅Cl의 CCD는 낮고, 셀 지그와 Li 표면이 그 값을 크게 흔든다. |
| `wheatcroft2023_nmc811_secondary_particle_fracture_insitu_sem` | Wheatcroft et al. 2023 | Fracture Testing of Lithium‐Ion Battery Cathode Secondary Particles in‐situ inside the Scanning Electron Microscope | 다결정 NMC811 2차입자는 입계를 따라 쪼개지고, 접촉이 날카로울수록, 사이클과 충전이 진행될수록 낮은 하중에서 깨진다. |
| `yun2023_deciphering_degradation_halide_vs_sulfide` | Yun et al. 2023 | Deciphering the critical degradation factors of solid composite electrodes with halide electrolytes: Interfacial reaction versus ionic transport | 황화물 LPSCl 양극은 계면 interphase 때문에, 할라이드 LIC 양극은 가압 균열로 인한 이온수송 손실 때문에 열화한다. |
| `zhang2023_pfib_multiscale_imaging_4d_thick_cathode` | Zhang et al. 2023 | Coupling of multiscale imaging analysis and computational modeling for understanding thick cathode degradation mechanisms | NMC811 후막에서 분리막 쪽 CEI가 두꺼워 두께방향 리튬화가 불균일해지고, 이것이 균열과 NMC와 CBD 사이 접촉 손실로 이어진다. |
| `jeong2025_tough_adhesive_binder_shield_ncm811` | Jeong et al. 2025 | A Tough, Adhesive, and Protective Binder Shield for Stabilizing High‐Nickel Cathodes in Lithium‐Ion Batteries | PVDF에 PAA를 붙이고 PEI로 가교한 바인더만 접착과 인성이 함께 올라 PVDF보다 오래 버텼다. |
| `kang2025_toughened_bimodal_nca_lzo` | Kang et al. 2025 | Toughened Bimodal Cathodes for All-Solid-State Batteries via Controlled Interfacial Heterogeneity | bimodal NCA는 패킹 이득을 주지만 큰 입자의 입계 균열로 수명이 줄고, LZO 코팅이 그 균열을 막는다. |
| `liao2025_interfacial_adhesion_li_plating_carbon_interlayer` | Liao et al. 2025 | Effects of Interfacial Adhesion on Lithium Plating Location in Solid‐State Batteries with Carbon Interlayers | 탄소 인터레이어와 LPSCl 계면의 인성이 ≈10 J m⁻²를 넘으면 Li가 집전체 쪽에만 석출된다 |
| `song2025_porous_argyrodite_modulus_fracture_toughness` | Song et al. 2025 | Investigation of the Mechanical Properties of Porous Argyrodite Sulfide Electrolytes for All-Solid-State Batteries | mm 시편 굽힘과 CT 시험으로 잰 다공 Li₆PS₅Cl의 E는 4.7 ± 1.1 GPa, K_Ic는 0.17 ± 0.03 MPa·m^½로 나노압입값보다 훨씬 낮다. |
| `gandla2026_layered_cathode_degradation_diagnostics_review` | Gandla et al. 2026 | Decoding Multiscale Degradation of Layered Cathodes in All‐Solid‐State Lithium Batteries: An Advanced Diagnostics‐Driven Framework | 층상 양극 고체전지의 용량 감소는 균열이 만든 접촉 손실이 지배하며, 실용 압력과 하중에서 검증된 완화책은 아직 없다. |
| `hamann2026_llzo_bilayer_porosity_asr_dendrite_ccd` | Hamann et al. 2026 | Effects of LLZO Microstructure Porosity, LLZO/Li‐Metal Interfacial Polarization Resistance, and Applied Areal Current Density on Li‐Metal Dendrite Formation in LLZO Bilayer Symmetric Cells | 다공 계면은 계면 과전압을 낮춰 CCD를 올리지만, 이중층 경계의 국소 이온전류 증폭은 내부 덴드라이트 위험을 키운다. |
| `hong2026_sulfide_cathode_binder_digitaltwin` | Hong et al. 2026 | Unveiling degradation mechanisms of sulfide-based composite cathodes supported by digital-twin modeling: Dry binder versus wet binder | NBR은 활물질 계면을 넓게 덮어 Li⁺ 경로를 끊고 void와 LPSCl 분해를 키우며, PTFE는 좁게 모여 경로를 보존한다. |
| `jun2026_ppma_econductive_binder_si_lowpressure_assb` | Jun et al. 2026 | Electron-conductive binder for silicon negative electrode enabling low-pressure all-solid-state batteries | 저압 Si 음극은 탈리튬화 때 전자 연결망이 끊겨 열화하고, 전도성 바인더 PPMA가 이를 막는다 |
| `kang2026_intertwined_electrochemo_mechanical_sulfide_assb_review` | Kang et al. 2026 | Intertwined nature of electrochemical reactions and mechanical instability in sulfide-based all-solid-state batteries | 황화물 ASSB의 계면 안정성은 화학 passivation과 기계 보강을 함께 다룰 때 얻어진다고 정리한 리뷰다. |
| `lee2026_microcrack_tolerant_bilayer_cathode_chemomech_fastcharging` | Lee et al. 2026 | Model-informed design of microcrack-tolerant cathodes for fast-charging lithium-ion batteries | 3C 충전 응력과 균열은 분리막 쪽 큰 다결정 입자에 몰린다. 10 µm 소형 단결정 상층이 이를 낮춰 사이클 유지율을 높였다. |
| `li2026_electrochemomechanical_coupling_asslmb_review` | Li et al. 2026 | Electro-Chemo-Mechanical Coupling in All-Solid-State Lithium Metal Batteries: From Stress Generation to Failure Mitigation | 전고체 리튬금속전지의 응력 출처, 전기화학 영향, 파괴 양식, 측정법, 완화 전략을 축척별로 묶은 총설이다. |
| `park2026_thiolene_sbr_binder_assb` | Park et al. 2026 | Multi‐Faceted Binder Enhancement via Slurry‐Applicable Thiol‐Ene Click Chemistry for Low‐Pressure‐Operable All‐Solid‐State Batteries | 0.3 MPa 작동에서 thiol-ene로 가교한 SBR 바인더가 접착 강화형보다 용량과 수명을 크게 개선했다. |
| `sedlatschek2026_nmc811_grain_boundary_strength_micro_tensile` | Sedlatschek et al. 2026 | Characterization of the grain boundary strength of polycrystalline NMC811 using in situ micro tensile tests | 다결정 NMC811 2차입자 안에서 깎은 미세인장 시편으로 입계 강도와 인장 영률을 처음 쟀고, 파괴는 입계를 따른 취성이었다. |
| `tabakovic2026_mechanical_stress_eis_ica_drt_dfn` | Tabakovic 2026 | Impact of Mechanical Stress on Electrochemical Impedance Spectra and Incremental Capacity of the Lithium-Ion Battery | 응력 결합 DFN 시뮬레이션에서 정수압은 ICA 피크를 저전압 쪽으로 평행 이동시키고, EIS 변화의 부호를 SoC에 따라 바꾼다. |
| `wang2026_dryprocess_thick_cathode_failure_ncm94` | Wang et al. 2026 | Failure mechanisms of dry-processed thick cathodes in sulfide solid-state batteries: a mechanistic investigation | 건식 후막 양극의 열화는 입자 간 접촉이 아니라 양극 계면의 화학분해와 전하이동 저항 증가에서 온다. |

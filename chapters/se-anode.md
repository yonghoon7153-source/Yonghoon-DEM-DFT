# 음극 · 리튬 금속 계면

전해질 · 계면 · 장 `se-anode` · 논문 23편 · 읽기 카드 23편

> Li 금속과 전해질 사이의 계면층, 덴드라이트, 중간층 설계.

## 장 서문 — Li 계면 분해 산물은 모였으나 자기제한은 미결이다

*읽기 카드 23편을 엮어 쓴 글 · 항목 30개 중 28개 검증 통과 · 2026-11-10*

Li 금속과 황화물 전해질이 닿으면 Li₂S, Li₃P, LiCl이 생긴다는 데 계산과 실험이 대체로 모였다. [근거: Wang et al. 2022 (`wang2022_resistive_decomposing_interfaces_se_alkali_metal`); Chaney et al. 2024 (`chaney2024_two_step_sei_growth_argyrodite_li_metal`); Ji Seon Kim 2025 (`kim2026_li_argyrodite_sei_reactive_md`); Lai et al. 2025 (`lai2025_haml_li_metal_lpscl_interface_doping_seFO`); Luo et al. 2022 (`luo2022_cryotem_li_dendrite_sulfide_interphase`); Liu et al. 2023 (`liu2023_electron_redistribution_redox_resistible_mgf2`)]

남은 질문은 이 계면상이 스스로 멈추는지, 전자를 막는지, 조성과 중간층으로 어떻게 바꾸는지다. 반응 MD는 나노초까지 닿았지만 전자를 다루지 않아 자기제한을 판정하지 못했다. [근거: Chaney et al. 2024 (`chaney2024_two_step_sei_growth_argyrodite_li_metal`); Ji Seon Kim 2025 (`kim2026_li_argyrodite_sei_reactive_md`); Li et al. 2026 (`li2026_mci_vs_sei_na3ps4_na_mlip_md`); Yuan et al. 2026 (`yuan2026_percolating_li2s_interphase_efield_md`)]

도핑과 코팅 논문은 CCD와 셀 수명을 늘렸다. 검토 측은 그 기전을 받치는 계산을 대부분 약하다고 본다. [근거: Liu et al. 2023 (`liu2023_electron_redistribution_redox_resistible_mgf2`); Ke et al. 2025 (`ke2025_orbital_hybridization_mgclo`); Wang et al. 2025 (`wang2025_electronic_localization_yo_argyrodite`); Li et al. 2026 (`li2026_functionally_differentiated_interphase`)]

### 무엇으로 분해되나

Li 금속과 Li₆PS₅Cl 계열이 만나면 Li₂S, Li₃P, LiCl이 생긴다는 데 계산과 실험이 모인다. Wang et al. 2022(산물 계면)는 Li₂S가 5배 과량으로 생기므로 Li 침투 경로가 Li₂S의 낮은 전도도에 막힌다고 적었다. Chaney et al. 2024는 Li₆PS₅Cl 한 단위가 Li 여덟 개를 흡수해 세 산물이 된다고 적었고, Lai et al. 2025의 하이브리드 MD도 같은 세 산물을 냈다. 실험에서는 Luo et al. 2022가 단면 Raman ~372 cm⁻¹ 피크로 계면 Li₂S를 확인했다. Liu et al. 2023은 XPS로 Li₂S와 Li₃P 신호를 보였다. [근거: Wang et al. 2022 (`wang2022_resistive_decomposing_interfaces_se_alkali_metal`); Chaney et al. 2024 (`chaney2024_two_step_sei_growth_argyrodite_li_metal`); Lai et al. 2025 (`lai2025_haml_li_metal_lpscl_interface_doping_seFO`); Luo et al. 2022 (`luo2022_cryotem_li_dendrite_sulfide_interphase`); Liu et al. 2023 (`liu2023_electron_redistribution_redox_resistible_mgf2`)]

산물이 어떤 구조로 모이는지는 논문마다 다르게 그린다. Chaney et al. 2024는 결정 산물이 5Li₂S·Li₃P·LiCl 단일 고용체라고 적었지만, 검토 측은 이것이 실험 증거가 아니며 원전도 Golov & Carrasco 2023이라고 본다. Kim 2025는 Li₂S 결정만 자라고 Li₃P·LiCl 모티프는 작은 클러스터로 남는다고 보고했다. Yuan et al. 2026도 Li₂S-like S만 연결망을 이룬다고 적었으나, 이 분류는 거리로 고른 것이라 결정 Li₂S로 읽을 수 없다. Luo et al. 2022는 25 °C에서 약 12 nm의 단결정 Li₂S 층을 보였고, Kim 2025는 대형 모델의 ~11 nm를 이 값과 견주었지만 검토 측은 자릿수 일치까지만 인정한다. [근거: Chaney et al. 2024 (`chaney2024_two_step_sei_growth_argyrodite_li_metal`); Ji Seon Kim 2025 (`kim2026_li_argyrodite_sei_reactive_md`); Yuan et al. 2026 (`yuan2026_percolating_li2s_interphase_efield_md`); Luo et al. 2022 (`luo2022_cryotem_li_dendrite_sulfide_interphase`)]

### 계면상은 멈추는가

반응 MD가 보인 성장 정지는 모두 전자 없이 얻은 것이라 자기 부동태화의 증거로 서지 못한다. Kim 2025는 Li₂S 결정이 핵생성할 때 PS₄ 분해가 멈췄다고 적었지만, 검토 측은 이를 동시성일 뿐 인과가 아니라고 보고 유한 셀 고갈 가능성도 남긴다. Chaney et al. 2024에서는 큰 계의 모든 런이 완전 환원까지 갔고, 검토 측은 자기제한 SEI가 보여지지 않았다고 본다. Lai et al. 2025의 포화도 검토 측은 부동태화가 아니라 연료 소진으로 읽는다. Yuan et al. 2026의 검토 측은 전자가 없는 닫힌 계라서 장을 뒤집어도 산물이 남는 것은 발견보다 귀결에 가깝다고 본다. [근거: Ji Seon Kim 2025 (`kim2026_li_argyrodite_sei_reactive_md`); Chaney et al. 2024 (`chaney2024_two_step_sei_growth_argyrodite_li_metal`); Lai et al. 2025 (`lai2025_haml_li_metal_lpscl_interface_doping_seFO`); Yuan et al. 2026 (`yuan2026_percolating_li2s_interphase_efield_md`)]

성장의 시간 법칙도 계산마다 다르고 대부분 적합으로 검정되지 않았다. Yuan et al. 2026은 장 없이 √t 성장을 적합해 계수 0.99 Å ps^−½를 얻었고, 장을 걸자 6.77 Å ps^−½로 커졌다. Chaney et al. 2024는 환원량이 log(t)를 따른다고 적었지만, 검토 측은 결정화 곡선에 적합선과 검정이 없다고 본다. Li et al. 2026(Na₃PS₄‖Na)의 계면상은 log 모양으로 느려지되 멈추지 않았으나, log는 적합 없는 서술어이고 Li 대조군은 선행 연구에서 가져왔다. 실험에서는 Luo et al. 2022가 25 °C 개회로 R_SEI의 위로 볼록한 증가를 부동태화 서명으로 읽고, 60 °C의 S자 증가는 반응율속에서 확산율속으로 바뀐 것으로 읽었다. [근거: Yuan et al. 2026 (`yuan2026_percolating_li2s_interphase_efield_md`); Chaney et al. 2024 (`chaney2024_two_step_sei_growth_argyrodite_li_metal`); Li et al. 2026 (`li2026_mci_vs_sei_na3ps4_na_mlip_md`); Luo et al. 2022 (`luo2022_cryotem_li_dendrite_sulfide_interphase`)]

### 보호 성분의 수치

Li₃P와 Li₃N이 전자를 새게 하는지가 보호층 해석을 가른다. Lomeli et al. 2024의 스크린에서 Li₃P와 Li₃N은 밴드갭 필터로 빠졌다. 우리 PBE 계산의 Li₃P 갭은 0.7092 eV이고, 우리는 이를 Li₃P 형성을 안정한 SEI로 보는 Lai et al. 2025의 해석에 대한 반론으로 본다. Li et al. 2026(Na₃PS₄‖Na)은 Li₃P 밴드갭을 1991년 계산의 2.03 eV로 표에 넣었다. Li et al. 2026(복합 계면상)이 빠른 수송 성분으로 고른 Li₃N은 원문 그림에서 다섯 코팅 중 갭이 가장 좁다고 검토 측은 보고, 설계가 작동한다면 LiF가 Li와 Li₃N 사이에 끼어 있기 때문이라고 본다. [근거: Lomeli et al. 2024 (`lomeli2024_predicting_reactivity_passivation_ssb_interfaces`); Lai et al. 2025 (`lai2025_haml_li_metal_lpscl_interface_doping_seFO`); Li et al. 2026 (`li2026_mci_vs_sei_na3ps4_na_mlip_md`); Li et al. 2026 (`li2026_functionally_differentiated_interphase`)]

Li⁺ 장벽으로 보호 성분을 고르는 계산은 같은 물질에서도 값이 크게 엇갈린다. LiCl은 Lu et al. 2025에서 0.05 eV, Li et al. 2026(복합 계면상)의 CI-NEB에서 0.4800 eV다. Li₃N은 Li et al. 2026(복합 계면상)에서 0.0103 eV, Kim et al. 2026(무음극)의 표면 adatom 두 점 구속이완에서 0.118 eV다. 검토 측은 0.0103 eV가 힘 수렴 한계 안에 있다고 보고, Lu et al. 2025의 LiCl 장벽은 결정상 계산이라 비정질 SEI를 담지 않는다고 본다. Kim et al. 2026(무음극)의 Li₃N과 LiC₆ 비교도 검토 측은 동일 프로토콜 비교가 아니라고 본다. [근거: Lu et al. 2025 (`lu2025_tailoring_cl_rich_anode_licl`); Li et al. 2026 (`li2026_functionally_differentiated_interphase`); Kim, Kang, Lee, Shin, An, Lee 2026 (`ahn2026_cej_agno3_pvp_li3n_anodefree`)]

### Cl과 도펀트 처방

Cl을 늘리면 Li와의 화학 안정성은 좋아지지만 덴드라이트 내성은 한 방향으로 따라오지 않는다. Zeng et al. 2022에서 CCD는 Cl-13의 1.038 ± 0.043 mA cm⁻²가 최대였고, σ가 가장 높은 Cl-16은 0.56 ± 0.028 mA cm⁻²로 최저였다. 원문의 LiCl 나노껍질 설명을 검토 측은 원문 자신의 Rietveld 정량과 맞지 않는다고 본다. Lu et al. 2025는 Cl15에서 4d 자리 Cl이 LiCl 층을 만들어 음극을 보호한다고 적었고, 검토 측은 이를 Cl 양이 아니라 4d 자리 점유를 조건으로 한 해석으로만 인용하라고 한다. Kang et al. 2026의 45 °C CCD에서는 Cl-rich LPSC₁.₆가 LPSC와 거의 같았고 LPSOC를 섞은 M-SE가 가장 높았다. [근거: Zeng et al. 2022 (`zeng2022_cl_rich_licl_nanoshell_li_interface`); Lu et al. 2025 (`lu2025_tailoring_cl_rich_anode_licl`); Kang et al. 2026 (`kang2026_site_specific_customized_se_dendrite_tolerant_li_metal`)]

Mg, Y, O 같은 도펀트는 셀 성능을 올렸지만 기전 계산은 검토 측이 대부분 받아들이지 않는다. Liu et al. 2023의 Mg·F 공도핑은 CCD를 0.6에서 1.4 mA cm⁻²로 올렸고, 이온전도도는 2.91에서 1.70 mS cm⁻¹로 낮췄다. Ke et al. 2025의 Mg(ClO₄)₂ 공도핑과 Wang et al. 2025의 Y/O 공치환도 CCD와 대칭셀 수명을 늘렸다. 검토 측은 Liu et al. 2023의 Mg@P 자리 배정, Ke et al. 2025의 PBE 갭, Wang et al. 2025의 BVSE 장벽과 전자전도도 수치를 근거가 약하다고 본다. Ke et al. 2025의 MgClO는 bulk 치환이 아니라 in-situ (de)lithiation으로 만든 계면상이라 bulk 치환 결과로 옮기기 어렵다. [근거: Liu et al. 2023 (`liu2023_electron_redistribution_redox_resistible_mgf2`); Ke et al. 2025 (`ke2025_orbital_hybridization_mgclo`); Wang et al. 2025 (`wang2025_electronic_localization_yo_argyrodite`)]

### 중간층과 강성 논리

h-BN 중간층 연구 두 편은 Li가 h-BN 위가 아니라 아래 틈에 쌓인다는 같은 결론을 다른 방법으로 냈다. Shi et al. 2017은 PBE-D2로 계면 틈 흡착 에너지 −2.0~−2.3 eV가 맨 h-BN의 −0.46/−0.56 eV보다 강하다고 계산했다. Liu et al. 2022는 h-BN–Li–Cu 샌드위치 −3.16 eV가 h-BN 표면 −0.33 eV보다 강하다는 서열과 EDS 단면, in-situ 광학 관찰로 샌드위치 증착을 보였다. Shi et al. 2017의 값은 고립 Li 원자 기준이고 Liu et al. 2022는 기준 상태와 vdW 보정을 밝히지 않아, 두 값은 절대값이 아니라 서열로 읽어야 한다. 우리는 Liu et al. 2022에 없는 Li 확산 장벽을 VGCF와 h-BN 샌드위치 모델로 계산할 계획이다. [근거: Shi et al. 2017 (`shi2017_hbn_interfacial_layer_li_anode`); Liu et al. 2022 (`liu2022_hbn_lithiophobic_sandwich_li_anode`)]

중간층 효과를 강성으로 설명하는 논리는 이 장에서 여러 번 흔들린다. Liu et al. 2022는 분말 h-BN 코팅의 탄성률 1.655 GPa가 Li metal의 4.9 GPa보다 낮아 원인을 기계강도가 아닌 수송과 핵생성에서 찾았다. Kang et al. 2026의 검토 측은 가장 단단한 LPSC₁.₆의 CCD가 LPSC와 같아, CCD를 가르는 변수가 강성이 아니라 LPSOC 유무라고 본다. Pustorino et al. 2025는 LPSC의 낮은 탄성률과 파괴에너지, 절연적인 PS₄ 종결 표면을 근거로 필라멘트가 균열을 뒤따르는 dry crack으로 자란다고 적었다. Wang et al. 2022(K*–E_hull)의 검토 측도 실패한 조성과 성공한 조성의 K*가 같아 데이터가 가르는 축은 E_hull 하나라고 본다. [근거: Liu et al. 2022 (`liu2022_hbn_lithiophobic_sandwich_li_anode`); Kang et al. 2026 (`kang2026_site_specific_customized_se_dendrite_tolerant_li_metal`); Pustorino et al. 2025 (`pustorino2025_lpscl_bulk_surface_mechanical_electronic_li_filament`); Wang et al. 2022 (`wang2022_two_parameter_space_dendrite_constriction`)]

### 이 장의 값

| 값 | 표기 | 근거 |
|---|---|---|
| 25 °C Li₂S 계면상 두께(cryo-TEM) | ∼12 nm | Luo et al. 2022 (`luo2022_cryotem_li_dendrite_sulfide_interphase`) |
| 대형 MTP 모델 interphase 두께 | ~11 nm | Ji Seon Kim 2025 (`kim2026_li_argyrodite_sei_reactive_md`) |
| 장 없는 계면상 성장 계수(425 K) | 0.99 Å ps^−½ | Yuan et al. 2026 (`yuan2026_percolating_li2s_interphase_efield_md`) |
| Cl-13 최대 CCD | 1.038 ± 0.043 mA cm⁻² | Zeng et al. 2022 (`zeng2022_cl_rich_licl_nanoshell_li_interface`) |
| LiCl Li⁺ 장벽(결정상 DFT) | 0.05 eV | Lu et al. 2025 (`lu2025_tailoring_cl_rich_anode_licl`) |
| LiCl Li⁺ 장벽(CI-NEB, VASP/PBE) | 0.4800 eV | Li et al. 2026 (`li2026_functionally_differentiated_interphase`) |

### 아직 열린 문제

- 계면상이 멈추는 원인이 전자 차단인지 원자 공급 고갈인지 아직 가려지지 않았다. 반응 MD는 모두 전자를 다루지 않았고, 우리는 자기제한 서술을 원자 수송 정지와 전자 차단 정지로 나눠 고치며 stepwise CV가 필요하다고 본다. [근거: Chaney et al. 2024 (`chaney2024_two_step_sei_growth_argyrodite_li_metal`); Ji Seon Kim 2025 (`kim2026_li_argyrodite_sei_reactive_md`); Lai et al. 2025 (`lai2025_haml_li_metal_lpscl_interface_doping_seFO`); Li et al. 2026 (`li2026_mci_vs_sei_na3ps4_na_mlip_md`); Yuan et al. 2026 (`yuan2026_percolating_li2s_interphase_efield_md`)]
- Cl 함량의 최적점이 논문마다 다르다. Zeng et al. 2022는 Cl-13에서, Lu et al. 2025는 4d 점유가 가장 높은 Cl15에서 음극 성능이 가장 좋았고, 검토 측은 같은 조성에서 moderate Cl이 낫다는 Gil-González와의 긴장을 짚는다. [근거: Zeng et al. 2022 (`zeng2022_cl_rich_licl_nanoshell_li_interface`); Lu et al. 2025 (`lu2025_tailoring_cl_rich_anode_licl`)]
- 실측 계면 저항을 계산이 설명하지 못한다. Burov et al. 2026은 Li|Ga-LLZO의 계산 R_ct가 실측 0.08 Ω cm²보다 훨씬 작은 하한이라 실측 저항이 접촉과 계면상에서 온다고 해석했다. 황화물 쪽에서 Wang et al. 2022(산물 계면)의 'resistive'는 면저항이 아니라 작은 D*만 뜻한다고 검토 측은 본다. Yuan et al. 2026의 초기 사이클 저항 결론도 저항 계산이 없는 외삽이라고 검토 측은 본다. [근거: Burov et al. 2026 (`burov2026_li_llzo_charge_transfer_mlmd`); Wang et al. 2022 (`wang2022_resistive_decomposing_interfaces_se_alkali_metal`); Yuan et al. 2026 (`yuan2026_percolating_li2s_interphase_efield_md`)]
- 보호층 장벽의 정의와 모델이 맞춰지지 않았다. Lai et al. 2020의 Li₂S 층 0.22 eV와 LiF 층 0.67 eV 대비는 얇은 자립 슬랩의 값이고, 최대점과 초기상태의 차로 재면 대비가 2.0배로 줄어든다고 검토 측은 본다. Kim et al. 2026(ICCF)의 LiF-rich SEI 전자 차단도 σ_e 실측 없는 간접 추론이라고 검토 측은 본다. [근거: Lai et al. 2020 (`lai2020_li2s_interfacial_layer_amorphous_sulfide_cse`); Kim et al. 2026 (`kim2026_iccf_molten_salt_sei_lpscl_sheet`)]

### 먼저 읽을 논문

1. Wang et al. 2022 (`wang2022_resistive_decomposing_interfaces_se_alkali_metal`) — 분해 산물별로 접합과 Li 수송을 나눠 본 틀이라 뒤 논문들의 산물 해석을 읽는 기준이 된다.
2. Chaney et al. 2024 (`chaney2024_two_step_sei_growth_argyrodite_li_metal`) — 비정질을 거쳐 결정화하는 2단계 기구와 자기제한 주장이 어디서 무너지는지를 먼저 보여 준다.
3. Ji Seon Kim 2025 (`kim2026_li_argyrodite_sei_reactive_md`) — 같은 기구를 더 큰 계와 실험 두께 비교, S 중간층 제어로 넓힌 반응 MD다.
4. Luo et al. 2022 (`luo2022_cryotem_li_dendrite_sulfide_interphase`) — 계산들이 대조하는 Li₂S 계면상의 두께와 결정성 실험 앵커다.
5. Zeng et al. 2022 (`zeng2022_cl_rich_licl_nanoshell_li_interface`) — Cl 함량과 CCD가 엇갈리는 실험이라 조성과 도핑 처방 논문들을 읽는 출발점이 된다.

## 이 장의 논문 (23편)

| digest | 저자 · 연도 | 제목 | 한 줄 결론 |
|---|---|---|---|
| `shi2017_hbn_interfacial_layer_li_anode` | Shi et al. 2017 | First-Principles Investigations of the Working Mechanism of 2D h-BN as an Interfacial Layer for the Anode of Lithium Metal Batteries | 두 층 h-BN의 전자 차단, 계면 틈의 강한 Li 흡착, 낮은 확산 장벽과 높은 강성이 함께 작용해 dendrite가 억제된다. |
| `lai2020_li2s_interfacial_layer_amorphous_sulfide_cse` | Lai et al. 2020 | Stabilizing a Lithium Metal Battery by an In Situ Li₂S-modified Interfacial Layer via Amorphous-Sulfide Composite Solid Electrolyte | PVDF–LiTFSI에 비정질 LPS를 넣으면 Li 표면에 Li₂S 계면층이 생겨 PVDF 분해가 억제되고 도금이 균일해진다. |
| `liu2022_hbn_lithiophobic_sandwich_li_anode` | Liu et al. 2022 | Uniform Lithium Deposition Induced by Double Lithiophobic Sandwich Structure for Stable Lithium Metal Anode | Li를 약하게 붙드는 h-BN 코팅이 Li를 h-BN과 Cu 사이로 몰아 평평한 샌드위치 증착을 만들고 셀 수명을 늘린다. |
| `luo2022_cryotem_li_dendrite_sulfide_interphase` | Luo et al. 2022 | Nanostructure of the Interphase Layer between a Single Li Dendrite and Sulfide Electrolyte in All-Solid-State Li Batteries | Li 덴드라이트 위 Li₂S 계면상은 25 °C에서 단결정, 60 °C에서 다결정이 되고 저항도 그에 따라 갈린다. |
| `wang2022_resistive_decomposing_interfaces_se_alkali_metal` | Wang et al. 2022 | The resistive nature of decomposing interfaces of solid electrolytes with alkali metal electrodes | 분해산물 가운데 Li₃P만 Li을 통과시키고, 다섯 배 많은 Li₂S와 LiCl이 막아 아르지로다이트‖Li 계면은 저항성이다. |
| `wang2022_two_parameter_space_dendrite_constriction` | Wang et al. 2022 | A Two-Parameter Space to Tune Solid Electrolytes for Lithium Dendrite Constriction | Li 금속 계면 분해를 K*와 E_hull로 놓고, K*는 낮게, E_hull은 0이 아닌 적당한 값으로 맞춰야 덴드라이트가 갇힌다고 주장한다. |
| `zeng2022_cl_rich_licl_nanoshell_li_interface` | Zeng et al. 2022 | Promoting favorable interfacial properties in lithium-based batteries using chlorine-rich sulfide inorganic solid-state electrolytes | Cl이 늘수록 σ와 Li에 대한 화학 안정성은 좋아진다. 덴드라이트 내성은 x = 1.3에서 가장 높고 x = 1.6에서 가장 낮다. |
| `liu2023_electron_redistribution_redox_resistible_mgf2` | Liu et al. 2023 | Electron Redistribution Enables Redox‐Resistible Li₆PS₅Cl towards High‐Performance All‐Solid‐State Lithium Batteries | Mg를 P 자리에, F를 Cl 자리에 넣은 Li₆PS₅Cl은 Li 금속에 대한 분해가 줄어 CCD와 대칭셀 수명이 크게 는다. |
| `chaney2024_two_step_sei_growth_argyrodite_li_metal` | Chaney et al. 2024 | Two-Step Growth Mechanism of the Solid Electrolyte Interphase in Argyrodyte/Li-Metal Contacts | Li₆PS₅Cl은 Li 금속에 환원돼 먼저 비정질층이 되고, 뒤늦게 antifluorite 고용체로 결정화한다. |
| `lomeli2024_predicting_reactivity_passivation_ssb_interfaces` | Lomeli et al. 2024 | Predicting Reactivity and Passivation of Solid-State Battery Interfaces | AIMD 라벨로 학습한 로지스틱 회귀는 ΔE_rxn 단독 기준보다 많은 안정 후보를 고르지만, 홀드아웃 오분류율은 35.3 %다. |
| `ke2025_orbital_hybridization_mgclo` | Ke et al. 2025 | S-p and p-p orbital hybridization induced electronic structure reconfiguration toward manipulating redox behavior of Li-Argyrodite electrolyte for enhanced lithium-compatibility | Mg(ClO₄)₂ 2 wt% 공도핑이 궤도 혼성으로 Li/LPSC1.5 계면을 금속성에서 갭이 있는 상태로 바꿔 Li 호환성을 높인다. |
| `kim2026_li_argyrodite_sei_reactive_md` | Ji Seon Kim 2025 | Deciphering Li₂S-like SEI Formation Mechanism at Li/Argyrodite Anodic Interfaces via Large-Scale Machine-Learned Reactive Dynamics | MTP 반응 MD에서 PS₄ 분해로 생긴 S-rich 비정질층 안에 Li₂S 결정이 자라며 전해질 분해가 멈춘다. |
| `lai2025_haml_li_metal_lpscl_interface_doping_seFO` | Lai et al. 2025 | Machine-learning-accelerated mechanistic exploration of interface modification in lithium metal anode | γ 게이트 하이브리드로 Li\|Li₆PS₅Cl 계면을 1 ns까지 돌렸고, 방법과 비용은 단단하지만 도핑 가속 주장은 자기 SI와 어긋난다. |
| `lu2025_tailoring_cl_rich_anode_licl` | Lu et al. 2025 | Tailoring argyrodite electrolyte for enhanced interface compatibility with lithium anode | 4d 자리 Cl이 많은 Cl15는 스스로 분해해 전자 절연성 LiCl 계면층을 만들고 덴드라이트를 억제한다. |
| `pustorino2025_lpscl_bulk_surface_mechanical_electronic_li_filament` | Pustorino et al. 2025 | Mechanical and Electronic Properties of Bulk and Surface Li₆PS₅Cl Argyrodite: First-Principles Insights on Li-Filament Resistance | LPSC는 탄성률과 파괴에너지가 낮고 PS₄ 종결 표면이 벌크만큼 절연적이라, Li 필라멘트가 균열을 뒤따르는 dry crack으로 자란다. |
| `wang2025_electronic_localization_yo_argyrodite` | Wang et al. 2025 | Electronic Localization Enables Long‐Cycling Sulfides‐Based All‐Solid‐State Lithium Batteries | Li₆PS₅Cl에 Y/O를 5% 공치환하면 Li 금속 계면 분해가 줄어 수명이 늘지만, 전자 국재화 기전은 근거가 약하다. |
| `ahn2026_cej_agno3_pvp_li3n_anodefree` | Kim, Kang, Lee, Shin, An, Lee 2026 | Electrochemical precursor conversion for coupled control of Li nucleation and transport in anode-free all-solid-state batteries | PVP로 잘게 분산한 AgNO₃를 첫 충전에 전환하면 고른 Ag–Li 자리와 Li₃N 계면상이 함께 생겨 수명이 늘어난다. |
| `burov2026_li_llzo_charge_transfer_mlmd` | Burov et al. 2026 | Charge-transfer mechanisms at Li/Ga-doped Li 7 La 3 Zr 2 O 12 (LLZO) interfaces from machine learning assisted molecular dynamics | 계면 횡단만 센 MLMD에서 Li\|Ga-LLZO 전하이동 장벽은 167 ± 18 meV이고, R_ct는 실측보다 훨씬 작은 하한값으로 나왔다. |
| `kang2026_site_specific_customized_se_dendrite_tolerant_li_metal` | Kang et al. 2026 | Dendrite-tolerant fast-kinetics design for all-solid-state lithium-metal batteries via site-specific customized sulfide electrolytes | 양극, 분리막, Li 계면에 서로 다른 argyrodite를 배정하자 NCM811‖Li 풀셀이 1C 500 사이클을 단락 없이 돌았다. |
| `kim2026_iccf_molten_salt_sei_lpscl_sheet` | Kim et al. 2026 | Ion-conducting cavity filler enabling in-situ formation of SEI in sulfide-based solid electrolyte sheets for all-solid-state batteries | [EMIM][TFSI]에 LiTFSI와 FEC를 더한 충진재를 LPSCl 시트에 떨어뜨리면 전도도가 회복되고 음극에 LiF-rich SEI가 생긴다. |
| `li2026_functionally_differentiated_interphase` | Li et al. 2026 | Functionally differentiated composite interphase enables stable sulfide-based all-solid-state lithium metal batteries | LiF, LiCl/LiBr, Li₃N을 차례로 습식 코팅한 Li 금속은 CCD와 수명이 크게 늘었지만, 층 분화 자체는 증명되지 않았다. |
| `li2026_mci_vs_sei_na3ps4_na_mlip_md` | Li et al. 2026 | Distinguishing the mixed conduction interphase: a machine learning molecular dynamics study on the Na₃PS₄ /Na battery interface | MLIP-MD에서 Na₃PS₄‖Na 계면상은 감속하며 계속 자라고 세 표지가 MCI와 부합하지만, 전자 전도는 계산하지 않았다. |
| `yuan2026_percolating_li2s_interphase_efield_md` | Yuan et al. 2026 | Reversible Ion Transport Through an Irreversibly Percolating Li₂S Interphase at the Li/Li₆PS₅Cl Interface | Li/Li₆PS₅Cl 계면에 건 장을 뒤집으면 Li 흐름은 반전된다. 그러나 Li₂S-like 연결망과 사라진 아르지로다이트 배위는 돌아오지 않는다. |

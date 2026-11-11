# 인접 분야와 기초 이론

전해질 · 계면 · 장 `se-adjacent` · 논문 23편 · 읽기 카드 23편

> 표면 · 점착 이론, 전도성 고분자 바인더, 수계 전지 등 축 밖에서 참고하는 문헌.

## 장 서문 — 기하평균 규칙은 분산 성분에만 맞고 계산 점착값은 조건부다

*읽기 카드 23편을 엮어 쓴 글 · 항목 30개 중 30개 검증 통과 · 2026-11-10*

표면 에너지와 점착을 성분으로 나누는 고전 이론은 기하평균 결합 규칙이 분산 성분이나 LW 성분에만 맞는다는 데까지 정리되어 있다. 극성 몫을 어떻게 다루는지는 이론마다 다르다. [근거: Fowkes 1964 (`fowkes1964_attractive_forces_interfaces_dispersion`); Van Oss et al. 1988 (`vanoss1988_lifshitz_vdw_acid_base_interfacial`)]

계산 쪽에서는 같은 Ag(111) 위 그래핀도 분산 기술에 따라 결합 크기가 달라진다. 흑연 층간 점착의 실험 기준점은 자기수축으로 잰 비정합 벽개에너지 하나다. [근거: Giovannetti et al. 2008 (`giovannetti2008_doping_graphene_metal_contacts`); Maurer et al. 2015 (`maurer2015_mbd_adsorbates_metal_surfaces`); Wang et al. 2015 (`wang2015_graphite_cleavage_energy`)]

바인더와 수계 전지 문헌의 실험 성능은 일관된다. 검토 측은 그 결합에너지와 장벽 계산 상당수가 상태나 조건이 정해지지 않은 값이라고 본다. [근거: Han et al. 2025 (`han2025_icep_binder_ultrahigh_loading_ncm811`); Noh et al. 2026 (`noh2026_pedotpss_peg_swcnt_binder_ultrahigh_loading_lfp`); Li et al. 2026 (`li2026_li_kinetic_promoter_aqueous_mn_sulfur`); Wu et al. 2026 (`wu2026_dilute_electrolyte_zn_calendar_aging`); Zhu et al. 2026 (`zhu2026_zhs_precoverage_quasi_anode_free_zn`)]

### 기하평균은 어디까지

두 고전 이론은 기하평균 결합 규칙이 분산 성분에만 맞는다는 데서 같다. Fowkes 1964는 분산 성분 γ^d의 기하평균으로 계면 장력을 계산했다. 물–Hg 계면 장력 예측 424.8 ± 4.4는 실측 426–7과 맞았다. 총 γ에 기하평균을 쓰면 맞지 않는다는 점은 Van Oss et al. 1988이 보였다. 유기 액체와 물의 계면 장력은 예측이 10–17이었으나 실측은 1.7–51 mJ/m²였다. [근거: Fowkes 1964 (`fowkes1964_attractive_forces_interfaces_dispersion`); Van Oss et al. 1988 (`vanoss1988_lifshitz_vdw_acid_base_interfacial`)]

두 논문은 극성 상호작용을 다루는 방식에서 갈린다. Fowkes 1964는 측정값과 분산 예측의 차를 극성 초과 항으로 남겼고, 실리카–물의 초과는 368로 분산 항 94–118보다 컸다. Van Oss et al. 1988은 극성 몫을 전자 받개 γ⁺와 주개 γ⁻의 교차항으로 다루며, 그래서 계면 장력이 음수가 될 수 있다고 적었다. 원문은 산화물과 황화물을 단극성 전자 주개로 분류했지만, 검토 측은 이 분류가 측정값이 아닌 한 문장이라고 본다. 이에 따라 우리 이종기술 논지의 W_ij ≈ 2√(γ_i·γ_j)는 W₁₂ = 2√(γ₁^dγ₂^d) + I₁₂^p로 다시 써야 한다. [근거: Fowkes 1964 (`fowkes1964_attractive_forces_interfaces_dispersion`); Van Oss et al. 1988 (`vanoss1988_lifshitz_vdw_acid_base_interfacial`)]

### 분말 표면을 재는 법

분말의 표면 에너지 값은 재는 경로와 조건에 따라 흔들린다. Fowkes 1964의 분말 값은 탈기 분말의 증기 흡착 결과이고, 검토 측은 산화물 γ^d가 표마다 달라 ±25 % 이상 불확실하다고 본다. Mohammadi-Jam · Waters 2014는 IGC로 분말의 분산 성분과 산염기 성분을 쟀고, 5 % 덮임에서 석영의 γ_S^D는 Schultz법 52.76, Dorris–Gray법 52.61 mJ/m²로 두 계산법이 거의 같았다. 같은 리뷰는 γ^D가 덮임률에 강하게 의존한다고 적어, 덮임률 없는 단일 값은 비교할 수 없다. γ⁺와 γ⁻ 같은 특이 성분은 기준값을 가정한 상대 척도라 다른 기준의 문헌 값과 섞을 수 없다. [근거: Fowkes 1964 (`fowkes1964_attractive_forces_interfaces_dispersion`); Mohammadi-Jam · Waters 2014 (`mohammadijam2014_inverse_gas_chromatography_review`); Van Oss et al. 1988 (`vanoss1988_lifshitz_vdw_acid_base_interfacial`)]

청정 표면 DFT도 절대값보다 순위를 준다. Kim et al. 2012는 같은 48 원자 슬랩 GGA+U 규약에서 LiNiO₂의 표면 에너지가 모든 면에서 LiCoO₂보다 낮다고 적었고, (104)에서 3.019 대 7.008 eV nm⁻²였다. 검토 측은 모형 크기를 늘려도 값이 계속 내려가 절대값이 수렴하지 않았다고 본다. LPSCl은 물과 극성 양성자 용매와 반응하므로, 우리는 세 액체 접촉각 대신 IGC, AFM 콜로이드 탐침, Lifshitz–DFT 경로로 γ^LW, γ⁺, γ⁻를 구해야 한다. [근거: Kim et al. 2012 (`kim2012_lno_lco_surface_energy_morphology_dft`); Van Oss et al. 1988 (`vanoss1988_lifshitz_vdw_acid_base_interfacial`)]

### 분산 모델과 점착값

같은 Ag(111) 위 그래핀도 분산 기술에 따라 결합 크기가 달라진다. Giovannetti et al. 2008은 vdW 보정 없는 LSDA로 Ag를 약결합군에 넣었고, 결합에너지 0.043 eV / C 원자를 얻었다. Maurer et al. 2015는 같은 계에서 vdW^surf 위에 MBD를 얹자 결합이 72에서 45 meV/C로 줄었다고 보고했다. 그래핀/Ag(111)에는 실험값이 없어 두 계산을 가를 기준이 없다. 검토 측은 LSDA 값을 PBE+D3(BJ) 결과와 나란히 비교하지 말라고 본다. [근거: Giovannetti et al. 2008 (`giovannetti2008_doping_graphene_metal_contacts`); Maurer et al. 2015 (`maurer2015_mbd_adsorbates_metal_surfaces`)]

흑연 층간 점착에서는 Wang et al. 2015의 직접 측정이 실험 기준점이다. 자기수축으로 얻은 비정합 벽개에너지는 0.37 ± 0.01 J/m²이고, 이상 AB 값 0.39 ± 0.02 J/m²는 이론 σ₀를 더한 합성값이다. Maurer et al. 2015와 Wang et al. 2015에는 D3 계열 수치가 없어 PBE+D3(BJ)를 채점할 수 없다. 우리 환산으로 같은 셀에서 vdW^surf와 MBD만 바꿔도 0.16 J/m²가 움직이므로, 우리 W는 분산 모델 조건부로 적어야 한다. [근거: Wang et al. 2015 (`wang2015_graphite_cleavage_energy`); Maurer et al. 2015 (`maurer2015_mbd_adsorbates_metal_surfaces`)]

### 술폰산 고분자의 근거

술폰산을 고분자 골격에 묶는 발상은 Patil et al. 1987의 자기도핑에서 시작한다. 원문은 상대이온을 골격에 공유결합으로 미리 묶어 두는 해법을 제시했다. 자기도핑 상태의 캐스팅 필름은 10⁻² S/cm였고, 10 S/cm 수준은 외부 도판트를 넣어야 나왔다. 검토 측은 이 값이 preliminary이고 물을 머금은 필름의 값이라 자릿수 인용만 허용한다고 본다. 우리 계산이 SDCP 상에 쓰는 σ_e = 250 S/cm는 이 논문이 지지하지 않는다. [근거: Patil et al. 1987 (`patil1987_self_doped_conducting_polymers`)]

고로딩 성능은 액체 전해질 셀에서 일관되지만, 술폰산이 산화물 표면에 세게 붙는다는 DFT 근거는 엇갈린다. Han et al. 2025의 ICEP-8 양극은 62.4 mg cm⁻²까지 균열 없이 작동했고, Jung et al. 2026의 PAMPS-CNT 캐소드는 58.4 mg cm⁻²까지 균일하게 캐스팅됐다. Han et al. 2025는 AMPS 조각이 PVDF보다 NCM811 (001)에 강하게 붙는다고 적었지만, 검토 측은 AN 조각이 PVDF보다 약하게 붙어 조성으로 가중하면 결론이 뒤집힐 수 있다고 본다. Noh et al. 2026의 PSS 배향 −3.62 eV도 검토 측은 어느 상태의 값인지 정해지지 않았다고 본다. 그래서 우리는 이 결합에너지들과 절대값을 나란히 놓지 않고, 불소계 대조군보다 술폰산이 깊다는 부호 방향만 공유한다. [근거: Han et al. 2025 (`han2025_icep_binder_ultrahigh_loading_ncm811`); Jung et al. 2026 (`jung2026_pamps_cnt_crosstalk_high_loading_lmb`); Noh et al. 2026 (`noh2026_pedotpss_peg_swcnt_binder_ultrahigh_loading_lfp`)]

### 정적 계산의 쓰임새

수계와 액체 전지 논문들은 실험 결과를 정적 계산으로 설명하지만, 검토 측은 계산이 주장을 직접 받치지 못한다고 본다. Wu et al. 2026(Zn 수계 전해질)은 Zn²⁺ 1차 껍질 경로의 Volmer 장벽이 순수 물 1.207 eV보다 낮은 0.601 eV라고 보고했고, 이를 희석의 물리적 근거로 삼았다. 검토 측은 이 값이 단일 배열의 ΔE이고 암시적 용매가 1 M 차폐를 써서 농도를 바꾸는 효과를 계산이 본 적이 없다고 지적한다. Li et al. 2026은 Li⁺가 S–S를 약화시킨다고 해석했지만, 검토 측은 장벽 계산이 없고 벌크 NEB가 고율 용량과 긴장한다고 본다. Kim et al. 2026의 5 ps AIMD 무반응도 검토 측은 매우 낮은 장벽의 경로가 없다는 데까지만 말한다고 본다. [근거: Wu et al. 2026 (`wu2026_dilute_electrolyte_zn_calendar_aging`); Li et al. 2026 (`li2026_li_kinetic_promoter_aqueous_mn_sulfur`); Kim et al. 2026 (`kim2026_electrolyte_interfacial_reactivity_alloying_anode_pulverization`)]

관측량과 서술자는 정의와 규약을 붙여야 비교할 수 있다. Gan et al. 2026은 최적 ΔG*OOH에 두 규약을 섞어 썼고, 검토 측은 규약 없이 숫자만 옮기면 값이 통째로 어긋난다고 본다. Spencer et al. 2022가 모은 Sc₂O₃ 절연파괴장은 gap 기반 예측 11 MV/cm, ALD 막 실측 3.5 MV/cm로 갈렸다. Whitten 2023의 UPS VBM은 극표면의 수직 이온화 값이라, 검토 측은 bulk DFT VBM과 바로 같게 놓으면 안 된다고 본다. Mulks 2024의 EHI는 PBE에서 DSD-BLYP 대비 +41.2 % 달랐지만 네 범함수에서 부호가 같아 부호와 순위로만 읽힌다. [근거: Gan et al. 2026 (`gan2026_defective_carbon_orr_selectivity_review`); Spencer et al. 2022 (`spencer2022_review_tco_band_structure_oxides`); Whitten 2023 (`whitten2023_ups_practical_best_practices`); Mulks 2024 (`mulks2024_hard_soft_electrons_holes`)]

### 이 장의 값

| 값 | 표기 | 근거 |
|---|---|---|
| 물–Hg 계면 장력 예측(식 (1)) | 424.8 ± 4.4 | Fowkes 1964 (`fowkes1964_attractive_forces_interfaces_dispersion`) |
| 유기 액체–물 계면 장력 실측 | 1.7–51 mJ/m² | Van Oss et al. 1988 (`vanoss1988_lifshitz_vdw_acid_base_interfacial`) |
| 석영 γ_S^D, 5 % 덮임 IGC | 52.76 (Schultz) / 52.61 (Dorris–Gray) mJ/m² | Mohammadi-Jam · Waters 2014 (`mohammadijam2014_inverse_gas_chromatography_review`) |
| 흑연 비정합 벽개에너지(대기 중) | 0.37 ± 0.01 J/m² | Wang et al. 2015 (`wang2015_graphite_cleavage_energy`) |
| 그래핀/Ag(111) 결합, PBE+MBD | 45 meV per C atom at 3.23 Å | Maurer et al. 2015 (`maurer2015_mbd_adsorbates_metal_surfaces`) |
| 그래핀/Ag(111) 결합, LSDA | 0.043 eV / C 원자 | Giovannetti et al. 2008 (`giovannetti2008_doping_graphene_metal_contacts`) |
| 자기도핑 폴리티오펜 as-cast 전도도 | 10⁻² S/cm | Patil et al. 1987 (`patil1987_self_doped_conducting_polymers`) |
| Zn 1차 껍질 Volmer 장벽(정적 DFT) | 0.601 eV | Wu et al. 2026 (`wu2026_dilute_electrolyte_zn_calendar_aging`) |

### 아직 열린 문제

- 배터리 소재의 표면 에너지 성분은 어느 카드에도 측정값이 없다. Fowkes 1964에는 NCM이나 황화물 값이 없고, Mohammadi-Jam · Waters 2014에는 공기 민감 황화물이나 배터리 소재의 IGC 예가 없다. NCM과 LPSCl의 γ⁺가 0이라는 근거도 없다고 우리는 추정한다. [근거: Fowkes 1964 (`fowkes1964_attractive_forces_interfaces_dispersion`); Mohammadi-Jam · Waters 2014 (`mohammadijam2014_inverse_gas_chromatography_review`); Van Oss et al. 1988 (`vanoss1988_lifshitz_vdw_acid_base_interfacial`)]
- Ag–그래핀과 흑연 점착에서 어느 분산 기술이 맞는지는 정해지지 않았다. LSDA와 MBD@vdW^surf는 서로 다른 값을 주는데 그래핀/Ag(111)에는 실험이 없다. 두 계산 논문과 흑연 측정 논문 어디에도 D3 계열 값이 없다. [근거: Giovannetti et al. 2008 (`giovannetti2008_doping_graphene_metal_contacts`); Maurer et al. 2015 (`maurer2015_mbd_adsorbates_metal_surfaces`); Wang et al. 2015 (`wang2015_graphite_cleavage_energy`)]
- 술폰산기와 산화물 표면의 결합 세기를 정의된 상태에서 계산한 값은 아직 없다. 검토 측은 Han et al. 2025에 자기 배열과 상태 선택 규칙이 없고, Noh et al. 2026이 스핀과 hole 위치를 적지 않았다고 본다. [근거: Han et al. 2025 (`han2025_icep_binder_ultrahigh_loading_ncm811`); Noh et al. 2026 (`noh2026_pedotpss_peg_swcnt_binder_ultrahigh_loading_lfp`)]
- 수계 Zn 계면에서 기판별 부반응의 원인은 측정으로 닫히지 않았다. Zhu et al. 2026은 평판 Cu의 개선을 표면합금층 덕으로 돌렸지만, 검토 측은 Cu 쪽 XRD, Cu 2p 분석, Cu 표면 DFT가 모두 없다고 지적한다. Wu et al. 2026(Zn 수계 전해질)의 계산은 용매화 껍질 조성과 D₂O의 동위원소 효과를 다루지 않았다. [근거: Zhu et al. 2026 (`zhu2026_zhs_precoverage_quasi_anode_free_zn`); Wu et al. 2026 (`wu2026_dilute_electrolyte_zn_calendar_aging`)]

### 먼저 읽을 논문

1. Fowkes 1964 (`fowkes1964_attractive_forces_interfaces_dispersion`) — 기하평균 규칙이 분산 성분에만 해당한다는 원전이라 뒤의 점착 논의가 모두 여기서 출발한다.
2. Van Oss et al. 1988 (`vanoss1988_lifshitz_vdw_acid_base_interfacial`) — 극성 몫을 γ⁺와 γ⁻의 교차항으로 나누고 음의 계면 장력을 보여 Fowkes 틀과의 차이를 드러낸다.
3. Wang et al. 2015 (`wang2015_graphite_cleavage_energy`) — 흑연 층간 점착의 유일한 직접 측정이라 계산값을 맞춰 볼 실험 기준점이다.
4. Maurer et al. 2015 (`maurer2015_mbd_adsorbates_metal_surfaces`) — 같은 Ag–그래핀 셀에서 분산 모델만 바꿔도 결합이 크게 움직인다는 점을 보인다.
5. Patil et al. 1987 (`patil1987_self_doped_conducting_polymers`) — 술폰산계 바인더 문헌이 기대는 자기도핑 개념의 원전이며 전도도 값의 한계도 함께 보여 준다.

## 이 장의 논문 (23편)

| digest | 저자 · 연도 | 제목 | 한 줄 결론 |
|---|---|---|---|
| `fowkes1964_attractive_forces_interfaces_dispersion` | Fowkes 1964 | ATTRACTIVE FORCES AT INTERFACES | 계면을 건너는 인력이 분산력뿐이면 γ₁₂ = γ₁ + γ₂ − 2√(γ₁^dγ₂^d)이고, 극성 상호작용은 따로 초과 항으로 남는다. |
| `patil1987_self_doped_conducting_polymers` | Patil et al. 1987 | Self-doped conducting polymers | 알킬술폰산염 곁사슬 폴리티오펜으로 자기도핑 개념과 수용성 전도성 고분자를 처음 제시했지만, 전도도는 예비값에 그친다. |
| `vanoss1988_lifshitz_vdw_acid_base_interfacial` | Van Oss et al. 1988 | Interfacial Lifshitz-van der Waals and polar interactions in macroscopic systems | 표면 장력을 LW 성분과 산·염기 성분으로 나누면 극성 상호작용은 교차항을 따르고, 계면 장력은 음수가 될 수도 있다. |
| `giovannetti2008_doping_graphene_metal_contacts` | Giovannetti et al. 2008 | Doping Graphene with Metal Contacts | 약하게 붙는 금속도 그래핀을 도핑하며, 교환 반발 전위계단 때문에 n/p 교차가 W_M ≈ 5.4 eV로 밀린다. |
| `kim2012_lno_lco_surface_energy_morphology_dft` | Kim et al. 2012 | First-principles and experimental investigation of the morphology of layer-structured LiNiO2 and LiCoO2 | 같은 48 원자 슬랩 GGA+U 계산에서 LiNiO₂의 표면 에너지는 모든 면에서 LiCoO₂보다 낮고, 원문은 이를 작은 1차입자의 원인으로 제안한다. |
| `liu2013_cage_methane_adsorption_hydrate_nucleation` | Liu et al. 2013 | Effects of cage type and adsorption face on the cage–methane adsorption interaction: Implications for hydrate nucleation studies | 물 cage의 면이 클수록 메탄 흡착이 세지고, 7각형 이상 면에서는 흡착 대신 통과가 일어난다. |
| `mohammadijam2014_inverse_gas_chromatography_review` | Mohammadi-Jam · Waters 2014 | Inverse gas chromatography applications: A review | IGC는 탐침 증기의 머무름으로 분말의 분산 성분과 산염기 성분을 재며, 값은 덮임률을 밝혀야 비교할 수 있다. |
| `maurer2015_mbd_adsorbates_metal_surfaces` | Maurer et al. 2015 | Many-body dispersion effects in the binding of adsorbates on metal surfaces | vdW^surf 위에 MBD를 얹으면 Ag(111) 위 세 흡착계의 결합이 약해지고 높이가 늘어, 실험이 있는 두 계에서 일치가 좋아진다. |
| `wang2015_graphite_cleavage_energy` | Wang et al. 2015 | Measurement of the cleavage energy of graphite | 자기수축 측정으로 흑연 비정합 벽개에너지 0.37 J/m²를 직접 얻었고, AB 값 0.39는 이론을 더한 합성값이다. |
| `spencer2022_review_tco_band_structure_oxides` | Spencer et al. 2022 | A review of band structure and material properties of transparent conducting and semiconducting oxides: Ga2O3, Al2O3, In2O3, ZnO, SnO2, CdO, NiO, CuO, and Sc2O3 | 아홉 가지 산화물의 물성을 문헌에서 모아 보니 bandgap과 절연파괴장은 측정 정의, 시료, 도핑에 따라 크게 갈렸다. |
| `whitten2023_ups_practical_best_practices` | Whitten 2023 | Ultraviolet photoelectron spectroscopy: Practical aspects and best practices | UPS 스펙트럼은 쉽게 얻지만, 의미 있게 얻으려면 표면 청정과 대전 제거, 시료 바이어스가 핵심이다. |
| `mulks2024_hard_soft_electrons_holes` | Mulks 2024 | Hard and soft electrons and holes | 같은 기하에서 전자 하나와 둘을 넣고 뺀 밀도의 2차 차분으로 분자의 hard 자리와 soft 자리를 부호 하나로 가린다. 다만 정량 예측자는 아니다. |
| `han2025_icep_binder_ultrahigh_loading_ncm811` | Han et al. 2025 | Ionically Conductive Elastic Polymer Binder for Ultrahigh Loading Electrode in High‐Energy‐Density Lithium Batteries | 세 기능을 한 트리블록에 담은 ICEP 바인더로 62.4 mg cm⁻² 양극이 균열 없이 돌고 파우치 377.6 Wh kg_cell⁻¹를 냈다. |
| `gan2026_defective_carbon_orr_selectivity_review` | Gan et al. 2026 | Unraveling the Catalytic Mechanisms of Defective Carbons for Selective 2e⁻/4e⁻ Oxygen Reduction: From Intrinsic Defects to Synergies with Heteroatoms and Single-Metal Atoms | ORR 경로는 결함 밀도나 도펀트 하나로 정해지지 않는다. 결함 정체, 기하, 배위가 만든 전자구조가 *OOH의 O–O 결합 보존 여부를 정한다. |
| `jung2026_pamps_cnt_crosstalk_high_loading_lmb` | Jung et al. 2026 | Enhanced Kinetics and Dual‐Interfacial Stability in High‐Areal‐Loading Electrodes for Lithium Metal Batteries via Crosstalk‐Active Polymer‐Functionalized Carbon Nanotubes | PAMPS 그래프팅 CNT는 고로딩 캐소드를 가능하게 하고, 분해된 술폰산이 애노드 SEI까지 바꿔 양쪽 계면을 안정화한다. |
| `kim2026_electrolyte_interfacial_reactivity_alloying_anode_pulverization` | Kim et al. 2026 | Electrolyte Interfacial Reactivity Regulates Alloying Anode Pulverization | 같은 NaPF₆ 염에서 EC/PC는 Bi 음극을 nm 크기로 미분화시켜 10 사이클 안에 무너뜨리고, TEGDME는 수명을 지킨다. |
| `li2026_li_kinetic_promoter_aqueous_mn_sulfur` | Li et al. 2026 | Activating Aqueous Multivalent Metal–Sulfur Electrochemistry via Kinetic Promoter | 1 m MnCl₂에 LiCl 20 m을 더하면 황 양극이 고율에서 큰 용량을 내지만, 장벽을 낮춘다는 DFT 근거는 간접적이다. |
| `noh2026_pedotpss_peg_swcnt_binder_ultrahigh_loading_lfp` | Noh et al. 2026 | Enabling ultra-high-loading LiFePO4 cathodes via a conductive binder architecture with minimized inactive content | PPP 바인더 하나로 비활성 함량을 4 wt%로 줄였고, SWCNT와 탄소 코팅 Al을 더해 1 wt%에서도 8 C 동작을 보였다. |
| `wu2026_dilute_electrolyte_zn_calendar_aging` | Wu et al. 2026 | Dilute electrolytes for suppressing metal anode corrosion during calendar aging and cycling in aqueous zinc batteries | Zn²⁺ 배위 물을 부식의 주범으로 보고 ZnSO₄를 0.1 M로 낮춘 뒤 첨가제로 보완해 보관 손실과 사이클 열화를 함께 줄였다. |
| `wu2026_tmd_intercalation_engineering_review` | Wu et al. 2026 | Recent progress in intercalation engineering of transition metal dichalcogenides for energy storage and conversion | 층상 TMD 삽입 공학을 113편 인용으로 정리한 리뷰이며, 인용된 계산값은 조건이 빠져 그대로 옮겨 쓸 수 없다. |
| `xu2026_xlsdft_linear_scaling_100m_atoms` | Xu, Zhang et al. 2026 | Extreme-Scale Linear-Scaling Kohn-Sham DFT at 100 Million Atoms: Bridging Quantum Simulations and Experiments | 밀도행렬 근시안성으로 KS-DFT를 O(N)으로 만들어 2억 원자 Si와 1,132만 원자 Li/LGPS 계면을 풀었지만 정확도 검증은 없다. |
| `yu2026_pvdf_mos2_anion_solvent_confinement` | Yu et al. 2026 | Composite Polymer Electrolytes With Hierarchical Confinement of Anions and Solvents for Stable Solid‐State Li Metal Batteries | MoS₂ 필러 7.5 wt%는 PVDF 막의 전도도와 Li 금속 계면 안정성을 함께 높였지만, 이를 받치는 계산은 약하다. |
| `zhu2026_zhs_precoverage_quasi_anode_free_zn` | Zhu et al. 2026 | Pre‐Coverage of Side Reaction Sites Enables Quasi‐Anode‐Free Rechargeable Aqueous Zinc Batteries | 고전류 예비순환으로 탄소 기판의 HER 활성자리를 ZHS로 미리 덮으면 Zn 도금/탈리 평균 CE가 99.94 %까지 오른다. |

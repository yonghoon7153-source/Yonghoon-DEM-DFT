# 양극 계면과 코팅

전해질 · 계면 · 장 `se-cathode` · 논문 42편 · 읽기 카드 42편

> 양극 활물질과 전해질 사이의 반응, 코팅 물질 선정, 고전압 구동.

## 장 서문 — 황화물 양극 계면 코팅은 반응을 막되 수송을 내준다

*읽기 카드 42편을 엮어 쓴 글 · 항목 30개 중 29개 검증 통과 · 2026-11-10*

황화물 고체전해질과 산화물 양극이 맞닿는 계면이 왜 무너지는지, 그 사이에 무엇을 끼워 막을지가 여기 모인 논문들의 질문이다. [근거: Zhu et al. 2016 (`zhu2016_first_principles_interface_stability_assb`); Xiao et al. 2019 (`xiao2019_cathode_coating_screening`); Park et al. 2026 (`park2026_ml_framework_stable_interfaces_assb`)]

계산은 음이온 화학의 불일치와 탈리튬 양극을 반응의 원인으로 지목했고, 코팅 후보를 폴리음이온 산화물 쪽으로 좁혀 왔다. [근거: Zhu et al. 2016 (`zhu2016_first_principles_interface_stability_assb`); Nolan et al. 2019 (`nolan2019_chemistries_stable_high_energy_cathodes`); Xiao et al. 2019 (`xiao2019_cathode_coating_screening`); Park et al. 2026 (`park2026_ml_framework_stable_interfaces_assb`)]

실험은 LiNbO₃, LTO, 할라이드, 황화물 자체 코팅이 수명을 늘린다는 것을 보였다. 그러나 두께와 전압창, 수송 대가를 어디서 끊을지는 아직 정량되지 않았다. [근거: Bong et al. 2023 (`bong2023_linbo3_thickness_uniformity_ncm523`); Kim et al. 2025 (`kim2025_lto_pald_conformal_coating_nca`); Cha et al. 2024 (`cha2024_dualcompatible_halide_ncm_lpscl_interface`); Kang et al. 2025 (`kang2025_highvoltage_parasitic_reaction_benefit_sulfide_assb`); Clausnitzer et al. 2024 (`clausnitzer2024_degradation_mechanisms_cathode_llzo`); Lee et al. 2026 (`lee2026_lpscl_coating_thickness_ncm811`)]

### 계면은 왜 반응하나

열역학 계산들은 황화물과 산화물 양극이 그대로 닿으면 크게 반응한다는 데 일치한다. Zhu et al. 2016은 황화물–LiCoO₂ 닫힌계 상호 반응 에너지를 −340 ~ −564 meV/atom으로 계산했다. 같은 계산에서 산화물 전해질–LiCoO₂는 0 ~ −53 meV/atom에 그쳤고, 원문은 그 차이를 Co가 아니라 O와 S 음이온 화학퍼텐셜의 불일치로 돌렸다. Xiao et al. 2019는 Li₃PS₄와 NCM의 반응이 충전이 진행될수록 커진다고 적었다. Park et al. 2026은 황화물 일곱 종과 양극 열 종을 짝지은 평균을 −332 meV/atom으로 냈다. [근거: Zhu et al. 2016 (`zhu2016_first_principles_interface_stability_assb`); Xiao et al. 2019 (`xiao2019_cathode_coating_screening`); Park et al. 2026 (`park2026_ml_framework_stable_interfaces_assb`)]

충전된 양극이 병목이라는 점도 여러 계산이 같은 방향을 가리킨다. Nolan et al. 2019는 탈리튬 양극이 Li가 많은 접촉물질과 반응한다고 정리했다. 검토 측 재분석에서 여덟 양극 상태 모두와 안정한 물질은 Li₂SO₄와 BeO 둘뿐이었다. Nolan et al. 2021은 가넷 LLZO와 NMC 계열의 E_d를 −87 ~ −132 meV/atom으로 계산해, 산화물 전해질에서도 Li 화학퍼텐셜 불일치가 반응을 부른다고 적었다. 이 값들은 hull 세대와 정규화가 서로 달라 같은 표에 놓지 않는다. [근거: Nolan et al. 2019 (`nolan2019_chemistries_stable_high_energy_cathodes`); Nolan et al. 2021 (`nolan2021_garnet_cathode_coating`); Zhu et al. 2016 (`zhu2016_first_principles_interface_stability_assb`)]

### 원자 수준의 첫 걸음

정적 DFT 슬랩 계산은 LiCoO₂|β-Li₃PS₄ 계면에서 Li 고갈과 양이온 교환이 일어나기 쉽다는 그림을 준다. Haruyama et al. 2014는 계면 LP2 자리의 Li 공공 형성에너지가 벌크 LPS의 3.2 eV보다 훨씬 낮은 1.44 eV라고 계산했다. Haruyama et al. 2017은 같은 계면의 Co↔P 교환이 −2.18 eV로 발열이고, 두 벌크 사이에서는 +1.98 eV로 흡열이라고 적었다. Okuno et al. 2020은 산화물 전해질과 LTO 버퍼가 낮은 형성에너지 자리를 줄인다고 보고, 그 원인을 가전자대 오프셋으로 설명했다. [근거: Haruyama et al. 2014 (`haruyama2014_space_charge_layer_oxide_cathode_sulfide_se`); Haruyama et al. 2017 (`haruyama2017_cation_mixing_co_diffusion_lco_lps`); Okuno et al. 2020 (`okuno2020_sulfide_vs_oxide_electrolyte_cathode_interfaces`)]

검토 측은 이 계열이 현상의 근거이지 정량의 근거가 아니라고 본다. 공간전하층의 두께와 전위는 계산되지 않았고, 결론은 LCO(110) 한 면과 적은 표본, 스핀 비편극 계산에 기댄다. MLIP 분자동역학은 더 큰 계와 긴 시간에서 같은 방향을 보였다. Guo 2025는 충전 LiCoO₂ 계면에서 Li 고갈층과 Co 이동을 관측했지만 임피던스는 계산하지 않았다. Ncube et al. 2026은 (010)LCO|LGPS에서 Co와 O가 넘어가는 상호확산을 보였고, 검토 측은 그 궤적이 평형에 이르지 않았다고 본다. [근거: Haruyama et al. 2014 (`haruyama2014_space_charge_layer_oxide_cathode_sulfide_se`); Haruyama et al. 2017 (`haruyama2017_cation_mixing_co_diffusion_lco_lps`); Guo 2025 (`guo2025_kinetic_cathode_se_interface`); Ncube et al. 2026 (`ncube2026_ionic_interdiffusion_lco_lgps_multiscale`)]

### 코팅 후보를 고르는 법

고속 스크리닝은 강한 공유결합을 가진 폴리음이온 산화물, 특히 인산염을 반복해서 남긴다. Zhu et al. 2016에서는 열여덟 종 가운데 Li₃PO₄만 네 상대와 모두 반응 에너지가 0이었고, 표준 코팅 LiNbO₃는 Li₃PS₄와 −155 meV/atom으로 반응했다. Xiao et al. 2019는 104,082종을 네 게이트로 걸러 184종을 남겼고, 산화물 쪽 생존자는 거의 폴리음이온 산화물이었다. Park et al. 2026도 O와 B, P, Si 폴리음이온 조성이 황화물과 양극 양쪽에 온건하다는 같은 결론을 냈다. [근거: Zhu et al. 2016 (`zhu2016_first_principles_interface_stability_assb`); Xiao et al. 2019 (`xiao2019_cathode_coating_screening`); Park et al. 2026 (`park2026_ml_framework_stable_interfaces_assb`)]

판정 기준이 논문마다 달라 같은 물질이 다른 판정을 받는다. 액체 LiPF₆ 전지를 다룬 Aykol et al. 2016은 양극과 평형된 Al₂O₃가 HF-scavenger 기능을 잃는다고 보았고, 그 계보는 Li₂ZrO₃와 LiAlO₂를 잘랐다. Nolan et al. 2021은 문턱을 |E_d| < 0.05 eV/atom으로 완화해 둘을 남겼다. 반응성 문턱도 Fitzhugh et al. 2019는 50 meV atom⁻¹, Xiao et al. 2019는 100 meV/atom으로 갈린다. Kim et al. 2026은 여덟 후보 중 계면 반응성 합산이 가장 나쁜 Li₃Sc₂(PO₄)₃를 골랐고, 검토 측은 최종 판정을 계면 열역학이 아니라 Li 수송이 내렸다고 본다. [근거: Aykol et al. 2016 (`aykol2016_ht_cathode_coating_design`); Nolan et al. 2021 (`nolan2021_garnet_cathode_coating`); Fitzhugh et al. 2019 (`fitzhugh2019_ht_functionally_stable_interfaces_sulfide`); Xiao et al. 2019 (`xiao2019_cathode_coating_screening`); Kim et al. 2026 (`kim2026_hts_li3sc2po43_coating_midni_ncm`)]

### 두께와 수송의 대가

실험은 코팅이 두꺼울수록 수명은 늘지만 초기 성능을 잃는 맞교환을 보인다. Bong et al. 2023에서 LiNbO₃를 두껍고 고르게 입힌 NCM523은 300사이클 유지율이 무코팅 26.5 %에서 85.1 %로 올랐다. Kim et al. 2025의 분체 ALD LTO는 두께가 늘수록 100사이클 유지율이 48 %에서 90 %로 올랐지만 첫 방전 용량은 줄었다. 검토 측은 두 논문 모두 두께가 다른 변수와 함께 움직이거나 최적이 곱셈 지표에서만 나와, 최적 두께를 정하지 못한다고 본다. [근거: Bong et al. 2023 (`bong2023_linbo3_thickness_uniformity_ncm523`); Kim et al. 2025 (`kim2025_lto_pald_conformal_coating_nca`)]

모델과 계산은 대가의 한 축이 코팅 안의 Li 확산이라고 본다. Clausnitzer et al. 2024는 100 nm 막의 Li 확산도가 1·10⁻¹² cm²/s보다 크게 낮으면 안 된다는 문턱을 내고, 이 기준이 열화층과 코팅층에 모두 적용된다고 적었다. Hu et al. 2024의 MLIP 계산에서 a-LiF는 가장 두꺼운 층에서 규칙 Li–F 사면체가 생겨 확산이 크게 줄었다. 전자 쪽 대가도 있어, Choi et al. 2026은 절연 WZO 코팅이 계면 저항을 192.9 Ω까지 키운 반면 산소결핍 BZOx는 55.2 Ω로 bare급을 유지했다고 적었다. Lee et al. 2026의 LPSCl 껍질 연구에서는 두께가 늘수록 유효 전자전도도가 단조로 줄었다. [근거: Clausnitzer et al. 2024 (`clausnitzer2024_degradation_mechanisms_cathode_llzo`); Hu et al. 2024 (`hu2024_amorphous_lif_coating_lco_lpscl_interface`); Choi et al. 2026 (`choi2026_bzox_dry_zro2x_nmc_shell_coating`); Lee et al. 2026 (`lee2026_lpscl_coating_thickness_ncm811`)]

### 전압창과 분해 산물

충전 상한과 방전 하한이 코팅 효과의 크기를 바꾼다. Wei et al. 2023에서 LiNbO₃ 코팅 이득은 3.9 V(vs Li-In)에서 가장 컸다. 4.2 V에서는 LiCoO₂의 H2에서 M2로 가는 비가역 상전이가 코팅 유무와 관계없이 열화를 지배했다. Du et al. 2022는 LMRO의 2.0 V 방전하한에서 충전 때 생긴 −S⁰−가 사라진다고 적었다. 검토 측은 가역인 것이 황 채널뿐이고 산소가 붙은 P·S 종은 쌓인다고 본다. [근거: Wei et al. 2023 (`wei2023_linbo3_coating_cutoff_voltage_lco_argyrodite`); Du et al. 2022 (`du2022_lmro_lpscl_reversible_redox_assb`)]

### 이 장의 값

| 값 | 표기 | 근거 |
|---|---|---|
| 황화물–LCO 닫힌계 상호 반응 에너지 | −340 ~ −564 meV/atom | Zhu et al. 2016 (`zhu2016_first_principles_interface_stability_assb`) |
| 황화물 SE–양극 70쌍 평균 반응에너지 | −332 meV/atom | Park et al. 2026 (`park2026_ml_framework_stable_interfaces_assb`) |
| LiNbO₃–Li₃PS₄ 닫힌계 반응 에너지 | −155 meV/atom | Zhu et al. 2016 (`zhu2016_first_principles_interface_stability_assb`) |
| LCO\|LPS 계면 LP2 Li 공공 형성에너지 | 1.44 eV | Haruyama et al. 2014 (`haruyama2014_space_charge_layer_oxide_cathode_sulfide_se`) |
| LCO\|LPS 계면 Co2↔P3 교환에너지 | −2.18 eV | Haruyama et al. 2017 (`haruyama2017_cation_mixing_co_diffusion_lco_lps`) |
| LiNbO₃ 9–18 nm NCM523 300사이클 유지율 | 85.1 % | Bong et al. 2023 (`bong2023_linbo3_thickness_uniformity_ncm523`) |
| NCM@Li₂ZrCl₆ 계면저항(TLM) | 20.1 Ω·cm² | Cha et al. 2024 (`cha2024_dualcompatible_halide_ncm_lpscl_interface`) |
| 100 nm 막 Li 확산도 문턱 | 1·10⁻¹² cm²/s | Clausnitzer et al. 2024 (`clausnitzer2024_degradation_mechanisms_cathode_llzo`) |

### 아직 열린 문제

- Li₃InCl₆가 양극 계면에 좋은지 두 실험이 갈린다. Cha et al. 2024에서 LIC 코팅은 100 사이클 유지율 80.8 %로 bare보다 나빴고 Li₂ZrCl₆만 NCM과 LPSCl 양쪽과 호환됐다. Lu et al. 2024는 LIC 셀이 −30 °C 용량비 26.9 %로 가장 좋다고 판정했다. Lu et al. 2024의 LIC 셀은 코팅이 아니라 catholyte와 분리막을 바꾼 설계라 두 결과는 같은 조건이 아니다. [근거: Cha et al. 2024 (`cha2024_dualcompatible_halide_ncm_lpscl_interface`); Lu et al. 2024 (`lu2024_lowtemp_assb_li2zro3_interface`)]
- 최적 코팅 두께를 받치는 근거가 아직 없다. Nisar et al. 2021의 10 nm 권고는 자기 표에서 유도되지 않는다고 검토 측은 본다. Bong et al. 2023의 9 nm 문턱, Hu et al. 2024의 약 1 nm, Lee et al. 2026의 317 nm, Kim et al. 2025의 3 nm도 검토 측은 측정 설계나 오차막대로 서지 않는다고 본다. [근거: Nisar et al. 2021 (`nisar2021_cathode_coating_review_critical_thickness`); Bong et al. 2023 (`bong2023_linbo3_thickness_uniformity_ncm523`); Hu et al. 2024 (`hu2024_amorphous_lif_coating_lco_lpscl_interface`); Lee et al. 2026 (`lee2026_lpscl_coating_thickness_ncm811`); Kim et al. 2025 (`kim2025_lto_pald_conformal_coating_nca`)]
- 코팅과 계면 산물을 지나는 Li 수송은 정량이 비어 있다. 스크리닝 논문 다수는 전도도를 선정에 넣지 않았고, Nolan et al. 2021의 후보 문헌 전도도는 10⁻⁷ S/cm 이하다. 검토 측은 Nisar et al. 2021의 확산계수 표가 박막 코팅 실물을 기술하지 못한다고 본다. Clausnitzer et al. 2024의 확산도 문턱과 이 후보들을 잇는 측정은 카드에 없다. [근거: Nolan et al. 2021 (`nolan2021_garnet_cathode_coating`); Nisar et al. 2021 (`nisar2021_cathode_coating_review_critical_thickness`); Clausnitzer et al. 2024 (`clausnitzer2024_degradation_mechanisms_cathode_llzo`); Xiao et al. 2019 (`xiao2019_cathode_coating_screening`); Park et al. 2026 (`park2026_ml_framework_stable_interfaces_assb`)]
- 공간전하층의 두께와 전위는 정량되지 않았다. Haruyama et al. 2014는 공공 형성에너지만 계산했고, Guo 2025의 Li 고갈 영역은 정성 관측이다. Wang et al. 2026 리뷰의 공간전하층 서술에는 검토 측이 부호 오류를 짚었다. [근거: Haruyama et al. 2014 (`haruyama2014_space_charge_layer_oxide_cathode_sulfide_se`); Guo 2025 (`guo2025_kinetic_cathode_se_interface`); Wang et al. 2026 (`wang2026_lirich_mn_cathode_solid_state_review`)]

### 먼저 읽을 논문

1. Zhu et al. 2016 (`zhu2016_first_principles_interface_stability_assb`) — 반응 에너지, 전기화학 창, 코팅 요건을 한 편에서 세워 뒤 논문들이 쓰는 계산 틀을 먼저 익힐 수 있다.
2. Xiao et al. 2019 (`xiao2019_cathode_coating_screening`) — 게이트형 스크리닝 깔때기와 폴리음이온 원리의 원형이라 뒤의 스크리닝 논문들을 이 설계와 견주어 읽게 된다.
3. Haruyama et al. 2014 (`haruyama2014_space_charge_layer_oxide_cathode_sulfide_se`) — 계면 슬랩과 자리별 Li 공공 형성에너지 지표의 출발점으로, 원자 수준 계산 계열이 여기서 갈라진다.
4. Bong et al. 2023 (`bong2023_linbo3_thickness_uniformity_ncm523`) — LiNbO₃ 두께와 피복을 바꾼 황화물 풀셀 비교로 실험 쪽 기준점을 준다.
5. Clausnitzer et al. 2024 (`clausnitzer2024_degradation_mechanisms_cathode_llzo`) — 막 Li 확산도 문턱을 내놓아 코팅의 수송 대가를 따지는 기준을 준다.

## 이 장의 논문 (42편)

| digest | 저자 · 연도 | 제목 | 한 줄 결론 |
|---|---|---|---|
| `aykol2014_cathode_coating_thermodynamics` | Aykol et al. 2014 | Thermodynamic Aspects of Cathode Coatings for Lithium‐Ion Batteries | HF 포획 엔탈피와 불화물 전환전압으로 이원 산화물을 거르면 알려진 코팅이 재현되고 3가 전이금속 산화물이 새 후보로 나온다. |
| `haruyama2014_space_charge_layer_oxide_cathode_sulfide_se` | Haruyama et al. 2014 | Space–Charge Layer Effect at Interface between Oxide Cathode and Sulfide Electrolyte in All-Solid-State Lithium-Ion Battery | LCO(110)의 산소 능선이 황화물 쪽 Li을 끌어당겨 공공 형성에너지를 낮추고, LiNbO₃ 버퍼가 그 흡착 자리를 없앤다고 원문은 계산으로 보였다. |
| `aykol2016_ht_cathode_coating_design` | Aykol et al. 2016 | High-throughput computational design of cathode coatings for Li-ion batteries | 산물을 자동 결정하는 반응 모델로 약 13만 종을 역할별로 걸렀고, 양극과 평형된 코팅은 기능이 달라졌다. |
| `zhu2016_first_principles_interface_stability_assb` | Zhu et al. 2016 | First principles study on electrochemical and chemical stability of solid electrolyte–electrode interfaces in all-solid-state Li-ion batteries | 대부분의 고체전해질–전극 계면은 열역학적으로 불안정하고, 황화물–LiCoO₂ 계면이 가장 크게 반응한다. |
| `garcia2017_nmc111_surface_energy_wulff_dft` | Garcia et al. 2017 | Surface Structure, Morphology, and Stability of Li(Ni1/3Mn1/3Co1/3)O₂ Cathode Material | NMC111 저지수면 중 (104)의 표면 에너지가 가장 낮고, 산화성과 Li 화학퍼텐셜에 따라 (012)와 (001)의 비중이 바뀐다. |
| `haruyama2017_cation_mixing_co_diffusion_lco_lps` | Haruyama et al. 2017 | Cation Mixing Properties toward Co Diffusion at the LiCoO₂ Cathode/Sulfide Electrolyte Interface in a Solid-State Battery | LiCoO₂\|β-Li₃PS₄ 계면에서 Co↔P 교환은 계면 CoO₄ 준위 덕분에 발열이고, 두 벌크 사이에서는 흡열이다. |
| `calpa2019_small_li7p3s11_liquid_phase_composite_cathode` | Calpa et al. 2019 | Electrochemical performance of bulk-type all-solid-state batteries using small-sized Li7P3S11 solid electrolyte prepared by liquid phase as the ionic conductor in the composite cathode | 액상법 소립 Li₇P₃S₁₁은 펠릿 σ가 낮아도 NCM 사이로 고르게 퍼져 첫 방전이 높지만 계면 저항이 크다. |
| `fitzhugh2019_ht_functionally_stable_interfaces_sulfide` | Fitzhugh et al. 2019 | A High‐Throughput Search for Functionally Stable Interfaces in Sulfide Solid‐State Lithium Ion Conductors | 67,062개 물질을 LSPS와 짝지어 계산하니 양극 범위에서는 황화물, 셀레늄화물, 아이오딘화물이 주로 통과했다 |
| `nolan2019_chemistries_stable_high_energy_cathodes` | Nolan et al. 2019 | Solid-State Chemistries Stable with High-Energy Cathodes for Lithium-Ion Batteries | 리튬화와 탈리튬화 양쪽에서 E_d가 0인 고체는 드물다. 탈리튬 양극이 병목이고, 리튬 인산염과 리튬 삼원 불화물이 고전압 양극과 맞는다. |
| `xiao2019_cathode_coating_screening` | Xiao et al. 2019 | Computational Screening of Cathode Coatings for Solid-State Batteries | P–O 같은 강공유결합 골격을 가진 폴리음이온 산화물이 양극과 황화물 전해질 양쪽에 안정해 코팅 후보로 남는다. |
| `okuno2020_sulfide_vs_oxide_electrolyte_cathode_interfaces` | Okuno et al. 2020 | Comparative Study on Sulfide and Oxide Electrolyte Interfaces with Cathodes in All-Solid-State Battery via First-Principles Calculations | 황화물 LPS 계면은 산화물 계면보다 Li가 쉽게 빠지는 자리가 많고, 원문은 그 원인을 가전자대 오프셋으로 설명한다. |
| `barai2021_delamination_cathode_llzo_multiscale` | Barai et al. 2021 | Investigation of Delamination-Induced Performance Decay at the Cathode/LLZO Interface | 박리는 양극 SOC 변화에 따른 수축 하나로 생기고, 그 세기는 Li 부분몰부피와 전해질 영률이 정한다. |
| `nisar2021_cathode_coating_review_critical_thickness` | Nisar et al. 2021 | Valuation of Surface Coatings in High-Energy Density Lithium-ion Battery Cathode Materials | 원문은 t = l²/D로 코팅이 10 nm 아래여야 한다고 권고한다. 검토 측은 그 권고가 자기 표에서 유도되지 않는다고 본다. |
| `nolan2021_garnet_cathode_coating` | Nolan et al. 2021 | Computation-guided discovery of coating materials to stabilize the interface between lithium garnet solid electrolyte and high-energy cathodes for all-solid-state lithium batteries | LLZO와 NMC는 Li 화학퍼텐셜 불일치로 반응하며, 둘 모두와 안정한 코팅은 Li₂O–MOₓ 타이라인 근처에만 있다. |
| `trevisanello2021_sc_pc_ncm_cracking_diffusion` | Trevisanello et al. 2021 | Polycrystalline and Single Crystalline NCM Cathode Materials—Quantifying Particle Cracking, Active Surface Area, and Lithium Diffusion | 다결정 NCM811의 겉보기 D̃_Li 상승은 균열로 액체가 침투해 표면적이 늘어난 결과이고, 본질 확산계수는 단결정과 같다. |
| `du2022_lmro_lpscl_reversible_redox_assb` | Du et al. 2022 | High-Energy and Long-Cycling All-Solid-State Lithium-Ion Batteries with Li- and Mn-Rich Layered Oxide Cathodes and Sulfide Electrolytes | LMRO의 2.0 V 방전하한에서 Li₆PS₅Cl의 폴리설파이드가 환원되고, 전도도를 높인 양극은 1000사이클 83 %를 유지했다. |
| `hikima2022_operando_band_structure_assb` | Hikima et al. 2022 | Operando analysis of electronic band structure in an all-solid-state thin-film battery | 박막 전고체전지를 반도체 소자로 보고 operando HAXPES로 재면, 충전 중 Li₂₋ₓMnO₃가 n형에서 p형으로 바뀌어 고전압 충전이 막힌다. |
| `bong2023_linbo3_thickness_uniformity_ncm523` | Bong et al. 2023 | Effect of thickness and uniformity of LiNbO3-coated layer on LiNi0.5Co0.2Mn0.3O2 cathode material on enhancement of cycle performance of full-cell sulfide-based all-solid-state batteries | LiNbO₃ 코팅을 두껍고 고르게 하면 300사이클 유지율이 26.5 %에서 85.1 %로 오르고, 성능은 양극 쪽 열화층 유무가 가른다. |
| `tron2023_rational_cathode_composite_optimization_lpscl` | Tron et al. 2023 | Rational Optimization of Cathode Composites for Sulfide-Based All-Solid-State Batteries | 한 시험 규약으로 복합양극 변수를 차례로 고정하자 단결정 NMC811, C65, 작은 Li₆PS₅Cl, AM:SE 40:60–60:40 vol이 남았다. |
| `wei2023_linbo3_coating_cutoff_voltage_lco_argyrodite` | Wei et al. 2023 | Unraveling the LiNbO3 coating layer on battery performances of lithium argyrodite-based all-solid-state batteries under different cut-off voltages | LiNbO₃ 코팅은 3.9 V(vs Li-In)에서 이득이 가장 크고, 4.2 V에서는 LiCoO₂의 비가역 상전이가 열화를 지배해 코팅으로 막지 못한다. |
| `zuo2022_chlorination_cathode_interface` | Zuo et al. 2023 | Impact of the Chlorination of Lithium Argyrodites on the Electrolyte/Cathode Interface in Solid‐State Batteries | Li₅.₅PS₄.₅Cl₁.₅는 Li₆PS₅Cl보다 더 많이 산화 분해되지만 NCM85 계면에서 고체 phosphate를 덜 만들어 정전압 홀드 중 저항 증가가 느리다. |
| `cha2024_dualcompatible_halide_ncm_lpscl_interface` | Cha et al. 2024 | Stabilizing the interface between high-Ni oxide cathode and Li6PS5Cl for all-solid-state batteries via dual-compatible halides | 할라이드 코팅의 성패는 이온전도도가 아니라 NCM과 LPSCl 양쪽과의 화학적 호환성이 가르고, LZC만 이를 만족한다. |
| `clausnitzer2024_degradation_mechanisms_cathode_llzo` | Clausnitzer et al. 2024 | Impact of degradation mechanisms at the cathode/electrolyte interface of garnet-based all-solid-state batteries | LCO\|LLZO 복합양극의 용량 손실은 옴 저항보다 계면 막 안의 낮은 Li 확산도가 지배한다. |
| `hu2024_amorphous_lif_coating_lco_lpscl_interface` | Hu et al. 2024 | Impact of Amorphous LiF Coating Layers on Cathode‐Electrolyte Interfaces in Solid‐State Batteries | a-LiF 코팅은 두께에 따라 계면 부반응을 억제하지만 20 Å에서 Li 확산이 크게 줄어, 원문은 최적 두께를 약 1 nm로 제안했다. |
| `liu2024_sc_ni90_sulfur_coating_sulfide_assb` | Liu et al. 2024 | High‐Capacity, Long‐Life Sulfide All‐Solid‐State Batteries with Single‐Crystal Ni‐Rich Layered Oxide Cathodes | 단결정 Ni90에 황 0.2 wt%로 만든 10–20 nm 황화물 피막이 55 °C 전고체 셀의 율속, 수명, 면용량을 모두 가장 크게 올렸다. |
| `lu2024_lowtemp_assb_li2zro3_interface` | Lu et al. 2024 | Superior Low-Temperature All-Solid-State Battery Enabled by High-Ionic-Conductivity and Low-Energy-Barrier Interface | −30 °C 성능은 양극 계면이 좌우하고, Li₃InCl₆로 계면을 고치면 율속이 전해질 입계로 넘어간다. |
| `guo2025_kinetic_cathode_se_interface` | Guo 2025 | Kinetic analysis of cathode-solid electrolyte interface in all-solid-state batteries | 범용 MLIP 분자동역학은 충전 양극 계면에서 세 가지 운동학 기전을 보였지만, 임피던스와 반응속도는 재지 않았다. |
| `kang2025_highvoltage_parasitic_reaction_benefit_sulfide_assb` | Kang et al. 2025 | High-voltage stability of sulfide-based all-solid-state batteries: benefit of the parasitic reaction | LPSCl 건식 코팅은 고전압 기생반응을 막지 않고 고르게 퍼뜨린다. 그 결과 NCM811의 SOC가 균일하게 낮아져 구조 붕괴가 늦춰진다. |
| `kim2025_lto_pald_conformal_coating_nca` | Kim et al. 2025 | Effect of a conformal lithium titanate buffer layer deposited via powder atomic layer deposition on the performance of sulfide-based all-solid-state batteries | 분체 ALD로 입힌 비정질 LTO 막은 황화물 산화와 NCA 상전이를 함께 억제한다. 다만 두께가 늘면 초기 용량이 줄어든다. |
| `qi2025_high_voltage_limits_halide_sulfide_assb` | Qi et al. 2025 | Deciphering and overcoming the high-voltage limitations of halide and sulfide-based all-solid-state lithium batteries | 4.5 V에서 LZC 셀은 장기 붕괴, LPSC 셀은 첫 사이클 손실이 크고, LZPO 코팅이 둘 다 개선하지만 DFT 해석은 약하다. |
| `qian2025_lipo2f2_coating_stable_cei` | Qian et al. 2025 | Engineering Stable Decomposition Products on Cathode Surfaces to Enable High Voltage All‐Solid‐State Batteries | 분해산물이 안정한 LiPO₂F₂를 NCM85에 용액 코팅하면 LiF와 LiPₓOᵧF_z 계면층이 생겨 Li₆PS₅Cl 산화가 억제되고 수명이 는다. |
| `son2025_fivevolt_assb` | Son et al. 2025 | Five-volt-class high-capacity all-solid-state lithium batteries | LiCl–4Li₂TiF₆ 불소계 차폐층은 황화물, 할라이드, LiNbO₃가 버티지 못하는 5 V급 LNMO 양극을 안정하게 구동시킨다. |
| `choi2026_bzox_dry_zro2x_nmc_shell_coating` | Choi et al. 2026 | Dry‐Crafted Charge‐Conductive ZrO₂ − x Cathode Shell Coating for High‐Performance Sulfide‐Based Solid‐State Batteries | 건식 코팅한 black ZrO₂₋ₓ 셸은 NMC811의 전하 수송을 보존하면서 LPSCl 계면 부반응을 억제해 초기 CE를 69.6에서 77.5 %로 올렸다. |
| `jang2026_halide_se_interfacial_stability_highv_na` | Jang et al. 2026 | Interfacial Stability and Design Strategies for Halide Solid Electrolytes in High‐Voltage All‐Solid‐State Sodium‐Ion Batteries | Na 할라이드 7종은 산화 창이 넓지만 양극과의 상호 분해 구동력이 작지 않고, NaB₃O₅ 같은 코팅이 그 구동력을 크게 낮춘다. |
| `kawaguchi2026_se_size_soc_dependent_cathode_resistance` | Kawaguchi et al. 2026 | Interface Engineering in Sulfide‐Based All‐Solid‐State Batteries: Insights from Resistance Analysis | LPSCl 복합양극에서 높은 SOC는 큰 SE가, 낮은 SOC는 작은 SE가 저항이 낮아 최적 입도는 SOC에 따라 다르다. |
| `kim2026_hts_li3sc2po43_coating_midni_ncm` | Kim et al. 2026 | High-throughput discovery of Li3Sc2(PO4)3 as a protective coating for stabilizing mid-Ni NCM interfaces in all-solid-state batteries | 계면 열역학으로 좁힌 8종 가운데 Li가 실제로 움직인 Li₃Sc₂(PO₄)₃가 mid-Ni NCM523 코팅으로 뽑혔다. |
| `lee2026_lpscl_coating_thickness_ncm811` | Lee et al. 2026 | Balancing Ionic and Electronic Conductivities in All‐Solid‐State Batteries: The Effect of LPSCl Coating Thickness on Cathode Active Materials | NCM811에 입힌 LPSCl 껍질은 317 nm에서 유효 이온전도도가 가장 높았고, 유효 전자전도도는 두께가 늘수록 계속 줄었다. |
| `lee2026_mechanical_halogen_argyrodite_drycoating` | Lee et al. 2026 | Beyond Electrochemistry: Tailoring Mechanical Properties of Halogen-Substituted Argyrodites for Conformal Dry Coating and Enhanced Battery Performance | 할로겐-rich argyrodite는 산화 안정성이 나쁜데도 기계 물성과 접착이 커서 NCM 건식 코팅이 잘 되고 셀 성능이 가장 좋다. |
| `liu2026_ccto_colossal_dielectric_interlayer_dry_lpscl` | Liu et al. 2026 | Colossal-dielectric cathode interface engineering enables interfacial stability in dry-processed Li6PS5Cl solid-state batteries | CCTO를 섞은 얇은 이온겔 중간층이 끝없는 충전을 없애지만, 격리 효과 대부분은 CCTO 없는 겔로도 나온다. |
| `ncube2026_ionic_interdiffusion_lco_lgps_multiscale` | Ncube et al. 2026 | Ionic interdiffusion at cathode\|solid-electrolyte interface: A machine learning–assisted multiscale investigation and mitigation strategies | LCO\|LGPS는 상온에서 Co·O가 넘어가 interphase를 만들고, LNTO는 이를 막지만 단단해서 계면 박리를 부른다. |
| `park2026_ml_framework_stable_interfaces_assb` | Park et al. 2026 | Machine‐Learning Framework for Designing Stable Interfaces in All‐Solid‐State Lithium‐Ion Batteries | 황화물 SE와 산화물 양극은 그대로 붙이면 강하게 반응하고, O 중심 폴리음이온 코팅이 양쪽 반응을 함께 낮춘다. |
| `wang2026_lirich_mn_cathode_solid_state_review` | Wang et al. 2026 | Recent progress and perspectives of lithium-rich manganese-based cathodes for high-energy-density solid-state batteries | LRM의 고용량은 격자산소 활성화에 기대고, 그 산소 화학이 전해질 족마다 다른 열화 경로로 계면을 무너뜨린다고 정리했다. |

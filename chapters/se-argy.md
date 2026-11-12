# 아지로다이트 조성 설계

전해질 · 계면 · 장 `se-argy` · 논문 24편 · 읽기 카드 24편

> 할로젠 조성, 이종 원소 치환, 자리 무질서가 전도도와 안정성을 어떻게 바꾸는가.

## 장 서문 — 음이온 자리 무질서가 아지로다이트 전도를 켠다

*읽기 카드 24편을 엮어 쓴 글 · 항목 30개 중 29개 검증 통과 · 2026-11-10*

아지로다이트에서 할로젠 조성, 이종 원소 치환, 자리 무질서가 Li 전도도와 계면, 대기 안정성을 어떻게 바꾸는지가 질문이다. 할로젠과 S²⁻가 두 음이온 자리에 섞여 앉아야 케이지 사이 점프가 켜진다는 데는 구조, 계산, 실험이 모였다. [근거: Deiseroth et al. 2008 (`deiseroth2008_li6ps5x_argyrodite_high_li_mobility`); de Klerk et al. 2016 (`deklerk2016_diffusion_site_disorder_argyrodite`); Kraft et al. 2017 (`kraft2017_lattice_polarizability_argyrodite_Li6PS5X`); Adeli et al. 2019 (`adeli2019_halide_substitution_boosting_argyrodite`)]

그러나 최적 무질서 정도와 Cl 과잉이 전도도를 올리는 기전은 아직 논문마다 다르게 답한다. 고용한계도 공정 조건과 얽혀 있다. [근거: de Klerk et al. 2016 (`deklerk2016_diffusion_site_disorder_argyrodite`); Feng et al. 2020 (`feng2020_li_deficient_argyrodite_cl_disorder`); Wang et al. 2020 (`wang2020_br_rich_argyrodite_fast_ion_conduction_origin`); Jang et al. 2025 (`jang2025_thioarsenate_argyrodite_mlip_mechanism`); Liu et al. 2022 (`liu2022_cl_crystallization_interface_argyrodite`)]

공도핑 연구들은 Li 금속 계면과 대기 안정성을 얻었다고 보고하지만 전도도는 오르기도 하고 내리기도 한다. 도펀트 자리 배정과 기전 계산은 검토 측이 약하다고 본 경우가 많다. [근거: Dual-Functional Ga/F Co-Doped … (`liyaru_gaf3_codoping_argyrodite`); Li et al. 2025 (`li2025_cubr2_dualdoping_argyrodite`); Yang et al. 2025 (`yang2025_lao_dualdoping_argyrodite_lacl3`); Xu et al. 2026 (`xu2026_ndo_codoping_argyrodite`); Wu et al. 2026 (`wu2026_ta_argyrodite_selfpassivating`)]

### 무질서가 전도를 켠다

할로젠과 S²⁻가 두 음이온 자리를 섞어 앉는 무질서가 거시 Li 전도의 조건이라는 데 여러 방법이 함께 모인다. Deiseroth et al. 2008은 Cl과 Br에서는 S²⁻와 할라이드가 자리를 섞고 I에서는 질서를 이룬다고 보고했다. de Klerk et al. 2016의 AIMD에서는 Cl을 모두 4a에 두면 intercage 점프가 사라졌고, Li₆PS₅I는 세 온도 모두에서 intercage 점프가 없었다. Kraft et al. 2017은 음이온 무질서가 Cl 62 %에서 I 0 %로 사라진다고 정련했고, I 계의 낮은 전도도를 격자 무름이 아니라 무질서 소멸과 prefactor 붕괴로 해석했다. Jang et al. 2025의 MLIP-MD에서도 Li₆AsS₅Br의 계산 σ는 반전율이 오를수록 가파르게 올랐다. [근거: Deiseroth et al. 2008 (`deiseroth2008_li6ps5x_argyrodite_high_li_mobility`); de Klerk et al. 2016 (`deklerk2016_diffusion_site_disorder_argyrodite`); Kraft et al. 2017 (`kraft2017_lattice_polarizability_argyrodite_Li6PS5X`); Jang et al. 2025 (`jang2025_thioarsenate_argyrodite_mlip_mechanism`)]

Cl이나 Br을 늘리고 Li를 빼는 실험 계열은 전도도를 올렸지만, 기전은 논문마다 다른 레버를 지목한다. Adeli et al. 2019는 cold-press total σ가 x=0에서 2.5 mS/cm, x=0.5에서 9.4 mS/cm로 올랐다고 적고 정전 약화, Li 공공, 자리 무질서를 함께 원인으로 들었다. Feng et al. 2020은 x = 0.7까지 단상을 얻어 25 °C 전도도 17.3 mS cm⁻¹를 보고했고, AIMD 세 모형으로 혼합이 Ea를 정하고 결핍이 σ의 크기를 정한다고 제시했다. Wang et al. 2020은 Br 계열에서 1S3Br 배치를 주요인으로 들었다. 검토 측은 그 점프율이 de Klerk et al. 2016의 Cl 값을 차용한 것이고 공공, 4d-Br, 24g 분율이 함께 움직여 기원을 가르지 못했다고 본다. [근거: Adeli et al. 2019 (`adeli2019_halide_substitution_boosting_argyrodite`); Feng et al. 2020 (`feng2020_li_deficient_argyrodite_cl_disorder`); Wang et al. 2020 (`wang2020_br_rich_argyrodite_fast_ion_conduction_origin`); de Klerk et al. 2016 (`deklerk2016_diffusion_site_disorder_argyrodite`)]

### 최적 무질서의 위치

얼마나 섞여야 가장 빠른지에는 서로 다른 답이 나와 있다. de Klerk et al. 2016은 Li₆PS₅Cl에서 4c-Cl 75 %의 제한 점프율이 가장 크다고 예측했다. 검토 측은 이 결론이 σ_J 지표, 분포당 단일 배열, 단위셀 조건에 묶이고, 2024년 MTP-MLIP 연구는 σ 피크를 25 %로 보고했다고 적었다. Jang et al. 2025는 Li₆AsS₅Br의 σ 최대를 반전 50 %로 보고 배열 엔트로피 최대 1.386R과 겹쳐 읽었지만, 검토 측은 ΔS_conf가 반전율의 결정론적 함수라 인과를 말해 주지 않는다고 본다. Kraft et al. 2017은 격자 강성 축에서 최적을 찾았고, 장벽과 prefactor가 함께 낮아져 상온 전도도 최대가 가장 무른 조성이 아닌 Li₆PS₅Cl₀.₅Br₀.₅에서 나왔다. [근거: de Klerk et al. 2016 (`deklerk2016_diffusion_site_disorder_argyrodite`); Jang et al. 2025 (`jang2025_thioarsenate_argyrodite_mlip_mechanism`); Kraft et al. 2017 (`kraft2017_lattice_polarizability_argyrodite_Li6PS5X`)]

무질서의 실측값도 측정법마다 갈린다. 검토 측은 Feng et al. 2020의 x = 0 시료에서 4d-Cl이 ³⁵Cl 5 %, ³¹P 31 %, X-선 36.7 %로 갈리고 중성자 문헌값은 ≈ 62 %인데 원문이 이 불일치를 다루지 않는다고 적었다. Liu et al. 2022의 무질서 값은 오차 없는 lab XRD 정련값이고, 검토 측은 S²⁻와 Cl⁻의 X선 대비가 거의 없으며 두 조성 모두 중성자 문헌값보다 낮다고 본다. Feng et al. 2020과 Wang et al. 2020은 ⁶Li 스펙트럼을 24g와 48h 두 성분으로 나눠 24g를 빠른 전도의 핵심으로 읽었다. 검토 측은 두 성분의 간격이 수 Hz라서 빠른 교환이면 한 선으로 합쳐져야 한다고 본다. [근거: Feng et al. 2020 (`feng2020_li_deficient_argyrodite_cl_disorder`); Liu et al. 2022 (`liu2022_cl_crystallization_interface_argyrodite`); Wang et al. 2020 (`wang2020_br_rich_argyrodite_fast_ion_conduction_origin`); Kraft et al. 2017 (`kraft2017_lattice_polarizability_argyrodite_Li6PS5X`)]

### 고용한계와 공정

Cl 고용한계는 논문마다 다르고, 그 차이에 열처리 조건이 겹쳐 있다. Adeli et al. 2019의 공정에서는 x=0.5를 넘으면 LiCl이 석출해 x=0.6의 σ가 3.3 mS/cm로 떨어졌다. 검토 측은 이 상한을 550 °C 고상 공정의 결과로 보고 열역학 상수로 읽지 않는다. Feng et al. 2020은 더 높은 x까지 단상을 얻었지만 소결 온도가 x와 함께 내려가 단일 변수 계열이 아니라고 검토 측은 본다. [근거: Adeli et al. 2019 (`adeli2019_halide_substitution_boosting_argyrodite`); Feng et al. 2020 (`feng2020_li_deficient_argyrodite_cl_disorder`)]

Cl-rich 조성의 전도도 이득도 공정에 따라 달라진다. Liu et al. 2022에서 Li₅.₅PS₄.₅Cl₁.₅는 450 °C 어닐에서만 순상이었고, 550 °C에서는 Li₆PS₅Cl과 전도도가 같았다. Xu et al. 2026(다상 재구성)은 같은 명목 조성을 480 °C로 구워 argyrodite 기지, P₂S₆⁴⁻ 2차상, LiCl의 다상을 얻고 σ 6.9 mS/cm를 보고했다. 검토 측은 이 조성이 대조군 상용 LPSC1.5와 같고 열처리가 달라 다상 고유의 몫이 분리되지 않았다고 본다. 우리 modelc(Li₅.₄PS₄.₄Cl₁.₆)는 이 공정들에서 모두 다상이 되는 구간에 있으므로, 우리는 단상 가정에 LiCl과 P₂S₆⁴⁻를 2차상 후보로 붙인다. [근거: Liu et al. 2022 (`liu2022_cl_crystallization_interface_argyrodite`); Xu et al. 2026 (`xu2026_offstoich_composite_lpsc_highvoltage`); Adeli et al. 2019 (`adeli2019_halide_substitution_boosting_argyrodite`)]

### 공도핑의 맞교환

Li 금속 쪽에서는 전자전도도가 낮은 조성에서 CCD가 높다는 관찰이 반복된다. GaF₃ 공도핑 논문, Taklu et al. 2021, Li et al. 2025가 이 역상관을 보고했다. Yang et al. 2025에서는 전자전도도가 2.59×10⁻⁹에서 2.2×10⁻⁸ S/cm로 올랐는데도 CCD가 0.9에서 3.1 mA/cm²로 커졌고, 원문은 CCD가 이온전도도와도 상관없어 보인다고 적었다. Liu et al. 2022는 반대로 전도도가 CCD를 주로 정한다고 해석했다. Liu et al. 2024의 검토 측은 CCD와 대칭셀 수명이 셀 형상과 압력에 의존해 다른 논문과 절대 비교할 수 없다고 본다. [근거: Dual-Functional Ga/F Co-Doped … (`liyaru_gaf3_codoping_argyrodite`); Taklu et al. 2021 (`taklu2021_cucl_dualdoping_air_stability_argyrodite`); Li et al. 2025 (`li2025_cubr2_dualdoping_argyrodite`); Yang et al. 2025 (`yang2025_lao_dualdoping_argyrodite_lacl3`); Liu et al. 2022 (`liu2022_cl_crystallization_interface_argyrodite`); Liu et al. 2024 (`liu2024_pband_center_sbo_dual_interface`)]

### 자리 배정과 계산 근거

3가 도판트가 P 자리(4b)에 들어간다는 배정은 여러 편이 쓰지만 직접 증거는 약하다. GaF₃ 공도핑 논문의 Ga 자리 배정은 같은 그룹의 InF₃ 선행 논문에서 그대로 인용한 것이고, 검토 측은 Li 2024의 In 자리 증거도 약하다고 본다. Xu et al. 2026(Nd–O)은 Nd³⁺의 P 치환을 inferred라 적었고, 검토 측은 Rietveld, ³¹P NMR, EXAFS가 없다고 확인했다. Yang et al. 2025의 Rietveld도 La와 O를 명목 점유로 고정한 모델이라 검토 측은 La 자리를 결정한 것이 아니라고 본다. 우리 스크리닝 규칙은 3가 도판트를 모두 Li_24g에 두어 이 배정과 갈리므로, 우리는 두 자리의 형성에너지를 DFT로 직접 비교해야 한다. [근거: Dual-Functional Ga/F Co-Doped … (`liyaru_gaf3_codoping_argyrodite`); Li 2024 (`li2024_inf3_argyrodite_ultrathin_film`); Xu et al. 2026 (`xu2026_ndo_codoping_argyrodite`); Yang et al. 2025 (`yang2025_lao_dualdoping_argyrodite_lacl3`)]

기전을 받치는 계산은 실측과 어긋나는 곳이 많다. 검토 측은 GaF₃ 공도핑 논문이 표면 NEB 장벽으로 벌크 σ를 설명한 것을 범주 오류로 보고, Wu et al. 2026의 DFT 셀 팽창이 실험 격자 팽창보다 훨씬 커 NEB 장벽 감소의 상당 부분이 인공 팽창일 수 있다고 본다. Lee et al. 2024의 MTP가 실험과 맞은 구간은 0.001–14.8 mS/cm인데 논문이 내세운 값은 38–80 mS/cm다. Jang et al. 2025의 계산 σ는 실험과 겹치는 두 조성에서 3.3배와 6.3배 크다. Jiang et al. 2022의 호스트 σ가 실험과 맞은 것도 검토 측은 낮은 Ea와 Haven 비 1 가정의 상쇄로 보고 검증으로 쓰지 않는다. [근거: Dual-Functional Ga/F Co-Doped … (`liyaru_gaf3_codoping_argyrodite`); Wu et al. 2026 (`wu2026_ta_argyrodite_selfpassivating`); Lee et al. 2024 (`lee2024_multicomponent_argyrodite_mixed_oxidation_mtp`); Jang et al. 2025 (`jang2025_thioarsenate_argyrodite_mlip_mechanism`); Jiang et al. 2022 (`jiang2022_se_doped_lpscl_high_throughput_dft`)]

### 이 장의 값

| 값 | 표기 | 근거 |
|---|---|---|
| Li₅.₅PS₄.₅Cl₁.₅ σ, cold-press 298 K | 9.4±0.1 mS/cm | Adeli et al. 2019 (`adeli2019_halide_substitution_boosting_argyrodite`) |
| Cl 과잉 x = 0.7 σ, 25 °C 소결 | 17.3 mS cm⁻¹ | Feng et al. 2020 (`feng2020_li_deficient_argyrodite_cl_disorder`) |
| Li₆PS₅Cl 4c-Cl 75 %/50 % 점프율 비 | 1.99× | de Klerk et al. 2016 (`deklerk2016_diffusion_site_disorder_argyrodite`) |
| Li₆PS₅Cl 음이온 자리 무질서, 중성자 | 62 % | Kraft et al. 2017 (`kraft2017_lattice_polarizability_argyrodite_Li6PS5X`) |
| Li₆AsS₅Br 배열 엔트로피 최대 | 1.386R | Jang et al. 2025 (`jang2025_thioarsenate_argyrodite_mlip_mechanism`) |
| CuBr₂ 도핑 LPSC-CB 상온 σ | 10.3 mS/cm | Li et al. 2025 (`li2025_cubr2_dualdoping_argyrodite`) |
| Nd–O 공도핑 CCD, Li 대칭셀 | 6.62 mA/cm² | Xu et al. 2026 (`xu2026_ndo_codoping_argyrodite`) |
| MTP가 실험과 맞은 σ 구간 | 0.001–14.8 mS/cm | Lee et al. 2024 (`lee2024_multicomponent_argyrodite_mixed_oxidation_mtp`) |

### 아직 열린 문제

- Li₆PS₅Cl계에서 4c(4d) 할로젠 점유의 최적점은 정해지지 않았다. de Klerk et al. 2016은 75 %를, 그 카드가 전하는 2024년 MTP-MLIP 연구는 25 %를 보고했고, Jang et al. 2025는 Li₆AsS₅Br에서 50 %를 내놓았다. [근거: de Klerk et al. 2016 (`deklerk2016_diffusion_site_disorder_argyrodite`); Jang et al. 2025 (`jang2025_thioarsenate_argyrodite_mlip_mechanism`)]
- Cl이나 Br 과잉이 전도도를 올리는 레버가 Li 공공인지 4d 배치인지는 갈리지 않았다. x 하나만 바꾸는 계열에서 공공, 4d 할로젠, 24g 분율이 함께 움직인다. 우리 원장의 공공 판정과 Wang et al. 2020의 4d 배치 주장은 서로 다른 레버를 지목하며, 우리 데이터로도 어느 쪽인지 가르지 못한다. [근거: Wang et al. 2020 (`wang2020_br_rich_argyrodite_fast_ion_conduction_origin`); Feng et al. 2020 (`feng2020_li_deficient_argyrodite_cl_disorder`); Adeli et al. 2019 (`adeli2019_halide_substitution_boosting_argyrodite`)]
- 3가 도판트가 P_4b와 Li_24g 중 어디에 앉는지는 비어 있다. 원문들의 4b 배정은 인용이나 추론에 기대고, 우리는 두 자리의 형성에너지를 아직 비교하지 않았다. [근거: Dual-Functional Ga/F Co-Doped … (`liyaru_gaf3_codoping_argyrodite`); Li 2024 (`li2024_inf3_argyrodite_ultrathin_film`); Xu et al. 2026 (`xu2026_ndo_codoping_argyrodite`)]
- CCD를 전자전도도가 정하는지 이온전도도가 정하는지는 논문마다 다르게 읽는다. 전자전도도가 올랐는데 CCD가 커진 사례도 있다. [근거: Dual-Functional Ga/F Co-Doped … (`liyaru_gaf3_codoping_argyrodite`); Li et al. 2025 (`li2025_cubr2_dualdoping_argyrodite`); Liu et al. 2022 (`liu2022_cl_crystallization_interface_argyrodite`); Yang et al. 2025 (`yang2025_lao_dualdoping_argyrodite_lacl3`)]

### 먼저 읽을 논문

1. Deiseroth et al. 2008 (`deiseroth2008_li6ps5x_argyrodite_high_li_mobility`) — Li₆PS₅X의 F-43m 구조, 48h와 24g 부분점유, S/X 자리 섞임을 처음 정의해 이후 논문의 공통 언어가 된다.
2. de Klerk et al. 2016 (`deklerk2016_diffusion_site_disorder_argyrodite`) — intercage 점프를 율속으로 보는 틀과 75 % 최적 예측을 세워, 뒤 논문들이 이 예측을 시험하거나 차용한다.
3. Adeli et al. 2019 (`adeli2019_halide_substitution_boosting_argyrodite`) — Cl 과잉 계열의 실험 기준선과 중성자 점유율, x=0.5 고용한계를 준다.
4. Feng et al. 2020 (`feng2020_li_deficient_argyrodite_cl_disorder`) — 같은 계열을 더 높은 x로 밀고, 무질서 실측값이 측정법마다 갈리는 문제를 드러낸다.
5. Dual-Functional Ga/F Co-Doped … (`liyaru_gaf3_codoping_argyrodite`) — 단일 도판트 대조군으로 공도핑의 전도도와 계면 맞교환, 자리 배정과 계산 근거의 약점을 한 편에서 보여 준다.

## 이 장의 논문 (24편)

| digest | 저자 · 연도 | 제목 | 한 줄 결론 |
|---|---|---|---|
| `liyaru_gaf3_codoping_argyrodite` |  | Dual-Functional Ga/F Co-Doped Argyrodite Sulfide Electrolytes for All-Solid-State Lithium Batteries | Li₅.₅PS₄.₅Cl₁.₅에 GaF₃를 4 % 넣으면 σ는 줄지만 F가 전자를 막아 CCD와 대기 안정성이 크게 오른다. |
| `deiseroth2008_li6ps5x_argyrodite_high_li_mobility` | Deiseroth et al. 2008 | Li₆PS₅X: A Class of Crystalline Li‐Rich Solids With an Unusually High Li⁺ Mobility | Li₆PS₅X를 단상 결정으로 확립했고, 구조와 ⁷Li NMR 선폭을 근거로 높은 Li⁺ 이동도를 주장했다 |
| `deklerk2016_diffusion_site_disorder_argyrodite` | de Klerk et al. 2016 | Diffusion Mechanism of Li Argyrodite Solid Electrolytes for Li-Ion Batteries and Prediction of Optimized Halogen Doping: The Effect of Li Vacancies, Halogens, and Halogen Disorder | Li₆PS₅X의 거시 전도는 intercage 점프가 율속이고, Cl을 4c에 75 % 두면 제한 점프율이 50 % 대비 약 두 배다. |
| `kraft2017_lattice_polarizability_argyrodite_Li6PS5X` | Kraft et al. 2017 | Influence of Lattice Polarizability on the Ionic Conductivity in the Lithium Superionic Argyrodites Li₆PS₅X (X = Cl, Br, I) | Li₆PS₅X에서 할라이드가 무거워질수록 격자가 물러져 E_A와 prefactor가 함께 낮아지고, 전도도는 중간 강성인 Li₆PS₅Cl₀.₅Br₀.₅에서 가장 높다. |
| `adeli2019_halide_substitution_boosting_argyrodite` | Adeli et al. 2019 | Boosting Solid‐State Diffusivity and Conductivity in Lithium Superionic Argyrodites by Halide Substitution | Cl⁻/S²⁻ 비를 x=0.5까지 높이면 정전 약화, Li 공공, 자리 무질서가 겹쳐 전도도가 2.5에서 9.4 mS/cm로 오른다. |
| `feng2020_li_deficient_argyrodite_cl_disorder` | Feng et al. 2020 | Enhanced ion conduction by enforcing structural disorder in Li-deficient argyrodites Li6−xPS5−xCl1+x | Li₆₋ₓPS₅₋ₓCl₁₊ₓ를 x = 0.7까지 단상으로 만들자 전도도가 오르고 Ea가 내려갔지만, 기전을 받치는 구조 정량은 측정법마다 갈린다. |
| `wang2020_br_rich_argyrodite_fast_ion_conduction_origin` | Wang et al. 2020 | Fast Ion Conduction and Its Origin in Li6–xPS5–xBr1+x | Br 과잉은 전도도를 올리고 4d의 Br 분율을 늘리지만, 1S3Br 배치와 24g가 그 원인이라는 주장은 가설 수준이다. |
| `taklu2021_cucl_dualdoping_air_stability_argyrodite` | Taklu et al. 2021 | Dual CuCl doped argyrodite superconductor to boost the interfacial compatibility and air stability for all solid-state lithium metal batteries | Li₆PS₅Cl에 CuCl을 x=0.1만큼 넣으면 전도도 4.34 mS/cm, CCD 3.0 mA/cm², H₂S 발생 절반을 함께 얻는다. |
| `jiang2022_se_doped_lpscl_high_throughput_dft` | Jiang et al. 2022 | Se-doped Li₆PS₅Cl and Li 5.5 PS 4.5 Cl 1.5 with improved ionic conductivity and interfacial compatibility: a high-throughput DFT study | Se 치환은 계산 전도도를 높이고 Ea를 낮추지만, 양극 계면 반응에너지와 밴드갭은 오히려 나빠진다. |
| `liu2022_cl_crystallization_interface_argyrodite` | Liu et al. 2022 | Revealing the Impact of Cl Substitution on the Crystallization Behavior and Interfacial Stability of Superionic Lithium Argyrodites | Li₅.₅PS₄.₅Cl₁.₅를 450 °C에서 어닐하면 4d 무질서가 커지고 전도도가 오르며, Li 금속과의 계면 분해도 느려진다. |
| `jang2023_zno_cosubstitution_argyrodite` | Jang et al. 2023 | Preparation of argyrodite Li6–2xZnxPS5−xOxCl with improved electrochemical performance and air stability for all-solid-state batteries | Li₆PS₅Cl에 ZnO로 Zn과 O를 함께 넣으면 CCD와 H₂S 발생은 개선되지만 이온전도도는 조성에 따라 단조 감소한다. |
| `lee2024_multicomponent_argyrodite_mixed_oxidation_mtp` | Lee et al. 2024 | Design of multicomponent argyrodite based on a mixed oxidation state as promising solid-state electrolyte using moment tensor potentials | Li₆PS₅I의 P 자리를 4가와 6가 양이온으로 함께 치환한 조합이 84개 구조 중 가장 높은 계산 전도도를 보였다. |
| `li2024_inf3_argyrodite_ultrathin_film` | Li 2024 | A Versatile InF₃ Substituted Argyrodite Sulfide Electrolyte Toward Ultrathin Films for All-Solid-State Lithium Batteries | InF₃ 공도핑은 σ를 크게 잃지 않고 Li 금속·대기·유기용매 내성을 높였지만, In과 F가 맡는 역할은 축마다 다르다. |
| `liu2024_pband_center_sbo_dual_interface` | Liu et al. 2024 | Regulating p‐Band Center of Sulfur in Li‐Argyrodite to Stabilize Dual Solid–Solid Interface for Robust All‐Solid‐State Lithium–Sulfur Battery | Li₆PS₅Cl에 Sb와 O를 함께 넣어 SbS₄ 사면체를 만들면 S-p 밴드중심이 내려가 Li 금속 쪽과 S₈ 쪽 계면이 동시에 안정해진다고 원문은 주장한다. |
| `ma2024_sb_doping_lpsc_conductivity` | Ma et al. 2024 | High performance P-based argyrodite sulfide electrolytes enabled by Sb-based argyrodite doping for all-solid-state lithium metal batteries | LPSC에 LSSSI를 녹여 Sn·Sb·I를 치환하면 전도도가 오르고 Li 금속 계면과 공기 안정성이 함께 좋아진다. |
| `jang2025_thioarsenate_argyrodite_mlip_mechanism` | Jang et al. 2025 | Mechanistic insights into superionic thioarsenate argyrodite solid electrolytes via machine learning interatomic potentials | Li₆AsS₅Br의 4a/4d 자리반전은 Li 전도도를 크게 올리지만 Ehull도 올려, 원문은 중간 반전의 설계창을 제안한다. |
| `li2025_cubr2_dualdoping_argyrodite` | Li et al. 2025 | Engineering high-performance argyrodite sulfide electrolytes via metal halide doping for all-solid-state lithium metal batteries | Cu가 P 자리를, Br이 4a/4d 자리를 채우면 σ가 10.3 mS/cm로 오르고 Li 계면과 대기 안정성도 좋아진다 |
| `muy2025_li7ps6_dopant_engineering_conductivity` | Muy et al. 2025 | Optimizing Ionic Conductivity of Lithium in Li₇PS₆ Argyrodite via Dopant Engineering | 결함열역학으로 도펀트를 고르고 DeePMD 지도와 합성으로 Cl은 높게, Mg/Si는 낮게라는 처방을 냈다. |
| `rao2025_iodide_argyrodite` | Rao et al. 2025 | Iodide substituted halide-rich lithium argyrodite solid electrolytes with improved performance for all solid-state batteries | Cl-rich 아지로다이트에 I를 넣으면 E_hull이 낮아지고, I/Cl 등량에서 계산 전도도가 23.5 mS/cm로 가장 높다. |
| `yang2025_lao_dualdoping_argyrodite_lacl3` | Yang et al. 2025 | Lanthanum and oxygen co-doping of lithium argyrodite for enhanced humid air stability and lithium metal compatibility | La₂O₃ 공도핑은 σ를 9.58에서 6.23 mS/cm로 낮추지만 습윤공기 안정성과 CCD를 크게 높인다. |
| `park2026_oxygen_induced_li_intercage_conduction` | Park et al. 2026 | Oxygen-induced lithium inter-cage conduction for enhanced performance in all-solid-state batteries | Li₆PS₅Cl에 Li₂SO₄로 O를 넣으면 σ는 조금만 줄고 NCM811 계면 열화가 줄지만, inter-cage 전도 활성화 기전은 근거가 약하다. |
| `wu2026_ta_argyrodite_selfpassivating` | Wu et al. 2026 | High‐Conductivity Argyrodite Electrolyte with Self‐Passivating Stability for Single‐Electrolyte All‐Solid‐State Lithium Batteries | Cl/Br 혼합과 Ta⁵⁺ 치환으로 σ 12 mS/cm를 얻었고, Ta 계면 산물이 실용 창을 0.1 – 4.3 V로 넓혔다. |
| `xu2026_ndo_codoping_argyrodite` | Xu et al. 2026 | High-air-stability lithium superionic conductor with excellent Li-metal compatibility for superior all-solid-state Li batteries | Li₅.₃PS₄.₃Cl₁.₇에 Nd–O를 x=0.025만큼 넣으면 전도도, CCD, 공기 안정성이 함께 오르지만 Nd 자리는 추정에 머문다. |
| `xu2026_offstoich_composite_lpsc_highvoltage` | Xu et al. 2026 | Locally off-stoichiometric composite-phase reconstruction of argyrodite sulfide electrolytes for high-voltage all-solid-state lithium batteries | Li₅.₅PS₄.₅Cl₁.₅ 명목 조성을 480 °C로 구우면 argyrodite 기지, P₂S₆⁴⁻ 2차상, LiCl의 다상이 되고 NCM811 셀 성능이 오른다. |

# SE 입도 효과

전극 미세구조 · 공정 · 장 `dem-size` · 논문 11편 · 읽기 카드 11편

> 전해질 입자 크기와 분포가 충진, 접촉, 전도도에 주는 영향.

## 장 서문 — 작은 SE는 복합양극 접촉을 넓히지만 펠릿 전도도를 잃는다

*읽기 카드 11편을 엮어 쓴 글 · 항목 30개 중 30개 검증 통과 · 2026-11-10*

고체전해질(SE) 입자의 크기와 분포가 충진, 접촉, 이온 전도를 어떻게 바꾸는지가 질문이다. 복합양극에서는 작은 SE가 공극을 줄이고 CAM을 고르게 덮어 이온 전달과 용량을 올린다는 실험과 계산이 여럿 모였다. [근거: Shi et al. 2019 (`shi2019_high_am_loading_particle_size_assb`); Schlautmann et al. 2023 (`schlautmann2023_se_particle_size_composite_transport`); Lin et al. 2025 (`lin2025_submicron_lpscl_cathode_li_kinetics`); Zhou et al. 2025 (`tailored_cathode_microstructure_low_pressure_assb`)]

순수 SE 펠릿에서는 작은 입자가 대체로 σ가 낮다. 그 손해가 크기 자체에서 오는지, 밀링 손상에서 오는지, 분포 폭에서 오는지는 아직 갈리지 않았다. [근거: Ghanshyam et al. 2021 (`yadav2021_lpscl_sieved_psd_impedance_tortuosity`); Schneider et al. 2023 (`schneider2023_particle_size_pressure_transport`); Lin et al. 2025 (`lin2025_submicron_lpscl_cathode_li_kinetics`); Lei et al. 2026 (`lei2026_se_particle_size_effects_review`); Yano et al. 2026 (`yano2026_se_psd_width_ionic_tortuosity_dem`)]

### 순수 SE 펠릿의 σ

같은 원료를 체로만 나눈 실험에서는 큰 등급의 펠릿 σ가 높았다. Ghanshyam et al. 2021은 Li₆PS₅Cl에서 <20 µm 등급 3.96 × 10⁻⁴ S·cm⁻¹, 50–150 µm 등급 1.46 × 10⁻³ S·cm⁻¹을 보고했다. Schneider et al. 2023은 t-Li₇SiPS₈에서 <50µm 4.1 mS/cm, >50µm 5.7 mS/cm를 적었다. 원문은 작은 분율이 더 치밀한데도 σ가 낮은 이유를 많은 grain 간 접촉과 입계 저항으로 해석했다. Faka et al. 2026도 4, 11 µm가 낮고 20, 40 µm가 높은 두 무리를 보였다. [근거: Ghanshyam et al. 2021 (`yadav2021_lpscl_sieved_psd_impedance_tortuosity`); Schneider et al. 2023 (`schneider2023_particle_size_pressure_transport`); Faka et al. 2026 (`faka2026_particle_size_consolidation_strain_lpscl`)]

Schlautmann et al. 2023만은 순수 Li₆PS₅Cl 전도도가 입도에 평평하다고 적었다. S, M, XL이 모두 2.2 mS cm⁻¹였고 XRD, PDF, Raman에서도 차이가 없었다. 원문은 그래서 복합체 차이가 재료가 아니라 미세구조에서 온다고 보았다. 반면 다른 연구들은 등급마다 분포와 치밀도가 함께 달라져 크기 효과만 떼어 볼 수 없다고 검토 측은 본다. [근거: Schlautmann et al. 2023 (`schlautmann2023_se_particle_size_composite_transport`); Ghanshyam et al. 2021 (`yadav2021_lpscl_sieved_psd_impedance_tortuosity`)]

밀링으로 입자를 줄이면 펠릿 σ가 크게 떨어진다. Lin et al. 2025의 습식 밀링 Li₆PS₅Cl은 4.96에서 1.51 mS cm⁻¹로 낮아졌고 활성화 에너지는 0.296에서 0.357 eV로 올랐다. Yano et al. 2026의 볼밀 분말도 원 분말 4.03 × 10⁻³ S/cm보다 낮은 1.45 × 10⁻³ S/cm였다. Lei et al. 2026은 밀링 SE의 σ 하락이 입도 감소와 부분 비정질화만으로 설명되지 않고 불순물과 분해도 기여할 수 있다고 정리했다. [근거: Lin et al. 2025 (`lin2025_submicron_lpscl_cathode_li_kinetics`); Yano et al. 2026 (`yano2026_se_psd_width_ionic_tortuosity_dem`); Lei et al. 2026 (`lei2026_se_particle_size_effects_review`)]

### 복합양극은 어느 쪽

복합양극에서는 작은 SE가 공극을 줄이고 이온 전달을 높인다는 결과가 우세하다. Schlautmann et al. 2023은 무탄소 NCM811 복합체에서 공극률이 S 14.1 %, XL 24.3 %였고 σ_ion,eff가 0.165에서 0.254 mS cm⁻¹로 올랐다고 적었다. Zhou et al. 2025는 미세 LPSC 양극의 FIB-SEM 공극률이 11.3 %에서 4.4 %로, median 굴곡도가 1.84에서 1.21로 낮아졌다고 보고했다. Lin et al. 2025는 펠릿 σ 손해에도 미립 SE 양극의 첫 방전이 175.7에서 197.5 mAh g⁻¹로 올랐다고 적었다. [근거: Schlautmann et al. 2023 (`schlautmann2023_se_particle_size_composite_transport`); Zhou et al. 2025 (`tailored_cathode_microstructure_low_pressure_assb`); Lin et al. 2025 (`lin2025_submicron_lpscl_cathode_li_kinetics`)]

반대 방향의 결과는 크기 척도와 분포 폭이 다른 조건에서 나왔다. Ghanshyam et al. 2021은 50–150 µm 등급 복합양극의 유효 σ가 ~1.12 × 10⁻⁴ S/cm로 <20 µm 등급의 ~2.16 × 10⁻⁵ S/cm보다 높다고 적었지만, 검토 측은 이득의 대부분이 펠릿 σ 차가 넘어온 것이라고 본다. Yano et al. 2026은 거친 꼬리가 있는 원 분말이 볼밀 분말보다 이온 전도가 좋았고 τ_eff가 2.15에서 6.72로 올랐다고 적었다. 검토 측은 이 결과가 PSD 폭이 아니라 밀링하지 않은 분말의 이점과 구분되지 않는다고 본다. 우리 대리 입도는 D50 0.7–3 µm 단분산이라 Ghanshyam et al. 2021의 체 등급과 1–2 자릿수 떨어져 우리 범위의 방향을 검정하지 않는다. [근거: Ghanshyam et al. 2021 (`yadav2021_lpscl_sieved_psd_impedance_tortuosity`); Yano et al. 2026 (`yano2026_se_psd_width_ionic_tortuosity_dem`)]

### 기하와 연결성

강체 구 패킹과 DEM 연결성 모델은 크기비가 충진과 이용률을 정한다고 본다. McGeary 1961은 직경비가 7을 넘어야 미세 구가 조대 구의 간극을 채우고 이성분 최대밀도가 86.0 %로 평탄해진다고 적었다. Shi et al. 2019는 CAM 이용률이 로딩과 λ = D̄_CAM/D̄_SE에 함께 달리고, 75 wt%에서 98 % 이용률에 λ_min=2.1이 필요하다고 계산했다. 85 wt%에서는 λ를 1에서 8로 키워도 θ가 ≈16 %에서 ≈20 %로만 올랐다. Zhou et al. 2025의 DEM은 2 % overlap 기준에서 미세 쪽 CAM utilization 100 %, 거친 쪽 83 %를 냈다. [근거: McGEARY 1961 (`mcgeary1961_bimodal_sphere_packing`); Shi et al. 2019 (`shi2019_high_am_loading_particle_size_assb`); Zhou et al. 2025 (`tailored_cathode_microstructure_low_pressure_assb`)]

접촉 면적과 유효 전도도는 같은 방향으로 움직이지 않을 수 있다. Park et al. 2020은 1D 원기둥 LLZO-Ta가 0D 250 nm보다 접촉면적이 낮아도 유효 이온전도도가 크게 높다고 계산했다. Yano et al. 2026의 DEM에서는 기하 τ가 1.14–1.17로 거의 평평했고 경로당 입자 수만 20.5에서 26.3으로 늘었다. 원문은 큰 입자가 경로의 입계 수를 줄이는 fast-track이 된다고 적었다. 그래서 우리는 coverage와 tau2를 하나로 접지 않고, 경로당 입자 수 N을 우리 수송 지표가 민감하게 반응하는 양으로 본다. [근거: Park et al. 2020 (`park2020_dimension_controlled_se_percolation_contact_area`); Yano et al. 2026 (`yano2026_se_psd_width_ionic_tortuosity_dem`)]

### 압력과 치밀화

입도에 따른 치밀화 방향은 두 연구에서 엇갈린다. Schneider et al. 2023은 작은 분율이 더 치밀하고 Heckel 평균 항복압도 0.95(3) GPa로 큰 분율의 1.65(3) GPa보다 낮다고 적었다. Faka et al. 2026은 같은 Li₆PS₅Cl에서 큰 입자가 1 GPa에서 상대밀도 100 %에 닿고 작은 입자는 1.5 GPa에서도 95 %에 머문다고 보고했다. 소재가 t-Li₇SiPS₈와 Li₆PS₅Cl로 다르고, Faka et al. 2026의 밀도는 장치 순응도 보정이 서술되지 않은 in-die 값이라고 검토 측은 본다. [근거: Schneider et al. 2023 (`schneider2023_particle_size_pressure_transport`); Faka et al. 2026 (`faka2026_particle_size_consolidation_strain_lpscl`)]

압력은 σ와 미세구조 효과의 크기를 함께 바꾼다. Schneider et al. 2023에서 σ는 저압에서 미세구조로 오르고 고압에서 격자압축으로 내려가 ~0.5 GPa 근처에서 최대가 되었다. Faka et al. 2026은 압축 뒤 격자 변형이 4 µm에서 가장 컸고 DEM이 그 원인을 크기 불균일로 돌렸다고 적었다. Zhou et al. 2025에서는 작동압 30 MPa의 유지율 격차가 84.0 대 90.3 %였고 2 MPa에서는 63.3 대 85.6 %로 커졌다. [근거: Schneider et al. 2023 (`schneider2023_particle_size_pressure_transport`); Faka et al. 2026 (`faka2026_particle_size_consolidation_strain_lpscl`); Zhou et al. 2025 (`tailored_cathode_microstructure_low_pressure_assb`)]

### 모델이 빼는 항

이 장의 계산은 대부분 접촉 저항이나 입계 저항을 넣지 않는다. Park et al. 2020은 겹친 복셀의 융합으로 접촉을 처리해 계면 저항 항이 0이고, 검토 측은 σ_eff를 상한 쪽으로 본다. Schlautmann et al. 2023의 GeoDict는 σ_el,eff를 S에서 0.765 mS cm⁻¹로 예측했지만 실측은 0.26–0.41 mS cm⁻¹로 거의 평평했다. Schneider et al. 2023도 FV 시뮬레이션에 입계 저항이 없다고 적었다. Yano et al. 2026은 입자 수 비례 항 α를 0 wt% 실험값에 맞춰 넣었지만 30 wt%에서 τ*가 2.54에 그쳤다. [근거: Park et al. 2020 (`park2020_dimension_controlled_se_percolation_contact_area`); Schlautmann et al. 2023 (`schlautmann2023_se_particle_size_composite_transport`); Schneider et al. 2023 (`schneider2023_particle_size_pressure_transport`); Yano et al. 2026 (`yano2026_se_psd_width_ionic_tortuosity_dem`)]

DEM의 탄성 입력도 연구마다 다르다. Shi et al. 2019와 Faka et al. 2026은 Young률 18.5 GPa를 연화 없이 썼고 Yano et al. 2026은 21 GPa를 썼다. 우리 DEM은 E_eff를 1.35 GPa로 연화해 반대 선택을 했다. Faka et al. 2026은 DEM 밀도를 보고하지 않아 그 선택이 실험 밀도를 재현했는지 판정할 수 없다. [근거: Shi et al. 2019 (`shi2019_high_am_loading_particle_size_assb`); Faka et al. 2026 (`faka2026_particle_size_consolidation_strain_lpscl`); Yano et al. 2026 (`yano2026_se_psd_width_ionic_tortuosity_dem`)]

### 이 장의 값

| 값 | 표기 | 근거 |
|---|---|---|
| 이성분 강체 구 최대밀도 (d_c/d_f ≥ 7) | 86.0 % | McGEARY 1961 (`mcgeary1961_bimodal_sphere_packing`) |
| 98 % 이용률 최소 크기비 (75 wt%) | λ_min=2.1 | Shi et al. 2019 (`shi2019_high_am_loading_particle_size_assb`) |
| 50–150 µm Li₆PS₅Cl 펠릿 σ | 1.46 × 10⁻³ S·cm⁻¹ | Ghanshyam et al. 2021 (`yadav2021_lpscl_sieved_psd_impedance_tortuosity`) |
| S 입도 NCM811 복합체 σ_ion,eff | 0.254 mS cm⁻¹ | Schlautmann et al. 2023 (`schlautmann2023_se_particle_size_composite_transport`) |
| <50µm t-Li₇SiPS₈ 최대 σ | 4.1 mS/cm | Schneider et al. 2023 (`schneider2023_particle_size_pressure_transport`) |
| 습식 밀링 Li₆PS₅Cl 펠릿 σ (25 °C) | 1.51 mS cm⁻¹ | Lin et al. 2025 (`lin2025_submicron_lpscl_cathode_li_kinetics`) |
| 미세 LPSC 양극 2 MPa 100사이클 유지율 | 85.6 % | Zhou et al. 2025 (`tailored_cathode_microstructure_low_pressure_assb`) |
| 작은 입경 Li₆PS₅Cl 1.5 GPa 상대밀도 | 95 % | Faka et al. 2026 (`faka2026_particle_size_consolidation_strain_lpscl`) |

### 아직 열린 문제

- 입도 효과와 밀링 손상을 가른 실험이 없다. Lin et al. 2025에는 같은 크기의 손상 없는 대조군이 없고, Yano et al. 2026에서는 PSD 폭, D50, 밀링 손상, 응집, 상대밀도가 함께 움직였다. Shi et al. 2019의 σ 하락도 밀링 조건이 함께 바뀐 네 점이다. [근거: Lin et al. 2025 (`lin2025_submicron_lpscl_cathode_li_kinetics`); Yano et al. 2026 (`yano2026_se_psd_width_ionic_tortuosity_dem`); Shi et al. 2019 (`shi2019_high_am_loading_particle_size_assb`)]
- 순수 SE 펠릿 σ가 입도에 의존하는지가 엇갈린다. Schlautmann et al. 2023은 평평하다고 보았고, Ghanshyam et al. 2021, Schneider et al. 2023, Faka et al. 2026은 작은 입자에서 낮다고 보았다. [근거: Schlautmann et al. 2023 (`schlautmann2023_se_particle_size_composite_transport`); Ghanshyam et al. 2021 (`yadav2021_lpscl_sieved_psd_impedance_tortuosity`); Schneider et al. 2023 (`schneider2023_particle_size_pressure_transport`); Faka et al. 2026 (`faka2026_particle_size_consolidation_strain_lpscl`)]
- 작은 입자가 더 치밀해지는지가 정해지지 않았다. Schneider et al. 2023과 Faka et al. 2026은 반대 방향을 보였고, Lei et al. 2026은 작을수록 덜 치밀한 냉간 압밀 반례를 다루지 않았다고 검토 측은 본다. [근거: Schneider et al. 2023 (`schneider2023_particle_size_pressure_transport`); Faka et al. 2026 (`faka2026_particle_size_consolidation_strain_lpscl`); Lei et al. 2026 (`lei2026_se_particle_size_effects_review`)]
- 중앙값과 분리한 PSD 폭의 효과는 아직 검증되지 않았다. Yano et al. 2026은 넓은 PSD의 이점을 주장했지만 확실한 신호는 30 wt% 하나이고, 우리 단분산 대리 입도는 거친 꼬리가 만드는 직렬 접촉 수 감소를 담지 못한다. [근거: Yano et al. 2026 (`yano2026_se_psd_width_ionic_tortuosity_dem`)]

### 먼저 읽을 논문

1. Schlautmann et al. 2023 (`schlautmann2023_se_particle_size_composite_transport`) — 같은 Li₆PS₅Cl의 입도만 바꿔 순수 SE와 복합체, 실측과 voxel 계산을 한 논문에서 갈라 보여 장 전체의 기준점이 된다.
2. Shi et al. 2019 (`shi2019_high_am_loading_particle_size_assb`) — 로딩과 크기비 λ로 CAM 이용률을 설명하는 DEM 틀을 세워 이후 논문들이 이 언어로 비교된다.
3. Yano et al. 2026 (`yano2026_se_psd_width_ionic_tortuosity_dem`) — PSD 폭과 경로당 입자 수라는 다른 축을 열고, 기하 τ와 실험 τ의 간극을 직접 다룬다.
4. Ghanshyam et al. 2021 (`yadav2021_lpscl_sieved_psd_impedance_tortuosity`) — 큰 SE 등급이 이긴다는 반대 방향 결과이며 그 이득이 펠릿 σ에서 넘어온 것이라는 검토가 붙어 있다.
5. Schneider et al. 2023 (`schneider2023_particle_size_pressure_transport`) — 압력의 두 영역과 입계 저항 해석을 제시해 펠릿 σ와 밀도가 엇갈리는 이유를 읽게 해 준다.

## 이 장의 논문 (11편)

| digest | 저자 · 연도 | 제목 | 한 줄 결론 |
|---|---|---|---|
| `mcgeary1961_bimodal_sphere_packing` | McGEARY 1961 | Mechanical Packing of Spherical Particles | 진동으로 채운 강체 구의 충전밀도는 재료보다 크기비가 정하고, 직경비가 7을 넘어야 미세 구가 조대 구의 간극을 채운다. |
| `shi2019_high_am_loading_particle_size_assb` | Shi et al. 2019 | High Active Material Loading in All‐Solid‐State Battery Electrode via Particle Size Optimization | 양극 이용률은 CAM 로딩과 입자 크기비 λ에 함께 달리고, 고로딩에서는 SE를 CAM보다 작게 하는 것이 가장 결정적이다. |
| `park2020_dimension_controlled_se_percolation_contact_area` | Park et al. 2020 | Dimension-controlled solid oxide electrolytes for all-solid-state electrodes: Percolation pathways, specific contact area, and effective ionic conductivity | 흑연 음극 가상 전극에서 1D 원기둥 LLZO-Ta는 접촉면적을 잃는 대신 유효 이온전도도를 크게 높여 가장 좋은 성능을 낸다. |
| `yadav2021_lpscl_sieved_psd_impedance_tortuosity` | Ghanshyam et al. 2021 | Impact of Sulfide-based Solid Electrolyte Particle Size Distribution on the Electrochemistry of ASSB via Impedance Study | 같은 Li₆PS₅Cl을 체로 나누면 50–150 µm 등급이 순수 SE와 복합양극 모두에서 이온 전도가 높고 굴곡도가 낮았다. |
| `schlautmann2023_se_particle_size_composite_transport` | Schlautmann et al. 2023 | Impact of the Solid Electrolyte Particle Size Distribution in Sulfide‐Based Solid‐State Battery Composites | Li₆PS₅Cl 입도를 줄이면 무탄소 NCM811 복합양극의 공극이 줄어 이온전도와 용량이 오르지만, 전자전도는 거의 그대로다. |
| `schneider2023_particle_size_pressure_transport` | Schneider et al. 2023 | Effect of Particle Size and Pressure on the Transport Properties of the Fast Ion Conductor t ‐Li₇ SiPS₈ | t-Li₇SiPS₈ 펠릿에서 압력은 저압에서 미세구조로 σ를 올리고 고압에서 격자압축으로 σ를 낮추며, 입도분포가 밀도보다 강한 지표다. |
| `lin2025_submicron_lpscl_cathode_li_kinetics` | Lin et al. 2025 | Sub-micrometer Li₆PS₅Cl regulated cathodic Li kinetics in sulfide based all-solid-state batteries | 습식 밀링으로 D50 2.34 µm가 된 Li₆PS₅Cl은 펠릿 전도도가 떨어져도 NCM811 복합양극의 기공, 용량, 수명을 개선했다. |
| `tailored_cathode_microstructure_low_pressure_assb` | Zhou et al. 2025 | Tailored Cathode Composite Microstructure Enables Long Cycle Life at Low Pressure for All-Solid-State Batteries | LPSC를 ~1 µm로 잘게 만들면 NCM811을 고르게 덮어 2 MPa 작동압에서도 100 사이클 뒤 85.6 %를 유지한다. |
| `faka2026_particle_size_consolidation_strain_lpscl` | Faka et al. 2026 | How Particle Size Affects Consolidation Behavior, Strain and Properties of Li₆PS₅Cl Fast Ionic Conductors | 같은 Li₆PS₅Cl에서 큰 입자는 약 1 GPa에서 상대밀도 100 %에 닿고, 작은 입자는 1.5 GPa에서도 95 %에 머물며, 변형은 크기 불균일에서 온다. |
| `lei2026_se_particle_size_effects_review` | Lei et al. 2026 | Review of Particle Size Effects of Solid Electrolytes in All-Solid-State Batteries | 작은 SE는 충진, 접촉, 기계 강도에 유리하고 큰 SE는 이온전도와 화학 안정성에 유리하다. 모든 수치는 2차 인용이다. |
| `yano2026_se_psd_width_ionic_tortuosity_dem` | Yano et al. 2026 | Effect of size distribution of solid electrolyte on tortuosity of ionic conductive paths: A combined experimental and simulation study | 거친 꼬리가 있는 원 분말 LPSCl은 볼밀 분말보다 복합양극 이온 전도도가 높았다. DEM 기하 τ는 거의 그대로였고 경로당 입자 수만 늘었다. |

# 이온 수송 기구와 확산 해석

전해질 · 계면 · 장 `se-transport` · 논문 19편 · 읽기 카드 19편

> Li 이동 경로와 협동 운동, 그리고 MD에서 확산계수와 전도도를 믿을 수 있게 구하는 방법.

## 장 서문 — 음이온 무질서와 협동 운동이 Li 장거리 전도를 연다

*읽기 카드 19편을 엮어 쓴 글 · 항목 30개 중 30개 검증 통과 · 2026-11-10*

이 장에는 두 질문이 있다. 첫째는 아지로다이트 같은 황화물 고체전해질에서 Li가 어떤 경로로 멀리 이동하는가이다. 둘째는 MD 궤적에서 확산계수와 전도도를 어떻게 믿을 만하게 뽑는가이다. [근거: Rao · Adams 2011 (`rao2011_argyrodite_se_studies_bvse`); Morgan 2021 (`morgan2021_anion_disorder_superionic_mechanism_li6ps5x`); Marcolongo · Marzari (`marcolongo_ionic_correlations_failure_nernst_einstein`); He et al. 2018 (`he2018_statistical_variances_diffusional_aimd`); Maginn et al. 2019 (`maginn2019_best_practices_transport_selfdiffusivity_viscosity`)]

기전 쪽에서는 cage 사이 연결이 dc 전도를 율속하고, 4a·4c 음이온 자리의 무질서가 그 연결을 연다는 데 여러 계산이 모인다. [근거: Rao · Adams 2011 (`rao2011_argyrodite_se_studies_bvse`); Morgan 2021 (`morgan2021_anion_disorder_superionic_mechanism_li6ps5x`); Kim et al. 2024 (`kim2024_mtp_argyrodite_disorder_gb`); Liang et al. 2025 (`liang2025_quasilayered_argyrodite_li_migration`); Ou et al. 2026 (`ou2026_microstructural_multiscale_fast_ion_transport`)]

Haven 비의 크기와 부호, 회전 음이온의 인과, 계산 전도도의 절대값은 아직 논문마다 조건이 달라 하나로 정해지지 않았다. [근거: Marcolongo · Marzari (`marcolongo_ionic_correlations_failure_nernst_einstein`); Jeon et al. 2026 (`jeon2026_concerted_li_motion_argyrodite_assi`); Fang · Jena 2022 (`fang2022_argyrodite_transport_beyond_paddlewheel`); Shin et al. 2026 (`shin2026_bh4_reorientation_li_transport_li6ps5x`); Ohno et al. 2020 (`ohno2020_interlab_ionic_conductivity_argyrodite`); Zaby et al. 2026 (`zaby2026_reliable_conductivity_estimates_md`)]

### 장거리 경로를 여는 것

장거리 확산을 막는 것은 cage 안의 짧은 hop이 아니라 cage 사이를 잇는 연결이다. Rao·Adams 2011은 bond-valence 경로 분석에서 세 할라이드 모두 cage 간 연결의 장벽이 가장 높다고 보았다. Li₆PS₅Cl의 cage 간 장벽은 0.35 eV였다. 원문은 I가 느린 이유를 장벽 높이가 아니라 경로 위상과 자리 연결성으로 돌렸다. Dyre 2004는 장벽 분포가 넓을 때 percolation cluster 위의 가장 큰 병목 장벽이 dc 활성화에너지가 된다고 보였고, 검토 측은 이 모델에서 수치가 아니라 병목 개념만 결정질로 옮길 수 있다고 본다. [근거: Rao · Adams 2011 (`rao2011_argyrodite_se_studies_bvse`); Dyre 2004 (`dyre2004_hopping_models_ion_conduction_noncrystals`)]

4a·4c 음이온 자리의 S/X 무질서가 그 연결을 연다는 데 여러 계산이 모인다. Morgan 2021은 자리반전 50 % 배열만 장거리 확산을 보였다고 적었다. 정렬 배열에서는 특정 자리 사이 전이가 끊겨 Li가 닫힌 궤도에 갇힌다. Kim et al. 2024의 MTP 계산에서는 ordered와 disordered의 σ가 3–4자릿수 벌어졌다. Ou et al. 2026은 무질서가 벌크 장벽을 168.0 meV 낮춘다고 적었다. Ishikawa et al. 2025는 무작위 치환 모델에서 Li 자리가 침투망을 이루는 x 0.2 부근에서 전도도가 급등한다고 적었으나, 원문 스스로 일반 rock-salt에서는 이 문턱이 어긋날 수 있다고 밝혔다. Jeon et al. 2026은 음이온 정렬 상태인 Li₆₊ₓAs₁₋ₓSiₓS₅I에서 다른 기전을 적었는데, Si 치환이 폴리음이온 S를 전자 부화시켜 케이지간 점프 빈도를 높인다는 것이다. [근거: Morgan 2021 (`morgan2021_anion_disorder_superionic_mechanism_li6ps5x`); Kim et al. 2024 (`kim2024_mtp_argyrodite_disorder_gb`); Ou et al. 2026 (`ou2026_microstructural_multiscale_fast_ion_transport`); Ishikawa et al. 2025 (`ishikawa2025_site_percolation_cooperative_ion_conduction`); Jeon et al. 2026 (`jeon2026_concerted_li_motion_argyrodite_assi`)]

### 협동 운동과 Haven 비

tracer 확산계수를 넣은 Nernst–Einstein 식이 맞는지는 계에 따라 답이 갈린다. Marcolongo·Marzari는 LGPS Car–Parrinello MD에서 골격 역류를 뺀 Haven 비가 등방 평균 0.42라고 적었다. 이 값은 1보다 작으므로 원문은 NE 식이 σ를 과소평가한다고 보았다. 두 경로의 활성화에너지는 오차 안에서 같아, 원문은 상관이 전치인자에만 들어간다고 결론지었다. Lynch 2026의 산화물 MLIP-MD에서도 개별 모델 Haven 비가 0.53 ~ 1.03이었다. 반대로 Zaby et al. 2026의 두 액체계에서는 cross 항이 음수여서 NE가 참 σ를 1.3–2.1× 과대평가했다. [근거: Marcolongo · Marzari (`marcolongo_ionic_correlations_failure_nernst_einstein`); D. Cory Lynch 2026 (`lynch2026_greenkubo_mlip_conductivity_thesis`); Zaby et al. 2026 (`zaby2026_reliable_conductivity_estimates_md`)]

아지로다이트 계열의 Haven 비는 아직 단일 궤적이나 단일 온도에서 나온 값뿐이다. Jeon et al. 2026은 x=0에서 1.83, x=0.25–0.75에서 0.53–0.77을 보고했다. 검토 측은 이 값에 오차막대가 없고 x=0의 집단 MSD가 확산 거동이 아니라고 본다. Fang·Jena 2022가 적은 Haven 비 역수 1.3과 1.5도 온도와 오차 없이 클러스터 계 두 개에서만 나왔다. Morgan 2021은 확산하지 않는 정렬계에도 협동 운동이 있고, 확산을 가르는 것은 끈 길이 분포의 모양이라고 적었다. [근거: Jeon et al. 2026 (`jeon2026_concerted_li_motion_argyrodite_assi`); Fang · Jena 2022 (`fang2022_argyrodite_transport_beyond_paddlewheel`); Morgan 2021 (`morgan2021_anion_disorder_superionic_mechanism_li6ps5x`)]

### 회전 음이온의 역할

다원자 음이온의 회전이 Li 수송을 이끄는지를 두고 두 논문이 엇갈린다. Fang·Jena 2022는 SH⁻·BH₄⁻ 치환 계에서 회전이 Li 변위 뒤나 도중에 나타나므로 원인이 아니라 반응이라고 적었다. 검토 측은 이 판정이 상호상관이나 통계 검정 없이 시계열을 눈으로 본 데 기대고, 회전을 구속한 개입 실험도 없다고 본다. Shin et al. 2026은 회전을 구속한 AIMD에서 500 K Li⁺ 확산계수가 2.0 – 3.0배 줄었다고 보고했다. 검토 측은 Shin et al. 2026에서도 회전의 기여는 측정됐지만, 전도도 향상의 주 원인이라는 주장은 기여도 분해가 없어 측정되지 않았다고 본다. [근거: Fang · Jena 2022 (`fang2022_argyrodite_transport_beyond_paddlewheel`); Shin et al. 2026 (`shin2026_bh4_reorientation_li_transport_li6ps5x`)]

PS₄³⁻의 움직임은 배열보다 부차적인 요인으로 다뤄진다. Kim et al. 2024는 600 K에서 PS₄를 고정하면 disordered 배열의 D가 −50% 줄었다고 적었다. 그래도 고정한 disordered가 ordered보다 빨라서, 원문은 확산 순위를 정하는 것이 배열이라고 보았다. Shin et al. 2026의 AIMD에서 PS₄³⁻는 자리에서 작게 흔들릴 뿐 회전하지 않았고, ³¹P SLR 활성화에너지는 0.16–0.18 eV로 시료와 무관했다. [근거: Kim et al. 2024 (`kim2024_mtp_argyrodite_disorder_gb`); Shin et al. 2026 (`shin2026_bh4_reorientation_li_transport_li6ps5x`)]

### 확산계수의 오차와 창

D의 오차는 MSD 직선 회귀가 아니라 독립 표본의 산포에서 내야 한다는 데 방법론 논문들이 모인다. Pranami·Lamm 2015는 개별 제곱변위가 정규성과 등분산성을 어겨 회귀 오차를 쓸 수 없다고 보였다. Maginn et al. 2019는 복제 런 부트스트랩을 권했고, 이 방법이 N_reps ≥ 20일 때 가장 신뢰할 만하다고 적었다. Zaby et al. 2026에서는 단일 궤적을 토막내 얻은 표준오차가 1.33–1.52× 과소였다. McCluskey et al. 2025는 해석적 공분산 Σ′과 베이지안 회귀로 궤적 하나에서 오차막대를 얻었고, OLS는 중심값은 같지만 자기 오차막대를 크게 과소평가한다고 보였다. [근거: Pranami · Lamm 2015 (`pranami2015_estimating_error_diffusion_coefficients_md`); Maginn et al. 2019 (`maginn2019_best_practices_transport_selfdiffusivity_viscosity`); Zaby et al. 2026 (`zaby2026_reliable_conductivity_estimates_md`); McCluskey et al. 2025 (`mccluskey2025_accurate_diffusion_coefficients_uncertainties`)]

홉 수가 적은 AIMD에서는 유효 홉 수가 통계 오차를 정하고, 적합창과 점 선택이 값 자체를 흔든다. He et al. 2018은 RSD = 3.43/√N_eff + 0.04라는 경험식을 냈고, 검토 측은 이 식을 통계 바닥으로 보며 큰 N_eff에서는 낙관적이라고 본다. 같은 논문에서 LGPS의 Ea는 두 온도 점을 빼자 0.21 ± 0.01에서 0.26 ± 0.02 eV로 바뀌었다. Zaby et al. 2026의 액체계에서 MSD 후반부 고정 적합은 σ를 최대 2.8× 낮췄다. Maginn et al. 2019는 중간 구간을 정하는 객관적 방법을 모른다고 밝히고 선택 방법과 변동폭을 보고하라고 요구했으며, 우리 생산 MD의 Langevin NVT 결합시간 약 0.51 ps는 이 문헌이 D를 극적으로 낮춘다고 경고한 강한 결합 대역에 든다. [근거: He et al. 2018 (`he2018_statistical_variances_diffusional_aimd`); Zaby et al. 2026 (`zaby2026_reliable_conductivity_estimates_md`); Maginn et al. 2019 (`maginn2019_best_practices_transport_selfdiffusivity_viscosity`)]

### 계산과 실험의 거리

실험 전도도 자체가 넓게 흩어져 있어 계산값을 맞댈 기준점이 하나로 서지 않는다. Ohno et al. 2020에서 같은 배치의 Li₆PS₅Cl을 여덟 데이터셋이 재자 σ₂₅가 0.44–2.98 mS cm⁻¹로 흩어졌다. Ea는 0.342–0.456 eV로 덜 흩어졌다. 최댓값은 측정 중 315 MPa로 누른 연구실에서 나왔지만, 검토 측은 여덟 연구실로는 압력의 인과를 가를 수 없다고 본다. Rao·Adams 2011의 결정질 Li₆PS₅Cl 값은 1.9 × 10⁻³ S/cm였다. [근거: Ohno et al. 2020 (`ohno2020_interlab_ionic_conductivity_argyrodite`); Rao · Adams 2011 (`rao2011_argyrodite_se_studies_bvse`)]

계산 전도도의 절대값은 functional, 보정식, 외삽에 크게 매여 있다. Kim et al. 2024에서 같은 스냅샷으로 학습한 MTP의 σ80%bulk는 optB88-vdw에서 2.46, PBE-D3(BJ)에서 0.55였다. 검토 측은 이 결정화도 보정이 경험식이라 개념만 쓰라고 본다. Fang·Jena 2022의 계산 전도도도 같은 방법 계보가 양론 Li₆PS₅Cl을 실험보다 훨씬 낮게 보므로 실험 예측으로 읽을 수 없다고 검토 측은 본다. Ou et al. 2026의 예측 29.47 mS/cm는 QENS와 가깝고 EIS보다 높았으며, 원문은 이를 입도별 상한이라 부르고 µm 입도에서는 입계 효과가 거의 사라진다고 적었다. [근거: Kim et al. 2024 (`kim2024_mtp_argyrodite_disorder_gb`); Fang · Jena 2022 (`fang2022_argyrodite_transport_beyond_paddlewheel`); Ou et al. 2026 (`ou2026_microstructural_multiscale_fast_ion_transport`)]

### 이 장의 값

| 값 | 표기 | 근거 |
|---|---|---|
| LGPS Haven 비, 등방 평균 | 0.42 | Marcolongo · Marzari (`marcolongo_ionic_correlations_failure_nernst_einstein`) |
| 같은 배치 Li₆PS₅Cl σ₂₅ 범위 | 0.44–2.98 mS cm⁻¹ | Ohno et al. 2020 (`ohno2020_interlab_ionic_conductivity_argyrodite`) |
| 결정질 Li₆PS₅Cl 전도도 | 1.9 × 10⁻³ S/cm | Rao · Adams 2011 (`rao2011_argyrodite_se_studies_bvse`) |
| AIMD D의 RSD 경험식 계수 | A = 3.43, B = 0.04 | He et al. 2018 (`he2018_statistical_variances_diffusional_aimd`) |
| 액체계 NE의 참 σ 과대평가 배율 | 1.3–2.1× | Zaby et al. 2026 (`zaby2026_reliable_conductivity_estimates_md`) |
| Li₆₊ₓAs₁₋ₓSiₓS₅I Haven 비 | 1.83 (x=0) / 0.53–0.77 | Jeon et al. 2026 (`jeon2026_concerted_li_motion_argyrodite_assi`) |
| BH₄⁻ 회전 구속 시 Li D 감소 | 2.0 – 3.0배 | Shin et al. 2026 (`shin2026_bh4_reorientation_li_transport_li6ps5x`) |
| 무질서 Li₆PS₅Cl 입계/벌크 D 비 | 0.44× | Ou et al. 2026 (`ou2026_microstructural_multiscale_fast_ion_transport`) |

### 아직 열린 문제

- 아지로다이트의 Haven 비가 1보다 작은지, 크기가 얼마인지는 정해지지 않았다. 지금 있는 값은 단일 궤적이나 단일 온도에서 오차 없이 나왔고, 액체계 결과는 반대 방향이다. 검토 측은 Langevin 열욕이 늦게 쌓이는 교차상관을 감쇠시켜 우리 gen1 H_R 0.84가 1 쪽으로 치우쳤을 수 있다고 보고, NVE 생산 세그먼트로 확인하자고 제안한다. [근거: Jeon et al. 2026 (`jeon2026_concerted_li_motion_argyrodite_assi`); Fang · Jena 2022 (`fang2022_argyrodite_transport_beyond_paddlewheel`); Zaby et al. 2026 (`zaby2026_reliable_conductivity_estimates_md`); Marcolongo · Marzari (`marcolongo_ionic_correlations_failure_nernst_einstein`)]
- BH₄⁻ 회전이 전도도 향상의 주 원인인지는 가려지지 않았다. 한쪽은 회전을 반응으로 보고, 다른 쪽은 구속 실험에서 D가 줄었다고 보고하지만 기여도 분해는 어느 쪽에도 없다. [근거: Fang · Jena 2022 (`fang2022_argyrodite_transport_beyond_paddlewheel`); Shin et al. 2026 (`shin2026_bh4_reorientation_li_transport_li6ps5x`)]
- 무질서 배열을 바꿀 때 D와 Ea가 얼마나 흔들리는지는 비어 있다. 기전 논문들은 무질서 수준마다 배열을 하나씩만 썼다. 우리 시드도 초기 속도와 Langevin 잡음만 바꾸므로 배열에서 오는 분산을 잡지 못한다. [근거: Morgan 2021 (`morgan2021_anion_disorder_superionic_mechanism_li6ps5x`); Ishikawa et al. 2025 (`ishikawa2025_site_percolation_cooperative_ion_conduction`); Kim et al. 2024 (`kim2024_mtp_argyrodite_disorder_gb`); Pranami · Lamm 2015 (`pranami2015_estimating_error_diffusion_coefficients_md`); Zaby et al. 2026 (`zaby2026_reliable_conductivity_estimates_md`)]
- MSD 적합창의 상한을 정하는 공통 기준은 없다. 0.7 t_tot 규칙은 검토 측이 보편 문턱이 아니라고 보며, 우리 2–50 ps 창의 상한 50 ps는 Marcolongo·Marzari가 다루지 않는다. [근거: He et al. 2018 (`he2018_statistical_variances_diffusional_aimd`); Maginn et al. 2019 (`maginn2019_best_practices_transport_selfdiffusivity_viscosity`); Marcolongo · Marzari (`marcolongo_ionic_correlations_failure_nernst_einstein`)]

### 먼저 읽을 논문

1. Marcolongo · Marzari (`marcolongo_ionic_correlations_failure_nernst_einstein`) — tracer와 전하 확산계수의 차이, Haven 비, 골격 역류 보정을 한 번에 정의해 이 장의 협동 운동 논의의 기준이 된다.
2. Morgan 2021 (`morgan2021_anion_disorder_superionic_mechanism_li6ps5x`) — 음이온 무질서가 Li 장거리 확산을 여는 기전을 자리 전이와 끈 분석으로 보여 주는 중심 기전 논문이다.
3. He et al. 2018 (`he2018_statistical_variances_diffusional_aimd`) — AIMD 확산계수의 오차를 유효 홉 수로 정량하고 적합창 규칙을 내어 이후 방법론 카드의 출발점이 된다.
4. Ohno et al. 2020 (`ohno2020_interlab_ionic_conductivity_argyrodite`) — 같은 시료의 실험 전도도가 얼마나 흩어지는지 보여 주어 계산값을 실험과 맞댈 때의 기준을 정한다.
5. Zaby et al. 2026 (`zaby2026_reliable_conductivity_estimates_md`) — replica, 적합창, NE 식의 실패 모드를 실측으로 정리해 실무 점검표 역할을 한다.

## 이 장의 논문 (19편)

| digest | 저자 · 연도 | 제목 | 한 줄 결론 |
|---|---|---|---|
| `marcolongo_ionic_correlations_failure_nernst_einstein` | Marcolongo · Marzari | Ionic correlations and failure of Nernst-Einstein relation in solid-state electrolytes | LGPS에서 Li끼리의 속도 상관으로 D_σ가 D_tr보다 커서 tracer 기반 NE 식은 σ를 과소평가하지만 Ea는 두 경로가 같다. |
| `dyre2004_hopping_models_ion_conduction_noncrystals` | Dyre 2004 | Hopping models for ion conduction in noncrystals | 장벽만 무질서한 random barrier model 하나로 무질서 고체 이온 전도의 네 가지 보편 사실이 percolation에서 함께 설명된다. |
| `rao2011_argyrodite_se_studies_bvse` | Rao · Adams 2011 | Studies of lithium argyrodite solid electrolytes for all‐solid‐state batteries | 짧은 밀링과 어닐로 만든 Li₆PS₅Cl, Li₆PS₅Br은 10⁻³ S/cm급이고 I만 3–4 자릿수 낮으며, dc 전도는 cage 간 hop이 율속한다. |
| `pranami2015_estimating_error_diffusion_coefficients_md` | Pranami · Lamm 2015 | Estimating Error in Diffusion Coefficients Derived from Molecular Dynamics Simulations | MSD 회귀가 주는 오차는 가정 위반으로 무효다. 겹치지 않는 시간원점과 여러 독립 시뮬레이션의 D 표본으로 t-분포 신뢰구간을 내야 한다. |
| `deklerk2018_diffusion_analysis_md_beta_li3ps4` | de Klerk et al. 2018 | Analysis of Diffusion in Solid-State Electrolytes through MD Simulations, Improvement of the Li-Ion Conductivity in β-Li3PS4 as an Example | MD 궤적 하나에서 점프별 활성화에너지를 뽑아 β-Li₃PS₄의 율속 점프를 찾았고, Li 공공으로 그 점프를 여는 처방을 냈다. |
| `he2018_statistical_variances_diffusional_aimd` | He et al. 2018 | Statistical variances of diffusional properties from ab initio molecular dynamics simulations | AIMD 확산계수의 상대표준편차는 적합의 R²가 아니라 유효 홉 수 N_eff가 정하며, RSD = 3.43/√N_eff + 0.04로 쓸 수 있다. |
| `maginn2019_best_practices_transport_selfdiffusivity_viscosity` | Maginn et al. 2019 | Best Practices for Computing Transport Properties 1. Self-Diffusivity and Viscosity from Equilibrium Molecular Dynamics [Article v1.0] | D와 η의 EMD 계산은 표집 설계, 복제 부트스트랩, 적합 구간 선택의 보고를 갖출 때 재현 가능해진다. |
| `ohno2020_interlab_ionic_conductivity_argyrodite` | Ohno et al. 2020 | How Certain Are the Reported Ionic Conductivities of Thiophosphate-Based Solid Electrolytes? An Interlaboratory Study | 한 배치를 여덟 데이터셋이 재자 Li₆PS₅Cl의 σ₂₅는 0.44–2.98 mS cm⁻¹로 흩어졌고 Ea는 훨씬 덜 흩어졌다. |
| `morgan2021_anion_disorder_superionic_mechanism_li6ps5x` | Morgan 2021 | Mechanistic Origin of Superionic Lithium Diffusion in Anion-Disordered Li₆PS₅X Argyrodites | Li₆PS₅X의 빠른 Li 확산은 할로겐 종류가 아니라 4a·4c 자리의 S/X 무질서에서 온다고 원문은 적었다. |
| `fang2022_argyrodite_transport_beyond_paddlewheel` | Fang · Jena 2022 | Argyrodite-type advanced lithium conductors and transport mechanisms beyond paddle-wheel effect | SH⁻·BH₄⁻를 할로겐 자리에 넣은 argyrodite의 고전도는 paddle-wheel이 아니라 Li–Li 릴레이와 클러스터의 반응 이완에서 온다고 원문은 주장한다. |
| `kim2024_mtp_argyrodite_disorder_gb` | Kim et al. 2024 | Highly reliable and large-scale simulations of promising argyrodite solid-state electrolytes using a machine-learned moment tensor potential | optB88-vdw로 학습한 MTP가 자리 무질서에 따른 전도도를 재현했고, 입계에서는 Li이 정전기적으로 쌓여 확산이 느려진다. |
| `ishikawa2025_site_percolation_cooperative_ion_conduction` | Ishikawa et al. 2025 | Cooperative ion conduction enabled by site percolation in random substitutional crystals | 무질서 치환 결정의 장거리 이온전도는 운반이온 자리 침투망 위의 협동 밀어내기가 맡고, 그 문턱은 격자의 site-percolation 임계와 같다. |
| `liang2025_quasilayered_argyrodite_li_migration` | Liang et al. 2025 | Unraveling Lithium‐Ion Migration Mechanisms in Novel Quasi‐Layered Argyrodite Solid Electrolyte for All‐Solid‐State Battery | 4a/4c 음이온 자리 50% 무질서가 만든 준층상 골격에서 약하게 결합한 4c 할라이드가 Li를 놓아주어 층별로 다른 전도가 생긴다. |
| `mccluskey2025_accurate_diffusion_coefficients_uncertainties` | McCluskey et al. 2025 | Accurate Estimation of Diffusion Coefficients and their Uncertainties from Computer Simulation | 자유확산의 해석적 공분산 Σ′과 베이지안 회귀를 쓰면 복제 궤적 없이 GLS급 정밀도의 D*와 오차막대를 얻는다. |
| `jeon2026_concerted_li_motion_argyrodite_assi` | Jeon et al. 2026 | Unraveling the concerted motion of Li ions in argyrodite Li 6+ x As 1− x Si x S₅I solid electrolytes | Si가 폴리음이온 S를 전자 부화시켜 케이지간 협동 점프 빈도를 높이고, 협동의 양상은 조성과 무관하다. |
| `lynch2026_greenkubo_mlip_conductivity_thesis` | D. Cory Lynch 2026 | A Computational Investigation of Solid Electrolyte Materials Using First Principles and Machine Learning Methodologies | Allegro MLIP-MD로 full Green-Kubo 전도도를 구하니 Haven 비가 1보다 작았고, tracer 근사만으로는 부족했다. |
| `ou2026_microstructural_multiscale_fast_ion_transport` | Ou et al. 2026 | Microstructural insights into fast ion transport in solid electrolytes via multiscale modeling | 아지로다이트 입계는 느린 질서 Li₆PS₅I의 확산을 크게 높이고 빠른 무질서 Li₆PS₅Cl은 조금 늦추며, µm 입도에서는 그 효과가 거의 사라진다. |
| `shin2026_bh4_reorientation_li_transport_li6ps5x` | Shin et al. 2026 | Enhancing Li⁺ Ion Transport via Dynamic Coupling With Borohydride Reorientation in Li₆PS₅X Argyrodites | Li₆PS₅X의 4a·4d 자리에 넣은 BH₄⁻의 회전이 Li⁺ 수송에 기여함을 NMR과 AIMD로 보였으나, 주 원인인지는 가려지지 않았다. |
| `zaby2026_reliable_conductivity_estimates_md` | Zaby et al. 2026 | Lessons Learned on Obtaining Reliable Conductivity Estimates From Molecular Dynamics Simulations | Nernst–Einstein은 집단 σ를 과대평가하고, 단일 궤적 분할은 오차를, MSD 후반부 적합은 값을 과소평가한다. |

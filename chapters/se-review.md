# 분야 지도와 리뷰

전해질 · 계면 · 장 `se-review` · 논문 17편 · 읽기 카드 17편

> 분야 전체를 한 번에 잡는 리뷰와 필독 문헌.

## 장 서문 — 고체전해질의 병목은 전도도에서 계면으로 옮겨 갔다

*읽기 카드 17편을 엮어 쓴 글 · 항목 30개 중 30개 검증 통과 · 2026-11-10*

고체전해질 연구의 병목이 bulk 전도도에서 계면과 역학으로 옮겨 갔다는 판단에 리뷰들이 모인다. [근거: Famprikis et al. 2019 (`famprikis2019_fundamentals_inorganic_sse`); Xiao et al. 2020 (`xiao2020_interface_stability_ssb_review`); Kim et al. 2021 (`kim2021_review_oxide_sulfide_se_interfaces`); Liang et al. 2026 (`liang2026_interface_bottleneck_solid_state_batteries`)]

황화물의 열역학 창이 좁고, 그런데도 셀이 작동하는 것은 분해산물 계면층 덕이라는 그림도 널리 공유된다. [근거: Nolan et al. 2018 (`nolan2018_computation_accelerated_design_review`); Xiao et al. 2020 (`xiao2020_interface_stability_ssb_review`); Fan 2026 (`fan2026_sulfide_assb_stability_review_ECERD2600097`)]

세 가지는 아직 갈린다. 계산 창을 하한으로 읽을지, 열역학 판정이 부동태와 속도까지 말해 주는지, argyrodite 전도도 보고값을 어떻게 맞출지다. [근거: Dutra et al. 2025 (`dutra2025_atomistic_modelling_ml_se_review`); Wu et al. 2026 (`wu2026_ml_driven_electrolyte_interface_design_review`); He et al. 2023 (`he2023_halogen_chemistry_solid_electrolytes`); Nosrati et al. 2026 (`nosrati2026_anion_engineering_sulfide_se_review`)]

### 병목은 어디로 갔나

bulk 전도도가 더는 주된 병목이 아니라는 판단이 2019년 이후 리뷰들에 공통으로 깔려 있다. Famprikis et al. 2019는 상온 Li⁺ 전도도가 10 mS/cm 수준에 이르러 액체 전해질과 대등하다고 적었다. Kim et al. 2021은 황화물 최대 전도도로 25 mS/cm를 들었다. 그러면서도 인용한 β-Li3PS4 셀의 전체 저항 350–450 Ω cm²가 상용 LIB의 10–25 Ω cm²보다 아직 한 자릿수 이상 크다고 정리했다. Xiao et al. 2020과 Liang et al. 2026도 남은 병목을 계면으로 본다. [근거: Famprikis et al. 2019 (`famprikis2019_fundamentals_inorganic_sse`); Kim et al. 2021 (`kim2021_review_oxide_sulfide_se_interfaces`); Xiao et al. 2020 (`xiao2020_interface_stability_ssb_review`); Liang et al. 2026 (`liang2026_interface_bottleneck_solid_state_batteries`)]

에너지 이득을 주는 Li 금속 음극이 역학 문제를 함께 끌고 온다. Janek·Zeier 2016은 큰 에너지 이득이 Li 금속 음극에서만 나온다고 어림했다. Famprikis et al. 2019는 대부분의 무기 Li 고체전해질에서 임계전류밀도가 0.3 mA/cm² 이하이고 목표는 3–10 mA/cm²라고 적었다. Monroe–Newman 기준이 무기 고체전해질의 덴드라이트를 설명하지 못한다는 판단은 Famprikis et al. 2019, Kim et al. 2021, Alharbi 2026이 함께 한다. Alharbi 2026은 LLZO도 0.05–0.9 mA cm⁻²에서 실패한다는 보고를 근거로 들어, 전단 탄성률 대신 풀셀 CCD를 1차 서술자로 쓰자고 한다. [근거: Janek · Zeier 2016 (`janek2016_solid_future_battery_development`); Famprikis et al. 2019 (`famprikis2019_fundamentals_inorganic_sse`); Kim et al. 2021 (`kim2021_review_oxide_sulfide_se_interfaces`); Alharbi 2026 (`alharbi2026_coupled_design_ultrathin_composite_se_review`)]

### 창은 얼마나 넓나

계산 열역학 창으로 보면 황화물 전해질은 좁은 전위 구간에서만 안정하다. Nolan et al. 2018은 Li₃PS₄, Li₇P₃S₁₁, Li₆PS₅Cl이 1.7 V에서 환원되고 2.4 V에서 산화된다고 정리했다. Kim et al. 2021의 표는 Li₆PS₅Cl이 2.01 V에서 Li₃PS₄, S, LiCl로 산화 분해한다고 적었고, Bai et al. 2020도 같은 산물을 인용했다. Nolan et al. 2018과 Xiao et al. 2020은 CV로 보고된 넓은 창을 반응면적이 작은 전극 배치가 만든 결과로 보고, 탄소를 섞은 복합전극을 처방으로 낸다. 이 값들은 모두 2차 인용이고, 같은 물질에도 hull 세대가 다른 값이 나란히 실린다. [근거: Nolan et al. 2018 (`nolan2018_computation_accelerated_design_review`); Kim et al. 2021 (`kim2021_review_oxide_sulfide_se_interfaces`); Bai et al. 2020 (`bai2020_argyrodite_review_progress`); Xiao et al. 2020 (`xiao2020_interface_stability_ssb_review`)]

좁은 계산 창을 어떻게 읽을지에서 리뷰들이 갈린다. Xiao et al. 2020은 grand-potential 창을 동역학 안정화가 없는 최악 시나리오로, topotactic 추출을 최선 시나리오로 둔다. 실험값은 그 사이에 떨어져야 한다는 것이 원문의 기본 문법이다. Dutra et al. 2025는 Schwietert 2020을 따라, 분해가 간접 경로를 거치므로 hull 기반 창이 관측을 과소평가할 수 있다고 적었다. Nosrati et al. 2026은 O와 할라이드가 VBM을 낮춰 창을 넓힌다고 설명했지만, 검토 측은 S가 남는 한 argyrodite의 VBM이 S 3p라고 보고, 우리 계산에서도 comp1과 modelc의 산화 onset이 모두 2.256 V이고 VBM이 S 3p라 그 서술과 맞지 않는다. [근거: Xiao et al. 2020 (`xiao2020_interface_stability_ssb_review`); Dutra et al. 2025 (`dutra2025_atomistic_modelling_ml_se_review`); Nosrati et al. 2026 (`nosrati2026_anion_engineering_sulfide_se_review`)]

### 계면상의 전자 성격

Li 금속 쪽 계면은 분해산물이 전자를 막느냐에서 운명이 갈린다는 분류가 여러 리뷰에 공유된다. Nolan et al. 2018, Xiao et al. 2020, Miao et al. 2023은 계면을 세 유형으로 나눈다. 본질적 안정 계면, 이온과 전자를 모두 통하는 혼합전도 계면상(MCI), 이온만 통하는 SEI다. Famprikis et al. 2019도 계속 자라는 MCI를 최악으로 분류한다. He et al. 2023은 Li₃MX₆ 할라이드가 M⁰로 환원되어 MCI가 자라는 반면, Li₆PS₅X는 Li₂S, LiCl, Li₃P로 다단 분해해 자기제한 SEI를 만든다고 갈랐다. Fan 2026은 SEI 안에서도 밴드갭이 좁은 산물로 전자가 스며 dead Li이 생긴다고 적었다. [근거: Nolan et al. 2018 (`nolan2018_computation_accelerated_design_review`); Xiao et al. 2020 (`xiao2020_interface_stability_ssb_review`); Miao et al. 2023 (`miao2023_role_of_interfaces_solid_state_batteries`); Famprikis et al. 2019 (`famprikis2019_fundamentals_inorganic_sse`); He et al. 2023 (`he2023_halogen_chemistry_solid_electrolytes`); Fan 2026 (`fan2026_sulfide_assb_stability_review_ECERD2600097`)]

양극 쪽에서는 황화물이 산화물 양극과 발열 반응한다는 계산이 반복해 인용된다. Xiao et al. 2020은 S와 O 교환과 Li₃PO₄ 형성으로 >300 meV/atom의 구동력이 생긴다고 정리했다. Nolan et al. 2018은 Li₃PS₄와 LiCoO₂의 닫힌계 ΔH_D를 −0.41 eV/atom으로 인용하고, 코팅의 역할을 계면 분해 억제로 다시 해석했다. 검토 측은 코팅 창이 양극에 안정하다는 Nolan et al. 2018의 문장이 자기 Fig. 11B와 어긋난다고 본다. Wang et al. 2025가 소개한 코팅 게이트 ΔE_rxt ≥ −0.1 eV/atom에 대면 우리 comp1|LiCoO₂ 반응에너지 −0.3227 eV/atom은 탈락이다. [근거: Xiao et al. 2020 (`xiao2020_interface_stability_ssb_review`); Nolan et al. 2018 (`nolan2018_computation_accelerated_design_review`); Wang et al. 2025 (`wang2025_ai_ecosystems_electrolyte_interface_ssb`)]

### 무질서와 Cl 과잉

argyrodite의 빠른 전도는 할라이드와 free S²⁻ 자리가 섞이는 음이온 자리 무질서가 율속인 inter-cage 점프를 켜기 때문이라는 데 리뷰들이 일치한다. I⁻는 S²⁻보다 커서 섞이지 않고, Bai et al. 2020은 Li₆PS₅I의 σ를 ~10⁻⁷ S/cm로 인용했다. He et al. 2023은 de Klerk 2016을 따라 Cl이 4a와 4d에 1:3으로 나뉠 때 전도도가 가장 높다고 옮겼다. Wu et al. 2026은 MLIP 배열 샘플에서 Li₆PS₅Cl 음이온 무질서 최적창을 37.5 – 50 %로 인용했다. 검토 측은 최적 분포가 방법에 따라 달라지므로 중간 무질서에 최적이 있다는 데까지만 쓰라고 본다. [근거: Bai et al. 2020 (`bai2020_argyrodite_review_progress`); He et al. 2023 (`he2023_halogen_chemistry_solid_electrolytes`); Dutra et al. 2025 (`dutra2025_atomistic_modelling_ml_se_review`); Wu et al. 2026 (`wu2026_ml_driven_electrolyte_interface_design_review`)]

Cl 과잉 조성의 전도도는 보고마다 크게 달라, 같은 출처 안에서만 비교해야 한다. Li₅.₅PS₄.₅Cl₁.₅는 Bai et al. 2020에서 10 mS/cm이고, He et al. 2023이 옮긴 Yu 2020에서는 6.41×10⁻³ S cm⁻¹이다. Li₅.₄PS₄.₄Cl₁.₆은 Nosrati et al. 2026의 Table 1에 20.2 mS cm⁻¹로 실렸다. 검토 측은 같은 명목 조성을 Adeli 2019가 LiCl 석출과 함께 3.3 mS cm⁻¹로 보고했다고 지적한다. Li₆PS₅I 전도도도 He et al. 2023의 본문과 SI, Liang et al. 2026 사이에서 자릿수가 어긋난다. [근거: Bai et al. 2020 (`bai2020_argyrodite_review_progress`); He et al. 2023 (`he2023_halogen_chemistry_solid_electrolytes`); Nosrati et al. 2026 (`nosrati2026_anion_engineering_sulfide_se_review`); Liang et al. 2026 (`liang2026_interface_bottleneck_solid_state_batteries`)]

### 계산 도구의 신뢰 범위

정적 DFT와 AIMD의 오차 원천은 리뷰들이 비교적 분명히 적어 두었다. He et al. 2019는 PBE가 반응전압을 수 십 분의 1 V, band gap을 약 1 eV 과소평가한다고 적었고, 에너지 계산에 SCAN이나 HSE06을 권했다. 우리 정적 DFT 백본은 PBE와 MP hull이어서, 배터리 계산은 PBE가 주류라는 원문 서술이 functional 선택의 근거가 된다. Nolan et al. 2018은 AIMD가 보통 600 K 이상에서 돌고, 실온 전도도로 외삽할 때 오차가 두 자릿수까지 커질 수 있다고 적었다. 검토 측은 He et al. 2019의 band-edge 안정창이 고체전해질 분해창을 과대평가한다고 보아, 분해 전압 근거로 쓰지 않는다. [근거: He et al. 2019 (`he2019_dft_for_battery_materials_review`); Nolan et al. 2018 (`nolan2018_computation_accelerated_design_review`)]

MLIP는 계산 규모를 넓히지만, 학습 범함수의 편향과 검증 방식이라는 새 쟁점을 낳는다. Dutra et al. 2025의 도식은 MLIP 적용 스케일을 >10,000 atoms and >1 ns로 적었는데, 이 문구에는 출처가 없어 리뷰의 권고 기준일 뿐이다. 이 기준으로 보면 558 원자, 200–400 ps인 우리 UMA-MD는 MLIP 칸이 아니라 참조데이터 칸에 앉는다. Wu et al. 2026은 범용 uMLIP의 힘 RMSE를 40–80 meV/Å로 적고, 낮은 RMSE가 동역학 물성의 정확도를 보장하지 않는다고 적었다. Oginni et al. 2026도 ML이 학습 범함수의 편향을 상속하므로 관측량으로 검증해야 한다고 정리했다. [근거: Dutra et al. 2025 (`dutra2025_atomistic_modelling_ml_se_review`); Wu et al. 2026 (`wu2026_ml_driven_electrolyte_interface_design_review`); Oginni et al. 2026 (`oginni2026_computational_design_review`)]

### 이 장의 값

| 값 | 표기 | 근거 |
|---|---|---|
| 황화물 SE 계산 환원 전위(Li₆PS₅Cl 등) | 1.7 V | Nolan et al. 2018 (`nolan2018_computation_accelerated_design_review`) |
| 황화물 SE 계산 산화 전위(Li₆PS₅Cl 등) | 2.4 V | Nolan et al. 2018 (`nolan2018_computation_accelerated_design_review`) |
| Li₆PS₅Cl DFT 산화 분해전위 | 2.01 V | Kim et al. 2021 (`kim2021_review_oxide_sulfide_se_interfaces`) |
| 무기 Li SE 임계전류밀도(상온) | ≤ 0.3 mA/cm² | Famprikis et al. 2019 (`famprikis2019_fundamentals_inorganic_sse`) |
| β-Li3PS4 황화물 셀 전체 저항 | 350–450 Ω cm² | Kim et al. 2021 (`kim2021_review_oxide_sulfide_se_interfaces`) |
| 황화물과 산화물 양극 반응 구동력 | >300 meV/atom | Xiao et al. 2020 (`xiao2020_interface_stability_ssb_review`) |
| Li₅.₅PS₄.₅Cl₁.₅ 이온전도도(실험) | 10 mS/cm | Bai et al. 2020 (`bai2020_argyrodite_review_progress`) |
| 범용 uMLIP 힘 RMSE(2차 인용) | 40–80 meV/Å | Wu et al. 2026 (`wu2026_ml_driven_electrolyte_interface_design_review`) |

### 아직 열린 문제

- hull 기반 계산 창을 실제 창의 하한으로 볼지, kinetic 안정화를 설명하는 출발점으로만 볼지가 정리되지 않았다. 간접 분해 경로와 고유 안정성 논거는 Dutra et al. 2025의 요약에 머물러 있어, Schwietert 원전 확인이 남아 있다. [근거: Dutra et al. 2025 (`dutra2025_atomistic_modelling_ml_se_review`); Xiao et al. 2020 (`xiao2020_interface_stability_ssb_review`); Fan 2026 (`fan2026_sulfide_assb_stability_review_ECERD2600097`)]
- 열역학 반응에너지가 계면이 부동태가 될지, 얼마나 빨리 자랄지까지 말해 주는지는 답이 없다. Wang et al. 2025와 Wu et al. 2026은 열역학 판정의 한계를 강조하지만, 검토 측은 Wu et al. 2026의 해당 문장이 원전보다 강하게 쓰였다고 본다. 우리 0 K hull grand-potential 방법도 반응이 일어나는가에만 답한다. [근거: Wang et al. 2025 (`wang2025_ai_ecosystems_electrolyte_interface_ssb`); Wu et al. 2026 (`wu2026_ml_driven_electrolyte_interface_design_review`)]
- Li₃P를 어느 쪽 산물로 볼지도 갈린다. 우리는 Li₃P를 전자 누설 산물로 판정해 왔다. Xiao et al. 2020은 Li₃PO₄/Li와 LiPON/Li 계면에서 Li₃P를 부동태 산물로 쓴다. [근거: Xiao et al. 2020 (`xiao2020_interface_stability_ssb_review`)]
- 역학 변수의 값은 아직 비어 있다. Famprikis et al. 2019는 K_Ic를 성능 인자로 세우고도 수치를 주지 않았다. Alharbi 2026은 두께 의존 자료 없이 틀을 세웠고, 분해 산물의 부피가 접촉을 바꾸는 경로는 한 문장도 다루지 않았다. [근거: Famprikis et al. 2019 (`famprikis2019_fundamentals_inorganic_sse`); Alharbi 2026 (`alharbi2026_coupled_design_ultrathin_composite_se_review`)]

### 먼저 읽을 논문

1. Famprikis et al. 2019 (`famprikis2019_fundamentals_inorganic_sse`) — 수송, 안정창, 역학, 공정의 네 축과 기본 용어를 한 번에 정해 준다.
2. Nolan et al. 2018 (`nolan2018_computation_accelerated_design_review`) — 계산 창의 정의와 계면 세 유형의 출발점이고, 본문과 그림의 어긋남도 함께 정리되어 있다.
3. Xiao et al. 2020 (`xiao2020_interface_stability_ssb_review`) — 계산이 예측한 계면 분해산물을 실험과 대조하고, 네 층의 계산 모델이 각각 상한인지 하한인지를 밝힌다.
4. He et al. 2023 (`he2023_halogen_chemistry_solid_electrolytes`) — argyrodite의 4a/4d 무질서와 Cl 과잉 기전을 가장 자세히 다루고, 본문과 SI가 어긋나는 수치 사례도 보여 준다.
5. Wu et al. 2026 (`wu2026_ml_driven_electrolyte_interface_design_review`) — MLIP 정확도 대역과 계면 판정의 세 갈래를 정리해 계산 쪽 최근 쟁점으로 이어 준다.

## 이 장의 논문 (17편)

| digest | 저자 · 연도 | 제목 | 한 줄 결론 |
|---|---|---|---|
| `janek2016_solid_future_battery_development` | Janek · Zeier 2016 | A solid future for battery development | 고체 전지는 다섯 과제를 넘어야 하며, 에너지보다 빠른 동역학이 먼저 개발을 이끌 수 있다고 원문은 내다봤다. |
| `nolan2018_computation_accelerated_design_review` | Nolan et al. 2018 | Computation-Accelerated Design of Materials and Interfaces for All-Solid-State Lithium-Ion Batteries | 황화물 전해질의 열역학적 창은 1.7–2.4 V로 좁고, 전지가 도는 것은 분해산물 계면층이 전자를 막기 때문이라고 정리한 리뷰다. |
| `famprikis2019_fundamentals_inorganic_sse` | Famprikis et al. 2019 | Fundamentals of inorganic solid-state electrolytes for batteries | 상온 전도도는 액체 수준에 이르렀고, 남은 과제는 다중스케일 수송, 계면 안정성, 역학, 공정이라고 정리한 리뷰다. |
| `he2019_dft_for_battery_materials_review` | He et al. 2019 | Density Functional Theory for Battery Materials | 배터리 재료 DFT를 다섯 축으로 정리하고, 에너지 계산에는 PBE보다 SCAN이나 HSE06을 권한다. |
| `bai2020_argyrodite_review_progress` | Bai et al. 2020 | Research progress in Li-argyrodite-based solid-state electrolytes | Li₆PS₅X는 전도도와 연성의 균형이 좋지만, 수분, 고전압 산화, 합성 편차의 약점은 다중 치환과 공정 최적화로 함께 풀어야 한다. |
| `xiao2020_interface_stability_ssb_review` | Xiao et al. 2020 | Understanding interface stability in solid-state batteries | 계면 안정성은 네 층의 계산 모델로 상한과 하한을 괄호쳐야 하며, 2015–2019년 실험이 그 예측을 상 수준에서 거의 따라잡았다. |
| `kim2021_review_oxide_sulfide_se_interfaces` | Kim et al. 2021 | Solid‐State Li–Metal Batteries: Challenges and Horizons of Oxide and Sulfide Solid Electrolytes and Their Interfaces | 고체전해질 자체 성능은 충분히 올라왔고, 전고체 Li 금속 전지의 성패는 양극과 음극 계면의 분해와 dendrite 제어에 달려 있다. |
| `he2023_halogen_chemistry_solid_electrolytes` | He et al. 2023 | Halogen chemistry of solid electrolytes in all-solid-state batteries | 할로겐 고체전해질 100년 계보를 정리하고, argyrodite의 빠른 전도를 4a/4d 자리 S²⁻/X⁻ 무질서로 설명한 개관 리뷰다. |
| `miao2023_role_of_interfaces_solid_state_batteries` | Miao et al. 2023 | Role of Interfaces in Solid‐State Batteries | 계면을 세 층위로 나누고 접촉, 안정성, 부피변화 문제를 코팅, 버퍼층, 압력 해법과 짝지은 비계산 리뷰다. |
| `dutra2025_atomistic_modelling_ml_se_review` | Dutra et al. 2025 | Understanding solid-state battery electrolytes using atomistic modelling and machine learning | 고체전해질 원자단위 계산 문헌을 세 축으로 정리했고, 분해산물 기반 전기화학 창이 관측을 과소평가할 수 있다고 명시했다. |
| `wang2025_ai_ecosystems_electrolyte_interface_ssb` | Wang et al. 2025 | Toward AI ecosystems for electrolyte and interface engineering in solid-state batteries | SSB 전해질·계면 설계의 AI 활용을 세 양식으로 정리했지만, AI 생태계는 제안 단계이고 CEI 조건 대부분에는 측정량이 없다. |
| `alharbi2026_coupled_design_ultrathin_composite_se_review` | Alharbi 2026 | Coupled Design Principles for Ultrathin Composite Solid Electrolytes: Reconciling Transport, Mechanics, and Interfacial Chemistry in All-Solid-State Lithium Batteries | 초박형 복합 전해질은 수송, 역학, 계면, 제조가 서로 묶여 따로 최적화할 수 없다는 틀을 세운 미심사 리뷰다. |
| `fan2026_sulfide_assb_stability_review_ECERD2600097` | Fan 2026 | Stability Issues in Sulfide-Based All-Solid-State Batteries: From Material Properties to Electrode Interfaces | 황화물 전고체전지의 안정성 문제는 단일 재료 결함이 아니라 화학, 전기화학, 열, 기계 인자의 결합 효과이고, 해법은 고유 안정성과 동적 계면 조절에 있다. |
| `liang2026_interface_bottleneck_solid_state_batteries` | Liang et al. 2026 | Overcoming the Interface Bottleneck in Solid‐State Batteries: Electrolyte Design, Interface Engineering, and Computational Discovery | 세 계열 무기 고체전해질을 계면이라는 렌즈로 다시 정리하고, 계산 도구는 소개에 그친 종설이다. |
| `nosrati2026_anion_engineering_sulfide_se_review` | Nosrati et al. 2026 | Anion Engineering of Sulfide Solid Electrolytes: From Fundamentals to High‐Performance All‐Solid‐State Batteries | 단일 음이온 치환은 한 성질을 올리고 다른 성질에서 손해를 보며, 기능을 나눠 맡기는 공도핑이 그 손해를 피한다고 원문은 정리했다. |
| `oginni2026_computational_design_review` | Oginni et al. 2026 | Computational design of quantum and functional materials for next generation electronic and energy technologies | DFT, beyond-DFT, MD·MC, ML, 양자컴퓨팅을 정확도와 비용의 계층으로 묶었지만 정량 비교와 방법 파라미터는 없는 개관 리뷰다. |
| `wu2026_ml_driven_electrolyte_interface_design_review` | Wu et al. 2026 | Machine Learning‐Driven Design of Electrolytes and Interfaces for Solid‐State Lithium Batteries: Progress and Outlook | 고체 리튬전지 전해질과 계면의 ML 연구를 정리하며, 정적 계면에너지만으로는 계면 품질을 판정할 수 없다고 주장한 리뷰다. |

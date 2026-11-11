# Highly reliable and large-scale simulations of promising argyrodite solid-state electrolytes using a machine-learned moment tensor potential

*optB88-vdw로 학습한 MTP만 무질서 의존 전도도를 재현한다*

- Kim et al. · Nano Energy 124, 109436 (2024) · doi:10.1016/j.nanoen.2024.109436 · digest `kim2024_mtp_argyrodite_disorder_gb`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## optB88-vdw로 학습한 MTP만 무질서 의존 전도도를 재현한다

> optB88-vdw로 학습한 MTP가 자리 무질서에 따른 전도도를 재현했고, 입계에서는 Li이 정전기적으로 쌓여 확산이 느려진다. (L17)

### 요점

1. 같은 AIMD 스냅샷을 세 가지 DFT functional로 다시 계산해 MTP를 학습하고, 아지로다이트의 여섯 가지 4a/4c 배열, 무질서 대형셀, Σ5 입계를 MD로 계산했다. (L13 · 118 · 120)
2. optB88-vdw로 학습한 MTP만 ordered는 느리고 disordered는 빠른 경향과 실험 전도도를 함께 재현했고, 입계에서는 Li 확산계수가 bulk의 약 0.3배로 줄었다. (L17 · 73 · 108)
3. 전도도 가중과 결정화도 보정은 경험식이고 표기 오류와 단일 입계 모델의 한계가 있어, 검토 측은 절대값보다 경향과 개념을 가져다 쓰라고 본다. (L205 · 207 · 215)

### 문제와 접근

Li₆PS₅X에서 할라이드와 S²⁻가 4a/4c 자리를 나누는 방식이 전도도를 좌우한다. 그러나 여섯 가지 배열을 모두 AIMD(ab initio molecular dynamics)로 돌리기에는 셀 크기, 시간, 온도의 제약이 크다. 원문은 AIMD를 MTP(moment tensor potential)로 대체하되, 어떤 DFT functional로 학습해야 맞는 물리가 나오는지를 먼저 판정했다. (L13 · 22–23)

여섯 배열은 enumlib로 만든 정수 점유 모델이다. 4c의 X⁻ 점유율이 0%와 100%인 배열을 ordered, 그 사이 배열을 disordered로 부르고, 50%에는 배치가 다른 두 배열이 있다. 훈련셋은 격자 변형과 고온 AIMD 스냅샷으로 만들었고, 같은 스냅샷을 PBE, PBE-D3(BJ), optB88-vdw로 각각 다시 계산해 세 MTP를 학습했다. (L29–30 · 120)

- 그림 — Fig. S1: (b)에서 초록 원이 4c 자리의 X⁻ 위치이고, 각 백분율이 4c의 X⁻ 점유율이다. (L47)

### functional 판정

세 MTP 모두 회귀 오차는 작았지만, 배열에 따른 전도도 차이는 optB88-vdw로 학습한 MTP만 재현했다. 원문 Table 1에서 ordered와 disordered 사이의 σ는 3–4자릿수 벌어진다. MTP_PBE와 MTP_PBE-D3(BJ)는 100% 배열에서 3.7 mS/cm라는 비정상적으로 높은 전도도를 냈다. (L70 · 73 · 130)

결정화도 보정을 거친 σ80%bulk에서도 같은 판정이 나왔다. 이 값은 경험식 σ_exp=σ_calc·χc^7.14에 χc=0.8을 넣어 얻는다. optB88-vdw는 2.46으로 실험 2.3–2.5와 맞았고, PBE-D3(BJ)는 0.55로 낮았다. (L71 · 95 · 131)

- 그림 — Fig. 2: (a) AIMD_PBE와 (d) MTP_optB88-vdw의 배열별 순서를 비교하고, (b)와 (c)에서 100% 배열이 비정상적으로 빠른 점을 보면 된다. (L73 · 152)

### random 셀과 PS₄

여섯 배열을 상대 에너지에 따른 Boltzmann 가중 개수로 3×3×3 셀에 섞은 random structure가 배열 전수 계산을 대신할 수 있었다. 이 셀의 Arrhenius 곡선은 ordered와 disordered 사이에서 disordered 쪽에 가까웠다. Li₆PS₅Cl의 σ80%는 2.3 mS/cm로 실험 2.3–2.5와 일치했다. (L17 · 31 · 91 …)

PS₄의 회전과 진동은 Li 확산을 키우는 역할을 했다. 600 K에서 PS₄를 고정하면 D가 ordered에서 −18%, disordered에서 −50% 줄었다. 고정해도 disordered가 ordered보다 빨라서, 원문은 확산 순위를 정하는 것은 배열이라고 보았다. (L100 · 140)

- 그림 — Fig. 3: (b)에서 random 곡선이 0% 배열과 50% 배열 곡선 사이에 놓이는 위치를, (c)에서 배열별 Li 궤적의 cage 간 연결을 보면 된다. (L135–136)

### 입계의 Li 축적

입계에서는 Li이 쌓이면서 확산이 느려졌다. 가장 안정한 tilt Σ5[100](021) 입계를 골라 active learning으로 MTP를 보강하고, 13,860원자가 넘는 셀을 350 K에서 10 ns 동안 계산했다. 입계 core의 D는 5.4×10⁻⁸ cm²/s로 bulk 1.8×10⁻⁷의 약 0.3배였고, 영향은 계면에서 10–20 Å까지 미쳤다. (L107–109 · 143)

원문은 그 원인을 구조 붕괴가 아닌 전하 분포에서 찾았다. 입계에 PS₄³⁻와 S²⁻가 인접해 국소적으로 강한 음전하가 생기고, Li이 bulk에서 입계 쪽으로 차례로 옮겨와 쌓인다. 처방으로 고산화수 원소 도핑으로 S 전하를 줄이는 inductive effect를 제안했지만 계산으로 검증하지는 않았다. (L111 · 113 · 145–146)

- 그림 — Fig. 5: (c)의 입계 거리별 D와 (d)의 시간에 따른 Li 수 지도가 Li 축적을 정량화한 부분이다. (L155)

### 어디까지 믿나

검토 측은 전도도 가중 방식의 통계적 근거가 약하다고 본다. P_i(σ)는 전도도를 Boltzmann 인자에 넣은 차원이 맞지 않는 heuristic이고, σ80% 보정도 경험 회귀식이다. 열역학 가중으로 만든 random 셀의 4c-Cl 평균 점유율은 42.6%로 실험 70%와 어긋나는데, 원문은 이를 점검하지 않았다. (L205–206)

검토 측은 표기 오류도 여럿 지적한다. 힘 MAE 단위가 본문과 SI 세 곳에서 meV/Å로 잘못 적혔고, 실제 힘 MAE는 0.07 eV/Å급으로 봐야 한다. Table S1에서 I 조성의 Ea가 AIMD와 MTP에서 같아, 검토 측은 MTP 쪽이 복제된 것으로 본다. 입계는 단일 모델이고 10 ns에서도 Li 축적이 수렴하지 않았다. (L24 · 207–208 · 215)

- 그림 — Fig. S3: inset의 MAE 단위는 meV/Å로 적혀 있지만 산점도 축은 eV/Å이어서, 검토 측은 값을 eV/Å로 읽어야 한다고 본다. (L49)

### 용어 풀이 (논문에 없는 일반 설명)

- **MTP (moment tensor potential)**: 원자 주변 환경을 moment tensor 기저로 전개해 에너지와 힘을 선형 회귀로 맞추는 기계학습 원자간 퍼텐셜이다.
- **Nernst–Einstein 관계**: MD에서 얻은 확산계수를 이온 농도와 전하를 이용해 이온 전도도로 바꾸는 식으로, 이온 간 상관을 무시하면 Haven 비를 1로 두는 셈이다.
- **Σ 입계 (CSL)**: 두 결정립을 특정 축으로 회전시켰을 때 겹치는 격자점의 비율로 입계를 분류하는 방식이며, Σ 값은 그 일치 격자 밀도의 역수다.

### 우리 연구에 주는 뜻

- 우리 disorder_ensemble에서 disordered는 빠르고 ordered는 600–800 K에서 frozen이었던 관측은 이 논문의 ordered와 disordered 이분법과 방향이 같다. (L180 · 193)
- 같은 스냅샷에서 functional만 바꿔 σ80%가 크게 갈린 결과는 우리가 UMA MLIP-MD의 σ 절대값을 인용하지 않고 Ea와 비율만 쓰는 규율의 외부 근거가 된다. (L183 · 192)
- 입계 계산은 우리에게 없는 축이고, 고산화수 도핑으로 S 전하를 줄이는 처방은 우리 cascade의 inductive-effect 언어와 이어진다. (L186 · 195)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| MTP_optB88-vdw 6배열 가중 σ80%bulk | 2.46 | Li₆PS₅Cl, 실험 2.3–2.5와 비교 | L71 |
| MTP_PBE-D3(BJ) 6배열 가중 σ80%bulk | 0.55 | Li₆PS₅Cl, 같은 훈련 스냅샷 | L71 |
| random structure σ80% | 2.3 mS/cm | Li₆PS₅Cl 3×3×3 random 셀 | L17 |
| 입계 영향 범위 | 10–20 Å | 10 Å bin 영역 분해 MSD | L109 |
| PS₄ 고정 시 D 감소 | −50% | disordered 배열, 600 K | L100 |

### 읽을 때 조심할 것

- 검토 측은 P_i(σ) 가중과 χc^7.14 결정화도 보정이 경험적 heuristic이므로 수치는 옮기지 말고 개념만 쓰라고 본다. (L171 · 205)
- Table S1의 I 조성 Ea는 AIMD와 MTP 열이 여섯 배열 모두 같아, 검토 측은 I의 MTP Ea를 인용하지 말라고 본다. (L24 · 86 · 208)
- 힘 MAE 단위가 본문과 SI에서 meV/Å로 잘못 적혀 있어 Fig S3 산점도 축의 eV/Å 해석만 유효하다. (L207)
- 입계는 Σ5[100](021) 단일 모델이고 Li 축적이 10 ns에서도 수렴하지 않아, 입계 D 절대값은 다결정 대표값이 아니다. (L215)

### 원문에서 먼저 볼 곳

- Table 1에서 네 방법의 배열별 E_rel, Ea, σRT와 σ80%bulk를 나란히 보면 functional 판정의 근거가 한눈에 들어온다. (L63 · 73)
- Fig. 5 (c)(d)는 입계 거리별 D와 Li 수의 시간 지도로 Li 축적을 정량화한 핵심 그림이다. (L155)
- Fig. S8은 PS₄ 고정 MD로 회전 기여를 분리한 결과라 간단한 구속 MD 분석법의 예로 볼 만하다. (L52 · 161)

태그: Li₆PS₅Cl · argyrodite · MTP · optB88-vdw · grain boundary · AIMD

# Fine-tuning MLIP foundation models: strategies for accuracy and transferability

*fine-tune 결과는 전략보다 파운데이션과 E₀가 먼저 좌우한다*

- Tompa & Varga-Umbrich · arXiv preprint, 2026 · doi:n/a (preprint) · digest `tompa2026_finetuning_mlip_foundation_strategies`
- 읽기 카드: digest를 풀어 쓰고 기계로 검증한 것. 괄호 안의 L 번호는 digest의 줄이다. 인용은 digest와 원문에서 확인한다.

## fine-tune 결과는 전략보다 파운데이션과 E₀가 먼저 좌우한다

> 전략 선택보다 파운데이션 품질, E₀ 초기화, 안정적 학습이 먼저이고, 넓게 쓸 모델에서는 replay만 견고성을 지켰다. (L30–33)

### 요점

1. MACE 파운데이션 모델을 일곱 가지 방식으로 fine-tune해 Li₆PS₅Cl을 포함한 다섯 화학계에서 비교했다. (L29 · 44–45)
2. 원문은 파운데이션 품질, E₀ 초기화, 하이퍼파라미터가 전략 차이보다 영향이 크고, 좁은 표적에는 naive가, 넓은 배치에는 multihead replay가 낫다고 적었다. (L30–32)
3. 동료심사 전 preprint이고, 모든 실험이 MACE이며 이온전도도 같은 수송 물성은 계산하지 않았다. (L7 · 58 · 313–314)

### 질문과 벤치마크

MACE 파운데이션 모델을 어떤 방식으로 fine-tune해야 하는지를 여러 전략으로 비교했다. 전략은 from-scratch, 전 파라미터를 학습하는 naive, layer freezing, 저랭크 어댑터를 붙이는 LoRA, multihead replay, pseudolabel replay, replay와 LoRA의 결합이다. 라벨은 모두 기존 공개 데이터셋을 재사용했고 새 DFT 캠페인은 하지 않았다. (L29 · 45 · 166)

다섯 벤치마크 계는 사전학습셋 OMat24의 핵심 영역에서 멀어지는 순서로 놓였고, Li₆PS₅Cl(LPSC)이 가장 가깝다. 원문은 LPSC만으로는 방법 간 구분이 어려울 것으로 예상한다고 적었다. LPSC fine-tune에는 단일 조성 500 구성의 PBE 라벨을 썼고, 평가는 학습에 쓰지 않은 130+ 다른 argyrodite 조성과 비-argyrodite Li 전해질 구조로 했다. (L94 · 167 · 419–420 …)

- 그림 — Fig. 2: 다섯 계가 OMat24 핵심 영역에서 멀어지는 순서로 배열돼 있고, LPSC가 가장 가까운 쪽 끝이다. (L167)

### 세 가지 전제

원문의 중심 주장은 전략보다 파운데이션 품질이 결과를 먼저 정한다는 것이다. LPSC에서 여덟 체크포인트를 같은 pseudolabel replay 레시피로 fine-tune하자 MP-0a가 가장 나빴고 OMat, MH 계열이 최상위였다. Sɴ2 NEB에서도 OMat24 기반은 MP2 장벽을 재현했지만 MPTraj 기반은 곡선이 붕괴했다. (L30 · 168 · 427 …)

둘째 전제는 원자기준에너지 E₀의 초기화다. MACE는 고립원자 기준 원자화에너지를 예측하므로 이론수준이 바뀌면 기준선이 어긋나고, 원문은 이를 fine-tuning 실패의 주된 원인으로 본다. 사전학습 모델의 예측과 참조에너지의 잔차로 원소별 보정을 맞추는 model-aware reestimation은 학습 없이 SPICE E₀ 오차를 평균법 3.13 eV에서 0.33 eV로 줄였다. ice Ih 25구성 학습에서는 averaged E₀이면 모든 fine-tune 모델이 MD에서 불안정했고 reestimated E₀이면 모두 안정했다. (L145–146 · 153–154 · 159 …)

- 그림 — Fig. 4: a 패널에서 LPSC의 reestimated와 averaged E₀를 Naive, LoRA로 나눠 비교한다. averaged E₀ 모델이 두 평가셋 모두에서 오차가 크고 분포가 넓다. (L169 · 453)

### Li 전해질 전이

LPSC 벤치마크에서 fine-tune의 이득은 더 먼 계로의 전이에서 갈렸다. 원문은 모든 방법이 다른 argyrodite에서 파운데이션보다 나아지고, replay 계열이 비-argyrodite 셋에서 가장 좋은 전이를 준다고 적었다. 또 fine-tune하지 않은 OMat24 기반 파운데이션이 MPTraj 기반을 가장 잘 fine-tune한 모델과 동등하거나 더 낮은 오차를 보였다고 적었다. (L278–279 · 468–469)

multihead replay는 학습률에 민감하다. LPSC에서 lr 1e-3이면 표적 힘 RMSE는 18.1 meV/Å로 권장값 1e-4의 18.4와 거의 같지만 replay head 힘 오차는 23.9에서 217.6으로 커졌다. replay 구조는 OMat24 원소일치본, 무작위 MPTraj 10,000, 둘의 결합 중 무엇을 써도 결과가 사실상 같았다. 원문은 weight decay를 0으로 두라고 하는데, weight decay가 파라미터를 사전학습 해가 아니라 0 쪽으로 당기기 때문이다. (L138 · 485–486 · 489 …)

- 그림 — Fig. 7: b 패널에서 다른 argyrodite와 비-argyrodite 두 평가셋의 힘 MAE를 전략별로 비교한다. replay 계열이 더 먼 비-argyrodite 셋에서 가장 낫다. (L172 · 467–469)

### 망각과 PES 구멍

좁은 표적 하나에는 naive fine-tune이 가장 정확했다. Sɴ2 전체 데이터에서 naive의 검증 힘 RMSE는 3.8 meV/Å로 scratch의 12.1보다 낮았다. 그러나 SPICE에서 naive는 OMat test set 성능을 자릿수 단위로 떨어뜨렸고, replay 계열은 파운데이션에 가까운 정확도를 유지했다. (L31 · 80 · 519–521)

NaCl fine-tune 모델의 random structure search(RSS)는 단거리 반발벽이 무너진 PES 구멍을 셌다. replay 없는 방법은 데이터를 늘릴수록 구멍이 늘어, naive는 50 GPa에서 9.4에서 34.4%로 올랐다. multihead와 pseudolabel은 모든 조건에서 파운데이션 수준이거나 그 이하였다. 모든 모델에 ZBL pair 반발항이 들어 있는데도 구멍이 생겼다. (L226–227 · 543 · 558–559 …)

- 그림 — Fig. 11: 셀에 숫자가 인쇄돼 있다. 0.1 GPa와 50 GPa 패널에서 데이터량이 늘 때 naive와 LoRA의 구멍 비율이 커지고 replay 계열은 그대로인 것을 본다. (L176 · 544 · 558 …)

### 어디까지 믿나

원문은 스스로 한계를 적었다. 모든 실험이 MACE라 LoRA, layer freezing, multihead의 거동이 다른 아키텍처에서 다를 수 있다. 하이퍼파라미터 탐색이 제한적이었고, RSS는 단거리 반발벽 붕괴만 보며 상대 상안정성 오류는 다른 진단이 필요하다. (L313–314 · 316–317 · 319–320)

검토 측은 동료심사 전 preprint v1이라 수치가 바뀔 수 있다고 본다. Fig. 10의 두 패널은 y축 단위가 1000배 어긋나 절대값이 아니라 파운데이션 대비 비율만 쓸 수 있다고 본다. Freeze (5)와 Freeze (6)의 정의가 주어지지 않아 어느 동결 변형이 안전한지 판단할 수 없다고 본다. LPSC 결과에 시드 산포가 없고 500 구성의 샘플링과 Cl/S 부분점유 처리가 적혀 있지 않다는 점도 지적한다. (L7 · 290 · 293 …)

- 그림 — Fig. 10: a 패널은 meV/Å, b 패널은 eV/Å로 축이 적혀 있어, 같은 패널 안에서 파운데이션 기준선 대비 배율만 읽는다. (L291–292 · 295)

### 용어 풀이 (논문에 없는 일반 설명)

- **E₀ (원자기준에너지)**: 원소별 고립원자 에너지로, 모델이 총에너지에서 이를 빼고 원자화에너지를 학습할 때의 기준선이다.
- **multihead replay**: 몸통을 공유하고 표적용과 replay용 readout head를 따로 두어 새 데이터와 사전학습 분포 데이터를 함께 학습하는 방식이다.
- **catastrophic forgetting**: 새 과제를 학습하면서 이전 과제에서의 성능이 크게 무너지는 현상이다.

### 우리 연구에 주는 뜻

- 우리가 쓰는 UMA-s-1p1은 fine-tune하지 않은 OMat24 계열 파운데이션이라, 이 논문의 비교에서 fine-tune 전 OMat 파운데이션 자리에 해당한다. (L237 · 248 · 250)
- RSS PES 구멍 진단은 DFT 없이 UMA에 바로 돌릴 수 있어, 우리 계에서 구멍 비율을 재고 b₂o₃ 골격 creep을 사후 진단하는 데 쓸 수 있다. (L672–675)
- 우리 Li₃PS₄ 벤치의 선형 원소보정은 원문이 쓰지 말라고 한 averaging 방식이고 fit R² 0.620이 낮아, model-aware reestimation으로 바꾸는 것을 검토한다. (L686–689)

### 핵심 수치

| 항목 | 값 | 맥락 | 근거 |
|---|---|---|---|
| LPSC 검증 힘 RMSE (target head) | 18.4 meV/Å | MACE-OMat-0-medium, pseudolabel, lr 1e-4 | L75 |
| LPSC fine-tune 데이터 크기 | 500 구성 | Li₆PS₅Cl 단일 조성, PBE | L419 |
| SPICE E₀ 복원 MAE, 평균법 | 3.13 eV | 학습 없이, 10원소 | L159 |
| SPICE E₀ 복원 MAE, reestimation | 0.33 eV | 학습 없이, 10원소 | L159 |
| multihead 추가 학습비용 | 3–15배 | naive 대비, 데이터 크기 의존 | L83 |
| naive의 RSS 구멍 비율 | 34.4% | NaCl, 50 GPa, 최대 데이터 | L558 |

### 읽을 때 조심할 것

- 동료심사 전 preprint v1이라 인용할 때 preprint로 표기하고 수치 변경을 전제해야 한다. (L7–9)
- Fig. 10은 두 패널의 축 단위가 1000배 어긋나 절대값을 인용하지 말고 패널 안 비율만 써야 한다고 검토 측은 본다. (L290 · 293 · 295)
- LPSC의 RSS 결과는 서술만 있고 그림이 없어 황화물의 PES 구멍 수치는 이 논문에서 얻을 수 없다. (L308–310)
- 모든 실험이 MACE이고 LoRA, pseudolabel replay, E₀ reestimation 구현도 MACE 3.15+에만 있어 다른 아키텍처로 바로 옮길 수 없다. (L313–314 · 614)

### 원문에서 먼저 볼 곳

- Fig. 7b와 Fig. 17은 LPSC에서 전략별, 파운데이션 계열별 OOD 전이를 보여 주는 핵심 그림이다. (L172 · 182 · 467)
- Table 9와 Fig. 13은 LPSC multihead replay의 학습률 민감도를 인쇄된 수치로 보여 준다. (L178 · 194 · 489)
- Table 1과 Fig. 11은 검증 오차가 멀쩡해도 MD가 무너지거나 PES 구멍이 늘어나는 실패를 직접 잰 자료다. (L176 · 186 · 566–567)

태그: Li₆PS₅Cl · MACE · MLIP · fine-tuning · LoRA · multihead replay · catastrophic forgetting · RSS

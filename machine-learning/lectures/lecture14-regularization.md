# Lecture 14: Regularization

## 1. Overfitting 복습
- Validation/test error > training error
- Overfitting에 민감한 경우:
  - 데이터셋 크기가 작음
  - hypothesis class가 큼 (모델이 너무 복잡)

## 2. Regularization 개념
- 신경망은 너무 강력해서 **noise까지 fit** → overfitting
- 목표: overfitting 줄이고 better generalization
- 방법: 추가 제약/정보 부여 → prior knowledge 인코딩
- **Occam's Razor**: 경쟁하는 가설 중 가장 단순한 것이 최고
- 목표: case 3(overfit) → case 2(적절)로

### 딥러닝 성공 공식
```
복잡한 모델 + 효과적 regularization + 빅데이터
- 복잡한 모델: 데이터 fit 가능성 ↑
- regularization + 빅데이터: generalization gap ↓
```

## 3. Regularization 전략
1. 모델에 제약 (예: Dropout)
2. cost function에 항 추가 (soft constraint)
3. 여러 가설 결합 (Ensemble)
4. Data Augmentation

## 4. Parameter Norm Penalty (cost에 항 추가)
```
J(w) = Data loss + λ·Ω(w)
       ────────   ──────
       예측이      regularization
       맞아야 함    (과적합 방지)
```
- λ: hyperparameter, validation set으로 선택
- 학습 전에 미리 고정

### 왜 bias는 penalize 안 하나? (시험 포인트!)
- Weight: 함수의 **곡률(curvature)** 결정, 두 변수 상호작용
- Bias: 함수의 **offset** 결정, 단일 변수만 제어
- bias를 안 건드려도 variance 별로 안 늚
- bias를 regularize하면 → 심각한 underfitting 위험

## 5. L1 vs L2 Regularizer (시험 단골!)

### L1 Regularizer
```
Ω(w) = ||w||₁ = Σᵢ |wᵢ|
```
- a.k.a. **Lasso** (통계), basis pursuit (신호처리)
- Convex이지만 **모든 곳에서 미분 불가** (0에서 꺾임)
- **Sparse solution** (일부 weight를 정확히 0으로!)
- 변수 shrinkage + **selection**
- 크기와 무관하게 동일한 penalty

### L2 Regularizer
```
Ω(w) = ||w||₂² = Σᵢ wᵢ²
```
- a.k.a. **Ridge** (통계), **Weight Decay** (신경망)
- Convex이고 **미분 가능**
- 변수 shrinkage만 (0으로 만들진 않음)
- 큰 magnitude에 더 큰 penalty

### 비교표
| | L1 (Lasso) | L2 (Ridge/Weight Decay) |
|---|---|---|
| 수식 | Σ\|wᵢ\| | Σwᵢ² |
| 미분 | 불가능(0에서) | 가능 |
| 해 | **Sparse (0 다수)** | small but non-zero |
| 효과 | shrinkage + selection | shrinkage만 |
| penalty | 크기 무관 동일 | 클수록 큰 penalty |

## 6. Early Stopping
- Overfitting: training error는 계속 ↓지만 validation error는 ↑
- 아이디어: **validation error가 가장 낮을 때 멈추자**
- training/validation error 둘 다 추적 → validation 최저점에서 stop
- validation error는 매 epoch 측정
- 간단/효과적 → 딥러닝에서 매우 인기

## 7. Model Ensemble
- 약한 모델들을 결합해 강한 모델 만들기 ("model averaging")
- 강하다 = lower bias/variance, 더 나은 정확도
- 가정: 다른 모델 → 다른 실수 → noise 평균내면 0
- 종류: voting, Bagging, Boosting

### Bagging (Bootstrap Aggregating)
- 여러 모델을 따로 학습 → test에서 투표
- 다른 데이터 만드는 법: **random sampling으로 k개 데이터셋 구성**
- 같은 모델/알고리즘/loss 재사용 → 다른 모델 학습 효과
- generalization error 감소

### Boosting
- 개별 모델보다 **높은 capacity**의 앙상블 구성 (예: AdaBoost)
- 약한 learner를 **순차적**으로 학습
- 이전 learner가 틀린 예제에 더 집중 (가중치 ↑)
- 신경망: 점진적으로 네트워크/hidden unit 추가

### 앙상블이 작동하는 이유
- 다양성의 원천: random 초기화, random minibatch, hyperparameter, 비결정적 구현
- → 부분적으로 독립적인 error → 평균내면 효과적
- 매우 강력하고 신뢰할 만함

## 8. Dropout ★ (시험 핵심!)
- 여러 모델 학습은 비쌈 (특히 DL)
- 동기: **하나의 네트워크에서 여러 subnetwork를 추출!**
- 방법: input & hidden unit을 **랜덤하게 0으로** 만듦
- → exponentially many 네트워크의 bagging 앙상블을 싸게 근사

### Dropout Idea
- 매 forward pass마다 일부 뉴런을 랜덤하게 0
- inclusion(또는 dropout) 확률 = hyperparameter
  - 보통 hidden unit 0.5, input unit 0.8

### Training Time
- minibatch마다 binary mask μ를 랜덤 샘플 → input/hidden에 적용
- 예: μ = (μ_x1, μ_x2, μ_h1, μ_h2) = (1,1,0,1)
- 평소처럼 forward → backprop → update

### Inference Time: Weight Scaling Inference Rule
- 문제: 앙상블 예측은 exponential 개수 합 → 계산 불가능
- 해결: 한 모델로 근사 (weight scaling)
- 각 unit의 outgoing weight: w → β·w
  - β = inclusion 확률 (drop 안 할 확률)
- 이유: test 시 모든 뉴런 활성 → activation 스케일 맞춰야
  - test 출력 = training 시 기대 출력

### Inverted Dropout (더 흔함)
```
Vanilla Dropout:
  Training: drop with prob (1-β)
  Test: activation에 β 곱함

Inverted Dropout:
  Training: drop + activation에 1/β 곱함
  Test: 변경 없음! ← 효율적
```
- Dropout은 **비선형 activation 뒤에** 배치

### Dropout 장점
- weight decay 같은 표준 regularizer보다 효과적
- 다른 regularization과 결합 가능
- 매우 계산 저렴 (training/inference 모두)
- 거의 모든 모델에 잘 작동 (feedforward, RNN)

### 관련: DropConnect
- weight의 랜덤 subset을 0으로 (unit이 아니라 connection)

## 9. Common Pattern (시험 포인트!)
```
Training:  랜덤성 추가
Inference: 랜덤성 평균화
```
예시:
- **Batch Normalization**: train은 minibatch 통계, test는 고정 통계
- **Stochastic Depth**: train은 일부 층 skip, test는 모든 층
- Dropout, DropConnect, Fractional Pooling, Data Augmentation

## 10. Data Augmentation
- training data를 변형해 데이터 늘리기
- 성공 사례: object recognition, speech recognition

### 이미지 기법
- Random Crops and Scales (예: ResNet)
- Color Jitter (대비/밝기 랜덤, PCA color offset)
- Translation, Rotation, Stretching, Shearing, Lens distortion
- **AutoAugment**: RL로 좋은 augmentation 찾기

### Mixup / Cutout / CutMix
- **Mixup**: 두 샘플(이미지+레이블)을 선형결합
  - prior: feature 선형보간 → target 선형보간
  - 훈련 예제 사이에서 단순 선형 동작 선호 → generalization ↑
- **Cutout**: 랜덤 패치를 0으로 (regional dropout)
- **CutMix**: 이미지 간 랜덤 패치 잘라 붙임

## 11. Parameter Tying & Sharing
- **Parameter Tying**: 비슷한 task는 비슷한 파라미터값 (norm penalty로 A,B 묶음)
- **Parameter Sharing** (더 인기): 파라미터 집합을 동일하게
  - 표현/계산 효율 (weight 수 ↓)
  - 예: **CNN**, multi-task learning

### Multi-task Learning
- 방법1: 여러 task의 예제를 pool → 추가 예제 = soft constraint → generalization ↑
- 방법2: 모델 일부를 task 간 공유 → 공유부가 좋은 값으로 제약

## 12. Sparse Representations
- unit의 **activation**에 penalty → sparse representation 유도
- 예: hidden representation에 L1: Ω(a) = ||a||₁ = Σ|aᵢ|
- cf. Lasso는 **parameter**에 직접 penalty (Ω(w)=||w||₁)
  - Sparse parameterization vs Sparse representation

## 핵심 요약 (시험)
1. **Regularization = overfitting 방지 = Occam's razor 적용**
2. **L1(Lasso): sparse, 미분불가 / L2(Ridge/weight decay): shrinkage, 미분가능**
3. **bias는 penalize 안 함** (offset만 제어, underfitting 위험)
4. **Early stopping**: validation 최저점에서 멈춤
5. **Bagging(병렬, random sampling) vs Boosting(순차, 틀린 것에 집중)**
6. **Dropout = 싼 bagging 근사** (랜덤 뉴런 0, inverted dropout으로 test 변경 없음)
7. **Common pattern**: train에 랜덤성, test에 평균화
8. **SVM margin도 regularization의 일종**

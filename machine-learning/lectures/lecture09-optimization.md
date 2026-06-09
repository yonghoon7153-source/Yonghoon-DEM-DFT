# Lecture 9: Optimization

## 1. Recap (Lecture 4~5, 8)
- SVM: margin 최대화, support vectors, soft-margin (slack), hinge loss
- Regularization = Occam's Razor (단순한 모델 선호)
  - Data loss: 예측이 training data와 맞아야 함
  - Regularization: training에 과적합 방지 (generalization)
  - SVM에서 regularization = 가장 큰 margin 선택
- Cross-entropy (softmax + CE 결합으로 수치 안정)

## 2. Optimization의 목표
- Cost function을 최소화하는 파라미터 찾기

## 3. Random Search — 나쁜 방법
- 좋은 결과 보장 안 됨
- 무한히 많은 선택 → 영원히 걸림
- 파라미터와 loss의 관계를 활용 안 함

## 4. Analytic Solution (해석적 해)
- Partial derivative (편미분)로 각 파라미터가 loss에 미치는 영향 계산
- Chain rule 사용
- Critical point: ∂L/∂w = 0으로 놓고 풀기
- **Pros**: 정확한 해
- **Cons**: 행렬 역행렬 계산 (computationally expensive)
- Linear model: w = (XᵀX)⁻¹Xᵀy
- → 대부분의 모델은 closed-form이 없음!

## 5. Numerical Solution: Gradient Descent (핵심!)

### 개념
- Iterative algorithm: 파라미터를 반복적으로 업데이트
- 최소 loss에 도달할 때까지 gradient 방향으로 이동

### 단계
1. weight를 작은 값(0 근처)으로 random 초기화
2. steepest descent 방향(= gradient 반대 방향)으로 업데이트

### Update Rule
```
w ← w - α·∇L(w)
```

### 직관 (왜 gradient 반대 방향?)
- ∂L/∂w > 0이면: w 증가 → L 증가  → w를 줄여야 함
- ∂L/∂w < 0이면: w 증가 → L 감소  → w를 늘려야 함
- 즉 gradient 반대 방향으로 가면 항상 L이 감소!

## 6. Learning Rate (α)
- Hyperparameter (step size)
- 클수록 w가 빠르게 변함
- 일반적으로 0.001 ~ 0.1
- **α 너무 작음**: 느린 진행
- **α 너무 큼**: 진동(oscillation)
- **α 매우 큼**: 불안정(instability), 발산
- Training curve (cost vs iteration)로 진단

## 7. Batch / Stochastic / Mini-batch GD

### Batch Gradient Descent (BGD)
- 전체 training data의 평균 loss로 gradient 계산
- 문제: 데이터가 크면 비현실적 (예: ImageNet 수백만 장)

### Stochastic Gradient Descent (SGD)
- 데이터 1개로 gradient 계산 (랜덤 선택)
- 전체를 보기 전에도 진전 가능!
- 수학적 근거: SGD는 BGD의 **unbiased estimate**
- 문제:
  - estimate의 variance가 높음
  - 1개씩 보면 벡터화(GPU 병렬연산) 활용 불가

### Mini-batch Gradient Descent (실전 표준!)
- subset(mini-batch)으로 gradient 계산
- mini-batch 클수록 variance 작아짐
- mini-batch size m = hyperparameter
  - 보통 GPU 메모리 한계까지 크게
  - m 크면 → learning rate 크게
  - m 작으면 → learning rate 작게

## 8. Training Algorithm (mini-batch size m, learning rate α)
```
1: 모든 파라미터 초기화
2: repeat
3:   minibatch B를 D에서 뽑음
4:   forward: 예측 ŷ 계산
5:   cost 계산
6:   backward: 모든 gradient 계산
7:   파라미터 업데이트: w ← w - α·∇L
8: until 멈출 때 (validation loss 수렴)
9: 최종 파라미터 반환
```

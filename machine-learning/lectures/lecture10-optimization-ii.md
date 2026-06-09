# Lecture 10: Optimization II

## 1. Critical Points (= Stationary Points)
- 기울기가 0인 점: ∇f = 0
- 3종류:
  - **Maxima**: negative curvature (음의 곡률)
  - **Minima**: positive curvature (양의 곡률)
  - **Saddle point**: 양/음 곡률 둘 다 가짐
    - 한 축으로는 위로(λ>0, local min), 다른 축으로는 아래로(λ<0)

## 2. Second Derivative (이차 미분)의 용도
1. critical point 분류
2. curvature(곡률) 측정
3. gradient 기반 최적화의 성능 예측

곡률에 따른 효과:
- **Negative curvature**: f가 gradient 예측보다 빨리 감소
- **No curvature**: gradient 예측이 정확
- **Positive curvature**: f가 gradient 예측보다 느리게 감소 (결국 증가)

## 3. Deep Learning에서의 최적화
- 목적함수에 많은 local minima + 평평한 영역에 둘러싸인 saddle point
- → 고차원에서 최적화 매우 어려움
- 보통 최소값이 아니어도 충분히 낮은 f를 찾는 것으로 만족
- (Dauphin 2014): 고차원에서 saddle point가 local minima보다 훨씬 흔함

## 4. Gradient Descent 복습
- 작은 α에 대해: f(x - α·sign(f'(x))) < f(x)
- gradient 반대 부호로 작은 스텝 이동 → f 감소

## 5. SGD 변형 (m = minibatch 크기, N = 전체)
- **m = 1**: SGD
- **1 < m < N**: Mini-batch SGD (m: 64,128,256,512, 2의 거듭제곱)
- **m = N**: Batch GD

### SGD 장점 (+)
- update당 계산 시간이 전체 데이터 수와 무관 → 큰 데이터에도 수렴 가능
- 이론보다 실전에서 더 잘 작동

### SGD 단점 (-)
- Local minima / saddle point에서 멈춤 (gradient = 0)
- Gradient noise
- **Poor conditioning of Hessian**

## 6. Poor Conditioning (poorly conditioned Hessian)
- 다차원에서 방향마다 second derivative가 다름
- **Condition number of Hessian H**: 고유값의 최대/최소 비율
  ```
  condition number = max_{i,j} |λᵢ / λⱼ|
  ```
- Condition number가 크면(poorly conditioned):
  - 한 방향은 미분이 급격히 증가, 다른 방향은 천천히
  - → gradient descent가 zig-zag (느림)
- Gradient descent는 greedy해서 이 변화를 모름 → step size 선택 어려움
- 예: condition number 5 → 가장 가파른 방향이 5배 곡률 (긴 협곡)
- H를 직접 쓰면 해결되지만 계산 비쌈
- → H 없이 poor conditioning 해결하는 법? (momentum, adaptive LR)

## 7. Method of Momentum (Polyak 1964)
- SGD 가속, 특히 다음 상황에서:
  - High curvature
  - 작지만 일관된 gradient
  - Noisy gradient
- 핵심: 과거 gradient의 exponentially decaying moving average를 누적 → 그 방향으로 계속 이동

### EWMA (Exponentially Weighted Moving Average)
```
v_t = γ·v_{t-1} + (1-γ)·g_t

v_t: 시간 t의 EWMA
g_t: 시간 t의 관측값
γ:   smoothing factor (과거에 주는 가중치)
```
- 과거로 갈수록 가중치가 지수적으로 감소
- 유효 관측 수 ≈ 1/(1-γ)
  - γ=0.9 → 10개 평균
  - γ=0.98 → 50개, γ=0.5 → 2개
- γ 클수록: 더 부드러운 곡선, 더 지연됨(latency)
- **Bias correction**: 초기값이 0에 가까워 작음 → v_t/(1-γᵗ)로 보정

### Gradient Descent with Momentum
```
v ← γ·v + (1-γ)·g   (또는 v ← γv + g 형태)
θ ← θ - α·v
```
- 물리 비유: momentum = mass·velocity, γ = 마찰(friction)
- 거의 항상 표준 GD보다 빠름

## 8. Nesterov Momentum
- 표준 momentum과 차이: **gradient를 어디서 계산하는가**
- momentum이 우리를 새 위치로 데려갈 거니까, **새 위치에서** gradient 계산
- velocity 적용 후 gradient 평가 → standard momentum에 보정항 추가
- 장점: convex에서 더 강한 수렴 보장, 일관되게 약간 더 좋음

## 9. Per-Parameter Adaptive Learning Rates
- 문제: 축(파라미터)마다 곡률이 다름 (수직 진동, 수평 느림)
- 해결: 수직은 느리게, 수평은 빠르게
- 기존: 모든 파라미터에 동일한 global learning rate
- 신규: AdaGrad, RMSProp, Adam → 파라미터마다 learning rate 적응

### AdaGrad
- 각 파라미터의 learning rate를 개별 조정
  - 가파른 방향(큰 gradient): 느리게
  - 완만한 방향(작은 gradient): 빠르게
```
r ← r + g⊙g           (gradient 제곱 누적)
θ ← θ - (α/√(r+δ))⊙g
```
- 단점: r이 단조 증가 → learning rate가 너무 빨리 감소 → 학습 조기 종료
- Adadelta: 누적 window를 고정 크기로 제한 → 감소 완화

### RMSProp (Root-Mean-Square prop)
- AdaGrad를 non-convex에서 잘 되게 수정
- gradient 누적을 EWMA로 변경 → 먼 과거 버림
```
r ← ρ·r + (1-ρ)·g⊙g
θ ← θ - (α/√(r+δ))⊙g
```
- ρ: decay rate (보통 0.9, 0.99, 0.999)
- δ: 수치 안정용 작은 수

### Adam (Adaptive Moment Estimation) ★ 기본 추천
- RMSProp + Momentum + bias correction
```
1. gradient g 계산
2. first moment:  s ← ρ₁·s + (1-ρ₁)·g          ← momentum
3. second moment: r ← ρ₂·r + (1-ρ₂)·g⊙g         ← RMSProp
4. bias correction: ŝ = s/(1-ρ₁ᵗ),  r̂ = r/(1-ρ₂ᵗ)
5. update: θ ← θ - α·ŝ/(√r̂ + δ)
```
- 추천 값: α=0.001(튜닝 필요), ρ₁=0.9, ρ₂=0.999, δ=10⁻⁸
- 보통 RMSProp보다 좋음 → **기본 알고리즘으로 추천**

## 10. Learning Rate Scheduling
- 모든 optimizer가 learning rate를 hyperparameter로 가짐
- 고정 LR보다 → 시간에 따라 점점 감소시키면 더 좋음
- 완만한/평평한 영역 도달 시 LR 감소
- SGD+Momentum에서 더 중요, Adam에선 덜 흔함

### Decay 방법
- Linear decay (특정 지점까지 감소 후 상수)
- Step decay (계단식)
- Exponential decay
- 1/k or 1/√k decay
- Manual decay (plateau에서 수동 감소)

### Initial Learning Rate 설정
- 100 iteration 정도 후 최고 성능을 내는 LR
- 조언: 처음 몇 iteration 모니터링, best보다 약간 높되 불안정하지 않게
- **Linear scaling rule**: minibatch 크기를 k배 → LR도 k배
  - 큰 batch일수록 update에 더 확신
- **Learning rate warmup**: 높은 초기 LR은 loss 폭발 → 처음 ~5000 iter 동안 0에서 선형 증가

## 11. Second-Order Optimization

### Newton's Method
- Gradient descent: first-order
- Newton: second-order 근사 후 최소화 → GD보다 빠름
```
2차 Taylor 근사 → critical point 풀면:
θ ← θ - H⁻¹·g       (Newton's update rule)
```
- 장점: (이론상) hyperparameter 없음
- 단점: H가 O(n²) 원소, 역행렬 O(n³) → 비쌈
- Levenberg-Marquardt: Newton과 GD 사이 전환

### Quasi-Newton Methods
- H를 직접 역행렬 안 하고 M_t로 H⁻¹ 근사
- **BFGS**: 가장 인기, 하지만 O(n²) 메모리
- **L-BFGS** (limited memory BFGS):
  - 전체 H⁻¹ 저장 안 함
  - full batch에선 잘 작동, minibatch/stochastic에선 부진

## 12. 실전 Optimizer 선택 조언
- **Adam**: 많은 경우 좋은 기본 선택
- **SGD + Momentum + LR decay**: 종종 Adam 능가, 하지만 튜닝 더 필요
- **L-BFGS**: full batch 가능하면 시도, noise 제거 필요

## 핵심 계보 (시험 포인트)
```
SGD
 → + Momentum (과거 gradient EWMA로 가속)
 → + Nesterov (새 위치에서 gradient 평가)
 → AdaGrad (파라미터별 적응 LR, gradient² 누적)
 → RMSProp (AdaGrad의 누적을 EWMA로)
 → Adam (RMSProp + Momentum + bias correction) ★
```

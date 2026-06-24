# Lecture 11: Feedforward Neural Networks

## 1. Limits of Linear Classification
- XOR은 linearly separable하지 않음
- Feature map으로 극복 가능 (예: XOR을 고차원으로)
- 하지만 general solution이 아님: 좋은 basis function 고르기 어려움

## 2. Feature Maps (사람이 설계하는 예시)
- Color Histogram
- Histogram of Gradients (HoG)
- Bag of Words (BoW)
- 문제: 일일이 사람이 설계해야 함

## 3. Features = Part of the Model
```
y = wᵀφ(x)
  = [non-linear φ] + [linear wᵀ·]
  = non-linear model
```
- 기존 ML: φ를 사람이 설계
- **Deep Learning: φ도 학습!** (Representation Learning)

## 4. Feedforward Networks 아이디어
- φ(x)의 각 차원을 **학습 대상**으로 봄
- Linear function만으로는 부족 → 비선형 필요
- 보통: h = g(Wx + b), g = 비선형 함수
- 더 깊게: 여러 층을 쌓음 (deep network)

## 5. Neural Networks (뇌에서 영감)
- Neuron: 뇌의 기본 계산 단위
- 뇌: ~10¹¹개 neuron, 각각 ~10⁴개와 연결

### 인공 뉴런 모델 (3요소)
1. **Synapses (weights)**: 입력에 가중치
2. **Adder**: 입력 벡터 → 스칼라 (가중합)
3. **Activation function**: 비선형 변환

```
입력 x → affine transform (Wx+b) → activation g(·) → output
z = Wx + b
a = g(z)
```

### 뇌 비유 주의!
- 생물학적 뉴런은 훨씬 복잡 (dendrite가 비선형 계산, synapse가 동적 시스템)
- 인공 뉴런은 매우 단순화된 모델

## 6. Artificial Neural Network 구조 (layers)
```
Input layer → Hidden layer 1 → ... → Hidden layer L → Output layer
```

### Input Layer
- 벡터로 표현
- 전처리: 평균 빼기, [-1,1] 정규화

### Output Layer (task별)
| Task | Output |
|------|--------|
| Regression | Linear unit (비선형 없음) |
| Multi-dim Regression | Linear units |
| Binary classification | Sigmoid (= logistic regression on 마지막 hidden) |
| Multi-class | Softmax (= multiclass logistic regression) |

### Hidden Layers
- 각 뉴런 = 이전 층의 가중 선형결합 + 비선형
- Unit j: a_j = g(Σ w_ji·x_i + b_j)
- 전체 층: a = g(Wx + b)

## 7. Feed-forward Neural Network
- 여러 unit을 **DAG (directed acyclic graph)**로 연결
- **No feedback connection** (출력이 다시 입력으로 안 감)
- Unit들을 layer로 그룹화

## 8. Multilayer Perceptron (MLP)
- 각 층이 N input → M output
- **Fully connected layer**: 모든 input이 모든 output에 연결
- Fully connected layer들로 구성된 네트워크 = **MLP**
- 함수의 합성(composition):
  ```
  f(x) = f_L(...f_2(f_1(x)))
  ```
- 모듈성: 각 층을 black box로 구현 가능

## 9. Feature Learning 관점
```
Hidden Layers:  Feature mapping (φ 학습)
Output Layer:   Linear regressor/classifier
```
- 예: 28×28=784 픽셀 손글씨 숫자
- 첫 층 hidden unit = feature detector (예: 대각선 획에 반응)
- wⱼ를 이미지로 reshape하면 시각화 가능

## 10. Expressive Power (표현력)

### 핵심: 비선형이 필수!
- 선형 층을 아무리 쌓아도 → 하나의 선형 층과 동일! (의미 없음)
  ```
  W₂(W₁x) = (W₂W₁)x = Wx   ← 결국 선형
  ```
- **비선형 activation을 써야** 진짜 깊어짐

### Universal Function Approximator
- 비선형 activation을 가진 multilayer feedforward net은
  **어떤 함수든 임의 정밀도로 근사 가능!**

## 11. Activation Functions (시험 중요!)

### Sigmoid
- σ(z) = 1/(1+e⁻ᶻ)
- 장점: 확률 해석 (firing rate)
- 단점:
  - **Saturation → killed gradient** (vanishing gradient)
  - **Not zero-centered** → zig-zag gradient update (비효율)
- hidden unit엔 권장 안 함, **output unit(확률)엔 사용**

### Tanh
- 보통 sigmoid보다 나음
- **Zero-centered** (장점)
- 0 근처에서 선형 → 학습 쉬움
- 단점: 여전히 saturation → vanishing gradient

### ReLU (Rectified Linear Unit) ★
- g(z) = max(0, z)
- 장점:
  - (+) 영역에서 saturation 없음
  - 계산 효율적
  - sigmoid보다 빠르게 수렴
- 단점:
  - not zero-centered
  - **Dying ReLU**: (-) 영역에 갇히면 gradient 영원히 0
- 조언: learning rate 너무 높지 않게, 입력을 살짝 양수로 초기화(0.01)

### ReLU 변형 (dying ReLU 해결)
- **Leaky ReLU**: g(z) = max(0.01z, z) — (-) 영역도 작은 gradient (fixed)
- **PReLU**: 기울기를 학습 (learnable)
- **ELU**: (-) 영역 exp로 부드럽게, zero mean에 가까움, noise robust
- **Maxout**: activation 자체를 학습 (piecewise linear convex), saturation/die 없음, 단 파라미터 증가

## 12. Activation 미분 (시험 가능!)

### Sigmoid 미분
```
g(z) = 1/(1+e⁻ᶻ)
g'(z) = g(z)(1 - g(z))
z > 10이면 g'(z) ≈ 0  ← vanishing gradient!
```

### Tanh 미분
```
g(z) = tanh(z)
g'(z) = 1 - tanh²(z) = 1 - g(z)²
z > 10이면 g'(z) ≈ 0
```

### ReLU 미분
```
g(z) = max(0,z)
g'(z) = 0 if z<0,  1 if z≥0

Leaky ReLU: g'(z) = 0.01 if z<0,  1 if z≥0
```

## 13. 실전 조언
- Feedforward net: **ReLU 사용** (learning rate 잘 튜닝)
- Leaky ReLU, maxout, ELU 시도
- tanh도 시도 (큰 기대는 X)
- **hidden unit에 sigmoid 쓰지 말 것**
- RNN/확률모델/autoencoder엔 sigmoid 흔함

## 14. 다음 문제: gradient를 어떻게 다 계산?
- Gradient descent로 학습하려면 모든 파라미터의 gradient 필요
- 직접 계산: 계산량 많음, loss 바뀌면 전부 다시 유도, 복잡한 모델엔 불가능
- → **Backpropagation** (다음 강의)

# Lecture 12: Backpropagation

## 1. Modern Neural Nets
- 핵심 아이디어는 80년대 이후 변화 없음 (backprop + gradient descent)
- 최근 발전 이유:
  - 더 큰 데이터셋 → 더 나은 generalization
  - 더 큰 네트워크 ← 하드웨어/소프트웨어 발전
  - 더 나은 알고리즘:
    - MSE → **Cross-entropy loss**
    - Sigmoid → **ReLU**

## 2. Backpropagation 개념
- **Chain rule을 재귀적으로 적용**하여 gradient 계산
- **Local process**: 각 노드는 자기 주변만 알면 됨
- 네트워크 전체를 추상화 가능 (loss나 상위 층이 바뀌어도 매번 다시 유도 안 해도 됨)
- 먼저 현재 activation 값을 계산해야 함
  - 주어진 입력 + 현재 파라미터로
  - 이 과정이 **forward propagation**

## 3. 핵심 흐름
```
Forward propagation:  입력 → 출력 (activation 계산)
Backward propagation: 출력 → 입력 (gradient 계산, chain rule)
```

## 4. Backprop 예시 1: Logistic Regression

### Forward
```
z = wᵀx + b
a = σ(z)
L(a, y) = -y log a - (1-y) log(1-a)
```

### Backward (chain rule)
```
da = dL/da = -y/a + (1-y)/(1-a)

dz = dL/dz = dL/da · da/dz
           = da · σ'(z)
           = da · σ(z)(1-σ(z))
           = da · a(1-a)
           = a - y          ← 깔끔하게 정리됨!

dw = dz · x
db = dz
```

**핵심 결과: dz = a - y** (예측 - 정답)

## 5. Backprop 예시 2: Two-Layer Neural Network

### Forward
```
z[1] = W[1]x + b[1]
a[1] = g(z[1])           ← g: 은닉층 activation
z[2] = W[2]a[1] + b[2]
a[2] = σ(z[2])           ← σ: 출력층 sigmoid
L(a[2], y)
```

### Backward (출력층 → 입력층 순서)
```
dz[2] = a[2] - y                       ← (예측 - 정답)

dW[2] = dz[2] · (a[1])ᵀ                 [n2,1]×[1,n1] = [n2,n1]
db[2] = dz[2]

da[1] = (W[2])ᵀ · dz[2]                 [n1,n2]×[n2,1] = [n1,1]

dz[1] = da[1] ∗ g'(z[1])                ← element-wise product!
      = (W[2])ᵀdz[2] ∗ g'(z[1])

dW[1] = dz[1] · xᵀ                      [n1,1]×[1,n0] = [n1,n0]
db[1] = dz[1]
```

### 핵심 패턴
- **dz = a - y** (출력층, cross-entropy + sigmoid/softmax일 때)
- **dW[l] = dz[l] · (a[l-1])ᵀ** (gradient = 현재층 error × 이전층 activation)
- **db[l] = dz[l]**
- **da[l-1] = (W[l])ᵀ · dz[l]** (error를 이전층으로 전파)
- **dz[l-1] = da[l-1] ∗ g'(z[l-1])** (element-wise, activation 미분 곱)

## 6. 일반화: layer l의 연산
```
parameters: W[l], b[l]
activation: g[l]

Forward:
  z[l] = W[l]a[l-1] + b[l]
  a[l] = g[l](z[l])

Backward:
  dz[l] = da[l] ∗ g[l]'(z[l])
  dW[l] = dz[l](a[l-1])ᵀ
  db[l] = dz[l]
  da[l-1] = (W[l])ᵀ dz[l]
```

## 7. 행렬 차원 체크 (시험 포인트!)
```
W[l]: [n[l], n[l-1]]
b[l]: [n[l], 1]
z[l], a[l]: [n[l], 1]

dW[l] = dz[l](a[l-1])ᵀ:  [n[l],1]×[1,n[l-1]] = [n[l],n[l-1]]  ✓ (W와 같은 모양)
da[l-1] = (W[l])ᵀdz[l]:  [n[l-1],n[l]]×[n[l],1] = [n[l-1],1]  ✓
```

## 8. Vectorized (minibatch)
- 여러 데이터를 한꺼번에 처리 → design matrix
- X: 각 열(또는 행)이 한 데이터
- 행렬 연산으로 GPU 병렬화

## 9. Forward / Backward Function
- 각 층을 **모듈(black box)**로 구현
- Forward: 입력 받아 출력 + 중간값 저장
- Backward: 상위 gradient 받아 하위 gradient 반환
- → PyTorch 같은 프레임워크의 autograd 원리

## 10. 전체 Training Algorithm
```
1: 모든 파라미터 초기화
2: repeat
3:   minibatch B를 D에서 뽑음
4:   forward: 모든 activation 계산
5:   cost 계산
6:   backward: 모든 gradient 계산
7:   파라미터 업데이트: w ← w - α∇L
8: until validation loss 수렴
9: 최종 파라미터 반환
```

## 핵심 요약 (시험)
1. **Backprop = chain rule 재귀 적용**
2. Forward로 activation 먼저 계산 → Backward로 gradient
3. **dz[L] = a[L] - y** (출력층, CE+softmax/sigmoid)
4. **dW[l] = dz[l](a[l-1])ᵀ**, **db[l] = dz[l]**
5. **da[l-1] = (W[l])ᵀdz[l]** → error 역전파
6. **dz[l] = da[l] ∗ g'(z[l])** → activation 미분 element-wise 곱
7. 행렬 차원이 W와 일치하는지 항상 체크

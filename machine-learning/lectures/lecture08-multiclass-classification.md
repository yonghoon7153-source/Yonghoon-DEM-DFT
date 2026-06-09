# Lecture 8: Multiclass Classification

## 1. Math Formulation
- x ∈ ℝᴰ, y ∈ {1, 2, ..., K}
- Find f(x): ℝᴰ → {1, 2, ..., K}
- One-hot encoding: y = (0,...,0,1,0,...,0)
- Weight matrix W: K×D, bias b: K-dim

## 2. Multiple Binary Classifiers

### 1-vs-All (1-vs-rest)
- K-1개 binary classifier
- f₁: 1 vs {2,3,...,K}, f₂: 2 vs {1,3,...,K}, ...
- 문제: 애매한 영역 (여러 클래스에 동시 속하거나 어디에도 안 속함)

### 1-vs-1
- K(K-1)/2개 binary classifier
- 모든 쌍에 대해 분류, 다수결
- 문제: transitivity 없음 (가위바위보 현상), 계산 비용 높음

## 3. Discriminant Functions — 해결책
- K개 scoring function: z₁, z₂, ..., z_K
- 분류: argmax_k z_k(x)
- 장점: 계산 저렴, 애매한 영역 없음

### Linear Discriminant
- z_k(x) = (wᵏ)ᵀx
- wᵏ: k번째 클래스와 높은 유사도(내적)를 가지는 벡터

## 4. Conditional Distribution as Discriminant
- z_k(x) = P(y=k|x) = P_wᵏ(y=k|x)
- Bayes Rule로 유도

## 5. Binary → Multiclass: Sigmoid → Softmax

### Binary Logistic Regression Review
- P(C=1|x) = σ(w₀ + wᵀx) = 1/(1+e⁻ᶻ)
- Bayes Rule로 유도:
  P(C=1|x) = P(x|C=1)P(C=1) / [P(x|C=1)P(C=1) + P(x|C=0)P(C=0)]
            = 1 / (1 + e⁻ᶻ)

### Multiclass 확장
- e^(z_k) = P(x|C=k)P(C=k)
- P(C=k|x) = e^(z_k) / Σ_{k'} e^(z_{k'})
- 이것이 **Softmax function**

## 6. Softmax Function
```
ŷ_k = softmax(z₁,...,z_K)_k = e^(z_k) / Σ_{k'} e^(z_{k'})
```
- Sigmoid의 multiclass 일반화
- 성질:
  - 모든 출력 ≥ 0
  - Σ_k ŷ_k = 1 (확률 해석)
  - K=2이면 sigmoid와 동일
  - argmax의 smooth approximation (softargmax)

### 구체적 예시
```
z = [5.8, 1.9, -3.2]  (dog, cat, alpaca)
exp: [330.3, 6.7, 0.04]
norm: [0.98, 0.0199, 0.0001]
→ dog!
```

## 7. Loss: Multiclass Cross-Entropy
```
L_CE = -Σ_k y_k · log(ŷ_k)
```
y가 one-hot이므로 정답 클래스 c에서만: L = -log(ŷ_c)

### Softmax-Cross-Entropy (수치 안정)
```
L_SCE = -Σ_k (y_k · z_k - y_k · log Σ_{k'} e^(z_{k'}))
```

## 8. Binary vs Multiclass 대응표

| | Binary | Multiclass |
|---|---|---|
| Activation | Sigmoid | Softmax |
| 출력 | 스칼라 ∈ (0,1) | K차원 벡터, 합=1 |
| Loss | -ylogŷ-(1-y)log(1-ŷ) | -Σ_k y_k log ŷ_k |
| Weight | w ∈ ℝᵈ | W ∈ ℝ^(K×D) |
| 분포 가정 | Bernoulli | Categorical |

# Lecture 16: CNN II - Batch Normalization

## 1. Data Preprocessing (입력 전처리)
- 입력 데이터를 조작해 학습을 쉽게
- 네트워크에 입력되기 **전에** 수행

### Mean Subtraction (평균 빼기)
- 각 차원의 평균을 빼기
- 기하학적 의미: 데이터 구름을 원점 중심으로 이동(centering)

### Normalization (정규화)
- 차원들을 비슷한 scale로
- 2가지 방법:
  - 평균 빼고 표준편차로 나누기
  - 각 차원을 min/max가 -1, 1이 되게
- 이유: scale 다른 차원은 동등하게 기여 못 함

### Decorrelation (탈상관)
- zero-centered 데이터의 공분산 행렬 구함
- SVD로 공분산의 eigenbasis에 데이터 투영

### Whitening (백색화)
- decorrelation 후, 각 차원을 eigenvalue로 나눠 scale 정규화

### 효과
- 정규화 → zigzag gradient update 감소 → 빠른 수렴
```
Unnormalized: 타원형 → zigzag (느림)
Normalized: 원형 → 직선 (빠름)
```

### Validation/Test에도 전처리? (시험 포인트!)
- **Yes!** 학습한 분포와 같은 분포를 inference에 기대
- **주의**: 전처리 통계(예: 평균)는 **training data로 계산**한 것 사용
- 왜? test 이미지는 한꺼번에 안 옴 (하나씩 올 수도) → 정확한 통계 계산 불가

## 2. Feature Normalization (활성값 정규화)
- 초기화를 정교하게 설계해서 zero-mean unit-variance를 얻는 대신
- **그냥 그렇게 만들어버리자!**
- 각 층의 activation 배치에 대해 정규화 적용
- 보통 **FC/conv layer 뒤, activation 앞**에 배치
```
FC → Norm → ReLU
```

### 정규화 차원 (용어)
```
N: minibatch 크기
C: 채널 수
H, W: 공간 차원 (높이, 너비)
C×H×W: hidden unit 수
```
- 어느 차원으로 정규화하느냐에 따라 종류가 달라짐

## 3. Batch Normalization (BN) ★
- **batch와 spatial 차원**으로 정규화
- CNN에 흔히 사용
- **training과 testing에서 다르게 동작** (왜?)
  - training 통계 사용하는데, batch마다 계산됨
  - batch는 매 iteration 바뀜
  - → training 중 본 통계의 **running average** 사용
  - running average = 전체 분포 통계의 대략적 추정
- PyTorch: model.train() / model.eval() 명시 필요

### BN 수식 (개념)
```
training: 각 batch의 평균 μ, 분산 σ²로 정규화
  x̂ = (x - μ_batch) / √(σ²_batch + ε)

inference: running average 사용
```

### Running Average (EWMA)
- inference 시: 입력이 하나씩 오거나 적음 → batch 통계 계산 불가
- activation 분포는 학습 내내 변함 (파라미터 업데이트되니까)
- 전체 분포 통계를 추정하고 싶음
- → 학습 중 통계의 running/moving average 사용
```
training 중:
  μ_running ← γ·μ_running + (1-γ)·μ_batch

inference:
  최종 running average로 정규화
```

## 4. 다른 Normalization 종류 (정규화 차원이 다름!)

| 종류 | 정규화 차원 | 특징 | 용도 |
|------|----------|------|------|
| **Batch Norm (BN)** | batch + spatial (N,H,W) | batch에 의존 | CNN |
| **Group Norm (GN)** | 채널 group + spatial | batch 무관 | 작은 batch |
| **Layer Norm (LN)** | 전체 층 hidden units | batch 무관 | FC, RNN, **Transformer** |
| **Instance Norm (IN)** | spatial만 | batch 무관 | Style Transfer |

### Group Normalization
- batch size 작을 때 BN 대안
- 큰 batch가 GPU에 안 들어갈 때 유용
- batch 작으면 batch 통계가 부정확 → GN이 해결
- 채널 일부(group) + spatial로 정규화

### Layer Normalization
- 전체 층의 hidden unit으로 정규화
- batch 무관
- FC, RNN, **Transformer**에 흔히 사용

### Instance Normalization
- spatial 차원만 정규화 (FC엔 안 씀)
- batch 무관
- Style Transfer에 사용

## 5. Feature Normalization 장점 (시험!)
- 깊은 네트워크 학습 쉬워짐
- **gradient flow 개선**
- 높은 learning rate 허용, 빠른 수렴
- 초기화에 robust
- 학습 중 **regularization 역할**
- test 시 overhead 없음 (running average 미리 계산)

## 6. Affine Transformation (Learnable γ, β) ★
- zero-mean unit-variance가 항상 좋은가? → 너무 강한 제약일 수도
- 해결: 정규화 후 **affine transform** 적용
```
y = γ·x̂ + β

γ (scale), β (shift): 학습 가능한 파라미터
```
- γ=√(σ²), β=μ로 학습하면 → **identity function 복원** (정규화 효과 끌 수 있음)
- 각 정규화마다 다른 차원:
  - **BN**: hidden unit마다 한 쌍 (CNN은 채널마다, spatial 공유)
  - **LN**: hidden unit마다 한 쌍
  - **IN**: 채널마다 (spatial 공유)

## 핵심 요약 (시험)
1. **Data preprocessing**: mean subtraction → normalization → decorrelation → whitening
2. **Test 통계는 training data로 계산** (test는 하나씩 올 수 있어서)
3. **Batch Norm**: batch+spatial 정규화, FC/conv 뒤 activation 앞
4. **BN은 train/test 다르게**: train은 batch 통계, test는 running average (EWMA)
5. **정규화 종류 = 정규화 차원의 차이** (BN/GN/LN/IN)
6. **Layer Norm = Transformer**, Instance Norm = Style Transfer
7. **Affine transform (γ, β)**: 너무 강한 제약 완화, identity 복원 가능
8. BN 효과: gradient flow 개선, 빠른 수렴, 초기화 robust, regularization

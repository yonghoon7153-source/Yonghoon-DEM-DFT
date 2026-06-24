# Lecture 17: CNN III - Architectures

## CNN 아키텍처 발전사 (ImageNet 우승자 흐름)
```
LeNet-5 (1998) → AlexNet (2012) → ZFNet (2013) → VGG (2014)
→ GoogLeNet (2014) → ResNet (2015) → SENet (2017)
"Revolution of Depth" (점점 깊어짐)
```

## 1. LeNet-5 (1998)
- 구조: CONV-POOL-CONV-POOL-FC-FC
- 5×5 conv (stride 1), 2×2 pooling (stride 2)
- 손글씨 숫자 인식

## 2. AlexNet (2012) — 첫 CNN 기반 우승자 ★
- Krizhevsky, Sutskever, Hinton, ILSVRC 2012 우승
- 총 파라미터: **60M**
- CONV1 출력: 55×55×96
- CONV1 파라미터: (11×11×3 + 1)×96
- MAX POOL 파라미터: **0!** (pooling은 파라미터 없음)

### 특징 (시험 가능!)
- **First use of ReLU**
- Local Response Normalization (지금은 안 씀)
- Heavy data augmentation
- Dropout 0.5
- Batch size 128, SGD+momentum(0.9)
- LR 10⁻², L2 weight decay 5×10⁻⁴
- 7 CNN ensemble: 18.2% → 15.4%
- GTX 580 GPU 2개에 분산 (그림이 반으로 나뉜 이유)

## 3. ZFNet (2013)
- AlexNet과 같지만 hyperparameter 개선
- CONV1: 11×11 stride 4 → 7×7 stride 2
- top-5 error: 16.4% → 11.7%

## 4. VGG (2014) — 작은 필터, 깊은 네트워크 ★
- Oxford VGG lab
- **핵심: 작은 필터(3×3), 더 깊게**
  - 3×3 CONV stride 1, pad 1
  - 2×2 MAX POOL stride 2
- 8층(AlexNet) → 16-19층(VGG16, VGG19)
- top-5 error: 11.7% → 7.3%

### 왜 작은 필터? (시험 핵심!)
- **3×3 conv 3개 쌓기 = 7×7 conv 1개와 같은 receptive field**
  - 1층: 3×3, 2층: 5×5, 3층: 7×7 (effective receptive field)
- 장점:
  - 더 깊음 → **더 많은 비선형성**
  - **더 적은 파라미터**: 3×(3²C²) = 27C² vs 7²C² = 49C²
- 메모리: 초기 CONV에 가장 많음
- 파라미터: 후기 FC에 가장 많음

## 5. GoogLeNet (2014) — 효율성 ★
- **핵심: 깊으면서 계산 효율적**
- 22층, **Inception module**
- FC 최소화 → **파라미터 5M만!** (AlexNet의 1/12, VGG의 1/27)
- ILSVRC'14 우승 (6.7% top-5 error)

### Inception Module
- 좋은 local network topology 설계 → 쌓기 (network within a network)
- **Naive inception**: 여러 필터 병렬 (1×1, 3×3, 5×5 conv + 3×3 pooling)
  - 출력을 depth(channel)-wise concatenate
- 문제: **계산 비쌈** (854M ops), depth가 계속 커짐 (pooling이 depth 보존)

### 1×1 Convolution (Bottleneck) ★
- **1×1 conv로 feature depth 감소**
- 각 픽셀에 같은 FC를 적용하는 것으로 해석
- spatial 차원 보존, depth만 감소!
- 예: 1×1 CONV 32필터, 각 필터 1×1×64 → 64차원 dot product
- inception에 bottleneck 추가: 854M → 358M ops

### 전체 구조
1. Stem network: CONV-POOL-CONV-CONV-POOL
2. Stacked inception modules
3. Classifier output: **Global Average Pooling** (비싼 FC 대신)
4. Auxiliary classification outputs: 하위 층에 추가 gradient 주입
- 총 22층 (병렬은 1층으로 카운트, auxiliary는 미포함)

## 6. ResNet (2015) — 매우 깊은 네트워크 ★★ (가장 중요!)
- **핵심: residual connection으로 매우 깊은 네트워크**
- 152층, ILSVRC'15 우승 (3.57% top-5, 인간 초월!)

### 동기: 깊을수록 나빠지는 역설
```
plain CNN을 깊게 쌓으면:
56층 모델이 20층보다 train/test 둘 다 나쁨!
→ overfitting 아님 (train도 나쁨) → UNDERFITTING!
→ optimization 문제 (깊은 모델이 최적화 어려움)
```

### 가설과 해결
- 깊은 모델은 표현력 더 큼 (파라미터 多)
- 깊은 모델이 얕은 모델을 흉내낼 수 있어야 함 (추가 층이 identity면 됨)
- 그런데 못 한다 = optimization 문제
- → **residual layer로 identity 학습을 쉽게!**

### Residual Block ★
```
직접 H(x)를 학습하는 대신, residual F(x) = H(x) - x를 학습
출력: H(x) = F(x) + x   (skip connection)

F(x) = 0이면 → H(x) = x (identity)
→ identity 학습이 매우 쉬움! (weight를 0으로만 하면 됨)
```

### Residual Block의 두 가지 좋은 성질 (시험!)
1. **L2 regularization 해석**
   - residual block weight를 0으로 → identity 계산
   - 모델이 필요 없는 층을 안 쓰도록 유도 (weight → 0)
   - 일반 CNN에선 weight=0이 무의미하지만, ResNet에선 "층 안 쓰기"
2. **Gradient flow** (매우 중요!)
   - residual connection = **gradient super highway**
   - backward에서 gradient가 잘 흐름 → 학습 쉽고 빠름

### Architecture
- residual block 쌓기, 각 block에 3×3 conv 2개
- 주기적으로 필터 수 2배 + downsample (stride 2)
- 시작: 추가 CONV, 끝: Global Average Pooling + FC(클래스 수)
- 깊이: 34, 50, 101, 152층
- 50+ 층: **bottleneck layer** (GoogLeNet처럼 효율화)

### Training
- 모든 CONV 뒤에 **Batch Normalization**
- SGD+momentum(0.9), LR 0.1, batch 256, weight decay 10⁻⁵
- **Dropout 안 씀**

## 7. 아키텍처 비교
- **VGG**: 메모리 최대, 연산 최대
- **GoogLeNet**: 가장 효율적
- **AlexNet**: 연산 적지만 메모리 무겁고 정확도 낮음
- **ResNet**: 적당한 효율 + 최고 정확도

## 8. ResNet 개선들
- **Improved residual block**: 정보 전파 경로 직접화
- **Wide ResNet**: depth보다 residual이 중요 → 너비 키움 (F×k 필터)
- **ResNeXt**: 병렬 경로로 residual block 너비 확장 (inception 유사)
- **Stochastic Depth**: 학습 시 일부 층 랜덤 drop (vanishing gradient 완화)
- **SENet (2017 우승)**: Squeeze-Excitation block, 채널 간 상호의존 모델링

## 9. ResNet 이후 발전
- **FractalNet**: residual 없이 깊게 (fractal 구조)
- **DenseNet**: 모든 층을 서로 연결 (dense block)
  - vanishing gradient 완화, feature 재사용
- **효율 네트워크** (모바일):
  - **SqueezeNet**: 1×1 squeeze + expand, AlexNet 정확도에 파라미터 50배 적음
  - **MobileNet**: **depthwise separable convolution**
    - = depthwise conv (공간) + pointwise conv (채널, 1×1)
  - ShuffleNet
- **NAS (Neural Architecture Search)**: RNN controller가 RL로 구조 설계
- **EfficientNet**: compound scaling (width/depth/resolution 균형)

## Main Takeaways (시험 정리!)
1. **AlexNet**: CNN으로 CV 잘 됨을 보임 (첫 CNN 우승, ReLU)
2. **ZFNet, VGG**: 더 큰/깊은 네트워크가 더 좋음 (VGG: 작은 필터)
3. **GoogLeNet**: 1×1 bottleneck으로 효율 (inception)
4. **ResNet**: residual connection으로 극도로 깊은 네트워크 학습
5. ResNet 이후: 인간 초월 → 효율 네트워크(MobileNet) + NAS

## 핵심 암기 포인트
- **Pooling은 파라미터 0**
- **3×3 conv 3개 = 7×7 conv 1개 receptive field, but 더 적은 파라미터 + 더 많은 비선형**
- **1×1 conv = depth 감소 (bottleneck), spatial 보존**
- **ResNet residual: H(x)=F(x)+x, identity 학습 쉬움, gradient highway**
- **깊은 plain net의 문제 = underfitting (optimization), not overfitting**
- **Global Average Pooling으로 FC 대체 (파라미터 절감)**

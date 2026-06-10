# Lecture 15: Convolutional Neural Networks (CNN)

## 1. CNN의 동기 (왜 FC를 안 쓰나?)
- 큰 이미지를 FC로 처리하면 파라미터 폭발!
- 예: 200×200 RGB 이미지
  - 뉴런 1개당 200×200×3 = 120,000개 weight
  - 같은 크기 5채널 출력 → 200×200×5 = 200,000 뉴런
  - 한 층에 너무 많은 파라미터 → overfitting 위험!

## 2. Inductive Bias (핵심 개념!)
- 데이터에 대해 하는 가정의 집합
- 이미지의 가정:
  - 각 픽셀은 **근처 픽셀과 관련** (local)
  - 비슷한 패턴이 **여러 위치에 나타남** (translation)
- 효과:
  - 더 나은 generalization, 데이터 적을 때 도움
  - 데이터가 아주 많으면 오히려 성능 제한할 수도
- CNN = 이미지용 inductive bias를 architecture에 녹인 것

## 3. 신경과학적 영감
- 인간 시각: Simple cells → Complex cells → Hyper-complex cells
- 각 cell은 이전 단계의 **local 영역**을 봄
- 각 cell은 공간상에서 **특정 패턴**을 찾음
- → CNN이 활용하는 3가지:
  - **Local connectivity** (지역 연결)
  - **Parameter sharing** (파라미터 공유)
  - **Pooling/subsampling**

## 4. Convolution 연산
- 적어도 한 층에서 일반 행렬곱 대신 **convolution** 사용하는 신경망
- 매 위치에서 가중평균 연산
- weight 패턴에 따라 다른 응답 → 다른 feature 감지

### 용어
- Input: 입력
- **Kernel (Filter)**: 가중치
- **Feature map (Activation map)**: 출력

### Cross-correlation
- convolution과 같지만 **kernel을 뒤집지(flip) 않음**
- 딥러닝 라이브러리는 cross-correlation을 구현하고 "convolution"이라 부름
- 둘 다 convolution이라 부름 (필요시 flip 여부 명시)

## 5. Filters (필터 = Feature Detector)
- 예: vertical edge detector (수직 엣지 감지)
- 기존 ML: 사람이 hand-design
- CNN: **학습으로 얻음** (예: AlexNet의 96개 11×11 필터)

## 6. RGB 이미지 convolution
- 여러 kernel 사용 (예: vertical line detector, horizontal line detector)
- 각 필터가 전체 depth(채널)를 관통

## 7. CNN 4가지 층
1. **Convolutional layer**
2. **Non-linear activation layer** (ReLU 등)
3. **Pooling layer**
4. **Fully-connected (FC) layer**
- 이들을 쌓으면 전체 CNN

## 8. CNN의 장점 (시험 핵심!)

### Parameter Sharing
- 유용한 feature(예: 윤곽)는 여러 위치에서 반복됨
- 같은 feature detector(필터)를 모든 위치에 사용 → 위치마다 재학습 X
- 이미지의 **translation-invariant 구조** 활용
```
Conv: 모든 공간 위치에서 같은 파라미터 공유
FC:   파라미터 공유 없음
```

### Sparse Connectivity (Sparse Interactions)
- 작은 kernel → 각 출력이 입력의 **local 영역**에만 의존
```
Conv: 작은 kernel → sparse connection
FC:   dense connection (모든 입력에 연결)
```

### 종합 효과
- 파라미터 수 대폭 감소
- 성능 향상 (generalization + efficiency)
- 가변 크기 입력 처리 가능 (flexibility)

## 9. Convolutional Layer 상세

### 필터 (3D)
- 공간(H,W)으로는 작음
- depth(채널)로는 입력 전체를 관통
- 각 필터 → 하나의 2D activation map 생성
- 여러 필터의 activation map을 depth로 쌓아 → output volume (3D)
```
Input volume (3D) ∗ 필터 1개 = activation map (2D)
Input volume (3D) ∗ 필터 N개 = output volume (3D, depth=N)
```
- 예: 첫 층 필터 3×3×3 (H×W×depth)
- **Receptive field** = 필터가 보는 공간적 범위

### Spatial Arrangement (출력 크기 제어 3 hyperparameter)
1. **Depth**: 출력 depth = 필터 개수
2. **Stride**: 필터를 몇 픽셀씩 이동
3. **Zero-padding**: 경계에 0을 얼마나 채움
- Stride & Padding이 출력의 공간 크기 결정

### Zero-padding
- 32×32를 5×5 필터로 반복 convolve → 32→28→24... 빠르게 줄어듦 (안 좋음)
- 경계 픽셀은 덜 사용됨 → 정보 손실
- Zero-padding: 입력 둘레를 0으로 채움
  - kernel 크기와 출력 크기를 독립적으로 제어
  - 경계 정보 보존
- **"same" padding**: stride=1이면 공간 크기 보존

### 출력 크기 공식 (시험 필수!)
```
입력: W
필터: F (보통 홀수)
패딩: P (한쪽당)
스트라이드: S

출력: O = (W - F + 2P)/S + 1
```

## 10. Pooling Layer
- CONV 층 사이에 주기적으로 삽입
- 기능:
  - 공간 크기 점진적 축소 → 파라미터/계산 감소 + overfitting 제어
  - receptive field를 효율적으로 키움
- 각 depth slice에 독립적으로 작동, **depth 불변**
- **파라미터 없음**
- **(local) translation invariance** 제공

### Max Pooling
- 가장 흔함: **2×2 max pooling, stride 2** → activation의 75% 버림
- 다른 종류: average pooling, L2-norm pooling

### Pooling 제거 추세
- pooling은 공간 정보 약간 손실
- 대안: CONV만 반복 (가끔 큰 stride 사용)
- GAN, VAE 등 generative model 학습에 중요

## 11. FC Layer
- 연결: 일반 MLP와 동일
- 역할: classification/regression 같은 high-level reasoning
- 공간 정보 없음 → FC 뒤엔 CONV 불가
- CNN 파라미터의 대부분을 차지할 수 있음

## 12. 전체 구조 (예: LeNet-5)
- layer 진행할수록: 입력 크기 ↓, 필터 수 ↑ (CNN 공통 경향)
- 이유 (hierarchical feature learning):
  - 복잡한 feature 수가 층마다 증가
  - 각 뉴런의 effective receptive field가 층마다 증가

## 13. Equivariance vs Invariance (시험 포인트!)
- **Equivariance**: 입력 변환 → 출력도 같이 변환 (변환 보존)
  - **Convolution은 shift-equivariant**: 입력 이동 → 출력 이동
- **Invariance**: 출력이 변환과 무관
  - **Max Pooling은 (local) shift-invariant**: 입력 이동해도 출력 동일

## 핵심 요약 (시험)
1. **FC는 이미지에 파라미터 폭발** → CNN 필요
2. **Inductive bias**: 이미지의 local + translation 가정
3. **CNN 3원리**: local connectivity, parameter sharing, pooling
4. **출력 크기: O = (W-F+2P)/S + 1** ★
5. **Parameter sharing + sparse connectivity** = 파라미터 ↓
6. **Pooling: 파라미터 없음, depth 불변, translation invariance**
7. **Convolution = equivariance, Pooling = invariance**
8. CNN 4층: Conv, Activation, Pooling, FC

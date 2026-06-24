# Lecture 13: Training Neural Networks (Hyperparameter Tuning)

## (Slide 2~22: Lecture 10 복습)
- SGD 약점 (local minima, saddle, poor conditioning)
- EWMA, Nesterov, AdaGrad, RMSProp, Adam
- Learning rate scheduling, second-order (Newton, L-BFGS)
- 실전: Adam(기본) / SGD+Momentum+decay(튜닝하면 더 좋음)
→ Lecture 10 노트 참조

## ★ 새 내용: Hyperparameter Tuning

## 1. Parameter vs Hyperparameter
| | Parameter (model parameter) | Hyperparameter (meta/free parameter) |
|---|---|---|
| 정의 | 학습으로 얻어짐 | 사람이 돌리는 "손잡이(knob)" |
| 예시 | weight, bias | learning rate, # layers, # hidden units, minibatch size |
| 역할 | - | 알고리즘 동작/시간/메모리/품질/수렴에 영향 |

- **Hyperparameter tuning = model selection** (정식 용어)

## 2. 두 가지 접근
- **Manual tuning**: hyperparameter가 뭘 하는지, 모델이 어떻게 generalize하는지 이해 필요
- **Automated (meta-learning, AutoML)**: 이해 부담 줄지만 계산 비용 큼

## 3. Manual Tuning 전략
- 기본: hyperparameter 값 넣고 → Cross-Validation으로 best 선택
- 도전: search space가 거대함
- 휴리스틱:
  1. **Coarse-to-fine sampling**
  2. **Random sampling > Grid search**
  3. **적절한 분포로 sampling**

### Coarse-to-fine Sampling
1. 큰 영역에서 듬성듬성 샘플 (각각 몇 epoch만)
2. 좋은 작은 영역에 집중해서 촘촘히 샘플

### Random Search > Grid Search (시험 포인트!)
- **Grid Search 문제**:
  - 어떤 hyperparameter는 더 중요(influential)함
  - 안 중요한 것을 튜닝하느라 계산 낭비
  - 낭비량이 non-influential 개수에 지수적
- **Random Search**:
  - 더 풍부한 탐색 (지수적으로 효율적)
  - 거의 매 시도마다 중요한 hyperparameter의 unique 값 테스트
  ```
  Grid: 중요한 축의 값이 몇 개만 반복됨
  Random: 중요한 축의 값이 매번 다름 → 더 잘 탐색
  ```

### 적절한 Sampling 분포
- Binary/discrete: Bernoulli/multinoulli
- Positive real-valued (예: learning rate): **log-scale uniform**
  ```
  예: [0.0001, 1] 범위 샘플링
  Uniform: 대부분 0.1~1에 몰림 (작은 값 거의 안 뽑힘)
  Log-uniform: 10⁻⁴, 10⁻³, 10⁻², 10⁻¹ 골고루 ← better!
  ```

## 4. 추천 단계 (Recommended Steps) ★ 시험 가능

### Step 1: Check initial loss
- weight decay 끄고, 초기화 시 loss 확인 (sanity check)
- 예: softmax C classes → loss ≈ log(C)여야 함
  (C=10이면 log(10)≈2.3)

### Step 2: Overfit a small sample
- 작은 샘플(~5-10 minibatch)로 100% training accuracy 목표
- architecture, learning rate, weight init 조정
- **Loss 안 내려가면**: LR 너무 낮음, 나쁜 초기화, 또는 네트워크 너무 작음(underfit)
- **Loss가 Inf/NaN으로 폭발**: LR 너무 높음, 나쁜 초기화

### Step 3: Find LR that makes loss go down
- 이전 architecture 사용, 전체 데이터, 작은 weight decay 켬
- ~100 iteration 내에 loss가 크게 떨어지는 LR 찾기
- 시도할 LR: 10⁻¹, 10⁻², 10⁻³, 10⁻⁴

### Step 4: Coarse grid, ~1-5 epochs
- Step 3 근처의 LR과 weight decay 몇 개 선택
- 시도할 weight decay: 10⁻⁴, 10⁻⁵, 0

### Step 5: Refine grid, train longer
- Step 4의 best 모델 → 더 길게(~10-20 epochs) 학습
- LR decay/schedule 없이

### Step 6: Monitor performance curve

### Step 7: GOTO Step 5 (반복)

## 5. Monitoring Performance Curve
- 가치: hyperparameter tuning, under/overfit 감지
- Loss가 noisy할 수 있음 → scatter plot + moving average로 추세 확인
- Example: 처음에 평평하다 떨어지면 → 나쁜 초기화 의심
- **Update ratio 추적**: ||Δw|| / ||w|| ≈ 0.1%~1% 권장
  - 크게 벗어나면 update가 너무 빠르거나 느림

## 핵심 요약 (시험)
1. **Parameter(학습됨) vs Hyperparameter(사람이 설정)**
2. **Hyperparameter tuning = model selection**
3. **Random search > Grid search** (중요한 hyperparameter를 더 잘 탐색)
4. **Learning rate는 log-scale로 sampling**
5. **초기 loss sanity check**: softmax C classes → log(C)
6. **Overfit small sample**으로 디버깅

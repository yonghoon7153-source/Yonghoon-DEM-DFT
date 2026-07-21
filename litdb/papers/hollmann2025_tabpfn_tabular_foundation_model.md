# Hollmann 2025 — TabPFN: 소데이터 표형(tabular) 파운데이션 모델 (Nature)

- **서지**: Hollmann, Müller, Purucker, Krishnakumar, Körfer, Hoo, Schirrmeister, Hutter,
  "Accurate predictions on small data with a tabular foundation model", *Nature* 637, 319–326
  (2025-01-08), DOI 10.1038/s41586-024-08328-6.  Open access.  Freiburg ML Lab + Prior Labs.
- **분류**: ML 방법론 (배터리 아님) — 우리 5-phase ML 트랙(predictor)·R_int Phase 3 ML의 도구 후보.
- **한 줄**: 수백만 개 **합성 데이터셋으로 사전학습**한 트랜스포머가 임의의 소규모 표 데이터에
  대해 **경사하강 없이 단일 forward pass(ICL)로** 학습+예측을 수행 — ≤10,000행/500특징에서
  4시간 튜닝한 GBDT(CatBoost/XGBoost)를 **2.8초(분류)/4.8초(회귀)** 만에 능가.

## 1. 방법 핵심
- **Prior-data Fitted Network (PFN) + in-context learning**: (X_train, y_train, X_test)를 통째로
  입력받아 y_test 분포를 출력하는 트랜스포머.  학습 = "데이터셋을 푸는 알고리즘 자체"를 학습.
- **합성 prior**: ~1억 개 합성 데이터셋 (인과 DAG → 랜덤 NN/트리 엣지 매핑 + 노이즈 + 결측/
  이상치/범주형/왜곡 주입) — 실데이터 0으로 사전학습, 베이지안 사후예측 근사라는 이론 해석.
- **아키텍처**: 2D 어텐션 (1D feature-attention × 1D sample-attention) ×12층 — 행/열 구조를
  직접 인코딩.  회귀 출력 = piecewise-constant (Riemann) **전체 예측분포** (다봉 가능 —
  이중슬릿 광강도 분포 재현 데모, 1.2s vs CatBoost 분위수 조립 169.3s).
- 사전학습 8×RTX2080Ti 2주 1회 — 사용은 소비자 GPU 1장(CPU 가능).

## 2. 결과 (AutoML Benchmark + OpenML-CTR23; 29 분류/28 회귀, ≤10k행/500특징)
- 분류: normalized ROC AUC **0.939 (기본값)** vs CatBoost 0.752(기본)/튜닝 대비 +0.13 —
  4h 튜닝 앙상블보다 2.8s 기본값이 우위 = **5,140× 스피드업**.
- 회귀: normalized −RMSE **0.923** vs CatBoost 0.872(기본), 튜닝 대비 +0.093 = **3,000×**.
- 강건성 (Fig 5a): 무정보 특징·이상치에 신경망답지 않게 둔감 (MLP는 붕괴); **행 절반만으로
  CatBoost(전체 행) 성능** 재현; 결측/범주형/행·열 수 서브그룹 전부에서 우위 유지.
- TabPFN(PHE, 자체 앙상블) ROC AUC 0.971 > AutoGluon 0.914 (4h); Kaggle Tabular Playground
  5/5 승 (<10k 행).  ref.14 벤치(트리 우위로 유명)에서도 전 베이스라인 능가.
- 부가기능: fine-tuning, **데이터 생성**(증강), **밀도추정**(이상탐지), 재사용 임베딩.

## 3. 한계 (정직)
- ≤10k행/500특징 스케일 검증 — 대용량은 범위 밖.  외삽(훈련범위 밖)은 여전히 취약 계열.
- 블랙박스 — 물리식 같은 해석가능성/단조성 보장 없음 (특징중요도는 permutation 등 사후).
- 추론 시 train 데이터를 컨텍스트로 항상 지참 (모델=알고리즘, 파라미터에 데이터 저장 안 됨).

## 4. 우리 프레임 연결 (comparison_vs_ours)
- **정확히 우리 체급**: 코퍼스 n=88–132 케이스 × ~수십 특징 = TabPFN 스위트스폿.
  현행 predictor(GPR/RF, sklearn·WSL)의 직접 대체/보완 후보 — 튜닝 0, 분포 출력(우리
  Bayesian PI 관행과 정합), 결측 견고(fallback-flag 케이스).
- **물리 스케일링 법칙(σ_ionic 5-param 0.975 / σ_e 8+2 0.953 / κ Ridge 0.90)과의 관계**:
  대체 아님 — 물리식 = 해석·외삽·논문 서사 담보, TabPFN = ① 신규 타깃 빠른 베이스라인
  ② 잔차 사냥(TabPFN이 물리식을 이기는 영역 = 남은 구조신호 증거) ③ 대량 설계 스크리닝.
- **적용점**: (a) 설계→전-메트릭 서로게이트 = 5-phase Phase 3 그 자체; (b) STEP4 곡선 스칼라
  (delivered/knee/η) 서로게이트 — 런 수 적을수록 유리; (c) R_int 프로젝트 Phase 3
  (BOL지표→cycling 견고성); (d) active learning(우리 active_learning_suggest 계보)의 획득함수용
  분포.  ⚠ 생성기능으로 만든 합성 케이스는 학습보조 전용 — 앵커 아님(§F1).

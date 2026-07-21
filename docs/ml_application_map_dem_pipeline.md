# ML 적용 지도 — 느린 파이프라인 구간 × TabPFN/랩-ML (2026-07-21)

입력 자료: ① Hollmann 2025 TabPFN (Nature; litdb 정본 카드
`hollmann2025_tabpfn_tabular_foundation_model.md`) ② BML 랩 덱 "머신러닝 모델의 이해"
(아래 §4 digest) ③ 기존 ML 트랙 정독 (5-phase 로드맵 Phase 1 완료: σ_ionic 5-param
LOOCV 0.975 / σ_e 8+2 0.953 / κ Ridge-14 0.90; predictor_engine GPR/RF; Phase 2–5 대기)
④ **Duquesnoy 2023 digest 정독** (litdb `duquesnoy2023_ml_*` — 우리 비전의 published
archetype: Sobol DOE → SISSO 해석식 → GP-Hedge 베이지안 다목적최적화 → 실험검증 닫힌
loop) ⑤ 정본(DFT) 브랜치 `kb/platforms/ml_automation_platforms.md` (BO 도구 skopt/BoTorch).

## 0. 세 조각의 자리 (Duquesnoy §8과 통합)
| 조각 | 역할 | 출처 |
|---|---|---|
| **물리 스케일링 법칙** (σ 삼중, LOCKED prior) | 해석·외삽·인과 — 우리 소유 | Phase 1 완료 |
| **SISSO** (해석식 자동발견) | 손유도 폼의 교차검증 + per-metric 해석식 엔진 | Duquesnoy §8.A-2 |
| **TabPFN** (분포-출력 소데이터 서로게이트) | 스크리닝·잔차사냥·BO 내부 surrogate — 튜닝 0 | 본 문서 §3 |
루프 기계장치는 Duquesnoy 것: **Sobol DOE**(코퍼스 갭 CN≥7·중간두께 채우기) +
**스칼라화 C_f + GP-Hedge BO** (surrogate 자리에 GP 대신 TabPFN 분포를 꽂는 변형 가능).
= "설계수치 → 최적 미세구조" 역설계 loop 를 우리 기계론 predictor 위에서 닫는 청사진.

## 1. 어디가 느린가 (wall-clock 병목)
| 단계 | 시간 | ML 대체 가능성 |
|---|---|---|
| DEM 압밀 (LIGGGHTS) | 시간~일 | ◎ 스크리닝 서로게이트 (메트릭 예측으로 런 자체 회피) |
| MPM 압밀+payload (V100) | 수십분~시간 | ◎ 〃 (porosity/coverage 예측) |
| STEP3 σ 필드솔브 (CG 2.9M dof) | 수십분 | ◎ 〃 (σ 삼중 예측 — Phase 1 형식이 이미 함) |
| STEP4 시간전개 (2C CCCV V100) | 시간~수시간 | ○ 곡선 스칼라 서로게이트 (런 수 적어 소데이터 ML 적합) |
| A10 100사이클 원장+RNM | 분 (후처리) | △ 불필요 (이미 빠름) — 대신 궤적→파라미터 학습엔 적합 |
| **설계점 1개 전체 체인** | **1~2일** | **핵심 타깃: 후보 스크리닝을 초 단위로** |

## 2. TabPFN이 정확히 우리 체급인 이유
- 코퍼스 n=88–132 케이스 × 수십 특징 = TabPFN 검증범위(≤10k행/500특징)의 소데이터 끝.
- 튜닝 0 (기본값 2.8–4.8 s가 4 h-튜닝 GBDT 능가) → sklearn GPR/RF 튜닝 루프 제거.
- **전체 예측분포 출력** = 우리 Bayesian PI 관행(σ_ionic Laplace, bootstrap 밴드)과 정합
  — active_learning_suggest의 획득함수에 바로 연결.
- 결측/이상치 견고 = fallback-flag·phantom 케이스가 섞인 실코퍼스에 유리.
- GPR의 O(n³)·커널 선택 부담(랩 덱 단점 슬라이드) 없음.  ⚠ 외삽 취약은 트리계와 동일
  — 코퍼스 볼록껍질 밖 설계는 물리 스케일링 법칙이 담당 (역할분담).

## 3. 적용 지도 (우선순위순)
1. **P3-TabPFN (5-phase Phase 3 그 자체)** — 설계 노브(조성·P:S·크기·두께·압력·첨가제)
   → full_metrics 전체(σ 삼중, porosity, coverage, CN, τ, fracture …) 멀티타깃 예측.
   기존 계획의 GPR/RF 자리에 TabPFN 추가 → 타깃당 5초, 튜닝 없음.  **새 설계점 수천 개를
   초 단위 스크리닝 → 시뮬은 top-k만** (1~2일/점 → 사실상 즉답 + 확정 런).
2. **STEP4 곡선 서로게이트** — (구조 메트릭 + C-rate + R_int + D_s split) → delivered %,
   knee V, η 분해 스칼라.  런 수십 개 = 소데이터 극한이라 TabPFN 최적; 분포 출력이
   "이 조건은 런 해볼 가치 있나"를 정직하게 답함.
3. **R_int 프로젝트 Phase 3 ML** — BOL 구조지표 → cycling 견고성 (R_int(N) 파라미터,
   retention).  A10 원장 출력(f_broken(N)·A_rel(N))이 학습 특징으로 합류.
4. **물리식 잔차사냥** — TabPFN을 σ 삼중의 물리식 잔차에 학습시켜 물리식을 유의하게
   이기는 영역 = 남은 구조신호의 증거 (형식 추가 근거를 데이터로 확보; ⚠ CLAUDE.md
   "form 추가 금지" 원칙과 충돌 않게 **진단 전용** — 발견 시 데이터 확충으로 대응).
5. **부가기능**: 임베딩 → 케이스 유사도 (비슷한 기존 런 재사용 제안); 밀도추정 → 코퍼스
   갭/이상 케이스 탐지 (EXCL 감사 보조); 생성 → 합성 케이스 (⚠ 학습보조 전용, 앵커 금지 §F1).

## 4. BML 랩 덱 digest ("머신러닝 모델의 이해", Hanyang BML, 26 pp)
- 구성: ML 정의(입력=EIS/DRT 특징 예: logp32_t, p3_h_ratio → 출력=SOH/저항/Severe 분류)
  → 지도/비지도/강화 → 분류 vs 회귀 → **9모델 각론** (GPR, KNN, Decision Tree, Random
  Forest, SVM-RBF/Linear, LogReg L1/L2, Ensemble; 각 이름유래·원리·장단점·특징중요도
  [GPR 1/길이척도, KNN·SVM Permutation/SHAP, DT MDI ΔGini, RF MDI 평균, 선형 |계수|])
  → 요약표(해석력/비선형성/대용량 적합) → 기타(NB, MLP, LightGBM/CatBoost, PCA, HC,
  AdaBoost) → **모델 선택 가이드 5규칙** (①해석 중요→DT/LogReg/SVM-L ②정확도
  최우선→RF/Stacking ③**데이터 적고 불확실성 필요→GPR** ④빠른 baseline→KNN/NB/LogReg
  ⑤특징 자동선택→L1/XGBoost).
- 우리 매핑: 덱 규칙 ③(소데이터+불확실성=GPR)이 우리 predictor의 현행 선택과 일치 —
  **TabPFN은 그 ③ 칸의 2025 업그레이드** (분포 출력 유지 + O(n³)/커널 부담 제거).
  덱의 특징중요도 방법론(permutation)은 TabPFN에도 그대로 적용 가능 (모델-비종속).
- 덱은 랩 임피던스-ML(DRT→Severe/SOH) 맥락 — 우리 DEM 메트릭 예측과 특징만 다르고
  방법 카탈로그는 공유.  랩 공동 어휘로 이 문서의 §3 항목을 설명할 때 이 덱 용어 사용.

## 5. 실행 순서 제안 (승인 시)
1. Phase 2 (단일 데이터층: full_metrics ∪ grade ∪ fracture 통합 벡터) — 원래 계획 그대로,
   TabPFN/GPR 공용 학습행렬.  2. WSL에 `pip install tabpfn` (PyTorch; V100 가능) →
   σ 삼중 + porosity 4타깃 벤치: TabPFN vs 물리식 vs GPR (LOOCV 동일 프로토콜).
   3. 이기는 조합으로 Phase 3 predictor 확장 + 스크리닝 UI (webapp what-if).
   ⚠ 클라우드 컨테이너는 sklearn/torch 없음 — 정적 배선만, 실학습 = WSL (기존 규약).

## 6. 수업 노트 브랜치 정독 (claude/linear-regression-lecture-DaaRi, 2026-07-22)
한양대 데이터사이언스 ML 수업 시험노트 15편 (중간 L2–5: 선형대수/확률·선형회귀·분류·SVM /
기말 L8–17: softmax·최적화(SGD/momentum/Adam)·MLP·역전파·훈련/튜닝·정규화·CNN·BN·아키텍처).
README에 "향후 DEM/DFT + ML 관련 내용 추가 예정" 명시 — 이 지도가 그 연결의 초안.

**수업 ↔ 프로젝트 로제타 표** (이미 하고 있던 것의 교과서 이름):
| 수업 개념 | 우리 프로젝트에서의 실체 |
|---|---|
| L3 정규방정식 w*=(XᵀX)⁻¹Xᵀy | σ 스케일링 법칙의 OLS fit (log-공간 선형회귀) |
| L5 "features as part of model" (수제 φ) | 물리-잠금 descriptor (√φ_eff·CN²·cov^½ = 손설계 φ) |
| L5→L11 "φ도 학습" (DL) | TabPFN/SISSO = φ 자동화의 표형 버전 |
| L14 L2(Ridge/weight decay) | σ_thermal Ridge-14 (α=0.05) 그 자체 |
| L14 L1 sparse selection | Stage 22.5의 약항 4개 제거 = 수동 L0/ablation |
| L4 bias-variance·CV | LOOCV 규약, n/k 비율 관리, over-fit 판정 (16→14 feat) |
| L13 random>grid·log-uniform 샘플링 | 하이퍼파라미터/스윕 설계 규약 (+Duquesnoy Sobol이 상위호환) |
| L9–10 SGD/momentum/Adam | (우리는 closed-form OLS라 불사용) BO 내부·NN 훈련 시 필요 지식 |
| L15 CNN inductive bias (local+공유) | ★미래: 복셀 sid 그리드 → 필드/σ 예측 3D-CNN 서로게이트 (STEP3 대체 후보 — 필드 샘플 수 부족이 관문, long-term) |
| L14 Ensemble/Bagging | TabPFN(PHE)·RF의 원리; 다중-시드 케이스 평균과 동형 |

시사점: ① 수업 범위(선형→NN→CNN)가 우리 스택의 이론 기반을 정확히 커버 — 논문/발표에서
"우리 폼 = physics-prior 선형회귀 + Ridge, ML 확장 = TabPFN/SISSO/BO"를 수업 용어로 설명
가능. ② 새 아이디어 1건: L15–17의 CNN(공간 inductive bias)을 우리 복셀 그리드(sid/필드)에
적용하는 **필드-레벨 서로게이트**는 표형 predictor와 별개 축 — 데이터(필드 스냅샷 수십 개)
부족으로 지금은 future, Phase 4(2D synth)와 합류 지점만 기록.

## 7. argyrodite-ml(DFT/MLIP) 브랜치 자산 이식 (2026-07-22 확인)
브랜치 `claude/argyrodite-ml-{prediction-ozuoX,migration-kDtHW}` = DFT/MLIP 프로그램
(db/ 조성·물성 JSON + QE/MLIP 템플릿 + kb/ 방법론·논문 digest — "PDF 먹인" 산출물).
정본은 friendly-meitner로 이관됨 (kb/platforms, choi2025_mlip 카드 확인).  **DEM 쪽에
직접 이식 가능한 자산 3건**:
1. ★★ **Wad(계면 접착에너지) 방법론** (`kb/methodology/adhesion_energy.md`: isolated-slab
   Wad=(E_SE+E_NCM−E_interface)/A, v5 crystalline+surface-MQA, cell-matching 규약, UMA
   MLIP 검증 R=+0.989) → **A10의 정직 갭 "AM-SE 계면 G_c 실측 부재"를 계산 앵커로 충전**
   (Wad = 정확히 그 계면 분리에너지; Bucci 1–10 J/m² 스윕을 계산값으로 대체 가능) +
   LPSCl 표면에너지 2γ_s → Griffith G_c로 2.8±1.8 밴드 교차검증.
2. ★ **SDCP E_bind DFT (A4′ 유일 잔여)**: 같은 Wad 템플릿/워크플로를 SDCP(전도고분자)–
   NCM/SE 계면에 이식 → σ_SDCP 원장의 "Li⁺ DFT/펠릿 정량 앵커 예정" 칸 실행 경로 확보 (gabia).
3. **BO/자동화 스택 참조**: atomate2·BoTorch·dscribe (kb/platforms) — Phase 3 BO 도구
   선정 시 DFT 프로그램과 공용 스택으로 통일 (skopt=Duquesnoy GP-Hedge 계열).

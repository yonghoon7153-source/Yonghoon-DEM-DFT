# 강의 이론 → 우리 DEM/DFT ML 적용 매핑 (Stage 5)

이 문서는 `lectures/`의 ML 이론을 **우리 프로젝트의 실제 production form**에 연결한다.
핵심 메시지: **우리의 transport-triad(σ_ionic / σ_electronic / σ_thermal) 스케일링 법칙은
"물리로 구조화된 선형회귀 + 정규화"** 그 자체다.  강의 노트가 곧 이 work의 교과서적 근거.

(form·계수·LOOCV 수치의 1차 출처는 `CLAUDE.md`의 σ_ionic / σ_e / σ_thermal FINALIZED 섹션.)

---

## 0. 한눈에 보는 대응표

| 강의 개념 | 강의 | 우리 production 적용 | 위치 |
|---|---|---|---|
| Normal equation `w*=(XᵀX)⁻¹Xᵀy` | L3 | σ_ionic 5-param OLS, σ_e 8-param OLS — **log-공간 선형회귀** | `generate_comparison_plots.py` `_stage_e_global_fit`, `_electronic_fit` |
| Pseudoinverse `(XᵀX)⁻¹Xᵀ` | L2 | 동일 OLS의 해법 (numpy `lstsq`) | 위 |
| Bias trick (feature에 1 추가) | L3 | 절편항 `a`(ionic), `p_τ`(e), log-offset | C(τ) logpoly2 상수항 |
| MLE: Gaussian → ℓ₂(MSE) | L4 | log σ 잔차에 ℓ₂ → OLS 정당화 | 모든 σ form |
| Generalization = test error | L3/L4 | **LOOCV** = 모든 form의 controlling metric | `nested_cv_sat.py`, `electronic_nested_cv.py` |
| Cross-validation (idea #4) | L4 | LOOCV(전 case) + nested-CV(form 선택 편향 제거) | `nested_cv_sat.py` |
| L2 / Ridge / weight decay | L14 | **σ_thermal Stage T1 = Ridge α=0.1**, 14 feature | `_thermal_fit(...,alpha)` |
| L1 / Lasso = sparse + selection | L14 | σ_e Stage 22.5 — ablation으로 4약항 제거(WEAK BLOCK) = **물리적 Lasso** | `electronic_ablation_full.py` |
| Occam's razor / overfitting | L14/L4 | "DO NOT add more terms — info-theoretic ceiling" 규율 | CLAUDE.md 전반 |
| Bias–Variance tradeoff (U자) | L4 | n/k 비율 규율 (ionic 18:1, e 9.5:1, thermal 6:1) | `final_form_status.py` |
| Bagging / ensemble (model averaging) | L14 | **bootstrap PI band** (ionic B=500, e B=200) | `_BOOTSTRAP_CACHE` |
| Multivariate Gaussian N(μ,Σ) | L2 | **GPR predictor** (예측 + Bayesian PI) | `predictor_engine.py` |
| Non-parametric (RF, k-NN) | L4 | **RandomForest predictor** 대안 | `predictor_engine.py` |
| Curse of dimensionality | L4 | feature 늘리면 corpus gap → 외삽 위험 (high-φ corner) | σ_e 2mAh outlier 서사 |
| Gradient descent / SGD | L9/L10 | sklearn GPR·RF 내부 최적화 (closed-form 없는 모델) | predictor 학습 |
| Normalization (zero-mean/unit-var) | L4 | feature 표준화 후 Ridge (collinearity 완화) | thermal 14-feature |
| Information / entropy | L2 | "information-theoretic ceiling" — 5 OLS가 solver 출력을 압축하는 한계 | ionic close-out |

---

## 1. Linear Regression (L3) — σ_ionic / σ_e의 뼈대

강의 L3의 결론은 `min_w ||Xw−y||²` → **normal equation `w*=(XᵀX)⁻¹Xᵀy`**.
우리 σ form은 겉보기엔 power-law 곱(`σ_grain·(φ_eff)^½·CN²·cov^½·f_p³·…`)이지만,
**log를 취하면 정확히 선형회귀**가 된다:

```
log σ = log σ_grain + ½·log φ_eff + 2·log CN + ½·log cov + 3·log f_p
        + [a + b·lnτ + c·(lnτ)² + β_P2·P2 + β_F·log f_intact]
        └──────────────── 이 대괄호가 OLS로 fit하는 선형부 ────────────────┘
```
- **고정 지수(½, 2, ½, 3)** = 물리(percolation·Holm·isotropy) → design matrix `X`의 *고정* 열.
- **LIVE 계수(a,b,c,β_P2,β_F)** = L3의 `w` → `lstsq`로 normal equation 푸는 대상.
- **Bias trick(L3 §7.5)** = 절편 `a`. feature에 상수열 1을 넣어 weight에 흡수한 것과 동일.

→ 즉 σ_ionic은 **"물리가 일부 열을 고정한 제약 선형회귀"**. L3의 closed-form이 그대로 엔진.
σ_e Stage 22.5(8 LIVE OLS)도 동일 구조 — Trevisanello 끝점·φ_AM⁴·√A는 LOCKED 열, 나머지 8개가 `w`.

**왜 ℓ₂(MSE)인가 (L4 §2–3):** log σ 잔차가 Gaussian이라 가정 → MLE → ℓ₂ loss.
classification이 아니라 연속값 회귀라서 0-1/CE가 아닌 MSE가 자연 손실.

---

## 2. Regularization (L14) — σ_thermal은 교과서적 Ridge

σ_ionic/σ_e는 OLS로 충분했지만 **σ_thermal은 다르다**(CLAUDE.md Stage T1):
- κ는 **multi-pathway**(AM-AM + AM-SE + SE-SE 병렬) → 단일 backbone power-law 불가
  (순수 power-law LOOCV 천장 0.59).
- 14개 구조 feature가 필요하고, n_fit=82 → **n/k≈6:1로 빡빡** + feature 강한 공선성
  (Bruggeman 비율들이 porosity와 상관).

→ 이것이 **L14 §5의 L2/Ridge 도입 동기 그 자체**:
```
J(w) = Σ(log κ_pred − log κ)²  +  α·||w||₂²      (α=0.1, validation으로 선택)
```
- **공선성 shrinkage** = Ridge가 하는 일(L14: "큰 magnitude에 더 큰 penalty, 미분가능").
- **bias(절편)는 penalize 안 함**(L14 §4 시험포인트) — 우리 Ridge도 절편 제외.
- α=0.1은 **validation으로 고정한 hyperparameter**(L14 §4) — `thermal_push_higher.py`의 α-sweep으로 결정.

**L1/Lasso는 안 쓰지만 효과는 구현했다 (중요 인사이트):**
σ_e Stage 22.5는 ablation으로 4개 약항(β_v, β_AC, β_fpth, β_logrSE)을 **정확히 0으로** 제거(WEAK BLOCK,
joint ΔLOOCV +0.0060).  이는 L14의 **Lasso(sparse + selection)와 같은 목표**를 — L1 penalty 대신
**물리-가이드 ablation + LOOCV**로 — 달성한 것.  각 항이 *물리적 의미*를 유지해야 하므로
자동 L1보다 ablation이 맞다(0이 된 항이 왜 0인지 설명 가능).

**Early stopping / Ensemble (L14 §6–7):**
- Occam·early-stop 정신 = "DO NOT add more form terms" 규율. LOOCV가 안 오르면 멈춘다.
- **Bagging(L14 §7) = 우리 bootstrap PI band**: B=500 resampling으로 잔차 분포 → per-case 68% PI.
  "다른 데이터 → 다른 model → noise 평균" 그대로(`_BOOTSTRAP_CACHE`).

---

## 3. Generalization · Overfitting (L3/L4/L14) — n/k 규율의 근거

- **Generalization error는 직접 못 잰다(L3 §3)** → test error로 근사 → 우리는 **LOOCV**로 근사.
  cross-validation(L4 idea #4)이 train/val/test 단순분할보다 robust → 작은 corpus(n≈80–100)라 LOOCV 채택.
- **Overfitting 민감조건(L14 §1) = "작은 데이터 + 큰 hypothesis class"** → 우리 corpus가 정확히 작은쪽.
  그래서 **n/k 비율**(ionic 88/5=18:1, e 76/8=9.5:1, thermal 82/14=6:1)을 overfit-margin 지표로 관리.
- **nested-CV**(`nested_cv_sat.py`)는 form *선택* 자체의 편향까지 제거 — L4가 경고한
  "test에 overfitting(idea #2)"을 form-screening 레벨에서 차단.  φc 재선택 금지(CLAUDE.md ⚠)도 같은 이유.
- **Bias–Variance U자(L4 §12)**: 항을 더 넣으면 train↓ but LOOCV↑(variance) → "info-theoretic ceiling"에서
  멈추는 게 U자 최저점. σ_e MINIMAL(5 LIVE)은 과소, Stage 22.5(8 LIVE)가 최저점.

---

## 4. Predictor (Phase 3–5) — GPR/RF로 가는 다리

Phase 1(transport triad)은 *손으로 만든* 선형회귀 form.  Phase 3+의 predictor는
설계변수 → 전체 metric을 학습하는 **일반 ML 모델**:
- **GPR(Gaussian Process)** = L2 Part2의 **multivariate Gaussian N(μ,Σ)** + precision matrix.
  예측 평균 μ + 공분산 Σ로 **Bayesian PI**를 바로 준다(σ_ionic Laplace PI의 일반화).
- **RandomForest** = L4 §8의 **non-parametric**(파라미터가 데이터와 함께 증가) 대안.
  form 가정 없이 비선형 상호작용 포착 — multi-pathway κ처럼 분석 form이 약한 타깃에 유리.
- closed-form 없는 이 모델들은 L9/L10의 **gradient descent / 2nd-order 최적화**로 학습(sklearn 내부).
- **Curse of dimensionality(L4 §11)**: feature를 늘릴수록 corpus gap(high-φ corner 등)에서 외삽 →
  σ_e 2mAh outlier가 정확히 이 현상. 해법은 "term 추가"가 아니라 "그 corner에 multi-seed 데이터".

---

## 5. 시험포인트 ↔ 우리 규율 (빠른 참조)

| L14 시험포인트 | 우리 프로젝트 대응 |
|---|---|
| L1=sparse·미분불가 / L2=shrinkage·미분가능 | σ_e=ablation-sparse / σ_thermal=Ridge-shrinkage |
| bias는 penalize 안 함 | Ridge·OLS 모두 절편 제외 |
| Early stopping = val 최저점 | "LOOCV 안 오르면 form 동결" |
| Bagging(병렬·random sampling) | bootstrap PI band B=500 |
| Common pattern: train 랜덤성 / test 평균화 | bootstrap resample(train) → PI(test 평균) |
| Occam's razor | "info-theoretic ceiling, DO NOT add terms" |

---

## 6. 아직 안 쓴 강의 (향후 레버)

- **L11–13 (MLP/backprop/training), L15–17 (CNN)**: Phase 4 의 "예측 numbers → 2D microstructure 이미지"
  단계에서 생성모델(CNN/U-Net류)로 microstructure를 그릴 때 사용 예정
  (`scripts/extract_2d_microstructure.py synthesize_microstructure`의 ML 버전).
- **L16 BatchNorm / L14 Dropout**: 그 생성망 학습 시 정규화로 직접 사용.
- **L4 logistic / L8 softmax**: "percolate 여부 / dead-AM 여부" 같은 **이진·다중 분류** 타깃에 적용 가능
  (현재는 회귀만; 향후 grade rubric 분류에 후보).

→ 결론: 지금까지의 Phase 1 σ work는 **L2·L3·L4·L9·L14의 직접 응용**으로 이미 완결.
딥러닝 강의(L11–17)는 Phase 4(이미지 생성)에서 비로소 본격 투입된다.

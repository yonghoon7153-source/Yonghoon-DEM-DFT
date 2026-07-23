# #33 v3 ML: Duquesnoy 설계 폐루프 (`scripts/ml_design_loop.py`)

litdb 적용표 **B-1위 (최고 레버리지)**: Duquesnoy 2023(ARTISTIC)의 Sobol DOE → SISSO 형식발견 →
Bayesian 다목적 역설계 = **우리 5-phase 비전의 출판 원형**.  `predictor_engine.py`(GPR+RF, Phase 1-2)를
설계→최적화→합성 폐루프(Phase 3-5)로 확장.  corpus(88-132) 준비됨·frame-neutral(설계층).

## 3 조각 + 스칼라화

| 조각 | 역할 | 의존성 | 상태 |
|---|---|---|---|
| **sobol_doe** | Sobol 저불일치 공간충전 DOE (explore) | scipy.stats.qmc | ✅ **클라우드 검증** |
| **scalarize** | 앱-가중 다목적 → 스칼라 | 순수 numpy | ✅ 검증 |
| **sisso_discover** | SISSO 기호회귀 자동 형식발견 | pysisso | 🔶 WSL (import-guard) |
| **bayes_minimize** | GP+gp_hedge 다목적 역설계 | scikit-optimize | 🔶 WSL (import-guard) |

⚠ pysisso/skopt = 클라우드 부재 → import-guard 로 graceful 안내 dict(크래시 금지; predictor_engine 규약 동일).
Sobol·scalarize 는 여기서 완전 검증.

## 각 조각

### 1. Sobol DOE explore (검증됨)
`sobol_doe(bounds, n)` → Sobol 저불일치 수열로 설계공간 균일충전.  `active_learning_suggest`의
exploit-corner를 보완하는 **EXPLORE 모드** — σ_ionic close-out의 구조 gap(CN≥7, mid-thickness) 균일 샘플.
검증: 16pt L2-star discrepancy **0.025 < 랜덤 0.103** (4× 균일).

### 2. scalarize — 앱-가중 다목적 (검증됨)
`scalarize(metrics, app)` — 정규화 metric → 스칼라.  앱 프리셋:
- `fast_charge`: min τ · max σ_e · min current_focus
- `high_energy`: max density · min porosity · max σ_ionic
- `long_life`: max dip_margin · min current_focus · max coverage
- `balanced`: σ_ionic·σ_e·density·τ 균등
검증: fast_charge 방향(저-τ 선호) 정확.

### 3. SISSO 형식발견 (WSL)
`sisso_discover(X, y, feature_names)` → σ-폼 자동발견, hand-폼과 CV-R² 병기.
- √φ_eff·CN²·√cov 재발견 시 = **frame[4] 독립확인**.
- σ_thermal은 SISSO **실패 예측**(다경로 = 단일 backbone 불가) → "Ridge irreducible" 논거 강화.

### 4. Bayesian 다목적 역설계 (WSL)
`bayes_minimize(objective_fn, bounds, app)` → GP+gp_hedge(LCB+EI+PI)로 설계 역탐색.
objective_fn(design) → predictor_engine 예측 → scalarize → 최소화.  **Phase 3-5 폐루프**:
predict → synthesize(2D) → z-stack(layer).

## WSL 실행
```bash
pip install pysisso scikit-optimize SALib      # 클라우드 부재, WSL 전용
python scripts/ml_design_loop.py               # selftest (Sobol·scalarize 검증)
# 실제 루프: predictor_engine corpus 로드 → sisso_discover / bayes_minimize
```

## frame[5] 위치
ML 루프는 DEM/MPM **위** 설계층(frame-neutral).  우리 structure→σ 기전이 그들이 없는 "why"를 제공 —
ML은 탐색·최적화, 물리는 해석.  selftest 6/6 PASS(Sobol 균일·scalarize 방향·guard·엣지).

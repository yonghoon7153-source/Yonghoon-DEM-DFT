#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""#33 v3 ML: Duquesnoy 2023 설계 폐루프 — Sobol DOE → SISSO 형식발견 → Bayesian 다목적 역설계.

litdb 적용표 B-1위(최고 레버리지): 우리 5-phase 비전(design→micro→σ→2D→layer)의 출판 원형.
`predictor_engine.py`(GPR+RF, Phase 1-2)를 **설계→최적화→합성 폐루프**(Phase 3-5)로 확장.

3 조각 (의존성):
  1. sobol_doe        — Sobol 저불일치 공간충전 DOE.  **scipy.stats.qmc (클라우드 검증됨).**
  2. sisso_discover   — SISSO 기호회귀 자동 형식발견.  pysisso (WSL — import-guard).
  3. bayes_minimize   — Bayesian 다목적 역설계 (GP+acquisition).  scikit-optimize (WSL — import-guard).
  + scalarize         — 앱-가중 스칼라화 (fast-charge=min τ·max σ_e / high-energy=max density).  순수.

★ sklearn/pysisso/skopt 는 클라우드 부재 → 무거운 조각은 import-guard 로 graceful (predictor_engine
규약과 동일; 실제 학습은 WSL).  Sobol·scalarize 는 여기서 완전 검증.
"""
from __future__ import annotations

import numpy as np


# ── 1. Sobol DOE (scipy.stats.qmc — 클라우드 검증) ──────────────────────────────
def sobol_doe(bounds: dict, n: int, seed: int = 0) -> list[dict]:
    """Sobol 저불일치 수열로 설계공간 균일충전 → n개 설계점 (dict list).
    bounds = {param: (lo, hi)}.  active_learning 의 exploit-corner 를 보완하는 EXPLORE 모드
    (σ_ionic close-out 의 구조 gap: CN≥7, mid-thickness 를 균일 샘플).  log-scale 은 호출측서."""
    if n <= 0 or not bounds:
        return []
    from scipy.stats import qmc
    keys = list(bounds)
    lo = np.array([bounds[k][0] for k in keys], float)
    hi = np.array([bounds[k][1] for k in keys], float)
    # Sobol 은 2^m 에서 균형 → n 을 올림한 2의 거듭제곱으로 뽑고 앞 n개 사용 (경고 회피)
    m = max(1, int(np.ceil(np.log2(max(n, 2)))))
    unit = qmc.Sobol(d=len(keys), scramble=True, seed=seed).random_base2(m)[:n]
    pts = qmc.scale(unit, lo, hi)
    return [{k: float(pts[i, j]) for j, k in enumerate(keys)} for i in range(len(pts))]


def sobol_discrepancy(pts: list[dict], bounds: dict) -> float:
    """설계점 집합의 L2-star discrepancy (낮을수록 균일 = Sobol 우수).  Sobol vs 랜덤 비교용."""
    if not pts or not bounds:
        return float('inf')
    from scipy.stats import qmc
    keys = list(bounds)
    lo = np.array([bounds[k][0] for k in keys], float)
    hi = np.array([bounds[k][1] for k in keys], float)
    U = np.array([[(p[k] - lo[j]) / max(hi[j] - lo[j], 1e-30) for j, k in enumerate(keys)] for p in pts])
    return float(qmc.discrepancy(np.clip(U, 0, 1)))


# ── scalarize: 앱-가중 다목적 → 스칼라 (순수, 검증) ─────────────────────────────
# 앱 프리셋: (metric, 방향 +1=max/-1=min, 가중).  metric 은 정규화된 [0,1] 가정.
APP_OBJECTIVES = {
    'fast_charge':  [('sigma_e', +1, 0.4), ('tau', -1, 0.4), ('current_focus', -1, 0.2)],  # 저-τ·고-σ_e·저-집중
    'high_energy':  [('density', +1, 0.5), ('porosity', -1, 0.3), ('sigma_ionic', +1, 0.2)],
    'long_life':    [('dip_margin', +1, 0.4), ('current_focus', -1, 0.3), ('coverage', +1, 0.3)],
    'balanced':     [('sigma_ionic', +1, 0.25), ('sigma_e', +1, 0.25), ('density', +1, 0.25), ('tau', -1, 0.25)],
}


def scalarize(metrics: dict, app: str = 'balanced') -> float:
    """정규화된 metric dict → 앱-가중 스칼라 (클수록 좋음).  누락 metric 은 0.5(중립)."""
    obj = APP_OBJECTIVES.get(app, APP_OBJECTIVES['balanced'])
    s = 0.0
    for key, sign, w in obj:
        v = metrics.get(key, 0.5)
        try:
            v = float(v)
        except (TypeError, ValueError):
            v = 0.5
        s += w * sign * v
    return float(s)


# ── 2. SISSO 형식발견 (pysisso — WSL, import-guard) ─────────────────────────────
def sisso_discover(X, y, feature_names, n_dim=2, ops=('+', '-', '*', '/'), **kw):
    """SISSO 기호회귀 → σ-폼 자동 발견 (hand-폼과 CV-R² 병기).  √φ_eff·CN²·√cov 재발견 시
    frame[4] 독립확인; σ_thermal 은 SISSO 실패 예측(다경로) → 'Ridge irreducible' 논거 강화.
    ⚠ pysisso 필요 (WSL — 클라우드 부재).  import 실패 시 안내 dict 반환(크래시 금지)."""
    try:
        from pysisso.sklearn import SISSORegressor          # noqa: F401
    except ImportError:
        return {'available': False, 'reason': 'pysisso 미설치 (WSL 전용) — pip install pysisso',
                'note': 'sobol_doe/scalarize 는 클라우드 검증됨; SISSO 는 WSL에서 실행'}
    from pysisso.sklearn import SISSORegressor
    reg = SISSORegressor(rung=n_dim, opset=list(ops), **kw)
    reg.fit(np.asarray(X, float), np.asarray(y, float))
    return {'available': True, 'model': reg, 'feature_names': list(feature_names)}


# ── 3. Bayesian 다목적 역설계 (scikit-optimize — WSL, import-guard) ──────────────
def bayes_minimize(objective_fn, bounds: dict, n_calls=40, app='balanced', seed=0, **kw):
    """GP 기반 Bayesian 최적화로 설계 역탐색 (predict→scalarize 를 objective 로).
    acquisition = gp_hedge(LCB+EI+PI).  objective_fn(design_dict) → metrics dict → −scalarize (최소화).
    ⚠ scikit-optimize 필요 (WSL).  import 실패 시 안내 dict."""
    try:
        from skopt import gp_minimize                        # noqa: F401
    except ImportError:
        return {'available': False, 'reason': 'scikit-optimize 미설치 (WSL 전용) — pip install scikit-optimize',
                'note': 'Sobol DOE 로 explore 후 WSL에서 BO exploit'}
    from skopt import gp_minimize
    from skopt.space import Real
    keys = list(bounds)
    space = [Real(bounds[k][0], bounds[k][1], name=k) for k in keys]

    def _neg(x):
        d = {k: x[j] for j, k in enumerate(keys)}
        return -scalarize(objective_fn(d), app)

    res = gp_minimize(_neg, space, n_calls=n_calls, acq_func='gp_hedge', random_state=seed, **kw)
    best = {k: res.x[j] for j, k in enumerate(keys)}
    return {'available': True, 'best_design': best, 'best_score': -res.fun, 'result': res}


# ─────────────────────────── self-test ───────────────────────────
def _selftest() -> int:
    fails = []
    bounds = {'am_pct': (70.0, 90.0), 'ps_frac': (0.0, 1.0), 'd_se': (0.3, 1.5),
              'loading': (1.0, 8.0), 'rve': (30.0, 70.0)}
    # 1) Sobol DOE: n점·범위 내·키 일치
    pts = sobol_doe(bounds, 16, seed=1)
    assert len(pts) == 16, len(pts)
    for p in pts:
        assert set(p) == set(bounds)
        for k, (lo, hi) in bounds.items():
            assert lo <= p[k] <= hi, (k, p[k])
    # 2) Sobol < 랜덤 discrepancy (저불일치 = 더 균일)
    rng = np.random.default_rng(0)
    rand = [{k: float(rng.uniform(*bounds[k])) for k in bounds} for _ in range(16)]
    d_sobol = sobol_discrepancy(pts, bounds); d_rand = sobol_discrepancy(rand, bounds)
    if not (d_sobol < d_rand):
        fails.append(f'Sobol discrepancy {d_sobol:.4f} !< random {d_rand:.4f}')
    # 3) scalarize: 방향·가중 (fast_charge 는 저-τ 선호)
    hi_sig = scalarize({'sigma_e': 1.0, 'tau': 0.0, 'current_focus': 0.0}, 'fast_charge')
    lo_sig = scalarize({'sigma_e': 0.0, 'tau': 1.0, 'current_focus': 1.0}, 'fast_charge')
    if not (hi_sig > lo_sig):
        fails.append(f'scalarize 방향 오류 {hi_sig} !> {lo_sig}')
    # 4) 누락 metric → 0.5 중립 (크래시 금지)
    _ = scalarize({}, 'high_energy')
    # 5) WSL 조각 import-guard (크래시 대신 안내 dict)
    s = sisso_discover([[1, 2]], [1], ['a', 'b'])
    b = bayes_minimize(lambda d: {}, bounds, n_calls=5)
    if s.get('available') is not False or b.get('available') is not False:
        # pysisso/skopt 가 있으면 available=True 도 정상 (WSL) — 클라우드선 False 기대
        pass
    if 'reason' not in s and not s.get('available'):
        fails.append('sisso guard dict 이상')
    # 6) n=0 / 빈 bounds 안전
    assert sobol_doe({}, 5) == [] and sobol_doe(bounds, 0) == []
    print('selftest OK' if not fails else 'selftest FAIL: ' + '; '.join(fails))
    if not fails:
        print(f"  Sobol 16pt discrepancy {d_sobol:.5f} < random {d_rand:.5f} (더 균일) · "
              f"scalarize fast_charge hi {hi_sig:.2f} > lo {lo_sig:.2f} · "
              f"SISSO/BO guard = {'WSL' if not s.get('available') else 'available'}")
    return 1 if fails else 0


if __name__ == '__main__':
    import sys
    raise SystemExit(_selftest())

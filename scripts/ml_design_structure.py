#!/usr/bin/env python3
"""ml_design_structure — 설계 → **구조** 예측기.  σ 는 배우지 않는다.

왜 σ 를 배우지 않나
────────────────────
리포의 σ 스케일링법칙은 이미 LOOCV **σ_ion 0.975 · σ_e 0.953 · σ_th 0.90** 이다 (CLAUDE.md
Phase 1 완료).  물리형이고 항마다 의미가 있고 문헌에 앵커돼 있다.  일반 회귀가 그걸 이길
이유가 없고, 이기더라도 해석을 잃는다.  ⇒ **ML 은 그 법칙의 입력을 예측한다:**

    설계 ──[이 모듈]──▶ 구조 (φ_SE·φ_AM·CN·coverage·τ·porosity·f_perc·MPM 소성)
                          ├─[σ 스케일링법칙, LOOCV .975]──▶ σ 삼중항
                          └─[perf_reduced_order, 적합 0]──▶ η 분해·율특성

★ 이 모듈이 쓰는 방법론 = **리포가 σ 삼중항에 이미 쓴 것과 동일**
   (새 기법을 들여온 게 아니라, 검증된 자체 방법론을 구조 타깃에 적용한다)

   1. **해석적 LOOCV** (hat 행렬 e_i = r_i/(1−h_i))          … nested_cv_sat.py
   2. **탐욕 전방선택 + 절제(ablation) + 다중비교 보정**        … σ_th Stage T1 / σ_e 22.5
      - σ_e 는 항을 **빼서** LOOCV 가 올랐다(WEAK BLOCK).  같은 규율을 여기에 강제한다:
        **n/k ≥ 15:1** (σ_ion 18:1, σ_e 9.5:1 이 "safe" 였다).  전(前) 판본은 특징 105 개를
        n=235 에 그냥 던져 2.2:1 이었다 — 리포 자체 기준으로 과적합.
      - 채택 문턱은 고정값이 아니라 **후보 개수·표본·현재 R² 의 함수** (`_gain_floor`).
        후보 m 개 중 최댓값을 고르면 전부 잡음이어도 하나는 우연히 오른다.
   3. **중첩 CV** (outer K-fold · inner 에서 항선택+λ 재선택)  … nested_cv_sat.py
      naive LOOCV 와의 차 = **선택 편향**.  둘 다 보고한다.  ★보고 기준값은 nested.
   4. **베이즈(Laplace) 사후 → 케이스별 PI + 경험적 커버리지** … bayesian_laplace.py
      ridge = 가우시안 사전의 MAP → 사후 N(β̂, s²A⁻¹) 가 닫힌형.  90% PI 의 실제 커버리지를
      LOO 잔차로 잰다(σ_ion 의 94.4% 와 같은 검사).
   5. **외삽 게이트** (leverage h*)                            … 배포 안전장치
      학습 볼록포 밖 질의는 조용히 그럴듯한 값을 내지 않고 EXTRAPOLATION 으로 표시.
   6. **능동학습** (PI 폭 × 신규성)                            … active_learning_suggest.py
      다음 DEM 을 어디서 돌릴지 — 계산 예산 대비 정보이득 최대점.
   7. **물리 감사** (단조성 부호 · 닫힘 φ_SE+φ_AM+ε)          … frame[4] 정신
      강제하지 않고 **보고**한다.  강제하면 모형 오차가 숨는다.

★ porosity 타깃은 **regime-gated `use_porosity_pct`**
raw DEM 도 raw MPM 도 아니다.  케이스마다 신뢰되는 모델의 값을 쓴다
(docs/mpm_scaffold_reliability_and_am_freeze.md — "clamp = 신뢰성 0, 정답은 regime-gate").

★ sklearn 없이 **돌아간다**.  배포 호스트에 sklearn 이 없어 예측기 페이지가 영구
"Not Trained" 이었다.  전부 numpy 이고 계수는 JSON 으로 떨어져 추론엔 numpy 만 있으면 된다.

Selftest:  python3 scripts/ml_design_structure.py --selftest
학습:      python3 scripts/ml_design_structure.py --csv docs/data/design_performance_corpus.csv \
               --out docs/data/structure_model.json
능동학습:  python3 scripts/ml_design_structure.py --csv ... --suggest 10
"""

import argparse
import csv as _csv
import json
import math
import os

import numpy as np

# ── 설계 노브 (predictor_engine.INPUT_FEATURES 규약 — 재구현 금지) ────────────────────
DESIGN_FEATURES = ['d_se', 'd_am', 'am_pct', 'ps_frac', 'rve', 'loading',
                   'd_ratio', 'am_loading', 'se_density_proxy', 'layer_count',
                   'size_ratio_inv', 'am_se_interaction', 'log_d_se']

# ML 이 맡는 **구조** 타깃.  σ 는 여기 없다 (스케일링법칙 소관).
STRUCTURE_TARGETS = [
    ('phi_se', 'lin'), ('phi_am', 'lin'), ('cn', 'lin'), ('am_cn', 'lin'),
    ('coverage', 'lin'), ('tau', 'log'), ('f_perc', 'lin'), ('thickness', 'log'),
    ('use_porosity_pct', 'lin'),            # ★regime-gated (raw DEM/MPM 아님)
    ('se_of_solid_pct', 'lin'),
    # MPM 고유 — 강체구 DEM 엔 존재하지 않는 양
    ('mpm_plastic_gain_AM_P_tabor_pp', 'lin'), ('mpm_dg_mean', 'lin'),
]

# ★ n/k 하한 — σ_e Stage 22.5 가 항을 **빼서** LOOCV 를 올린 그 규율.
#   σ_ion 18:1 / σ_e 9.5:1 이 "safe", 6.3:1 은 "over-fit" 판정이었다.  15 는 그 사이 보수값.
MIN_N_OVER_K = 15.0
MAX_TERMS = 12                 # 위 비율과 함께 걸리는 절대 상한
MIN_GAIN = 0.004               # 절대 바닥 (σ_ion LOOCV 잡음 SE ≈ 0.0045)
MC_K = 2.0                     # 다중비교 상수 — 아래 _gain_floor 설명
LAM_GRID = (1e-3, 1e-2, 1e-1, 1.0, 10.0, 100.0)
LAM_SELECT = 1.0               # 항 고를 때 쓰는 고정 λ (λ 는 항 확정 후 한 번만 튜닝)
MIN_N_TARGET = 20              # 이보다 표본 적으면 아예 적합하지 않는다
Z90 = 1.6448536269514722       # 정규 90% 양측

# 물리적으로 **정의상** 정해진 부호 — 위반하면 적합이 비물리 (강제 안 함, 보고만)
MONOTONE_PRIORS = [
    ('am_pct', 'phi_am', +1, 'AM 비율↑ → AM 부피분율↑ (정의상)'),
    ('am_pct', 'phi_se', -1, 'AM 비율↑ → SE 부피분율↓ (고정 부피 배분)'),
    ('am_pct', 'se_of_solid_pct', -1, 'AM 비율↑ → 고체 중 SE 몫↓ (정의상)'),
    ('loading', 'thickness', +1, '로딩↑ → 전극 두께↑ (물질량 보존)'),
]


# ══════════════════════════════════════════════════════════════════════════════
#  기저 · 적합 · 해석적 LOOCV
# ══════════════════════════════════════════════════════════════════════════════
def candidate_terms(d):
    """항 후보: 절편 [] · 1차 [i] · 2차 [i,i] · 교호작용 [i,j].  JSON 직렬화 가능한 표현."""
    terms = [[]] + [[i] for i in range(d)] + [[i, i] for i in range(d)]
    terms += [[i, j] for i in range(d) for j in range(i + 1, d)]
    return terms


def build(X, terms):
    """[n,d] 표준화 설계 + 항목록 → [n,k] 설계행렬."""
    n = X.shape[0]
    cols = []
    for t in terms:
        c = np.ones(n)
        for i in t:
            c = c * X[:, i]
        cols.append(c)
    return np.column_stack(cols) if cols else np.ones((n, 1))


def _ridge_A(Phi, lam, has_intercept):
    A = Phi.T @ Phi + lam * np.eye(Phi.shape[1])
    if has_intercept:
        A[0, 0] -= lam                                # 절편은 벌하지 않는다
    return A


def ridge(Phi, y, lam, has_intercept=True):
    return np.linalg.solve(_ridge_A(Phi, lam, has_intercept), Phi.T @ y)


def loocv(Phi, y, lam, has_intercept=True):
    """해석적 LOOCV — (R², LOO 잔차 e, leverage h).  n 번 재적합 불필요.

    ★ hat 행렬은 _ridge 와 **같은 A** 를 써야 한다 (절편 미벌점 보정 포함).  이 보정을
      빠뜨리면 해석식이 실제 leave-one-out 과 8.8e-2 어긋난다 (개발 중 실제로 밟음).
    """
    A = _ridge_A(Phi, lam, has_intercept)
    try:
        Ainv = np.linalg.inv(A)
    except np.linalg.LinAlgError:
        return -np.inf, None, None
    h = np.clip(np.einsum('ij,jk,ik->i', Phi, Ainv, Phi), 0.0, 1.0 - 1e-9)
    r = y - Phi @ np.linalg.solve(A, Phi.T @ y)
    e = r / (1.0 - h)
    ss = float(((y - y.mean()) ** 2).sum())
    r2 = 1.0 - float((e ** 2).sum()) / ss if ss > 0 else float('nan')
    return r2, e, h


def _gain_floor(n, m, r2_cur):
    """항 하나를 채택하려면 넘어야 할 LOOCV 이득 — **다중비교 보정**.

    고정 문턱(0.004)은 틀렸다.  탐욕선택은 후보 m(≈105)개 중 **최댓값**을 고르므로, 전부
    무의미한 항이어도 최선 하나는 우연히 꽤 오른다.  귀무가정에서 항 하나가 줄이는 RSS 는
    σ²·χ²(1) 이고, R² 로 환산하면 χ²(1)·(1−R²_cur)/n.  m 개 중 최댓값이면
    E[max χ²] ≈ 2·ln m ⇒

        floor ≈ MC_K · ln(m) · (1 − R²_cur) / n

    성질이 옳다: 표본이 커지면(n↑) 문턱이 내려가 항을 더 허용하고, 후보를 늘리면(m↑)
    올라가 우연을 막고, 이미 잘 맞을수록(R²↑) 남은 분산이 적어 문턱이 낮아진다.
    (고정 0.004 은 n=240·m=105 잡음에서 항 7 개를 통과시켰다 — 실제로 밟은 실패.)
    """
    return max(MIN_GAIN, MC_K * math.log(max(m, 2)) * max(1.0 - r2_cur, 0.02) / max(n, 1))


def select_terms(X, y, max_terms=MAX_TERMS, lam=LAM_SELECT):
    """탐욕 전방선택 — 항을 하나씩 넣고 다중비교-보정 문턱을 넘을 때만 채택.

    σ_th Stage T1 의 16-특징 그리디 · σ_e 22.5 의 절제 스크린과 같은 절차.  **n/k ≥
    MIN_N_OVER_K** 를 동시에 강제해 표본 대비 항 수가 넘지 않게 한다.
    """
    n, d = X.shape
    cand = candidate_terms(d)
    k_cap = int(min(max_terms, max(2, math.floor(n / MIN_N_OVER_K))))
    chosen, trace = [[]], []                          # 절편은 항상
    cur, _, _ = loocv(build(X, chosen), y, lam)
    trace.append(('intercept', cur))
    pool = [t for t in cand if t]
    while len(chosen) < k_cap:
        best, best_t = cur, None
        for t in pool:
            r2, _, _ = loocv(build(X, chosen + [t]), y, lam)
            if r2 > best:
                best, best_t = r2, t
        if best_t is None or (best - cur) < _gain_floor(n, len(pool), cur):
            break
        chosen.append(best_t)
        pool.remove(best_t)
        cur = best
        trace.append(('*'.join(DESIGN_FEATURES[i] for i in best_t), cur))
    return chosen, trace, k_cap


def fit_target(X, y, kind='lin', max_terms=MAX_TERMS):
    """한 타깃 적합 — 항선택 → λ 튜닝 → Laplace 사후.  반환 model dict (JSON 직렬화 가능)."""
    ylog = kind == 'log'
    yy = np.log(np.clip(y, 1e-12, None)) if ylog else np.asarray(y, float)
    mu, sd = X.mean(0), X.std(0)
    sd = np.where(sd == 0, 1.0, sd)
    Xs = (X - mu) / sd
    terms, trace, k_cap = select_terms(Xs, yy, max_terms=max_terms)
    Phi = build(Xs, terms)
    r2, lam = max(((loocv(Phi, yy, l)[0], l) for l in LAM_GRID), key=lambda t: t[0])
    _, e, h = loocv(Phi, yy, lam)
    beta = ridge(Phi, yy, lam)
    # ── Laplace 사후 (ridge = 가우시안 사전의 MAP) : β|y ~ N(β̂, s²A⁻¹) ──────────────
    A = _ridge_A(Phi, lam, True)
    Ainv = np.linalg.inv(A)
    dof_eff = float(np.sum(h))                        # trace(H) = 유효 자유도
    resid = yy - Phi @ beta
    s2 = float((resid ** 2).sum()) / max(len(yy) - dof_eff, 1.0)
    # 경험적 커버리지 — 명목 90% PI 가 실제 LOO 오차를 얼마나 덮나 (σ_ion 94.4% 와 같은 검사)
    pi_half = Z90 * math.sqrt(s2) * np.sqrt(1.0 + h)
    cover = float(np.mean(np.abs(e) <= pi_half))
    return {'target': None, 'terms': terms, 'coef': beta.tolist(),
            'loocv_r2_naive': r2, 'lam': lam, 'mu': mu.tolist(), 'sd': sd.tolist(),
            'log_target': ylog, 'n': int(len(yy)), 'k': len(terms),
            'n_over_k': round(len(yy) / len(terms), 2), 'k_cap': k_cap,
            's2': s2, 'Ainv': Ainv.tolist(), 'h_max_train': float(h.max()),
            'pi90_coverage': cover, 'select_trace': [(a, round(b, 4)) for a, b in trace]}


def nested_cv(X, y, kind='lin', folds=10, seed=0, max_terms=MAX_TERMS):
    """중첩 CV — outer K-fold, inner 에서 **항선택과 λ 를 다시** 고른다.

    naive LOOCV 는 전체 데이터로 항을 고른 뒤 같은 데이터로 채점하므로 낙관 편향이 있다.
    보류된 폴드는 하이퍼선택에 일절 관여하지 않는다 ⇒ 편향 없는 일반화 추정.
    """
    ylog = kind == 'log'
    yy = np.log(np.clip(y, 1e-12, None)) if ylog else np.asarray(y, float)
    n = len(yy)
    if n < 3 * folds:
        folds = max(3, n // 8)
    rs = np.random.default_rng(seed)
    order = rs.permutation(n)
    pred = np.empty(n)
    for f in range(folds):
        te = order[f::folds]
        tr = np.setdiff1d(order, te)
        mu, sd = X[tr].mean(0), X[tr].std(0)
        sd = np.where(sd == 0, 1.0, sd)
        Xtr, Xte = (X[tr] - mu) / sd, (X[te] - mu) / sd
        terms, _, _ = select_terms(Xtr, yy[tr], max_terms=max_terms)
        Ptr = build(Xtr, terms)
        _, lam = max(((loocv(Ptr, yy[tr], l)[0], l) for l in LAM_GRID), key=lambda t: t[0])
        pred[te] = build(Xte, terms) @ ridge(Ptr, yy[tr], lam)
    ss = float(((yy - yy.mean()) ** 2).sum())
    return 1.0 - float(((yy - pred) ** 2).sum()) / ss if ss > 0 else float('nan')


# ══════════════════════════════════════════════════════════════════════════════
#  추론 — PI + 외삽 게이트 (배포 경로, numpy 만 필요)
# ══════════════════════════════════════════════════════════════════════════════
def predict(model, x_row, z=Z90):
    """설계 1행 → {value, lo, hi, sd, leverage, extrapolation}.

    ★ 외삽 게이트: leverage h* 가 학습셋 최대치를 넘으면 학습 볼록포 밖 → 값은 주되
      `extrapolation=True` 로 표시한다.  조용히 그럴듯한 숫자를 내놓지 않기 위한 것.
    """
    x = (np.asarray(x_row, float) - np.asarray(model['mu'])) / np.asarray(model['sd'])
    phi = build(x.reshape(1, -1), model['terms'])[0]
    v = float(phi @ np.asarray(model['coef']))
    Ainv = np.asarray(model['Ainv'])
    hstar = float(phi @ Ainv @ phi)
    sd = math.sqrt(max(model['s2'], 0.0) * (1.0 + max(hstar, 0.0)))
    lo, hi = v - z * sd, v + z * sd
    if model.get('log_target'):
        v, lo, hi = math.exp(v), math.exp(lo), math.exp(hi)
    return {'value': v, 'lo': lo, 'hi': hi, 'sd': sd, 'leverage': hstar,
            'extrapolation': hstar > model.get('h_max_train', np.inf)}


def predict_target(model, x_row):
    """점추정만 (구판 호환)."""
    return predict(model, x_row)['value']


# ══════════════════════════════════════════════════════════════════════════════
#  물리 감사 — 강제하지 않고 보고 (frame[4] 정신)
# ══════════════════════════════════════════════════════════════════════════════
def physics_audit(bundle, X):
    """단조성 부호 + 닫힘(φ_SE+φ_AM+ε).  ML 이 조용히 비물리를 학습했는지 잡는 렌즈."""
    out = {'monotone': [], 'closure': None}
    med = np.median(X, 0)
    for feat, tgt, sign, why in MONOTONE_PRIORS:
        m = bundle['models'].get(tgt)
        if m is None or feat not in DESIGN_FEATURES:
            continue
        j = DESIGN_FEATURES.index(feat)
        lo_x, hi_x = med.copy(), med.copy()
        lo_x[j], hi_x[j] = np.percentile(X[:, j], 10), np.percentile(X[:, j], 90)
        d = predict(m, hi_x)['value'] - predict(m, lo_x)['value']
        okk = (d > 0) if sign > 0 else (d < 0)
        out['monotone'].append({'feature': feat, 'target': tgt, 'expect': sign,
                                'delta_p10_p90': round(float(d), 4), 'ok': bool(okk),
                                'why': why})
    ms = bundle['models']
    if all(t in ms for t in ('phi_se', 'phi_am', 'use_porosity_pct')):
        # ★ 절대 1.0 을 요구하지 않는다 — 코퍼스 자체의 닫힘 잔차가 기준선이다.
        #   모형이 그 기준선보다 **더** 벌어지면 그건 모형이 만든 오차.
        pv = [predict(ms[t], r)['value'] for t in ('phi_se', 'phi_am', 'use_porosity_pct')
              for r in [med]]
        out['closure'] = {'pred_sum': round(pv[0] + pv[1] + pv[2] / 100.0, 4),
                          'note': '중앙설계에서 φ_SE+φ_AM+ε.  코퍼스 기준선과 대조할 값 (강제 아님)'}
    return out


# ══════════════════════════════════════════════════════════════════════════════
#  능동학습 — 다음 DEM 을 어디서 돌릴까
# ══════════════════════════════════════════════════════════════════════════════
def derive_features(d_se, d_am, am_pct, ps_frac, rve, loading):
    """설계 13-특징을 **자유노브 6개**에서 유도 — predictor_engine 과 같은 정의.

    ★ 13 특징 중 7 개(d_ratio·am_loading·se_density_proxy·layer_count·size_ratio_inv·
      am_se_interaction·log_d_se)는 나머지 6 개의 **결정론적 함수**다.  그래서 13 차원을
      독립으로 뽑으면 자기모순 설계가 나온다 (실제로 첫 실런에서 d_se=2.92 인데
      log_d_se=0.85, d_ratio=0.215 인데 d_se/d_am=6.23 인 후보를 뱉었다 — 시뮬에 못 넣는 값).
      가능하면 predictor_engine 을 그대로 재사용하고, 못 불러오면 아래 사본을 쓴다
      (사본이 원본과 같은지는 selftest 가 대조한다).
    """
    try:                                              # 원본 재사용 (재구현 금지)
        import sys as _sys
        _wa = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'webapp')
        if _wa not in _sys.path:
            _sys.path.insert(0, _wa)
        from predictor_engine import derive_features as _df
        return _df(d_se, d_am, am_pct, ps_frac, rve, loading)
    except Exception:                                 # noqa: BLE001 — 오프라인 사본
        return {'d_se': d_se, 'd_am': d_am, 'am_pct': am_pct, 'ps_frac': ps_frac,
                'rve': rve, 'loading': loading,
                'd_ratio': d_se / d_am if d_am > 0 else 0.1,
                'am_loading': am_pct * loading / 100,
                'se_density_proxy': (100 - am_pct) / max(d_se, 0.1),
                'layer_count': loading * 30 / max(d_se, 0.1),
                'size_ratio_inv': d_am / d_se if d_se > 0 else 10,
                'am_se_interaction': am_pct * (1 - ps_frac) / 100,
                'log_d_se': math.log(max(d_se, 0.1))}


FREE_KNOBS = ['d_se', 'd_am', 'am_pct', 'ps_frac', 'rve', 'loading']


def suggest(bundle, X, target, n_out=10, n_cand=2000, seed=0, allow_weak=False):
    """후보에서 (PI 폭 × 신규성) 상위 n_out.  active_learning_suggest.py 와 같은 논리.

    ★ 후보는 **자유노브 6 개만 뽑고 나머지 7 개는 유도**한다 — 그래야 나온 설계를
      그대로 DEM 에 넣을 수 있다 (13 차원 독립 샘플링은 자기모순 설계를 만든다).
    ★ 판정이 REJECT 인 타깃에는 제안하지 않는다.  못 맞히는 모형의 불확실성 순위는
      "어디가 정보가 많은가" 가 아니라 그냥 잡음이다.

    CAVEAT: 휴리스틱 플래너다.  진짜 정보이득은 그 점을 실제로 돌려봐야 안다.
    """
    m = bundle['models'].get(target)
    if m is None:
        return {'error': f'타깃 없음: {target}', 'rows': []}
    vd = m.get('verdict', 'WEAK')
    if vd == 'REJECT' or (vd == 'WEAK' and not allow_weak):
        return {'error': (f'{target} 판정 = {vd} (nested R²={m.get("nested_cv_r2", float("nan")):+.3f}). '
                          '못 맞히는 모형의 불확실성 순위는 정보이득이 아니라 잡음이다 — '
                          'USABLE 타깃으로 제안하거나 --allow-weak 로 강행.'), 'rows': []}
    rs = np.random.default_rng(seed)
    ji = [DESIGN_FEATURES.index(k) for k in FREE_KNOBS]
    lo, hi = np.percentile(X[:, ji], 2, axis=0), np.percentile(X[:, ji], 98, axis=0)
    mu, sd = np.asarray(m['mu']), np.asarray(m['sd'])
    Xs = (X - mu) / sd
    rows = []
    for knob in rs.uniform(lo, hi, size=(int(n_cand), len(FREE_KNOBS))):
        d = derive_features(*knob)
        c = np.array([float(d[f]) for f in DESIGN_FEATURES])
        p = predict(m, c)
        nov = float(np.min(np.linalg.norm(Xs - (c - mu) / sd, axis=1)))
        rows.append((p['sd'] * nov, p, nov, knob))
    rows.sort(key=lambda t: -t[0])
    return {'error': None, 'target': target, 'verdict': vd,
            'rows': [{'score': round(s, 4), 'pred': round(p['value'], 4),
                      'pi90': [round(p['lo'], 4), round(p['hi'], 4)],
                      'novelty': round(nov, 3), 'extrapolation': p['extrapolation'],
                      'design': {f: round(float(v), 4) for f, v in zip(FREE_KNOBS, k)}}
                     for s, p, nov, k in rows[:n_out]]}


# ══════════════════════════════════════════════════════════════════════════════
#  데이터층 → 학습
# ══════════════════════════════════════════════════════════════════════════════
def _column(rows, name):
    """행 목록에서 한 수치열 → (idx, y).  파싱 안 되는 칸은 그 열에서만 뺀다."""
    idx, val = [], []
    for i, r in enumerate(rows):
        v = r.get(name, '')
        if v in ('', None):
            continue
        try:
            val.append(float(v))
            idx.append(i)
        except (ValueError, TypeError):
            pass
    return np.asarray(idx, int), np.asarray(val, float)


def load_corpus(csv_path):
    """데이터층 CSV → (X, {target: (idx, y)}, names, rows).  결측은 그 타깃에서만 제외."""
    raw = list(_csv.DictReader(open(csv_path)))
    keep, names = [], []
    for r in raw:
        try:
            keep.append(([float(r[f]) for f in DESIGN_FEATURES], r))
            names.append(r.get('name', ''))
        except (KeyError, ValueError, TypeError):
            continue
    X = np.asarray([k[0] for k in keep], float)
    kept_rows = [k[1] for k in keep]
    ys = {}
    for t, _k in STRUCTURE_TARGETS:
        idx, val = _column(kept_rows, t)
        if len(val) >= MIN_N_TARGET:
            ys[t] = (idx, val)
    return X, ys, names, kept_rows


def diagnose(csv_path, target, split_by='use_source', vs=None, folds=10):
    """REJECT/WEAK 타깃 부검 — **혼합 자체가 문제인가**를 가른다.

    `use_porosity_pct` 는 regime-gate 가 케이스마다 DEM 값이나 MPM 값을 고른 **스위치된**
    양이다.  설계공간의 매끄러운 다항식은 "어느 모델이 무너졌나" 에 달린 불연속을 표현할
    수 없다.  가설이 맞다면:

      · 부분집합(DEM-출처만 / MPM-출처만)의 nested R² 가 혼합보다 뚜렷이 높다
      · 단일-출처 원열(raw DEM porosity)이 게이트된 열보다 잘 배워진다

    둘 다 아니면 게이트 탓이 아니라 porosity 가 이 설계해상도에서 **본래 확률적**이라는
    뜻이다 (씨앗별 패킹).  둘은 처방이 다르다 — 전자는 게이트를 따로 배우면 되고,
    후자는 더 배워도 소용없으니 ±밴드로 보고해야 한다.
    """
    X, _ys, _names, rows = load_corpus(csv_path)
    kind = dict(STRUCTURE_TARGETS).get(target, 'lin')
    idx, y = _column(rows, target)
    out = {'target': target, 'kind': kind,
           'mixture': {'n': int(len(y)),
                       'nested': nested_cv(X[idx], y, kind, folds=folds) if len(y) >= MIN_N_TARGET else None},
           'split_by': split_by, 'groups': {}, 'vs': None}
    groups = {}
    for i in idx:
        groups.setdefault(str(rows[i].get(split_by, '') or '?'), []).append(i)
    for g, ii in sorted(groups.items()):
        ii = np.asarray(ii, int)
        yy = np.asarray([float(rows[i][target]) for i in ii], float)
        out['groups'][g] = {
            'n': int(len(ii)),
            'nested': (nested_cv(X[ii], yy, kind, folds=min(folds, max(3, len(ii) // 8)))
                       if len(ii) >= MIN_N_TARGET else None)}
    if vs:
        i2, y2 = _column(rows, vs)
        out['vs'] = {'column': vs, 'n': int(len(y2)),
                     'nested': (nested_cv(X[i2], y2, kind, folds=folds)
                                if len(y2) >= MIN_N_TARGET else None)}
    # ── 판정 ───────────────────────────────────────────────────────────────────────
    mx = out['mixture']['nested']
    subs = [v['nested'] for v in out['groups'].values() if v['nested'] is not None]
    gain_split = (max(subs) - mx) if (subs and mx is not None) else None
    gain_vs = ((out['vs']['nested'] - mx)
               if (out['vs'] and out['vs']['nested'] is not None and mx is not None) else None)
    best = max([g for g in (gain_split, gain_vs) if g is not None], default=None)
    if best is None:
        out['verdict'] = 'INCONCLUSIVE — 부분집합 표본이 모자라 비교 불가'
    elif best > 0.15:
        out['verdict'] = ('SWITCHED — 단일-출처로 좁히면 뚜렷이 잘 배워진다.  게이트가 만든 '
                          '불연속이 원인 ⇒ 구성요소와 게이트를 따로 배우는 게 맞다.')
    elif best > 0.05:
        out['verdict'] = 'PARTIALLY SWITCHED — 게이트가 일부 기여하지만 그것만으론 설명 안 됨.'
    else:
        out['verdict'] = ('INTRINSIC — 좁혀도 안 좋아진다.  게이트 탓이 아니라 이 설계해상도에서 '
                          '본래 확률적(씨앗별 패킹) ⇒ 더 배우지 말고 ±PI 로 보고할 것.')
    return out


def verdict(nested_r2, cover):
    """배포 판정 — nested 기준.  naive 로 판정하면 선택 편향을 성능으로 착각한다."""
    if not np.isfinite(nested_r2):
        return 'REJECT'
    if nested_r2 >= 0.75 and 0.80 <= cover <= 0.99:
        return 'USABLE'
    if nested_r2 >= 0.40:
        return 'WEAK'          # ±PI 와 함께라면 쓸 수 있지만 점추정만 쓰면 안 됨
    return 'REJECT'


def train(csv_path, out_path=None, verbose=True, folds=10, do_nested=True):
    X, ys, names, _rows = load_corpus(csv_path)
    if verbose:
        print(f'  설계행렬 {X.shape[0]} × {X.shape[1]}  ·  타깃 {len(ys)}개  '
              f'(n/k ≥ {MIN_N_OVER_K:.0f}:1 강제, 항 상한 {MAX_TERMS})')
        print(f"  {'타깃':32s} {'n':>4s} {'k':>3s} {'n/k':>6s} "
              f"{'naive':>7s} {'nested':>7s} {'편향':>6s} {'PI90':>6s}  판정")
    models, skipped = {}, []
    for t, kind in STRUCTURE_TARGETS:
        if t not in ys:
            skipped.append(t)
            continue
        idx, y = ys[t]
        m = fit_target(X[idx], y, kind)
        m['target'] = t
        m['nested_cv_r2'] = (nested_cv(X[idx], y, kind, folds=folds)
                             if do_nested else float('nan'))
        m['selection_bias'] = (m['loocv_r2_naive'] - m['nested_cv_r2']
                               if np.isfinite(m['nested_cv_r2']) else float('nan'))
        m['verdict'] = verdict(m['nested_cv_r2'], m['pi90_coverage'])
        models[t] = m
        if verbose:
            print(f"  {t:32s} {m['n']:4d} {m['k']:3d} {m['n_over_k']:6.1f} "
                  f"{m['loocv_r2_naive']:+7.3f} {m['nested_cv_r2']:+7.3f} "
                  f"{m['selection_bias']:+6.3f} {m['pi90_coverage']*100:5.1f}%  {m['verdict']}"
                  + ('  (log)' if m['log_target'] else ''))
    if verbose:
        if skipped:
            print(f'  ⚠ 표본 {MIN_N_TARGET} 미만이라 미적합: {", ".join(skipped)}')
        print('  ★ σ 삼중항은 의도적으로 타깃이 아니다 — 스케일링법칙(.975/.953/.90) 소관')
        print('  ★ 판정은 **nested** 기준.  naive−nested = 선택 편향(그만큼 낙관적).')
    bundle = {'kind': 'design_to_structure', 'features': DESIGN_FEATURES,
              'models': models, 'skipped': skipped, 'n_cases': int(X.shape[0]),
              'method': {'loocv': 'analytic hat-matrix (intercept unpenalized)',
                         'selection': (f'greedy forward, n/k>={MIN_N_OVER_K}, gain floor = '
                                       f'max({MIN_GAIN}, {MC_K}*ln(m)*(1-R2)/n)  '
                                       '[multiple-comparison corrected]'),
                         'nested_cv': f'outer {folds}-fold, inner re-selects terms and lambda',
                         'posterior': 'Laplace (ridge MAP), N(beta_hat, s2*Ainv)',
                         'gate': 'leverage h* > train max -> extrapolation flag'},
              'note': ('ML 은 **구조**만 예측한다.  σ 는 리포의 스케일링법칙, 성능은 '
                       'perf_reduced_order(적합 0) 가 맡는다.  porosity 타깃은 regime-gated '
                       'use_porosity_pct (raw DEM/MPM 아님).'),
              'inference': 'predict() — numpy 만 있으면 된다 (sklearn 불요)'}
    bundle['physics_audit'] = physics_audit(bundle, X)
    if verbose:
        pa = bundle['physics_audit']['monotone']
        if pa:
            bad = [p for p in pa if not p['ok']]
            print(f"  물리 감사(단조성): {len(pa)-len(bad)}/{len(pa)} 통과"
                  + ('' if not bad else '  ⚠ 위반 ' + ', '.join(
                      f"{p['feature']}→{p['target']}" for p in bad)))
    if out_path:
        os.makedirs(os.path.dirname(os.path.abspath(out_path)) or '.', exist_ok=True)
        json.dump(bundle, open(out_path, 'w'), ensure_ascii=False, indent=1)
        if verbose:
            print(f'  → {out_path}')
    return bundle


# ══════════════════════════════════════════════════════════════════════════════
#  Selftest
# ══════════════════════════════════════════════════════════════════════════════
def _selftest():                                                   # noqa: C901
    ok = tot = 0

    def chk(name, cond, extra=''):
        nonlocal ok, tot
        tot += 1
        ok += 1 if cond else 0
        print(f"  {'✓' if cond else '✗ FAIL'} {name}" + (f' — {extra}' if extra else ''))

    rng = np.random.default_rng(7)
    n = 240
    X = np.column_stack([rng.uniform(lo, hi, n) for lo, hi in
                         ((0.3, 2.0), (2, 12), (50, 90), (0, 1), (30, 80), (1, 8),
                          (0.05, 0.5), (0.5, 7), (0.2, 2), (10, 90),
                          (2, 20), (0.1, 0.9), (-1.2, 0.7))])
    y_lin = 0.6 * X[:, 2] - 2.0 * X[:, 1] + 0.03 * X[:, 2] * X[:, 1] + rng.normal(0, 1.0, n)

    print(' [1] 기저·적합·해석적 LOOCV')
    m = fit_target(X, y_lin, 'lin')
    chk('알려진 교호작용 관계를 복원 (naive LOOCV R² > 0.9)',
        m['loocv_r2_naive'] > 0.9, f"R²={m['loocv_r2_naive']:.4f} λ={m['lam']:g} k={m['k']}")
    # 해석적 LOOCV = 실제 leave-one-out
    mu2, sd2 = X.mean(0), X.std(0)
    sd2 = np.where(sd2 == 0, 1, sd2)
    Xs = (X - mu2) / sd2
    terms = candidate_terms(X.shape[1])[:14]
    Phi = build(Xs, terms)
    lam = 1.0
    brute = []
    for i in range(0, n, 11):
        k = np.ones(n, bool)
        k[i] = False
        brute.append(y_lin[i] - float(Phi[i] @ ridge(Phi[k], y_lin[k], lam)))
    _, ana, _ = loocv(Phi, y_lin, lam)
    dif = np.max(np.abs(np.asarray(brute) - ana[::11][:len(brute)]))
    chk('★해석적 LOOCV = 실제 leave-one-out 잔차 (hat 공식, 절편 미벌점 포함)',
        dif < 1e-6, f'최대차 {dif:.2e}')
    y_noise = rng.normal(0, 1, n)
    mn = fit_target(X, y_noise, 'lin')
    chk('★순수 잡음 → LOOCV R² ≤ 0.2 (과적합을 성능으로 착각 안 함)',
        mn['loocv_r2_naive'] <= 0.2, f"R²={mn['loocv_r2_naive']:.4f} k={mn['k']}")

    print(' [2] 탐욕 전방선택 + n/k 규율 (σ_e 22.5 절제 규율)')
    chk(f'★항 수가 n/k ≥ {MIN_N_OVER_K:.0f}:1 을 지킨다 (구판은 105 항 = 2.2:1 였음)',
        m['n_over_k'] >= MIN_N_OVER_K, f"n={m['n']} k={m['k']} → {m['n_over_k']}:1")
    chk('전방선택이 실제 관계항을 골랐다 (am_pct 또는 d_am 이 선택됨)',
        any(2 in t or 1 in t for t in m['terms'] if t),
        '선택: ' + ', '.join('*'.join(DESIGN_FEATURES[i] for i in t) or '1'
                            for t in m['terms'][:5]))
    chk('★잡음 타깃에선 항을 거의 안 고른다 (다중비교 문턱이 작동)',
        mn['k'] <= 3, f"k={mn['k']} (절편 포함)")
    # 문턱 자체의 성질 — 고정값이었다면 전부 같아서 이 검사가 무의미하다
    f_small_n, f_big_n = _gain_floor(60, 105, 0.0), _gain_floor(600, 105, 0.0)
    f_few_m, f_many_m = _gain_floor(240, 5, 0.0), _gain_floor(240, 105, 0.0)
    f_lo_r2, f_hi_r2 = _gain_floor(240, 105, 0.0), _gain_floor(240, 105, 0.9)
    chk('★문턱이 n↑ 에 내려가고 · 후보 m↑ 에 올라가고 · R²↑ 에 내려간다 (셋 다 옳은 방향)',
        f_big_n < f_small_n and f_many_m > f_few_m and f_hi_r2 < f_lo_r2,
        f'n:{f_small_n:.4f}→{f_big_n:.4f}  m:{f_few_m:.4f}→{f_many_m:.4f}  '
        f'R²:{f_lo_r2:.4f}→{f_hi_r2:.4f}')

    print(' [3] 중첩 CV — 선택 편향 측정 (nested_cv_sat.py 논리)')
    nst = nested_cv(X, y_lin, 'lin', folds=5)
    chk('실제 신호에선 nested 도 높다', nst > 0.85, f'nested R²={nst:+.4f}')
    nst_noise = nested_cv(X, y_noise, 'lin', folds=5)
    chk('★잡음에선 nested 가 0 이하 (naive 가 살짝 양수여도 nested 가 폭로)',
        nst_noise <= 0.05, f'nested R²={nst_noise:+.4f} vs naive {mn["loocv_r2_naive"]:+.4f}')

    print(' [4] Laplace 사후 · PI · 커버리지 (bayesian_laplace.py 논리)')
    chk('명목 90% PI 의 경험 커버리지가 0.80–0.99',
        0.80 <= m['pi90_coverage'] <= 0.99, f"{m['pi90_coverage']*100:.1f}%")
    p0 = predict(m, X[0])
    chk('PI 가 점추정을 감싼다 (lo < value < hi)',
        p0['lo'] < p0['value'] < p0['hi'],
        f"{p0['lo']:.2f} < {p0['value']:.2f} < {p0['hi']:.2f}")
    m2 = json.loads(json.dumps(m))
    chk('★JSON 왕복 후 추론이 동일 (sklearn 없이 배포 가능)',
        abs(predict(m2, X[0])['value'] - p0['value']) < 1e-9)

    print(' [5] 외삽 게이트')
    far = X.mean(0) + 8.0 * X.std(0)
    pf = predict(m, far)
    chk('★학습 범위 밖 질의 → extrapolation=True', pf['extrapolation'],
        f"h*={pf['leverage']:.3f} vs 학습최대 {m['h_max_train']:.3f}")
    chk('★외삽에선 PI 가 넓어진다 (조용히 자신 있는 값 안 냄)',
        pf['sd'] > p0['sd'] * 1.5, f"sd {p0['sd']:.3f} → {pf['sd']:.3f}")
    chk('범위 안 질의는 extrapolation=False', not p0['extrapolation'])

    print(' [6] log 타깃 (τ·두께)')
    y_log = np.exp(0.02 * X[:, 2] + 0.1 * X[:, 5] + rng.normal(0, 0.05, n))
    ml = fit_target(X, y_log, 'log')
    chk('log 타깃 복원', ml['loocv_r2_naive'] > 0.85, f"R²={ml['loocv_r2_naive']:.4f}")
    pl = predict(ml, X[0])
    chk('log 모델의 PI 가 전부 양수 (로그정규 역변환)',
        pl['lo'] > 0 and pl['value'] > 0, f"[{pl['lo']:.3f}, {pl['hi']:.3f}]")

    print(' [7] 설계 의도 고정 (σ 배제 · regime-gate · MPM 고유량)')
    chk('★σ 삼중항이 ML 타깃이 아니다 (스케일링법칙 소관)',
        not any(t.startswith('sigma') for t, _ in STRUCTURE_TARGETS))
    chk('★porosity 타깃이 regime-gated use_porosity_pct (raw DEM/MPM 아님)',
        any(t == 'use_porosity_pct' for t, _ in STRUCTURE_TARGETS)
        and not any(t in ('porosity', 'porosity_mpm_pct') for t, _ in STRUCTURE_TARGETS))
    chk('★MPM 고유량이 타깃에 있다 (예측기가 0건 쓰던 층)',
        any('plastic_gain' in t for t, _ in STRUCTURE_TARGETS)
        and any('dg_mean' in t for t, _ in STRUCTURE_TARGETS))

    print(' [8] CSV 왕복 · 판정 · 물리 감사 · 능동학습')
    import tempfile
    # am_pct↑ → phi_am↑ / phi_se↓ 를 **데이터에 심어** 물리 감사가 잡는지 본다
    phi_am = 0.006 * X[:, 2] + rng.normal(0, 0.01, n)
    phi_se = 0.90 - 1.0 * phi_am + rng.normal(0, 0.01, n)
    with tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False, newline='') as fh:
        cols = ['name'] + DESIGN_FEATURES + ['phi_se', 'phi_am', 'use_porosity_pct', 'tau']
        w = _csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for i in range(n):
            row = {'name': f'c{i}'}
            row.update({f: X[i, j] for j, f in enumerate(DESIGN_FEATURES)})
            row.update({'phi_se': phi_se[i], 'phi_am': phi_am[i],
                        'use_porosity_pct': y_lin[i], 'tau': 1.8})
            w.writerow(row)
        cp = fh.name
    o = train(cp, verbose=False, folds=5)
    chk('CSV → 학습 왕복', 'use_porosity_pct' in o['models']
        and o['models']['use_porosity_pct']['loocv_r2_naive'] > 0.9)
    chk(f'표본 {MIN_N_TARGET} 미만 타깃은 미적합·skipped 보고',
        'coverage' in o['skipped'] and 'cn' in o['skipped'])
    chk('★판정이 nested 기준이고 USABLE 이 나온다',
        o['models']['use_porosity_pct']['verdict'] == 'USABLE',
        f"nested={o['models']['use_porosity_pct']['nested_cv_r2']:+.3f}")
    mono = o['physics_audit']['monotone']
    chk('★물리 감사가 심어둔 단조성(am_pct→phi_am ↑, →phi_se ↓)을 확인',
        len(mono) >= 2 and all(p['ok'] for p in mono
                               if p['target'] in ('phi_am', 'phi_se')),
        '; '.join(f"{p['feature']}→{p['target']} Δ={p['delta_p10_p90']:+.3f} "
                  f"{'OK' if p['ok'] else 'VIOLATION'}" for p in mono))
    # 감사의 판별력 — 부호를 뒤집은 가짜 모형은 반드시 VIOLATION 이어야
    import copy
    fake = copy.deepcopy(o)
    fake['models']['phi_am']['coef'] = [-c for c in fake['models']['phi_am']['coef']]
    fmono = physics_audit(fake, X)['monotone']
    chk('★감사에 판별력이 있다 — 부호 뒤집은 모형은 VIOLATION (돌연변이 검사)',
        any((not p['ok']) and p['target'] == 'phi_am' for p in fmono))
    sg = suggest(o, X, 'use_porosity_pct', n_out=5, n_cand=300)
    chk('능동학습이 후보를 순위화 (PI 폭 × 신규성)',
        sg['error'] is None and len(sg['rows']) == 5
        and sg['rows'][0]['score'] >= sg['rows'][-1]['score'],
        f"top score={sg['rows'][0]['score'] if sg['rows'] else 'n/a'}")
    chk('★후보가 **자유노브 6 개**만 낸다 (나머지 7 은 유도량)',
        list(sg['rows'][0]['design'].keys()) == FREE_KNOBS)
    # ★ 첫 실런이 뱉은 자기모순 설계(ln(2.92)≠0.85 등)가 재발하지 않는지
    _d0 = sg['rows'][0]['design']
    _full = derive_features(*[_d0[k] for k in FREE_KNOBS])
    chk('★제안 설계가 자기무모순 — log_d_se=ln(d_se), size_ratio_inv=d_am/d_se, d_ratio=d_se/d_am',
        abs(_full['log_d_se'] - math.log(max(_d0['d_se'], 0.1))) < 1e-9
        and abs(_full['size_ratio_inv'] - _d0['d_am'] / _d0['d_se']) < 1e-9
        and abs(_full['d_ratio'] - _d0['d_se'] / _d0['d_am']) < 1e-9,
        f"d_se={_d0['d_se']:.3f} → log_d_se={_full['log_d_se']:.3f}")
    # 판별력: 13 차원 독립 샘플이면 이 검사가 **떨어져야** 한다 (구판이 실제로 그랬음)
    _bad = dict(zip(DESIGN_FEATURES, rng.uniform(0.5, 3.0, len(DESIGN_FEATURES))))
    chk('★위 검사에 판별력이 있다 — 13 차원 독립 샘플은 자기모순으로 걸린다 (돌연변이)',
        abs(_bad['log_d_se'] - math.log(max(_bad['d_se'], 0.1))) > 1e-6)
    # REJECT 타깃엔 제안하지 않는다
    import copy as _cp
    rej = _cp.deepcopy(o)
    rej['models']['use_porosity_pct']['verdict'] = 'REJECT'
    chk('★판정 REJECT 타깃엔 제안을 거부한다 (못 맞히는 모형의 불확실성 = 잡음)',
        suggest(rej, X, 'use_porosity_pct', n_out=3, n_cand=50)['error'] is not None)
    # 로컬 사본이 predictor_engine 원본과 같은가 (있는 환경에서만 — WSL 에선 반드시 검사됨)
    try:
        import sys as _s
        _s.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), 'webapp'))
        from predictor_engine import derive_features as _pdf, INPUT_FEATURES as _PIF
        _a = _pdf(1.3, 5.0, 78.0, 0.7, 60.0, 3.2)
        chk('★DESIGN_FEATURES 가 predictor_engine.INPUT_FEATURES 와 동일 (규약 공유)',
            DESIGN_FEATURES == list(_PIF))
        chk('★유도식이 predictor_engine 과 일치 (재구현 표류 없음)',
            all(abs(float(_a[k]) - float(derive_features(1.3, 5.0, 78.0, 0.7, 60.0, 3.2)[k]))
                < 1e-9 for k in DESIGN_FEATURES))
    except Exception as _e:                                        # noqa: BLE001
        print(f'  ‥ predictor_engine 미가용 — 유도식 대조 생략 ({type(_e).__name__})')
    os.unlink(cp)

    print(' [9] 부검(diagnose) — "스위치된 타깃" vs "본래 확률적" 구별')

    def _mk(y, src):
        with tempfile.NamedTemporaryFile('w', suffix='.csv', delete=False, newline='') as f2:
            c2 = ['name', 'use_source'] + DESIGN_FEATURES + ['use_porosity_pct', 'porosity']
            w2 = _csv.DictWriter(f2, fieldnames=c2)
            w2.writeheader()
            for i in range(n):
                r2 = {'name': f'c{i}', 'use_source': src[i]}
                r2.update({f: X[i, j] for j, f in enumerate(DESIGN_FEATURES)})
                r2.update({'use_porosity_pct': y[i],
                           'porosity': 0.5 * X[i, 2] + rng.normal(0, 0.5)})   # 단일-출처
                w2.writerow(r2)
            return f2.name
    # (a) 스위치: 두 출처가 **서로 다른 함수** → 혼합은 못 배우고 부분집합은 배운다
    src = np.where(X[:, 3] > 0.5, 'DEM', 'MPM')
    y_sw = np.where(src == 'DEM', 0.5 * X[:, 2], 60.0 - 0.5 * X[:, 2]) + rng.normal(0, 0.5, n)
    p_sw = _mk(y_sw, src)
    d_sw = diagnose(p_sw, 'use_porosity_pct', folds=5)
    chk('★스위치된 타깃을 SWITCHED 로 진단 (부분집합이 혼합보다 뚜렷이 높다)',
        d_sw['verdict'].startswith('SWITCHED'),
        f"혼합 {d_sw['mixture']['nested']:+.3f} → "
        + ' / '.join(f"{g} {v['nested']:+.3f}" for g, v in d_sw['groups'].items()
                     if v['nested'] is not None))
    # (b) 본래 확률적: 출처와 무관한 잡음 → 좁혀도 안 좋아진다
    y_in = 0.3 * X[:, 2] + rng.normal(0, 12.0, n)
    p_in = _mk(y_in, src)
    d_in = diagnose(p_in, 'use_porosity_pct', folds=5)
    chk('★본래 확률적인 타깃은 INTRINSIC (좁혀도 개선 없음 — 처방이 반대)',
        d_in['verdict'].startswith('INTRINSIC'),
        f"혼합 {d_in['mixture']['nested']:+.3f} → "
        + ' / '.join(f"{g} {v['nested']:+.3f}" for g, v in d_in['groups'].items()
                     if v['nested'] is not None))
    chk('부검이 단일-출처 원열과도 대조한다 (--diagnose-vs)',
        diagnose(p_sw, 'use_porosity_pct', vs='porosity', folds=5)['vs']['nested'] > 0.8)
    os.unlink(p_sw)
    os.unlink(p_in)

    print(f"ML-DESIGN-STRUCTURE SELFTEST {ok}/{tot} {'PASS' if ok == tot else 'FAIL'}")
    return 0 if ok == tot else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--csv', default='docs/data/design_performance_corpus.csv',
                    help='design_performance_dataset.py 산출 CSV')
    ap.add_argument('--out', default='', help='계수 JSON 경로 (webapp 추론용)')
    ap.add_argument('--folds', type=int, default=10, help='중첩 CV 의 outer 폴드 수')
    ap.add_argument('--no-nested', action='store_true',
                    help='중첩 CV 생략 (빠르지만 선택 편향을 못 잰다 — 보고용으로 쓰지 말 것)')
    ap.add_argument('--suggest', type=int, default=0, metavar='N',
                    help='능동학습: 다음 DEM 후보 N 개.  자유노브 6 개만 출력한다 '
                         '(나머지 7 개는 유도량이라 그대로 시뮬에 넣을 수 있음)')
    ap.add_argument('--suggest-target', default='tau',
                    help='제안을 뽑을 타깃 (판정 USABLE 이어야 함)')
    ap.add_argument('--allow-weak', action='store_true',
                    help='WEAK 타깃에도 제안 강행 (REJECT 는 여전히 거부)')
    ap.add_argument('--diagnose', default='', metavar='TARGET',
                    help='REJECT/WEAK 부검 — 출처별로 쪼개 혼합 자체가 문제인지 본다')
    ap.add_argument('--split-by', default='use_source', help='--diagnose 의 분할 열')
    ap.add_argument('--diagnose-vs', default='', metavar='COL',
                    help='--diagnose 와 비교할 단일-출처 원열 (예: porosity = raw DEM)')
    a = ap.parse_args(argv)
    if a.selftest:
        raise SystemExit(_selftest())
    if not os.path.isfile(a.csv):
        print(f'CSV 없음: {a.csv}\n  먼저: python3 scripts/design_performance_dataset.py --out {a.csv}')
        return 1
    if a.diagnose:
        print(f'부검 — {a.diagnose}  (분할: {a.split_by})')
        d = diagnose(a.csv, a.diagnose, split_by=a.split_by,
                     vs=a.diagnose_vs or None, folds=a.folds)
        _f = lambda v: ('  n/a' if v is None else f'{v:+.3f}')          # noqa: E731
        print(f"  혼합 전체            n={d['mixture']['n']:4d}  nested {_f(d['mixture']['nested'])}")
        for g, v in d['groups'].items():
            print(f"  └ {a.split_by}={g:<18s} n={v['n']:4d}  nested {_f(v['nested'])}"
                  + ('   (표본 부족 — 미적합)' if v['nested'] is None else ''))
        if d['vs']:
            print(f"  단일-출처 원열 {d['vs']['column']:<12s} n={d['vs']['n']:4d}  "
                  f"nested {_f(d['vs']['nested'])}")
        print(f"  ⇒ {d['verdict']}")
        return 0
    print(f'설계 → 구조 학습 — {a.csv}')
    b = train(a.csv, a.out or None, folds=a.folds, do_nested=not a.no_nested)
    if a.suggest:
        X, _ys, _n, _r = load_corpus(a.csv)
        res = suggest(b, X, a.suggest_target, n_out=a.suggest, allow_weak=a.allow_weak)
        if res['error']:
            print(f"\n  능동학습 거부 — {res['error']}")
            _use = [t for t, m in b['models'].items() if m.get('verdict') == 'USABLE']
            print(f"    USABLE 타깃: {', '.join(_use) if _use else '(없음)'}")
            return 0
        print(f"\n  능동학습 — 다음 DEM 후보 ({res['target']}, 판정 {res['verdict']}, "
              'PI 폭 × 신규성):')
        for i, s in enumerate(res['rows'], 1):
            print(f"   {i:2d}. score={s['score']:8.3f}  pred={s['pred']:8.3f} "
                  f"PI90={s['pi90']}  novelty={s['novelty']}"
                  + ('  ⚠외삽' if s['extrapolation'] else ''))
            print('       ' + '  '.join(f'{k}={v}' for k, v in s['design'].items()))
        print('   ★ 위 6 개가 자유노브 전부다 — 나머지 7 특징은 여기서 유도된다.')
        print('   CAVEAT: 휴리스틱 플래너다 — 진짜 정보이득은 그 점을 실제로 돌려야 안다.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

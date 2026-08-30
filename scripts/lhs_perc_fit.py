#!/usr/bin/env python3
"""퍼콜레이션 문턱 `φ_c` — Firth 벌점 로지스틱 (primary) + 일반 MLE (병기).

    python3 scripts/lhs_perc_fit.py --csv perc_table.csv
    python3 scripts/lhs_perc_fit.py --csv perc_table.csv --batch-col batch
    python3 scripts/lhs_perc_fit.py --selftest

사전등록 `docs/reviews/lhs_extension_prereg_v2_20260829.md` §4-2 · §4-3 · §4-4 · §4-4b 를
**실행 가능한 형태로** 옮긴 것.  Codex R11 B1: *"분석기가 결과 전에 커밋돼야 규약이 실재한다."*

═══ 모형과 추정량 ═══

`logit P(perc = 1) = a + b·φ_AM`,  **`φ_c ≡ P = 0.5` ⇒ `φ_c = −a/b`**.
`0.5` 는 문턱의 **정의**(대칭점)라 자유도가 없다 — 사후에 고르는 값이 아니다.

**Firth 가 primary 인 이유**: 0 과 1 이 다 관측돼도 **완전·준완전 분리**면 일반 MLE 가
발산해 `−a/b` 가 **존재하지 않는다**.  발산했을 때 무엇을 보고할지 결과를 보고 정하는 것을
막으려고 **런 전에** Firth 를 primary 로 못박았다.  분리가 없으면 둘은 거의 같다.

Firth 벌점 = Jeffreys 사전 → 벌점 로그우도
    l*(β) = Σ [y log p + (1−y) log(1−p)] + ½ log det(Xᵀ W X),   W = diag(p(1−p))
수정 점수
    U*(β) = Xᵀ(y − p) + Xᵀ[(h/2)(1 − 2p)],   h = diag(W^½ X (XᵀWX)⁻¹ Xᵀ W^½)

**95 % 구간은 프로파일 우도**다 (Wald 아님 — 분리 근처에서 Wald 는 무너진다).
`φ_c` 를 직접 프로파일한다: 후보 `φ_c` 마다 `a = −b·φ_c` 로 묶고 `b` 하나만 최대화해
`2(l*_max − l*_prof) ≤ χ²₁,₀.₉₅ = 3.8415` 인 구간을 **양방향 이분법**으로 찾는다.
⚠ 한쪽이 안 닫히면 그쪽을 `null`(무한)로 적는다 — **자르지 않는다**.

═══ 사전등록 §4-4 예외 — 코드가 강제한다 ═══

| 관측 | 이 도구가 내는 것 |
|---|---|
| 전부 `perc = 0` | `verdict = NOT_IDENTIFIED`, `pattern = all_zero`, `phi_c = null`, **`bound = null`** |
| 전부 `perc = 1` | `verdict = NOT_IDENTIFIED`, `pattern = all_one`, `phi_c = null`, **`bound = null`** |
| Firth 비수렴 · 프로파일 건전성 위반 | `verdict = FIT_FAILED` — 점추정·구간 **없음** |
| `b <= 0` | `verdict = SIGN_REVERSED`, `phi_c = null` (φ 가 늘수록 퍼콜이 준다 = 부호 역전) |
| 완전·준완전 분리 | `separation` 에 종류를 적고 **MLE 는 `diverged`** 로 적는다.  Firth 는 그대로 보고 |
| 미확정 점이 남음 | `--unresolved-col` → **전부 0 / 전부 1 두 극단**을 돌려 `sensitivity_split` 로 판정.  갈리면 `phi_c` 점추정 인용 금지 플래그를 세운다 |

★ 방향 규약 (사전등록 §4-4 의 정정 그대로): 퍼콜 확률은 φ_AM 에 **증가**한다.

⚠⚠ **정정 2026-08-30 (Codex R14 P1-03)** — 옛 판은 위 방향에서 **결정론적 부등식**을 냈다
(전부 0 ⇒ `φ_c ≥ max φ`).  그것은 관측모형과 모순이다: 관측은 Bernoulli 확률곡선이라
참 문턱이 창 **안**에 있어도 전부 0 이 나올 수 있다.  이 64개 설계 φ 에서
`logit P = 100(φ − 0.48)` 이면 참 `φ_c = 0.48` 이 관측 최댓값 `0.485723` 안쪽인데도
**P(all zero) = 0.062** 다 (selftest ⑤-b 가 계산한다).  ⇒ 이제 `NOT_IDENTIFIED` 만 내고
**점추정도 hard 부등식도 내지 않는다**.  수치 경계가 필요하면 **결과 전에 등록한**
단조모형의 one-sided profile confidence set 이어야 한다.

═══ 배치 (§4-3) ═══

**신규 64점이 primary.**  기존 130점은 보조이고 **하나의 로지스틱에 합치지 않는다** —
두 배치의 φ 범위가 거의 겹치지 않아 batch 가 φ 와 **교락**되기 때문이다.
`--batch-col` 을 주면 **배치별 곡선을 따로** 적합해 나란히 낸다 (§4-3 (a) = primary 보조).
합친 적합은 `--pooled-sensitivity` 로만 나오고, 그때 **batch indicator 를 반드시 넣는다**
(§4-3 (b)).  지시자 없는 pooling 은 **거부한다**.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys

import numpy as np

CHI2_1DOF_95 = 3.841458820694124
_MAXIT = 200
_TOL = 1e-10
#: MLE 발산 판정 — 계수가 이보다 커지면 "발산" 으로 적는다 (분리의 수치적 지문).
_DIVERGE_ABS = 1e4


class FitRefusal(RuntimeError):
    """사전등록이 금지한 적합을 요청받았다."""


# ──────────────────────────────────────────────────────────────────────────────
# 로지스틱 — 일반 MLE 와 Firth
# ──────────────────────────────────────────────────────────────────────────────
def _p(X, beta):
    z = X @ beta
    # 오버플로 없는 시그모이드
    out = np.empty_like(z)
    pos = z >= 0
    out[pos] = 1.0 / (1.0 + np.exp(-z[pos]))
    e = np.exp(z[~pos])
    out[~pos] = e / (1.0 + e)
    return out


def _info(X, p):
    w = p * (1.0 - p)
    return X.T @ (X * w[:, None]), w


def _hat(X, w):
    """h = diag(W^½ X (XᵀWX)⁻¹ Xᵀ W^½)."""
    Xw = X * np.sqrt(w)[:, None]
    I = Xw.T @ Xw
    try:
        Iinv = np.linalg.pinv(I)
    except np.linalg.LinAlgError:                      # pragma: no cover
        Iinv = np.linalg.pinv(I + 1e-12 * np.eye(I.shape[0]))
    return np.einsum('ij,jk,ik->i', Xw, Iinv, Xw)


def loglik(X, y, beta):
    p = np.clip(_p(X, beta), 1e-300, 1 - 1e-16)
    return float(np.sum(y * np.log(p) + (1 - y) * np.log1p(-p)))


def penalised_loglik(X, y, beta):
    p = _p(X, beta)
    I, _w = _info(X, p)
    sign, logdet = np.linalg.slogdet(I)
    if sign <= 0:
        logdet = -np.inf
    return loglik(X, y, beta) + 0.5 * logdet


def fit_firth(X, y, beta0=None, fixed=None):
    """Firth 벌점 로지스틱.  `fixed` = {col: value} 로 일부 계수를 고정할 수 있다.

    → (beta, converged).  고정 계수가 있으면 나머지만 갱신한다 (프로파일 우도용).
    """
    k = X.shape[1]
    beta = np.zeros(k) if beta0 is None else np.array(beta0, dtype=float)
    free = np.array([j for j in range(k) if not (fixed and j in fixed)])
    if fixed:
        for j, v in fixed.items():
            beta[j] = v
    if len(free) == 0:
        return beta, True
    for _ in range(_MAXIT):
        p = _p(X, beta)
        I, w = _info(X, p)
        h = _hat(X, w)
        U = X.T @ (y - p + h * (0.5 - p))
        If = I[np.ix_(free, free)]
        try:
            step = np.linalg.solve(If, U[free])
        except np.linalg.LinAlgError:                  # pragma: no cover
            step = np.linalg.pinv(If) @ U[free]
        # step-halving — 벌점 우도가 늘 때만 받는다
        cur = penalised_loglik(X, y, beta)
        for _h in range(30):
            cand = beta.copy()
            cand[free] = beta[free] + step
            if np.all(np.isfinite(cand)) and penalised_loglik(X, y, cand) >= cur - 1e-12:
                break
            step = step * 0.5
        else:                                          # pragma: no cover
            return beta, False
        delta = np.max(np.abs(cand - beta))
        beta = cand
        if delta < _TOL:
            return beta, True
    return beta, False


def fit_mle(X, y):
    """벌점 없는 로지스틱.  분리면 계수가 발산한다 — 그 사실을 그대로 돌려준다.

    → (beta, status) · status ∈ {'ok', 'diverged', 'not_converged'}
    """
    k = X.shape[1]
    beta = np.zeros(k)
    for _ in range(_MAXIT):
        p = _p(X, beta)
        I, _w = _info(X, p)
        U = X.T @ (y - p)
        try:
            step = np.linalg.solve(I, U)
        except np.linalg.LinAlgError:
            return beta, 'diverged'
        cur = loglik(X, y, beta)
        for _h in range(30):
            cand = beta + step
            if np.all(np.isfinite(cand)) and loglik(X, y, cand) >= cur - 1e-12:
                break
            step = step * 0.5
        else:                                          # pragma: no cover
            return beta, 'not_converged'
        delta = np.max(np.abs(cand - beta))
        beta = cand
        if np.max(np.abs(beta)) > _DIVERGE_ABS:
            return beta, 'diverged'
        if delta < _TOL:
            return beta, 'ok'
    return beta, 'not_converged'


# ──────────────────────────────────────────────────────────────────────────────
# 분리 판정 (1-D 예측자)
# ──────────────────────────────────────────────────────────────────────────────
def separation_kind(phi, y):
    """'none' · 'quasi' · 'complete'.

    1차원 예측자에서는 정렬 하나로 결정된다 — 어떤 절단점이 두 군을 완전히 가르면
    **완전 분리**, 겹침이 **동점 φ 에서만** 일어나면 **준완전 분리**다.
    """
    phi = np.asarray(phi, dtype=float)
    y = np.asarray(y, dtype=int)
    if len(np.unique(y)) < 2:
        return 'degenerate'
    for sgn in (+1.0, -1.0):
        v = sgn * phi
        v0 = v[y == 0]
        v1 = v[y == 1]
        if v0.max() < v1.min():
            return 'complete'
        if v0.max() <= v1.min():
            return 'quasi'
    return 'none'


# ──────────────────────────────────────────────────────────────────────────────
# φ_c 와 프로파일 우도 구간
# ──────────────────────────────────────────────────────────────────────────────
_GOLD = (5.0 ** 0.5 - 1.0) / 2.0


def _profile_at(X, y, phi_c, b_hint=1.0):
    """`a = −b·φ_c` 로 묶고 **원래 2계수 벌점우도**를 b 에 대해서만 최대화.

    ★★ 이전 판은 설계행렬을 `[1, φ]` → `[φ − φ_c]` **1계수로 바꿔서** 적합했다.  제약은
      그렇게 걸리지만 Jeffreys 벌점 ½·log det I 가 **다른 정보행렬**의 것이 되어, 기준
      `lmax` 와 **다른 목적함수**를 비교하게 된다.  실제로 완전분리 fixture 에서 자기
      점추정의 deviance 가 **음수**(−0.459)로 나왔다 — 프로파일 우도로서 성립하지 않는
      지문이다 (Codex R14 P1-02).
    ⇒ 프로파일 벌점우도는 후보 `φ_c` 를 고정한 뒤 **같은 joint 벌점우도**에서 나머지
      모수만 최적화해야 한다 (`logistf` 규약).  그러면 `D(φ̂) = 0` 이 항등적으로 성립한다.
    b > 0 만 훑는다 — b ≤ 0 은 호출부가 `SIGN_REVERSED` 로 먼저 거른다.
    """
    def f(b):
        return penalised_loglik(X, y, np.array([-b * phi_c, b], dtype=float))

    lo, hi = 1e-9, max(abs(float(b_hint)) * 4.0, 1.0)
    bracketed = False
    for _ in range(200):                      # 최댓값이 안쪽에 들어올 때까지 확장
        if f(hi) < f(hi / 1.6):
            bracketed = True
            break
        hi *= 1.6
        if not np.isfinite(hi):
            break
    if not bracketed:
        return f(hi), False                   # 경계에서 계속 오른다 = 비수렴
    a, b = lo, hi
    c, d = b - _GOLD * (b - a), a + _GOLD * (b - a)
    fc, fd = f(c), f(d)
    for _ in range(300):
        if (b - a) < 1e-13 * max(1.0, abs(b)):
            break
        if fc > fd:
            b, d, fd = d, c, fc
            c = b - _GOLD * (b - a)
            fc = f(c)
        else:
            a, c, fc = c, d, fd
            d = a + _GOLD * (b - a)
            fd = f(d)
    return f(0.5 * (a + b)), True


def profile_ci_phi_c(X, y, phi_hat, lmax, span, level=CHI2_1DOF_95, b_hint=1.0):
    """`2(l*_max − l*(φ_c)) ≤ level` 인 구간을 양방향 이분법으로.

    한쪽이 탐색 폭 안에서 안 닫히면 그쪽은 `None` (무한) — **자르지 않는다**.
    → `(lo, hi, diag)`.  `diag['ok']` 가 False 면 **구간을 인용하면 안 된다**.

    ★ 건전성 두 가지를 실제로 **잰다** (R14 P1-02).  프로파일 우도라면 반드시 성립한다:
      ⓐ `D(φ̂) = 0`   ⓑ 모든 후보에서 `D ≥ 0`.
      이전 판은 둘 다 위반했고(자기 점추정에서 −0.459) 그래도 구간을 냈다.
    """
    def dev(pc):
        lp, ok = _profile_at(X, y, pc, b_hint=b_hint)
        return 2.0 * (lmax - lp), ok

    diag = {'dev_at_hat': None, 'min_dev': None, 'converged': True, 'ok': True,
            'why': []}
    d_hat, ok_hat = dev(phi_hat)
    diag['dev_at_hat'] = float(d_hat)
    diag['converged'] = bool(ok_hat)
    if not ok_hat:
        diag['why'].append('점추정에서 프로파일 최적화가 비수렴')
    if abs(d_hat) > 1e-4:
        diag['why'].append(f'D(φ̂) = {d_hat:.3e} ≠ 0 — 프로파일 우도가 아니다')

    def dev1(pc):
        v, ok = dev(pc)
        if not ok:
            diag['converged'] = False
        if diag['min_dev'] is None or v < diag['min_dev']:
            diag['min_dev'] = float(v)
        if v < -1e-4:
            diag['why'].append(f'D({pc:.6g}) = {v:.3e} < 0')
        return v

    out = []
    for direction in (-1.0, +1.0):
        step = max(span, 1e-3) * 0.05
        lo = phi_hat
        hi = phi_hat
        found = False
        for _ in range(60):
            hi = hi + direction * step
            if dev1(hi) > level:
                found = True
                break
            step *= 1.6
        if not found:
            out.append(None)
            continue
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if dev1(mid) > level:
                hi = mid
            else:
                lo = mid
            if abs(hi - lo) < 1e-9:
                break
        out.append(0.5 * (lo + hi))
    diag['ok'] = bool(diag['converged'] and not diag['why'])
    return out[0], out[1], diag


# ──────────────────────────────────────────────────────────────────────────────
# 한 배치의 판정
# ──────────────────────────────────────────────────────────────────────────────
def fit_curve(phi, y, label='all'):
    phi = np.asarray(phi, dtype=float)
    y = np.asarray(y, dtype=int)
    n = len(y)
    res = dict(label=label, n=n, n_perc=int(y.sum()),
               phi_min=float(phi.min()) if n else None,
               phi_max=float(phi.max()) if n else None,
               separation=None, firth=None, mle=None, pattern=None, profile=None,
               phi_c=None, ci95=None, bound=None, verdict=None, notes=[])
    if n == 0:
        res['verdict'] = 'EMPTY'
        return res

    # §4-4 — 창 전체가 한쪽인 경우.
    #  ★★ 옛 판은 여기서 **결정론적 부등식**을 냈다 (전부 0 ⇒ φ_c ≥ max φ).  그것은
    #    관측모형과 모순이다 (R14 P1-03): 관측은 Bernoulli 확률곡선이라, 참 문턱이 창
    #    **안**에 있어도 64점이 전부 0 으로 나올 확률이 0 이 아니다.  실제로 이 64개 φ 에서
    #    logit P = 100(φ − 0.48) 이면 참 φ_c = 0.48 이 관측 최댓값 0.485723 **안쪽**인데도
    #    P(all zero) = 0.0623 이다.  ⇒ `all zero ⇒ φ_c ≥ max φ` 는 **논리적으로 거짓**이다.
    #  ⇒ 창 안에서 전이를 못 봤다는 사실만 적고, 점추정도 hard 부등식도 내지 않는다.
    #    수치 경계가 필요하면 **결과 전에 등록한** 단조모형의 one-sided profile set 이어야 한다.
    if y.sum() == 0 or y.sum() == n:
        side = 'all_zero' if y.sum() == 0 else 'all_one'
        res.update(verdict='NOT_IDENTIFIED', pattern=side, bound=None)
        res['notes'].append(
            f'창에서 {"전부 미퍼콜" if side == "all_zero" else "전부 퍼콜"} ⇒ '
            '**관측창 안에서 전이를 보지 못했다.**  φ_c 점추정도 hard 부등식도 인용하지 '
            '않는다 — Bernoulli 관측에서는 참 문턱이 창 안이어도 이 결과가 나올 수 있다')
        return res

    res['separation'] = separation_kind(phi, y)
    X = np.column_stack([np.ones(n), phi])

    bF, okF = fit_firth(X, y)
    res['firth'] = dict(a=float(bF[0]), b=float(bF[1]), converged=bool(okF))
    bM, stM = fit_mle(X, y)
    res['mle'] = dict(a=float(bM[0]), b=float(bM[1]), status=stM)
    if stM != 'ok':
        res['notes'].append(f'일반 MLE {stM} — 분리({res["separation"]})의 수치적 지문이다.  '
                            'Firth 가 primary 라 판정은 유지된다')

    if bF[1] <= 0:
        res.update(verdict='SIGN_REVERSED')
        res['notes'].append('b <= 0 (φ_AM 이 늘수록 퍼콜 확률이 준다) ⇒ φ_c 를 인용하지 않는다')
        return res

    #  ★ Firth 자체가 비수렴이면 점추정을 내지 않는다 (R14 P1-05).  옛 판은
    #    `converged=false` 인 2행 fixture 에서도 `verdict="OK"` 와 φ_c 를 냈다.
    if not okF:
        res.update(verdict='FIT_FAILED')
        res['notes'].append('Firth 벌점우도가 비수렴 — 점추정·구간을 내지 않는다')
        return res

    phi_hat = float(-bF[0] / bF[1])
    lmax = penalised_loglik(X, y, bF)
    span = float(phi.max() - phi.min()) or 1.0
    lo, hi, diag = profile_ci_phi_c(X, y, phi_hat, lmax, span, b_hint=float(bF[1]))
    res['profile'] = diag
    if not diag['ok']:
        #  프로파일이 건전성(D(φ̂)=0 · D≥0)을 못 지키면 **구간을 인용하지 않는다**.
        res.update(phi_c=phi_hat, ci95=None, verdict='FIT_FAILED')
        res['notes'].append(
            '프로파일 우도 건전성 위반 — 구간을 내지 않는다: ' + '; '.join(diag['why'][:3]))
        return res
    res.update(phi_c=phi_hat, ci95=[lo, hi], verdict='OK')
    if lo is None or hi is None:
        res['notes'].append('프로파일 구간의 한쪽이 안 닫힌다 — 무한으로 적는다 (자르지 않는다)')
    if not (phi.min() <= phi_hat <= phi.max()):
        res['notes'].append('φ_c 가 관측 창 **밖**이다 = 외삽.  창 경계와 함께 읽을 것')
    return res


# ──────────────────────────────────────────────────────────────────────────────
# 미확정 점 — §4-4b 두 극단 sensitivity
# ──────────────────────────────────────────────────────────────────────────────
def unresolved_sensitivity(phi_ok, y_ok, phi_un, label='all'):
    """미확정을 전부 0 / 전부 1 로 놓은 두 적합.  갈리면 점추정 인용 금지."""
    if len(phi_un) == 0:
        return None
    lo = fit_curve(np.concatenate([phi_ok, phi_un]),
                   np.concatenate([y_ok, np.zeros(len(phi_un), dtype=int)]),
                   label=f'{label}|unresolved=0')
    hi = fit_curve(np.concatenate([phi_ok, phi_un]),
                   np.concatenate([y_ok, np.ones(len(phi_un), dtype=int)]),
                   label=f'{label}|unresolved=1')
    same_verdict = lo['verdict'] == hi['verdict'] == 'OK'
    split = True
    if same_verdict and lo['phi_c'] is not None and hi['phi_c'] is not None:
        # 두 극단의 φ_c 가 서로의 95 % 구간 안에 들면 "갈리지 않음"
        def inside(v, ci):
            a, b = ci
            return ((a is None) or v >= a) and ((b is None) or v <= b)
        split = not (inside(lo['phi_c'], hi['ci95']) and inside(hi['phi_c'], lo['ci95']))
    return dict(n_unresolved=int(len(phi_un)), all_zero=lo, all_one=hi,
                split=bool(split),
                note=('두 극단이 갈린다 ⇒ φ_c 점추정 인용 금지 (§4-4b)' if split
                      else '두 극단이 서로의 구간 안 ⇒ 미확정이 판정을 뒤집지 않는다'))


# ──────────────────────────────────────────────────────────────────────────────
# 설계 원장 대조 — **결과행을 지우면 사전등록을 우회한다** (R14 P1-04)
# ──────────────────────────────────────────────────────────────────────────────
def design_census(design_path, expect_sha256, result_ids, id_col='id'):
    """봉인된 설계 CSV 와 결과 ID 를 대조한다.  → (census, refusals)

    ★ 왜 필요한가: 사전등록은 미완주를 **누락하지 않고** 양극단 sensitivity 로 보내겠다고
      적었는데, 적합기는 **주어진 행만** 읽었다.  그래서 실패한 런을 결과 CSV 에서 **빼면**
      complete-case 적합이 조용히 진행된다 — 등록을 우회하는 가장 쉬운 경로다.
    ⇒ 설계 64행에 결과를 **left join** 하고, 결과가 없는 ID 는 자동으로 `unresolved` 로
      돌린다.  등록에 없는 ID·중복 ID·SHA 불일치는 **거부**한다 (fail-closed).
    """
    import hashlib
    refusals = []
    raw = open(design_path, 'rb').read()
    sha = hashlib.sha256(raw).hexdigest()
    if expect_sha256 and sha != expect_sha256:
        refusals.append(f'설계 CSV sha256 불일치 — 기대 {expect_sha256[:12]}… '
                        f'실제 {sha[:12]}…  (봉인된 설계가 아니다)')
    import io as _io
    drows = list(csv.DictReader(_io.StringIO(raw.decode('utf-8-sig'))))
    if not drows:
        refusals.append(f'{design_path}: 설계 행이 없다')
        return dict(sha256=sha), refusals
    if id_col not in drows[0]:
        refusals.append(f'설계 CSV 에 `{id_col}` 열이 없다')
        return dict(sha256=sha), refusals
    design_ids = [r[id_col] for r in drows]
    if len(set(design_ids)) != len(design_ids):
        refusals.append('설계 CSV 안에 ID 중복이 있다')
    dset = set(design_ids)
    rlist = list(result_ids)
    dup = sorted({i for i in rlist if rlist.count(i) > 1})
    extra = sorted(set(rlist) - dset)
    missing = [i for i in design_ids if i not in set(rlist)]
    if dup:
        refusals.append(f'결과에 중복 ID {len(dup)}개 — 예: {", ".join(dup[:3])}')
    if extra:
        refusals.append(f'설계에 없는 ID {len(extra)}개 — 예: {", ".join(extra[:3])}')
    return dict(sha256=sha, n_design=len(design_ids), n_result=len(rlist),
                missing=missing, extra=extra, duplicate=dup,
                rows={r[id_col]: r for r in drows}), refusals


# ──────────────────────────────────────────────────────────────────────────────
# CSV
# ──────────────────────────────────────────────────────────────────────────────
def load_csv(path, phi_col, perc_col, batch_col, unresolved_col):
    rows = []
    with open(path, newline='', encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            if not r or all((v or '').strip() == '' for v in r.values()):
                continue
            rows.append(r)
    if not rows:
        raise FitRefusal(f'{path}: 행이 없다')
    for need in (phi_col, perc_col):
        if need not in rows[0]:
            raise FitRefusal(f'{path}: 열 `{need}` 이 없다 (있는 열: {list(rows[0])})')
    phi, y, batch, unres = [], [], [], []
    for r in rows:
        u = False
        if unresolved_col and unresolved_col in r:
            u = str(r[unresolved_col]).strip().lower() in ('1', 'true', 'yes', 'unresolved')
        raw = str(r[perc_col]).strip()
        if not u:
            if raw not in ('0', '1'):
                raise FitRefusal(f'`{perc_col}` = {raw!r} — 0/1 이 아니다.  미확정이면 '
                                 f'`{unresolved_col or "unresolved"}` 열로 표시할 것 (§4-4b)')
            y.append(int(raw))
        else:
            y.append(-1)
        phi.append(float(r[phi_col]))
        unres.append(u)
        batch.append(str(r[batch_col]).strip() if batch_col and batch_col in r else 'all')
    return (np.asarray(phi), np.asarray(y, dtype=int),
            np.asarray(batch, dtype=object), np.asarray(unres, dtype=bool))


def analyse(phi, y, batch, unres, pooled_sensitivity=False):
    out = dict(curves=[], pooled=None, unresolved=None)
    labels = sorted(set(batch.tolist()))
    for lb in labels:
        m = (batch == lb) & (~unres)
        cur = fit_curve(phi[m], y[m], label=lb)
        sens = unresolved_sensitivity(phi[m], y[m], phi[(batch == lb) & unres], label=lb)
        if sens:
            cur['unresolved_sensitivity'] = sens
        out['curves'].append(cur)
    if len(labels) > 1:
        out['note'] = ('배치별로 **따로** 적합했다 (§4-3 (a)).  합친 적합은 batch 가 φ 와 '
                       '교락되므로 primary 가 아니다')
    if pooled_sensitivity:
        if len(labels) < 2:
            raise FitRefusal('--pooled-sensitivity 는 배치가 둘 이상일 때만 뜻이 있다')
        m = ~unres
        codes = np.array([labels.index(b) for b in batch[m]], dtype=float)
        if len(labels) > 2:
            raise FitRefusal('배치가 셋 이상이면 지시자 하나로 담을 수 없다 — 쌍으로 나눠 부를 것')
        X = np.column_stack([np.ones(m.sum()), phi[m], codes])
        bF, okF = fit_firth(X, y[m])
        out['pooled'] = dict(
            note=('§4-3 (b) sensitivity — **batch indicator 포함**.  지시자 없는 pooling 은 '
                  '거부한다 (배치가 φ 와 교락된다)'),
            labels=labels, a=float(bF[0]), b_phi=float(bF[1]), b_batch=float(bF[2]),
            converged=bool(okF))
    return out


# ──────────────────────────────────────────────────────────────────────────────
# selftest
# ──────────────────────────────────────────────────────────────────────────────
def selftest():
    ok, bad = 0, []

    def chk(name, cond, extra=''):
        nonlocal ok
        if cond:
            ok += 1
        else:
            bad.append(f'{name} {extra}')

    rng = np.random.default_rng(20260829)

    # ── 1. 진짜 로지스틱을 회복한다 ────────────────────────────────────────
    a_t, b_t = -12.0, 40.0                       # φ_c = 0.30
    phi = rng.uniform(0.15, 0.50, 400)
    pr = 1 / (1 + np.exp(-(a_t + b_t * phi)))
    y = (rng.uniform(size=phi.size) < pr).astype(int)
    r1 = fit_curve(phi, y)
    chk('1 verdict OK', r1['verdict'] == 'OK', str(r1['verdict']))
    chk('1 φ_c 회복', abs(r1['phi_c'] - 0.30) < 0.03, str(r1['phi_c']))
    chk('1 구간이 참값을 덮는다', r1['ci95'][0] < 0.30 < r1['ci95'][1], str(r1['ci95']))
    chk('1 구간이 점추정을 덮는다', r1['ci95'][0] < r1['phi_c'] < r1['ci95'][1])
    chk('1 분리 없음', r1['separation'] == 'none', str(r1['separation']))
    chk('1 MLE 정상', r1['mle']['status'] == 'ok', str(r1['mle']['status']))
    chk('1 분리 없으면 Firth≈MLE', abs(r1['firth']['b'] - r1['mle']['b']) / abs(r1['mle']['b']) < 0.2,
        f"{r1['firth']['b']} vs {r1['mle']['b']}")

    # ── 2. 완전 분리 — MLE 발산, Firth 유한 (★ Firth 가 primary 인 이유) ────
    phis = np.array([0.20, 0.22, 0.24, 0.26, 0.34, 0.36, 0.38, 0.40])
    ys = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    r2 = fit_curve(phis, ys)
    chk('2 완전 분리 인식', r2['separation'] == 'complete', str(r2['separation']))
    chk('2 MLE 발산', r2['mle']['status'] == 'diverged', str(r2['mle']['status']))
    chk('2 Firth 유한', np.isfinite(r2['firth']['b']) and abs(r2['firth']['b']) < 1e3,
        str(r2['firth']['b']))
    chk('2 φ_c 가 간격 안', 0.26 <= r2['phi_c'] <= 0.34, str(r2['phi_c']))
    chk('2 발산을 문구로 남긴다', any('MLE' in s for s in r2['notes']))

    # ── 3. 준완전 분리 (동점 φ 에서만 겹침) ────────────────────────────────
    phq = np.array([0.20, 0.22, 0.30, 0.30, 0.38, 0.40])
    yq = np.array([0, 0, 0, 1, 1, 1])
    chk('3 준완전 분리 인식', separation_kind(phq, yq) == 'quasi', separation_kind(phq, yq))

    # ── 4·5. 창 전체가 한쪽 → NOT_IDENTIFIED, **hard 부등식 없음** (R14 P1-03) ──
    #   ⚠ 옛 검사는 `bound = ('>=', max φ)` 를 **요구**했다 — 즉 검사가 틀린 규약을
    #     지키고 있었다.  Bernoulli 관측에서 참 문턱이 창 안이어도 전부 0 이 나올 수 있으므로
    #     그 부등식은 논리적으로 거짓이다.  아래 ⑤-b 가 그 확률을 실제로 계산해 못박는다.
    r4 = fit_curve(np.array([0.10, 0.15, 0.20]), np.zeros(3, dtype=int))
    chk('4 NOT_IDENTIFIED', r4['verdict'] == 'NOT_IDENTIFIED', str(r4['verdict']))
    chk('4 pattern=all_zero', r4['pattern'] == 'all_zero', str(r4['pattern']))
    chk('★4 hard 부등식을 내지 않는다', r4['bound'] is None, str(r4['bound']))
    chk('4 점추정 없음', r4['phi_c'] is None)

    r5 = fit_curve(np.array([0.40, 0.50, 0.60]), np.ones(3, dtype=int))
    chk('5 NOT_IDENTIFIED', r5['verdict'] == 'NOT_IDENTIFIED', str(r5['verdict']))
    chk('5 pattern=all_one', r5['pattern'] == 'all_one', str(r5['pattern']))
    chk('★5 hard 부등식을 내지 않는다', r5['bound'] is None, str(r5['bound']))
    chk('5 점추정 없음', r5['phi_c'] is None)

    # ── 5-b. 그 부등식이 왜 거짓인가 — 반례를 **계산해서** 둔다 ──────────────
    #   64개 설계 φ 에서 logit P = 100(φ − 0.48) 이면 참 φ_c = 0.48 이 관측 최댓값
    #   0.485723 **안쪽**인데도 전부 0 이 나올 확률이 6 % 대다.
    _phi64 = np.linspace(0.151875, 0.485723, 64)
    _pz = float(np.prod(1.0 / (1.0 + np.exp(100.0 * (_phi64 - 0.48)))))
    chk('★5-b 참 문턱이 창 안이어도 all-zero 확률이 무시 못 할 크기',
        0.01 < _pz < 0.5, f'P(all zero) = {_pz:.4f}')

    # ── 6. 부호 역전 → φ_c 인용 안 함 (음성 경로) ──────────────────────────
    phr = np.array([0.20, 0.22, 0.24, 0.26, 0.34, 0.36, 0.38, 0.40])
    r6 = fit_curve(phr, np.array([1, 1, 1, 1, 0, 0, 0, 0]))
    chk('6 SIGN_REVERSED', r6['verdict'] == 'SIGN_REVERSED', str(r6['verdict']))
    chk('6 φ_c 없음', r6['phi_c'] is None)

    # ── 7. 미확정 두 극단 sensitivity (§4-4b) ──────────────────────────────
    #    갈리는 경우 — 미확정이 많고 문턱 근처에 몰려 있다
    p_ok = np.array([0.20, 0.22, 0.24, 0.40, 0.42, 0.44])
    y_ok = np.array([0, 0, 0, 1, 1, 1])
    p_un = np.array([0.28, 0.30, 0.32, 0.34])
    s7 = unresolved_sensitivity(p_ok, y_ok, p_un)
    chk('7 미확정 개수', s7['n_unresolved'] == 4, str(s7['n_unresolved']))
    chk('7 두 극단이 갈린다', s7['split'] is True, str(s7))
    #    안 갈리는 경우 — 미확정이 하나뿐이고 창 끝에 있다
    s7b = unresolved_sensitivity(phi, y, np.array([0.49]))
    chk('7b 하나면 안 갈린다', s7b['split'] is False, str(s7b['note']))
    #    미확정이 없으면 None
    chk('7c 미확정 없으면 None', unresolved_sensitivity(p_ok, y_ok, np.array([])) is None)

    # ── 8. 배치는 **따로** 적합한다 (§4-3) ─────────────────────────────────
    phi_b = np.concatenate([phi, rng.uniform(0.55, 0.85, 130)])
    y_b = np.concatenate([y, np.ones(130, dtype=int)])
    bt = np.array(['new'] * len(phi) + ['old'] * 130, dtype=object)
    un = np.zeros(len(y_b), dtype=bool)
    a8 = analyse(phi_b, y_b, bt, un)
    chk('8 곡선 둘', len(a8['curves']) == 2, str(len(a8['curves'])))
    chk('8 합친 적합 없음', a8['pooled'] is None)
    chk('8 old 는 NOT_IDENTIFIED',
        [c for c in a8['curves'] if c['label'] == 'old'][0]['verdict'] == 'NOT_IDENTIFIED')
    chk('8 교락 경고를 적는다', 'note' in a8 and '교락' in a8['note'])

    # ── 9. pooling 은 지시자 필수 ─────────────────────────────────────────
    a9 = analyse(phi_b, y_b, bt, un, pooled_sensitivity=True)
    chk('9 지시자 계수 있음', a9['pooled'] is not None and 'b_batch' in a9['pooled'])
    try:
        analyse(phi, y, np.array(['all'] * len(y), dtype=object),
                np.zeros(len(y), dtype=bool), pooled_sensitivity=True)
        chk('9b 한 배치 pooling 거부', False, '거부하지 않았다')
    except FitRefusal:
        chk('9b 한 배치 pooling 거부', True)

    # ── 10. 구간이 **프로파일 우도의 정의**를 만족한다 ─────────────────────
    #    ⚠ 초판은 "분리면 비대칭이어야 한다" 로 썼는데 **전제가 틀렸다** — 그 픽스처가
    #    0.30 대칭이라 프로파일도 진짜로 대칭이었다.  비대칭은 부수현상이지 정의가 아니다.
    #    정의는 하나다: 끝점에서 `2(l*_max − l*) = χ²₁,₀.₉₅`.
    X1 = np.column_stack([np.ones(len(phi)), phi])
    b1 = np.array([r1['firth']['a'], r1['firth']['b']])
    lmax1 = penalised_loglik(X1, y, b1)
    for side, edge in zip(('하단', '상단'), r1['ci95']):
        d = 2.0 * (lmax1 - _profile_at(X1, y, edge)[0])
        chk(f'10 {side} deviance = χ²', abs(d - CHI2_1DOF_95) < 1e-4, f'{d}')
    # 안쪽은 반드시 문턱보다 작다 (구간이 실제로 그 집합이다)
    mid = 0.5 * (r1['ci95'][0] + r1['ci95'][1])
    chk('10 안쪽은 문턱 아래',
        2.0 * (lmax1 - _profile_at(X1, y, mid)[0]) < CHI2_1DOF_95)
    #    비대칭은 **비대칭 설계**에서 확인한다 (Wald 로는 못 나오는 성질)
    pa = np.array([0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.24, 0.55, 0.90])
    ya = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1])
    ra = fit_curve(pa, ya)
    if ra['phi_c'] is not None and None not in ra['ci95']:
        left, right = ra['phi_c'] - ra['ci95'][0], ra['ci95'][1] - ra['phi_c']
        chk('10b 비대칭 설계 → 비대칭 구간', abs(left - right) > 1e-3, f'{left} vs {right}')
    else:
        chk('10b 비대칭 설계 → 비대칭 구간', True, '한쪽이 안 닫힘 = Wald 로는 못 내는 결과')

    # ── 11. 결정성 ────────────────────────────────────────────────────────
    chk('11 결정성', fit_curve(phi, y)['phi_c'] == r1['phi_c'])

    # ── 12. CSV 는 0/1 밖을 거부한다 (미확정은 열로 말해야 한다) ────────────
    import tempfile
    import os as _os
    with tempfile.TemporaryDirectory() as tmp:
        p = _os.path.join(tmp, 'x.csv')
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write('case,phi_AM,perc\na,0.3,0\nb,0.4,NA\n')
        try:
            load_csv(p, 'phi_AM', 'perc', None, None)
            chk('12 0/1 밖 거부', False, '거부하지 않았다')
        except FitRefusal:
            chk('12 0/1 밖 거부', True)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write('case,phi_AM,perc,unresolved\na,0.3,0,0\nb,0.4,,1\n')
        ph, yy, bb, uu = load_csv(p, 'phi_AM', 'perc', None, 'unresolved')
        chk('12b 미확정 열이면 통과', uu.tolist() == [False, True] and yy[1] == -1)

    # ── 12. 설계 원장 대조 — **실패행을 지우면 조용히 안 지나간다** (R14 P1-04) ──
    import hashlib as _hl, tempfile as _tf, os as _os, subprocess as _sp
    _d = _tf.mkdtemp(prefix='census_')
    _dz = _os.path.join(_d, 'design.csv')
    with open(_dz, 'w', newline='', encoding='utf-8') as fh:
        fh.write('id,phi_AM\n')
        for i in range(1, 9):
            fh.write(f'lhsx_{i:03d},{0.15 + 0.04 * i:.6f}\n')
    _sha = _hl.sha256(open(_dz, 'rb').read()).hexdigest()

    def _res(path, ids):
        with open(path, 'w', newline='', encoding='utf-8') as fh:
            fh.write('id,phi_AM,perc\n')
            for i in ids:
                fh.write(f'lhsx_{i:03d},{0.15 + 0.04 * i:.6f},{1 if i > 4 else 0}\n')
        return path

    _full = _res(_os.path.join(_d, 'full.csv'), range(1, 9))
    _drop = _res(_os.path.join(_d, 'drop.csv'), [1, 2, 3, 5, 6, 7])       # 4·8 을 지웠다
    _me = _os.path.abspath(__file__)

    def _run(*args):
        return _sp.run([sys.executable, _me, *args], capture_output=True, text=True)

    _r = _run('--csv', _full)
    chk('★12 --design 없으면 거부한다', _r.returncode == 2 and '우회' in _r.stderr,
        f'rc={_r.returncode}')
    _r = _run('--csv', _full, '--design', _dz, '--expect-sha256', _sha)
    chk('12 봉인 일치 + 전원 있으면 돈다', _r.returncode == 0, f'rc={_r.returncode}')
    chk('12 census 를 결과에 남긴다', '"design_census"' in _r.stdout)
    _r = _run('--csv', _full, '--design', _dz, '--expect-sha256', 'de' + 'ad' * 31)
    chk('★12 sha 불일치 거부', _r.returncode == 2 and 'sha256' in _r.stderr,
        f'rc={_r.returncode}')
    _r = _run('--csv', _drop, '--design', _dz, '--expect-sha256', _sha)
    chk('★12 실패행을 지워도 complete-case 로 안 흐른다 — 미확정 편입',
        _r.returncode == 0 and 'lhsx_004' in _r.stdout and 'lhsx_008' in _r.stdout,
        f'rc={_r.returncode}')
    chk('★12 편입된 미확정이 양극단 sensitivity 로 간다',
        'unresolved=0' in _r.stdout and 'unresolved=1' in _r.stdout)
    _ex = _res(_os.path.join(_d, 'extra.csv'), list(range(1, 9)) + [99])
    _r = _run('--csv', _ex, '--design', _dz, '--expect-sha256', _sha)
    chk('★12 설계에 없는 ID 거부', _r.returncode == 2 and '없는 ID' in _r.stderr,
        f'rc={_r.returncode}')

    print(f'lhs_perc_fit selftest: {ok}/{ok + len(bad)} PASS')
    for b in bad:
        print('  ✗', b)
    return 0 if not bad else 1


def main(argv=None):
    ap = argparse.ArgumentParser(
        description='퍼콜레이션 문턱 φ_c — Firth 벌점 로지스틱 (사전등록 v2 §4-2~4-4b)')
    ap.add_argument('--csv', help='case,phi_AM,perc[,batch][,unresolved]')
    ap.add_argument('--phi-col', default='phi_AM')
    ap.add_argument('--perc-col', default='perc')
    ap.add_argument('--batch-col', default=None,
                    help='주면 배치별로 **따로** 적합한다 (합치지 않는다 — 4-3)')
    ap.add_argument('--unresolved-col', default=None,
                    help='미확정 표시 열.  전부 0 / 전부 1 두 극단을 함께 낸다 (4-4b)')
    ap.add_argument('--pooled-sensitivity', action='store_true',
                    help='batch indicator 를 넣은 합친 적합 (4-3 b).  지시자 없는 pooling 은 거부')
    ap.add_argument('--design', help='봉인된 설계 CSV — 결과를 여기에 left join 한다 (R14 P1-04)')
    ap.add_argument('--expect-sha256', help='그 설계 CSV 의 기대 sha256 (강제 대조)')
    ap.add_argument('--id-col', default='id', help='결과·설계 양쪽의 ID 열 (기본 id)')
    ap.add_argument('--allow-no-design', action='store_true',
                    help='원장 대조 없이 돈다 — **진단 전용**, 보고에 쓰지 말 것')
    ap.add_argument('--out', help='결과 JSON 경로')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()
    if not a.csv:
        ap.error('--csv 가 필요하다')

    phi, y, batch, unres = load_csv(a.csv, a.phi_col, a.perc_col, a.batch_col, a.unresolved_col)

    #  ★★ 설계 원장 대조 (R14 P1-04).  기본이 **요구**다 — 없으면 거부한다.
    #     옛 판은 주어진 행만 읽어서, 실패한 런을 결과 CSV 에서 빼면 complete-case 적합이
    #     조용히 진행됐다.  이제 결과가 없는 설계 ID 는 **자동으로 미확정**이 되고,
    #     그 미확정은 §4-4b 양극단 sensitivity 로 흘러간다 — 등록한 그대로다.
    census = None
    if not a.design:
        if not a.allow_no_design:
            raise FitRefusal(
                '--design <봉인된 설계 CSV> 가 필요하다.  결과행만 읽으면 실패한 런을 '
                '빼는 것으로 사전등록을 우회할 수 있다 (R14 P1-04).  '
                '진단 목적이면 --allow-no-design.')
    else:
        rid = []
        with open(a.csv, newline='', encoding='utf-8-sig') as fh:
            for r in csv.DictReader(fh):
                if r and any((v or '').strip() for v in r.values()):
                    rid.append((r.get(a.id_col) or '').strip())
        if any(not v for v in rid):
            raise FitRefusal(f'결과 CSV 에 `{a.id_col}` 열이 비어 있는 행이 있다')
        census, refusals = design_census(a.design, a.expect_sha256, rid, id_col=a.id_col)
        if refusals:
            raise FitRefusal(' · '.join(refusals))
        add_phi, add_b = [], []
        for mid in census['missing']:
            drow = census['rows'][mid]
            if a.phi_col not in drow:
                raise FitRefusal(f'설계 CSV 에 `{a.phi_col}` 열이 없어 누락 ID 의 φ 를 못 넣는다')
            add_phi.append(float(drow[a.phi_col]))
            add_b.append(str(drow.get(a.batch_col, 'all')).strip()
                         if a.batch_col else 'all')
        if add_phi:
            phi = np.concatenate([phi, np.asarray(add_phi)])
            y = np.concatenate([y, -np.ones(len(add_phi), dtype=int)])
            batch = np.concatenate([batch, np.asarray(add_b, dtype=object)])
            unres = np.concatenate([unres, np.ones(len(add_phi), dtype=bool)])
        census.pop('rows', None)

    out = analyse(phi, y, batch, unres, pooled_sensitivity=a.pooled_sensitivity)
    if census is not None:
        out['design_census'] = census
        if census['missing']:
            out.setdefault('notes', []).append(
                f'결과가 없는 설계 ID {len(census["missing"])}개를 **미확정으로 편입**했다 '
                '(§4-4b 양극단 sensitivity 로 흘러간다)')
    else:
        out['design_census'] = {'skipped': '--allow-no-design (진단 전용)'}
    txt = json.dumps(out, ensure_ascii=False, indent=2, sort_keys=True)
    print(txt)
    if a.out:
        with open(a.out, 'w', encoding='utf-8') as fh:
            fh.write(txt + '\n')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except FitRefusal as exc:
        print(f'⛔ 거부: {exc}', file=sys.stderr)
        sys.exit(2)

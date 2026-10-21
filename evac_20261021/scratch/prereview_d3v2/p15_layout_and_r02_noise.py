#!/usr/bin/env python3
"""PRE-D3V2 탐침 15 — (a) v2 기본 시드 배치 그대로의 포괄 · (b) R02 보장 문장 (잡음이 있는 칸 끝값) 의 해석 반례.

(a) C04 의 몬테카를로 (포괄 0.998 · 통계 띠만 0.977) 는 '8 수준 모두 2 시드 · ν 8' 이다.  v2 기본 배치 (§3-3) =
    T2 8 수준 × A + 4 수준 (0.6718 · 6.718 · 67.18 · 637.3) × B → ν = 4 · 1 시드 수준 u = s_pool.  같은 [가정 예시]
    (참 곡선 40 + 5x · σ_seed 1.5° · u_exp 0.3°) 로 그 배치의 포괄을 잰다.  + T1 탭 4 수준 × 2 시드 (1 decade 칸).
(b) R02 보장 (v2 §3-7): "칸 안에서 참 곡선이 단조이고 통계 오차가 띠 안이면 그 시험의 집합은 참 Bo 를 포함한다".
    손 계산: 칸 [x_k, x_k+1] 에서 참 곡선이 x_k 바로 뒤에서 35 → 48.9 로 뛰고 참 x* 가 그 직후 · DEM 끝값 오차 e_k = 0 ·
    e_k+1 = −2.7 (= 0.9 × 2u · u 1.5) · 측정 오차 e_m = +0.54 (= 0.9 × 2u_exp · u_exp 0.3).  x* 에서의 통계 오차 |e_m − e_L(x*)| = 0.54
    ≤ 띠 3.06 (전제 성립) 인데, 띠의 |ΔI| 가 잡음 낀 추정 (11.2 < 참 13.9) 이라 |L(x*) − m| = 14.44 > 3.06 + 11.2 = 14.26 → 놓친다.
    (확률은 작다 — 한쪽 ≈ 2 %; 결함은 '전제 ⇒ 포함' 이라는 결정론 문장.)

재실행: python3 -I p15_layout_and_r02_noise.py   (가볍다 — 수 초)
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

c = pcommon.load_checks()
R2 = c.RulesV2()
X = c.X
rng = random.Random(15)
out = {}


def coverage(levels_x, two_seed_idx, trials=4000, sig=1.5, uexp=0.3, slope=5.0, x_lo=None, x_hi=None):
    cov = cov_stat = 0
    nus = set()
    for _ in range(trials):
        seeds = [[40.0 + slope * x + rng.gauss(0, sig)] + ([40.0 + slope * x + rng.gauss(0, sig)] if i in two_seed_idx else [])
                 for i, x in enumerate(levels_x)]
        u, how = R2.u_dem(seeds)
        nu = sum(len(v) - 1 for v in seeds if len(v) >= 2)
        nus.add(nu)
        I = [sum(v) / len(v) for v in seeds]
        lo = levels_x[1] if x_lo is None else x_lo
        hi = levels_x[-2] if x_hi is None else x_hi
        xt = lo + (hi - lo) * rng.random()
        mm = 40.0 + slope * xt + rng.gauss(0, uexp)
        A = R2.accept(levels_x, I, u, mm, uexp, nu=nu)
        B = R2.accept_stat_only(levels_x, I, u, mm, uexp, nu=nu)
        cov += A is not None and c.inside(xt, A['comps'])
        cov_stat += B is not None and c.inside(xt, B['comps'])
    return dict(coverage=cov / trials, coverage_stat_only=cov_stat / trials, nu=sorted(nus))


out['C04_as_checked_8x2'] = coverage(X, set(range(8)))
out['v2_default_T2_8A_plus_4B'] = coverage(X, {1, 3, 5, 7})
X1 = [X[k] for k in (1, 3, 5, 7)]
out['v2_default_T1_tap_4x2'] = coverage(X1, {0, 1, 2, 3}, slope=5.0)

# (b) R02 결정론 반례 — 참 곡선 f 는 엄격 증가 (참 x* 하나):
#     칸 k 안에서 x_k → x_k + 0.002 decade 동안 35 → 48.85 · 그 뒤 칸 끝까지 48.85 → 48.9 · 칸 밖은 기울기 0.01 °/decade
k = 2
xa, xb = X[k], X[k + 1]


def f(x):
    if x <= xa:
        return 35.0 - 0.01 * (xa - x)
    if x >= xb:
        return 48.9 + 0.01 * (x - xb)
    if x <= xa + 0.002:
        return 35.0 + 13.85 * (x - xa) / 0.002
    return 48.85 + 0.05 * (x - xa - 0.002) / (xb - xa - 0.002)


e_k, e_k1, e_m = 0.0, -0.9 * 2 * 1.5, 0.9 * 2 * 0.3
I_est = [f(x) for x in X]
I_est[k] += e_k
I_est[k + 1] += e_k1
xstar = xa + 0.002                       # f(x*) = 48.85 (유일)
mm = f(xstar) + e_m
A = R2.accept(X, I_est, [1.5] * len(X), mm, 0.3, nu=None)
t = (xstar - xa) / (xb - xa)
L = I_est[k] + t * (I_est[k + 1] - I_est[k])
band_stat = ((2 * 0.3) ** 2 + (2 * 1.5) ** 2) ** 0.5
out['R02_noise_counterexample'] = dict(
    cell=(xa, xb), x_star=xstar, measured=mm, I_est_cell=(I_est[k], I_est[k + 1]),
    stat_error_at_xstar=abs(e_m - e_k), band_stat=band_stat, premise_holds=abs(e_m - e_k) <= band_stat,
    L_at_xstar=L, abs_L_minus_m=abs(L - mm), band_total=band_stat + abs(I_est[k + 1] - I_est[k]),
    accepted_comps=A['comps'], x_star_covered=c.inside(xstar, A['comps']))
pcommon.dump('p15_layout_and_r02_noise.json', out)
for kk, v in out.items():
    print(kk, v)

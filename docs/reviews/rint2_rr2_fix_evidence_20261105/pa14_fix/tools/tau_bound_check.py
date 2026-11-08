"""P3-d 위 한계 근거 점검 — 생산 판정 `step3_conv_cert.target_judge` (read_run 이 다시 부르는 같은 함수) 가 ⓓ 통과 (pass_d True) 를 낸 해의 float 보장 오차
target_err_bound_rel ≤ τ (= CERT_TARGET_TOL) 인가.  칼날 (정확 분수로 τ·G 바로 안 · 바로 밖의 lo · hi) + 무작위 (자릿수 10^-30 … 10^30).
쓰임: python3 tau_bound_check.py <scripts 뿌리> [표본 수 (기본 200000)] [씨앗 (기본 14)]"""
import math
import random
import sys
from fractions import Fraction

sys.path.insert(0, sys.argv[1])
import step3_conv_cert as CC  # noqa: E402

N = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
rng = random.Random(int(sys.argv[3]) if len(sys.argv) > 3 else 14)
tau = CC.CERT_TARGET_TOL
T = Fraction(repr(float(tau)))


def nxt(x, d):
    return math.nextafter(x, math.inf if d > 0 else -math.inf) if hasattr(math, 'nextafter') else None


def edge(G, side):
    """정확 분수 τ·G 칼날의 float (side −1 = lo 쪽 · +1 = hi 쪽) — 칼날에 가장 가까운 float 과 그 이웃 둘."""
    FG = Fraction(G)
    t = FG - T * FG if side < 0 else FG + T * FG
    x = float(t)
    return [x, nxt(x, -1), nxt(x, +1)]


n_pass = n_edge_pass = n_bad = 0
worst = 0.0
bad = []
for i in range(N):
    G = math.ldexp(rng.uniform(0.5, 1.0), rng.randint(-100, 100))
    if i % 2 == 0:
        lo_c, hi_c = edge(G, -1), edge(G, +1)
        pairs = [(lo, G) for lo in lo_c] + [(G, hi) for hi in hi_c] + [(lo, hi) for lo in lo_c for hi in hi_c]
    else:
        w = rng.uniform(0.0, 1.2) * tau
        u = rng.uniform(0.0, 1.0)
        pairs = [(G * (1.0 - u * w), G * (1.0 + (1.0 - u) * w))]
    for lo, hi in pairs:
        jd = CC.target_judge(lo, hi, G)
        if jd.get('pass_d') is not True:
            continue
        n_pass += 1
        e = jd['target_err_bound_rel']
        worst = max(worst, e)
        if i % 2 == 0:
            n_edge_pass += 1
        if not (isinstance(e, float) and 0.0 <= e <= tau):
            n_bad += 1
            if len(bad) < 5:
                bad.append((lo, hi, G, e))
print(f'τ = {tau!r} · 표본 G {N} · ⓓ 통과 {n_pass} (칼날 {n_edge_pass}) · e > τ (또는 음수 · float 아님) {n_bad} · 최대 e = {worst!r} · 최대 e == τ {worst == tau}')
print('어긋남 예:', bad)
sys.exit(1 if n_bad else 0)

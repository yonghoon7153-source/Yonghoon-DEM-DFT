import sys
sys.path.insert(0, sys.argv[1])
import time_budget_v3 as T
K, G = T.KGY, T.GAB['gpu146']
def hi_h(r, mode):
    return T.f1_two(K, G, 1, s=1.0, r=r, m=1.0, r_mode=mode)['sim_s'] / 3600
for mode in ('arm', 'solve'):
    lo, hi = 1.0, 20.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if hi_h(mid, mode) <= 384.0: lo = mid
        else: hi = mid
    print(mode, 'r_boundary_1205 =', round(lo, 3), ' check hi(h) =', round(hi_h(lo, mode), 2))
    lo, hi = 1.0, 20.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if hi_h(mid, mode) <= 264.0: lo = mid
        else: hi = mid
    print(mode, 'r_boundary_1130 =', round(lo, 3))

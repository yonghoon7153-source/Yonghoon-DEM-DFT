# (11-17 반입 때 본 세션이 두 줄 더함) 인자 = time_budget_v3.py 가 든 폴더 (예: ../work) · 나머지 = 리뷰 조수 글 그대로
import sys
sys.path.insert(0, sys.argv[1])
import time_budget_v3 as T
K, G = T.KGY, T.GAB['gpu146']
def h(x): return round(x/3600, 1)
for r in (2.933, 3.42, 4.34, 5.866, 8.68):
    for mode in ('arm', 'solve'):
        lo = T.f1_two(K, G, 0, s=1.0, r=r, m=1.0, r_mode=mode); hi = T.f1_two(K, G, 1, s=1.0, r=r, m=1.0, r_mode=mode)
        st = T.stage_table(K, G, s=1.0, r=r, m=1.0, r_mode=mode)
        print(f"r {r:5.3f} {mode:5s} GPU end {h(lo['sim_s'])}-{h(hi['sim_s'])} h split {hi['n_kgy']}/{hi['n_gabia']}  slack1205 {round(384-hi['sim_s']/3600,1)}  point8 kgy {st['kgy']['point_first_8_arms_h']} gabia {st['gabia']['point_first_8_arms_h']}  unit_first kgy {st['kgy']['unit_first_hi_h']} gabia {st['gabia']['unit_first_hi_h']} merge12 {st['kgy']['merge_12_graph_only_h']}")
# largest r covered by 168 h for gabia first point (arm / solve), m=1
import math
for mode in ('arm','solve'):
    for M in (K, G):
        lo, hi_ = 0.5, 30.0
        for _ in range(60):
            mid = (lo+hi_)/2
            c = T.comp(M, s=1.0, r=mid, m=1.0, r_mode=mode)
            t = 8*c['arm_d'] + T.ORIGIN8_NEW*c['build_d']
            if t <= 168*3600: lo = mid
            else: hi_ = mid
        print(mode, M['name'], 'max r for point8 <=168h:', round(lo,2))
# iteration multiplier covered by maxiter 5M vs time cap: per-arm with GPU x (=r*m) at solve mode (prep=SBE)
for M in (K, G):
    c1 = T.comp(M, s=1.0, r=1.0, m=1.0, r_mode='solve')
    for x in (12.0, 17.35, 17.99):
        arm = c1['prep_s'] + x*(T.GPU*M['g']) + x*T.CERT_CPU*M['c']
        t = 8*arm + T.ORIGIN8_NEW*T.BUILD_EXTRA*M['c']
        print(M['name'], 'x', x, 'point8 (solve mode, converged just under cap) =', h(t), 'h')

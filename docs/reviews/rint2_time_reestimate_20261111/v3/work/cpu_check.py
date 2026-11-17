import sys, copy
sys.path.insert(0, sys.argv[1])
import time_budget_v3 as T
K = T.KGY; G = copy.deepcopy(T.GAB['gpu146']); G['c'] = 3.50/2.40
for mode in ('arm','solve'):
    lo = T.f1_two(K, G, 0, s=1.0, r=2.933, m=1.0, r_mode=mode); hi = T.f1_two(K, G, 1, s=1.0, r=2.933, m=1.0, r_mode=mode)
    st = T.stage_table(K, G, s=1.0, r=2.933, m=1.0, r_mode=mode)
    print(mode, round(lo['sim_s']/3600,1), round(hi['sim_s']/3600,1), 'split', hi['n_kgy'], hi['n_gabia'], 'gabia point8', st['gabia']['point_first_8_arms_h'])

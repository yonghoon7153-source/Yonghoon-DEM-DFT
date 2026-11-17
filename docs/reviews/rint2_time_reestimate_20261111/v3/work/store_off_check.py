#!/usr/bin/env python3
# 저장본 끔 (C 꼴만) 꼴 — time_budget_v3 의 함수를 READ/BUILD_EXTRA 만 바꿔 다시 부른다 (읽기만 · 화면)
import importlib.util, sys, datetime
spec = importlib.util.spec_from_file_location('tb3', sys.argv[1]); tb = importlib.util.module_from_spec(spec); spec.loader.exec_module(tb)
def run(label):
    for mode in ('arm', 'solve'):
        lo = tb.f1_two(tb.KGY, tb.GAB['gpu146'], 0, s=1.0, r=tb.REG_RATIO, r_mode=mode)
        hi = tb.f1_two(tb.KGY, tb.GAB['gpu146'], 1, s=1.0, r=tb.REG_RATIO, r_mode=mode)
        print(label, mode, 'sim_h', tb.h(lo['sim_s']), tb.h(hi['sim_s']), 'split', lo['n_kgy'], hi['n_kgy'], 'ladder_gabia_h', tb.h(lo['ladder_gabia_s']))
run('store_on ')
tb.READ, tb.BUILD_EXTRA = tb.CJ_NOSTORE, 0
run('store_off')
for d in ('2026-11-17','2026-11-20','2026-11-27','2026-11-28','2026-12-01','2026-12-05','2026-12-06'):
    print(d, datetime.date.fromisoformat(d).strftime('%a'))

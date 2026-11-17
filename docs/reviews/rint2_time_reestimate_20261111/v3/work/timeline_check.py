#!/usr/bin/env python3
import importlib.util, sys
spec = importlib.util.spec_from_file_location('tb3', sys.argv[1]); tb = importlib.util.module_from_spec(spec); spec.loader.exec_module(tb)
for mode in ('arm', 'solve'):
    for s in (1.0, 2.0):
        ck = tb.comp(tb.KGY, s=s, r_mode=mode); cg = tb.comp(tb.GAB['gpu146'], s=s, r_mode=mode)
        first5_k = 5 * ck['arm_s'] + ck['build_s']; first5_g = 5 * cg['arm_s'] + cg['build_s']
        lad = max(tb.ladder(tb.KGY, s=s, r_mode=mode), tb.ladder(tb.GAB['gpu146'], s=s, r_mode=mode))
        corner_k = ck['prep_d'] + ck['build_d'] + 2 * ck['cold_d']
        print(mode, 's', s, 'first5 kgy/gabia h', tb.h(first5_k), tb.h(first5_g), 'ladders_done h', tb.h(lad),
              'first DBE corner (kgy) done h', tb.h(lad + corner_k), 'corner arm h', tb.h(corner_k))
# 한 점 (사다리 점) 더함
print('ladder point add kgy/gabia h', tb.h(tb.comp(tb.KGY)['arm_s']), tb.h(tb.comp(tb.GAB['gpu146'])['arm_s']))
# 다른 부하 (gpu_util) 평균 — 우리 풀이 전 구간
for p in sys.argv[2:]:
    rows=[l.rstrip('\n').split('\t') for l in open(p) if not l.startswith('#') and l.strip()]
    gu=[int(r[7]) for r in rows if r[7] not in ('NA','')]
    print(p.split('/')[-2], 'rows', len(rows))

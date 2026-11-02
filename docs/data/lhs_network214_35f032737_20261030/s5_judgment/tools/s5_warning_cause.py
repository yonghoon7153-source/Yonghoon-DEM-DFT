#!/usr/bin/env python3
"""warning_count +1 의 원인 가설 검사 — webapp/app.py 의 'physics_hertzian_divergence' (|σ_P/σ_H − 1| > 0.5 · 3563–3570 줄) 경고가
B7 에서만 켜진 행 = warning_count 가 +1 된 행인가 (두 배치 metrics_flat 의 sigma_full_mScm · sigma_full_mScm_physics 로 · 읽기 전용).
사용: python3 -I s5_warning_cause.py --repo <리포> --root194 <풀어 둔 B7 194 뿌리>
"""
import argparse
import csv
import json
import os

ap = argparse.ArgumentParser()
ap.add_argument('--repo', required=True)
ap.add_argument('--root194', required=True)
a = ap.parse_args()
OLD = os.path.join(a.repo, 'docs', 'data', 'lhs_network194_11fcf91e8', 'merged')


def read(p):
    with open(p, encoding='utf-8', newline='') as f:
        return {r['case']: r for r in csv.DictReader(f)}


def fl(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


def div(r):
    h, p = fl(r.get('sigma_full_mScm')), fl(r.get('sigma_full_mScm_physics'))
    return bool(h and p and h > 0 and abs(p - h) / h > 0.5)


res = {}
for ds in ('lhs', 'lhsx'):
    n, o = read(os.path.join(a.root194, 'merged', ds, 'metrics_flat.csv')), read(os.path.join(OLD, ds, 'metrics_flat.csv'))
    agree = disagree = 0
    bad = []
    for k in sorted(n):
        dw = int(n[k]['warning_count']) - int(o[k]['warning_count'])
        pred = int(div(n[k])) - int(div(o[k]))
        if dw == pred:
            agree += 1
        else:
            disagree += 1
            bad.append((k, dw, pred, n[k].get('sigma_full_mScm'), n[k].get('sigma_full_mScm_physics'), o[k].get('sigma_full_mScm_physics')))
    res[ds] = dict(n=len(n), agree=agree, disagree=disagree, first_disagree=bad[:8],
                   dw_counts={str(v): sum(1 for k in n if int(n[k]['warning_count']) - int(o[k]['warning_count']) == v) for v in (-1, 0, 1, 2)})
print(json.dumps(res, ensure_ascii=False, indent=1))

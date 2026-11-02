#!/usr/bin/env python3
"""회귀 세부 — (1) B7 에만 있는 열의 분류 (선언된 변경 범주) · (2) H0 σ (이온 · 전자 · 열) 차의 부호 · 분위 (읽기 전용).
사용: python3 -I s5_reg_detail.py --repo <리포> --root194 <풀어 둔 B7 194 뿌리>
"""
import argparse
import csv
import json
import math
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
        x = float(s)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def cat(c):
    if 'physics_union' in c:
        return 'C2-⑥ 피복 합집합 cap 새 키'
    if c in ('electrode_model', 'bulk_model', 'area_rule_physics', 'psi_placement_physics') or c.endswith('.psi_placement'):
        return '세대 2 표기 (전극 · bulk · 면적 규칙 · ψ 배치)'
    if ('electronic_sigma_full_' in c or 'thermal_sigma_full_' in c) and (c.endswith('_status') or c.endswith('_reason')
                                                                          or c.endswith('_status_physics') or c.endswith('_reason_physics')):
        return 'L214 전자 · 열 FULL 상태 · 사유 기록 키 (값 칸 아님)'
    return '분류 밖'


def q(v, p):
    v = sorted(v)
    return v[min(len(v) - 1, int(p * (len(v) - 1) + 0.5))] if v else None


res = {}
for ds in ('lhs', 'lhsx'):
    n, o = read(os.path.join(a.root194, 'merged', ds, 'metrics_flat.csv')), read(os.path.join(OLD, ds, 'metrics_flat.csv'))
    only_new = sorted(set(next(iter(n.values()))) - set(next(iter(o.values()))))
    cats = {}
    for c in only_new:
        cats.setdefault(cat(c), []).append(c)
    D = res[ds] = {'only_new_by_category': {k: len(v) for k, v in cats.items()}, 'unclassified': cats.get('분류 밖', [])}
    for col in ('sigma_full', 'electronic_sigma_full_mScm', 'thermal_sigma_full_mScm'):
        rel, pos, neg = [], 0, 0
        for k in n:
            x, y = fl(n[k].get(col)), fl(o[k].get(col))
            if x is None or y is None or max(abs(x), abs(y)) == 0:
                continue
            r = (x - y) / max(abs(x), abs(y))          # 상대 차 = |B7 − v1.2| / max(|B7|, |v1.2|) — 다른 두 대조 스크립트와 같은 정의
            rel.append(abs(r))
            pos += r > 0
            neg += r < 0
        D[col] = dict(n=len(rel), b7_gt_v12=pos, b7_lt_v12=neg, p50=q(rel, .5), p90=q(rel, .9), max=max(rel) if rel else None,
                      note=('metrics_flat 글자 = 유효숫자 4 자리 (예 6.554e-05) — 상대 해상도 ~1e-4 · 이온은 배포값 (17 자리) 대조가 정본' if col == 'sigma_full' else ''))
print(json.dumps(res, ensure_ascii=False, indent=1))

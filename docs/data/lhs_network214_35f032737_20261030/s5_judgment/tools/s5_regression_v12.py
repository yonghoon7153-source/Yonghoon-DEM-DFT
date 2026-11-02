#!/usr/bin/env python3
"""등록 §5-7 회귀 — B7 배치 metrics_flat (194) ↔ v1.2 배치 metrics_flat (11fcf91e8 · 커밋된 기록) — **레코드 수준** 대조 (읽기 전용).

  망 단계 열 = webapp/pipeline_service.NET_MERGE_KEYS (+ 펼친 자식 '<키>.…') ∪ network_dual.* ∪ 채널 판정 · 사유 ∪ 솔버 상태 · 실행 id ·
               physics_resistance_model (리포 정의 — 손 목록 아님)
  망 단계 밖 열 = 나머지 공통 열 → 등록 §5-7 "같은 값" (글자 같음 · 아니면 수치 같음 · 다르면 그대로 보고)
  H0 σ (선언된 다름 = 전극 정확 Dirichlet · σ 상대 ≤ 1.5e-4 · 등록 §5-7) = sigma_full · electronic_sigma_full_mScm · thermal_sigma_full_mScm
     (hertz 최상위 = legacy = dual hertzian 사본) — 두 쪽 다 숫자일 때만 상대 차 · 한쪽 빈칸은 따로 센다

사용: python3 -I s5_regression_v12.py --repo <리포> --root194 <풀어 둔 B7 194 뿌리> --out <폴더>
"""
import argparse
import collections
import csv
import json
import math
import os
import sys

ap = argparse.ArgumentParser()
ap.add_argument('--repo', required=True)
ap.add_argument('--root194', required=True)
ap.add_argument('--out', required=True)
a = ap.parse_args()
sys.path.insert(0, os.path.join(a.repo, 'webapp'))
import pipeline_service as PS  # noqa: E402

OLD = os.path.join(a.repo, 'docs', 'data', 'lhs_network194_11fcf91e8', 'merged')
NET = set(PS.NET_MERGE_KEYS)
EXTRA_NET = {'network_solver_status', 'failed_channels', 'network_run_id', 'active_network_run_id', 'physics_resistance_model'}


def is_net(c):
    base = c.split('.', 1)[0]
    return (c in NET or base in NET or c.startswith('network_dual.') or c in EXTRA_NET
            or c.endswith('_channel_verdict') or c.endswith('_channel_reason'))


def read(p):
    with open(p, encoding='utf-8', newline='') as f:
        return {r['case']: r for r in csv.DictReader(f)}


def num(s):
    try:
        x = float(s)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


res = {'schema': 's5_regression_v12/v1', 'datasets': {}}
diff_rows = []
for ds in ('lhs', 'lhsx'):
    new = read(os.path.join(a.root194, 'merged', ds, 'metrics_flat.csv'))
    old = read(os.path.join(OLD, ds, 'metrics_flat.csv'))
    cn, co = set(next(iter(new.values()))), set(next(iter(old.values())))
    common = sorted(cn & co)
    D = res['datasets'][ds] = dict(n_new=len(new), n_old=len(old), same_case_set=(set(new) == set(old)),
                                   cols_new=len(cn), cols_old=len(co), cols_common=len(common),
                                   cols_only_new=sorted(cn - co), cols_only_old=sorted(co - cn))
    nonnet = [c for c in common if not is_net(c) and c != 'case']
    net = [c for c in common if is_net(c)]
    D['n_nonnet_cols'], D['n_net_cols'] = len(nonnet), len(net)
    eq_text = eq_num = 0
    dcols = collections.Counter()
    for k in sorted(set(new) & set(old)):
        for c in nonnet:
            x, y = new[k].get(c, ''), old[k].get(c, '')
            if x == y:
                eq_text += 1
                continue
            nx, ny = num(x), num(y)
            if nx is not None and ny is not None and nx == ny:
                eq_num += 1
                continue
            dcols[c] += 1
            rel = (abs(nx - ny) / max(abs(nx), abs(ny))) if (nx is not None and ny is not None and max(abs(nx), abs(ny)) > 0) else None
            diff_rows.append(dict(dataset=ds, case=k, column=c, b7=x, v12=y, rel=rel))
    D['nonnet_cells'] = len(set(new) & set(old)) * len(nonnet)
    D['nonnet_equal_text'], D['nonnet_equal_numeric'] = eq_text, eq_num
    D['nonnet_diff_cols'] = dict(dcols.most_common())
    # H0 σ (hertz 최상위 열) — 선언된 다름 (≤ 1.5e-4)
    h0 = {}
    for c in ('sigma_full', 'electronic_sigma_full_mScm', 'thermal_sigma_full_mScm'):
        rels, blank_new, blank_old, zero_both = [], [], [], 0
        for k in sorted(set(new) & set(old)):
            nx, ny = num(new[k].get(c, '')), num(old[k].get(c, ''))
            if nx is None or ny is None:
                (blank_new if nx is None else blank_old).append(k)
                continue
            if nx == 0 and ny == 0:
                zero_both += 1
                continue
            rels.append((abs(nx - ny) / max(abs(nx), abs(ny)), k))
        rels.sort(reverse=True)
        h0[c] = dict(n_compared=len(rels), zero_both=zero_both, blank_new=blank_new[:10], n_blank_new=len(blank_new),
                     blank_old=blank_old[:10], n_blank_old=len(blank_old), max_rel=(rels[0] if rels else None),
                     n_over_1p5e4=sum(1 for r, _ in rels if r > 1.5e-4), median_rel=(rels[len(rels) // 2][0] if rels else None))
    D['h0_sigma'] = h0
    D['net_cols_examples'] = net[:80]

os.makedirs(a.out, exist_ok=True)
with open(os.path.join(a.out, 'regression_v12_summary.json'), 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
with open(os.path.join(a.out, 'regression_v12_nonnet_diffs.tsv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['dataset', 'case', 'column', 'b7', 'v12', 'rel'], delimiter='\t', lineterminator='\n')
    w.writeheader()
    for r in diff_rows:
        w.writerow(r)
print(json.dumps({ds: {k: v for k, v in d.items() if k not in ('net_cols_examples',)} for ds, d in res['datasets'].items()}, ensure_ascii=False, indent=1)[:9000])

#!/usr/bin/env python3
"""H0 이온 배포값 회귀 — v1.2 배포 (커밋 · docs/data/lhs_release_20261006_v12) 의 f_ion_hertz · tau2_ion_hertz · 상태 ↔
B7 다시 읽기 기록 (reread.json) 의 row_cells (load_tau_results 칸 = v1.3 인계표에 실릴 τ 칸) — 등록 §5-7 선언된 다름 '전극 정확 Dirichlet
(H0 σ 상대 ≤ 1.5e-4 · 설계 기록 §1 "배포값 변화 ≤ 1.5e-4")' 대조 (읽기 전용).  + metrics_flat sigma_full (두 배치) 의 원 글자.
사용: python3 -I s5_tau_vs_v12.py --repo <리포> --root194 <풀어 둔 B7 194 뿌리> --out <폴더>
"""
import argparse
import csv
import json
import math
import os

ap = argparse.ArgumentParser()
ap.add_argument('--repo', required=True)
ap.add_argument('--root194', required=True)
ap.add_argument('--out', required=True)
a = ap.parse_args()
REL = os.path.join(a.repo, 'docs', 'data', 'lhs_release_20261006_v12')
rr = json.load(open(os.path.join(a.root194, 'reread.json'), encoding='utf-8'))
cells = {c['case']: (c['cohort'], c['row_cells']) for c in rr['cases']}


def f(s):
    try:
        x = float(s)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def read_csv(p, key):
    with open(p, encoding='utf-8', newline='') as fh:
        return {r[key]: r for r in csv.DictReader(fh)}


out = {'schema': 's5_tau_vs_v12/v1', 'datasets': {}}
rows_out = []
for ds in ('lhs', 'lhsx'):
    v12 = read_csv(os.path.join(REL, f'{ds}_release_20261006_v12.csv'), 'case_id')
    D = out['datasets'][ds] = {'n_v12': len(v12), 'n_b7': sum(1 for c in cells.values() if c[0] == ds)}
    st_pairs, rels, rels_t2, blank = {}, [], [], []
    for k, r in sorted(v12.items()):
        coh, rc = cells.get(k, (None, None))
        if rc is None:
            blank.append(k)
            continue
        sp = (r.get('ion_net_status_hertz', ''), rc.get('ion_net_status_hertz', ''))
        st_pairs[sp] = st_pairs.get(sp, 0) + 1
        x, y = f(rc.get('f_ion_hertz')), f(r.get('f_ion_hertz'))
        if x is not None and y is not None and max(abs(x), abs(y)) > 0:
            rels.append((abs(x - y) / max(abs(x), abs(y)), k, rc.get('f_ion_hertz'), r.get('f_ion_hertz')))
        elif x is not None and y is not None:
            pass
        x2, y2 = f(rc.get('tau2_ion_hertz')), f(r.get('tau2_ion_hertz'))
        if x2 is not None and y2 is not None and max(abs(x2), abs(y2)) > 0:
            rels_t2.append((abs(x2 - y2) / max(abs(x2), abs(y2)), k))
        rows_out.append(dict(dataset=ds, case_id=k, status_v12=sp[0], status_b7=sp[1], f_v12=r.get('f_ion_hertz', ''), f_b7=rc.get('f_ion_hertz', ''),
                             rel=(rels[-1][0] if rels and rels[-1][1] == k else '')))
    rels.sort(reverse=True)
    rels_t2.sort(reverse=True)
    D['status_pairs_v12_to_b7'] = {f'{a_}→{b_}': n for (a_, b_), n in sorted(st_pairs.items())}
    D['f_n_compared'] = len(rels)
    D['f_max_rel'] = rels[:5]
    D['f_n_over_1p5e4'] = sum(1 for r in rels if r[0] > 1.5e-4)
    D['f_median_rel'] = rels[len(rels) // 2][0] if rels else None
    D['tau2_max_rel'] = rels_t2[:3]
    D['missing_in_b7'] = blank
    # f_ion_hertz 글자 자릿수 (반올림 해상도)
    D['f_v12_text_examples'] = [v12[k]['f_ion_hertz'] for k in list(v12)[:3]]
    D['f_b7_text_examples'] = [cells[k][1]['f_ion_hertz'] for k in list(v12)[:3]]
# metrics_flat 원 글자 — 최대 차 케이스
mfo = read_csv(os.path.join(a.repo, 'docs', 'data', 'lhs_network194_11fcf91e8', 'merged', 'lhs', 'metrics_flat.csv'), 'case')
mfn = read_csv(os.path.join(a.root194, 'merged', 'lhs', 'metrics_flat.csv'), 'case')
out['lhs00_123_metrics_flat'] = {c: (mfn['lhs00_123'].get(c), mfo['lhs00_123'].get(c)) for c in
                                 ('sigma_full', 'sigma_full_mScm', 'sigma_ratio', 'electrode_model', 'network_dual.hertzian.sigma_full')}
os.makedirs(a.out, exist_ok=True)
json.dump(out, open(os.path.join(a.out, 'tau_vs_v12_summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1)[:6000])

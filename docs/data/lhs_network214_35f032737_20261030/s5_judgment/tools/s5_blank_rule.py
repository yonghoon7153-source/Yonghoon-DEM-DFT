#!/usr/bin/env python3
"""§9-8 ④ 공란 의미 · ③ 값 유지 규칙을 다시 읽기 칸 (row_cells) 에서 확인 + lhsx sigma_full_reason_physics 값 (읽기 전용).
  ④ 모형 한계 (NOT_COMPUTED · 사유 정확히 full_over_conduction) 모드 = f · f_gap · tau2 · tau 빈칸 · 표지 True
  MODEL_BELOW_CONTINUUM_BOUND 모드 = 값 유지 (f · tau2 숫자) · NOT_PERCOLATING = f 0.0 · tau2 · tau 빈칸 (∞ 저장 표현)
사용: python3 -I s5_blank_rule.py --root194 <뿌리> --rootsupp <뿌리>
"""
import argparse
import collections
import csv
import json
import os

ap = argparse.ArgumentParser()
ap.add_argument('--root194', required=True)
ap.add_argument('--rootsupp', required=True)
a = ap.parse_args()
MODES = ('hertz', 'physics', 'hertz_h12')
VALS = ('f_ion_{m}', 'f_ion_{m}_gap', 'tau2_ion_{m}', 'tau_ion_{m}')
viol = []
pat = collections.Counter()
for root in (a.root194, a.rootsupp):
    rr = json.load(open(os.path.join(root, 'reread.json'), encoding='utf-8'))
    for c in rr['cases']:
        r = c['row_cells']
        for m in MODES:
            st, why = r.get(f'ion_net_status_{m}', ''), r.get(f'ion_net_status_reason_{m}', '')
            blanks = tuple(r.get(v.format(m=m), '') == '' for v in VALS)
            pat[(m, st, why, blanks)] += 1
            if st == 'NOT_COMPUTED' and why == 'full_over_conduction' and not all(blanks):
                viol.append((c['case'], m, '모형 한계인데 값 칸이 있다'))
            if st == 'MODEL_BELOW_CONTINUUM_BOUND' and any(blanks[:3]):
                viol.append((c['case'], m, 'MBCB 인데 값 칸 빈칸'))
            if st == 'NOT_PERCOLATING' and (r.get(f'f_ion_{m}') not in ('0.0', '0') or not blanks[2] or not blanks[3]):
                viol.append((c['case'], m, '비관통 저장 표현 다름'))
            if st == 'OK' and any(blanks):
                viol.append((c['case'], m, 'OK 인데 값 칸 빈칸'))
            flag = r.get(f'full_model_limit_{m}') if m != 'hertz_h12' else None
            if flag is not None and (flag == 'True') != (st == 'NOT_COMPUTED' and why == 'full_over_conduction'):
                viol.append((c['case'], m, f'표지 {flag} ↔ 상태 {st}/{why}'))
print('규칙 위반', len(viol), viol[:10])
for k, v in sorted(pat.items(), key=str):
    print(' ', v, k[0], k[1], repr(k[2]), '값 칸 빈칸 (f · f_gap · tau2 · tau) =', k[3])
with open(os.path.join(a.root194, 'merged', 'lhsx', 'metrics_flat.csv'), encoding='utf-8', newline='') as f:
    mf = list(csv.DictReader(f))
print('lhsx sigma_full_reason_physics', dict(collections.Counter(r.get('sigma_full_reason_physics', 'ABSENT') for r in mf)))
print('lhsx sigma_full_status_physics', dict(collections.Counter(r.get('sigma_full_status_physics', 'ABSENT') for r in mf)))

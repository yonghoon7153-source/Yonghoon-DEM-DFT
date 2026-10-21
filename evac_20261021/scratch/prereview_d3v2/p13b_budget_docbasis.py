#!/usr/bin/env python3
"""PRE-D3V2 탐침 13b — p13 정정판: T2 런 = 설계의 기준 그대로 (1.6 s × ×20 step/s ÷ 63–70 step/s = 1.11–1.24 일 · 이 처리량은
dev-bo 의 steps_run (회전만) ÷ sacct 전체 벽시계라 정착 비용이 분모에 이미 있다 — p13 의 '생성기 정착 더하기' 는 이중 계상이라 버린다).

(a) R02 세분 상한 (최대 2 회 · 칸마다 중점 · B 끝이 있으면 A·B) — 설계 = "+ 세분 (미리 셀 수 없음)"
(b) f_cal (⬜ 0.11 – 0.30) 에 따른 T2 parcel 수 (N = f × 8.27×10⁵) — 설계 합계 = 10 만 parcel 기준 · "N 이 다르면 비례 [추정]"
재실행: python3 -I p13b_budget_docbasis.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pcommon  # noqa: E402

c = pcommon.load_checks()
ref = c.computed_numbers('lab20261014')
t2 = (ref['t2_run_d_lo'], ref['t2_run_d_hi'])
t1s = (ref['t1_short_lo'], ref['t1_short_hi'])
t1t = (ref['t1_tap_lo'], ref['t1_tap_hi'])
t1p = (ref['t1_pour_lo'], ref['t1_pour_hi'])
c2r = (ref['c2_run_lo'], ref['c2_run_hi'])


def totals(scale):
    a = [v * scale for v in t2]
    c0 = ((9 * a[0] + 6 * t1s[0]) / 3, (9 * a[1] + 6 * t1s[1]) / 3)
    c1 = ((12 * a[0] + 8 * t1t[0] + 4 * t1p[0]) / 3, (12 * a[1] + 8 * t1t[1] + 4 * t1p[1]) / 3)
    c2 = ((7 * c2r[0] + 6 * a[0]) / 3, (11 * c2r[1] + 10 * a[1]) / 3)
    return dict(c0=c0, c1=c1, c2=c2, sum=(c0[0] + c1[0] + c2[0], c0[1] + c1[1] + c2[1]))


refine_T2, refine_T1 = 2 * 7 + 2 * 14, 2 * 3 + 2 * 6
n030 = 0.30 * ref['n_per_fill']
res = dict(
    doc_basis=totals(1.0),
    f_cal_030=dict(N=n030, scale=n030 / 1e5, totals=totals(n030 / 1e5)),
    refine_upper=dict(T2_runs=refine_T2, T1_tap_runs=refine_T1,
                      days=((refine_T2 * t2[0] + refine_T1 * t1t[0]) / 3, (refine_T2 * t2[1] + refine_T1 * t1t[1]) / 3)),
)
pcommon.dump('p13b_budget_docbasis.json', res)
for k, v in res.items():
    print(k, v)

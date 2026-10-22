# -*- coding: utf-8 -*-
"""탐침 2-Q-B (PRE-impl-02 (ii) 재확인) — 모서리 인접 두 다리 (중심선 0.1414 · 닿음) 를 같은 fid (먼 길로 이어짐) · 다른 fid 로 둘 때
자기 / 서로 다른 instance 의 d0 · L_c · 배율 · k 를 나란히.  Q-B = 한 접촉 기준 (d ≤ D) — 같은 기하면 같은 접합 크기여야 (경로 위상만 다름)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pcommon import *   # noqa: F401,F403

N2 = (5, 8, 8)
SF = [[(1.95, 1.95, 0.5), (1.95, 1.95, 3.5), (1.95, 6.5, 3.5), (1.95, 6.5, 6.5), (2.05, 6.5, 6.5), (2.05, 6.5, 6.6),
       (3.5, 6.5, 6.6), (3.5, 2.05, 6.6), (2.05, 2.05, 6.6), (2.05, 2.05, 1.5)]]
out = {}
for tag, polys in (('same_fid', SF), ('distinct_fids (leg1 · leg2 only)', [SF[0][:2], SF[0][8:]])):
    P = rows(polys)
    sid, _ = bed(P, N2)
    reg = registry(sid, P, s_min_um=1.0)
    I = reg['instances']
    rowsI = []
    for q in range(len(I['fi'])):
        rowsI.append({'self': bool(I['self'][q]), 'd0': round(float(I['d0'][q]), 6), 'Lc': round(float(I['Lc'][q]), 6),
                      'mult': round(float(I['mult'][q]), 6), 'k': int(I['nsub'][q]), 's': (round(float(I['s'][q]), 4) if I['self'][q] else None),
                      'realized_sub': int(sum(1 for e, ok in zip(reg['subedges']['inst'], reg['subedges']['realized']) if e == q and ok))})
    out[tag] = rowsI
    print(tag, rowsI)
jdump(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probe2_selfd_ii.json'), out)

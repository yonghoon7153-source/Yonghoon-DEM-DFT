# -*- coding: utf-8 -*-
"""고침 C — 시험 파일의 RR5A–F (+ RR4D) 행 이름 · 수 (ast 아님 · 글: 각 t_<검사> 함수 안의 rows 목록 원소 첫 글).  쓰임: python3 rr5_row_names.py <test_rint_r_chain.py>"""
import re
import sys

src = open(sys.argv[1], encoding='utf-8').read()
cur = None
rows = {}
for line in src.splitlines():
    m = re.match(r"def t_(RR5[A-F]|RR4D)\(\):", line)
    if m:
        cur = m.group(1)
        rows[cur] = []
        continue
    if line.startswith('def ') or line.startswith('@check('):
        cur = None if not line.startswith('def t_') else cur
    if cur:
        m2 = re.match(r"\s+\('([A-Z][0-9]+[a-z]?_[A-Za-z0-9_]+)'", line)
        if m2:
            rows[cur].append(m2.group(1))
tot = 0
for k in sorted(rows):
    print(k, len(rows[k]), ' '.join(rows[k]))
    if k.startswith('RR5'):
        tot += len(rows[k])
print('RR5 행 합', tot)

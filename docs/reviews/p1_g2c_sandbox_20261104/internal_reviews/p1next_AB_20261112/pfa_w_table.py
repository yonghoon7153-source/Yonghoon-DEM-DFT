#!/usr/bin/env python3
"""Pre-attack final — re-derive the deterministic rows of draft A 15-5b power table (W and 1-round share) on the sandbox
(honest B as background, loss model Ft -> 0).  Read-only.  Usage: python3 -I pfa_w_table.py <run40000 dir>"""
import math
import sys

sys.path.insert(0, __import__('os').path.dirname(__file__))
from pfa_w_check import load, metrics, norm  # noqa: E402  (module-level code re-runs; acceptable for a small check)

D = sys.argv[1]
A = load(f'{D}/A/post/c_40000.txt')
B = load(f'{D}/B/post/c_40000.txt')
keys = sorted(set(A) & set(B))
byft = sorted(keys, key=lambda k: norm(A[k][15:18]))
n = len(keys)


def row(label, lost):
    m = metrics(B, A, lost=frozenset(lost))
    print(f'{label:28s} lost {len(lost):5d} · W {m["W"]:.4f} · share(1st round) {m["share"]:.4f}')


row('periodic flag 1', [k for k in keys if int(A[k][8]) == 1])
row('top 1 %', byft[-(n // 100):])
row('top 2 %', byft[-(2 * n // 100):])
row('bottom 25 %', byft[:n // 4])
row('bottom 50 %', byft[:n // 2])
print('periodic flag count', sum(1 for k in keys if int(A[k][8]) == 1), 'of', n)

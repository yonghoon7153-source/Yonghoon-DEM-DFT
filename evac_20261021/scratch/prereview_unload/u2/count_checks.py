#!/usr/bin/env python3
"""U2 — 자체시험 화면에서 ✓ / ✗ 줄을 묶음 (첫 낱말 · 예 R37 · C5) 마다 센다.
사용: python3 -I count_checks.py <log> [묶음 …]   (묶음 없으면 전체 합 + ✗ 줄 목록)"""
import collections
import sys

p = sys.argv[1]
want = sys.argv[2:]
ok, bad = collections.Counter(), collections.Counter()
fails = []
for ln in open(p, encoding='utf-8', errors='replace'):
    s = ln.strip()
    if s.startswith('✓') or s.startswith('✗'):
        body = s[1:].strip()
        g = body.split()[0] if body.split() else '?'
        (ok if s.startswith('✓') else bad)[g] += 1
        if s.startswith('✗'):
            fails.append(body[:150])
print(f'{p}: ok {sum(ok.values())} · fail {sum(bad.values())}')
for g in (want or sorted(set(ok) | set(bad))):
    if want or bad[g]:
        print(f'  {g}: ok {ok[g]} · fail {bad[g]}')
for f in fails:
    print('  ✗', f)

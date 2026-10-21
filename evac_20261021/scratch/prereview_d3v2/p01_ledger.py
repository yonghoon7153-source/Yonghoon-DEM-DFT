#!/usr/bin/env python3
"""PRE-D3V2 탐침 01 — 원장 MXD3-01..21 · MXD2-07 의 필드 · 등급 · 상태 · SHA 언급 (읽기만).

    python3 -I p01_ledger.py <repo>/docs/reviews/findings.json
"""
import json
import re
import sys
from collections import Counter

path = sys.argv[1]
data = json.load(open(path, encoding='utf-8'))
items = data['findings'] if isinstance(data, dict) and 'findings' in data else data
if isinstance(items, dict):
    items = list(items.values())
sel = [f for f in items if isinstance(f, dict) and str(f.get('id', '')).startswith(('MXD3-', 'MXD2-07'))]
print('found', len(sel))
sev = Counter()
keys = Counter()
for f in sel:
    keys.update(f.keys())
for f in sorted(sel, key=lambda f: f['id']):
    s = f.get('severity') or f.get('priority') or f.get('level')
    sev[s] += 1 if f['id'].startswith('MXD3') else 0
    txt = json.dumps(f, ensure_ascii=False)
    shas = sorted(set(re.findall(r'\b[0-9a-f]{9,40}\b', txt)))
    print(f"{f['id']:9s} sev={s} status={f.get('status')} shas={shas}")
print('severity counts (MXD3 only):', dict(sev))
print('keys:', dict(keys))

#!/usr/bin/env python3
"""원장 MXD3 항목 본문 출력 (읽기만).  python3 -I p01b_ledger_show.py <findings.json> [ID ...]"""
import json
import sys

data = json.load(open(sys.argv[1], encoding='utf-8'))
items = data['findings'] if isinstance(data, dict) and 'findings' in data else data
want = set(sys.argv[2:])
for f in items:
    if isinstance(f, dict) and (f.get('id') in want or (not want and str(f.get('id', '')).startswith('MXD3-'))):
        print('=' * 100)
        for k, v in f.items():
            print(f'{k}: {v}')

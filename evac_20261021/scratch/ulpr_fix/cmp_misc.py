#!/usr/bin/env python3
"""Compare two probe_misc JSON outputs key by key (short repr) — prints keys whose value differs."""
import json
import sys

a = json.load(open(sys.argv[1], encoding='utf-8'))
b = json.load(open(sys.argv[2], encoding='utf-8'))


def short(v, n=420):
    s = json.dumps(v, ensure_ascii=False, default=str)
    return s if len(s) <= n else s[:n] + '…'


keys = list(dict.fromkeys(list(a) + list(b)))
print('keys', len(keys))
for k in keys:
    va, vb = a.get(k), b.get(k)
    same = json.dumps(va, sort_keys=True, default=str) == json.dumps(vb, sort_keys=True, default=str)
    print(('SAME ' if same else 'DIFF ') + k)
    if not same:
        print('   A:', short(va))
        print('   B:', short(vb))

#!/usr/bin/env python3
"""diff_json.py A.json B.json — every leaf that differs (exact compare, floats bitwise via ==)."""
import json
import sys


def walk(x, y, p=''):
    out = []
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x) | set(y)):
            if k not in x or k not in y:
                out.append((p + '/' + k, 'missing', k in x, k in y))
            else:
                out += walk(x[k], y[k], p + '/' + k)
    elif isinstance(x, list) and isinstance(y, list):
        if len(x) != len(y):
            return [(p, 'len', len(x), len(y))]
        for i, (u, v) in enumerate(zip(x, y)):
            out += walk(u, v, p + f'[{i}]')
    elif x != y:
        out.append((p, x, y))
    return out


a = json.load(open(sys.argv[1], encoding='utf-8'))
b = json.load(open(sys.argv[2], encoding='utf-8'))
d = walk(a, b)
print('top keys', sorted(a) if isinstance(a, dict) else type(a).__name__)
print('n diffs', len(d))
for x in d[:20]:
    print('  ', x)

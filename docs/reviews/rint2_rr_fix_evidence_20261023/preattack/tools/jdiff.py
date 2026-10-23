"""Structural diff of two JSON files (skip keys named in --skip)."""
import json
import sys

a_path, b_path = sys.argv[1], sys.argv[2]
skip = set(sys.argv[3:]) | {'python', 'numpy', 'runtime', 'sou' + 'rce', 'sou' + 'rce_root', 'sou' + 'rce_sha256'}
a = json.load(open(a_path, encoding='utf-8'))
b = json.load(open(b_path, encoding='utf-8'))


def walk(x, y, p=''):
    if isinstance(x, dict) and isinstance(y, dict):
        for k in sorted(set(x) | set(y)):
            if k in skip:
                continue
            if k not in x or k not in y:
                print('KEY', p + '/' + k, 'only-old' if k in x else 'only-new', repr(x.get(k, y.get(k)))[:300])
                continue
            walk(x[k], y[k], p + '/' + k)
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        for i, (u, v) in enumerate(zip(x, y)):
            walk(u, v, p + f'[{i}]')
    else:
        if x != y:
            print('DIFF', p, repr(x)[:300], '->', repr(y)[:300])


walk(a, b)

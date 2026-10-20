"""Max relative difference of every sigma_eff / resid leaf between two q7_independent.json files.

Usage: python3 -I q7_maxrel.py <codex.json> <ours.json>
"""
import json
import sys

a = json.load(open(sys.argv[1], encoding='utf-8'), parse_constant=float)
b = json.load(open(sys.argv[2], encoding='utf-8'), parse_constant=float)
out = {}


def walk(x, y, path):
    if isinstance(x, dict) and isinstance(y, dict):
        for k in x:
            if k in y:
                walk(x[k], y[k], path + (k,))
    elif isinstance(x, list) and isinstance(y, list):
        for i, (p, q) in enumerate(zip(x, y)):
            walk(p, q, path + ('[]',))
    elif isinstance(x, float) and isinstance(y, float) and path and path[-1] in ('sigma_eff', 'resid', 'max', 'min'):
        group = path[0] + ':' + path[-1]
        r = abs(x - y) / abs(x) if x else abs(y)
        out.setdefault(group, []).append(r)


walk(a, b, ())
for g, v in sorted(out.items()):
    print(f'{g:32s} n={len(v):3d}  max_rel={max(v):.3e}  n_exact={sum(1 for r in v if r == 0)}')

"""Recursively compare two probe-evidence JSON files, ignoring path/time/environment fields.

Usage: python3 -I json_compare.py <codex.json> <ours.json> [--ignore KEY ...] [--max N]
Path-like strings (containing '/scratchpad/', 'C:\\', 'C:/', '/home/', '\\\\?\\') compare equal to each other.
Floats compare exactly (repr); NaN == NaN.
"""
import json
import math
import sys

args = sys.argv[1:]
a_path, b_path = args[0], args[1]
ignore = {'fixture', 'paths', 'path', 'source', 'file', 'seconds', 'command', 'python', 'numpy', 'scipy',
          'source_sha256', 'log_sha256', 'tail'}
mx = 60
if '--ignore' in args:
    i = args.index('--ignore')
    j = i + 1
    while j < len(args) and not args[j].startswith('--'):
        ignore.add(args[j])
        j += 1
if '--max' in args:
    mx = int(args[args.index('--max') + 1])


def load(p):
    return json.load(open(p, encoding='utf-8'), parse_constant=lambda c: float(c))


def pathlike(s):
    return isinstance(s, str) and any(t in s for t in ('/scratchpad/', 'C:\\', 'C:/', '/home/', '\\\\?\\', '/tmp/'))


diffs = []
nleaf = [0]


def cmp(a, b, where):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k in ignore:
                continue
            if k not in a or k not in b:
                diffs.append((where + '/' + str(k), 'missing-in-' + ('codex' if k not in a else 'ours'),
                              a.get(k, '<absent>') if k in a else '<absent>', b.get(k, '<absent>') if k in b else '<absent>'))
                continue
            cmp(a[k], b[k], where + '/' + str(k))
        return
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            diffs.append((where, 'len', len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            cmp(x, y, f'{where}[{i}]')
        return
    nleaf[0] += 1
    if pathlike(a) and pathlike(b):
        return
    if isinstance(a, float) and isinstance(b, float):
        if (math.isnan(a) and math.isnan(b)) or a == b:
            return
        diffs.append((where, 'float', repr(a), repr(b)))
        return
    if isinstance(a, str) and isinstance(b, str) and a != b:
        # strings that embed paths (messages) — compare after removing path prefixes
        if pathlike(a) or pathlike(b):
            diffs.append((where, 'str-with-path', a[:160], b[:160]))
            return
    if a != b:
        diffs.append((where, 'value', a if not isinstance(a, str) else a[:160], b if not isinstance(b, str) else b[:160]))


cmp(load(a_path), load(b_path), '')
print(f'leaves {nleaf[0]}  diffs {len(diffs)}')
for d in diffs[:mx]:
    print('  ', d)

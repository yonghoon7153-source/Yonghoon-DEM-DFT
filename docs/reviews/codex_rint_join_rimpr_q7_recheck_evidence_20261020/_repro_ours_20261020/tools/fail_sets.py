"""Compare the set of FAIL / PASS item lines between two test logs (read-only).

Usage: python3 -I fail_sets.py <codex.log> <ours.log>
Item lines: '  PASS  ...' / '  FAIL  ...' and the trailing '  - ...' failure list.
"""
import re
import sys


def items(p):
    t = open(p, 'rb').read().decode('utf-8', 'replace').splitlines()
    pas = [l.strip() for l in t if re.match(r'^\s+PASS\s', l)]
    fai = [l.strip() for l in t if re.match(r'^\s+FAIL\s', l)]
    lst = [l.strip() for l in t if re.match(r'^\s+- ', l)]
    return pas, fai, lst


a, b = items(sys.argv[1]), items(sys.argv[2])
for name, x, y in (('PASS', a[0], b[0]), ('FAIL', a[1], b[1]), ('fail-list', a[2], b[2])):
    sx, sy = set(x), set(y)
    print(f'{name:9s} codex {len(x):4d} ours {len(y):4d}  same-set {sx == sy}  only-codex {len(sx - sy)} only-ours {len(sy - sx)}')
    for s in sorted(sx - sy)[:5]:
        print('    only-codex:', s[:150])
    for s in sorted(sy - sx)[:5]:
        print('    only-ours :', s[:150])

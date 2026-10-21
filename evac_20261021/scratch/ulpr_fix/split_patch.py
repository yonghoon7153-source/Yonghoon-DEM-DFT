#!/usr/bin/env python3
"""Split a unified git diff into a filtered patch by hunk selection.
Usage: python3 split_patch.py <in.patch> <out.patch> <spec>
spec = 'file=lo-hi,lo-hi;file2=lo-hi' — keep hunks whose OLD start line falls in any range for that file (basename)."""
import re
import sys

src, dst, spec = sys.argv[1:4]
want = {}
for part in spec.split(';'):
    f, rngs = part.split('=')
    want[f] = [tuple(int(x) for x in r.split('-')) for r in rngs.split(',')]
out, cur_file, header, hunk, keep_any = [], None, [], [], {}
lines = open(src, encoding='utf-8').read().split('\n')
i = 0
blocks = []   # (file, header lines, [hunks])
while i < len(lines):
    ln = lines[i]
    if ln.startswith('diff --git '):
        blocks.append([None, [ln], []])
        i += 1
        while i < len(lines) and not lines[i].startswith('@@'):
            blocks[-1][1].append(lines[i])
            if lines[i].startswith('+++ b/'):
                blocks[-1][0] = lines[i][6:].split('/')[-1]
            i += 1
        continue
    if ln.startswith('@@'):
        h = [ln]
        i += 1
        while i < len(lines) and not lines[i].startswith(('@@', 'diff --git ')):
            h.append(lines[i])
            i += 1
        if h[-1] == '' and i >= len(lines):
            h = h[:-1]
        blocks[-1][2].append(h)
        continue
    i += 1
res = []
for f, hdr, hunks in blocks:
    sel = []
    for h in hunks:
        m = re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', h[0])
        old = int(m.group(1))
        if any(lo <= old <= hi for lo, hi in want.get(f, [])):
            sel.append(h)
    print(f, 'hunks', len(hunks), 'kept', len(sel))
    if sel:
        res += hdr
        for h in sel:
            res += h
open(dst, 'w', encoding='utf-8').write('\n'.join(res) + '\n')

#!/usr/bin/env python3
"""splice.py <file> <start-marker> <end-marker> <replacement-file> — replace [start, end) of file with replacement text."""
import sys

path, start_m, end_m, rep = sys.argv[1:5]
s = open(path, encoding='utf-8').read()
a = s.index(start_m)
b = s.index(end_m, a)
new = open(rep, encoding='utf-8').read()
open(path, 'w', encoding='utf-8').write(s[:a] + new + s[b:])
print(f'spliced {path}: {b - a} chars -> {len(new)} chars')

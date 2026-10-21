"""Scan HEAD code for names used in the design / registration / kgy documents.

Usage: python3 -I name_scan.py <repo_root> <names.txt>
Prints, per name, production files (non-test) and test-file count.
Read-only.
"""
import os
import sys

root = sys.argv[1]
names = [ln.strip() for ln in open(sys.argv[2], encoding='utf-8') if ln.strip()]
exts = ('.py', '.sh', '.html', '.js')
files = []
for sub in ('scripts', 'webapp'):
    for dp, dn, fn in os.walk(os.path.join(root, sub)):
        if '__pycache__' in dp or '/templates/' in dp + '/' and False:
            pass
        for f in fn:
            if f.endswith(exts):
                files.append(os.path.join(dp, f))
texts = {}
for p in files:
    try:
        texts[p] = open(p, encoding='utf-8', errors='replace').read()
    except OSError:
        pass
for n in names:
    prod, tests = [], []
    for p, t in texts.items():
        if n in t:
            rel = os.path.relpath(p, root)
            (tests if os.path.basename(p).startswith('test_') else prod).append(rel)
    print(f"{n} | prod: {' '.join(sorted(prod)) or 'NONE'} | tests: {len(tests)}")

#!/usr/bin/env python3
"""List backticked path / SHA tokens of a markdown file the way scripts/check_doc_refs.py classifies them.
Usage: python3 refscan.py <repo root> <doc.md> [doc folder in repo (for relative paths)]"""
import os
import re
import subprocess
import sys

root, doc = sys.argv[1], sys.argv[2]
rel_dir = sys.argv[3] if len(sys.argv) > 3 else ''
txt = open(doc, encoding='utf-8').read()
EXTS = ('py', 'sh', 'json', 'csv', 'md', 'mjs', 'js', 'yml', 'yaml', 'liggghts', 'stl', 'npy', 'txt')
RP = re.compile(r'`([A-Za-z0-9_][A-Za-z0-9_./+-]*\.(?:' + '|'.join(EXTS) + r'))`')
for p in sorted(set(RP.findall(txt))):
    q = p.lstrip('./')
    ex = os.path.exists(os.path.join(root, q)) or (rel_dir and os.path.exists(os.path.join(root, rel_dir, q)))
    print(('OK  ' if ex else ('BARE' if '/' not in q else 'MISS')), q)
shas = set(subprocess.run(['git', '-C', root, 'rev-list', '--remotes', 'HEAD'], capture_output=True, text=True).stdout.split())
for s in sorted(set(re.findall(r'`([0-9a-f]{7,40})`', txt))):
    if s.isdigit():
        continue
    print('SHA', s, 'reachable' if any(x.startswith(s) for x in shas) else 'NOT-REACHABLE')

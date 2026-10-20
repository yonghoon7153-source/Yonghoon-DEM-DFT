"""Compare a GitHub API recursive tree JSON with `git ls-tree -r` output (blob path+sha+mode), read-only.

Usage: python3 -I tree_vs_lstree.py <tree.json> <lstree.txt>
"""
import json
import sys

t = json.load(open(sys.argv[1], encoding='utf-8'))
gh = {(x['path'], x['sha'], x['mode']) for x in t['tree'] if x['type'] == 'blob'}
loc = set()
raw = open(sys.argv[2], 'rb').read().decode('utf-8')  # `git ls-tree -r -z` output (NUL-separated, unquoted)
for rec in raw.split('\0'):
    if not rec:
        continue
    meta, path = rec.split('\t', 1)
    mode, typ, sha = meta.split()
    if typ == 'blob':
        loc.add((path, sha, mode))
print('tree sha', t.get('sha'), 'truncated', t.get('truncated'), '| github blobs', len(gh), 'git ls-tree blobs', len(loc),
      '| equal', gh == loc, '| only-github', len(gh - loc), 'only-git', len(loc - gh))
for x in sorted(gh - loc)[:5]:
    print('  only-github', x)
for x in sorted(loc - gh)[:5]:
    print('  only-git   ', x)

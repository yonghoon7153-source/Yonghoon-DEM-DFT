"""Check every (path, git_blob) of a Codex source_manifest.json against `git ls-tree -r -z <pin>` (read-only).

Usage: python3 -I manifest_vs_lstree.py <source_manifest.json> <lstree.z>
"""
import json
import sys

m = json.load(open(sys.argv[1], encoding='utf-8'))
tree = {}
for rec in open(sys.argv[2], 'rb').read().decode('utf-8').split('\0'):
    if rec:
        meta, path = rec.split('\t', 1)
        mode, typ, sha = meta.split()
        if typ == 'blob':
            tree[path] = sha
ok = sum(1 for e in m['files'] if tree.get(e['path']) == e['git_blob'])
bad = [e['path'] for e in m['files'] if tree.get(e['path']) != e['git_blob']]
print('pin', m['pin'], 'manifest', len(m['files']), 'equal to git ls-tree blob', ok, 'different/missing', len(bad), bad[:5])

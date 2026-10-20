"""Compare a Codex source_manifest.json against a local tree (sha256 + git blob), read-only.

Usage: python3 -I manifest_vs_tree.py <source_manifest.json> <tree_root> [--require PREFIX ...]
Prints counts: same / differ / missing, and lists differ + missing among --require prefixes.
"""
import hashlib
import json
import os
import sys

mf = json.load(open(sys.argv[1], encoding='utf-8'))
root = sys.argv[2]
req = []
if '--require' in sys.argv:
    req = sys.argv[sys.argv.index('--require') + 1:]
same = differ = missing = 0
diffs, miss = [], []
for e in mf['files']:
    p = os.path.join(root, e['path'])
    if not os.path.isfile(p):
        missing += 1
        miss.append(e['path'])
        continue
    b = open(p, 'rb').read()
    blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
    if hashlib.sha256(b).hexdigest() == e['sha256'] and blob == e['git_blob'] and len(b) == e['bytes']:
        same += 1
    else:
        differ += 1
        diffs.append(e['path'])
print('pin', mf.get('pin'), 'manifest files', len(mf['files']), 'same', same, 'differ', differ, 'missing', missing)
for d in diffs[:40]:
    print('  DIFFER', d)
if req:
    for m in miss:
        if any(m.startswith(r) for r in req):
            print('  MISSING(required)', m)
else:
    for m in miss[:15]:
        print('  missing', m)

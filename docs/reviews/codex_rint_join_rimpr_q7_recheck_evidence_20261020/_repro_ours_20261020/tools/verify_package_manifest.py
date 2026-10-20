"""Verify the bundle's PACKAGE_MANIFEST.json against the extracted files (read-only).

Usage: python3 -I verify_package_manifest.py <extract_root>
"""
import hashlib
import json
import os
import sys

root = sys.argv[1]
m = json.load(open(os.path.join(root, 'PACKAGE_MANIFEST.json'), encoding='utf-8'))
print({k: v for k, v in m.items() if k != 'files'})
listed = {}
bad = []
for e in m['files']:
    p = os.path.join(root, e['path'])
    listed[e['path']] = e
    if not os.path.isfile(p):
        bad.append(('missing', e['path']))
        continue
    b = open(p, 'rb').read()
    if len(b) != e['bytes'] or hashlib.sha256(b).hexdigest() != e['sha256']:
        bad.append(('mismatch', e['path']))
actual = set()
for dp, dn, fn in os.walk(root):
    for f in fn:
        actual.add(os.path.relpath(os.path.join(dp, f), root).replace(os.sep, '/'))
extra = sorted(actual - set(listed) - {'PACKAGE_MANIFEST.json'})
print('listed', len(listed), 'actual files', len(actual), 'bad', len(bad), 'unlisted extra', len(extra))
for x in bad[:10]:
    print('  ', x)
for x in extra[:10]:
    print('   extra', x)

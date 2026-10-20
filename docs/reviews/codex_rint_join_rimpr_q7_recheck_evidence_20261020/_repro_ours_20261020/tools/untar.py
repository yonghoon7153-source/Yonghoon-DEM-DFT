"""Extract a tar (made by git archive from our own repo) into a new empty directory.

Usage: python3 -I untar.py <tar> <dest>
"""
import os
import sys
import tarfile

tp, dest = sys.argv[1], os.path.abspath(sys.argv[2])
if os.path.exists(dest) and os.listdir(dest):
    sys.exit('dest not empty')
os.makedirs(dest, exist_ok=True)
with tarfile.open(tp) as t:
    members = t.getmembers()
    for m in members:
        if m.name.startswith('/') or '..' in m.name.split('/'):
            sys.exit('bad member ' + m.name)
        if m.issym() or m.islnk():
            print('skip link', m.name)
    t.extractall(dest, members=[m for m in members if not (m.issym() or m.islnk())], filter='data')
n = sum(len(f) for _, _, f in os.walk(dest))
print('files', n)

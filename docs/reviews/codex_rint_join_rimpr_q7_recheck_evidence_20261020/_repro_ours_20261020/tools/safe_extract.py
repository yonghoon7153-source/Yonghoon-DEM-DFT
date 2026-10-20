"""Extract a ZIP into a NEW empty directory, refusing any member that would land outside it.

Usage: python3 -I safe_extract.py <zip> <dest_dir_that_must_not_exist_or_be_empty>
"""
import os
import stat
import sys
import zipfile

zp, dest = sys.argv[1], sys.argv[2]
dest = os.path.abspath(dest)
if os.path.exists(dest):
    if os.listdir(dest):
        sys.exit('dest not empty: ' + dest)
else:
    os.makedirs(dest)
real_dest = os.path.realpath(dest)
n = 0
with zipfile.ZipFile(zp) as z:
    for i in z.infolist():
        name = i.filename
        mode = (i.external_attr >> 16) & 0xFFFF
        if mode and stat.S_ISLNK(mode):
            sys.exit('symlink refused: ' + name)
        if name.startswith('/') or '\\' in name or (len(name) > 1 and name[1] == ':'):
            sys.exit('bad name refused: ' + name)
        parts = name.split('/')
        if '..' in parts:
            sys.exit('dotdot refused: ' + name)
        target = os.path.realpath(os.path.join(real_dest, name))
        if not (target == real_dest or target.startswith(real_dest + os.sep)):
            sys.exit('escape refused: ' + name)
        if name.endswith('/'):
            os.makedirs(target, exist_ok=True)
            continue
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with z.open(i) as src, open(target, 'xb') as out:
            while True:
                b = src.read(1 << 20)
                if not b:
                    break
                out.write(b)
        os.chmod(target, 0o644)
        n += 1
print('extracted files', n, 'into', real_dest)

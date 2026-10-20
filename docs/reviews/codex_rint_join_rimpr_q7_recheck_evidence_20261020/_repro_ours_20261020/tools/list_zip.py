"""List a ZIP's members and flag dangerous entries (absolute paths, '..', symlinks, drive letters, backslashes).

Usage: python3 -I list_zip.py <zip>
Reads only; writes nothing.
"""
import stat
import sys
import zipfile
from collections import Counter

zp = sys.argv[1]
with zipfile.ZipFile(zp) as z:
    infos = z.infolist()
    n = len(infos)
    danger = []
    dirs = 0
    files = 0
    total = 0
    tops = Counter()
    for i in infos:
        name = i.filename
        mode = (i.external_attr >> 16) & 0xFFFF
        is_link = stat.S_ISLNK(mode) if mode else False
        parts = name.replace('\\', '/').split('/')
        bad = []
        if name.startswith('/') or name.startswith('\\'):
            bad.append('absolute')
        if len(name) >= 2 and name[1] == ':':
            bad.append('drive')
        if '..' in parts:
            bad.append('dotdot')
        if '\\' in name:
            bad.append('backslash')
        if is_link:
            bad.append('symlink')
        if '\x00' in name:
            bad.append('nul')
        if bad:
            danger.append((name, bad))
        if name.endswith('/'):
            dirs += 1
        else:
            files += 1
            total += i.file_size
        tops[parts[0]] += 1
    print('entries', n, 'dirs', dirs, 'files', files, 'uncompressed_bytes', total)
    print('danger', len(danger))
    for d in danger[:50]:
        print('  DANGER', d)
    print('top-level:')
    for k, v in sorted(tops.items()):
        print('  ', k, v)
    bad_crc = z.testzip()
    print('testzip first bad member:', bad_crc)

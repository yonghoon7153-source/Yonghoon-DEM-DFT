"""List zip members, flag dangerous paths, and (optionally) extract safely.

usage: python3 -I inspect_zip.py <zip> [<dest_dir_to_extract_into>]
Refuses: absolute paths, '..' components, drive letters, backslashes,
symlinks (unix mode S_IFLNK), duplicate names.
"""
import os
import stat
import sys
import zipfile


def main():
    zpath = sys.argv[1]
    dest = sys.argv[2] if len(sys.argv) > 2 else None
    bad = []
    names = []
    total = 0
    with zipfile.ZipFile(zpath) as z:
        infos = z.infolist()
        for i in infos:
            n = i.filename
            names.append(n)
            mode = (i.external_attr >> 16) & 0xFFFF
            reason = []
            if n.startswith('/') or n.startswith('\\'):
                reason.append('absolute')
            if len(n) > 1 and n[1] == ':':
                reason.append('drive')
            if '\\' in n:
                reason.append('backslash')
            parts = n.replace('\\', '/').split('/')
            if any(p == '..' for p in parts):
                reason.append('dotdot')
            if mode and stat.S_ISLNK(mode):
                reason.append('symlink')
            if reason:
                bad.append((n, reason))
            total += i.file_size
        dups = len(names) - len(set(names))
        n_dirs = sum(1 for i in infos if i.is_dir())
        print(f'entries={len(infos)} dirs={n_dirs} files={len(infos)-n_dirs} '
              f'uncompressed_bytes={total} dup_names={dups}')
        for i in infos:
            print(f'{i.file_size:>10}  {i.filename}')
        if bad:
            print('DANGEROUS:')
            for n, r in bad:
                print('  ', r, n)
            sys.exit(2)
        if dups:
            print('DUPLICATE NAMES - refuse')
            sys.exit(3)
        if dest:
            if os.listdir(dest):
                print('dest not empty - refuse')
                sys.exit(4)
            dest_real = os.path.realpath(dest)
            for i in infos:
                target = os.path.realpath(os.path.join(dest_real, i.filename))
                if not (target == dest_real or target.startswith(dest_real + os.sep)):
                    print('escape - refuse', i.filename)
                    sys.exit(5)
            z.extractall(dest_real)
            print('extracted to', dest_real)


if __name__ == '__main__':
    main()

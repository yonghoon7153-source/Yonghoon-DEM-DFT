"""Compare bundle CONTENTS_SHA256.json against the extracted files.

usage: python3 -I check_contents.py <extracted_root>
"""
import hashlib
import json
import os
import sys


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def main():
    root = sys.argv[1]
    with open(os.path.join(root, 'CONTENTS_SHA256.json'), encoding='utf-8') as f:
        d = json.load(f)
    print('top type', type(d).__name__)
    if isinstance(d, dict):
        print('keys', list(d.keys())[:12])
        for k, v in list(d.items())[:2]:
            print(' ', k, '->', str(v)[:400])
    # find the list of entries
    entries = None
    if isinstance(d, list):
        entries = d
    elif isinstance(d, dict):
        for k in ('files', 'entries', 'items', 'contents'):
            if k in d and isinstance(d[k], (list, dict)):
                entries = d[k]
                break
        if entries is None:
            entries = d
    rows = []
    if isinstance(entries, dict):
        for k, v in entries.items():
            if isinstance(v, dict):
                rows.append((k, v.get('sha256'), v.get('bytes', v.get('size'))))
            else:
                rows.append((k, v, None))
    else:
        for e in entries:
            if isinstance(e, dict):
                rows.append((e.get('path') or e.get('name'), e.get('sha256'),
                             e.get('bytes', e.get('size'))))
    print('manifest rows', len(rows))
    ok = bad = missing = 0
    listed = set()
    for p, s, b in rows:
        if p is None:
            continue
        listed.add(p)
        fp = os.path.join(root, p)
        if not os.path.isfile(fp):
            missing += 1
            print('MISSING', p)
            continue
        actual = sha(fp)
        sz = os.path.getsize(fp)
        if actual == s and (b is None or int(b) == sz):
            ok += 1
        else:
            bad += 1
            print('DIFF', p, s, actual, b, sz)
    all_files = []
    for dp, dn, fn in os.walk(root):
        for n in fn:
            rel = os.path.relpath(os.path.join(dp, n), root).replace(os.sep, '/')
            all_files.append(rel)
    unlisted = sorted(set(all_files) - listed)
    print(f'ok={ok} bad={bad} missing={missing} unlisted={len(unlisted)}')
    for u in unlisted:
        print('UNLISTED', u)


if __name__ == '__main__':
    main()

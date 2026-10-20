"""Compare two fixture folders file-by-file: exact bytes, then CRLF->LF normalized, then gunzipped.

Usage: python3 -I fixture_cmp.py <codex_dir> <ours_dir>
"""
import gzip
import os
import sys

a, b = sys.argv[1], sys.argv[2]
names = sorted(set(os.listdir(a)) | set(os.listdir(b)))
exact = crlf = gz_same = other = missing = 0
odd = []
for n in names:
    pa, pb = os.path.join(a, n), os.path.join(b, n)
    if not (os.path.isfile(pa) and os.path.isfile(pb)):
        missing += 1
        odd.append(('missing', n))
        continue
    x, y = open(pa, 'rb').read(), open(pb, 'rb').read()
    if x == y:
        exact += 1
    elif x.replace(b'\r\n', b'\n') == y.replace(b'\r\n', b'\n'):
        crlf += 1
    elif n.endswith('.gz') and gzip.decompress(x) == gzip.decompress(y):
        gz_same += 1
    else:
        other += 1
        odd.append(('differ', n))
print(f'files {len(names)} exact {exact} same-after-CRLF->LF {crlf} same-after-gunzip {gz_same} differ {other} missing {missing}')
for o in odd[:20]:
    print('  ', o)

#!/usr/bin/env python3
"""Which step3 values differ between the old (given scripts dir) and the current payload for the B6 'off LEAN2' run."""
import importlib.util
import os
import shutil
import sys
import tempfile

WT = sys.argv[1]
OLD = sys.argv[2]
sys.path.insert(0, os.path.join(WT, 'scripts'))
spec = importlib.util.spec_from_file_location('b6', os.path.join(WT, 'scripts', 'test_ca_ext_b6.py'))
B6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B6)
import run_contract as RC  # noqa: E402
import ca_ext_cjunc as CW  # noqa: E402
B6.RC, B6.CW = RC, CW


class A:
    old_scripts = OLD
    keep = False
B6.ARGS = A
td = tempfile.mkdtemp(prefix='b1probe_')
try:
    os.makedirs(os.path.join(td, 'w'))
    d = B6.make_fixture(os.path.join(td, 'w'), sdcp=True)
    extra = B6.OFF + B6.LEAN2
    r_old = B6.run_payload(d, extra, out='old.json', payload=os.path.join(OLD, 'mpm_webapp_payload.py'))
    r_new = B6.run_payload(d, extra, out='new.json')
    print('rc', r_old[0], r_new[0])
    s_old = {k: v for k, v in B6.s3_of(r_old[2]).items() if k != 'manifest'}
    s_new = {k: v for k, v in B6.s3_of(r_new[2]).items() if k != 'manifest'}
    ks = sorted(set(s_old) | set(s_new))
    def walk(x, y, p):
        if isinstance(x, dict) and isinstance(y, dict):
            for k in sorted(set(x) | set(y)):
                walk(x.get(k), y.get(k), p + '/' + str(k))
        elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
            for i, (u, v) in enumerate(zip(x, y)):
                walk(u, v, p + f'[{i}]')
        elif x != y:
            print('DIFF', p, repr(x)[:300], '|', repr(y)[:300])
    for k in ks:
        if s_old.get(k) != s_new.get(k):
            walk(s_old.get(k), s_new.get(k), k)
    print('n keys', len(ks))
finally:
    shutil.rmtree(td, ignore_errors=True)

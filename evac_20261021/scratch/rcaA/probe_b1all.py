#!/usr/bin/env python3
"""Off-path identity vs a base scripts snapshot (B6 B1 cases, junction off): manifest (code_sha · exec_env out) and step3 values
compared directly (no 'new field' popping — the base snapshot already has the Z3 fields)."""
import importlib.util
import json
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
td = tempfile.mkdtemp(prefix='b1all_')
try:
    os.makedirs(os.path.join(td, 'w'))
    d = B6.make_fixture(os.path.join(td, 'w'), sdcp=True)
    for nm, extra in (('off LEAN2', B6.OFF + B6.LEAN2), ('centerline LEAN2', ['--ptfe-stamp', 'centerline'] + B6.LEAN2),
                      ('off LEAN3', B6.OFF + B6.LEAN3), ('face_alpha LEAN2', ['--ptfe-stamp', 'face_alpha'] + B6.LEAN2),
                      ('off LEAN2 + rtol 1e-12', B6.OFF + B6.LEAN2 + ['--step3-rtol', '1e-12'])):
        r_old = B6.run_payload(d, extra, out='old_%s.json' % nm.replace(' ', '_'), payload=os.path.join(OLD, 'mpm_webapp_payload.py'))
        r_new = B6.run_payload(d, extra, out='new_%s.json' % nm.replace(' ', '_'))
        m_old = dict(B6.man_of(r_old[2])); m_new = dict(B6.man_of(r_new[2]))
        for k in ('code_sha', 'exec_env'):
            m_old.pop(k, None); m_new.pop(k, None)
        s_old = {k: v for k, v in B6.s3_of(r_old[2]).items() if k != 'manifest'}
        s_new = {k: v for k, v in B6.s3_of(r_new[2]).items() if k != 'manifest'}
        mdiff = sorted(k for k in set(m_old) | set(m_new) if m_old.get(k) != m_new.get(k))
        sdiff = sorted(k for k in set(s_old) | set(s_new) if s_old.get(k) != s_new.get(k))
        same = (r_old[0] == 0 and r_new[0] == 0 and json.dumps(m_old, sort_keys=True) == json.dumps(m_new, sort_keys=True)
                and s_old == s_new)
        print(f'{nm}: rc {r_old[0]}/{r_new[0]} · manifest diff {mdiff} · step3 diff {sdiff} · identical {same}')
finally:
    shutil.rmtree(td, ignore_errors=True)

"""Debug test_ca_ext_b6 B1: run one payload case with old (base) and new scripts and print the step3 / manifest differences.

usage: python3 b1_debug.py <repo scripts dir> <old scripts dir> <case: off|face_alpha|rtol>
"""
import json
import os
import shutil
import sys
import tempfile

scripts, old, which = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, scripts)
import test_ca_ext_b6 as B6  # noqa: E402

extra = {'off': B6.OFF + B6.LEAN2, 'face_alpha': ['--ptfe-stamp', 'face_alpha'] + B6.LEAN2,
         'rtol': B6.OFF + B6.LEAN2 + ['--step3-rtol', '1e-12']}[which]
td = tempfile.mkdtemp(prefix='b1dbg_')
try:
    os.makedirs(os.path.join(td, 'w'))
    d = B6.make_fixture(os.path.join(td, 'w'), sdcp=True)
    r_old = B6.run_payload(d, extra, out='old.json', payload=os.path.join(old, 'mpm_webapp_payload.py'))
    r_new = B6.run_payload(d, extra, out='new.json')
    print('rc', r_old[0], r_new[0])
    so, sn = B6.s3_of(r_old[2]), B6.s3_of(r_new[2])
    mo, mn = dict(so.get('manifest') or {}), dict(sn.get('manifest') or {})
    for k in ('code_sha', 'exec_env'):
        mo.pop(k, None)
        mn.pop(k, None)
    print('manifest keys differing:', sorted(k for k in set(mo) | set(mn) if mo.get(k) != mn.get(k)))
    so2 = {k: v for k, v in so.items() if k != 'manifest'}
    sn2 = {k: v for k, v in sn.items() if k != 'manifest'}
    for k in sorted(set(so2) | set(sn2)):
        if so2.get(k) != sn2.get(k):
            a, b = so2.get(k), sn2.get(k)
            if isinstance(a, dict) and isinstance(b, dict):
                sub = sorted(x for x in set(a) | set(b) if a.get(x) != b.get(x))
                print(f'step3 [{k}] dict keys differing: {sub[:40]}')
                for x in sub[:12]:
                    print('    ', x, json.dumps(a.get(x))[:160], '|', json.dumps(b.get(x))[:160])
            else:
                print(f'step3 [{k}]', json.dumps(a)[:200], '|', json.dumps(b)[:200])
    if which == 'face_alpha':
        eo = (((mo.get('ca_ext') or {}).get('ptfe_face') or {}).get('evidence') or {})
        en = (((mn.get('ca_ext') or {}).get('ptfe_face') or {}).get('evidence') or {})
        for x in sorted(set(eo) | set(en)):
            if eo.get(x) != en.get(x):
                print('  evidence', x, json.dumps(eo.get(x))[:200], '|', json.dumps(en.get(x))[:200])
finally:
    shutil.rmtree(td, ignore_errors=True)

"""B1 diff probe — run the payload old/new on the b6 fixture and print every differing path (manifest + step3 values)."""
import json
import os
import shutil
import sys
import tempfile

W = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-afe53be7bdb176c82'
OLD = sys.argv[1]
CASES = sys.argv[2].split('|') if len(sys.argv) > 2 else None
sys.path.insert(0, os.path.join(W, 'scripts'))
import test_ca_ext_b6 as B6
import run_contract as RC
B6.RC = RC
import ca_ext_cjunc as CW
B6.CW = CW


def walk(a, b, p=''):
    out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append(('+', p + '.' + k, json.dumps(b[k], sort_keys=True)[:160]))
            elif k not in b:
                out.append(('-', p + '.' + k, json.dumps(a[k], sort_keys=True)[:160]))
            else:
                out += walk(a[k], b[k], p + '.' + k)
    elif a != b:
        out.append(('~', p, (json.dumps(a, sort_keys=True)[:120], json.dumps(b, sort_keys=True)[:120])))
    return out


td = tempfile.mkdtemp(prefix='b1diff_')
try:
    os.makedirs(os.path.join(td, 'w'))
    d = B6.make_fixture(os.path.join(td, 'w'), sdcp=True)
    allc = (('off LEAN2', B6.OFF + B6.LEAN2), ('centerline LEAN2', ['--ptfe-stamp', 'centerline'] + B6.LEAN2),
            ('off LEAN3', B6.OFF + B6.LEAN3), ('face_alpha LEAN2', ['--ptfe-stamp', 'face_alpha'] + B6.LEAN2),
            ('off LEAN2 + rtol 1e-12', B6.OFF + B6.LEAN2 + ['--step3-rtol', '1e-12']),
            ('off LEAN2 + cjunc', B6.OFF + B6.LEAN2 + B6.CJ),
            ('face_alpha LEAN2 + rtol', ['--ptfe-stamp', 'face_alpha'] + B6.LEAN2 + ['--step3-rtol', '1e-12']))
    for nm, extra in allc:
        if CASES and nm not in CASES:
            continue
        tag = nm.replace(' ', '_').replace('+', 'p')
        r_old = B6.run_payload(d, extra, out=f'old_{tag}.json', payload=os.path.join(OLD, 'mpm_webapp_payload.py'))
        r_new = B6.run_payload(d, extra, out=f'new_{tag}.json')
        po, pn = r_old[2] or {}, r_new[2] or {}
        so, sn = B6.s3_of(po), B6.s3_of(pn)
        print(f'== {nm}: rc old {r_old[0]} new {r_new[0]}')
        for x in walk(so, sn, 'step3'):
            if x[1].endswith('.code_sha') or '.exec_env' in x[1]:
                continue
            print('   ', x)
finally:
    shutil.rmtree(td, ignore_errors=True)

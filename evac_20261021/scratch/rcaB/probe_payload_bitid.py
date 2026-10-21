"""Off-path / on-path byte comparison of the real production payload: base modules (a76f59d0d run_contract · step3_conv_cert ·
step3_sigma = b7pre) vs this fix (b7fix) — the same fixture bed and the same five configurations as test_ca_ext_b6 B1, but the
expected difference is THIS change only (B1 hard-codes the pre-Z3 base: it strips fp.sid_off and cg_iters from the new side,
which b7pre already has, so B1 cannot be used with this base).

Expected: off LEAN2 · centerline LEAN2 · off LEAN3 · face_alpha LEAN2 (no certificate) → manifest (code_sha · exec_env removed) and
step3 values byte-identical; off LEAN2 + rtol 1e-12 → identical except conv_cert gains exactly the six binding keys (bind_version ·
fp_sid · fp_sig · fp_face_plan · fp_cjunc_registry · fp_cjunc_rows), all other conv_cert values equal.
usage: python3 probe_payload_bitid.py <b7pre> <b7fix>"""
import json
import os
import shutil
import sys
import tempfile

PRE, FIX = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(FIX, 'scripts'))
import test_ca_ext_b6 as B6     # noqa: E402

BIND = {'bind_version', 'fp_sid', 'fp_sig', 'fp_face_plan', 'fp_cjunc_registry', 'fp_cjunc_rows'}
CONFIGS = (('off LEAN2', B6.OFF + B6.LEAN2), ('centerline LEAN2', ['--ptfe-stamp', 'centerline'] + B6.LEAN2),
           ('off LEAN3', B6.OFF + B6.LEAN3), ('face_alpha LEAN2', ['--ptfe-stamp', 'face_alpha'] + B6.LEAN2),
           ('off LEAN2 + rtol 1e-12', B6.OFF + B6.LEAN2 + ['--step3-rtol', '1e-12']))
td = tempfile.mkdtemp(prefix='b7_bitid_')
bad = 0
try:
    os.makedirs(os.path.join(td, 'w'))
    d = B6.make_fixture(os.path.join(td, 'w'), sdcp=True)
    for nm, extra in CONFIGS:
        tag = nm.replace(' ', '_')
        r_old = B6.run_payload(d, extra, out=f'old_{tag}.json', payload=os.path.join(PRE, 'scripts', 'mpm_webapp_payload.py'))
        r_new = B6.run_payload(d, extra, out=f'new_{tag}.json', payload=os.path.join(FIX, 'scripts', 'mpm_webapp_payload.py'))
        m_old, m_new = dict(B6.man_of(r_old[2]) or {}), dict(B6.man_of(r_new[2]) or {})
        for k in ('code_sha', 'exec_env'):
            m_old.pop(k, None)
            m_new.pop(k, None)
        s_old = {k: v for k, v in (B6.s3_of(r_old[2]) or {}).items() if k != 'manifest'}
        s_new = {k: v for k, v in (B6.s3_of(r_new[2]) or {}).items() if k != 'manifest'}
        man_same = json.dumps(m_old, sort_keys=True) == json.dumps(m_new, sort_keys=True)
        added = []
        cert_rest_same = True
        for ck in ('conv_cert', 'ion_conv_cert'):
            co, cn = s_old.get(ck), s_new.get(ck)
            if isinstance(co, dict) and isinstance(cn, dict):
                added += [f'{ck}.{k}' for k in sorted(set(cn) - set(co))]
                gone = sorted(set(co) - set(cn))
                rest = {k: v for k, v in cn.items() if k in co}
                cert_rest_same &= (not gone) and json.dumps(rest, sort_keys=True) == json.dumps(co, sort_keys=True)
                s_old = dict(s_old, **{ck: None})
                s_new = dict(s_new, **{ck: None})
        other_same = json.dumps(s_old, sort_keys=True, default=str) == json.dumps(s_new, sort_keys=True, default=str)
        want_added = sorted(f'conv_cert.{k}' for k in BIND) if 'rtol' in nm else []
        ok = (r_old[0] == 0 and r_new[0] == 0 and man_same and other_same and cert_rest_same and sorted(added) == want_added)
        bad += (not ok)
        print(f"{'  ok ' if ok else '  BAD'} [{nm}] rc {r_old[0]}/{r_new[0]} · manifest same {man_same} · step3 (certificates "
              f"aside) same {other_same} · certificate old keys same {cert_rest_same} · added {added}")
finally:
    shutil.rmtree(td, ignore_errors=True)
print(f'== probe_payload_bitid: {len(CONFIGS) - bad}/{len(CONFIGS)}')
sys.exit(1 if bad else 0)

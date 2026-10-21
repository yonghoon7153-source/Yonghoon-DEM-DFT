"""Off-path bit identity of the payload — base a76f59d0d (archive with docs/data/rint_eis_anchors.csv) ↔ HEAD, NO field allowances.
Same fixture / runner as test_ca_ext_b6 (B6.make_fixture · B6.run_payload).  Reports, per arm, rc · manifest equality (code_sha /
exec_env removed) · step3 dict equality · the differing leaf paths (if any)."""
import importlib.util
import json
import os
import shutil
import sys
import tempfile

WT = '/home/user/Yonghoon-DEM-DFT/.claude/worktrees/agent-a1ea4b71aa06a03ee'
OLD = '/tmp/claude-0/-home-user-Yonghoon-DEM-DFT/81c0ad95-542f-503b-9cf7-2f6a678a4b5b/scratchpad/rcaA2/old_a76/scripts'
sys.path.insert(0, WT + '/scripts')
spec = importlib.util.spec_from_file_location('b6t', WT + '/scripts/test_ca_ext_b6.py')
B6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(B6)


def leaves(a, b, path='', out=None):
    out = [] if out is None else out
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(f'{path}.{k} ({"new only" if k not in a else "old only"})')
            else:
                leaves(a[k], b[k], f'{path}.{k}', out)
    elif isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        for i, (x, y) in enumerate(zip(a, b)):
            leaves(x, y, f'{path}[{i}]', out)
    elif json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True):
        out.append(f'{path}: {json.dumps(a)[:90]} -> {json.dumps(b)[:90]}')
    return out


arms = [('off LEAN2', B6.OFF + B6.LEAN2), ('centerline LEAN2', ['--ptfe-stamp', 'centerline'] + B6.LEAN2),
        ('off LEAN3', B6.OFF + B6.LEAN3), ('face_alpha LEAN2', ['--ptfe-stamp', 'face_alpha'] + B6.LEAN2),
        ('off LEAN2 + rtol 1e-12', B6.OFF + B6.LEAN2 + ['--step3-rtol', '1e-12']),
        ('face_alpha LEAN2 + rtol 1e-12', ['--ptfe-stamp', 'face_alpha'] + B6.LEAN2 + ['--step3-rtol', '1e-12']),
        ('off LEAN2 (collector on)', B6.OFF + [x for x in B6.LEAN2 if x != '--no-collector']),
        ('off LEAN2 + junction (quantitative) [ON — expected to differ]', B6.OFF + B6.LEAN2 + B6.CJ)]
td = tempfile.mkdtemp(prefix='pbid_')
res = []
try:
    os.makedirs(os.path.join(td, 'w'))
    d = B6.make_fixture(os.path.join(td, 'w'), sdcp=True)
    for i, (nm, extra) in enumerate(arms):
        if os.environ.get('ONLY_LAST') and i != len(arms) - 1:
            continue
        ro = B6.run_payload(d, extra, out=f'old_{i}.json', payload=os.path.join(OLD, 'mpm_webapp_payload.py'))
        rn = B6.run_payload(d, extra, out=f'new_{i}.json')
        mo, mn = dict(B6.man_of(ro[2])), dict(B6.man_of(rn[2]))
        for k in ('code_sha', 'exec_env'):
            mo.pop(k, None)
            mn.pop(k, None)
        so = {k: v for k, v in B6.s3_of(ro[2]).items() if k != 'manifest'}
        sn = {k: v for k, v in B6.s3_of(rn[2]).items() if k != 'manifest'}
        lm, ls = leaves(mo, mn, 'manifest'), leaves(so, sn, 'step3')
        row = {'arm': nm, 'rc': (ro[0], rn[0]), 'manifest_same': json.dumps(mo, sort_keys=True) == json.dumps(mn, sort_keys=True),
               'step3_same': json.dumps(so, sort_keys=True) == json.dumps(sn, sort_keys=True), 'n_manifest_keys': len(mn),
               'n_step3_keys': len(sn), 'sigma_e': (so.get('sigma_e_eff_S_cm'), sn.get('sigma_e_eff_S_cm')),
               'diff_manifest': lm[:int(os.environ.get('CAP', '14'))], 'diff_step3': ls[:8]}
        res.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
finally:
    shutil.rmtree(td, ignore_errors=True)
json.dump(res, open(sys.argv[1] if len(sys.argv) > 1 else os.devnull, 'w'), ensure_ascii=False, indent=1)

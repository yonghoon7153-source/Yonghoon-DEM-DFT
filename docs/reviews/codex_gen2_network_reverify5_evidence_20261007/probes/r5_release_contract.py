"""Independent review-only gate probes. No numeric certification and no production run.

Uses the committed detailed test fixture; only v13_reread_tau is stubbed, as in
the previous review. All release/build/check gates are unmodified source code.
"""
from pathlib import Path
import contextlib
import argparse
import copy
import io
import json
import sys
from unittest.mock import patch

R = Path(__file__).resolve().parents[1]
S = R / 'source'
ap=argparse.ArgumentParser();ap.add_argument('--output-name',default='r5_release_contract');args=ap.parse_args()
assert Path(args.output_name).name==args.output_name and args.output_name not in ('.','..')
E = R / 'evidence' / args.output_name
assert not E.exists(), 'Choose a fresh --output-name; preserve existing evidence'
E.mkdir(parents=True, exist_ok=True)
sys.path[:0] = [str(S / 'scripts'), str(S / 'webapp')]
p = S / 'scripts' / 'test_lhs_release_v13.py'
ns = {'__file__': str(p), '__name__': 'review_fixture'}
exec(compile(p.read_text(encoding='utf8').split("print('V0  API')")[0], str(p), 'exec'), ns)
lb, rr, np = ns['LRB'], ns['G2RR'], ns['NP194']
HD = ns['make_g2_handover_dir'](str(E / 'handover'))
VERDICT = E / 'TEST_ONLY_NOT_GO.md'
VERDICT.write_text('SYNTHETIC GATE TEST ONLY. NOT A LAUNCH OR RELEASE APPROVAL.\n', encoding='utf8')


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def first_binding(a):
    return next(iter(a['import_observation']['stage_binding']['attempts'].values()))


def changed_binding_value(a):
    d = a['import_observation']['stage_binding']['attempts']
    d[next(iter(d))] = None


def missing_final(a):
    first_binding(a)['observed'].pop('scripts/parse_liggghts.py')


def wrong_count(a):
    first_binding(a)['observed']['scripts/parse_liggghts.py'] = 0


def unknown_process(a):
    first_binding(a)['observed']['scripts/unplanned.py'] = 1


def bool_count(a):
    first_binding(a)['observed']['scripts/parse_liggghts.py'] = True


def duplicate_meta(r):
    r['meta'].append(copy.deepcopy(r['meta'][0]))


def wrong_cohort(r):
    r['cases'][0]['cohort'] = 'lhsx'


variants = [
    ('control', None, None),
    ('reread_M2_false', lambda r: next(m for m in r['meta'] if m['name'].startswith('M2 ')).update(ok=False), None),
    ('reread_empty_cases', lambda r: r.update(cases=[]), None),
    ('reread_empty_checks', lambda r: r['cases'][0].update(checks=[]), None),
    ('reread_ok_integer', lambda r: r['cases'][0]['checks'][0].update(ok=1), None),
    ('reread_unknown_check', lambda r: r['cases'][0]['checks'].append(dict(name='Z99 unknown', ok=True)), None),
    ('reread_duplicate_meta', duplicate_meta, None),
    ('reread_wrong_cohort', wrong_cohort, None),
    ('reread_M3_inconsistent', lambda r: r['meta'][-1].update(read_n=193), None),
    ('observation_inner_problem', None, lambda a: a['import_observation']['problems'].append('truncated receipt')),
    ('observation_outside', None, lambda a: a['import_observation']['outside'].append('scripts/unsealed.py')),
    ('binding_attempt_missing', None, lambda a: a['import_observation']['stage_binding']['attempts'].pop(next(iter(a['import_observation']['stage_binding']['attempts'])))),
    ('binding_payload_null', None, changed_binding_value),
    ('binding_parser_absent', None, missing_final),
    ('binding_parser_zero', None, wrong_count),
    ('binding_unplanned_process', None, unknown_process),
    ('binding_count_bool', None, bool_count),
    ('observation_finalized_zero', None, lambda a: a['import_observation'].update(n_finalized=0)),
]
rows = []
with patch.object(lb, 'v13_reread_tau', lambda *a, **k: []):
    for label, rf, af in variants:
        br = Path(ns['make_batch_root'](str(E / label / 'batch')))
        r = json.loads((br / 'reread.json').read_text(encoding='utf8'))
        a = json.loads((br / 'seal_audit.json').read_text(encoding='utf8'))
        if rf:
            rf(r)
        if af:
            af(a)
        dump(br / 'reread.json', r)
        dump(br / 'seal_audit.json', a)
        out = E / label / 'release'
        stream = io.StringIO()
        row = dict(label=label, direct_gate=lb.v13_batch_gate_problems(str(br))[1])
        with contextlib.redirect_stdout(stream), contextlib.redirect_stderr(stream):
            try:
                lb.build_v13(out_dir=str(out), handover_dir=HD, batch_root=str(br), date='20991231', codex_verdict=str(VERDICT))
                row.update(build_accepted=True, check=lb.check_v13(str(out), HD))
            except Exception as ex:
                row.update(build_accepted=False, error=f'{type(ex).__name__}: {ex}')
        row['output_exists'] = out.exists()
        (E / label / 'build.log').write_text(stream.getvalue(), encoding='utf8')
        rows.append(row)
        print(json.dumps(dict(label=label, accepted=row['build_accepted'], gate_problems=len(row['direct_gate']), check=row.get('check')), ensure_ascii=False), flush=True)

    # Independently recheck a formerly valid release after its batch evidence changes.
    cb = E / 'control' / 'batch'
    co = E / 'control' / 'release'
    baseline_r = (cb / 'reread.json').read_bytes()
    baseline_a = (cb / 'seal_audit.json').read_bytes()
    mp = co / 'v13_build_manifest.json'
    baseline_m = mp.read_bytes()
    checks = []
    for label, rf, af in variants[1:]:
        r, a = json.loads(baseline_r), json.loads(baseline_a)
        if rf:
            rf(r)
        if af:
            af(a)
        dump(cb / 'reread.json', r)
        dump(cb / 'seal_audit.json', a)
        direct = lb.check_v13(str(co), HD)
        # Update only the build's evidence fingerprint cache, exactly as author V18.
        m = json.loads(baseline_m)
        m['batch_gate_files'] = lb.v13_batch_gate_files(str(cb))
        dump(mp, m)
        refreshed = lb.check_v13(str(co), HD)
        checks.append(dict(label=label, original_cache=direct, refreshed_cache=refreshed))
        cb.joinpath('reread.json').write_bytes(baseline_r)
        cb.joinpath('seal_audit.json').write_bytes(baseline_a)
        mp.write_bytes(baseline_m)
    restored = lb.check_v13(str(co), HD)

# Actual submitted detailed producer records: no path translation is needed for
# the within-record detail contract; do not mistake this for full provenance QA.
submitted = []
for rel in ('submitted/g2rr5_839dbac6b_1007_2224/old_reread.json',
            'submitted/g2pre_pilot_839dbac6b_1007_2224/reread.json'):
    rec = json.loads((R / rel).read_text(encoding='utf8'))
    exp = np.registered_id_set('pilot3')['pairs']
    submitted.append(dict(path=rel, meta=len(rec['meta']), cases=len(rec['cases']), n_fail=rec['n_fail'],
                          problems=rr.launcher_detail_problems(rec, exp)))
result = dict(scope=__doc__, variants=rows, rechecks=checks, control_restored=restored, actual_submitted_detail=submitted)
dump(E / 'results.json', result)
print(json.dumps(dict(result=str(E / 'results.json'), submitted=submitted, control_restored=restored), ensure_ascii=False), flush=True)

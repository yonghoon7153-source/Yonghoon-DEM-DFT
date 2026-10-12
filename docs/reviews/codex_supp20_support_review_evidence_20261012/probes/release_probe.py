"""Independent actual build/check probe, source tree read-only.

The supplied test's fixture helpers construct synthetic G2 handovers and batch
evidence. As in V21, ONLY the build's tau reread is stubbed: real lhss G2 values
do not exist in this review. The real build, per-batch/cross gates, CSV/profile,
ML/refit and check_v13 implementations execute unmodified. All check calls run
with the real tau function restored (check does not call it).
"""
from pathlib import Path
import contextlib
import copy
import csv
import io
import json
import os
import sys
import tempfile

R = Path(__file__).resolve().parents[1]
S = R / 'source'
sys.path[:0] = [str(S / 'scripts'), str(S / 'webapp')]
import lhs_release_build as LRB

T = Path(tempfile.mkdtemp(prefix='release_probe_', dir=R / 'tmp'))
E = R / 'evidence'
fixture_path = S / 'scripts' / 'test_lhs_release_v13.py'
text = fixture_path.read_text(encoding='utf-8').split('# ═══ V0 ')[0]
F = {'__file__': str(fixture_path), '__name__': 'review_fixture_helpers'}
exec(compile(text, str(fixture_path), 'exec'), F)

def capture(fn):
    try:
        return {'returned': fn()}
    except Exception as exc:
        return {'error': type(exc).__name__, 'message': str(exc)}

def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

hd = F['make_g2_handover_dir'](str(T / 'handover'))
b194 = F['make_batch_root'](str(T / 'batch194'))
bsup = F['make_supp_batch_root'](str(T / 'batch_supp'))
bother = F['make_supp_batch_root'](
    str(T / 'batch_supp_other_code'),
    alter={'scripts/lhs_release_build.py': F['_sha_file']('scripts/lhs_release_build.py')})
verdict = T / 'TEST_ONLY_NOT_GO.md'
verdict.write_text('# TEST ONLY: fixture marker, not a production GO\n', encoding='utf-8')
out = T / 'release'
results = {'pin': 'b429c3c1df0956d2721861d89cc29a2d56f2b581',
           'limitations': __doc__, 'tau_stub_calls': []}
old = LRB.v13_reread_tau
LRB.v13_reread_tau = lambda ds, root, rows, gen: results['tau_stub_calls'].append([ds, root, len(rows), gen]) or []
try:
    results['baseline_build'] = capture(lambda: LRB.build_v13(
        out_dir=str(out), handover_dir=hd, batch_root=b194, supp_batch_root=bsup,
        date='20991231', codex_verdict=str(verdict)))
    results['normal_build_different_fp'] = capture(lambda: LRB.build_v13(
        out_dir=str(T / 'must_not_build_other_fp'), handover_dir=hd,
        batch_root=b194, supp_batch_root=bother, date='20991231', codex_verdict=str(verdict)))
finally:
    LRB.v13_reread_tau = old

mp = out / LRB.V13_MANIFEST_NAME
if not mp.exists():
    dump(E / 'release_probe.json', results)
    raise SystemExit('baseline build failed: see release_probe.json')
baseline = json.loads(mp.read_text(encoding='utf-8'))
results['baseline_check'] = capture(lambda: LRB.check_v13(str(out), hd))
results['baseline_counts'] = {k: baseline[k] for k in ('datasets', 'rows', 'n_total')}
results['original194_projection_bytes'] = {}
for ds in ('lhs', 'lhsx'):
    hp194 = Path(hd) / f'{ds}_handover_v13_20991231.csv'
    for kind, suffix, appendix in (('main', '', False), ('physics', '_physics', True)):
        solo = T / f'solo_{ds}{suffix}'
        LRB.build(str(hp194), LRB.v13_columns(ds, kind), str(solo), appendix=appendix,
                  profile='ml_v1', expect_ids=str(S / LRB.V13_INPUTS[ds]['expect_ids']))
        released = out / f'{ds}_release_20991231_v13{suffix}'
        for extension in ('.csv', '_columns.tsv'):
            results['original194_projection_bytes'][f'{ds}{suffix}{extension}'] = (
                Path(str(solo) + extension).read_bytes() == Path(str(released) + extension).read_bytes())
summary = json.loads((out / 'lhs_v13_refit_porosity_sigma_cn_summary.json').read_text(encoding='utf-8'))
results['synthetic_refit_counts'] = {k: summary[k] for k in ('n_total', 'n_fit', 'n_fit_by_dataset')}
results['synthetic_refit_counts']['reference194'] = {k: summary['reference_without_supp'][k] for k in ('n_total', 'n_fit', 'n_fit_by_dataset')}

def check_mutation(name, edit):
    m = copy.deepcopy(baseline)
    edit(m)
    dump(mp, m)
    results[name] = capture(lambda: LRB.check_v13(str(out), hd))
    dump(T / (name + '_manifest.json'), m)
    dump(mp, baseline)

check_mutation('missing_cross_root', lambda m: m['batches']['supp20'].update(root=str(T / 'does_not_exist')))
check_mutation('missing_supp_code_identity', lambda m: m['supp_batch'].pop('code_identity'))
check_mutation('missing_primary_code_identity', lambda m: m.pop('code_identity'))
check_mutation('unauthorized_supp_code_change', lambda m: m['supp_batch']['code_identity'].update(sealed_changed=['webapp/app.py'], allowed=[]))

gate, warnings = LRB.v13_batch_gate_check(bother, expect_set='supp20')
replacement = {'batch_gate': {k: v for k, v in gate.items() if k != 'files'},
               'batch_gate_files': gate['files'],
               'batch_manifest': {'path': str(Path(bother) / 'manifest.json'),
                                  'sha256': LRB._sha256(str(Path(bother) / 'manifest.json')),
                                  'expected_network_generation': 'g2'},
               'code_identity': LRB.v13_seal_gate(str(Path(bother) / 'manifest.json'))[0]}
results['other_supp_gate'] = capture(lambda: LRB.v13_batch_gate_problems(bother, 'supp20')[1])
results['actual_cross_problem'] = LRB.v13_cross_batch_problems({'production194': b194, 'supp20': bother})[1]
results['fps'] = {'production194': LRB.v13_batch_identity(b194)[0]['seal_fp'],
                  'supp_original': LRB.v13_batch_identity(bsup)[0]['seal_fp'],
                  'supp_replacement': LRB.v13_batch_identity(bother)[0]['seal_fp']}
check_mutation('different_fp_gate_original_cross_roots', lambda m: m.update(supp_batch=replacement))

def replace_and_point(m):
    m['supp_batch'] = replacement
    m['batches']['supp20']['root'] = bother
check_mutation('different_fp_gate_matching_cross_root', replace_and_point)

def replace_and_hide(m):
    m['supp_batch'] = replacement
    m['batches']['supp20']['root'] = str(T / 'does_not_exist')
check_mutation('different_fp_gate_missing_cross_root', replace_and_hide)

# Source provenance checks: alter handover-only data, keep distribution untouched.
hp = Path(hd) / 'lhss_handover_v13_20991231.csv'
original_handover = hp.read_bytes()
with hp.open(encoding='utf-8', newline='') as f:
    rows = list(csv.reader(f))
ix = rows[0].index('lhss_loading_rule')
results['handover_omitted_source_column'] = rows[0][ix]
rows[1][ix] = 'CORRUPT_SOURCE_BINDING'
with hp.open('w', encoding='utf-8', newline='') as f:
    csv.writer(f, lineterminator='\n').writerows(rows)
results['changed_source_only_handover_check'] = capture(lambda: LRB.check_v13(str(out), hd))
results['changed_handover_sha'] = {'manifest': baseline['handover']['lhss']['sha256'], 'actual': LRB._sha256(str(hp))}
hp.write_bytes(original_handover)

pv = hp.with_name(hp.stem + '_tau_provenance.tsv')
pv_bytes = pv.read_bytes()
with pv.open(encoding='utf-8', newline='') as f:
    pvs = list(csv.reader(f, delimiter='\t'))
check_ix = pvs[0].index('same_generation_checks')
pvs[1][check_ix] = 'INVALID_PROVENANCE'
with pv.open('w', encoding='utf-8', newline='') as f:
    csv.writer(f, delimiter='\t', lineterminator='\n').writerows(pvs)
results['changed_tau_provenance_check'] = capture(lambda: LRB.check_v13(str(out), hd))
results['changed_tau_provenance_build'] = capture(lambda: LRB.build_v13(
    out_dir=str(T / 'must_not_build_bad_provenance'), handover_dir=hd,
    batch_root=b194, supp_batch_root=bsup, date='20991231', codex_verdict=str(verdict)))
pv.write_bytes(pv_bytes)
results['restored_check'] = capture(lambda: LRB.check_v13(str(out), hd))

# Numeric fixed-loading contract: these columns are outside tau reread.
for dataset in ('lhss', 'lhs'):
    datafile = Path(hd) / f'{dataset}_handover_v13_20991231.csv'
    original = datafile.read_bytes()
    with datafile.open(encoding='utf-8', newline='') as f:
        data = list(csv.reader(f))
    ci = data[0].index('loading_mAh_cm2')
    ri = next(i for i in range(1, len(data)) if data[i][ci] != '')
    before = data[ri][ci]
    data[ri][ci] = '99'
    with datafile.open('w', encoding='utf-8', newline='') as f:
        csv.writer(f, lineterminator='\n').writerows(data)
    LRB.v13_reread_tau = lambda ds, root, rows, gen: []
    numeric_out = T / f'release_{dataset}_loading99'
    try:
        results[f'{dataset}_loading99_build'] = capture(lambda: LRB.build_v13(
            out_dir=str(numeric_out), handover_dir=hd, batch_root=b194,
            supp_batch_root=bsup, date='20991231', codex_verdict=str(verdict)))
    finally:
        LRB.v13_reread_tau = old
    results[f'{dataset}_loading99_input'] = {'case': data[ri][0], 'before': before, 'after': '99'}
    if numeric_out.exists():
        results[f'{dataset}_loading99_check'] = capture(lambda: LRB.check_v13(str(numeric_out), hd))
    datafile.write_bytes(original)

dump(E / 'release_probe.json', results)
print(json.dumps({k: v for k, v in results.items() if k not in ('limitations', 'baseline_build')}, ensure_ascii=False, indent=2))

"""Independent SUP20-01 root/allowance probes; no production or solver run.

Only fixture records are created. Real v13_prepare_batches, seal gate, batch
gate and cross gate execute without replacement. No full build is needed.
"""
from pathlib import Path
import copy
import json
import os
import sys
import tempfile

R = Path(__file__).resolve().parents[1]
S = R / 'source'
sys.path[:0] = [str(S / 'scripts'), str(S / 'webapp')]
import lhs_release_build as L

fixture_path = S / 'scripts/test_lhs_release_v13.py'
fixture_text = fixture_path.read_text(encoding='utf-8').split('# ═══ V0 ')[0]
F = {'__file__': str(fixture_path), '__name__': 'independent_release_fixture'}
exec(compile(fixture_text, str(fixture_path), 'exec'), F)
T = Path(tempfile.mkdtemp(prefix='release_extra_', dir=R / 'tmp'))
p = F['make_batch_root'](str(T / 'primary'))
s = F['make_supp_batch_root'](str(T / 'supp'))
other = F['make_supp_batch_root'](str(T / 'other_same_code'))
roots = {'production194': p, 'supp20': s}
batches, cross, warnings = L.v13_prepare_batches(roots)

def manifest_of(batches, cross):
    def evidence(b):
        return {'batch_manifest': b['manifest'], 'code_identity': b['code_identity'],
                'batch_gate': {k: v for k, v in b['gate'].items() if k != 'files'},
                'batch_gate_files': b['gate']['files']}
    m = evidence(batches['production194'])
    m['supp_batch'] = evidence(batches['supp20'])
    m['batches'] = {name: {k: b[k] for k in ('root', 'expect_set', 'datasets', 'n')}
                    for name, b in batches.items()}
    m['cross_batch'] = cross
    return m

base = manifest_of(batches, cross)
results = {'pin': 'a9422d2e772f28417a6e0a5167aaab8d987bf27a', 'scope': __doc__,
           'temp_dir': str(T), 'prepare_warnings': warnings, 'cases': {}}

def probe(name, m, accept):
    try:
        ps = L._v13_code_identity_problems(m.get('code_identity'))
        ps += L.v13_batch_gate_recheck(m)
        value = {'problems': ps, 'accepted': not ps, 'expected_accept': accept,
                 'matches_expectation': (not ps) == accept}
    except Exception as exc:
        value = {'exception': type(exc).__name__, 'message': str(exc),
                 'expected_accept': accept, 'matches_expectation': False}
    results['cases'][name] = value

probe('baseline_authority', base, True)
# Legitimate non-identical spelling: same location, not string identity.
m = copy.deepcopy(base)
for name in roots:
    m['batches'][name]['root'] = str(Path(roots[name]) / '.') + os.sep
    m['cross_batch']['roots'][name] = str(Path(roots[name]).parent / '.' / Path(roots[name]).name)
    m['cross_batch']['roots'][name] = m['cross_batch']['roots'][name].replace('\\', '/')
probe('copies_location_equivalent_spelling', m, True)
for mode in ('missing', 'null'):
    m = copy.deepcopy(base)
    for ci in (m['code_identity'], m['supp_batch']['code_identity']):
        if mode == 'missing':
            ci.pop('allowed', None)
        else:
            ci['allowed'] = None
    probe('no_changes_allowed_' + mode, m, True)

for label, value, accept in [
    ('exact_list', ['webapp/app.py'], True),
    ('empty_list', [], False),
    ('string_exact', 'webapp/app.py', False),
    ('string_superpath', 'NOT_webapp/app.py_NOT', False),
    ('list_superpath', ['NOT_webapp/app.py_NOT'], False),
    ('list_wrong_file', ['webapp/other.py'], False),
]:
    for where in ('primary', 'supp'):
        m = copy.deepcopy(base)
        ci = m['code_identity'] if where == 'primary' else m['supp_batch']['code_identity']
        ci.update(sealed_changed=['webapp/app.py'], allowed=value)
        probe('allowed_' + where + '_' + label, m, accept)

for where in ('batches', 'cross_batch'):
    m = copy.deepcopy(base)
    if where == 'batches':
        m['batches']['supp20']['root'] = other
    else:
        m['cross_batch']['roots']['supp20'] = other
    probe('other_valid_samecode_' + where, m, False)

for value in (20.0, True, '20', 19, None):
    m = copy.deepcopy(base)
    m['batches']['supp20']['n'] = value
    probe('n_' + repr(value), m, False)

# Rebinding the entire consistent evidence set to another genuine same-code
# batch remains possible and is expected: the checker is not an authenticity
# or cryptographic signature service.
b2, c2, _ = L.v13_prepare_batches({'production194': p, 'supp20': other})
probe('whole_consistent_samecode_batch', manifest_of(b2, c2), True)

# Producer-authorized spellings normalize before serialization, so list-only
# validation does not demand users type just one slash/prefix convention.
changed_file = 'scripts/lhs_release_build.py'
changed = F['make_supp_batch_root'](str(T / 'authorized_changed'), alter={changed_file: 'f' * 64})
for spelling in (changed_file, './' + changed_file, changed_file.replace('/', '\\')):
    ci, warns = L.v13_seal_gate(os.path.join(changed, 'manifest.json'), [spelling])
    results['cases']['producer_allow_' + spelling] = {
        'identity': ci, 'warnings': warns,
        'problems': L._v13_code_identity_problems(ci),
        'matches_expectation': (ci['allowed'] == [changed_file] and not L._v13_code_identity_problems(ci)),
    }

results['all_matched'] = all(v['matches_expectation'] for v in results['cases'].values())
results['n_cases'] = len(results['cases'])
(R / 'evidence/release_extra.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'n_cases': results['n_cases'], 'all_matched': results['all_matched'],
                  'failed_expectations': {k:v for k,v in results['cases'].items() if not v['matches_expectation']}}, ensure_ascii=False, indent=2))
raise SystemExit(0 if results['all_matched'] else 1)

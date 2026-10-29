"""Read-only imported-validator probes; never calls run/retry/audit/selftest/solver.

Fixture JSON and results are written only to the selected output directory. Sparse reviewed
archive has no harvest files, so these probes report targeted F1/F7 checks,
never a fabricated end-to-end launch-receipt success.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, default=HERE.parent.parent / 'repo',
                    help='Reviewed source tree containing scripts/; read only')
parser.add_argument('--out', type=Path, default=HERE,
                    help='Separate directory for synthetic fixtures and validator_results.json')
args = parser.parse_args()
REPO = args.repo.expanduser().resolve()
OUT = args.out.expanduser().resolve()
if not (REPO / 'scripts' / 'run_network_194_parallel.py').is_file():
    parser.error('--repo must contain scripts/run_network_194_parallel.py')
if OUT == REPO or OUT.is_relative_to(REPO):
    parser.error('--out must be outside the reviewed source tree')
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(REPO / 'scripts'))
import run_network_194_parallel as N
import supp20_input_receipt as S

PIN = '35f0327377a4213774010a090df4d224e50d29e1'
ALT = PIN[:-1] + ('0' if PIN[-1] != '0' else '1')
ch = N.code_hashes()
assert len(ch) == 32 and all(ch.values())
fp = N.code_fp(ch)
plan = dict(cohorts=[dict(name='lhss')],
            queue=[dict(case=f'lhss_{i:03}', cohort='lhss') for i in range(1, 21)])
dg = dict(n=20, ids_sha256=N.ids_digest((e['case'], e['cohort']) for e in plan['queue']),
          raw_sha256_table_sha256='1'*64, missing_raw_sha=[], cohort_tsv_sha256={'lhss': '2'*64})
base = dict(schema=N.SCHEMA, launch_format=N.LAUNCH_FORMAT,
            seal=dict(schema=N.LAUNCH_SEAL_SCHEMA, launch_format=N.LAUNCH_FORMAT,
                      code_fp=fp, files=len(ch), **{N.GEN_KEY: N.CURRENT_GENERATION}),
            **{N.GEN_KEY: N.CURRENT_GENERATION},
            generation_probe=dict(generation=N.CURRENT_GENERATION, problems=[], error=''),
            code_hashes=ch, code_dependency_closure=[N.CODE_FILES[0]],
            handover_code_hashes={f: N.sha256_file(N.ROOT/f) for f in N.HANDOVER_FILES},
            git=dict(sha=PIN, dirty=False), plan=plan, input_digest=dg,
            observe_imports=True, import_obs_run_id='a'*32)
assert N.launch_eligibility(base)['kind'] == 'current'

variants = [
    ('exact_full', PIN, PIN, True),
    ('lf_full', PIN+'\n', PIN, False),
    ('lf_none', PIN+'\n', None, None),
    ('lf_short', PIN+'\n', PIN[:7], False),
    ('wrong_full', ALT, PIN, False),
    ('wrong_none', ALT, None, None),
    ('wrong_short', ALT, PIN[:7], True),
    ('empty_approval', ALT, '', None),
    ('missing_sha', None, PIN, False),
    ('sha_7chars', PIN[:7], PIN, False),
]
rows = []
for name, sha, approval, expected in variants:
    m = copy.deepcopy(base)
    m['git']['sha'] = sha
    fixture = OUT / (name + '.json')
    fixture.write_text(json.dumps(m, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    r = S._Receipt()
    S._manifest_checks(r, 'F', str(fixture), 'supp20', {'code_fp': fp}, approved_sha=approval)
    checks = {c['id']: c['ok'] for c in r.checks}
    assert checks.get('F7') == expected, (name, checks)
    rows.append(dict(name=name, manifest_sha=repr(sha), approved_sha=approval,
                     eligibility=N.launch_eligibility(m)['kind'], F1=checks['F1'],
                     F7_present='F7' in checks, F7=checks.get('F7'),
                     all_failed_checks=[c['id'] for c in r.checks if not c['ok']]))

# 'current' is a format verdict; it does not attest completion or permitted retries.
states=[]
for name, edits in [
    ('no_completion_fields', {}),
    ('retry_dirty_override', {'retries':[{'allow_dirty':True, 'allow_mixed_generation':True}]}),
    ('all_cases_pending', {'status':'running', 'completed':False}),
]:
    m=copy.deepcopy(base); m.update(edits)
    states.append(dict(name=name, eligibility=N.launch_eligibility(m)['kind']))
    assert states[-1]['eligibility']=='current'

result=dict(python=sys.version, review_pin='bf8cf21c6466cdb9411f9320711b871c2d1c651e',
            launch_pin=PIN, code_fp=fp,
            source_sha256={p:hashlib.sha256((REPO/p).read_bytes()).hexdigest()
                           for p in ('scripts/run_network_194_parallel.py','scripts/supp20_input_receipt.py')},
            scope='synthetic data; real imported pure validators; no launch, solver, WSL, Bash, or git call',
            note='F2 is false because the 70-file source archive omits harvest folders; no end-to-end receipt rc is asserted.',
            rows=rows, states=states)
(OUT/'validator_results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))

"""Independent recipient data/static comparisons; no received imports or function calls."""
import ast
import collections
import hashlib
import json
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NEW = ROOT / 'received'
OLD = NEW / 'basis/source30'
PRIOR = ROOT.parent / 'normal30_native_review_20260930/received'
checks = []

def j(p):
    return json.loads(p.read_bytes())

def sha(p):
    with p.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def ck(name, value, detail=None):
    checks.append({'name': name, 'pass': bool(value), 'detail': detail})

manifest = j(NEW / 'CODE_MANIFEST.json')
mh = sha(NEW / 'CODE_MANIFEST.json')
old_manifest = j(OLD / 'CODE_MANIFEST.json')
for r in manifest['files']:
    p = NEW / r['file']
    ck('manifest:' + r['file'], p.stat().st_size == r['bytes'] and sha(p) == r['sha256'])
for r in old_manifest['files']:
    p = OLD / r['file']
    pp = PRIOR / 'candidate' / r['file']
    ck('old-source:' + r['file'], p.exists() and pp.exists() and p.read_bytes() == pp.read_bytes())
ck('old-manifest-direct-prior', (OLD / 'CODE_MANIFEST.json').read_bytes() == (PRIOR / 'candidate/CODE_MANIFEST.json').read_bytes())
ck('previous-manifest-pin', sha(OLD / 'CODE_MANIFEST.json') == manifest['previous_manifest_sha256'])

mapping = j(NEW / 'LITERAL_CHANGE_MAP.json')
for old_name, replacements in mapping.items():
    new_name = old_name.replace('Normal30Candidate.java', 'Normal60Candidate.java')
    b = (OLD / old_name).read_bytes()
    for i, r in enumerate(replacements):
        before, after = r['before'].encode('utf-8'), r['after'].encode('utf-8')
        ck(f'literal-count:{old_name}:{i}', b.count(before) == r['count'])
        b = b.replace(before, after)
    ck('forward-complete-byte-map:' + new_name, b == (NEW / new_name).read_bytes())
    for r in reversed(replacements):
        b = b.replace(r['after'].encode('utf-8'), r['before'].encode('utf-8'))
    ck('reverse-complete-byte-map:' + new_name, b == (OLD / old_name).read_bytes())

new_java = (NEW / 'src/Normal60Candidate.java').read_text(encoding='utf-8')
ck('Java-seven-declared-literal-substitutions', len(mapping['src/Normal30Candidate.java']) == 7)
ck('Java-tlist-map-is-extension-only',
   mapping['src/Normal30Candidate.java'][-1]['after'].startswith(mapping['src/Normal30Candidate.java'][-1]['before'][:-1] + ' '))

c, o = j(NEW / 'CONTRACT.json'), j(OLD / 'CONTRACT.json')
changed = sorted(k for k in c.keys() | o.keys() if c.get(k) != o.get(k))
allowed = {'run_id','root','run_root','approval_path','release_path','candidate_java','baseline_files',
           'requested_times_s','maximum_physical_s','policy','commands','future_native_blockers',
           'baseline_requested_times_s','comparison_end_s','b020_requested_times_s'}
ck('contract-changed-fields-exact', set(changed) == allowed, changed)
ck('inactive-flags', all(manifest[k] is False and c[k] is False for k in ('approved','usable')))
ck('contract-state', c['run_id'] == manifest['run_id'] == 'normal60_candidate_001' and c['maximum_physical_s'] == '60')
ts = [Decimal(v) for v in c['requested_times_s']]
ck('737-time-construction', len(ts) == 737 and len(set(ts)) == 737 and ts == sorted(ts)
   and c['requested_times_s'][:437] == o['requested_times_s']
   and ts[437:] == [Decimal(i)/10 for i in range(301, 601)])
ck('primary437-secondary187', c['baseline_requested_times_s'] == o['requested_times_s']
   and c['b020_requested_times_s'] == o['baseline_requested_times_s']
   and len(c['b020_requested_times_s']) == 187 and c['comparison_end_s'] == '30')
ck('java-tlist-contract-binding', mapping['src/Normal30Candidate.java'][-1]['after'][1:-1].split() == c['requested_times_s'])
ck('unchanged-physical-comparison-contract', all(c[k] == o[k] for k in ('coordinates','threshold_mol_m3','fresh_t0','runAll_calls','loadCopy_calls','guard_expression','domains','lagrange_order','storestopcondsol','limits','budgets_seconds','resource_proposal','guard_stop_descriptions','runtime_settings_required','parent_completion_boundary')))
ck('unchanged-external-16-pins', c['external_source_pins'] == o['external_source_pins'] and len(c['external_source_pins']) == 16)
ck('policy-changes-only-narrative', {k:v for k,v in c['policy'].items() if k != 'native_permission_status'} == {k:v for k,v in o['policy'].items() if k != 'native_permission_status'})
pins = j(NEW / 'BASELINE_IDENTITIES.json')
for family, folder in [('normal30', PRIOR / 'run/tables'), ('b020', PRIOR / 'baseline')]:
    for name, r in pins[family].items():
        p = folder / name
        ck('baseline-prior-bytes:' + family + ':' + name, p.exists() and p.stat().st_size == r['bytes'] and sha(p) == r['sha256'])
        k = name if family == 'normal30' else 'B020_' + name
        ck('baseline-contract:' + k, c['baseline_files'][k] == r)
        if family == 'b020':
            ck('unchanged-B020-pin:' + name, o['baseline_files'][name] == r)

cmd, fields = j(NEW / 'COMMAND_MAP.json'), j(NEW / 'NATIVE_APPROVAL_FIELD_SPEC.json')
for f, key in [('LIMITED_VALIDATION_PLAN.json','manifest_sha256'),('FINAL_STATIC_BINDING.json','manifest_sha256'),('STATIC_AUDIT.json','candidate_manifest_sha256'),('COMMAND_MAP.json','manifest_sha256'),('NATIVE_APPROVAL_FIELD_SPEC.json','code_manifest_sha256')]:
    ck('manifest-consumer:' + f, j(NEW / f)[key] == mh)
for phase in ('compile','batch'):
    ck('native-command-map:' + phase, cmd['native'][phase]['argv'] == c['commands'][phase] == fields['required_future_fields']['commands'][phase])
    expected = [x.replace(o['root'], c['root']).replace('Normal30Candidate', 'Normal60Candidate') for x in o['commands'][phase]]
    ck('native-command-change-only-root-class:' + phase, c['commands'][phase] == expected)
for phase in ('execute','analyze'):
    argv = cmd[phase]['argv']
    ck('entry-command-binding:' + phase, argv == ['-I','-S','-B','-X','utf8',c['root']+'/src/candidate_entry.py',phase,'--approval',c['approval_path'],'--manifest-sha',mh]
       and cmd[phase]['cwd'] == c['cwd'] and cmd[phase]['executable'] == c['python']['path'])
ck('parent-command-binding', cmd['parent']['argv'] == ['-NoLogo','-NoProfile','-NoExit','-File',c['root']+'/PARENT_COMMAND.ps1','-ManifestSha',mh]
   and cmd['parent']['cwd'] == c['cwd'] and cmd['parent']['currently_usable'] is False)
ck('approval-field-budget-binding', fields['required_future_fields']['budgets_seconds'] == c['budgets_seconds'])
ck('candidate-java-pin', c['candidate_java']['path'] == c['root']+'/src/Normal60Candidate.java' and c['candidate_java']['sha256'] == sha(NEW/'src/Normal60Candidate.java'))

function_changes = {}
for rel in ('src/candidate_entry.py','src/diagnostic_consumer.py'):
    trees = [ast.parse((base / rel).read_bytes()) for base in (OLD, NEW)]
    ds = [{x.name: ast.dump(x, include_attributes=False) for x in t.body if isinstance(x, (ast.FunctionDef, ast.ClassDef))} for t in trees]
    function_changes[rel] = sorted(k for k in ds[0].keys() | ds[1].keys() if ds[0].get(k) != ds[1].get(k))
ck('entry-changed-functions', function_changes['src/candidate_entry.py'] == ['analyze','execute','permission'])
ck('consumer-changed-functions', function_changes['src/diagnostic_consumer.py'] == ['analyze','coverage','guard_evidence','late_summary','native_stop','numeric'])
ps0, ps1 = [(base/'PARENT_COMMAND.ps1').read_bytes() for base in (OLD,NEW)]
ck('parent-BSave-BInvoke-byte-identical', ps0.split(b'function BSave',1)[1].split(b'function GDecision',1)[0] == ps1.split(b'function BSave',1)[1].split(b'function GDecision',1)[0])
ck('parent-after-GDecision-only-purpose-field', ps0.split(b'\r\ntry {',1)[1].replace(b'native30',b'native60') == ps1.split(b'\r\ntry {',1)[1])

plan = j(NEW / 'LIMITED_VALIDATION_PLAN.json')
groups = plan['groups']; cases = [x for g in groups for x in g['cases']]
counts = collections.Counter()
for g in groups:
    counts[g['engine']] += len(g['cases'])
ck('12groups46cases-distinct', len(groups) == 12 == len(set(g['id'] for g in groups)) and len(cases) == 46 == len(set(x['id'] for x in cases)))
ck('validation-budget-sum', sum(v for k,v in plan['budget_seconds'].items() if k != 'overall') == plan['budget_seconds']['overall'] == 1380)
ck('preimport-inert-and-no-retry', plan['inert_required_before_target_import'] is True and plan['first_failure_stop_no_retry'] is True and plan['harness_sha256'] is None and plan['approved'] is False and plan['usable'] is False)

before, after = j(NEW/'PRESERVATION_BEFORE.json'), j(NEW/'PRESERVATION_AFTER.json')
ck('sender39-preservation-record-consistency', len(before) == 39 and before == after == j(NEW/'FINAL_STATIC_BINDING.json')['preservation'])
static = j(NEW/'STATIC_AUDIT.json')
ck('sender66-static-not-functional', len(static['checks']) == 66 and all(x['status'] == 'STATIC_MATCH' for x in static['checks']))
ck('sender-final15-static', len(j(NEW/'FINAL_STATIC_BINDING.json')['checks']) == 15 and all(x['match'] for x in j(NEW/'FINAL_STATIC_BINDING.json')['checks']))
outer = j(ROOT/'supplement/PACKAGING_TOOL_RETURN.json')['tool_return']
stdout = json.loads(outer['output'])
arc = j(ROOT/'ARCHIVE_AUDIT.json')[0]
ck('packaging-return-source-bound', outer['exit_code'] == 0 and stdout['zip']['sha256'] == arc['sha256'] and stdout['zip']['bytes'] == arc['bytes'] and stdout['manifest_sha256'] == mh and stdout['cases_proposed'] == 46 and stdout['logical_groups_proposed'] == 12)
ck('no-real-runtime-in-archive', not any(p.startswith(('future_run_001/','future_parent_001/','future_authorizations/')) for p in [x.relative_to(NEW).as_posix() for x in NEW.rglob('*') if x.is_file()]))

result = {'scope':'Independent static and byte/data comparisons, not candidate functional tests. No received import/execution.',
          'status':'PASS' if all(x['pass'] for x in checks) else 'REVIEW_REQUIRED',
          'candidate_manifest_sha256':mh,'checks':checks,'check_count':len(checks),
          'function_ast_changes':function_changes,'proposed_cases_by_engine':dict(counts),
          'remote_preservation_scope':'39 sender-record entries; not direct remote verification.',
          'candidate_functions_executed':0,'COMSOL_calls':0,'native_approval':False}
(ROOT/'STATIC_DATA_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':result['status'],'check_count':len(checks),'failed':[x for x in checks if not x['pass']],'case_counts':dict(counts),'function_changes':function_changes},ensure_ascii=False,indent=2))

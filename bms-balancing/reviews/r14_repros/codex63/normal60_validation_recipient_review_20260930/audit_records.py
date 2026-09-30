"""Recipient byte/JSON reconciliation only. Never imports received modules."""
from pathlib import Path
import hashlib
import json
import re
from collections import Counter

R = Path(__file__).resolve().parent
P = R / 'received'
S = R / 'supplement'
OLD = R.parent / 'normal60_preparation_review_20260930' / 'received'
V3 = Path('C:/Users/Administrator/Desktop/CLAUDE_REPLY_NORMAL30_LONG_HORIZON_KO_v3.md')
checks = []

def read(p):
    return json.loads(p.read_bytes())

def ident(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def check(name, ok, detail=None):
    checks.append({'check': name, 'pass': bool(ok), 'detail': detail})

def matches(p, claim):
    return ident(p) == {k: claim[k] for k in ('bytes', 'sha256')}

def mapped(path):
    path = path.replace('\\', '/')
    for marker, base in (
        ('/normal60_offline_preparation_20260930/', P / 'candidate'),
        ('/normal60_validation_attempt_02_20260930/', P),
    ):
        if marker in path:
            return base / path.split(marker, 1)[1]
    return None

inputs = [Path('C:/Users/Administrator/Downloads') / n for n in (
    'COMSOL63_NORMAL60_LIMITED_VALIDATION_COMPLETE_20260930.zip',
    'NORMAL60_VALIDATION_DELIVERY_SUPPLEMENT_20260930.zip')]
inputs.append(V3)
before = {str(p): ident(p) for p in inputs}

manifest = read(P / 'candidate/CODE_MANIFEST.json')
mh = ident(P / 'candidate/CODE_MANIFEST.json')['sha256']
check('candidate_manifest_fixed', mh == '82e556243b29b10ae65b95dcdff7f854734b6f1cfffc1881327cab1939ebe5c8')
for row in manifest['files']:
    p = P / 'candidate' / row['file']
    check('manifest_payload:' + row['file'], matches(p, row))
    check('prior_candidate_exact_bytes:' + row['file'], p.read_bytes() == (OLD / row['file']).read_bytes())
for name in ('CODE_MANIFEST.json', 'LIMITED_VALIDATION_PLAN.json'):
    check('prior_candidate_exact_bytes:' + name, (P / 'candidate' / name).read_bytes() == (OLD / name).read_bytes())
check('manifest_inactive', manifest['approved'] is False and manifest['usable'] is False)

seal = read(P / 'PRE_TEST_SEAL.json')
after_seal = read(P / 'PRESERVATION_AFTER.json')
check('pre_post_seal_exact_list', seal['files'] == after_seal)
verified_local = 0
engine_claims = []
for row in seal['files']:
    p = mapped(row['path'])
    if p is None:
        engine_claims.append(row)
    else:
        verified_local += 1
        check('pre_test_seal_payload:' + str(p.relative_to(P)), matches(p, row))

planned = read(P / 'CASE_FIXTURE_SEAL.json')['cases']
summary = read(P / 'CASE_RECONCILIATION.json')
py = read(P / 'records/PYTHON_RESULT.json')
ps = read(P / 'records/PS_RESULT.json')
final = read(P / 'FINAL_STATUS.json')
java_out = (P / 'records/jvm_STDOUT.txt').read_text('utf-8')
java_ids = re.findall(r'^(J\d+-\d+) PASS$', java_out, re.M)
actual = py['results'] + ps['results'] + [{'id': i, 'status': 'PASS'} for i in java_ids]
plan_ids = [x['id'] for x in planned]
actual_ids = [x['id'] for x in actual]
check('46_unique_cases_exact_set', len(actual_ids) == len(set(actual_ids)) == 46 and set(actual_ids) == set(plan_ids))
check('12_logical_groups', len(set(x.split('-')[0] for x in actual_ids)) == 12)
check('all_reported_case_status_pass', all(x['status'] == 'PASS' for x in actual))
check('summary_case_set_and_count', set(x['id'] for x in summary['rows']) == set(actual_ids) and summary['cases'] == 46)
check('engine_case_counts', len(py['results']) == 27 and len(ps['results']) == 15 and len(java_ids) == 4)
check('final_declared_counts', final['counts'] == {'Python': 27, 'Java_helper': 4, 'PowerShell51': 15})
check('python_bound_candidate', py['manifest'] == mh)
for row in py['results']:
    check('python_checkpoint:' + row['id'], read(P / 'records' / ('case_' + row['id'] + '.json')) == row)

ex = read(P / 'EXTRACTED_SOURCES.json')
method = ex['Java_method']
java_source = (P / 'candidate/src/Normal60Candidate.java').read_text('utf-8')
helper = (P / 'tests/ShapeHarness.java').read_text('utf-8')
check('java_method_source_and_harness', method in java_source and method in helper)
check('java_method_lf_digest', hashlib.sha256(method.encode()).hexdigest() == ex['Java_method_utf8_lf_sha256'])
gbytes = (P / 'tests/GDecision.txt').read_bytes()
check('powershell_exact_extraction', gbytes in (P / 'candidate/PARENT_COMMAND.ps1').read_bytes() and ps['extracted_source'].encode('utf-8') == gbytes)
check('powershell_actual_engine51', ps['engine'] == '5.1.26100.9444')
check('java_helper_engine11', 'JAVA_VERSION=11.0.24' in java_out)
class_bytes = (P / 'classes/ShapeHarness.class').read_bytes()
check('helper_class_header55', class_bytes[:4] == bytes.fromhex('cafebabe') and int.from_bytes(class_bytes[6:8], 'big') == 55)
cfg = read(P / 'candidate/CONTRACT.json')
check('time_request_counts', len(cfg['requested_times_s']) == 737 and len(cfg['baseline_requested_times_s']) == 437 and len(cfg['b020_requested_times_s']) == 187)
check('native_future_inactive', cfg['approved'] is False and cfg['usable'] is False and final['approved'] is False and final['usable'] is False)

cache = sorted((P / 'records').glob('profile_cache_*.json'))
modes = Counter()
seen_original = set()
for path in cache:
    record = read(path)
    modes[record['mode']] += 1
    cur = mapped(record['current']['path'])
    check('cache_current_identity:' + path.name, matches(cur, record['current']))
    check('cache_reader_identity:' + path.name, matches(mapped(record['production_reader_source']['path']), record['production_reader_source']))
    raw = cur.read_bytes()
    check('cache_complete_row_boundary:' + path.name, raw.endswith(b'\n') and raw.count(b'\n') == 1 + 241 * record['time_count'])
    if record['mode'] == 'ORIGINAL_PROFILE_VALIDATOR':
        seen_original.add(record['current']['sha256'])
    else:
        src = record['validated_full_source']
        check('cache_earlier_source_and_exact_prefix:' + path.name, src['sha256'] in seen_original and matches(mapped(src['path']), src) and mapped(src['path']).read_bytes().startswith(raw))
check('18_cache_records_bound_result', [read(p) for p in cache] == py['profile_cache_records'])
check('cache_scope_counts', dict(modes) == {'ORIGINAL_PROFILE_VALIDATOR': 2, 'EXACT_VALIDATED_PREFIX_REUSE': 16})

for i, n in enumerate(('positive_result.json', 'protected_25_result.json', 'protected_45_result.json'), 1):
    obs = py['results'][i - 1]['observations'][0]
    p = mapped(obs['result']['path'])
    check('entry_output_identity:' + str(i), matches(p, obs['result']))
    check('entry_output_consumed_copy:' + str(i), read(p) == read(P / 'records' / n))
    check('entry_rc:' + str(i), obs['entry_rc'] == (0 if i == 1 else 1))

tools = read(P / 'TOOL_RETURNS.json')['returns']
commands = read(P / 'COMMANDS.json')
stages = []
prev_end = 0.0
for phase, key in [('python','python_return'), ('compile','compile_return'), ('jvm','jvm_return'), ('powershell','ps_return')]:
    ext = read(P / 'records' / (phase + '_EXTERNAL_RETURN.json'))
    res = read(P / 'records' / (phase + '_RESERVATION.json'))
    host = tools[key]
    check('stage_binding:' + phase, ext == final['stages'][phase] == json.loads(host['output']) and ext['command'] == res['command'] == commands[phase])
    check('stage_exit_budget_order:' + phase, ext['status'] == 'PASS' and ext['rc'] == host['exit_code'] == 0 and not ext['timeout'] and ext['elapsed_seconds'] <= ext['command']['timeout_seconds'] and prev_end <= res['overall_seconds'] <= ext['overall_seconds'] <= 1380)
    check('stage_stderr_empty:' + phase, (P / 'records' / (phase + '_STDERR.txt')).stat().st_size == 0)
    prev_end = ext['overall_seconds']
    stages.append({'phase': phase, 'elapsed_seconds': ext['elapsed_seconds'], 'host_chunk': host['chunk_id'], 'host_rc': host['exit_code']})

failure = P / 'previous_failed_attempt/FIRST_FAILURE.json'
check('first_failure_unchanged_pin', ident(failure)['sha256'] == '71a066220530be20eed1e72c6ab361e8871de535ff3314557c455eecae1134e3')
oldfail = read(failure)
check('first_failure_timeout_retained', oldfail['first_failure']['timeout'] is True)

receipt = read(S / 'DELIVERY_RECEIPT.json')
pack = read(S / 'PACKAGING_TOOL_RETURN.json')
close = read(S / 'DELIVERY_CLOSEOUT.json')
packout = json.loads(pack['completion']['output'])
check('main_zip_finish_identity', matches(inputs[0], packout['zip']) and matches(inputs[0], close['main_zip']))
check('closeout_linked_receipt_and_return', matches(S / 'DELIVERY_RECEIPT.json', close['receipt']) and matches(S / 'PACKAGING_TOOL_RETURN.json', close['tool_return']))
check('main_packaging_rc_budget', pack['completion']['exit_code'] == 0 and packout['within_limits'] and packout['post_receipt_overall_seconds'] < 1380 and packout['post_receipt_package_seconds'] < 300)
check('closeout_snapshot_order_budget', packout['post_receipt_overall_seconds'] <= close['overall_snapshot_seconds'] <= 1380)
check('closeout_boundary_explicit', 'before supplement ZIP write' in close['time_scope'])
check('delivery_receipt_generation_unmodified', receipt['recipient'] is None)

check('review_inputs_preserved', before == {str(p): ident(p) for p in inputs})
report = {
    'scope': 'Recipient byte/JSON and static source audit; no received code, tests, Java, COMSOL or native60 executed',
    'status': 'PASS' if all(x['pass'] for x in checks) else 'REVIEW_SCRIPT_CHECK_FAILED',
    'data_checks_not_functional_tests': len(checks),
    'failed_checks': [x for x in checks if not x['pass']],
    'checks': checks,
    'inputs': before,
    'candidate_manifest_sha256': mh,
    'pretest_seal_included_files_verified': verified_local,
    'sender_engine_file_identity_claims_not_independently_remeasured': engine_claims,
    'engine_stages': stages,
    'profile_cache_modes': modes,
    'functional_results_scope': '27 Python / 4 extracted Java helper / 15 extracted PowerShell5.1 function cases. No new recipient functional test.',
    'delivery_boundary': {'main_post_receipt_overall_s': packout['post_receipt_overall_seconds'], 'main_package_s': packout['post_receipt_package_seconds'], 'closeout_snapshot_s': close['overall_snapshot_seconds'], 'supplement_final_host_return_supplied': False, 'note': close['time_scope']},
    'native60_approved': False,
}
(R / 'EVIDENCE_AUDIT.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: report[k] for k in ('status', 'data_checks_not_functional_tests', 'failed_checks', 'candidate_manifest_sha256', 'pretest_seal_included_files_verified', 'profile_cache_modes', 'delivery_boundary')}, ensure_ascii=False))
if report['status'] != 'PASS':
    raise SystemExit(1)

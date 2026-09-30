"""Reviewer-only data checks: units, log markers, external return boundaries."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R = ROOT / 'received'
S = ROOT / 'supplement'
T = R / 'run/tables'
checks = []

def check(name, ok):
    checks.append({'check': name, 'pass': bool(ok)})
    assert ok, name

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def identity(p):
    with p.open('rb') as f:
        return {'bytes': p.stat().st_size, 'sha256': hashlib.file_digest(f, 'sha256').hexdigest()}

units = {
 'eguard':['s']+['mol/m^3']*5+['1']*3,
 'nglobal':['s']+['mol/m^2']*3+['1']*7+['A/m^2']*3,
 'point1':['s','V','V','V','V','V','1','1','mol/m^3','mol/m^3','mol/m^3','V','A/m^2'],
 'point4':['s','V','V','V','V','V','1','1','mol/m^3','mol/m^3','mol/m^3','V','A/m^2'],
 'MinLinece':['s','mol/m^3'], 'MaxLinece':['s','mol/m^3'],
 'profiletimes':['s'], 'profileN':['s','m','1','1','V','V','V','1'],
 'profileP':['s','m','1','1','V','V','V','1']}
for tag, expected in units.items():
    for phase in (['inferred','configured','evaluated'] if tag == 'eguard' else ['configured','evaluated']):
        a = expected.copy()
        if phase != 'configured':
            for i in ([6,7,8] if tag == 'eguard' else [10] if tag == 'nglobal' else [7] if tag in ['profileN','profileP'] else []):
                a[i] = ''
        value = '[' + ', '.join(a) + ']'
        with (T / f'units_{tag}_{phase}.csv').open(encoding='utf-8-sig', newline='') as f:
            rows = list(csv.DictReader(f))
        check(tag + ' ' + phase, rows == [{'tag':tag, 'phase':phase, 'expected':value, 'actual':value}])

markers = [
 'AXES_PHYSICAL_MESH_DOMAIN=1|numelem=120',
 'AXES_PHYSICAL_MESH_DOMAIN=2|numelem=60',
 'AXES_PHYSICAL_MESH_DOMAIN=3|numelem=120',
 'AXES_PARTICLE=pce1|Nel=320|Nord=1|Distribution=CubicRoot',
 'AXES_PARTICLE=pce2|Nel=320|Nord=1|Distribution=CubicRoot',
 'AXES_ACTUAL_MESH=mesh1|edges=300|vertices=301',
 'PREFLIGHT_SOLVE_BEGIN=0..120 seconds; NO full protocol or sweep',
 'ELECTROLYTE_THRESHOLD_EXPRESSION=0[mol/m^3]',
 'ELECTROLYTE_THRESHOLD_SI=0.0']
counts = dict.fromkeys(markers, 0)
with (R / 'run/batch_console.log').open(encoding='utf-8-sig') as f:
    for line in f:
        if line.strip() in counts:
            counts[line.strip()] += 1
for k, v in counts.items():
    check(k, v == 1)
java = (R / 'candidate/src/Normal120Candidate.java').read_text(encoding='utf-8-sig')
check('one textual runAll call', java.count('.runAll();') == 1)
ps = (R / 'candidate/PARENT_COMMAND.ps1').read_text(encoding='utf-8-sig')
stop = 'STOP. No rerun, cleanup fallback, policy toggle or additional solve. Preserve this output.'
check('reported STOP is literal parent instruction', stop in ps)

post = read(S / 'POST_WRITE_USER_RETURN.json')
raw_line = post['raw_user_text'].splitlines()[0]
check('declared one-opening-brace normalization only', json.loads('{' + raw_line) == post['value'])
value = post['value']
check('user return identifies final boundary bytes', {k:value['boundary'][k] for k in ['bytes','sha256']} == identity(R/'parent/FINAL_BOUNDARY.json'))
boundary = read(R / 'parent/FINAL_BOUNDARY.json')
check('post-write follows pre-write', value['snapshot_seconds'] >= boundary['elapsed_seconds'] == value['pre_write_seconds'])
check('post-write budget and error list', value['snapshot_seconds'] <= 5100 and value['delivery_elapsed_seconds'] <= 300 and value['within_limits'] and value['record_errors'] == [])
check('NoExit boundary does not invent process rc', value['raw_host_rc'] is None and boundary['raw_host_rc'] is None and value['host_boundary'] == 'SCRIPT_FINAL_RECORD_NOT_PROCESS_EXIT')

archives = read(ROOT / 'ARCHIVE_AUDIT.json')
main, supplement = archives
ret = read(ROOT / 'USER_SUPPLIED_FINAL_RETURN.json')['result']
out = json.loads(ret['output'])
check('last supplied external return rc0 with explicit provenance', ret['exit_code'] == 0 and ret['chunk_id'] == 'ed5452' and out['status'] == 'SUPPLEMENT_VERIFIED')
check('last return binds actual supplemental bytes', all(out['supplement'][k] == supplement[k] for k in ['bytes','sha256']))
check('last return still generation recipient null', out['recipient'] is None)
check('last snapshot source is before tool return', out['scope'] == 'After supplement readback, before tool return')
pack = read(S / 'PACKAGING_TOOL_RETURN.json')['completion']
pout = json.loads(pack['output'])
check('main packaging rc and raw identity', pack['exit_code'] == 0 and all(pout['zip'][k] == main[k] for k in ['bytes','sha256']))
check('main packaging native counts', pout['stored_count'] == 2140 and pout['profile_rows'] == 1031480 and pout['payloads'] == 5332)

prior = read(R / 'preexec/SUPPLEMENT_LAST_RETURN_ADDENDUM.json')
p_ret = prior['tool_response']
p_out = p_ret['parsed_output']
prior_audit_path = ROOT.parent / 'normal120_validation_review_20260930/ARCHIVE_AUDIT.json'
prior_audit = read(prior_audit_path)[1]
check('prior validation supplied final return matches historical recipient audit identity', {k:prior_audit[k] for k in ['bytes','sha256']} == {k:p_out['supplement'][k] for k in ['bytes','sha256']})
check('prior validation final return rc0 and snapshot within 1500', p_ret['exit_code'] == 0 and p_ret['chunk_id'] == '7ad24f' and p_out['overall_post_supplement_snapshot_seconds'] <= 1500)
check('prior validation return not new native approval', prior['new_native_authorization'] is False and p_out['native120_approved'] is False)

result = {
 'status':'PASS', 'checks':checks, 'check_count':len(checks),
 'scope':'Reviewer data checks, not functionality tests or new sender execution.',
 'final_return_provenance':'Current user message transcribed by reviewer; not independently observed sender host call.',
 'prior_validation_boundary':'Additional historical transcription matches prior recipient archive-audit identity, not a fresh rehash of the prior ZIP; no historical receipt changed.',
 'prior_recipient_audit':{'path':str(prior_audit_path), **identity(prior_audit_path), 'supplement_record':prior_audit},
 'parent_boundary':'User-console script final record with null outer PowerShell process rc.',
 'final_return_call_wall_seconds':ret['wall_time_seconds'],
 'final_return_snapshot_seconds':out['elapsed_seconds'],
 'native_post_write_seconds':value['snapshot_seconds'],
 'separate_collection_post_receipt_seconds':pout['post_receipt_snapshot_seconds']
}
(ROOT/'SUPPLEMENTAL_AUDIT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'PASS','checks':len(checks)},ensure_ascii=False))

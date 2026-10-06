"""Read-only comparison of two supplied ZIP containers. No supplied code is executed."""
import hashlib
import json
import stat
import zipfile
from pathlib import Path, PurePosixPath

A = Path(r'C:/Users/Administrator/Downloads/BMIN150_EXISTING_AFTER_RECORDS_20261007.zip')
B = Path(r'C:/Users/Administrator/Downloads/BMIN150_DELIVERY_AFTER_SUPPLEMENT_20261007.zip')
PRIOR = Path('outputs/bmin150_preservation_closeout_review_20261007/CHECK_RESULT.json')
DECISION = Path('outputs/bmin150_preservation_closeout_review_20261007/DECISION.json')
SHARED = ['SELECTED_SOURCES_AFTER.json', 'DELIVERY_RECEIPT.json', 'FINAL_PACKAGE_TOOL_RETURN.json']

def identify(b):
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def parse(b):
    def unique(items):
        out = {}
        for k, v in items:
            if k in out:
                raise ValueError('Duplicate JSON key: ' + k)
            out[k] = v
        return out
    return json.loads(b.decode('utf-8-sig'), object_pairs_hook=unique)

errors = []
def check(label, value):
    if not value:
        errors.append(label)

containers = {}
raws = {}
for label, p in [('previous', A), ('additional', B)]:
    whole = p.read_bytes()
    with zipfile.ZipFile(p) as z:
        names = z.namelist()
        check(label + ':unique', len(names) == len(set(names)) == len({n.casefold() for n in names}))
        check(label + ':paths', all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n and ':' not in n for n in names))
        check(label + ':no_links', all(not stat.S_ISLNK(e.external_attr >> 16) for e in z.infolist()))
        data = {n: z.read(n) for n in names}
        manifest = parse(data['PACKAGE_MANIFEST.json'])
        check(label + ':exact_set', set(names) == {'PACKAGE_MANIFEST.json'} | {r['file'] for r in manifest['files']} and len(names) == len(manifest['files']) + 1)
        ids = {n: identify(b) for n, b in data.items()}
        for r in manifest['files']:
            check(label + ':pin:' + r['file'], ids[r['file']] == {'bytes': r['bytes'], 'sha256': r['sha256']})
        containers[label] = {'filename': p.name, **identify(whole), 'entries': len(names), 'members': ids, 'crc_all_members_read_to_eof': True}
        raws[label] = data

prior = parse(PRIOR.read_bytes())
check('previous_sup_identity', {k: containers['previous'][k] for k in ('bytes','sha256')} == prior['supplement_identity'])
check('prior_no_errors', prior['errors'] == [] and prior['selected_before_count'] == prior['selected_after_count'] == 8674 and prior['path_set_equal'] is True and prior['changed'] == [])
check('previous_decision_identity', identify(DECISION.read_bytes())['sha256'] == 'c088ca3506978b3a93d5c96d9761af1b369ff574bfc6119eb0486bf740711662')
comparison = []
for n in SHARED:
    same = raws['previous'][n] == raws['additional'][n]
    check('shared_bytes:' + n, same)
    check('prior_accepted_pin:' + n, identify(raws['additional'][n]) == prior['supplement_members'][n])
    comparison.append({'file': n, **identify(raws['additional'][n]), 'byte_for_byte_equal': same})

check('only_extra_cover_letter', set(raws['additional']) - set(raws['previous']) == {'SEND_TO_REVIEWER_KO.md'} and not (set(raws['previous']) - set(raws['additional'])))
check('manifest_rebuilt_not_original_record', raws['previous']['PACKAGE_MANIFEST.json'] != raws['additional']['PACKAGE_MANIFEST.json'])
result = {
    'status': 'SAME_ACCEPTED_RECORDS_CLOSURE_UNCHANGED' if not errors else 'REVIEW_REQUIRED',
    'errors': errors,
    'containers': containers,
    'shared_records': comparison,
    'additional_document': 'SEND_TO_REVIEWER_KO.md',
    'container_manifest_differs': True,
    'selected_preservation_count_from_unchanged_accepted_record': 8674,
    'previous_closeout_decision_identity': identify(DECISION.read_bytes()),
    'previous_check_result_identity': identify(PRIOR.read_bytes()),
    'received_code_execution': 0,
    'COMSOL_calls': 0,
    'numeric_recalculation': 0,
    'remote_source_remeasurement': False,
    'note': 'Two containers carry the same three historical records; they are not two independent preservation observations. New cover letter and container manifest do not change the underlying accepted evidence.'
}
print(json.dumps(result, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))

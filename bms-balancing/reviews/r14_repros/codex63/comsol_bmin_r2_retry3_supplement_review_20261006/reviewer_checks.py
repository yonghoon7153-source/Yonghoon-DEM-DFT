"""Independent data-only review. Does not import or execute supplied programs."""
import collections
import hashlib
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile

ROOT = Path(__file__).resolve().parent
ARCHIVE = Path('C:/Users/Administrator/Downloads/BMIN_R2_LIMITED_VALIDATION_RETRY3_RESULT_20261005.zip')
SNAP = json.loads((ROOT / 'RECEIVED_SNAPSHOT.json').read_text(encoding='utf-8'))
NAME = 'BMIN_R2_RETRY3_ACCOUNTING_CORRECTION_20261006.json'
raw = SNAP['files'][NAME]['content'].encode('utf-8')
correction = json.loads(raw)
errors = []
checks = 0
refs = []
row_results = []
def sha(data):
    return hashlib.sha256(data).hexdigest()
def check(ok, label):
    global checks
    checks += 1
    if not ok:
        errors.append(label)
def key(row):
    return (row['id'], row['input_index'])
before = sha(ARCHIVE.read_bytes())
check(sha(raw) == '16876bb01afe549f9f78ef1c5b32569a85f8e8e3dde0c1daef65bf56305c4414', 'correction_sha')
check(bool(raw) and correction['schema'] == 'bmin-r2-retry3-accounting-correction/v1', 'correction_schema')
# Verify the Git blob identity independently of the declared SHA-256.
check(hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest() == SNAP['files'][NAME]['sha'], 'github_blob')
with zipfile.ZipFile(ARCHIVE) as z:
    names = z.namelist()
    def data(path):
        return json.loads(z.read(path).decode('utf-8-sig'))
    manifest = data('PACKAGE_MANIFEST.json')
    check(len(names) == len(set(names)) == len({n.casefold() for n in names}), 'archive_unique_names')
    check(set(names) == {p['file'] for p in manifest['files']} | {'PACKAGE_MANIFEST.json'}, 'archive_exact_set')
    for info in z.infolist():
        p = PurePosixPath(info.filename)
        check(not (p.is_absolute() or '..' in p.parts or '\\' in info.filename or ':' in info.filename or stat.S_ISLNK(info.external_attr >> 16)), 'safe_member:' + info.filename)
    for pin in manifest['files']:
        b = z.read(pin['file'])
        check(len(b) == pin['bytes'] and sha(b) == pin['sha256'], 'manifest:' + pin['file'])
    check(z.testzip() is None, 'crc')
    check(before == correction['source']['zip_sha256'] == 'ed0138b90cf2dc4e42f22ec18d8719ff56906780f74b4139850d604b096bb470', 'archive_sha')
    check(sha(z.read('PACKAGE_MANIFEST.json')) == correction['source']['manifest_sha256'], 'manifest_sha')
    def references(obj):
        if isinstance(obj, dict):
            if 'path' in obj and 'sha256' in obj:
                refs.append((obj['path'], obj['sha256']))
                check(obj['path'] in names and sha(z.read(obj['path'])) == obj['sha256'], 'reference:' + obj['path'])
            for v in obj.values():
                references(v)
        elif isinstance(obj, list):
            for v in obj:
                references(v)
    references(correction)
    old = data('FINAL_INPUT_ACCOUNTING.json')
    pre = data('INPUT_CASE_MAP.json')
    premap = {key(r):r for r in pre}
    prepared = {key(r):r for r in data('PREPARED_PYTHON_INPUTS.json')}
    psbindings = {key(r):r for r in data('PS_INPUT_BINDINGS.json')['inputs']}
    expected = {key(r) for r in old}
    rows = correction['rows']
    check(len(rows) == 77 and len({key(r) for r in rows}) == 77 and {key(r) for r in rows} == expected, 'rows_exact_set')
    check(len({r['final_accounting_row'] for r in rows}) == 77, 'row_offsets_unique')
    counts = collections.Counter(r['engine'].split()[0] for r in rows)
    check(dict(counts) == {k:v for k,v in correction['counts'].items() if k != 'rows'}, 'engine_counts')
    for r in rows:
        start = len(errors)
        k = key(r)
        orig = old[r['final_accounting_row']]
        tmpl = premap[k]
        check(key(orig) == k and r['engine'] == orig['engine'], 'original_key:' + str(k))
        check(r['original'] == {f:orig[f] for f in ('status','fixture_created','actual_call_bound')}, 'original_fields:' + str(k))
        check(r['pretest_template'] == dict(file='INPUT_CASE_MAP.json', **{f:tmpl[f] for f in ('status','fixture_created','actual_call_bound')}), 'pretest_fields:' + str(k))
        check('최종 판정 권위 없음' in r['interpretation'] and 'superseded_by_evidence' in r['interpretation'], 'interpretation:' + str(k))
        ev = r['superseded_by_evidence']
        ret = data(ev['engine_return']['path'])
        check(ret['rc'] == 0 and ret['error'] is None and ret['elapsed_s'] <= ret['limit_s'], 'engine_return:' + str(k))
        verdict = ev['harness_verdict']
        b = z.read(verdict['path'])
        check(sha(b) == ret['stdout']['sha256'] and len(b) == ret['stdout']['bytes'], 'stdout_return:' + str(k))
        line = b.decode('utf-8-sig').splitlines()[verdict['line']-1]
        if r['engine'] == 'Python':
            check(json.loads(line) == orig['observed'], 'python_stdout:' + str(k))
            p = prepared[k]
            check(ev['prepared_input_row']['key'] == list(k) and p['expectation'] == tmpl, 'prepared_key:' + str(k))
            prefix = 'fixtures/' + r['id'] + '_' + str(r['input_index']) + '/'
            check(p['path'].replace('\\','/').endswith('/' + prefix[:-1]), 'prepared_path:' + str(k))
            check({f['path'] for f in ev['fixture_files']} == {n for n in names if n.startswith(prefix)}, 'fixture_set:' + str(k))
            check(data(prefix + 'INPUT_EXPECTATION.json') == tmpl, 'fixture_expectation:' + str(k))
            check(ev['entry_output']['path'] == 'results/' + r['id'] + '_' + str(r['input_index']) + '.json', 'entry_path:' + str(k))
            check(json.loads(line) == data('results/PYTHON_RESULTS.json')['results'][verdict['line']-1], 'python_result:' + str(k))
        elif r['engine'].startswith('Windows'):
            check(json.loads(line) == orig['observed'], 'ps_stdout:' + str(k))
            check(ev['input_binding_row']['key'] == list(k) and psbindings[k] == tmpl, 'ps_binding:' + str(k))
            check(data(ev['result']['file']['path'])['results'][ev['result']['results_index']] == orig['observed'], 'ps_result:' + str(k))
        else:
            fields = line.split('|')
            check(fields == [r['id'], orig['observed']['status'], orig['observed']['reason']], 'java_stdout:' + str(k))
            helper = z.read(ev['harness']['path'])
            for ex in ev['extracted']:
                check(z.read(ex['path']).strip() in helper, 'java_extraction:' + str(k))
        row_results.append({'id':k[0], 'input_index':k[1], 'status':'PASS' if len(errors)==start else 'FAIL', 'errors':errors[start:]})
    ps16 = next(r for r in old if r['id']=='PS01-16')['observed']
after = sha(ARCHIVE.read_bytes())
check(before == after, 'archive_unchanged')
out = {
    'scope':'Independent static and data-only comparisons. No supplied code, generator, candidate, suite, Java or COMSOL executed.',
    'commit':SNAP['commit'], 'archive_sha256':before, 'archive_unchanged':before==after,
    'archive_payloads':len(manifest['files']), 'correction_bytes':len(raw), 'correction_sha256':sha(raw),
    'rows':len(rows), 'unique_ids':len({r['id'] for r in rows}), 'engine_counts':dict(counts),
    'reference_occurrences':len(refs), 'unique_referenced_members':len(set(refs)),
    'checks':checks, 'errors':errors, 'row_results':row_results, 'PS01_16_observed':ps16,
    'nonblocking_stale_text':correction['not_claimed'][0],
}
(ROOT/'REVIEW_CHECKS.json').write_text(json.dumps(out, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k != 'row_results'}, ensure_ascii=False, indent=2))
raise SystemExit(1 if errors else 0)

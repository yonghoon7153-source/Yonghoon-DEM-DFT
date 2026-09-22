"""Package this review's existing evidence, not target production files."""
import datetime
import hashlib
import json
import pathlib
import subprocess
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
WORK = HERE.parents[1]
REPO = WORK / 'work/gate67-head'
ZIP = HERE.parent / 'GATE67_CODEX_REVIEW_cdc49e91_20260922.zip'
EXPECTED = 'cdc49e91af15b2ef968753110cfae3bbe7ab5c2f'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read(name):
    return json.loads((HERE / name).read_text(encoding='utf-8'))

def emit(name, obj):
    (HERE / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args]).decode('utf-8').strip()

assert not ZIP.exists(), 'Do not overwrite an existing review package'
identity = read('TARGET_IDENTITY.json')
assert git('rev-parse', 'HEAD') == EXPECTED == identity['head']
assert git('status', '--porcelain') == ''
checked = []
for item in identity['files']:
    data = (REPO / item['path']).read_bytes()
    assert len(data) == item['bytes'] and sha(data) == item['sha256'], item['path']
    checked.append(item['path'])

boundary = {r['case']: r for r in read('boundary-cases/summary.json')}
assert boundary['namespace_explicit_off']['forged_actual_entry']['result'] == 'ACCEPTED'
assert boundary['namespace_explicit_on']['forged_actual_entry']['result'] == 'REJECTED'
assert boundary['zip_package_remove_path']['complete']['result'] == 'ACCEPTED'
assert boundary['zip_package_remove_path']['entry']['result'] == 'REJECTED'
for name in ('zip_package_plain', 'zip_module_remove_path'):
    assert boundary[name]['entry']['result'] == 'ACCEPTED'
premise = read('premise-no-execution/observations.json')
assert len(premise) == 4 and all(r['committed_test_returned_normally'] for r in premise)
assert all(r['child_rc'] == 4 for r in premise if r['case'].startswith('usage'))
assert all(r['child_rc'] == 0 and r['call_phase_count'] == 0 for r in premise if r['case'].startswith('collect'))
mutations = read('partial-mutations-final/summary.json')
exact = [r for r in mutations if r['phases']['mutant']['expected_failure_set_matches']]
assert len(mutations) == 9 and len(exact) == 8
for r in exact:
    assert r['phases']['baseline']['rc'] == 0
    assert all(v == ['call'] for v in r['phases']['mutant']['failure_phases'].values())
witness = [r for r in exact if all(r['phases']['mutant']['call_witness_matches'].values())]
assert len(witness) == 7
registry = read('registry-audit.json')
assert (registry['previous_count'], registry['current_count']) == (366, 367)
assert len(registry['added']) == 1 and not registry['deleted'] and not registry['changed_survivors']

old_script = WORK / 'outputs/gate66_review_20260922/repro_startup.py'
old_bytes = old_script.read_bytes()
copy = HERE / 'repro_startup_gate66.py'
if copy.exists():
    assert copy.read_bytes() == old_bytes
else:
    copy.write_bytes(old_bytes)

emit('FINAL_CHECK.json', dict(
    verified_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), head=EXPECTED,
    status_porcelain='', target_identity_files_byte_unchanged=checked,
    findings=['G67-N1:P1', 'G67-N2:P1', 'G67-T1:P2'],
    mutation_supplement=dict(selected=9, exact_failure_node_and_call_matches=8, witness_matches=7,
                             official_coverage=False),
    registry_delta=dict(previous=366, current=367, added=1, deleted=0, changed_survivors=0),
    original_repro_copy_sha256=sha(old_bytes), production_edits=0,
    scope='Offline evidence consistency and target identity, not a new test run or independent scientific validation'))

members = {}
def add(path):
    if path.is_symlink():
        raise AssertionError('symlink evidence not packaged: ' + str(path))
    name = path.relative_to(HERE).as_posix()
    assert name not in members
    members[name] = path.read_bytes()

for path in HERE.iterdir():
    if path.is_file() and path.name not in ('REVIEW_MANIFEST.json', 'PACKAGE_RECEIPT.json'):
        add(path)

# Only direct evidence files in mutation folders. Never traverse their pytest temp trees.
for folder in ('partial-mutations', 'partial-mutations-portable', 'partial-mutations-isolated', 'partial-mutations-final', 'premise-no-execution'):
    for path in (HERE / folder).iterdir():
        if path.is_file():
            add(path)

# Small generated fixture/evidence trees only; no venv or bytecode.
for folder in ('old-startup', 'boundary-cases'):
    def walk(directory):
        for path in directory.iterdir():
            if path.name in ('venv-on', 'venv-off', '__pycache__', '.pytest_cache'):
                continue
            if path.is_symlink():
                raise AssertionError(str(path))
            if path.is_dir():
                walk(path)
            elif path.is_file():
                add(path)
    walk(HERE / folder)

names = sorted(members)
assert len({n.casefold() for n in names}) == len(names)
assert all(not n.startswith('/') and '..' not in pathlib.PurePosixPath(n).parts and ':' not in n for n in names)
manifest = dict(schema_version=1, head=EXPECTED, scope='review evidence only',
                payloads=[dict(path=n, bytes=len(members[n]), sha256=sha(members[n])) for n in names])
manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
(HERE / 'REVIEW_MANIFEST.json').write_bytes(manifest_bytes)
with zipfile.ZipFile(ZIP, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name in names:
        z.writestr(name, members[name])
    z.writestr('REVIEW_MANIFEST.json', manifest_bytes)
with zipfile.ZipFile(ZIP) as z:
    assert len(z.namelist()) == len(names) + 1
    assert set(z.namelist()) == set(names) | {'REVIEW_MANIFEST.json'}
    assert z.testzip() is None
    assert z.read('REVIEW_MANIFEST.json') == manifest_bytes
    for row in manifest['payloads']:
        data = z.read(row['path'])
        assert len(data) == row['bytes'] and sha(data) == row['sha256']
raw = ZIP.read_bytes()
receipt = dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               path=str(ZIP), bytes=len(raw), sha256=sha(raw), payload_count=len(names),
               total_zip_entries=len(names) + 1, manifest_sha256=sha(manifest_bytes),
               verified_exact_set_size_sha_crc=True, recipient_verification=None,
               target_head=EXPECTED, production_edits=0,
               scope='Reviewer evidence; no target checkout, venvs, complete temp sandboxes or science results')
emit('PACKAGE_RECEIPT.json', receipt)
print(json.dumps(receipt, ensure_ascii=True, indent=2))

"""Package the completed review; never run a simulator or modify source/."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
ARCHIVE = ROOT.parent / 'codex_dem_unloading_kit_fix_recheck_20261015.zip'
MANIFEST = ROOT / 'PACKAGE_MANIFEST.json'

def sha(data):
    return hashlib.sha256(data).hexdigest()

src = json.loads((ROOT / 'source_manifest.json').read_text(encoding='utf-8'))
for row in src['files']:
    data = (ROOT / 'source' / row['path']).read_bytes()
    assert len(data) == row['bytes'], row['path']
    assert sha(data) == row['sha256'], row['path']
    blob = b'blob ' + str(len(data)).encode('ascii') + b'\0' + data
    assert hashlib.sha1(blob).hexdigest() == row['blob_sha'], row['path']

selected_cases = set()
for name in ('resume_recheck.json', 'receipt_ids_recheck.json'):
    result = json.loads((ROOT / 'evidence' / name).read_text(encoding='utf-8'))
    # Evidence retains original Windows paths; normalize for portable packing.
    selected_cases.add(result['fixture_root'].replace('\\', '/').rstrip('/').split('/')[-1])

files = []
excluded = set()
for path in sorted(ROOT.rglob('*')):
    if not path.is_file():
        continue
    rel = path.relative_to(ROOT)
    if path == MANIFEST or '__pycache__' in rel.parts or rel.parts[0] in ('tmp', 'tmp_baseline'):
        continue
    if len(rel.parts) > 2 and rel.parts[0] == 'evidence':
        folder = rel.parts[1]
        if folder.startswith(('resume_cases_', 'receipt_ids_cases_')) and folder not in selected_cases:
            excluded.add(folder)
            continue
    data = path.read_bytes()
    files.append({'path': rel.as_posix(), 'bytes': len(data), 'sha256': sha(data)})

manifest = {
    'schema': 'codex_review_package/v1',
    'source_pin': src['pin'],
    'verdict': 'HOLD',
    'source_files_verified_unchanged': len(src['files']),
    'selected_case_folders': sorted(selected_cases),
    'excluded_previous_case_folders': sorted(excluded),
    'file_count_excluding_manifest': len(files),
    'bytes_excluding_manifest': sum(row['bytes'] for row in files),
    'files': files,
}
MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
with zipfile.ZipFile(ARCHIVE, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for row in files:
        z.write(ROOT / row['path'], ROOT.name + '/' + row['path'])
    z.write(MANIFEST, ROOT.name + '/' + MANIFEST.name)
with zipfile.ZipFile(ARCHIVE) as z:
    assert z.testzip() is None
    assert len(z.namelist()) == len(files) + 1
    assert len({name.casefold() for name in z.namelist()}) == len(z.namelist())
    for row in files:
        data = z.read(ROOT.name + '/' + row['path'])
        assert len(data) == row['bytes'] and sha(data) == row['sha256'], row['path']
    assert z.read(ROOT.name + '/' + MANIFEST.name) == MANIFEST.read_bytes()
print(json.dumps({
    'zip': str(ARCHIVE), 'bytes': ARCHIVE.stat().st_size,
    'sha256': sha(ARCHIVE.read_bytes()), 'entries': len(files) + 1,
    'source_files_verified_unchanged': len(src['files']),
    'manifest_sha256': sha(MANIFEST.read_bytes()),
    'crc_and_all_entry_hashes_verified': True,
}, ensure_ascii=False, indent=2))

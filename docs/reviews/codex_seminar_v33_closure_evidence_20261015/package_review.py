"""Seal reviewer outputs; never run producer code or change submitted files."""
from pathlib import Path
import hashlib
import json
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent
sha = lambda b: hashlib.sha256(b).hexdigest()
EV = ROOT / 'evidence'
intake = json.loads((EV/'intake.json').read_text(encoding='utf-8'))
preservation = {'input_members': [], 'original_attachments': []}
for entry in intake['members']:
    p = ROOT/'input'/entry['path']
    actual = sha(p.read_bytes())
    assert actual == entry['sha256'], f'Changed submitted member: {entry["path"]}'
    preservation['input_members'].append({'path': entry['path'], 'sha256': actual, 'unchanged': True})
downloads = Path(intake['zip']).parent
originals = [(Path(intake['zip']), intake['sha256'])]
originals += [(downloads/name, record['sha256']) for name,record in intake['standalone_matches'].items()]
for p, expected in originals:
    record = {'path': str(p), 'present': p.exists(), 'expected_sha256': expected}
    if p.exists():
        record['sha256'] = sha(p.read_bytes())
        assert record['sha256'] == expected, f'Original changed: {p}'
        record['unchanged'] = True
    preservation['original_attachments'].append(record)
(EV/'source_preservation.json').write_text(json.dumps(preservation, ensure_ascii=False, indent=2), encoding='utf-8')

for switch, filename in [('-Check','semantics_check.json'), ('-Compare','semantics_compare.txt')]:
    # Use the same installed PowerShell 7 runtime used by the independent probe.
    script = str(ROOT/'agents/semantics_probe.ps1').replace("'", "''")
    command = "[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false); & '"+script+"' "+switch
    result = subprocess.run(['pwsh', '-NoProfile', '-Command', command], capture_output=True, check=True)
    output = result.stdout.decode('utf-8-sig')
    if switch == '-Check':
        parsed = json.loads(output)
        assert parsed['passed'] == parsed['total'] == 21 and not parsed['failed']
        output = json.dumps(parsed, ensure_ascii=False, indent=2)
    (EV/filename).write_text(output, encoding='utf-8')

excluded = {'REVIEW_MANIFEST.json', 'evidence/figure_debug.json', 'evidence/figure_normalized.diff'}
files = sorted(p for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts
               and p.relative_to(ROOT).as_posix() not in excluded)
entries = [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size,
            'sha256': sha(p.read_bytes())} for p in files]
manifest = {'schema': 'codex_review_delivery/v1', 'self_excluded': 'REVIEW_MANIFEST.json',
            'source_zip_sha256': intake['sha256'], 'files': entries}
mp = ROOT/'REVIEW_MANIFEST.json'
mp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
archive = ROOT.parent/'codex_seminar_v33_closure_review_20261015.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for p in files+[mp]:
        z.write(p, arcname=ROOT.name+'/'+p.relative_to(ROOT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    expected = {ROOT.name+'/'+entry['path'] for entry in entries} | {ROOT.name+'/REVIEW_MANIFEST.json'}
    assert set(z.namelist()) == expected and len(z.namelist()) == len(expected)
    for entry in entries:
        content = z.read(ROOT.name+'/'+entry['path'])
        assert len(content) == entry['bytes'] and sha(content) == entry['sha256']
    assert z.read(ROOT.name+'/REVIEW_MANIFEST.json') == mp.read_bytes()
receipt = {'archive': str(archive), 'bytes': archive.stat().st_size,
           'sha256': sha(archive.read_bytes()), 'files_in_zip': len(entries)+1,
           'crc_ok': True, 'exact_members': True, 'all_member_hashes_ok': True,
           'input_preserved': len(preservation['input_members'])}
receipt_path = archive.with_suffix('.receipt.json')
receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(receipt, ensure_ascii=False, indent=2))

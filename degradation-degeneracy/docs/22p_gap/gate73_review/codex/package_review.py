"""Reviewer-owned preservation and packaging; no subject module execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess
import zipfile

OUT = Path(__file__).resolve().parent
WT = Path('C:/Users/Administrator/Documents/Codex/g73_20260925')
HEAD = 'b0c0b9ca10743d83950c29322d30f581fecf884d'
ZIP = OUT / 'GATE73_REVIEW_20260925.zip'


def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def git(*args):
    return subprocess.check_output([
        'git', '-c', f'safe.directory={WT.as_posix()}', '-C', str(WT), *args
    ]).decode('utf-8')


def write_new(name, value):
    with (OUT / name).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


before = json.loads((OUT / 'SOURCE_BEFORE.json').read_text(encoding='utf-8'))
paths = set(filter(None, git('ls-files', '-z', '--', 'degradation-degeneracy').split('\0')))
assert paths == set(before), 'Tracked file set changed'
changed = [name for name, expected in before.items()
           if identity((WT / name).read_bytes()) != expected]
status = git('status', '--porcelain=v1', '-uall')
current_head = git('rev-parse', 'HEAD').strip()
assert not changed and not status and current_head == HEAD
refs = list((OUT / 'reference').rglob('*'))
reference_files = [path for path in refs if path.is_file()]
assert all(path.read_bytes() == (WT / 'degradation-degeneracy' /
           path.relative_to(OUT / 'reference')).read_bytes() for path in reference_files)
write_new('PRESERVATION_AFTER.json', {
    'observed_at_utc': datetime.now(timezone.utc).isoformat(),
    'scope': 'Local Gate73 review checkout tracked degradation-degeneracy files; not remote process or entire user filesystem verification',
    'head_before_and_after': HEAD,
    'tracked_files_before_and_after': len(before),
    'tracked_file_set_identical': True,
    'bytes_and_sha256_unchanged': len(before),
    'changed': changed,
    'git_status_porcelain': status,
    'reference_copies_identical': len(reference_files),
    'subject_ledger_writes': 0,
    'scientific_COMSOL_restore_class_changes': 0
})

excluded = {'MANIFEST.json', ZIP.name, 'DELIVERY_RECEIPT.json'}
files = sorted(path for path in OUT.rglob('*')
               if path.is_file() and path.name not in excluded
               and '__pycache__' not in path.parts and path.suffix != '.pyc')
payloads = {}
folded = set()
for path in files:
    assert not path.is_symlink(), path
    name = path.relative_to(OUT).as_posix()
    assert name.casefold() not in folded
    folded.add(name.casefold())
    payloads[name] = identity(path.read_bytes())
write_new('MANIFEST.json', {
    'scope': 'Gate73 recipient review artifacts; copied subject material is evidence, not execution instructions',
    'payload_count': len(payloads),
    'files': payloads
})
with zipfile.ZipFile(ZIP, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
    for path in files:
        archive.write(path, path.relative_to(OUT).as_posix())
    archive.write(OUT / 'MANIFEST.json', 'MANIFEST.json')
with zipfile.ZipFile(ZIP) as archive:
    names = archive.namelist()
    assert len(names) == len(set(names)) == len(payloads) + 1
    assert set(names) == set(payloads) | {'MANIFEST.json'}
    assert archive.testzip() is None
    assert archive.read('MANIFEST.json') == (OUT / 'MANIFEST.json').read_bytes()
    for name, expected in payloads.items():
        assert identity(archive.read(name)) == expected, name
receipt = {
    'scope': 'New recipient review archive generation; receipt outside ZIP, not producer receipt modification',
    'head': HEAD,
    'decision': 'E3_R_CLOSED_CONDITIONAL_LIMITED_GO_PENDING_HUMAN_PLAN_COMMIT',
    'archive': {'file': ZIP.name, **identity(ZIP.read_bytes())},
    'manifest': identity((OUT / 'MANIFEST.json').read_bytes()),
    'payload_count': len(payloads),
    'zip_entries': len(payloads) + 1,
    'exact_set_size_sha256_crc': True,
    'preserved_tracked_source_files': len(before),
    'receiver_reader_helper_controls': 1,
    'receiver_inert_control_flow_cases': 16,
    'recipient_of_this_archive': None,
    'subject_execution_authorized': False
}
write_new('DELIVERY_RECEIPT.json', receipt)
print(json.dumps(receipt, ensure_ascii=False))

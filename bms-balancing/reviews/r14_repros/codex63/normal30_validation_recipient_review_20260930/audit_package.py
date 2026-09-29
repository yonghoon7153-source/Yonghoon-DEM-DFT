"""Reviewer-only ZIP/data inspection. Never imports or executes received code."""
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import stat
import zipfile

ROOT = Path(__file__).resolve().parent
SOURCE = Path('C:/Users/Administrator/Downloads/COMSOL63_NORMAL30_LIMITED_VALIDATION_COMPLETE_20260930.zip')

def sha(b):
    return hashlib.sha256(b).hexdigest()

def audit(raw, label):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names = z.namelist()
        assert len(names) == len(set(names)) == len(set(n.casefold() for n in names))
        for e in z.infolist():
            p = PurePosixPath(e.filename)
            assert not p.is_absolute() and all(t not in ('..', '.', '') for t in p.parts)
            assert '\\' not in e.filename and ':' not in e.filename
            assert not stat.S_ISLNK(e.external_attr >> 16) and not e.is_dir()
            assert not (e.flag_bits & 1)
        assert sum(e.file_size for e in z.infolist()) < 128 * 1024 * 1024
        assert z.testzip() is None
        files = {n: z.read(n) for n in names}
        manifest_names = [n for n in names if '/' not in n and 'MANIFEST' in n]
        assert len(manifest_names) == 1, manifest_names
        mn = manifest_names[0]
        m = json.loads(files[mn])
        rows = m['files']
        assert len(rows) == len({r['file'] for r in rows})
        assert set(names) == {r['file'] for r in rows} | {mn}
        for r in rows:
            b = files[r['file']]
            assert len(b) == r['bytes'] and sha(b) == r['sha256'], r['file']
    return files, dict(label=label, bytes=len(raw), sha256=sha(raw), entries=len(names), payload_count=len(rows), manifest=mn, manifest_sha256=sha(files[mn]), exact_set=True, size_sha_crc=True, path_case_link_checks=True)

raw = SOURCE.read_bytes()
files, report = audit(raw, SOURCE.name)
out = ROOT / 'received'
assert not out.exists(), 'No overwrite of prior review extraction'
for name, body in files.items():
    p = out.joinpath(*PurePosixPath(name).parts)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(body)
nested = []
for name, body in files.items():
    if name.endswith('.zip'):
        _, result = audit(body, name)
        nested.append(result)
report['nested_archives'] = nested
cm = json.loads(files['candidate_snapshot/CODE_MANIFEST.json'])
for row in cm['files']:
    b = files['candidate_snapshot/' + row['file']]
    assert len(b) == row['bytes'] and sha(b) == row['sha256']
report['candidate_manifest_sha256'] = sha(files['candidate_snapshot/CODE_MANIFEST.json'])
report['candidate_files_verified'] = len(cm['files'])
report['source_after_sha256'] = sha(SOURCE.read_bytes())
assert report['source_after_sha256'] == report['sha256']
(ROOT / 'PACKAGE_AUDIT.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))

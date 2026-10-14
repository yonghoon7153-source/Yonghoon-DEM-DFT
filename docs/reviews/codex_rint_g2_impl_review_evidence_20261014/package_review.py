"""Package review-owned artifacts; verify pinned source without changing it."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
ZIP = ROOT.parent / 'codex_rint_g2_impl_review_1087a9b2f_20261014.zip'
RECEIPT = ZIP.with_suffix('.receipt.json')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    manifest = json.loads((ROOT / 'source_manifest.json').read_text(encoding='utf-8'))
    wrong = []
    for f in manifest['files']:
        p = ROOT / 'source' / f['path']
        b = p.read_bytes()
        if sha(b) != f['sha256']:
            wrong.append(f['path'])
        git_blob = hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()
        if git_blob != f['sha']:
            wrong.append(f['path'] + ' [git blob]')
    if wrong:
        raise RuntimeError(wrong)
    files = [p for p in sorted(ROOT.rglob('*'))
             if p.is_file() and not any(x in {'tmp', '__pycache__'} for x in p.relative_to(ROOT).parts)
             and p.name != 'artifact_manifest.json']
    entries = [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size,
                'sha256': sha(p.read_bytes())} for p in files]
    am = ROOT / 'artifact_manifest.json'
    am.write_text(json.dumps({'pin': manifest['pin'], 'files': entries}, ensure_ascii=False,
                             indent=2) + '\n', encoding='utf-8')
    files.append(am)
    with zipfile.ZipFile(ZIP, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in files:
            z.write(p, (Path(ROOT.name) / p.relative_to(ROOT)).as_posix())
    with zipfile.ZipFile(ZIP) as z:
        if z.testzip() is not None:
            raise RuntimeError('ZIP CRC failure')
        for e in entries:
            data = z.read(ROOT.name + '/' + e['path'])
            if sha(data) != e['sha256']:
                raise RuntimeError('ZIP content mismatch: ' + e['path'])
    receipt = {'zip': ZIP.name, 'bytes': ZIP.stat().st_size, 'sha256': sha(ZIP.read_bytes()),
               'pin': manifest['pin'], 'archive_entries': len(files),
               'source_files_verified': len(manifest['files']), 'source_mismatches': [],
               'zip_crc': 'PASS', 'all_entry_sha256': 'PASS',
               'scope': 'Packaging integrity only; does not supersede the review verdict'}
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

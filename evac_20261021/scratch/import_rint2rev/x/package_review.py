"""Verify immutable inputs and package local review artifacts; no repo changes."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
PIN = '5dc6f7f0b91fd9db39ab595f6b8c79a8f0d2f3b5'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def longpath(p):
    return Path('\\\\?\\' + str(p)) if os.name == 'nt' else p


def main():
    original = json.loads((ROOT / 'source_manifest.json').read_text('utf-8'))
    errors = []
    for item in original['files']:
        p = ROOT / 'source' / item['path']
        raw = longpath(p).read_bytes()
        git_blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        if sha(raw) != item['sha256'] or git_blob != item['git_blob']:
            errors.append(item['path'])
    integrity = {'pin': PIN, 'checked': len(original['files']), 'mismatches': errors,
                 'source_bytes': sum(x['bytes'] for x in original['files'])}
    (ROOT / 'integrity_final.json').write_text(json.dumps(integrity, indent=2)+'\n', 'utf-8')
    if errors:
        raise SystemExit(f'Source integrity failed: {errors}')
    selected = []
    top = ['codex_review_rint2_carbon_additive_design_20261021.md', 'REPRODUCTION.md',
           'USER_REQUEST.txt', 'PIN.txt', 'source_manifest.json', 'integrity_final.json',
           'intake.py', 'package_review.py']
    selected += [ROOT / name for name in top]
    selected += [ROOT / 'source' / item['path'] for item in original['files']]
    for dirname in ('litdb_cards', 'geometry', 'registration', 'part_b', 'evidence'):
        for p in (ROOT / dirname).rglob('*'):
            if not longpath(p).is_file():
                continue
            parts = p.relative_to(ROOT).parts
            if any(x in parts for x in ('__pycache__', 'staged_source', 'tmp', 'adapted')):
                continue
            if p.suffix.lower() in ('.pyc', '.pdf', '.png'):
                continue
            selected.append(p)
    selected = sorted(set(selected), key=lambda p: p.relative_to(ROOT).as_posix())
    manifest = {'pin': PIN, 'files': []}
    for p in selected:
        data = longpath(p).read_bytes()
        manifest['files'].append({'path': p.relative_to(ROOT).as_posix(),
                                  'bytes': len(data), 'sha256': sha(data)})
    mp = ROOT / 'delivery_manifest.json'
    mp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', 'utf-8')
    selected.append(mp)
    out = ROOT.parent / 'codex_rint2_carbon_design_review_20261021.zip'
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in selected:
            z.write(longpath(p), p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(out) as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f'CRC failed: {bad}')
        for entry in manifest['files']:
            if sha(z.read(entry['path'])) != entry['sha256']:
                raise RuntimeError(f'Archive hash failed: {entry["path"]}')
    result = {'path': str(out), 'bytes': out.stat().st_size, 'sha256': sha(out.read_bytes()),
              'entries': len(selected), 'source_integrity': integrity}
    (ROOT / 'delivery_receipt.json').write_text(json.dumps(result, indent=2)+'\n', 'utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

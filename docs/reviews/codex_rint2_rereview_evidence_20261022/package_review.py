"""Verify fixed inputs and package review evidence only. Does not modify source."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
PIN = '0b3012460fb8e8b7d53484b0efe399e2dc506aec'

def lp(p):
    s = str(p)
    return Path('\\\\?\\' + s) if os.name == 'nt' and not s.startswith('\\\\?\\') else p

def sha(b):
    return hashlib.sha256(b).hexdigest()

def main():
    mf = json.loads((ROOT/'source_manifest.json').read_text('utf-8'))
    assert mf['pin'] == PIN
    errors = []
    for row in mf['files']:
        raw = lp(ROOT/'source'/row['path']).read_bytes()
        blob = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        if sha(raw) != row['sha256'] or blob != row['git_blob'] or len(raw) != row['bytes']:
            errors.append(row['path'])
    final = {'pin':PIN, 'checked':len(mf['files']), 'mismatches':errors,
             'source_bytes':sum(x['bytes'] for x in mf['files'])}
    (ROOT/'integrity_final.json').write_text(json.dumps(final,indent=2)+'\n','utf-8')
    if errors:
        raise RuntimeError(f'Pinned sources changed: {errors}')
    items = [ROOT/n for n in ('codex_review_rint2_rereview_20261022.md','REPRODUCTION.md',
                              'PIN.txt','source_manifest.json','integrity_final.json',
                              'intake.py','package_review.py')]
    items.extend(ROOT/'source'/x['path'] for x in mf['files'])
    for sub in ('certificate','geometry','registration','probes','evidence'):
        for p in (ROOT/sub).rglob('*'):
            parts = p.relative_to(ROOT).parts
            if lp(p).is_file() and '__pycache__' not in parts and 'tmp' not in parts and p.suffix != '.pyc':
                items.append(p)
    items = sorted(set(items),key=lambda p:p.relative_to(ROOT).as_posix())
    manifest = {'pin':PIN, 'files':[]}
    for p in items:
        b = lp(p).read_bytes()
        manifest['files'].append({'path':p.relative_to(ROOT).as_posix(),'bytes':len(b),'sha256':sha(b)})
    mp = ROOT/'delivery_manifest.json'
    mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n','utf-8')
    items.append(mp)
    output = ROOT.parent/'codex_rint2_rereview_20261022.zip'
    with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in items:
            z.write(lp(p),p.relative_to(ROOT).as_posix())
    with zipfile.ZipFile(output) as z:
        if z.testzip():
            raise RuntimeError('ZIP CRC failure')
        for row in manifest['files']:
            if sha(z.read(row['path'])) != row['sha256']:
                raise RuntimeError('ZIP SHA mismatch: '+row['path'])
    receipt = {'path':str(output),'bytes':output.stat().st_size,'sha256':sha(output.read_bytes()),
               'entries':len(items),'source_integrity':final}
    (ROOT/'delivery_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n','utf-8')
    print(json.dumps(receipt,ensure_ascii=False,indent=2))

if __name__ == '__main__':
    main()

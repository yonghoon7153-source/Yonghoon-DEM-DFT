"""Package reviewer outputs as data; no source-tree operation or project import."""
from pathlib import Path, PurePosixPath
import hashlib, json, zipfile
ROOT = Path(__file__).resolve().parent
ZIP = ROOT/'GATE71_REVIEW_20260925.zip'
assert not ZIP.exists(), 'Existing archive must not be overwritten'
excluded = {'MANIFEST.json','REVIEW_PACKAGE_RECEIPT.json',ZIP.name}
files = [p for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name not in excluded]
inventory = []
for p in files:
    assert not p.is_symlink()
    rel = p.relative_to(ROOT).as_posix()
    assert not PurePosixPath(rel).is_absolute() and '..' not in PurePosixPath(rel).parts
    b = p.read_bytes()
    inventory.append({'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
assert len({r['path'].casefold() for r in inventory}) == len(inventory)
manifest = json.dumps({'scope':'Gate71 receiver review artifacts; not executable authorization',
                       'payload':inventory},ensure_ascii=False,indent=2).encode('utf-8')+b'\n'
(ROOT/'MANIFEST.json').write_bytes(manifest)
with zipfile.ZipFile(ZIP,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for row in inventory:
        z.write(ROOT/row['path'],row['path'])
    z.writestr('MANIFEST.json',manifest)
with zipfile.ZipFile(ZIP) as z:
    names = z.namelist()
    assert len(names)==len(set(names))==len({x.casefold() for x in names})
    assert set(names)=={r['path'] for r in inventory}|{'MANIFEST.json'}
    assert z.testzip() is None
    assert z.read('MANIFEST.json')==manifest
    for row in inventory:
        b=z.read(row['path'])
        assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
receipt = {'archive':ZIP.name,'bytes':ZIP.stat().st_size,
           'sha256':hashlib.sha256(ZIP.read_bytes()).hexdigest(),
           'payload_count':len(inventory),'manifest_sha256':hashlib.sha256(manifest).hexdigest(),
           'exact_set_size_sha_crc_case_paths_verified':True,
           'scope':'Receiver review package only; no producer/COMSOL execution approval',
           'receipt_outside_zip':True}
(ROOT/'REVIEW_PACKAGE_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))

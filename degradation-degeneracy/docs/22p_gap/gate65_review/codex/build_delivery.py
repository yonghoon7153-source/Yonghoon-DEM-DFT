"""Package this review only; no repo, dependencies, or upstream sandbox payload."""
from pathlib import Path
import hashlib,json,zipfile
root=Path(__file__).resolve().parent
archive=root.parent/'GATE65_REVIEW_20260922.zip'
if archive.exists():
    raise SystemExit('Refusing to overwrite existing review delivery')
files=[p for p in root.iterdir() if p.is_file() and p.name!='DELIVERY_RECEIPT.json']
for name in ('real_entry_cases','real_entry_sandbox_cases','import_full_cases',
             'namespace_case_corrected','namespace_case'):
    for p in (root/name).rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:
            files.append(p)
manifest={p.relative_to(root).as_posix():{'bytes':p.stat().st_size,
           'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(set(files))}
manifest_bytes=json.dumps(manifest,ensure_ascii=False,sort_keys=True,indent=2).encode('utf-8')
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=7) as z:
    for name in manifest:
        z.write(root/name,name)
    z.writestr('PAYLOAD_MANIFEST.json',manifest_bytes)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(set(z.namelist()))==len(manifest)+1
    assert set(z.namelist())==set(manifest)|{'PAYLOAD_MANIFEST.json'}
    for name, rec in manifest.items():
        b=z.read(name)
        assert len(b)==rec['bytes'] and hashlib.sha256(b).hexdigest()==rec['sha256']
receipt={'path':str(archive),'bytes':archive.stat().st_size,
         'sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),
         'payload_count':len(manifest),'entries':len(manifest)+1,
         'manifest_sha256':hashlib.sha256(manifest_bytes).hexdigest(),
         'verified':'exact set, unique names, CRC, every payload size and SHA256',
         'scope':'Review reports and bounded repro evidence only; no upstream mutation replay PASS; no Linux kernel-lock PASS'}
(root/'DELIVERY_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))

from pathlib import Path
import hashlib, json, os, zipfile

R = Path(__file__).resolve().parent
OUTPUT = R.parent/'codex_supp20_support_review_20261012.zip'
def readable(p):
    return Path('\\\\?\\'+str(p.resolve())) if os.name == 'nt' else p

qa=json.loads((R/'evidence/final_qa.json').read_text(encoding='utf8'))
assert not qa['source_integrity_problems']
assert not qa['source_extra_noncache_files']
assert all(qa['evidence_checks'].values())
entries=[]
longroot=readable(R)
for p in sorted(longroot.rglob('*')):
    if not p.is_file(): continue
    rel=p.relative_to(longroot)
    if rel.parts[0]=='tmp' or '__pycache__' in rel.parts or p.suffix=='.pyc': continue
    if rel.as_posix() in ('MANIFEST.sha256.json', 'delivery_receipt.json'): continue
    raw=p.read_bytes()
    entries.append({'path':rel.as_posix(), 'bytes':len(raw),
                    'sha256':hashlib.sha256(raw).hexdigest()})
manifest={'pin':qa['pin'], 'base':qa['base'], 'files':entries,
          'note':'Delivery checksum inventory; this manifest is excluded from its own list.'}
(R/'MANIFEST.sha256.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf8')
with zipfile.ZipFile(OUTPUT,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for row in entries:
        z.writestr(R.name+'/'+row['path'],readable(R/row['path']).read_bytes())
    z.writestr(R.name+'/MANIFEST.sha256.json',(R/'MANIFEST.sha256.json').read_bytes())
with zipfile.ZipFile(OUTPUT) as z:
    assert z.testzip() is None
    names=z.namelist()
    assert len(names)==len(set(names))==len(entries)+1
    assert not any('/../' in n or n.startswith(('/', '\\')) for n in names)
    for row in entries:
        raw=z.read(R.name+'/'+row['path'])
        assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
receipt={'zip':str(OUTPUT),'bytes':OUTPUT.stat().st_size,
         'sha256':hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
         'entries':len(entries)+1, 'uncompressed_bytes':sum(r['bytes'] for r in entries),
         'all_entry_hashes_verified':True,'source_files_verified':qa['source_files_verified']}
(R/'delivery_receipt.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(receipt,ensure_ascii=False,indent=2))

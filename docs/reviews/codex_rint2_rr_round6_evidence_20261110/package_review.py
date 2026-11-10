import hashlib, json, os, zipfile
from pathlib import Path

root = Path(__file__).resolve().parent
walk = Path('\\\\?\\' + str(root)) if os.name == 'nt' else root
dest = root.parent/'codex_rint2_rr_round6_review_aec8ca2f6cbc_20261110.zip'
manifest_name='SHA256SUMS.review.txt'
files=sorted(p for p in walk.rglob('*') if p.is_file() and p.name != manifest_name)
assert not any(p.is_symlink() for p in files)
names=[p.relative_to(walk).as_posix() for p in files]
assert len(names)==len(set(names)) and all(not n.startswith('/') and '..' not in n.split('/') for n in names)
manifest=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+n+'\n' for p,n in zip(files,names))
(walk/manifest_name).write_text(manifest,encoding='utf-8',newline='\n')
files.append(walk/manifest_name)
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in files:
        name=p.relative_to(walk).as_posix()
        info=zipfile.ZipInfo(name,date_time=(2026,11,10,0,0,0))
        info.compress_type=zipfile.ZIP_DEFLATED
        info.external_attr=0o100644<<16
        z.writestr(info,p.read_bytes(),compresslevel=9)
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    rows=z.read(manifest_name).decode().splitlines()
    for row in rows:
        expected,name=row.split('  ',1)
        assert hashlib.sha256(z.read(name)).hexdigest()==expected,name
    assert set(z.namelist())==set(names+[manifest_name])
result={'zip':str(dest),'bytes':dest.stat().st_size,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),
        'files':len(files),'manifest_rows':len(rows),'crc':'PASS','manifest':'PASS'}
(dest.with_suffix('.verification.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))

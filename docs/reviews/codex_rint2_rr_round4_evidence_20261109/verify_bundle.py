import argparse,hashlib,json,stat,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument('--zip',type=Path,default=ROOT/'input'/'codex_rint2_rr_round4_1f9f3607eb2f.zip')
ZIP=ap.parse_args().zip
DEST=ROOT/'package'
sha=lambda b:hashlib.sha256(b).hexdigest()
blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
with zipfile.ZipFile(ZIP) as z:
    assert z.testzip() is None
    names=z.namelist(); assert len(names)==len(set(names))==len({n.casefold() for n in names})
    for i in z.infolist():
        p=PurePosixPath(i.filename)
        assert not p.is_absolute() and '..' not in p.parts and ':' not in i.filename and '\\' not in i.filename
        assert not stat.S_ISLNK(i.external_attr>>16)
        f=DEST/i.filename
        if i.is_dir(): f.mkdir(parents=True,exist_ok=True);continue
        data=z.read(i)
        if f.exists():assert f.read_bytes()==data,str(f)
        else:f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
    pin=z.read('PIN.txt').decode().splitlines()[0]
    assert pin=='1f9f3607eb2f0118d322eeff780bba6eb17b85a2'
    hashes={}
    for line in z.read('SHA256SUMS').decode().splitlines():
        h,n=line.split('  ',1); assert n not in hashes;hashes[n]=h
        assert sha(z.read(n))==h,n
    assert {i.filename for i in z.infolist() if not i.is_dir()}==set(hashes)|{'SHA256SUMS'}
files=[{'path':f.relative_to(DEST/'repo').as_posix(),'bytes':f.stat().st_size,'sha256':sha(f.read_bytes()),'git_blob':blob(f.read_bytes())} for f in sorted((DEST/'repo').rglob('*')) if f.is_file()]
nested=[]
for manifest in sorted((DEST/'repo').rglob('SHA256SUMS')):
    count=0
    for line in manifest.read_text(encoding='utf-8').splitlines():
        if not line.strip():continue
        h,n=line.split(None,1);n=n.strip().lstrip('*')
        assert sha((manifest.parent/n).read_bytes())==h,str(manifest)+':'+n
        count+=1
    nested.append({'path':manifest.relative_to(DEST).as_posix(),'checked':count})
out={'pin':pin,'zip_bytes':ZIP.stat().st_size,'zip_sha256':sha(ZIP.read_bytes()),'members':len(names),'hash_entries':len(hashes),'repo_files':len(files),'crc':'PASS','nested_manifests':nested,'files':files}
(ROOT/'integrity.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='files'}))

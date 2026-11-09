from pathlib import Path,PurePosixPath
import argparse,hashlib,json,stat,zipfile,sys
ROOT=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--zip',type=Path,default=ROOT/'inputs/codex_rint2_rr_round5_abf0911ebc99.zip');a=ap.parse_args()
INPUT=a.zip
SHA='ba6a16dce289cda1ea9d5a057d0bd612094cee8ff5bf6f0af40cf0690b4eb927'
raw=INPUT.read_bytes();assert hashlib.sha256(raw).hexdigest()==SHA
dest=ROOT/'package'
if sys.platform=='win32':dest=Path('\\\\?\\'+str(dest))
rows=[]
with zipfile.ZipFile(INPUT) as z:
    assert len(z.namelist())==len(set(z.namelist())) and z.testzip() is None
    for info in z.infolist():
        n=info.filename;p=PurePosixPath(n)
        assert not p.is_absolute() and '..' not in p.parts and ':' not in n and '\\' not in n
        assert not stat.S_ISLNK(info.external_attr>>16)
        if info.is_dir():continue
        b=z.read(n);out=dest/n
        if out.exists():assert out.read_bytes()==b
        else:out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
        rows.append(dict(path=n,bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()))
    sums=z.read('SHA256SUMS').decode().splitlines()
    entries={}
    for line in sums:
        h,n=line.split(maxsplit=1);n=n.lstrip('*');entries[n]=h
        assert hashlib.sha256(z.read(n)).hexdigest()==h
    assert set(entries)=={r['path'] for r in rows}-{'SHA256SUMS'}
    pin=z.read('PIN.txt').decode();assert pin.splitlines()[0]=='abf0911ebc994167ac50132c78207c6c8d4421f1'
result=dict(zip_sha256=SHA,zip_bytes=len(raw),members=len(z.namelist()),files=len(rows),hash_rows=len(sums),crc='PASS',pin=pin,rows=rows)
(ROOT/'input_verification.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
print('AGENTS:',[r['path'] for r in rows if r['path'].endswith('AGENTS.md')])

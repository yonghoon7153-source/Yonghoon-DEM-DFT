"""Reviewer-owned bounded ZIP/hash inspection; never imports submitted code."""
from pathlib import Path, PurePosixPath
import hashlib, json, stat, zipfile
ROOT=Path(__file__).resolve().parent
SRC=Path('C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1_OPEN_CONNECTION_R1_20261010.zip')
def sha(b):return hashlib.sha256(b).hexdigest()
b=SRC.read_bytes()
assert len(b)==4011062 and sha(b)=='c9cf85b30f48fce0a8e747a8428b74b22a2d4c101498e2c0306720ed571fee0b'
with zipfile.ZipFile(SRC) as z:
    entries=z.infolist(); names=[e.filename for e in entries]
    assert len(names)==len(set(names))==len({n.casefold() for n in names})
    assert sum(e.file_size for e in entries)<64*1024*1024
    for e in entries:
        p=PurePosixPath(e.filename)
        assert not p.is_absolute() and '..' not in p.parts and ':' not in e.filename and '\\' not in e.filename
        assert not e.is_dir() and not stat.S_ISLNK(e.external_attr>>16)
    data={n:z.read(n) for n in names}
m=json.loads(data['PACKAGE_MANIFEST.json'])
assert len(m['files'])==m['payload_count']==117
assert set(names)=={r['path'] for r in m['files']}|{'PACKAGE_MANIFEST.json'}
for r in m['files']:
    raw=data[r['path']]; assert len(raw)==r['bytes'] and sha(raw)==r['sha256'],r['path']
dest=ROOT/'received'; assert not dest.exists()
for n,raw in data.items():
    p=dest/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
result={'input':{'path':str(SRC),'bytes':len(b),'sha256':sha(b)},'payload':117,'entries':len(names),'uncompressed_bytes':sum(map(len,data.values())),'exact_set_size_SHA_CRC_casefold_path_symlink':'PASS','package_manifest_sha256':sha(data['PACKAGE_MANIFEST.json']),'code_manifest_sha256':sha(data['CODE_MANIFEST.json']),'received_code_executed':0}
(ROOT/'INPUT_CHECK.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))

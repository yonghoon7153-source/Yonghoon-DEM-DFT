"""Reviewer-owned archive/data inspection. Never imports submitted code."""
import hashlib, json, stat, zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent
SRC = Path('C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1_OPEN_CONNECTION_PREPARATION_20261009.zip')
def sha(b): return hashlib.sha256(b).hexdigest()
def save(n, obj): (ROOT/n).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
raw = SRC.read_bytes()
assert len(raw)==1929576 and sha(raw)=='32cbb6ee5b8885a645da762154dab38d8f67ef4c7f97b5b4bc9c2ecd5fdd6f5c'
with zipfile.ZipFile(SRC) as z:
    entries=z.infolist(); names=[i.filename for i in entries]
    assert len(names)==len(set(names))==len(set(n.casefold() for n in names))
    assert sum(i.file_size for i in entries)<50*1024*1024
    for i in entries:
        p=PurePosixPath(i.filename)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in i.filename and ':' not in i.filename
        assert not stat.S_ISLNK(i.external_attr>>16) and not i.is_dir()
    data={n:z.read(n) for n in names} # zipfile verifies CRC
manifest=json.loads(data['PACKAGE_MANIFEST.json'])
assert set(names)=={x['path'] for x in manifest['files']}|{'PACKAGE_MANIFEST.json'}
assert len(manifest['files'])==manifest['payload_count']==79
for r in manifest['files']:
    assert len(data[r['path']])==r['bytes'] and sha(data[r['path']])==r['sha256']
out=ROOT/'received'
assert not out.exists()
for n,b in data.items():
    dest=out/n; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(b)
save('INPUT_CHECK.json',{'archive':{'path':str(SRC),'bytes':len(raw),'sha256':sha(raw)},'payload':79,'entries':80,'exact_set_size_sha_crc_casefold_path_symlink':'PASS','uncompressed_bytes':sum(map(len,data.values())),'manifest_sha256':sha(data['PACKAGE_MANIFEST.json']),'code_manifest_sha256':sha(data['CODE_MANIFEST.json']),'received_code_execution':0})
print(json.dumps(json.loads((ROOT/'INPUT_CHECK.json').read_text(encoding='utf8')),indent=2))

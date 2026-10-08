"""Reviewer data inspection only; no received program imports or calls."""
from pathlib import Path, PurePosixPath
import hashlib, json, stat, zipfile
ROOT=Path(__file__).resolve().parent
SRC=Path('C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1O_R1_003_VALIDATION_STOP_20261008.zip')
DEST=ROOT/'received'
def sha(b): return hashlib.sha256(b).hexdigest()
assert not DEST.exists(), 'Do not overwrite received copies'
raw=SRC.read_bytes()
assert len(raw)==876456 and sha(raw)=='11a27f3034fed763442ccce9730f7e008058b819bfbffd9d58a5d2994b875d4b'
with zipfile.ZipFile(SRC) as z:
    names=z.namelist()
    assert len(names)==len(set(names))==len({n.casefold() for n in names})
    assert sum(i.file_size for i in z.infolist()) < 50*1024*1024
    for i in z.infolist():
        p=PurePosixPath(i.filename)
        assert not p.is_absolute() and '..' not in p.parts and ':' not in i.filename and '\\' not in i.filename
        assert not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16)
    mb=z.read('PACKAGE_MANIFEST.json'); m=json.loads(mb)
    entries={e['path']:e for e in m['files']}
    assert len(entries)==len(m['files'])==153
    assert set(names)==set(entries)|{'PACKAGE_MANIFEST.json'}
    assert len(mb)==25683 and sha(mb)=='9a7b73e50223c152c87af3250e1ee955263837ae873dabcaffcee0d82653a5c4'
    payload={n:z.read(n) for n in names}
    for n,e in entries.items():
        assert len(payload[n])==e['bytes'] and sha(payload[n])==e['sha256'], n
    assert z.testzip() is None
for n,b in payload.items():
    p=DEST/n; p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(b)
cm=json.loads((DEST/'source/CODE_MANIFEST.json').read_text(encoding='utf-8'))
assert sha((DEST/'source/CODE_MANIFEST.json').read_bytes())=='4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da'
for e in cm['files']:
    b=(DEST/'source'/e['path']).read_bytes()
    assert len(b)==e['bytes'] and sha(b)==e['sha256'],e['path']
result={'kind':'INDEPENDENT_ARCHIVE_DATA_CHECK','archive':{'file':SRC.name,'bytes':len(raw),'sha256':sha(raw)},'payload_count':153,'entries':154,'exact_set_size_sha_crc_paths':True,'source_manifest_members':len(cm['files']),'source_manifest_matches_previous_accepted_R1':True,'received_programs_executed':0}
with (ROOT/'INPUT_CHECK.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps(result,ensure_ascii=False))

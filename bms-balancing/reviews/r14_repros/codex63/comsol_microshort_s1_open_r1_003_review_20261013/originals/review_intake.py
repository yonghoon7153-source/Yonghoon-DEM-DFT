"""Reviewer-only archive/data intake; no received code import or execution."""
from pathlib import Path, PurePosixPath
import json, hashlib, zipfile, stat

ROOT = Path(__file__).resolve().parent
SOURCE = Path('C:/Users/Administrator/Downloads/COMSOL_MICROSHORT_S1_OPEN_R1_VALIDATION_003_20261013.zip')
AFTER = Path('C:/Users/Administrator/.codex/attachments/76a81b79-7d12-4f4c-a60d-79b054a5e148/붙여넣은 텍스트.txt')
def sha(b): return hashlib.sha256(b).hexdigest()
raw = SOURCE.read_bytes()
assert len(raw)==665105 and sha(raw)=='6458419127231ce44203ddef9d10981954ae877fdbf990faab5d3649db172bb3'
destination=ROOT/'evidence'
if destination.exists(): raise RuntimeError('Evidence destination already exists')
with zipfile.ZipFile(SOURCE) as z:
    infos=z.infolist()
    assert len(infos)==139
    assert len({i.filename.casefold() for i in infos})==len(infos)
    assert sum(i.file_size for i in infos)<50*1024*1024
    for i in infos:
        n=PurePosixPath(i.filename)
        assert not i.is_dir() and not n.is_absolute() and '..' not in n.parts
        assert ':' not in i.filename and '\\' not in i.filename
        assert not stat.S_ISLNK(i.external_attr>>16)
    data={i.filename:z.read(i) for i in infos}
    manifest=json.loads(data['PACKAGE_MANIFEST.json'])
    assert len(data['PACKAGE_MANIFEST.json'])==24117
    assert sha(data['PACKAGE_MANIFEST.json'])=='0345322ff029459bb421a8b249f785c06e46455fdaa8beb5f69ba9ff42975961'
    expected={r['entry']:r for r in manifest['files']}
    assert len(expected)==138 and set(expected)==set(data)-{'PACKAGE_MANIFEST.json'}
    for name,row in expected.items():
        assert len(data[name])==row['bytes'] and sha(data[name])==row['sha256'],name
    assert z.testzip() is None
    for name,b in data.items():
        target=destination/name
        target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('xb') as stream: stream.write(b)
after=AFTER.read_bytes()
after_json=json.loads(after.decode('utf-8-sig'))
with (ROOT/'POST_PACKAGE_SELECTED_SOURCES_AFTER.json').open('xb') as stream: stream.write(after)
out={'archive':{'path':str(SOURCE),'bytes':len(raw),'sha256':sha(raw)},
     'entries':len(infos),'payload_count':len(expected),'decompressed_bytes':sum(len(b) for b in data.values()),
     'verification':'Exact set, size, SHA256, CRC, casefold, path and symlink checks',
     'after_attachment':{'path':str(AFTER),'bytes':len(after),'sha256':sha(after),'top_keys':list(after_json)},
     'execution':'No supplied code imported or executed. Reviewer data utility only.'}
with (ROOT/'INTAKE_CHECK.json').open('x',encoding='utf-8') as stream: json.dump(out,stream,ensure_ascii=False,indent=2)
print(json.dumps(out,ensure_ascii=False))

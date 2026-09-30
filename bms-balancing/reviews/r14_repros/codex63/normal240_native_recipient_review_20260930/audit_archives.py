"""Reviewer-owned streaming archive verification; no received code execution."""
import hashlib, json, stat, zipfile
from pathlib import Path, PurePosixPath
ROOT=Path(__file__).resolve().parent
SOURCES=[Path('C:/Users/Administrator/Downloads')/n for n in ['COMSOL63_NORMAL240_NATIVE_RESULT_20260930.zip','NORMAL240_NATIVE_DELIVERY_SUPPLEMENT_20260930.zip']]
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
records=[]
for source,folder in zip(SOURCES,['received','supplement']):
    before={'bytes':source.stat().st_size,'sha256':sha(source)}
    dest=ROOT/folder
    assert not dest.exists(), 'No extraction overwrite'
    with zipfile.ZipFile(source) as z:
        infos=z.infolist(); names=[x.filename for x in infos]
        assert len(names)==len(set(names))==len({x.casefold() for x in names})
        assert sum(x.file_size for x in infos)<10*1024**3
        for i in infos:
            p=PurePosixPath(i.filename)
            assert not p.is_absolute() and all(x not in ('','.','..') for x in i.filename.split('/'))
            assert '\\' not in i.filename and ':' not in i.filename and not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16)
        raw=z.read('MANIFEST.json'); m=json.loads(raw); entries=m['files']
        assert len({e['file'] for e in entries})==len(entries)
        assert set(names)=={e['file'] for e in entries}|{'MANIFEST.json'}
        identities={}
        for e in entries:
            info=z.getinfo(e['file']); assert info.file_size==e['bytes']
            target=dest/e['file']; target.parent.mkdir(parents=True,exist_ok=True); h=hashlib.sha256()
            with z.open(info) as stream,target.open('xb') as out:
                while chunk:=stream.read(1024*1024): h.update(chunk);out.write(chunk)
            assert h.hexdigest()==e['sha256'],e['file']
            identities[e['file']]={'bytes':info.file_size,'sha256':h.hexdigest()}
        (dest/'MANIFEST.json').write_bytes(raw)
        r={'file':str(source),**before,'payload':len(entries),'entries':len(infos),'manifest_bytes':len(raw),'manifest_sha256':hashlib.sha256(raw).hexdigest(),'exact_set_size_sha_crc_path_case_link':True,'members':identities}
        records.append(r)
        print(json.dumps({k:v for k,v in r.items() if k!='members'}),flush=True)
    assert before=={'bytes':source.stat().st_size,'sha256':sha(source)}
assert records[1]['bytes']==41791 and records[1]['sha256']=='b45ec184ddfc6f54153a0f6a06e88d638035d11ebf1b183982cf3636e16d3bd0'
(ROOT/'ARCHIVE_AUDIT.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

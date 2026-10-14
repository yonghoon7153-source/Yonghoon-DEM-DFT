from pathlib import Path, PurePosixPath
import hashlib, json, shutil, tarfile

R=Path(__file__).resolve().parent
OLD=R.parent/'rint_g2_impl_review_20261014'
ARCHIVE=Path('C:/Users/Administrator/Downloads/lhs214_run_evidence_1014_1520.tgz')
REQUEST=Path('C:/Users/Administrator/Downloads/codex_lhs_run214_failures_request_20261014.md')
for name in ['source','submitted','evidence','probes','notes','tmp']:(R/name).mkdir(parents=True,exist_ok=True)
m=json.loads((OLD/'source_manifest.json').read_text(encoding='utf8'))
assert m['pin']=='1087a9b2f4a93aa6a3b0debc698a14fffa13488d'
for f in m['files']:
    src=OLD/'source'/f['path']; data=src.read_bytes()
    assert hashlib.sha256(data).hexdigest()==f['sha256'],f['path']
    dst=R/'source'/f['path'];dst.parent.mkdir(parents=True,exist_ok=True)
    if not dst.exists():shutil.copyfile(src,dst)
    assert hashlib.sha256(dst.read_bytes()).hexdigest()==f['sha256']
shutil.copyfile(OLD/'source_manifest.json',R/'source_manifest.json')
shutil.copyfile(REQUEST,R/'submitted'/REQUEST.name)
shutil.copyfile(ARCHIVE,R/'submitted'/ARCHIVE.name)
inventory=[]
base=(R/'submitted').resolve()
with tarfile.open(ARCHIVE,'r:gz') as t:
    names=set()
    for member in t.getmembers():
        p=PurePosixPath(member.name)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in member.name and ':' not in member.name,member.name
        assert member.name not in names,member.name
        names.add(member.name)
        assert member.isdir() or member.isfile(),member.name
        target=(base/Path(*p.parts)).resolve()
        assert target.is_relative_to(base)
        if member.isdir():target.mkdir(parents=True,exist_ok=True);continue
        data=t.extractfile(member).read();assert len(data)==member.size
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(data)
        inventory.append({'path':p.as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
record={'pin':m['pin'],'archive':ARCHIVE.name,'archive_bytes':ARCHIVE.stat().st_size,'archive_sha256':hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),'archive_hazards':[],'files':inventory,'reused_source_files_verified':len(m['files'])}
(R/'evidence/input_inventory.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:v for k,v in record.items() if k!='files'},ensure_ascii=False,indent=2))
print('archive_files',len(inventory),'unpacked_bytes',sum(f['bytes'] for f in inventory))

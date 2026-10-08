"""Reviewer-owned archive data verification. No received code imports/calls."""
from pathlib import Path, PurePosixPath
import hashlib,json,stat,zipfile
ROOT=Path(__file__).resolve().parent
DOWNLOADS=Path('C:/Users/Administrator/Downloads')
SPECS=[('main','COMSOL_MICROSHORT_S1O_R1_OFFLINE_CORRECTIONS_20261008 (1).zip',813053,'0a18cb64f8bcbcd4725b45088ee310f85e9292a1ffdced2332b5102f5fd6f9dc','PACKAGE_MANIFEST.json',116),('supplement','COMSOL_MICROSHORT_S1O_R1_DELIVERY_SUPPLEMENT_20261008 (1).zip',3750,'4cfd310ae5c019cce63a2ce012debfa9307f44ac739c1253cc07a5cf0c8d73b2','MANIFEST.json',4)]
def sha(b):return hashlib.sha256(b).hexdigest()
results=[]
for label,name,size,expected,mname,count in SPECS:
    dest=ROOT/'received'/label
    if dest.exists():raise RuntimeError('Existing output '+str(dest))
    raw=(DOWNLOADS/name).read_bytes()
    assert len(raw)==size and sha(raw)==expected
    with zipfile.ZipFile(DOWNLOADS/name) as z:
        names=z.namelist();assert len(names)==len(set(names))==len({n.casefold() for n in names})
        assert sum(i.file_size for i in z.infolist())<30*1024*1024
        for info in z.infolist():
            p=PurePosixPath(info.filename)
            assert not p.is_absolute() and '..' not in p.parts and ':' not in info.filename and '\\' not in info.filename
            assert not stat.S_ISLNK(info.external_attr>>16) and not info.is_dir()
        mb=z.read(mname);m=json.loads(mb);entries={i['path']:i for i in m['files']}
        assert len(entries)==len(m['files'])==count and set(names)==set(entries)|{mname}
        payload={}
        for n in names:
            data=z.read(n)
            if n in entries:assert len(data)==entries[n]['bytes'] and sha(data)==entries[n]['sha256'],n
            payload[n]=data
        assert z.testzip() is None
    for n,b in payload.items():
        p=dest/n;p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb') as f:f.write(b)
    results.append({'label':label,'file':name,'bytes':size,'sha256':expected,'payload':count,'entries':len(names),'manifest_bytes':len(mb),'manifest_sha256':sha(mb),'exact_set_size_sha_crc_paths':True})
main=ROOT/'received/main'
cm=json.loads((main/'CODE_MANIFEST.json').read_text(encoding='utf8'))
assert sha((main/'CODE_MANIFEST.json').read_bytes())=='4ce5c08dbde5153027819b5a651e3995ec82417b4429b9bb0f789082b440f5da'
for entry in cm['files']:
    b=(main/entry['path']).read_bytes();assert len(b)==entry['bytes'] and sha(b)==entry['sha256'],entry['path']
result={'scope':'Data-only archive inspection','archives':results,'code_manifest_count':len(cm['files']),'all_code_manifest_entries_match':True,'received_programs_executed':0}
with (ROOT/'INPUT_CHECK.json').open('x',encoding='utf8') as f:json.dump(result,f,ensure_ascii=False,indent=2)
print(json.dumps(result,ensure_ascii=False))

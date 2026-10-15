"""Safe read-only intake of v3.3 review package. Never execute submitted code."""
from pathlib import Path, PurePosixPath
import hashlib, json, shutil, stat, zipfile

ROOT = Path(__file__).resolve().parent
DL = Path('C:/Users/Administrator/Downloads')
ZIP = DL/'codex_seminar_deck_v3_3_closure_20261015.zip'
OUT = ROOT/'input'
def sha(b): return hashlib.sha256(b).hexdigest()
ROOT.joinpath('evidence').mkdir(parents=True, exist_ok=True)
OUT.mkdir(exist_ok=True)
audit={'zip':str(ZIP),'sha256':sha(ZIP.read_bytes()),'bytes':ZIP.stat().st_size,'members':[]}
with zipfile.ZipFile(ZIP) as z:
    assert z.testzip() is None
    names=set(); roots=set()
    for m in z.infolist():
        p=PurePosixPath(m.filename)
        assert not p.is_absolute() and '..' not in p.parts and '\\' not in m.filename and ':' not in m.filename
        assert not stat.S_ISLNK(m.external_attr >> 16)
        assert m.filename.casefold() not in names
        names.add(m.filename.casefold()); roots.add(p.parts[0])
        assert m.file_size < 200_000_000
    assert len(roots)==1
    root=next(iter(roots))
    for m in z.infolist():
        if m.is_dir(): continue
        rel=PurePosixPath(m.filename).relative_to(root)
        dest=OUT.joinpath(*rel.parts)
        data=z.read(m)
        dest.parent.mkdir(parents=True,exist_ok=True)
        if dest.exists(): assert dest.read_bytes()==data
        else: dest.write_bytes(data)
        audit['members'].append({'path':str(rel),'bytes':len(data),'sha256':sha(data)})
audit['standalone_matches']={}
for suffix in ['pdf','pptx']:
    name='seminar_20261013_v33.'+suffix
    data=(DL/name).read_bytes()
    audit['standalone_matches'][name]={'sha256':sha(data),'same_as_package':data==(OUT/'deck'/name).read_bytes()}
    assert audit['standalone_matches'][name]['same_as_package']
checks=[]
for line in (OUT/'MANIFEST.sha256').read_text(encoding='utf-8-sig').splitlines():
    if not line.strip(): continue
    digest,rel=line.split(maxsplit=1)
    rel=PurePosixPath(rel.lstrip('*').strip()).as_posix()
    target=OUT.joinpath(*PurePosixPath(rel).parts)
    checks.append({'path':rel,'exists':target.is_file(),'match':target.is_file() and sha(target.read_bytes())==digest})
audit['manifest_checks']=checks
audit['all_manifest_matches']=all(c['match'] for c in checks)
audit['manifest_exact_members']=set(c['path'] for c in checks)==set(m['path'] for m in audit['members'] if m['path']!='MANIFEST.sha256')
audit['pin_text']=(OUT/'PIN.txt').read_text(encoding='utf-8')
(ROOT/'evidence/intake.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in audit.items() if k not in ['members','manifest_checks']},ensure_ascii=False,indent=2))

import hashlib,json,zipfile
from pathlib import Path
root=Path(__file__).resolve().parent
initial=json.loads((root/'integrity.json').read_text(encoding='utf-8'))
changed=[]
for f in initial['repo_files']:
    p=root/'package/repo'/f['path']
    if hashlib.sha256(p.read_bytes()).hexdigest()!=f['sha256']:changed.append(f['path'])
assert not changed,changed
(root/'final_source_preservation.json').write_text(json.dumps({'files':len(initial['repo_files']),'changed':changed,'source_pin':initial['pin']},indent=2)+'\n',encoding='utf-8')
def include(p):
    rel=p.relative_to(root)
    if rel.parts[0]=='package':return p.is_file()
    if any(part in ('temp','tmp','__pycache__','.git') or part.startswith('scratch') for part in rel.parts):return False
    if p.suffix=='.zip':return False
    if p.parent==root and (p.name in ('EVIDENCE_MANIFEST.sha256','delivery.json') or p.name.endswith('.zip.sha256')):return False
    return p.is_file()
files=sorted((p for p in root.rglob('*') if include(p)),key=lambda p:p.relative_to(root).as_posix())
lines=[hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(root).as_posix() for p in files]
manifest=root/'EVIDENCE_MANIFEST.sha256';manifest.write_text('\n'.join(lines)+'\n',encoding='utf-8')
dest=root/'codex_rint2_rr_round3_independent_review_17d45fb9cdfc_20261108.zip'
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=8) as z:
    for p in files+[manifest]:z.write(p,p.relative_to(root).as_posix())
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    names=z.namelist();assert len(names)==len(set(names))
    for line in z.read('EVIDENCE_MANIFEST.sha256').decode('utf-8').splitlines():
        sha,name=line.split('  ',1);assert hashlib.sha256(z.read(name)).hexdigest()==sha,name
    assert len([n for n in names if n.startswith('package/repo/')])==660
sha=hashlib.sha256(dest.read_bytes()).hexdigest()
delivery={'zip':dest.name,'bytes':dest.stat().st_size,'sha256':sha,'entries':len(names),'manifest_entries':len(lines),'source_unchanged':660,'verdict':'HOLD','new_findings':['RR3-01 P2','RR3-02 P3']}
(root/'delivery.json').write_text(json.dumps(delivery,indent=2)+'\n',encoding='utf-8')
(root/(dest.name+'.sha256')).write_text(sha+'  '+dest.name+'\n',encoding='utf-8')
print(json.dumps(delivery))

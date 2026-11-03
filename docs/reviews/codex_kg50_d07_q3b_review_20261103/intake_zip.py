from pathlib import Path, PurePosixPath
import hashlib,json,re,zipfile
base=Path(__file__).resolve().parent
zp=Path(r'C:/Users/Administrator/Downloads/codex_kg50_d07_compress_resume_20261103.zip')
out=base/'received_zip'
z=zipfile.ZipFile(zp)
seen=set(); hazards=[]
for item in z.infolist():
    n=item.filename; pp=PurePosixPath(n)
    if pp.is_absolute() or '..' in pp.parts or '\\' in n or ':' in n or n.casefold() in seen or ((item.external_attr>>16)&0o170000)==0o120000:
        hazards.append(n)
    seen.add(n.casefold())
assert not hazards,hazards
rows=[]
for line in z.read('MANIFEST.sha256').decode().splitlines():
    expected,name=line.split('  ',1); name=name.removeprefix('./')
    actual=hashlib.sha256(z.read(name)).hexdigest()
    rows.append(dict(path=name,expected=expected,actual=actual,match=actual==expected))
files={i.filename for i in z.infolist() if not i.is_dir()}
covered={r['path'] for r in rows}
assert len(covered)==len(rows)
assert files-covered=={'MANIFEST.sha256'},files-covered
assert all(r['match'] for r in rows)
for item in z.infolist():
    if item.is_dir():continue
    p=out.joinpath(*PurePosixPath(item.filename).parts)
    p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(item))
comp=[]
for p in (base/'source/repo').rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(base/'source/repo');q=out/'repo'/rel
    comp.append(dict(path=rel.as_posix(),in_zip=q.is_file(),identical=q.is_file() and p.read_bytes()==q.read_bytes()))
r=dict(zip_path=str(zp),sha256=hashlib.sha256(zp.read_bytes()).hexdigest(),bytes=zp.stat().st_size,
       pin=z.read('PIN.txt').decode(),hazards=hazards,verified=len(rows),manifest_all_pass=True,
       files=rows,prior_snapshot_comparison=comp)
(base/'zip_intake.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in r.items() if k not in ('files','prior_snapshot_comparison')},ensure_ascii=False))
print(json.dumps(comp,ensure_ascii=False))

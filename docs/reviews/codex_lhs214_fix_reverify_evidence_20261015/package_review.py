"""Verify immutable inputs and package review outputs, without touching originals."""
from pathlib import Path
import hashlib,json,os,sys,zipfile
R=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def long(p):return Path('\\\\?\\'+str(p)) if os.name=='nt' else p
def read(p):return long(p).read_bytes()
files=set();integrity={}
for label in ('source','base'):
    mf=json.loads((R/f'{label}_manifest.json').read_text(encoding='utf8'))
    checked=[]
    for rec in mf['files']:
        p=R/label/rec['path'];b=read(p)
        assert len(b)==rec['bytes'] and sha(b)==rec['sha256'],str(p)
        assert hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()==rec['git_blob'],str(p)
        files.add(p);checked.append(rec['path'])
    integrity[label]={'pin':mf['pin'],'files':len(checked),'mismatches':0}
(R/'integrity.json').write_text(json.dumps(integrity,indent=2),encoding='utf8')
excluded=('evidence/display_work/','evidence/consumers_temp/','evidence/consumers_release/')
for directory in ('probes','notes','submitted','evidence'):
    for lp in long(R/directory).rglob('*'):
        if not lp.is_file():continue
        p=Path(str(lp)[4:]) if os.name=='nt' else lp
        rel=p.relative_to(R).as_posix()
        if rel.startswith(excluded) or '__pycache__' in p.parts:continue
        files.add(p)
for p in R.iterdir():
    if p.is_file() and p.suffix in ('.md','.py','.json') and p.name not in ('package_manifest.json','package_result.json'):
        files.add(p)
rows=[]
for p in sorted(files):
    b=read(p);rows.append({'path':p.relative_to(R).as_posix(),'bytes':len(b),'sha256':sha(b)})
(R/'package_manifest.json').write_text(json.dumps({'files':rows,'excluded_scratch':excluded,'integrity':integrity},ensure_ascii=False,indent=2),encoding='utf8')
target=R.parent/'codex_lhs214_fix_reverify_20261015.zip'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for rec in rows:z.writestr(rec['path'],read(R/rec['path']))
    z.write(R/'package_manifest.json','package_manifest.json')
    z.writestr('tmp/.keep','Review-only temporary files may be created here.\n')
with zipfile.ZipFile(target) as z:
    assert z.testzip() is None
    for rec in rows:assert sha(z.read(rec['path']))==rec['sha256'],rec['path']
    assert len(z.namelist())==len(set(z.namelist()))
result={'zip':str(target),'bytes':target.stat().st_size,'sha256':sha(target.read_bytes()),'files':len(rows)+2,'uncompressed_bytes':sum(r['bytes'] for r in rows),'integrity':integrity,'zip_readback':'all_sha256_match'}
(R/'package_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(result,ensure_ascii=False,indent=2))

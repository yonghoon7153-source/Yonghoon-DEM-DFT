"""Verify immutable source and package this review; no source or Git writes."""
from pathlib import Path
import hashlib,json,os,zipfile
R=Path(__file__).resolve().parent;W=R.parent
def read(p):return Path('\\\\?\\'+str(p.resolve())).read_bytes() if os.name=='nt' else p.read_bytes()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
audits=[]
for label,root,mf in [('current',R/'source',R/'source_manifest.json'),('prior_source',W/'lhs214r_fix_recheck_20261017/source',W/'lhs214r_fix_recheck_20261017/source_manifest.json'),('prior_base',W/'lhs214r_fix_recheck_20261017/base',W/'lhs214r_fix_recheck_20261017/base_manifest.json')]:
    rows=json.loads(read(mf))['files'];bad=[]
    for row in rows:
        actual=sha(read(root/row['path']))
        if actual!=row['sha256']:bad.append(dict(path=row['path'],expected=row['sha256'],actual=actual))
    audits.append(dict(label=label,checked=len(rows),bad=bad));assert not bad,(label,bad[:3])
save(R/'evidence/source_integrity_final.json',audits)
# Retain original probe bytes the derived replay files read, with exact hashes.
ref=R/'prior_reference';ref.mkdir(exist_ok=True)
old=W/'lhs214r_fix_recheck_20261017'
reference=[]
for p in sorted((old/'probes').glob('*')):
    if p.is_file():
        b=read(p);q=ref/p.name;q.write_bytes(b);reference.append(dict(original=str(p),copy='prior_reference/'+p.name,sha256=sha(b)))
save(ref/'manifest.json',reference)
report=read(R/'codex_review_lhs214rr_fix_recheck_20261019.md').decode('utf8')
assert all(s in report for s in ['23/26','36/36','113/113','새 P1/P2는 찾지 못했다','전체 요청 종결: 부분'])
files=[]
for p in R.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(R).as_posix()
    if rel.split('/')[0] in ('deps','tmp') or '/__pycache__/' in rel or rel=='PACKAGE_MANIFEST.json':continue
    b=read(p);files.append(dict(path=rel,bytes=len(b),sha256=sha(b)))
files.sort(key=lambda x:x['path'])
save(R/'PACKAGE_MANIFEST.json',dict(pin='77d8fd44545c33cd10ab18fc250c7ad3023833ea',files=files,excludes=['deps','tmp','__pycache__','manifest self'],reproduction_dependency='prior review source/base snapshots and dependency roots; README'))
z=W/'codex_lhs214rr_fix_recheck_20261019.zip'
with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as f:
    for row in files:f.writestr(R.name+'/'+row['path'],read(R/row['path']))
    f.writestr(R.name+'/PACKAGE_MANIFEST.json',read(R/'PACKAGE_MANIFEST.json'))
with zipfile.ZipFile(z) as f:
    assert f.testzip() is None
    assert len(f.namelist())==len(set(f.namelist()))==len(files)+1
    for row in files:assert sha(f.read(R.name+'/'+row['path']))==row['sha256'],row['path']
receipt=dict(zip=str(z),bytes=z.stat().st_size,sha256=sha(read(z)),entries=len(files)+1,crc='PASS',file_hashes='PASS',source_integrity=audits)
save(z.with_suffix('.receipt.json'),receipt)
print(json.dumps(receipt,ensure_ascii=False,indent=2))

"""Final read-only source QA and evidence packaging. No repository/Git mutation."""
from pathlib import Path
import hashlib, json, os, zipfile

R=Path(__file__).resolve().parent
def long(p):
    return Path('\\\\?\\'+str(p)) if os.name=='nt' else p
def read(p): return long(p).read_bytes()
def dump(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf8')
manifest=json.loads(read(R/'source_manifest.json'))
bad=[]
for f in manifest['files']:
    b=read(R/'source'/f['path'])
    blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    if hashlib.sha256(b).hexdigest()!=f['sha256'] or blob!=f['sha']:
        bad.append(f['path'])
assert not bad, bad
dg=json.loads(read(R/'evidence/digest_probe/results.json'))
co=json.loads(read(R/'evidence/completion_probe/results.json'))
en=json.loads(read(R/'evidence/completion_environment/summary.json'))
assert dg['passed']==dg['total']==42
assert len(co['cases'])==40 and all(x['expected'] for x in co['cases'])
assert en['runs'][1]['rc']==0 and '88/88' in en['runs'][1]['final_line']
assert en['bootstrapped_real_generation']['generation']=='g2'
assert en['bootstrapped_real_generation']['problems']==[]
qa=dict(pin=dg['pin'], source_files=len(manifest['files']),source_modified=bad,
        digest_cases=dg['passed'],completion_cases=len(co['cases']),
        receipt_selftest='88/88 with dependency bootstrap only; untouched first run 79/88 (missing SciPy)',
        release='254/256 with scientific dependencies; Windows path and missing checkout HEAD failures retained',
        production_runs=False,repository_edits=False)
dump(R/'evidence/final_qa.json',qa)

files=[]
for current, dirs, names in os.walk(long(R)):
    dirs[:]=[d for d in dirs if d not in ('tmp','__pycache__','.git')]
    for n in names:
        if n.endswith(('.pyc','.pyo')) or n=='package_manifest.json':continue
        p=Path(current)/n
        normal=Path(str(p)[4:]) if str(p).startswith('\\\\?\\') else p
        rel=normal.relative_to(R).as_posix()
        b=p.read_bytes()
        files.append((rel,b))
assert not any('/tmp/' in rel for rel,b in files)
listing=dict(schema='review_evidence/v1',pin=dg['pin'],
             files=[dict(path=rel,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()) for rel,b in sorted(files)])
dump(R/'package_manifest.json',listing)
files.append(('package_manifest.json',read(R/'package_manifest.json')))
archive=R.parent/'codex_supr_fix_reverify_df647d4e3_20261014.zip'
if archive.exists(): raise RuntimeError('Do not overwrite existing review archive')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for rel,b in sorted(files):z.writestr('supr_reverify_20261014/'+rel,b)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(files)
record=dict(path=str(archive),bytes=archive.stat().st_size,
            sha256=hashlib.sha256(archive.read_bytes()).hexdigest(),entries=len(files),crc='PASS')
dump(R.parent/'codex_supr_fix_reverify_df647d4e3_20261014.package.json',record)
print(json.dumps(record))
